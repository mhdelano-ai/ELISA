"""Build every output of card A into cad/out/card/:  python -m elisa_cad.card.build  (run from cad/)

STEP (one per part + assembly), DXF + SVG cut profiles of the laser-cut layers (L0, L1, L1s shim, L1b, L2), die
mask layers (metal, passivation openings) as DXF + SVG, PNG views, checks.json."""
from __future__ import annotations

import json
import time

import ezdxf
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import unary_union

from .. import common as C
from .. import interface as I
from . import checks, parts as Q, profiles as P, render

OUT = C.out_dir("card")


# ------------------------------------------------------------------------------------------------ 2D export
def _polys(g):
    return list(g.geoms) if isinstance(g, MultiPolygon) else [g]


def write_dxf(path, layers, note):
    """layers: {layer_name: shapely geometry}. Every ring becomes a closed LWPOLYLINE (laser cut path), mm."""
    doc = ezdxf.new("R2010")
    doc.units = ezdxf.units.MM
    msp = doc.modelspace()
    for i, (lname, g) in enumerate(layers.items()):
        doc.layers.add(lname, color=(i % 6) + 1)
        for p in Q.clean(g, e=1e-5):
            msp.add_lwpolyline([(round(x, 5), round(y, 5)) for x, y in list(p.exterior.coords)[:-1]], close=True,
                               dxfattribs={"layer": lname})
            for r in p.interiors:
                msp.add_lwpolyline([(round(x, 5), round(y, 5)) for x, y in list(r.coords)[:-1]], close=True,
                                   dxfattribs={"layer": lname})
    doc.layers.add("NOTE", color=7)
    msp.add_mtext(note, dxfattribs={"layer": "NOTE", "char_height": 0.8}).set_location((0, -3))
    doc.saveas(str(path))


def write_svg(path, layers, note, flip=True):
    allg = unary_union([g for g in layers.values()])
    x0, y0, x1, y1 = allg.bounds
    pad = 2.0
    W, H = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad + 4
    cols = ["#000000", "#c00000", "#0050c0", "#008000", "#a06000", "#600080"]

    def tr(x, y):
        return (x - x0 + pad, (y1 - y + pad) if flip else (y - y0 + pad))

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.2f}mm" height="{H:.2f}mm" '
           f'viewBox="0 0 {W:.3f} {H:.3f}">']
    for i, (lname, g) in enumerate(layers.items()):
        out.append(f'<g id="{lname}" fill="none" stroke="{cols[i % 6]}" stroke-width="0.02">')
        for p in Q.clean(g, e=1e-5):
            for ring in [p.exterior] + list(p.interiors):
                pts = " ".join("%.4f,%.4f" % tr(x, y) for x, y in list(ring.coords)[:-1])
                out.append(f'<polygon points="{pts}"/>')
        out.append("</g>")
    out.append(f'<text x="{pad}" y="{H - 1:.2f}" font-size="1.2" font-family="sans-serif">{note}</text>')
    out.append("</svg>")
    path.write_text("\n".join(out))


def export_2d():
    hdr = "Card A C2 (docs/19), card coords mm seen from the TOP of the card, origin lower-left; "
    sets = {
        "L0_foil": ({"CUT": P.L0()}, "L0 COC foil 0.140: outline + 11 port holes D1.0 + contact window + 2 pin holes"),
        "L1_channel_sheet": ({"CUT": P.L1()}, "L1 COC sheet 0.175: all channels through-cut; cut on a transfer "
                                              "liner (5 islands); pin holes D2.0 / slot 2x3"),
        "L1s_WE2_shim": ({"CUT": P.L1s_shim()}, "L1s COC shim 0.150 (WE2 channel floor), 0.98 x 2.88"),
        "L1b_die_film": ({"CUT": P.L1b()}, "L1b 25 um adhesive film = die + 0.15, cut with the L1 pattern under the "
                                           "die; place with liner jig on the pins"),
        "L2_TPE": ({"CUT": P.L2()}, "L2 TPE 0.40: cut-outs chambers, tanks, MC, BW, die + 0.10, pin holes"),
    }
    for name, (layers, note) in sets.items():
        write_dxf(OUT / f"cut_{name}.dxf", layers, hdr + note)
        write_svg(OUT / f"cut_{name}.svg", layers, hdr + note)
    # die masks: die-local coords looking AT the electrode face (mirror of the card top view)
    m = unary_union(list(P.metal().values()))
    o = unary_union(list(P.passivation_openings().values()))
    die = P.to_die_local(P.DIE)
    masks = {"DIE_OUTLINE": die, "METAL": P.to_die_local(m), "PASSIVATION_OPEN": P.to_die_local(o)}
    note = ("Die A 6.0 x 10.0 mask, die-local mm, viewed LOOKING AT THE ELECTRODE FACE; origin = die corner at card "
            "(61.0, 23.35); u = 61.0 - x_card, v = y_card - 23.35. METAL = Au 150 nm / Ti 50 nm (positive), "
            "PASSIVATION_OPEN = openings in SU-8/polyimide")
    write_dxf(OUT / "die_mask_layers.dxf", masks, note)
    write_svg(OUT / "die_mask_metal.svg", {"DIE_OUTLINE": die, "METAL": masks["METAL"]}, note)
    write_svg(OUT / "die_mask_passivation.svg", {"DIE_OUTLINE": die, "PASSIVATION_OPEN": masks["PASSIVATION_OPEN"]},
              note)


# ------------------------------------------------------------------------------------------------ STEP
def export_step():
    parts = Q.all_parts()
    files = {}
    groups = {
        "L0_foil": ["L0_foil"], "L1_channel_sheet": ["L1_channel_sheet"], "L1s_WE2_shim": ["L1s_WE2_shim"],
        "L1b_die_film": ["L1b_die_film"], "L2_TPE": ["L2_TPE"], "seam_adhesive": ["seam_adhesive"],
        "L3_body": ["L3_body"], "die": ["die_glass", "die_metal", "die_passivation"],
        "L4_discs": [n for n, _, _ in parts if n.startswith("L4_")],
    }
    by = {n: (w, m) for n, w, m in parts}
    for g, names in groups.items():
        p = OUT / f"card_{g}.step"
        if len(names) > 1:
            C.export_step(C.assembly([(n, by[n][0], by[n][1]) for n in names], name="grp_" + g), p)
        else:
            C.export_step(by[names[0]][0], p)
        files[g] = p
    a = C.assembly(parts, name="card_A_C2")
    C.export_step(a, OUT / "card_A_assembly.step")
    return files


def main():
    t0 = time.time()
    export_2d()
    print("2D done", round(time.time() - t0, 1))
    export_step()
    print("STEP done", round(time.time() - t0, 1))
    res = checks.run_all()
    (OUT / "checks.json").write_text(json.dumps(res, indent=1, default=str))
    print("checks done", round(time.time() - t0, 1))
    render.plan_L1(OUT)
    render.zooms(OUT)
    render.sections(OUT)
    render.iso_views(OUT)
    print("renders done", round(time.time() - t0, 1))
    sizes = {p.name: round(p.stat().st_size / 1e6, 2) for p in OUT.iterdir()}
    big = {k: v for k, v in sizes.items() if v > 5.0}
    print("files", len(sizes), "largest MB", max(sizes.values()), "over 5 MB:", big)
    print("total", round(time.time() - t0, 1), "s")


if __name__ == "__main__":
    main()
