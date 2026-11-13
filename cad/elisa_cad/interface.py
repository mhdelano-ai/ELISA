"""Cartridge A (docs/13 Revision B) <-> dock interface: single source of truth for interface geometry.

Units: mm, N, degrees, deg C. Importable with no side effects (pure constants and pure geometry helpers).
Owner: interface architect (docs/18). Downstream CAD modules READ this file; they never redefine a number in it.

Source tags on every value:
  docs/13 §x.y   number taken from docs/13 Revision B (or another docs file named)
  Derived        computed here from tagged inputs (arithmetic in the comment or in a helper below)
  CHOICE-n       open point decided in this round, listed in docs/18 §9 (user may overrule)
  DEV-n          deviation from docs/13 Rev B because its geometry cannot be built as written, docs/18 §10
  UNVERIFIED     not checked against a source in this session
  [assessment]   engineering judgement

Coordinate systems (docs/18 §2):
  CARD: origin at the lower-left corner of the card seen from the TOP (docs/13 §2.1); x along 75.5, y along 50;
        z = 0 is the foil (L0) underside = anvil top plane (datum C); +z up into the card.
  DOCK: origin at the front-left corner of the dock base at bench level; X to the operator's right, Y away from the
        operator (front -> back), Z up. Card axes are parallel to dock axes (no rotation):
        P_dock = P_card + CARD_ORIGIN_IN_DOCK.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

# =====================================================================================================
# 1. Coordinate systems
# =====================================================================================================
CARD_ORIGIN_IN_DOCK = (190.0, 75.0, 170.0)  # CHOICE-12: card lower-left-foil corner in dock coords
CARD_INSERTION_DIRECTION_DOCK = (0.0, 0.0, -1.0)  # CHOICE-11: card lowered vertically into the open nest,
#   top face up, x = 0 edge (reagent zone) on the operator's LEFT, y = 0 edge toward the operator.


def card_to_dock(p):
    """Card coords (x, y[, z]) -> dock coords. Pure translation (axes parallel)."""
    x, y = p[0], p[1]
    z = p[2] if len(p) > 2 else 0.0
    ox, oy, oz = CARD_ORIGIN_IN_DOCK
    return (x + ox, y + oy, z + oz)


def dock_to_card(p):
    ox, oy, oz = CARD_ORIGIN_IN_DOCK
    return (p[0] - ox, p[1] - oy, p[2] - oz)


# =====================================================================================================
# 2. Card envelope and layer stack
# =====================================================================================================
CARD_L = 75.5          # docs/13 §1.1 (x extent)
CARD_W = 50.0          # docs/13 §1.1 (y extent)
CARD_CORNER_R = 1.0    # CHOICE-13 [assessment]: outer corner radius of L3 (datum contacts stay >= 10 mm away)
LAMINATE_INSET = 0.2   # CHOICE-13: L0-L2 outline 0.2 mm inside the L3 outline, so only milled L3 touches datums

# z-ranges (bottom, top) in card coords
Z_L0 = (0.000, 0.140)   # COC floor foil 140 um, docs/13 §2.1
Z_L1 = (0.140, 0.315)   # COC channel sheet 0.175 mm, all channels through-cut, docs/13 §2.1
Z_L1B = (0.315, 0.340)  # 25 um die film, ONLY under the die (+0.15 seam cover, CHOICE-14), docs/13 §2.1
TPE_T = 0.40            # CHOICE-15: TPE ceiling 0.40 mm (docs/13 §2.1 range 0.3-0.5, thickness UNVERIFIED)
Z_L2 = (0.315, 0.315 + TPE_T)            # TPE ceiling = membrane of every valve and gate
L3_T = 5.5                               # COC upper body, docs/13 §2.1 (CNC-milled for C2, docs/16 §6.4)
Z_L3 = (Z_L2[1], Z_L2[1] + L3_T)         # (0.715, 6.215)
CARD_T = Z_L3[1]                         # Derived: 0.14 + 0.175 + 0.40 + 5.5 = 6.215 (docs/13 "~6.2")
CHANNEL_H = Z_L1[1] - Z_L1[0]            # 0.175, docs/13 §2.3
CELL_H = 0.200                           # docs/13 §2.7: L1 0.175 + L1b 0.025

LAYERS = {
    # name: (z_bottom, z_top, material, function)  -- docs/13 §2.1
    "L0_foil": (*Z_L0, "COC foil", "floor of all fluidics; magnet and Peltier side; pierced at liquid ports"),
    "L1_channel_sheet": (*Z_L1, "COC sheet", "all channels/lanes/RC/BW outline as through-cuts"),
    "L1b_die_film": (*Z_L1B, "25 um bonding film", "die bond, cell height 0.200; under die (+seam cover)"),
    "L2_TPE": (*Z_L2, "TPE sheet", "channel ceiling and membrane of all 21 valves/gates"),
    "L3_body": (*Z_L3, "COC, CNC-milled (C2)", "chambers, tanks, meter, plunger bores, die window, vents"),
    "L4_vents": (Z_L3[1] - 0.3, Z_L3[1], "PTFE membrane discs D4", "chamber/tank vents, recessed (CHOICE-16)"),
}

# Thermal zones in card x (docs/13 §2.1)
X_REAGENT = (0.0, 20.0)       # 4-8 degC
X_BREAK = (20.0, 24.0)        # L3 through-slot except two 3 mm bridges; L0-L2 continuous
X_ASSAY = (24.0, CARD_L)      # 25.0 +- 0.2 degC
BREAK_BRIDGES_Y = [(3.5, 6.5), (43.5, 46.5)]   # CHOICE-17: the two 3 mm L3 bridges of docs/13 §2.1

# =====================================================================================================
# 3. Datum scheme (card in the nest) -- CHOICE-1
# =====================================================================================================
# Primary  C: foil underside on the lapped anvil top plane z = 0 (anvil assay plate + reagent cold plate coplanar).
#             docs/13 §6.4 speaks of "three datum pads" AND of the foil resting on the anvil everywhere outside
#             windows and slot; the second is what the valves need (docs/13 §2.1), so the whole anvil top is datum C.
# Secondary A: card front edge y = 0 (L3 side face) against two fixed pins.
# Tertiary B: card left edge x = 0 (L3 side face) against one fixed pin.
DATUM_PIN_D = 4.0                         # hardened steel, protrudes 5.0 mm above z = 0 [assessment]
DATUM_PIN_PROTRUSION = 5.0
DATUM_A_PINS = [(12.0, -DATUM_PIN_D / 2), (63.0, -DATUM_PIN_D / 2)]   # touch y = 0 at x = 12, 63
DATUM_B_PIN = (-DATUM_PIN_D / 2, 25.0)                               # touches x = 0 at y = 25
PUSHERS = {  # spring plungers pushing the card onto datums A and B (before clamping) [assessment]
    "push_A": {"contact": (37.75, CARD_W), "direction": (0, -1), "force_N": 5.0},
    "push_B": {"contact": (CARD_L, 25.0), "direction": (-1, 0), "force_N": 5.0},
}
TOL = {
    "anvil_flatness": 0.02,          # UNVERIFIED target; sets the magnet gap tolerance 0.16 +- 0.05 (docs/13 §6.2)
    "card_edge_to_feature": 0.05,    # milled L3, [assessment]
    "L1_to_L3_registration": 0.05,   # REQUIRED at the cell and J clusters (stub rule); laser-cut + pinned
                                     # lamination, achievability UNVERIFIED (card agent, docs/18 §12)
    "die_in_window": 0.05,           # docs/13 §2.7 (UNVERIFIED)
    "datum_pin_position": 0.01,      # [assessment]
    "head_to_nest": 0.03,            # lid head located on nest by two guide pins [assessment]
    "pin_in_card_bore_radial_clearance_min": 0.15,  # Derived: (1.5-1.2)/2; (1.2-0.8)/2 = 0.2
}

# =====================================================================================================
# 4. Chambers, tanks, meter, die, cell (card coords)
# =====================================================================================================
@dataclass(frozen=True)
class Bore:
    name: str
    center: tuple
    d: float = 0.0          # round bore diameter (0 if rectangular)
    size: tuple = (0, 0)    # rectangular footprint (x, y)
    z: tuple = (0.0, 0.0)   # open volume z-range
    note: str = ""


CHAMBER_ROOF_T = 0.5   # CHOICE-16: chamber/tank cavities are blind from below in L3 with a 0.5 mm roof
IC1 = Bore("IC1", (40.0, 38.0), d=8.0, z=(Z_L0[1], CARD_T - CHAMBER_ROOF_T),
           note="docs/13 §2.3; 185 uL working, fill 3.68 mm; total Derived pi*4^2*5.575 = 280 uL (docs/13 ~290)")
IC2 = Bore("IC2", (40.0, 12.0), d=8.0, z=IC1.z, note="docs/13 §2.3")
RCJ = Bore("RCj", (8.0, 38.0), size=(10.0, 10.0), z=(Z_L0[1], CARD_T - CHAMBER_ROOF_T),
           note="conjugate tank, docs/13 §2.3 (3-13, 33-43), 0.50 mL + 0.06 mL in L1/L2")
RS = Bore("RS", (68.0, 10.0), size=(12.0, 12.0), z=(Z_L0[1], CARD_T - CHAMBER_ROOF_T),
          note="HQDP tank, docs/13 §2.3 (62-74, 4-16)")
MC = Bore("MC", (16.0, 30.0), size=(2.0, 1.0), z=(Z_L0[1], Z_L0[1] + 5.0),
          note="conjugate meter 10.0 uL = 2.0 x 1.0 x 5.0 from foil to PTFE stop (docs/13 §2.3); "
               "L3 cavity depth Derived 5.0 - 0.575 = 4.425 (CHOICE-16)")
BW = Bore("BW", (57.85, 17.2), size=(2.5, 2.5), z=(Z_L0[1], Z_L2[1]),
          note="bead-waste pocket 2.5 x 2.5 x 0.575 = 3.6 uL (docs/13 §2.3); MOVED from (56.8, 20.5): DEV-5")
CHAMBERS = {b.name: b for b in (IC1, IC2, RCJ, RS, MC, BW)}

# Vents (L4 PTFE discs D4, recessed in D4.4 x 0.3 counterbores in the L3 top, CHOICE-16) and vent holes D2
VENTS = {
    "vent_IC1": (40.0, 38.0),   # docs/13 §3.2.1 (vent in the roof)
    "vent_IC2": (40.0, 12.0),
    "vent_RS": (70.0, 13.0),    # docs/13 §2.1 L4 "tank vents"
}
VENT_DISC_D = 4.0               # docs/13 §2.1
VENT_POCKET_D_LID = 6.0         # lid clearance pocket over each vent, vented sideways (CHOICE-16)

# Electrode die (docs/13 §2.7) -- face down on L1b
DIE_X = (55.0, 61.0)
DIE_Y = (23.35, 33.35)
DIE_T = 0.70                    # UNVERIFIED ("foundry standard", docs/13 §2.1); press-pad stroke covers 0.5-1.1
DIE_Z = (Z_L1B[1], Z_L1B[1] + DIE_T)
DIE_WINDOW_CLEAR = 0.05         # L3/L2 window = die outline + 0.05 (TPE cut-out die + 0.10, CHOICE-14)
DIE_DATUM_EDGES = ("x = 55.0 for y 27.0-33.35", "y = 33.35")  # CHOICE-14: notch-free window edges
# Readout cell (docs/13 §2.3, §3.5.1)
RC_CENTER = (56.8, 25.0)
RC_SIZE = (2.6, 2.0)            # x 55.5-58.1, y 24.0-26.0, height 0.200
WE2_CHANNEL = {"x": (58.1, 61.0), "y_c": 25.0, "w": 1.0, "h": 0.05}   # docs/13 §2.3
CER_POCKET = {"x": (55.3, 55.7), "y": (23.45, 23.85)}                 # 0.4 x 0.4, DEV-2 (moved to x 55.5)
CER_NECK = {"x": (55.5, 55.9), "y": (23.85, 24.0), "h": 0.15}          # 0.4 wide x 0.15 long, docs/13 §2.3
G3_FINGER = {"x": (55.0, 55.5), "y_c": 25.0, "w": 0.5}                # docs/13 §2.3 (0.5 mm)
G4_FINGER = {"x_c": 57.85, "y": (23.35, 24.0), "w": 0.5}               # docs/13 §2.3 (0.65 mm); x DEV-2
# Pads on the die's lower face, inside the dry contact window (docs/13 §2.7). Layout 2 x 3: CHOICE-9
CONTACT_WINDOW = {"x": (55.3, 60.7), "y": (29.8, 33.2)}                # docs/13 §2.2/§2.7 (through L1 and L0)
PAD_SIZE = (1.2, 1.0)
PADS = {
    "WE1": (56.2, 30.6), "WE2": (58.0, 30.6), "CE": (59.8, 30.6),
    "RE": (56.2, 32.4), "LOOP_A": (58.0, 32.4), "LOOP_B": (59.8, 32.4),
}

# =====================================================================================================
# 5. Channel network (L1 through-cuts). Polylines in card coords, width w, height h.
#    The network is PLANAR (single cut layer): checked in docs/18 §11. Lanes are generated below.
# =====================================================================================================
LANE_W = 0.5        # docs/13 §2.3
LINE_W = 0.4        # bead / conjugate / supply lines, docs/13 §2.3
STUB_W = 0.3        # V14/V15 stubs, docs/13 §3.6


def _arc_pts(cx, cy, r, a0, a1, step_deg=5.0):
    n = max(2, int(abs(a1 - a0) / step_deg) + 1)
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / (n - 1))),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / (n - 1)))) for i in range(n)]


def _lane(start, mirror=False, R=3.0, phi=77.04555995, L=9.28319381, end_head=-40.0):
    """Wash lane from the bore wall (heading +x) to J, arriving at heading end_head (DEV-3).
    Arc cw R to heading -phi, straight L, arc ccw R to end_head. phi, L solved so the end point is J = (50, 25)
    (scratch wl.py, fsolve). Length Derived = R*phi + L + R*(phi + end_head) = 15.257 mm (docs/13: 15.0)."""
    s = -1.0 if mirror else 1.0
    x0, y0 = start
    pts = []
    # arc 1: centre below (above if mirrored) the start
    c1 = (x0, y0 - s * R)
    a_start = 90.0 * s
    a_end = a_start - s * phi
    pts += _arc_pts(c1[0], c1[1], R, a_start, a_end)
    h = -s * phi
    x1, y1 = pts[-1]
    x2, y2 = x1 + L * math.cos(math.radians(h)), y1 + L * math.sin(math.radians(h))
    pts.append((x2, y2))
    # arc 2: turning back to end_head (ccw for the upper lane, cw for the mirrored lane)
    dh = s * (phi + end_head)
    # centre of a left turn (ccw) from heading h is at h + 90 deg; right turn at h - 90 deg
    ang_c = h + (90.0 if s > 0 else -90.0)
    c2 = (x2 + R * math.cos(math.radians(ang_c)), y2 + R * math.sin(math.radians(ang_c)))
    a_from = ang_c + 180.0
    pts += _arc_pts(c2[0], c2[1], R, a_from, a_from + dh)[1:]
    return pts


def polyline_length(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


J = (50.0, 25.0)                       # docs/13 §2.3
WL1 = _lane((44.0, 38.0))              # docs/13 §2.3 (44,38)->(50,25); geometry DEV-3
WL2 = _lane((44.0, 12.0), mirror=True)
WL1[-1] = J
WL2[-1] = J
WLC = [J, (G3_FINGER["x"][0], 25.0)]   # J -> die edge (x 55.0); docs/13 §2.3 WLc 4.4 mm to G3 + finger
J_HALF_ANGLE = 40.0                    # DEV-3: lanes meet WLc at +-40 deg (drag fillet R3 deviates 0.19 mm)

# Drag trajectories (M_d centre path in card coords) -- docs/13 §3.3.3; fillet R 3 at J (DEV-3)
FUNNEL = {"IC1": [(42.0, 38.0), (44.0, 38.0)], "IC2": [(42.0, 12.0), (44.0, 12.0)]}  # 2.5 -> 0.5 wide, docs/13 §2.3
FUNNEL_APEX = {"IC1": (42.5, 38.0), "IC2": (42.5, 12.0)}  # pellet held at x_c + 2.5 (docs/13 §2.3)


def _fillet_J(lane, R=3.0, n=9):
    """Round the 40 deg kink at J (lane -> WLc) for the magnet trajectory: quadratic Bezier with control point J
    and legs t = R*tan(20 deg) = 1.092 mm (approximates an R 3 fillet; max deviation from the lane centrelines
    ~0.19 mm < lane half-width 0.25, checked in docs/18 §11). Returns the trajectory up to the WLc leg."""
    t = R * math.tan(math.radians(J_HALF_ANGLE / 2.0))
    body = [p for p in lane[:-1] if math.dist(p, J) > t + 1e-6]
    # entry point on the lane polyline at arc-length t before J
    acc, p_in = 0.0, lane[-2]
    for i in range(len(lane) - 1, 0, -1):
        seg = math.dist(lane[i], lane[i - 1])
        if acc + seg >= t:
            f = (t - acc) / seg
            p_in = (lane[i][0] + f * (lane[i - 1][0] - lane[i][0]), lane[i][1] + f * (lane[i - 1][1] - lane[i][1]))
            break
        acc += seg
    p_out = (J[0] + t, J[1])
    bez = [((1 - u) ** 2 * p_in[0] + 2 * u * (1 - u) * J[0] + u ** 2 * p_out[0],
            (1 - u) ** 2 * p_in[1] + 2 * u * (1 - u) * J[1] + u ** 2 * p_out[1]) for u in
           [k / (n - 1) for k in range(n)]]
    return body + bez


DRAG_PATH = {
    "IC1": [FUNNEL_APEX["IC1"]] + _fillet_J(WL1) + [RC_CENTER],
    "IC2": [FUNNEL_APEX["IC2"]] + _fillet_J(WL2) + [RC_CENTER],
}
BEAD_OUT_PATH = [RC_CENTER, (57.85, 25.0), (57.85, 21.5)]   # DEV-5: axis-aligned, stops 3 mm short of BW
GATHER_PASSES = {  # docs/13 §3.3.3: start (x_c-3.5, +2 / -2 / 0) -> funnel apex (x_c+2.5, 0), relative to centre
    "pass1": [(-3.5, 2.0), (2.5, 0.0)], "pass2": [(-3.5, -2.0), (2.5, 0.0)], "pass3": [(-3.5, 0.0), (2.5, 0.0)]}
M_D_HOLD_POS = RC_CENTER        # DEV-4: M_d holds the pellet under the RC (accumulation + READ)
M_D_PARK_POS = (50.0, 25.0)     # CHOICE-6: park under J, lowered 8 mm

# --- Supply network (valve island I: ladder between the two inlet rails H1 = C1 and H2 = C2) -- DEV-1
H1 = [(26.4, 31.0), (39.0, 31.0), (39.0, 34.6)]   # C1 swept inlet: head (after V6) -> bore wall at (39, 34.13)
H2 = [(26.4, 19.0), (39.0, 19.0), (39.0, 15.4)]   # C2
M_IN = [(34.2, 27.3), (34.2, 28.9), (30.5, 28.9), (30.5, 21.1), (34.2, 21.1), (34.2, 23.3)]  # P_in ... V3 ... P_byp

CHANNELS = {
    # name: dict(pts, w, h, src)
    "WL1": dict(pts=WL1, w=LANE_W, h=CHANNEL_H, src="docs/13 §2.3; shape DEV-3"),
    "WL2": dict(pts=WL2, w=LANE_W, h=CHANNEL_H, src="docs/13 §2.3; shape DEV-3"),
    "WLc": dict(pts=WLC, w=LANE_W, h=CHANNEL_H, src="docs/13 §2.3"),
    "G3_finger": dict(pts=[(55.0, 25.0), (55.5, 25.0)], w=0.5, h=CELL_H, src="docs/13 §2.3 (under die)"),
    "WE2_link": dict(pts=[(58.1, 25.0), (61.0, 25.0)], w=1.0, h=0.05, src="docs/13 §2.3 WE2 channel 0.05 high"),
    "G4_lane": dict(pts=[(57.85, 24.0), (57.85, BW.center[1] + 1.25)], w=LANE_W, h=CHANNEL_H,
                    src="docs/13 §2.3 G4 finger 0.65 in die; rest to BW (DEV-5)"),
    "fun1": dict(pts=FUNNEL["IC1"], w=0.5, h=CHANNEL_H, src="docs/13 §2.3 funnel 2.5->0.5 (open above)"),
    "fun2": dict(pts=FUNNEL["IC2"], w=0.5, h=CHANNEL_H, src="docs/13 §2.3"),
    "C1_H1": dict(pts=H1, w=LANE_W, h=CHANNEL_H, src="docs/13 §2.3 C1 0.5 wide; length DEV-1"),
    "C2_H2": dict(pts=H2, w=LANE_W, h=CHANNEL_H, src="docs/13 §2.3 C2; length DEV-1"),
    "M_in": dict(pts=M_IN, w=LANE_W, h=CHANNEL_H, src="docs/13 §2.3 M_in 0.5 wide; route DEV-1"),
    # rungs and bridges (valve tips sit on these segments)
    "A1_rung": dict(pts=[(28.0, 30.75), (28.0, 19.25)], w=LINE_W, h=CHANNEL_H, src="DEV-1 (S_A -> V17/V18)"),
    "bead_rung": dict(pts=[(37.5, 30.75), (37.5, 19.25)], w=LINE_W, h=CHANNEL_H, src="DEV-1 (P_b -> V4/V5)"),
    "V1_bridge": dict(pts=[(31.0, 30.75), (31.0, 29.15)], w=LINE_W, h=CHANNEL_H, src="docs/13 §2.6 stub rule"),
    "V2_bridge": dict(pts=[(31.0, 19.25), (31.0, 20.85)], w=LINE_W, h=CHANNEL_H, src="docs/13 §2.6"),
    "conj_line": dict(pts=[(17.0, 30.0), (24.75, 30.0), (24.75, 31.0), (26.4, 31.0)], w=LINE_W, h=CHANNEL_H,
                      src="docs/13 §2.3 (MC -> V6); crosses the thermal break under the L3 slot"),
    "conj_leg2": dict(pts=[(24.75, 30.0), (24.75, 19.0), (26.4, 19.0)], w=LINE_W, h=CHANNEL_H,
                      src="docs/13 §2.3 (MC -> V7)"),
    "RCj_to_MC": dict(pts=[(12.0, 33.0), (12.0, 30.0), (15.0, 30.0)], w=LINE_W, h=CHANNEL_H,
                      src="docs/13 §2.3 RCj -> V8 -> MC"),
    "nozzle1": dict(pts=[(29.5, 41.0), (37.6, 41.0)], w=0.5, h=CHANNEL_H,
                    src="docs/13 §2.3 nozzle 0.5 wide, tangential at the -x wall (offset +3.0 from centre)"),
    "nozzle2": dict(pts=[(29.5, 9.0), (37.6, 9.0)], w=0.5, h=CHANNEL_H, src="docs/13 §2.3"),
    "V11_line": dict(pts=[(51.3, 36.5), (51.3, 25.25)], w=LINE_W, h=CHANNEL_H,
                     src="docs/13 §3.3.6 S_A -> V11 -> WLc tee; port P_a2 is DEV-6"),
    "V12_waste": dict(pts=[(52.9, 25.25), (52.9, 35.5), (66.0, 35.5)], w=LINE_W, h=CHANNEL_H,
                      src="docs/13 §2.5 V12 -> P_wo"),
    "V14_out": dict(pts=[(61.0, 25.0), (63.0, 25.0), (63.0, 20.5)], w=STUB_W, h=CHANNEL_H,
                    src="docs/13 §3.6 stub 0.3 wide; -> P_s"),
    "V16_out": dict(pts=[(59.1, 17.2), (63.0, 17.2), (63.0, 20.5)], w=LINE_W, h=CHANNEL_H, src="BW -> V16 -> P_s"),
    "RS_feed": dict(pts=[(55.5, 23.45), (55.5, 12.5), (62.0, 12.5)], w=STUB_W, h=CHANNEL_H,
                    src="docs/13 §3.5.5 RS -> V15 -> pocket; route DEV-2"),
}

# =====================================================================================================
# 6. Valves and gates (21): plunger points, tip, class, fail state, force -- docs/13 §4, CHOICE-2/3, DEV-1/2/3
# =====================================================================================================
@dataclass(frozen=True)
class Valve:
    id: str
    xy: tuple                 # plunger axis = tip centre, card coords
    tip_d: float              # flat tip diameter (seal land)
    pin_d: float              # pin shank diameter in the card bore and the dock guide
    bore_d: float             # L3 bore diameter (merged into a notch where noted)
    klass: str                # "anvil" (<= 3 N) | "slot" (<= 1.5 N over the drag slot) | "cold" (reagent plate)
    fail: str                 # "closed" (spring closes) | "open" (V3)
    f_close_nom: float        # spring preload at the closed position, N (CHOICE-3)
    f_close_max: float        # limit, N (docs/13 §4)
    function: str
    src: str


def _v(id_, xy, klass, function, src, tip=1.0, fail="closed"):
    pin = 1.2 if tip >= 1.0 else 0.8
    bore = 1.5 if tip >= 1.0 else 1.2
    fmax = 1.5 if klass == "slot" else 3.0
    fnom = 1.2 if klass == "slot" else 2.5
    return Valve(id_, xy, tip, pin, bore, klass, fail, fnom, fmax, function, src)


def _point_at_arclength_from_end(pts, s):
    """Point on polyline pts at arc length s measured back from its last point (pure)."""
    acc = 0.0
    for i in range(len(pts) - 1, 0, -1):
        seg = math.dist(pts[i], pts[i - 1])
        if acc + seg >= s:
            f = (s - acc) / seg
            return (round(pts[i][0] + f * (pts[i - 1][0] - pts[i][0]), 3),
                    round(pts[i][1] + f * (pts[i - 1][1] - pts[i][1]), 3))
        acc += seg
    return pts[0]


GATE_J_ARCLEN = 1.2   # DEV-3: G1/G2 tip centres 1.2 mm (along the lane) before J -> (49.26, 25.93)/(49.26, 24.07);
#                       lane walls separate 0.55 mm before J (scratch check) -> stub 1.2 - 0.4 - 0.55 = 0.25 mm

# tip centre = trunk wall + 0.3 stub + tip radius (docs/13 §2.6); rails at y 31.0 / 19.0, wall 30.75 / 19.25
VALVES = {v.id: v for v in [
    _v("V1", (31.0, 29.95), "anvil", "M_in -> C1 (sample)", "docs/13 §4; bridge DEV-1"),
    _v("V2", (31.0, 20.05), "anvil", "M_in -> C2 (sample)", "docs/13 §4; bridge DEV-1"),
    _v("V3", (33.0, 21.1), "anvil", "M_in -> bypass P_byp (in-line)", "docs/13 §4 fail-OPEN", fail="open"),
    _v("V4", (37.5, 29.95), "anvil", "bead line -> C1", "docs/13 §4"),
    _v("V5", (37.5, 20.05), "anvil", "bead line -> C2", "docs/13 §4"),
    _v("V6", (25.9, 31.0), "anvil", "meter MC -> C1 (in-line at rail head)", "docs/13 §4; DEV-1"),
    _v("V7", (25.9, 19.0), "anvil", "meter MC -> C2 (in-line at rail head)", "docs/13 §4; DEV-1"),
    _v("V8", (12.0, 31.8), "cold", "RCj -> MC (fill-to-vent)", "docs/13 §4"),
    _v("V9", (32.5, 41.0), "anvil", "IC1 nozzle <-> P_d1 (tidal/drain)", "docs/13 §4"),
    _v("V10", (32.5, 9.0), "anvil", "IC2 nozzle <-> P_d2", "docs/13 §4"),
    _v("V11", (51.3, 25.95), "slot", "S_A (P_a2) -> WLc tee", "docs/13 §4; tee 1.3 mm after J (docs/13: 1.5)", tip=0.8),
    _v("V12", (52.9, 25.95), "slot", "WLc tee -> P_wo", "docs/13 §4", tip=0.8),
    _v("V14", (61.75, 25.0), "anvil", "WE2 channel -> P_s", "docs/13 §4; stub 0.35 + die tol, DEV-2", tip=0.8),
    _v("V15", (55.5, 22.6), "anvil", "RS -> CE/RE pocket (substrate inlet)",
       "docs/13 §4; over the anvil but only 0.25 mm from the slot edge (CHOICE-5 exception); DEV-2", tip=0.8),
    _v("V16", (60.55, 17.2), "anvil", "BW -> P_s", "docs/13 §4"),
    _v("V17", (28.0, 29.95), "anvil", "S_A (P_a) -> C1", "docs/13 §4"),
    _v("V18", (28.0, 20.05), "anvil", "S_A (P_a) -> C2", "docs/13 §4"),
    _v("G1", _point_at_arclength_from_end(WL1, GATE_J_ARCLEN), "slot", "WL1 <-> J",
       "docs/13 §4; on WL1 1.2 mm (arc length) before J; stub 0.25 (DEV-3)", tip=0.8),
    _v("G2", _point_at_arclength_from_end(WL2, GATE_J_ARCLEN), "slot", "WL2 <-> J",
       "docs/13 §4; mirror of G1 (DEV-3)", tip=0.8),
    _v("G3", (54.25, 25.0), "slot", "WLc <-> cell", "docs/13 §4; seal 0.35 from die edge, DEV-2", tip=0.8),
    _v("G4", (57.85, 22.6), "slot", "cell <-> BW", "docs/13 §4; DEV-2", tip=0.8),
]}
assert len(VALVES) == 21  # docs/13 §4: 17 valves + 4 gates

# Plunger interface (CHOICE-2): pin guided in the lid head, spring-closed, lifted pneumatically via a yoke
PLUNGER = {
    "principle": "spring-closed pin; opened by a single-acting pneumatic cylinder lifting the pin head via a "
                 "yoke; V3 inverted (spring lifts, cylinder closes through a 2.5 N force-limiting spring)",
    "stroke_pin": 0.8,                 # CHOICE-2: >= 0.5 required (docs/13 §6.2); 0.175 + TPE + 0.3 clearance
    "tip_z_closed": Z_L1[0] + 0.03,    # Derived: TPE pressed onto the foil top (z 0.14) less ~30 um residual TPE
    "tip_z_open": Z_L2[1] + 0.3,       # Derived: 0.3 mm above the TPE top (1.015)
    "pin_extension_limit_below_open": 1.0,  # collar stops the pin 0.2 mm below 'closed' when no card is present
    "tip_edge_chamfer": 0.05,          # flat land, edge-broken [assessment]
    "card_bore_lead_in": 0.3,          # 0.3 x 45 deg chamfer at the L3 top of each bore (CHOICE-2)
    "actuation_time_max_s": 0.2,       # docs/13 §4
    "pilot_pressure_kPa": 300.0,       # CHOICE-2 [assessment]; pilot valves rated >= 400 kPa, to be selected
    "cylinder_bore": 5.0,              # CHOICE-2: custom block, O-ring piston; lift force Derived 300 kPa x 19.6
                                       # mm^2 = 5.9 N vs spring 2.5 N + friction <= 1.5 N [assessment]
    "cylinder_pitch_min": 9.0,         # CHOICE-2: bore 5 + walls/seals
    "pin_pitch_min": {"0.8-0.8": 1.4, "0.8-1.2": 1.6, "1.2-1.2": 1.8},   # shank/2 + shank/2 + 0.6 web [assessment]
    "position_feedback": "per-yoke sensor, type to be selected (UNVERIFIED); minimum: pilot-line pressure switch",
}
# Fan-out (CHOICE-2): cylinders on a 9.0 mm grid (offset x 0.0 / y 0.5 from the card origin) in a block above the
# head; each cylinder lifts its pin through a horizontal yoke blade (1.0 wide x 4.0 tall) at one of two tiers.
# Assignment = minimum sum of squared offsets (scipy linear_sum_assignment, scratch act.py); tiers from a
# precedence graph (blade over another pin's hook -> higher; blade under another cylinder's rod -> lower;
# crossing blades -> different tiers): acyclic, 2 tiers. Forbidden sites: press-pad stem (58, 31.4) r 7.5,
# gas lines P_c, P_mv r 5. xy in card coords.
CYLINDERS = {
    "V1": {"xy": (32.0, 32.5), "tier": 0},
    "V2": {"xy": (32.0, 14.5), "tier": 0},
    "V3": {"xy": (32.0, 23.5), "tier": 0},
    "V4": {"xy": (41.0, 32.5), "tier": 0},
    "V5": {"xy": (41.0, 14.5), "tier": 0},
    "V6": {"xy": (23.0, 41.5), "tier": 0},
    "V7": {"xy": (23.0, 14.5), "tier": 0},
    "V8": {"xy": (5.0, 32.5), "tier": 0},
    "V9": {"xy": (32.0, 41.5), "tier": 0},
    "V10": {"xy": (32.0, 5.5), "tier": 0},
    "V11": {"xy": (50.0, 23.5), "tier": 1},
    "V12": {"xy": (50.0, 32.5), "tier": 0},
    "V14": {"xy": (68.0, 32.5), "tier": 0},
    "V15": {"xy": (59.0, 14.5), "tier": 0},
    "V16": {"xy": (68.0, 14.5), "tier": 0},
    "V17": {"xy": (23.0, 32.5), "tier": 1},
    "V18": {"xy": (23.0, 23.5), "tier": 0},
    "G1": {"xy": (41.0, 23.5), "tier": 0},
    "G2": {"xy": (50.0, 14.5), "tier": 0},
    "G3": {"xy": (59.0, 23.5), "tier": 1},
    "G4": {"xy": (68.0, 23.5), "tier": 0},
}

HEAD_Z = {  # card z of the lid-head stack (CHOICE-2/7); dock Z = card z + 170.0
    "heater_block": (CARD_T, CARD_T + 10.0),           # Al, 25 degC, pin guide bushings, bears on L3 top
    "pin_spring_zone": (CARD_T + 10.0, 24.5),          # compression spring per pin, seats on the heater block
    "pin_head_closed_top": 25.0,                       # head/collar top when the valve is closed (+0.8 open)
    "yoke_tier_0": (27.0, 31.0), "yoke_tier_1": (32.0, 36.0),
    "cylinder_block": (38.0, 68.0),                    # custom block, D5 bores, single acting, spring return
    "cover_top_max": 125.0,                            # = UPPER claim top (dock Z 295)
}
YOKE = {"blade_w": 1.0, "blade_h": 4.0, "plan_clearance_min": 0.3, "hook": "slot under the pin head, lifts only"}

# Card bores: L3 bores coaxial with each valve; notches merge with the die window for G3, G4, V14, V15 (DEV-2);
# G1/G2 bores (D1.2 at 1.6 pitch) merged into one 1.2 x 2.8 slot; V11/V12 likewise (1.2 x 2.8).
MERGED_BORES = {"G1G2": ("G1", "G2"), "V11V12": ("V11", "V12")}
DIE_NOTCHED_BORES = ("G3", "G4", "V14", "V15")

# =====================================================================================================
# 7. Ports (card side holes through L0+L1 D1.0, docs/13 §2.5) and dock face seals
# =====================================================================================================
@dataclass(frozen=True)
class Port:
    id: str
    xy: tuple
    kind: str        # "liquid" (from below, anvil seal) | "gas" (top, lid seal)
    connects: str
    dock: str
    src: str


PORTS = {p.id: p for p in [
    Port("P_in", (34.2, 27.3), "liquid", "SM-FL outlet -> M_in", "1/16in PEEK >= 0.3 m from SM-FL", "docs/13 §2.5"),
    Port("P_byp", (34.2, 23.3), "liquid", "V3 -> waste", "waste line with air gap", "docs/13 §2.5"),
    Port("P_b", (37.5, 25.0), "liquid", "bead line -> V4/V5", "S_b outlet line 0.25 ID", "docs/13 §2.5"),
    Port("P_a", (28.0, 25.0), "liquid", "S_A -> V17/V18", "S_A (dispense only), valve port 1", "docs/13 §2.5"),
    Port("P_a2", (51.3, 36.5), "liquid", "S_A -> V11", "S_A (dispense only), valve port 2", "DEV-6 (new)"),
    Port("P_d1", (29.5, 41.0), "liquid", "V9 <-> IC1 nozzle", "60 uL FEP coil -> S_IC1", "docs/13 §2.5"),
    Port("P_d2", (29.5, 9.0), "liquid", "V10 <-> IC2 nozzle", "60 uL FEP coil -> S_IC2", "docs/13 §2.5"),
    Port("P_wo", (66.0, 35.5), "liquid", "V12 -> waste", "waste", "docs/13 §2.5"),
    Port("P_s", (63.0, 20.5), "liquid", "V14, V16 -> S_RC", "S_RC (pull only)", "docs/13 §2.5"),
    Port("P_rf", (72.5, 5.5), "liquid", "HQDP bottle -> RS floor", "pressure fill at insertion", "docs/13 §2.5"),
    Port("P_cf", (5.0, 35.0), "liquid", "conjugate bottle -> RCj floor", "pressure fill (cooled)", "docs/13 §2.5"),
    Port("P_c", (8.0, 41.5), "gas", "RCj headspace", "pressure channel 1", "docs/13 §2.5"),
    Port("P_mv", (16.0, 30.0), "gas", "MC stop vent / air push", "pressure channel 2", "docs/13 §2.5"),
]}
PORT_HOLE_D = 1.0          # docs/13 §2.5 (0.24 uL Derived pi/4*1^2*0.315)
# Liquid face seal in the anvil (CHOICE-4): 1/16" PEEK tube bonded in a replaceable PEEK port insert, tube end
# flush with z = 0 under the port hole; flat elastomer annulus around the tube end in a counterbore.
FACE_SEAL = {
    "tube_od": 1.5875,             # 1/16 in
    "gasket_id": 1.7, "gasket_od": 3.3, "gasket_t": 0.50,
    "counterbore_depth": 0.38,     # compression 0.12 mm = 24 % [assessment]
    "material": "FFKM or EPDM sheet, laser-cut (to be selected; HQ/Tween compatibility UNVERIFIED)",
    "force_per_seal_N": (3.0, 10.0),   # [assessment, UNVERIFIED]: 0.5-1.5 MPa x 6.3 mm^2 annulus
    "port_pitch_min": 3.6,         # gasket OD + 0.3 web
    "insert_d": 3.3,               # gasket seat diameter = keep-out for valve tips (+0.3)
}
GAS_SEAL_LID = {"id": 5.0, "od": 7.0, "t": 1.0, "compression": 0.25, "force_N": 5.0}   # CHOICE-4 [assessment]

# =====================================================================================================
# 8. Anvil openings (dock side, plan view, card coords) -- docs/13 §2.2 zoning
# =====================================================================================================
WINDOW_SIZE = 11.4          # DEV-4: square (docs/13: D12) -- 10x10 M_c diagonal 14.1 does not pass a D12 bore
WINDOW_CORNER_R = 1.0
WINDOWS = {"W1": IC1.center, "W2": IC2.center}
SLOT_W = 4.0                # docs/13 §2.2 (drag slot 4 mm)
SLOT_W_BEADOUT = 3.4        # DEV-5: bead-out leg (axis-aligned) narrowed to 3.4 (holder 2.6 + 2 x 0.4)
SLOT_W_WLC = 3.4           # DEV-5: straight, axis-aligned J -> RC part narrowed to 3.4 (holder 2.6 + 2 x 0.4)
SLOT_CENTERLINES = {        # buffers of these polylines (round caps) form the slot; widths in SLOT_WIDTHS
    "slot_IC1": [FUNNEL_APEX["IC1"]] + WL1,
    "slot_IC2": [FUNNEL_APEX["IC2"]] + WL2,
    "slot_WLc": [J, RC_CENTER],
    "slot_beadout": BEAD_OUT_PATH,
}
SLOT_WIDTHS = {"slot_IC1": SLOT_W, "slot_IC2": SLOT_W, "slot_WLc": SLOT_W_WLC, "slot_beadout": SLOT_W_BEADOUT}
M_W_RECESS = {"center": BW.center, "size": (3.4, 3.4), "depth": 3.2}   # M_w 3x3x3 top at z = -0.16
ANVIL_CONTACT_OPENING = {"x": (55.3, 60.7), "y": (29.8, 33.2)}          # = card contact window, docs/13 §2.7
ANVIL_TOP_PLATE_T_THIN = 5.0   # CHOICE-5: over the magnet bay (card x 31-64): 5 mm non-magnetic Al plate
ANVIL_THICK_ZONES = {          # CHOICE-5: port inserts need depth; no magnet below these zones
    "island_boss": {"x": (24.0, 39.5), "y": (19.0, 31.0), "t": 15.0},
    "west_strip": {"x": (24.0, 33.5), "y": (0.0, 50.0), "t": 15.0},
    "east_block": {"x": (62.5, 75.5), "y": (0.0, 50.0), "t": 15.0},
    "P_a2_boss": {"x": (49.0, 53.5), "y": (34.5, 39.0), "t": 15.0},
}
VALVE_TIP_EDGE_MARGIN = 0.5    # CHOICE-5: tip edge >= 0.5 from any anvil opening/gasket (V15 exception 0.25)

# =====================================================================================================
# 9. Magnets (docs/13 §3.3.1; mag_b.py: B_r 1.3 T UNVERIFIED, gap 0.16 + foil 0.14 = bead plane 0.30)
# =====================================================================================================
MAGNET_GAP = 0.16              # docs/13 §6.2, +-0.05 (foil underside to magnet face)
MAGNETS = {
    "M_c1": {"size": (10.0, 10.0, 5.0), "mag_axis": "z", "xy": IC1.center, "z_top_up": -MAGNET_GAP,
             "motion": "Z down 25 then retract +y 18 (DEV-4 'lower-and-away'); spring returns to UP",
             "z_top_down": -MAGNET_GAP - 25.0, "parked_xy": (40.0, 56.0), "holder": (10.6, 10.6),
             "src": "docs/13 §3.3.1; retract DEV-4"},
    "M_c2": {"size": (10.0, 10.0, 5.0), "mag_axis": "z", "xy": IC2.center, "z_top_up": -MAGNET_GAP,
             "motion": "Z down 25 then retract -y 18", "z_top_down": -MAGNET_GAP - 25.0,
             "parked_xy": (40.0, -6.0), "holder": (10.6, 10.6), "src": "docs/13 §3.3.1; DEV-4"},
    "M_d": {"size": (2.0, 2.0, 4.0), "mag_axis": "z (along 4 mm)", "z_top_up": -MAGNET_GAP,
            "z_stroke": 8.0, "holder": (2.6, 2.6), "post_from_below": True,
            "travel_x": (35.0, 59.6), "travel_y": (6.0, 44.0),
            "speeds": {"drag": 0.20, "gather": 0.30, "transit_max": 5.0},
            "motion": "X-Y stage below the bay + spring-up Z post (pulled down by cam); holds at RC (DEV-4)",
            "src": "docs/13 §3.3.1, §6.2"},
    "M_w": {"size": (3.0, 3.0, 3.0), "xy": BW.center, "z_top": -MAGNET_GAP, "motion": "fixed in anvil recess",
            "src": "docs/13 §3.3.1; position DEV-5"},
    # M_h (3x3x4 Z-only under the RC) is NOT built: DEV-4 (cannot share the RC column with the M_d post)
}
MAGNET_TRANSIT_RULE = "lowered moves of M_d only via J (x >= 44) and never under the electrode bay; " \
                      ">= 8 mm below and >= 6 mm laterally from an incubating chamber (docs/13 §2.2)"

# =====================================================================================================
# 10. Electrical: pogo block (docs/13 §2.7, §6.2) -- CHOICE-9
# =====================================================================================================
POGO = {
    "pins": dict(PADS),                # pin axes = pad centres (card coords)
    "pitch_min": 1.8,                  # Derived from PADS
    "barrel_d_max": 1.6,               # UNVERIFIED (part to be selected at <= 1.8 mm pitch)
    "working_travel": 1.0,             # UNVERIFIED class value
    "force_at_working_N": 1.25,        # class value from PTR series 1064 (opened 2026-11-13; its 2.54 pitch does
                                       # not fit -> part UNVERIFIED); budget 6 x 1.5 N
    "tip_z_engaged": DIE_Z[0],         # 0.340: pad plane
    "block_lift_stroke": 3.0,          # CHOICE-9: tips at z = -1.0 while loading, raised after the lid is latched
    "tip_z_retracted": -1.0,
}
DIE_PRESS_PAD = {  # lid side, reacts the pogo force on the die back (docs/13 §2.7)
    "footprint_x": (55.5, 60.5), "footprint_y": (29.6, 33.1),   # over the pads only
    "contact_z": DIE_Z[1],                                       # die back z = 1.04 (DIE_T UNVERIFIED)
    "compliant_layer": "1.0 mm silicone 40 ShA on a grounded metal stem [assessment]",
    "force_N": 12.0,                                             # >= 6 x 1.5 N + 30 % (Derived)
    "stroke_compliance": 1.0,                                    # covers DIE_T 0.5-1.1 UNVERIFIED
}
WE_RELAY_AND_LEADS = "reed relay in the electrode bay; shielded leads <= 0.3 m to the Gamry cell cable (docs/13 §6.3)"

# =====================================================================================================
# 11. Thermal interface (docs/13 §6.5) -- card coords
# =====================================================================================================
THERMAL = {
    "reagent_bottom": {"x": X_REAGENT, "y": (0.0, CARD_W), "T": (4.0, 8.0), "part": "Peltier cold plate (anvil)"},
    "break_bottom": {"x": X_BREAK, "y": (0.0, CARD_W), "part": "4 mm gap filled with PEEK insulator (CHOICE-7)"},
    "assay_bottom": {"x": X_ASSAY, "y": (0.0, CARD_W), "T": 25.0, "part": "heated Al anvil (minus openings)"},
    "reagent_top": {"x": X_REAGENT, "y": (0.0, CARD_W), "part": "PEEK pressure plate (insulating, no heater)"},
    "assay_top": {"x": X_ASSAY, "y": (0.0, CARD_W), "T": 25.0, "part": "Al heater block 10 mm (pin guide)"},
}
HEATER_BLOCK_T = 10.0          # CHOICE-7
COLD_PLATE_T = 5.0             # CHOICE-7

# =====================================================================================================
# 12. Clamp force budget (Derived, docs/18 §6)
# =====================================================================================================
def clamp_budget(seal_force=10.0, pogo_force=1.5, margin=1.5):
    n_liq = sum(1 for p in PORTS.values() if p.kind == "liquid")
    n_gas = sum(1 for p in PORTS.values() if p.kind == "gas")
    seals = n_liq * seal_force                              # push card UP off the anvil
    pogo = len(PADS) * pogo_force                           # pushes die UP; reacted by the press pad (lid)
    springs = sum(v.f_close_max for v in VALVES.values() if v.fail == "closed")  # push card DOWN, react on lid
    v3 = 3.0                                                # V3 cylinder force-limiting spring (closed in runs)
    card_clamp = margin * seals                             # lid -> card top, min
    lid_total = card_clamp + springs + v3 + DIE_PRESS_PAD["force_N"] + n_gas * GAS_SEAL_LID["force_N"]
    return {"n_liquid_seals": n_liq, "seal_up_N": seals, "pogo_up_N": pogo, "plunger_springs_N": springs,
            "card_clamp_min_N": card_clamp, "press_pad_N": DIE_PRESS_PAD["force_N"],
            "gas_seals_N": n_gas * GAS_SEAL_LID["force_N"], "lid_latch_total_N": lid_total}


CLAMP_DESIGN_FORCE = 250.0     # CHOICE-8: latch/toggle rated >= 250 N (budget ~ 240 N at upper seal force)
CLAMP_APPLICATION = "distributed: heater block (assay zone) + PEEK plate (reagent zone) bear on the flat L3 top, " \
                    "minus pockets for vents, gas seals, pins and the die window (CHOICE-8)"

# =====================================================================================================
# 13. Optical / identity (docs/13 §6.7)
# =====================================================================================================
ID_CODE = {"xy": (44.0, 0.8), "size": (6.0, 6.0), "face": "top",
           "reader": "down-looking reader on the nest front frame, reads with the lid open (CHOICE-11)"}

# =====================================================================================================
# 14. Dock space claims (DOCK coords; boxes ((x0, y0, z0), (x1, y1, z1))) -- CHOICE-12
# =====================================================================================================
ANVIL_TOP_Z_DOCK = CARD_ORIGIN_IN_DOCK[2]                    # 170.0
CARD_TOP_Z_DOCK = ANVIL_TOP_Z_DOCK + CARD_T                  # 176.215
DOCK_FOOTPRINT = ((0.0, 0.0, 0.0), (470.0, 420.0, 330.0))    # CHOICE-12: enclosure envelope (open above the
#   card bay: the lid swings out through the top, see lid_sweep_bbox())

SPACE_CLAIMS = {
    # owner: agent that designs inside; others keep out
    "UPPER_lid_closed": {"box": ((150.0, 30.0, CARD_TOP_Z_DOCK), (320.0, 200.0, 300.0)), "owner": "DOCK UPPER",
                         "note": "head (heater block, pins, springs, yokes, cylinders, press pad, gas seals), "
                                 "pilot-valve manifold, grounded cover, hinge leaves, latch"},
    "LOWER_nest_anvil": {"box": ((150.0, 20.0, 155.0), (320.0, 185.0, ANVIL_TOP_Z_DOCK + 6.0)),
                         "owner": "DOCK LOWER",
                         "note": "anvil plate, cold plate, datum pins, pushers, guide-pin bushes for the lid head; "
                                 "up to z = card top only outside the card footprint (nest frame)"},
    "LOWER_bay": {"box": ((150.0, 20.0, 40.0), (320.0, 200.0, 155.0)), "owner": "DOCK LOWER",
                  "note": "M_c units, M_d stage + post, electrode bay, reagent Peltier stack, tube corridors"},
    "BASE_drip_tray": {"box": ((0.0, 0.0, 0.0), (470.0, 420.0, 15.0)), "owner": "DOCK BASE"},
    "BASE_cold_compartment": {"box": ((10.0, 20.0, 15.0), (145.0, 200.0, 220.0)), "owner": "DOCK BASE",
                              "note": "cooled conjugate bottle, cooled rocking bead vial, S_b; SM-FL line entry"},
    "BASE_under_bay": {"box": ((150.0, 20.0, 15.0), (320.0, 200.0, 40.0)), "owner": "DOCK BASE",
                       "note": "waste bottle low, leak electrodes"},
    "BASE_bottles": {"box": ((325.0, 10.0, 15.0), (465.0, 200.0, 260.0)), "owner": "DOCK BASE",
                     "note": "A1 1 L, HQDP, waste >= 1 L (or under the bay), flow sensors"},
    "BASE_rear_low": {"box": ((150.0, 205.0, 15.0), (320.0, 315.0, 180.0)), "owner": "DOCK BASE",
                      "note": "under the opened lid (keep Z <= 180): 2-ch pressure controller, flow sensors, "
                              "air regulator, tube manifolds"},
    "BASE_pumps": {"box": ((150.0, 320.0, 15.0), (465.0, 415.0, 280.0)), "owner": "DOCK BASE",
                   "note": "S_A, S_IC1, S_IC2, S_RC (+ S_b if not in the cold compartment); envelopes UNVERIFIED"},
    "BASE_electronics": {"box": ((5.0, 205.0, 15.0), (145.0, 415.0, 320.0)), "owner": "DOCK BASE",
                         "note": "controller + watchdog, drivers, PSUs, isolated DAQ (left rear, beside the lid "
                                 "sweep)"},
    "BASE_right_rear": {"box": ((325.0, 205.0, 15.0), (465.0, 315.0, 260.0)), "owner": "DOCK BASE",
                        "note": "free for pumps/bottles overflow"},
    "BENCH_gamry": {"box": ((480.0, 90.0, 0.0), (570.0, 360.0, 190.0)), "owner": "DOCK BASE (placement only)",
                    "note": "Gamry Reference 600+ 9 x 19 x 27 cm W x H x D (gamry.com legacy page, opened)"},
}
# sub-claims inside LOWER_bay (card coords; z negative below the anvil top). LOWER agent owns them all; they are
# listed so that UPPER/BASE agents know the pass-through routes.
LOWER_SUBCLAIMS_CARD = {
    "electrode_bay": {"x": (54.0, 62.5), "y": (28.8, 36.5), "z": (-70.0, 0.0),
                      "note": "grounded enclosure, pogo block + Z lift, relay, RH sensor; cable exits +X"},
    "reagent_peltier_stack": {"x": (-5.0, 20.0), "y": (-5.0, 55.0), "z": (-85.0, 0.0)},
    "tube_corridor_W": {"x": (20.5, 33.5), "y": (-10.0, 60.0), "z": (-110.0, -15.0),
                        "note": "island + west ports turn west/down here"},
    "tube_corridor_E": {"x": (62.5, 80.0), "y": (-10.0, 60.0), "z": (-110.0, -15.0)},
    "Mc_units": {"x": (33.0, 47.0), "y": (-20.0, 70.0), "z": (-70.0, 0.0),
                 "note": "two Z + retract units; columns rise only inside W1/W2"},
    "Md_stage": {"x": (5.0, 90.0), "y": (-25.0, 75.0), "z": (-115.0, -55.0),
                 "note": "X-Y stage (e.g. 2 x 50 mm class, Zaber X-LSM050A opened: 50.8 mm, <3 um, 26 mm/s, "
                         "non-back-driving; footprint UNVERIFIED) and post base; post rises from z -55"},
}
PASS_THROUGHS = {
    "liquid_lines_west": {"dock": card_to_dock((22.0, 25.0, -60.0)), "lines": ["P_in", "P_byp", "P_b", "P_a",
                                                                             "P_d1", "P_d2", "P_cf"]},
    "liquid_lines_east": {"dock": card_to_dock((75.0, 25.0, -60.0)), "lines": ["P_s", "P_wo", "P_rf", "P_a2"]},
    "lid_umbilical": {"dock": (235.0, 200.0, 190.0),
                      "carries": "air supply 1 line, 2 gas lines (P_c, P_mv), heater + sensor + pilot-valve cable"},
    "gamry_cell_cable": {"dock": (320.0, card_to_dock((0, 32.0))[1], card_to_dock((0, 0, -35.0))[2]),
                         "note": "shielded bulkhead on the LOWER claim +X wall; leads <= 0.3 m (docs/13 §6.3)"},
    "smfl_peek_line": {"dock": (0.0, 110.0, 160.0), "note": "left wall; Waters stack stands left of the dock"},
}
LID_HINGE_AXIS = {"point": (150.0, 195.0, 190.0), "direction": (1.0, 0.0, 0.0), "open_angle_deg": 85.0,
                  "note": "CHOICE-10: lid opens upward-back to a stop at 85 deg (beyond 90 deg the lid top would sweep down into the rear claims); head descends vertically 8 mm on 2 guide pins after "
                          "the lid is closed (cam latch), so pins enter the card bores vertically"}
HEAD_VERTICAL_STROKE = 8.0
OPERATOR_LOADING_PATH = {"from": card_to_dock((CARD_L / 2, CARD_W / 2, 150.0)),
                         "to": card_to_dock((CARD_L / 2, CARD_W / 2, 0.0)),
                         "clear_box": ((175.0, 55.0, CARD_TOP_Z_DOCK), (285.0, 145.0, 330.0)),
                         "note": "lid open; card held by its long edges, lowered vertically, then pushers seat it"}


def lid_sweep_bbox(n=22):
    """Bounding box of the closed UPPER claim rotated about the hinge axis 0..open_angle (Derived)."""
    (x0, y0, z0), (x1, y1, z1) = SPACE_CLAIMS["UPPER_lid_closed"]["box"]
    py, pz = LID_HINGE_AXIS["point"][1], LID_HINGE_AXIS["point"][2]
    ys, zs = [], []
    for i in range(n + 1):
        a = math.radians(LID_HINGE_AXIS["open_angle_deg"] * i / n)
        for (y, z) in ((y0, z0), (y0, z1), (y1, z0), (y1, z1)):
            dy, dz = y - py, z - pz
            # opening lifts the front edge (dy < 0) and turns the top face (dz > 0) toward +Y
            ys.append(py + dy * math.cos(a) + dz * math.sin(a))
            zs.append(pz - dy * math.sin(a) + dz * math.cos(a))
    return ((x0, min(ys), min(zs)), (x1, max(ys), max(zs)))


# =====================================================================================================
# 15. Material / colour keys used by common.py
# =====================================================================================================
MATERIALS = {
    "card_L3": "COC", "card_L2": "TPE", "card_L1": "COC", "card_L0": "COC", "die": "glass",
    "anvil": "Al 6061 anodised", "cold_plate": "Al", "heater_block": "Al", "pins": "stainless 303 (non-magnetic "
    "grade to be confirmed)", "magnet": "NdFeB", "pogo": "Au/CuBe", "insulator": "PEEK",
}
