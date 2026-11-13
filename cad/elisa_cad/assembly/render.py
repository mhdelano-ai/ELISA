"""Renders of the integrated dock (docs/23 §3.3) with the z-buffer renderer (zrender.py). Dock coordinates.
Labels are placed at real 3-D points; section views cut every solid with a half-space and tint the cut faces."""
from __future__ import annotations

import cadquery as cq

from .. import interface as I
from . import collect as K
from . import zrender as Z

O = I.CARD_ORIGIN_IN_DOCK
LID_GHOST = (0.72, 0.74, 0.78, 0.22)
GHOST_NAMES = ("cover",)


def _it(items, ghost=GHOST_NAMES, drop=()):
    out = []
    for it in items:
        if it["name"].startswith(drop):
            continue
        m = it["material"]
        if it["name"].startswith(ghost):
            m = LID_GHOST
        out.append((it["shape"], m, it["module"] + ":" + it["name"]))
    return out


def _cd(x, y, z):
    return (x + O[0], y + O[1], z + O[2])


def cut_items(items, axis, value, keep="below", window=None):
    """Keep the half-space axis <= value ('below') or >= value ('above'); window = optional ((x0,y0,z0),(x1,y1,z1))
    clip box applied as well (dock coords)."""
    big = 2000.0
    lo = [-big, -big, -big]
    hi = [big, big, big]
    k = "xyz".index(axis)
    if keep == "below":
        hi[k] = value
    else:
        lo[k] = value
    if window:
        for i in range(3):
            lo[i] = max(lo[i], window[0][i])
            hi[i] = min(hi[i], window[1][i])
    box = cq.Solid.makeBox(hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2], cq.Vector(*lo))
    bb_box = (lo, hi)
    out = []
    for s, m, n in items:
        b = s.BoundingBox()
        if b.xmax < lo[0] or b.xmin > hi[0] or b.ymax < lo[1] or b.ymin > hi[1] or b.zmax < lo[2] or b.zmin > hi[2]:
            continue
        inside = b.xmin >= lo[0] and b.xmax <= hi[0] and b.ymin >= lo[1] and b.ymax <= hi[1] and \
            b.zmin >= lo[2] and b.zmax <= hi[2]
        if inside:
            out.append((s, m, n))
            continue
        try:
            c = s.intersect(box)
            if c.Volume() > 1e-6:
                out.append((c, m, n))
        except Exception:  # noqa: BLE001
            pass
    return out, bb_box


def render_all(OUT, log=print):
    closed = K.scene("closed", "hold_RC")
    full = _it(closed)
    # 1-2 overall iso views (lid cover translucent)
    lab = [(_cd(37.75, 25, 125), "lid (UPPER): head, 21 pin cylinders,\npilot valves, cam + latches", (-170, -60)),
           ((75, 2, 90), "cold-box door (BASE)", (-60, 60)), ((395, 2, 140), "bottle door (BASE)", (40, 70)),
           ((525, 90, 150), "Gamry Reference 600+", (40, -60)), ((235, 2, 120), "front-bay panel + Peltier louvre",
                                                                  (0, 70))]
    Z.render(full, OUT / "dock_iso_front_left_closed.png", "iso_fl", px=(2000, 1500), labels=lab,
             title="Integrated dock + card A, closed and latched (read state): iso front-left; lid cover translucent")
    log("render dock_iso_front_left_closed")
    lab2 = [(_cd(37.75, 25, 125), "lid (UPPER)", (-60, -80)), ((525, 200, 190), "Gamry Reference 600+ (bench)",
                                                                        (60, -50)),
            ((395, 2, 140), "bottle door", (-60, 80))]
    Z.render(full, OUT / "dock_iso_front_right_closed.png", "iso_fr", px=(2000, 1500), labels=lab2,
             title="Integrated dock + card A, closed (read state): iso front-right; lid cover translucent")
    log("render dock_iso_front_right_closed")
    # 3 open with the card above the nest
    lo = list(K.lower("load")) + list(K.upper("open")) + list(K.base(True))
    card_up = [dict(it, shape=it["shape"].translate(cq.Vector(0, 0, 60.0))) for it in K.card()]
    win = ((140, -30, 100), (330, 330, 400))
    its = _it(lo + card_up, drop=())
    its = [t for t in its if not t[2].startswith(("BASE:panel_front", "BASE:panel_top", "BASE:rail_front"))]
    Z.render(its, OUT / "dock_open_loading.png", "iso_fl_steep", px=(1900, 1600),
             labels=[(_cd(37.75, 25, 66), "card A lowered vertically\n(top up, reagent zone left)", (-200, -40)),
                     (_cd(80, 52, 5), "nest corner block\n(poka-yoke)", (170, 30)),
                     (_cd(37.75, 25, 0), "nest: datum pins A/B,\npushers, 2 guide bushes", (-230, 120)),
                     ((235, 150, 330), "lid open 85 deg\n(head raised)", (120, -40))],
             title="Loading: lid open 85 deg, head raised, M_c parked, M_d parked lowered, pogo down;\n"
                   "card 60 mm above the nest (front-bay and top panels hidden)")
    log("render dock_open_loading")
    # 4 full-height section through IC1/IC2 (card x 40), keep x >= 40, look from -X
    coll = list(K.card()) + list(K.lower("collect_IC1")) + list(K.upper("closed")) + list(K.base(True))
    sec, _ = cut_items(_it(coll), "x", O[0] + 40.0, keep="above", window=((0, -40, -5), (600, 460, 400)))
    Z.render(sec, OUT / "section_chamber_full_height.png", "left", px=(1500, 1700), cut_plane=((O[0] + 40, 0, 0),
             (1, 0, 0)), bounds=(-440, 0, 0, 335),
             labels=[(_cd(40, 38, 6.2), "IC1 (card)", (-120, -60)), (_cd(40, 12, 6.2), "IC2", (120, -60)),
                     (_cd(40, 38, -3), "M_c1 up (gap 0.16)", (-160, 40)), (_cd(40, -6.7, -46), "M_c2 parked", (160, 40)),
                     (_cd(40, 25, 20), "lid head", (160, -120)), ((230, 110, 42), "LOWER bay base plate on the BASE deck",
                                                                  (-60, 60))],
             title="Full-height section x_card = 40 (dock X 230) through IC1/IC2, W1/W2 and the M_c units,\n"
                   "looking +X (front of the dock on the right); state collect_IC1, lid closed and latched",
             note="M_c1 up under W1 (gap 0.16), M_c2 parked on its swing. Cut faces lighter.")
    log("render section_chamber_full_height")
    # 4b zoom of the same section
    sec2, _ = cut_items(_it(list(K.card()) + list(K.lower("collect_IC1")) + list(K.upper("closed"))), "x", O[0] + 40.0,
                        keep="above", window=((0, O[1] - 25, O[2] - 60), (600, O[1] + 75, O[2] + 45)))
    Z.render(sec2, OUT / "section_chamber_zoom_collect_IC1.png", "left", px=(1800, 1400),
             cut_plane=((O[0] + 40, 0, 0), (1, 0, 0)),
             labels=[(_cd(40, 38, 3), "IC1 chamber (185 uL)", (-150, -120)), (_cd(40, 38, -2.6), "M_c1 up, gap 0.16",
                                                                         (-200, 60)),
                     (_cd(40, 12, 3), "IC2", (120, -110)), (_cd(40, 25, 11), "heater block + CuSn8 guides", (40, -160)),
                     (_cd(40, -6.7, -46), "M_c2 parked (swing)", (170, -20)), (_cd(40, 25, -10), "anvil 5-mm plate",
                                                                                 (0, 90))],
             title="Section x_card = 40, state collect_IC1 (M_c1 up under W1, M_c2 parked),\n"
                   "lid closed: head, card, anvil, magnets")
    log("render section_chamber_zoom")
    # 5 section along the readout cell / die: plane x_card = 58.0 (RC, G4, pogo WE2/LOOP_A, M_d holder), keep x <= 58
    sec3, _ = cut_items(_it(closed), "x", O[0] + 58.0, keep="below",
                        window=((0, O[1] + 14, O[2] - 16), (600, O[1] + 38, O[2] + 27)))
    Z.render(sec3, OUT / "section_cell_die_pogo_Md.png", "right", px=(1500, 1900),
             cut_plane=((O[0] + 58.0, 0, 0), (1, 0, 0)),
             labels=[(_cd(58, 28.3, 0.7), "die (face down)", (-150, -150)), (_cd(58, 25, 0.25), "readout cell 0.2",
                                                                            (-200, -40)),
                     (_cd(58, 30.6, -1.5), "pogo pins on the pads", (170, 40)), (_cd(58, 25, -2.5), "M_d holder at RC",
                                                                                 (-170, 80)),
                     (_cd(58, 31.4, 2.5), "die-back press pad", (170, -110)), (_cd(58, 22.6, 4), "G4 pin", (-180, -100)),
                     (_cd(58, 32, -30), "electrode bay (grounded)", (170, 0))],
             title="Section x_card = 58.0: readout cell, die, G4 pin,\npogo WE2/LOOP_A, M_d holding at the RC;\n"
                   "read state, looking -X")
    log("render section_cell_die")
    # 6 section through a port insert (P_in, P_byp) with the real card: plane x_card = 34.2
    sec4, _ = cut_items(_it(closed), "x", O[0] + 34.2, keep="below",
                        window=((0, O[1] + 16, O[2] - 20), (600, O[1] + 34, O[2] + 8.5)))
    Z.render(sec4, OUT / "section_port_insert_P_in_P_byp.png", "right", px=(1800, 1300),
             cut_plane=((O[0] + 34.2, 0, 0), (1, 0, 0)),
             labels=[(_cd(34.2, 27.3, 0.07), "P_in foil hole D1.0", (-160, -110)),
                     (_cd(34.2, 27.3, -0.2), "gasket 1.7/3.3 x 0.5", (-220, 40)),
                     (_cd(34.2, 27.3, -8), "PEEK insert + bonded 1/16in tube", (-120, 120)),
                     (_cd(34.2, 23.3, -0.2), "P_byp", (150, 60)), (_cd(34.2, 25, 3.5), "card L3", (170, -110))],
             title="Section x_card = 34.2 through the P_in and P_byp port inserts, real card, closed")
    log("render section_port")
    # 7 bench layout (top view)
    bench = list(_it(closed))
    stack = cq.Solid.makeBox(343.0, 712.0, 711.0, cq.Vector(-393.0, 0.0, 0.0))
    bench.append((stack, (0.75, 0.75, 0.80, 1.0), "ACQUITY"))
    bench.append((cq.Solid.makeBox(1060.0, 750.0, 2.0, cq.Vector(-430.0, -20.0, -2.0)), (0.93, 0.92, 0.88, 1.0),
                  "bench"))
    Z.render(bench, OUT / "bench_layout_top.png", "top", px=(2000, 1500),
             labels=[((-221, 356, 711), "Waters ACQUITY I-Class stack\n343 x 712 (footprint UNVERIFIED for SM-FL)",
                      (0, 0)), ((235, 210, 330), "dock 470 x 420", (0, -180)), ((525, 225, 190), "Gamry\nRef 600+",
                                                                                (0, 0)),
                      ((0, 110, 160), "PEEK line SM-FL -> P_in", (-120, -60))],
             title="Bench layout, top view: stack | 50 mm | dock | 10 mm | Gamry (bench 1060 x 750 drawn, UNVERIFIED)")
    log("render bench_layout")
    # 8 exploded view of the four modules
    ex = []
    for it in K.base(True):
        if it["name"].startswith(("panel_", "rail_", "post_", "well_rear", "partition", "rear_low_cover")):
            continue
        ex.append((it["shape"], it["material"], "BASE:" + it["name"]))
    for it in K.lower("hold_RC"):
        ex.append((it["shape"].translate(cq.Vector(0, 0, 260.0)), it["material"], "LOWER:" + it["name"]))
    for it in K.card():
        ex.append((it["shape"].translate(cq.Vector(0, 0, 330.0)), it["material"], "CARD:" + it["name"]))
    for it in K.upper("closed"):
        m = LID_GHOST if it["name"].startswith(GHOST_NAMES) else it["material"]
        ex.append((it["shape"].translate(cq.Vector(0, 0, 400.0)), m, "UPPER:" + it["name"]))
    Z.render(ex, OUT / "exploded_four_modules.png", "iso_fl", px=(1700, 2000),
             labels=[((235, 110, 760), "DOCK UPPER (lid, head) +400", (260, 0)),
                     ((228, 100, 506), "CARD A +330", (300, 0)), ((235, 110, 400), "DOCK LOWER (nest, anvil, magnets,"
                                                                                   " stage, electrode bay) +260",
                                                                     (330, 40)),
                     ((235, 210, 120), "DOCK BASE (panels, posts, rails hidden)", (330, 0))],
             title="Exploded view of the four modules along Z (offsets in mm)")
    log("render exploded")
