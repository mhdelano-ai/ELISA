"""DOCK UPPER parameters (lid / head), C2 prototype. Units mm, N, kPa, W, deg C.

Every interface number is IMPORTED from elisa_cad.interface (never retyped). Numbers defined here are owned by
DOCK UPPER and carry a source tag: docs/xx §y | interface.<NAME> | Derived (arithmetic in comment) |
CHOICE-Un / DEV-Un (docs/20 §6/§7) | [assessment] | UNVERIFIED | vendor document opened 2026-11-13 (docs/20 §11).
Coordinates: CARD coords (x, y, z; z = 0 foil underside) unless named *_DOCK. P_dock = P_card + CARD_ORIGIN_IN_DOCK.
"""
from __future__ import annotations

import math

from elisa_cad import interface as IF

# ---------------------------------------------------------------------------------------------------------------
# 0. Reference levels (card z)
# ---------------------------------------------------------------------------------------------------------------
Z_CARD_TOP = IF.CARD_T                                  # 6.215, interface.CARD_T
Z_NEST_TOP_MAX = IF.NEST_FRAME_TOP_Z                    # 5.0: nest frame + guide-bush top (revised at integration:
#                                                         was the LOWER claim top 6.0; interface Rev B NEST_FRAME_TOP_Z)
HEAD_DROP = IF.HEAD_VERTICAL_STROKE                     # 8.0, interface.HEAD_VERTICAL_STROKE
HB_Z0, HB_Z1 = IF.HEAD_Z["heater_block"]                # 6.215 .. 16.215 interface.HEAD_Z
SPRING_ZONE = IF.HEAD_Z["pin_spring_zone"]              # 16.215 .. 24.5
TIER_Z = {0: IF.HEAD_Z["yoke_tier_0"], 1: IF.HEAD_Z["yoke_tier_1"]}   # (27, 31), (32, 36)
CYL_Z0, CYL_Z1 = IF.HEAD_Z["cylinder_block"]            # 38 .. 68
COVER_TOP_MAX = IF.HEAD_Z["cover_top_max"]              # 125 (= dock Z 295)

# ---------------------------------------------------------------------------------------------------------------
# 1. Head plates (thermal + clamp) -- CHOICE-7/8 (docs/18), detailing CHOICE-U1..U3
# ---------------------------------------------------------------------------------------------------------------
HB_X = IF.X_ASSAY                                       # (24.0, 75.5) Al heater block = pin guide, interface.THERMAL
HB_Y = (0.0, IF.CARD_W)
PEEK_X = (0.0, IF.X_REAGENT[1])                         # (0, 20) PEEK pressure plate, interface.THERMAL
HEATER_FIN = {"t": 2.0, "x": (24.5, 75.3), "z": (HB_Z1, HB_Z1 + 13.1)}  # CHOICE-U3: two vertical fins rising from
#   the heater-block top at its +/-y edges (y 0-2 and 48-50); one 12.7 x 50.8 foil heater on each outer face
GUIDE_PLATE_T = 3.0          # CHOICE-U2: bearing-bronze CuSn8 lower guide plate inset in the heater block face
GUIDE_PLATE_T_UP = 2.0       # upper guide plate (same material) in the heater-block top: 2-point pin guidance
PIN_FIT = {"0.8": (0.800, 0.806), "1.0": (1.000, 1.006), "1.2": (1.200, 1.206)}   # guide hole H7 (+0..+6 um at <3 mm)
#   ISO 286 [assessment]; "1.0" = Rev C slot pins (G1-G4, V11, V12), which use the 0.8-class collar/neck/button
PIN_SHANK_TOL = {"0.8": (-0.006, -0.002), "1.2": (-0.006, -0.002)}   # g5-class grinding [assessment]

# Clearance pockets in the head face (card coords)
VENT_POCKET_D = IF.VENT_POCKET_D_LID                    # 6.0, interface.VENT_POCKET_D_LID
VENT_POCKET_DEPTH = 1.0                                 # [assessment]
VENT_GROOVE_W = 2.0                                     # sideways vent groove to the block edge [assessment]
VENT_EXITS = {"vent_IC1": (0, 1), "vent_IC2": (0, -1), "vent_RS": (1, 0)}   # direction of the groove (CHOICE-U4)
DIE_POCKET_CLEAR = 0.5       # head-face pocket = die window outline (die + 0.05) + 0.5 [assessment]
PIN_FACE_CLEAR_D = {"0.8": 1.0, "1.2": 1.5}             # guide hole at the face (lead-in into the card bore)

# Head-plate standoffs (PEEK, insulating) between plates and the cylinder block -- [assessment] positions checked
STANDOFF_D = 6.0
STANDOFFS_HB = [(26.5, 5.0), (73.0, 5.0), (26.5, 45.0), (73.0, 45.0)]
MID_PILLARS = [(46.0, 5.0), (46.0, 45.0)]     # under the spring plate only
STANDOFFS_PEEK = [(10.0, 5.0), (12.0, 46.5)]

# ---------------------------------------------------------------------------------------------------------------
# 2. Valve pins, springs, collars (CHOICE-2/3, PLUNGER) -- detailing CHOICE-U5..U7
# ---------------------------------------------------------------------------------------------------------------
STROKE = IF.PLUNGER["stroke_pin"]                        # 0.8
TIP_Z_CLOSED = IF.PLUNGER["tip_z_closed"]                # 0.50 (interface Rev C: real stop height; Rev B 0.17)
TIP_Z_CLOSED_RANGE = IF.PLUNGER["tip_z_closed_range"]    # (0.37, 0.54) estimate, docs/24 S3
TIP_Z_OPEN = IF.PLUNGER["tip_z_open"]                    # 0.97 (interface Rev B; Rev A 1.015)
DROP_BELOW_CLOSED = 0.2                                  # interface.PLUNGER pin_extension_limit (collar stop)
COLLAR_T = 0.5                                           # [assessment]
COLLAR_D = {"0.8": 1.4, "1.2": 2.0}                      # spring seat; 1.4 at 1.6 pitch leaves 0.2 [assessment]
# collar position (closed): bottom 0.2 above the heater-block top, so the collar lands on the block when no card
COLLAR_Z_CLOSED = (HB_Z1 + DROP_BELOW_CLOSED, HB_Z1 + DROP_BELOW_CLOSED + COLLAR_T)   # 16.415..16.915 (Derived)
SPRING_PLATE_Z = (SPRING_ZONE[1], SPRING_ZONE[1] + 1.5)  # 24.5..26.0 fixed retainer plate (springs react here)
NECK_D = {"0.8": 0.5, "1.2": 0.8}                        # pin extension above the collar [assessment]
HEAD_BTN_D = {"0.8": 1.3, "1.2": 1.8}                    # top button (bonded hypotube sleeve, CHOICE-U6)
HEAD_BTN_T = 0.8
EYE_T = 1.5                                              # blade eye (fork) height at the pin end
HOOK_GAP = 0.2                                           # eye top -> button underside at 'closed' (CHOICE-U6):
#   with no card the pin drops 0.2 and the collar AND button land together (collar on the block is the stop)
FORK_SLOT = {"0.8": 0.7, "1.2": 1.0}                     # fork slot width (neck + 0.2)

# Pin springs (compression, above the collar, below the spring plate). (revised at integration, docs/23 I-10):
# material Co-Cr-Ni non-magnetic spring wire (Elgiloy/Phynox class, interface MATERIALS) instead of 1.4310, which is
# partly martensitic (magnetic) when work-hardened. G kept at 70 GPa for the calculation [UNVERIFIED; Co-Cr-Ni class
# G is similar]; preload is trimmed per pin by shim washers, so a G error moves only the force at +0.8 open.
SPRING_G = 70000.0           # N/mm^2 [UNVERIFIED]
PIN_SPRINGS = {  # klass -> d wire, D mean, n active, target preload at closed (N)  [CHOICE-U5]
    "slot":  {"d": 0.20, "Dm": 1.10, "n": 24, "F_closed": 1.2},
    "anvil08": {"d": 0.25, "Dm": 1.05, "n": 22, "F_closed": 2.5},   # V14, V15 (0.8 pins, 2.5 N)
    "anvil12": {"d": 0.30, "Dm": 1.55, "n": 18, "F_closed": 2.5},
    "cold":  {"d": 0.30, "Dm": 1.55, "n": 18, "F_closed": 2.5},
}
SPRING_TOL = 0.10            # +-10 % on force (custom-wound springs; preload trimmed by shim washers) [assessment]
# (revised after review, docs/24 S3) preload is set per pin with a force gauge at the MEASURED closed height on the
# reference card (I-13 extended): residual force error = gauge/shim step, +-5 % [assessment]
SHIM_SET_TOL = 0.05
V3 = {   # inverted valve (fail-open) -- CHOICE-U7
    "open_spring": {"d": 0.20, "Dm": 1.55, "n": 10, "F_open": 0.5},      # lifts the pin (below the collar)
    "limit_spring_preload": 2.1,      # force-limiting spring inside the V3 piston (N)
    "limit_spring_rate": 1.0,         # N/mm
    "overtravel": 1.0,                # piston travel beyond tip contact (mm)
    # geometry (card z, valve OPEN = rest): collar under the spring plate (open stop), button BELOW the eye
    "collar_open": (24.0, 24.5),      # collar top against the spring-plate underside = open stop
    "button_open": (27.0, 27.8),      # lands on the spring-plate top (26.0) 0.2 below 'closed' (no card)
    "eye_rest": (28.0, 29.5),         # eye bottom 0.2 above the button (HOOK_GAP); eye pushes the button down
}

# ---------------------------------------------------------------------------------------------------------------
# 3. Yokes and cylinders (interface.CYLINDERS / YOKE / PLUNGER) -- CHOICE-U8..U10
# ---------------------------------------------------------------------------------------------------------------
BLADE_W = IF.YOKE["blade_w"]                 # 1.0
BLADE_H = IF.YOKE["blade_h"]                 # 4.0
PLAN_CLEAR_MIN = IF.YOKE["plan_clearance_min"]   # 0.3
BOSS_D = 3.0                                 # blade boss on the rod end [assessment]
ROD_D = 1.5                                  # piston rod (stainless, ground) [assessment]
BORE_D = IF.PLUNGER["cylinder_bore"]         # 6.0 (DEV-U2, adopted in interface Rev B)
BORE_D_IF = IF.PLUNGER["cylinder_bore"]      # 5.0 (interface value, kept for reference)
PISTON_T = 2.5
PULL_STROKE = HOOK_GAP + STROKE              # 1.0 Derived: gap 0.2 + lift 0.8 (pull cylinders, pressure under piston)
V3_STROKE = HOOK_GAP + STROKE + 1.0          # 2.0 Derived: gap + 0.8 + limit-spring overtravel 1.0
RETURN_SPRING_F = 0.5                        # N, piston return spring in the vented chamber [assessment]
P_SUPPLY_KPA = IF.PLUNGER["pilot_pressure_kPa"]   # 400 (DEV-U1, adopted in interface Rev B)
P_MIN_KPA = IF.PLUNGER["pilot_switch_trip_kPa"]  # 350: pressure switch trip [assessment], interface Rev B
CYL_LAYERS = {   # card z of the cylinder block layers (CHOICE-U10)
    "cover": (CYL_Z0 - 1.0, CYL_Z0),         # 37..38 gallery cover (bottom layer grooves are not used: 1 layer)
    "air_plate": (CYL_Z0, CYL_Z0 + 6.0),     # 38..44 rod guides + gallery grooves on its top face
    "bore_block": (CYL_Z0 + 6.0, CYL_Z1 - 6.0),   # 44..62 bores D5
    "cap": (CYL_Z1 - 6.0, CYL_Z1),           # 62..68 return-spring seats, vents, V3 air
}
GALLERY_W = 0.6                              # groove 0.6 x 0.6 [assessment]
GALLERY_PITCH = 1.2
CYL_BLOCK_X = (-10.0, 85.5)                  # body incl. guide-pin ears (card x)  [assessment]
CYL_BLOCK_Y = (0.0, IF.CARD_W)
PISTON_MAGNET = {"d": 2.0, "t": 1.0}         # NdFeB disc in the piston top, read by a Hall IC above the cap
HALL_PCB_Z = (CYL_Z1 + 0.5, CYL_Z1 + 2.1)    # 1.6 mm FR4 on the cap

# ---------------------------------------------------------------------------------------------------------------
# 4. Guide pins to the nest (LOWER provides the bushes -- interface change request ICR-U1)
# ---------------------------------------------------------------------------------------------------------------
GUIDE_PINS = {k: IF.HEAD_GUIDE_PINS[k] for k in ("GP1", "GP2")}   # (revised at integration) interface Rev B
#   HEAD_GUIDE_PINS (-8, 46), (84, 4); were (-5, 44), (80.5, 6) here (the bush at (-5, 44) broke into the nest opening)
GUIDE_PIN_D = IF.HEAD_GUIDE_PINS["pin_d"]                  # 6.0, h6 hardened (>= 45 mm from every magnet)
GUIDE_PIN_TIP_Z_RAISED = IF.HEAD_GUIDE_PINS["pin_tip_z_raised"]   # 5.5: tip 0.5 above the bush top (z 5.0) when raised
GUIDE_PIN_TIP_Z = GUIDE_PIN_TIP_Z_RAISED - HEAD_DROP       # -1.5 lowered (Derived)
GUIDE_PIN_NOSE = 1.0                                       # conical lead 1.0 long
GUIDE_EAR_BOTTOM_Z = 8.0                                   # ears stop 2.0 above the nest top when lowered

# ---------------------------------------------------------------------------------------------------------------
# 5. Press pad, gas seals (interface.DIE_PRESS_PAD, GAS_SEAL_LID)
# ---------------------------------------------------------------------------------------------------------------
PAD = IF.DIE_PRESS_PAD
PAD_STOP_BELOW_DIE = 0.5      # pad face stop 0.5 below the nominal die back when no card (z 0.54)
PAD_SPRING = {"d": 0.8, "Dm": 6.0, "n": 9.4, "preload_at_stop": 11.0, "rate": 2.0}   # 12.0 N at DIE_T 0.70
PAD_STEM_D = 4.0
GAS = IF.GAS_SEAL_LID
GAS_GROOVE_DEPTH = GAS["t"] - GAS["compression"]           # 0.75 Derived
GAS_PORTS = {k: p for k, p in IF.PORTS.items() if p.kind == "gas"}   # P_c, P_mv

# ---------------------------------------------------------------------------------------------------------------
# 6. Lid structure, hinge, cam, latch (CHOICE-10 docs/18; CHOICE-U11..U15)
# ---------------------------------------------------------------------------------------------------------------
HINGE = IF.LID_HINGE_AXIS                                  # point (150, 195, 190) dock, 85 deg
CLAIM = IF.SPACE_CLAIMS["UPPER_lid_closed"]["box"]         # ((150, 30, 176.215), (320, 200, 300)) dock
SIDE_PLATE_X = ((154.0, 162.0), (306.5, 314.5))            # dock X of the two lid side plates (8 mm Al 6082)
LID_Y = (55.0, 196.0)                                       # dock Y: cover front wall / rear wall (CHOICE-U12)
LID_BOTTOM_Z = CLAIM[0][2] + 2.0                            # 178.215 dock: 2 mm above the claim floor
COVER_T = 1.5                                               # Al 5754 sheet, grounded (shield above the die)
COVER_X = (152.5, 316.0)
COVER_TOP_Z = 295.0                                         # dock (<= 300 claim; card z 125 = HEAD_Z cover_top_max)
SIDE_PLATE_Y = (56.5, 200.0)                                # side plates reach round the hinge axis (r 8)
SIDE_PLATE_Z = (LID_BOTTOM_Z, 287.0)
HEAD_GUIDE_POSTS = [(-21.0, 6.0), (-21.0, 44.0), (96.5, 6.0), (96.5, 44.0)]   # card xy, D8 posts on the bridge
POST_D = 8.0
POST_TOP_Z = 278.0                                          # dock, head lowered (stays in the 263-275 bearing blocks when raised)
BRIDGE_X = (-27.0, 102.5)                                   # card x of the head bridge (cam thrust member)
BRIDGE_Z = (CYL_Z1 + 3.0, CYL_Z1 + 11.0)                    # 71..79 card (dock 241..249)
CAM = {"e": 4.5, "R": 10.0, "w": 8.0, "x": (-17.0, 92.5), "y": 25.0,   # eccentric e 4.5 -> stroke 9 = 8 + 1
       "follower_top_latched_dock": 262.0, "shaft_d": 10.0, "lever_L": 60.0}
CAM["shaft_z_dock"] = CAM["follower_top_latched_dock"] + CAM["e"] + CAM["R"]     # 276.5 Derived
CLAMP_SPRING = {"preload": 135.0, "rate": 15.0, "overtravel": 1.0, "OD": 14.0, "free_L": 25.0}   # per side
HEAD_RETURN_SPRINGS_N = 20.0                                # total, 4 springs on the posts [assessment]
LATCH = {"model": "Kipp K0045.1541092 (stainless, form A, F1 2000 N)", "L": 109.0, "W": 26.0, "H": 21.0,
         "x_dock": (173.0, 297.0), "y_face_dock": 55.0, "src": "marek.eu K0045 catalogue page (opened); W/H interpretation UNVERIFIED"}

# ---------------------------------------------------------------------------------------------------------------
# 7. Pilot valves (SMC S070, catalogue opened 2026-11-13)
# ---------------------------------------------------------------------------------------------------------------
PILOT = {"model": "SMC S070B-5DG (base mounted, 24 VDC, 0.5 W, max 0.5 MPa, Cv 0.011, C 0.042, grommet)",
         "pitch": 7.2, "max_stations": 20, "P_W": 0.5, "C_dm3_s_bar": 0.042, "b": 0.27,
         "t_on_ms": 3.0, "t_off_ms": 3.0, "envelope": (7.0, 25.5, 28.5),   # w, l, h incl. base [catalogue drawing,
         #   overall sizes read from the dimension sheet, interpretation UNVERIFIED]
         "manifold": "SS073B01-11C and SS073B01-10C bar bases (2 manifolds: 11 + 10 stations)",
         "L2": lambda n: n * 7.2 + 14.8,                     # (revised after review, docs/24 M2) catalogue SS073B01:
         "L1": lambda n: n * 7.2 + 8.8}                      # L1 = n x 7.2 + 8.8, L2 (overall) = n x 7.2 + 14.8 (the
#                                                            envelope uses the overall L2; Rev B labelled it L1)

# ---------------------------------------------------------------------------------------------------------------
# 8. Thermal (docs/07 §5.1 via docs/13 §6.5: 25.0 +- 0.2 degC)
# ---------------------------------------------------------------------------------------------------------------
T_SET = IF.THERMAL["assay_top"]["T"]       # 25.0
T_AMB = (18.0, 26.0)                       # lab range [assessment]
HEATER = {"model": "Omega KHLVA-0502/5-P (12.7 x 50.8 x 0.25 mm, 5 W at 28 V, PSA)", "n": 2,
          "R_ohm": 28.0 ** 2 / 5.0, "V_drive_max": 24.0}   # R Derived 156.8 ohm
SENSOR = {"model": "Pt100 thin-film class A, M222 class (2.3 x 2.1 x 0.9 mm)", "positions":
          {"T_ctrl": (58.0, 38.5, 11.0), "T_mon": (30.0, 46.0, 11.0)}}   # card xyz in the heater block

H_CONV = 10.0      # W/m2K natural convection inside the lid [assessment]
K_AL = 167.0       # W/mK 6061-T6 handbook [UNVERIFIED]
K_PEEK = 0.25      # W/mK [UNVERIFIED]
CP_AL = 0.90       # J/gK [UNVERIFIED]
RHO_AL = 2.70e-3   # g/mm3


def valve_class(v):
    if v.id == "V3":
        return "V3"
    if v.klass == "slot":
        return "slot"
    if v.klass == "cold":
        return "cold"
    return "anvil08" if v.pin_d < 1.0 else "anvil12"


def pkey(v):
    # (revised after review) the D1.0 slot pins (interface Rev C) take the 0.8-class collar 1.4 / neck 0.5 / button 1.3
    return "0.8" if v.pin_d < 1.1 else "1.2"


def to_dock(p):
    return IF.card_to_dock(p)
