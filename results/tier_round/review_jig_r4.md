# Review of the washer punching jig (docs/36 Revision D), round 4

Reviewer: independent agent (mechanical / fixture design / lab practice), 2026-11-18.
Read: docs/36 (Rev D), `cad/elisa_cad/tier2_cell/jig/{params,parts,build}.py`, `results/tier_round/punch_jig_sourcing.md`,
`review_jig_r1.md`, `review_jig_r2.md` and `review_jig_r3.md`. Also `cad/out/tier2_cell/punch_jig/check_results.json` and the
renders `section.png`, `section_detail.png`, `assembly_iso.png`, `assembly_exploded.png` and `handle_B_section.png`.

Re-ran `python -m elisa_cad.tier2_cell.jig.build --fast`: **44 checks, all pass**, which matches docs/36 §6. The run changed
only the timestamps in the STEP headers. I restored those files with `git checkout`, so the working tree is unchanged.

All seven PNGs are dated 22:17, one minute before the Rev D commit (22:18), and they show Revision D: the short liner, the
body through the foot ring, the parking bosses and the handle pocket shoulder. Round 2's finding R2-11 is therefore
resolved.

I used one throw-away calculation (inline Python) for three things:
- the finger stop angle against the DIN 464 heads;
- the liner's weight against the drag of the epoxy;
- the parking-hole margin.

No web checks this round. The vendor numbers are unchanged from round 3.

---

## Round-3 findings

| R3 | Topic | Status | Reason |
|---|---|---|---|
| N1 (MAJOR) | Locator bushing glued into the liner | **resolved** | §2.4 steps 1–6 and §3 now specify: paste epoxy instead of an anaerobic compound; epoxy on the middle third only; mould release on the body and under the head; the bushing turned until gel, then lifted out and cleaned; free-turn and flush checks after cure. §4 refers to these steps. (The new set-up has a different defect, see F1.) |
| N2 | Bonding set-up physically inconsistent | **partly** | The inverted two-flat set-up is written up (§2.4 step 4) and "two flat plates" is in the §3 tools. But step 4 tells you to *raise* the plate after it has been lowered onto the liner, and raising drags the liner off the head (F1). Step 5's "lift it out" does not say that in this set-up it is the plate that has to be lifted off. |
| N3 | Reamer, ledge gap, body hole | resolved | Chucking reamer with a short lead; depth set from the foot face. Ledge at 1.775 above the foot (params.py:100–102; the doc's "1.78 ±0.1" agrees). `LEDGE_GAP` 1.4, and `PRINT_TOL` is now in the check (build.py:289–294): the worst-stack gap is **0.41**, and the ring is 1.77 thick. ⌀5.2 drilled without unclamping. One wording slip remains (F4). |
| N4 | Finger cannot swing 90° | resolved | The lift check is now run over 60–74° at the largest head with a 0.1 offset (build.py:258–264). A new check tests the finger at its stop against every part (build.py:265–271), and the 90° case is reported as information only. My calculation: the ring touches a ⌀12 head at (15, 16) at **74.3°** (centre distance 10.80 against 10.8 needed), so 74° as the stop is right. Docs §1, §2.1 and §6 agree. |
| N5 | Bushing rise / axial play | resolved | NBR O-ring 4 × 1 preload under the shims, `FINGER_PLAY` 0, gap 0.05 (params.py:107–116). The rise is stated in §2.4, including the extra 0.8 for unmatched heads, and that is given as the reason for the matched order. The preload is about 15–30 N at 30 % squeeze, well above the few newtons the withdrawing tube can put on the bushing, so the bushing should rise only by the gap. |
| N6 | Lapping up to 0.8 mm by hand | resolved | §2.4 and §4: lap only up to 0.05 with a blue check; anything more goes to a surface grinder; or order the pair matched. |
| N7 | Shoulder screw data | resolved | params.py:118–119 has head 7 × 3 and thread 7 (Ganter GN 35215). §3 calls 4-M3 a maker's extension. §2.4 gives a light torque. The checks pass: thread 7.0 in 7.5, grip 1.57 from the screw head. |
| N8 | Check and model details | resolved | The face-flush check is labelled as a procedure item (build.py:295–297). `SHEET_T_TOL` 0.08 gives a tip depth of 0.12–0.38. The chamfer is modelled in `parts.finger()` (parts.py:113–116); I checked that it is a 45° × 0.3 lead under the outer edge of the ring. The head drawing is in the Carr Lane RFQ. |
| N9 | Facing the nose square | **partly** | §2.5 says the nose is faced "against its own bushing … in the jig". The same paragraph then says "abrasive paper on a flat plate with a ⌀3 clearance hole for the tube", which is the round-3 method. §4 does not say which method to use. See F2. |
| N10 | Parking holes, renders | resolved | Bosses ⌀10 × 4.5 with ⌀5.3 holes 13.2 deep, so the head seats on the boss (parts.py:53–55). All renders are regenerated. The margin is thin (F3, NOTE). |

---

## New findings

### F1 — MAJOR: the inverted set-up lifts the plate through the wet epoxy, which carries the liner off the head and leaves the bushing face up to 1.4 mm proud of the foot

**What.** docs/36 §2.4 step 4 reads: "Lower the plate over the liner, foot up. Lay flat 2 … across the foot and the bushing
face, **raise the plate on shims until its foot touches flat 2**".

Lowered over the liner, the plate comes to rest on the only thing that stops it: its ledge lands on the liner's upper end.
At that point the foot is 1.4 (`LEDGE_GAP`) below the bushing face. Flat 2 then lies on the face, and the plate has to
be raised by about 1.4 to reach it.

Step 3 has already coated the middle third of the liner's outside with paste epoxy. That epoxy now sits in an
11–22 µm radial gap. The only force holding the liner on the head is its own weight.

**Evidence (Derived).**
- **Liner weight.** L-20-6, ⌀7.97/⌀4.76 × 9.525 steel: 2.4 g, so **0.024 N**.
- **Drag of the epoxy.** The band is π·8·3.2 ≈ 80 mm². For a paste epoxy of about 100 Pa·s, raising the plate at 1 mm/s
  across a 15 µm gap gives a shear stress η·v/h ≈ 6.7 kPa. That is **about 0.5 N**, twenty times the liner's weight.
  Even the yield stress of a thixotropic paste alone (about 200 Pa → 0.016 N) is comparable to the weight.

So the liner travels up with the plate and stays seated on the ledge. It cures there, 0 to 1.4 above the head instead of
on it. In use the head then sits on a liner end that is too low. The bushing face stands up to **1.4 mm below the foot**,
which is more than the 1.04 mm of sheet and backing together. The plate then rocks on the bushing face, and the foot no
longer clamps the strip.

Step 6 (straightedge and feeler) catches the error, but only after cure. By then the liner is bonded, so the plate and
the liner are scrap and the hole has to be re-reamed in a new print. Followed literally, the procedure gives this result
every time.

**Secondary, same step.** Lowering the plate's 8.00 hole over the epoxy band scrapes the paste toward the head end. It
collects as a bead at the hole mouth, 0.8 above the released head, hanging downward in the inverted set-up. The mould
release limits the damage. The fix below keeps the bead out of the slip fit.

**Fix (text only; no CAD change).** The rule is that the plate may only move **down** relative to the liner once the liner
carries epoxy, because the drag then pushes the liner onto the head.
- Rewrite step 4 as: "Support the plate on three compliant pads (modelling clay or soft springs) so that, lowered over
  the liner, its foot stands 0.3–0.5 above the bushing face. Lay flat 2 (PTFE film) on the foot and press or weight it
  down until it also rests on the bushing face. The plate only moves down over the liner, and the head stops the liner."
- Optionally, check before gel that the liner is on the head: no light under the liner end at the head, seen from the
  side.
- In step 5, say that the *plate* (with the gelled liner) is lifted off the bushing, the bushing is cleaned, and the plate
  is lowered back over it.
- Optionally, add a 0.3 × 45° chamfer at the mouth of the liner hole to catch the scraped paste.

### F2 — MINOR: §2.5 gives two facing methods, and the in-jig one puts grit into the 2.5 µm and 8–15 µm fits

**What.** §2.5 says the nose is faced "against its own bushing (the handle's tube running in that bushing in the jig keeps
the face square)". It also says "abrasive paper on a flat plate with a ⌀3 clearance hole for the tube". §4 says only
"face the nose against its own bushing". If the in-jig method is meant, abrasive grit and PA12 dust are made directly on
the bushing head. That is next to:
- the liner–bushing slip fit (1.3–7.6 µm radial), which docs/36 §1 step 7 already treats as sensitive to FKM debris;
- the tube–bore fit (8–15 µm).

**Fix.**
- Choose one method and state it in §2.5 and §4.
- Recommended: hold the bushing in a separate block (a spare L-20-6 liner pressed or bonded into a scrap plate, or a
  ⌀4.77 reamed hole in a block), with a pierced abrasive disc on its head. Rotate the handle with the tube guided by that
  bushing.
- Afterwards, clean the bushing and the tube (ultrasonic or solvent and air) before they go back into the jig.

### F3 — NOTE: parking hole only 0.10 deeper than the longest bushing body

`PARK_DEPTH + PARK_BOSS_H` = 13.2 against a body of 12.7 + 0.397 = **13.10** (params.py:142, 204). A printed hole bottom
0.1–0.2 too shallow (MJF/FDM) puts the idle bushing back on its ground face. Make the boss 5.5 high, so the hole is
14.2 deep and the base floor stays 1.3. Or state "drill the parking holes to 14 deep".

### F4 — NOTE: editorial and consistency slips

- docs/36 §2.4, "**Finger.**": "the spacer J-004 is printed 1.2 high" should read "printed 1.2 higher than needed (6.81) and
  faced". §2.1 has it right.
- §4 bullet 1 lists the ⌀5.2 body hole twice: first "without unclamping" (correct), then "drill the body hole 5.2, the
  handle pockets …". Delete the second.
- params.py:130 says `STRIP_L` gives "about 30 washers per strip". docs/36 §1 and §8 say about 25, which is right:
  (100 − 21 − about 6)/3 ≈ 24.
- The parts.py:43 docstring of `base()` says "holes reamed 3.0" (params: base 2.95 press, plate 3.0 slide) and does not
  mention the parking bosses.
- `section_detail.png` is titled "foot, bushing face, sheet, tip", but the tip is not visible. The tube is drawn in the
  same grey as the backing, and the sheet is drawn over it. Give the tube its own colour, or leave "tip" out of the title.

### F5 — NOTE: the printed finger's thickness is not in the shoulder-stack check

build.py:281 checks `SHOULDER_L + 0.25 − (hi_h + gap) − FINGER_T − ORING_H ≥ 0`. Two things make that check optimistic:
- at the highest head with a shoulder at its lower limit (10.00) the margin is only 0.19;
- the check uses the +0.25 upper limit and the nominal 2.5 finger.

A finger printed 0.2 thick, together with that shoulder, squeezes the O-ring to about 0.5 (50 %). The finger then turns
stiffly. Fix: face the finger to 2.5 at assembly (it is already reamed), or add `PRINT_TOL` to the check and allow a
thinner O-ring cross-section (4 × 0.8).

### F6 — NOTE: the 11–22 µm bond gap is narrow for an epoxy and is not needed for location

In Rev D the bushing's axis is set by its face on flat 2, not by the 8.00 hole. The liner only follows the bushing.

If the reamed hole is tilted from the foot normal by more than gap/length = 0.011/9.5 ≈ **1.2 mrad**, the liner binds in the
hole. The bushing then cannot square itself on flat 2. The effect is small: a tilt of 3 mrad is 7 µm across the face.

Epoxies also bond best at 0.05–0.15 mm. A hole of 8.06–8.10 instead of 8.00 H7 would give a better bond and accept a
drill-press ream. This is optional. The current fit works if the paste is unfilled or fine-filled; say so in §3.

---

## Summary

Revision D resolves round 3's MAJOR (N1): no anaerobic compound, release on the locator, the bushing turned and lifted at
gel. It also resolves N3–N8 and N10 in both the CAD and the document. The swing window (60° free, 74.3° stop), the
O-ring preload, the Ganter numbers, the 2.5 finger, the parking bosses and the modelled chamfer all check out. The 44
checks re-run and pass, and every render is current.

One new MAJOR remains, in the bonding text (F1). The inverted set-up as written lifts the plate about 1.4 mm through the
wet epoxy. The epoxy's drag (about 0.5 N) is about twenty times the liner's weight (0.024 N), so the liner is carried off
the bushing head, and the bushing face cures up to 1.4 mm proud of the foot. The fix is a rewrite of step 4 so the plate
only ever moves down over the liner (compliant pads, flat 2 pressed down), with no CAD change. F2 (MINOR) asks for one
nose-facing method kept away from the precision fits. The rest are notes.

Converged: no (F1 MAJOR; text-only fix in docs/36 §2.4 steps 4–5)
