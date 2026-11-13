"""Integrated dock + card A assembly:  cd cad && python -m elisa_cad.assembly.build [--no-renders] [--no-step]
[--fast]

Places the REAL card, the lower bay, the lid (closed / head raised / open 85 deg) and the base in dock coordinates
(collect.py), runs the one-off cross-module checks (checks.py) and writes cad/out/assembly/:
  dock_closed.step, dock_open_loading.step (each < 10 MB: full-detail card and lower/upper/base parts, simplified
  where noted in docs/23 §3.2), checks.json + checks.txt, and the PNG renders (zrender.py, z-buffer).
--fast skips the M_c/M_d state checks and the lid sweep."""
from __future__ import annotations

import json
import sys
import time

import cadquery as cq

from .. import common as C
from .. import interface as I
from . import checks as CH
from . import collect as K

OUT = C.out_dir("assembly")
LOG = []


def log(msg):
    print(msg, flush=True)
    LOG.append(msg)


def _items_for_step(items, drop=()):
    return [it for it in items if not it["name"].startswith(drop)]


# parts dropped from the integrated STEP files (still in the module STEPs): small catalogue envelopes inside the lid
STEP_DROP = ("ENV_spring_", "ENV_hall_DRV", "ENV_gallery_barbs", "ENV_magnet_", "ENV_return_spring_", "button_",
             "ENV_gas_barb")


def _cyl_chain(pts, r):
    sol = []
    for p, q in zip(pts[:-1], pts[1:]):
        v = cq.Vector(q[0] - p[0], q[1] - p[1], q[2] - p[2])
        if v.Length > 1e-6:
            sol.append(cq.Solid.makeCylinder(r, v.Length, cq.Vector(*p), v.normalized()))
    return cq.Compound.makeCompound(sol)


def _bbox_solid(s):
    b = s.BoundingBox()
    return cq.Solid.makeBox(max(b.xlen, 1e-3), max(b.ylen, 1e-3), max(b.zlen, 1e-3), cq.Vector(b.xmin, b.ymin, b.zmin))


def simplified(items):
    """Envelope versions for the integrated STEP files (docs/23 §3.2): full detail stays in the module STEPs.
    CARD: L3 body, die glass and L4 discs real; L0-L2 + film + seam as one laminate slab. UPPER: head mechanism
    (pins, buttons, springs, yokes, rods, pistons, magnets, Hall ICs, barbs) omitted; cylinder-block layers and the
    pilot manifolds, guide plates and spring plate as boxes. LOWER: tubes as plain cylinder chains (bends
    coarsened), anvil with the openings simplified to 0.15 mm, heat sink and foil heaters as boxes. BASE: rear/left panels as boxes; only the 11 card lines and 2
    gas lines as plain cylinder chains (all other lines: base_tubing.step)."""
    from unittest import mock
    from ..dock_base import fluidics as F
    from ..dock_lower import geom as LG
    from ..dock_lower import parts as LP
    O = cq.Vector(*I.CARD_ORIGIN_IN_DOCK)
    out, lam_done = [], False
    l3 = next((it for it in items if it["module"] == "CARD" and it["name"].startswith("L3_body")), None)
    dz = 0.0 if l3 is None else l3["shape"].BoundingBox().zmin - (I.CARD_ORIGIN_IN_DOCK[2] + I.Z_L3[0])
    for it in items:
        m, n = it["module"], it["name"]
        if m == "CARD" and n.startswith(("L0_", "L1", "L2_", "seam", "die_metal", "die_passivation")):
            if not lam_done:
                slab = cq.Solid.makeBox(I.CARD_L - 2 * I.LAMINATE_INSET, I.CARD_W - 2 * I.LAMINATE_INSET, I.Z_L2[1],
                                        cq.Vector(I.LAMINATE_INSET, I.LAMINATE_INSET, 0)).translate(O) \
                    .translate(cq.Vector(0, 0, dz))
                out.append(dict(it, name="laminate_L0-L2_envelope", shape=slab, material="COC_foil"))
                lam_done = True
            continue
        if m == "UPPER" and n.startswith(("pin_", "button_", "ENV_spring_", "yoke_", "rod_", "piston_", "ENV_magnet",
                                          "ENV_return", "ENV_hall", "ENV_gallery", "ENV_gas_barb", "ENV_limit",
                                          "standoff_", "guide_post_", "thrust_", "ENV_clamp")):
            continue
        if (m == "UPPER" and n.startswith(("cyl_block_", "ENV_SMC", "gallery_header", "guide_plate_", "spring_plate"))) \
                or (m == "BASE" and n in ("panel_rear", "panel_left")) or (m == "LOWER" and (n == "heatsink_env" or n.startswith("heater_"))):
            out.append(dict(it, shape=_bbox_solid(it["shape"]), name=n + "_envelope"))
            continue
        if m == "LOWER" and n.startswith("tube_"):
            full = LG.tube_route(n[5:])
            pts = [p for i, p in enumerate(full) if i % 4 == 0 or i == len(full) - 1 or i < 2]   # coarser bends
            pts = [tuple(a + b for a, b in zip(p, I.CARD_ORIGIN_IN_DOCK)) for p in pts]
            out.append(dict(it, shape=_cyl_chain(pts, LG.TUBE_OD / 2)))
            continue
        if m == "LOWER" and n == "anvil":
            simp = LG.through_openings().simplify(0.15)
            with mock.patch.object(LG, "through_openings", lambda: simp):
                a = LP.anvil()
            out.append(dict(it, shape=C._shape(a).translate(O), name="anvil_slot_simplified"))
            continue
        if m == "BASE" and n.startswith("tube:"):
            r = next(r for r in F.ROUTES if "tube:" + r.name == n)
            if not r.port and not r.name.startswith(("P_c gas", "P_mv gas")):
                continue          # pump-side, supply, waste and air lines: in base_tubing.step only
            od = F.TUBES[r.tube][2] if F.TUBES[r.tube][2] else 3.0
            out.append(dict(it, shape=_cyl_chain(r.pts, od / 2)))
            continue
        out.append(it)
    # generic envelope rule: compact, many-faced bodies (fins, holes, pockets) -> their bounding box; thin shells and
    # the parts named in KEEP stay as they are
    keep = ("anvil", "nest_frame", "heater_block", "peek_plate", "cover", "guide_bush", "datum_pin", "pogo_")
    res = []
    for it in out:
        s = it["shape"]
        if it["module"] != "CARD" and not it["name"].startswith(keep) and len(s.Faces()) > 40:
            b = s.BoundingBox()
            if s.Volume() > 0.45 * b.xlen * b.ylen * b.zlen:
                it = dict(it, shape=_bbox_solid(s), name=it["name"] + "_bbox")
        res.append(it)
    return res


def export_step(items, path, name):
    a = cq.Assembly(name=name)
    for it in items:
        m = it["material"]
        rgba = C.color(m) if isinstance(m, str) else m
        nm = f"{it['module']}__{it['name']}".replace(" ", "_").replace(">", "").replace("/", "_").replace(":", "_") \
            .replace("(", "").replace(")", "").replace(",", "")
        a.add(it["shape"], name=nm, color=cq.Color(*rgba))
    a.export(str(path), exportType="STEP")
    return path.stat().st_size / 1e6


def run_checks(fast=False):
    res = {}
    t0 = time.time()
    closed = K.scene("closed", "hold_RC")
    log(f"closed scene: {len(closed)} solids ({time.time() - t0:.0f} s)")
    bad, good, n = CH.cross_interference(closed)
    res["closed_read_hold_RC"] = {"pairs_tested": n, "unintended": bad, "intended": good}
    log(f"[closed/read] {n} cross-module bbox pairs; unintended {len(bad)}: {bad}")
    log(f"[closed/read] intended {len(good)} (by class): " +
        str(sorted({(g[0].split(':')[0] + ':' + g[0].split(':')[1].split('_')[0], g[1].split(':')[0] + ':' +
                     g[1].split(':')[1].split('_')[0]) for g in good})))
    res["pins_in_bores"] = CH.pins_in_bores(closed)
    log(f"pins in bores ok={res['pins_in_bores']['ok']}")
    res["ports"] = CH.ports(closed)
    log(f"ports ok={res['ports']['ok']}")
    res["pogo"] = CH.pogo(closed)
    log(f"pogo ok={res['pogo']['ok']} on_pad={res['pogo']['on_pad']}")
    res["datums"] = CH.datums(closed)
    log(f"datums ok={res['datums']['ok']} {res['datums']}")
    res["pad_gas_vents"] = CH.press_pad_gas_vents(closed)
    log(f"pad/gas/vents ok={res['pad_gas_vents']['ok']} {res['pad_gas_vents']}")
    res["contact_areas"] = CH.contact_areas(closed)
    log(f"contact areas {res['contact_areas']}")
    res["guide_pins"] = CH.guide_pins(closed)
    log(f"guide pins {res['guide_pins']}")
    res["tube_handover"] = CH.tube_handover()
    log(f"tube hand-over ok={res['tube_handover']['ok']}")
    # open / loading: lid open 85, lower 'load', card above the nest at 3 heights and seated
    lo = list(K.lower("load")) + list(K.upper("open")) + list(K.base(True))
    bad, good, n = CH.cross_interference(lo)
    res["open_load_no_card"] = {"pairs_tested": n, "unintended": bad, "intended": good}
    log(f"[open/load] {n} pairs; unintended {len(bad)}: {bad}")
    load_hits = {}
    for dz in (120.0, 60.0, 20.0, 5.0):
        cardz = [dict(it, shape=it["shape"].translate(cq.Vector(0, 0, dz))) for it in K.card()]
        b2, g2, n2 = CH.cross_interference(cardz + lo, modules_pairs=[{"CARD", "UPPER"}, {"CARD", "LOWER"},
                                                                        {"CARD", "BASE"}])
        load_hits[f"card_dz_{dz:g}"] = b2
    res["loading_path_card"] = load_hits
    log(f"[loading] card above the nest: {load_hits}")
    if not fast:
        mstates = {}
        for st in ("collect_IC1", "collect_IC2", "gather_IC1", "gather_IC1_low", "drag_mid_IC1", "beadout_end"):
            sc = list(K.card()) + list(K.lower(st)) + list(K.upper("closed"))
            b3, g3, n3 = CH.cross_interference(sc, modules_pairs=[{"CARD", "LOWER"}, {"UPPER", "LOWER"}])
            mstates[st] = {"pairs": n3, "unintended": b3, "intended_n": len(g3)}
            log(f"[state {st}] {n3} pairs; unintended {b3}")
        res["magnet_states"] = mstates
        others = list(K.lower("load")) + list(K.base(True)) + list(K.card())
        res["lid_sweep"] = CH.lid_sweep(list(K.upper("raised")), others)
        log(f"[lid sweep] {res['lid_sweep']['pairs_tested']} pairs; hits {res['lid_sweep']['hits']}; "
            f"moving x {res['lid_sweep']['moving_lid_x_range']}; partitions {res['lid_sweep']['clearance_to_partitions_mm']}")
    res["run_time_s"] = round(time.time() - t0, 1)
    return res


def exports():
    sizes = {}
    closed = simplified(K.scene("closed", "hold_RC"))
    sizes["dock_closed.step"] = round(export_step(closed, OUT / "dock_closed.step", "dock_closed_read_state"), 2)
    lo = list(K.lower("load")) + list(K.upper("open")) + list(K.base(True))
    lo += [dict(it, shape=it["shape"].translate(cq.Vector(0, 0, 60.0)), name=it["name"] + "_loading")
           for it in K.card()]
    lo = simplified(lo)
    sizes["dock_open_loading.step"] = round(export_step(lo, OUT / "dock_open_loading.step", "dock_open_loading"), 2)
    log(f"STEP sizes MB: {sizes}")
    return sizes


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    t0 = time.time()
    res = run_checks(fast="--fast" in argv)
    (OUT / "checks.json").write_text(json.dumps(res, indent=1, default=str))
    (OUT / "checks.txt").write_text("\n".join(LOG) + "\n")
    if "--no-step" not in argv:
        res["step_sizes_MB"] = exports()
    if "--no-renders" not in argv:
        from . import render
        render.render_all(OUT, log)
    (OUT / "checks.txt").write_text("\n".join(LOG) + f"\ntotal {time.time() - t0:.0f} s\n")
    (OUT / "checks.json").write_text(json.dumps(res, indent=1, default=str))
    C.shrink_pngs(OUT)   # palette PNGs (docs/23 §3.4)
    log(f"done in {time.time() - t0:.0f} s -> {OUT}")


if __name__ == "__main__":
    main()
