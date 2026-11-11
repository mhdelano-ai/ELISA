"""Agreement with published numbers (docs/01) and Task 1/2 worked estimates.

Where the model disagrees with a publication the test is marked xfail(strict=True) with the measured
discrepancy, so a future change that removes the discrepancy is noticed.  Numbers are reported in
docs/03 section 8.
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
    assert 100 <= v["implied_kcat"] <= 6000          # implied kcat inside the Task 1 bounds


@pytest.mark.xfail(strict=True, reason="model (nominal kcat 1000/s) predicts a 5.5x lower ALP LOD than "
                                       "DellaCiana1996; implied kcat ~180/s")
def test_dellaciana_alp_lod_within_2x(ps):
    assert 0.5 < V.dellaciana_alp_lod(ps)["ratio"] < 2


@pytest.mark.xfail(strict=True, reason="model predicts a ~44x lower ALP LOD than Thompson1991; implied kcat "
                                       "~23/s, below the Task 1 low bound of 100/s")
def test_thompson_alp_lod_within_10x(ps):
    assert 0.1 < V.thompson_alp_lod(ps)["ratio"] < 10


def test_bead_capture_chang2012_within_35_percent(ps):
    v = V.chang_bead_capture(ps)
    assert 0.65 < v["ratio"] < 1.35
    assert v["model_without_transport_and_activity"] == pytest.approx(0.7, abs=0.03)


def test_simoa_blank_closure_within_2x(ps):
    v = V.simoa_blank(ps)
    assert 0.5 < v["ratio"] < 2


@pytest.mark.xfail(strict=True, reason="NSB rate derived from digital-ELISA beads, extrapolated linearly to "
                                       "nM conjugate in a plate, overpredicts the 85 fM conventional-ELISA blank "
                                       "by ~9x (1 nM label) to ~35x (10 nM)")
def test_conventional_elisa_blank_within_3x(ps):
    assert 1 / 3 < V.conventional_elisa_blank(ps)["ratio"] < 3
