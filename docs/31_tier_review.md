# 31 — Independent review of the three implementations, and resolution of the findings

Status: 2026-11-18. Written by the orchestrator. Section 1 says how the review was made, section 2 gives its
result in short, section 3 lists every finding of the first review with what was done, section 4 does the same
for the second pass, section 5 says where the changes in the predicted LODs come from, section 6 lists the
findings that reach beyond this round, section 7 what is still open.

Evidence labels as in the reviewer reports: **[V]** opened by the reviewer in the session, **[V-abs]** abstract read,
**[S]** search summary only, **Derived** (calculation named), **UNVERIFIED**.

## 1. How the review was made

| Round | Reviewed | Reviewer (lens) | Report | Own calculation |
|---|---|---|---|---|
| 1 | first version of docs/30 (commit 7bff783), docs/26–29, the kit | Numbers: every number re-derived without the kit; physics; Monte Carlo wiring | `results/tier_round/review_numbers.md` (N1–N13) | `scripts/tier_round/review_numbers.py` |
| 1 | the same | Chemistry: reagents and vendor pages re-opened; surface, substrate and label chemistry; bench realism | `review_chemistry.md` (C1–C12) | `review_chemistry_calc.py` |
| 1 | the same | Feasibility: Waters, Gamry and MicruX constraints; docs/26 constraints; consistency; tier 3 | `review_feasibility.md` (F1–F10) | `review_feasibility_calc.py` |
| 2 | Revision B of docs/30 and docs/27 (commit 0578dfc), the revised kit | Numbers and physics of the revision | `review2_numbers.md` (its R1–R10, here **M1–M10**) | `review2_numbers.py` |
| 2 | the same | Resolution of the round-1 findings, step tables, consistency, sourcing | `review2_consistency.md` (its R1–R14, here **K1–K14**) | `review2_consistency.py` |

The reviewers were independent agent tasks with no part in writing the designs. Their reports are kept as written;
section numbers and values in them refer to the version they reviewed. After each round the orchestrator changed
the kit and the designs, re-ran every number and rewrote the documents (Revision B after round 1, Revision C after
round 2).

**Revision C was not reviewed again.** Its kit changes answer the findings of round 2, but the orchestrator also
moved the operating points afterwards (section 4.3). What checks it: the 36 kit checks, the cross-check with the
audited model, and `scripts/tier_round/doc_tables.py --check`, which compares the tables of docs/30 with the model
output.

## 2. Result in short

* **The numbers were faithful to the kit in both rounds** (36 of 36 checks; independent recomputation within 1 %
  in round 1 and within 1.4 % in round 2). **The kit left out physics that sets the blank**, one step of every
  method could not work as written, and two assumptions of the chemistry are open.
* Round 1 rated four findings blocking: the tier-1 read had no reference window near it (N1) and ignored the
  conjugate on the walls upstream of the electrode (N2); no step table set Loop Offline, so the substrate would
  not have reached the cell (F1); and at picomolar enzyme the product of hydroquinone diphosphate should be the
  monophosphate, not hydroquinone (C1, blocking until tested). N1, N2 and F1 are resolved. C1 cannot be resolved
  on paper.
* Round 2 found no error in the numbers of Revision B and eight significant gaps: the tier-1 read compared two
  different buffers (M1); the short half-life of hydroquinone was applied to the product but not to the substrate
  reservoir (M2); the read bed of the transfer was nearly full of capture antibody (M3); the push of the transfer
  followed a flow step (K2); the current ranges clipped inside the calibration (K3); the transfer was still
  presented at a release nobody has measured (K7); parts of what docs/26 asks of every design were missing for
  tier 3 (K4); and two numbers had no source in the repository (K8). All are resolved in Revision C.

| | First version: nominal; median | Revision B | Revision C: nominal; median [5–95 %]; P(LOD ≤ 1 pg/mL) |
|---|---|---|---|
| Tier 1 | 3.1; 16 | 9.4; 35 [4.4–560] | 3.6; 16 [2.8–110]; 0.00 |
| Tier 2 | 0.75; 3.0 | 2.6; 13 [1.4–170] | 2.1; 8.4 [1.0–100]; 0.05 |
| Tier 3, one valve | not computed | 1.5; 6.9 [0.87–85] | 1.2; 5.1 [0.78–58]; 0.09 |
| Tier 3 with the transfer | 0.33; 1.4 (transfer 0.7) | 0.62; 4.8 [0.54–260] (release 0.7) | 1.1; 5.8 [0.64–280]; 0.12 (release 0.35). At a release of 0.7: 0.53; 2.0 |

The order tier 3 < tier 2 < tier 1 survived every change. Two claims did not: that tier 3 is better than the
earlier design of docs/05 (F5), and that the transfer is the tier-3 design (K7): one valve without transfer now
is.

## 3. Round 1: findings and resolution

Status words: **Resolved** = design or kit changed and the numbers re-run. **Bounded** = carried as a parameter
range or a scenario; a named bench experiment decides. **Open** = stated in docs/30; needs a measurement or a
vendor answer. **Not adopted** = with the reason. Numbers are those of Revision C unless marked.

### 3.1 Numbers and physics (N)

| # | Severity | Finding | What was done | Status |
|---|---|---|---|---|
| N1 | blocking | Tier 1's only reference was the read made on the chip before the sample, 55 min before the read. From the drift over that time alone the LOD is 17–69 pg/mL (reviewer, Derived) | The read is reference → substrate → reference at one constant flow: two windows 3.7 min apart bracket the read. The kit takes the time between them (`read.t_span_s`) for the drift. The pre-run sequence on the fresh strip is used only for the substrate's own background | Resolved |
| N2 | blocking | Conjugate on the inlet bore and the transfer line was not counted, though its product flows onto the electrode (30–59 pg/mL as written; reviewer, Derived) | `evaluate_planar` counts both walls, collected at the conversion of the stream. The design reads at 200 µL/min, where that conversion is 6 % while the electrode's own enzyme is collected in full, and uses a 0.05 mm × 15 cm line (24 mm² instead of 80 mm²). Loop Offline is set before the substrate. Build-up on the line from run to run is not modelled | Resolved; build-up Open |
| N3 | significant | Tier 2: walls above the bed that saw conjugate stand in substrate during the stop; their product follows the plug into the read window | `evaluate_bed` counts the capillary above the bed and the transfer line in full. They are 45 % of the blank. Without them the LOD would be 1.1; a valve removes them (tier 3). T2-1 measures an empty capillary against a bed | Resolved |
| N4 | significant | Tier 2: the baseline of the swept read is a step, not a constant: the electrode empties its layer of free hydroquinone during the stop, and the sweep brings it back while the peak passes | The pre-run of tier 2 is the identical substrate step, stop and sweep on the fresh bed and strip; its trace is subtracted, and 4 % [1–10 %] of the step is taken as left. In tier 3 the cell stays in flowing substrate, so there is no step. After M2 the step is 1 pA unless the background does not decay | Resolved (tier 3), Bounded (tier 2) |
| N5 | significant | The bed was given the surface factor of beads washed in tubes (1), not the model's packed-bed factor (3 [1–30]) | Packed-bed factor used; factor 1 is a case (1.6) | Resolved |
| N6 | significant | A transfer efficiency of 0.7 needs complete release, because re-capture at 5 µL/min is itself only 0.70 | Transfer = released fraction × re-capture at 2 µL/min from the bed equation. See C8, F4, M3, K7 for what became of both factors | Resolved as a model; release Open |
| N7 | significant | The most favourable scaling of drift with electrode area was the nominal | Exponent 0.5 [0–1]; the tier-1 electrode is now the model's reference area, where the exponent does not act | Resolved |
| N8 | significant | Tier 2's "upper limit 460 pg/mL" belonged to a different design | docs/30 §2.4 gives, per design, the upper limit by the slope criterion, the concentration up to which the curve rises, and the decades above the LOD (tier 2: 1400 pg/mL, 2.8 decades, with its 5 min stop) | Resolved |
| N9 | minor | The wall-jet mapping is exact only for lubrication flow; the check R1 compares two forms of the same assumption; the stagnation disc is dropped | Stated in the README (Limits) and in docs/30 §6.4, with the Reynolds number at the read flow | Resolved by statement |
| N10 | minor | The rule for product formed on the lid overcounts | Stated as an upper estimate in the README; effect < 10 % | Resolved by statement |
| N11 | minor | 1 % residual for a background read 55 min earlier is optimistic; 3 % [1–10 %] proposed | `tr.noise.preread_residual_cv` 3 % [1–10 %] (the high bound was 6 % in Revision B; K10) | Resolved |
| N12 | minor | Optimistic or unstated defaults (frit area, unit-to-unit CVs, gap, bore length); the product diffusion coefficient and the reservoir age are not sampled | Frit 1, 5 and 20 mm² are cases (1.7, 2.1, 3.4), as are the gaps; the CVs are sampled. What is uncertain but not sampled is listed in docs/30 §6.4 and in the README | Bounded; sampling Not adopted |
| N13 | minor | Eight text slips | Corrected; the result tables of docs/30 are now generated from the model output | Resolved |

### 3.2 Chemistry and bench realism (C)

| # | Severity | Finding | What was done | Status |
|---|---|---|---|---|
| C1 | blocking until tested | Alkaline phosphatase removes one phosphate per turnover. From the diphosphate it makes the monophosphate, which is hydrolysed again only in competition with a thousandfold excess of diphosphate: hydroquinone/monophosphate ≈ 10⁻⁴–10⁻³ after the tier-2 stop (Derived). No paper found addresses it (Wilson2004 used a dense enzyme layer, Bekhit2021 exhaustive coulometry [V-abs]). If the monophosphate is not oxidised at the read potential, all signals are 10²–10⁵ too high | docs/30 §2.6 states the question, the three outcomes and the half-day test. The read potential is to be set on enzyme-generated product. Alternatives named: p-hydroxyphenyl phosphate (supplier not found, docs/07 §6), ascorbic acid 2-phosphate. Scenarios: 1 % of the turnovers electroactive gives 200, 13, 20 and 42 pg/mL; 0.1 % gives 2000, 120, 200 and 420. The operating points of tiers 2 and 3 were chosen to leave current for this case (section 4.3) | **Open: first bench experiment** |
| C2 | significant | Tier 1 assumes hydroquinone is oxidised through a thiol monolayer and a protein layer without penalty; common biotin-OEG thiols have a C11 chain; gold in chloride allows only −0.3 to +0.6 V | Short-chain thiols specified as a class (part numbers UNVERIFIED). The reviewer's pass criterion is in T1-1. The fraction of the transport-limited current that the coated gold delivers is a kit parameter (`tr.detection.monolayer_collection_efficiency`, 1 [0.1–1], sampled); at 0.3 the LOD is 7.2. Printed carbon without a monolayer is the fallback (11) | Bounded |
| C3 | significant | The thiol and protein coat also covered the chip's gold pseudo-reference, which carries the drift | The electrode is the printed gold strip, whose printed silver reference stands apart; the drop covers the working electrode only. Reference stability is checked (docs/27 §9 item 8, T1-1) | Resolved by design |
| C4 | significant | The detection conjugate 109-056-006 is not adsorbed against bovine proteins and is stabilised with BSA [V]; the M-280 stock contains 0.1 % ordinary BSA [V] | Stated in docs/30 §2.1 with the request for the stabiliser's certificate. Beads are washed and re-blocked in IgG-free BSA. T2-1 compares beads as supplied with re-blocked beads. A bovine-adsorbed conjugate is to be found | Bounded; reagent Open |
| C5 | significant | Hydroquinone half-life at pH 9.5 is about 7 min by extrapolation of half-lives at pH 7–9 ([S], compilation quoting Moussavi 1979; primary source not opened), not the model's 2 h | This round uses 600 s [120–7200] (`run_tiers.base_params`; `params/` not edited), and after M2 for the whole liquid path. Standards are kept at pH 7.5. Question 2 of docs/30 §2.6 measures it, with and without sulfite | Resolved for this round; value UNVERIFIED |
| C6 | significant | The add-on is clamped by magnets a few millimetres from a bed of magnetic beads; proposal: hold the bed with a magnet and drop the frit | The check of the bed with the add-on in place is in docs/30 §4.2 and T2-3; non-magnetic particles are the fallback. **The magnet-held bed is not adopted**: a plug that fills the bore carries the whole pressure drop, 25 bar × 0.031 mm² on 10⁶ beads = 78 nN per bead at 80 µL/min and 3 nN at the loading flow, against 0.02–0.2 nN of magnetic force (Derived: 2×10⁻¹³ A·m² per bead at saturation, gradient 100–1000 T/m; UNVERIFIED order of magnitude). The feasibility reviewer reached the same result | Bounded; proposal Not adopted |
| C7 | significant | Tier 2 reused the strip, but every determination passes conjugate over it | A fresh strip with every bed | Resolved |
| C8 | significant | A 5 min release of desthiobiotin by biotin is unsupported: 0.3–26 % from the affinity (Derived; K_d UNVERIFIED), "too slow" in Ying, Branchaud and Corry 2011 [V]; and the read bed has to take all released capture antibody. Proposed bound for the transfer: 0.05–0.7 | Desthiobiotin is a case (3.7 nominal, worse than no transfer). The route taken for the model is a cleavable link with a hapten tag; every part of it is UNVERIFIED. Release 0.35 [0.05–0.74], which with the computed re-capture is the bound asked (K7). The capacity of the read bed is in the kit and in the design (M3). T3-3 measures release, re-capture with the full antibody load and the leak from bed 1 | Bounded; chemistry Open |
| C9 | minor | 0.1 M Tris buffers weakly at pH 9.5 (8 mM per pH unit, Derived); the turnover number is not tied to the buffer | The product test compares Tris with 1 M diethanolamine pH 9.8 | Adopted |
| C10 | minor | Buildability of the capillary bed: sleeve fit, frit pore size unknown, bed compacts at the first fast flush | Pre-compaction and a mechanical stop for the tip are in docs/30 §4.2; the sleeve is cited as a class of part [S]. A tapered tip without a frit is an option if T2-1 shows the frit dominates (UNVERIFIED for 2.8 µm beads) | Adopted |
| C11 | minor | No purity, free-hydroquinone or monophosphate specification on the substrate | Stated; the separation in the product test measures both; a certificate of analysis is to be asked for (docs/07 §6 already lists it) | Adopted |
| C12 | minor | A surface factor below 1 for the coated gold has no support | Low bound 1 (3 [1–30]) | Resolved |

### 3.3 Feasibility, constraints, consistency (F)

| # | Severity | Finding | What was done | Status |
|---|---|---|---|---|
| F1 | blocking | No table set Loop Offline. With the 100 µL loop in line the programmed 100–160 µL of substrate does not reach the cell; with the loop offline it reaches 52–82 % | Loop Offline is in every step table, after two loop volumes have followed the reagent and before a change of composition. A composition change is 215 µL (95 %; Derived by the reviewer). docs/27 §1 and §9 item 9 (dye test) | Resolved; volumes to be measured |
| F2 | significant | Pressure relaxation was computed for 1000 psi, but the stops start from 5000–8100 psi: 6.4–10.2 µL creep through the bed; the real compliance is unknown | The Waters 40 µm restrictor is now the first choice (960 psi at 80 µL/min, about 1 µL stored). Step-down rule: 1 min at 5 µL/min before the stop. Tier 1 has no flow step around its read. docs/27 §2, §3 and §9 item 10 | Resolved by design and rule; compliance Open |
| F3 | significant | Tier 3 did not fit 58 min as described, and its "hold" was not a hold with the valve open | Step tables rebuilt from flows and volumes; bed 1 is closed by its valve for the hold; totals 56.7 min (one valve) and 58.2 min (transfer). See K2, K6 for the eluent rows | Resolved |
| F4 | significant | The transfer efficiency 0.7 [0.4–0.9] cannot be reached with one pass at 5 µL/min; capture antibody also leaks from bed 1 before the release | As N6. The leak arm is in T3-3 | Resolved as a model |
| F5 | significant | The comparison with the docs/05 design was unfair: its row with the transfer (nominal 0.29, median 1.5, P 0.33) was not quoted, the P values use different criteria, and the models differ | docs/30 §0 and §5.6 quote both rows, say that the two sets of numbers are not on the same footing and that neither design is shown to be better. The docs/05 design was not run through the kit: the kit has no chamber or trap format (its bed format agrees with the model to 10⁻⁹ on the overlapping case) | Resolved by statement |
| F6 | significant | "Valves only: an electrode that never sees conjugate" contradicted the geometry | Claim dropped. The one-valve design is modelled with its loop walls (10 mm²), a transit volume of 4 µL and the cell in flow; docs/30 §5.1 says that the cell sees the conjugate | Resolved |
| F7 | significant | Current range, potential hold and the signal routine were not specified; the Gamry backend of `automation/` is a stub and its signal routine cannot subtract a pre-run | Range, potential and marks are in docs/30 §2.3 and in every step table (K3, K4). No code was written: `automation/` is outside this round | Stated; software Open |
| F8 | minor | 0.5 µL, not 0.1 µL, lie between the capillary tip and the electrode, with 2.5 mm² of conjugate-exposed bore wall | Wall counted; 0.5 µL in the kit (K9) | Resolved |
| F9 | minor | Labels and sentences that disagreed | Corrected in `designs.py` and docs/30 | Resolved |
| F10 | minor | Overfill setting, flow between lines and the way a gradient row steps the flow are unverified | docs/27 §9 items 9–11; docs/30 §8 question 4 | Adopted |
| — | note | Is a fritted capillary a "fitting"? Then the tier-2 design would be a tier-1 design | Put to the user (docs/30 §8 question 6) | Open (user) |
| — | note | A pre-electrolysis electrode in the substrate line attacks the substrate background | Runner-up in docs/30 §5.4; it matters only if the background does not decay | Noted |

## 4. Round 2 (Revision B): findings and resolution

### 4.1 Numbers and physics (M)

| # | Severity | Finding | What was done | Status |
|---|---|---|---|---|
| M1 | significant | Tier 1 subtracts windows in wash buffer (pH 7.5) from a read in substrate buffer (pH 9.5). The difference in background current between the two buffers is not counted; with the 3 % residual of the pre-run it equals the whole blank SD at 168 pA (Derived) | The reference liquid is now the substrate buffer without substrate, on pump line A2, so that the windows differ from the read only by the substrate. The unmatched case is in the kit (`read.buffer_step_A`): a step of 100 pA gives 4.9, 300 pA gives 11 against 3.6. Whether A2 reaches the cell in time depends on the internal volume of pump A (docs/27 §9 item 12); the fallback is in docs/30 §3.1 | Resolved by design; pump volume Open |
| M2 | significant | The 600 s half-life of hydroquinone acts on the product in the bed but not on the substrate reservoir, which is the same solution. Applied to both, the free hydroquinone that "limits tier 1" is gone (9.4 → 5.8) | One stability for the whole path (`_free_product`, `tr.detection.reservoir_background_decays` = 1): the lot's free hydroquinone decays over the reservoir age and the hydrolysis product stands at its steady state. The assumption of Revision B and of the audited model is kept as the scenario "the substrate's background does not decay" in every table (5.9, 2.2, 1.3, 1.3). Question 2 of docs/30 §2.6 measures it. The dip that the closed loop of tier 3 leaves in the baseline is not modelled (README) | Resolved; value UNVERIFIED |
| M3 | significant | At the model's own site density the read bed of the transfer receives 1.7×10¹¹ capture antibodies on 2.1×10¹¹ sites: re-capture 0.83, not 0.95; 0.36 if bed 1 is coated at the vendor's capacity | The kit computes the re-capture with site depletion (Bohart–Adams; reproduces the reviewer's simulation: 0.83 and 0.36). The read bed has three times the beads and bed 1 is coated at a third of the vendor's capacity, which gives a re-capture above 0.99. The two cases of the reviewer are rows of docs/30 §5.4 (0.65 and 1.5 at a release of 0.7) | Resolved |
| M4 | minor | Tier 3: the steady currents of conjugate on the electrode and the inlet bore were counted nowhere | `read.count_steady`: they enter the background, so that their noise counts while the baseline removes their mean | Resolved |
| M5 | minor | The tanks-in-series elution used 0.01 tanks; product made while the bed is swept was omitted | Laminar tail from the transit volume (0.6 µL tier 2, 4 µL tier 3: 7 % of the plug outside the window); the product made during the sweep is counted in signal and blank | Resolved |
| M6 | minor | Product of the bore wall enters the gap along the lid and is collected at about 0, not at the stream's conversion | Stated as an upper estimate (docs/30 §3.4, README); no change to the kit | Resolved by statement |
| M7 | minor | Tier 2: the uncounted terms (electrode's own conjugate, product lost to the electrode during the stop, the smaller volume below the tip) net to under ±5 % | The baseline is the last 30 s of the stop, which removes the electrode's steady current; 0.5 µL below the tip in the kit; the rest under Limits in the README | Resolved |
| M8 | minor | The reservoir age (4 h) is fixed although its parameter has bounds; hydrolysis grows between pre-run and read | docs/30 §2.2 states the age window (1–8 h). With M2 the hydrolysis product is at its steady state after about an hour, so the age no longer acts at nominal. Listed among the inputs that are not sampled | Bounded |
| M9 | minor | Geometry that the text calls uncertain is not sampled, so the 5–95 % ranges are narrower than the text's own uncertainty | Said in the header of docs/30 and listed in its §6.4 with the cases that show each effect | Resolved by statement |
| M10 | minor | Two rows of §4.5 had P(≤ 1) of two cases under a P(≤ 1)/P(≤ 10) header; the wording on the earlier design was loose | The tables are generated, one case per row. The wording follows the output of `earlier_designs_halflife.py` | Resolved |

### 4.2 Resolution, feasibility, consistency (K)

| # | Severity | Finding | What was done | Status |
|---|---|---|---|---|
| K1 | significant | docs/31 did not exist although docs/30 cited it about 20 times | This document | Resolved |
| K2 | significant | The push of the transfer followed a 50 → 2 µL/min step with both beds in line: the relaxing volume carries the eluate through bed 2 at a far higher flow (re-capture 0.19 at 30 µL/min) | The last minute of the hold is at the push flow with both valves in bypass; then the valves switch. docs/27 §2 corrected. With the 40 µm restrictor the stored volume is also smaller | Resolved |
| K3 | significant | The fixed current ranges clip within the calibration (600 pA: tier 1 above 290 pg/mL; 6 nA: tier 2 above about 100 pg/mL), and the 1 µM hydroquinone plug overloads its range 60-fold | One range per determination: 6 nA (tier 1 to about 2000 pg/mL; peaks of tiers 2 and 3 to about 100 pg/mL), 60 nA for standards above that. The check plug is 10 nM | Resolved |
| K4 | significant | Tier 3 had no bench preparation, no Gamry column and no potential; tier 1 no potential (docs/26 §5) | Added: docs/30 §2.3 (potential and its rule), §3.3, §5.2 and §5.3 (Gamry columns, bench preparation) | Resolved |
| K5 | significant | Tier 2 also exceeds 60 min if the sampler needs 2 min per line | Tier 2 now takes 56.7 min; docs/30 §2.3 gives every total at 2 min per line (59.2, 58.7, 58.7; transfer 61.2) | Resolved |
| K6 | significant | Tier 3: whether the eluent fills bed 1, when Loop Offline is set and whether 8 µL reach bed 2 were not defined | V1 is switched by volume after the Inject Start mark of the eluent line; Loop Offline after 200 µL of the hold; the volume between the beds must be at most a third of the push (valve passage volume UNVERIFIED). docs/30 §5.3 | Resolved; valve volume Open |
| K7 | significant | C8 was presented as handled, but the release kept a nominal at the reviewer's upper bound | Release 0.35 [0.05–0.74]. One valve without transfer is the tier-3 design; the transfer is described, computed and conditional on T3-3. docs/30 §5.4 gives the release above which it pays (about 30 %) | Resolved |
| K8 | significant | The numbers for the earlier design, and one current, had no source in the repository | `scripts/tier_round/earlier_designs_halflife.py` and its output; the current is marked Derived | Resolved |
| K9 | minor | 0.1 µL in the kit against 0.5 µL in the text; the stop was not in the integration window | 0.5 µL in the kit; docs/30 §4.1 defines the window and its baseline; the product that reaches the electrode during the stop (at most 5 %) is named in the README | Resolved |
| K10 | minor | Round-1 findings only partly carried: N11 bound, N12, C2 factor, C4 certificate, C6 magnet, C5 sulfite, F5 | All carried: see their rows in section 3 | Resolved |
| K11 | minor | The tier-2 pre-run ended in substrate, so substrate followed the sample through the bed | Every pre-run ends with 300 µL of wash buffer | Resolved |
| K12 | minor | S1 and S4a were called the kill conditions of docs/05 §5; they are the scenarios of its §3, and the kill rule is the G1 rule | Corrected (docs/30 §6.3) | Resolved |
| K13 | minor | The sensitivity table selected loosely; one comparison held only at nominal | The table is generated: every parameter among the eight largest swings of any design, with its value in all four | Resolved |
| K14 | minor | docs/27: one wrong pointer, one wrong citation, a cell test below the design flow | Corrected; the cell is tested at 250 µL/min | Resolved |
| — | language | Ten places a new reader could not follow (codes without definition, an ambiguous sentence, a waiting time that did not match its table) | Terms and codes are defined at the top of docs/30; the sentences are rewritten | Resolved |

### 4.3 Changes after round 2 that no reviewer asked for

With the kit of round 2 the orchestrator looked again at the operating points and moved them. These choices were
not reviewed.

| Change | Why | Effect (nominal) |
|---|---|---|
| Tier 1: read 60 s at 200 µL/min instead of 120 s at 150 µL/min; conjugate 20 nM instead of 10 nM; load 44 min | With the substrate background gone (M2) the tier is limited by drift and by its own signal: a shorter span between the reference windows and more label help | 5.7 → 3.6 (5.9 if the background does not decay) |
| Tier 2: conjugate 5 nM instead of 10 nM; stop 5 min instead of 7 | The tier is limited by the conjugate count, so less conjugate costs nothing; the lowest nominal (3 nM, 3 min: 2.0) was not taken because it leaves less current if the product is only partly electroactive (27 against 13 pg/mL at 1 %) | 2.4 → 2.1 |
| Tier 3, one valve: conjugate 5 nM, accumulation 3 min, load 40 min | The same reasoning; a short accumulation keeps the calibration to 270 pg/mL | 1.5 → 1.2 |
| Restrictor: the Waters 40 µm kit for all tiers | A known part; little liquid stored upstream; tier 1 needs it at 200 µL/min | none in the model |

## 5. Where the changes in the numbers come from

Round 1, reviewers' own runs of the first kit, one change at a time (nominal LOD, pg/mL; from their reports):

| Change | Tier 1 (3.1) | Tier 2 (0.75) | Tier 3 with transfer (0.33) |
|---|---|---|---|
| reference window 55 min away (N1) | 17–69 | — | — |
| bore wall, then the transfer line (N2) | 6.7; 30–59 | — | — |
| drift exponent 0.5 instead of 1 (N7) | 7.7 | — | — |
| walls above the bed (N3) | — | 1.3–3.0 | — |
| baseline residual 5 % instead of 1 % (N4) | — | 0.89 | 1.1 |
| packed-bed factor 3 instead of 1 (N5) | — | 1.25 | 0.40 |
| frit 20 mm² instead of 5 mm² (N12) | — | 2.3 | — |
| transfer 0.49 instead of 0.7 (N6) | — | — | 0.47 |

What the revisions did:
* **Tier 1** was redesigned twice. As first written it would have been 30–75 pg/mL. Revision B read at a fast
  constant flow between buffer windows (9.4, limited by the substrate's free hydroquinone). Revision C treats the
  hydroquinone of the reservoir like that of the product (5.7 at the same operating point), matches the reference
  buffer, and shortens the read (3.6). If the background does not decay it is 5.9.
* **Tier 2** kept its design and took the new blank terms (0.75 → 2.6). In Revision C the consistent half-life,
  the product made during the sweep and the lower conjugate dose bring it to 2.1. Its blank is still 45 % upstream
  walls and 21 % frit.
* **Tier 3** became the tier-2 bed in the loop of one valve (1.2). The transfer went from "0.33" to "1.1 at a
  release nobody has measured; 0.53 if 70 % is released in 5 min".

## 6. Findings that reach beyond this round

These concern the earlier designs (docs/05, docs/13) and the bench plan (docs/06) as much as the three tiers.
Nothing in docs/00–25 or `params/` was edited; the user decides what enters the plan.

1. **C1, the product of hydroquinone diphosphate.** docs/01–05 and the model count one hydroquinone (two
   electrons) per enzyme turnover. The earlier designs read the product of beads in a small volume after 5–7 min,
   like tier 2, so the same ratio of 10⁻⁴–10⁻³ applies. The test of docs/30 §2.6 fits before E1.2 (free
   hydroquinone of the lot) and uses the same materials. Until it is done, every predicted LOD of the project
   carries this condition.
2. **C5 and M2, the life of hydroquinone at pH 9.5.** With 600 s instead of 7200 s for the product, the earlier
   designs hardly move (audited model, n = 2000, same seed; `results/tier_round/earlier_designs_halflife.md`):
   primary of docs/05 nominal 0.60 → 0.62, median 3.49 → 3.46, P(success) 0.156 → 0.154; packed micro-bed backup
   nominal 0.85 → 0.99, median 3.4 → 3.9, P 0.085 → 0.062. The audited model, like Revision B, keeps the
   substrate's free hydroquinone in the reservoir at 10⁻⁵ whatever the half-life. If the half-life is short, that
   background is smaller than the model assumes, and its lever L7 (a purer substrate lot) and the pre-electrolysis
   test E1.2b lose their purpose. E1.2 can settle it by measuring the working solution over its age.
3. **C4, bovine IgG.** The detection conjugate of docs/07 §1 is the one the reviewer found not to be adsorbed
   against bovine proteins, and the bead stock is the same. E1.4 (bovine-IgG cross-reaction) covers it; a
   bovine-adsorbed conjugate should be looked for before the Stage 1 order.
4. **F1, Loop Offline**, was already finding W4 of docs/08 for the earlier design. The measured volume of a
   composition step (docs/27 §9 item 9) serves both.
5. **C9 and C11.** Tris at pH 9.5 buffers weakly, and the substrate has no specification (already an open item in
   docs/07 §6).

## 7. What is still open

Bench, in the order of docs/30 §7:
1. What the enzyme makes and at what potential it is oxidised (C1); how long hydroquinone lives at pH 9.5 and
   what the working substrate solution carries over its age (C5, M2).
2. Instrument facts: zero-flow row, steady flow at 2–5 µL/min against the restrictor, Loop Offline and the volume
   of a composition step, the volume that passes after a flow step, the internal volume of pump A, time between
   sampler lines, overfill, cell gap, bore length and pressure (docs/27 §9).
3. Tier 1: hydroquinone oxidation through the monolayer (C2); drift between the reference windows (N1); build-up
   of conjugate on the transfer line (N2); whether the pre-run harms the capture layer.
4. Tier 2: conjugate on walls and frit against conjugate on the beads (N3, N5, N12); the baseline during the stop
   (N4); the bed under the add-on's magnets (C6); bed-to-bed spread.
5. Tier 3: conjugate on the loop of the valve; then, for the transfer, whether a release in 5 min exists, the
   capacity of the read bed, the leak from bed 1, the passage volume of the valve (C8, F4, M3, K6).
6. Reagents: a bovine-adsorbed detection conjugate (C4); thiols with part numbers (C2); a fritted capillary and a
   sleeve that fits the port (C10); the substrate's certificate (C11).

Not in the model, by decision: build-up from run to run; the product diffusion coefficient, the reservoir age and
the unpublished geometry as sampled quantities; the dip of the tier-3 baseline; the site density of an anti-hapten
bed (README, Limits).

Software: the Gamry backend and the pre-run subtraction in `automation/` (F7).

For the user: the questions of docs/30 §8.
