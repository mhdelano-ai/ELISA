#!/usr/bin/env python3
"""Robustness of the optimised designs under the open scenarios, and parameter-scenario runs of the levers
that existing parameters can represent (Task 4, docs/05 sections 2 and 3).

Reads results/design/optimum_<FMT>__baseline.json (written by optimise_designs.py) and evaluates every
design under every scenario with n = 2000 Monte Carlo draws (seed 20261111).

Scenario values are NOT tuned toward the target: each one is either a bound already in the YAML files, the
pre-audit assumption, or a stated bounded estimate for a lever that the model cannot represent physically
(labelled OUTSIDE MODEL in the output and in docs/05).

Usage: python scripts/robustness.py [--n 2000] [--formats OS SQ FRB FRC]
Outputs: results/design/robustness.md, results/design/robustness.csv,
         results/design/levers.md, results/design/levers.csv
"""
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace

import design_lib as L
from design_lib import fmt


def load_opt(key, scen="baseline"):
    rec = json.load(open(L.OUT / f"optimum_{key}__{scen}.json"))
    return L.base_arch(key).with_design(**rec["design"]), rec


def scale_param(ps, key, factor):
    """Scale value and bounds of a sampled parameter (scenario: a lever that multiplies it)."""
    p = ps.params[key]
    return L.with_bounds(ps, key, value=p.value * factor, low=p.low * factor, high=p.high * factor)


def lv(ps, name):
    """Bounded-estimate lever values from params/model_assumptions.yaml (section design_levers)."""
    return float(ps.params[f"ma.design_levers.{name}"].value)


# ---- open scenarios (docs/04 section 6 + this task) --------------------------------------------------
SCENARIOS = [
    ("S0 audited baseline", lambda ps: ps, None),
    ("S1 old NSB rate (label factor 1.0, 0.3-3; x25)", lambda ps: L.with_bounds(
        ps, "ma.nsb.label_factor_igg_enzyme_conjugate", value=1.0, low=0.3, high=3.0), None),
    ("S2a detection reagent screened (koff 1e-4, <=1.9e-4 /s)", lambda ps: L.with_bounds(
        ps, "chem.antibodies.koff_detection", value=1.0e-4, low=3.0e-6, high=1.9e-4), None),
    ("S2b capture reagent unscreened (koff to 8.3e-3 /s)", lambda ps: L.with_bounds(
        ps, "chem.antibodies.koff_capture", high=8.3e-3), None),
    ("S3a NSB partly reversible, fraction removed by washes = ma.design_levers.nsb_fraction_removed_by_wash "
     "(OUTSIDE MODEL: label factor x(1-f))",
     lambda ps: scale_param(ps, "ma.nsb.label_factor_igg_enzyme_conjugate",
                            1.0 - lv(ps, "nsb_fraction_removed_by_wash")), None),
    ("S3b NSB irreversible and surfaces at high bound (tubing factor 30)",
     lambda ps: L.pin(ps, **{"ma.nsb.surface_factor_tubing": 30.0}), None),
    ("S4a free HQ in substrate 1e-3 (high bound)",
     lambda ps: L.pin(ps, **{"ma.chemistries.alp_hqdp.free_product_impurity": 1e-3}), None),
    ("S4b free HQ in substrate 1e-7 (low bound)",
     lambda ps: L.pin(ps, **{"ma.chemistries.alp_hqdp.free_product_impurity": 1e-7}), None),
    ("S5 <=100 uL DRAWN: PLNO 75 uL on the 100 uL loop", lambda ps: ps, "PLNO_100"),
    ("S6 worst plausible: S1 + S4a", lambda ps: L.pin(L.with_bounds(
        ps, "ma.nsb.label_factor_igg_enzyme_conjugate", value=1.0, low=0.3, high=3.0),
        **{"ma.chemistries.alp_hqdp.free_product_impurity": 1e-3}), None),
    ("S7 favourable: S2a + S4b", lambda ps: L.pin(L.with_bounds(
        ps, "chem.antibodies.koff_detection", value=1.0e-4, low=3.0e-6, high=1.9e-4),
        **{"ma.chemistries.alp_hqdp.free_product_impurity": 1e-7}), None),
]

# ---- levers representable by existing parameters (docs/05 section 2) ---------------------------------
LEVERS = [
    ("L0 none (optimised design)", lambda ps: ps),
    ("L1 inert/coated wetted path: tubing + trap-wall surface factor at its low bound (1)",
     lambda ps: L.pin(ps, **{"ma.nsb.surface_factor_tubing": 1.0})),
    ("L2 clean-zone re-trap: wall NSB term removed (tubing factor 0.01) [OUTSIDE MODEL as physics]",
     lambda ps: L.pin(ps, **{"ma.nsb.surface_factor_tubing": 0.01})),
    ("L3 Fab'-ALP conjugate: label NSB x fab_conjugate_nsb_factor (0.5) [OUTSIDE MODEL, bounded estimate]",
     lambda ps: scale_param(ps, "ma.nsb.label_factor_igg_enzyme_conjugate", lv(ps, "fab_conjugate_nsb_factor"))),
    ("L4 immune-complex transfer: NSB x0.1 / signal x0.7 => label factor x0.14 [OUTSIDE MODEL]",
     lambda ps: scale_param(ps, "ma.nsb.label_factor_igg_enzyme_conjugate",
                            lv(ps, "immune_complex_transfer_nsb_factor") / lv(ps, "immune_complex_transfer_efficiency"))),
    ("L5 reference-channel subtraction, rho = 0.8: CV_NSB x sqrt(2(1-rho)) = 0.63 [OUTSIDE MODEL]",
     lambda ps: scale_param(ps, "chem.nsb.blank_CV_analog_electrochemical",
                            (2 * (1 - lv(ps, "nsb_reference_channel_correlation"))) ** 0.5)),
    ("L6 detection reagent screened (t1/2 >= 1 h)", lambda ps: L.with_bounds(
        ps, "chem.antibodies.koff_detection", value=1.0e-4, low=3.0e-6, high=1.9e-4)),
    ("L7 substrate purified: free HQ pinned at 1e-6", lambda ps: L.pin(
        ps, **{"ma.chemistries.alp_hqdp.free_product_impurity": 1e-6})),
    ("L8 bench-measured NSB at the plate anchor low end (label factor 0.029)",
     lambda ps: L.with_bounds(ps, "ma.nsb.label_factor_igg_enzyme_conjugate", value=0.029, low=0.01, high=0.06)),
    ("L6+L7 (reagent + substrate screening)", lambda ps: L.pin(L.with_bounds(
        ps, "chem.antibodies.koff_detection", value=1.0e-4, low=3.0e-6, high=1.9e-4),
        **{"ma.chemistries.alp_hqdp.free_product_impurity": 1e-6})),
    ("L1+L6+L7", lambda ps: L.pin(L.with_bounds(
        ps, "chem.antibodies.koff_detection", value=1.0e-4, low=3.0e-6, high=1.9e-4),
        **{"ma.chemistries.alp_hqdp.free_product_impurity": 1e-6, "ma.nsb.surface_factor_tubing": 1.0})),
    ("L1+L3+L6+L7", lambda ps: scale_param(L.pin(L.with_bounds(
        ps, "chem.antibodies.koff_detection", value=1.0e-4, low=3.0e-6, high=1.9e-4),
        **{"ma.chemistries.alp_hqdp.free_product_impurity": 1e-6, "ma.nsb.surface_factor_tubing": 1.0}),
        "ma.nsb.label_factor_igg_enzyme_conjugate", lv(ps, "fab_conjugate_nsb_factor"))),
]


def run_table(designs, entries, ps0, n, out_md, out_csv, title, arch_mod=True):
    rows = []
    with open(out_md, "w") as fh:
        fh.write(f"## {title}\n\nn = {n} Monte Carlo draws, seed {L.SEED}. Success = LOD <= 1 pg/mL and ULOQ >= 1000 "
                 "pg/mL.\n\n| Design | Scenario | LOD nominal | LOD median [5-95 %] | P(LOD<=1) | P(success) | "
                 "time to result (min) |\n|---|---|---|---|---|---|---|\n")
        for dkey, arch in designs:
            for ent in entries:
                label, fn = ent[0], ent[1]
                inj = ent[2] if len(ent) > 2 else None
                a = replace(arch, injection=inj, name=arch.name + "/" + inj) if inj else arch
                ps = fn(ps0)
                why = [w for w in L.constraint_violations(a, ps) if "ULOQ" not in w]
                s = L.mc(a, ps, n=n)
                flag = (" (violates: " + "; ".join(why) + ")") if why else ""
                fh.write(f"| {dkey} | {label}{flag} | {fmt(s['lod_nominal'])} | {fmt(s['lod_median'])} "
                         f"[{fmt(s['lod_p05'])}-{fmt(s['lod_p95'])}] | {s['p_lod_only']:.2f} | {s['p_success']:.2f} | "
                         f"{s['time_to_result_min']:.1f} |\n")
                rows.append(dict(design=dkey, scenario=label, lod_nominal=s["lod_nominal"], lod_median=s["lod_median"],
                                 lod_p05=s["lod_p05"], lod_p95=s["lod_p95"], p_lod=s["p_lod_only"],
                                 p_success=s["p_success"], uloq_nominal=s["uloq_nominal"],
                                 time_to_result=s["time_to_result_min"], violations="; ".join(why)))
                print(f"{dkey:10s} {label[:60]:60s} nom {fmt(s['lod_nominal'])} med {fmt(s['lod_median'])} "
                      f"P {s['p_lod_only']:.2f} Ps {s['p_success']:.2f}{flag}", flush=True)
    with open(out_csv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        for r in rows:
            w.writerow({k: (fmt(v, 4) if isinstance(v, float) else v) for k, v in r.items()})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=L.N_FINAL)
    ap.add_argument("--formats", nargs="*", default=["OS", "SQ", "FRB", "FRC"])
    ap.add_argument("--part", choices=["both", "scenarios", "levers"], default="both")
    args = ap.parse_args()
    ps0 = L.load_ps()
    designs = [("OS-base", L.base_arch("OS"))]
    for k in args.formats:
        designs.append((f"{k}-opt", load_opt(k)[0]))
    if args.part in ("both", "scenarios"):
        run_table(designs, SCENARIOS, ps0, args.n, L.OUT / "robustness.md", L.OUT / "robustness.csv",
                  "Robustness of the optimised designs under the open scenarios")
    if args.part in ("both", "levers"):
        run_table([d for d in designs if d[0] != "OS-base"], LEVERS, ps0, args.n, L.OUT / "levers.md",
                  L.OUT / "levers.csv", "Levers represented by existing parameters (scenario runs)")


if __name__ == "__main__":
    main()
