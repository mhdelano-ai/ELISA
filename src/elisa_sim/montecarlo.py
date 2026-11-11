"""Monte Carlo propagation of parameter uncertainty.

Sampling: every parameter the architecture's model actually reads (recorded by ParameterSet.get during a
nominal evaluation) is sampled independently from its low/value/high bounds with the distribution stated
in params.py (log-triangular for ranges >= 3x, else triangular), except design variables
(monte_carlo.fixed_patterns in model_assumptions.yaml) and values pinned by the architecture.
Independence is an assumption (e.g. kon and koff are sampled independently; KD is not used).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .architectures import Architecture
from .model import Result, apply_design, evaluate
from .params import ParameterSet


@dataclass
class MCResult:
    arch: Architecture
    nominal: Result
    result: Result                 # vectorised result (arrays of length n)
    samples: dict                  # key -> sampled values (YAML units)
    keys: list

    def summary(self, target_pgml: float = 1.0, time_limit_min: float = 60.0, range_top: float = 1000.0) -> dict:
        r = self.result
        lod = np.asarray(r.lod_pgml, float)
        uloq = np.asarray(r.uloq_pgml, float)
        q = lambda x, a: float(np.nanpercentile(np.where(np.isfinite(x), x, 1e30), a))
        lim = r.limiting_term
        names, counts = np.unique(lim, return_counts=True)
        frac = r.variance_fractions()
        meets_lod = lod <= target_pgml
        meets_range = meets_lod & (uloq >= range_top)
        out = dict(
            name=self.arch.name,
            lod_nominal=float(self.nominal.lod_pgml),
            lod_median=q(lod, 50), lod_p05=q(lod, 5), lod_p95=q(lod, 95),
            p_lod_le_target=float(np.mean(meets_lod)),
            p_lod_and_range=float(np.mean(meets_range)),
            uloq_median=q(uloq, 50),
            blank_equiv_median=q(np.asarray(r.diagnostics["blank_equivalent_pgml"], float), 50),
            cycle_time_min=float(self.nominal.cycle_time_min),
            time_to_result_min=float(self.nominal.time_to_result_min),
            meets_time=bool(self.nominal.time_to_result_min <= time_limit_min),
            limiting_term_nominal=str(self.nominal.limiting_term),
            limiting_term_mc_mode=str(names[np.argmax(counts)]),
            limiting_term_mc_share=float(np.max(counts) / len(lim)),
        )
        for k, v in frac.items():
            out[f"varfrac_median_{k}"] = float(np.median(v))
        return out


def used_keys(arch: Architecture, ps: ParameterSet) -> list[str]:
    probe = ps.copy()
    probe.accessed = set()
    evaluate(arch, probe)
    return sorted(probe.accessed)


def run(arch: Architecture, ps: ParameterSet, n: int | None = None, seed: int | None = None) -> MCResult:
    mc_cfg = ps.extra.get("monte_carlo", {})
    n = int(n or mc_cfg.get("default_samples", 1000))
    seed = int(seed if seed is not None else mc_cfg.get("seed", 0))
    rng = np.random.default_rng(seed)
    nominal = evaluate(arch, ps)
    keys = used_keys(arch, ps)
    base = apply_design(arch, ps)               # pins architecture design values
    sampled = base.sample(n, rng, keys)
    keys_s = base.sampleable(keys)
    res = evaluate(arch, sampled)
    samples = {k: np.asarray(sampled.values[k]) for k in keys_s}
    return MCResult(arch=arch, nominal=nominal, result=res, samples=samples, keys=keys_s)
