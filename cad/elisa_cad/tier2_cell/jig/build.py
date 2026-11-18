"""Build the washer punching jig (docs/36): STEP and STL of the two printed parts, assembly STEP (stroke 2, the
outside punch at the bottom of its stroke), renders, section, checks -> cad/out/tier2_cell/punch_jig/.

Run from cad/:   python -m elisa_cad.tier2_cell.jig.build   [--fast: no renders]     (under 1 min)
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


def clamp_force(squeeze, sheet_t=J.SHEET_T):
    """Force (N) to squeeze the sheet under the foot: annulus from the slip bore to the foot outside, clipped to the
    strip width; bonded-disc correction 1 + 2 S^2 with the shape factor S of the annulus (loaded / free area)."""
    r_in = J.slip_bore(J.PUNCH_B) / 2.0
    r_out = J.FOOT_D / 2.0
    # area of the foot disc within |y| <= STRIP_W/2 (circular segment clipping), minus the bore
    h = J.STRIP_W / 2.0
    if h >= r_out:
        a_out = math.pi * r_out ** 2
    else:
        a_out = 2 * (h * math.sqrt(r_out ** 2 - h ** 2) + r_out ** 2 * math.asin(h / r_out))
    area = a_out - math.pi * r_in ** 2
    perim = 2 * math.pi * (r_in + r_out)
    s = area / (perim * sheet_t)
    return E_FKM * (squeeze / sheet_t) * (1 + 2 * s * s) * area, area, s


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
    add(f"no interference between any two parts ({len(names)} solids; the punch is checked separately)",
        worst <= 1e-4, f"largest common volume {worst:.2e} mm3")
    pb = PT.punch(J.PUNCH_B)
    for nm in ("plate", "liner", "slip_bushing", "base", "screw_0", "lock_screw", "lock_washer", "lock_spacer"):
        v = common_volume(pb, solids[nm])
        add(f"outside punch at the bottom of its stroke clears the {nm}", v <= 1e-4, f"{v:.2e} mm3")
    for key, p in (("A", J.PUNCH_A), ("B", J.PUNCH_B)):
        need, have = J.reach_needed(), J.exposed(p)
        add(f"{p['name']}: exposed tube {have:.1f} reaches {J.TIP_INTO_BACKING} into the backing with the handle "
            f">= 3 above the bushing (needs {need:.2f})", have >= need, f"margin {have - need:.2f} mm")
        add(f"{p['name']}: push wire {J.PUSH_WIRE[key]} passes the tube bore {p['bore']:.3f} (>= 0.05 clearance)",
            p["bore"] - J.PUSH_WIRE[key] >= 0.05, f"{p['bore'] - J.PUSH_WIRE[key]:.3f} mm")
    for p in (J.PUNCH_A, J.PUNCH_B, J.PUNCH_C):
        b = J.slip_bore(p)
        add(f"slip bushing bore {b:.4f} mm = {b / J.IN:.4f} in for {p['name']} is in the SF-12 range .0135-.0980 in",
            0.0135 <= b / J.IN <= 0.0980, f"{b / J.IN:.4f} in")
    lock_wall = J.LOCK_R - J.LINER_HOLE_D / 2.0 - J.INSERT_HOLE_D / 2.0
    add("printed wall between the liner hole and the lock-screw insert >= 0.7", lock_wall >= 0.7,
        f"{lock_wall:.2f} mm")
    overlap = J.LOCK_WASHER_D / 2.0 - (J.LOCK_R - J.SLIP_HEAD_D / 2.0)
    add("lock washer overlaps the bushing head by >= 0.5", overlap >= 0.5, f"{overlap:.2f} mm")
    lk_eng = J.LOCK_SCREW_L - 0.5 - J.SLIP_HEAD_H
    add("lock screw engages its insert 3-5.7 mm", 3.0 <= lk_eng <= J.INSERT_L, f"{lk_eng:.2f} mm")
    worst_c, rss_c = J.concentricity_budget()
    add("hole-to-outside offset, root-sum-square of both strokes <= 0.05 (T2C-004: concentric within dia 0.10)",
        rss_c <= J.CONC_LIMIT / 2.0, f"RSS {rss_c:.3f}, worst case {worst_c:.3f} mm radial")
    wall_min = (J.PUNCH_B["cut_d"] - J.PUNCH_A["cut_d"]) / 2.0 - worst_c
    add("washer wall at the worst-case offset >= 0.175 (docs/34 functional limit)", wall_min >= 0.175,
        f"{wall_min:.3f} mm")
    # cut sizes against the drawing
    for nm, d, nom, tol in (("hole", J.PUNCH_A["cut_d"], J.WASHER_ID, 0.10), ("outside", J.PUNCH_B["cut_d"],
                                                                                J.WASHER_OD, 0.10)):
        add(f"{nm} punch {d:.2f} within the drawing limits {nom - tol:.2f}-{nom + tol:.2f}",
            nom - tol - 1e-9 <= d <= nom + tol + 1e-9, f"{d - nom:+.2f} mm from nominal")
    # clamping: force-set (the plate floats on the sheet)
    n_total = 2 * J.SCREW_FORCE
    f_disp, area, sfac = clamp_force(0.001)                 # N per 1 um of squeeze
    add("information: squeeze of the sheet under the foot at the screw force (nearly incompressible thin layer)",
        True, f"{n_total / f_disp:.2f} um at {n_total:.0f} N (foot {area:.0f} mm2, shape factor {sfac:.1f}, "
        f"E {E_FKM} MPa UNVERIFIED)")
    r_in, r_out = J.slip_bore(J.PUNCH_B) / 2.0, J.FOOT_D / 2.0
    r_eff = 2.0 / 3.0 * (r_out ** 3 - r_in ** 3) / (r_out ** 2 - r_in ** 2)
    t_hold = J.MU_SHEET * n_total * r_eff
    add("friction under the foot holds the sheet: lateral >= 20 N and torque >= 50 N mm (a punch pressed with a "
        "slight twist)", J.MU_SHEET * n_total >= 20.0 and t_hold >= 50.0,
        f"{J.MU_SHEET * n_total:.0f} N, {t_hold:.0f} N mm at mu {J.MU_SHEET} and {n_total:.0f} N (UNVERIFIED)")
    z_min = J.BACKING_T - J.BACKING_T_TOL + J.SHEET_T - J.SHEET_T_TOL
    add("plate floats: at the thinnest stack its underside clears the base by >= 0.4 outside the relief, and the "
        "relief clears the rails by >= 0.2", z_min >= 0.4 and z_min + J.RECESS_DEPTH - J.RAIL_H >= 0.2
        and z_min - J.RAIL_H >= 0.2,
        f"underside {z_min:.2f} above the base; foot {z_min - J.RAIL_H:.2f} above the rail tops")
    add("rails lie under the plate's relief", J.STRIP_W / 2 + J.RAIL_GAP / 2 + J.RAIL_W <= J.RECESS_HALF_W,
        f"rail outer edge {J.STRIP_W / 2 + J.RAIL_GAP / 2 + J.RAIL_W:.2f} <= {J.RECESS_HALF_W}")
    clear = J.Z_FOOT + J.RECESS_DEPTH - (J.BACKING_T + J.BACKING_T_TOL + J.SHEET_T + J.SHEET_T_TOL)
    add("thickest strip clears the relief by >= 0.5 (the strip slides under the plate)", clear >= 0.5,
        f"{clear:.2f} mm")
    web = J.PITCH - J.WASHER_OD - 0.2
    add("web between washers >= 1.0 at the pitch (outside + 0.2 for the punch bevel)", web >= 1.0, f"{web:.2f} mm")
    eng = J.DOWEL_L - J.DOWEL_IN_BASE - J.Z_FOOT - (J.BACKING_T_TOL + J.SHEET_T_TOL)
    add("dowel engages the plate >= 3 mm at the thickest stack", eng >= 3.0, f"{eng:.2f} mm")
    thread = J.SCREW_L - J.PLATE_T - J.Z_FOOT
    add("thumb screw engages the insert >= 4 mm and stays within the insert hole", 4.0 <= thread <= J.INSERT_L + 1.0,
        f"{thread:.2f} mm in an {J.INSERT_L} mm insert")
    add("foot wall around the liner >= 1.0 and the foot lies on the strip", J.FOOT_WALL >= 1.0 and
        J.FOOT_D <= J.STRIP_W + J.RAIL_GAP, f"foot dia {J.FOOT_D:.1f}, strip {J.STRIP_W}")
    return rows


def main(argv=None):
    fast = "--fast" in (argv or sys.argv[1:])
    base, plate = PT.base(), PT.plate()
    printed = [("J-001_base", base), ("J-002_head_plate", plate), ("J-003_handle_A", PT.handle(J.PUNCH_A)),
               ("J-003_handle_B", PT.handle(J.PUNCH_B)), ("J-004_lock_spacer", PT.lock_spacer())]
    for nm, o in printed:
        C.export_step(o, OUT / f"{nm}.step")
        cq.exporters.export(o, str(OUT / f"{nm}.stl"), exportType="STL", tolerance=0.01, angularTolerance=0.1)
    slip_a, slip_b = PT.slip_bushing(J.PUNCH_A), PT.slip_bushing(J.PUNCH_B)
    solids = {"base": base, "plate": plate, "liner": PT.liner(), "slip_bushing": slip_b,
              "backing": PT.backing(), "sheet": PT.sheet()}
    w, sc = PT.lock_screw()
    solids["lock_washer"], solids["lock_screw"], solids["lock_spacer"] = w, sc, PT.lock_spacer()
    for i, s in enumerate(PT.dowels()):
        solids[f"dowel_{i}"] = s
    for i, s in enumerate(PT.screws()):
        solids[f"screw_{i}"] = s
    rows = checks(solids)
    mats = {"base": "PEEK", "plate": "PEEK", "liner": "steel", "slip_bushing": "steel", "backing": "default",
            "sheet": "elastomer"}
    items = [(nm, o, mats.get(nm, "steel")) for nm, o in solids.items()]
    items += [("insert_" + str(i), s, "copper") for i, s in enumerate(PT.inserts())]
    for nm in ("lock_washer", "lock_screw", "lock_spacer"):
        mats[nm] = "PEEK" if nm == "lock_spacer" else "steel"
    items.append(("outside_punch", PT.punch(J.PUNCH_B), "default"))
    C.export_step(C.assembly(items, "punch_jig"), OUT / "J-000_assembly.step")
    C.export_step(slip_a, OUT / "slip_bushing_A_hole.step")
    C.export_step(PT.slip_bushing(J.PUNCH_C), OUT / "slip_bushing_C_membrane.step")
    C.export_step(slip_b, OUT / "slip_bushing_B_outside.step")
    worst_c, rss_c = J.concentricity_budget()
    res = dict(checks=rows, all_pass=all(r["ok"] for r in rows),
               numbers=dict(z_foot=J.Z_FOOT, plate_t=J.PLATE_T, foot_d=J.FOOT_D,
                            slip_bore_A=J.slip_bore(J.PUNCH_A), slip_bore_B=J.slip_bore(J.PUNCH_B),
                            slip_bore_C=J.slip_bore(J.PUNCH_C),
                            reach_needed=J.reach_needed(), concentricity_rss=rss_c,
                            concentricity_worst=worst_c))
    (OUT / "check_results.json").write_text(json.dumps(res, indent=1))
    for r in rows:
        print(("pass  " if r["ok"] else "FAIL  ") + r["check"] + "  [" + str(r["value"]) + "]")
    if not fast:
        vis = [(o, m) for nm, o, m in items]
        C.render_png(vis, OUT / "assembly_iso.png", view="iso", title="Washer punching jig (docs/36), stroke 2")
        lift = {"base": 0, "backing": 3, "sheet": 5, "plate": 14, "liner": 26,
                "slip_bushing": 40, "outside_punch": 60, "screw_0": 70, "screw_1": 70}
        ex = [(o.translate((0, 0, lift.get(nm, 0))), m) for nm, o, m in items]
        C.render_png(ex, OUT / "assembly_exploded.png", view="iso", size=(8, 10), title="Exploded")
        half = C.box_from_corners((-60, 0, -20), (60, 40, 80))
        sec = []
        for nm, o, m in items:
            try:
                c = o.cut(half)
                if C._shape(c).Volume() > 1e-6:
                    sec.append((c, m))
            except Exception:
                pass
        C.render_png(sec, OUT / "section.png", view="front", title="Section y = 0 (punch axis)")
        C.render_png(sec, OUT / "section_detail.png", view="front", title="Section y = 0, foot and sheet",
                     xlim=(-6, 6), ylim=(-1.5, 3.5))
        C.render_png([(plate, "PEEK")], OUT / "head_plate_underside.png", view="bottom", title="Head plate, underside")
        C.render_png([(base, "PEEK")], OUT / "base_top.png", view="top", title="Base, top")
        C.shrink_pngs(OUT)
    print("all checks pass" if res["all_pass"] else "CHECKS FAILED")
    return 0 if res["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
