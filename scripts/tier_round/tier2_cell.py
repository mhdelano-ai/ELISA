#!/usr/bin/env python3
"""Tier-2 flow cell with the bead bed inside the cell (docs/34): model cases, hydraulics, mechanics at 500 psi.

  python scripts/tier_round/tier2_cell.py [--n 2000] [--quick]
writes results/tier_round/tier2_cell.md and tier2_cell.json (not with --quick).

The cell's dimensions come from cad/elisa_cad/tier2_cell/params.py (the same file the CAD model reads).  The
assay is the unchanged tier 2 of docs/30 (`run_tiers.t2()`); only the bed holder, the retainer, the walls around
the bed and the cell are replaced.  tierkit.py, designs.py, src/ and params/ are not edited.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))
import designs as D  # noqa: E402
import run_tiers as R  # noqa: E402
import tierkit as tk  # noqa: E402

_spec = importlib.util.spec_from_file_location("t2cell_params", ROOT / "cad/elisa_cad/tier2_cell/params.py")
P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P)

OUT = ROOT / "results" / "tier_round"
PSI = 6894.76                      # Pa
P_RATED = 500.0 * PSI              # the user's requirement
UL_MIN = 1e-9 / 60.0               # m3/s per uL/min

# ---- beads ---------------------------------------------------------------------------------------------------
M280 = dict(key="M-280", label="Dynabeads M-280 Streptavidin, 2.8 um", d_p=2.8e-6, V_bed_uL=0.019)
# the same bead area (24 mm2) in larger beads: volume scales with the diameter
PS12 = dict(key="PS 10-14", label="streptavidin polystyrene 10-14 um (taken as 12 um), same bead area",
            d_p=12e-6, V_bed_uL=0.019 * 12.0 / 2.8)


# ---- retainer area --------------------------------------------------------------------------------------------
def retainer_area(bore_d, membrane=True):
    """Wetted area (mm2) of the retainer inside the bore cross-section: (low, nominal, high).  UNVERIFIED.

    Screen (VICI 2SR1, 0.075 mm): the vendor does not publish its construction.  Low: woven wire cloth, specific
    surface 4 (1 - eps) / d_wire with eps 0.5, wire 25 um.  High: a porous body, 4 eps / d_pore with eps 0.3 and
    2 um pores.  Membrane (track-etched, 1 um pores, 2e5 per mm2 [S]): pore walls N pi d t plus both faces, for
    6 and 15 um thickness [S].  Liquid that diffuses sideways into the clamped part of the screen is not counted."""
    a = math.pi * bore_d ** 2 / 4.0
    v_screen = a * P.SCREEN_T
    s_lo, s_hi = v_screen * 4 * 0.5 / 0.025, v_screen * 4 * 0.3 / 0.002
    out = [s_lo, math.sqrt(s_lo * s_hi), s_hi]
    if membrane:
        wall = P.MEMBRANE_PORES_PER_MM2 * math.pi * P.MEMBRANE_PORE_D
        m = [a * (wall * t + 2.0) for t in (0.006, P.MEMBRANE_T, 0.015)]
        out = [o + mm for o, mm in zip(out, m)]
    return tuple(out)


# ---- the design in the kit ------------------------------------------------------------------------------------
def cell_design(beads=M280, bore_d=None, retainer_mm2=None, h=None, membrane=None, name=None, v_dead=None,
                **kw):
    """docs/30 tier 2 with the bed in the body of the cell."""
    bore_d = P.BED_D if bore_d is None else bore_d
    membrane = (beads["d_p"] < 7e-6) if membrane is None else membrane       # screen alone is absolute at 7-8 um
    if retainer_mm2 is None:
        retainer_mm2 = retainer_area(bore_d, membrane)[1]
    V_bed = beads["V_bed_uL"]                                               # uL = mm3
    L_bed = V_bed / (math.pi * bore_d ** 2 / 4.0)
    L_free = max(P.INLET_FLOOR - L_bed, 0.0)                                # empty bore above the bed
    d = R.t2(d_p=beads["d_p"], V_bed_uL=V_bed, column_id=bore_d * 1e-3, retainer_area=retainer_mm2 * 1e-6,
             V_dead_uL=P.EXIT_VOLUME_UL if v_dead is None else v_dead,
             V_transit_uL=(P.EXIT_VOLUME_UL if v_dead is None else v_dead) + 0.1, h=(P.GAP if h is None else h) * 1e-3,
             **kw)
    d["cell"].update(R=P.CHAMBER_R * 1e-3, bore_radius=0.5 * P.EXIT_D * 1e-3, bore_length=P.EXIT_LENGTH * 1e-3)
    d["bed"]["bore_area"] = P.EXIT_WALL * 1e-6                               # exit bore, at the lid factor
    # the hole of the elastomer washer below the screen is counted with the retainer, at the frit factor (an
    # elastomer factor has no source; UNVERIFIED)
    d["bed"]["extra_area"] = d["bed"]["extra_area"] + P.WASHER_WALL * 1e-6
    d["bed"]["upstream_area"] = math.pi * bore_d * L_free * 1e-6 + D.LINE_AREA   # bore above the bed + line
    d["name"] = name or f"cell, {beads['key']}, bore {bore_d} mm, retainer {retainer_mm2:.2g} mm2"
    d["_geom"] = dict(L_bed_mm=L_bed, L_free_mm=L_free, retainer_mm2=retainer_mm2, bore_d=bore_d,
                      membrane=membrane)
    return d


def run(design, ps, n):
    s = tk.monte_carlo(tk.evaluate_bed, design, ps, n=n)
    nom = s["_nominal"]
    g = nom.diagnostics
    f = lambda k: float(np.asarray(g[k]).reshape(-1)[0])
    out = {k: v for k, v in s.items() if not k.startswith("_")}
    out.update(capture=f("capture_fraction"), k_m=f("k_m"), k_r=f("k_r"), dp_load_bar=f("bed_dp_Pa") / 1e5, N_nsb_bed=f("N_nsb_bed"),
               N_nsb_extra=f("N_nsb_extra"), eta=f("cell_conversion"), geom=design.get("_geom"))
    return out


# ---- hydraulics -------------------------------------------------------------------------------------------------
def hydraulics(ps, beads, bore_d, membrane):
    mu = float(ps.params["ma.fluid.viscosity"].value)
    a = math.pi * (bore_d * 1e-3) ** 2 / 4.0
    L_bed = beads["V_bed_uL"] * 1e-9 / a
    rows = {}
    for q in (3.4, 5.0, 50.0, 80.0, 200.0):
        Q = q * UL_MIN
        u = Q / a
        bed = tk.kozeny_carman_dp(mu, u, beads["d_p"], 0.4, L_bed)
        hp = lambda d_mm, L_mm: 128.0 * mu * (L_mm * 1e-3) * Q / (math.pi * (d_mm * 1e-3) ** 4)
        # membrane: Hagen-Poiseuille in each pore; screen: capillary bundle, eps 0.3, 2 um, tortuosity 2 (UNVERIFIED)
        n_pores = P.MEMBRANE_PORES_PER_MM2 * a * 1e6
        mem = 128.0 * mu * (P.MEMBRANE_T * 1e-3) * (Q / n_pores) / (math.pi * (P.MEMBRANE_PORE_D * 1e-3) ** 4) \
            if membrane else 0.0
        scr = 2.0 * 32.0 * mu * (P.SCREEN_T * 1e-3) * u / (0.3 * (2e-6) ** 2)
        bore = hp(bore_d, P.INLET_FLOOR) + hp(P.EXIT_D, P.EXIT_LENGTH)
        gap = 6.0 * mu * Q * math.log(P.RING_R0 / (0.5 * P.EXIT_D)) / (math.pi * (P.GAP * 1e-3) ** 3)
        out_path = hp(P.RISER_PLATE_D, P.PLATE_T - P.RING_DEPTH) + hp(P.RISER_BODY_D, P.OUTLET_Z + 3.3)
        rows[q] = dict(bed=bed, membrane=mem, screen=scr, bores=bore, gap=gap, outlet=out_path,
                       total=bed + mem + scr + bore + gap + out_path)
    return rows


# ---- mechanics at the rated pressure ----------------------------------------------------------------------------
def mechanics():
    """Forces and stresses with the whole liquid path at 500 psi (the bed itself needs a few bar, section 4).
    PEEK properties are typical values for unfilled PEEK, UNVERIFIED (take them from the certificate of the stock)."""
    E, SHEAR, COMP = 3600.0, 53.0, 118.0          # MPa: modulus, shear strength, compressive yield (UNVERIFIED)
    p = P_RATED / 1e6                             # MPa = N/mm2
    A = lambda d: math.pi * d * d / 4.0
    F_strip = p * A(P.GROOVE_STRIP_OD)            # worst case: pressure out to the outer wall of the groove
    F_iface = p * A(P.GROOVE_IFACE_OD)            # worst case: the film between body and plate is at pressure
    oring_n_per_mm = 1.0                          # UNVERIFIED: 1 mm cord, 70 Shore A, 25 % squeeze
    F_or_strip = oring_n_per_mm * math.pi * (P.ORING_STRIP[0] + P.ORING_STRIP[1])
    F_or_iface = oring_n_per_mm * math.pi * (P.ORING_IFACE[0] + P.ORING_IFACE[1])
    torque_m4 = 0.5                               # N m, CHOICE
    preload_m4 = torque_m4 / (0.2 * 0.004)        # N per screw, T = 0.2 d F
    need_main = F_strip + F_or_strip + F_iface + F_or_iface
    le = 8.0 - P.PLATE_T                          # M2.5 x 8 flat-head screw: engagement in the body
    strip_out = 0.5 * math.pi * 2.5 * le * SHEAR  # N per M2.5 thread in PEEK
    per_m25 = (F_iface + F_or_iface) / 4.0
    bearing = preload_m4 / (math.pi / 4.0 * (8.0 ** 2 - P.M4_CLEAR ** 2))   # under an 8 mm washer (DIN 433)
    # body and plate as one beam across the strip pocket, strip force at mid-span
    I_beam = (P.X1 - P.X0) * P.BODY_T ** 3 / 12.0
    sag = F_strip * P.POCKET_W ** 3 / (48.0 * E * I_beam)
    # floor of the inlet port (body floor + plate, not bonded) as a clamped disc under the fitting's seating force
    F_fit = 0.3 / (0.2 * 0.00635)                 # N at 0.3 N m on 1/4-28 (finger tight, UNVERIFIED)
    Dfl = E * (P.INLET_FLOOR ** 3 + P.PLATE_T ** 3) / (12.0 * (1 - 0.38 ** 2))
    floor = F_fit * (0.5 * P.PORT_TAP_DRILL) ** 2 / (16.0 * math.pi * Dfl)
    # retainer: the washer is the spring that presses screen and membrane against the body face.
    # Squeeze over the tolerances: pocket +-0.01, sheet +-0.02, membrane 6-15 um, screen +-0.005 (UNVERIFIED).
    E_R = 6.0                                     # MPa, FKM 75 Shore A (UNVERIFIED)
    A_w = A(P.WASHER_OD) - A(P.WASHER_ID)
    S_w = A_w / (math.pi * (P.WASHER_OD + P.WASHER_ID) * P.WASHER_T)        # shape factor (Gent)
    def washer_force(t, depth, mem, scr):
        h = depth - mem - scr
        e = max(1.0 - h / t, 0.0)
        return E_R * (1.0 + 2.0 * S_w ** 2) * e * A_w, e
    lo = washer_force(P.WASHER_T - 0.02, P.RET_POCKET_DEPTH + 0.01, 0.006, P.SCREEN_T - 0.005)
    no = washer_force(P.WASHER_T, P.RET_POCKET_DEPTH, P.MEMBRANE_T, P.SCREEN_T)
    hi = washer_force(P.WASHER_T + 0.02, P.RET_POCKET_DEPTH - 0.01, 0.015, P.SCREEN_T + 0.005)
    A_clamp = A(P.MEMBRANE_DISC_D) - A(P.BED_D)                             # band where the membrane seals
    Dpl = E * P.PLATE_T ** 3 / (12.0 * (1 - 0.38 ** 2))
    plate_k = 16.0 * math.pi * Dpl * 1e-3 / (math.hypot(*P.M25_XY[0]) ** 2)   # N per um, clamped disc (soft bound)
    squeeze = lambda cs, gland: 1.0 - gland / cs
    return dict(
        p_MPa=p, F_strip_N=F_strip, F_iface_N=F_iface, F_oring_strip_N=F_or_strip, F_oring_iface_N=F_or_iface,
        m4_torque_Nm=torque_m4, m4_preload_total_N=4 * preload_m4, main_needed_N=need_main,
        main_margin=4 * preload_m4 / need_main, m25_load_each_N=per_m25, m25_strip_out_N=strip_out,
        m25_margin=strip_out / per_m25, bearing_MPa=bearing, bearing_margin=COMP / bearing,
        sag_um=sag * 1e3, fitting_force_N=F_fit, floor_deflection_um=floor * 1e3,
        washer_squeeze=[lo[1], no[1], hi[1]], washer_force_N=[lo[0], no[0], hi[0]],
        membrane_clamp_MPa=[f / A_clamp for f in (lo[0], no[0], hi[0])],
        plate_bow_um=hi[0] / plate_k, pocket_area_mm2=A(P.RET_POCKET_D), washer_E_MPa=E_R,
        bed_force_N=p * A(P.BED_D),
        squeeze_strip=[squeeze(P.ORING_STRIP[1], P.GROOVE_STRIP_DEPTH + g)
                       for g in (P.GAP - P.GAP_TOL, P.GAP, P.GAP + P.GAP_TOL)],
        squeeze_iface=squeeze(P.ORING_IFACE[1], P.GROOVE_IFACE_DEPTH),
        peek_assumed=dict(E_MPa=E, shear_MPa=SHEAR, compressive_yield_MPa=COMP))


def side_paths(ps):
    """Two secondary flow paths, as ratios of resistances (Derived; creeping flow).

    Symmetry: the liquid reaches the riser either straight across the thin layer or across the layer on the far
    side and half-way round the collecting groove.  By-pass: a film of height `film` between body and plate (set by
    the flatness of the two faces; nothing stands proud) joins the edge of the retainer pocket to the cross channel
    past the electrode (width taken as 2 mm)."""
    mu = float(ps.params["ma.fluid.viscosity"].value)
    R_gap = 6.0 * mu * math.log(P.RING_R0 / (0.5 * P.EXIT_D)) / (math.pi * (P.GAP * 1e-3) ** 3)
    w, h = (P.RING_R1 - P.RING_R0) * 1e-3, P.RING_DEPTH * 1e-3
    a, b = max(w, h), min(w, h)
    L_half = math.pi * 0.5 * (P.RING_R0 + P.RING_R1) * 1e-3
    R_groove = 12.0 * mu * L_half / (a * b ** 3 * (1.0 - 0.63 * b / a)) / 2.0      # two half-rings in parallel
    hp = lambda d_mm, L_mm: 128.0 * mu * (L_mm * 1e-3) / (math.pi * (d_mm * 1e-3) ** 4)
    R_main = hp(P.EXIT_D, P.EXIT_LENGTH) + R_gap + hp(P.RISER_PLATE_D, P.PLATE_T - P.RING_DEPTH)
    L_film = (abs(P.RISER_PLATE_X) - P.CHANNEL_W / 2.0 - P.RET_POCKET_D / 2.0) * 1e-3
    bypass = {}
    for film_um in (5, 15, 25, 45):
        R_film = 12.0 * mu * L_film / (2e-3 * (film_um * 1e-6) ** 3)
        bypass[film_um] = R_main / (R_main + R_film)
    return dict(far_to_near_flow=R_gap / (R_gap + R_groove), bypass_fraction=bypass)


def scans(ps):
    """Nominal LOD and captured fraction against bead size and bore, in this cell (retainer at its nominal area
    for the 0.5 mm bore throughout, so that only the beads or the bore change)."""
    ret = retainer_area(P.BED_D, True)[1]
    ev = lambda d: tk.evaluate_bed(d, ps)
    out = dict(beads=[], bore=[])
    for dp in (1.0, 2.8, 4.5, 10.0, 20.0):
        row = dict(d_um=dp)
        for tag, V in (("same_volume", 0.019), ("same_area", 0.019 * dp / 2.8)):
            r = ev(cell_design(dict(key=f"{dp} um", d_p=dp * 1e-6, V_bed_uL=V), retainer_mm2=ret, membrane=True))
            row[tag] = dict(V_nL=V * 1e3, capture=float(np.ravel(r.diagnostics["capture_fraction"])[0]),
                            lod=float(r.lod_pgml), dp_bar=float(np.ravel(r.diagnostics["bed_dp_Pa"])[0]) / 1e5)
        out["beads"].append(row)
    for bore in (0.15, 0.2, 0.3, 0.5):
        r = ev(cell_design(bore_d=bore, retainer_mm2=ret))
        out["bore"].append(dict(bore=bore, capture=float(np.ravel(r.diagnostics["capture_fraction"])[0]),
                                lod=float(r.lod_pgml), dp_bar=float(np.ravel(r.diagnostics["bed_dp_Pa"])[0]) / 1e5))
    return out


def geometry_table():
    rows = []
    for beads in (M280, PS12):
        for bore in (P.BED_D, 0.3):
            a = math.pi * bore ** 2 / 4.0
            L = beads["V_bed_uL"] / a
            mem = beads["d_p"] < 7e-6
            rows.append(dict(beads=beads["key"], bore=bore, bed_nL=beads["V_bed_uL"] * 1e3, L_bed=L,
                             layers=L / (beads["d_p"] * 1e3), L_free=P.INLET_FLOOR - L,
                             wall_above=math.pi * bore * max(P.INLET_FLOOR - L, 0.0),
                             retainer=retainer_area(bore, mem), membrane=mem))
    return rows


def fmt(x, nd=2):
    return "inf" if (not np.isfinite(x) or x > 1e29) else f"{x:.{nd}g}"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--quick", action="store_true", help="n = 200, nothing written")
    a = ap.parse_args(argv)
    n = 200 if a.quick else a.n
    warnings.filterwarnings("ignore")
    ps = R.base_params()
    lo, nominal, hi = retainer_area(P.BED_D, True)

    cases = [
        ("ref", "docs/30 tier 2: capillary bed in the inlet bore of the MicruX cell", R.t2(), ps),
        ("cell", "**this cell, M-280, membrane on the screen (retainer 5 mm², nominal)**", cell_design(), ps),
        ("ret_lo", f"retainer {lo:.1f} mm² (low estimate)", cell_design(retainer_mm2=lo), ps),
        ("ret_hi", f"retainer {hi:.0f} mm² (high estimate)", cell_design(retainer_mm2=hi), ps),
        ("ret_40", "retainer 40 mm² (a 0.5 µm sintered frit in place of membrane and screen)",
         cell_design(retainer_mm2=40.0), ps),
        ("bore03", "bed bore 0.3 mm (variant body; retainer scales with the bore area)",
         cell_design(bore_d=0.3), ps),
        ("ps12", "streptavidin polystyrene 10–14 µm, same bead area, screen alone", cell_design(PS12), ps),
        ("ps12_f1", "the same if those beads bind conjugate like tube-washed M-280 (factor 1)",
         cell_design(PS12, bed_factor_key=R.MB), ps),
        ("ps12_f10", "the same if they bind 10 times more than that (factor 10)", cell_design(PS12),
         R.L.with_bounds(ps, "ma.nsb.surface_factor_packed_bed", value=10.0, low=3.0, high=100.0)),
        ("m280_f1", "M-280 behave as when washed in tubes (factor 1)", cell_design(bed_factor_key=R.MB), ps),
        ("vdead015", "exit bore of 0.15 µL instead of 0.49 µL (a shorter or narrower bore)",
         cell_design(v_dead=0.15), ps),
        ("gap005", "gap 0.05 mm", cell_design(h=0.05), ps),
        ("gap02", "gap 0.20 mm", cell_design(h=0.20), ps),
        ("nodecay", "the substrate's background does not decay", cell_design(), R.NODECAY(ps)),
        ("p01", "only 1 % of the turnovers electroactive, read as specified", cell_design(), R.P01(ps)),
        ("p01_fast", "the same, sweep at 20 µL/min for 22 s", cell_design(Q_read=20.0, t_read=22.0), R.P01(ps)),
        ("screened", "screened detection reagent and substrate lot (L6 + L7)", cell_design(),
         R.chain(R.L6, R.L7)(ps)),
    ]
    res = {}
    for key, label, design, pset in cases:
        res[key] = run(design, pset, n)
        res[key]["label"] = label
        print(f"{key:9s} LOD {res[key]['lod_nominal']:.3g}  median {res[key]['lod_median']:.3g}", flush=True)

    hyd = {b["key"]: hydraulics(ps, b, P.BED_D, b["d_p"] < 7e-6) for b in (M280, PS12)}
    hyd["M-280, bore 0.2 mm x 0.6 mm (docs/30)"] = hydraulics(ps, M280, 0.2, False)
    mech = mechanics()
    # upper bound of the force that pushes the retainer stack off the body face: the pressure drop through bed,
    # membrane and screen acting on the whole pocket area
    mech["stack_push_N"] = {q: (r["bed"] + r["membrane"] + r["screen"]) * mech["pocket_area_mm2"] * 1e-6
                            for q, r in hyd["M-280"].items()}
    geo = geometry_table()
    side = side_paths(ps)
    scan = scans(ps)

    # ---- checks -------------------------------------------------------------------------------------------
    tiers = json.loads((OUT / "tiers.json").read_text())
    def find(o):
        if isinstance(o, dict):
            if o.get("name", "").startswith("T2 bed 0.019") and "lod_nominal" in o:
                return o
            for v in o.values():
                r = find(v)
                if r:
                    return r
        if isinstance(o, list):
            for v in o:
                r = find(v)
                if r:
                    return r
        return None
    ref = find(tiers)
    checks_lift = mech["stack_push_N"][80.0] < 0.5 * mech["washer_force_N"][0]
    checks = [
        ("the unchanged tier 2 reproduces tiers.json (nominal LOD)", ref is not None
         and abs(res["ref"]["lod_nominal"] / ref["lod_nominal"] - 1) < 1e-6,
         f"{res['ref']['lod_nominal']:.6g} vs {ref['lod_nominal'] if ref else None}"),
        ("gap from the stack is 0.10 mm", abs(P.GAP - 0.10) < 1e-9, f"{P.GAP:.3f}"),
        ("dead volume between retainer and electrode (exit bore and washer hole) equals the 0.5 uL of docs/30 within 5 %",
         abs(P.EXIT_VOLUME_UL / 0.5 - 1) < 0.05, f"{P.EXIT_VOLUME_UL:.3f} uL"),
        ("total pressure drop of the cell at 200 uL/min is below a tenth of the rating (M-280)",
         hyd["M-280"][200.0]["total"] < 0.1 * P_RATED, f"{hyd['M-280'][200.0]['total'] / 1e5:.2f} bar"),
        ("main screws hold the rated pressure with a margin of at least 2", mech["main_margin"] >= 2.0,
         f"{mech['main_margin']:.1f}"),
        ("plate screws alone hold the body-plate joint at the rated pressure, margin at least 3",
         mech["m25_margin"] >= 3.0, f"{mech['m25_margin']:.1f}"),
        ("the lowest washer force holds the retainer against the body face at 80 uL/min with a margin of 2",
         checks_lift, f"{mech['stack_push_N'][80.0]:.2f} N vs {mech['washer_force_N'][0]:.2f} N"),
        ("O-ring squeeze on the strip stays within 15-35 % over the gap tolerance",
         all(0.15 <= s <= 0.35 for s in mech["squeeze_strip"]),
         ", ".join(f"{100 * s:.0f} %" for s in mech["squeeze_strip"])),
    ]
    ok = all(c[1] for c in checks)

    # ---- report -------------------------------------------------------------------------------------------
    med = lambda k: f"{fmt(k['lod_median'])} [{fmt(k['lod_p05'])}–{fmt(k['lod_p95'])}]"
    L = ["# Tier-2 flow cell with the bed inside the cell — numbers behind docs/34", "",
         f"Generated by `scripts/tier_round/tier2_cell.py` (Monte Carlo n = {n}, seed of the kit). Dimensions from "
         "`cad/elisa_cad/tier2_cell/params.py`. Model predictions, not measurements.", "",
         "## 0. Checks", "", "| Check | Result | Value |", "|---|---|---|"]
    L += [f"| {c[0]} | {'pass' if c[1] else '**FAIL**'} | {c[2]} |" for c in checks]
    L += ["", "## 1. Bed and retainer by bead and bore", "",
          "| Beads | Bore (mm) | Bed (nL) | Bed length (mm) | Bead layers | Empty bore above (mm) | Wall above the "
          "bed (mm²) | Retainer | Retainer area low / nominal / high (mm², UNVERIFIED) |", "|---|---|---|---|---|---|---|---|---|"]
    for g in geo:
        L.append(f"| {g['beads']} | {g['bore']} | {g['bed_nL']:.0f} | {g['L_bed']:.2f} | {g['layers']:.0f} | "
                 f"{g['L_free']:.2f} | {g['wall_above']:.1f} | "
                 f"{'membrane on screen' if g['membrane'] else 'screen'} | "
                 + " / ".join(f"{x:.1f}" for x in g["retainer"]) + " |")
    L += ["", "### Bead size and bore (nominal; retainer held at its nominal area for the 0.5 mm bore)", "",
          "| Beads (µm) | Same bed volume: nL; captured; LOD; bed Δp at the load flow (bar) | Same bead area: nL; "
          "captured; LOD; bed Δp (bar) |", "|---|---|---|"]
    for r in scan["beads"]:
        c = lambda k: (f"{r[k]['V_nL']:.0f}; {100 * r[k]['capture']:.0f} %; {fmt(r[k]['lod'])}; "
                       f"{r[k]['dp_bar']:.2g}")
        L.append(f"| {r['d_um']:g} | {c('same_volume')} | {c('same_area')} |")
    L += ["", "| Bore (mm), M-280, 19 nL | Captured | LOD | Bed Δp at the load flow (bar) |", "|---|---|---|---|"]
    L += [f"| {r['bore']} | {100 * r['capture']:.0f} % | {fmt(r['lod'])} | {r['dp_bar']:.2g} |" for r in scan["bore"]]
    L += ["", "## 2. Model cases (LOD in pg/mL)", "",
          "| Case | Nominal | Median [5–95 %] | P(≤ 1) / P(≤ 10) | Upper limit (slope) | Captured | Bed Δp at the "
          "load flow (bar) | Blank enzymes: beads / everything else |", "|---|---|---|---|---|---|---|---|"]
    for key, label, _d, _p in cases:
        k = res[key]
        L.append(f"| {label} | {fmt(k['lod_nominal'])} | {med(k)} | {k['p_lod_le_target']:.2f} / "
                 f"{k['p_lod_le_10']:.2f} | {fmt(k['uloq_nominal'])} | {100 * k['capture']:.0f} % | "
                 f"{k['dp_load_bar']:.2g} | {k['N_nsb_bed']:.2g} / {k['N_nsb_extra']:.2g} |")
    L += ["", "## 3. Pressure drop along the cell (bar)", "",
          "Bed: Kozeny–Carman as in the kit. Bores: Hagen–Poiseuille. Gap: radial creeping flow. Membrane: "
          "Hagen–Poiseuille in each pore. Screen: capillary bundle, porosity 0.3, 2 µm, tortuosity 2 (UNVERIFIED).", "",
          "| Bed | Flow (µL/min) | Bed | Membrane | Screen | Bores | Gap | Outlet path | Total | Share of 500 psi |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for name, rows in hyd.items():
        for q, r in rows.items():
            L.append(f"| {name} | {q:g} | " + " | ".join(f"{r[k] / 1e5:.2g}" for k in
                     ("bed", "membrane", "screen", "bores", "gap", "outlet", "total"))
                     + f" | {100 * r['total'] / P_RATED:.2g} % |")
    m = mech
    L += ["", "## 4. Mechanics with the whole liquid path at 500 psi (3.45 MPa)", "",
          "| Quantity | Value |", "|---|---|",
          f"| Force that lifts the plate off the strip (pressure to the outer groove wall, 9.3 mm) | {m['F_strip_N']:.0f} N |",
          f"| Force that parts body and plate (pressure to the outer groove wall, 14.3 mm) | {m['F_iface_N']:.0f} N |",
          f"| O-ring compression loads (1 N/mm, UNVERIFIED) | {m['F_oring_strip_N']:.0f} N + {m['F_oring_iface_N']:.0f} N |",
          f"| Four M4 screws at {m['m4_torque_Nm']} N·m: clamp force | {m['m4_preload_total_N']:.0f} N |",
          f"| Needed on the main screws; margin | {m['main_needed_N']:.0f} N; {m['main_margin']:.1f} |",
          f"| Load on each M2.5 if the plate screws carry the body–plate joint alone; thread strip-out in PEEK; margin | {m['m25_load_each_N']:.0f} N; {m['m25_strip_out_N']:.0f} N; {m['m25_margin']:.1f} |",
          f"| Bearing stress under the M4 washers; margin to compressive yield | {m['bearing_MPa']:.0f} MPa; {m['bearing_margin']:.0f} |",
          f"| Sag of body and plate across the strip pocket | {m['sag_um']:.2f} µm |",
          f"| Deflection of the port floor under the inlet fitting ({m['fitting_force_N']:.0f} N) | {m['floor_deflection_um']:.1f} µm |",
          "| Retainer washer squeeze, low / nominal / high tolerance | " + " / ".join(f"{100 * x:.0f} %" for x in m["washer_squeeze"]) + " |",
          "| Washer force (E " + f"{m['washer_E_MPa']:.0f}" + " MPa, UNVERIFIED), low / nominal / high | " + " / ".join(f"{x:.2f} N" for x in m["washer_force_N"]) + " |",
          "| Pressure on the membrane's sealing band, low / nominal / high | " + " / ".join(f"{x:.2f} MPa" for x in m["membrane_clamp_MPa"]) + " |",
          f"| Bow of the plate under the highest washer force | {m['plate_bow_um']:.2f} µm |",
          f"| Force of the bed on the retainer if the whole 500 psi fell across the bed | {m['bed_force_N']:.2f} N |",
          "| Force pushing the retainer stack away from the body face (pressure drop of bed, membrane and screen on the "
          "whole pocket; upper bound), at " + " / ".join(f"{q:g}" for q in m["stack_push_N"]) + " µL/min | "
          + " / ".join(f"{v:.2g} N" for v in m["stack_push_N"].values()) + " |",
          f"| O-ring squeeze on the strip at gap {P.GAP - P.GAP_TOL:.2f} / {P.GAP:.2f} / {P.GAP + P.GAP_TOL:.2f} mm | " + " / ".join(f"{100 * s:.0f} %" for s in m["squeeze_strip"]) + " |",
          f"| O-ring squeeze between body and plate | {100 * m['squeeze_iface']:.0f} % |", "",
          "## 5. Secondary flow paths", "", "| Quantity | Value |", "|---|---|",
          f"| Flow through the sector of the thin layer opposite the riser, relative to the nearest sector | {side['far_to_near_flow']:.2f} |",
          "| Share of the stream that by-passes the electrode through the film between body and plate, for a film of "
          + " / ".join(f"{k} µm" for k in side["bypass_fraction"]) + " | "
          + " / ".join(f"{100 * v:.2g} %" for v in side["bypass_fraction"].values()) + " |", ""]
    text = "\n".join(L)
    print("\n" + text)
    if not a.quick:
        (OUT / "tier2_cell.md").write_text(text + "\n")
        (OUT / "tier2_cell.json").write_text(json.dumps(
            dict(n=n, cases=res, hydraulics_Pa={k: {str(q): r for q, r in v.items()} for k, v in hyd.items()},
                 mechanics=mech, geometry=geo, side_paths=side, scans=scan, checks=[dict(check=c[0], ok=bool(c[1]), value=c[2]) for c in checks],
                 params={k: getattr(P, k) for k in dir(P) if k.isupper()}), indent=1, default=float))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
