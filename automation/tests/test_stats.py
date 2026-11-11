"""Hand-computed examples for the LOD and the Stage-1 conversions (docs/06 s7.4, E1.2, E1.3, E1.5)."""
import math

import numpy as np
import pytest

from elisa_auto import stats as S


def test_lod_hand_example():
    # Blanks (nC): mean = 110/10 = 11.0; squared deviations 1,1,0,4,4,0,1,1,0,0 = 12; var = 12/9; SD = 1.154701.
    blanks = [10, 12, 11, 9, 13, 11, 10, 12, 11, 11]
    # Standards exactly on S = 11 + 2*C (nC, C in pg/mL): slope 2 nC per pg/mL.
    conc = [1, 2, 5, 10, 100]
    sig = [13, 15, 21, 31, 211]
    r = S.lod(blanks, conc, sig)
    sd = math.sqrt(12 / 9)
    assert r["blank"]["mean"] == pytest.approx(11.0)
    assert r["blank"]["sd"] == pytest.approx(sd)
    assert r["threshold"] == pytest.approx(11 + 3 * sd)              # 14.4641
    assert r["slope"] == pytest.approx(2.0)
    assert r["lod"] == pytest.approx(3 * sd / 2)                     # 1.73205 pg/mL
    assert r["lod_free_intercept"] == pytest.approx(1.7320508, rel=1e-6)
    assert r["n_low_standards"] == 4                                 # 100 pg/mL excluded (> 10)
    # one-sided 95 % UCL of SD, n = 10: chi2_0.05(9) = 3.32511 -> factor sqrt(9/3.32511) = 1.64520
    assert r["lod_ucl95"] == pytest.approx(1.7320508 * 1.6452, rel=1e-3)


def test_blank_sd_ci_matches_plan_table():
    # docs/06 s12.1 table, n = 20: 95 % CI 0.76-1.46 x s, UCL 1.37 x s
    x = np.random.default_rng(1).normal(size=20)
    b = S.blank_stats(x)
    assert b["sd_ci95"][0] / b["sd"] == pytest.approx(0.760, abs=0.005)
    assert b["sd_ci95"][1] / b["sd"] == pytest.approx(1.461, abs=0.005)
    assert b["sd_ucl95"] / b["sd"] == pytest.approx(1.370, abs=0.005)


def test_label_factor_hand_example():
    # docs/06 E1.3: 6.4e4 enzymes on 5e6 beads (2.8 um) after 0.3 nM x 30 min.
    # A = 5e6 * pi * (2.8e-6)^2 = 1.23150e-4 m^2; exposure = 3e-7 mol/m3 * 1800 s = 5.4e-4 mol s/m3
    # k_eff = 6.4e4 / (1.23150e-4 * 5.4e-4 * 6.02214e23) = 1.59809e-12 m/s; factor = /4e-11 = 0.039952
    r = S.label_factor(6.4e4, 5e6, 0.3, 30)
    assert r["area_m2"] == pytest.approx(1.23150e-4, rel=1e-4)
    assert r["k_eff_m_s"] == pytest.approx(1.59809e-12, rel=1e-4)
    assert r["label_factor"] == pytest.approx(0.039952, rel=1e-4)


def test_model_nsb_consistency():
    # The model's N_nsb = 6407 conjugates for 5e5 beads at 0.3 nM x 30 min (P-vial diagnostics) <-> factor 0.04
    assert S.label_factor(6407, 5e5, 0.3, 30)["label_factor"] == pytest.approx(0.04, rel=0.01)


def test_power_law_linear_data():
    x = np.array([1, 3, 10, 30, 100.0])
    r = S.power_law_fit(x, 7 * x)
    assert r["beta"] == pytest.approx(1.0) and r["alpha"] == pytest.approx(7.0)


def test_standard_addition_and_free_hq():
    # S = 2 * (10 + added): free HQ 10 nM in 1 mM HQDP -> 1e-5 mol/mol (docs/05 U3 confirm limit)
    added = [0, 3, 10, 30]
    sa = S.standard_addition(added, [2 * (10 + a) for a in added])
    assert sa["x0_nM"] == pytest.approx(10.0)
    assert S.free_hq_fraction(sa["x0_nM"], 1.0) == pytest.approx(1e-5)


def test_hydrolysis_rate_recovers_synthetic():
    k_h, t_half_h, S0, hq0 = 1e-9, 2.0, 1.0, 10.0          # 1/s, h, mM, nM
    k_ox = math.log(2) / (t_half_h * 3600)
    t = np.array([0, 1, 2, 4, 8.0])
    ts = t * 3600
    hq = hq0 * np.exp(-k_ox * ts) + k_h * S0 * 1e6 * (1 - np.exp(-k_ox * ts)) / k_ox
    r = S.hydrolysis_rate(t, hq, S0, t_half_h)
    assert r["k_h_per_s"] == pytest.approx(1e-9, rel=1e-6)


def test_decay_half_life():
    t = np.array([0, 15, 30, 60, 120.0])
    r = S.decay_half_life(t, 100 * 0.5 ** (t / 60))
    assert r["t_half_min"] == pytest.approx(60.0)


def test_carryover_hand():
    r = S.carryover([1000, 1000], [12, 12], [11, 11])
    assert r["carryover"] == pytest.approx(1 / 989)
