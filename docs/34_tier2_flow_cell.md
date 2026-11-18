# 34 — A custom flow cell for tier 2, with the bead bed inside the cell

Status: 2026-11-18. Follow-up to the tier round (docs/26–33) on the user's request: "Let's design a custom flow
cell for tier 2. What type of beads? I'd like the bead bed to be part of the flow cell not the inlet tubing. It
should handle 500 psi. Ideally all custom parts can be ordered from a place like Xometry." Written by the
orchestrator without agents. **Desk work, not independently reviewed; nothing is ordered.**

**Revision B (2026-11-18, same day): the joint between bed bore and exit bore.** In the first version the screen
stood 15 µm proud of a seat in the body and the nozzle plate, drawn up by its screws, pinched it. That clamp had no
defined force, held body and plate apart by a film that joined the retainer to the outlet channel, and bowed the
plate into the thin layer. The retainer now sits in a pocket in the top face of the plate: an elastomer washer
punched from 0.25 mm sheet at the bottom, the screen on it, the membrane on top. The washer is a spring that
presses the membrane against the flat underside of the body around the bed bore; nothing stands proud, so body and
plate meet face to face and the plate stays flat. Sections 0, 3, 4, 5, 6.3, 7, 8 and 10 are revised; the model
numbers changed by at most 0.1 pg/mL.

**Strip dimensions from the vendor drawing (same day).** The user supplied MicruX's drawing "Thick-film
based-electrode features". It is to scale: 17.13 px/mm from the 10.1 mm width gives 27.50 mm for the length,
against 27.5 stated, and 2.8–2.9 mm for the 3 mm working electrode. Measured on it: working electrode centred on
the width, its centre **8.26 mm** from the free end (6.0 had been assumed); printed counter and reference
electrodes from r = 2.56 to **3.64 mm** (3.3 assumed); printed area ends and the four pads begin 21.78 mm from the
free end. The strip stop moved, the stack was shortened to x = +12 so that the pads start 1.5 mm clear of it, and
the strip pocket was deepened to 0.55 mm so that the ceramic strip (0.38 mm) fits as well (section 5.4). The user
then confirmed that the drawing is accurate and that the cell will use the **ceramic strips, 380 µm thick**; the
shim is 0.07 mm (0.05 + 0.02).

**Drawings (same day).** Dimensioned drawings of the three parts were made for ordering from Xometry, with as many
standard tolerances as possible (section 5.2). To get there the strip pocket became 0.65 mm deep at standard
tolerance, measured at assembly with the gap set by the shim (section 4.3); the second dowel hole in plate and
body became a slot; the dowel pins are bonded into the base; the body is 11.4 mm thick.

**Cut gasket (same day).** The washer of the retainer stack became a part with its own drawing, T2C-004, a STEP
file and DXF cut files (one part, and 100 nested at 3 mm pitch). Its outer diameter went from 1.2 to 1.4 mm: at
1.2 the ring wall was 0.225 mm nominal and could fall to about 0.075 mm at the tolerance limits, too fragile to
cut or handle; at 1.4 it is 0.325 mm (at least 0.175 mm). The screen (⌀1.59) still covers it and the compressed
ring fills about 87 % of the free area of its ⌀1.65 pocket (Derived). The spring force doubles (3.2 N nominal),
which widens the margin against lift-off.

**Independent review of the drawings (same day).** An agent that had not seen the design work reviewed the four
drawings against the STEP files and Xometry's drawing requirements and returned 19 findings; all were applied
except a material call-out to ASTM D2000 for the washer (the line call-out could not be checked) and a cosmetic
thread display for the M4 holes. The changes that reach the parts: the M2.5 screws now sit in counterbores in the
plate (low-head M2.5 × 6, DIN 7984) instead of countersinks, so the screw heads no longer fight the dowels; the
dowel holes are ⌀3.00 +0.05/+0.01 everywhere; every screw hole carries a position of ⌀0.3; M4 clearance is ⌀4.8;
the body underside is flat within 0.02 and Ra 1.6 inside ⌀16 and Ra 0.4 inside ⌀3 around the bed bore; the plate's
top face is flat within 0.02 inside ⌀16; the base pocket floor is parallel to A within 0.02; both ends of both
0.5 mm bores are sharp; the inlet port carries a position and its bottom a perpendicularity (neither is on the
user's port drawing); the M2.5 tapped holes have 6.0 mm of full thread; the washer drawing gives its thickness as
0.25 ±0.05 and a process note. The tolerance table (section 5.2) is the current list.

**Tightest tolerance ±0.03 mm (same day, at the user's request).** Nothing on the drawings is now tighter than
±0.03 mm; geometric zones are at least 0.03. Dowel holes and slot ⌀3.00 +0.05/+0.01 → **⌀3.04 ±0.03** (3.01–3.07);
retainer pocket ⌀1.65 +0.05/−0 × 0.27 ±0.025 → **⌀1.68 ±0.03 × 0.27 ±0.03**; base top face flat, base pocket floor
parallel, plate top face and body underside flat: 0.02 → **0.03**. Nominals moved to the middle of the old limits so
no part loosens by more than 0.02 mm; STEP files, checks (all pass) and `tier2_cell.md` were regenerated. Effects
(Derived): the pin clearance on a 3 m6 pin is 0.002–0.068 mm instead of 0.002–0.048, so plate and body can sit up
to about 0.02 mm further apart sideways and the worst-case sealing band around the bed bore narrows by that much
more; the compressed washer fills about 84 % of the pocket instead of 87 %; the force pushing the retainer away at
80 µL/min goes from 0.21 to 0.22 N (margin still > 2); a 0.03 mm flatness on each face of the body–plate joint
allows a film up to about 0.03 mm at the worst, which would by-pass about 2 % of the stream (5 µm 0.01 %, 15 µm
0.26 %, 25 µm 1.2 %, `tier2_cell.md` §5) — faces at their tolerance limit and both bowed the same way are unlikely,
and a dimensional report on the first lot shows it. The gap is unaffected: the pocket depth is measured and the shim
sets it. No LOD figure changes.

**Screw torques for acetal (same day).** The 0.5 N·m of the M4 screws had been set for PEEK; on acetal it puts
24 MPa under the 8 mm washers, enough for the plastic to creep and the clamp to relax. Now M4 0.25 N·m and M2.5
0.05 N·m (none had been given), each keeping the stress on the acetal near 10 MPa. The mechanics of section 6.3
were re-run for acetal; the load path was traced (the M4 screws carry 595 N at 500 psi, not the 854 N of every
load added) and the M4 margin is 2.1 (1.5 after relaxation; 19 in operation). Sections 0, 4.2, 6.3 and 7.

Where the numbers come from:
* Dimensions: `cad/elisa_cad/tier2_cell/params.py`, the one file that the CAD model and the calculation read.
* CAD: `cad/elisa_cad/tier2_cell/` → `cad/out/tier2_cell/` (STEP files of the three custom parts and of the
  assembly, renders, the section below, notes for the drawings, 28 checks, all pass).
* Model, pressure drop, mechanics: `scripts/tier_round/tier2_cell.py` → `results/tier_round/tier2_cell.md`,
  `.json` (10 checks, all pass; about 1 min). The assay is the unchanged tier 2 of docs/30; only the bed holder, the retainer,
  the walls around the bed and the cell are replaced. `tierkit.py`, `designs.py`, `src/` and `params/` are not
  edited.

Every LOD is a model prediction with the kit and parameters of docs/30, not a measurement. "Nominal" = all
parameters at their best estimate; "median [5–95 %]" = Monte Carlo over the parameter bounds (n = 2000). Evidence
labels as in docs/28: **[V]** page or document opened in this session, **[S]** search summary only, **Derived**,
**UNVERIFIED**. **Gap** = height of the liquid layer over the working electrode. **Retainer** = whatever holds the
beads back while the liquid passes.

## 0. Summary

**Beads: stay with Dynabeads M-280 Streptavidin, 2.8 µm (11205D), 1×10⁶ per determination.** They are the surface
on which the project's non-specific-binding rate is defined, and the model finds no better size: at equal bead
area the captured fraction is the same from 1 to 20 µm (63–66 %), because capture is limited by the binding
reaction and not by transport to the bead. What the bead size does decide is the retainer (next point). A second
bead fits the same cell without change and is the fallback: non-porous streptavidin polystyrene of 10–14 µm.

**The retainer is the part that needed a new answer.** The stainless screens sold for HPLC filters are rated
nominally: the vendor states that its 1 µm screen is absolute only at 6–7 µm and its 2 µm screen at 7–8 µm [V].
Neither holds 2.8 µm beads safely. A sintered 0.5 µm frit does, but its inner surface takes up conjugate: with
40 mm² the model LOD is 5.0 pg/mL. The design therefore uses a **track-etched membrane with 1 µm pores lying on
the 2 µm screen**: the membrane retains, the screen carries it. The 10–14 µm beads need the screen alone.

**The cell** is a stack of three machined parts, 29 × 44 × 21.9 mm (figure in section 4):

| Part | Material | What it carries |
|---|---|---|
| Body | acetal copolymer (PEEK fallback) | inlet port on top; the port floor is 2.5 mm thick and the **bed bore (0.5 mm) runs through it**, so the bed sits in the body; its flat underside is the face the membrane seals against; outlet port on the end face |
| Nozzle plate | acetal copolymer (PEEK fallback) | pocket in its top face for the retainer (washer, screen, membrane), which the washer presses against the body; exit bore (0.5 mm) to the electrode; its underside is the lid of the thin layer, with the O-ring that seals on the strip and a collecting groove around the electrode |
| Base | 316L stainless | pocket that locates the MicruX strip and sets the gap (0.10 mm) with a shim |

The bed is 2.5 mm above the working electrode with 0.52 µL between them, the same dead volume as docs/30. The
MicruX strips, their connector cable and the 1/4-28 fittings in hand are used as they are. There is no magnet in
the cell, so the concern of docs/30 §4.2 (step 4) about the magnets of the MicruX add-on does not arise.

**500 psi.** The whole liquid path, including the seal on the strip, is laid out for 500 psi (34.5 bar): the four
M4 screws at 0.25 N·m hold 2.1 times the force that pressure puts on them (1.5 after the acetal relaxes), and the thinnest wall beside a bore is 0.9 mm. In use the
cell needs far less. With the bed in a 0.5 mm bore the pressure drop of the whole cell is 1.0 bar at 80 µL/min
and 2.5 bar at 200 µL/min (docs/30: 25 bar across the bed at 80 µL/min, because its capillary is 0.2 mm). **Not
shown by calculation: that an O-ring seals on a printed strip at 500 psi.** That needs a proof test (section 8).

**Xometry.** All three custom parts are plain 3-axis milling. Every hole is ≥ 0.5 mm, the feature size Xometry
recommends as its minimum [S], and no hole is deeper than 7.5 diameters. Dimensioned drawings (A3 PDF, one per
part) are in `cad/out/tier2_cell/drawings/` with an ordering sheet. Everything is at Xometry's standard tolerance
except the features listed in section 5.2, none tighter than ±0.03 mm (user's limit, 2026-11-18), looser than the
±0.001 in (±0.025 mm) Xometry quotes automatically [S]. No quote was obtained and no price is given.

**What the cell changes in the model** (pg/mL):

| | docs/30 tier 2 (capillary in the MicruX inlet bore) | This cell, M-280 | This cell, 10–14 µm beads |
|---|---|---|---|
| LOD nominal; median [5–95 %] | 2.1; 8.4 [1.0–100] | **1.9; 7.9 [0.96–93]** | 1.8; 7.4 [0.93–88] |
| P(LOD ≤ 1) / P(≤ 10) | 0.05 / 0.54 | 0.06 / 0.57 | 0.06 / 0.58 |
| Upper limit by the slope criterion | 1400 | 1400 | 1400 |
| Pressure drop across the bed at 80 µL/min | 25 bar | 0.63 bar | 0.15 bar |

The gain is small (10 %) and comes from the shorter wall above the bed (3.8 mm² instead of 13 mm² of capillary).
The cell is not a way to a lower LOD; it is a way to make tier 2 a rigid, repeatable part instead of a sleeved
capillary. The largest unknown of the cell is the conjugate that the retainer takes up (section 6.1).

**Strip dimensions are settled**: ceramic strips, 380 µm (stated by the user), positions from MicruX's drawing,
which the user confirmed is accurate (section 5.4). What still has to be made before an order is a dimensioned
drawing for each part (section 8.2).

## 1. What the request changes

| Request | Consequence |
|---|---|
| The bed is part of the cell | The bed bore is machined into the body, on the axis of the electrode. The retainer cannot be a frit in a capillary; it is a stack held between two parts of the cell |
| 500 psi | The MicruX add-on is PMMA, held by magnets, with no pressure rating (docs/28 §1.1). The new cell is acetal copolymer (or PEEK) on a steel base, bolted, with O-rings in grooves and a hard stop that sets the gap |
| Custom parts from a service such as Xometry | No hole below 0.5 mm, no micro-drilling, no bonded or moulded part, no custom electrode. Everything else is a catalogue part |
| "What type of beads?" | Section 2 |

Kept from docs/30 and docs/33: the assay and its step table (56.7 min), the fresh strip and fresh bed for every
determination, the printed carbon strip with its printed Ag/AgCl reference, the radial thin-layer shape (inlet on
the electrode axis, radial outflow), 0.5 µL between bed and electrode.

## 2. Beads

### 2.1 What the model says about size

From `results/tier_round/tier2_cell.md` §1 (this cell, retainer 4.9 mm², nominal LOD in pg/mL):

| Beads | Same bed volume (19 nL): captured; LOD | Same bead area (24 mm²): bed volume; captured; LOD |
|---|---|---|
| 1.0 µm | 78 %; 2.5 | 7 nL; 66 %; 1.9 |
| **2.8 µm** | **65 %; 1.9** | 19 nL; 65 %; 1.9 |
| 4.5 µm | 52 %; 2.0 | 31 nL; 65 %; 1.9 |
| 10 µm | 29 %; 3.1 | 68 nL; 64 %; 1.9 |
| 20 µm | 16 %; 5.5 | 136 nL; 63 %; 1.9 |

Reading. In the kit the film coefficient to a 2.8 µm bead is 1.0×10⁻⁴ m/s and the surface reaction is
4.2×10⁻⁶ m/s, so the reaction limits capture and only the bead area counts. The bore does not matter either:
65–66 % from 0.15 to 0.5 mm at the same bed volume (LOD 1.8–1.9). The blank grows with the bead area, so more beads do not
help (docs/30 §4.5: twice the beads 2.3). The model therefore leaves the size free, and the choice is made on
other grounds.

### 2.2 The choice

| Candidate | For | Against | Verdict |
|---|---|---|---|
| **Dynabeads M-280 Streptavidin, 2.8 µm, non-porous, superparamagnetic** (11205D; 6–7×10⁸ beads/mL, about 10 µg biotinylated antibody per mg; docs/28 R32 [V]) | the surface on which the project's non-specific rate is defined (docs/04); in the bill of materials; uniform size; coated and washed in tubes on a magnet rack. Tosyl-activated hydrophobic surface, blocked with BSA [S] | needs a retainer that is absolute below 2.8 µm; the stock's BSA must be exchanged for IgG-free BSA (docs/30 §2.1) | **first choice** |
| Dynabeads M-270 Streptavidin, 2.8 µm | hydrophilic carboxylic-acid surface, not blocked with BSA; the vendor recommends it where M-280 gives background [S] | conjugate binding to it is not known to this project | comparator in test T2-1; same cell, same retainer |
| **Streptavidin polystyrene, 10–14 µm, non-porous** (Spherotech SVP-100-4, 0.5 % w/v, 4 mL [S]) | held by the 2 µm screen alone (absolute at 7–8 µm [V]), so no membrane; bed pressure 4 times lower | not magnetic (washed by centrifugation); polystyrene surface, conjugate binding and biotin capacity unmeasured (the vendor's sheet gives about 0.37 nmol biotin-FITC per mg for particles it does not name [S]); 4.3 times the bed volume for the same area | **fallback** if the membrane proves awkward. Same cell |
| Dynabeads MyOne, 1 µm | — | no gain in the model at equal area; needs a 0.2–0.45 µm membrane; 3 times the pressure | no |
| Porous media (agarose, perfusion resins of 20–50 µm) | high capacity | the inner surface takes up conjugate and releases product slowly; agarose deforms under pressure; capacity is not what limits this assay | no |

The model treats both chosen beads alike (packed-bed factor 3 on the bead surface). That is an assumption for
the polystyrene beads: with factor 1 their LOD would be 1.3, with factor 10 it would be 3.3. Test T2-1 of docs/30
measures it on empty and non-immune beds.

Amounts per determination (Derived). M-280: 1×10⁶ beads = 1.5 µL of stock (docs/30); bed 19 nL, 0.10 mm long in
the 0.5 mm bore (35 bead layers). Polystyrene 10–14 µm, taken as 12 µm: 5.4×10⁴ beads for the same 24 mm², bed
81 nL, 0.41 mm long (35 layers), about 10 µL of the 0.5 % stock (density 1.05 g/mL, UNVERIFIED).

## 3. The retainer

| Retainer | Holds 2.8 µm beads? | Wetted area inside a 0.5 mm bore (UNVERIFIED) | Verdict |
|---|---|---|---|
| VICI stainless screen 1/16 in, 2 µm, 0.075 mm thick (2SR1-10) or 1 µm, 0.050 mm (1SR1-10) [V] | **no**: "nominal micron retention"; absolute 7–8 µm (2 µm screen) and 6–7 µm (1 µm screen) [V] | 1.2–8.8 mm² | alone: only for the 10–14 µm beads |
| VICI sintered frit 1/16 in, 0.5 µm, 0.75 mm thick (.5FR1-10); 1/32 in, 0.25 mm (.5FR.5-5) [V] | yes | of the order of 10–100 mm² (ten times the thickness of the screen, finer pores) | no: model LOD 5.0 at 40 mm² |
| Track-etched polycarbonate membrane, 1 µm pores, 6–15 µm thick, about 2×10⁷ pores/cm², made hydrophilic with PVP (e.g. Sterlitech PCT1013100, 13 mm discs, 100 per pack [S]) | yes: the pores are straight holes of one size | 1.1–2.3 mm² (pore walls and both faces) | **on top of the 2 µm screen**, which carries it |

How the areas were estimated (`retainer_area()` in the script). The vendor does not publish what its screens are
made of. Low: woven wire cloth, surface 4(1 − ε)/d with ε = 0.5 and 25 µm wire. High: a porous body, 4ε/d with
ε = 0.3 and 2 µm pores. The nominal value is their geometric mean. Membrane: N·π·d·t for 2×10⁵ pores per mm²,
plus both faces. Only the part of the retainer inside the bore cross-section is counted; conjugate that diffuses
sideways into the clamped rim of the screen (about 0.12 mm in the 4 min of the conjugate step, Derived) is not.

| Bed | Retainer | Low / nominal / high (mm²) |
|---|---|---|
| M-280, bore 0.5 mm | membrane on screen | 2.3 / 4.9 / 11 |
| M-280, bore 0.3 mm | membrane on screen | 0.8 / 1.7 / 4.0 |
| 10–14 µm, bore 0.5 mm | screen | 1.2 / 3.2 / 8.8 |

The nominal value for the chosen case, 4.9 mm², is by coincidence the 5 mm² that docs/30 takes for its frit. The
retainer area grows with the bore area. That is the price of the 0.5 mm bore, and section 6.3 has the 0.3 mm
variant.

### 3.1 How the joint between bed bore and exit bore is sealed (Revision B)

The retainer sits in a pocket ⌀1.68 × 0.27 mm (both ±0.03) in the top face of the nozzle plate, over the exit bore.
From the bottom:

| Layer | Part | Thickness free → in place (mm) | Job |
|---|---|---|---|
| 1 | Washer ⌀1.4/⌀0.75, cut from 0.25 mm FKM sheet (drawing T2C-004) | 0.25 → 0.185 (26 % squeeze) | the spring; its hole passes the liquid to the exit bore |
| 2 | Screen 1/16 in, 2 µm (VICI 2SR1-10) | 0.075 | carries the membrane over the washer's hole |
| 3 | Membrane ⌀1.5, 1 µm track-etched polycarbonate | 0.010 | retains the beads |

The stack is 0.335 mm free and 0.27 mm in place. The pocket is made to ±0.03 (drawing T2C-002), measured,
and each washer is picked by its measured thickness so that the squeeze stays near 26 %. Its top, the membrane, is in the plane of the plate's top face,
where it meets the flat underside of the body. What each path meets:

| Path | What closes it |
|---|---|
| Beads from the bore, sideways over the membrane to its edge | the membrane pressed against the body face (Ra ≤ 0.4 µm there) over a band 0.5 mm wide around the bore, at about 2 MPa (0.9–3.0 MPa over the tolerances) |
| Liquid from the screen's edge, between body and plate, to the cross channel | body and plate face to face, flat within 0.03 mm, clamped by the M2.5 and M4 screws; with nothing proud the film is set by the flatness of the faces. A 5 µm film passes 0.01 % of the stream, 15 µm 0.3 % (`tier2_cell.md` §5) |
| Liquid to the outside | the 12 × 1 O-ring between body and plate, rated with the rest of the cell for 500 psi |

Numbers (`tier2_cell.md` §4; rubber modulus 6 MPa and the shape-factor correction of Gent, UNVERIFIED):
* Squeeze of the washer 26 % nominal; 11–39 % for a pocket within ±0.01 of the washer chosen for it, a sheet
  at ±0.02, membranes of 6–15 µm and the screen at ±0.005. The low end is below the usual 15 % for a gasket:
  pick washers from the thick end of the sheet for a deep pocket.
* Washer force 3.2 N (1.4–4.7 N). It bows the plate by at most 4.4 µm in acetal (the first version: up to 15 µm).
* The flow pushes the stack away from the body face with the pressure drop through bed, membrane and screen. Taken
  over the whole pocket this is 0.21 N at 80 µL/min, a sixth of the lowest washer force, and 0.53 N at
  200 µL/min, still under half of it. Every step of docs/30 through the bed stays at ≤ 80 µL/min, packing included.
* At 500 psi with the outlet plugged the pressure is the same on both sides of the stack, so it does not load the
  washer.

Why not an O-ring here. An O-ring of 0.5 mm cross-section around the bore, pressing the membrane's rim, was the
first idea (the conversation of 2026-11-18). Such O-rings are hard to get. An O-ring in the body face also needs a
land inside it next to the bed bore, which either holds body and plate apart again or leaves a gap the beads
spread into. A 1 mm cross-section works only as the spring under a 1/8 in screen, around a PEEK boss that carries
the exit bore (section 6.4).

Load on the retainer. The bed pushes on it with the pressure drop across the bed times the bore area: 0.012 N at
80 µL/min, and 0.68 N if the full 500 psi fell across the bed (Derived). The screen carries that; the membrane
spans only the openings of the screen.

## 4. The cell

![Section of the cell](../cad/out/tier2_cell/section.png)

Other views: `cad/out/tier2_cell/assembly_iso.png`, `assembly_exploded.png`, `nozzle_plate_underside.png`,
`nozzle_plate_top.png`, `body_underside.png`, `base_top.png`.

### 4.1 Liquid path

| # | Element | Dimensions (mm) | Volume | Note |
|---|---|---|---|---|
| 1 | Inlet port | 1/4-28 flat-bottom, in the top of the body, on the electrode axis | — | the 1/16 in transfer line butts on the port floor; no cavity between tube and bore |
| 2 | **Bed bore** | ⌀0.5 × 2.5, the floor of the inlet port | 0.49 µL | the bed occupies the lowest 0.10 mm (M-280) or 0.41 mm (10–14 µm); the rest is 3.8 mm² of plastic wall above the bed (docs/30: 13 mm² of capillary) |
| 3 | Retainer | membrane on screen on washer, in a pocket in the plate, section 3.1 | about 6 nL of pores | |
| 4 | Washer hole and exit bore | ⌀0.75 × 0.185 in the washer, then ⌀0.5 × 2.23 through the plate | 0.08 + 0.44 µL | 3.5 mm² of plastic and 0.44 mm² of elastomer between bed and electrode (docs/30: 2.5 mm²); the elastomer is counted with the retainer at the frit factor (UNVERIFIED); the volume is kept at 0.5 µL on purpose, section 6.1 |
| 5 | Thin layer | gap 0.10 over the strip, liquid disc ⌀6.9 inside the O-ring | 0.71 µL over the electrode, 3.7 µL in all | flat land of the plate out to r = 2.3; the 3 mm electrode ends at r = 1.5 |
| 6 | Collecting groove | r = 2.3–2.9, 0.5 deep, in the plate underside | 4.9 µL | takes the liquid all round the electrode so that the outflow is radial, as the kit assumes. The sector opposite the riser carries 0.75 of the flow of the nearest one (`tier2_cell.md` §5) |
| 7 | Riser, cross channel, riser | ⌀0.6 through the plate; slot 0.8 × 0.5 in the top face of the plate; ⌀1.0 in the body | — | the slot moves the liquid outward past the inlet port; it is closed by the body underside inside the 12 × 1 O-ring |
| 8 | Outlet port | 1/4-28 flat-bottom, end face away from the strip's contacts | — | to waste, or to a restrictor if back-pressure is wanted |

### 4.2 Seals, stops and screws

| Joint | Seal | Hard stop | Held by |
|---|---|---|---|
| Plate on strip | O-ring 7 × 1 in a groove ⌀6.9/⌀9.3 × 0.65 deep; 25 % squeeze at the nominal gap, 20–30 % over the gap tolerance | the plate rests on the base on both sides of the strip pocket | 4 × M4 × 20 through body and plate into the base, **0.25 N·m**; 2 × ⌀3 dowel pins |
| Body on plate | O-ring 12 × 1 in a groove ⌀11.9/⌀14.3 × 0.75 deep in the body | face to face | 4 × M2.5 × 6 low-head socket screws in counterbores, from the plate underside into the body, **0.05 N·m**, so that the retainer and the bed are not disturbed when the strip is changed |

Torques (section 6.3; dry threads, nut factor 0.2). They are set by the acetal, not by the screws: the stress under
the M4 washers and the M2.5 heads is kept near 10 MPa, a long-term guide for acetal (UNVERIFIED), so that the
plastic does not creep and let the clamp go. The 0.5 N·m of the PEEK version would put 24 MPa under the 8 mm
washers. No larger washer fits: the screws at x = +8 are 4 mm from the edge of the body, and a washer under the
M2.5 heads would stand 0.2 mm proud of the plate underside. A trace of anti-seize on the M4 threads (stainless
into 316L can gall) gives about a third more preload at the same torque, so the margins are minima. 0.05 N·m is
below most adjustable torque screwdrivers (commonly from 0.1 N·m, UNVERIFIED); a micro-torque driver is needed.
| Retainer | membrane pressed against the body face by the washer | membrane top in the plane of the plate face | the washer (3.2 N); body and plate held by the same four M2.5 screws |

### 4.3 The gap

Gap = pocket depth − strip thickness − shim = **0.10 mm**. The pocket is 0.65 mm deep at the standard
tolerance (±0.13); its depth is measured once per base with a depth micrometer, and the shim under the ceramic
strip (380 µm, stated by the user) is chosen as depth − 0.38 − 0.10: 0.17 mm at the nominal depth, 0.04–0.30 mm
over the tolerance. A strip lot of another thickness, or a PET strip, needs only another shim. With the depth
measured to ±0.01, the strip at an estimated ±0.02 and the shim at ±0.005 the gap is 0.10 ± 0.03.

Why 0.10 and not the 0.05 of docs/33. For tier 2 the model LOD is 1.9 at 0.05, 0.10 and 0.20 mm alike; the gap
matters only if the signal is weak (section 6.1). A printed strip is not known to be flat to 0.05 mm. A thicker
shim gives 0.05 without a new part.

The liquid layer between working and reference electrode is thin, as in docs/33 §6.2: tens of kΩ, a few tens of
microvolts at nanoampere currents.

## 5. Parts

### 5.1 Custom parts (STEP files in `cad/out/tier2_cell/`)

| Part | File | Material | Size (mm); mass | Machining |
|---|---|---|---|---|
| Base | `base.step` | 316L stainless | 29 × 44 × 8; 78 g | one side: pocket, 4 threads, 2 reamed holes |
| Nozzle plate | `nozzle_plate.step` | acetal copolymer (POM-C), natural; PEEK fallback | 29 × 44 × 2.5; 4 g | two sides: grooves and counterbores below, retainer pocket and slot above |
| Body | `body.step` | acetal copolymer (POM-C), natural; PEEK fallback | 29 × 44 × 11.4; 17 g | three sides: port and holes from the top, groove and threads from below, port from one end |

Why these materials (revised 2026-11-18 at the user's request for a cheaper plastic). Plate and body are acetal
copolymer (POM-C): cheaper than PEEK (UNVERIFIED; no quote obtained, and for parts this small machining time
dominates the price), it machines cleanly to burr-free 0.5 mm bores, fine threads and flat faces, its modulus
(about 2.8–3.1 GPa against 3.6, UNVERIFIED) is close to PEEK's, and it takes neutral and mildly alkaline buffer
(pH 9.5), isopropanol and methanol (UNVERIFIED against a chemical-resistance table). Copolymer, not Delrin
homopolymer: thick homopolymer stock can be porous along its centreline, where the bed bore runs. Open points:
the conjugate uptake of the walls between bed and electrode was taken for PEEK and may differ for acetal (test
C-3 and the bench conjugate-sticking test show it); acetal can release traces of formaldehyde (effect on the read
UNVERIFIED, not expected at the read potential). The numbers of section 6.3 were first left at PEEK (user's
decision) and were re-run for acetal when the screw torques were set (same day, at the user's request): the plate
bows 4.4 µm instead of 3.3, and the torques are now set by the bearing stress on the acetal (section 4.2). PEEK, unfilled, natural, stays the fallback if the
bench shows conjugate uptake or leachables. The reasons first given for PEEK: PEEK is the usual wetted polymer of HPLC, takes a thread for the fittings and does not
craze in the 10 % methanol used for storage; PMMA does (docs/28 §4). Unfilled, because glass or carbon fill
would put fibres at the bore edges and carbon-filled PEEK conducts. The base is not wetted in normal use; 316L
keeps threads and flatness and tolerates spilled chloride buffer. Xometry lists PEEK for machining [V, its
micro-machining page]; that it stocks 316L was not checked on a page of its own.

### 5.2 Drawings and tolerance policy

**Drawings** (A3, third-angle, mm; generated by `python -m elisa_cad.tier2_cell.drawings` from the same solids and
parameters as the STEP files, so the two cannot drift apart):

| Part | Drawing | STEP | Views |
|---|---|---|---|
| Base | `cad/out/tier2_cell/drawings/T2C-001_base.pdf` | `T2C-001_base_revA.step` | top, section A–A |
| Nozzle plate | `T2C-002_nozzle_plate.pdf` | `T2C-002_nozzle_plate_revA.step` | top, bottom, section A–A (2:1, under the top view), detail D of it (10:1) |
| Body | `T2C-003_body.pdf` | `T2C-003_body_revA.step` | top, bottom, section A–A, detail E (10:1) |
| Washer (cut gasket) | `T2C-004_washer.pdf` | `T2C-004_washer_revA.step`; cut files `T2C-004_washer.dxf`, `T2C-004_washer_sheet.dxf` (100 parts) | top view at 20:1 (thickness as a note) |

At the user's request the drawings carry **only the features toleranced tighter than standard and the threaded
holes**: each such feature is flagged (finer finishes and the 0.05 mm edge break at the ends of the 0.5 mm bores
included), with the datums and basic dimensions its tolerance needs. All other geometry is defined by the STEP file
of the same drawing number and revision at the standard tolerance stated in the title block. A second request
removed every note on how to make, clean or pack the parts (left to the supplier), the reasons in the flag texts,
the isometric views, the part masses and the washer's actual-size outline; the notes are now the material and the
threads only. A third request ("as simple as possible") removed the list of flagged features (each requirement now
sits on the views, with its numbered flag), the basic dimensions (locations of toleranced features are BASIC per
the STEP model, stated in the title block), the base's section and the plate's bottom view, and the separate Ra 1.6
symbols (Ra 1.6 all over in the title block of the three machined parts; only the body's Ra 0.4 and the port
bottoms' Ra 0.8 remain). To let the M4 holes go to standard tolerance their clearance in plate and body became
⌀5.5 (fixed-fastener check: 5.5 − 4.0 = 1.5 mm ≥ ⌀0.37 for steel at ±0.13 plus ⌀0.71 for plastic at ±0.25,
Derived). The riser position went back to standard: the riser only has to open into the collecting groove inside
the liquid disc, which it does anywhere within ±0.25. The collecting groove keeps ±0.10: at standard tolerance on
its diameters and depth the flow through the far side of the thin layer could fall from 0.75 to 0.21 of the near
side (Derived, same formula as `tier2_cell.md` §5). The port-bottom perpendicularity and the body's overall
flatness of 0.05 (both added after the review, neither needed for a seal) were dropped.

Each sheet carries what Xometry's drawing guidance asks for [V, its "technical drawing best practices" page]: a
title block with material specification, finish, scale, units, projection and a default-tolerance block; notes at
the top left; a revision table at the top right; sheet number; an isometric view (removed at the user's request:
the STEP file shows the part); threads with series, class and
depth; tighter-than-standard tolerances called out and flagged (triangular flags) for inspection.
`ORDERING.md` beside the drawings lists what to upload and select for each part.

**Tolerance policy.** Everything is at Xometry's standard (±0.13 mm metals, ±0.25 mm plastics, Ra 3.2, edges
broken [S]) unless a function needs more. Three design changes made that possible:

| Change | What it relaxed |
|---|---|
| Strip pocket depth measured at assembly and the gap set with the shim (section 4.3) | the base pocket depth, from ±0.02 to standard |
| Second dowel hole in plate and body made a slot along the line between the pins | the pin spacing in all three parts, from a matched ±0.01 to standard |
| Pins bonded into the base instead of pressed | the base pin holes, from a press fit (P7) to the same ⌀3.04 ±0.03 as the others |

What remains tighter than standard, and why:

| Part | Feature | Called out | Why |
|---|---|---|---|
| all | dowel hole (B) and slot (C) | ⌀3.04 ±0.03 | locate the three parts on ⌀3 m6 pins (bonded in the base, so the base holes need room for the compound) |
| Plate, body | M2.5 clearance holes (plate) and tapped holes (body) | position ⌀0.3 to A\|B\|C | M2.5 in ⌀3.2 leaves 0.7 mm, less than two plastic parts at standard (1.42); the M4 holes are at standard with a ⌀5.5 clearance |
| Base | top face (datum A) | flat 0.03 | the plate rests on it; sets the gap |
| Base | pocket floor | parallel to A within 0.03 | carries the brittle ceramic strip; keeps the gap even across the electrode |
| Plate | exit bore, retainer pocket | ⌀0.50 ±0.05; ⌀1.68 ±0.03; position ⌀0.10 to A\|B\|C; edge break ≤ 0.05 at both ends of the bore | the membrane's sealing band around the bed bore must survive the offsets of both parts (worst case it narrows from 0.5 to about 0.3 mm, 0.02 less with the ±0.03 pin holes) |
| Plate | retainer pocket depth | 0.27 ±0.03 | sets the washer's squeeze; the washer is picked by measured thickness to suit the measured depth (section 3.1) |
| Plate | strip O-ring groove; collecting groove | ⌀ ±0.05 and depth ±0.05; ⌀ ±0.10 and depth ±0.10 | O-ring gland; radial outflow |
| Base, plate, body | all surfaces | Ra 1.6 all over (title block) | lid of the thin layer, O-ring seats, sealing faces; one call-out instead of a symbol on each |
| Plate | top face inside ⌀16 | flat 0.03 | the body seals on it, face to face |
| Body | bed bore | ⌀0.50 ±0.05, position ⌀0.10 to A\|B\|C, edge break ≤ 0.05 at both ends | as for the exit bore |
| Body | underside (datum A) | inside ⌀16 flat 0.03; inside ⌀3 Ra 0.4 | the membrane seals on the ⌀3 area, the 12 × 1 O-ring and the face-to-face joint on the ⌀16 area |
| Body | body–plate O-ring groove | ⌀ ±0.10, depth ±0.05 | O-ring gland |
| Body | both 1/4-28 ports | values of the user's port drawing: bottom flat 0.05, Ra 0.8, corner R ≤ 0.18, full thread ≥ 7.11; added here: inlet thread position ⌀0.10 to A\|B\|C | the fitting seals on the port bottom; the tubing end must sit over the bed bore |
| Washer (T2C-004) | outer and inner diameter; thickness; hole position | ⌀1.40 ±0.10 / ⌀0.75 ±0.10; 0.25 ±0.05 (sheet tolerance); ⌀0.10 to the outer edge (B) | wall ≥ 0.175 mm; washers are sorted by measured thickness at assembly |

Nothing is tighter than ±0.03 mm (the user's limit; geometric zones ≥ 0.03). Outside ⌀16 the plate's flatness is left at standard: the 2.5 mm plate is
clamped flat between the body and the base, whose top face is held to 0.03.

### 5.3 What Xometry states (checked as far as its pages were reached)

| Point | Statement | Evidence |
|---|---|---|
| Smallest feature | "keep features 0.020 in (0.50 mm) or larger"; may vary with geometry and material | [S], Xometry precision-machining page |
| Standard tolerance | ±0.005 in for metals, ±0.010 in for plastics unless a drawing says otherwise | [S] |
| Tight tolerance | ±0.001 in auto-quoted for metals and for PEEK, ULTEM, Delrin and PTFE; tighter after manual review | [S], Xometry blog on tight tolerances |
| Hole depth | 4 diameters standard, up to 10 achievable | [S] |
| Micro machining | offered, with cutters below 0.010 in; PEEK listed among its plastics | [V], Xometry micro-machining page |

The design uses 0.5 mm holes at up to 5 diameters and a 1.0 mm hole at 7.5. The tightest tolerances on the
drawings are ±0.03 mm (pin holes and slot, retainer pocket) and flatness 0.03 (sealing faces); whether Xometry quotes them instantly or
after manual review was not tried. No quote was requested; price and lead time are not known.

### 5.4 Purchased parts, and what to measure first

| Item | Part | Evidence |
|---|---|---|
| Electrode | MicruX ED-S1PE-C21C strip (ceramic, 0.38 mm), 27.5 × 10.1 mm, 3 mm carbon working electrode, printed Ag/AgCl reference; ED-SPE-CABLE | docs/28 [V]; in hand |
| Fittings | 1/4-28 flat-bottom, for 1/16 in tubing; the MicruX packs state 1000 psi for their ferrules (docs/28 R6 [V]); IDEX states 2000 psi for its flangeless nut with the P-200 ferrule [V, page of XP-235, a part now marked obsolete] | in hand |
| Screen | VICI 2SR1-10, 1/16 in, 2 µm, 0.075 mm, pack of 10 | [V] |
| Washer | drawing T2C-004: cut gasket ⌀1.4/⌀0.75 from FKM (or EPDM) sheet 0.25 ±0.05 mm, 70–75 Shore A, cut with a compound punch die or fine waterjet from the DXF (not laser: FKM releases HF); one washer per bed (or punched in the lab with 1.4 and 0.75 mm biopsy punches) | sheet thickness tolerance and punch sizes UNVERIFIED |
| Membrane | track-etched polycarbonate, 1.0 µm, hydrophilic, 13 mm discs; 1.5 mm biopsy punch | [S]; thickness and pore density of the lot to be read from its certificate |
| O-rings | 7 × 1 and 12 × 1 mm, 70–75 Shore A (FKM or EPDM) | standard sizes, UNVERIFIED against a catalogue |
| Screws, pins | 4 × M4 × 20 socket head with small washers (8 mm, DIN 433) over ⌀5.5 clearance holes; 4 × M2.5 × 6 low-head socket (DIN 7984; head about ⌀4.5 × 1.6, UNVERIFIED) in ⌀5.5 × 1.9 counterbores; 2 × ⌀3 m6 × 16 dowel pins, bonded into the base with a retaining compound; stainless | standard |
| Shim | stainless shim stock 0.01, 0.02, 0.05 and 0.10 mm, cut 10 × 20 mm, stacked to depth − 0.38 − 0.10 (0.17 at the nominal pocket depth) | standard |
| Beads | Dynabeads M-280 Streptavidin 11205D | docs/07 |

**Strip dimensions** (`params.py`). Items 2–4 were measured on MicruX's drawing "Thick-film based-electrode
features" (supplied by the user, who confirmed it is accurate; to scale, checked by its length, 27.50 mm
against 27.5 stated). Item 1 is the user's.

| # | Dimension | Used for | Value | Source |
|---|---|---|---|---|
| 1 | Thickness of the strip | shim | **0.38 mm** (ceramic) | user; MicruX drawing gives the substrate as 380 µm |
| 2 | Centre of the working electrode from the end without contacts | position of the pocket stop | **8.26 mm** (6.0 assumed before) | drawing |
| 3 | Outer radius of the printed counter (arc) and reference (sector) electrodes | inner edge of the strip O-ring's contact | **3.64 mm** (3.3 assumed); inner radius 2.56 | drawing |
| 4 | Where the pads begin | the stack must end before them | 21.78 mm from the free end; the stack ends 1.5 mm before them | drawing |

Ceramic is brittle. The strip carries the O-ring's 25 N and, at 500 psi, about 230 N of pressure, both pushing it
onto the shim and the pocket floor; it is not bent as long as it lies flat on them. Hence the floor is specified
parallel to A within 0.03 mm, the shim is cut whole (no stacked offcuts under the electrode) and kept free of burrs, and the
M4 screws are tightened evenly in a cross pattern.

What item 3 means for the strip seal. The 7 × 1 O-ring has its inner edge at r = 3.5; its contact band starts
about 0.15 mm further out, at r ≈ 3.65, which is the outer rim of the printed counter and reference electrodes
(margin 0.0 mm). With pressure inside, the ring is pushed to the outer wall of its groove (r = 4.65) and its contact
moves out to about r = 3.85–4.55, clear of the print. At worst the ring lies on the outer 0.1 mm of the print,
whose step (10–20 µm, UNVERIFIED) is small against the 0.25 mm the ring is squeezed. A larger ring has no room:
the space between the print (r = 3.64) and the strip edge (r = 5.05) is 1.41 mm, and a 1 mm cord needs a groove
about 1.2 mm wide plus play for the strip in its pocket. MicruX seals the same strip with an O-ring of 8 mm inner
diameter [V docs/28], which on a 10.1 mm strip can only be a thinner cord.

## 6. Numbers

### 6.1 Model (`results/tier_round/tier2_cell.md` §2)

| Case | Nominal | Median [5–95 %] | P(≤ 1) / P(≤ 10) | Upper limit |
|---|---|---|---|---|
| docs/30 tier 2 (capillary bed in the MicruX cell) | 2.1 | 8.4 [1.0–100] | 0.05 / 0.54 | 1400 |
| **this cell, M-280, membrane on screen on washer (4.9 mm² + 0.44 mm² of washer)** | **1.9** | 7.9 [0.96–93] | 0.06 / 0.57 | 1400 |
| retainer 2.3 mm² (low estimate) | 1.7 | 6.9 [0.89–84] | 0.06 / 0.59 | 1400 |
| retainer 11 mm² (high estimate) | 2.4 | 9.6 [1.1–110] | 0.04 / 0.51 | 1400 |
| retainer 40 mm² (a sintered 0.5 µm frit instead) | 5.0 | 17 [1.7–210] | 0.02 / 0.36 | 1400 |
| bed bore 0.3 mm (variant body) | 1.6 | 6.6 [0.86–80] | 0.07 / 0.61 | 1400 |
| 10–14 µm polystyrene beads, same area, screen alone | 1.8 | 7.4 [0.93–88] | 0.06 / 0.58 | 1400 |
| the same, beads bind conjugate like tube-washed M-280 (factor 1) | 1.4 | 5.4 [0.73–62] | 0.09 / 0.67 | 1400 |
| the same, beads bind 10 times that (factor 10) | 3.3 | 13 [1.5–160] | 0.02 / 0.43 | 1400 |
| M-280 behave as when washed in tubes (factor 1) | 1.5 | 5.8 [0.76–68] | 0.08 / 0.64 | 1400 |
| exit bore of 0.15 µL instead of 0.52 µL | 1.9 | 8.1 [0.97–95] | 0.06 / 0.56 | 460 |
| gap 0.05 mm; gap 0.20 mm | 1.9; 1.9 | 7.9; 7.9 | 0.06 / 0.57 | 1400 |
| the substrate's background does not decay | 2.0 | 11 [1.4–120] | 0.02 / 0.47 | 1400 |
| only 1 % of the turnovers electroactive, read as specified | 9.3 | 23 [3.6–250] | 0.00 / 0.25 | 10⁵ |
| the same, sweep at 20 µL/min for 22 s | 4.9 | 20 [2.9–220] | 0.00 / 0.31 | 3.4×10⁴ |
| screened detection reagent and substrate lot (L6 + L7) | 1.3 | 5.5 [0.82–50] | 0.07 / 0.67 | 790 |

Reading.
1. **The cell is worth about 10 % at nominal** (2.1 → 1.9). Of the blank's enzymes in the nominal case, 4.2×10⁴
   sit on the beads and 8.4×10⁴ elsewhere (docs/30: 9.6×10⁴ elsewhere). The transfer line (24 mm²) is still the
   largest wall; it is outside the cell.
2. **The retainer moves the result more than the cell does**: 1.7 to 2.4 over its estimated range.
3. **The dead volume is kept at 0.5 µL on purpose.** A smaller volume between bed and electrode does not lower
   the LOD (1.9), and it lowers the upper limit from 1400 to 460 pg/mL, because the phosphate released with the
   product inhibits the enzyme in the smaller volume (docs/30 §2.4).
4. **The gap does not matter at nominal**, as in docs/33. If only 1 % of the turnovers are electroactive, the
   0.10 mm gap helps: 9.3 instead of the 13 of docs/30 as specified, and 4.9 with a faster sweep (docs/33: 7.4
   for the 0.2 mm cell).
5. With the cell and screened reagents the nominal LOD is 1.3; the criterion of 1 pg/mL is inside the range but
   not at the nominal, as for every design of docs/30.

### 6.2 Pressure drop (`tier2_cell.md` §3; bar)

| Bed | 3.4 µL/min (load) | 50 (conjugate) | 80 (substrate step) | 200 |
|---|---|---|---|---|
| M-280 in the 0.5 mm bore: bed / membrane / screen / total | 0.03 / 0.005 / 0.01 / 0.04 | 0.39 / 0.08 / 0.15 / 0.62 | 0.63 / 0.12 / 0.24 / **0.99** | 1.6 / 0.31 / 0.60 / 2.5 |
| 10–14 µm in the 0.5 mm bore: bed / screen / total | 0.006 / 0.01 / 0.02 | 0.09 / 0.15 / 0.24 | 0.15 / 0.24 / 0.39 | 0.37 / 0.60 / 0.97 |
| M-280 in a 0.2 mm bore, 0.6 mm long (the bed of docs/30), in this cell | 1.1 | 16 | 26 (76 % of 500 psi) | 65 (above the rating) |

Bores, gap and outlet path together stay below 0.001 bar. The membrane and screen figures are estimates
(Hagen–Poiseuille in the pores; UNVERIFIED). Consequences:
* The cell works at about 1 bar. The 500 psi is margin, and it would allow the narrow bed of docs/30 at up to
  80 µL/min.
* The bed is no longer the stiffest spring upstream of the cell, which should make the stop of the read cleaner
  (test T2-2 of docs/30). The restrictor that gives the pump its back-pressure stays upstream of the injector
  (docs/30 §2.3).
* A bed of 0.63 bar is too small to check on the pump's pressure reading. The 0.3 mm variant gives 4.9 bar at
  80 µL/min and can be checked that way (Derived).

### 6.3 Mechanics with the whole liquid path at 500 psi (`tier2_cell.md` §4)

| Quantity | Value |
|---|---|
| Force lifting the plate off the strip (pressure taken out to the outer groove wall) | 234 N |
| Force parting body and plate (the same, 14.3 mm) | 554 N |
| Plate: pushed down by the body–plate pressure and its O-ring, up by the strip pressure and its O-ring; net | 335 N down, so it stays on the base and the M4 screws do not carry the strip load |
| Clamp force of the four M4 screws at 0.25 N·m; carried (body–plate pressure + 12 × 1 O-ring); margin; after 30 % relaxation of the acetal (UNVERIFIED) | 1250 N; 595 N; 2.1; 1.5 |
| The same against every load added (the conservative sum used before); margin | 854 N; 1.5 |
| Margin of the M4 clamp in operation (about 1 bar: the two O-rings only) | 19 |
| Stress under the M4 washers (8 mm, DIN 433, on a ⌀5.5 clearance hole); long-term guide for acetal (UNVERIFIED) | 11.8 MPa; 10 MPa (0.5 N·m would give 24 MPa) |
| Four M2.5 at 0.05 N·m: preload each; stress under the head (⌀4.5, UNVERIFIED, on ⌀3.2) | 100 N; 12.7 MPa |
| What the M2.5 hold with the bed unit off the base (12 × 1 O-ring + retainer washer); margin | 44 N; 9.1 |
| Each M2.5 if the plate screws alone held the body–plate joint at 500 psi; thread strip-out in acetal; margin | 149 N; 848 N; 5.7 |
| Sag of body and plate across the strip pocket | 0.55 µm |
| Deflection of the port floor when the inlet fitting is tightened | 4 µm (4 % of the gap) |
| Thinnest drilled wall (inlet thread to riser) | 1.0 mm |
| Retainer washer: squeeze; force; pressure on the membrane's sealing band (low / nominal / high tolerance) | 11 / 26 / 39 %; 1.4 / 3.2 / 4.7 N; 0.9 / 2.0 / 3.0 MPa |
| Bow of the plate under the washer | ≤ 4.4 µm |
| Force of the flow pushing the stack off the body face, 80 / 200 µL/min (upper bound) | 0.21 / 0.53 N |

Computed for acetal copolymer (re-run 2026-11-18 with the torques of section 4.2): typical values, modulus
2.8 GPa, shear strength 40 MPa, Poisson 0.35, long-term bearing guide 10 MPa, all UNVERIFIED (take them from the
data sheet of the stock); preload from T = 0.2 · d · F (dry threads); the O-ring load is taken as 1 N per mm of ring.

Not covered by these numbers, and to be shown by the proof test: the seal of a 70 Shore A O-ring over the printed
tracks of the strip, and extrusion of that O-ring into a gap of up to 0.15 mm at 34.5 bar (within common design
charts as recalled, UNVERIFIED; a 90 Shore A ring is the remedy).

### 6.4 The retainer with a 1 mm O-ring instead of the washer (not drawn)

If an O-ring is preferred to a punched washer, a cross-section of 1 mm (sizes such as 1 × 1 mm are common in
assortments, UNVERIFIED) can be the spring, in the same place:

| | Washer (chosen) | O-ring 1 × 1 |
|---|---|---|
| Screen | 1/16 in (2SR1-10) | 1/8 in (VICI 2SR2-10 [V], ⌀3.175 × 0.075): it has to cover the ring |
| Membrane | ⌀1.5 | ⌀3.0 |
| Pocket | ⌀1.68 × 0.27 | stepped: ⌀3.25 × 0.09 for screen and membrane, then a ring groove ⌀3.1 × 0.84 deep |
| What fills the ring's bore | nothing (washer hole 0.08 µL) | a PEEK boss ⌀1.0 left standing in the groove, its top 0.095 below the face, the exit bore through it; without the boss the ring's bore adds 0.6 µL and 2.4 mm² of elastomer to the dead volume |
| Thinnest wall | 1.0 mm | 0.25 mm (the boss around the 0.5 mm bore), below the 0.5 mm Xometry recommends |
| Land between pocket and cross channel | 1.4 mm | 0.6 mm |
| Spring force; plate bow | 3.2 N; ≤ 3.3 µm | about 6 N (1 N per mm of ring, UNVERIFIED); about 4 µm |
| Screen and membrane outside the flow, where conjugate collects | small | about 5 times more |

It can be done, but every line favours the washer. If punching washers proves awkward, they can be bought as
die-cut parts from a gasket cutter (not checked).

**The 0.3 mm variant.** A second body with the last 0.6 mm of the bed bore at 0.3 mm (the rest stays 0.5 mm)
cuts the retainer area to a third: 1.6 instead of 1.9 pg/mL, and a bed that can be checked by pressure. A 0.3 mm
hole is below the feature size Xometry recommends and belongs to its micro-machining service. `BED_D` in
`params.py` changes the model; the stepped bore is not drawn.

## 7. Use

1. **Assemble the bed unit once per bed.** Nozzle plate top face up: washer, then screen, then membrane into the
   retainer pocket (tweezers; wet with assay buffer so they lie flat); O-ring 12 × 1 into the body's groove; body
   on, located by two loose pins; four M2.5 screws from below, crosswise, to 0.05 N·m. Check that the membrane top is level with
   the plate face before the body goes on (it may stand up to 0.07 mm above it; the body pushes it down).
2. **Pack.** Connect a packing line (1/16 in tube holding at least 25 µL) to the inlet port and push the bead
   suspension of docs/30 §4.2 (1.5 µL of coated M-280 in 20 µL of assay buffer) through at 20–50 µL/min, then
   assay buffer at 80 µL/min for 1 min. Never above 80 µL/min through the bed (section 3.1). The beads collect on the membrane at the bottom of the bore. Check by
   looking down the port bore with a stereo microscope; the body is opaque, so the bed cannot be seen from the side.
3. **Mount.** Once per base: measure the pocket depth with a depth micrometer and cut the shim stack to
   depth − 0.38 − 0.10. Shim and a fresh strip into the base pocket against its stop, O-ring 7 × 1 into the plate, the bed
   unit onto the pins, four M4 screws crosswise, first to 0.1 N·m, then to 0.25 N·m. Connect the transfer line and
   the cable. Before a run at high pressure (test C-1) check the M4 torque again after an hour: acetal relaxes.
4. **Run** the unchanged step table of docs/30 §4.3, with its pre-run on the fresh bed and strip.
5. **After the run.** Take the bed unit off and flush the beads out of the inlet port from the exit bore, or open
   the four M2.5 screws and rinse. Fit a new washer, screen and membrane. Body and plate are used again, so their walls
   carry the conjugate of the run before; the pre-run of docs/30 measures what is left, and a cleaning step has
   to be found (test C-5).

Two or three bed units (body, plate, screws) allow beds to be packed ahead; one base is enough.

Back-pressure. The cell would tolerate a restrictor at its outlet, for instance to keep bubbles in solution
during the stop. docs/28 advised against that for the MicruX add-on. It is not part of the design, because any
pressure in the cell is released through the bed when the flow stops.

## 8. What is not known, tests, and choices

### 8.1 Tests of the cell (in addition to T2-1 … T2-5 of docs/30 §4.6, which apply unchanged)

| # | Test | Decides | Pass |
|---|---|---|---|
| C-1 | Proof test: blank strip, outlet plugged, pump at 10 µL/min with its pressure limit at 750 psi; hold 10 min at 500 psi; repeat on a printed strip | whether the strip seal holds 500 psi | no drop, no weeping |
| C-2 | Retention: pack M-280 at 80 µL/min, then run 200 µL/min to find the margin, collect the outflow on a magnet, inspect the strip | whether the membrane on the screen holds the beads | no beads downstream |
| C-3 | Gap: the two electrochemical readings of docs/33 §6.2 (limiting current at 5 µL/min; charge in the stopped cell) | the gap as built | 0.05–0.15 mm |
| C-4 | Empty cell with retainer, no beads, through conjugate, wash, substrate, stop and sweep (the empty arm of T2-1) | the conjugate on retainer and walls; the largest unknown of section 6.1 | walls and retainer ≤ 2 × beads (the criterion of T2-1) |
| C-5 | The same sequence twice on one body and plate with a cleaning step between; candidates for the step are not chosen | carry-over of conjugate on the re-used parts | second pre-run within 10 % of the first |
| C-6 | Ten beds, 100 pg/mL (T2-4) | packing in a bed only 35 layers deep | signal CV ≤ 10 % |

### 8.2 Limits of this document

* Not reviewed by a second party, unlike docs/30. The CAD checks are the model's own (interference, connected
  liquid path, wall thicknesses).
* The retainer areas, the surface factor of membrane and screen (10, range 1–100, the kit's frit factor), the
  pressure drop of membrane and screen and every PEEK property are UNVERIFIED.
* A bed 0.10 mm deep in a 0.5 mm bore is treated like the long bed of docs/30. The kit has no term for uneven
  packing or for flow that by-passes a shallow bed; test C-6 addresses it.
* The radial outflow relies on the collecting groove; its 25 % asymmetry is not in the kit.
* The washer's force rests on a rubber modulus and a shape-factor formula (UNVERIFIED), and its squeeze on the
  tolerance of punched sheet. Test C-2 shows whether the membrane seals; a washer that has taken a set must be
  replaced with every bed in any case.
* The drawings are generated and were checked by eye against the model only; they carry no checker's or
  approver's name. A person should check them before an order.
* The thin-film chips (10 × 6 × 0.7 mm glass) would need another base and a smaller O-ring; not designed.

### 8.3 Choices the user may overrule, and questions

1. **Beads**: M-280 with a membrane on the screen (chosen), or 10–14 µm polystyrene with the screen alone?
2. **Bore**: 0.5 mm throughout (chosen; standard machining), or the 0.3 mm variant body as well?
3. **Rating**: is 500 psi wanted for the bed side only, or for the whole cell including the strip seal? The
   design takes the second, stricter reading.
4. **Gap**: 0.10 mm (chosen) or 0.05 mm by a thicker shim?
5. **Body material**: acetal copolymer (chosen 2026-11-18, opaque; PEEK fallback). An acrylic body for low-pressure trials only would show the bed packing. A polished polyetherimide body would let the bed be seen from the
   side; its resistance to the pH 9.5 buffer over months was not checked.
6. Settled: ceramic strips, 0.38 mm; the drawing's dimensions are accurate (the user, 2026-11-18).
7. Whether this cell replaces the capillary in docs/30 §4, and whether tests C-1 … C-6 enter the bench plan, is
   the user's decision. docs/30 and docs/06 are not changed.

## 9. Sources

In the repository: docs/28 (MicruX cell, strips, fittings, beads), docs/30 §4 (tier 2), docs/31 (findings C6,
C7), docs/33 (cell geometry).

Opened or searched in this session:

| Key | Document | Evidence | Used for |
|---|---|---|---|
| VICI-screens | Valco Instruments catalogue page "Frits • Screens • for filters" (p. 40), https://analytics-shop.com/media/pdfs/VC-10FR1-10.pdf ; https://vici.com/vfit/screens.php | [V], text of the PDF read | part numbers, thicknesses, nominal against absolute retention |
| Xometry-precision | https://www.xometry.com/capabilities/cnc-machining-service/precision-cnc-machining/ | [S] | 0.5 mm feature size |
| Xometry-tolerances | https://www.xometry.com/resources/blog/tight-tolerances/ ; https://www.xometry.com/resources/machining/what-every-designer-needs-to-know-about-cnc-part-tolerances/ | [S] | standard and tight tolerances |
| Xometry-depth | Xometry Europe design page, https://xometry.eu/en/?p=1161 | [S] | hole depth |
| Xometry-micro | https://www.xometry.com/capabilities/cnc-machining-service/micro-machining-service/ | [V] | cutters below 0.010 in; PEEK listed |
| IDEX-XP235 | https://www.idex-hs.com/store/product-detail/flangeless_fitting_short_peek_1_4_28_flat_bottom_for_1_16_od_natural_single/xp-235 | [V] | 2000 psi with the P-200 ferrule; part obsolete |
| IDEX-ports | https://idex-hs.com/resources/tools-drawings/standard-port-drawings | [V] | a 1/4-28 flat-bottom port drawing exists behind registration; the port dimensions used are from the drawing the user supplied |
| Thermo-M270 | Thermo Fisher and Fisher product pages for Dynabeads M-270 and M-280 Streptavidin (e.g. https://www.thermofisher.com/order/catalog/product/65305) | [S] | surface chemistry of the two beads |
| Spherotech | https://spherotech.com/coa_pol_par.htm and the catalogue PDF of coated polystyrene particles | [S] | SVP-100-4, 10.0–14.0 µm, 0.5 % w/v |
| Sterlitech | https://www.sterlitech.com/hydrophilic-polycarbonate-membrane-filters ; FAQ on PCTE membranes | [S] | PCT1013100; thickness 6–15 µm; PVP coating |
| GVS-PCTE | GVS specification sheet for hydrophilic PCTE membranes | [S] | 2×10⁷ pores/cm² at 1 µm |

No price, lead time or stock status was taken from any of these.

## 10. Record of this follow-up

* Request as quoted at the top. No question was put to the user; the open choices are in section 8.3.
* Done by the orchestrator alone: `cad/elisa_cad/tier2_cell/` (new: `params.py`, `parts.py`, `section.py`,
  `build.py`), `cad/out/tier2_cell/` (new), `scripts/tier_round/tier2_cell.py` (new),
  `results/tier_round/tier2_cell.md` and `.json` (new), this document, lines in `scripts/tier_round/README.md`
  and `cad/README.md`, a section in docs/32, and the project guide. No agent, no review.
* Not changed: `tierkit.py`, `designs.py`, `run_tiers.py`, `tier_params.yaml`, `src/`, `params/`, docs/26–31,
  docs/33, the other CAD packages, the deck.
* On the way. The first layout took a 1 µm or 2 µm stainless screen as the retainer; the vendor's own catalogue
  page then showed that those ratings are nominal, and the membrane was added. The first layouts kept the 0.2 mm
  bed of docs/30, which needs micro-drilling; the kit showed that the bore does not change capture, and every
  hole became 0.5 mm. A spigot on the body that reached down to the electrode, and a single body with a pressed-in
  nozzle, were dropped for the three-part stack. Revision B: asked how the bed bore and the exit bore are sealed,
  the orchestrator found that the first version's pinched screen had no defined force, opened a film between body
  and plate and bowed the plate; it proposed an O-ring of 0.5 mm cross-section around the bore. Working it out
  showed that this needs a land beside the bore that brings the same problems back, and the user then pointed out
  that 0.5 mm O-rings are hard to get. The washer in a pocket of the plate replaced both. In the first CAD build the O-rings were drawn round and cut into
  their neighbours (now drawn at their compressed height), and the body riser was 9.2 diameters deep (now 1.0 mm
  wide, 7.5 diameters).
