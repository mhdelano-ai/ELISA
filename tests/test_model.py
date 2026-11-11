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
    r = evaluate(A.get(REF), ps)
    assert r.cycle_time_min == pytest.approx(ps.get("hw.timing.cycle_time_baseline", "min"))


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
