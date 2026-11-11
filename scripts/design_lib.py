"""Shared helpers for the Task 4 design scripts (optimisation, robustness, levers).

Nothing here changes model physics: designs are expressed with ``Architecture.with_design(...)`` (design
variables, YAML units) and scenarios with ``ParameterSet.with_values`` / bound changes on a copy of the
parameter set.  All numbers come from params/*.yaml unless a script states a scenario value explicitly.

Conventions
-----------
* "success" for one Monte Carlo draw = LOD <= 1 pg/mL AND ULOQ >= 1000 pg/mL (brief: LOD and 3-log range).
* L_eff = LOD x max(1, 1000 / ULOQ): a single per-draw figure of merit whose median is the optimisation
  objective; P(L_eff <= 1) is exactly P(success).
* The calibration grid is refined to 61 points (numerical setting only; LOD unchanged, ULOQ resolution
  finer) for every design run, including the baseline it is compared with.
"""
from __future__ import annotations

import sys
from dataclasses import replace as _replace
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from elisa_sim import architectures as A            # noqa: E402
from elisa_sim import montecarlo                    # noqa: E402
from elisa_sim.model import evaluate                # noqa: E402
from elisa_sim.params import ParameterSet           # noqa: E402

OUT = ROOT / "results" / "design"
OUT.mkdir(parents=True, exist_ok=True)

TARGET, TIME_LIMIT, RANGE_TOP = 1.0, 60.0, 1000.0
SEED = 20261111
N_OPT = 300          # Monte Carlo draws inside the optimiser (common random numbers, fixed seed)
N_FINAL = 2000       # Monte Carlo draws for reported numbers

# physical / operating limits used as constraints (each justified in docs/05 section 1.1)
_P0 = ParameterSet.load()
# trap/bed screwed directly into the isolation-valve ports (ma.design_levers.min_isolated_connection_length)
MIN_CONNECTION_LENGTH_M = float(_P0.get("ma.design_levers.min_isolated_connection_length", "m"))
# trap efficiency (UNVERIFIED) only assumed at <= baseline flow (ma.design_levers.max_bead_loading_flow)
MAX_BEAD_LOAD_FLOW = float(_P0.get("ma.design_levers.max_bead_loading_flow", "uL/min"))
MIN_FLUSH_VOLUMES = 2.0            # loop volumes; below 2 the loop model and Task 2 table are not validated
MIN_CHIP_CHANNEL_MM = 3.0          # IDA (1 mm) + inlet/outlet margins in the custom chip
REACTOR_DP_LIMIT_MPA = 10.0        # hw.reactors.packed_microbed_10uL.pressure_limit nominal
MIN_TRAP_LENGTH_MM = 1.0           # magnet pole / trap zone length; shorter traps not credible (UNVERIFIED)


def load_ps(points: int = 61) -> ParameterSet:
    ps = ParameterSet.load()
    return ps.with_values({"ma.numerics.calibration_points": points})


def with_bounds(ps: ParameterSet, key: str, value=None, low=None, high=None) -> ParameterSet:
    """Copy of ps whose parameter ``key`` has a different nominal value and/or sampling bounds."""
    params = dict(ps.params)
    p0 = params[key]
    v = p0.value if value is None else value
    lo = p0.low if low is None else low
    hi = p0.high if high is None else high
    params[key] = _replace(p0, value=v, low=lo, high=hi)
    vals = dict(ps.values)
    if key not in ps.pinned:
        vals[key] = v
    out = ParameterSet(params, ps.extra, vals, ps.n)
    out.pinned = set(ps.pinned)
    return out


def pin(ps: ParameterSet, **kv) -> ParameterSet:
    """Pin parameters (keys with '.' passed via dict unpacking) to fixed values (removed from sampling)."""
    return ps.with_values(kv)


def design_of(arch) -> dict:
    return dict(arch.design)


def reactor_pressure_drop_mpa(arch, ps) -> float:
    """Kozeny-Carman pressure drop over the packed capture bed at the loading flow (MPa).
    dP = 150 mu u L (1-eps)^2 / (eps^3 d^2); u = superficial velocity.  Packed / chip-bed captures only."""
    if arch.capture not in ("packed_bed", "chip_bead_bed"):
        return 0.0
    p = ps.with_values(dict(arch.design)) if arch.design else ps
    g = lambda k, u: float(np.asarray(p.get(k, u)).reshape(-1)[0])
    mu = g("ma.fluid.viscosity", "Pa*s")
    Q = g("hw.timing.sample_load_flow", "m^3/s")
    eps = g("hw.reactors.packed_microbed_10uL.void_fraction", "fraction")
    d = g("hw.reactors.packed_microbed_10uL.bead_diameter", "m")
    if arch.capture == "packed_bed":
        V = g("hw.reactors.packed_microbed_10uL.bed_volume", "m^3")
        D = g("ma.geometry.packed_bed_column_inner_diameter", "m")
    else:
        V = g("ma.geometry.chip_bead_bed_volume", "m^3")
        D = g("ma.geometry.chip_bead_bed_inner_diameter", "m")
    area = np.pi * (D / 2) ** 2
    L = V / area
    u = Q / area
    dp = 150 * mu * u * L * (1 - eps) ** 2 / (eps ** 3 * d ** 2)
    return dp / 1e6


def constraint_violations(arch, ps, r=None) -> list[str]:
    """Hard constraints of the design problem (docs/05 section 1.1).  r = nominal Result (computed if None)."""
    why = []
    try:
        r = r or evaluate(arch, ps)
    except ValueError as e:                      # model's own plumbing checks (loop/mode, BSM minimum flow)
        return [str(e)]
    d = design_of(arch)
    if r.time_to_result_min > TIME_LIMIT + 1e-9:
        why.append(f"time to result {r.time_to_result_min:.1f} min > {TIME_LIMIT:g}")
    if r.uloq_pgml < RANGE_TOP:
        why.append(f"nominal ULOQ {r.uloq_pgml:.0f} < {RANGE_TOP:g} pg/mL")
    L = d.get("ma.geometry.reactor_connection_length", ps.values["ma.geometry.reactor_connection_length"])
    if arch.scheme == "B" and L < MIN_CONNECTION_LENGTH_M - 1e-12:
        why.append(f"isolated connection length {L} m < {MIN_CONNECTION_LENGTH_M} m")
    q = d.get("hw.timing.sample_load_flow", ps.values["hw.timing.sample_load_flow"])
    if arch.capture == "magnetic_beads" and q > MAX_BEAD_LOAD_FLOW + 1e-9:
        why.append(f"bead loading flow {q} uL/min > {MAX_BEAD_LOAD_FLOW} (trap efficiency unverified above)")
    nf = d.get("hw.smfl.loop_flush_volumes_for_transfer", ps.values["hw.smfl.loop_flush_volumes_for_transfer"])
    if nf < MIN_FLUSH_VOLUMES - 1e-9:
        why.append(f"loop flush {nf} < {MIN_FLUSH_VOLUMES} loop volumes")
    if arch.scheme == "C":
        Lch = d.get("ma.geometry.chip_channel_length", ps.values["ma.geometry.chip_channel_length"])
        if Lch < MIN_CHIP_CHANNEL_MM - 1e-9:
            why.append(f"chip channel {Lch} mm < {MIN_CHIP_CHANNEL_MM} mm")
    if arch.capture == "magnetic_beads":
        V = d.get("ma.geometry.magnetic_trap_volume", ps.values["ma.geometry.magnetic_trap_volume"])
        D = d.get("ma.geometry.magnetic_trap_tube_inner_diameter", ps.values["ma.geometry.magnetic_trap_tube_inner_diameter"])
        Lt = V / (3.14159265 * (D / 2) ** 2)          # uL / mm^2 = mm
        if Lt < MIN_TRAP_LENGTH_MM - 1e-9:
            why.append(f"trap length {Lt:.2f} mm < {MIN_TRAP_LENGTH_MM} mm")
    dp = reactor_pressure_drop_mpa(arch, ps)
    if dp > REACTOR_DP_LIMIT_MPA:
        why.append(f"bed pressure drop {dp:.1f} MPa > {REACTOR_DP_LIMIT_MPA} MPa")
    return why


def mc(arch, ps, n=N_FINAL, seed=SEED, lod_scale: float = 1.0) -> dict:
    """Monte Carlo summary with the success metric of this task added.

    Work-around for a bug in elisa_sim.montecarlo.used_keys (found in this task, reported in docs/05 s.7):
    for an architecture with a non-empty ``design`` the accessed-key probe is recorded on the copy made by
    apply_design, so NO parameter is sampled.  We therefore apply the design to the parameter set first
    (design keys become pinned and stay unsampled) and run the Monte Carlo on the design-free architecture.
    (The src fix of commit 6cbf85e makes both paths identical; docs/08 s3.2.)

    lod_scale: factor applied to EVERY draw's LOD before the summary and before P is computed (added after the
    final review, docs/08 S13). The chamber designs use 1/0.96 for the analyte lost in the loop -> cup
    transfer; before the review it was applied to the reported LOD only, so P was slightly optimistic. The
    returned lod_* values are already scaled: callers must not multiply them again.
    """
    if arch.design:
        ps = ps.with_values(dict(arch.design))
        arch = _replace(arch, design=())
    m = montecarlo.run(arch, ps, n=n, seed=seed)
    s = m.summary(TARGET, TIME_LIMIT, RANGE_TOP)
    lod = np.asarray(m.result.lod_pgml, float) * float(lod_scale)
    uloq = np.asarray(m.result.uloq_pgml, float)
    if lod_scale != 1.0:
        q = lambda x, a: float(np.nanpercentile(np.where(np.isfinite(x), x, 1e30), a))
        s.update(lod_nominal=float(m.nominal.lod_pgml) * float(lod_scale), lod_median=q(lod, 50),
                 lod_p05=q(lod, 5), lod_p95=q(lod, 95), p_lod_le_target=float(np.mean(lod <= TARGET)),
                 p_lod_and_range=float(np.mean((lod <= TARGET) & (uloq >= RANGE_TOP))))
    s["lod_scale"] = float(lod_scale)
    leff = np.where(np.isfinite(lod), lod, 1e30) * np.maximum(1.0, RANGE_TOP / np.maximum(uloq, 1e-30))
    s["leff_median"] = float(np.median(leff))
    s["p_success"] = float(np.mean(leff <= TARGET))
    s["p_lod_only"] = float(np.mean(lod <= TARGET))
    s["p_lod_le_3"] = float(np.mean(lod <= 3.0))
    s["uloq_nominal"] = float(m.nominal.uloq_pgml)
    s["blank_equiv_nominal"] = float(m.nominal.diagnostics["blank_equivalent_pgml"]) * float(lod_scale)
    s["lod_draws"] = lod
    s["_mc"] = m
    return s


def fmt(x, nd=2):
    if x is None:
        return ""
    if isinstance(x, str):
        return x
    x = float(x)
    if not np.isfinite(x) or x >= 1e29:
        return "inf"
    return f"{x:.{nd}g}"


def row_text(label, s, r=None):
    return (f"| {label} | {fmt(s['lod_nominal'])} | {fmt(s['lod_median'])} [{fmt(s['lod_p05'])}-{fmt(s['lod_p95'])}] "
            f"| {s['p_lod_only']:.2f} | {s['p_success']:.2f} | {fmt(s['uloq_nominal'], 2)} | "
            f"{s['time_to_result_min']:.1f} |")


TABLE_HEAD = ("| Design | LOD nominal (pg/mL) | LOD MC median [5-95 %] (pg/mL) | P(LOD<=1) | P(LOD<=1 and ULOQ>=1000) "
              "| ULOQ nominal (pg/mL) | Time to result (min) |\n|---|---|---|---|---|---|---|\n")


# --------------------------------------------------------------------------------------------------------
# Candidate formats and their design spaces (discrete grids; values in YAML units)
# --------------------------------------------------------------------------------------------------------
def base_arch(key: str):
    if key == "OS":
        return A.get("B-mag1-IDA/alp_hqdp")
    if key == "SQ":
        return A.get("B-mag-IDA/alp_hqdp")
    if key == "FRB":
        return A.get("B-bed-IDA/alp_hqdp")
    if key == "FRC":
        return A.get("C-bed-IDA/alp_hqdp")
    if key == "CAP":
        return A.get("B-cap-TL/alp_hqdp")
    raise KeyError(key)


FORMAT_LABEL = {
    "OS": "One-step magnetic beads (beads + conjugate in the vial), flow IDA",
    "SQ": "Sequential magnetic beads (beads in the vial, conjugate injected), flow IDA",
    "FRB": "Fixed packed micro-bed (regenerated), Scheme B, flow IDA",
    "FRC": "Fixed chip bead bed upstream of an on-chip IDA (regenerated), Scheme C",
    "CAP": "Fixed open capillary (regenerated), Scheme B, thin-layer cell",
}

_COMMON_DET = {
    "hw.timing.accumulation_time": [5, 7.5, 10, 12.5, 15],
    "ma.readout.sweep_flow": [10, 20, 50],
    "hw.timing.readout_time": [1, 1.5, 2, 3],
    "ma.chemistries.alp_hqdp.substrate_concentration": [3e-4, 1e-3, 3e-3],
}

SPACES = {
    "OS": {
        "ma.geometry.reactor_connection_length": [0.01, 0.02, 0.05, 0.1],
        "chem.surfaces.bead_number_per_100uL_digital_ELISA": [2e5, 3e5, 5e5, 7e5, 1e6, 1.5e6, 2e6],
        "ma.timing.in_vial_incubation": [20, 25, 30, 35, 38.5, 45],
        "chem.antibodies.conc_detection_antibody_typical": [2e-10, 3e-10, 5e-10, 7e-10, 1e-9, 2e-9],
        "ma.geometry.magnetic_trap_volume": [0.5, 1, 2, 3, 5],
        "ma.geometry.magnetic_trap_tube_inner_diameter": [0.25, 0.5, 0.75, 1.0, 1.5],
        "hw.timing.sample_load_flow": [50, 75, 100],
        "hw.smfl.loop_flush_volumes_for_transfer": [2, 2.5, 3, 4],
        "ma.timing.post_sample_wash": [1, 2],   # < 1 min not allowed: wash efficiency is not modelled
        **_COMMON_DET,
    },
    "SQ": {
        "ma.geometry.reactor_connection_length": [0.01, 0.02, 0.05, 0.1],
        "chem.surfaces.bead_number_per_100uL_digital_ELISA": [5e5, 1e6, 1.5e6, 2e6, 3e6],
        "ma.timing.in_vial_incubation": [15, 20, 25, 29.5, 35],
        "chem.antibodies.conc_detection_antibody_typical": [3e-10, 1e-9, 3e-9, 1e-8],
        "ma.delivery.conjugate_injection_volume": [10, 20, 50, 75],
        "hw.timing.conjugate_stopped_flow_incubation": [2, 3, 5, 10],
        "hw.timing.wash_after_conjugate": [2, 3],   # < 2 min not allowed: free-conjugate removal not modelled
        "ma.geometry.magnetic_trap_volume": [0.5, 1, 2, 3, 5],
        "ma.geometry.magnetic_trap_tube_inner_diameter": [0.25, 0.5, 0.75, 1.0, 1.5],
        "hw.timing.sample_load_flow": [50, 75, 100],
        "hw.smfl.loop_flush_volumes_for_transfer": [2, 2.5, 3, 4],
        **_COMMON_DET,
    },
    "FRB": {
        "hw.reactors.packed_microbed_10uL.bed_volume": [0.25, 0.5, 1, 2, 4, 10],
        "hw.reactors.packed_microbed_10uL.bead_diameter": [10, 20, 35, 50],
        "ma.geometry.packed_bed_column_inner_diameter": [0.25, 0.5, 1.0],
        "ma.geometry.reactor_connection_length": [0.01, 0.02, 0.05, 0.1],
        "hw.timing.sample_load_flow": [10, 15, 20, 25, 30, 40, 50, 100],
        "hw.smfl.loop_flush_volumes_for_transfer": [2, 2.5, 3],
        "ma.delivery.conjugate_injection_volume": [10, 20, 50],
        "hw.timing.conjugate_stopped_flow_incubation": [2, 3, 5, 10],
        "chem.antibodies.conc_detection_antibody_typical": [3e-10, 1e-9, 3e-9],
        "hw.timing.wash_after_conjugate": [2, 3],
        **_COMMON_DET,
    },
    "FRC": {
        "ma.geometry.chip_bead_bed_volume": [0.1, 0.25, 0.5, 1, 2],
        "ma.geometry.chip_bead_bed_inner_diameter": [0.2, 0.3, 0.5],
        "hw.reactors.packed_microbed_10uL.bead_diameter": [10, 20, 35, 50],
        "ma.geometry.chip_channel_length": [3, 5, 10],
        "ma.geometry.chip_channel_width": [0.2, 0.3, 0.5],
        "hw.timing.sample_load_flow": [10, 15, 20, 25, 30, 40, 50, 100],
        "hw.smfl.loop_flush_volumes_for_transfer": [2, 2.5, 3],
        "ma.delivery.conjugate_injection_volume": [10, 20, 50],
        "hw.timing.conjugate_stopped_flow_incubation": [2, 3, 5, 10],
        "chem.antibodies.conc_detection_antibody_typical": [3e-10, 1e-9, 3e-9],
        "hw.timing.wash_after_conjugate": [2, 3],
        "hw.timing.accumulation_time": [5, 7.5, 10, 12.5, 15],
        "hw.timing.readout_time": [1, 1.5, 2, 3],
        "ma.chemistries.alp_hqdp.substrate_concentration": [3e-4, 1e-3, 3e-3],
    },
    "CAP": {
        "ma.geometry.capillary_inner_diameter": [50, 100, 150, 250],
        "ma.geometry.capillary_length": [0.1, 0.2, 0.3, 0.5, 1.0],
        "ma.geometry.reactor_connection_length": [0.01, 0.02, 0.05, 0.1],
        "hw.timing.sample_load_flow": [10, 15, 20, 25, 30, 50, 100],
        "hw.smfl.loop_flush_volumes_for_transfer": [2, 2.5, 3],
        "hw.timing.conjugate_stopped_flow_incubation": [2, 3, 5, 10],
        "chem.antibodies.conc_detection_antibody_typical": [3e-10, 1e-9, 3e-9],
        **_COMMON_DET,
    },
}

# design variables whose optimum would rest on an UNVERIFIED parameter (flagged in the report)
ASSUMPTION_FLAGS = {
    "ma.chemistries.alp_hqdp.substrate_concentration": "gain depends on HQDP Km (UNVERIFIED) and free-HQ impurity (UNVERIFIED)",
    "ma.timing.in_vial_incubation": "NSB assumed linear in time (UNVERIFIED); unstirred capture factor UNVERIFIED",
    "chem.surfaces.bead_number_per_100uL_digital_ELISA": "bead NSB surface factor and unstirred capture factor UNVERIFIED",
    "ma.geometry.reactor_connection_length": "tubing NSB surface factor UNVERIFIED (direction certain, size not)",
    "ma.geometry.magnetic_trap_tube_inner_diameter": "trap-wall NSB uses the tubing surface factor (UNVERIFIED)",
    "ma.geometry.magnetic_trap_volume": "trap efficiency at smaller volume UNVERIFIED",
    "hw.timing.sample_load_flow": "bead traps: trap efficiency vs flow UNVERIFIED; beds: Wilson-Geankoplis (recalled) + kon/density",
    "hw.reactors.packed_microbed_10uL.bead_diameter": "packed-bed surface factor UNVERIFIED; capture via Wilson-Geankoplis",
    "hw.reactors.packed_microbed_10uL.bed_volume": "packed-bed surface factor UNVERIFIED",
    "ma.geometry.chip_bead_bed_volume": "packed-bed and chip surface factors UNVERIFIED",
    "hw.timing.conjugate_stopped_flow_incubation": "linear irreversible NSB vs equilibrating labelling (koff_detection, unscreened)",
    "chem.antibodies.conc_detection_antibody_typical": "linear NSB (UNVERIFIED) and detection-antibody KD; in OS also keeps ULOQ >= 1000 via Pi inhibition (Ki INHERITED)",
    "ma.readout.sweep_flow": "flow-IDA generator conversion (slit solution, verified limits) x IDA amplification held flow-independent (empirical)",
    "hw.timing.readout_time": "shorter window = less integrated noise/drift; elution in window from tanks-in-series (UNVERIFIED tanks)",
    "hw.timing.accumulation_time": "more product vs fixed free-HQ impurity and drift (both UNVERIFIED); limited by Pi inhibition (ULOQ)",
    "hw.smfl.loop_flush_volumes_for_transfer": "loop-transfer model (verified vs Task 2 table); time saved is re-used elsewhere",
    "ma.geometry.chip_bead_bed_inner_diameter": "geometry only (bed area unchanged); small effect",
    "ma.geometry.chip_channel_length": "chip-wall NSB area (chip surface factor UNVERIFIED, 1-100)",
    "ma.geometry.chip_channel_width": "chip-wall NSB area (chip surface factor UNVERIFIED, 1-100)",
    "ma.geometry.packed_bed_column_inner_diameter": "geometry only (W-G film transfer); small effect",
    "ma.delivery.conjugate_injection_volume": "linear NSB (UNVERIFIED); plug dispersion from loop model (verified)",
}


# --------------------------------------------------------------------------------------------------------
# Bench values entered the way automation/elisa_auto/model_feedback.py enters them (docs/06 s9.3). Moved here
# after the final review (docs/08 B3) so the G1 decision table and the bench feedback use ONE implementation.
# --------------------------------------------------------------------------------------------------------
# A bench measurement of the label factor is a measurement of the absolute k_eff on the actual beads
# (docs/06 E1.3: factor = k_eff / 4e-11 m/s). The model computes k_eff = label factor x
# chem.nsb.nsb_effective_rate_constant x ma.nsb.surface_factor_magnetic_beads and the Monte Carlo samples the
# last two as well; left free they would re-spread the measured value over ~50x. So when the label factor is
# measured, the reference rate and the bead surface factor are pinned at their nominal values (4e-11 m/s, 1).
COUPLED = {"ma.nsb.label_factor_igg_enzyme_conjugate": ("chem.nsb.nsb_effective_rate_constant",
                                                        "ma.nsb.surface_factor_magnetic_beads")}


def apply_bench_values(ps: ParameterSet, measured: dict, notes: list | None = None) -> ParameterSet:
    """measured: {key: {value, low?, high?}} -> copy of ps narrowed to the bench values (coupled factors pinned)."""
    for key, partners in COUPLED.items():
        if key in measured:
            for k2 in partners:
                if k2 not in measured and k2 in ps.params:
                    v = ps.params[k2].value
                    ps = with_bounds(ps, k2, value=v, low=v, high=v)
                    if notes is not None:
                        notes.append(f"{k2} pinned at {v:g} because {key} was measured on the actual beads")
    for key, v in measured.items():
        if key not in ps.params:
            raise KeyError(f"unknown model parameter {key!r} (see params/*.yaml)")
        val = float(v["value"])
        lo, hi = float(v.get("low", val)), float(v.get("high", val))
        if not (lo <= val <= hi):
            raise ValueError(f"{key}: low <= value <= high violated")
        ps = with_bounds(ps, key, value=val, low=lo, high=hi)
    return ps


def l4_transfer(ps: ParameterSet) -> ParameterSet:
    """Lever L4 (immune-complex transfer) on top of whatever label factor ps holds: factor x NSB/efficiency
    (ma.design_levers nominal 0.1 / 0.7), bounds scaled alike (OUTSIDE MODEL as physics; docs/05 s2)."""
    k = "ma.nsb.label_factor_igg_enzyme_conjugate"
    m = (float(ps.params["ma.design_levers.immune_complex_transfer_nsb_factor"].value)
         / float(ps.params["ma.design_levers.immune_complex_transfer_efficiency"].value))
    p = ps.params[k]
    v = float(np.asarray(ps.values[k]).reshape(-1)[0]) if k in ps.pinned else p.value
    out = with_bounds(ps, k, value=p.value * m, low=p.low * m, high=p.high * m)
    if k in ps.pinned:
        out = out.with_values({k: v * m})
    return out


# G1 decision rule fixed before any Stage-1 data exist (docs/06 s4.11, automation/config/gates.yaml G1_rule;
# reasoning in docs/08 'Resolution of findings', B3). P = model P(success) of a design with the bench values
# entered by apply_bench_values (thin-layer default detector, chamber approximation with the S13 corrections).
G1_GO_MIN = 0.30
G1_LEVER_MIN = 0.10


def g1_decision(p_no_lever: dict, p_with_l4: dict) -> str:
    """p_*: {design: P(success)} over the ADMISSIBLE designs (P-chamb, S-chamb, B-bed)."""
    p0 = max(p_no_lever.values())
    pl = max([p0] + list(p_with_l4.values()))
    if p0 >= G1_GO_MIN:
        return "GO"
    if pl >= G1_LEVER_MIN:
        return "GO-WITH-LEVER" if p0 >= G1_LEVER_MIN else "GO-WITH-LEVER (Stage 1C first; Stage-2 order waits for G1')"
    return "STOP"
