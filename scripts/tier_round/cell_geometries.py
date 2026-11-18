#!/usr/bin/env python3
"""Flow-cell geometries put into the tier implementations of docs/30 (docs/33).

  python scripts/tier_round/cell_geometries.py [--n 2000]
writes results/tier_round/cell_geometries.md (tables) and cell_geometries.json (all numbers).
  python scripts/tier_round/cell_geometries.py --quick    nominal values on screen (no Monte Carlo, no files).
  python scripts/tier_round/cell_geometries.py --doc      prints the tables of docs/33 from that JSON.

Question: does another flow-cell geometry give a lower LOD than the MicruX wall-jet cells of docs/28 and docs/30?
The cell has two different jobs in the tier designs:

  role A (tier 1)      the working electrode is the capture surface; it reads its own enzyme under substrate flow;
  role B (tiers 2, 3)  the cell only detects the product plug swept out of a capture bed.

Each candidate replaces the cell and electrode dictionaries of the unchanged designs (run_tiers.t1, t2, t3v), and
the designs are evaluated with tierkit.py as in run_tiers.py (same parameters, same Monte Carlo, same seed).
tierkit.py, src/ and params/ are not edited.  Two things are added here:

* walls of a cross-flow channel upstream of the electrode (role A).  The kit's fast-flow read counts no floor,
  because in the wall-jet cell the stream arrives on the electrode first.  In a channel the floor and the lid
  between the inlet and the electrode saw conjugate and release product next to the wall; slit_wall_source()
  solves how much of it the electrode collects.  It enters the kit through the existing hook
  design["upstream"]["line_area"] as an equivalent area (factor ratio at the best estimates).
* two detector types the kit does not have (role B): a stated conversion ('fixed': porous flow-through electrode,
  ideal bound) and the free wall-jet equation of the model ('free_jet').  tierkit.cell_conversion is wrapped,
  not edited.

Geometry of cells other than the MicruX cells is a design input here (UNVERIFIED unless docs/02 section 5 or
docs/28 gives the number); it is never sampled.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
import warnings
from pathlib import Path

import numpy as np
from scipy.linalg import solve_banded

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))
import designs as D  # noqa: E402
import run_tiers as R  # noqa: E402
import tierkit as tk  # noqa: E402
from elisa_sim import transport as tr  # noqa: E402
from elisa_sim.architectures import CHEMISTRIES  # noqa: E402

OUT = ROOT / "results" / "tier_round"
UL, ULMIN = tk.UL, tk.ULMIN
LID = "tr.nsb.surface_factor_lid"
TUBING = "ma.nsb.surface_factor_tubing"
PRINTED = "tr.nsb.surface_factor_printed_electrode"


# ----------------------------------------------------------------------------------------------------------
# 1. product released from a channel wall upstream of the electrode
# ----------------------------------------------------------------------------------------------------------
def _eta_grid(n):
    faces = 0.5 * (1.0 - np.cos(np.pi * np.arange(n + 1) / n))          # clustered at both walls
    F = 3.0 * faces ** 2 - 2.0 * faces ** 3                             # integral of the profile 6 y (1 - y)
    return faces, 0.5 * (faces[:-1] + faces[1:]), np.diff(F)


def _march(c, xi_len, n_steps, floor, lid, grid):
    """Backward-Euler march of 6 y (1 - y) dc/dxi = d2c/dy2 over a section of length xi_len (xi = x D w / (Q h),
    y = height / h).  floor: 'sink' (c = 0), 'source' (unit flux in) or 'inert'; lid: 'source' or 'inert'.
    Returns (c, amount taken up by the sink over the section)."""
    faces, yc, uw = grid
    n = len(yc)
    G = 1.0 / np.diff(yc)                                               # conductances between cell centres
    g_wall = 1.0 / yc[0]
    edges = np.concatenate([[0.0], np.geomspace(xi_len * 1e-7, xi_len, n_steps)])
    taken = 0.0
    for dxi in np.diff(edges):
        ab = np.zeros((3, n))
        ab[1] = uw / dxi
        ab[1, :-1] += G
        ab[1, 1:] += G
        ab[0, 1:] = -G
        ab[2, :-1] = -G
        rhs = uw / dxi * c
        if floor == "sink":
            ab[1, 0] += g_wall
        elif floor == "source":
            rhs[0] += 1.0
        if lid == "source":
            rhs[-1] += 1.0
        c = solve_banded((1, 1), ab, rhs)
        if floor == "sink":
            taken += g_wall * c[0] * dxi
    return c, taken


def slit_wall_source(xi_up, xi_el, where="floor", n=300, n_steps=800):
    """Fraction of the product released uniformly from one wall of a slit over the length xi_up that a perfect
    sink on the floor over the following length xi_el collects.  where: 'floor' (the electrode's wall) or 'lid'.
    Plane Poiseuille flow, axial diffusion neglected, lengths as xi = x D w / (Q h) (the kit's slit variable)."""
    grid = _eta_grid(n)
    c = np.zeros(n)
    c, _ = _march(c, xi_up, n_steps, "source" if where == "floor" else "inert",
                  "source" if where == "lid" else "inert", grid)
    released = float(grid[2] @ c)                                       # flow-weighted content = xi_up
    c, taken = _march(c, xi_el, n_steps, "sink", "inert", grid)
    return taken / released, released / xi_up, (taken + float(grid[2] @ c)) / released


def slit_inlet_conversion(xi, n=300, n_steps=800):
    """Conversion of a uniform inlet stream at a floor sink of length xi (check against the model's table)."""
    grid = _eta_grid(n)
    c, taken = _march(np.ones(n), xi, n_steps, "sink", "inert", grid)
    return taken


def solver_checks():
    rows = []
    for xi in (0.01, 0.1, 1.0):
        a, b = slit_inlet_conversion(xi), float(tr.conversion("slit", xi, np.inf))
        rows.append((f"uniform inlet, floor sink of length xi = {xi:g}: conversion against elisa_sim.transport",
                     a, b, abs(a / b - 1.0) < 0.02))
    for where in ("floor", "lid"):
        N, rel, bal = slit_wall_source(0.05, 0.05, where)
        rows.append((f"{where} source, xi_up = xi_el = 0.05: released amount / xi_up", rel, 1.0, abs(rel - 1) < 1e-9))
        rows.append((f"{where} source, xi_up = xi_el = 0.05: (collected + leaving) / released", bal, 1.0,
                     abs(bal - 1) < 1e-9))
        N2, _, _ = slit_wall_source(0.05, 0.05, where, n=600, n_steps=1600)
        rows.append((f"{where} source: collected fraction, grid 300 x 800 against 600 x 1600", N, N2,
                     abs(N - N2) < 0.02 * N2))
        Nl, _, _ = slit_wall_source(0.05, 30.0, where)
        rows.append((f"{where} source followed by a very long sink (xi_el = 30): everything is collected", Nl, 1.0,
                     abs(Nl - 1) < 1e-3))
    # thin boundary layer, sink as long as the source.  For comparison only (not a pass criterion on its own):
    # the zero-gap collection efficiency of a double channel electrode with a generator at uniform concentration
    # is 1 + b^(2/3) - (1 + b)^(2/3), b = collector / generator length (recalled, UNVERIFIED): 0.413 for b = 1.
    N, _, _ = slit_wall_source(1e-4, 1e-4, "floor")
    rows.append(("floor source, thin boundary layer (xi = 1e-4), sink as long as the source: collected fraction; "
                 "second number: double-channel-electrode efficiency for a generator at uniform concentration "
                 "(recalled formula; a uniform-flux source releases more of its product near the sink, so the "
                 "solver must be above it)", N, 0.413, 0.413 < N < 0.75))
    return rows


# ----------------------------------------------------------------------------------------------------------
# 2. detectors the kit does not have
# ----------------------------------------------------------------------------------------------------------
_kit_conversion = tk.cell_conversion
_NU = {"value": 1.0e-6}


def cell_conversion(cell, D_, area, Q):
    g = cell.get("flow_geometry", "radial")
    if g == "fixed":                       # stated conversion: porous flow-through electrode, ideal bound
        return float(cell["eta"])
    if g == "free_jet":                    # free wall jet on a disc, Yamada-Matsuda form of the model (docs/03)
        return float(np.minimum(1.0, tr.wall_jet_conversion(D_, _NU["value"], cell["nozzle"],
                                                            np.sqrt(area / np.pi), Q, cell["coeff"])))
    return _kit_conversion(cell, D_, area, Q)


tk.cell_conversion = cell_conversion


# ----------------------------------------------------------------------------------------------------------
# 3. role A: capture on the electrode (tier 1)
# ----------------------------------------------------------------------------------------------------------
def nominal(ps, key, unit=None):
    prm = ps.params[key]
    return float(prm.value) if unit is None else float(tk.convert(prm.value, prm.unit, unit))


def role_a(ps, kind, h, Q_read=200.0, electrode="AU10", L_up=0.0, w=None):
    """Tier 1 of docs/30 with another cell.  kind 'radial': the MicruX cell of that electrode with gap h.
    kind 'channel': cross-flow channel of height h and width w (default: the side of the equal-area square of the
    electrode, i.e. the electrode spans the channel) with the electrode L_up downstream of the inlet; the inlet
    bore is that of the MicruX cell, so that only the geometry of the chamber differs."""
    d = R.t1(electrode, h=h, Q_read=Q_read)
    info = dict(kind=kind, h=h, L_up=L_up, Q_read=Q_read, electrode=electrode)
    if kind == "radial":
        return d, info
    el, cell0 = d["electrode"], d["cell"]
    side = float(np.sqrt(el["area"]))
    w = side if w is None else w
    d["cell"] = dict(flow_geometry="channel", h=h, w_channel=w, R=cell0["R"], lid_factor_key=LID)
    D_prod = tk.Ctx(ps).nominal(CHEMISTRIES["alp_hqdp"]["D_product"], "m^2/s")
    Q = Q_read * ULMIN
    eta = float(tk.cell_conversion(d["cell"], D_prod, el["area"], Q))
    f_tub, f_lid, f_floor = nominal(ps, TUBING), nominal(ps, LID), nominal(ps, el["floor_factor_key"])
    bore = 2.0 * np.pi * cell0["bore_radius"] * cell0["bore_length"]
    eq = bore * f_lid / f_tub                                # inlet bore: mixed into the stream, as in the kit
    N_f = N_l = 0.0
    if L_up > 0:
        xi_up, xi_el = D_prod * L_up * w / (Q * h), D_prod * side * w / (Q * h)
        N_f, N_l = slit_wall_source(xi_up, xi_el, "floor")[0], slit_wall_source(xi_up, xi_el, "lid")[0]
        strip = L_up * min(w, side)                          # walls in the lane that passes over the electrode
        eq += strip * (f_floor * N_f + f_lid * N_l) / (f_tub * eta)
    d["upstream"] = dict(d["upstream"], line_area=d["upstream"]["line_area"] + eq)
    d["name"] = f"T1 channel h={h * 1e6:.0f} um, w={w * 1e3:.2f} mm, L_up={L_up * 1e3:.0f} mm"
    info.update(w=w, eta_stream=eta, collected_upstream_floor=N_f, collected_upstream_lid=N_l,
                equivalent_line_area_mm2=eq * 1e6)
    return d, info


def pressure_drop(ps, kind, h, Q_uL_min, cell=None, w=None, length=None):
    mu = nominal(ps, "ma.fluid.viscosity", "Pa*s")
    Q = Q_uL_min * ULMIN
    if kind == "radial":
        return 6.0 * mu * Q / (np.pi * h ** 3) * np.log(cell["R"] / cell["bore_radius"])
    return 12.0 * mu * length * Q / (w * h ** 3)


# ----------------------------------------------------------------------------------------------------------
# 4. role B: detector behind the bed (tiers 2 and 3)
# ----------------------------------------------------------------------------------------------------------
def disc(d_mm):
    return float(np.pi * (0.5e-3 * d_mm) ** 2)


BORE_SPE = 2.0 * np.pi * D.SPE_CELL["bore_radius"] * D.SPE_CELL["bore_length"]       # 12.6 mm2
V_BORE_SPE = np.pi * D.SPE_CELL["bore_radius"] ** 2 * D.SPE_CELL["bore_length"] / UL  # 2.5 uL
CARBON = dict(kind="thinfilm", we_factor_key=PRINTED, floor_factor_key=PRINTED)


def detectors(ps):
    """Detector candidates of role B.  'tip': the capillary bed of tier 2 can sit in a straight inlet bore 1 mm
    above the electrode (docs/30 section 4); otherwise the bed sits in a fitting on the inlet port and the whole
    inlet passage lies between bed and electrode (taken as the bore of the strip cell: 0.8 mm x 5 mm, UNVERIFIED
    for every other cell).  V_in: liquid inside the detector that the plug has to pass before it is read."""
    coeff = nominal(ps, "ma.detection.walljet_coefficient")
    nozzle = nominal(ps, "ma.geometry.walljet_nozzle_diameter", "m")
    A_por = nominal(ps, "ma.geometry.coulometric_effective_area", "m^2")
    eta_por = nominal(ps, "hw.flow_cells.thermo_6011rs_coulometric.collection_efficiency")
    V_por = nominal(ps, "hw.flow_cells.thermo_6011rs_coulometric.volume", "m^3") / UL
    Q_por = nominal(ps, "hw.flow_cells.thermo_6011rs_coulometric.min_flow", "m^3/s") / ULMIN
    V_sen = nominal(ps, "hw.flow_cells.antec_sencell.working_volume", "m^3")
    h_sen = V_sen / disc(2.0)                                            # working volume taken as the disc over the WE
    w_tl = nominal(ps, "ma.geometry.thin_layer_channel_width", "m")
    spe = lambda h: dict(D.SPE_CELL, h=h)
    tf = lambda h: dict(D.TF_CELL, h=h)
    out = []

    def add(key, label, cell, el, tip, Q_min=None, V_in=0.0, family=""):
        out.append(dict(key=key, label=label, cell=cell, electrode=el, tip=tip, Q_min=Q_min, V_in=V_in,
                        family=family))

    for h in (0.5e-3, 0.2e-3, 0.1e-3, 0.05e-3, 0.025e-3):
        add(f"spe_{h * 1e6:.0f}", f"radial thin gap, MicruX strip cell, 3 mm printed carbon, gap {h * 1e3:.3g} mm"
            + (" (docs/30)" if h == 0.2e-3 else ""), spe(h), dict(D.C21), True, family="radial")
    for h in (0.16e-3, 0.05e-3, 0.025e-3):
        add(f"tf_{h * 1e6:.0f}", f"radial thin gap, MicruX thin-film cell, 1 mm electrode, gap {h * 1e3:.3g} mm",
            tf(h), dict(CARBON, area=disc(1.0)), True, family="radial")
    add("sencell", f"radial thin gap, adjustable (Antec SenCell type): 2 mm glassy carbon, working volume "
        f"{V_sen / UL * 1e3:.0f} nL = gap {h_sen * 1e6:.0f} um",
        dict(flow_geometry="radial", h=h_sen, R=1.0e-3, bore_radius=0.5 * nozzle, bore_length=5.0e-3,
             lid_factor_key=LID), dict(CARBON, area=disc(2.0)), False, family="radial")
    for hg in (127e-6, 51e-6, 13e-6):
        add(f"tl_{hg * 1e6:.0f}", f"cross-flow thin-layer channel (BASi type): 3 mm glassy carbon, gasket "
            f"{hg * 1e6:.0f} um, channel {w_tl * 1e3:.0f} mm wide",
            dict(flow_geometry="channel", h=hg, w_channel=w_tl, R=4.0e-3, lid_factor_key=LID),
            dict(CARBON, area=disc(3.0)), False, family="channel")
    add("free_jet", f"free wall jet, large gap (DropSens FLWCL type): 4 mm printed carbon, nozzle "
        f"{nozzle * 1e3:.1f} mm; wall-jet equation, outside its validity at these flows",
        dict(flow_geometry="free_jet", nozzle=nozzle, coeff=coeff, h=1.0e-3, R=4.0e-3, bore_radius=0.5 * nozzle,
             bore_length=5.0e-3, lid_factor_key=LID), dict(D.C21, area=disc(4.0)), False, family="free jet")
    add("porous", f"porous flow-through graphite (Dionex 6011RS type): conversion {eta_por:.2f}, wetted area "
        f"{A_por * 1e6:.0f} mm2, {V_por:.1f} uL, flow >= {Q_por:.0f} uL/min",
        dict(flow_geometry="fixed", eta=eta_por, h=1.0e-4, R=4.0e-3, lid_factor_key=LID),
        dict(CARBON, area=A_por), False, Q_min=Q_por, V_in=V_por, family="porous")
    add("ideal_3", "bound: every product molecule oxidised, 3 mm electrode",
        dict(flow_geometry="fixed", eta=1.0, h=1.0e-4, R=4.0e-3, lid_factor_key=LID), dict(D.C21), True,
        family="bound")
    add("ideal_1", "bound: every product molecule oxidised, 1 mm electrode",
        dict(flow_geometry="fixed", eta=1.0, h=1.0e-4, R=1.0e-3, lid_factor_key=LID),
        dict(CARBON, area=disc(1.0)), True, family="bound")
    return out


V_SWEEP = 7.5          # uL swept in the read window of docs/30 (5 uL/min x 90 s)
T_MIN = 6.0            # s, shortest read window used here (design choice: a few time constants of a 1 Hz filter)


def role_b(tier, det, Q_read=5.0):
    """Tier 2 or tier 3 (one valve) of docs/30 with another detector.  The read window sweeps the same volume
    as in docs/30 (7.5 uL) plus twice the detector's internal volume, but lasts at least T_MIN."""
    t_read = max(T_MIN, (V_SWEEP + 2.0 * det["V_in"]) / Q_read * 60.0)
    make = R.t2 if tier == 2 else R.t3v
    d = make(Q_read=Q_read, t_read=t_read)
    d["cell"], d["electrode"] = copy.deepcopy(det["cell"]), copy.deepcopy(det["electrode"])
    rb = det["cell"].get("bore_radius", D.SPE_CELL["bore_radius"])
    if tier == 2:
        if det["tip"]:      # capillary tip 1 mm above the chamber, in the cell's own bore
            d["bed"]["bore_area"] = 2.0 * np.pi * rb * 1.0e-3
            scale = (rb / D.SPE_CELL["bore_radius"]) ** 2
            d["bed"]["V_dead"] = 0.5 * UL * scale              # docs/30: 0.5 uL below the tip in the 0.8 mm bore
            d["read"]["V_transit_uL"] = 0.6 * scale + det["V_in"]
        else:               # bed in a fitting on the inlet port: the whole passage lies in between
            d["bed"]["bore_area"] = BORE_SPE
            d["bed"]["V_dead"] = V_BORE_SPE * UL
            d["read"]["V_transit_uL"] = V_BORE_SPE + det["V_in"]
    else:
        d["read"]["steady_bore_area"] = BORE_SPE
        d["read"]["V_transit_uL"] = 4.0 + det["V_in"]
    d["name"] = f"T{tier} {det['key']} Q={Q_read:g}"
    return d, t_read


# ----------------------------------------------------------------------------------------------------------
# evaluation helpers
# ----------------------------------------------------------------------------------------------------------
def evaluate(design, ps):
    f = tk.evaluate_planar if design["tier"] == 1 else tk.evaluate_bed
    if design.get("ps_values"):
        ps = ps.with_values(design["ps_values"])
    return f(design, ps)


def lod(design, ps):
    return float(evaluate(design, ps).lod_pgml)


def fractions(res):
    tot = sum(np.asarray(v, float) for v in res.variance_terms.values())
    return {k: float(np.asarray(v, float) / tot) for k, v in res.variance_terms.items()}


def fmt(x, nd=2):
    if x is None:
        return "-"
    if not np.isfinite(x) or x > 1e29:
        return "inf"
    return f"{x:.{nd}g}"


def mc_cell(k):
    return f"{fmt(k['lod_median'])} [{fmt(k['lod_p05'])}-{fmt(k['lod_p95'])}]", f"{k['p_lod_le_target']:.2f}"


def doc_tables():
    """The condensed tables of docs/33, printed from cell_geometries.json (nothing is recomputed)."""
    o = json.loads((OUT / "cell_geometries.json").read_text())
    fmt = lambda x: f"{float(f'{x:.2g}'):.0f}" if x >= 100 else f"{x:.2g}" if x < 10 else f"{x:.0f}"

    def emit(text):                                    # typographic units for the document
        for a, b in ((" um", " µm"), (" uL", " µL"), ("mm2", "mm²"), (">=", "≥")):
            text = text.replace(a, b)
        print(text)
    med = lambda k: f"{fmt(k['lod_median'])} [{fmt(k['lod_p05'])}–{fmt(k['lod_p95'])}]"
    pp = lambda k: f"{k['p_lod_le_target']:.2f} / {k['p_lod_le_10']:.2f}"
    emit("| Cell | gap (µm) | IgG of the vial captured (%) | product of the stream oxidised at 200 µL/min (%) | "
          "LOD nominal, read at 200 µL/min | median [5–95 %] | P(≤ 1) / P(≤ 10) | nominal, read at 500 µL/min | "
          "substrate background persists | 1 % of turnovers electroactive |\n|---|---|---|---|---|---|---|---|---|---|")
    for r in o["role_A"]:
        nm = r["name"]
        emit(f"| {nm} | {r['h_um']:.0f} | {100 * r['captured']:.1f} | {100 * r['collected_stream']:.1f} | "
              f"**{fmt(r['lod']['200.0'])}** | {med(r['mc_200'])} | {pp(r['mc_200'])} | {fmt(r['lod']['500.0'])} | "
              f"{fmt(r['lod_nodecay']['200.0'])} | {fmt(r['lod_p01']['200.0'])} |")
    for tier in ("tier3", "tier2"):
        emit(f"\n{tier}\n| Detector | " + ("bed | " if tier == "tier2" else "") + "electrode (mm²) | product "
              "oxidised at 5 / 50 µL/min (%) | LOD nominal | median [5–95 %] | P(≤ 1) / P(≤ 10) | substrate "
              "background persists | 1 % electroactive: as specified | 1 %: best sweep (µL/min) | 1 %, best sweep: "
              "median [5–95 %] |\n|---|" + ("---|" if tier == "tier2" else "") + "---|---|---|---|---|---|---|---|---|")
        for r in o["role_B"][tier]:
            b = r["best_p01"]
            emit(f"| {r['label']} | " + (("tip" if r["tip"] else "port") + " | " if tier == "tier2" else "")
                  + f"{r['area_mm2']:.3g} | {100 * r['eta_5']:.0f} / {100 * r['eta_50']:.0f} | **{fmt(r['lod'])}** | "
                  f"{med(r['mc'])} | {pp(r['mc'])} | {fmt(r['lod_nodecay'])} | {fmt(r['lod_p01'])} | "
                  f"{fmt(b[0])} ({b[1]:g}) | {med(r['mc_p01_best'])} |")
    emit("\nshapes\n| Shape | area (mm²) | captured of what enters (%) | k_eff (µm/s) | k_eff / k_r | product of the "
          "stream oxidised at 200 µL/min (%) |\n|---|---|---|---|---|---|")
    for r in o["shapes"]:
        emit(f"| {r['name']} | {r['area_mm2']:.3g} | {100 * r['captured']:.1f} | {r['k_eff'] * 1e6:.2f} | "
              f"{r['k_eff_over_k_r']:.2f} | {100 * r['stream_collected_200']:.1f} |")
    g = o.get("per_draw_gap_50_vs_200")
    if g:
        emit(f"\nper draw, LOD(50 um) / LOD(0.2 mm): median {g['median']:.2f} [{g['p05']:.2f}-{g['p95']:.2f}]; "
             f"worse in {g['share_worse']:.2f}; gain below 10 % in {g['share_gain_below_10pct']:.2f}; "
             + "; ".join(f"{c['key']} {c['r']:+.2f}" for c in g["correlations"]))
    emit(f"\nk_r = {o['k_r'] * 1e6:.2f} um/s; checks passed:{sum(c['passed'] for c in o['checks'])} of {len(o['checks'])}")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--quick", action="store_true", help="nominal values on screen, no Monte Carlo, no files")
    ap.add_argument("--doc", action="store_true", help="print the tables of docs/33 from cell_geometries.json")
    args = ap.parse_args(argv)
    if args.doc:
        doc_tables()
        return 0
    warnings.simplefilter("ignore")
    ps0 = R.base_params()
    _NU["value"] = nominal(ps0, "ma.fluid.viscosity", "Pa*s") / nominal(ps0, "ma.fluid.density", "kg/m^3")
    n = args.n
    out, md = {}, []
    P01, NODECAY = R.P01(ps0), R.NODECAY(ps0)

    raw = {}

    def mc(design, ps, tag=None):
        if args.quick:
            return None
        keep, s = R.run(design, ps, n)
        if tag is not None:
            raw[tag] = s
        return keep

    # ---- 0. checks -------------------------------------------------------------------------------------
    md.append("\n## 0. Checks\n")
    md.append("| Check | value | reference | pass |\n|---|---|---|---|")
    ok = True
    chk = solver_checks()
    # the unchanged designs must reproduce results/tier_round/tiers.json
    ref = json.loads((OUT / "tiers.json").read_text())["1. The three implementations, as specified"]
    labels = list(ref)
    for lab, design in ((labels[0], R.t1()), (labels[1], R.t2()), (labels[2], R.t3v())):
        a, b = lod(design, ps0), ref[lab]["lod_nominal"]
        chk.append((f"unchanged design reproduces tiers.json: {lab}", a, b, abs(a / b - 1.0) < 1e-6))
    d_a, _ = role_a(ps0, "radial", 0.2e-3)
    chk.append(("role_a('radial', 0.2 mm) is tier 1 of docs/30", lod(d_a, ps0), ref[labels[0]]["lod_nominal"],
                abs(lod(d_a, ps0) / ref[labels[0]]["lod_nominal"] - 1.0) < 1e-6))
    dets = detectors(ps0)
    base_det = next(x for x in dets if x["key"] == "spe_200")
    for tier, lab in ((2, labels[1]), (3, labels[2])):
        d_b, _ = role_b(tier, base_det)
        chk.append((f"role_b(tier {tier}, strip cell 0.2 mm, 5 uL/min) is the design of docs/30", lod(d_b, ps0),
                    ref[lab]["lod_nominal"], abs(lod(d_b, ps0) / ref[lab]["lod_nominal"] - 1.0) < 1e-6))
    for name, a, b, good in chk:
        ok = ok and bool(good)
        md.append(f"| {name} | {a:.6g} | {b:.6g} | {'yes' if good else 'NO'} |")
    out["checks"] = [dict(name=nm, value=float(a), reference=float(b), passed=bool(g)) for nm, a, b, g in chk]

    # ---- 1. role A -------------------------------------------------------------------------------------
    D_igg = nominal(ps0, "chem.analyte.diffusion_coefficient", "m^2/s")
    flows = (200.0, 300.0, 500.0)
    cases = [("radial", h, "AU10", 0.0, None) for h in (0.5e-3, 0.2e-3, 0.1e-3, 0.05e-3, 0.025e-3)]
    cases += [("radial", h, "SE1", 0.0, None) for h in (0.16e-3, 0.05e-3, 0.025e-3)]
    cases += [("channel", h, "AU10", 0.0, None) for h in (0.1e-3, 0.05e-3, 0.025e-3)]
    cases += [("channel", h, "AU10", 2.0e-3, None) for h in (0.1e-3, 0.05e-3, 0.025e-3)]
    cases += [("channel", 0.05e-3, "AU10", 2.0e-3, 5.0e-3)]
    md.append("\n## 1. Role A - the electrode is the capture surface (tier 1 of docs/30 with another cell)\n")
    md.append("Printed gold strip (3 mm) or thin-film gold chip (1 mm), everything else as tier 1 of docs/30: load "
              "2.86 uL/min for 44 min, 20 nM conjugate, read 60 s under substrate flow. 'Captured' = fraction of the "
              "IgG in the vial that ends on the electrode. 'Stream collected' = fraction of the product arriving "
              "with the stream (walls upstream, free hydroquinone) that the electrode oxidises at 200 uL/min. "
              "'Upstream floor / lid collected' = fraction of the product of the channel walls between inlet and "
              "electrode that the electrode oxidises (section 0 solver). Pressure drop over the chamber at the "
              "read flow (Derived; laminar).\n")
    md.append("| Cell | gap (um) | captured | k_m (um/s) | stream collected at 200 | upstream floor / lid collected | "
              "LOD nominal, read at 200 / 300 / 500 uL/min (pg/mL) | median [5-95 %] at 200 | P(LOD <= 1) at 200 | "
              "median [5-95 %] at 500 | 1 % electroactive, nominal at 200 / 500 | no decay, nominal at 200 / 500 | "
              "pressure drop at 200 / 500 uL/min (kPa) |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    out["role_A"] = []
    for kind, h, eln, L_up, w in cases:
        row = dict(kind=kind, h_um=h * 1e6, electrode=eln, L_up_mm=L_up * 1e3)
        lods, p01s, nodec, infos = {}, {}, {}, {}
        for Qr in flows:
            d, info = role_a(ps0, kind, h, Qr, eln, L_up, w)
            res = evaluate(d, ps0)
            lods[Qr], infos[Qr] = float(res.lod_pgml), info
            p01s[Qr] = lod(d, P01)
            nodec[Qr] = lod(d, NODECAY)
            if Qr == 200.0:
                dg = res.diagnostics
                row.update(captured=float(dg["capture_fraction"]), k_m=float(dg["k_m"]),
                           collected_stream=float(dg["collected_upstream"]), fractions=fractions(res),
                           time_min=res.time_to_result_min)
                row["mc_200"] = mc(d, ps0, tag=(kind, eln, h, L_up, w))
            if Qr == 500.0:
                row["mc_500"] = mc(d, ps0)
        cell_now = D.ELECTRODES[eln][0]
        if kind == "radial":
            dp = [pressure_drop(ps0, "radial", h, q, cell=cell_now) / 1e3 for q in (200.0, 500.0)]
            name = (f"radial thin gap (wall-jet inlet), MicruX {'strip' if eln == 'AU10' else 'thin-film'} cell, "
                    f"{'3' if eln == 'AU10' else '1'} mm gold")
            if (eln, h) in (("AU10", 0.2e-3), ("SE1", 0.16e-3)):
                name += " (docs/30)"
        else:
            side = float(np.sqrt(D.ELECTRODES[eln][1]["area"]))
            ww = side if w is None else w
            dp = [pressure_drop(ps0, "channel", h, q, w=ww, length=L_up + side + 2.0e-3) / 1e3
                  for q in (200.0, 500.0)]
            name = (f"cross-flow channel {ww * 1e3:.1f} mm wide, 3 mm gold, electrode "
                    + ("at the channel entrance" if L_up == 0 else f"{L_up * 1e3:.0f} mm downstream of the inlet"))
        i2 = infos[200.0]
        row.update(name=name, lod=lods, lod_p01=p01s, lod_nodecay=nodec, dp_kPa=dp, info={str(k): v for k, v in infos.items()})
        up = "-" if kind == "radial" or L_up == 0 else \
            f"{i2['collected_upstream_floor']:.2f} / {i2['collected_upstream_lid']:.3f}"
        m2 = mc_cell(row["mc_200"]) if row.get("mc_200") else ("-", "-")
        m5 = mc_cell(row["mc_500"]) if row.get("mc_500") else ("-", "-")
        md.append(f"| {name} | {h * 1e6:.0f} | {row['captured']:.3f} | {row['k_m'] * 1e6:.2f} | "
                  f"{row['collected_stream']:.3f} | {up} | {fmt(lods[200.0])} / {fmt(lods[300.0])} / "
                  f"{fmt(lods[500.0])} | {m2[0]} | {m2[1]} | {m5[0]} | {fmt(p01s[200.0])} / {fmt(p01s[500.0])} | "
                  f"{fmt(nodec[200.0])} / {fmt(nodec[500.0])} | {fmt(dp[0])} / {fmt(dp[1])} |")
        print(md[-1], flush=True)
        out["role_A"].append(row)

    # the same Monte Carlo draws with the gap of docs/30 and with the 50 um gap
    ka, kb = ("radial", "AU10", 0.2e-3, 0.0, None), ("radial", "AU10", 0.05e-3, 0.0, None)
    if ka in raw and kb in raw:
        a, b = raw[ka], raw[kb]
        assert a["_keys"] == b["_keys"]
        ratio = np.asarray(b["_mc"].lod_pgml, float) / np.asarray(a["_mc"].lod_pgml, float)
        cors = []
        for key, v in a["_samples"].items():
            v = np.asarray(v, float)
            if np.all(v > 0) and np.std(np.log(v)) > 0:
                cors.append((float(np.corrcoef(np.log(v), np.log(ratio))[0, 1]), key))
        cors.sort(key=lambda x: -abs(x[0]))
        q = np.percentile(ratio, [5, 50, 95])
        out["per_draw_gap_50_vs_200"] = dict(median=float(q[1]), p05=float(q[0]), p95=float(q[2]),
                                             share_worse=float(np.mean(ratio > 1.0)),
                                             share_gain_below_10pct=float(np.mean(ratio > 0.9)),
                                             correlations=[dict(key=k, r=c) for c, k in cors[:6]])
        md.append("\n### 1a. The same Monte Carlo draws with a 0.2 mm and with a 50 um gap (strip cell, read at "
                  "200 uL/min)\n")
        md.append(f"LOD at 50 um divided by LOD at 0.2 mm, draw by draw: median {q[1]:.2f} [{q[0]:.2f}-{q[2]:.2f}]; "
                  f"above 1 (the thin gap is worse) in {np.mean(ratio > 1.0):.2f} of the draws, above 0.9 in "
                  f"{np.mean(ratio > 0.9):.2f}. Correlation of log ratio with log parameter, six largest: "
                  + "; ".join(f"`{k}` {c:+.2f}" for c, k in cors[:6]) + ".")

    # geometries the planar format of the kit cannot evaluate: transport figures only
    md.append("\n### 1b. Capture transport of other shapes at the load flow (no LOD)\n")
    md.append("Mean flux to the capture surface per unit inlet concentration, k_eff = captured fraction x Q / area "
              "(reaction and transport in series), at 2.86 uL/min, with the reaction velocity k_r of tier 1. The "
              "specific label per area of electrode, and with it the ratio to the electrode's own non-specific "
              "label, scales with k_eff; its ceiling is k_r.\n")
    md.append("| Shape | area (mm2) | captured fraction of what enters | k_eff (um/s) | k_eff / k_r | product of the "
              "stream collected at 200 uL/min |\n|---|---|---|---|---|---|")
    res0 = evaluate(R.t1(), ps0)
    k_r = float(res0.diagnostics["k_r"])
    Ql = 2.86 * ULMIN
    D_prod = tk.Ctx(ps0).nominal(CHEMISTRIES["alp_hqdp"]["D_product"], "m^2/s")
    Qr = 200.0 * ULMIN
    shapes = []
    A3 = disc(3.0)
    for h in (0.2e-3, 0.025e-3):
        s = A3 - np.pi * D.SPE_CELL["bore_radius"] ** 2
        f = float(tr.conversion("slit", D_igg * s / (Ql * h), k_r * h / D_igg))
        e = float(tr.conversion("slit", D_prod * s / (Qr * h), np.inf))
        shapes.append((f"radial thin gap {h * 1e6:.0f} um over a 3 mm disc", A3, f, e))
    for dia, lab in ((250e-6, "0.25 mm"), (100e-6, "0.10 mm")):
        for area in (A3, disc(1.0)):
            Lt = area / (np.pi * dia)
            f = float(tr.conversion("tube", np.pi * Lt * D_igg / Ql, k_r * 0.5 * dia / D_igg))
            e = float(tr.conversion("tube", np.pi * Lt * D_prod / Qr, np.inf))
            shapes.append((f"tubular electrode, bore {lab}, length {Lt * 1e3:.1f} mm (no part identified)", area, f, e))
    bed = evaluate(R.t2(), ps0).diagnostics
    A_bed = float(bed["bed_area_m2"])
    k_bed = 1.0 / (1.0 / float(bed["k_m"]) + 1.0 / k_r)
    f_bed = 1.0 - np.exp(-k_bed * A_bed / (3.4 * ULMIN))
    shapes.append(("porous or packed electrode with the surface of the tier-2 bed, at 3.4 uL/min (no part identified)",
                   A_bed, float(f_bed), 1.0))
    out["shapes"] = []
    for name, area, f, e in shapes:
        Qx = 3.4 * ULMIN if name.startswith("porous") else Ql
        k_eff = f * Qx / area
        md.append(f"| {name} | {area * 1e6:.2f} | {f:.3f} | {k_eff * 1e6:.2f} | {k_eff / k_r:.2f} | {e:.3f} |")
        out["shapes"].append(dict(name=name, area_mm2=area * 1e6, captured=f, k_eff=k_eff, k_eff_over_k_r=k_eff / k_r,
                                  stream_collected_200=e))
    out["k_r"] = k_r

    # ---- 2. role B -------------------------------------------------------------------------------------
    D_prod = tk.Ctx(ps0).nominal(CHEMISTRIES["alp_hqdp"]["D_product"], "m^2/s")
    sweep = (2.0, 5.0, 10.0, 20.0, 50.0, 100.0)
    out["role_B"] = {}
    for tier, title in ((3, "tier 3, the bed in the loop of one valve"), (2, "tier 2, capillary bed, stop and sweep")):
        md.append(f"\n## {2 if tier == 3 else 3}. Role B - the cell detects the product of a bed: {title}\n")
        note = ("The bed, its loop and the valve are those of docs/30; only the detector differs. "
                if tier == 3 else
                "'Bed position': 'tip' = the capillary tip sits in the cell's straight inlet bore 1 mm above the "
                "chamber (docs/30); 'port' = the bed sits in a fitting on the inlet port and the inlet passage "
                "(taken as 0.8 mm x 5 mm for every such cell, UNVERIFIED) lies between bed and electrode. ")
        md.append(note + "'As specified' = sweep at 5 uL/min for 90 s (porous cell: at its minimum flow). 'Best "
                  "sweep' = lowest nominal LOD over 2-100 uL/min with the same swept volume (window at least "
                  f"{T_MIN:.0f} s, result within 60 min). Scenario '1 %' = only 1 % of the enzyme turnovers give "
                  "an electroactive product (docs/31 C1); 'no decay' = the substrate's free hydroquinone persists "
                  "(docs/31 C5, M2).\n")
        md.append("| Detector | " + ("bed position | " if tier == 2 else "") + "electrode (mm2) | product oxidised "
                  "at 5 / 50 uL/min | as specified: LOD nominal | median [5-95 %] | P(LOD <= 1) | no decay, "
                  "nominal | 1 %: nominal as specified | 1 %: best sweep (uL/min, s) | 1 %: median [5-95 %] at the "
                  "best sweep | 1 % and no decay: best sweep |\n|---|" + ("---|" if tier == 2 else "")
                  + "---|---|---|---|---|---|---|---|---|---|")
        rows = []
        for det in dets:
            qs = [q for q in sweep if det["Q_min"] is None] or [det["Q_min"], 500.0, 1000.0]
            q0 = 5.0 if det["Q_min"] is None else det["Q_min"]
            d0, t0 = role_b(tier, det, q0)
            r0 = evaluate(d0, ps0)
            e5 = float(tk.cell_conversion(det["cell"], D_prod, det["electrode"]["area"], 5.0 * ULMIN))
            e50 = float(tk.cell_conversion(det["cell"], D_prod, det["electrode"]["area"], 50.0 * ULMIN))
            best = {}
            for scen, psx in (("p01", P01), ("p01_nodecay", R.NODECAY(P01))):
                cand = []
                for q in qs:
                    dq, tq = role_b(tier, det, q)
                    if tk.timing(dq)[0] > 60.0:
                        continue
                    cand.append((lod(dq, psx), q, tq))
                best[scen] = min(cand)
            db, _tb = role_b(tier, det, best["p01"][1])
            row = dict(key=det["key"], label=det["label"], family=det["family"], tip=det["tip"],
                       area_mm2=det["electrode"]["area"] * 1e6, eta_5=e5, eta_50=e50, Q_spec=q0, t_spec=t0,
                       lod=float(r0.lod_pgml), fractions=fractions(r0), lod_nodecay=lod(d0, NODECAY),
                       lod_p01=lod(d0, P01), best_p01=best["p01"], best_p01_nodecay=best["p01_nodecay"],
                       time_min=r0.time_to_result_min, mc=mc(d0, ps0), mc_p01_best=mc(db, P01))
            rows.append(row)
            m0 = mc_cell(row["mc"]) if row["mc"] else ("-", "-")
            m1 = mc_cell(row["mc_p01_best"]) if row["mc_p01_best"] else ("-", "-")
            b, bn = best["p01"], best["p01_nodecay"]
            md.append(f"| {det['label']} | " + (("tip" if det["tip"] else "port") + " | " if tier == 2 else "")
                      + f"{row['area_mm2']:.2f} | {e5:.2f} / {e50:.2f} | {fmt(row['lod'])} | {m0[0]} | {m0[1]} | "
                      f"{fmt(row['lod_nodecay'])} | {fmt(row['lod_p01'])} | {fmt(b[0])} ({b[1]:g}, {b[2]:.0f}) | "
                      f"{m1[0]} | {fmt(bn[0])} ({bn[1]:g}, {bn[2]:.0f}) |")
            print(md[-1], flush=True)
        out["role_B"][f"tier{tier}"] = rows

    md.append("\nAll checks pass.\n" if ok else "\n**A CHECK FAILED.**\n")
    if args.quick:                                     # nominal values on screen only: the result files keep
        print("quick run: result files not written - checks", "pass" if ok else "FAIL")   # their Monte Carlo
        return 0 if ok else 1
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "cell_geometries.md").write_text(
        "# Flow-cell geometries on the tier implementations (scripts/tier_round/cell_geometries.py)\n\n"
        f"Monte Carlo n = {n}, seed 20261111, parameters and scenarios of run_tiers.py. Model predictions, not "
        "measurements. Geometry of cells other than the MicruX cells is a design input (UNVERIFIED unless docs/02 "
        "section 5 or docs/28 gives it) and is not sampled.\n" + "\n".join(md) + "\n")
    (OUT / "cell_geometries.json").write_text(json.dumps(out, indent=1, default=float))
    print("written", OUT / "cell_geometries.md", "- checks", "pass" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
