# Review of the washer punching jig (docs/36 Revision A), round 1

Reviewer: independent agent (mechanical / fixture design / lab practice), 2026-11-18.
Read: docs/36, `cad/elisa_cad/tier2_cell/jig/{params,parts,build}.py`, `results/tier_round/punch_jig_sourcing.md`,
`cad/out/tier2_cell/punch_jig/` (check_results.json, assembly_iso.png, section.png, section_detail.png). Re-ran
`python -m elisa_cad.tier2_cell.jig.build --fast`: all checks pass, **32 rows** (the doc says 33).
Spot checks on the web this session: SYNEO catheter-punch page (both part numbers, edge 0.030/0.055 in, OD .035/.065,
ID .027/.049, 1.500 in, TiN, middle tip, no tolerances: confirmed); Ted Pella Rapid-Core page (15115-2 ID 0.77/OD 1.07,
15115-5 ID 1.5/OD 1.9, US$6.50: confirmed; no cannula length stated); Oxford Instruments eStore Rapid-Core page
(search summary only: "maximum depth 8 mm" for the line, not size-specific).

The core idea — pierce first, then blank, two hardened slip bushings exchanged in one bonded liner, sheet never
released — is sound and is the right way to get concentricity from cheap parts. The problems are in the details that
make the swap, the depth and the parts physically work.

---

## MAJOR

### 1. The bushing swap cannot be done as written: a round DIN 125 washer locks the bushing head permanently
**What.** §1 step 4: "Lift the lock screw washer a quarter turn, pull bushing A". The lock is an M3 screw with a
round ⌀7 washer at R 6.75 that overlaps the ⌀7.94 head by 0.72 mm (params.py:67–70, parts.py:242–254). A round washer
overlaps the head at every angle, so a quarter turn (0.125 mm lift) releases nothing; the bushing has to rise its full
17.5 mm to come out, i.e. the screw, washer and the loose J-004 spacer must be removed completely at every swap, twice
per washer (~200 times), next to the clamped strip. The real SF head has a lock-screw recess and a "slip" recess
(Carr Lane: "slip down, then rotate to lock"), sized for the Carr Lane lock-screw head; the CAD models the head as a
plain cylinder (parts.py:229–232), so neither the release nor the bearing area of the washer on the recessed head is
represented. The 0.72 mm overlap may also land partly in a recess.
**Fix.** Use the bushing as designed: Carr Lane lock screw for SF-12 (LS-0; confirm thread and head ⌀ with Carr
Lane, then an 8-32 or matching insert) at R 17/64 in, procedure "rotate bushing counter-clockwise to the slip recess,
lift". Or, if the M3 is kept, replace the washer by a clamp finger that swings clear (a printed or steel lever on
the screw, or a washer with a flat ground at r ≥ 4.0 from the bushing axis when turned), and model the head
recesses from the Carr Lane drawing before checking the overlap. State the swap sequence that results.

### 2. Liner "bonded" in a 7.95–7.96 hole is actually a 10–28 µm press fit; the insert next to it violates the vendor wall
**What.** Liner L-20-8 OD is 5/16 in **+0.0013/+0.0016 in** = 7.970–7.978 mm (sourcing §4, params.py:60), but the
hole is reamed to 7.95–7.96 (docs/36 §2.1, params.py:66). Interference 0.010–0.028 mm diametral: the retaining
compound is wiped off, the liner is pressed into a print, and the CAD/checks hide it because the liner is modelled at
nominal 7.9375 (parts.py:226). Next to that bore the lock-screw heat-set insert hole (⌀4.0) leaves a printed wall of
6.75 − 3.975 − 2.0 = **0.77 mm** (build.py check "≥ 0.7"); ruthex gives **W min 1.6 mm** for RX-M3x5.7 (sourcing §5).
Heat-setting an insert 0.77 mm from a pressed steel liner will bulge or crack the wall, and with SLA resin (allowed
in §2.1/§4) heat-set inserts do not work at all (thermoset).
**Fix.** Ream the liner hole to a standard 8.00 mm (H7 reamer, readily available; 7.95–7.96 is not) → 20–30 µm
clearance, bond with a gap-filling retaining grade, liner located on a flat plate and a ⌀4.76 gauge pin through
a tight bushing for squareness. Move the lock screw out to wall ≥ 1.6 (e.g. lock axis ≥ 7.6 mm, which also requires
Finding 1's clamp redesign), or use an epoxied insert / tapped steel. Specify MJF PA12 (or FDM PETG/ASA) for parts with
heat-set inserts; for SLA, epoxy the inserts. Add a check on the actual liner OD (nominal + tolerance) and on the
insert's vendor minimum wall.

### 3. Handle A has no tube pocket: the ⌀1.4 push-wire hole is larger than the 0.889 tube
**What.** parts.py:221 cuts the tube pocket (tube_od + 0.05 = 0.939, 10 deep) and a ⌀1.4 through hole
(`PUSH_WIRE["B"] + 0.3`) in *both* handles. In handle A the 1.4 hole swallows the 0.939 pocket: no blind bore, no
shoulder, the tube sits in a 1.4 hole with 0.25 mm radial gap, and the 30–60 N punching force (estimate below) is
carried by the glue alone; the doc (§2.1 "blind bore 10 deep for the tube … ⌀1.4 through hole") does not describe
the part as modelled. In handle B the shoulder is only (1.4 → 1.70)/2 = 0.15 mm of printed material. Separately a
⌀0.94 × 10 blind bore is not printable to size by SLA/MJF/FDM; it has to be drilled.
**Fix.** Push-wire hole per punch: ⌀0.8 for A (wire 0.6), ⌀1.3 for B (wire 1.1), so each tube end bears on a
printed shoulder; print the pockets undersize and drill to tube + 0.02–0.05 with a numbered drill; bond with epoxy.
Better still, a steel or brass collar (pin-vise style or a drilled ⌀3 rod) as the handle core. Add a check that the
pocket diameter exceeds the wire hole.

### 4. The Rapid-Core 1.5 (membrane disc, and the "fallback pair") cannot reach through a slip bushing
**What.** The guide stack is head 4.76 + body 12.7 = 17.46 mm, plus 0.4 below the foot: a cannula must project
≥ ~18 mm from its holder. Rapid-Core has a short retractable cannula; no vendor states its length (sourcing §1 note a,
Ted Pella page checked: none), WPI states "max sample depth 2 mm" and Oxford Instruments "maximum depth 8 mm"
(snippet). Bushing C (SF-12-8-.0751) and the "Fallback punches … in a third slip bushing" therefore very likely do
not work, yet the bushing is in the BOM and the fallback is offered to the user (§0, §8). Note also that the membrane
disc needs no concentricity at all, so a precision guide buys nothing.
**Fix.** Drop bushing C from the BOM: punch membrane discs freehand on the backing (or through a printed guide plate
with a ⌀2.0 hole). For the fallback pair, state that it needs either a short bushing (SF-12-4 + no head, or a custom
bushing) measured against a cannula in hand, or a different jig; buy one Rapid-Core (US$6.50) and measure the
exposed length before relying on it.

### 5. No positive depth stop: stroke end "felt" in a soft backing
**What.** §1 step 3: push "until it stops in the backing (0.15 mm in; felt as the end of the cut)". Nothing stops
it: HDPE yields progressively, so the operator either stops early (washer still attached by a ligament, especially
with the middle edge whose inner bevel is still 0.07 mm above the edge) or drives the tip through the 0.79 HDPE into
the printed base. The reach check (build.py, "handle ≥ 3 above the bushing") deliberately *prevents* the obvious
stop. The two strokes per washer at ~200 strokes will not be uniform.
**Fix.** Make the stroke end a hard stop: a collar on the tube (or the handle face) landing on the bushing head when
the tip is 0.15–0.25 mm into the backing; set the exposed length with a gauge block when bonding (±0.05 is enough,
since the HDPE takes the error). Note the ⌀10 handle overlaps the lock-screw head radially (lock head r 4.0–9.5 from
the axis, top at z 22.0) — a stop collar ⌀ ≤ 7 on the tube, or the lock relocated, is needed. Turn the reach check
into "stop lands on the head with the tip 0.1–0.3 into the backing".

---

## MINOR

### 6. Outside punch with a middle edge squeezes the product into a 1.245 bore
The washer (⌀1.40) is the slug of stroke 2 and is forced into the 1.245 bore: 11 % hoop compression at its outside,
and the 0.76 hole must collapse to ~0.4 (area conservation) or the ring thickens/buckles while the cut is still
forming. Standard practice is the edge on the product side: **inside edge** (straight bore 1.40) for the blank,
middle or outside edge for the pierce (the hole is the product; a 0.76 middle edge is fine there). docs/36 already
asks for this in the RFQ but treats it as optional. Fix: make "inside edge, ID 0.055 in" the primary RFQ line for the
outside punch and the middle edge the fallback, and add washer flatness/edge condition to the 10-washer acceptance
(§5.2).

### 7. Concentricity budget: worst case already exceeds the limit, and the largest real risk is not in it
RSS 0.025 / worst 0.068 vs 0.050 (params.py:125–135; arithmetic checked: per stroke 7.6 + 5 + 11.4 + 10 µm). Missing:
sheet shift during the swap (FKM sticking to the withdrawn bushing face, slug dragged out of the hole), asymmetric
elastomer flow at the cut, the 0.25 mm radial dowel play if the operator pushes the plate (common-mode only if the
sheet follows the foot), and the measurement error of the acceptance microscope. The edge-runout term assumes
10 µm; a hypodermic wall eccentricity of ~10 % of wall (0.01–0.02 mm) puts the middle edge off by 5–10 µm, so it is
plausible but not conservative. Fix: list the missing terms with an allowance (e.g. 10 µm sheet shift), say that
acceptance rests on the measured washers (§5.2) rather than on the budget, and measure 10 washers' offset before
running the batch. Optionally tighten the tube bore to measured + 0.0002 in.

### 8. Bushing end may not sit at the foot face: liner/plate length stack
PLATE_T = LINER_L = 12.7 (params.py:104). A printed 12.7 plate is ±0.1–0.2; the liner is bonded flush at the foot,
so the liner top ends above or below the plate top. If the plate is thicker, the bushing head seats on plastic and
the bushing face stands back from the foot; if thinner, on the liner. Fix: model the plate 0.3 mm thinner than the
liner (or a ⌀9 counterbore 0.3 deep around the liner on top) so the head always seats steel-on-steel on the liner
end; then the bushing face is flush with the liner face within Carr Lane's length tolerance (state it, UNVERIFIED).

### 9. Clamp: two screws and the foot are collinear; screw force is not 50 N
Screws at (15, 16) and (−15, −16) and the foot at the origin lie on one line (params.py:95). Rocking across that line
and differential screw torque are resisted only by the ⌀10.9 foot (kern moment ≈ N·D/8 = 136 N·mm at 100 N, i.e. a
6 N imbalance over the 21.9 mm lever lifts one edge). The tilt is common-mode to both strokes, so concentricity is
not hurt, but the strip load is uneven. "Finger tight" on a ⌀12 knurl is typically 0.1–0.3 N·m → 170–500 N per M3,
not 50 N: friction is better than the check says, the squeeze is still sub-µm, but the imbalance is larger. Fix:
a third screw (foot inside the triangle) or springs under the screw heads (set force, equal sides); state the force
as a range.

### 10. Pitch scale is off by 1 mm from the hole positions
Holes downstream are at multiples of 3 (21, 24, …), ticks at 22, 25, … 37 (params.py:83, parts.py:180–186; only six
ticks, long ticks at 22 and 37, not "every 15"). Nothing to read for the first seven washers (holes hidden under the
40 mm plate). Fix: SCALE_X0 = 21; mark the strip end start position; or a printed index pin that drops into the last
visible hole.

### 11. Build checks that test something else, or not at all
- "thickest strip clears the relief by ≥ 0.5" (build.py) mixes the nominal foot height with the thickest strip; the
  plate rides on the strip, so the true clearance is always ≈ RECESS_DEPTH; harmless but mislabeled.
- "plate floats … foot above the rail tops": the foot (r 5.47) is never over the rails (r ≥ 7.3).
- Liner modelled at nominal OD (hides Finding 2); handle A geometry unchecked (Finding 3); outside punch checked
  against screw_0 only, not screw_1; inserts not in the interference set; hole punch/handle A never placed.
- Count: 32 rows, docs/36 §0/§6 say 33.
- section.png / section_detail.png show the outside of the remaining half (view from −y after removing y > 0), not the
  cut face: no liner, bushing, tube or sheet is visible in section. Render from +y (or remove y < 0).
Fix accordingly.

### 12. Thumb screw M3 × 18 DIN 464 is probably not a stock length
DIN 464 M3 is usually 6/8/10/12/16/20. M3 × 20 fits (engagement 6.26 at nominal, insert hole 6.7 deep: 0.44 margin,
6.36 at the thinnest stack — tight); M3 × 16 gives 2.3 mm, too little. Fix: M3 × 20 with the base insert hole 7.5
deep, or a plain knurled-head screw at a stock length; confirm the head (McMaster lists 2.5 mm, DIN says 7.5).

### 13. Plate dowel hole printed 3.05 unreamed
Printed small holes come out −0.05…−0.15: the plate may not go on the pins, or rattle if drilled out. Fix: print
2.8 and ream 3.0 H8 + light hand finish (the round hole); the slot likewise reamed at its ends.

---

## NOTE

14. Slip fit of a 0.889 TiN tube in a hardened bore with 10–18 µm play over 17.5 mm: a tube bow of 0.0005 in/in
    already uses ~9 µm; ask SYNEO for straightness and check that the tube slides freely before ordering the bushing
    bore, or accept +0.0005 in.
15. Buckling: tube A free above the bushing ~10 mm; EI ≈ 3.8×10³ N·mm² → fixed-free ≈ 94 N, more than the estimated
    30–60 N (FKM cut ~10 N/mm × 2.4 mm + HDPE indentation), so acceptable; a stop (Finding 5) also limits overload.
16. The hole slug may stay in the sheet and be blanked together with the washer; expect a slug with each ejected
    washer and sort under the microscope.
17. HDPE raised rims from previous cuts sit under the foot at x = +3 and lift the FKM locally; renew the backing
    per strip as written; consider a 1.5 mm self-healing mat (UNVERIFIED part) or PP.
18. Throughput ~1–2 min per washer (two screws, lock, two strokes, swap, eject): ~2–3 h for 100; acceptable.
19. Safety: TiN tips are needle-sharp; add tip caps and a pin vise for the push wires; handle ⌀10 × 30 is small for
    30–60 N — a ⌀16 mushroom top is kinder to the palm.
20. BOM missing: reamers (8.00 H7, 3.0), drills for the handle pockets, epoxy for tubes/inserts (retaining compound
    is not for a 0.25 mm gap), tip caps, gauge block/feeler for the exposed length, measuring microscope with
    reticle; retaining-compound grade unspecified.
21. parts.py:170 docstring says "two M4 heat-set inserts"; they are M3.

---

## Verdict

Five MAJOR findings (swap lock, liner fit + insert wall, handle A pocket, Rapid-Core reach, no depth stop); none
invalidates the concept, all are quick to fix in params/parts and the doc.

Converged: no
