# 30 — Three implementations for the lowest LOD on the equipment in hand

Status: 2026-11-17, **Revision B** (after the independent review, docs/31). Written by the orchestrator. Inputs:
docs/26 (brief and interview), docs/27 (capability map), docs/28 (MicruX hardware), docs/29 (literature), the model
(`src/elisa_sim`) and the calculation kit of this round (`scripts/tier_round/`, 36 checks pass). Every LOD below is a
model prediction, not a measurement. "Nominal" = all parameters at their best estimate. "Median [5–95 %]" = Monte
Carlo over the parameter bounds (n = 2000, seed 20261111); the interval is a scenario range, not a confidence
interval (docs/03 §7). P = fraction of draws. Numbers come from `results/tier_round/tiers.md`.

What Revision B changed: the review found blank terms the first version left out (conjugate on the walls upstream of
the electrode or bed, no reference window next to the tier-1 read, an unsteady baseline in the tier-2 read, a
transfer efficiency above what the bed physics allows) and a method error (no Loop Offline). The designs and the
kit were changed and the predicted LODs rose about threefold. docs/31 §3 lists every finding and what was done.

## 0. Summary

One assay, built three ways. All three are sequential sandwich assays for human IgG with an alkaline-phosphatase
label and a hydroquinone-releasing substrate, read by holding one electrode at the hydroquinone oxidation plateau
and integrating the current. They differ in where the IgG is captured.

| | **Tier 1 — consumables only** | **Tier 2 — plus passive parts** | **Tier 3 — anything** |
|---|---|---|---|
| Capture | on the working electrode itself: printed gold strip (3 mm), biotin-OEG monolayer, streptavidin, biotinylated anti-Fc F(ab′)₂ | on 1×10⁶ streptavidin beads (2.8 µm) packed by hand against a frit in a capillary whose tip sits in the cell's inlet bore, 1 mm above a printed carbon electrode | on the same kind of bed, in the loop of a valve; the captured complex is then released and re-captured on a second, clean bed in the loop of a second valve, and that bed is read |
| Added to the equipment in hand | strips, thiols, reagents, restrictor, a 50 µm transfer line | the same reagents on beads; fritted capillary, sleeve, fitting | one 6-port valve for the first step (the capture bed in its loop), a second valve and bed for the transfer; a cleavable link and a hapten tag on the capture antibody; Python valve control |
| Read | substrate flows at 150 µL/min; current of the enzyme on the electrode for 2 min, between two buffer windows at the same flow | flow stopped 7 min (product collects in the bed), then swept over the electrode in 90 s | bed 2 closed by its valve for 7 min while the cell stays in flow, then swept |
| Injection to result | 56.9 min | 58.7 min | 58.2 min |
| LOD nominal (pg/mL) | **9.4** | **2.6** | **0.62** |
| LOD median [5–95 %] | 35 [4.4–560] | 13 [1.4–170] | 4.8 [0.54–260] |
| P(LOD ≤ 1 pg/mL) / P(≤ 10) | 0.00 / 0.16 | 0.02 / 0.43 | 0.15 / 0.64 |
| With the detection reagent and substrate lot screened (L6 + L7) | 4.5; 16 [2.6–130] | 1.7; 7.4 [1.0–78] | 0.22; 1.5 [0.32–23]; P(≤ 1) 0.34 |
| What limits it | the substrate's own hydroquinone: a 107 pA current under a 1.6 pA per pg/mL signal; then drift | conjugate stuck to the walls upstream of the bed and to the frit, more than to the beads | the conjugate that comes along in the transfer; then the substrate background |
| Depends on, unproven | hydroquinone oxidation through the monolayer; a background stable to 3 % over an hour | a zero-flow step in the pump method (fallback 3.0 nominal, its drift not modelled); the frit's area | the transfer chemistry itself (no release rate is known; without the transfer, one valve alone gives 1.5) |

Reading of the table.
* **Each tier is about four times lower than the one before.** Tier 1 → 2: the bed takes 66 % of the sample instead
  of 8 %, and its product is read as one plug. Tier 2 → 3: a valve keeps the conjugate-coated walls upstream of the
  bed out of the read (one valve alone: 1.5 nominal, median 6.9), and the transfer to a second bed leaves most of the
  first bed's own conjugate behind.
* **None of the three is predicted to reach the project's 1 pg/mL as specified** (P 0.00, 0.02, 0.15). With screened
  reagents and the credit for the F(ab′)₂ conjugate, tier 3 does in 45 % of the draws and tier 2 in 13 %.
* **Without valves, the conjugate wets every wall between injector and waste, and that is what tiers 1 and 2 pay
  for.** The earlier design of this project stands at a median of 3.5 pg/mL, P 0.16 (docs/08 §10; reproduced here:
  3.49, 0.156). Its numbers and these are not on the same footing: the kit counts terms the earlier model does not
  have (unit-to-unit spread of hand-made consumables, frit, walls in the read path, a 10 min instead of 2 h
  half-life of hydroquinone). Neither is shown to be better than the other (section 5.5).
* The orchestrator's judgement of what a first working version would show, given what the model still does not
  carry (section 6.4): tier 1 10–100 pg/mL, tier 2 3–30 pg/mL, tier 3 1–10 pg/mL if the transfer works.
* **One chemistry question stands above all three tiers and above the earlier designs** (review finding C1,
  section 2.5): alkaline phosphatase removes one phosphate per turnover, so at picomolar enzyme the product of
  hydroquinone *di*phosphate should be the monophosphate, not hydroquinone. If the monophosphate is not oxidised at
  the read potential, every signal in this document is too high by 10² to 10⁵. A half-day test decides; the
  substrate would then be the monophosphate (p-hydroxyphenyl phosphate) or ascorbic acid 2-phosphate.

**Recommendation.** First the half-day product test, because it decides the substrate for everything. Then build
tier 2: it uses the strip cell the user named and the reagents already in the bill of materials (docs/07 §1), and
its bed is the bed of tier 3. If one 6-port valve can be bought, put the bed in its loop at once (tier 3 without the
transfer): by the model it is 1.7 times lower than tier 2 and needs no zero-flow step. The second valve, the second
bed and the transfer are added only after the transfer has passed a tube test at the 5 min time scale (section 5.4).
Tier 1 is the cheapest to try and the least likely to pass 10 pg/mL.

## 1. What sets the LOD on this equipment

1. **The blank is non-specifically bound conjugate, wherever its product can reach the electrode.** As in docs/04
   and docs/05, the LOD is 3 × the SD of that blank. For a short conjugate exposure the ratio of specific to
   non-specific label on a surface is (captured IgG per area) × k_on,detection / (non-specific rate × surface
   factor): it does not depend on the conjugate concentration or on the area.
2. **Without a valve the conjugate wets every wall from the injector to waste**, and the substrate later follows
   the same path. Under flow, the product of all upstream walls arrives at the electrode with the stream. In a
   stopped line, it stands in the liquid right behind the bed and follows the plug into the read window. The first
   version of this document counted only the capture surface and its immediate surroundings (docs/31 N2, N3).
3. **Both MicruX flow add-ons are wall-jet cells** (docs/28 §1 [V]): the stream enters through a bore above the
   centre of the working electrode and leaves radially through a gap whose height is not published. The whole
   sample passes over the electrode. For a thin gap in creeping flow the capture problem is the channel problem in
   the swept area (`scripts/tier_round/README.md` B). At 3 µL/min a 3 mm electrode under a 0.2 mm gap takes 7.9 % of
   the sample (mass-transfer coefficient 0.86×10⁻⁶ m/s against a reaction velocity of 4.2×10⁻⁶ m/s). Stop-and-go
   loading is no better, so the sample is pumped slowly and continuously.
4. **A bed of small beads captures by reaction, not by transport**: 1×10⁶ beads of 2.8 µm are 24 mm² and take 66 %
   of a 100 µL sample at 3.4 µL/min.
5. **Product formed on the electrode is collected in full at any flow; product that arrives with the stream is
   collected only at the stream's conversion**, which falls with flow: 99 % at 1 µL/min, 62 % at 5 µL/min, 7.4 % at
   150 µL/min for the 3 mm electrode under a 0.2 mm gap (kit, `cell_conversion`). Tier 1 therefore reads at a fast flow, where the electrode sees its own enzyme in full and the
   upstream walls at 7 %; tiers 2 and 3 sweep their plug slowly.

From the literature (docs/29 Part A): p-aminophenol fouls printed carbon and gold (Buckey2022 [V-abs]), so the read
is hydroquinone; amplification by a reductant in solution is shown only on ITO and on gold under long monolayers
(Das2007, Kwon2008, Akanda2011a, Akanda2013 [V-abs]) and amplifies the blank with the signal; a potential step
charges about 1 µC on a 3 mm printed electrode, a thousand times the signal at the LOD, so the potential is held.

## 2. What the three implementations share

### 2.1 Reagents (docs/07 §1; evidence labels as given there; vendor pages re-opened by the reviewer, docs/31 C)

| Item | Choice | Note |
|---|---|---|
| Capture antibody | biotinylated goat F(ab′)₂ anti-human IgG, Fcγ-specific, minimal cross-reaction to bovine, horse, mouse (Jackson 109-066-098) | [V] reviewer; tier 3 needs it with other tags (section 5.1) |
| Detection conjugate | alkaline-phosphatase goat F(ab′)₂ anti-human IgG, F(ab′)₂-specific (Jackson 109-056-006) | [V] reviewer: **not** adsorbed against bovine proteins and stabilised with BSA; a conjugate adsorbed against bovine serum is to be found (part UNVERIFIED) |
| Streptavidin beads (tiers 2, 3) | Dynabeads M-280 Streptavidin 11205D, 10 mg/mL, 6–7×10⁸ beads/mL, about 10 µg biotinylated antibody per mg (docs/28 R32 [V]); 1×10⁶ beads = 1.5 µL of stock and hold up to about 8×10⁵ F(ab′)₂ per bead (Derived) | the stock holds 0.1 % ordinary BSA: wash and re-block in IgG-free BSA (docs/06 §4.0; docs/31 C4) |
| Substrate | HQDP, Metrohm DropSens DRP-HQDP-0.5G; no purity, free-hydroquinone or monophosphate specification | [V]; subject to the product test of section 2.5 |
| Standard | NISTmAb RM 8671 (after gate G1a), polyclonal human IgG for development | docs/07 §1 |
| Blocker and carrier | IgG-free BSA | bovine IgG cross-reacts with anti-human-IgG reagents (docs/29 C.2) |

The acceptance criteria for the antibody pair are those of docs/05 §4.1 (half-lives ≥ 1 h, bench item U2). The
detection conjugate's off-rate is among the two largest sensitivities in every tier: at its best estimate
(half-life 13 min) 28–63 % of the label leaves between the conjugate step and the read.

### 2.2 Solutions

| Line or vial | Content | Note |
|---|---|---|
| BSM A1 | wash buffer: 50 mM Tris-HCl pH 7.5, 150 mM NaCl, 0.05 % Tween 20 | no phosphate (docs/08 B1) |
| BSM B1 | substrate in 0.1 M Tris pH 9.5, 1 mM MgCl₂, 150 mM NaCl: 0.3 mM (tier 1), 1 mM (tiers 2, 3) | fresh daily, dark; the chloride keeps a printed silver reference where it was in A1 (docs/28 §4). Tris buffers weakly at pH 9.5 (8 mM per pH unit); 1 M diethanolamine pH 9.8 is the alternative to compare in the product test (docs/31 C9) |
| BSM A2 | water, then 10 % methanol for storage | docs/02 §1.2 |
| Tray vial, 4 °C | conjugate, 10 nM in assay buffer (wash buffer + 1 % IgG-free BSA) | full-loop injection |
| Tray vial | assay buffer, for a loop-cleaning injection before each determination | |
| Tray vial | 1 µM hydroquinone, kept at pH 7 and diluted into substrate buffer just before use | hydroquinone autoxidises within minutes at pH 9.5 (docs/31 C5) |
| Tray vial (tier 3) | eluent (section 5.1) | |
| Sample vial | sample only; standards and blanks are made in assay buffer | docs/26 §3 |

### 2.3 Flow path, control and timing rules

* BSM → mixer → restrictor → SM-FL (100 µL loop, full loop) → transfer line of **50 µm bore, 15 cm** → cell → short
  open waste line. The short narrow line matters: its 24 mm² of wall carries conjugate (fact 2). With a 0.127 mm ×
  20 cm line tier 2 goes from 2.6 to 4.5 pg/mL. Restrictor: 25 µm × 30 cm for tier 1 (67 psi per µL/min: 10 000 psi
  at 150 µL/min, 200 psi at 3 µL/min), 25 µm × 45 cm for tiers 2 and 3 (docs/27 §3; availability UNVERIFIED). The
  transfer line itself adds 25 bar at 150 µL/min and 13 bar at 80 µL/min (Derived, Hagen–Poiseuille).
* **Loop Offline is set in every line's method**: after the sample has left the loop (line 1), and after two loop
  volumes of flush behind the conjugate (line 2), always before a step to substrate. A step to substrate is
  **215 µL** of B1 (95 % of full strength at the cell; docs/27 §1, docs/31 F1).
* One determination is two sample-set lines after a pre-run line; tier 3 has three.
* Flows: sample 3–5 µL/min; conjugate 50 µL/min; washes and composition steps 50–150 µL/min. Before any stop the
  flow is stepped down to 5 µL/min for 1 min so that the pressure upstream of the restrictor has relaxed
  (docs/27 §2, docs/31 F2).
* The Gamry holds the read potential from the pre-run to the end, on one fixed current range per tier (600 pA
  range tier 1, 6 nA tiers 2 and 3), and records at 2–10 Hz; Inject Start of each line and one timed switch mark
  the record (docs/27 §5). The potential is set once per strip lot, on the plateau of a voltammogram of
  enzyme-generated product in substrate buffer (section 2.5), not from a hydroquinone standard alone.
* Washes are 1.5 min after the sample and 2 min after the conjugate, not below the minima of docs/05 §1.1 (1 min
  and 2 min), because wash efficiency is not modelled.
* Before each determination (not counted in the 60 min, docs/26 §3): mount the fresh consumables, flush, one
  full-loop injection of assay buffer to clean needle and loop, then the pre-run read of the tier.
* Not yet in `automation/`: the Gamry worker's instrument backend is a stub, and the signal routine fits a baseline
  through windows around a peak; the pre-run subtraction of tiers 1 and 2 has to be added (docs/31 F7).

### 2.4 Calibration, blanks and the LOD

A calibration is a set of determinations, each on its own fresh consumables (strip, bed): blanks (assay buffer) and
standards up to 1000 pg/mL. The LOD is the concentration at mean blank + 3 SD of at least ten blanks on ten sets of
consumables, read through the curve (docs/26 §3). The unit-to-unit spread of the blank is part of the LOD; the
model carries it as 10 % (model blank CV) plus 15 % (hand-coated electrodes) or 10 % (hand-packed beds), both
UNVERIFIED (`tier_params.yaml`).

Range. The kit reports two numbers: the upper limit by the model's slope criterion (docs/03) and the concentration
up to which the nominal curve still rises. Tier 1 is linear to 10⁵ pg/mL. Tiers 2 and 3 bend early (32 and
93 pg/mL by the slope criterion, because the released phosphate inhibits the enzyme in the small volume) but rise
up to 10⁵ pg/mL. They meet docs/26 §3 (a monotonic curve over two decades above the LOD) only as a curved
calibration; the slope criterion gives 1.1 and 2.2 decades. A stop of 30 s instead of 7 min has an upper limit of
460 pg/mL at an LOD of 4.7 (a separate determination, not a second read of the same bed).

### 2.5 The product question (review finding C1) — to be settled before anything else

Alkaline phosphatase hydrolyses one phosphate ester per turnover. From hydroquinone diphosphate it releases the
monophosphate, which must bind again, in competition with a thousandfold excess of diphosphate, before
hydroquinone appears. With the enzyme amounts of this document the hydroquinone-to-monophosphate ratio after a
7 min stop in tier 2 is about 10⁻⁴ to 10⁻³, and in tier 1 about 3×10⁻⁶ of the monophosphate is hydrolysed again
before the flow removes it (Derived by the reviewer, `results/tier_round/review_chemistry.md` C1; for equal
Michaelis constants and turnover numbers of the two esters the ratio is half the converted fraction of the
substrate). The model, like docs/01–05, counts one hydroquinone per turnover. The papers the choice rests on
(Wilson2004, Bekhit2021; docs/29 A.1) do not address the intermediate.

| If the test shows | Then |
|---|---|
| the monophosphate is oxidised at or near the hydroquinone potential | nothing changes (one or two electrons per turnover) |
| it is oxidised only at a higher potential | the read potential moves up; on gold in chloride the window ends at +0.6 V (docs/28 §4) |
| it is not oxidised | change the substrate: p-hydroxyphenyl phosphate (the monophosphate itself, DellaCiana1996, docs/01; supplier not found, docs/07 §6) or ascorbic acid 2-phosphate (docs/01 b). The designs stay as they are |

Scenario "only 1 % of the turnovers give an electroactive product": tier 1 890, tier 2 36, tier 3 37 pg/mL nominal.

The test (half a day, no flow system): 1–10 pM conjugate in 1 mM HQDP for 7 min; voltammogram on a printed carbon
strip and on a coated gold strip against a hydroquinone standard; the same solution on the I-Class with UV
detection to separate diphosphate, monophosphate and hydroquinone; repeat in 1 M diethanolamine pH 9.8.

## 3. Tier 1 — consumables only: the electrode is the solid phase

### 3.1 Design

| Element | Choice | Source and confidence |
|---|---|---|
| Cell | MicruX AIO-SPE cell with its flow add-on: wall jet, 0.8 mm inlet bore, 8 mm O-ring | docs/28 §1 [V]; gap not published: 0.2 mm taken (the user's 10 µL), 0.1 and 0.5 mm as cases |
| Electrode | MicruX ED-S1PE-Au10 printed gold strip, 3 mm working electrode (7.1 mm²), printed silver reference; one strip per determination | docs/28 §2.1 [V] |
| Surface | on the working electrode only (a 2–3 µL drop): mixed monolayer of a short-chain biotin-terminated and hydroxy-terminated oligo(ethylene glycol) thiol, then streptavidin, then biotinylated capture F(ab′)₂, then assay buffer | principle: Nishimura2011 [V-abs] (short tri(ethylene glycol) thiols resist protein and pass p-aminophenol); thiol part numbers and the quality of monolayers on printed gold UNVERIFIED |
| Capture | sample through the cell at 3.0 µL/min for 42 min (126 µL; 99 % of the plug leaves the loop) | docs/27 §4 |
| Label | 100 µL of 10 nM conjugate at 50 µL/min, 4 min (two loop volumes) | exposure 20 nM·min |
| Read | flow constant at 150 µL/min: buffer (reference window, 30 s) → substrate (front 1.4 min, read 2 min) → buffer (front 1.4 min, reference window 30 s). Signal = current in the read window minus the mean of the two reference windows, minus the same quantity from the identical sequence run on the fresh strip before the sample | docs/31 N1, N2 |

Why a fast, constant flow. (i) The conjugate on the inlet bore and on the transfer line (36 mm², 1.25×10⁵ enzymes)
makes product that the stream carries over the electrode; at 150 µL/min only 7.4 % of it is collected, against
62 % at 5 µL/min and 99 % at 1 µL/min, while the electrode's own enzyme is collected in full. (ii) The reference windows are at the same
flow, so no pressure or charging transient separates them from the read, and they are 5.4 min apart instead of an
hour. (iii) No zero-flow step and no flow below 3 µL/min is needed. The price is the substrate's free
hydroquinone, which arrives faster: 107 pA at 0.3 mM against a signal of 1.6 pA per pg/mL. It is measured on the
same strip before the sample and subtracted; the model allows 3 % for what that subtraction leaves (UNVERIFIED),
and that term is 61 % of the blank variance.

Why printed gold, and why it is not certain. The model puts gold with an OEG monolayer at 9.4 pg/mL, printed
carbon with adsorbed streptavidin at 17 and the thin-film gold chip in its small cell at 13. The gold figure rests
on two guesses: a surface factor of 3 against 10 for carbon, and hydroquinone being oxidised at full rate through
the monolayer and the protein on it (docs/31 C2). The printed strip is preferred to the thin-film chip because its
silver reference stands apart from the working electrode and is not covered by the thiol, and because its current
is five times larger (docs/31 C3, N7). **Printed carbon (ED-S1PE-C21, printed Ag/AgCl reference, no thiol
chemistry) is the fallback, and the first tier-1 experiment compares the two.**

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

### 3.3 Step table (56.9 min from Inject Start to result)

| Clock (min) | Step | BSM | SM-FL | Gamry |
|---|---|---|---|---|
| before (12 min) | mount strip; flush; cleaning injection; hydroquinone plug as a check of the strip's response; then the read sequence of rows 49.5–56.9 on the fresh strip | A1, B1, 150 µL/min | assay buffer; hydroquinone | on from here to the end |
| 0–1 | sample aspirated and loaded; Inject Start | A1 3.0 µL/min | line 1: sample, full loop | mark |
| 1–43 | sample through the cell | A1 3.0 µL/min | loop in line | — |
| 43–44.5 | wash 1 | A1 50 µL/min | Loop Offline | — |
| 44.5–45.5 | conjugate aspirated and loaded | A1 50 µL/min | line 2: conjugate, full loop | mark |
| 45.5–49.5 | conjugate through the cell, two loop volumes | A1 50 µL/min | loop in line, then Loop Offline | — |
| 49.5–51.5 | wash 2; last 30 s = reference window 1 | A1 150 µL/min | — | window |
| 51.5–52.9 | substrate front (215 µL) | B1 150 µL/min | — | — |
| 52.9–54.9 | **read** | B1 150 µL/min | — | window |
| 54.9–56.4 | buffer front | A1 150 µL/min | — | — |
| 56.4–56.9 | reference window 2 | A1 150 µL/min | — | window |

### 3.4 Where the number comes from (nominal; `tiers.json`)

| Quantity | Value |
|---|---|
| Sample molecules at 1 pg/mL | 4.0×10⁵ |
| Captured on the electrode | 3.2×10⁴ (7.9 % of the vial) |
| Labelled (36 %), label still bound at the read (72 %), analyte still bound (83 %) | 6.7×10³ enzymes |
| Signal | 1.6 pA per pg/mL (750 turnovers per second at 0.3 mM, 2 electrons); 0.19 nC in the 2 min window |
| Conjugate on the electrode (surface factor 3) | 2.5×10⁴ enzymes, collected in full: 3.6 pg/mL equivalent |
| Conjugate on bore and transfer line | 1.25×10⁵ enzymes, 7.4 % collected: 1.4 pg/mL equivalent |
| Free hydroquinone of the substrate (10⁻⁵) | 107 pA; hydrolysis in the bottle 15 pA |
| Blank equivalent (non-specific label and hydrolysis) | 14.6 pg/mL |
| Noise, drift | 3 pA rms; 5 pA/min, of which 20 % is taken as not removed over the 5.4 min between windows |
| Variance at the blank | substrate background 61 %, drift 28 %, non-specific label 9 % |
| LOD | 9.4 pg/mL: 15 pA to be told from a 130 pA background |

### 3.5 Scenarios and alternatives (`tiers.md` §2, §3)

| Case | Nominal | Median [5–95 %] |
|---|---|---|
| as specified | 9.4 | 35 [4.4–560] |
| detection reagent and substrate lot screened (L6 + L7) | 4.5 | 16 [2.6–130] |
| the same with the credit for the F(ab′)₂ conjugate (L3) | 4.1 | 11 [2.0–100] |
| conjugate binds non-specifically 25× more (S1) | 71 | 280 [38–2400] |
| free hydroquinone 10⁻³ in the substrate (S4a) | 630 | 920 [140–6500] |
| **printed carbon ED-S1PE-C21, adsorbed streptavidin** | 17 | 78 [8.8–1100] |
| thin-film gold chip SE1 in the thin-film cell | 13 | 48 [5.5–890] |
| strip-cell gap 0.10 mm / 0.50 mm | 9.1 / 12 | 36 / 39 |
| read at 80 µL/min / 40 µL/min | 11 / 20 | 39 / 56 |
| substrate 0.1 mM / 1 mM | 8.8 / 21 | 30 / 61 |
| read in the stopped cell (needs a zero-flow row) | 15 | 39 [5.7–350] |
| transfer line 0.127 mm × 20 cm | 9.8 | 40 [5.3–570] |
| no pre-run read on the strip | 27 | 75 [7.9–1700] |

Substrate at 0.1 mM (the Michaelis constant) is marginally better than 0.3 mM and more exposed to the uncertainty
of that constant; 0.3 mM is kept. The cell's unknown gap changes little.

### 3.6 What could make it fail, and the experiments that decide (in order)

| # | Experiment | Decides | Pass |
|---|---|---|---|
| T1-1 | Coated gold strip and bare carbon strip in the cell at 150 µL/min, no protein: hydroquinone wave and plateau; noise and drift; the A–B–A sequence five times over 70 min, with a conjugate-free protein exposure in between | whether hydroquinone is oxidised through the monolayer; whether the substrate background repeats to 3 % | half-wave ≤ +0.25 V and plateau ≥ 70 % of bare gold at 1 µM hydroquinone; background repeat ≤ 3 %; drift ≤ 5 pA/min |
| T1-2 | Non-specific binding: non-immune strips, the conjugate step, the read; 10 strips each of gold/OEG and carbon | surface factors and unit-to-unit CV | gold: ≤ 2.5×10⁴ enzymes on the electrode (about 6 pA), CV ≤ 20 % |
| T1-3 | Capture: 1 ng/mL IgG through the full protocol, 5 strips | captured fraction and labelling | ≥ 1 pA per pg/mL |
| T1-4 | Blanks on 10 strips, then 10, 30, 100, 1000 pg/mL | the LOD | — |

Risks the model does not carry: the monolayer slows hydroquinone oxidation (T1-1); a printed silver reference in
chloride needs conditioning and may drift (docs/27 §9 item 8); protein adsorbed during the sample step changes the
electrode's collection of the substrate's hydroquinone between pre-run and read; the conjugate on the transfer line
builds up from run to run unless the line is flushed or replaced.

## 4. Tier 2 — plus passive in-line parts: a hand-packed micro-bed in the inlet bore

### 4.1 Design

| Element | Choice | Source and confidence |
|---|---|---|
| Capture bed | 1×10⁶ Dynabeads M-280 Streptavidin carrying the biotinylated capture F(ab′)₂, packed against a frit in a fused-silica capillary of 0.20 mm bore and 0.36 mm outside diameter: bed 19 nL, 0.6 mm long (about 215 bead diameters), 24 mm² of bead surface | beads [V]; fritted capillaries are standard in capillary LC, part numbers and frit pore size UNVERIFIED |
| Position | the capillary passes through the inlet port, sleeved to fill the 0.8 mm bore (sleeves of 1/32″ outside diameter for 0.36 mm capillaries exist as a class: IDEX F-385 [S], `review_chemistry.md` C10), and ends 1 mm above the working electrode (0.5 µL of bore between tip and electrode); 20 mm of capillary above the bed | bore 0.8 mm [V docs/28]; fit of the sleeve in the port UNVERIFIED |
| Cell and electrode | MicruX AIO-SPE cell with its flow add-on; printed carbon strip ED-S1PE-C21 (3 mm, printed Ag/AgCl reference), blocked with assay buffer; **a fresh strip with every bed** | docs/28 §1, §2.1 [V]; docs/31 C7 |
| Capture | sample through the bed at 3.4 µL/min for 37 min; 66 % captured; pressure drop 1.0 bar | kit, bed correlation of the model |
| Label | 100 µL of 10 nM conjugate through the bed at 50 µL/min, 4 min (15 bar across the bed) | exposure 20 nM·min |
| Read | substrate in (215 µL at 80 µL/min, 25 bar across the bed), 1 min at 5 µL/min, flow stopped 7 min, then 5 µL/min for 90 s: the plug crosses the electrode, which converts 62 % of it. The same step, stop and sweep on the fresh bed and strip before the sample gives the trace that is subtracted | kit; docs/27 §2 for the stop; docs/31 N4 |

Why beads of 2.8 µm. They are the surface on which the project's non-specific-binding rate is defined, they are in
the bill of materials, and a million of them is the smallest bed that still takes two thirds of the sample. Packed
in a column and washed in flow they are given the model's packed-bed factor of 3 (1–30), not the factor of 1 they
have when washed in tubes (docs/31 N5); with 1 the LOD is 2.0.

Why at the tip, and what still lies in the read path. Every conjugate-coated wall that stands in substrate during
the stop makes product, and the sweep carries all of it over the electrode. Below the bed: the frit (5 mm² taken)
and 1 mm of bore (2.5 mm²). Above the bed: the capillary (13 mm²) and the transfer line (24 mm²); their product
arrives right behind the plug, inside the read window. Of the blank's 2.8×10⁵ enzymes, 45 % sit on the walls above
the bed, 31 % on the beads, 21 % on the frit, 3 % on the bore. A valve would remove the first group (tier 3).

Why the stop needs an identical pre-run. During the stop the electrode is on and empties the layer above it of the
substrate's free hydroquinone. When the sweep starts, fresh substrate arrives and the background steps from about
zero to 100 pA while the peak passes (the mean blank peak is about 170 pA). The trace of the same stop and sweep on
the fresh bed and strip, before the sample, carries the same step and is subtracted; 4 % of the step is taken as
left (UNVERIFIED).

The frit is the other open point: a 0.5 mm silicate frit may have 20 mm² of inner surface (Derived: 4ε/d for
1.5 µm pores, UNVERIFIED). Model LOD for 1, 5 and 20 mm²: 2.1, 2.6 and 4.3 pg/mL.

### 4.2 Bench preparation

1. Coat beads in a tube: wash the stock three times in wash buffer, re-block in assay buffer; 10 µg biotinylated
   capture F(ab′)₂ per mg, 30 min; wash; assay buffer 30 min (docs/06 §4.0). Non-immune beads likewise.
2. Pack: draw 1.5 µL of coated beads (10 mg/mL), diluted in 20 µL assay buffer, into the capillary against the
   frit; follow with assay buffer. Compact the bed at 80 µL/min for 1 min on the bench and check its length (0.6 mm).
3. Sleeve the capillary, seat it in the inlet port against a mechanical stop so that the tip is 1 mm above the
   strip, mount a fresh strip.
4. The add-on is held by magnets (docs/28 §1 [V]) and the beads are magnetic: check under a lens that the bed stays
   packed with the add-on in place. If it does not, use non-magnetic streptavidin particles of 3–10 µm (docs/31 C6).

### 4.3 Step table (58.7 min)

| Clock (min) | Step | BSM | SM-FL | Gamry |
|---|---|---|---|---|
| before (14 min) | mount bed and strip; flush; cleaning injection; the substrate step, stop and sweep of rows 46.5–58.7 on the fresh bed and strip | A1, B1 | assay buffer | on (+0.30 V vs the printed Ag/AgCl, set once per strip lot) |
| 0–1 | sample loaded; Inject Start | A1 3.4 µL/min | line 1: sample, full loop | mark |
| 1–38 | sample through the bed | A1 3.4 µL/min | loop in line | — |
| 38–39.5 | wash 1 | A1 50 µL/min | Loop Offline | — |
| 39.5–40.5 | conjugate loaded | A1 50 µL/min | line 2: conjugate, full loop | mark |
| 40.5–44.5 | conjugate through the bed, two loop volumes | A1 50 µL/min | loop in line, then Loop Offline | — |
| 44.5–46.5 | wash 2 | A1 50 µL/min | — | — |
| 46.5–49.2 | step to substrate, 215 µL | B1 80 µL/min | — | — |
| 49.2–50.2 | step down | B1 5 µL/min | — | — |
| 50.2–57.2 | **stop**: product collects in the bed | 0 µL/min | — | baseline |
| 57.2–58.7 | **sweep and read** | B1 5 µL/min | — | trace minus pre-run trace |

### 4.4 Where the number comes from (nominal)

| Quantity | Value |
|---|---|
| Captured at 1 pg/mL | 2.6×10⁵ (66 % of the vial) |
| Enzymes at the read | 5.3×10⁴ (labelled 36 %, label still bound 67 %, analyte still bound 83 %) |
| Signal | 2.7 nC per pg/mL, about 30 pA over 90 s |
| Blank enzymes: beads / frit / bore below the tip / capillary and line above the bed | 8.5×10⁴ / 5.8×10⁴ / 0.9×10⁴ / 12.5×10⁴ |
| Blank equivalent | 6.0 pg/mL |
| Variance at the blank | non-specific label 93 %, electrode response 4 %, substrate background 3 % |
| LOD | 2.6 pg/mL |
| Upper limit by the slope criterion / curve rises up to | 32 pg/mL / 10⁵ pg/mL |

### 4.5 Scenarios and alternatives (`tiers.md` §2, §4)

| Case | Nominal | Median [5–95 %] | P(≤ 1) / P(≤ 10) |
|---|---|---|---|
| as specified | 2.6 | 13 [1.4–170] | 0.02 / 0.43 |
| screened detection reagent and substrate lot (L6 + L7) | 1.7 | 7.4 [1.0–78] | 0.05 / 0.58 |
| the same with the credit for the F(ab′)₂ conjugate (L3) | 0.81 | 3.6 [0.64–36] | 0.13 / 0.78 |
| conjugate binds 25× more (S1) | 100 | 390 [33–6200] | 0.00 / 0.00 |
| free hydroquinone 10⁻³ (S4a) | 60 | 100 [13–1200] | 0.00 / 0.03 |
| no conjugate-coated wall above the bed (bound: what a valve would give) | 1.4 | 6.9 [0.96–92] | 0.06 / 0.59 |
| transfer line 0.127 mm × 20 cm | 4.5 | 22 [2.1–300] | 0.01 / 0.30 |
| bed in a fitting on the port (whole bore between bed and electrode) | 2.9 | 15 [1.6–190] | 0.02 / 0.39 |
| frit 1 mm² / 20 mm² | 2.1 / 4.3 | 11 / 19 | 0.03 / 0.01 |
| beads behave as when washed in tubes (factor 1) | 2.0 | 9.9 [1.1–120] | 0.04 / 0.50 |
| half / twice the beads | 3.0 / 2.9 | 18 / 12 | 0.01 / 0.02 |
| stop 3 min instead of 7 | 2.5 | 13 [1.5–170] | 0.02 / 0.42 |
| parked read | 3.3 | 14 [1.6–200] | 0.02 / 0.41 |
| **pump cannot stop: continuous read at 1 µL/min** | 3.0 | 12 [1.6–120] | 0.01 / 0.44 |
| pump cannot stop and cannot go below 10 µL/min | 4.2 | 20 [2.8–230] | 0.00 / 0.29 |
| strip-cell gap 0.10 / 0.50 mm | 2.6 / 2.6 | 13 / 13 | — |

The continuous read counts the same walls and loses little in the blank, but its reference is the pre-run an hour
earlier; the drift over that time is not in the kit (docs/31 N1), so its figure is optimistic. The length of the
stop hardly matters, because blank and signal grow together; 3 min would free 4 min for the load.

### 4.6 What could make it fail, and the experiments that decide

| # | Experiment | Decides | Pass |
|---|---|---|---|
| T2-1 | Blank path: (a) an empty fritted capillary, (b) one with non-immune beads, each through conjugate, wash, substrate, 7 min stop and sweep on the full path; 5 each; with beads as supplied and re-blocked in IgG-free BSA | conjugate on walls and frit against conjugate on the beads; the bovine-IgG route | walls and frit ≤ 2 × beads; blank peak CV ≤ 15 % |
| T2-2 | The stop: zero-flow row (docs/27 §9), creep after the step-down, shape of the baseline step with and without the pre-run subtraction; 50 nM hydroquinone held 0, 3, 7, 12 min | whether the stop exists; the step; hydroquinone loss | residual step ≤ 4 % of the step; ≥ 60 % of hydroquinone left after 7 min |
| T2-3 | Breakthrough: 1 ng/mL IgG at 2, 3.4, 7 µL/min; bed viewed with the add-on's magnets in place | captured fraction; channelling | ≥ 50 % at 3.4 µL/min |
| T2-4 | Bed-to-bed: 10 beds, 100 pg/mL | packing reproducibility | signal CV ≤ 10 % |
| T2-5 | Blanks on 10 beds; 1–1000 pg/mL | the LOD | — |

## 5. Tier 3 — anything: the bed in the loop of a valve, then an immune-complex transfer to a clean second bed

### 5.1 Design

| Element | Choice | Source and confidence |
|---|---|---|
| Valves | two 2-position 6-port PEEK valves (IDEX MXP9900-000), each with a bed in its loop, in series between the SM-FL and the cell; Python-driven as in docs/05 §4.1. The first step needs only one of them | docs/07 §2 [V] |
| Capture bed (bed 1) | 1×10⁶ streptavidin beads holding the capture F(ab′)₂ through a biotin on a **cleavable link** | link chemistry UNVERIFIED (see below) |
| Read bed (bed 2) | 1×10⁶ beads carrying an antibody against a **hapten tag** on the capture F(ab′)₂. It has to hold all the released capture antibody, not only the complexes (see below) | UNVERIFIED; replaces the "phase-2 antibody not yet identified" of docs/06 §4.12 |
| Transfer | eluent held on bed 1 for 5 min (bed 1 closed by its valve), then pushed through bed 2 at 2 µL/min (re-capture 95 % by the bed equation); wash | release in 5 min: 0.7 (0.2–0.95) taken, **no rate known**; non-specific label that comes along ×0.1 (0.01–0.5), `ma.design_levers` |
| Cell and electrode | as tier 2 (strip cell, printed carbon ED-S1PE-C21, fresh with every pair of beds); the cell is always in the flow, downstream of both valves | |
| Read | substrate into bed 2; bed 2 closed by its valve for 7 min while substrate flows on through the bypass and the cell at 5 µL/min; then the valve opens and the plug is swept over the electrode | steady baseline before and after the peak |

```
SM-FL -> V1 -> V2 -> cell -> waste          each valve: port 1 in, port 6 out, bed between ports 2 and 5,
                                            ports 3 and 4 plugged
IN  (1-2, 5-6): the stream passes through the bed        OUT (1-6): bed bypassed and closed at both ends
sample, wash, conjugate, wash : V1 IN,  V2 OUT    conjugate never reaches bed 2
eluent                        : V1 IN until bed 1 is filled; V1 OUT for the hold; V1 IN + V2 IN for the push
wash of bed 2, substrate      : V1 OUT, V2 IN
accumulation                  : V2 OUT, pump at 5 uL/min through the bypasses and the cell
read                          : V2 IN
```

What one valve changes, before any transfer (the capture bed sits in the loop of that valve and is the bed that
is read; load 36 min at 3.5 µL/min, 56.7 min to result):
* The walls upstream of the bed never stand still in substrate: their product is a steady current, not a plug.
  The same holds for the conjugate on the electrode and in the cell, which every tier-3 variant still sees.
* The electrode stays in flowing substrate during the accumulation, so the peak sits on a flat baseline and no
  pre-run trace is subtracted. The steady background of the substrate in the same record (100 pA at 5 µL/min)
  serves as the check of each strip's response; the model allows 3 % for that normalisation.
* The pump never stops and never runs below 2 µL/min. The pressure that relaxes after a flow step passes through the
  bypass, not through the closed bed.
* Only the bed, its frit and the loop of the valve (rotor passages and tubing, 10 mm² taken) hold conjugate that
  counts in the read.

Model: **1.5 nominal, median 6.9 [0.87–85]**, against 2.6 and 13 for tier 2.

The transfer adds the second valve and bed. Two conditions go with it that the model does not carry:
* **Capacity.** Bed 2 binds the tag on the capture antibody, so it takes every released capture F(ab′)₂, with or
  without analyte: about 2×10¹¹ molecules at the model's site density, up to 8×10¹¹ at the vendor's bead capacity,
  against 10⁴–10⁵ complexes. The model takes the re-capture as first order (95 % at 2 µL/min), which holds only
  while bed 2 is far from full. If it fills, the recovery is the ratio of capacity to eluate (0.12–0.95, Derived by
  the reviewer, docs/31 C8). Either bed 2 is given several times the capacity of bed 1 (more beads; or the order of
  the tags is reversed so that the read bed is the streptavidin bed, 6–8×10¹² biotin sites per 10⁶ beads, Derived
  from docs/28 R32), or bed 1 is loaded below its capacity, which costs capture (site density at its low bound:
  4.1 pg/mL).
* **The eluent crosses the electrode.** A reductant may be oxidised at the read potential; the strip has 15 min of
  buffer and substrate flow to recover before the read (experiment T3-2).

The transfer chemistry is not settled. Three routes, none with a verified rate at 5 min:

| Route | How | What is known |
|---|---|---|
| Cleavable link + hapten (taken as primary) | capture F(ab′)₂ carries a biotin on a disulfide spacer and a hapten (dinitrophenyl or fluorescein); a reductant in the eluent cuts the spacer; bed 2 holds anti-hapten antibody. A photocleavable biotin with a 365 nm lamp on the loop of V1 is the variant without reductant | UNVERIFIED throughout (reagent part numbers not checked). The reductant also meets the hinge disulfides of both F(ab′)₂ and of the analyte, and the enzyme; alkaline phosphatase has been run with TCEP in the substrate solution (Akanda2011a [V-abs], docs/29 A.2) |
| Desthiobiotin displaced by biotin (docs/06 §4.12) | as planned for Stage 1C, with a hapten tag for bed 2 | too slow: 0.3–26 % released in 5 min (Derived by the reviewer from K_d ≈ 10⁻¹¹ M, UNVERIFIED); Hirsch2002 [V-abs] gives no rate; "the rate of elution of desthiobiotinylated materials is too slow" (Ying, Branchaud and Corry 2011 [V full text, reviewer; `review_chemistry.md` C8]). Model: 4.3 nominal, worse than no transfer |
| Dinitrophenyl first, streptavidin second (Ishikawa1990, Hashida1997) | the original immune-complex transfer | developed with elutions of hours (recalled, UNVERIFIED) |

### 5.2 Step table (58.2 min)

| Clock (min) | Step | Valves | BSM | SM-FL |
|---|---|---|---|---|
| before (14 min) | mount both beds and the strip; flush; cleaning injection; substrate over the strip with both beds bypassed (response check), back to buffer | both OUT | A1, B1 | assay buffer |
| 0–1 | sample loaded | V1 IN, V2 OUT | A1 5.0 µL/min | line 1 |
| 1–26 | sample through bed 1 (55 % captured) | V1 IN, V2 OUT | A1 5.0 µL/min | loop in line |
| 26–27.5 | wash 1 | V1 IN, V2 OUT | A1 50 µL/min | Loop Offline |
| 27.5–32.5 | conjugate loaded and passed | V1 IN, V2 OUT | A1 50 µL/min | line 2; Loop Offline at the end |
| 32.5–34.5 | wash 2 | V1 IN, V2 OUT | A1 50 µL/min | — |
| 34.5–36 | eluent loaded and brought to bed 1 | V1 IN, V2 OUT | A1 50 µL/min | line 3 |
| 36–41 | hold | V1 OUT, V2 OUT | A1 50 µL/min (flushes the path) | Loop Offline |
| 41–45 | push, 8 µL | V1 IN, V2 IN | A1 2 µL/min | — |
| 45–47 | wash of bed 2 | V1 OUT, V2 IN | A1 50 µL/min | — |
| 47–49.7 | substrate to bed 2, 215 µL | V1 OUT, V2 IN | B1 80 µL/min | — |
| 49.7–56.7 | accumulation | V1 OUT, V2 OUT | B1 5 µL/min | — |
| 56.7–58.2 | sweep and read | V1 OUT, V2 IN | B1 5 µL/min | — |

The label waits 19 min between the conjugate and the accumulation; with the unscreened detection reagent 63 % of
it is gone. Screening the reagent is worth more in tier 3 than anywhere else (0.62 → 0.22 with the substrate lot).
The three SM-FL lines are counted at 1 min each (docs/02 §2.2, UNVERIFIED: 0.25–2 min); at 2 min each the margin
of 1.8 min is used up and the load has to be shortened.

One valve, no transfer: rows 34.5–47 fall away and the load is 36 min at 3.5 µL/min; the bed is in the loop of
the one valve, IN for every step except the accumulation. 56.7 min.

### 5.3 Numbers (`tiers.md` §2, §5)

| Case | Nominal | Median [5–95 %] | P(≤ 1) / P(≤ 10) |
|---|---|---|---|
| as specified (release 0.7, re-capture 0.95, non-specific ×0.1) | 0.62 | 4.8 [0.54–260] | 0.15 / 0.64 |
| screened detection reagent and substrate lot (L6 + L7) | 0.22 | 1.5 [0.32–23] | 0.34 / 0.88 |
| the same with the credit for the F(ab′)₂ conjugate (L3) | 0.14 | 1.1 [0.25–12] | 0.45 / 0.94 |
| with a reference channel as well (L5) | 0.56 | 4.4 [0.53–250] | 0.17 / 0.65 |
| **one valve only: the capture bed is read (no transfer)** | 1.5 | 6.9 [0.87–85] | 0.06 / 0.61 |
| one valve only, screened reagents (L6 + L7) | 1.1 | 4.3 [0.72–46] | 0.10 / 0.72 |
| transfer at its optimistic bounds (release 0.95, ×0.01) | 0.27 | 1.2 [0.23–76] | 0.43 / 0.84 |
| transfer at its pessimistic bounds (release 0.2, ×0.5) | 9.0 | 48 [3.6–2200] | 0.00 / 0.18 |
| transfer by desthiobiotin and biotin, 5 min | 4.3 | 56 [2.5–4000] | 0.01 / 0.19 |
| accumulation 12 min instead of 7 | 0.63 | 5.0 [0.53–280] | 0.15 / 0.63 |
| blanks contaminated up to 1 pg/mL (C1 of docs/08) | 0.62 | 5.0 [0.77–260] | 0.08 / 0.64 |
| conjugate binds 25× more (S1) | 14 | 70 [3.7–4200] | 0.01 / 0.16 |
| free hydroquinone 10⁻³ (S4a) | 33 | 91 [5.9–3900] | 0.00 / 0.09 |

Nominal chain: 2.2×10⁵ captured, 1.6×10⁴ enzymes at the read per pg/mL (transfer 67 %, label still bound 37 %),
0.93 nC per pg/mL, blank equivalent 1.1 pg/mL; variance: non-specific label 61 %, substrate background 22 %, drift
12 %. A transfer that performs at its pessimistic bounds is six times worse than one valve alone: **the transfer
is added only after its test (T3-1)**. Not in the design, as runners-up: a second potentiostat channel with a
reference bed (0.62 → 0.56); a pre-electrolysis electrode in the substrate line, which removes free hydroquinone
before the bed (at 10⁻⁷ free hydroquinone: 0.55; the project's bench test E1.2b decides whether it works); redox
cycling on an interdigitated array (it amplifies the substrate background with the signal).

### 5.4 What could make it fail

| # | Experiment | Decides | Pass |
|---|---|---|---|
| T3-1 | Transfer at the time scale of the design, first in tubes, then in two beds: release in 5 min for each route, re-capture at 2 µL/min with the full load of capture antibody (capacity of bed 2), conjugate that comes along; leak of capture antibody from bed 1 over 40 min | whether a transfer exists | blank reduced ≥ 5× with ≥ 50 % recovery (docs/05 §5 U8) |
| T3-2 | Effect of the eluent on the enzyme label and on the complex; the strip's background and response before and after the eluent has crossed it | the cleavable route | ≥ 80 % of the enzyme activity after 5 min; background back within 3 % in 10 min |
| T3-3 | Tier-2 experiments T2-1 and T2-3 to T2-5 on the one-valve set-up, without transfer; time between sample-set lines | the base | as tier 2 |
| T3-4 | Blank handling: blanks prepared in a hood with dedicated consumables against open-bench blanks | the contamination floor | ≤ 0.1 pg/mL equivalent (docs/05 §5 U9) |

### 5.5 Relation to the earlier design

The dosing-pump, stirred-chamber and magnetic-trap design of docs/05 §4.1 is the other "anything" design. Its model
numbers (docs/08 §10.1): nominal 0.60, median 3.5 [0.51–158], P(success) 0.16 as specified; with the transfer lever
nominal 0.29, median 1.5, P 0.33. Re-run here with the 10 min half-life of hydroquinone they are unchanged
(median 3.46). They cannot be set against the tier figures: the kit adds the unit-to-unit spread of hand-made
consumables, the frit, the loop walls and the tighter transfer, and the earlier model adds a reuse term and uses a
success criterion that includes the range. What can be said: both rest on the same two measurements, both need the
same transfer to go below 1 pg/mL, and the two-bed arrangement needs two valves where the earlier design needs
several valves, a syringe pump with a selection valve, an incubation cup and a magnetic trap. The earlier design keeps the simultaneous incubation and the
unattended queue, which this round does not ask for.

## 6. Comparison

### 6.1 The same quantities side by side (nominal)

| | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Captured fraction of the sample | 7.9 % | 66 % | 55 %, of which 67 % is transferred |
| Enzymes at the read per pg/mL | 6.7×10³ | 5.3×10⁴ | 1.6×10⁴ |
| Signal per pg/mL | 1.6 pA for 120 s (0.19 nC) | 2.7 nC | 0.93 nC |
| Blank equivalent (pg/mL) | 14.6 | 6.0 | 1.1 |
| Largest variance term | substrate background | non-specific label | non-specific label |
| Needs the pump to stop | no | yes | no |
| Lowest flow | 3.0 µL/min | 3.4 µL/min | 2 µL/min |
| New consumables per determination | strip | capillary bed, strip | two beds, strip |

### 6.2 Largest sensitivities (one parameter at its bounds; `tiers.md` §6)

| Parameter [low–high] | Tier 1: LOD at low / high | Tier 2 | Tier 3 |
|---|---|---|---|
| detection off-rate 8.6×10⁻⁴ s⁻¹ [3×10⁻⁶–8.3×10⁻³] | 6.4 / 240 | 1.6 / 110 | 0.22 / 4700 |
| free hydroquinone 10⁻⁵ [10⁻⁷–10⁻³] | 6.1 / 630 | 2.5 / 60 | 0.55 / 33 |
| non-specific rate 4×10⁻¹¹ m/s [0.8–40×10⁻¹¹] | 8.9 / 30 | 0.60 / 35 | 0.38 / 5.3 |
| detection on-rate 3.9×10⁵ M⁻¹s⁻¹ [0.9–12×10⁵] | 34 / 4.5 | 9.3 / 1.2 | 2.3 / 0.30 |
| enzyme turnover 1000 s⁻¹ [100–6000] | 89 / 3.2 | (small) | 3.7 / 0.52 |
| hydrolysis of the substrate 10⁻¹⁰ s⁻¹ [10⁻¹²–10⁻⁸] | 8.5 / 190 | (small) | (small) |
| label factor of the conjugate 0.04 [0.01–0.15] | (small) | 0.70 / 11 | (small) |
| surface factor of tubing 3 [1–30] | (small) | 1.8 / 16 | (small) |
| surface factor of the bed 3 [1–30] | — | 2.0 / 11 | 0.50 / 2.7 |
| surface factor of the frit 10 [1–100] | — | 2.1 / 8.2 | (small) |
| surface factor of the coated gold 3 [1–30] | 9.0 / 23 | — | — |
| non-specific label that comes along in the transfer 0.1 [0.01–0.5] | — | — | 0.37 / 2.6 |

### 6.3 What holds in every case run

* Tier 3 < tier 2 < tier 1 in nominal and median LOD as specified and in the screening scenarios, and tier 3
  without transfer is still below tier 2. Exceptions: with a conjugate that binds 25× more, tier 2 (100) is above
  tier 1 (71), because the walls and the frit then dominate; if only 1 % of the turnovers give an electroactive
  product, tiers 2 and 3 are equal (36, 37); and the transfer at its pessimistic bounds or by the desthiobiotin
  route is worse than tier 2.
* A substrate lot with 10⁻³ free hydroquinone puts every tier above 30 pg/mL (630, 60, 33). A conjugate that binds
  25× more than the plate anchor puts them at 71, 100 and 14. These are the two kill conditions of docs/05 §5.
* Screening the detection reagent and the substrate lot is worth a factor of 2.1 in tier 1, 1.5 in tier 2 and 2.8
  in tier 3.

### 6.4 Why the judgement is above the model

Not in the model: channelling in a hand-packed bed; the monolayer's effect on the hydroquinone current; drift of a
printed reference; the pump at 2–5 µL/min and 200–500 psi; protein on an electrode that every sample and conjugate
now passes; conjugate that builds up on the transfer line from run to run; bovine IgG in blockers; temperature;
the true unit-to-unit spread of hand-made consumables. Human IgG from the laboratory is nominally zero and sampled
up to 0.45 pg/mL. Each is more likely to hurt than to help.

## 7. Bench order

1. **The product test of section 2.5** (half a day). It decides the substrate for these designs and for the
   earlier ones.
2. **Instrument facts** (docs/27 §9, two days): low flow, zero-flow row, Loop Offline and the substrate front (dye),
   pressure relaxation, cell gap, cell pressure, loop draw, reference stability.
3. **The shared Stage 1A experiments of docs/06** (E1.1 readout, E1.2 free hydroquinone, E1.3 conjugate
   non-specific binding on beads), with the MicruX strip in its cell as the electrode, plus two arms from the
   review: hydroquinone loss at pH 9.5 over 0–12 min, and beads as supplied against beads re-blocked in IgG-free
   BSA. Gate G1a is unchanged.
4. **Tier 2**: T2-1 (walls and frit), T2-2 (the stop), T2-3 (breakthrough), T2-4, T2-5.
5. **Tier 1 beside it** if wanted: T1-1 and T1-2 need only strips, thiols, streptavidin and conjugate.
6. **Tier 3**: one valve with the bed in its loop as soon as it can be had (T3-3); the second valve, the second
   bed and the transfer after T3-1.

This round changes no gate, no kill criterion and no order in docs/06. Whether its experiments are added to that
plan is the user's decision (section 8).

## 8. Choices the user may overrule, and open questions

Choices made here:
1. Tier 1 on a printed gold strip with a thiol monolayer (model 9.4) rather than on printed carbon (17).
2. Tier 1 reads at 150 µL/min between buffer windows; it uses about 1 mL of substrate solution per determination
   (pre-run and read).
3. Tier 2 uses the project's 2.8 µm beads in a fritted capillary, a fresh strip with every bed, and one stop.
4. Tier 3 is two beds on two valves with a transfer whose chemistry is still to be chosen; the one-valve arrangement
   without transfer is given as its robust core.
5. The range is reported, not enforced (docs/26 §3).
6. The gap of the strip cell is taken as 0.2 mm (the user's 10 µL); MicruX states < 5 µL, which would be ≤ 0.1 mm.
7. The half-life of hydroquinone at pH 9.5 is taken as 10 min (2 min to 2 h) in this round instead of the model's
   2 h (docs/31 C5); `params/` is not edited.

Questions only the user can answer (docs/27 §9, docs/28 §8):
1. Which flow add-on and which electrodes are in hand (part numbers on the packs)?
2. Where does "10 µL" come from?
3. Does a BSM method accept a 0.000 mL/min row? Is a restrictor installed, and which?
4. Is the full-loop overfill set to 2× on this sampler (the Waters default draws five loop volumes)?
5. Should the experiments of section 7, above all the product test, enter the bench plan (docs/06), and before or
   after gate G1a?
6. Does a fritted capillary count as a fitting (an in-line filter is one)? If it does, the tier-2 design is also the
   best tier-1 design, and the electrode-capture design becomes its runner-up.

## 9. Reproduction and references

```bash
pip install -e .
python scripts/tier_round/check_tierkit.py     # 36 checks
python scripts/tier_round/run_tiers.py         # results/tier_round/tiers.md, tiers.json (about 1 min)
```

Designs: `scripts/tier_round/designs.py` (`tier1`, `tier2`, `tier3`) and `run_tiers.py`. Parameters added by this
round: `scripts/tier_round/tier_params.yaml` (UNVERIFIED engineering estimates unless a source is named). Reviewer
reports and their scripts: `results/tier_round/review_*.md`, `scripts/tier_round/review_*.py`.

References are held where they were checked: MicruX and parts in docs/28 §9; Waters in docs/27 Appendix A;
literature keys (Nishimura2011, Bekhit2021, Buckey2022, Das2007, Kwon2008, Akanda2011a, Akanda2013, DiazGonzalez2005,
Squires2008 and others) in docs/29 A.R and B.R and in docs/01; Ishikawa1990, Hashida1997 and Hirsch2002 in docs/05;
reagents in docs/07 §7; Ying, Branchaud and Corry 2011 and the vendor pages re-opened by the reviewers in
`results/tier_round/review_chemistry.md`.
