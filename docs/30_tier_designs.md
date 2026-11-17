# 30 — Three implementations for the lowest LOD on the equipment in hand

Status: 2026-11-17, written by the orchestrator. Inputs: docs/26 (brief and interview), docs/27 (capability map),
docs/28 (MicruX hardware), docs/29 (literature), the model (`src/elisa_sim`) and the calculation kit of this round
(`scripts/tier_round/`, 36 checks pass). Every LOD below is a model prediction, not a measurement.
"Nominal" = all parameters at their best estimate. "Median [5–95 %]" = Monte Carlo over the parameter bounds
(n = 2000, seed 20261111); the interval is a scenario range, not a confidence interval (docs/03 §7). P = fraction of
draws. Numbers come from `results/tier_round/tiers.md`; the review of this document is docs/31.

## 0. Summary

One assay, built three ways. All three are sequential sandwich assays for human IgG with an alkaline-phosphatase
label and hydroquinone diphosphate (HQDP) as substrate, read by holding one electrode at the hydroquinone
oxidation plateau and integrating the current. They differ in where the IgG is captured.

| | **Tier 1 — consumables only** | **Tier 2 — plus passive parts** | **Tier 3 — anything** |
|---|---|---|---|
| Capture | on the working electrode itself: thin-film gold chip (1 mm), biotin-OEG monolayer, streptavidin, biotinylated anti-Fc F(ab′)₂ | on 1×10⁶ streptavidin beads (2.8 µm) packed by hand in a fritted capillary whose tip sits in the cell's inlet bore, 1 mm above a printed carbon electrode | the tier-2 bed, behind two valves, followed by an immune-complex transfer to a second, clean bed that is the one read |
| Added to the equipment in hand | electrode chips, thiols, reagents, restrictor, tubing | the same reagents on beads; capillary with frit, sleeve and fitting | two 6-port valves, a second bed, elution reagent, Python valve control |
| Read | substrate flows at 1 µL/min; steady current of the enzyme on the electrode, 4 min | flow stopped 7 min (product collects in the bed), then swept over the electrode in 90 s | as tier 2; the valve isolates the bed, the pump never stops |
| Injection to result | 53 min | 58 min | 58 min |
| LOD nominal (pg/mL) | **3.1** | **0.75** | **0.33** |
| LOD median [5–95 %] | 16 [2.1–160] | 3.0 [0.51–45] | 1.4 [0.28–43] |
| P(LOD ≤ 1 pg/mL) / P(≤ 10) | 0.01 / 0.37 | 0.18 / 0.78 | 0.38 / 0.84 |
| With the detection reagent and substrate lot screened (L6 + L7) | 2.1; 10 [1.6–74] | 0.48; 1.7 [0.40–16]; P 0.31 | 0.11; 0.74 [0.18–3.0]; P 0.67 |
| What limits it | drift of a sub-pA current; then non-specific conjugate on the electrode | non-specific conjugate on the bed's retainer and on the beads | at this level the substrate background, drift and human-IgG contamination of blanks |
| Depends on, unproven | conjugate adsorption on the coated gold; a steady 1 µL/min from the pump | a low-area bead retainer; a zero-flow step in the pump method (fallback 1.6 nominal) | the transfer itself (magnitude UNVERIFIED; without it 1.2 nominal; a phase-2 antibody still to be found) |

Reading of the table.
* **Tier 2 is four times lower than tier 1 in nominal LOD, tier 3 another factor of two.** Tier 1 → 2: the beads
  capture 65 % of the sample instead of 1.4 %, on a surface that binds less conjugate. Tier 2 → 3: the transfer
  leaves the non-specifically bound conjugate behind, and the substrate background becomes the limit.
* **None of the three is predicted to reach the project's 1 pg/mL with confidence as specified.** Tier 2 does in
  18 % of the draws and tier 3 in 38 %; with screened reagents 31 % and 67 %. The earlier valve-and-chamber design
  stands at a median of 3.5 pg/mL, P 0.16, and 1.3 pg/mL, P 0.32 after screening (docs/08 §10): **tier 2 matches it
  with no valves, no dosing pump and no chamber**, because a fresh bed per determination is now allowed (docs/26,
  answer 2).
* The orchestrator's judgement of what a first working version would show, given what the model does not capture
  (section 6.4): tier 1 5–50 pg/mL, tier 2 1–10 pg/mL, tier 3 0.5–5 pg/mL if the transfer works. The literature
  task's independent estimate is 2–20, 0.5–5 and 0.5–3 pg/mL (docs/29 C.4).
* The same two measurements decide all three: the conjugate's non-specific binding per area (bench item U1 of
  docs/05, now also on the coated electrode and on the bed retainer) and the free hydroquinone in the HQDP lot (U3).

**Recommendation.** Build tier 2 first. It uses the strip cell the user named, the reagents already in the bill of
materials (docs/07 §1) and about ten new small parts, and it is the tier-3 design minus the valves. Run tier 1 beside
it only if the thiol chemistry is at hand; it is the cheapest to try and the least likely to go below 5 pg/mL.
Tier 3 adds its valves after the transfer has passed its tube test (docs/06 §4.12, Stage 1C).

## 1. What sets the LOD on this equipment

Four facts carry every choice below.

1. **The blank is non-specifically bound conjugate, not the electrode.** As in docs/04 and docs/05, the LOD is
   3 × the SD of the conjugate that sticks to every surface whose enzyme product reaches the electrode. In the
   limit of a short conjugate exposure the ratio of specific to non-specific label is
   (captured IgG per area) × k_on,detection / (non-specific rate × surface factor): it does not depend on the
   conjugate concentration or on the electrode area. What can be designed is the captured IgG per area, the surface
   factor, and which surfaces count.
2. **Both MicruX flow add-ons are wall-jet cells with a thin gap** (docs/28 §1 [V]): the stream enters through a
   bore above the centre of the working electrode and leaves radially. The whole sample passes over the electrode,
   not past it. For the thin gap the capture problem is identical to a channel in the swept area
   (`scripts/tier_round/README.md` B; checked against an independent Lighthill–Lévêque result within 1.2 %). At
   3.25 µL/min a 1 mm electrode under a 0.16 mm gap takes 1.4 % of the sample (mass-transfer coefficient
   1.9×10⁻⁶ m/s against a reaction velocity of 4.2×10⁻⁶ m/s); a 3 mm electrode under 0.2 mm takes 7 %. Stop-and-go
   loading is no better (1.42 % against 1.37 %; 4.5 % against 7.5 %), so the sample is pumped slowly and continuously.
3. **A bed of small beads captures by reaction, not by transport, and can be made as small as the kinetics allow.**
   1×10⁶ beads of 2.8 µm are 24 mm² and take 65 % of a 100 µL sample at 3.5 µL/min. The beads' own non-specific
   label is then smaller than that of the few square millimetres of frit that hold them.
4. **Product that forms on the electrode is collected in full, flow or no flow**; product that forms a millimetre
   away is collected only if the liquid stands still. Tier 1 therefore reads while the substrate flows (the
   conjugate stuck to the lid and to the chip around the electrode is washed downstream and does not count), and
   tier 2 stops the flow to keep the bed's product together.

Two things the literature settled (docs/29 Part A): hydroquinone from HQDP is the product to read on these
electrodes (p-aminophenol fouls printed carbon and gold, Buckey2022 [V-abs]); and amplification by a reductant in
solution has been shown only on ITO and on gold under long monolayers, never on printed carbon or bare thin-film
gold (Das2007, Kwon2008, Akanda2011, Akanda2013 [V-abs]). It also amplifies the blank by the same factor. It is not
used; the model puts it at 11 pg/mL nominal in tier 1, worse than the plain read.

## 2. What the three implementations share

### 2.1 Reagents (docs/07 §1; evidence labels as given there)

| Item | Choice | Source |
|---|---|---|
| Capture antibody | biotinylated goat F(ab′)₂ anti-human IgG, Fcγ-specific, cross-adsorbed (Jackson 109-066-098) | docs/07 §1 [D] |
| Detection conjugate | alkaline-phosphatase goat F(ab′)₂ anti-human IgG, F(ab′)₂-specific (Jackson 109-056-006) | docs/07 §1 [D] |
| Streptavidin beads (tiers 2, 3) | Dynabeads M-280 Streptavidin 11205D, 2.8 µm; about 10 µg biotinylated antibody per mg | docs/07 §1 [V]; docs/28 §6 [V] |
| Substrate | HQDP, Metrohm DropSens DRP-HQDP-0.5G; no purity or free-hydroquinone specification | docs/07 §1 [V]; docs/29 A.1.3 [V] |
| Standard | NISTmAb RM 8671 (after gate G1a), polyclonal human IgG for development | docs/07 §1 [D] |
| Blocker and carrier | IgG-free BSA (bovine IgG in ordinary BSA cross-reacts with anti-human-IgG reagents, docs/29 C.2) | docs/06 §4.0 |

The acceptance criteria for the antibody pair are those of docs/05 §4.1 (capture and detection half-lives ≥ 1 h, to
be measured in bench item U2). The detection conjugate's off-rate is the largest single sensitivity in all three
tiers: with its best estimate (half-life 13 min) about a third of the label leaves between the conjugate step and
the read.

### 2.2 Solutions

| Line or vial | Content | Note |
|---|---|---|
| BSM A1 | wash buffer: 50 mM Tris-HCl pH 7.5, 150 mM NaCl, 0.05 % Tween 20 | no phosphate (it inhibits the enzyme, docs/08 B1) |
| BSM B1 | substrate: HQDP in 0.1 M Tris pH 9.5, 1 mM MgCl₂, **150 mM NaCl**; 0.3 mM (tier 1), 1 mM (tiers 2, 3) | fresh daily, dark; the chloride keeps the printed Ag/AgCl reference where it was in A1 (docs/28 §4) |
| BSM A2 | water, then 10 % methanol for storage | docs/02 §1.2 |
| Tray vial, 4 °C | conjugate in assay buffer (wash buffer + 1 % IgG-free BSA): 10 nM (tier 1), 3 nM (tiers 2, 3) | injected as a full loop |
| Tray vial | assay buffer for a loop-cleaning injection before each determination | |
| Tray vial | 1 µM hydroquinone in substrate buffer, fresh, dark (tier 1 pre-run) | locates the oxidation wave on each chip |
| Tray vial (tier 3) | 2 mM D-biotin in assay buffer | elution |
| Sample vial | sample only; standards and blanks are made in assay buffer | docs/26 §3 |

0.3 mM HQDP in tier 1 is three times the Michaelis constant (87 µM at pH 10, Bekhit2021 [V-abs]; model value 0.1 mM):
the enzyme runs at 75 % of its maximum while the impurity current falls to a third. In tiers 2 and 3 the product
collects in 0.1 µL, where a higher substrate concentration delays depletion.

### 2.3 Flow path, control and timing rules

* BSM → mixer → restrictor 25 µm × 45 cm → SM-FL (100 µL loop, full loop) → 0.127 mm I.D. PEEK, 0.2 m → cell →
  short open waste line. Pressures: docs/27 §3.
* One determination is two sample-set lines after a pre-run line: line 1 injects the sample, line 2 the conjugate;
  the BSM programme of line 2 also carries the washes, the step to substrate and the read. Tier 3 adds one line
  (eluent).
* Flows: sample 3.25–4.5 µL/min; conjugate, washes and the step to substrate 50–80 µL/min (the step needs
  100–200 µL, docs/27 §1); read as stated per tier.
* The Gamry holds the read potential from the pre-run to the end and records continuously at 2–10 Hz; Inject Start
  of each line and one timed switch mark the record (docs/27 §5). The result is the charge in the read window minus
  the charge of the reference window named per tier.
* Washes are never shorter than 1.5 min after the sample and 2 min after the conjugate (the model does not credit
  wash efficiency, so shorter washes would gain by artefact; docs/05 §1.1).
* Before each determination (not counted in the 60 min, docs/26 §3): mount the fresh consumable, flush, one
  full-loop injection of assay buffer to clean needle and loop, then the pre-read of the tier.

### 2.4 Calibration, blanks and the LOD

A calibration is a set of determinations, each on its own fresh consumable: blanks (assay buffer), 0.3, 1, 3, 10,
30, 100, 1000 pg/mL. The LOD is the concentration at mean blank + 3 SD of at least ten blanks on ten consumables,
read through the curve (docs/26 §3). The unit-to-unit spread of the blank is therefore part of the LOD; the model
carries it as 10 % (model blank CV) plus 15 % (hand-coated electrodes) or 10 % (hand-packed beds), both UNVERIFIED
(`tier_params.yaml`).

## 3. Tier 1 — consumables only: the electrode is the solid phase

### 3.1 Design

| Element | Choice | Source and confidence |
|---|---|---|
| Cell | MicruX All-in-One cell with flow add-on ED-AIO-ADD-ON-FC-PMMA-2.0: wall jet, 0.5 mm inlet bore, 2.0 mm O-ring, < 0.5 µL | docs/28 §1 [V]; gap not published, 0.16 mm taken (0.10–0.30 as scenarios) |
| Electrode | MicruX ED-SE1-Au thin-film chip: 1 mm gold disc (0.785 mm²), gold counter and gold pseudo-reference on the chip; one chip per determination | docs/28 §2.2 [V] |
| Surface | mixed monolayer of a biotin-terminated and a hydroxy-terminated oligo(ethylene glycol) alkanethiol (about 1 : 9), then streptavidin, then the biotinylated capture F(ab′)₂, then assay buffer | principle: short OEG monolayers resist protein and pass p-aminophenol (Nishimura2011 [V-abs], docs/29 B.3); recipe and thiol part numbers UNVERIFIED |
| Capture | sample pumped through the cell at 3.25 µL/min for 39 min (127 µL: 98 % of the plug leaves the loop) | docs/27 §4 |
| Label | 100 µL of 10 nM conjugate passed in 2 min at 50 µL/min, no stop | exposure 20 nM·min |
| Read | substrate at 1 µL/min; electrode held on the hydroquinone plateau; 60 s to settle, 240 s read; reference window: the same read on the same chip before the sample | docs/27 §2, §5 |

Why thin-film gold. The surface decides tier 1, and an evaporated gold film under an OEG monolayer is the
best-defined low-adsorption surface the MicruX catalogue allows; its exposed area in the cell is 3.1 mm² against
50 mm² for a strip. The price is a small current (0.27 pA per pg/mL) and a gold pseudo-reference.

Why read under flow. In the stopped cell the electrode also collects the product of the conjugate stuck to the
chip around it and to the lid: 7.9 pg/mL nominal against 3.1 under flow (`tiers.md` §3). Under flow those
surfaces are downstream. The price is that the free hydroquinone of the substrate arrives continuously; it is
measured on the same chip in the pre-read and subtracted. Tier 1 therefore does not need the pump to stop.

### 3.2 Bench preparation (per batch of chips; UNVERIFIED as a recipe, each step is standard practice)

1. Clean the gold by cycling in chloride-free acid as the vendor prescribes (−1.0 to +1.3 V, ≥ 12 cycles, 0.1 V/s;
   docs/28 §4 [V]); rinse.
2. Monolayer: 1 mM total thiol in ethanol, a drop confined to the 2 mm opening, overnight in a closed humid box;
   rinse with ethanol and water. The drop covers working, counter and pseudo-reference electrodes alike.
3. Streptavidin 50 µg/mL in assay buffer without BSA, 30 min; rinse. Biotinylated capture F(ab′)₂ 10 µg/mL,
   30 min; rinse. Assay buffer 30 min. Store wet at 4 °C; shelf life to be measured.
4. For the non-specific-binding test make chips with biotinylated normal goat F(ab′)₂ instead (docs/07 §1).

### 3.3 Step table (53 min from Inject Start to result)

| Clock (min) | Step | BSM | SM-FL | Gamry |
|---|---|---|---|---|
| before | mount chip; flush A1 2 min at 50 µL/min; cleaning injection; hydroquinone plug: find the wave, set the read potential 0.25 V above its half-wave; B1 fill, 1 µL/min, **pre-read** 240 s; flush A1 | A1, B1 | assay buffer; 1 µM hydroquinone (20 µL partial loop) | on from here to the end |
| 0–1 | sample aspirated and loaded, Inject Start | A1 3.25 µL/min | line 1: sample, full loop | mark |
| 1–40 | sample through the cell | A1 3.25 µL/min | loop in line | — |
| 40–41.5 | wash 1 | A1 50 µL/min | — | — |
| 41.5–42.5 | conjugate aspirated and loaded | A1 50 µL/min | line 2: conjugate, full loop | mark |
| 42.5–44.5 | conjugate through the cell | A1 50 µL/min | loop in line | — |
| 44.5–46.5 | wash 2 | A1 80 µL/min | — | — |
| 46.5–48 | step to substrate | B1 80 µL/min | — | — |
| 48–49 | settle | B1 1 µL/min | — | — |
| 49–53 | **read** | B1 1 µL/min | — | charge over 240 s |

### 3.4 Where the number comes from (nominal; `tiers.json`)

| Quantity | Value |
|---|---|
| Sample molecules at 1 pg/mL | 4.0×10⁵ |
| Reaching the cell (adsorptive loss 20 %, loop transfer 98 %) | 3.1×10⁵ |
| Captured on the electrode | 5.5×10³ (1.4 %) |
| Labelled (36 %), still bound at the read (68 %), analyte still bound (83 %) | 1.1×10³ enzymes |
| Signal | 0.27 pA per pg/mL (1000 turnovers per second, 2 electrons) |
| Conjugate stuck to the electrode (surface factor 3) | 2.7×10³ enzymes; on the lid above it, 4 % collected |
| Blank equivalent | 5.2 pg/mL |
| Blank current incl. substrate background | 5.7 pA; noise 1 pA rms; drift 0.55 pA/min |
| Variance at the blank | drift 63 %, non-specific label 24 %, noise 5 %, substrate 4 % |
| LOD | 3.1 pg/mL; at the LOD the signal is 0.8 pA |

### 3.5 Scenarios and alternatives (`tiers.md` §2, §3)

| Case | Nominal | Median [5–95 %] |
|---|---|---|
| as specified | 3.1 | 16 [2.1–160] |
| detection reagent and substrate lot screened (L6 + L7) | 2.1 | 10 [1.6–74] |
| the same with the F(ab′)₂ credit (L3) | 1.9 | 7.9 [1.3–64] |
| conjugate binds non-specifically 25× more (S1) | 39 | 130 [15–1300] |
| free hydroquinone 10⁻³ in the substrate (S4a) | 49 | 94 [11–900] |
| gap 0.10 mm / 0.30 mm | 2.7 / 4.0 | 15 / 18 |
| pump cannot go below 10 µL/min: read at 10 µL/min | 3.4 | 19 [2.3–230] |
| read in the stopped cell | 7.9 | 30 [4.1–260] |
| no pre-read on the chip | 5.2 | 26 [3.0–470] |
| 3 nM conjugate for 5 min + 3 min stop, 36 min load | 4.3 | 20 [2.4–330] |
| **printed gold strip S1PE-AU10 in the strip cell, same chemistry** | 5.3 | 15 [2.4–130] |
| printed carbon strip S1PE-C21, adsorbed streptavidin | 9.4 | 25 [3.6–250] |
| printed carbon, strip-cell gap 0.10 / 0.50 mm | 6.6 / 16 | 19 / 37 |
| reductant in the stopped cell (chemical redox cycling) | 11 | 64 [6.9–880] |

The printed gold strip is the same assay in the cell the user named. Its electrode is nine times larger, so the
current is five times higher (1.4 pA per pg/mL) and the drift term matters less; its printed silver reference
stands apart from the working electrode and is not touched by the thiol. The model cannot separate the two (medians
15 and 16) because it gives printed gold the same surface factor as evaporated gold, which is unlikely to be true
for a printed ink. **They should be compared in the first tier-1 experiment.** Printed carbon with adsorbed
streptavidin needs no thiol chemistry and is the fallback.

### 3.6 What could make it fail, and the experiments that decide (in order)

| # | Experiment | Decides | Pass |
|---|---|---|---|
| T1-1 | Coated chip in the cell, substrate at 1 µL/min, no protein: noise, drift, hydroquinone wave and plateau, 0.1–100 nM hydroquinone in substrate buffer; 5 chips | whether a sub-pA signal can be read; the pseudo-reference | drift ≤ 0.6 pA/min, noise ≤ 1 pA rms, plateau ≥ 150 mV wide, response CV ≤ 6 % |
| T1-2 | Non-specific binding: non-immune chips, 10 nM conjugate 2 min, wash, read; 10 chips; thin-film gold and printed gold side by side | the surface factor and the unit-to-unit CV | ≤ 3×10³ enzymes on 0.785 mm² (about 0.7 pA), CV ≤ 20 % |
| T1-3 | Capture: 1 ng/mL IgG through the full protocol, 5 chips | captured fraction and labelling | ≥ 0.2 pA per pg/mL |
| T1-4 | Blanks on 10 chips, then 3, 10, 30, 100 pg/mL | the LOD | — |

Risks the model does not carry: the monolayer slows hydroquinone oxidation (a long plateau is needed; T1-1); the
thiol also covers the gold pseudo-reference (T1-1 measures its drift; the pre-run hydroquinone plug re-locates the
wave on every chip); gold thin film peels in chloride outside −0.3 to +0.6 V (docs/28 §4 [V]; the read stays
inside); protein adsorbed during the sample step may change the plateau current between pre-read and read.

## 4. Tier 2 — plus passive in-line parts: a hand-packed micro-bed in the inlet bore

### 4.1 Design

| Element | Choice | Source and confidence |
|---|---|---|
| Capture bed | 1×10⁶ Dynabeads M-280 Streptavidin (1.5 µL of stock) carrying the biotinylated capture F(ab′)₂, packed against a frit in a fused-silica capillary of 0.20 mm bore and 0.36 mm outside diameter: bed 19 nL, 0.6 mm long, 24 mm² of bead surface | beads docs/07 [V]; fritted capillary and its part numbers UNVERIFIED (class of part used in capillary LC) |
| Position | the capillary passes through the inlet port of the cell, sleeved to fill the 0.8 mm bore, and ends about 1 mm above the working electrode; 0.1 µL between bed and electrode | sleeve and fitting UNVERIFIED; bore 0.8 mm [V docs/28] |
| Cell and electrode | MicruX AIO-SPE cell with its flow add-on; printed carbon strip S1PE-C21 (3 mm working electrode, printed Ag/AgCl reference), blocked with assay buffer; the strip can stay for a series, the bed is new each time | docs/28 §1, §2.1 [V] |
| Capture | sample through the bed at 3.5 µL/min for 36 min; 65 % captured; pressure drop 1.1 bar | kit, bed correlation of the model |
| Label | 100 µL of 3 nM conjugate through the bed in 5 min at 20 µL/min | exposure 15 nM·min |
| Read | substrate in, flow stopped 7 min, then 5 µL/min for 90 s: the plug crosses the electrode, which converts 62 % of it; charge above the baseline before and after the peak | kit; docs/27 §2 for the stop |

Why beads of 2.8 µm. They are the surface on which the project's non-specific-binding rate is defined (surface
factor 1; docs/04 §3.1), they are already in the bill of materials, and a million of them is the smallest bed that
still takes two thirds of the sample.

Why at the tip. Every surface between the bed and the electrode that saw conjugate makes product during the stop,
and that product reaches the electrode with the plug. With the bed in a fitting on the port, 13 mm² of bore wall
lies in between. With the tip in the bore, only the frit does.

Why swept and not parked. Parked over the electrode, the plug is read together with the product of the conjugate
stuck to the strip (1.3 pg/mL nominal). Swept, the strip's own conjugate gives a steady current that is the same
before and after the peak and is subtracted.

The retainer is the open point. A 0.5 mm long silicate frit has an inner surface of the order of 20 mm²
(Derived: 4ε/d for 1.5 µm pores, UNVERIFIED), as much as the beads, and conjugate sticks to it more. The design
assumes 5 mm² (a frit of about 0.15 mm, or a woven screen). Model LOD for 1, 5 and 20 mm²: 0.36, 0.75 and
2.3 pg/mL. Experiment T2-1 measures it with an empty capillary.

### 4.2 Bench preparation

1. Coat beads in a tube: wash the stock three times in wash buffer (it is supplied in PBS), 10 µg biotinylated
   capture F(ab′)₂ per mg, 30 min, wash, assay buffer 30 min (docs/06 §4.0). Non-immune beads likewise with normal
   goat F(ab′)₂.
2. Pack: draw 1.5 µL of 10 mg/mL coated beads, diluted in 20 µL assay buffer, into the capillary from the open end
   with a syringe; follow with 50 µL assay buffer. Check the bed length under a lens (0.6 mm).
3. Sleeve the capillary, seat it in the inlet port with the tip 1 mm above the strip, mount the strip.
4. One capillary per determination. Used capillaries are discarded.

### 4.3 Step table (58 min)

| Clock (min) | Step | BSM | SM-FL | Gamry |
|---|---|---|---|---|
| before | mount bed and strip; flush A1; cleaning injection; B1 fill, stop 1 min, sweep: substrate baseline of this bed and strip; flush A1 | A1, B1 | assay buffer | on (+0.30 V vs the printed Ag/AgCl, set once per strip lot from a voltammogram) |
| 0–1 | sample loaded, Inject Start | A1 3.5 µL/min | line 1: sample, full loop | mark |
| 1–37 | sample through the bed | A1 3.5 µL/min | loop in line | — |
| 37–38.5 | wash 1 | A1 50 µL/min | — | — |
| 38.5–39.5 | conjugate loaded | A1 20 µL/min | line 2: conjugate, full loop | mark |
| 39.5–44.5 | conjugate through the bed | A1 20 µL/min | loop in line | — |
| 44.5–47.5 | wash 2 | A1 50 µL/min | — | — |
| 47.5–49.5 | step to substrate | B1 50–80 µL/min | — | — |
| 49.5–56.5 | **stop**: product collects in the bed | 0 µL/min | — | baseline |
| 56.5–58 | **sweep and read** | B1 5 µL/min | — | peak charge |

### 4.4 Where the number comes from (nominal)

| Quantity | Value |
|---|---|
| Captured at 1 pg/mL | 2.6×10⁵ (65 % of the vial) |
| Enzymes at the read | 3.9×10⁴ (labelled 26 %, label still bound 68 %) |
| Product in 7 min, in 0.11 µL | 2.3×10⁻¹⁴ mol |
| Signal | 2.8 nC per pg/mL, about 31 pA over 90 s |
| Conjugate on the beads / on the retainer | 2.1×10⁴ / 4.3×10⁴ enzymes |
| Blank equivalent | 1.7 pg/mL |
| Variance at the blank | non-specific label 93 % |
| LOD | 0.75 pg/mL |
| Upper limit by the model's slope criterion | 54 pg/mL (phosphate inhibition in the small volume; the curve stays monotonic above it) |

Range. The stop concentrates the product, and the released phosphate inhibits the enzyme (K_i UNVERIFIED,
docs/08 §10). A second, 30 s stop and sweep after the first read gives a low-gain point with an upper limit of
460 pg/mL for 2.5 min more; the load is then shortened to 33.5 min. docs/26 §3 asks for two decades above the LOD:
0.75 to 54 pg/mL is 1.9 decades with the long stop alone, 2.8 with both.

### 4.5 Scenarios and alternatives (`tiers.md` §2, §4)

| Case | Nominal | Median [5–95 %] | P(≤ 1) |
|---|---|---|---|
| as specified | 0.75 | 3.0 [0.51–45] | 0.18 |
| screened detection reagent and substrate lot (L6 + L7) | 0.48 | 1.7 [0.40–16] | 0.31 |
| the same with the F(ab′)₂ credit (L3) | 0.24 | 1.0 [0.26–8.0] | 0.48 |
| conjugate binds 25× more (S1) | 25 | 71 [6.7–1300] | 0.00 |
| free hydroquinone 10⁻³ (S4a) | 11 | 22 [2.6–270] | 0.00 |
| blanks contaminated up to 1 pg/mL (C1) | 0.75 | 3.3 [0.71–45] | 0.10 |
| retainer 1 mm² / 20 mm² | 0.36 / 2.3 | 1.8 / 7.2 | 0.28 / 0.07 |
| bed in a fitting on the port, 1 mm² screen | 0.72 | 3.3 [0.57–39] | 0.14 |
| 20 µm polystyrene streptavidin beads, 0.15 µL, on the port | 1.7 | 7.0 [0.97–80] | 0.05 |
| half / twice the beads | 0.90 / 0.85 | 3.9 / 3.0 | 0.14 / 0.16 |
| **pump cannot stop: continuous read at 1 µL/min** | 1.6 | 6.1 [1.0–68] | 0.05 |
| pump cannot stop and cannot go below 10 µL/min | 3.2 | 15 [1.9–220] | 0.01 |
| parked read | 1.3 | 4.9 [0.76–69] | 0.09 |
| strip-cell gap 0.10 / 0.50 mm | 0.75 / 0.76 | 3.0 / 3.0 | 0.18 |

The cell's unknown gap does not matter in tier 2: the electrode only has to convert a plug.

### 4.6 What could make it fail, and the experiments that decide

| # | Experiment | Decides | Pass |
|---|---|---|---|
| T2-1 | Empty fritted capillary (no beads) through conjugate, wash, stop, sweep; 5 capillaries; then with non-immune beads | conjugate on the retainer against conjugate on the beads | retainer ≤ beads; blank peak CV ≤ 15 % |
| T2-2 | Zero-flow row (docs/27 §9 item 2); creep after the stop seen as the time the peak arrives | whether the stop exists | peak arrival reproducible within 5 s |
| T2-3 | Breakthrough: 1 ng/mL IgG at 2, 3.5, 7 µL/min; signal against flow | captured fraction; bypass through a short bed | ≥ 50 % at 3.5 µL/min |
| T2-4 | Bed-to-bed: 10 beds, 100 pg/mL | packing reproducibility | signal CV ≤ 10 % |
| T2-5 | Blanks on 10 beds; 0.3–100 pg/mL | the LOD | — |

Risks the model does not carry: channelling through a bed three bead-layers per 10 µm long (T2-3); bed compaction
at the 50–80 µL/min flushes (25 bar; if seen, flush at 30 µL/min and add 2 min); the dead annulus if the sleeve does
not fill the bore (air, slow exchange); bead loss through the frit; hydroquinone autoxidation at pH 9.5 during the
7 min stop (in the model as a half-life; sulfite stabilises the current, Bekhit2021 [V-abs], untested here).

## 5. Tier 3 — anything: valves, and an immune-complex transfer to a clean bed

### 5.1 Design

Tier 3 keeps the tier-2 bed, electrode and read, and adds what the blank asks for: the conjugate that sticks to the
capture bed and its retainer must not be there when the product is made.

| Element | Choice | Source and confidence |
|---|---|---|
| Capture bed (bed 1) | as tier 2, but the capture F(ab′)₂ carries desthiobiotin instead of biotin (NHS-desthiobiotin, Thermo 16129) | docs/06 §4.12; Hirsch2002 (docs/05) |
| Read bed (bed 2) | 1×10⁶ beads carrying a second antibody that binds the complex but not the conjugate, in the capillary above the electrode | **antibody not yet identified** (docs/06 §4.12, docs/07 §1.4: UNVERIFIED) |
| Valves | two 2-position 6-port PEEK valves (IDEX MXP9900-000), Python-driven as in docs/05 §4.1 | docs/07 §2 [V] |
| Transfer | 100 µL of 2 mM D-biotin injected by the SM-FL, held on bed 1 for 5 min, then pushed through bed 2 at 5 µL/min; wash | magnitude UNVERIFIED: non-specific label ×0.1 (0.01–0.5), specific ×0.7 (0.4–0.9), `ma.design_levers` |
| Read | substrate through bed 2 only; bed 2 isolated by its valve for 7 min; swept over the electrode | as tier 2 |

```
SM-FL -> V1 -> [bed 1] -> V2 -> [bed 2 -> cell] -> waste
V1: A = through bed 1,  B = bed 1 bypassed.     V2: A = to waste (bed 2 and cell isolated),  B = through bed 2 and cell.
sample, wash, conjugate, wash : V1 A, V2 A   (conjugate never reaches bed 2 or the electrode)
eluent                        : V1 A, hold; then V2 B
wash of bed 2, substrate fill : V1 B, V2 B
accumulation                  : V2 A (pump keeps running to waste)        read: V2 B
```

What the valves alone give (no transfer): the tier-2 LOD (0.71 nominal, median 2.9) without the zero-flow step and
with an electrode that never sees conjugate. What the transfer adds, if it performs as bounded: 0.33 nominal.

An alternative transfer chemistry that needs no second anti-IgG antibody is the original one of Ishikawa: capture
antibody labelled with both dinitrophenyl and biotin, held on anti-dinitrophenyl beads, released by
dinitrophenyl-lysine and re-captured on streptavidin beads (Ishikawa1990, Hashida1997; docs/05 references). It was
developed with elution times of hours in tubes (recalled, UNVERIFIED); whether 5 min in a bed suffices is as open as
for desthiobiotin.

### 5.2 Step table (58 min)

| Clock (min) | Step | Valves | BSM | SM-FL |
|---|---|---|---|---|
| 0–1 | sample loaded | V1 A, V2 A | A1 4.5 µL/min | line 1 |
| 1–30 | sample through bed 1 (58 % captured) | V1 A, V2 A | A1 4.5 µL/min | loop in line |
| 30–31.5 | wash 1 | V1 A, V2 A | A1 50 µL/min | — |
| 31.5–37.5 | conjugate loaded and passed | V1 A, V2 A | A1 20 µL/min | line 2 |
| 37.5–39.5 | wash 2 | V1 A, V2 A | A1 50 µL/min | — |
| 39.5–47.5 | eluent loaded, held on bed 1, pushed through bed 2; wash of bed 2 | V1 A then V2 B; V1 B | A1 5–50 µL/min | line 3 |
| 47.5–49.5 | substrate to bed 2 | V1 B, V2 B | B1 50 µL/min | — |
| 49.5–56.5 | accumulation | V2 A | B1 to waste | — |
| 56.5–58 | sweep and read | V2 B | B1 5 µL/min | — |

### 5.3 Numbers (`tiers.md` §2, §5)

The transfer enters the kit as two sampled factors on the tier-2 bed: specific complexes × 0.7 (0.4–0.9),
non-specific label of bed and retainer × 0.1 (0.01–0.5).

| Case | Nominal | Median [5–95 %] | P(≤ 1) |
|---|---|---|---|
| as specified (transfer at its bounded magnitude) | 0.33 | 1.4 [0.28–43] | 0.38 |
| screened detection reagent and substrate lot (L6 + L7) | 0.11 | 0.74 [0.18–3.0] | 0.67 |
| the same with the F(ab′)₂ credit (L3) | 0.092 | 0.64 [0.15–1.9] | 0.76 |
| with a reference channel as well (L5) | 0.32 | 1.3 [0.27–42] | 0.39 |
| accumulation 12 min instead of 7, load 24 min | 0.26 | 1.3 [0.26–36] | 0.41 |
| transfer at its optimistic bounds (×0.01, ×0.9) | 0.22 | 0.91 [0.18–31] | 0.54 |
| transfer at its pessimistic bounds (×0.5, ×0.4) | 1.6 | 6.5 [0.83–180] | 0.07 |
| transfer does not work, same timing | 1.2 | 4.4 [0.62–120] | 0.12 |
| valves only, tier-2 timing | 0.71 | 2.9 [0.50–40] | 0.18 |
| blanks contaminated up to 1 pg/mL (C1) | 0.33 | 2.0 [0.41–43] | 0.22 |
| conjugate binds 25× more (S1) | 4.5 | 12 [0.97–410] | 0.05 |
| free hydroquinone 10⁻³ (S4a) | 24 | 41 [3.8–1100] | 0.00 |

With the transfer the blank equivalent falls to 0.39 pg/mL and other terms show: the substrate background (44 % of
the variance at the blank), drift (25 %), and in the Monte Carlo the human IgG that reaches a blank from the
laboratory (the largest term in 51–60 % of the draws once the reagents are screened). Below about 0.5 pg/mL the
assay measures the cleanliness of the substrate and of the blanks. Two additions that "anything" allows are
therefore not in the design: a second potentiostat channel with a reference bed changes the median from 1.4 to 1.3,
and an interdigitated array with redox cycling amplifies the signal together with the substrate background. A pessimistic
transfer (half of the non-specific label comes along, 40 % of the complexes) is worse than no transfer at tier-2
timing: the transfer has to pass its tube test before the valves are bought for it.

The earlier design of this project (dosing pump, stirred chamber, magnetic trap; docs/05 §4.1) remains the
alternative. Its strength is the simultaneous incubation; its model numbers with the commercial thin-layer cell are
a median of 3.5 pg/mL as specified and 1.3 after screening (docs/08 §10), against 2.9 and about 1.7 for the valve-only
bed here. The flow-through bed gains no LOD from a chamber, and loses a dosing pump.

### 5.4 What could make it fail

| # | Experiment | Decides | Pass |
|---|---|---|---|
| T3-1 | Stage 1C of docs/06 §4.12 in tubes, with the elution cut to 5 min | whether the transfer exists at this time scale | blank reduced ≥ 5× with ≥ 50 % recovery |
| T3-2 | A phase-2 antibody that binds captured, labelled NISTmAb and not the goat reagents | the read bed | as docs/06 §4.12 |
| T3-3 | Tier-2 experiments T2-1 to T2-5 on the valve set-up | the base | as tier 2 |
| T3-4 | Blank handling: blanks prepared in a hood with dedicated consumables against open-bench blanks | the contamination floor | ≤ 0.1 pg/mL equivalent (docs/05 U9) |

## 6. Comparison

### 6.1 The same quantities side by side (nominal)

| | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Captured fraction of the sample | 1.4 % | 65 % | 58 % (shorter load) × transfer 70 % |
| Enzymes at the read per pg/mL | 1.1×10³ | 3.9×10⁴ | 1.7×10⁴ |
| Signal per pg/mL | 0.27 pA for 240 s (64 pC) | 2.8 nC | 1.2 nC |
| Blank equivalent (pg/mL) | 5.2 | 1.7 | 0.39 |
| Largest variance term | drift | non-specific label | substrate background, then non-specific label and drift |
| Needs the pump to stop | no | yes (fallback 1.6) | no |
| Needs the pump at 1 µL/min | yes (at 10 µL/min: 3.4) | no | no |
| New consumable per determination | chip | capillary bed (strip stays) | two capillary beds |
| Hands-on preparation | monolayer overnight, two 30 min steps | bead coating 1.5 h per batch, packing 5 min each | as tier 2, twice |

### 6.2 Largest sensitivities (one parameter at its bounds; `tiers.md` §6)

| Parameter [low–high] | Tier 1: LOD at low / high | Tier 2 | Tier 3 |
|---|---|---|---|
| detection off-rate 8.6×10⁻⁴ s⁻¹ [3×10⁻⁶–8.3×10⁻³] | 2.0 / 130 | 0.46 / 48 | 0.14 / 480 |
| free hydroquinone 10⁻⁵ [10⁻⁷–10⁻³] | 3.1 / 49 | 0.75 / 11 | 0.25 / 24 |
| non-specific rate 4×10⁻¹¹ m/s [0.8–40×10⁻¹¹] | 2.7 / 16 | 0.19 / 8.6 | 0.28 / 1.7 |
| enzyme turnover 1000 s⁻¹ [100–6000] | 27 / 1.6 | (small) | 2.8 / 0.18 |
| surface factor of the coated gold 3 [0.5–30] | 2.7 / 14 | — | — |
| surface factor of the retainer 10 [1–100] | — | 0.31 / 5.8 | 0.29 / 1.2 |
| drift scales with electrode area: exponent 1 [0–1] | 23 / 3.1 | — | — |

### 6.3 What holds in every scenario run

* The order tier 3 < tier 2 < tier 1 holds in every row of `tiers.md` except where the transfer fails (tier 3
  without it is 1.2 nominal, worse than tier 2, because the path is longer).
* A substrate lot with 10⁻³ free hydroquinone puts every tier above 10 pg/mL nominal (49, 11, 24). A conjugate that
  binds 25× more than the plate anchor puts tier 1 at 39 and tier 2 at 25; tier 3 holds at 4.5 if the transfer
  performs. These are the two kill conditions of docs/05 §5.
* Screening the detection reagent for a half-life of at least 1 h and the substrate lot for 10⁻⁶ free hydroquinone
  is worth a factor of 1.5 in tier 1, 1.6 in tier 2 and 3.0 in tier 3.

### 6.4 Why the judgement is above the model

The model does not carry: channelling in a hand-packed bed; the monolayer's effect on the hydroquinone current;
drift of the pseudo-reference; the pump's behaviour at 1–5 µL/min and 100–330 psi; protein fouling of the
electrode by the sample and conjugate that now pass over it; temperature; human IgG from the laboratory (nominal
zero in the model, sampled up to 0.45 pg/mL). Each is more likely to hurt than to help. The unit-to-unit CVs of
hand-made consumables (15 % and 10 %) are guesses.

## 7. Bench order

1. **Instrument facts** (docs/27 §9, two days): low flow, zero-flow row, cell gap, cell pressure, loop draw,
   reference stability. They decide between primary and fallback read in tiers 1 and 2 before any reagent is used.
2. **The shared Stage 1A experiments of docs/06** (E1.1 readout, E1.2 free hydroquinone, E1.3 conjugate
   non-specific binding on beads), run with the MicruX strip in its cell as the electrode. Nothing in them changes;
   gate G1a is unchanged.
3. **Tier 2**: T2-1 (retainer), T2-2 (stop), T2-3 (breakthrough), T2-4, T2-5. Parts: fritted capillaries, sleeves,
   one fitting, the restrictor; no instrument purchase.
4. **Tier 1 beside it** if wanted: T1-1 and T1-2 need only chips, thiols, streptavidin and conjugate, and T1-2
   answers on its own whether tier 1 can pass 5 pg/mL.
5. **Tier 3** after Stage 1C (docs/06 §4.12) has passed in tubes: add the two valves to the tier-2 set-up.

This round changes no gate, no kill criterion and no order in docs/06. Whether its experiments are added to that
plan is the user's decision (section 8).

## 8. Choices the user may overrule, and open questions

Choices made here:
1. Tier 1 on thin-film gold rather than on the printed strips named in the request (the printed gold strip is the
   equal-median alternative, section 3.5).
2. Tier 1 reads under flow at the pump's minimum rather than in a stopped cell.
3. Tier 2 uses the project's 2.8 µm magnetic beads in a fritted capillary, not a bought micro-column, and no magnet.
4. Tier 3 is the tier-2 bed with valves and a transfer, not the dosing-pump design of docs/05.
5. The range is reported, not enforced (docs/26 §3); tier 2 covers two decades only with its second, short read.
6. The gap of the strip cell is taken as 0.2 mm (the user's 10 µL) and that of the thin-film cell as 0.16 mm
   (vendor's < 0.5 µL).

Questions only the user can answer (docs/27 §9, docs/28 §8):
1. Which flow add-on and which electrodes are in hand (part numbers on the packs)?
2. Where does "10 µL" come from? MicruX states < 5 µL for the strip cell and < 0.5 µL for the thin-film cell.
3. Does a BSM method accept a 0.000 mL/min row, and is the 1 µL/min minimum confirmed on this instrument?
4. Is a restrictor installed, and which?
5. Should the tier experiments of section 7 enter the bench plan (docs/06), and before or after gate G1?

## 9. Reproduction and references

```bash
pip install -e .
python scripts/tier_round/check_tierkit.py     # 36 checks
python scripts/tier_round/run_tiers.py         # results/tier_round/tiers.md, tiers.json
```

Designs: `scripts/tier_round/run_tiers.py` (`t1`, `t2`, `t3`) and `designs.py`. Parameters added by this round:
`scripts/tier_round/tier_params.yaml` (all UNVERIFIED engineering estimates unless a source is named).

References are held where they were checked: MicruX and parts in docs/28 §9; Waters in docs/27 Appendix A;
literature keys (Nishimura2011, Bekhit2021, Buckey2022, Das2007, Kwon2008, Akanda2011, Akanda2013, Squires2008 and
others) in docs/29 A.R and B.R and in docs/01; Ishikawa1990, Hashida1997 and Hirsch2002 in docs/05; reagents in
docs/07 §9.
