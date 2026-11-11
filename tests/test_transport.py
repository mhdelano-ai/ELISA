"""Transport sub-models against analytic limits (Leveque/Levich, Graetz, kinetic limit, convective loop
limit) and conservation."""
import numpy as np
import pytest

from elisa_sim import constants as K
from elisa_sim import transport as tr


def test_slit_perfect_sink_matches_leveque_levich_at_small_length():
    zeta = np.array([1e-6, 1e-5, 1e-4])
    num = tr.march_conversion("slit", np.inf, zeta)
    lev = tr.leveque_slit_conversion(zeta)
    assert np.allclose(num, lev, rtol=0.02)


def test_levich_channel_current_equals_conversion_in_leveque_regime():
    D, L, w, H, Q = 1e-9, 1e-3, 2e-3, 100e-6, 1e-7     # high flow -> small zeta
    i_per_c = tr.levich_channel_current_per_conc(1, D, L, w, H, w, Q)
    eta = i_per_c / (K.FARADAY * Q)
    assert eta < 0.05
    assert tr.thin_layer_conversion(D, L, w, H, w, Q) == pytest.approx(eta, rel=0.03)


def test_thin_layer_cell_becomes_coulometric_at_low_flow():
    D, L, w, H = 1e-9, 3e-3, 3e-3, 13e-6
    assert tr.thin_layer_conversion(D, L, w, H, w, 1e-12) > 0.999


def test_tube_perfect_sink_matches_graetz_series():
    x_star = np.array([0.005, 0.01, 0.05, 0.1, 0.3])
    num = tr.march_conversion("tube", np.inf, 4 * x_star)
    ana = 1 - tr.graetz_tube_remaining(x_star)
    assert np.allclose(num, ana, rtol=0.01, atol=2e-4)


def test_tube_leveque_entrance_regime():
    # Leveque for a tube: Sh_m = 1.615 x*^(-1/3) -> conversion = 4 Sh_m x* = 6.46 x*^(2/3)
    x_star = np.array([1e-6, 1e-5])
    num = tr.march_conversion("tube", np.inf, 4 * x_star)
    assert np.allclose(num, 4 * 1.615 * x_star ** (2 / 3), rtol=0.03)


@pytest.mark.parametrize("geom,a", [("tube", 2.0), ("slit", 1.0)])
def test_kinetic_limit_small_damkohler(geom, a):
    Da = 1e-3
    xi = np.array([0.01, 1.0, 10.0])
    num = tr.march_conversion(geom, Da, xi)
    assert np.allclose(num, 1 - np.exp(-a * Da * xi), rtol=0.01)


def test_reactive_wall_between_limits():
    xi = np.array([0.01, 0.1, 1.0])
    for geom, a in (("tube", 2.0), ("slit", 1.0)):
        sink = tr.march_conversion(geom, np.inf, xi)
        for Da in (0.1, 1.0, 10.0):
            f = tr.march_conversion(geom, Da, xi)
            assert np.all(f <= sink + 1e-6)
            assert np.all(f <= 1 - np.exp(-a * Da * xi) + 1e-6)


def test_interpolated_table_matches_direct_solution():
    xi = np.array([3e-4, 3e-2, 0.7])
    for Da in (0.03, 3.0, np.inf):
        direct = tr.march_conversion("tube", Da, xi)
        interp = tr.conversion("tube", xi, Da)
        assert np.allclose(interp, direct, rtol=0.03, atol=1e-6)


def test_loop_transfer_convective_limit_and_conservation():
    n = np.array([1.0, 1.5, 2.0, 3.0])
    frac, peak, mass = tr.loop_transfer(1e-5, 1.0, False, n, return_mass=True)
    assert np.allclose(frac, tr.convective_loop_recovery(n), atol=0.01)
    assert mass["exited"] + mass["remaining"] == pytest.approx(mass["initial"], rel=1e-6)
    assert peak == pytest.approx(1.0, abs=0.01)


def test_loop_transfer_diffusion_helps_and_converges():
    n = np.array([1.0, 2.0, 3.0, 6.0])
    slow, _ = tr.loop_transfer(1e-4, 0.3, False, n)
    fast, _ = tr.loop_transfer(0.5, 0.3, False, n)
    assert np.all(np.diff(fast) >= -1e-9) and fast[-1] > 0.999
    assert fast[1] > slow[1]


def test_wall_jet_scaling():
    D, nu, a, R = 9e-10, 8.9e-7, 3e-4, 1e-3
    e1 = tr.wall_jet_conversion(D, nu, a, R, 1e-9, 0.898)
    e2 = tr.wall_jet_conversion(D, nu, a, R, 16e-9, 0.898)
    assert e2 / e1 == pytest.approx(16 ** -0.25, rel=1e-9)        # current ~ Q^(3/4)


def test_aoki_ida_proportionality():
    base = tr.aoki_ida_current_per_conc(2, 1e-9, 50, 1e-3, 5e-6, 5e-6, 0.637, 2.55, 0.19)
    assert tr.aoki_ida_current_per_conc(2, 1e-9, 100, 1e-3, 5e-6, 5e-6, 0.637, 2.55, 0.19) == pytest.approx(2 * base)
    assert base > 0


def test_wilson_geankoplis_scaling():
    k1, _ = tr.wilson_geankoplis_k(4e-11, 20e-6, 0.4, 1e-3, 8.9e-7, 1.09)
    k2, _ = tr.wilson_geankoplis_k(4e-11, 20e-6, 0.4, 8e-3, 8.9e-7, 1.09)
    assert k2 / k1 == pytest.approx(2.0, rel=1e-9)


def test_tanks_in_series_limits():
    assert tr.tanks_in_series_eluted(1.0, 1) == pytest.approx(1 - np.exp(-1))
    assert tr.tanks_in_series_eluted(1.2, 500) > 0.99            # plug flow
    assert tr.tanks_in_series_eluted(0.8, 500) < 0.01
