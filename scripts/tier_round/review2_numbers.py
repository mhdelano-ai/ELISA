#!/usr/bin/env python3
"""Second-pass review of the numbers and physics of docs/30 Revision B (results/tier_round/review2_numbers.md).

Part A calls the kit (tierkit, run_tiers) only to reproduce the nominal results and to list the keys that the
Monte Carlo samples.  Part B recomputes each nominal chain from the raw parameter values with its own formulas
(slit solver, bed equation, labelling, Michaelis-Menten with product decay, blank terms, variance terms) and does
NOT use the kit's functions for those terms.  Part C estimates terms the kit does not count.

    python scripts/tier_round/review2_numbers.py          (about 1 min; writes nothing)
"""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))
warnings.simplefilter("ignore")
import review_numbers as RN  # noqa: E402  (raw YAML loader and the independent slit solver of round 1)
import run_tiers as RT  # noqa: E402
import tierkit as tk  # noqa: E402

NA, F = 6.02214076e23, 96485.33212
ULMIN, UL = 1e-9 / 60, 1e-9
P = dict(RN.P)
P["ma.chemistries.alp_hqdp.product_half_life"] = 600.0      # override of Revision B (run_tiers.base_params)


# ================================================================ Part A: the kit, nominal
def kit_nominal():
    ps = RT.base_params()
    out = {}
    for lab, d in (("T1", RT.t1()), ("T2", RT.t2()), ("T3", RT.t3()), ("T3 one valve", RT.t3(transfer=False))):
        p = ps.with_values(d["ps_values"]) if d.get("ps_values") else ps
        ev = tk.evaluate_planar if d["tier"] == 1 else tk.evaluate_bed
        r = ev(d, p)
        tot = sum(float(np.asarray(v, float)) for v in r.variance_terms.values())
        out[lab] = (r, d, p, ev)
        print(f"\n[kit] {lab}: LOD {float(r.lod_pgml):.4g} pg/mL, blank SD {float(r.blank_sd):.4g} C")
        print("   variance shares: " + ", ".join(f"{k} {float(np.asarray(v, float)) / tot:.3f}"
                                               for k, v in r.variance_terms.items()))
        for k, v in r.diagnostics.items():
            try:
                print(f"   {k:28s} {float(np.asarray(v, float).reshape(-1)[0]):.4g}")
            except Exception:
                pass
    js = json.load(open(ROOT / "results/tier_round/tiers.json"))["1. The three implementations, as specified"]
    for (lab, (r, *_)), (name, k) in zip(list(out.items())[:3], js.items()):
        print(f"[json] {lab}: nominal {k['lod_nominal']:.4g} vs kit now {float(r.lod_pgml):.4g}")
    return out


def mc_keys(kit):
    want = ["tr.transfer.elution_efficiency", "ma.design_levers.immune_complex_transfer_nsb_factor",
            "tr.noise.preread_residual_cv", "tr.noise.swept_step_residual_cv", "tr.noise.drift_area_exponent",
            "tr.nsb.surface_factor_gold_oeg", "tr.nsb.surface_factor_frit", "ma.nsb.surface_factor_tubing",
            "ma.nsb.surface_factor_packed_bed", "ma.chemistries.alp_hqdp.product_half_life",
            "tr.nsb.surface_factor_lid", "ma.timing.substrate_reservoir_age", "tr.nsb.unit_to_unit_cv_planar",
            "tr.nsb.unit_to_unit_cv_bed", "ma.noise.background_current_relative_noise"]
    print("\n[MC] sampled (S) / read but not sampled (r) / not read (-)")
    for lab in ("T1", "T2", "T3"):
        r, d, p, ev = kit[lab]
        s = tk.monte_carlo(ev, d, p, n=200, seed=1)
        samp = set(s["_keys"])
        probe = p.copy(); probe.accessed = set(); ev(d, probe)
        acc = probe.accessed
        print(f"  {lab}: n sampled {s['n_sampled_keys']}")
        for k in want:
            print(f"     {'S' if k in samp else ('r' if k in acc else '-')}  {k}")


# ================================================================ Part B: independent chains
M = P["chem.analyte.molar_mass"]
D_igg = P["chem.analyte.diffusion_coefficient"]
D_conj = P["chem.antibodies.diffusion_coefficient_IgG_ALP_conjugate"]
Gam = P["chem.surfaces.igg_surface_density_monolayer"] * P["chem.surfaces.active_fraction_oriented"] / NA
k_r = P["chem.antibodies.kon_capture"] * 1e-3 * Gam
kon_d = P["chem.antibodies.kon_detection"] * 1e-3
koff_d, koff_c = P["chem.antibodies.koff_detection"], P["chem.antibodies.koff_capture"]
k_nsb = (P["chem.nsb.nsb_effective_rate_constant"] * P["ma.nsb.label_factor_igg_enzyme_conjugate"]
         * P["ma.labelling.detection_on_capture_residual_factor"])
kcat, Km = P["chem.enzymes.alp.kcat_conjugate_assay_conditions"], P["ma.chemistries.alp_hqdp.Km"] * 1e3
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
pre_cv, step_cv = P["tr.noise.preread_residual_cv"], P["tr.noise.swept_step_residual_cv"]
N_VIAL = (1e-12 / 1e-6) / M * 100e-9 * NA          # molecules in 100 uL at 1 pg/mL
OVH = 1.0


def labelled(C_nM=10, V_uL=100, Q=50):
    C = C_nM * 1e-6; t = V_uL / Q * 60
    a = kon_d * C
    return a / (a + koff_d) * (1 - np.exp(-(a + koff_d) * t)), C * t


def noise_rms(area):
    i_ref = P["hw.gamry.noise_rms_flow"]
    i_ref = i_ref * 1e-12 if i_ref > 1e-6 else i_ref
    fl = P["hw.gamry.antec_decade_floor_pp"]
    fl = (fl * 1e-12 if fl > 1e-6 else fl) / P["ma.noise.pp_to_rms"]
    return max(fl, i_ref * (area / A_ref) ** P["ma.noise.area_exponent"])


def var_noise(area, T):
    i_n = noise_rms(area)
    return 2 * (i_n * np.sqrt(T / (2 * P["ma.noise.reference_bandwidth"]))) ** 2, i_n


def var_drift(area, T, T_span):
    dr = drift_ref / 60 * (area / A_ref) ** P["tr.noise.drift_area_exponent"]
    return (drift_res * 0.5 * dr * T_span * T) ** 2


def bed_product(N_enz, V, t_acc=420.0, S0=1.0, steps=6000, kdec=None):
    """Explicit Euler, Michaelis-Menten with competitive phosphate inhibition (1 Pi per product), first-order
    product decay; returns (enzyme product, hydrolysis product) in mol."""
    kdec = np.log(2) / t_half if kdec is None else kdec
    E = N_enz / NA / V
    Pe, Ph, S, formed, dt = 0.0, 0.0, S0, 0.0, t_acc / steps
    ppp = P["ma.chemistries.alp_hqdp.phosphate_per_product"]
    for _ in range(steps):
        r = kcat * E * S / (Km * (1 + ppp * formed / Ki) + S)    # phosphate does not decay with the product
        rh = khyd * S
        Pe += (r - kdec * Pe) * dt; Ph += (rh - kdec * Ph) * dt; S -= (r + rh) * dt; formed += (r + rh) * dt
    return Pe * V, Ph * V


def report(name, d, terms, slope):
    sd = np.sqrt(sum(terms.values())); tot = sum(terms.values())
    print(f"\n== {name}")
    for k, v in d.items():
        print(f"  {k:36s} {v:.4g}")
    print("  variance shares: " + ", ".join(f"{k} {v / tot:.3f}" for k, v in terms.items()))
    L = 3 * sd / slope
    print(f"  blank SD {sd:.4g} C; slope {slope:.4g} C per pg/mL; LOD {L:.4g} pg/mL")
    return L


def tier1(extra=None, imp_=imp, hyd_conc=None, verbose=True):
    """Tier 1 primary: AU10 strip, SPE cell h 0.2 mm, bore r 0.4 mm, 3 mm electrode; read 150 uL/min, 0.3 mM."""
    h, a, rb, Lb, R = 0.2e-3, 1.5e-3, 0.4e-3, 5e-3, 4e-3
    A_we = np.pi * a ** 2; s_we = np.pi * (a ** 2 - rb ** 2)
    Q = 3.0 * ULMIN; t_load = 42.0
    N_in = N_VIAL * f_del * (1 - loss) * 0.9789          # loop transfer from the kit (round 1: within 2 % of 1)
    Da = k_r * h / D_igg
    f_cap = RN.slit_conversion(D_igg * s_we / (Q * h), Da)
    N_cap = N_in * f_cap
    f_lab, expo = labelled()
    t_front = 215 / 150
    to_mid = t_front + 1.0
    t_label = (2.0 + 2.0 + to_mid) * 60                   # mid-conjugate (2 of 4 min) + wash 2 + to read middle
    t_cap = (0.5 * t_load + 1.5 + 1 + 4 + 2 + to_mid) * 60
    N_enz = N_cap * f_lab * np.exp(-koff_d * t_label) * np.exp(-koff_c * t_cap)
    S0 = 0.3
    v = kcat * S0 / (Km + S0)
    i_enz = v / NA * nF                                   # A per enzyme on the electrode
    T = 120.0
    slope = N_enz * i_enz * T
    pa = k_nsb * expo * NA
    N_we = pa * P["tr.nsb.surface_factor_gold_oeg"] * A_we
    Qr = 150 * ULMIN
    eta = RN.slit_conversion(D_hq * s_we / (Qr * h), np.inf)
    A_lid = np.pi * (R ** 2 - rb ** 2)
    N_lid = pa * P["tr.nsb.surface_factor_lid"] * A_lid
    lid_col = 0.5 * eta * s_we / A_lid
    N_bore = pa * P["tr.nsb.surface_factor_lid"] * 2 * np.pi * rb * Lb
    N_line = pa * P["ma.nsb.surface_factor_tubing"] * np.pi * 50e-6 * 0.15
    N_eff = N_we + N_lid * lid_col + (N_bore + N_line) * eta
    c_inj = P["hw.smfl.carryover_protein_conjugate"]
    N_carry = c_inj ** 2 * 10e-6 * 100e-9 * NA * (1 - np.exp(-k_nsb * 3 * A_we / Q))
    Qn = N_eff * i_enz * T; Qc = N_carry * i_enz * T
    c_hyd = khyd * S0 * age if hyd_conc is None else hyd_conc
    Qi = nF * eta * Qr * imp_ * S0 * T; Qh = nF * eta * Qr * c_hyd * T
    vn, i_n = var_noise(A_we, T)
    T_span = T + 2 * (t_front * 60 + 15)
    terms = dict(nsb=(cv_nsb ** 2 + P["tr.nsb.unit_to_unit_cv_planar"] ** 2 + inj ** 2) * Qn ** 2,
                 label_counting=(i_enz * T) ** 2 * (N_eff + N_carry),
                 carry=(P["ma.noise.carryover_cv"] * Qc) ** 2,
                 substrate=(cv_sub * Qh) ** 2 + (rel_bg * (Qi + Qh)) ** 2 + (pre_cv * (Qi + Qh)) ** 2,
                 sensitivity=(pre_cv * (Qn + Qc + Qh)) ** 2,
                 noise=vn, drift=var_drift(A_we, T, T_span))
    for k, val in (extra or {}).items():
        terms[k] = val(locals())
    d = dict(N_in=N_in, f_capture=f_cap, N_captured=N_cap, f_label=f_lab, ret_label=np.exp(-koff_d * t_label),
             ret_capture=np.exp(-koff_c * t_cap), enzymes=N_enz, i_per_pgml_pA=N_enz * i_enz * 1e12,
             eta_150=eta, N_nsb_we=N_we, N_bore=N_bore, N_line=N_line, N_lid=N_lid,
             upstream_equiv_pgml=(N_bore + N_line) * eta / N_enz, we_equiv_pgml=N_we / N_enz,
             i_imp_pA=Qi / T * 1e12, i_hyd_pA=Qh / T * 1e12, blank_equiv_pgml=(Qn + Qc + Qh) / slope,
             noise_pA=i_n * 1e12, T_span_s=T_span)
    L = report("tier 1 nominal (independent)", d, terms, slope) if verbose else 3 * np.sqrt(sum(terms.values())) / slope
    return L, locals()


def bed_capture(Q, D, A_bed, col=200e-6, eps=0.4, dp=2.8e-6):
    u = Q / (np.pi * (col / 2) ** 2); nu = P["ma.fluid.viscosity"] / P["ma.fluid.density"]
    Re, Sc = u * dp / nu, nu / D
    km = P["ma.correlations.wilson_geankoplis_coefficient"] / eps * u * Re ** (-2 / 3) * Sc ** (-2 / 3)
    return 1 - np.exp(-A_bed / Q / (1 / km + 1 / k_r)), km


def tier_bed(tier=2, transfer=True, verbose=True, extra=None, kdec=None, imp_=imp):
    eps, dp, V_bed, col = 0.4, 2.8e-6, 0.019e-9, 200e-6
    A_bed = 6 * (1 - eps) / dp * V_bed
    if tier == 2:
        Q, t_load, t_extra, t_down = 3.4 * ULMIN, 37.0, 0.0, 1.0
        bore_mm, cap_mm, line_area = 1.0, 20.0, np.pi * 50e-6 * 0.15
        sigma = 1.0e-9
    else:
        Q, t_load, t_down = 5.0 * ULMIN, 25.0, 0.0
        t_extra = (OVH + 0.5 + 5 + 8 / 2 + 2) if transfer else 0.0
        bore_mm, cap_mm, line_area = 0.0, 0.0, 10e-6
        sigma = 1.5e-9
    N_in = N_VIAL * f_del * (1 - loss) * 0.9827
    f_bed, km = bed_capture(Q, D_igg, A_bed)
    N_cap = N_in * f_bed
    f_lab, expo = labelled()
    t_fill = 215 / 80
    after_conj = (2.0 + t_extra + t_fill + t_down) * 60
    t_label = 2.0 * 60 + after_conj
    t_cap = 0.5 * t_load * 60 + (1.5 + 1 + 4) * 60 + after_conj
    N_enz = N_cap * f_lab * np.exp(-koff_d * t_label) * np.exp(-koff_c * t_cap)
    pa = k_nsb * expo * NA
    rb = 0.4e-3
    N_beads = pa * P["ma.nsb.surface_factor_packed_bed"] * A_bed
    N_frit = pa * P["tr.nsb.surface_factor_frit"] * 5e-6
    N_bore = pa * P["tr.nsb.surface_factor_lid"] * 2 * np.pi * rb * bore_mm * 1e-3
    N_up = pa * P["ma.nsb.surface_factor_tubing"] * (np.pi * col * cap_mm * 1e-3 + line_area)
    recap, f_tr = 1.0, 1.0
    if tier == 3 and transfer:
        recap, _ = bed_capture(2.0 * ULMIN, D_conj, A_bed)
        f_tr = P["tr.transfer.elution_efficiency"] * recap
        fn = P["ma.design_levers.immune_complex_transfer_nsb_factor"]
        N_enz *= f_tr; N_beads *= fn; N_frit *= fn; N_bore *= fn; N_up *= fn
    N_nsb = N_beads + N_frit + N_bore + N_up
    c_inj = P["hw.smfl.carryover_protein_conjugate"]
    N_carry = c_inj ** 2 * 10e-6 * 100e-9 * NA * (1 - np.exp(-k_nsb * P["ma.nsb.surface_factor_packed_bed"] * A_bed / Q))
    V_acc = eps * V_bed + 0.1e-9
    S0 = 1.0
    n_b, n_h = bed_product(N_nsb + N_carry, V_acc, kdec=kdec)
    n_t, _ = bed_product(N_nsb + N_carry + N_enz, V_acc, kdec=kdec)
    a, h = 1.5e-3, 0.2e-3
    s = np.pi * (a ** 2 - rb ** 2); Qr = 5 * ULMIN; T = 90.0
    eta = RN.slit_conversion(D_hq * s / (Qr * h), np.inf)
    # elution of the plug in the read window: tanks in series n_eff, own gamma CDF
    from scipy.stats import gamma as G
    n_eff = V_acc ** 2 / (V_acc ** 2 / 3 + sigma ** 2)
    eluted = G.cdf(Qr * T / V_acc * n_eff, n_eff)
    q = nF * eta * eluted
    slope = q * (n_t - n_b)
    Qb = q * n_b; Qn = Qb * N_nsb / (N_nsb + N_carry); Qc = Qb - Qn
    Qh = q * n_h
    Qi = nF * eta * Qr * imp_ * S0 * T
    vn, i_n = var_noise(np.pi * a ** 2, T)
    i_enz = Qb / (N_nsb + N_carry)
    terms = dict(nsb=(cv_nsb ** 2 + P["tr.nsb.unit_to_unit_cv_bed"] ** 2 + inj ** 2) * Qn ** 2,
                 label_counting=i_enz ** 2 * (N_nsb + N_carry),
                 carry=(P["ma.noise.carryover_cv"] * Qc) ** 2,
                 substrate=(cv_sub * Qh) ** 2 + (rel_bg * (Qi + Qh)) ** 2 + ((step_cv * Qi) ** 2 if tier == 2 else 0),
                 sensitivity=(pre_cv * (Qn + Qc + Qh)) ** 2,
                 noise=vn, drift=var_drift(np.pi * a ** 2, T, T))
    for k, val in (extra or {}).items():
        terms[k] = val(locals())
    d = dict(N_in=N_in, f_bed=f_bed, k_m=km, N_captured=N_cap, f_label=f_lab, ret_label=np.exp(-koff_d * t_label),
             ret_capture=np.exp(-koff_c * t_cap), recapture=recap, transfer=f_tr, enzymes=N_enz, N_beads=N_beads,
             N_frit=N_frit, N_bore=N_bore, N_up=N_up, eta_5=eta, eluted=eluted, n_eff=n_eff,
             signal_nC_per_pgml=slope * 1e9, blank_equiv_pgml=(Qn + Qc + Qh) / slope, i_imp_pA=Qi / T * 1e12,
             blank_peak_mean_pA=Qb / T * 1e12, A_bed_mm2=A_bed * 1e6)
    name = f"tier {tier}{'' if transfer or tier == 2 else ' one valve'} nominal (independent)"
    L = report(name, d, terms, slope) if verbose else 3 * np.sqrt(sum(terms.values())) / slope
    return L, locals()


if __name__ == "__main__":
    kit = kit_nominal()
    if "--no-mc" not in sys.argv:
        mc_keys(kit)
    L1, v1 = tier1()
    L2, v2 = tier_bed(2)
    L3, v3 = tier_bed(3)
    L3b, v3b = tier_bed(3, transfer=False)
    for lab, L, k in (("T1", L1, "T1"), ("T2", L2, "T2"), ("T3", L3, "T3"), ("T3 one valve", L3b, "T3 one valve")):
        Lk = float(kit[k][0].lod_pgml)
        print(f"[agreement] {lab}: independent {L:.4g} vs kit {Lk:.4g} ({100 * (L / Lk - 1):+.1f} %)")


# ================================================================ Part C: terms the kit does not count
def part_c():
    print("\n================ Part C")
    # fact 5 of docs/30 section 1: stream conversion of the 3 mm electrode under a 0.2 mm gap
    s = np.pi * (1.5e-3 ** 2 - 0.4e-3 ** 2)
    for q in (1, 5, 150):
        print(f"  eta(HQ) at {q} uL/min: {RN.slit_conversion(D_hq * s / (q * ULMIN * 0.2e-3), np.inf):.4f}")

    # (a) tier 1: bore-wall product enters the gap along the lid; diffusion length during the passage over the
    # electrode at 150 uL/min against the 0.2 mm gap
    t_pass = s * 0.2e-3 / (150 * ULMIN)
    t_bore = np.pi * 0.4e-3 ** 2 * 5e-3 / (150 * ULMIN)
    print(f"  (a) passage over the electrode {t_pass:.2f} s: diffusion length {np.sqrt(2 * D_hq * t_pass) * 1e6:.0f} um"
          f" (gap 200 um); bore residence {t_bore:.2f} s: {np.sqrt(2 * D_hq * t_bore) * 1e6:.0f} um (bore radius 400 um)")
    L0, v = tier1(verbose=False)
    L_nobore, _ = tier1(verbose=False, extra=None)
    v_ = dict(v)
    # LOD without the bore term: rebuild with N_bore -> 0 through a correction of Qn in the nsb terms
    Qb = v["N_bore"] * v["eta"] * v["i_enz"] * v["T"]
    def nob(vv):
        return -((cv_nsb ** 2 + P["tr.nsb.unit_to_unit_cv_planar"] ** 2 + inj ** 2) * (vv["Qn"] ** 2 - (vv["Qn"] - Qb) ** 2))
    L_a, _ = tier1(verbose=False, extra=dict(nobore=nob))
    print(f"  (a) bore product share of tier-1 non-specific charge {Qb / v['Qn']:.3f}; LOD {L0:.3g} -> {L_a:.3g} without it")

    # (b) tier 1: background-current difference between buffer A1 (pH 7.5) and substrate buffer B1 (pH 9.5), not
    # removed by the pre-run beyond the same 3 % residual.  Break-even step and LOD for assumed steps.
    slope, sd = v["slope"], np.sqrt(sum(v["terms"].values()))
    print(f"  (b) break-even matrix step (3 % residual equals the present blank SD): {sd / (pre_cv * v['T']) * 1e12:.0f} pA")
    for di in (30e-12, 100e-12, 300e-12, 1e-9):
        L, _ = tier1(verbose=False, extra=dict(matrix=lambda vv, d=di: (pre_cv * d * vv["T"]) ** 2))
        print(f"      matrix step {di * 1e12:.0f} pA: LOD {L:.3g} pg/mL")
    # hydrolysis grows with reservoir age between the pre-run and the read (about 55 min later)
    print(f"  (b) hydrolysis current at age {age / 3600:.1f} h: {v['Qh'] / v['T'] * 1e12:.3g} pA; "
          f"growth over 55 min: {v['Qh'] / v['T'] * 55 * 60 / age * 1e12:.2f} pA "
          f"(= {v['Qh'] * 55 * 60 / age / slope:.2f} pg/mL equivalent, systematic)")

    # (e) half-life 600 s applied to the substrate reservoir: free HQ impurity decays, hydrolysis product is at
    # its steady state k_hyd S0 / k_dec instead of k_hyd S0 age
    kd = np.log(2) / t_half
    print(f"  (e) impurity left after {age / 3600:.1f} h at t1/2 {t_half:.0f} s: {np.exp(-kd * age):.2e} of 1e-5")
    L_e, ve = tier1(verbose=False, imp_=imp * np.exp(-kd * age), hyd_conc=khyd * 0.3 / kd)
    print(f"  (e) tier 1 with the reservoir obeying the same half-life: LOD {L_e:.3g} pg/mL "
          f"(background {ve['Qi'] / 120 * 1e12 + ve['Qh'] / 120 * 1e12:.3g} pA)")
    L_e2, _ = tier1(verbose=False, imp_=imp, hyd_conc=khyd * 0.3 / kd)
    print(f"  (e) tier 1 with impurity kept, hydrolysis at steady state only: LOD {L_e2:.3g} pg/mL")
    L2e, _ = tier_bed(2, verbose=False, imp_=imp * np.exp(-kd * age))
    L3e, _ = tier_bed(3, verbose=False, imp_=imp * np.exp(-kd * age))
    print(f"  (e) tiers 2 / 3 with the reservoir impurity decayed: {L2e:.3g} / {L3e:.3g}")
    L2n, _ = tier_bed(2, verbose=False, kdec=np.log(2) / 7200)
    L3n, _ = tier_bed(3, verbose=False, kdec=np.log(2) / 7200)
    print(f"  (e) tiers 2 / 3 with the model's 7200 s half-life: {L2n:.3g} / {L3n:.3g}")
    print(f"  (e) mean survival of product over a 420 s stop at 600 s: {(1 - np.exp(-kd * 420)) / (kd * 420):.3f}")
    # tier 3: free HQ in the closed loop of bed 2 decays during the 7 min while the stream outside does not
    for Vl in (0.5e-9, 1.0e-9, 2.0e-9):
        dip = nF * 0.62 * imp * 1.0 * (1 - np.exp(-kd * 420)) * Vl
        print(f"      tier 3 loop {Vl * 1e9:.1f} uL: baseline dip {dip * 1e9:.3g} nC "
              f"(signal 0.93 nC per pg/mL, blank SD 0.19 nC)")

    # (c) tier 2: steady current of the electrode's own conjugate and of the lid above it, not in the pre-run trace
    _, v2 = tier_bed(2, verbose=False)
    pa = v2["pa"]
    i_e = kcat * 1.0 / (Km + 1.0) / NA * nF
    N_el = pa * P["tr.nsb.surface_factor_printed_electrode"] * np.pi * 1.5e-3 ** 2
    N_lid = pa * P["tr.nsb.surface_factor_lid"] * s * 0.5 * v2["eta"]
    Q_el = (N_el + N_lid) * i_e * 90
    print(f"  (c) tier 2 electrode NSB {N_el:.3g} + lid-equivalent {N_lid:.3g} enzymes: {(N_el + N_lid) * i_e * 1e12:.3g} pA,"
          f" {Q_el * 1e9:.3g} nC in the read (kit Q_nsb {v2['Qn'] * 1e9:.3g} nC)")
    cvp2 = cv_nsb ** 2 + P["tr.nsb.unit_to_unit_cv_planar"] ** 2
    L2c, _ = tier_bed(2, verbose=False, extra=dict(el=lambda vv: cvp2 * Q_el ** 2 + (pre_cv * Q_el) ** 2))
    print(f"  (c) tier 2 with it counted (planar CV): LOD {L2c:.3g} pg/mL (kit-equivalent {tier_bed(2, verbose=False)[0]:.3g})")
    # walls above the bed: product per enzyme in the dilute wall volume vs in the bed's accumulation volume
    n_in_bed = bed_product(v2["N_up"], v2["V_acc"])[0]
    n_in_wall = bed_product(v2["N_up"], np.pi * 1e-4 ** 2 * 0.02 + np.pi * 25e-6 ** 2 * 0.15)[0]
    n_alone = bed_product(v2["N_up"], v2["V_acc"] * 1e6)[0]
    n_bed_all = bed_product(v2["N_nsb"] + v2["N_carry"], v2["V_acc"])[0] / (v2["N_nsb"] + v2["N_carry"]) * v2["N_up"]
    print(f"  (c) product of the walls above the bed: kit (inhibited with the bed blank) {n_bed_all:.3g} mol; in the "
          f"wall volume {n_in_wall:.3g} mol; uninhibited {n_alone:.3g} mol")
    # product made during the 90 s sweep (bed in flow, fresh substrate), arriving inside the window
    r = (v2["N_nsb"] + v2["N_carry"]) * kcat / (Km + 1.0) / NA
    print(f"  (c,d) product made during the sweep relative to the stop: {r * 88 / bed_product(v2['N_nsb'] + v2['N_carry'], v2['V_acc'])[0]:.2f}")

    # (d) tier 3: steady currents under flow counted like the free-HQ current (1 % of the background charge)
    _, v3 = tier_bed(3, verbose=False)
    N_bore3 = pa * P["tr.nsb.surface_factor_lid"] * 2 * np.pi * 0.4e-3 * 5e-3
    for extra_up in (0.0, 1e4, 5e4):
        i_st = (N_el + 0.62 * (N_bore3 + extra_up)) * i_e
        L3d, _ = tier_bed(3, verbose=False,
                          extra=dict(substrate=lambda vv, q=i_st * 90: (cv_sub * vv["Qh"]) ** 2
                                     + (rel_bg * (vv["Qi"] + vv["Qh"] + q)) ** 2))
        print(f"  (d) tier 3 steady enzyme current {i_st * 1e12:.3g} pA (upstream extra {extra_up:.0e}): LOD {L3d:.3g}")
    # bed-2 capacity: plug-flow bed with site depletion, 8 uL eluate at 2 uL/min
    A_bed = v3["A_bed"]
    sites_model = P["chem.surfaces.igg_surface_density_monolayer"] * P["chem.surfaces.active_fraction_oriented"] * A_bed
    _, km2 = bed_capture(2.0 * ULMIN, D_conj, A_bed)
    print(f"  (d) capture antibody on bed 1: model {P['chem.surfaces.igg_surface_density_monolayer'] * A_bed:.3g} "
          f"(active {sites_model:.3g}); vendor 10 ug/mg x 15 ug beads / 110 kDa = {0.15e-6 / 110e3 * NA:.3g}")
    for load, cap in ((0.7 * 2.44e11, 2.08e11), (0.7 * 8.2e11, 2.08e11), (0.7 * 8.2e11, 8.2e11 * 0.85),
                      (0.7 * 2.44e11, 3 * 2.08e11)):
        rec = capacity_recovery(load, cap, A_bed, km2, 8e-9, 2.0 * ULMIN)
        print(f"      load {load:.2g}, bed-2 sites {cap:.2g} (ratio {cap / load:.2f}): recovery {rec:.3f} "
              f"(first order 0.951)")

    # (f) elution in the 7.5 uL window: Gaussian of SD sigma centred at the transit volume
    from scipy.stats import norm
    for sig, Vt in ((1.0, 0.6), (1.5, 1.5), (1.5, 3.0)):
        print(f"  (f) sigma {sig} uL, peak at {Vt} uL: fraction in 7.5 uL {norm.cdf((7.5 - Vt) / sig) - norm.cdf(-Vt / sig):.3f}"
              f" (kit n_eff {v2['n_eff']:.3g} tanks)")


def capacity_recovery(load, sites, A_bed, km, V_el, Q, n=200, nt=4000):
    """Plug-flow bed of n slices; eluate of volume V_el with `load` molecules fed at Q; local flux per area
    C / (1/k_m + 1/(kon Gamma_free)); returns the fraction captured (complexes follow the same fraction)."""
    kon = P["chem.antibodies.kon_capture"] * 1e-3
    a = A_bed / n
    G = np.full(n, sites / A_bed / NA)              # free sites mol/m^2
    C_in = load / NA / V_el
    t_end = V_el / Q
    dt = t_end / nt
    cap = 0.0
    for _ in range(nt):
        C = C_in
        for i in range(n):
            kt = 1.0 / (1.0 / km + 1.0 / max(kon * G[i], 1e-30))
            f = 1.0 - np.exp(-kt * a / Q)
            flux = C * Q * f                         # mol/s captured in slice
            dG = min(flux * dt / a, G[i])
            G[i] -= dG
            cap += dG * a
            C = C * (1 - f)
    return cap * NA / load


if __name__ == "__main__":
    part_c()


def corrected():
    """Reviewer's corrected nominal estimates (Part D)."""
    print("\n================ Part D: corrected nominal estimates")
    kd = np.log(2) / t_half
    # tier 1: (i) bore-wall product not collected; (ii) matrix step of 100 pA between A1 and B1 at 3 % residual
    _, v = tier1(verbose=False)
    Qb = v["N_bore"] * v["eta"] * v["i_enz"] * v["T"]
    cvp = cv_nsb ** 2 + P["tr.nsb.unit_to_unit_cv_planar"] ** 2 + inj ** 2
    nob = lambda vv: -cvp * (vv["Qn"] ** 2 - (vv["Qn"] - Qb) ** 2)
    for lab, kw, ms in (("as kit, bore removed", {}, 0.0), ("bore removed, matrix step 100 pA", {}, 100e-12),
                        ("reservoir obeys t1/2 600 s, bore removed", dict(imp_=imp * np.exp(-kd * age),
                                                                         hyd_conc=khyd * 0.3 / kd), 0.0),
                        ("reservoir t1/2 600 s, bore removed, matrix step 100 pA", dict(imp_=imp * np.exp(-kd * age),
                                                                                      hyd_conc=khyd * 0.3 / kd), 100e-12)):
        L, _ = tier1(verbose=False, extra=dict(nobore=nob, matrix=lambda vv, d=ms: (pre_cv * d * vv["T"]) ** 2), **kw)
        print(f"  T1 {lab}: {L:.3g}")
    # tier 3: bed-2 capacity at the model's site density (recovery 0.83 instead of 0.951), steady enzyme currents
    # counted like the free-HQ current, tail of the plug through the 5 mm bore (7 % outside the window), product
    # made during the sweep (+28 % of signal and of the bed blank)
    _, v3 = tier_bed(3, verbose=False)
    pa = v3["pa"]
    i_e = kcat / (Km + 1.0) / NA * nF
    N_el = pa * P["tr.nsb.surface_factor_printed_electrode"] * np.pi * 1.5e-3 ** 2
    N_bore3 = pa * P["tr.nsb.surface_factor_lid"] * 2 * np.pi * 0.4e-3 * 5e-3
    q_st = (N_el + 0.62 * N_bore3) * i_e * 90
    t = v3["terms"]
    for lab, cap, tail, sweep, steady in (("capacity only", 0.83 / 0.951, 1.0, 1.0, 0.0),
                                          ("capacity + steady currents", 0.83 / 0.951, 1.0, 1.0, q_st),
                                          ("capacity + steady + tail 7 %", 0.83 / 0.951, 0.93, 1.0, q_st),
                                          ("all four (incl. sweep product +28 %)", 0.83 / 0.951, 0.93, 1.28, q_st)):
        g = tail * sweep                              # scales the plug: signal and bed blank
        var = (t["nsb"] + t["label_counting"] + t["carry"] + t["sensitivity"]) * g ** 2 + t["noise"] + t["drift"] \
            + (cv_sub * v3["Qh"]) ** 2 + (rel_bg * (v3["Qi"] + v3["Qh"] + steady)) ** 2
        L = 3 * np.sqrt(var) / (v3["slope"] * cap * g)
        print(f"  T3 {lab}: {L:.3g}")


if __name__ == "__main__":
    corrected()
