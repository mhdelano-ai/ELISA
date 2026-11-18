"""Build the washer punching jig (docs/36): STEP and STL of the printed parts, assembly STEP (stroke 2, the
outside punch at the end of its stroke), renders, section, checks -> cad/out/tier2_cell/punch_jig/.

Run from cad/:   python -m elisa_cad.tier2_cell.jig.build   [--fast: no renders]     (seconds; renders ~7 min)
"""
from __future__ import annotations

import json
import math
import sys

import cadquery as cq

from ... import common as C
from . import params as J
from . import parts as PT

OUT = C.out_dir("tier2_cell/punch_jig")

E_FKM = 5.5          # MPa, Young's modulus of 70 Shore A (Gent's relation; UNVERIFIED for the lot)


def vol(o):
    return C._shape(o).Volume()


def common_volume(a, b):
    try:
        return C._shape(a.intersect(b)).Volume()
    except Exception:
        return 0.0


def foot_area():
    """Area of the foot annulus on the sheet and its shape factor (inner edge taken at the liner bore)."""
    r_in, r_out = J.LINER_ID / 2.0, J.FOOT_D / 2.0      # bushing face + printed foot
    area = math.pi * (r_out ** 2 - r_in ** 2)
    s = area / (2 * math.pi * (r_in + r_out) * J.SHEET_T)
    return area, s


def checks(solids):
    rows = []

    def add(name, ok, value):
        rows.append(dict(check=name, ok=bool(ok), value=value))

    names = list(solids)
    worst = 0.0
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            v = common_volume(solids[a], solids[b])
            worst = max(worst, v)
            if v > 1e-4:
                add(f"no interference {a} / {b}", False, f"{v:.4f} mm3")
    add(f"no interference between any two parts ({len(names)} solids, liner at its largest OD; the punches are "
        f"checked below)", worst <= 1e-4, f"largest common volume {worst:.2e} mm3")
    # punches at the end of the stroke, each in its own bushing, against every part but the strip and backing
    for p in (J.PUNCH_A, J.PUNCH_B):
        pu = PT.punch(p)
        others = {k: v for k, v in solids.items() if k not in ("sheet", "backing", "slip_bushing")}
        others["slip_bushing"] = PT.slip_bushing(p)
        hits = [k for k, v in others.items() if common_volume(pu, v) > 1e-4]
        add(f"{p['name']} at the end of its stroke (nose on the bushing head) clears every part", not hits,
            "none" if not hits else ", ".join(hits))
    # finger: retains the bushing when locked, frees it when swung, at the head's largest diameter and with the
    # finger shifted toward the axis by its play [R2-4]
    head_max = J.SLIP_HEAD_D + 2 * J.HEAD_TOL
    head_min = J.SLIP_HEAD_D - 2 * J.HEAD_TOL
    lift = PT._cyl(head_max, 40.0, 0, 0, J.Z_LINER_TOP + 0.01)
    add("ring finger locked: bears on the whole head rim, also at the smallest head (r_in < head r min - 0.3)",
        J.RING_R_IN <= head_min / 2 - 0.3 and J.RING_R_OUT >= head_max / 2 + 0.3,
        f"ring r {J.RING_R_IN}-{J.RING_R_OUT}, head r {head_min / 2:.2f}-{head_max / 2:.2f}; recesses anywhere")
    swings = [a for a in range(int(J.SWING_MIN), int(J.SWING_STOP) + 1, 7)] + [int(J.SWING_STOP)]
    clear_vol = max(common_volume(PT.finger(-90.0 + sgn * a, J.FINGER_PLAY_DESIGN), lift)
                    for a in swings for sgn in (1, -1))
    d_boss = J.LOCK_R - J.FINGER_PLAY_DESIGN - J.BOSS_D / 2 - head_max / 2
    add(f"finger swung {J.SWING_MIN:.0f}-{J.SWING_STOP:.0f} deg either way (shifted 0.1 toward the axis): a head of the "
        f"largest diameter lifts out freely; boss >= 0.6 from it [R3-4]", clear_vol <= 1e-6 and d_boss >= 0.6,
        f"{clear_vol:.1e} mm3, boss {d_boss:.2f} mm")
    others = {k: v for k, v in solids.items() if k not in ("finger",)}
    hits = []
    for sgn in (1, -1):
        f_sw = PT.finger(-90.0 + sgn * J.SWING_STOP)
        hits += [k for k, v in others.items() if common_volume(f_sw, v) > 1e-4]
    add(f"finger at its stop ({J.SWING_STOP:.0f} deg either way) touches no part", not hits,
        "none" if not hits else ", ".join(sorted(set(hits))))
    f90 = [k for k, v in others.items() if common_volume(PT.finger(0.0), v) > 1e-4]
    add("information: at 90 deg the finger would meet (so it stops earlier, on the thumb head)", True,
        ", ".join(f90) if f90 else "nothing")
    add("nose of the handle passes inside the ring (radial >= 0.3, finger shifted by its play)",
        J.RING_R_IN - J.FINGER_PLAY_DESIGN - J.NOSE_D / 2.0 >= 0.3,
        f"{J.RING_R_IN - J.FINGER_PLAY_DESIGN - J.NOSE_D / 2.0:.2f} mm")
    lo_h, hi_h = J.head_top_range()
    add("finger height is set at assembly: spacer printed high enough to be faced for the highest head, and the "
        "shoulder leaves room for the shims at the lowest", J.SPACER_H + J.FINGER_SET_ALLOW >= hi_h + J.FINGER_GAP
        and J.SHOULDER_L + 0.25 - (hi_h + J.FINGER_GAP) - J.FINGER_T - J.ORING_H >= 0.0
        and lo_h + J.FINGER_GAP > 1.0,
        f"head top {lo_h:.2f}-{hi_h:.2f} above the plate; spacer printed {J.SPACER_H + J.FINGER_SET_ALLOW:.2f}, faced "
        f"to {lo_h + J.FINGER_GAP:.2f}-{hi_h + J.FINGER_GAP:.2f}; shims above {J.SHIMS_ABOVE:.2f} nominal")
    proud = (J.Z_LINER_TOP - J.Z_PLATE_TOP - J.BODY_L_TOL - J.PRINT_TOL,
             J.Z_LINER_TOP - J.Z_PLATE_TOP + J.BODY_L_TOL + J.PRINT_TOL)
    add("bushing head seats on the liner end, not on the plate (liner top above the plate top >= 0.1 over the "
        "tolerances)", proud[0] >= 0.1, f"{proud[0]:.2f}-{proud[1]:.2f} mm")
    liner_bot_lo = J.BODY_L - J.BODY_L_TOL - (J.LINER_L + J.LINER_L_TOL)
    ledge_hi = J.Z_LEDGE - J.Z_FOOT + J.PRINT_TOL
    add("liner floats above its ledge at bonding over the length tolerances and the ledge's position (+-0.2) "
        "(gap >= 0.1); ledge ring >= 1.5 thick [R3-3]",
        liner_bot_lo - ledge_hi >= 0.1 and J.Z_LEDGE - J.Z_FOOT - J.PRINT_TOL >= 1.5,
        f"gap {liner_bot_lo - ledge_hi:.2f} at the worst stack, ring {J.Z_LEDGE - J.Z_FOOT:.2f} +- {J.PRINT_TOL}")
    add("procedure, not computed: bushing face flush with the foot (bonded with the longer bushing; faces matched or "
        "ground) and checked after cure with a straightedge and a 0.02 feeler", True,
        f"0 to -{J.FACE_MATCH} mm (docs/36 section 2.4)")
    # stroke depth
    lo, hi = J.tip_depth_range()
    add("tip depth into the backing at the stop stays in 0.1 to backing - 0.3 (sheet tolerance and the setting)",
        lo >= 0.1 and hi <= J.BACKING_T - 0.3, f"{lo:.2f}-{hi:.2f} mm of {J.BACKING_T}")
    f_lo, f_hi = J.facing_range()
    add("the nose is always faced, never too short (facing >= 0), and keeps >= 5 mm of its length",
        f_lo >= 0.0 and J.NOSE_L - (f_hi - J.NOSE_ALLOW) >= 5.0,
        f"facing {f_lo:.2f}-{f_hi:.2f} mm of {J.NOSE_ALLOW} printed extra")
    gap_head = J.NOSE_L - (J.Z_SHOULDER_TOP + J.SHOULDER_HEAD_H - J.Z_HEAD_TOP) - (hi_h - lo_h) / 2
    add("grip clears the shoulder-screw head at the stop over the head-top tolerance (>= 0.5)", gap_head >= 0.5,
        f"{gap_head:.2f} mm")
    for key, p in (("A", J.PUNCH_A), ("B", J.PUNCH_B)):
        d = J.pocket_depth(p)
        add(f"{p['name']}: tube {J.protrusion():.2f} below the nose, {d:.2f} in the handle (pocket ends in the grip, "
            f">= 3 below its top)", J.NOSE_L <= d <= J.NOSE_L + J.GRIP_L - 3.0, f"pocket {d:.2f} mm")
        hole = p["bore"] + J.PUSH_HOLE_EXTRA
        add(f"{p['name']}: shoulder locates the tube (push hole {hole:.3f} <= bore + 0.02 < tube); the bond carries "
            f"the load",
            hole <= p["bore"] + 0.02 + 1e-9 and hole < p["tube_od"], f"shoulder {(p['tube_od'] - hole) / 2:.3f} mm")
        add(f"{p['name']}: push wire {J.PUSH_WIRE[key]} passes the bore {p['bore']:.3f} with >= 0.05",
            p["bore"] - J.PUSH_WIRE[key] >= 0.05, f"{p['bore'] - J.PUSH_WIRE[key]:.3f} mm")
        b = J.slip_bore(p)
        add(f"{p['name']}: bushing bore {b / J.IN:.4f} in on the nominal tube is in the SF-12 range .0135-.0980 in",
            0.0135 <= b / J.IN <= 0.0980, f"{b:.4f} mm")
    # liner and inserts
    gap = (J.LINER_HOLE_D - (J.LINER_OD_NOM + J.LINER_OD_TOL[1]),
           J.LINER_HOLE_D + 0.015 - (J.LINER_OD_NOM + J.LINER_OD_TOL[0]))
    add("liner bond gap (8.00 H7 hole on the L-20 OD 7.970-7.978) is a clearance of 0.02-0.06 diametral",
        0.02 <= gap[0] and gap[1] <= 0.06, f"{gap[0]:.3f}-{gap[1]:.3f} mm")
    lw = J.LOCK_R - J.LINER_HOLE_D / 2.0 - J.INSERT_HOLE_D / 2.0
    add(f"wall between the liner hole and the shoulder-screw insert >= {J.INSERT_WALL} (ruthex minimum)", lw >= J.INSERT_WALL,
        f"{lw:.2f} mm")
    walls = []
    for x, y in J.SCREW_XY:
        walls.append(min(J.BASE_X / 2 - abs(x), J.BASE_Y / 2 - abs(y)) - J.INSERT_HOLE_D / 2)
        walls += [math.hypot(x - dx, y - dy) - J.INSERT_HOLE_D / 2 - J.DOWEL_D / 2 for dx, dy in J.DOWEL_XY]
    add(f"base: inserts >= {J.INSERT_WALL} from the edge and from the pin holes", min(walls) >= J.INSERT_WALL,
        f"smallest {min(walls):.2f} mm")
    add("shoulder screw: M3 thread fits the plate's insert hole (<= depth - 0.3) and engages >= 4",
        4.0 <= J.SHOULDER_THREAD <= J.INSERT_HOLE_DEPTH - 0.3, f"{J.SHOULDER_THREAD} mm in {J.INSERT_HOLE_DEPTH}")
    add("parking holes for the idle bushing clear the plate, the screws and the rails",
        all(abs(x) - J.PARK_D / 2 >= J.PLATE_X / 2 + 2 and abs(y) - J.PARK_D / 2 >= J.STRIP_W / 2 + J.RAIL_GAP / 2
            + J.RAIL_W + 1 and all(math.hypot(x - sx, y - sy) >= J.SLIP_HEAD_D / 2 + J.THUMB_HEAD_D / 2 + 1
                                   for sx, sy in J.SCREW_XY) for x, y in J.PARK_XY), "ok")
    for nm, t in (("thinnest", -1), ("thickest", 1)):
        z_foot = J.Z_FOOT + t * (J.BACKING_T_TOL + J.SHEET_T_TOL)
        th = J.SCREW_L - J.PLATE_T - z_foot
        add(f"thumb screw engagement at the {nm} stack: >= {J.INSERT_L} (whole insert) and <= hole depth - 0.3",
            J.INSERT_L <= th <= J.INSERT_HOLE_DEPTH - 0.3, f"{th:.2f} mm")
    # concentricity and sizes
    worst_c, rss_c = J.concentricity_budget()
    add("hole-to-outside offset, root-sum-square <= 0.05 (T2C-004: within dia 0.10); acceptance rests on the measured "
        "washers (docs/36 section 5)", rss_c <= J.CONC_LIMIT / 2.0,
        f"RSS {rss_c:.3f}, worst case {worst_c:.3f} mm radial (incl. {J.SHEET_SHIFT} sheet shift)")
    wall_min = (J.PUNCH_B["cut_d"] - J.PUNCH_A["cut_d"]) / 2.0 - worst_c
    add("washer wall at the worst-case offset >= 0.175 (docs/34 functional limit)", wall_min >= 0.175,
        f"{wall_min:.3f} mm")
    for nm, d, nom in (("hole", J.PUNCH_A["cut_d"], J.WASHER_ID), ("outside", J.PUNCH_B["cut_d"], J.WASHER_OD)):
        add(f"{nm} punch edge {d:.3f} within the drawing limits {nom - 0.1:.2f}-{nom + 0.1:.2f}",
            nom - 0.1 - 1e-9 <= d <= nom + 0.1 + 1e-9, f"{d - nom:+.3f} mm from nominal")
    # clamp
    area, sfac = foot_area()
    n_lo, n_hi = (len(J.SCREW_XY) * f for f in J.SCREW_FORCE)
    strain = n_hi / area / (E_FKM * (1 + 2 * sfac ** 2))
    add("information: squeeze of the sheet under the foot at the largest screw force", True,
        f"{strain * J.SHEET_T * 1e3:.1f} um at {n_hi:.0f} N ({n_hi / area:.1f} MPa on {area:.0f} mm2, shape factor "
        f"{sfac:.1f}, E {E_FKM} MPa UNVERIFIED)")
    r_in, r_out = J.LINER_ID / 2.0, J.FOOT_D / 2.0
    r_eff = 2.0 / 3.0 * (r_out ** 3 - r_in ** 3) / (r_out ** 2 - r_in ** 2)
    add("friction under the foot at the smallest screw force: lateral >= 20 N, torque >= 50 N mm",
        J.MU_SHEET * n_lo >= 20.0 and J.MU_SHEET * n_lo * r_eff >= 50.0,
        f"{J.MU_SHEET * n_lo:.0f} N, {J.MU_SHEET * n_lo * r_eff:.0f} N mm at mu {J.MU_SHEET}, {n_lo:.0f} N (UNVERIFIED)")
    xs = [x for x, _y in J.SCREW_XY]
    ys = [y for _x, y in J.SCREW_XY]
    add("the foot lies inside the screw pattern (no rocking line through the foot)",
        min(xs) < 0 < max(xs) and min(ys) < 0 < max(ys) and len(J.SCREW_XY) >= 3, f"{len(J.SCREW_XY)} screws")
    z_min = J.Z_FOOT - J.BACKING_T_TOL - J.SHEET_T_TOL
    add("plate floats: at the thinnest stack the underside outside the relief clears the base by >= 0.4",
        z_min >= 0.4, f"{z_min:.2f} mm")
    add("relief over the strip clears the rails by >= 0.5 and lies over them",
        z_min + J.RECESS_DEPTH - J.RAIL_H >= 0.5 and J.STRIP_W / 2 + J.RAIL_GAP / 2 + J.RAIL_W <= J.RECESS_HALF_W,
        f"{z_min + J.RECESS_DEPTH - J.RAIL_H:.2f} mm; rail outer edge {J.STRIP_W / 2 + J.RAIL_GAP / 2 + J.RAIL_W}")
    add("strip slides under the relief (the plate rides on the strip: clearance = relief depth >= 0.5)",
        J.RECESS_DEPTH >= 0.5, f"{J.RECESS_DEPTH} mm")
    add("the foot lies wholly on the strip, inside the rails, and presses the sheet from the bushing body outwards",
        J.FOOT_D / 2 <= J.STRIP_W / 2 and J.BODY_HOLE_D / 2 - J.LINER_ID / 2 <= 0.3,
        f"foot r {J.BODY_HOLE_D / 2:.2f}-{J.FOOT_D / 2:.2f}, strip half-width {J.STRIP_W / 2}")
    web = J.PITCH - J.WASHER_OD - 0.2
    add("web between washers >= 1.0 at the pitch (outside + 0.2 for the punch bevel)", web >= 1.0, f"{web:.2f} mm")
    eng = J.DOWEL_L - J.DOWEL_IN_BASE - (J.Z_FOOT + J.BACKING_T_TOL + J.SHEET_T_TOL)
    add("dowel engages the plate >= 3 mm at the thickest stack; plate holes a slide fit, base holes a press fit",
        eng >= 3.0 and J.DOWEL_PLATE_FIT[0] > J.DOWEL_D + 0.008 and J.DOWEL_BASE_REAM < J.DOWEL_D + 0.002,
        f"{eng:.2f} mm; plate {J.DOWEL_PLATE_FIT[0]}-{J.DOWEL_PLATE_FIT[1]}, base reamed {J.DOWEL_BASE_REAM}")
    ticks_ok = abs(J.SCALE_X0 % J.PITCH) < 1e-9 and J.SCALE_X0 >= J.PLATE_X / 2
    add("pitch scale ticks on the hole positions, downstream of the plate", ticks_ok,
        f"first tick x = {J.SCALE_X0}, plate edge {J.PLATE_X / 2}")
    return rows


def main(argv=None):
    fast = "--fast" in (argv or sys.argv[1:])
    base, plate = PT.base(), PT.plate()
    printed = [("J-001_base", base), ("J-002_head_plate", plate),
               ("J-003_handle_A", PT.handle(J.PUNCH_A, printed=True)),
               ("J-003_handle_B", PT.handle(J.PUNCH_B, printed=True)),
               ("J-004_spacer", PT.spacer(printed=True)), ("J-005_finger", PT.finger(-90.0))]
    for nm, o in printed:
        C.export_step(o, OUT / f"{nm}.step")
        cq.exporters.export(o, str(OUT / f"{nm}.stl"), exportType="STL", tolerance=0.01, angularTolerance=0.1)
    solids = {"base": base, "plate": plate, "liner": PT.liner(), "slip_bushing": PT.slip_bushing(J.PUNCH_B),
              "backing": PT.backing(), "sheet": PT.sheet(), "spacer": PT.spacer(), "finger": PT.finger(-90.0)}
    solids["shims"], solids["shoulder_screw"] = PT.lock_screw()
    for i, s in enumerate(PT.dowels()):
        solids[f"dowel_{i}"] = s
    for i, s in enumerate(PT.screws()):
        solids[f"screw_{i}"] = s
    for i, s in enumerate(PT.inserts()):
        solids[f"insert_{i}"] = s
    rows = checks(solids)
    mats = {"base": "PEEK", "plate": "PEEK", "spacer": "PEEK", "finger": "PEEK", "backing": "default",
            "sheet": "elastomer"}
    items = [(nm, o, "copper" if nm.startswith("insert") else mats.get(nm, "steel")) for nm, o in solids.items()]
    items.append(("outside_punch", PT.punch(J.PUNCH_B), "default"))
    C.export_step(C.assembly(items, "punch_jig"), OUT / "J-000_assembly.step")
    C.export_step(PT.slip_bushing(J.PUNCH_A), OUT / "slip_bushing_A_hole.step")
    C.export_step(PT.slip_bushing(J.PUNCH_B), OUT / "slip_bushing_B_outside.step")
    for stale in ("slip_bushing_C_membrane.step", "J-004_lock_spacer.step", "J-004_lock_spacer.stl",
                  "J-004_sleeve.step", "J-004_sleeve.stl"):
        (OUT / stale).unlink(missing_ok=True)
    worst_c, rss_c = J.concentricity_budget()
    lo, hi = J.tip_depth_range()
    res = dict(checks=rows, n_checks=len(rows), all_pass=all(r["ok"] for r in rows),
               numbers=dict(z_foot=J.Z_FOOT, plate_t=J.PLATE_T, foot_d=J.FOOT_D, z_head_top=J.Z_HEAD_TOP,
                            protrusion=J.protrusion(), spacer_h=J.SPACER_H, shims_above=J.SHIMS_ABOVE,
                            head_top_range=list(J.head_top_range()), facing_range=list(J.facing_range()), pocket_A=J.pocket_depth(J.PUNCH_A),
                            pocket_B=J.pocket_depth(J.PUNCH_B), tip_depth=[lo, hi],
                            slip_bore_A_in=J.slip_bore(J.PUNCH_A) / J.IN, slip_bore_B_in=J.slip_bore(J.PUNCH_B) / J.IN,
                            concentricity_rss=rss_c, concentricity_worst=worst_c))
    (OUT / "check_results.json").write_text(json.dumps(res, indent=1))
    for r in rows:
        print(("pass  " if r["ok"] else "FAIL  ") + r["check"] + "  [" + str(r["value"]) + "]")
    print(f"{len(rows)} checks")
    if not fast:
        vis = [(o, m) for _nm, o, m in items]
        C.render_png(vis, OUT / "assembly_iso.png", view="iso", title="Washer punching jig (docs/36), stroke 2")
        lift = {"base": 0, "backing": 3, "sheet": 5, "plate": 14, "liner": 26, "slip_bushing": 40, "spacer": 30,
                "finger": 46, "shims": 52, "shoulder_screw": 58, "outside_punch": 75}
        ex = []
        for nm, o, m in items:
            dz = lift.get(nm, 70 if nm.startswith("screw") else (14 if nm == "insert_4" else 0))
            ex.append((o.translate((0, 0, dz)), m))
        C.render_png(ex, OUT / "assembly_exploded.png", view="iso", size=(8, 10), title="Exploded")
        cut_away = C.box_from_corners((-60, -40, -20), (60, 0, 80))       # remove y < 0: the cut face looks at -y
        sec = []
        for _nm, o, m in items:
            try:
                c = o.cut(cut_away)
                if C._shape(c).Volume() > 1e-6:
                    sec.append((c, m))
            except Exception:
                pass
        C.render_png(sec, OUT / "section.png", view="front", title="Section y = 0 (punch axis), stroke 2")
        win = C.box_from_corners((-8, -1, -2), (8, 10, 6))                # only what lies in the detail window
        det = []
        for o, m in sec:
            try:
                c = o.intersect(win)
                if C._shape(c).Volume() > 1e-6:
                    det.append((c, m))
            except Exception:
                pass
        C.render_png(det, OUT / "section_detail.png", view="front", title="Section y = 0: foot, bushing face, sheet, tip",
                     size=(9, 4.5), xlim=(-7, 7), ylim=(-1.0, 6.0))
        C.render_png([(plate, "PEEK")], OUT / "head_plate_underside.png", view="bottom", title="Head plate, underside")
        C.render_png([(base, "PEEK")], OUT / "base_top.png", view="top", title="Base, top")
        C.render_png([(PT.handle(J.PUNCH_B).cut(C.box_from_corners((-20, -20, -1), (20, 0, 40))), "PEEK")],
                     OUT / "handle_B_section.png", view="front", title="Handle B, section")
        C.shrink_pngs(OUT)
    print("all checks pass" if res["all_pass"] else "CHECKS FAILED")
    return 0 if res["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
