#!/usr/bin/env python3
"""What the SHARED bead + conjugate reservoir of docs/05 s4.1 would have cost (final review docs/08, finding B4).

docs/05 held beads and conjugate together in one stirred reservoir for hours (20 uL dose carries 0.3 nM final in
~220 uL, so the reservoir holds ~3.3 nM conjugate with the beads). The design is now changed to SEPARATE bead and
conjugate reservoirs; this script quantifies the counterfactual with existing parameters only:

  * The model's conjugate NSB is linear and irreversible in exposure C*t (docs/04 s3.6, UNVERIFIED), and NSB on
    the beads scales with ma.nsb.surface_factor_magnetic_beads (bead term only; walls are not pre-exposed).
  * Pre-exposure in the reservoir for a hold time t_h at C_res = 3.3 nM adds C_res * t_h * k_T to the in-cup
    exposure E_cup = 0.3 nM x (30 + 6.6) min = 11 nM*min, where k_T is the unknown slowing of NSB at 4-8 C
    (k_T = 1: no slowing; 0.25: an illustrative 4x slowing, UNVERIFIED).
  * So the bead NSB term is multiplied by M = 1 + C_res * t_h * k_T / E_cup, applied as a scale on the bead
    surface factor (value and bounds).
Outside the model (not represented): saturation of adsorption, conjugate aggregation during storage, complete
sandwiches formed on capture beads by human IgG carried in the reagents, and detection-on-capture binding in the
reservoir. All of these act in the same direction (larger blank). docs/06 E1.3 (reservoir-ageing arm) measures it.

Usage: python scripts/shared_reservoir_cost.py [--n 2000] -> results/design/shared_reservoir_cost.md
"""
from __future__ import annotations

import argparse

import design_lib as L
import final_designs as F
from design_lib import fmt

C_RES_NM = 0.3 * 220.0 / 20.0          # 3.3 nM in a shared reservoir dosed 20 uL into ~220 uL
E_CUP_NM_MIN = 0.3 * (30.0 + 6.6)      # in-cup exposure of the one-step chamber design (incubation + emptying)
HOLDS_H = [0.0, 0.5, 2.0, 4.0, 8.0, 12.0, 24.0]
SLOWING = [1.0, 0.25]
SF_KEY = "ma.nsb.surface_factor_magnetic_beads"


def bead_nsb_multiplier(hold_h: float, slowing: float = 1.0) -> float:
    return 1.0 + C_RES_NM * hold_h * 60.0 * slowing / E_CUP_NM_MIN


def with_preexposure(ps, mult: float):
    p = ps.params[SF_KEY]
    return L.with_bounds(ps, SF_KEY, value=p.value * mult, low=p.low * mult, high=p.high * mult)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=L.N_FINAL)
    a = ap.parse_args(argv)
    ps0 = L.load_ps()
    dkey, arch, pmod, f = next(e for e in F.designs(ps0) if e[0] == "P-chamb")
    lines = ["| mean hold time in the shared reservoir (h) | NSB slowing at 4-8 C | bead NSB multiplier M | "
             "LOD nominal | LOD median [5-95 %] | P(success) |", "|---|---|---|---|---|---|"]
    for k in SLOWING:
        for h in HOLDS_H:
            if h == 0.0 and k != SLOWING[0]:
                continue
            m = bead_nsb_multiplier(h, k)
            s = L.mc(arch, pmod(with_preexposure(ps0, m)), n=a.n, lod_scale=f)
            lines.append(f"| {h:g} | {'none' if k == 1 else f'x{k:g} (illustrative)'} | {m:.3g} | "
                         f"{fmt(s['lod_nominal'])} | {fmt(s['lod_median'])} [{fmt(s['lod_p05'])}-{fmt(s['lod_p95'])}] | "
                         f"~{s['p_success']:.2f} |")
            print(lines[-1], flush=True)
    txt = ("# Cost of a shared bead + conjugate reservoir (counterfactual; docs/08 B4)\n\n"
           f"Primary design P-chamb (final_designs default), n = {a.n}, seed {L.SEED}. Reservoir conjugate "
           f"{C_RES_NM:.2g} nM; in-cup exposure {E_CUP_NM_MIN:.3g} nM*min. A reservoir filled once and used for 8 h "
           "gives a mean hold of 4 h (worst sample 8 h); for a 24-h sequence 12 h (worst 24 h). Linear irreversible "
           "NSB assumed (UNVERIFIED); saturation, aggregation and reagent-borne human IgG are outside the model. "
           "The primary design now uses separate reservoirs (hold time 0 by construction).\n\n"
           + "\n".join(lines) + "\n")
    (L.OUT / "shared_reservoir_cost.md").write_text(txt)


if __name__ == "__main__":
    main()
