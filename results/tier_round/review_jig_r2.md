# Review of the washer punching jig (docs/36 Revision B), round 2

Reviewer: independent agent (mechanical / fixture design / lab practice), 2026-11-18.
Read: docs/36 (Rev B), `cad/elisa_cad/tier2_cell/jig/{params,parts,build}.py`, `results/tier_round/punch_jig_sourcing.md`,
`results/tier_round/review_jig_r1.md`, `cad/out/tier2_cell/punch_jig/check_results.json`, `section.png`,
`section_detail.png`. Re-ran `python -m elisa_cad.tier2_cell.jig.build --fast`: **36 checks, all pass** (matches the doc).
A full render run was in progress during the review (started 21:49); `handle_B_section.png` did not yet exist.
Web spot checks this session:
- Carr Lane SF parts view (carrlane.com, page): SF-12-8 ID range **.0135–.0980 in** (confirms the sourcing; bores .0352 and
  .0652 in are available), F dia 5/16, columns G 3/16, H 3/32, J 3/32, L 55°, R 17/64 unlabeled, lock screw LS-0; **no
  length, head diameter or head thickness tolerance on the page**.
- amesweb SF table (page): for the 3/16 body, body length **±1/64 in**, head diameter 5/16 **±1/64 in**, head thickness
  3/16 **±1/64 in** (±0.40 mm each). The sourcing file already cites amesweb for the head tolerance, but params.py uses
  `SLIP_L_TOL = 0.1` (UNVERIFIED). The only tolerance figure found is four times larger.

Geometry used below (params.py, Derived): Z_FOOT 1.04, plate top 13.44, liner top 13.74, head top 18.5025, finger
18.6025–21.1025, sleeve top 21.2025, lock-screw head top 24.70, grip underside 26.00. Lock pivot at (0, 8). Finger boss
⌀8 (`SLEEVE_D + 3`), finger hole ⌀5.2 on a ⌀5.0 sleeve.

---

## Round-1 findings

| R1 | Topic | Status | Reason |
|---|---|---|---|
| 1 | Bushing swap impossible with a round washer | **partly** | The swing finger removes the need to take the screw out, and the swap now needs no tool. But the finger relies on the head rim being complete under a 0.57 mm overlap while the head recesses are still not modelled and the bushing's orientation is random after every swap (new F3). It also assumes a nominal head thickness and diameter (new F2, F4). |
| 2 | Liner press fit; insert wall 0.77 | resolved | Hole 8.00 H7 gives a bond gap of 0.022–0.045 (check). The liner is modelled at 7.978 max OD. The lock insert wall is 8.0 − 4.0 − 2.0 = 2.0 ≥ 1.6. PA12/PETG/ASA are specified and SLA excluded. (Doc §2.2 says 0.044; the check gives 0.045. Trivial.) |
| 3 | Handle A had no pocket | resolved | Pockets 0.919 / 1.681 × 20.14, push holes 0.706 / 1.265; shoulders 0.09 / 0.19 (parts.py:78–86, check). Making the pockets is a new issue (F6). |
| 4 | Rapid-Core cannot reach through a bushing | resolved | Bushing C and the fallback were removed. The membrane disc is punched freehand (§0, §1, §8). |
| 5 | No positive depth stop | resolved | The nose lands on the bushing head and the backing thickness cancels (params.py:146–160). The setting can only be corrected in one direction (new F5). |
| 6 | Middle edge squeezes the washer | resolved | The inside edge is now the first line of the RFQ (§3). §5 items 3–4 check flatness and edges. |
| 7 | Concentricity budget incomplete | resolved | A 10 µm sheet-shift term was added; bore = measured tube + 0.0002 in; acceptance rests on measured washers (§2.5, §5). Worst case 0.0755 / RSS 0.026, arithmetic re-checked. |
| 8 | Plate/liner length stack | resolved for the head seat | The plate is 0.3 thinner, so the head seats on steel. The related stack at the **lower** end (bushing body length against liner length) is not handled (new F1). |
| 9 | Collinear screws; force 50 N | resolved | Four screws; force given as a range of 50–400 N. |
| 10 | Scale 1 mm off | resolved (minor gap) | Ticks at 21…39 on the hole positions. There is still no start reference for the first seven washers (F14). |
| 11 | Checks testing the wrong thing | resolved | Labels corrected. Liner at max OD, handle A modelled, all screws and inserts in the interference set. The section is cut away at y < 0 and seen from −y, so the cut face is shown. Count 36 = doc. New check gaps are in F9. |
| 12 | Thumb screw length | resolved | M3 × 20, insert hole 7.5 deep; engagement 6.46–6.66 (whole insert). |
| 13 | Dowel hole unreamed | partly | Plate holes are now reamed 3.0. Reaming the **base** press-fit holes to 3.0 gives no press on an m6 pin, and an H8/m6 fit can make the floating plate bind (F8). |
| 14–21 | Notes | resolved | Straightness §2.5, slug §1.6, backing per strip §1.7, tip caps §4, ⌀16 grip, tools in §3, docstring fixed. Small BOM gaps remain (F12). |

---

## New findings

### F1 — MAJOR: the bushing face can stand up to 0.4 mm below the foot, into the 0.25 mm sheet, and differently for A and B
**What.** The liner is bonded flush with the foot (§4) and the bushing head seats on the liner end (`LINER_PROUD`). The
bushing face therefore sits at (liner length − bushing body length) relative to the foot face. Both are nominally 1/2 in,
but the only tolerance found for the SF body length is **±1/64 in (±0.40 mm)** (amesweb, page, this session). Carr Lane
states none. The L-20 liner length tolerance is not stated either. params.py:79 assumes `SLIP_L_TOL = 0.1` UNVERIFIED and
uses it only for the depth stop, where it is set out per handle. Nothing models where the **face** of the bushing lies.
**Why it matters.**
- A long bushing stands proud of the foot and presses into the 0.25 sheet (it cannot go 0.4 deep). When it is dropped in at
  the swap, it either lifts the clamped plate against the screws or indents the sheet around the hole cut in stroke 1. That
  moves rubber radially just before the outside is cut: concentricity and OD both suffer.
- A short bushing leaves the sheet unsupported under its bore, so the punch drags the rubber down.
- A and B are random relative to each other, so the error differs between the two strokes. It is not common-mode.

**Fix.**
1. Measure the under-head length of both bushings and the liner length (micrometer) on receipt.
2. Bond the liner with the **longer** bushing seated in it and that bushing's face on the flat plate together with the foot, so the
   longer face is flush by construction.
3. Lap the longer bushing face, or specify both bushings to the same under-head length, so the two faces agree within
   ≈ 0.02 mm. Carr Lane grinds special lengths; ask in the quote.
4. Add the tolerance (±0.40 mm, amesweb) to params.py.
5. Add a check that the bushing face lies 0 to −0.03 from the foot face after this procedure.

### F2 — MAJOR: the finger is fixed at 0.10 above a head whose thickness can vary by ±0.40 mm, and it must suit two bushings
**What.** The finger height is set by the printed lower sleeve (5.16 mm, `Z_FINGER0 − Z_PLATE_TOP`). The gap to the head is
5.1625 − 0.3 (liner proud) − 4.7625 (head) = **0.10**. Three tolerances feed into that gap:
- head thickness 3/16 ±1/64 in = ±0.40 (amesweb);
- the printed sleeve height, ±0.1–0.2 (MJF/FDM);
- the liner protrusion, which depends on the printed plate thickness (±0.1–0.2) and the liner length.

**Effect.** If either head is more than 0.1 thicker, the finger cannot be swung over it: it runs into the side of the head.
If it is thinner, the bushing can rise 0.5 mm or more on withdrawal. That gap is not fatal for guidance, but it is the
"bushing dragged up" mode the finger is meant to stop. One sleeve height has to suit both A and B.
**Fix.**
- Set the finger height at assembly: print the lower sleeve 0.4 tall and face it so that a 0.05–0.15 feeler passes under the
  finger over the **thicker** of the two heads. Or put shim washers under the sleeve.
- Give the finger tip a 0.3 × 30° lead-in chamfer on its underside so that a slightly high head is pressed down rather than
  struck.
- Alternatively order both bushings with the same head thickness specified.
- State the procedure in §4 and model the sleeve as "faced at assembly".

### F3 — MAJOR: the head recesses can come under the finger after any swap, and then nothing retains the bushing
**What.** The SF head carries a lock-screw recess and a slip recess (sourcing §4: "slip down, then rotate to lock"; Carr Lane
columns H 3/32, J 3/32, L 55°, R 17/64 are unlabeled). The slip recess must let the head pass an LS-0 screw head centred at
R 6.75. It is therefore cut inward to about R 6.75 − r(LS-0 head), which is very probably inside r 3.4 (UNVERIFIED: LS-0
head diameter not found).

The finger bears only on the segment r 3.40–3.97 (0.57 overlap, chord about 4.1 mm wide, about 1.6 mm²; parts.py:97–104).
params.py:68–69 and docs/36 §2.1 say to "turn the recesses away from the finger". But the operator lifts a bushing out and
drops the other one in at **every washer**, about 200 times, with no orientation feature, and the bushing turns freely in a
2.5–15 µm slip fit. Over a sector of perhaps 60–120° (UNVERIFIED) the finger lies over air.
**Fix.** Pick one of these and confirm the recess geometry with Carr Lane's drawing first:
- (a) an anti-rotation key: a ⌀2 pin (or a printed rib) standing on the plate top at R ≈ 6.75 that sits in the slip recess.
  The bushing can only be lifted and dropped in one orientation, and the finger is placed 90° or more away from it, over the
  full rim.
- (b) a fork-shaped finger that bears on the head on two sides 120° or more apart.

Add the recesses to `slip_bushing()` and a check that the finger's bearing area on the real head is ≥ 1 mm² at the worst
orientation that the key allows.

### F4 — MAJOR: the finger boss is 0.03 mm from the head's lift path; the check passes only at nominal
**What.** The finger boss is ⌀8 at the pivot (0, 8), so its inner edge lies at r = 8 − 4 = **4.00**. The head radius is 3.969
nominal (⌀5/16), and the boss sits above the head. Lifting the bushing out passes the head through the boss's height at
r ≤ 3.97. The clearance is therefore **0.031 mm** nominal, and three things take it away:
- the finger's hole play: ⌀5.2 on ⌀5.0 lets the boss move 0.10 toward the axis;
- the printed boss tolerance (±0.1–0.2);
- the head diameter tolerance of ±1/64 in, up to r 4.17.

The worst case is about −0.3 mm. The head then catches under the boss or scrapes it on every lift. build.py:70–72 checks
the lift path only with the nominal head and the finger centred (`clear_vol <= 1e-6`), so it reports a pass. docs/36 §2.1
and §6 ("clear of the head when turned 90°", "frees it") overstate it.
**Fix.**
- Move the pivot out to `LOCK_R = 9.5` (insert wall then 3.5) or reduce the boss to ⌀7 with a flat on the axis side. The
  target is ≥ 0.6 mm between the boss and a ⌀8.33 head at full play.
- Lengthen the arm to keep the tip at r ≤ 3.4 (or further in, see F3).
- In the check, model the head at ⌀8.33 and offset the finger 0.1 toward the axis.
- Check the lower sleeve too: ⌀7 at r 4.5 leaves 0.33 to a ⌀8.33 head, which is OK.

### F5 — MINOR: the depth can be corrected only one way, and at nominal there is nothing to remove
**What.** §2.4 and §4 set the depth by facing the nose, which only makes the tip deeper. Several errors can each make the
tip too deep before any facing:
- the tube length (unknown tolerance);
- the hand-drilled pocket depth (±0.2 by hand);
- a thinner head (up to −0.4).

The nominal design puts the tip at exactly 0.25 into the 0.79 backing, so a tip that ends too deep (up to 0.54 into the
remaining 0.54 of backing and then into the printed base) cannot be corrected by facing. Facing a ⌀6 printed nose with an
18 mm tube sticking out of it also needs a method.
**Fix.**
- Make the nose 0.5 longer nominal (`NOSE_L = 8.0`, so the grip still clears the screw head by 1.3 − 0 at nominal; recheck),
  so that setting always removes material.
- Describe the facing: abrasive paper on a flat plate with a ⌀3 clearance hole for the tube, or a lathe with the tube in a
  collet. Or set the depth with a printed shim washer under the nose.

### F6 — MINOR: making the handle pockets (⌀0.92 × 20 and ⌀1.68 × 20 blind, ⌀0.71 through) and bonding the tube
**What.**
- The STLs carry the holes at final size (parts.py:85–86). A ⌀0.7 × 9 hole and a ⌀0.92 × 20 hole do not print open or to
  size in MJF (trapped powder) or FDM.
- Drilling 22:1 with a #64 drill by hand wanders and breaks drills. A crooked pocket bends the tube against its bushing bore
  and moves the nose toward the finger (only 0.4 clearance).
- The shoulder bears on a tube end of about 0.23 mm² (A): 60 N gives about 260 MPa, which crushes PA12. The epoxy bond
  (about 56 mm²) carries the load, so the "shoulder carries the tube" claim (build.py:84–85) is a locator, not a load path.
- Epoxy wicks into the tube bore and the push hole and can block the ejector path.

**Fix.**
- Print the handle with ⌀0.5 pilot holes, or solid, and drill on a lathe or a drill press in a V-block, pecking.
- Better: a turned brass core (⌀6 nose + ⌀4 stem) drilled on a lathe and pressed or bonded into the printed grip.
- Bond with a waxed or PTFE-coated wire through the tube and push hole during cure.
- Reword the check as "shoulder locates the tube; the bond carries the load".

### F7 — MINOR: the finger's free rotation depends on 0.1 mm printed clearances
**What.** The finger (2.5 thick) sits on a 2.6 mm upper sleeve step under a clamped DIN 125 washer: 0.10 axial play. It runs
⌀5.2 on ⌀5.0: 0.10 radial play. Printed tolerances are of the same size, so the finger is likely to be either clamped by the
lock screw or rocking. The rocking adds to F4. The lock-screw clamp load also creeps the PA12 sleeve.
**Fix.** Use a steel shoulder screw (ISO 7379, ⌀4 shoulder, M3 thread) with the finger reamed ⌀4 H8 and 0.2–0.3 axial play.
Or ream the finger hole and face the sleeve step at assembly to 0.15–0.25 axial play. Face the plate's heat-set insert flush
before the sleeve goes on.

### F8 — MINOR: dowel fits
**What.**
- Base: "print 2.8, ream 3.0" for a pressed m6 pin (+0.002/+0.008) in PA12 is a transition fit at best, so the pins will be
  loose.
- Plate: reamed 3.0 H8 on m6 is close to zero clearance on two pins 34 mm apart (one a slot). A plate that must **float**
  down onto a 1.04 ± 0.10 stack under finger-tight screws will bind on the pins, and screw force goes into pin friction
  instead of the foot.

**Fix.** Ream the base holes 2.95 and press, or bond the pins. Make the plate's round hole and slot a slide fit, e.g.
3.00 + 0.02/+0.04: ream 3.0, then lap with the pin. Positioning is common-mode and the plate does not move between strokes.

### F9 — MINOR: checks run only at nominal where the margins are small
build.py:67–74 (finger retain/free, nose clearance) uses the nominal head and a centred finger. That is why F4 passes.
- `tip_depth_range` uses `SLIP_L_TOL = 0.1`, which contradicts the sourced ±1/64 in.
- No check covers the bushing face against the foot face (F1) or the finger-to-head gap under tolerances (F2).
- The concentricity check passes on RSS (0.026) while the worst case (0.0755) exceeds 0.05. That is stated in the label, but
  as written this check can never fail on the worst case.

**Fix.** Add tolerance cases (head ⌀ ±0.40, head thickness ±0.40, body length ±0.40, finger play 0.1) to the finger, sleeve
and face checks. Put the amesweb tolerances into params.py with their source.

### F10 — MINOR: does the backing move with the FKM?
§1 step 7: "push the strip on by 3 mm". The backing and the FKM are separate strips (§1 step 1). If only the FKM is pushed,
all of a strip's roughly 30 strokes land in the same backing crater. The cut then ends in a hole rather than in material, and
the outside edge gets ragged. If the backing is pushed too, it is not said how.
**Fix.** Tape the FKM to the backing at the leading end (or use a backing 1 mm longer with a folded tab) and feed them
together. Say so in §1.

### F11 — NOTE: section_detail.png
The `section_detail.png` present during the review (timestamp 21:47, before the current render run) shows the plate in
brown across the whole x-range above the sheet. It shows no liner, no bushing and no backing, and no relief gap at
|x| 5.5–6. It does not show what its title claims. Re-check it after the running render finishes. If it is unchanged, the
xlim/ylim crop or the depth ordering in `C.render_png` is hiding the steel parts.

### F12 — NOTE: BOM and set-up gaps
- §4 uses a ⌀4.76 (3/16 in) gauge pin "through a bushing above", but neither is in the §3 tools. The squareness actually
  comes from the liner end and the foot both standing on the flat plate; the gauge pin adds nothing unless the "bushing
  above" is held square. Simplify the text.
- Add PTFE release film under the liner (retaining compound otherwise bonds the jig to the surface plate), feeler gauges,
  a drill press or lathe (F6), and colour or engraved marks A/B on both bushings and both handles. A swapped bushing takes
  the 0.889 tube with 0.38 mm play, which is a mis-punch not a crash.
- Add a parking block on the base: two ⌀8.5 holes for the idle bushing, and a tip-down hole for the idle handle (safety:
  the tube is needle-sharp).

### F13 — NOTE: sourcing confirmations this session
Carr Lane confirms SF-12-8 bores .0135–.0980 in (both bores to order are in range), F dia 5/16, LS-0. The page states no
length or head tolerance. amesweb gives ±1/64 in on body length, head diameter and head thickness (used in F1, F2 and F4).
Ask Carr Lane in the quote for the real tolerances and the head recess drawing (F3).

### F14 — NOTE: scale start
There is nothing to read for the first seven washers (holes under the plate). Load the strip with its leading end on the
tick at x = 21 and use the end as the index until holes appear; say so in §1.

### F15 — NOTE: throughput and handling
Each washer takes four screws loosened and retightened, two swaps, two strokes and an ejection, about 1.5 min, so 2.5–3 h
for 100. That is acceptable. The head is gripped with the fingers inside the 0.53 gap to the sleeve on one side; tweezers
with flat jaws make it easier. FKM debris in a 2.5 µm minimum slip fit can make a bushing stick: blow out the liner per
strip.

---

## Summary

The two-punch, one-axis concept, the liner bond, the handle pockets and the depth stop are now right. The open problems
are in the new swing-finger retention and in the bushing's own tolerances. These were taken as 0.1 mm UNVERIFIED, but the
only figure found is ±1/64 in (±0.40 mm):
- the bushing face can stand into the 0.25 sheet, by a different amount for A and B (F1);
- the finger cannot be guaranteed to swing over the head (F2);
- the head recesses can come under the finger after a random-orientation swap (F3);
- the finger boss blocks the head's lift path within tolerance (F4).

All four are fixed with parameter changes, one key pin, and procedures done at assembly.

Converged: no
