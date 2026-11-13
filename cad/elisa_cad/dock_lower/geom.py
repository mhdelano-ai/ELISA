"""DOCK LOWER geometry: every number of the lower bay, in CARD coordinates (docs/18 §2; z = 0 = anvil top = datum C,
z < 0 below the anvil). Interface numbers are IMPORTED from interface.py (never retyped). Numbers defined here carry a
source tag: docs §, Derived (arithmetic shown), CHOICE-Ln / DEV-Ln (docs/21 §7/§8), [assessment] or UNVERIFIED.
Pure module: no CAD calls, no side effects."""
from __future__ import annotations

import math

from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

from .. import interface as I

# =====================================================================================================
# 0. Helpers
# =====================================================================================================


def rrect(cx, cy, sx, sy, r):
    """Rounded rectangle polygon (corner radius r)."""
    return box(cx - sx / 2 + r, cy - sy / 2 + r, cx + sx / 2 - r, cy + sy / 2 - r).buffer(r, quad_segs=8)


def mirror_y(p):
    """Mirror a card point about the card mid-line y = 25 (IC1 <-> IC2 symmetric, docs/13 §2.2)."""
    return (p[0], I.CARD_W - p[1]) + tuple(p[2:])


# =====================================================================================================
# 1. Anvil plate (Al, heated 25.0 degC) -- CHOICE-5 (interface), CHOICE-L1..L3 (here)
# =====================================================================================================
ANVIL_X = (-15.0, 91.0)        # CHOICE-L1; (revised at integration, docs/23 I-1): -12/90 -> -15/91 so the head guide
#                                bushes at interface.HEAD_GUIDE_PINS keep a 2-mm anvil wall (was 0 at x -12)
ANVIL_Y = (-16.0, 66.0)        # CHOICE-L1: card +16 S / +16 N: datum A pins, pusher A, gutter, bushes
ANVIL_T = 15.0                 # interface ANVIL_THICK_ZONES t = 15.0
T_THIN = I.ANVIL_TOP_PLATE_T_THIN   # 5.0 (CHOICE-5)
Z_THIN_BOTTOM = -T_THIN               # -5.0: underside of the thin plate = hard-stop face of the M_c flanges
# cold-zone cut-out in the anvil (holds the PEEK break frame + cold plate; CHOICE-7 / CHOICE-L4)
COLD_CUTOUT = {"x": (0.6, I.X_BREAK[1]), "y": (1.0, I.CARD_W - 1.0)}    # x 0.6-24, y 1-49 [assessment]
COLD_PLATE = {"x": (1.6, I.X_BREAK[0]), "y": (2.0, I.CARD_W - 2.0)}     # Al top x 1.6-20, y 2-48 (Derived: 1 mm PEEK)
PEEK_GAP = 1.0                                                          # PEEK wall between cold plate and anvil, W/S/N
# bottom pocket (thin plate region over the magnet bay). Interface: thin plate over x 31-64; thick zones as
# I.ANVIL_THICK_ZONES. Local changes (DEV-L3): island boss extended to x 40.5 (P_b bore wall was 0.35 mm),
# P_s boss added at x 60.3-62.5 (P_s bore D3.3 reaches x 61.35 < 62.5), west strip narrowed to x 32.5 at the windows
# (M_c flange 12.6 wide must clear it).
POCKET_RECT = (32.5, 0.0, 62.5, I.CARD_W)
def _tz(k):
    z = I.ANVIL_THICK_ZONES[k]
    return (z["x"][0], z["y"][0], z["x"][1], z["y"][1])


ISLAND_BOSS = _tz("island_boss")                          # DEV-L3, in interface Rev B (24-40.5 x 19-31)
P_A2_BOSS = _tz("P_a2_boss")
P_S_BOSS = _tz("P_s_boss")                                # DEV-L3, interface Rev B: bore D3.3 at (63, 20.5) + 1.0 wall
POCKET_CORNER_R = 1.0                                     # end-mill D2 [assessment]


def pocket_poly():
    p = box(*POCKET_RECT)
    for b in (ISLAND_BOSS, P_A2_BOSS, P_S_BOSS):
        p = p.difference(box(*b))
    # end-mill corner radius on the pocket's convex corners
    return p.buffer(-POCKET_CORNER_R, join_style=1).buffer(POCKET_CORNER_R, join_style=1)


def window_poly(c):
    h, r = I.WINDOW_SIZE / 2, I.WINDOW_CORNER_R
    return box(c[0] - h + r, c[1] - h + r, c[0] + h - r, c[1] + h - r).buffer(r, quad_segs=8)


SLOT_HOLDER_CLEAR = I.SLOT_HOLDER_CLEAR   # DEV-L4, in interface Rev B (0.30)


def slot_poly_interface():
    """Drag slot exactly as interface.py defines it (union of round-capped buffers)."""
    return unary_union([LineString(v).buffer(I.SLOT_WIDTHS[k] / 2, quad_segs=16)
                        for k, v in I.SLOT_CENTERLINES.items()])


def holder_sweep(path, clear=SLOT_HOLDER_CLEAR, step=0.1):
    h = I.MAGNETS["M_d"]["holder"][0] / 2 + clear
    ls = LineString(path)
    n = max(2, int(ls.length / step) + 1)
    sq = [box(p[0] - h, p[1] - h, p[0] + h, p[1] + h) for p in
          (ls.interpolate(i * ls.length / (n - 1)).coords[0] for i in range(n))]
    return unary_union(sq)


def slot_poly():
    """Anvil drag slot = interface slot U swept holder footprint + 0.30 (DEV-L4, adopted in interface Rev B as
    interface.slot_polygon(): the buffers alone leave 0.04 mm at the J fillet and 0.16 mm on the 45-deg lane arcs for
    the 2.6-sq holder, and the round cap at the bead-out stop cuts the holder corners)."""
    return I.slot_polygon()


def contact_poly():
    o = I.ANVIL_CONTACT_OPENING
    return box(o["x"][0], o["y"][0], o["x"][1], o["y"][1])


def mw_recess_poly():
    c, s = I.M_W_RECESS["center"], I.M_W_RECESS["size"]
    return box(c[0] - s[0] / 2, c[1] - s[1] / 2, c[0] + s[0] / 2, c[1] + s[1] / 2)


def through_openings():
    """All openings through the thin plate (windows, slot, contact opening)."""
    return unary_union([window_poly(c) for c in I.WINDOWS.values()] + [slot_poly(), contact_poly()])


# Liquid ports: 10 in the anvil, P_cf in the cold plate (interface PORTS, CHOICE-4)
LIQ_PORTS = {k: p for k, p in I.PORTS.items() if p.kind == "liquid"}
ANVIL_PORTS = [k for k, p in LIQ_PORTS.items() if p.xy[0] > I.X_BREAK[1]]
COLD_PORTS = [k for k, p in LIQ_PORTS.items() if p.xy[0] < I.X_BREAK[0]]
PORT_BORE_D = I.FACE_SEAL["insert_d"]          # 3.3: insert bore = gasket seat (CHOICE-4)
INSERT = {
    "d": PORT_BORE_D,                          # PEEK insert, sliding fit in a reamed D3.3 H7 bore [assessment]
    "top_z": -I.FACE_SEAL["counterbore_depth"],  # -0.38: gasket seat (interface counterbore depth)
    "bottom_z": -ANVIL_T,                      # rests on the retainer plate under the thick zone
    "tube_bore": 1.60,                         # bonded 1/16" tube: D1.5875 + 0.0125 radial for adhesive [assessment]
    "material": "PEEK (natural, unfilled), turned",
}
RETAINER_T = 3.0                               # retainer plates under the thick zones (Al), screwed [assessment]
GASKET = {k: I.FACE_SEAL[k] for k in ("gasket_id", "gasket_od", "gasket_t")}
TUBE_OD = I.FACE_SEAL["tube_od"]               # 1.5875
TUBE_BEND_R_MIN = 25.0                         # MTC/MicroSolv KB "smallest recommended bend radius for PEEK tubing is
#                                                25 mm" (mtc-usa.com, opened 2026-11-13)

# Retainer plate groups (CHOICE-L5): one plate per thick zone; footprints (x0, y0, x1, y1)
RETAINERS = {
    "ret_island": (26.0, 21.2, 39.5, 29.4),    # P_in, P_byp, P_b, P_a
    "ret_Pd1": (27.0, 38.5, 32.0, 43.5),
    "ret_Pd2": (27.0, 6.5, 32.0, 11.5),
    "ret_Pa2": (49.3, 34.8, 53.3, 38.7),
    "ret_Ps": (60.6, 18.2, 65.5, 22.8),
    "ret_Pwo": (63.5, 33.0, 68.5, 38.0),
    "ret_Prf": (70.0, 3.0, 75.0, 8.0),
}

# Head guide pin bushes (lid head located on the nest, interface TOL head_to_nest 0.03). Positions are NOT in
# interface.py -> chosen here (CHOICE-L6) and listed as an interface change request (docs/21 §10).
GUIDE_BUSH = {"pins": [I.HEAD_GUIDE_PINS["GP1"], I.HEAD_GUIDE_PINS["GP2"]],   # (revised at integration): interface
              # Rev B HEAD_GUIDE_PINS (-8, 46), (84, 4) (was (-7, 46), (83, 4) here, (-5, 44), (80.5, 6) in UPPER)
              "pin_d": I.HEAD_GUIDE_PINS["pin_d"], "bush_od": I.HEAD_GUIDE_PINS["bush_od"], "bush_len": 15.0,
              "material": "CuSn8 bronze, non-magnetic, reamed D6 H7 [assessment]"}

# Drip gutter on the anvil top just outside the card (CHOICE-L7)
GUTTER = {"inner_offset": 0.3, "w": 1.5, "depth": 1.0,
          "drains": [(-1.05, -1.05), (I.CARD_L + 1.05, -1.05)], "drain_d": 3.0}
# M_w waste magnet in its recess (interface M_W_RECESS, MAGNETS M_w)
M_W = I.MAGNETS["M_w"]

# Anvil heater (assay zone 25.0 degC): polyimide foil heaters bonded to the underside of the thick frame, PID on a
# thermistor at the windows (CHOICE-L8). Envelopes only (heater part UNVERIFIED).
ANVIL_HEATERS = {"hW": (-11.0, -15.0, 0.0, 65.0), "hE": (76.0, -15.0, 89.0, 65.0), "hS": (24.0, -15.0, 75.0, -1.0),
                 "hN": (24.0, 51.0, 75.0, 65.0)}
HEATER_T = 0.3

# =====================================================================================================
# 2. Nest frame (on the anvil top, z 0 .. 5.0 <= LOWER_nest_anvil top 6.0)
# =====================================================================================================
NEST_T = I.NEST_FRAME_TOP_Z                     # 5.0 = datum pin protrusion (interface Rev B NEST_FRAME_TOP_Z)
NEST_OPEN = {"x": (-1.8, I.CARD_L + 1.8), "y": (-1.8, I.CARD_W + 1.8)}   # card + 1.8: gutter visible, lead-in
NEST_CHAMFER = 1.5                              # 45 deg lead-in at the top inner edge [assessment]
DATUM_PIN_Z = (0.2, I.DATUM_PIN_PROTRUSION)     # pins held in the frame, 0.2 above the anvil (gutter passes below)
DATUM_PIN_MATERIAL = "zirconia ceramic dowel D4 (non-magnetic, hard) -- part UNVERIFIED (CHOICE-L9)"
PUSHER = {"body_d": 4.0, "body_len": 12.0, "tip_d": 2.5, "z": 2.5, "stroke": 1.5,
          "note": "spring plunger with domed POM tip, 5 N at the seated card (interface PUSHERS) -- part UNVERIFIED"}
CARD_PRESENCE = {"xy": (-6.0, 10.0), "z": 2.5, "size": (5.0, 4.0, 3.0),
                 "note": "reflective IR sensor in the W wall aimed +x at the L3 side face -- part UNVERIFIED"}

# Bay frame (CHOICE-L15): base plate on the BASE_under_bay boundary, side walls outside the M_d X-stage sweep,
# four beams carrying the anvil (lift-off on dowels). Boxes (x0, y0, z0, x1, y1, z1).
BAY_BASE = (-40.0, -55.0, -130.0, 130.0, 125.0, -126.0)
BAY_WALLS = {"wall_W": (-38.0, -20.0, -126.0, -30.0, 70.0, -15.0), "wall_E": (124.0, -20.0, -126.0, 130.0, 70.0, -15.0)}
BAY_BEAMS = {"beam_SW": (-30.0, -15.0, -25.0, -5.0, -8.0, -15.0), "beam_NW": (-30.0, 54.0, -25.0, -4.0, 62.0, -15.0),
             "beam_SE": (82.0, -15.0, -25.0, 124.0, -8.0, -15.0), "beam_NE": (82.0, 54.0, -25.0, 124.0, 62.0, -15.0)}
BEAM_DOWELS = [(-8.0, -11.5), (-8.0, 58.0), (86.0, -11.5), (86.0, 58.0)]
# =====================================================================================================
# 3. Reagent cold plate and Peltier stack (CHOICE-7, CHOICE-L4)
# =====================================================================================================
COLD_BODY_Z = (-22.0, 0.0)                       # Al block: 5-mm top plate region + body (P_cf insert, thermistor)
COLD_SPREADER = {"x": (-10.0, I.X_REAGENT[1]), "y": (2.0, 32.0), "z": (-22.0, -17.0)}   # flange under the module
PELTIER = {"x": (-10.0, 20.0), "y": (2.0, 32.0), "t": 3.3,
           "part": "Custom Thermoelectric 12711-5L31-04CL: 30.0 x 30.0 x 3.3 mm, 127 couples, Imax 4.0 A, "
                   "Qmax 33.4 W, Vmax 15.4 V, DTmax 67 degC (spec sheet opened 2026-11-13)"}
HEATSINK = {"x": (-12.0, 20.0), "y": (-4.0, 33.0), "base_t": 6.0, "fin_to": -52.0,   # west tubes pass below at z -56..-60
            "spec": "Al extrusion, fins along y, R_th <= 1.0 K/W at the duct flow -- part UNVERIFIED"}
FAN = {"x": (-4.0, 20.0), "y": (-14.0, -4.0), "z": (-52.0, -26.0),
       "spec": "25 x 25 x 10 mm class axial fan, exhausting -y into a duct to the front panel -- part UNVERIFIED"}
DUCT = {"x": (-4.0, 20.0), "y": (-55.0, -14.0), "z": (-52.0, -26.0)}   # x >= -4: clear of beam_SW for lift-off
FOAM_T = 5.0                                     # closed-cell foam (k ~0.035 W/m K UNVERIFIED) round the cold block

# =====================================================================================================
# 4. M_c collection units (two, mirror about y = 25) -- parallelogram swing (DEV-L1, DEV-L2, CHOICE-L10)
# =====================================================================================================
MC = I.MAGNETS["M_c1"]
MC_MAG = MC["size"]                              # 10 x 10 x 5 NdFeB (docs/13 §3.3.1); catalogue: supermagnete
#                                                  Q-10-10-05-N, N42, Ni, +-0.1, magnetised through 5 (opened)
MC_HOLDER = MC["holder"]                         # 10.6 sq (interface)
MC_TOP_UP = MC["z_top_up"]                       # -0.16
MC_FLANGE = (12.6, 13.0, 2.0)                    # x, y, t: seats on the plate underside z = -5.0 (CHOICE-L10)
#  gap = plate thickness - (flange top to magnet top) = 5.000 - 4.840 = 0.160 (Derived); tolerance chain in docs/21 §5
MC_COLUMN = (8.0, 8.0)                           # carrier column below the flange [assessment]
MC_LINK_Z = (-18.5, -28.5)                       # parallelogram link pivot heights on the carrier (up state)
MC_R = 64.5                                      # link length (DEV-L2): window exit drift 65 - sqrt(65^2 - 5^2) = 0.19
#                                                  mm < 0.40 holder clearance (Derived); M_c2 pivot at y 12 - 64.5 = -52.5
#                                                  inside the LOWER claim (y >= -55)
MC_PARK_SHIFT = 18.7                             # outward shift at park (interface retract 18; DEV-L2)
MC_THETA_PARK = math.degrees(math.acos(1 - MC_PARK_SHIFT / MC_R))   # Derived 44.6 deg
MC_DROP_PARK = MC_R * math.sin(math.radians(MC_THETA_PARK))         # Derived 45.6 mm
MC_UP_PRELOAD_N = 6.0                            # torsion spring in the drive coupling -> flange onto the plate [assessment]
MC_DRIVE = {"spec": "stepper + self-locking worm gearbox on the upper link shaft, >= 0.6 N m, 45 deg in <= 5 s; "
                    "part UNVERIFIED", "size": (26.0, 12.0, 30.0)}
MC_SWITCHES = "optical fork switches on a flag at the drive shaft: UP (spring wound), PARK; part UNVERIFIED"


def mc_offset(theta_deg, unit=1):
    """(dy, dz) of the M_c carrier for swing angle theta (0 = up). Positive dy = outward (+y for unit 1)."""
    t = math.radians(theta_deg)
    dy = MC_R * (1 - math.cos(t))
    dz = -MC_R * math.sin(t)
    return (dy if unit == 1 else -dy), dz


MC_STATES = {"up": 0.0, "park": MC_THETA_PARK}

# =====================================================================================================
# 5. M_d drag magnet system (CHOICE-6 interface; CHOICE-L11..L13 here)
# =====================================================================================================
MD = I.MAGNETS["M_d"]
MD_MAG = MD["size"]                              # 2 x 2 x 4 along z
MD_HOLDER = MD["holder"]                         # 2.6 sq
MD_TOP_UP = MD["z_top_up"]                       # -0.16
MD_STROKE = MD["z_stroke"]                       # 8.0
MD_HOLDER_Z = (-4.6, MD_TOP_UP)                  # holder body (Ti) [assessment]
MD_NECK = {"d": 2.0, "z": (-6.0, -4.6)}          # inside the plate when up (plate underside -5.0)
MD_POST = {"d": 4.0, "z": (-62.0, -6.0), "material": "Ti-6Al-4V (non-magnetic)"}
MD_ZUNIT = {"half": 8.0, "z": (-80.0, -62.0),   # carried by the X carriage; spring-up post carrier, cam pull-down
            "spec": "post carrier on 2 x D3 ground pins in bronze bushes; compression spring 3 N up; eccentric cam "
                    "4 mm on a back-drivable gearmotor (<= 30:1) pulls 8 mm down; up-stop M3 x 0.35 fine screw "
                    "sets the 0.16 gap -- motor UNVERIFIED",
            "umbrella": 20.0}                    # PEEK drip umbrella on the Z unit top (CHOICE-L13)
STAGE = {  # Zaber X-LSM050A (zaber.com spec page opened 2026-11-13): travel 50.8, repeatability < 3 um, accuracy
    # 20 um, 26 mm/s max, 0.000029 mm/s min, continuous thrust 25 N, flatness < 11 um, straightness < 14 um,
    # pitch/roll/yaw 0.03 deg, non-back-driving, 0.34 kg. FOOTPRINT NOT PUBLISHED ON THE PAGES OPENED ->
    # allocation envelope below is UNVERIFIED (L x W x H).
    "env": (150.0, 40.0, 22.0),
    "x_travel_center": 0.5 * sum(MD["travel_x"]),   # 47.3
    "y_travel_center": 0.5 * sum(MD["travel_y"]),   # 25.0
    "Y_z": (-126.0, -104.0), "X_z": (-104.0, -82.0),   # on the bay base plate (top z -126)
}

# M_d paths (card xy), all from interface.py
GATHER = {}
for ch, c in (("IC1", I.IC1.center), ("IC2", I.IC2.center)):
    for k, (a, b) in I.GATHER_PASSES.items():
        GATHER[(ch, k)] = [(c[0] + a[0], c[1] + a[1]), (c[0] + b[0], c[1] + b[1])]
TRANSIT_LOWERED = {  # CHOICE-L12: lowered moves only via J (interface MAGNET_TRANSIT_RULE)
    "park_to_IC1": [I.M_D_PARK_POS, (44.0, 30.0), (I.IC1.center[0] - 3.5, I.IC1.center[1] + 2.0)],
    "park_to_IC2": [I.M_D_PARK_POS, (44.0, 20.0), (I.IC2.center[0] - 3.5, I.IC2.center[1] - 2.0)],
    "beadout_to_park": [I.BEAD_OUT_PATH[-1], (57.85, 25.0), I.M_D_PARK_POS],
    "gather_return_IC1": [(I.IC1.center[0] + 2.5, I.IC1.center[1]), (I.IC1.center[0] - 3.5, I.IC1.center[1] - 2.0)],
}

# =====================================================================================================
# 6. Electrode bay (interface LOWER_SUBCLAIMS_CARD electrode_bay x 54-62.5, y 28.8-36.5, z -70-0)
# =====================================================================================================
EBAY = {"x": (54.0, 62.5), "y": (28.8, 36.5), "z": (-58.0, Z_THIN_BOTTOM), "wall": 1.0,
        "material": "Al 6061, grounded (star point), chromate-free conversion coat"}
POGO_PROBE = {  # PTR Hartmann series 1007.70 (opened 2026-11-13): centre 1.27 mm, full travel 1.27, preload 0.50 N,
    # 1.40 N at full travel, recommended drill 0.87 (0.95 with press ring), CuBe Au plunger, bronze Au barrel, <= 25 mOhm
    "drill": 0.87, "full_travel": 1.27, "f_pre": 0.50, "f_full": 1.40, "work_travel": I.POGO["working_travel"],
    "exposed": 1.5,                                  # plunger length above the block, UNVERIFIED (drawing not read)
}
POGO_F_WORK = POGO_PROBE["f_pre"] + (POGO_PROBE["f_full"] - POGO_PROBE["f_pre"]) * POGO_PROBE["work_travel"] / \
    POGO_PROBE["full_travel"]                        # Derived linear spring: 1.21 N
POGO_TIP_Z_ENGAGED_FREE = I.POGO["tip_z_engaged"] + I.POGO["working_travel"]   # 1.34: free tip height at the up stop
POGO_TIP_Z_RETRACTED = I.POGO["tip_z_retracted"]   # -1.66 (ICR-3, adopted in interface Rev B)
POGO_NOSE = (5.2, 3.2)                               # PEEK nose in the 5.4 x 3.4 opening (0.1 radial) [assessment]
POGO_NOSE_TOP_UP = POGO_TIP_Z_ENGAGED_FREE - POGO_PROBE["exposed"]   # -0.16
POGO_SHOULDER = (7.0, 6.2, 4.0)                      # block body under the plate; hits z -5.0 at the up position
POGO_WEDGE = {"ratio": 2.0, "x_stroke": 6.0,
              "cyl": "single-acting spring-return pneumatic cylinder, bore 6-8, stroke >= 6, non-magnetic piston, "
                     "outside the E wall in corridor E -- part UNVERIFIED"}
RELAY = {"xy": (58.25, 34.5), "z": (-48.0, -40.0), "size": (5.0, 4.0, 8.0),
         "spec": "reed relay, insulation >= 1e13 Ohm (Pickering 'Series X, Y & Z' class quoted >1e13 in search "
                 "snippet; page 403 -> UNVERIFIED), mu-metal screened, 1 Form A"}
RH_SENSOR = {"xy": (58.25, 31.0), "z": (-30.0, -28.0), "spec": "digital RH/T sensor on a 6 x 4 mm PTFE board -- "
             "part UNVERIFIED (Sensirion SHT4x class, datasheet not opened)"}
GAMRY_BULKHEAD = I.PASS_THROUGHS["gamry_cell_cable"]["dock"]    # (320, 107, 135) dock

# =====================================================================================================
# 7. Tube routes (1/16" PEEK, bend R >= 25; CHOICE-L14)
# =====================================================================================================
TUBE_VERT_TO = {"P_in": -31.0, "P_byp": -33.0, "P_b": -37.0, "P_a": -35.0, "P_d1": -33.0, "P_d2": -33.0,
                "P_a2": -33.0, "P_wo": -30.0, "P_s": -33.0, "P_rf": -33.0}   # staggered so parallel runs keep
#                 >= 0.4 mm between tube walls (CHOICE-L14)


def _arc(p0, d_h, R=TUBE_BEND_R_MIN, n=12):
    """Vertical-down to horizontal (unit plan direction d_h) bend of radius R starting at p0 = (x, y, z)."""
    x0, y0, z0 = p0
    pts = []
    for i in range(n + 1):
        a = math.radians(90.0 * i / n)
        h = R * (1 - math.cos(a))
        v = R * math.sin(a)
        pts.append((x0 + d_h[0] * h, y0 + d_h[1] * h, z0 - v))
    return pts


def _plan_arc(p0, d0, d1, R=TUBE_BEND_R_MIN, n=10):
    """Horizontal bend of radius R from plan direction d0 to d1 (90 deg), at constant z."""
    x0, y0, z0 = p0
    cx, cy = x0 + d1[0] * R, y0 + d1[1] * R
    pts = []
    for i in range(n + 1):
        a = math.radians(90.0 * i / n)
        pts.append((cx - d1[0] * R * math.cos(a) + d0[0] * R * math.sin(a),
                    cy - d1[1] * R * math.cos(a) + d0[1] * R * math.sin(a), z0))
    return pts


TUBE_DIR = {"P_in": (-1, 0), "P_byp": (-1, 0), "P_b": (-1, 0), "P_a": (-1, 0), "P_d1": (-1, 0), "P_d2": (-1, 0),
            "P_s": (1, 0), "P_rf": (1, 0), "P_a2": (0, 1), "P_wo": (1, 0)}
TUBE_EXIT = {"W": I.SPACE_CLAIMS["LOWER_bay"]["box"][0][0] - I.CARD_ORIGIN_IN_DOCK[0],      # card x -40
             "E": I.SPACE_CLAIMS["LOWER_bay"]["box"][1][0] - I.CARD_ORIGIN_IN_DOCK[0]}      # card x 130


def tube_route(port):
    """3-D polyline of a port tube from the anvil top (z 0) to the LOWER claim wall (card coords)."""
    x, y = I.PORTS[port].xy
    if port == "P_cf":   # through the cold block, straight down beside the module, then west under the heat sink
        pts = [(x, y, 0.0), (x, y, -33.0)]
        pts += _arc((x, y, -33.0), (-1, 0))[1:]
        pts.append((TUBE_EXIT["W"], y, pts[-1][2]))
        return pts
    d = TUBE_DIR[port]
    zv = TUBE_VERT_TO[port]
    pts = [(x, y, 0.0), (x, y, zv)]
    pts += _arc((x, y, zv), d)[1:]
    if d[0] != 0:
        ex = TUBE_EXIT["W"] if d[0] < 0 else TUBE_EXIT["E"]
        pts.append((ex, pts[-1][1], pts[-1][2]))
    else:  # north, then plan bend to +x, run east to the E wall
        pend = pts[-1]
        pts += _plan_arc(pend, (0, 1), (1, 0))[1:]
        pts.append((TUBE_EXIT["E"], pts[-1][1], pts[-1][2]))
    return pts


TUBE_PORTS = list(LIQ_PORTS)

# =====================================================================================================
# 7b. Integration additions (revised at integration, docs/23): poka-yoke block, latch catch brackets, hinge
#     pedestals, mounting to the BASE deck
# =====================================================================================================
POKA = I.NEST_POKA_BLOCK                          # 0.3 clear of the card chamfer, z 0.2-5.0, lead-in 1.5
LATCH_BRACKETS = []                               # card-coord boxes (x0, y0, z0, x1, y1, z1) per latch
for (_p0, _p1) in I.LID_LATCH["catch_keepouts_dock"]:
    _a, _b = I.dock_to_card(_p0), I.dock_to_card(_p1)
    LATCH_BRACKETS.append({"x": (_a[0], _b[0]), "y": (_a[1], ANVIL_Y[0]),     # y -41 ... -16 (anvil front face)
                           "shelf_z": (-9.0, -4.0), "flange": (-20.0, -15.0, -4.0),   # flange y -20..-16, z -15..-4
                           "catch": {"y": (_a[1] + 1.0, _a[1] + 15.0), "z": (-4.0, 1.0)}})
#   Al 6061, 5 mm shelf + flange, 2 x M5 into the anvil front face [assessment]; catch plate K0045.9143372 envelope
#   (UNVERIFIED dims). Load 95 N up per bracket (interface LID_LATCH): bending 95 x 25 = 2.4 N m on a 26 x 5 section
#   -> 22 MPa (Derived), well below Al 6061-T6 yield (~240 MPa, handbook UNVERIFIED)
HINGE_PEDESTALS = [tuple(I.dock_to_card(p) for p in b) for b in I.HINGE_SUPPORT["pedestals_dock"]]
#   Al 6061 blocks 4 x 15 x 116, bolted to the bay base plate (2 x M5 from below) + gusset to the wall [assessment]
MOUNT_BOLTS = [I.dock_to_card((x, y, 0))[:2] for (x, y) in I.LOWER_MOUNT["bolts_dock"]]
MOUNT_DOWELS = [I.dock_to_card(I.LOWER_MOUNT["dowel_round_dock"] + (0,))[:2],
                I.dock_to_card(I.LOWER_MOUNT["dowel_slot_dock"] + (0,))[:2]]

# =====================================================================================================
# 8. Machine states for the assembly and the checks
# =====================================================================================================
STATES = {
    # name: (M_c1 swing deg, M_c2 swing deg, M_d xy, M_d up?, pogo up?)
    "load":        (MC_THETA_PARK, MC_THETA_PARK, I.M_D_PARK_POS, False, False),
    "collect_IC1": (0.0, MC_THETA_PARK, I.M_D_PARK_POS, False, True),
    "collect_IC2": (MC_THETA_PARK, 0.0, I.M_D_PARK_POS, False, True),
    "gather_IC1":  (MC_THETA_PARK, MC_THETA_PARK, GATHER[("IC1", "pass1")][0], True, True),
    "gather_IC1_low": (MC_THETA_PARK, MC_THETA_PARK, GATHER[("IC1", "pass2")][0], False, True),
    "drag_mid_IC1": (MC_THETA_PARK, MC_THETA_PARK, I.DRAG_PATH["IC1"][len(I.DRAG_PATH["IC1"]) // 2], True, True),
    "hold_RC":     (MC_THETA_PARK, MC_THETA_PARK, I.M_D_HOLD_POS, True, True),
    "beadout_end": (MC_THETA_PARK, MC_THETA_PARK, I.BEAD_OUT_PATH[-1], True, True),
}
RENDER_STATES = ["load", "collect_IC1", "gather_IC1", "drag_mid_IC1", "hold_RC", "beadout_end"]
