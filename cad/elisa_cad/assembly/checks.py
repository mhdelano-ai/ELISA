"""One-off cross-module checks on the REAL geometry (docs/23 §4). Run by build.py; results -> out/assembly/checks.json.

Method: axis-aligned bounding-box prefilter, then OCC Boolean common volume for every overlapping pair of items from
DIFFERENT modules (module-internal pairs were checked by the module agents). Volume > TOL_VOL counts. Designed
contacts/compressions are classified by INTENDED (and their volume is reported against the expected value).
Feature checks (pins in bores and on channels, ports, pogo, datums, pad, gas rings, vents, contact areas, guide
pins, lid sweep, tube hand-over) are explicit functions below.
"""
from __future__ import annotations

import itertools
import math

import cadquery as cq
import numpy as np

from .. import interface as I
from . import collect as K

TOL_VOL = 1e-4      # mm^3
ORIGIN = np.array(I.CARD_ORIGIN_IN_DOCK)

def _pin_tpe_expected(name):
    """(revised after review, docs/24 M8) expected pin x TPE volume: tip land (0.1 high, tip D) + shank (pin D) from the
    closed tip height (interface Rev C 0.50) to the TPE top 0.715 (Derived)."""
    v = I.VALVES[name.split("pin_")[1]]
    if v.fail == "open":
        return 0.0
    d = I.Z_L2[1] - I.PLUNGER["tip_z_closed"]
    return math.pi / 4 * (v.tip_d ** 2 * min(0.1, d) + v.pin_d ** 2 * max(0.0, d - 0.1))


_GASKET_EXP = math.pi / 4 * (I.FACE_SEAL["gasket_od"] ** 2 - I.FACE_SEAL["gasket_id"] ** 2) * \
    (I.FACE_SEAL["gasket_t"] - I.FACE_SEAL["counterbore_depth"])      # annulus x 0.12 compression (Derived)

# ((module, name prefix), (module, name prefix), reason, expected volume mm^3 (number or f(name of the first item)),
#  relative tolerance). (revised after review, docs/24 M8): every designed contact now has an expected volume; a pair of
# an intended class whose volume departs from it by more than the tolerance (or by > 0.01 mm^3 when ~0) is UNINTENDED.
# Rev B's pin x L1 rule is gone: at the Rev C closed height 0.50 no pin may touch L1.
INTENDED = [
    (("UPPER", "pin_"), ("CARD", "L2_TPE"), "closed valve presses the TPE membrane (by design, tip z 0.50)",
     _pin_tpe_expected, 0.15),
    (("UPPER", "press_pad_silicone"), ("CARD", "die_glass"), "die-back pad compliance (DIE_PRESS_PAD, by design)",
     0.0, None),
    (("UPPER", "ENV_gas_ring"), ("CARD", "L3_body"), "lid gas ring compression 0.25 (GAS_SEAL_LID, by design)",
     math.pi / 4 * (I.GAS_SEAL_LID["od"] ** 2 - I.GAS_SEAL_LID["id"] ** 2) * I.GAS_SEAL_LID["compression"], 0.15),
    (("UPPER", "ENV_gas_ring"), ("CARD", "L4_"), "gas ring over the P_c PTFE disc recess rim (checked §4.6)", 0.0, None),
    (("LOWER", "gasket_"), ("CARD", "L0_foil"), "face-seal compression 0.12 (FACE_SEAL, by design)", _GASKET_EXP, 0.10),
    (("LOWER", "pogo_probes"), ("CARD", "die_"), "pogo tips on the die pads (by design)", 0.0, None),
    (("LOWER", "tube_"), ("BASE", "tube:"), "tube hand-over at the LOWER claim wall (same tube, two owners)", 0.0, None),
]
ZERO_CONTACT_MAX = 0.01     # mm^3: 'contact' classes may only touch (faceting)


def _intended(a, b, vol=None):
    """Reason string if (a, b) is a designed contact AND its volume matches the expected value; else None."""
    for (ma, pa), (mb, pb), why, exp, rtol in INTENDED:
        if a["module"] == ma and a["name"].startswith(pa) and b["module"] == mb and b["name"].startswith(pb):
            first = a["name"]
        elif b["module"] == ma and b["name"].startswith(pa) and a["module"] == mb and a["name"].startswith(pb):
            first = b["name"]
        else:
            continue
        if vol is None:
            return why
        e = exp(first) if callable(exp) else exp
        ok = (vol <= ZERO_CONTACT_MAX) if rtol is None else (abs(vol - e) <= rtol * e + 0.005)
        return (why + f" [expected {e:.3f} mm3]") if ok else None
    return None


def _bb(s):
    b = s.BoundingBox()
    return (b.xmin, b.ymin, b.zmin, b.xmax, b.ymax, b.zmax)


def _ov(a, b, eps=1e-6):
    return not (a[3] <= b[0] + eps or b[3] <= a[0] + eps or a[4] <= b[1] + eps or b[4] <= a[1] + eps or
                a[5] <= b[2] + eps or b[5] <= a[2] + eps)


def common_volume(sa, sb):
    try:
        return sa.intersect(sb).Volume()
    except Exception:  # noqa: BLE001
        return float("nan")


def cross_interference(items, modules_pairs=None):
    """All cross-module overlapping pairs. Returns (unintended, intended, n_pairs_tested)."""
    bbs = [_bb(it["shape"]) for it in items]
    bad, good, n = [], [], 0
    for i, j in itertools.combinations(range(len(items)), 2):
        a, b = items[i], items[j]
        if a["module"] == b["module"]:
            continue
        if modules_pairs and {a["module"], b["module"]} not in modules_pairs:
            continue
        if not _ov(bbs[i], bbs[j]):
            continue
        n += 1
        v = common_volume(a["shape"], b["shape"])
        if v != v or v > TOL_VOL:
            rec = (a["module"] + ":" + a["name"], b["module"] + ":" + b["name"], round(v, 4))
            why = _intended(a, b, v) if v == v else None
            (good if why else bad).append(rec + ((why,) if why else ()))
    return bad, good, n


# ----------------------------------------------------------------------------------------------- feature checks
def _get(items, module, name):
    return K.by_name(items, module, name)["shape"]


def _cardpt(x, y, z):
    return cq.Vector(*(ORIGIN + np.array([x, y, z])))


def pins_in_bores(items):
    """Each of the 21 lid pins (closed state): no contact with the real L3 body; tip centre on its channel (point in
    an L1 cut at z 0.23); tip disc covered by TPE (8 points on 0.95 r inside L2); radial clearance in the bore."""
    l3 = _get(items, "CARD", "L3_body")
    l1 = _get(items, "CARD", "L1_channel_sheet")
    l2 = _get(items, "CARD", "L2_TPE")
    res = {}
    for vid, v in I.VALVES.items():
        pin = _get(items, "UPPER", f"pin_{vid}")
        bb = pin.BoundingBox()
        x, y = (bb.xmin + bb.xmax) / 2 - ORIGIN[0], (bb.ymin + bb.ymax) / 2 - ORIGIN[1]
        tipz = bb.zmin - ORIGIN[2]
        vol_l3 = common_volume(pin, l3)
        vol_l1 = common_volume(pin, l1)   # (revised after review) Rev C closed height 0.50: must be 0
        d_l3 = pin.distance(l3)
        in_channel = not l1.isInside(_cardpt(v.xy[0], v.xy[1], 0.23))
        r = 0.95 * v.tip_d / 2
        tpe_cover = all(l2.isInside(_cardpt(v.xy[0] + r * math.cos(a), v.xy[1] + r * math.sin(a), 0.5))
                        for a in np.linspace(0, 2 * math.pi, 8, endpoint=False))
        res[vid] = {"tip_xy_err": round(math.hypot(x - v.xy[0], y - v.xy[1]), 4), "tip_z": round(tipz, 3),
                    "vol_in_L3": round(vol_l3, 5), "vol_in_L1": round(vol_l1, 5), "min_gap_to_L3": round(d_l3, 3), "tip_on_channel": in_channel,
                    "tip_covered_by_TPE": tpe_cover}
    ok = all(r["vol_in_L3"] <= TOL_VOL and r["vol_in_L1"] <= TOL_VOL and r["tip_on_channel"] and r["tip_covered_by_TPE"] and r["tip_xy_err"] < 0.01
             for k, r in res.items() if k != "V3") and res["V3"]["vol_in_L3"] <= TOL_VOL
    return {"ok": ok, "per_valve": res,
            "note": "V3 is drawn OPEN (de-energised, fail-open): tip 0.8 above closed"}


def ports(items):
    """11 liquid ports: foil hole present in the real L0 at the port, gasket concentric and compressing only foil
    (common volume vs the full annulus x 0.12), no other foil hole under the gasket."""
    l0 = _get(items, "CARD", "L0_foil")
    exp = math.pi / 4 * (I.FACE_SEAL["gasket_od"] ** 2 - I.FACE_SEAL["gasket_id"] ** 2) * \
        (I.FACE_SEAL["gasket_t"] - I.FACE_SEAL["counterbore_depth"])
    res = {}
    for k, p in I.PORTS.items():
        if p.kind != "liquid":
            continue
        g = _get(items, "LOWER", f"gasket_{k}")
        ins = _get(items, "LOWER", f"insert_{k}")
        bb = g.BoundingBox()
        cx, cy = (bb.xmin + bb.xmax) / 2 - ORIGIN[0], (bb.ymin + bb.ymax) / 2 - ORIGIN[1]
        hole = not l0.isInside(_cardpt(p.xy[0], p.xy[1], 0.07))
        vg = common_volume(g, l0)
        res[k] = {"foil_hole_at_port": hole, "gasket_centre_err": round(math.hypot(cx - p.xy[0], cy - p.xy[1]), 4),
                  "gasket_foil_overlap_mm3": round(vg, 4), "expected_mm3": round(exp, 4),
                  "insert_vs_foil_mm3": round(common_volume(ins, l0), 5)}
    ok = all(r["foil_hole_at_port"] and r["gasket_centre_err"] < 0.01 and abs(r["gasket_foil_overlap_mm3"] -
             r["expected_mm3"]) < 0.02 * r["expected_mm3"] and r["insert_vs_foil_mm3"] <= TOL_VOL
             for r in res.values())
    return {"ok": ok, "per_port": res}


def pogo(items):
    """Pogo probes (read state, block up): pass the real contact window (no overlap with L0/L1/L3/L1b), tips at the
    pad plane, each tip on a pad."""
    probes = _get(items, "LOWER", "pogo_probes")
    res = {"vol_vs": {}}
    for n in ("L0_foil", "L1_channel_sheet", "L1b_die_film", "L2_TPE", "L3_body", "seam_adhesive"):
        res["vol_vs"][n] = round(common_volume(probes, _get(items, "CARD", n)), 5)
    tips = []
    for s in probes.Solids():
        bb = s.BoundingBox()
        tips.append((round((bb.xmin + bb.xmax) / 2 - ORIGIN[0], 3), round((bb.ymin + bb.ymax) / 2 - ORIGIN[1], 3),
                     round(bb.zmax - ORIGIN[2], 4)))
    on_pad = []
    for nm, (px, py) in I.PADS.items():
        hit = [t for t in tips if abs(t[0] - px) <= I.PAD_SIZE[0] / 2 and abs(t[1] - py) <= I.PAD_SIZE[1] / 2]
        on_pad.append((nm, len(hit), hit[0][2] if hit else None))
    res["tips"] = tips
    res["on_pad"] = on_pad
    res["vol_vs_die_metal"] = round(common_volume(probes, _get(items, "CARD", "die_metal")), 6)
    res["ok"] = all(v <= TOL_VOL for v in res["vol_vs"].values()) and all(c == 1 and abs(z - I.DIE_Z[0]) < 0.002
                                                                         for _, c, z in on_pad)
    return res


def datums(items):
    """Datum pins touch the real L3 edges (distance 0, no overlap); pushers touch; nest corner block clears the card
    chamfer (>= 0.3) and a 180-deg-rotated card would hit it."""
    l3 = _get(items, "CARD", "L3_body")
    res = {}
    for n in ("datum_pin_A1", "datum_pin_A2", "datum_pin_B", "pusher_A", "pusher_B"):
        s = _get(items, "LOWER", n)
        res[n] = {"dist": round(s.distance(l3), 4), "overlap": round(common_volume(s, l3), 5)}
    nest = _get(items, "LOWER", "nest_frame")
    res["nest_frame_to_card_min"] = round(nest.distance(l3), 3)
    # wrong orientation: card rotated 180 deg about z through its centre
    c = cq.Vector(*(ORIGIN + np.array([I.CARD_L / 2, I.CARD_W / 2, 0])))
    rot = l3.rotate(c, c + cq.Vector(0, 0, 1), 180)
    res["rotated_card_vs_nest_mm3"] = round(common_volume(rot, nest), 3)
    flip = l3.mirror("YZ", c)   # card turned over left-right (top face still up is impossible; mirror = wrong corner)
    res["mirrored_card_vs_nest_mm3"] = round(common_volume(flip, nest), 3)
    res["ok"] = all(res[n]["dist"] < 0.005 and res[n]["overlap"] <= TOL_VOL
                    for n in ("datum_pin_A1", "datum_pin_A2", "datum_pin_B")) and res["nest_frame_to_card_min"] >= 0.29 \
        and res["rotated_card_vs_nest_mm3"] > 1.0
    return res


def press_pad_gas_vents(items):
    die = _get(items, "CARD", "die_glass")
    l3 = _get(items, "CARD", "L3_body")
    l4 = _get(items, "CARD", "L4_discs") if any(it["name"] == "L4_discs" for it in items) else None
    res = {}
    sil = _get(items, "UPPER", "press_pad_silicone")
    bb = sil.BoundingBox()
    res["pad_vs_die_mm3"] = round(common_volume(sil, die), 4)
    res["pad_footprint_card"] = [round(bb.xmin - ORIGIN[0], 2), round(bb.xmax - ORIGIN[0], 2),
                                 round(bb.ymin - ORIGIN[1], 2), round(bb.ymax - ORIGIN[1], 2)]
    res["pad_inside_die"] = (bb.xmin - ORIGIN[0] >= I.DIE_X[0] - 1e-6 and bb.xmax - ORIGIN[0] <= I.DIE_X[1] + 1e-6 and
                             bb.ymin - ORIGIN[1] >= I.DIE_Y[0] - 1e-6 and bb.ymax - ORIGIN[1] <= I.DIE_Y[1] + 1e-6)
    res["pad_vs_L3_mm3"] = round(common_volume(sil, l3), 5)
    foot = _get(items, "UPPER", "press_pad_stem_foot")
    res["pad_foot_vs_L3_mm3"] = round(common_volume(foot, l3), 5)
    # gas rings are drawn seated (compressed state, flush with the head face): check that the ring face lies fully on
    # flat L3 (contact area = full annulus; a bore or lead-in under the ring would reduce it)
    exp = math.pi / 4 * (I.GAS_SEAL_LID["od"] ** 2 - I.GAS_SEAL_LID["id"] ** 2)
    zt = ORIGIN[2] + I.CARD_T
    d = 0.01
    top = l3.intersect(_slab(zt - d, zt))
    for k in ("P_c", "P_mv"):
        r = next(it["shape"] for it in items if it["module"] == "UPPER" and it["name"].startswith(f"ENV_gas_ring_{k}_"))
        rb = r.BoundingBox()
        res[f"gas_ring_{k}_bottom_z_card"] = round(rb.zmin - ORIGIN[2], 4)
        face = r.intersect(_slab(rb.zmin, rb.zmin + d)).translate(cq.Vector(0, 0, zt - d - rb.zmin))
        res[f"gas_ring_{k}_contact_mm2"] = round(common_volume(face, top) / d, 2)
        res[f"gas_ring_{k}_annulus_mm2"] = round(exp, 2)
        res[f"gas_ring_{k}_centre_err"] = round(math.hypot((rb.xmin + rb.xmax) / 2 - ORIGIN[0] - I.PORTS[k].xy[0],
                                                           (rb.ymin + rb.ymax) / 2 - ORIGIN[1] - I.PORTS[k].xy[1]), 4)
    res["pad_to_die_gap"] = round(sil.distance(die), 4)
    hb = _get(items, "UPPER", "heater_block")
    pk = _get(items, "UPPER", "peek_plate")
    res["heater_block_vs_L3_mm3"] = round(common_volume(hb, l3), 5)
    res["peek_plate_vs_L3_mm3"] = round(common_volume(pk, l3), 5)
    parts = [it for it in items if it["module"] == "CARD" and it["name"].startswith("L4")]
    res["head_vs_L4_mm3"] = round(sum(common_volume(hb, p["shape"]) + common_volume(pk, p["shape"]) for p in parts), 5)
    res["ok"] = res["pad_to_die_gap"] < 0.005 and res["pad_inside_die"] and res["pad_vs_L3_mm3"] <= TOL_VOL and \
        res["heater_block_vs_L3_mm3"] <= TOL_VOL and res["peek_plate_vs_L3_mm3"] <= TOL_VOL and \
        res["head_vs_L4_mm3"] <= TOL_VOL and all(res[f"gas_ring_{k}_contact_mm2"] > 0.98 * exp
                                                 for k in ("P_c", "P_mv"))
    return res


def _slab(z0, z1):
    return cq.Solid.makeBox(2000, 2000, z1 - z0, cq.Vector(-500, -500, z0))


def contact_areas(items):
    """Area of real contact (mm^2): head face on the L3 top; anvil + cold block + PEEK frame on the foil underside."""
    zt = ORIGIN[2] + I.CARD_T
    zb = ORIGIN[2]
    d = 0.01
    l3 = _get(items, "CARD", "L3_body")
    l0 = _get(items, "CARD", "L0_foil")
    top_card = l3.intersect(_slab(zt - d, zt))
    res = {}
    for n in ("heater_block", "peek_plate", "guide_plate_lower"):
        s = _get(items, "UPPER", n).intersect(_slab(zt, zt + d)).translate(cq.Vector(0, 0, -d))
        res[f"{n}_on_L3_top_mm2"] = round(common_volume(s, top_card) / d, 1)
    bot = l0.intersect(_slab(zb, zb + d))
    for n in ("anvil", "cold_block", "peek_break_frame"):
        s = _get(items, "LOWER", n).intersect(_slab(zb - d, zb)).translate(cq.Vector(0, 0, d))
        res[f"{n}_under_foil_mm2"] = round(common_volume(s, bot) / d, 1)
    res["L3_top_area_mm2"] = round(top_card.Volume() / d, 1)
    res["foil_area_mm2"] = round(bot.Volume() / d, 1)
    return res


def guide_pins(items):
    res = {}
    for k in ("GP1", "GP2"):
        pin = _get(items, "UPPER", f"guide_pin_{k}")
        bush = _get(items, "LOWER", f"guide_bush_{1 if k == 'GP1' else 2}")
        pb, bb = pin.BoundingBox(), bush.BoundingBox()
        res[k] = {"centre_err": round(math.hypot((pb.xmin + pb.xmax - bb.xmin - bb.xmax) / 2,
                                                 (pb.ymin + pb.ymax - bb.ymin - bb.ymax) / 2), 4),
                  "pin_tip_z_card": round(pb.zmin - ORIGIN[2], 3), "bush_top_z_card": round(bb.zmax - ORIGIN[2], 3),
                  "overlap_mm3": round(common_volume(pin, bush), 5)}
    res["ok"] = all(res[k]["centre_err"] < 0.01 and res[k]["overlap_mm3"] <= TOL_VOL for k in ("GP1", "GP2"))
    return res


def tube_handover():
    """LOWER tube end points == BASE route start/end points at the claim walls (interface LIQUID_LINE_EXITS)."""
    from ..dock_base import fluidics as F
    from ..dock_lower import geom as LG
    res = {}
    for k in I.LIQUID_LINE_EXITS:
        e = np.array(I.card_to_dock(LG.tube_route(k)[-1]))
        r = next(r for r in F.ROUTES if r.port == k)
        ends = [np.array(r.pts[0]), np.array(r.pts[-1])]
        d = min(np.linalg.norm(e - q) for q in ends)
        res[k] = {"lower_end": [round(v, 2) for v in e], "gap_mm": round(float(d), 3),
                  "interface": I.LIQUID_LINE_EXITS[k]}
    res["ok"] = all(v["gap_mm"] < 0.05 for k, v in res.items() if k != "ok")
    return res


def lid_sweep(upper_raised, others, step=5.0):
    """Rotate every lid solid of the 'raised' configuration (rotating parts only) 0..85 deg about the hinge and test
    it against every LOWER/BASE/CARD solid (bbox prefilter, Boolean). Returns hits and min clearances."""
    hx, hy, hz = I.LID_HINGE_AXIS["point"]
    rot = [it for it in upper_raised if it["kind"] != "fixed"]
    ob = [(it, _bb(it["shape"])) for it in others]
    hits = []
    n = 0
    angs = list(np.arange(0.0, I.LID_HINGE_AXIS["open_angle_deg"] + 1e-6, step))
    for a in angs:
        for it in rot:
            s = it["shape"].rotate(cq.Vector(hx, hy, hz), cq.Vector(hx + 1, hy, hz), -a)
            b = _bb(s)
            for o, obb in ob:
                if not _ov(b, obb):
                    continue
                n += 1
                v = common_volume(s, o["shape"])
                if v > TOL_VOL:
                    hits.append((round(float(a), 1), it["name"], o["module"] + ":" + o["name"], round(v, 3)))
    # moving lid hardware vs the BASE well partitions (IR-5)
    xs = []
    for it in rot:
        b = _bb(it["shape"])
        xs.append((b[0], b[3], it["name"]))
    xmin = min(xs, key=lambda t: t[0])
    xmax = max(xs, key=lambda t: t[1])
    return {"angles": [float(a) for a in angs], "pairs_tested": n, "hits": hits,
            "moving_lid_x_range": [round(xmin[0], 2), xmin[2], round(xmax[1], 2), xmax[2]],
            "clearance_to_partitions_mm": [round(xmin[0] - _part()["left"][1], 2),
                                           round(_part()["right"][0] - xmax[1], 2)]}


def _part():
    from ..dock_base import params as BP
    return BP.PART_X
