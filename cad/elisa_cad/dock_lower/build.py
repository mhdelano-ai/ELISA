"""Regenerate every DOCK LOWER output:  cd cad && python -m elisa_cad.dock_lower.build [--fast]
STEP files are written in DOCK coordinates (card coords + interface.CARD_ORIGIN_IN_DOCK) so they overlay the other
agents' models; PNGs are in card coordinates. --fast skips the M_d sweep check (~2 min)."""
from __future__ import annotations

import json
import sys
import time

from .. import common as C
from .. import interface as I
from . import assy, calcs, checks, render
from . import geom as G
from . import parts as P

OUT = C.out_dir("dock_lower")


def _dock(s):
    return s.translate(I.CARD_ORIGIN_IN_DOCK)


def export_parts():
    """One STEP per custom part type (dock coords)."""
    one = {
        "anvil": P.anvil(), "nest_frame": P.nest_frame(), "cold_block": P.cold_block(),
        "peek_break_frame": P.peek_break_frame(), "port_insert_P_in": P.port_insert("P_in"),
        "port_insert_P_cf": P.port_insert("P_cf"), "face_gasket": P.gasket("P_in"),
        "retainer_island": P.retainer("ret_island"), "retainer_Ps": P.retainer("ret_Ps"),
        "guide_bush": P.guide_bushes()[0][1], "exhaust_duct": P.duct(), "foam_insulation": P.foam_shell(),
        "bay_frame": P.bay_frame(), "ebay_enclosure": P.ebay_enclosure(), "pogo_block": P.pogo_block(True),
    }
    for n, s, m, k in P.mc_unit(1, 0.0):
        if k == "custom":
            one[n] = s
    for n, s, m, k in P.md_moving(I.M_D_HOLD_POS, True) + P.md_carriage(I.M_D_HOLD_POS) + \
            P.md_stages(I.M_D_HOLD_POS) + P.pogo_guide_and_wedge(True) + P.ebay_internals():
        if k == "custom":
            one[n] = s
    files = []
    for n, s in one.items():
        f = OUT / f"part_{n}.step"
        C.export_step(_dock(s), f)
        files.append(f)
    return files


def export_assemblies():
    files = []
    for st in G.RENDER_STATES:
        items = assy.state_items(st)
        a = C.assembly([(n, _dock(s), m) for n, s, m, k in items], name=f"lower_bay_{st}")
        f = OUT / f"assy_lower_bay_{st}.step"
        C.export_step(a, f)
        files.append(f)
    items = assy.state_items("hold_RC")
    subs = {
        "sub_nest_anvil": lambda n: n.startswith(("anvil", "nest_frame", "datum", "pusher", "guide_bush", "gasket",
                                                  "insert", "ret_", "heater", "M_w", "card_presence")),
        "sub_cold_stack": lambda n: n.startswith(("peek_break", "cold_block", "peltier", "heatsink", "fan", "exhaust",
                                                  "foam", "thermistor_T_cold", "thermistor_T_heatsink")),
        "sub_Mc_units": lambda n: n.startswith("Mc"),
        "sub_Md_system": lambda n: n.startswith("Md_"),
        "sub_electrode_bay": lambda n: n.startswith(("ebay", "pogo", "WE_relay", "RH_", "gamry")),
        "sub_tubes": lambda n: n.startswith("tube_"),
    }
    for nm, f_ in subs.items():
        a = C.assembly([(n, _dock(s), m) for n, s, m, k in items if f_(n)], name=nm)
        f = OUT / f"{nm}.step"
        C.export_step(a, f)
        files.append(f)
    return files


def main(fast=False):
    t0 = time.time()
    log = {}
    log["calcs"] = calcs.run()
    (OUT / "calcs.json").write_text(json.dumps(log["calcs"], indent=1))
    print(f"calcs done {time.time() - t0:.0f} s")
    chk = checks.run(md=not fast)
    (OUT / "checks.json").write_text(json.dumps(chk, indent=1, default=str))
    print(f"checks done {time.time() - t0:.0f} s")
    files = export_parts() + export_assemblies()
    print(f"STEP done {time.time() - t0:.0f} s")
    pngs = render.render_all(OUT)
    print(f"PNG done {time.time() - t0:.0f} s")
    big = [(f.name, round(f.stat().st_size / 1e6, 2)) for f in files if f.stat().st_size > 8e6]
    summary = {"step_files": len(files), "png_files": len(pngs), "steps_over_8MB": big,
               "interference_hits": {k: v for k, v in chk["interference"].items() if v},
               "md_sweep_collisions": {k: v["n_collisions"] for k, v in chk.get("md_sweep", {}).items()},
               "run_time_s": round(time.time() - t0, 1)}
    (OUT / "build_summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main(fast="--fast" in sys.argv)
