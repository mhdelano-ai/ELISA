#!/usr/bin/env python3
"""How the one-step (pre-filled vial) format behaves when the in-vial incubation time is not controlled
(docs/05 section 4.3: customer adds sample to all pre-filled vials at once, then the queue sets the time).

For the optimised one-step design, evaluates at in-vial incubation 20 ... 240 min (nominal parameters):
  * LOD when blanks see the same incubation time,
  * calibration slope at 1-10 pg/mL relative to the design incubation (a sample read against a calibration
    made at the design time is biased by this ratio),
  * blank mean relative to the design incubation.
Time-to-result is reported but the 60-min limit is ignored here on purpose (queue case).
NSB is linear in time in the model (UNVERIFIED); a saturable NSB would make the long-time blank smaller.

Usage: python scripts/incubation_queue.py   -> results/design/incubation_queue.md
"""
from __future__ import annotations

import json

import numpy as np

import design_lib as L
from design_lib import fmt
from elisa_sim.model import evaluate


def main():
    ps = L.load_ps()
    rec = json.load(open(L.OUT / "optimum_OS__baseline.json"))
    base = L.base_arch("OS").with_design(**rec["design"])
    t0 = rec["design"].get("ma.timing.in_vial_incubation", ps.values["ma.timing.in_vial_incubation"])
    r0 = evaluate(base, ps)
    i1 = np.searchsorted(r0.conc_pgml, 1.0)
    i10 = np.searchsorted(r0.conc_pgml, 10.0)
    slope0 = r0.net_signal[i10] / r0.conc_pgml[i10]
    lines = ["| In-vial time (min) | LOD nominal, blanks at same time (pg/mL) | slope vs design time | "
             "blank mean vs design time | blank-equivalent (pg/mL) | ULOQ (pg/mL) |", "|---|---|---|---|---|---|"]
    for t in [20, 30, t0, 45, 60, 90, 120, 180, 240]:
        a = base.with_design(**{"ma.timing.in_vial_incubation": float(t)})
        r = evaluate(a, ps)
        slope = r.net_signal[i10] / r.conc_pgml[i10]
        lines.append(f"| {t:g} | {fmt(r.lod_pgml)} | {slope / slope0:.2f} | {float(r.blank_mean / r0.blank_mean):.2f} | "
                     f"{fmt(r.diagnostics['blank_equivalent_pgml'])} | {fmt(r.uloq_pgml)} |")
    # timing error tolerance: +-2 min around the design time
    sl = []
    for dt in (-2, 2):
        r = evaluate(base.with_design(**{"ma.timing.in_vial_incubation": float(t0 + dt)}), ps)
        sl.append(r.net_signal[i10] / r.conc_pgml[i10] / slope0)
    txt = (f"# One-step format: dependence on the in-vial incubation time\n\nDesign incubation {t0:g} min "
           f"(optimised one-step design). Slope change for +-2 min timing error: {sl[0]:.3f} / {sl[1]:.3f}.\n\n"
           + "\n".join(lines) + "\n")
    (L.OUT / "incubation_queue.md").write_text(txt)
    print(txt)


if __name__ == "__main__":
    main()
