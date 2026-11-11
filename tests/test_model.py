"""Whole-model checks against physical limits (not against the code's own previous output)."""
import numpy as np
import pytest

from elisa_sim import architectures as A
from elisa_sim import montecarlo
from elisa_sim.model import evaluate, _flow_capture, Ctx
from elisa_sim import constants as K

NA = K.AVOGADRO
REF = "B-bed-TL/alp_hqdp"


@pytest.fixture(scope="module")
def archs():
    a, skipped = A.registry()
    return a


def test_registry_covers_schemes_and_chemistries(archs):
    assert {a.scheme for a in archs} == {"A", "B", "C"}
    assert set(A.CHEMISTRY_ORDER) <= {a.chemistry for a in archs}
    assert {a.capture for a in archs} == set(A.CAPTURES)


def test_incompatible_combinations_rejected():
    bad = A.Architecture(name="x", scheme="B", capture="packed_bed", chemistry="alp_aap", detector="ida_flow")
    assert A.check(bad)
    with pytest.raises(ValueError):
        evaluate(bad, None)


def test_no_analyte_gives_exactly_the_blank(ps, archs):
    for a in archs[::7]:
        r = evaluate(a, ps, conc_pgml=np.array([0.0, 1.0]))
        assert r.net_signal[0] == 0.0
        assert np.isfinite(r.blank_mean) and r.blank_sd > 0


def test_blank_without_nsb_carryover_or_substrate_is_pure_electrochemical_noise(ps):
    zero = {"chem.nsb.nsb_effective_rate_constant": 0.0, "hw.smfl.carryover_protein_conjugate": 0.0,
            "chem.regeneration.residual_label_carryover_fraction": 0.0,
            "ma.chemistries.alp_hqdp.free_product_impurity": 0.0, "ma.chemistries.alp_hqdp.hydrolysis_rate": 0.0}
    ps0 = ps.with_values(zero)
    r = evaluate(A.get(REF), ps0)
    assert r.blank_mean == pytest.approx(0.0, abs=1e-30)
    T = 60 * ps.get("hw.timing.readout_time", "min")
    i_n = r.diagnostics["noise_rms_A"]
    var_ec = 2 * i_n ** 2 * T / (2 * ps.get("ma.noise.reference_bandwidth", "Hz"))
    d = ps.get("hw.gamry.baseline_drift", "A/s") * ps.get("ma.noise.drift_residual_fraction", "fraction")
    var_drift = (0.5 * d * T ** 2) ** 2
    assert r.blank_sd ** 2 == pytest.approx(var_ec + var_drift, rel=1e-9)


def test_calibration_monotonic_below_saturation(ps, archs):
    for a in archs:
        r = evaluate(a, ps)
        c = r.conc_pgml
        y = r.net_signal
        below = c <= 1000
        assert np.all(np.diff(y[below]) > 0), a.name


def test_signal_linear_at_low_concentration(ps):
    r = evaluate(A.get(REF), ps, conc_pgml=np.array([0.0, 0.01, 0.1, 1.0]))
    y = r.net_signal[1:]
    assert y[1] / y[0] == pytest.approx(10, rel=1e-3) and y[2] / y[1] == pytest.approx(10, rel=1e-3)


def test_lod_equals_three_sd_over_slope_in_linear_regime(ps):
    r = evaluate(A.get(REF), ps)
    assert r.lod_pgml == pytest.approx(r.lod_slope_pgml, rel=0.05)


def test_analyte_mass_balance(ps):
    r = evaluate(A.get(REF), ps, conc_pgml=np.array([0.0, 1.0]))
    d = r.diagnostics
    N_sample = 1.0 * 1e-12 / 1e-6 * ps.get("ma.delivery.sample_volume", "m^3") / ps.get(
        "chem.analyte.molar_mass", "g/mol") * NA
    assert d["enzymes_at_1pg"] <= N_sample * d["enzymes_per_label"]
    assert 0 < d["capture_fraction_low"] <= d["delivered_fraction"] * (1 - d["adsorptive_loss"]) * d["loop_transfer"] + 1e-12


def test_flow_capture_transport_and_kinetic_limits(ps):
    p = Ctx(ps)
    arch = A.get(REF)
    Q = ps.get("hw.timing.sample_load_flow", "m^3/s")
    D = ps.get("chem.analyte.diffusion_coefficient", "m^2/s")
    gamma = 1e-8
    # kinetic limit: tiny kon -> f = 1 - exp(-kon gamma A / Q)
    f, geo = _flow_capture("packed_bed", p, arch, Q, 1.0, gamma, 1e-6, D)
    assert f == pytest.approx(1 - np.exp(-1e-6 * gamma * geo["A_capture"] / Q), rel=1e-6)
    # transport limit (capillary): huge kon -> Graetz/Leveque perfect sink
    from elisa_sim import transport as tr
    f, geo = _flow_capture("capillary", p, arch, Q, 1.0, gamma, 1e12, D)
    xi = np.pi * geo["L"] * D / Q
    assert f == pytest.approx(tr.march_conversion("tube", np.inf, np.array([xi]))[0], rel=0.03)
    # site saturation lowers the captured fraction
    f_low, _ = _flow_capture("capillary", p, arch, Q, 1.0, gamma, 300.0, D)
    f_sat, geo = _flow_capture("capillary", p, arch, Q, 5 * gamma * geo["A_capture"] * NA, gamma, 300.0, D)
    assert f_sat < f_low


def test_bead_capture_equilibrium_limit(ps):
    """Very long in-vial incubation: captured fraction -> k/(k + koff) (Langmuir with sites in excess)."""
    a = A.get("B-mag-IDA/alp_hqdp")
    long = ps.with_values({"ma.timing.in_vial_incubation": 1e6})
    r = evaluate(a, long, conc_pgml=np.array([0.0, 1.0]))
    r0 = evaluate(a, ps, conc_pgml=np.array([0.0, 1.0]))
    assert r.diagnostics["capture_fraction_low"] > r0.diagnostics["capture_fraction_low"]


def test_scheme_b_baseline_cycle_time_matches_task2_timeline(ps):
    """Task 2's 38 min timeline was for a 250 uL loop (PLNO); the installed 100 uL loop loads in 3 x 100 uL at
    100 uL/min = 3 min instead of 7.5 min, so the installed cycle is 4.5 min shorter."""
    legacy = ps.with_values({"hw.smfl.loop_volume_recommended": 250})
    from dataclasses import replace
    r250 = evaluate(replace(A.get(REF), injection="PLNO_250"), legacy)
    assert r250.cycle_time_min == pytest.approx(ps.get("hw.timing.cycle_time_baseline", "min"))
    r = evaluate(A.get(REF), ps)
    assert r.cycle_time_min == pytest.approx(ps.get("hw.timing.cycle_time_baseline", "min") - 4.5)


# ---------------------------------------------------------------------------------------------------------
# audit additions (docs/04_model_audit.md): each test fails on the code/parameters before the audit
# ---------------------------------------------------------------------------------------------------------
def test_installed_configuration_is_the_baseline(ps):
    """docs/00 Installed configuration: 100 uL loop, full-loop injection of 100 uL, BSM down to 1 uL/min."""
    assert ps.get("hw.smfl.loop_volume_recommended", "uL") == 100
    assert ps.get("hw.bsm.flow_min", "uL/min") == 1
    a = A.get("B-mag1-IDA/alp_hqdp")
    assert a.injection == "FL_100"
    r = evaluate(a, ps, conc_pgml=np.array([0.0, 1.0]))
    assert r.diagnostics["delivered_fraction"] == pytest.approx(1.0)


def test_injection_mode_must_match_fitted_loop(ps):
    from dataclasses import replace
    a = replace(A.get(REF), injection="PLNO_250")
    with pytest.raises(ValueError, match="loop"):
        evaluate(a, ps)                                   # 250 uL-loop mode on the installed 100 uL loop
    evaluate(a, ps.with_values({"hw.smfl.loop_volume_recommended": 250}))


def test_flows_below_bsm_minimum_rejected(ps):
    a = A.get(REF)
    slow = ps.with_values({"ma.readout.sweep_flow": 5})
    evaluate(a, slow, conc_pgml=np.array([0.0, 1.0]))   # 5 uL/min is allowed at the installed 1 uL/min minimum
    with pytest.raises(ValueError, match="BSM minimum"):
        evaluate(a, slow.with_values({"hw.bsm.flow_min": 10}), conc_pgml=np.array([0.0, 1.0]))


def test_conjugate_plug_dilution_recomputed_for_100uL_loop(ps):
    """A 20 uL plug is smeared over about one loop volume: peak ~0.12 in a 250 uL loop, ~0.3 in 100 uL."""
    a = A.get(REF)
    r100 = evaluate(a, ps, conc_pgml=np.array([0.0, 1.0]))
    from dataclasses import replace
    r250 = evaluate(replace(a, injection="PLNO_250"), ps.with_values({"hw.smfl.loop_volume_recommended": 250}),
                    conc_pgml=np.array([0.0, 1.0]))
    assert 0.10 < r250.diagnostics["conjugate_peak_dilution"] < 0.14
    assert 0.25 < r100.diagnostics["conjugate_peak_dilution"] < 0.40


def test_one_step_bead_share_uses_in_vial_exposure(ps):
    """With (almost) no wall/tubing NSB, all NSB is on the beads, so the bead share must approach 1.  Before the
    audit the bead part was computed with the in-flow conjugate exposure (55x too small) -> share ~0.02."""
    a = A.get("B-mag1-IDA/alp_hqdp")
    r = evaluate(a, ps.with_values({"ma.nsb.surface_factor_tubing": 1e-9}), conc_pgml=np.array([0.0, 1.0]))
    assert float(r.diagnostics["bead_share_of_nsb"]) == pytest.approx(1.0, abs=1e-3)
    r0 = evaluate(a, ps, conc_pgml=np.array([0.0, 1.0]))
    assert 0.0 < float(r0.diagnostics["bead_share_of_nsb"]) < 1.0


def test_bead_share_of_nsb_not_double_scaled_by_label_factor(ps):
    """Sequential bead format: bead share must not depend on the label NSB factor (it multiplies beads and walls
    alike).  Before the audit the bead part carried the factor twice."""
    a = A.get("B-mag-IDA/alp_hqdp")
    s1 = evaluate(a, ps.with_values({"ma.nsb.label_factor_igg_enzyme_conjugate": 0.04}),
                  conc_pgml=np.array([0.0, 1.0])).diagnostics["bead_share_of_nsb"]
    s2 = evaluate(a, ps.with_values({"ma.nsb.label_factor_igg_enzyme_conjugate": 1.0}),
                  conc_pgml=np.array([0.0, 1.0])).diagnostics["bead_share_of_nsb"]
    assert float(s1) == pytest.approx(float(s2), rel=1e-9)


def test_two_step_dab_nsb_uses_igg_factor(ps):
    """Two-step labels: the NSB of the biotinylated dAb scales with the IgG NSB factor."""
    a = A.get("B-bed-TL/sa_polyhrp_tmb")
    n1 = evaluate(a, ps.with_values({"ma.nsb.label_factor_igg_enzyme_conjugate": 0.01}),
                  conc_pgml=np.array([0.0, 1.0])).diagnostics["N_nsb"]
    n2 = evaluate(a, ps.with_values({"ma.nsb.label_factor_igg_enzyme_conjugate": 0.15}),
                  conc_pgml=np.array([0.0, 1.0])).diagnostics["N_nsb"]
    assert float(n2) > float(n1)


def test_capture_koff_sampled_only_within_reagent_acceptance(ps):
    """docs/01 f rejects capture reagents with t1/2 < 1 h; Monte Carlo must not sample them in the baseline."""
    m = montecarlo.run(A.get("B-mag1-IDA/alp_hqdp"), ps, n=200, seed=1)
    assert np.max(m.samples["chem.antibodies.koff_capture"]) <= np.log(2) / 3600 * 1.001


def test_longer_accumulation_increases_signal_not_noise_floor(ps):
    a = A.get(REF)
    r1 = evaluate(a, ps)
    r2 = evaluate(a, ps.with_values({"hw.timing.accumulation_time": 15}))
    assert r2.net_signal[-1] > r1.net_signal[-1]


def test_monte_carlo_shapes_and_reproducibility(ps):
    a = A.get(REF)
    m1 = montecarlo.run(a, ps, n=64, seed=3)
    m2 = montecarlo.run(a, ps, n=64, seed=3)
    assert np.shape(m1.result.lod_pgml) == (64,)
    assert np.array_equal(m1.result.lod_pgml, m2.result.lod_pgml)
    s = m1.summary()
    assert 0.0 <= s["p_lod_le_target"] <= 1.0
    assert s["lod_p05"] <= s["lod_median"] <= s["lod_p95"]
    assert "hw.timing.accumulation_time" not in m1.keys
    assert "chem.nsb.nsb_effective_rate_constant" in m1.keys


def test_mc_sample_of_nominal_values_reproduces_nominal(ps):
    """Evaluating the vectorised model with every 'sample' equal to the nominal value gives the scalar answer."""
    a = A.get("B-mag1-IDA/alp_hqdp")
    keys = montecarlo.used_keys(a, ps)
    ps_vec = ps.copy()
    ps_vec.n = 3
    for k in ps.sampleable(keys):
        ps_vec.values[k] = np.full(3, ps.params[k].value)
    rv = evaluate(a, ps_vec)
    rs = evaluate(a, ps)
    assert np.allclose(rv.lod_pgml, rs.lod_pgml, rtol=1e-9)
    assert np.allclose(rv.blank_sd, rs.blank_sd, rtol=1e-9)


def test_monte_carlo_still_samples_when_design_values_are_pinned(ps, archs):
    """Regression: an architecture built with with_design() must not silence the Monte Carlo.

    The access log used to be lost on the copy made when design values are applied, so no parameter
    was sampled and every draw returned the nominal result.
    """
    base = next(a for a in archs if a.name == REF)
    keys = montecarlo.used_keys(base, ps)
    pin = next(k for k in keys if k.startswith("ma.") and isinstance(ps.values[k], (int, float)))
    pinned = base.with_design(**{pin: ps.values[pin]})
    keys_pinned = montecarlo.used_keys(pinned, ps)
    assert set(keys_pinned) == set(keys)
    mc = montecarlo.run(pinned, ps, n=50, seed=1)
    assert pin not in mc.keys                      # the pinned design value itself is never sampled
    assert len(mc.keys) >= len(montecarlo.run(base, ps, n=50, seed=1).keys) - 1
    assert np.ptp(np.asarray(mc.result.lod_pgml, float)) > 0
