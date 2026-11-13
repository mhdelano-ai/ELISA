"""PNG views of card A: iso top/bottom, exploded, L1 plan, sections, zooms (matplotlib, Agg)."""
from __future__ import annotations

import cadquery as cq
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.collections import PolyCollection  # noqa: E402
from matplotlib.patches import Polygon as MPoly  # noqa: E402
from shapely.geometry import MultiPolygon  # noqa: E402

from .. import common as C  # noqa: E402
from .. import interface as I  # noqa: E402
from . import parts as Q  # noqa: E402
from . import profiles as P  # noqa: E402

EXPLODE = {  # z offsets for the exploded view (mm); large so every laminate layer shows in front of L3
    "L0_foil": -48.0, "L1_channel_sheet": -36.0, "L1s_WE2_shim": -33.0, "L1b_die_film": -24.0, "L2_TPE": -12.0,
    "seam_adhesive": -12.0, "L3_body": 0.0, "die_glass": -20.0, "die_metal": -20.0, "die_passivation": -20.0,
}

MAT_FC = {"COC_foil": "#9fc8e6", "COC": "#cfe3ef", "TPE": "#f2b45e", "elastomer": "#555555", "glass": "#8fd3c5",
          "gold": "#e8b923", "pcb": "#2e7d32", "PTFE": "#f4f4f4"}


def _opaque(m):
    r, g, b, _ = C.color(m)
    return (r, g, b, 1.0)


def _translate(wp, dz):
    return wp.translate((0, 0, dz))


def iso_views(out):
    parts = Q.all_parts()
    items = [(w, _opaque(m)) for n, w, m in parts if n not in ("die_metal", "die_passivation")]
    C.render_png(items, out / "card_iso_top.png", view="iso",
                 title="Card A (C2 laminate) - iso from front-right-top (opaque): vents, bores, die window, thermal "
                       "break, ID recess, poka-yoke chamfer (back right)")
    # bottom: rotate the card 180 deg about the x axis and look from the iso direction
    rot = [(w.rotate((0, 0, 0), (1, 0, 0), 180), _opaque(m)) for n, w, m in parts
           if n in ("L0_foil", "die_glass", "die_metal", "L3_body", "L1_channel_sheet")]
    C.render_png(rot, out / "card_iso_bottom.png", view="iso",
                 title="Card A - iso from below (card turned over about x): foil, port holes, contact window, "
                       "die pads")
    ex = []
    for n, w, m in parts:
        dz = EXPLODE.get(n, 10.0)
        if n in ("die_metal", "die_passivation"):
            continue
        ex.append((_translate(w, dz), _opaque(m)))
    C.render_png(ex, out / "card_exploded.png", view="iso", size=(10, 13),
                 title="Exploded: L0 foil / L1 channel sheet + WE2 shim / L1b film + die / L2 TPE + seam / "
                       "L3 body / L4 discs")


# ------------------------------------------------------------------------------------------------ 2D helpers


def _patch(ax, geom, **kw):
    if geom.is_empty:
        return
    for g in (geom.geoms if isinstance(geom, MultiPolygon) or hasattr(geom, "geoms") else [geom]):
        if g.geom_type != "Polygon":
            continue
        ax.add_patch(MPoly(np.array(g.exterior.coords), closed=True, **kw))
        for r in g.interiors:
            ax.add_patch(MPoly(np.array(r.coords), closed=True, fc="white", ec=kw.get("ec", "k"),
                               lw=kw.get("lw", 0.3)))


def _rings(ax, geom, color, lw=0.8, ls="-"):
    """Draw every ring (exterior and holes) of a polygon geometry as a line."""
    for g in getattr(geom, "geoms", [geom]):
        if g.geom_type != "Polygon":
            continue
        for r in [g.exterior] + list(g.interiors):
            a = np.array(r.coords)
            ax.plot(a[:, 0], a[:, 1], color=color, lw=lw, ls=ls)


def plan_L1(out):
    fig, ax = plt.subplots(figsize=(15, 10.5), dpi=150)
    _patch(ax, P.L1(), fc="#cfe3ef", ec="k", lw=0.3)
    _patch(ax, P.L1s_shim(), fc="#7fa7c9", ec="k", lw=0.3)
    for k, v in I.VALVES.items():
        ax.add_patch(plt.Circle(v.xy, v.tip_d / 2, fill=False, ec="red" if v.klass == "slot" else "k", lw=0.5))
        ax.text(v.xy[0], v.xy[1] + 0.9, k, fontsize=5, ha="center", color="darkred")
    for k, p in I.PORTS.items():
        ax.text(p.xy[0] + 1.2, p.xy[1] - 0.6, k, fontsize=5, color="green")
    for k in ("IC1", "IC2", "RCj", "RS", "MC", "BW"):
        c = I.CHAMBERS[k].center
        ax.text(c[0], c[1], k, fontsize=7, ha="center", va="center")
    ax.text(*P.PIN_ROUND, "pin\n(round)", fontsize=5, ha="center", va="center")
    ax.text(*P.PIN_SLOT, "pin\n(slot)", fontsize=5, ha="center", va="center")
    ax.set_xlim(-1, 76.5)
    ax.set_ylim(-1, 51)
    ax.set_aspect("equal")
    ax.grid(lw=0.2)
    ax.set_title("L1 channel sheet 0.175 mm COC, seen from the top (white = through-cut; 5 islands carried on the "
                 "transfer liner); dark blue = WE2 shim 0.15; circles = valve tips (red: slot class)", fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "plan_L1.png")
    plt.close(fig)


def _stack_plan(ax, xlim, ylim):
    _patch(ax, P.L1(), fc="#cfe3ef", ec="#7a9cb5", lw=0.3)
    _patch(ax, P.L1s_shim(), fc="#7fa7c9", ec="k", lw=0.3)
    _patch(ax, P.film_outline().difference(P.l1_cuts().intersection(P.DIE)), fc="#555555", ec="none", alpha=0.25)
    for g in P.l2_cut_named().values():
        _rings(ax, g, "#e08a00", lw=1.0)
    _rings(ax, P.l3_through(), "k", lw=1.2)
    for k, (g, _) in P.l3_blind_bottom().items():
        _rings(ax, g, "#666666", lw=0.8, ls="--")
    for k, g in P.metal().items():
        _patch(ax, g, fc="#e8b923", ec="none", alpha=0.6)
    for k, g in P.passivation_openings().items():
        _rings(ax, g, "#2e7d32", lw=0.6)
    _rings(ax, P.DIE, "#1b9e77", lw=1.0, ls=":")
    for k, v in I.VALVES.items():
        if xlim[0] - 1 < v.xy[0] < xlim[1] + 1 and ylim[0] - 1 < v.xy[1] < ylim[1] + 1:
            ax.add_patch(plt.Circle(v.xy, v.tip_d / 2, fc="none", ec="red", lw=0.8, ls="--"))
            ax.text(v.xy[0], v.xy[1], k, fontsize=6, ha="center", va="center", color="darkred", weight="bold")
    for k, p in I.PORTS.items():
        if xlim[0] < p.xy[0] < xlim[1] and ylim[0] < p.xy[1] < ylim[1]:
            ax.text(p.xy[0], p.xy[1] - 0.8, k, fontsize=6, ha="center", color="green")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.grid(lw=0.2)


def zooms(out):
    leg = ("light blue = L1 sheet (white = cut); orange = L2 TPE cut edge; black = L3 through features (bores, merged\n"
           "slots, window, notches); grey dashed = L3 blind cavity; grey wash = L1b film; yellow = die metal; green = "
           "passivation openings; teal dotted = die; red dashed = valve tips")
    fig, ax = plt.subplots(figsize=(12, 10), dpi=160)
    _stack_plan(ax, (23.0, 40.5), (17.0, 33.5))
    ax.set_title("Zoom: valve island I (ladder, DEV-1)\n" + leg, fontsize=7)
    fig.tight_layout()
    fig.savefig(out / "zoom_valve_island.png")
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(12, 11), dpi=170)
    _stack_plan(ax, (47.5, 63.5), (16.0, 34.0))
    ax.set_title("Zoom: junction J, gates, readout cell, die (electrode face seen through the card from the top)\n"
                 + leg, fontsize=7)
    fig.tight_layout()
    fig.savefig(out / "zoom_junction_cell.png")
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(15, 9), dpi=170)
    _stack_plan(ax, (54.6, 61.5), (22.8, 26.4))
    ax.set_title("Zoom: readout cell, CE/RE pocket, lane fingers and trace routing\n" + leg, fontsize=7)
    fig.tight_layout()
    fig.savefig(out / "zoom_cell_electrodes.png")
    plt.close(fig)


# ------------------------------------------------------------------------------------------------ sections


def _section_tris(wp, axis, val):
    """Triangles of the cut faces of wp on the plane axis = val, projected to (u, z)."""
    bb = wp.val().BoundingBox() if len(wp.vals()) == 1 else cq.Compound.makeCompound(wp.vals()).BoundingBox()
    eps = 0.0005
    if axis == "y":
        if not (bb.ymin <= val <= bb.ymax):
            return []
        slab = cq.Workplane("XY").box(200, 2 * eps, 50, centered=(True, True, True)).translate((40, val, 0))
    else:
        if not (bb.xmin <= val <= bb.xmax):
            return []
        slab = cq.Workplane("XY").box(2 * eps, 200, 50, centered=(True, True, True)).translate((val, 30, 0))
    try:
        cut = cq.Compound.makeCompound([s for v in wp.vals() for s in v.Solids()]).intersect(slab.val())
    except Exception:
        return []
    tris = []
    n_ax = np.array([0, 1, 0]) if axis == "y" else np.array([1, 0, 0])
    for f in cut.Faces():
        nrm = f.normalAt()
        if abs(np.dot([nrm.x, nrm.y, nrm.z], n_ax)) < 0.99:
            continue
        c = f.Center()
        if (axis == "y" and c.y > val) or (axis == "x" and c.x > val):
            continue
        v, t = f.tessellate(0.002, 0.2)
        V = np.array([[p.x, p.y, p.z] for p in v])
        uv = V[:, [0, 2]] if axis == "y" else V[:, [1, 2]]
        tris += [uv[list(tt)] for tt in t]
    return tris


def section(out, name, axis, val, xlim, zlim=(-0.3, 6.6), title="", zoom=None, annot=None):
    parts = Q.all_parts()
    panels = [(xlim, zlim)] + ([zoom] if zoom else [])
    fig, axs = plt.subplots(len(panels), 1, figsize=(13, 4.2 * len(panels)), dpi=170, squeeze=False)
    secs = []
    for n, w, m in parts:
        if n in ("die_metal", "die_passivation"):
            continue
        tr = _section_tris(w, axis, val)
        if tr:
            secs.append((n, m, tr))
    for ax, (xl, zl) in zip(axs[:, 0], panels):
        for n, m, tr in secs:
            ax.add_collection(PolyCollection(tr, facecolors=MAT_FC.get(m, "#999999"), edgecolors="none"))
        ax.axhline(0, color="k", lw=0.4)
        ax.set_xlim(*xl)
        ax.set_ylim(*zl)
        ax.set_aspect("equal")
        ax.set_xlabel(("x" if axis == "y" else "y") + " (mm, card coords)", fontsize=7)
        ax.set_ylabel("z (mm)", fontsize=7)
        ax.tick_params(labelsize=6)
        ax.grid(lw=0.2)
        for (u, z, txt) in (annot or []):
            if xl[0] <= u <= xl[1] and zl[0] <= z <= zl[1]:
                ax.annotate(txt, (u, z), fontsize=6, ha="center", color="darkred",
                            bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.75))
    axs[0, 0].set_title(title + "\nfoil light blue / L1 + L3 pale blue (COC) / TPE orange / film + adhesive grey / "
                        "glass die teal / PTFE white; z = 0 = anvil plane; true scale", fontsize=7)
    fig.tight_layout()
    fig.savefig(out / f"{name}.png")
    plt.close(fig)


def sections(out):
    va = [(v.xy[0], 6.5, k) for k, v in I.VALVES.items() if abs(v.xy[1] - 29.95) < 0.01]
    section(out, "section_valves_y29.95", "y", 29.95, (23.5, 40.5),
            title="Section y = 29.95 through V17 (A1 rung), V1 (bridge), V4 (bead rung): D1.5 bores, TPE over the "
                  "0.175 channels, IC1 at right", zoom=((27.0, 32.0), (-0.1, 1.2)), annot=va)
    section(out, "section_chamber_IC1_y38.6", "y", 38.6, (33.0, 47.0),
            title="Section y = 38.6 (0.6 off the IC1 axis): D8 blind bore, 0.5 roof, D2 vent + PTFE disc in D4.4 "
                  "recess; zoom: L1 funnel wall (x 43.3-44) inside the bore, TPE and L3 from the bore wall x 44",
            zoom=((41.0, 45.5), (-0.1, 1.0)))
    section(out, "section_cell_y25", "y", 25.0, (48.5, 63.5), zlim=(-0.3, 6.6),
            title="Section y = 25 through J, WLc, G3 notch, RC under the die, WE2 channel on the shim, V14",
            zoom=((53.5, 62.5), (-0.05, 1.15)),
            annot=[(54.25, 1.1, "G3"), (61.75, 1.1, "V14"), (56.8, 1.1, "RC 0.200"), (59.5, 0.55, "WE2 0.05")])
    section(out, "section_die_x57.85", "x", 57.85, (15.0, 35.0), zlim=(-0.3, 6.6),
            title="Section x = 57.85 through BW, G4 lane, G4 notch, RC, contact window and pads (die over the dry "
                  "window)", zoom=((21.5, 34.0), (-0.05, 1.15)))
