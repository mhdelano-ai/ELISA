#!/usr/bin/env python3
"""Model support for the kill thresholds of docs/05 section 5 (U1 label factor 0.15; U3 free HQ 1e-5 / 1e-4).

Enters the IgG-conjugate NSB label factor or the free-HQ impurity at the threshold values THE WAY A BENCH VALUE IS
ENTERED (design_lib.apply_bench_values = elisa_auto.model_feedback: the coupled NSB factors are pinned at nominal when
the label factor is given) and evaluates the final designs of scripts/final_designs.py (n = 1000). Revised after the
final review (docs/08 B3): before, only the label factor was pinned, so P at the threshold was still spread over the
reference NSB rate and the bead surface factor. The full G1 table is scripts/g1_decision_table.py.
Usage: python scripts/kill_thresholds.py
-> results/design/kill_thresholds.md
"""
from __future__ import annotations

import design_lib as L
import final_designs as F
from design_lib import fmt


def main():
    ps0 = L.load_ps()
    lf, hq = "ma.nsb.label_factor_igg_enzyme_conjugate", "ma.chemistries.alp_hqdp.free_product_impurity"
    lines = ["| Design | Threshold scenario (bench-consistent) | LOD nominal | LOD median | P(success) |", "|---|---|---|---|---|"]
    for dkey, a, pmod, f in F.designs(ps0):
        if dkey not in ("P-chamb", "S-chamb", "B-bed"):
            continue
        for lab, meas in [("label factor 0.04 (docs/05 U1 confirm level)", {lf: {"value": 0.04}}),
                          ("label factor 0.15 (docs/05 U1 kill level)", {lf: {"value": 0.15}}),
                          ("free HQ 1e-4 (U3 kill)", {hq: {"value": 1e-4}}),
                          ("free HQ 1e-5 (U3 accept)", {hq: {"value": 1e-5}})]:
            s = L.mc(a, pmod(L.apply_bench_values(ps0, meas)), n=1000, lod_scale=f)
            lines.append(f"| {dkey} | {lab} | {fmt(s['lod_nominal'])} | {fmt(s['lod_median'])} | {s['p_success']:.2f} |")
            print(lines[-1], flush=True)
    (L.OUT / "kill_thresholds.md").write_text(
        "# Kill-threshold scenarios (bench-consistent; revised after the final review, docs/08 B3)\n\n"
        "n = 1000; designs of final_designs.py (thin-layer default, S13 corrections). The decision rule is now on P "
        "(results/design/g1_decision_table.md); these thresholds are fast screens only.\n\n" + "\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
