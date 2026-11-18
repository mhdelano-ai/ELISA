"""Solids of the tier-2 flow cell (docs/34).  Every number comes from params.py.

Custom parts: base(), plate(), body().  Purchased parts and the liquid are modelled for the assembly, the
renders and the checks only.  Threads are modelled as their tap-drill holes; the thread call-outs are in docs/34
section 5.2 and in out/tier2_cell/drawing_notes.md.
"""
from __future__ import annotations

import cadquery as cq

from . import params as P

LX, LY = P.X1 - P.X0, 2.0 * P.Y_HALF
Z_PLATE, Z_BODY, Z_TOP = 0.0, P.PLATE_T, P.PLATE_T + P.BODY_T


def _block(z0, t):
    b = cq.Workplane("XY").box(LX, LY, t, centered=False).translate((P.X0, -P.Y_HALF, z0))
    return b.edges("|Z").chamfer(P.EDGE_CHAMFER)


def _cyl(d, h, x=0.0, y=0.0, z0=0.0):
    return cq.Workplane("XY").circle(d / 2.0).extrude(h).translate((x, y, z0))


def _ring(d_in, d_out, h, z0=0.0):
    return cq.Workplane("XY").circle(d_out / 2.0).circle(d_in / 2.0).extrude(h).translate((0, 0, z0))


def _xcyl(d, x_from, x_to, y, z):
    """Cylinder along x."""
    return cq.Workplane("YZ").circle(d / 2.0).extrude(x_to - x_from).translate((x_from, y, z))


def _dowel_holes(z0, t):
    """Round hole for the first pin (datum B), slot along y for the second (datum C)."""
    (xb, yb), (xc, yc) = P.DOWEL_XY
    slot = cq.Workplane("XY").slot2D(P.DOWEL_SLOT_L, P.DOWEL_D, angle=90).extrude(t).translate((xc, yc, z0))
    return [_cyl(P.DOWEL_D, t, xb, yb, z0), slot]


def _cut_all(body, tools):
    for t in tools:
        body = body.cut(t)
    return body


# ---- custom parts ---------------------------------------------------------------------------------------------
def base():
    """316L.  Strip pocket open at +x, closed end = stop for the strip; four M4 threads; two dowel holes."""
    b = _block(-P.BASE_T, P.BASE_T)
    x0 = P.POCKET_X_END
    pocket = cq.Workplane("XY").box(P.X1 - x0 + 1.0, P.POCKET_W, P.POCKET_DEPTH, centered=False) \
        .translate((x0, -P.POCKET_W / 2.0, -P.POCKET_DEPTH))
    tools = [pocket]
    for s in (-1, 1):                                   # corner reliefs so that a square strip end seats
        tools.append(_cyl(P.POCKET_RELIEF_D, P.POCKET_DEPTH, x0 + 0.3, s * (P.POCKET_W / 2.0 - 0.3),
                          -P.POCKET_DEPTH))
    tools += [_cyl(P.M4_TAP_DRILL, P.BASE_T, x, y, -P.BASE_T) for x, y in P.M4_XY]          # M4 x 0.7 through
    tools += [_cyl(P.DOWEL_D, 6.0, x, y, -6.0) for x, y in P.DOWEL_XY]                      # 3 mm, press fit
    return _cut_all(b, tools)


def plate():
    """PEEK nozzle plate.  Underside (z = 0) is the cell face; top face carries the retainer and the cross channel."""
    b = _block(Z_PLATE, P.PLATE_T)
    tools = [
        _cyl(P.EXIT_D, P.PLATE_T),                                                            # exit bore
        _cyl(P.RET_POCKET_D, P.RET_POCKET_DEPTH, 0, 0, P.PLATE_T - P.RET_POCKET_DEPTH),       # retainer pocket
        _ring(P.GROOVE_STRIP_ID, P.GROOVE_STRIP_OD, P.GROOVE_STRIP_DEPTH),                    # O-ring on the strip
        _ring(2 * P.RING_R0, 2 * P.RING_R1, P.RING_DEPTH),                                    # collecting groove
        _cyl(P.RISER_PLATE_D, P.PLATE_T, P.RISER_PLATE_X),                                    # riser
    ]
    ch_len = P.RISER_PLATE_X - P.CHANNEL_X_END
    slot = cq.Workplane("XY").slot2D(ch_len + P.CHANNEL_W, P.CHANNEL_W).extrude(P.CHANNEL_DEPTH) \
        .translate(((P.RISER_PLATE_X + P.CHANNEL_X_END) / 2.0, 0, P.PLATE_T - P.CHANNEL_DEPTH))
    tools.append(slot)
    tools += [_cyl(P.M4_CLEAR, P.PLATE_T, x, y) for x, y in P.M4_XY]
    tools += _dowel_holes(0.0, P.PLATE_T)
    for x, y in P.M25_XY:                                                                     # M2.5 flat heads
        tools.append(_cyl(P.M25_CLEAR, P.PLATE_T, x, y))
        h = (P.M25_CSK_D - P.M25_CLEAR) / 2.0                                                 # 90 degree countersink
        cone = cq.Solid.makeCone(P.M25_CSK_D / 2.0, P.M25_CLEAR / 2.0, h, cq.Vector(x, y, 0), cq.Vector(0, 0, 1))
        tools.append(cq.Workplane("XY").add(cone))
    return _cut_all(b, tools)


def body():
    """PEEK body.  Inlet port on top; its floor carries the bed bore; outlet port on the -x face."""
    b = _block(Z_BODY, P.BODY_T)
    zo = Z_BODY + P.OUTLET_Z
    x_port_end = P.X0 + P.PORT_DEPTH
    tools = [
        _cyl(P.PORT_TAP_DRILL, P.PORT_DEPTH, 0, 0, Z_TOP - P.PORT_DEPTH),                     # inlet port 1/4-28
        cq.Workplane("XY").add(cq.Solid.makeCone(P.PORT_TAP_DRILL / 2.0, P.PORT_CHAMFER_D / 2.0,
                                                 (P.PORT_CHAMFER_D - P.PORT_TAP_DRILL) / 2.0,
                                                 cq.Vector(0, 0, Z_TOP - (P.PORT_CHAMFER_D - P.PORT_TAP_DRILL) / 2.0),
                                                 cq.Vector(0, 0, 1))),                       # 90 deg chamfer
        _cyl(P.BED_D, P.INLET_FLOOR, 0, 0, Z_BODY),                                           # bed bore
        _ring(P.GROOVE_IFACE_ID, P.GROOVE_IFACE_OD, P.GROOVE_IFACE_DEPTH, Z_BODY),            # O-ring to the plate
        _cyl(P.RISER_BODY_D, P.OUTLET_Z + P.OUTLET_THROUGH_D / 2.0, P.RISER_BODY_X, 0, Z_BODY),   # riser
        _xcyl(P.PORT_TAP_DRILL, P.X0, x_port_end, 0, zo),                                     # outlet port 1/4-28
        cq.Workplane("XY").add(cq.Solid.makeCone(P.PORT_CHAMFER_D / 2.0, P.PORT_TAP_DRILL / 2.0,
                                                 (P.PORT_CHAMFER_D - P.PORT_TAP_DRILL) / 2.0,
                                                 cq.Vector(P.X0, 0, zo), cq.Vector(1, 0, 0))),
        _xcyl(P.OUTLET_THROUGH_D, x_port_end, P.RISER_BODY_X, 0, zo),                         # to the riser
    ]
    tools += [_cyl(P.M4_CLEAR, P.BODY_T, x, y, Z_BODY) for x, y in P.M4_XY]
    tools += _dowel_holes(Z_BODY, P.BODY_T)
    tools += [_cyl(P.M25_TAP_DRILL, P.M25_THREAD_DEPTH, x, y, Z_BODY) for x, y in P.M25_XY]  # M2.5 x 0.45
    return _cut_all(b, tools)


# ---- purchased parts (for the assembly and the checks) ---------------------------------------------------------
Z_STRIP0 = -P.POCKET_DEPTH + P.SHIM_T            # underside of the strip
Z_STRIP1 = Z_STRIP0 + P.STRIP_T                  # electrode face = -GAP


def strip():
    x0 = -P.WE_FROM_FREE_END
    return cq.Workplane("XY").box(P.STRIP_L, P.STRIP_W, P.STRIP_T, centered=False) \
        .translate((x0, -P.STRIP_W / 2.0, Z_STRIP0))


def working_electrode():
    return _cyl(P.WE_D, 0.01, 0, 0, Z_STRIP1)


def shim():
    x0 = -P.WE_FROM_FREE_END
    return cq.Workplane("XY").box(P.X1 - x0, P.STRIP_W, P.SHIM_T, centered=False) \
        .translate((x0, -P.STRIP_W / 2.0, -P.POCKET_DEPTH))


def _oring(size, z_mid):
    d_i, cs = size
    t = cq.Solid.makeTorus((d_i + cs) / 2.0, cs / 2.0 * 0.72, cq.Vector(0, 0, z_mid), cq.Vector(0, 0, 1))
    return cq.Workplane("XY").add(t)             # drawn at 72 % of its cord: the compressed height


def oring_strip():
    return _oring(P.ORING_STRIP, (Z_STRIP1 + P.GROOVE_STRIP_DEPTH) / 2.0)


def oring_iface():
    return _oring(P.ORING_IFACE, Z_BODY + P.GROOVE_IFACE_DEPTH / 2.0)


Z_POCKET = P.PLATE_T - P.RET_POCKET_DEPTH        # floor of the retainer pocket


def washer_free():
    """The washer as cut (free thickness), at the origin: the part of drawing T2C-004."""
    return _ring(P.WASHER_ID, P.WASHER_OD, P.WASHER_T, 0.0)


def washer():
    """Elastomer washer, drawn at its compressed height (its bulge is not drawn)."""
    return _ring(P.WASHER_ID, P.WASHER_OD, P.WASHER_H, Z_POCKET)


def screen():
    return _cyl(P.SCREEN_D, P.SCREEN_T, 0, 0, Z_POCKET + P.WASHER_H)


def membrane():
    return _cyl(P.MEMBRANE_DISC_D, P.MEMBRANE_T, 0, 0, Z_POCKET + P.WASHER_H + P.SCREEN_T)   # top = body face


def screws():
    out = []
    for x, y in P.M4_XY:                                                         # M4 x 20 socket head cap
        s = _cyl(4.0, 20.0, x, y, Z_TOP - 20.0).union(_cyl(P.M4_HEAD_D, 4.0, x, y, Z_TOP))
        out.append(s)
    return out


def dowels():
    return [_cyl(P.DOWEL_D - 0.02, 16.0, x, y, -6.0) for x, y in P.DOWEL_XY]


def bed(volume_ul=0.019):
    """Packed bed in the bed bore, on the retainer (default: 1e6 beads of 2.8 um, 19 nL)."""
    import math
    L = volume_ul / (math.pi * P.BED_D ** 2 / 4.0)
    return _cyl(P.BED_D, L, 0, 0, Z_BODY)


def liquid():
    """The wetted volume from the floor of the inlet port to the floor of the outlet port, as one solid."""
    zo = Z_BODY + P.OUTLET_Z
    ch_len = P.RISER_PLATE_X - P.CHANNEL_X_END
    parts = [
        _cyl(P.BED_D, P.INLET_FLOOR, 0, 0, Z_BODY),
        _cyl(P.BED_D, P.RET_POCKET_DEPTH - P.WASHER_H, 0, 0, Z_POCKET + P.WASHER_H),      # through membrane and screen
        _cyl(P.WASHER_ID, P.WASHER_H, 0, 0, Z_POCKET),                                       # hole of the washer
        _cyl(P.EXIT_D, Z_POCKET),
        _cyl(P.GROOVE_STRIP_ID, P.GAP, 0, 0, -P.GAP),                                          # the thin layer
        _ring(2 * P.RING_R0, 2 * P.RING_R1, P.RING_DEPTH),
        _cyl(P.RISER_PLATE_D, P.PLATE_T, P.RISER_PLATE_X),
        cq.Workplane("XY").slot2D(ch_len + P.CHANNEL_W, P.CHANNEL_W).extrude(P.CHANNEL_DEPTH)
        .translate(((P.RISER_PLATE_X + P.CHANNEL_X_END) / 2.0, 0, P.PLATE_T - P.CHANNEL_DEPTH)),
        _cyl(P.RISER_BODY_D, P.OUTLET_Z + P.OUTLET_THROUGH_D / 2.0, P.RISER_BODY_X, 0, Z_BODY),
        _xcyl(P.OUTLET_THROUGH_D, P.X0 + P.PORT_DEPTH, P.RISER_BODY_X, 0, zo),
    ]
    out = parts[0]
    for p in parts[1:]:
        out = out.union(p)
    return out.clean()
