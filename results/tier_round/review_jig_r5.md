# Review of the washer punching jig (docs/36 Revision E), round 5

Reviewer: independent agent (mechanical / fixture design / lab practice), 2026-11-18.
Read: docs/36 (Rev E), `cad/elisa_cad/tier2_cell/jig/{params,parts,build}.py`, `results/tier_round/punch_jig_sourcing.md`,
`review_jig_r1.md` … `review_jig_r4.md`, `cad/out/tier2_cell/punch_jig/check_results.json` and the renders `section.png`
and `section_detail.png` (regenerated 22:27, after the Rev E commits; they show the 8.10 hole with its epoxy gap and the
new detail title).

Checks: I did not run `build --fast` (a full build with renders was running). Instead I called `build.checks()` from a
scratch script on freshly built solids, without exporting anything: **45 checks, all pass**, matching docs/36 §0 and §6
and `check_results.json`. The full build finished at 22:27, also reporting 45 passing. I wrote nothing in the
repository except this report.

Scratch numbers (Derived): plate top 5.56 above flat 1 in the inverted bonding set-up; liner engaged 8.73 in the
plate; bond gap 0.122–0.149 diametral; parking hole 1.10 under the longest face, floor 1.30; spacer printed 6.81;
finger STL 2.5 thick; drill-point cone from ⌀8.1 to ⌀5.2 at 118° is 0.87 deep.

---

## Round-4 findings (and the round-3 items round 4 marked partly)

| Item | Topic | Status | Reason |
|---|---|---|---|
| R4-1 (MAJOR) | Plate lifted through wet epoxy carries the liner off the head | **resolved** | §2.4 step 4 now states the rule "the plate may only move down over the liner once it carries epoxy". It sets the plate on three compliant pads with the foot 0.3–0.5 above the bushing face, then presses flat 2 down until it rests on both the foot and the face. The drag then pushes the liner onto the head. A side-light check of the liner–head joint is added. Step 5 says that the plate, with the gelled liner, is lifted off, then lowered back. With the 8.10 hole the radial gap is now 60–75 µm, so drag is far lower anyway. Small procedural gaps remain (F2, F3, NOTE). |
| R4-2 (MINOR) | Two nose-facing methods; grit in the fits | **resolved** | §2.5 gives one method: the handle's own bushing in a separate block (⌀4.77 reamed print, or a spare L-20-6 bonded into one), with a pierced abrasive disc, and both parts cleaned before they go back into the jig, "which must never see grit". §3 tools and §4 bullet 4 agree. The depth target is still not measurable as written (F1). |
| R4-3 (NOTE) | Parking hole 0.10 deeper than the longest body | **resolved** | `PARK_BOSS_H` 5.5 gives a hole 14.2 deep and 1.10 under the longest face, with a floor of 1.30 (params.py:149, 211). A new check (build.py:154–156) covers it, and §2.1, §4 ("drill to 14.2 from the boss tops") and §6 agree. |
| R4-4 (NOTE) | Editorial slips | **resolved** | Fixed: the spacer text in §2.4 ("printed 1.2 higher than needed (6.81) and faced"); §4 now lists the ⌀5.2 hole once; `STRIP_L` comment "about 25"; the `base()` docstring (2.95, parking bosses); the detail render title "foot, bushing face, sheet" (build.py:288, PNG regenerated). |
| R4-5 (NOTE) | Finger thickness not in the shoulder stack | **resolved** | The check now uses `SHOULDER_L` 10.00 (lower limit) and `FINGER_T + 0.05`, with a margin of 0.14 at the highest head. §2.4 says the finger is faced to 2.5. The STL is printed at 2.5, so there may be nothing to face (F5, NOTE). |
| R4-6 (NOTE) | 11–22 µm bond gap | **resolved** | `LINER_HOLE_D` 8.10 (+0.02) gives a bond gap of 0.12–0.15 (check build.py:139–142). §2.1, §2.2 and §3 all say 8.10. The liner can now tilt about 15 mrad in the hole, so a drill-press hole that is a few mrad out of square no longer binds it, and the bushing on the two flats sets the axis. The liner's lateral offset (≤ 0.075) leaves the bushing body 0.15 radial in the ⌀5.2 foot hole. |
| R3-N2 | Bonding set-up physically inconsistent | **resolved** | See R4-1. Step 5 now says the plate is lifted. |
| R3-N9 | Facing the nose square | **resolved** | See R4-2. |

---

## New findings

### F1 — MINOR: the depth-setting target in §2.5 cannot be measured as written

**What.** §2.5 says the nose is faced "until test punches in a scrap strip cut through with the tip 0.2–0.3 into the
backing". The method then says "measure against the head with a feeler".
- With the nose resting on the head, a feeler between them measures nothing.
- The depth of a 0.89 mm ring cut in HDPE cannot practically be read to ±0.05.
- A test-punch acceptance forces a loop for every facing pass: block → clean → jig → test punch → block.

The tolerance is generous (tip 0.12–0.38 is accepted, and too shallow shows up as an uncut washer), so the jig still
works. But the technician has no number to face to.

**Evidence.** docs/36 §2.5, lines 160–169. Per `tip_depth_range()` and `protrusion()`, depth into the backing is the tip's
protrusion below the bushing face minus the sheet thickness.

**Fix.** State the target as a measurable protrusion: with the nose on its bushing head (disc removed), the tip
should stand **measured sheet thickness + 0.25 (about 0.50) ±0.05** below the bushing's face. Make the facing block
thinner than the bushing body (for example 8 mm), so the face and tip stand free. Measure the protrusion with a depth
micrometer, or under the microscope with the reticle, or go/no-go by standing the bushing face on two feeler stacks of
0.45 and 0.55. Confirm once with a test punch in the jig.

### F2 — NOTE: squeeze-out at the plate-top mouth ends up beside the bushing seat

In the inverted set-up the liner enters the 8.10 hole from the plate-top mouth. The mouth sweeps down the liner and
across the epoxy band, and stops 0.2–1.4 (0.8 nominal) from the head. Paste scraped off the band collects on the
liner's exposed end, right beside the seat where the head bears. Two things limit the risk:
- with the 60–75 µm radial gap, less paste is scraped;
- the head is released, so a bead cast against it ends at the seat plane.

Still, a bead that wraps the liner's end face or enters the head's recesses would hold the head off its seat. Fix:
in step 5, after lifting the plate at gel, cut any squeeze-out from the liner's exposed end and the plate top (scalpel)
before lowering it back. Optionally add a 0.3 × 45° chamfer at the plate-top mouth of the 8.10 hole.

### F3 — NOTE: details of the Rev E bonding steps that a technician will ask about

- **Pad height.** "Foot 0.3–0.5 above the bushing face" depends on the parts as printed and as bought. Give the pad
  height as *(bushing overall length, head + body) − (plate thickness as printed) + 0.4*, measured. Form the clay
  slightly higher and press the plate down to it, never up.
- **Turning the bushing.** In this set-up the head sits under the plate, in a gap of about 5.6, with flat 2 weighted
  on the face. Say "turn it by the head with tweezers, reaching between the pads".
- **Step 5, re-lowering.** After the plate is lowered back, press flat 2 down again until it rests on the bushing face.
  Repeat the light check before the cure. A soft gel can let the liner shift a little in the plate when the plate is
  lifted, and pressing down (plate moving down only) restores flush.
- **Gel point.** Judge gel from the residue in the mixing cup.

### F4 — NOTE: "drilled or reamed 8.10" leaves a conical ledge if drilled

A twist drill leaves a 118° cone from ⌀8.1 down to ⌀5.2, 0.87 deep. The ledge ring at the body hole is then about
0.9 thick, not the 1.77 that the check (build.py:107–110, "ledge ring ≥ 1.5") assumes. Two things make this harmless:
- the cone falls away inside the liner's OD, so the liner's float gap is unchanged;
- the foot ring is backed by the full plate outside r 4.05.

Say in §2.1/§4 that the depth "1.78 above the foot" refers to the full-diameter corner. A reamer, or a flat-bottom
counterbore, leaves the flat ledge that the CAD models.

### F5 — NOTE: the finger is printed at the thickness it is to be faced to

§2.4 says the finger "is faced to 2.5", but J-005 is 2.5 thick in the STL (`FINGER_T`). A print at 2.3–2.5 cannot be
faced up, though a thin finger is harmless (the shims take the room). Either print it about 2.7 (a `FINGER_FACE_ALLOW`
like the spacer's) or write "faced to 2.5 if printed thicker".

---

## Summary

Revision E resolves every round-4 finding, including the MAJOR R4-1, and the round-3 items N2 and N9 in both the CAD and
the document:
- the plate moves only down over the epoxied liner, on compliant pads;
- the plate is lifted off at gel;
- one nose-facing method, in a separate block;
- 14.2 parking holes;
- the finger stack checked at the shoulder's lower limit;
- an 8.10 hole that gives a proper epoxy gap and lets the bushing, not the hole, set the liner's axis.

45 checks pass, the renders are current, and document and CAD agree.

The jig as documented can be built, assembled and used by a competent technician. Remaining: one MINOR (F1, give the
nose-facing a measurable protrusion target) and four NOTEs on the bonding and printing procedure. Acceptance still rests
on the bench checks of §5: the SYNEO tube OD, straightness and edge runout, and ten measured washers.

Converged: yes
