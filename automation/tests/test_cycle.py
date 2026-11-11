"""Step tables reproduce docs/05 s4.1 timing and are validated."""
import pytest

from elisa_auto.cycle import CycleError, load_cycle, validate


def test_primary_matches_docs05_step_table(primary):
    # docs/05 s4.1: time to result 56.1 min; Inject Start t0 at 1 min; incubation 3->33; accumulation 41.6->51.6;
    # readout 51.6->52.6.
    assert primary.end_min == pytest.approx(56.1)
    assert primary.first_inject_min == pytest.approx(1.0)
    st = {s.name: s for s in primary.steps}
    assert (st["incubation"].start_min, st["incubation"].end_min) == (3.0, 33.0)
    assert (st["accumulation"].start_min, st["accumulation"].end_min) == (41.6, 51.6)
    assert (st["readout"].start_min, st["readout"].end_min) == (51.6, 52.6)
    assert st["load_trap"].duration_min == pytest.approx(6.6)
    assert sum(s.duration_min for s in primary.steps) == pytest.approx(57.1)   # -1 -> 56.1
    assert primary.time_to_result_min() == pytest.approx(52.1)                  # t0 -> end of post-baseline
    assert primary.end_min <= primary.time_limit_min


def test_sequential_matches_docs05_total(sequential):
    # docs/05 s4.1 sequential mode: 3 min conjugate stop, 2 min wash, 5 min accumulation, 58.1 min to result.
    assert sequential.end_min == pytest.approx(58.1)
    st = {s.name: s for s in sequential.steps}
    assert st["conjugate_stop"].duration_min == pytest.approx(3.0)
    assert st["wash_after_conjugate"].duration_min == pytest.approx(2.0)
    assert st["accumulation"].duration_min == pytest.approx(5.0)
    assert [i.name for i in sequential.injects] == ["sample", "conjugate"]


def test_safe_state_is_docs05(primary):
    assert primary.safe_state["valves"]["V2"] == "isolate"
    assert primary.safe_state["valves"]["V3"] == "bypass"


def test_validation_rejects_gap_and_unknown_valve(primary, hw_sim, tmp_path):
    import dataclasses
    bad = dataclasses.replace(primary.steps[3], start_min=3.5)
    c = dataclasses.replace(primary, steps=primary.steps[:3] + [bad] + primary.steps[4:])
    with pytest.raises(CycleError):
        validate(c)
    pos = {k: v["positions"] for k, v in hw_sim["valves"].items()}
    validate(primary, pos)
    pos["V3"] = ["bypass"]
    with pytest.raises(CycleError):
        validate(primary, pos)


def test_overlong_cycle_rejected(tmp_path, primary):
    text = open(primary.path).read().replace("end_min: 56.1", "end_min: 60.5")
    p = tmp_path / "c.yaml"
    p.write_text(text)
    with pytest.raises(CycleError):
        load_cycle(p)
