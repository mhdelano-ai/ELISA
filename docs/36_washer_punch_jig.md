# 36 — A punching jig for the tier-2 retainer washer

Status: desk work, 2026-11-18, Revision B (after review round 1, §7). Follow-up to docs/34 (tier-2 flow cell): the
retainer washer T2C-004 (⌀1.40 ±0.10 / ⌀0.75 ±0.10 × 0.25 ±0.05 FKM, hole concentric within ⌀0.10) is too small
for an online gasket cutter; the user asked for a printable jig to punch it in the lab, with the punches sourced,
iterated with an independent reviewer until converged. Nothing is ordered; docs/34 is not changed.
CAD: `cad/elisa_cad/tier2_cell/jig/` (`params.py` single source of dimensions, `parts.py`, `build.py`), outputs in
`cad/out/tier2_cell/punch_jig/` (`python -m elisa_cad.tier2_cell.jig.build` from `cad/`: checks in seconds with
`--fast`, about 7 min with the renders).
Sourcing: `results/tier_round/punch_jig_sourcing.md` (vendor pages read this session; [J-src n] = its item n).
Reviews: `results/tier_round/review_jig_r1.md` … ([R1-n] = finding n of round 1).
Tags: [V] read on the vendor page this session; [S] search summary only; UNVERIFIED not checked; Derived computed
here; CHOICE design choice of this document.

## 0. Summary

**Two hollow punches on one axis, never moving the sheet in between.** The hole is punched first, then the outside,
through one liner bushing bonded into a printed head plate. Each punch has its own hardened slip bushing whose bore
is ordered to the measured punch tube; the two bushings are exchanged in the liner between the strokes, and a swing
finger keeps the bushing down while the punch is withdrawn. The head plate stands on the FKM strip with a foot
around the liner and is pulled down by four thumb screws, so friction holds the strip while the bushings are
swapped. Each punch tube is bonded into a handle whose nose lands on the bushing head: the stroke ends 0.25 mm into
the backing, every time. Between washers the screws are loosened and the strip is pushed on by 3 mm.

| | Choice | Why |
|---|---|---|
| Punches | SYNEO C-Series catheter punches, straight 304 SS tubes, TiN: **CR0350275N20R4** (edge 0.76, tube 0.889, middle edge) for the hole; **CR0650495N16R4** (edge 1.397, tube 1.651) for the outside, RFQ asking first for an **inside edge** [J-src 1, 2; V] | the only catalogue punches found at 0.75 and 1.40; straight ground tubes run in a bushing; washer on nominal ⌀1.40 / ⌀0.76 |
| Guidance | Carr Lane slip/fixed renewable bushings **SF-12-8-<bore>-NCB** (bores = measured tube + 0.0002 in; nominal .0352 and .0652 in) in one liner **L-20-8** [J-src 4; V] | one liner takes bores 0.34–2.49 mm; liner-to-bushing play 2.5–15 µm; -NCB guides the tube over the full 12.7 mm |
| Retention | printed swing finger on a stepped sleeve and an M3 screw, 0.1 above the bushing head; swung 90° to lift the bushing | the swap needs no tool and loosens nothing [R1-1] |
| Depth | handle nose (⌀6) lands on the bushing head; protrusion 17.96, set per handle against its bushing | tip 0.15–0.35 into the 0.79 backing [R1-5] |
| Clamp | force-set: plate floats on the strip, foot ⌀11 around the liner, 4 × M3 thumb screws | a 0.25 mm rubber sheet under a rigid foot is nearly incompressible; a shim-set squeeze (Revision A's first version) would have needed tens of kN |
| Printed parts | J-001 base, J-002 head plate, J-003 handles (one per tube), J-004 sleeve, J-005 finger: **MJF PA12** (or FDM PETG/ASA); not SLA, the inserts are heat-set | the steel parts carry every precise function; reamed and drilled where it matters |
| Membrane disc ⌀1.5 | freehand with a Rapid-Core 1.5 (Ted Pella 15115-5, US$6.50) on the backing, not in the jig | the disc needs no concentricity, and the Rapid-Core cannula is too short for a bushing [R1-4] |

Model checks: 36, all pass (§6). Hole-to-outside offset 0.026 mm root-sum-square, worst case 0.075 (both strokes
plus 0.010 for the sheet moving at the swap) against 0.05 for the drawing; the punch edge runout (0.010 assumed) and
the sheet shift are UNVERIFIED, so acceptance rests on measured washers (§5).
**Order of work:** quote and buy the two SYNEO tubes, measure them, then order the slip bushings; print, ream,
assemble, set the stops, punch ten washers and measure them (§5).

## 1. What the jig does

1. **Load.** Cut a strip 14 × 100 mm from the 0.25 mm FKM sheet and one from 0.79 mm HDPE (the backing the punch
   ends in). Lay the backing, then the FKM, between the rails of the base, under the raised head plate.
2. **Clamp.** Turn the four thumb screws until snug (finger tight, no more): the foot presses the strip around the
   punch axis.
3. **Stroke 1 (hole).** Bushing A in the liner, finger swung over its head. Push the 0.76 punch straight down
   through the bushing until the handle's nose lands on the bushing head. Withdraw.
4. **Swap.** Swing the finger 90°, lift bushing A out, drop bushing B in, swing the finger back. The strip has not
   moved: the foot holds it and nothing touched it.
5. **Stroke 2 (outside).** Push the 1.397 punch through bushing B to its stop. With the catalogue middle edge the
   washer is now inside the tube, squeezed into its 1.245 bore (an inside-edge tube would not squeeze it). Withdraw.
6. **Eject.** Push the washer out of the tube with the ⌀1.1 wire through the handle, into a dish of water or onto a
   clean card; the hole slug may come with it (sort under the microscope). Clear the 0.76 punch with the ⌀0.6 wire
   every few holes.
7. **Feed.** Loosen the thumb screws half a turn, push the strip on by 3 mm (scale beside the rail: the ticks sit on
   the hole positions, a long tick at 30 mm), retighten, bushing A back in, repeat. About 30 washers per strip; a new
   backing strip with each FKM strip.

Membrane discs (⌀1.5): Rapid-Core 1.5 pressed freehand through the membrane on a piece of the backing.

## 2. Design

### 2.1 Parts (STEP and STL in `cad/out/tier2_cell/punch_jig/`)

| Part | File | Size (mm) | Features |
|---|---|---|---|
| J-001 base | `J-001_base.step/.stl` | 80 × 48 × 10 | flat top = datum; two rails 1.5 × 0.30 high, 14.6 apart, guide the strip; 2 × ⌀3 holes at (0, ±17) for pressed pins (print 2.8, ream 3.0); 4 × M3 heat-set inserts at (±15, ±16), hole ⌀4.0 × 7.5 deep; pitch scale ticks at x = 21, 24 … 39 on the hole positions |
| J-002 head plate | `J-002_head_plate.step/.stl` | 40 × 40 × 12.4 | liner hole printed 7.8, reamed **8.00 H7**, liner bonded flush with the foot face and 0.3 proud of the top (the bushing head seats on the liner end); foot ⌀11 (1.5 mm ring around the liner); relief 20 wide × 1.0 deep over the strip except the foot; round hole at (0, 17) and slot at (0, −17), reamed 3.0; 4 × ⌀3.4 for the thumb screws; M3 insert for the lock screw at (0, 8): 2.0 wall to the liner hole |
| J-003 handle A, B | `J-003_handle_A/B.step/.stl` | nose ⌀6 × 7.5 + grip ⌀16 × 22 | pocket for the tube drilled to tube + 0.03, 20.14 deep, so the tube bears on the shoulder at its end; push-wire hole = tube bore + 0.02 (0.706 / 1.265), drilled through the grip; tube bonded with epoxy, 17.96 protruding below the nose face |
| J-004 sleeve | `J-004_sleeve.step/.stl` | ⌀7 / ⌀5 × 7.8, bore 3.2 | stepped: the shoulder carries the finger 0.1 above the bushing head; clamped by the lock screw |
| J-005 finger | `J-005_finger.step/.stl` | 2.5 thick, arm 5 wide | runs on the sleeve (hole 5.2); tip 3.4 from the punch axis: covers the bushing head rim by 0.57 when swung over it; clear of the head when turned 90° either way |
| Assembly | `J-000_assembly.step` | | stroke 2: outside punch at its stop |
| Slip bushings (fit checks) | `slip_bushing_A_hole.step`, `slip_bushing_B_outside.step` | | as ordered (head recesses not modelled) |

Renders: `assembly_iso.png`, `assembly_exploded.png`, `section.png`, `section_detail.png`,
`head_plate_underside.png`, `base_top.png`, `handle_B_section.png`. Check results: `check_results.json`.

### 2.2 The numbers that matter

| Quantity | Value | Source |
|---|---|---|
| Punch tube OD, A / B | 0.889 / 1.651 mm (0.035 / 0.065 in) | [J-src 1, 2; V]; tolerance and straightness UNVERIFIED: measure |
| Cutting edge, A / B | 0.762 / 1.397 mm | same |
| Tube bore, A / B | 0.686 / 1.245 mm | same |
| Tube length | 38.1 mm: 17.96 below the nose, 20.14 in the handle | same; Derived |
| Slip bushing bores to order | measured tube + 0.0002 in; on nominal .0352 in and .0652 in | CHOICE [R1-7]; SF-12 bore range .0135–.0980 in, tolerance +0.0001/+0.0004 in [V] |
| Bushing–tube play | 0.0003–0.0006 in (8–15 µm) diametral, plus the micrometer reading | Derived |
| Liner–bushing play | 2.5–15 µm diametral | [J-src 4; V] |
| Liner bond gap | 0.022–0.044 mm in the 8.00 H7 hole (liner OD 7.970–7.978) | [V]; Derived [R1-2] |
| Foot face above the base | 1.04 (0.79 HDPE + 0.25 FKM) | Derived |
| Tip at the end of the stroke | 0.25 into the backing (0.15–0.35 with the sheet's ±0.05 and a ±0.05 setting) | CHOICE; Derived |

### 2.3 Why a floating, force-set clamp

The first draft set the squeeze of the sheet under the foot with shim strips under the plate (0.05 mm of 0.25). The
build's own check showed the error: a thin rubber layer under a rigid foot is held laterally by friction and behaves
as a bonded disc, stiffness E(1 + 2S²) with a shape factor S ≈ 6–12, so 0.05 mm would need tens of kN. Now the plate
rests only on the strip; four M3 thumb screws, snug (50–400 N each, UNVERIFIED), press it down; the squeeze is at most
about 12 µm and does not depend on the sheet's thickness, and friction (µ ≥ 0.3, UNVERIFIED) holds the strip with at
least 60 N laterally and 250 N·mm against a twist. The four screws surround the foot, so the plate cannot rock about
a line through it [R1-9]. Press the punches straight down; a slight twist is acceptable.

### 2.4 Depth stop

The handle's nose lands on the bushing head. Because the plate rides on the strip, depth into the backing =
protrusion − sheet − liner − head: the backing's thickness cancels; the bushing's length tolerance (UNVERIFIED) is
taken out by setting each handle against its own bushing at assembly (face the nose; check on test punches in a
scrap strip until the cut is complete with the tip 0.2–0.3 into the backing); the sheet's ±0.05 remains. The nose
(⌀6) passes inside the finger's tip (r 3.4) and its grip stays above the lock screw head.

### 2.5 Concentricity

Each stroke adds: play of the slip bushing in the liner (≤ 7.6 µm radial), runout of the bushing bore (5 µm,
UNVERIFIED: Carr Lane states none), play of the tube in its bore (≤ 10 µm radial with the tube measured to
±2.5 µm), runout of the cutting edge to the tube (10 µm, UNVERIFIED). Both strokes are independent; one allowance of
10 µm covers the sheet moving at the swap or the withdrawal [R1-7]. Worst case 0.075 mm radial (above the 0.05 of
"concentric within ⌀0.10"), root-sum-square 0.026. The worst case still leaves a wall of 0.24 mm (functional minimum
0.175, docs/34). The budget is a guide; acceptance is the measurement of real washers (§5). Also UNVERIFIED and not in
the budget: tube straightness over the 17.5 mm guide (ask SYNEO; a bow of 0.0005 in/in uses about 9 µm of the play)
and asymmetric flow of the rubber at the cut.

## 3. Purchased parts

| Item | Part | Qty | Status |
|---|---|---|---|
| Hole punch | SYNEO CR0350275N20R4 (1.500 in, middle edge) | 2 | RFQ (sales@syneoco.com); not in SYNEO's standard kits [V] |
| Outside punch | SYNEO, edge 0.055 in, **inside edge** (custom C-Series; bore = 0.055 in) — or CR0650495N16R4 (catalogue, middle edge) | 2 | RFQ; ask OD and edge tolerance, straightness, price [V] |
| Slip bushings | Carr Lane SF-12-8-<bore>-NCB, bores = measured tubes + 0.0002 in | 1 each (A, B) | about US$25 each (SF-12-10 example) [V] |
| Liner | Carr Lane L-20-8 | 1 | US$13.68 [V] |
| Membrane punch | Rapid-Core 1.5, Ted Pella 15115-5 (freehand) | 2 | US$6.50 each [V] |
| Dowel pins | McMaster 91595A112, ⌀3 m6 × 12 | 2 | [V] |
| Thumb screws | M3 × 20 knurled, DIN 464 | 4 | length and head height UNVERIFIED (McMaster 92558A330 is M3 × 12) [R1-12] |
| Lock screw | M3 × 14 socket head ISO 4762 + DIN 125 M3 washer | 1 | |
| Heat-set inserts | ruthex RX-M3x5.7 (hole ⌀4.0, wall ≥ 1.6) | 5 | 100 for US$8.23 [V] |
| Backing | McMaster 8619K561, HDPE 0.79 ±0.05 | 1 sheet | [V] |
| Push wires | ⌀0.6 and ⌀1.1 stainless wire or gauge pins, about 60 long, in a pin vise | 1 each | UNVERIFIED part |
| FKM sheet | J-Flex thin-gauge Viton 0.25 ±0.08 | | quote [V]; ±0.08 is wider than the drawing: sort washers by thickness (docs/34 §3.1) |
| Adhesives | gap-filling retaining compound or epoxy for the liner; epoxy for the tubes in the handles | | grade CHOICE of the lab |
| Tools | 8.00 H7 and 3.0 H8 reamers; drills for the pockets (0.92 / 1.68) and push holes (0.70 / 1.25); soldering iron tip for the inserts; tip caps for the punches; microscope with a reticle | | [R1-20] |

## 4. Set-up

* Print all five parts in MJF PA12 (or FDM PETG/ASA, base top and plate underside on the bed). Ream the liner hole to
  8.00 and the pin holes to 3.0; drill the handle pockets and push holes; set the five inserts.
* Bond the liner: plate upside down on a flat plate, liner standing on the flat plate (so it is flush with the foot),
  a ⌀4.76 gauge pin in the liner through a bushing above for squareness; let the adhesive cure.
* Press the pins into the base. Bond each tube into its handle against the pocket's shoulder; check the protrusion
  (17.96) with the bushing in place and a feeler under the nose; face the nose to set the depth (§2.4).
* Put tip caps on the punches when they are not in use: the TiN tips are needle-sharp.

## 5. What to check first

1. Measure the SYNEO tubes: OD to ±2.5 µm with a micrometer at three places; straightness and edge runout on a
   microscope, rolling the tube in a V-block. Order the slip bushings only then.
2. Set each handle's stop on scrap strip (§2.4).
3. Punch ten washers; measure OD, ID, the offset of the hole, flatness and the edges under the microscope. Accept if
   all ten are inside the drawing; otherwise look first at edge runout and at whether the strip moves at the swap.
4. If the 1.397 middle edge leaves a ragged outside or the washer tears in the 1.245 bore, use the inside-edge tube.

## 6. Checks (`check_results.json`, 36, all pass)

Interference between 21 solids, with the liner at its largest OD: none. Both punches at their stops (nose on the
bushing head) clear every part. The finger covers the bushing head when locked and frees it when turned 90° either
way; the nose clears the finger's tip by 0.40. Tip depth 0.15–0.35 of the 0.79 backing. Handle pockets 20.14 deep end
in the grip; the shoulders carry the tube walls (0.09 / 0.19); the push wires pass the bores; both bores in the SF-12
range. Liner bond gap 0.022–0.044. Insert walls: 2.0 to the liner hole, at least 6.0 in the base (ruthex minimum
1.6). Lock screw engagement 5.7, thumb screws 6.5–6.7 (whole insert) at both stack extremes. Concentricity (§2.5).
Punch edges inside the drawing. Clamp: squeeze at most 12 µm at 1600 N; friction at 200 N 60 N and 250 N·mm; the foot
inside the four screws. The plate floats: 0.94 above the base at the thinnest stack; relief 1.64 above the rails; the
strip slides with 1.0 clearance; the foot lies on the strip; the bushing head seats on the liner (0.3 proud). Web
between washers 1.4; pin engagement 4.9; scale ticks on the hole positions.

## 7. Review

| Round | Report | Result | Changes |
|---|---|---|---|
| 1 | `results/tier_round/review_jig_r1.md` | 5 MAJOR, 8 MINOR, 8 NOTE; not converged | Revision B: swing finger instead of a locked washer (R1-1); liner hole 8.00 H7 with a bonding gap, liner modelled at its largest OD, lock insert at a 2.0 wall, PA12 instead of SLA (R1-2); handles with a shoulder for each tube (R1-3); bushing C and the Rapid-Core fallback removed from the jig (R1-4); nose stop on the bushing head (R1-5); inside-edge outside punch first in the RFQ (R1-6); sheet shift in the budget, bore + 0.0002 in, acceptance by measurement (R1-7); plate 0.3 thinner than the liner (R1-8); four screws, force as a range (R1-9); scale on the hole positions (R1-10); checks corrected and added, section from the cut side, 36 checks (R1-11); M3 × 20 screws, insert holes 7.5 deep (R1-12); pin holes reamed (R1-13); notes 14–21 in §2.5, §1, §3, §4 |

## 8. Open questions and choices the user may overrule

* SYNEO price, tolerances and whether an inside-edge 1.40 tube can be made (RFQ).
* Rapid-Core punches as a quick start: not in this jig (cannula too short for the bushing); a separate guide would be
  needed.
* Strip width 14 and pitch 3 (about 30 washers per 100 mm strip).

## 9. Record

2026-11-18: request "Create CAD of the punching jig, loop until convergence. Make sure to also source the
punches." Sourcing by a research agent (`results/tier_round/punch_jig_sourcing.md`); design and CAD in this session;
review rounds by independent agents (`results/tier_round/review_jig_r*.md`).
