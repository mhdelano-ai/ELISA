"""DOCK LOWER parts as CadQuery solids, CARD coordinates (z = 0 anvil top). Custom parts are real machinable solids;
catalogue parts are labelled envelopes (kind = 'catalogue'/'envelope'). Numbers come from geom.py / interface.py."""
from __future__ import annotations

import math

import cadquery as cq

from .. import common as C
from .. import interface as I
from . import geom as G


def _poly_cut(wp, poly, z0, h):
    """Cut a shapely polygon (or multipolygon) prism z0..z0+h from wp."""
    geoms = getattr(poly, "geoms", [poly])
    for g in geoms:
        s = C.polygon_solid(list(g.exterior.coords), z0, h)
        for hole in g.interiors:
            s = s.cut(C.polygon_solid(list(hole.coords), z0 - 1, h + 2))
        wp = wp.cut(s)
    return wp


def _poly_solid(poly, z0, h):
    geoms = getattr(poly, "geoms", [poly])
    out = None
    for g in geoms:
        s = C.polygon_solid(list(g.exterior.coords), z0, h)
        for hole in g.interiors:
            s = s.cut(C.polygon_solid(list(hole.coords), z0 - 1, h + 2))
        out = s if out is None else out.union(s)
    return out


def cyl(x, y, z0, h, d):
    return cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(d / 2).extrude(h)


def boxc(x0, y0, z0, x1, y1, z1):
    return C.box_from_corners((x0, y0, z0), (x1, y1, z1))


# ------------------------------------------------------------------------------------------------ card envelope
def card_envelope():
    """Card envelope from interface.py only (the CARD agent's model replaces it in the integrated assembly,
    docs/23); (revised at integration) with the Rev B poka-yoke chamfer, so the nest corner block is checked."""
    env = C.rounded_rect(I.CARD_L / 2, I.CARD_W / 2, I.CARD_L, I.CARD_W, I.CARD_CORNER_R, 0.0, I.CARD_T)
    cx, cy = I.CARD_POKA_CHAMFER["corner"]
    leg = I.CARD_POKA_CHAMFER["leg"]
    tri = cq.Workplane("XY").workplane(offset=-1).polyline([(cx - leg, cy), (cx + 1, cy), (cx + 1, cy + 1), (cx, cy + 1),
                                                            (cx, cy - leg)]).close().extrude(I.CARD_T + 2)
    tri = tri.union(cq.Workplane("XY").workplane(offset=-1).polyline([(cx - leg, cy), (cx, cy - leg), (cx, cy)])
                    .close().extrude(I.CARD_T + 2))
    return env.cut(tri)


# ------------------------------------------------------------------------------------------------ anvil
def anvil():
    x0, x1 = G.ANVIL_X
    y0, y1 = G.ANVIL_Y
    a = boxc(x0, y0, -G.ANVIL_T, x1, y1, 0.0)
    # cold-zone cut-out (PEEK break frame + cold plate sit in it)
    cc = G.COLD_CUTOUT
    a = a.cut(boxc(cc["x"][0], cc["y"][0], -G.ANVIL_T - 1, cc["x"][1], cc["y"][1], 1))
    # bottom pocket -> 5 mm thin plate over the magnet bay
    a = _poly_cut(a, G.pocket_poly(), -G.ANVIL_T - 1, G.ANVIL_T - G.T_THIN + 1)
    # through openings: windows, slot, contact opening
    a = _poly_cut(a, G.through_openings(), -G.ANVIL_T - 1, G.ANVIL_T + 2)
    # M_w recess
    a = _poly_cut(a, G.mw_recess_poly(), -I.M_W_RECESS["depth"], I.M_W_RECESS["depth"] + 1)
    # port bores (inserts) D3.3 through the thick zones
    for k in G.ANVIL_PORTS:
        x, y = I.PORTS[k].xy
        a = a.cut(cyl(x, y, -G.ANVIL_T - 1, G.ANVIL_T + 2, G.PORT_BORE_D))
    # head guide bushes
    for (x, y) in G.GUIDE_BUSH["pins"]:
        a = a.cut(cyl(x, y, -G.ANVIL_T - 1, G.ANVIL_T + 2, G.GUIDE_BUSH["bush_od"]))
    # drip gutter ring + drains
    g = G.GUTTER
    o = g["inner_offset"]
    from shapely.geometry import box as sbox
    ring = sbox(-o - g["w"], -o - g["w"], I.CARD_L + o + g["w"], I.CARD_W + o + g["w"]).difference(
        sbox(-o, -o, I.CARD_L + o, I.CARD_W + o))
    ring = ring.difference(sbox(G.COLD_CUTOUT["x"][0] - 0.01, G.COLD_CUTOUT["y"][0], G.COLD_CUTOUT["x"][1],
                                G.COLD_CUTOUT["y"][1]))
    a = _poly_cut(a, ring, -g["depth"], g["depth"] + 1)
    for (x, y) in g["drains"]:
        a = a.cut(cyl(x, y, -G.ANVIL_T - 1, G.ANVIL_T + 2, g["drain_d"]))
    # dowel/locating holes on the support posts (D6 H7) and M4 clearance (4 posts)
    for (x, y) in G.BEAM_DOWELS:
        a = a.cut(cyl(x, y, -G.ANVIL_T - 1, 7.0, 4.0))
    return a


def anvil_heaters():
    out = []
    keep = [boxc(b[0] - 1, b[1] - 1, -20, b[3] + 1, b[4] + 1, -14) for b in G.BAY_BEAMS.values()]
    keep += [cyl(x, y, -20, 6, 5.0) for (x, y) in G.GUTTER["drains"]]
    for cx in (I.IC1.center[0],):   # M_c bracket plates under the anvil edges
        keep += [boxc(cx - 13, G.ANVIL_Y[1] - 7, -20, cx + 13, G.ANVIL_Y[1] + 1, -14),
                 boxc(cx - 13, G.ANVIL_Y[0] - 1, -20, cx + 13, G.ANVIL_Y[0] + 7, -14)]
    keep += [cyl(x, y, -20, 6, G.GUIDE_BUSH["bush_od"] + 1) for (x, y) in G.GUIDE_BUSH["pins"]]
    for k in G.ANVIL_PORTS:
        keep.append(cyl(*I.PORTS[k].xy, -20, 6, 6.0))
    for k, (x0, y0, x1, y1) in G.ANVIL_HEATERS.items():
        h = boxc(x0, y0, -G.ANVIL_T - G.HEATER_T, x1, y1, -G.ANVIL_T)
        for kk in keep:
            h = h.cut(kk)
        out.append((k, h))
    return out


def m_w_magnet():
    s = I.MAGNETS["M_w"]["size"]
    c = I.M_W_RECESS["center"]
    zt = I.MAGNETS["M_w"]["z_top"]
    return boxc(c[0] - s[0] / 2, c[1] - s[1] / 2, zt - s[2], c[0] + s[0] / 2, c[1] + s[1] / 2, zt)


# ------------------------------------------------------------------------------------------------ inserts, seals
def port_insert(k):
    x, y = I.PORTS[k].xy
    zt = G.INSERT["top_z"] if k in G.ANVIL_PORTS else G.INSERT["top_z"]
    zb = G.INSERT["bottom_z"] if k in G.ANVIL_PORTS else G.COLD_BODY_Z[0]
    s = cyl(x, y, zb, zt - zb, G.INSERT["d"] - 0.01)
    s = s.cut(cyl(x, y, zb - 1, zt - zb + 2, G.INSERT["tube_bore"]))
    # 0.3 x 45 deg chamfer at the bottom (insertion from below) -- simplified as a step
    return s


def gasket(k):
    x, y = I.PORTS[k].xy
    zb = G.INSERT["top_z"]
    s = cyl(x, y, zb, G.GASKET["gasket_t"], G.GASKET["gasket_od"] - 0.01)
    return s.cut(cyl(x, y, zb - 1, 3, G.GASKET["gasket_id"]))


def retainer(name):
    x0, y0, x1, y1 = G.RETAINERS[name]
    r = boxc(x0, y0, -G.ANVIL_T - G.RETAINER_T, x1, y1, -G.ANVIL_T)
    for k in G.ANVIL_PORTS:
        x, y = I.PORTS[k].xy
        if x0 < x < x1 and y0 < y < y1:
            r = r.cut(cyl(x, y, -G.ANVIL_T - G.RETAINER_T - 1, G.RETAINER_T + 2, 2.0))
    return r


def tube_solid(port, z_from=None):
    """1/16 in tube along the route; union of cylinders (sampled)."""
    pts = G.tube_route(port)
    if z_from is not None:
        pts = [(pts[0][0], pts[0][1], z_from)] + pts[1:]
    # (revised at integration) compound of cylinders + joint spheres, no Boolean fuse: same geometry for checks and
    # renders, ~5x smaller STEP (docs/23 §3.4)
    solids = []
    r = G.TUBE_OD / 2
    for i, (p, q) in enumerate(zip(pts[:-1], pts[1:])):
        v = cq.Vector(q[0] - p[0], q[1] - p[1], q[2] - p[2])
        L = v.Length
        if L < 1e-6:
            continue
        solids.append(cq.Solid.makeCylinder(r, L, cq.Vector(*p), v.normalized()))
        if i < len(pts) - 2:
            solids.append(cq.Solid.makeSphere(r, cq.Vector(*q), angleDegrees1=-90, angleDegrees2=90))
    return cq.Workplane("XY").add(cq.Compound.makeCompound(solids))


# ------------------------------------------------------------------------------------------------ nest frame
def nest_frame():
    x0, x1 = G.ANVIL_X
    y0, y1 = G.ANVIL_Y
    f = boxc(x0, y0, 0.0, x1, y1, G.NEST_T)
    o = G.NEST_OPEN
    c = G.NEST_CHAMFER
    # opening with 45 deg lead-in (loft from the opening at z NEST_T-c to the enlarged opening at the top)
    f = f.cut(boxc(o["x"][0], o["y"][0], -1, o["x"][1], o["y"][1], G.NEST_T + 1))
    lead = (cq.Workplane("XY").workplane(offset=G.NEST_T - c)
            .center(0.5 * sum(o["x"]), 0.5 * sum(o["y"])).rect(o["x"][1] - o["x"][0], o["y"][1] - o["y"][0])
            .workplane(offset=c + 0.01).rect(o["x"][1] - o["x"][0] + 2 * c + 0.02, o["y"][1] - o["y"][0] + 2 * c + 0.02)
            .loft())
    f = f.cut(lead)
    # datum pin bores (pins are pressed into half-open reamed bores in the frame wall)
    for (x, y) in I.DATUM_A_PINS + [I.DATUM_B_PIN]:
        f = f.cut(cyl(x, y, -1, G.NEST_T + 2, I.DATUM_PIN_D))
    # pusher bores
    pa = I.PUSHERS["push_A"]["contact"]
    f = f.cut(cq.Workplane("XZ").workplane(offset=-(o["y"][1] - 0.01)).center(pa[0], G.PUSHER["z"])
              .circle(G.PUSHER["body_d"] / 2).extrude(-G.PUSHER["body_len"]))
    pb = I.PUSHERS["push_B"]["contact"]
    f = f.cut(cq.Workplane("YZ").workplane(offset=o["x"][1] - 0.01).center(pb[1], G.PUSHER["z"])
              .circle(G.PUSHER["body_d"] / 2).extrude(G.PUSHER["body_len"]))
    # guide bush bores, card-presence sensor pocket
    for (x, y) in G.GUIDE_BUSH["pins"]:
        f = f.cut(cyl(x, y, -1, G.NEST_T + 2, G.GUIDE_BUSH["bush_od"]))
    cx, cy = G.CARD_PRESENCE["xy"]
    sx, sy, sz = G.CARD_PRESENCE["size"]
    f = f.cut(boxc(cx - sx / 2, cy - sy / 2, G.CARD_PRESENCE["z"] - sz / 2, o["x"][0] + 0.01, cy + sy / 2,
                   G.CARD_PRESENCE["z"] + sz / 2))
    return f.union(poka_block())


def poka_block():
    """(revised at integration) Nest corner block matching the card's 4 x 45 deg poka-yoke chamfer at (75.5, 50)
    (interface CARD_POKA_CHAMFER, NEST_POKA_BLOCK): face 0.3 clear of the chamfer, z 0.2-5.0, 1.5 lead-in at the top.
    A card in any of the three wrong orientations lands on it (its full corner is where the chamfer should be)."""
    cx, cy = I.CARD_POKA_CHAMFER["corner"]
    leg = I.CARD_POKA_CHAMFER["leg"]
    c0 = cx + cy - leg + I.NEST_POKA_BLOCK["clear"] * math.sqrt(2.0)       # x + y of the block face
    z0, z1 = I.NEST_POKA_BLOCK["z"]
    li = I.NEST_POKA_BLOCK["lead_in"]
    xm, ym = G.NEST_OPEN["x"][1] + 2.0, G.NEST_OPEN["y"][1] + 2.0          # 2 mm into the frame wall

    def tri(c):
        return [(c - ym, ym), (xm, ym), (xm, c - xm)]
    low = cq.Workplane("XY").workplane(offset=z0).polyline(tri(c0)).close().extrude(z1 - li - z0)
    top = (cq.Workplane("XY").workplane(offset=z1 - li).polyline(tri(c0)).close()
           .workplane(offset=li).polyline(tri(c0 + li * math.sqrt(2.0))).close().loft())
    return low.union(top)


def latch_brackets():
    """(revised at integration) Two Al brackets on the anvil front face carrying the Kipp K0045.9143372 catch plates
    of the lid draw latches (interface LID_LATCH keep-outs; catch-plate envelope UNVERIFIED)."""
    out = []
    for i, b in enumerate(G.LATCH_BRACKETS):
        x0, x1 = b["x"]
        y0, y1 = b["y"]
        fy0, fz0, fz1 = b["flange"]
        br = boxc(x0, y0, b["shelf_z"][0], x1, y1, b["shelf_z"][1])
        br = br.union(boxc(x0, fy0, fz0, x1, y1, fz1))
        cat = boxc(x0 + 1.0, b["catch"]["y"][0], b["catch"]["z"][0], x1 - 1.0, b["catch"]["y"][1], b["catch"]["z"][1])
        out.append((f"latch_bracket_{i + 1}", br, "aluminium", "custom"))
        out.append((f"latch_catch_plate_env_{i + 1}", cat, "steel", "catalogue"))
    return out


def hinge_pedestals():
    """(revised at integration) Two Al pedestals on the bay base plate carrying the UPPER hinge blocks at dock Z 160
    (interface HINGE_SUPPORT)."""
    out = []
    for i, (p0, p1) in enumerate(G.HINGE_PEDESTALS):
        out.append((f"hinge_pedestal_{'L' if i == 0 else 'R'}", boxc(*p0, *p1), "aluminium", "custom"))
    return out


def datum_pins():
    return [(f"datum_pin_{n}", cyl(x, y, G.DATUM_PIN_Z[0], G.DATUM_PIN_Z[1] - G.DATUM_PIN_Z[0], I.DATUM_PIN_D))
            for n, (x, y) in zip(("A1", "A2", "B"), I.DATUM_A_PINS + [I.DATUM_B_PIN])]


def pushers(card_present=True):
    o = G.NEST_OPEN
    out = []
    pa = I.PUSHERS["push_A"]["contact"]
    tip_y = I.CARD_W if card_present else I.CARD_W - G.PUSHER["stroke"]
    body = (cq.Workplane("XZ").workplane(offset=-(o["y"][1])).center(pa[0], G.PUSHER["z"])
            .circle(G.PUSHER["body_d"] / 2 - 0.05).extrude(-G.PUSHER["body_len"]))
    tip = (cq.Workplane("XZ").workplane(offset=-tip_y).center(pa[0], G.PUSHER["z"])
           .circle(G.PUSHER["tip_d"] / 2).extrude(-(o["y"][1] - tip_y)))
    out.append(("pusher_A", body.union(tip)))
    pb = I.PUSHERS["push_B"]["contact"]
    tip_x = I.CARD_L if card_present else I.CARD_L - G.PUSHER["stroke"]
    body = (cq.Workplane("YZ").workplane(offset=o["x"][1]).center(pb[1], G.PUSHER["z"])
            .circle(G.PUSHER["body_d"] / 2 - 0.05).extrude(G.PUSHER["body_len"]))
    tip = (cq.Workplane("YZ").workplane(offset=tip_x).center(pb[1], G.PUSHER["z"])
           .circle(G.PUSHER["tip_d"] / 2).extrude(o["x"][1] - tip_x))
    out.append(("pusher_B", body.union(tip)))
    return out


def guide_bushes():
    out = []
    for n, (x, y) in enumerate(G.GUIDE_BUSH["pins"]):
        b = cyl(x, y, -G.GUIDE_BUSH["bush_len"], G.GUIDE_BUSH["bush_len"] + G.NEST_T, G.GUIDE_BUSH["bush_od"] - 0.01)
        b = b.cut(cyl(x, y, -G.ANVIL_T - 1, G.ANVIL_T + 10, G.GUIDE_BUSH["pin_d"]))
        out.append((f"guide_bush_{n + 1}", b))
    return out


def card_presence_sensor():
    cx, cy = G.CARD_PRESENCE["xy"]
    sx, sy, sz = G.CARD_PRESENCE["size"]
    return boxc(cx - sx / 2, cy - sy / 2, G.CARD_PRESENCE["z"] - sz / 2, cx + sx / 2 - 0.2, cy + sy / 2,
                G.CARD_PRESENCE["z"] + sz / 2)


# ------------------------------------------------------------------------------------------------ cold zone
def peek_break_frame():
    cc = G.COLD_CUTOUT
    cp = G.COLD_PLATE
    f = boxc(cc["x"][0] + 0.01, cc["y"][0] + 0.01, -G.ANVIL_T, cc["x"][1] - 0.01, cc["y"][1] - 0.01, 0.0)
    f = f.cut(boxc(cp["x"][0], cp["y"][0], -G.ANVIL_T - 1, cp["x"][1], cp["y"][1], 1))
    return f


def cold_block():
    cp = G.COLD_PLATE
    b = boxc(cp["x"][0] + 0.01, cp["y"][0] + 0.01, G.COLD_BODY_Z[0], cp["x"][1] - 0.01, cp["y"][1] - 0.01, 0.0)
    s = G.COLD_SPREADER
    b = b.union(boxc(s["x"][0], s["y"][0], s["z"][0], s["x"][1], s["y"][1], s["z"][1]))
    for k in G.COLD_PORTS:
        x, y = I.PORTS[k].xy
        b = b.cut(cyl(x, y, G.COLD_BODY_Z[0] - 1, -G.COLD_BODY_Z[0] + 2, G.PORT_BORE_D))
    # thermistor well D2 x 15 from below under RCj
    b = b.cut(cyl(8.0, 38.0, G.COLD_BODY_Z[0] - 1, 21.0, 2.0))
    return b


def peltier():
    p = G.PELTIER
    z1 = G.COLD_SPREADER["z"][0]
    return boxc(p["x"][0], p["y"][0], z1 - p["t"], p["x"][1], p["y"][1], z1)


def heatsink():
    h = G.HEATSINK
    zt = G.COLD_SPREADER["z"][0] - G.PELTIER["t"]
    base = boxc(h["x"][0], h["y"][0], zt - h["base_t"], h["x"][1], h["y"][1], zt)
    n = 9
    pitch = (h["x"][1] - h["x"][0]) / n
    for i in range(n):
        xf = h["x"][0] + (i + 0.3) * pitch
        base = base.union(boxc(xf, h["y"][0], h["fin_to"], xf + 0.4 * pitch, h["y"][1], zt - h["base_t"]))
    return base


def fan():
    f = G.FAN
    s = boxc(f["x"][0], f["y"][0], f["z"][0], f["x"][1], f["y"][1], f["z"][1])
    cx, cz = 0.5 * sum(f["x"]), 0.5 * sum(f["z"])
    return s.cut(cq.Workplane("XZ").workplane(offset=-f["y"][1] - 1).center(cx, cz).circle(11).extrude(-(f["y"][1] - f["y"][0]) - 2))


def duct():
    d = G.DUCT
    s = boxc(d["x"][0], d["y"][0], d["z"][0], d["x"][1], d["y"][1], d["z"][1])
    return s.cut(boxc(d["x"][0] + 1, d["y"][0] - 1, d["z"][0] + 1, d["x"][1] - 1, d["y"][1] + 1, d["z"][1] - 1))


def foam_shell():
    """Closed-cell foam round the cold block (sides and below the anvil), cut where the module/heatsink sit."""
    cp = G.COLD_PLATE
    t = G.FOAM_T
    outer = boxc(cp["x"][0] - t - 2, cp["y"][0] - t + 1, G.COLD_BODY_Z[0] - 0.0, cp["x"][1], cp["y"][1] + t - 1,
                 -G.ANVIL_T - G.HEATER_T - 0.01)
    inner = boxc(cp["x"][0] - 0.01, cp["y"][0] - 0.01, G.COLD_BODY_Z[0] - 1, cp["x"][1] + 1, cp["y"][1] + 0.01, 0)
    s = G.COLD_SPREADER
    sp = boxc(s["x"][0] - 0.5, s["y"][0] - 0.5, s["z"][0] - 1, s["x"][1] + 1, s["y"][1] + 0.5, s["z"][1] + 0.5)
    f = outer.cut(inner).cut(sp)
    for k in G.COLD_PORTS:
        x, y = I.PORTS[k].xy
        f = f.cut(cyl(x, y, -60, 60, 2.2))
    return f


# ------------------------------------------------------------------------------------------------ bay frame
BASE_PLATE_Z = (G.BAY_BASE[2], G.BAY_BASE[5])


def bay_frame():
    b = G.BAY_BASE
    bp = boxc(*b[:3], *b[3:])
    for w in list(G.BAY_WALLS.values()) + list(G.BAY_BEAMS.values()):
        bp = bp.union(boxc(*w[:3], *w[3:]))
    for (x, y) in G.BEAM_DOWELS:
        bp = bp.union(cyl(x, y, -G.ANVIL_T, 6.0, 3.98))      # lift-off dowels into the anvil
    # holes for tubes and the Gamry cable through the walls (D4 / D7)
    for k in G.TUBE_PORTS:   # open-top U-slots 4 wide: the anvil module lifts out with its tubes (CHOICE-L15)
        e = G.tube_route(k)[-1]
        x0 = e[0] - 10 if e[0] > 0 else e[0] - 1
        bp = bp.cut(boxc(x0, e[1] - 2.0, e[2], x0 + 12, e[1] + 2.0, -14.0))
        bp = bp.cut(cq.Workplane("YZ").workplane(offset=x0).center(e[1], e[2]).circle(2.0).extrude(12))
    bp = bp.cut(cq.Workplane("YZ").workplane(offset=G.TUBE_EXIT["E"] - 10).center(
        I.dock_to_card(G.GAMRY_BULKHEAD)[1], I.dock_to_card(G.GAMRY_BULKHEAD)[2]).circle(3.5).extrude(12))
    # (revised at integration) mounting to the BASE deck: 6 x M6 counterbored (D6.6 / D11 x 1.5) + 2 dowel holes D6
    for (x, y) in G.MOUNT_BOLTS:
        bp = bp.cut(cyl(x, y, b[2] - 1, 6.0, 6.6)).cut(cyl(x, y, b[5] - 1.5, 2.0, 11.0))
    for (x, y) in G.MOUNT_DOWELS:
        bp = bp.cut(cyl(x, y, b[2] - 1, 6.0, 6.0))
    return bp


# ------------------------------------------------------------------------------------------------ M_c units
def _mc_moving_up(unit):
    """Carrier parts (move with the parallelogram) in the UP state for unit 1; unit 2 mirrored about y = 25."""
    cx, cy = I.IC1.center
    h = G.MC_HOLDER
    fx, fy, ft = G.MC_FLANGE
    m = G.MC_MAG
    zt = G.MC_TOP_UP
    holder = boxc(cx - h[0] / 2, cy - h[1] / 2, G.Z_THIN_BOTTOM, cx + h[0] / 2, cy + h[1] / 2, zt)
    holder = holder.union(boxc(cx - fx / 2, cy - fy / 2, G.Z_THIN_BOTTOM - ft, cx + fx / 2, cy + fy / 2, G.Z_THIN_BOTTOM))
    holder = holder.cut(boxc(cx - m[0] / 2 - 0.02, cy - m[1] / 2 - 0.02, zt - m[2], cx + m[0] / 2 + 0.02,
                             cy + m[1] / 2 + 0.02, zt + 1))
    magnet = boxc(cx - m[0] / 2, cy - m[1] / 2, zt - m[2], cx + m[0] / 2, cy + m[1] / 2, zt)
    zc0 = G.Z_THIN_BOTTOM - ft
    zl = G.MC_LINK_Z
    col = boxc(cx - G.MC_COLUMN[0] / 2, cy - G.MC_COLUMN[1] / 2, zl[1] - 3.0, cx + G.MC_COLUMN[0] / 2,
               cy + G.MC_COLUMN[1] / 2, zc0)
    parts = [("Mc_holder", holder, "aluminium"), ("Mc_magnet", magnet, "NdFeB"), ("Mc_carrier", col, "aluminium")]
    if unit == 2:
        parts = [(n, s.mirror("XZ", (0, I.CARD_W / 2, 0)), mat) for n, s, mat in parts]
    return parts


def _mc_link(unit, zl, theta):
    """One parallelogram link (bar 3 thick in x on each side of the carrier) rotated by theta about its frame pivot."""
    cx, cy = I.IC1.center if unit == 1 else I.IC2.center
    s = 1 if unit == 1 else -1
    yp = cy + s * G.MC_R
    bars = None
    for xside in (-1, 1):
        x0 = cx + xside * (G.MC_COLUMN[0] / 2 + 0.5)
        x1 = x0 + xside * 3.0
        b = boxc(min(x0, x1), min(cy, yp) - 2.5, zl - 2.5, max(x0, x1), max(cy, yp) + 2.5, zl + 2.5)
        bars = b if bars is None else bars.union(b)
    ang = theta if unit == 1 else -theta
    return bars.rotate((cx, yp, zl), (cx + 1, yp, zl), ang)


def mc_unit(unit, theta):
    """All parts of one M_c unit at swing angle theta (deg): list of (name, solid, material, kind)."""
    dy, dz = G.mc_offset(theta, unit)
    out = []
    for n, s, mat in _mc_moving_up(unit):
        out.append((f"Mc{unit}_{n[3:]}", s.translate((0, dy, dz)), mat, "custom" if mat != "NdFeB" else "catalogue"))
    for i, zl in enumerate(G.MC_LINK_Z):
        out.append((f"Mc{unit}_link_{'upper' if i == 0 else 'lower'}", _mc_link(unit, zl, theta), "aluminium", "custom"))
    # fixed bracket with the two frame pivots and the worm drive (envelope)
    cx, cy = I.IC1.center if unit == 1 else I.IC2.center
    s = 1 if unit == 1 else -1
    yp = cy + s * G.MC_R
    y_in = G.ANVIL_Y[1] - 6.0 if unit == 1 else G.ANVIL_Y[0] + 6.0   # bolted under the anvil edge
    ya, yb = sorted((y_in, yp + s * 2.5))
    br = None
    for xa, xb in ((cx - 12.0, cx - 7.5), (cx + 7.5, cx + 12.0)):
        pl = boxc(xa, ya, G.MC_LINK_Z[1] - 10.0, xb, yb, -G.ANVIL_T)
        yo0, yo1 = sorted((G.ANVIL_Y[1] if unit == 1 else G.ANVIL_Y[0], yp + s * 2.5))
        pl = pl.union(boxc(xa, yo0, G.MC_LINK_Z[1] - 10.0, xb, yo1, G.MC_LINK_Z[0] + 8.0))
        br = pl if br is None else br.union(pl)
    out.append((f"Mc{unit}_bracket", br, "aluminium", "custom"))
    dsx, dsy, dsz = G.MC_DRIVE["size"]
    yd0, yd1 = sorted((yp + s * 2.5, yp - s * (dsy - 2.5)))
    drv = boxc(cx + 12.0, yd0, G.MC_LINK_Z[0] - dsz / 2, cx + 12.0 + dsx, yd1, G.MC_LINK_Z[0] + dsz / 2)
    out.append((f"Mc{unit}_drive_env", drv, "envelope", "envelope"))
    shaft = (cq.Workplane("YZ").workplane(offset=cx - 12.0).center(yp, G.MC_LINK_Z[0]).circle(2.0).extrude(24.0))
    shaft = shaft.union(cq.Workplane("YZ").workplane(offset=cx - 12.0).center(yp, G.MC_LINK_Z[1]).circle(2.0)
                        .extrude(24.0))
    out.append((f"Mc{unit}_pivot_shafts", shaft, "steel", "catalogue"))
    return out


# ------------------------------------------------------------------------------------------------ M_d system
def md_moving(xy, up=True):
    """M_d holder + magnet + post + Z unit (post carrier) at plan position xy; up or lowered by z_stroke."""
    x, y = xy
    dz = 0.0 if up else -G.MD_STROKE
    h = G.MD_HOLDER
    m = G.MD_MAG
    zt = G.MD_TOP_UP + dz
    holder = boxc(x - h[0] / 2, y - h[1] / 2, G.MD_HOLDER_Z[0] + dz, x + h[0] / 2, y + h[1] / 2, zt)
    holder = holder.cut(boxc(x - m[0] / 2 - 0.02, y - m[1] / 2 - 0.02, zt - m[2], x + m[0] / 2 + 0.02, y + m[1] / 2 + 0.02, zt + 1))
    magnet = boxc(x - m[0] / 2, y - m[1] / 2, zt - m[2], x + m[0] / 2, y + m[1] / 2, zt)
    neck = cyl(x, y, G.MD_NECK["z"][0] + dz, G.MD_NECK["z"][1] - G.MD_NECK["z"][0], G.MD_NECK["d"])
    post = cyl(x, y, G.MD_POST["z"][0] + dz - 10.0, G.MD_POST["z"][1] - G.MD_POST["z"][0] + 10.0, G.MD_POST["d"])
    post = post.union(neck)
    return [("Md_holder", holder, "PEEK", "custom"), ("Md_magnet", magnet, "NdFeB", "catalogue"),
            ("Md_post", post, "steel", "custom")]


def md_carriage(xy):
    """Z unit (moves with X-Y, not with Z) + umbrella."""
    x, y = xy
    hz = G.MD_ZUNIT["half"]
    z0, z1 = G.MD_ZUNIT["z"]
    zu = boxc(x - hz, y - hz, z0, x + hz, y + hz, z1 - 2.0)
    zu = zu.cut(cyl(x, y, z1 - 12, 14, G.MD_POST["d"] + 0.4))
    um = boxc(x - G.MD_ZUNIT["umbrella"] / 2, y - G.MD_ZUNIT["umbrella"] / 2, z1 - 2.0, x + G.MD_ZUNIT["umbrella"] / 2,
              y + G.MD_ZUNIT["umbrella"] / 2, z1)
    um = um.cut(cyl(x, y, z1 - 3, 4, G.MD_POST["d"] + 0.6))
    return [("Md_Zunit", zu, "aluminium", "custom"), ("Md_umbrella", um, "PEEK", "custom")]


def md_stages(xy):
    """X-Y stage allocation envelopes (Zaber X-LSM050A class; footprint UNVERIFIED)."""
    L, W, H = G.STAGE["env"]
    xc, yc = G.STAGE["x_travel_center"], G.STAGE["y_travel_center"]
    x, y = xy
    yz, xz = G.STAGE["Y_z"], G.STAGE["X_z"]
    ystage = boxc(xc - W / 2, yc - L / 2, BASE_PLATE_Z[1], xc + W / 2, yc + L / 2, BASE_PLATE_Z[1] + H)
    xstage = boxc(xc - L / 2, y - W / 2, BASE_PLATE_Z[1] + H, xc + L / 2, y + W / 2, BASE_PLATE_Z[1] + 2 * H)
    xcar = boxc(x - 15, y - 15, BASE_PLATE_Z[1] + 2 * H, x + 15, y + 15, G.MD_ZUNIT["z"][0])
    return [("Md_stage_Y_env", ystage, "envelope", "envelope"), ("Md_stage_X_env", xstage, "envelope", "envelope"),
            ("Md_adapter", xcar, "aluminium", "custom")]


# ------------------------------------------------------------------------------------------------ electrode bay
def ebay_enclosure():
    e = G.EBAY
    w = 0.8
    b = boxc(e["x"][0], e["y"][0], e["z"][0], e["x"][1], e["y"][1], e["z"][1])
    b = b.cut(boxc(e["x"][0] + w, e["y"][0] + w, e["z"][0] + w, e["x"][1] - w, e["y"][1] - w, e["z"][1] + 1))
    # cable gland hole E wall at z -45, drain hole in the floor, wedge slot in the E wall
    b = b.cut(cq.Workplane("YZ").workplane(offset=e["x"][1] - 2).center(EBAY_GLAND[1], EBAY_GLAND[2])
              .circle(2.5).extrude(4))
    b = b.cut(cyl(58.25, 34.5, e["z"][0] - 1, 3, 2.0))
    b = b.cut(boxc(e["x"][1] - 2, WEDGE["y"][0] - 0.2, WEDGE["z"][0] - 0.2, e["x"][1] + 1, WEDGE["y"][1] + 0.2,
                   WEDGE["z"][1] + 0.2))
    return b


EBAY_GLAND = (62.5, 31.5, -45.0)
WEDGE = {"y": (30.0, 32.2), "z": (-28.0, -24.0)}


def pogo_block(up=True):
    """PEEK pogo block: nose in the contact opening, shoulder bearing on the plate underside at the up stop."""
    dz = 0.0 if up else -I.POGO["block_lift_stroke"]
    cx = 0.5 * sum(I.ANVIL_CONTACT_OPENING["x"])
    cy = 0.5 * sum(I.ANVIL_CONTACT_OPENING["y"])
    nx, ny = G.POGO_NOSE
    nose = boxc(cx - nx / 2, cy - ny / 2, G.Z_THIN_BOTTOM + dz, cx + nx / 2, cy + ny / 2, G.POGO_NOSE_TOP_UP + dz)
    sx, sy = 6.3, I.ANVIL_CONTACT_OPENING["y"][1] - I.ANVIL_CONTACT_OPENING["y"][0]
    sh = boxc(cx - sx / 2, cy - sy / 2, -9.0 + dz, cx + sx / 2, cy + sy / 2, G.Z_THIN_BOTTOM + dz)
    body = boxc(cx - sx / 2, 29.75, WEDGE["z"][1] + dz, cx + sx / 2, 34.9, -9.0 + dz)
    blk = nose.union(sh).union(body)
    for (px, py) in I.POGO["pins"].values():
        blk = blk.cut(cyl(px, py, WEDGE["z"][1] + dz - 1, 40, G.POGO_PROBE["drill"]))
    for gx in (cx - 2.4, cx + 2.4):
        blk = blk.cut(cyl(gx, 34.0, WEDGE["z"][1] + dz - 1, 12, 1.6))
    return blk


def pogo_probes(up=True, card=True):
    dz = 0.0 if up else -I.POGO["block_lift_stroke"]
    out = None
    for (px, py) in I.POGO["pins"].values():
        tip = (I.POGO["tip_z_engaged"] if (up and card) else G.POGO_TIP_Z_ENGAGED_FREE + dz)
        barrel = cyl(px, py, WEDGE["z"][1] + dz + 1.0, G.POGO_NOSE_TOP_UP + dz - WEDGE["z"][1] - dz - 1.0, 0.86)
        plunger = cyl(px, py, G.POGO_NOSE_TOP_UP + dz - 0.5, tip - (G.POGO_NOSE_TOP_UP + dz - 0.5), 0.5)
        p = barrel.union(plunger)
        out = p if out is None else out.union(p)
    return out


def pogo_guide_and_wedge(up=True):
    cx = 0.5 * sum(I.ANVIL_CONTACT_OPENING["x"])
    gb = boxc(G.EBAY["x"][0] + 0.8, G.EBAY["y"][0] + 0.8, -36.0, G.EBAY["x"][1] - 0.8, G.EBAY["y"][1] - 0.8, -30.0)
    gb = gb.cut(boxc(cx - 3.6, WEDGE["y"][0] - 0.3, -37, G.EBAY["x"][1] + 1, WEDGE["y"][1] + 0.3, -29))
    pins = cyl(cx - 2.4, 34.0, -36.0, 14.0, 1.5).union(cyl(cx + 2.4, 34.0, -36.0, 14.0, 1.5))
    # wedge: 2:1 ramp, x position sets the block height (up: wedge pushed -x)
    xs = 0.0 if up else G.POGO_WEDGE["x_stroke"]
    x0 = cx - 3.0 + xs
    pts = [(x0, WEDGE["z"][0]), (x0 + 14.0, WEDGE["z"][0]), (x0 + 14.0, WEDGE["z"][1]), (x0 + 6.0, WEDGE["z"][1]),
           (x0, WEDGE["z"][1] - 3.0)]
    w = (cq.Workplane("XZ").workplane(offset=-WEDGE["y"][1]).polyline(pts).close().extrude(WEDGE["y"][1] - WEDGE["y"][0]))
    cyl_env = (cq.Workplane("YZ").workplane(offset=cx - 3.0 + G.POGO_WEDGE["x_stroke"] + 14.0 + 1.0)
               .center(0.5 * sum(WEDGE["y"]), -26.0).circle(4.0).extrude(22.0))
    rod = (cq.Workplane("YZ").workplane(offset=x0 + 14.0).center(0.5 * sum(WEDGE["y"]), -26.0).circle(1.0)
           .extrude(cx - 3.0 + G.POGO_WEDGE["x_stroke"] + 15.0 - (x0 + 14.0) + 0.5))
    cyl_env = cyl_env.union(rod)
    return [("pogo_guide_block", gb, "PEEK", "custom"), ("pogo_guide_pins", pins, "steel", "catalogue"),
            ("pogo_wedge", w, "PEEK", "custom"), ("pogo_cylinder_env", cyl_env, "envelope", "envelope")]


def ebay_internals():
    rx, ry = 58.25, 32.65
    rs = G.RELAY["size"]
    relay = boxc(rx - rs[0] / 2 + 0.5, ry - rs[1] / 2, G.RELAY["z"][0], rx + rs[0] / 2 - 0.5, ry + rs[1] / 2,
                 G.RELAY["z"][1])
    rh = boxc(G.EBAY["x"][0] + 0.8, 30.5, -45.0, G.EBAY["x"][0] + 1.8, 34.5, -39.0)
    leak = boxc(G.EBAY["x"][0] + 0.8, G.EBAY["y"][0] + 0.8, G.EBAY["z"][0] + 0.8, G.EBAY["x"][1] - 0.8,
                G.EBAY["y"][1] - 0.8, G.EBAY["z"][0] + 1.6)
    leak = leak.cut(cyl(58.25, 34.5, G.EBAY["z"][0], 3, 2.0))
    gland = (cq.Workplane("YZ").workplane(offset=G.EBAY["x"][1]).center(EBAY_GLAND[1], EBAY_GLAND[2]).circle(3.5)
             .extrude(6.0))
    return [("WE_relay_env", relay, "envelope", "envelope"), ("RH_sensor_env", rh, "pcb", "envelope"),
            ("ebay_leak_electrode", leak, "pcb", "custom"), ("ebay_cable_gland_env", gland, "envelope", "envelope")]


def gamry_cable():
    gb = I.dock_to_card(G.GAMRY_BULKHEAD)
    pts = [EBAY_GLAND, (100.0, EBAY_GLAND[1], EBAY_GLAND[2]), (115.0, gb[1], gb[2]), (G.TUBE_EXIT["E"], gb[1], gb[2])]
    s = None
    for p, q in zip(pts[:-1], pts[1:]):
        v = cq.Vector(q[0] - p[0], q[1] - p[1], q[2] - p[2])
        c = cq.Solid.makeCylinder(2.5, v.Length, cq.Vector(*p), v.normalized())
        s = c if s is None else s.fuse(c)
    return cq.Workplane("XY").add(s)


# ------------------------------------------------------------------------------------------------ sensors
THERMISTORS = {"T_anvil_win": (50.0, 47.0, -6.0), "T_anvil_RC": (66.0, 26.0, -16.0), "T_cold": (8.0, 38.0, -21.0),
               "T_heatsink": (4.0, 15.0, -40.0)}


def thermistors():
    return [(k, cyl(x, y, z - 1.0, 2.0, 1.6), "steel") for k, (x, y, z) in THERMISTORS.items()]
