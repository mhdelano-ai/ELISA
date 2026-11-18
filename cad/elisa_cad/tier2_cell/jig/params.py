"""Dimensions of the punching jig for the retainer washer T2C-004 (docs/36).  Single source of truth for
`parts.py` and `build.py`.  No CadQuery import here.

The jig punches the washer's hole first, then its outside, on one axis and without moving the sheet: the punch
tube is guided by a hardened slip bushing; the two slip bushings (one per punch) are interchangeable in one liner
bushing bonded into the printed head plate, and a swing finger keeps the bushing down while the punch is withdrawn.
The head plate stands on the strip with a foot around the liner and is pulled down by four thumb screws (force-set
clamp: a thin rubber sheet under a wide rigid foot is nearly incompressible, so the plate floats on the sheet and
friction holds it).  Each punch tube is bonded into a handle whose nose lands on the bushing head: the stroke ends
at a fixed depth in the backing.  Between washers the thumb screws are loosened and the strip is pushed on by one
pitch.

Revision B (review round 1, results/tier_round/review_jig_r1.md): swing finger instead of a locked washer (R1-1);
liner hole 8.00 H7 with a bonding gap, lock insert moved out to a 2.0 wall, inserts not in SLA (R1-2); handle with a
nose stop and a shoulder for each tube (R1-3, R1-5); bushing C and the Rapid-Core fallback removed from the jig
(R1-4); plate 0.3 thinner than the liner so the bushing head seats on steel (R1-8); four thumb screws (R1-9); scale
on the hole positions (R1-10); M3 x 20 screws (R1-12); dowel holes reamed (R1-13).

Units mm.  Coordinates: origin on the punch axis, z = 0 on the top face of the base (the datum on which the
backing strip and the sheet lie); +x is the feed direction of the strip, y across it, z up.

Source tags: as in ../params.py.  [J-src n] = item n of results/tier_round/punch_jig_sourcing.md (vendor page read
in the session of 2026-11-18); [R1-n] = finding n of review round 1; CHOICE = design choice of docs/36; Derived;
UNVERIFIED = not checked, measure or confirm before use.
"""
from __future__ import annotations

import math

from .. import params as P2

IN = 25.4

# ---- the part --------------------------------------------------------------------------------------------------
WASHER_ID, WASHER_OD, SHEET_T = P2.WASHER_ID, P2.WASHER_OD, P2.WASHER_T     # drawing T2C-004
SHEET_T_TOL = P2.WASHER_T_TOL
CONC_LIMIT = 0.10                      # T2C-004: hole concentric to the outside within dia 0.10 (offset <= 0.05)

# ---- punches (bought; [J-src 1, 2]) ---------------------------------------------------------------------------------
# SYNEO C-Series catheter punches: straight 304 SS tubes, hard temper, TiN, "middle" cutting edge (between bore and
# outside), 1.500 in long, no handle, no ejector [syneoco.com/catheter-punches, page read twice]; tube tolerances,
# straightness, edge runout and price not stated (RFQ).  For the outside punch the RFQ asks first for an INSIDE edge
# (bore = edge 0.055 in; the washer is then not squeezed into the bore) [R1-6]; the catalogue middle edge is
# modelled because its dimensions are confirmed.
PUNCH_A = dict(name="hole punch (SYNEO CR0350275N20R4)", cut_d=0.030 * IN, bore=0.027 * IN, tube_od=0.035 * IN,
               tube_l=1.500 * IN)
PUNCH_B = dict(name="outside punch (SYNEO CR0650495N16R4)", cut_d=0.055 * IN, bore=0.049 * IN, tube_od=0.065 * IN,
               tube_l=1.500 * IN)
PUNCH_TIP_RUNOUT = 0.010               # UNVERIFIED: cutting edge to tube outside, radial (measure, docs/36 section 5)
PUNCH_OD_TOL = 0.0025                  # the bore is ordered to the MEASURED tube (+-0.0025 = micrometer reading)
SHEET_SHIFT = 0.010                    # UNVERIFIED allowance: sheet moved by the bushing swap or the withdrawal [R1-7]

# ---- handle (printed J-003, one per tube) ---------------------------------------------------------------------------
# A nose that lands on the bushing head (the stroke's end) and a mushroom grip.  The tube sits in a drilled pocket and
# bears on a shoulder; the push-wire hole beyond the shoulder is the tube's bore + 0.02, so the shoulder carries the
# whole tube wall [R1-3].
NOSE_D, NOSE_L = 6.0, 7.5              # CHOICE: nose clears the swing finger (nose r 3.0 < finger tip r 3.4) and its
#                                        top clears the lock screw head (Derived, checked)
GRIP_D, GRIP_L = 16.0, 22.0            # CHOICE: mushroom grip [R1-19]
PUSH_HOLE_EXTRA = 0.02                 # CHOICE: push-wire hole = tube bore + 0.02 (drilled)
POCKET_CLEAR = 0.03                    # CHOICE: tube pocket = tube + 0.03, drilled; bonded with epoxy [R1-3, R1-20]
PUSH_WIRE = {"A": 0.60, "B": 1.10}     # CHOICE: stainless wire or gauge pin, < bore (0.686 / 1.245)

# ---- liner and slip bushings (bought, hardened; Carr Lane; [J-src 4]) -----------------------------------------------
# Slip/fixed renewable bushing SF-12-8-<ID>-NCB: body OD 3/16 in (0/-0.0002 in), 1/2 in long, head dia 5/16 x 3/16 in
# (head thickness from amesweb), bore to order 0.0135-0.0980 in in 0.0001 in steps, +0.0001/+0.0004 in, Rc 62-64;
# -NCB = no counterbore (the bore guides over the whole length).  Liner L-20-8: ID 3/16 in +0.0001/+0.0004,
# OD 5/16 in +0.0013/+0.0016 in, 1/2 in long.  The head's lock and slip recesses are not modelled: the swing finger
# bears on the head's full rim away from the recesses (turn the recesses away from the finger) [R1-1].
LINER_ID, LINER_OD_NOM, LINER_L = 0.1875 * IN, 0.3125 * IN, 0.500 * IN
LINER_ID_TOL = (0.0001 * IN, 0.0004 * IN)
LINER_OD_TOL = (0.0013 * IN, 0.0016 * IN)
LINER_OD = LINER_OD_NOM + LINER_OD_TOL[1]                 # 7.978: modelled at its largest [R1-2]
SLIP_OD_TOL = (-0.0002 * IN, 0.0)
SLIP_HEAD_D, SLIP_HEAD_H = 0.3125 * IN, 0.1875 * IN
SLIP_BORE_CLEAR = 0.0002 * IN          # CHOICE: bore ordered = measured tube outside + 0.0002 in [R1-7]
SLIP_BORE_TOL = (0.0001 * IN, 0.0004 * IN)
SLIP_RUNOUT = 0.005                    # UNVERIFIED: bore to body, radial (concentricity not stated by Carr Lane)
SLIP_L_TOL = 0.1                       # UNVERIFIED: bushing length and head tolerance (taken out at assembly)
LINER_HOLE_D = 8.00                    # CHOICE: printed 7.8, reamed 8.00 H7 (0 / +0.015); gap 0.022-0.045 for a
#                                        gap-filling retaining compound or epoxy [R1-2]
LINER_PROUD = 0.3                      # CHOICE: liner stands 0.3 above the plate top: the bushing head seats on the
#                                        liner end, steel on steel [R1-8]
# Swing finger (J-005, printed PA12 or cut from 2.5 mm aluminium): pivots on a sleeve (J-004) clamped by an M3 screw
# into an insert in the plate; it lies 0.1 above the bushing head, so it retains the bushing (no clamp) and swings
# 90 degrees to free it.
LOCK_R, LOCK_ANGLE = 8.0, 90.0         # CHOICE: pivot axis 8.0 from the punch axis, at +y [R1-2]
FINGER_T, FINGER_W, FINGER_TIP_R = 2.5, 5.0, 3.4   # CHOICE: tip 3.4 from the punch axis: overlap 0.57 on the head
FINGER_GAP = 0.10                      # CHOICE: above the head
SLEEVE_D, SLEEVE_ID = 5.0, 3.2         # CHOICE: printed or steel round spacer; the finger's hole 5.2 runs on it
LOCK_SCREW_L, LOCK_HEAD_D, LOCK_HEAD_H = 14.0, 5.5, 3.0   # M3 x 14 socket head (ISO 4762) with a DIN 125 washer
LOCK_WASHER_D, LOCK_WASHER_T = 7.0, 0.5

# ---- workpiece ---------------------------------------------------------------------------------------------------
BACKING_T, BACKING_T_TOL = 0.79, 0.05  # HDPE sheet 1/32 in +-0.002 in, McMaster 8619K561 [J-src 5]; the punch ends in it
STRIP_W = 14.0                         # CHOICE: FKM and backing cut to strips 14 wide (scalpel and rule)
STRIP_L = 100.0                        # CHOICE: about 30 washers per strip at the pitch below
PITCH = 3.0                            # CHOICE: washer spacing along the strip (web 1.6 between outsides)
TIP_INTO_BACKING = 0.25                # CHOICE: nominal stop: tip 0.25 into the 0.79 backing (0.15-0.35, tip_depth_range)
STOP_SET_TOL = 0.05                    # CHOICE: each handle's protrusion is set against ITS bushing at assembly
#                                        (face the nose, check with test punches in a scrap strip) to +-0.05

# ---- base (printed: MJF PA12 or FDM PETG/ASA; not SLA, the inserts are heat-set) [R1-2] -----------------------------
BASE_X, BASE_Y, BASE_T = 80.0, 48.0, 10.0      # CHOICE: x from -40 to +40
RAIL_GAP = 0.6                         # CHOICE: strip guide, 0.3 each side
RAIL_W, RAIL_H = 1.5, 0.30             # CHOICE: printed rails on the base top; lower than the strip
SCALE_X0, SCALE_X1, SCALE_TICK = 21.0, 39.0, (0.4, 1.2, 0.3)   # CHOICE: ticks on the hole positions (multiples of
#                                        PITCH) downstream of the plate; long tick at 30 [R1-10]

# ---- head plate (printed, same process as the base) ---------------------------------------------------------------
PLATE_X, PLATE_Y = 40.0, 40.0          # CHOICE
FOOT_WALL = 1.5                        # CHOICE: printed ring around the liner at the foot
RECESS_HALF_W, RECESS_DEPTH = 10.0, 1.0   # CHOICE: underside relief over the strip, except the foot
SCREW_FORCE = (50.0, 400.0)            # N per thumb screw, finger tight: range (UNVERIFIED) [R1-9]
MU_SHEET = 0.3                         # friction FKM on HDPE and on PA12, lower bound (UNVERIFIED)

DOWEL_D, DOWEL_L, DOWEL_IN_BASE = 3.0, 12.0, 6.0   # 3 m6 x 12 hardened pins, McMaster 91595A112 [J-src 5]
DOWEL_XY = [(0.0, 17.0), (0.0, -17.0)]             # CHOICE: round hole at the first, slot along y at the second;
#                                                    plate and base holes printed 2.8 and reamed 3.0 H8 [R1-13]
SLOT_L = 1.0                           # CHOICE: extra length of the slot
SCREW_XY = [(15.0, 16.0), (-15.0, 16.0), (15.0, -16.0), (-15.0, -16.0)]   # CHOICE: four M3 thumb screws [R1-9]
SCREW_D, SCREW_CLEAR = 3.0, 3.4
INSERT_HOLE_D, INSERT_L, INSERT_WALL = 4.0, 5.7, 1.6     # ruthex RX-M3x5.7: hole 4.0, minimum wall 1.6 [J-src 5]
INSERT_HOLE_DEPTH = 7.5                # CHOICE: blind hole below the insert, for the screw end [R1-12]
THUMB_HEAD_D, THUMB_HEAD_H, SCREW_L = 12.0, 7.5, 20.0   # M3 x 20 knurled thumb screw DIN 464 (head UNVERIFIED) [R1-12]


# ---- derived ----------------------------------------------------------------------------------------------------
Z_FOOT = BACKING_T + SHEET_T                     # underside of the plate = foot face = sheet top (nominal stack)
PLATE_T = LINER_L - LINER_PROUD                  # the liner runs through the plate, flush at the foot
Z_PLATE_TOP = Z_FOOT + PLATE_T
Z_LINER_TOP = Z_FOOT + LINER_L
Z_HEAD_TOP = Z_LINER_TOP + SLIP_HEAD_H           # the handle's nose lands here
FOOT_D = LINER_HOLE_D + 2.0 * FOOT_WALL
Z_SHEET0 = BACKING_T                             # underside of the sheet
Z_TIP = BACKING_T - TIP_INTO_BACKING             # punch tip at the bottom of the stroke
Z_FINGER0 = Z_HEAD_TOP + FINGER_GAP
Z_SLEEVE_TOP = Z_FINGER0 + FINGER_T + 0.1        # the finger turns on the sleeve, under the screw's washer
LOCK_XY = (LOCK_R * math.cos(math.radians(LOCK_ANGLE)), LOCK_R * math.sin(math.radians(LOCK_ANGLE)))


def slip_bore(punch):
    return punch["tube_od"] + SLIP_BORE_CLEAR


def protrusion():
    """Tube length below the nose face: from the bushing head top to the tip at the end of the stroke."""
    return Z_HEAD_TOP - Z_TIP


def pocket_depth(punch):
    """Tube length inside the handle: the tube bears on the pocket's shoulder."""
    return punch["tube_l"] - protrusion()


def tip_depth_range():
    """Tip depth into the backing.  The plate rides on the sheet and the nose lands on the bushing head, so
    depth = protrusion - sheet - liner - head: the backing's thickness cancels; the bushing's length tolerance is
    taken out by setting each handle against its own bushing (STOP_SET_TOL); the sheet's tolerance remains."""
    return TIP_INTO_BACKING - SHEET_T_TOL - STOP_SET_TOL, TIP_INTO_BACKING + SHEET_T_TOL + STOP_SET_TOL


def concentricity_budget():
    """Radial offset between hole and outside: each stroke adds liner/slip play, slip runout, punch/bore play and
    tip runout; the two strokes are independent; plus one allowance for the sheet moving at the swap.  Returns
    worst case and root-sum-square (mm, radial)."""
    liner_slip = (LINER_ID_TOL[1] - SLIP_OD_TOL[0]) / 2.0        # largest radial play (slip body in the liner)
    per = []
    for _p in (PUNCH_A, PUNCH_B):
        bore_play = (SLIP_BORE_CLEAR + SLIP_BORE_TOL[1] + 2 * PUNCH_OD_TOL) / 2.0
        per += [liner_slip, SLIP_RUNOUT, bore_play, PUNCH_TIP_RUNOUT]
    per.append(SHEET_SHIFT)
    worst = sum(per)
    rss = math.sqrt(sum(v * v for v in per))
    return worst, rss
