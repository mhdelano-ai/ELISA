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
FS, FS_S, FS_T = 6.5, 5.6, 9.0           # font sizes (pt): dimensions, small text, titles
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
    half = _shape(solid).intersect(_shape(keeper))
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
            for loops in faces:
                verts, codes = [], []
                for lp in loops:
                    q = [self.pp(*t) for t in lp]
                    verts += q + [q[0]]
                    codes += [MPath.MOVETO] + [MPath.LINETO] * (len(q) - 1) + [MPath.CLOSEPOLY]
                ax.add_patch(PathPatch(MPath(verts, codes), facecolor="none", edgecolor="none", hatch="/////",
                                       lw=0, zorder=1))
        else:
            edges = project(solid, self.view, hidden)
        for pts, hid in edges:
            q = np.array([self.pp(*t) for t in pts])
            ax.plot(q[:, 0], q[:, 1], color="k", lw=LW_THIN if hid else LW_PART,
                    ls=(0, (3, 2)) if hid else "-", zorder=3, solid_capstyle="round")

    def title(self, text, dy=-7.0, x=None, y=None):
        self.s.text(x if x is not None else self.o[0], y if y is not None else self.o[1] + dy, text, size=FS_T,
                    ha="center", weight="bold")

    def centre_mark(self, x, y, z, r=1.5, ext=1.5):
        c = self.p(x, y, z)
        L = r * self.k + ext
        for dx, dy in ((1, 0), (0, 1)):
            self.s.ax.plot([c[0] - L * dx, c[0] + L * dx], [c[1] - L * dy, c[1] + L * dy], color="k", lw=0.15,
                           ls=(0, (8, 2, 1, 2)), zorder=2)

    def centre_line(self, a, b):
        a, b = self.p(*a), self.p(*b)
        self.s.ax.plot([a[0], b[0]], [a[1], b[1]], color="k", lw=0.15, ls=(0, (8, 2, 1, 2)), zorder=2)


class Sheet:
    def __init__(self, number, title, material, finish, scale, notes, flags, revs, mass_g):
        self.fig = plt.figure(figsize=(W / 25.4, H / 25.4))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, W)
        self.ax.set_ylim(0, H)
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.number, self.title_ = number, title
        self._frame()
        self._title_block(number, title, material, finish, scale, mass_g)
        self._notes(notes, flags)
        self._revisions(revs)

    # text and lines
    def text(self, x, y, s, size=FS, ha="left", va="center", rot=0, **kw):
        self.ax.text(x, y, s, fontsize=size, ha=ha, va=va, rotation=rot, zorder=6, **kw)

    def line(self, a, b, lw=LW_THIN, **kw):
        self.ax.plot([a[0], b[0]], [a[1], b[1]], color="k", lw=lw, zorder=4, **kw)

    def arrow(self, tip, tail):
        tip, tail = np.array(tip, float), np.array(tail, float)
        d = tip - tail
        n = np.linalg.norm(d)
        if n < 1e-9:
            return
        d /= n
        L, Wd = 2.2, 0.55
        b = tip - L * d
        nrm = np.array([-d[1], d[0]])
        self.ax.add_patch(Polygon([tip, b + Wd * nrm, b - Wd * nrm], closed=True, color="k", lw=0, zorder=5))

    # frame
    def _frame(self):
        ax = self.ax
        ax.add_patch(Rectangle((10, 10), W - 20, H - 20, fill=False, lw=0.8))
        for i in range(8):                      # zone marks
            x = 10 + (W - 20) * (i + 0.5) / 8
            self.text(x, 6, str(i + 1), size=FS_S, ha="center")
            self.text(x, H - 6, str(i + 1), size=FS_S, ha="center")
        for j, z in enumerate("DCBA"):
            y = 10 + (H - 20) * (j + 0.5) / 4
            self.text(6, y, z, size=FS_S, ha="center")
            self.text(W - 6, y, z, size=FS_S, ha="center")

    def _title_block(self, number, title, material, finish, scale, mass_g):
        x0, y0, w = W - 10 - 190, 10, 190
        rows = [  # (height, cells [(width, label, value, value size)])
            (9, [(190, "TITLE", f"{title}  —  tier-2 flow cell, ELISA project (docs/34)", 9.0)]),
            (8, [(60, "DRAWING NO.", number, 8.5), (25, "REV", REV, 8.5), (35, "SHEET", "1 OF 1", 7.5),
                 (35, "SIZE", "A3", 7.5), (35, "SCALE", scale, 7.5)]),
            (8, [(110, "MATERIAL", material, 6.4), (80, "FINISH", finish, 6.4)]),
            (8, [(60, "UNITS", "MILLIMETRES (mm)", 6.5), (45, "PROJECTION", "THIRD ANGLE", 6.5),
                 (40, "MASS (CALC.)", f"{mass_g:.0f} g", 6.5), (45, "DATE", DATE, 6.5)]),
            (8, [(95, "DRAWN", "generated: elisa_cad.tier2_cell.drawings", 5.8), (47.5, "CHECKED", "", 6),
                 (47.5, "APPROVED", "", 6)]),
            (17, [(190, "UNLESS OTHERWISE SPECIFIED",
                   "Dimensions in mm.  General tolerances per Xometry manufacturing standard (ISO 2768):\n"
                   "linear ±0.13 mm (±0.005 in) metals, ±0.25 mm (±0.010 in) plastics; angles ±1°;\n"
                   "form and orientation per that standard.  Surface finish Ra 3.2 µm (125 µin) as machined.\n"
                   "Break sharp edges 0.1–0.3 mm except where marked SHARP.  Do not scale the drawing.", 5.6)]),
        ]
        y = y0 + sum(r[0] for r in rows)
        top = y
        for hgt, cells in rows:
            y -= hgt
            x = x0
            for cw, lab, val, vs in cells:
                self.ax.add_patch(Rectangle((x, y), cw, hgt, fill=False, lw=0.5, zorder=4))
                self.text(x + 1.0, y + hgt - 1.6, lab, size=4.3, va="center", color="0.3")
                self.text(x + 1.5, y + (hgt - 2.6) / 2.0, val, size=vs, va="center")
                x += cw
        self._proj_symbol(x0 + 60 + 25 + 35 + 35 + 35 - 9, top - 9 - 4.0)
        self.tb_top = top

    def _proj_symbol(self, x, y):
        # third-angle symbol, drawn small inside the SCALE cell's right edge
        s = 0.55
        ax = self.ax
        ax.add_patch(Polygon([(x - 6 * s, y - 2 * s), (x - 6 * s, y + 2 * s), (x - 1 * s, y + 3.5 * s),
                              (x - 1 * s, y - 3.5 * s)], closed=True, fill=False, lw=0.4, zorder=5))
        ax.add_patch(Circle((x + 4 * s, y), 3.5 * s, fill=False, lw=0.4, zorder=5))
        ax.add_patch(Circle((x + 4 * s, y), 2 * s, fill=False, lw=0.4, zorder=5))

    def _notes(self, notes, flags):
        x, y = 15, H - 16
        self.text(x, y, "NOTES", size=7.5, weight="bold")
        y -= 4.2
        for i, n in enumerate(notes, 1):
            lines = n.split("\n")
            self.text(x, y, f"{i}.", size=FS_S)
            for ln in lines:
                self.text(x + 4, y, ln, size=FS_S)
                y -= 3.0
            y -= 0.5
        if flags:
            y -= 1.0
            self.text(x, y, "FLAGGED FEATURES — tolerances tighter than the Xometry standard (inspect)", size=6.2,
                      weight="bold")
            y -= 4.0
            for k, (num, txt) in enumerate(flags):
                self.flag(x + 2, y, num)
                for ln in txt.split("\n"):
                    self.text(x + 6, y, ln, size=FS_S)
                    y -= 3.0
                y -= 0.6
        self.notes_bottom = y

    def flag(self, x, y, num):
        self.ax.add_patch(Polygon([(x - 2.1, y - 1.6), (x + 2.1, y - 1.6), (x, y + 2.0)], closed=True, fill=False,
                                  lw=0.45, zorder=6))
        self.text(x, y - 0.35, str(num), size=4.6, ha="center")

    def _revisions(self, revs):
        x0, w = W - 10 - 150, 150
        y = H - 10
        cols = [(12, "REV"), (22, "DATE"), (92, "DESCRIPTION"), (24, "BY")]
        rows = [[c[1] for c in cols]] + revs
        for r in rows:
            y -= 5
            x = x0
            for (cw, _), val in zip(cols, r):
                self.ax.add_patch(Rectangle((x, y), cw, 5, fill=False, lw=0.4, zorder=4))
                self.text(x + 1, y + 2.5, val, size=5.2)
                x += cw

    # annotations
    def dim(self, a, b, at, text, axis="x", tol=None, text_side=1.0, inside=True, size=FS, shift=0.0):
        """Linear dimension between paper points a and b, measured along axis; dimension line at x or y = at."""
        a, b = np.array(a, float), np.array(b, float)
        if axis == "x":
            pa, pb = np.array([a[0], at]), np.array([b[0], at])
            for p, q in ((a, pa), (b, pb)):
                sgn = 1 if at > p[1] else -1
                self.line((p[0], p[1] + sgn * 0.8), (q[0], q[1] + sgn * 1.5))
        else:
            pa, pb = np.array([at, a[1]]), np.array([at, b[1]])
            for p, q in ((a, pa), (b, pb)):
                sgn = 1 if at > p[0] else -1
                self.line((p[0] + sgn * 0.8, p[1]), (q[0] + sgn * 1.5, q[1]))
        L = np.linalg.norm(pb - pa)
        u = (pb - pa) / max(L, 1e-9)
        if inside and L > 7:
            self.line(pa, pb)
            self.arrow(pa, pa + u)
            self.arrow(pb, pb - u)
        else:
            self.line(pa - 4 * u, pb + 4 * u)
            self.arrow(pa, pa - u)
            self.arrow(pb, pb + u)
        mid = (pa + pb) / 2 + u * shift
        label = text + (f" {tol}" if tol else "")
        if axis == "x":
            self.text(mid[0], mid[1] + 1.6 * text_side, label, size=size, ha="center",
                      va="bottom" if text_side > 0 else "top")
        else:
            self.text(mid[0] - 1.6 * text_side, mid[1], label, size=size, ha="center",
                      va="bottom" if text_side > 0 else "top", rot=90)

    def leader(self, tip, txt_xy, text, ha="left", size=FS, arrow=True, dot=False):
        tip, t = np.array(tip, float), np.array(txt_xy, float)
        land = t + np.array([-1.5 if ha == "left" else 1.5, 0])
        self.line(tip, land)
        self.line(land, t)
        if dot:
            self.ax.add_patch(Circle(tip, 0.45, color="k", zorder=5))
        elif arrow:
            self.arrow(tip, land)
        lines = text.split("\n")
        for i, ln in enumerate(lines):
            self.text(t[0] + (0.5 if ha == "left" else -0.5), t[1] - i * 2.9, ln, size=size, ha=ha)

    def flatness(self, x, y, tol, datum=None, leader_to=None):
        """Feature control frame for flatness (no datum) at (x, y) = left middle of the frame."""
        hgt = 4.2
        cells = [6.0, 9.0] + ([5.0] if datum else [])
        xx = x
        for cw in cells:
            self.ax.add_patch(Rectangle((xx, y - hgt / 2), cw, hgt, fill=False, lw=0.45, zorder=6))
            xx += cw
        # flatness symbol: parallelogram
        cx = x + 3.0
        self.ax.add_patch(Polygon([(cx - 2.0, y - 0.9), (cx + 1.0, y - 0.9), (cx + 2.0, y + 0.9), (cx - 1.0, y + 0.9)],
                                  closed=True, fill=False, lw=0.45, zorder=6))
        self.text(x + 6 + 4.5, y, tol, size=6.0, ha="center")
        if datum:
            self.text(x + 15 + 2.5, y, datum, size=6.0, ha="center")
        if leader_to is not None:
            a = np.array([x, y])
            self.line(a, leader_to)
            self.arrow(leader_to, a)

    def position(self, x, y, tol, datums, leader_to=None):
        hgt = 4.2
        cells = [6.0, 13.0] + [5.0] * len(datums)
        xx = x
        for cw in cells:
            self.ax.add_patch(Rectangle((xx, y - hgt / 2), cw, hgt, fill=False, lw=0.45, zorder=6))
            xx += cw
        cx = x + 3.0
        self.ax.add_patch(Circle((cx, y), 1.2, fill=False, lw=0.45, zorder=6))
        self.line((cx - 1.9, y), (cx + 1.9, y), lw=0.45)
        self.line((cx, y - 1.9), (cx, y + 1.9), lw=0.45)
        self.text(x + 6 + 6.5, y, tol, size=6.0, ha="center")
        xx = x + 19
        for d in datums:
            self.text(xx + 2.5, y, d, size=6.0, ha="center")
            xx += 5
        if leader_to is not None:
            a = np.array([x, y])
            self.line(a, leader_to)
            self.arrow(leader_to, a)

    def datum(self, tip, letter, direction=(0, -1), length=6.0):
        """Datum feature symbol: filled triangle on the feature at tip, line, square with the letter."""
        tip = np.array(tip, float)
        d = np.array(direction, float)
        d /= np.linalg.norm(d)
        n = np.array([-d[1], d[0]])
        tri = [tip, tip + 1.6 * d + 1.1 * n, tip + 1.6 * d - 1.1 * n]
        self.ax.add_patch(Polygon(tri, closed=True, color="k", lw=0, zorder=6))
        end = tip + length * d
        self.line(tip + 1.6 * d, end, lw=0.45)
        c = end + 2.3 * d
        self.ax.add_patch(Rectangle((c[0] - 2.3, c[1] - 2.3), 4.6, 4.6, fill=False, lw=0.45, zorder=6))
        self.text(c[0], c[1], letter, size=6.5, ha="center", weight="bold")

    def finish(self, x, y, ra, rot=0):
        """Surface texture symbol (material removal required) with Ra value; (x, y) = the point of the V."""
        pts = np.array([[-1.4, 1.4], [0, 0], [3.0, 3.6], [7.5, 3.6]])
        if rot:
            c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
            pts = pts @ np.array([[c, s], [-s, c]])
        pts = pts + [x, y]
        self.ax.plot(pts[:, 0], pts[:, 1], color="k", lw=0.45, zorder=6)
        self.line(pts[0], (x + 1.4 if not rot else pts[0][0], pts[0][1]), lw=0.45)
        self.text(pts[2][0] + 0.8, pts[2][1] + 1.6, ra, size=5.4)

    def image(self, png, box):
        img = plt.imread(str(png))
        x0, y0, x1, y1 = box
        hgt, wid = img.shape[0], img.shape[1]
        sc = min((x1 - x0) / wid, (y1 - y0) / hgt)
        w, h = wid * sc, hgt * sc
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        self.ax.imshow(img, extent=(cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2), zorder=0)

    def save(self, stem):
        pdf = OUT / f"{stem}.pdf"
        png = OUT / f"{stem}.png"
        self.fig.savefig(pdf)
        self.fig.savefig(png, dpi=110)
        plt.close(self.fig)
        return pdf, png


# ---- common text ---------------------------------------------------------------------------------------------------
PEEK = "PEEK, unfilled, natural (virgin, e.g. Victrex 450G based), annealed / stress-relieved stock"
SS = "Stainless steel 316L (ASTM A276 bar or A240 plate)"
REVS = [["A", DATE, "First issue (docs/34 Revision B, ceramic strip, IDEX-type 1/4-28 ports)", "generated"]]
COMMON = [
    "A STEP model of the same revision is supplied with this drawing. Where a feature is not dimensioned\n"
    "here, the model governs at the general tolerances; where it is dimensioned, this drawing governs.",
    "Liquid-path part for an analytical flow cell: no lubricant, coolant or marking residue on the part.\n"
    "Clean (detergent, then water and isopropanol), dry, bag individually. Do not engrave or stamp.",
    "Holes are drilled to the size shown; small bores (⌀0.5–1.0) must be open and free of burrs and chips.",
]


def _iso_png(solid, mat, name):
    path = OUT / f"_iso_{name}.png"
    C.render_png([(solid, mat)], path, view="iso", size=(4.0, 3.2), dpi=130)
    return path


def _mass(solid, rho):
    return _shape(solid).Volume() * rho


# ---- shared view helpers ----------------------------------------------------------------------------------------
PEEK_TB = "PEEK, unfilled, natural (annealed stock)"


def cut_marks_x(S, view, letter, x0=None, x1=None):
    """Section line along x at y = 0 on a top view; arrows point +y (the section is viewed from the front)."""
    ca, cb = view.p((P.X0 if x0 is None else x0) - 3, 0, 0), view.p((P.X1 if x1 is None else x1) + 3, 0, 0)
    S.ax.plot([ca[0], cb[0]], [ca[1], cb[1]], color="k", lw=0.2, ls=(0, (10, 2, 2, 2)), zorder=2)
    for q in (ca, cb):
        S.line(q, q + np.array([0, -5]), lw=0.5)
        S.arrow(q, q + np.array([0, -5]))
        S.text(q[0], q[1] - 8.0, letter, size=8, ha="center", weight="bold")


def top_ordinates(S, view, xs, ys, left=False):
    """Ordinate dimensions from the lower-left corner: x values along the top edge, y values on one side."""
    yt = view.p(0, P.Y_HALF, 0)[1] + 8
    for c, t in xs:
        foot = view.p(c, P.Y_HALF, 0)
        S.line((foot[0], foot[1] + 1.0), (foot[0], yt - 1))
        S.text(foot[0], yt, t, size=FS_S, ha="center", va="bottom", rot=90)
    if left:
        xl = view.p(P.X0, 0, 0)[0] - 8
        for c, t in ys:
            foot = view.p(P.X0, c, 0)
            S.line((foot[0] - 1.0, foot[1]), (xl + 1, foot[1]))
            S.text(xl, foot[1], t, size=FS_S, ha="right")
    else:
        xr = view.p(P.X1, 0, 0)[0] + 8
        for c, t in ys:
            foot = view.p(P.X1, c, 0)
            S.line((foot[0] + 1.0, foot[1]), (xr - 1, foot[1]))
            S.text(xr, foot[1], t, size=FS_S, ha="left")


def marks(view, pts, r=1.5):
    for x, y in pts:
        view.centre_mark(x, y, 0, r=r)


# ---- T2C-001 base -------------------------------------------------------------------------------------------------
def sheet_base():
    solid = PT.base()
    notes = [f"MATERIAL: {SS}."] + COMMON + [
        "Strip pocket depth is to general tolerance: it is measured at assembly and the shim under\n"
        "the electrode strip is chosen so that the gap over the electrode is 0.10 mm (docs/34 §4.3).",
        "Dowel holes take ⌀3 m6 × 16 stainless dowel pins, bonded with retaining compound at assembly\n"
        "(pins not supplied by the machinist).",
        "Pocket corners at the closed end may keep the radius of the cutter; the two relief holes let a\n"
        "square-ended strip reach the stop.",
    ]
    flags = [
        (1, "Top face (datum A): flat within 0.02 — the nozzle plate rests on it."),
        (2, "Pocket floor: flat within 0.02, Ra 1.6 µm (63 µin) — it carries the ceramic electrode strip."),
        (3, "Dowel holes ⌀3.00 +0.04/−0."),
    ]
    S = Sheet("T2C-001", "BASE", SS, "As machined, cleaned", "2:1 (DETAIL 10:1)", notes, flags, REVS,
              _mass(solid, 8.0e-3))
    k = 2.0
    top = View(S, "top", (75, 128), k)
    top.draw(solid)
    marks(top, P.M4_XY + P.DOWEL_XY)
    top.centre_mark(0, 0, 0, r=2.5)
    a, b = top.p(P.X0, -P.Y_HALF, 0), top.p(P.X1, -P.Y_HALF, 0)
    S.dim(a, b, a[1] - 8, "29")
    S.dim(a, top.p(P.X0, P.Y_HALF, 0), a[0] - 9, "44", axis="y")
    top_ordinates(S, top, [(P.X0, "0"), (-12, "5"), (P.POCKET_X_END, f"{P.POCKET_X_END - P.X0:.2f}"), (-2, "15"),
                           (0, "(17)"), (8, "25"), (P.X1, "29")],
                  [(-P.Y_HALF, "0"), (-16, "6"), (-P.POCKET_W / 2, f"{P.Y_HALF - P.POCKET_W / 2:.2f}"),
                   (0, "(22)"), (P.POCKET_W / 2, f"{P.Y_HALF + P.POCKET_W / 2:.2f}"), (16, "38"),
                   (P.Y_HALF, "44")])
    m4 = top.p(8, 16, 0)
    S.leader(m4 + np.array([1.2, 2.0]), (m4[0] + 26, m4[1] + 18), "4× M4×0.7-6H THRU", size=FS_S)
    dw = top.p(-2, -16, 0)
    S.leader(dw + np.array([1.3, -1.3]), (dw[0] + 12, dw[1] - 9), "2× ⌀3.00 +0.04/−0 ↧ 6", size=FS_S)
    S.flag(dw[0] + 9, dw[1] - 9, 3)
    rl = top.p(P.POCKET_X_END + 0.3, P.POCKET_W / 2 - 0.3, 0)
    S.leader(rl + np.array([-0.7, 0.7]), (rl[0] - 14, rl[1] + 14),
             f"2× ⌀{P.POCKET_RELIEF_D} ↧ {P.POCKET_DEPTH}", ha="right", size=FS_S)
    S.text(top.o[0], a[1] - 15, "TOP VIEW", size=FS_T, ha="center", weight="bold")
    cut_marks_x(S, top, "A")
    cc, cd = top.p(0, -P.Y_HALF - 3, 0), top.p(0, P.Y_HALF + 3, 0)
    S.ax.plot([cc[0], cd[0]], [cc[1], cd[1]], color="k", lw=0.2, ls=(0, (10, 2, 2, 2)), zorder=2)
    for q in (cc, cd):
        S.line(q, q + np.array([5, 0]), lw=0.5)
        S.arrow(q, q + np.array([5, 0]))
        S.text(q[0] + 8, q[1], "B", size=8, ha="center", weight="bold")
    # section A-A
    front = View(S, "front", (75, 45), k)
    front.draw(solid, cut=("y", 0.0))
    S.dim(front.p(P.X1, 0, -P.BASE_T), front.p(P.X1, 0, 0), front.p(P.X1, 0, 0)[0] + 8, f"{P.BASE_T:g}",
          axis="y", text_side=-1)
    tA = front.p(-15.5, 0, 0)
    S.datum(tA, "A", direction=(0, 1), length=4)
    S.flatness(tA[0] + 9, tA[1] + 8, "0.02", leader_to=front.p(-10, 0, 0) + np.array([0, 0.3]))
    S.flag(tA[0] + 27, tA[1] + 8, 1)
    S.text(front.o[0], 17, "SECTION A–A", size=FS_T, ha="center", weight="bold")
    # section B-B
    right = View(S, "right", (168, 45), k)
    right.draw(solid, cut=("x", 0.0))
    S.dim(right.p(0, -P.POCKET_W / 2, 0), right.p(0, P.POCKET_W / 2, 0), 54, f"{P.POCKET_W:.2f}")
    S.leader(right.p(0, 0, -P.POCKET_DEPTH / 2), (right.p(0, 0, 0)[0] + 2, 62),
             f"pocket ↧ {P.POCKET_DEPTH:.2f} (detail C)", size=FS_S)
    S.text(right.o[0], 17, "SECTION B–B", size=FS_T, ha="center", weight="bold")
    # detail C at 10:1
    kd = 10.0
    det = View(S, "right", (240, 160), kd)
    clip = cq.Workplane("XY").box(4, 4.0, 2.0, centered=False).translate((-2, 3.0, -1.6))
    det.draw(_shape(solid).intersect(_shape(clip)), cut=("x", 0.0))
    p0, p1 = det.p(0, 6.4, -P.POCKET_DEPTH), det.p(0, 6.4, 0)
    S.dim(det.p(0, 5.15, -P.POCKET_DEPTH), det.p(0, 5.15, 0), det.p(0, 7.0, 0)[0] + 5, f"{P.POCKET_DEPTH:.2f}",
          axis="y", text_side=-1, inside=False)
    fl = det.p(0, 3.9, -P.POCKET_DEPTH)
    S.flatness(fl[0] - 6, fl[1] - 14, "0.02", leader_to=fl + np.array([0, -0.3]))
    S.flag(fl[0] + 12, fl[1] - 14, 2)
    S.finish(det.p(0, 4.6, -P.POCKET_DEPTH)[0], det.p(0, 4.6, -P.POCKET_DEPTH)[1] + 0.3, "Ra 1.6")
    S.text(det.p(0, 3.6, 0)[0], det.p(0, 3.6, -P.POCKET_DEPTH)[1] + 3, "pocket floor", size=FS_S, ha="center")
    S.text(det.p(0, 5.0, 0)[0], 128, "DETAIL C (SECTION B–B, 10:1)", size=FS_T, ha="center", weight="bold")
    S.image(_iso_png(solid, "steel", "base"), (300, 190, 405, 268))
    S.text(352, 188, "ISOMETRIC (reference)", size=FS_S, ha="center")
    return S.save("T2C-001_base")


# ---- T2C-002 nozzle plate -----------------------------------------------------------------------------------------
def sheet_plate():
    solid = PT.plate()
    rp = P.RET_POCKET_D
    notes = [f"MATERIAL: {PEEK}.", "The plate is clamped flat in use; machine both faces with light cuts."] \
        + COMMON + [
        "Datum A is the underside (cell face). Datum B is the round dowel hole, datum C the slot.",
        "M2.5 flat-head screws enter from the underside; heads must sit 0–0.2 below the face.",
    ]
    flags = [
        (1, f"Exit bore ⌀{P.EXIT_D:.2f} ±0.05 and retainer pocket ⌀{rp} +0.05/−0: position ⌀0.10 to A|B|C;\n"
            "bore ends and pocket floor edge SHARP (deburr only, no chamfer)."),
        (2, f"Retainer pocket depth {P.RET_POCKET_DEPTH:.2f} ±0.025 (a sealing washer is compressed in it);\n"
            "floor Ra 1.6."),
        (3, "O-ring groove and collecting groove: as toleranced in detail D; groove floors Ra 1.6."),
        (4, "Underside inside ⌀9.3: Ra 1.6 µm (63 µin). Dowel hole and slot ⌀3.00 +0.04/−0."),
    ]
    S = Sheet("T2C-002", "NOZZLE PLATE", PEEK_TB, "As machined, cleaned", "2:1 (DETAIL 10:1)", notes, flags,
              REVS, _mass(solid, 1.31e-3))
    k = 2.0
    top = View(S, "top", (75, 128), k)
    top.draw(solid)
    marks(top, P.M4_XY + P.DOWEL_XY + P.M25_XY)
    top.centre_mark(0, 0, 0, r=1.5)
    top_ordinates(S, top, [(P.X0, "0"), (-12, "5"), (-2, "15"), (0, "17"), (8, "25"), (P.X1, "29")],
                  [(-P.Y_HALF, "0"), (-16, "6"), (-7, "15"), (0, "22"), (7, "29"), (16, "38"), (P.Y_HALF, "44")],
                  left=True)
    a, b = top.p(P.X0, -P.Y_HALF, 0), top.p(P.X1, -P.Y_HALF, 0)
    S.dim(a, b, a[1] - 8, "29")
    m4 = top.p(8, 16, 0)
    S.leader(m4 + np.array([1.6, 1.6]), (m4[0] + 8, m4[1] + 9), f"4× ⌀{P.M4_CLEAR} THRU", size=FS_S)
    m25 = top.p(8, 7, 0)
    S.leader(m25 + np.array([1.4, 0.4]), (m25[0] + 8, m25[1] + 3),
             f"4× ⌀{P.M25_CLEAR} THRU,\nCSK ⌀{P.M25_CSK_D} × 90°\nFROM UNDERSIDE", size=FS_S)
    dB = top.p(*P.DOWEL_XY[0], 0)
    S.leader(dB + np.array([1.2, -1.2]), (dB[0] + 12, dB[1] - 9), "⌀3.00 +0.04/−0 THRU", size=FS_S)
    S.datum(dB + np.array([-3.0, -0.5]), "B", direction=(-1, -1), length=3.5)
    dC = top.p(*P.DOWEL_XY[1], 0)
    S.leader(dC + np.array([1.0, 2.6]), (dC[0] + 10, dC[1] + 13),
             f"SLOT 3.00 +0.04/−0 × {P.DOWEL_SLOT_L} THRU", size=FS_S)
    S.datum(dC + np.array([-3.0, 0.5]), "C", direction=(-1, 1), length=3.5)
    S.flag(dB[0] + 40, dB[1] - 9, 4)
    ax_ = top.p(0, 0, 0)
    S.leader(ax_ + np.array([1.0, -1.0]), (ax_[0] + 32, ax_[1] - 12), "retainer pocket, exit bore,\nslot: detail D",
             size=FS_S)
    S.text(top.o[0], a[1] - 14, "TOP VIEW", size=FS_T, ha="center", weight="bold")
    cut_marks_x(S, top, "A")
    # section A-A at 2:1
    front = View(S, "front", (75, 40), k)
    front.draw(solid, cut=("y", 0.0))
    S.dim(front.p(P.X1, 0, 0), front.p(P.X1, 0, P.PLATE_T), front.p(P.X1, 0, 0)[0] + 7, f"{P.PLATE_T:g}",
          axis="y", text_side=-1, inside=False)
    S.datum(front.p(-14, 0, 0), "A", direction=(0, -1), length=3.5)
    S.text(front.o[0], 20, "SECTION A–A", size=FS_T, ha="center", weight="bold")
    # bottom view
    bot = View(S, "bottom", (185, 128), k)
    bot.draw(solid)
    marks(bot, P.M4_XY + P.DOWEL_XY + P.M25_XY)
    bot.centre_mark(0, 0, 0, r=4.8)
    g = bot.p(-P.GROOVE_STRIP_OD / 2 * 0.7071, P.GROOVE_STRIP_OD / 2 * 0.7071, 0)
    S.leader(g, (bot.p(P.X0, 0, 0)[0] - 4, 100), "O-ring groove and\ncollecting groove: detail D", ha="right",
             size=FS_S)
    csk = bot.p(-12, -7, 0)
    S.leader(csk + np.array([-1.8, 1.8]), (bot.p(P.X0, 0, 0)[0] - 4, 130), "4× CSK ⌀5.0 × 90°", ha="right",
             size=FS_S)
    S.finish(bot.p(0, 2.3, 0)[0] - 2, bot.p(0, 2.3, 0)[1] + 7, "Ra 1.6 inside ⌀9.3")
    S.flag(bot.p(0, 0, 0)[0] + 18, bot.p(0, 2.3, 0)[1] + 11, 4)
    S.datum(bot.p(6, -P.Y_HALF, 0), "A", direction=(0, 1), length=4)
    S.text(bot.o[0], bot.p(0, P.Y_HALF, 0)[1] - 8, "BOTTOM VIEW", size=FS_T, ha="center", weight="bold")
    S.text(bot.o[0], bot.p(0, P.Y_HALF, 0)[1] - 12.5, "(cell face = datum A)", size=FS_S, ha="center")
    # detail D: section A-A at 10:1
    kd = 10.0
    det = View(S, "front", (300, 150), kd)
    clip = cq.Workplane("XY").box(10.8, 4.0, 3.0, centered=False).translate((-5.4, -2, -0.2))
    det.draw(_shape(solid).intersect(_shape(clip)), cut=("y", 0.0))
    det.centre_line((0, 0, -0.6), (0, 0, P.PLATE_T + 0.9))
    zp = P.PLATE_T - P.RET_POCKET_DEPTH
    # above the part: pocket and slot
    q0, q1 = det.p(-rp / 2, 0, P.PLATE_T), det.p(rp / 2, 0, P.PLATE_T)
    S.dim(q0, q1, q0[1] + 9, f"⌀{rp} +0.05/−0  ↧ {P.RET_POCKET_DEPTH:.2f} ±0.025", size=FS_S)
    S.flag(q1[0] + 22, q0[1] + 11, 2)
    S.position(q1[0] + 4, q0[1] + 19, "⌀0.10", ["A", "B", "C"], leader_to=q1 + np.array([0.0, 0.4]))
    S.flag(q1[0] + 41, q0[1] + 19, 1)
    sl = det.p(-3.6, 0, P.PLATE_T - 0.15)
    S.leader(sl, (sl[0] - 12, sl[1] + 12),
             f"SLOT {P.CHANNEL_W} WIDE, R{P.CHANNEL_W / 2:g} ENDS, ↧ {P.CHANNEL_DEPTH},\n"
             f"from the riser to {abs(P.CHANNEL_X_END)} from the axis (along −X)", ha="right", size=FS_S)
    S.dim(det.p(P.CHANNEL_X_END, 0, P.PLATE_T), det.p(0, 0, P.PLATE_T), det.p(0, 0, P.PLATE_T)[1] + 26,
          f"{abs(P.CHANNEL_X_END)}", size=FS_S)
    # through bores
    e1 = det.p(P.EXIT_D / 2, 0, 1.6)
    S.leader(e1, (det.p(5.6, 0, 0)[0] + 2, e1[1] + 4), f"⌀{P.EXIT_D:.2f} ±0.05 THRU\n(exit bore)", size=FS_S)
    r0 = det.p(P.RISER_PLATE_X - P.RISER_PLATE_D / 2, 0, 1.2)
    S.leader(r0, (r0[0] - 20, r0[1] + 2), f"⌀{P.RISER_PLATE_D} THRU", ha="right", size=FS_S)
    S.dim(det.p(P.RISER_PLATE_X, 0, 0), det.p(0, 0, 0), det.p(0, 0, 0)[1] - 10, f"{abs(P.RISER_PLATE_X)} ±0.10",
          size=FS_S)
    # below the part: grooves
    S.dim(det.p(-P.RING_R0, 0, 0), det.p(P.RING_R0, 0, 0), det.p(0, 0, 0)[1] - 17, f"⌀{2 * P.RING_R0:.2f} ±0.10",
          size=FS_S, shift=12)
    S.dim(det.p(-P.RING_R1, 0, 0), det.p(P.RING_R1, 0, 0), det.p(0, 0, 0)[1] - 24, f"⌀{2 * P.RING_R1:.2f} ±0.10",
          size=FS_S, shift=12)
    S.dim(det.p(-P.GROOVE_STRIP_ID / 2, 0, 0), det.p(P.GROOVE_STRIP_ID / 2, 0, 0), det.p(0, 0, 0)[1] - 31,
          f"⌀{P.GROOVE_STRIP_ID} ±0.05", size=FS_S, shift=12)
    S.dim(det.p(-P.GROOVE_STRIP_OD / 2, 0, 0), det.p(P.GROOVE_STRIP_OD / 2, 0, 0), det.p(0, 0, 0)[1] - 38,
          f"⌀{P.GROOVE_STRIP_OD} ±0.05", size=FS_S, shift=12)
    S.dim(det.p(P.RING_R1, 0, 0), det.p(P.RING_R1, 0, P.RING_DEPTH), det.p(P.RING_R1, 0, 0)[0] + 5,
          f"{P.RING_DEPTH:.2f} ±0.10", axis="y", inside=False, size=FS_S, text_side=-1)
    S.dim(det.p(P.GROOVE_STRIP_OD / 2, 0, 0), det.p(P.GROOVE_STRIP_OD / 2, 0, P.GROOVE_STRIP_DEPTH),
          det.p(P.GROOVE_STRIP_OD / 2, 0, 0)[0] + 6, f"{P.GROOVE_STRIP_DEPTH:.2f} ±0.05", axis="y", inside=False,
          size=FS_S, text_side=-1)
    S.flag(det.p(P.GROOVE_STRIP_OD / 2, 0, 0)[0] + 12, det.p(0, 0, 0)[1] - 31, 3)
    S.finish(det.p(-4.05, 0, P.GROOVE_STRIP_DEPTH)[0], det.p(-4.05, 0, P.GROOVE_STRIP_DEPTH)[1], "Ra 1.6", rot=180)
    S.text(det.o[0], 95, "DETAIL D: SECTION A–A AT THE AXIS, 10:1 (cell face down)", size=FS_T, ha="center",
           weight="bold")
    S.image(_iso_png(solid, "PEEK", "plate"), (240, 216, 320, 268))
    S.image(_iso_png(solid.rotate((0, 0, 0), (1, 0, 0), 180), "PEEK", "plate_under"), (325, 216, 405, 268))
    S.text(322, 213, "ISOMETRIC, top face and underside (reference)", size=FS_S, ha="center")
    return S.save("T2C-002_nozzle_plate")


# ---- T2C-003 body ---------------------------------------------------------------------------------------------------
def sheet_body():
    solid = PT.body()
    zb = P.PLATE_T              # the body is modelled in assembly coordinates: its underside is at z = 2.5
    notes = [f"MATERIAL: {PEEK}."] + COMMON + [
        "Datum A is the underside. Datum B is the round dowel hole, datum C the slot.",
        "PORTS (2×: inlet on the top face, outlet on the end face, both on section plane A–A), to the\n"
        "1/4-28 flat-bottom port drawing supplied with the order: 1/4-28 UNF-2B, full thread ≥ 7.11 (0.28 in)\n"
        "from the face; flat bottom at 8.89 (0.350 in), flat within 0.05 (0.002 in), Ra 0.8 µm (32 µin),\n"
        "corner radius ≤ 0.18 (0.007 in); chamfer ⌀6.86 (0.27 in) × 90°. The bottom seals the fitting.",
        "Drill the bed bore from the inlet port bottom in the same set-up as the inlet port.",
    ]
    flags = [
        (1, f"Bed bore ⌀{P.BED_D:.2f} ±0.05 through the port floor: position ⌀0.10 to A|B|C; edge at the\n"
            "underside SHARP (deburr only, no chamfer)."),
        (2, "Underside (datum A): flat within 0.05; Ra 1.6 µm (63 µin) inside ⌀16 (a membrane and an\n"
            "O-ring seal on it)."),
        (3, f"O-ring groove ⌀{P.GROOVE_IFACE_ID} / ⌀{P.GROOVE_IFACE_OD} ±0.10, ↧ {P.GROOVE_IFACE_DEPTH} ±0.05, floor Ra 1.6."),
        (4, "Port bottoms flat within 0.05, Ra 0.8 (note 7). Dowel hole and slot ⌀3.00 +0.04/−0."),
    ]
    S = Sheet("T2C-003", "BODY", PEEK_TB, "As machined, cleaned", "2:1 (DETAIL 10:1)", notes, flags, REVS,
              _mass(solid, 1.31e-3))
    k = 2.0
    top = View(S, "top", (75, 128), k)
    top.draw(solid)
    marks(top, P.M4_XY + P.DOWEL_XY)
    top.centre_mark(0, 0, 0, r=3.5)
    top_ordinates(S, top, [(P.X0, "0"), (-12, "5"), (-2, "15"), (0, "17"), (8, "25"), (P.X1, "29")],
                  [(-P.Y_HALF, "0"), (-16, "6"), (0, "22"), (16, "38"), (P.Y_HALF, "44")], left=True)
    a, b = top.p(P.X0, -P.Y_HALF, 0), top.p(P.X1, -P.Y_HALF, 0)
    S.dim(a, b, a[1] - 8, "29")
    port = top.p(0, 0, 0)
    S.leader(port + np.array([2.6, -2.6]), (port[0] + 36, port[1] - 14), "1/4-28 UNF-2B PORT,\nNOTE 7 (inlet)",
             size=FS_S)
    S.flag(port[0] + 33, port[1] - 14, 4)
    m4 = top.p(8, 16, 0)
    S.leader(m4 + np.array([1.6, 1.6]), (m4[0] + 8, m4[1] + 9), f"4× ⌀{P.M4_CLEAR} THRU", size=FS_S)
    dB = top.p(*P.DOWEL_XY[0], 0)
    S.leader(dB + np.array([1.2, -1.2]), (dB[0] + 12, dB[1] - 9), "⌀3.00 +0.04/−0 THRU", size=FS_S)
    S.datum(dB + np.array([-3.0, -0.5]), "B", direction=(-1, -1), length=3.5)
    dC = top.p(*P.DOWEL_XY[1], 0)
    S.leader(dC + np.array([1.0, 2.6]), (dC[0] + 10, dC[1] + 13),
             f"SLOT 3.00 +0.04/−0 × {P.DOWEL_SLOT_L} THRU", size=FS_S)
    S.datum(dC + np.array([-3.0, 0.5]), "C", direction=(-1, 1), length=3.5)
    S.text(top.o[0], a[1] - 14, "TOP VIEW", size=FS_T, ha="center", weight="bold")
    cut_marks_x(S, top, "A")
    # section A-A
    front = View(S, "front", (75, 22 - zb * k), k)
    front.draw(solid, cut=("y", 0.0))
    fa, fb = front.p(P.X1, 0, zb), front.p(P.X1, 0, zb + P.BODY_T)
    S.dim(fa, fb, fa[0] + 13, f"{P.BODY_T:g}", axis="y", text_side=-1)
    tap = P.PORT_TAP_DRILL / 2
    S.dim(front.p(tap, 0, zb + P.INLET_FLOOR), front.p(tap, 0, zb + P.BODY_T), fa[0] + 5, f"{P.PORT_DEPTH}",
          axis="y", text_side=-1)
    S.dim(front.p(-tap, 0, zb), front.p(-tap, 0, zb + P.INLET_FLOOR), front.p(-tap, 0, zb)[0] - 2,
          f"({P.INLET_FLOOR:.1f})", axis="y", inside=False, size=FS_S)
    oz = front.p(P.X0, 0, zb + P.OUTLET_Z)
    S.dim(front.p(P.X0, 0, zb), oz, oz[0] - 7, f"{P.OUTLET_Z:g}", axis="y")
    S.dim(oz, front.p(P.X0 + P.PORT_DEPTH, 0, zb + P.OUTLET_Z), front.p(0, 0, zb + P.BODY_T)[1] + 6,
          f"{P.PORT_DEPTH}")
    th = front.p(-6.0, 0, zb + P.OUTLET_Z + 0.4)
    S.leader(th, (th[0] + 30, front.p(0, 0, zb + P.BODY_T)[1] + 12), f"⌀{P.OUTLET_THROUGH_D} (outlet port to riser)",
             size=FS_S)
    rs = front.p(P.RISER_BODY_X + 0.5, 0, zb + 3.0)
    S.leader(rs, (rs[0] + 6, front.p(0, 0, zb)[1] - 6), f"⌀{P.RISER_BODY_D} ↧ {P.OUTLET_Z + P.OUTLET_THROUGH_D / 2:g},"
             f" at {abs(P.RISER_BODY_X)} from the axis", size=FS_S)
    S.text(front.o[0] + 52, front.p(0, 0, zb + 1.5)[1], "outlet port\non plane A–A,\n22 from the\nside edge",
           size=FS_S)
    S.datum(front.p(-14, 0, zb), "A", direction=(0, -1), length=3.5)
    S.text(front.o[0] + 82, 18, "SECTION A–A", size=FS_T, ha="center", weight="bold")
    # bottom view
    bot = View(S, "bottom", (185, 128), k)
    bot.draw(solid)
    marks(bot, P.M4_XY + P.DOWEL_XY + P.M25_XY)
    bot.centre_mark(0, 0, 0, r=7.2)
    g = bot.p(P.GROOVE_IFACE_OD / 2 * 0.7071, -P.GROOVE_IFACE_OD / 2 * 0.7071, zb)
    S.leader(g, (g[0] + 18, g[1] - 22),
             f"O-RING GROOVE ⌀{P.GROOVE_IFACE_ID} / ⌀{P.GROOVE_IFACE_OD} ±0.10\n↧ {P.GROOVE_IFACE_DEPTH} ±0.05",
             size=FS_S)
    S.flag(g[0] + 16, g[1] - 22, 3)
    m25 = bot.p(8, -7, zb)
    S.leader(m25 + np.array([1.2, -1.0]), (m25[0] + 12, m25[1] + 4),
             f"4× M2.5×0.45-6H ↧ 5.5 FULL THREAD\n(drill ⌀{P.M25_TAP_DRILL} ↧ {P.M25_THREAD_DEPTH:g})", size=FS_S)
    rs = bot.p(P.RISER_BODY_X, 0, zb)
    S.leader(rs + np.array([-0.8, -0.8]), (bot.p(P.X0, 0, 0)[0] - 4, 104), "riser (section A–A)", ha="right",
             size=FS_S)
    bb = bot.p(0, 0, zb)
    S.leader(bb + np.array([0.4, 0.4]), (bb[0] + 24, bb[1] + 46), f"⌀{P.BED_D:.2f} ±0.05 THRU (bed bore)",
             size=FS_S)
    S.position(bb[0] + 24, bb[1] + 40, "⌀0.10", ["A", "B", "C"])
    S.flag(bb[0] + 21, bb[1] + 46, 1)
    S.finish(bot.p(-6, 5, zb)[0], bot.p(-6, 5, zb)[1], "Ra 1.6 inside ⌀16")
    fl = bot.p(P.X1 - 2, P.Y_HALF - 3, zb)
    S.flatness(fl[0] + 6, fl[1] + 12, "0.05", leader_to=fl)
    S.flag(fl[0] + 24, fl[1] + 12, 2)
    S.datum(bot.p(6, -P.Y_HALF, zb), "A", direction=(0, 1), length=4)
    S.text(bot.o[0], bot.p(0, P.Y_HALF, 0)[1] - 8, "BOTTOM VIEW", size=FS_T, ha="center", weight="bold")
    # detail E: 10:1
    kd = 10.0
    det = View(S, "front", (300, 112 - zb * kd), kd)
    clip = cq.Workplane("XY").box(7.0, 4.0, 4.2, centered=False).translate((-3.5, -2, zb - 0.3))
    det.draw(_shape(solid).intersect(_shape(clip)), cut=("y", 0.0))
    det.centre_line((0, 0, zb - 0.6), (0, 0, zb + 4.3))
    b1 = det.p(P.BED_D / 2, 0, zb + 1.2)
    bt = (det.p(3.5, 0, 0)[0] + 22, b1[1] - 8)
    S.leader(b1, bt, f"⌀{P.BED_D:.2f} ±0.05 THRU", size=FS_S)
    S.flag(bt[0] - 3, bt[1], 1)
    fbt = det.p(-1.6, 0, zb + P.INLET_FLOOR)
    S.flatness(fbt[0] - 6, det.p(0, 0, zb + 4.2)[1] + 8, "0.05", leader_to=fbt + np.array([0, 0.3]))
    S.flag(fbt[0] - 10, det.p(0, 0, zb + 4.2)[1] + 8, 4)
    S.finish(det.p(1.2, 0, zb + P.INLET_FLOOR)[0], det.p(1.2, 0, zb + P.INLET_FLOOR)[1] + 0.3, "Ra 0.8")
    cr = det.p(P.PORT_TAP_DRILL / 2, 0, zb + P.INLET_FLOOR)
    S.leader(cr + np.array([-0.3, 0.3]), (cr[0] + 10, cr[1] + 14), f"R{P.PORT_CORNER_R} MAX", size=FS_S)
    ed = det.p(-P.BED_D / 2, 0, zb)
    S.leader(ed + np.array([-0.3, 0.0]), (ed[0] - 22, ed[1] - 12), "SHARP (deburr only)", ha="right", size=FS_S)
    S.dim(det.p(3.0, 0, zb), det.p(3.0, 0, zb + P.INLET_FLOOR), det.p(3.4, 0, zb)[0] + 10,
          f"({P.INLET_FLOOR:.1f})", axis="y", text_side=-1, size=FS_S)
    S.datum(det.p(2.4, 0, zb), "A", direction=(0, -1), length=3.5)
    S.text(det.o[0], 78, "DETAIL E: PORT BOTTOM AND BED BORE (SECTION A–A, 10:1)", size=FS_T, ha="center",
           weight="bold")
    S.image(_iso_png(solid, "PEEK", "body"), (300, 175, 405, 262))
    S.text(352, 173, "ISOMETRIC (reference)", size=FS_S, ha="center")
    return S.save("T2C-003_body")


def main():
    out = [sheet_base(), sheet_plate(), sheet_body()]
    for f in Path(OUT).glob("_iso_*.png"):
        f.unlink()
    for pdf, png in out:
        print(pdf, png)


if __name__ == "__main__":
    main()
