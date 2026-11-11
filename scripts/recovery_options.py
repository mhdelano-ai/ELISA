#!/usr/bin/env python3
"""Automated ways to recover simultaneous sample + bead + conjugate incubation without reagent in the sample vial
(user decision 2026-11-11, docs/00). Uses the chamber approximation of scripts/final_designs.py / inline_chamber.py.

Options evaluated (each with the stated parameter representation; all UNVERIFIED hardware):
  A  SIA dispenser (syringe pump + selection valve) doses beads + conjugate from a stirred, cooled reservoir into a
     stirred cup; sample pushed in by the SM-FL/BSM.        -> design P-chamb (unstirred factor 0.45)
  B  The SM-FL injects beads + conjugate from a SHARED reagent vial into the cup, then the sample. No dispenser,
     but the SM-FL cannot resuspend beads in the vial      -> P-chamb with bead_dose_cv pinned at its high bound 0.15
  C  Held-up zone: sample and reagent plugs parked in an unstirred holding coil (no mixing)
                                                            -> capture factor 0.2/2.2 = 0.09 (YAML low bound / dilution)
  S  Sequential mode on hardware A (beads only into the cup; conjugate injected onto the trap) -> S-chamb
Not evaluated: merging from a BSM line (docs/02 s.1.2: no protein or bead suspensions through BSM pump heads,
check valves and mixer) - inadmissible.

Usage: python scripts/recovery_options.py  -> results/design/recovery_options.md
"""
from __future__ import annotations

import design_lib as L
import final_designs as F
import robustness as R
from design_lib import fmt


def main():
    ps0 = L.load_ps()
    d = {k: (a, pm, f) for k, a, pm, f in F.designs(ps0)}
    a_ch, pm_ch, f_ch = d["P-chamb"]
    a_sq, pm_sq, f_sq = d["S-chamb"]
    opts = [("A SIA dispenser + stirred cup (one-step)", a_ch, pm_ch, f_ch),
            ("B SM-FL injects shared bead/conjugate vial into cup (bead dose CV 0.15)", a_ch,
             lambda p: L.pin(pm_ch(p), **{"ma.capture.bead_dose_cv": 0.15}), f_ch),
            ("C unstirred held-up coil (capture factor 0.09)", a_ch,
             lambda p: L.pin(p, **{"ma.capture.in_vial_unstirred_rate_factor": 0.09}), f_ch),
            # route B with the separate SM-FL reagent vials is not re-evaluated: it shares the B4 pre-exposure
            # problem only if beads and conjugate share a vial (docs/08 B4)
            ("S sequential mode on hardware A", a_sq, pm_sq, f_sq)]
    scen = {"S0 audited": lambda p: p,
            "L6+L7 screening passed": [x for x in R.LEVERS if x[0].startswith("L6+L7")][0][1]}
    lines = ["| Option | Scenario | LOD nominal | LOD median [5-95 %] | P(LOD<=1) | P(success) | time to result |",
             "|---|---|---|---|---|---|---|"]
    for lab, a, pm, f in opts:
        for sl, fn in scen.items():
            s = L.mc(a, pm(fn(ps0)), n=L.N_FINAL, lod_scale=f)
            lines.append(f"| {lab} | {sl} | {fmt(s['lod_nominal'])} | {fmt(s['lod_median'])} "
                         f"[{fmt(s['lod_p05'])}-{fmt(s['lod_p95'])}] | ~{s['p_lod_only']:.2f} | "
                         f"~{s['p_success']:.2f} | {s['time_to_result_min']:.1f} |")
            print(lines[-1], flush=True)
    (L.OUT / "recovery_options.md").write_text(
        "# Automated recovery of simultaneous incubation (no reagent in sample vials)\n\nn = 2000, seed 20261111; "
        "'~' = chamber approximation. Revised after the final review (docs/08 S9, S13): thin-layer cell, sampled "
        "stirring factor (route C keeps its pinned 0.09), 1/0.96 applied per draw before P.\n\n" + "\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
