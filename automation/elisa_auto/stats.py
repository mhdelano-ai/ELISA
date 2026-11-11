"""Statistics exactly as the validation protocol defines them (docs/06 s7.4, s12) and the Stage-1 conversions
(docs/06 E1.2, E1.3, E1.5). Pure functions; each has a hand-computed test in automation/tests/test_stats.py."""
from __future__ import annotations

import math

import numpy as np

AVOGADRO = 6.02214076e23
NSB_REFERENCE_RATE_M_S = 4.0e-11   # chem.nsb.nsb_effective_rate_constant (docs/05 s5 U1: factor = k_eff / 4e-11)

try:
    from scipy import stats as _st
except ImportError:  # pragma: no cover
    _st = None


def _chi2_ppf(p, df):
    if _st is not None:
        return float(_st.chi2.ppf(p, df))
    # Wilson-Hilferty approximation (fallback only)
    z = math.sqrt(2) * _erfinv(2 * p - 1)
    return df * (1 - 2 / (9 * df) + z * math.sqrt(2 / (9 * df))) ** 3


def _erfinv(y):  # pragma: no cover - fallback only
    a = 0.147
    ln = math.log(1 - y * y)
    t = 2 / (math.pi * a) + ln / 2
    return math.copysign(math.sqrt(math.sqrt(t * t - ln / a) - t), y)


# ---- blanks, calibration, LOD ---------------------------------------------------------------------------
def blank_stats(values) -> dict:
    x = np.asarray(values, float)
    n = x.size
    if n < 2:
        raise ValueError("need >= 2 blanks")
    mean, sd = float(x.mean()), float(x.std(ddof=1))
    df = n - 1
    lo = sd * math.sqrt(df / _chi2_ppf(0.975, df))
    hi = sd * math.sqrt(df / _chi2_ppf(0.025, df))
    ucl = sd * math.sqrt(df / _chi2_ppf(0.05, df))
    return {"n": n, "mean": mean, "sd": sd, "cv": sd / mean if mean else float("nan"),
            "sd_ci95": (lo, hi), "sd_ucl95": ucl, "threshold_3sd": mean + 3 * sd}


def linear_fit(conc, signal, intercept=None, weights=None) -> dict:
    """S = a + b*C by (weighted) least squares; if intercept is given, a is fixed to it."""
    c = np.asarray(conc, float)
    s = np.asarray(signal, float)
    w = np.ones_like(c) if weights is None else np.asarray(weights, float)
    if intercept is None:
        W = w.sum()
        cm, sm = (w * c).sum() / W, (w * s).sum() / W
        b = float((w * (c - cm) * (s - sm)).sum() / (w * (c - cm) ** 2).sum())
        a = float(sm - b * cm)
    else:
        a = float(intercept)
        b = float((w * c * (s - a)).sum() / (w * c * c).sum())
    return {"a": a, "b": b}


def lod(blanks, conc, signal, k_sd: float = 3.0, low_range_max: float = 10.0) -> dict:
    """LOD as docs/00 defines it: mean blank + k*SD of the blanks, converted to concentration through the
    low-range linear calibration (standards with 0 < C <= low_range_max pg/mL).

    Primary value: intercept fixed at the blank mean, so LOD = k*SD/b. Also reported: free-intercept fit
    ((threshold - a)/b) and the LOD using the one-sided 95 % upper confidence bound of the SD."""
    bs = blank_stats(blanks)
    c = np.asarray(conc, float)
    s = np.asarray(signal, float)
    m = (c > 0) & (c <= low_range_max)
    if m.sum() < 2:
        raise ValueError("need >= 2 low-range standards")
    fixed = linear_fit(c[m], s[m], intercept=bs["mean"])
    free = linear_fit(c[m], s[m])
    if fixed["b"] <= 0:
        raise ValueError("non-positive calibration slope")
    thr = bs["mean"] + k_sd * bs["sd"]
    return {"blank": bs, "threshold": thr, "slope": fixed["b"],
            "lod": k_sd * bs["sd"] / fixed["b"],
            "lod_free_intercept": (thr - free["a"]) / free["b"],
            "lod_ucl95": k_sd * bs["sd_ucl95"] / fixed["b"],
            "fit_fixed": fixed, "fit_free": free, "n_low_standards": int(m.sum())}


def fourpl(c, a, b, c50, d):
    """4PL: S = d + (a - d) / (1 + (C/c50)^b); a = response at 0, d = response at infinity."""
    c = np.asarray(c, float)
    return d + (a - d) / (1.0 + (np.maximum(c, 0) / c50) ** b)


def fit_4pl(conc, signal, weights_1_over_y2: bool = True) -> dict:
    from scipy.optimize import curve_fit
    c = np.asarray(conc, float)
    s = np.asarray(signal, float)
    p0 = [float(s[c == c.min()].mean()), 1.0, float(np.median(c[c > 0])), float(s.max() * 1.2)]
    sigma = np.abs(s) if weights_1_over_y2 else None
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")      # covariance warnings: the 4PL is reported as a cross-check only
        p, _ = curve_fit(fourpl, c, s, p0=p0, sigma=sigma, maxfev=20000,
                         bounds=([-np.inf, 0.1, 1e-6, -np.inf], [np.inf, 5.0, 1e9, np.inf]))
    return dict(zip(["a", "b", "c50", "d"], map(float, p)))


def inverse_4pl(y, p) -> float:
    a, b, c50, d = p["a"], p["b"], p["c50"], p["d"]
    r = (a - d) / (y - d) - 1.0
    return float(c50 * r ** (1.0 / b)) if r > 0 else float("nan")


def carryover(high, blank_after, blank_second) -> dict:
    """docs/06 s7.6: (mean B1 - mean B2) / (mean H - mean B2)."""
    h, b1, b2 = (float(np.mean(x)) for x in (high, blank_after, blank_second))
    return {"carryover": (b1 - b2) / (h - b2), "mean_high": h, "mean_b1": b1, "mean_b2": b2}


def carryover_challenge(blank_after, blank_second, slope, challenge_pgml) -> dict:
    """Carry-over after a challenge ABOVE the calibrated range (docs/06 s7.6 revised after the final review, S6):
    the excess of B1 over B2 is converted to pg/mL through the low-range slope and divided by the NOMINAL challenge
    concentration (10 ng/mL: a 1e-4 carry-over then gives 1 pg/mL in B1, ~5 SD of the B1-B2 difference at n = 5)."""
    b1, b2 = float(np.mean(blank_after)), float(np.mean(blank_second))
    excess = (b1 - b2) / float(slope)
    return {"carryover": excess / float(challenge_pgml), "excess_pgml": excess, "mean_b1": b1, "mean_b2": b2,
            "challenge_pgml": float(challenge_pgml)}


def cv_by_level(conc, signal) -> dict:
    c = np.asarray(conc, float)
    s = np.asarray(signal, float)
    out = {}
    for lev in sorted(set(c.tolist())):
        v = s[c == lev]
        if v.size >= 2:
            out[lev] = {"n": int(v.size), "mean": float(v.mean()), "cv": float(v.std(ddof=1) / v.mean())}
    return out


# ---- Stage-1 conversions --------------------------------------------------------------------------------
def bead_area_m2(n_beads: float, diameter_um: float = 2.8) -> float:
    d = diameter_um * 1e-6
    return n_beads * math.pi * d * d


def label_factor(n_alp: float, n_beads: float, conc_nM: float, time_min: float, diameter_um: float = 2.8) -> dict:
    """docs/05 s5 U1: k_eff = N_ALP / (A_beads * integral C dt * N_A); factor = k_eff / 4e-11 m/s."""
    A = bead_area_m2(n_beads, diameter_um)
    exposure = conc_nM * 1e-9 * 1e3 * time_min * 60.0      # mol/m^3 * s
    k_eff = n_alp / (A * exposure * AVOGADRO)
    return {"k_eff_m_s": k_eff, "label_factor": k_eff / NSB_REFERENCE_RATE_M_S, "area_m2": A,
            "exposure_mol_s_m3": exposure}


def power_law_fit(x, y) -> dict:
    """log y = log alpha + beta log x; beta with 95 % CI (t distribution). Used for NSB linearity (E1.3)."""
    lx, ly = np.log(np.asarray(x, float)), np.log(np.asarray(y, float))
    n = lx.size
    beta, la = np.polyfit(lx, ly, 1)
    res = ly - (la + beta * lx)
    s = math.sqrt(float((res ** 2).sum()) / (n - 2)) if n > 2 else float("nan")
    se = s / math.sqrt(float(((lx - lx.mean()) ** 2).sum())) if n > 2 else float("nan")
    t = float(_st.t.ppf(0.975, n - 2)) if (_st is not None and n > 2) else 2.0
    return {"beta": float(beta), "alpha": float(math.exp(la)), "beta_ci95": (beta - t * se, beta + t * se), "n": n}


def standard_addition(added_nM, signal) -> dict:
    """Free analyte by standard addition: S = k*(x0 + added) -> x0 = intercept/slope (E1.2)."""
    f = linear_fit(added_nM, signal)
    return {"x0_nM": f["a"] / f["b"], "slope": f["b"], "intercept": f["a"]}


def free_hq_fraction(x0_nM: float, hqdp_mM: float) -> float:
    return x0_nM * 1e-9 / (hqdp_mM * 1e-3)


def hydrolysis_rate(t_h, hq_nM, hqdp_mM: float, hq_t_half_h: float) -> dict:
    """E1.2: d[HQ]/dt = k_h [HQDP] - k_ox [HQ]  ->  HQ(t) - HQ0 e^{-k_ox t} = k_h [HQDP] (1 - e^{-k_ox t}) / k_ox.
    Linear least squares through the origin for k_h (HQDP consumption negligible). Units: t in h, k_h in 1/s."""
    t = np.asarray(t_h, float) * 3600.0
    y = np.asarray(hq_nM, float)
    k_ox = math.log(2) / (hq_t_half_h * 3600.0)
    hq0 = y[np.argmin(t)]
    lhs = y - hq0 * np.exp(-k_ox * t)
    x = (hqdp_mM * 1e6) * (1 - np.exp(-k_ox * t)) / k_ox      # nM * s
    k_h = float((x * lhs).sum() / (x * x).sum())
    return {"k_h_per_s": k_h, "k_ox_per_s": k_ox, "hq0_nM": float(hq0)}


def decay_half_life(t_min, n_remaining) -> dict:
    """E1.5: N(t) = N0 exp(-k t) by log-linear least squares; t_half in min."""
    t = np.asarray(t_min, float)
    ly = np.log(np.asarray(n_remaining, float))
    k, la = np.polyfit(t, ly, 1)
    k = -float(k)
    return {"k_per_min": k, "k_per_s": k / 60.0, "t_half_min": math.log(2) / k if k > 0 else float("inf"),
            "n0": float(math.exp(la))}
