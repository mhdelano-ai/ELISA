"""Dimensions of the punching jig for the retainer washer T2C-004 (docs/36).  Single source of truth for
`parts.py` and `build.py`.  No CadQuery import here.

The jig punches the washer's hole first, then its outside, on one axis and without moving the sheet: the punch
tube is guided by a hardened slip bushing; the two slip bushings (one per punch) are interchangeable in one liner
bushing bonded into the printed head plate; a ring finger on a shoulder screw keeps the bushing down while the
punch is withdrawn.  The head plate stands on the strip with a foot around the bushing and is pulled down by four
thumb screws (force-set clamp: a thin rubber sheet under a wide rigid foot is nearly incompressible, so the plate
floats on the sheet and friction holds it).  Each punch tube is bonded into a handle whose nose lands on the bushing
head: the stroke ends at a fixed depth in the backing.  Between washers the thumb screws are loosened and the strip
is pushed on by one pitch.

Revision B (review round 1, results/tier_round/review_jig_r1.md): swing finger, liner bond gap, handle shoulders,
nose stop, four screws, Rapid-Core out of the jig, scale on the hole positions, M3 x 20 screws.
Revision C (review round 2, review_jig_r2.md): bushing tolerances +-1/64 in (amesweb) used everywhere [R2-9];
liner one size shorter (L-20-6) and bonded with the bushing face flush with the foot, so the bushing's own face
clamps the sheet whatever the lengths [R2-1]; ring finger bearing on the whole head rim (recesses anywhere) [R2-3];
pivot at 9.5 on an ISO 7379 shoulder screw, finger height set at assembly by facing a spacer and with shim rings
[R2-2, R2-4, R2-7]; nose printed long and faced to set the depth [R2-5]; pin fits [R2-8]; parking holes [R2-12].
Revision D (review round 3, review_jig_r3.md): bonding procedure with paste epoxy, release film and two flats
(docs/36 section 2.4) [R3-1, R3-2]; ledge gap 1.4 with the plate's print tolerance [R3-3]; finger swing checked over
its real range (stops on a thumb head near 75 deg) [R3-4]; finger preloaded by an O-ring, gap 0.05 [R3-5]; shoulder
screw head 7 x 3, thread 7 (Ganter GN 35215) [R3-7]; stock sheet +-0.08, ring lead-in chamfer modelled, parking bosses
[R3-8, R3-10].

Units mm.  Coordinates: origin on the punch axis, z = 0 on the top face of the base (the datum on which the
backing strip and the sheet lie); +x is the feed direction of the strip, y across it, z up.

Source tags: as in ../params.py.  [J-src n] = item n of results/tier_round/punch_jig_sourcing.md (vendor page read
in the session of 2026-11-18); [R1-n], [R2-n] = findings of review rounds 1 and 2; CHOICE = design choice of
docs/36; Derived; UNVERIFIED = not checked, measure or confirm before use.
"""
from __future__ import annotations

import math

from .. import params as P2

IN = 25.4

# ---- the part --------------------------------------------------------------------------------------------------
WASHER_ID, WASHER_OD, SHEET_T = P2.WASHER_ID, P2.WASHER_OD, P2.WASHER_T     # drawing T2C-004
SHEET_T_TOL = 0.08                     # the stock sheet (J-Flex 0.25 +-0.08 [J-src 6]); washers are sorted to the
#                                        drawing's +-0.05 afterwards [R3-8]
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
TUBE_L_TOL = 0.1                       # UNVERIFIED: tube length (the depth is set per handle, so it only costs facing)

# ---- handle (printed J-003, one per tube) ---------------------------------------------------------------------------
# A nose that lands on the bushing head (the stroke's end) and a mushroom grip.  The tube sits in a pocket drilled on
# a drill press or lathe and is located by a shoulder; the epoxy bond carries the load [R2-6].  The nose is printed
# NOSE_ALLOW longer and faced down at assembly until the depth is right [R2-5].
NOSE_D, NOSE_L = 5.0, 10.0             # CHOICE: as set; nose r 2.5 inside the finger ring (r 3.2); grip above the
#                                        shoulder-screw head (Derived, checked)
NOSE_ALLOW = 1.2                       # CHOICE: printed extra length, faced at assembly (covers head +-0.4, body
#                                        +-0.4 if unmatched, pocket +-0.2, tube +-0.1)
GRIP_D, GRIP_L = 16.0, 22.0            # CHOICE: mushroom grip [R1-19]
PUSH_HOLE_EXTRA = 0.02                 # CHOICE: push-wire hole = tube bore + 0.02 (drilled)
POCKET_CLEAR = 0.03                    # CHOICE: tube pocket = tube + 0.03, drilled; bonded with epoxy, a waxed wire
#                                        through tube and push hole while it cures [R2-6]
PUSH_WIRE = {"A": 0.60, "B": 1.10}     # CHOICE: stainless wire or gauge pin, < bore (0.686 / 1.245)

# ---- liner and slip bushings (bought, hardened; Carr Lane; [J-src 4]) -----------------------------------------------
# Slip/fixed renewable bushing SF-12-8-<ID>-NCB: body OD 3/16 in (0/-0.0002 in), body 1/2 in long under the head, head
# dia 5/16 x 3/16 in, bore to order .0135-.0980 in, +0.0001/+0.0004 in, Rc 62-64; -NCB = no counterbore.
# Tolerances on body length, head diameter and head thickness: +-1/64 in (amesweb SF table, read by the round-2
# reviewer; Carr Lane states none) [R2-9].  RFQ: both bushings ground to the same under-head length and head
# thickness within 0.001 in (CHOICE; if refused, see docs/36 section 4).
# Liner L-20-6: ID 3/16 in +0.0001/+0.0004, OD 5/16 in +0.0013/+0.0016 in (L-20 series [V]), 3/8 in long, US$13.01 [V]:
# one size shorter than the bushing body, so the bushing's own face reaches the foot [R2-1].
BODY_L, BODY_L_TOL = 0.500 * IN, IN / 64.0
LINER_ID, LINER_OD_NOM, LINER_L = 0.1875 * IN, 0.3125 * IN, 0.375 * IN
LINER_L_TOL = IN / 64.0                # UNVERIFIED (taken as the bushing's)
LINER_ID_TOL = (0.0001 * IN, 0.0004 * IN)
LINER_OD_TOL = (0.0013 * IN, 0.0016 * IN)
LINER_OD = LINER_OD_NOM + LINER_OD_TOL[1]                 # 7.978: modelled at its largest [R1-2]
SLIP_OD_TOL = (-0.0002 * IN, 0.0)
SLIP_HEAD_D, SLIP_HEAD_H = 0.3125 * IN, 0.1875 * IN
HEAD_TOL = IN / 64.0                   # on head diameter and head thickness [R2-9]
FACE_MATCH = 0.02                      # CHOICE: the two bushing faces agree within this (matched order, or lapped)
SLIP_BORE_CLEAR = 0.0002 * IN          # CHOICE: bore ordered = measured tube outside + 0.0002 in [R1-7]
SLIP_BORE_TOL = (0.0001 * IN, 0.0004 * IN)
SLIP_RUNOUT = 0.005                    # UNVERIFIED: bore to body, radial (concentricity not stated by Carr Lane)
LINER_HOLE_D = 8.00                    # CHOICE: printed 7.8, reamed 8.00 H7 (0/+0.015); bond gap 0.022-0.045 [R1-2]
BODY_HOLE_D = 5.2                      # CHOICE: below the liner the bushing body passes through the plate (printed,
#                                        drilled 5.2): the printed foot ring presses the sheet from r 2.6 outwards
LEDGE_GAP = 1.4                        # CHOICE: below the liner's bottom: room for the liner to float at bonding,
#                                        with the plate's print tolerance [R3-3]; ream with a chucking reamer, depth
#                                        set from the foot face (ledge 1.775 above it)

# Ring finger (J-005, printed PA12, reamed 4 H8) on a shoulder screw ISO 7379-4-M3-10 (Ganter GN 35215: head 7 x 3,
# thread 7, shoulder 10 +0.25, d1 f9 [R3-7, page read by the round-3 reviewer]; 4-M3 is a maker's extension of the
# ISO sheet).  Stack on the shoulder from the plate top: spacer J-004 (printed FINGER_SET_ALLOW high and faced at
# assembly), the finger, an NBR O-ring 4 x 1 (compressed to about 0.7: presses the finger down onto the spacer, so it
# has no axial play and turns with light friction [R3-5]), shim rings DIN 988 4 x 8 to fill up to the screw head.
# The ring bears on the whole rim of the bushing head, wherever its recesses are [R2-3].
LOCK_R, LOCK_ANGLE = 9.5, 90.0         # CHOICE: pivot 9.5 from the punch axis, at +y [R2-4]
FINGER_T, FINGER_W = 2.5, 5.0          # CHOICE (2.5: room on the 10 mm shoulder at the highest head, R3-7)
RING_R_IN, RING_R_OUT = 3.2, 4.8       # CHOICE: ring around the nose (r 2.5), over the head rim (r 3.97 +- 0.40)
BOSS_D, FINGER_HOLE_D = 8.0, 4.0       # CHOICE: hole reamed 4 H8 on the 4 mm shoulder
FINGER_GAP = 0.05                      # CHOICE: set at assembly over the thicker head (feeler 0.05) [R3-5]
FINGER_PLAY = 0.0                      # the O-ring preload takes the axial play out [R3-5]
ORING_H = 0.7                          # NBR O-ring 4 x 1, compressed height (CHOICE)
FINGER_CHAMFER = 0.3                   # CHOICE: lead-in chamfer under the ring's outer edge [R2-2], modelled [R3-8]
SHOULDER_D, SHOULDER_L = 4.0, 10.0     # ISO 7379-4-M3-10 [R3-7]
SHOULDER_HEAD_D, SHOULDER_HEAD_H, SHOULDER_THREAD = 7.0, 3.0, 7.0   # Ganter GN 35215 [R3-7]
SWING_STOP = 74.0                      # deg: with DIN 464 heads (7.5 tall) the swung finger stops on a thumb head
SWING_MIN = 60.0                       # deg: the bushing lifts out freely from here on [R3-4]
SPACER_D = 8.0                         # J-004
FINGER_SET_ALLOW = 1.2                 # CHOICE: spacer printed this much higher, faced at assembly
FINGER_PLAY_DESIGN = 0.1               # CHOICE: a finger offset of this much toward the axis is checked [R2-4]

# ---- workpiece ---------------------------------------------------------------------------------------------------
BACKING_T, BACKING_T_TOL = 0.79, 0.05  # HDPE sheet 1/32 in +-0.002 in, McMaster 8619K561 [J-src 5]; the punch ends in it
STRIP_W = 14.0                         # CHOICE: FKM and backing cut to strips 14 wide; the FKM taped to the backing at
#                                        its leading end, the two fed together [R2-10]
STRIP_L = 100.0                        # CHOICE: about 30 washers per strip at the pitch below
PITCH = 3.0                            # CHOICE: washer spacing along the strip (web 1.6 between outsides)
TIP_INTO_BACKING = 0.25                # CHOICE: nominal stop: tip 0.25 into the 0.79 backing
STOP_SET_TOL = 0.05                    # CHOICE: each handle's nose is faced against ITS bushing to +-0.05

# ---- base (printed: MJF PA12 or FDM PETG/ASA; not SLA, the inserts are heat-set) [R1-2] -----------------------------
BASE_X, BASE_Y, BASE_T = 80.0, 48.0, 10.0      # CHOICE: x from -40 to +40
RAIL_GAP = 0.6                         # CHOICE: strip guide, 0.3 each side
RAIL_W, RAIL_H = 1.5, 0.30             # CHOICE: printed rails on the base top; lower than the strip
SCALE_X0, SCALE_X1, SCALE_TICK = 21.0, 39.0, (0.4, 1.2, 0.3)   # CHOICE: ticks on the hole positions; long tick at 30;
#                                        load the strip with its leading end on the tick at 21 [R2-14]
PARK_XY = [(-32.0, 14.0), (-32.0, -14.0)]   # CHOICE: parking holes for the idle bushing (body down) [R2-12]
PARK_D, PARK_BOSS_D, PARK_BOSS_H = 5.3, 10.0, 4.5   # CHOICE: on a boss, deep enough that the bushing hangs on its
#                                        head and its ground face touches nothing [R3-10]

# ---- head plate (printed, same process as the base) ---------------------------------------------------------------
PLATE_X, PLATE_Y = 40.0, 40.0          # CHOICE
PLATE_T = 11.9                         # CHOICE: liner top (= bushing seat) 0.8 above the plate top, 0.2-1.4 [R1-8]
FOOT_D = 11.0                          # CHOICE: printed foot around the bushing body
RECESS_HALF_W, RECESS_DEPTH = 10.0, 1.0   # CHOICE: underside relief over the strip, except the foot
SCREW_FORCE = (50.0, 400.0)            # N per thumb screw, finger tight: range (UNVERIFIED) [R1-9]
MU_SHEET = 0.3                         # friction FKM on HDPE and on PA12, lower bound (UNVERIFIED)
PRINT_TOL = 0.2                        # CHOICE: printed thickness tolerance used in the checks (MJF/FDM)

DOWEL_D, DOWEL_L, DOWEL_IN_BASE = 3.0, 12.0, 6.0   # 3 m6 x 12 hardened pins, McMaster 91595A112 [J-src 5]
DOWEL_XY = [(0.0, 17.0), (0.0, -17.0)]             # CHOICE: round hole at the first, slot along y at the second
DOWEL_BASE_REAM, DOWEL_PLATE_FIT = 2.95, (3.02, 3.04)   # CHOICE: base pressed (ream 2.95, or bond); plate a slide
#                                        fit (ream 3.0, lap with the pin) so the plate floats [R2-8]
SLOT_L = 1.0                           # CHOICE: extra length of the slot
SCREW_XY = [(15.0, 16.0), (-15.0, 16.0), (15.0, -16.0), (-15.0, -16.0)]   # CHOICE: four M3 thumb screws [R1-9]
SCREW_D, SCREW_CLEAR = 3.0, 3.4
INSERT_HOLE_D, INSERT_L, INSERT_WALL = 4.0, 5.7, 1.6     # ruthex RX-M3x5.7: hole 4.0, minimum wall 1.6 [J-src 5]
INSERT_HOLE_DEPTH = 7.5                # CHOICE: blind hole below the insert, for the screw end [R1-12]
THUMB_HEAD_D, THUMB_HEAD_H, SCREW_L = 12.0, 7.5, 20.0   # M3 x 20 knurled thumb screw DIN 464 (head UNVERIFIED) [R1-12]


# ---- derived ----------------------------------------------------------------------------------------------------
Z_FOOT = BACKING_T + SHEET_T                     # plate underside = foot face = bushing face = sheet top
Z_PLATE_TOP = Z_FOOT + PLATE_T
Z_LINER_TOP = Z_FOOT + BODY_L                    # the bushing face is flush with the foot: the head seats here
Z_LINER_BOT = Z_LINER_TOP - LINER_L
Z_LEDGE = Z_LINER_BOT - LEDGE_GAP                # bottom of the reamed liner hole
Z_HEAD_TOP = Z_LINER_TOP + SLIP_HEAD_H           # the handle's nose lands here
Z_SHEET0 = BACKING_T                             # underside of the sheet
Z_TIP = BACKING_T - TIP_INTO_BACKING             # punch tip at the bottom of the stroke
Z_FINGER0 = Z_HEAD_TOP + FINGER_GAP              # finger underside (set at assembly)
SPACER_H = Z_FINGER0 - Z_PLATE_TOP               # spacer height as faced (nominal)
SHIMS_ABOVE = SHOULDER_L - SPACER_H - FINGER_T - ORING_H       # shim rings between the O-ring and the screw head
Z_SHOULDER_TOP = Z_PLATE_TOP + SHOULDER_L        # underside of the shoulder-screw head
LOCK_XY = (LOCK_R * math.cos(math.radians(LOCK_ANGLE)), LOCK_R * math.sin(math.radians(LOCK_ANGLE)))


def slip_bore(punch):
    return punch["tube_od"] + SLIP_BORE_CLEAR


def protrusion():
    """Tube length below the (faced) nose: from the bushing head top to the tip at the end of the stroke."""
    return Z_HEAD_TOP - Z_TIP


def pocket_depth(punch):
    """Tube length inside the handle, measured from the faced nose: the tube bears on the pocket's shoulder."""
    return punch["tube_l"] - protrusion()


def head_top_range():
    """Head top above the plate top over the tolerances: bushing body and head (+-1/64 in each, unmatched) and the
    printed plate thickness; the bushing face is flush with the foot by the bonding procedure."""
    nom = Z_HEAD_TOP - Z_PLATE_TOP
    d = BODY_L_TOL + HEAD_TOL + PRINT_TOL
    return nom - d, nom + d


PARK_DEPTH = BODY_L + 0.5 - PARK_BOSS_H          # hole below the base top (the boss adds PARK_BOSS_H)


def facing_range():
    """Nose facing needed at assembly (mm): NOSE_ALLOW nominal, less or more by the head-top error relative to the
    foot (body + head, unmatched), the drilled pocket depth (+-0.2) and the tube length."""
    d = BODY_L_TOL + HEAD_TOL + 0.2 + TUBE_L_TOL
    return NOSE_ALLOW - d, NOSE_ALLOW + d


def tip_depth_range():
    """Tip depth into the backing.  The plate rides on the sheet and the nose lands on the bushing head, so
    depth = protrusion - sheet - (body + head): the backing's thickness cancels; the bushing's length tolerance is
    taken out by facing each handle against its own bushing (STOP_SET_TOL); the sheet's tolerance remains."""
    return TIP_INTO_BACKING - SHEET_T_TOL - STOP_SET_TOL, TIP_INTO_BACKING + SHEET_T_TOL + STOP_SET_TOL


def liner_slip_offset():
    """Largest radial offset of the bushing face from the liner axis: the body may tilt in the liner's play and the
    face is OVERHANG below the liner's bottom."""
    play = LINER_ID_TOL[1] - SLIP_OD_TOL[0]
    overhang = BODY_L - LINER_L
    return play / 2.0 + play * overhang / LINER_L


def concentricity_budget():
    """Radial offset between hole and outside: each stroke adds liner/slip play (with the overhang), slip runout,
    punch/bore play and tip runout; the two strokes are independent; plus one allowance for the sheet moving at the
    swap.  Returns worst case and root-sum-square (mm, radial)."""
    per = []
    for _p in (PUNCH_A, PUNCH_B):
        bore_play = (SLIP_BORE_CLEAR + SLIP_BORE_TOL[1] + 2 * PUNCH_OD_TOL) / 2.0
        per += [liner_slip_offset(), SLIP_RUNOUT, bore_play, PUNCH_TIP_RUNOUT]
    per.append(SHEET_SHIFT)
    worst = sum(per)
    rss = math.sqrt(sum(v * v for v in per))
    return worst, rss
