"""Solids of the washer punching jig (docs/36).  Every number comes from params.py.

Printed parts: base(), plate().  Bought parts (liner, slip bushings, pins, screws, inserts) and the workpiece are
modelled for the assembly, the renders and the checks only.
"""
from __future__ import annotations

import math

import cadquery as cq

from . import params as J


def _cyl(d, h, x=0.0, y=0.0, z0=0.0):
    return cq.Workplane("XY").circle(d / 2.0).extrude(h).translate((x, y, z0))


def _tube(d_in, d_out, h, x=0.0, y=0.0, z0=0.0):
    return cq.Workplane("XY").circle(d_out / 2.0).circle(d_in / 2.0).extrude(h).translate((x, y, z0))


def _box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def _cut_all(body, tools):
    for t in tools:
        body = body.cut(t)
    return body


# ---- printed parts -------------------------------------------------------------------------------------------------
def base():
    """Base: flat top (datum), two guide rails for the strip, two pressed pins, two M4 heat-set inserts, a pitch
    scale beside the rail downstream of the head plate."""
    hx, hy = J.BASE_X / 2.0, J.BASE_Y / 2.0
    b = _box(-hx, hx, -hy, hy, -J.BASE_T, 0.0).edges("|Z").fillet(3.0)
    y_in = J.STRIP_W / 2.0 + J.RAIL_GAP / 2.0
    for s in (-1, 1):
        y0, y1 = sorted((s * y_in, s * (y_in + J.RAIL_W)))
        b = b.union(_box(-hx + 3.0, hx - 3.0, y0, y1, 0.0, J.RAIL_H))
    tools = [_cyl(J.DOWEL_D, J.DOWEL_IN_BASE, x, y, -J.DOWEL_IN_BASE) for x, y in J.DOWEL_XY]   # printed 2.9, reamed
    tools += [_cyl(J.INSERT_HOLE_D, J.INSERT_L + 1.0, x, y, -(J.INSERT_L + 1.0)) for x, y in J.SCREW_XY]
    w, l, d = J.SCALE_TICK
    y_tick = y_in + J.RAIL_W + 0.4
    n = int((J.SCALE_X1 - J.SCALE_X0) / J.PITCH) + 1
    for i in range(n):
        x = J.SCALE_X0 + i * J.PITCH
        ll = 2 * l if i % 5 == 0 else l
        tools.append(_box(x - w / 2, x + w / 2, y_tick, y_tick + ll, -d, 0.0))
    return _cut_all(b, tools)


def plate():
    """Head plate: carries the liner bushing on the punch axis; it rests only on the sheet, with the foot around the
    liner (the rest of the underside is relieved over the strip and clears the base outside it)."""
    hx, hy = J.PLATE_X / 2.0, J.PLATE_Y / 2.0
    p = _box(-hx, hx, -hy, hy, J.Z_FOOT, J.Z_PLATE_TOP).edges("|Z").fillet(2.0)
    relief = _box(-hx - 1, hx + 1, -J.RECESS_HALF_W, J.RECESS_HALF_W, J.Z_FOOT, J.Z_FOOT + J.RECESS_DEPTH) \
        .cut(_cyl(J.FOOT_D, J.RECESS_DEPTH, 0, 0, J.Z_FOOT))
    tools = [relief, _cyl(J.LINER_HOLE_D, J.PLATE_T, 0, 0, J.Z_FOOT)]
    lx, ly = _lock_xy()
    tools.append(_cyl(J.INSERT_HOLE_D, J.INSERT_L + 1.0, lx, ly, J.Z_PLATE_TOP - J.INSERT_L - 1.0))   # lock insert
    (xa, ya), (xb, yb) = J.DOWEL_XY
    tools.append(_cyl(J.DOWEL_D + J.DOWEL_HOLE_CLEAR, J.PLATE_T, xa, ya, J.Z_FOOT))
    # slot at the second pin, along the line joining the pins (only the pin spacing is free)
    import math
    ang = math.degrees(math.atan2(yb - ya, xb - xa))
    slot = cq.Workplane("XY").slot2D(J.DOWEL_D + J.DOWEL_HOLE_CLEAR + 1.0, J.DOWEL_D + J.DOWEL_HOLE_CLEAR,
                                     angle=ang).extrude(J.PLATE_T).translate((xb, yb, J.Z_FOOT))
    tools.append(slot)
    tools += [_cyl(J.SCREW_CLEAR, J.PLATE_T, x, y, J.Z_FOOT) for x, y in J.SCREW_XY]
    return _cut_all(p, tools)


def _lock_xy():
    a = math.radians(J.LOCK_ANGLE)
    return J.LOCK_R * math.cos(a), J.LOCK_R * math.sin(a)


def handle(p):
    """Printed handle J-003 for a SYNEO tube: the tube is bonded into a blind bore; a through hole on the axis lets the
    push wire reach the tube's bore.  Drawn at the origin, tube bore from z = 0 up."""
    h = _cyl(J.HANDLE_D, J.HANDLE_L).edges().chamfer(0.8)
    return _cut_all(h, [_cyl(p["tube_od"] + 0.05, J.TUBE_IN_HANDLE), _cyl(J.PUSH_WIRE["B"] + 0.3, J.HANDLE_L)])


# ---- bought parts --------------------------------------------------------------------------------------------------
def liner():
    return _tube(J.LINER_ID, J.LINER_OD, J.LINER_L, 0, 0, J.Z_FOOT)


def slip_bushing(punch):
    shank = _tube(J.slip_bore(punch), J.LINER_ID, J.LINER_L, 0, 0, J.Z_FOOT)
    head = _tube(J.slip_bore(punch), J.SLIP_HEAD_D, J.SLIP_HEAD_H, 0, 0, J.Z_PLATE_TOP)
    return shank.union(head)


def punch(p, z_tip=None):
    """SYNEO tube in its handle at the bottom of its stroke."""
    z_tip = J.Z_TIP if z_tip is None else z_tip
    tube = _tube(p["bore"], p["tube_od"], p["tube_l"], 0, 0, z_tip)
    return tube.union(handle(p).translate((0, 0, z_tip + J.exposed(p))))


def lock_screw():
    """M3 x 10 socket head screw with a DIN 125 washer, clamping the slip bushing's head (CHOICE; or Carr Lane LS-0)."""
    lx, ly = _lock_xy()
    z = J.Z_PLATE_TOP + J.SLIP_HEAD_H
    w = _tube(3.2, J.LOCK_WASHER_D, 0.5, lx, ly, z)
    sc = _cyl(J.SCREW_D, J.LOCK_SCREW_L, lx, ly, z + 0.5 - J.LOCK_SCREW_L).union(_cyl(5.5, 3.0, lx, ly, z + 0.5))
    return w, sc


def lock_spacer():
    """Printed or cut ring under the lock washer, so that the washer bears on the bushing head (head height)."""
    lx, ly = _lock_xy()
    return _tube(3.4, J.LOCK_SPACER_D, J.SLIP_HEAD_H, lx, ly, J.Z_PLATE_TOP)


def dowels():
    return [_cyl(J.DOWEL_D, J.DOWEL_L, x, y, -J.DOWEL_IN_BASE) for x, y in J.DOWEL_XY]


def screws():
    out = []
    for x, y in J.SCREW_XY:
        out.append(_cyl(J.SCREW_D, J.SCREW_L, x, y, J.Z_PLATE_TOP - J.SCREW_L)
                   .union(_cyl(J.THUMB_HEAD_D, J.THUMB_HEAD_H, x, y, J.Z_PLATE_TOP)))
    return out


def inserts():
    lx, ly = _lock_xy()
    out = [_tube(J.SCREW_D, J.INSERT_HOLE_D, J.INSERT_L, x, y, -J.INSERT_L) for x, y in J.SCREW_XY]
    out.append(_tube(J.SCREW_D, J.INSERT_HOLE_D, J.INSERT_L, lx, ly, J.Z_PLATE_TOP - J.INSERT_L))
    return out


def backing(x0=-45.0):
    return _box(x0, x0 + J.STRIP_L, -J.STRIP_W / 2, J.STRIP_W / 2, 0.0, J.BACKING_T)


def sheet(x0=-45.0, punched=True):
    """FKM strip (top = foot face); upstream of the axis it is whole,
    downstream it carries the holes left by earlier washers."""
    s = _box(x0, x0 + J.STRIP_L, -J.STRIP_W / 2, J.STRIP_W / 2, J.Z_SHEET0, J.Z_FOOT)
    if punched:
        x = J.PITCH
        while x < x0 + J.STRIP_L - 1.0:
            s = s.cut(_cyl(J.WASHER_OD, J.Z_FOOT - J.Z_SHEET0, x, 0, J.Z_SHEET0))
            x += J.PITCH
    return s.cut(_cyl(J.WASHER_ID, J.Z_FOOT - J.Z_SHEET0, 0, 0, J.Z_SHEET0))     # the hole punched by stroke 1


def washer_in_sheet():
    """The washer being made, at the axis (hole punched, outside about to be punched)."""
    return _tube(J.WASHER_ID, J.WASHER_OD, J.Z_FOOT - J.Z_SHEET0, 0, 0, J.Z_SHEET0)
