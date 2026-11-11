"""Enzyme and binding kinetics against closed-form limits."""
import numpy as np
import pytest
from scipy.special import lambertw

from elisa_sim import kinetics as kin


def test_zero_order_limit():
    E, S0, kcat, Km, t = 1e-9, 1.0, 1000.0, 1e-3, 600.0
    Pe, Pb, S = kin.enzyme_accumulation(E, S0, kcat, Km, t)
    assert Pe == pytest.approx(kcat * E * t * S0 / (Km + S0), rel=1e-6)


def test_first_order_limit():
    E, S0, kcat, Km, t = 1e-6, 1e-6, 100.0, 1.0, 5000.0
    Pe, _, _ = kin.enzyme_accumulation(E, S0, kcat, Km, t)
    assert Pe == pytest.approx(S0 * (1 - np.exp(-kcat * E / Km * t)), rel=1e-4)


def test_integrated_michaelis_menten_lambert_w():
    E, S0, kcat, Km, t = 1e-5, 0.1, 50.0, 0.05, 200.0
    Vmax = kcat * E
    S_exact = Km * np.real(lambertw(S0 / Km * np.exp((S0 - Vmax * t) / Km)))
    Pe, _, S = kin.enzyme_accumulation(E, S0, kcat, Km, t, steps=400)
    assert S == pytest.approx(S_exact, rel=1e-6)
    assert Pe + S == pytest.approx(S0, rel=1e-12)                # mass conservation


def test_product_inhibition_and_decay_reduce_product():
    args = (1e-8, 10.0, 1000.0, 0.05, 600.0)
    P0, _, _ = kin.enzyme_accumulation(*args)
    Pi, _, _ = kin.enzyme_accumulation(*args, Ki=1e-3)
    Pd, _, _ = kin.enzyme_accumulation(*args, k_decay=1e-3)
    assert Pi < P0 and Pd < P0
    assert Pd == pytest.approx(kcat_zero_order_with_decay(1e-8 * 1000 * 10 / 10.05, 1e-3, 600.0), rel=1e-3)


def kcat_zero_order_with_decay(v, k, t):
    return v / k * (1 - np.exp(-k * t))


def test_background_hydrolysis_and_conservation():
    S0, kh, t = 1.0, 1e-6, 1000.0
    Pe, Pb, S = kin.enzyme_accumulation(0.0, S0, 1000.0, 0.05, t, k_hyd=kh, P_bg0=1e-4)
    assert Pe == 0.0
    assert Pb == pytest.approx(1e-4 + S0 * (1 - np.exp(-kh * t)), rel=1e-6)
    assert S == pytest.approx(S0 * np.exp(-kh * t), rel=1e-9)


def test_rk4_converged():
    a = kin.enzyme_accumulation(1e-5, 0.1, 50.0, 0.05, 200.0, Ki=1e-3, k_decay=1e-3, steps=200)[0]
    b = kin.enzyme_accumulation(1e-5, 0.1, 50.0, 0.05, 200.0, Ki=1e-3, k_decay=1e-3, steps=4000)[0]
    assert a == pytest.approx(b, rel=1e-6)


def test_reversible_binding_equilibrium_limit():
    kc, koff = 1e-3, 1e-4
    assert kin.reversible_binding_fraction(kc, koff, 1e7) == pytest.approx(kc / (kc + koff))
    assert kin.reversible_binding_fraction(kc, 0.0, 10.0) == pytest.approx(1 - np.exp(-kc * 10))


def test_one_step_sandwich_conservation_and_hook():
    C0, D0 = 2e-6, 1e-6                       # mol/m^3 (2 nM sites, 1 nM conjugate)
    kc, kd, koff = 300.0, 390.0, 1e-4
    A0 = np.array([1e-12, 1e-10, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4])
    ACD, AC, AD, A = kin.one_step_sandwich(A0, C0, D0, kc, koff, kd, koff, 1800.0, steps=2000)
    assert np.allclose(A + AC + AD + ACD, A0, rtol=1e-8)
    # linear at low dose
    assert ACD[1] / ACD[0] == pytest.approx(100, rel=1e-3)
    # high-dose hook: labelled-captured complex falls once analyte exceeds the conjugate/sites
    assert ACD[-1] < ACD.max()
