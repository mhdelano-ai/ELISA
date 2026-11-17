"""Reviewer's back-of-envelope checks for results/tier_round/review_chemistry.md (chemistry lens).

All inputs are docs/30 nominal values or are labelled; every output is Derived.  Run: python review_chemistry_calc.py
"""
import numpy as np

NA = 6.022e23
LN2 = np.log(2)

# ---- 1. Two-step hydrolysis of HQDP: how much HQ (not HQMP) does a sparse enzyme population make? ----------------
# ALP is a non-processive monoesterase: E + HQDP -> E-P + HQMP (released); HQMP must re-bind to give HQ.
# HQMP competes with HQDP for the same site; with similar Km the HQMP turnover rate per enzyme is
# kcat*[HQMP]/(Km*(1+[HQDP]/Km)+[HQMP]) ~ kcat/(Km+[HQDP]) * [HQMP]  (Km for HQMP assumed equal: UNVERIFIED)
kcat, Km = 1000.0, 1e-4                      # docs/30 / params model_assumptions alp_hqdp
# Tier 2: 3.9e4 enzymes per pg/mL in the bed liquid (bed 19 nL, porosity 0.4 -> 7.6 nL; product volume 0.11 uL)
for label, V_L in (("bed pores 7.6 nL", 7.6e-9), ("product volume 0.11 uL", 0.11e-6)):
    E = 3.9e4 / NA / V_L
    k2 = kcat / (Km + 1e-3) * E              # 1/s, pseudo-first-order conversion HQMP -> HQ at 1 mM HQDP
    T = 420.0                                # 7 min stop
    # HQMP made at a constant rate r: HQ(T) = r*k2*T^2/2  vs HQMP ~ r*T  -> HQ/HQMP = k2*T/2
    print(f"T2 {label}: [E] = {E:.2e} M, k2 = {k2:.2e} 1/s, HQ/HQMP after 7 min = {k2*T/2:.1e}")
# Tier 1: enzymes on the electrode, product swept by flow.  Surface 'reaction velocity' for HQMP vs mass transfer.
Gamma = 1.1e3 / NA / 0.785e-6                # mol/m^2 (1.1e3 enzymes on 0.785 mm^2 at 1 pg/mL)
ks = kcat / (Km + 0.3e-3) * 1e-3 * Gamma     # m/s  (kcat/(Km+S) in M^-1 s^-1 -> x1e-3 to m^3/mol/s)
km = 1.9e-6                                  # m/s, docs/30 section 1 mass-transfer coefficient
print(f"T1: Gamma = {Gamma:.2e} mol/m2, k_s = {ks:.1e} m/s vs k_m = {km:.1e} m/s -> HQMP re-hydrolysed {ks/(ks+km):.1e}")

# ---- 2. Hydroquinone autoxidation at pH 9.5 (extrapolated) ------------------------------------------------------
# Moussavi 1979 via a property compilation [S]: first-order half-lives 111 h (pH 7), 41 h (pH 8), 0.84 h (pH 9).
pH = np.array([7.0, 8.0, 9.0]); th = np.array([111.0, 41.0, 0.84])
slope = np.polyfit(pH[1:], np.log10(th[1:]), 1)[0]          # use the pH 8-9 segment (dianion-controlled)
t95 = 10 ** (np.log10(0.84) + slope * 0.5)
print(f"HQ autoxidation: d log10(t1/2)/dpH (8-9) = {slope:.2f}; extrapolated t1/2 at pH 9.5 = {t95*60:.0f} min "
      f"(model product_half_life 120 min, low bound 30 min)")
for th_min in (t95 * 60, 30, 120):
    k = LN2 / (th_min * 60); T = 420
    keep = (1 - np.exp(-k * T)) / (k * T)   # fraction of product made at constant rate that survives to t = T
    print(f"  t1/2 {th_min:5.0f} min: fraction of 7-min product still HQ at the sweep = {keep:.2f}")

# ---- 3. Buffers ------------------------------------------------------------------------------------------------------
def beta(C, pKa, pH):
    a = 1 / (1 + 10 ** (pKa - pH)); return 2.303 * C * a * (1 - a)
print(f"Buffer capacity at pH 9.5: 0.1 M Tris (pKa 8.07) {beta(0.1, 8.07, 9.5)*1e3:.1f} mM/pH; "
      f"1 M DEA (pKa 8.9) {beta(1.0, 8.9, 9.5)*1e3:.0f} mM/pH; 0.1 M carbonate (pKa 10.3) {beta(0.1, 10.3, 9.5)*1e3:.0f} mM/pH")
Ksp = 5.6e-12; OH = 10 ** (9.5 - 14)
print(f"Mg(OH)2 solubility limit at pH 9.5: {Ksp/OH**2*1e3:.1f} mM (1 mM MgCl2 is below it)")

# ---- 4. Bead bed ---------------------------------------------------------------------------------------------------
d, eps, L, ID, mu = 2.8e-6, 0.4, 0.6e-3, 0.2e-3, 1e-3
A = np.pi * (ID / 2) ** 2
for Q_ul in (3.5, 20, 50, 80):
    u = Q_ul * 1e-9 / 60 / A
    dP = 180 * mu * L * u * (1 - eps) ** 2 / (eps ** 3 * d ** 2)
    print(f"Kozeny-Carman bed 0.6 mm x 0.2 mm, 2.8 um, eps 0.4: {Q_ul:4.1f} uL/min -> {dP/1e5:5.1f} bar")
n_beads = 1e6; beads_per_mg = 6.5e7       # 10 mg/mL ~ 6-7e8 beads/mL (Thermo MAN0014017 [V])
m_mg = n_beads / beads_per_mg
print(f"1e6 M-280 beads = {m_mg*1e3:.1f} ug = {m_mg/10*1e3:.2f} uL of stock; capacity 10 ug Ab/mg -> "
      f"{m_mg*10*1e3:.0f} ng F(ab')2 = {m_mg*10e-6/110e3*NA:.1e} molecules ({m_mg*10e-6/110e3*NA/n_beads:.1e} per bead)")
wall = 1 - ((ID / 2 - 5 * d) / (ID / 2)) ** 2
print(f"Fraction of the 0.2 mm bore within 5 bead diameters of the wall (loose-packed zone): {wall:.2f}")
print(f"Suspension volume 20 uL in a 0.2 mm bore occupies {20e-9/A*1e3:.0f} mm of capillary")

# ---- 5. Tier-3 transfer: desthiobiotin release in 5 min ---------------------------------------------------------------
# Kd(desthiobiotin-streptavidin) ~1e-11 M (vendor statements [S], UNVERIFIED); kon for streptavidin ligands 1e6-1e8 /M/s.
for kon in (1e6, 1e7, 1e8):
    koff = 1e-11 * kon
    print(f"desthiobiotin: kon {kon:.0e} -> koff {koff:.0e} 1/s, t1/2 {LN2/koff/60:7.1f} min, "
          f"single-tag release in 5 min {1-np.exp(-koff*300):.2f}; two tags both off (no rebinding) {(1-np.exp(-koff*300))**2:.3f}")
# bed-2 capacity against the eluted free capture F(ab')2
released = m_mg * 10e-6 / 110e3 * NA
for sites_per_bead in (1e5, 2.7e5, 8e5):
    cap = 1e6 * sites_per_bead
    print(f"bed 2 with {sites_per_bead:.0e} sites/bead: capacity {cap:.1e} vs eluted tagged F(ab')2 up to {released:.1e} "
          f"-> complex recovery bounded by ~{min(1, cap/released):.2f} if bed 2 targets the capture-antibody tag")
