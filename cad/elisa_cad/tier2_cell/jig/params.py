"""Dimensions of the punching jig for the retainer washer T2C-004 (docs/36).  Single source of truth for
`parts.py` and `build.py`.  No CadQuery import here.

The jig punches the washer's hole first, then its outside, on one axis and without moving the sheet: the punch
tube is guided by a hardened slip bushing; the two slip bushings (one per punch) are interchangeable in one liner
bushing bonded into the printed head plate.  The head plate clamps the sheet locally with its foot (the end face
of the liner and slip bushing), pulled down by two thumb screws: the plate floats on the sheet (force-set clamp,
not a set squeeze: a thin rubber sheet under a wide rigid foot is nearly incompressible, so a shim-set squeeze
would need tens of kN), and friction holds the sheet so that it cannot move between the two strokes.  Between
washers the thumb screws are loosened and the strip is pushed on by one pitch.

Units mm.  Coordinates: origin on the punch axis, z = 0 on the top face of the base (the datum on which the
backing strip and the sheet lie); +x is the feed direction of the strip, y across it, z up.

Source tags: as in ../params.py.  [J-src n] = row n of results/tier_round/punch_jig_sourcing.md (vendor page read
in the session of 2026-11-18); CHOICE = design choice of docs/36; Derived; UNVERIFIED = not checked, measure or
confirm before use.
"""
from __future__ import annotations

import math

from .. import params as P2

# ---- the part --------------------------------------------------------------------------------------------------
WASHER_ID, WASHER_OD, SHEET_T = P2.WASHER_ID, P2.WASHER_OD, P2.WASHER_T     # drawing T2C-004
SHEET_T_TOL = P2.WASHER_T_TOL
CONC_LIMIT = 0.10                      # T2C-004: hole concentric to the outside within dia 0.10 (offset <= 0.05)
MEMBRANE_DISC_D = P2.MEMBRANE_DISC_D   # 1.5: the jig also punches the membrane disc (outside punch only)

# ---- punches (bought; results/tier_round/punch_jig_sourcing.md, items 1-3) --------------------------------------------
IN = 25.4
# SYNEO C-Series catheter punches: straight 304 SS tubes, hard temper, TiN, "middle" cutting edge (between bore and
# outside), 1.500 in long, no handle, no ejector [J-src 1, 2: syneoco.com/catheter-punches, page read]; tube
# tolerances, edge runout and price not stated (RFQ).  Each tube is bonded into a printed handle J-003.
PUNCH_A = dict(name="hole punch (SYNEO CR0350275N20R4)", cut_d=0.030 * IN, bore=0.027 * IN, tube_od=0.035 * IN,
               tube_l=1.500 * IN)
PUNCH_B = dict(name="outside punch (SYNEO CR0650495N16R4)", cut_d=0.055 * IN, bore=0.049 * IN, tube_od=0.065 * IN,
               tube_l=1.500 * IN)
# Membrane disc (dia 1.5): Rapid-Core 1.5 (Ted Pella 15115-5), cutting dia 1.50, tube OD 1.90, own handle with
# push-button ejector [J-src 3, page]; exposed cannula length not published (UNVERIFIED): a third slip bushing C.
PUNCH_C = dict(name="membrane punch (Rapid-Core 1.5, Ted Pella 15115-5)", cut_d=1.50, bore=1.50, tube_od=1.90,
               tube_l=None)
PUNCH_TIP_RUNOUT = 0.010               # UNVERIFIED: cutting edge to tube outside, radial (straight ground tube;
#                                        measure under the microscope, docs/36 section 5)
PUNCH_OD_TOL = 0.0025                  # the bore is ordered to the MEASURED tube (+-0.0025 = micrometer reading)

# ---- handle (printed J-003): the tube is bonded into it; a push wire ejects the part through the tube --------------
HANDLE_D, HANDLE_L, TUBE_IN_HANDLE = 10.0, 30.0, 10.0   # CHOICE
PUSH_WIRE = {"A": 0.60, "B": 1.10}     # CHOICE: stainless wire or gauge pin, < bore (0.686 / 1.245)

# ---- liner and slip bushings (bought, hardened; Carr Lane; [J-src 4]) -----------------------------------------------
# Slip/fixed renewable bushing SF-12-8-<ID>-NCB: body OD 3/16 in (0/-0.0002 in), 1/2 in long, head dia 5/16 x 3/16 in
# (head thickness from amesweb), bore to order 0.0135-0.0980 in in 0.0001 in steps, +0.0001/+0.0004 in, Rc 62-64;
# -NCB = no counterbore (the bore guides over the whole length).  Liner L-20-8: ID 3/16 in +0.0001/+0.0004,
# OD 5/16 in +0.0016/+0.0013 (press fit), 1/2 in long.  Lock screw LS-0 at 17/64 in from the axis (thread 8-32,
# UNVERIFIED): here an M3 screw with a DIN 125 washer clamps the bushing head instead (CHOICE).
LINER_ID, LINER_OD, LINER_L = 0.1875 * IN, 0.3125 * IN, 0.500 * IN
LINER_ID_TOL = (0.0001 * IN, 0.0004 * IN)
LINER_OD_TOL = (0.0013 * IN, 0.0016 * IN)
SLIP_OD_TOL = (-0.0002 * IN, 0.0)
SLIP_HEAD_D, SLIP_HEAD_H = 0.3125 * IN, 0.1875 * IN
SLIP_BORE_CLEAR = 0.0003 * IN          # CHOICE: bore ordered = measured tube outside + 0.0003 in (0.008 mm)
SLIP_BORE_TOL = (0.0001 * IN, 0.0004 * IN)
SLIP_RUNOUT = 0.005                    # UNVERIFIED: bore to body, radial (concentricity not stated by Carr Lane)
LINER_HOLE_D = 7.95                    # CHOICE: printed, reamed to 7.95-7.96, liner bonded (retaining compound)
LOCK_R = 17.0 / 64.0 * IN              # 6.75 mm: lock screw axis from the bushing axis (Carr Lane LS-0 position)
LOCK_ANGLE = 90.0                      # CHOICE: lock screw at +y (away from the strip feed)
LOCK_SPACER_D, LOCK_SCREW_L = 5.4, 10.0   # CHOICE: spacer ring (printed) under the washer; M3 x 10 socket head
LOCK_WASHER_D = 7.0                    # DIN 125 M3 washer: overlaps the bushing head by 7/2 - (6.75 - 3.97) = 0.72

# ---- workpiece ---------------------------------------------------------------------------------------------------
BACKING_T, BACKING_T_TOL = 0.79, 0.05  # HDPE sheet 1/32 in +-0.002 in, McMaster 8619K561 [J-src 5]; the punch ends in it
STRIP_W = 14.0                         # CHOICE: FKM and backing cut to strips 14 wide (scalpel and rule)
STRIP_L = 100.0                        # CHOICE: about 30 washers per strip at the pitch below
PITCH = 3.0                            # CHOICE: washer spacing along the strip (web 1.5 between outsides)
TIP_INTO_BACKING = 0.15                # CHOICE: the punch is pushed through the sheet and 0.15 into the backing

# ---- base (printed) ----------------------------------------------------------------------------------------------
BASE_X, BASE_Y, BASE_T = 80.0, 48.0, 10.0      # CHOICE: x from -40 to +40
RAIL_GAP = 0.6                         # CHOICE: strip guide, 0.3 each side
RAIL_W, RAIL_H = 1.5, 0.30             # CHOICE: printed rails on the base top; lower than the clamped workpiece
SCALE_X0, SCALE_X1, SCALE_TICK = 22.0, 38.0, (0.4, 1.2, 0.3)   # CHOICE: ticks at PITCH beside the rail, x > plate

# ---- head plate (printed) ----------------------------------------------------------------------------------------
PLATE_X, PLATE_Y = 40.0, 40.0          # CHOICE
FOOT_WALL = 1.5                        # CHOICE: printed ring around the liner at the foot
RECESS_HALF_W, RECESS_DEPTH = 10.0, 1.0   # CHOICE: underside relief over the strip, except the foot
SCREW_FORCE = 50.0                     # N per thumb screw, finger tight (UNVERIFIED; a light turn is enough)
MU_SHEET = 0.3                         # friction FKM on PP and on steel/resin, lower bound (UNVERIFIED)

DOWEL_D, DOWEL_L, DOWEL_IN_BASE = 3.0, 12.0, 6.0   # 3 m6 x 12 hardened pins, McMaster 91595A112 [J-src 5]
DOWEL_XY = [(-15.0, 16.0), (15.0, -16.0)]          # CHOICE: round hole at the first, slot along the line at the second
DOWEL_HOLE_CLEAR = 0.05                # CHOICE: printed hole 3.05 in the plate (reamed 3.0 H8 + 0.05 if needed)
SCREW_XY = [(15.0, 16.0), (-15.0, -16.0)]          # CHOICE: M3 thumb screws into heat-set inserts in the base
SCREW_D, SCREW_CLEAR = 3.0, 3.4
INSERT_HOLE_D, INSERT_L = 4.0, 5.7     # ruthex RX-M3x5.7, hole dia 4.0 [J-src 5]
THUMB_HEAD_D, THUMB_HEAD_H, SCREW_L = 12.0, 7.5, 18.0   # M3 x 18 knurled thumb screw DIN 464 (head UNVERIFIED;
#                                        McMaster 92558A330 is M3 x 12: check its head before ordering, docs/36)


# ---- derived ----------------------------------------------------------------------------------------------------
Z_FOOT = BACKING_T + SHEET_T                     # underside of the plate = foot face = sheet top (nominal stack)
PLATE_T = LINER_L                                # the liner runs through the plate, flush at both faces
Z_PLATE_TOP = Z_FOOT + PLATE_T
FOOT_D = LINER_OD + 2.0 * FOOT_WALL
Z_SHEET0 = BACKING_T                             # underside of the sheet
Z_TIP = BACKING_T - TIP_INTO_BACKING             # punch tip at the bottom of the stroke


def slip_bore(punch):
    return punch["tube_od"] + SLIP_BORE_CLEAR


def exposed(punch):
    return punch["tube_l"] - TUBE_IN_HANDLE if punch["tube_l"] else None


def reach_needed():
    """Exposed tube length needed: from the head top of the slip bushing to the tip at the bottom of the stroke,
    plus 3 mm so that the handle never lands on the bushing (the stroke ends in the backing, felt by hand)."""
    return Z_PLATE_TOP + SLIP_HEAD_H - Z_TIP + 3.0


def concentricity_budget():
    """Radial offset between hole and outside: each stroke adds liner/slip play, slip runout, punch/bore play and
    tip runout; the two strokes are independent.  Returns worst case and root-sum-square (mm, radial)."""
    liner_slip = (LINER_ID_TOL[1] - SLIP_OD_TOL[0]) / 2.0        # largest radial play (slip body in the liner)
    per = []
    for p in (PUNCH_A, PUNCH_B):
        bore_play = (SLIP_BORE_CLEAR + SLIP_BORE_TOL[1] + 2 * PUNCH_OD_TOL) / 2.0
        per += [liner_slip, SLIP_RUNOUT, bore_play, PUNCH_TIP_RUNOUT]
    worst = sum(per)
    rss = math.sqrt(sum(v * v for v in per))
    return worst, rss
