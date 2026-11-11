#!/usr/bin/env python3
"""Attribute the optimisation gain of each format to its design changes (docs/05 s.1.3).

For each optimised format the design changes are applied cumulatively (in the order listed in the optimum
file) starting from the audited baseline architecture; each step reports nominal LOD, MC median and P(success)
(n = 1000), plus the flag saying which UNVERIFIED parameter the gain rests on (design_lib.ASSUMPTION_FLAGS).
Infeasible intermediate states (e.g. > 60 min before the time is recovered elsewhere) are shown as such.

Usage: python scripts/gain_decomposition.py  -> results/design/gain_decomposition.md
"""
from __future__ import annotations

import json

import design_lib as L
from design_lib import fmt


def main():
    ps = L.load_ps()
    out = ["# Cumulative gain decomposition of the optimised designs\n", "n = 1000 per row.\n"]
    for key in ["OS", "SQ", "FRB", "FRC"]:
        rec = json.load(open(L.OUT / f"optimum_{key}__baseline.json"))
        a = L.base_arch(key)
        s = L.mc(a, ps, n=1000)
        out += [f"\n## {key}: {L.FORMAT_LABEL[key]}\n",
                "| Step (cumulative) | value | LOD nominal | MC median | P(success) | feasible | gain rests on |",
                "|---|---|---|---|---|---|---|",
                f"| audited baseline | - | {fmt(s['lod_nominal'])} | {fmt(s['lod_median'])} | {s['p_success']:.2f} | "
                f"{'yes' if not L.constraint_violations(a, ps) else 'no'} | - |"]
        # order: largest single-step effects first is hard to know a priori; use the optimiser trajectory order
        traj = [l.split(",") for l in open(L.OUT / f"trajectory_{key}__baseline.csv").read().splitlines()[2:]]
        order = []
        for t in traj:
            if t[1] in rec["design"] and t[1] not in order:
                order.append(t[1])
        order += [k for k in rec["design"] if k not in order]
        for k in order:
            a = a.with_design(**{k: rec["design"][k]})
            s = L.mc(a, ps, n=1000)
            why = L.constraint_violations(a, ps)
            out.append(f"| {k} | {rec['design'][k]:g} | {fmt(s['lod_nominal'])} | {fmt(s['lod_median'])} | "
                       f"{s['p_success']:.2f} | {'yes' if not why else 'no: ' + '; '.join(why)} | "
                       f"{L.ASSUMPTION_FLAGS.get(k, 'detector/timing settings; model physics verified (transport)')} |")
            print(out[-1], flush=True)
    (L.OUT / "gain_decomposition.md").write_text("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
