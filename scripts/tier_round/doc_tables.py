#!/usr/bin/env python3
"""Print the result tables of docs/30 from results/tier_round/tiers.json, in the layout docs/30 uses.

  python scripts/tier_round/doc_tables.py            # all tables
  python scripts/tier_round/doc_tables.py --check    # compare with the tables now in docs/30; exit 1 on a difference

The tables of docs/30 sections 0, 3.5, 4.5, 5.4 and 6.2 are pasted from this output, so that no number in them is
typed by hand.  Numbers are rounded to two significant figures.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
J = json.loads((ROOT / "results" / "tier_round" / "tiers.json").read_text())

T1 = "Tier 1: capture on a printed gold strip, read at the electrode under fast substrate flow"
T2 = "Tier 2: capillary micro-bed above a printed carbon strip, stop and sweep"
T3V = "Tier 3: the capture bed in the loop of one valve"
T3T = "Tier 3 with the immune-complex transfer to a second bed"
PRIM = "1. The three implementations, as specified"
SC = "2. Scenarios - "
A1, A2, A3 = "3. Tier 1 - alternatives and hardware cases", "4. Tier 2 - alternatives and hardware cases", \
    "5. Tier 3 - alternatives"
L67 = "detection reagent and substrate lot pass screening (L6 + L7)"
L367 = "L3 + L6 + L7"
S1 = "non-specific binding x25 (S1)"
ND = "no decay in the reservoir: background 1e-5 of the substrate at the time of use"
ND67 = "no decay and screened reagents (L6 + L7)"
S4 = "background 1e-3 of the substrate, no decay (S4a)"
CONT = "blank contamination up to 1 pg/mL"
P01 = "only 1 % of the turnovers give an electroactive product (review C1)"
P01ND = "only 1 % of the turnovers electroactive, and no decay in the reservoir"
P001 = "only 0.1 % of the turnovers give an electroactive product"

NAMES = {   # parameter key -> wording of docs/30 section 6.2
    "chem.antibodies.koff_detection": "detection off-rate 8.6×10⁻⁴ s⁻¹ [3×10⁻⁶–8.3×10⁻³]",
    "chem.nsb.nsb_effective_rate_constant": "non-specific rate 4×10⁻¹¹ m/s [0.8–40×10⁻¹¹]",
    "ma.nsb.label_factor_igg_enzyme_conjugate": "label factor of the conjugate 0.04 [0.01–0.15]",
    "chem.antibodies.kon_detection": "detection on-rate 3.9×10⁵ M⁻¹s⁻¹ [0.9–12×10⁵]",
    "chem.enzymes.alp.kcat_conjugate_assay_conditions": "enzyme turnover 1000 s⁻¹ [100–6000]",
    "tr.nsb.surface_factor_gold_oeg": "surface factor of the coated gold 3 [1–30]",
    "tr.detection.monolayer_collection_efficiency": "current through the coated gold 1 [0.1–1]",
    "ma.nsb.surface_factor_tubing": "surface factor of tubing and walls 3 [1–30]",
    "ma.nsb.surface_factor_packed_bed": "surface factor of the bed 3 [1–30]",
    "tr.nsb.surface_factor_frit": "surface factor of the frit 10 [1–100]",
    "chem.surfaces.igg_surface_density_monolayer": "capture site density 1×10¹⁶ m⁻² [0.2–1.5×10¹⁶]",
    "tr.transfer.elution_efficiency": "released fraction in the transfer 0.35 [0.05–0.74]",
    "ma.design_levers.immune_complex_transfer_nsb_factor":
        "non-specific label that comes along in the transfer 0.1 [0.01–0.5]",
    "ma.labelling.detection_on_capture_residual_factor": "conjugate binding to the capture antibody 1 [1–3]",
    "tr.nsb.unit_to_unit_cv_planar": "unit-to-unit CV, hand-coated electrodes 0.15 [0.05–0.4]",
    "tr.nsb.unit_to_unit_cv_bed": "unit-to-unit CV, hand-packed beds 0.10 [0.03–0.3]",
    "ma.delivery.adsorptive_loss_fraction_with_carrier": "analyte lost to walls 0.2 [0.02–0.6]",
    "chem.antibodies.kon_capture": "capture on-rate 3×10⁵ M⁻¹s⁻¹ [0.9–12×10⁵]",
    "ma.chemistries.alp_hqdp.hydrolysis_rate": "hydrolysis of the substrate 10⁻¹⁰ s⁻¹ [10⁻¹²–10⁻⁸]",
    "ma.chemistries.alp_hqdp.product_half_life": "half-life of hydroquinone 600 s [120–7200]",
    "tr.noise.preread_residual_cv": "residual of the pre-run subtraction 0.03 [0.01–0.10]",
}
N_TOP = 8        # a parameter enters the table if it is among the N_TOP largest swings of any design


def f2(x):
    """Two significant figures, plain decimal (0.62, 2.0, 35, 560, 52000)."""
    v = float(f"{float(x):.2g}")
    if v >= 10:
        return f"{v:.0f}"
    if v >= 1:
        return f"{v:.1f}"
    if v >= 0.1:
        return f"{v:.2f}"
    return f"{v:.2g}"


def med(k):
    return f"{f2(k['lod_median'])} [{f2(k['lod_p05'])}–{f2(k['lod_p95'])}]"


def pp(k):
    return f"{k['p_lod_le_target']:.2f} / {k['p_lod_le_10']:.2f}"


def r4(label, k):
    return f"| {label} | {f2(k['lod_nominal'])} | {med(k)} | {pp(k)} |"


def tables():
    out = {}
    P = J[PRIM]
    prim = [P[T1], P[T2], P[T3V], P[T3T]]
    sc = [J[SC + t] for t in (T1, T2, T3V, T3T)]
    a1, a2, a3 = J[A1], J[A2], J[A3]
    g = lambda d, start: next(v for k, v in d.items() if k.startswith(start))

    def four(fn):
        return " | ".join(fn(x) for x in prim)

    out["summary"] = "\n".join([
        "| Injection to result (min) | " + four(lambda k: f"{k['time_to_result_min']:.1f}") + " |",
        "| LOD nominal (pg/mL) | " + four(lambda k: f"**{f2(k['lod_nominal'])}**") + " |",
        "| LOD median [5–95 %] | " + four(med) + " |",
        "| P(LOD ≤ 1 pg/mL) / P(≤ 10) | " + four(pp) + " |",
        "| Detection reagent and substrate lot screened (L6 + L7): nominal; median | "
        + " | ".join(f"{f2(s[L67]['lod_nominal'])}; {med(s[L67])}" for s in sc) + " |",
        "| If the substrate's background does not decay (10⁻⁵ at the time of use): nominal; median | "
        + " | ".join(f"{f2(s[ND]['lod_nominal'])}; {med(s[ND])}" for s in sc) + " |",
    ])

    s1 = sc[0]
    out["tier1"] = "\n".join([
        "| Case | Nominal | Median [5–95 %] | P(≤ 1) / P(≤ 10) |", "|---|---|---|---|",
        r4("as specified", s1["as specified"]),
        r4("detection reagent and substrate lot screened (L6 + L7)", s1[L67]),
        r4("the same with the credit for the F(ab′)₂ conjugate (L3)", s1[L367]),
        r4("conjugate binds non-specifically 25× more (S1)", s1[S1]),
        r4("the substrate's background does not decay: 10⁻⁵ of the substrate at the time of use", s1[ND]),
        r4("the same with screened reagents (L6 + L7)", s1[ND67]),
        r4("background 10⁻³ of the substrate, no decay (S4a)", s1[S4]),
        r4("**printed carbon ED-S1PE-C21, adsorbed streptavidin, 10 nM conjugate**", g(a1, "printed carbon C21 with adsorbed")),
        r4("printed carbon, background does not decay", g(a1, "printed carbon C21, no decay")),
        r4("thin-film gold chip SE1 in the thin-film cell", g(a1, "thin-film gold chip SE1")),
        r4("strip-cell gap 0.10 mm", g(a1, "strip-cell gap 0.10")),
        r4("strip-cell gap 0.50 mm", g(a1, "strip-cell gap 0.50")),
        r4("read at 300 µL/min", g(a1, "read at 300")),
        r4("read at 80 µL/min", g(a1, "read at 80")),
        r4("read at 40 µL/min", g(a1, "read at 40")),
        r4("read 120 s at 150 µL/min, 10 nM conjugate (operating point of Revision B)", g(a1, "read 120 s at 150")),
        r4("conjugate 10 nM", g(a1, "conjugate 10 nM")),
        r4("conjugate 40 nM", g(a1, "conjugate 40 nM")),
        r4("substrate 0.1 mM", g(a1, "substrate 0.1 mM")),
        r4("substrate 1 mM", g(a1, "substrate 1 mM")),
        r4("substrate 1 mM, background does not decay", g(a1, "substrate 1 mM, no decay")),
        r4("reference windows in wash buffer pH 7.5, background step of 100 pA", g(a1, "reference windows in wash buffer pH 7.5: background step of 100")),
        r4("reference windows in wash buffer pH 7.5, background step of 300 pA", g(a1, "reference windows in wash buffer pH 7.5: background step of 300")),
        r4("coated gold delivers 30 % of the transport-limited current", g(a1, "coated gold delivers 30")),
        r4("no pre-run read on the strip", g(a1, "no pre-read on the electrode")),
        r4("no pre-run read, background does not decay", g(a1, "no pre-read on the electrode, no decay")),
        r4("read in the stopped cell (needs a zero-flow row)", g(a1, "stopped read")),
        r4("stop-and-go loading, 13 portions held 190 s (needs a zero-flow row)", g(a1, "stop-and-go loading")),
        r4("transfer line 0.127 mm × 20 cm", g(a1, "transfer line 0.127")),
        r4("detection conjugate with 5 [2–10] enzymes per antibody (UNVERIFIED reagent)", g(a1, "detection conjugate with 5")),
    ])

    s2 = sc[1]
    out["tier2"] = "\n".join([
        "| Case | Nominal | Median [5–95 %] | P(≤ 1) / P(≤ 10) |", "|---|---|---|---|",
        r4("as specified", s2["as specified"]),
        r4("screened detection reagent and substrate lot (L6 + L7)", s2[L67]),
        r4("the same with the credit for the F(ab′)₂ conjugate (L3)", s2[L367]),
        r4("conjugate binds 25× more (S1)", s2[S1]),
        r4("the substrate's background does not decay (10⁻⁵ at the time of use)", s2[ND]),
        r4("background 10⁻³ of the substrate, no decay (S4a)", s2[S4]),
        r4("no conjugate-coated wall above the bed (bound: what a valve gives)", g(a2, "no conjugate-exposed")),
        r4("walls above the bed bind like blocked beads (factor 1; a coated capillary)", g(a2, "walls above the bed bind")),
        r4("transfer line 0.025 mm × 15 cm", g(a2, "transfer line 0.025")),
        r4("transfer line 0.127 mm × 20 cm", g(a2, "transfer line 0.127")),
        r4("bed in a fitting on the port (whole bore between bed and electrode)", g(a2, "bed in a fitting")),
        r4("frit 1 mm²", g(a2, "retainer wetted area 1 mm2")),
        r4("frit 20 mm²", g(a2, "retainer wetted area 20 mm2")),
        r4("beads behave as when washed in tubes (factor 1)", g(a2, "bed binds conjugate like beads")),
        r4("half the beads", g(a2, "half the beads")),
        r4("twice the beads", g(a2, "twice the beads")),
        r4("conjugate 10 nM", g(a2, "conjugate 10 nM")),
        r4("conjugate 3 nM", g(a2, "conjugate 3 nM")),
        r4("stop 7 min instead of 5 (load 35 min)", g(a2, "stop 7 min instead of 5")),
        r4("stop 3 min instead of 5 (load 39 min)", g(a2, "stop 3 min instead of 5")),
        r4("stop 30 s", g(a2, "stop 30 s")),
        r4("conjugate 3 nM and stop 3 min (lowest nominal)", g(a2, "conjugate 3 nM, stop 3 min")),
        r4("the same if only 1 % of the turnovers give an electroactive product", g(a2, "the same, only 1 %")),
        r4("parked read", g(a2, "parked read")),
        r4("**pump cannot stop: continuous read at 1 µL/min**", g(a2, "pump cannot stop: continuous")),
        r4("pump cannot stop and cannot go below 10 µL/min", g(a2, "pump cannot stop and cannot")),
        r4("strip-cell gap 0.10 mm", g(a2, "strip-cell gap 0.10")),
        r4("strip-cell gap 0.50 mm", g(a2, "strip-cell gap 0.50")),
    ])

    s3, s4 = sc[2], sc[3]
    out["tier3"] = "\n".join([
        "| Case | Nominal | Median [5–95 %] | P(≤ 1) / P(≤ 10) |", "|---|---|---|---|",
        r4("**one valve, as specified**", s3["as specified"]),
        r4("one valve, screened detection reagent and substrate lot (L6 + L7)", s3[L67]),
        r4("one valve, the same with the credit for the F(ab′)₂ conjugate (L3)", s3[L367]),
        r4("one valve, with a reference channel as well (L5)", s3["with a reference channel as well (L5)"]),
        r4("one valve, conjugate binds 25× more (S1)", s3[S1]),
        r4("one valve, the substrate's background does not decay", s3[ND]),
        r4("one valve, background 10⁻³ of the substrate, no decay (S4a)", s3[S4]),
        r4("one valve, accumulation 7 min instead of 3 (load 36 min)", g(a3, "one valve, accumulation 7 min")),
        r4("one valve, conjugate 10 nM", g(a3, "one valve, conjugate 10 nM")),
        r4("one valve, conjugate 3 nM", g(a3, "one valve, conjugate 3 nM")),
        r4("one valve, loop walls 30 mm² instead of 10 mm²", g(a3, "one valve, loop walls 30")),
        r4("**transfer as specified (release 0.35 [0.05–0.74], non-specific ×0.1)**", s4["as specified"]),
        r4("transfer, release 0.7 in 5 min (the value docs/05 assumed for its tube protocol)", g(a3, "transfer: release 0.7 in 5 min")),
        r4("transfer at its optimistic bounds (release 0.74, ×0.01)", g(a3, "transfer: release 0.74")),
        r4("transfer at its pessimistic bounds (release 0.05, ×0.5)", g(a3, "transfer: release 0.05")),
        r4("transfer by desthiobiotin and biotin, 5 min", g(a3, "transfer with desthiobiotin")),
        r4("transfer, release 0.7, read bed no larger than the capture bed (sites per antibody 1.2)", g(a3, "transfer, release 0.7, read bed the same size")),
        r4("the same, capture bed coated at the vendor's capacity (sites per antibody 0.36)", g(a3, "transfer, release 0.7, same size")),
        r4("transfer, screened detection reagent and substrate lot (L6 + L7)", s4[L67]),
        r4("transfer, release 0.7, screened reagents (L6 + L7)", g(a3, "transfer, release 0.7, screened")),
        r4("transfer, screened reagents and the credit for the F(ab′)₂ conjugate (L3 + L6 + L7)", s4[L367]),
        r4("transfer, the substrate's background does not decay", s4[ND]),
        r4("transfer, conjugate binds 25× more (S1)", s4[S1]),
    ])

    sens = J["sensitivity"]
    labs = (T1, T2, T3V, T3T)
    keys = []
    for lab in labs:
        for r in sens[lab][:N_TOP]:
            if r["key"] not in keys:
                keys.append(r["key"])
    look = {lab: {r["key"]: r for r in sens[lab]} for lab in labs}
    lines = ["| Parameter, value [low–high] | Tier 1: LOD at low / high | Tier 2 | Tier 3, one valve | "
             "Tier 3 with transfer |", "|---|---|---|---|---|"]
    for k in keys:
        cells = []
        for lab in labs:
            r = look[lab].get(k)
            cells.append("—" if r is None else f"{f2(r['lod_low'])} / {f2(r['lod_high'])}")
        lines.append(f"| {NAMES.get(k, k)} | " + " | ".join(cells) + " |")
    out["sensitivity"] = "\n".join(lines)

    def trio(key):
        return ", ".join(f"{f2(s[key]['lod_nominal'])}" for s in sc)
    out["scenario_p01"] = (f"1 % of the turnovers: {trio(P01)} pg/mL; 1 % and a background that does not decay: "
                           f"{trio(P01ND)}; 0.1 %: {trio(P001)}")
    out["scenario_s1_s4"] = f"S1: {trio(S1)}; S4a: {trio(S4)}"
    out["scenario_cont"] = "contamination: " + "; ".join(f"{f2(s[CONT]['lod_nominal'])}, {med(s[CONT])}, P {pp(s[CONT])}" for s in sc)
    return out


CHECKED = ("summary", "tier1", "tier2", "tier3", "sensitivity")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    t = tables()
    if "--check" in argv:
        doc = (ROOT / "docs" / "30_tier_designs.md").read_text()
        bad = 0
        for name in CHECKED:
            for line in t[name].splitlines():
                if line not in doc:
                    bad += 1
                    print(f"[{name}] not in docs/30: {line}")
        print("docs/30 tables agree with tiers.json" if not bad else f"{bad} line(s) differ")
        return 1 if bad else 0
    for name, text in t.items():
        print(f"\n### {name}\n\n{text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
