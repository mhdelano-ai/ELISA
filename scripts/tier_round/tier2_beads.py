#!/usr/bin/env python3
"""Alternative capture beads for the tier-2 cell with the bed inside (docs/35): which bead gives the lowest LOD.

  python scripts/tier_round/tier2_beads.py [--n 2000] [--quick]
writes results/tier_round/tier2_beads.md and tier2_beads.json (not with --quick).

Each candidate is the docs/34 cell (`tier2_cell.cell_design`) with three bead properties changed:
  * diameter (bed volume for a given bead area, retainer: membrane below 7 um, screen alone above);
  * the non-specific binding of the conjugate per unit bead area, as a factor relative to M-280 Streptavidin
    (`rel`, UNVERIFIED judgement, docs/35 section 3).  It multiplies `ma.nsb.surface_factor_packed_bed`
    (3, 1-30), which stays the packing factor of the M-280 bed of docs/34; the candidate's own range is
    combined with that range in quadrature on a log scale (each side separately);
  * the active capture sites per unit area: biotinylated F(ab')2 on streptavidin (the kit's
    `tr.capture.site_factor_streptavidin_biotin`, 1 [0.4-1]) or covalent coupling of the F(ab')2 (0.4 [0.15-0.8],
    UNVERIFIED) or a sub-monolayer streptavidin coat (0.4 [0.1-0.8], UNVERIFIED).
Then the bead amount is optimised (nominal LOD) within two limits from docs/34: the retainer washer must still hold
the stack at 80 uL/min with a margin of 2 (the check of tier2_cell.py), and the bed must fit the 2.5 mm bore.

tierkit.py, designs.py, tier2_cell.py, src/ and params/ are not edited.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_tiers as R  # noqa: E402
import tier2_cell as T  # noqa: E402
import tierkit as tk  # noqa: E402

OUT = T.OUT
PB = "ma.nsb.surface_factor_packed_bed"
SITE = "tr.capture.site_factor_streptavidin_biotin"
A_REF_MM2 = 24.4          # bead area of 1e6 M-280 in the 19 nL bed (tier2_cell, Derived)
V_REF_UL = 0.019          # bed volume of 1e6 M-280 (docs/30)
EPS = 0.4                 # bed porosity of the kit

# site-density cases (value, low, high), relative to the oriented monolayer of chem.surfaces
SITES = {
    "sa": None,                                       # the kit's own parameter, unchanged
    "covalent": (0.4, 0.15, 0.8),                     # UNVERIFIED: random-orientation covalent F(ab')2
    "sub_sa": (0.4, 0.1, 0.8),                        # UNVERIFIED: streptavidin coat ~10x below a monolayer
}

# candidates: rel = NSB per area relative to M-280 Streptavidin (value, low, high), all UNVERIFIED judgement;
# f_R = the same relative to the Rissin 2010 surface, as proposed in the evidence review (docs/35 section 3)
CANDIDATES = [
    dict(key="m280", label="Dynabeads M-280 Streptavidin (11205D), BSA in the stock; current choice",
         d_um=2.8, f_R=(1.5, 1.0, 5.0), sites="sa", magnetic=True, status="current"),
    dict(key="m270sa", label="Dynabeads M-270 Streptavidin (65305), hydrophilic COOH surface, no BSA",
         d_um=2.8, f_R=(1.0, 0.5, 3.0), sites="sa", magnetic=True, status="catalogue, drop-in"),
    dict(key="lodesa", label="Agilent LodeStars 2.7 µm Streptavidin (PL6727-1001)",
         d_um=2.7, f_R=(1.0, 0.5, 3.0), sites="sa", magnetic=True, status="catalogue, drop-in"),
    dict(key="lodecooh", label="Agilent LodeStars 2.7 µm Carboxyl (PL6727-0001), F(ab')₂ by EDC/NHS, "
         "SuperBlock-type block (the Rissin 2010 surface)", d_um=2.7, f_R=(1.0, 0.5, 3.0), sites="covalent",
         magnetic=True, status="catalogue, covalent coupling"),
    dict(key="m270ep", label="Dynabeads M-270 Epoxy (14301), F(ab')₂ coupled covalently",
         d_um=2.8, f_R=(1.0, 0.5, 3.0), sites="covalent", magnetic=True, status="catalogue, covalent coupling"),
    dict(key="peg10", label="micromod micromer-M PEG-COOH 10 µm (08-56-104), F(ab')₂ coupled covalently",
         d_um=10.0, f_R=(0.6, 0.2, 2.0), sites="covalent", magnetic=True, status="catalogue (2010 data sheet)"),
    dict(key="brush", label="carboxybetaine or POEGMA brush grafted on M-270 Amine in house, F(ab')₂ coupled to "
         "the brush", d_um=2.8, f_R=(0.3, 0.05, 1.0), sites="covalent", magnetic=True,
         status="development project"),
    dict(key="mm_sa10", label="micromod micromer-M Streptavidin 10 µm (08-19-104), sub-monolayer streptavidin",
         d_um=10.0, f_R=(2.0, 1.0, 10.0), sites="sub_sa", magnetic=True, status="catalogue"),
    dict(key="svp", label="Spherotech SVP-100-4 streptavidin polystyrene 10–14 µm (docs/34 fallback)",
         d_um=12.0, f_R=(2.0, 1.0, 10.0), sites="sa", magnetic=False, status="catalogue, fallback of docs/34"),
    dict(key="silica5", label="streptavidin silica 5 µm, non-porous (Bangs CS01002 type)",
         d_um=5.0, f_R=(2.0, 1.0, 10.0), sites="sa", magnetic=False, status="catalogue (not checked)"),
    dict(key="c1", label="Dynabeads MyOne Streptavidin C1 (65001), 1 µm; needs a 0.2–0.45 µm membrane",
         d_um=1.0, f_R=(1.0, 0.5, 3.0), sites="sa", magnetic=True, status="catalogue; retainer not designed"),
]
REF_F_R = CANDIDATES[0]["f_R"][0]
MULTS = (0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0)   # bead area relative to 24.4 mm2


def beads_dict(c, mult):
    d = c["d_um"] * 1e-6
    V = V_REF_UL * mult * c["d_um"] / 2.8                   # same porosity: V ~ A d
    return dict(key=c["key"], label=c["label"], d_p=d, V_bed_uL=V)


def n_beads(c, mult):
    return A_REF_MM2 * mult * 1e-6 / (math.pi * (c["d_um"] * 1e-6) ** 2)


def combine(base, rel):
    """Product of two uncertain factors, each (value, low, high); log half-widths added in quadrature."""
    v = base[0] * rel[0]
    lo = v * math.exp(-math.hypot(math.log(base[0] / base[1]), math.log(rel[0] / rel[1])))
    hi = v * math.exp(math.hypot(math.log(base[2] / base[0]), math.log(rel[2] / rel[0])))
    return v, lo, hi


def pset(ps, c, zero_nsb=False):
    b = ps.params[PB]
    base = (float(b.value), float(b.low), float(b.high))
    rel = tuple(x / REF_F_R for x in c["f_R"])
    rel = (rel[0], rel[1], rel[2]) if c["key"] != "m280" else (1.0, 1.0, 1.0)
    f = combine(base, rel)
    if zero_nsb:
        f = (1e-9, 1e-9, 1e-9)
    out = R.L.with_bounds(ps, PB, value=f[0], low=f[1], high=f[2])
    s = SITES[c["sites"]]
    if s is not None:
        out = R.L.with_bounds(out, SITE, value=s[0], low=s[1], high=s[2])
    return out, f


def limits(c, mult, mech):
    """Washer-lift check of docs/34 at 80 uL/min and bed length in the 2.5 mm bore."""
    b = beads_dict(c, mult)
    membrane = b["d_p"] < 7e-6
    hyd = T.hydraulics(BASE_PS, b, T.P.BED_D, membrane)[80.0]
    push = (hyd["bed"] + hyd["membrane"] + hyd["screen"]) * mech["pocket_area_mm2"] * 1e-6
    L_bed = b["V_bed_uL"] / (math.pi * T.P.BED_D ** 2 / 4.0)
    ok = push < 0.5 * mech["washer_force_N"][0] and L_bed < T.P.INLET_FLOOR - 0.1
    return ok, dict(push_N=push, limit_N=0.5 * mech["washer_force_N"][0], L_bed_mm=L_bed,
                    dp_bed_80_bar=hyd["bed"] / 1e5)


def nominal(design, ps):
    r = tk.evaluate_bed(design, ps)
    return float(np.asarray(r.lod_pgml).reshape(-1)[0])


BASE_PS = None


def main(argv=None):
    global BASE_PS
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--quick", action="store_true", help="n = 200, nothing written")
    a = ap.parse_args(argv)
    n = 200 if a.quick else a.n
    warnings.filterwarnings("ignore")
    ps = R.base_params()
    BASE_PS = ps
    mech = T.mechanics()

    res = {}
    for c in CANDIDATES:
        p, f = pset(ps, c)
        scan = []
        for m in MULTS:
            ok, lim = limits(c, m, mech)
            scan.append(dict(mult=m, n_beads=n_beads(c, m), ok=ok, lod=nominal(T.cell_design(beads_dict(c, m)), p),
                             **lim))
        allowed = [s for s in scan if s["ok"]]
        best = min(allowed, key=lambda s: s["lod"]) if allowed else None
        r1 = T.run(T.cell_design(beads_dict(c, 1.0)), p, n)
        rb = T.run(T.cell_design(beads_dict(c, best["mult"])), p, n) if best else None
        res[c["key"]] = dict(candidate={k: v for k, v in c.items()}, bed_factor=f, scan=scan,
                             best_mult=best["mult"] if best else None, at_ref=r1, at_best=rb)
        print(f"{c['key']:9s} factor {f[0]:.2g} [{f[1]:.2g}-{f[2]:.2g}]  same area {r1['lod_nominal']:.3g} "
              f"(median {r1['lod_median']:.3g})  best x{best['mult'] if best else '-'} "
              f"{rb['lod_nominal'] if rb else float('nan'):.3g} (median {rb['lod_median'] if rb else float('nan'):.3g})",
              flush=True)

    # the ceiling of the bead lever: no NSB on the beads at all (M-280 geometry and sites)
    p0, _ = pset(ps, CANDIDATES[0], zero_nsb=True)
    ceil = []
    for m in MULTS:
        ok, lim = limits(CANDIDATES[0], m, mech)
        ceil.append(dict(mult=m, ok=ok, lod=nominal(T.cell_design(beads_dict(CANDIDATES[0], m)), p0)))
    cbest = min((s for s in ceil if s["ok"]), key=lambda s: s["lod"])
    ceil_mc = T.run(T.cell_design(beads_dict(CANDIDATES[0], cbest["mult"])), p0, n)

    # where the blank enzymes of the M-280 cell sit (nominal), to show the share the beads can remove
    d = T.cell_design()
    b = d["bed"]
    share = {}
    for name, key, area in (("beads", b["surface_factor_key"], tk.np.nan),
                            ("retainer and washer hole", b["extra_factor_key"], b["extra_area"]),
                            ("exit bore", b["bore_factor_key"], b["bore_area"]),
                            ("bore above the bed and line", b["upstream_factor_key"], b["upstream_area"])):
        fac = float(ps.params[key].value)
        a_mm2 = A_REF_MM2 if name == "beads" else area * 1e6
        share[name] = dict(area_mm2=a_mm2, factor=fac, area_x_factor=a_mm2 * fac, key=key)
    tot = sum(v["area_x_factor"] for v in share.values())
    for v in share.values():
        v["share"] = v["area_x_factor"] / tot

    # ---- report -----------------------------------------------------------------------------------------------
    fmt = T.fmt
    med = lambda k: f"{fmt(k['lod_median'])} [{fmt(k['lod_p05'])}–{fmt(k['lod_p95'])}]"
    L = ["# Alternative capture beads for the tier-2 cell — numbers behind docs/35", "",
         f"Generated by `scripts/tier_round/tier2_beads.py` (Monte Carlo n = {n}, seed of the kit). The cell is the "
         "docs/34 cell; only the beads change. Model predictions, not measurements; every bead factor is a "
         "judgement (UNVERIFIED, docs/35 §3).", "",
         "## 1. Where the non-specific enzyme of the M-280 cell sits (nominal, area × surface factor)", "",
         "| Surface | Area (mm²) | Factor (key) | Share |", "|---|---|---|---|"]
    for k, v in share.items():
        L.append(f"| {k} | {v['area_mm2']:.3g} | {v['factor']:g} (`{v['key']}`) | {100 * v['share']:.0f} % |")
    L += ["", "## 2. Candidates (LOD in pg/mL)", "",
          "Bed factor = `ma.nsb.surface_factor_packed_bed` (3, 1–30) × the bead's NSB relative to M-280; ranges "
          "combined on a log scale. 'Same area' = 24.4 mm² of beads (1×10⁶ M-280). 'Best amount' = the bead area "
          "with the lowest nominal LOD among 0.5–8 × that, within the washer-lift check at 80 µL/min and the "
          "2.5 mm bore.", "",
          "| Bead | Bed factor (low–high) | Sites | Same area: nominal; median [5–95 %]; P(≤ 1) | Best amount: × area "
          "(beads) | Best amount: nominal; median [5–95 %]; P(≤ 1) | Bed Δp at 80 µL/min (bar) |",
          "|---|---|---|---|---|---|---|"]
    for c in CANDIDATES:
        r = res[c["key"]]
        f = r["bed_factor"]
        a1, ab = r["at_ref"], r["at_best"]
        bs = next(s for s in r["scan"] if s["mult"] == r["best_mult"]) if ab else None
        L.append(f"| {c['label']} | {f[0]:.2g} ({f[1]:.2g}–{f[2]:.2g}) | {c['sites']} | "
                 f"{fmt(a1['lod_nominal'])}; {med(a1)}; {a1['p_lod_le_target']:.2f} | "
                 + (f"{r['best_mult']:g} ({bs['n_beads']:.2g}) | {fmt(ab['lod_nominal'])}; {med(ab)}; "
                    f"{ab['p_lod_le_target']:.2f} | {bs['dp_bed_80_bar']:.2g} |" if ab else "— | — | — |"))
    L += ["", f"Ceiling of the bead lever (M-280 geometry and sites, no NSB on the beads at all): best amount × "
          f"{cbest['mult']:g}, nominal {fmt(ceil_mc['lod_nominal'])}, median {med(ceil_mc)}, P(≤ 1) "
          f"{ceil_mc['p_lod_le_target']:.2f}.", "",
          "## 3. Nominal LOD against bead amount", "",
          "| Bead | " + " | ".join(f"× {m:g}" for m in MULTS) + " |", "|---|" + "---|" * len(MULTS)]
    for c in CANDIDATES:
        L.append(f"| {c['key']} | " + " | ".join(
            (fmt(s["lod"]) if s["ok"] else f"({fmt(s['lod'])})") for s in res[c["key"]]["scan"]) + " |")
    L.append("| no bead NSB | " + " | ".join((fmt(s["lod"]) if s["ok"] else f"({fmt(s['lod'])})") for s in ceil)
             + " |")
    L += ["", "Values in brackets fail the washer-lift check or do not fit the bore.", ""]
    text = "\n".join(L)
    print("\n" + text)
    if not a.quick:
        (OUT / "tier2_beads.md").write_text(text + "\n")
        (OUT / "tier2_beads.json").write_text(json.dumps(
            dict(n=n, candidates=res, ceiling=dict(scan=ceil, best_mult=cbest["mult"], mc=ceil_mc),
                 blank_share=share), indent=1, default=float))
    return 0


if __name__ == "__main__":
    sys.exit(main())
