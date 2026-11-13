"""Calculations of docs/22: liquid budget and bottle sizing, cold-box heat load, power budget, air supply, mass and
centre of gravity, and the one-off geometric checks. All arithmetic is here so the document quotes printed numbers."""
from __future__ import annotations

import itertools
import math

from . import fluidics as F
from . import layout as L
from . import params as P

# ============================================================================================== liquid budget
RUNS = 14                                   # docs/13 §5.2 card cap
A1_DOCK_PER_RUN = 1.52                      # mL, docs/13 §3.7 (rinses 600 + cleaning 900 + chases 10 + WL 10 uL)
WASTE_PER_RUN = 1.9                         # mL, docs/13 §3.7 (incl. BSM A1 0.38 mL to P_byp)
POSTHIGH_EXTRA = 2                          # recovery/post-high cycles per card allowance, docs/13 §4 ("2 recovery")
RECOVERY_A1 = 1.0                           # mL per recovery cycle [assessment]: 6 x 150 uL rinse + flushes
CONJ_FILL = 0.26                            # mL, docs/13 §5.2
HQDP_FILL = 0.60                            # mL (0.75 fallback), docs/13 §5.2
BEAD_DOSE = 10.0e-3                         # mL, docs/13 §5.1
BSM_PARK = 1.0e-3 * 60 * 8                  # mL per 8 h, 1 uL/min parked to the bypass (docs/13 §7.3)
CARDS_PER_DAY = 3                           # 24 h operation at 8 h per card [assessment, worst case]


def prime_volume():
    """A1 to prime at docking (Derived from the routed lines): every pump line volume x 3 + syringes once."""
    lines = sum(r_vol(r) for r in F.ROUTES if r.tube.startswith(("PEEK", "FEP")) and "purge" not in r.name)
    syr = sum(P.PUMP_SYRINGE_uL.values())
    return (3 * lines + syr) / 1000.0, lines / 1000.0, syr / 1000.0


def r_vol(r):
    idm = F.TUBES[r.tube][1]
    return math.pi / 4 * idm ** 2 * r.total + r.inline_uL


def liquid_budget():
    prime, lines, syr = prime_volume()
    pcf = next(r for r in F.ROUTES if r.port == "P_cf")
    prf = next(r for r in F.ROUTES if r.port == "P_rf")
    pb = next(r for r in F.ROUTES if r.port == "P_b")
    a1_card = RUNS * A1_DOCK_PER_RUN + POSTHIGH_EXTRA * RECOVERY_A1 + prime
    conj_card = CONJ_FILL + 2 * r_vol(pcf) / 1000.0 + 0.10    # line primed once to waste + line hold-up + tube dead
    hqdp_card = HQDP_FILL + 2 * r_vol(prf) / 1000.0 + 0.20
    hqdp_card_fb = 0.75 + 2 * r_vol(prf) / 1000.0 + 0.20
    bead_card = RUNS * BEAD_DOSE + 2 * r_vol(pb) / 1000.0 + 0.10   # + line priming + vial dead volume [assessment]
    waste_card = RUNS * WASTE_PER_RUN + POSTHIGH_EXTRA * RECOVERY_A1 + prime + BSM_PARK + 0.5
    rows = {
        "A1 (dock)": dict(per_card=a1_card, per_day=a1_card * CARDS_PER_DAY, bottle_mL=500,
                          note=f"14 x 1.52 + 2 x {RECOVERY_A1} + prime {prime:.1f}"),
        "conjugate": dict(per_card=conj_card, per_day=conj_card, bottle_mL=2, note="fresh tube per card (daily)"),
        "HQDP": dict(per_card=hqdp_card, per_day=hqdp_card, bottle_mL=15,
                     note=f"fallback mode {hqdp_card_fb:.2f} mL; fresh per card"),
        "beads": dict(per_card=bead_card, per_day=bead_card, bottle_mL=2, note="fresh vial per card"),
        "waste": dict(per_card=waste_card, per_day=waste_card * CARDS_PER_DAY, bottle_mL=1000,
                      note="alarm at 800 mL"),
    }
    for k, v in rows.items():
        v["cards_per_fill"] = v["bottle_mL"] * (0.8 if k == "waste" else 0.9) / v["per_card"]
    return rows, dict(prime_mL=prime, lines_uL=lines * 1000, syringes_uL=syr * 1000)


# ============================================================================================== cold box heat load
def cold_box_heat():
    (x0, y0, z0), (x1, y1, z1) = P.COLD_BOX["outer"]
    w = P.COLD_BOX["wall"]
    A_out = 2 * ((x1 - x0) * (y1 - y0) + (x1 - x0) * (z1 - z0) + (y1 - y0) * (z1 - z0)) * 1e-6
    (a0, b0, c0), (a1, b1, c1) = L.COLD_INNER
    A_in = 2 * ((a1 - a0) * (b1 - b0) + (a1 - a0) * (c1 - c0) + (b1 - b0) * (c1 - c0)) * 1e-6
    A_m = math.sqrt(A_out * A_in)
    dT = P.T_AMB_IN_DOCK - P.T_COLD
    q_wall = P.K_INSUL * A_m * dT / (w * 1e-3)
    q_door = 0.5 * q_wall                                    # gasket + seam allowance [assessment]
    q_shaft = 16.0 * math.pi / 4 * 4e-3 ** 2 * dT / (w * 1e-3)   # 4 mm stainless rocker shaft (k 16 W/m/K class)
    q_tubes = 6 * 0.25 * 0.79e-3 ** 2 * math.pi * dT / (w * 1e-3)   # 6 polymer tubes, k ~0.25 W/m/K [assessment]
    q_purge = 1.2 * 1005 * (0.1e-3 / 60) * dT               # 0.1 L/min dry air
    q_rocker = 0.0                                           # motor outside the box (CHOICE-B6)
    q_total = q_wall + q_door + q_shaft + q_tubes + q_purge + q_rocker
    # thermal mass for pull-down: liner + holder block + cradle + liquids
    m_liner = A_in * LINER_T_M() * 2700
    C_th = m_liner * 900 + 30 * 30 * 25 * 2.7e-6 * 900 + 0.05 * 900 + 0.003 * 4186
    cap_at_dT = P.COOLER["Q_W"] * 0.4                      # [assessment] ~40 % of Qmax at ~25 K across the TEC
    t_pull = C_th * (P.T_LAB - P.T_COLD) / max(cap_at_dT - q_total / 2, 1e-6) / 60
    # outer-skin condensation check
    h_out = 8.0                                              # W/m2/K natural convection [assessment]
    dT_skin = (q_wall / A_out) / h_out
    return dict(A_out=A_out, A_in=A_in, A_m=A_m, dT=dT, q_wall=q_wall, q_door=q_door, q_shaft=q_shaft,
                q_tubes=q_tubes, q_purge=q_purge, q_total=q_total, C_th=C_th, cap_at_dT=cap_at_dT, t_pull_min=t_pull,
                dT_skin=dT_skin, T_skin_min=P.T_LAB - dT_skin)


def LINER_T_M():
    return P.LINER_T * 1e-3


# ============================================================================================== power budget
POWER = [  # (load, rail, peak W, average W, source)
    ("5 x Centris pumps (2 moving at once)", "M", 2 * 24 * 2.5, 5 * 3.0, "V:TECAN_CENTRIS_P peak 2.5 A at 24 V; idle 3 W each UNVERIFIED"),
    ("2 x Flow EZ + LINK", "M", 2 * 6 + 2, 2 * 6 + 2, "V:FLUIGENT_FEZ_P 6 W; LINK 2 W UNVERIFIED"),
    ("21 pilot valves (lid) <= 10 on at once", "M", 10 * 1.0, 4.0, "1 W per valve UNVERIFIED"),
    ("stepper drivers: M_c x2, M_d cam Z, rocker (LOWER parts; pogo lift is pneumatic, revised after review)", "M", 40.0, 8.0, "UNVERIFIED allowance"),
    ("aux valves: pogo-lift 3/2 + 3 x 3/2 fill/P_mv (<= 2 on, 1 W each UNVERIFIED; revised after review M5)", "M", 2.0, 0.2, "UNVERIFIED allowance"),
    ("M_d X-Y stage (Zaber class, own controller)", "M", 20.0, 6.0, "UNVERIFIED allowance"),
    ("controller, watchdog, DAQ, sensors, scanner, hub", "L", 12.0, 10.0, "UNVERIFIED allowance"),
    ("fans (1 x 80 mm + cooler fan)", "M", 4.0, 4.0, "UNVERIFIED"),
    ("cold box Peltier DA-024-24", "T", 24 * 2.4, 35.0, "V:LAIRD_TCA_CAT 2.4 A at 24 V; average [assessment]"),
    ("reagent-zone Peltier (LOWER)", "T", 40.0, 25.0, "UNVERIFIED allowance"),
    ("anvil heater + lid heater block (LOWER/UPPER)", "T", 40.0, 15.0, "UNVERIFIED allowance"),
]
PSU_EFF = 0.88      # UNVERIFIED class efficiency
PSU_RATING = {"M": 350.0, "T": 350.0, "L": 15.0}


def power_budget():
    rails = {}
    for n, r, pk, av, s in POWER:
        d = rails.setdefault(r, [0.0, 0.0])
        d[0] += pk
        d[1] += av
    pk = sum(v[0] for v in rails.values())
    av = sum(v[1] for v in rails.values())
    mains_pk = pk / PSU_EFF
    mains_av = av / PSU_EFF
    # heat into the electronics bay: PSU losses + driver losses (PWM 90 %) + logic
    loss_psu = mains_av - av
    loss_drivers = 0.10 * (35 + 25 + 15) + 0.05 * 30
    q_bay = loss_psu + loss_drivers + 10.0
    flow = q_bay / (1.2 * 1005 * 10.0)         # m^3/s for a 10 K rise
    return dict(rails=rails, peak_W=pk, avg_W=av, mains_peak_W=mains_pk, mains_avg_W=mains_av, q_bay_W=q_bay,
                airflow_m3s=flow, airflow_Lmin=flow * 60000, airflow_cfm=flow * 2118.88)


# ============================================================================================== air supply
def air_supply():
    # (revised at integration) lid cylinders: D6 bore, 90 mm^3 chamber per actuation at 400 kPa gauge (docs/20 §4.3/4.4:
    # 0.36 NmL per actuation, 17 per run); pogo-lift cylinder (LOWER, bore 6 x stroke 6, 2 actuations per card)
    v_cyl = 90.0e-9                                                # m^3 per actuation (docs/20 §4.3)
    free_per_act = v_cyl * P.AIR_LID_KPA / 101.3   # gauge ratio: chamber vents to ambient
    acts_per_h = 17 * 60 / 31.0                                    # 17 actuations per run (docs/20 §4.4), 31-min cadence
    q_cyl = free_per_act * acts_per_h * 1000                       # L/h
    q_pogo = (math.pi / 4 * 6.0 ** 2 * 6.0 + 50.0) * 1e-9 * P.AIR_LID_KPA / 101.3 * 2 * 1000 / 8.0
    q_purge = 0.1 * 60                                             # L/h
    q_fez_bleed = 2 * 0.5 * 60                                     # L/h, Flow EZ consumption allowance UNVERIFIED
    q_fill = 0.05                                                  # L/h, bottle pressurisation (negligible)
    total = q_cyl + q_pogo + q_purge + q_fez_bleed + q_fill
    reservoir_8h = total * 8                                       # L free air for an 8-h card without supply
    return dict(free_per_act_mL=free_per_act * 1e6, acts_per_h=acts_per_h, q_cyl_Lh=q_cyl, q_pogo_Lh=q_pogo,
                q_purge_Lh=q_purge, p_lid_kPa=P.AIR_LID_KPA, p_supply_min_kPa=P.AIR_SUPPLY_MIN_KPA,
                q_fez_Lh=q_fez_bleed, total_Lh=total, total_Lmin=total / 60, free_air_8h_L=reservoir_8h,
                tank_L_at_7bar_for_8h=reservoir_8h / 6.0)


# ============================================================================================== mass and CoG
ALLOW = {  # other agents' content (UNVERIFIED allowances), placed at their claim centroids
    "LOWER (nest, anvil, magnets, stage, electrode bay)": (8.0, "LOWER_bay"),
    "UPPER (lid head, cylinders, cover)": (5.0, "UPPER_lid_closed"),
}
LIQUIDS = [("A1 500 mL", 0.5, "A1_bottle_500mL"), ("waste 0-1 L (full)", 1.0, "waste_bottle_1L")]


def mass_cog(include_allow=True, waste_full=True):
    m, mx, my, mz = 0.0, 0.0, 0.0, 0.0
    groups = {}
    for it in L.ITEMS:
        if it.group == "bench":
            continue
        (x0, y0, z0), (x1, y1, z1) = it.box
        c = ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
        mm = it.mass
        if it.name == "waste_bottle_1L" and not waste_full:
            mm -= 1.0
        m += mm
        mx += mm * c[0]
        my += mm * c[1]
        mz += mm * c[2]
        groups[it.group] = groups.get(it.group, 0.0) + mm
    base_mass = m
    if include_allow:
        for k, (mm, cl) in ALLOW.items():
            (x0, y0, z0), (x1, y1, z1) = P.CL[cl]["box"]
            m += mm
            mx += mm * (x0 + x1) / 2
            my += mm * (y0 + y1) / 2
            mz += mm * (z0 + z1) / 2
    cog = (mx / m, my / m, mz / m)
    # support polygon = feet rectangle
    fx = [f[0] for f in P.FEET_XY]
    fy = [f[1] for f in P.FEET_XY]
    margin = min(cog[0] - min(fx), max(fx) - cog[0], cog[1] - min(fy), max(fy) - cog[1])
    # tipping: lateral force at the top edge (Z 330) that tips the dock over the front foot line
    tip_N = m * 9.81 * (cog[1] - min(fy)) / P.FZ
    return dict(base_mass=base_mass, total=m, cog=cog, margin=margin, groups=groups, tip_front_N=tip_N)


# ============================================================================================== geometric checks
def item_overlaps():
    """Pairwise AABB overlaps between DOCK BASE items (intended assemblies excluded)."""
    intended = {("conj_holder_block", "conj_tube_2mL"), ("partition_right", "gamry_lead_duct"),
                ("A1_bottle_500mL", "A1_cap"), ("bead_rocker_cradle", "bead_vial_2mL")}
    skip = {"base_plate", "drip_tray", "cold_box", "electronics_box", "electronics_box_side", "electronics_box_rear"}
    out = []
    for a, b in itertools.combinations(L.ITEMS, 2):
        if a.name in skip or b.name in skip or (a.name, b.name) in intended or (b.name, a.name) in intended:
            continue
        if all(min(a.box[1][i], b.box[1][i]) - max(a.box[0][i], b.box[0][i]) > 0.01 for i in range(3)):
            out.append((a.name, b.name))
    # items that must be INSIDE the hollow cold box / electronics box must not cut their walls
    return out


def contained(inner, outer, tol=0.01):
    return all(inner[0][i] >= outer[0][i] - tol and inner[1][i] <= outer[1][i] + tol for i in range(3))


def cold_and_elec_containment():
    res = []
    for n in ("bead_rocker_cradle", "bead_vial_2mL", "conj_holder_block", "conj_tube_2mL", "cooler_DA024_cold"):
        res.append((n, "cold inner", contained(L.get(n).box, L.COLD_INNER)))
    inners = {n: ((b[0][0] + 1, b[0][1] + 1, b[0][2] + 1), (b[1][0] - 1, b[1][1] - 1, b[1][2] - 1))
              for n, b in L.ELEC_BOXES.items()}   # (revised after review) three boxes
    for it in L.ITEMS:
        if it.group == "electronics" and not it.name.startswith("electronics_box") and \
                it.name not in ("connector_panel", "estop", "status_light"):
            ok = [n for n, inner in inners.items() if contained(it.box, inner)]
            res.append((it.name, "electronics inner " + (ok[0] if ok else "none"), bool(ok)))
    return res


def footprint_ok():
    """Every DOCK BASE item inside DOCK_FOOTPRINT except the bench items and the front controls."""
    (fx0, fy0, fz0), (fx1, fy1, fz1) = P.FOOT
    out = []
    for it in L.ITEMS:
        if it.group == "bench":
            continue
        b = it.box
        inside = b[0][0] >= fx0 - 0.01 and b[0][1] >= fy0 - 0.01 and b[0][2] >= fz0 - 0.01 and \
            b[1][0] <= fx1 + 0.01 and b[1][1] <= fy1 + 0.01 and b[1][2] <= fz1 + 0.01
        if not inside:
            out.append(it.name)
    return out


def bench_layout():
    stack_w, dock_w = P.ACQUITY["w"], P.FX
    gamry_w = P.GAMRY[1][0] - P.GAMRY[0][0]
    gap_dg = P.GAMRY[0][0] - P.FX
    width = stack_w + P.STACK_GAP + dock_w + gap_dg + gamry_w
    depth = max(P.ACQUITY["d"], P.FY, P.GAMRY[1][1])
    return dict(width=width, depth=depth, bench_depth=P.BENCH_DEPTH, fits_depth=depth <= P.BENCH_DEPTH,
                card_height_above_floor=P.BENCH_HEIGHT + I_card_z(), lid_top_open=388.3 + P.BENCH_HEIGHT)


def I_card_z():
    from .. import interface as I
    return I.ANVIL_TOP_Z_DOCK


# ============================================================================================== carry-over budget
def carryover_budget():
    """(revised after review, docs/24 B1) docs/13 §8.3 worst-determination budget re-scaled with the as-built geometry.
    Allocations are docs/13's (all UNVERIFIED placeholders). Scaling ASSUMPTIONS (not measured):
      path 2 (P_in line + M_in) and path 3 (C_k + its valve stubs): wetted channel/tube area ratio (adsorption-type
        term, the reviewer's basis, docs/24 B1); path 5 (tidal coil): coil wall-area ratio vs a 60 uL D0.508 coil
        (docs/13 §3.2.2; docs/13 §8.3 also quotes 'FEP ~320 mm2', which is inconsistent with 60 uL -> sensitivity);
      path 9 (cell stubs): stub-volume ratio (docs/13's own liquid arithmetic); all other paths unchanged (bead-count,
        valve-leak or SM-FL terms that the physical design does not change).
    Returns rows (path, docs13, RevB, RevC, basis) and totals (Derived)."""
    import math as m
    from .. import interface as I
    per = lambda w, h=I.CHANNEL_H: 2 * (w + h)
    ln = lambda pts: I.polyline_length(pts)
    route = {r.port: r for r in F.ROUTES if r.port}
    # path 2
    old2 = m.pi * 0.127 * 300.0 + per(0.5) * 12.0                    # docs/13: 0.3 m x 0.127 + M_in 12 mm
    m_in = per(0.5) * ln(I.M_IN)                                     # as built 19.0 mm (card CAD)
    revB2 = m.pi * 0.127 * route["P_in"].total + m_in
    revC2 = m.pi * F.TUBES[route["P_in"].tube][1] * route["P_in"].total + m_in
    # path 3: sample-wetted C_k (V1 bridge junction -> chamber) + bridge, vs docs/13 C_k 3.0 mm + 2 x 0.3 stubs
    x_br = I.CHANNELS["V1_bridge"]["pts"][0][0]
    ck = ln([(x_br, I.H1[0][1])] + I.H1[1:])
    old3 = per(0.5) * 3.0 + 2 * per(0.4) * 0.3
    new3 = per(0.5) * ck + per(0.4) * ln(I.CHANNELS["V1_bridge"]["pts"])
    revB3_reviewer = per(0.5) * ln(I.H1) / (per(0.5) * 3.0)          # whole rail, reviewer's ratio (5.4)
    # path 5
    coil60 = 60.0 / (m.pi / 4 * 0.508 ** 2) * m.pi * 0.508
    revB5 = max(791.0, 689.0) * m.pi * 0.508 / coil60                # Rev B routed coils (tubing_schedule Rev B)
    revC5 = max(route["P_d1"].total, route["P_d2"].total) * m.pi * 0.508 / coil60
    revC5_320 = max(route["P_d1"].total, route["P_d2"].total) * m.pi * 0.508 / 320.0
    # path 9: stubs G3, G4 (lane 0.5), V14, V15 (0.3)
    h = I.CHANNEL_H
    g3 = (I.DIE_X[0] - (I.VALVES["G3"].xy[0] + I.VALVES["G3"].tip_d / 2)) * 0.5 * h
    g4 = (I.DIE_Y[0] - (I.VALVES["G4"].xy[1] + I.VALVES["G4"].tip_d / 2)) * 0.5 * h
    st_new = g3 + g4 + 0.018 + 0.024                                 # V14, V15 unchanged (docs/18 DEV-2)
    st_old, st_revB = 0.044 + 0.044 + 0.026 + 0.016, 0.031 + 0.031 + 0.018 + 0.024
    rows = [  # (path, class, docs13, ratio Rev B, ratio Rev C, basis)
        ("1 SM-FL needle/loop/injector", "consec", 3e-5, 1.0, 1.0, "unchanged (E1.10)"),
        ("2 P_in line + M_in", "consec", 1e-5, revB2 / old2, revC2 / old2,
         "wetted area: line pi d L + M_in 1.35 mm2/mm x 19.0 mm [assumption]"),
        ("7 J, WLc, G_k'/V11/V12 stubs", "consec", 2e-5, 1.0, 1.0, "bead count (M1), unchanged"),
        ("8 cell beads/enzyme", "consec", 2e-5, 1.0, 1.0, "bead count (M1), unchanged"),
        ("9 cell stubs", "consec", 1e-6, st_revB / st_old, st_new / st_old, "stub volume (docs/13 liquid arithmetic)"),
        ("10 BW", "consec", 1e-6, 1.0, 1.0, "gate leak, unchanged"),
        ("3 C_k + valve stubs (sample-wetted)", "same", 1e-6, new3 / old3, new3 / old3,
         "wetted area of the sample path V1 bridge -> chamber [assumption]"),
        ("4 IC walls", "same", 1e-5, 1.0, 1.0, "185 uL working fill unchanged"),
        ("5 tidal coil", "same", 2e-6, revB5, revC5, "coil wall area vs 60 uL D0.508 [assumption]"),
        ("6 WL branch", "same", 1e-6, 1.0, 1.0, "bead count, unchanged"),
    ]
    tot = {}
    for col, idx in (("docs13", None), ("RevB", 3), ("RevC", 4)):
        c = sum(r[2] * (1.0 if idx is None else r[idx]) for r in rows if r[1] == "consec")
        s = sum(r[2] * (1.0 if idx is None else r[idx]) for r in rows if r[1] == "same")
        tot[col] = {"consecutive": c, "same_chamber": s, "worst": c + s}
    sens = {
        "RevC_with_docs13_literal_coil_320mm2": tot["RevC"]["worst"] + 2e-6 * (revC5_320 - revC5),
        "RevC_if_P_in_0.102_fallback": tot["RevC"]["worst"] + 1e-5 * ((m.pi * 0.1016 * route["P_in"].total + m_in) / old2
                                                                       - revC2 / old2),
        "RevB_reviewer_basis_whole_rail_Ck": tot["RevB"]["worst"] + 1e-6 * (revB3_reviewer - new3 / old3),
        "face_seal_annulus_RevB": "0.110 uL per port unswept (reviewer); Rev C: 0 (gasket on the tube OD)"}
    return {"rows": [dict(path=r[0], cls=r[1], docs13=r[2], ratio_RevB=round(r[3], 3), ratio_RevC=round(r[4], 3),
                          RevC=r[2] * r[4], basis=r[5]) for r in rows],
            "totals": tot, "sensitivity": sens, "criterion": 1e-4,
            "coil_mm": {"P_d1": round(route["P_d1"].total), "P_d2": round(route["P_d2"].total)}}
