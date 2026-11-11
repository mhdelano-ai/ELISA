#!/usr/bin/env python3
"""Model support for the kill thresholds of docs/05 section 5 (U1 label factor 0.15; U3 free HQ 1e-5 / 1e-4).

Pins the IgG-conjugate NSB label factor or the free-HQ impurity at the threshold values and evaluates the final
designs of scripts/final_designs.py (n = 1000).  Usage: python scripts/kill_thresholds.py
-> results/design/kill_thresholds.md
"""
from __future__ import annotations

import design_lib as L
import final_designs as F
from design_lib import fmt


def main():
    ps0 = L.load_ps()
    lines = ["| Design | Threshold scenario | LOD nominal | LOD median | P(success) |", "|---|---|---|---|---|"]
    for dkey, a, pmod, f in F.designs(ps0):
        if dkey not in ("P-chamb", "S-chamb", "B-bed"):
            continue
        for lab, ps in [("label factor 0.15 (U1 kill)", L.pin(ps0, **{"ma.nsb.label_factor_igg_enzyme_conjugate": 0.15})),
                        ("free HQ 1e-4 (U3 kill)", L.pin(ps0, **{"ma.chemistries.alp_hqdp.free_product_impurity": 1e-4})),
                        ("free HQ 1e-5 (U3 accept)", L.pin(ps0, **{"ma.chemistries.alp_hqdp.free_product_impurity": 1e-5}))]:
            s = L.mc(a, pmod(ps), n=1000)
            lines.append(f"| {dkey} | {lab} | {fmt(s['lod_nominal'] * f)} | {fmt(s['lod_median'] * f)} | {s['p_success']:.2f} |")
            print(lines[-1], flush=True)
    (L.OUT / "kill_thresholds.md").write_text("# Kill-threshold scenarios\n\n" + "\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
