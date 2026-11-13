"""Tubing schedule of the DOCK BASE: every liquid line to the 11 card liquid ports, the 2 gas ports, supply, waste,
air and cell-lead routes. Each route is a Manhattan polyline of waypoints in dock coords (mm); lengths come from
these polylines (= the CAD routing). Segments inside the LOWER claim (gland -> pass-through -> card port) are
ESTIMATED as Manhattan distances (owner DOCK LOWER) and reported separately; they are not built as solids here."""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from .. import interface as I
from . import layout as L
from . import params as P

IN = 25.4
TUBES = {  # name: (material, ID mm, OD mm, source)
    "PEEK_0.127": ("PEEK", 0.005 * IN, 1 / 16 * IN, "docs/13 §2.5; params/hardware.yaml (0.005 in PEEK)"),
    "PEEK_0.102": ("PEEK", 0.004 * IN, 1 / 16 * IN, "CHOICE-B11 (bead line, keeps <= 2.5 uL)"),
    "PEEK_0.25": ("PEEK", 0.010 * IN, 1 / 16 * IN, "[assessment] clean A1 lines"),
    "FEP_0.25": ("FEP", 0.010 * IN, 1 / 16 * IN, "[assessment] reagent fill lines (low hold-up)"),
    "FEP_0.5": ("FEP", 0.020 * IN, 1 / 16 * IN, "docs/13 §3.2.2, §5.1 (0.5 mm FEP coils)"),
    "FEP_0.75": ("FEP", 0.030 * IN, 1 / 16 * IN, "[assessment] waste/supply, low resistance"),
    "PTFE_gas": ("PTFE", 1 / 16 * IN, 1 / 8 * IN, "[assessment] gas lines 1/8 x 1/16 in"),
    "PU_6x4": ("PU", 4.0, 6.0, "[assessment] lab-air supply"),
    "PU_4x2.5": ("PU", 2.5, 4.0, "[assessment] lid pilot supply 300 kPa"),
    "shield_lead": ("shielded coax", 0.0, 3.0, "docs/13 §6.3"),
}

PW = I.PASS_THROUGHS["liquid_lines_west"]["dock"]   # (212, 100, 110)
PE = I.PASS_THROUGHS["liquid_lines_east"]["dock"]   # (265, 100, 110)
GW_X, GE_X = P.GLAND_W["x"], P.GLAND_E["x"]
UMB = I.PASS_THROUGHS["lid_umbilical"]["dock"]      # (235, 200, 190)
UMB_GROMMET = (249.0, 208.0, 180.0)                 # IR-4: hand-over point in the rear-low cover (DOCK BASE side)


def port_dock(pid):
    return I.card_to_dock(I.PORTS[pid].xy)


# gland entry points (IR-2): west wall X 150, east wall X 320; every line has its own Y (no crossings)
GW = {"P_b": (96, 120), "P_byp": (100, 104), "P_cf": (104, 120), "P_in": (112, 120), "P_a": (116, 104),
      "P_d1": (120, 120), "P_d2": (124, 112)}
GE = {"P_s": (78, 110.75), "P_a2": (70, 122), "P_wo": (86, 112), "P_rf": (64, 118)}
LANE_Y = 316.5        # pump lines descend between the well rear wall (Y 312-314) and the pump spine (Y 319)
Z_LANE = {"P_a": 156.0, "gas_conj": 162.0, "P_d2": 167.0, "P_d1": 170.0, "S_b": 173.0}   # west lanes at Y 203


def gw(pid):
    y, z = GW[pid]
    return (GW_X, float(y), float(z))


def ge(pid):
    y, z = GE[pid]
    return (GE_X, float(y), float(z))


def pump_port(pump, k=0):
    """Valve ports on the pump front face: k = 0 card line, +1 A1 in, -1 waste, +2 second card line (S_A)."""
    x = L.PUMP_X[pump] + 6.0 * k
    return (x, P.PUMP_BODY_Y[1] + P.PUMP_FRONT_ZONE, P.PUMP_SHELF_Z[1] + P.CENTRIS["H"] - 12.0)


def pump_head(pump, k, z_lane):
    """Pump valve -> up to Z 232 -> forward over the pump bodies to LANE_Y -> down to the lane height."""
    p = pump_port(pump, k)
    return [p, (p[0], p[1], 232.0), (p[0], LANE_Y, 232.0), (p[0], LANE_Y, z_lane)]


def west_strip(pid, x_lane, z_lane, y_from=203.0):
    """From the Y 203 lane through the partition slot, down the cold-claim strip at x_lane to the gland."""
    y, z = GW[pid]
    return [(x_lane, y_from, z_lane), (x_lane, float(y), z_lane), (x_lane, float(y), float(z)), gw(pid)]


@dataclass
class Route:
    name: str
    tube: str
    pts: list
    frm: str
    to: str
    port: str = ""              # card port if any
    lower_est: float = 0.0      # LOWER-internal estimated length (mm)
    external: float = 0.0       # outside the dock (mm), e.g. SM-FL -> dock wall
    inline_uL: float = 0.0      # inline device volume added (sensor), uL
    assumed: str = ""           # what docs/13 assumes
    allowed: tuple = ()         # items the route may pass through (glands, walls, its own end devices)
    note: str = ""

    @property
    def length(self):
        return sum(math.dist(self.pts[i], self.pts[i + 1]) for i in range(len(self.pts) - 1))

    @property
    def total(self):
        return self.length + self.lower_est + self.external


def lower_estimate(g, pid):
    """Manhattan gland -> pass-through -> card port (owner DOCK LOWER; estimate)."""
    pt = PW if g[0] == GW_X else PE
    pd = port_dock(pid)
    d1 = sum(abs(a - b) for a, b in zip(g, pt))
    d2 = abs(pd[0] - pt[0]) + abs(pd[1] - pt[1]) + abs(pd[2] - pt[2])
    return d1 + d2


ROUTES: list[Route] = []


def R(*a, **k):
    r = Route(*a, **k)
    if r.port:
        g = gw(r.port) if r.port in GW else ge(r.port)
        r.lower_est = lower_estimate(g, r.port)
    ROUTES.append(r)
    return r


WALLS = ("partition_left", "partition_right", "panel_left", "panel_right", "panel_rear", "cold_box", "rear_low_cover",
         "drip_tray", "pump_back_plate")
iz0 = L.COLD_INNER[0][2]
# air-gap head nipples in one row at Y 258.5 (x, approach height): lines ending further west run higher (no crossing)
NIPPLES = {"P_wo": (365.0, 266.0), "P_byp": (371.0, 280.0), "S_b": (377.0, 278.0), "S_IC1": (383.0, 276.0),
           "S_IC2": (389.0, 274.0), "S_A": (395.0, 272.0), "S_RC": (401.0, 270.0)}
Y_HEAD = 258.5
Z_HEAD = 259.0


def to_head(key, xa, ya):
    xn, zh = NIPPLES[key]
    return [(xa, ya, zh), (xa, Y_HEAD, zh), (xn, Y_HEAD, zh), (xn, Y_HEAD, Z_HEAD)]


# ----------------------------------------------------------------------------------------------- card liquid lines
R("P_in (SM-FL -> card)", "PEEK_0.127",
  [(0.0, 110.0, 160.0), (4.0, 110.0, 160.0), (34.0, 110.0, 160.0), (138.0, 110.0, 160.0), (138.0, 112.0, 160.0),
   (138.0, 112.0, 120.0), gw("P_in")],
  "SM-FL outlet (via the P_in sensor)", "P_in", port="P_in", external=P.SMFL_OUTLET_TO_DOCK, inline_uL=1.0,
  assumed="docs/13 §2.6: PEEK 3.8 uL (0.3 m x 0.127 mm); >= 0.3 m isolation (docs/13 §2.5)",
  allowed=WALLS + ("P_in_pressure_sensor",), note="sensor swept volume <= 1 uL UNVERIFIED; external 0.2 m UNVERIFIED")
R("P_b (SV_b -> card)", "PEEK_0.102",
  [(140.0, 77.0, 177.0), (143.0, 77.0, 177.0), (143.0, 96.0, 177.0), (143.0, 96.0, 120.0), gw("P_b")],
  "SV_b port P_b", "P_b", port="P_b", assumed="docs/13 §5.1: outlet line 0.25 mm x 50 mm = 2.5 uL",
  allowed=WALLS + ("SV_b_selection_valve",))
R("P_cf (conjugate tube -> card)", "FEP_0.25",
  [(65.0, 100.0, iz0 + 45), (65.0, 103.0, iz0 + 45), (65.0, 103.0, 182.0), (135.0, 103.0, 182.0),
   (135.0, 104.0, 182.0), (135.0, 104.0, 120.0), gw("P_cf")],
  "conjugate tube (cold box)", "P_cf", port="P_cf", assumed="docs/13 §5.2: dead volume ~100 uL in the 0.26 mL fill",
  allowed=WALLS + ("conj_tube_2mL", "conj_holder_block"))
R("P_d1 coil (S_IC1 <-> card)", "FEP_0.5",
  pump_head("S_IC1", 0, Z_LANE["P_d1"]) + [(232.0, 203.0, Z_LANE["P_d1"])] + west_strip("P_d1", 126.0, Z_LANE["P_d1"]),
  "S_IC1 valve", "P_d1", port="P_d1", assumed="docs/13 §3.2.2: 60 uL FEP coil (>= 50 uL stroke + margin)",
  allowed=WALLS + ("S_IC1_valve_syringe",))
R("P_d2 coil (S_IC2 <-> card)", "FEP_0.5",
  pump_head("S_IC2", 0, Z_LANE["P_d2"]) + [(292.0, 203.0, Z_LANE["P_d2"])] + west_strip("P_d2", 129.0, Z_LANE["P_d2"]),
  "S_IC2 valve", "P_d2", port="P_d2", assumed="docs/13 §3.2.2: 60 uL FEP coil", allowed=WALLS + ("S_IC2_valve_syringe",))
R("P_a (S_A -> card, via FS1)", "PEEK_0.25",
  pump_head("S_A", 0, Z_LANE["P_a"]) + [(304.45, LANE_Y, Z_LANE["P_a"]), (304.45, 203.0, Z_LANE["P_a"])]
  + west_strip("P_a", 132.0, Z_LANE["P_a"]), "S_A valve port 1", "P_a", port="P_a", inline_uL=1.0,
  assumed="clean A1 (prime only)", allowed=WALLS + ("S_A_valve_syringe", "FS1_SLF3S_P_a"),
  note="FS1 internal volume UNVERIFIED (1 uL allowance)")
R("P_byp (card -> waste, air gap)", "FEP_0.75",
  [gw("P_byp"), (124.0, 100.0, 104.0), (124.0, 100.0, 24.0), (124.0, 140.0, 24.0), (441.5, 140.0, 24.0),
   (441.5, 230.0, 24.0)] + to_head("P_byp", 441.5, 230.0),
  "P_byp", "waste air-gap head", port="P_byp", assumed="waste (docs/13 §3.7)",
  allowed=WALLS + ("waste_airgap_head", "leak_electrode_1"))
R("P_s (card -> FS2 -> S_RC)", "PEEK_0.25",
  [ge("P_s"), (330.0, 78.0, 110.75), (330.0, LANE_Y, 110.75), (412.0, LANE_Y, 110.75), (412.0, LANE_Y, 232.0),
   (412.0, pump_port("S_RC")[1], 232.0), pump_port("S_RC")],
  "P_s", "S_RC valve (pull only)", port="P_s", inline_uL=1.0, assumed="product side, pulled to waste (no budget)",
  allowed=WALLS + ("FS2_P_s", "S_RC_valve_syringe"))
R("P_a2 (S_A -> card)", "PEEK_0.25",
  pump_head("S_A", 2, 122.0) + [(331.5, LANE_Y, 122.0), (331.5, 70.0, 122.0), ge("P_a2")],
  "S_A valve port 2", "P_a2", port="P_a2", assumed="clean A1 (DEV-6 of docs/18)", allowed=WALLS + ("S_A_valve_syringe",))
R("P_wo (card -> waste, air gap)", "FEP_0.75",
  [ge("P_wo"), (327.0, 86.0, 112.0), (327.0, 86.0, 30.0), (327.0, 290.0, 30.0)] + to_head("P_wo", 327.0, 290.0),
  "P_wo", "waste air-gap head", port="P_wo", assumed="waste", allowed=WALLS + ("waste_airgap_head",))
R("P_rf (HQDP tube -> card)", "FEP_0.25",
  [(443.0, 43.0, 147.0), (443.0, 43.0, 160.0), (443.0, 97.5, 160.0), (326.0, 97.5, 160.0), (326.0, 64.0, 160.0),
   (326.0, 64.0, 118.0), ge("P_rf")],
  "HQDP tube (dark sleeve)", "P_rf", port="P_rf", assumed="docs/13 §5.2: dead ~200 uL in the 0.6 mL fill",
  allowed=WALLS + ("HQDP_holder",))

# ----------------------------------------------------------------------------------------------- gas lines (2 ports)
R("P_c gas (Flow EZ ch1 -> umbilical)", "PTFE_gas",
  [(196.0, 240.0, 148.0), (196.0, 240.0, 154.0), (196.0, 208.0, 154.0), (240.0, 208.0, 154.0), (240.0, 208.0, 180.0)],
  "Flow EZ ch1", "lid umbilical -> P_c", assumed="gas, compliance only", allowed=WALLS + ("FEZ_ch1_P_c",),
  note="+ UPPER segment grommet -> (235,200,190) -> lid gas ring (owner DOCK UPPER)")
R("P_mv gas (ch2 -> 3/2 valve -> umbilical)", "PTFE_gas",
  [(252.0, 262.0, 175.0), (252.0, 262.0, 177.0), (252.0, 208.0, 177.0), (248.0, 208.0, 177.0), (248.0, 208.0, 180.0)],
  "switch valve 1 (fed by Flow EZ ch2 from below)", "lid umbilical -> P_mv", assumed="gas",
  allowed=WALLS + ("switch_valves_3x3-2",))
R("gas -> conjugate tube (fill)", "PTFE_gas",
  [(250.0, 262.0, 162.0), (246.0, 262.0, 162.0), (246.0, 203.0, 162.0), (118.0, 203.0, 162.0), (118.0, 130.0, 162.0),
   (118.0, 130.0, 168.0), (62.0, 130.0, 168.0), (62.0, 97.0, 168.0), (62.0, 97.0, iz0 + 45)],
  "switch valve 2", "conjugate tube cap", assumed="gas", allowed=WALLS + ("switch_valves_3x3-2", "conj_tube_2mL",
  "conj_holder_block"))
R("gas -> HQDP tube (fill)", "PTFE_gas",
  [(286.0, 271.0, 162.0), (326.0, 271.0, 162.0), (326.0, 271.0, 205.0), (326.0, 118.0, 205.0), (452.0, 118.0, 205.0),
   (452.0, 40.0, 205.0), (440.0, 40.0, 205.0), (440.0, 40.0, 147.0)],
  "switch valve 3", "HQDP tube cap", assumed="gas", allowed=WALLS + ("switch_valves_3x3-2", "HQDP_holder"))

# ----------------------------------------------------------------------------------------------- pump-side lines
R("S_b holding coil (S_b -> SV_b)", "FEP_0.5",
  pump_head("S_b", 0, Z_LANE["S_b"]) + [(172.0, 203.0, Z_LANE["S_b"]), (141.0, 203.0, Z_LANE["S_b"]),
                                        (141.0, 62.0, Z_LANE["S_b"]), (140.0, 62.0, Z_LANE["S_b"])],
  "S_b valve", "SV_b coil port", assumed="docs/13 §5.1: holding coil >= 40 uL (beads stay out of the syringe)",
  allowed=WALLS + ("S_b_valve_syringe", "SV_b_selection_valve"))
R("vial line (SV_b <-> bead vial)", "FEP_0.5",
  [(120.0, 70.0, 152.0), (120.0, 70.0, 140.0), (70.0, 70.0, 140.0), (70.0, 47.0, 140.0), (70.0, 47.0, iz0 + 75)],
  "SV_b vial port", "bead vial", assumed="returned to the vial before each dose (docs/13 §5.1)",
  allowed=WALLS + ("SV_b_selection_valve", "bead_vial_2mL"), note="flexible loop at the vial for the rocking")
for i, pmp in enumerate(P.PUMP_ORDER):
    pa, pw_ = pump_port(pmp, 1), pump_port(pmp, -1)
    za, zw = 240.0 + 2 * i, 252.0 + 2 * i
    R(f"A1 -> {pmp}", "FEP_0.75",
      [(380.0 - 8 * i, 146.0, 180.0), (380.0 - 8 * i, 150.0, 200.0 + 3 * i), (456.0 - 2 * i, 150.0, 200.0 + 3 * i),
       (456.0 - 2 * i, 317.0 + 2 * i, 200.0 + 3 * i), (456.0 - 2 * i, 317.0 + 2 * i, za),
       (pa[0], 317.0 + 2 * i, za), (pa[0], pa[1], za), pa], "A1 manifold", f"{pmp} valve A1 port", assumed="supply",
      allowed=WALLS + ("A1_manifold", f"{pmp}_valve_syringe"))
    R(f"{pmp} -> waste", "FEP_0.75",
      [pw_, (pw_[0], pw_[1], zw), (pw_[0], 405.0, zw), (440.0 - 2 * i, 405.0, zw)]
      + to_head(pmp, 440.0 - 2 * i, 405.0),
      f"{pmp} valve waste port", "waste air-gap head", assumed="waste",
      allowed=WALLS + (f"{pmp}_valve_syringe", "waste_airgap_head"))
R("A1 bottle -> manifold", "FEP_0.75",
  [(380.0, 53.0, 223.0), (380.0, 53.0, 228.0), (380.0, 134.0, 228.0), (380.0, 134.0, 190.0)],
  "A1 bottle cap", "A1 manifold", assumed="supply", allowed=WALLS + ("A1_cap", "A1_manifold", "A1_bottle_500mL"))

# ----------------------------------------------------------------------------------------------- air
R("lab air -> FR1", "PU_6x4",
  [(470.0, 380.0, 45.0), (452.0, 380.0, 45.0), (452.0, 195.0, 45.0), (360.0, 195.0, 45.0), (360.0, 190.0, 45.0)],
  "right-panel push-in (behind the Gamry)",
  "FR1", allowed=WALLS + ("FR1_filter_regulator",))
R("FR1 300 kPa -> lid pilots (umbilical)", "PU_4x2.5",
  [(360.0, 190.0, 160.0), (360.0, 196.0, 160.0), (328.0, 196.0, 160.0), (328.0, 196.0, 176.0), (328.0, 210.0, 176.0),
   (258.0, 210.0, 176.0), (258.0, 208.0, 176.0), (258.0, 208.0, 180.0)], "FR1", "umbilical grommet",
  allowed=WALLS + ("FR1_filter_regulator",))
R("R2 120 kPa -> Flow EZ supplies", "PU_4x2.5",
  [(405.0, 190.0, 80.0), (405.0, 195.0, 80.0), (333.0, 195.0, 80.0), (333.0, 310.0, 80.0), (196.0, 310.0, 80.0),
   (196.0, 310.0, 40.0), (196.0, 303.9, 40.0)], "R2", "Flow EZ supply (tee to both)",
  allowed=WALLS + ("R2_precision_reg", "FEZ_ch1_P_c"))
R("Flow EZ ch2 -> switch valves", "PTFE_gas", [(270.0, 262.0, 148.0), (270.0, 262.0, 150.0)], "Flow EZ ch2",
  "switch valve manifold", allowed=WALLS + ("FEZ_ch2_P_mv_bottles", "switch_valves_3x3-2"))
R("dry-air purge -> cold box", "FEP_0.75",
  [(412.0, 134.0, 150.0), (412.0, 134.0, 27.0), (412.0, 148.0, 27.0), (126.0, 148.0, 27.0), (126.0, 148.0, 100.0),
   (126.0, 120.0, 100.0), (110.0, 120.0, 100.0)], "purge restrictor", "cold box", allowed=WALLS + ("purge_restrictor",),
  note="gas, ~0.1 L/min dry air")

# ----------------------------------------------------------------------------------------------- cell leads
CELL = R("cell leads (bulkhead -> junction box)", "shield_lead",
         [P.BULKHEAD, (452.0, P.BULKHEAD[1], P.BULKHEAD[2])], "LOWER bulkhead", "junction box",
         assumed="docs/13 §6.3: <= 0.3 m", allowed=("gamry_lead_duct", "gamry_junction_box", "partition_right"))


def gamry_cable_length():
    g = L.get("Gamry_Ref600plus").box
    a = ((g[0][0] + g[1][0]) / 2, g[0][1], 100.0)
    b = (P.FX, P.BULKHEAD[1], P.BULKHEAD[2])
    return sum(abs(x - y) for x, y in zip(a, b))


# ----------------------------------------------------------------------------------------------- checks
def seg_hits_box(p, q, box, r):
    """Sample the segment every 0.5 mm; True if any sample lies inside box shrunk by 0.2 and grown by r."""
    (x0, y0, z0), (x1, y1, z1) = box
    n = max(2, int(math.dist(p, q) / 0.5) + 1)
    for k in range(n):
        t = k / (n - 1)
        x, y, z = (p[i] + t * (q[i] - p[i]) for i in range(3))
        if x0 - r + 0.2 < x < x1 + r - 0.2 and y0 - r + 0.2 < y < y1 + r - 0.2 and z0 - r + 0.2 < z < z1 + r - 0.2:
            return True
    return False


def route_collisions():
    out = []
    claims = {k: v["box"] for k, v in P.CL.items() if not k.startswith(("BASE", "BENCH"))}
    claims["loading_path"] = P.LOAD_BOX
    for r in ROUTES:
        rad = TUBES[r.tube][2] / 2
        for it in L.ITEMS:
            if it.name in r.allowed or it.group in ("bench",):
                continue
            for i in range(len(r.pts) - 1):
                if seg_hits_box(r.pts[i], r.pts[i + 1], it.box, rad):
                    out.append((r.name, it.name, i))
                    break
        for cn, cb in claims.items():
            for i in range(len(r.pts) - 1):
                # gland points sit ON the LOWER wall: allow the last/first 1 mm
                p, q = r.pts[i], r.pts[i + 1]
                if seg_hits_box(p, q, cb, rad - 1.0 if rad > 1.0 else 0.0):
                    if r.name.startswith("cell leads") and cn.startswith("LOWER"):
                        continue
                    out.append((r.name, cn, i))
                    break
    return out


def route_pair_clashes():
    """Tube-tube near misses (centre lines closer than the sum of radii), sampled."""
    import itertools
    import numpy as np
    samp = {}
    for r in ROUTES:
        pts = []
        for i in range(len(r.pts) - 1):
            p, q = np.array(r.pts[i]), np.array(r.pts[i + 1])
            n = max(2, int(np.linalg.norm(q - p) / 1.0) + 1)
            pts.append(p + np.linspace(0, 1, n)[:, None] * (q - p))
        samp[r.name] = np.vstack(pts)
    out = []
    for a, b in itertools.combinations(ROUTES, 2):
        A, B = samp[a.name], samp[b.name]
        d = np.min(np.linalg.norm(A[:, None, :] - B[None, :, :], axis=2))
        lim = (TUBES[a.tube][2] + TUBES[b.tube][2]) / 2
        if d < lim - 0.05:
            out.append((a.name, b.name, round(float(d), 2), round(lim, 2)))
    return out


def schedule_rows():
    rows = []
    for r in ROUTES:
        mat, idm, od, src = TUBES[r.tube]
        vb = math.pi / 4 * idm ** 2 * r.length          # mm^3 = uL
        vt = math.pi / 4 * idm ** 2 * r.total + r.inline_uL
        rows.append(dict(name=r.name, frm=r.frm, to=r.to, tube=f"{mat} {od:.2f} OD x {idm:.3f} ID" if idm else mat,
                         base_mm=round(r.length), lower_mm=round(r.lower_est), ext_mm=round(r.external),
                         total_mm=round(r.total), vol_base_uL=round(vb, 2) if idm else 0.0,
                         vol_total_uL=round(vt, 2) if idm else 0.0, assumed=r.assumed, note=r.note))
    return rows


def dp_kPa(r, Q_uL_min):
    """Hagen-Poiseuille over the whole line (Derived)."""
    idm = TUBES[r.tube][1] * 1e-3
    Lm = r.total * 1e-3
    Q = Q_uL_min * 1e-9 / 60.0
    return 128 * P.FLUID["eta"] * Lm * Q / (math.pi * idm ** 4) / 1000.0
