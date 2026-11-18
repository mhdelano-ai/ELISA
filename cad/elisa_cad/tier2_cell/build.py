"""Build the tier-2 flow cell (docs/34): STEP files of the three custom parts and of the assembly, renders,
the labelled section, the notes for the machining drawing and the check results -> cad/out/tier2_cell/.

Run from cad/:   python -m elisa_cad.tier2_cell.build   [--fast: no renders]     (about 1 min)
"""
from __future__ import annotations

import json
import math
import sys

import cadquery as cq

from .. import common as C
from . import params as P
from . import parts as PT
from . import section as S

OUT = C.out_dir("tier2_cell")


def vol(o):
    return C._shape(o).Volume()


def common_volume(a, b):
    try:
        return C._shape(a.intersect(b)).Volume()
    except Exception:                                   # no common solid
        return 0.0


def n_solids(o):
    return len(C._shape(o).Solids())


def checks(parts, liquid):
    rows = []

    def add(name, ok, value):
        rows.append(dict(check=name, ok=bool(ok), value=value))

    names = list(parts)
    worst = 0.0
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            v = common_volume(parts[a], parts[b])
            worst = max(worst, v)
            if v > 1e-4:
                add(f"no interference {a} / {b}", False, f"{v:.4f} mm3")
    add("no interference between any two solid parts (11 parts; O-rings and washer drawn at their compressed height)", worst <= 1e-4,
        f"largest common volume {worst:.2e} mm3")
    add("the liquid is one connected solid from the inlet port floor to the outlet port floor",
        n_solids(liquid) == 1, f"{n_solids(liquid)} solid(s), {vol(liquid):.2f} mm3")
    for nm in ("base", "plate", "body", "strip"):
        v = common_volume(liquid, parts[nm])
        add(f"the liquid does not cut into the {nm}", v <= 1e-4, f"{v:.2e} mm3")
    # the liquid reaches both port floors
    bb = C._shape(liquid).BoundingBox()
    add("liquid reaches the floor of the inlet port", abs(bb.zmax - (PT.Z_TOP - P.PORT_DEPTH)) < 1e-6 or
        bb.zmax >= PT.Z_TOP - P.PORT_DEPTH - 1e-6, f"z max {bb.zmax:.3f}")
    add("liquid reaches the floor of the outlet port", abs(bb.xmin - (P.X0 + P.PORT_DEPTH)) < 1e-6,
        f"x min {bb.xmin:.3f}")
    # walls (mm), from the dimensions
    r_port = P.PORT_MAJOR_D / 2.0
    walls = {
        "inlet thread to body riser": abs(P.RISER_BODY_X) - P.RISER_BODY_D / 2.0 - r_port,
        "inlet thread to the end of the outlet through-hole": abs(P.RISER_BODY_X) - r_port,
        "outlet thread to the M2.5 threads": abs(P.M25_XY[0][1]) - 1.25 - r_port,
        "outlet thread to the body underside": P.OUTLET_Z - r_port,
        "outlet thread to the body top": P.BODY_T - P.OUTLET_Z - r_port,
        "collecting groove to the O-ring groove (plate underside)": P.GROOVE_STRIP_ID / 2.0 - P.RING_R1,
        "thin-layer land beyond the working electrode": P.RING_R0 - P.WE_D / 2.0,
        "plate under the cross channel, above the collecting groove": P.PLATE_T - P.CHANNEL_DEPTH - P.RING_DEPTH,
        "plate above the O-ring groove": P.PLATE_T - P.GROOVE_STRIP_DEPTH,
        "face seal between retainer pocket and cross channel": abs(P.RISER_PLATE_X) - P.CHANNEL_W / 2.0
        - P.RET_POCKET_D / 2.0,
        "membrane overlap beyond the bed bore (clamped band)": (P.MEMBRANE_DISC_D - P.BED_D) / 2.0,
        "plate under the retainer pocket": P.PLATE_T - P.RET_POCKET_DEPTH,
        "cross channel and riser to the body-plate O-ring groove": P.GROOVE_IFACE_ID / 2.0 - abs(P.CHANNEL_X_END)
        - max(P.CHANNEL_W, P.RISER_BODY_D) / 2.0,
        "strip beyond the O-ring groove, each side": (P.STRIP_W - P.GROOVE_STRIP_OD) / 2.0,
        "inner edge of the strip O-ring's contact band (ring I.D./2 + 0.15) beyond the printed electrodes":
        P.ORING_STRIP[0] / 2.0 + 0.15 - P.PRINT_R_MAX,
        "contact pads start beyond the stack (room for the connector)": P.PADS_FROM_FREE_END - P.WE_FROM_FREE_END
        - P.X1,
    }
    limits = {"membrane overlap beyond the bed bore (clamped band)": 0.4,
              "strip beyond the O-ring groove, each side": 0.3,
              "contact pads start beyond the stack (room for the connector)": 1.0,
              "inner edge of the strip O-ring's contact band (ring I.D./2 + 0.15) beyond the printed electrodes": 0.0,
              "collecting groove to the O-ring groove (plate underside)": 0.5}
    for k, v in walls.items():
        lim = limits.get(k, 0.8)
        add(f"wall or margin: {k} >= {lim} mm", v >= lim - 1e-9, f"{v:.2f} mm")
    stack = P.WASHER_T + P.SCREEN_T + P.MEMBRANE_T
    add("nothing stands proud: the retainer stack is compressed into its pocket (washer squeeze 15-35 %)",
        0.15 <= P.WASHER_SQUEEZE <= 0.35, f"stack {stack:.3f} free, pocket {P.RET_POCKET_DEPTH:.3f}, squeeze "
        f"{100 * P.WASHER_SQUEEZE:.0f} %")
    add("membrane top lies in the plane of the plate top face (meets the body face)",
        abs(P.RET_POCKET_DEPTH - P.WASHER_H - P.SCREEN_T - P.MEMBRANE_T) < 1e-9, "0")
    add("every drilled hole is at least 0.5 mm in diameter",
        min(P.EXIT_D, P.BED_D, P.RISER_PLATE_D, P.RISER_BODY_D, P.OUTLET_THROUGH_D) >= 0.5,
        f"smallest {min(P.EXIT_D, P.BED_D, P.RISER_PLATE_D, P.RISER_BODY_D, P.OUTLET_THROUGH_D)} mm")
    deepest = max(P.INLET_FLOOR / P.BED_D, P.PLATE_T / P.EXIT_D,
                  (P.OUTLET_Z + 0.4) / P.RISER_BODY_D, (P.PLATE_T) / P.RISER_PLATE_D)
    add("no hole deeper than 10 diameters", deepest <= 10.0, f"deepest {deepest:.1f} diameters")
    return rows


def drawing_notes(masses):
    """Index of the drawings; the call-outs themselves are on the drawings (drawings.py)."""
    L = ["# Tier-2 flow cell — machining drawings (index; generated)", "",
         f"The dimensioned drawings are `out/tier2_cell/drawings/T2C-00x_*_v{P.VERSION}.pdf`, made by "
         "`python -m elisa_cad.tier2_cell.drawings` from the same solids and parameters as the STEP files. "
         "Upload each STEP with its PDF. Ordering notes: `out/tier2_cell/drawings/ORDERING.md`; "
         "tolerance policy: docs/34 section 5.2.", "",
         "| Part | Drawing | STEP | Envelope (mm) | Mass (g) |", "|---|---|---|---|---|"]
    files = {"base": ("T2C-001_base.pdf", "base.step"), "nozzle_plate": ("T2C-002_nozzle_plate.pdf",
                                                                          "nozzle_plate.step"),
             "body": ("T2C-003_body.pdf", "body.step")}
    for nm, (env, m) in masses.items():
        L.append(f"| {nm} | `drawings/{P.vname(files[nm][0])}` | `{P.vname(files[nm][1])}` | {env} | {m:.0f} |")
    return "\n".join(L) + "\n"

def write_washer_dxf():
    """Cut files of the washer (T2C-004): one part, and a nested sheet of WASHER_ARRAY parts. Layer CUT holds the
    cut contours (circles, mm); layer SHEET the blank outline (not cut, reference)."""
    import ezdxf
    for name, (nx, ny) in (("washer.dxf", (1, 1)), ("washer_sheet.dxf", P.WASHER_ARRAY)):
        doc = ezdxf.new("R2010")
        doc.units = ezdxf.units.MM
        doc.layers.add("CUT", color=1)
        doc.layers.add("SHEET", color=8)
        msp = doc.modelspace()
        pitch = P.WASHER_PITCH
        for i in range(nx):
            for j in range(ny):
                c = ((i + 0.5) * pitch, (j + 0.5) * pitch)
                msp.add_circle(c, P.WASHER_ID / 2.0, dxfattribs={"layer": "CUT"})     # inner contour first
                msp.add_circle(c, P.WASHER_OD / 2.0, dxfattribs={"layer": "CUT"})
        if (nx, ny) != (1, 1):
            msp.add_lwpolyline([(0, 0), (nx * pitch, 0), (nx * pitch, ny * pitch), (0, ny * pitch)], close=True,
                               dxfattribs={"layer": "SHEET"})
        doc.saveas(OUT / P.vname(name))


def main(argv=None):
    fast = "--fast" in (argv or sys.argv[1:])
    custom = {"base": (PT.base(), "steel"), "nozzle_plate": (PT.plate(), "PEEK"), "body": (PT.body(), "PEEK")}
    bought = {"strip": (PT.strip(), "PTFE"), "shim": (PT.shim(), "steel"),
              "oring_strip": (PT.oring_strip(), "elastomer"), "oring_interface": (PT.oring_iface(), "elastomer"),
              "washer": (PT.washer(), "elastomer"), "screen": (PT.screen(), "steel"),
              "membrane": (PT.membrane(), "PTFE")}
    liquid = PT.liquid()
    for nm, (o, _m) in custom.items():
        C.export_step(o, OUT / P.vname(f"{nm}.step"))
    C.export_step(PT.washer_free(), OUT / P.vname("washer.step"))
    write_washer_dxf()
    everything = [(nm, o, m) for nm, (o, m) in {**custom, **bought}.items()]
    everything += [(f"screw_M4_{i}", s, "steel") for i, s in enumerate(PT.screws())]
    everything += [(f"dowel_{i}", s, "steel") for i, s in enumerate(PT.dowels())]
    everything += [("working_electrode", PT.working_electrode(), "default"), ("bed", PT.bed(), "copper"),
                   ("liquid", liquid, "liquid")]
    C.export_step(C.assembly(everything, "tier2_cell"), OUT / P.vname("assembly.step"))
    C.export_step(liquid, OUT / P.vname("liquid_path.step"))

    solid = {"base": custom["base"][0], "plate": custom["nozzle_plate"][0], "body": custom["body"][0],
             "strip": bought["strip"][0], "shim": bought["shim"][0], "screen": bought["screen"][0],
             "membrane": bought["membrane"][0], "washer": bought["washer"][0], "oring_strip": bought["oring_strip"][0],
             "oring_interface": bought["oring_interface"][0], "dowel_0": PT.dowels()[0]}
    rows = checks(solid, liquid)
    dens = {"base": 8.0e-3, "nozzle_plate": 1.31e-3, "body": 1.31e-3}                # g/mm3
    masses = {}
    for nm, (o, _m) in custom.items():
        bb = C._shape(o).BoundingBox()
        masses[nm] = (f"{bb.xlen:.0f} × {bb.ylen:.0f} × {bb.zlen:.1f}", vol(o) * dens[nm])
    (OUT / P.vname("drawing_notes.md")).write_text(drawing_notes(masses))
    res = dict(checks=rows, all_pass=all(r["ok"] for r in rows),
               liquid_volume_uL=vol(liquid),
               volumes_uL=dict(bed_bore=P.BORE_AREA * P.INLET_FLOOR, exit_bore=P.EXIT_VOLUME_UL,
                               thin_layer_over_electrode=math.pi * (P.WE_D / 2) ** 2 * P.GAP,
                               chamber_disc=math.pi * P.CHAMBER_R ** 2 * P.GAP,
                               collecting_groove=math.pi * (P.RING_R1 ** 2 - P.RING_R0 ** 2) * P.RING_DEPTH),
               masses_g={k: v[1] for k, v in masses.items()})
    (OUT / P.vname("check_results.json")).write_text(json.dumps(res, indent=1))
    for r in rows:
        print(("pass  " if r["ok"] else "FAIL  ") + r["check"] + "  [" + str(r["value"]) + "]")
    S.draw(OUT / P.vname("section.png"))
    if not fast:
        items = [(o, m) for _n, o, m in everything if _n != "liquid"]
        C.render_png(items, OUT / P.vname("assembly_iso.png"), view="iso", title="Tier-2 flow cell (docs/34)")
        # exploded
        lift = {"base": 0, "shim": 4, "strip": 8, "working_electrode": 8, "oring_strip": 14, "nozzle_plate": 18,
                "washer": 23, "screen": 25, "membrane": 27, "bed": 30, "oring_interface": 29, "body": 34}
        ex = []
        for nm, o, m in everything:
            if nm == "liquid":
                continue
            dz = lift.get(nm, 46 if nm.startswith("screw") else 0)
            ex.append((o.translate((0, 0, dz)), m))
        C.render_png(ex, OUT / P.vname("assembly_exploded.png"), view="iso", size=(8, 10), title="Exploded")
        C.render_png([(custom["nozzle_plate"][0], "PEEK")], OUT / P.vname("nozzle_plate_underside.png"), view="bottom",
                     title="Nozzle plate, underside (cell face)")
        C.render_png([(custom["nozzle_plate"][0], "PEEK")], OUT / P.vname("nozzle_plate_top.png"), view="top",
                     title="Nozzle plate, top face")
        C.render_png([(custom["body"][0], "PEEK")], OUT / P.vname("body_underside.png"), view="bottom",
                     title="Body, underside")
        C.render_png([(custom["base"][0], "steel")], OUT / P.vname("base_top.png"), view="top", title="Base, top face")
        C.shrink_pngs(OUT)
    print("all checks pass" if res["all_pass"] else "CHECKS FAILED")
    return 0 if res["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
