#!/usr/bin/env python3
"""Constrained design optimisation of the candidate formats (Task 4, docs/05 section 1).

Coordinate search over the discrete design grids in design_lib.SPACES.  Objective: Monte Carlo median of
L_eff = LOD x max(1, 1000/ULOQ) (n = 300 draws, fixed seed = common random numbers between designs);
ties broken by P(success).  Only designs that satisfy every hard constraint (design_lib.constraint_violations:
time to result <= 60 min, nominal ULOQ >= 1000 pg/mL, BSM minimum flow, loop/mode consistency, >= 2 loop
volumes of flush, isolated tubing >= 1 cm, bead loading flow <= 100 uL/min, chip channel >= 3 mm, bed
pressure drop <= 10 MPa) are accepted.  The optimum is then re-evaluated with n = 2000.

Usage:
  python scripts/optimise_designs.py                       # all formats, audited parameters
  python scripts/optimise_designs.py --formats OS SQ --scenario dab_screened
Outputs (results/design/):
  optimum_<FMT>__<scenario>.json      design dict, constraint status, MC summary, bound flags
  trajectory_<FMT>__<scenario>.csv    every accepted move
  optimisation_<scenario>.md          table: baseline vs optimised, with detector alternatives
"""
from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import replace

import numpy as np

import design_lib as L
from design_lib import fmt

SCENARIOS = {
    "baseline": lambda ps: ps,
    # detection reagent screened to t1/2 >= 1 h, like the capture reagent (docs/04 section 3.3)
    "dab_screened": lambda ps: L.with_bounds(ps, "chem.antibodies.koff_detection", value=1.0e-4, low=3.0e-6,
                                             high=1.9e-4),
}

DETECTORS = {"OS": ["ida_flow", "thin_layer", "coulometric", "wall_jet_sencell"],
             "SQ": ["ida_flow", "thin_layer", "coulometric", "wall_jet_sencell"],
             "FRB": ["ida_flow", "thin_layer", "coulometric", "wall_jet_sencell"],
             "CAP": ["thin_layer", "ida_flow"],
             "FRC": ["ida_chip"]}


def objective(arch, ps, n):
    why = L.constraint_violations(arch, ps)
    if why:
        return np.inf, 0.0, why
    s = L.mc(arch, ps, n=n)
    return s["leff_median"], s["p_success"], []


def optimise(key, ps, n, sweeps, log):
    arch = L.base_arch(key)
    space = L.SPACES[key]
    best_val, best_p, why = objective(arch, ps, n)
    log.append(dict(sweep=0, variable="(start)", value="", leff_median=best_val, p_success=best_p,
                    note="; ".join(why)))
    print(f"[{key}] start: L_eff median {fmt(best_val, 3)} P {best_p:.3f} {why}", flush=True)
    for sw in range(1, sweeps + 1):
        moved = False
        for var, grid in space.items():
            cur = dict(arch.design).get(var, ps.values[var])
            cands = []
            for v in grid:
                if np.isclose(v, cur, rtol=1e-6, atol=0.0):
                    continue
                a2 = arch.with_design(**{var: v})
                val, p, why = objective(a2, ps, n)
                cands.append((val, -p, v, a2))
            cands = [c for c in cands if np.isfinite(c[0])]
            if not cands:
                continue
            cands.sort(key=lambda c: (round(np.log10(c[0]), 3), c[1]))
            val, negp, v, a2 = cands[0]
            better = (np.log10(val) < np.log10(best_val) - 0.004) if np.isfinite(best_val) else True
            if not better and np.isclose(np.log10(val), np.log10(best_val), atol=0.004) and -negp > best_p + 0.01:
                better = True
            if better:
                arch, best_val, best_p = a2, val, -negp
                moved = True
                log.append(dict(sweep=sw, variable=var, value=v, leff_median=val, p_success=-negp, note=""))
                print(f"[{key}] sweep {sw}: {var} -> {v}: L_eff median {fmt(val, 3)} P {-negp:.3f}", flush=True)
        if not moved:
            break
    return arch


def bound_flags(key, arch, ps):
    """Which optimised variables sit on the edge of their grid (re-check required)."""
    out = {}
    for var, grid in L.SPACES[key].items():
        v = dict(arch.design).get(var, ps.values[var])
        if np.isclose(v, min(grid), rtol=1e-6, atol=0.0) or np.isclose(v, max(grid), rtol=1e-6, atol=0.0):
            out[var] = "low edge" if np.isclose(v, min(grid), rtol=1e-6, atol=0.0) else "high edge"
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--formats", nargs="*", default=["OS", "SQ", "FRB", "FRC", "CAP"])
    ap.add_argument("--scenario", default="baseline", choices=list(SCENARIOS))
    ap.add_argument("--n", type=int, default=L.N_OPT)
    ap.add_argument("--n-final", type=int, default=L.N_FINAL)
    ap.add_argument("--sweeps", type=int, default=4)
    args = ap.parse_args()
    ps = SCENARIOS[args.scenario](L.load_ps())
    t0 = time.time()
    lines = []
    for key in args.formats:
        log = []
        base = L.base_arch(key)
        opt = optimise(key, ps, args.n, args.sweeps, log)
        with open(L.OUT / f"trajectory_{key}__{args.scenario}.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(log[0].keys()))
            w.writeheader()
            for r in log:
                w.writerow({k: (fmt(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
        s_base = L.mc(base, ps, n=args.n_final)
        s_opt = L.mc(opt, ps, n=args.n_final)
        det_rows = []
        for det in DETECTORS[key]:
            if det == opt.detector:
                continue
            a_det = replace(opt, detector=det, name=f"{opt.name}[{det}]")
            why = L.constraint_violations(a_det, ps)
            if why:
                det_rows.append((det, None, why))
                continue
            det_rows.append((det, L.mc(a_det, ps, n=args.n_final), []))
        r_opt = s_opt["_mc"].nominal
        flags = bound_flags(key, opt, ps)
        rec = dict(format=key, label=L.FORMAT_LABEL[key], scenario=args.scenario, base=base.name,
                   design={k: v for k, v in opt.design},
                   constraints_ok=not L.constraint_violations(opt, ps),
                   time_to_result_min=r_opt.time_to_result_min, cycle_time_min=r_opt.cycle_time_min,
                   timeline_min={k: float(v) for k, v in r_opt.diagnostics["timeline_min"].items()},
                   pressure_drop_MPa=L.reactor_pressure_drop_mpa(opt, ps),
                   on_grid_edge=flags,
                   summary_opt={k: v for k, v in s_opt.items() if not k.startswith("_")},
                   summary_base={k: v for k, v in s_base.items() if not k.startswith("_")},
                   variance_fractions_nominal={k: float(v) for k, v in r_opt.variance_fractions().items()},
                   blank_equivalent_nominal=float(r_opt.diagnostics["blank_equivalent_pgml"]),
                   capture_fraction=float(np.squeeze(r_opt.diagnostics["capture_fraction_low"])),
                   label_fraction=float(np.squeeze(r_opt.diagnostics["label_fraction_low"])),
                   bead_share_of_nsb=float(np.squeeze(r_opt.diagnostics["bead_share_of_nsb"])),
                   detectors={d: ({k: v for k, v in s.items() if not k.startswith("_")} if s else why)
                              for d, s, why in det_rows})
        with open(L.OUT / f"optimum_{key}__{args.scenario}.json", "w") as fh:
            json.dump(rec, fh, indent=1, default=float)
        lines.append(L.row_text(f"{key} baseline ({base.name})", s_base))
        lines.append(L.row_text(f"**{key} optimised**", s_opt))
        for d, s, why in det_rows:
            if s:
                lines.append(L.row_text(f"{key} optimised, detector {d}", s))
            else:
                lines.append(f"| {key} optimised, detector {d} | infeasible: {'; '.join(why)} | | | | | |")
        print(f"[{key}] done ({time.time() - t0:.0f} s): base median {fmt(s_base['lod_median'])} P {s_base['p_success']:.3f}"
              f" -> opt nominal {fmt(s_opt['lod_nominal'])} median {fmt(s_opt['lod_median'])} "
              f"[{fmt(s_opt['lod_p05'])}-{fmt(s_opt['lod_p95'])}] P(LOD) {s_opt['p_lod_only']:.3f} "
              f"P(success) {s_opt['p_success']:.3f}; edges {flags}", flush=True)
    with open(L.OUT / f"optimisation_{args.scenario}.md", "a") as fh:
        fh.write(f"\n### Scenario: {args.scenario} (n = {args.n_final}, seed {L.SEED}; optimiser n = {args.n})\n\n")
        fh.write(L.TABLE_HEAD)
        fh.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
