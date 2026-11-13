"""DOCK UPPER solids. Head parts are built in CARD coords with the head LOWERED (latched); lid-frame parts in DOCK
coords with the lid closed. assy.py places them. Catalogue parts are labelled envelopes (name prefix 'ENV_').
All numbers from params.py / interface.py.
"""
from __future__ import annotations

import math

import cadquery as cq
from shapely.geometry import LineString, Point
from shapely.ops import unary_union

from elisa_cad import interface as IF
from elisa_cad.common import box_from_corners
from elisa_cad.dock_upper import params as P


# ------------------------------------------------------------------------------------------------ helpers
def cyl(x, y, z0, z1, d):
    return cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(d / 2.0).extrude(z1 - z0)


def tube(x, y, z0, z1, od, id_):
    return (cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(od / 2.0).circle(id_ / 2.0)
            .extrude(z1 - z0))


def box(x0, x1, y0, y1, z0, z1):
    return box_from_corners((x0, y0, z0), (x1, y1, z1))


def slab_from_poly(poly, z0, z1):
    pts = [(float(x), float(y)) for x, y in poly.exterior.coords][:-1]
    return cq.Workplane("XY").workplane(offset=z0).polyline(pts).close().extrude(z1 - z0)


def union_all(objs):
    out = None
    for o in objs:
        out = o if out is None else out.union(o)
    return out


def cut_cyls(solid, pts_d, z0, z1):
    for (x, y), d in pts_d:
        solid = solid.cut(cyl(x, y, z0, z1, d))
    return solid


# ------------------------------------------------------------------------------------------------ pin geometry
def pin_levels(v):
    """Card-z levels of pin v in the CLOSED state (tip on the foil), see params / docs/20 §2.3."""
    k = P.pkey(v)
    tier = IF.CYLINDERS[v.id]["tier"]
    if v.id == "V3":
        d = P.STROKE  # V3 'closed' = open position - 0.8
        return dict(tip=P.TIP_Z_CLOSED, collar=(P.V3["collar_open"][0] - d, P.V3["collar_open"][1] - d),
                    button=(P.V3["button_open"][0] - d, P.V3["button_open"][1] - d), neck_top=None, k=k, tier=tier)
    eye0 = P.TIER_Z[tier][0]
    btn0 = eye0 + P.EYE_T + P.HOOK_GAP
    return dict(tip=P.TIP_Z_CLOSED, collar=P.COLLAR_Z_CLOSED, button=(btn0, btn0 + P.HEAD_BTN_T), k=k, tier=tier)


def pin_solid(v, dz=0.0):
    """Valve pin (custom turned part, non-magnetic stainless) + bonded button sleeve. dz = lift above closed."""
    L = pin_levels(v)
    x, y = v.xy
    k = L["k"]
    tip = L["tip"] + dz
    sh = v.pin_d
    s = cyl(x, y, tip + 0.1, L["collar"][0] + dz, sh)
    s = s.union(cyl(x, y, tip, tip + 0.1, v.tip_d))                       # flat tip land (0.1 x 45 at 1.2 -> 1.0)
    s = s.union(cyl(x, y, L["collar"][0] + dz, L["collar"][1] + dz, P.COLLAR_D[k]))
    s = s.union(cyl(x, y, L["collar"][1] + dz, L["button"][1] + dz, P.NECK_D[k]))
    btn = tube(x, y, L["button"][0] + dz, L["button"][1] + dz, P.HEAD_BTN_D[k], P.NECK_D[k])
    return s, btn


def spring_env(v, dz=0.0):
    """Pin spring envelope (tube OD/ID). Normal pins: collar top -> spring-plate underside. V3: block top -> collar."""
    L = pin_levels(v)
    x, y = v.xy
    if v.id == "V3":
        s = P.V3["open_spring"]
        return tube(x, y, P.HB_Z1, L["collar"][0] + dz, s["Dm"] + s["d"], s["Dm"] - s["d"])
    s = P.PIN_SPRINGS[P.valve_class(v)]
    return tube(x, y, L["collar"][1] + dz, P.SPRING_PLATE_Z[0], s["Dm"] + s["d"], s["Dm"] - s["d"])


# ------------------------------------------------------------------------------------------------ yokes
def yoke(vid, dz=0.0):
    """Yoke blade (laser-cut 1.4310 sheet 1.0, folded/brazed where noted). Returns (solid, rod_top_z, rod_bot_z).
    dz = vertical travel of the yoke (+ up) relative to rest."""
    v = IF.VALVES[vid]
    c = IF.CYLINDERS[vid]
    k = P.pkey(v)
    px, py = v.xy
    cx, cy = c["xy"]
    L = math.dist(v.xy, c["xy"])
    ux, uy = (cx - px) / L, (cy - py) / L          # pin -> rod
    t0, t1 = P.TIER_Z[c["tier"]]
    eye_r = P.FORK_SLOT[k] / 2 + 0.4
    btn_r = P.HEAD_BTN_D[k] / 2
    w = P.BLADE_W
    slot = P.FORK_SLOT[k]

    def strip(a, b, z0, z1, width=w):
        ln = LineString([a, b]).buffer(width / 2, cap_style=2, join_style=2)
        return slab_from_poly(ln, z0 + dz, z1 + dz)

    if vid == "V3":                                 # push yoke: everything above the button
        e0, e1 = P.V3["eye_rest"]
        body = strip((px, py), (cx, cy), e0, t1)
        body = body.union(cyl(cx, cy, e0 + dz, t1 + dz, P.BOSS_D)).union(cyl(px, py, e0 + dz, e1 + dz, 2 * eye_r))
        top = t1
    elif L >= P.BOSS_D / 2 + btn_r + 0.4:           # standard: web stops short of the button, tongue to the eye
        web_end = (px + ux * (btn_r + 0.3), py + uy * (btn_r + 0.3))
        body = strip(web_end, (cx, cy), t0, t1)
        body = body.union(strip((px, py), (cx, cy), t0, t0 + P.EYE_T))
        body = body.union(cyl(cx, cy, t0 + dz, t1 + dz, P.BOSS_D)).union(cyl(px, py, t0 + dz, t0 + P.EYE_T + dz,
                                                                            2 * eye_r))
        top = t1
    else:                                           # J-yoke (V9): rod nearly coaxial with the pin
        bu = J_BACK_DIR.get(vid, (ux, uy))
        back = (cx + bu[0] * 3.0, cy + bu[1] * 3.0)
        tab0, tab1 = t0 + P.EYE_T + P.HOOK_GAP + P.HEAD_BTN_T + P.STROKE + 0.2, t1 + 1.0   # 30.6 .. 32.0
        body = strip((px, py), back, t0, t0 + P.EYE_T)                       # tongue under the button
        body = body.union(strip((cx, cy), back, tab0, tab1))                  # top tab under the rod
        body = body.union(cyl(back[0], back[1], t0 + dz, tab1 + dz, 1.6))     # web post
        body = body.union(cyl(px, py, t0 + dz, t0 + P.EYE_T + dz, 2 * eye_r))
        body = body.union(cyl(cx, cy, tab0 + dz, tab1 + dz, P.BOSS_D))
        top = tab1
    # fork slot (open toward the far side of the rod) at the eye
    fx, fy = px - ux * 2 * eye_r, py - uy * 2 * eye_r
    sx_, sy_ = px + ux * (slot / 2 + 0.1), py + uy * (slot / 2 + 0.1)     # slot end beyond the neck
    fork = slab_from_poly(LineString([(sx_, sy_), (fx, fy)]).buffer(slot / 2, cap_style=2, join_style=2), -10, 100)
    body = body.cut(fork)
    return body, top + dz


def rod_solid(vid, dz=0.0):
    c = IF.CYLINDERS[vid]
    _, top = yoke(vid, 0.0)
    return cyl(c["xy"][0], c["xy"][1], top + dz, P.CYL_LAYERS["bore_block"][0] + 1.0 + dz, P.ROD_D)


# ------------------------------------------------------------------------------------------------ air galleries
J_BACK_DIR = {"V9": (1.0, 0.0)}     # J-yoke web direction override (clear of the standoff)
V8_BUSH_Z0 = P.HB_Z0 + 1.5          # V8 bronze bush starts 1.5 above the face (P_mv groove 0.75 deep)
COL_DIR = {5.0: -1, 23.0: -1, 32.0: 1, 41.0: 1, 50.0: 1, 59.0: 1, 68.0: 0}   # 0 = straight to the +x face
VIA_R_OFF = 1.9          # via (D0.8) radius position inside the annulus (rod seal r 1.25 .. bore r 3.0)
SLOT0, SLOT_PITCH = 3.0, 1.1


def route_galleries():
    """Single-layer gallery routing on the air-plate underside (docs/20 §2.5). Returns {vid: dict(via, path, exit)}.
    Lanes between cylinder columns, exits on the rear (+y) face, column x = 68 straight to the +x face.
    Order inside a lane: the cylinder farthest from the exit gets the outermost slot (no crossings)."""
    groups = {}
    for vid, c in IF.CYLINDERS.items():
        groups.setdefault(c["xy"][0], []).append(vid)
    routes = {}
    for xc, vids in groups.items():
        d = COL_DIR[xc]
        vids = sorted(vids, key=lambda i: IF.CYLINDERS[i]["xy"][1], reverse=True)   # nearest to +y exit first
        for k, vid in enumerate(vids):
            yc = IF.CYLINDERS[vid]["xy"][1]
            if d == 0:
                via = (xc + VIA_R_OFF, yc)
                routes[vid] = dict(via=via, path=[via, (P.CYL_BLOCK_X[1], yc)], exit="+x")
                continue
            off = 4.0 if vid == "V3" else VIA_R_OFF
            via = (xc + d * off, yc)
            sx = xc + d * (SLOT0 + k * SLOT_PITCH)
            if vid == "V3":
                sx = max(sx, via[0]) if d > 0 else min(sx, via[0])
            routes[vid] = dict(via=via, path=[via, (sx, yc), (sx, P.CYL_BLOCK_Y[1])], exit="+y")
    return routes


def gallery_check(routes):
    """Min web between grooves, and grooves vs rod holes, vias of others, screw holes (shapely, 2D)."""
    gw = P.GALLERY_W
    grooves = {vid: LineString(r["path"]).buffer(gw / 2, cap_style=2) for vid, r in routes.items()}
    rods = {vid: Point(c["xy"]).buffer(0.9) for vid, c in IF.CYLINDERS.items()}
    vias = {vid: Point(r["via"]).buffer(0.4) for vid, r in routes.items()}
    screws = [Point(p).buffer(1.6) for p in P.STANDOFFS_HB[:4] + P.STANDOFFS_PEEK]
    screws += [Point(p).buffer(4.0) for p in P.GUIDE_PINS.values()]
    mins = {"groove-groove": 99.0, "groove-rod": 99.0, "groove-via(other)": 99.0, "groove-screw/ear": 99.0}
    ids = list(grooves)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            mins["groove-groove"] = min(mins["groove-groove"], grooves[a].distance(grooves[b]))
        for b in ids:
            mins["groove-rod"] = min(mins["groove-rod"], grooves[a].distance(rods[b]) if b != a else 99)
            if b != a:
                mins["groove-via(other)"] = min(mins["groove-via(other)"], grooves[a].distance(vias[b]))
        for s in screws:
            mins["groove-screw/ear"] = min(mins["groove-screw/ear"], grooves[a].distance(s))
    length = {vid: LineString(r["path"]).length for vid, r in routes.items()}
    return mins, length


# ------------------------------------------------------------------------------------------------ head plates
def heater_block():
    """Al 6061-T6 heater block = pin guide carrier (custom, CNC). Card coords, head lowered."""
    x0, x1 = P.HB_X
    b = box(x0, x1, P.HB_Y[0], P.HB_Y[1], P.HB_Z0, P.HB_Z1)
    fz0, fz1 = P.HEATER_FIN["z"]
    fx0, fx1 = P.HEATER_FIN["x"]
    t = P.HEATER_FIN["t"]
    b = b.union(box(fx0, fx1, 0.0, t, fz0, fz1)).union(box(fx0, fx1, IF.CARD_W - t, IF.CARD_W, fz0, fz1))
    # guide-plate recesses (lower + upper)
    gp = guide_plate_outline()
    b = b.cut(slab_from_poly(gp, P.HB_Z0 - 0.1, P.HB_Z0 + P.GUIDE_PLATE_T))
    b = b.cut(slab_from_poly(gp, P.HB_Z1 - P.GUIDE_PLATE_T_UP, P.HB_Z1 + 0.1))
    # pin clearance holes between the plates
    for v in IF.VALVES.values():
        if v.xy[0] > P.HB_X[0]:
            b = b.cut(cyl(v.xy[0], v.xy[1], P.HB_Z0, P.HB_Z1 + 0.1, v.pin_d + 0.3))
    # vent pockets + sideways grooves
    b = b.cut(vent_cutter(P.HB_Z0))
    # press-pad stem bore + pad clearance window
    px = (P.PAD["footprint_x"][0] + P.PAD["footprint_x"][1]) / 2
    py = (P.PAD["footprint_y"][0] + P.PAD["footprint_y"][1]) / 2
    b = b.cut(cyl(px, py, P.HB_Z0, P.HB_Z1 + 0.1, P.PAD_STEM_D + 0.02))
    b = b.cut(box(P.PAD["footprint_x"][0] - 0.3, P.PAD["footprint_x"][1] + 0.3,
                  P.PAD["footprint_y"][0] - 0.3, P.PAD["footprint_y"][1] + 0.3, P.HB_Z0 - 0.1, P.HB_Z0 + 3.0))
    # standoff screw holes (M3) and sensor holes (D2.6 x along x)
    for (x, y) in P.STANDOFFS_HB:
        b = b.cut(cyl(x, y, P.HB_Z1 - 8.0, P.HB_Z1 + 0.1, 2.5))
    for name, (sx, sy, sz) in P.SENSOR["positions"].items():
        xa = P.HB_X[1] if sx > 45 else P.HB_X[0]
        lo, hi = (sx - 1.6, xa + 0.1) if xa > sx else (xa - 0.1, sx + 1.6)
        b = b.cut(cq.Workplane("YZ").workplane(offset=lo).center(sy, sz).circle(1.6).extrude(hi - lo))
    # guide-pin ear clearance not needed (ears are on the cylinder block)
    return b


def guide_plate_outline():
    pts = [v.xy for v in IF.VALVES.values() if v.xy[0] > P.HB_X[0]]
    hull = unary_union([Point(p).buffer(2.0) for p in pts]).convex_hull
    return hull.buffer(0.5, join_style=2).simplify(0.05)


def guide_plate(lower=True):
    """CuSn8 bearing-bronze guide plates, reamed H7 holes (custom; jig-bored/reamed)."""
    gp = guide_plate_outline()
    z0, z1 = (P.HB_Z0, P.HB_Z0 + P.GUIDE_PLATE_T) if lower else (P.HB_Z1 - P.GUIDE_PLATE_T_UP, P.HB_Z1)
    g = slab_from_poly(gp, z0, z1)
    for v in IF.VALVES.values():
        if v.xy[0] > P.HB_X[0]:
            g = g.cut(cyl(v.xy[0], v.xy[1], z0 - 0.1, z1 + 0.1, v.pin_d + 0.004))
            if lower:  # lead-out chamfer at the face, simplified as a 0.2 counterbore
                g = g.cut(cyl(v.xy[0], v.xy[1], z0 - 0.1, z0 + 0.2, v.pin_d + 0.4))
    g = g.cut(vent_cutter(P.HB_Z0))
    px = (P.PAD["footprint_x"][0] + P.PAD["footprint_x"][1]) / 2
    py = (P.PAD["footprint_y"][0] + P.PAD["footprint_y"][1]) / 2
    g = g.cut(cyl(px, py, z0 - 0.1, z1 + 0.1, P.PAD_STEM_D + 0.02))
    g = g.cut(box(P.PAD["footprint_x"][0] - 0.3, P.PAD["footprint_x"][1] + 0.3,
                  P.PAD["footprint_y"][0] - 0.3, P.PAD["footprint_y"][1] + 0.3, z0 - 0.1, z0 + 3.0))
    return g


def vent_cutter(zface):
    out = None
    for name, (x, y) in IF.VENTS.items():
        dx, dy = P.VENT_EXITS[name]
        c = cyl(x, y, zface - 0.1, zface + P.VENT_POCKET_DEPTH, P.VENT_POCKET_D)
        far = (x + dx * 60.0, y + dy * 60.0)
        c = c.union(slab_from_poly(LineString([(x, y), far]).buffer(P.VENT_GROOVE_W / 2, cap_style=2),
                                   zface - 0.1, zface + P.VENT_POCKET_DEPTH))
        out = c if out is None else out.union(c)
    return out


def peek_plate():
    """PEEK pressure plate over the reagent zone (custom, CNC): V8 bush bore, gas-seal grooves and gas bores."""
    x0, x1 = P.PEEK_X
    b = box(x0, x1, 0.0, IF.CARD_W, P.HB_Z0, P.HB_Z1)
    v8 = IF.VALVES["V8"]
    b = b.cut(cyl(v8.xy[0], v8.xy[1], V8_BUSH_Z0, P.HB_Z1 + 0.1, 3.0))         # bronze bush seat D3
    b = b.cut(cyl(v8.xy[0], v8.xy[1], P.HB_Z0 - 0.1, V8_BUSH_Z0 + 0.1, v8.pin_d + 0.3))
    for pid, p in P.GAS_PORTS.items():
        x, y = p.xy
        groove = tube(x, y, P.HB_Z0 - 0.1, P.HB_Z0 + P.GAS_GROOVE_DEPTH, P.GAS["od"] + 0.1, P.GAS["id"] - 0.1)
        b = b.cut(groove).cut(cyl(x, y, P.HB_Z0 - 0.1, P.HB_Z1 + 0.1, 1.0))
        b = b.cut(cyl(x, y, P.HB_Z1 - 4.0, P.HB_Z1 + 0.1, 2.5))                # M3 tapped seat for the barb
    for (x, y) in P.STANDOFFS_PEEK:
        b = b.cut(cyl(x, y, P.HB_Z1 - 8.0, P.HB_Z1 + 0.1, 2.5))
    return b


def v8_bush():
    v8 = IF.VALVES["V8"]
    b = cyl(v8.xy[0], v8.xy[1], V8_BUSH_Z0, P.HB_Z1, 3.0)      # starts above the P_mv ring groove (CHOICE-U2)
    return b.cut(cyl(v8.xy[0], v8.xy[1], P.HB_Z0 - 0.1, P.HB_Z1 + 0.1, v8.pin_d + 0.004))


def gas_rings():
    out = []
    for pid, p in P.GAS_PORTS.items():
        x, y = p.xy
        z0 = P.HB_Z0 - P.GAS["compression"]       # drawn uncompressed (protrudes 0.25 below the face)
        out.append((pid, tube(x, y, z0 + 0.25, z0 + 0.25 + P.GAS_GROOVE_DEPTH, P.GAS["od"], P.GAS["id"])))
    return out


def gas_barbs():
    return [(pid, cyl(p.xy[0], p.xy[1], P.HB_Z1, P.HB_Z1 + 9.0, 5.0)) for pid, p in P.GAS_PORTS.items()]


def standoffs():
    """PEEK standoffs (custom turned): heater block / PEEK plate -> spring plate -> cylinder-block cover."""
    out = []
    for (x, y) in P.STANDOFFS_HB + P.STANDOFFS_PEEK:
        out.append(cyl(x, y, P.HB_Z1, P.SPRING_PLATE_Z[0], P.STANDOFF_D)
                   .cut(cyl(x, y, P.HB_Z1 - 1, P.SPRING_PLATE_Z[0] + 1, 3.2)))
        out.append(cyl(x, y, P.SPRING_PLATE_Z[1], P.CYL_LAYERS["cover"][0], P.STANDOFF_D)
                   .cut(cyl(x, y, P.SPRING_PLATE_Z[1] - 1, P.CYL_LAYERS["cover"][0] + 1, 3.2)))
    for (x, y) in P.MID_PILLARS:                        # mid pillars under the spring plate only
        out.append(cyl(x, y, P.HB_Z1, P.SPRING_PLATE_Z[0], 5.0))
    return out


def spring_plate():
    """Stainless 1.4301 plate 1.5 (laser-cut, flat-ground): seat of all pin springs, open stop of V3, lower stop
    of the V3 button. Holes: necks + 0.3, press-pad stem, standoff screws."""
    z0, z1 = P.SPRING_PLATE_Z
    sp = box(1.0, 76.0, 3.0, 47.0, z0, z1)
    for v in IF.VALVES.values():
        k = P.pkey(v)
        d = P.NECK_D[k] + 0.3 if v.id != "V3" else v.pin_d + 0.3
        sp = sp.cut(cyl(v.xy[0], v.xy[1], z0 - 0.1, z1 + 0.1, d))
    px = (P.PAD["footprint_x"][0] + P.PAD["footprint_x"][1]) / 2
    py = (P.PAD["footprint_y"][0] + P.PAD["footprint_y"][1]) / 2
    sp = sp.cut(cyl(px, py, z0 - 0.1, z1 + 0.1, 2.5))
    for p in P.GAS_PORTS.values():
        sp = sp.cut(cyl(p.xy[0], p.xy[1], z0 - 0.1, z1 + 0.1, 7.0))
    for (x, y) in P.STANDOFFS_HB + P.STANDOFFS_PEEK + P.MID_PILLARS:
        sp = sp.cut(cyl(x, y, z0 - 0.1, z1 + 0.1, 3.2))
    return sp


# ------------------------------------------------------------------------------------------------ press pad
def press_pad(dz=0.0):
    """Die-back press pad: grounded stainless stem + Al foot + 1 mm silicone (custom). Drawn at the nominal die."""
    fx, fy = P.PAD["footprint_x"], P.PAD["footprint_y"]
    cx, cy = (fx[0] + fx[1]) / 2, (fy[0] + fy[1]) / 2
    zc = P.PAD["contact_z"] + dz
    sil = box(fx[0], fx[1], fy[0], fy[1], zc, zc + 1.0)
    foot = box(fx[0], fx[1], fy[0], fy[1], zc + 1.0, zc + 3.0)
    stem = cyl(cx, cy, zc + 3.0, P.HB_Z1 + 1.5, P.PAD_STEM_D)
    collar = cyl(cx, cy, P.HB_Z1 + 1.5 - 0.0, P.HB_Z1 + 2.5, 7.4)
    stem2 = cyl(cx, cy, P.HB_Z1 + 2.5, P.SPRING_PLATE_Z[1] + 1.0, 2.0)
    spring = tube(cx, cy, P.HB_Z1 + 2.5, P.SPRING_PLATE_Z[0], 6.8, 5.2)
    return foot.union(stem).union(collar).union(stem2), sil, spring


# ------------------------------------------------------------------------------------------------ cylinder block
def cylinder_block_layers(routes):
    """Custom Al 6061 cylinder block in 4 layers (CNC): cover, air plate (rod guides, vias, galleries underneath),
    bore block (D6 bores), cap (return-spring seats, vents, V3 air groove)."""
    X0, X1 = P.CYL_BLOCK_X
    Y0, Y1 = P.CYL_BLOCK_Y
    lay = {}
    for name, (z0, z1) in P.CYL_LAYERS.items():
        lay[name] = box(X0, X1, Y0, Y1, z0, z1)
    cz0, cz1 = P.CYL_LAYERS["cover"]
    az0, az1 = P.CYL_LAYERS["air_plate"]
    bz0, bz1 = P.CYL_LAYERS["bore_block"]
    kz0, kz1 = P.CYL_LAYERS["cap"]
    for vid, c in IF.CYLINDERS.items():
        x, y = c["xy"]
        lay["cover"] = lay["cover"].cut(cyl(x, y, cz0 - 0.1, cz1 + 0.1, P.ROD_D + 0.5))
        lay["air_plate"] = lay["air_plate"].cut(cyl(x, y, az0 - 0.1, az1 + 0.1, P.ROD_D + 0.3))
        lay["air_plate"] = lay["air_plate"].cut(cyl(x, y, az1 - 1.5, az1 + 0.1, 3.2))   # rod seal + bush seat
        lay["bore_block"] = lay["bore_block"].cut(cyl(x, y, bz0 - 0.1, bz1 + 0.1, P.BORE_D))
        lay["cap"] = lay["cap"].cut(cyl(x, y, kz0 - 0.1, kz0 + 3.0, 4.0))                # return-spring seat
        lay["cap"] = lay["cap"].cut(cyl(x, y, kz0 - 0.1, kz1 + 0.1, 1.0))                # vent / sensing hole
    for vid, r in routes.items():
        vx, vy = r["via"]
        g = slab_from_poly(LineString(r["path"]).buffer(P.GALLERY_W / 2, cap_style=2, join_style=2), az0 - 0.01,
                           az0 + P.GALLERY_W)
        lay["air_plate"] = lay["air_plate"].cut(g).cut(cyl(vx, vy, az0 - 0.1, az1 + 0.1, 0.8))
        if vid == "V3":   # vertical passage to the cap and a groove to the V3 bore top
            lay["bore_block"] = lay["bore_block"].cut(cyl(vx, vy, bz0 - 0.1, bz1 + 0.1, 0.8))
            cx, cy = IF.CYLINDERS["V3"]["xy"]
            lay["cap"] = lay["cap"].cut(slab_from_poly(LineString([(vx, vy), (cx, cy)]).buffer(0.3, cap_style=2), kz0 - 0.01,
                                                       kz0 + 0.6))
    for (x, y) in P.STANDOFFS_HB + P.STANDOFFS_PEEK:
        lay["cover"] = lay["cover"].cut(cyl(x, y, cz0 - 0.1, cz1 + 0.1, 3.2))
        lay["air_plate"] = lay["air_plate"].cut(cyl(x, y, az0 - 0.1, az0 + 5.0, 2.5))
    return lay


def guide_ears():
    """Al ears under the cylinder block carrying the D6 guide pins (h6, hardened 1.2842) to the nest bushes."""
    out = []
    for name, (x, y) in P.GUIDE_PINS.items():
        ear = box(x - 4.0, x + 4.0, y - 4.0, y + 4.0, P.GUIDE_EAR_BOTTOM_Z, P.CYL_LAYERS["cover"][0])
        tip = P.GUIDE_PIN_TIP_Z
        pin = cyl(x, y, tip + P.GUIDE_PIN_NOSE, P.GUIDE_EAR_BOTTOM_Z + 8.0, P.GUIDE_PIN_D)
        nose = (cq.Workplane("XY").workplane(offset=tip).center(x, y)
                .circle(1.5).workplane(offset=P.GUIDE_PIN_NOSE).circle(P.GUIDE_PIN_D / 2).loft())
        out.append((name, ear, pin.union(nose)))
    return out


def pistons(state_lift=None):
    """Piston (PTFE-filled POM or Al with O-ring groove, custom) + NdFeB marker; returns per vid (piston, magnet,
    return-spring envelope). Rest position: pull pistons DOWN (pin closed), V3 piston UP (pin open)."""
    out = {}
    bz0, bz1 = P.CYL_LAYERS["bore_block"]
    for vid, c in IF.CYLINDERS.items():
        x, y = c["xy"]
        lift = (state_lift or {}).get(vid, 0.0)
        if vid == "V3":
            p0 = bz1 - P.PISTON_T - 1.0 - P.V3_STROKE + P.V3_STROKE - lift    # rest up
        else:
            p0 = bz0 + 0.5 + lift
        pist = cyl(x, y, p0, p0 + P.PISTON_T, P.BORE_D - 0.05)
        mag = cyl(x, y, p0 + P.PISTON_T, p0 + P.PISTON_T + P.PISTON_MAGNET["t"], P.PISTON_MAGNET["d"])
        spr = tube(x, y, p0 + P.PISTON_T + 0.2, P.CYL_LAYERS["cap"][0] + 3.0, 3.8, 3.0)
        out[vid] = (pist, mag, spr)
    return out


def hall_pcb():
    X0, X1 = P.CYL_BLOCK_X
    z0, z1 = P.HALL_PCB_Z
    pcb = box(-3.0, 79.0, 2.0, 48.0, z0, z1)
    sens = []
    for vid, c in IF.CYLINDERS.items():
        x, y = c["xy"]
        sens.append(box(x - 1.46, x + 1.46, y - 1.2, y + 1.2, z1, z1 + 1.1))   # DRV5055 SOT-23 (2.92 x 2.37)
    return pcb, union_all(sens)


def gallery_headers(routes):
    """Gallery headers (custom Al) on the rear (+y) and right (+x) faces with one D3 barb seat per channel."""
    az0, az1 = P.CYL_LAYERS["air_plate"]
    rear_x = [r["path"][-1][0] for r in routes.values() if r["exit"] == "+y"]
    rx0, rx1 = min(rear_x) - 3, max(rear_x) + 3
    rear = box(rx0, rx1, P.CYL_BLOCK_Y[1], P.CYL_BLOCK_Y[1] + 6.0, az0 - 1.0, az1)
    right_y = [r["path"][-1][1] for r in routes.values() if r["exit"] == "+x"]
    right = box(P.CYL_BLOCK_X[1], P.CYL_BLOCK_X[1] + 6.0, min(right_y) - 3, max(right_y) + 3, az0 - 1.0, az1)
    barbs = []
    for r in routes.values():
        ex, ey = r["path"][-1]
        if r["exit"] == "+y":
            barbs.append(cq.Workplane("XZ").workplane(offset=-(P.CYL_BLOCK_Y[1] + 6.0)).center(ex, az0 + 2.0)
                         .circle(0.9).extrude(-5.0))
        else:
            barbs.append(cq.Workplane("YZ").workplane(offset=P.CYL_BLOCK_X[1] + 6.0).center(ey, az0 + 2.0)
                         .circle(0.9).extrude(5.0))
    return rear, right, union_all(barbs)


# ------------------------------------------------------------------------------------------------ bridge, posts, cam
def bridge():
    """Head bridge (Al 6082, custom): takes the cam thrust at both x ends, carries the 4 guide posts and the
    pilot-valve manifolds (rear extension)."""
    z0, z1 = P.BRIDGE_Z
    b = box(P.BRIDGE_X[0], P.BRIDGE_X[1], 0.0, IF.CARD_W, z0, z1)
    b = b.cut(box(-6.0, 81.5, 3.0, 47.0, z0 - 0.1, z1 + 0.1))           # window over the Hall PCB (connectors)
    ext = box(0.0, 98.0, IF.CARD_W, IF.CARD_W + 52.0, z0, z0 + 4.0)    # manifold shelf
    b = b.union(ext)
    for (x, y) in P.HEAD_GUIDE_POSTS:
        b = b.cut(cyl(x, y, z0 - 0.1, z1 + 0.1, P.POST_D))
    spacers = union_all([box(x - 3, x + 3, y - 3, y + 3, P.CYL_Z1, z0) for (x, y) in
                         [(-7.0, 3.5), (-7.0, 46.5), (82.5, 3.5), (82.5, 46.5)]])
    return b, spacers


def posts(top_card_z):
    return [cyl(x, y, P.BRIDGE_Z[0], top_card_z, P.POST_D) for (x, y) in P.HEAD_GUIDE_POSTS]


def thrust_units(follower_top_card_z):
    """Thrust housing (on the bridge) + clamp-spring envelope + follower cap, at both x ends (card coords)."""
    out = []
    for x in P.CAM["x"]:
        y = P.CAM["y"]
        z0 = P.BRIDGE_Z[1]
        hous = tube(x, y, z0, z0 + 8.0, 19.0, 17.0).union(cyl(x, y, z0, z0 + 1.0, 19.0))
        cap_top = follower_top_card_z
        cap = cyl(x, y, cap_top - 8.0, cap_top, 16.8).cut(cyl(x, y, cap_top - 8.1, cap_top - 2.0, 14.4))
        spr = tube(x, y, z0 + 1.0, cap_top - 2.0, P.CLAMP_SPRING["OD"], P.CLAMP_SPRING["OD"] - 6.0)
        out.append((hous, cap, spr))
    return out


def manifolds():
    """2 x SMC SS073B01 bar manifold with S070B-5DG valves (envelopes, catalogue L1 = n x 7.2 + 14.8)."""
    z0 = P.BRIDGE_Z[0] + 4.0
    w, l, h = P.PILOT["envelope"]
    out = []
    for i, n in enumerate((11, 10)):
        L1 = P.PILOT["L1"](n)
        y0 = IF.CARD_W + 4.0 + i * (l + 1.0)
        out.append((f"ENV_SMC_SS073B01-{n:02d}C_S070B-5DG_x{n}", box(2.0, 2.0 + L1, y0, y0 + l, z0, z0 + h)))
    return out


def heaters_and_sensors():
    fx0, fx1 = P.HEATER_FIN["x"]
    fz0 = P.HEATER_FIN["z"][0] + 0.2
    h = [("ENV_heater_Omega_KHLVA-0502-5-P_front", box(fx0, fx0 + 50.8, -0.25, 0.0, fz0, fz0 + 12.7)),
         ("ENV_heater_Omega_KHLVA-0502-5-P_rear", box(fx0, fx0 + 50.8, IF.CARD_W, IF.CARD_W + 0.25, fz0,
                                                      fz0 + 12.7))]
    for name, (x, y, z) in P.SENSOR["positions"].items():
        h.append((f"ENV_Pt100_M222_{name}", box(x - 1.15, x + 1.15, y - 1.05, y + 1.05, z - 0.45, z + 0.45)))
    return h


# ------------------------------------------------------------------------------------------------ lid frame (DOCK)
def lid_frame():
    """Lid frame in DOCK coords, lid closed. Returns list of (name, solid, material)."""
    out = []
    zb = P.LID_BOTTOM_Z
    ys0, ys1 = P.SIDE_PLATE_Y
    hy, hz = P.HINGE["point"][1], P.HINGE["point"][2]
    for i, (x0, x1) in enumerate(P.SIDE_PLATE_X):
        sp = box(x0, x1, P.SIDE_PLATE_Y[0], P.LID_Y[1] - P.COVER_T - 0.5, zb, P.SIDE_PLATE_Z[1])
        knuckle = cq.Workplane("YZ").workplane(offset=x0).center(hy, hz).circle(5.0).extrude(x1 - x0)
        sp = sp.union(knuckle).cut(cq.Workplane("YZ").workplane(offset=x0 - 1).center(hy, hz).circle(3.0)
                                   .extrude(x1 - x0 + 2))
        # cam shaft bore
        sz = P.CAM["shaft_z_dock"]
        sy = IF.card_to_dock((0, P.CAM["y"]))[1]
        sp = sp.cut(cq.Workplane("YZ").workplane(offset=x0 - 1).center(sy, sz).circle(P.CAM["shaft_d"] / 2 + 0.05)
                    .extrude(x1 - x0 + 2))
        out.append((f"lid_side_plate_{'L' if i == 0 else 'R'}", sp, "aluminium"))
    xin0, xin1 = P.SIDE_PLATE_X[0][1], P.SIDE_PLATE_X[1][0]
    out.append(("lid_front_beam", box(xin0, xin1, P.SIDE_PLATE_Y[0], P.SIDE_PLATE_Y[0] + 8.0, 262.0, 287.0),
                "aluminium"))
    out.append(("lid_rear_beam", box(xin0, xin1, 184.0, 192.0, zb + 2.0, 194.0), "aluminium"))
    # post bearing blocks (fixed in the lid frame, flanged bushes inside)
    for (cx, cy) in P.HEAD_GUIDE_POSTS:
        X, Y, _ = IF.card_to_dock((cx, cy, 0))
        xa, xb = (xin0, X + 9.0) if X < 230 else (X - 9.0, xin1)
        blk = box(xa, xb, Y - 9.0, Y + 9.0, 263.0, 275.0).cut(cyl(X, Y, 262.0, 276.0, P.POST_D + 0.1))
        out.append((f"lid_post_block_{cx:.0f}_{cy:.0f}", blk, "aluminium"))
    return out


def cover():
    t = P.COVER_T
    x0, x1 = P.COVER_X
    y0, y1 = P.LID_Y
    zb, zt = P.LID_BOTTOM_Z, P.COVER_TOP_Z
    outer = box(x0, x1, y0, y1, zb, zt)
    inner = box(x0 + t, x1 - t, y0 + t, y1 - t, zb - 1, zt - t)
    c = outer.cut(inner)
    # side openings for the shaft and the hinge knuckles
    sy = IF.card_to_dock((0, P.CAM["y"]))[1]
    c = c.cut(cq.Workplane("YZ").workplane(offset=x0 - 1).center(sy, P.CAM["shaft_z_dock"]).circle(6.0)
              .extrude(x1 - x0 + 2))
    hy, hz = P.HINGE["point"][1], P.HINGE["point"][2]
    c = c.cut(box(x0 - 1, x1 + 1, hy - 10, y1 + 1, zb - 1, hz + 9))
    # umbilical hole in the rear wall
    ux, uy, uz = IF.PASS_THROUGHS["lid_umbilical"]["dock"]
    c = c.cut(cq.Workplane("XZ").workplane(offset=-(y1 + 1)).center(ux, uz + 12.0).circle(9.0).extrude(5.0))
    return c


def cam_parts(latched=True):
    """Cam shaft (D10 1.4305), two eccentrics (e 4.5, R 10), lever (right, outside the side plate)."""
    sy = IF.card_to_dock((0, P.CAM["y"]))[1]
    sz = P.CAM["shaft_z_dock"]
    x0, x1 = P.SIDE_PLATE_X[0][0], P.COVER_X[1] + 2.0
    shaft = cq.Workplane("YZ").workplane(offset=x0).center(sy, sz).circle(P.CAM["shaft_d"] / 2).extrude(x1 - x0)
    e = P.CAM["e"]
    ez = sz - e if latched else sz + e
    eccs = []
    for cx in P.CAM["x"]:
        X = IF.card_to_dock((cx, 0))[0]
        eccs.append(cq.Workplane("YZ").workplane(offset=X - P.CAM["w"] / 2).center(sy, ez).circle(P.CAM["R"])
                    .extrude(P.CAM["w"]))
    lx0 = P.COVER_X[1] + 0.5
    ang = math.pi if latched else 0.0       # lever points -Y (front) when latched
    ly, lz = sy + P.CAM["lever_L"] * math.cos(ang), sz
    lever = (cq.Workplane("YZ").workplane(offset=lx0).polyline([(sy, sz - 4), (ly, lz - 3), (ly, lz + 3),
                                                                 (sy, sz + 4)]).close().extrude(3.0))
    knob = cq.Workplane("YZ").workplane(offset=lx0).center(ly, lz).circle(6.0).extrude(3.5)
    return shaft, union_all(eccs), lever.union(knob)


def hinge_parts():
    """Fixed hinge blocks (custom Al, bolt to the base hinge rail -- ICR-U3) with D8 pins and the 85 deg stops."""
    hy, hz = P.HINGE["point"][1], P.HINGE["point"][2]
    out = []
    for x0, x1 in ((150.0, 153.8), (316.2, 320.0)):
        blk = box(x0, x1, hy - 10.0, 200.0, 160.0, hz + 9.0)
        blk = blk.cut(cq.Workplane("YZ").workplane(offset=x0 - 1).center(hy, hz).circle(3.0).extrude(6.0))
        out.append((f"hinge_block_{'L' if x0 < 200 else 'R'}", blk, "aluminium"))
    pin = cq.Workplane("YZ").workplane(offset=150.0).center(hy, hz).circle(3.0).extrude(170.0)
    out.append(("hinge_pin_D6", pin, "steel"))
    return out


def handle_and_latches():
    out = []
    y0 = P.LID_Y[0]
    h = box(205.0, 250.0, y0 - 20.0, y0 - 14.0, 240.0, 248.0)
    h = h.union(box(205.0, 211.0, y0 - 20.0, y0, 240.0, 248.0)).union(box(244.0, 250.0, y0 - 20.0, y0, 240.0, 248.0))
    out.append(("lid_handle", h, "steel"))
    for x0 in (P.LATCH["x_dock"][0], P.LATCH["x_dock"][1] - P.LATCH["W"]):
        env = box(x0, x0 + P.LATCH["W"], y0 - P.LATCH["H"], y0, P.LID_BOTTOM_Z, P.LID_BOTTOM_Z + P.LATCH["L"])
        out.append((f"ENV_latch_Kipp_K0045.1541092_X{x0:.0f}", env, "envelope"))
    return out


def latch_keepout_lower():
    """NOT an UPPER part: keep-out for the catch plates the LOWER agent must provide (ICR-U2), drawn for reference."""
    y0 = P.LID_Y[0]
    return [box(x0, x0 + P.LATCH["W"], y0 - P.LATCH["H"], y0, 161.0, 176.0)
            for x0 in (P.LATCH["x_dock"][0], P.LATCH["x_dock"][1] - P.LATCH["W"])]


def lid_switch_and_umbilical():
    sy = IF.card_to_dock((0, P.CAM["y"]))[1]
    sw = box(299.0, 305.0, sy + 4.0, sy + 16.8, P.CAM["shaft_z_dock"] + 5.0, P.CAM["shaft_z_dock"] + 11.5)
    ux, uy, uz = IF.PASS_THROUGHS["lid_umbilical"]["dock"]
    clamp = box(ux - 12, ux + 12, P.LID_Y[1] - 10.0, P.LID_Y[1] - P.COVER_T, uz + 5.0, uz + 22.0)
    bundle = cq.Workplane("XZ").workplane(offset=-P.LID_Y[1]).center(ux, uz + 12.0).circle(7.0).extrude(40.0)
    return [("ENV_lid_switch_Omron_D2F-class", sw, "envelope"), ("umbilical_clamp", clamp, "aluminium"),
            ("ENV_umbilical_bundle_D14", bundle, "envelope")]
