"""DOCK BASE parameters (docs/22). Dock coordinates (interface.py §1): X to the operator's right, Y away from the
operator, Z up; origin front-left corner at bench level. Units mm, kg, W, uL.

Interface numbers are IMPORTED from interface.py, never retyped. Every local constant carries a source tag:
  docs/xx §y | interface.<NAME> | Derived (arithmetic in the comment) | CHOICE-Bn (docs/22 §11) | DEV-Bn (docs/22 §12)
  | [assessment] | UNVERIFIED | V:<key> = vendor page opened this session (URL list in docs/22 §15 and SOURCES below)
"""
from __future__ import annotations

from .. import interface as I

# ------------------------------------------------------------------------------------------------ sources opened
SOURCES = {
    "TECAN_CENTRIS_P": "https://partnering.tecan.com/cavro-centris-pump-for-oem-liquid-handling (opened 2026-11-13: "
                       "H 184.2, W 44.5, D 68.8 mm, 1.3 kg, 24 VDC +-10 %, 2.5 A peak, RS-232/485/CAN, 16 per bus, "
                       "valves 3/4-port and 3/6/9/12-port distribution)",
    "FLUIGENT_FEZ_P": "https://fluigent.com/research/instruments/pressure-flow-controllers/lineup-series/flow-ez/ "
                      "(opened: 91.9 x 71.8 x 131 mm, 634 g, 6 W; LU-FEZ-0345 supply 1100 mbar, max 1300 mbar) and "
                      "datasheet PDF text (same dimensions, weight, 6 W)",
    "LAIRD_TCA_CAT": "https://www.lairdthermal.com/.../Thermoelectric-Cooler-Assemblies-Catalog.pdf (redirect to "
                     "tark-solutions.com, PDF text extracted 2026-11-13: DA-024-24-02-00-00 24 W, 24 V, 2.4 A, 0.3 kg, "
                     "Lw 80 Lc 60 Ww 60 Wc 40 Hw 56 Hc 14; specs at 32 degC ambient)",
    "WATERS_ICLASS_SPEC": "https://ucrf.unist.ac.kr/wp-content/uploads/2024/11/ACQ.-I-Class-PLUS-Sys.-CH-A-wSM-FTN-I-"
                          "Specification.pdf (Waters spec sheet, PDF text: I-Class BSM + SM-FTN + CH-A W 34.3 cm, "
                          "H 71.1 cm, D 71.2 cm)",
    "GAMRY_CABLE_60": "https://orders.gamry.com/reference-600-cell-cable-60-cm.html (opened 2026-11-13: 60 cm, SKU "
                      "985-00071, listed 'For Reference 600 and Interface 1000/1010' only -- NOT for the Reference 600+; "
                      "revised after review, docs/24 S6)",
    "GAMRY_600P_STD_CABLE": "https://cn.gamry.com/assets/Uploads/Instructions-for-using-a-Standard-Cable-on-a-Reference-"
                            "600+.pdf (opened 2026-11-13, PDF text: the 60 cm Standard Cell Cable PN 985-00071 is used on a "
                            "Reference 600+ only with the Gamry-supplied IE correction file REF600P_CID14.IECOR and a "
                            "re-calibration with that cable in the calibration shield)",
    "GAMRY_LEGACY": "docs/18 §14 (gamry.com legacy page: 9 x 19 x 27 cm W x H x D, 3 kg) via interface.SPACE_CLAIMS",
}

# ------------------------------------------------------------------------------------------------ interface imports
FOOT = I.DOCK_FOOTPRINT                    # ((0,0,0),(470,420,330)) CHOICE-12
FX, FY, FZ = FOOT[1]
CL = I.SPACE_CLAIMS
PT = I.PASS_THROUGHS
UPPER = CL["UPPER_lid_closed"]["box"]
LOWER_NEST = CL["LOWER_nest_anvil"]["box"]
LOWER_BAY = CL["LOWER_bay"]["box"]
LOAD_BOX = I.OPERATOR_LOADING_PATH["clear_box"]
HINGE = I.LID_HINGE_AXIS

# ------------------------------------------------------------------------------------------------ structure
SHEET_T = 2.0                    # [assessment] Al 5754 sheet, powder-coated, enclosure panels
FOOT_PAD = (40.0, 5.0)           # UNVERIFIED part: swivel pad D40, 5 mm high under the plate; M10 screw adjusted
#                                  from above through the base plate (+-3 mm) [assessment]
FEET_XY = [(30.0, 30.0), (440.0, 30.0), (30.0, 390.0), (440.0, 390.0)]   # [assessment]
BASE_PLATE_Z = (FOOT_PAD[1], 15.0)        # Al 6082-T6 tooling plate 10 mm; top = BASE_drip_tray claim top (15)
TRAY = {"z0": 15.0, "floor_t": 1.0, "rim_h": 13.0, "inset": 3.0, "notch": 22.0,
        "sump": ((245.0, 150.0), (285.0, 190.0), 8.0)}   # 316 stainless 1.0 mm, folded + welded corners [assessment]
EXTR = 20.0                      # 20x20 slot-6 profile (dims UNVERIFIED, generic B-type class) [assessment]
POST_INSET = 2.0                 # posts sit inside the 2 mm panels
TOP_RAIL_Z = (FZ - SHEET_T - EXTR, FZ - SHEET_T)      # Derived 308-328
PART_X = {"left": (147.0, 149.0), "right": (323.0, 325.0)}   # (revised at integration) right partition moved +2
#   so the moving cam lever (X <= 320.0) keeps 3.0 mm (IR-5); left side: cover X 152.5 -> 3.5 mm   # well partitions in the 5-mm gaps between claims
#   (cold compartment X <= 145 | LOWER X 150-320 | bottles X >= 325), Derived from SPACE_CLAIMS

# Bay deck: carries LOWER_bay at its bottom face Z = 40 (interface request IR-1: bolt pattern below)
DECK = {"x": (LOWER_BAY[0][0], LOWER_BAY[1][0]), "y": (LOWER_BAY[0][1], LOWER_BAY[1][1]),
        "z": (LOWER_BAY[0][2] - 10.0, LOWER_BAY[0][2]), "material": "Al 6082-T6, 10 mm, fly-cut top"}
DECK_SPACERS_XY = [(170.0, 40.0), (300.0, 40.0), (170.0, 180.0), (300.0, 180.0), (235.0, 110.0)]  # [assessment]
DECK_BOLTS = [(x, y) for x in (165.0, 235.0) for y in (35.0, 110.0, 185.0)] + \
    [(305.0, y) for y in (35.0, 110.0, 185.0)]
#   (revised at integration) interface Rev B LOWER_MOUNT uses the 6 holes at X 165 / 305; the 3 holes at X 235 lie
#   under the M_d stage and are kept as spare tapped holes (IR-1)
DECK_BOLTS_USED = list(I.LOWER_MOUNT["bolts_dock"])
DECK_DOWELS = {"round": I.LOWER_MOUNT["dowel_round_dock"], "slot": I.LOWER_MOUNT["dowel_slot_dock"]}
DECK_TUBE_SLOTS = []   # tubes leave LOWER through side-wall glands (IR-2), not through the deck

# Interface request IR-2: tube glands in the LOWER_bay side walls (dock coords)
# (revised at integration) grommet windows in the well partitions around the exact LOWER line exits
# (interface Rev B LIQUID_LINE_EXITS: west Y 84-116, Z 108-114; east Y 80.5-110.5 Z 112-115 and P_a2 at Y 161.5)
GLAND_W = {"x": LOWER_BAY[0][0], "y": (82.0, 118.0), "z": (106.0, 116.0)}   # -X wall, west lines
GLAND_E = {"x": LOWER_BAY[1][0], "y": (78.0, 113.0), "z": (110.0, 117.0)}   # +X wall, P_rf, P_s, P_wo (bulkhead Z 124+)
GLAND_E2 = {"x": LOWER_BAY[1][0], "y": (190.0, 196.0), "z": (119.0, 125.0)}  # +X partition, P_a2 crossing at Y 193, Z 122
GLAND_C = {"x": LOWER_BAY[0][0], "y": I.PASS_THROUGHS["cable_window_W"]["y"],
           "z": I.PASS_THROUGHS["cable_window_W"]["z"]}                     # -X wall, power/motor cables (Rev B)
EXHAUST = I.PASS_THROUGHS["peltier_exhaust"]   # (revised at integration) LOWER Peltier duct outlet at Y 20 -> BASE
#   duct extension Y 2-20 + louvre in the front-bay panel (X 186-210, Z 118-144), <= 12.3 W (revised after review,
#   interface Rev C; Rev B 10.6 W)

# ------------------------------------------------------------------------------------------------ cold compartment
CC = CL["BASE_cold_compartment"]["box"]        # ((10,20,15),(145,200,220))
COLD_BOX = {"outer": ((24.0, 2.0, 17.0), (122.0, 150.0, 150.0)), "wall": 20.0,
            "door_y": (2.0, 20.0)}  # CHOICE-B5: PU foam 20 mm + 1.5 mm Al liner; door = insulated front wall at
#   Y 2-20 in the unclaimed front strip (DEV-B4 note); top at Z 150 leaves Z 150-220 for the SM-FL line, P_in sensor
#   and the S_b selection valve
K_INSUL = 0.025          # W/m/K, PU foam class value UNVERIFIED
LINER_T = 1.5            # [assessment]
COOLER = {  # Laird/Tark DA-024-24-02-00-00, V:LAIRD_TCA_CAT (direct-to-air: cold plate inside, sink + fan outside)
    "Q_W": 24.0, "V": 24.0, "I_A": 2.4, "mass": 0.3,
    "Lw": 80.0, "Ww": 60.0, "Hw": 56.0, "Lc": 60.0, "Wc": 40.0, "Hc": 14.0,
}
T_COLD = 5.0              # setpoint in the 4-8 degC window, docs/13 §5
T_AMB_IN_DOCK = 30.0      # worst-case air temperature around the box (dock interior) [assessment]
T_LAB = 22.0              # docs/13 §6.6 example

# ------------------------------------------------------------------------------------------------ pumps
CENTRIS = {"W": 44.5, "D": 68.8, "H": 184.2, "mass": 1.3, "V": 24.0, "I_peak": 2.5}   # V:TECAN_CENTRIS_P
PUMP_FRONT_ZONE = 22.0    # UNVERIFIED: valve head + syringe projecting from the front face (not on the page)
PUMP_PITCH = 60.0         # [assessment] 15.5 mm between bodies for tubes and fingers
PUMP_ORDER = ["S_b", "S_IC1", "S_IC2", "S_A", "S_RC"]   # CHOICE-B2 (index kept for lane offsets)
PUMP_X0 = 172.0           # centre of the first pump [assessment]
# (revised after review, docs/24 B1) S_IC1/S_IC2 moved from the rear row (X 232/292) to the FRONT of the left rear
# zone, beside the bay (X 54-144, Y 208-299, valves facing -Y toward the lane gap): tidal coils 140/160 -> ~77 uL
PUMP_REAR = ["S_b", "S_A", "S_RC"]
PUMP_FRONT_X = {"S_IC1": 76.25, "S_IC2": 121.75}        # bodies X 54.0-98.5 and 99.5-144.0 [assessment]
PUMP_FRONT_Y = {"zone": (208.0, 230.0), "body": (230.0, 230.0 + 68.8)}   # front zone (valve + syringe) toward -Y
PUMP_FRONT_SHELF = ((52.0, 207.0, 31.0), (145.0, 300.0, 37.0))
PUMP_BODY_Y = (325.0, 325.0 + CENTRIS["D"])             # front (valve) face toward +Y = rear service door
PUMP_SHELF_Z = (31.0, 37.0)   # 6 mm Al shelf on 4 elastomer isolators (Z 16-31), isolators UNVERIFIED
PUMP_SYRINGE_uL = {"S_b": 250, "S_A": 1000, "S_IC1": 1000, "S_IC2": 1000, "S_RC": 250}   # docs/13 §3.2.2, §5.1,
#   §6.1 (S_A volume [assessment]: 1 mL covers a 150 uL rinse fill in one stroke)
PUMP_VALVE = {  # ports per pump (Centris valve options, V:TECAN_CENTRIS_P); port use docs/13 §5.1, §6.1
    "S_b": "3-port: A1 in / coil out / bypass; coil -> 6-port selection valve SV_b (vial, P_b, waste, air, A1, spare)",
    "S_A": "4-port: A1 in, P_a, P_a2, waste (purge)",
    "S_IC1": "3-port: coil (P_d1), waste, A1 (prime)",
    "S_IC2": "3-port: coil (P_d2), waste, A1 (prime)",
    "S_RC": "3-port: P_s (via FS2), waste, A1 (prime)",
}

# ------------------------------------------------------------------------------------------------ bottles (CHOICE-B3)
DURAN_500 = {"d": 86.0, "h": 181.0, "cap_h": 25.0}    # search-result listings (Bartelt/DWK, ISO 4796-1); pages
#   not opened (403/truncated) -> UNVERIFIED
DURAN_1000 = {"d": 101.0, "h": 230.0, "cap_h": 25.0}  # same status, UNVERIFIED
TUBE_15 = {"d": 17.0, "h": 120.0}     # 15 mL conical tube class, UNVERIFIED
TUBE_2 = {"d": 11.0, "h": 45.0}       # 2 mL screw-cap microtube class, UNVERIFIED

# ------------------------------------------------------------------------------------------------ Gamry
GAMRY = CL["BENCH_gamry"]["box"]      # 9 x 19 x 27 cm (docs/18), 3 kg
GAMRY_MASS = 3.0                      # docs/18 §8 (gamry.com legacy page)
LEAD_MAX = 300.0                      # docs/13 §6.3 shielded leads <= 0.3 m
GAMRY_CELL_CABLE = 600.0              # V:GAMRY_CABLE_60
BULKHEAD = PT["gamry_cell_cable"]["dock"]   # (320, 107, 135)

# ------------------------------------------------------------------------------------------------ bench
ACQUITY = {"w": 343.0, "d": 712.0, "h": 711.0}   # V:WATERS_ICLASS_SPEC (I-Class BSM + SM-FTN + CH-A); the SM-FL
#   stack of this lab assumed the same footprint (I-Class PLUS SM-FL spec page returned 503) -> UNVERIFIED for SM-FL
STACK_GAP = 50.0          # [assessment] gap stack -> dock (PEEK line, air flow)
BENCH_DEPTH = 750.0       # UNVERIFIED typical lab bench
BENCH_HEIGHT = 900.0      # UNVERIFIED typical lab bench
SMFL_OUTLET_TO_DOCK = 200.0   # UNVERIFIED: SM-FL outlet fitting to the dock left wall entry (stack beside the dock)
P_IN_SENSOR_RANGE_BAR = (0.0, 25.0)   # (revised after review) 0.0635-mm line: 1.9 MPa over 0.52 m at 100 uL/min
#   (Derived, fluidics.dp_kPa); the sensor at the upstream end sees ~1.2 MPa -> 0-25 bar class, part UNVERIFIED

# ------------------------------------------------------------------------------------------------ tubing
FLUID = {"eta": 0.89e-3}      # Pa s, docs/13 §3.1

# ------------------------------------------------------------------------------------------------ air (revised at integration)
AIR_LID_KPA = I.PLUNGER["pilot_pressure_kPa"]      # 400 (interface Rev B; was 300 here)
AIR_SUPPLY_MIN_KPA = I.PLUNGER["air_supply_min_kPa"]   # 450 at the dock inlet; lab air spec 500-700 kPa [assessment]
AIR_LOW_SWITCH_KPA = 450.0                         # BASE supply switch (warning/fault before the lid switch trips at 350)
