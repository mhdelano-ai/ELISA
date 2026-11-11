"""Comparisons of sub-models with published numbers (docs/01) and Task 1/2 worked estimates.

Each function returns a dict with the model value, the published value, their ratio and the inputs, so
that tests and docs/03 report the same numbers.  Scenario inputs that the publications do not state are
parameters in the ``validation`` section of model_assumptions.yaml (marked UNVERIFIED there).
"""
from __future__ import annotations

import numpy as np

from . import constants as K
from . import kinetics as kin
from . import transport as tr
from .params import ParameterSet
from .units import convert

NA = K.AVOGADRO


def task1_product_estimate(ps: ParameterSet) -> dict:
    """docs/01 b: ~1e5 ALP labels, kcat ~1000 /s, 10 min, 10 uL -> ~10 nM product (pAPP at 1 mM)."""
    g = ps.get
    N = g("ma.validation.task1_labels", "count")
    V = g("ma.validation.task1_volume", "m^3")
    t = g("ma.validation.task1_time", "s")
    E = N / NA / V
    Pe, _, _ = kin.enzyme_accumulation(E, g("chem.substrates.pAPP.working_concentration", "mol/m^3"),
                                       g("chem.enzymes.alp.kcat_conjugate_assay_conditions", "1/s"),
                                       g("chem.enzymes.alp.Km_pAPP", "mol/m^3"), t,
                                       Ki=g("chem.enzymes.alp.phosphate_inhibition_Ki", "mol/m^3"))
    model = float(convert(float(Pe), "mol/m^3", "M"))
    pub = g("ma.validation.task1_product_concentration", "M")
    return dict(name="Task 1 worked estimate (1e5 ALP, 10 min, 10 uL)", model=model, published=pub,
                unit="M", ratio=model / pub)


def dellaciana_alp_lod(ps: ParameterSet, kcat_key="chem.enzymes.alp.kcat_conjugate_assay_conditions") -> dict:
    """DellaCiana1996: free ALP detected at 1.2e-15 M after 10 min (HQ FIA LOD 1.2e-10 M).

    Model: ALP concentration that produces the published HQ detection limit in the stated time.
    """
    g = ps.get
    t = g("ma.validation.dellaciana_incubation_time", "s")
    S0 = g("ma.validation.dellaciana_substrate_concentration", "mol/m^3")
    Km = g("ma.chemistries.alp_hqdp.Km", "mol/m^3")
    kcat = g(kcat_key, "1/s")
    hq_lod = g("chem.substrates.HQ.FIA_detection_limit", "mol/m^3")
    # product per unit enzyme concentration (linear in E)
    E_probe = 1e-12
    Pe, _, _ = kin.enzyme_accumulation(E_probe, S0, kcat, Km, t)
    model = float(convert(hq_lod / (float(Pe) / E_probe), "mol/m^3", "M"))
    pub = g("chem.enzymes.alp.detection_limit_FIA_EC_free_enzyme", "M")
    implied_kcat = kcat * model / pub
    # The published enzyme LOD can only be limited by the product-detector LOD or by something larger (substrate
    # blank: free HQ / hydrolysis), so the kcat that puts exactly the detector-LOD of product at the enzyme LOD is a
    # LOWER BOUND on the effective kcat, not an estimate (audit, docs/04).  model/published < 1 is expected.
    return dict(name="DellaCiana1996 free-ALP LOD (10 min, HQ)", model=model, published=pub, unit="M",
                ratio=model / pub, implied_kcat=implied_kcat, implied_kcat_lower_bound=implied_kcat)


def dellaciana_hq_fia_lod(ps: ParameterSet) -> dict:
    """HQ detection limit of a GC wall-jet FIA detector predicted from the wall-jet equation and the
    Task 2 flow-noise estimate, vs the published 1.2e-10 M (DellaCiana1996)."""
    g = ps.get
    Q = g("ma.validation.dellaciana_flow", "m^3/s")
    R = 0.5 * g("ma.validation.dellaciana_electrode_diameter", "m")
    nu = g("ma.fluid.viscosity", "Pa*s") / g("ma.fluid.density", "kg/m^3")
    eta = tr.wall_jet_conversion(g("chem.substrates.HQ.diffusion_coefficient", "m^2/s"), nu,
                                 g("ma.geometry.walljet_nozzle_diameter", "m"), R, Q,
                                 g("ma.detection.walljet_coefficient", "dimensionless"))
    n = g("chem.substrates.HQ.n_electrons", "e-/molecule")
    i_n = g("hw.gamry.noise_rms_flow", "A") * (np.pi * R ** 2 / g("ma.noise.reference_electrode_area", "m^2")) \
        ** g("ma.noise.area_exponent", "dimensionless")
    c_lod = convert(g("ma.statistics.k_sd", "dimensionless") * i_n / (n * K.FARADAY * eta * Q), "mol/m^3", "M")
    pub = g("chem.substrates.HQ.FIA_detection_limit", "M")
    return dict(name="DellaCiana1996 HQ FIA LOD (wall-jet + noise model)", model=float(c_lod), published=pub,
                unit="M", ratio=float(c_lod) / pub, conversion=float(eta))


def thompson_alp_lod(ps: ParameterSet) -> dict:
    """Thompson1991: ALP 0.05 ug/L detected after 15 min with pAP LC-EC LOD 7 nM."""
    g = ps.get
    t = g("ma.validation.thompson_incubation_time", "s")
    S0 = g("chem.substrates.pAPP.working_concentration", "mol/m^3")
    Km = g("chem.enzymes.alp.Km_pAPP", "mol/m^3")
    kcat = g("chem.enzymes.alp.kcat_conjugate_assay_conditions", "1/s")
    pap_lod = g("chem.substrates.pAP.FIA_detection_limit", "mol/m^3")
    E_probe = 1e-12
    Pe, _, _ = kin.enzyme_accumulation(E_probe, S0, kcat, Km, t)
    E_lod = pap_lod / (float(Pe) / E_probe)                                   # mol/m^3
    model_ugL = convert(E_lod * g("chem.enzymes.alp.molar_mass", "g/mol"), "g/m^3", "ug/L")
    pub = g("chem.enzymes.alp.detection_limit_LC_EC_pAPP", "ug/L ALP")
    implied_kcat = kcat * model_ugL / pub
    # lower bound only (see dellaciana_alp_lod); Thompson1991 also does not state the ALP source/grade, so the mass
    # unit (ug/L of a commercial preparation of unknown specific activity) adds a further unknown factor.
    return dict(name="Thompson1991 ALP LOD (15 min, pAPP, LC-EC 7 nM pAP)", model=model_ugL, published=pub,
                unit="ug/L", ratio=model_ugL / pub, implied_kcat=implied_kcat, implied_kcat_lower_bound=implied_kcat)


def chang_bead_capture(ps: ParameterSet) -> dict:
    """Bead capture in a well-mixed suspension (5e5 beads/100 uL), 30 min, vs the ~70 % of docs/01 a.2."""
    g = ps.get
    t = g("ma.validation.chang_capture_time", "s")
    V = g("ma.delivery.sample_volume", "m^3")
    n_b = g("chem.surfaces.bead_number_per_100uL_digital_ELISA", "beads/m^3")
    a = 0.5 * g("ma.validation.simoa_bead_diameter", "m")
    sites = g("chem.surfaces.igg_surface_density_monolayer", "molecules/m^2") * 4 * np.pi * a ** 2 \
        * g("chem.surfaces.active_fraction_oriented", "fraction")
    kon = g("chem.antibodies.kon_capture", "m^3/(mol*s)")
    k_R = kon * sites / NA
    k_D = tr.smoluchowski_rate(g("chem.analyte.diffusion_coefficient", "m^2/s"), a)
    k = n_b * k_D * k_R / (k_D + k_R)
    f = float(kin.reversible_binding_fraction(k, g("chem.antibodies.koff_capture", "1/s"), t))
    f_simple = float(1 - np.exp(-kon * g("chem.surfaces.bead_ab_concentration_digital_ELISA", "mol/m^3") * t))
    pub = g("ma.validation.chang_capture_fraction", "fraction")
    return dict(name="Bead capture, 30 min (Chang2012-derived ~70 %)", model=f, published=pub, unit="fraction",
                ratio=f / pub, model_without_transport_and_activity=f_simple, pseudo_first_order_rate=k)


def _beq_from_counts(N_nsb, V, f_specific):
    """Analyte-equivalent blank concentration (M) from NSB enzymes and enzymes per analyte molecule."""
    return convert(N_nsb / (V * NA * f_specific), "mol/m^3", "M")


def simoa_blank(ps: ParameterSet) -> dict:
    """Closure check of the NSB rate constant with its own source (Rissin2010 conditions)."""
    g = ps.get
    V = g("ma.delivery.sample_volume", "m^3")
    n_b = g("ma.validation.simoa_beads_per_100uL", "beads/m^3") * V
    a = 0.5 * g("ma.validation.simoa_bead_diameter", "m")
    A = n_b * 4 * np.pi * a ** 2
    sites = g("chem.surfaces.igg_surface_density_monolayer", "molecules/m^2") * 4 * np.pi * a ** 2 \
        * g("chem.surfaces.active_fraction_oriented", "fraction")
    kon_c = g("chem.antibodies.kon_capture", "m^3/(mol*s)")
    k_R = kon_c * sites / NA
    k_D = tr.smoluchowski_rate(g("chem.analyte.diffusion_coefficient", "m^2/s"), a)
    f_cap = kin.reversible_binding_fraction(n_b / V * k_D * k_R / (k_D + k_R), g("chem.antibodies.koff_capture", "1/s"),
                                            g("ma.validation.simoa_capture_time", "s"))
    f_dab = kin.reversible_binding_fraction(g("chem.antibodies.kon_detection", "1/(M*s)") *
                                            g("chem.antibodies.conc_detection_antibody_typical", "M"),
                                            g("chem.antibodies.koff_detection", "1/s"), g("ma.validation.simoa_dab_time", "s"))
    C_sbg = g("chem.antibodies.conc_streptavidin_enzyme_typical", "mol/m^3")
    t_sbg = g("ma.validation.simoa_sbg_time", "s")
    f_sbg = kin.reversible_binding_fraction(g("chem.antibodies.streptavidin_biotin_kon", "m^3/(mol*s)") * C_sbg,
                                            g("chem.antibodies.streptavidin_biotin_koff", "1/s"), t_sbg)
    N_nsb = g("chem.nsb.nsb_effective_rate_constant", "m/s") * A * C_sbg * t_sbg * NA
    B = _beq_from_counts(N_nsb, V, f_cap * f_dab * f_sbg)
    pub = g("chem.nsb.background_equivalent_best_in_class", "M")
    return dict(name="Simoa blank equivalent (closure check of the NSB rate, Rissin2010)", model=float(B),
                published=pub, unit="M", ratio=float(B) / pub, N_nsb=float(N_nsb),
                active_bead_fraction=float(N_nsb / n_b))


def conventional_elisa_blank(ps: ParameterSet, label_conc_M: float | None = None) -> dict:
    """Blank equivalent of a conventional 96-well ELISA predicted by the same NSB sub-model, vs the
    85 fM reported for a commercial TNF-a ELISA (Rissin2010)."""
    g = ps.get
    V = g("ma.delivery.sample_volume", "m^3")
    d = g("ma.validation.plate_well_diameter", "m")
    h = V / (np.pi * (0.5 * d) ** 2)
    A = np.pi * (0.5 * d) ** 2 + np.pi * d * h
    D = g("chem.analyte.diffusion_coefficient", "m^2/s")
    t_cap = g("ma.validation.plate_capture_time", "s")
    # capture: planar diffusion to a perfect sink from a quiescent layer, capped by kinetics
    gamma = g("chem.surfaces.igg_surface_density_monolayer", "molecules/m^2") * \
        g("chem.surfaces.active_fraction_random_adsorbed", "fraction") / NA
    k_r = g("chem.antibodies.kon_capture", "m^3/(mol*s)") * gamma
    f_diff = min(1.0, A / V * 2 * np.sqrt(D * t_cap / np.pi))
    f_kin = 1 - np.exp(-k_r * A / V * t_cap)
    f_cap = min(f_diff, f_kin)
    C_lab = convert(label_conc_M if label_conc_M is not None else g("ma.validation.plate_label_concentration", "M"),
                    "M", "mol/m^3")
    t_lab = g("ma.validation.plate_label_time", "s")
    f_lab = kin.reversible_binding_fraction(g("chem.antibodies.kon_detection", "m^3/(mol*s)") * C_lab,
                                            g("chem.antibodies.koff_detection", "1/s"), t_lab)
    k_eff = g("chem.nsb.nsb_effective_rate_constant", "m/s") * g("ma.nsb.label_factor_igg_enzyme_conjugate", "fold")
    N_nsb = k_eff * A * C_lab * t_lab * NA
    B = _beq_from_counts(N_nsb, V, f_cap * f_lab)
    pub = g("chem.nsb.background_equivalent_conventional_ELISA", "M")
    return dict(name=f"Conventional plate ELISA blank equivalent (Rissin2010 85 fM), "
                     f"{convert(C_lab, 'mol/m^3', 'nM'):g} nM label", model=float(B),
                published=pub, unit="M", ratio=float(B) / pub, capture_fraction=f_cap,
                label_fraction=float(f_lab), label_conc_M=convert(C_lab, "mol/m^3", "M"),
                k_nsb_effective=k_eff, implied_k_nsb=k_eff * pub / float(B))


def simoa_detection_antibody_consistency(ps: ParameterSet) -> dict:
    """Internal consistency of the NSB sub-model with its own source experiment (audit, docs/04 section 3.1).

    In Rissin2010 the beads were exposed to ~1 nM biotinylated detection antibody for 45 min before the SbG
    step, and Chang2012 reports that only ~13 % of bead-bound biotinylated dAb is labelled by 15 pM SbG in
    30 min.  The blank (active-bead fraction) predicted from BOTH reagents with the model's NSB rates must not
    exceed the observed blank: ~1 % active beads (Rissin2010) or ~0.3 % (Chang2012).
    """
    g = ps.get
    V = g("ma.delivery.sample_volume", "m^3")
    n_b = g("ma.validation.simoa_beads_per_100uL", "beads/m^3") * V
    a = 0.5 * g("ma.validation.simoa_bead_diameter", "m")
    A = n_b * 4 * np.pi * a ** 2
    k = g("chem.nsb.nsb_effective_rate_constant", "m/s")
    f_igg = g("ma.nsb.label_factor_igg_enzyme_conjugate", "fold")
    N_sbg = k * A * g("chem.antibodies.conc_streptavidin_enzyme_typical", "mol/m^3") * g("ma.validation.simoa_sbg_time", "s") * NA
    N_dab = k * f_igg * A * g("chem.antibodies.conc_detection_antibody_typical", "mol/m^3") \
        * g("ma.validation.simoa_dab_time", "s") * NA
    lab = g("ma.validation.simoa_sbg_labelling_efficiency", "fraction")
    active_sbg = float(N_sbg / n_b)
    active_dab = float(N_dab * lab / n_b)
    total = active_sbg + active_dab
    pub = g("ma.validation.simoa_blank_active_bead_fraction", "fraction")
    return dict(name="Simoa blank incl. detection-antibody NSB (Rissin2010 ~1 % active beads)", model=total,
                published=pub, unit="fraction of beads active", ratio=total / pub, from_sbg=active_sbg,
                from_dab=active_dab,
                max_igg_factor_if_all_from_dab=float(pub / (N_dab / f_igg * lab / n_b)))


def task2_loop_table() -> list[dict]:
    """Loop-transfer fractions vs the Task 2 table (docs/02 section 2.4c); inputs are that table's cases."""
    cases = [  # (V_loop uL, ID mm, plug uL, at_outlet, Q uL/min, published fractions at 1, 1.5, 2, 3 V_loop)
        (250, 0.5, 250, False, 50, (0.84, 0.97, 0.997, 1.000)),
        (250, 0.5, 85, False, 50, (0.62, 0.91, 0.99, 1.000)),
        (250, 0.5, 250, False, 200, (0.78, 0.91, 0.97, 0.9985)),
        (250, 0.5, 85, False, 200, (0.57, 0.78, 0.91, 0.996)),
        (100, 0.5, 100, False, 100, (0.77, 0.90, 0.96, 0.997)),
        (100, 0.25, 75, True, 50, (0.95, 0.998, 1.000, 1.000)),
    ]
    D = 3.89e-11  # IgG diffusion coefficient used by Task 2 (chem.analyte.diffusion_coefficient)
    out = []
    for V, idm, plug, outlet, Q, pub in cases:
        r = 0.5e-3 * idm
        beta = D * V * 1e-9 / (Q * 1e-9 / 60 * r ** 2)
        frac, peak = tr.loop_transfer(beta, plug / V, outlet, [1, 1.5, 2, 3])
        out.append(dict(case=f"{V} uL loop, {idm} mm ID, {plug} uL plug {'at outlet' if outlet else 'far end'}, "
                             f"{Q} uL/min", model=[float(x) for x in frac], published=list(pub),
                        max_abs_diff=float(np.max(np.abs(np.array(frac) - np.array(pub))))))
    return out


def all_validations(ps: ParameterSet) -> list[dict]:
    return [task1_product_estimate(ps), dellaciana_alp_lod(ps), dellaciana_hq_fia_lod(ps), thompson_alp_lod(ps),
            chang_bead_capture(ps), simoa_blank(ps), simoa_detection_antibody_consistency(ps),
            conventional_elisa_blank(ps),
            conventional_elisa_blank(ps, label_conc_M=ps.get("chem.antibodies.conc_detection_antibody_typical", "M"))]
