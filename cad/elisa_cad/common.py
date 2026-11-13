"""Shared CAD helpers (tested headless in this environment, 2026-11-13; see cad/README.md).

* out_dir(module)                -> cad/out/<module>/ (created)
* export_step(obj, path)         -> STEP of a cq.Workplane / cq.Shape / cq.Assembly (assembly keeps names + colours)
* export_svg(obj, path, view)    -> CadQuery hidden-line SVG (orthographic line drawing)
* render_png(items, path, view)  -> shaded PNG via matplotlib (Agg) from tessellation; VTK offscreen is NOT
                                    usable here (no X, EGL or OSMesa), so this is the PNG route for all modules.
* COLORS / color(material)       -> one colour per material (RGBA 0-1), used by every module.
* assembly(parts)                -> cq.Assembly from [(name, obj, material), ...]

Units mm. Views: "top" (looking -Z), "bottom" (+Z), "front" (looking +Y, from the operator), "back", "left"
(looking +X), "right" (looking -X), "iso" (from front-right-top), "iso_back" (from back-left-top).
"""
from __future__ import annotations

import os
from pathlib import Path

import cadquery as cq
import numpy as np

CAD_ROOT = Path(__file__).resolve().parents[1]          # .../cad
OUT_ROOT = CAD_ROOT / "out"

COLORS = {  # material -> RGBA
    "COC": (0.80, 0.90, 0.95, 0.55),          # card body, translucent
    "COC_foil": (0.70, 0.85, 0.95, 0.70),
    "TPE": (0.95, 0.75, 0.45, 0.90),
    "glass": (0.60, 0.85, 0.80, 0.70),
    "gold": (0.95, 0.75, 0.20, 1.0),
    "aluminium": (0.72, 0.74, 0.78, 1.0),
    "anodised": (0.35, 0.38, 0.45, 1.0),
    "steel": (0.55, 0.57, 0.60, 1.0),
    "PEEK": (0.85, 0.75, 0.55, 1.0),
    "NdFeB": (0.75, 0.15, 0.15, 1.0),
    "copper": (0.85, 0.50, 0.25, 1.0),
    "elastomer": (0.15, 0.15, 0.15, 1.0),
    "PTFE": (0.97, 0.97, 0.97, 1.0),
    "liquid": (0.30, 0.55, 0.95, 0.60),
    "pcb": (0.10, 0.45, 0.20, 1.0),
    "envelope": (0.55, 0.65, 0.80, 0.35),      # placed envelope bodies (pumps, bottles, electronics)
    "claim_upper": (0.95, 0.55, 0.25, 0.20),
    "claim_lower": (0.30, 0.65, 0.35, 0.20),
    "claim_base": (0.35, 0.45, 0.85, 0.20),
    "keepout": (0.90, 0.20, 0.20, 0.25),
    "cold": (0.40, 0.70, 1.00, 1.0),
    "heater": (0.95, 0.40, 0.30, 1.0),
    "default": (0.70, 0.70, 0.70, 1.0),
}


def color(material: str):
    return COLORS.get(material, COLORS["default"])


def out_dir(module: str) -> Path:
    d = OUT_ROOT / module
    d.mkdir(parents=True, exist_ok=True)
    return d


def _shape(obj):
    if isinstance(obj, cq.Workplane):
        vals = [v for v in obj.vals() if isinstance(v, cq.Shape)]
        return cq.Compound.makeCompound(vals) if len(vals) != 1 else vals[0]
    if isinstance(obj, cq.Assembly):
        return obj.toCompound()
    return obj


def assembly(parts, name="assy"):
    """parts: iterable of (name, cq object, material). Returns cq.Assembly with colours."""
    a = cq.Assembly(name=name)
    for nm, obj, mat in parts:
        r, g, b, al = color(mat)
        a.add(obj, name=nm, color=cq.Color(r, g, b, al))
    return a


def export_step(obj, path):
    path = str(path)
    if isinstance(obj, cq.Assembly):
        obj.export(path, exportType="STEP")
    else:
        cq.exporters.export(_shape(obj) if not isinstance(obj, cq.Workplane) else obj, path, exportType="STEP")
    return path


_VIEW_DIRS = {  # projection direction for CadQuery SVG = direction FROM which the viewer looks (camera position)
    "top": (0, 0, 1), "bottom": (0, 0, -1), "front": (0, -1, 0), "back": (0, 1, 0),
    "left": (-1, 0, 0), "right": (1, 0, 0), "iso": (1, -1, 1), "iso_back": (-1, 1, 1),
}


def export_svg(obj, path, view="iso", width=900, height=650, hidden=False, stroke=0.5):
    shp = _shape(obj)
    opt = {"width": width, "height": height, "marginLeft": 20, "marginTop": 20, "showAxes": False,
           "projectionDir": _VIEW_DIRS[view], "strokeWidth": stroke, "showHidden": hidden}
    cq.exporters.export(cq.Workplane().add(shp), str(path), exportType="SVG", opt=opt)
    return str(path)


def _view_matrix(view):
    """Rows = screen x, screen y, depth (towards viewer) unit vectors in world coords."""
    eye = np.array(_VIEW_DIRS[view], float)
    eye /= np.linalg.norm(eye)
    up = np.array([0, 0, 1.0]) if abs(eye[2]) < 0.99 else np.array([0, 1.0, 0])
    if view == "bottom":
        up = np.array([0, 1.0, 0])
    sx = np.cross(up, eye)
    sx /= np.linalg.norm(sx)
    sy = np.cross(eye, sx)
    return np.vstack([sx, sy, eye])


def tessellate(obj, tol=0.05, ang=0.3):
    shp = _shape(obj)
    verts, tris = shp.tessellate(tol, ang)
    v = np.array([[p.x, p.y, p.z] for p in verts], float)
    t = np.array(tris, int) if len(tris) else np.zeros((0, 3), int)
    return v, t


def render_png(items, path, view="iso", size=(9, 6.5), dpi=150, title=None, tol=0.05, edges=False,
               light=(0.4, -0.6, 0.8), annotate=None, xlim=None, ylim=None):
    """items: list of (cq object, material or RGBA). Flat-shaded, depth-sorted (painter) orthographic render.
    annotate: optional list of (world xyz, text). Returns path."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection

    M = _view_matrix(view)
    L = np.array(light, float)
    L /= np.linalg.norm(L)
    polys, cols, depth = [], [], []
    for obj, mat in items:
        rgba = np.array(color(mat) if isinstance(mat, str) else mat, float)
        v, t = tessellate(obj, tol)
        if len(t) == 0:
            continue
        p = v @ M.T
        tri = v[t]
        n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        nn = np.linalg.norm(n, axis=1)
        nn[nn == 0] = 1
        n = n / nn[:, None]
        facing = n @ M[2]
        shade = 0.45 + 0.55 * np.abs(n @ L)
        keep = facing > -1e-6 if rgba[3] >= 0.99 else np.ones(len(t), bool)
        for k in np.nonzero(keep)[0]:
            polys.append(p[t[k], :2])
            c = rgba.copy()
            c[:3] = np.clip(c[:3] * shade[k], 0, 1)
            cols.append(c)
            depth.append(p[t[k], 2].mean())
    fig, ax = plt.subplots(figsize=size, dpi=dpi)
    if polys:
        order = np.argsort(depth)
        pc = PolyCollection([polys[i] for i in order], facecolors=[cols[i] for i in order],
                            edgecolors=[cols[i] for i in order] if not edges else "k", linewidths=0.15)
        ax.add_collection(pc)
        allp = np.vstack(polys)
        ax.set_xlim(*(xlim or (allp[:, 0].min() - 3, allp[:, 0].max() + 3)))
        ax.set_ylim(*(ylim or (allp[:, 1].min() - 3, allp[:, 1].max() + 3)))
    if annotate:
        for xyz, txt in annotate:
            q = np.array(xyz, float) @ M.T
            ax.text(q[0], q[1], txt, fontsize=6, ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.7))
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=9)
    fig.tight_layout()
    fig.savefig(str(path))
    plt.close(fig)
    return str(path)


def box_from_corners(p0, p1):
    """Axis-aligned solid box between two corners (any order)."""
    x0, y0, z0 = (min(a, b) for a, b in zip(p0, p1))
    x1, y1, z1 = (max(a, b) for a, b in zip(p0, p1))
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def polyline_solid(pts, w, z0, h):
    """Extruded flat-capped strip of width w along a 2D polyline (for channels, lanes, slots)."""
    from shapely.geometry import LineString
    poly = LineString(pts).buffer(w / 2.0, cap_style=2, join_style=1)
    return polygon_solid(list(poly.exterior.coords), z0, h)


def polygon_solid(coords, z0, h):
    pts = [(float(x), float(y)) for x, y in coords]
    if pts[0] == pts[-1]:
        pts = pts[:-1]
    return cq.Workplane("XY").workplane(offset=z0).polyline(pts).close().extrude(h)


def rounded_rect(cx, cy, sx, sy, r, z0, h):
    return (cq.Workplane("XY").workplane(offset=z0).center(cx, cy).rect(sx, sy).extrude(h)
            .edges("|Z").fillet(min(r, min(sx, sy) / 2 - 1e-3)) if r > 0 else
            cq.Workplane("XY").workplane(offset=z0).center(cx, cy).rect(sx, sy).extrude(h))


__all__ = ["COLORS", "color", "out_dir", "assembly", "export_step", "export_svg", "render_png", "tessellate",
           "box_from_corners", "polyline_solid", "polygon_solid", "rounded_rect", "OUT_ROOT", "CAD_ROOT"]
