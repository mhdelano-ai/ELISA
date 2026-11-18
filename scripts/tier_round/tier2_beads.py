#!/usr/bin/env python3
"""Alternative capture beads for the tier-2 cell with the bed inside (docs/35): which bead gives the lowest LOD.

  python scripts/tier_round/tier2_beads.py [--n 2000] [--quick]
writes results/tier_round/tier2_beads.md and tier2_beads.json (not with --quick).

Each candidate is the docs/34 cell (`tier2_cell.cell_design`) with three bead properties changed:
  * diameter (bed volume for a given bead area, retainer: membrane below 7 um, screen alone above);
  * the non-specific binding of the conjugate per unit bead area.  M-280's bed keeps the packed-bed factor of
    docs/34 (3, 1-30); a share phi of it sits on the capture-antibody layer and is the same for every bead, the
    rest scales with the bead surface relative to M-280 (`rel`).  phi and rel are UNVERIFIED judgement (docs/35
    section 3) and are drawn independently of the kit's parameters, so that P(bead beats M-280) comes from paired
    draws;
  * the active capture sites per unit area: biotinylated F(ab')2 on streptavidin (the kit's
    `tr.capture.site_factor_streptavidin_biotin`, 1 [0.4-1]), covalent random coupling (0.7 [0.3-1], UNVERIFIED
    judgement; 1/3 from chem.antibodies.oriented_vs_random_capacity_gain and 1 as sensitivity) or a
    bead-specific value (UNVERIFIED);
  * `load`, the capture antibody per area relative to M-280 coated as docs/30: the capture-layer share of the
    NSB scales with it (covalent beads keep load 1: the inactive antibody is still there).
Then the bead amount is optimised (nominal LOD) within two limits from docs/34: the retainer washer must still hold
the stack at 80 uL/min with a margin of 2 (the check of tier2_cell.py), and the bed must fit the bed bore (0.5 mm wide, 2.5 mm long).

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

PHI = (0.5, 0.1, 0.9)      # share of M-280's bead NSB that sits on the capture-antibody layer (UNVERIFIED, docs/35 §3)
COV = (0.7, 0.3, 1.0)      # covalent random F(ab')2 relative to biotin-F(ab')2 on streptavidin: UNVERIFIED judgement
COV_PELUSO = (1 / 3.0, 1 / 10.0, 1 / 1.5)   # sensitivity: 1 / chem.antibodies.oriented_vs_random_capacity_gain
# (Peluso2003 compares site-specific with random biotinylation, both on streptavidin; review round 2, M1)

# candidates: rel = NSB per area of the bead surface (not of the capture layer) relative to M-280 Streptavidin as
# used in the project (re-blocked in IgG-free BSA), value, low, high; sites = active capture sites relative to the
# oriented monolayer of chem.surfaces (None: the kit's streptavidin-biotin parameter, 1 [0.4-1]).  All UNVERIFIED
# judgement unless docs/35 §3 says otherwise.
CANDIDATES = [
    dict(key="m280", label="Dynabeads M-280 Streptavidin (11205D); current choice", d_um=2.8,
         rel=(1.0, 1.0, 1.0), sites=None, status="current"),
    dict(key="m270sa", label="Dynabeads M-270 Streptavidin (65305)", d_um=2.8,
         rel=(0.8, 0.4, 2.0), sites=None, status="catalogue, drop-in"),
    dict(key="lodesa", label="Agilent LodeStars 2.7 µm Streptavidin (PL6727-1001)", d_um=2.7,
         rel=(0.8, 0.4, 2.0), sites=(0.7, 0.5, 1.0), load=0.7, status="catalogue, drop-in"),
    dict(key="magnalink", label="Vector MagnaLINK Streptavidin 2.8 µm (M-1003), coated as docs/30 (10 µg/mg)",
         d_um=2.8, rel=(0.8, 0.4, 3.0), sites=None, status="catalogue [V vendor page, review round 2]"),
    dict(key="magplex", label="Luminex MagPlex-Avidin 6.5 µm (deglycosylated avidin)", d_um=6.5,
         rel=(0.8, 0.4, 2.0), sites=(0.7, 0.3, 1.0), status="catalogue [S]"),
    dict(key="lodecooh", label="Agilent LodeStars 2.7 µm Carboxyl (PL6727-0001), F(ab')₂ by EDC/NHS", d_um=2.7,
         rel=(0.8, 0.4, 2.0), sites=COV, status="catalogue, covalent coupling"),
    dict(key="m270ep", label="Dynabeads M-270 Epoxy (14301), F(ab')₂ coupled covalently", d_um=2.8,
         rel=(0.8, 0.4, 2.0), sites=COV, status="catalogue, covalent coupling"),
    dict(key="peg10", label="micromod micromer-M PEG-COOH 10 µm (08-56-104), F(ab')₂ coupled covalently",
         d_um=10.0, rel=(0.5, 0.15, 1.5), sites=COV, status="catalogue (2010 data sheet)"),
    dict(key="brush", label="POEGMA or carboxybetaine brush on M-270 Amine (in house), antibody entangled or "
         "coupled in the brush", d_um=2.8, rel=(0.25, 0.05, 1.0), sites=(0.3, 0.05, 1.0),
         load=0.3, status="development project"),
    dict(key="mm_sa10", label="micromod micromer-M Streptavidin 10 µm (08-19-104), sub-monolayer streptavidin",
         d_um=10.0, rel=(1.3, 0.7, 7.0), sites=(0.4, 0.1, 0.8), load=0.4, status="catalogue"),
    dict(key="svp", label="Spherotech SVP-100-4 streptavidin polystyrene 10–14 µm (docs/34 fallback)",
         d_um=12.0, rel=(1.3, 0.7, 7.0), sites=(0.7, 0.1, 1.0), status="catalogue, fallback of docs/34"),
    dict(key="silica5", label="streptavidin silica 5 µm, non-porous (Bangs CS01002 type)", d_um=5.0,
         rel=(1.3, 0.7, 7.0), sites=(0.7, 0.1, 1.0), status="catalogue (not checked)"),
]
MULTS = (0.25, 0.35, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0)   # bead area relative to 24.4 mm2


def beads_dict(c, mult):
    d = c["d_um"] * 1e-6
    V = V_REF_UL * mult * c["d_um"] / 2.8                   # same porosity: V ~ A d
    return dict(key=c["key"], label=c["label"], d_p=d, V_bed_uL=V)


def n_beads(c, mult):
    return A_REF_MM2 * mult * 1e-6 / (math.pi * (c["d_um"] * 1e-6) ** 2)


def ltri(v, rng, n):
    """Draws of (value, low, high) as the kit samples: log-triangular for ranges >= 3x, else triangular."""
    lo, mode, hi = v[1], v[0], v[2]
    if lo == hi:
        return np.full(n, mode)
    if lo > 0 and hi / lo >= 3.0:
        return np.exp(rng.triangular(np.log(lo), np.log(mode), np.log(hi), size=n))
    return rng.triangular(lo, mode, hi, size=n)


def bead_mult(c, phi):
    """Bed factor relative to M-280: capture layer (scales with the capture antibody loaded per area, `load`,
    relative to M-280 coated as in docs/30) + bead surface (`rel`)."""
    return phi * c.get("load", 1.0) + (1.0 - phi) * c["rel"][0]


def pset(ps, c, phi=PHI[0], zero_nsb=False):
    """Nominal parameter set of a candidate: the M-280 packed-bed factor (3, 1-30) times bead_mult; sites."""
    b = ps.params[PB]
    m = 1e-9 if zero_nsb else bead_mult(c, phi)
    out = R.L.with_bounds(ps, PB, value=float(b.value) * m, low=float(b.low) * m, high=float(b.high) * m)
    if c["sites"] is not None:
        out = R.L.with_bounds(out, SITE, value=c["sites"][0], low=c["sites"][1], high=c["sites"][2])
    return out


def paired_mc(c, mult, ps, n):
    """Monte Carlo with the kit's seed for every shared parameter (so the beads are compared on the same draws),
    and independent draws of the capture-layer share and of the bead's relative factor, applied to the sampled
    packed-bed factor.  M-280 (rel = 1) gets exactly the kit's sampling."""
    design = T.cell_design(beads_dict(c, mult))
    base = pset(ps, dict(c, rel=(1.0, 1.0, 1.0), load=1.0))       # packed-bed factor of M-280, candidate sites
    probe = base.copy()
    probe.accessed = set()
    nom = tk.evaluate_bed(design, pset(ps, c))
    tk.evaluate_bed(design, probe)
    keys = sorted(probe.accessed)
    seed = int(ps.extra.get("monte_carlo", {}).get("seed", 0))
    sampled = base.sample(n, np.random.default_rng(seed), keys)
    rng2 = np.random.default_rng(seed + 1)
    phi = ltri(PHI, rng2, n)
    rel = ltri(c["rel"], rng2, n)
    sampled.values[PB] = np.asarray(sampled.values[PB]) * (phi * c.get("load", 1.0) + (1.0 - phi) * rel)
    res = tk.evaluate_bed(design, sampled)
    lod = np.where(np.isfinite(np.asarray(res.lod_pgml, float)), np.asarray(res.lod_pgml, float), 1e30)
    q = lambda x: float(np.percentile(lod, x))
    return dict(lod_nominal=float(np.asarray(nom.lod_pgml).reshape(-1)[0]), lod_median=q(50), lod_p05=q(5),
                lod_p95=q(95), p_lod_le_target=float(np.mean(lod <= 1.0)), keys=keys, _lod=lod,
                _pb=np.asarray(sampled.values[PB]), _mult=phi * c.get("load", 1.0) + (1.0 - phi) * rel)


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
    PHIS = (0.0, PHI[0], 0.8)

    def scan(c, phi, zero=False):
        p = pset(ps, c, phi, zero_nsb=zero)
        rows = []
        for m in MULTS:
            ok, lim = limits(c, m, mech)
            rows.append(dict(mult=m, n_beads=n_beads(c, m), ok=ok,
                             lod=nominal(T.cell_design(beads_dict(c, m)), p), **lim))
        best = min((r for r in rows if r["ok"]), key=lambda r: r["lod"])
        return rows, best

    res = {}
    for c in CANDIDATES:
        by_phi = {phi: scan(c, phi) for phi in PHIS}
        rows, best = by_phi[PHI[0]]
        r1 = paired_mc(c, 1.0, ps, n)
        rb = paired_mc(c, best["mult"], ps, n)
        res[c["key"]] = dict(candidate=c, scan=rows, best_mult=best["mult"], best_row=best, at_ref=r1, at_best=rb,
                             phi_scan={str(phi): dict(best_mult=v[1]["mult"], lod=v[1]["lod"])
                                       for phi, v in by_phi.items()})
    ref = res["m280"]["at_ref"]
    m280_at = {1.0: ref}
    for k, r in res.items():
        m = r["best_mult"]
        if m not in m280_at:
            m280_at[m] = paired_mc(CANDIDATES[0], m, ps, n)
        for tag in ("at_ref", "at_best"):
            r[tag]["p_better_than_m280"] = float(np.mean(r[tag]["_lod"] < ref["_lod"]))
            r[tag]["same_keys"] = r[tag]["keys"] == ref["keys"]
        r["at_best"]["p_better_than_m280_same_area"] = float(np.mean(r["at_best"]["_lod"] < m280_at[m]["_lod"]))

        print(f"{k:9s} same area {r['at_ref']['lod_nominal']:.3g} (median {r['at_ref']['lod_median']:.3g}, "
              f"P<M280 {r['at_ref']['p_better_than_m280']:.2f})  best x{r['best_mult']:g} "
              f"{r['at_best']['lod_nominal']:.3g} (median {r['at_best']['lod_median']:.3g}, "
              f"P<M280 {r['at_best']['p_better_than_m280']:.2f})", flush=True)

    # sensitivity variants (review round 2): best amount, nominal and paired median
    C = {c["key"]: c for c in CANDIDATES}
    VARIANTS = [
        ("covalent beads at Peluso's 1/3 of the sites (Rev B assumption)", "peg10", dict(sites=COV_PELUSO)),
        ("the same, LodeStars Carboxyl", "lodecooh", dict(sites=COV_PELUSO)),
        ("PEG-COOH 10 µm with the sites of M-280 (covalent as good as oriented)", "peg10", dict(sites=(1.0, 0.4, 1.0))),
        ("MagnaLINK coated with 3 × the antibody (30 µg/mg), sites 2 (0.7–3)", "magnalink",
         dict(sites=(2.0, 0.7, 3.0), load=3.0)),
        ("the same, all of it active: sites 3", "magnalink", dict(sites=(3.0, 1.0, 3.0), load=3.0)),
        ("the same, the extra antibody inaccessible: sites 1", "magnalink", dict(sites=(1.0, 0.4, 1.0), load=3.0)),
        ("the same with sites 3, capture-layer NSB not scaling with the load", "magnalink",
         dict(sites=(3.0, 1.0, 3.0), load=1.0)),
        ("MagnaLINK as docs/30, its 3D polymer surface 3 × M-280", "magnalink", dict(rel=(3.0, 1.0, 10.0))),
        ("brush with the capture layer per area of M-280 (load 1)", "brush", dict(load=1.0)),
        ("brush with the sites and load of M-280 (antibody fully active in the brush)", "brush",
         dict(sites=(1.0, 0.4, 1.0), load=1.0)),
    ]
    variants = []
    for label, key, ov in VARIANTS:
        c = dict(C[key], **ov)
        rows, best = scan(c, PHI[0])
        mc = paired_mc(c, best["mult"], ps, n)
        variants.append(dict(label=label, key=key, best_mult=best["mult"], lod_nominal=best["lod"],
                             lod_median=mc["lod_median"], p_better=float(np.mean(mc["_lod"] < ref["_lod"])),
                             same_keys=mc["keys"] == ref["keys"]))

    # the ceiling of the bead lever: no NSB on the beads at all (M-280 geometry and sites)
    ceil, cbest = scan(CANDIDATES[0], 0.0, zero=True)
    surf0, sbest = scan(dict(CANDIDATES[0], rel=(0.0, 0.0, 0.0)), PHI[0])     # bead surface clean, capture layer kept

    # where the blank enzymes of the M-280 cell sit (nominal)
    d = T.cell_design()
    b = d["bed"]
    share = {}
    for name, key, area in (("beads", b["surface_factor_key"], A_REF_MM2 * 1e-6),
                            ("retainer and washer hole", b["extra_factor_key"], b["extra_area"]),
                            ("exit bore", b["bore_factor_key"], b["bore_area"]),
                            ("bore above the bed and line", b["upstream_factor_key"], b["upstream_area"])):
        fac = float(ps.params[key].value)
        share[name] = dict(area_mm2=area * 1e6, factor=fac, area_x_factor=area * 1e6 * fac, key=key)
    tot = sum(v["area_x_factor"] for v in share.values())
    for v in share.values():
        v["share"] = v["area_x_factor"] / tot

    # ---- checks -----------------------------------------------------------------------------------------------
    t34 = json.loads((OUT / "tier2_cell.json").read_text())["cases"]["cell"]
    checks = [
        ("M-280 at 1x reproduces docs/34 (nominal and median)",
         abs(ref["lod_nominal"] / t34["lod_nominal"] - 1) < 1e-6 and (a.quick or abs(ref["lod_median"] / t34["lod_median"] - 1) < 1e-6),
         f"{ref['lod_nominal']:.4g} / {ref['lod_median']:.4g} vs {t34['lod_nominal']:.4g} / {t34['lod_median']:.4g}"),
        ("every candidate is sampled on the same parameter keys as M-280 (paired draws)",
         all(r[t]["same_keys"] for r in res.values() for t in ("at_ref", "at_best")), ""),
        ("no chosen best amount (candidates and variants) sits at the low edge of the scan",
         all(r["best_mult"] != MULTS[0] for r in res.values()) and all(v["best_mult"] != MULTS[0] for v in variants), ""),
        ("in the paired Monte Carlo each bead's sampled packed-bed factor is M-280's draw times "
         "(φ·load + (1 − φ)·rel), applied once",
         all(np.allclose(r[t]["_pb"], ref["_pb"] * r[t]["_mult"], rtol=1e-12) for r in res.values()
             for t in ("at_ref", "at_best")) and all(v["same_keys"] for v in variants), ""),
    ]

    # ---- report -----------------------------------------------------------------------------------------------
    fmt = T.fmt
    med = lambda k: f"{fmt(k['lod_median'])} [{fmt(k['lod_p05'])}–{fmt(k['lod_p95'])}]"
    L = ["# Alternative capture beads for the tier-2 cell — numbers behind docs/35", "",
         f"Generated by `scripts/tier_round/tier2_beads.py` (Monte Carlo n = {n}, seed of the kit; the capture-layer "
         "share and the bead factors are drawn with the seed + 1, the same for every bead). The cell is the docs/34 "
         "cell; only the beads change. Model predictions, not measurements; every bead factor is a judgement "
         "(UNVERIFIED, docs/35 §3).", "", "## 0. Checks", "", "| Check | Result | Value |", "|---|---|---|"]
    L += [f"| {c[0]} | {'pass' if c[1] else '**FAIL**'} | {c[2]} |" for c in checks]
    L += ["", "## 1. Where the non-specific enzyme of the M-280 cell sits (nominal, area × surface factor)", "",
          "| Surface | Area (mm²) | Factor (key) | Share |", "|---|---|---|---|"]
    for k, v in share.items():
        L.append(f"| {k} | {v['area_mm2']:.3g} | {v['factor']:g} (`{v['key']}`) | {100 * v['share']:.0f} % |")
    L += ["", "## 2. Candidates (LOD in pg/mL)", "",
          f"Bed factor = M-280's `{PB}` (3, 1–30) × (φ·load + (1 − φ)·rel), φ = share of M-280's bead NSB on the "
          f"capture-antibody layer, {PHI[0]} ({PHI[1]}–{PHI[2]}); rel = the bead surface relative to M-280. "
          "'Same area' = 24.4 mm² of beads (1×10⁶ M-280). 'Best amount' = lowest nominal LOD over 0.25–8 × that "
          "area, within the washer-lift check at 80 µL/min and the bed bore (0.5 mm × 2.5 mm). P(< M-280) = share "
          "of paired draws in which the bead's LOD is below that of 1×10⁶ M-280.", "",
          "P(< M-280, same area) compares with M-280 at the bead's best area. load = capture antibody per area "
          "relative to M-280 coated as in docs/30; the capture-layer share scales with it.", "",
          "| Bead | rel (low–high) | Sites (low–high); load | Same area: nominal; median [5–95 %]; P(≤ 1); P(< M-280) | "
          "Best amount: × area (beads) | Best: nominal; median [5–95 %]; P(≤ 1); P(< M-280); P(< M-280, same area) "
          "| Bed Δp at 80 µL/min (bar) |", "|---|---|---|---|---|---|---|"]
    for c in CANDIDATES:
        r = res[c["key"]]
        a1, ab, bs = r["at_ref"], r["at_best"], r["best_row"]
        s_ = "kit (1, 0.4–1)" if c["sites"] is None else f"{c['sites'][0]:.2g} ({c['sites'][1]:.2g}–{c['sites'][2]:.2g})"
        s_ += f"; {c.get('load', 1.0):g}"
        L.append(f"| {c['label']} | {c['rel'][0]:g} ({c['rel'][1]:g}–{c['rel'][2]:g}) | {s_} | "
                 f"{fmt(a1['lod_nominal'])}; {med(a1)}; {a1['p_lod_le_target']:.2f}; {a1['p_better_than_m280']:.2f} | "
                 f"{r['best_mult']:g} ({bs['n_beads']:.2g}) | {fmt(ab['lod_nominal'])}; {med(ab)}; "
                 f"{ab['p_lod_le_target']:.2f}; {ab['p_better_than_m280']:.2f}; "
                 f"{ab['p_better_than_m280_same_area']:.2f} | {bs['dp_bed_80_bar']:.2g} |")
    at1 = lambda rows: fmt(next(x["lod"] for x in rows if x["mult"] == 1.0))
    L += ["", "Limits of the bead lever (M-280 geometry and sites, nominal): a bead surface with no NSB, the "
          f"capture layer kept (φ = {PHI[0]}): same area {at1(surf0)}, best × {sbest['mult']:g} {fmt(sbest['lod'])}. "
          f"No NSB on the beads at all, capture layer included: same area {at1(ceil)}, best × {cbest['mult']:g} "
          f"{fmt(cbest['lod'])} (at the edge of the allowed amounts: 6 × fails the washer-lift check).", "",
          "## 3. Best-amount nominal LOD against the capture-layer share φ", "",
          "| Bead | " + " | ".join(f"φ = {p:g}: × amount, LOD" for p in PHIS) + " |", "|---|" + "---|" * len(PHIS)]
    for c in CANDIDATES:
        ps_ = res[c["key"]]["phi_scan"]
        L.append(f"| {c['key']} | " + " | ".join(f"× {ps_[str(p)]['best_mult']:g}, {fmt(ps_[str(p)]['lod'])}"
                                              for p in PHIS) + " |")
    L += ["", f"## 3a. Sensitivity (φ = {PHI[0]}, best amount)", "",
          "| Variant | Best × area | Nominal | Median | P(< M-280) |", "|---|---|---|---|---|"]
    L += [f"| {v['label']} | {v['best_mult']:g} | {fmt(v['lod_nominal'])} | {fmt(v['lod_median'])} | "
          f"{v['p_better']:.2f} |" for v in variants]
    L += ["", f"## 4. Nominal LOD against bead amount (φ = {PHI[0]})", "",
          "| Bead | " + " | ".join(f"× {m:g}" for m in MULTS) + " |", "|---|" + "---|" * len(MULTS)]
    for c in CANDIDATES:
        L.append(f"| {c['key']} | " + " | ".join(
            (fmt(s["lod"]) if s["ok"] else f"({fmt(s['lod'])})") for s in res[c["key"]]["scan"]) + " |")
    L.append("| bead surface clean (φ kept) | " + " | ".join((fmt(s["lod"]) if s["ok"] else f"({fmt(s['lod'])})")
                                                        for s in surf0) + " |")
    L.append("| no bead NSB at all | " + " | ".join((fmt(s["lod"]) if s["ok"] else f"({fmt(s['lod'])})") for s in ceil)
             + " |")
    L += ["", "Values in brackets fail the washer-lift check or do not fit the bore.", ""]
    text = "\n".join(L)
    print("\n" + text)
    if not a.quick:
        for r in res.values():
            for t in ("at_ref", "at_best"):
                for x in ("_lod", "_pb", "_mult"):
                    r[t].pop(x, None)
        (OUT / "tier2_beads.md").write_text(text + "\n")
        (OUT / "tier2_beads.json").write_text(json.dumps(
            dict(n=n, phi=PHI, candidates=res, ceiling=dict(scan=ceil, best=cbest, surface_clean=dict(scan=surf0, best=sbest)), blank_share=share, variants=variants,
                 checks=[dict(check=c[0], ok=bool(c[1]), value=c[2]) for c in checks]), indent=1, default=float))
    return 0 if all(c[1] for c in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
