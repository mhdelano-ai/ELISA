# 33 — Flow-cell geometries: which shape of cell gives the lowest LOD

Status: 2026-11-18. Follow-up to the tier round (docs/26–32) on the user's request "Explore other flow cell
geometries and pick the best one." Written by the orchestrator without agents. Calculations:
`scripts/tier_round/cell_geometries.py` → `results/tier_round/cell_geometries.md`, `cell_geometries.json`
(18 checks pass). **Not independently reviewed**, unlike docs/30.

How to read the numbers. Every LOD is a model prediction with the kit and parameters of docs/30, not a
measurement. "Nominal" = all parameters at their best estimate; "median [5–95 %]" = Monte Carlo over the parameter
bounds (n = 2000, seed 20261111), a scenario range and not a confidence interval. Each candidate cell replaces the
cell and the electrode in the unchanged designs of docs/30, so the tables compare geometries, not assays. Dimensions
of cells other than the MicruX cells are design inputs, **UNVERIFIED** unless a source is named, and are not
sampled. The result tables are pasted from `python scripts/tier_round/cell_geometries.py --doc`.

Terms: **gap** = height of the liquid layer over the working electrode. **Stream** = liquid arriving at the
electrode from upstream, as opposed to product made on the electrode itself. Scenario names as in docs/30:
"substrate background persists" = the free hydroquinone of the substrate does not decay before use (docs/31 C5,
M2); "1 % electroactive" = only 1 % of the enzyme turnovers give a product the electrode oxidises (docs/31 C1).

## 0. Summary

**The pick: a radial thin-layer cell. The stream enters through a bore centred over the working electrode and
leaves radially through a gap of about 50 µm (25–100 µm), over the 3 mm strip electrode.** This is the shape of the
MicruX flow add-ons already in hand. What has to change, or be confirmed, is the gap: docs/30 takes 0.2 mm, the
vendor's volume implies ≤ 0.1 mm, and it has not been measured (docs/28 §1.3).

| | Cell of docs/30 (gap 0.2 mm taken) | **Pick: same shape, gap 50 µm** | Best other shape | Worst shape tried (tier 1: at the same 50 µm gap) |
|---|---|---|---|---|
| Tier 1, LOD nominal; median (pg/mL) | 3.6; 16 [2.8–110] | **2.3; 12 [2.0–95]** | cross-flow channel with the electrode as the first surface: 2.3; 12 | cross-flow channel 5 mm wide, electrode 2 mm downstream: 4.1; 19 |
| Tier 1 with the read at 500 µL/min | 2.9 | **1.8** | 1.7 | 3.4 |
| Tier 2, LOD nominal; median | 2.1; 8.4 [1.0–100] | **2.1; 8.4** | any thin-layer cell: 2.1–2.3 | free wall jet, large gap: 3.3; 13 |
| Tier 3 (one valve), LOD nominal; median | 1.2; 5.1 [0.78–58] | **1.2; 4.9** | any thin-layer cell: 1.2–1.3 | free wall jet, large gap: 3.7; 11 |
| Tier 3 if only 1 % of the turnovers are electroactive, best sweep | 11 | **5.0** | cross-flow channel, 13 µm gasket: 2.9 | free wall jet: 85 |

What the comparison shows.
* **The shape matters less than two numbers: the gap, and what lies upstream of the electrode.** A cross-flow
  channel and the radial cell give the same capture and the same conversion at the same gap and electrode area.
  They differ only in what the stream passes before it reaches the electrode.
* **Where the electrode is the capture surface (tier 1), a thinner gap is worth a factor of 1.6**: 3.6 → 2.3 pg/mL
  at 50 µm, because the electrode takes 16 % of the sample instead of 8 %. Below 50 µm the gain stops (2.2 at
  25 µm). The radial cell is the right shape for this job because the stream meets the electrode first. In a
  channel with 2 mm of unblocked floor ahead of the electrode, half of that floor's product reaches the electrode
  and the gain is lost (3.6 at 50 µm).
* **Where the cell only detects the product of a bed (tiers 2 and 3), no geometry lowers the nominal LOD.** Every
  thin-layer cell gives 1.2–1.3 (one valve) and 2.1–2.3 (tier 2), and so does a detector that oxidises every
  molecule.
  The blank is conjugate on the bed and its walls; a better detector multiplies signal and blank alike.
* **The gap does matter in those tiers if the signal turns out weak.** With 1 % electroactive turnovers the read
  is limited by drift and noise. A 50 µm gap with a sweep at 20 µL/min then gives 5.0 instead of 20 pg/mL (tier 3)
  and 3.7 instead of 13 (tier 2).
* **Two shapes to avoid**: a wall-jet cell with a large gap (about 5 % of the product oxidised; 3 times worse in
  tier 3 and 1.6 times in tier 2), and a porous flow-through electrode (no gain at nominal, 1.4–2 times worse if
  the substrate background persists, and it needs ≥ 300 µL/min).
* **No other cell needs to be bought for the LOD.** None of the commercial cells of docs/02 §5 beats the cell in
  hand once its gap is thin.

The effect is modest. Cell geometry moves tier 1 by 1.6 at nominal and leaves tiers 2 and 3 where they were; in
16 % of the Monte Carlo draws the thin gap is worse for tier 1 than the 0.2 mm gap (section 4.1, point 7).
The detection reagent's off-rate and the conjugate's non-specific binding each move every tier by more
(docs/30 §6.2). None of this changes the recommendation of docs/30 (the two chemistry questions first, then
tier 2, then one valve).

**What to do at the bench**: measure the gap of the cell in hand (already instrument check 4 of docs/27 §9;
section 6.2 adds two electrochemical readings), and ask MicruX whether the add-on can be had or shimmed to
50–100 µm (section 8).

## 1. What the cell has to do

The cell has two different jobs in the designs of docs/30.

* **Role A — tier 1.** The working electrode is the capture surface. The whole sample flows over it at
  2.9 µL/min for 44 min, then conjugate, then substrate at 200 µL/min while the electrode reads the product of its
  own enzyme. Two properties of the geometry count. The first is the mass-transfer coefficient to the electrode at
  the slow load flow, which sets how much IgG is captured per area. The second is the fraction of the *stream*
  the electrode oxidises at the fast read flow, which sets how much product of the conjugate on upstream walls,
  and how much free hydroquinone, is read along with the signal. A good cell is high on the first and low on the
  second.
* **Role B — tiers 2 and 3.** The cell is only a detector. Product collects in the stopped bed and is then swept
  over the electrode as a plug. The geometry sets the fraction of the plug that is oxidised and the electrode
  area, which sets noise and drift.

**"Wall jet" in docs/28 and docs/30 is the vendor's word; at the flows of this assay the MicruX cells are radial
thin-layer cells.** The liquid fills the gap and moves outward in creeping flow (kit README B; reduced Reynolds
number Q·h/(2π·r²·ν) at the bore edge: 0.75 for 0.2 mm at 200 µL/min, 0.19 for 50 µm; Derived). A *free* wall
jet is a different regime: a jet strikes a wall in a chamber much deeper than its boundary layer, and the
limiting current follows the Yamada–Matsuda equation. The model of docs/03 treats its "confined wall-jet"
detector with that equation, which gives a few per cent conversion (2–3 % for a 2 mm electrode at
5–20 µL/min; Derived), and docs/05 §1.2 ranks that detector 3–6 times behind the best one, where thin-layer
cells are 1.1–1.5 times behind. A ranking obtained with the free-jet equation does not carry over to a thin gap.
Section 5 has both: the adjustable confined cell as a radial thin layer, and a large-gap cell with the wall-jet
equation.

## 2. Candidates

| # | Shape | Commercial examples and what is known | Role A | Role B | How it is evaluated here |
|---|---|---|---|---|---|
| 1 | **Radial thin gap**: inlet bore centred over the electrode, radial outflow | MicruX AIO-SPE flow add-on: 0.8 mm bore, 8 mm O-ring, < 5 µL, gap not published, 0.1–0.5 mm bounded (docs/28 §1 [V], bounds UNVERIFIED). MicruX thin-film add-on FC-2.0: 0.5 mm bore, 2 mm O-ring, < 0.5 µL (docs/28 [V]). Antec SenCell: confined wall jet with an adjustable spacer, working volume ≈ 0–300 nL [V], 2 mm electrode [S] (docs/02 §5) | yes, with the strips and chips in hand | yes | kit, `flow_geometry="radial"`, gaps 0.5–0.025 mm. SenCell type: gap 32 µm from 100 nL over a 2 mm disc (Derived; that the working volume is the disc over the electrode is UNVERIFIED) |
| 2 | **Cross-flow thin-layer channel** | BASi cell, 3 mm glassy carbon, gaskets 13, 51, 127 µm [S]; Antec VT-03, 25/50 µm spacers [S]; Metrohm thin-layer cell, < 0.35 µL with a 50 µm spacer [V] (all docs/02 §5). MicruX "Thin Layer PMMA-1.0" add-on: listed by PalmSens only, no geometry (docs/28 §1.1 [V]) | only with a strip or chip as the electrode: a custom part, or the MicruX thin-layer add-on if it exists | yes | kit, `flow_geometry="channel"`. Role A: electrode spanning the channel, at the entrance or 2 mm downstream; walls ahead of the electrode by the solver of section 3. Role B: 3 mm disc in a 3 mm channel (width UNVERIFIED, `ma.geometry.thin_layer_channel_width`) |
| 3 | **Free wall jet, large gap** | Metrohm DropSens DRP-FLWCL-PEEK, wall-jet cell for printed electrodes, dimensions not stated (docs/02 §5 [V]) | no (capture needs a thin layer) | yes | wall-jet equation of the model (`transport.wall_jet_conversion`; coefficient recalled, nozzle 0.3 mm UNVERIFIED). Outside its validity at 5–100 µL/min: the number is an indication only |
| 4 | **Porous flow-through electrode** | Thermo Dionex 6011RS: porous graphite, 4.3 µL, "near 100 %" conversion, usable above 0.3 mL/min (docs/02 §5 [V]); wiring to a Gamry UNVERIFIED | no | yes | stated conversion 0.95; wetted area 100 mm² (30–1000, UNVERIFIED, `ma.geometry.coulometric_effective_area`); swept at ≥ 300 µL/min |
| 5 | **Tubular electrode** | none identified | transport figures only (section 4.2) | — | exact tube solution of the model |
| 6 | **Porous or packed capture electrode** (the bed is the electrode) | none identified | transport figures only (section 4.2) | — | bed equation of the kit |
| 7 | **Interdigitated array** in the thin-film cell | MicruX IDA and IDRA chips: redox-cycling factors 2.0–3.0 by the vendor (docs/28 §2.2 [V]); needs a second potentiostat channel | — | not run | argument only (section 5.3) |
| — | **Bound** | — | — | yes | every product molecule oxidised, on a 3 mm and on a 1 mm electrode |

## 3. Method

Each candidate is put into `run_tiers.t1()`, `t2()` and `t3v()` (tier 1, tier 2, tier 3 with one valve) by
replacing `design["cell"]` and `design["electrode"]`. Reagents, flows, times, beds and walls stay as in docs/30.
`tierkit.py`, `src/` and `params/` are not edited. The unchanged designs reproduce `tiers.json` (checks).

Two things are added.

1. **Walls of a channel ahead of the electrode (role A).** The fast-flow read of the kit counts no floor,
   because in the radial cell the stream arrives on the electrode first. In a channel, the floor and the lid
   between the inlet and the electrode have seen conjugate. Their product is released next to the wall, not
   mixed into the stream. `slit_wall_source()` solves the convection–diffusion equation of the slit for a wall
   that releases product uniformly, followed by a perfect sink. It gives the fraction the electrode collects:
   0.50–0.52 from the floor and 0.00–0.07 from the lid for 2 mm of channel ahead of a 2.66 mm electrode at
   200 µL/min. This enters the kit through the existing hook for upstream walls, as an equivalent area. The
   floor is counted at the surface factor of the strip around the electrode (10), the lid at the lid factor (3).
   In the Monte Carlo the equivalent area carries the tubing factor's distribution (1–30), not the floor's
   (1–100); both are UNVERIFIED.
2. **Two detectors the kit does not have (role B)**: a stated conversion (porous electrode, bound) and the free
   wall-jet equation. `tierkit.cell_conversion` is wrapped, not edited.

**Read window in role B.** docs/30 sweeps 7.5 µL at 5 µL/min in 90 s. For the weak-signal scenario the sweep flow
is re-chosen for every detector over 2–100 µL/min at the same swept volume (plus twice the detector's own
volume), with a window of at least 6 s and the result within 60 min.

**Bed position in tier 2.** In the radial MicruX cells the capillary tip sits in the cell's straight inlet bore,
1 mm above the chamber, as in docs/30 ("tip"). For every other cell the bed is taken to sit in a fitting on the
inlet port, with the whole inlet passage between bed and electrode ("port"; passage taken as 0.8 mm × 5 mm,
UNVERIFIED). In tier 3 the bed is in the valve loop and this does not arise.

**Checks** (`results/tier_round/cell_geometries.md` §0, 18 of 18 pass): the solver reproduces the model's slit
conversion within 0.3 % at three lengths; it conserves mass to 10⁻⁹; the collected fractions change by less than
2 % on a grid twice as fine; a very long sink collects everything; in the thin-boundary-layer limit it gives 0.45
against 0.41 for the textbook double-channel electrode, whose generator is at uniform concentration and not at
uniform flux (formula recalled, UNVERIFIED; plausibility only); the unchanged designs and the base cases of this
script reproduce the three LODs of `tiers.json` to 10⁻⁶.

## 4. Role A: the electrode is the capture surface (tier 1)

### 4.1 Results

Tier 1 of docs/30 (printed gold strip with a biotin-OEG monolayer, or thin-film gold chip; load 2.86 µL/min for
44 min; 20 nM conjugate; read 60 s under substrate flow) with another cell. Time to result 57.1 min with the
read at 200 µL/min, 55.9 min at 500 µL/min. All LODs in pg/mL.

| Cell | gap (µm) | IgG of the vial captured (%) | product of the stream oxidised at 200 µL/min (%) | LOD nominal, read at 200 µL/min | median [5–95 %] | P(≤ 1) / P(≤ 10) | nominal, read at 500 µL/min | substrate background persists | 1 % of turnovers electroactive |
|---|---|---|---|---|---|---|---|---|---|
| radial thin gap (wall-jet inlet), MicruX strip cell, 3 mm gold | 500 | 4.9 | 3.3 | **5.6** | 22 [3.9–160] | 0.00 / 0.23 | 4.5 | 7 | 330 |
| radial thin gap (wall-jet inlet), MicruX strip cell, 3 mm gold (docs/30) | 200 | 8.2 | 6.1 | **3.6** | 16 [2.8–110] | 0.00 / 0.33 | 2.9 | 5.9 | 200 |
| radial thin gap (wall-jet inlet), MicruX strip cell, 3 mm gold | 100 | 11.8 | 9.6 | **2.8** | 13 [2.3–100] | 0.01 / 0.39 | 2.2 | 5.8 | 140 |
| radial thin gap (wall-jet inlet), MicruX strip cell, 3 mm gold | 50 | 16.1 | 15.0 | **2.3** | 12 [2–95] | 0.01 / 0.42 | 1.8 | 6.3 | 100 |
| radial thin gap (wall-jet inlet), MicruX strip cell, 3 mm gold | 25 | 20.9 | 23.5 | **2.2** | 13 [2–100] | 0.01 / 0.42 | 1.6 | 7.3 | 78 |
| radial thin gap (wall-jet inlet), MicruX thin-film cell, 1 mm gold (docs/30) | 160 | 1.5 | 1.4 | **4.1** | 21 [3.3–160] | 0.00 / 0.27 | 2.8 | 7.2 | 350 |
| radial thin gap (wall-jet inlet), MicruX thin-film cell, 1 mm gold | 50 | 2.3 | 3.1 | **3.1** | 19 [2.9–150] | 0.00 / 0.31 | 2.1 | 8.9 | 230 |
| radial thin gap (wall-jet inlet), MicruX thin-film cell, 1 mm gold | 25 | 2.8 | 4.9 | **3** | 20 [3–170] | 0.00 / 0.29 | 2 | 11 | 200 |
| cross-flow channel 2.7 mm wide, 3 mm gold, electrode at the channel entrance | 100 | 12.4 | 10.1 | **2.7** | 13 [2.2–96] | 0.01 / 0.40 | 2.1 | 5.7 | 130 |
| cross-flow channel 2.7 mm wide, 3 mm gold, electrode at the channel entrance | 50 | 17.1 | 15.8 | **2.3** | 12 [2–91] | 0.01 / 0.43 | 1.7 | 6.2 | 95 |
| cross-flow channel 2.7 mm wide, 3 mm gold, electrode at the channel entrance | 25 | 22.2 | 24.6 | **2.1** | 12 [1.9–99] | 0.01 / 0.44 | 1.5 | 7.2 | 74 |
| cross-flow channel 2.7 mm wide, 3 mm gold, electrode 2 mm downstream of the inlet | 100 | 12.4 | 10.1 | **4.4** | 20 [3.3–150] | 0.00 / 0.28 | 3.8 | 6.7 | 130 |
| cross-flow channel 2.7 mm wide, 3 mm gold, electrode 2 mm downstream of the inlet | 50 | 17.1 | 15.8 | **3.6** | 17 [2.8–140] | 0.00 / 0.32 | 3 | 6.8 | 95 |
| cross-flow channel 2.7 mm wide, 3 mm gold, electrode 2 mm downstream of the inlet | 25 | 22.2 | 24.6 | **3.2** | 16 [2.5–150] | 0.01 / 0.34 | 2.5 | 7.6 | 74 |
| cross-flow channel 5.0 mm wide, 3 mm gold, electrode 2 mm downstream of the inlet | 50 | 14.5 | 12.6 | **4.1** | 19 [3.1–150] | 0.00 / 0.29 | 3.4 | 6.8 | 110 |

Reading.
1. **Gap.** From 0.5 to 0.05 mm the captured share rises from 4.9 to 16 % and the nominal LOD falls from 5.6 to
   2.3. The mass-transfer coefficient scales with gap^(−2/3) until it meets the reaction velocity of the capture
   layer (k_r = 4.2 µm/s); at 25 µm it is 3.2 µm/s and little is left to gain. At the same time the electrode
   oxidises more of the stream (6 % → 24 % at 200 µL/min), so the product of the conjugate on the inlet bore and
   the transfer line counts more. Below about 50 µm the second effect takes most of what the first still gives
   (2.3 → 2.2).
2. **Radial against channel.** With the electrode as the first surface the channel equals the radial cell (2.3
   and 2.3 at 50 µm; the few per cent between them are the area under the bore, which the radial mapping leaves
   out). With 2 mm of floor and lid ahead of the electrode it is 1.5–1.6 times worse (3.6), and a channel wider
   than the electrode is worse again (4.1), because part of the sample passes beside the electrode. A floor
   passivated like the electrode would shrink the penalty; that is a property of the strip, not of the cell.
3. **Electrode size.** The 1 mm thin-film electrode has the higher mass-transfer coefficient (3.9 against
   2.1 µm/s at 50 µm) but a ninth of the area. Its read is limited by drift, and it stays behind the 3 mm strip
   at every gap (3.1 against 2.3).
4. **Read flow.** A faster read lowers the stream's share: 1.8 at 500 µL/min with a 50 µm gap. The pressure drop
   over the chamber stays below 0.3 kPa (Derived; laminar), and the thin gap keeps the flow creeping (reduced
   Reynolds number 0.47). It costs about 0.3 mL more substrate solution per determination (Derived). This is an
   operating point, not a geometry; docs/30 §3.5 already notes the trend.
5. **If the substrate background persists**, the gain of the thin gap is gone: 5.9 at 0.2 mm, 5.8 at 0.1 mm,
   6.3 at 50 µm, 7.3 at 25 µm. The electrode then reads more free hydroquinone with the stream. This is the
   reason for 50–100 µm and not "as thin as possible".
6. **If the signal is weak** (1 % electroactive), the thin gap helps by its full capture ratio: 200 → 100 pg/mL.
7. **The gain is not uniform over the parameter draws.** The Monte Carlo median moves less than the nominal
   value (16 → 12). Draw by draw, the LOD at 50 µm is 0.75 times the LOD at 0.2 mm in the median
   [0.54–1.20]; the thin gap is worse in 16 % of the draws, and worse or less than 10 % better in
   27 %. It helps most where capture is fast (correlation of the ratio with the capture on-rate
   −0.42, with the site density −0.36) and least where the walls upstream bind much conjugate (tubing
   factor +0.26) (`cell_geometries.md` §1a).

### 4.2 Other shapes: transport only

For shapes the planar format of the kit cannot evaluate, the table gives the mean flux to the capture surface per
unit inlet concentration, k_eff = captured fraction × flow / area, at the load flow of tier 1. The specific
label per area of electrode scales with k_eff, and so does its ratio to the non-specific label on the same
surface. The ceiling is k_r = 4.2 µm/s.

| Shape | area (mm²) | captured of what enters (%) | k_eff (µm/s) | k_eff / k_r | product of the stream oxidised at 200 µL/min (%) |
|---|---|---|---|---|---|
| radial thin gap 200 µm over a 3 mm disc | 7.07 | 10.4 | 0.70 | 0.17 | 6.1 |
| radial thin gap 25 µm over a 3 mm disc | 7.07 | 26.5 | 1.79 | 0.42 | 23.5 |
| tubular electrode, bore 0.25 mm, length 9.0 mm (no part identified) | 7.07 | 14.1 | 0.95 | 0.22 | 9.0 |
| tubular electrode, bore 0.25 mm, length 1.0 mm (no part identified) | 0.785 | 2.8 | 1.68 | 0.40 | 2.2 |
| tubular electrode, bore 0.10 mm, length 22.5 mm (no part identified) | 7.07 | 21.2 | 1.43 | 0.34 | 15.9 |
| tubular electrode, bore 0.10 mm, length 2.5 mm (no part identified) | 0.785 | 3.8 | 2.32 | 0.55 | 4.0 |
| porous or packed electrode with the surface of the tier-2 bed, at 3.4 µL/min (no part identified) | 24.4 | 83.2 | 1.93 | 0.46 | 100.0 |

* **A tubular electrode** of the same area is no better than a thin gap (1.4 against 1.8 µm/s for a 0.1 mm bore
  against a 25 µm gap), there is no catalogue part, and its inner wall cannot be inspected or coated as a strip
  can.
* **A porous or packed capture electrode** takes most of the sample (83 %), but per area it is where the 25 µm
  gap is (1.9 against 1.8 µm/s), because the sample is depleted along it. And it oxidises all of the stream at
  any flow. Tier 1 gets its selectivity from an electrode that collects its own product in full and the
  stream's only in part; a porous electrode gives that up, and every conjugate-coated wall upstream counts in
  full. Behind a valve it would be tier 3 with the bed as the electrode, with no gain over the bed formats by
  the model and no part to buy.

## 5. Role B: the cell detects the product of a bed (tiers 2 and 3)

### 5.1 Tier 3, the bed in the loop of one valve

| Detector | electrode (mm²) | product oxidised at 5 / 50 µL/min (%) | LOD nominal | median [5–95 %] | P(≤ 1) / P(≤ 10) | substrate background persists | 1 % electroactive: as specified | 1 %: best sweep (µL/min) | 1 %, best sweep: median [5–95 %] |
|---|---|---|---|---|---|---|---|---|---|
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.5 mm | 7.07 | 36 / 8 | **1.3** | 5.2 [0.83–58] | 0.08 / 0.68 | 1.3 | 35 | 20 (20) | 39 [5.9–410] |
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.2 mm (docs/30) | 7.07 | 62 / 15 | **1.2** | 5.1 [0.78–58] | 0.09 / 0.69 | 1.3 | 20 | 11 (20) | 25 [3.7–260] |
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.1 mm | 7.07 | 84 / 23 | **1.2** | 5 [0.76–58] | 0.10 / 0.69 | 1.3 | 15 | 7.3 (20) | 19 [2.9–190] |
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.05 mm | 7.07 | 97 / 36 | **1.2** | 4.9 [0.76–58] | 0.10 / 0.69 | 1.3 | 13 | 5 (20) | 15 [2.3–150] |
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.025 mm | 7.07 | 100 / 55 | **1.2** | 4.9 [0.76–58] | 0.10 / 0.69 | 1.3 | 13 | 3.7 (50) | 13 [1.9–140] |
| radial thin gap, MicruX thin-film cell, 1 mm electrode, gap 0.16 mm | 0.785 | 16 / 4 | **1.3** | 5.1 [0.82–58] | 0.08 / 0.68 | 1.3 | 26 | 15 (20) | 32 [4.8–340] |
| radial thin gap, MicruX thin-film cell, 1 mm electrode, gap 0.05 mm | 0.785 | 34 / 8 | **1.2** | 5 [0.76–58] | 0.10 / 0.69 | 1.3 | 12 | 7.3 (20) | 19 [2.9–200] |
| radial thin gap, MicruX thin-film cell, 1 mm electrode, gap 0.025 mm | 0.785 | 52 / 12 | **1.2** | 4.9 [0.73–58] | 0.10 / 0.69 | 1.3 | 8.2 | 4.7 (20) | 15 [2.3–150] |
| radial thin gap, adjustable (Antec SenCell type): 2 mm glassy carbon, working volume 100 nL = gap 32 µm | 3.14 | 93 / 30 | **1.2** | 4.9 [0.73–58] | 0.10 / 0.69 | 1.3 | 9.1 | 4 (20) | 13 [2–140] |
| cross-flow thin-layer channel (BASi type): 3 mm glassy carbon, gasket 127 µm, channel 3 mm wide | 7.07 | 73 / 20 | **1.2** | 5 [0.77–58] | 0.09 / 0.69 | 1.3 | 17 | 8.5 (20) | 21 [3.1–210] |
| cross-flow thin-layer channel (BASi type): 3 mm glassy carbon, gasket 51 µm, channel 3 mm wide | 7.07 | 87 / 36 | **1.2** | 5 [0.76–58] | 0.10 / 0.69 | 1.3 | 14 | 5.1 (20) | 15 [2.3–160] |
| cross-flow thin-layer channel (BASi type): 3 mm glassy carbon, gasket 13 µm, channel 3 mm wide | 7.07 | 89 / 73 | **1.2** | 5 [0.76–58] | 0.10 / 0.69 | 1.3 | 14 | 2.9 (50) | 11 [1.7–130] |
| free wall jet, large gap (DropSens FLWCL type): 4 mm printed carbon, nozzle 0.3 mm; wall-jet equation, outside its validity at these flows | 12.6 | 5 / 3 | **3.7** | 11 [1.9–94] | 0.01 / 0.46 | 3.8 | 340 | 85 (100) | 140 [19–1700] |
| porous flow-through graphite (Dionex 6011RS type): conversion 0.95, wetted area 100 mm², 4.3 µL, flow ≥ 300 µL/min | 100 | 95 / 95 | **1.2** | 5.2 [0.76–59] | 0.10 / 0.68 | 1.9 | 6 | 6 (300) | 23 [2.8–340] |
| bound: every product molecule oxidised, 3 mm electrode | 7.07 | 100 / 100 | **1.2** | 4.9 [0.76–58] | 0.10 / 0.69 | 1.3 | 13 | 2 (100) | 9.9 [1.5–130] |
| bound: every product molecule oxidised, 1 mm electrode | 0.785 | 100 / 100 | **1.2** | 4.9 [0.7–58] | 0.11 / 0.69 | 1.3 | 4.4 | 1.4 (100) | 8.1 [1.1–120] |

### 5.2 Tier 2, capillary bed, stop and sweep

| Detector | bed | electrode (mm²) | product oxidised at 5 / 50 µL/min (%) | LOD nominal | median [5–95 %] | P(≤ 1) / P(≤ 10) | substrate background persists | 1 % electroactive: as specified | 1 %: best sweep (µL/min) | 1 %, best sweep: median [5–95 %] |
|---|---|---|---|---|---|---|---|---|---|---|
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.5 mm | tip | 7.07 | 36 / 8 | **2.1** | 8.5 [1.1–100] | 0.04 / 0.54 | 2.2 | 21 | 13 (20) | 33 [5–370] |
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.2 mm (docs/30) | tip | 7.07 | 62 / 15 | **2.1** | 8.4 [1–100] | 0.05 / 0.54 | 2.2 | 13 | 7.4 (20) | 24 [3.8–270] |
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.1 mm | tip | 7.07 | 84 / 23 | **2.1** | 8.4 [1–100] | 0.05 / 0.54 | 2.2 | 9.4 | 5.1 (20) | 21 [3–230] |
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.05 mm | tip | 7.07 | 97 / 36 | **2.1** | 8.4 [0.99–100] | 0.05 / 0.54 | 2.2 | 8.2 | 3.7 (20) | 18 [2.6–210] |
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.025 mm | tip | 7.07 | 100 / 55 | **2.1** | 8.4 [0.99–100] | 0.05 / 0.54 | 2.2 | 8 | 3.1 (50) | 17 [2.4–200] |
| radial thin gap, MicruX thin-film cell, 1 mm electrode, gap 0.16 mm | tip | 0.785 | 16 / 4 | **2.1** | 8.5 [1–100] | 0.05 / 0.54 | 2.2 | 16 | 9.8 (20) | 29 [4.4–320] |
| radial thin gap, MicruX thin-film cell, 1 mm electrode, gap 0.05 mm | tip | 0.785 | 34 / 8 | **2.1** | 8.5 [0.98–100] | 0.05 / 0.54 | 2.2 | 7.7 | 5 (20) | 21 [3.1–240] |
| radial thin gap, MicruX thin-film cell, 1 mm electrode, gap 0.025 mm | tip | 0.785 | 52 / 12 | **2.1** | 8.5 [0.98–100] | 0.05 / 0.54 | 2.2 | 5.3 | 3.6 (20) | 17 [2.5–210] |
| radial thin gap, adjustable (Antec SenCell type): 2 mm glassy carbon, working volume 100 nL = gap 32 µm | port | 3.14 | 93 / 30 | **2.3** | 9.5 [1.1–110] | 0.04 / 0.51 | 2.4 | 6.5 | 3.5 (20) | 18 [2.7–220] |
| cross-flow thin-layer channel (BASi type): 3 mm glassy carbon, gasket 127 µm, channel 3 mm wide | port | 7.07 | 73 / 20 | **2.3** | 9.5 [1.2–110] | 0.04 / 0.51 | 2.4 | 12 | 6.1 (20) | 24 [3.5–260] |
| cross-flow thin-layer channel (BASi type): 3 mm glassy carbon, gasket 51 µm, channel 3 mm wide | port | 7.07 | 87 / 36 | **2.3** | 9.5 [1.1–110] | 0.04 / 0.51 | 2.4 | 10 | 4.1 (20) | 20 [2.9–230] |
| cross-flow thin-layer channel (BASi type): 3 mm glassy carbon, gasket 13 µm, channel 3 mm wide | port | 7.07 | 89 / 73 | **2.3** | 9.5 [1.1–110] | 0.04 / 0.51 | 2.4 | 9.8 | 3 (50) | 17 [2.5–220] |
| free wall jet, large gap (DropSens FLWCL type): 4 mm printed carbon, nozzle 0.3 mm; wall-jet equation, outside its validity at these flows | port | 12.6 | 5 / 3 | **3.3** | 13 [2–130] | 0.01 / 0.41 | 3.4 | 220 | 57 (100) | 100 [14–1400] |
| porous flow-through graphite (Dionex 6011RS type): conversion 0.95, wetted area 100 mm², 4.3 µL, flow ≥ 300 µL/min | port | 100 | 95 / 95 | **2.3** | 9.9 [1.2–110] | 0.04 / 0.50 | 4.4 | 5.4 | 5.4 (300) | 31 [3.6–570] |
| bound: every product molecule oxidised, 3 mm electrode | tip | 7.07 | 100 / 100 | **2.1** | 8.4 [0.99–100] | 0.05 / 0.54 | 2.2 | 8 | 2.5 (100) | 15 [2–230] |
| bound: every product molecule oxidised, 1 mm electrode | tip | 0.785 | 100 / 100 | **2.1** | 8.4 [0.98–100] | 0.05 / 0.54 | 2.2 | 3.3 | 2.2 (50) | 14 [1.8–190] |

Reading.
1. **At nominal the detector does not matter.** Tier 3 is 1.2–1.3 for every thin-layer cell, from 16 % to 100 %
   of the product oxidised, and for the bound. The read is limited by the non-specific label on the bed and its
   walls (93 % of the nominal blank variance of tier 3 in the kit), which the detector passes on in proportion.
2. **Tier 2 separates the cells by where the bed can sit, not by the electrode.** The radial MicruX cells take
   the capillary tip in their inlet bore (2.1). A cell fed through a port has the inlet passage between bed and
   electrode (2.3). This is the case "bed in a fitting on the inlet port" of docs/30 §4.5 again.
3. **A free wall jet with a large gap is the one shape that costs at nominal**: 3.7 against 1.2 in tier 3 and
   3.3 against 2.1 in tier 2. With about 5 % of the product oxidised the read becomes limited by drift. The
   equation is used outside its validity (the jet does not form at these flows), so the factors are an
   indication; the direction is not in doubt.
4. **A porous electrode gains nothing at nominal and loses if the substrate background persists** (1.9 against
   1.3; 4.4 against 2.2). It oxidises the whole stream at ≥ 300 µL/min, so the background current is the largest
   of all cells. In the weak-signal scenario it is good as specified (6.0), because its window is 6 s, but a thin
   gap with a faster sweep does as well or better (3.7–5.0).
5. **If the signal is weak, gap and sweep matter together.** As specified (5 µL/min, 90 s) the thin-layer cells
   spread from 8 to 35 pg/mL in tier 3. The drift charge grows with the square of the window, so a faster sweep
   helps every cell, and it helps a thin gap most because the conversion stays high: 0.2 mm 20 → 11,
   0.1 mm 15 → 7.3, 50 µm 13 → 5.0, 25 µm 13 → 3.7 (at 50 µL/min). A cross-flow channel with a 13 µm gasket
   gives 2.9, the adjustable radial cell at 32 µm 4.0, the bound 2.0.
6. **A by-product for docs/30 as it stands:** in the weak-signal scenario, sweeping at 20 µL/min for 22 s instead
   of 5 µL/min for 90 s lowers tier 3 from 20 to 11 and tier 2 from 13 to 7.4 with no change of hardware. At
   nominal it changes nothing. docs/30 is not edited; the point belongs with test T2-2 (the stop and the sweep)
   if the signal is weak.

### 5.3 Interdigitated arrays

Not run. The MicruX arrays cycle the product 2–3 times by the vendor's own data (docs/28 §2.2 [V]) and need a
second potentiostat channel (tier 3 only). Cycling multiplies signal and blank alike, so at nominal it would not
lower the LOD of a bed format. In the weak-signal scenario its ceiling is that factor of 2–3 on an electrode of
about 0.15 mm² (UNVERIFIED area), and a thin gap with a faster sweep gives as much without the second channel.
In a flowing wall-jet cell cycling is lost above about 100 nL/min (Niwa2000, docs/29 [V-abs]). This agrees with
docs/08 S9, which made the single-channel thin-layer cell the default of the earlier design.

## 6. The pick

### 6.1 What and why

**A radial thin-layer cell: inlet bore centred over a 3 mm working electrode, gap about 50 µm (25–100 µm).**

| Against | Why the pick is preferred |
|---|---|
| The same cell at 0.2–0.5 mm | tier 1: 2.3 against 3.6–5.6; weak signal in tier 3: 5.0 against 11–20 |
| The same cell at 25 µm | equal at nominal (2.2 against 2.3); worse if the substrate background persists (7.3 against 6.3); a 25 µm layer may be thinner than a printed strip is flat (UNVERIFIED: the thickness of the inks and of the dielectric is not published, docs/28 §2.1) |
| Cross-flow thin-layer channel | equal at equal gap in both roles. It loses in tier 1 unless the electrode is the first surface (3.6 against 2.3), in tier 2 because the bed cannot sit 1 mm above the electrode (2.3 against 2.1), and it is not a part that takes the strips in hand |
| MicruX thin-film cell, 1 mm electrode | tier 1: 3.1 against 2.3; equal in tiers 2 and 3 |
| Free wall jet, large gap | 3 times worse in tier 3, 1.6 times in tier 2; captures too little for tier 1 |
| Porous flow-through electrode | no gain; worse if the background persists; ≥ 300 µL/min; wiring to the Gamry UNVERIFIED |
| Tubular or porous capture electrode, interdigitated array | no gain by the transport figures; no part, or a second channel |

For role B alone, a commercial thin-layer or adjustable confined wall-jet cell with a glassy-carbon electrode
would serve as well as the pick. It would not serve better, and docs/26 §4 keeps the MicruX cell in use in every
tier.

### 6.2 How to get it

1. **Measure the gap of the cell in hand.** Until then the gain is unknown: if the gap is already ≤ 0.1 mm, as
   the vendor's "< 5 µL" implies, tier 1 stands at 2.8 and not 3.6, and half of the gain is already there. Two
   electrochemical readings can stand beside the mechanical measurement of docs/27 §9 (item 4), both with the
   strip in place and hydroquinone at neutral pH as the probe (Derived with the kit; D = 9×10⁻¹⁰ m²/s as in
   `params/`, UNVERIFIED there):
   * *Under flow.* The limiting current at 5 µL/min divided by n·F·c·Q is the fraction oxidised: 36 % at 0.5 mm,
     62 % at 0.2 mm, 84 % at 0.1 mm, 97 % at 50 µm (table of section 5.1). One reading separates the cases.
   * *Stopped.* With the electrode switched on in the stopped cell, the layer above it is exhausted within a few
     h²/D (44 s at 0.2 mm, 3 s at 50 µm), and the charge is n·F·A·c·h: 136 µC at 0.2 mm and 34 µC at 50 µm per
     electron for a 1 mM probe over the 3 mm electrode. Probe from the rest of the chamber arrives later
     (a²/D ≈ 2500 s); `tierkit.ThinLayer` gives the full curve.
2. **If the gap is above 0.1 mm, reduce it.** Whether the add-on can be shimmed, or its O-ring seat changed,
   depends on a drawing MicruX has not published (docs/28 §8, questions 1 and 3). The alternatives are a custom
   add-on from MicruX with a defined gap, or the "Thin Layer" add-on that PalmSens lists, if it exists and is
   radial or has the electrode at its entrance (docs/28 §8, question 2). No part is named here.
3. **Tier.** A spacer for the add-on in hand is a consumable or a passive part (tier 1 or 2). A custom add-on
   is a custom part (tier 3). The user decides how to count it (section 8).

A thin layer raises the film resistance between the working electrode and the printed reference: about 13 kΩ for
a 2 mm path in a 50 µm layer at 1 S/m (Derived; conductivity assumed). At nanoampere currents the ohmic drop is
tens of microvolts and does not matter.

### 6.3 What would change the pick

* **The substrate background persists** (question 2 of docs/30 §2.6): choose 100 µm rather than 50 µm for tier 1
  (5.8 against 6.3); the shape stays.
* **The strip cannot be sealed flat at 50–100 µm**: the gain of tier 1 is limited to what the smallest workable
  gap gives (2.8 at 0.1 mm).
* **Tier 1 is not pursued**: then no change to the cell lowers the nominal LOD at all, and the gap is worth
  setting only as insurance against a weak signal.
* **The capture floor ahead of a channel electrode can be passivated like the electrode**: then a cross-flow
  channel is equal to the pick for tier 1, and the choice is by which part can be had.

## 7. Limits

* Everything in docs/30 §6.4 applies. The comparison inherits the kit's parameters, including the UNVERIFIED
  surface factors, noise and drift.
* The radial mapping assumes creeping flow in a gap much thinner than the electrode radius, and it leaves out
  the area under the bore. Radial and channel cells are compared *within* that assumption; the equality of the
  two at equal gap is a property of the mapping, not an independent result.
* A thinner gap is credited with no drawback other than the stream's share: bubbles, the flatness of printed
  strips, the seal, and particles are not modelled.
* Geometry of the non-MicruX cells is assumed where the vendor does not state it: channel width of the BASi-type
  cell, nozzle and gap of the free wall-jet cell, the meaning of the SenCell's working volume, the wetted area of
  the porous electrode, the inlet passage of every "port" cell.
* The weak-signal results depend on the model's drift and noise (UNVERIFIED, docs/02 §4.5) and on a shortest
  read window of 6 s, which is a choice.
* The upstream-wall solver gives the collected fraction for a uniform release; the equivalent-area step uses the
  best-estimate ratio of surface factors.
* Reading tier 1 at 500 µL/min was not checked against the pump programme or the cell's pressure rating, which
  is not stated (docs/28 §1.1).
* Not explored: recirculating or oscillating the sample over the electrode (a flow-path change, tier 3), and
  beads held on the electrode by a magnet (the chamber format of docs/05).

## 8. Decisions for the user, and questions

1. **Is a spacer or a custom add-on for the MicruX cell acceptable in tier 1?** If not, tier 1 keeps the gap
   the cell has.
2. **Should the two electrochemical gap readings (section 6.2) join instrument check 4 of docs/27 §9?** That
   check measures the gap mechanically; docs/27 is not edited here.
3. **Should docs/30 take the 50 µm gap as its tier-1 case once the gap is known?** Nothing in docs/30 is changed
   by this document.
4. To MicruX, in addition to docs/28 §8: can the SPE flow add-on be supplied or shimmed for a gap of 50 µm and
   of 100 µm over the strip; what is the height of the printed layers and of the dielectric above the substrate?

## 9. References

In the repository: docs/02 §5 (commercial cells, with the evidence labels given there); docs/28 (MicruX cells and
electrodes); docs/29 (Squires2008 [V-full], Niwa2000 [V-abs]); docs/30 and docs/31 (designs, findings C1, C5, M2,
M6, N9).

Looked up in this session (bibliographic record in Crossref; "abstract" = abstract read; nothing was opened in
full; authors as the records give them, initials only where a record showed them):

| Key | Reference | Checked | Used for |
|---|---|---|---|
| Kang2025 | Kang S-Y, Davis. Leveraging microfluidic confinement to boost assay sensitivity and selectivity. Chem Sci 2025;16:6965–74. doi:10.1039/d5sc00199d | record and abstract | direction only: a lower channel raised target flux and response in a surface assay (abstract: "600 % improvement in target response magnitude"); a reagentless format, not this assay |
| Gervais2006 | Gervais T, Jensen. Mass transport and surface reactions in microfluidic systems. Chem Eng Sci 2006;61:1102–21. doi:10.1016/j.ces.2005.06.024 | record and abstract | capture fraction in shallow channels as the quantity of interest; no number taken |
| Elbicki1984 | Elbicki JM, Morgan DM, Weber SG. Theoretical and practical limitations on the optimization of amperometric detectors. Anal Chem 1984;56:978–85. doi:10.1021/ac00270a026 | record only | comparison of thin-layer and wall-jet detectors; content recalled, **UNVERIFIED**; no number taken |
| Fuhrmann2009 | Fuhrmann, Linke, Langmach, Baltruschat. Numerical calculation of the limiting current for a cylindrical thin layer flow cell. Electrochim Acta 2009;55:430–8. doi:10.1016/j.electacta.2009.03.065 | record only | a published treatment of the radial thin-layer cell exists; not read, no number taken |
| Yamada1973 | Yamada J, Matsuda H. Limiting diffusion currents in hydrodynamic voltammetry. J Electroanal Chem 1973;44:189–98. doi:10.1016/S0022-0728(73)80245-1 | record only | origin of the wall-jet equation of the model; the coefficient remains "recalled" as in `params/model_assumptions.yaml` |
| Albery1983 | Albery, Brett. The wall-jet ring-disc electrode. J Electroanal Chem 1983;148:201–10. doi:10.1016/S0022-0728(83)80396-9 | record only | second convention of the wall-jet coefficient, as above |

No result of this document rests on a paper that was not opened: the comparison is computed with the kit.

## 10. Record of this follow-up

* Request (2026-11-18): "Explore other flow cell geometries and pick the best one", after the question "Why did
  you choose hydroquinone, alkaline phosphatase, and a wall jet configuration?" No question was put to the user.
* Done by the orchestrator alone: `scripts/tier_round/cell_geometries.py` (new),
  `results/tier_round/cell_geometries.md` and `.json` (new), this document, a line in
  `scripts/tier_round/README.md`, a section in docs/32, and the project guide. No agent, no review.
* Not changed: `tierkit.py`, `designs.py`, `run_tiers.py`, `tier_params.yaml`, `src/`, `params/`, docs/26–31, the
  deck. `check_tierkit.py` and `doc_tables.py --check` were re-run and pass.
* On the way: the first version of the tier-2 base case differed from docs/30 in the fifth digit (dead volume
  computed from the bore instead of taken as 0.5 µL) and the lid fraction of the solver changed by 2 % on a finer
  grid; both were found by the script's own checks and corrected. A first "ideal detector" case had also shrunk
  the dead volume between bed and electrode, which exhausts the substrate in the model; the bound was redefined
  to change the detector only. A quick test run without Monte Carlo overwrote the result files once; the full
  run was repeated, and the `--quick` option no longer writes files. The first draft said the Monte Carlo median
  moves less than the nominal value because of draws the cell cannot help; the draw-by-draw comparison (section
  4.1, point 7) was then computed and the sentence replaced by its result.
* Literature look-up: two of three Consensus searches were refused by a rate limit; two web pages could not be
  opened. The records in section 9 come from one Consensus result and from Crossref.
