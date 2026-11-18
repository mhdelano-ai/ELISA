# 30 — Three implementations for the lowest LOD on the equipment in hand

Status: 2026-11-18, **Revision C** (after the independent review and a second pass on Revision B; docs/31 lists
every finding and what was done). Written by the orchestrator. Inputs: docs/26 (brief and interview), docs/27
(capability map), docs/28 (MicruX hardware), docs/29 (literature), the model (`src/elisa_sim`) and the calculation
kit of this round (`scripts/tier_round/`, 36 checks pass).

How to read the numbers. Every LOD below is a model prediction, not a measurement. "Nominal" = all parameters at
their best estimate. "Median [5–95 %]" = Monte Carlo over the parameter bounds (n = 2000, seed 20261111); the
interval is a scenario range, not a confidence interval (docs/03 §7). P = fraction of draws. Geometry that is not
published (cell gap, bore length, frit area, loop walls) is a design input and is not sampled; its effect is shown
as separate cases. The result tables are pasted from `python scripts/tier_round/doc_tables.py`, which reads
`results/tier_round/tiers.json`.

Terms used throughout:
* **HQDP** = hydroquinone diphosphate, the substrate of the alkaline-phosphatase label; its product is read at
  the electrode.
* **Surface factor** = how much conjugate a surface binds non-specifically per area, relative to blocked
  streptavidin beads washed in tubes (factor 1), the surface on which the project's non-specific-binding rate is
  defined (docs/03, docs/04).
* **Scenarios and levers** (names of docs/05 §2–3): **L6** = detection reagent screened to a half-life ≥ 1 h;
  **L7** = substrate lot with 10⁻⁶ free hydroquinone; **L3** = credit for a F(ab′)₂ conjugate (binds less
  non-specifically; magnitude UNVERIFIED); **L5** = reference channel; **S1** = conjugate binds non-specifically
  25× more than the model assumes; **S4a** = substrate with 10⁻³ oxidisable background.
* **Upper limit by the slope criterion** = the concentration at which the calibration curve has lost the slope
  the model requires (docs/03 §3.6); "curve rises up to" = the highest concentration at which it still increases.
* Project codes (U1–U9, E1.x, gates G1a and G1) are defined in docs/05 §5 and docs/06.

## 0. Summary

One assay, built three ways. All are sequential sandwich assays for human IgG with an alkaline-phosphatase label
and HQDP, read by holding one electrode at the oxidation plateau of the product and integrating the current. They
differ in where the IgG is captured and in what the equipment lets the read exclude.

| | **Tier 1 — consumables only** | **Tier 2 — plus passive parts** | **Tier 3 — anything: one valve** | **Tier 3 with a transfer to a second bed** |
|---|---|---|---|---|
| Capture | on the working electrode itself: printed gold strip (3 mm), biotin-OEG monolayer, streptavidin, biotinylated anti-Fc F(ab′)₂ | on 1×10⁶ streptavidin beads (2.8 µm) packed by hand against a frit in a capillary whose tip sits in the cell's inlet bore, 1 mm above a printed carbon electrode | on the same bed, in the loop of a 6-port valve | as before; the complex is then released and re-captured on a clean bed in the loop of a second valve, and that bed is read |
| Added to the equipment in hand | strips, thiols, reagents, restrictor, a 50 µm transfer line | the same reagents on beads; fritted capillary, sleeve, fitting | one valve, Python valve control | a second valve and bed; a cleavable link and a hapten tag on the capture antibody |
| Read | substrate flows at 200 µL/min; current of the enzyme on the electrode for 60 s, between two reference windows in the same buffer without substrate | flow stopped 5 min, then the product is swept over the electrode in 90 s | bed closed by its valve for 3 min while the cell stays in flow, then swept | the same on the second bed, 7 min |
| Injection to result (min) | 57.1 | 56.7 | 56.7 | 58.2 |
| LOD nominal (pg/mL) | **3.6** | **2.1** | **1.2** | **1.1** |
| LOD median [5–95 %] | 16 [2.8–110] | 8.4 [1.0–100] | 5.1 [0.78–58] | 5.8 [0.64–280] |
| P(LOD ≤ 1 pg/mL) / P(≤ 10) | 0.00 / 0.33 | 0.05 / 0.54 | 0.09 / 0.69 | 0.12 / 0.61 |
| Detection reagent and substrate lot screened (L6 + L7): nominal; median | 2.7; 12 [2.3–79] | 1.4; 6.0 [0.90–56] | 0.88; 3.7 [0.71–34] | 0.43; 3.0 [0.48–42] |
| If the substrate's background does not decay (10⁻⁵ at the time of use): nominal; median | 5.9; 31 [4.6–390] | 2.2; 12 [1.4–130] | 1.3; 6.7 [0.98–79] | 1.3; 9.9 [0.89–640] |
| What limits it | conjugate on the electrode itself; then baseline drift | conjugate on the walls upstream of the bed (45 %) and on the frit (21 %), more than on the beads (31 %) | conjugate on beads, frit and valve loop | the conjugate that comes along in the transfer; the label lost in the 19 min it takes |
| Rests on, unproven | hydroquinone oxidation through the monolayer; the gap of the cell | a zero-flow step in the pump method; the frit's area | the same bed as tier 2 | the transfer chemistry: no release rate is known |

Reading of the table.
* **The order is tier 3 < tier 2 < tier 1, but the steps are small: 3.6, 2.1 and 1.2 pg/mL.** Tier 1 → 2: the bed
  takes 66 % of the sample instead of 8 %. Tier 2 → 3: a valve keeps the conjugate-coated walls upstream of the bed
  out of the read, and the pump no longer has to stop.
* **The transfer to a second bed is not worth building until its chemistry is measured.** With a released
  fraction of 0.35 (0.05–0.74; the reviewers' bound, nothing is known) it gives 1.1 against 1.2 for one valve, with
  a much worse tail. If 70 % is released in 5 min it gives 0.53, and 0.21 with a screened detection reagent.
* **None is predicted to reach the project's 1 pg/mL as specified** (P 0.00, 0.05, 0.09, 0.12). With screened
  reagents and the F(ab′)₂ credit, one valve reaches it in 23 % of the draws.
* **The earlier design of this project** (dosing pump, chamber and trap, docs/05) stands at nominal 0.60, median
  3.5 pg/mL, P 0.16 (docs/08 §10.1). Its numbers and these are not on the same footing: the kit counts terms the
  earlier model does not have (unit-to-unit spread of hand-made consumables, frit, walls in the read path, a 10 min
  half-life of hydroquinone). Neither is shown to be better than the other (section 5.6).
* The orchestrator's judgement of what a first working version would show, given what the model does not carry
  (section 6.4): tier 1 10–100 pg/mL, tier 2 3–30 pg/mL, tier 3 with one valve 2–20 pg/mL.

**Two chemistry questions stand above all tiers and above the earlier designs** (section 2.6). Both are settled by
half a day at the bench, before anything is built.
1. *What does the enzyme make?* Alkaline phosphatase removes one phosphate per turnover, so at picomolar enzyme the
   product of hydroquinone *di*phosphate should be the monophosphate, not hydroquinone (review finding C1). If the
   monophosphate is not oxidised at the read potential, the signals of this document are 10² to 10⁵ too high, and
   the substrate has to change. Model, if only 1 % of the turnovers give an electroactive product: 200, 13 and
   20 pg/mL for tiers 1, 2 and 3.
2. *How long does hydroquinone live at pH 9.5?* If its half-life is the 10 min the review found, the free
   hydroquinone of the substrate lot is gone before the substrate is used, and the model says so (this is the "as
   specified" case). If the substrate's oxidisable background persists at 10⁻⁵, tier 1 is 5.9 instead of 3.6.

**Recommendation.** First the two bench questions. Then build tier 2: it uses the strip cell the user named and
the reagents already in the bill of materials (docs/07 §1), and its bed is the bed of tier 3. If one 6-port valve
can be bought, put the bed in its loop at once: by the model it is 1.7 times lower than tier 2 and needs no
zero-flow step. Tier 1 is the cheapest to try. The second valve and the transfer wait for their own test
(section 5.5).

## 1. What sets the LOD on this equipment

1. **The blank is non-specifically bound conjugate, wherever its product can reach the electrode.** The LOD is
   3 × the SD of that blank (docs/04, docs/05). Specific and non-specific label on a surface both scale with its
   area and, for a short exposure, with the conjugate dose, so their ratio depends on neither: it is (captured
   IgG per area) × k_on,detection / (non-specific rate × surface factor).
2. **Without a valve the conjugate wets every wall from the injector to waste**, and the substrate later follows
   the same path. Under flow, the product of the upstream walls arrives at the electrode with the stream. In a
   stopped line it stands in the liquid right behind the bed and follows the plug into the read window.
3. **Both MicruX flow add-ons are wall-jet cells** (docs/28 §1 [V]): the stream enters through a bore above the
   centre of the working electrode and leaves radially through a gap whose height is not published. The whole
   sample passes over the electrode. For a thin gap in creeping flow the capture problem is the channel problem in
   the swept area (`scripts/tier_round/README.md` B). At 2.9 µL/min a 3 mm electrode under a 0.2 mm gap takes 8.2 %
   of the sample (mass-transfer coefficient 0.85×10⁻⁶ m/s against a reaction velocity of 4.2×10⁻⁶ m/s). Loading in
   stopped portions takes 5.0 % and needs a zero-flow step.
4. **A bed of small beads captures by reaction, not by transport**: 1×10⁶ beads of 2.8 µm are 24 mm² and take 66 %
   of a 100 µL sample at 3.4 µL/min.
5. **Product formed on the electrode is collected in full at any flow; product that arrives with the stream is
   collected only at the stream's conversion**, which falls with flow: 99 % at 1 µL/min, 62 % at 5 µL/min, 6.1 % at
   200 µL/min for the 3 mm electrode under a 0.2 mm gap (kit, `cell_conversion`). Tier 1 therefore reads at a fast
   flow; tiers 2 and 3 sweep their plug slowly.
6. **Label is lost while the assay waits.** At the best estimate of the detection off-rate (half-life 13 min)
   25–63 % of the label leaves between the conjugate step and the read. This is the largest single sensitivity of
   every tier.

From the literature (docs/29 Part A): p-aminophenol fouls printed carbon and gold (Buckey2022 [V-abs]), so the read
is the hydroquinone system; amplification by a reductant in solution is shown only on ITO and on gold under long
monolayers (Das2007, Kwon2008, Akanda2011a, Akanda2013 [V-abs]) and amplifies the blank with the signal; a
potential step charges about 1 µC on a 3 mm printed electrode, a thousand times the signal at the LOD, so the
potential is held (docs/29 A.4).

## 2. What the implementations share

### 2.1 Reagents (docs/07 §1; vendor pages re-opened by the chemistry reviewer, docs/31 §3.2)

| Item | Choice | Note |
|---|---|---|
| Capture antibody | biotinylated goat F(ab′)₂ anti-human IgG, Fcγ-specific, minimal cross-reaction to bovine, horse, mouse (Jackson 109-066-098) | [V] reviewer |
| Detection conjugate | alkaline-phosphatase goat F(ab′)₂ anti-human IgG, F(ab′)₂-specific (Jackson 109-056-006) | [V] reviewer: **not** adsorbed against bovine proteins, stabilised with BSA. A conjugate adsorbed against bovine serum is to be found (part UNVERIFIED); ask for the certificate of the BSA stabiliser |
| Streptavidin beads (tiers 2, 3) | Dynabeads M-280 Streptavidin 11205D, 10 mg/mL, 6–7×10⁸ beads/mL, about 10 µg biotinylated antibody per mg (docs/28 R32 [V]); 1×10⁶ beads = 1.5 µL of stock (Derived) | the stock holds 0.1 % ordinary BSA: wash and re-block in IgG-free BSA (docs/06 §4.0; docs/31 C4) |
| Substrate | hydroquinone diphosphate, Metrohm DropSens DRP-HQDP-0.5G; no purity, free-hydroquinone or monophosphate specification | [V]; subject to the tests of section 2.6 |
| Standard | NISTmAb RM 8671 (after gate G1a), polyclonal human IgG for development | docs/07 §1 |
| Blocker and carrier | IgG-free BSA | bovine IgG cross-reacts with anti-human-IgG reagents (docs/29 C.2) |

The acceptance criteria for the antibody pair are those of docs/05 §4.1 (half-lives ≥ 1 h; bench item U2 of
docs/05 §5).

### 2.2 Solutions

| Line or vial | Content | Note |
|---|---|---|
| BSM A1 | wash buffer: 50 mM Tris-HCl pH 7.5, 150 mM NaCl, 0.05 % Tween 20 | no phosphate (docs/08 finding B1) |
| BSM B1 | substrate in substrate buffer (0.1 M Tris pH 9.5, 1 mM MgCl₂, 150 mM NaCl): 0.3 mM HQDP (tier 1), 1 mM (tiers 2, 3) | fresh daily, dark, used between 1 and 8 h after it is made (model: 4 h). The chloride keeps a printed silver reference where it was in A1 (docs/28 §4). Tris buffers weakly at pH 9.5 (8 mM per pH unit, Derived by the reviewer); 1 M diethanolamine pH 9.8 is the alternative to compare (docs/31 C9) |
| BSM A2 (tier 1) | substrate buffer without HQDP, from the same batch of buffer as B1 | reference liquid of the tier-1 read (section 3.1) |
| BSM B2 | water, then 10 % methanol for storage | docs/02 §1.2 |
| Tray vial, 4 °C | conjugate in assay buffer (wash buffer + 1 % IgG-free BSA): 20 nM (tier 1), 5 nM (tier 2, tier 3 with one valve), 10 nM (transfer) | full-loop injection |
| Tray vial | assay buffer, for a loop-cleaning injection before each determination | |
| Tray vial (tier 1) | 10 nM hydroquinone in wash buffer, made the same day | response check of each strip; bench standards are diluted into substrate buffer just before use (docs/31 C5) |
| Tray vial (transfer) | eluent (section 5.3) | |
| Sample vial | sample only; standards and blanks are made in assay buffer | docs/26 §3 |

### 2.3 Flow path, control and timing rules

* **Path.** BSM → mixer → restrictor → SM-FL (100 µL loop, full loop) → transfer line of **0.05 mm bore, 15 cm** →
  cell → short open waste line. The line is short and narrow because its 24 mm² of wall carries conjugate (fact 2):
  with a 0.127 mm × 20 cm line tier 2 goes from 2.1 to 3.5 pg/mL. It adds 12 bar at 80 µL/min and 29 bar at
  200 µL/min upstream of the cell (Derived, Hagen–Poiseuille).
* **Restrictor.** First choice for all tiers: the Waters restrictor kit, 40 µm × 35 cm (kit 205000547, docs/27 §3
  [V]): 12 psi per µL/min, so 36 psi at 3 µL/min, 960 psi at 80 µL/min and 2400 psi at 200 µL/min. It keeps the
  liquid stored upstream small (section 2.3, flow steps). If the pump does not hold a steady 2–5 µL/min against
  36–60 psi (docs/27 §9 item 1), the alternative is 25 µm × 45 cm (100 psi per µL/min; availability UNVERIFIED),
  which cannot be used at the 200 µL/min of tier 1.
* **Loop Offline is set in every line's method**: after the sample has left the loop (line 1), and after two loop
  volumes of flush behind a reagent, always before a change of pump composition. A change of composition is
  **215 µL** of the new liquid (95 % of full strength at the cell; docs/27 §1, docs/31 F1).
* **Lines.** One determination is two sample-set lines (sample, conjugate) after a pre-run; the transfer has a
  third (eluent). The time a line needs before its injection is taken as 1 min (docs/02 §2.2: 0.25–2 min,
  UNVERIFIED). At 2 min per line tiers 1, 2 and 3 with one valve still end within 60 min (59.2, 58.7 and
  58.7 min); the transfer ends at 61.2 min and has to shorten its load.
* **Flow steps.** Sample 2.9–5 µL/min; conjugate 50 µL/min; washes and composition changes 50–200 µL/min. Before a
  stop the flow is set to 5 µL/min for 1 min so that the pressure upstream of the restrictor has relaxed
  (docs/27 §2, docs/31 F2). A valve is switched into a slow step only after 1 min at that flow.
* **Potentiostat.** The Gamry holds the read potential from the pre-run to the end and records at 2–10 Hz; the
  Inject Start contact of each line and the valve commands mark the record (docs/27 §5). Potential: +0.30 V
  against the strip's printed reference in 0.15 M chloride as a starting value, set once per strip lot on the
  plateau of a voltammogram of enzyme-generated product in substrate buffer (section 2.6), not above +0.5 V on
  gold (MicruX gives −0.3 to +0.6 V for its thin-film gold in chloride, docs/28 §4 [V]; taken as a caution for
  printed gold, UNVERIFIED). Current range, fixed for a whole determination (ranges and accuracy: docs/02 §4.1
  [V]): 6 nA. It covers tier 1 to about 2000 pg/mL and the peaks of tiers 2 and 3 to about 100 pg/mL; standards
  above that are run on the 60 nA range (Derived: a peak about 12 s wide; docs/31 K3). A range is never
  changed within 60 s of a read window.
* **Washes** are 1.5 min after the sample and 2 min after the conjugate, not below the minima of docs/05 §1.1
  (1 min and 2 min), because wash efficiency is not modelled.
* **Before each determination** (not counted in the 60 min, docs/26 §3): mount the fresh consumables, flush, one
  full-loop injection of assay buffer to clean needle and loop, the pre-run of the tier, and at least 300 µL of
  wash buffer so that no substrate is left upstream of the injector.
* **Not yet in `automation/`:** the Gamry worker's instrument backend is a stub, and the signal routine fits a
  baseline through windows around a peak; the pre-run subtraction of tiers 1 and 2 has to be added (docs/31 F7).

### 2.4 Calibration, blanks and the LOD

A calibration is a set of determinations, each on its own fresh consumables (strip, bed): blanks (assay buffer) and
standards up to 1000 pg/mL. The LOD is the concentration at mean blank + 3 SD of at least ten blanks on ten sets of
consumables, read through the curve (docs/26 §3). The unit-to-unit spread of the blank is part of the LOD; the
model carries it as 10 % (the model's blank CV) plus 15 % (hand-coated electrodes) or 10 % (hand-packed beds), both
UNVERIFIED (`tier_params.yaml`).

Range (docs/26 §3 asks for a monotonic curve over two decades above the LOD):

| | Tier 1 | Tier 2 | Tier 3, one valve | Tier 3 with transfer |
|---|---|---|---|---|
| Upper limit by the slope criterion (pg/mL) | 10⁵ | 1400 | 270 | 270 |
| Curve rises up to (pg/mL) | 10⁵ | 10⁵ | 10⁵ | 10⁵ |
| Decades above the nominal LOD by the slope criterion | > 4 | 2.8 | 2.3 | 2.4 |

The curves of tiers 2 and 3 bend because the phosphate released with the product inhibits the enzyme in the small
volume around the bed. A shorter stop bends less.

### 2.5 What the model takes for granted

* One molecule of electroactive product (two electrons) per enzyme turnover (section 2.6, question 1).
* One stability of hydroquinone for the whole liquid path: half-life 600 s (120–7200 s) at pH 9.5, in the bed and
  in the substrate reservoir alike (section 2.6, question 2). The earlier model of this project takes 2 h and
  keeps the substrate's free hydroquinone at 10⁻⁵ of the substrate; that case is shown in every table as "the
  substrate's background does not decay".
* The detection conjugate binds non-specifically at the rate the project's audit derived from published bead
  assays (docs/04), times the surface factor of each surface. This is the largest uncertainty after the off-rate.

### 2.6 Two bench questions to settle before anything is built

**Question 1: the product (review finding C1).** Alkaline phosphatase hydrolyses one phosphate ester per turnover.
From hydroquinone diphosphate it releases the monophosphate, which has to bind again, in competition with a
thousandfold excess of diphosphate, before hydroquinone appears. With the enzyme amounts of this document the
hydroquinone-to-monophosphate ratio after the stop of tier 2 is about 10⁻⁴ to 10⁻³, and in tier 1 less than 10⁻⁵
of the monophosphate is hydrolysed again before the flow removes it (Derived by the chemistry reviewer,
`results/tier_round/review_chemistry.md` C1; for equal Michaelis constants and turnover numbers of the two esters
the ratio is half the converted fraction of the substrate). The model, like docs/01–05, counts one hydroquinone per
turnover. The papers the choice of substrate rests on (Wilson2004, Bekhit2021; docs/29 A.1) do not address the
intermediate.

| If the test shows | Then |
|---|---|
| the monophosphate is oxidised at or near the hydroquinone potential | nothing changes (one or two electrons per turnover) |
| it is oxidised only at a higher potential | the read potential moves up; on gold the window is narrow (section 2.3) |
| it is not oxidised | change the substrate: p-hydroxyphenyl phosphate (the monophosphate itself; DellaCiana1996, docs/01; supplier not found, docs/07 §6) or ascorbic acid 2-phosphate (docs/01). The designs stay as they are |

Model if only 1 % of the turnovers give an electroactive product (nominal, pg/mL): tier 1 200, tier 2 13, tier 3
with one valve 20, with the transfer 42. With 0.1 %: 2000, 120, 200, 420. The bed designs lose little at first
because their limit is the conjugate, not the current.

**Question 2: the life of hydroquinone at pH 9.5 (review findings C5 and M2).** Half-lives of 111 h, 41 h and
0.84 h at pH 7, 8 and 9 extrapolate to about 7 min at pH 9.5 ([S], a compilation quoting Moussavi 1979; primary
source not opened; the rate at nanomolar concentration may differ). The same number acts twice. It takes 10–21 %
of the product formed during a 3–7 min stop (Derived). And it removes the free hydroquinone of the substrate lot from the working
solution before use, leaving only what hydrolysis keeps forming (about 10⁻⁷ of the substrate). Both follow from
one measurement.

**The test** (half a day, no flow system; materials of E1.1 and E1.2 of docs/06):
1. 1–10 pM conjugate in 1 mM HQDP in substrate buffer for 7 min; voltammogram on a printed carbon strip and on a
   coated gold strip against a hydroquinone standard of the expected concentration. Repeat in 1 M diethanolamine
   pH 9.8.
2. The same mixture separated on the I-Class (reversed-phase column) to see diphosphate, monophosphate and
   hydroquinone: with a UV detector if one is on the stack, otherwise with the MicruX cell as the detector at two
   potentials.
3. 50 nM hydroquinone in substrate buffer, read after 0, 3, 7 and 12 min, with and without sulfite (Bekhit2021).
4. The oxidation current of the working substrate solution 0, 1, 4 and 8 h after it is made.

## 3. Tier 1 — consumables only: the electrode is the solid phase

### 3.1 Design

| Element | Choice | Source and confidence |
|---|---|---|
| Cell | MicruX AIO-SPE cell with its flow add-on: wall jet, 0.8 mm inlet bore, 8 mm O-ring | docs/28 §1 [V]; gap not published: 0.2 mm taken (the user's 10 µL), 0.1 and 0.5 mm as cases |
| Electrode | MicruX ED-S1PE-Au10 printed gold strip, 3 mm working electrode (7.1 mm²), printed silver reference; one strip per determination | docs/28 §2.1 [V] |
| Surface | on the working electrode only (a 2–3 µL drop): mixed monolayer of a short-chain biotin-terminated and hydroxy-terminated oligo(ethylene glycol) thiol, then streptavidin, then biotinylated capture F(ab′)₂, then assay buffer | principle: Nishimura2011 [V-abs] (short tri(ethylene glycol) thiols resist protein and pass p-aminophenol); thiol part numbers and the quality of monolayers on printed gold UNVERIFIED |
| Capture | sample through the cell at 2.86 µL/min for 44 min (126 µL; 99 % of the plug leaves the loop) | docs/27 §4 |
| Label | 100 µL of 20 nM conjugate at 50 µL/min, 4 min (two loop volumes) | exposure 40 nM·min |
| Read | flow constant at 200 µL/min: reference liquid (window 30 s) → substrate (front 1.1 min, read 60 s) → reference liquid (front 1.1 min, window 30 s). The reference liquid is the substrate buffer without substrate (line A2). Signal = current in the read window minus the mean of the two reference windows, minus the same quantity from the identical sequence run on the fresh strip before the sample | docs/31 N1, N2, M1 |

Why a fast, constant flow. (i) The conjugate on the inlet bore and on the transfer line (36 mm², 2.5×10⁵ enzymes)
makes product that the stream carries over the electrode. At 200 µL/min at most 6 % of it is collected, against
62 % at 5 µL/min, while the electrode's own enzyme is collected in full. (ii) The two reference windows are at the
same flow as the read and 3.7 min apart, so no pressure or charging transient separates them from it and the
baseline has little time to drift. (iii) No zero-flow step and no flow below 2.9 µL/min is needed.

Why the reference liquid is the substrate buffer. A read in substrate buffer (pH 9.5) against windows in wash
buffer (pH 7.5) would contain the difference in background current between the two buffers, and what the pre-run
subtraction leaves of it. A difference of 100 pA costs a third of the LOD (4.9 against 3.6), 300 pA a factor of
three (docs/31 M1). With the same buffer on both sides the windows differ from the read only by the substrate.
Line A2 is selected in the method of the conjugate line; whether its liquid has replaced A1 at the cell by the
first reference window depends on the internal volume of pump A, which is to be measured (docs/27 §9 item 12). If
it has not, the substrate buffer without substrate becomes the wash buffer of the whole determination (sample and
conjugate travel in their own pH 7.5 buffer), after a check that the complex holds at pH 9.5.

Why printed gold, and why it is not certain. The model puts gold with an OEG monolayer at 3.6 pg/mL, the thin-film
gold chip in its small cell at 4.1 and printed carbon with adsorbed streptavidin at 11. The gold figure rests on
a surface factor of 3 against 10 for carbon, and on hydroquinone being oxidised at full rate through the monolayer
and the protein on it; if the coated gold delivers 30 % of the current the LOD is 7.2 (docs/31 C2). The printed
strip is preferred to the thin-film chip because its silver reference stands apart from the working electrode and
is not covered by the thiol (docs/31 C3). **Printed carbon (ED-S1PE-C21, printed Ag/AgCl reference, no thiol
chemistry, 10 nM conjugate) is the fallback, and the first tier-1 experiment compares the two.**

Why 0.3 mM substrate. With a background that decays, 1 mM is as good (3.5). If the background does not decay,
1 mM costs a factor of two (13 against 5.9). 0.3 mM is the choice that loses little either way.

### 3.2 Bench preparation (per batch of strips; UNVERIFIED as a recipe)

1. Gold: clean electrochemically in chloride-free acid as the vendor prescribes (docs/28 §4 [V]); rinse.
2. Monolayer: 1 mM total thiol (biotin-OEG : OEG about 1 : 9, alkyl part C2–C6), a 2–3 µL drop on the working
   electrode only, in a closed humid box; rinse. Check each batch by the blocking of ferricyanide or by the
   reductive desorption charge.
3. Streptavidin 50 µg/mL, 30 min; rinse. Biotinylated capture F(ab′)₂ 10 µg/mL, 30 min; rinse. Assay buffer
   30 min. Store wet at 4 °C; shelf life to be measured.
4. Carbon fallback: streptavidin adsorbed on the working electrode overnight at 4 °C (DiazGonzalez2005,
   docs/29 B.2 [V-abs]), then as step 3.
5. Non-immune strips for the blank test: biotinylated normal goat F(ab′)₂ (docs/07 §1).

### 3.3 Step table (57.1 min from Inject Start to result)

| Clock (min) | Step | BSM | SM-FL | Gamry (+0.30 V, 6 nA range, chronoamperometry) |
|---|---|---|---|---|
| before (12 min) | mount strip; flush; cleaning injection; 10 nM hydroquinone plug as a check of the strip's response; then the read sequence of rows 51.5–57.1 on the fresh strip; 300 µL of wash buffer | A1, A2, B1 | assay buffer; hydroquinone | on from here to the end |
| 0–1 | sample aspirated and loaded; Inject Start | A1 2.86 µL/min | line 1: sample, full loop | mark |
| 1–45 | sample through the cell | A1 2.86 µL/min | loop in line | — |
| 45–46.5 | wash 1 | A1 50 µL/min | Loop Offline | — |
| 46.5–47.5 | conjugate aspirated and loaded | A2 50 µL/min | line 2: conjugate, full loop | mark |
| 47.5–51.5 | conjugate through the cell, two loop volumes | A2 50 µL/min | loop in line, then Loop Offline | — |
| 51.5–53.5 | wash 2 in substrate buffer without substrate; last 30 s = reference window 1 | A2 200 µL/min | — | window |
| 53.5–54.6 | substrate front (215 µL) | B1 200 µL/min | — | — |
| 54.6–55.6 | **read** | B1 200 µL/min | — | window |
| 55.6–56.6 | front back to the reference liquid | A2 200 µL/min | — | — |
| 56.6–57.1 | reference window 2 | A2 200 µL/min | — | window |

### 3.4 Where the number comes from (nominal; `tiers.json`)

| Quantity | Value |
|---|---|
| Sample molecules at 1 pg/mL | 4.0×10⁵ |
| Captured on the electrode | 3.3×10⁴ (8.2 % of the vial) |
| Labelled (58 %), label still bound at the read (75 %), analyte still bound (82 %) | 1.2×10⁴ enzymes |
| Signal | 2.9 pA per pg/mL (750 turnovers per second at 0.3 mM, 2 electrons); 0.17 nC in the 60 s window |
| Conjugate on the electrode (surface factor 3) | 4.9×10⁴ enzymes, collected in full: 12 pA |
| Conjugate on bore and transfer line | 2.5×10⁵ enzymes, 6.1 % collected: 3.7 pA. An upper estimate: product of the bore wall enters the gap along the lid, away from the electrode (docs/31 M6) |
| Substrate background | 1.0 pA from hydrolysis; free hydroquinone of the lot decayed. If it does not decay: 118 pA from the lot and 17 pA from hydrolysis (Derived) |
| Blank current; blank equivalent | 17 pA; 5.9 pg/mL |
| Noise, drift (model values, UNVERIFIED, docs/02 §4.5) | 3 pA rms; 5 pA/min, of which 20 % is taken as not removed over the 3.7 min between the windows |
| Variance at the blank | non-specific label 68 %, drift 28 %, electrode response 2 %, noise 1 % |
| LOD | 3.6 pg/mL: 10 pA to be told from a 17 pA blank |

### 3.5 Scenarios and alternatives (`tiers.md` §2, §3)

| Case | Nominal | Median [5–95 %] | P(≤ 1) / P(≤ 10) |
|---|---|---|---|
| as specified | 3.6 | 16 [2.8–110] | 0.00 / 0.33 |
| detection reagent and substrate lot screened (L6 + L7) | 2.7 | 12 [2.3–79] | 0.00 / 0.42 |
| the same with the credit for the F(ab′)₂ conjugate (L3) | 1.9 | 8.3 [1.7–52] | 0.01 / 0.57 |
| conjugate binds non-specifically 25× more (S1) | 76 | 250 [36–2100] | 0.00 / 0.00 |
| the substrate's background does not decay: 10⁻⁵ of the substrate at the time of use | 5.9 | 31 [4.6–390] | 0.00 / 0.18 |
| the same with screened reagents (L6 + L7) | 2.9 | 16 [2.8–120] | 0.00 / 0.35 |
| background 10⁻³ of the substrate, no decay (S4a) | 390 | 670 [100–4900] | 0.00 / 0.00 |
| **printed carbon ED-S1PE-C21, adsorbed streptavidin, 10 nM conjugate** | 11 | 32 [4.4–340] | 0.00 / 0.17 |
| printed carbon, background does not decay | 15 | 78 [8.3–1300] | 0.00 / 0.06 |
| thin-film gold chip SE1 in the thin-film cell | 4.1 | 21 [3.3–160] | 0.00 / 0.27 |
| strip-cell gap 0.10 mm | 2.8 | 13 [2.3–100] | 0.01 / 0.39 |
| strip-cell gap 0.50 mm | 5.6 | 22 [3.9–160] | 0.00 / 0.23 |
| read at 300 µL/min | 3.2 | 14 [2.5–100] | 0.00 / 0.37 |
| read at 80 µL/min | 5.9 | 25 [4.2–190] | 0.00 / 0.20 |
| read at 40 µL/min | 11 | 42 [7.0–420] | 0.00 / 0.10 |
| read 120 s at 150 µL/min, 10 nM conjugate (operating point of Revision B) | 5.7 | 22 [3.5–180] | 0.00 / 0.24 |
| conjugate 10 nM | 4.1 | 18 [2.9–140] | 0.00 / 0.31 |
| conjugate 40 nM | 4.5 | 18 [3.3–130] | 0.00 / 0.29 |
| substrate 0.1 mM | 4.2 | 19 [3.2–140] | 0.00 / 0.29 |
| substrate 1 mM | 3.5 | 15 [2.7–120] | 0.00 / 0.34 |
| substrate 1 mM, background does not decay | 13 | 51 [6.0–950] | 0.00 / 0.12 |
| reference windows in wash buffer pH 7.5, background step of 100 pA | 4.9 | 25 [4.7–170] | 0.00 / 0.19 |
| reference windows in wash buffer pH 7.5, background step of 300 pA | 11 | 48 [8.0–370] | 0.00 / 0.08 |
| coated gold delivers 30 % of the transport-limited current | 7.2 | 19 [3.5–120] | 0.00 / 0.29 |
| no pre-run read on the strip | 4.0 | 18 [3.4–130] | 0.00 / 0.30 |
| no pre-run read, background does not decay | 18 | 58 [6.9–1100] | 0.00 / 0.09 |
| read in the stopped cell (needs a zero-flow row) | 13 | 49 [7.5–460] | 0.00 / 0.08 |
| stop-and-go loading, 13 portions held 190 s (needs a zero-flow row) | 6.0 | 23 [4.0–160] | 0.00 / 0.22 |
| transfer line 0.127 mm × 20 cm | 4.6 | 20 [3.4–140] | 0.00 / 0.26 |
| detection conjugate with 5 [2–10] enzymes per antibody (UNVERIFIED reagent) | 3.1 | 11 [1.9–87] | 0.01 / 0.47 |

The cell's unknown gap matters here (2.8 to 5.6 pg/mL for 0.1 to 0.5 mm). A read at 300 µL/min is slightly better
by the model and leaves its range of validity (section 6.4). A detection conjugate that carries several enzymes
would help tier 1 a little (3.1) and tiers 2 and 3 not at all, because they are limited by the conjugate count.

### 3.6 What could make it fail, and the experiments that decide (in order)

| # | Experiment | Decides | Pass |
|---|---|---|---|
| T1-1 | Coated gold strip and bare carbon strip in the cell at 200 µL/min, no protein: hydroquinone wave and plateau; noise and drift on the 6 nA and 600 pA ranges; the read sequence five times over 70 min with a conjugate-free protein exposure in between; the same with wash buffer as the reference liquid | whether hydroquinone is oxidised through the monolayer; drift; whether the background repeats; the size of the buffer step | half-wave ≤ +0.25 V and plateau ≥ 70 % of bare gold at 1 µM hydroquinone; drift ≤ 5 pA/min; background repeat ≤ 3 % |
| T1-2 | Non-specific binding: non-immune strips, the conjugate step, the read; 10 strips each of gold/OEG and carbon | surface factors and unit-to-unit CV | gold: ≤ 5×10⁴ enzymes on the electrode (about 12 pA), CV ≤ 20 % |
| T1-3 | Capture: 1 ng/mL IgG through the full protocol, 5 strips, with and without the pre-run | captured fraction and labelling; whether the pre-run harms the capture layer | ≥ 2 pA per pg/mL |
| T1-4 | Blanks on 10 strips, then 10, 30, 100, 1000 pg/mL | the LOD | — |

Risks the model does not carry: a printed silver reference in chloride needs conditioning and may drift
(docs/27 §9 item 8); protein adsorbed during the sample step changes the electrode's response between pre-run and
read; the conjugate on the transfer line builds up from run to run unless the line is flushed or replaced; the
pre-run exposes the capture layer to pH 9.5 and to the benzoquinone formed at the electrode.

## 4. Tier 2 — plus passive in-line parts: a hand-packed micro-bed in the inlet bore

### 4.1 Design

| Element | Choice | Source and confidence |
|---|---|---|
| Capture bed | 1×10⁶ Dynabeads M-280 Streptavidin carrying the biotinylated capture F(ab′)₂, packed against a frit in a fused-silica capillary of 0.20 mm bore and 0.36 mm outside diameter: bed 19 nL, 0.6 mm long (about 215 bead diameters), 24 mm² of bead surface | beads [V]; fritted capillaries are standard in capillary LC, part numbers and frit pore size UNVERIFIED |
| Position | the capillary passes through the inlet port, sleeved to fill the 0.8 mm bore (sleeves of 1/32″ outside diameter for 0.36 mm capillaries exist as a class: IDEX F-385 [S], `review_chemistry.md` C10), and ends 1 mm above the working electrode (0.5 µL of bore between tip and electrode); 20 mm of capillary above the bed | bore 0.8 mm [V docs/28]; fit of the sleeve in the port UNVERIFIED |
| Cell and electrode | MicruX AIO-SPE cell with its flow add-on; printed carbon strip ED-S1PE-C21 (3 mm, printed Ag/AgCl reference), blocked with assay buffer; **a fresh strip with every bed** | docs/28 §1, §2.1 [V]; docs/31 C7 |
| Capture | sample through the bed at 3.4 µL/min for 37 min; 66 % captured; pressure drop 1.0 bar | kit, bed correlation of the model |
| Label | 100 µL of 5 nM conjugate through the bed at 50 µL/min, 4 min (15 bar across the bed) | exposure 10 nM·min |
| Read | substrate in (215 µL at 80 µL/min, 25 bar across the bed), 1 min at 5 µL/min, flow stopped 5 min, then 5 µL/min for 90 s: the product crosses the electrode, which converts 62 % of it. Signal = charge of (trace minus pre-run trace) over the 90 s above the level of the last 30 s of the stop. The pre-run is the same substrate step, stop and sweep on the fresh bed and strip | kit; docs/27 §2 for the stop; docs/31 N4 |

Why beads of 2.8 µm. They are the surface on which the project's non-specific-binding rate is defined, they are in
the bill of materials, and a million of them is the smallest bed that still takes two thirds of the sample. Packed
in a column and washed in flow they are given the model's packed-bed factor of 3 (1–30), not the factor of 1 they
have when washed in tubes (docs/31 N5); with 1 the LOD is 1.6.

Why at the tip, and what still lies in the read path. Every conjugate-coated wall that stands in substrate during
the stop makes product, and the sweep carries all of it over the electrode. Below the bed: the frit (5 mm² taken)
and 1 mm of bore (2.5 mm²). Above the bed: the capillary (13 mm²) and the transfer line (24 mm²); their product
arrives right behind that of the bed, inside the read window. Of the blank's 1.4×10⁵ enzymes, 45 % sit on the walls
above the bed, 31 % on the beads, 21 % on the frit, 3 % on the bore. Three ways to shrink the first group: a valve
(tier 3: 1.2); a transfer line of 0.025 mm bore (1.8; it clogs more easily); walls that bind as little as blocked
beads, for which fused silica with a neutral hydrophilic coating, as sold for capillary electrophoresis, is the
candidate (1.4 if the factor is 1; UNVERIFIED).

Why 5 nM conjugate and a 5 min stop. The tier is limited by the conjugate count, so less conjugate and a shorter
stop cost nothing at the nominal: 3 nM with a 3 min stop gives 2.0. But that point leaves less current, and if the
enzyme product is only partly electroactive (section 2.6) it suffers first: 27 pg/mL against 13 at 1 %. The chosen
point gives up 5 % of the nominal LOD for that margin and keeps the calibration to 1400 pg/mL. The stop also gives
the read its baseline.

Why the pre-run. During the stop the electrode is on and empties the layer above it of whatever oxidisable
background the substrate has. When the sweep starts, fresh substrate arrives and the background steps up while the
product passes. If the background decays in the reservoir the step is 1 pA and does not matter. If it does not
(10⁻⁵ of 1 mM), the step is 100 pA beside a mean blank current of 93 pA; the trace of the same stop and sweep on the
fresh bed and strip carries the same step and is subtracted, and 4 % of it is taken as left (UNVERIFIED).

The frit is the other open point: a 0.5 mm silicate frit may have 20 mm² of inner surface (Derived: 4ε/d for
1.5 µm pores, UNVERIFIED). Model LOD for 1, 5 and 20 mm²: 1.7, 2.1 and 3.4 pg/mL. A magnet instead of a frit does
not hold a packed bed: the pressure drop puts 3 nN on each bead at the loading flow and 78 nN at 80 µL/min, against
0.02–0.2 nN of magnetic force (Derived, docs/31 C6).

### 4.2 Bench preparation

1. Coat beads in a tube: wash the stock three times in wash buffer, re-block in assay buffer; biotinylated capture
   F(ab′)₂ at 10 µg per mg of beads, 30 min; wash; assay buffer 30 min (docs/06 §4.0). Non-immune beads likewise.
2. Pack: draw 1.5 µL of coated beads (10 mg/mL), diluted in 20 µL assay buffer, into the capillary against the
   frit; follow with assay buffer. Compact the bed at 80 µL/min for 1 min on the bench and check its length (0.6 mm).
3. Sleeve the capillary, seat it in the inlet port against a mechanical stop so that the tip is 1 mm above the
   strip, mount a fresh strip.
4. The add-on is held by magnets (docs/28 §1 [V]) and the beads are magnetic: check under a lens that the bed stays
   packed with the add-on in place. If it does not, use non-magnetic streptavidin particles of 3–10 µm (docs/31 C6).

### 4.3 Step table (56.7 min)

| Clock (min) | Step | BSM | SM-FL | Gamry (+0.30 V vs the printed Ag/AgCl, 6 nA range, chronoamperometry) |
|---|---|---|---|---|
| before (17 min) | mount bed and strip; flush; cleaning injection; the substrate step, stop and sweep of rows 46.5–56.7 on the fresh bed and strip; then 300 µL of wash buffer at 80 µL/min | A1, B1 | assay buffer | on from here to the end; pre-run trace |
| 0–1 | sample loaded; Inject Start | A1 3.4 µL/min | line 1: sample, full loop | mark |
| 1–38 | sample through the bed | A1 3.4 µL/min | loop in line | — |
| 38–39.5 | wash 1 | A1 50 µL/min | Loop Offline | — |
| 39.5–40.5 | conjugate loaded | A1 50 µL/min | line 2: conjugate, full loop | mark |
| 40.5–44.5 | conjugate through the bed, two loop volumes | A1 50 µL/min | loop in line, then Loop Offline | — |
| 44.5–46.5 | wash 2 | A1 50 µL/min | — | — |
| 46.5–49.2 | step to substrate, 215 µL | B1 80 µL/min | — | — |
| 49.2–50.2 | step down | B1 5 µL/min | — | — |
| 50.2–55.2 | **stop**: product collects in and around the bed | 0 µL/min | — | last 30 s = baseline |
| 55.2–56.7 | **sweep and read** | B1 5 µL/min | — | trace minus pre-run trace |

The margin to 60 min is 3.3 min. It covers a sampler that needs 2 min per line instead of 1.

### 4.4 Where the number comes from (nominal)

| Quantity | Value |
|---|---|
| Captured at 1 pg/mL | 2.6×10⁵ (66 % of the vial) |
| Enzymes at the read | 2.9×10⁴ (labelled 20 %, label still bound 67 %, analyte still bound 83 %) |
| Signal | 1.8 nC per pg/mL, about 20 pA over the 90 s; about a quarter of it is made while the bed is swept (Derived) |
| Blank enzymes: beads / frit / bore below the tip / capillary and line above the bed | 4.2×10⁴ / 2.9×10⁴ / 0.4×10⁴ / 6.3×10⁴ |
| Blank charge; blank equivalent | 8.4 nC (93 pA mean, Derived); 4.8 pg/mL |
| Variance at the blank | non-specific label 95 %, electrode response 4 % |
| LOD | 2.1 pg/mL |
| Upper limit by the slope criterion / curve rises up to | 1400 pg/mL / 10⁵ pg/mL |

### 4.5 Scenarios and alternatives (`tiers.md` §2, §4)

| Case | Nominal | Median [5–95 %] | P(≤ 1) / P(≤ 10) |
|---|---|---|---|
| as specified | 2.1 | 8.4 [1.0–100] | 0.05 / 0.54 |
| screened detection reagent and substrate lot (L6 + L7) | 1.4 | 6.0 [0.90–56] | 0.06 / 0.65 |
| the same with the credit for the F(ab′)₂ conjugate (L3) | 0.70 | 3.0 [0.61–27] | 0.15 / 0.82 |
| conjugate binds 25× more (S1) | 57 | 230 [23–2600] | 0.00 / 0.01 |
| the substrate's background does not decay (10⁻⁵ at the time of use) | 2.2 | 12 [1.4–130] | 0.02 / 0.45 |
| background 10⁻³ of the substrate, no decay (S4a) | 67 | 110 [16–1100] | 0.00 / 0.02 |
| no conjugate-coated wall above the bed (bound: what a valve gives) | 1.1 | 4.4 [0.67–53] | 0.11 / 0.71 |
| walls above the bed bind like blocked beads (factor 1; a coated capillary) | 1.4 | 5.1 [0.77–61] | 0.09 / 0.67 |
| transfer line 0.025 mm × 15 cm | 1.8 | 7.3 [0.93–85] | 0.06 / 0.59 |
| transfer line 0.127 mm × 20 cm | 3.5 | 14 [1.5–180] | 0.02 / 0.41 |
| bed in a fitting on the port (whole bore between bed and electrode) | 2.3 | 9.7 [1.2–120] | 0.04 / 0.50 |
| frit 1 mm² | 1.7 | 7.3 [0.89–89] | 0.06 / 0.58 |
| frit 20 mm² | 3.4 | 13 [1.4–150] | 0.03 / 0.43 |
| beads behave as when washed in tubes (factor 1) | 1.6 | 6.5 [0.82–76] | 0.07 / 0.62 |
| half the beads | 2.5 | 11 [1.2–140] | 0.04 / 0.47 |
| twice the beads | 2.3 | 8.1 [1.1–91] | 0.05 / 0.55 |
| conjugate 10 nM | 2.3 | 9.5 [1.1–110] | 0.04 / 0.51 |
| conjugate 3 nM | 2.0 | 8.2 [1.0–97] | 0.05 / 0.56 |
| stop 7 min instead of 5 (load 35 min) | 2.1 | 8.7 [1.0–110] | 0.05 / 0.53 |
| stop 3 min instead of 5 (load 39 min) | 2.0 | 8.2 [1.0–99] | 0.05 / 0.55 |
| stop 30 s | 2.1 | 8.8 [1.2–96] | 0.04 / 0.54 |
| conjugate 3 nM and stop 3 min (lowest nominal) | 2.0 | 8.0 [1.0–93] | 0.05 / 0.56 |
| the same if only 1 % of the turnovers give an electroactive product | 27 | 50 [7.0–540] | 0.00 / 0.09 |
| parked read | 2.8 | 12 [1.4–140] | 0.02 / 0.46 |
| **pump cannot stop: continuous read at 1 µL/min** | 2.8 | 11 [1.5–120] | 0.01 / 0.47 |
| pump cannot stop and cannot go below 10 µL/min | 4.1 | 15 [2.2–150] | 0.01 / 0.37 |
| strip-cell gap 0.10 mm | 2.1 | 8.4 [1.0–100] | 0.05 / 0.54 |
| strip-cell gap 0.50 mm | 2.1 | 8.5 [1.1–100] | 0.04 / 0.54 |

The two rows for a pump that cannot stop read the bed's steady current against the pre-run an hour earlier; the
drift over that hour is not in the kit, so those figures are optimistic. The length of the stop hardly matters.

### 4.6 What could make it fail, and the experiments that decide

| # | Experiment | Decides | Pass |
|---|---|---|---|
| T2-1 | Blank path: (a) an empty fritted capillary, bare and with a neutral coating, (b) one with non-immune beads, each through conjugate, wash, substrate, stop and sweep on the full path; 5 each; with beads as supplied and re-blocked in IgG-free BSA | conjugate on walls and frit against conjugate on the beads; the bovine-IgG route | walls and frit ≤ 2 × beads; blank CV ≤ 15 % |
| T2-2 | The stop: zero-flow row (docs/27 §9), volume that still passes after the step-down, baseline during the stop, the step at the sweep with and without the pre-run subtraction | whether the stop exists; the baseline | creep ≤ 0.5 µL; residual step ≤ 4 % of the step |
| T2-3 | Breakthrough: 1 ng/mL IgG at 2, 3.4, 7 µL/min, with and without the pre-run; bed viewed with the add-on's magnets in place | captured fraction; channelling; whether the pre-run harms the bed | ≥ 50 % at 3.4 µL/min |
| T2-4 | Bed-to-bed: 10 beds, 100 pg/mL | packing reproducibility | signal CV ≤ 10 % |
| T2-5 | Blanks on 10 beds; 1–1000 pg/mL | the LOD | — |

## 5. Tier 3 — anything: the bed in the loop of a valve

### 5.1 Design with one valve

| Element | Choice | Source and confidence |
|---|---|---|
| Valve | one 2-position 6-port PEEK valve (IDEX MXP9900-000) between the SM-FL and the cell, driven by the Python layer as in docs/05 §4.1; the bed in its loop | docs/07 §2 [V] |
| Bed | as tier 2: 1×10⁶ beads against a frit in a 0.2 mm capillary, connected between two ports of the valve with the shortest stubs the fittings allow | section 4.1 |
| Cell and electrode | as tier 2 (strip cell, printed carbon ED-S1PE-C21, fresh with every bed); the cell is downstream of the valve and always in the flow | |
| Capture, label | sample at 3.15 µL/min for 40 min (68 % captured); 100 µL of 5 nM conjugate at 50 µL/min | kit |
| Read | substrate into the bed; the bed is closed by its valve for 3 min while substrate flows on through the bypass and the cell at 5 µL/min; then the valve opens and the product is swept over the electrode in 90 s. Signal = charge above the level of the 30 s before the valve opens | docs/31 N4, F6 |

```
SM-FL -> V -> cell -> waste                 valve: port 1 in, port 6 out, bed between ports 2 and 5,
                                            ports 3 and 4 plugged
IN  (1-2, 5-6): the stream passes through the bed        OUT (1-6): bed bypassed and closed at both ends
sample, wash, conjugate, wash, substrate : IN
accumulation                             : OUT, pump at 5 uL/min through the bypass and the cell
read                                     : IN
```

What the valve changes against tier 2:
* The walls upstream of the bed never stand still in substrate: their product is a steady current, not part of
  the peak. The same holds for the conjugate on the electrode and in the cell, which still see it. These steady
  currents (about 12 pA from the electrode and 13 pA from the walls, Derived) are removed by the baseline; the model counts
  their noise like that of the substrate background.
* The electrode stays in flowing substrate during the accumulation, so the peak sits on a flat baseline and no
  pre-run trace is subtracted. The pre-run only checks the strip's response in flowing substrate.
* The pump never stops. The pressure that relaxes after a flow step passes through the bypass, not the closed bed.
* Only the bed, its frit and the loop of the valve (rotor passages and stubs, 10 mm² taken; with 30 mm² the LOD is
  1.7) hold conjugate that counts in the read.

### 5.2 Step table with one valve (56.7 min)

| Clock (min) | Step | Valve | BSM | SM-FL | Gamry (+0.30 V, 6 nA range) |
|---|---|---|---|---|---|
| before (10 min) | mount bed and strip; flush; cleaning injection; substrate over the strip with the bed bypassed (response check); 300 µL of wash buffer | OUT, then IN | A1, B1 | assay buffer | on from here to the end |
| 0–1 | sample loaded | IN | A1 3.15 µL/min | line 1 | mark |
| 1–41 | sample through the bed | IN | A1 3.15 µL/min | loop in line | — |
| 41–42.5 | wash 1 | IN | A1 50 µL/min | Loop Offline | — |
| 42.5–47.5 | conjugate loaded and passed | IN | A1 50 µL/min | line 2; Loop Offline at the end | mark |
| 47.5–49.5 | wash 2 | IN | A1 50 µL/min | — | — |
| 49.5–52.2 | substrate to the bed, 215 µL | IN | B1 80 µL/min | — | — |
| 52.2–55.2 | accumulation | OUT | B1 5 µL/min | — | mark at the switch; last 30 s = baseline |
| 55.2–56.7 | sweep and read | IN | B1 5 µL/min | — | mark at the switch; window |

Bench preparation: as section 4.2 steps 1 and 2; the capillary is then mounted between ports 2 and 5 with
zero-dead-volume fittings and the loop is filled with assay buffer. No sleeve and no magnet check are needed.

### 5.3 The transfer to a second bed (conditional)

| Element | Choice | Source and confidence |
|---|---|---|
| Second valve and bed | a second valve of the same kind between the first and the cell; in its loop a read bed of 3×10⁶ beads | docs/07 §2 [V] |
| Capture bed (bed 1) | 1×10⁶ streptavidin beads holding the capture F(ab′)₂ through a biotin on a **cleavable link**, coated at about 3 µg per mg of beads (2.5×10⁵ per bead, the model's density) | link chemistry UNVERIFIED |
| Read bed (bed 2) | beads carrying an antibody against a **hapten tag** on the capture F(ab′)₂ | UNVERIFIED; replaces the "phase-2 antibody not yet identified" of docs/06 §4.12 |
| Transfer | eluent held on bed 1 for 5 min with bed 1 closed, then pushed through bed 2 at 2 µL/min; wash | released fraction 0.35 (0.05–0.74), **no rate known**; non-specific label that comes along ×0.1 (0.01–0.5), `ma.design_levers`; both UNVERIFIED |

Why the read bed is three times larger. Bed 2 binds the tag on the capture antibody, so it takes every released
capture F(ab′)₂, with or without analyte: 2×10¹¹ molecules against 10⁴–10⁵ complexes. With a bed of the same size
the sites would outnumber the antibodies only 1.2-fold and 17 % of the complexes would pass (0.65 against 0.53 at a
release of 0.7); with bed 1 coated at the vendor's capacity, 64 % would pass (Derived by the second reviewer,
docs/31 M3; the kit computes the re-capture with site depletion). Three times the beads on bed 2, and bed 1 coated
at a third of the vendor's capacity, keep the read bed far from full.

```
SM-FL -> V1 -> V2 -> cell -> waste          both valves plumbed as in section 5.1
sample, wash, conjugate, wash : V1 IN,  V2 OUT    the conjugate does not enter the loop of V2
eluent                        : V1 IN until bed 1 is filled; V1 OUT for the hold; V1 IN + V2 IN for the push
wash of bed 2, substrate      : V1 OUT, V2 IN
accumulation                  : V2 OUT, pump at 5 uL/min through the bypasses and the cell
read                          : V2 IN
```

| Clock (min) | Step | Valves | BSM | SM-FL | Gamry (+0.30 V, 6 nA range) |
|---|---|---|---|---|---|
| before (10 min) | as section 5.2, both beds bypassed for the response check | | A1, B1 | assay buffer | on |
| 0–1 | sample loaded | V1 IN, V2 OUT | A1 5.0 µL/min | line 1 | mark |
| 1–26 | sample through bed 1 (55 % captured) | V1 IN, V2 OUT | A1 5.0 µL/min | loop in line | — |
| 26–27.5 | wash 1 | V1 IN, V2 OUT | A1 50 µL/min | Loop Offline | — |
| 27.5–32.5 | conjugate (10 nM) loaded and passed | V1 IN, V2 OUT | A1 50 µL/min | line 2; Loop Offline at the end | mark |
| 32.5–34.5 | wash 2 | V1 IN, V2 OUT | A1 50 µL/min | — | — |
| 34.5–36 | eluent loaded; 25 µL after the Inject Start mark of line 3 the eluent fills bed 1 | V1 IN, V2 OUT | A1 50 µL/min | line 3 | mark |
| 36–40 | hold; the rest of the eluent is flushed through the bypasses and the cell | V1 OUT, V2 OUT | A1 50 µL/min | Loop Offline at 40 | — |
| 40–41 | hold; the pressure relaxes at the push flow | V1 OUT, V2 OUT | A1 2 µL/min | — | — |
| 41–45 | push, 8 µL | V1 IN, V2 IN | A1 2 µL/min | — | — |
| 45–47 | wash of bed 2 | V1 OUT, V2 IN | A1 50 µL/min | — | — |
| 47–49.7 | substrate to bed 2, 215 µL | V1 OUT, V2 IN | B1 80 µL/min | — | — |
| 49.7–56.7 | accumulation | V1 OUT, V2 OUT | B1 5 µL/min | — | last 30 s = baseline |
| 56.7–58.2 | sweep and read | V1 OUT, V2 IN | B1 5 µL/min | — | window |

Conditions of this table: the valve V1 is switched by volume after the Inject Start mark of line 3, not by the
clock; the volume from bed 1 to bed 2 (two rotor passages and the stubs) is at most 2.5 µL, a third of the push,
and is to be taken from the valve's data sheet (UNVERIFIED); the eluent crosses the electrode at 36–40 min and the
strip has 15 min of flow to recover before the read. The label waits 17 min from the end of the conjugate step to
the accumulation; with the unscreened detection reagent 63 % of it is gone.

The transfer chemistry is not settled. Three routes, none with a verified rate at 5 min:

| Route | How | What is known |
|---|---|---|
| Cleavable link + hapten (taken for the model) | capture F(ab′)₂ carries a biotin on a disulfide spacer and a hapten (dinitrophenyl or fluorescein); a reductant in the eluent cuts the spacer; bed 2 holds anti-hapten antibody. A photocleavable biotin with a 365 nm lamp on the loop of V1 is the variant without reductant | UNVERIFIED throughout (reagent part numbers not checked). The reductant also meets the hinge disulfides of both F(ab′)₂ and of the analyte, and the enzyme; alkaline phosphatase has been run with TCEP in the substrate solution (Akanda2011a [V-abs], docs/29 A.2) |
| Desthiobiotin displaced by biotin (docs/06 §4.12) | as planned for Stage 1C, with a hapten tag for bed 2 | too slow: 0.3–26 % released in 5 min (Derived by the reviewer from K_d ≈ 10⁻¹¹ M, UNVERIFIED); Hirsch2002 [V-abs] gives no rate; "the rate of elution of desthiobiotinylated materials is too slow" (Ying, Branchaud and Corry 2011 [V full text, reviewer; `review_chemistry.md` C8]). Model: 3.7 nominal, worse than no transfer |
| Dinitrophenyl first, streptavidin second (Ishikawa1990, Hashida1997) | the original immune-complex transfer; the read bed is then the streptavidin bed, which has the larger capacity | developed with elutions of hours (recalled, UNVERIFIED) |

Bench preparation for the transfer (UNVERIFIED as a recipe): capture F(ab′)₂ labelled with the cleavable biotin and
the hapten; bed 1 coated at 3 µg per mg; anti-hapten antibody, biotinylated, on streptavidin beads at 10 µg per mg
for bed 2; both capillaries packed as in section 4.2 (bed 2 is 1.8 mm long) and mounted in the loops.

### 5.4 Numbers (`tiers.md` §2, §5)

| Case | Nominal | Median [5–95 %] | P(≤ 1) / P(≤ 10) |
|---|---|---|---|
| **one valve, as specified** | 1.2 | 5.1 [0.78–58] | 0.09 / 0.69 |
| one valve, screened detection reagent and substrate lot (L6 + L7) | 0.88 | 3.7 [0.71–34] | 0.11 / 0.77 |
| one valve, the same with the credit for the F(ab′)₂ conjugate (L3) | 0.46 | 2.0 [0.49–16] | 0.23 / 0.90 |
| one valve, with a reference channel as well (L5) | 1.1 | 4.4 [0.70–49] | 0.11 / 0.71 |
| one valve, conjugate binds 25× more (S1) | 36 | 140 [13–1600] | 0.00 / 0.03 |
| one valve, the substrate's background does not decay | 1.3 | 6.7 [0.98–79] | 0.06 / 0.62 |
| one valve, background 10⁻³ of the substrate, no decay (S4a) | 27 | 52 [6.6–550] | 0.00 / 0.10 |
| one valve, accumulation 7 min instead of 3 (load 36 min) | 1.3 | 5.4 [0.76–64] | 0.09 / 0.67 |
| one valve, conjugate 10 nM | 1.4 | 5.6 [0.80–64] | 0.08 / 0.66 |
| one valve, conjugate 3 nM | 1.2 | 4.9 [0.79–55] | 0.09 / 0.69 |
| one valve, loop walls 30 mm² instead of 10 mm² | 1.7 | 7.3 [0.93–82] | 0.06 / 0.60 |
| **transfer as specified (release 0.35 [0.05–0.74], non-specific ×0.1)** | 1.1 | 5.8 [0.64–280] | 0.12 / 0.61 |
| transfer, release 0.7 in 5 min (the value docs/05 assumed for its tube protocol) | 0.53 | 2.0 [0.37–87] | 0.28 / 0.81 |
| transfer at its optimistic bounds (release 0.74, ×0.01) | 0.24 | 1.1 [0.24–27] | 0.47 / 0.90 |
| transfer at its pessimistic bounds (release 0.05, ×0.5) | 34 | 120 [9.7–4800] | 0.00 / 0.05 |
| transfer by desthiobiotin and biotin, 5 min | 3.7 | 32 [1.9–2100] | 0.02 / 0.28 |
| transfer, release 0.7, read bed no larger than the capture bed (sites per antibody 1.2) | 0.65 | 3.4 [0.46–150] | 0.20 / 0.72 |
| the same, capture bed coated at the vendor's capacity (sites per antibody 0.36) | 1.5 | 7.4 [0.81–330] | 0.08 / 0.56 |
| transfer, screened detection reagent and substrate lot (L6 + L7) | 0.43 | 3.0 [0.48–42] | 0.19 / 0.79 |
| transfer, release 0.7, screened reagents (L6 + L7) | 0.21 | 1.2 [0.29–11] | 0.41 / 0.94 |
| transfer, screened reagents and the credit for the F(ab′)₂ conjugate (L3 + L6 + L7) | 0.26 | 1.8 [0.37–21] | 0.28 / 0.89 |
| transfer, the substrate's background does not decay | 1.3 | 9.9 [0.89–640] | 0.06 / 0.50 |
| transfer, conjugate binds 25× more (S1) | 27 | 140 [7.8–8500] | 0.00 / 0.07 |

Nominal chain with one valve: 2.7×10⁵ captured (68 %), 3.2×10⁴ enzymes at the read per pg/mL (labelled 20 %, label
still bound 71 %, analyte still bound 83 %), 1.1 nC per pg/mL; blank 4.2×10⁴ enzymes on the beads, 2.9×10⁴ on the
frit and 1.7×10⁴ on the loop walls, equivalent to 2.8 pg/mL; variance: non-specific label 93 %, electrode response
4 %, drift 2 %.

Nominal chain with the transfer: 2.2×10⁵ captured (55 %), transfer 35 %, 8.2×10³ enzymes at the read per pg/mL
(label still bound 37 %), 0.51 nC per pg/mL; blank equivalent 2.2 pg/mL; variance: non-specific label 74 %, drift
14 %, substrate background 6 %.

When the transfer pays. By the nominal model it beats one valve when more than about 30 % of the complex is
released in 5 min (Derived: 1.1 at 0.35 against 1.2), and by a factor of two or more only with a release of 0.7 or
a screened detection reagent. At its pessimistic bounds it is almost thirty times worse than one valve.

Not in the design, as runners-up: a second potentiostat channel with a reference bed (1.2 → 1.1); a pre-electrolysis
electrode or a reversed-phase guard column in the substrate line, to remove free hydroquinone before the bed
(useful only if the substrate's background does not decay; the project's bench test E1.2b covers the first, the
second is UNVERIFIED); redox cycling on an interdigitated array (it amplifies the blank with the signal).

### 5.5 What could make it fail

| # | Experiment | Decides | Pass |
|---|---|---|---|
| T3-1 | One valve: the tier-2 experiments T2-1 and T2-3 to T2-5 on the valve set-up; conjugate on the loop of the valve; time the sampler needs between lines | the tier-3 design | as tier 2; loop walls ≤ beads |
| T3-2 | Blank handling: blanks prepared in a hood with dedicated consumables against open-bench blanks | the contamination floor | ≤ 0.1 pg/mL equivalent (docs/05 §5 U9) |
| T3-3 | Transfer at the time scale of the design, first in tubes, then in two beds: release in 5 min for each route, re-capture at 2 µL/min with the full load of capture antibody, conjugate that comes along; leak of capture antibody from bed 1 over 40 min | whether a transfer exists | released ≥ 50 %; blank reduced ≥ 5× (docs/05 §5 U8) |
| T3-4 | Effect of the eluent on the enzyme label and on the complex; the strip's background and response before and after the eluent has crossed it | the cleavable route | ≥ 80 % of the enzyme activity after 5 min; background back within 3 % in 10 min |

### 5.6 Relation to the earlier design

The dosing-pump, stirred-chamber and magnetic-trap design of docs/05 §4.1 is the other "anything" design. Its model
numbers (docs/08 §10.1): nominal 0.60, median 3.5 [0.51–158], P(success) 0.16 as specified; with the transfer lever
nominal 0.29, median 1.5, P 0.33. With the 10 min half-life of hydroquinone they hardly move (nominal 0.60 → 0.62,
median 3.49 → 3.46, P 0.156 → 0.154; `results/tier_round/earlier_designs_halflife.md`). They cannot be set against
the tier figures: the kit adds the unit-to-unit spread of hand-made consumables, the frit, the loop walls and a
bounded transfer, and the earlier model adds a reuse term and a success criterion that includes the range (for the
primary 0.154 against 0.174 for the LOD alone). What can be said: both rest on the same two measurements
(non-specific binding of the conjugate, background of the substrate), both need a working transfer to go well
below 1 pg/mL, and the valve design needs one valve where the earlier design needs several valves, a syringe pump
with a selection valve, an incubation cup and a magnetic trap. The earlier design keeps the simultaneous
incubation and the unattended queue, which this round does not ask for.

## 6. Comparison

### 6.1 The same quantities side by side (nominal)

| | Tier 1 | Tier 2 | Tier 3, one valve | Tier 3 with transfer |
|---|---|---|---|---|
| Captured fraction of the sample | 8.2 % | 66 % | 68 % | 55 %, of which 35 % is transferred |
| Enzymes at the read per pg/mL | 1.2×10⁴ | 2.9×10⁴ | 3.2×10⁴ | 8.2×10³ |
| Signal per pg/mL | 2.9 pA for 60 s (0.17 nC) | 1.8 nC | 1.1 nC | 0.51 nC |
| Blank equivalent (pg/mL) | 5.9 | 4.8 | 2.8 | 2.2 |
| Largest variance term | non-specific label 68 % | non-specific label 95 % | non-specific label 93 % | non-specific label 74 % |
| Needs the pump to stop | no | yes | no | no |
| Lowest flow | 2.9 µL/min | 3.4 µL/min | 3.15 µL/min | 2 µL/min |
| New consumables per determination | strip | capillary bed, strip | capillary bed, strip | two beds, strip |

### 6.2 Largest sensitivities (one parameter at its bounds, all others at their best estimate; `tiers.json`)

| Parameter, value [low–high] | Tier 1: LOD at low / high | Tier 2 | Tier 3, one valve | Tier 3 with transfer |
|---|---|---|---|---|
| detection off-rate 8.6×10⁻⁴ s⁻¹ [3×10⁻⁶–8.3×10⁻³] | 2.6 / 61 | 1.3 / 94 | 0.84 / 36 | 0.38 / 8100 |
| non-specific rate 4×10⁻¹¹ m/s [0.8–40×10⁻¹¹] | 2.1 / 30 | 0.43 / 22 | 0.32 / 13 | 0.47 / 10 |
| surface factor of the coated gold 3 [1–30] | 2.5 / 23 | — | — | — |
| enzyme turnover 1000 s⁻¹ [100–6000] | 20 / 3.1 | 2.4 / 2.1 | 2.4 / 1.3 | 4.3 / 1.0 |
| label factor of the conjugate 0.04 [0.01–0.15] | 2.1 / 12 | 0.53 / 7.9 | 0.37 / 4.8 | 0.49 / 3.7 |
| current through the coated gold 1 [0.1–1] | 20 / 3.6 | — | — | — |
| detection on-rate 3.9×10⁵ M⁻¹s⁻¹ [0.9–12×10⁵] | 11 / 2.3 | 8.2 / 0.84 | 5.0 / 0.51 | 3.9 / 0.52 |
| unit-to-unit CV, hand-coated electrodes 0.15 [0.05–0.4] | 2.8 / 7.1 | — | — | — |
| surface factor of tubing and walls 3 [1–30] | 3.4 / 7.4 | 1.4 / 11 | 1.1 / 3.5 | 0.94 / 2.9 |
| surface factor of the bed 3 [1–30] | — | 1.6 / 7.9 | 0.86 / 6.8 | 0.81 / 5.1 |
| surface factor of the frit 10 [1–100] | — | 1.7 / 6.0 | 0.89 / 5.0 | 0.83 / 3.8 |
| capture site density 1×10¹⁶ m⁻² [0.2–1.5×10¹⁶] | 6.2 / 3.4 | 5.6 / 1.8 | 3.3 / 1.1 | 4.2 / 0.90 |
| conjugate binding to the capture antibody 1 [1–3] | 3.6 / 9.3 | 2.1 / 6.3 | 1.2 / 3.8 | 1.1 / 3.0 |
| released fraction in the transfer 0.35 [0.05–0.74] | — | — | — | 7.5 / 0.50 |
| non-specific label that comes along in the transfer 0.1 [0.01–0.5] | — | — | — | 0.51 / 4.8 |

### 6.3 What holds in every case run

* Tier 3 with one valve < tier 2 < tier 1 in nominal and median LOD, as specified and in every scenario of
  `tiers.md` §2 except one kind: if only 1 % or 0.1 % of the turnovers give an electroactive product, tier 2 (13;
  120) is below tier 3 with one valve (20; 200) at nominal, because its longer stop leaves more current.
* The transfer is below one valve only with a release above about 30 %; over the sampled range its median is
  higher (5.8 against 5.1) and its 95th percentile five times higher.
* A substrate whose oxidisable background is 10⁻³ and does not decay (scenario S4a of docs/05 §3) puts the tiers at
  390, 67, 27 and 58 pg/mL. A conjugate that binds 25× more than the model assumes (S1) puts them at 76, 57, 36
  and 27. The project decides on these two quantities by its G1 rule (docs/06 §4.11).
* Screening the detection reagent (L6; L7 has no effect when the background decays) is worth a factor of 1.3 in
  tier 1, 1.5 in tier 2, 1.4 with one valve and 2.5 with the transfer.

### 6.4 Why the judgement is above the model

Not in the model: channelling in a hand-packed bed; drift of a printed reference; the pump at 2–5 µL/min against
40–60 psi; protein on an electrode that every sample and conjugate now passes; conjugate that builds up on the
transfer line from run to run; bovine IgG in blockers; temperature; the true unit-to-unit spread of hand-made
consumables. The model's parameter for human IgG that reaches a blank from the laboratory is zero at nominal and
sampled up to 0.45 pg/mL.

Design inputs that are uncertain but not sampled, so that the 5–95 % ranges are narrower than the uncertainty of
the text: the gap of the cell (tier 1: 2.8–5.6), the bore length (5 mm assumed), the frit's wetted area (tier 2:
1.7–3.4), the walls of the valve loop (1.2–1.7), the volume between bed and electrode, the age of the substrate
solution (1–8 h), and the capacity of the read bed in the transfer.

Limits of validity: the wall-jet mapping assumes creeping flow in a thin gap; at 200 µL/min the Reynolds number at
the bore is about 1 and the washes and the tier-1 read are at its edge (docs/31 N9). The read at 300 µL/min is
beyond it and needs a cell that holds the pressure.

Each of these is more likely to hurt than to help.

## 7. Bench order

1. **The two questions of section 2.6** (half a day). They decide the substrate and the size of its background
   for these designs and for the earlier ones.
2. **Instrument facts** (docs/27 §9, two days): low flow against the restrictor, zero-flow row, Loop Offline and
   the composition front (dye), the volume that passes after a flow step, the internal volume of pump A, the time
   between sampler lines, cell gap, cell pressure at 200 µL/min, loop draw, reference stability.
3. **The shared Stage 1A experiments of docs/06** (E1.1 readout, E1.2 free hydroquinone, E1.3 conjugate
   non-specific binding on beads), with the MicruX strip in its cell as the electrode, plus one arm from the
   review: beads as supplied against beads re-blocked in IgG-free BSA. Gate G1a is unchanged.
4. **Tier 2**: T2-1 (walls and frit), T2-2 (the stop), T2-3 (breakthrough), T2-4, T2-5.
5. **Tier 1 beside it** if wanted: T1-1 and T1-2 need only strips, thiols, streptavidin and conjugate.
6. **Tier 3**: one valve with the bed in its loop as soon as it can be had (T3-1); the second valve, the second
   bed and the transfer only after T3-3.

This round changes no gate, no kill criterion and no order in docs/06. Whether its experiments are added to that
plan is the user's decision (section 8).

## 8. Choices the user may overrule, and open questions

Choices made here:
1. Tier 1 on a printed gold strip with a thiol monolayer (model 3.6) rather than on printed carbon (11).
2. Tier 1 reads at 200 µL/min between windows in substrate buffer without substrate; it uses about 0.8 mL of
   substrate solution and a second buffer line per determination.
3. Tier 2 uses the project's 2.8 µm beads in a fritted capillary, a fresh strip with every bed, 5 nM conjugate and
   a 5 min stop: 5 % above the lowest nominal LOD, for more current and a longer calibration.
4. Tier 3 is the same bed in the loop of one valve. The transfer to a second bed is described and computed but
   not recommended before its test.
5. The Waters 40 µm restrictor for all tiers, at the price of the 1000 psi guidance during the slow steps.
6. The range is reported, not enforced (docs/26 §3).
7. The gap of the strip cell is taken as 0.2 mm (the user's 10 µL); MicruX states < 5 µL, which would be ≤ 0.1 mm.
8. One stability of hydroquinone for the whole liquid path (half-life 10 min, 2 min to 2 h), instead of the
   model's 2 h in the bed and a constant background in the reservoir (docs/31 C5, M2); `params/` is not edited.

Questions only the user can answer (docs/27 §9, docs/28 §8):
1. Which flow add-on and which electrodes are in hand (part numbers on the packs)?
2. Where does "10 µL" come from?
3. Does a BSM method accept a 0.000 mL/min row? Is a restrictor installed, and which?
4. Is the full-loop overfill set to 2× on this sampler (the Waters default draws five loop volumes)?
5. Is there a UV detector and a reversed-phase column on the stack (for the product test)?
6. Does a fritted capillary count as a fitting (an in-line filter is one)? If it does, the tier-2 design is also
   the best tier-1 design, and the electrode-capture design becomes its runner-up.
7. Should the experiments of section 7, above all the two questions of section 2.6, enter the bench plan
   (docs/06), and before or after gate G1a?

## 9. Reproduction and references

```bash
pip install -e .
python scripts/tier_round/check_tierkit.py              # 36 checks
python scripts/tier_round/run_tiers.py                  # results/tier_round/tiers.md, tiers.json (about 2 min)
python scripts/tier_round/doc_tables.py --check         # the tables of this document against tiers.json
python scripts/tier_round/earlier_designs_halflife.py   # section 5.6
```

Designs: `scripts/tier_round/designs.py` (`tier1`, `tier2`, `tier3`) and `run_tiers.py`. Parameters added by this
round: `scripts/tier_round/tier_params.yaml` (UNVERIFIED engineering estimates unless a source is named). Reviewer
reports and their scripts: `results/tier_round/review_*.md`, `review2_*.md`, `scripts/tier_round/review*.py`.

References are held where they were checked: MicruX and parts in docs/28 §9; Waters in docs/27 Appendix A;
literature keys (Nishimura2011, Bekhit2021, Buckey2022, Das2007, Kwon2008, Akanda2011a, Akanda2013,
DiazGonzalez2005, Squires2008 and others) in docs/29 A.R and B.R and in docs/01; Ishikawa1990, Hashida1997 and
Hirsch2002 in docs/05; reagents in docs/07 §7; Ying, Branchaud and Corry 2011, the hydroquinone half-lives and the
vendor pages re-opened by the reviewers in `results/tier_round/review_chemistry.md`.
