#!/usr/bin/env python3
"""Compute the chart data of the tier-round deck that results/tier_round/tiers.json does not hold.

Three things, all nominal (every parameter at its best estimate), all from the calculation kit of the round:
  1. the detection limit of the tier-3 transfer design against the released fraction, with the detection reagent
     as specified and with screened reagents (levers L6 + L7), and the two one-valve figures it is compared with;
  2. the share of stream-borne product that the 3 mm electrode of the strip cell converts, against flow;
  3. where the conjugate that makes the blank sits in the bed designs (beads, frit, bore, walls), from the areas
     of the designs and the surface factors of the parameter set.

Usage (from the repository root, after `pip install -e .`):
    python docs/presentation/source_tiers/gen/chart_extra.py
writes chart_extra.json beside this file.  make_slides.py reads it.
"""
import json
import os
import pathlib
import sys
import warnings

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent


def find_repo():
    env = os.environ.get("ELISA_REPO")
    for c in ([pathlib.Path(env)] if env else []) + list(HERE.parents):
        if (c / "scripts" / "tier_round" / "tierkit.py").exists():
            return c
    raise SystemExit("scripts/tier_round/tierkit.py not found; set ELISA_REPO to the repository root")


REPO = find_repo()
sys.path[:0] = [str(REPO / "scripts" / "tier_round"), str(REPO / "scripts")]
warnings.filterwarnings("ignore")

import design_lib as L   # noqa: E402
import designs as D      # noqa: E402
import run_tiers as R    # noqa: E402
import tierkit as tk     # noqa: E402

ps = R.base_params()


def evaluate(d, mod=lambda p: p):
    p = mod(ps)
    if d.get("ps_values"):
        p = p.with_values(d["ps_values"])
    ev = tk.evaluate_planar if d["tier"] == 1 else tk.evaluate_bed
    return ev(d, p)


def nominal_lod(d, mod=lambda p: p):
    return float(np.squeeze(evaluate(d, mod).lod_pgml))


def blank_split(d):
    """Enzymes of the nominal blank by the surface they sit on (a bed design)."""
    ctx = tk.Ctx(ps)
    bed = d["bed"]
    diag = evaluate(d).diagnostics
    n_bed = float(np.squeeze(diag["N_nsb_bed"]))
    n_extra = float(np.squeeze(diag["N_nsb_extra"]))
    a_bed = float(np.squeeze(diag["bed_area_m2"]))
    per_area = n_bed / (ctx.nominal(bed["surface_factor_key"], "fold") * a_bed)
    parts = {
        "beads": n_bed,
        "frit": per_area * ctx.nominal(bed["extra_factor_key"], "fold") * bed.get("extra_area", 0.0),
        "bore": per_area * ctx.nominal(bed["bore_factor_key"], "fold") * bed.get("bore_area", 0.0),
        "walls": per_area * ctx.nominal(bed["upstream_factor_key"], "fold") * bed.get("upstream_area", 0.0),
    }
    total = sum(parts.values())
    assert abs(total - (n_bed + n_extra)) < 1e-6 * total, (parts, n_bed, n_extra)
    return {k: float(v) for k, v in parts.items()}


def main():
    out = {}
    rel = [round(0.05 + 0.025 * i, 3) for i in range(37)]          # 0.05 ... 0.95
    out["transfer_vs_release"] = [
        (r, nominal_lod(R.t3(), lambda p, r=r: L.pin(p, **{R.REL: r}))) for r in rel]
    out["transfer_vs_release_screened"] = [
        (r, nominal_lod(R.t3(), lambda p, r=r: R.chain(R.L6, R.L7)(L.pin(p, **{R.REL: r})))) for r in rel]
    out["one_valve"] = nominal_lod(R.t3v())
    out["one_valve_screened"] = nominal_lod(R.t3v(), R.chain(R.L6, R.L7))

    ctx = tk.Ctx(ps)
    d_hq = ctx.nominal("chem.substrates.HQ.diffusion_coefficient", "m^2/s")
    flows = sorted(set([1, 5, 200] + [round(float(q), 3) for q in np.logspace(0, np.log10(200), 41)]))
    out["conversion_vs_flow"] = [
        (q, float(tk.cell_conversion(D.SPE_CELL, d_hq, D.C21["area"], q * 1e-9 / 60))) for q in flows]

    out["blank_split"] = {"t2": blank_split(R.t2()), "t3": blank_split(R.t3v())}
    (HERE / "chart_extra.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps({k: (v if not isinstance(v, list) else f"{len(v)} points") for k, v in out.items()}, indent=1))


if __name__ == "__main__":
    main()
