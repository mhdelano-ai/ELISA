# Review of the washer punching jig (docs/36 Revision C), round 3

Reviewer: independent agent (mechanical / fixture design / lab practice), 2026-11-18.
Read: docs/36 (Rev C), `cad/elisa_cad/tier2_cell/jig/{params,parts,build}.py`, `results/tier_round/punch_jig_sourcing.md`,
`review_jig_r1.md`, `review_jig_r2.md`, `cad/out/tier2_cell/punch_jig/check_results.json`, `section.png`.
Re-ran `python -m elisa_cad.tier2_cell.jig.build --fast`: **42 checks, all pass**, which matches the doc. This rewrote the
STEP/STL/JSON outputs in place, and git now shows them as modified, so it is worth discarding or re-committing them.
Wrote two throw-away probes (scratchpad `p1.py`, `p2.py`) that swing the finger through 0–90° against the thumb screws
and against the lift path of the largest head.

Render timestamps seen: `section.png`, `assembly_iso.png` and `assembly_exploded.png` are from 22:05 and show Revision C
(short liner, body through the foot). `section_detail.png`, `base_top.png` and `head_plate_underside.png` are from 21:47,
before the Rev C commit at 22:06, so they are stale. `handle_B_section.png` is absent.

Web spot checks this session:
- amesweb SF table (page): 3/16 body: head ⌀5/16 ±1/64, head thickness 3/16 ±1/64, body length ±1/64 in. This confirms the
  tolerances used in Rev C. The table also has a "Radius Min." column D = 1/32 in, which is not explained.
- Elesa-Ganter ISO 7379 datasheet (PDF, page, 10/2024): **"the official ISO standard sheet has … M5-6,5 / M10-13 /
  M20-25"**, so the 4-M3 size is a manufacturer extension, not ISO. GN 35215 "ISO 7379-4-M3-10-NI" reads: d1 4 **f9**,
  d2 M3, **d3 7**, l1 10 **+0.25**, l2 **7** (thread), l3 **3** (head), sw 2. params.py has head 8 × 2.5 and thread 6.

---

## Round-2 findings (and the round-1 "partly" items)

| R2 | Topic | Status | Reason |
|---|---|---|---|
| 1 | Bushing face vs foot, A ≠ B | **resolved (design)** | The liner is one size shorter (L-20-6, 9.525 against a 12.7 body). It floats 1.0 above its ledge and is bonded with the longer bushing as the locator, so that bushing's face is flush with the foot by construction. The faces are matched or lapped to within 0.02. The numbers check: liner float 0.21 at the worst stack; liner top 0.20–1.40 above the plate. The **procedure** that achieves this has problems (N1, N2, N3, N6). |
| 2 | Finger height vs head thickness ±0.4 | resolved | The spacer is printed 6.86 tall and faced to 4.67–6.66; shim rings take up the rest of the shoulder (0.19–2.18 left). The 0.3 lead-in chamfer is specified but not modelled (N8). The gap over the thinner head when heads are unmatched is not stated (N5). |
| 3 | Head recesses under the finger | resolved | The ring r 3.2–4.8 bears on the whole rim for head r 3.57–4.37, so the recesses can be at any angle. |
| 4 | Boss in the head's lift path | resolved | The pivot is at 9.5 and the boss ⌀8, so the boss is 1.03 from a ⌀8.73 head with the finger offset 0.1. Checked at the extremes (build.py:68–77). But the "swung 90°" position used by that check collides with the thumb screws (N4). |
| 5 | Depth correctable only one way | resolved | The nose is printed 1.2 long; facing needed is 0.11–2.29 (body + head + pocket + tube), so the nose is always faced. The facing method is given, though it is weak (N9). |
| 6 | Making the handle pockets, bonding | resolved | Pockets drilled from pilots on a drill press or lathe; waxed wire during cure; the check now says the bond carries the load. |
| 7 | Finger running on printed clearances | resolved | Steel shoulder screw, finger reamed 4 H8 on the shoulder (vendor: f9, so 0.010–0.048 play), DIN 988 shims for the axial play. The vendor data differ from the model (N7). |
| 8 | Dowel fits | resolved | Base holes reamed 2.95, pins pressed or bonded. Plate holes 3.02–3.04, a slide fit. |
| 9 | Checks only at nominal | resolved, with gaps | Head ⌀, head thickness, body length (±1/64) and finger play are now in the checks. Remaining gaps: the swung finger is not checked against other parts (N4); the ledge-gap check omits the plate's print tolerance (N3); the face-flush check is tautological; the sheet tolerance differs from the stock (N8). |
| 10 | Backing fed with the FKM | resolved | §1 step 1: tape the FKM to the backing at the leading end. |
| 11 | section_detail.png | **not yet** | The current file is still from 21:47, before Rev C, and has not been regenerated. Re-check it after the render run. `section.png` (22:05) is correct. |
| 12 | BOM / set-up gaps | resolved | Gauge-pin text gone; PTFE film, feelers, drill press, A/B marks, parking holes and tip caps added. |
| 13 | Sourcing confirmations | resolved | Carr Lane RFQ items listed in §3 and §8. |
| 14 | Scale start | resolved | Leading end on the tick at x = 21. |
| 15 | Throughput, debris | resolved | Liner blown out per strip; flat tweezers. |
| R1-1 | Bushing swap | resolved | Ring finger, no tool needed, recesses irrelevant. |
| R1-13 | Dowel holes | resolved | See R2-8. |

---

## New findings

### N1 — MAJOR: the liner bond can glue the locator bushing into the liner (and the body into the foot)
**What.** Revision C bonds the liner with the precision slip bushing sitting inside it as the locator. The liner end is held
against the bushing head for the whole cure (docs/36 §2.4, §4). Adhesive goes into the 0.011–0.022 mm radial gap
between the liner and the plate. The bushing-to-liner fit is a 1.3–7.6 µm radial metal-on-metal slip fit, open at both
liner ends. The first adhesive listed (§3) is a "gap-filling retaining compound", which is anaerobic, low-viscosity and
made to wick into exactly such fits and cure there without air. Nothing in §2.4 or §4 puts a release agent on the
bushing.

**Where it goes wrong.**
- Squeeze-out at the head end of the liner lands on the head/liner-end joint and wicks into the slip fit.
- Squeeze-out at the lower end of the liner falls into the 1.0 float gap and then into the 0.22 radial gap between the
  bushing body (r 2.38) and the drilled ⌀5.2 foot hole (params.py:92), bonding the body to the printed foot.

Either way the bushing cannot be swapped any more, and the jig stops working. Repair means a new plate, a new liner, and a
new bushing ground to the measured tube, with weeks of lead time.

**Fix (procedure; nothing in the CAD changes).**
1. Bond with an epoxy, not an anaerobic compound. Anaerobics also cure poorly against PA12, so use a thixotropic
   (paste) epoxy. Put a thin band of it only on the middle third of the 8.00 bore, none near either end.
2. Coat the locator bushing's body and the underside of its head with mould release (PTFE dry film or paste wax) and wipe
   it to a film.
3. Turn the bushing a few degrees in the liner every few minutes until the epoxy gels. Turning does not change its axial
   seat or its axis.
4. Lift the bushing out once the epoxy has gelled but not cured, clean it, and put it back.
5. After the cure, check that both bushings drop in and turn freely, and that each face is flush with the foot (straightedge
   and 0.02 feeler).

Write this into §2.4 and §4.

### N2 — MINOR: the bonding procedure in §2.4 cannot be done as written
**What.** §2.4 asks for three things that do not fit together:
- the plate "upside down on a flat plate";
- the bushing "with its face on the flat plate (through the foot)";
- the liner "pushed down against the bushing's head".

With the plate upright (foot on the flat plate), the bushing face is on the flat plate, but the liner hangs **below** the
head. Gravity pulls it 1.0 down onto the ledge, away from the head, and nothing can reach it from below to push it up.
With the plate upside down, the head is underneath and the liner rests on it by gravity, as the text intends. But then the
foot and the bushing face point up, away from the flat plate.

**Fix.** Use the inverted set-up with two flats:
1. Stand the bushing head-down on flat 1 (with PTFE film). Slide the liner, with epoxy applied, over the body; it rests on
   the head.
2. Lower the plate over the liner, foot up.
3. Lay flat 2 (a glass plate or gauge block, with PTFE film) across the foot and the bushing face.
4. Raise the plate on shims until its foot touches flat 2, then weight flat 2.

The liner's weight keeps it on the head, and flat 2 makes the foot and the face coplanar. This also matches the 1.0 float
gap, which is then above the liner. Describe it in §2.4 and add "two flat plates" to the §3 tools.

### N3 — MINOR: reaming the blind 8.00 H7 liner hole, the ledge gap, and the body hole
**What.**
- **Reamer type.** The liner hole is blind: it ends on a printed ledge with only the ⌀5.2 hole below it (parts.py:72–73).
  A hand reamer has a long taper lead (several mm at ⌀8). It cannot size the lower part of the bore, and the liner's
  lower end sits only 1.0 above the ledge. A tapered bore there jams the liner, which then sets neither its axis nor its
  height.
- **Ledge gap check.** The hole is specified "9.73 deep from the top", so the ledge's height above the foot carries the
  printed plate thickness tolerance (±0.2, `PRINT_TOL`). build.py:91–94 compares the liner bottom with
  `Z_LEDGE − Z_FOOT = 2.175` and omits that tolerance. The worst stack is 2.381 − (2.175 + 0.2) = **0.006 mm**, not 0.21.
  If the liner bottoms on the ledge, the bushing face cannot come flush.
- **Body hole.** The ⌀5.2 body hole (0.22 radial clearance on the body) is drilled separately. If it is off the reamed axis
  by more than about 0.2, the body rubs the printed foot and tilts the bushing.

**Fix.**
- Use a chucking (machine) reamer with a short 45° lead, on a drill press with a depth stop.
- Set the depth from the **foot face**: ledge 2.0 ± 0.1 above the foot.
- Or raise `LEDGE_GAP` to 1.4. The ledge ring is then 1.775 thick, still ≥ 1.5, and the worst-stack gap is about 0.21 even
  with the print tolerance.
- Drill the ⌀5.2 in the same set-up as the ream, without unclamping.
- Add `PRINT_TOL` to the ledge-gap check.

### N4 — MINOR: the finger cannot swing 90°: it hits the thumb-screw heads at about 75°
**What.** docs/36 §2.1, §2.4 and §6 and check build.py:74–77 all use the finger "swung 90° either way". At 90° the ring
centre is at (±9.5, 9.5), with outside radius 4.8 and z 18.60–21.60. The DIN 464 thumb heads are ⌀12 at (±15, 16), z
12.94–20.44. The centres are 8.5 apart, against 10.8 needed, so the parts overlap: **16 mm³** per side (probe p1.py,
measured with `PT.finger(0/180)` against `PT.screws()`).

Stepping the angle (probe p2.py):
- contact with the thumb head starts between 74° and 76°;
- a ⌀8.73 head with the finger offset 0.1 lifts out freely only from **58°**.

So the usable window is about 58–75°. The jig still works, and the thumb head makes a natural end stop. But the check
validates a position the finger cannot reach, and the interference check never looks at the swung finger.

**Fix.**
- State the swing as "until it stops on the thumb screw (about 75°)".
- Run the lift check at 65°, and add an interference check of the swung finger, at its stop, against every part.
- Or move the thumb screws to (±16, ±17), or add a printed stop boss at 70°.
- If shorter thumb heads are bought (McMaster shows 2.5 tall), the stop disappears. In that case add the boss.

### N5 — MINOR: the bushing can rise 0.2–0.3 (up to 1.1 with unmatched heads), not "at most 0.10"
**What.** §2.4 says "a ring 0.10 above the head lets the bushing rise at most that much". The finger rests on the spacer by
gravity and has 0.10–0.20 axial play under the shims (`FINGER_PLAY` 0.15). When the withdrawing tube pulls the sheet
and bushing up, the head lifts the finger through its play, so the rise is gap + play = **0.20–0.30**, plus the
deflection of a printed arm 9.5 long.

The finger is also set over the **thicker** head. If the heads are not matched (±1/64 in each, so up to 0.79 apart), the
thinner one can rise up to about 1.1.

Stroke 1 matters here. The 0.889 tube OD sits in a 0.762 hole, so the sheet grips the tube on the way out. Inside
r 2.6 the sheet is held down only by the bushing face, so it lifts with the face. The 10 µm sheet-shift allowance
(UNVERIFIED) is what this eats into.

**Fix.**
- Preload the finger downward: a thin wave washer or a ⌀4 × 1 O-ring under the shims, which also gives the swing some
  friction.
- Or set the axial play to ≤ 0.05 and the gap to 0.05.
- Correct the sentence in §2.4, and add the gap over the thinner head to the RFQ reasoning (matched head thickness).

### N6 — MINOR: "lap the longer face until they agree within 0.02" can mean removing up to 0.8 mm of Rc 62 steel by hand
**What.** With ±1/64 in on each under-head length, two unmatched bushings can differ by up to 0.79 mm. Hand-lapping that
much off a hardened ⌀4.76 face while keeping it square, so that it seats flat on the sheet, is not a bench job.
docs/36 §2.4 and §4 offer lapping as the alternative to a matched order.

**Fix.**
- Lap only differences ≤ 0.05.
- Above that, send the longer bushing to a surface grinder (spin fixture or V-block, face square to the body within
  0.01), or make matched length a condition of the order.
- Check squareness after lapping: face on a flat plate with blue, or a square and a feeler.

### N7 — NOTE: the shoulder screw differs from the model
The 4-M3 size is a manufacturer extension of ISO 7379 (Elesa-Ganter, page). For GN 35215 / ISO 7379-4-M3-10 the
datasheet gives:
- head ⌀**7 × 3** (params.py:108 has 8 × 2.5);
- thread **7** (build.py:135 assumes 6);
- shoulder length **10 +0.25**, d1 f9.

Effects:
- The thread in the 7.5 hole leaves 0.5, which still passes ≤ depth − 0.3.
- The grip-to-head clearance drops from 2.07 to about 1.57, still ≥ 0.5.
- The +0.25 on l1 is absorbed by the shims.

Also, the shoulder's end face bears on the faced brass insert, an annulus of r 1.5–2.0. Specify a light torque (≈ 0.3–0.5
N·m) so it does not drive the insert down. Update params.py and docs/36 §3: "ISO 7379-4-M3-10 (Ganter GN 35215 or
equivalent; 4-M3 is not in the ISO sheet)".

### N8 — NOTE: check and model details
- The check "bushing face flush with the foot" (build.py:95–96) only tests `FACE_MATCH <= 0.03`, a constant. Label it as a
  procedure item, or replace it with the real measurement after N1 step 5.
- `SHEET_T_TOL` = 0.05 (drawing) is used in the tip-depth, plate-float and screw checks. The stock sheet is ±0.08 (J-Flex,
  sourcing §6). Over a whole sheet the tip depth becomes 0.12–0.38, still inside 0.1–0.49, so nothing fails. Say so, or use
  0.08.
- The 0.3 lead-in chamfer under the ring is "to add when printing; not modelled" (docs/36 §2.1), so a print from
  `J-005_finger.stl` will not have it. Model it in `parts.finger()`, since the STL is the print file.
- The amesweb "Radius Min." column (D, 1/32 in = 0.79) is unexplained. If it is the head's top-edge radius, the flat rim of
  the smallest head ends near r 2.8, inside the ring's r 3.2. That is harmless for a retainer with a 0.1 gap, but ask for
  it in the Carr Lane head drawing request.

### N9 — NOTE: facing the nose square
§2.5 faces the nose on abrasive paper over a ⌀3 clearance hole, with 17.96 of tube sticking through. That allows only
rotation about a loosely guided axis, so squareness depends on the hand. A tilted nose still stops, on one edge, but
less repeatably.

Better: face it in the jig's own axis. Put a disc of abrasive (pierced ⌀2) on the bushing head in the liner, insert the
handle, and rotate it under light pressure. The tube is guided by the bushing, so the nose is faced square to the axis
and against the surface it will land on. Allow for the paper thickness, which the test punches calibrate anyway.

### N10 — NOTE: parking holes and renders
- The parking holes are 9 deep (params.py:129) for a 12.7 body, so the idle bushing stands on its **ground face** on the
  printed hole bottom, with the head 3.7 above the base. Make them 13.5 deep so the head seats on the base top and the face
  touches nothing.
- `section_detail.png`, `base_top.png` and `head_plate_underside.png` are still from 21:47 (Rev B), and
  `handle_B_section.png`, listed in §2.1, does not exist yet. Re-check them after the render run.

---

## Summary

Revision C resolves every round-2 MAJOR in the design:
- the bushing face is located by the bushing itself;
- the finger height is set at assembly;
- the full-rim ring makes the recesses irrelevant;
- the boss is 1.03 from the largest head;
- the faced nose can only remove material.

The checks now run at the ±1/64 in extremes, and the arithmetic re-computes correctly.

The new risk is in the procedure that Revision C relies on. Bonding the liner with the precision bushing inside it, using
a wicking retaining compound and no release agent, can lock the bushing into the liner (N1). The written set-up for that
bond is also not physically consistent (N2). Both are cheap text fixes, but N1 must be fixed before anyone bonds a liner.
The finger's 90° swing is blocked by the thumb heads at about 75°, though 58–75° works (N4). The other items are minor
corrections.

Converged: no (N1 MAJOR open; the fix is procedural, with no CAD change)
