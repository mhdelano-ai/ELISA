"""DOCK UPPER assemblies: head (card coords -> dock), lid frame (dock), card envelope (from interface.py only),
three configurations: 'closed' (latched, head down, de-energised valve states), 'raised' (lid closed, head up 8,
no card in the bores: pins at the 0.2 drop stop), 'open' (raised head, lid at 85 deg)."""
from __future__ import annotations

import cadquery as cq

from elisa_cad import interface as IF
from elisa_cad.dock_upper import params as P
from elisa_cad.dock_upper import parts as Pt

ORIGIN = IF.CARD_ORIGIN_IN_DOCK


def card_envelope():
    """Card envelope from interface.py (CARD agent geometry not used): L3 body with pin bores, die window, vent
    recesses and the thermal-break slot; laminate L0-L2 slab; die. Card coords."""
    z0, z1 = IF.Z_L3
    body = Pt.box(0, IF.CARD_L, 0, IF.CARD_W, z0, z1)
    for v in IF.VALVES.values():
        body = body.cut(Pt.cyl(v.xy[0], v.xy[1], z0 - 0.1, z1 + 0.1, v.bore_d))
        body = body.cut(cq.Workplane("XY").workplane(offset=z1 - IF.PLUNGER["card_bore_lead_in"])
                        .center(*v.xy).circle(v.bore_d / 2).workplane(offset=IF.PLUNGER["card_bore_lead_in"] + 0.01)
                        .circle(v.bore_d / 2 + IF.PLUNGER["card_bore_lead_in"] + 0.01).loft())
    c = IF.DIE_WINDOW_CLEAR
    body = body.cut(Pt.box(IF.DIE_X[0] - c, IF.DIE_X[1] + c, IF.DIE_Y[0] - c, IF.DIE_Y[1] + c, z0 - 0.1, z1 + 0.1))
    for (x, y) in IF.VENTS.values():
        body = body.cut(Pt.cyl(x, y, z1 - 0.3, z1 + 0.1, IF.VENT_DISC_D + 0.4))
    # break slot except the two bridges
    yb = [0.0] + [v for b in IF.BREAK_BRIDGES_Y for v in b] + [IF.CARD_W]
    for i in range(0, len(yb), 2):
        body = body.cut(Pt.box(IF.X_BREAK[0], IF.X_BREAK[1], yb[i], yb[i + 1], z0 - 0.1, z1 + 0.1))
    ins = IF.LAMINATE_INSET
    lam = Pt.box(ins, IF.CARD_L - ins, ins, IF.CARD_W - ins, 0.0, z0)
    lam = lam.cut(Pt.box(IF.DIE_X[0] - c, IF.DIE_X[1] + c, IF.DIE_Y[0] - c, IF.DIE_Y[1] + c, IF.Z_L1B[0], z0 + 0.1))
    die = Pt.box(IF.DIE_X[0], IF.DIE_X[1], IF.DIE_Y[0], IF.DIE_Y[1], IF.DIE_Z[0], IF.DIE_Z[1])
    return [("CARD_ENV_L3", body, "COC"), ("CARD_ENV_L0-L2", lam, "COC_foil"), ("CARD_ENV_die", die, "glass")]


def head_parts(state="closed", routes=None):
    """List of (name, solid in CARD coords with the head LOWERED, material, kind). kind: 'custom'|'env'|'std'.
    state 'closed': card present, de-energised (all closed, V3 open). 'nocard': pins at the drop stop."""
    routes = routes or Pt.route_galleries()
    out = []
    add = lambda n, s, m, k="custom": out.append((n, s, m, k))
    add("heater_block", Pt.heater_block(), "aluminium")
    add("guide_plate_lower", Pt.guide_plate(True), "copper")
    add("guide_plate_upper", Pt.guide_plate(False), "copper")
    add("peek_plate", Pt.peek_plate(), "PEEK")
    add("V8_bush", Pt.v8_bush(), "copper")
    add("spring_plate", Pt.spring_plate(), "steel")
    for i, s in enumerate(Pt.standoffs()):
        add(f"standoff_{i:02d}", s, "PEEK")
    gr = Pt.gas_rings()
    for pid, r in gr:
        add(f"ENV_gas_ring_{pid}_ID5_OD7_t1", r.translate((0, 0, -0.25 if state == "nocard" else 0.0)),
            "elastomer", "env")
    for pid, b in Pt.gas_barbs():
        add(f"ENV_gas_barb_M3_{pid}", b, "steel", "env")
    pad_dz = -P.PAD_STOP_BELOW_DIE if state == "nocard" else 0.0
    foot, sil, pspr = Pt.press_pad(pad_dz)
    add("press_pad_stem_foot", foot, "steel")
    add("press_pad_silicone", sil, "elastomer")
    add("ENV_press_pad_spring", pspr, "steel", "env")
    for vid, v in IF.VALVES.items():
        if vid == "V3":
            dz = P.STROKE if state in ("closed", "nocard") else 0.0     # de-energised: V3 OPEN (pin up)
        else:
            dz = -P.DROP_BELOW_CLOSED if state == "nocard" else 0.0
        pin, btn = Pt.pin_solid(v, dz)
        add(f"pin_{vid}", pin, "steel")
        add(f"button_{vid}", btn, "steel")
        add(f"ENV_spring_{vid}", Pt.spring_env(v, dz), "steel", "env")
        yk, top = Pt.yoke(vid, 0.0)
        add(f"yoke_{vid}", yk, "steel")
    for vid in IF.CYLINDERS:
        c = IF.CYLINDERS[vid]
        if vid == "V3":
            rod = Pt.cyl(c["xy"][0], c["xy"][1], P.TIER_Z[0][1], 52.0, P.ROD_D)
            add("rod_V3", rod, "steel")
            add("ENV_limit_spring_V3", Pt.tube(c["xy"][0], c["xy"][1], 52.0, 58.5, 4.0, 2.6), "steel", "env")
        else:
            add(f"rod_{vid}", Pt.rod_solid(vid), "steel")
    pis = Pt.pistons()
    for vid, (p_, m_, s_) in pis.items():
        add(f"piston_{vid}", p_, "PTFE")
        add(f"ENV_magnet_{vid}_D2x1", m_, "NdFeB", "env")
        add(f"ENV_return_spring_{vid}", s_, "steel", "env")
    for name, solid in Pt.cylinder_block_layers(routes).items():
        add(f"cyl_block_{name}", solid, "aluminium")
    rear, right, barbs = Pt.gallery_headers(routes)
    add("gallery_header_rear", rear, "aluminium")
    add("gallery_header_right", right, "aluminium")
    add("ENV_gallery_barbs_x21", barbs, "steel", "env")
    for name, ear, pin in Pt.guide_ears():
        add(f"guide_ear_{name}", ear, "aluminium")
        add(f"guide_pin_{name}", pin, "steel")
    pcb, sens = Pt.hall_pcb()
    add("ENV_hall_pcb", pcb, "pcb", "env")
    add("ENV_hall_DRV5055_x21", sens, "copper", "env")
    br, sp = Pt.bridge()
    add("bridge", br, "aluminium")
    add("bridge_spacers", Pt.union_all([sp]), "aluminium")
    top_card = P.POST_TOP_Z - ORIGIN[2]
    for i, p in enumerate(Pt.posts(top_card)):
        add(f"guide_post_{i}", p, "steel")
    fol = P.CAM["follower_top_latched_dock"] - ORIGIN[2] + (0.0 if state == "closed" else P.CLAMP_SPRING["overtravel"])
    for i, (h, cap, spr) in enumerate(Pt.thrust_units(fol)):
        add(f"thrust_housing_{i}", h, "aluminium")
        add(f"thrust_cap_{i}", cap, "steel")
        add(f"ENV_clamp_spring_{i}_D16", spr, "steel", "env")
    for name, m in Pt.manifolds():
        out.append((name, m, "envelope", "env"))
    for name, h in Pt.heaters_and_sensors():
        out.append((name, h, "heater" if "heater" in name else "copper", "env"))
    return out


def to_dock(parts, dz=0.0):
    ox, oy, oz = ORIGIN
    return [(n, s.translate((ox, oy, oz + dz)), m, k) for (n, s, m, k) in parts]


def lid_parts(latched=True):
    out = [(n, s, m, "custom") for (n, s, m) in Pt.lid_frame()]
    out.append(("cover", Pt.cover(), "aluminium", "custom"))
    sh, ecc, lev = Pt.cam_parts(latched)
    out += [("cam_shaft", sh, "steel", "custom"), ("cam_eccentrics", ecc, "steel", "custom"),
            ("cam_lever", lev, "steel", "custom")]
    for n, s, m in Pt.handle_and_latches():
        out.append((n, s, m, "env" if n.startswith("ENV") else "custom"))
    for n, s, m in Pt.lid_switch_and_umbilical():
        out.append((n, s, m, "env" if n.startswith("ENV") else "custom"))
    return out


def fixed_parts():
    return [(n, s, m, "custom") for (n, s, m) in Pt.hinge_parts()]


def rotate_lid(parts, angle):
    hx, hy, hz = IF.LID_HINGE_AXIS["point"]
    return [(n, s.rotate((hx, hy, hz), (hx + 1, hy, hz), -angle), m, k) for (n, s, m, k) in parts]


def configuration(name, routes=None):
    """Returns dict(rotating=[...], fixed=[...], card=[...]) in DOCK coords."""
    routes = routes or Pt.route_galleries()
    card = to_dock([(n, s, m, "card") for (n, s, m) in card_envelope()])
    if name == "closed":
        head = to_dock(head_parts("closed", routes))
        lid = lid_parts(latched=True)
        rot = head + lid
    else:
        head = to_dock(head_parts("nocard", routes), dz=P.HEAD_DROP)
        lid = lid_parts(latched=False)
        rot = head + lid
        if name == "open":
            rot = rotate_lid(rot, IF.LID_HINGE_AXIS["open_angle_deg"])
    return dict(rotating=rot, fixed=fixed_parts(), card=card)
