"""CadQuery solids for the DOCK BASE items (layout.py) and tubes (fluidics.py)."""
from __future__ import annotations

import math

import cadquery as cq

from .. import common as C
from . import fluidics as F
from . import layout as L
from . import params as P


def _box(b):
    return C.box_from_corners(*b)


def _cyl(b, axis="z"):
    (x0, y0, z0), (x1, y1, z1) = b
    if axis == "z":
        r = min(x1 - x0, y1 - y0) / 2
        return cq.Workplane("XY").workplane(offset=z0).center((x0 + x1) / 2, (y0 + y1) / 2).circle(r).extrude(z1 - z0)
    r = min(x1 - x0, z1 - z0) / 2
    return (cq.Workplane("XZ").workplane(offset=-y1).center((x0 + x1) / 2, (z0 + z1) / 2).circle(r)
            .extrude(y1 - y0))


def _cut_boxes(solid, boxes):
    for b in boxes:
        solid = solid.cut(_box(b))
    return solid


def _hollow(b, t, open_top=False):
    (x0, y0, z0), (x1, y1, z1) = b
    inner = ((x0 + t, y0 + t, z0 + t), (x1 - t, y1 - t, z1 - (0 if open_top else t) + (1 if open_top else 0)))
    return _box(b).cut(_box(inner))


def _holes_z(solid, pts, d, z0, z1):
    for (x, y) in pts:
        solid = solid.cut(cq.Workplane("XY").workplane(offset=z0 - 1).center(x, y).circle(d / 2).extrude(z1 - z0 + 2))
    return solid


def custom(it):
    n, b = it.name, it.box
    (x0, y0, z0), (x1, y1, z1) = b
    if n == "base_plate":
        s = _holes_z(_box(b), P.FEET_XY, 10.5, z0, z1)
        (sx0, sy0), (sx1, sy1), sd = P.TRAY["sump"]
        return s.cut(_box(((sx0 - 1, sy0 - 1, z1 - sd - 1), (sx1 + 1, sy1 + 1, z1 + 1))))
    if n == "drip_tray":
        t, nt = 1.0, P.TRAY["notch"]
        s = _hollow(b, t, open_top=True)
        s = _cut_boxes(s, [((x0 - 1, y0 - 1, z0 - 1), (nt + 1, nt + 1, z1 + 1)),
                           ((P.FX - nt - 1, y0 - 1, z0 - 1), (x1 + 1, nt + 1, z1 + 1)),
                           ((x0 - 1, P.FY - nt - 1, z0 - 1), (nt + 1, y1 + 1, z1 + 1)),
                           ((P.FX - nt - 1, P.FY - nt - 1, z0 - 1), (x1 + 1, y1 + 1, z1 + 1))])
        (sx0, sy0), (sx1, sy1), sd = P.TRAY["sump"]
        sump = _hollow(((sx0, sy0, z0 - sd), (sx1, sy1, z0 + t)), t, open_top=True)
        s = s.cut(_box(((sx0 + t, sy0 + t, z0 - 0.5), (sx1 - t, sy1 - t, z0 + 1.5)))).union(sump)
        return s
    if n == "bay_deck":
        s = _holes_z(_box(b), P.DECK_BOLTS, 5.0, z0, z1)          # M6 tap drill
        s = _holes_z(s, [P.DECK_DOWELS["round"]], 6.0, z0, z1)
        sx, sy = P.DECK_DOWELS["slot"]
        s = s.cut(_box(((sx - 3, sy - 6, z0 - 1), (sx + 3, sy + 6, z1 + 1))))
        return s
    if n == "partition_left":
        g, c = P.GLAND_W, P.GLAND_C
        return _cut_boxes(_box(b), [((x0 - 1, g["y"][0], g["z"][0]), (x1 + 1, g["y"][1], g["z"][1])),
                                    ((x0 - 1, c["y"][0], c["z"][0]), (x1 + 1, c["y"][1], c["z"][1])),
                                    ((x0 - 1, 108.0, 154.0), (x1 + 1, 116.0, 166.0)),      # PEEK line
                                    ((x0 - 1, 199.0, 150.0), (x1 + 1, 207.0, 177.0)),      # west lane slot
                                    ((x0 - 1, 96.0, 18.0), (x1 + 1, 152.0, 32.0))])       # raceway (waste, purge)
    if n == "partition_right":
        g = P.GLAND_E
        bh = P.BULKHEAD
        return _cut_boxes(_box(b), [((x0 - 1, g["y"][0], g["z"][0]), (x1 + 1, g["y"][1], g["z"][1])),
                                    ((x0 - 1, bh[1] - 9, bh[2] - 11), (x1 + 1, bh[1] + 9, bh[2] + 11)),
                                    ((x0 - 1, 205.0, 150.0), (x1 + 1, 275.0, 178.0)),     # rear-low <-> bottles
                                    ((x0 - 1, 136.0, 18.0), (x1 + 1, 146.0, 32.0)),       # raceway
                                    ((x0 - 1, 300.0, 70.0), (x1 + 1, 314.0, 90.0))])      # R2 supply
    if n == "panel_left":
        cut = [((x0 - 1, 108.0, 158.0), (x1 + 1, 112.0, 162.0))]
        for k in range(6):   # louvres: cooler exhaust and electronics intake
            cut.append(((x0 - 1, 152.0 + 9 * k, 50.0), (x1 + 1, 157.0 + 9 * k, 115.0)))
            cut.append(((x0 - 1, 334.0 + 10 * k, 145.0), (x1 + 1, 340.0 + 10 * k, 295.0)))
        return _cut_boxes(_box(b), cut)
    if n == "panel_right":
        bh = P.BULKHEAD
        return _cut_boxes(_box(b), [((x0 - 1, bh[1] - 6, bh[2] - 6), (x1 + 1, bh[1] + 6, bh[2] + 6)),
                                    ((x0 - 1, 377.0, 42.0), (x1 + 1, 383.0, 48.0))])
    if n == "panel_front_left":
        (cx0, _, cz0), (cx1, _, cz1) = P.COLD_BOX["outer"]
        s = _cut_boxes(_box(b), [((cx0, y0 - 1, cz0), (cx1, y1 + 1, cz1))])
        return s.cut(cq.Workplane("XZ").workplane(offset=-y1 - 1).center(75.0, 285.0).circle(12.0).extrude(y1 - y0 + 2))
    if n == "panel_front_right":
        # bottle door outline as a 1 mm groove (door X 327-465, Z 20-255)
        s = _box(b)
        for (a0, a1) in [((327.0, y0 - 0.5, 20.0), (465.0, y0 + 1.0, 21.0)), ((327.0, y0 - 0.5, 254.0), (465.0, y0 + 1.0, 255.0)),
                         ((327.0, y0 - 0.5, 20.0), (328.0, y0 + 1.0, 255.0)), ((464.0, y0 - 0.5, 20.0), (465.0, y0 + 1.0, 255.0))]:
            s = s.cut(_box((a0, a1)))
        return s
    if n == "panel_rear":
        cut = [((30.0, y0 - 1, 50.0 + 25 * k), (130.0, y1 + 1, 62.0 + 25 * k)) for k in range(0)]
        for k in range(7):
            cut.append(((22.0 + 11 * k, y0 - 1, 140.0), (28.0 + 11 * k, y1 + 1, 220.0)))   # exhaust louvre
        for (a, c) in [((30.0, 50.0), (60.0, 75.0)), ((70.0, 55.0), (85.0, 65.0)), ((90.0, 55.0), (105.0, 65.0)),
                       ((110.0, 55.0), (125.0, 65.0)), ((70.0, 80.0), (86.0, 94.0)), ((95.0, 80.0), (105.0, 90.0))]:
            cut.append(((a[0], y0 - 1, a[1]), (c[0], y1 + 1, c[1])))                       # connector cut-outs
        s = _cut_boxes(_box(b), cut)
        for (a0, a1) in [((152.0, y1 - 1.0, 20.0), (463.0, y1 + 0.5, 21.0)), ((152.0, y1 - 1.0, 300.0), (463.0, y1 + 0.5, 301.0)),
                         ((152.0, y1 - 1.0, 20.0), (153.0, y1 + 0.5, 301.0)), ((462.0, y1 - 1.0, 20.0), (463.0, y1 + 0.5, 301.0))]:
            s = s.cut(_box((a0, a1)))                                                       # pump door outline
        return s
    if n == "panel_top_right":
        s = _box(b)
        for (a0, a1) in [((326.0, 200.0, z1 - 1.0), (465.0, 201.0, z1 + 0.5)), ((326.0, 316.0, z1 - 1.0), (465.0, 317.0, z1 + 0.5)),
                         ((326.0, 200.0, z1 - 1.0), (327.0, 317.0, z1 + 0.5)), ((464.0, 200.0, z1 - 1.0), (465.0, 317.0, z1 + 0.5))]:
            s = s.cut(_box((a0, a1)))
        return s
    if n == "cold_box":
        w = P.COLD_BOX["wall"]
        inner = L.COLD_INNER
        s = _box(b).cut(_box(inner))
        s = s.cut(_box(((x0 - 1, P.COLD_BOX["door_y"][1] - 0.5, z0 - 1), (x1 + 1, P.COLD_BOX["door_y"][1] + 0.5,
                                                                          z0 + 2))))   # door seam mark
        return s
    if n == "electronics_box":
        return _hollow(b, 1.0)
    return _box(b)


def solid(it):
    if it.shape == "custom":
        return custom(it)
    if it.shape == "cyl_z":
        return _cyl(it.box, "z")
    if it.shape == "cyl_y":
        return _cyl(it.box, "y")
    return _box(it.box)


def tube_solid(route, vis_scale=1.0):
    od = F.TUBES[route.tube][2] * vis_scale
    r = od / 2
    out = None
    pts = route.pts
    for i in range(len(pts) - 1):
        p, q = cq.Vector(*pts[i]), cq.Vector(*pts[i + 1])
        d = q - p
        Ln = d.Length
        if Ln < 1e-6:
            continue
        c = cq.Solid.makeCylinder(r, Ln, p, d.normalized())
        s = cq.Solid.makeSphere(r, p, angleDegrees1=-90, angleDegrees2=90) if i > 0 else None
        w = cq.Workplane().add(c)
        if s is not None:
            w = w.union(cq.Workplane().add(s))
        out = w if out is None else out.union(w)
    return out


def tube_color(route):
    n = route.name
    if "gas" in n or "air" in n or "purge" in n or "pilot" in n or "Flow EZ" in n:
        return (0.95, 0.85, 0.20, 1.0)
    if "waste" in n or n.startswith(("P_byp", "P_wo")):
        return (0.55, 0.35, 0.20, 1.0)
    if n.startswith("cell"):
        return (0.10, 0.10, 0.10, 1.0)
    if n.startswith(("P_in",)):
        return (0.85, 0.20, 0.60, 1.0)
    if n.startswith(("P_b", "vial", "S_b")):
        return (0.60, 0.20, 0.85, 1.0)
    if n.startswith(("P_cf", "P_rf")):
        return (0.10, 0.65, 0.65, 1.0)
    if n.startswith("A1"):
        return (0.30, 0.55, 0.95, 1.0)
    return (0.15, 0.40, 0.90, 1.0)


def claim_box(name):
    return _box(P.CL[name]["box"])


def lid_sweep_solid(step_deg=1.0):
    """Exact-enough swept volume of the closed UPPER claim box rotated about the hinge axis 0..85 deg: union of
    rotated YZ rectangles (shapely, 1-deg steps, hull of consecutive pairs) extruded over X 150-320 (Derived)."""
    from shapely.geometry import MultiPoint, Polygon
    from shapely.ops import unary_union
    (x0, y0, z0), (x1, y1, z1) = P.UPPER
    py, pz = P.HINGE["point"][1], P.HINGE["point"][2]
    n = int(P.HINGE["open_angle_deg"] / step_deg)

    def rect(a):
        a = math.radians(a)
        pts = []
        for (y, z) in ((y0, z0), (y1, z0), (y1, z1), (y0, z1)):
            dy, dz = y - py, z - pz
            pts.append((py + dy * math.cos(a) + dz * math.sin(a), pz - dy * math.sin(a) + dz * math.cos(a)))
        return pts
    polys = []
    for k in range(n):
        a0, a1 = k * step_deg, (k + 1) * step_deg
        polys.append(MultiPoint(rect(a0) + rect(a1)).convex_hull)
    reg = unary_union(polys)
    coords = list(reg.exterior.coords)[:-1]
    wp = cq.Workplane("YZ").workplane(offset=x0).polyline(coords).close().extrude(x1 - x0)
    return wp, reg
