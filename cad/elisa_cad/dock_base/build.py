"""Build the DOCK BASE: STEP files, PNG/SVG views, tubing schedule and check results -> cad/out/dock_base/.
Run from cad/:  python -m elisa_cad.dock_base.build   [--fast: skip renders]"""
from __future__ import annotations

import csv
import json
import sys
import time

import cadquery as cq

from .. import common as C
from .. import interface as I
from . import calcs as K
from . import fluidics as F
from . import layout as L
from . import params as P
from . import parts as PT
from . import render as RD

OUT = C.out_dir("dock_base")
STEP_GROUPS = {
    "frame": ["frame"], "enclosure_panels": ["enclosure"], "drip_tray": ["tray"], "brackets": ["bracket"],
    "cold_compartment": ["cold"], "pumps": ["pumps"], "bottles_pneumatics": ["bottles", "pneumatics"],
    "electronics": ["electronics"], "sensors": ["sensors"], "gamry_route_bench": ["gamry", "bench"],
}
MAT_RGBA = lambda m: C.color(m)  # noqa: E731


def build_solids():
    sol = {}
    for it in L.ITEMS:
        sol[it.name] = PT.solid(it)
    return sol


def build_tubes(scale=1.0):
    return {r.name: PT.tube_solid(r, scale) for r in F.ROUTES}


def vol_common(a, b):
    try:
        sa = a.val() if isinstance(a, cq.Workplane) else a
        sb = b.val() if isinstance(b, cq.Workplane) else b
        if isinstance(sa, cq.Workplane):
            sa = sa.val()
        bba, bbb = sa.BoundingBox(), sb.BoundingBox()
        if (bba.xmax <= bbb.xmin or bbb.xmax <= bba.xmin or bba.ymax <= bbb.ymin or bbb.ymax <= bba.ymin
                or bba.zmax <= bbb.zmin or bbb.zmax <= bba.zmin):
            return 0.0
        return sa.intersect(sb).Volume()
    except Exception as e:  # pragma: no cover
        return float("nan")


def _val(w):
    v = w.vals()
    return cq.Compound.makeCompound(v) if len(v) > 1 else v[0]


def intrusion_checks(sol, tubes):
    sweep, _reg = PT.lid_sweep_solid()
    targets = {"UPPER_lid_closed": PT.claim_box("UPPER_lid_closed"), "LOWER_nest_anvil": PT.claim_box("LOWER_nest_anvil"),
               "LOWER_bay": PT.claim_box("LOWER_bay"), "lid_sweep_0-85": sweep,
               "loading_path": C.box_from_corners(*P.LOAD_BOX)}
    res = []
    for tname, tw in targets.items():
        tv = _val(tw)
        worst = []
        for n, w in list(sol.items()) + [("tube:" + k, v) for k, v in tubes.items()]:
            if n in ("Gamry_Ref600plus",):
                continue
            vv = vol_common(_val(w), tv)
            if vv != vv or vv > 0.5:
                worst.append((n, round(vv, 1)))
        res.append((tname, worst))
    return res, sweep


def sweep_clearance(sweep):
    """Minimum distance between the lid sweep and the nearest DOCK BASE bodies around the well (Derived)."""
    out = {}
    sv = _val(sweep)
    for n in ("rear_low_cover", "well_rear_wall", "partition_left", "partition_right", "panel_top_left",
              "panel_top_right", "panel_top_rear", "rail_well_rear"):
        it = L.get(n)
        out[n] = round(sv.distance(_val(PT.solid(it))), 2)
    return out


def export_steps(sol, tubes):
    sizes = {}
    for fname, groups in STEP_GROUPS.items():
        parts = [(it.name, sol[it.name], it.material) for it in L.ITEMS if it.group in groups]
        a = C.assembly(parts, name="grp_" + fname)
        p = OUT / f"base_{fname}.step"
        C.export_step(a, p)
        sizes[p.name] = p.stat().st_size
    a = cq.Assembly(name="tubing")
    for r in F.ROUTES:
        rgba = PT.tube_color(r)
        if tubes[r.name] is not None:
            a.add(tubes[r.name], name=r.name.split(" (")[0].replace(" ", "_").replace(">", "").replace("/", "_"),
                  color=cq.Color(*rgba))
    p = OUT / "base_tubing.step"
    C.export_step(a, p)
    sizes[p.name] = p.stat().st_size
    # full base assembly with translucent claim placeholders
    A = cq.Assembly(name="dock_base_assembly")
    for it in L.ITEMS:
        r, g, b, al = C.color(it.material)
        A.add(sol[it.name], name=it.name, color=cq.Color(r, g, b, al))
    for r in F.ROUTES:
        if tubes[r.name] is not None:
            A.add(tubes[r.name], name="tube_" + str(F.ROUTES.index(r)), color=cq.Color(*PT.tube_color(r)))
    for k in ("UPPER_lid_closed", "LOWER_nest_anvil", "LOWER_bay"):
        col = C.color("claim_upper" if k.startswith("UPPER") else "claim_lower")
        A.add(PT.claim_box(k), name="CLAIM_" + k, color=cq.Color(*col))
    sweep, _ = PT.lid_sweep_solid()
    A.add(sweep, name="ENVELOPE_lid_sweep_0_85deg", color=cq.Color(0.95, 0.55, 0.25, 0.12))
    p = OUT / "base_assembly_with_claims.step"
    C.export_step(A, p)
    sizes[p.name] = p.stat().st_size
    return sizes


def write_tables(chk):
    rows = F.schedule_rows()
    with open(OUT / "tubing_schedule.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(OUT / "check_results.json", "w") as f:
        json.dump(chk, f, indent=1, default=str)


def renders(sol, tubes_vis, sweep):
    E = {it.name: it for it in L.ITEMS}

    def items(groups=None, exclude=(), include_tubes=True, alpha_override=None, extra=()):
        out = []
        for it in L.ITEMS:
            if groups and it.group not in groups:
                continue
            if it.name in exclude or it.group == "bench" and "bench" not in (groups or ()):
                continue
            rgba = C.color(it.material)
            if alpha_override and it.name in alpha_override:
                rgba = rgba[:3] + (alpha_override[it.name],)
            out.append((it.name, sol[it.name], rgba))
        if include_tubes:
            for r in F.ROUTES:
                out.append(("tv:" + r.name, tubes_vis[r.name], PT.tube_color(r)))
        out.extend(extra)
        return out

    claims = [("cl_up", PT.claim_box("UPPER_lid_closed"), (0.95, 0.55, 0.25, 0.30)),
              ("cl_nest", PT.claim_box("LOWER_nest_anvil"), (0.30, 0.65, 0.35, 0.35)),
              ("cl_bay", PT.claim_box("LOWER_bay"), (0.30, 0.65, 0.35, 0.25))]
    sweep_it = [("sweep", sweep, (0.95, 0.55, 0.25, 0.10))]
    panels = [it.name for it in L.ITEMS if it.group == "enclosure" and it.name.startswith("panel")]
    lab_main = [((235, 110, 300), "lid (UPPER claim)", (0, 0)), ((70, 2, 90), "cold-box door", None),
                ((395, 2, 140), "bottle door", None), ((75, -10, 285), "E-stop", None),
                ((75, 0, 318), "status light", None)]
    note = "Claims: orange = DOCK UPPER, green = DOCK LOWER (translucent placeholders). Dock coords, mm."
    gamry = [("gamry", sol["Gamry_Ref600plus"], C.color("anodised"))]
    RD.render(items(extra=claims + gamry, include_tubes=False), OUT / "view_iso_front_left.png", "iso_fl",
              title="DOCK BASE - iso front-left (enclosure on, claims translucent, Gamry on the right)",
              labels=lab_main, note=note)
    RD.render(items(extra=claims + gamry, include_tubes=False), OUT / "view_iso_front_right.png", "iso_fr",
              title="DOCK BASE - iso front-right", labels=lab_main, note=note)
    RD.render(items(extra=claims + gamry, include_tubes=False), OUT / "view_rear.png", "rear",
              title="DOCK BASE - rear (pump service door; connector panel and exhaust on the electronics side, viewer right; lab-air inlet on the right panel)",
              labels=[((80, 420, 70), "connector panel", (-60, 40)), ((300, 420, 160), "pump service door", None),
                      ((60, 420, 180), "exhaust louvre", (-60, 60)), ((470, 380, 45), "lab-air inlet", (60, -30))],
              note=note)
    RD.top_plan(OUT / "plan_top_labelled.png")
    RD.render(items(extra=claims + gamry, include_tubes=False), OUT / "view_front_elevation.png", "front",
              title="DOCK BASE - front elevation (card plane Z 170; lid closed)",
              labels=[((235, 0, 240), "card bay / lid (open top)", None), ((73, 0, 80), "cold-box door", None),
                      ((395, 0, 140), "bottle door", None)], note=note)
    nopanel = set(panels) | {"electronics_box", "rail_front_left", "rail_front_right", "rail_left", "rail_right",
                              "rail_rear", "rail_well_rear", "partition_left", "partition_right", "well_rear_wall",
                              "rear_low_cover", "Gamry_Ref600plus", "cold_box", "estop", "status_light"}
    cb_cut = sol["cold_box"].cut(C.box_from_corners((0, 0, 0), (130, 60, 200)))
    RD.render(items(exclude=nopanel, extra=claims[2:] + [("cb_cut", cb_cut, (0.97, 0.97, 0.97, 1.0))]),
              OUT / "view_fluidics_no_enclosure.png", "iso_fl",
              title="DOCK BASE - enclosure removed: fluidics (tubes drawn 2x OD), pumps, bottles, pneumatics",
              labels=[((172, 400, 240), "pumps S_b S_IC1 S_IC2 S_A S_RC", (0, 60)),
                      ((385, 258, 265), "waste air-gap head", (60, 40)), ((235, 110, 160), "LOWER bay (claim)", None),
                      ((120, 77, 190), "SV_b", (-40, 30)), ((20, 110, 160), "P_in sensor / PEEK from SM-FL", (-40, -40)),
                      ((232, 260, 150), "Flow EZ x2", (0, -50))],
              note="Lines inside the LOWER claim (gland -> port) are owned by DOCK LOWER and not drawn.")
    RD.render(items(exclude=nopanel - {"cold_box"} | {"cold_box"}, extra=claims[2:] + [("cb_cut", cb_cut, (0.97, 0.97, 0.97, 1.0))]),
              OUT / "view_fluidics_rear_left.png", "iso_rl",
              title="DOCK BASE - enclosure removed, from rear-left (pump valves face the rear service door)")
    # cold compartment detail
    cold_names = [it.name for it in L.ITEMS if it.group == "cold"] + ["P_in_pressure_sensor"]
    cold_items = [(n, sol[n], C.color(E[n].material)) for n in cold_names if n != "cold_box"]
    cb2 = sol["cold_box"].cut(C.box_from_corners((0, -5, 0), (130, 75, 300)))
    clip = C.box_from_corners((0, 0, 0), (149, 212, 230))
    cold_tubes = [("tvc:" + r.name, tubes_vis[r.name].intersect(clip), PT.tube_color(r)) for r in F.ROUTES
                  if any(p[0] < 150 and p[1] < 210 for p in r.pts)]
    RD.render(cold_items + [("cb2", cb2, (0.9, 0.9, 0.95, 1.0))] + cold_tubes, OUT / "view_cold_compartment.png",
              (0.55, -1.3, 0.75), title="Cold compartment detail (front half of the insulated box cut away at Y 75)",
              xlim=None, labels=[((70, 47, 105), "bead vial on rocker", (-60, 30)), ((65, 100, 82), "conjugate tube", (-70, -10)),
                                ((73, 123, 80), "DA-024 cold plate", (-60, 40)),
                                ((134, 47, 72), "rocker motor", (60, -20)), ((120, 75, 197), "SV_b", (40, 30)),
                                ((19, 110, 170), "P_in sensor", (-40, 30)), ((40, 20, 40), "door (Y 2-20)", (-40, -20))])
    # electronics detail (2D elevations) and right elevation with the lid sweep (2D)
    RD.electronics_layout(OUT / "view_electronics_bay.png", K.power_budget())
    _, reg = PT.lid_sweep_solid()
    RD.side_elevation(OUT / "view_right_elevation_lid_sweep.png", reg)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    t0 = time.time()
    sol = build_solids()
    tubes = build_tubes(1.0)
    print(f"[dock_base] {len(sol)} bodies, {len(tubes)} tube routes built in {time.time() - t0:.1f} s")
    chk = {}
    chk["route_item_collisions"] = F.route_collisions()
    chk["route_pair_clashes"] = F.route_pair_clashes()
    chk["item_overlaps"] = K.item_overlaps()
    chk["containment_failures"] = [x for x in K.cold_and_elec_containment() if not x[2]
                                   and x[0] not in ("intake_filter_grille", "fan_exhaust_80")]
    chk["outside_footprint"] = K.footprint_ok()
    intr, sweep = intrusion_checks(sol, tubes)
    chk["intrusions"] = intr
    chk["sweep_clearance_mm"] = sweep_clearance(sweep)
    _, reg = PT.lid_sweep_solid()
    chk["sweep_region_bounds_YZ"] = [round(v, 1) for v in reg.bounds]
    chk["liquid_budget"], chk["prime"] = K.liquid_budget()
    chk["cold_box_heat"] = K.cold_box_heat()
    chk["power"] = K.power_budget()
    chk["air"] = K.air_supply()
    chk["mass_cog_full"] = K.mass_cog(True, True)
    chk["mass_cog_empty_waste"] = K.mass_cog(True, False)
    chk["mass_cog_base_only"] = K.mass_cog(False, True)
    chk["bench"] = K.bench_layout()
    chk["gamry_cable_mm"] = F.gamry_cable_length()
    chk["dp_kPa"] = {r.name: {q: round(F.dp_kPa(r, q), 2) for q in (10, 100, 500, 1500)} for r in F.ROUTES
                     if r.port in ("P_in", "P_b", "P_d1", "P_d2", "P_s", "P_cf", "P_rf")}
    for k in ("route_item_collisions", "route_pair_clashes", "item_overlaps", "containment_failures",
              "outside_footprint", "intrusions", "sweep_clearance_mm"):
        print(f"  {k}: {chk[k]}")
    print(f"[dock_base] checks done {time.time() - t0:.1f} s")
    sizes = export_steps(sol, tubes)
    chk["step_sizes_bytes"] = sizes
    write_tables(chk)
    print(f"[dock_base] STEP written {time.time() - t0:.1f} s: {sizes}")
    if "--fast" not in argv:
        tubes_vis = build_tubes(2.0)
        renders(sol, tubes_vis, sweep)
        RD.bench_plan(OUT / "plan_bench_layout.png", K.bench_layout())
        RD.schematic(OUT / "fluidic_schematic.png")
        print(f"[dock_base] renders written {time.time() - t0:.1f} s")
    print(f"[dock_base] done in {time.time() - t0:.1f} s -> {OUT}")


if __name__ == "__main__":
    main()
