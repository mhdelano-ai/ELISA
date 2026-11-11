"""Per-run signal: baseline-corrected charge in the readout window (docs/05 s4.1: "Chronoamperometry during the
1 min sweep. Charge is integrated with baseline windows before and after"; docs/06 s9.2).

Q = integral over the readout window of (i(t) - b(t)) dt, where b(t) is a straight line fitted by least squares to
all samples in the pre- and post-baseline windows (pre only -> a constant equal to the pre-window mean, because a
slope fitted to 30 s alone is too noisy to extrapolate). Units: A, s -> C.
"""
from __future__ import annotations

import numpy as np

from .numutil import trapz


def baseline_corrected_charge(t, i, readout, pre, post=None) -> dict:
    t = np.asarray(t, float)
    i = np.asarray(i, float)
    m_pre = (t >= pre[0]) & (t <= pre[1])
    if m_pre.sum() < 2:
        raise ValueError("pre-baseline window has fewer than 2 samples")
    if post is not None:
        m_post = (t >= post[0]) & (t <= post[1])
        if m_post.sum() < 2:
            raise ValueError("post-baseline window has fewer than 2 samples")
        m = m_pre | m_post
        slope, intercept = np.polyfit(t[m], i[m], 1)
        resid = i[m] - (slope * t[m] + intercept)
    else:
        slope, intercept = 0.0, float(i[m_pre].mean())
        resid = i[m_pre] - intercept
    m_ro = (t >= readout[0]) & (t <= readout[1])
    if m_ro.sum() < 2:
        raise ValueError("readout window has fewer than 2 samples")
    base = slope * t[m_ro] + intercept
    q = float(trapz(i[m_ro] - base, t[m_ro]))
    width = float(t[m_ro][-1] - t[m_ro][0])
    return {"charge_C": q, "baseline_slope_A_per_s": float(slope),
            "baseline_at_readout_start_A": float(slope * t[m_ro][0] + intercept),
            "baseline_rms_A": float(np.sqrt(np.mean(resid ** 2))),
            "readout_width_s": width, "n_readout": int(m_ro.sum())}


def run_signal(trace: dict, windows_clock: dict) -> dict:
    """trace: {'t','ch1','ch2'}; windows_clock: {'readout': (a,b), 'pre_baseline': (a,b), 'post_baseline'?}.
    Returns generator (ch1) and, if present, collector (ch2) charges. The run signal S is the generator charge."""
    pre = windows_clock["pre_baseline"]
    post = windows_clock.get("post_baseline")
    ro = windows_clock["readout"]
    out = {"generator": baseline_corrected_charge(trace["t"], trace["ch1"], ro, pre, post)}
    if trace.get("ch2") is not None:
        out["collector"] = baseline_corrected_charge(trace["t"], trace["ch2"], ro, pre, post)
    out["S"] = out["generator"]["charge_C"]
    return out
