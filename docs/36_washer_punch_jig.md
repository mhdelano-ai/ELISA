# 36 — A punching jig for the tier-2 retainer washer

Status: desk work, 2026-11-18, Revision D (after review rounds 1–3, §7). Follow-up to docs/34 (tier-2 flow
cell): the retainer washer T2C-004 (⌀1.40 ±0.10 / ⌀0.75 ±0.10 × 0.25 ±0.05 FKM, hole concentric within ⌀0.10) is
too small for an online gasket cutter; the user asked for a printable jig to punch it in the lab, with the punches
sourced, iterated with an independent reviewer until converged. Nothing is ordered; docs/34 is not changed.
CAD: `cad/elisa_cad/tier2_cell/jig/` (`params.py` single source of dimensions, `parts.py`, `build.py`), outputs in
`cad/out/tier2_cell/punch_jig/` (`python -m elisa_cad.tier2_cell.jig.build` from `cad/`: checks in seconds with
`--fast`, about 7 min with the renders).
Sourcing: `results/tier_round/punch_jig_sourcing.md` (vendor pages read this session; [J-src n] = its item n).
Reviews: `results/tier_round/review_jig_r1.md`, `review_jig_r2.md`, … ([R1-n], [R2-n], … = their findings).
Tags: [V] read on the vendor page this session; [S] search summary only; UNVERIFIED not checked; Derived computed
here; CHOICE design choice of this document.

## 0. Summary

**Two hollow punches on one axis, never moving the sheet in between.** The hole is punched first, then the outside,
through one liner bushing bonded into a printed head plate. Each punch has its own hardened slip bushing whose bore
is ordered to the measured punch tube; the two bushings are exchanged in the liner between the strokes. A ring
finger on a shoulder screw lies over the bushing head and keeps it down while the punch is withdrawn; swung aside, it
frees the bushing. The bushing's own face is flush with the plate's foot, which stands on the FKM strip and is pulled
down by four thumb screws, so friction holds the strip while the bushings are swapped. Each punch tube is bonded into
a handle whose nose lands on the bushing head: the stroke ends 0.25 mm into the backing, every time. Between washers
the screws are loosened and the strip is pushed on by 3 mm.

| | Choice | Why |
|---|---|---|
| Punches | SYNEO C-Series catheter punches, straight 304 SS tubes, TiN: **CR0350275N20R4** (edge 0.76, tube 0.889, middle edge) for the hole; **CR0650495N16R4** (edge 1.397, tube 1.651) for the outside, RFQ asking first for an **inside edge** [J-src 1, 2; V] | the only catalogue punches found at 0.75 and 1.40; straight ground tubes run in a bushing; washer on nominal ⌀1.40 / ⌀0.76 |
| Guidance | Carr Lane slip/fixed renewable bushings **SF-12-8-<bore>-NCB** (bores = measured tube + 0.0002 in; nominal .0352 and .0652 in; RFQ: the two ground to the same under-head length and head thickness) in one liner **L-20-6** [J-src 4; V] | one liner takes bores 0.34–2.49 mm; liner-to-bushing play 2.5–15 µm; the liner one size shorter than the bushing body lets the bushing face reach the foot whatever the lengths [R2-1] |
| Retention | printed ring finger (bears on the whole head rim, r 3.2–4.8) on an ISO 7379-4-M3-10 shoulder screw at 9.5 mm from the axis, pressed onto a faced spacer by an O-ring; 0.05 above the head | works with the head's recesses at any angle and with head tolerances of ±1/64 in [R2-2, R2-3, R2-4, R2-7, R3-5] |
| Depth | handle nose (⌀5) lands on the bushing head; the nose is printed 1.2 long and faced against its own bushing | tip 0.12–0.38 into the 0.79 backing [R1-5, R2-5] |
| Clamp | force-set: plate floats on the strip, foot ⌀11 around the bushing body, 4 × M3 thumb screws | a 0.25 mm rubber sheet under a rigid foot is nearly incompressible; a shim-set squeeze would need tens of kN |
| Printed parts | J-001 base, J-002 head plate, J-003 handles (one per tube), J-004 spacer, J-005 ring finger: **MJF PA12** (or FDM PETG/ASA); not SLA, the inserts are heat-set | the steel parts carry every precise function; reamed, drilled and faced where it matters |
| Membrane disc ⌀1.5 | freehand with a Rapid-Core 1.5 (Ted Pella 15115-5, US$6.50) on the backing, not in the jig | the disc needs no concentricity, and the Rapid-Core cannula is too short for a bushing [R1-4] |

Model checks: 44, all pass (§6), with the bushing tolerances of ±1/64 in (body length, head diameter, head thickness;
amesweb, as read by the round-2 reviewer; Carr Lane states none) at their extremes where they matter. Hole-to-outside
offset 0.030 mm root-sum-square, worst case 0.086 (both strokes plus 0.010 for the sheet moving at the swap)
against 0.05 for the drawing; the punch edge runout (0.010 assumed) and the sheet shift are UNVERIFIED, so acceptance
rests on measured washers (§5).
**Order of work:** quote and buy the two SYNEO tubes, measure them, then order the slip bushings and the liner; print,
ream, drill, assemble, set the finger and the stops, punch ten washers and measure them (§4, §5).

## 1. What the jig does

1. **Load.** Cut a strip 14 × 100 mm from the 0.25 mm FKM sheet and one from 0.79 mm HDPE (the backing the punch
   ends in). Tape the FKM to the backing at its leading end, so the two are fed together and each stroke lands on fresh
   backing [R2-10]. Lay the pair between the rails of the base, under the raised head plate, with the leading end on the
   tick at x = 21 (the first washer is then 21 mm from the end; the ticks sit on the hole positions downstream) [R2-14].
2. **Clamp.** Turn the four thumb screws until snug (finger tight, no more): the foot and the bushing face press the
   strip around the punch axis.
3. **Stroke 1 (hole).** Bushing A (marked) in the liner, finger swung over its head. Push the 0.76 punch (handle A)
   straight down through the bushing until the nose lands on the bushing head. Withdraw.
4. **Swap.** Swing the finger aside until it stops on a thumb-screw head (about 75°; the bushing is free from 60°),
   lift bushing A out with flat tweezers into its parking hole on the base, drop
   bushing B in (any angle), swing the finger back. The strip has not moved: the foot holds it and nothing touched it.
5. **Stroke 2 (outside).** Push the 1.397 punch (handle B) through bushing B to its stop. With the catalogue middle
   edge the washer is now inside the tube, squeezed into its 1.245 bore (an inside-edge tube would not squeeze it).
   Withdraw.
6. **Eject.** Push the washer out of the tube with the ⌀1.1 wire through the handle, into a dish of water or onto a
   clean card; the hole slug may come with it (sort under the microscope). Clear the 0.76 punch with the ⌀0.6 wire
   every few holes.
7. **Feed.** Loosen the thumb screws half a turn, push the strip pair on by 3 mm, retighten, bushing A back in, repeat.
   About 25 washers per strip. Blow out the liner with each strip (FKM debris in a 2.5 µm fit can make a bushing stick).

Membrane discs (⌀1.5): Rapid-Core 1.5 pressed freehand through the membrane on a piece of the backing.

## 2. Design

### 2.1 Parts (STEP and STL in `cad/out/tier2_cell/punch_jig/`)

| Part | File | Size (mm) | Features |
|---|---|---|---|
| J-001 base | `J-001_base.step/.stl` | 80 × 48 × 10 | flat top = datum; two rails 1.5 × 0.30 high, 14.6 apart, guide the strip; 2 × ⌀3 holes at (0, ±17) for pressed pins (print 2.8, ream 2.95, press; or bond); 4 × M3 heat-set inserts at (±15, ±16), hole ⌀4.0 × 7.5 deep; 2 parking bosses ⌀10 × 4.5 at (−32, ±14) with ⌀5.3 holes 13.2 deep, so the idle bushing hangs on its head and its ground face touches nothing [R3-10]; pitch scale ticks at x = 21, 24 … 39 |
| J-002 head plate | `J-002_head_plate.step/.stl` | 40 × 40 × 11.9 | liner hole printed 7.8, reamed **8.00 H7** with a chucking reamer (short 45° lead) on a drill press, depth set from the foot face: ledge 1.78 ±0.1 above it [R3-3]; below it ⌀5.2 drilled in the same set-up, for the bushing body; foot ⌀11; relief 20 wide × 1.0 deep over the strip except the foot; round hole at (0, 17) and slot at (0, −17) reamed 3.0 and lapped to a slide fit (3.02–3.04); 4 × ⌀3.4 for the thumb screws; M3 insert for the shoulder screw at (0, 9.5): 3.5 wall to the liner hole |
| J-003 handle A, B | `J-003_handle_A/B.step/.stl` (as printed) | nose ⌀5 × 10 (printed 11.2) + grip ⌀16 × 22 | pocket for the tube drilled (drill press or lathe, from a printed pilot) to tube + 0.03, 20.14 deep from the faced nose, so the tube is located by the shoulder at its end; push-wire hole = tube bore + 0.02 (0.706 / 1.265) through the grip; tube bonded with epoxy (a waxed wire through tube and push hole while it cures); 17.96 protruding below the faced nose |
| J-004 spacer | `J-004_spacer.step/.stl` (as printed) | ⌀8 / ⌀4.1 × 6.81 printed, faced to about 5.61 | under the finger on the shoulder; faced at assembly so that the finger lies 0.05 above the thicker bushing head |
| J-005 ring finger | `J-005_finger.step/.stl` | 2.5 thick; boss ⌀8, hole reamed 4 H8; arm 5 wide; ring r 3.2–4.8 | the ring lies over the bushing head and bears on its whole rim (head r 3.57–4.37 over ±1/64 in); 0.3 lead-in chamfer under the ring's outer edge (modelled); the bushing lifts out from a swing of 60°; the finger stops on a thumb-screw head near 75° (with DIN 464 heads; with low heads it swings further, also free) [R3-4] |
| Assembly | `J-000_assembly.step` | | stroke 2: outside punch at its stop |
| Slip bushings (fit checks) | `slip_bushing_A_hole.step`, `slip_bushing_B_outside.step` | | as ordered (head recesses not modelled; the ring does not depend on them) |

Renders: `assembly_iso.png`, `assembly_exploded.png`, `section.png`, `section_detail.png`,
`head_plate_underside.png`, `base_top.png`, `handle_B_section.png`. Check results: `check_results.json`.

### 2.2 The numbers that matter

| Quantity | Value | Source |
|---|---|---|
| Punch tube OD, A / B | 0.889 / 1.651 mm (0.035 / 0.065 in) | [J-src 1, 2; V]; tolerance and straightness UNVERIFIED: measure |
| Cutting edge, A / B | 0.762 / 1.397 mm | same |
| Tube bore, A / B | 0.686 / 1.245 mm | same |
| Tube length | 38.1 mm: 17.96 below the faced nose, 20.14 in the handle | same; Derived |
| Slip bushing bores to order | measured tube + 0.0002 in; on nominal .0352 in and .0652 in | CHOICE [R1-7]; SF-12 bore range .0135–.0980 in, tolerance +0.0001/+0.0004 in [V] |
| Bushing body length, head ⌀ and thickness | 1/2, 5/16, 3/16 in, each ±1/64 in | amesweb SF table (round-2 reviewer) [R2-9]; Carr Lane states none |
| Bushing–tube play | 0.0003–0.0006 in (8–15 µm) diametral, plus the micrometer reading | Derived |
| Liner–bushing play | 2.5–15 µm diametral; the bushing face is 3.18 below the liner (overhang): up to 12.7 µm radial at the face | [J-src 4; V]; Derived |
| Liner bond gap | 0.022–0.044 mm in the 8.00 H7 hole (liner OD 7.970–7.978) | [V]; Derived |
| Liner top (bushing seat) above the plate top | 0.8 nominal, 0.2–1.4 | Derived |
| Bushing head top above the plate top | 5.56 nominal, 4.57–6.56 (body, head, plate print) | Derived |
| Foot face above the base | 1.04 (0.79 HDPE + 0.25 FKM) | Derived |
| Tip at the end of the stroke | 0.25 into the backing (0.12–0.38 with the stock sheet's ±0.08 and a ±0.05 setting) | CHOICE; Derived [R3-8] |
| Nose facing at assembly | 1.2 nominal, 0.11–2.29 (always some) | Derived |

### 2.3 Why a floating, force-set clamp

The first draft set the squeeze of the sheet under the foot with shim strips under the plate (0.05 mm of 0.25). The
build's own check showed the error: a thin rubber layer under a rigid foot is held laterally by friction and behaves
as a bonded disc, stiffness E(1 + 2S²) with a shape factor S ≈ 6–12, so 0.05 mm would need tens of kN. Now the plate
rests only on the strip; four M3 thumb screws, snug (50–400 N each, UNVERIFIED), press it down; the squeeze is at
most about 12 µm and does not depend on the sheet's thickness, and friction (µ ≥ 0.3, UNVERIFIED) holds the strip
with at least 60 N laterally and 250 N·mm against a twist. The four screws surround the foot, so the plate cannot
rock about a line through it. The plate's pin holes are a slide fit, so the plate does not hang on the pins [R2-8].
Press the punches straight down; a slight twist is acceptable.

### 2.4 Bushing face, seat and finger (Revisions C, D)

With a bushing body tolerance of ±1/64 in, a liner flush with the foot would leave the bushing face up to 0.4 mm
proud of or recessed from the foot, differently for A and B [R2-1]. So the liner (L-20-6, 3/8 in) is one size
shorter than the bushing body (1/2 in) and is bonded in a position set by the bushing itself; the bushing body passes
through the printed foot ring (⌀5.2), which presses the sheet from r 2.6 outwards, and the bushing face is flush with
the foot. The liner floats 1.4 above its ledge for this (0.41 at the worst stack with the ledge's ±0.2).

**Bonding (inverted, two flats)** [R3-1, R3-2]. The bushing used as the locator must not be glued in: its fit in the
liner is 1.3–7.6 µm radial, and an anaerobic retaining compound would wick into it.
1. Use a thixotropic (paste) epoxy, not an anaerobic compound (which also cures poorly on PA12).
2. Coat the locator bushing (the longer one) on its body and under its head with mould release (PTFE dry film or
   paste wax), wiped to a film.
3. Flat 1 (glass plate or gauge block, PTFE film on it): stand the bushing on it head down. Put a thin band of epoxy
   on the middle third of the liner's outside only (none near either end) and slide the liner over the body: it rests
   on the head.
4. Lower the plate over the liner, foot up. Lay flat 2 (PTFE film) across the foot and the bushing face, raise the
   plate on shims until its foot touches flat 2, and weight flat 2. The liner's weight keeps it on the head; flat 2
   makes the foot and the bushing face coplanar.
5. Turn the bushing a few degrees every few minutes until the epoxy gels (this changes neither its seat nor its
   axis); then lift it out, clean it, and put it back until the epoxy has cured.
6. After curing: both bushings drop in and turn freely; each face is flush with the foot (straightedge and a 0.02
   feeler).

The other bushing's face is recessed by the difference of their under-head lengths: order the two matched (RFQ:
within 0.001 in). Lap the longer one only for differences up to 0.05 (check squareness with blue on a flat plate);
anything more goes to a surface grinder (spin fixture or V-block, face square to the body within 0.01) [R3-6].

**Finger.** Its height is set once at assembly: the spacer J-004 is printed 1.2 high and faced (abrasive paper on a
flat plate) until a 0.05 feeler passes under the ring over the thicker head. An NBR O-ring 4 × 1 above the finger,
under DIN 988 shim rings that fill up to the shoulder-screw head, presses the finger onto the spacer: no axial play,
and the finger turns with light friction [R3-5]. The bushing can then rise only by the gap (0.05) and the bending of
the printed arm on withdrawal; with unmatched head thicknesses the thinner head could rise up to 0.8 more, which is a
second reason for the matched order. The ring bears on the whole rim between r 3.2 and the head's edge, so the head's
lock and slip recesses can lie anywhere [R2-3]; the boss stays 1.0 from a head of the largest diameter when swung,
with the finger moved 0.1 toward the axis [R2-4]. Tighten the shoulder screw lightly (about 0.3–0.5 N·m): its
shoulder bears on the brass insert [R3-7].

### 2.5 Depth stop

The handle's nose lands on the bushing head. Because the plate rides on the strip, depth into the backing =
protrusion − sheet − (body + head): the backing's thickness cancels. The nose is printed 1.2 long and faced against
its own bushing (the handle's tube running in that bushing in the jig keeps the face square [R3-9]) until test punches in a scrap strip cut through with the tip 0.2–0.3 into the backing (feeler under
the nose, then a punch; abrasive paper on a flat plate with a ⌀3 clearance hole for the tube). The facing needed is
0.11–2.29 mm over the tolerances (head top, pocket depth ±0.2, tube length), so it never has to add material [R2-5].
Mark handle A with bushing A and handle B with bushing B: the depth is set per pair. The stock sheet's ±0.08 remains:
tip 0.12–0.38 into the 0.79 backing.

### 2.6 Concentricity

Each stroke adds: the bushing's play in the liner, which with the 3.18 mm overhang below the liner gives up to
12.7 µm radial at the face; runout of the bushing bore (5 µm, UNVERIFIED: Carr Lane states none); play of the tube in
its bore (≤ 10 µm radial with the tube measured to ±2.5 µm); runout of the cutting edge to the tube (10 µm,
UNVERIFIED). Both strokes are independent; one allowance of 10 µm covers the sheet moving at the swap or the
withdrawal. Worst case 0.086 mm radial (above the 0.05 of "concentric within ⌀0.10"), root-sum-square 0.030. The worst
case still leaves a wall of 0.23 mm (functional minimum 0.175, docs/34). The budget is a guide; acceptance is the
measurement of real washers (§5). Also UNVERIFIED and not in the budget: tube straightness over the 17.5 mm guide
(ask SYNEO; a bow of 0.0005 in/in uses about 9 µm of the play) and asymmetric flow of the rubber at the cut.

## 3. Purchased parts

| Item | Part | Qty | Status |
|---|---|---|---|
| Hole punch | SYNEO CR0350275N20R4 (1.500 in, middle edge) | 2 | RFQ (sales@syneoco.com); not in SYNEO's standard kits [V] |
| Outside punch | SYNEO, edge 0.055 in, **inside edge** (custom C-Series; bore = 0.055 in) — or CR0650495N16R4 (catalogue, middle edge) | 2 | RFQ; ask OD and edge tolerance, straightness, price [V] |
| Slip bushings | Carr Lane SF-12-8-<bore>-NCB, bores = measured tubes + 0.0002 in; RFQ: matched under-head length and head thickness within 0.001 in, and the head drawing | 1 each (A, B) | about US$25 each (SF-12-10 example) [V] |
| Liner | Carr Lane L-20-6 (3/8 in) | 1 | US$13.01 [V] |
| Shoulder screw | ISO 7379-4-M3-10 (Ganter GN 35215 or equivalent; 4-M3 is a maker's extension of the ISO sheet): head ⌀7 × 3, thread 7, shoulder 10 +0.25 | 1 | per the round-3 reviewer's reading of the Ganter/Elesa sheet [R3-7] |
| Shim rings, O-ring | DIN 988 4 × 8, 0.1 / 0.2 / 0.5 / 1.0; NBR O-ring 4 × 1 | assortment; 2 | |
| Membrane punch | Rapid-Core 1.5, Ted Pella 15115-5 (freehand) | 2 | US$6.50 each [V] |
| Dowel pins | McMaster 91595A112, ⌀3 m6 × 12 | 2 | [V] |
| Thumb screws | M3 × 20 knurled, DIN 464 | 4 | length and head height UNVERIFIED (McMaster 92558A330 is M3 × 12) |
| Heat-set inserts | ruthex RX-M3x5.7 (hole ⌀4.0, wall ≥ 1.6) | 5 | 100 for US$8.23 [V] |
| Backing | McMaster 8619K561, HDPE 0.79 ±0.05 | 1 sheet | [V] |
| Push wires | ⌀0.6 and ⌀1.1 stainless wire or gauge pins, about 60 long, in a pin vise | 1 each | UNVERIFIED part |
| FKM sheet | J-Flex thin-gauge Viton 0.25 ±0.08 | | quote [V]; ±0.08 is wider than the drawing: sort washers by thickness (docs/34 §3.1) |
| Adhesives and film | thixotropic (paste) epoxy for the liner and the tubes (not an anaerobic retaining compound); mould release (PTFE dry film or paste wax); PTFE release film | | grade CHOICE of the lab [R3-1] |
| Tools | 8.00 H7 chucking reamer (short lead), 4.0 H8, 3.0 and 2.95 reamers; two flat plates (glass or gauge blocks); drill press with a depth stop, or lathe and drills for the pockets (0.92 / 1.68), push holes (0.70 / 1.25) and the body hole (5.2); soldering iron tip for the inserts; feeler gauges; micrometer; flat plate and abrasive paper; flat tweezers; tip caps; microscope with a reticle; marking for A/B | | [R1-20, R2-12] |

## 4. Set-up

* Print all five parts in MJF PA12 (or FDM PETG/ASA, base top and plate underside on the bed). Ream the liner hole to
  8.00 with the chucking reamer on a drill press (depth from the foot face, ledge 1.78 ±0.1) and drill the ⌀5.2 body
  hole without unclamping; ream the finger hole to 4.0, the plate's pin holes to 3.0 (lap to a slide fit) and the base's to 2.95; drill the
  body hole 5.2, the handle pockets and push holes from their pilots on a drill press or lathe; set the five inserts
  and face the plate's insert flush.
* Measure both bushings' under-head lengths and heads; if they differ by more than 0.02 (unless ordered matched), lap
  (≤ 0.05) or grind the longer face (§2.4). Bond the liner with the longer bushing as its locator, released and turned
  while the epoxy gels (§2.4).
* Press (or bond) the pins into the base. Fit the shoulder screw with the spacer and the finger; face the spacer until a 0.05 feeler passes under the ring over the thicker head;
  O-ring and shim rings above the finger until it is pressed lightly onto the spacer and still turns by hand (§2.4).
* Bond each tube into its handle against the pocket's shoulder (waxed wire through it while the epoxy cures); face
  the nose against its own bushing until the depth is right (§2.5). Mark the bushings and handles A and B.
* Put tip caps on the punches when they are not in use: the TiN tips are needle-sharp.

## 5. What to check first

1. Measure the SYNEO tubes: OD to ±2.5 µm with a micrometer at three places; straightness and edge runout on a
   microscope, rolling the tube in a V-block. Order the slip bushings only then.
2. Set the finger and each handle's stop (§2.4, §2.5).
3. Punch ten washers; measure OD, ID, the offset of the hole, flatness and the edges under the microscope. Accept if
   all ten are inside the drawing; otherwise look first at edge runout, at the bushing faces and at whether the strip
   moves at the swap.
4. If the 1.397 middle edge leaves a ragged outside or the washer tears in the 1.245 bore, use the inside-edge tube.

## 6. Checks (`check_results.json`, 44, all pass)

Interference between 21 solids, with the liner at its largest OD: none. Both punches at their stops clear every
part. The ring bears on the whole head rim for head diameters 7.14–8.73 (±1/64 in); swung 60–74° either way, with
the finger moved 0.1 toward the axis, it lets a head of the largest diameter lift out (boss 1.03 away); at its stop
(74°) it touches no part; at 90° it would meet a thumb-screw head, so it stops before (information); the nose passes
inside the ring with 0.6 radial. The spacer can be faced for the whole head-top range (4.57–6.56 above the plate) and
the shoulder (10 +0.25) leaves room for finger, O-ring and shims. The bushing head seats on the liner (0.2–1.4 above
the plate). The liner floats above its ledge at bonding (0.41 at the worst stack with the ledge's ±0.2). Bushing face
flush with the foot: a procedure item, checked after cure. Tip depth 0.12–0.38 of the 0.79 backing with the stock
sheet's ±0.08; the nose is always faced (0.11–2.29) and keeps ≥ 5 mm; the grip clears the shoulder-screw head. Handle
pockets 20.14 deep end in the grip; the shoulders locate the tubes; the push wires pass the bores; both bores in the
SF-12 range. Liner bond gap 0.022–0.044. Insert walls: 3.5 to the liner hole, at least 6.0 in the base; shoulder-screw
thread 7 in its 7.5 hole; thumb screws 6.9–7.2 at both stack extremes; parking bosses clear. Concentricity (§2.6).
Punch edges inside the drawing. Clamp: squeeze at most 12 µm at 1600 N; friction at 200 N 60 N and 250 N·mm; the
foot inside the four screws. The plate floats (0.91 above the base at the thinnest stack), the relief clears the
rails and the strip, the foot lies on the strip and presses it from the bushing body outwards. Web between washers
1.4; pins engage, plate slide fit, base press fit; scale ticks on the hole positions.

## 7. Review

| Round | Report | Result | Changes |
|---|---|---|---|
| 1 | `results/tier_round/review_jig_r1.md` | 5 MAJOR, 8 MINOR, 8 NOTE; not converged | Revision B: swing finger instead of a locked washer (R1-1); liner hole 8.00 H7 with a bonding gap, liner at its largest OD, lock insert at a 2.0 wall, PA12 instead of SLA (R1-2); handles with a shoulder for each tube (R1-3); bushing C and the Rapid-Core fallback removed from the jig (R1-4); nose stop on the bushing head (R1-5); inside-edge outside punch first in the RFQ (R1-6); sheet shift in the budget, bore + 0.0002 in, acceptance by measurement (R1-7); plate thinner than the liner (R1-8); four screws, force as a range (R1-9); scale on the hole positions (R1-10); checks corrected, section from the cut side (R1-11); M3 × 20 screws (R1-12); pin holes reamed (R1-13); notes 14–21 |
| 2 | `results/tier_round/review_jig_r2.md` | 4 MAJOR, 5 MINOR, 5 NOTE; R1-1, R1-13 partly resolved; not converged | Revision C: bushing tolerances ±1/64 in in the model and the checks (R2-9); liner L-20-6 bonded with the longer bushing's face flush with the foot, faces matched or lapped (R2-1); finger height set by a faced spacer and shim rings, lead-in chamfer (R2-2); ring finger on the whole rim, recesses anywhere (R2-3); pivot at 9.5, boss 1.0 from the largest head with the play (R2-4); nose printed 1.2 long and faced, facing method (R2-5); pockets drilled from pilots, bond carries the load, waxed wire (R2-6); ISO 7379 shoulder screw, finger reamed 4 H8, shims for the play (R2-7); plate pin holes a slide fit, base press (R2-8); tolerance cases in the checks, 42 checks (R2-9); backing taped to the FKM and fed with it (R2-10); renders re-run (R2-11); BOM, parking holes, A/B marks, PTFE film (R2-12); scale start (R2-14); debris, tweezers (R2-15) |
| 3 | `results/tier_round/review_jig_r3.md` | 1 MAJOR, 5 MINOR, 4 NOTE; round 2 resolved except the stale renders; not converged | Revision D: liner bonding with paste epoxy on the middle third, released locator turned while it gels (R3-1); inverted two-flat bonding set-up (R3-2); chucking reamer, ledge from the foot face, LEDGE_GAP 1.4 with the print tolerance in the check (R3-3); finger swing checked over 60–74° and at its stop on the thumb head (R3-4); O-ring preload, gap 0.05, rise stated (R3-5); lap ≤ 0.05 else grind (R3-6); Ganter GN 35215 head 7 × 3, thread 7, light torque, finger 2.5 thick (R3-7); face-flush check labelled a procedure, stock sheet ±0.08 in the checks, ring chamfer modelled (R3-8); nose faced in its own bushing (R3-9); parking bosses (R3-10); detail render cropped to its window and all renders regenerated (R2-11) |

## 8. Open questions and choices the user may overrule

* SYNEO price, tolerances and whether an inside-edge 1.40 tube can be made (RFQ).
* Carr Lane: real tolerances on body length and head, the head drawing, and matched grinding of the two bushings.
* Rapid-Core punches as a quick start: not in this jig (cannula too short for the bushing); a separate guide would be
  needed.
* Strip width 14 and pitch 3 (about 25 washers per 100 mm strip).

## 9. Record

2026-11-18: request "Create CAD of the punching jig, loop until convergence. Make sure to also source the
punches." Sourcing by a research agent (`results/tier_round/punch_jig_sourcing.md`); design and CAD in this session;
review rounds by independent agents (`results/tier_round/review_jig_r*.md`).
