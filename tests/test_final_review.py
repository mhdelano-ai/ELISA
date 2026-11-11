"""Tests for the model-side changes made when resolving the final review (docs/08 s10)."""
import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

KI = "chem.enzymes.alp.phosphate_inhibition_Ki"


def test_phosphate_ki_override_marked_unverified_and_widened(ps):
    """S10: the K_i measured on E. coli AP is not assumed for calf-intestinal ALP."""
    p = ps.params[KI]
    assert p.overridden_from is not None and p.overridden_from.low == pytest.approx(1e-6)
    assert p.unverified and p.confidence == "low"
    assert p.value == pytest.approx(2e-6)
    assert p.low == pytest.approx(2e-7) and p.high == pytest.approx(1e-3)
    assert "Fernley" in p.source and "OBrien2002" in p.source


def test_lower_ki_lowers_the_upper_range(ps):
    """The low K_i bound matters for the 1000 pg/mL range (docs/08 S10)."""
    import design_lib as L
    import final_designs as F
    from dataclasses import replace
    from elisa_sim.model import evaluate
    ps0 = L.load_ps()
    _, a, pm, _ = next(e for e in F.designs(ps0) if e[0] == "P-chamb")
    p = pm(ps0).with_values(dict(a.design))
    a0 = replace(a, design=())
    hi = evaluate(a0, p.with_values({KI: 2e-6})).uloq_pgml
    lo = evaluate(a0, p.with_values({KI: 2e-7})).uloq_pgml
    assert lo < 1000 < hi


def test_mc_lod_scale_applied_before_p():
    """S13: the transfer factor scales every draw before P is computed."""
    import design_lib as L
    import final_designs as F
    ps0 = L.load_ps()
    _, a, pm, f = next(e for e in F.designs(ps0) if e[0] == "S-chamb")
    s1 = L.mc(a, pm(ps0), n=200, lod_scale=f)
    s0 = L.mc(a, pm(ps0), n=200)
    assert np.allclose(s1["lod_draws"], s0["lod_draws"] * f)
    uloq = np.asarray(s0["_mc"].result.uloq_pgml, float)
    leff = s0["lod_draws"] * f * np.maximum(1.0, 1000.0 / np.maximum(uloq, 1e-30))   # design_lib's L_eff
    assert s1["p_success"] == pytest.approx(np.mean(leff <= 1.0))
    assert s1["lod_nominal"] == pytest.approx(s0["lod_nominal"] * f)


def test_design_variants():
    """S9: thin-layer default, IDA option; S13: chamber stirring factor sampled, docs05 reproduction pinned."""
    import design_lib as L
    import final_designs as F
    ps0 = L.load_ps()
    d = {k: (a, pm, f) for k, a, pm, f in F.designs(ps0)}
    assert {a.detector for a, _, _ in d.values()} == {"thin_layer"}
    assert {a.detector for _, a, _, _ in F.designs(ps0, "review_ida")} == {"ida_flow"}
    key = "ma.capture.in_vial_unstirred_rate_factor"
    p = d["P-chamb"][1](ps0)
    assert key not in p.pinned
    assert p.params[key].low == pytest.approx(0.2 / 2.2) and p.params[key].high == pytest.approx(1 / 2.2)
    old = next(e for e in F.designs(ps0, "docs05") if e[0] == "P-chamb")
    assert key in old[2](ps0).pinned and old[1].detector == "ida_flow"
    with pytest.raises(ValueError):
        F.designs(ps0, "nonsense")


def test_bench_values_pin_coupled_factors():
    """B3: the decision table enters the label factor exactly as model_feedback does."""
    import design_lib as L
    notes = []
    ps = L.apply_bench_values(L.load_ps(), {"ma.nsb.label_factor_igg_enzyme_conjugate": {"value": 0.05}}, notes)
    for k in ("chem.nsb.nsb_effective_rate_constant", "ma.nsb.surface_factor_magnetic_beads"):
        assert ps.params[k].low == ps.params[k].high == ps.params[k].value
    assert len(notes) == 2
    l4 = L.l4_transfer(ps)
    assert l4.params["ma.nsb.label_factor_igg_enzyme_conjugate"].value == pytest.approx(0.05 * 0.1 / 0.7)
    assert L.g1_decision({"P-chamb": 0.31}) == "GO"
    assert L.g1_decision({"P-chamb": 0.29, "B-bed": 0.1}) == "GO-WITH-LEVER"
    assert L.g1_decision({"P-chamb": 0.09}) == "STOP"


def test_shared_reservoir_multiplier():
    """B4: 3.3 nM x 8 h against 0.3 nM x 36.6 min is ~145x the bead exposure."""
    import shared_reservoir_cost as S
    assert S.C_RES_NM == pytest.approx(3.3)
    assert S.bead_nsb_multiplier(0.0) == 1.0
    assert S.bead_nsb_multiplier(8.0) == pytest.approx(1 + 3.3 * 480 / 10.98, rel=1e-3)
    assert S.bead_nsb_multiplier(8.0, 0.25) < S.bead_nsb_multiplier(8.0)


def test_contamination_scenario_is_one_pg_per_ml():
    """S5: scenario bound 1 pg/mL of a 150 kDa IgG = 6.7 fM."""
    import design_lib as L
    import final_designs as F
    assert F.CONTAMINATION_1PG_M == pytest.approx(6.67e-15, rel=1e-2)
    name, fn, inj = F.scen("C1")
    p = fn(L.load_ps()).params["ma.nsb.blank_igg_contamination_equivalent"]
    assert p.high == pytest.approx(F.CONTAMINATION_1PG_M) and p.value == 0.0 and inj is None
