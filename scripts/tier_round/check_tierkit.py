"""Validation of scripts/tier_round/tierkit.py against analytic limits.

Run:  python scripts/tier_round/check_tierkit.py     (writes results/tier_round/check_tierkit.md)
Exits non-zero if any check fails.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tierkit as tk  # noqa: E402
from elisa_sim import transport as tr  # noqa: E402

OUT = HERE.parents[1] / "results" / "tier_round" / "check_tierkit.md"
rows = []


def check(name, got, want, tol, note=""):
    err = abs(got - want) / abs(want) if want != 0 else abs(got)
    ok = err <= tol
    rows.append((name, got, want, err, tol, "PASS" if ok else "FAIL", note))
    return ok


D_IGG, D_HQ = 3.89e-11, 9.0e-10

# ---- B. planar capture under flow ----------------------------------------------------------------------
h, w, L, Q = 250e-6, 4e-3, 2.66e-3, 5 * tk.ULMIN
f = float(tk.planar_flow_capture(D_IGG, 1e3, h, w, L, w, 200 * tk.ULMIN))          # perfect sink, fast flow
zeta = L * D_IGG * w / (200 * tk.ULMIN * h)
check("B1 Leveque limit of the slit conversion (perfect sink, zeta = %.1e)" % zeta, f,
      1.4675 * zeta ** (2 / 3), 0.03, "1.4675 zeta^(2/3)")
km = float(tk.leveque_mass_transfer_coefficient(D_IGG, h, w, L, 200 * tk.ULMIN))
check("B2 k_m L w / Q equals the Leveque conversion", km * L * w / (200 * tk.ULMIN), 1.4675 * zeta ** (2 / 3), 0.002)
kr = 1e-9
f = float(tk.planar_flow_capture(D_IGG, kr, h, w, L, w, Q))
check("B3 kinetic limit (Da -> 0): conversion = k_r L w / Q", f, kr * L * w / Q, 0.02)
f_full = float(tk.planar_flow_capture(D_IGG, 4e-6, h, w, L, w, Q))
f_half = float(tk.planar_flow_capture(D_IGG, 4e-6, h, w, L, 0.5 * w, Q))
check("B4 a patch half as wide as the channel captures half", f_half, 0.5 * f_full, 1e-9)
f = float(tk.planar_flow_capture(D_IGG, 1e3, 25e-6, 0.5e-3, 20e-3, 0.5e-3, 0.2 * tk.ULMIN))
check("B5 long thin channel, slow flow: complete capture", f, 1.0, 0.01)
# disc versus square of equal area in the Leveque regime (integral of chord^(2/3))
u = np.linspace(-1, 1, 200001)
disc = 2 ** (2 / 3) * np.trapezoid((1 - u ** 2) ** (1 / 3), u)                   # x a^(5/3)
square = np.pi ** (5 / 6)                                                        # (a sqrt(pi))^(5/3)
check("B6 Leveque flux to a disc / to a square of equal area", disc / square, 1.03, 0.01, "justifies sqrt(A) side")

# ---- C. stopped slab with a reactive floor --------------------------------------------------------------
hs = 100e-6
for T in (0.05, 0.3, 1.0):
    t = T * hs ** 2 / D_IGG
    n = np.arange(0, 200)
    want = 1 - 8 / np.pi ** 2 * np.sum(np.exp(-(2 * n + 1) ** 2 * np.pi ** 2 * T / 4) / (2 * n + 1) ** 2)
    check(f"C1 perfect-sink slab, D t / h^2 = {T}", float(tk.slab_capture_fraction(D_IGG, 1e2, hs, t)), want, 0.01)
t = 30.0
check("C2 short time, perfect sink: 2 sqrt(D t / pi) / h", float(tk.slab_capture_fraction(D_IGG, 1e2, 500e-6, t)),
      2 * np.sqrt(D_IGG * t / np.pi) / 500e-6, 0.02)
kr = 1e-8
check("C3 slow reaction (Bi -> 0): 1 - exp(-k_r t / h)", float(tk.slab_capture_fraction(D_IGG, kr, hs, 2000.0)),
      1 - np.exp(-kr * 2000.0 / hs), 0.01)

# ---- G. thin-layer solver ---------------------------------------------------------------------------------
a, hh, R = 1.5e-3, 250e-6, 3.0e-3
tl = tk.ThinLayer(a, hh, R, D_HQ)
check("G0 electrode area on the grid", tl.we_area, np.pi * a ** 2, 1e-9)
r = tl.run([("off", 300.0)], source=tl.source_surface("floor", 0.0, a))
check("G1 mass conservation, electrode off, floor source 1 mol/s for 300 s", r["mass"][-1], 300.0, 1e-9)
r = tl.run([("off", 200.0), ("on", 400.0)], source=tl.source_surface("ceiling", 0.0, R))
check("G2 mass balance with electrode on: mass + collected = produced", r["mass"][-1] + r["cum"][-1], 600.0, 1e-9)

full = tk.ThinLayer(R, hh, R, D_HQ)                                             # electrode covers the whole floor
T = 0.4
t = T * hh ** 2 / D_HQ
r = full.run([("on", t)], c0=1.0)
n = np.arange(0, 200)
rem = 8 / np.pi ** 2 * np.sum(np.exp(-(2 * n + 1) ** 2 * np.pi ** 2 * T / 4) / (2 * n + 1) ** 2)
check("G3 exhaustive thin-layer electrolysis, fraction collected at D t / h^2 = 0.4",
      r["cum"][-1] / (np.pi * R ** 2 * hh), 1 - rem, 0.01)
t_long = 20 * hh ** 2 / D_HQ
r = full.run([("on", t_long)], source=full.source_surface("ceiling", 0.0, R))
check("G4 ceiling source over a full-floor electrode: steady collection rate", r["rate"][-1], 1.0, 1e-3)
check("G5 same: time lag h^2 / (2 D)", t_long - r["cum"][-1], hh ** 2 / (2 * D_HQ), 0.02)
r = full.run([("off", t_long)], source=full.source_surface("floor", 0.0, R))
J = 1.0 / (np.pi * R ** 2)
check("G6 floor source, electrode off: surface concentration J t / h + J h / (3 D)", r["csurf"][-1],
      J * t_long / hh + J * hh / (3 * D_HQ), 0.01, "cell-centre value of the first layer")
r = tl.run([("on", 2.0)], c0=1.0)
i_cott = np.pi * a ** 2 * np.sqrt(D_HQ / (np.pi * 2.0))
check("G7 Cottrell flux to the disc at 2 s (layer not yet depleted)", r["rate"][-1], i_cott, 0.06,
      "backward Euler; edge diffusion adds a few %")
r = tl.run([("on", 30000.0)], c0=1.0)
check("G8 long electrolysis collects the whole layer", r["cum"][-1], np.pi * R ** 2 * hh, 0.03)
r1 = tl.run([("on", 600.0)], source=tl.source_surface("floor", a, R))
fine = tk.ThinLayer(a, hh, R, D_HQ, nr_in=60, nz=26)
r2 = fine.run([("on", 600.0)], source=fine.source_surface("floor", a, R))
check("G9 grid convergence: floor-ring source collected in 600 s (36x18 vs 60x26 grid)", r1["cum"][-1],
      r2["cum"][-1], 0.02)

# ---- G4. chemical redox cycling -----------------------------------------------------------------------------
check("G10 cycling velocity, thin reaction layer: sqrt(D k)", float(tk.cycling_surface_velocity(D_HQ, 100.0, hh)),
      np.sqrt(D_HQ * 100.0), 1e-6)
check("G11 cycling velocity, layer thinner than the reaction layer: k h",
      float(tk.cycling_surface_velocity(D_HQ, 1e-3, 20e-6)), 1e-3 * 20e-6, 0.01)
# independent check of the reaction-diffusion flux with a 1-D finite-difference solution
k_reg, hz, nzz = 1.0, 250e-6, 4000
z = np.linspace(0, hz, nzz + 1)
dz = z[1] - z[0]
# steady state of D R'' - k R + k c_tot = 0, R(0) = 0, R'(h) = 0, c_tot = 1
Amat = np.zeros((nzz + 1, nzz + 1)); b = np.zeros(nzz + 1)
Amat[0, 0] = 1.0
for i in range(1, nzz):
    Amat[i, i - 1] = D_HQ / dz ** 2; Amat[i, i] = -2 * D_HQ / dz ** 2 - k_reg; Amat[i, i + 1] = D_HQ / dz ** 2
    b[i] = -k_reg
Amat[nzz, nzz - 1] = 2 * D_HQ / dz ** 2; Amat[nzz, nzz] = -2 * D_HQ / dz ** 2 - k_reg; b[nzz] = -k_reg
Rz = np.linalg.solve(Amat, b)
flux_fd = D_HQ * (-3 * Rz[0] + 4 * Rz[1] - Rz[2]) / (2 * dz)
check("G12 cycling velocity against a 1-D finite-difference reaction-diffusion solution",
      float(tk.cycling_surface_velocity(D_HQ, k_reg, hz)), flux_fd, 0.01)

# ---- H. impurity and hydrolysis in the stopped layer -----------------------------------------------------------
tlk, kr_ = tk.thin_layer_kernels(a, hh, R, D_HQ, (("on", 600.0),),
                                 (("we", "floor", 0.0, a), ("floor", "floor", a, R), ("lid", "ceiling", 0.0, R)))
V_over = np.pi * a ** 2 * hh
check("H1 impurity collected in 600 s exceeds the layer above the electrode (lateral in-diffusion)",
      float(kr_["initial"]["cum"][-1] > V_over), 1.0, 0.0)
check("H2 impurity collected in 600 s is below the whole layer", float(kr_["initial"]["cum"][-1] < np.pi * R ** 2 * hh),
      1.0, 0.0)
check("H3 hydrolysis source: collected + stored = produced", kr_["volume"]["cum"][-1] + kr_["volume"]["mass"][-1],
      600.0 * np.pi * R ** 2 * hh, 1e-9)
check("H4 lid source collected fraction lies between 0 and 1", float(0 < kr_["lid"]["cum"][-1] / 600.0 < 1), 1.0, 0.0)

# ---- radial (wall-jet thin gap) capture and inlet bore ------------------------------------------------------------
cellr = dict(flow_geometry="radial", h=100e-6, bore_radius=0.4e-3)
Qf = 200 * tk.ULMIN
s_eff = np.pi * (1.5e-3) ** 2 - np.pi * (0.4e-3) ** 2
got = float(tk.cell_conversion(cellr, D_IGG, np.pi * (1.5e-3) ** 2, Qf))
# Lighthill / Leveque solution for radial outflow in a gap: 3.147 D^(2/3) Q^(1/3) h^(-2/3) (a^2 - r0^2)^(2/3) / Q
want = 3.147 * D_IGG ** (2 / 3) * Qf ** (1 / 3) * (100e-6) ** (-2 / 3) * (s_eff / np.pi) ** (2 / 3) / Qf
check("R1 radial thin-gap capture equals the Lighthill-Leveque result for radial outflow", got, want, 0.03,
      "independent derivation, README B")
tb = tk.ThinLayer(0.5e-3, 0.16e-3, 1.0e-3, D_HQ, bore_radius=0.25e-3, bore_length=3e-3)
check("R2 liquid volume of layer + bore on the grid", tb.volume,
      np.pi * (1.0e-3) ** 2 * 0.16e-3 + np.pi * (0.25e-3) ** 2 * 3e-3, 1e-9)
rb_ = tb.run([("off", 300.0), ("on", 300.0)], source=tb.source_surface("ceiling", 0.25e-3, 1.0e-3))
check("R3 mass balance with a bore", rb_["mass"][-1] + rb_["cum"][-1], 600.0, 1e-9)

# ---- D. packed bed -------------------------------------------------------------------------------------------
check("D1 Kozeny-Carman, 2.8 um beads, eps 0.4, 24 um cake, 0.21 mm/s",
      float(tk.kozeny_carman_dp(0.89e-3, 2.1e-4, 2.8e-6, 0.4, 24e-6)),
      150 * 0.89e-3 * 2.1e-4 * 0.36 * 24e-6 / (0.064 * (2.8e-6) ** 2), 1e-9)

# ---- chain cross-checks with the audited model -------------------------------------------------------------------
import crosscheck_model  # noqa: E402

ref, res = crosscheck_model.bed_against_model()
check("X1 bed format: captured fraction equals the model's B-bed-TL/alp_hqdp", float(res.diagnostics["capture_fraction"]),
      float(ref.diagnostics["capture_fraction_low"]), 0.02)
check("X2 bed format: specific enzymes at 1 pg/mL equal the model's", float(res.diagnostics["enzymes_at_1pg"]),
      float(ref.diagnostics["enzymes_at_1pg"]), 0.05)
check("X3 bed format: signal at 1 pg/mL equals the model's", float(res.diagnostics["signal_at_1pg_C"]),
      float(ref.diagnostics["signal_at_1pg_C"]), 0.05)
check("X4 bed format: LOD within 25 % of the model's (unit-to-unit terms and regeneration differ)",
      float(res.lod_pgml), float(ref.lod_pgml), 0.25,
      f"kit {float(res.lod_pgml):.3g} vs model {float(ref.lod_pgml):.3g} pg/mL")

# ---- report -----------------------------------------------------------------------------------------------------
lines = ["# Checks of scripts/tier_round/tierkit.py against analytic limits and the audited model", "",
         "| Check | Kit | Reference | Relative error | Tolerance | Result | Note |", "|---|---|---|---|---|---|---|"]
for name, got, want, err, tol, res_, note in rows:
    lines.append(f"| {name} | {got:.5g} | {want:.5g} | {err:.2e} | {tol:.0e} | {res_} | {note} |")
n_fail = sum(1 for r in rows if r[5] == "FAIL")
lines += ["", f"{len(rows) - n_fail} of {len(rows)} checks passed."]
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(1 if n_fail else 0)
