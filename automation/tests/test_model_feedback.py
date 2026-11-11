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
