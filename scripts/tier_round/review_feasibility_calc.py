#!/usr/bin/env python3
"""Reviewer's checks for docs/30 (feasibility lens). Writes nothing; prints numbers quoted in
results/tier_round/review_feasibility.md.   python scripts/tier_round/review_feasibility_calc.py [--kit]"""
import sys
import warnings
from math import pi, exp, erf
from pathlib import Path

import numpy as np

PSI = 6894.76
MU = 0.89e-3            # Pa s, water 25 C (docs/27 A.6)
BETA = 4.6e-10          # 1/Pa water compressibility (docs/27 §2)
ULMIN = 1e-9 / 60


def restrictor_psi(d_um, L_m, q_ulmin):
    return 128 * MU * L_m * q_ulmin * ULMIN / (pi * (d_um * 1e-6) ** 4) / PSI


print("A. 25 um x 45 cm restrictor (upstream of injector), pump pressure")
for q in (1, 3.25, 3.5, 4.5, 5, 20, 50, 80):
    print(f"  {q:6.2f} uL/min: {restrictor_psi(25, .45, q):7.0f} psi   (ID 23 um: {restrictor_psi(23, .45, q):7.0f};"
          f" ID 27 um: {restrictor_psi(27, .45, q):7.0f})")

print("\nB. Stored volume and decay after a step down (compressed liquid 0.4 mL UNVERIFIED, docs/27 §2)")
V = 0.4e-6
R = restrictor_psi(25, .45, 1) * PSI / ULMIN          # Pa s / m^3
for V_c in (0.4e-6, 4e-6):                             # water only, and 10x for seals/tubing compliance
    C = V_c * BETA
    tau = R * C
    for q0 in (50, 80):
        dV = C * restrictor_psi(25, .45, q0) * PSI
        print(f"  compliant vol {V_c*1e6:.1f} mL, step {q0}->0 uL/min: stored {dV*1e9:5.1f} uL, tau {tau:5.1f} s,"
              f" 95 % out after {3*tau:5.0f} s")
    print(f"  ... step 80 -> 1 uL/min (tier 1): flow at the cell after 60 s settle = "
          f"{1 + 79*exp(-60/tau):.2f} uL/min")

print("\nC. Substrate front at the electrode after the A1 -> B1 step (plug + 50 uL mixer as one tank)")
def front(V_prog, dwell, loop_in_line, V_post=3.5):
    V_plug = dwell - 50.0 + V_post + (100.0 if loop_in_line else 0.0)
    x = V_prog - V_plug
    return 0.0 if x <= 0 else 1 - exp(-x / 50.0)
cases = [("tier 1 (80 uL/min x1.5 min + 1 uL/min x5 min)", 125.0),
         ("tier 2 (50-80 uL/min x 2 min)", 100.0), ("tier 2 at 80", 160.0),
         ("tier 3 (50 uL/min x 2 min)", 100.0)]
for name, Vp in cases:
    s = "  ".join(f"dwell {dw:.0f}: offline {front(Vp, dw, False):.2f} / loop in line {front(Vp, dw, True):.2f}"
                  for dw in (85.0, 110.0))
    print(f"  {name:45s} {Vp:5.0f} uL -> {s}")
for target in (0.95, 0.99):
    v = 110 - 50 + 3.5 - 50 * np.log(1 - target)
    print(f"  volume for {target:.0%} of B1 at the cell, dwell 110, loop offline: {v:.0f} uL "
          f"(+100 uL with the loop in line)")

print("\nD. Tier 2: product diffusing from the bed to the electrode during the 7 min stop (1-D, area-weighted)")
D = 9e-10
# z = 0 electrode (absorbing).  0..0.8 mm: cell bore 0.8 mm I.D. below the capillary tip (tip 1 mm above the WE,
# 0.2 mm gap counted with the bore).  then frit 0.15 mm, bed 0.6 mm (eps 0.4), capillary 0.2 mm bore up to 10 mm.
dz = 5e-6
z = np.arange(0, 10e-3, dz) + dz / 2
A = np.where(z < 1.0e-3, pi * 0.4e-3 ** 2, pi * 0.1e-3 ** 2)
A = np.where((z >= 1.0e-3) & (z < 1.75e-3), A * 0.4, A)
src = ((z >= 1.15e-3) & (z < 1.75e-3)).astype(float)
src /= (src * A * dz).sum()                 # 1 mol/s total, spread over the bed volume
c = np.zeros_like(z)
Af = np.minimum(A[1:], A[:-1])              # face area
dt = 0.2 * dz ** 2 / D
t, absorbed, made = 0.0, 0.0, 0.0
while t < 420.0:
    flux = D * Af * (c[1:] - c[:-1]) / dz   # mol/s between cells (toward +z positive)
    dc = np.zeros_like(c)
    dc[:-1] += flux / (A[:-1] * dz)
    dc[1:] -= flux / (A[1:] * dz)
    out = D * A[0] * c[0] / (dz / 2)        # to the absorbing electrode
    dc[0] -= out / (A[0] * dz)
    c += dt * (dc + src)
    absorbed += out * dt
    made += dt
    t += dt
inv = (c * A * dz)
print(f"  of the product made during the stop: {absorbed/made:.2f} reached the electrode during the stop; "
      f"{inv[z < 1.0e-3].sum()/made:.2f} sits below the tip, {inv[z >= 1.0e-3].sum()/made:.2f} in frit/bed/capillary")
print(f"  liquid between capillary tip and electrode (0.8 mm bore, 1 mm): {pi*0.4**2*1.0:.2f} uL (docs/30: 0.1 uL)")
print(f"  rms diffusion length in 420 s: {np.sqrt(2*D*420)*1e3:.2f} mm")

print("\nE. Tier 3: single-pass re-capture on bed 2 (same beads and k_r as bed 1, kit nominal values)")
k_r, A_bed = 4.234e-6, 2.443e-5
for q in (1, 2, 5, 10):
    print(f"  push at {q:2d} uL/min: recapture {1-exp(-k_r*A_bed/(q*ULMIN)):.2f}")

print("\nF. Tier 2 alternative: bead plug held by a fixed magnet instead of a frit")
for q in (3.5, 80):
    dp = 1.076e5 * q / 3.5            # kit: 1.08 bar at 3.5 uL/min, scales with flow
    F = dp * pi * (0.1e-3) ** 2 / 1e6
    print(f"  {q:4.1f} uL/min: bed dP {dp/1e5:5.1f} bar -> {F*1e9:6.1f} nN per bead to hold "
          f"(magnetic force on an M-280 bead in a strong gradient is of order 0.01-0.1 nN, UNVERIFIED)")

print("\nG. Tier 3 time line rebuilt (min)")
steps = [("line 1 overhead", 1), ("sample 4.5 uL/min", 29), ("wash 1", 1.5), ("line 2 overhead", 1),
         ("conjugate 20 uL/min", 5), ("wash 2", 2), ("line 3 overhead", 1), ("eluent to bed 1 (~10 uL at 50)", 0.2),
         ("hold, V1 B", 5), ("push bed1->bed2, ~10 uL at 5 uL/min", 2), ("wash bed 2 (>= 2 min rule)", 2),
         ("B1 step 200 uL at 80 uL/min, loop offline", 2.5), ("accumulation", 7), ("sweep + read", 1.5)]
tot = 0
for n, m in steps:
    tot += m
    print(f"  {n:45s} {m:4.1f}  -> {tot:5.1f}")

if "--kit" in sys.argv:
    warnings.simplefilter("ignore")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import run_tiers as RT
    import tierkit as tk
    import design_lib as L
    ps0 = tk.load_params()
    EFF = "ma.design_levers.immune_complex_transfer_efficiency"

    def show(label, design, ps, n=600):
        k, _ = RT.run(design, ps, n)
        print(f"  {label:60s} nominal {k['lod_nominal']:.2f}  median {k['lod_median']:.2f} "
              f"[{k['lod_p05']:.2f}-{k['lod_p95']:.2f}]  P(<=1) {k['p_lod_le_target']:.2f}  t {k['time_to_result_min']:.1f}")
    print("\nH. Kit runs (n = 600, seed of the kit)")
    show("tier 2 as specified", RT.t2(), ps0)
    show("tier 2, 0.5 uL below the tip + 2.5 mm2 bore wall (as frit-eq.)", RT.t2(V_dead_uL=0.5, retainer_area=5.75e-6), ps0)
    show("tier 2, 6.3 min effective stop (creep)", RT.t2(t_acc=380.0), ps0)
    for e in (1.0, 0.8, 0.5):
        eff = 0.71 * e
        ps = L.with_bounds(ps0, EFF, value=eff, low=0.71 * 0.3, high=0.71)
        show(f"tier 3, efficiency 0.71 x elution {e:.1f} = {eff:.2f} [0.21-0.71]", RT.t3(), ps)
    show("tier 3 with load cut to 27 min (fits 60 min after G)", RT.t3(t_load=27.0, Q_load=4.8), ps0)
