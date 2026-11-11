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

Revised after the final review (docs/08, findings S9 and S13); the pre-review version is reproduced exactly by
``designs(ps, variant="docs05")`` with ``convention="docs05"`` (see ``summarise``):
  * detector: the Stage-3 default is now a commercial single-channel thin-layer cell (``thin_layer``); the flow
    IDA with a second potentiostat channel is an option bought only if Stage-2 data show that electrochemical
    noise is a material part of the blank SD (S9). Designs were optimised with the IDA and are not re-optimised.
  * chamber designs: the stirred-capture factor is SAMPLED, log-triangular on [0.2, 1.0]/2.2 with mode 0.45
    (was pinned at 0.45 = well mixed / 2.2 dilution; mixing by a 50 uL aspirate/dispense every 2 min is not
    "well mixed"), and the 1/0.96 transfer factor is applied to every draw BEFORE P is computed (S13).
  * the SIA module doses beads and conjugate from SEPARATE reservoirs (B4); in the model this changes nothing
    (the in-cup exposure is the same), the shared-reservoir pre-exposure is quantified in shared_reservoir_cost.py.

Usage: python scripts/final_designs.py [--n 2000]  -> results/design/final_designs.md, final_designs.csv
       python scripts/final_designs.py --variant docs05 --out-suffix _docs05   (pre-review reproduction)
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
DEFAULT_DETECTOR = "thin_layer"           # Stage-3 default after the final review (docs/08 S9)
CHAMBER_STIR = dict(value=0.45, low=0.2 / 2.2, high=1.0 / 2.2)   # ma.capture.in_vial_unstirred_rate_factor (S13)
VARIANTS = ("review", "review_ida", "docs05")


def chamber_ps_fn(variant: str):
    """Parameter modifier of the chamber designs (approximation documented in scripts/inline_chamber.py)."""
    key = "ma.capture.in_vial_unstirred_rate_factor"
    if variant == "docs05":
        return lambda p: L.pin(p, **{key: 0.45})
    return lambda p: L.with_bounds(p, key, **CHAMBER_STIR)


def designs(ps, variant: str = "review"):
    """[(key, architecture, parameter modifier, LOD scale)] of the final designs.

    variant 'review'     : thin-layer detector, sampled stirring factor (default after the final review);
    variant 'review_ida' : as 'review' but with the flow IDA (the optional Stage-3 upgrade, S9);
    variant 'docs05'     : the designs exactly as docs/05 evaluated them (IDA, stirring factor pinned at 0.45).
    LOD scale: apply with design_lib.mc(..., lod_scale=f) (per draw, before P) - except when reproducing docs/05,
    which multiplied the summary LODs after P had been computed (summarise(..., convention='docs05'))."""
    if variant not in VARIANTS:
        raise ValueError(f"variant must be one of {VARIANTS}")
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
    chamber_ps = chamber_ps_fn(variant)
    out = [("P-vial", os_opt, lambda p: p, 1.0),
           ("P-chamb", chamb, chamber_ps, 1.0 / CHAMBER_TRANSFER),
           ("B-bed", bed, lambda p: p, 1.0),
           ("F-seq", seq, lambda p: p, 1.0),
           ("S-chamb", seq_ch, chamber_ps, 1.0 / CHAMBER_TRANSFER)]
    if variant == "review":
        out = [(k, replace(a, detector=DEFAULT_DETECTOR), pm, f) for k, a, pm, f in out]
    return out


def summarise(arch, ps, f, n, convention: str = "review") -> dict:
    """Monte Carlo summary of one design entry. convention 'review': LOD scale applied per draw before P (S13);
    'docs05': P computed on the unscaled LOD and the reported LODs multiplied afterwards (as docs/05 did)."""
    if convention == "docs05":
        s = L.mc(arch, ps, n=n)
        for k in ("lod_nominal", "lod_median", "lod_p05", "lod_p95"):
            s[k] = s[k] * f
        return s
    return L.mc(arch, ps, n=n, lod_scale=f)


# 1 pg/mL of a 150 kDa IgG = 1e-12 g/mL / 1.5e5 g/mol = 6.7e-15 M
CONTAMINATION_1PG_M = 1e-12 / 1.5e5 * 1e3
EXTRA = [("C1 human-IgG contamination of blanks up to 1 pg/mL-equivalent (6.7 fM; nominal 0) [docs/08 S5, scenario]",
          lambda ps: L.with_bounds(ps, "ma.nsb.blank_igg_contamination_equivalent", high=CONTAMINATION_1PG_M), None)]


def scen(label):
    for s in EXTRA:
        if s[0].startswith(label):
            return s
    for s in R.SCENARIOS:
        if s[0].startswith(label):
            return s
    for s in R.LEVERS:
        if s[0].startswith(label):
            return (s[0], s[1], None)
    raise KeyError(label)


LIST = ["S0", "S2a", "S2b", "S1", "S3a", "S3b", "S4a", "S4b", "S5", "C1", "L6+L7", "L1+L3+L6+L7", "L4"]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=L.N_FINAL)
    ap.add_argument("--variant", default="review", choices=VARIANTS)
    ap.add_argument("--out-suffix", default="", help="e.g. _docs05 -> final_designs_docs05.md")
    args = ap.parse_args(argv)
    conv = "docs05" if args.variant == "docs05" else "review"
    ps0 = L.load_ps()
    rows = []
    md = ["| Design | Scenario | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD<=1) | P(success) | "
          "ULOQ nominal | time to result (min) | constraint flags |", "|---|---|---|---|---|---|---|---|---|"]
    for dkey, arch, pmod, f in designs(ps0, args.variant):
        for lab in LIST:
            name, fn, inj = scen(lab)
            a = replace(arch, injection=inj, name=arch.name + "/" + inj) if inj else arch
            ps = pmod(fn(ps0))
            why = L.constraint_violations(a, ps)
            s = summarise(a, ps, f, args.n, conv)
            approx = "~" if f != 1.0 else ""
            md.append(f"| {dkey} | {name[:80]} | {fmt(s['lod_nominal'])} | {fmt(s['lod_median'])} "
                      f"[{fmt(s['lod_p05'])}-{fmt(s['lod_p95'])}] | {approx}{s['p_lod_only']:.2f} | "
                      f"{approx}{s['p_success']:.2f} | {fmt(s['uloq_nominal'])} | {s['time_to_result_min']:.1f} | "
                      f"{'; '.join(why) or 'ok'} |")
            rows.append(dict(design=dkey, scenario=lab, lod_nominal=s["lod_nominal"],
                             lod_median=s["lod_median"], lod_p05=s["lod_p05"], lod_p95=s["lod_p95"],
                             p_lod=s["p_lod_only"], p_success=s["p_success"], uloq=s["uloq_nominal"],
                             time=s["time_to_result_min"], flags="; ".join(why)))
            print(md[-1], flush=True)
    if conv == "docs05":
        head = ("n = {n}, seed {seed}. Variant docs05 (pre-review reproduction): flow IDA, stirring factor pinned at "
                "0.45. '~': chamber approximation (P computed before the 1/0.96 transfer factor, so slightly "
                "optimistic).")
    else:
        det = "flow IDA (optional Stage-3 upgrade)" if args.variant == "review_ida" else \
            "commercial single-channel thin-layer cell (Stage-3 default, docs/08 S9)"
        head = ("n = {n}, seed {seed}. Revised after the final review (docs/08). Detector: " + det + ". "
                "'~': chamber approximation; stirred-capture factor sampled on [0.2, 1.0]/2.2 (mode 0.45) and the "
                "1/0.96 transfer factor applied to every draw before P (S13). F-seq and P-vial put reagent in the "
                "sample vial (inadmissible, reference only).")
    txt = ("# Final candidate designs under the decisive scenarios\n\n" + head.format(n=args.n, seed=L.SEED)
           + "\n\n" + "\n".join(md) + "\n")
    (L.OUT / f"final_designs{args.out_suffix}.md").write_text(txt)
    with open(L.OUT / f"final_designs{args.out_suffix}.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        for r in rows:
            w.writerow({k: (fmt(v, 4) if isinstance(v, float) else v) for k, v in r.items()})


if __name__ == "__main__":
    main()
