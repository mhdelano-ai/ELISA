#!/usr/bin/env python3
"""Decomposition of the change in the headline predictions made by the final-review corrections (docs/08).

Steps (cumulative), for the primary (P-chamb), the sequential mode (S-chamb) and the backup bed (B-bed), in the
audited scenario (S0) and after reagent + substrate screening (L6 + L7):
  a  docs/05 exactly: flow IDA, chamber stirring factor pinned at 0.45, P before the 1/0.96 factor, Ki prior
     of chemistry.yaml (2 uM, 1-540 uM)
  b  + 1/0.96 transfer factor applied per draw before P (S13)
  c  + chamber stirring factor sampled on [0.2, 1.0]/2.2 (S13)
  d  + commercial single-channel thin-layer cell instead of the flow IDA (S9, Stage-3 default)
  e  + phosphate Ki override (UNVERIFIED, 0.2 uM - 1 mM; S10) = the revised headline
Usage: python scripts/review_changes.py [--n 2000] -> results/design/review_changes.md
"""
from __future__ import annotations

import argparse
from dataclasses import replace

import design_lib as L
import final_designs as F
import robustness as R
from design_lib import fmt

KI = "chem.enzymes.alp.phosphate_inhibition_Ki"
STEPS = [("a docs/05 as published", "docs05", "docs05", "ida_flow", True),
         ("b + transfer factor before P (S13)", "docs05", "review", "ida_flow", True),
         ("c + stirring factor sampled (S13)", "review_ida", "review", "ida_flow", True),
         ("d + thin-layer cell default (S9)", "review_ida", "review", "thin_layer", True),
         ("e + Ki override UNVERIFIED 0.2 uM-1 mM (S10) = revised", "review_ida", "review", "thin_layer", False)]


def old_ki(ps):
    return L.with_bounds(ps, KI, value=2e-6, low=1e-6, high=5.4e-4)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=L.N_FINAL)
    a = ap.parse_args(argv)
    ps0 = L.load_ps()
    l67 = next(x for x in R.LEVERS if x[0].startswith("L6+L7"))[1]
    lines = ["| Design | Scenario | Step | LOD nominal | LOD median [5-95 %] | P(success) | ULOQ nominal |",
             "|---|---|---|---|---|---|---|"]
    for dk in ("P-chamb", "S-chamb", "B-bed"):
        for sl, sfn in (("S0", lambda p: p), ("L6+L7", l67)):
            for label, variant, conv, det, use_old_ki in STEPS:
                ent = next(e for e in F.designs(ps0, variant) if e[0] == dk)
                _, arch, pm, f = ent
                base = old_ki(ps0) if use_old_ki else ps0
                s = F.summarise(replace(arch, detector=det), pm(sfn(base)), f, a.n, conv)
                ap_ = "~" if f != 1.0 else ""
                lines.append(f"| {dk} | {sl} | {label} | {fmt(s['lod_nominal'])} | {fmt(s['lod_median'])} "
                             f"[{fmt(s['lod_p05'])}-{fmt(s['lod_p95'])}] | {ap_}{s['p_success']:.2f} | "
                             f"{fmt(s['uloq_nominal'])} |")
                print(lines[-1], flush=True)
    txt = ("# Effect of the final-review corrections on the headline predictions\n\n"
           f"n = {a.n}, seed {L.SEED}. Steps are cumulative (see the script docstring). Row 'a' reproduces docs/05 "
           "and results/design/final_designs.md as committed before the review.\n\n" + "\n".join(lines) + "\n")
    (L.OUT / "review_changes.md").write_text(txt)


if __name__ == "__main__":
    main()
