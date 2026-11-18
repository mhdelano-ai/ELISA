#!/usr/bin/env python3
"""Second-pass review (consistency lens) of docs/30 Revision B: arithmetic of the step tables and a few Derived
checks.  Reads the design builders and the kit; does NOT run run_tiers.py and writes no file.

  python scripts/tier_round/review2_consistency.py
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))
import designs as D  # noqa: E402
import tierkit as tk  # noqa: E402
import design_lib as L  # noqa: E402

F = 96485.0

# 1. step tables of docs/30 (clock rows as printed), flows in uL/min
T1 = [(0, 1, 3.0), (1, 43, 3.0), (43, 44.5, 50), (44.5, 45.5, 50), (45.5, 49.5, 50), (49.5, 51.5, 150),
      (51.5, 52.9, 150), (52.9, 54.9, 150), (54.9, 56.4, 150), (56.4, 56.9, 150)]
T2 = [(0, 1, 3.4), (1, 38, 3.4), (38, 39.5, 50), (39.5, 40.5, 50), (40.5, 44.5, 50), (44.5, 46.5, 50),
      (46.5, 49.2, 80), (49.2, 50.2, 5), (50.2, 57.2, 0), (57.2, 58.7, 5)]
T3 = [(0, 1, 5), (1, 26, 5), (26, 27.5, 50), (27.5, 32.5, 50), (32.5, 34.5, 50), (34.5, 36, 50), (36, 41, 50),
      (41, 45, 2), (45, 47, 50), (47, 49.7, 80), (49.7, 56.7, 5), (56.7, 58.2, 5)]
for name, tab in (("T1", T1), ("T2", T2), ("T3", T3)):
    gaps = [i for i in range(1, len(tab)) if abs(tab[i][0] - tab[i - 1][1]) > 1e-9]
    print(f"{name}: end {tab[-1][1]} min, gaps {gaps}; volumes per row (uL):",
          [round((b - a) * q, 1) for a, b, q in tab])

# 2. builders' own totals
for nm, d in (("tier1", D.tier1()), ("tier2", D.tier2()), ("tier3", D.tier3()), ("one valve", D.tier3(
        transfer=False, Q_load=3.5, t_load=36.0))):
    t, _ = tk.timing(d)
    vd = d.get("bed", {}).get("V_dead")
    print(f"{nm}: {t:.2f} min; V_dead = {vd}")

# 3. nominal curves with the round's parameters (half-life 600 s) -> currents against the fixed ranges
ps = L.with_bounds(tk.load_params(), "ma.chemistries.alp_hqdp.product_half_life", value=600.0, low=120.0,
                   high=7200.0)
r1 = tk.evaluate_planar(dict(D.tier1(), ps_values={"ma.chemistries.alp_hqdp.substrate_concentration": 3.0e-4}),
                        ps) if False else None
for nm, d, ev in (("tier1", dict(D.tier1(), ps_values={"ma.chemistries.alp_hqdp.substrate_concentration": 3.0e-4}),
                   tk.evaluate_planar), ("tier2", D.tier2(), tk.evaluate_bed), ("tier3", D.tier3(), tk.evaluate_bed)):
    try:
        r = ev(d, ps)
    except Exception as e:  # noqa: BLE001
        print(nm, "evaluation failed:", e)
        continue
    c = np.asarray(r.conc_pgml, float).ravel()
    s = np.asarray(r.net_signal, float).ravel()
    diag = r.diagnostics
    print(f"{nm}: LOD {float(np.ravel(r.lod_pgml)[0]):.3g}; signal per pg/mL at 1 pg/mL "
          f"{float(np.ravel(diag.get('signal_at_1pg_C', np.nan))[0]):.3g} C; mean blank current "
          f"{float(np.ravel(diag.get('mean_blank_current_A', np.nan))[0]):.3g} A")
    for cc in (10, 100, 1000):
        i = np.argmin(abs(c - cc))
        print(f"   net signal at {c[i]:g} pg/mL: {s[i]:.3g} C")

# 4. Derived currents
# tier 1: 1 uM HQ check plug at 150 uL/min, stream conversion 0.074 (docs/30 section 1 item 5)
i_plug = 2 * F * 1e-3 * 150e-9 / 60 * 0.074
print(f"tier-1 HQ check plug (1 uM, 150 uL/min, eta 0.074): {i_plug * 1e9:.1f} nA vs 0.6 nA range")
# tier 1: current at 1000 pg/mL if linear, 1.6 pA per pg/mL on a 130 pA background
print(f"tier-1 current at 300 / 1000 pg/mL: {(130 + 1.6 * 300):.0f} / {(130 + 1.6 * 1000):.0f} pA vs 600 pA range")
# tier 2: peak current of the swept plug per pg/mL, sigma 1 uL (designs.tier2), Q 5 uL/min, 2.7 nC per pg/mL
sig_t = 1.0 / 5.0 * 60
print(f"tier-2 plug sigma {sig_t:.0f} s; Gaussian peak {2.7e-9 / (sig_t * np.sqrt(2 * np.pi)) * 1e12:.0f} pA per "
      f"pg/mL (linear regime); 6 nA range minus 124 pA baseline clips near "
      f"{(6000 - 124) / (2.7e-9 / (sig_t * np.sqrt(2 * np.pi)) * 1e12):.0f} pg/mL if linear")
# tier 3: eluent front at bed 1 within row 34.5-36 if the SM-FL line overhead is t_o
for t_o in (0.25, 1.0, 1.5, 2.0):
    v = max(0.0, 1.5 - t_o) * 50
    print(f"tier-3 line-3 overhead {t_o} min -> {v:.0f} uL pushed behind the eluent before V1 goes OUT at 36 min")
# tier 2 bore volume below the tip vs kit V_dead
print(f"bore below tip 1 mm x 0.8 mm: {np.pi * 0.4 ** 2 * 1.0:.2f} uL (kit V_dead 0.1 uL)")
# tier 2 dwell after the pre-run: B1 pushed behind the sample at 3.4 uL/min over 38 min
V_push = 3.4 * 38
for dwell in (85, 110):
    print(f"dwell {dwell} uL of B1 after the tier-2 pre-run: {max(0, V_push - 100):.0f} uL of what follows the sample "
          f"reaches the bed before Loop Offline, all of it B1")
