# 31 — Independent review of the three implementations, and resolution of the findings

Status: 2026-11-17. Written by the orchestrator. Section 1 says how the review was made, section 2 gives its
result in short, section 3 lists every finding with what was done about it, section 4 says where the change in the
predicted LODs comes from, section 5 lists the findings that reach beyond this round, section 6 reports the second
pass on the revised documents, section 7 lists what is still open.

Evidence labels as in the reviewer reports: **[V]** opened by the reviewer in the session, **[V-abs]** abstract read,
**[S]** search summary only, **Derived** (calculation named), **UNVERIFIED**.

## 1. How the review was made

Three independent reviewers (agent tasks with no part in writing the designs) each read the first version of
docs/30 (commit 7bff783) with docs/26–29, the calculation kit and its outputs, through one lens:

| Reviewer | Lens | Report | Own calculation |
|---|---|---|---|
| Numbers | every number re-derived without the kit; physics of the kit; Monte Carlo wiring | `results/tier_round/review_numbers.md` (N1–N13) | `scripts/tier_round/review_numbers.py` |
| Chemistry | reagents and vendor pages re-opened; surface, substrate and label chemistry; bench realism | `results/tier_round/review_chemistry.md` (C1–C12) | `scripts/tier_round/review_chemistry_calc.py` |
| Feasibility | Waters, Gamry and MicruX constraints; docs/26 constraints; consistency; tier 3 | `results/tier_round/review_feasibility.md` (F1–F10) | `scripts/tier_round/review_feasibility_calc.py` |

The reports are kept as written. Their section numbers and values refer to the first version of docs/30
(tier 1 on a thin-film gold chip read at 1 µL/min: nominal 3.1 pg/mL; tier 2: 0.75; tier 3: 0.33).

The orchestrator then changed the kit and the designs, re-ran every number and rewrote docs/30 and docs/27 as
Revision B. Two further reviewers checked Revision B (section 6).

## 2. Result in short

* **The numbers of the first version were faithful to the kit** (36 of 36 checks; outputs reproduced byte for byte;
  the numbers reviewer's independent chains agreed within 1 %). **The kit left out physics that sets the blank**, one
  step of every method could not work as written, and one assumption of the chemistry is open.
* Four findings were rated blocking: the tier-1 read had no reference window near it (N1) and ignored the
  conjugate on the walls upstream of the electrode (N2); no step table set Loop Offline, so the substrate would
  not have reached the cell (F1); and at picomolar enzyme the product of hydroquinone diphosphate should be the
  monophosphate, not hydroquinone (C1, blocking until tested).
* N1, N2 and F1 are resolved in Revision B. C1 cannot be resolved on paper. It is the first bench experiment, and it
  concerns every design of this project, not only this round (section 5).

| Tier | First version: nominal; median | Reviewers' corrected nominal | Revision B: nominal; median [5–95 %] | P(LOD ≤ 1 pg/mL) |
|---|---|---|---|---|
| 1 | 3.1; 16 | 30–75 as written, about 7 if redesigned | TIER1_ROW | TIER1_P |
| 2 | 0.75; 3.0 | 1.3–3.2 | TIER2_ROW | TIER2_P |
| 3 | 0.33; 1.4 | 0.5–1.6 | TIER3_ROW | TIER3_P |

The order tier 3 < tier 2 < tier 1 survived every change. The claim of the first version that tier 3 is better
than the earlier design of docs/05 did not (F5).

## 3. Findings and resolution

Status words: **Resolved** = design or kit changed and the numbers re-run. **Bounded** = carried as a parameter
range or a scenario; a named bench experiment decides. **Open** = stated in docs/30; needs a measurement or a
vendor answer. **Not adopted** = with the reason.

### 3.1 Numbers and physics (N)

| # | Severity | Finding | What was done | Status |
|---|---|---|---|---|
| N1 | blocking | Tier 1's only reference was the read made on the chip before the sample, 55 min before the read. The kit's drift term assumed a reference window next to the read. From this term alone the LOD is 17–69 pg/mL (reviewer, Derived) | The read is now buffer → substrate → buffer at one constant flow: two reference windows 5.4 min apart bracket the read. The kit takes the time between them (`read.t_span_s`) for the drift. The pre-run sequence on the fresh strip is used only for the substrate's own background, and what that subtraction leaves is a parameter (N11) | Resolved |
| N2 | blocking | Conjugate on the inlet bore and the transfer line was not counted, though its product flows onto the electrode (bore 6.7, line 30–59 pg/mL as written; reviewer, Derived). The line also collects conjugate from run to run | `evaluate_planar` counts both walls (`design["upstream"]`), collected at the conversion of the stream. The design reads at 150 µL/min, where that conversion is 7.4 % while the electrode's own enzyme is still collected in full, and uses a 0.05 mm × 15 cm line (24 mm² instead of 80 mm²). Loop Offline is set before the substrate. Build-up on the line from run to run is not modelled; the line is flushed or replaced (docs/30 §3.6) | Resolved; build-up Open |
| N3 | significant | Tier 2: walls above the bed that saw conjugate stand in substrate during the stop; their product follows the plug into the read window (LOD ×1.7 to ×4; reviewer, Derived) | `evaluate_bed` counts the capillary above the bed and the transfer line in full (`bed["upstream_area"]`). Nominal share of the blank: 45 %. The bound "no such wall" is run (1.4 pg/mL) and is what a valve gives (tier 3). T2-1 measures an empty capillary against a bed | Resolved |
| N4 | significant | Tier 2: the baseline of the swept read is a step, not a constant. The electrode empties its layer of free hydroquinone during the stop, and the sweep brings 100 pA back while the peak passes | The pre-run of tier 2 is now the identical substrate step, stop and sweep on the fresh bed and strip; its trace is subtracted. What is left of the step is `tr.noise.swept_step_residual_cv` = 4 % [1–10 %] of the impurity charge (UNVERIFIED). In tier 3 the cell stays in flowing substrate during the accumulation, so there is no step. T2-2 measures the step | Resolved (tier 3), Bounded (tier 2) |
| N5 | significant | The bed was given the surface factor of beads washed in tubes (1), not the model's packed-bed factor (3 [1–30]) | Packed-bed factor used. Factor 1 is run as a case (2.0 pg/mL) | Resolved |
| N6 | significant | Tier 3: a transfer efficiency of 0.7 needs complete release, because re-capture on the second bed at 5 µL/min is itself only 0.70 | Transfer = released fraction (parameter, 0.7 [0.2–0.95], UNVERIFIED) × re-capture from the bed equation at the push flow, now 2 µL/min (0.95). See also C8, F4 | Resolved as a model; the release is Open |
| N7 | significant | The most favourable scaling of drift with electrode area (exponent 1) was the nominal and the mode | `tr.noise.drift_area_exponent` 0.5 [0–1]. The tier-1 primary moved to a 3 mm electrode, which is the model's reference area, so the exponent no longer enters its nominal | Resolved |
| N8 | significant | Tier 2's "upper limit 460 pg/mL" belonged to a different design (a 30 s stop on a fresh bed) | docs/30 §2.4 reports the upper limit by the slope criterion (32 pg/mL) and the concentration up to which the curve rises (10⁵), says that the two-decade requirement is met only as a curved calibration, and names the 30 s stop as a separate determination | Resolved |
| N9 | minor | The wall-jet mapping is exact only for lubrication flow; the check R1 compares two forms of the same assumption; the stagnation disc is dropped (tier 1 conservative by 0–30 % in the thin-film cell) | Stated in the README (Limits). The primary cells now have a 3 mm electrode under a 0.8 mm bore, where the disc is 7 % of the area | Resolved by statement |
| N10 | minor | The rule for product formed on the lid overcounts | Stated as an upper estimate in the README; effect < 10 % | Resolved by statement |
| N11 | minor | 1 % residual for a background read 55 min earlier is optimistic; 3 % [1–10 %] proposed | `tr.noise.preread_residual_cv` 3 % [1–10 %], applied to the substrate background of tier 1 (`read.reference_far`). It is now the largest variance term of tier 1 | Resolved |
| N12 | minor | Optimistic or unstated defaults: frit area, unit-to-unit CVs, gap, bore length; the product diffusion coefficient and the reservoir age are not sampled | Frit 1, 5 and 20 mm² are run (2.1, 2.6, 4.3); the gap cases are run; the CVs are sampled over their ranges. The diffusion coefficient (nominal inside the kernels) and the reservoir age (4 h) stay fixed and are named in the README | Bounded; two items Not adopted (small effect) |
| N13 | minor | Eight text slips | All corrected in Revision B: 750 turnovers per second; the exceptions to the tier order are listed (docs/30 §6.3); the large sensitivities are in §6.2; the stop-and-go numbers are gone; captured fractions are "of the vial"; the valve-only case is computed; the upper limits are reported; printed carbon runs with its own site factor (0.3) | Resolved |

### 3.2 Chemistry and bench realism (C)

| # | Severity | Finding | What was done | Status |
|---|---|---|---|---|
| C1 | blocking until tested | Alkaline phosphatase removes one phosphate per turnover. From the diphosphate it makes the monophosphate, which is hydrolysed again only in competition with a thousandfold excess of diphosphate: hydroquinone/monophosphate ≈ 10⁻⁴–10⁻³ after the tier-2 stop, 3×10⁻⁶ in tier 1 (Derived). No paper found addresses it (Wilson2004 used a dense enzyme layer, Bekhit2021 exhaustive coulometry [V-abs]). If the monophosphate is not oxidised at the read potential, all signals are 10²–10⁵ too high | docs/30 §2.5 states the question, the three possible outcomes and the half-day test (voltammetry of 1–10 pM conjugate in 1 mM substrate against a hydroquinone standard; HPLC-UV on the I-Class). The read potential is to be set on enzyme-generated product. Alternatives named: p-hydroxyphenyl phosphate (supplier not found, docs/07 §6), ascorbic acid 2-phosphate. The kit carries the scenario "1 % of turnovers electroactive" (890, 36, 37 pg/mL) | **Open: first bench experiment** |
| C2 | significant | Tier 1 assumes hydroquinone is oxidised through a thiol monolayer and a protein layer without penalty; common biotin-OEG thiols have a C11 chain; gold in chloride allows only −0.3 to +0.6 V | Short-chain thiols specified as a class (C2–C6; part numbers UNVERIFIED). The reviewer's pass criterion is in T1-1 (half-wave ≤ +0.25 V, plateau ≥ 70 % of bare gold). A collection efficiency of the coated electrode is now a kit parameter (MONO_PARAM). Printed carbon without a monolayer is the fallback and is run | Bounded |
| C3 | significant | The thiol and protein coat also covered the chip's gold pseudo-reference, which carries the drift | The primary electrode is now the printed gold strip, whose printed silver reference stands apart; the 2–3 µL drop covers the working electrode only. Reference stability is checked (docs/27 §9 item 8, T1-1) | Resolved by design |
| C4 | significant | The detection conjugate 109-056-006 is not adsorbed against bovine proteins and is stabilised with BSA [V]; the M-280 stock contains 0.1 % ordinary BSA [V] | Stated in the reagent table (docs/30 §2.1). Beads are washed and re-blocked in IgG-free BSA. T2-1 compares beads as supplied with re-blocked beads. A bovine-adsorbed conjugate is to be found (part number UNVERIFIED) | Bounded; reagent Open |
| C5 | significant | Hydroquinone half-life at pH 9.5 is about 7 min by extrapolation of half-lives at pH 7–9 ([S], compilation quoting Moussavi 1979; primary source not opened), not the model's 2 h | This round uses 600 s [120–7200] (`run_tiers.base_params`; `params/` not edited). Standards are kept at pH 7. T2-2 measures the loss over 0–12 min, with and without sulfite (Bekhit2021). Effect on the earlier designs: section 5 | Resolved for this round; value UNVERIFIED |
| C6 | significant | The add-on is clamped by magnets a few millimetres from a bed of magnetic beads; proposal: hold the bed with a magnet and drop the frit | The check of the bed with the add-on in place is in docs/30 §4.2 and T2-3; non-magnetic particles are the fallback. **The magnet-held bed is not adopted.** A plug that fills the bore carries the whole pressure drop: 25 bar × 0.031 mm² on 10⁶ beads is 78 nN per bead at 80 µL/min and 3.3 nN at the loading flow, against 0.02–0.2 nN of magnetic force per bead (Derived: 2×10⁻¹³ A·m² per bead at saturation, gradient 100–1000 T/m; UNVERIFIED order of magnitude). The feasibility reviewer reached the same result | Bounded; proposal Not adopted |
| C7 | significant | Tier 2 reused the strip, but every determination passes conjugate over it, and blanks on one strip are not independent | A fresh strip with every bed (docs/30 §4.1, §2.4) | Resolved |
| C8 | significant | A 5 min release of desthiobiotin by biotin is unsupported: 0.3–26 % from the affinity (Derived; K_d UNVERIFIED), "too slow" in Ying, Branchaud and Corry 2011 [V]; and the read bed has to take all released capture antibody, not only the complexes | Desthiobiotin is no longer the primary route; it is run as a case (4.3 nominal, worse than no transfer). The primary is a cleavable link with a hapten tag for the read bed; every part of it is UNVERIFIED and the release is a bounded parameter. The capacity condition is stated in docs/30 §5.1 with its remedies and is not in the model. T3-1 measures release, re-capture with the full antibody load and the leak from bed 1 | Bounded; chemistry and capacity Open |
| C9 | minor | 0.1 M Tris buffers weakly at pH 9.5 (8 mM per pH unit, Derived); the turnover number is not tied to the buffer | The product test compares Tris with 1 M diethanolamine pH 9.8 (docs/30 §2.2, §2.5) | Adopted |
| C10 | minor | Buildability of the capillary bed: sleeve fit, frit pore size unknown, bed compacts at the first fast flush | Pre-compaction at 80 µL/min and a mechanical stop for the tip are in docs/30 §4.2; the sleeve is cited as a class of part [S]. A tapered tip without a frit is a further option if T2-1 shows the frit dominates (UNVERIFIED for 2.8 µm beads) | Adopted |
| C11 | minor | No purity, free-hydroquinone or monophosphate specification on the substrate | Stated in docs/30 §2.1; the HPLC-UV run of the product test measures both; a certificate of analysis is to be asked for (docs/07 §6 already lists it) | Adopted |
| C12 | minor | A surface factor below 1 for the coated gold has no support | Low bound set to 1 (3 [1–30]) | Resolved |

### 3.3 Feasibility, constraints, consistency (F)

| # | Severity | Finding | What was done | Status |
|---|---|---|---|---|
| F1 | blocking | No table set Loop Offline. With the 100 µL loop in line the programmed 100–160 µL of substrate does not reach the cell; with the loop offline it reaches 52–82 % | Loop Offline is in every step table, after two loop volumes have followed the reagent and before the step to substrate. A composition step is 215 µL (95 %; Derived by the reviewer). docs/27 §1 and §9 item 9 (dye test). All three timings were rebuilt | Resolved; volumes to be measured |
| F2 | significant | Pressure relaxation was computed for 1000 psi, but the stops start from 5000–8100 psi: 6.4–10.2 µL creep through the bed, 60–100 times the product plug; the real compliance is unknown | Step-down rule: 1 min at 5 µL/min before the stop (tier 2). Tier 1 has no flow step between its reference windows and its read. In tier 3 the relaxing flow passes through the bypass. docs/27 §2 corrected; §9 item 10 measures the creep | Resolved by rule; compliance Open |
| F3 | significant | Tier 3 did not fit 58 min as described, and its "hold" was not a hold with the valve open | Step table rebuilt from flows and volumes: bed 1 is closed by its valve for the hold; load 25 min at 5.0 µL/min; 58.2 min. Three sampler lines at 1 min each (UNVERIFIED, 0.25–2 min) leave 1.8 min; the inter-line time is measured before tier 3 is committed (T3-3) | Resolved |
| F4 | significant | The transfer efficiency 0.7 [0.4–0.9] cannot be reached with one pass at 5 µL/min; capture antibody also leaks from bed 1 during the 40 min before the release | As N6. The leak arm is in T3-1 | Resolved as a model |
| F5 | significant | The comparison with the docs/05 design was unfair: its row with the transfer (nominal 0.29, median 1.5, P 0.33) was not quoted, the P values use different criteria, and the models differ | docs/30 §0 and §5.5 quote both rows, state that the two sets of numbers are not on the same footing and that neither design is shown to be better. The sentence "gains no LOD from a chamber" is gone. The docs/05 design was not run through the kit: the kit has no chamber or trap format (the bed format agrees with the model to 10⁻⁹ on the overlapping case) | Resolved by statement |
| F6 | significant | "Valves only: an electrode that never sees conjugate" contradicted the geometry | Claim dropped. The one-valve case is modelled with its loop walls (10 mm²), a wider dispersion and the cell in flow; docs/30 §5.1 says that the cell sees the conjugate and the eluate | Resolved |
| F7 | significant | Current range, potential hold and the signal routine were not specified; the Gamry backend of `automation/` is a stub and its signal routine cannot subtract a pre-run | One fixed range per tier (600 pA; 6 nA) and the missing software are stated in docs/30 §2.3. No code was written: `automation/` is outside this round | Stated; software Open |
| F8 | minor | 0.5 µL, not 0.1 µL, lie between the capillary tip and the electrode, with 2.5 mm² of conjugate-exposed bore wall | The wall is counted (`bore_below_tip_mm`); docs/30 §4.1 states 0.5 µL | Resolved |
| F9 | minor | Labels and sentences that disagreed (step label, "thin gap" given as verified, the reason for the 0.2 mm gap, bed length, strip reuse) | Corrected in `designs.py` and docs/30 | Resolved |
| F10 | minor | Overfill setting, flow between lines and the way a gradient row steps the flow are unverified | docs/27 §9 items 9–11; docs/30 §8 question 4 | Adopted |
| — | note | Is a fritted capillary a "fitting"? Then the tier-2 design would be a tier-1 design | Put to the user (docs/30 §8 question 6) | Open (user) |
| — | note | A pre-electrolysis electrode in the substrate line attacks tier 3's substrate background | Listed as a runner-up in docs/30 §5.3; the project's bench test E1.2b decides | Noted |

## 4. Where the change in the numbers comes from

Reviewers' own runs of the first kit, one change at a time (nominal LOD, pg/mL; from their reports, Derived):

| Change | Tier 1 (3.1) | Tier 2 (0.75) | Tier 3 (0.33) |
|---|---|---|---|
| reference window 55 min away (N1) | 17–69 | — | — |
| bore wall, then the transfer line (N2) | 6.7; 30–59 | — | — |
| drift exponent 0.5 instead of 1 (N7) | 7.7 | — | — |
| walls above the bed (N3) | — | 1.3–3.0 | — |
| baseline residual 5 % instead of 1 % (N4) | — | 0.89 | 1.1 |
| packed-bed factor 3 instead of 1 (N5) | — | 1.25 | 0.40 |
| frit 20 mm² instead of 5 mm² (N12) | — | 2.3 | — |
| transfer 0.49 instead of 0.7 (N6) | — | — | 0.47 |

What Revision B did with them:
* **Tier 1** was redesigned rather than corrected. As written it would have been 30–75 pg/mL. The fast constant flow
  takes the upstream walls down to 1.4 pg/mL of blank equivalent and brings the reference windows next to the read.
  The price is the substrate's own hydroquinone: 107 pA to be subtracted to 3 %.
* **Tier 2** keeps its design and carries the new terms. Of its blank, 45 % now comes from the walls above the bed
  and 21 % from the frit. Without the upstream walls it would be 1.4 pg/mL; with the bead factor of 1 it would be 2.0.
* **Tier 3** was rearranged so that the valves remove what tier 2 suffers from (cell always in flow, bed closed by
  its valve), and its transfer became release × re-capture with a longer protocol (the label waits 19 min).

## 5. Findings that reach beyond this round

These concern the earlier designs (docs/05, docs/13) and the bench plan (docs/06) as much as the three tiers.
Nothing in docs/00–25 or `params/` was edited; the user decides what enters the plan.

1. **C1, the product of hydroquinone diphosphate.** docs/01–05 and the model count one hydroquinone (two
   electrons) per enzyme turnover. The earlier designs read the product of beads in a small volume after 5–7 min,
   like tier 2, so the same ratio of 10⁻⁴–10⁻³ applies. The half-day test of docs/30 §2.5 fits before E1.2 (free
   hydroquinone of the lot) and uses the same materials. Until it is done, every predicted LOD of the project
   carries this condition.
2. **C5, the half-life of hydroquinone at pH 9.5.** With 600 s instead of 7200 s the earlier designs hardly move
   (model re-run, n = 2000, same seed): primary of docs/05 nominal 0.60 → 0.62, median 3.49 → 3.46, P(success)
   0.156 → 0.154; packed micro-bed backup nominal 0.85 → 0.99, median 3.4 → 3.9, P 0.085 → 0.062. E1.2 already
   measures hydroquinone stability; the standards should be made at pH 7.
3. **C4, bovine IgG.** The detection conjugate of docs/07 §1 is the one the reviewer found not to be adsorbed
   against bovine proteins, and the bead stock is the same. E1.4 (bovine-IgG cross-reaction) covers it; a
   bovine-adsorbed conjugate should be looked for before the Stage 1 order.
4. **F1, Loop Offline**, was already finding W4 of docs/08 for the earlier design. The measured volume of a
   composition step (docs/27 §9 item 9) serves both.
5. **C9 and C11.** Tris at pH 9.5 buffers weakly, and the substrate has no specification (already an open item in
   docs/07 §6).

## 6. Second pass on Revision B

SECOND_PASS

## 7. What is still open

Bench, in the order of docs/30 §7:
1. The product of the enzyme reaction and its oxidation potential (C1).
2. Instrument facts: zero-flow row, steady flow at 2–5 µL/min, Loop Offline and the volume of a composition step,
   creep after flow steps, time between sampler lines, overfill, cell gap and bore length (docs/27 §9).
3. Tier 1: hydroquinone oxidation through the monolayer (C2); repeatability of the substrate background on one
   strip over an hour (N11); build-up of conjugate on the transfer line (N2).
4. Tier 2: conjugate on walls and frit against conjugate on the beads (N3, N5, N12); the baseline step (N4); the
   bed under the add-on's magnets (C6); bed-to-bed spread.
5. Tier 3: whether a release in 5 min exists, the capacity of the read bed, the leak from bed 1 (C8, F4).
6. Reagents: a bovine-adsorbed detection conjugate (C4); thiols with part numbers (C2); a fritted capillary and a
   sleeve that fits the port (C10); the substrate's certificate (C11).

Not in the model, by decision: build-up from run to run, the capacity of the read bed, the diffusion coefficient
of the product and the reservoir age as sampled quantities, the steady current of wall-bound conjugate in the
swept read (README, Limits).

Software: the Gamry backend and the pre-run subtraction in `automation/` (F7).

For the user: the questions of docs/30 §8.
