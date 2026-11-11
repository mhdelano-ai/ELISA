#!/usr/bin/env python3
"""Run every architecture at nominal parameters and with Monte Carlo; write tables and figures to results/.

Usage:  python scripts/run_baseline.py [--n 1000] [--seed 20261111] [--no-figures]

Outputs (all small):
  results/baseline_results.csv       one row per architecture (nominal + MC summary + diagnostics)
  results/baseline_table.md          the condensed table used in docs/03
  results/skipped_architectures.csv  combinations rejected by architectures.check (with reasons)
  results/validation.csv             model vs published values
  results/sensitivity_<arch>.csv     one-at-a-time and global indices for the leading architectures
  results/reuse.csv                  reuse / regeneration projection
  results/fig_lod_intervals.png, fig_calibration.png, fig_blank_breakdown.png, fig_tornado.png
"""
from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from elisa_sim import architectures as A                      # noqa: E402
from elisa_sim import montecarlo, sensitivity, validation     # noqa: E402
from elisa_sim.model import evaluate                          # noqa: E402
from elisa_sim.params import ParameterSet                     # noqa: E402

RES = ROOT / "results"
TERMS = ["nsb_variability", "label_counting", "carryover", "substrate_background", "electrode_sensitivity",
         "electrochemical_noise", "baseline_drift", "contamination"]
# reference categorical palette (dataviz skill, light mode), fixed order
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"


def fmt(x, nd=3):
    if x is None:
        return ""
    if isinstance(x, (bool, np.bool_)):
        return str(bool(x))
    if isinstance(x, str):
        return x
    x = float(x)
    if np.isnan(x):
        return "n/a"
    if not np.isfinite(x) or x >= 1e29:      # 1e30 = sentinel for "LOD beyond the calibration grid"
        return "inf"
    return f"{x:.{nd}g}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=None)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--no-figures", action="store_true")
    args = ap.parse_args()
    RES.mkdir(exist_ok=True)
    ps = ParameterSet.load()
    archs, skipped = A.registry()
    target = ps.get("ma.statistics.lod_target", "pg/mL")
    tlim = ps.get("ma.statistics.time_limit", "min")
    top = ps.get("ma.statistics.range_top", "pg/mL")

    with open(RES / "skipped_architectures.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["architecture", "reason"])
        for name, why in skipped:
            w.writerow([name, "; ".join(why)])

    # NSB scenario: rate constant rescaled so that the plate-ELISA blank matches Rissin2010 (1 nM label)
    v_plate = validation.conventional_elisa_blank(
        ps, label_conc_M=ps.get("chem.antibodies.conc_detection_antibody_typical", "M"))
    ps_plate = ps.with_values({"chem.nsb.nsb_effective_rate_constant": v_plate["implied_k_nsb"]})

    rows, mcs = [], {}
    t0 = time.time()
    for i, a in enumerate(archs):
        mc = montecarlo.run(a, ps, n=args.n, seed=args.seed)
        mcs[a.name] = mc
        s = mc.summary(target, tlim, top)
        nom = mc.nominal
        d = nom.diagnostics
        lod_plate = float(evaluate(a, ps_plate).lod_pgml)
        row = dict(
            architecture=a.name, scheme=a.scheme, capture=a.capture, chemistry=a.chemistry, detector=a.detector,
            injection=a.injection, substrate_delivery=a.substrate_delivery, labelling_format=a.labelling_format,
            chemical_cycling=a.chemical_cycling, sample_treatment=a.sample_treatment,
            lod_nominal_pgml=s["lod_nominal"], lod_median_pgml=s["lod_median"], lod_p05_pgml=s["lod_p05"],
            lod_p95_pgml=s["lod_p95"], p_lod_le_1pgml=s["p_lod_le_target"],
            p_lod_and_range=s["p_lod_and_range"],
            lod_nominal_nsb_plate_calibrated_pgml=lod_plate,
            blank_equiv_nominal_pgml=d["blank_equivalent_pgml"], blank_equiv_median_pgml=s["blank_equiv_median"],
            uloq_nominal_pgml=nom.uloq_pgml, dynamic_range_decades_nominal=nom.dynamic_range_decades,
            cycle_time_min=s["cycle_time_min"], time_to_result_min=s["time_to_result_min"],
            meets_time=s["meets_time"], limiting_term_nominal=s["limiting_term_nominal"],
            limiting_term_mc=s["limiting_term_mc_mode"], limiting_term_mc_share=s["limiting_term_mc_share"],
            signal_at_1pgml_C=d["signal_at_1pg_C"], blank_sd_nominal_C=float(nom.blank_sd),
            blank_mean_nominal_C=float(nom.blank_mean),
            capture_fraction=d["capture_fraction_low"], label_fraction=float(np.squeeze(d["label_fraction_low"])),
            enzymes_per_pgml=d["enzymes_per_pg_per_mL"], nsb_enzymes=float(d["N_nsb"]),
            carry_enzymes=float(d["N_carry"]), cell_conversion=float(np.squeeze(d["cell_conversion"])),
            accumulation_volume_uL=float(d["accumulation_volume_uL"]),
            conjugate_peak_dilution=float(d["conjugate_peak_dilution"]),
            carryover_after_top_pgml=float(np.squeeze(d["carryover_after_top_pgml"])),
        )
        for k in TERMS:
            row[f"varfrac_nominal_{k}"] = float(nom.variance_fractions()[k])
        rows.append(row)
        print(f"[{i + 1:3d}/{len(archs)}] {a.name:42s} LOD nominal {fmt(s['lod_nominal']):>8s}  median "
              f"{fmt(s['lod_median']):>8s} [{fmt(s['lod_p05'])}, {fmt(s['lod_p95'])}] pg/mL  "
              f"P(<=1) {s['p_lod_le_target']:.3f}  {s['limiting_term_nominal']}  cycle {s['cycle_time_min']:.1f} "
              f"min  ({time.time() - t0:.0f} s)", flush=True)

    rows.sort(key=lambda r: r["lod_median_pgml"])
    keys = list(rows[0].keys())
    with open(RES / "baseline_results.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: fmt(v, 4) if not isinstance(v, str) else v for k, v in r.items()})

    # condensed markdown table
    with open(RES / "baseline_table.md", "w") as fh:
        fh.write("| Architecture | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD<=1) | "
                 "LOD, plate-calibrated NSB (pg/mL) | Blank equiv. B (pg/mL) | ULOQ (pg/mL) | Cycle / to result (min) "
                 "| Limiting term |\n|---|---|---|---|---|---|---|---|---|\n")
        for r in rows:
            fh.write(f"| {r['architecture']} | {fmt(r['lod_nominal_pgml'], 2)} | {fmt(r['lod_median_pgml'], 2)} "
                     f"[{fmt(r['lod_p05_pgml'], 2)}-{fmt(r['lod_p95_pgml'], 2)}] | {r['p_lod_le_1pgml']:.3f} | "
                     f"{fmt(r['lod_nominal_nsb_plate_calibrated_pgml'], 2)} | {fmt(r['blank_equiv_nominal_pgml'], 2)} | "
                     f"{fmt(r['uloq_nominal_pgml'], 2)} | {r['cycle_time_min']:.1f} / {r['time_to_result_min']:.1f} | "
                     f"{r['limiting_term_nominal']} |\n")

    # validation
    vals = validation.all_validations(ps)
    with open(RES / "validation.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["comparison", "model", "published", "unit", "model/published", "extra"])
        for v in vals:
            extra = "; ".join(f"{k}={fmt(x)}" for k, x in v.items()
                              if k not in ("name", "model", "published", "unit", "ratio"))
            w.writerow([v["name"], fmt(v["model"]), fmt(v["published"]), v["unit"], fmt(v["ratio"]), extra])
        for c in validation.task2_loop_table():
            w.writerow([f"Task 2 loop transfer: {c['case']}", " ".join(fmt(x) for x in c["model"]),
                        " ".join(fmt(x) for x in c["published"]), "fraction at 1/1.5/2/3 V_loop",
                        f"max |diff| {fmt(c['max_abs_diff'])}", ""])
    print("\nValidation:")
    for v in vals:
        print(f"  {v['name']:70s} model {fmt(v['model'])}  published {fmt(v['published'])}  ratio {fmt(v['ratio'])}")

    # sensitivity for the three architectures with the lowest median LOD, plus the Scheme B reference
    lead = [r["architecture"] for r in rows[:3]]
    if "B-bed-TL/alp_hqdp" not in lead:
        lead.append("B-bed-TL/alp_hqdp")
    sens_all = {}
    for name in lead:
        a = A.get(name)
        oat = sensitivity.one_at_a_time(a, ps)
        glob = {g["parameter"]: g for g in sensitivity.global_indices(mcs[name])}
        sens_all[name] = oat
        fn = RES / f"sensitivity_{name.replace('/', '__')}.csv"
        with open(fn, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["parameter", "unit", "low", "nominal", "high", "dlog10_LOD_at_low", "dlog10_LOD_at_high",
                        "spearman_vs_logLOD", "first_order_index"])
            for o in oat:
                g = glob.get(o["parameter"], {})
                w.writerow([o["parameter"], o["unit"], fmt(o["low"]), fmt(o["nominal"]), fmt(o["high"]),
                            fmt(o["dlog10_lod_at_low"]), fmt(o["dlog10_lod_at_high"]),
                            fmt(g.get("spearman")), fmt(g.get("first_order"))])
        print(f"\nSensitivity {name}: top OAT", [(o["parameter"], round(o["swing"], 2)) for o in oat[:6]])

    # reuse projection (nominal)
    tol = ps.get("ma.reuse.slope_drift_tolerance", "fraction")
    with open(RES / "reuse.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["architecture", "surface", "capacity_loss_per_cycle", "electrode_loss_per_cycle",
                    "cycles_to_slope_change_tolerance", "slope_after_100_cycles", "residual_label_per_cycle",
                    "carryover_after_top_standard_pgml", "lod_nominal_pgml"])
        for r in rows:
            d = mcs[r["architecture"]].nominal.diagnostics
            lc = float(np.squeeze(d["capacity_loss_per_cycle"]))
            le = float(np.squeeze(d["electrode_loss_per_cycle"]))
            per = (1 - lc) * (1 - le)
            cyc = np.log(1 - tol) / np.log(per) if per < 1 else np.inf
            w.writerow([r["architecture"], "renewed beads" if r["capture"] == "magnetic_beads" else "regenerated",
                        fmt(lc), fmt(le), fmt(cyc), fmt(per ** 100), fmt(float(np.squeeze(d["residual_label_per_cycle"]))),
                        fmt(r["carryover_after_top_pgml"]), fmt(r["lod_nominal_pgml"])])

    if not args.no_figures:
        figures(rows, mcs, sens_all, target, ps)
    print(f"\nWrote results to {RES} ({time.time() - t0:.0f} s)")


def _style(ax):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(INK2)
    ax.tick_params(colors=INK2, labelsize=8)
    ax.grid(True, color=GRID, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)


def figures(rows, mcs, sens_all, target, ps):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    scheme_color = {"A": PALETTE[0], "B": PALETTE[1], "C": PALETTE[2]}
    # 1. LOD intervals (all architectures)
    fig, ax = plt.subplots(figsize=(8.5, 0.16 * len(rows) + 1.2))
    y = np.arange(len(rows))[::-1]
    cap = 1e7
    for yi, r in zip(y, rows):
        lo, med, hi = (min(r["lod_p05_pgml"], cap), min(r["lod_median_pgml"], cap), min(r["lod_p95_pgml"], cap))
        c = scheme_color[r["scheme"]]
        ax.plot([lo, hi], [yi, yi], color=c, lw=2, solid_capstyle="round", zorder=3)
        ax.plot(med, yi, "o", ms=5, color=c, markeredgecolor="white", markeredgewidth=1, zorder=4)
    ax.axvline(target, color=INK, lw=1, ls="--", zorder=2)
    ax.text(target * 1.15, y[0] + 0.6, "target 1 pg/mL", fontsize=7, color=INK, va="bottom")
    ax.set_xscale("log")
    ax.set_yticks(y)
    ax.set_yticklabels([r["architecture"] for r in rows], fontsize=6, color=INK)
    ax.set_xlabel("LOD (pg/mL): Monte Carlo median and 5-95 % interval (capped at 1e7)", fontsize=8, color=INK)
    ax.set_title("Predicted LOD per architecture", fontsize=10, color=INK, loc="left")
    for s, c in scheme_color.items():
        ax.plot([], [], "o-", color=c, label=f"Scheme {s}")
    ax.legend(frameon=False, fontsize=7, loc="lower right")
    _style(ax)
    fig.tight_layout()
    fig.savefig(RES / "fig_lod_intervals.png", dpi=110)
    plt.close(fig)

    # 2. calibration curves: best architecture of each scheme (nominal), with 3 SD threshold
    best = {}
    for r in rows:
        best.setdefault(r["scheme"], r["architecture"])
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for s, name in sorted(best.items()):
        nom = mcs[name].nominal
        c = nom.conc_pgml[1:]
        k = ps.get("ma.statistics.k_sd", "dimensionless")
        ax.plot(c, nom.net_signal[1:], color=scheme_color[s], lw=2, label=f"{name}")
        ax.axhline(k * nom.blank_sd, color=scheme_color[s], lw=1, ls=":")
    ax.axvspan(1, 1000, color=GRID, alpha=0.5, zorder=0, lw=0)
    ax.text(1.2, 3e-15, "required range 1-1000 pg/mL", fontsize=7, color=INK2)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(1e-15, None)
    ax.set_xlabel("IgG concentration (pg/mL)", fontsize=8, color=INK)
    ax.set_ylabel("Net charge above blank (C)", fontsize=8, color=INK)
    ax.set_title("Nominal calibration curves (dotted: 3 x blank SD)", fontsize=10, color=INK, loc="left")
    ax.legend(frameon=False, fontsize=7)
    _style(ax)
    fig.tight_layout()
    fig.savefig(RES / "fig_calibration.png", dpi=110)
    plt.close(fig)

    # 3. blank variance breakdown, one representative per (scheme, capture, detector) base config (alp_hqdp)
    reps = [r for r in rows if r["chemistry"] == "alp_hqdp" and r["architecture"].count("/") == 1]
    reps += [r for r in rows if r["architecture"].startswith("B-mag-IDA/") and r["chemistry"] != "alp_hqdp"]
    fig, ax = plt.subplots(figsize=(8, 0.28 * len(reps) + 1.4))
    yy = np.arange(len(reps))[::-1]
    left = np.zeros(len(reps))
    for j, term in enumerate(TERMS):
        vals = np.array([r[f"varfrac_nominal_{term}"] for r in reps])
        ax.barh(yy, vals, left=left, color=PALETTE[j], height=0.7, edgecolor="white", linewidth=1,
                label=term.replace("_", " "), zorder=3)
        left += vals
    ax.set_yticks(yy)
    ax.set_yticklabels([r["architecture"] for r in reps], fontsize=7, color=INK)
    ax.set_xlim(0, 1)
    ax.set_xlabel("Share of blank variance (nominal parameters)", fontsize=8, color=INK)
    ax.set_title("What limits the LOD", fontsize=10, color=INK, loc="left")
    ax.legend(frameon=False, fontsize=7, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.12))
    _style(ax)
    fig.tight_layout()
    fig.savefig(RES / "fig_blank_breakdown.png", dpi=110)
    plt.close(fig)

    # 4. tornado for the leading architecture
    name = rows[0]["architecture"]
    oat = sens_all[name][:12][::-1]
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    yy = np.arange(len(oat))
    lo = np.array([o["dlog10_lod_at_low"] for o in oat])
    hi = np.array([o["dlog10_lod_at_high"] for o in oat])
    lo = np.clip(lo, -3, 3)
    hi = np.clip(hi, -3, 3)
    ax.barh(yy, lo, color=PALETTE[0], height=0.6, label="parameter at low bound", zorder=3)
    ax.barh(yy, hi, color=PALETTE[1], height=0.6, label="parameter at high bound", zorder=3)
    ax.axvline(0, color=INK, lw=0.8)
    ax.set_yticks(yy)
    ax.set_yticklabels([o["parameter"] for o in oat], fontsize=7, color=INK)
    ax.set_xlabel("change in log10(LOD) from nominal (one at a time)", fontsize=8, color=INK)
    ax.set_title(f"LOD sensitivity: {name}", fontsize=10, color=INK, loc="left")
    ax.legend(frameon=False, fontsize=7, loc="lower right")
    _style(ax)
    fig.tight_layout()
    fig.savefig(RES / "fig_tornado.png", dpi=110)
    plt.close(fig)


if __name__ == "__main__":
    main()
