"""2D profiles (shapely, card coords, mm, seen from the TOP) of every card layer, the die masks and fluid regions.

Every interface number is imported from elisa_cad.interface (never retyped). Card-only numbers defined here carry a
source tag: docs/13 §x | docs/18 §x | Derived | CHOICE-Cn / DEV-Cn (docs/19 §7/§8) | UNVERIFIED | [assessment].
"""
from __future__ import annotations

import math

from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

from .. import interface as I

QS = 32  # shapely quad_segs for circles: 128 segments, chord error <= 1.2 um at r = 4 (Derived r(1-cos(pi/256)))

# ------------------------------------------------------------------------------------------------ card numbers
# Laminate layer outline = L3 outline offset inward by LAMINATE_INSET (interface, CHOICE-13).
POKA_CHAMFER = I.CARD_POKA_CHAMFER["leg"]   # 4.0, CHOICE-C7 (interface Rev B CARD_POKA_CHAMFER; nest block: LOWER)
TANK_CORNER_R = 1.0         # CHOICE-C3: RCj/RS L3 cavities milled with a D2 end mill (vertical corners R1.0)
FUNNEL_X = (2.0, 4.0)       # docs/13 §2.3: funnel in L1 from x_c + 2.0 to x_c + 4.0 (the bore wall)
FUNNEL_W = (2.5, 0.5)       # docs/13 §2.3: 2.5 -> 0.5 wide
MC_D = I.MC.d               # DEV-C1 (interface Rev B MC.d): round meter of the same area, Derived
#   sqrt(4 x 2.0 / pi) = 1.596 mm; 2.000 mm^2 x 5.0 mm (foil to stop) = 10.0 uL as docs/13 §2.3
MC_STOP_Z = I.MC.z[1]       # 5.14: lower face of the PTFE stop disc (docs/13 §2.3, interface MC.z)
TPE_CUT_CLEAR = 0.10        # docs/18 CHOICE-14: TPE cut-out = die + 0.10
FILM_CLEAR = 0.15           # docs/18 CHOICE-14: L1b film = die + 0.15 (seam cover)
#   L3 window: CHOICE-C1 -- datum edges flush with the nominal die edges (x = 55.0, y = 33.35, I.DIE_DATUM_EDGES),
#   the two free edges at die + 2 x DIE_WINDOW_CLEAR = +0.10 (same total clearance as +0.05 per side).
WIN_RELIEF_R = 0.5          # CHOICE-C1: D1.0 corner reliefs (die corners clear the milled inside corners)
WE2_SHIM_T = 0.15           # docs/13 §2.3: 0.15 mm COC shim on the foil in the L1 cut-out -> 0.05 channel
WE2_SHIM_GAP = 0.01         # CHOICE-C5: shim cut 0.01 smaller per side than the L1 slot (press fit, UNVERIFIED)
PIN_D = 2.0                 # CHOICE-C4: lamination dowels D2.0 [assessment]
PIN_ROUND = I.CARD_TOOLING_HOLES["round"]["xy"]   # (59, 42) CHOICE-C4 (interface Rev B CARD_TOOLING_HOLES)
PIN_SLOT = I.CARD_TOOLING_HOLES["slot"]["xy"]     # (59, 5) slot hole, elongated along the pin-to-pin line (y)
PIN_SLOT_LEN = I.CARD_TOOLING_HOLES["slot"]["len_y"]   # 3.0
PIN_L3_DEPTH = I.CARD_TOOLING_HOLES["depth_L3"]        # 3.0
VENT_RECESS_D = 4.4         # docs/18 §4 (vents recessed in D4.4 x 0.3)
VENT_RECESS_T = I.LAYERS["L4_vents"][1] - I.LAYERS["L4_vents"][0]   # 0.3 (interface LAYERS L4)
VENT_HOLE_D = 2.0           # docs/18 DEV-7 (D2 vent hole in the 0.5 roof)
DISC_T = 0.20               # UNVERIFIED: PTFE membrane disc thickness (supported ePTFE class)
ADH_T = 0.025               # CHOICE-C6: 25 um acrylic transfer-adhesive ring under each disc (UNVERIFIED grade)
P_C_DISC = True             # CHOICE-C8: P_c (RCj headspace) also gets a PTFE disc (liquid barrier to the gas line)
MC_CBORE_D = 3.4            # CHOICE-C2: counterbore from the top over MC, holds the D3.0 stop disc
MC_DISC_D = 3.0             # CHOICE-C2
ID_RECESS = 0.10            # CHOICE-C9: label recess depth (label <= 0.08 thick, UNVERIFIED) under the ID area
ID_MARGIN = 0.3             # CHOICE-C9: recess = ID area + 0.3 per side
ARROW = [(10.0, 4.0), (8.5, 1.5), (11.5, 1.5)]   # CHOICE-C7: engraved orientation triangle (points to +y = away)
ARROW_DEPTH = 0.2
MIN_WEB_L3 = 0.5            # [assessment]: minimum milled COC web 5.5 mm tall; narrower bore pairs are merged
LEAD_IN = I.PLUNGER["card_bore_lead_in"]          # 0.3 x 45 deg (CHOICE-2)
LEAD_IN_LOCAL = dict(I.PLUNGER["card_bore_lead_in_except"])   # {"V8": 0.0} CHOICE-C10 (interface Rev B): no lead-in at V8 (edge break only) so the P_mv lid gas ring (OD 7)
#                               keeps 0.14 mm of flat land to the bore

TIP_TOL_WC = 0.14           # Derived worst case tip-to-channel: head-to-nest 0.03 + datum pin 0.01 + L3 edge-to-
#                             feature 0.05 + L1-to-L3 registration 0.05 (interface TOL); RSS 0.078 (docs/19 §5)

# ------------------------------------------------------------------------------------------------ helpers


def circ(c, d):
    return Point(c).buffer(d / 2.0, quad_segs=QS)


def rect_c(c, sx, sy):
    return box(c[0] - sx / 2, c[1] - sy / 2, c[0] + sx / 2, c[1] + sy / 2)


def rrect_c(c, sx, sy, r):
    return rect_c(c, sx - 2 * r, sy - 2 * r).buffer(r, quad_segs=QS)


def chan(name, qs=QS):
    ch = I.CHANNELS[name]
    return LineString(ch["pts"]).buffer(ch["w"] / 2.0, cap_style=2, join_style=1, quad_segs=qs)


def hull2(c1, c2, d):
    return unary_union([circ(c1, d), circ(c2, d)]).convex_hull


# ------------------------------------------------------------------------------------------------ outlines


def l3_outline():
    L, W, r, k = I.CARD_L, I.CARD_W, I.CARD_CORNER_R, POKA_CHAMFER
    core = box(r, r, L - r, W - r).buffer(r, quad_segs=QS)
    cham = Polygon([(L - k - 1, W + 1), (L + 1, W + 1), (L + 1, W - k - 1)])   # x + y >= L + W - k
    return core.difference(cham)


def laminate_outline():
    return l3_outline().buffer(-I.LAMINATE_INSET, quad_segs=QS, join_style=1)


DIE = box(I.DIE_X[0], I.DIE_Y[0], I.DIE_X[1], I.DIE_Y[1])


def pin_holes(d=PIN_D):
    rnd = circ(PIN_ROUND, d)
    slt = LineString([(PIN_SLOT[0], PIN_SLOT[1] - (PIN_SLOT_LEN - d) / 2),
                      (PIN_SLOT[0], PIN_SLOT[1] + (PIN_SLOT_LEN - d) / 2)]).buffer(d / 2, quad_segs=QS)
    return rnd, slt


# ------------------------------------------------------------------------------------------------ L1 features


def funnel_walls(center):
    """L1 material kept inside the chamber circle: the two funnel walls (docs/13 §2.3)."""
    xc, yc = center
    r = I.IC1.d / 2
    seg = circ(center, I.IC1.d).intersection(box(xc + FUNNEL_X[0], yc - r - 1, xc + r + 1, yc + r + 1))
    taper = Polygon([(xc + FUNNEL_X[0] - 0.01, yc - FUNNEL_W[0] / 2), (xc + FUNNEL_X[1], yc - FUNNEL_W[1] / 2),
                     (xc + r + 0.5, yc - FUNNEL_W[1] / 2), (xc + r + 0.5, yc + FUNNEL_W[1] / 2),
                     (xc + FUNNEL_X[1], yc + FUNNEL_W[1] / 2), (xc + FUNNEL_X[0] - 0.01, yc + FUNNEL_W[0] / 2)])
    return seg.difference(taper)


def chamber_region_L1(center):
    """Bore circle minus the funnel walls, plus the 0.5 throat to x_c + 4.1 so no sliver is left between the
    circle and the flat start of the lane (the circle touches x_c + 4 only at y_c)."""
    xc, yc = center
    throat = box(xc + FUNNEL_X[1] - 0.2, yc - FUNNEL_W[1] / 2, xc + FUNNEL_X[1] + 0.1, yc + FUNNEL_W[1] / 2)
    return unary_union([circ(center, I.IC1.d), throat]).difference(funnel_walls(center))


def mc_region():
    """Meter: D1.596 (DEV-C1) + bridging strip so RCj_to_MC (ends x 15.0) and conj_line (starts x 17.0) reach it."""
    c = I.MC.center
    strip = LineString([(c[0] - I.MC.size[0] / 2, c[1]), (c[0] + I.MC.size[0] / 2, c[1])]).buffer(
        I.LINE_W / 2, cap_style=2)
    return unary_union([circ(c, MC_D), strip])


def rc_region():
    return rect_c(I.RC_CENTER, *I.RC_SIZE)


def cer_region():
    p, n = I.CER_POCKET, I.CER_NECK
    return unary_union([box(p["x"][0], p["y"][0], p["x"][1], p["y"][1]),
                        box(n["x"][0], n["y"][0], n["x"][1], n["y"][1])])


def contact_window():
    cw = I.CONTACT_WINDOW
    return box(cw["x"][0], cw["y"][0], cw["x"][1], cw["y"][1])


def we2_slot():
    return chan("WE2_link")


def we2_shim():
    return we2_slot().buffer(-WE2_SHIM_GAP, join_style=2)


def port_holes(kind="liquid"):
    return {k: circ(p.xy, I.PORT_HOLE_D) for k, p in I.PORTS.items() if p.kind == kind}


def channel_polys():
    return {k: chan(k) for k in I.CHANNELS}


def l1_cut_named():
    """Named L1 through-cut regions (each a fluid region of height CHANNEL_H, the cell ones CELL_H)."""
    d = dict(channel_polys())
    for nz in ("nozzle1", "nozzle2"):   # nozzle cut carried 0.4 into the bore: no sliver at the tangential mouth
        (xa, y), (xb, _) = I.CHANNELS[nz]["pts"]
        d[nz + "_mouth"] = box(xb - 0.1, y - I.CHANNELS[nz]["w"] / 2, xb + 0.4, y + I.CHANNELS[nz]["w"] / 2)
    d["IC1"] = chamber_region_L1(I.IC1.center)
    d["IC2"] = chamber_region_L1(I.IC2.center)
    d["RCj"] = rect_c(I.RCJ.center, *I.RCJ.size)
    d["RS"] = rect_c(I.RS.center, *I.RS.size)
    d["MC"] = mc_region()
    d["BW"] = rect_c(I.BW.center, *I.BW.size)
    d["RC"] = rc_region()
    d["CER"] = cer_region()
    for k, p in port_holes().items():
        d["port_" + k] = p
    d["contact_window"] = contact_window()
    return d


def l1_cuts():
    rnd, slt = pin_holes()
    return unary_union(list(l1_cut_named().values()) + [rnd, slt])


# ------------------------------------------------------------------------------------------------ layer materials


def L0():
    rnd, slt = pin_holes()
    holes = unary_union(list(port_holes().values()) + [contact_window(), rnd, slt])
    return laminate_outline().difference(holes)


def L1():
    return laminate_outline().difference(l1_cuts())


def L1s_shim():
    return we2_shim()


def film_outline():
    return DIE.buffer(FILM_CLEAR, join_style=2)


def L1b():
    cut = l1_cuts().intersection(DIE)
    return film_outline().difference(cut)


def tpe_die_cut():
    return DIE.buffer(TPE_CUT_CLEAR, join_style=2)


def l2_cut_named():
    rnd, slt = pin_holes()
    return {"IC1": circ(I.IC1.center, I.IC1.d), "IC2": circ(I.IC2.center, I.IC2.d),
            "RCj": rect_c(I.RCJ.center, *I.RCJ.size), "RS": rect_c(I.RS.center, *I.RS.size),
            "MC": circ(I.MC.center, MC_D), "BW": rect_c(I.BW.center, *I.BW.size),
            "die": tpe_die_cut(), "pin_round": rnd, "pin_slot": slt}


def L2():
    return laminate_outline().difference(unary_union(list(l2_cut_named().values())))


def seam_fill():
    """Adhesive in the die-to-TPE seam (docs/18 CHOICE-14), z DIE_Z[0] .. Z_L2[1]."""
    return tpe_die_cut().difference(DIE)


# ------------------------------------------------------------------------------------------------ L3 plan


def die_window():
    x0, x1 = I.DIE_X[0], I.DIE_X[1] + 2 * I.DIE_WINDOW_CLEAR
    y0, y1 = I.DIE_Y[0] - 2 * I.DIE_WINDOW_CLEAR, I.DIE_Y[1]
    w = box(x0, y0, x1, y1)
    reliefs = [circ(p, 2 * WIN_RELIEF_R) for p in ((x0, y0), (x1, y0), (x0, y1), (x1, y1))]
    return w, unary_union([w] + reliefs)


def bore_d(v):
    return v.bore_d


def notch(vid):
    """Bore of a die-window-notched valve joined to the window by a strip of the bore width (DEV-2)."""
    v = I.VALVES[vid]
    w, _ = die_window()
    x0, y0, x1, y1 = w.bounds
    (x, y), d = v.xy, v.bore_d
    if x < x0:                               # G3: window -x edge
        strip = box(x, y - d / 2, x0 + 0.01, y + d / 2)
    elif x > x1:                             # V14: +x edge
        strip = box(x1 - 0.01, y - d / 2, x, y + d / 2)
    else:                                    # G4, V15: -y edge
        strip = box(x - d / 2, y, x + d / 2, y0 + 0.01)
    return unary_union([circ(v.xy, d), strip])


def l3_bore_groups():
    """Through bores grouped: merged pairs (interface MERGED_BORES + any web < MIN_WEB_L3), notched, single."""
    groups = {k: list(v) for k, v in I.MERGED_BORES.items()}
    grouped = {m for g in groups.values() for m in g}
    singles = [k for k in I.VALVES if k not in grouped and k not in I.DIE_NOTCHED_BORES]
    # extra merges where two bores leave a web < MIN_WEB_L3 (CHOICE-C11)
    ids = [k for k in I.VALVES]
    extra = []
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            va, vb = I.VALVES[a], I.VALVES[b]
            web = math.dist(va.xy, vb.xy) - (va.bore_d + vb.bore_d) / 2
            same = any(a in g and b in g for g in groups.values())
            if web < MIN_WEB_L3 and not same:
                extra.append((a, b, round(web, 3)))
    return groups, singles, extra


def l3_through():
    """Plan of all through features of L3 (bores, merged slots, notches, window, thermal slot)."""
    groups, singles, extra = l3_bore_groups()
    parts = []
    for g in groups.values():
        va, vb = I.VALVES[g[0]], I.VALVES[g[1]]
        parts.append(hull2(va.xy, vb.xy, va.bore_d))
    for k in singles:
        parts.append(circ(I.VALVES[k].xy, I.VALVES[k].bore_d))
    for k in I.DIE_NOTCHED_BORES:
        parts.append(notch(k))
    for a, b, _ in extra:
        va, vb = I.VALVES[a], I.VALVES[b]
        parts.append(hull2(va.xy, vb.xy, min(va.bore_d, vb.bore_d)))
    parts.append(die_window()[1])
    parts.append(thermal_slot())
    return unary_union(parts)


def thermal_slot():
    x0, x1 = I.X_BREAK
    ys = [-1.0] + [v for b in I.BREAK_BRIDGES_Y for v in b] + [I.CARD_W + 1.0]
    segs = [box(x0, ys[i], x1, ys[i + 1]) for i in range(0, len(ys), 2)]
    # milled with a D2 end mill: the closed ends at the bridges get R1.0 corners (CHOICE-C3)
    out = []
    for s in segs:
        out.append(s.buffer(-1.0).buffer(1.0, quad_segs=QS) if s.bounds[1] > 0 and s.bounds[3] < I.CARD_W else
                   _round_inner_end(s))
    return unary_union(out)


def _round_inner_end(s):
    x0, y0, x1, y1 = s.bounds
    if y0 < 0:   # open at the front edge, round the end at y1
        return unary_union([box(x0, y0, x1, y1 - 1.0), box(x0 + 1, y1 - 1.0, x1 - 1, y1),
                            circ((x0 + 1, y1 - 1), 2), circ((x1 - 1, y1 - 1), 2)])
    return unary_union([box(x0, y0 + 1.0, x1, y1), box(x0 + 1, y0, x1 - 1, y0 + 1.0),
                        circ((x0 + 1, y0 + 1), 2), circ((x1 - 1, y0 + 1), 2)])


def l3_blind_bottom():
    """Blind cavities from below: name -> (plan, z_top).  z_bottom = Z_L3[0]."""
    rnd, slt = pin_holes()
    return {
        "IC1": (circ(I.IC1.center, I.IC1.d), I.IC1.z[1]),
        "IC2": (circ(I.IC2.center, I.IC2.d), I.IC2.z[1]),
        "RCj": (rcj_l3(), I.RCJ.z[1]),
        "RS": (rrect_c(I.RS.center, *I.RS.size, TANK_CORNER_R), I.RS.z[1]),
        "MC": (circ(I.MC.center, MC_D), MC_STOP_Z - ADH_T),
        "pin_round": (rnd, I.Z_L3[0] + PIN_L3_DEPTH),
        "pin_slot": (slt, I.Z_L3[0] + PIN_L3_DEPTH),
    }


V8_BOSS = I.VALVES["V8"].bore_d / 2 + MIN_WEB_L3   # CHOICE-C13: RCj L3 wall bulges around the V8 bore


def rcj_l3():
    """RCj cavity in L3: 10 x 10, R1.0 corners, minus a boss keeping a 0.5 mm web to the V8 bore (CHOICE-C13)."""
    return rrect_c(I.RCJ.center, *I.RCJ.size, TANK_CORNER_R).difference(circ(I.VALVES["V8"].xy, 2 * V8_BOSS))


def vent_sites():
    s = dict(I.VENTS)
    if P_C_DISC:
        s["vent_P_c"] = I.PORTS["P_c"].xy
    return s


# ------------------------------------------------------------------------------------------------ die masks
# Electrode pattern on the die's LOWER face, card coords seen from the top (mask export mirrors it, docs/19 §2.8).
WE1_OPEN = unary_union([
    rect_c(I.RC_CENTER, I.RC_SIZE[0] - 0.10, I.RC_SIZE[1] - 0.10),            # 2.5 x 1.9 (docs/13 §3.5.1)
    box(I.G3_FINGER["x"][0] + 0.05, I.G3_FINGER["y_c"] - 0.20, I.RC_CENTER[0] - I.RC_SIZE[0] / 2 + 0.05,
        I.G3_FINGER["y_c"] + 0.20),                                             # G3 finger 0.4 wide (docs/13 §2.7)
    box(I.G4_FINGER["x_c"] - 0.20, 23.60, I.G4_FINGER["x_c"] + 0.20, I.G4_FINGER["y"][1] + 0.05),
    #   G4 finger 0.4 wide; starts at y 23.60 (not 23.40): CE/RE traces pass below it (CHOICE-C12)
])
WE2_OPEN = box(58.6, 24.45, 60.6, 25.55)   # CHOICE-C12: 2.0 long (docs/13 1.0 x 2.0); 1.1 wide so the wetted
#   width is set by the 1.0 channel, not by registration
_P = I.CER_POCKET
RE_OPEN = box(_P["x"][0] + 0.02, _P["y"][0] + 0.02, _P["x"][0] + 0.12, _P["y"][0] + 0.12)   # 0.1 x 0.1 (docs/13)
CE_OPEN = box(_P["x"][0] + 0.02, _P["y"][0] + 0.02, _P["x"][1] - 0.02, _P["y"][1] - 0.02).difference(
    box(_P["x"][0], _P["y"][0], _P["x"][0] + 0.16, _P["y"][0] + 0.16))         # CHOICE-C12: L-shape 0.110 mm^2
PAD_OPEN_INSET = 0.05      # CHOICE-C12: passivation opening = pad - 0.05 per side
TRACES = {                 # CHOICE-C12: single metal layer routing (no crossings), (polyline, width)
    "WE1": ([(56.2, 25.9), (56.2, 30.2)], 0.20),
    "WE2": ([(59.0, 25.5), (59.0, 27.0), (58.0, 27.0), (58.0, 30.2)], 0.20),
    "CE": ([(60.3, 30.6), (60.77, 30.6), (60.77, 23.50), (55.67, 23.50)], 0.04),
    "RE": ([(56.2, 32.8), (56.2, 33.15), (60.85, 33.15), (60.85, 23.42), (55.37, 23.42), (55.37, 23.48)], 0.04),
    "LOOP": ([(58.5, 32.4), (59.3, 32.4)], 0.05),      # docs/13 §3.5.1: two pads joined by a 50 um line
}
METAL_T = 0.0002           # docs/13 §2.1: Au 150 nm on Ti 50 nm
PASS_T = 0.001             # UNVERIFIED: SU-8/polyimide passivation thickness (1 um drawn)


def pads():
    return {k: rect_c(c, *I.PAD_SIZE) for k, c in I.PADS.items()}


def metal():
    m = {"WE1": WE1_OPEN.buffer(0.01, join_style=2), "WE2": WE2_OPEN.buffer(0.01, join_style=2),
         "CE": CE_OPEN.buffer(0.005, join_style=2), "RE": RE_OPEN.buffer(0.005, join_style=2)}
    pp = pads()
    tr = {k: LineString(p).buffer(w / 2, cap_style=2, join_style=2) for k, (p, w) in TRACES.items()}
    nets = {"WE1": unary_union([m["WE1"], tr["WE1"], pp["WE1"]]),
            "WE2": unary_union([m["WE2"], tr["WE2"], pp["WE2"]]),
            "CE": unary_union([m["CE"], tr["CE"], pp["CE"]]),
            "RE": unary_union([m["RE"], tr["RE"], pp["RE"]]),
            "LOOP": unary_union([tr["LOOP"], pp["LOOP_A"], pp["LOOP_B"]])}
    return nets


def passivation_openings():
    o = {"WE1": WE1_OPEN, "WE2": WE2_OPEN, "CE": CE_OPEN, "RE": RE_OPEN}
    for k, p in pads().items():
        o["pad_" + k] = p.buffer(-PAD_OPEN_INSET, join_style=2)
    return o


def passivation():
    return DIE.difference(unary_union(list(passivation_openings().values())))


def to_die_local(geom):
    """Card (seen from top) -> die-local mask coords seen looking AT the electrode face (from below the card):
    u = DIE_X[1] - x (mirror), v = y - DIE_Y[0]; origin = die corner (61.0, 23.35)."""
    from shapely.affinity import affine_transform
    return affine_transform(geom, [-1, 0, 0, 1, I.DIE_X[1], -I.DIE_Y[0]])
