"""PNG/SVG views of the DOCK BASE (matplotlib painter renderer with arbitrary camera; 2D plans and schematic)."""
from __future__ import annotations

import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.collections import PolyCollection  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Polygon as MPoly, Rectangle  # noqa: E402

from .. import common as C  # noqa: E402
from .. import interface as I  # noqa: E402
from . import fluidics as F  # noqa: E402
from . import layout as L  # noqa: E402
from . import params as P  # noqa: E402

_TESS = {}


def _subdivide(v, t, lmax=12.0):
    """Split triangles until every edge < lmax (keeps the painter sort honest for large flat faces)."""
    V = [tuple(p) for p in v]
    out = []
    stack = [tuple(x) for x in t]
    while stack:
        a, b, c = stack.pop()
        pa, pb, pc = np.array(V[a]), np.array(V[b]), np.array(V[c])
        e = max(np.linalg.norm(pa - pb), np.linalg.norm(pb - pc), np.linalg.norm(pc - pa))
        if e <= lmax or len(out) > 400000:
            out.append((a, b, c))
            continue
        V.extend([tuple((pa + pb) / 2), tuple((pb + pc) / 2), tuple((pc + pa) / 2)])
        ab, bc, ca = len(V) - 3, len(V) - 2, len(V) - 1
        stack.extend([(a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca)])
    return np.array(V, float), np.array(out, int)


def _tess(key, obj, tol, lmax=12.0):
    k = (key, tol, lmax)
    if k not in _TESS:
        v, t = C.tessellate(obj, tol)
        if len(t):
            v, t = _subdivide(v, t, lmax)
        _TESS[k] = (v, t)
    return _TESS[k]


def view_matrix(eye):
    eye = np.array(eye, float)
    eye /= np.linalg.norm(eye)
    up = np.array([0, 0, 1.0]) if abs(eye[2]) < 0.99 else np.array([0, 1.0, 0])
    sx = np.cross(up, eye)
    sx /= np.linalg.norm(sx)
    sy = np.cross(eye, sx)
    return np.vstack([sx, sy, eye])


EYES = {"iso_fl": (-1, -1.25, 0.9), "iso_fr": (1, -1.25, 0.9), "rear": (0.35, 1, 0.45), "front": (0, -1, 0),
        "right": (1, 0, 0), "top": (0, 0, 1), "iso_rl": (-1, 1.2, 0.9)}


def render(items, path, eye, title=None, size=(11, 8), dpi=140, labels=None, xlim=None, ylim=None, legend=None,
           note=None, light=(0.3, -0.5, 0.8)):
    """items: list of (key, cq obj, rgba). labels: list of (xyz, text, (dx, dy) in screen mm or None)."""
    M = view_matrix(EYES.get(eye, eye) if isinstance(eye, str) else eye)
    Lg = np.array(light, float)
    Lg /= np.linalg.norm(Lg)
    polys, cols, depth = [], [], []
    for key, obj, rgba in items:
        if obj is None:
            continue
        rgba = np.array(rgba, float)
        v, t = _tess(key, obj, 0.4)
        if len(t) == 0:
            continue
        p = v @ M.T
        tri = v[t]
        n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        nn = np.linalg.norm(n, axis=1)
        nn[nn == 0] = 1
        n = n / nn[:, None]
        facing = n @ M[2]
        shade = 0.50 + 0.50 * np.abs(n @ Lg)
        keep = facing > -1e-6 if rgba[3] >= 0.99 else np.ones(len(t), bool)
        idx = np.nonzero(keep)[0]
        pp = p[t[idx]]
        cc = np.repeat(rgba[None, :], len(idx), axis=0)
        cc[:, :3] = np.clip(cc[:, :3] * shade[idx, None], 0, 1)
        polys.extend(list(pp[:, :, :2]))
        cols.extend(list(cc))
        depth.extend(list(pp[:, :, 2].mean(axis=1)))
    fig, ax = plt.subplots(figsize=size, dpi=dpi)
    order = np.argsort(depth)
    pc = PolyCollection([polys[i] for i in order], facecolors=[cols[i] for i in order],
                        edgecolors=[cols[i] if cols[i][3] >= 0.99 else (0, 0, 0, 0) for i in order], linewidths=0.25)
    ax.add_collection(pc)
    allp = np.vstack(polys)
    ax.set_xlim(*(xlim or (allp[:, 0].min() - 10, allp[:, 0].max() + 10)))
    ax.set_ylim(*(ylim or (allp[:, 1].min() - 10, allp[:, 1].max() + 10)))
    if labels:
        for xyz, txt, off in labels:
            q = np.array(xyz, float) @ M.T
            if off:
                ax.annotate(txt, xy=(q[0], q[1]), xytext=(q[0] + off[0], q[1] + off[1]), fontsize=6.5, ha="center",
                            va="center", arrowprops=dict(arrowstyle="-", lw=0.5, color="0.2"),
                            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="0.6", lw=0.3, alpha=0.9))
            else:
                ax.text(q[0], q[1], txt, fontsize=6.5, ha="center", va="center",
                        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="0.6", lw=0.3, alpha=0.9))
    if legend:
        from matplotlib.patches import Patch
        ax.legend(handles=[Patch(fc=c, ec="0.3", label=t) for t, c in legend], loc="lower left", fontsize=6.5,
                  frameon=True, ncol=2)
    if note:
        ax.text(0.99, 0.01, note, transform=ax.transAxes, fontsize=6, ha="right", va="bottom", color="0.3")
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=10)
    fig.tight_layout()
    fig.savefig(str(path))
    plt.close(fig)
    return str(path)


# ============================================================================================ 2D drawings
def _r(ax, b2, **kw):
    (x0, y0), (x1, y1) = b2
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, **kw))


def top_plan(path, sweep_region=None):
    fig, ax = plt.subplots(figsize=(12, 11), dpi=140)
    claimc = {"UPPER": (0.95, 0.55, 0.25, 0.15), "LOWER": (0.30, 0.65, 0.35, 0.15), "BASE": (0.35, 0.45, 0.85, 0.06)}
    for k, v in P.CL.items():
        (x0, y0, _), (x1, y1, _) = v["box"]
        if k.startswith("BENCH"):
            continue
        c = claimc[k.split("_")[0]]
        _r(ax, ((x0, y0), (x1, y1)), fc=c, ec=c[:3] + (0.8,), lw=0.8, ls="--")
        ax.text(x0 + 2, y1 - 2, k, fontsize=6, va="top", color=c[:3])
    (lx0, ly0, _), (lx1, ly1, _) = P.LOAD_BOX
    _r(ax, ((lx0, ly0), (lx1, ly1)), fc="none", ec="r", lw=0.8, ls=":")
    ax.text((lx0 + lx1) / 2, ly0 + 3, "operator loading path", fontsize=6, color="r", ha="center")
    sw = I.lid_sweep_bbox()
    _r(ax, ((sw[0][0], sw[0][1]), (sw[1][0], sw[1][1])), fc="none", ec="orange", lw=1.0, ls="-.")
    ax.text(sw[1][0] - 3, sw[1][1] - 3, f"lid sweep 0-85 deg (to Y {sw[1][1]:.0f})", fontsize=6, color="orange",
            ha="right", va="top")
    gcol = {"frame": "0.55", "enclosure": "0.75", "tray": "0.85", "bracket": "0.6", "cold": (0.4, 0.7, 1.0),
            "pumps": (0.55, 0.65, 0.85), "bottles": (0.6, 0.85, 0.95), "pneumatics": (0.95, 0.85, 0.3),
            "electronics": (0.3, 0.7, 0.4), "gamry": (0.85, 0.5, 0.25), "sensors": (0.9, 0.4, 0.6),
            "bench": (0.5, 0.5, 0.6)}
    skip_lbl = {"base_plate", "drip_tray", "panel_top_left", "panel_top_right", "panel_top_rear", "panel_left",
                "panel_right", "panel_front_left", "panel_front_right", "panel_front_bay", "panel_rear"}
    big = sorted([it for it in L.ITEMS if it.name not in skip_lbl and not it.name.startswith(("leak_", "post_", "rail",
                  "foot_", "deck_spacer", "pump_isolator"))], key=lambda i: -(i.box[1][2]))
    for it in L.ITEMS:
        if it.name in ("base_plate", "panel_top_left", "panel_top_right", "panel_top_rear"):
            continue
        (x0, y0, _), (x1, y1, _) = it.box
        if it.group in ("enclosure", "frame", "tray", "bracket"):
            _r(ax, ((x0, y0), (x1, y1)), fc="none", ec="0.45", lw=0.35)
        else:
            _r(ax, ((x0, y0), (x1, y1)), fc=gcol.get(it.group, "0.7"), ec="k", lw=0.25, alpha=0.55)
    for r in F.ROUTES:
        a = np.array(r.pts)
        from . import parts as PT
        ax.plot(a[:, 0], a[:, 1], color=PT.tube_color(r)[:3], lw=0.6)
    lbl = {"cold_box": "cold box (4-8 C)\nconjugate + bead vial", "SV_b_selection_valve": "SV_b",
           "cooler_DA024_warm": "Peltier DA-024\n(warm side)", "electronics_box": "electronics bay\n(noisy zone)",
           "A1_bottle_500mL": "A1 500 mL", "HQDP_holder": "HQDP\n(dark)", "waste_bottle_1L": "waste 1 L\n+ air-gap head",
           "FEZ_ch1_P_c": "Flow EZ\nch1 P_c", "FEZ_ch2_P_mv_bottles": "Flow EZ\nch2 P_mv", "bay_deck": "",
           "FR1_filter_regulator": "FR1", "R2_precision_reg": "R2", "gamry_junction_box": "JB",
           "gamry_lead_duct": "cell-lead duct", "Gamry_Ref600plus": "Gamry\nRef 600+", "P_in_pressure_sensor": "P_in\nsensor",
           "switch_valves_3x3-2": "3/2 x3", "FS1_SLF3S_P_a": "FS1", "FS2_P_s": "FS2"}
    for n, t in lbl.items():
        if not t:
            continue
        (x0, y0, _), (x1, y1, _) = L.get(n).box
        dy = -25 if n.startswith("FEZ") else 0
        ax.text((x0 + x1) / 2, (y0 + y1) / 2 + dy, t, fontsize=6.5, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.75))
    for pmp in P.PUMP_ORDER:
        x = L.PUMP_X[pmp]
        ax.text(x, 360, pmp, fontsize=6.5, rotation=90, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.75))
    for pid in I.PORTS:
        p = F.port_dock(pid)
        ax.plot(p[0], p[1], "o", ms=2.2, color="b" if I.PORTS[pid].kind == "liquid" else "orange")
    for k in ("liquid_lines_west", "liquid_lines_east", "lid_umbilical", "gamry_cell_cable", "smfl_peek_line"):
        p = I.PASS_THROUGHS[k]["dock"]
        ax.plot(p[0], p[1], "x", ms=5, color="k")
        ax.text(p[0] + 3, p[1] - 6, k, fontsize=5.5)
    ax.annotate("operator", xy=(235, -5), xytext=(235, -45), ha="center", fontsize=8,
                arrowprops=dict(arrowstyle="->", lw=1))
    ax.annotate("Waters stack\n(left)", xy=(-5, 110), xytext=(-60, 110), ha="center", fontsize=7,
                arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.set_xlim(-90, 590)
    ax.set_ylim(-60, 440)
    ax.set_aspect("equal")
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.grid(lw=0.2, alpha=0.4)
    ax.set_title("DOCK BASE - top plan (top panels removed), dock coordinates; claims dashed; tubes as centre lines",
                 fontsize=10)
    fig.tight_layout()
    fig.savefig(str(path))
    if str(path).endswith(".png"):
        fig.savefig(str(path)[:-4] + ".svg")
    plt.close(fig)


def side_elevation(path, sweep_region):
    """Right elevation as a YZ drawing: every DOCK BASE body (outline, by group), claims, lid sweep, loading path."""
    fig, ax = plt.subplots(figsize=(12, 8.5), dpi=140)
    gcol = {"frame": "0.55", "enclosure": "0.8", "tray": "0.85", "bracket": "0.6", "cold": (0.4, 0.7, 1.0),
            "pumps": (0.55, 0.65, 0.85), "bottles": (0.6, 0.85, 0.95), "pneumatics": (0.95, 0.85, 0.3),
            "electronics": (0.3, 0.7, 0.4), "gamry": (0.85, 0.5, 0.25), "sensors": (0.9, 0.4, 0.6)}
    for it in sorted(L.ITEMS, key=lambda i: -(i.box[1][0] - i.box[0][0])):
        if it.group == "bench" or it.name.startswith(("panel_left", "panel_right")):
            continue
        (x0, y0, z0), (x1, y1, z1) = it.box
        _r(ax, ((y0, z0), (y1, z1)), fc=gcol.get(it.group, "0.7"), ec="k", lw=0.25, alpha=0.35)
    for k, c in (("UPPER_lid_closed", (0.95, 0.55, 0.25)), ("LOWER_nest_anvil", (0.3, 0.65, 0.35)),
                 ("LOWER_bay", (0.3, 0.65, 0.35))):
        (_, y0, z0), (_, y1, z1) = P.CL[k]["box"]
        _r(ax, ((y0, z0), (y1, z1)), fc=c + (0.18,), ec=c, lw=1.0, ls="--")
        ax.text(y0 + 3, z1 - 3, k, fontsize=7, va="top", color=c)
    ax.add_patch(MPoly(list(sweep_region.exterior.coords), closed=True, fc=(0.95, 0.55, 0.25, 0.15),
                       ec=(0.9, 0.4, 0.1), lw=1.2))
    ax.text(250, 360, "lid sweep 0-85 deg\n(UPPER claim rotated about the hinge)", fontsize=8, color=(0.8, 0.35, 0.05),
            ha="center")
    hy, hz = P.HINGE["point"][1], P.HINGE["point"][2]
    ax.plot(hy, hz, "ko", ms=4)
    ax.text(hy + 4, hz + 4, "hinge axis (Y 195, Z 190)", fontsize=7)
    (_, ly0, lz0), (_, ly1, lz1) = P.LOAD_BOX
    _r(ax, ((ly0, lz0), (ly1, lz1)), fc="none", ec="r", lw=1.0, ls=":")
    ax.text((ly0 + ly1) / 2, lz1 - 8, "loading path", color="r", fontsize=7, ha="center")
    ax.plot([0, P.FY], [P.FZ, P.FZ], "k-", lw=0.6)
    ax.axhline(180, xmin=0, xmax=1, color="0.4", lw=0.5, ls=":")
    ax.text(312, 182, "rear-low cover Z 180 (sweep clears by 1.9 mm)", fontsize=7, ha="right", va="bottom")
    for txt, y, z in (("cold box / bottles (behind)", 70, 60), ("electronics (left) /\nwaste (right)", 300, 100),
                      ("pump bank", 370, 120), ("drip tray + base plate", 210, 5), ("Flow EZ x2", 258, 60)):
        ax.text(y, z, txt, fontsize=7, ha="center", bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none",
                                                              alpha=0.8))
    ax.annotate("operator (front)", xy=(0, 90), xytext=(-70, 90), fontsize=8, ha="center", va="center",
                arrowprops=dict(arrowstyle="->"))
    ax.set_xlim(-110, 440)
    ax.set_ylim(-10, 400)
    ax.set_aspect("equal")
    ax.grid(lw=0.2, alpha=0.4)
    ax.set_xlabel("Y (mm), front -> rear")
    ax.set_ylabel("Z (mm)")
    ax.set_title("Right elevation (all X superimposed, outlines): lid sweep, claims, loading path; dock coordinates",
                 fontsize=10)
    fig.tight_layout()
    fig.savefig(str(path))
    plt.close(fig)


def bench_plan(path, calc):
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=140)
    A = P.ACQUITY
    sx1 = -P.STACK_GAP
    sx0 = sx1 - A["w"]
    _r(ax, ((sx0, 0), (sx1, A["d"])), fc=(0.85, 0.85, 0.9), ec="k", lw=0.8)
    ax.text((sx0 + sx1) / 2, A["d"] / 2, f"Waters ACQUITY stack\nBSM + SM-FL (+CH-A)\n{A['w']:.0f} W x {A['d']:.0f} D x "
            f"{A['h']:.0f} H mm\n(I-Class spec sheet;\nSM-FL footprint UNVERIFIED)", ha="center", va="center", fontsize=8)
    _r(ax, ((0, 0), (P.FX, P.FY)), fc=(0.75, 0.85, 1.0), ec="k", lw=0.8)
    ax.text(P.FX / 2, P.FY / 2, f"DOCK\n{P.FX:.0f} x {P.FY:.0f} x {P.FZ:.0f} mm\n(lid open: {388:.0f} high)",
            ha="center", va="center", fontsize=8)
    (lx0, ly0, _), (lx1, ly1, _) = I.SPACE_CLAIMS["UPPER_lid_closed"]["box"]
    _r(ax, ((lx0, ly0), (lx1, ly1)), fc="none", ec=(0.9, 0.5, 0.2), lw=0.8, ls="--")
    ax.text((lx0 + lx1) / 2, ly0 + 8, "card bay / lid", ha="center", fontsize=7, color=(0.8, 0.4, 0.1))
    g = P.GAMRY
    _r(ax, ((g[0][0], g[0][1]), (g[1][0], g[1][1])), fc=(0.95, 0.75, 0.55), ec="k", lw=0.8)
    ax.text((g[0][0] + g[1][0]) / 2, (g[0][1] + g[1][1]) / 2, "Gamry\nRef 600+\n90 x 270\n(190 H)", ha="center",
            va="center", fontsize=7)
    ax.plot([sx1, 0], [110, 110], color=(0.85, 0.2, 0.6), lw=1.5)
    ax.text(-P.STACK_GAP / 2, 125, "PEEK\nline", fontsize=6, ha="center", color=(0.85, 0.2, 0.6))
    ax.plot([(g[0][0] + g[1][0]) / 2, (g[0][0] + g[1][0]) / 2, P.FX], [g[0][1], P.BULKHEAD[1], P.BULKHEAD[1]],
            color="k", lw=1.2)
    ax.text(P.FX + 15, P.BULKHEAD[1] - 20, "cell cable\n60 cm", fontsize=6)
    ax.plot([sx0 - 30, g[1][0] + 30], [P.BENCH_DEPTH, P.BENCH_DEPTH], "k--", lw=0.6)
    ax.text(g[1][0] + 25, P.BENCH_DEPTH + 8, f"bench depth {P.BENCH_DEPTH:.0f} (UNVERIFIED)", fontsize=7, ha="right")
    ax.plot([sx0 - 30, g[1][0] + 30], [0, 0], "k-", lw=1.0)
    ax.text(sx0 - 25, -18, "bench front edge", fontsize=7)
    ax.annotate("", xy=(sx0, -45), xytext=(g[1][0], -45), arrowprops=dict(arrowstyle="<->", lw=0.8))
    ax.text((sx0 + g[1][0]) / 2, -60, f"total width {calc['width']:.0f} mm (stack + {P.STACK_GAP:.0f} gap + dock + "
            f"{g[0][0] - P.FX:.0f} gap + Gamry)", ha="center", fontsize=8)
    ax.annotate("operator", xy=(P.FX / 2, -75), xytext=(P.FX / 2, -120), ha="center", fontsize=8,
                arrowprops=dict(arrowstyle="->", lw=1))
    ax.set_xlim(sx0 - 60, g[1][0] + 60)
    ax.set_ylim(-130, P.BENCH_DEPTH + 40)
    ax.set_aspect("equal")
    ax.grid(lw=0.2, alpha=0.4)
    ax.set_xlabel("X (mm, dock coordinates)")
    ax.set_ylabel("Y (mm)")
    ax.set_title("Bench layout, to scale (plan): Waters stack left, dock, Gamry right", fontsize=10)
    fig.tight_layout()
    fig.savefig(str(path))
    plt.close(fig)


def schematic(path):
    """Fluidic schematic of all lines (not to scale)."""
    fig, ax = plt.subplots(figsize=(16, 10.5), dpi=130)
    B = {}

    def box(k, x, y, w, h, txt, fc):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4", fc=fc, ec="k", lw=0.7))
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=7.2)
        B[k] = (x, y, w, h)

    def pin(k, side, f=0.5):
        x, y, w, h = B[k]
        return {"l": (x, y + f * h), "r": (x + w, y + f * h), "t": (x + f * w, y + h), "b": (x + f * w, y)}[side]

    def line(a, b, c, lab=None, ls="-", lw=1.2, mid=None, fs=6.2):
        pts = [a] + (mid or []) + [b]
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=c, lw=lw, ls=ls)
        if lab:
            i = len(pts) // 2
            p, q = pts[i - 1], pts[i]
            ax.text((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + 0.6, lab, fontsize=fs, ha="center", va="bottom", color=c,
                    bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))

    vol = {r.port: r for r in F.ROUTES if r.port}
    import math as _m

    def v(pid):
        r = vol[pid]
        idm = F.TUBES[r.tube][1]
        return f"{pid}: {F.TUBES[r.tube][0]} ID {idm:.3f}, {r.total / 1000:.2f} m, {_m.pi / 4 * idm ** 2 * r.total + r.inline_uL:.1f} uL"

    # card (centre)
    box("card", 44, 30, 22, 40, "CARD A\n(lid closed)\n\nliquid ports\nfrom below\n(anvil face seals)\n\ngas ports\nfrom the lid",
        (0.85, 0.92, 1.0))
    # left side
    box("smfl", 0, 82, 13, 8, "Waters SM-FL\n(Inject Start ->\nLabJack U3)", (0.88, 0.88, 0.92))
    box("pin", 18, 82, 9, 6, "P_in sensor\n(flow-through)", (0.95, 0.8, 0.9))
    box("sv", 18, 58, 10, 10, "SV_b 6-port\nvial|P_b|waste\nair|A1|coil", (0.85, 0.75, 0.95))
    box("cold", 0, 44, 14, 24, "COLD BOX 4-8 C\n\nbead vial 2 mL\n(rocked)\n\nconjugate tube\n2 mL", (0.75, 0.88, 1.0))
    box("sb", 18, 40, 10, 9, "S_b Centris\n250 uL", (0.8, 0.85, 0.95))
    box("sic1", 18, 26, 10, 8, "S_IC1 Centris\n1 mL", (0.8, 0.85, 0.95))
    box("sic2", 18, 14, 10, 8, "S_IC2 Centris\n1 mL", (0.8, 0.85, 0.95))
    box("sa", 18, 2, 10, 8, "S_A Centris\n1 mL (dispense)", (0.8, 0.85, 0.95))
    # right side
    box("src", 80, 2, 10, 8, "S_RC Centris\n250 uL (pull)", (0.8, 0.85, 0.95))
    box("hq", 80, 46, 10, 8, "HQDP 15 mL\n(dark sleeve)", (0.8, 0.95, 0.95))
    box("waste", 96, 22, 12, 16, "WASTE 1 L\nair-gap head\n(9 nipples)\nlevel sensor", (0.85, 0.75, 0.65))
    box("a1", 96, 48, 12, 10, "A1 500 mL\n-> manifold\n-> 5 pumps", (0.75, 0.85, 1.0))
    box("fez1", 64, 84, 11, 7, "Flow EZ ch1\n0-345 mbar", (1.0, 0.95, 0.7))
    box("fez2", 78, 84, 11, 7, "Flow EZ ch2\n0-345 mbar", (1.0, 0.95, 0.7))
    box("sw", 78, 70, 11, 8, "3/2 valves x3\nP_mv | conj |\nHQDP bottle", (1.0, 0.95, 0.7))
    box("air", 96, 82, 12, 9, "lab air 400-700 kPa\nFR1 300 kPa (lid)\nR2 120 kPa (FEZ)", (1.0, 0.9, 0.6))
    box("fs1", 32, 5, 6, 4, "FS1", (0.95, 0.8, 0.9))
    box("fs2", 72, 5, 6, 4, "FS2", (0.95, 0.8, 0.9))
    cl = {"liq": (0.15, 0.4, 0.9), "smp": (0.85, 0.2, 0.6), "bead": (0.6, 0.2, 0.85), "reag": (0.1, 0.6, 0.6),
          "waste": (0.55, 0.35, 0.2), "gas": (0.85, 0.65, 0.05)}
    cy = lambda f: pin("card", "l", f)  # noqa: E731
    cr = lambda f: pin("card", "r", f)  # noqa: E731
    line(pin("smfl", "r"), pin("pin", "l", 0.6), cl["smp"], "PEEK 0.127, 0.2 m outside (UNVERIFIED)", mid=None)
    line(pin("pin", "r", 0.6), cy(0.92), cl["smp"], v("P_in"), mid=[(40, 85.6), (40, 66.8)])
    line(pin("sv", "r", 0.5), cy(0.78), cl["bead"], v("P_b"), mid=[(36, 63), (36, 61.2)])
    line(pin("cold", "r", 0.85), pin("sv", "l", 0.6), cl["bead"], "vial line FEP 0.5")
    line(pin("sb", "t"), pin("sv", "b"), cl["bead"], "holding coil FEP 0.5, 95 uL")
    line(pin("cold", "r", 0.2), cy(0.66), cl["reag"], v("P_cf"), mid=[(16, 48.8), (16, 37), (34, 37), (34, 56.4)])
    line(pin("sic1", "r"), cy(0.5), cl["liq"], v("P_d1"), mid=[(38, 30), (38, 50)])
    line(pin("sic2", "r"), cy(0.36), cl["liq"], v("P_d2"), mid=[(40, 18), (40, 44.4)])
    line(pin("sa", "r"), pin("fs1", "l"), cl["liq"])
    line(pin("fs1", "r"), cy(0.2), cl["liq"], v("P_a"), mid=[(42, 7), (42, 38)])
    line(pin("sa", "b"), cr(0.08), cl["liq"], v("P_a2"), mid=[(23, -1), (70, -1), (70, 33.2)])
    line(cr(0.28), pin("fs2", "t"), cl["liq"], v("P_s"), mid=[(75, 41.2)])
    line(pin("fs2", "r"), pin("src", "l"), cl["liq"])
    line(pin("hq", "l"), cr(0.55), cl["reag"], v("P_rf"), mid=[(72, 50), (72, 52)])
    line(cr(0.4), pin("waste", "l", 0.7), cl["waste"], v("P_wo"), mid=[(92, 46), (92, 33.2)])
    line(cy(0.06), pin("waste", "b"), cl["waste"], v("P_byp"), mid=[(30, 32.4), (30, -6), (102, -6)])
    line(pin("a1", "b"), pin("waste", "t"), cl["liq"], "A1 -> pump valves (5 lines)", ls=":")
    line(pin("src", "r"), pin("waste", "b", 0.3), cl["waste"], "pump waste ports (5) via air gap", ls=":",
         mid=[(99.6, 6)])
    line(pin("fez1", "b"), pin("card", "t", 0.25), cl["gas"], "P_c gas (umbilical)", mid=[(69.5, 78), (49.5, 78)])
    line(pin("fez2", "b"), pin("sw", "t"), cl["gas"])
    line(pin("sw", "l"), pin("card", "t", 0.75), cl["gas"], "P_mv gas (umbilical)", mid=[(60.5, 74)])
    line(pin("sw", "b"), pin("hq", "t"), cl["gas"], "bottle pressure (fill at insertion)")
    line(pin("sw", "r", 0.2), pin("cold", "t"), cl["gas"], "conj. tube pressure", mid=[(92, 71.6), (92, 96), (7, 96)])
    line(pin("air", "l"), pin("fez2", "r"), cl["gas"], "120 kPa supply")
    ax.text(0, -12, "Line volumes = routed CAD length (DOCK BASE) + estimated LOWER-internal length (gland -> pass-through -> port, "
            "owner DOCK LOWER) + external; inline sensors +1 uL each (UNVERIFIED). Not to scale.", fontsize=7)
    from matplotlib.lines import Line2D
    ax.legend(handles=[Line2D([0], [0], color=c, lw=2, label=k) for k, c in
                       [("sample (PEEK)", cl["smp"]), ("beads", cl["bead"]), ("reagent fill", cl["reag"]),
                        ("clean A1 / pump lines", cl["liq"]), ("waste (air gap)", cl["waste"]), ("gas", cl["gas"])]],
              loc="upper center", fontsize=7, ncol=6, frameon=False, bbox_to_anchor=(0.5, 1.02))
    ax.set_xlim(-2, 112)
    ax.set_ylim(-15, 100)
    ax.axis("off")
    ax.set_title("DOCK BASE fluidic schematic - 11 liquid ports, 2 gas ports, supply, waste, air", fontsize=11, pad=18)
    fig.tight_layout()
    fig.savefig(str(path))
    fig.savefig(str(path)[:-4] + ".svg")
    plt.close(fig)


def electronics_layout(path, power):
    """Electronics bay as four YZ elevations, one per X slab, seen from +X (no overlapping bodies per panel)."""
    eb = L.get("electronics_box").box
    slabs = [(4, 40, "X 4-40 (left wall)"), (40, 74, "X 40-74"), (74, 100, "X 74-100 (plate + boards)"),
             (100, 142, "X 100-142")]
    fig, axs = plt.subplots(1, 4, figsize=(17, 6.5), dpi=140)
    pal = {"PSU": (0.95, 0.75, 0.45), "mains": (0.95, 0.55, 0.45), "LabJack": (0.55, 0.75, 0.95),
           "USB": (0.55, 0.75, 0.95), "Fluigent": (0.95, 0.9, 0.5), "fan": (0.8, 0.8, 0.8), "intake": (0.85, 0.85, 0.85),
           "mount": (0.75, 0.75, 0.78), "connector": (0.6, 0.6, 0.65)}
    for ax, (xa, xb, ttl) in zip(axs, slabs):
        _r(ax, ((eb[0][1], eb[0][2]), (eb[1][1], eb[1][2])), fc="none", ec="k", lw=1.0)
        for it in L.ITEMS:
            if it.group != "electronics" or it.name in ("electronics_box", "estop", "status_light"):
                continue
            (x0, y0, z0), (x1, y1, z1) = it.box
            xc = (x0 + x1) / 2
            if not (xa <= xc < xb):
                continue
            c = next((v for k, v in pal.items() if it.name.startswith(k)), (0.45, 0.75, 0.5))
            _r(ax, ((y0, z0), (y1, z1)), fc=c, ec="k", lw=0.6, alpha=0.9)
            ax.text((y0 + y1) / 2, (z0 + z1) / 2, it.name.replace("_", " ") + f"\nX {x0:.0f}-{x1:.0f}", fontsize=6.5,
                    ha="center", va="center", rotation=90 if (y1 - y0) < 45 else 0)
        ax.set_xlim(eb[0][1] - 10, P.FY + 5)
        ax.set_ylim(0, 335)
        ax.set_aspect("equal")
        ax.grid(lw=0.2, alpha=0.4)
        ax.set_xlabel("Y (mm)")
        ax.set_ylabel("Z (mm)")
        ax.set_title(ttl, fontsize=9)
        ax.axvline(P.FY - 2, color="0.3", lw=1.5)
    fig.suptitle(f"Electronics bay (X 4-144, Y 207-396, Z 35-318; noisy EMC zone), slabs seen from +X. Peak "
                 f"{power['peak_W']:.0f} W DC, average {power['avg_W']:.0f} W; bay heat {power['q_bay_W']:.0f} W -> "
                 f"{power['airflow_Lmin']:.0f} L/min for a 10 K rise (rear panel at Y 418)", fontsize=9)
    fig.tight_layout()
    fig.savefig(str(path))
    plt.close(fig)
