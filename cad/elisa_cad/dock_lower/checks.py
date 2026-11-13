"""One-off CAD checks for docs/21 §6 (run by build.py; results written to out/dock_lower/checks.json + .txt).
Methods: OCC boolean intersection volumes between every pair of solids (bounding-box pre-filter) per machine state;
M_d swept positions sampled every 0.25 mm along all paths (both Z states where the path allows); 2-D shapely
clearances in the plate; discrete curvature of the tube routes; valve-tip margins to anvil-top features."""
from __future__ import annotations

import itertools
import json
import math

import cadquery as cq
from shapely.geometry import LineString, Point, box

from .. import interface as I
from . import assy
from . import geom as G
from . import parts as P

TOL_VOL = 1e-3   # mm^3
# designed contacts / fits that are not interferences (pressed, bonded, threaded or nested by design)
ALLOWED = [("pogo_guide_pins", "pogo_guide_block"), ("pogo_guide_pins", "pogo_block"), ("Md_post", "Md_Zunit"),
           ("Md_post", "Md_holder"), ("pogo_probes", "pogo_block"), ("gamry_cable", "ebay_cable_gland_env"),
           ("pogo_wedge", "pogo_guide_block"), ("tube_", "insert_"), ("tube_", "retainer"),
           ("tube_P_cf", "cold_block"), ("tube_P_cf", "foam_insulation"), ("insert_P_cf", "foam_insulation"),
           ("Mc1_pivot_shafts", "Mc1_"), ("Mc2_pivot_shafts", "Mc2_"), ("Md_magnet", "Md_holder"),
           ("thermistor_T_cold", "cold_block"), ("pogo_probes", "CARD"), ("thermistor_T_heatsink", "heatsink"),
           ("pusher_", "nest_frame"), ("pogo_block", "pogo_wedge"), ("latch_catch_plate_env", "latch_bracket")]


def _allowed(a, b):
    for p, q in ALLOWED:
        if (a.startswith(p) and b.startswith(q)) or (b.startswith(p) and a.startswith(q)):
            return True
    return False


def _shape(o):
    return o.val() if isinstance(o, cq.Workplane) and len(o.vals()) == 1 else (
        cq.Compound.makeCompound([v for v in o.vals()]) if isinstance(o, cq.Workplane) else o)


def interference(items, card=False):
    sh = [(n, _shape(s)) for n, s, m, k in items if (k != "reference" or card)]
    bbs = [(n, s, s.BoundingBox()) for n, s in sh]
    hits = []
    for (na, sa, ba), (nb, sb, bb) in itertools.combinations(bbs, 2):
        if (ba.xmax < bb.xmin or bb.xmax < ba.xmin or ba.ymax < bb.ymin or bb.ymax < ba.ymin or
                ba.zmax < bb.zmin or bb.zmax < ba.zmin):
            continue
        if _allowed(na, nb):
            continue
        try:
            v = sa.intersect(sb).Volume()
        except Exception:  # noqa: BLE001
            v = float("nan")
        if v > TOL_VOL or v != v:
            hits.append((na, nb, round(v, 4)))
    return hits


def _sample(path, step=0.25):
    ls = LineString(path)
    n = max(2, int(ls.length / step) + 1)
    return [ls.interpolate(i * ls.length / (n - 1)).coords[0] for i in range(n)]


def md_paths():
    """(label, points, up) for every M_d motion."""
    out = []
    for ch in ("IC1", "IC2"):
        out.append((f"drag_{ch}", _sample(I.DRAG_PATH[ch]), True))
        for k in ("pass1", "pass2", "pass3"):
            out.append((f"gather_{ch}_{k}", _sample(G.GATHER[(ch, k)]), True))
    out.append(("bead_out", _sample(I.BEAD_OUT_PATH), True))
    for k, v in G.TRANSIT_LOWERED.items():
        out.append((f"transit_{k}", _sample(v, 0.5), False))
    # mirror of IC1 transits for IC2
    out.append(("transit_gather_return_IC2", _sample([G.mirror_y(p) for p in G.TRANSIT_LOWERED["gather_return_IC1"]], 0.5), False))
    return out


def md_sweep_check():
    """M_d moving parts + Z unit + umbrella + adapter at every sample vs every static part (both M_c parked) and
    vs both M_c units UP (for the positions used while the other chamber collects: park only)."""
    th = G.MC_THETA_PARK
    static = [(n, s, m, k) for n, s, m, k in assy.static_items()] + P.mc_unit(1, th) + P.mc_unit(2, th)
    static += [("pogo_block", P.pogo_block(True), "PEEK", "custom")]
    static += [x for x in P.pogo_guide_and_wedge(True)]
    static_sh = [(n, _shape(s)) for n, s, m, k in static if not n.startswith("Md_")]
    bbs = [(n, s, s.BoundingBox()) for n, s in static_sh]
    res = {}
    for label, pts, up in md_paths():
        worst = []
        for (x, y) in pts[:: max(1, len(pts) // 60)] + [pts[-1]]:
            mov = P.md_moving((x, y), up) + P.md_carriage((x, y))
            for nm, s, m, k in mov:
                sa = _shape(s)
                ba = sa.BoundingBox()
                for nb, sb, bb in bbs:
                    if (ba.xmax < bb.xmin or bb.xmax < ba.xmin or ba.ymax < bb.ymin or bb.ymax < ba.ymin or
                            ba.zmax < bb.zmin or bb.zmax < ba.zmin):
                        continue
                    v = sa.intersect(sb).Volume()
                    if v > TOL_VOL:
                        worst.append((round(x, 2), round(y, 2), nm, nb, round(v, 3)))
        res[label] = {"n_samples": len(pts), "up": up, "collisions": worst[:10], "n_collisions": len(worst)}
    return res


def plate_clearance_2d():
    """Min plan clearance of the M_d holder (D2.6 round, Rev C; was 2.6 sq) and neck to the plate openings along all up-paths,
    and of the post (D4) to the plate underside features while lowered (Derived with shapely)."""
    openings = G.through_openings()
    h = G.MD_HOLDER[0] / 2
    res = {}
    for label, pts, up in md_paths():
        if not up:
            continue
        mins = []
        for (x, y) in pts:
            sq = Point(x, y).buffer(h, quad_segs=16)   # (revised after review) round D2.6 holder (interface Rev C)
            inside = openings.contains(sq)
            mins.append((openings.exterior.distance(sq) if hasattr(openings, "exterior") else
                         min(g.exterior.distance(sq) for g in openings.geoms if g.intersects(sq) or g.contains(sq)),
                         inside))
        res[label] = {"min_clearance_holder_to_opening_edge": round(min(m for m, _ in mins), 3),
                      "always_inside": all(i for _, i in mins)}
    return res


def tube_bend_radii():
    res = {}
    for k in G.TUBE_PORTS:
        pts = G.tube_route(k)
        rmin = float("inf")
        for a, b, c in zip(pts[:-2], pts[1:-1], pts[2:]):
            A, B, Cc = (math.dist(b, c), math.dist(a, c), math.dist(a, b))
            s = (A + B + Cc) / 2
            area = max(s * (s - A) * (s - B) * (s - Cc), 0.0) ** 0.5
            if area > 1e-9:
                rmin = min(rmin, A * B * Cc / (4 * area))
        res[k] = round(rmin, 2)
    return res


def tip_margins():
    """Valve-tip edge distance to every anvil-top feature (openings, M_w recess, gasket seats, cold-zone seams)."""
    feats = {"openings": G.through_openings(), "M_w_recess": G.mw_recess_poly(),
             "gaskets": None, "cold_seam": box(G.COLD_PLATE["x"][0], G.COLD_PLATE["y"][0], G.COLD_CUTOUT["x"][1],
                                              G.COLD_PLATE["y"][1]).exterior}
    from shapely.ops import unary_union
    feats["gaskets"] = unary_union([Point(I.PORTS[k].xy).buffer(G.PORT_BORE_D / 2) for k in G.LIQ_PORTS])
    feats["cold_cutout_edge"] = box(G.COLD_CUTOUT["x"][0], G.COLD_CUTOUT["y"][0], G.COLD_CUTOUT["x"][1],
                                    G.COLD_CUTOUT["y"][1]).exterior
    res = {}
    for vid, v in I.VALVES.items():
        tip = Point(v.xy).buffer(v.tip_d / 2)
        d = {k: round(f.distance(tip), 3) for k, f in feats.items()}
        res[vid] = {"klass": v.klass, "min_mm": min(d.values()), "nearest": min(d, key=d.get)}
    return res


MODULE_PREFIX = ("anvil", "nest_frame", "datum", "pusher", "guide_bush", "gasket", "insert", "ret_", "tube_", "heater",
                 "peek_break", "cold_block", "peltier", "heatsink", "fan_env", "exhaust", "foam", "M_w", "ebay", "pogo",
                 "WE_relay", "RH_", "thermistor", "card_presence", "Mc", "latch_")   # latch brackets: on the anvil
#                (revised at integration)


def service_lift(dz_list=(5, 10, 20, 40, 60, 90, 120)):
    """Anvil module (everything except bay frame, M_d system, Gamry cable) lifted straight up in state 'load'
    (M_c parked, M_d parked lowered, pogo down): intersections with the parts that stay."""
    items = [it for it in assy.state_items("load", card=False)]
    mod = [(n, _shape(s)) for n, s, m, k in items if n.startswith(MODULE_PREFIX)]
    stay = [(n, _shape(s)) for n, s, m, k in items if not n.startswith(MODULE_PREFIX) and n != "gamry_cable"]
    res = {}
    for dz in dz_list:
        hits = []
        for na, sa in mod:
            sa2 = sa.translate(cq.Vector(0, 0, dz))
            ba = sa2.BoundingBox()
            for nb, sb in stay:
                bb = sb.BoundingBox()
                if (ba.xmax < bb.xmin or bb.xmax < ba.xmin or ba.ymax < bb.ymin or bb.ymax < ba.ymin or
                        ba.zmax < bb.zmin or bb.zmax < ba.zmin):
                    continue
                v = sa2.intersect(sb).Volume()
                if v > TOL_VOL:
                    hits.append((na, nb, round(v, 3)))
        res[f"lift_{dz}mm"] = hits
    return res


def run(states=None, md=True):
    out = {"interference": {}, "tube_bend_radius_min": tube_bend_radii(), "tip_margins": tip_margins(),
           "plate_clearance_2d": plate_clearance_2d()}
    for st in (states or list(G.STATES)):
        out["interference"][st] = interference(assy.state_items(st))
        out["interference"][st + "+card"] = [h for h in interference(assy.state_items(st), card=True)
                                            if "CARD" in h[0] or "CARD" in h[1]]
    out["service_lift"] = service_lift()
    if md:
        out["md_sweep"] = md_sweep_check()
    return out
