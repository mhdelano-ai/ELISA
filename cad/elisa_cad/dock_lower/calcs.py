"""DOCK LOWER calculations for docs/21 §5 (Derived; inputs tagged). Run by build.py -> out/dock_lower/calcs.json.
Magnet fields: uniformly magnetised blocks by surface-charge integration, the method of
scripts/chip_round/design_A_docs13/revision_B/mag_b.py (B_r 1.3 T UNVERIFIED, bead moment 1.15e-13 A m^2
UNVERIFIED), re-implemented here for blocks at arbitrary positions; magnet-magnet forces as the sum over 0.5-mm
dipole cells of grad(m . B)."""
from __future__ import annotations

import math

import numpy as np

from .. import interface as I
from . import geom as G

MU0 = 4e-7 * math.pi
BR = 1.3            # T, N42 class (docs/13 §3.3.2, UNVERIFIED); supermagnete Q-10-10-05-N page: N42, Br not listed
M_BEAD = 1.15e-13   # A m^2 (docs/13 §3.3.2, UNVERIFIED)
mm = 1e-3


# ------------------------------------------------------------------------------------------------ magnetics
def bfield(P, centre_top, size, N=40):
    """B (T) at points P (..., 3) in mm (card coords) of a block magnetised +z with top-face centre centre_top (mm)
    and size (a, b, c) mm (c along z)."""
    a, b, c = (s * mm for s in size)
    P = (np.asarray(P, float) - np.asarray(centre_top, float)) * mm
    xs = (np.arange(N) + 0.5) / N * a - a / 2
    ys = (np.arange(N) + 0.5) / N * b - b / 2
    X, Y = np.meshgrid(xs, ys)
    X, Y = X.ravel(), Y.ravel()
    dA = (a / N) * (b / N)
    sh = P.shape[:-1]
    P = P.reshape(-1, 3)
    out = np.zeros_like(P)
    for i0 in range(0, len(P), 200):
        p = P[i0:i0 + 200]
        for zf, s in ((0.0, 1.0), (-c, -1.0)):
            R = np.stack([p[:, 0, None] - X[None], p[:, 1, None] - Y[None],
                          np.broadcast_to(p[:, 2, None] - zf, (len(p), len(X)))], -1)
            r3 = np.sum(R ** 2, -1) ** 1.5
            out[i0:i0 + 200] += s * np.sum(R / r3[..., None], 1) * dA
    return (BR / (4 * np.pi) * out).reshape(sh + (3,))


def absB(P, ct, size):
    return np.linalg.norm(bfield(P, ct, size), axis=-1)


def bead_force_pN(pt, ct, size, h=0.02):
    pt = np.asarray(pt, float)
    g = []
    for i in range(3):
        d = np.zeros(3)
        d[i] = h
        g.append((absB(pt + d, ct, size) - absB(pt - d, ct, size)) / (2 * h * mm))
    return float(M_BEAD * np.linalg.norm(g) * 1e12)


def magnet_force(ct_src, size_src, ct_tgt, size_tgt, cell=0.5, h=0.02):
    """Force (N) on the target block (magnetised +z, B_r) in the field of the source block."""
    a, b, c = size_tgt
    nx, ny, nz = (max(1, int(round(s / cell))) for s in (a, b, c))
    xs = ct_tgt[0] + ((np.arange(nx) + 0.5) / nx - 0.5) * a
    ys = ct_tgt[1] + ((np.arange(ny) + 0.5) / ny - 0.5) * b
    zs = ct_tgt[2] - (np.arange(nz) + 0.5) / nz * c
    pts = np.array([(x, y, z) for x in xs for y in ys for z in zs])
    mcell = BR / MU0 * (a * b * c * mm ** 3) / len(pts)        # A m^2 per cell
    F = np.zeros(3)
    for i in range(3):
        d = np.zeros(3)
        d[i] = h
        bz_p = bfield(pts + d, ct_src, size_src)[:, 2]
        bz_m = bfield(pts - d, ct_src, size_src)[:, 2]
        F[i] = mcell * np.sum((bz_p - bz_m) / (2 * h * mm))
    return F


def magnetics():
    r = {}
    mc, md, mw = G.MC_MAG, G.MD_MAG, I.MAGNETS["M_w"]["size"]
    c1 = I.IC1.center
    up1 = (c1[0], c1[1], G.MC_TOP_UP)
    dy, dz = G.mc_offset(G.MC_THETA_PARK, 1)
    park1 = (c1[0], c1[1] + dy, G.MC_TOP_UP + dz)
    iface_park1 = (I.MAGNETS["M_c1"]["parked_xy"][0], I.MAGNETS["M_c1"]["parked_xy"][1], I.MAGNETS["M_c1"]["z_top_down"])
    zb = I.Z_L0[1] + 0.0 + 0.16 - 0.16 + 0.30 - 0.14   # bead plane z = 0.30 above the magnet face -> card z 0.14 (foil top)
    zb = I.Z_L0[1]                                    # beads sit on the foil top, card z 0.14
    floor_c1 = (c1[0], c1[1], zb)
    r["Mc_park_this_design"] = {"centre_top": [round(v, 2) for v in park1]}
    r["F_bead_own_chamber_floor_Mc_parked_pN"] = round(bead_force_pN(floor_c1, park1, mc), 4)
    r["F_bead_own_chamber_floor_interface_park_pN"] = round(bead_force_pN(floor_c1, iface_park1, mc), 4)
    r["F_bead_own_chamber_floor_Zonly_25mm_pN_docs13"] = 0.055
    wall = (c1[0], c1[1] + 4.0, zb)
    r["F_bead_own_chamber_wall_foot_Mc_parked_pN"] = round(bead_force_pN(wall, park1, mc), 4)
    # other chamber with M_c1 up (unchanged geometry vs docs/13): spot value
    c2 = I.IC2.center
    r["F_bead_other_chamber_near_edge_Mc1_up_pN"] = round(bead_force_pN((c2[0], c2[1] + 4.0, zb), up1, mc), 4)
    # fields at the WE relay and the pogo pins
    relay = (58.25, 32.65, 0.5 * sum(G.RELAY["z"]))
    pads = (58.0, 31.5, I.DIE_Z[0])
    for lbl, ct, sz in (("Mc1_up", up1, mc), ("Mc1_parked", park1, mc),
                        ("Mc2_up", (c2[0], c2[1], G.MC_TOP_UP), mc),
                        ("Md_hold_RC", (I.RC_CENTER[0], I.RC_CENTER[1], G.MD_TOP_UP), md),
                        ("Mw", (I.BW.center[0], I.BW.center[1], I.MAGNETS["M_w"]["z_top"]), mw)):
        r[f"B_at_WE_relay_{lbl}_mT"] = round(float(absB(relay, ct, sz)) * 1e3, 3)
        r[f"B_at_pads_{lbl}_mT"] = round(float(absB(pads, ct, sz)) * 1e3, 3)
    # magnet-magnet forces
    md_bo = (I.BEAD_OUT_PATH[-1][0], I.BEAD_OUT_PATH[-1][1], G.MD_TOP_UP)
    mw_ct = (I.BW.center[0], I.BW.center[1], I.MAGNETS["M_w"]["z_top"])
    r["F_Md_at_beadout_stop_from_Mw_N"] = [round(v, 4) for v in magnet_force(mw_ct, mw, md_bo, md)]
    md_hold = (I.RC_CENTER[0], I.RC_CENTER[1], G.MD_TOP_UP)
    r["F_Md_at_hold_from_Mw_N"] = [round(v, 4) for v in magnet_force(mw_ct, mw, md_hold, md)]
    md_park = (I.M_D_PARK_POS[0], I.M_D_PARK_POS[1], G.MD_TOP_UP - G.MD_STROKE)
    r["F_Md_parked_from_Mc1_up_N"] = [round(v, 5) for v in magnet_force(up1, mc, md_park, md)]
    md_g = (G.GATHER[("IC1", "pass1")][0][0], G.GATHER[("IC1", "pass1")][0][1], G.MD_TOP_UP)
    r["F_Md_gather_IC1_from_Mc1_parked_N"] = [round(v, 5) for v in magnet_force(park1, mc, md_g, md)]
    r["F_Mc2_parked_from_Mc1_up_N"] = [round(v, 4) for v in magnet_force(
        up1, mc, (c2[0], c2[1] - dy, G.MC_TOP_UP + dz), mc)]
    # post deflection under the largest lateral magnet force (Ti D4 x 56 + D2 x 1.4 neck, cantilever from Z unit)
    E_ti = 110e3   # N/mm^2 (Ti-6Al-4V, UNVERIFIED handbook class value)
    Lp = G.MD_POST["z"][1] - G.MD_POST["z"][0]
    Ip = math.pi * G.MD_POST["d"] ** 4 / 64
    k = 3 * E_ti * Ip / Lp ** 3
    Flat = max(math.hypot(*r["F_Md_at_beadout_stop_from_Mw_N"][:2]), math.hypot(*r["F_Md_at_hold_from_Mw_N"][:2]))
    r["post_stiffness_N_per_mm"] = round(k, 2)
    r["post_deflection_um_at_max_lateral_magnet_force"] = round(Flat / k * 1e3, 2)
    # valve pins near M_c (lid side): field and gradient at V4 tip (worst neighbour of W1)
    v4 = (I.VALVES["V4"].xy[0], I.VALVES["V4"].xy[1], 1.0)
    Bv = float(absB(v4, up1, mc))
    gz = (float(absB((v4[0], v4[1], v4[2] + 0.1), up1, mc)) - float(absB((v4[0], v4[1], v4[2] - 0.1), up1, mc))) / (0.2 * mm)
    Vpin = math.pi * 0.6 ** 2 * 5.0 * mm ** 3   # lowest 5 mm of a D1.2 pin
    r["V4_pin_B_T"] = round(Bv, 3)
    r["V4_pin_gradB_T_per_m"] = round(abs(gz), 1)
    r["F_pin_austenitic_chi0.01_N"] = round(0.01 * Vpin / MU0 * Bv * abs(gz), 6)
    r["F_pin_ferromagnetic_saturated_Ms1.5e6_N"] = round(1.5e6 * Vpin * abs(gz), 4)
    return r


# ------------------------------------------------------------------------------------------------ mechanics
def plate():
    """Thin plate (5 mm Al) between the thick zones under the distributed clamp (Roark simply supported rectangle,
    alpha(a/b=1.5) = 0.0843 [Roark table 11.4, recalled, UNVERIFIED]); knock-down x5 for the openings [assessment]."""
    E = 69e3
    t = G.T_THIN
    b = G.POCKET_RECT[2] - G.POCKET_RECT[0]          # 30 (short span, x)
    a = G.POCKET_RECT[3] - G.POCKET_RECT[1]          # 50
    area_assay = (I.CARD_L - I.X_ASSAY[0]) * I.CARD_W
    q = I.CLAMP_DESIGN_FORCE / area_assay              # N/mm^2, whole latch force on the assay zone (upper bound)
    alpha = 0.0843
    w = alpha * q * b ** 4 / (E * t ** 3)
    # local: M_c up preload at the window rim and pogo shoulder (point loads, beta 0.1478 recalled UNVERIFIED)
    P_local = G.MC_UP_PRELOAD_N + 10.0
    w_pt = 0.1478 * P_local * b ** 2 / (E * t ** 3)
    # foil span over the widened slot under a 1.5 N slot plunger (docs/13 §2.1 formula, w ~ F a^2 / (16 pi D))
    from .geom import slot_poly
    D = 7.7e-3 * 1e3   # N mm (docs/13 §2.1: 7.7e-3 N m)
    widths = []
    for vid in ("G1", "G2", "G3", "G4", "V11", "V12"):
        from shapely.geometry import Point, LineString
        p = Point(I.VALVES[vid].xy)
        sp = slot_poly()
        # local slot width: shortest chord through the tip centre over 0..180 deg
        best = 99.0
        for ang in range(0, 180, 5):
            d = (math.cos(math.radians(ang)) * 10, math.sin(math.radians(ang)) * 10)
            seg = LineString([(p.x - d[0], p.y - d[1]), (p.x + d[0], p.y + d[1])]).intersection(sp)
            parts = getattr(seg, "geoms", [seg])
            for s in parts:
                if s.distance(p) < 1e-6:
                    best = min(best, s.length)
        # (revised after review, docs/24 S2) the slot is a long strip: clamped long rectangle under a central load,
        # w = 0.00791 F b^2 / D (Timoshenko coefficient recalled by the reviewer, UNVERIFIED); circle kept for reference.
        # F = 1.32 N = 1.2 N nominal + 10 % (closing force at the real height, docs/20 §4.1 Rev C); also at the 1.5 N limit
        w_c = 1.5 * (best / 2) ** 2 / (16 * math.pi * D) * 1e3
        w_s132 = 0.00791 * 1.32 * best ** 2 / D * 1e3
        w_s15 = 0.00791 * 1.5 * best ** 2 / D * 1e3
        widths.append((vid, round(best, 2), round(w_c, 1), round(w_s132, 1), round(w_s15, 1)))
    return {"q_N_per_mm2": round(q, 4), "span_short_mm": b, "span_long_mm": a,
            "w_uniform_um": round(w * 1e3, 2), "w_uniform_with_openings_x5_um": round(5 * w * 1e3, 1),
            "w_local_point_16N_um": round(w_pt * 1e3, 2),
            "foil_span_at_slot_valves_[id, min chord mm, circle um 1.5 N, strip um 1.32 N, strip um 1.5 N]": widths,
            "foil_deflection_limit_um_M4": 20.0,
            "budget": "magnet gap 0.16 +- 0.05 (docs/13 §6.2)"}


def seal():
    od, idd, t = G.GASKET["gasket_od"], G.GASKET["gasket_id"], G.GASKET["gasket_t"]
    A = math.pi / 4 * (od ** 2 - idd ** 2)
    eps = (t - I.FACE_SEAL["counterbore_depth"]) / t
    S = A / (math.pi * (od + idd) * t)                          # shape factor (loaded / free area)
    out = {"annulus_mm2": round(A, 2), "compression": round(eps, 3), "shape_factor": round(S, 2)}
    for sh, E in (("50ShA", 2.5), ("60ShA", 4.5), ("70ShA", 6.0)):   # Young's moduli UNVERIFIED class values
        Ec = E * (1 + 2 * 0.6 * S ** 2)                            # Gent/Lindley form, k = 0.6 UNVERIFIED
        out[f"F_per_seal_{sh}_N"] = round(Ec * eps * A, 1)
    out["n_liquid_seals"] = len(G.LIQ_PORTS)
    out["recommendation"] = "50-60 ShA EPDM/FFKM keeps 7-12 N per seal; > 10 N at 60+ ShA exceeds the docs/18 budget"
    return out


# ------------------------------------------------------------------------------------------------ thermal
def thermal():
    # (revised after review, docs/24 B2) every wall counted, no unexplained factor. Rev B: 1-mm full-depth PEEK on
    # -x/+-y (2.76 + 3.45 W, the y walls had been x0.1 and -x omitted) + break 0.86 W = 7.07 W. Rev C: each gap is a
    # 2-mm PEEK lip (z -2..0) over foam (z -15..-2); E break 4 mm the same; 4 PEEK pads 3 x 3 across 2 mm.
    k_peek, k_coc, k_foam = 0.25, 0.15, 0.035     # W/m K, UNVERIFIED handbook class values
    Ta, Tc = 25.0, 5.0
    cp, gap, lip, T = G.COLD_PLATE, G.PEEK_GAP, G.PEEK_LIP_T, G.ANVIL_T
    Ly = (cp["y"][1] - cp["y"][0]) * 1e-3                 # W wall and E break length (44)
    Lx = (cp["x"][1] - cp["x"][0]) * 1e-3                 # S and N walls (17.4 each)
    g_side = (k_peek * lip + k_foam * (T - lip)) / gap    # W/(m K) per metre of gap
    g_brk = (k_peek * lip + k_foam * (T - lip)) / 4.0
    q = {}
    q["gap_W_S_N_lip_plus_foam"] = (Ly + 2 * Lx) * g_side * (Ta - Tc)
    q["break_E_lip_plus_foam"] = (Ly + 2 * gap * 1e-3) * g_brk * (Ta - Tc)
    q["PEEK_pads_4x"] = 4 * k_peek * (G.PEEK_PAD["len"] * 3.0 * 1e-6) * (Ta - Tc) / (gap * 1e-3)
    q["card_laminate_and_bridges"] = k_coc * (50e-3 * 0.715e-3 + 2 * 3e-3 * 5.5e-3) * (Ta - Tc) / 4e-3
    q["card_L3_lateral_from_warm_y_strips"] = k_coc * (2 * Lx * 5.5e-3) * (Ta - Tc) / (gap * 1e-3 + 1e-3)
    q["card_top_via_PEEK_lid_plate"] = k_peek * (20e-3 * 50e-3) * (Ta - Tc) / 10e-3
    q["foam_shell"] = k_foam * 6.0e-3 * (Ta - Tc) / (G.FOAM_T * 1e-3)   # area 6e-3 m2 [assessment, Rev B estimate kept]
    q["P_cf_line_and_fill"] = 0.05
    Q = sum(q.values())
    Qd = 1.5 * Q
    # TEC model from the datasheet maxima (revised after review: 07111-5L31-03CL, Th = 27 degC curves, PDF opened)
    Imax, Vmax, DTmax, Thr = 3.0, 8.6, 68.0, 300.15
    S = Vmax / Thr
    R = Vmax * (Thr - DTmax) / (Imax * Thr)
    K = Imax * Vmax * (Thr - DTmax) / (2 * Thr * DTmax)
    Th = 273.15 + 35.0
    Tcold = 273.15 + 3.0          # cold face 2 K below the plate set point 5 degC [assessment]
    dT = Th - Tcold
    best = None
    for I_ in np.arange(0.05, Imax, 0.01):
        Qc = S * I_ * Tcold - 0.5 * I_ ** 2 * R - K * dT
        if Qc >= Qd:
            V = S * dT + I_ * R
            best = (round(float(I_), 2), round(float(V), 2), round(float(V * I_), 2), round(float(Qc), 2))
            break
    Qh = Qd + best[2]

    # self-consistent hot side for a given sink resistance (air 25 / 30 degC): Th = Ta + R * (Qd + P_el)
    def op(R_sink, T_air):
        Th_ = T_air + 10.0
        for _ in range(200):
            dT_ = Th_ - Tcold
            sol = None
            for I_ in np.arange(0.02, Imax, 0.005):
                if S * I_ * Tcold - 0.5 * I_ ** 2 * R - K * dT_ >= Qd:
                    sol = I_
                    break
            if sol is None:
                return None
            V_ = S * dT_ + sol * R
            Th_new = T_air + R_sink * (Qd + V_ * sol)
            if abs(Th_new - (Th_ - 273.15 if Th_ > 200 else Th_)) < 0.01:
                break
            Th_ = Th_new
        return {"R_sink": R_sink, "T_air": T_air, "Th_C": round(Th_new, 1), "I_A": round(float(sol), 2),
                "P_el_W": round(float(V_ * sol), 2), "Q_hot_W": round(float(Qd + V_ * sol), 2)}

    def op_k(R_sink, T_air):
        # same in kelvin bookkeeping
        Th_ = T_air + 273.15 + 10.0
        res = None
        for _ in range(300):
            dT_ = Th_ - Tcold
            sol = None
            for I_ in np.arange(0.02, Imax, 0.005):
                if S * I_ * Tcold - 0.5 * I_ ** 2 * R - K * dT_ >= Qd:
                    sol = I_
                    break
            if sol is None:
                return {"R_sink": R_sink, "T_air": T_air, "result": "TEC cannot reach the load (runaway)"}
            V_ = S * dT_ + sol * R
            Th_new = T_air + 273.15 + R_sink * (Qd + V_ * sol)
            res = {"R_sink_K_per_W": R_sink, "T_air_C": T_air, "Th_C": round(float(Th_new) - 273.15, 1), "I_A": round(float(sol), 2),
                   "P_el_W": round(float(V_ * sol), 2), "Q_hot_W": round(float(Qd + V_ * sol), 2)}
            if abs(Th_new - Th_) < 0.01:
                return res
            Th_ = 0.5 * (Th_ + Th_new)
        return res
    sweep = [op_k(Rs, Ta_) for Rs in (1.0, 1.2, 1.4, 1.6, 2.0) for Ta_ in (25.0, 30.0)]
    return {"loads_W": {k: round(v, 3) for k, v in q.items()}, "Q_total_W": round(Q, 2), "Q_design_x1.5_W": round(Qd, 2),
            "sink_sweep_self_consistent": sweep,
            "acceptance": "Th <= 50 degC and I <= 0.6 Imax at T_air 30 degC [assessment] -> R_sink <= 1.6 K/W (Q_hot <= 12.3 W)",
            "TEC_S_V_per_K": round(S, 4), "TEC_R_ohm": round(R, 2), "TEC_K_W_per_K": round(K, 3),
            "operating_point_[I A, V, P_el W, Qc W] at Th 35 / Tc 3 degC": best,
            "Q_hot_W": round(Qh, 2), "heatsink_Rth_required_K_per_W (Th - 25 degC air)": round((35.0 - 25.0) / Qh, 2),
            "anvil_heater_loss_to_cold_zone_W": round(q["gap_W_S_N_lip_plus_foam"] + q["break_E_lip_plus_foam"] + q["PEEK_pads_4x"], 2),
            "RevB_recomputed_W": {"y_walls": round(2 * k_peek * (18.4e-3 * 15e-3) * (Ta - Tc) / 1e-3, 2),
                                  "minus_x_wall": round(k_peek * (46e-3 * 15e-3) * (Ta - Tc) / 1e-3, 2),
                                  "break": round(k_peek * (46e-3 * 15e-3) * (Ta - Tc) / 4e-3, 2)}}


def dewpoint(T, RH):
    a, b = 17.62, 243.12   # Magnus constants (docs/13 §6.6 Magnus approximation; constants UNVERIFIED)
    g = math.log(RH / 100) + a * T / (b + T)
    return b * g / (a - g)


def dew():
    out = {}
    for T, RH in ((22, 50), (25, 60), (22, 70)):
        out[f"{T}C_{RH}%"] = round(dewpoint(T, RH), 1)
    return out


# ------------------------------------------------------------------------------------------------ motion
def motion():
    v_g, v_d, v_t = I.MAGNETS["M_d"]["speeds"]["gather"], I.MAGNETS["M_d"]["speeds"]["drag"], \
        I.MAGNETS["M_d"]["speeds"]["transit_max"]
    t_cam = 0.5   # s per 8 mm cam stroke [assessment, motor UNVERIFIED]

    def L(p):
        return sum(math.dist(p[i], p[i + 1]) for i in range(len(p) - 1))
    passes = [L(G.GATHER[("IC1", k)]) for k in ("pass1", "pass2", "pass3")]
    ret = [math.dist(G.GATHER[("IC1", "pass1")][1], G.GATHER[("IC1", "pass2")][0]),
           math.dist(G.GATHER[("IC1", "pass2")][1], G.GATHER[("IC1", "pass3")][0])]
    t_tr = L(G.TRANSIT_LOWERED["park_to_IC1"]) / v_t
    t_gather = t_tr + t_cam + sum(passes) / v_g + sum(r / v_t for r in ret) + 4 * t_cam
    drag = L(I.DRAG_PATH["IC1"])
    bo = L(I.BEAD_OUT_PATH)
    mc_t = 5.0
    rows = [
        ("M_c up (30.0-30.1)", mc_t, 6.0),
        ("M_c park (34.1-34.2)", mc_t, 6.0),
        ("M_d park -> gather start, 3 passes, returns (34.2-36.2)", t_gather, 120.0),
        ("drag 23.41 mm at 0.20 mm/s + 2 gate actuations (39.5-41.75)", drag / v_d + 0.4, 135.0),
        # (revised after review, docs/24 M7) incl. G4 opening (0.06 s, docs/20 §4.3) and the M_d Z-down cam stroke
        # at the end (0.5 s [assessment]) inside the 24-s window: 23.3 s, 0.7 s left
        ("bead-out 4.55 mm at 0.20 mm/s + G4 open 0.06 s + M_d Z-down 0.5 s (56.75-57.15)", bo / v_d + 0.06 + t_cam, 24.0),
        ("M_d down + transit to park after bead-out (57.15-57.65 flush, no conflict)",
         t_cam + L(G.TRANSIT_LOWERED["beadout_to_park"]) / v_t, 30.0),
        ("pogo lift (after the head is latched; once per card)", 0.5, None),
    ]
    return {"rows_[step, needed s, window s]": [(a, round(b, 1), c) for a, b, c in rows],
            "chord_error_0.5mm_segments_on_R3_um": round(0.5 ** 2 / (8 * 3.0) * 1e3, 1),
            "stage_repeatability_um": "< 3 (X-LSM050A) vs <= 10 required (docs/13 §6.2)",
            "speed_range": "0.000029-26 mm/s (X-LSM050A) covers 0.05-5 mm/s"}


def gap_budget():
    md = {"anvil top flatness (card datum)": 20, "X stage flatness of travel": 11, "Y stage flatness of travel": 11,
          "X pitch x 20 mm lever": 10, "Y roll x 20 mm lever": 10, "up-stop setting": 10, "magnet bond/face": 10}
    mc = {"anvil top flatness": 20, "plate thickness 5.000 (ground both faces)": 5, "holder flange-to-magnet-top 4.840": 10,
          "magnet face flatness after bonding": 5}
    rss = lambda d: round(math.sqrt(sum(v ** 2 for v in d.values())), 1)
    return {"M_d_um": md, "M_d_worst_um": sum(md.values()), "M_d_rss_um": rss(md),
            "M_c_um": mc, "M_c_worst_um": sum(mc.values()), "M_c_rss_um": rss(mc), "budget_um": 50}


def run():
    return {"plate": plate(), "seal": seal(), "thermal": thermal(), "dewpoint_C": dew(), "motion": motion(),
            "gap_budget": gap_budget(), "pogo": {"F_per_pin_N": round(G.POGO_F_WORK, 3),
                                                 "F_total_N": round(6 * G.POGO_F_WORK, 2),
                                                 "budget_N": 9.0, "press_pad_N": I.DIE_PRESS_PAD["force_N"],
                                                 "tip_retracted_z": G.POGO_TIP_Z_RETRACTED},
            "magnetics": magnetics()}


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=1))
