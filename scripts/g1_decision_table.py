#!/usr/bin/env python3
"""G1 decision table, evaluated the way bench values will actually be used (final review docs/08, finding B3).

At G1 the measured label factor (docs/06 E1.3) is entered with the two coupled NSB factors
(chem.nsb.nsb_effective_rate_constant, ma.nsb.surface_factor_magnetic_beads) pinned at their nominal values,
exactly as `python -m elisa_auto.model_feedback` does (shared code: design_lib.apply_bench_values). Before the
review, scripts/kill_thresholds.py pinned only the label factor, so the quoted P at a threshold was still spread
over the other two factors and was not the P the bench value would imply.

Table 1: P(success) and median LOD against the label factor for the primary (P-chamb, one-step chamber), the
sequential mode (S-chamb) and the backup bed (B-bed), each without and with lever L4 (immune-complex transfer).
Table 2 (G1a, docs/06 s4.10): P of the two chamber modes against label factor x free HQ in the HQDP lot (U1 + U3).
All other parameters keep their docs/05 priors. Designs: scripts/final_designs.py default variant (commercial
thin-layer cell, sampled stirring factor, 1/0.96 transfer factor before P; docs/08 S9, S13).
The decision rule itself is design_lib.g1_decision (thresholds G1_GO_MIN, G1_LEVER_MIN), fixed before any data.

Usage: python scripts/g1_decision_table.py [--n 2000] [--n2 1000] -> results/design/g1_decision_table.md
"""
from __future__ import annotations

import argparse

import design_lib as L
import final_designs as F
from design_lib import fmt

LF_GRID = [0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10, 0.12, 0.15, 0.20, 0.30]
HQ_GRID = [1e-6, 1e-5, 3e-5, 1e-4]
LF2_GRID = [0.01, 0.02, 0.04, 0.06, 0.08, 0.10, 0.15]
DESIGNS = ("P-chamb", "S-chamb", "B-bed")
LF_KEY = "ma.nsb.label_factor_igg_enzyme_conjugate"
HQ_KEY = "ma.chemistries.alp_hqdp.free_product_impurity"


def evaluate_point(entries, ps0, measured: dict, n: int, with_l4: bool = True) -> dict:
    """{design: {'p', 'median', 'p_l4', 'median_l4'}} for one set of bench values."""
    ps1 = L.apply_bench_values(ps0, measured)
    out = {}
    for dkey, arch, pmod, f in entries:
        s = L.mc(arch, pmod(ps1), n=n, lod_scale=f)
        r = {"p": s["p_success"], "median": s["lod_median"], "nominal": s["lod_nominal"]}
        if with_l4:
            s4 = L.mc(arch, pmod(L.l4_transfer(ps1)), n=n, lod_scale=f)
            r.update(p_l4=s4["p_success"], median_l4=s4["lod_median"])
        out[dkey] = r
    return out


def decision(point: dict) -> str:
    return L.g1_decision({d: v["p"] for d, v in point.items()}, {d: v.get("p_l4", 0.0) for d, v in point.items()})


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=L.N_FINAL)
    ap.add_argument("--n2", type=int, default=1000)
    a = ap.parse_args(argv)
    ps0 = L.load_ps()
    entries = [e for e in F.designs(ps0) if e[0] in DESIGNS]
    t1 = ["| label factor | tube blank-equivalent B (P-vial reference, pg/mL) | "
          + " | ".join(f"{d}: median / P | {d} + L4: median / P" for d in DESIGNS) + " | G1 rule |",
          "|---" * (3 + 2 * len(DESIGNS)) + "|"]
    screen = []
    for lf in LF_GRID:
        pt = evaluate_point(entries, ps0, {LF_KEY: {"value": lf}}, a.n)
        b = 24.0 * lf      # docs/08 B3: B ~ 24 x factor (P-vial nominal 0.96 pg/mL at 0.04)
        cells = " | ".join(f"{fmt(v['median'])} / {v['p']:.2f} | {fmt(v['median_l4'])} / {v['p_l4']:.2f}"
                           for v in (pt[d] for d in DESIGNS))
        dec = decision(pt)
        screen.append((lf, dec, pt))
        t1.append(f"| {lf:g} | {b:.2g} | {cells} | {dec} |")
        print(t1[-1], flush=True)
    t2 = ["| label factor | " + " | ".join(f"free HQ {h:g}: P-chamb / S-chamb P" for h in HQ_GRID) + " |",
          "|---" * (1 + len(HQ_GRID)) + "|"]
    chamb = [e for e in entries if e[0] in ("P-chamb", "S-chamb")]
    for lf in LF2_GRID:
        cells = []
        for h in HQ_GRID:
            pt = evaluate_point(chamb, ps0, {LF_KEY: {"value": lf}, HQ_KEY: {"value": h}}, a.n2, with_l4=False)
            cells.append(f"{pt['P-chamb']['p']:.2f} / {pt['S-chamb']['p']:.2f}")
        t2.append(f"| {lf:g} | " + " | ".join(cells) + " |")
        print(t2[-1], flush=True)
    go = [lf for lf, d, _ in screen if d == "GO"]
    stop = [lf for lf, d, _ in screen if d == "STOP"]
    txt = ("# G1 decision table (bench-consistent evaluation; docs/08 B3)\n\n"
           f"Table 1: n = {a.n}, seed {L.SEED}; Table 2: n = {a.n2}. The label factor is entered as a bench value "
           "would be (`design_lib.apply_bench_values`, the code `elisa_auto.model_feedback` uses): coupled NSB "
           "factors pinned at nominal (4e-11 m/s, bead surface factor 1); every other parameter keeps its prior. "
           "Designs: `final_designs.designs()` default (thin-layer cell; chamber stirring factor sampled; 1/0.96 "
           "before P). L4 = immune-complex transfer, label factor x 0.1/0.7 (UNVERIFIED lever magnitude). Monte "
           "Carlo sampling noise on P: about +/-0.02 (95 %) at n = 2000, +/-0.03 at n = 1000.\n\n"
           f"Rule (design_lib.g1_decision, fixed before data): GO if max P over admissible designs >= {L.G1_GO_MIN}; "
           f"GO-WITH-LEVER if below that but max P including L4 >= {L.G1_LEVER_MIN}; STOP otherwise.\n\n"
           "## Table 1 - P(success) and median LOD (pg/mL) against the measured label factor\n\n"
           + "\n".join(t1) + "\n\n"
           f"Label-factor screen implied by Table 1 (other Stage-1 values at their priors): GO up to "
           f"{max(go) if go else 'none'}; STOP from {min(stop) if stop else 'none in the grid'}.\n\n"
           "## Table 2 - G1a (U1 + U3): P(success) of P-chamb / S-chamb against label factor and free HQ\n\n"
           + "\n".join(t2) + "\n")
    (L.OUT / "g1_decision_table.md").write_text(txt)


if __name__ == "__main__":
    main()
