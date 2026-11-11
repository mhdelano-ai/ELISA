#!/usr/bin/env python3
"""Approximate evaluation of the one-step format with a TIMED, IN-LINE incubation chamber instead of
pre-filled vials (docs/05 section 4): the SM-FL injects only the sample; an external syringe pump doses
beads + conjugate from a stirred, cooled reservoir into a ~220 uL stirred chamber on valve V1; after the
incubation the chamber is emptied through the magnetic trap.

The model has no chamber element, so the variant is represented with existing parameters (all stated):
  * capture rate: chamber stirred (ma.capture.in_vial_unstirred_rate_factor -> 1.0, its upper bound = well
    mixed) but the sample is diluted ~2.2x (2 loop volumes of transfer + 20 uL reagent), and the same total
    number of beads is used -> effective factor 1.0 / 2.2 = 0.45 (pinned);
  * conjugate concentration in the chamber kept at the design value (dose scaled by the dilution);
  * emptying the chamber through the trap: 3 chamber volumes = 660 uL at 100 uL/min = 6.6 min, represented
    by hw.smfl.loop_flush_volumes_for_transfer = 6.6 (sets both load time and the convective transfer of
    beads, 1 - 1/(4 x 6.6) = 0.96, close to a stirred tank's 1 - e^-3 = 0.95);
  * the 2 min loop -> chamber transfer of the sample is added to the timeline through
    ma.timing.post_sample_wash (+2 min), and analyte loss in that transfer (~4 %, docs/02 table: 0.96 at
    2 loop volumes) is applied as a 1/0.96 factor on the reported LOD.
  * time to result = model cycle + incubation (the incubation now starts at injection, so it is counted
    exactly, and it is the same for every sample in the queue).
These are approximations; the chamber itself is UNVERIFIED hardware (bench item U6 in docs/05).

Usage: python scripts/inline_chamber.py  -> results/design/inline_chamber.md
"""
from __future__ import annotations

import json
from dataclasses import replace

import design_lib as L
import final_designs as F
from design_lib import fmt

TRANSFER = 0.96


def main():
    ps = L.load_ps()
    rec = json.load(open(L.OUT / "optimum_OS__baseline.json"))
    opt = L.base_arch("OS").with_design(**rec["design"])
    wash = rec["design"].get("ma.timing.post_sample_wash", ps.values["ma.timing.post_sample_wash"])
    rows = ["| Variant | LOD nominal (pg/mL) | LOD median [5-95 %] | P(LOD<=1) | P(success) | time to result (min) | "
            "constraints |", "|---|---|---|---|---|---|---|"]
    for t_inc, acc in [(30, 10), (30, 7.5), (25, 10), (35, 5)]:
        a = opt.with_design(**{"ma.timing.in_vial_incubation": t_inc, "hw.timing.accumulation_time": acc,
                               "hw.smfl.loop_flush_volumes_for_transfer": 6.6,
                               "ma.timing.post_sample_wash": wash + 2.0})
        a = replace(a, detector=F.DEFAULT_DETECTOR)
        p = F.chamber_ps_fn("review")(ps)
        why = L.constraint_violations(a, p)
        s = L.mc(a, p, n=L.N_FINAL, lod_scale=1.0 / TRANSFER)
        rows.append(f"| chamber, incubation {t_inc} min, accumulation {acc} min | {fmt(s['lod_nominal'])} | "
                    f"{fmt(s['lod_median'])} [{fmt(s['lod_p05'])}-{fmt(s['lod_p95'])}] | "
                    f"~{s['p_lod_only']:.2f} | ~{s['p_success']:.2f} | {s['time_to_result_min']:.1f} | "
                    f"{'; '.join(why) or 'ok'} |")
        print(rows[-1], flush=True)
    txt = ("# One-step format with a timed in-line incubation chamber (approximation)\n\n"
           "Revised after the final review (docs/08 S9, S13): thin-layer cell (Stage-3 default), stirred-capture "
           "factor sampled on [0.2, 1.0]/2.2 (mode 0.45), 1/0.96 transfer factor applied to every draw before P. "
           "'~' = chamber approximation.\n\n" + "\n".join(rows) + "\n")
    (L.OUT / "inline_chamber.md").write_text(txt)


if __name__ == "__main__":
    main()
