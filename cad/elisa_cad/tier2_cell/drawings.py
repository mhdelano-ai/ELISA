"""Dimensioned manufacturing drawings of the three custom parts of the tier-2 flow cell (docs/34 section 5.2).

Run from cad/:   python -m elisa_cad.tier2_cell.drawings          (about 1 min)
writes cad/out/tier2_cell/drawings/T2C-001_base.pdf, T2C-002_nozzle_plate.pdf, T2C-003_body.pdf (+ PNG previews).

One A3 sheet per part, third-angle projection, millimetres. Views are hidden-line projections and sections of the
same solids as the STEP files (parts.py), so geometry and drawing cannot drift apart; every dimension value is read
from params.py. Layout follows Xometry's drawing guidance (title block with default-tolerance block, notes at the
top left, revision table at the top right, sheet number at the bottom right, isometric view, threads called out
with series, class and depth, tighter-than-standard tolerances called out and flagged).
"""
from __future__ import annotations

import math
from pathlib import Path

import cadquery as cq
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Circle, PathPatch, Polygon, Rectangle  # noqa: E402
from matplotlib.path import Path as MPath  # noqa: E402
from OCP.BRepAdaptor import BRepAdaptor_Curve  # noqa: E402
from OCP.BRepTools import BRepTools, BRepTools_WireExplorer  # noqa: E402
from OCP.GCPnts import GCPnts_QuasiUniformDeflection  # noqa: E402
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt  # noqa: E402
from OCP.HLRAlgo import HLRAlgo_Projector  # noqa: E402
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape  # noqa: E402
from OCP.TopAbs import TopAbs_EDGE, TopAbs_REVERSED  # noqa: E402
from OCP.TopExp import TopExp_Explorer  # noqa: E402
from OCP.TopoDS import TopoDS  # noqa: E402

from .. import common as C  # noqa: E402
from . import params as P  # noqa: E402
from . import parts as PT  # noqa: E402

OUT = C.out_dir("tier2_cell") / "drawings"
OUT.mkdir(parents=True, exist_ok=True)
DATE = "2026-11-18"
REV = "A"
W, H = 420.0, 297.0                      # A3 landscape, mm
LW_PART, LW_THIN = 0.5, 0.18             # line widths in points
FS, FS_S, FS_T = 7.5, 6.8, 10.0          # font sizes (pt): dimensions, small text, titles (cap height ~1.7 mm)
plt.rcParams["hatch.linewidth"] = 0.35
plt.rcParams["font.family"] = "DejaVu Sans"

VIEWS = {  # projection direction (towards the viewer) and the paper x direction
    "top": ((0, 0, 1), (1, 0, 0)), "bottom": ((0, 0, -1), (1, 0, 0)), "front": ((0, -1, 0), (1, 0, 0)),
    "left": ((-1, 0, 0), (0, -1, 0)), "right": ((1, 0, 0), (0, 1, 0)),
}


# ---- geometry: hidden-line projection, sections -------------------------------------------------------------------
def _shape(o):
    return C._shape(o)


def _discretize_edge(e, defl=0.003):
    c = BRepAdaptor_Curve(e)
    pts = GCPnts_QuasiUniformDeflection(c, defl)
    return [(pts.Value(i).X(), pts.Value(i).Y(), pts.Value(i).Z()) for i in range(1, pts.NbPoints() + 1)]


def project(solid, view, hidden=False):
    d, xd = VIEWS[view]
    algo = HLRBRep_Algo()
    algo.Add(_shape(solid).wrapped)
    algo.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(*d), gp_Dir(*xd))))
    algo.Update()
    algo.Hide()
    h = HLRBRep_HLRToShape(algo)
    comps = [h.VCompound(), h.OutLineVCompound()] + ([h.HCompound()] if hidden else [])
    out = []
    for k, comp in enumerate(comps):
        if comp is None or comp.IsNull():
            continue
        ex = TopExp_Explorer(comp, TopAbs_EDGE)
        while ex.More():
            pts = _discretize_edge(TopoDS.Edge_s(ex.Current()))
            out.append(([(p[0], p[1]) for p in pts], k == 2))
            ex.Next()
    return out


def uv(view, x, y, z):
    """Model point -> projected 2D coordinates of a view (the same frame as HLR)."""
    d, xd = (np.array(v, float) for v in VIEWS[view])
    yd = np.cross(d, xd)
    p = np.array([x, y, z], float)
    return float(p @ xd), float(p @ yd)


def section(solid, view, plane_axis, plane_pos):
    """Cut the solid at plane_axis = plane_pos, keep the half away from the viewer; return (edges, cut-face paths)."""
    d = np.array(VIEWS[view][0], float)
    big = 200.0
    lo = [-big, -big, -big]
    hi = [big, big, big]
    i = "xyz".index(plane_axis)
    if d[i] > 0:          # viewer on the + side: keep the - side
        hi[i] = plane_pos
    else:
        lo[i] = plane_pos
    keeper = cq.Workplane("XY").box(hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2], centered=False) \
        .translate((lo[0], lo[1], lo[2]))
    half = _shape(solid).intersect(_shape(keeper)).clean()
    edges = project(half, view)
    faces = []
    for f in half.Faces():
        bb = f.BoundingBox()
        ext = [bb.xlen, bb.ylen, bb.zlen][i]
        c = [bb.xmin, bb.ymin, bb.zmin][i]
        if ext < 1e-6 and abs(c - plane_pos) < 1e-6:
            faces.append(_face_path(f.wrapped, view))
    return edges, faces


def _wire_pts(wire, face, view):
    pts = []
    we = BRepTools_WireExplorer(wire, face)
    while we.More():
        e = we.Current()
        p = _discretize_edge(e)
        if e.Orientation() == TopAbs_REVERSED:
            p = p[::-1]
        pts += [uv(view, *q) for q in p]
        we.Next()
    return pts


def _face_path(face, view):
    outer = BRepTools.OuterWire_s(face)
    loops = [_wire_pts(outer, face, view)]
    from OCP.TopAbs import TopAbs_WIRE
    ex = TopExp_Explorer(face, TopAbs_WIRE)
    while ex.More():
        w = TopoDS.Wire_s(ex.Current())
        if not w.IsSame(outer):
            loops.append(_wire_pts(w, face, view))
        ex.Next()
    return loops


# ---- sheet and views ----------------------------------------------------------------------------------------------
class View:
    def __init__(self, sheet, view, origin, scale, label=None):
        self.s, self.view, self.o, self.k = sheet, view, np.array(origin, float), scale
        self.label = label

    def p(self, x, y, z):
        u, w = uv(self.view, x, y, z)
        return self.o + self.k * np.array([u, w])

    def pp(self, u, w):
        return self.o + self.k * np.array([u, w])

    def draw(self, solid, hidden=False, cut=None):
        ax = self.s.ax
        if cut:
            edges, faces = section(solid, self.view, *cut)
            from shapely.geometry import Polygon as SPoly
            from shapely.ops import unary_union
            polys = []
            for loops in faces:
                rings = [[tuple(self.pp(*t)) for t in lp] for lp in loops]
                polys.append(SPoly(rings[0], rings[1:]).buffer(0))
            merged = unary_union(polys).buffer(0.02).buffer(-0.02)
            # explicit 45-degree hatch lines, 1.2 mm apart on paper, clipped to the cut faces (a pattern fill
            # renders at different densities in different viewers)
            from shapely.geometry import LineString
            x0, y0, x1, y1 = merged.bounds
            step = 1.2
            c = y0 - x1
            while c < y1 - x0:
                ln = LineString([(x0 - 1, x0 - 1 + c), (x1 + 1, x1 + 1 + c)]).intersection(merged)
                for seg in getattr(ln, "geoms", [ln]):
                    if seg.is_empty or seg.geom_type != "LineString":
                        continue
                    q = np.array(seg.coords)
                    ax.plot(q[:, 0], q[:, 1], color="k", lw=0.22, zorder=1, solid_capstyle="butt")
                c += step * math.sqrt(2.0)
        else:
            edges = project(solid, self.view, hidden)
        for pts, hid in edges:
            q = np.array([self.pp(*t) for t in pts])
            ax.plot(q[:, 0], q[:, 1], color="k", lw=LW_THIN if hid else LW_PART,
                    ls=(0, (3, 2)) if hid else "-", zorder=3, solid_capstyle="round")

    def title(self, text, dy=-7.0, x=None, y=None):
        self.s.text(x if x is not None else self.o[0], y if y is not None else self.o[1] + dy, text, size=FS_T,
                    ha="center", weight="bold")

    def centre_mark(self, x, y, z, r=1.5, ext=1.0):
        c = self.p(x, y, z)
        L = r * self.k + ext
        for dx, dy in ((1, 0), (0, 1)):
            self.s.ax.plot([c[0] - L * dx, c[0] + L * dx], [c[1] - L * dy, c[1] + L * dy], color="k", lw=0.15,
                           ls=(0, (8, 2, 1, 2)), zorder=2)

    def centre_line(self, a, b):
        a, b = self.p(*a), self.p(*b)
        self.s.ax.plot([a[0], b[0]], [a[1], b[1]], color="k", lw=0.15, ls=(0, (8, 2, 1, 2)), zorder=2)


class Sheet:
    def __init__(self, number, title, material, finish, scale, notes, flags, revs, mass_g, general=None):
        self.general = general
        self.fig = plt.figure(figsize=(W / 25.4, H / 25.4))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, W)
        self.ax.set_ylim(0, H)
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self._frame()
        self._title_block(number, title, material, finish, scale, mass_g)
        self._notes(notes, flags)
        self._revisions(revs)

    # ---- primitives
    def text(self, x, y, s, size=FS, ha="left", va="center", rot=0, **kw):
        kw.setdefault("zorder", 6)
        self.ax.text(x, y, s, fontsize=size, ha=ha, va=va, rotation=rot, **kw)

    def line(self, a, b, lw=LW_THIN, **kw):
        kw.setdefault("zorder", 4)
        self.ax.plot([a[0], b[0]], [a[1], b[1]], color="k", lw=lw, solid_capstyle="butt", **kw)

    def arrow(self, tip, tail):
        tip, tail = np.array(tip, float), np.array(tail, float)
        d = tip - tail
        n = np.linalg.norm(d)
        if n < 1e-9:
            return
        d /= n
        L, Wd = 2.2, 0.5
        b = tip - L * d
        nrm = np.array([-d[1], d[0]])
        self.ax.add_patch(Polygon([tip, b + Wd * nrm, b - Wd * nrm], closed=True, color="k", lw=0, zorder=5))

    def dot(self, p):
        self.ax.add_patch(Circle(p, 0.45, color="k", zorder=5))

    @staticmethod
    def width(text, size=FS_S):
        def w(t):
            em = sum(0.68 if (c.isupper() or c.isdigit()) else 0.34 if c in " .,:;|/()-'" else 0.56 for c in t)
            return em * size * 0.3528
        return max(w(t) for t in text.split("\n")) + 0.8

    # ---- frame, title block, notes, revisions
    def _frame(self):
        self.ax.add_patch(Rectangle((10, 10), W - 20, H - 20, fill=False, lw=0.8))
        for i in range(8):
            x = 10 + (W - 20) * (i + 0.5) / 8
            self.text(x, 6, str(i + 1), size=FS_S, ha="center")
            self.text(x, H - 6, str(i + 1), size=FS_S, ha="center")
        for j, z in enumerate("DCBA"):
            y = 10 + (H - 20) * (j + 0.5) / 4
            self.text(6, y, z, size=FS_S, ha="center")
            self.text(W - 6, y, z, size=FS_S, ha="center")

    def _title_block(self, number, title, material, finish, scale, mass_g):
        x0 = W - 10 - 190
        rows = [
            (9, [(190, "TITLE", title, 9.0)]),
            (8, [(52, "DRAWING NO.", number, 8.5), (18, "REV", REV, 8.5), (27, "SHEET", "1 OF 1", 7.0),
                 (20, "SIZE", "A3", 7.0), (45, "SCALE", scale, 6.5), (28, "PROJECTION", "", 6.5)]),
            (8, [(110, "MATERIAL", material, 6.4), (80, "FINISH", finish, 6.4)]),
            (8, [(60, "UNITS", "MILLIMETRES (mm)", 6.5), (45, "PROJECTION", "THIRD ANGLE", 6.5),
                 (85, "DATE", DATE, 6.5)]),
            (8, [(95, "DRAWN", "generated: elisa_cad.tier2_cell.drawings", 5.8), (47.5, "CHECKED", "", 6),
                 (47.5, "APPROVED", "", 6)]),
            (19, [(190, "UNLESS OTHERWISE SPECIFIED", self.general or (
                   "Dimensions in mm.  Geometry not dimensioned here, and the locations of features with a position\n"
                   "tolerance (BASIC), per the STEP model of the same drawing number and revision; standard\n"
                   "tolerance per Xometry.  Do not scale the drawing."), 5.4)]),
        ]
        y = 10 + sum(r[0] for r in rows)
        self.tb_top = y
        for hgt, cells in rows:
            y -= hgt
            x = x0
            for cw, lab, val, vs in cells:
                self.ax.add_patch(Rectangle((x, y), cw, hgt, fill=False, lw=0.5, zorder=4))
                self.text(x + 1.0, y + hgt - 1.6, lab, size=4.8, color="0.3")
                if lab == "PROJECTION" and val == "":
                    self._proj_symbol(x + cw / 2, y + (hgt - 2.4) / 2)
                else:
                    self.text(x + 1.5, y + (hgt - 2.6) / 2.0, val, size=vs)
                x += cw

    def _proj_symbol(self, x, y):
        """Third-angle projection symbol: truncated cone seen from the side (left) and from the end (right)."""
        s = 0.42
        # large end on the left, small end facing the right-hand (end) view: third angle
        self.ax.add_patch(Polygon([(x - 9 * s, y - 3.5 * s), (x - 9 * s, y + 3.5 * s), (x - 3 * s, y + 2 * s),
                                   (x - 3 * s, y - 2 * s)], closed=True, fill=False, lw=0.4, zorder=5))
        self.ax.add_patch(Circle((x + 5 * s, y), 3.5 * s, fill=False, lw=0.4, zorder=5))
        self.ax.add_patch(Circle((x + 5 * s, y), 2.0 * s, fill=False, lw=0.4, zorder=5))

    def _notes(self, notes, flags):
        x, y = 15, H - 16
        self.text(x, y, "NOTES", size=7.5, weight="bold")
        y -= 4.5
        for i, n in enumerate(notes, 1):
            self.text(x, y, f"{i}.", size=FS_S)
            for ln in n.split("\n"):
                self.text(x + 4.5, y, ln, size=FS_S)
                y -= 3.3
            y -= 0.6
        self.notes_bottom = y
        if flags:
            x, y = 158, H - 22
            self.text(x, y, "FLAGGED FEATURES — tighter than the Xometry standard (inspect these)",
                      size=7.0, weight="bold")
            y -= 5.5
            for num, txt in flags:
                lines = txt.split("\n")
                self.flag(x + 2.5, y, num)
                for ln in lines:
                    self.text(x + 7, y, ln, size=FS_S)
                    y -= 3.3
                y -= 1.8

    def flag(self, x, y, num):
        """Triangular flag with the number of a flagged feature; (x, y) = centre."""
        self.ax.add_patch(Polygon([(x - 2.5, y - 1.9), (x + 2.5, y - 1.9), (x, y + 2.4)], closed=True,
                                  facecolor="white", edgecolor="k", lw=0.45, zorder=7))
        self.text(x, y - 0.5, str(num), size=5.6, ha="center", zorder=8)

    def _revisions(self, revs):
        x0 = W - 10 - 150
        y = H - 10
        cols = [(12, "REV"), (22, "DATE"), (92, "DESCRIPTION"), (24, "BY")]
        for r in [[c[1] for c in cols]] + revs:
            y -= 5
            x = x0
            for (cw, _), val in zip(cols, r):
                self.ax.add_patch(Rectangle((x, y), cw, 5, fill=False, lw=0.4, zorder=4))
                self.text(x + 1, y + 2.5, val, size=5.2)
                x += cw

    # ---- annotations
    def dim(self, a, b, at, text, axis="x", side=1, size=FS_S, basic=False, outside_text=None):
        """Linear dimension between paper points a and b along axis; dimension line at x or y = at.
        side: +1 text above (x) / left (y) of the line, -1 below / right. Short dimensions get outside arrows;
        outside_text = 'before' / 'after' puts the text beyond the arrows instead of over the line."""
        a, b = np.array(a, float), np.array(b, float)
        if axis == "x":
            pa, pb = np.array([a[0], at]), np.array([b[0], at])
            for p, q in ((a, pa), (b, pb)):
                sg = 1 if at > p[1] else -1
                self.line((p[0], p[1] + sg * 0.8), (q[0], q[1] + sg * 1.5))
        else:
            pa, pb = np.array([at, a[1]]), np.array([at, b[1]])
            for p, q in ((a, pa), (b, pb)):
                sg = 1 if at > p[0] else -1
                self.line((p[0] + sg * 0.8, p[1]), (q[0] + sg * 1.5, q[1]))
        if (pb - pa) @ (pb - pa) < 1e-12:
            return
        u = (pb - pa) / np.linalg.norm(pb - pa)
        L = np.linalg.norm(pb - pa)
        if L > 8:
            self.line(pa, pb)
            self.arrow(pa, pa + u)
            self.arrow(pb, pb - u)
        else:
            self.line(pa - 5 * u, pb + 5 * u)
            self.arrow(pa, pa - u)
            self.arrow(pb, pb + u)
        mid = (pa + pb) / 2
        if outside_text == "before":
            mid = pa - (6.5 + self.width(text, size) / 2) * u
        elif outside_text == "after":
            mid = pb + (6.5 + self.width(text, size) / 2) * u
        if axis == "x":
            tp = (mid[0], mid[1] + 1.9 * side) if outside_text is None else (mid[0], mid[1])
            self._dimtext(tp, text, size, 0, basic)
        else:
            tp = (mid[0] - 2.0 * side, mid[1]) if outside_text is None else (mid[0], mid[1])
            self._dimtext(tp, text, size, 90, basic)

    def _dimtext(self, p, text, size, rot, basic):
        self.text(p[0], p[1], text, size=size, ha="center", va="center", rot=rot)
        if basic:
            w, h = self.width(text, size) + 1.6, size * 0.3528 + 1.4
            if rot:
                w, h = h, w
            self.ax.add_patch(Rectangle((p[0] - w / 2, p[1] - h / 2), w, h, fill=False, lw=0.45, zorder=6))

    def leader(self, tip, txt_xy, text, ha="left", size=FS_S, dot=False, flag=None):
        """Leader from tip to a text; ha='left' puts the text to the right of the landing. Returns the text's
        bounding box (x0, x1) so that frames can be stacked under it."""
        tip, t = np.array(tip, float), np.array(txt_xy, float)
        sg = 1 if ha == "left" else -1
        land = t - np.array([sg * 2.0, 0])
        self.line(tip, land)
        self.line(land, t - np.array([sg * 0.6, 0]))
        if dot:
            self.dot(tip)
        else:
            self.arrow(tip, land)
        for i, ln in enumerate(text.split("\n")):
            self.text(t[0], t[1] - i * 3.3, ln, size=size, ha=ha)
        w = self.width(text, size)
        x0, x1 = (t[0], t[0] + w) if ha == "left" else (t[0] - w, t[0])
        if flag is not None:
            self.flag(x1 + 3.5 if ha == "left" else x0 - 3.5, t[1], flag)
        return x0, x1

    def frame(self, x, y, sym, cells):
        """Feature control frame, left-middle at (x, y). sym: 'flat' or 'pos'. Returns its right edge."""
        hgt = 4.4
        widths = [6.0] + [max(5.0, self.width(c, 7.0) + 2.4) for c in cells]
        xx = x
        for wdt in widths:
            self.ax.add_patch(Rectangle((xx, y - hgt / 2), wdt, hgt, facecolor="white", edgecolor="k", lw=0.45,
                                        zorder=6))
            xx += wdt
        cx = x + 3.0
        if sym == "par":
            for dx in (-0.8, 0.8):
                self.line((cx + dx - 0.7, y - 1.2), (cx + dx + 0.7, y + 1.2), lw=0.45, zorder=7)
        elif sym == "flat":
            self.ax.add_patch(Polygon([(cx - 2.0, y - 0.9), (cx + 1.0, y - 0.9), (cx + 2.0, y + 0.9),
                                       (cx - 1.0, y + 0.9)], closed=True, fill=False, lw=0.45, zorder=7))
        else:
            self.ax.add_patch(Circle((cx, y), 1.2, fill=False, lw=0.45, zorder=7))
            self.line((cx - 1.9, y), (cx + 1.9, y), lw=0.45, zorder=7)
            self.line((cx, y - 1.9), (cx, y + 1.9), lw=0.45, zorder=7)
        xx = x + widths[0]
        for wdt, c in zip(widths[1:], cells):
            self.text(xx + wdt / 2, y, c, size=7.0, ha="center", zorder=8)
            xx += wdt
        return xx

    def datum(self, tip, letter, direction=(0, -1), length=4.0):
        """Datum feature symbol: filled triangle on the feature at tip, line, square with the letter."""
        tip = np.array(tip, float)
        d = np.array(direction, float)
        d /= np.linalg.norm(d)
        n = np.array([-d[1], d[0]])
        self.ax.add_patch(Polygon([tip, tip + 1.6 * d + 1.1 * n, tip + 1.6 * d - 1.1 * n], closed=True, color="k",
                                  lw=0, zorder=6))
        end = tip + length * d
        self.line(tip + 1.6 * d, end, lw=0.45)
        c = end + 2.4 * d
        self.ax.add_patch(Rectangle((c[0] - 2.4, c[1] - 2.4), 4.8, 4.8, facecolor="white", edgecolor="k", lw=0.45,
                                    zorder=6))
        self.text(c[0], c[1], letter, size=6.5, ha="center", weight="bold", zorder=8)

    def finish(self, x, y, ra, leader_to=None, note=None):
        """Surface texture symbol (material removal required), its point at (x, y), with Ra over the long arm;
        leader_to: a surface point the symbol is attached to by a leader with an arrow."""
        label = ra + (f"   {note}" if note else "")
        arm = max(8.5, 3.6 + self.width(label, 6.5))
        pts = np.array([[-1.5, 1.5], [0, 0], [3.2, 3.8], [arm, 3.8]]) + [x, y]
        self.ax.plot(pts[:, 0], pts[:, 1], color="k", lw=0.45, zorder=6)
        self.line(pts[0], (x + 1.5, y + 1.5), lw=0.45)
        self.text(x + 3.8, y + 5.6, label, size=6.5)
        if leader_to is not None:
            self.line((x, y), leader_to)
            self.arrow(leader_to, (x, y))

    def callout(self, tip, at, text, flag=None, flat=None, ra=None, note=None, dot=True, frame=None):
        """A surface callout: leader to a text, the flag after the text, a flatness frame under the text and
        the surface-texture symbol to the right of that frame."""
        x0, x1 = self.leader(tip, at, text, dot=dot, flag=flag)
        xe = x0
        if flat:
            xe = self.frame(x0, at[1] - 6.5, "flat", [flat])
        elif frame:
            xe = self.frame(x0, at[1] - 6.5, frame[0], frame[1])
        if ra:
            self.finish(xe + 4.0, at[1] - 10.0, ra, note=note)

    def check_overlaps(self, name):
        """Report pairs of texts whose boxes overlap (frames, flags and the title block are drawn on purpose
        around their own texts and are not texts, so they do not count)."""
        r = self.fig.canvas.get_renderer()
        boxes = [(t.get_text(), t.get_window_extent(r)) for t in self.ax.texts if t.get_text().strip()]
        bad = []
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i][1], boxes[j][1]
                ox = min(a.x1, b.x1) - max(a.x0, b.x0)
                oy = min(a.y1, b.y1) - max(a.y0, b.y0)
                if ox > 1.0 and oy > 1.0:
                    bad.append((boxes[i][0][:40], boxes[j][0][:40]))
        for a, b in bad:
            print(f"  {name}: text overlap: {a!r} / {b!r}")
        return bad

    def detail_circle(self, c, r, letter):
        self.ax.add_patch(Circle(c, r, fill=False, lw=0.35, ls=(0, (6, 2)), zorder=4))
        p = np.array(c) + r * np.array([0.72, 0.72])
        self.text(p[0] + 1.6, p[1] + 1.6, letter, size=8, weight="bold")

    def cut_marks(self, a, b, letter, arrow_dir):
        """Section line from a to b with view arrows (arrow_dir = viewing direction) and letters at both ends."""
        a, b = np.array(a, float), np.array(b, float)
        self.ax.plot([a[0], b[0]], [a[1], b[1]], color="k", lw=0.2, ls=(0, (10, 2, 2, 2)), zorder=2)
        d = np.array(arrow_dir, float)
        for q in (a, b):
            self.line(q, q - 5 * d, lw=0.5)
            self.arrow(q, q - 5 * d)
            self.text(*(q - 8 * d), letter, size=8, ha="center", weight="bold")

    def image(self, png, box):
        img = plt.imread(str(png))
        x0, y0, x1, y1 = box
        hh, ww = img.shape[0], img.shape[1]
        sc = min((x1 - x0) / ww, (y1 - y0) / hh)
        w, h = ww * sc, hh * sc
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        self.ax.imshow(img, extent=(cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2), zorder=0,
                       interpolation="antialiased")

    def save(self, stem):
        self.fig.canvas.draw()
        self.overlaps = self.check_overlaps(stem)
        pdf, png = OUT / f"{stem}.pdf", OUT / f"{stem}.png"
        self.fig.savefig(pdf)
        self.fig.savefig(png, dpi=110)
        plt.close(self.fig)
        return pdf, png


# ---- common text and helpers ---------------------------------------------------------------------------------------
PEEK = "Acetal copolymer (POM-C), natural, not homopolymer"   # plate and body; PEEK is the fallback (docs/34 §5.4)
PEEK_TB = PEEK
SS = "Stainless steel 316L"
REVS = [["A", DATE, "First issue", "generated"]]


def _iso_png(solid, mat, name):
    """Isometric render for reference, without the renderer's scale bar, trimmed to the part."""
    from PIL import Image
    path = OUT / f"_iso_{name}.png"
    C.render_png([(solid, mat)], path, view="iso", size=(4.0, 3.2), dpi=150, scale_bar=False)
    a = np.asarray(Image.open(path).convert("RGB")).copy()
    mask = (a < 245).any(axis=2)
    ys, xs = np.nonzero(mask)
    a = a[max(ys.min() - 6, 0): ys.max() + 6, max(xs.min() - 6, 0): xs.max() + 6]
    Image.fromarray(a).save(path)
    return path


def _mass(solid, rho):
    return _shape(solid).Volume() * rho


def marks(view, pts, r=1.5):
    for x, y in pts:
        view.centre_mark(x, y, 0, r=r)


K = 2.0                                           # scale of the main views
# view positions on each sheet (paper mm, origin bottom left): every callout is placed relative to its view
LAYOUT = {
    "base": dict(top=(195.0, 165.0)),
    "plate": dict(top=(80.0, 180.0), sec_y=95.0, det=(300.0, 180.0)),
    "body": dict(top=(82.0, 170.0), bot=(185.0, 170.0), sec_y=68.0, det=(332.0, 168.0)),
    "washer": dict(top=(188.0, 168.0)),
}


def dowel_callouts(S, top, flag):
    """Datum B (round hole) and C (slot), with their size."""
    xb, yb = P.DOWEL_XY[0]
    xc, yc = P.DOWEL_XY[1]
    pb, pc = top.p(xb, yb, 0), top.p(xc, yc, 0)
    rp = P.DOWEL_D / 2 * K
    # datum feature symbols of features of size sit on the leader of their size callout (ASME Y14.5)
    tb = (pb[0] + 40, pb[1] - 16)
    S.leader(pb + rp * np.array([0.71, -0.71]), tb, "⌀3.00 +0.05/+0.01 THRU", flag=flag)
    S.datum((tb[0] - 2.0, tb[1]), "B", direction=(0, -1), length=2.5)
    tc = (pc[0] + 40, pc[1] + 18)
    S.leader(pc + np.array([rp * 0.71, P.DOWEL_SLOT_L / 2 * K * 0.6]), tc, "SLOT WIDTH 3.00 +0.05/+0.01 THRU",
             flag=flag)
    S.datum((tc[0] - 2.0, tc[1]), "C", direction=(0, 1), length=2.5)


def flat_datum(S, tip, at, text, flag, tol, letter):
    """Callout of a datum face: leader with a dot, flatness frame under the text, datum symbol under the frame."""
    x0, _ = S.leader(tip, at, text, dot=True, flag=flag)
    S.frame(x0, at[1] - 6.5, "flat", [tol])
    S.datum((x0 + 3.0, at[1] - 8.7), letter, direction=(0, -1), length=2.5)


FLAG_NOTE = "Numbered triangles mark tolerances tighter than standard: inspect these features."
FIN = "Ra 1.6 µm (63 µin) all over"


# ---- T2C-001 base -------------------------------------------------------------------------------------------------
def sheet_base():
    solid = PT.base()
    notes = [f"MATERIAL: {SS}.", FLAG_NOTE]
    S = Sheet("T2C-001", "BASE", SS, FIN, "2:1", notes, [], REVS, _mass(solid, 8.0e-3))
    TV = LAYOUT["base"]["top"]
    top = View(S, "top", TV, K)
    top.draw(solid)
    marks(top, P.M4_XY + P.DOWEL_XY)
    m4 = top.p(8, 16, 0)
    S.leader(m4 + 2.15 * K * np.array([0.71, 0.71]), (m4[0] + 30, m4[1] + 22), "4× M4×0.7-6H THRU")
    dw = top.p(*P.DOWEL_XY[1], 0)
    S.leader(dw + 1.5 * K * np.array([-0.71, 0.71]), (dw[0] - 14, dw[1] + 22), "2× ⌀3.00 +0.05/+0.01",
             ha="right", flag=3)
    xr = top.p(P.X1, 0, 0)[0]
    flat_datum(S, top.p(-14.0, 9.0, 0), (xr + 26, TV[1] + 28), "TOP FACE", 1, "0.02", "A")
    S.callout(top.p(4.0, -3.5, 0), (xr + 26, TV[1] - 20), "STRIP POCKET FLOOR", flag=2, frame=("par", ["0.02", "A"]))
    S.text(TV[0], top.p(0, -P.Y_HALF, 0)[1] - 8, "TOP VIEW", size=FS_T, ha="center", weight="bold")
    return S.save("T2C-001_base")


# ---- T2C-002 nozzle plate -----------------------------------------------------------------------------------------
def sheet_plate():
    solid = PT.plate()
    rp = P.RET_POCKET_D
    zp = P.PLATE_T - P.RET_POCKET_DEPTH
    notes = [f"MATERIAL: {PEEK}.", FLAG_NOTE]
    S = Sheet("T2C-002", "NOZZLE PLATE", PEEK_TB, FIN, "2:1 (DETAIL 10:1)", notes, [], REVS,
              _mass(solid, 1.31e-3))
    L = LAYOUT["plate"]
    TV = L["top"]
    top = View(S, "top", TV, K)
    top.draw(solid)
    marks(top, P.M4_XY + P.DOWEL_XY + P.M25_XY)
    top.centre_mark(0, 0, 0, r=1.0)
    dowel_callouts(S, top, 5)
    S.cut_marks(top.p(P.X0 - 4, 0, 0), top.p(P.X1 + 4, 0, 0), "A", (0, 1))
    S.callout(top.p(5.0, -4.0, 0), (top.p(P.X1, 0, 0)[0] + 14, top.p(0, 0, 0)[1] - 22), "TOP FACE INSIDE ⌀16",
              flag=6, flat="0.02")
    m25 = top.p(8, 7, 0)
    tm = (top.p(P.X1, 0, 0)[0] + 14, m25[1] + 10)
    x0, _ = S.leader(m25 + P.M25_CLEAR / 2 * K * np.array([0.71, 0.71]), tm, f"4× ⌀{P.M25_CLEAR} THRU", flag=7)
    S.frame(x0, tm[1] - 6.0, "pos", ["⌀0.3", "A", "B", "C"])
    S.text(TV[0], top.p(0, -P.Y_HALF, 0)[1] - 8, "TOP VIEW", size=FS_T, ha="center", weight="bold")
    # section A-A, 2:1, projected under the top view; detail D of it at 10:1
    sec = View(S, "front", (TV[0], L["sec_y"]), K)
    sec.draw(solid, cut=("y", 0.0))
    sec.centre_line((0, 0, -0.8), (0, 0, P.PLATE_T + 0.8))
    S.detail_circle(sec.p(0, 0, P.PLATE_T / 2), 11.5, "D")
    S.text(TV[0] + 54, sec.p(0, 0, P.PLATE_T / 2)[1], "SECTION A–A", size=FS_T, ha="center", weight="bold")
    kd = 10.0
    det = View(S, "front", L["det"], kd)
    clip = cq.Workplane("XY").box(10.8, 60.0, 3.0, centered=False).translate((-5.4, -30, -0.2))
    det.draw(_shape(solid).intersect(_shape(clip)), cut=("y", 0.0))
    det.centre_line((0, 0, -0.7), (0, 0, P.PLATE_T + 0.7))
    S.text(det.o[0], det.o[1] - 47, "DETAIL D (SECTION A–A, 10:1)", size=FS_T, ha="center", weight="bold")
    # pocket: size, depth, position (frame attached under the dimension)
    q0, q1 = det.p(-rp / 2, 0, P.PLATE_T), det.p(rp / 2, 0, P.PLATE_T)
    lab = f"⌀{rp} +0.05/−0  ↧ {P.RET_POCKET_DEPTH:.2f} ±0.025"
    S.dim(q0, q1, q0[1] + 7, lab, outside_text="after")
    tx = q1[0] + 6.5
    S.frame(tx, q0[1] + 2.0, "pos", ["⌀0.10", "A", "B", "C"])
    S.flag(tx + S.width(lab, FS_S) + 4.0, q0[1] + 7, 2)
    # exit bore
    e1 = det.p(P.EXIT_D / 2, 0, 1.0)
    x0, x1 = S.leader(e1, (det.p(5.4, 0, 0)[0] + 8, e1[1] + 3), f"⌀{P.EXIT_D:.2f} ±0.05 THRU", flag=1)
    S.frame(x0, e1[1] - 3.5, "pos", ["⌀0.10", "A", "B", "C"])
    ept = det.p(-P.EXIT_D / 2, 0, zp)
    S.leader(ept + np.array([-0.2, 0.0]), (det.p(-5.4, 0, 0)[0] - 3, det.p(0, 0, P.PLATE_T)[1] + 9),
             "EDGE BREAK 0.05 MAX,\nboth ends", ha="right", flag=1)
    # grooves
    yb = det.p(0, 0, 0)[1]
    xf = det.p(P.GROOVE_STRIP_OD / 2, 0, 0)[0] + 6
    for r_, yy, lab_, fl_ in ((P.RING_R0, yb - 9, f"⌀{2 * P.RING_R0:.2f} ±0.10", 4),
                              (P.RING_R1, yb - 16, f"⌀{2 * P.RING_R1:.2f} ±0.10  ↧ {P.RING_DEPTH:.2f} ±0.10", 4),
                              (P.GROOVE_STRIP_ID / 2, yb - 23, f"⌀{P.GROOVE_STRIP_ID} ±0.05", 3),
                              (P.GROOVE_STRIP_OD / 2, yb - 30,
                               f"⌀{P.GROOVE_STRIP_OD} ±0.05  ↧ {P.GROOVE_STRIP_DEPTH:.2f} ±0.05", 3)):
        S.dim(det.p(-r_, 0, 0), det.p(r_, 0, 0), yy, lab_)
        S.flag(xf, yy, fl_)
    S.datum(det.p(-5.15, 0, 0), "A", direction=(0, -1), length=3.0)
    return S.save("T2C-002_nozzle_plate")


# ---- T2C-003 body ---------------------------------------------------------------------------------------------------
def sheet_body():
    solid = PT.body()
    zb = P.PLATE_T              # the body is modelled in assembly coordinates: its underside is at z = 2.5
    notes = [f"MATERIAL: {PEEK}.", FLAG_NOTE,
             "PORTS (2×): 1/4-28 UNF-2B, full thread ≥ 7.11 (0.28 in) from the face; flat bottom at 8.89\n"
             "(0.350 in), flat within 0.05 (0.002 in), Ra 0.8 µm (32 µin), corner radius ≤ 0.18 (0.007 in);\n"
             "chamfer ⌀6.86 (0.27 in) × 90°."]
    S = Sheet("T2C-003", "BODY", PEEK_TB, FIN, "2:1 (DETAIL 10:1)", notes, [], REVS, _mass(solid, 1.31e-3))
    L = LAYOUT["body"]
    TV, BV = L["top"], L["bot"]
    top = View(S, "top", TV, K)
    top.draw(solid)
    marks(top, P.M4_XY + P.DOWEL_XY)
    top.centre_mark(0, 0, 0, r=3.6)
    dowel_callouts(S, top, 6)
    pt = top.p(0, 0, 0)
    tp = (TV[0] - 59, top.p(0, P.Y_HALF, 0)[1] + 20)
    x0, x1 = S.leader(pt + P.PORT_CHAMFER_D / 2 * K * np.array([-0.71, 0.71]), tp, "1/4-28 UNF-2B PORT, NOTE 3",
                      flag=5)
    S.frame(x0, tp[1] - 6.0, "pos", ["⌀0.10", "A", "B", "C"])
    S.cut_marks(top.p(P.X0 - 4, 0, 0), top.p(P.X1 + 4, 0, 0), "A", (0, 1))
    S.text(TV[0], top.p(0, -P.Y_HALF, 0)[1] - 8, "TOP VIEW", size=FS_T, ha="center", weight="bold")
    # bottom view
    bot = View(S, "bottom", BV, K)
    bot.draw(solid)
    marks(bot, P.M4_XY + P.DOWEL_XY + P.M25_XY)
    bot.centre_mark(0, 0, 0, r=7.3)
    g = bot.p(P.GROOVE_IFACE_OD / 2 * 0.71, -P.GROOVE_IFACE_OD / 2 * 0.71, zb)
    S.leader(g, (bot.p(P.X1, 0, 0)[0] + 8, g[1] + 6),
             f"O-RING GROOVE ⌀{P.GROOVE_IFACE_ID} ±0.10 /\n⌀{P.GROOVE_IFACE_OD} ±0.10  ↧ {P.GROOVE_IFACE_DEPTH:.2f} ±0.05",
             flag=4)
    m25 = bot.p(8, 7, zb)
    tm = (bot.p(P.X1, 0, 0)[0] + 8, m25[1] - 24)
    x0, _ = S.leader(m25 + 1.35 * K * np.array([0.71, -0.71]), tm,
                     f"4× M2.5×0.45-6H ↧ {P.M25_FULL_THREAD:.1f} FULL THREAD", flag=7)
    S.frame(x0, tm[1] - 6.0, "pos", ["⌀0.3", "A", "B", "C"])
    flat_datum(S, bot.p(-5, -3, zb), (BV[0] + 10, BV[1] + 61), "UNDERSIDE INSIDE ⌀16", 2, "0.02", "A")
    S.text(BV[0], bot.p(0, P.Y_HALF, 0)[1] - 8, "BOTTOM VIEW", size=FS_T, ha="center", weight="bold")
    S.text(BV[0], bot.p(0, P.Y_HALF, 0)[1] - 13, "part turned over about the horizontal axis", size=FS_S,
           ha="center")
    # section A-A at 2:1
    front = View(S, "front", (TV[0], L["sec_y"] - zb * K), K)
    front.draw(solid, cut=("y", 0.0))
    th = P.PORT_MAJOR_D / 2
    for sg in (-1, 1):            # thread major diameter, thin lines over the full-thread length
        S.line(front.p(sg * th, 0, zb + P.BODY_T), front.p(sg * th, 0, zb + P.BODY_T - P.PORT_FULL_THREAD))
        S.line(front.p(P.X0, 0, zb + P.OUTLET_Z + sg * th), front.p(P.X0 + P.PORT_FULL_THREAD, 0,
                                                                    zb + P.OUTLET_Z + sg * th))
    op = front.p(P.X0, 0, zb + P.OUTLET_Z + th)
    S.leader(op + np.array([0.6, 0.6]), (TV[0] - 55, op[1] + 16), "1/4-28 UNF-2B PORT, NOTE 3", flag=5)
    S.detail_circle(front.p(0, 0, zb + 1.6), 7.5, "E")
    S.text(TV[0] + 54, front.p(0, 0, zb + 2.0)[1], "SECTION A–A", size=FS_T, ha="center", weight="bold")
    # detail E, 10:1
    kd = 10.0
    det = View(S, "front", (L["det"][0], L["det"][1] - zb * kd), kd)
    clip = cq.Workplane("XY").box(7.0, 60.0, 4.2, centered=False).translate((-3.5, -30, zb - 0.3))
    det.draw(_shape(solid).intersect(_shape(clip)), cut=("y", 0.0))
    det.centre_line((0, 0, zb - 0.7), (0, 0, zb + 4.4))
    S.text(det.o[0], L["det"][1] - 24, "DETAIL E (SECTION A–A, 10:1)", size=FS_T, ha="center", weight="bold")
    b1 = det.p(P.BED_D / 2, 0, zb + 1.3)
    x0, x1 = S.leader(b1, (det.p(3.5, 0, 0)[0] + 10, b1[1] + 2), f"⌀{P.BED_D:.2f} ±0.05 THRU", flag=1)
    S.frame(x0, b1[1] - 4.5, "pos", ["⌀0.10", "A", "B", "C"])
    ed = det.p(P.BED_D / 2, 0, zb)
    S.leader(ed + np.array([0.3, -0.1]), (ed[0] + 22, ed[1] - 8), "EDGE BREAK 0.05 MAX", flag=1)
    eu = det.p(P.BED_D / 2, 0, zb + P.INLET_FLOOR)
    S.leader(eu + np.array([0.3, 0.1]), (det.p(3.5, 0, 0)[0] + 8, eu[1] + 6), "EDGE BREAK 0.05 MAX", flag=1)
    S.finish(det.p(-1.2, 0, zb)[0] - 34, det.p(0, 0, zb)[1] - 12, "Ra 0.4", note="inside ⌀3",
             leader_to=det.p(-1.0, 0, zb) + np.array([0, -0.2]))
    S.flag(det.p(-1.2, 0, zb)[0] - 34 + 33, det.p(0, 0, zb)[1] - 12 + 5.6, 3)
    return S.save("T2C-003_body")


# ---- T2C-004 washer (cut gasket) ------------------------------------------------------------------------------------
FKM = "FKM (fluoroelastomer) sheet 0.25 mm, 70–75 Shore A"


def sheet_washer():
    solid = PT.washer_free()
    tD, tT = P.WASHER_D_TOL, P.WASHER_T_TOL
    notes = [f"MATERIAL: {FKM}.", FLAG_NOTE]
    flags = []
    general = ("Dimensions in mm.  Geometry per the STEP model and DXF files of the same drawing number and\n"
               "revision.  Do not scale the drawing.")
    S = Sheet("T2C-004", "WASHER (CUT GASKET)", "FKM sheet 0.25 mm, 70–75 Shore A", "As supplied", "20:1",
              notes, flags, REVS_WASHER, _mass(solid, 1.85e-3), general=general)
    k = 20.0
    top = View(S, "top", LAYOUT["washer"]["top"], k)
    top.draw(solid)
    top.centre_mark(0, 0, 0, r=P.WASHER_OD / 2, ext=3.0)
    ro, ri = P.WASHER_OD / 2 * k, P.WASHER_ID / 2 * k
    c = np.array(top.o)
    to = (c[0] + 34, c[1] + 26)
    S.leader(c + ro * np.array([0.71, 0.71]), to, f"⌀{P.WASHER_OD:.2f} ±{tD:.2f}", size=FS, flag=1)
    S.datum((to[0] - 2.0, to[1]), "B", direction=(0, 1), length=2.5)
    ti = (c[0] + 34, c[1] - 26)
    x0, x1 = S.leader(c + ri * np.array([0.71, -0.71]), ti, f"⌀{P.WASHER_ID:.2f} ±{tD:.2f} THRU", size=FS, flag=1)
    S.frame(x0, ti[1] - 6.0, "pos", ["⌀0.10", "B"])
    S.text(top.o[0], top.p(0, -P.WASHER_OD / 2, 0)[1] - 18, "TOP VIEW (20:1)", size=FS_T, ha="center",
           weight="bold")
    tt = (c[0] + 34, c[1])
    S.text(tt[0], tt[1], f"THICKNESS {P.WASHER_T:.2f} ±{tT:.2f}", size=FS)
    S.flag(tt[0] + S.width(f"THICKNESS {P.WASHER_T:.2f} ±{tT:.2f}", FS) + 3.5, tt[1], 2)
    return S.save("T2C-004_washer")


REVS_WASHER = REVS


def main():
    import shutil
    out = [sheet_base(), sheet_plate(), sheet_body(), sheet_washer()]
    # the STEP files a quote needs, named after their drawings (written by build.py from the same solids)
    for src, dst in (("base", "T2C-001_base"), ("nozzle_plate", "T2C-002_nozzle_plate"), ("body", "T2C-003_body"),
                     ("washer", "T2C-004_washer")):
        f = OUT.parent / f"{src}.step"
        if f.exists():
            shutil.copyfile(f, OUT / f"{dst}_rev{REV}.step")
    for src, dst in (("washer.dxf", "T2C-004_washer.dxf"), ("washer_sheet.dxf", "T2C-004_washer_sheet.dxf")):
        f = OUT.parent / src
        if f.exists():
            shutil.copyfile(f, OUT / dst)
    for f in Path(OUT).glob("_iso_*.png"):
        f.unlink()
    for pdf, png in out:
        print(pdf, png)


if __name__ == "__main__":
    main()
