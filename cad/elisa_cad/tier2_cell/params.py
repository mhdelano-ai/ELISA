"""Dimensions of the tier-2 flow cell with the bead bed inside the cell (docs/34).  Single source of truth:
`parts.py` (CadQuery), `section.py` (figure) and `scripts/tier_round/tier2_cell.py` (model, hydraulics, mechanics)
all read this file.  No CadQuery import here.

Units mm.  Coordinates: origin on the axis of the working electrode, z = 0 on the top face of the base (the datum
on which the nozzle plate rests); +x towards the contact pads of the strip, y across the strip, z up.

Source tags: [V docs/28] = vendor document read in the tier round; [V] = read in this session (docs/34 section 9);
[S] = search summary only; CHOICE = design choice of docs/34; Derived; UNVERIFIED = not checked, measure or confirm
before ordering.
"""
from __future__ import annotations

import math

# ---- the electrode strip (MicruX S1PE, e.g. ED-S1PE-C21) ---------------------------------------------------
STRIP_L, STRIP_W = 27.5, 10.1          # [V docs/28 section 2.1]
STRIP_T = 0.38                         # ceramic (Al2O3) strip, e.g. ED-S1PE-C21C: 380 um, stated by the user 2026-11-18;
#                                        the substrate thickness is also on MicruX's drawing [V docs/28]
WE_D = 3.0                             # [V docs/28]
WE_FROM_FREE_END = 8.26                # MicruX drawing "Thick-film based-electrode features" (user, 2026-11-18),
#                                        measured to scale: 17.13 px/mm from the 10.1 mm width gives 27.50 mm length;
#                                        the user confirmed the drawing is accurate
PRINT_R_MAX = 3.65                     # same drawing: outer radius of the printed counter (arc) and reference
#                                        (sector) electrodes, 3.64 mm; inner radius of both 2.56-2.59 mm
PADS_FROM_FREE_END = 21.78             # same drawing: end of the printed (red) area = start of the four contact pads
#                                        (pads 5.7 mm long, 4 pads within +-4.8 mm of the axis)

# ---- stack -----------------------------------------------------------------------------------------------
X0, X1 = -17.0, 12.0                   # CHOICE: body, plate and base from x = -17 to +12; the pads start at +13.5
Y_HALF = 22.0                          # CHOICE: 44 mm across
BASE_T, PLATE_T, BODY_T = 8.0, 2.5, 12.0   # CHOICE
EDGE_CHAMFER = 0.5

# ---- base (316L) ------------------------------------------------------------------------------------------
POCKET_W = STRIP_W + 0.2               # CHOICE: strip pocket, open at +x
POCKET_DEPTH = 0.55                    # CHOICE: strip + shim + gap; deep enough for the ceramic strip (0.38) too
POCKET_X_END = -(WE_FROM_FREE_END + 0.1)   # Derived: closed end of the pocket is the stop for the strip
POCKET_RELIEF_D = 1.6                  # CHOICE: corner reliefs at the closed end
SHIM_T = 0.07                          # CHOICE: shim stock under the ceramic strip (0.05 + 0.02); sets the gap.
#                                        A PET strip (0.25 + print) would take about 0.18

GAP = POCKET_DEPTH - STRIP_T - SHIM_T  # Derived: 0.10 mm liquid layer over the electrode
GAP_TOL = 0.05                         # Derived (docs/34 section 5.3): pocket, strip and shim tolerances

# ---- fasteners and pins -----------------------------------------------------------------------------------
M4_XY = [(-12.0, -16.0), (-12.0, 16.0), (8.0, -16.0), (8.0, 16.0)]   # CHOICE: main screws, into the base
M4_CLEAR, M4_TAP_DRILL, M4_HEAD_D = 4.3, 3.3, 7.0
DOWEL_XY = [(-2.0, -16.0), (-2.0, 16.0)]                              # CHOICE: 3 mm pins, pressed into the base
DOWEL_D = 3.0
M25_XY = [(-12.0, -7.0), (-12.0, 7.0), (8.0, -7.0), (8.0, 7.0)]      # CHOICE: plate to body, heads in the plate
M25_CLEAR, M25_TAP_DRILL, M25_CSK_D, M25_THREAD_DEPTH = 2.7, 2.05, 5.0, 7.0

# ---- nozzle plate (PEEK), underside = cell face -------------------------------------------------------------
EXIT_D = 0.5                           # CHOICE: exit bore on the electrode axis, through the plate
ORING_STRIP = (7.0, 1.0)               # CHOICE: O-ring I.D. x cross-section on the strip (UNVERIFIED fit, see above)
GROOVE_STRIP_ID, GROOVE_STRIP_OD, GROOVE_STRIP_DEPTH = 6.9, 9.3, 0.65   # Derived: 25 % squeeze at the nominal gap
RING_R0, RING_R1, RING_DEPTH = 2.3, 2.9, 0.5       # CHOICE: collecting groove around the electrode
RISER_PLATE_X, RISER_PLATE_D = -2.6, 0.6           # CHOICE: from the collecting groove up through the plate
CHANNEL_X_END, CHANNEL_W, CHANNEL_DEPTH = -4.6, 0.8, 0.5   # CHOICE: slot in the top face of the plate
# Retainer pocket in the top face of the plate (Revision B, docs/34 section 3.1): from the bottom, an elastomer
# washer (the spring), the screen, the membrane.  The washer pushes screen and membrane up against the flat
# underside of the body around the bed bore; nothing stands proud of the plate, so body and plate meet face to
# face and the plate stays flat.
RET_POCKET_D = 1.65                    # CHOICE: guides the 1/16 in screen
RET_POCKET_DEPTH = 0.27                # CHOICE, +-0.01: washer compressed + screen + membrane
WASHER_OD, WASHER_ID, WASHER_T = 1.2, 0.75, 0.25   # CHOICE: punched from 0.25 mm FKM sheet (+-0.02, UNVERIFIED)
#                                        with 1.2 and 0.75 mm biopsy punches (sizes UNVERIFIED)

# ---- body (PEEK) -------------------------------------------------------------------------------------------
BED_D = 0.5                            # CHOICE: bed bore = floor of the inlet port (0.3 as a variant, docs/34 6.3)
PORT_THREAD = "1/4-28 UNF-2B"
PORT_MAJOR_D, PORT_TAP_DRILL = 6.35, 5.5          # thread standard; tap drill for 1/4-28 (No. 3, 5.41 mm) rounded
PORT_DEPTH = 9.5                       # UNVERIFIED: take the depth and the flat-bottom finish from the fitting
#                                        maker's port drawing (IDEX "1/4-28 Standard Flat-Bottom Port")
INLET_FLOOR = BODY_T - PORT_DEPTH      # Derived: 2.5 mm = length of the bed bore
ORING_IFACE = (12.0, 1.0)              # CHOICE: body-to-plate O-ring
GROOVE_IFACE_ID, GROOVE_IFACE_OD, GROOVE_IFACE_DEPTH = 11.9, 14.3, 0.75
RISER_BODY_X, RISER_BODY_D = -4.6, 1.0
OUTLET_Z = 7.0                         # CHOICE: axis of the outlet port above the body underside, on the -x face
OUTLET_THROUGH_D = 0.8

# ---- purchased parts in the liquid path ----------------------------------------------------------------------
SCREEN_D, SCREEN_T = 1.5875, 0.075     # VICI 2SR1-10: 1/16 in, 2 um nominal, 0.075 mm [V]
MEMBRANE_T = 0.010                     # track-etched polycarbonate, 1 um pores; 6-15 um thick [S], taken as 10
MEMBRANE_PORES_PER_MM2 = 2.0e5         # 2e7 per cm2 for 1 um pores [S]
MEMBRANE_PORE_D = 1.0e-3
MEMBRANE_DISC_D = 1.5                  # CHOICE: punched; lies on the screen inside the pocket

# ---- derived quantities used by the model script ------------------------------------------------------------
def area_circle(d):
    return math.pi * d * d / 4.0


BORE_AREA = area_circle(BED_D)                                  # mm2
WASHER_H = RET_POCKET_DEPTH - SCREEN_T - MEMBRANE_T              # compressed height of the washer (0.185)
WASHER_SQUEEZE = 1.0 - WASHER_H / WASHER_T                      # 0.26 nominal
EXIT_LENGTH = PLATE_T - RET_POCKET_DEPTH                        # exit bore from the pocket floor to the cell face
EXIT_WALL = math.pi * EXIT_D * EXIT_LENGTH                      # mm2 of PEEK between retainer and electrode
WASHER_WALL = math.pi * WASHER_ID * WASHER_H                    # mm2 of elastomer between retainer and electrode
EXIT_VOLUME_UL = area_circle(EXIT_D) * EXIT_LENGTH + area_circle(WASHER_ID) * WASHER_H   # mm3 = uL
CHAMBER_R = GROOVE_STRIP_ID / 2.0                               # liquid disc under the plate
