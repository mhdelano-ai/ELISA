"""Solids of the washer punching jig (docs/36).  Every number comes from params.py.

Printed parts: base() J-001, plate() J-002, handle() J-003, spacer() J-004, finger() J-005.  Bought parts (liner,
slip bushings, punch tubes, pins, screws, inserts) and the workpiece are modelled for the assembly, the renders and
the checks only.
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


def _dowel_tools(z0, h):
    (xa, ya), (xb, yb) = J.DOWEL_XY
    ang = math.degrees(math.atan2(yb - ya, xb - xa))
    slot = cq.Workplane("XY").slot2D(J.DOWEL_D + J.SLOT_L, J.DOWEL_D, angle=ang).extrude(h).translate((xb, yb, z0))
    return [_cyl(J.DOWEL_D, h, xa, ya, z0), slot]


# ---- printed parts -------------------------------------------------------------------------------------------------
def base():
    """J-001: flat top (datum), two guide rails for the strip, two pressed pins (holes reamed 2.95), four M3 heat-set
    inserts, two parking bosses for the idle bushing, a pitch scale on the hole positions downstream of the plate."""
    hx, hy = J.BASE_X / 2.0, J.BASE_Y / 2.0
    b = _box(-hx, hx, -hy, hy, -J.BASE_T, 0.0).edges("|Z").fillet(3.0)
    y_in = J.STRIP_W / 2.0 + J.RAIL_GAP / 2.0
    for s in (-1, 1):
        y0, y1 = sorted((s * y_in, s * (y_in + J.RAIL_W)))
        b = b.union(_box(-hx + 3.0, hx - 3.0, y0, y1, 0.0, J.RAIL_H))
    tools = [_cyl(J.DOWEL_D, J.DOWEL_IN_BASE, x, y, -J.DOWEL_IN_BASE) for x, y in J.DOWEL_XY]
    tools += [_cyl(J.INSERT_HOLE_D, J.INSERT_HOLE_DEPTH, x, y, -J.INSERT_HOLE_DEPTH) for x, y in J.SCREW_XY]
    for x, y in J.PARK_XY:                                                     # bosses for the idle bushing
        b = b.union(_cyl(J.PARK_BOSS_D, J.PARK_BOSS_H, x, y, 0.0))
    tools += [_cyl(J.PARK_D, J.PARK_DEPTH + J.PARK_BOSS_H, x, y, -J.PARK_DEPTH) for x, y in J.PARK_XY]
    w, l, d = J.SCALE_TICK
    y_tick = y_in + J.RAIL_W + 0.4
    n = int(round((J.SCALE_X1 - J.SCALE_X0) / J.PITCH)) + 1
    for i in range(n):
        x = J.SCALE_X0 + i * J.PITCH
        ll = 2 * l if abs(x % 15.0) < 1e-6 else l
        tools.append(_box(x - w / 2, x + w / 2, y_tick, y_tick + ll, -d, 0.0))
    return _cut_all(b, tools)


def plate():
    """J-002: reamed hole for the liner (bonded with the bushing face flush with the foot, liner top 0.8 above the
    plate top); below it the bushing body passes through the foot; relief over the strip; dowel hole + slot; four
    screw holes; the insert for the finger's shoulder screw."""
    hx, hy = J.PLATE_X / 2.0, J.PLATE_Y / 2.0
    p = _box(-hx, hx, -hy, hy, J.Z_FOOT, J.Z_PLATE_TOP).edges("|Z").fillet(2.0)
    relief = _box(-hx - 1, hx + 1, -J.RECESS_HALF_W, J.RECESS_HALF_W, J.Z_FOOT, J.Z_FOOT + J.RECESS_DEPTH) \
        .cut(_cyl(J.FOOT_D, J.RECESS_DEPTH, 0, 0, J.Z_FOOT))
    tools = [relief, _cyl(J.LINER_HOLE_D, J.Z_PLATE_TOP - J.Z_LEDGE, 0, 0, J.Z_LEDGE),
             _cyl(J.BODY_HOLE_D, J.Z_LEDGE - J.Z_FOOT, 0, 0, J.Z_FOOT)]
    tools += _dowel_tools(J.Z_FOOT, J.PLATE_T)
    tools += [_cyl(J.SCREW_CLEAR, J.PLATE_T, x, y, J.Z_FOOT) for x, y in J.SCREW_XY]
    lx, ly = J.LOCK_XY
    tools.append(_cyl(J.INSERT_HOLE_D, J.INSERT_HOLE_DEPTH, lx, ly, J.Z_PLATE_TOP - J.INSERT_HOLE_DEPTH))
    return _cut_all(p, tools)


def handle(p, printed=False):
    """J-003 for one SYNEO tube, nose face at z = 0 (the stop on the bushing head) as faced; printed=True gives the
    part as printed, with NOSE_ALLOW more nose below z = 0.  Nose, mushroom grip, drilled pocket in which the tube is
    located by a shoulder, push-wire hole (tube bore + 0.02) through to the top."""
    extra = J.NOSE_ALLOW if printed else 0.0
    nose = _cyl(J.NOSE_D, J.NOSE_L + extra, 0, 0, -extra)
    grip = _cyl(J.GRIP_D, J.GRIP_L, 0, 0, J.NOSE_L).edges(">Z").fillet(3.0).faces("<Z").edges().chamfer(1.0)
    h = nose.union(grip)
    depth = J.pocket_depth(p)
    return _cut_all(h, [_cyl(p["tube_od"] + J.POCKET_CLEAR, depth + extra, 0, 0, -extra),
                        _cyl(p["bore"] + J.PUSH_HOLE_EXTRA, J.NOSE_L + J.GRIP_L + extra, 0, 0, -extra)])


def spacer(printed=False):
    """J-004: ring under the finger on the shoulder screw; printed FINGER_SET_ALLOW high, faced at assembly so that
    the finger lies FINGER_GAP above the thicker bushing head."""
    lx, ly = J.LOCK_XY
    h = J.SPACER_H + (J.FINGER_SET_ALLOW if printed else 0.0)
    return _tube(J.SHOULDER_D + 0.1, J.SPACER_D, h, lx, ly, J.Z_PLATE_TOP)


def finger(angle_deg=-90.0, toward_axis=0.0):
    """J-005: ring finger on the shoulder screw.  angle -90 = ring over the bushing head (locked); 0 or 180 = swung
    clear.  toward_axis shifts it (hole play, printed tolerance) for the clearance checks."""
    lx, ly = J.LOCK_XY
    arm = _box(0, J.LOCK_R, -J.FINGER_W / 2, J.FINGER_W / 2, 0, J.FINGER_T)
    ring = _cyl(2 * J.RING_R_OUT, J.FINGER_T, J.LOCK_R, 0, 0)
    boss = _cyl(J.BOSS_D, J.FINGER_T)
    f = arm.union(ring).union(boss)
    f = f.cut(_cyl(2 * J.RING_R_IN, J.FINGER_T, J.LOCK_R, 0, 0)).cut(_cyl(J.FINGER_HOLE_D, J.FINGER_T))
    c = J.FINGER_CHAMFER                                                # lead-in under the ring's outer edge
    lead = cq.Workplane("XY").add(cq.Solid.makeCone(J.RING_R_OUT - c, J.RING_R_OUT + 0.01, c,
                                                    cq.Vector(J.LOCK_R, 0, 0), cq.Vector(0, 0, 1)))
    f = f.cut(_tube(2 * J.RING_R_OUT - 2 * c, 2 * J.RING_R_OUT + 2, c, J.LOCK_R, 0, 0).cut(lead))
    f = f.rotate((0, 0, 0), (0, 0, 1), angle_deg)
    return f.translate((lx, ly - toward_axis, J.Z_FINGER0))


# ---- bought parts --------------------------------------------------------------------------------------------------
def liner():
    """Carr Lane L-20-6, at its largest OD; its top (the bushing's seat) is where the bushing face is flush with the
    foot."""
    return _tube(J.LINER_ID, J.LINER_OD, J.LINER_L, 0, 0, J.Z_LINER_BOT)


def slip_bushing(punch):
    """Carr Lane SF-12-8-<bore>-NCB, seated on the liner end (recesses in the head not modelled)."""
    shank = _tube(J.slip_bore(punch), J.LINER_ID, J.BODY_L, 0, 0, J.Z_FOOT)
    head = _tube(J.slip_bore(punch), J.SLIP_HEAD_D, J.SLIP_HEAD_H, 0, 0, J.Z_LINER_TOP)
    return shank.union(head)


def punch(p):
    """Tube in its handle at the end of the stroke (nose on the bushing head)."""
    tube = _tube(p["bore"], p["tube_od"], p["tube_l"], 0, 0, J.Z_TIP)
    return tube.union(handle(p).translate((0, 0, J.Z_HEAD_TOP)))


def lock_screw():
    """ISO 7379-4-M3-10 shoulder screw and, above the finger, the O-ring and the shim rings (one solid)."""
    lx, ly = J.LOCK_XY
    sc = _cyl(J.SHOULDER_D, J.SHOULDER_L, lx, ly, J.Z_PLATE_TOP) \
        .union(_cyl(J.SHOULDER_HEAD_D, J.SHOULDER_HEAD_H, lx, ly, J.Z_SHOULDER_TOP)) \
        .union(_cyl(J.SCREW_D, J.SHOULDER_THREAD, lx, ly, J.Z_PLATE_TOP - J.SHOULDER_THREAD))
    z_sh = J.Z_FINGER0 + J.FINGER_T + J.FINGER_PLAY
    shims = _tube(J.SHOULDER_D + 0.1, 8.0, J.Z_SHOULDER_TOP - z_sh, lx, ly, z_sh)
    return shims, sc


def dowels():
    return [_cyl(J.DOWEL_D, J.DOWEL_L, x, y, -J.DOWEL_IN_BASE) for x, y in J.DOWEL_XY]


def screws():
    out = []
    for x, y in J.SCREW_XY:
        out.append(_cyl(J.SCREW_D, J.SCREW_L, x, y, J.Z_PLATE_TOP - J.SCREW_L)
                   .union(_cyl(J.THUMB_HEAD_D, J.THUMB_HEAD_H, x, y, J.Z_PLATE_TOP)))
    return out


def inserts():
    lx, ly = J.LOCK_XY
    out = [_tube(J.SCREW_D, J.INSERT_HOLE_D, J.INSERT_L, x, y, -J.INSERT_L) for x, y in J.SCREW_XY]
    out.append(_tube(J.SCREW_D, J.INSERT_HOLE_D, J.INSERT_L, lx, ly, J.Z_PLATE_TOP - J.INSERT_L))
    return out


def backing(x0=-45.0):
    return _box(x0, x0 + J.STRIP_L, -J.STRIP_W / 2, J.STRIP_W / 2, 0.0, J.BACKING_T)


def sheet(x0=-45.0, punched=True):
    """FKM strip (top = foot face); downstream of the axis it carries the holes of earlier washers; at the axis the
    hole of stroke 1."""
    s = _box(x0, x0 + J.STRIP_L, -J.STRIP_W / 2, J.STRIP_W / 2, J.Z_SHEET0, J.Z_FOOT)
    if punched:
        x = J.PITCH
        while x < x0 + J.STRIP_L - 1.0:
            s = s.cut(_cyl(J.WASHER_OD, J.Z_FOOT - J.Z_SHEET0, x, 0, J.Z_SHEET0))
            x += J.PITCH
    return s.cut(_cyl(J.WASHER_ID, J.Z_FOOT - J.Z_SHEET0, 0, 0, J.Z_SHEET0))
