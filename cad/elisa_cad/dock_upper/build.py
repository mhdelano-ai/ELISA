"""Regenerate every DOCK UPPER output:  cd cad && python -m elisa_cad.dock_upper.build  [--fast]
Writes cad/out/dock_upper/: STEP (custom parts, families, sub-assemblies, three lid configurations), PNG views,
calcs.txt and checks.txt (the numbers quoted in docs/20)."""
from __future__ import annotations

import math
import sys
import time

import cadquery as cq

from elisa_cad import interface as IF
from elisa_cad.common import assembly, export_step, out_dir, render_png, color
from elisa_cad.dock_upper import assy, calcs, checks
from elisa_cad.dock_upper import params as P
from elisa_cad.dock_upper import parts as Pt

OUT = out_dir("dock_upper")
FAMILIES = ("pin_", "button_", "yoke_", "rod_", "piston_", "standoff_", "guide_post_", "thrust_", "lid_post_block_",
            "guide_ear_", "guide_pin_", "lid_side_plate_", "hinge_block_", "cyl_block_")
COVER_RGBA = (0.72, 0.74, 0.78, 0.15)


def log(msg, fh):
    print(msg)
    fh.write(msg + "\n")


def _mat(n, m, see_through=False):
    if n == "cover":
        return COVER_RGBA
    if see_through and n.startswith(("lid_side_plate", "ENV_latch", "lid_front_beam")):
        return (0.72, 0.74, 0.78, 0.18)
    return m


def export_all(cfgs, fh):
    closed = cfgs["closed"]
    custom = [(n, s, m) for (n, s, m, k) in closed["rotating"] + closed["fixed"] if k == "custom"]
    fam = {}
    singles = []
    for n, s, m in custom:
        f = next((p for p in FAMILIES if n.startswith(p)), None)
        (fam.setdefault(f, []).append((n, s, m)) if f else singles.append((n, s, m)))
    pd = OUT / "parts"
    pd.mkdir(exist_ok=True)
    for n, s, m in singles:
        export_step(s, pd / f"{n}.step")
    for f, lst in fam.items():
        export_step(assembly(lst, name=f.rstrip("_")), pd / f"{f.rstrip('_')}_family.step")
    head = [(n, s, m) for (n, s, m, k) in closed["rotating"] if not n.startswith(("lid_", "cover", "cam_", "ENV_latch",
                                                                                   "lid_handle", "umbilical",
                                                                                   "ENV_umbilical", "ENV_lid_switch"))]
    export_step(assembly(head, "head_closed"), OUT / "subassy_head_closed.step")
    lid = [(n, s, m) for (n, s, m, k) in assy.lid_parts(True) + assy.fixed_parts()]
    export_step(assembly(lid, "lid_frame_closed"), OUT / "subassy_lid_frame_closed.step")
    for name, c in cfgs.items():
        a = assembly([(n, s, _mat(n, m) if isinstance(_mat(n, m), str) else "aluminium")
                      for (n, s, m, k) in c["rotating"] + c["fixed"]], f"lid_{name}")
        export_step(a, OUT / f"lid_assembly_{name}.step")
    export_step(assembly([(n, s, m) for (n, s, m, k) in closed["card"]], "card_envelope_ref"),
                OUT / "card_envelope_ref.step")
    sizes = sorted(((p.stat().st_size / 1e6, p.name) for p in OUT.rglob("*.step")), reverse=True)
    log(f"STEP files: {len(sizes)}; largest {sizes[0][1]} {sizes[0][0]:.2f} MB", fh)


# ------------------------------------------------------------------------------------------------ renders
def items(lst, see_through=False):
    return [(s, _mat(n, m, see_through)) for (n, s, m, *_r) in lst]


def render_views(cfgs, fh):
    c = cfgs["closed"]
    render_png(items(c["rotating"] + c["fixed"] + c["card"], True), OUT / "iso_closed.png", "iso", size=(10, 7.5),
               dpi=170, title="Lid closed + latched, head down (cover, side plates, latches transparent); card envelope")
    head = [p for p in c["rotating"] if not p[0].startswith(("lid_", "cover", "cam_lever", "ENV_latch", "lid_handle",
                                                             "umbilical", "ENV_umb", "ENV_lid"))]
    render_png(items(head + c["card"]), OUT / "iso_head_closed.png", "iso", size=(10, 8), dpi=170,
               title="Head alone, down on the card envelope (closed state), with cam shaft and eccentrics")
    o = cfgs["open"]
    claim = IF.OPERATOR_LOADING_PATH["clear_box"]
    lb = Pt.box(claim[0][0], claim[1][0], claim[0][1], claim[1][1], claim[0][2], claim[1][2])
    render_png(items(o["rotating"] + o["fixed"] + o["card"]) + [(lb, (0.2, 0.8, 0.3, 0.12))], OUT / "iso_open.png",
               "iso", size=(10, 8), dpi=170,
               title="Lid open 85 deg (head raised), card envelope in the nest; green = operator loading-path box")
    kin_side(cfgs)
    underside()
    section_pin()
    section_pair()
    plan_grid()
    plan_galleries()
    exploded()
    log("PNG renders written", fh)


def kin_side(cfgs):
    """Side view (looking -X) of the three configurations + claims and sweep box."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    from elisa_cad.common import tessellate
    fig, axs = plt.subplots(1, 3, figsize=(15, 6), dpi=150)
    for ax, name in zip(axs, ("closed", "raised", "open")):
        cf = cfgs[name]
        for (n, s, m, *_r) in cf["rotating"] + cf["fixed"] + cf["card"]:
            if n == "cover" or n.startswith(("lid_side_plate", "ENV_latch")):
                continue
            v, t = tessellate(s, 0.2)
            if len(t) == 0:
                continue
            col = color(m) if isinstance(m, str) else m
            ax.add_collection(__import__("matplotlib.collections", fromlist=["PolyCollection"]).PolyCollection(
                [v[tr][:, [1, 2]] for tr in t], facecolors=[col], edgecolors="none", alpha=min(1, col[3] + 0.2)))
        for k, cl in IF.SPACE_CLAIMS.items():
            (x0, y0, z0), (x1, y1, z1) = cl["box"]
            if z0 > 400 or y0 > 330:
                continue
            ax.add_patch(Rectangle((y0, z0), y1 - y0, z1 - z0, fill=False, lw=0.6,
                                   ec="tab:orange" if k.startswith("UPPER") else "tab:green" if "LOWER" in k else
                                   "tab:blue", ls="--"))
        (x0, y0, z0), (x1, y1, z1) = IF.lid_sweep_bbox()
        ax.add_patch(Rectangle((y0, z0), y1 - y0, z1 - z0, fill=False, lw=0.8, ec="red", ls=":"))
        (lx0, ly0, lz0), (lx1, ly1, lz1) = IF.OPERATOR_LOADING_PATH["clear_box"]
        ax.add_patch(Rectangle((ly0, lz0), ly1 - ly0, lz1 - lz0, fill=False, lw=0.8, ec="green"))
        hy, hz = IF.LID_HINGE_AXIS["point"][1:]
        ax.plot([hy], [hz], "k+", ms=8)
        ax.set_xlim(0, 330)
        ax.set_ylim(140, 400)
        ax.set_aspect("equal")
        ax.set_title({"closed": "closed + latched (head down)", "raised": "closed, head raised 8 mm",
                      "open": "open 85 deg"}[name], fontsize=9)
        ax.set_xlabel("dock Y (mm, operator at left)")
        ax.set_ylabel("dock Z (mm)")
        ax.tick_params(labelsize=7)
    fig.suptitle("Kinematics, side view looking -X. Orange dashed = UPPER claim, green = LOWER claims, "
                 "blue = BASE claims, red dotted = interface lid_sweep_bbox, green solid = loading-path box", fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "kinematics_side.png")
    plt.close(fig)


def head_closed_card():
    return assy.head_parts("closed")


def underside():
    """Head face (z = card top) as a 2D drawing, seen from BELOW (x mirrored so it matches the real part)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, Polygon, Rectangle
    from shapely.geometry import LineString, Point

    def draw(path, xl, yl, title, fs=7):
        fig, ax = plt.subplots(figsize=(13, 9), dpi=170)
        ax.add_patch(Rectangle((P.HB_X[0], 0), P.HB_X[1] - P.HB_X[0], 50, fc="0.75", ec="k", lw=0.6))
        ax.add_patch(Rectangle((P.PEEK_X[0], 0), P.PEEK_X[1] - P.PEEK_X[0], 50, fc="tan", ec="k", lw=0.6))
        gp = Pt.guide_plate_outline()
        ax.add_patch(Polygon(list(gp.exterior.coords), fc="#c87533", ec="k", lw=0.5, alpha=0.9))
        for name, (x, y) in IF.VENTS.items():
            dx, dy = P.VENT_EXITS[name]
            g = LineString([(x, y), (x + dx * 60, y + dy * 60)]).buffer(P.VENT_GROOVE_W / 2, cap_style=2)
            g = g.union(Point(x, y).buffer(P.VENT_POCKET_D / 2)).intersection(
                Point(37.75, 25).buffer(200).envelope.intersection(
                    LineString([(0, 0), (75.5, 50)]).envelope))
            ax.add_patch(Polygon(list(g.exterior.coords), fc="white", ec="0.3", lw=0.5, ls="--"))
            ax.text(x, y - 4.0 if dy >= 0 else y + 4.0, name.replace("vent_", "vent "), ha="center", fontsize=fs)
        fx, fy = P.PAD["footprint_x"], P.PAD["footprint_y"]
        ax.add_patch(Rectangle((fx[0], fy[0]), fx[1] - fx[0], fy[1] - fy[0], fc="0.15", ec="k"))
        ax.text((fx[0] + fx[1]) / 2, fy[1] + 0.8, "press pad 12 N", ha="center", fontsize=fs)
        for pid, p in P.GAS_PORTS.items():
            ax.add_patch(Circle(p.xy, P.GAS["od"] / 2, fc="0.1", ec="none"))
            ax.add_patch(Circle(p.xy, P.GAS["id"] / 2, fc="tan", ec="none"))
            ax.add_patch(Circle(p.xy, 0.5, fc="white", ec="none"))
            ax.text(p.xy[0], p.xy[1] + 4.3, f"{pid} gas ring", ha="center", fontsize=fs)
        cols = {"slot": "tab:red", "anvil": "tab:blue", "cold": "tab:cyan"}
        for vid, v in IF.VALVES.items():
            ax.add_patch(Circle(v.xy, v.tip_d / 2, fc=cols[v.klass], ec="k", lw=0.3))
            ax.text(v.xy[0] + 0.45, v.xy[1] + 0.45, vid + (" (fail-open)" if vid == "V3" else ""), fontsize=fs)
        for n, (x, y) in P.GUIDE_PINS.items():
            ax.add_patch(Circle((x, y), P.GUIDE_PIN_D / 2, fc="0.5", ec="k"))
            ax.text(x, y - 4.5, n + " Ø6", ha="center", fontsize=fs)
        ax.add_patch(Rectangle((0, 0), IF.CARD_L, IF.CARD_W, fill=False, ec="k", lw=1.0, ls=":"))
        ax.set_xlim(*xl)
        ax.set_ylim(*yl)
        ax.invert_xaxis()
        ax.set_aspect("equal")
        ax.grid(True, lw=0.2)
        ax.set_xlabel("card x (mm) - axis reversed: view from below")
        ax.set_ylabel("card y (mm)")
        ax.set_title(title, fontsize=9)
        fig.tight_layout()
        fig.savefig(path)
        plt.close(fig)

    draw(OUT / "head_underside.png", (-11, 86), (-3, 53),
         "Head face seen from below: 21 pin tips (red slot class 1.2 N, blue 2.5 N, cyan cold), CuSn8 guide plate "
         "(copper), Al heater block (grey), PEEK plate (tan), gas rings, vent pockets + grooves, press pad, guide pins")
    draw(OUT / "head_underside_zoom_J_cell.png", (47, 63.5), (16, 34),
         "Head face from below, zoom on J and the cell: Ø0.8 tips, 1.60 mm minimum pitch (V11-V12)", fs=9)


def _section(parts, p0, ang_deg, keep_depth, path, xlim, ylim, title, ann=None):
    """Rotate about z through p0 by -ang (so the section line becomes +x), keep y' in [p0y, p0y+keep_depth],
    view from the front (-y)."""
    px, py = p0
    slab = Pt.box(-200, 300, py, py + keep_depth, -50, 200).val()
    its = []
    for (n, s, m, *_r) in parts:
        sh = (s.val() if isinstance(s, cq.Workplane) else s).rotate(cq.Vector(px, py, 0), cq.Vector(px, py, 1),
                                                                      -ang_deg)
        bb = sh.BoundingBox()
        if bb.ymax < py or bb.ymin > py + keep_depth:
            continue
        cut = sh.intersect(slab)
        if cut.Volume() > 1e-6:
            its.append((cut, _mat(n, m)))
    w = xlim[1] - xlim[0]
    h = ylim[1] - ylim[0]
    render_png(its, path, "front", size=(max(5.0, 10.0 * w / h) + 1.0, 10.5), dpi=190, xlim=xlim, ylim=ylim,
               title=title, annotate=ann)


def section_pin():
    hp = head_closed_card() + [(n, s, m, "card") for (n, s, m) in assy.card_envelope()]
    v = IF.VALVES["G4"]
    c = IF.CYLINDERS["G4"]
    ang = math.degrees(math.atan2(c["xy"][1] - v.xy[1], c["xy"][0] - v.xy[0]))
    L = math.dist(v.xy, c["xy"])
    x0 = v.xy[0]
    ann = [((x0 - 3.5, v.xy[1], 3.0), "card (L3)"), ((x0 - 3, v.xy[1], 11), "heater block"),
           ((x0 + 1.2, v.xy[1], 20), "pin spring"), ((x0 - 2.5, v.xy[1], 25.3), "spring plate"),
           ((x0 + 4, v.xy[1], 29.5), "yoke tier 0"), ((x0 + L, v.xy[1], 52), "Ø6 cylinder"),
           ((x0 + L, v.xy[1], 41), "air plate + gallery"), ((x0 + L + 5, v.xy[1], 65), "cap"),
           ((x0 + L, v.xy[1], 72.5), "Hall PCB"), ((x0, v.xy[1], 0.2), "tip on foil")]
    _section(hp, v.xy, ang, 1.5, OUT / "section_pin_G4.png", (x0 - 12, x0 + L + 12), (-1, 82),
             "Section through G4 (closed, de-energised): pin Ø0.8 - CuSn8 guide plates -\nspring - spring plate - "
             "yoke tier 0 - rod - Ø6 cylinder - Hall PCB", ann)


def section_pair():
    hp = head_closed_card() + [(n, s, m, "card") for (n, s, m) in assy.card_envelope()]
    y = IF.VALVES["V11"].xy[1]
    ann = [((51.3, y, 35.6), "V11 t1"), ((53.6, y, 30.6), "V12 t0"), ((49.0, y, 30.9), "G1 t0"),
           ((47.6, y, 20.5), "springs"), ((47.6, y, 25.3), "spring plate"), ((47.6, y, 11.2), "heater blk"),
           ((47.6, y, 3.5), "card L3")]
    _section(hp, (0.0, y - 0.02), 0.0, 1.2, OUT / "section_tightest_pair_V11_V12.png", (46.5, 55.0), (-0.5, 39.5),
             "Section y = 25.93: G1, V11, V12 (Ø0.8 pins,\nV11-V12 pitch 1.60): collars Ø1.4, springs OD 1.3,\n"
             "buttons Ø1.3 on two tiers", ann)


def plan_grid():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, Polygon, Rectangle
    from shapely.geometry import LineString
    fig, ax = plt.subplots(figsize=(13, 9), dpi=160)
    ax.add_patch(Rectangle((0, 0), IF.CARD_L, IF.CARD_W, fill=False, ec="k", lw=0.8))
    ax.add_patch(Rectangle((P.CYL_BLOCK_X[0], 0), P.CYL_BLOCK_X[1] - P.CYL_BLOCK_X[0], 50, fill=False, ec="0.5",
                           lw=0.6, ls="--"))
    tier_col = {0: "tab:blue", 1: "tab:red"}
    for vid, c in IF.CYLINDERS.items():
        v = IF.VALVES[vid]
        ax.add_patch(Circle(c["xy"], P.BORE_D / 2, fill=False, ec="0.4", lw=0.8))
        ax.add_patch(Circle(c["xy"], P.BOSS_D / 2, fc=tier_col[c["tier"]], ec="none", alpha=0.6))
        poly = LineString([v.xy, c["xy"]]).buffer(P.BLADE_W / 2, cap_style=2)
        ax.add_patch(Polygon(list(poly.exterior.coords), fc=tier_col[c["tier"]], alpha=0.45, ec="none"))
        k = P.pkey(v)
        ax.add_patch(Circle(v.xy, P.HEAD_BTN_D[k] / 2, fc="k", ec="none"))
        ax.text(c["xy"][0], c["xy"][1] + 3.4, f"{vid} t{c['tier']}", ha="center", fontsize=7)
        ax.text(v.xy[0] + 0.5, v.xy[1] - 1.0, vid, fontsize=5.5, color="0.2")
    for (x, y) in P.STANDOFFS_HB + P.STANDOFFS_PEEK:
        ax.add_patch(Circle((x, y), P.STANDOFF_D / 2, fc="tan", ec="k", lw=0.4, alpha=0.6))
    for n, (x, y) in P.GUIDE_PINS.items():
        ax.add_patch(Circle((x, y), P.GUIDE_PIN_D / 2, fc="0.6", ec="k", lw=0.4))
        ax.text(x, y - 5, n, ha="center", fontsize=7)
    ax.set_xlim(-14, 90)
    ax.set_ylim(-4, 54)
    ax.set_aspect("equal")
    ax.grid(True, lw=0.2)
    ax.set_xlabel("card x (mm)")
    ax.set_ylabel("card y (mm)")
    ax.set_title("Plan: 21 Ø6 cylinders on the 9 mm grid (interface.CYLINDERS), yoke blades (blue tier 0 z 27-31, "
                 "red tier 1 z 32-36), pin buttons (black), PEEK standoffs (tan), guide pins", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "plan_cylinders_yokes.png")
    plt.close(fig)


def plan_galleries():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, Polygon, Rectangle
    from shapely.geometry import LineString
    routes = Pt.route_galleries()
    fig, ax = plt.subplots(figsize=(13, 8), dpi=160)
    ax.add_patch(Rectangle((P.CYL_BLOCK_X[0], 0), P.CYL_BLOCK_X[1] - P.CYL_BLOCK_X[0], 50, fill=False, ec="k",
                           lw=0.8))
    for vid, c in IF.CYLINDERS.items():
        ax.add_patch(Circle(c["xy"], P.BORE_D / 2, fill=False, ec="0.6", lw=0.6, ls=":"))
        ax.add_patch(Circle(c["xy"], (P.ROD_D + 0.3) / 2, fc="0.3", ec="none"))
        r = routes[vid]
        poly = LineString(r["path"]).buffer(P.GALLERY_W / 2, cap_style=2)
        ax.add_patch(Polygon(list(poly.exterior.coords), fc="tab:cyan", ec="tab:blue", lw=0.3))
        ax.add_patch(Circle(r["via"], 0.4, fc="tab:red", ec="none"))
        ex, ey = r["path"][-1]
        ax.text(ex, ey + 1.0 if r["exit"] == "+y" else ey, vid, fontsize=6, rotation=90 if r["exit"] == "+y" else 0,
                ha="center" if r["exit"] == "+y" else "left", va="bottom" if r["exit"] == "+y" else "center")
    for (x, y) in P.STANDOFFS_HB + P.STANDOFFS_PEEK:
        ax.add_patch(Circle((x, y), 1.6, fc="tan", ec="k", lw=0.3))
    ax.set_xlim(-12, 92)
    ax.set_ylim(-2, 56)
    ax.set_aspect("equal")
    ax.grid(True, lw=0.2)
    ax.set_title("Air plate underside: 21 galleries 0.6 x 0.6 (cyan), vias into the annulus (red; V3 via feeds its "
                 "cap), rod holes (grey), screw holes (tan); exits rear (+y) and right (+x) headers", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "plan_air_galleries.png")
    plt.close(fig)


def exploded():
    hp = head_closed_card()
    off = {"heater_block": 0, "guide_plate_lower": -14, "guide_plate_upper": 8, "peek_plate": 0, "V8_bush": 0,
           "ENV_gas": -10, "ENV_heater": 0, "ENV_Pt100": 0, "press_pad": -18, "pin_": 20, "button_": 20,
           "ENV_spring_": 20, "standoff_": 30, "spring_plate": 45, "yoke_": 60, "rod_": 60, "ENV_limit": 60,
           "cyl_block_cover": 80, "guide_ear": 80, "guide_pin": 80, "cyl_block_air_plate": 92, "gallery_": 92,
           "ENV_gallery": 92, "cyl_block_bore_block": 110, "piston_": 140, "ENV_magnet": 140, "ENV_return": 140,
           "cyl_block_cap": 150, "ENV_hall": 165, "bridge": 185, "guide_post": 185, "thrust_": 185, "ENV_clamp": 185,
           "ENV_SMC": 185}
    its = []
    for (n, s, m, k) in hp:
        dz = next((v for p, v in off.items() if n.startswith(p)), 0)
        if "spacer" in n:
            dz = 178
        its.append((s.translate((0, 0, dz)), m))
    render_png(its, OUT / "exploded_head.png", "iso", size=(10, 13), dpi=170,
               title="Head exploded along z: plates + guides, pins + springs, spring plate, yokes,\n"
                     "cylinder-block layers, pistons, Hall PCB, bridge + thrust units + S070 manifolds")


# ------------------------------------------------------------------------------------------------ main
def main(fast=False):
    t0 = time.time()
    fh = open(OUT / "checks.txt", "w")
    rep, text = calcs.report()
    (OUT / "calcs.txt").write_text(text + "\n")
    log("calcs written (calcs.txt)", fh)
    routes = Pt.route_galleries()
    mins, length = Pt.gallery_check(routes)
    log(f"gallery routing: min webs {mins}; length max {max(length.values()):.1f} mm", fh)
    cfgs = {n: assy.configuration(n, routes) for n in ("closed", "raised", "open")}
    log(f"configurations built ({time.time() - t0:.0f} s)", fh)
    for name in ("closed", "raised"):
        c = cfgs[name]
        hits, npairs, n = checks.interference(c["rotating"] + c["fixed"], extra=c["card"])
        bad = [h for h in hits if not h[3]]
        log(f"interference [{name}]: {n} solids, {npairs} bbox-overlapping pairs tested, "
            f"{len(hits) - len(bad)} intended overlaps, {len(bad)} unintended: {bad}", fh)
        cc = checks.claim_check(c["rotating"] + c["fixed"])
        log(f"outside UPPER claim [{name}] (name, mm3, zmin, ymin, ymax, allowed): {cc}", fh)
    sw = checks.sweep_check(cfgs["raised"]["rotating"])
    log(f"sweep 0-85 deg: overlaps with other claims {sw['overlaps']}; min z of lid over nest "
        f"{sw['min_z_over_nest']:.2f}; loading-path overlap {sw['loading_path_overlap_mm3']:.3f} mm3; "
        f"sweep bbox {tuple(round(v, 1) for v in sw['sweep_bbox'])}; interface bbox {sw['interface_sweep_bbox']}", fh)
    log(f"closing arc: {checks.closing_arc()}", fh)
    log(f"descent: {checks.descent_sequence()}", fh)
    log(f"plan clearances: {checks.plan_clearances()}; min pin pitch {checks.pin_pitch_min()}", fh)
    mc = checks.mass_and_com(cfgs["closed"]["rotating"])
    log(f"lid mass {mc['mass_g']:.0f} g, CoM dock {tuple(round(v, 1) for v in mc['com'])}", fh)
    log(f"lid torques: {checks.lid_torques(mc['com'], mc['mass_g'])}", fh)
    head_only = [p for p in cfgs["closed"]["rotating"] if not p[0].startswith(("lid_", "cover", "cam_", "ENV_latch",
                                                                                 "lid_handle", "umbilical", "ENV_umb",
                                                                                 "ENV_lid"))]
    mh = checks.mass_and_com(head_only)
    log(f"head (moving 8 mm) mass {mh['mass_g']:.0f} g", fh)
    if not fast:
        export_all(cfgs, fh)
        render_views(cfgs, fh)
    log(f"done in {time.time() - t0:.0f} s", fh)
    fh.close()


if __name__ == "__main__":
    main(fast="--fast" in sys.argv)
