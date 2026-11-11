#!/usr/bin/env python3
"""Final candidate designs of docs/05 section 4 under the decisive scenarios (one reproducible table).

Designs
  P-vial  : optimised one-step beads, beads + conjugate pre-filled in the SAMPLE vial (reference; needs a timed
            start of the in-vial incubation, docs/05 s.4.3)
  P-chamb : PRIMARY - same chemistry and trap, incubation in a timed, stirred in-line chamber
            (approximation documented in scripts/inline_chamber.py; LOD x 1/0.96 for the extra transfer)
  B-bed   : BACKUP - fixed packed micro-bed (0.5 uL, 50 um beads, 0.5 mm ID: column/particle ratio 10),
            sample loaded at 10 uL/min with 2 loop volumes, regenerated each cycle; no beads to handle
  S-chamb : sequential-labelling MODE of the primary hardware: beads dosed into the chamber, conjugate injected
            through the SM-FL onto the trapped beads (same chamber approximation)
  F-seq   : sequential-bead mode on the primary hardware (conjugate injected through the SM-FL instead of
            dosed into the chamber) - in-platform fallback; evaluated with beads pre-filled in the vial
Scenarios: see LIST below (values from params/model_assumptions.yaml or robustness.py definitions).

Usage: python scripts/final_designs.py [--n 2000]  -> results/design/final_designs.md, final_designs.csv
"""
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace

import design_lib as L
import robustness as R
from design_lib import fmt

CHAMBER_TRANSFER = 0.96


def designs(ps):
    os_rec = json.load(open(L.OUT / "optimum_OS__baseline.json"))["design"]
    sq_rec = json.load(open(L.OUT / "optimum_SQ__baseline.json"))["design"]
    fr_rec = json.load(open(L.OUT / "optimum_FRB__baseline.json"))["design"]
    os_opt = L.base_arch("OS").with_design(**os_rec)
    wash = os_rec.get("ma.timing.post_sample_wash", ps.values["ma.timing.post_sample_wash"])
    chamb = os_opt.with_design(**{"ma.timing.in_vial_incubation": 30, "hw.timing.accumulation_time": 10,
                                  "hw.smfl.loop_flush_volumes_for_transfer": 6.6,
                                  "ma.timing.post_sample_wash": wash + 2.0})
    bed = L.base_arch("FRB").with_design(**fr_rec).with_design(**{
        "ma.geometry.packed_bed_column_inner_diameter": 0.5, "hw.timing.sample_load_flow": 10,
        "hw.smfl.loop_flush_volumes_for_transfer": 2})
    seq = L.base_arch("SQ").with_design(**sq_rec)
    seq_ch = seq.with_design(**{"ma.timing.in_vial_incubation": 30, "hw.smfl.loop_flush_volumes_for_transfer": 6.6,
                                "ma.timing.post_sample_wash": 3.0})
    chamber_ps = lambda p: L.pin(p, **{"ma.capture.in_vial_unstirred_rate_factor": 0.45})
    return [("P-vial", os_opt, lambda p: p, 1.0),
            ("P-chamb", chamb, chamber_ps, 1.0 / CHAMBER_TRANSFER),
            ("B-bed", bed, lambda p: p, 1.0),
            ("F-seq", seq, lambda p: p, 1.0),
            ("S-chamb", seq_ch, chamber_ps, 1.0 / CHAMBER_TRANSFER)]


def scen(label):
    for s in R.SCENARIOS:
        if s[0].startswith(label):
            return s
    for s in R.LEVERS:
        if s[0].startswith(label):
            return (s[0], s[1], None)
    raise KeyError(label)


LIST = ["S0", "S2a", "S2b", "S1", "S3a", "S3b", "S4a", "S4b", "S5", "L6+L7", "L1+L3+L6+L7", "L4"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=L.N_FINAL)
    args = ap.parse_args()
    ps0 = L.load_ps()
    rows = []
    md = ["| Design | Scenario | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD<=1) | P(success) | "
          "ULOQ nominal | time to result (min) | constraint flags |", "|---|---|---|---|---|---|---|---|---|"]
    for dkey, arch, pmod, f in designs(ps0):
        for lab in LIST:
            name, fn, inj = scen(lab)
            a = replace(arch, injection=inj, name=arch.name + "/" + inj) if inj else arch
            ps = pmod(fn(ps0))
            why = L.constraint_violations(a, ps)
            s = L.mc(a, ps, n=args.n)
            approx = "~" if f != 1.0 else ""
            md.append(f"| {dkey} | {name[:80]} | {fmt(s['lod_nominal'] * f)} | {fmt(s['lod_median'] * f)} "
                      f"[{fmt(s['lod_p05'] * f)}-{fmt(s['lod_p95'] * f)}] | {approx}{s['p_lod_only']:.2f} | "
                      f"{approx}{s['p_success']:.2f} | {fmt(s['uloq_nominal'])} | {s['time_to_result_min']:.1f} | "
                      f"{'; '.join(why) or 'ok'} |")
            rows.append(dict(design=dkey, scenario=lab, lod_nominal=s["lod_nominal"] * f,
                             lod_median=s["lod_median"] * f, lod_p05=s["lod_p05"] * f, lod_p95=s["lod_p95"] * f,
                             p_lod=s["p_lod_only"], p_success=s["p_success"], uloq=s["uloq_nominal"],
                             time=s["time_to_result_min"], flags="; ".join(why)))
            print(md[-1], flush=True)
    txt = ("# Final candidate designs under the decisive scenarios\n\n"
           f"n = {args.n}, seed {L.SEED}. '~': chamber approximation (P computed before the 1/0.96 transfer "
           "factor, so slightly optimistic).\n\n" + "\n".join(md) + "\n")
    (L.OUT / "final_designs.md").write_text(txt)
    with open(L.OUT / "final_designs.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        for r in rows:
            w.writerow({k: (fmt(v, 4) if isinstance(v, float) else v) for k, v in r.items()})


if __name__ == "__main__":
    main()
