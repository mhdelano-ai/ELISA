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

Revision B (integration, 2026-11-13, docs/18 §15 and docs/23). Changes against Revision A (each line: request ->
decision; tag I-n = integration choice, docs/23 §8):
  * HEAD_GUIDE_PINS new: GP1 (-8, 46), GP2 (84, 4), D6, bush top z 5.0 = NEST_FRAME_TOP_Z (ICR-U1/ICR-1, I-1)
  * PLUNGER pilot 300 -> 400 kPa, cylinder bore 5 -> 6, supply >= 450 kPa, lid switch 350 kPa (DEV-U1/U2, ICR-U5, I-2)
  * CLAMP_DESIGN_FORCE 250 -> 300 N; LID_LATCH catch plates on LOWER brackets (DEV-U3, ICR-U2/U4, I-3)
  * HINGE: UPPER hinge blocks on LOWER hinge pedestals (top Z 160); new claims (ICR-U3, IR-5, I-4)
  * PASS_THROUGHS: per-line exits taken from the LOWER routes; cable window, Peltier exhaust, umbilical grommet,
    Gamry bulkhead flange (ICR-6, IR-2/4/6, I-5); LOWER_MOUNT bolt pattern (IR-1, I-6)
  * drag slot = buffers U swept 2.6-sq holder + 0.30 (slot_polygon(); DEV-L4/ICR-2, I-7)
  * POGO tip_z_retracted -1.0 -> -1.66; class force 1.21 N/pin (ICR-3, I-8)
  * MAGNETS M_c: parallelogram swing, parked (40, 56.7)/(40, -6.7), top z -45.6, fail state HOLD (ICR-4, I-9)
  * ANVIL_THICK_ZONES per DEV-L3 (ICR-5, I-9); NON_MAGNETIC_ZONE materials (ICR-8, I-10)
  * card: MC round D1.596 (DEV-C1), CARD_POKA_CHAMFER + nest block, CARD_TOOLING_HOLES, DIE_WINDOW (CHOICE-C1),
    CER_NECK 'len', lead-in exception V8 (docs/19 §9, I-11); WE2 channel 2.9 confirmed (I-11)
  * VALVE_TIP_SEAT_MARGIN 0.3 (gasket seat) beside VALVE_TIP_EDGE_MARGIN 0.5 (openings) (ICR-7, I-12)
  * SPACE_CLAIMS: BASE_front_strip, BASE_lane_gap, LOWER_hinge_pedestals, UPPER_hinge_blocks; LOWER sub-claims per
    DEV-L6 (IR-3, ICR-6/9)
  * PLUNGER tip_z_open 1.015 -> 0.97 (= closed + 0.8 stroke; Rev A inconsistent by 0.045) (I-16)
  * slot_polygon simplified at 0.02 (STEP size); LOWER/BASE tubes as compounds (no Boolean fuse) (I-15)

Revision C (resolution of the review docs/24, 2026-11-13; docs/18 §17, docs/24 §8). Each line: finding -> change:
  * S1 TOL: complete lateral tolerance list (laser kerf, guide-hole position, pin play, tip diameter, cold-zone
    contraction, COC/Al CTE) and VALVE_TIP_LATERAL_WC(); slot valves G1-G4, V11, V12: pin and tip D0.8 -> D1.0 in
    D1.2 -> D1.3 card bores (radial clearance 0.15 as the D1.2/D1.5 class); every tip now overlaps its channel wall by
    >= 0.25 -> worst case +0.035, RSS +0.16 (DEV-IF-C1)
  * S2: M_d magnet 2x2x4 square -> D2 x 4 cylinder in a ROUND D2.6 holder; drag-slot arms 4.0 -> 3.4 (as the WLc and
    bead-out legs); slot = buffers U swept round holder + 0.30; every slot-valve chord 3.40 -> long-strip model 15.6 um at
    1.32 N (DEV-IF-C2; lateral drag force 0.96x, Derived)
  * S3: PLUNGER tip_z_closed 0.17 -> 0.50 (real stop height on compressed TPE over the lands, estimate 0.37-0.54);
    tip_z_open 0.97 -> 1.30; preload shimmed with a force gauge at the measured height on the reference card (I-13
    extended)
  * S4: FACE_SEAL gasket installed ID = tube OD (free ID 1.50, stretch fit): no annulus open to the port
  * B2: THERMAL reagent cold plate x 2.6-20 / y 3-47 behind a 2-mm insulation gap (PEEK lip 1.5 mm + foam);
    peltier_exhaust heat 10.6 -> 12.3 W max (sink acceptance R <= 1.6 K/W; docs/21 §5.4 Rev C)
  * B1: (no interface number) P_in line PEEK 0.0635 mm ID; S_IC1/S_IC2 moved beside the bay (docs/22 Rev C)
  * M3: stale Rev A comments (DATUM_PIN_D, cylinder_pitch_min, P_b dock text)

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
DATUM_PIN_D = 4.0                         # zirconia (docs/21 CHOICE-L9; Rev A said hardened steel), protrudes 5.0 mm
#                                           above z = 0 [assessment]
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
    "pin_in_card_bore_radial_clearance_min": 0.15,  # Derived: (1.5-1.2)/2 = (1.2-0.8)/2 - 0.05 = (1.3-1.0)/2
    # Rev C (docs/24 S1): terms missing from the Rev B lateral chain
    "laser_kerf_per_side": 0.02,     # +-0.04 on a laser-cut L1 channel width -> 0.02 per wall [assessment, M11 coupon]
    "guide_hole_position": 0.01,     # CuSn8 guide-plate hole to the head guide pins (docs/20 §3.1) [assessment]
    "pin_play": 0.006,               # pin g5 in guide H7 (docs/20 PIN_FIT) [Derived, max]
    "tip_diameter": 0.005,           # ground tip land +-0.01 on D -> 0.005 on the radius [assessment]
    "cold_zone_contraction": 0.024,  # 20 mm COC x 60e-6/K x 20 K after clamping (reviewer docs/24 S1) [assessment,
                                     # alpha_COC UNVERIFIED]; x direction only, taken in full on every valve
    "coc_vs_al_head_cte": 0.010,     # 55 mm x (60 - 23)e-6/K x 5 K (20 -> 25 degC) [assessment]
}


X_ONLY_TOL = ("cold_zone_contraction", "coc_vs_al_head_cte")   # act along card x only (from datum B / x = 0)


def valve_tip_lateral_wc_dir(vid, rss=False):
    """Rev C: lateral worst case for valve vid, projected on the channel normal: the x-only terms count with |n_x| of
    the normal of the channel the tip sits on; the y CTE term (datum A, 25 mm x 37e-6 x 5 K = 0.005) with |n_y|."""
    from shapely.geometry import LineString as _LS, Point as _Pt
    v = VALVES[vid]
    k = min(CHANNELS, key=lambda c: _LS(CHANNELS[c]["pts"]).distance(_Pt(v.xy)))
    pts = CHANNELS[k]["pts"]
    i = min(range(len(pts) - 1), key=lambda j: _LS([pts[j], pts[j + 1]]).distance(_Pt(v.xy)))
    dx, dy = pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]
    L = math.hypot(dx, dy)
    nx, ny = abs(dy / L), abs(dx / L)
    iso = [TOL[q] for q in ("head_to_nest", "datum_pin_position", "card_edge_to_feature", "L1_to_L3_registration",
                            "laser_kerf_per_side", "guide_hole_position", "pin_play", "tip_diameter")]
    xo = [TOL[q] * nx for q in X_ONLY_TOL] + [0.005 * ny]
    vals = iso + xo
    return math.sqrt(sum(q * q for q in vals)) if rss else sum(vals)


def valve_tip_lateral_wc(rss=False):
    """Rev C (docs/24 S1): worst-case (or RSS) lateral error of a valve tip relative to its L1 channel wall.
    Chain: head->nest, datum pin, L3 edge->feature, L1->L3 registration, kerf, guide hole, pin play, tip D,
    cold-zone contraction, COC/Al CTE. Returns mm (Derived)."""
    keys = ("head_to_nest", "datum_pin_position", "card_edge_to_feature", "L1_to_L3_registration",
            "laser_kerf_per_side", "guide_hole_position", "pin_play", "tip_diameter", "cold_zone_contraction",
            "coc_vs_al_head_cte")
    v = [TOL[k] for k in keys]
    return math.sqrt(sum(x * x for x in v)) if rss else sum(v)

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
MC = Bore("MC", (16.0, 30.0), d=round(math.sqrt(4.0 * 2.0 * 1.0 / math.pi), 4), size=(2.0, 1.0),
          z=(Z_L0[1], Z_L0[1] + 5.0),
          note="conjugate meter 10.0 uL from foil to PTFE stop (docs/13 §2.3); Rev B: ROUND bore d = sqrt(4 x 2.0 x "
               "1.0 / pi) = 1.5958 of the same 2.000 mm^2 area as the docs/13 2.0 x 1.0 rectangle (DEV-C1, docs/19); "
               "'size' kept as the equivalent rectangle; L3 cavity depth Derived 5.0 - 0.575 = 4.425 (CHOICE-16)")
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
DIE_WINDOW_CLEAR = 0.05         # L3/L2 window = die outline + 0.05 (TPE cut-out die + 0.10, CHOICE-14). Rev B reading
#                                 (CHOICE-C1, docs/19): the same total clearance 0.10 is put on the two FREE faces only;
#                                 the datum faces are flush with the nominal die -> use DIE_WINDOW for the L3 window.
DIE_DATUM_EDGES = ("x = 55.0 for y 27.0-33.35", "y = 33.35")  # CHOICE-14: notch-free window edges
DIE_WINDOW = {"x": (DIE_X[0], DIE_X[1] + 2 * DIE_WINDOW_CLEAR),   # (55.00, 61.10) Rev B (CHOICE-C1)
              "y": (DIE_Y[0] - 2 * DIE_WINDOW_CLEAR, DIE_Y[1])}   # (23.25, 33.35); D1.0 corner reliefs (card)
# Readout cell (docs/13 §2.3, §3.5.1)
RC_CENTER = (56.8, 25.0)
RC_SIZE = (2.6, 2.0)            # x 55.5-58.1, y 24.0-26.0, height 0.200
WE2_CHANNEL = {"x": (58.1, 61.0), "y_c": 25.0, "w": 1.0, "h": 0.05}   # docs/13 §2.3; Rev B CONFIRMED 2.9 long
#   (bounded by the RC edge x 58.1 and the die edge x 61.0; docs/13's "1.0 x 3.0" is nominal) -> cell 1.31 uL in the
#   card CAD instead of 1.34 (DEV-C4, docs/19 §6.1; I-11, docs/23)
CER_POCKET = {"x": (55.3, 55.7), "y": (23.45, 23.85)}                 # 0.4 x 0.4, DEV-2 (moved to x 55.5)
CER_NECK = {"x": (55.5, 55.9), "y": (23.85, 24.0), "len": 0.15,       # 0.4 wide x 0.15 long, docs/13 §2.3; height =
            "h": 0.15}  # cell height 0.200. Rev B: 'len' is the name; 'h' is a deprecated alias of 'len' (docs/19 §9)

# Card poka-yoke and tooling holes (Rev B, docs/19 CHOICE-C7/C4)
CARD_POKA_CHAMFER = {"corner": (CARD_L, CARD_W), "leg": 4.0}   # CHOICE-C7: 4 x 45 deg chamfer at (75.5, 50), all layers
NEST_POKA_BLOCK = {"clear": 0.3, "z": (0.2, 5.0), "lead_in": 1.5}   # I-11: nest corner block parallel to the chamfer,
#   0.3 clear of it, 0.2 above the anvil (gutter passes below), same 1.5 lead-in as the nest (owner DOCK LOWER)
CARD_TOOLING_HOLES = {"round": {"xy": (59.0, 42.0), "d": 2.0}, "slot": {"xy": (59.0, 5.0), "w": 2.0, "len_y": 3.0},
                      "depth_L3": 3.0, "note": "CHOICE-C4: open in the foil (L0-L2), blind 3.0 into L3 from below; "
                      "over the 5-mm anvil plate, clear of every opening (checked docs/23 §4)"}
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


SLOT_VALVE_TIP_D = 1.0   # Rev C (docs/24 S1, DEV-IF-C1): slot valves G1-G4, V11, V12 D0.8 -> D1.0 (pin = tip)
SLOT_VALVE_BORE_D = 1.3  # card bore for the D1.0 slot pins: radial clearance 0.15 (TOL rule)


def _v(id_, xy, klass, function, src, tip=1.0, fail="closed", slot_tip=SLOT_VALVE_TIP_D):
    if klass == "slot":                       # Rev C: slot class pin = tip, D1.0 in D1.3 bores (G3: D0.9 in D1.2)
        tip = pin = slot_tip
        bore = SLOT_VALVE_BORE_D if slot_tip >= 1.0 else 1.2
        fmax, fnom = 1.5, 1.2
        return Valve(id_, xy, tip, pin, bore, klass, fail, fnom, fmax, function, src)
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
    _v("G3", (54.2, 25.0), "slot", "WLc <-> cell", "docs/13 §4; DEV-2; Rev C (docs/24 S1): D0.9 at x 54.20 (was D0.8 "
       "at 54.25): seal edge 0.35 from the die edge, tip + WC tolerance stays 0.035 inside the TPE cut (die - 0.10); a "
       "D1.0 tip would leave the TPE and D1.0 at 54.15 breaks the V12 collar gap", slot_tip=0.9),
    _v("G4", (57.85, 22.5), "slot", "cell <-> BW", "docs/13 §4; DEV-2; Rev C: D1.0 at y 22.50 (was D0.8 at 22.60): seal "
       "edge 0.35 from the die edge"),
]}
assert len(VALVES) == 21  # docs/13 §4: 17 valves + 4 gates

# Plunger interface (CHOICE-2): pin guided in the lid head, spring-closed, lifted pneumatically via a yoke
PLUNGER = {
    "principle": "spring-closed pin; opened by a single-acting pneumatic cylinder lifting the pin head via a "
                 "yoke; V3 inverted (spring lifts, cylinder closes through a 2.5 N force-limiting spring)",
    "stroke_pin": 0.8,                 # CHOICE-2: >= 0.5 required (docs/13 §6.2); 0.175 + TPE + 0.3 clearance
    "tip_z_closed": 0.50,              # Rev C (docs/24 S3): REAL stop height. Every tip is wider than its channel, so
                                       # it stops on the TPE compressed over the L1 lands (land top 0.315 + TPE), not
                                       # at the foil. Estimate 0.37-0.54 (rigid translation of the TPE column 0.175 ->
                                       # 0.54; 0.37 at 54 % land compression) [Derived, docs/24 §3]; nominal 0.50.
                                       # Rev A/B 0.17 (= foil top + 30 um) lay inside the L1 lands (docs/23 §4.2).
                                       # Preload, hook gap and collar are set on the reference card at the MEASURED
                                       # height with a force gauge (I-13 extended, docs/20 §2.3 Rev C)
    "tip_z_closed_range": (0.37, 0.54),
    "tip_z_open": 0.50 + 0.8,          # Rev C: = tip_z_closed + stroke_pin = 1.30 (Rev B 0.97 = 0.17 + 0.8; Rev A wrote Z_L2 top
                                       # + 0.3 = 1.015, inconsistent with the 0.8 stroke by 0.045); 0.255 above the TPE
    "pin_extension_limit_below_open": 1.0,  # collar stops the pin 0.2 mm below 'closed' when no card is present
    "tip_edge_chamfer": 0.05,          # flat land, edge-broken [assessment]
    "card_bore_lead_in": 0.3,          # 0.3 x 45 deg chamfer at the L3 top of each bore (CHOICE-2)
    "card_bore_lead_in_except": {"V8": 0.0},   # Rev B (CHOICE-C10, docs/19 §6.5): no lead-in at V8, edge break only,
                                       # so the P_mv gas ring (OD 7.0 kept) has 0.14 mm of flat land to the V8 bore
    "actuation_time_max_s": 0.2,       # docs/13 §4
    "pilot_pressure_kPa": 400.0,       # Rev B (DEV-U1, docs/20 §4.2): 300 -> 400 kPa; worst force margin 1.60 (V14)
                                       # with D6; SMC S070B-5DG 0.5 W coil rated 0.5 MPa (docs/20 §2.5)
    "pilot_switch_trip_kPa": 350.0,    # Rev B: pressure switch on the lid manifold -> fault latch (docs/20 §2.5)
    "air_supply_min_kPa": 450.0,       # Rev B: at the dock inlet, upstream of the BASE regulator FR1 (docs/22 §8)
    "cylinder_bore": 6.0,              # Rev B (DEV-U2): 5 -> 6 (pitch 9 kept); pull area Derived pi/4 (6^2 - 1.5^2)
                                       # = 26.5 mm^2 -> 10.6 N at 400 kPa vs need <= 6.6 N (docs/20 §4.2)
    "cylinder_pitch_min": 9.0,         # CHOICE-2: bore 6 (Rev B) + walls/seals (Rev A comment said bore 5)
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
    "pin_collar_closed": (16.415, 16.915),             # Rev B (DEV-U5, docs/20 §2.2): collar 0.2 above the block
    "spring_plate": (24.5, 26.0),                      # Rev B: spring plate reacts all pin springs
    "pin_head_closed_top": 25.0,                       # Rev A envelope value (kept for reference; real parts above)
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
    Port("P_b", (37.5, 25.0), "liquid", "bead line -> V4/V5", "S_b outlet line 0.102 ID (DEV-B3)", "docs/13 §2.5"),
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
    "gasket_id": 1.5875, "gasket_od": 3.3, "gasket_t": 0.50,   # Rev C (docs/24 S4): installed ID = tube OD; the
    "gasket_id_free": 1.50,        # gasket is cut at ID 1.50 and stretched over the tube (radial interference 0.044,
                                   # [assessment]) so it seals on the tube OD and on the foil round the D1.0 hole: no
                                   # annulus is open to the port. Rev B ID 1.7 left a 0.056 x 0.38 annulus = 0.110 uL
                                   # per port (reviewer, Derived), unswept
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
SLOT_W = 3.4                # Rev C (DEV-IF-C2, docs/24 S2): arms 4.0 -> 3.4 like the WLc/bead-out legs (round holder
#                             D2.6 + 2 x 0.4); docs/13 §2.2: 4 mm
SLOT_W_BEADOUT = 3.4        # DEV-5: bead-out leg (axis-aligned) narrowed to 3.4 (holder 2.6 + 2 x 0.4)
SLOT_W_WLC = 3.4           # DEV-5: straight, axis-aligned J -> RC part narrowed to 3.4 (holder 2.6 + 2 x 0.4)
SLOT_CENTERLINES = {        # buffers of these polylines (round caps) form the slot; widths in SLOT_WIDTHS
    "slot_IC1": [FUNNEL_APEX["IC1"]] + WL1,
    "slot_IC2": [FUNNEL_APEX["IC2"]] + WL2,
    "slot_WLc": [J, RC_CENTER],
    "slot_beadout": BEAD_OUT_PATH,
}
SLOT_WIDTHS = {"slot_IC1": SLOT_W, "slot_IC2": SLOT_W, "slot_WLc": SLOT_W_WLC, "slot_beadout": SLOT_W_BEADOUT}
# Rev B (DEV-L4 / ICR-2, I-7): the anvil slot is the union of the buffers above AND the footprint of the axis-aligned
# 2.6-sq M_d holder swept along every drag and bead-out path, grown by SLOT_HOLDER_CLEAR (the buffers alone leave
# 0.03 mm at the J fillet). Max local width 4.44 at G1/G2 -> foil deflection under a 1.5 N slot valve 19 um
# (docs/13 §2.1: 15 um at 4.0; M4 acceptance <= 20 um). Kept: square holder (a round holder cannot carry the
# 2 x 2 magnet, diagonal 2.83).
SLOT_HOLDER_CLEAR = 0.30       # stage accuracy 0.020 + post/holder run-out 0.05 + 0.2 margin [assessment] (docs/21)
SLOT_MAX_LOCAL_WIDTH = 3.40    # Rev C: min chord through every slot-valve tip centre = 3.40 (Derived, slot_polygon();
#                                Rev B 4.44 at G1/G2 with the square holder)
SLOT_HOLDER_ROUND = True       # Rev C: round D2.6 holder (D2 x 4 magnet); swept footprint = buffer of the path


def slot_polygon(clear=SLOT_HOLDER_CLEAR, step=0.1):
    """Anvil drag slot (shapely polygon, card coords): buffers U swept holder squares + clear (Rev B)."""
    from shapely.geometry import LineString, box as _box
    from shapely.ops import unary_union
    h = 0.5 * 2.6 + clear      # M_d holder D2.6 round (Rev C; Rev B 2.6 sq) (MAGNETS['M_d']['holder'])
    parts = [LineString(v).buffer(SLOT_WIDTHS[k] / 2, quad_segs=16) for k, v in SLOT_CENTERLINES.items()]
    for path in (DRAG_PATH["IC1"], DRAG_PATH["IC2"], BEAD_OUT_PATH):
        if SLOT_HOLDER_ROUND:
            parts.append(LineString(path).buffer(h, quad_segs=16))
            continue
        ls = LineString(path)
        n = max(2, int(ls.length / step) + 1)
        for i in range(n):
            p = ls.interpolate(i * ls.length / (n - 1)).coords[0]
            parts.append(_box(p[0] - h, p[1] - h, p[0] + h, p[1] + h))
    return unary_union(parts).simplify(0.02)   # 0.02 << 0.30 holder clearance; keeps the anvil STEP small
M_W_RECESS = {"center": BW.center, "size": (3.4, 3.4), "depth": 3.2}   # M_w 3x3x3 top at z = -0.16
ANVIL_CONTACT_OPENING = {"x": (55.3, 60.7), "y": (29.8, 33.2)}          # = card contact window, docs/13 §2.7
ANVIL_TOP_PLATE_T_THIN = 5.0   # CHOICE-5: over the magnet bay (card x 31-64): 5 mm non-magnetic Al plate
ANVIL_THICK_ZONES = {          # CHOICE-5: port inserts need depth; no magnet below these zones
    # Rev B (DEV-L3 / ICR-5): island boss to x 40.5 (P_b insert bore wall 0.35 -> 1.35), P_s boss added, west strip
    # x 24-32.5 (M_c flange 12.6 must clear); thin plate = bottom pocket x 32.5-62.5, y 0-50 minus the bosses
    "island_boss": {"x": (24.0, 40.5), "y": (19.0, 31.0), "t": 15.0},
    "west_strip": {"x": (24.0, 32.5), "y": (0.0, 50.0), "t": 15.0},
    "east_block": {"x": (62.5, 75.5), "y": (0.0, 50.0), "t": 15.0},
    "P_a2_boss": {"x": (49.0, 53.5), "y": (34.5, 39.0), "t": 15.0},
    "P_s_boss": {"x": (60.3, 62.5), "y": (17.8, 23.2), "t": 15.0},
}
VALVE_TIP_EDGE_MARGIN = 0.5    # CHOICE-5: tip edge >= 0.5 from any anvil THROUGH-opening (unsupported foil);
#                                V15 exception 0.25 (accepted, CHOICE-5)
VALVE_TIP_SEAT_MARGIN = 0.3    # Rev B (ICR-7, I-12): tip edge >= 0.3 from a gasket SEAT edge (the compressed gasket
#                                supports the foil; FACE_SEAL rule); V3 -> P_byp seat 0.36 passes

# =====================================================================================================
# 9. Magnets (docs/13 §3.3.1; mag_b.py: B_r 1.3 T UNVERIFIED, gap 0.16 + foil 0.14 = bead plane 0.30)
# =====================================================================================================
MAGNET_GAP = 0.16              # docs/13 §6.2, +-0.05 (foil underside to magnet face)
MAGNETS = {
    # Rev B (DEV-L1/L2, ICR-4, I-9): parallelogram swing R 64.5 (one worm drive per unit), holder flange seats on the
    # plate underside (gap by geometry); FAIL STATE = HOLD (self-locking worm) -- a spring return would drive M_c into
    # the M_d post while M_d works from the window (docs/21 DEV-L1). Departure from docs/13 §3.3.1 "spring-up".
    "M_c1": {"size": (10.0, 10.0, 5.0), "mag_axis": "z", "xy": IC1.center, "z_top_up": -MAGNET_GAP,
             "motion": "parallelogram swing R 64.5 outward (+y) and down to park; fail state HOLD",
             "swing_R": 64.5, "z_top_down": -45.6, "parked_xy": (40.0, 56.7), "holder": (10.6, 10.6),
             "fail": "hold", "src": "docs/13 §3.3.1; DEV-4; Rev B DEV-L1/L2 (docs/21)"},
    "M_c2": {"size": (10.0, 10.0, 5.0), "mag_axis": "z", "xy": IC2.center, "z_top_up": -MAGNET_GAP,
             "motion": "parallelogram swing R 64.5 outward (-y); fail state HOLD", "swing_R": 64.5,
             "z_top_down": -45.6, "parked_xy": (40.0, -6.7), "holder": (10.6, 10.6), "fail": "hold",
             "src": "docs/13 §3.3.1; DEV-4; Rev B DEV-L1/L2"},
    # Rev C (docs/24 S2, DEV-IF-C2): D2 x 4 axially magnetised cylinder in a ROUND D2.6 holder (Rev B: 2 x 2 x 4 in a
    # 2.6-sq holder, which widened the slot to 4.44 at G1/G2). 'size' keeps the bounding box. Charge-sheet model at the
    # bead plane 0.30: |B| 0.97x, max lateral grad(B^2) 0.96x, axial grad(B^2) 1.06x of the square magnet, same B_r
    # (Derived, docs/21 §5.3 Rev C). Part: catalogue D2 x 4 N42-class NdFeB, part number UNVERIFIED
    "M_d": {"size": (2.0, 2.0, 4.0), "shape": "cyl", "d": 2.0, "holder_shape": "round",
            "mag_axis": "z (along 4 mm)", "z_top_up": -MAGNET_GAP,
            "z_stroke": 8.0, "holder": (2.6, 2.6), "post_from_below": True,   # holder D2.6 (Rev C round)
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
    "force_at_working_N": 1.21,        # Rev B: PTR series 1007.70 class (docs/21 §4, page opened: preload 0.50 N,
                                       # 1.40 N at 1.27 full travel) linear at 1.0 mm -> 1.21 N; 6 pins 7.25 N
                                       # (budget 9 N); part number not chosen (UNVERIFIED)
    "tip_z_engaged": DIE_Z[0],         # 0.340: pad plane
    "block_lift_stroke": 3.0,          # CHOICE-9 (kept)
    "tip_z_free_up": DIE_Z[0] + 1.0,   # 1.34 Derived: free tip height at the block's up stop (working travel 1.0)
    "tip_z_retracted": DIE_Z[0] + 1.0 - 3.0,   # Rev B (ICR-3): -1.66 Derived 1.34 - 3.0 (Rev A said -1.0, which would
                                       # need 1.66 mm compression > 1.27 full travel)
}
DIE_PRESS_PAD = {  # lid side, reacts the pogo force on the die back (docs/13 §2.7)
    "footprint_x": (55.5, 60.5), "footprint_y": (29.6, 33.1),   # over the pads only
    "contact_z": DIE_Z[1],                                       # die back z = 1.04 (DIE_T UNVERIFIED)
    "compliant_layer": "1.0 mm silicone 40 ShA on a grounded metal stem [assessment]",
    "force_N": 12.0,                                             # >= 6 x 1.5 N + 30 % (Derived); Rev B: kept
    #   12 N > pogo 7.25 N: the die never lifts; net 4.75 N presses the die onto L1b/foil/anvil (0.12 MPa, Derived)
    "stroke_compliance": 1.0,                                    # covers DIE_T 0.5-1.1 UNVERIFIED
}
WE_RELAY_AND_LEADS = "reed relay in the electrode bay; shielded leads <= 0.3 m to the Gamry cell cable (docs/13 §6.3)"
WE_RELAY_FIELD = {  # Rev B (I-10): |B| at the relay 1.9 mT with M_c1 parked (docs/21 §5.5). Decision: relay stays in
    # the electrode bay (lead length rules); reed relay with internal mu-metal screen + an extra 0.3-mm mu-metal can,
    # reed axis along y [assessment]; acceptance: no change of state or contact resistance with 5 mT applied at the
    # parked-magnet direction (incoming test + M5a). Optical (PhotoMOS) relays rejected: off-state leakage too high
    # for >= 1e13 Ohm [assessment].
    "B_max_mT": 1.9, "test_field_mT": 5.0, "screen": "internal mu-metal + 0.3 mm mu-metal can (UNVERIFIED part)"}

# =====================================================================================================
# 11. Thermal interface (docs/13 §6.5) -- card coords
# =====================================================================================================
THERMAL = {
    "reagent_bottom": {"x": X_REAGENT, "y": (0.0, CARD_W), "T": (4.0, 8.0), "part": "Peltier cold plate (anvil)",
                       # Rev C (docs/24 B2): cold plate x 2.6-20 / y 3-47 (covers RCj 3-13 x 33-43, MC, V8, P_cf),
                       # inside a 2-mm insulation gap (PEEK lip z -1.5..0 for foil support + closed-cell foam below);
                       # +x break x 20-24 PEEK lip + foam. Rev B: 1-mm full-depth PEEK walls (7.1 W leak, reviewer)
                       "cold_plate_xy": ((2.6, 3.0), (20.0, 47.0)), "insulation_gap": 2.0, "peek_lip_t": 1.5},
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


CLAMP_DESIGN_FORCE = 300.0     # Rev B (DEV-U3, ICR-U4): head force 280 N nominal, 265-295 N over the stack tolerance
#                                (docs/20 §4.6); design value 300 N for nest, anvil, latches and hinge (Rev A 250 N)
CLAMP_APPLICATION = "distributed: heater block (assay zone) + PEEK plate (reagent zone) bear on the flat L3 top, " \
                    "minus pockets for vents, gas seals, pins and the die window (CHOICE-8)"

# -----------------------------------------------------------------------------------------------------
# 12b. Nest, head location, latch and hinge (Rev B, integration; docs/18 §15, docs/23)
# -----------------------------------------------------------------------------------------------------
NEST_FRAME_TOP_Z = 5.0         # Rev B (ICR-9): nest frame top = datum-pin protrusion (card z; dock Z 175.0);
#                                M_c bracket stubs stay below z -15 (docs/21)
HEAD_GUIDE_PINS = {            # Rev B (ICR-U1 / ICR-1, I-1): one position set for both modules
    "GP1": (-8.0, 46.0), "GP2": (84.0, 4.0),   # card xy, diagonal; 1.2 / 1.7 mm walls to the nest opening (card+1.8)
    "pin_d": 6.0,                               # h6, hardened 1.2842 (>= 45 mm from any magnet, docs/20 CHOICE-U15)
    "bush_bore": "D6 H7", "bush_od": 10.0, "bush_material": "CuSn8",   # LOWER, reamed in place
    "bush_top_z": NEST_FRAME_TOP_Z,             # 5.0; bush through the anvil (z -15 ... 5)
    "pin_tip_z_raised": NEST_FRAME_TOP_Z + 0.5,  # 5.5: tip 0.5 above the bush/nest top with the head raised
    "pin_tip_z_down": NEST_FRAME_TOP_Z + 0.5 - 8.0,   # -2.5 Derived (head stroke 8.0, HEAD_VERTICAL_STROKE)
    "nose": 1.0,                                # conical lead (docs/20)
    "src": "positions: LOWER CHOICE-L6 moved 1 mm outward (GP1 x -7 -> -8, GP2 x 83 -> 84) for bush walls; "
           "UPPER CHOICE-U15 ears follow"}
LID_LATCH = {                  # Rev B (ICR-U2, I-3): two Kipp K0045 draw latches on the lid front (UPPER), catch plates
    # K0045.9143372 on two LOWER brackets bolted to the anvil front face; keep-outs (dock boxes) for bail + catch:
    "catch_keepouts_dock": [((173.0, 34.0, 161.0), (199.0, 55.0, 176.0)), ((271.0, 34.0, 161.0), (297.0, 55.0, 176.0))],
    "reaction_N_each": 95.0,   # Derived: latches 186 N at 295 N head force (docs/20 §4.6) -> 189 N at 300 N, /2
    "src": "docs/20 CHOICE-U13; Kipp K0045 catalogue page (opened by UPPER); envelope UNVERIFIED"}
HINGE_SUPPORT = {              # Rev B (ICR-U3, IR-5, I-4): UPPER hinge blocks bolt onto two LOWER hinge pedestals
    "blocks_dock": [((150.0, 185.0, 160.0), (153.8, 200.0, 199.0)), ((316.2, 185.0, 160.0), (320.0, 200.0, 199.0))],
    "pedestals_dock": [((150.0, 185.0, 44.0), (154.0, 200.0, 160.0)), ((316.0, 185.0, 44.0), (320.0, 200.0, 160.0))],
    "pedestal_top_Z": 160.0,
    "load": "110 N + 1.9 N m per side at 300 N (docs/20 §2.7, scaled 300/295)",
    "why": "closes the clamp loop (head -> card -> anvil -> bay frame -> pedestals -> hinge; latches -> anvil) inside "
           "the LOWER + UPPER modules; BASE carries weight only; BASE has no structure in X 150-154 above the deck",
    "partition_clearance": "fixed blocks 1.0 mm from the BASE partitions (no relative motion); moving lid parts "
                           ">= 3 mm (checked docs/23 §4)"}
LOWER_MOUNT = {                # Rev B (IR-1, I-6): LOWER bay base plate (dock Z 40-44) on the BASE deck (top Z 40)
    "deck_top_Z": 40.0,
    "bolts_dock": [(165.0, 35.0), (165.0, 110.0), (165.0, 185.0), (305.0, 35.0), (305.0, 110.0), (305.0, 185.0)],
    "bolt": "M6, counterbored in the 4-mm base plate (heads below the stages: X stage starts 22 mm above)",
    "dowel_round_dock": (165.0, 50.0), "dowel_slot_dock": (305.0, 50.0), "dowel_d": 6.0,
    "unused": "BASE offers 9 holes; the three at X 235 lie under the M_d stage (not used)"}

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
                              "note": "cooled conjugate tube, cooled rocking bead vial, SV_b; SM-FL line entry (Rev C: "
                                      "S_b is in the rear pump row; Rev B text said S_b here)"},
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
    # Rev B additions (IR-3, ICR-U3, I-4)
    "BASE_front_strip": {"box": ((0.0, 0.0, 15.0), (470.0, 20.0, 330.0)), "owner": "DOCK BASE",
                         "note": "cold-box door, Peltier exhaust duct extension + louvre; front controls may protrude "
                                 "to Y -25 (E-stop), light bar to Y -6"},
    "BASE_lane_gap": {"box": ((145.0, 200.0, 15.0), (325.0, 205.0, 178.0)), "owner": "DOCK BASE",
                      "note": "tube lanes between LOWER and BASE_rear_low"},
    "LOWER_hinge_pedestal_L": {"box": ((150.0, 185.0, 44.0), (154.0, 200.0, 160.0)), "owner": "DOCK LOWER"},
    "LOWER_hinge_pedestal_R": {"box": ((316.0, 185.0, 44.0), (320.0, 200.0, 160.0)), "owner": "DOCK LOWER"},
    "UPPER_hinge_block_L": {"box": ((150.0, 185.0, 160.0), (153.8, 200.0, 199.0)), "owner": "DOCK UPPER"},
    "UPPER_hinge_block_R": {"box": ((316.2, 185.0, 160.0), (320.0, 200.0, 199.0)), "owner": "DOCK UPPER"},
}
# sub-claims inside LOWER_bay (card coords; z negative below the anvil top). LOWER agent owns them all; they are
# listed so that UPPER/BASE agents know the pass-through routes.
LOWER_SUBCLAIMS_CARD = {
    "electrode_bay": {"x": (54.0, 62.5), "y": (28.8, 36.5), "z": (-70.0, 0.0),
                      "note": "grounded enclosure, pogo block + Z lift, relay, RH sensor; cable exits +X"},
    "reagent_peltier_stack": {"x": (-12.0, 20.0), "y": (-55.0, 55.0), "z": (-85.0, 0.0),
                              "note": "Rev B (DEV-L6): incl. heat sink, fan and exhaust duct to dock Y 20"},
    "tube_corridor_W": {"x": (20.5, 33.5), "y": (-10.0, 60.0), "z": (-110.0, -15.0),
                        "note": "island + west ports turn west/down here"},
    "tube_corridor_E": {"x": (62.5, 80.0), "y": (-10.0, 60.0), "z": (-110.0, -15.0)},
    "Mc_units": {"x": (28.0, 52.0), "y": (-55.0, 106.0), "z": (-77.0, 0.0),
                 "note": "Rev B (DEV-L2/L6): two parallelogram swing units; columns rise only inside W1/W2"},
    "Md_stage": {"x": (-28.0, 123.0), "y": (-50.0, 100.0), "z": (-126.0, -62.0),
                 "note": "X-Y stage (e.g. 2 x 50 mm class, Zaber X-LSM050A opened: 50.8 mm, <3 um, 26 mm/s, "
                         "non-back-driving; footprint UNVERIFIED) and post base; post rises from z -55"},
}
PASS_THROUGHS = {
    # Rev A points inside LOWER (kept for reference): west card (22, 25, -60), east card (75, 25, -60)
    "liquid_lines_west": {"dock": card_to_dock((22.0, 25.0, -60.0)), "lines": ["P_in", "P_byp", "P_b", "P_a",
                                                                             "P_d1", "P_d2", "P_cf"]},
    "liquid_lines_east": {"dock": card_to_dock((75.0, 25.0, -60.0)), "lines": ["P_s", "P_wo", "P_rf", "P_a2"]},
    "lid_umbilical": {"dock": (235.0, 200.0, 190.0),
                      "carries": "air supply 1 line, 2 gas lines (P_c, P_mv), heater + sensor + pilot-valve cable",
                      # Rev B (IR-4): BASE hand-over grommet in the rear-low cover; UPPER owns the flexible loop
                      "base_grommet_dock": {"x": (236.0, 262.0), "y": (205.0, 211.0), "z": 180.0,
                                            "P_c_x": 240.0, "P_mv_x": 248.0, "air_x": 258.0}},
    "gamry_cell_cable": {"dock": (320.0, card_to_dock((0, 32.0))[1], card_to_dock((0, 0, -35.0))[2]),
                         "note": "shielded bulkhead on the LOWER claim +X wall; leads <= 0.3 m (docs/13 §6.3)",
                         # Rev B (IR-6): flange <= 16 (Y) x 20 (Z) on that axis; connector type to be selected
                         "flange_YZ": (16.0, 20.0)},
    "smfl_peek_line": {"dock": (0.0, 110.0, 160.0), "note": "left wall; Waters stack stands left of the dock"},
    # Rev B (ICR-6 / IR-2, I-5): cable window on the LOWER west boundary (motor, heater, sensor, Peltier, pogo-cylinder
    # air); the LOWER bay frame is open there
    "cable_window_W": {"x": 150.0, "y": (150.0, 195.0), "z": (60.0, 140.0)},
    # Rev B (ICR-6): LOWER Peltier exhaust duct outlet (10.6 W); BASE continues it to a louvre in the front-bay panel
    "peltier_exhaust": {"x": (186.0, 210.0), "y": 20.0, "z": (118.0, 144.0), "heat_W": 12.3},   # Rev C: <= 12.3 W at the
    #   acceptance limit (sink R_th 1.6 K/W, 30 degC air, design load 3.47 W; docs/21 §5.4 Rev C); Rev B said 10.6 W
}
# Rev B (ICR-6 / IR-2, I-5): exact exit point of every card liquid line on the LOWER claim boundary (dock coords,
# tube axis, 1/16 in OD), taken from the LOWER routes (dock_lower.geom.tube_route, vertical drop, R 25 bend, run to
# the wall). BASE routes start here; glands (grommets) sit in the BASE well partitions X 147-149 / 323-325 (Rev C comment fix, docs/24 M3; Rev B text 321-323).
LIQUID_LINE_EXITS = {
    "P_in": (150.0, 102.3, 114.0), "P_byp": (150.0, 98.3, 112.0), "P_b": (150.0, 100.0, 108.0),
    "P_a": (150.0, 100.0, 110.0), "P_d1": (150.0, 116.0, 112.0), "P_d2": (150.0, 84.0, 112.0),
    "P_cf": (150.0, 110.0, 112.0),
    "P_rf": (320.0, 80.5, 112.0), "P_s": (320.0, 95.5, 112.0), "P_wo": (320.0, 110.5, 115.0),
    "P_a2": (320.0, 161.5, 112.0),
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
    "anvil": "Al cast tooling plate, hard-anodised (docs/21)", "cold_plate": "Al", "heater_block": "Al",
    # Rev B (ICR-8, I-10): parts within ~40 mm of a magnet are non-magnetic
    "pins": "Nitronic 60 (UNS S21800) valve pins; fallback 1.4404 solution-annealed; incoming check mu_r <= 1.02 "
            "with a permeability indicator [assessment; permeability UNVERIFIED]",
    "pin_springs": "Co-Cr-Ni spring wire (Elgiloy/Phynox class, non-magnetic; G and strength comparable to 1.4310, "
                   "UNVERIFIED) -- NOT 1.4310 (work-hardened 1.4310 is partly martensitic, magnetic)",
    "yokes_spring_plate_buttons": "1.4404 (not 1.4310/1.4301)",
    "guides": "CuSn8 bearing bronze (docs/20 DEV-U4)", "datum_pins": "zirconia (docs/21 CHOICE-L9)",
    "head_guide_pins": "1.2842 hardened, ferromagnetic -- allowed: >= 45 mm from every magnet position",
    "magnet": "NdFeB", "pogo": "Au/CuBe", "insulator": "PEEK",
}
NON_MAGNETIC_RADIUS = 40.0     # Rev B [assessment]: no ferromagnetic part within 40 mm of a magnet working position
