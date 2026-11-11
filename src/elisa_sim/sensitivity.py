"""Sensitivity analysis of the LOD.

* one_at_a_time: each sampleable parameter set to its low and its high bound, others nominal.
  Reported as log10(LOD_bound / LOD_nominal).
* global_indices: from a Monte Carlo run, Spearman rank correlation between each parameter and log LOD,
  and a first-order (Sobol-type) index estimated as the correlation ratio Var(E[log LOD | X]) / Var(log LOD)
  using equal-count bins of X.  Both assume independent inputs (as sampled).
"""
from __future__ import annotations

import numpy as np

from .architectures import Architecture
from .model import evaluate, apply_design
from .montecarlo import MCResult, used_keys
from .params import ParameterSet


def _rank(x):
    order = np.argsort(x, kind="mergesort")
    r = np.empty(len(x), float)
    r[order] = np.arange(len(x))
    # average ties
    _, inv, counts = np.unique(x, return_inverse=True, return_counts=True)
    if np.any(counts > 1):
        sums = np.bincount(inv, weights=r)
        r = sums[inv] / counts[inv]
    return r


def spearman(x, y):
    rx, ry = _rank(np.asarray(x, float)), _rank(np.asarray(y, float))
    rx -= rx.mean()
    ry -= ry.mean()
    den = np.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / den) if den > 0 else 0.0


def correlation_ratio(x, y, bins: int = 20):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    order = np.argsort(x)
    groups = np.array_split(y[order], bins)
    means = np.array([g.mean() for g in groups if len(g)])
    sizes = np.array([len(g) for g in groups if len(g)])
    var_cond = np.sum(sizes * (means - y.mean()) ** 2) / len(y)
    v = y.var()
    return float(var_cond / v) if v > 0 else 0.0


def _finite_log(lod):
    lod = np.asarray(lod, float)
    cap = np.nanmax(lod[np.isfinite(lod)]) * 10 if np.any(np.isfinite(lod)) else 1e30
    return np.log10(np.where(np.isfinite(lod), lod, cap))


def global_indices(mc: MCResult, bins: int = 20) -> list[dict]:
    y = _finite_log(mc.result.lod_pgml)
    rows = []
    for k in mc.keys:
        x = mc.samples[k]
        if np.ptp(x) == 0:
            continue
        rows.append(dict(parameter=k, spearman=spearman(x, y), first_order=correlation_ratio(x, y, bins)))
    rows.sort(key=lambda d: -abs(d["spearman"]))
    return rows


def one_at_a_time(arch: Architecture, ps: ParameterSet) -> list[dict]:
    base = apply_design(arch, ps)
    keys = base.sampleable(used_keys(arch, ps))
    lod0 = float(evaluate(arch, ps).lod_pgml)
    rows = []
    for k in keys:
        prm = ps.params[k]
        out = {}
        for side, val in (("low", prm.low), ("high", prm.high)):
            lod = float(evaluate(arch, ps.with_values({k: val})).lod_pgml)
            out[side] = np.log10(lod / lod0) if np.isfinite(lod) and lod > 0 else np.inf
        rows.append(dict(parameter=k, low=prm.low, high=prm.high, nominal=prm.value, unit=prm.unit,
                         dlog10_lod_at_low=out["low"], dlog10_lod_at_high=out["high"],
                         swing=max(abs(out["low"]), abs(out["high"]))))
    rows.sort(key=lambda d: -d["swing"])
    return rows
