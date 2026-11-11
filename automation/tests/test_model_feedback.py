"""Bench -> model feedback runs against the repository model without editing params/."""
import hashlib
from pathlib import Path

import pytest

from elisa_auto import model_feedback as MF

ROOT = MF.repo_root()


@pytest.mark.skipif(not (ROOT / "scripts" / "design_lib.py").exists(), reason="model repository not present")
def test_feedback_moves_p_success_in_the_right_direction(tmp_path):
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT / "params").glob("*.yaml")}
    good = {"ma.nsb.label_factor_igg_enzyme_conjugate": {"value": 0.01, "low": 0.008, "high": 0.012}}
    bad = {"ma.nsb.label_factor_igg_enzyme_conjugate": {"value": 0.3, "low": 0.25, "high": 0.35}}
    rg = MF.evaluate(good, n=200, designs=("P-chamb",))
    rb = MF.evaluate(bad, n=200, designs=("P-chamb",))
    base = rg[0]["p_success"]
    assert rg[0]["case"].startswith("before") and rg[1]["case"] == "with bench values"
    assert rg[1]["p_success"] > base > rb[1]["p_success"]
    after = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT / "params").glob("*.yaml")}
    assert before == after


def test_unknown_key_rejected():
    L, _ = MF._import_model()
    with pytest.raises(KeyError):
        MF.apply_measured(L, L.load_ps(), {"ma.not.a.key": {"value": 1}})


def test_label_factor_measurement_pins_reference_rate():
    L, _ = MF._import_model()
    notes = []
    ps = MF.apply_measured(L, L.load_ps(), {"ma.nsb.label_factor_igg_enzyme_conjugate":
                                            {"value": 0.03, "low": 0.02, "high": 0.04}}, notes)
    p = ps.params["chem.nsb.nsb_effective_rate_constant"]
    assert p.low == p.high == p.value == 4e-11
    assert len(notes) == 2


def test_g1_rule_same_in_gates_and_model_and_fixed_values():
    """B3 (docs/08): one G1 rule, fixed before data; gates.yaml and design_lib agree."""
    from elisa_auto.gates import g1_rule_verdict, load_gates
    L, _ = MF._import_model()
    g = load_gates()
    assert g["G1_rule"]["p_go_min"] == L.G1_GO_MIN == 0.30
    assert g["G1_rule"]["p_lever_min"] == L.G1_LEVER_MIN == 0.10
    for p, word in ((0.35, "GO"), (0.2, "GO-WITH-LEVER"), (0.05, "STOP")):
        d = {"P-chamb": p, "S-chamb": p - 0.01, "B-bed": 0.0}
        assert L.g1_decision(d) == word
        assert g1_rule_verdict(g, d).startswith(word)
    # the unmeasured L4 lever never rescues a STOP; a measured one (G1') can
    assert L.g1_decision({"P-chamb": 0.05}) == "STOP"
    assert L.g1_decision({"P-chamb": 0.05}, {"P-chamb": 0.12}) == "GO-WITH-LEVER"


def test_feedback_applies_transfer_factor_before_p():
    """S13 (docs/08): the chamber designs' 1/0.96 is applied per draw, so P is computed on the scaled LOD."""
    L, F = MF._import_model()
    ps = L.load_ps()
    _, arch, pm, f = next(e for e in F.designs(ps) if e[0] == "P-chamb")
    a = L.mc(arch, pm(ps), n=300, lod_scale=f)
    b = L.mc(arch, pm(ps), n=300)
    import numpy as np
    assert np.allclose(a["lod_draws"], b["lod_draws"] * f)
    assert a["p_success"] <= b["p_success"]
    assert a["lod_median"] == __import__("pytest").approx(b["lod_median"] * f, rel=1e-9)


def test_measured_chamber_value_not_overwritten_by_design_modifier():
    """A bench-measured chamber stirring factor (E3.3) must survive the chamber designs' parameter modifier."""
    L, F = MF._import_model()
    ps0 = L.load_ps()
    _, arch, pm, f = next(e for e in F.designs(ps0) if e[0] == "P-chamb")
    key = "ma.capture.in_vial_unstirred_rate_factor"
    ps = MF.apply_measured(L, pm(ps0), {key: {"value": 0.3, "low": 0.28, "high": 0.32}})
    assert ps.params[key].value == 0.3 and ps.params[key].low == 0.28
