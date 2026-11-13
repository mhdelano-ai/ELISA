"""DOCK UPPER calculations: springs, cylinder forces, pneumatic timing and air, clamp, cam, thermal (docs/20 §4).

Pure functions; `report()` returns a dict and a printable text. Inputs from params.py / interface.py only.
Material constants are handbook values marked UNVERIFIED in params.py.
"""
from __future__ import annotations

import math

from elisa_cad import interface as IF
from elisa_cad.dock_upper import params as P

P_ATM = 101.325  # kPa
R_AIR, T_K = 287.0, 296.0


# ------------------------------------------------------------------------------------------------ springs
def spring(d, Dm, n, G=P.SPRING_G):
    k = G * d ** 4 / (8.0 * Dm ** 3 * n)                     # N/mm
    C = Dm / d
    wahl = (4 * C - 1) / (4 * C - 4) + 0.615 / C
    return k, C, wahl


def tau(F, d, Dm, wahl):
    return wahl * 8.0 * F * Dm / (math.pi * d ** 3)          # MPa


def pin_springs():
    L_closed = P.SPRING_PLATE_Z[0] - P.COLLAR_Z_CLOSED[1]    # 24.5 - 16.915 = 7.585
    out = {}
    for cls, s in P.PIN_SPRINGS.items():
        k, C, w = spring(s["d"], s["Dm"], s["n"])
        F0 = s["F_closed"]
        F_open = F0 + k * P.STROKE
        F_nocard = F0 - k * P.DROP_BELOW_CLOSED
        L_solid = (s["n"] + 2) * s["d"]
        L_free = L_closed + F0 / k
        out[cls] = dict(k=k, C=C, F_closed=F0, F_closed_range=(F0 * (1 - P.SPRING_TOL), F0 * (1 + P.SPRING_TOL)),
                        F_open=F_open, F_open_max=F_open * (1 + P.SPRING_TOL), F_nocard=F_nocard,
                        L_closed=L_closed, L_open=L_closed - P.STROKE, L_free=L_free, L_solid=L_solid,
                        solid_margin=L_closed - P.STROKE - L_solid, OD=s["Dm"] + s["d"], ID=s["Dm"] - s["d"],
                        tau_open=tau(F_open * (1 + P.SPRING_TOL), s["d"], s["Dm"], w),
                        dF_per_0p06=k * 0.06)
    return out


# ------------------------------------------------------------------------------------------------ cylinders
def cylinder_forces(p_kpa=P.P_SUPPLY_KPA, mu_rod=0.15, f_oring=0.7, f_pin_guide=0.05, guide_span=8.0):
    """Pull cylinders (annulus under the piston) lift pin + spring; V3 push cylinder closes through a limit spring.
    Friction: pin guide 0.05 N [assessment]; piston O-ring 0.6 N UNVERIFIED (small O-ring at 0.4 MPa);
    rod side load from the blade couple F*L reacted over guide_span 8 mm, mu 0.15 (bronze/steel) [assessment]."""
    A_pull = math.pi / 4 * (P.BORE_D ** 2 - P.ROD_D ** 2)
    A_push = math.pi / 4 * P.BORE_D ** 2
    sp = pin_springs()
    rows = []
    for vid, c in IF.CYLINDERS.items():
        v = IF.VALVES[vid]
        L = math.dist(v.xy, c["xy"])
        if vid == "V3":
            F_lim_end = P.V3["limit_spring_preload"] + P.V3["limit_spring_rate"] * P.V3["overtravel"]
            need = F_lim_end + P.RETURN_SPRING_F + f_oring
            F_cyl = p_kpa * 1e-3 * A_push
            k_o = spring(P.V3["open_spring"]["d"], P.V3["open_spring"]["Dm"], P.V3["open_spring"]["n"])[0]
            F_open_closed = P.V3["open_spring"]["F_open"] + k_o * P.STROKE
            F_tpe = F_lim_end - F_open_closed - f_pin_guide
            rows.append(dict(id=vid, L=L, F_cyl=F_cyl, need=need, margin=F_cyl / need, F_tpe=F_tpe,
                             F_tpe_range=(F_lim_end * 0.9 - F_open_closed - f_pin_guide,
                                          F_lim_end * 1.1 - F_open_closed + f_pin_guide)))
            continue
        cls = P.valve_class(v)
        Fs = sp[cls]["F_open_max"]
        f_couple = mu_rod * 2 * Fs * L / guide_span
        need = Fs + f_couple + f_oring + f_pin_guide + P.RETURN_SPRING_F
        F_cyl = p_kpa * 1e-3 * A_pull
        rows.append(dict(id=vid, L=L, F_cyl=F_cyl, need=need, margin=F_cyl / need,
                         F_tpe_range=(sp[cls]["F_closed_range"][0] - f_pin_guide,
                                      sp[cls]["F_closed_range"][1] + f_pin_guide), F_max=v.f_close_max))
    return dict(A_pull=A_pull, A_push=A_push, rows=rows, worst=min(rows, key=lambda r: r["margin"]))


# ------------------------------------------------------------------------------------------------ pneumatics
def orifice_mdot(p_up, p_dn, A_m2, Cd=0.8):
    """Isentropic orifice mass flow (kg/s), pressures kPa abs."""
    g = 1.4
    pu, pd = p_up * 1e3, p_dn * 1e3
    r = pd / pu
    rc = (2 / (g + 1)) ** (g / (g - 1))
    if r <= rc:
        return Cd * A_m2 * pu * math.sqrt(g / (R_AIR * T_K)) * (2 / (g + 1)) ** ((g + 1) / (2 * (g - 1)))
    return Cd * A_m2 * pu * math.sqrt(2 * g / ((g - 1) * R_AIR * T_K) * (r ** (2 / g) - r ** ((g + 1) / g)))


def chamber_volume_mm3(L_gallery=70.0):
    gallery = P.GALLERY_W ** 2 * L_gallery
    adapter = 15.0                                   # manifold adapter passage [assessment]
    valve_out = 10.0                                 # S070 OUT passage [assessment, UNVERIFIED]
    dead = math.pi / 4 * (P.BORE_D ** 2 - P.ROD_D ** 2) * 0.5   # 0.5 mm end clearance
    swept = math.pi / 4 * (P.BORE_D ** 2 - P.ROD_D ** 2) * P.PULL_STROKE
    return dict(gallery=gallery, adapter=adapter, valve=valve_out, dead=dead, swept=swept,
                total=gallery + adapter + valve_out + dead + swept)


def actuation_times(p_kpa=P.P_SUPPLY_KPA, orifice_d=0.15, dt=1e-5):
    """Fill/exhaust of one pull-cylinder chamber through a per-channel orifice (the S070 C = 0.042 dm3/(s bar) is
    ~10x larger and is neglected). Isothermal tank; motion threshold: p*A = spring force (+/- friction)."""
    vol = chamber_volume_mm3()
    V = vol["total"] * 1e-9
    A_or = math.pi / 4 * (orifice_d * 1e-3) ** 2
    A_pull = math.pi / 4 * (P.BORE_D ** 2 - P.ROD_D ** 2)
    sp = pin_springs()
    res = {}
    for cls in ("slot", "anvil12"):
        F_lift = sp[cls]["F_open"] + 1.2 + P.RETURN_SPRING_F      # spring + friction ~1.2 N + return
        p_lift = P_ATM + F_lift / A_pull * 1e3                     # kPa abs to start lifting
        F_drop = sp[cls]["F_closed"] - 1.2 + P.RETURN_SPRING_F
        p_drop = P_ATM + max(F_drop, 0.1) / A_pull * 1e3
        ps = P_ATM + p_kpa
        # fill
        p, t, t_lift = P_ATM, 0.0, None
        while p < 0.98 * ps and t < 1.0:
            m = orifice_mdot(ps, p, A_or)
            p += m * R_AIR * T_K / V * dt * 1e-3
            t += dt
            if t_lift is None and p >= p_lift:
                t_lift = t
        t_fill = t
        p, t, t_drop = ps, 0.0, None
        while p > P_ATM * 1.02 and t < 1.0:
            m = orifice_mdot(p, P_ATM, A_or)
            p -= m * R_AIR * T_K / V * dt * 1e-3
            t += dt
            if t_drop is None and p <= p_drop:
                t_drop = t
        res[cls] = dict(p_lift_kPa_abs=p_lift, p_drop_kPa_abs=p_drop, t_valve_ms=P.PILOT["t_on_ms"],
                        t_start_lift_ms=t_lift * 1e3, t_fill98_ms=t_fill * 1e3, t_start_close_ms=t_drop * 1e3,
                        t_exhaust_ms=t * 1e3,
                        t_open_total_ms=(t_lift + 0.5 * (t_fill - t_lift)) * 1e3 + P.PILOT["t_on_ms"],
                        t_close_total_ms=t * 1e3 + P.PILOT["t_off_ms"])
    return dict(volume_mm3=vol, orifice_d=orifice_d, by_class=res)


def air_consumption(p_kpa=P.P_SUPPLY_KPA, runs_per_day=16):
    vol = chamber_volume_mm3()["total"]
    per_act = vol * (p_kpa / P_ATM)                        # mm3 free air (ANR) per actuation (Derived)
    acts_per_run = 16 + 1                                   # docs/13 §4: 16 cycles per run (+V3)
    per_run = per_act * acts_per_run
    return dict(per_actuation_Nml=per_act * 1e-3, per_run_Nml=per_run * 1e-3,
                per_day_Nl=per_run * runs_per_day * 1e-6, docking_all21_Nml=21 * per_act * 1e-3)


def pilot_heat():
    """Energised valve-minutes per run from docs/13 §4 'open during' (min); V3 energised when CLOSED."""
    open_min = {"V1/V2": 6.8, "V4/V5": 1.0, "V6/V7": 0.5, "V8": 0.5, "V9/V10": 46.45, "V11": 0.6, "V12": 0.3,
                "V15": 0.5, "V16": 0.5, "V17/V18": 7.05 + 13.65, "G1/G2": 2.55, "G3": 2.2, "G4": 0.9}
    s = sum(open_min.values())
    run_period = 60.0                                        # [assessment] per-run slot length incl. stagger
    avg_valves = s / run_period + (1 - 6.8 / run_period)     # + V3 (energised = closed)
    return dict(valve_min_per_run=s, avg_energised=avg_valves, avg_W=avg_valves * P.PILOT["P_W"],
                peak_W=6 * P.PILOT["P_W"])


# ------------------------------------------------------------------------------------------------ clamp + cam
def clamp():
    cs = P.CLAMP_SPRING
    F_side = cs["preload"] + cs["rate"] * cs["overtravel"]
    F_head = 2 * F_side - P.HEAD_RETURN_SPRINGS_N
    springs_up = sum(pin_springs()[P.valve_class(v)]["F_closed"] for v in IF.VALVES.values() if v.id != "V3")
    v3 = P.V3["limit_spring_preload"] + P.V3["limit_spring_rate"] * P.V3["overtravel"]
    reactions = springs_up + v3 + P.PAD["force_N"] + 2 * P.GAS["force_N"]
    card_face = F_head - reactions
    b_hi, b_lo = IF.clamp_budget(), IF.clamp_budget(seal_force=3.0)
    dF = 2 * cs["rate"] * 0.5                                # +-0.5 mm frame/card stack
    # cam torque: s(th) = e (1 - cos th); head contact at s = 8; force = return springs before, ramps after
    e = P.CAM["e"]
    tmax, th_max = 0.0, 0.0
    for i in range(1, 1800):
        th = math.radians(i / 10)
        s = e * (1 - math.cos(th))
        F = (P.HEAD_RETURN_SPRINGS_N if s < HEAD_CONTACT_S else
             2 * (cs["preload"] + cs["rate"] * (s - HEAD_CONTACT_S)))
        T = F * e * math.sin(th) * 1e-3 + 0.1 * F * 4.0e-3   # N m; + journal friction mu 0.1 on r 4 [assessment]
        if T > tmax:
            tmax, th_max = T, math.degrees(th)
    lever = 60.0
    return dict(F_side=F_side, F_head=F_head, F_head_range=(F_head - dF, F_head + dF), reactions=reactions,
                card_face=card_face, card_face_min=card_face - dF, budget_card_min=(b_lo["card_clamp_min_N"],
                b_hi["card_clamp_min_N"]), budget_total=(b_lo["lid_latch_total_N"], b_hi["lid_latch_total_N"]),
                cam_stroke=2 * e, cam_Tmax_Nm=tmax, cam_th_deg=th_max, hand_force_N=tmax / (lever * 1e-3),
                latch_front_N=None)


HEAD_CONTACT_S = 8.0


def latch_reaction(F_head):
    """Lid-frame reactions: cam at dock Y 100 pushes the frame up; hinge Y 195, front draw latches Y ~36."""
    y_cam = IF.card_to_dock((0, P.CAM["y"]))[1]
    y_h, y_l = P.HINGE["point"][1], 36.0
    F_latch = F_head * (y_h - y_cam) / (y_h - y_l)
    return dict(F_latches_total=F_latch, F_hinge=F_head - F_latch, per_latch=F_latch / 2)


# ------------------------------------------------------------------------------------------------ thermal
def thermal():
    Lx = P.HB_X[1] - P.HB_X[0]
    Ly = P.HB_Y[1] - P.HB_Y[0]
    T = P.HB_Z1 - P.HB_Z0
    fin_area = 2 * (Lx - 0.6) * (P.HEATER_FIN["z"][1] - P.HEATER_FIN["z"][0])
    A_exposed = (Lx * Ly + 2 * Lx * T + 2 * Ly * T + 2 * fin_area) * 1e-6     # m2 (top, sides, fins both faces)
    G_conv = P.H_CONV * A_exposed
    n_so = len(P.STANDOFFS_HB)
    L_so = (P.CYL_Z0 - P.HB_Z1) * 1e-3
    G_so = n_so * P.K_PEEK * math.pi / 4 * (P.STANDOFF_D * 1e-3) ** 2 / L_so
    G_pins = 21 * 15.0 * math.pi / 4 * (0.5e-3) ** 2 / 10e-3                    # stainless necks, 10 mm [assessment]
    G = G_conv + G_so + G_pins
    dT_worst = P.T_SET - P.T_AMB[0]
    P_loss = G * dT_worst
    vol = Lx * Ly * T + 2 * (Lx - 0.6) * P.HEATER_FIN["t"] * (P.HEATER_FIN["z"][1] - P.HEATER_FIN["z"][0])
    m = vol * P.RHO_AL
    C = m * P.CP_AL
    P_max = P.HEATER["n"] * P.HEATER["V_drive_max"] ** 2 / P.HEATER["R_ohm"]
    t_warm = C * dT_worst / (P_max - P_loss / 2)
    # in-plane gradient: heat enters at the two y fins, losses distributed: dT = P L / (8 k A)
    A_cross = Lx * T * 1e-6
    dT_grad = P_loss * (Ly * 1e-3) / (8 * P.K_AL * A_cross)
    # pilot-valve disturbance through standoffs and pins: cylinder block rise ~ P_pilot / (h A_cyl)
    A_cyl = 2 * (95.5 * 50 + 95.5 * 30 + 50 * 30) * 1e-6
    ph = pilot_heat()
    dT_cyl = ph["avg_W"] / (P.H_CONV * A_cyl)
    P_dist = (G_so + G_pins) * dT_cyl
    return dict(A_exposed_m2=A_exposed, G_W_per_K=G, G_conv=G_conv, G_standoffs=G_so, G_pins=G_pins,
                P_loss_worst_W=P_loss, P_heater_max_W=P_max, mass_g=m, C_J_per_K=C, t_warmup_s=t_warm,
                tau_passive_s=C / G, dT_gradient_K=dT_grad, dT_cylblock_K=dT_cyl, P_disturbance_W=P_dist)


def report():
    sp = pin_springs()
    cyl300 = cylinder_forces(300.0)
    cyl = cylinder_forces()
    act = actuation_times()
    air = air_consumption()
    ph = pilot_heat()
    cl = clamp()
    lr = latch_reaction(cl["F_head_range"][1])
    th = thermal()
    lines = ["== pin springs (k N/mm, F N, L mm, tau MPa) =="]
    for c, s in sp.items():
        lines.append(f"{c:8s} k={s['k']:.3f} C={s['C']:.1f} F_closed={s['F_closed']:.2f} "
                     f"[{s['F_closed_range'][0]:.2f}-{s['F_closed_range'][1]:.2f}] F_open={s['F_open']:.2f} "
                     f"F_nocard={s['F_nocard']:.2f} L_free={s['L_free']:.2f} L_closed={s['L_closed']:.2f} "
                     f"L_solid={s['L_solid']:.2f} solid_margin={s['solid_margin']:.2f} OD={s['OD']:.2f} "
                     f"tau_open_max={s['tau_open']:.0f} dF(0.06 stack)={s['dF_per_0p06']:.3f}")
    for name, cc in (("300 kPa", cyl300), (f"{P.P_SUPPLY_KPA:.0f} kPa", cyl)):
        lines.append(f"== cylinders at {name}: A_pull={cc['A_pull']:.2f} mm2 A_push={cc['A_push']:.2f} ==")
        for r in cc["rows"]:
            lines.append(f"{r['id']:4s} L={r['L']:5.2f} F_cyl={r['F_cyl']:.2f} need={r['need']:.2f} "
                         f"margin={r['margin']:.2f} F_tpe={r['F_tpe_range'][0]:.2f}-{r['F_tpe_range'][1]:.2f}")
        lines.append(f"worst: {cc['worst']['id']} margin {cc['worst']['margin']:.2f}")
    lines.append(f"== actuation (orifice {act['orifice_d']} mm) volume {act['volume_mm3']} ==")
    for c, r in act["by_class"].items():
        lines.append(f"{c}: " + ", ".join(f"{k}={v:.1f}" for k, v in r.items()))
    lines.append("== air == " + ", ".join(f"{k}={v:.3f}" for k, v in air.items()))
    lines.append("== pilot heat == " + ", ".join(f"{k}={v:.2f}" for k, v in ph.items()))
    lines.append("== clamp == " + ", ".join(f"{k}={v}" for k, v in cl.items()))
    lines.append("== lid reactions (at F_head max) == " + ", ".join(f"{k}={v:.1f}" for k, v in lr.items()))
    lines.append("== thermal == " + ", ".join(f"{k}={v:.4g}" for k, v in th.items()))
    return dict(springs=sp, cyl300=cyl300, cyl=cyl, act=act, air=air, pilot=ph, clamp=cl, latch=lr,
                thermal=th), "\n".join(lines)


if __name__ == "__main__":
    print(report()[1])
