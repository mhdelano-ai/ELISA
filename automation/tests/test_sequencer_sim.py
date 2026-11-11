"""End-to-end simulated sequences: timing, device states, watchdog and safe state, run log, signal."""
import json

import pytest

from elisa_auto.clock import SimClock
from elisa_auto.hardware import build_sim
from elisa_auto.sequencer import Sequencer, build_actions, summarize_events


def _run(cycle, hw, tmp_path, q=5e-9, omit=None, extra_delay=None, fail_valve=None, extra_edges=(), **kw):
    clock = SimClock(1000.0)
    dev = build_sim(clock, hw, fail_valve=fail_valve)
    dev.potentiostat.set_true_charge(q)
    dev.empower.plan_cycle(cycle, t_arm=clock.now(), omit=omit, extra_delay=extra_delay)
    for t in extra_edges:
        dev.inject.schedule(clock.now() + t, 1)
    res = Sequencer(cycle, dev, clock, tmp_path / "run", **kw).run({"type": "blank", "conc_pgml": 0})
    return res, dev, clock, summarize_events(tmp_path / "run")


def test_primary_timing_end_to_end(primary, hw_sim, tmp_path):
    res, dev, clock, ev = _run(primary, hw_sim, tmp_path)
    assert res.status == "ok", res.fault
    t0 = res.t0_clock
    assert t0 == pytest.approx(1000.0 + 120.0)          # arm at cycle -1 min, Inject Start at cycle +1 min
    starts = {e["step"]: e["t"] for e in ev if e["kind"] == "step_start"}
    for s in primary.steps:
        if s.start_min >= 1.0:
            assert starts[s.name] - t0 == pytest.approx((s.start_min - 1.0) * 60.0, abs=1e-6), s.name
    end = [e for e in ev if e["kind"] == "cycle_end"][0]
    assert end["t"] - t0 == pytest.approx((56.1 - 1.0) * 60.0, abs=1e-6)
    assert res.time_to_result_min == pytest.approx(52.1)
    assert res.time_to_result_min <= 60.0
    # valve states follow the table: V3 in detect only during accumulation/readout/post-baseline
    v3 = [(e["cycle_min"], e["position"]) for e in ev if e["kind"] == "valve" and e["valve"] == "V3"]
    detect = sorted({cm for cm, p in v3 if p == "detect"})
    assert detect == [41.6, 51.6, 52.6]
    # 15 mixing commands during the 30-min incubation (every 2 min)
    mixes = [e for e in ev if e["kind"] == "sia" and e["command"]["action"] == "mix"]
    assert len(mixes) == 15
    assert dev.magnet.is_on() is False                  # magnet off at cleaning
    # signal: recovers the simulated charge (5 nC) within 1 %
    assert res.signal["S"] == pytest.approx(5e-9, rel=0.01)
    meta = json.loads((tmp_path / "run" / "metadata.json").read_text())
    assert meta["status"] == "ok" and len(meta["trace_sha256"]) == 64
    assert (tmp_path / "run" / "trace.csv").exists()


def test_inject_jitter_within_tolerance_reanchors(sequential, hw_sim, tmp_path):
    res, dev, clock, ev = _run(sequential, hw_sim, tmp_path, extra_delay={"conjugate": 12.0})
    assert res.status == "ok", res.fault
    t_conj = res.anchors["conjugate"]
    t_samp = res.anchors["sample"]
    assert t_conj - t_samp == pytest.approx((41.6 - 1.0) * 60 + 12.0)
    starts = {e["step"]: e["t"] for e in ev if e["kind"] == "step_start"}
    assert starts["conjugate_stop"] - t_conj == pytest.approx(60.0)   # timed from the actual conjugate edge
    assert res.signal["S"] == pytest.approx(5e-9, rel=0.01)


def test_missing_inject_start_goes_to_safe_state(primary, hw_sim, tmp_path):
    res, dev, clock, ev = _run(primary, hw_sim, tmp_path, omit={"sample"},
                               watchdog_overrides={"first_inject_max_wait_s": 300})
    assert res.status == "fault" and "late" in res.fault
    assert dev.valves["V2"].get_position() == "isolate"
    assert dev.valves["V3"].get_position() == "bypass"
    assert dev.valves["V4"].get_position() == "B"
    assert dev.sia.stopped and dev.potentiostat.cell_is_off and dev.magnet.is_on()
    fault_t = [e["t"] for e in ev if e["kind"] == "fault"][0]
    assert fault_t - 1000.0 == pytest.approx(120 + 300, abs=0.2)     # expected edge + max wait
    assert any(e["kind"] == "safe_state" and not e["failed"] for e in ev)


def test_late_second_inject_beyond_tolerance_faults(sequential, hw_sim, tmp_path):
    res, dev, clock, ev = _run(sequential, hw_sim, tmp_path, extra_delay={"conjugate": 45.0})
    assert res.status == "fault" and "conjugate" in res.fault
    assert dev.valves["V2"].get_position() == "isolate"


def test_unexpected_inject_faults(primary, hw_sim, tmp_path):
    res, *_ = _run(primary, hw_sim, tmp_path, extra_edges=(600.0,))    # extra edge during incubation
    assert res.status == "fault" and "unexpected" in res.fault


def test_device_fault_mid_run_safe_state_and_trace_kept(primary, hw_sim, tmp_path):
    # V3 cannot reach 'detect' at the start of accumulation (after acquisition has started)
    res, dev, clock, ev = _run(primary, hw_sim, tmp_path, fail_valve=("V3", "detect"))
    assert res.status == "fault" and "V3" in res.fault
    assert dev.valves["V3"].get_position() == "bypass" and dev.valves["V2"].get_position() == "isolate"
    assert dev.potentiostat.cell_is_off
    meta = json.loads((tmp_path / "run" / "metadata.json").read_text())
    assert meta["status"] == "fault" and "trace_sha256" in meta     # partial raw trace is still stored


def test_actions_ordering(primary):
    acts = build_actions(primary)
    assert acts[0].cycle_min == -1.0 and acts[-1].kind == "cycle_end"
    times = [a.cycle_min for a in acts]
    assert times == sorted(times)
