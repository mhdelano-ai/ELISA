"""Architecture configuration: capture geometry x label/substrate chemistry x detection cell x plumbing
scheme x timing.  An :class:`Architecture` holds only choices and parameter-key references; every number
comes from the parameter files (``design`` lets an architecture pin design variables to other values).
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from itertools import product

SCHEMES = {
    "A": "one 6-port valve, cell bypass; reactor cannot be isolated -> continuous-flow substrate readout",
    "B": "10-port reactor isolation + 6-port cell bypass; stopped-flow accumulation, product swept to cell",
    "C": "integrated capture-detection chip isolated by the 10-port valve; stopped-flow readout in the cell",
}

CAPTURES = {
    "packed_bed": "10 uL column of non-porous capture beads (hw.reactors.packed_microbed_10uL)",
    "monolith": "100 uL CIM-type monolith, straight-channel model (hw.reactors.monolith_cimac_100uL)",
    "capillary": "open-tubular antibody-coated capillary",
    "magnetic_beads": "streptavidin magnetic beads pre-dispensed in the sample vial, captured in-vial, "
                      "trapped magnetically in-line, discarded every run (renewable)",
    "chip_planar": "antibody on the channel wall of the electrode chip (Scheme C)",
    "chip_bead_bed": "1 uL bead bed in the chip immediately upstream of the IDA (Scheme C)",
}

DETECTORS = {
    "thin_layer": "thin-layer channel amperometric cell, 3 mm GC (BASi type), flow-through",
    "wall_jet_sencell": "confined wall-jet, 2 mm WE (Antec SenCell type), flow-through",
    "wall_jet_spe": "wall-jet with disposable screen-printed electrode (DropSens), flow-through",
    "coulometric": "porous-graphite coulometric cell (Dionex 6011RS type), flow >= 0.3 mL/min",
    "ida_flow": "thin-film IDA in a 25 um channel, redox cycling (bipotentiostat), flow-through",
    "ida_chip": "IDA in the sealed chip channel, stopped-flow steady-state redox cycling (Aoki)",
}

INJECTIONS = {
    # mode: (delivered-fraction key, description)
    "PLNO_250": ("hw.smfl.delivered_fraction_plno_250loop", "250 uL loop, PLNO 82 uL"),
    "PLPA_250": ("hw.smfl.delivered_fraction_plpa_250loop", "250 uL loop, PLPA 97 uL"),
    "PLNO_100": ("hw.smfl.delivered_fraction_plno_100loop", "100 uL loop, PLNO 75 uL"),
}

_ALP = "chem.enzymes.alp"
_PAP = "chem.substrates.pAP"

CHEMISTRIES = {
    "alp_hqdp": dict(
        label="ALP / HQDP -> hydroquinone",
        enzyme="alp", labelling="direct",
        kcat=f"{_ALP}.kcat_conjugate_assay_conditions", Km="ma.chemistries.alp_hqdp.Km",
        S0="ma.chemistries.alp_hqdp.substrate_concentration",
        impurity="ma.chemistries.alp_hqdp.free_product_impurity",
        hydrolysis="ma.chemistries.alp_hqdp.hydrolysis_rate",
        half_life="ma.chemistries.alp_hqdp.product_half_life",
        D_product="chem.substrates.HQ.diffusion_coefficient", n_e="chem.substrates.HQ.n_electrons",
        Ki=f"{_ALP}.phosphate_inhibition_Ki", pi_per_product="ma.chemistries.alp_hqdp.phosphate_per_product",
        reversible=True, fouling="ma.chemistries.alp_hqdp.electrode_fouling",
        enzymes_per_label="chem.antibodies.enzyme_to_antibody_ratio_ALP",
        label_nsb_factor="ma.nsb.label_factor_igg_enzyme_conjugate",
        inactivation=f"{_ALP}.inactivation_by_low_pH_regeneration",
        cycling=None),
    "alp_aap": dict(
        label="ALP / AAP -> ascorbate (+TCEP chemical cycling)",
        enzyme="alp", labelling="direct",
        kcat=f"{_ALP}.kcat_conjugate_assay_conditions", Km=f"{_ALP}.Km_ascorbic_acid_2_phosphate",
        S0="ma.chemistries.alp_aap.substrate_concentration",
        impurity="ma.chemistries.alp_aap.free_product_impurity",
        hydrolysis="ma.chemistries.alp_aap.hydrolysis_rate",
        half_life="ma.chemistries.alp_aap.product_half_life",
        D_product="ma.chemistries.alp_aap.product_diffusion_coefficient", n_e="chem.substrates.AA.n_electrons",
        Ki=f"{_ALP}.phosphate_inhibition_Ki", pi_per_product="ma.chemistries.alp_papp.phosphate_per_product",
        reversible=False, fouling="ma.chemistries.alp_aap.electrode_fouling",
        enzymes_per_label="chem.antibodies.enzyme_to_antibody_ratio_ALP",
        label_nsb_factor="ma.nsb.label_factor_igg_enzyme_conjugate",
        inactivation=f"{_ALP}.inactivation_by_low_pH_regeneration",
        cycling=dict(gain=f"{_PAP}.chemical_redox_cycling_gain",
                     noise_factor="ma.chemistries.alp_aap.tcep_noise_factor")),
    "sbg_papg": dict(
        label="biotin-dAb + SbG / pAPG -> pAP (neutral pH, two-step)",
        enzyme="beta_gal", labelling="two_step",
        kcat="chem.enzymes.beta_gal.kcat", Km="chem.enzymes.beta_gal.Km_pAPG",
        S0="ma.chemistries.sbg_papg.substrate_concentration",
        impurity="ma.chemistries.sbg_papg.free_product_impurity",
        hydrolysis="chem.substrates.pAPG.spontaneous_hydrolysis_rate",
        half_life="ma.chemistries.sbg_papg.product_half_life",
        D_product=f"{_PAP}.diffusion_coefficient", n_e=f"{_PAP}.n_electrons",
        Ki=None, pi_per_product=None,
        reversible=True, fouling=f"{_PAP}.fouling",
        enzymes_per_label="ma.labelling.sbg_enzymes_per_conjugate",
        second_conc="chem.antibodies.conc_streptavidin_enzyme_typical",
        label_nsb_factor=None,
        inactivation="ma.chemistries.sbg.enzyme_inactivation_by_regeneration",
        cycling=None),
    "alp_papp": dict(
        label="ALP / pAPP -> pAP",
        enzyme="alp", labelling="direct",
        kcat=f"{_ALP}.kcat_conjugate_assay_conditions", Km=f"{_ALP}.Km_pAPP",
        S0="chem.substrates.pAPP.working_concentration",
        impurity="chem.substrates.pAPP.free_pAP_impurity_fraction",
        hydrolysis="chem.substrates.pAPP.spontaneous_hydrolysis_rate",
        half_life=f"{_PAP}.autoxidation_half_life_pH9_air",
        D_product=f"{_PAP}.diffusion_coefficient", n_e=f"{_PAP}.n_electrons",
        Ki=f"{_ALP}.phosphate_inhibition_Ki", pi_per_product="ma.chemistries.alp_papp.phosphate_per_product",
        reversible=True, fouling=f"{_PAP}.fouling",
        enzymes_per_label="chem.antibodies.enzyme_to_antibody_ratio_ALP",
        label_nsb_factor="ma.nsb.label_factor_igg_enzyme_conjugate",
        inactivation=f"{_ALP}.inactivation_by_low_pH_regeneration",
        cycling=None),
    "hrp_tmb": dict(
        label="IgG-HRP / TMB (reduction of TMB ox)",
        enzyme="hrp", labelling="direct",
        kcat="chem.enzymes.hrp.kcat_TMB", Km="chem.enzymes.hrp.Km_TMB",
        S0="ma.chemistries.hrp_tmb.substrate_concentration",
        impurity="ma.chemistries.hrp_tmb.free_product_impurity",
        hydrolysis="ma.chemistries.hrp_tmb.hydrolysis_rate",
        half_life="ma.chemistries.hrp_tmb.product_half_life",
        D_product="ma.chemistries.hrp_tmb.product_diffusion_coefficient", n_e="chem.substrates.TMB.n_electrons",
        Ki=None, pi_per_product=None,
        reversible=True, fouling="ma.chemistries.hrp_tmb.electrode_fouling",
        enzymes_per_label="chem.antibodies.enzyme_to_antibody_ratio_HRP",
        label_nsb_factor="ma.nsb.label_factor_igg_enzyme_conjugate",
        inactivation="ma.chemistries.hrp_tmb.enzyme_inactivation_by_regeneration",
        cycling=None),
    "sa_polyhrp_tmb": dict(
        label="biotin-dAb + SA-polyHRP / TMB (two-step)",
        enzyme="hrp", labelling="two_step",
        kcat="chem.enzymes.hrp.kcat_TMB", Km="chem.enzymes.hrp.Km_TMB",
        S0="ma.chemistries.hrp_tmb.substrate_concentration",
        impurity="ma.chemistries.hrp_tmb.free_product_impurity",
        hydrolysis="ma.chemistries.hrp_tmb.hydrolysis_rate",
        half_life="ma.chemistries.hrp_tmb.product_half_life",
        D_product="ma.chemistries.hrp_tmb.product_diffusion_coefficient", n_e="chem.substrates.TMB.n_electrons",
        Ki=None, pi_per_product=None,
        reversible=True, fouling="ma.chemistries.hrp_tmb.electrode_fouling",
        enzymes_per_label="chem.antibodies.poly_HRP_per_streptavidin_polymer",
        second_conc="ma.labelling.sa_polyhrp_concentration",
        label_nsb_factor="ma.nsb.label_factor_polyhrp",
        inactivation="ma.chemistries.hrp_tmb.enzyme_inactivation_by_regeneration",
        cycling=None),
}


@dataclass(frozen=True)
class Architecture:
    name: str
    scheme: str                        # "A", "B", "C"
    capture: str                       # key of CAPTURES
    chemistry: str                     # key of CHEMISTRIES
    detector: str                      # key of DETECTORS
    injection: str = "PLNO_250"        # key of INJECTIONS
    substrate_delivery: str = "bsm"    # "bsm" (B1 line) or "injected" (from a vial through the loop)
    labelling_format: str = "sequential"   # or "one_step_in_vial" (magnetic beads only)
    chemical_cycling: bool = False     # TCEP/hydrazine cycling (only chemistries with a cycling entry)
    sample_treatment: str = "carrier"  # "carrier" (IgG-free carrier protein) or "untreated"
    symmetric_pair: bool = False       # Fc-Fc symmetric sandwich penalty
    design: tuple = field(default_factory=tuple)  # ((param_key, value_in_yaml_unit), ...)

    @property
    def regenerated(self) -> bool:
        return self.capture != "magnetic_beads"

    @property
    def stopped(self) -> bool:
        return self.scheme in ("B", "C")

    def describe(self) -> str:
        return (f"Scheme {self.scheme} | {CAPTURES[self.capture]} | {CHEMISTRIES[self.chemistry]['label']} | "
                f"{DETECTORS[self.detector]} | {INJECTIONS[self.injection][1]}"
                + (" | injected substrate" if self.substrate_delivery == "injected" else "")
                + (" | one-step in vial" if self.labelling_format == "one_step_in_vial" else "")
                + (" | chemical redox cycling" if self.chemical_cycling else ""))

    def with_design(self, **updates) -> "Architecture":
        d = dict(self.design)
        d.update(updates)
        return replace(self, design=tuple(sorted(d.items())))


def check(arch: Architecture) -> list[str]:
    """Return reasons why an architecture is not physically/operationally consistent ([] if fine)."""
    why = []
    chem = CHEMISTRIES[arch.chemistry]
    if arch.scheme not in SCHEMES:
        why.append("unknown scheme")
    if arch.detector.startswith("ida") and not chem["reversible"]:
        why.append("IDA redox cycling needs a chemically reversible product (ascorbate oxidation is irreversible)")
    if arch.chemical_cycling and chem["cycling"] is None:
        why.append("no chemical redox-cycling reagent defined for this chemistry")
    if arch.scheme == "C" and not arch.capture.startswith("chip"):
        why.append("Scheme C integrates capture on the detection chip")
    if arch.capture.startswith("chip") and arch.scheme != "C":
        why.append("chip capture geometries belong to Scheme C")
    if arch.detector == "ida_chip" and arch.scheme != "C":
        why.append("stopped-flow IDA readout in the capture channel requires Scheme C")
    if arch.scheme == "C" and arch.detector != "ida_chip":
        why.append("Scheme C reads out in the chip (ida_chip)")
    if arch.scheme == "A" and arch.capture == "magnetic_beads":
        why.append("bead trap needs reactor isolation for the bead workflow (Scheme B)")
    if arch.labelling_format == "one_step_in_vial" and arch.capture != "magnetic_beads":
        why.append("one-step in-vial format is defined only for pre-dispensed magnetic beads")
    if arch.injection not in INJECTIONS:
        why.append("unknown injection mode")
    return why


# ----------------------------------------------------------------------------------------------------
# registry used by scripts/run_baseline.py
# ----------------------------------------------------------------------------------------------------
BASE_CONFIGS = [
    # (short id, scheme, capture, detector, labelling_format)
    ("A-bed-COUL", "A", "packed_bed", "coulometric", "sequential"),
    ("A-bed-TL", "A", "packed_bed", "thin_layer", "sequential"),
    ("B-bed-TL", "B", "packed_bed", "thin_layer", "sequential"),
    ("B-bed-WJ", "B", "packed_bed", "wall_jet_sencell", "sequential"),
    ("B-bed-SPE", "B", "packed_bed", "wall_jet_spe", "sequential"),
    ("B-bed-COUL", "B", "packed_bed", "coulometric", "sequential"),
    ("B-bed-IDA", "B", "packed_bed", "ida_flow", "sequential"),
    ("B-mono-TL", "B", "monolith", "thin_layer", "sequential"),
    ("B-cap-TL", "B", "capillary", "thin_layer", "sequential"),
    ("B-mag-TL", "B", "magnetic_beads", "thin_layer", "sequential"),
    ("B-mag-IDA", "B", "magnetic_beads", "ida_flow", "sequential"),
    ("B-mag1-IDA", "B", "magnetic_beads", "ida_flow", "one_step_in_vial"),
    ("C-planar-IDA", "C", "chip_planar", "ida_chip", "sequential"),
    ("C-bed-IDA", "C", "chip_bead_bed", "ida_chip", "sequential"),
]

CHEMISTRY_ORDER = ["alp_hqdp", "alp_aap", "sbg_papg", "alp_papp", "hrp_tmb", "sa_polyhrp_tmb"]


def registry(include_variants: bool = True) -> tuple[list[Architecture], list[tuple[str, list[str]]]]:
    """All base configurations x Task 1 chemistries (+ a few plumbing variants).

    Returns (valid architectures, [(name, reasons)] for skipped combinations).
    """
    archs, skipped = [], []
    for (cid, scheme, cap, det, fmt), chem in product(BASE_CONFIGS, CHEMISTRY_ORDER):
        cyc = CHEMISTRIES[chem]["cycling"] is not None
        det_use = det
        a = Architecture(name=f"{cid}/{chem}", scheme=scheme, capture=cap, chemistry=chem, detector=det_use,
                         labelling_format=fmt, chemical_cycling=cyc)
        why = check(a)
        if why:
            skipped.append((a.name, why))
        else:
            archs.append(a)
    if include_variants:
        base = Architecture(name="B-bed-TL/alp_hqdp", scheme="B", capture="packed_bed", chemistry="alp_hqdp",
                            detector="thin_layer")
        archs.append(replace(base, name="B-bed-TL/alp_hqdp/injected-substrate", substrate_delivery="injected"))
        archs.append(replace(base, name="B-bed-TL/alp_hqdp/PLPA97", injection="PLPA_250"))
        archs.append(replace(base, name="B-bed-TL/alp_hqdp/untreated-sample", sample_treatment="untreated"))
        mag = Architecture(name="B-mag-IDA/alp_hqdp", scheme="B", capture="magnetic_beads", chemistry="alp_hqdp",
                           detector="ida_flow")
        archs.append(replace(mag, name="B-mag-IDA/alp_hqdp/PLPA97", injection="PLPA_250"))
    # de-duplicate names
    seen, out = set(), []
    for a in archs:
        if a.name not in seen:
            seen.add(a.name)
            out.append(a)
    return out, skipped


def get(name: str) -> Architecture:
    archs, _ = registry()
    for a in archs:
        if a.name == name:
            return a
    raise KeyError(name)
