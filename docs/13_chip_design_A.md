# 13 — Cartridge A: detailed concept design (multi-run bead-transfer cartridge)

Status: 2026-11-12, **Revision B** (after the adversarial review docs/15). Inputs: docs/00, 02, 06, 07, 09, 10, 11, 12,
15; `params/*.yaml`; `automation/`. This document changes no other document, parameter or code. Every nearest-model
estimate quoted here was run on a **scratch copy** of the repository outside it (method of docs/12 §8 and Appendix A;
scripts in Appendix A of this document); no file in the repository was generated or modified.

## Revision B (after review docs/15) — what changed and why

The first pass (Revision A) could not be built as drawn: a TPE membrane on the top face could not close channels lying
5.8 mm lower in the bottom face (docs/15 A1), and the electrode pads of a face-down die were unreachable from the lid
(A2). Revision B redesigns the card around a **foil / channel-sheet / TPE-ceiling laminate** in which every valve and gate
is the TPE ceiling of the channel it closes, pressed from the top onto the foil floor, while all magnets act from below
through the foil; a **plan-view zoning** separates anvil-supported valve islands from magnet windows and the drag slot
(§2). The die rests face-down on the channel sheet and is contacted **from below through a dry contact window** outside
its seal (§2.7). The read is now a **three-window step read** that cancels constant offset and linear drift (§3.5.4).
The step table was rebuilt and checked for overlaps of every read window against every actuation of every run (§7).
The user decisions of 2026-11-12 (reagents from the dock, ≈ 14 determinations per card, ≥ 3 min margin, mandatory
post-high cleaning cycle, M5a before G1) are built in.

**Consequences stated up front (headline numbers, nearest-model, §1.3):**
* **Without the pre-electrolysis credit (headline): median LOD 3.67 pg/mL [0.53–126], P(success) 0.150**; with the
  ×0.01 credit (UNVERIFIED until E1.2b and M5a; supported by the computed escape 0.2–0.5 % of the new geometry, §3.6):
  2.33 pg/mL, P 0.215. After U1–U3 screening (L6 + L7): 1.34 / 0.328 without, 1.33 / 0.330 with the credit.
  **Revision B therefore has no LOD advantage over gen-1** (primary 3.5 pg/mL, P 0.16; after screening 1.3, P 0.32;
  CLAUDE.md status, docs/08 §10). The price of the ≥ 3-min margin and of quiet read windows is ≈ 0.04 in P
  (0.187 → 0.150 without credit at equal dilution; 0.196 → 0.150 against Revision A as published, §1.3).
* Result **56.75 min after Inject Start** (margin 3.25 min; 57.75 min from the start of aspiration); cadence 31.0 min;
  **14 determinations per card** (10 samples + 4 QC) in 7.9 h from insertion; 17 membrane valves + 4 gates = 21,
  16 actuations per run (18 in the fallback read mode), busiest valve 17 cycles per card (31 in the fallback).
* The case for A is now throughput (31 vs 56 min per sample), buffer use and automation — not LOD (docs/15 §5 item 1).

### Finding-by-finding map (docs/15 → this document)

"Resolved" means the design now addresses the finding with arithmetic shown; every such item still has a bench check,
named in the last column. "Open" means it cannot be closed on paper.

| docs/15 ID | Finding (short) | Status in Revision B | Where | Bench experiment that decides |
|---|---|---|---|---|
| A1 | top TPE cannot reach bottom-face channels; gates as deep wells | **Resolved in design**: channels are through-cuts in a 0.175 mm channel sheet on the foil, TPE is their ceiling, valves/gates press the TPE onto the foil; magnets below; plan-view zoning; per-valve stubs ≤ 0.3–0.5 mm recomputed | §2.1–2.6, §4 | M4 (sealing of a flat-floor TPE valve in a 0.5 × 0.175 mm channel, 100 cycles), M1 (bead passage under gates) |
| A2 | die pads unreachable | **Resolved in design**: die face-down on the channel sheet, pads on its lower face outside the seal, contacted from below by pogo pins through a dry contact window in a zone no magnet enters; electrode bay shielded | §2.7, §6.3 | M5a uses the same contact route on a catalogue die; C2 |
| S1 | stub geometry contradicts table; escape ≈ 11 % | **Resolved**: geometry made consistent (stubs ≤ 0.5 mm, WE fingers over the in-die lane segments, fast-exchanging CE/RE pocket fed by the flush); escape recomputed **0.2–0.5 %** (D 9–7×10⁻¹⁰); 1-mm stubs would give 4.8–5.6 % | §3.6 | M5a escape arm (≤ 1 %), M5 |
| S2 | double step does not cancel drift; noise mapping lacks √2 | **Resolved in design, open on the bench**: three-window read Q_a − 2Q_b + Q_c (offset and linear drift cancel; curvature bound 0.27 pA/min² for 0.025 nC); mapping with the factor 2; requirement SD(Q_net) ≤ 0.05 nC ⇔ white noise ≤ 3.7 pA | §3.5.4, §1.3 | **M5a** (drift-corrected acceptance, with dock noise sources) |
| S3 | read window collides with other runs; check only adjacent | **Resolved**: periodic check over all offsets k·C (k = −4…4) for every actuator class, ±0.25 min jitter guard; zero conflicts at C = 31.0; activities allowed during reads defined | §7.1–7.2 | C2 (two staggered chambers); M5a tests the allowed class |
| S4 | step-table arithmetic (3.5 min per pair, 22.3 mm drag); margin ≈ 1.1 min; reagent life | **Resolved**: table rebuilt by script; drag path 23.3 mm at 0.20 mm/s (116.5 s); margin 3.25 min; card capped at 14 determinations ≈ 7.9 h | §7.1, §1.1 | Stage 0 (injection overhead), C2 timing log |
| S5 | stranded WL beads pushed into the next incubation | **Resolved**: WL_k is refreshed J → IC_k immediately after the drag of the same run, before that chamber's cleaning | §3.3.6, §7.1 | M1 (beads arriving in IC_k after refresh + cleaning ≤ 1) |
| S6 | shared clean/dirty syringe paths; serpentine unbudgeted | **Resolved**: clean pump S_A only dispenses, S_IC_k and S_RC only pull to waste; rinses enter through a separate chamber inlet; the serpentine never returns liquid during washing; all paths in the budget | §3.2, §3.4, §8.3 | M7 (same-chamber carry-over), M2 |
| S7, S7b | gather cannot reach the far half; hand-over order impossible | **Resolved**: fixed collection magnet per chamber (Z only), gather by three raster passes of the small drag magnet (two cover the floor, the third is spare) (capture half-width ≥ 2.7 mm at 0.3 mm/s, recomputed), no magnet ever under the other chamber; M_c and M_d are separate units | §3.3 | M1 (≤ 1 % of beads left on the floor) |
| S8 | credits unsupported; fallback voids credit | **Resolved for A**: credit only for the step-read mode with the computed escape; headline without credit; the R-flow fallback runs **without** pre-electrolysis (so baseline and plug carriers match) and is the no-credit case | §3.5.7, §3.6 | E1.2b, M5a |
| S9 | docs/14 contamination pinning | not candidate A — **open for docs/14's owner** (this document uses additive bounds only) | — | — |
| S10 | stale comparison tables | **Resolved for A here**: like-for-like table with and without credit (§1.3); docs/12 §0 and docs/14 §F still carry the old A — **open for their owners** | §1.3 | — |
| S11 | carry-over budget not allocated | **Resolved**: per-path budget, normal and post-high, sum 9.6×10⁻⁵ ≤ 10⁻⁴; SM-FL allocated 3×10⁻⁵ (better than its nominal 10⁻⁴) | §8.3 | E1.10, M1, M7 (100 ng/mL challenge) |
| W1 | "reagents on the card" no longer true | **Resolved by user decision (2026-11-12)**: the card is a fluidic/valve/electrode consumable, not a reagent pack | §5 | — |
| W2 | transfer CV not in M1 | **Resolved**: M1 acceptance transfer CV ≤ 5 % | §10.3 | M1 |
| W3 | M1 cannot count stranded beads by sampling | **Resolved**: whole-path fluorescence imaging | §10.3 | M1 |
| W4 | carry-over test cannot resolve 10⁻⁴ | **Resolved**: 100 ng/mL challenge in M7/GC2, n = 5 per path | §8.3, §10.3 | M7, GC2 |
| W5 | Au QRE in a pocket with changing HQ/BQ | **Open**: within-run QRE log against a docked Ag/AgCl in M5a/M5 | §3.5.5, §10.1 | M5a (e) |
| W6 | substrate conductivity | **Resolved**: NaCl 50 mM fixed (ALP effect UNVERIFIED, E1.7-type check); R_u ≈ 14 kΩ (55 kΩ without NaCl), R_u·C ≤ 0.08 s ≪ τ | §3.5.5 | E1.7-type check |
| W7 | two calibration populations | **Resolved**: per-chamber lot calibration; per card one blank per chamber at the start and one control per chamber at the end | §8.2 | C2/GC2 |
| W8 | docs/09 F1 relaxed silently; dilution /1.7 | **Resolved**: F1 relaxation recorded (§3.1); model now uses the real dilution /1.85 | §3.1, §1.3 | M2 |
| W9, W10 | C′ transfer; Sun2008 over-read | not candidate A (Sun2008 is not cited here) — open for docs/12/14 | — | — |
| N1 | MC dimensions, 170/176 µL, conjugate stock | **Resolved**: MC 2.0 × 1.0 mm footprint × 5.0 mm deep; chamber 185 µL; stock 5.6 nM | §2.3, §3.1 | — |
| N2 | CE charge count | **Resolved**: 7 forward steps per run, ≈ 1.5 µC per direction | §3.5.5 | — |
| N3 | turnover during step b | **Resolved**: the three-window read cancels constant turnover to −0.9 % (computed) | §3.5.4 | — |
| N4 | Otieno2014 wording | not cited in docs/13 — open for docs/10/12 | — | — |
| N5 | Kim2015 key collision | cited here with its DOI (Sensors, doi:10.3390/s150306469) | §3.5.5 | — |
| N6 | docs/14 part numbers | not candidate A; no part number here outside docs/11 | §6.2 | — |
| N7 | CHILDERS2024 / CS_1367 not the TPE-on-COC system | **Resolved**: both qualified; no endurance evidence exists for the chosen pair; M4 decides | §4 | M4 |
| N8 | M-280 magnetisation | **Open** (UNVERIFIED, kept as such) | §3.3.2 | M1 (follow speed measured directly) |
| N9 | E1.2b on carbon, 1 mM, bulk | **Resolved**: M5a adds Au, 3 mM, the RC geometry | §10.1 | M5a (d) |
| N10 | U5 residual-bead 10⁻³ in docs/06 E2.4 | not candidate A — open for docs/06's owner | — | — |
| docs/15 §4 stretched sources | Otieno2014, Sun2008, CHILDERS2024/CS_1367 | the two cited here (CHILDERS2024, CS_1367) are qualified in §2.1 and §4; Wang2013 speed is not transferred to M-280 (bead type not in the abstract) | §2.1, §3.3, §4 | — |

**Sourcing conventions** (as docs/12). Every number names its source: repository section (`docs/09 §2.2 F8`),
parameter key (`ma.capture.bead_dose_cv`), or a literature/vendor key already cited with DOI/URL in docs/10 or docs/11
(Wang2013 = doi:10.1039/c3an01166f; CS_1367, CS_EXPLAINED, … = docs/11 §9). **Derived** = calculated here, arithmetic
shown or script named (Appendix A). **[assessment]** = engineering judgement. **UNVERIFIED** = not traceable to a
checked source (this includes every physical constant used that is not in the repository: the magnetic moment of an
M-280 bead, the double-layer capacitance of thin-film gold, NdFeB remanence, the Young's moduli of COC and TPE).
**Nearest-model estimate** = output of the existing model on an existing architecture with stated overrides (docs/12
§8); it is not a prediction of the cartridge.

---

## 1. Design summary and what changed

### 1.1 The design in one paragraph

A 75.5 × 50 mm card (double-slide footprint, CS_EXPLAINED), ≈ 6.2 mm thick, built as a laminate: a 140 µm COC floor
foil (magnet and Peltier side), a 0.175 mm COC **channel sheet** with all channels, lanes and the readout chamber cut
through it, a 0.3–0.5 mm **TPE ceiling** that is the membrane of every valve and gate, and a moulded COC **upper body**
carrying the chambers, tanks, plunger bores and the die window. Two stirred incubation chambers (IC1, IC2, ≈ 185 µL
working) receive the SM-FL plug (1.5 loop volumes), a 10 µL bead dose from a cooled, agitated dock vial and a 10 µL
conjugate dose from an on-card tank that the dock filled at insertion, all through one swept inlet channel per
chamber. After a 28.5-min one-step incubation with tangential tidal mixing (22.15 min of it stirred; the rest paused
for other runs' reads), a fixed collection magnet under the chamber pulls the beads to the foil; a small drag magnet
gathers them in three raster passes to the throat funnel, holds them through six partial-drain rinses, and drags the pellet at
0.20 mm/s along a buffer-filled wash lane (drag path 23.3 mm) into a **1.34 µL, 0.200 mm high readout cell** whose
ceiling is the working electrode (WE1 plus its lane fingers, with WE2 in parallel). The cell was flushed with fresh 3 mM
HQDP through its CE/RE pocket, pre-electrolysed twice (PE1 removal; PE2 = residual-activity monitor and final removal)
before the pellet arrived. Accumulation 11 min, sealed, at open circuit; readout by a **three-window potential-step
read** (Q_net = Q_a − 2Q_b + Q_c). A gen-1-type flow read over WE2 is kept as the fallback (without pre-electrolysis).
Beads leave to a bead-waste pocket held by a fixed magnet. **Result 56.75 min after Inject Start; cadence 31.0 min; 14
determinations per card in ≈ 7.9 h from insertion.** The card carries no factory-filled reagent (§5).

### 1.2 Changes from docs/12 candidate A (D1–D13) and from Revision A (R1–R14)

| # | Before | Revision B | Reason |
|---|---|---|---|
| D1 | RC 4 × 10 mm × 50 µm = 2 µL; WE 37 mm² | RC 2.6 × 2.0 × 0.200 mm plus electrolysed lane fingers and WE2 channel: **cell 1.34 µL**; WE1 + fingers 5.35 mm², WE2 2.0 mm²; 3 mM HQDP | step-read double-layer charge (§3.5.4); exhaustive collection kept (τ = 18 s); ULOQ ≥ 1000 pg/mL needs 3 mM (§3.5.6) |
| D2 | single step read | **three-window step read** (R1, below) | docs/15 S2 |
| D3 | no fallback | WE2 flow read, **run without pre-electrolysis** | docs/15 S8 (iv) |
| D4 | CE/RE at the end of a dead-end branch | CE/RE in a 0.032 µL pocket behind a short wide neck (0.4 × 0.2 × 0.15 mm), **fed by every substrate flush** | escape (§3.6) and chloride constancy (§3.5.5) |
| D5 | collection and drag magnets on one carriage | **fixed collection magnet per chamber (Z only)** + one X–Y–Z drag-magnet carriage + fixed hold and waste magnets | docs/15 S7, S7b |
| D6 | flat-floor gates actuated through a top membrane that could not reach them | all valves and gates are flat-floor TPE-ceiling valves in one laminate (R2) | docs/15 A1 |
| D7 | V2 recommended | **dock supply is the user decision** (§5) | user decision 2026-11-12 |
| D8 | HQDP tank at 25 °C in use | kept for the step-read mode; the fallback reads without pre-electrolysis, so a 25 °C tank only adds gen-1-type referenced hydrolysis (§3.5.7) | docs/15 S8 (iv) |
| D9 | 20 valves, busiest 40 | **21** (17 valves + 4 gates; V13 deleted, V17/V18 added), busiest **17 per card** (31 fallback) | §4 |
| D10 | bead-waste pocket flushed every run | kept; flush now enters through the CE/RE pocket | §3.8 |
| D11 | cadence 31.0, result 58.0 (really 58.9) | cadence 31.0, **result 56.75** | user decision 2 |
| D12 | dock fill at insertion as default | **binding** (user decision 1) | §5 |
| D13 | 2-min post-transfer flush to bypass | kept; the card valves switch at 3.35 min (BSM at 1 µL/min from 1.5 to 3.35 min), then the 2-min flush | §3.1, §7.1 |
| R1 | Q_a − Q_b, 90/15/90 s | Q_a − 2Q_b + Q_c, windows 60 s, rests 15 s, pre-rest 30 s (4.0 min) | offset, linear drift and constant turnover cancel (§3.5.4) |
| R2 | 6 mm moulded body, channels in the bottom face, TPE on top | foil / 0.175 mm channel sheet / TPE ceiling / upper body; plunger bores to the TPE | §2.1 |
| R3 | die pads from the lid | contact from below through a dry window | §2.7 |
| R4 | gather by sweeping the collection block 4 mm | three raster passes of the drag magnet (y = +2, −2, 0 mm; two suffice for the Ø 8 mm floor at ≥ 2.7 mm capture half-width) | §3.3.3 |
| R5 | rinses through the tidal serpentine | rinse fills through a clean inlet, drains through the serpentine, six partial drains (30 µL residual, pellet never exposed) | §3.4 |
| R6 | IC1/IC2 16 mm apart | 26 mm apart (centres y = 38 and 12) | a raised collection magnet pulls 1.0 pN on beads 12 mm away, 0.08 pN at 22 mm (§3.3.2) |
| R7 | PE1 25 min before the drag, PE2 as Q_a − Q_b monitor | PE1 right after the flush; open-circuit hold 2.95 min; PE2 = monitor + final removal | a second-difference read cancels constant turnover, so residual activity must accumulate *before* PE2 (§3.6) |
| R8 | WL refresh before the next dose | WL refresh J → IC_k right after the drag of the same run | docs/15 S5 |
| R9 | S_RC both dispensed and pulled; rinses via S_IC | clean pump S_A (dispense only), S_IC_k and S_RC pull only | docs/15 S6 |
| R10 | 16 determinations, 2 priming runs | **14 determinations, no priming runs** (the start blanks replace them) | user decision 2, reagent life |
| R11 | 3 → 6 rinses after > 100 pg/mL | 6-rinse cleaning by default + **mandatory post-high cycle and blank check** in the next slot of the same chamber (§7.4) | user decision 3 |
| R12 | inlet, bead, conjugate ports separately into the chamber | one **swept inlet channel C_k** per chamber, chased by S_A after every delivery | port stubs would otherwise carry ≈ 10⁻⁴ (§2.6) |
| R13 | accumulation 15 min, incubation 30 min | accumulation 11 min, incubation 28.5 min (22.15 stirred) | margin ≥ 3 min with quiet reads; the split is P-neutral (§1.3) |
| R14 | ports as 1.4 mm through-holes in a 2 mm slide | liquid ports through the foil from below (≈ 0.24 µL each), sealed in the anvil plate | no 5.5-mm vertical vias (≈ 8 µL each) |

**What did not change:** chemistry, antibody pair and doses of docs/05 §4.1 (5×10⁵ beads, 0.3 nM conjugate in the
chamber, HQDP pH 9.5); one-step format; Waters interface of docs/12 §2.1 (BSM delivers only A1, parked at 1 µL/min to a
bypass; Inject Start contact closure); 25.0 °C assay zone; the 10⁻⁴ carry-over criterion (`gates.yaml` `carryover`).

### 1.3 Nearest-model estimates (scratch copy, n = 2000, seed 20261111)

Base = docs/12 run "A0" architecture (`OS` design with the chamber, timing and thin-layer overrides of docs/12 §8), with
3 mM HQDP, `lod_scale` 1/0.90, tubing NSB factor pinned 0.01 (clean readout path, docs/15 §3 (i)), and these Revision B
values: `ma.timing.in_vial_incubation` **25.33 min** (22.15 stirred + 0.5 × 6.35 paused, the 0.5 being
`ma.capture.in_vial_unstirred_rate_factor`), `hw.timing.accumulation_time` **11 min**, `ma.geometry.magnetic_trap_volume`
**1.34 µL**, chamber dilution **/1.85** (185 µL per 100 µL loop, §3.1; docs/13 Revision A used /1.7). "Credit" =
pre-electrolysis factor on `ma.chemistries.alp_hqdp.free_product_impurity` (UNVERIFIED until E1.2b and M5a). The
three-window read is not represented by the model; its background enters only through the noise rows.

| Run | Nominal LOD | Median [5–95 %] (pg/mL) | P(success) | ULOQ nominal (pg/mL) |
|---|---|---|---|---|
| *Reference:* docs/13 Revision A (credit ×0.01) — reproduces docs/15 §3 | 0.40 | 1.88 [0.37–54] | 0.258 | 3043 |
| *Reference:* docs/13 Revision A without credit — reproduces docs/15 §3 | 0.41 | 2.45 [0.43–81] | 0.196 | 3043 |
| step 1: Revision A, no credit, real dilution /1.85 | 0.44 | 2.63 [0.46–88] | 0.187 | 3043 |
| step 2: + incubation 25.33 min effective (accumulation 15, RC 1.0 µL) | 0.47 | 3.00 [0.50–93] | 0.165 | 3981 |
| step 3: + accumulation 11 min | 0.50 | 3.37 [0.52–108] | 0.156 | 5208 |
| **Revision B, no credit (headline)** = step 3 + cell 1.34 µL | **0.54** | **3.67 [0.53–126]** | **0.150** | 6813 |
| Revision B, credit ×0.01 (escape 0.2–0.5 %, §3.6) | 0.46 | 2.33 [0.44–63] | 0.215 | 6813 |
| Revision B, credit ×0.07 (stubs 1 mm instead of ≤ 0.5 mm) | 0.46 | 2.44 [0.46–65] | 0.203 | 6813 |
| Revision B + U1–U3 screening (L6 + L7), no credit | 0.18 | 1.34 [0.33–9.0] | 0.328 | 3043 |
| Revision B + L6 + L7, credit ×0.01 | 0.18 | 1.33 [0.33–8.9] | 0.330 | 3043 |
| Revision B, S4a (lot free HQ 10⁻³), no credit | 27.9 | 64.7 [5.5–1731] | 0.000 | 6813 |
| Revision B, S4a, credit ×0.01 | 0.54 | 2.75 [0.51–60] | 0.171 | 6813 |
| Revision B, S4a, credit ×0.07 | 2.00 | 6.27 [0.90–159] | 0.056 | 6813 |
| no credit, tidal mixing allowed during reads (incubation 28.5 min effective) | 0.50 | 3.32 [0.50–116] | 0.164 | 6813 |
| no credit, paused minutes capture nothing (22.15 min) | 0.59 | 4.18 [0.58–134] | 0.139 | 8913 |
| no credit, chamber dilution /2.2 (gen-1 mixing) | 0.62 | 4.27 [0.59–147] | 0.135 | 8913 |
| no credit, bead-dose CV pinned 0.05 / 0.10 | 0.54 / 0.62 | 3.23 / 3.78 | 0.149 / 0.124 | 6813 |
| no credit, bead transfer pinned 0.80 | 0.56 | 3.46 [0.54–112] | 0.151 | 8913 |
| no credit, read SD(Q_net) pinned 0.023 / **0.05** / 0.08 / 0.155 / 0.30 nC | 0.54 / **0.58** / 0.65 / 0.92 / 1.55 | 3.26 / **3.46** / 3.74 / 4.51 / 6.03 | 0.154 / **0.141** / 0.124 / 0.097 / 0.061 | 6813 |
| credit ×0.01, read SD(Q_net) 0.05 nC | 0.51 | 2.35 [0.47–50] | 0.198 | 6813 |
| L6 + L7, no credit, read SD(Q_net) 0.05 nC | 0.20 | 1.37 [0.37–10] | 0.322 | 3043 |

Read-noise mapping (docs/15 S2 correction): the model's electrochemical term is σ_Q = i_ref·√(T/2B)·√2 with T =
`hw.timing.readout_time` 60 s and B = `ma.noise.reference_bandwidth` 1 Hz, i.e. **σ_Q = 7.75 s × i_ref** (at the nominal
`hw.flow_cells.thin_layer_basi.we_area`); the rows pin i_ref = SD(Q_net)/7.75 s (3.0, 6.5, 10.3, 20, 38.7 pA). The
unpinned rows sample `hw.gamry.noise_rms_flow` over 0.5–20 pA (default 3 pA), which is why a pinned 0.023 nC row has a
lower median than the headline.

**Like-for-like comparison (docs/15 S10; numbers of other candidates as reproduced in docs/15 §3, n = 2000):**

| Candidate | No pre-electrolysis credit: median / P | With credit: median / P | Note |
|---|---|---|---|
| gen-1 primary (docs/08 §10, thin-layer default) | 3.5 / 0.16 | — | after screening 1.3 / 0.32 |
| **A, Revision B (this document)** | **3.67 / 0.150** | 2.33 / 0.215 (×0.01, escape computed 0.2–0.5 %) | after screening 1.34 / 0.328 (either) |
| A, Revision A (docs/13 first pass; not buildable, docs/15 A1/A2) | 2.45 / 0.196 | 1.88 / 0.258 | margin was ≈ 1 min, reads unguarded |
| B (docs/12/14) | B0 2.33 / 0.153 | B1 2.08 / 0.174 | B's guard-cell credit unsupported (docs/15 S8) |
| C′ (docs/14) | — | C′1 2.13 / 0.165 | C′ credit unsupported (docs/15 S8) |

Reading (Derived from the rows): (i) **the cost of the user's timing decision is ≈ 0.04 in P** (0.187 → 0.150 without
credit), almost all from the incubation (25.33 min effective instead of 30: −0.022) and from the read-free tidal pauses;
the incubation/accumulation split is P-neutral (P 0.150–0.154 for 26.5/13 to 31.5/8, scratch `runB2`); (ii) the
pre-electrolysis credit is worth +0.065 at nominal, nothing after screening, and decides S4a (0.000 → 0.171), which it
rescues only if the stubs stay ≤ 0.5 mm (×0.07 at 1 mm: 0.056); (iii) the read requirement **SD(Q_net) ≤ 0.05 nC** costs
0.013 against the 0.023 nC row; at 0.155 nC P falls to 0.097; (iv) the chamber mixing factor and dilution remain worth
as much as the whole cartridge-vs-gen-1 difference (/2.2: 0.135); (v) allowing tidal strokes during reads (if M5a shows
no effect) is worth +0.014.

---

## 2. Layer stack and layout

### 2.1 Valve principle and layer stack

**Principle.** The actuated layer must *be* the wall of the channel it closes (docs/15 A1). docs/11 §3 sources two
forms: the mechanically actuated membrane valve, in which a foil or TPE membrane forming the channel lid is pressed onto
a seat (CS_1367: the 100 µm Topas lid foil of a COC chip is pressed, "No membrane", single use, tight to 3 bar), and the
TPE membrane valve between moulded layers (ChipShop moulds TPE and bonds multi-layer stacks, CS_FAB). Revision B uses
the first principle with a TPE membrane: **every channel is a through-cut in a thin channel sheet, its floor is the
foil, its ceiling is the TPE; a valve or gate is a plunger pressing the TPE ceiling down onto the foil floor** across the
full channel height (flat-floor valve, no seat ridge, no bead-trapping step). The differences from CS_1367 are stated,
not hidden: the membrane is TPE, not the foil (a 100 µm COC foil pressed 0.175 mm into a 0.5 mm channel would deform
plastically [assessment], which is consistent with CS_1367 being single use); it is pressed from the top, not from
below; and no endurance evidence exists for TPE on COC (CHILDERS2024 is an eCOC membrane on PC/PETG, > 50 actuations;
CS_1367 is single use; docs/15 N7). M4 decides.

**Why this resolves the magnet conflict.** Beads sit on the foil; magnets act from below through 140 µm of foil;
plungers act from above on the TPE. The foil under a closed valve needs a counter-support: valves lie over an
**anvil plate** in the dock, which has **windows and a slot only where magnets must reach the foil** (§2.2 zoning). The
four gates and two lane valves (V11, V12) sit over the 4 mm drag slot; their plunger force is limited to ≤ 1.5 N, which
deflects the bonded foil + sheet (0.315 mm COC) by ≈ 15 µm over a 4 mm span (Derived: clamped plate, w = F a²/(16πD),
a = 2 mm, D = E t³/(12(1 − ν²)) = 7.7×10⁻³ N·m with E 2.6 GPa and ν 0.35, both UNVERIFIED; w = 1.5 × 4×10⁻⁶ /
(16π × 7.7×10⁻³) = 15 µm). No valve lies over the Ø 12 mm chamber windows (the same arithmetic over an 11 mm span gives
≈ 80 µm per N, too much against a 0.16 mm magnet gap).

| Layer | Material / thickness | Function | Source / reasoning |
|---|---|---|---|
| L0 floor foil | COC foil 140 µm, thermally or solvent bonded to L1 | floor of every chamber, channel, lane, the readout cell and the tanks; magnet-side wall (beads sit on it); Peltier contact face; pierced at the liquid ports | 140 µm COC lid (DARWIN_CS4CH); requirement ≤ 0.5 mm (docs/09 F8) |
| L1 channel sheet | COC 0.175 mm, all channels as **through-cuts** (laser-cut for C1/C2 prototypes; hot-embossed or moulded for series, UNVERIFIED as a 0.175 mm through-cut part) | defines every channel height (0.175 mm), the throat funnels, the bead-waste pocket outline and, with L1b, the readout-cell height | laser-cut layers (docs/11 §1.3); hot embossing of COC (GOODFELLOW_MF); channel widths ≥ 0.3 mm here, inside the ≥ 50 µm guideline (DATRON_POTOMAC, PMMA) |
| L1b die film | 25 µm double-sided adhesive or bonding film, laser-cut with the L1 pattern, **only under the die** | bonds the die; makes the cell height 0.175 + 0.025 = **0.200 mm** | 25 µm PET/PTFE gasket of docs/07 §5.3; adhesive creep and leachables UNVERIFIED (docs/11 §1.3, §6.2) |
| L2 TPE ceiling | TPE sheet 0.3–0.5 mm (thickness UNVERIFIED), laminated to L1 | ceiling of every channel outside the die; membrane of all valves and gates; cut out over chambers, tanks, the die window, BW and ports | ChipShop moulds TPE and bonds stacks (CS_FAB); TPE–COC bond under cycling UNVERIFIED |
| L3 upper body | COC, injection-moulded (milled for prototypes), ≈ 5.5 mm | chamber bores (Ø 8 mm), conjugate tank and meter, HQDP tank, BW recess, plunger bores Ø 1.5 mm down to the TPE at every valve and gate, die window, vents and gas ports | moulding of COC, MOQ 100 (CS_FAB); vias ≥ 0.5 mm (VANTIVA_GUIDE); 5.5 mm body for 250 µL chambers (docs/11 §0) |
| L4 vents | PTFE membrane discs (Ø 4 mm), heat-staked on L3 | chamber headspace vents, meter stop vent, tank vents | docs/09 F1; wet-out by Tween/BSA UNVERIFIED |
| D electrode die | borosilicate glass 10.0 × 6.0 mm, thickness to foundry standard (UNVERIFIED), Au 150 nm on 50 nm Ti, SU-8 or polyimide passivation; WE1 (with two lane fingers), WE2, CE, RE, contact-check loop; pads on the **lower** face at the far end | ceiling of the readout cell, its lane ends, the WE2 channel and the CE/RE pocket | Micrux custom thin film (MICRUX_TF); IMT (IMT_FLYER); 10 × 6 mm support size (PALMSENS_IDA) |

Card thickness 0.14 + 0.175 + 0.4 + 5.5 ≈ **6.2 mm** (custom; the catalogue double slide is 2 mm, CS_EXPLAINED).
Coordinates: origin at the lower-left corner seen **from the top**, x along 75.5 mm, y along 50 mm. Thermal zones:
**reagent zone** x = 0–20 mm (4–8 °C), **thermal break** x = 20–24 mm (through-slot in L3 except two 3 mm bridges;
L0–L2 continuous), **assay zone** x = 24–75.5 mm (25.0 ± 0.2 °C, docs/07 §5.1).

### 2.2 Plan view and zoning (top view; not to scale; coordinates in mm)

```
 y=50 +----------------------------------------------------------------------------------------------+
      | REAGENT ZONE 4-8 C ||       ASSAY ZONE 25.0 C                                                     |
      |                    ||  [V9]-P_d1      .----.                                                      |
      | RCj conj tank      ||   (31,38)      / IC1  \ =fun=\                     ......................   |
      |  (3-13, 33-43)     ||     Valve     |(40,38) |      \WL1                 :E  contact window    :   |
      |  [V8]   P_cf o     ||     island    |  Ø8    |       \\                 :  pads, pogo from    :   |
      |   |                ||     II         \  Mc1 /         \\                :  below (55-61,30-33):   |
      |  MC 10 uL (16,30)  ||                 '-C1-'            \\  [V11]      :......................:   |
      |   stop vent P_mv   ||   VALVE ISLAND I   |               G1\  |  [V12]   +------ DIE 6 x 10 ------+   |
      |   |                ||   P_in o-[V1][V2]-[V3]-o P_byp      J(50,25)==WLc==G3=[ RC (56.8,25) ]=WE2=[V14] |
      |   +--conj line=====>|   P_b o-[V4][V5]   P_a o-[V17][V18]-+G2/              |  neck+pocket   |   |      |
      |                    ||   conj: [V6][V7]   (S_A manifold,  /                 +--[V15]--G4-----+   |      |
      |                    ||                     also to V11)  //                       |    BW (56.8,20.5) |
      |                    ||                 .-C2-.            //                        [V16]  M_w below  |
      |                    ||  [V10]-P_d2    /  Mc2 \          //WL2                 RS HQDP tank 0.72 mL   |
      |                    ||   (31,12)     | IC2    | =fun=  /                       (62-74, 4-16) P_rf o   |
      |                    ||               |(40,12) |                               P_s o  P_wo o          |
      |                    ||                \      /                                                     |
 y=0  +----------------------------------------------------------------------------------------------+
     x=0               x=20-24                                                                     x=75.5
  ==   wash lane / drag path (foil floor, TPE ceiling; anvil SLOT 4 mm wide below it)
  fun  throat funnel 2.5 -> 0.5 mm in L1 inside the chamber bore (open above)
  C1,C2 swept chamber inlet channels; [Vn] valve over the anvil; G1-G4, V11, V12 over/at the slot (force <= 1.5 N)
  o    liquid port through the foil from below (face seal in the anvil plate)
```

**Zoning below the card (dock side, plan view):**

| Zone | Where (x, y in mm) | What is below the foil | What may be above (in the card) |
|---|---|---|---|
| Anvil (valve islands I, II, III, reagent zone) | everything not listed below | rigid plate (reagent zone: the Peltier plate), face seals for ports | all valves except G1–G4, V11, V12; all ports |
| Chamber windows W1, W2 | Ø 12 mm centred on (40, 38) and (40, 12) | M_c,k (10 × 10 × 5 mm, Z only, 25 mm stroke) and, during the gather/rinses, M_d | chamber floor, throat funnel, C_k crossing; **no valve** |
| Drag slot | 4 mm wide along WL1, WL2, J, WLc, RC → BW | M_d on its post (carriage below the anvil) | lanes, gates G1–G4, V11, V12 (force-limited) |
| Hold window | 4 × 4 mm at (56.8, 25.0) | M_h (Z lift) | readout cell |
| BW recess | (56.8, 20.5) | M_w fixed in the plate | bead-waste pocket |
| Electrode bay | (55.3–60.7, 29.8–33.2) and the space below it | pogo block in a grounded enclosure | die pads only (dry); ≥ 3.8 mm from the nearest wetted edge |

No magnet moves into the electrode bay or under the other chamber: M_c,k never leaves its window; M_d travels between
windows lowered by ≥ 8 mm below the bead plane and ≥ 6 mm laterally from an incubating chamber (§3.3.2: ≤ 0.35 pN).

### 2.3 Feature table

Volumes Derived (V = L × W × D; cylinder π r² D). Channel height 0.175 mm under the TPE, 0.200 mm under the die.

| ID | Feature | Centre / route (x, y) mm | Footprint | Height | Volume | Notes |
|---|---|---|---|---|---|---|
| IC1, IC2 | incubation chambers | (40, 38), (40, 12) | Ø 8.0 mm bore through L3, L2, L1; floor = foil | 5.5 + 0.6 mm | 290 µL total; **185 µL working**, fill height 3.68 mm | 185 µL = 150 + 10 + 4 + 10 + 3 + 3 + 5.3 (§3.1); wetted area 50.3 + π·8·3.68 = **143 mm²** |
| fun1, fun2 | throat funnel in L1 inside the bore | x_c + 2.0 → x_c + 4.0 | 2.5 → 0.5 mm wide | 0.175 (open above) | — | pellet held at x_c + 2.5 during the rinses (open to the chamber) |
| C1, C2 | swept chamber inlet channels | from valve island I to the chamber −y/+y wall | 0.5 mm × 3 mm | 0.175 | 0.26 µL each | sample, beads, conjugate and A1 enter through it; chased after every delivery (§3.1) |
| P_d1, P_d2 + nozzles | tidal/drain port and tangential nozzle opposite the throat | (31, 38), (31, 12) | 0.5 mm × 6 mm | 0.175 | 0.5 µL + port 0.24 µL | tidal buffer coil of 60 µL is on the **dock** side (FEP), not on the card |
| WL1, WL2 | wash-lane branches, bore wall → J | (44, 38) → (50, 25); (44, 12) → (50, 25) | 0.5 mm × 15.0 mm (bends ≥ 3 mm radius) | 0.175 | 1.31 µL each | foil floor; drag slot below |
| J | junction | (50, 25) | — | 0.175 | — | G1, G2 seals 0.3 mm from J; V11 tee on WLc 1.5 mm after J |
| WLc | common lane J → G3 | (50, 25) → (54.4, 25) | 0.5 mm × 4.4 mm | 0.175 | 0.39 µL | drag path apex → RC centre **23.3 mm** (1.5 funnel + 15.0 + 6.8) |
| RC | readout chamber | (56.8, 25.0) | 2.6 × 2.0 mm | **0.200** | 1.04 µL | floor = foil, ceiling = WE1; hold magnet below |
| cell | RC + G3 lane finger (0.5 mm) + G4 lane finger (0.65 mm) + RC → WE2 link + WE2 channel | — | — | 0.200 / 0.05 | **1.34 µL** | the electrolysed and read volume (§3.5.1) |
| WE2 channel | flow detector, fallback | (58.1 → 61.0, 25.0) | 1.0 × 3.0 mm, WE2 1.0 × 2.0 mm | **0.05 mm** (laminated 0.15 mm COC shim on the foil in the L1 cut-out) | 0.15 µL | shim tolerance UNVERIFIED |
| CER | CE/RE neck + pocket at the die's −y edge | neck 0.4 × 0.2 × 0.15 mm from the RC −y edge; pocket 0.4 × 0.4 mm | CE 0.3 × 0.3 mm, RE 0.1 × 0.1 mm on the die | 0.200 | 0.012 + 0.032 = **0.044 µL** | substrate inlet (V15) enters through the pocket (§3.5.5) |
| BW | bead-waste pocket | (56.8, 20.5) | 2.5 × 2.5 mm cut in L1 and L2 | 0.575 | 3.6 µL | M_w below; flushed every run via V16 |
| RCj | conjugate tank | (8, 38) | 10 × 10 mm | 5.0 mm | 0.50 mL (0.26 mL fill) | reagent zone; filled at insertion through P_cf |
| MC | conjugate meter | (16, 30) | **2.0 × 1.0 mm footprint, 5.0 mm deep** in L3 | — | **10.0 µL** | fill-to-vent (PTFE stop, vent port P_mv); docs/15 N1 |
| RS | HQDP tank | (68, 10) | 12 × 12 mm | 5.0 mm (+ L1/L2) | 0.72 mL usable (0.6 mL fill) | assay zone (D8); filled at insertion through P_rf |
| M_in | sample manifold P_in → V1/V2/V3 | island I | 0.5 mm wide, 12 mm total | 0.175 | 1.05 µL | V3 = bypass; stubs ≤ 0.3 mm (§2.6) |
| bead / conj lines | P_b → V4/V5; MC → V6/V7 | island I | 0.4 mm | 0.175 | 0.3 / 0.6 µL to the valves | join C_k within 0.3 mm |

### 2.4 Cross-sections

```
 lane / valve (open)                lane / valve (closed)               readout cell (section through WE1)
  plunger (up)                        plunger v (<= 1.5 N on gates)       == glass die, WE1 + fingers on its LOWER face ==
  | L3 COC 5.5 mm |                   | L3 |  |  | L3 |                  |L3|  die window   (no TPE under the die) |L3|
  |____  bore ____|                   |____|  |  |____|                  ====L1b 25 um film=====    ====L1b====
  ~~~~ TPE ceiling 0.4 ~~~~           ~~~~\  TPE  /~~~~                   |L1 0.175|  cell 0.200 mm (1.04 uL)  |L1|
  |L1|  lane 0.5 x 0.175   |L1|       |L1| \_____/ |L1|  TPE on the foil  ~~~~~~~~~ L0 foil 140 um, beads on it ~~~~
  ~~~~~~~ L0 foil 140 um ~~~~~~~      ~~~~~~~ L0 foil ~~~~~~~~            [M_h hold magnet, 0.16 mm gap]
  [anvil]  or [slot + M_d]            [anvil] (slot: <= 15 um deflection)
```

The TPE must conform into the corners of a 0.5 × 0.175 mm rectangular channel; leak rate UNVERIFIED (requirement
§4, test M4). Closing a valve displaces ≈ 0.5 × 0.175 × 1.0 mm ≈ 0.09 µL (half to each side, Derived); the last
closure on the sealed cell (G3 at the end of the drag) pushes ≈ 0.045 µL into it, taken up by the compliance of the TPE
over the cell-side stubs at a few kPa [assessment; E of TPE ≈ 2 MPa UNVERIFIED]; M4 measures the transient.

### 2.5 Ports (card ↔ dock)

Liquid ports are holes through the foil (and L1) from below, Ø 1.0 mm × 0.315 mm ≈ **0.24 µL** (Derived), sealed by face
seals in the anvil plate; gas ports and vents are on the top face. No Mini Luer anywhere (16.5 µL, CS_EXPLAINED).

| Port | Connects | Liquid | Dock side |
|---|---|---|---|
| P_in | SM-FL outlet → M_in → V1/V2/V3 | sample + A1 | 1/16″ PEEK ≥ 0.3 m (`hw.tubing.peek_isolation_length_each_side_of_cell`) |
| P_byp | V3 → waste | A1 | waste line with air gap |
| P_b | bead line → V4/V5 → C_k | bead slug, A1 chase | S_b holding coil, outlet line 2.5 µL |
| P_a | S_A manifold → V17/V18 (C_k) and V11 (J) | clean A1 only | S_A (dispense only) |
| P_d1, P_d2 | V9/V10 → nozzle → IC_k | chamber liquid (tidal, drain) | 60 µL FEP coil → S_IC_k (pull to waste only) |
| P_wo | V12 → waste | A1 (WLc refresh) | waste |
| P_s | V14, V16 → S_RC | substrate, product, spent-bead flush | S_RC (pull only) |
| P_rf | dock HQDP bottle → RS | HQDP at insertion | pressure-driven fill |
| P_cf | dock conjugate bottle → RCj | conjugate at insertion | pressure-driven fill (cooled bottle) |
| P_c, P_mv (top, gas) | RCj headspace; MC stop vent / air push | air | pressure channels |

9 liquid face seals + 2 gas ports; pogo contacts on 6 die pads (WE1, WE2, CE, RE, contact loop ×2) from below.

### 2.6 Swept volumes, dead volumes and stubs per path

Design rule (Derived from the escape and carry-over arithmetic of §3.6 and §8.3): **every branch off a sample, product or
bead path has its valve seal ≤ 0.3 mm from the trunk (≤ 0.5 mm at the cell)**; plunger tip Ø 1.0 mm centred 0.8 mm from
the trunk wall gives a 0.3 mm stub (0.5 × 0.175 × 0.3 = 0.026 µL).

| Path | Segments | Swept per run | Stubs / hold-up (volume) | Treatment |
|---|---|---|---|---|
| sample → IC_k | loop 100 µL + PEEK 3.8 µL + P_in 0.24 + M_in to V_k 0.6 + C_k 0.26 | 150 µL A1 at 100 µL/min, then 1.85 µL at 1 µL/min | V_k′ and V3 branch stubs 0.026 µL each; V_k seal on C_k 0.016 µL | D13 flush to bypass; C_k chased with 3 µL A1 by S_A |
| beads → IC_k | vial → coil → 2.5 µL line → P_b 0.24 → V4/V5 0.3 → C_k 0.26 | 10 µL slug + 4 µL A1 chase | 0.016 µL at C_k | chase ≥ 3.2 µL path volume (§5.2) |
| conjugate → IC_k | RCj → V8 → MC 10.0 → V6/V7 → C_k | 10.0 µL by air | 0.6 µL line, air-cleared | C_k chased with 3 µL A1 |
| tidal / drain | IC_k ↔ nozzle ↔ port ↔ dock coil | 50 µL every 30 s; drains | nozzle 0.5 µL inside the stroke | one-way to waste during washing |
| rinse / clean | S_A → P_a → V17/V18 → C_k → IC_k | 6 × 100 µL + 6 × 150 µL | — | clean side only |
| wash lane | WL_k + J + WLc | refresh 5 µL J → IC_k and 5 µL J → V12 per run | G_k′ stub at J 0.026 µL; V11 and V12 tee stubs 0.026 µL each | §3.3.6 |
| cell prep | RS → V15 → pocket → neck → RC → G4 → BW → V16 → P_s | 20 µL at 40 µL/min | G3 stub 0.044, G4 stub 0.044, V14 stub 0.026, V15 stub 0.02 µL | PE1 + PE2 (§3.6) |
| fallback read | RS → V15 → pocket → RC → WE2 → V14 → P_s | 10 µL at 10 µL/min | WE2 channel 0.15 µL | §3.5.7 |

**Bead-trapping stubs on the drag path:** the G_k′ stub at J, the V11 and V12 tee mouths, and the neck to the CE/RE
pocket (0.15 mm, beside the RC). The drag magnet passes none of them; beads follow the field maximum, not the flow
[assessment]. They are the reason for the allocation "≤ 10 beads per run at J and WLc" (§8.3) and for whole-path imaging
in M1.

### 2.7 Electrode die: orientation, contacts, seal, gap, shielding (docs/15 A2)

* **Orientation.** The die lies face-down on the channel sheet in the die window of L3/L2, long axis along y (x 55.0–61.0,
  y 23.35–33.35). Its lower face carries, from −y to +y: the CE/RE pocket electrodes at the edge, WE1 over the RC with
  two 0.4 mm fingers along the in-die lane segments (G3 side 0.5 mm, G4 side 0.65 mm), WE2 over the 50 µm channel, then
  ≥ 3.8 mm of passivated glass, then **six pads at y 30.0–33.0**.
* **Seal.** The 25 µm L1b film, cut with the L1 pattern, bonds the die to the sheet everywhere except the wetted
  features; the pads lie outside the film over a **dry contact window** cut through L1 and L0 (x 55.3–60.7, y
  29.8–33.2), separated from the nearest wetted edge by ≥ 3.8 mm of bonded film.
* **Contact route.** Gold-plated spring pins rise from below through the contact window onto the pads (same side they
  face). Their force (6 pins, value UNVERIFIED) is reacted by a compliant pad in the lid pressing on the die back, so the
  bond line is not peeled. The electrode bay below the window is outside every magnet path (§2.2 zoning).
* **Gap definition.** Cell height = L1 (0.175 mm) + L1b (0.025 mm) = 0.200 mm; tolerance UNVERIFIED (±10 % would change
  τ by ±21 %; collection in a 60-s window 0.97 → 0.95, calibrated per lot; §9). The die is located on two moulded datum
  edges of the L3 window (±0.05 mm, UNVERIFIED), not by the adhesive. The cell height of each card is measured at
  docking from the PE1 current decay (τ = 4h²/(π²D), §3.5.2).
* **Shielding and leakage.** The electrode bay is a grounded metal enclosure with the pogo block, separated from the
  magnet bay by a grounded wall; shielded leads ≤ 0.3 m to the Gamry cell cable; the lid above the die is grounded metal.
  Leakage requirement ≥ 5×10¹² Ω from any pad to WE (≤ 0.1 pA at 0.5 V, Derived); the bay is at 25 °C, ≥ 35 mm from the
  cold zone, with its own RH sensor (dew-point margin logged, §6.6).
* **Catalogue route for M5a.** The same arrangement (die face-down on a laser-cut sheet + film, pogo pins from below
  through a window) is used with a catalogue Micrux die in M5a, so the contact route is tested before any custom die.

---
## 3. Functional units

### 3.1 Sample reception and metering of the dispersed plug

* **Volume and flow.** Empower method per line: A1 at 100 µL/min for 1.5 min into IC_k (V_k open, V3 closed): 150 µL =
  1.5 loop volumes, analyte transfer 0.90 (docs/09 §1.2; loop ID 0.5 mm UNVERIFIED). The chamber then holds 150 µL +
  10 µL beads + 4 µL bead chase + 10 µL conjugate + 3 µL conjugate chase + 3 µL post-transfer chase + 5.3 µL of parked
  BSM flow (1 µL/min for 3.45 min before and 1.85 min after the transfer, §7.1) = **185 µL**. Capture gain vs gen-1
  (0.90/1.85)/(0.96/2.2) = **×1.11** (Derived as docs/12 §2.2). Conjugate stock for 0.3 nM in 185 µL from 10 µL:
  **5.6 nM** (docs/15 N1).
* **docs/09 F1 relaxed, recorded (docs/15 W8).** F1 asks to capture ≥ 96 % of the injected analyte; A transfers 0.90 by
  design, trading 6 % of the analyte for a 1.5 instead of 2.2 dilution (net ×1.11 capture rate). The model now uses the
  real dilution /1.85 (Revision A used /1.7, ≈ 0.009 in P too optimistic, §1.3 step 1).
* **Metering** is by time × BSM flow (`hw.bsm.flow_accuracy`, `hw.bsm.flow_precision_rsd_low_flow`, UNVERIFIED at low flow);
  a 1 % volume error changes the dilution by ≈ 0.9 %, identically for calibrators and samples; gravimetric check in C1.
* **Hydraulics.** Inlet path M_in + C_k ≈ 15 mm of 0.5 × 0.175 mm: R = 12ηL/(w h³(1 − 0.63 h/w)) = 12 × 0.89×10⁻³ ×
  0.015 / (5×10⁻⁴ × 5.36×10⁻¹² × 0.78) = 7.7×10¹⁰ Pa·s/m³ → **0.13 kPa at 100 µL/min** (Derived; η 0.89 mPa·s). The
  chamber is vented; the BSM back-pressure question is unchanged from gen-1 (docs/08 §10).
* **Line flush (D13) with the switch moved.** At 1.5 min the BSM steps to 1 µL/min (no card valve moves: the previous
  run's PE2 is still running, §7.2); at 3.35 min V_k closes and V3 opens; the BSM runs 100 µL/min to the bypass for 2.0 min
  (200 µL; the loop has then seen 352 µL = 3.5 loop volumes, > 0.997 out, docs/09 §1.2); **Loop Offline at 5.4 min**
  (`hw.smfl.loop_offline_supported`), then parked at 1 µL/min. Without the flush the line + manifold (3.8 + 1.05 µL) would
  carry ≈ 0.12 C₀ into the next chamber: 4.9 × 0.12 / 100 = **6×10⁻³** (Derived as Revision A). A1 from the BSM per
  determination ≈ 150 + 1.85 + 200 + 25.6 ≈ **0.38 mL**.
* **C_k chase.** At 3.40–3.55 min S_A pushes 3 µL A1 through V17/V18 into C_k, so the inlet channel holds clean A1 until
  the next delivery (≈ 11 channel volumes of 0.26 µL). Every delivery into the chamber (beads, conjugate, sample) and the
  last step of every cleaning ends with such a chase (carry-over arithmetic §8.3).
* **Adsorption.** Sample-contact area: inlet ≈ 2 × 15 × (0.5 + 0.175) = 20 mm² + chamber 143 mm². Perfect-sink upper bound
  (Derived): k_m = D/δ = 3.9×10⁻¹¹ m²/s (`chem.analyte` IgG diffusion coefficient) / 100 µm = 3.9×10⁻⁷ m/s; k_m·A/V =
  3.9×10⁻⁷ × 1.63×10⁻⁴ / 1.85×10⁻⁷ = 3.4×10⁻⁴ s⁻¹ → 44 % lost in 28.5 min. Real loss on blocked COC is far lower but
  **unmeasured** — mock-up M2 (spike recovery vs a LoBind tube). Same issue in the gen-1 cup; not credited by the model.

### 3.2 Stirred incubation chambers IC1, IC2

**3.2.1 Geometry.** Ø 8.0 mm bore through L3, L2 and L1 (≈ 6.1 mm high), floor = foil, 185 µL working (fill height
3.68 mm), PTFE vent in the roof; tangential tidal nozzle at the far (−x) wall; throat funnel (in L1, open above) and the
wash-lane entrance on the +x wall; swept inlet channel C_k on the side wall. Centres 26 mm apart (R6).

**3.2.2 Mixing.** Dock syringe S_IC_k (1 mL, A1 working fluid) behind the open floor valve V9/V10 aspirates 50 µL into a
60 µL FEP coil on the dock side and dispenses it back every 30 s, 2 s per half-stroke.
* Jet (Derived): 25 µL/s through 0.5 × 0.175 mm → 0.29 m/s; hydraulic diameter 0.26 mm; Re = 1000 × 0.29 × 2.6×10⁻⁴ /
  0.89×10⁻³ = **83**; tangential entry sets the chamber swirling [assessment; not computed].
* **Pauses:** tidal strokes stop during every read window of every run (§7.2): 6.35 of 28.5 min (the previous run's PE2
  at 1.5–3.35 and its READ at 21.5–26.0, guards included) → **22.15 min stirred**. In a 4.5-min pause beads settle 7 mm/h ×
  4.5 min = 0.53 mm of the 3.68 mm column (`ma.capture.in_vial_unstirred_rate_factor` note). The model counts paused
  minutes at the repository's unstirred factor 0.5 (UNVERIFIED): effective 25.33 min (§1.3; 0 instead of 0.5: P 0.139;
  no pauses: 0.164).
* Beads entering the nozzle need 0.175 mm / 7 mm/h = 1.5 min to settle there, ≫ 2 s; the 50 µL stroke stays in the
  coil, so beads and conjugate never reach the syringe.
* Capture factor relative to a well-mixed tube: **UNVERIFIED** (model samples 0.2–1.0, /1.85) — the most important
  unmeasured chamber property (docs/08 §10.2; docs/12 risk A2); M2 measures it with the pause pattern of §7.1.

**3.2.3 Full drain.** S_IC_k pulls the chamber through the nozzle at 500 µL/min to its waste port. Residual: wetted area
143 mm² × film 10–30 µm (UNVERIFIED) = 1.4–4.3 µL + meniscus → **≤ 5 µL** design assumption (docs/12 §3.8). Full drains
are used only in the cleaning (§3.2.6), never while a pellet is in the chamber (§3.4).

**3.2.4 Bubbles.** Liquids enter at floor level below the meniscus; air leaves through the PTFE vent; conjugate arrives by
air push into the vented chamber. Vent wet-out by 0.05 % Tween + 1 % BSA: UNVERIFIED (§9 FM8, M3).

**3.2.5 Wall area and NSB.** Conjugate-exposed IC wall 143 mm² — **not in the product path**; it enters only through
analyte loss (§3.1), free conjugate carried with the pellet (§3.4) and desorption into the next incubation of the same
chamber 62 min later (allocated in §8.3). Beads: 5×10⁵ × π(2.8 µm)² = **12.3 mm²** (docs/12 §3.8), factor 1
(`ma.nsb.surface_factor_magnetic_beads`), exposure 0.3 nM × ≈ 34 min — this carries the blank.

**3.2.6 Cleaning** (after the drag and the WL refresh, 42.35–49.85 min): full drain; **6** × (150 µL A1 via C_k at
500 µL/min, 2 tidal strokes, full drain); before the last drain a 3 µL bead-port chase (S_b, A1, via V4/V5) and a 3 µL
C_k chase (S_A). Liquid and loose-bead residue: (5/155)⁶ = **1.1×10⁻⁹** of what the chamber held after the drag (Derived;
three rinses would give 3.4×10⁻⁵), on top of the 6.6×10³ dilution of the wash (§3.4). Six rinses are the **default**, so
that the post-high cleaning of §7.4 needs no decision before the result is known (the result of run n arrives after
chamber k has been cleaned); 7.5 min fit the chamber's idle time with 7.15 min to spare (§7.1); cost ≈ 0.45 mL A1 per run.

### 3.3 Bead capture, gather and magnet-dragged transfer

**3.3.1 Magnets and actuators.**

| Magnet | Size, grade | Position | Motion | Fail-safe |
|---|---|---|---|---|
| M_c,1, M_c,2 collection | NdFeB 10 × 10 × 5 mm, magnetised through 5 mm, B_r ≈ 1.3 T (N42 class, UNVERIFIED) | fixed X–Y under each chamber centre, in window W_k | **Z only**, ≥ 25 mm stroke | spring-up (on) |
| M_d drag / gather | NdFeB 2 × 2 × 4 mm, along 4 mm | on a post of an X–Y–Z carriage below the anvil; rises through windows and the slot | X–Y path following, Z ≥ 8 mm | spring-up |
| M_h hold | NdFeB 3 × 3 × 4 mm (size UNVERIFIED) | fixed under the RC centre | Z only | spring-up (pellet held) |
| M_w bead waste | NdFeB 3 × 3 × 3 mm | fixed in the anvil under BW | none | permanent |

M_c and M_d are separate units, so the hand-over is "M_c,k down, then M_d up" (docs/15 S7b) and M_c,k can never pass
under the other chamber (S7).

**3.3.2 Field and force arithmetic** (Derived, scratch `mag_b.py`: surface-charge integration of uniformly magnetised
blocks, B_r 1.3 T; bead moment m = 1.15×10⁻¹³ A·m² from an assumed saturation magnetisation of 1×10⁴ A/m, **UNVERIFIED**,
docs/15 N8; F = m∇|B|; Stokes 6πηr = 2.35×10⁻⁸ N·s/m; wall factor 3 for a bead on the floor, UNVERIFIED; buoyant weight
0.046 pN from the repository settling velocity). The point values reproduce docs/15 `rev15/mag.py`.

| Situation | field magnitude (T) | gradient (T/m) | Force (pN) | Consequence |
|---|---|---|---|---|
| M_c,k up, bead at the fill top above the centre (3.7 mm above the face) | 0.187 | 49 vertical | 5.6 | 0.24 mm/s → floor in ≈ 15 s (150 s at a 10× weaker moment); collection lasts 4.1 min |
| M_d edge, bead on the floor (0.30 mm) | 0.378 | 377 lateral, 636 vertical | **43 lateral**, 73 vertical | v_max = 43/(3 × 2.35×10⁻⁸) = **0.61 mm/s**; drag at 0.20 mm/s (3.0× margin), gather at 0.30 mm/s (2.0×) |
| M_d, bead 1.5 / 2.0 / 2.5 mm from the centre | 0.19 / 0.10 / 0.06 | 263 / 113 / 57 lateral | 30 / 13 / 6.5 | wide capture zone (next row) |
| **Gather capture half-width** (2-D trajectories, magnet moving +x, friction μ·F_z with μ = 0 / 0.2 / 0.4) | — | — | — | **≥ 2.8 / 2.8 / 2.7 mm at 0.30 mm/s; ≥ 3.0 mm at 0.20 mm/s** (grid limit 3.5 mm) |
| M_c,k lowered by 10 / 15 / 20 / **25** / 30 mm, chamber floor | 0.039 / 0.016 / 0.008 / 0.0046 / 0.0028 | — | 0.91 / 0.29 / 0.12 / **0.055** / 0.029 | stroke ≥ 25 mm to stay near the buoyant weight (saturated-moment upper bound; at 5 mT the bead is far from saturation, real force lower, UNVERIFIED) |
| M_c,k up, beads of the **other** chamber 12 / 16 / 22 mm away | — | — | 1.0 / 0.31 / **0.083** | Revision A spacing (12 mm) pulled 22× the buoyant weight; with 26 mm centres (22 mm) 1.8× for 4.1 min = ≤ 0.9 mm drift at 3.5 µm/s, against mm/s swirl [assessment], identical every run |
| M_d up in chamber k, other chamber 6 / 8 mm away; M_d lowered 8 mm directly below a bead | — | — | 0.35 / 0.12; 0.11 | transit rule: lowered ≥ 8 mm and ≥ 6 mm laterally from an incubating chamber |

Docs/15 found the lateral gradient just outside the M_c edge at ≈ 365 T/m (not 64): irrelevant now, because M_c no longer
gathers. **Bead–foil friction/adhesion decides whether beads follow at all** (vertical force 1.7× the lateral at the M_d
edge; no value for blocked COC with Tween exists) — M1 measures follow speed and immobile fraction directly.

**3.3.3 Sequence and times** (t from the run's Inject Start):

| t (min) | Action | Motion |
|---|---|---|
| 30.0 | collection: M_c,k up (static from 30.1; PE2 of the RC runs 30.1–34.1 in parallel) | Z |
| 34.1 | M_c,k down 25 mm (beads stay on the floor, mostly at the wall foot, docs/15 S7) | Z |
| 34.2–36.2 | **gather:** M_d up at (x_c − 3.5, +2); pass 1 to the funnel mouth (x_c + 2.5, 0) at 0.30 mm/s (6.3 mm, 21 s); M_d down 8 mm, back to (x_c − 3.5, −2), up; pass 2; pass 3 along y = 0; M_d stays at the funnel mouth | X–Y–Z |
| 36.2–39.5 | partial-drain rinses (§3.4), M_d holding | — |
| 39.5–41.75 | **drag:** G_k, G3 open; 23.3 mm at 0.20 mm/s (116.5 s) along funnel → WL_k → J → WLc → RC centre; M_d down and away, M_h up (pellet unheld ≈ 2 s); G3 closed, then G_k (0.25 min for gates and hand-over) | X–Y path following the lane centre line |
| 41.75 | accumulation starts; carriage free | — |
| 41.75–42.35 | WL_k refresh J → IC_k, then WLc → V12 (§3.3.6) | — |
| 56.75–57.15 | **bead-out:** M_h down, M_d up under the RC, G4 open, 4.5 mm at 0.20 mm/s into BW (22.5 s), M_d down (M_w holds) | X–Y–Z |

Transfer block 30.0 → 41.75 = 11.75 min, of which 4.1 min overlap PE2 (Revision A: 8.25 min, ≈ 8.9 after the docs/15 S4 corrections).

**3.3.4 Bead loss budget (targets, UNVERIFIED until M1).** Collection ≥ 0.99, gather ≥ 0.99 (three passes, capture zone
≥ 2.7 mm), drag ≥ 0.97 (Wang2013 > 0.95 at 0.7 mm/s; its bead type is not in the abstract, so its speed is not
transferred to M-280), arrival and hold ≥ 0.995 → **≥ 0.95 overall, run-to-run CV ≤ 5 %** (docs/15 W2). A constant
transfer barely matters for the LOD (0.80: P 0.151 vs 0.150) because the NSB rides on the same beads; a variable transfer
acts as a dose CV (CV 0.10: P 0.124).

**3.3.5 Where lost beads go.**
* Not collected or not gathered (in IC_k): removed by the cleaning (1.1×10⁻⁹ of the post-drag content, §3.2.6).
* Stranded in WL_k: pushed into IC_k by the refresh of the **same** run right after the drag, before the cleaning (§3.3.6);
  nothing stranded in WL_k can reach a later incubation (docs/15 S5).
* Stranded at J, in WLc or in the G_k′/V11/V12 stubs: the WLc refresh flushes WLc to waste; beads at J or in stubs that
  the flow does not reach can be collected by the next run's drag (other chamber) → allocated **≤ 10 beads per run =
  2×10⁻⁵** (§8.3), counted by whole-path imaging in M1.
* Left in the RC after bead-out: measured every run by the PE2 monitor (§3.6), allocated ≤ 10 beads.

**3.3.6 Wash-lane refresh.** 41.75–42.35 min: S_A → P_a → V11 → WLc tee → J → G_k (open) → WL_k → IC_k (5 µL at
20 µL/min), then G_k closed, V12 open: V11 → WLc → V12 → waste (5 µL). Floor speed of a bead in the lane at 20 µL/min:
mean 3.8 mm/s, at 1.4 µm height ≈ 6 ū z/h = 0.18 mm/s → drag ≈ 7 pN ≫ the buoyant weight (Derived) — loose beads move,
stuck ones stay and are what M1 counts.

### 3.4 Wash (pellet held at the funnel mouth, 36.2–39.5 min)

* **Partial-drain rinses:** S_IC_k pulls 155 µL (185 → 30 µL) at 500 µL/min; then 6 × (S_A fills 100 µL through C_k at
  500 µL/min; S_IC_k pulls 100 µL), the sixth fill staying as the 130 µL drag medium: 0.31 + 11 × 0.2 + 11 × 0.07
  switching ≈ **3.3 min**. The chamber never holds less than 30 µL (mean depth 0.6 mm over 50.3 mm², deeper at the wall
  where the pellet sits), so the pellet never meets an air–liquid interface (Revision A drained to ≤ 5 µL with the pellet
  in the chamber) [assessment; filmed in M1].
* **Dilution:** (30 + 100)/30 = 4.33 per fill, 4.33⁶ = **6.6×10³**; free conjugate in the drag medium 0.3 nM / 6.6×10³ =
  45 fM × 130 µL = **3.5×10⁶ molecules**; carried with the pellet at Wang2013's small-molecule carry-over 2×10⁻⁵ of the
  source content (protein UNVERIFIED) → **≈ 71 molecules** in the RC, 1.2 % of the ≈ 5700 NSB enzymes of the nominal
  blank (docs/12 "A0") (Derived).
* **Clean and dirty paths are separate (docs/15 S6):** fills come only from S_A (dispense only, never aspirates from the
  card); drains go through the nozzle and the dock coil into S_IC_k and out of its waste port; no liquid returns from the
  coil during washing (tidal strokes are off). Revision A delivered the rinse through the coil, so the first 60 µL of
  each rinse was the coil's incubation liquid (Derived) — eliminated.
* Wash minima of docs/09 C11: post-capture wash ≥ 1 min (3.3 min), ≥ 50 accumulation-zone volumes (600 µL / 1.34 µL = 450).

### 3.5 Readout cell and electrodes

**3.5.1 Geometry.** Cell 1.34 µL (RC 2.6 × 2.0 × 0.200 mm = 1.04 µL, lane fingers 0.115 µL, RC → WE2 link and WE2 channel
0.175 µL, §2.3). WE1 Au 2.5 × 1.9 mm plus two 0.4 mm fingers (0.6 mm²) = **5.35 mm²**; WE2 Au 1.0 × 2.0 mm = 2.0 mm²,
switched in parallel with WE1 during PE1, PE2 and the read (dock relay) so that the WE2 channel is electrolysed and read
too; alone in the fallback. CE/RE in the pocket behind the short wide neck (§2.3). Contact-check loop: two pads joined by
a 50 µm Au line. Passivation SU-8 or polyimide (MICRUX_TF).

**3.5.2 Exhaustive collection (Derived).** For a layer of height h with the WE at z = h, insulating floor and uniform
initial product, F(t) = 1 − Σₙ 8/((2n+1)²π²)·exp(−(2n+1)² t/τ), τ = 4h²/(π²D). h = 0.200 mm, D_HQ = 9×10⁻¹⁰ m²/s
(`chem.substrates.HQ.diffusion_coefficient`, 7–11×10⁻¹⁰): **τ = 18.0 s**; one 60-s window collects F(60) = 1 −
0.811 e⁻³·³³ = **0.971**. The **weight of accumulated product in Q_net = Q_a − 2Q_b + Q_c is 0.916** (D 9×10⁻¹⁰), 0.829
(7×10⁻¹⁰), 0.959 (1.1×10⁻⁹) (finite differences incl. the 15-s rests, scratch `read_b.py`) — constant, calibrated per
lot, and temperature-controlled (D depends on T; ±0.2 °C). WE2 channel (50 µm): τ = 1.1 s. Lane-finger rims (50 µm):
2.8 s. Pocket exchange 0.010 s⁻¹ (τ 100 s): product that entered it during accumulation returns partly within the read
(constant, calibrated). The cell height of each card is read from the PE1 current decay.

**3.5.3 Charge at 1 pg/mL and in the blank (Derived).** 5708 specific enzymes at 1 pg/mL (docs/12 "A0", 30-min
incubation; fewer with 25.3 min — the model accounts for that) × k_cat 1000 s⁻¹
(`chem.enzymes.alp.kcat_conjugate_assay_conditions`) × S/(K_m + S) = 3/3.1 = 0.968 (`ma.chemistries.alp_hqdp.Km`,
UNVERIFIED) × 660 s = 3.65×10⁹ HQ × 2e = **1.17 nC** (× 0.95 transfer × 0.916 read weight ≈ 1.02 nC). The nominal blank
carries ≈ 5700 NSB enzymes → ≈ 1.2 nC; with blank CV 0.10 (`chem.nsb.blank_CV_analog_electrochemical`) **SD_blank ≈
0.12 nC**. Hydrolysis during accumulation: 10⁻¹⁰ s⁻¹ × 660 s × 3 mM × 1.34 µL × 2F = **0.051 nC** (0.51 nC at the
acceptance limit 10⁻⁹ s⁻¹; a blank offset not removed by pre-electrolysis). Lot free HQ in a fresh fill: 10⁻⁵
(`ma.chemistries.alp_hqdp.free_product_impurity`) × 3 mM × 1.34 µL × 2F = **7.8 nC**, 6.6× the 1 pg/mL signal.

**3.5.4 Read background and drift — the design driver (docs/15 S2).**

*Charging.* Q_dl = C_dl·A·ΔE = 20 µF/cm² (UNVERIFIED, note of `hw.gamry.noise_capacitive_per_uV_per_uF`) × 0.0735 cm² ×
0.15 V = **0.22 µC** per step; peak ΔE/R_u = 0.15 V / 14 kΩ = 11 µA, decaying with R_u·C = 21 ms. Identical steps cancel
in any difference scheme; what does not cancel is drift.

*Why the Revision A pair fails.* With a linear background drift d, two equal windows T apart by Δ differ by d·Δ·T. At the
repository's drift `hw.gamry.baseline_drift` 5 pA/min (1–10, UNVERIFIED): **0.79 nC** for 90/105 s, 0.37 nC for 60/75 s —
8–16× the 0.05 nC target (docs/15 S2 reproduced).

*Revision B read (R1).* Cell on at E_rest for 30 s (pre-rest, not integrated); **a**: E_det 60 s; E_rest 15 s; **b**: E_det
60 s; E_rest 15 s; **c**: E_det 60 s; cell off. Total **4.0 min**. **Q_net = Q_a − 2Q_b + Q_c** (fixed, identical
integration windows; the first 0.5 s of each window on a µA range, then the same nA range in every window, so a range
offset enters all windows equally).
* Constant offset (incl. a steady faradaic background and range offsets): cancels exactly (1 − 2 + 1 = 0).
* Linear drift: cancels exactly. Curvature d₂ leaves d₂·Δ²·T = d₂ × 337 500 s³ (Δ = 75 s, T = 60 s). For ≤ 0.025 nC
  (half the target): **d₂ ≤ 7.4×10⁻¹⁷ A/s² = 0.27 pA/min²**, i.e. a 5 pA/min drift must hold its rate for a time
  constant ≥ 19 min (Derived, `read_b.py`). This is the drift requirement M5a tests.
* Constant enzyme turnover during the read (docs/15 N3): contributes −0.9 % of the accumulated product (Revision A's pair:
  −2.8 %) — calibrated.
* White noise: SD(Q_net) = √6 × i·√(T/2B) = **13.4 s × i** (B = 1 Hz) → **SD(Q_net) ≤ 0.05 nC needs ≤ 3.7 pA rms**
  (Revision A's pair at 90 s would have allowed 5.3 pA; the price of drift immunity is √3 in white noise).
* E_rest segments: E_rest is chosen (CV in M5a) so that a 30-s hold at E_rest on 100 nM HQ collects ≤ 1 % of Q_a; the
  rests are then excluded from Q_net and logged as a diagnostic (docs/15 S2, last point).
* E_det is the lowest potential on the HQ diffusion plateau on Au at pH 9.5 (CV on the die, docs/09 C16); Pt is not
  used for WE1 (earlier oxide formation [assessment]).

*Requirement.* **SD(Q_net) ≤ 0.05 nC** on blank fills with all dock activity in its planned state (§7.2); it adds
(0.05/0.12)² = 17 % to the blank variance and costs 0.013 in P (§1.3: 0.141 vs 0.154). At 0.155 nC P is 0.097.

**3.5.5 Reference and counter electrode strategy.**
* The pocket sees only substrate: every flush enters through it (V15 → pocket → neck → RC). Substrate recipe with fixed
  chloride: 0.1 M Tris pH 9.5, 1 mM MgCl₂, **50 mM NaCl** (value set here; its effect on ALP UNVERIFIED — an E1.7-type
  activity check; docs/15 W6).
* **R-a (preferred if offered): thin-film Ag/AgCl** — not in the Micrux custom offer (Au/Pt only, MICRUX_TF); IMT lists
  Au, Pt, ITO, Ti (IMT_FLYER) → UNVERIFIED; best drift found < 2 mV over 26 days (GO-coated, constant medium;
  Kim2015 (Sensors), doi:10.3390/s150306469).
* **R-b (baseline): Au quasi-reference** (Micrux dies carry Au RE and CE, PALMSENS_IDA). A linear QRE drift between windows
  is cancelled by the three-window read like any linear drift. Targets (own, UNVERIFIED): ≤ 20 mV over 8 h and ≤ 2 mV
  between windows a and c. **Open (docs/15 W5):** PE converts HQ → BQ near the pocket and the CE reduces BQ or O₂, so the
  pocket's redox state changes within a run; logged against a docked salt-bridge Ag/AgCl in M5a (e).
* **CE charge (docs/15 N2):** 7 forward steps per run (PE1 1, PE2 3, READ 3) × 0.22 µC ≈ **1.5 µC per direction**, ≤ 16 pmol
  in 0.044 µL ≈ 0.36 mM; Tris at pH 9.5 (≈ 4 % protonated, pKa ≈ 8.1 UNVERIFIED) buffers ≈ 2.3 × 0.1 M × 0.04 × 0.96 ≈
  9 mM/pH → ΔpH ≤ 0.04 per direction, partly reversed by the return steps; flushed every run (Derived).
* BQ redox cycling through the short neck: the neck mouth (0.4 mm) is ≈ 4 % of the RC perimeter (9.2 mm) and BQ needs
  (0.3 mm)²/D ≈ 100 s to reach the CE → a small, constant amplification, calibrated [assessment].
* Uncompensated resistance: κ ≈ 0.1–0.2 S/m without NaCl (docs/15 W6), + ≈ 0.5 S/m from 50 mM NaCl (molar conductivity
  ≈ 10.7 mS·m²/mol, UNVERIFIED) → ≈ 0.6 S/m; neck 0.15×10⁻³ / (0.6 × 8×10⁻⁸) = 3.1 kΩ + spreading ≈ 11 kΩ (Revision A's
  4 kΩ at 1.6 S/m, scaled) → **R_u ≈ 14 kΩ**, R_u·C = 14 kΩ × 1.47 µF = **21 ms** (without NaCl ≈ 55 kΩ, 81 ms); both
  ≪ τ = 18 s; iR at nA currents < 0.1 mV (Derived).

**3.5.6 Model check.** Cell 1.34 µL at 3 mM: ULOQ 6813 pg/mL nominal (§1.3); 3 mM stays a requirement (Revision A: 1360
at 1 mM with 1 µL).

**3.5.7 Fallback read mode R-flow (WE2) — without pre-electrolysis (docs/15 S8 iv).** If M5a/M5 fail the step-read
acceptance: PE1 and the removal function of PE2 are dropped, so the cell keeps the same un-electrolysed substrate as the
sweep supply; after accumulation the cell is swept with fresh substrate (RS → V15 → pocket → RC → WE2 → V14 → P_s,
S_RC) at 10 µL/min over WE2 at E_det, with 0.5-min baselines before and after at the same flow (gen-1 rule, docs/08 W5).
Baseline and plug then carry the same substrate — no mismatch — but the lot free HQ and the hydrolysis growth of the 25 °C
tank appear as a referenced, drifting baseline exactly as in gen-1: **the R-flow mode is the no-credit case of §1.3**.
The pre-drag carry-over check becomes a flow check of the cell content in the PE2 slot. Costs: conversion < 1 (gen-1
thin-layer 0.78 at 10 µL/min, docs/09 §5.2; this 1 × 2 mm, 50 µm channel not computed), +10 µL substrate per run (RS fill
0.75 mL), V14/V15 cycles double (§4). If R-flow becomes routine, RS should move to the cold zone with a warm-up path
(bubble risk, D8) — open.

### 3.6 Pre-electrolysis (UNVERIFIED pending docs/06 E1.2b and M5a)

* **What is electrolysed in place** (docs/15 S8 correction): the whole 1.34 µL cell (WE1 + fingers + WE2 in parallel);
  stubs and the pocket only by exchange with the cell. Nothing is pre-electrolysed outside the card.
* **Sequence** (own-run times): flush ends 26.65 (= 57.65 of the previous run); **PE1** 26.65–27.65 (15 s E_rest, 45 s
  E_det; removes F(45 s) = 93 % of the cell's free HQ; not a measurement, no quiet requirement); open-circuit **hold**
  until 30.6 (2.95 min incl. the PE2 pre-rest); **PE2** 30.1–34.1 = three-window read: Q_mon = Q_a − 2Q_b + Q_c measures
  what accumulated during the hold and removes it; it is the last removal before the drag (39.5). A second-difference
  read cancels constant turnover, so the monitor sees only product made *before* window a — hence PE1 and the hold
  (Revision A's PE2 pair would have been blind to it under R1).
* **Escape** (Derived, scratch `escape_b3.py`; method of docs/15 `rev15/escape.py`: 1-D dead-end diffusion, c = 1 in every
  stub at the flush, sink at the cell mouth until the end of PE2, flux counted from 34.10 to the READ at 52.75):

| Source | Geometry | Escape, D = 9×10⁻¹⁰ | Escape, D = 7×10⁻¹⁰ |
|---|---|---|---|
| G3 stub | 0.5 mm × 0.5 × 0.175 mm (holds drag A1 — c = 1 is conservative) | 0.05 % | 0.12 % |
| G4 stub | 0.5 mm × 0.5 × 0.175 mm | 0.05 % | 0.12 % |
| V14 stub behind WE2 | 0.5 mm × 0.3 × 0.175 mm | 0.03 % | 0.07 % |
| neck + pocket + V15 stub | 0.4 × 0.2 × 0.15 mm + 0.032 µL + 0.016 µL | 0.07 % | 0.17 % |
| **Total** | | **0.20 %** | **0.49 %** |
| sensitivity: all stubs 1.0 mm | | 4.8 % | 5.6 % |
| sensitivity: Revision A pocket (neck 0.2 × 0.2 × 0.5 mm, 0.074 µL) | | 2.8 % | 2.6 % |

  The model credit stays ×0.01 (≥ 2× the computed escape); **the credit holds only if every stub is ≤ 0.5 mm and the
  pocket is fast** — at 1-mm stubs the S4a rescue collapses (P 0.171 → 0.056, §1.3). M5a and M5 acceptance: escape ≤ 1 %.
* **PE2 as carry-over monitor:** 10⁻⁴ of a 10 ng/mL sample's enzymes (≈ 5700, linear upper estimate, docs/12 §3.8) × 968 s⁻¹
  × 177 s × 2e = **0.31 nC** (Derived). Threshold **0.15 nC above the card's running median of Q_mon** (3 × 0.05 nC; the
  median absorbs the lot- and age-dependent HQ that returns from the stubs after PE1 and the hydrolysis during the hold) →
  detects residual activity ≥ 4.8×10⁻⁵ of a 10 ng/mL sample (≈ 0.5 pg/mL-equivalent in the next read). Above threshold:
  the run is flagged invalid (there is no time for an extra flush before its drag), an extra RC + BW flush follows its
  read; two in a row → fault latch.
* E1.2b decides at G1 whether the guard principle works (docs/06 §4); the cartridge keeps PE1/PE2 regardless, because PE2
  is the monitor. Under E1.2b INTERMEDIATE/FAIL the headline (no credit) stands and 3 mM is re-checked (docs/15 S8).

### 3.7 Waste

* No liquid waste is stored on the card except spent beads in BW. Liquid leaves through P_byp, the IC drains (S_IC_k waste
  ports), P_wo and P_s into one dock waste bottle (≥ 1 L, level sensor) through air-gapped lines.
* Per determination (Derived): BSM A1 0.38 mL; dock A1: rinses 600 + cleaning 900 + chases 10 + WL refresh 10 µL ≈
  1.52 mL; substrate 20 µL (+ 10 µL fallback) → **≈ 1.9 mL** (Revision A 0.94; gen-1 ≈ 5–6 mL, docs/09 §3.6); ≈ 27 mL
  per 14-run card plus docking.
* Beads: ≤ 16 doses × 5×10⁵ = 8×10⁶ beads × 11.5 µm³ = 0.09 µL in the 3.6 µL BW, held by M_w.

### 3.8 Bead-waste pocket and cell flush

After bead-out (56.75–57.15), G4 stays open and S_RC pulls 20 µL at 40 µL/min: RS → V15 → pocket → neck → RC → G4 → BW →
V16 → P_s (57.15–57.65). M_w holds the spent beads against a mean 0.46 mm/s through 2.5 × 0.575 mm [assessment; M1].
Closing order V16, G4, then V15. Spent beads keep making HQ in BW; G4 next opens only after the next READ, so that HQ
cannot reach a read; it reaches the cell only through a leaking G4 (M4 requirement). PE1 follows at 57.65.

---
## 4. Valve map

All 21 valves and gates are **flat-floor TPE-ceiling valves** of one type (§2.1): open when not pressed, closed by a
plunger pressing the TPE onto the foil. Plungers are **spring-closed, solenoid-opened** (fail-closed) except V3, which is
**spring-open** (fail-open) so that the BSM, which keeps pumping when the dock loses power, always reaches the bypass
(a dead-ended BSM would exceed the card's ≈ 3 bar class, CS_1367, long before its own 18 000 psi limit,
`hw.bsm.pressure_max_to_1mLmin`; the Empower pressure-limit setting is UNVERIFIED). G1–G4, V11, V12 sit over or at the
drag slot: plunger force ≤ 1.5 N (§2.1). V13 of Revision A is deleted (the substrate enters through the CE/RE pocket via
V15); V17/V18 are new.

Cycle = close → open → close. Per card = 14 runs + 2 recovery cycles + 1 docking prime (shared valves 17 uses; each
chamber valve 7 own runs + 3).

| ID | De-energised | Isolates / function | Open during (t from the Inject Start of its run) | Cycles per run | Cycles per card |
|---|---|---|---|---|---|
| V1, V2 | closed | M_in → C_1 / C_2 (sample) | −3.45 → 3.35 (own chamber) | 1 | 10 each |
| V3 | **open** | M_in → bypass | always except −3.45 → 3.35 of any run | 1 | 17 |
| V4, V5 | closed | bead port → C_k | −5.0 → −4.0 (dose + 4 µL chase); cleaning chase ≈ 49 | 2 | 17 each |
| V6, V7 | closed | meter MC → C_k | −4.0 → −3.5 | 1 | 10 each |
| V8 | closed | conjugate tank RCj → MC | −10.0 → −9.5 (fill-to-vent) | 1 | 17 |
| V9, V10 | closed | IC_k nozzle ↔ dock coil ↔ S_IC_k | 3.4 → 49.85 (tidal, rinses, drag, cleaning) | 1 | 10 each |
| V11 | closed | S_A → WLc tee (WL refresh) | 41.75 → 42.35 | 1 | 17 |
| V12 | closed | WLc tee → P_wo | 42.05 → 42.35 | 1 | 17 |
| V14 | closed | WE2 channel → P_s | docking prime only (fallback: sweep) | 0 (1) | 3 (17) |
| V15 | closed | RS → CE/RE pocket → cell (substrate inlet) | 57.15 → 57.65 (flush) (fallback: + sweep) | 1 (2) | 17 (**31**) |
| V16 | closed | BW → P_s | 57.15 → 57.65 | 1 | 17 |
| V17, V18 | closed | S_A → C_k (chases, rinses, cleaning) | −3.5 → 3.55; 36.2 → 49.85 | 2 | 17 each |
| G1, G2 | closed | WL_k ↔ J | 39.5 → 42.05 (drag, then WL refresh) | 1 | 10 each |
| G3 | closed | WLc ↔ cell | 39.5 → 41.7 | 1 | 17 |
| G4 | closed | cell ↔ BW | 56.75 → 57.65 (bead-out, flush) | 1 | 17 |

**Totals (Derived):** 16 cycles per run (18 in the fallback mode); ≈ 270 per card; **busiest valve 17 cycles per card
(V15 31 in the fallback)** — Revision A: 18 per run, 360, busiest 40 (60). Evidence for endurance: **none for TPE on COC**.
CHILDERS2024 shows eCOC membranes on PC/PETG "reproducibly actuated > 50 times without failure" (a different material
pair); CS_1367 is a single-use foil valve (docs/15 N7). Hence the **M4 endurance gate: 100 cycles (≥ 3× the busiest valve
in the fallback mode) with the real media**, leak tests at 20 kPa and 50 kPa, burst at 3 bar.

**Requirements per valve** (own targets; feasibility UNVERIFIED): closed leak ≤ 0.1 µL/min at 20 kPa (the cell sees no
pressure source during accumulation: all pumps stopped, chambers vented); closed solution resistance ≥ 1 GΩ (gen-1
minimum 15 MΩ); actuation ≤ 0.2 s; plunger force ≤ 1.5 N on slot valves, ≤ 3 N elsewhere (value set in M4); **closing
transient in the sealed cell ≤ 5 kPa** (§2.4); seal ≤ 0.3 mm from its trunk channel (≤ 0.5 mm at the cell) (§2.6).

**Fail-safe state** (dock power lost, PC lost, or sequencer safe state): all valves and gates closed except V3 open; all
magnets spring-up (beads stay where they are; a raised M_d below the anvil stops against the plate); syringe pumps stop
and hold; Gamry cell off; Peltiers off (the latch flags the card if the reagent zone exceeds 10 °C, docs/12 F16); the dock
hardware watchdog (heartbeat from Python) drives the same state if the PC dies. Nothing drains or siphons: every chamber
is vented and isolated, the cell is sealed.

---

## 5. Reagent system: dock supply (user decision 2026-11-12)

**The card is a fluidic, valve and electrode consumable, not a reagent pack.** By user decision of 2026-11-12, which
**supersedes the earlier "reagents on the cartridge" choice** recorded in docs/09 ("on-board reagents") and docs/12 §9:
* **beads:** stock in a cooled (4–8 °C), agitated vial in the dock (rocking or end-over-end, no stir bar), metered by S_b;
* **conjugate:** the on-card tank RCj is filled at insertion from a cooled dock bottle (through P_cf);
* **substrate:** the on-card tank RS is filled at insertion from a dock bottle (through P_rf);
* **no factory-filled reagent** on the card; the factory-fill option of Revision A (D12) is dropped, which removes the
  shelf-life questions (1.9 days to the Pi limit for factory-filled 3 mM HQDP at the acceptance-limit k_h, docs/12 §2.3).

The operator loads, per card, the bead vial, the conjugate bottle and the HQDP bottle before loading the autosampler —
not a manual step between autosampler loading and result in the sense of docs/00. The dock bottles are replaced daily
(conjugate ageing data exist to 24 h at 4 and 22 °C only, docs/06 E1.3 ageing arm).

### 5.1 Bead dosing (the former variant V2)

S_b is a Cavro Centris / Hamilton PSD/4-class pump (250 µL syringe, ≈ 10 nL/step, docs/11 §5.2) with a selection valve
(vial, A1, card, waste) and a 0.5 mm ID FEP holding coil of ≈ 40 µL that keeps beads out of the syringe (SIA principle of
gen-1, docs/07 §2); outlet line 0.25 mm ID × 50 mm (2.5 µL) to P_b. Per dose: (1) return the vial-to-valve line content
to the vial; (2) aspirate 2 µL air, 10.0 µL beads, 2 µL air; (3) dispense through P_b, V4/V5 and C_k into the vented
chamber followed by **4 µL A1** (path 2.5 + 0.24 + 0.3 + 0.26 = 3.3 µL); (4) rinse the outlet line to waste. Dose CV is
measured by gen-1 E2.2 (target ≤ 5 % over 8 h) and in M3; model: CV 0.05 → P 0.149, 0.10 → 0.124 (§1.3).

### 5.2 Conjugate and substrate on the card

| Item | Conjugate (RCj + MC) | Substrate (RS) | Source / arithmetic |
|---|---|---|---|
| Fill at insertion | 0.26 mL (14 × 10 µL + priming 20 µL + dead volume ≈ 100 µL) | 0.6 mL (14 × 20 µL + priming ≈ 100 µL + dead ≈ 200 µL; 0.75 mL in the fallback mode) | Derived |
| Temperature in use | 4–8 °C (reagent zone) | 25 °C (D8) | docs/07 §5.1, §5.5 |
| In-use life | 8 h (default conjugate life, docs/07 §5.5; ageing beyond 24 h not measured, docs/06 E1.3) | 8 h: Pi 2·k_h·t·S₀ = 2 × 10⁻⁹ × 28 800 × 3 mM = **0.17 µM** at the acceptance-limit k_h (0.017 nominal) vs ≤ 1 µM target; free HQ grows ≤ 2.9×10⁻⁵ mol/mol, removed by PE1/PE2 in step-read mode, a referenced baseline in R-flow mode | `ma.chemistries.alp_hqdp.hydrolysis_rate`; docs/05 §5 U3; docs/09 §3.4 |
| Card cap from the 8-h life | **14 determinations**: first Inject Start ≈ 12 min after insertion, last result 12 + 13 × 31 + 56.75 = 472 min = **7.86 h** after insertion (fills at ≈ 2 min) | same | §7.1; docking time UNVERIFIED (C2) |

If the measured cadence exceeds 31.3 min the cap falls to 13 (12 + 13 × 31.3 + 56.75 = 476 min ≈ 7.9 h; at 32 min 14 runs
would need 8.08 h). Extending the in-use life instead needs E1.3 ageing beyond 8 h (docs/15 §6 Q6) — not assumed.

### 5.3 Why beads stay off the card (record of the V1/V2 comparison)

V1 (beads on the card) put on the consumable the one element with no precedent and no data — an on-board liquid bead
suspension dosed over hours (docs/10 §6.2, §9.3) — plus a shelf-stored bead cake, a dose that drifts with tank level
(7 mm/h × 31 min = 3.6 mm of a 5 mm tank cleared between doses), +3 valves and a pressure port; V2 reuses gen-1's
reservoir concept and its E2.2 data. The user decision makes V2 binding.

---
## 6. Docking station

### 6.1 Block diagram

```
                     Waters stack (earthed)                                   Lab PC (Windows)
  BSM (A1 only) -> restrictors -> SM-FL (100 uL loop) --PEEK >= 0.3 m-->+     orchestrator (Python >= 3.10)
  SM-FL Inject Start (conn. 1, pins 1-2) ------------------------------+  |      | JSON/TCP   gamry_worker (Gamry Py 3.7)
  +-------------------------------------- DOCK ---------------------------|--|------|------------------|-------------+
  |  isolated DAQ (Inject Start, line code) <----------------------------'  |      |                  |             |
  |  dock controller (MCU, to be selected): plungers, Peltier PID, carriage, magnet lifts, interlocks,  Reference 600+ |
  |      HARDWARE WATCHDOG (heartbeat from Python) <-------------------------------'                  (floating)     |
  |  LID (top): 21 plunger actuators | die-back press pad | top heater block 25.0 C | grounded metal cover            |
  |  CARD NEST: locating pins; card pressed by the lid onto the ANVIL PLATE (datum pads, 9 face seals, windows, slot) |
  |  BELOW THE ANVIL:  magnet bay (25 C air): M_c,1 / M_c,2 Z units (25 mm) | M_d X-Y-Z carriage | M_h lift | M_w   |
  |                    electrode bay (grounded enclosure, own RH sensor): pogo block (6 pins) -> relay -> Gamry WE/RE/CE |
  |                    reagent-zone Peltier plate (4-8 C) as the anvil under RCj/MC                                    |
  |  FLUIDICS: S_b + rocking cooled bead vial | S_A (clean A1, dispense only) | S_IC1, S_IC2 (1 mL, pull + tidal,      |
  |       60 uL FEP coils) | S_RC (250 uL, pull only) -- one RS-485 bus | 2 pressure channels (P_c, P_mv; bottle fills) |
  |       A1 bottle | conjugate bottle (cooled) | HQDP bottle | waste bottle with level sensor | drip tray with leak electrodes|
  |  SENSORS: T x6, RH x2 (lid, electrode bay), P on the P_in line, card presence, contact loop, ID scanner           |
  +-----------------------------------------------------------------------------------------------------------------+
```

### 6.2 Actuators, sensors and controllers

Candidate parts only as sourced in docs/11; otherwise "to be selected". No part number below is new.

| Item | Function | Specification it must meet | Candidate (docs/11) |
|---|---|---|---|
| Plunger actuators ×21 | press the TPE at V1–V12, V14–V18, G1–G4 | stroke ≥ 0.5 mm (0.175 mm channel + TPE compression, UNVERIFIED), force ≤ 1.5 N (slot valves) / ≤ 3 N, ≤ 0.2 s, spring fail state per §4, position feedback | memetis actuators sold for CS_1367 (named, model not read) — to be selected; solenoid plungers [assessment] |
| Anvil plate | counter-support under every valve; face seals; windows W1, W2 (Ø 12 mm), drag slot (4 mm), hold window, BW recess, contact window | flatness and datum to hold the foil-to-magnet gap 0.16 ± 0.05 mm at the windows (UNVERIFIED); non-magnetic | custom part [assessment] |
| M_c,k Z units ×2 | collection under each chamber | ≥ 25 mm stroke, spring-up, ≤ 10 s | to be selected (docs/11 §5.4 assessment: spring-loaded slide) |
| M_d X–Y–Z carriage | gather (raster), hold, drag, bead-out | travel x 34–60, y 6–44 mm, repeatability ≤ 10 µm, 0.05–5 mm/s, path following of a ≥ 3 mm radius lane, Z ≥ 8 mm, gap 0.16 ± 0.05 mm when up; drivers disabled during reads | Zaber stages with the Zaber Motion Library (ZABER_SW) — model, travel, speed UNVERIFIED |
| M_h lift | hold the pellet under WE1 | 4 mm stroke, spring-up | to be selected |
| Syringe pumps S_b, S_A, S_IC1, S_IC2, S_RC | beads; clean delivery; tidal + drain; cell fill/flush and fallback sweep | ≥ 24 000 steps per stroke; selection valve ≥ 4 ports; RS-485; S_RC pulsation-free at 10 µL/min | Tecan Cavro Centris (TECAN_CENTRIS) or Hamilton PSD/4 (HAMILTON_PSD4; smooth flow HAMILTON_97709 for S_RC) |
| Pressure channels ×2 | RCj headspace (P_c), meter vent/air push (P_mv); bottle pressurisation for the fills at insertion | 0–35 kPa, 1 % stability, 30 ms | Fluigent Flow EZ 345 mbar (FLUIGENT_FLOWEZ, FLUIGENT_SDK) or Elveflow OB1 (ELVEFLOW_OB1) |
| Flow sensors | verify the fallback sweep and the rinse flows | 1–20 and 50–500 µL/min | Sensirion LG16-0150D (7 µL/min FS, marginal; SENSIRION_LG16), SLF3S-0600F (SENSIRION_SLF3S) |
| Peltier zones ×3 | reagent zone 4–8 °C (RCj, MC; bead vial holder separately); assay plate and top heater 25.0 ± 0.2 °C | §6.5 | to be selected (docs/11 §5.4) |
| Bead vial holder | 4–8 °C, rocking, low shear | dose CV ≤ 5 % over 8 h | to be selected |
| Isolated DAQ | Inject Start into Python | opto-isolated, PC timestamp | LabJack U3 as gen-1 (`hardware_lab.example.yaml`) |
| Dock controller | plungers, Peltier PID, carriage and lifts, interlocks, heartbeat watchdog | independent of the PC | to be selected |
| Potentiostat | PE1, PE2, R3 read; fallback CA on WE2 | one channel | Gamry Reference 600+ (in hand; docs/02 §4) |
| WE relay | WE1 ∥ WE2 (step-read mode) or WE2 alone (fallback) | leakage ≤ 0.1 pA at 0.5 V, thermal EMF ≤ 10 µV; not switched during a read | low-leakage reed relay, to be selected |
| Pogo block | 6 gold-plated spring pins from below | contact resistance stable within a read; force UNVERIFIED | to be selected (docs/11 §5.4; Mill-Max not reachable) |

### 6.3 Electrical design for the step read

* **Signal levels (Derived):** per step ≈ 0.22 µC of charging (peak 11 µA, 21 ms) against ≈ 1.0 nC of product at 1 pg/mL
  and a 0.05 nC target SD (§3.5.4). The Ref 600+ resolves 20 aA and has 11 current ranges 60 pA–600 mA (docs/02 §4.1).
  Range plan: the same sequence in every window (µA range for 0.5 s, then a fixed nA range); autorange is not used inside
  a window. Range offset specifications were not read (UNVERIFIED); M5a measures the offset behaviour directly.
* **Contact route:** pogo pins from below in the electrode bay (§2.7), shielded leads ≤ 0.3 m; Faraday enclosure for the
  bay (docs/02 §4.4); the lid over the die is grounded metal; shield connection per the Gamry manual for floating
  operation (wording UNVERIFIED).
* **Contact resistance:** mΩ–Ω is negligible against R_u ≈ 14 kΩ; what matters is that it does not change within a read →
  no actuation anywhere in the dock during a read window (§7.2); contact-loop resistance logged at docking and hourly.
* **Leakage:** pads on the dry side of ≥ 3.8 mm of bonded film; ≥ 5×10¹² Ω pad-to-WE; the bay above the dew point (§6.6).
* **Grounding with the Waters stack:** the Gamry floats (`hw.gamry.floating`). During PE1, PE2 and the read the cell is
  closed on all sides (G3, G4, V14, V15, V16 closed), so the path to the earthed BSM is broken at closed membranes
  (≥ 1 GΩ, M4 by EIS); the ≥ 0.3 m PEEK line stays (`hw.tubing.peek_isolation_length_each_side_of_cell`).
* **Noise sources:** stepper drivers (carriage, pumps, Z units), solenoid plungers, Peltier PWM. Rules: Peltier drives
  linear or PWM ≥ 20 kHz with filtered leads; all actuators idle and stepper drivers disabled (holding brake) during read
  windows (§7.2); separate supplies, star ground at the Gamry chassis point. M5a measures each source's effect on Q_net.

### 6.4 Mechanical datum, anvil and magnet gap

The lid presses the card onto three datum pads of the anvil plate, so the foil underside sits on the anvil everywhere
outside the windows and the slot. At the windows the foil spans freely; the magnets rise to 0.16 ± 0.05 mm below it (foil
flatness UNVERIFIED). The card interior is never pressurised by the lid (chambers vented, cell liquid-filled at ambient
pressure); the only distributed loads on unsupported foil are the slot-valve plungers (≤ 1.5 N, ≈ 15 µm, §2.1).

### 6.5 Thermal design

* Reagent zone (x 0–20 mm) 4–8 °C from the Peltier plate on the foil side (tank walls are the thin foil, docs/11 §4);
  assay zone 25.0 ± 0.2 °C (docs/07 §5.1) from the anvil plate (heated, outside the windows), the top heater block on L3
  over the chambers and the die window, and the magnet and electrode bays held at 25 °C. Thermal break: through-slot in
  L3 at x 20–24 mm with two 3 mm bridges (L0–L2 continuous; the conjugate line crosses there).
* Time constants (Derived; COC diffusivity ≈ 1×10⁻⁷ m²/s UNVERIFIED): 5.5 mm upper body (2.75 mm)²/α ≈ 76 s; 0.2 mm cell
  (water, α ≈ 1.4×10⁻⁷ m²/s UNVERIFIED) 0.3 s. Card equilibration at docking ≈ 10 min.
* 10 µL of 4–8 °C conjugate into ≈ 175 µL at 25 °C: ΔT of the mix ≈ 1 K, recovered in ≈ 1 min [assessment]; identical
  every run. The substrate does not cross zones (D8).
* The model has no temperature dependence (docs/03 §11); ±0.2 °C acts on k_on, k_cat and D (read weight, §3.5.2) —
  calibrated out if constant.

### 6.6 Dew point and condensation

At 22 °C and 50 % RH the dew point is ≈ 11 °C (Magnus approximation; constants UNVERIFIED). The reagent zone (4–8 °C)
is below it: closed-cell insulation with a dry-gas or desiccant volume and a drip path away from the nest. The electrode
bay is ≥ 35 mm from the cold zone, at 25 °C, with its own RH sensor logging the margin; condensate on the pads would short
the WE (§6.3).

### 6.7 Presence, identity and docking check

Lid-closed switch; contact-loop resistance on the die via the pogo block (< 10 Ω expected); data-matrix code on the card
(serial, mould/die/laminate lot, date, expiry, lot calibration per chamber); Python keeps a usage log per serial (runs,
faults, post-high events) and refuses expired or exhausted cards.

### 6.8 Leak detection

(1) Docking pressure-hold test: every liquid port at 20 kPa against closed valves for 30 s, decay limit set in M4; (2) drip
tray with interdigitated electrodes and a level switch; (3) syringe-pump stall/pressure faults; (4) volume balance per run
(dispensed vs waste level); (5) P_in line pressure during the transfer; any of these → fault → safe state → latch.

---

## 7. Control and timing

### 7.1 Per-run step table and staggering

Times in minutes from the run's own Inject Start. Chamber k = 1 for odd runs, 2 for even runs; run n+1 is injected
31.0 min after run n. Valves not listed are closed (V3 open unless listed closed). Class: **A** = dock activity, **Q** =
read window (no dock activity of any run), **W** = Waters-side only, **S** = static. The table was generated and checked
by the scratch script `sched.py` (Appendix A); "movable" steps are placed by the scheduler against the predicted next
Inject Start.

| t (min) | Step | Flows / volumes | Valves / gates open | Magnets | Gamry | Class |
|---|---|---|---|---|---|---|
| −10.0 → −9.5 | conjugate meter fill-to-vent (movable) | P_c +10 kPa (value set in M3) | V8 | – | – | A |
| −5.0 → −4.0 | bead dose (movable) | S_b: 10 µL slug + 4 µL A1 chase | V(4/5)_k | – | – | A |
| −4.0 → −3.5 | conjugate push + C_k chase (movable) | P_mv air push 10.0 µL; S_A 3 µL | V(6/7)_k; V(17/18)_k opens at −3.5 | – | – | A |
| −3.45 | V_k open, V3 closed (movable) | BSM 1 µL/min now enters IC_k | V(1/2)_k, V(17/18)_k | – | – | A |
| −1.0 → 0 | SM-FL aspirates ≈ 200 µL | BSM 1 µL/min | – | – | – | W |
| **0** | **Inject Start** (anchor) | | | | | |
| 0 → 1.5 | transfer 150 µL into IC_k | BSM 100 µL/min | V(1/2)_k | – | – | W (inside the previous run's PE2) |
| 1.5 → 3.35 | BSM steps to 1 µL/min; no card actuation | 1.85 µL into IC_k | V(1/2)_k | – | – | W |
| 3.35 → 3.55 | V_k closed, V3 open; C_k chase 3 µL; V(9/10)_k opens (tidal starts) | S_A | V3, V(17/18)_k until 3.55 | – | – | A |
| 3.4 → 5.4 | loop + line flush to bypass; **Loop Offline at 5.4**; then parked 1 µL/min | BSM 100 µL/min, 200 µL | V3 | – | – | W |
| 1.5 → 30.0 | **incubation 28.5 min** at 25.0 °C; tidal 50 µL every 30 s from 3.4, paused 21.5–26.0 (READ of run n−1) | S_IC_k | V(9/10)_k | M_c,k down 25 mm | – | A (pausable) |
| 30.0 → 30.1 | M_c,k up (collection starts) | – | – | M_c,k | – | A |
| **30.1 → 34.1** | **PE2** = residual-activity monitor + last removal (three-window read); collection static | sealed | – | M_c,k up (static) | R3 | **Q** |
| 34.1 → 34.2 | M_c,k down | – | – | M_c,k | – | A |
| 34.2 → 36.2 | gather: 3 raster passes of M_d at 0.30 mm/s to the funnel mouth | – | V(9/10)_k | M_d | – | A |
| 36.2 → 39.5 | partial-drain rinses (185 → 30 µL; 6 × 100 µL); 130 µL drag medium stays | S_IC_k pull, S_A fill, 500 µL/min | V(9/10)_k, V(17/18)_k | M_d holds | – | A |
| 39.5 → 41.75 | **drag 23.3 mm at 0.20 mm/s** into the cell; hand-over to M_h; G3 then G_k closed | no flow | G_k, G3 (G_k stays open) | M_d, then M_h | – | A |
| **41.75 → 52.75** | **accumulation 11 min**, cell sealed, open circuit | – | – | M_h holds | off | S |
| 41.75 → 42.35 | WL_k refresh J → IC_k (5 µL), then WLc → V12 (5 µL) | S_A | V11, G_k (to 42.05), V12 (42.05–42.35) | – | – | A |
| 42.35 → 49.85 | chamber cleaning: full drain, **6** × (150 µL, 2 tidal strokes, full drain), bead-port and C_k chases | S_IC_k, S_A, S_b | V(9/10)_k, V(17/18)_k, V(4/5)_k | – | – | A |
| **52.75 → 56.75** | **READ** (R3): Q_net = Q_a − 2Q_b + Q_c | sealed | – | M_h | R3 | **Q** |
| **56.75** | **result** (56.75 min after Inject Start; 57.75 after the start of aspiration) | | | | | |
| 56.75 → 57.15 | bead-out to BW (4.5 mm at 0.20 mm/s) | – | G4 | M_h down, M_d | – | A |
| 57.15 → 57.65 | cell + BW flush with fresh HQDP (prepares the cell for run n+1) | S_RC pulls 20 µL at 40 µL/min | V15, G4, V16 | M_w (fixed) | – | A |
| 57.65 → 58.65 | **PE1 for run n+1** (removal; not a read) | sealed | – | – | 15 s E_rest, 45 s E_det | A |

**Checks (Derived by `sched.py`, all offsets k·C, k = −4…4, jitter guard ±0.25 min around other runs' read windows):**
* **No dock activity of any run falls in any read window** (PE2 or READ) at C = 31.0 — including the previous run's PE2
  (−0.9 → 3.1 in a run's own frame), which is why V_k opens at −3.45 and switches back only at 3.35.
* **Exclusive resources** (carriage, S_A, S_RC, S_b, P_c, P_mv, Gamry, cell, and each chamber two runs apart): no clash.
* **Cell sequence:** drag (39.5) … flush and PE1 end at 58.65; the next run's PE2 starts at 61.1 → **slack 2.45 min**
  (Revision A: 1.25 min claimed, ≈ 0.4 real, docs/15 S4).
* **Chamber cycle:** cleaning ends 49.85; the same chamber's next bead dose is at 57.0 → reserve 7.15 min.
* **Cadence tolerance:** with first-fit placement of the movable steps (conjugate fill, bead dose, conjugate push, V_k
  pre-switch), feasible for a measured cadence of **30.0–33.0 min** (checked at 30.0, 30.5, 31.0, 31.5, 32.0, 33.0); below
  30.0 the dosing window between READ(n−2) and PE2(n−1) is shorter than the 1.55 min of dosing.
* **Margin to the 60-min limit: 3.25 min** after Inject Start (2.25 min after the start of aspiration). Throughput 1.94
  samples/h; 14 determinations in 13 × 31 + 56.75 = 460 min from the first Inject Start.
* **Tidal pauses:** 6.35 of the 28.5-min incubation (1.5–3.35 and 21.5–26.0), at the same times in every run (C4).

**Cost of the margin (from §1.3):** 30 → 28.5 min incubation with 6.35 min of pauses (25.33 effective) and 15 → 11 min
accumulation: P 0.187 → 0.150 without credit. The split between incubation and accumulation is P-neutral; the pauses are
not (allowing tidal strokes during reads would give 0.164).

### 7.2 What may happen during a read window, and why

**Forbidden in PE2 and READ windows of any run (±0.25 min for other runs):** every dock actuation — card-valve plungers,
any syringe-pump step, pressure-channel switching, magnet Z lifts, carriage motion, M_h, the WE relay, the bead-vial
rocker (paused; beads settle ≈ 0.5 mm in the vial per 4-min pause; the line-return step precedes every dose
[assessment; E2.2 to include intermittent agitation]).

**Allowed:**
* static magnets (M_c,k up during PE2, M_h during the READ) — a static field induces nothing;
* Peltier and heater control (linear or PWM ≥ 20 kHz, continuous, identical in every read);
* the BSM's flow and flow steps and SM-FL-internal events that switch no card valve (aspiration, injection valve, Loop
  Offline) — the cell is sealed behind ≥ 1 GΩ closed membranes plus ≥ 0.3 m of PEEK, and these events fall at the same
  phase of every read [assessment; UNVERIFIED until C2, M5a cannot test the Waters coupling];
* sensor polling on low-level buses.

**Relaxation lever (decided by M5a, §10.1):** if tidal strokes inside the E_rest segments leave SD(Q_net) unchanged
(≤ 1.2× quiet), they are allowed there; worth +0.014 in P (§1.3).

### 7.3 Trigger chain from Empower

1. The operator docks the card and loads the bead vial and the conjugate and HQDP bottles (§5) and the SM-FL tray; Python
   reads the card ID, runs the leak test, fills RCj and RS, primes the lines, coils and the cell (≈ 12 min to the first
   injection, UNVERIFIED; the electrode QC of §8.1 runs during the first run's incubation).
2. Empower sample set: one line per determination, all with the **same instrument method**: SM-FL full loop 100 µL (2×
   overfill); BSM A1 **100 µL/min 0–1.5 min, 1 µL/min 1.5–3.4 min, 100 µL/min 3.4–5.4 min, Loop Offline at 5.4 min,
   1 µL/min 5.4–30.0 min**; run time 30.0 min; injection overhead ≈ 1 min (`hw.smfl.injection_overhead_time` 0.25–2,
   UNVERIFIED) → Inject Start every ≈ 31.0 min (measured at Stage 0). The card valves at 3.35 min are switched by Python
   from the Inject Start; the BSM flow steps are Empower's.
3. Inject Start (connector 1, pins 1–2, docs/02 §3.1) → isolated DAQ → Python timestamps t₀, checks the spacing,
   assigns the chamber, instantiates the run table and re-places the movable steps of the next run against the predicted
   t₀ + measured cadence.
4. Python drives the dock, the Gamry worker and logs everything; Empower only pumps and injects ("Empower is the fluidic
   master", docs/02 §3.2). Watchdog: an Inject Start outside the predicted ±0.25 min re-places movable steps; a fixed step
   that would enter a read window flags the affected run; a cadence < 30.0 min, a device error, leak or temperature
   excursion → safe state (§4) → fault latch.

### 7.4 Mandatory cleaning cycle and blank check after a result > 100 pg/mL (user decision 3)

**The timing fact that shapes it.** Run n's result arrives at 56.75 min. By then run n+1 (other chamber) has been in its
incubation since 31.0 + 1.5, and run n+2 (same chamber as n) starts its bead dose at 57.0. **Run n+1 cannot be protected by
a cleaning that precedes it** in a staggered schedule; it is protected by the shared-path budget (§8.3) and by the
immediate part of the cycle, which runs before n+1's drag.

**Cycle (sequencer state POST_HIGH):**

| Step | When (run-n frame) | What | Fits because |
|---|---|---|---|
| 1. extra cell clean | 58.65–60.15 | second cell + BW flush (20 µL) and a second PE1 | cell slack 2.45 min before run n+1's PE2 at 61.1 |
| 2. extra lane clean | 58.65–58.95 | WLc refresh to waste (S_A → V11 → V12, 5 µL) | S_A free; before run n+1's drag at 70.5 |
| 3. chamber k | already done | the default cleaning is the 6-rinse cycle (42.35–49.85), so no decision is needed before the result | chamber reserve 7.15 min |
| 4. **blank check** = slot n+2 (chamber k) | injection at 62.0 | (A) if the Empower Toolkit can insert a sample-set line (UNVERIFIED; docs/02 §3, Waters Q5): a buffer vial "W" is injected — tests every path incl. SM-FL and inlet; (B) otherwise Python diverts injection n+2 to the bypass (V3 open, V_k closed) and fills chamber k with 150 µL A1 from S_A — tests chamber, lanes, cell and reagents; the diverted injection and the D13 flush wash the inlet; **sample n+2 is not measured** and must be re-queued (vials with ≥ 2 draws, ≈ 400 µL) | same run table, same timing |
| 5. accept | blank result at 56.75 + 2 × 31 = 118.75 | blank ≤ chamber-k lot blank mean + 3 SD → clear POST_HIGH | — |
| 6. fail | — | recovery cycle `cycle_cartridgeA_recovery` (Python-only, ≈ 8 min in chamber k's next idle time: bead-out, two cell flushes + PE1, both lanes refreshed, chamber k drained and rinsed 6×, carriage park) and a second blank check in chamber k's next slot; fail again → fault latch, card rejected | — |
| 7. run n+1 (in flight) | at its result | flagged "post-high"; reported only if (shared-path fraction after steps 1–2, 4.6×10⁻⁵, §8.3) × R_n ≤ 0.1 × max(R_(n+1), LOD_lot); otherwise "re-measure" | §8.3 |

**Effect on throughput and on the staggered schedule:** the stagger is unchanged (the blank check uses the normal run
table; steps 1–2 fit into existing slack). Each result > 100 pg/mL costs **one slot (31 min) and one of the card's 14
determinations** (10 samples → 9), plus in mode (B) the re-queue of sample n+2, plus a re-measure of n+1 if rule 7 fails
(for R_n ≤ 2.2 ng/mL it never fails at LOD_lot = 1 pg/mL: 4.6×10⁻⁵ × 2200 = 0.10 pg/mL).

**Mapping to the existing fault-latch/recovery concepts** (`automation/elisa_auto/latch.py`, `config/cycle_recovery.yaml`):
POST_HIGH is a **second latch of the same kind** (JSON file in the sequence folder, survives an orchestrator restart, set
with run id and reason, every flagged run carries the flag in its metadata) but it is **set by a result** (> 100 pg/mL, or
a PE2 monitor flag) rather than by a device fault, and it is **cleared only by a blank-check run that passes** (logged
with that run's id). The fault latch keeps its meaning (device fault → safe state → runs invalid) but for cartridge A its
clearing condition becomes "recovery cycle completed **and** a passing blank check". Steps 1–2 are a short Python-only
cycle `cycle_cartridgeA_posthigh.yaml` (≈ 1.5 min) in the style of `cycle_recovery.yaml` (no SM-FL injection, no Empower
action).

### 7.5 Mapping onto the existing `automation/` package

| Existing element (automation/) | Reused as is | Needs change / new |
|---|---|---|
| `cycle.py` step table and `validate()` (no gaps, ≤ 60 min, injects declared, SM-FL actions) | schema and checks | chamber templating (`{k}`), per-step `resources:` and an **actuator-class tag** (A/Q/W/S), `movable: [earliest, latest]` windows, and the **periodic overlap check over all run offsets with a jitter guard** (the logic of the scratch `sched.py`); card valves as two-position valves; new `sia`-type actions `bead_dose`, `tidal_mix`, `partial_drain_rinse`, `drain_chamber`, `rinse_chamber`, `wl_refresh`, `flush_cell`, `chase`; `magnet` becomes `{Mc_k: up/down, carriage: path/position, M_h: up/down}`; potentiostat actions `step` and `step_triple` |
| `sequencer.py` (anchoring, watchdog, safe state, run log) | anchoring, watchdog, safe-state discipline, logging | two interleaved run instances sharing cell, carriage, Gamry, S_A and S_RC → a small scheduler that instantiates the table per Inject Start, places movable steps first-fit, and blocks any action in a read window |
| `latch.py` fault latch | unchanged mechanism; a fault invalidates **both** runs in flight | second latch type POST_HIGH (§7.4); cartridge-A clearing needs recovery + passing blank check |
| `cycle_recovery.yaml` | concept | `cycle_cartridgeA_recovery.yaml` and `cycle_cartridgeA_posthigh.yaml` (§7.4) |
| `devices/base.py` (`Valve`, `SIAModule`, `Magnet`, `InjectStartInput`, `Potentiostat`, `Empower`) | `Valve`, `InjectStartInput`, `Empower` (passive), `Magnet` for M_h and M_c,k | `MagnetCarriage` (move_to, follow_path(speed), z), five named `SyringePump`s with **dispense-only / pull-only flags enforced in software** (S_A dispense-only; S_IC_k, S_RC pull-to-waste only), `PressureChannel`, `DockController`, `ThermalZone`, `CardReader`, `LeakSensor`, `WERelay`; simulators in `devices/sim.py` |
| `gamry_worker.py` (JSON lines, sim backend) | process split and protocol style | command `step_triple` (E_rest, E_det, window and rest durations, range plan) returning the trace and the three window charges; ToolkitPy calls stay a stub (docs/02 §4.3) |
| `signal_proc.py` | used unchanged for the fallback R-flow read | `triple_window_charge()` (Q_a − 2Q_b + Q_c) and the PE2 monitor with the card's running median |
| `stats.py`, `analyze.py`, `gates.yaml` | LOD = 3·SD/b; carry-over criterion 10⁻⁴ unchanged | per-chamber calibration (§8.2); gate entries for M5a and M1–M7 (§10) with a 100 ng/mL carry-over challenge |
| `model_feedback.py`, hardware YAMLs | unchanged / format | `hardware_cartridgeA_sim.yaml` with V1–V12, V14–V18, G1–G4, five pumps, carriage, lifts, sensors |

---
## 8. Calibration and QC strategy

### 8.1 At docking (per card)

1. Card ID, expiry and usage check; lid closed; contact-loop resistance < 10 Ω.
2. Leak test (§6.8); thermal equilibration of both zones (≥ 10 min, §6.5).
3. RCj and RS filled from the dock bottles; priming of the bead coil and line, MC (one dose to waste through IC1), both
   lanes and WLc, the cell, WE2 channel and CE/RE pocket (V14 and V15 used once).
4. First Inject Start ≈ 12 min after insertion (blank, IC1).
5. **Electrode QC during the first incubation** (the cell is free until the first PE2 at 30.1): CV of WE1 ∥ WE2 between
   E_rest − 0.1 V and E_det + 0.1 V → double-layer capacitance (area check ±10 % of the lot value, own target), no
   unexpected wave; cell height from the PE1 decay; then **3 R3 reads on fresh substrate**: SD of Q_net ≤ 0.05 nC
   (n = 3 is a gross check; the statistical acceptance is M5a/M5). Failure → R-flow mode for this card (no credit) or
   reject.

### 8.2 Calibration (docs/15 W7)

* **Lot calibration per chamber** (bead lot × conjugate lot × die/laminate lot, made by the lab): full curve 0, 1, 3, 10,
  30, 100, 300, 1000 pg/mL in triplicate **in each chamber**, over ≥ 3 cards; 4PL and the 0–10 pg/mL linear slope of
  docs/06 §7.4 (`stats.py`); chamber-specific blank mean and SD.
* **Per card (14 determinations):** position 1 blank (IC1), 2 blank (IC2), 13 control 30 pg/mL (IC1), 14 control (IC2);
  **10 samples**. Acceptance (own targets): blank within the chamber's lot blank mean ± 3 SD; control within ±20 % of its
  lot value. Start blanks vs end controls track within-card drift per chamber. Post-high blank checks (§7.4) add blank
  data.
* **Why lot calibration might suffice:** the exhaustive read makes the specific charge nearly independent of electrode area
  (read weight 0.92 ± 0.07 over the D range, §3.5.2, and the cell height of each card is measured). To be tested (M5 on
  5 dies, C2 on ≥ 5 cards): if the card-to-card slope CV > 10 % (`ma.reuse.slope_drift_tolerance`), switch to a per-card
  4-point curve per chamber (costs 8 of 14 determinations — the card would then carry 2 samples; this would end A's
  throughput case).

### 8.3 Carry-over budget (docs/15 S11) and rules

The criterion is end-to-end: ≤ 1×10⁻⁴ of the previous determination's signal in the next (`gates.yaml` `carryover`,
docs/08 S6). Fractions below are of the source determination's analyte/enzyme signal. "Consecutive" = paths shared by run n
and run n+1 (other chamber); "same chamber" = paths shared by run n and run n+2.

| # | Path | Shared by | Mechanism and arithmetic | Allocation, normal | Into run n+1 after a high (steps 1–2 of §7.4 done) | After the blank check (first sample after it) | Verified by |
|---|---|---|---|---|---|---|---|
| 1 | SM-FL needle, loop, injector | consecutive | `hw.smfl.carryover_protein_conjugate` nominal 10⁻⁴ (10⁻⁵–10⁻³, UNVERIFIED) → needs a needle wash **3× better than nominal** | **3×10⁻⁵** | 3×10⁻⁵ (already injected) | 1×10⁻⁵ (one intermediate buffer injection, mode A; UNVERIFIED) | E1.10 (10 ng/mL → B1 → B2), extended by the flush programme |
| 2 | PEEK line, M_in, V_k′ and V3 stubs | consecutive | D13 flush 3.5 loop volumes (liquid ≤ 10⁻⁵); 0.3 mm stubs: 0.026 µL × 0.12 C₀ × ≤ 0.15 left after 30 min × 0.1 exit / 100 µL ≈ 5×10⁻⁷ (Derived); wall adsorption UNVERIFIED | 1×10⁻⁵ | 1×10⁻⁵ | 1×10⁻⁶ | E1.10, M7 |
| 3 | C_k and its valve stubs | same chamber | chased after every delivery and in the cleaning; 0.3 mm sample stub: 0.026 µL × 0.12 C₀ × 0.02 left after 62 min / 100 µL = 6×10⁻⁷ (Derived) | 1×10⁻⁶ | — | — | M7 |
| 4 | IC_k walls and film | same chamber | liquid: 6.6×10³ (wash) × (155/5)⁶ cleaning ≫ 10⁸ → 0; desorption of wall-adsorbed analyte/conjugate UNVERIFIED | 1×10⁻⁵ | — | 1×10⁻⁶ (chamber k has had one more full cycle) | M7 same-chamber path; blank check |
| 5 | tidal nozzle, dock coil, S_IC_k | same chamber | one-way during washing; coil content at the next incubation = last cleaning drain (≈ 10⁻⁹); coil wall adsorption UNVERIFIED (FEP ≈ 320 mm²) | 2×10⁻⁶ | — | — | M7 |
| 6 | WL_k branch | same chamber | stranded beads pushed into IC_k by the same run's refresh, then cleaned: ≤ 50 beads × 2×10⁻⁶ × (5/155)⁶ ≈ 0 | 1×10⁻⁶ | — | — | M1 (≤ 1 bead in IC_k after refresh + cleaning) |
| 7 | J, WLc, G_k′/V11/V12 stubs | consecutive | liquid flushed to waste each run (≈ 7 volumes); stranded beads not reached by the flow: ≤ 10 beads × 2×10⁻⁶ per bead | **2×10⁻⁵** | 2×10⁻⁶ (extra WLc refresh) | 2×10⁻⁶ | M1: ≤ 10 beads per pass by whole-path imaging |
| 8 | cell: beads left after bead-out, adsorbed enzyme | consecutive | ≤ 10 beads; PE2 monitor detects ≥ 4.8×10⁻⁵ of a 10 ng/mL source | **2×10⁻⁵** | 2×10⁻⁶ (extra flush + PE1) | 2×10⁻⁶ | M1 (≤ 10 beads in the RC), PE2 every run |
| 9 | cell stubs and pocket (previous product) | consecutive | flush + PE1 + PE2 + escape ≤ 0.5 % of a stub content that is itself ≪ 1 % of the product | 1×10⁻⁶ | 1×10⁻⁶ | 1×10⁻⁶ | M5 |
| 10 | BW (spent beads) | consecutive | G4 opens only after the next read; leak through closed G4 only | 1×10⁻⁶ | 1×10⁻⁶ | 1×10⁻⁶ | M4 (gate leak) |
| 11 | S_RC (pull only), S_A (dispense only), bead, conjugate and HQDP supply | — | no path back to a chamber or the cell except a leaking valve | 0 | 0 | 0 | M4 |
| | **Sum, consecutive paths** | | 3 + 1 + 2 + 2 (×10⁻⁵) + 2×10⁻⁶ | **8.2×10⁻⁵** | **4.6×10⁻⁵** | 1.7×10⁻⁵ | |
| | **Sum, same-chamber paths** | | | **1.4×10⁻⁵** | — | | |
| | **Worst determination (n−1 consecutive + n−2 same chamber)** | | | **9.6×10⁻⁵ ≤ 10⁻⁴** | | | |

**Consequences.** (i) The budget closes only if the SM-FL achieves 3×10⁻⁵ (its nominal value alone is 10⁻⁴); if E1.10
measures ≥ 10⁻⁴, the 10⁻⁴ criterion cannot be met by A in normal operation and the post-high rule becomes the only
protection for samples following results ≤ 100 pg/mL (then 10⁻⁴ × 100 pg/mL = 0.01 pg/mL — harmless). (ii) For normal
results (≤ 100 pg/mL) the budget means ≤ 0.01 pg/mL in the next sample. (iii) After a high result, run n+1 receives
≤ 4.6×10⁻⁵ × R_n (0.14 pg/mL at 3000 pg/mL), hence rule 7 of §7.4. (iv) M1 limits are derived from the budget: ≤ 10 beads
per pass at J/WLc and in the cell (not 50 as in Revision A).

**Validation (per lot, not per card):** 5 × (**100 ng/mL** → B1 → B2) per path class — (a) same chamber (C_k, IC, WL
branch, cell) and (b) other chamber (SM-FL, inlet, J/WLc, cell) — read through the low-range slope; 10⁻⁴ of 100 ng/mL is
10 pg/mL in B1, ≫ 3 SD at LOD ≤ 1.5 pg/mL (docs/15 W4; 10 ng/mL would give 1 pg/mL ≈ 2 SD). Run once with the post-high
cycle disabled (raw path carry-over) and once enabled (B1 = the blank check).

---

## 9. Tolerance and failure analysis (top 12, FMEA style)

S = severity, O = occurrence (before mitigation), D = detectability (1 = always detected), each 1–5 [assessment].

| # | Failure mode | Cause | Effect | Detection | Mitigation | S/O/D |
|---|---|---|---|---|---|---|
| FM1 | Read background SD(Q_net) > 0.05 nC | drift curvature (relaxation after switch-on), range offsets, contact or relay instability, dock EMI | P 0.141 → 0.097 at 0.155 nC (§1.3) | M5a; docking QC; blank SD | three-window read, identical range plan, strict quiet windows, Faraday bay; **fallback R-flow** (no credit) | 5/3/2 |
| FM2 | Flat-floor TPE valve leaks or sticks | corner sealing in a rectangular channel; TPE creep; delamination; BSA fouling | cell not sealed (product loss, noise path), cross-talk | docking leak test; PE2; EIS in M4 | M4 (100 cycles, real media); force limits; fail-closed springs | 5/3/3 |
| FM3 | Foil deflection at slot valves changes the magnet gap or seal | plunger force > 1.5 N; E of COC lower than assumed | drag speed margin drops (v_max 0.61 → 0.35 mm/s at +0.2 mm gap); leak | M4 slot variant | force limit; slot ≤ 4 mm | 3/2/3 |
| FM4 | Beads stranded on the drag path or not following | bead–foil friction/adhesion; gap > 0.2 mm | carry-over into the next run (shared J/WLc) | M1 whole-path imaging; 100 ng/mL challenge | 0.20 mm/s (3.0× margin), gap 0.16 ± 0.05 mm, WL refresh of the same run, WLc refresh each run | 5/3/3 |
| FM5 | Gather incomplete (beads at the far wall) | friction; capture zone smaller than computed | signal loss; a variable loss acts as dose CV (CV 0.10 → P 0.124) | M1 floor imaging | 3 passes with ≥ 2.7 mm capture half-width; spare third pass | 4/2/3 |
| FM6 | Residual activity in the cell | beads left after bead-out; adsorbed enzyme; HQ from BW | carry-over; biased low samples after high ones | **PE2 monitor every run** (≥ 4.8×10⁻⁵ of a 10 ng/mL source) | bead-out + flush + PE1; post-high extra flush (§7.4) | 4/3/1 |
| FM7 | Chamber mixing factor near 0.2 | swirl does not lift beads; 6.35 min of pauses | capture × 0.2–0.5 → LOD × 2–5 | M2 | tangential jet; lever: tidal strokes in E_rest segments (M5a-6) | 4/3/2 |
| FM8 | Pre-electrolysis ineffective or escape > 1 % | stubs longer than 0.5 mm (tolerance), slow pocket, E_det side reactions | credit lost; S4a rescue lost (P 0.171 → 0.056 at 1-mm stubs) | M5a escape arm; PE2 trend | stub rule (§2.6), fast pocket, PE1 + hold + PE2 | 3/3/2 |
| FM9 | Post-high carry-over into run n+1 | n+1 injected before the high result is known | bias ≤ 4.6×10⁻⁵ × R_n | rule 7 of §7.4 | extra cell/lane clean before n+1's drag; re-measure rule | 3/3/1 |
| FM10 | Bubble in the cell or vent wet-out | warming liquids; nucleation at the die edge; Tween wetting PTFE | read weight wrong; vent leaks | CV area check; PE1 decay (cell height); drip tray | HQDP at 25 °C (D8); fill at 40 µL/min through the pocket; vent test in M3/M6 | 4/3/2 |
| FM11 | Reference drift > 20 mV or within-run shift > 2 mV | Au QRE in a pocket with changing HQ/BQ (docs/15 W5); Cl⁻ change | read weight change; background change | M5a (e); control drift per chamber | fixed Cl⁻ (50 mM NaCl); pocket refreshed every flush; Ag/AgCl if available | 3/3/3 |
| FM12 | Cadence outside 30.0–33.0 min or Inject Start jitter > 0.25 min | Empower injection overhead (UNVERIFIED) | an actuation falls in a read window | scheduler/watchdog | movable steps re-placed; flag or fault; Stage 0 measures the overhead | 3/2/1 |

Tolerances that matter most: cell height 0.200 mm (L1 sheet + L1b film; ±10 % → τ ± 21 %, read weight 0.916 → ≈ 0.89 at
+10 %, measured per card from the PE1 decay); stub lengths ≤ 0.5 mm (escape 0.2–0.5 % → 4.8–5.6 % at 1 mm); magnet gap
0.16 ± 0.05 mm (drag margin 3.0× → ≈ 2×); MC volume ±1.7 % (moulded cavity, systematic per lot, UNVERIFIED tolerance); die
position ±0.05 mm on datum edges (WE1 rim 50 µm; fingers must stay inside the lanes).

---
## 10. Staged development plan with gates

Rule (user decision 4, 2026-11-12): **M5a (weeks 6–8) is the only cartridge work before G1; everything else for the
cartridge waits for G1 (docs/06 §4.11, weeks 7–8) and E1.2b.** Risks A1–A5 are those of docs/12 §3.11; A6 (read
background) and A7 (laminate valve) are added.

### 10.1 M5a — pre-G1 read-background test (approved; weeks 6–8; cost class low)

**Purpose.** Decide the read mode (three-window step read vs R-flow) with a drift-corrected acceptance and with
representative dock actuation noise running; test the bottom contact route; measure the pre-electrolysis escape on Au at
3 mM in the cell geometry (complement to E1.2b, which uses carbon, 1 mM and a bulk divided cell; docs/15 N9). Runs only
after E1.1/E1.2/E1.2b and must not delay G1a (week 5) or G1.

**Set-up.**
* 5–10 catalogue Micrux Au thin-film dies: single-electrode dies (DI_MICRUX_SINGLE, geometry UNVERIFIED) or IDA dies with
  both combs joined as one WE (BASI_IDA, PALMSENS_IDA: 10 × 6 mm, Au RE and CE on the die).
* Clamp cell reproducing §2: 140 µm COC foil floor, laser-cut 0.175 mm COC sheet + 25 µm adhesive film (cell 2.6 × 2.0 ×
  0.200 mm over the WE, or the WE area the die allows, ≈ 5 mm²), two lane stubs ending at clamped TPE flat-floor valves —
  one cell with **0.5 mm**, one with **1.0 mm** stubs; a fill path through the die's RE/CE region where its geometry
  allows (otherwise an external CE/RE through a 0.2 mm channel, noted as a deviation); pogo pins **from below through a
  contact window** (§2.7); PMMA/PEEK clamp; grounded Faraday box; block at 25.0 ± 0.2 °C.
* Gamry Reference 600+ (in hand); docked salt-bridge Ag/AgCl reference (docs/02 §5.2 approach) for the QRE log, read by a
  high-impedance (≥ 10¹² Ω) voltage input (to be selected).
* **Dock noise sources** (representative, to be selected; each switched by the PC): a solenoid plunger pressing a TPE
  coupon on a foil 20 mm from the die; a stepper motor with chopper driver moving a 2 × 2 × 4 mm NdFeB magnet 0.16 mm under
  a foil 10 mm from the cell; a syringe pump (gen-1 SIA pump or Cavro/PSD class) pumping water in a line 50 mm away; a
  Peltier module on PWM; a reed relay.
* Solutions: Stage-1 3 mM HQDP in 0.1 M Tris pH 9.5, 1 mM MgCl₂, 50 mM NaCl; HQ standards (Stage-1).

**Protocol.**
1. **CV on Au:** E_det (lowest potential on the HQ plateau), E_rest window (neither HQ oxidation nor BQ reduction), Au oxide
   onset; E_rest check: 30-s E_rest hold on 100 nM HQ.
2. **Quiet blank reads:** ≥ 30 R3 reads (30 s pre-rest, 3 × 60-s windows, 15-s rests) on fresh substrate fills per die, ≥ 3
   dies, over ≥ 3 days; from each read: Q_net = Q_a − 2Q_b + Q_c, the linear drift (Q_c − Q_a)/(2Δ·T), the curvature term,
   and — from the same data — Revision A's Q_a − Q_b for comparison. Fixed range plan vs autorange.
3. **Noise-source arms:** the same reads with each source (i) actuating during E_det windows, (ii) actuating only in the
   E_rest segments, (iii) off; randomised order, ≥ 10 reads per arm and source.
4. **Collection:** HQ standards 10–300 nM in the cell → Q_net vs 2F·V·c → read weight (predicted 0.92 at 25 °C).
5. **Pre-electrolysis and escape:** substrate spiked to 10⁻⁴ mol/mol HQ; flush → PE1 → 3-min hold → PE2 → 11-min hold → R3;
   escape = excess Q_net over unspiked fills / added HQ charge; both stub lengths (predicted 0.2–0.5 % vs 4.8–5.6 %).
6. **QRE:** Au QRE vs the docked Ag/AgCl over 8 h (a fill every 31 min) and within every read (window a vs window c).
7. **Contact route:** pad-to-WE leakage with a wet cell; contact-loop resistance over 8 h.

**Acceptance (quantitative, fixed before data):**

| ID | Quantity | Acceptance |
|---|---|---|
| M5a-1 | SD(Q_net) on blank fills, drift-corrected (three-window), sources in the planned state (off in windows), n ≥ 30 per die, ≥ 3 dies | **≤ 0.05 nC** |
| M5a-2 | curvature residual \|d₂\|·Δ²·T; day-to-day shift of mean Q_net | ≤ 0.025 nC in ≥ 95 % of reads (d₂ ≤ 0.27 pA/min²); ≤ 0.05 nC |
| M5a-3 | read weight on HQ standards; die-to-die slope CV | 0.92 ± 0.05; ≤ 5 % |
| M5a-4 | escape with 0.5 mm stubs (and the 1.0 mm cell as model check) | **≤ 1 %** (1.0 mm cell ≥ 3 %) |
| M5a-5 | E_rest hold charge; QRE drift | ≤ 1 % of Q_a; ≤ 20 mV / 8 h and ≤ 2 mV between windows a and c |
| M5a-6 | SD(Q_net) with sources actuating only in E_rest segments | ≤ 1.2 × the quiet value → tidal strokes allowed in rests (+0.014 P); arm (i) reported |
| M5a-7 | pad-to-WE leakage; contact-loop stability | ≥ 5×10¹² Ω; ≤ 0.1 Ω drift over 8 h |

**Decision.** M5a-1, -2 and -3 pass → the step read is retained; the measured SD enters scratch model runs as §1.3
(`hw.gamry.noise_rms_flow` pinned to SD/7.75 s) until a model extension exists. Any of them fails → R-flow mode (no
credit; the headline of §1.3 is already the no-credit case) and the WE2 channel gets its own test in M5. M5a-4 fails → the
credit is dropped (headline unchanged); S4a then has no rescue on A.

### 10.2 What the gen-1 programme answers for A (no cartridge needed)

| Question for A | gen-1 experiment | Feeds |
|---|---|---|
| bead-dose CV of a cooled, agitated reservoir over 8 h, incl. intermittent agitation (reads pause the rocker) | E2.2 (docs/06) | §5.1, FM5 |
| pre-electrolysis removes free HQ; side effects | E1.2b | §3.6, FM8 |
| U1 conjugate NSB, U3 free HQ / k_h, conjugate bottle ageing (≤ 24 h) | E1.3 (+ ageing arm), E1.2 | G1; §5.2 |
| SM-FL carry-over with a better needle wash (budget 3×10⁻⁵) and the second blank after a challenge | E1.10, extended by the flush programme | §8.3 row 1 |
| Inject Start wiring, injection overhead (cadence), Loop Offline at 5.4 min, BSM 1 → 100 µL/min steps | S0.3 and Stage-2 commissioning | §7.3 |
| Empower Toolkit sample-set insertion (blank-check mode A) | Waters question Q5 (docs/02) | §7.4 |
| phosphate tolerance and ULOQ at 3 mM HQDP; ALP with 50 mM NaCl | E1.7 (+ NaCl arm) | §3.5.5, §3.5.6 |

### 10.3 Stage C1 — mock-ups (after G1 GO / GO-WITH-LEVER and E1.2b; weeks 9–16, parallel to gen-1 Stage 2)

Prototype route: laser-cut COC sheets and TPE sheets on 140 µm COC foil, milled COC upper bodies, adhesive or solvent
lamination (docs/11 §1.3), a machined anvil plate with windows and slot, magnets on Z units and a motorised stage,
catalogue Micrux dies; PDMS only for visualising bead motion, never for electrochemistry (docs/11 §1.4).

| Mock-up | Retires | Method | Acceptance (quantitative) |
|---|---|---|---|
| **M1** collection, gather, drag, bead-out, BW | A1 | IC + funnel + 15 mm lane + J + WLc + cell + BW in the §2 laminate on the anvil; fluorescent M-280 SA beads (blocked as docs/06 §4.0); gap 0.16 mm; n = 20 transfers; **whole-path fluorescence imaging** (floor, wall foot, funnel, lane, J, stubs, cell, BW) | transfer ≥ 0.95 mean, **CV ≤ 5 %**; floor beads after the 3-pass gather ≤ 1 %; **≤ 10 beads** per pass at J + WLc + stubs and in the cell after bead-out; ≤ 1 bead in IC_k after WL refresh + cleaning; v_max ≥ 0.5 mm/s; capture half-width ≥ 2 mm at 0.3 mm/s; pellet never at an air–liquid interface during partial drains (video); BW retention ≥ 99.9 % at 40 µL/min |
| **M2** chamber mixing, recovery, wash | A2 | 185 µL foil-floor chamber with the tangential jet and the §7.1 pause pattern vs rotated tube; IgG spike recovery after 28.5 min; free conjugate in the drag medium by ALP activity | capture ≥ 0.80 of the rotated tube (docs/06 E3.3 criterion); recovery ≥ 0.90; free conjugate ≤ 2×10⁻⁴ of the incubation level (predicted 1.5×10⁻⁴) |
| **M3** dosing | A3 | 20 bead doses through P_b and C_k over 8 h with rocker pauses; 20 conjugate fill-to-vent doses; C_k chase efficiency; vent wet-out after 20 fills | bead CV ≤ 5 %, 8-h trend ≤ 5 %; conjugate CV ≤ 5 %; ≤ 10⁻³ of a dose left in C_k after a 3 µL chase; no vent wet-out |
| **M4** laminate valve | A4, A7 | flat-floor TPE valve on foil, in anvil and slot (4 mm, ≤ 1.5 N) variants; 100 cycles (≥ 3× the busiest valve in the fallback mode) with bead suspension, 1 % BSA conjugate buffer, 3 mM HQDP pH 9.5; leak at 20 and 50 kPa; burst 3 bar; EIS across a closed valve; closing transient into a sealed 1.34 µL cell; beads under a gate | leak ≤ 0.1 µL/min at 20 kPa after 100 cycles; ≥ 1 GΩ closed; transient ≤ 5 kPa; slot foil deflection ≤ 20 µm; ≤ 2 beads retained per gate per 20 passes; no delamination |
| **M5** readout on the custom die | A5, A6 | as M5a on the custom die (WE1 + fingers ∥ WE2, pocket, contact route), plus the R-flow WE2 channel | M5a acceptances; R-flow baseline-corrected SD ≤ 0.05 nC |
| **M6** thermal, bubbles, dew point | FM10 | two-zone anvil mock-up with a laminated card; 8 h of fills | zones ±0.2 °C and 4–8 °C; no bubble in the cell in 20 fills; electrode-bay RH margin ≥ 5 K |
| **M7** integrated single chamber | system | one IC + lanes + cell on a laminated card with a catalogue or custom die, gen-1 reagents, sample by syringe pump; 10 blanks + 3 × (1, 10, 100, 1000 pg/mL); 5 × (100 ng/mL → B1 → B2) with the post-high cycle off and on | LOD ≤ 1.5 pg/mL (G2 go threshold, `gates.yaml` G2 `lod_pgml`); carry-over ≤ 1×10⁻⁴ (raw); PE2 flags every challenge; with the cycle on, B1 within blank + 3 SD |
| **M8** two-chamber timing (new; docs/15 §5 item 4) | S3 | dock prototype with both chambers, the scheduler, the full step table at C = 31, buffer and beads only, 20 consecutive runs | zero actuations inside read windows (event log); result ≤ 57.0 min in every run; SD(Q_net) on blank fills under the full schedule ≤ 1.2 × the M5a quiet value |

**Gate GC1** (end of C1): M1, M4, M5 and M8 pass (A1, A4, A5–A7 retired); M2/M3 pass or have a defined fix; measured
mixing factor, dose CV, transfer, read SD and escape entered into scratch model runs (no credit unless M5a-4 and M5
passed). GO → C2.

### 10.4 Stage C2 — prototype cards and dock (after GC1 and gen-1 G2, ≈ weeks 17–28)

10–20 laminated cards with the custom die; first full dock (21 plungers, anvil, two M_c Z units, carriage, M_h lift, five
pumps, three thermal zones, electrode bay with pogo block, controller with watchdog); automation as §7.5. Tests on the
Waters stack: three 14-run cards in staggered operation. **Gate GC2:** LOD ≤ 1.5 pg/mL per card and ≤ 1.0 pooled (G3
target, `gates.yaml`); blank CV ≤ 0.10; card-to-card slope CV ≤ 10 % per chamber; carry-over ≤ 1×10⁻⁴ (100 ng/mL
challenge, both path classes); **time to result ≤ 57 min (≥ 3 min margin) in every run**; zero actuations in read windows;
zero valve failures in 3 cards; docking leak test 100 %. GO → C3.

### 10.5 Stage C3 — moulded pre-series and validation

Upper-body mould (MOQ 100, CS_FAB), series lamination (sheet process UNVERIFIED), bonded die; validation per docs/06
Stage 4 (G3: LOD ≤ 1 pg/mL, blank CV ≤ 0.10, carry-over ≤ 1×10⁻⁴, ≤ 60 min).

### 10.6 Order relative to the gen-1 gates

```
gen-1:  Stage 0/1A --E1.1-E1.2-E1.3-- G1a(wk5) --E1.2b, E1.4-1.10-- G1(wk7-8) -- Stage 2 (wk 9-16) -- G2(wk16) -- Stage 3
cart A: C0 desk + quotes ------------------ [M5a, wk 6-8, approved] --|  C1: M1-M8 -- GC1 --| C2 -- GC2 -- C3
                                            STOP at G1 or E1.2b FAIL of the read plan -> no C1 spend (C0 stays desk work)
```

---

## 11. BOM additions by stage

Cost class [assessment, no prices seen unless stated]: **low** < €1 k, **medium** €1–10 k, **high** > €10 k.

| Stage | Item | Qty | Cost class / price | Source |
|---|---|---|---|---|
| M5a | Micrux catalogue Au thin-film single-electrode or IDA dies | 5–10 | price on request → low–medium | DI_MICRUX_SINGLE, BASI_IDA, PALMSENS_IDA |
| M5a | laser-cut 0.175 mm COC sheets, 25 µm adhesive film, 140 µm COC foil, TPE coupons, PMMA/PEEK clamp, pogo pins, Faraday box | — | low | docs/11 §1.3, DARWIN_CS4CH |
| M5a | noise-source kit (solenoid, small stepper + chopper driver, Peltier module, reed relay), high-impedance voltage input for the QRE log | 1 | low (to be selected) | — |
| C1 | laminate coupons and mock-up cards (COC sheet, TPE, foil), milled COC upper bodies | 20–40 | medium (price on request) | CS_FAB, DARWIN_CS4CH |
| C1 | anvil plate with windows and slot; NdFeB magnets (10×10×5, 2×2×4, 3×3×4, 3×3×3 mm); two Z units; motorised X–Y–Z stage | 1 set | medium (Zaber, price not read) | ZABER_SW |
| C1 | syringe pumps for S_b, S_A, S_IC, S_RC duties; cooled rocking vial holder | 4–5 | medium (Cavro Centris / Hamilton PSD/4, price not read) | TECAN_CENTRIS, HAMILTON_PSD4 |
| C1 | pressure controller, 2 channels | 1 | medium | FLUIGENT_FLOWEZ, ELVEFLOW_OB1 |
| C1 (optional) | ChipShop membrane-valve chip Fluidic 1367 as a reference only (foil valve, single use — not the TPE valve, docs/15 N7) | 10 | €34.40 each from 10 (€42.20 single) | CS_1367 |
| C2 | custom electrode die (WE1 + fingers, WE2, CE, RE, contact loop, pads on the lower face at one end; Au; Ag/AgCl option), wafer run | 1 run | high (price on request) | MICRUX_TF, IMT_FLYER |
| C2 | laminated prototype cards with PTFE vents | 10–20 | medium–high | CS_FAB |
| C2 | dock: 21 plunger actuators, anvil with face seals, 2 Z units, carriage, M_h lift, 5 syringe pumps, 3 Peltier zones, controller with watchdog, electrode bay with pogo block and relay, sensors (T, RH ×2, leak, pressure, card ID), flow sensors | 1 | high (mostly "to be selected") | docs/11 §5; §6.2 |
| C3 | upper-body mould insert, moulded pre-series (MOQ 100), series lamination, die bonding | 100 | high (price on request) | CS_FAB |
| all | reagents as gen-1 (HQDP at 3 mM, ≈ 30 µL per run vs ≈ 315 µL in gen-1) | — | as docs/07 | docs/09 §3.3 |

Reused from gen-1 (docs/07): Gamry Reference 600+, LabJack-class DAQ, Python orchestration, SM-FL/BSM; the SIA pump class
is reused for S_b; gen-1's IDEX valves are not needed.

---

## 12. Open questions and UNVERIFIED list

### 12.1 Open questions (for the user or the next agent)

1. **Is the cartridge justified without an LOD gain?** Revision B: 3.67 / 0.150 without credit vs gen-1 3.5 / 0.16; equal
   after screening (1.34 / 0.328 vs 1.3 / 0.32). Its case is throughput (31 vs 56 min per sample), buffer (≈ 1.9 vs 5–6 mL per
   determination) and automation — and it now carries 10 samples per 8-h card (docs/15 §6 Q2, still open).
2. Blank-check mode A (Empower Toolkit inserts a buffer-vial line; UNVERIFIED, Waters Q5) or mode B (injection n+2
   diverted, sample n+2 lost and re-queued)?
3. QC per card: 4 slots (one blank and one control per chamber; 10 samples) or 3 (11 samples, one chamber without an
   end-of-card check)?
4. Allow tidal strokes in the E_rest segments if M5a-6 passes (+0.014 in P)?
5. If the R-flow fallback becomes routine: move RS to the cold zone with a warm-up path (bubble risk)?
6. Second potentiostat channel for WE2, or the dock relay (WE1 ∥ WE2 / WE2 alone)?
7. Laminate and foundry questions: 0.175 mm through-cut COC sheet (tolerance, series process); TPE–COC lamination under
   cycling; 25 µm die film (creep, leachables, HQ/BQ sorption); 0.15 mm shim for the 50 µm WE2 channel; die datum edges;
   pads on the lower face at one end; Ag/AgCl on the die; PTFE vent heat-staking on COC.
8. For the owners of other documents (not edited here): docs/12 §0 and docs/14 §F still show Revision A's or docs/12's A
   (docs/15 S10); docs/14 contamination pinning (S9); docs/06 E2.4 residual-bead criterion 10⁻³ (N10); docs/10 Kim2015
   key collision (N5); Otieno2014 and Sun2008 wording (N4, W10).
9. Model extensions (docs/09 §5.4) remain unbuilt by user decision; the step-read background (white noise, drift
   curvature, range offsets) is an item for such an extension.

### 12.2 UNVERIFIED values used in this document

| Value | Where used | Status |
|---|---|---|
| M-280 saturation magnetisation 1×10⁴ A/m; saturation above 0.15 T | §3.3.2 | UNVERIFIED (docs/15 N8); M1 measures follow speed |
| NdFeB B_r 1.3 T; near-wall drag factor 3; bead–foil friction | §3.3.2 | UNVERIFIED; M1 |
| Young's moduli of COC (2.6 GPa) and TPE (≈ 2 MPa), Poisson 0.35 | §2.1, §2.4 | UNVERIFIED; M4 |
| C_dl ≈ 20 µF/cm² for thin-film Au | §3.5.4 | UNVERIFIED (repository note) |
| E_rest window, E_det plateau, Au oxide onset at pH 9.5 | §3.5.4 | M5a CV |
| baseline drift 5 pA/min and its curvature | §3.5.4 | `hw.gamry.baseline_drift` UNVERIFIED; M5a-2 |
| Gamry range offsets and their stability | §6.3 | not read; M5a |
| Au QRE drift; Ag/AgCl availability on custom dies | §3.5.5 | UNVERIFIED; M5a-5 |
| substrate conductivity (≈ 0.1–0.2 S/m + 0.5 S/m from 50 mM NaCl); NaCl effect on ALP | §3.5.5 | UNVERIFIED; E1.7-type check |
| Tris pKa ≈ 8.1 | §3.5.5 | UNVERIFIED |
| K_m 0.1 mM, k_cat 1000 s⁻¹, free HQ 10⁻⁵, k_h 10⁻¹⁰ s⁻¹ | §3.5.3, §3.6, §5.2 | repository values, low confidence |
| unstirred capture factor 0.5 | §1.3, §3.2.2 | `ma.capture.in_vial_unstirred_rate_factor` UNVERIFIED |
| loop ID 0.5 mm; transfer 0.90 at 1.5 loop volumes | §3.1 | `hw.smfl.loop_inner_diameter` UNVERIFIED |
| injection overhead ≈ 1 min (cadence 31 min); docking time ≈ 12 min | §7.3, §5.2 | UNVERIFIED; Stage 0, C2 |
| SM-FL protein carry-over 3×10⁻⁵ needed (nominal 10⁻⁴) | §8.3 | `hw.smfl.carryover_protein_conjugate` UNVERIFIED; E1.10 |
| drain residual ≤ 5 µL; partial-drain residual 30 µL keeps the pellet covered | §3.2.3, §3.4 | UNVERIFIED; M1/M2 |
| Wang2013 2×10⁻⁵ carry-over applied to protein | §3.4 | measured for a small molecule |
| chamber mixing factor; analyte loss to blocked COC | §3.1, §3.2.2 | M2 |
| flat-floor TPE valve leak, isolation, endurance (no evidence for TPE on COC) | §4 | M4 |
| foil deflection at slot valves | §2.1 | Derived with UNVERIFIED moduli; M4 |
| PTFE vent wet-out | §3.2.4 | M3/M6 |
| laminate tolerances (sheet 0.175 mm, film 25 µm, shim 0.15 mm), die position ±0.05 mm, MC ±1.7 % | §2, §9 | UNVERIFIED |
| COC and water thermal diffusivity, gas solubility vs T, Magnus constants | §6.5–6.6 | UNVERIFIED |
| Empower Toolkit sample-set insertion; Empower pressure-limit setting; BSM flow-step programme at 1 ↔ 100 µL/min | §7.3, §7.4, §4 | UNVERIFIED (docs/02 §3, Q5) |
| ToolkitPy step commands | §7.5 | UNVERIFIED (docs/02 §4.3) |
| plunger, Z-unit, pogo forces; part numbers of actuators, Peltiers, relay, pogo pins, scanner | §6.2 | to be selected |

---

## Appendix A — scratch scripts and runs (not in the repository)

All scripts are in the session scratchpad, folder `revB/`; model runs use a copy of the repository installed there
(`pip install -e .` in the copy) and the docs/12 Appendix A helpers as reproduced in docs/15 (`runs.py`: `Aarch`, `A_ps`,
`pre_el`, `stir`, `S3`, `L67`, `S4a`); n = 2000, seed 20261111 (L.mc default).

```python
# Revision B architecture: docs/12 A (OS design + chamber/timing overrides) with the Revision B timing and cell volume
def AarchB(t_inc=25.33, t_acc=11.0, vol=1.34):
    d = {"ma.timing.in_vial_incubation": t_inc, "hw.timing.accumulation_time": t_acc,
         "hw.smfl.loop_flush_volumes_for_transfer": 6.6, "ma.timing.post_sample_wash": 1.5,
         "hw.timing.substrate_fill": 0.5, "ma.timing.bead_flush_and_clean": 2.0, "hw.timing.readout_time": 1.0,
         "ma.geometry.magnetic_trap_volume": vol}
    return replace(L.base_arch("OS").with_design(**os_rec).with_design(**d), detector="thin_layer")
Bps = lambda p, dil=1.85: S3(stir(dil)(p).with_values({"ma.nsb.surface_factor_tubing": 0.01}))
EFF = 22.15 + 0.5 * 6.35                     # stirred + unstirred factor x paused (sched.py)
L.mc(AarchB(EFF), Bps(ps0), n=2000, lod_scale=1/0.90)                         # headline, no credit
L.mc(AarchB(EFF), pre_el(Bps(ps0)), ...)                                      # credit x0.01 (pre_el(..., 0.07) for 1-mm stubs)
L.mc(AarchB(EFF), Bps(L67(ps0)), ...); L.mc(AarchB(EFF), Bps(S4a(ps0)), ...)  # screening, S4a
L.mc(AarchB(EFF), Bps(ps0).with_values({"hw.gamry.noise_rms_flow": SD / 7.746}), ...)   # read-SD rows
```

| Script (`revB/`) | What it computes | Used in |
|---|---|---|
| `mag_b.py`, `mag_far.py` | block fields (surface-charge integration, B_r 1.3 T), point forces, 2-D gather trajectories with friction, lowered and neighbouring magnet forces | §3.3.2 |
| `sched.py` | the step table, overlap check of all activities against all read windows over k·C (k = −4…4) with ±0.25 min guard, exclusive resources, cell and chamber cycles, tidal pauses, card duration, PE2 hold; parameters `T_inc=28.5 T_acc=11 C=31 clean=7.5` (and cadence/split sweeps) | §7.1, §1.3 |
| `escape_b.py`, `escape_b2.py`, `escape_b3.py` | escape of free HQ from stubs and the CE/RE pocket after the last removal (method of docs/15 `rev15/escape.py`); `escape_b3.py` with t_fill 26.65, t1 34.10, t2 52.75 min is the final geometry | §3.6 |
| `read_b.py` | three-window read: product weight, constant-turnover term, drift and white-noise requirements; comparison with the Revision A pair | §3.5.2, §3.5.4 |
| `runB.py`, `runB2.py`, `runB3.py`, `runB4.py` | nearest-model rows (first trial timing; incubation/accumulation splits; final rows; step decomposition) | §1.3 |

