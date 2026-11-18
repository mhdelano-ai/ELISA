# Second-pass review of docs/30 Revision B: resolution of findings, step tables, consistency, sourcing

Reviewer: independent second pass (consistency lens), 2026-11-17. Inputs read: docs/26 §3–5, docs/30 (all),
docs/27 Rev B (§1–6, 8, 9), `scripts/tier_round/README.md`, `designs.py`, `tier_params.yaml`, the relevant parts of
`tierkit.py` and `run_tiers.py`, `results/tier_round/tiers.md` and `tiers.json`, the three first-round reports.
Own script: `scripts/tier_round/review2_consistency.py` (sums the step tables, evaluates the three nominal designs with
the kit without writing any file, prints the Derived currents below). `run_tiers.py` was not run.

## Verdict

Revision B fixes most of what the first round found. N1–N3, N5–N7, N13, F1, F3, F4, F6, F9, C3, C5, C7, C9, C10
and C12 are resolved in text and kit. The step tables add up, and the volumes come from flow × time. Loop Offline
is set before every composition step. Of the 60-plus numbers I compared between docs/30, tiers.md and tiers.json,
all agree. Five problems remain:
(1) docs/31 does not exist. docs/30 points to it about 20 times for the record of findings and what was done.
(2) Tier 3's push follows a 50 → 2 µL/min step with both beds in line. The pressure stored upstream (6–64 µL)
then relaxes through bed 2 just as the eluate arrives. docs/27 §2 says the opposite.
(3) The fixed current ranges adopted from F7 clip inside the calibration range (tier 1 above about 290 pg/mL,
tier 2 above about 100 pg/mL), and the tier-1 hydroquinone check plug overloads its range.
(4) Tier 3 has no bench preparation, no Gamry column and no potential. Tier 1 states no potential. docs/26 §5
asks for all of these.
(5) The comparison numbers for the earlier design (3.49, 0.156; 3.46) have no output anywhere in the repository.
C8 and several chemistry fixes are only partly carried out.

## Findings (most severe first)

### R1 — significant — docs/31, the record of findings and their resolution, does not exist
*Place:* docs/30 l.3, l.13 ("docs/31 §3 lists every finding and what was done") and about 20 citations of the form
"docs/31 N1/C5/F7"; docs/27 l.3, 31, 61, 213, 216, 219; README l.1, 11, 22, 24, 93, 135, 138, 146; designs.py and
run_tiers.py docstrings.
*Evidence:* [V] `ls docs` lists 00–30 only; `git log` shows no docs/31. docs/26 §6 assigns docs/31 to "independent
review and resolution of findings". The finding ids N/C/F live in `results/tier_round/review_*.md`. No table maps each
of the 35 findings to its resolution. The table in this report (below) is the only such mapping.
*Fix:* write docs/31 with §3 as the resolution table, or point every "docs/31 Xn" to `results/tier_round/review_*.md`
and remove the claim at l.13. Mark as open the findings that the table below shows as partly resolved.

### R2 — significant — Tier 3: the push to bed 2 starts with a flow step, so the relaxing pump volume crosses both beds with the eluate
*Place:* docs/30 §5.2 rows 36–41 (A1 50 µL/min) and 41–45 (V1 IN + V2 IN, 2 µL/min); docs/27 §2 last bullet ("tier 3
lets the relaxing flow pass through the valve bypass, not through the closed bed"); `designs.tier3` (`t_down=0.0`).
*Evidence:* with the 25 µm × 45 cm restrictor the pump stands at about 5050 psi at 50 µL/min (docs/27 §3 [V]).
docs/27 §2 gives the stored volume as 6.4 µL for water-only compliance, with a time constant of about 8 s. At ten
times that compliance it is about 64 µL over minutes. The valves switch to IN + IN at the moment the flow drops to
2 µL/min. That surge therefore passes through bed 1 and then bed 2, and it carries the 8 nL eluate within the first
seconds. The kit's own bed equation (README D) gives the re-capture at the flow that actually crosses bed 2.
Derived: at 30 µL/min it is 1 − exp(−k_r·A/Q) = 1 − exp(−4.2×10⁻⁶ · 24.6×10⁻⁶ / 5.0×10⁻¹⁰) = 0.19. The design
takes 0.95 at 2 µL/min. The 8 µL push volume is also not what crosses bed 2. The same step happens in the one-valve
variant only at the accumulation, where it goes through the bypass, so the one-valve core is not affected.
*Fix:* add a row before the push: step down to 2 µL/min with both valves OUT and hold for at least 5 τ, where τ is
measured in docs/27 §9 item 10. Then switch to IN + IN. Count the minutes (40 s at water compliance; minutes at ten
times). The 1.8 min margin may not cover it, so shorten the load if needed. Correct docs/27 §2.

### R3 — significant — The fixed current ranges clip within the calibration range, and the tier-1 check plug overloads its range
*Place:* docs/30 §2.3 (one fixed range per tier: 600 pA tier 1, 6 nA tiers 2 and 3); §2.4 (standards up to
1000 pg/mL; tier 1 "linear to 10⁵"; tiers 2, 3 "rise up to 10⁵"); §3.3 pre-run row (1 µM hydroquinone plug,
"Gamry on from here to the end").
*Evidence:* Derived, `review2_consistency.py`:
* Tier 1: 130 pA background + 1.6 pA per pg/mL (§3.4) exceeds 600 pA above about 290 pg/mL. At 1000 pg/mL it is
  1.7 nA.
* Tier-1 check plug: nFcQη = 2 × 96485 × 10⁻³ mol/m³ × 2.5×10⁻⁹ m³/s × 0.074 = 36 nA on the 600 pA range. That is
  60× full scale, a few minutes before the pre-run read windows. F7 warned about overload recovery.
* Tier 2: the kit's nominal net charge is 152 nC at 93 pg/mL and 586 nC at 794 pg/mL. The plug width is σ = 1 µL at
  5 µL/min, so 12 s. The peak is therefore about 5 nA at 93 pg/mL and about 19 nA at 794 pg/mL, against 6 nA.
* Tier 3: 296 nC at 794 pg/mL with σ = 1.5 µL gives a peak of about 6.6 nA.
*Fix:* state the range the fixed current range allows, per tier. Alternatively, choose the range per calibration
level and change it at a fixed time at least 60 s before the window (the F7 rule). Tier 1 on the 6 nA range
(±10 pA offset, F7) would cover about 3600 pg/mL. Dilute the check plug to ≤ 10 nM (0.36 nA), or run it on its own
range at least 60 s before the first window.

### R4 — significant — Tier 3 lacks the bench preparation, the Gamry column and the potential; tier 1 lacks the potential (docs/26 §5 items 3–4)
*Place:* docs/30 §5.2 (columns Clock, Step, Valves, BSM, SM-FL; no Gamry), §5 (no "bench preparation"
subsection), §3.3 (Gamry column without a potential; §2.3 only says "on the plateau").
*Evidence:* [V] docs/26 §5 item 3 asks for "Gamry technique and potentials" in the step table and item 4 for "bench
preparation before the run". Tier 2 gives +0.30 V vs printed Ag/AgCl (§4.3). Tier 1 gives only the T1-1 pass limit
(half-wave ≤ +0.25 V) and the gold window (+0.6 V). Tier 3 has no prep for the cleavable-link capture F(ab′)₂, the
anti-hapten bed 2, packing two beds or mounting them in valve loops.
*Fix:* add §5.x Bench preparation (one-valve core = §4.2 plus mounting in the loop; transfer reagents as UNVERIFIED
recipe). Add a Gamry column to §5.2 (range, marks at Inject Start of lines 1–3 and at each valve switch, windows).
State the tier-1 potential, or a bounded value with the lot rule.

### R5 — significant — Tier 2 also exceeds 60 min at the upper end of the SM-FL line overhead, and docs/30 says this only for tier 3
*Place:* docs/30 §4.3 (58.7 min), §5.2 last paragraph.
*Evidence:* [V] docs/02 l.210 gives "≈ 1 min per injection (range 0.25–2 min)". Tier 2 has two lines. At 2 min per
line it takes 60.7 min. Tier 1 takes 58.9 and tier 3 61.2 (Derived from the tables). Tier 2 is the recommended
build.
*Fix:* state the tier-2 margin (1.3 min) and its fallback. The 3 min stop (2.5 nominal, §4.5) frees 4 min. Make
docs/27 §9 item 3 a go/no-go for tier 2 as well.

### R6 — significant — Tier 3 rows 34.5–41: whether the eluent fills bed 1, when Loop Offline is set, and whether 8 µL reaches bed 2 are not defined
*Place:* docs/30 §5.2 rows 34.5–36, 36–41, 41–45; `designs.tier3` (`OVERHEAD + 0.5` min).
*Evidence:* Derived: row 34.5–36 gives 1.5 min, of which the line takes 1 min (UNVERIFIED). That leaves 25 µL
behind the loop before V1 goes OUT at 36.0. At an overhead of 1.5 min or more, no eluent reaches bed 1 before the
hold. The SM-FL entry "Loop Offline" in row 36–41 does not say when. If it is set at 36, 75 µL of eluent stay in the
loop until the next determination. If it is set later, they cross the electrode during the hold. §5.1 says the
eluent crosses the electrode, which fits only the second reading. The volume from bed 1 to bed 2 (bed outlet stub,
V1 port 5 → 6, tubing, V2 port 1 → 2) is not stated, so it cannot be checked that the 8 µL push carries the eluate
(dispersed from 8 nL) into bed 2 and not past it.
*Fix:* time V1 OUT from the Inject Start mark of line 3 plus a measured volume, not from the clock. Set Loop Offline
at the end of the hold, after ≥ 2 loop volumes, and say so. State the bed-to-bed volume and require push ≥ 3× it.

### R7 — significant — C8 is presented as handled, but the release fraction keeps a nominal at the reviewer's upper bound and a high bound above it
*Place:* docs/30 §5.1 Transfer row, §5.3; `tier_params.yaml` `tr.transfer.elution_efficiency` 0.7 [0.2–0.95].
*Evidence:* [V] review_chemistry.md C8 Fix: "Bound the transfer as specific × 0.05–0.7 until T3-1 measures it".
Revision B moved the primary route from desthiobiotin to a cleavable disulfide link, for which no rate is known
either (docs/30 §5.1: "UNVERIFIED throughout"). It kept 0.7 nominal and set the range to 0.2–0.95. The capacity
problem of bed 2 is described but not modelled (README F). docs/30 states the uncertainty plainly (pessimistic case
9.0, §5.3). The headline tier-3 figures (0.62; P(≤ 1) 0.15; "about four times lower") still rest on it.
*Fix:* either run the primary with 0.05–0.7, or give the one-valve figure (1.5; 6.9 [0.87–85]) as tier 3's headline
until T3-1, with the transfer as an upside case.

### R8 — significant — Numbers for the earlier design have no source in the repository
*Place:* docs/30 §0 ("reproduced here: 3.49, 0.156"), §5.5 ("Re-run here with the 10 min half-life ... median 3.46").
*Evidence:* [V] no file in `results/tier_round/` or `scripts/tier_round/` contains these values (grep). `run_tiers.py`
docstring: "The earlier valve-and-chamber design of docs/05 is not re-evaluated here". Not in the history of
tiers.md either (`git show` of 5775ce9, 7bff783, d8db228). Similarly "the mean blank peak is about 170 pA" (§4.1) is
in no output.
*Fix:* add the run (script + output file) or remove the numbers and cite docs/08 §10.1 (3.5, P 0.16) only.

### R9 — minor — F8 is half done: the kit keeps 0.1 µL between bed and electrode, and the stop is not integrated
*Place:* docs/30 §4.1 Position row ("0.5 µL of bore"); `designs.tier2(V_dead_uL=0.1)`; §4.3 row 50.2–57.2 (Gamry
"baseline").
*Evidence:* [V] `review2_consistency.py` prints V_dead = 1.0×10⁻¹⁰ m³ for tiers 2 and 3. F8 Fix also asked to
include the stop in the integration window: 6 % of the product reaches the electrode during the stop. The tier-2
table reads only the 90 s sweep and gives no reason.
*Fix:* set `V_dead_uL=0.5` (F8 found 0.75 → 0.81), and either integrate from the stop or state why not.

### R10 — minor — First-round findings that are partly resolved or not mentioned in docs/30
*Place:* see the resolution table.
*Evidence:* N11: nominal 3 % adopted, high bound 6 % instead of the 10 % asked. This term is 61 % of the tier-1 blank
variance, so the upper Monte Carlo tail is understated. N12: open; only README "Limits" says it, and docs/30 §6.4
does not list it. C2: the "monolayer collection efficiency" factor (0.1–1) is not in the kit, so the 9.4 assumes
full rate (docs/30 says so). C4: no conjugate adsorbed against bovine serum was found, and the CoA question on the
BSA stabiliser is not carried. C6: the magnet-held variant (no frit) is neither run nor declined. C5: the sulfite
arm is dropped without a word. F5: the docs/05 design was not run through the kit; it is bounded by text.
*Fix:* carry these in the docs/31 table as "partly/open", and add N12 to docs/30 §6.4.

### R11 — minor — The tier-2 pre-run ends in substrate, so substrate follows the sample through the bed
*Place:* docs/30 §4.3 pre-run row.
*Evidence:* Derived: the pre-run ends with B1 at 5 µL/min, which leaves the 85–110 µL dwell volume (docs/27 §1) full
of B1. At 3.4 µL/min × 38 min = 129 µL, the last 29 µL through the bed before Loop Offline are substrate at pH 9.5.
Tier 3's pre-run says "back to buffer"; tier 2's does not.
*Fix:* end the tier-2 pre-run with ≥ 300 µL of A1 at 50–80 µL/min.

### R12 — minor — §6.3 names the wrong kill conditions
*Place:* docs/30 §6.3 second bullet ("These are the two kill conditions of docs/05 §5").
*Evidence:* [V] docs/05 l.66 and §5 U1: the kill thresholds are a label factor > 0.15 and free HQ 10⁻⁴. S1 (×25) and
S4a (10⁻³) are the robustness scenarios of docs/05 §3 (l.277). Both §5 thresholds were superseded by the G1 rule
(docs/05 §5 "(revised after final review, B3)").
*Fix:* "These are the S1 and S4a scenarios of docs/05 §3; the kill rule is now the G1 rule (docs/06 §4.11)."

### R13 — minor — §6.2 and §6.3 select and summarise loosely
*Place:* docs/30 §6.2, §6.3 first bullet.
*Evidence:* [V] tiers.md §6: the larger swings left out of §6.2 are T1 Km (7.7/29) and enzyme : antibody ratio
(18/5.3), and T3 site density (4.1/0.5) and kon_capture (2.2/0.42). Smaller swings are listed (gold factor 9.0/23,
T3 bed factor 0.50/2.7). §6.3 "tiers 2 and 3 are equal (36, 37)" holds nominally, but the medians are 76 and 150
(tiers.md §2).
*Fix:* list the nine largest per tier as tiers.md does, and give the medians in §6.3.

### R14 — minor — docs/27 Revision B: one wrong pointer, one wrong citation, one check below the design flow
*Place:* docs/27 §4 ("section 8, item 6"), §8 last paragraph, §9 item 5.
*Evidence:* [V] the overfill check is §9 item 6. docs/27 §8 says "washes are fixed at ≥ 1.5 min and ≥ 2 min as in
docs/05 §1.1", but docs/05 §1.1 gives ≥ 1 min and ≥ 2 min (docs/30 §2.3 has it right). §9 item 5 tests the cell to
100 µL/min, while tier 1 runs it at 150 µL/min. docs/28 §1.4 says the PMMA add-on is not rated for pressure.
*Fix:* correct the pointer and the citation, and test the cell at ≥ 150 µL/min.

## 1. Resolution table (35 first-round findings)

R = resolved; B = bounded (stated, carried as a scenario or bench test, not removed); P = partly; O = open. "Not in
docs/30" = docs/30 does not mention it (README or docs/27 may).

| Id | Status | Where in Revision B |
|---|---|---|
| N1 | R | §3.1, §3.3 A–B–A windows 5.4 min apart; kit `t_span` (README I); designs.tier1 |
| N2 | R | upstream bore + 50 µm × 15 cm line counted (§3.4: 1.25×10⁵ enzymes, 1.4 pg/mL); Loop Offline. Run-to-run build-up on the line: B (§3.6, not modelled) |
| N3 | R | `upstream_area` capillary + line counted in full (§4.1: 45 % of the blank) |
| N4 | R/B | pre-run trace subtraction, `swept_step_residual_cv` 4 % [1–10 %] UNVERIFIED; tier 3 cell always in flow |
| N5 | R | packed-bed factor 3 nominal (§4.1; scenario factor 1 = 2.0) |
| N6 | R | release × re-capture at 2 µL/min (0.95); see R2 for the flow step that defeats it |
| N7 | R | `drift_area_exponent` 0.5 [0–1] |
| N8 | R | §2.4: 30 s stop is a separate determination (4.7; 460); 1.1 and 2.2 decades stated |
| N9 | R (text) | README B, Limits; not in docs/30 |
| N10 | R (text) | README "upper estimate"; not in docs/30 |
| N11 | P | 3 % nominal adopted; high bound 6 % not 10 % (R10) |
| N12 | O | README Limits only; **not in docs/30** (R10) |
| N13 | R | 750 s⁻¹; §6.3 exceptions; §6.2 adds kon, hydrolysis; stop-and-go numbers removed; 7.9 % "of the vial"; valve-only screened computed (1.1); tier-1 range stated; carbon uses the adsorbed site factor (17) |
| C1 | B | §2.5 product test first; scenario 1 % (not a sampled factor, as C1 asked) |
| C2 | P | C2–C6 thiol, T1-1 pass on E½ and plateau, carbon fallback; kit factor 0.1–1 not added (R10) |
| C3 | R | printed gold strip with separate silver reference; drop on WE only; docs/27 §9 item 8 |
| C4 | P | bead re-block, T2-1 arm; adsorbed conjugate "to be found", BSA-stabiliser CoA not carried (R10) |
| C5 | R | t½ 600 s [120–7200] (run_tiers); T2-2 hold arm; HQ kept at pH 7. Sulfite arm dropped |
| C6 | P | lens check, non-magnetic fallback; magnet-held variant not addressed (R10) |
| C7 | R | fresh strip with every bed (§4.1) |
| C8 | P | desthiobiotin demoted (scenario 0.1 [0.003–0.26]); cleavable-link release 0.7 [0.2–0.95] above the asked 0.05–0.7; capacity not modelled (R7) |
| C9 | R | DEA arm in the product test (§2.2, §2.5) |
| C10 | R | pre-compaction, mechanical stop, sleeve [S], frit UNVERIFIED |
| C11 | R/B | "no purity specification" stated; HPLC-UV in the product test; vendor CoA not requested |
| C12 | R | gold factor low bound 1; T1-2; desorption-charge check §3.2 |
| F1 | R | Loop Offline in every table before the step to substrate; 215 µL; docs/27 §1, §9 item 9 |
| F2 | R (tier 2) / O (tier 3 push) | step-down rule tier 2; tier 1 no stop; tier 3 push: R2 |
| F3 | R | eluent IN / OUT hold / IN + IN push; table rebuilt; overhead sensitivity stated. Row timing: R6 |
| F4 | R | as N6; T3-1 in beds with a leak arm |
| F5 | B | §5.5 "cannot be set against"; L4 numbers quoted; "gains no LOD" dropped; docstring corrected. Re-run numbers unsourced (R8) |
| F6 | R | one-valve variant counts 10 mm² of loop at full conjugate; electrode sees conjugate and eluent stated |
| F7 | P | fixed ranges named, pre-run subtraction noted as missing in `automation/`; ranges clip (R3) |
| F8 | P | 0.5 µL and bore wall stated; kit V_dead 0.1 µL, stop not integrated (R9) |
| F9 | R | tiers.md §7 labels; gap UNVERIFIED; 215 bead diameters; strip reuse removed |
| F10 | R | docs/27 §9 items 10, 11; docs/30 §8 question 4 |

Claimed resolved but not: N6/F2 for the push (R2), F7 (R3), F8 (R9), C8 (R7). Not mentioned in docs/30 at all: N9,
N10, N12 (README only).

## 2. Step tables

Derived (`review2_consistency.py`): each table's rows are contiguous and end at the stated total (56.9, 58.7, 58.2).
The builders give 56.87, 58.69, 58.19 and the one-valve variant 56.69 (stated 56.7).

| Check | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Sample ≥ 120 µL | 3.0 × 42 = 126 | 3.4 × 37 = 125.8 | 5.0 × 25 = 125 (one valve 3.5 × 36 = 126) |
| Conjugate 2 loop volumes | 50 × 4 = 200 | 50 × 4 = 200 | 50 × 4 = 200 (in 27.5–32.5) |
| Substrate 215 µL | 150 × 1.4 = 210 (1.43 min exact) | 80 × 2.7 = 216 | 80 × 2.7 = 216 |
| Loop Offline before the step, after the reagent | 49.5 (≥ 200 µL behind conjugate); switch 1.5 min before window 1 | 44.5; step at 46.5 | row 36–41 (time unstated, R6); step at 47 |
| Read reference | windows at 51.0–51.5 and 56.4–56.9 + pre-run sequence | pre-run trace (taken about 1 h earlier) | steady baseline in flow + strip response check |
| Hands after Inject Start | none | none | none (valves by Python) |

Tier 1: the substrate passes 51.5–54.9 (510 µL), twice per determination, so "about 1 mL" (§8 item 2) holds.
Tier 2: the step-down (49.2–50.2) precedes the stop as F2 asked. On the pre-run's B1 left in the line, see R11.

Tier 3, traced through the §5.1 valve definition (IN = 1-2, 5-6 through the bed; OUT = 6-1 bypass, bed ends on
the plugged ports 3 and 4):
* Dead-heading: never. Every valve position leaves one open path (IN through the bed, OUT through the bypass).
* Conjugate into the loop of V2: no. V2 is OUT for 27.5–34.5, and bed 2's ends sit on plugged ports. The rotor groove
  that carries conjugate in OUT (6-1) becomes the 5-6 groove downstream of bed 2 in IN, so it is not upstream of
  bed 2. Its product is a steady current during the accumulation (V2 OUT, flowing).
* Eluent fills bed 1 before the hold: only if the line-3 overhead is < 1.5 min (25 µL at 1 min; 0 at ≥ 1.5 min) (R6).
* Eluate to bed 2 within 8 µL: cannot be checked, because the bed-to-bed volume is not given (R6). The flow step at
  41 min sends 6–64 µL of relaxation volume through both beds first (R2).
* Remainder of the eluent: in the loop if Loop Offline is set at 36; otherwise through V1 and V2 bypasses and the
  cell during the hold (R6).
* Cell always in flow: yes (50, 2, 50, 80, 5, 5 µL/min).
* Across the electrode: sample 1–26; conjugate 27.5–34.5 (full plug, via V2 bypass); eluent from about 35.5 to
  41 (and its remainder if the loop stays in line); the not-recaptured eluate and released capture antibody 41–45;
  wash, substrate. The read is at 56.7 (15.7 min after the eluent, as §5.1 states).
* Rows that cannot work as written: 41–45 (R2); 34.5–36 at an overhead ≥ 1.5 min (R6).

## 3. Constraints of docs/26 §3–4 and the six items of §5

| Item | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| One injection ≤ 100 µL | yes (full loop) | yes | yes |
| ≤ 60 min | 56.9 (58.9 at 2 min per line) | 58.7 (**60.7** at 2 min per line, R5) | 58.2 (61.2 at 2 min per line; stated) |
| Sample-only vial | yes | yes | yes |
| No hands after Inject Start | yes | yes | yes |
| No protein through the pump | yes (conjugate, BSA buffer by SM-FL) | yes | yes (eluent by SM-FL) |
| Additions within the tier | strips, thiols, restrictor, 50 µm line: consumables and tubing | fritted capillary, sleeve: passive | valves, Python: allowed |
| §5.1 flow path, consumables | yes | yes | yes (bed-to-bed volume missing, R6) |
| §5.2 electrode, chemistry, buffers | yes | yes | yes (tag chemistry UNVERIFIED) |
| §5.3 step table with Gamry technique and potentials | potential missing (R4) | yes | Gamry column and potential missing (R4) |
| §5.4 bench preparation | yes | yes | **missing** (R4) |
| §5.5 LOD nominal, median, limiting term | yes | yes | yes |
| §5.6 failure and experiments in order | yes | yes | yes |

## 4. Internal consistency (numbers compared)

Agree [V against tiers.md / tiers.json, or Derived]: every row of §0 table, §3.5, §4.5, §5.3, §6.2 against tiers.md
§1–6 (about 120 values). Times 56.9/58.7/58.2/56.7. Capture fractions 7.9/66/55 % (json 0.0794, 0.657, 0.550).
Blank equivalents 14.6/6.0/1.1 (json 14.62, 6.01, 1.14). Upper limits 32/93 (json 31.6, 92.6). Variance shares
§3.4 (61/28/9 %; json 0.606/0.283/0.088), §4.4 (93/4/3 %; json 0.93/0.042/0.027), §5.3 (61/22/12 %; json
0.609/0.218/0.123). Signals 0.19/2.7/0.93 nC (json 1.94e-10, 2.72e-9, 9.31e-10). Enzymes 5.3×10⁴/1.6×10⁴ (json
52 592, 15 666). Label retention 72/67/37 % (json 0.718, 0.673, 0.372). Labelled 36 % (0.357). Cell conversion 62 %
(0.622). Factors of screening 2.1/1.5/2.8. "1.7 times lower" (2.6/1.5). Margins 1.8 min. "28–63 %" (t½ 13.4 min).
Tier-2 blank split 30.7/20.9/3.2/45.1 % from 8.5/5.8/0.9/12.5×10⁴. Wall areas 24 (π·0.05·150), 2.5, 13 mm². Bead
area 24.6 mm², bed 19 nL, 214 bead diameters, 1.54 µL of stock. Capacity 2×10¹¹ (1×10¹⁶ × 0.85 × 24.6 mm²),
8×10¹¹, 6.0–8.4×10¹² biotin sites (650–900 pmol/mg, docs/28 R32). Restrictor 67 psi per µL/min (10 050, 201
psi). Line 22–24 bar at 150 µL/min (Hagen–Poiseuille). k_r = 4.2×10⁻⁶ m/s. Re-capture 0.955 at 2 µL/min. 4.0×10⁵
molecules at 1 pg/mL. Tier-1 signal 6.7×10³ × 750 × 2e = 1.6 pA. The 36 kit checks pass (check_tierkit.md: 36 PASS,
0 FAIL).

Statements of §0, §6.3, §7 and §8 follow from the tables, except: §0 "about four times" holds nominally (3.6, 4.2)
but not for medians (2.7, 2.7); §0 and §5.5 earlier-design numbers (R8); §6.3 kill conditions (R12) and "equal (36,
37)" (R13). docs/27 Rev B and the README carry the new flows, read modes and numbers. The contradictions are docs/27 §2
on the tier-3 relaxation (R2) and the items of R14. No old flows (1 µL/min tier-1 read, 80 µL/min tier-1 front) or
old LODs (0.75, 0.33, 3.1) remain in docs/27 or the README (grep).

## 5. Sourcing

Found where docs/30 points, with the label it gives [V, grep]:
* Jackson 109-066-098 and 109-056-006: docs/07 §1, §7; review_chemistry C4.
* Dynabeads 11205D, R32: docs/28 l.227, 317.
* DRP-HQDP-0.5G: docs/07 §1, §6; docs/29.
* NISTmAb 8671 and normal goat F(ab′)₂: docs/07 §1.
* MXP9900-000 [V]: docs/07 §2, §6, §7.
* IDEX F-385 [S]: review_chemistry C10.
* ED-S1PE-Au10 and -C21: docs/28 §2.1.
* AIO-SPE, magnets, 0.8 mm bore: docs/28 §1.
* Literature: Nishimura (docs/29), Buckey, Das2007, Kwon, Akanda2011a (docs/29 l.24–26, A.2), Akanda2013,
  DiazGonzalez, Squires, Wilson2004, Bekhit, DellaCiana (docs/01, docs/29), Hirsch, Ishikawa, Hashida (docs/05),
  Ying 2011 (review_chemistry C8).
* Ascorbic acid 2-phosphate: docs/01 b.
* Wash minima: docs/05 §1.1. U8, U9 pass rules: docs/05 §5. Phase-2 antibody: docs/06 §4.12. B1: docs/08.
  Scenario C1: docs/08 §10. Line overhead: docs/02 l.210.

Not found, or without source, Derived or UNVERIFIED label:
* the earlier-design re-run (3.49, 0.156, 3.46) and "mean blank peak about 170 pA" (R8);
* "(docs/31 C)" for the vendor pages (should be review_chemistry C4);
* §3.4 "3 pA rms; 5 pA/min" (model values, UNVERIFIED in docs/27 §5, unlabelled here);
* §6.3 kill conditions (wrong pointer, R12).

## 6. Cross-references

docs/30: all docs/26, 27, 28, 29, 05, 06, 07, 08, 01, 02, 03 targets exist and hold the claim, except:
* docs/31 throughout (R1);
* docs/05 §5 in §6.3 (R12);
* docs/28 §4 "window ends at +0.6 V" was stated for thin-film gold in chloride (review_chemistry C2), while tier 1
  uses printed gold (applicability not stated).

docs/27 (spot-check of 12): docs/29 A.4, B.5, B.7, docs/05 §4.0, §4.1, docs/03 §3.6 and docs/02 §1.1, §1.2 hold.
Wrong are §4's "section 8, item 6" and §8's "as in docs/05 §1.1" (R14), and docs/31 (R1).

## 7. Sentences a new reader could not follow (docs/30)

1. §0 table and §3.5/§4.5/§5.3: "L6 + L7", "L3", "L5", "S1", "S4a" are used without definition; they are docs/05
   §2–3 levers and scenarios.
2. §1 item 1 and throughout: "surface factor" is not defined (relative to what anchor: the bead/plate NSB rate).
3. §1 item 1: "it does not depend on the conjugate concentration or on the area" gives no step for why the area
   cancels (both specific and non-specific label scale with area).
4. §2.1: "HQDP" first appears in a table cell without expansion (expanded only in §2.5).
5. §2.1: "bench item U2", §7: "Stage 1A", "E1.1–E1.3", "gate G1a", §5.3: "E1.2b" are project codes without a pointer
   to their definitions (docs/05 §5, docs/06).
6. §3.1 (ii): "they are 5.4 min apart instead of an hour": "they" is ambiguous (the two reference windows), and the
   hour refers to the first version's design, which this revision does not describe.
7. §5.2: "The label waits 19 min between the conjugate and the accumulation" does not match the table (32.5 → 49.7
   = 17.2 min); 19 min is from the middle of the conjugate step.
8. §2.4 and §4.4: "upper limit by the slope criterion (docs/03)" is not explained.
9. §5.3: "blanks contaminated up to 1 pg/mL (C1 of docs/08)" collides with review finding C1 (the product question)
   in the same document.
10. §6.4: "Human IgG from the laboratory is nominally zero and sampled up to 0.45 pg/mL" does not say that this is
    the model's blank-contamination parameter.

## Checked and found sound

* The step tables add up. Flow × time gives the stated volumes, and the builders reproduce the totals.
* The tier-1 A–B–A read is wired in the kit as stated (T_span = 318 s, README I).
* Loop Offline is placed as F1 asked, with the switch ≥ 60 s before the next window.
* The §5.1 valve scheme is a valid 2-position 6-port plumbing: no dead-heading, and bed 2 is isolated during the
  conjugate.
* All numeric tables of docs/30 match tiers.md and tiers.json (section 4).
* Chain arithmetic of §3.4, §4.4, §5.3 (Derived).
* The part numbers and citation keys named in section 5 are found where docs/30 points.

## What could not be checked

* The compliance of the pump, mixer and seals (needed for R2's time constant), the MicruX cell's pressure limit and
  gap, and the SM-FL line overhead: these are bench facts (docs/27 §9).
* The peak-current estimates of R3 use the kit's σ (1 µL tier 2, 1.5 µL tier 3) and a Gaussian plug. The real plug
  shape is unmeasured.
* The kit was evaluated nominally only (no Monte Carlo); my tier-1 kit call did not apply the 0.3 mM substrate
  setting of `run_tiers.t1`, so tier-1 currents were taken from docs/30 §3.4 instead.
* Vendor pages, literature and evidence labels were not re-opened (no browsing, by instruction).
