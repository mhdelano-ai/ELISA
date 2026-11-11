"""Common interface: evaluate one architecture for one parameter set (scalar or Monte Carlo arrays).

    result = evaluate(arch, ps)

returns a :class:`Result` with the calibration curve, signal, blank mean, blank SD, LOD, dynamic range,
cycle time and a breakdown of the blank variance (which term limits the LOD), plus intermediate
diagnostics.  All quantities are SI internally; reported concentrations are in pg/mL.

Signal chain (docs/03 section 3):  sample delivery -> capture -> retention -> labelling -> enzyme
turnover in the accumulation volume (or continuous flow) -> transfer to the electrode -> charge.
Blank chain: conjugate NSB on every surface the product can reach + carry-over + substrate background +
electrochemical noise/drift + (optional) environmental IgG contamination.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from . import constants as K
from . import kinetics as kin
from . import transport as tr
from .architectures import Architecture, CHEMISTRIES, INJECTIONS, check
from .params import ParameterSet
from .units import convert
from .timing import cycle_timeline

NA = K.AVOGADRO
FARADAY = K.FARADAY


class Ctx:
    """Parameter accessor that reshapes Monte Carlo arrays to (n, 1) so they broadcast against the
    calibration grid (nc,)."""

    def __init__(self, ps: ParameterSet):
        self.ps = ps
        self.n = ps.n

    def __call__(self, key, unit):
        v = self.ps.get(key, unit)
        if isinstance(v, np.ndarray) and v.ndim == 1 and self.n:
            return v.reshape(-1, 1)
        return v


@dataclass
class Result:
    arch: Architecture
    conc_pgml: np.ndarray                 # calibration grid (nc,), first entry 0 (blank)
    net_signal: np.ndarray                # (n, nc) or (nc,) net charge above blank, C
    blank_mean: np.ndarray                # C
    blank_sd: np.ndarray                  # C
    lod_pgml: np.ndarray                  # mean blank + k SD through the calibration curve
    lod_slope_pgml: np.ndarray            # k SD / low-end slope
    uloq_pgml: np.ndarray
    dynamic_range_decades: np.ndarray
    cycle_time_min: float
    time_to_result_min: float
    variance_terms: dict                  # term -> variance (C^2)
    diagnostics: dict = field(default_factory=dict)

    @property
    def limiting_term(self):
        names = list(self.variance_terms)
        stack = np.stack([np.broadcast_to(np.asarray(self.variance_terms[k], float), np.shape(self.blank_sd))
                          for k in names])
        idx = np.argmax(stack, axis=0)
        return np.asarray(names, dtype=object)[idx]

    def variance_fractions(self):
        tot = sum(np.asarray(v, float) for v in self.variance_terms.values())
        return {k: np.asarray(v, float) / tot for k, v in self.variance_terms.items()}


# ----------------------------------------------------------------------------------------------------
# capture geometries
# ----------------------------------------------------------------------------------------------------
def _gamma_sites(p, arch):
    """Active capture-antibody surface density, mol/m^2 (oriented immobilisation assumed)."""
    dens = p("chem.surfaces.igg_surface_density_monolayer", "molecules/m^2")
    act = p("chem.surfaces.active_fraction_oriented", "fraction")
    return dens * act / NA


def _flow_capture(kind, p, arch, Q, N_in, gamma, kon, D):
    """Single-pass capture fraction with transport + kinetics + site saturation (fixed-point iteration)."""
    iters = int(p("ma.numerics.capture_saturation_iterations", "count"))
    geo = _reactor_geometry(kind, p, arch)
    A = geo["A_capture"]
    f = np.zeros(np.broadcast(N_in, gamma).shape)
    for _ in range(iters):
        occ = np.minimum(f * N_in / NA / (gamma * A), 0.999)
        k_r = kon * gamma * (1.0 - occ)                      # m/s
        if kind in ("packed_bed", "chip_bead_bed"):
            u_s = Q / (np.pi * (0.5 * geo["column_id"]) ** 2)
            k_m, Re = tr.wilson_geankoplis_k(D, geo["d_p"], geo["eps"], u_s, geo["nu"], geo["wg"])
            k_tot = 1.0 / (1.0 / k_m + 1.0 / k_r)
            f = 1.0 - np.exp(-k_tot * A / Q)
        elif kind == "monolith":
            r = 0.5 * geo["d_ch"]
            n_ch = geo["V_void"] / (np.pi * r ** 2 * geo["L"])
            xi = np.pi * geo["L"] * D * n_ch / Q
            f = tr.conversion("tube", xi, k_r * r / D)
        elif kind == "capillary":
            r = 0.5 * geo["d"]
            xi = np.pi * geo["L"] * D / Q
            f = tr.conversion("tube", xi, k_r * r / D)
        elif kind == "chip_planar":
            H, w, L = geo["H"], geo["w"], geo["L_cap"]
            xi = L * D * w / (Q * H)
            f = tr.conversion("slit", xi, k_r * H / D)
        else:
            raise ValueError(kind)
    return f, geo


def _reactor_geometry(kind, p, arch):
    g = {"nu": p("ma.fluid.viscosity", "Pa*s") / p("ma.fluid.density", "kg/m^3")}
    g["wg"] = p("ma.correlations.wilson_geankoplis_coefficient", "dimensionless")
    tube_d = p("hw.tubing.id_standard", "m")
    conn_L = p("ma.geometry.reactor_connection_length", "m")
    g["A_tubing_isolated"] = np.pi * tube_d * conn_L      # tubing sealed with the reactor (Scheme B)
    g["sf_tubing"] = p("ma.nsb.surface_factor_tubing", "fold")
    if kind == "packed_bed":
        V = p("hw.reactors.packed_microbed_10uL.bed_volume", "m^3")
        eps = p("hw.reactors.packed_microbed_10uL.void_fraction", "fraction")
        d_p = p("hw.reactors.packed_microbed_10uL.bead_diameter", "m")
        g.update(V_bed=V, eps=eps, d_p=d_p, column_id=p("ma.geometry.packed_bed_column_inner_diameter", "m"))
        g["A_capture"] = 6.0 * (1.0 - eps) / d_p * V
        g["V_acc"] = eps * V
        g["A_nsb"] = g["A_capture"] * p("ma.nsb.surface_factor_packed_bed", "fold")
        g["tanks"] = p("ma.readout.tanks_packed_bed", "tanks")
    elif kind == "chip_bead_bed":
        V = p("ma.geometry.chip_bead_bed_volume", "m^3")
        eps = p("hw.reactors.packed_microbed_10uL.void_fraction", "fraction")
        d_p = p("hw.reactors.packed_microbed_10uL.bead_diameter", "m")
        H = p("ma.geometry.chip_channel_height", "m")
        w = p("ma.geometry.chip_channel_width", "m")
        Lch = p("ma.geometry.chip_channel_length", "m")
        g.update(V_bed=V, eps=eps, d_p=d_p, column_id=p("ma.geometry.chip_bead_bed_inner_diameter", "m"))
        g["A_capture"] = 6.0 * (1.0 - eps) / d_p * V
        g["V_acc"] = eps * V + H * w * Lch
        g["A_nsb"] = (g["A_capture"] * p("ma.nsb.surface_factor_packed_bed", "fold")
                      + 2.0 * w * Lch * p("ma.nsb.surface_factor_chip", "fold"))
        g["A_tubing_isolated"] = 0.0 * g["A_tubing_isolated"]
        g["tanks"] = p("ma.readout.tanks_packed_bed", "tanks")
    elif kind == "monolith":
        V = p("hw.reactors.monolith_cimac_100uL.bed_volume", "m^3")
        eps = p("hw.reactors.monolith_cimac_100uL.void_fraction", "fraction")
        d_ch = p("ma.geometry.monolith_channel_diameter", "m")
        D_col = p("ma.geometry.monolith_diameter", "m")
        g.update(V_bed=V, eps=eps, d_ch=d_ch, V_void=eps * V, L=V / (np.pi * (0.5 * D_col) ** 2))
        g["A_capture"] = 4.0 * eps * V / d_ch
        g["V_acc"] = eps * V
        g["A_nsb"] = g["A_capture"] * p("ma.nsb.surface_factor_monolith", "fold")
        g["tanks"] = p("ma.readout.tanks_monolith", "tanks")
    elif kind == "capillary":
        d = p("ma.geometry.capillary_inner_diameter", "m")
        L = p("ma.geometry.capillary_length", "m")
        g.update(d=d, L=L)
        g["A_capture"] = np.pi * d * L
        g["V_acc"] = np.pi * (0.5 * d) ** 2 * L
        g["A_nsb"] = g["A_capture"] * p("ma.nsb.surface_factor_capillary", "fold")
        g["tanks"] = p("ma.readout.tanks_capillary", "tanks")
    elif kind == "chip_planar":
        H = p("ma.geometry.chip_channel_height", "m")
        w = p("ma.geometry.chip_channel_width", "m")
        Lc = p("ma.geometry.chip_capture_length", "m")
        Lch = p("ma.geometry.chip_channel_length", "m")
        g.update(H=H, w=w, L_cap=Lc)
        g["A_capture"] = w * Lc
        g["V_acc"] = H * w * Lch
        g["A_nsb"] = 2.0 * w * Lch * p("ma.nsb.surface_factor_chip", "fold")
        g["A_tubing_isolated"] = 0.0 * g["A_tubing_isolated"]
        g["tanks"] = 1.0
    elif kind == "magnetic_beads":
        d_b = p("ma.geometry.magnetic_bead_diameter", "m")
        V_trap = p("ma.geometry.magnetic_trap_volume", "m^3")
        d_t = p("ma.geometry.magnetic_trap_tube_inner_diameter", "m")
        L_t = V_trap / (np.pi * (0.5 * d_t) ** 2)
        g.update(d_b=d_b)
        g["V_acc"] = V_trap
        g["A_trap_wall"] = np.pi * d_t * L_t
        g["tanks"] = p("ma.readout.tanks_trap", "tanks")
    else:
        raise ValueError(kind)
    return g


# ----------------------------------------------------------------------------------------------------
# detection
# ----------------------------------------------------------------------------------------------------
def _detector(arch, p, D_prod, Q):
    """Return dict: conversion (charge per mol product passing, as fraction of nF), electrode area,
    reference noise, and for ida_chip the current per concentration."""
    det = arch.detector
    out = {}
    if det == "thin_layer":
        A_we = p("hw.flow_cells.thin_layer_basi.we_area", "m^2")
        side = np.sqrt(A_we)
        out["eta"] = tr.thin_layer_conversion(D_prod, side, side,
                                              p("hw.flow_cells.thin_layer_basi.channel_height", "m"),
                                              p("ma.geometry.thin_layer_channel_width", "m"), Q)
        out["area"] = A_we
    elif det in ("wall_jet_sencell", "wall_jet_spe"):
        key = ("hw.flow_cells.antec_sencell.we_diameter" if det == "wall_jet_sencell"
               else "hw.flow_cells.dropsens_spe_walljet.we_diameter")
        R = 0.5 * p(key, "m")
        nu = p("ma.fluid.viscosity", "Pa*s") / p("ma.fluid.density", "kg/m^3")
        out["eta"] = tr.wall_jet_conversion(D_prod, nu, p("ma.geometry.walljet_nozzle_diameter", "m"), R, Q,
                                            p("ma.detection.walljet_coefficient", "dimensionless"))
        out["area"] = np.pi * R ** 2
    elif det == "coulometric":
        out["eta"] = p("hw.flow_cells.thermo_6011rs_coulometric.collection_efficiency", "fraction")
        out["area"] = p("ma.geometry.coulometric_effective_area", "m^2")
    elif det == "ida_flow":
        H = p("ma.geometry.chip_channel_height", "m")
        w_ch = p("ma.geometry.chip_channel_width", "m")
        L = p("ma.geometry.ida_flow_cell_length", "m")
        gen = tr.thin_layer_conversion(D_prod, L, w_ch, H, w_ch, Q)
        out["eta"] = gen * p("hw.flow_cells.ida_redox_cycling.amplification", "fold")
        m = p("ma.geometry.ida_finger_pairs", "count")
        out["area"] = m * w_ch * p("ma.geometry.ida_finger_width", "m")
    elif det == "ida_chip":
        m = p("ma.geometry.ida_finger_pairs", "count")
        b = p("ma.geometry.ida_finger_length_chip", "m")
        wf = p("ma.geometry.ida_finger_width", "m")
        gap = p("hw.flow_cells.ida_redox_cycling.gap", "m")
        out["i_per_conc_per_ne"] = tr.aoki_ida_current_per_conc(
            1.0, D_prod, m, b, wf, gap, p("ma.detection.aoki_c1", "dimensionless"),
            p("ma.detection.aoki_c2", "dimensionless"), p("ma.detection.aoki_c3", "dimensionless")) \
            * p("ma.detection.ida_stopped_efficiency", "fraction")
        out["area"] = m * b * wf
    else:
        raise ValueError(det)
    return out


# ----------------------------------------------------------------------------------------------------
# main evaluation
# ----------------------------------------------------------------------------------------------------
def calibration_grid(p):
    n = int(p("ma.numerics.calibration_points", "count"))
    lo = p("ma.numerics.calibration_min", "pg/mL")
    hi = p("ma.numerics.calibration_max", "pg/mL")
    return np.concatenate([[0.0], np.geomspace(lo, hi, n)])


def apply_design(arch: Architecture, ps: ParameterSet) -> ParameterSet:
    return ps.with_values(dict(arch.design)) if arch.design else ps


def evaluate(arch: Architecture, ps: ParameterSet, conc_pgml: np.ndarray | None = None) -> Result:
    problems = check(arch)
    if problems:
        raise ValueError(f"{arch.name}: " + "; ".join(problems))
    ps = apply_design(arch, ps)
    p = Ctx(ps)
    chem = CHEMISTRIES[arch.chemistry]
    conc = calibration_grid(p) if conc_pgml is None else np.asarray(conc_pgml, float)
    if conc[0] != 0.0:
        conc = np.concatenate([[0.0], conc])
    tl = cycle_timeline(arch, p)                      # minutes, dict of step durations and windows (s)

    # ---------------- 1. sample delivery ----------------
    M_igg = p("chem.analyte.molar_mass", "g/mol")
    V_s = p("ma.delivery.sample_volume", "m^3")
    contamination = p("ma.nsb.blank_igg_contamination_equivalent", "mol/m^3")       # mol/m^3
    C_molar = convert(conc, "pg/mL", "g/m^3") / M_igg                             # mol/m^3
    f_del = p(INJECTIONS[arch.injection][0], "fraction")
    V_inj = f_del * V_s
    V_loop = p("hw.smfl.loop_volume_recommended", "m^3")
    r_loop = 0.5 * p("hw.smfl.loop_inner_diameter", "m")
    Q_load = p("hw.timing.sample_load_flow", "m^3/s")
    n_flush = p("hw.smfl.loop_flush_volumes_for_transfer", "loop volumes")
    at_outlet = bool(np.all(np.asarray(p("ma.delivery.plug_at_outlet_end", "boolean")) > 0.5))
    D_igg = p("chem.analyte.diffusion_coefficient", "m^2/s")
    if arch.sample_treatment == "carrier":
        loss = p("ma.delivery.adsorptive_loss_fraction_with_carrier", "fraction")
    else:
        loss = p("chem.analyte.adsorptive_loss_fraction_untreated_tube", "fraction")
    plug_frac = float(np.round(np.mean(np.asarray(V_inj / V_loop, float)), 2))
    if arch.capture == "magnetic_beads":
        beta = 0.0 * Q_load + 1e-6          # beads: D -> 0, convective limit
    else:
        beta = D_igg * V_loop / (Q_load * r_loop ** 2)
    f_transfer, _ = tr.loop_transfer_interp(beta, n_flush, plug_frac, at_outlet)
    N_molecules = (C_molar + contamination * 0.0) * V_s * NA                    # in the vial
    N_cont = contamination * V_s * NA                                            # added to blanks (below)

    # ---------------- 2. capture ----------------
    kon_c = p("chem.antibodies.kon_capture", "m^3/(mol*s)")                  # m^3/(mol s)
    koff_c = p("chem.antibodies.koff_capture", "1/s")
    kon_d = p("chem.antibodies.kon_detection", "m^3/(mol*s)")
    koff_d = p("chem.antibodies.koff_detection", "1/s")
    gamma = _gamma_sites(p, arch)
    t_vial = tl["in_vial_s"]

    def capture_chain(Nvial):
        """Return (captured analyte molecules at end of loading, labelled-in-vial fraction or None)."""
        if arch.capture == "magnetic_beads":
            geo = _reactor_geometry("magnetic_beads", p, arch)
            n_beads = p("chem.surfaces.bead_number_per_100uL_digital_ELISA", "beads/m^3") * V_s
            a_b = 0.5 * geo["d_b"]
            sites_per_bead = (p("chem.surfaces.igg_surface_density_monolayer", "molecules/m^2")
                              * 4.0 * np.pi * a_b ** 2 * p("chem.surfaces.active_fraction_oriented", "fraction"))
            k_R = kon_c * sites_per_bead / NA                                    # m^3/s per bead
            k_D = tr.smoluchowski_rate(D_igg, a_b)
            k_bead = k_D * k_R / (k_D + k_R)
            unstirred = p("ma.capture.in_vial_unstirred_rate_factor", "fraction")
            k_pseudo = unstirred * k_bead * n_beads / V_s                        # 1/s
            sites_conc = n_beads * sites_per_bead / NA / V_s                     # mol/m^3
            kin_c = k_pseudo / sites_conc                                        # effective kon (m^3/mol/s)
            if arch.labelling_format == "one_step_in_vial":
                D0 = p("chem.antibodies.conc_detection_antibody_typical", "mol/m^3")
                ACD, AC, AD, _A = kin.one_step_sandwich(Nvial / NA / V_s, sites_conc, D0, kin_c, koff_c,
                                                        kon_d, koff_d, t_vial,
                                                        steps=int(p("ma.numerics.label_ode_steps", "count")))
                cap = (ACD + AC) * V_s * NA
                lab_frac = ACD / np.maximum(ACD + AC, 1e-300)
                return cap, lab_frac, geo, n_beads, sites_per_bead
            f = kin.reversible_binding_fraction(k_pseudo, koff_c, t_vial)
            return f * Nvial, None, geo, n_beads, sites_per_bead
        f, geo = _flow_capture(arch.capture, p, arch, Q_load, Nvial * f_del * (1 - loss) * f_transfer,
                               gamma, kon_c, D_igg)
        return f * Nvial * f_del * (1 - loss) * f_transfer, None, geo, None, None

    N_vial = N_molecules * (1.0 - loss) if arch.capture == "magnetic_beads" else N_molecules
    cap_out = capture_chain(N_vial)
    N_cap, lab_vial, geo, n_beads, sites_per_bead = cap_out
    if arch.capture == "magnetic_beads":
        trap = p("ma.capture.magnetic_trap_efficiency", "fraction")
        N_cap = N_cap * f_del * f_transfer * trap
        A_beads = n_beads * f_del * f_transfer * trap * np.pi * geo["d_b"] ** 2
        geo["A_capture"] = A_beads
        geo["A_nsb"] = (A_beads * p("ma.nsb.surface_factor_magnetic_beads", "fold")
                        + geo["A_trap_wall"] * geo["sf_tubing"])
    capture_fraction = np.divide(N_cap, N_molecules, out=np.zeros(np.broadcast(N_cap, N_molecules).shape),
                                 where=np.broadcast_to(N_molecules, np.broadcast(N_cap, N_molecules).shape) > 0)

    # ---------------- 3. retention (dissociation before the reactor is sealed) ----------------
    retention_capture = np.exp(-koff_c * tl["capture_exposure_s"])
    retention_label = np.exp(-koff_d * tl["label_exposure_s"])

    # ---------------- 4. labelling ----------------
    enz_per_label = p(chem["enzymes_per_label"], "count")
    # conjugate concentration reaching the reactor (loop dispersion of a small plug + tubing)
    V_conj = p("ma.delivery.conjugate_injection_volume", "m^3")
    C_conj_vial = p("chem.antibodies.conc_detection_antibody_typical", "mol/m^3")       # mol/m^3
    beta_conj = p("chem.antibodies.diffusion_coefficient_IgG_ALP_conjugate", "m^2/s") * V_loop / (
        Q_load * r_loop ** 2)
    conj_frac = float(np.round(np.mean(np.asarray(V_conj / V_loop, float)), 2))
    _, peak = tr.loop_transfer_interp(beta_conj, n_flush, conj_frac, at_outlet)
    dil = peak * p("ma.delivery.tubing_dilution_factor", "fraction")
    if arch.scheme == "A":
        # conjugate passes through the bed in flow: exposure integral = C V_inj / Q (dispersion-free)
        t_inc1 = V_conj / Q_load
        C1 = C_conj_vial
    else:
        t_inc1 = tl["conj_incubation_s"]
        C1 = C_conj_vial * dil
    exposure1 = C1 * t_inc1                                                     # mol s / m^3
    if arch.labelling_format == "one_step_in_vial":
        f_label = lab_vial
        exposure_vial = C_conj_vial * t_vial
    else:
        f_label = kin.reversible_binding_fraction(kon_d * C1, koff_d, t_inc1)
    symmetric = p("chem.antibodies.symmetric_Fc_Fc_sandwich_penalty", "relative detection efficiency") \
        if arch.symmetric_pair else 1.0
    two_step = chem["labelling"] == "two_step"
    if two_step:
        kon_sa = p("chem.antibodies.streptavidin_biotin_kon", "m^3/(mol*s)")
        koff_sa = p("chem.antibodies.streptavidin_biotin_koff", "1/s")
        C2_vial = p(chem["second_conc"], "mol/m^3")
        nb = p("ma.labelling.effective_biotins_per_detection_antibody", "count")
        if arch.scheme == "A":
            t_inc2 = V_conj / Q_load
            C2 = C2_vial
        else:
            t_inc2 = tl["second_incubation_s"]
            C2 = C2_vial * dil
        f_sa = kin.reversible_binding_fraction(nb * kon_sa * C2, koff_sa, t_inc2)
        exposure2 = C2 * t_inc2
    else:
        f_sa = 1.0
        exposure2 = 0.0
    N_enz_spec = (N_cap * retention_capture * f_label * symmetric * retention_label * f_sa * enz_per_label)

    # ---------------- 5. non-specific binding of label (blank) ----------------
    k_nsb = p("chem.nsb.nsb_effective_rate_constant", "m/s")
    cross = p("ma.labelling.detection_on_capture_residual_factor", "fold")
    if two_step:
        label_factor = p(chem["label_nsb_factor"], "fold") if chem["label_nsb_factor"] else 1.0
        dab_lab = p("ma.nsb.biotin_dab_nsb_labelling_fraction", "fraction")
        eff_exposure = exposure2 * label_factor + exposure1 * f_sa * dab_lab
    else:
        label_factor = p(chem["label_nsb_factor"], "fold")
        eff_exposure = exposure1 * label_factor
    if arch.scheme == "A":
        # every surface between injector and cell that saw the conjugate keeps producing product
        L_path = (p("hw.tubing.injector_to_reactor_length", "m") + p("hw.tubing.reactor_to_cell_length", "m"))
        A_path = np.pi * p("hw.tubing.id_standard", "m") * L_path * geo["sf_tubing"]
    elif arch.scheme == "B":
        A_path = geo["A_tubing_isolated"] * geo["sf_tubing"]
    else:
        A_path = 0.0
    A_nsb_eff = (geo["A_nsb"] + A_path) * cross
    N_nsb = k_nsb * A_nsb_eff * eff_exposure * NA * enz_per_label
    if arch.labelling_format == "one_step_in_vial":
        # conjugate meets beads in the vial, then flows over the trap wall during loading
        A_b = geo["A_capture"] * p("ma.nsb.surface_factor_magnetic_beads", "fold")
        A_w = (geo["A_trap_wall"] + geo["A_tubing_isolated"]) * geo["sf_tubing"]
        N_nsb = k_nsb * cross * label_factor * enz_per_label * NA * (
            A_b * exposure_vial + A_w * C_conj_vial * V_inj / Q_load)
    N_nsb_beads_part = (k_nsb * cross * label_factor * enz_per_label * NA * eff_exposure * geo["A_capture"]
                        * p("ma.nsb.surface_factor_magnetic_beads", "fold")) if arch.capture == "magnetic_beads" else 0.0

    # ---------------- 6. carry-over (blank) ----------------
    c_inj = p("hw.smfl.carryover_protein_conjugate", "fraction")
    N_conj_injected = C_conj_vial * V_conj * NA * enz_per_label
    if two_step:
        N_conj_injected = C2_vial * V_conj * NA * enz_per_label
    V_acc = geo["V_acc"]
    N_carry = 0.0
    if arch.substrate_delivery == "injected" and arch.stopped:
        N_carry = N_carry + c_inj * N_conj_injected * np.minimum(1.0, V_acc / V_loop)
    # conjugate carried into the next cycle's sample injection; an intervening regeneration/cleaning
    # injection (always present in the timelines used here) squares the fraction
    uptake = 1.0 - np.exp(-k_nsb * A_nsb_eff / Q_load)
    N_carry = N_carry + c_inj ** 2 * N_conj_injected * uptake
    # residual label surviving regeneration (regenerated surfaces), steady state for blank after blank
    r_res = p("chem.regeneration.residual_label_carryover_fraction", "fraction")
    inact = p(chem["inactivation"], "fraction") if arch.regenerated else 0.0
    if arch.capture == "magnetic_beads":
        # beads leave; only the trap wall + tubing NSB can persist
        wall_share = 1.0 - np.minimum(1.0, N_nsb_beads_part / np.maximum(N_nsb, 1e-300))
        persist = r_res * wall_share
    else:
        persist = r_res * (1.0 - inact)
    N_residual_blank = persist / (1.0 - persist) * (N_nsb + N_carry)
    N_carry_total = N_carry + N_residual_blank

    # ---------------- 7. contamination (blank) ----------------
    frac_spec_per_molecule = N_enz_spec / np.maximum(N_molecules, 1e-300)   # enzymes per analyte molecule
    # low-concentration value (linear regime), from the first non-zero grid point
    eff_low = frac_spec_per_molecule[..., 1:2] if np.ndim(frac_spec_per_molecule) else frac_spec_per_molecule
    N_cont_enz = N_cont * eff_low

    # ---------------- 8. signal generation ----------------
    kcat = p(chem["kcat"], "1/s")
    Km = p(chem["Km"], "mol/m^3")
    S0 = p(chem["S0"], "mol/m^3")
    imp = p(chem["impurity"], "mol/mol")
    k_hyd = p(chem["hydrolysis"], "1/s")
    k_dec = K.LN2 / p(chem["half_life"], "s")
    D_prod = p(chem["D_product"], "m^2/s")
    n_e = p(chem["n_e"], "e-/molecule")
    if chem["Ki"]:
        Ki = p(chem["Ki"], "mol/m^3")
        ppp = p(chem["pi_per_product"], "count")
    else:
        Ki, ppp = np.inf, 1.0
    gain = p(chem["cycling"]["gain"], "fold") if (arch.chemical_cycling and chem["cycling"]) else 1.0
    noise_factor = p(chem["cycling"]["noise_factor"], "fold") if (arch.chemical_cycling and chem["cycling"]) else 1.0
    T_read = tl["readout_s"]
    N_blank_enz = N_nsb + N_carry_total
    steps = int(p("ma.numerics.enzyme_ode_steps", "count"))

    if arch.stopped:
        t_acc = tl["accumulation_s"]
        def product_moles(N_enz):
            E = N_enz / NA / V_acc
            Pe, Pb, S = kin.enzyme_accumulation(E, S0, kcat, Km, t_acc, Ki=Ki, pi_per_product=ppp,
                                                k_hyd=k_hyd, k_decay=k_dec, P_bg0=0.0, steps=steps)
            return Pe * V_acc, Pb * V_acc
        n_tot, _ = product_moles(N_enz_spec + N_blank_enz)
        n_blankenz, n_hyd = product_moles(N_blank_enz)
        n_cont, _ = product_moles(N_blank_enz + N_cont_enz)
        n_cont = n_cont - n_blankenz
        n_imp = imp * S0 * V_acc * np.exp(-k_dec * t_acc)        # impurity product in the plug
        if arch.detector == "ida_chip":
            det = _detector(arch, p, D_prod, Q_load)
            q_per_mol = n_e * det["i_per_conc_per_ne"] / V_acc * T_read      # C per mol in channel
            eluted = 1.0
            Q_read = 0.0 * Q_load
        else:
            Q_read = p("ma.readout.sweep_flow", "m^3/s")
            if arch.detector == "coulometric":
                Q_read = np.maximum(Q_read, p("hw.flow_cells.thermo_6011rs_coulometric.min_flow", "m^3/s"))
            det = _detector(arch, p, D_prod, Q_read)
            sig_t = p("hw.tubing.product_plug_sigma_reactor_to_cell", "m^3")
            n_eff = V_acc ** 2 / (V_acc ** 2 / geo["tanks"] + sig_t ** 2)
            eluted = tr.tanks_in_series_eluted(Q_read * T_read / V_acc, n_eff)
            q_per_mol = n_e * FARADAY * det["eta"] * eluted
        q_per_mol = q_per_mol * gain
        Q_signal_total = q_per_mol * n_tot
        Q_blankenz = q_per_mol * n_blankenz
        Q_spec = Q_signal_total - Q_blankenz
        Q_cont = q_per_mol * n_cont
        Q_hyd = q_per_mol * n_hyd
        Q_imp = q_per_mol * n_imp                                    # measured in the same run (baseline)
        baseline_referenced = True
    else:
        # Scheme A: substrate flows through the bed; signal = steady turnover current x read window
        Q_sub = p("ma.readout.continuous_flow", "m^3/s")
        if arch.detector == "coulometric":
            Q_sub = np.maximum(Q_sub, p("hw.flow_cells.thermo_6011rs_coulometric.min_flow", "m^3/s"))
        det = _detector(arch, p, D_prod, Q_sub)
        v_per_enz = kcat * S0 / (Km + S0) / NA                       # mol/s per enzyme (fresh substrate)
        q_rate = n_e * FARADAY * det["eta"] * gain                   # C per mol
        Q_spec = q_rate * v_per_enz * N_enz_spec * T_read
        Q_blankenz = q_rate * v_per_enz * N_blank_enz * T_read
        Q_cont = q_rate * v_per_enz * N_cont_enz * T_read
        t_age = tl["reservoir_age_s"]
        Q_hyd = q_rate * Q_sub * S0 * k_hyd * t_age * T_read         # reservoir hydrolysis, not referenced
        Q_imp = q_rate * Q_sub * S0 * imp * T_read
        baseline_referenced = False
        Q_read = Q_sub
        eluted = 1.0

    # split enzyme-borne blank into NSB and carry-over parts (proportional to enzyme numbers)
    share_nsb = N_nsb / np.maximum(N_blank_enz, 1e-300)
    Q_nsb = Q_blankenz * share_nsb
    Q_carry = Q_blankenz * (1.0 - share_nsb)
    q_per_enzyme = Q_blankenz / np.maximum(N_blank_enz, 1e-300)

    # ---------------- 9. noise and blank statistics ----------------
    stopped_readout = arch.detector == "ida_chip"
    i_ref = p("hw.gamry.noise_rms_stopped_flow" if stopped_readout else "hw.gamry.noise_rms_flow", "A")
    A_ref = p("ma.noise.reference_electrode_area", "m^2")
    alpha = p("ma.noise.area_exponent", "dimensionless")
    floor = p("hw.gamry.antec_decade_floor_pp", "A") / p("ma.noise.pp_to_rms", "dimensionless")
    i_n = np.maximum(floor, i_ref * (det["area"] / A_ref) ** alpha) * noise_factor
    B = p("ma.noise.reference_bandwidth", "Hz")
    var_ec = (i_n * np.sqrt(T_read / (2.0 * B))) ** 2 * 2.0          # signal window + baseline window
    drift = p("hw.gamry.baseline_drift", "A/min") / 60.0
    var_drift = (p("ma.noise.drift_residual_fraction", "fraction") * 0.5 * drift * T_read ** 2) ** 2

    cv_nsb = p("chem.nsb.blank_CV_analog_electrochemical", "fraction")
    fouling = float(np.max(np.asarray(p(chem["fouling"], "boolean")))) > 0.5
    if arch.detector == "wall_jet_spe":
        cv_sens = p("ma.noise.spe_sensor_to_sensor_cv", "fraction")
    elif fouling or arch.scheme == "C":
        cv_sens = p("ma.noise.electrode_sensitivity_cv_fouling", "fraction")
    else:
        cv_sens = p("ma.noise.electrode_sensitivity_cv_nonfouling", "fraction")
    inj_rsd = p("hw.smfl.injection_precision_rsd_large", "fraction")
    bead_cv = p("ma.capture.bead_dose_cv", "fraction") if arch.capture == "magnetic_beads" else 0.0
    bead_share = (N_nsb_beads_part / np.maximum(N_nsb, 1e-300)) if arch.capture == "magnetic_beads" else 0.0
    cv_sub = p("ma.noise.substrate_background_cv", "fraction")
    rel_bg = p("ma.noise.background_current_relative_noise", "fraction")
    cv_carry = p("ma.noise.carryover_cv", "fraction")

    terms = {}
    terms["nsb_variability"] = (cv_nsb * Q_nsb) ** 2 + (inj_rsd * Q_nsb) ** 2 + (bead_cv * bead_share * Q_nsb) ** 2
    terms["label_counting"] = q_per_enzyme ** 2 * N_blank_enz            # Poisson on enzyme numbers
    terms["carryover"] = (cv_carry * Q_carry) ** 2
    if baseline_referenced:
        terms["substrate_background"] = (cv_sub * Q_hyd) ** 2 + (rel_bg * (Q_imp + Q_hyd)) ** 2
        terms["electrode_sensitivity"] = (cv_sens * (Q_nsb + Q_carry + Q_hyd)) ** 2
    else:
        terms["substrate_background"] = (cv_sub * (Q_imp + Q_hyd)) ** 2 + (rel_bg * (Q_imp + Q_hyd)) ** 2
        terms["electrode_sensitivity"] = (cv_sens * (Q_nsb + Q_carry + Q_hyd + Q_imp)) ** 2
    terms["electrochemical_noise"] = var_ec + 0.0 * Q_nsb
    terms["baseline_drift"] = var_drift + 0.0 * Q_nsb
    terms["contamination"] = Q_cont ** 2
    terms = {k: np.squeeze(np.asarray(v, float), axis=-1) if np.ndim(v) and np.shape(v)[-1] == 1 else
             np.asarray(v, float) for k, v in terms.items()}

    blank_sd = np.sqrt(sum(terms.values()))
    blank_mean = np.squeeze(np.asarray(Q_nsb + Q_carry + Q_hyd + Q_cont + (0.0 if baseline_referenced else Q_imp),
                                       float))
    if np.ndim(blank_mean) == 2 and blank_mean.shape[-1] == 1:
        blank_mean = blank_mean[:, 0]

    # ---------------- 10. calibration, LOD, range ----------------
    net = np.asarray(Q_spec, float)
    net = net - net[..., :1]                                     # zero at blank
    k_sd = p("ma.statistics.k_sd", "dimensionless")
    lod, lod_slope, uloq = _lod_and_range(conc, net, k_sd * blank_sd,
                                          p("ma.statistics.uloq_min_log_slope", "dimensionless"))
    dr = np.log10(np.where(uloq > lod, uloq / lod, 1.0))

    top = p("ma.statistics.range_top", "pg/mL")
    n_between = 2.0   # injections between two sample injections in every timeline used (label + regen/clean)
    enz_per_pg = _low(N_enz_spec / np.maximum(conc, 1e-300))
    carry_top = (c_inj ** (n_between + 1.0) * top
                 + persist * _interp_at(conc, N_enz_spec, top) / np.maximum(enz_per_pg, 1e-300))
    if arch.regenerated:
        loss_cap = p("chem.regeneration.activity_loss_per_cycle", "fraction per cycle")
    else:
        loss_cap = 0.0 * persist
    if arch.detector == "wall_jet_spe":
        loss_el = 0.0 * persist
    elif fouling or arch.scheme == "C":
        loss_el = p("ma.reuse.electrode_sensitivity_loss_per_cycle_fouling", "fraction per cycle")
    else:
        loss_el = p("ma.reuse.electrode_sensitivity_loss_per_cycle_nonfouling", "fraction per cycle")

    diag = dict(
        carryover_after_top_pgml=carry_top, residual_label_per_cycle=persist,
        capacity_loss_per_cycle=loss_cap, electrode_loss_per_cycle=loss_el,
        delivered_fraction=f_del, loop_transfer=f_transfer, adsorptive_loss=loss,
        capture_fraction_low=_low(capture_fraction), retention_capture=retention_capture,
        label_fraction_low=_low(f_label) if np.ndim(f_label) else f_label, second_step_fraction=f_sa,
        retention_label=retention_label, enzymes_per_label=enz_per_label,
        enzymes_per_pg_per_mL=_low(N_enz_spec / np.maximum(conc, 1e-300)),
        enzymes_at_1pg=_interp_at(conc, N_enz_spec, 1.0),
        N_nsb=N_nsb, N_carry=N_carry_total, accumulation_volume_uL=convert(V_acc, "m^3", "uL"),
        conjugate_peak_dilution=dil, cell_conversion=det.get("eta", np.nan),
        eluted_fraction=eluted, noise_rms_A=i_n,
        signal_at_1pg_C=_interp_at(conc, net, 1.0),
        blank_equivalent_pgml=_blank_equiv(conc, net, blank_mean),
        capture_area_m2=geo.get("A_capture", np.nan), nsb_area_eff_m2=A_nsb_eff,
        timeline_min=tl["steps_min"],
    )
    diag = {k: (np.squeeze(v) if isinstance(v, np.ndarray) else v) for k, v in diag.items()}
    return Result(arch=arch, conc_pgml=conc, net_signal=net, blank_mean=blank_mean, blank_sd=blank_sd,
                  lod_pgml=lod, lod_slope_pgml=lod_slope, uloq_pgml=uloq, dynamic_range_decades=dr,
                  cycle_time_min=tl["cycle_min"], time_to_result_min=tl["time_to_result_min"],
                  variance_terms=terms, diagnostics=diag)


def _low(x):
    x = np.asarray(x, float)
    return x[..., 1] if x.ndim and x.shape[-1] > 1 else x


def _interp_at(conc, y, c0):
    y = np.asarray(y, float)
    y2 = np.broadcast_to(y, np.broadcast(y, conc).shape)
    lc = np.log(conc[1:])
    if y2.ndim == 1:
        return float(np.exp(np.interp(np.log(c0), lc, np.log(np.maximum(y2[1:], 1e-300)))))
    return np.array([np.exp(np.interp(np.log(c0), lc, np.log(np.maximum(r[1:], 1e-300)))) for r in y2])


def _blank_equiv(conc, net, blank_mean):
    """Concentration whose net signal equals the blank mean (analyte-equivalent blank B)."""
    net2 = np.atleast_2d(net)
    bm = np.atleast_1d(blank_mean)
    out = np.array([_inverse(conc, r, b) for r, b in zip(net2, np.broadcast_to(bm, (net2.shape[0],)))])
    return out if np.ndim(net) == 2 else float(out[0])


def _inverse(conc, row, target):
    """Smallest concentration at which the (monotone part of the) net signal reaches target."""
    c = conc[1:]
    y = row[1:]
    if not np.isfinite(target) or target <= 0:
        return 0.0
    if y[0] >= target:
        return c[0] * target / y[0]          # linear extrapolation below the grid
    above = np.nonzero(y >= target)[0]
    if len(above) == 0:
        return np.inf
    j = above[0]
    x0, x1 = np.log(c[j - 1]), np.log(c[j])
    y0, y1 = np.log(max(y[j - 1], 1e-300)), np.log(y[j])
    return float(np.exp(x0 + (np.log(target) - y0) * (x1 - x0) / (y1 - y0)))


def _lod_and_range(conc, net, threshold, min_log_slope):
    net2 = np.atleast_2d(net)
    thr = np.broadcast_to(np.atleast_1d(threshold), (net2.shape[0],))
    lods, lod_s, uloqs = [], [], []
    c = conc[1:]
    for row, t in zip(net2, thr):
        lods.append(_inverse(conc, row, t))
        slope = row[1] / c[0]
        lod_s.append(t / slope if slope > 0 else np.inf)
        y = np.maximum(row[1:], 1e-300)
        dlog = np.diff(np.log(y)) / np.diff(np.log(c))
        ok = dlog >= min_log_slope
        if len(ok) == 0:
            uloqs.append(c[-1])
        elif ok[0]:
            bad = np.nonzero(~ok)[0]
            uloqs.append(c[bad[0]] if len(bad) else c[-1])
        else:
            uloqs.append(c[0])
    lods, lod_s, uloqs = np.array(lods), np.array(lod_s), np.array(uloqs)
    if np.ndim(net) == 1:
        return float(lods[0]), float(lod_s[0]), float(uloqs[0])
    return lods, lod_s, uloqs
