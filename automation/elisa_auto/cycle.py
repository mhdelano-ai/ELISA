"""Declarative cycle/step tables (config/cycle_*.yaml): loading, validation and timing arithmetic.

Times in a table are *cycle minutes*: t = 0 is the start of the SM-FL sample aspiration. Inject events
(``injects``) are the anchors: once an Inject Start edge arrives, every later step is timed from that edge's actual
arrival, so Empower-side drift does not accumulate (docs/02 s3.2 point 3).
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path

import yaml

VALID_POT_ACTIONS = {None, "start_acquisition", "mark", "stop_acquisition"}
VALID_SIA_ACTIONS = {"dispense", "mix", "empty_cup_through_trap", "rinse_cup", "aspirate", "flush_channel",
                     "flush_trap"}
VALID_SMFL = {None, "aspirate", "inject", "needle_wash", "idle"}
# SIA actions that send liquid through the trap via the tee upstream of V2 (docs/05 s4.1 plumbing)
SIA_THROUGH_TRAP = {"empty_cup_through_trap", "flush_trap"}


class CycleError(ValueError):
    pass


@dataclass(frozen=True)
class Step:
    name: str
    start_min: float
    end_min: float
    valves: dict = field(default_factory=dict)
    magnet: str | None = None
    sia: dict | None = None
    potentiostat: str | None = None
    role: str | None = None
    empower: str | None = None
    note: str | None = None
    # structured Empower-side facts, checked by validate() (added after the final review, docs/08 S2, S3):
    bsm: dict | None = None        # {flow_uL_min: x, solvent: A1|B1|...}: what the BSM programme does in this step
    smfl: str | None = None        # aspirate | inject | needle_wash | idle: what the SM-FL does in this step

    @property
    def duration_min(self) -> float:
        return self.end_min - self.start_min


@dataclass(frozen=True)
class Inject:
    name: str
    at_min: float
    line_code: int | None = None


@dataclass
class Cycle:
    name: str
    mode: str
    source: str
    time_limit_min: float
    injects: list[Inject]
    steps: list[Step]
    watchdog: dict
    safe_state: dict
    potentiostat: dict
    signal: dict
    constraints: dict = field(default_factory=dict)
    path: str | None = None
    sha256: str | None = None

    # ---- derived timing ---------------------------------------------------------------------------------
    @property
    def start_min(self) -> float:
        return self.steps[0].start_min

    @property
    def end_min(self) -> float:
        return self.steps[-1].end_min

    @property
    def first_inject_min(self) -> float | None:
        return self.injects[0].at_min if self.injects else None

    @property
    def is_recovery(self) -> bool:
        return self.mode == "recovery"

    def time_to_result_min(self) -> float | None:
        """Injection (first Inject Start) to result (end of readout window + post baseline = signal available).

        docs/05 quotes 'time to result' as the cycle end (56.1 min, counted from the aspiration start, which is
        conservative by the 1 min aspiration); both are reported by ``timing_summary``. None for a recovery cycle."""
        if not self.signal or not self.injects:
            return None
        return self.signal_end_min() - self.first_inject_min

    def signal_end_min(self) -> float:
        return max(w[1] for w in self.signal.values())

    def anchor_for(self, t_min: float) -> Inject | None:
        """The inject event that times cycle time t (latest inject with at_min <= t), or None (before the first)."""
        a = None
        for inj in self.injects:
            if inj.at_min <= t_min + 1e-9:
                a = inj
        return a

    def timing_summary(self) -> dict:
        return {
            "cycle_start_min": self.start_min,
            "cycle_end_min": self.end_min,
            "first_inject_min": self.first_inject_min,
            "cycle_duration_from_aspiration_min": round(self.end_min - 0.0, 6),
            "inject_to_signal_min": (None if self.time_to_result_min() is None
                                     else round(self.time_to_result_min(), 6)),
            "time_limit_min": self.time_limit_min,
        }


def _as_step(d: dict) -> Step:
    known = {f for f in Step.__dataclass_fields__}
    extra = set(d) - known
    if extra:
        raise CycleError(f"step {d.get('name')!r}: unknown keys {sorted(extra)}")
    d = dict(d)
    if d.get("magnet") is True:      # YAML 1.1 'on' safety
        d["magnet"] = "on"
    if d.get("magnet") is False:
        d["magnet"] = "off"
    d["valves"] = dict(d.get("valves") or {})
    return Step(**d)


def load_cycle(path: str | Path) -> Cycle:
    path = Path(path)
    raw_text = path.read_text(encoding="utf-8")
    raw = yaml.safe_load(raw_text)
    cyc = Cycle(
        name=raw["name"], mode=raw["mode"], source=raw.get("source", ""),
        time_limit_min=float(raw.get("time_limit_min", 60)),
        injects=[Inject(**i) for i in raw["injects"]],
        steps=[_as_step(s) for s in raw["steps"]],
        watchdog=dict(raw.get("watchdog", {})),
        safe_state=dict(raw.get("safe_state", {})),
        potentiostat=dict(raw.get("potentiostat", {})),
        signal={k: tuple(float(x) for x in v) for k, v in (raw.get("signal") or {}).items()},
        constraints=dict(raw.get("constraints") or {}),
        path=str(path), sha256=hashlib.sha256(raw_text.encode()).hexdigest(),
    )
    if isinstance(cyc.safe_state.get("magnet"), bool):
        cyc.safe_state["magnet"] = "on" if cyc.safe_state["magnet"] else "off"
    validate(cyc)
    return cyc


def effective_valves(c: Cycle, initial: dict | None = None) -> list[dict]:
    """Valve state during each step (a step's valves dict changes only the valves it names)."""
    state, out = dict(initial or {}), []
    for s in c.steps:
        state.update(s.valves)
        out.append(dict(state))
    return out


def trap_flow_uL_min(step: Step, valves: dict) -> float | None:
    """Flow through the trap while the SIA pushes liquid to it through the tee (docs/05 s4.1 plumbing): the SIA
    flow plus the BSM flow, which reaches the same tee whenever V4 is in position B. None if no SIA push."""
    if not step.sia or step.sia.get("action") not in SIA_THROUGH_TRAP:
        return None
    q = float(step.sia.get("flow_uL_min", 0.0))
    if valves.get("V4") == "B" and step.bsm is not None:
        q += float(step.bsm.get("flow_uL_min", 0.0))
    return q


def sia_ports_used(c: Cycle) -> set:
    used = set()
    for s in c.steps:
        if s.sia:
            for k in ("from", "to", "port"):
                if s.sia.get(k):
                    used.add(s.sia[k])
    return used


def validate(c: Cycle, valve_positions: dict | None = None, sia_ports: dict | list | None = None) -> None:
    """Raise CycleError on any inconsistency. valve_positions: {valve: [allowed positions]}; sia_ports: names of
    the SIA selection-valve ports of the hardware (optional; checked when given)."""
    if not c.steps:
        raise CycleError("no steps")
    if not c.injects and not c.is_recovery:
        raise CycleError("only a recovery cycle may have no inject")
    if c.is_recovery and c.signal:
        raise CycleError("a recovery cycle has no signal windows")
    prev_end = None
    names = set()
    for s in c.steps:
        if s.name in names:
            raise CycleError(f"duplicate step name {s.name}")
        names.add(s.name)
        if s.end_min <= s.start_min:
            raise CycleError(f"step {s.name}: end {s.end_min} <= start {s.start_min}")
        if prev_end is not None and abs(s.start_min - prev_end) > 1e-9:
            raise CycleError(f"step {s.name}: starts at {s.start_min}, previous step ended at {prev_end} (gap/overlap)")
        prev_end = s.end_min
        if s.potentiostat not in VALID_POT_ACTIONS:
            raise CycleError(f"step {s.name}: unknown potentiostat action {s.potentiostat}")
        if s.sia is not None and s.sia.get("action") not in VALID_SIA_ACTIONS:
            raise CycleError(f"step {s.name}: unknown SIA action {s.sia.get('action')}")
        if s.magnet not in (None, "on", "off"):
            raise CycleError(f"step {s.name}: magnet must be on/off")
        if s.smfl not in VALID_SMFL:
            raise CycleError(f"step {s.name}: unknown SM-FL action {s.smfl}")
        if s.bsm is not None and float(s.bsm.get("flow_uL_min", -1)) < 0:
            raise CycleError(f"step {s.name}: bsm needs flow_uL_min >= 0")
        if valve_positions:
            for v, pos in s.valves.items():
                if v not in valve_positions:
                    raise CycleError(f"step {s.name}: unknown valve {v}")
                if pos not in valve_positions[v]:
                    raise CycleError(f"step {s.name}: valve {v} has no position {pos!r}")
    # S3: every SM-FL injection must be a declared inject (the sequencer faults on an undeclared Inject Start)
    inj_steps = [s for s in c.steps if s.smfl == "inject"]
    for s in inj_steps:
        if not any(abs(i.at_min - s.start_min) < 1e-9 for i in c.injects):
            raise CycleError(f"step {s.name}: SM-FL injection at {s.start_min} min is not a declared inject")
    if inj_steps or any(s.smfl for s in c.steps):
        for i in c.injects:
            if not any(abs(i.at_min - s.start_min) < 1e-9 for s in inj_steps):
                raise CycleError(f"inject {i.name}: no step declares the SM-FL injection (smfl: inject)")
    # S2: flow through the trap where two pumps meet at the tee
    qmax = c.constraints.get("max_trap_loading_flow_uL_min")
    for s, v in zip(c.steps, effective_valves(c, c.safe_state.get("valves"))):
        q = trap_flow_uL_min(s, v)
        if q is None:
            continue
        if v.get("V4") == "B" and s.bsm is None:
            raise CycleError(f"step {s.name}: SIA pushes through the tee while V4 = B, but the BSM flow is not "
                             "declared (bsm: {flow_uL_min: ...})")
        if qmax is not None and q > float(qmax) + 1e-9:
            raise CycleError(f"step {s.name}: trap flow {q:g} uL/min (SIA + BSM at the tee) > {qmax} uL/min")
    if sia_ports is not None:
        missing = sia_ports_used(c) - set(sia_ports)
        if missing:
            raise CycleError(f"SIA ports {sorted(missing)} used by the cycle are not defined in the hardware")
    ats = [i.at_min for i in c.injects]
    if ats != sorted(ats):
        raise CycleError("injects must be in time order")
    for i in c.injects:
        if not (c.start_min <= i.at_min < c.end_min):
            raise CycleError(f"inject {i.name} at {i.at_min} outside the cycle")
        if not any(abs(s.start_min - i.at_min) < 1e-9 for s in c.steps):
            raise CycleError(f"inject {i.name} at {i.at_min} min does not coincide with a step start")
    for k, (a, b) in c.signal.items():
        if b <= a:
            raise CycleError(f"signal window {k} is empty")
        if c.anchor_for(a) is None:
            raise CycleError(f"signal window {k} lies before the first inject")
    acq = [s.name for s in c.steps if s.potentiostat == "start_acquisition"]
    stop = [s.name for s in c.steps if s.potentiostat == "stop_acquisition"]
    if c.signal and (len(acq) != 1 or len(stop) != 1):
        raise CycleError("exactly one start_acquisition and one stop_acquisition step are required")
    if c.signal:
        t_acq = next(s.start_min for s in c.steps if s.potentiostat == "start_acquisition")
        t_stop = next(s.start_min for s in c.steps if s.potentiostat == "stop_acquisition")
        for k, (a, b) in c.signal.items():
            if a < t_acq - 1e-9 or b > t_stop + 1e-9:
                raise CycleError(f"signal window {k} not inside the acquisition ({t_acq}-{t_stop} min)")
    if c.end_min - 0.0 > c.time_limit_min + 1e-9:
        raise CycleError(f"cycle ends at {c.end_min} min > limit {c.time_limit_min} min")
    ttr = c.time_to_result_min()
    if ttr is not None and ttr > c.time_limit_min + 1e-9:
        raise CycleError("time to result exceeds the limit")
    for key in ("valves",):
        if key not in c.safe_state:
            raise CycleError("safe_state must define valves")
