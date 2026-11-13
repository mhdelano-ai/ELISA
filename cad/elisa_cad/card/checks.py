"""One-off checks of card A run on the CAD (not a test suite): volumes from the solids vs docs/13 §2.3 / docs/18,
minimum webs per layer, L3 millability, valve tips vs channels and TPE cover, lid gas-ring lands, registration and
tolerance stack, mass. run_all() -> dict (written to out/card/checks.json by build.py; reported in docs/19 §6)."""
from __future__ import annotations

import math

import cadquery as cq
from shapely.geometry import LineString, Point
from shapely.ops import unary_union

from .. import interface as I
from . import parts as Q
from . import profiles as P

RHO = {  # g/cm^3 = mg/mm^3
    "COC": 1.02,      # TOPAS 5013L-10 TDS (ISO 1183, 1020 kg/m3), topas.com, opened 2026-11-13 (grade family)
    "TPE": 1.0,       # UNVERIFIED (eCOC/TPE class ~0.9-1.2)
    "glass": 2.23,    # UNVERIFIED (borosilicate class)
    "PTFE": 2.2,      # UNVERIFIED (bulk PTFE; ePTFE membrane lower)
    "adhesive": 1.1,  # UNVERIFIED
}


def _vol_cut(probe_poly, z0, z1, solid_wp):
    """Fluid volume inside the probe prism = probe volume - probe ∩ material (from the CAD solids)."""
    probe = Q.poly_solid(probe_poly, z0, z1 - z0)
    pv = Q.volume(probe)
    mat = cq.Compound.makeCompound([s for v in solid_wp.vals() for s in v.Solids()])
    inter = probe.val().intersect(mat)
    return pv - inter.Volume(), inter.Volume()


def volumes():
    r = {}
    zL1, zL2, zL3 = I.Z_L1, I.Z_L2, I.Z_L3
    L1, L2, L3 = Q.L1(), Q.L2(), Q.L3()
    named = P.l1_cut_named()
    hC = I.CHANNEL_H

    def chan_v(k, h=hC, src=None):
        v, res = _vol_cut(named[k], zL1[0], zL1[0] + h, L1)
        return v, res

    # chambers: L1 part (circle minus funnel walls) + L2 circle + L3 blind bore (all from the solids)
    for ic in ("IC1", "IC2"):
        b = I.CHAMBERS[ic]
        c = P.circ(b.center, b.d)
        v1, _ = _vol_cut(c, zL1[0], zL1[1], L1)
        v2, _ = _vol_cut(c, zL2[0], zL2[1], L2)
        v3, res3 = _vol_cut(c, zL3[0], b.z[1], L3)
        tot = v1 + v2 + v3
        A = c.area
        target = 185.0
        h = hC + (target - v1) / A          # fill height above the foil for 185 uL (above L1 the full circle)
        r[ic] = {"total_uL": round(tot, 2), "L1_part": round(v1, 3), "fill_h_185uL_mm": round(h, 3),
                 "docs13": "290 (docs/18 DEV-7: 280) total; 185 working, fill 3.68", "residual_material": round(res3, 4)}
    for k, b in (("RCj", I.RCJ), ("RS", I.RS)):
        g = P.rect_c(b.center, *b.size)
        v12 = g.area * (zL2[1] - zL1[0])          # L1 + L2 cut-outs (square, laser-cut)
        v3, _ = _vol_cut(P.rect_c(b.center, b.size[0] + 1, b.size[1] + 1), zL3[0], b.z[1], L3)
        r[k] = {"L3_uL": round(v3, 1), "L1L2_uL": round(v12, 1), "total_uL": round(v3 + v12, 1),
                "docs13": "RCj 0.50 mL + 0.06 in L1/L2; RS 0.72 mL usable (5.0 deep)", "corner_R": P.TANK_CORNER_R}
    # meter: foil (z 0.14) to stop (z 5.14)
    c = P.circ(I.MC.center, P.MC_D)
    v1, _ = _vol_cut(c, zL1[0], zL1[1], L1)
    v2, _ = _vol_cut(c, zL2[0], zL2[1], L2)
    v3, _ = _vol_cut(c, zL3[0], P.MC_STOP_Z - P.ADH_T, L3)
    adh_gap = (math.pi / 4) * (2.0 ** 2 - P.MC_D ** 2) * P.ADH_T   # annulus under the stop disc inside the ring
    r["MC"] = {"foil_to_stop_uL": round(v1 + v2 + v3 + (math.pi / 4) * P.MC_D ** 2 * P.ADH_T, 3),
               "adhesive_ring_gap_uL": round(adh_gap, 4), "docs13": "10.0 uL (2.0 x 1.0 x 5.0)", "D_mm": round(P.MC_D, 4)}
    for k in ("C1_H1", "C2_H2", "M_in", "WL1", "WL2", "WLc", "conj_line", "conj_leg2", "nozzle1", "nozzle2",
              "A1_rung", "bead_rung", "V11_line", "V12_waste", "RCj_to_MC", "V14_out", "V16_out", "RS_feed"):
        v, _ = chan_v(k)
        r[k] = {"uL": round(v, 3), "length_mm": round(I.polyline_length(I.CHANNELS[k]["pts"]), 3)}
    r["BW"] = {"uL": round(_vol_cut(named["BW"], zL1[0], zL2[1], unary_wp([L1, L2]))[0], 3), "docs13": "3.6"}
    # cell components (height 0.200 under the die: L1 + film)
    film = Q.L1b()
    lf = unary_wp([L1, film])
    rc = _vol_cut(named["RC"], zL1[0], I.Z_L1B[1], lf)[0]
    g3 = _vol_cut(named["G3_finger"].difference(named["RC"]), zL1[0], I.Z_L1B[1], lf)[0]
    g4poly = named["G4_lane"].intersection(P.DIE).difference(named["RC"])
    g4 = _vol_cut(g4poly, zL1[0], I.Z_L1B[1], lf)[0]
    we2 = _vol_cut(P.we2_slot(), zL1[0], I.Z_L1B[1], unary_wp([L1, film, Q.L1s()]))[0]
    cer = _vol_cut(named["CER"], zL1[0], I.Z_L1B[1], lf)[0]
    r["cell"] = {"RC_uL": round(rc, 4), "G3_finger_uL": round(g3, 4), "G4_finger_in_die_uL": round(g4, 4),
                 "WE2_channel_uL": round(we2, 4), "cell_total_uL": round(rc + g3 + g4 + we2, 4),
                 "CER_pocket_neck_uL": round(cer, 4),
                 "docs13": "RC 1.04, fingers 0.115, link + WE2 0.175, cell 1.34; CER 0.044"}
    r["port_hole_uL"] = round(math.pi / 4 * I.PORT_HOLE_D ** 2 * (I.Z_L1[1]), 3)
    # paths (docs/18 DEV-1 numbers)
    h1 = I.CHANNELS["C1_H1"]
    bead_down = LineString([(37.5, 31.0), (39.0, 31.0), (39.0, 34.6)]).length * 0.5 * hC
    bead_rung = (30.75 - 25.0) * I.LINE_W * hC
    r["bead_path_uL"] = {"on_card": round(r["port_hole_uL"] + bead_rung + bead_down, 3),
                         "with_2.5_line": round(2.5 + r["port_hole_uL"] + bead_rung + bead_down, 3),
                         "docs18": "3.54 (DEV-1)"}
    r["conj_to_C1_uL"] = round(r["conj_line"]["uL"], 3)
    r["conj_to_C2_uL"] = round((7.75 + 12.65) * I.LINE_W * hC, 3)
    return r


def unary_wp(wps):
    return cq.Workplane("XY").newObject([cq.Compound.makeCompound([s for w in wps for v in w.vals()
                                                                   for s in v.Solids()])])


# ------------------------------------------------------------------------------------------------ webs
def min_web(material, lo=0.005, hi=3.0, it=22, amin=3e-3):
    """Smallest material width (opening test): largest t for which material.buffer(-t/2).buffer(t/2) keeps
    everything. Returns (t_min, location of the thinnest spot)."""
    def thin(t):
        o = material.buffer(-t / 2, join_style=2, mitre_limit=20).buffer(t / 2 + 1e-4, join_style=2,
                                                                          mitre_limit=20)
        d = material.difference(o)
        return d.area, d
    for _ in range(it):
        mid = (lo + hi) / 2
        a, _ = thin(mid)
        if a > amin:   # ignore corner cusps of polygonised arcs (< 0.003 mm2)
            hi = mid
        else:
            lo = mid
    _, d = thin(hi * 1.05)
    loc = None
    if not d.is_empty:
        parts = list(getattr(d, "geoms", [d]))
        parts = [g for g in parts if g.area > amin / 3] or parts
        big = max(parts, key=lambda g: g.area)
        loc = (round(big.centroid.x, 2), round(big.centroid.y, 2))
    return round(lo, 3), loc


def webs():
    out = {}
    for name, g in (("L0", P.L0()), ("L1", P.L1()), ("L1b", P.L1b()), ("L2", P.L2())):
        out[name] = min_web(g)
    l1 = P.L1()
    out["L1_pieces"] = [round(p.area, 2) for p in getattr(l1, "geoms", [l1])]
    # L3 plan: through features + blind cavities deeper than 1 mm, taken as walls over the full height
    blind = [g for k, (g, zt) in P.l3_blind_bottom().items() if zt - I.Z_L3[0] > 1.0]
    plan = P.l3_outline().difference(unary_union([P.l3_through()] + blind))
    out["L3_plan"] = min_web(plan)
    # pairwise webs between separate L3 cut features (more meaningful than the opening test at relief corners)
    feats = unary_union([P.l3_through()] + blind)
    comps = list(getattr(feats, "geoms", [feats]))
    pw = []
    for i, a in enumerate(comps):
        for b in comps[i + 1:]:
            d = a.distance(b)
            if d < 1.0:
                pa, pb = a.representative_point(), b.representative_point()
                pw.append((round(d, 3), (round(pa.x, 1), round(pa.y, 1)), (round(pb.x, 1), round(pb.y, 1))))
    edge = [(round(c.distance(P.l3_outline().exterior), 3), (round(c.centroid.x, 1), round(c.centroid.y, 1)))
            for c in comps if c.distance(P.l3_outline().exterior) < 2.0 and not c.intersects(
                P.l3_outline().exterior)]
    out["L3_feature_pairs_below_1mm"] = sorted(pw)
    out["L3_feature_to_card_edge_below_2mm"] = sorted(edge)
    # pairwise bore webs (before merging) that are below 1.0
    pairs = []
    ids = list(I.VALVES)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            va, vb = I.VALVES[a], I.VALVES[b]
            w = math.dist(va.xy, vb.xy) - (va.bore_d + vb.bore_d) / 2
            if w < 1.0:
                pairs.append((a, b, round(w, 3)))
    out["bore_pairs_web_below_1mm"] = pairs
    out["extra_merges"] = P.l3_bore_groups()[2]
    # bores to the die window (non-notched) and to cavities
    feat = {"die_window": P.die_window()[1]}
    feat.update({k: g for k, (g, _) in P.l3_blind_bottom().items()})
    near = []
    for k, v in I.VALVES.items():
        if k in I.DIE_NOTCHED_BORES:
            continue
        for fk, g in feat.items():
            d = P.circ(v.xy, v.bore_d).distance(g)
            if d < 1.5:
                near.append((k, fk, round(d, 3)))
    out["bore_to_cavity_below_1.5"] = near
    out["thin_floors"] = {"chamber/tank roof": I.CHAMBER_ROOF_T,
                          "under vent recess": round(I.CHAMBER_ROOF_T - P.VENT_RECESS_T, 3),
                          "MC counterbore ledge (annulus D1.596-D3.4)": round((P.MC_CBORE_D - P.MC_D) / 2, 3)}
    return out


def millability():
    t = []
    L3h = I.L3_T
    t.append(("plunger bores D1.5", 1.5, L3h, "twist drill + reamer", round(L3h / 1.5, 2)))
    t.append(("plunger bores D1.2 / D1.3 (slot valves, revised after review) / merged slots 1.3 wide / notches", 1.2, L3h,
              "drill D1.2 / D1.3; slots + notches: D1.0 end mill from both faces (2 x 2.75)", round(2.75 / 1.0, 2)))
    t.append(("die window corner reliefs D1.0", 1.0, L3h, "D1.0 end mill, both faces", 2.75))
    t.append(("MC D1.596 blind 4.4 deep", P.MC_D, P.MC_STOP_Z - P.ADH_T - I.Z_L3[0], "flat-bottom drill/end mill D1.5 "
              "+ circular interpolation", round((P.MC_STOP_Z - P.ADH_T - I.Z_L3[0]) / 1.5, 2)))
    t.append(("RCj/RS corners R1.0, 5.0 deep", 2.0, 5.0, "D2 end mill (roughing D6)", 2.5))
    t.append(("chambers D8 x 5.0", 8.0, 5.0, "D6 end mill, helical", round(5.0 / 6.0, 2)))
    t.append(("thermal slot 4 wide, R1.0 ends", 2.0, L3h, "D2 end mill from both faces", 2.75))
    t.append(("vent / P_c recess D4.4 x 0.3, MC counterbore D3.4", 3.0, 1.1, "D3 end mill", 0.37))
    t.append(("lead-ins 0.3 x 45 deg", 0, 0.3, "90 deg spot/chamfer tool", 0))
    return [dict(zip(("feature", "tool_d", "depth", "process", "L_over_D"), x)) for x in t]


# ------------------------------------------------------------------------------------------------ tips
TIP_CHANNEL = {"V1": "V1_bridge", "V2": "V2_bridge", "V3": "M_in", "V4": "bead_rung", "V5": "bead_rung",
               "V6": "conj_line", "V7": "conj_leg2", "V8": "RCj_to_MC", "V9": "nozzle1", "V10": "nozzle2",
               "V11": "V11_line", "V12": "V12_waste", "V14": "V14_out", "V15": "RS_feed", "V16": "V16_out",
               "V17": "A1_rung", "V18": "A1_rung", "G1": "WL1", "G2": "WL2", "G3": "WLc", "G4": "G4_lane"}


def tips():
    l2 = P.L2()
    named = P.l1_cut_named()
    through = P.l3_through()
    res = []
    for k, v in I.VALVES.items():
        ch = I.CHANNELS[TIP_CHANNEL[k]]
        line = LineString(ch["pts"])
        d = line.distance(Point(v.xy))
        r_tip = v.tip_d / 2
        lat = r_tip - (d + ch["w"] / 2)               # lateral overlap margin of the tip beyond the channel walls
        wc_dir = I.valve_tip_lateral_wc_dir(k)        # (revised after review) worst case on the channel normal
        disc = P.circ(v.xy, v.tip_d)
        tpe_ok = disc.buffer(P.TIP_TOL_WC).within(l2.buffer(1e-6))
        tpe_margin = round(min(disc.distance(g.boundary) for g in P.l2_cut_named().values()), 3)
        others = [n for n, g in named.items() if n != TIP_CHANNEL[k] and disc.intersection(g).area > 1e-6]
        bore_ok = disc.buffer(I.TOL["pin_in_card_bore_radial_clearance_min"] - 1e-3).within(through.buffer(1e-6))
        #   (revised after review) 1e-3 instead of 1e-6: D1.0 slot pin = tip in a D1.3 bore is exactly 0.15 radial,
        #   and the 128-segment bore polygon lies up to 2e-4 inside the true circle (faceting)
        res.append({"id": k, "channel": TIP_CHANNEL[k], "centre_off_mm": round(d, 4),
                    "lateral_margin_mm": round(lat, 3), "lateral_ok_WC": lat >= wc_dir, "lateral_WC_dir_mm": round(wc_dir, 3),
                    "TPE_full_cover_with_WC_tol": bool(tpe_ok), "tip_to_nearest_TPE_cut_mm": tpe_margin,
                    "other_cuts_touched": others, "tip_inside_L3_bore_with_clearance": bool(bore_ok)})
    return res


def gas_ring_lands():
    """Lid gas rings (ID 5 / OD 7) must lie on flat L3 top: no bore, lead-in, recess or slot inside the annulus."""
    top_feats = [P.l3_through(), P.circ(I.MC.center, P.MC_CBORE_D)]
    for k, c in P.vent_sites().items():
        if k != "vent_P_c":
            top_feats.append(P.circ(c, P.VENT_RECESS_D))
    for k, v in I.VALVES.items():
        li = P.LEAD_IN_LOCAL.get(k, P.LEAD_IN)
        top_feats.append(P.circ(v.xy, v.bore_d + 2 * li))
    tf = unary_union(top_feats)
    out = {}
    for pid in ("P_c", "P_mv"):
        c = I.PORTS[pid].xy
        ring = P.circ(c, I.GAS_SEAL_LID["od"]).difference(P.circ(c, I.GAS_SEAL_LID["id"]))
        own = P.circ(c, P.VENT_RECESS_D if pid == "P_c" else P.MC_CBORE_D)
        out[pid] = {"overlap_mm2": round(ring.intersection(tf.difference(own)).area, 4),
                    "clear_to_nearest_feature_mm": round(ring.distance(tf.difference(own)), 3),
                    "inner_land_mm": round((I.GAS_SEAL_LID["id"] - own.bounds[2] + own.bounds[0]) / 2, 3)}
    # same with the interface lead-in 0.3 at V8 (to justify CHOICE-C10)
    v8 = I.VALVES["V8"]
    c = I.PORTS["P_mv"].xy
    out["P_mv_with_V8_leadin_0.3_overlap_mm"] = round(
        I.GAS_SEAL_LID["od"] / 2 + v8.bore_d / 2 + P.LEAD_IN - math.dist(c, v8.xy), 3)
    return out


def registration():
    tol = I.TOL
    wc = tol["head_to_nest"] + tol["datum_pin_position"] + tol["card_edge_to_feature"] + tol["L1_to_L3_registration"]
    rss = math.sqrt(tol["head_to_nest"] ** 2 + tol["datum_pin_position"] ** 2 + tol["card_edge_to_feature"] ** 2
                    + tol["L1_to_L3_registration"] ** 2)
    # L1-to-L3 budget at J and the cell from the lamination pins (CHOICE-C4) [assessment / UNVERIFIED items]
    budget = {"laser position L1 (UNVERIFIED class)": 0.010, "dowel D2.0 in L1 hole (+0.02 clearance, half)": 0.010,
              "L1 shrink/stretch after bonding, 0.05 % over 20 mm (UNVERIFIED)": 0.010,
              "L3 dowel hole position (milled, [assessment])": 0.010, "dowel in L3 hole H7 (half clearance)": 0.006,
              "rotation about the round pin: slot clearance 0.01 over 37 mm, at 20 mm": 0.005}
    reg_wc = sum(budget.values())
    reg_rss = math.sqrt(sum(x * x for x in budget.values()))
    stub = {"stub_nominal_0.30": (0.30 - rss, 0.30 + rss), "cell_stub_0.35": (0.35 - rss, 0.35 + rss)}
    die = {"die_in_window": tol["die_in_window"], "WE1 opening inset in RC (per side)": 0.05,
           "film-to-die (film placed on pins, die on L3 datums): L1/L1b vs die WC": round(reg_wc + 0.05, 3)}
    return {"tip_to_channel_WC": round(wc, 3), "tip_to_channel_RSS": round(rss, 3),
            "L1_to_L3_budget": budget, "L1_to_L3_WC": round(reg_wc, 3), "L1_to_L3_RSS": round(reg_rss, 3),
            "required_L1_to_L3": tol["L1_to_L3_registration"], "stub_ranges_RSS": {k: (round(a, 3), round(b, 3))
                                                                                    for k, (a, b) in stub.items()},
            "die": die, "pins": {"round": P.PIN_ROUND, "slot": P.PIN_SLOT,
                                 "dist_round_to_J": round(math.dist(P.PIN_ROUND, I.J), 2),
                                 "dist_round_to_RC": round(math.dist(P.PIN_ROUND, I.RC_CENTER), 2)}}


def mass():
    m = {}
    groups = {"COC": ["L0_foil", "L1_channel_sheet", "L1s_WE2_shim", "L3_body"], "TPE": ["L2_TPE"],
              "glass": ["die_glass"], "adhesive": ["L1b_die_film", "seam_adhesive"]}
    parts = {n: w for n, w, _ in Q.all_parts()}
    tot = 0.0
    for mat, names in groups.items():
        v = sum(Q.volume(parts[n]) for n in names)
        m[mat] = {"mm3": round(v, 1), "g": round(v * RHO[mat] / 1000, 3)}
        tot += v * RHO[mat] / 1000
    v = sum(Q.volume(w) for n, w in parts.items() if n.startswith("L4_") and not n.endswith("_adh"))
    m["PTFE"] = {"mm3": round(v, 2), "g": round(v * RHO["PTFE"] / 1000, 4)}
    tot += v * RHO["PTFE"] / 1000
    m["total_dry_g"] = round(tot, 2)
    m["fluids_full_g"] = round((0.26 + 0.6) * 1.0, 2)   # docs/13 §5.2 fills (conjugate 0.26 mL, HQDP 0.6 mL)
    return m


def run_all():
    return {"volumes": volumes(), "webs": webs(), "millability": millability(), "tips": tips(),
            "gas_rings": gas_ring_lands(), "registration": registration(), "mass": mass(),
            "l3_groups": {"merged": P.l3_bore_groups()[0], "extra": P.l3_bore_groups()[2]}}
