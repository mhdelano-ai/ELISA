#!/usr/bin/env python3
"""Independent re-computation of the nominal chains of tiers 1 and 2 (docs/30 sections 3.4, 4.4) for the review
results/tier_round/review_numbers.md.  Does NOT call tierkit or elisa_sim: parameters are read straight from
params/*.yaml (with the ma.overrides section applied) and scripts/tier_round/tier_params.yaml; the slit conversion
is solved by its own finite-volume marching scheme and checked against the Leveque limit.

Part B (optional, --kit) re-runs the kit with the reviewer's alternative defaults (this part does call tierkit).

    python scripts/tier_round/review_numbers.py [--kit]
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]
NA, F = 6.02214076e23, 96485.33212


# ------------------------------------------------------------------ parameters (raw YAML, own flattening)
def load():
    flat = {}

    def fl(pfx, d):
        for k, v in d.items():
            if isinstance(v, dict) and "value" in v and "unit" in v:
                flat[f"{pfx}.{k}"] = v
            elif isinstance(v, dict):
                fl(f"{pfx}.{k}", v)
    for f, p in (("params/chemistry.yaml", "chem"), ("params/hardware.yaml", "hw"),
                 ("params/model_assumptions.yaml", "ma"), ("scripts/tier_round/tier_params.yaml", "tr")):
        fl(p, yaml.safe_load(open(ROOT / f)))
    for k in [k for k in flat if k.startswith("ma.overrides.")]:     # bench/override values replace the base
        flat[k[len("ma.overrides."):]] = flat[k]
    return {k: v["value"] for k, v in flat.items()}


P = load()
assert P["hw.smfl.loop_volume_recommended"] in (100, 100.0), P["hw.smfl.loop_volume_recommended"]


# ------------------------------------------------------------------ slit conversion, own solver
def slit_conversion(xi_end, Da, n=500, nsteps=4000):
    """Conversion of a fully developed plane Poiseuille stream over a reactive wall (one wall, Robin BC with
    Da = k_r h / D; Da = inf -> Dirichlet).  6 e(1-e) dc/dxi = d2c/de2, xi = D x w / (Q h).  Implicit FV."""
    # geometric grid clustered at the wall e = 0
    g = 1.02
    w = g ** np.arange(n); w /= w.sum()
    ef = np.concatenate([[0.0], np.cumsum(w)]); ec = 0.5 * (ef[1:] + ef[:-1]); de = np.diff(ef)
    u = 6 * ec * (1 - ec)                 # cell-centre velocity (normalised)
    # integrate u exactly over the cell for the mass weights
    U = 3 * (ef[1:] ** 2 - ef[:-1] ** 2) - 2 * (ef[1:] ** 3 - ef[:-1] ** 3)
    G = 1.0 / (ec[1:] - ec[:-1])          # conductances between cells
    if np.isinf(Da):
        g0 = 1.0 / (ec[0])                # Dirichlet c = 0 at e = 0
    else:
        g0 = 1.0 / (ec[0] + 1.0 / Da)     # Robin: series of half cell and 1/Da
    c = np.ones(n)
    xis = np.concatenate([[0.0], np.geomspace(1e-9 * max(xi_end, 1e-6), xi_end, nsteps)])
    from scipy.linalg import solve_banded
    for dxi in np.diff(xis):
        ab = np.zeros((3, n))
        diag = U / dxi
        diag[:-1] += G; diag[1:] += G; diag[0] += g0
        ab[1] = diag; ab[0, 1:] = -G; ab[2, :-1] = -G
        c = solve_banded((1, 1), ab, U / dxi * c)
    return 1.0 - float(U @ c)


def leveque(xi):
    return 1.4675 * xi ** (2 / 3)


# ------------------------------------------------------------------ shared pieces
M = P["chem.analyte.molar_mass"]                      # g/mol
V_s = 100e-9                                          # m^3
D_igg = P["chem.analyte.diffusion_coefficient"]
Gam = P["chem.surfaces.igg_surface_density_monolayer"] * P["chem.surfaces.active_fraction_oriented"] / NA
k_r = P["chem.antibodies.kon_capture"] * 1e-3 * Gam   # M^-1 s^-1 -> m^3/(mol s)
kon_d = P["chem.antibodies.kon_detection"] * 1e-3
koff_d, koff_c = P["chem.antibodies.koff_detection"], P["chem.antibodies.koff_capture"]
k_nsb = P["chem.nsb.nsb_effective_rate_constant"] * P["ma.nsb.label_factor_igg_enzyme_conjugate"] \
    * P["ma.labelling.detection_on_capture_residual_factor"]
kcat, Km = P["chem.enzymes.alp.kcat_conjugate_assay_conditions"], P["ma.chemistries.alp_hqdp.Km"] * 1e3  # mol/m^3
Ki = P["chem.enzymes.alp.phosphate_inhibition_Ki"] * 1e3
imp, khyd = P["ma.chemistries.alp_hqdp.free_product_impurity"], P["ma.chemistries.alp_hqdp.hydrolysis_rate"]
age = P["ma.timing.substrate_reservoir_age"] * 3600.0
t_half = P["ma.chemistries.alp_hqdp.product_half_life"]
D_hq = P["chem.substrates.HQ.diffusion_coefficient"]
nF = 2 * F
cv_nsb, inj = P["chem.nsb.blank_CV_analog_electrochemical"], P["hw.smfl.injection_precision_rsd_large"] / 100
cv_sub, rel_bg = P["ma.noise.substrate_background_cv"], P["ma.noise.background_current_relative_noise"]
drift_ref = P["hw.gamry.baseline_drift"] * 1e-12 if P["hw.gamry.baseline_drift"] > 1 else P["hw.gamry.baseline_drift"]
A_ref = P["ma.noise.reference_electrode_area"]
drift_res = P["ma.noise.drift_residual_fraction"]
f_del, loss = P["ma.delivery.delivered_fraction_full_loop_100"], P["ma.delivery.adsorptive_loss_fraction_with_carrier"]
F_TR = {1: 0.9789, 2: 0.9827}   # loop transfer of the full-loop plug: taken from the kit (Taylor-Aris table of
                                # elisa_sim; not re-derived here).  It is within 2 % of 1 and moves nothing.
ULMIN = 1e-9 / 60


def labelled(C_nM, V_uL, Q_uLmin):
    C = C_nM * 1e-6; t = V_uL / Q_uLmin * 60
    a = kon_d * C
    return a / (a + koff_d) * (1 - np.exp(-(a + koff_d) * t)), C * t     # fraction, exposure (mol s/m^3)


def per_area(exposure):            # non-specific enzymes per m^2 at surface factor 1
    return k_nsb * exposure * NA


def lod(slope, terms):
    sd = np.sqrt(sum(terms.values()))
    return 3 * sd / slope, sd


def report(name, d, terms, slope):
    L, sd = lod(slope, terms)
    tot = sum(terms.values())
    print(f"\n== {name}")
    for k, v in d.items():
        print(f"  {k:40s} {v:.4g}")
    print("  variance shares: " + ", ".join(f"{k} {v / tot:.2f}" for k, v in terms.items()))
    print(f"  blank SD {sd:.4g} C;  slope {slope:.4g} C per pg/mL;  LOD {L:.3g} pg/mL")
    return L


# ------------------------------------------------------------------ tier 1
def tier1(extra=None, rel_bg_t1=rel_bg, drift_exp=1.0, verbose=True, name="tier 1 nominal (independent)"):
    extra = extra or {}
    h, a, rb = 0.16e-3, 0.5e-3, 0.25e-3
    A_we = np.pi * a ** 2; s_we = np.pi * (a ** 2 - rb ** 2); R = 1.0e-3
    Q = 3.25 * ULMIN
    N_vial = 1e-12 / M * 1e3 * 1e-0 * V_s * NA * 1e0      # 1 pg/mL = 1e-9 g/m^3... computed below instead
    N_vial = (1e-12 / 1e-6) / M * V_s * NA                  # 1 pg/mL = 1e-6 g/m^3 -> mol/m^3 x V x NA
    N_in = N_vial * f_del * (1 - loss) * F_TR[1]
    xi = D_igg * s_we / (Q * h); Da = k_r * h / D_igg
    f_cap = slit_conversion(xi, Da)
    N_cap = N_in * f_cap
    f_lab, expo = labelled(10, 100, 50)
    # clocks (s): label from mid-conjugate (1 min) to mid-read: 1 + 2 + 1.5 + 1 + 2 min
    t_label = (1 + 2 + 1.5 + 1 + 2) * 60
    t_cap = (19.5 + 1.5 + 1 + 2 + 2 + 1.5 + 1 + 2) * 60
    N_enz = N_cap * f_lab * np.exp(-koff_d * t_label) * np.exp(-koff_c * t_cap)
    S0 = 0.3
    v = kcat * S0 / (Km + S0)
    i_spec = N_enz * v / NA * nF                 # A per pg/mL (product formed at the sink: collected in full)
    T = 240.0
    slope = i_spec * T
    pa = per_area(expo)
    N_we = pa * P["tr.nsb.surface_factor_gold_oeg"] * A_we
    A_lid = np.pi * (R ** 2 - rb ** 2)
    Qr = 1.0 * ULMIN
    eta = slit_conversion(D_hq * s_we / (Qr * h), np.inf)
    N_lid_eff = pa * P["tr.nsb.surface_factor_lid"] * 0.5 * eta * s_we      # the kit's lid rule
    i_nsb = (N_we + N_lid_eff) * v / NA * nF
    c_imp = imp * S0; c_hyd = khyd * S0 * age
    i_imp = nF * eta * Qr * c_imp; i_hyd = nF * eta * Qr * c_hyd
    Qn, Qh, Qi = i_nsb * T, i_hyd * T, i_imp * T
    i_n = max(2e-12 / 5, 3e-12 * (A_we / A_ref) ** 0.5)
    drift = drift_ref / 60 * (A_we / A_ref) ** drift_exp
    terms = dict(nsb=(cv_nsb ** 2 + P["tr.nsb.unit_to_unit_cv_planar"] ** 2 + inj ** 2) * Qn ** 2,
                 label_counting=(nF * v / NA * T) ** 2 * (N_we + N_lid_eff),
                 substrate=(cv_sub * Qh) ** 2 + (rel_bg_t1 * (Qi + Qh)) ** 2,
                 sensitivity=(P["tr.noise.preread_residual_cv"] * (Qn + Qh)) ** 2,
                 noise=i_n ** 2 * T,
                 drift_in_window=(drift_res * 0.5 * drift * T ** 2) ** 2)
    for k, val in extra.items():
        terms[k] = val(locals()) if callable(val) else val
    d = dict(N_vial=N_vial, N_in=N_in, xi_capture=xi, Da=Da, f_capture_of_N_in=f_cap,
             leveque_transport_limit=leveque(xi), N_captured=N_cap, f_label=f_lab,
             ret_label=np.exp(-koff_d * t_label), ret_capture=np.exp(-koff_c * t_cap), enzymes=N_enz,
             i_per_pgml_pA=i_spec * 1e12, eta_HQ_1uLmin=eta, N_nsb_we=N_we, N_lid_equiv=N_lid_eff,
             i_nsb_pA=i_nsb * 1e12, i_imp_pA=i_imp * 1e12, i_hyd_pA=i_hyd * 1e12,
             blank_current_pA=(i_nsb + i_imp + i_hyd) * 1e12, blank_equiv_pgml=(i_nsb + i_hyd) / i_spec,
             noise_pA=i_n * 1e12, drift_pA_per_min=drift * 60 * 1e12)
    L = report(name, d, terms, slope) if verbose else lod(slope, terms)[0]
    return L, locals()


# ------------------------------------------------------------------ tier 2
def bed_product(N_enz, V_acc, t_acc=420.0, S0=1.0, steps=4000):
    E = N_enz / NA / V_acc
    P_, S, dt = 0.0, S0, t_acc / steps
    kdec = np.log(2) / t_half
    for _ in range(steps):
        r = kcat * E * S / (Km * (1 + 2 * P_ / Ki) + S)
        P_ += (r - kdec * P_) * dt; S -= r * dt
    return P_ * V_acc


def tier2(verbose=True, name="tier 2 nominal (independent)", retainer=5e-6, bed_sf=None, V_dead=0.1e-9,
          upstream=None, rel_bg_t2=rel_bg):
    eps, dp, V_bed, col = 0.4, 2.8e-6, 0.019e-9, 200e-6
    A_bed = 6 * (1 - eps) / dp * V_bed
    Q = 3.5 * ULMIN
    N_vial = (1e-12 / 1e-6) / M * V_s * NA
    N_in = N_vial * f_del * (1 - loss) * F_TR[2]
    u = Q / (np.pi * (col / 2) ** 2); nu = P["ma.fluid.viscosity"] / P["ma.fluid.density"]
    Re, Sc = u * dp / nu, nu / D_igg
    km = P["ma.correlations.wilson_geankoplis_coefficient"] / eps * u * Re ** (-2 / 3) * Sc ** (-2 / 3)
    kt = 1 / (1 / km + 1 / k_r)
    f_bed = 1 - np.exp(-kt * A_bed / Q)
    N_cap = N_in * f_bed
    f_lab, expo = labelled(3, 100, 20)
    t_label = (2.5 + 3 + 2) * 60                         # mid-conjugate to start of the stop (kit convention)
    t_cap = (18 + 1.5 + 1 + 5 + 3 + 2) * 60
    N_enz = N_cap * f_lab * np.exp(-koff_d * t_label) * np.exp(-koff_c * t_cap)
    pa = per_area(expo)
    sf_b = P["ma.nsb.surface_factor_magnetic_beads"] if bed_sf is None else bed_sf
    N_nsb = pa * (sf_b * A_bed + P["tr.nsb.surface_factor_frit"] * retainer)
    V_acc = eps * V_bed + V_dead
    a, rb, h = 1.5e-3, 0.4e-3, 0.2e-3
    s = np.pi * (a ** 2 - rb ** 2); Qr = 5 * ULMIN; T = 90.0
    eta = slit_conversion(D_hq * s / (Qr * h), np.inf)
    n_blank = bed_product(N_nsb, V_acc)
    n_1 = bed_product(N_nsb + N_enz, V_acc) - n_blank
    slope = nF * eta * n_1
    Qn = nF * eta * n_blank
    Qh = nF * eta * khyd * 1.0 * 420 * V_acc
    Qi = nF * eta * Qr * imp * 1.0 * T
    A_we = np.pi * a ** 2
    terms = dict(nsb=(cv_nsb ** 2 + P["tr.nsb.unit_to_unit_cv_bed"] ** 2 + inj ** 2) * Qn ** 2,
                 label_counting=(Qn / N_nsb) ** 2 * N_nsb,
                 substrate=(cv_sub * Qh) ** 2 + (rel_bg_t2 * (Qi + Qh)) ** 2,
                 sensitivity=(P["tr.noise.preread_residual_cv"] * (Qn + Qh)) ** 2,
                 noise=(3e-12) ** 2 * T,
                 drift_in_window=(drift_res * 0.5 * drift_ref / 60 * T ** 2) ** 2)
    if upstream is not None:
        terms["upstream_walls"] = ((cv_nsb ** 2 + 0.1 ** 2) * upstream ** 2)   # upstream: absolute charge (C)
    d = dict(N_in=N_in, k_m_bed=km, k_r=k_r, f_bed=f_bed, f_capture_of_vial=N_cap / N_vial, N_captured=N_cap,
             f_label=f_lab, ret_label=np.exp(-koff_d * t_label), ret_capture=np.exp(-koff_c * t_cap),
             enzymes=N_enz, N_nsb=N_nsb, per_area_sf1_per_mm2=pa * 1e-6, V_acc_uL=V_acc * 1e9,
             product_per_pgml_mol=n_1, eta_HQ_5uLmin=eta, signal_nC_per_pgml=slope * 1e9,
             blank_equiv_pgml=Qn / slope, impurity_current_pA=nF * eta * Qr * imp * 1.0 * 1e12)
    L = report(name, d, terms, slope) if verbose else lod(slope, terms)[0]
    return L, locals()


# ------------------------------------------------------------------ physics add-ons of the review
def main():
    print("slit solver check (Da = inf): xi, solver, Leveque 1.4675 xi^(2/3)")
    for xi in (1e-3, 1e-2, 0.05):
        print(f"  {xi:g}  {slit_conversion(xi, np.inf):.5f}  {leveque(xi):.5f}")

    L1, t1 = tier1()
    L2, t2 = tier2()

    # --- R-1: tier 1 reference window is the pre-read, about 55 min before the read
    print("\n== tier 1 with the drift between the pre-read and the read (dt = 55 min)")
    for frac in (0.2, 0.05):
        L, _ = tier1(extra=dict(drift_between=lambda v, f=frac: (f * v["drift"] * 55 * 60 * v["T"]) ** 2),
                     verbose=False)
        print(f"  unpredictable fraction of the drift {frac:.2f}: LOD {L:.3g} pg/mL")

    # --- R-2: conjugate on the transfer tubing upstream of the cell (tier 1, flowing read)
    print("\n== tier 1 with the transfer tubing (0.127 mm x 0.2 m PEEK, surface factor 3) upstream of the cell")
    A_tube = np.pi * 0.127e-3 * 0.2
    v1 = t1
    N_tube = v1["pa"] * P["ma.nsb.surface_factor_tubing"] * A_tube
    ramp = ((2.5 ** 2 - 1) / 5 + 2.5) / 4          # mean fraction of steady state over min 1-5 after the switch
    i_tube = N_tube * v1["v"] / NA * nF * v1["eta"] * ramp
    print(f"  enzymes on the tubing {N_tube:.3g}; mean current in the read {i_tube * 1e12:.3g} pA "
          f"(= {i_tube / v1['i_spec']:.3g} pg/mL equivalent)")
    for cv in (0.1, 0.2):
        L, _ = tier1(extra=dict(tubing=lambda v, c=cv: (c * i_tube * v["T"]) ** 2), verbose=False)
        print(f"  tubing NSB with CV {cv:.2f}: LOD {L:.3g} pg/mL")
    A_loop = np.pi * 0.5e-3 * (100e-9 / (np.pi * 0.25e-3 ** 2))
    print(f"  (if the 100 uL loop stays in line: wall {A_loop * 1e6:.0f} mm^2; product ramps for 100 min at 1 uL/min)")

    # --- R-3: impurity normalisation residual 3 % and 5 % instead of 1 %
    for r in (0.03, 0.05):
        L, _ = tier1(rel_bg_t1=r, verbose=False)
        print(f"  tier 1 impurity residual after the pre-read {r:.2f}: LOD {L:.3g} pg/mL")
    L, _ = tier1(drift_exp=0.0, verbose=False)
    print(f"  tier 1 drift not scaled by electrode area: LOD {L:.3g} pg/mL")

    # --- R-4: tier 2, product made during the stop on the walls upstream of the bed
    print("\n== tier 2 with the walls upstream of the bed (stopped 7 min with the bed)")
    pa = t2["pa"]; sf_t = P["ma.nsb.surface_factor_tubing"]
    dens_bed = t2["N_nsb"] / t2["V_acc"]                                   # blank enzymes per m^3 in the plug
    dens_cap = pa * sf_t * 4 / 0.2e-3                                      # per m^3 of a 0.2 mm bore
    dens_peek = pa * sf_t * 4 / 0.127e-3
    print(f"  enzyme per volume: bed plug {dens_bed * 1e-9:.3g}/uL, capillary {dens_cap * 1e-9:.3g}/uL, "
          f"PEEK 0.127 mm {dens_peek * 1e-9:.3g}/uL")
    V_plug = np.sqrt(t2["V_acc"] ** 2 + 12 * (1e-9) ** 2)
    half_in_peak = 0.5 * dens_cap * V_plug / t2["N_nsb"]                   # residual of a straight baseline
    full_window = (dens_cap * 0.94e-9 + dens_peek * 2.53e-9 + dens_peek * 0 ) / t2["N_nsb"]
    print(f"  upstream product relative to the bed blank: {half_in_peak:.2f} (half the plateau under a "
          f"{V_plug * 1e9:.1f} uL peak) ... {full_window:.2f} (no baseline removal, 30 mm capillary + 0.2 m PEEK)")
    for rel in (half_in_peak, full_window):
        L, _ = tier2(upstream=rel * t2["Qn"], verbose=False)
        print(f"  tier 2 LOD with upstream term {rel:.2f} x bed blank: {L:.3g} pg/mL")
    L, _ = tier2(bed_sf=P["ma.nsb.surface_factor_packed_bed"], verbose=False)
    print(f"  tier 2 with the model's packed-bed surface factor (3): LOD {L:.3g} pg/mL")
    print(f"  tier 2 impurity current at 5 uL/min (steady, flowing; ~0 in the stopped, electrolysed cell): "
          f"{t2['d']['impurity_current_pA']:.3g} pA vs blank peak mean {t2['Qn'] / 90 * 1e12:.3g} pA")

    # --- R-5: tier 3 re-capture on bed 2 at 5 uL/min with the bed physics of the kit
    Q5 = 5 * ULMIN
    f_re = 1 - np.exp(-t2["kt"] * t2["A_bed"] / Q5)
    print(f"\n== tier 3: re-capture of eluted complexes on a 1e6-bead bed at 5 uL/min (same k_r): {f_re:.3f}")

    # --- R-6: stagnation zone under the bore (tier 1 capture), upper bound
    print(f"\n== tier 1 capture if the stagnation disc captured like the swept annulus: x"
          f"{(np.pi * 0.5e-3 ** 2) / (np.pi * (0.5e-3 ** 2 - 0.25e-3 ** 2)):.2f}")

    # --- R-7: tier 1 inlet-bore wall (PMMA, 0.5 mm x 5 mm, lid factor) directly upstream of the electrode
    A_bore = 2 * np.pi * 0.25e-3 * 5e-3
    N_bore = t1["pa"] * P["tr.nsb.surface_factor_lid"] * A_bore
    i_bore = N_bore * t1["v"] / NA * nF * t1["eta"]
    cvp = np.sqrt(cv_nsb ** 2 + P["tr.nsb.unit_to_unit_cv_planar"] ** 2)
    print(f"\n== tier 1 inlet-bore wall: {A_bore * 1e6:.2f} mm^2, {N_bore:.3g} enzymes, {i_bore * 1e12:.3g} pA "
          f"(= {i_bore / t1['i_spec']:.3g} pg/mL equivalent)")
    L, _ = tier1(extra=dict(bore=lambda v: (cvp * i_bore * v["T"]) ** 2), verbose=False)
    print(f"  tier 1 with the bore wall only: LOD {L:.3g} pg/mL")

    # --- corrected nominal estimates
    print("\n== reviewer's corrected nominal LODs")
    common = dict(bore=lambda v: (cvp * i_bore * v["T"]) ** 2, tubing=lambda v: (0.1 * i_tube * v["T"]) ** 2)
    L, _ = tier1(extra=dict(common, drift_between=lambda v: (0.2 * v["drift"] * 55 * 60 * v["T"]) ** 2),
                 verbose=False)
    print(f"  tier 1 as written (pre-read 55 min before; bore; tubing): {L:.3g}")
    L, _ = tier1(extra=dict(common), rel_bg_t1=0.03, verbose=False)
    print(f"  tier 1 with an adjacent buffer reference window (bore; tubing; impurity residual 3 %): {L:.3g}")
    L, _ = tier1(extra=dict(bore=common["bore"]), rel_bg_t1=0.03, verbose=False)
    print(f"  tier 1 as above, transfer tubing replaced by 2 cm of 0.0635 mm (term ~0): {L:.3g}")
    for lab, up, sf, rb_ in (("tier 2 upstream half-plateau, packed-bed factor 3, impurity residual 5 %", half_in_peak, 3.0, 0.05),
                             ("tier 2 upstream half-plateau only", half_in_peak, None, rel_bg),
                             ("tier 2 no baseline removal of upstream, factor 3, 5 %", full_window, 3.0, 0.05)):
        L, _ = tier2(upstream=up * t2["Qn"], bed_sf=sf, rel_bg_t2=rb_, verbose=False)
        print(f"  {lab}: {L:.3g}")

    if "--kit" in sys.argv:
        kit_alternatives()


def kit_alternatives():
    sys.path.insert(0, str(ROOT / "scripts" / "tier_round")); sys.path.insert(0, str(ROOT / "scripts"))
    import warnings; warnings.simplefilter("ignore")
    import run_tiers as RT, tierkit as tk
    ps = tk.load_params()

    def nom(d, mod=lambda p: p, ev=None):
        ev = ev or (tk.evaluate_planar if d["tier"] == 1 else tk.evaluate_bed)
        p = mod(ps)
        if d.get("ps_values"):
            p = p.with_values(d["ps_values"])
        return float(ev(d, p).lod_pgml)

    pin = lambda **kw: (lambda p: p.with_values(kw))
    print("\n== kit runs with the reviewer's alternatives (nominal LOD, pg/mL)")
    rows = [
        ("T1 primary", RT.t1(), None),
        ("T1 unit-to-unit CV planar 0.30", RT.t1(), pin(**{"tr.nsb.unit_to_unit_cv_planar": 0.30})),
        ("T1 pre-read residual CV 0.10", RT.t1(), pin(**{"tr.noise.preread_residual_cv": 0.10})),
        ("T1 impurity residual 0.05", RT.t1(), pin(**{"ma.noise.background_current_relative_noise": 0.05})),
        ("T1 drift area exponent 0.5", RT.t1(), pin(**{"tr.noise.drift_area_exponent": 0.5})),
        ("T1 gap 0.30 mm", RT.t1(h=0.30e-3), None),
        ("T2 primary", RT.t2(), None),
        ("T2 V_dead 0.4 uL", RT.t2(V_dead_uL=0.4), None),
        ("T2 packed-bed factor 3", RT.t2(bed_factor_key="ma.nsb.surface_factor_packed_bed"), None),
        ("T2 retainer 20 mm2", RT.t2(retainer_area=20e-6), None),
        ("T2 unit-to-unit CV bed 0.30", RT.t2(), pin(**{"tr.nsb.unit_to_unit_cv_bed": 0.30})),
        ("T2 impurity residual 0.05", RT.t2(), pin(**{"ma.noise.background_current_relative_noise": 0.05})),
        ("T2 retainer 20 mm2 + packed-bed factor 3",
         RT.t2(retainer_area=20e-6, bed_factor_key="ma.nsb.surface_factor_packed_bed"), None),
        ("T3 primary", RT.t3(), None),
        ("T3 transfer efficiency 0.49", RT.t3(), pin(**{"ma.design_levers.immune_complex_transfer_efficiency": 0.49})),
        ("T3 packed-bed factor 3", RT.t3(bed_factor_key="ma.nsb.surface_factor_packed_bed"), None),
        ("T3 impurity residual 0.05", RT.t3(), pin(**{"ma.noise.background_current_relative_noise": 0.05})),
    ]
    for lab, d, mod in rows:
        print(f"  {lab:50s} {nom(d, mod or (lambda p: p)):.3g}")
    # sampled keys per tier
    for lab, d in (("T1", RT.t1()), ("T2", RT.t2()), ("T3", RT.t3())):
        p = ps.with_values(d["ps_values"]) if d.get("ps_values") else ps
        probe = p.copy(); probe.accessed = set()
        (tk.evaluate_planar if d["tier"] == 1 else tk.evaluate_bed)(d, probe)
        keys = sorted(probe.accessed)
        samp = p.sampleable(keys)
        fixed = [k for k in keys if k not in samp]
        print(f"\n  {lab}: {len(samp)} sampled keys: {', '.join(samp)}")
        print(f"  {lab}: read but not sampled: {', '.join(fixed)}")


if __name__ == "__main__":
    main()
