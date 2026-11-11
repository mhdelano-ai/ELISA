#!/usr/bin/env python3
"""One-step vs sequential mode against the detection reagent's off-rate (final review docs/08, finding S4).

chem.antibodies.koff_detection is pinned at ln2 / t1/2 for each t1/2 (the effective on-bead value E1.5 measures);
everything else keeps its prior. Designs: final_designs default (thin-layer cell, sampled chamber stirring,
1/0.96 transfer before P). The crossing of the two modes sets the mode boundary of docs/06 s4.11 / gates.yaml.

Usage: python scripts/mode_choice.py [--n 2000] -> results/design/mode_choice.md
"""
from __future__ import annotations

import argparse
import math

import design_lib as L
import final_designs as F
from design_lib import fmt

T_HALF_MIN = [10, 13, 20, 30, 45, 60, 120]
KEY = "chem.antibodies.koff_detection"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=L.N_FINAL)
    a = ap.parse_args(argv)
    ps0 = L.load_ps()
    ent = {k: (ar, pm, f) for k, ar, pm, f in F.designs(ps0) if k in ("P-chamb", "S-chamb")}
    lines = ["| detection t1/2 (min) | k_off (1/s) | P-chamb (one-step) median / P | S-chamb (sequential) median / P | "
             "P difference (one-step - sequential) |", "|---|---|---|---|---|"]
    for th in T_HALF_MIN:
        koff = math.log(2) / (th * 60.0)
        ps = L.pin(ps0, **{KEY: koff})
        r = {}
        for k, (ar, pm, f) in ent.items():
            r[k] = L.mc(ar, pm(ps), n=a.n, lod_scale=f)
        d = r["P-chamb"]["p_success"] - r["S-chamb"]["p_success"]
        lines.append(f"| {th} | {koff:.2g} | {fmt(r['P-chamb']['lod_median'])} / {r['P-chamb']['p_success']:.2f} | "
                     f"{fmt(r['S-chamb']['lod_median'])} / {r['S-chamb']['p_success']:.2f} | {d:+.2f} |")
        print(lines[-1], flush=True)
    txt = ("# Mode choice against the detection reagent off-rate (docs/08 S4)\n\n"
           f"n = {a.n}, seed {L.SEED}; k_off,detection pinned; final_designs default designs. Monte Carlo noise on a "
           "P difference between two designs evaluated with common random numbers is smaller than on each P, but "
           "differences below ~0.05 are not decision-grade (docs/08 W7).\n\n" + "\n".join(lines) + "\n")
    (L.OUT / "mode_choice.md").write_text(txt)


if __name__ == "__main__":
    main()
