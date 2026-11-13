"""3D solids of card A (C2 laminate): L0, L1, L1s (WE2 shim), L1b, L2, seam fill, L3, L4 discs, die (glass, metal,
passivation). Laminate layers are extruded from the shapely profiles (profiles.py); L3 is machined from CadQuery
primitives (true arcs) in the order a CNC programmer would use. Card coords, z = 0 = foil underside."""
from __future__ import annotations

import math
from functools import lru_cache

import cadquery as cq
from shapely.geometry import MultiPolygon, Polygon  # noqa: F401
from shapely.geometry.polygon import orient

from .. import interface as I
from . import profiles as P

# ------------------------------------------------------------------------------------------------ shapely -> solid


def _wire(coords, z):
    pts = [cq.Vector(float(x), float(y), z) for x, y in list(coords)[:-1]]
    return cq.Wire.makePolygon(pts, close=True)


def _clean_ring(ring, eps=2e-5):
    cs = list(ring.coords)[:-1]
    out = [cs[0]]
    for q in cs[1:]:
        if math.dist(q, out[-1]) > eps:
            out.append(q)
    if math.dist(out[0], out[-1]) <= eps:
        out.pop()
    return out + [out[0]]


def clean(geom, e=1e-4):
    """Remove zero-width spikes/slivers left by coincident edges of the boolean union (close + open by 0.1 um,
    mitre joins keep corners), then drop near-duplicate vertices. Changes no dimension above 0.1 um."""
    g = geom.buffer(e, join_style=2, mitre_limit=10).buffer(-2 * e, join_style=2, mitre_limit=10).buffer(
        e, join_style=2, mitre_limit=10)
    polys = list(g.geoms) if isinstance(g, MultiPolygon) else [g]
    return [Polygon(_clean_ring(p.exterior), [_clean_ring(r) for r in p.interiors]) for p in polys if not p.is_empty]


def poly_solid(geom, z0, h):
    """Extrude a shapely (Multi)Polygon with holes from z0 by h. Returns cq.Workplane (one compound)."""
    polys = clean(geom)
    solids = []
    for p in polys:
        if p.is_empty or p.area < 1e-9:
            continue
        p = orient(p, 1.0)
        face = cq.Face.makeFromWires(_wire(p.exterior.coords, z0), [_wire(r.coords, z0) for r in p.interiors])
        solids.append(cq.Solid.extrudeLinear(face, cq.Vector(0, 0, h)))
    return cq.Workplane("XY").newObject([cq.Compound.makeCompound(solids)]) if len(solids) > 1 else \
        cq.Workplane("XY").newObject(solids)


def volume(wp):
    return sum(s.Volume() for s in (wp.vals() if isinstance(wp, cq.Workplane) else [wp]))


# ------------------------------------------------------------------------------------------------ laminate


def _lam_plate(z0, h):
    """Laminate outline (L3 outline inset 0.2, CHOICE-13) as a true-arc plate."""
    L, W, r, k, e = I.CARD_L, I.CARD_W, I.CARD_CORNER_R, P.POKA_CHAMFER, I.LAMINATE_INSET
    ri = r - e
    s = math.sqrt(0.5)
    kc = k - e * (2 - math.sqrt(2))      # Derived: chamfer line x + y = L + W - k moved inward by e
    x0, y0, x1, y1 = e, e, L - e, W - e
    wp = (cq.Workplane("XY").workplane(offset=z0).moveTo(x0 + ri, y0).lineTo(x1 - ri, y0)
          .threePointArc((x1 - ri + ri * s, y0 + ri - ri * s), (x1, y0 + ri)).lineTo(x1, y1 - kc)
          .lineTo(x1 - kc, y1).lineTo(x0 + ri, y1)
          .threePointArc((x0 + ri - ri * s, y1 - ri + ri * s), (x0, y1 - ri)).lineTo(x0, y0 + ri)
          .threePointArc((x0 + ri - ri * s, y0 + ri - ri * s), (x0 + ri, y0)).close())
    return wp.extrude(h)


def _pin_tools(z0, z1):
    sx, sy = P.PIN_SLOT
    h = (P.PIN_SLOT_LEN - P.PIN_D) / 2
    return [_cyl(P.PIN_ROUND, P.PIN_D, z0, z1), _slot((sx, sy - h), (sx, sy + h), P.PIN_D, z0, z1)]


def _union(tools):
    u = None
    for t in tools:
        u = t if u is None else u.union(t)
    return u


@lru_cache(None)
def L0():
    z0, z1 = I.Z_L0
    tools = [_cyl(p.xy, I.PORT_HOLE_D, z0 - 0.1, z1 + 0.1) for p in I.PORTS.values() if p.kind == "liquid"]
    cw = I.CONTACT_WINDOW
    tools.append(_box(cw["x"][0], cw["y"][0], cw["x"][1], cw["y"][1], z0 - 0.1, z1 + 0.1))
    tools += _pin_tools(z0 - 0.1, z1 + 0.1)
    return _lam_plate(z0, z1 - z0).cut(_union(tools))


def _funnel_walls_solid(center, z0, z1):
    xc, yc = center
    r = I.IC1.d / 2
    seg = _cyl(center, I.IC1.d, z0, z1).intersect(_box(xc + P.FUNNEL_X[0], yc - r - 1, xc + r + 1, yc + r + 1,
                                                       z0, z1))
    taper = Polygon([(xc + P.FUNNEL_X[0] - 0.01, yc - P.FUNNEL_W[0] / 2), (xc + P.FUNNEL_X[1], yc - P.FUNNEL_W[1] / 2),
                       (xc + r + 0.5, yc - P.FUNNEL_W[1] / 2), (xc + r + 0.5, yc + P.FUNNEL_W[1] / 2),
                       (xc + P.FUNNEL_X[1], yc + P.FUNNEL_W[1] / 2), (xc + P.FUNNEL_X[0] - 0.01, yc + P.FUNNEL_W[0] / 2)])
    return seg.cut(poly_solid(taper, z0 - 0.1, z1 - z0 + 0.2))


@lru_cache(None)
def L1():
    """True-arc L1: plate minus (channel strips from shapely, true circles/boxes for the rest), funnel walls kept."""
    from shapely.ops import unary_union
    z0, z1 = I.Z_L1
    a, b = z0 - 0.1, z1 + 0.1
    named = P.l1_cut_named()
    # channel strips with coarser round joins at the bends (quad_segs 6: chord error <= 4 um on a 0.25 radius)
    strips = unary_union([P.chan(k, qs=6) for k in I.CHANNELS] + [named["nozzle1_mouth"], named["nozzle2_mouth"],
                          P.mc_region().difference(P.circ(I.MC.center, P.MC_D))])
    tools = [poly_solid(strips, a, b - a)]
    for ic in (I.IC1, I.IC2):
        xc, yc = ic.center
        throat = _box(xc + P.FUNNEL_X[1] - 0.2, yc - P.FUNNEL_W[1] / 2, xc + P.FUNNEL_X[1] + 0.1,
                      yc + P.FUNNEL_W[1] / 2, a, b)
        tools.append(_cyl(ic.center, ic.d, a, b).union(throat).cut(_funnel_walls_solid(ic.center, a - 0.1, b + 0.1)))
    for bb in (I.RCJ, I.RS, I.BW):
        tools.append(_box(bb.center[0] - bb.size[0] / 2, bb.center[1] - bb.size[1] / 2,
                          bb.center[0] + bb.size[0] / 2, bb.center[1] + bb.size[1] / 2, a, b))
    tools.append(_cyl(I.MC.center, P.MC_D, a, b))
    rc = P.rc_region().bounds
    tools.append(_box(rc[0], rc[1], rc[2], rc[3], a, b))
    tools.append(poly_solid(P.cer_region(), a, b - a))
    cw = I.CONTACT_WINDOW
    tools.append(_box(cw["x"][0], cw["y"][0], cw["x"][1], cw["y"][1], a, b))
    tools += [_cyl(p.xy, I.PORT_HOLE_D, a, b) for p in I.PORTS.values() if p.kind == "liquid"]
    tools += _pin_tools(a, b)
    return _lam_plate(z0, z1 - z0).cut(_union(tools))


@lru_cache(None)
def L1s():
    return poly_solid(P.L1s_shim(), I.Z_L1[0], P.WE2_SHIM_T)


@lru_cache(None)
def L1b():
    return poly_solid(P.L1b(), I.Z_L1B[0], I.Z_L1B[1] - I.Z_L1B[0])


@lru_cache(None)
def L2():
    """TPE ceiling (true arcs). Where the seam-cover film runs under the TPE edge (die + 0.10 ... + 0.15) the TPE is
    drawn with a 25 um relief = its local compression over the film (docs/18 CHOICE-14, docs/19 §2.4)."""
    z0, z1 = I.Z_L2
    a, b = z0 - 0.1, z1 + 0.1
    tools = [_cyl(I.IC1.center, I.IC1.d, a, b), _cyl(I.IC2.center, I.IC2.d, a, b), _cyl(I.MC.center, P.MC_D, a, b)]
    for bb in (I.RCJ, I.RS, I.BW):
        tools.append(_box(bb.center[0] - bb.size[0] / 2, bb.center[1] - bb.size[1] / 2,
                          bb.center[0] + bb.size[0] / 2, bb.center[1] + bb.size[1] / 2, a, b))
    d = P.tpe_die_cut().bounds
    tools.append(_box(d[0], d[1], d[2], d[3], a, b))
    tools += _pin_tools(a, b)
    full = _lam_plate(z0, z1 - z0).cut(_union(tools))
    f = P.film_outline().bounds
    relief = _box(f[0], f[1], f[2], f[3], I.Z_L1B[0] - 0.01, I.Z_L1B[1]).cut(_box(d[0], d[1], d[2], d[3], a, b))
    return full.cut(relief)


@lru_cache(None)
def seam():
    return poly_solid(P.seam_fill(), I.DIE_Z[0], I.Z_L2[1] - I.DIE_Z[0])


# ------------------------------------------------------------------------------------------------ L3 body


def _l3_outline_wp(z0, h):
    L, W, r, k = I.CARD_L, I.CARD_W, I.CARD_CORNER_R, P.POKA_CHAMFER
    s = math.sqrt(0.5)
    wp = (cq.Workplane("XY").workplane(offset=z0).moveTo(r, 0).lineTo(L - r, 0)
          .threePointArc((L - r + r * s, r - r * s), (L, r)).lineTo(L, W - k).lineTo(L - k, W).lineTo(r, W)
          .threePointArc((r - r * s, W - r + r * s), (0, W - r)).lineTo(0, r)
          .threePointArc((r - r * s, r - r * s), (r, 0)).close())
    return wp.extrude(h)


def _cyl(c, d, z0, z1):
    return cq.Workplane("XY").workplane(offset=z0).center(*c).circle(d / 2).extrude(z1 - z0)


def _slot(c1, c2, d, z0, z1):
    cx, cy = (c1[0] + c2[0]) / 2, (c1[1] + c2[1]) / 2
    L = math.dist(c1, c2)
    ang = math.degrees(math.atan2(c2[1] - c1[1], c2[0] - c1[0]))
    return cq.Workplane("XY").workplane(offset=z0).center(cx, cy).slot2D(L + d, d, ang).extrude(z1 - z0)


def _box(x0, y0, x1, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def _rbox(c, sx, sy, r, z0, z1):
    return (cq.Workplane("XY").workplane(offset=z0).center(*c).rect(sx, sy).extrude(z1 - z0)
            .edges("|Z").fillet(r))


def _cone(c, r0, r1, z0, h):
    return cq.Workplane("XY").newObject([cq.Solid.makeCone(r0, r1, h, cq.Vector(c[0], c[1], z0))])


def l3_through_tools():
    """CadQuery tools for every through feature (true arcs). Returns list of (name, Workplane)."""
    z0, z1 = I.Z_L3[0] - 0.1, I.Z_L3[1] + 0.1
    tools = []
    groups, singles, extra = P.l3_bore_groups()
    for g, (a, b) in groups.items():
        va, vb = I.VALVES[a], I.VALVES[b]
        tools.append((g, _slot(va.xy, vb.xy, va.bore_d, z0, z1)))
    for k in singles:
        v = I.VALVES[k]
        tools.append((k, _cyl(v.xy, v.bore_d, z0, z1)))
    win, _ = P.die_window()
    x0, y0, x1, y1 = win.bounds
    tools.append(("die_window", _box(x0, y0, x1, y1, z0, z1)))
    for i, p in enumerate(((x0, y0), (x1, y0), (x0, y1), (x1, y1))):
        tools.append((f"win_relief{i}", _cyl(p, 2 * P.WIN_RELIEF_R, z0, z1)))
    for k in I.DIE_NOTCHED_BORES:
        v = I.VALVES[k]
        (x, y), d = v.xy, v.bore_d
        tools.append((k, _cyl(v.xy, d, z0, z1)))
        if x < x0:
            tools.append((k + "_notch", _box(x, y - d / 2, x0 + 0.01, y + d / 2, z0, z1)))
        elif x > x1:
            tools.append((k + "_notch", _box(x1 - 0.01, y - d / 2, x, y + d / 2, z0, z1)))
        else:
            tools.append((k + "_notch", _box(x - d / 2, y, x + d / 2, y0 + 0.01, z0, z1)))
    for a, b, _ in extra:
        va, vb = I.VALVES[a], I.VALVES[b]
        tools.append((f"{a}{b}_merge", _slot(va.xy, vb.xy, min(va.bore_d, vb.bore_d), z0, z1)))
    # thermal break slot: three segments, R1.0 inside corners at the bridges (CHOICE-C3)
    xa, xb = I.X_BREAK
    ys = [-1.0] + [v for b in I.BREAK_BRIDGES_Y for v in b] + [I.CARD_W + 1.0]
    for i in range(0, len(ys), 2):
        ya, yb = ys[i], ys[i + 1]
        t = _box(xa, ya, xb, yb, z0, z1)
        t = t.edges("|Z").fillet(P.TANK_CORNER_R)   # corners outside the card are harmless
        tools.append((f"thermal_slot{i // 2}", t))
    return tools


def l3_blind_tools():
    zb = I.Z_L3[0] - 0.1
    zt = I.Z_L3[1]
    t = []
    t.append(("IC1", _cyl(I.IC1.center, I.IC1.d, zb, I.IC1.z[1])))
    t.append(("IC2", _cyl(I.IC2.center, I.IC2.d, zb, I.IC2.z[1])))
    t.append(("RCj", _rbox(I.RCJ.center, *I.RCJ.size, P.TANK_CORNER_R, zb, I.RCJ.z[1])
              .cut(_cyl(I.VALVES["V8"].xy, 2 * P.V8_BOSS, zb - 0.1, I.RCJ.z[1] + 0.1))))
    t.append(("RS", _rbox(I.RS.center, *I.RS.size, P.TANK_CORNER_R, zb, I.RS.z[1])))
    t.append(("MC", _cyl(I.MC.center, P.MC_D, zb, P.MC_STOP_Z - P.ADH_T)))
    t.append(("MC_cbore", _cyl(I.MC.center, P.MC_CBORE_D, P.MC_STOP_Z - P.ADH_T, zt + 0.1)))
    t.append(("pin_round", _cyl(P.PIN_ROUND, P.PIN_D, zb, I.Z_L3[0] + P.PIN_L3_DEPTH)))
    sx, sy = P.PIN_SLOT
    h = (P.PIN_SLOT_LEN - P.PIN_D) / 2
    t.append(("pin_slot", _slot((sx, sy - h), (sx, sy + h), P.PIN_D, zb, I.Z_L3[0] + P.PIN_L3_DEPTH)))
    for k, c in P.vent_sites().items():
        t.append((k + "_hole", _cyl(c, P.VENT_HOLE_D, zt - I.CHAMBER_ROOF_T - 0.05, zt)))
        t.append((k + "_recess", _cyl(c, P.VENT_RECESS_D, zt - P.VENT_RECESS_T, zt + 0.1)))
    ix, iy = I.ID_CODE["xy"]
    sx_, sy_ = I.ID_CODE["size"]
    m = P.ID_MARGIN
    t.append(("ID_recess", _box(ix - m, iy - m, ix + sx_ + m, iy + sy_ + m, zt - P.ID_RECESS, zt + 0.1)))
    t.append(("arrow", cq.Workplane("XY").workplane(offset=zt - P.ARROW_DEPTH).polyline(P.ARROW).close()
              .extrude(P.ARROW_DEPTH + 0.1)))
    # bore lead-ins 0.3 x 45 deg at the top of every pin position (CHOICE-2), V8 reduced (CHOICE-C10)
    for k, v in I.VALVES.items():
        li = P.LEAD_IN_LOCAL.get(k, P.LEAD_IN)
        r = v.bore_d / 2
        if li <= 0:
            continue
        t.append((k + "_leadin", _cone(v.xy, r, r + li + 0.1, zt - li, li + 0.1)))
    return t


@lru_cache(None)
def L3():
    body = _l3_outline_wp(I.Z_L3[0], I.L3_T)
    cut = None
    for _, tool in l3_through_tools() + l3_blind_tools():
        cut = tool if cut is None else cut.union(tool)
    return body.cut(cut)


# ------------------------------------------------------------------------------------------------ L4 discs


@lru_cache(None)
def L4():
    """PTFE discs (vents IC1, IC2, RS, P_c; MC stop) with their adhesive rings. Returns dict name -> Workplane."""
    zt = I.Z_L3[1]
    out = {}
    for k, c in P.vent_sites().items():
        zf = zt - P.VENT_RECESS_T
        ring = _cyl(c, I.VENT_DISC_D, zf, zf + P.ADH_T).cut(_cyl(c, P.VENT_HOLE_D + 0.6, zf - 0.1, zf + 0.2))
        out[k + "_adh"] = ring
        out[k] = _cyl(c, I.VENT_DISC_D, zf + P.ADH_T, zf + P.ADH_T + P.DISC_T)
    c = I.MC.center
    zf = P.MC_STOP_Z - P.ADH_T
    out["MC_stop_adh"] = _cyl(c, P.MC_DISC_D, zf, zf + P.ADH_T).cut(_cyl(c, 2.0, zf - 0.1, zf + 0.2))
    out["MC_stop"] = _cyl(c, P.MC_DISC_D, P.MC_STOP_Z, P.MC_STOP_Z + P.DISC_T)
    return out


# ------------------------------------------------------------------------------------------------ die


@lru_cache(None)
def die_glass():
    return _box(I.DIE_X[0], I.DIE_Y[0], I.DIE_X[1], I.DIE_Y[1], I.DIE_Z[0], I.DIE_Z[1])


@lru_cache(None)
def die_metal():
    from shapely.ops import unary_union
    return poly_solid(unary_union(list(P.metal().values())), I.DIE_Z[0] - P.METAL_T, P.METAL_T)


@lru_cache(None)
def die_passivation():
    return poly_solid(P.passivation(), I.DIE_Z[0] - P.METAL_T - P.PASS_T, P.PASS_T)


# ------------------------------------------------------------------------------------------------ registry


def all_parts():
    """[(name, Workplane, material)] in z-order; materials are common.COLORS keys."""
    p = [("L0_foil", L0(), "COC_foil"), ("L1_channel_sheet", L1(), "COC"), ("L1s_WE2_shim", L1s(), "COC"),
         ("L1b_die_film", L1b(), "elastomer"), ("L2_TPE", L2(), "TPE"), ("seam_adhesive", seam(), "elastomer"),
         ("L3_body", L3(), "COC"), ("die_glass", die_glass(), "glass"), ("die_metal", die_metal(), "gold"),
         ("die_passivation", die_passivation(), "pcb")]
    for k, w in L4().items():
        p.append(("L4_" + k, w, "elastomer" if k.endswith("_adh") else "PTFE"))
    return p
