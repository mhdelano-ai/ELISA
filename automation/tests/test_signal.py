import numpy as np
import pytest

from elisa_auto.signal_proc import baseline_corrected_charge


def test_charge_with_sloped_baseline_hand_example():
    # Baseline i = 1e-10 + 1e-13 * t (A); a 1 nC rectangle of 1e-11 A between t = 100 and 200 s.
    t = np.arange(0, 300.0001, 0.1)
    i = 1e-10 + 1e-13 * t + np.where((t >= 100) & (t <= 200), 1e-11, 0.0)
    r = baseline_corrected_charge(t, i, readout=(100, 200), pre=(50, 99.9), post=(200.1, 250))
    assert r["charge_C"] == pytest.approx(1e-9, rel=1e-3)
    assert r["baseline_slope_A_per_s"] == pytest.approx(1e-13, rel=1e-6)


def test_pre_only_baseline_is_constant():
    t = np.arange(0, 200.0001, 0.5)
    i = np.full_like(t, 2e-11)
    r = baseline_corrected_charge(t, i, readout=(100, 150), pre=(50, 99))
    assert r["charge_C"] == pytest.approx(0.0, abs=1e-20)
