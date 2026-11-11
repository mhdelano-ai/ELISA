"""Agreement with published numbers (docs/01) and Task 1/2 worked estimates.

The audit (docs/04) resolved the three former strict xfails: the two ALP-LOD comparisons are lower bounds on
kcat (consistent with the model), and the plate-ELISA blank is reproduced once the IgG-conjugate NSB factor is
anchored to Rissin2010/Chang2012.  Numbers are reported in docs/03 section 8 and docs/04.
"""
import pytest

from elisa_sim import validation as V


def test_task1_worked_estimate_10nM(ps):
    v = V.task1_product_estimate(ps)
    assert v["ratio"] == pytest.approx(1.0, abs=0.1)


def test_task2_loop_transfer_table():
    for case in V.task2_loop_table():
        assert case["max_abs_diff"] < 0.01, case


def test_hq_fia_detection_limit_within_3x(ps):
    """DellaCiana1996 HQ 0.12 nM: wall-jet equation + Task 2 noise (flow/electrode size not published)."""
    v = V.dellaciana_hq_fia_lod(ps)
    assert 1 / 3 < v["ratio"] < 3


def test_dellaciana_alp_lod_within_10x(ps):
    v = V.dellaciana_alp_lod(ps)
    assert 0.1 < v["ratio"] < 10


def test_published_alp_lods_are_lower_bounds_on_kcat_consistent_with_model(ps):
    """Audit: an enzyme LOD is set by the product-detector LOD or by a larger (substrate-blank) noise, so the
    kcat implied by equating them is a LOWER BOUND.  Replaces two strict xfails that read these numbers as kcat
    estimates (180 and 23 /s).  The nominal kcat must be at least the larger lower bound."""
    kcat = ps.get("chem.enzymes.alp.kcat_conjugate_assay_conditions", "1/s")
    lb = max(V.dellaciana_alp_lod(ps)["implied_kcat_lower_bound"], V.thompson_alp_lod(ps)["implied_kcat_lower_bound"])
    assert lb <= kcat
    assert V.dellaciana_alp_lod(ps)["ratio"] < 1 and V.thompson_alp_lod(ps)["ratio"] < 1


def test_bead_capture_chang2012_within_35_percent(ps):
    v = V.chang_bead_capture(ps)
    assert 0.65 < v["ratio"] < 1.35
    assert v["model_without_transport_and_activity"] == pytest.approx(0.7, abs=0.03)


def test_simoa_blank_closure_within_2x(ps):
    v = V.simoa_blank(ps)
    assert 0.5 < v["ratio"] < 2


@pytest.mark.parametrize("label_nM", [1.0, 10.0])
def test_conventional_elisa_blank_within_3x(ps, label_nM):
    """Audit: with the IgG-conjugate NSB factor the plate blank of Rissin2010 (85 fM) is reproduced within 3x at
    both plausible label concentrations (was 9-35x too high, strict xfail)."""
    assert 1 / 3 < V.conventional_elisa_blank(ps, label_conc_M=label_nM * 1e-9)["ratio"] < 3


def test_simoa_blank_including_detection_antibody_nsb_within_3x(ps):
    """Audit: the NSB rates must reproduce the blank of the experiment they come from when the detection antibody
    (1 nM, 45 min, 13 % labelled) is counted, not only SbG.  With the pre-audit factor 1 this gives ~21x."""
    assert V.simoa_detection_antibody_consistency(ps)["ratio"] < 3
    old = ps.with_values({"ma.nsb.label_factor_igg_enzyme_conjugate": 1.0})
    assert V.simoa_detection_antibody_consistency(old)["ratio"] > 10
