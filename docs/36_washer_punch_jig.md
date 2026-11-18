# 36 — A punching jig for the tier-2 retainer washer

Status: desk work, 2026-11-18, Revision A (before review). Follow-up to docs/34 (tier-2 flow cell): the retainer
washer T2C-004 (⌀1.40 ±0.10 / ⌀0.75 ±0.10 × 0.25 ±0.05 FKM, hole concentric within ⌀0.10) is too small for an
online gasket cutter; the user asked for a printable jig to punch it in the lab, with the punches sourced, iterated
with an independent reviewer until converged. Nothing is ordered; docs/34 is not changed.
CAD: `cad/elisa_cad/tier2_cell/jig/` (`params.py` single source of dimensions, `parts.py`, `build.py`), outputs in
`cad/out/tier2_cell/punch_jig/` (`python -m elisa_cad.tier2_cell.jig.build` from `cad/`, under 1 min with `--fast`).
Sourcing: `results/tier_round/punch_jig_sourcing.md` (vendor pages read this session; [J-src n] = its item n).
Tags: [V] read on the vendor page this session; [S] search summary only; UNVERIFIED not checked; Derived computed
here; CHOICE design choice of this document.

## 0. Summary

**Two hollow punches on one axis, never moving the sheet in between.** The hole is punched first, then the outside,
through one liner bushing bonded into a printed head plate; each punch has its own hardened slip bushing whose bore
is ordered to the measured punch tube, and the two slip bushings are exchanged in the liner between the strokes.
The head plate stands on the FKM strip with a small foot around the liner and is pulled down by two thumb screws,
so friction holds the strip while the bushings are swapped. Between washers the screws are loosened a turn and the
strip is pushed on by 3 mm (a scale on the base).

| | Choice | Why |
|---|---|---|
| Punches | SYNEO C-Series catheter punches, straight 304 SS tubes, TiN, middle edge: **CR0350275N20R4** (edge 0.76, tube 0.889) for the hole, **CR0650495N16R4** (edge 1.397, tube 1.651) for the outside [J-src 1, 2; V] | the only catalogue punches found at 0.75 and 1.40; straight ground tubes run in a bushing; washer on nominal ⌀1.40 / ⌀0.76 |
| Guidance | Carr Lane slip/fixed renewable bushings **SF-12-8-.0353-NCB** and **SF-12-8-.0653-NCB** (bores to be re-set to the measured tubes), liner **L-20-8** [J-src 4; V] | one liner takes bores 0.34–2.49 mm; liner-to-bushing play 2.5–15 µm; -NCB guides the tube over the full 12.7 mm |
| Printed parts | J-001 base, J-002 head plate, J-003 handles (one per SYNEO tube), J-004 lock spacer | resin (SLA) or MJF PA12; the steel parts carry every precise function |
| Clamp | force-set: the plate floats on the strip, foot ⌀10.9 around the liner, 2 × M3 thumb screws | a 0.25 mm rubber sheet under a wide rigid foot is nearly incompressible (shape factor 9): a shim-set squeeze, the first design, would have needed tens of kN |
| Fallback punches, off the shelf | Rapid-Core 0.75 (Ted Pella 15115-2, tube 1.07) and 1.5 (15115-5, tube 1.90), US$6.50 each [V] | washer ⌀1.50 / ⌀0.77: at the drawing's upper OD limit; exposed cannula length unknown |
| Membrane disc ⌀1.5 | Rapid-Core 1.5 in a third slip bushing (.0751 in) | the disc is the core; the ejector pushes it out |

Model checks: 33 pass (§6), among them a hole-to-outside offset of 0.025 mm (root-sum-square of both strokes;
worst case 0.068) against the drawing's 0.05, with the punch edge runout UNVERIFIED (0.010 assumed).
**Order of work:** quote and buy the two SYNEO tubes, measure them, then order the slip bushings with bores =
measured tube + 0.0003 in; print, assemble, punch ten washers and measure them (§5).

## 1. What the jig does

1. **Load.** Cut a strip 14 × 100 mm from the 0.25 mm FKM sheet and one from 0.79 mm HDPE (the backing the punch
   ends in). Lay the backing, then the FKM, between the rails of the base, under the raised head plate.
2. **Clamp.** Turn the two thumb screws finger tight: the plate's foot presses the strip around the punch axis.
3. **Stroke 1 (hole).** Slip bushing A in the liner, lock screw down. Push the 0.76 punch (in its handle J-003)
   through the bushing until it stops in the backing (0.15 mm in; felt as the end of the cut). Withdraw.
4. **Swap.** Lift the lock screw washer a quarter turn, pull bushing A, insert bushing B, lock. The strip has not
   moved: the foot holds it and nothing touched it.
5. **Stroke 2 (outside).** Push the 1.397 punch through bushing B to the backing. The washer is now inside the tube
   (its bore is 1.245; the washer is squeezed in). Withdraw.
6. **Eject.** Push the washer out of the tube with a ⌀1.1 wire through the handle into a dish of water or onto a
   clean card; clear the 0.76 punch with a ⌀0.6 wire every few holes.
7. **Feed.** Loosen the thumb screws a turn, push the strip on by 3 mm (scale beside the rail), bushing A back in,
   repeat. About 30 washers per strip; replace the backing strip with each FKM strip.

Membrane discs (⌀1.5): bushing C, the Rapid-Core 1.5, one stroke, membrane on the backing alone.

## 2. Design

### 2.1 Parts (STEP and STL in `cad/out/tier2_cell/punch_jig/`)

| Part | File | Size (mm) | Features |
|---|---|---|---|
| J-001 base (printed) | `J-001_base.step/.stl` | 80 × 48 × 10 | flat top = datum; two rails 1.5 × 0.30 high, 14.6 apart, guide the strip; 2 × ⌀3 holes for pressed pins (print 2.9, ream 3.0); 2 × M3 heat-set inserts (hole ⌀4.0, ruthex RX-M3x5.7); pitch scale (ticks every 3 mm, long tick every 15) from x = 22 to 38 |
| J-002 head plate (printed) | `J-002_head_plate.step/.stl` | 40 × 40 × 12.7 | liner hole ⌀7.95 (ream 7.95–7.96, liner bonded with retaining compound); foot ⌀10.9 (1.5 mm printed ring around the liner, flush with the liner end); underside relief 20 wide × 1.0 deep over the strip except the foot; round hole ⌀3.05 at one pin, slot along the pin line at the other; 2 × ⌀3.4 for the thumb screws; M3 insert for the lock screw at 6.75 mm from the axis |
| J-003 handle (printed, × 2) | `J-003_handle_A/B.step/.stl` | ⌀10 × 30 | blind bore 10 deep for the SYNEO tube (tube + 0.05, bonded); ⌀1.4 through hole on the axis for the push wire |
| J-004 lock spacer (printed) | `J-004_lock_spacer.step/.stl` | ⌀5.4 / ⌀3.4 × 4.76 | under the lock screw's washer, so that the washer bears on the bushing head |
| Assembly | `J-000_assembly.step` | | stroke 2: outside punch at the bottom of its stroke |
| Slip bushings (for fit checks) | `slip_bushing_A_hole.step`, `_B_outside.step`, `_C_membrane.step` | | as ordered |

Renders: `assembly_iso.png`, `assembly_exploded.png`, `section.png`, `section_detail.png`,
`head_plate_underside.png`, `base_top.png`. Check results: `check_results.json`.

### 2.2 The numbers that matter

| Quantity | Value | Source |
|---|---|---|
| Punch tube OD, A / B | 0.889 / 1.651 mm (0.035 / 0.065 in) | [J-src 1, 2; V]; tolerance UNVERIFIED: measure |
| Cutting edge, A / B | 0.762 / 1.397 mm | same |
| Tube bore, A / B | 0.686 / 1.245 mm | same |
| Tube length | 38.1 mm; 28.1 exposed after 10 mm in the handle; 20.9 needed (§6) | same; Derived |
| Slip bushing bores to order | measured tube + 0.0003 in; on nominal .0353 in and .0653 in (C: .0751 in) | CHOICE; SF-12 bore range .0135–.0980 in, tolerance +0.0001/+0.0004 in [V] |
| Bushing–tube play | 0.0004–0.0007 in (10–18 µm) diametral | Derived |
| Liner–bushing play | 2.5–15 µm diametral | [J-src 4; V] |
| Foot face above the base | 1.04 (0.79 HDPE + 0.25 FKM) | Derived |
| Tip at the bottom of the stroke | 0.15 into the backing | CHOICE |

### 2.3 Why a floating, force-set clamp

The first version set the squeeze of the sheet under the foot with shim strips under the plate's lands (0.05 mm of
0.25). The build's own check showed the error: a thin rubber layer under a rigid foot is held laterally by friction
and behaves as a bonded disc, stiffness E(1 + 2S²) with a shape factor S ≈ 9–12, so 0.05 mm would need about
50 kN. Now the plate rests only on the strip; two M3 thumb screws, finger tight (about 50 N each, UNVERIFIED), press
it down; the squeeze is a fraction of a micrometre and does not depend on the sheet's thickness, and friction
(µ ≥ 0.3, UNVERIFIED) holds the strip with 30 N laterally and 110 N·mm against a twist. The punches are pressed
straight down, with at most a slight twist.

### 2.4 Concentricity

Each stroke adds: play of the slip bushing in the liner (≤ 7.5 µm radial), runout of the bushing bore (5 µm,
UNVERIFIED: Carr Lane states none), play of the tube in its bore (≤ 11 µm radial with the tube measured to
±2.5 µm), runout of the cutting edge to the tube (10 µm, UNVERIFIED). Both strokes are independent: worst case
0.068 mm radial, root-sum-square 0.025, against 0.05 for "concentric within ⌀0.10". The worst case still leaves a
wall of 0.25 mm (functional minimum 0.175, docs/34). The edge runout is the one number that can spoil it; measure it
on the tubes before ordering bushings (§5).

## 3. Purchased parts

| Item | Part | Qty | Status |
|---|---|---|---|
| Hole punch | SYNEO CR0350275N20R4 (1.500 in) | 2 | RFQ (sales@syneoco.com); not in SYNEO's standard kits [V] |
| Outside punch | SYNEO CR0650495N16R4 (1.500 in) | 2 | RFQ; ask for an inside-edge variant (the washer would not be squeezed into the bore) and the OD and edge tolerances |
| Membrane punch | Rapid-Core 1.5, Ted Pella 15115-5 | 2 | US$6.50 each [V] |
| Slip bushings | Carr Lane SF-12-8-<bore>-NCB, bores from the measured tubes (A, B; C .0751) | 1 each | about US$25 each (SF-12-10 example) [V] |
| Liner | Carr Lane L-20-8 | 1 | US$13.68 [V] |
| Dowel pins | McMaster 91595A112, ⌀3 m6 × 12 | 2 | [V] |
| Thumb screws | M3 × 18 knurled, DIN 464 | 2 | McMaster lists 92558A330 (M3 × 12): too short here; length and head UNVERIFIED |
| Lock screw | M3 × 10 socket head + DIN 125 M3 washer (⌀7) (or Carr Lane LS-0, thread UNVERIFIED) | 1 | |
| Heat-set inserts | ruthex RX-M3x5.7 (hole ⌀4.0) | 3 | 100 for US$8.23 [V] |
| Backing | McMaster 8619K561, HDPE 0.79 ±0.05 | 1 sheet | [V] |
| Push wires | ⌀0.6 and ⌀1.1 stainless wire or gauge pins, about 60 long | 1 each | UNVERIFIED part |
| FKM sheet | J-Flex thin-gauge Viton 0.25 ±0.08 | | quote [V]; ±0.08 is wider than the drawing: sort washers by thickness (docs/34 §3.1) |
| Retaining compound | for the liner (and the tubes in the handles) | | any cylindrical retaining grade |

## 4. Use and set-up

* Print the base and the plate flat side down (base top and plate underside are the faces that matter); ream the
  liner hole to 7.95–7.96 and the pin holes; set the inserts with a soldering iron; bond the liner flush with the
  foot face (assemble on a flat plate with the plate upside down).
* Bond each SYNEO tube into its handle with 28.1 mm exposed; keep the tip out of the adhesive.
* Each washer: stroke 1, swap, stroke 2, eject, feed (§1). Sort the washers by measured thickness (docs/34 §4.3).

## 5. What to check first

1. Measure the SYNEO tubes (OD to ±2.5 µm with a micrometer; edge runout to the tube on a microscope, rolling the
   tube in a V-block). Order the slip bushings only then.
2. Punch ten washers; measure OD, ID and the offset of the hole on a microscope with a scale. Accept if all ten are
   inside the drawing.
3. If the 1.397 edge leaves a ragged outside or the washer tears in the 1.245 bore, ask SYNEO for an inside-edge
   tube or fall back to the Rapid-Core pair.

## 6. Checks (`check_results.json`, 33, all pass)

Interference between all 13 solids (none); the outside punch at the bottom of its stroke clears plate, liner,
bushing, base, screws and lock; reach of both punches (28.1 exposed against 20.9 needed: tip 0.15 into the
backing, handle ≥ 3 above the bushing head); push wires pass the tube bores; all three bores in the SF-12 range;
printed wall between liner hole and lock insert 0.77; lock washer overlaps the bushing head by 0.72; lock and thumb
screw engagement; concentricity (§2.4); punch sizes inside the drawing; clamp friction; the plate floats (underside
0.94 above the base and the foot 0.64 above the rail tops at the thinnest stack); the thickest strip slides under
the relief (0.90 clearance); web between washers 1.4; pin engagement 4.9.

## 7. Review

Pending.

## 8. Open questions and choices the user may overrule

* SYNEO price and tolerances (RFQ); whether to ask for an inside-edge 1.40 tube.
* Rapid-Core pair as an immediate start (washer ⌀1.50: at the drawing's limit).
* Strip width 14 and pitch 3 (about 30 washers per 100 mm strip).

## 9. Record

2026-11-18: request "Create CAD of the punching jig, loop until convergence. Make sure to also source the
punches." Sourcing by a research agent (results/tier_round/punch_jig_sourcing.md); design and CAD in this session;
review rounds in `results/tier_round/review_jig_r*.md`.
