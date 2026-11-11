"""Cycle sequencer with timing, watchdog, safe state and run log (docs/02 s3.2 primary scheme; docs/05 s4.1).

Empower is the fluidic master. Python arms a cycle, performs the steps that precede the sample injection (SIA
dose), then waits for the SM-FL Inject Start edge; every later action is timed from the most recent Inject Start
edge (anchor), so Empower's run-to-run timing drift does not accumulate. Watchdog (docs/02 s3.2 point 6):
  * an expected Inject Start that is later than its tolerance, arrives with the wrong line code, or arrives when
    none is expected -> fault;
  * any device error (DeviceError, NotImplementedError from a stub, or anything else) -> fault;
  * on a fault every safe-state item is attempted independently (V2 isolate, V3 bypass, V4 B, SIA stop, magnet
    on, cell off), the fault is logged, and the run ends with status 'fault'. Python never starts or stops Empower;
    the BSM keeps flowing to waste through the shunt and the bypass.
Fault latch (docs/08 S12, latch.py): when a FaultLatch is given, a fault sets it; while it is set every run is
still executed but marked valid = False (metadata, result, run log); a recovery cycle (mode 'recovery') that
completes with status 'ok' clears it.
Limitation (stated): if the PC or this process dies, valves keep their last position. A hardware watchdog
(e.g. a DAQ output heartbeat that drops the cell relay) is a Stage-2 TODO (docs/06 E2.1).
"""
from __future__ import annotations

import json
import platform
from dataclasses import dataclass, field

from . import signal_proc
from .cycle import Cycle, validate
from .devices.base import DeviceError
from .runlog import RunLog


class SequenceFault(RuntimeError):
    pass


@dataclass
class Action:
    cycle_min: float
    order: int
    kind: str
    payload: object
    step: str


@dataclass
class RunResult:
    status: str                      # 'ok' or 'fault'
    run_dir: str
    fault: str | None = None
    signal: dict | None = None
    t0_clock: float | None = None
    anchors: dict = field(default_factory=dict)
    time_to_result_min: float | None = None
    valid: bool = True
    invalid_reason: str | None = None


def build_actions(c: Cycle) -> list[Action]:
    acts = []
    for s in c.steps:
        acts.append(Action(s.start_min, 0, "step_start", {"role": s.role, "duration_min": s.duration_min}, s.name))
        for v, pos in s.valves.items():
            acts.append(Action(s.start_min, 1, "valve", (v, pos), s.name))
        if s.magnet is not None:
            acts.append(Action(s.start_min, 2, "magnet", s.magnet == "on", s.name))
        if s.sia is not None:
            if s.sia.get("action") == "mix":
                every = float(s.sia.get("every_min", 2.0))
                k = 0
                while s.start_min + k * every < s.end_min - 1e-9:
                    acts.append(Action(s.start_min + k * every, 3, "sia", dict(s.sia), s.name))
                    k += 1
            else:
                acts.append(Action(s.start_min, 3, "sia", dict(s.sia), s.name))
        if s.potentiostat is not None:
            acts.append(Action(s.start_min, 4, "pot", (s.potentiostat, s.role or s.name), s.name))
    acts.append(Action(c.end_min, 9, "cycle_end", None, c.steps[-1].name))
    acts.sort(key=lambda a: (a.cycle_min, a.order))
    return acts


class Sequencer:
    def __init__(self, cycle: Cycle, devices, clock, run_dir, poll_s: float = 0.1, metadata: dict | None = None,
                 watchdog_overrides: dict | None = None, latch=None):
        self.c, self.dev, self.clock = cycle, devices, clock
        self.latch = latch
        self.poll_s = poll_s
        self.wd = {**cycle.watchdog, **(watchdog_overrides or {})}
        self.log = RunLog(run_dir, clock)
        self.metadata = dict(metadata or {})
        self.anchor_clock: dict[str, float] = {}
        self._base = None          # clock time of cycle minute 0 before the first anchor
        self.trace = None
        self._acquiring = False

    # ---- time mapping -------------------------------------------------------------------------------------
    def clock_of(self, cycle_min: float) -> float:
        a = self.c.anchor_for(cycle_min)
        if a is not None and a.name in self.anchor_clock:
            return self.anchor_clock[a.name] + (cycle_min - a.at_min) * 60.0
        # before the first anchor, or anchor not yet received: extrapolate from the latest known reference
        ref_name, ref_min = None, None
        for inj in self.c.injects:
            if inj.name in self.anchor_clock and inj.at_min <= cycle_min:
                ref_name, ref_min = inj.name, inj.at_min
        if ref_name is not None:
            return self.anchor_clock[ref_name] + (cycle_min - ref_min) * 60.0
        return self._base + cycle_min * 60.0

    def _next_pending_inject(self):
        for inj in self.c.injects:
            if inj.name not in self.anchor_clock:
                return inj
        return None

    # ---- inject handling ---------------------------------------------------------------------------------
    def _accept(self, ev, inj):
        if ev.line_code is not None and inj.line_code is not None and ev.line_code != inj.line_code:
            raise SequenceFault(f"Inject Start line code {ev.line_code} != expected {inj.line_code} ({inj.name})")
        expected = self.clock_of(inj.at_min)
        self.anchor_clock[inj.name] = ev.t
        self.log.event("inject_start", inj.at_min, inject=inj.name, line_code=ev.line_code,
                       deviation_s=round(ev.t - expected, 3))

    def _poll_injects(self):
        ev = self.dev.inject.poll()
        while ev is not None:
            inj = self._next_pending_inject()
            tol = float(self.wd.get("inject_tolerance_s", 30))
            if inj is None:
                raise SequenceFault(f"unexpected Inject Start at t={ev.t:.1f} s (no injection pending)")
            expected = self.clock_of(inj.at_min)
            first = inj is self.c.injects[0]
            if (not first) and ev.t < expected - tol:
                raise SequenceFault(f"Inject Start for {inj.name} {expected - ev.t:.1f} s early (> {tol} s)")
            self._accept(ev, inj)
            ev = self.dev.inject.poll()

    def _wait_for_inject(self, inj):
        tol = float(self.wd.get("inject_tolerance_s", 30))
        expected = self.clock_of(inj.at_min)
        first = inj is self.c.injects[0]
        deadline = expected + (max(float(self.wd.get("first_inject_max_wait_s", tol)), tol) if first else tol)
        self.log.event("wait_inject", inj.at_min, inject=inj.name, deadline_s=round(deadline - expected, 3))
        while inj.name not in self.anchor_clock:
            self._poll_injects()
            if inj.name in self.anchor_clock:
                break
            if self.clock.now() > deadline:
                raise SequenceFault(f"Inject Start for {inj.name} late by more than {deadline - expected:.0f} s")
            self.clock.sleep(self.poll_s)

    def _sleep_until(self, target: float):
        while True:
            self._poll_injects()
            dt = target - self.clock.now()
            if dt <= 0:
                return
            self.clock.sleep(min(self.poll_s, dt))

    # ---- actions ------------------------------------------------------------------------------------------
    def _do(self, a: Action):
        d = self.dev
        if a.kind == "step_start":
            self.log.event("step_start", a.cycle_min, step=a.step, **a.payload)
        elif a.kind == "valve":
            v, pos = a.payload
            d.valves[v].set_position(pos)
            self.log.event("valve", a.cycle_min, step=a.step, valve=v, position=pos)
        elif a.kind == "magnet":
            d.magnet.set(a.payload)
            self.log.event("magnet", a.cycle_min, step=a.step, on=a.payload)
        elif a.kind == "sia":
            d.sia.execute(a.payload)
            self.log.event("sia", a.cycle_min, step=a.step, command=a.payload)
        elif a.kind == "pot":
            what, label = a.payload
            if what == "start_acquisition":
                d.potentiostat.start_acquisition()
                self._acquiring = True
            elif what == "mark":
                d.potentiostat.mark(label)
            elif what == "stop_acquisition":
                self.trace = d.potentiostat.stop_acquisition()
                self._acquiring = False
            self.log.event("potentiostat", a.cycle_min, step=a.step, action=what, label=label)
        elif a.kind == "cycle_end":
            self.log.event("cycle_end", a.cycle_min)

    def safe_state(self, reason: str):
        ss = self.c.safe_state
        done, failed = [], []
        for v, pos in (ss.get("valves") or {}).items():
            try:
                self.dev.valves[v].set_position(pos)
                done.append(f"{v}={pos}")
            except Exception as e:  # keep going: every item is attempted
                failed.append(f"{v}: {e}")
        if ss.get("sia") == "stop":
            try:
                self.dev.sia.stop()
                done.append("sia=stop")
            except Exception as e:
                failed.append(f"sia: {e}")
        if ss.get("magnet") in ("on", "off"):
            try:
                self.dev.magnet.set(ss["magnet"] == "on")
                done.append(f"magnet={ss['magnet']}")
            except Exception as e:
                failed.append(f"magnet: {e}")
        if ss.get("potentiostat") == "cell_off":
            try:
                if self._acquiring:
                    self.trace = self.dev.potentiostat.stop_acquisition()
                    self._acquiring = False
            except Exception as e:
                failed.append(f"potentiostat stop: {e}")
            try:
                self.dev.potentiostat.cell_off()
                done.append("cell=off")
            except Exception as e:
                failed.append(f"cell_off: {e}")
        self.log.event("safe_state", None, reason=reason, done=done, failed=failed)
        return done, failed

    # ---- main ---------------------------------------------------------------------------------------------
    def run(self, sample: dict | None = None) -> RunResult:
        sample = dict(sample or {})
        c = self.c
        res = RunResult(status="ok", run_dir=str(self.log.dir))
        run_id = self.log.dir.name
        if self.latch is not None and self.latch.is_set and not c.is_recovery:
            st = self.latch.state()
            res.valid = False
            res.invalid_reason = (f"fault latch set by run {st.get('since_run')} ({st.get('reason')}); "
                                  "no recovery cycle completed since")
        meta = {"sample": sample, "cycle": {"name": c.name, "mode": c.mode, "file": c.path, "sha256": c.sha256,
                                           "source": c.source},
                "devices": {"empower": self.dev.empower.describe(),
                            "potentiostat": type(self.dev.potentiostat).__name__,
                            "valves": {k: type(v).__name__ for k, v in self.dev.valves.items()}},
                "clock": "simulated" if self.clock.simulated else "monotonic",
                "host": platform.node(), "python": platform.python_version(), **self.metadata}
        try:
            validate(c, self.dev.valve_positions(), self.dev.sia_ports())
            self._base = self.clock.now() - c.start_min * 60.0
            self.log.event("arm", c.start_min, sample=sample, cycle=c.name)
            if not res.valid:
                self.log.event("invalid_run", c.start_min, reason=res.invalid_reason)
            self.dev.potentiostat.configure(c.potentiostat.get("channels", {}),
                                            c.potentiostat.get("sample_period_s", 0.1))
            warn = float(self.wd.get("step_overrun_warn_s", 2))
            for a in build_actions(c):
                pend = self._next_pending_inject()
                while pend is not None and pend.at_min <= a.cycle_min + 1e-9:
                    self._sleep_until(self.clock_of(pend.at_min))
                    self._wait_for_inject(pend)
                    pend = self._next_pending_inject()
                target = self.clock_of(a.cycle_min)
                self._sleep_until(target)
                late = self.clock.now() - target
                if late > warn:
                    self.log.event("warning", a.cycle_min, message=f"action {a.kind} {late:.1f} s late")
                self._do(a)
            res.anchors = dict(self.anchor_clock)
            res.t0_clock = self.anchor_clock.get(c.injects[0].name) if c.injects else None
            if c.signal and self.trace is not None:
                win = {k: (self.clock_of(a), self.clock_of(b)) for k, (a, b) in c.signal.items()}
                sig = signal_proc.run_signal(self.trace, win)
                res.signal = sig
                t_res = self.clock_of(c.signal_end_min())
                res.time_to_result_min = (t_res - res.t0_clock) / 60.0
                self.log.write_json("result.json", {"S_C": sig["S"], "signal": sig, "sample": sample,
                                                    "time_to_result_min": res.time_to_result_min,
                                                    "windows_clock_s": win, "valid": res.valid,
                                                    "invalid_reason": res.invalid_reason})
        except (SequenceFault, DeviceError, NotImplementedError, Exception) as e:  # noqa: B014 - all faults
            res.status, res.fault = "fault", f"{type(e).__name__}: {e}"
            self.log.event("fault", None, error=res.fault)
            self.safe_state(res.fault)
            if self.latch is not None:
                self.latch.set(run_id, res.fault)
                self.log.event("latch_set", None, reason=res.fault)
        finally:
            if res.status == "ok" and c.is_recovery and self.latch is not None and self.latch.is_set:
                self.latch.clear(run_id)
                self.log.event("latch_cleared", c.end_min, recovery_run=run_id)
            if self.trace is not None:
                meta["trace_sha256"] = self.log.write_trace(self.trace)
                meta["trace_marks"] = self.trace.get("marks")
            meta["status"], meta["fault"] = res.status, res.fault
            meta["valid"], meta["invalid_reason"] = res.valid, res.invalid_reason
            if self.latch is not None:
                meta["fault_latch"] = self.latch.state()
            meta["anchors_clock_s"] = dict(self.anchor_clock)
            self.log.write_json("metadata.json", meta)
            self.log.close()
        return res


def summarize_events(run_dir) -> list[dict]:
    from pathlib import Path
    return [json.loads(l) for l in Path(run_dir, "events.jsonl").read_text().splitlines() if l.strip()]
