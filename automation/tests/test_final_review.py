"""Tests for the changes made when resolving the final review (docs/08 s10): B4 separate reservoirs, S2 trap flow
at the tee, S3 no undeclared second injection, S12 fault latch and recovery cycle."""
import dataclasses
import json

import pytest

from elisa_auto.analyze import analyze_folder
from elisa_auto.clock import SimClock
from elisa_auto.cycle import CycleError, effective_valves, load_cycle, trap_flow_uL_min, validate
from elisa_auto.hardware import build_sim, load_hw
from elisa_auto.latch import FaultLatch
from elisa_auto.run_sim import parse_samples, simulate
from elisa_auto.sequencer import Sequencer

from conftest import CFG


def _replace_step(c, name, **kw):
    steps = [dataclasses.replace(s, **kw) if s.name == name else s for s in c.steps]
    return dataclasses.replace(c, steps=steps)


# ---- B4: beads and conjugate from separate reservoirs ----------------------------------------------------------
def test_primary_doses_beads_and_conjugate_from_separate_ports(primary):
    doses = [s.sia for s in primary.steps if s.sia and s.sia.get("action") == "dispense"]
    assert [d["from"] for d in doses] == ["beads", "conjugate"]
    assert all(d["to"] == "cup" for d in doses)
    assert sum(d["volume_uL"] for d in doses) == pytest.approx(20)          # unchanged final volume ~220 uL
    assert not any("reservoir" == (s.sia or {}).get("from") for s in primary.steps)


@pytest.mark.parametrize("hwfile", ["hardware_sim.yaml", "hardware_lab.example.yaml"])
def test_sia_ports_exist_and_fit_the_selection_valve(primary, sequential, hwfile):
    hw = load_hw(CFG / hwfile)
    ports = hw["sia"]["ports"]
    assert ports["beads"] != ports["conjugate"]
    assert len(set(ports.values())) == len(ports) <= hw["sia"]["valve_ports"] == 8
    for c in (primary, sequential, load_cycle(CFG / "cycle_recovery.yaml")):
        validate(c, sia_ports=ports)


def test_unknown_sia_port_is_rejected(primary, hw_sim):
    bad = _replace_step(primary, "dose_beads", sia={"action": "dispense", "from": "reservoir", "to": "cup",
                                                     "volume_uL": 10})
    with pytest.raises(CycleError):
        validate(bad, sia_ports=hw_sim["sia"]["ports"])


# ---- S2: trap flow where SIA and BSM meet at the tee -----------------------------------------------------------
def test_trap_loading_flow_counts_both_pumps(primary):
    vs = effective_valves(primary, primary.safe_state["valves"])
    i = [s.name for s in primary.steps].index("load_trap")
    step = primary.steps[i]
    assert vs[i]["V4"] == "B" and step.bsm["flow_uL_min"] == 1
    assert trap_flow_uL_min(step, vs[i]) == pytest.approx(100.0)


def test_bsm_left_at_wash_flow_during_trap_loading_is_rejected(primary):
    bad = _replace_step(primary, "load_trap", bsm={"flow_uL_min": 100, "solvent": "A1"})
    with pytest.raises(CycleError, match="trap flow 199"):
        validate(bad)
    undeclared = _replace_step(primary, "load_trap", bsm=None)
    with pytest.raises(CycleError, match="BSM flow is not declared"):
        validate(undeclared)


def test_a1_and_accumulation_flows_declared(primary):
    st = {s.name: s for s in primary.steps}
    assert st["accumulation"].bsm["flow_uL_min"] == st["readout"].bsm["flow_uL_min"] == 10   # W5
    assert "no phosphate" in st["aspirate_sample"].empower


# ---- S3: no undeclared SM-FL injection ---------------------------------------------------------------------------
def test_cleaning_step_is_a_needle_wash_not_an_injection(primary, sequential):
    for c in (primary, sequential):
        clean = next(s for s in c.steps if s.name == "clean")
        assert clean.smfl == "needle_wash"
        assert "cleaning injection" not in (clean.empower or "")
        assert len([s for s in c.steps if s.smfl == "inject"]) == len(c.injects)


def test_undeclared_second_injection_is_rejected(primary):
    bad = _replace_step(primary, "clean", smfl="inject")
    with pytest.raises(CycleError, match="not a declared inject"):
        validate(bad)


# ---- S12: fault latch ----------------------------------------------------------------------------------------------
def test_runs_after_a_fault_are_invalid_until_recovery(primary, hw_sim, tmp_path):
    clock = SimClock(0.0)
    dev = build_sim(clock, hw_sim)
    latch = FaultLatch(tmp_path)
    # run 1: Inject Start withheld -> fault, latch set
    dev.empower.plan_cycle(primary, t_arm=clock.now(), omit={"sample"})
    r1 = Sequencer(primary, dev, clock, tmp_path / "r1", latch=latch,
                   watchdog_overrides={"first_inject_max_wait_s": 60}).run({"type": "blank", "conc_pgml": 0})
    assert r1.status == "fault" and latch.is_set
    assert dev.magnet.is_on()                       # safe state keeps the beads in the trap
    # run 2 without recovery: executed, but invalid
    dev.potentiostat.set_true_charge(5e-9)
    dev.empower.plan_cycle(primary, t_arm=clock.now())
    r2 = Sequencer(primary, dev, clock, tmp_path / "r2", latch=latch).run({"type": "blank", "conc_pgml": 0})
    assert r2.status == "ok" and r2.valid is False and "r1" in r2.invalid_reason
    meta = json.loads((tmp_path / "r2" / "metadata.json").read_text())
    assert meta["valid"] is False and meta["fault_latch"]["set"] is True
    # recovery cycle: magnet off, flush, rinse -> latch cleared and logged
    rec = load_cycle(CFG / "cycle_recovery.yaml")
    rr = Sequencer(rec, dev, clock, tmp_path / "rec", latch=latch).run({"type": "recovery"})
    assert rr.status == "ok" and not latch.is_set
    ev = [json.loads(l) for l in (tmp_path / "rec" / "events.jsonl").read_text().splitlines()]
    assert any(e["kind"] == "latch_cleared" for e in ev)
    assert any(e["kind"] == "magnet" and e["on"] is False for e in ev)
    flush = [e for e in ev if e["kind"] == "sia" and e["command"]["action"] == "flush_trap"]
    assert flush and flush[0]["command"]["flow_uL_min"] == 300
    # run 3: valid again
    dev.empower.plan_cycle(primary, t_arm=clock.now())
    r3 = Sequencer(primary, dev, clock, tmp_path / "r3", latch=latch).run({"type": "blank", "conc_pgml": 0})
    assert r3.status == "ok" and r3.valid


def test_simulated_sequence_without_recovery_excludes_later_runs(tmp_path):
    samples = parse_samples("blank:3,1:2,10:2")
    res = simulate(CFG / "cycle_primary.yaml", samples, tmp_path, fault_at={1}, auto_recover=False)
    assert res[1].status == "fault"
    assert all(r.valid is False for r in res[2:])
    out = "\n".join(analyze_folder(tmp_path))
    assert "EXCLUDED as invalid" in out and "SET since run" in out


def test_simulated_sequence_with_auto_recovery(tmp_path):
    samples = parse_samples("blank:3,1:2,10:2")
    res = simulate(CFG / "cycle_primary.yaml", samples, tmp_path, fault_at={1}, auto_recover=True)
    assert res[1].status == "fault"
    assert all(r.valid and r.status == "ok" for r in res[2:])
    assert (tmp_path / "run_001_recovery" / "metadata.json").exists()
    assert not FaultLatch(tmp_path).is_set


# ---- W2: design-cell label factor reported -------------------------------------------------------------------------
def test_u1_reports_design_cell_factor(tmp_path):
    import shutil
    from conftest import AUTO
    shutil.copy(AUTO / "templates" / "u1_nsb.csv", tmp_path / "u1_nsb.csv")
    out = "\n".join(analyze_folder(tmp_path))
    assert "DESIGN CELL 0.3 nM x 30 min" in out


# ---- S6: carry-over criterion 1e-4, 10 ng/mL challenge -----------------------------------------------------------
def test_carryover_criterion_and_challenge(tmp_path):
    from elisa_auto.gates import load_gates
    from elisa_auto.stats import carryover_challenge
    g = load_gates()
    assert g["G2"]["carryover"]["confirm_max"] == g["G3"]["carryover"]["confirm_max"] == 1e-4
    # hand example: slope 5.2 nC per pg/mL, B1 exceeds B2 by 5.2 nC = 1 pg/mL after 10 ng/mL -> 1e-4
    r = carryover_challenge([10.2e-9], [5.0e-9], 5.2e-9, 1e4)
    assert r["excess_pgml"] == pytest.approx(1.0) and r["carryover"] == pytest.approx(1e-4)
    # simulated sequence with true carry-over 1e-4 of the previous charge
    samples = parse_samples("blank:6,1:2,2:2,5:2,10:2,10000:1,blank:2,10000:1,blank:2")
    simulate(CFG / "cycle_primary.yaml", samples, tmp_path, carryover=1e-4, cv_blank=0.02)
    out = "\n".join(analyze_folder(tmp_path))
    line = next(l for l in out.splitlines() if "challenge" in l and l.startswith("[runs] carry-over"))
    co = float(line.split("): ")[1].split()[0])
    assert 0.5e-4 < co < 1.6e-4


# ---- S4: mode boundary --------------------------------------------------------------------------------------------
def test_mode_boundary_at_30_min():
    from elisa_auto.gates import detection_t_half_verdict, load_gates
    g = load_gates()["G1"]["detection_t_half_min"]
    assert detection_t_half_verdict(g, 90).startswith("ONE-STEP MODE (t1/2")
    assert "LOD-neutral" in detection_t_half_verdict(g, 35)
    assert detection_t_half_verdict(g, 20).startswith("SEQUENTIAL")
    assert detection_t_half_verdict(g, 5).startswith("REJECT")
