"""One-off checks for DOCK UPPER (run by build.py, results printed and written to out/dock_upper/checks.txt).
Not a test suite: each function returns numbers that docs/20 §4-§5 quote."""
from __future__ import annotations

import math

import cadquery as cq
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp

from elisa_cad import interface as IF
from elisa_cad.dock_upper import params as P
from elisa_cad.dock_upper import parts as Pt

# pairs whose overlap is intended (press fits, inserted parts, compressed seals): (name prefix a, name prefix b)
INTENDED = [
    ("rod_", "piston_"),            # rod pressed into its piston
    ("ENV_magnet_", "piston_"),     # marker magnet bonded into the piston top (drawn on top: touch only)
    ("guide_pin_", "guide_ear_"),   # guide pin pressed into the ear
    ("ENV_gas_barb", "peek_plate"),  # barb screwed into the M3 seat
    ("ENV_hall_DRV5055", "ENV_hall_pcb"),
    ("ENV_gallery_barbs", "gallery_header"),
    ("V8_bush", "peek_plate"),
    ("press_pad_stem_foot", "spring_plate"),
    ("pin_", "CARD_ENV_L0-L2"),     # tip presses the TPE into the channel (channels not in the envelope)
    ("cam_shaft", "cam_eccentrics"), ("cam_shaft", "cam_lever"),     # keyed / pinned on the shaft
    ("umbilical_clamp", "ENV_umbilical_bundle"),
]


def _vol(shape):
    pr = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape, pr)
    return pr.Mass()


def _intended(a, b):
    for p, q in INTENDED:
        if (a.startswith(p) and b.startswith(q)) or (a.startswith(q) and b.startswith(p)):
            return True
    return False


def interference(parts, tol=1e-4, extra=None):
    """Pairwise common volume with a bounding-box prefilter. parts: list of (name, solid, ...)."""
    items = [(n, s.val() if isinstance(s, cq.Workplane) else s) for (n, s, *_r) in parts]
    if extra:
        items += [(n, s.val() if isinstance(s, cq.Workplane) else s) for (n, s, *_r) in extra]
    bbs = [sh.BoundingBox() for _, sh in items]
    hits, npairs = [], 0
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = bbs[i], bbs[j]
            if a.xmax < b.xmin or b.xmax < a.xmin or a.ymax < b.ymin or b.ymax < a.ymin or \
               a.zmax < b.zmin or b.zmax < a.zmin:
                continue
            npairs += 1
            na, nb = items[i][0], items[j][0]
            com = BRepAlgoAPI_Common(items[i][1].wrapped, items[j][1].wrapped)
            v = _vol(com.Shape())
            if v > tol:
                hits.append((na, nb, v, _intended(na, nb)))
    return hits, npairs, len(items)


def claim_check(parts, claim=P.CLAIM, allowed=("guide_pin_", "guide_ear_")):
    """Portions of solids outside the UPPER claim box (volume)."""
    (x0, y0, z0), (x1, y1, z1) = claim
    big = Pt.box(x0 - 500, x1 + 500, y0 - 500, y1 + 500, z0 - 500, z1 + 500).val()
    inside = Pt.box(x0, x1, y0, y1, z0, z1).val()
    outside = big.cut(inside)
    res = []
    for (n, s, *_r) in parts:
        sh = s.val() if isinstance(s, cq.Workplane) else s
        bb = sh.BoundingBox()
        if bb.xmin >= x0 - 1e-6 and bb.xmax <= x1 + 1e-6 and bb.ymin >= y0 - 1e-6 and bb.ymax <= y1 + 1e-6 and \
           bb.zmin >= z0 - 1e-6 and bb.zmax <= z1 + 1e-6:
            continue
        v = _vol(BRepAlgoAPI_Common(sh.wrapped, outside.wrapped).Shape())
        if v > 1e-3:
            res.append((n, round(v, 2), round(bb.zmin, 2), round(bb.ymin, 2), round(bb.ymax, 2),
                        any(n.startswith(a) for a in allowed)))
    return res


def sweep_check(rotating_parts, step=5.0, n_ang=None):
    """Rotate the lid (head raised) 0..85 deg; at each angle check overlap with every other space claim and with
    the operator loading-path box (at 85 deg); report the minimum clearance of the lid above the nest claim."""
    from elisa_cad.dock_upper.assy import rotate_lid
    claims = {k: v["box"] for k, v in IF.SPACE_CLAIMS.items() if k != "UPPER_lid_closed"}
    solids = [(n, s) for (n, s, *_r) in rotating_parts if not n.startswith("guide_pin_")]
    comp = cq.Compound.makeCompound([s.val() for _, s in solids])
    angles = [i * step for i in range(int(IF.LID_HINGE_AXIS["open_angle_deg"] / step) + 1)]
    if angles[-1] != IF.LID_HINGE_AXIS["open_angle_deg"]:
        angles.append(IF.LID_HINGE_AXIS["open_angle_deg"])
    hx, hy, hz = IF.LID_HINGE_AXIS["point"]
    out = {"overlaps": [], "min_z_over_nest": 1e9, "sweep_bbox": None}
    allbb = None
    for a in angles:
        c = comp.rotate(cq.Vector(hx, hy, hz), cq.Vector(hx + 1, hy, hz), -a)
        bb = c.BoundingBox()
        allbb = bb if allbb is None else allbb.add(bb)
        for name, ((x0, y0, z0), (x1, y1, z1)) in claims.items():
            if bb.xmax <= x0 or bb.xmin >= x1 or bb.ymax <= y0 or bb.ymin >= y1 or bb.zmax <= z0 or bb.zmin >= z1:
                continue
            box = Pt.box(x0, x1, y0, y1, z0, z1).val()
            v = _vol(BRepAlgoAPI_Common(c.wrapped, box.wrapped).Shape())
            if v > 1e-3:
                out["overlaps"].append((a, name, round(v, 2)))
        # min z of lid material above the nest footprint (Y <= 185)
        nest = Pt.box(140, 330, 0, IF.SPACE_CLAIMS["LOWER_nest_anvil"]["box"][1][1], 100, 400).val()
        part = BRepAlgoAPI_Common(c.wrapped, nest.wrapped).Shape()
        try:
            zb = cq.Shape.cast(part).BoundingBox().zmin
            out["min_z_over_nest"] = min(out["min_z_over_nest"], zb)
        except Exception:
            pass
        if a == IF.LID_HINGE_AXIS["open_angle_deg"]:
            (x0, y0, z0), (x1, y1, z1) = IF.OPERATOR_LOADING_PATH["clear_box"]
            lb = Pt.box(x0, x1, y0, y1, z0, z1).val()
            out["loading_path_overlap_mm3"] = _vol(BRepAlgoAPI_Common(c.wrapped, lb.wrapped).Shape())
            out["open_bbox"] = (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)
    out["sweep_bbox"] = (allbb.xmin, allbb.xmax, allbb.ymin, allbb.ymax, allbb.zmin, allbb.zmax)
    out["interface_sweep_bbox"] = IF.lid_sweep_bbox()
    return out


def closing_arc():
    """Pin tips (head raised, no card) on the closing arc: lowest tip height above the card top and its angle."""
    hx, hy, hz = IF.LID_HINGE_AXIS["point"]
    worst = (1e9, None, None)
    for vid, v in IF.VALVES.items():
        tipz = P.TIP_Z_CLOSED - (0.0 if vid == "V3" else P.DROP_BELOW_CLOSED) + (P.STROKE if vid == "V3" else 0.0)
        X, Y, Z = IF.card_to_dock((v.xy[0], v.xy[1], tipz + P.HEAD_DROP))
        for i in range(0, 851):
            a = math.radians(i / 10)
            dy, dz = Y - hy, Z - hz
            z = hz - dy * math.sin(a) + dz * math.cos(a)
            h = z - (IF.CARD_TOP_Z_DOCK)
            if h < worst[0]:
                worst = (h, vid, i / 10)
    gp = {}
    for name, (x, y) in P.GUIDE_PINS.items():
        X, Y, Z = IF.card_to_dock((x, y, P.GUIDE_PIN_TIP_Z_RAISED))
        gp[name] = min(hz - (Y - hy) * math.sin(math.radians(i / 10)) + (Z - hz) * math.cos(math.radians(i / 10))
                       for i in range(0, 851)) - (IF.ANVIL_TOP_Z_DOCK + P.Z_NEST_TOP_MAX)
    return dict(min_tip_above_card=worst[0], vid=worst[1], angle=worst[2], guide_pin_min_above_nest=gp)


def descent_sequence():
    """Head descent d = 0..8: guide-pin full-diameter engagement vs valve-pin tips reaching the bore lead-in."""
    nose_full = P.GUIDE_PIN_TIP_Z_RAISED + P.GUIDE_PIN_NOSE        # z of the full-diameter start, raised
    d_guided = nose_full - P.Z_NEST_TOP_MAX                         # bush top assumed at the nest claim top
    tip_raised_lifted = P.TIP_Z_CLOSED + P.STROKE + P.HEAD_DROP      # air on during descent (pins lifted)
    tip_raised_dropped = P.TIP_Z_CLOSED - P.DROP_BELOW_CLOSED + P.HEAD_DROP   # air off
    lead = IF.PLUNGER["card_bore_lead_in"]
    d_tip_lifted = tip_raised_lifted - (IF.CARD_T)
    d_tip_dropped = tip_raised_dropped - (IF.CARD_T)
    capture = min((v.bore_d - v.pin_d) / 2 + lead for v in IF.VALVES.values())
    return dict(d_guide_engaged=d_guided, d_tip_at_card_top_air_on=d_tip_lifted,
                d_tip_at_card_top_air_off=d_tip_dropped, guided_travel_before_bores_air_on=d_tip_lifted - d_guided,
                guided_travel_before_bores_air_off=d_tip_dropped - d_guided, radial_capture_min=capture,
                tol_head_to_nest=IF.TOL["head_to_nest"])


def plan_clearances():
    """2D plan clearances per z-band (blades, eyes, bosses, necks, buttons, rods, springs, collars)."""
    from shapely.geometry import Point, LineString
    res = {}
    vals = list(IF.VALVES.values())
    # spring / collar clearance between neighbouring pins (spring zone)
    smin, cmin = (99, None), (99, None)
    for i, a in enumerate(vals):
        for b in vals[i + 1:]:
            d = math.dist(a.xy, b.xy)
            ra = (P.PIN_SPRINGS[P.valve_class(a)]["Dm"] + P.PIN_SPRINGS[P.valve_class(a)]["d"]) / 2 \
                if a.id != "V3" else (P.V3["open_spring"]["Dm"] + P.V3["open_spring"]["d"]) / 2
            rb = (P.PIN_SPRINGS[P.valve_class(b)]["Dm"] + P.PIN_SPRINGS[P.valve_class(b)]["d"]) / 2 \
                if b.id != "V3" else (P.V3["open_spring"]["Dm"] + P.V3["open_spring"]["d"]) / 2
            if d - ra - rb < smin[0]:
                smin = (d - ra - rb, f"{a.id}-{b.id}")
            ca, cb = P.COLLAR_D[P.pkey(a)] / 2, P.COLLAR_D[P.pkey(b)] / 2
            if d - ca - cb < cmin[0]:
                cmin = (d - ca - cb, f"{a.id}-{b.id}")
    res["spring_spring_min"] = smin
    res["collar_collar_min"] = cmin
    return res


def pin_pitch_min():
    vals = list(IF.VALVES.values())
    best = (99, None)
    for i, a in enumerate(vals):
        for b in vals[i + 1:]:
            d = math.dist(a.xy, b.xy)
            if d < best[0]:
                best = (d, f"{a.id}-{b.id}")
    return best


def mass_and_com(parts):
    dens = {"aluminium": 2.70e-3, "steel": 7.9e-3, "PEEK": 1.32e-3, "copper": 8.8e-3, "PTFE": 2.2e-3,
            "elastomer": 1.2e-3, "NdFeB": 7.5e-3, "pcb": 1.9e-3, "envelope": 1.0e-3, "heater": 1.5e-3}
    m_tot, mx, my, mz = 0.0, 0.0, 0.0, 0.0
    for (n, s, mat, *_r) in parts:
        sh = s.val() if isinstance(s, cq.Workplane) else s
        v = sh.Volume()
        rho = dens.get(mat, 2.0e-3)
        if n.startswith("ENV_SMC"):
            rho = 0.7e-3    # 5 g per valve + bar base, assessment
        if n.startswith("ENV_latch"):
            rho = 0.5e-3
        m = v * rho
        c = sh.Center()
        m_tot += m
        mx += m * c.x
        my += m * c.y
        mz += m * c.z
    return dict(mass_g=m_tot, com=(mx / m_tot, my / m_tot, mz / m_tot))


def lid_torques(com, mass_g):
    hx, hy, hz = IF.LID_HINGE_AXIS["point"]
    dy, dz = com[1] - hy, com[2] - hz
    W = mass_g * 1e-3 * 9.81
    out = []
    for a in (0, 30, 60, 75, 85):
        r = math.radians(a)
        y = dy * math.cos(r) + dz * math.sin(r)       # horizontal offset of the CoM from the axis (neg = front)
        out.append((a, round(-W * y * 1e-3, 3)))      # closing torque N m (+ = wants to close)
    lever = P.CLAIM[1][1] - P.LID_Y[0] + 0.0
    handle_y = P.LID_Y[0] - 17.0
    F_lift = (-W * dy * 1e-3) / ((hy - handle_y) * 1e-3)
    return dict(weight_N=W, torque_closing_Nm=out, F_lift_at_handle_N=F_lift)
