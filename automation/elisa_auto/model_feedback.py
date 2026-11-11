"""Bench -> model feedback: `python -m elisa_auto.model_feedback bench/measured_values.yaml [--n 1000] [--rank]`.

Reads measured model inputs (YAML: key: {value, low, high, source}), narrows each parameter to the measured
value and interval ON A COPY of the parameter set (params/*.yaml are never edited), and re-evaluates the final
designs of docs/05 exactly as scripts/final_designs.py does (same designs, same chamber approximation, same
Monte Carlo work-around in scripts/design_lib.mc). Prints nominal LOD, median [5-95 %] and P(success) before and
after, for the primary (P-chamb, one-step chamber), the sequential mode (S-chamb) and the backup bed (B-bed).
--rank lists the remaining sampled parameters by their one-at-a-time effect on the primary's nominal LOD: the top
entry is the most informative next measurement (docs/06 s9.3).
Needs the model package of this repository (pip install -e . at the repository root).
"""
from __future__ import annotations

import argparse
import math
import os
import sys
from dataclasses import replace
from pathlib import Path

import yaml

DESIGNS = ("P-chamb", "S-chamb", "B-bed")


def repo_root() -> Path:
    return Path(os.environ.get("ELISA_ROOT", Path(__file__).resolve().parents[2]))


def _import_model():
    root = repo_root()
    for sub in ("src", "scripts"):
        p = str(root / sub)
        if p not in sys.path:
            sys.path.insert(0, p)
    import design_lib as L          # noqa: E402  (repository scripts/)
    import final_designs as F       # noqa: E402
    return L, F


def load_measured(path) -> dict:
    d = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    for k, v in d.items():
        if not isinstance(v, dict) or "value" not in v:
            raise ValueError(f"{k}: expected a mapping with value (and low/high/source)")
    return d


# A bench measurement of the label factor is a measurement of the absolute k_eff on the actual beads
# (docs/06 E1.3: factor = k_eff / 4e-11 m/s). The model computes k_eff = label factor x
# chem.nsb.nsb_effective_rate_constant x ma.nsb.surface_factor_magnetic_beads, and the Monte Carlo samples the
# last two as well. Left free, they would re-spread the measured value over ~50x (8e-12 to 4e-10 m/s) and the bench
# information would be lost. So when the label factor is measured, the reference rate and the bead surface factor
# are pinned at their nominal values (4e-11 m/s and 1), unless they are themselves given.
COUPLED = {"ma.nsb.label_factor_igg_enzyme_conjugate": ("chem.nsb.nsb_effective_rate_constant",
                                                        "ma.nsb.surface_factor_magnetic_beads")}


def apply_measured(L, ps, measured: dict, notes: list | None = None):
    for key, partners in COUPLED.items():
        if key in measured:
            for k2 in partners:
                if k2 not in measured and k2 in ps.params:
                    v = ps.params[k2].value
                    ps = L.with_bounds(ps, k2, value=v, low=v, high=v)
                    if notes is not None:
                        notes.append(f"{k2} pinned at {v:g} because {key} was measured on the actual beads")
    for key, v in measured.items():
        if key not in ps.params:
            raise KeyError(f"unknown model parameter {key!r} (see params/*.yaml)")
        val = float(v["value"])
        lo, hi = float(v.get("low", val)), float(v.get("high", val))
        if not (lo <= val <= hi):
            raise ValueError(f"{key}: low <= value <= high violated")
        ps = L.with_bounds(ps, key, value=val, low=lo, high=hi)
    return ps


def evaluate(measured: dict, n: int = 1000, designs=DESIGNS) -> list[dict]:
    L, F = _import_model()
    ps0 = L.load_ps()
    notes = []
    ps1 = apply_measured(L, ps0, measured, notes)
    for n_ in notes:
        print(f"note: {n_}")
    rows = []
    for dkey, arch, pmod, f in F.designs(ps0):
        if dkey not in designs:
            continue
        for label, ps in (("before (docs/05)", ps0), ("with bench values", ps1)):
            s = L.mc(arch, pmod(ps), n=n)
            rows.append({"design": dkey, "case": label, "lod_nominal": s["lod_nominal"] * f,
                         "lod_median": s["lod_median"] * f, "lod_p05": s["lod_p05"] * f,
                         "lod_p95": s["lod_p95"] * f, "p_success": s["p_success"],
                         "uloq_nominal": s["uloq_nominal"], "approx": f != 1.0})
    return rows


def rank_remaining(measured: dict, top: int = 12) -> list[tuple]:
    """One-at-a-time nominal LOD at each sampled parameter's low and high bound (primary design)."""
    L, F = _import_model()
    from elisa_sim import montecarlo
    from elisa_sim.model import evaluate as ev
    ps1 = apply_measured(L, L.load_ps(), measured)
    dkey, arch, pmod, f = next(x for x in F.designs(ps1) if x[0] == "P-chamb")
    ps_d = pmod(ps1).with_values(dict(arch.design))
    a0 = replace(arch, design=())
    keys = ps_d.sampleable(montecarlo.used_keys(a0, ps_d))
    base = ev(a0, ps_d).lod_pgml
    out = []
    for k in keys:
        p = ps_d.params[k]
        try:
            lo = ev(a0, ps_d.with_values({k: p.low})).lod_pgml
            hi = ev(a0, ps_d.with_values({k: p.high})).lod_pgml
        except Exception:
            continue
        span = abs(math.log10(max(hi, 1e-30)) - math.log10(max(lo, 1e-30)))
        out.append((k, span, lo * f, hi * f, k in measured))
    out.sort(key=lambda x: -x[1])
    return [("(nominal LOD of P-chamb)", 0.0, base * f, base * f, False)] + out[:top]


def main(argv=None):
    ap = argparse.ArgumentParser(description="re-run the docs/05 final designs with bench-measured values")
    ap.add_argument("measured_yaml")
    ap.add_argument("--n", type=int, default=1000, help="Monte Carlo draws per design (docs/05 used 2000)")
    ap.add_argument("--rank", action="store_true", help="rank remaining uncertain parameters (primary design)")
    a = ap.parse_args(argv)
    measured = load_measured(a.measured_yaml)
    print(f"bench values: {', '.join(measured) or '(none)'}")
    print("| design | case | LOD nominal | median [5-95 %] (pg/mL) | P(success) | ULOQ nominal |")
    print("|---|---|---|---|---|---|")
    for r in evaluate(measured, a.n):
        ap_ = "~" if r["approx"] else ""
        print(f"| {r['design']} | {r['case']} | {r['lod_nominal']:.2g} | {r['lod_median']:.2g} "
              f"[{r['lod_p05']:.2g}-{r['lod_p95']:.2g}] | {ap_}{r['p_success']:.2f} | {r['uloq_nominal']:.3g} |")
    print("'~' = chamber approximation (docs/05 s7). Intervals are scenario ranges, not confidence intervals.")
    if a.rank:
        print("\nRemaining one-at-a-time sensitivity of the primary (log10 span of nominal LOD, low->high bound):")
        for k, span, lo, hi, meas in rank_remaining(measured):
            print(f"  {k:60s} {span:5.2f}  {lo:.3g} -> {hi:.3g} pg/mL{'  (bench-measured)' if meas else ''}")


if __name__ == "__main__":
    main()
