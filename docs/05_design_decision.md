# 05 — Design optimisation and architecture decision (Task 4)

> **Status note (orchestrator, after final review).** The Monte Carlo defect described in §1.1 and §7 has since been
> fixed in `src/elisa_sim/params.py` with a regression test (64 passed); the reviewer confirmed the numbers in this
> document are unchanged by the fix. docs/08 lists open findings on this design — in particular the shared
> bead + conjugate reservoir (B4), the G1 decision rule (B3) and the phosphate-containing A1 buffer (B1).

Status: 2026-11-11. Inputs: docs/00–04, `params/*.yaml`, `src/elisa_sim/` (audited model, docs/04). This task did
**not** change model physics. It added scripts under `scripts/`, outputs under `results/design/`, and a
`design_levers` section to `params/model_assumptions.yaml`. Every number below is a model prediction unless it is
marked as a literature value. "P" is the fraction of Monte Carlo draws, not a confidence level. The intervals are
scenario ranges built from the YAML bounds (docs/03 §7), not statistical confidence intervals.

## 0. Summary

**Decision.** Build one platform: **magnetic-bead capture with a timed incubation inside the instrument**,
an integrated bead trap on the reactor-isolation valve, a flow interdigitated-array (IDA) cell read with two
potentiostat channels, and ALP/hydroquinone-diphosphate (HQDP) chemistry. Beads are renewed every run.
* **Primary:** run the platform in **one-step mode** (beads and ALP conjugate dosed together into the incubation
  chamber).
* **In-platform fallback:** switch to **sequential mode** (conjugate injected onto the trapped beads) if no
  detection reagent with t½ ≥ 1 h is found.
* **Backup design:** a bead-free **fixed packed micro-bed** (0.5 µL, regenerated), in case bead handling fails.

**User decisions applied (docs/00, "Decisions by the user").** (1) Sample vials contain sample only; reagent may
not be supplied in vials or added by the end user, so mixing must be done by the instrument. The modelled one-step
in-vial format (beads + conjugate pre-dispensed in the sample vial) and the sequential in-vial format are therefore
**inadmissible** and appear below only as reference points. (2) The 100 µL limit is the injected volume, so the
installed full-loop injection (100 µL injected, about 200 µL drawn) is the design basis; the PLNO 75 µL variant is no
longer needed. Section 4.0 shows that the one-step format's advantage (sample, beads and conjugate incubated together)
can be recovered by automated means: a timed, stirred in-line chamber fed by an added bead/conjugate dispenser. That
is the primary design. Independently of decision 1, in-vial pre-mixing would also have failed on timing: the
calibration slope changes by ±6 % per ±2 min of incubation and doubles between 35 and 120 min (section 4.3).

> **Revised headline (revised after final review, docs/08 §10).** The table below is the docs/05 evaluation and is
> kept for the record. After the review corrections — Stage-3 default detector a commercial single-channel
> thin-layer cell (S9), chamber stirring factor sampled and the 1/0.96 transfer applied before P (S13), phosphate
> K_i marked UNVERIFIED with bounds 0.2 µM–1 mM (S10) — the model gives (n = 2000, `results/design/final_designs.md`):
> **primary (one-step chamber) median 3.5 [0.51–158] pg/mL, P ~0.16; after L6 + L7 1.3 [0.34–9.3], P ~0.32**;
> sequential chamber 3.0 [0.56–26], P ~0.13; after L6 + L7 2.1 [0.49–16], P ~0.17; backup bed 3.4 [0.65–33], P 0.09;
> after L6 + L7 2.8 [0.59–23], P 0.11. With the optional flow IDA: primary P ~0.18 (0.39 after L6 + L7). Beads and
> conjugate are now held in separate reservoirs (B4). Step-by-step attribution: `results/design/review_changes.md`.

**Predicted performance.** Monte Carlo, n = 2000. Success means LOD ≤ 1 pg/mL **and** ULOQ ≥ 1000 pg/mL.

| Design | Before optimisation: nominal / median [5–95 %] / P(success) | After optimisation: nominal / median [5–95 %] / P(success) | With reagent and substrate screening (L6 + L7) | Time to result |
|---|---|---|---|---|
| One-step beads in the sample vial (**reference only, inadmissible**) | 0.56 / 2.1 [0.44–36] / 0.21 | 0.32 / 1.3 [0.30–21] / 0.35 | 0.80 median, P 0.57 | 59.5 min |
| **Primary: one-step, timed in-line chamber** | (same chemistry as above) | 0.56 / 2.0 [0.36–73] / ~0.28 | 0.93 median, P ~0.55 | 56.1 min |
| In-platform fallback: sequential mode, chamber | 2.6 / 13 [1.4–150] / 0.02 (sequential beads, baseline) | 0.36 / 1.7 [0.39–15] / ~0.28 | 1.2 median, P ~0.38 | 58.1 min |
| **Backup: fixed packed micro-bed** | 19 / 49 [5.1–600] / 0.00 | 0.74 / 2.8 [0.52–31] / 0.16 | 2.2 median, P 0.21 | 51.5 min |

In the before-optimisation column, the primary's chemistry is the same as the reference row and its sequential
mode starts from the baseline sequential-bead row (B-mag-IDA). Sources:
`results/design/final_designs.md`, `optimisation_baseline.md`, `inline_chamber.md`.

**Honest probability.**
* The model gives the primary about 0.28 as specified today, and about 0.55 if the detection reagent and the
  substrate lot pass screening.
* My judgement of the real-world probability, given what the model does not capture (section 4.5), is **about 15 %
  today**. It rises to **about 40–50 % if the three gating measurements U1–U3 come back favourable**.
* **1 pg/mL is unlikely unless two levers are confirmed at the bench:**
  1. the IgG–ALP conjugate NSB on blocked streptavidin beads is at or below the published plate anchor (label
     factor ≤ 0.04, i.e. blank-equivalent ≤ ~1 pg/mL on beads);
  2. the free hydroquinone in the HQDP lot is ≤ 10⁻⁵ mol/mol.
* At the kill thresholds of section 5 (label factor 0.15, or free HQ 10⁻⁴) P(success) falls to 0.02–0.15 for every
  admissible design (`results/design/kill_thresholds.md`); at the S1/S4a levels (NSB ×25, free HQ 10⁻³) it is
  ≤ 0.03. Recovery would then need an immune-complex transfer step (lever L4).

## 1. Design optimisation with the model

### 1.1 Problem, constraints and method

**Formats optimised.** Each is an existing registry architecture with ALP/HQDP:

| Key | Format | Starting architecture | Reagent in the sample vial (as modelled)? | Needs bead handling? |
|---|---|---|---|---|
| OS | One-step beads | B-mag1-IDA | yes (as modelled) | yes |
| SQ | Sequential beads | B-mag-IDA | yes (beads in vial) | yes |
| FRB | Fixed packed micro-bed, Scheme B | B-bed-IDA | no | no |
| FRC | Fixed chip bead bed, Scheme C | C-bed-IDA | no | no |
| CAP | Fixed open capillary | B-cap-TL | no | no |

Note that the sequential bead format also captures in the vial, so as modelled it also puts reagent (beads) in the
sample vial; after the user's decision, OS and SQ as modelled are reference points and their admissible versions
are the in-line chamber modes of section 4.0. The only
formats needing neither are the fixed reactors.

**Objective.** Median over n = 300 Monte Carlo draws (fixed seed, so all designs see the same random numbers) of
L_eff = LOD × max(1, 1000/ULOQ). Ties are broken by P(success). P(L_eff ≤ 1) is exactly P(LOD ≤ 1 and ULOQ ≥ 1000).
**Search.** Coordinate search over discrete grids (`design_lib.SPACES`), at most 4 sweeps. **Reported numbers.**
Re-evaluated with n = 2000. The Monte Carlo sampling error on P at n = 2000 is about ±0.01.

**Hard constraints** (`design_lib.constraint_violations`). A design violating any of them is rejected.

| Constraint | Value | Basis |
|---|---|---|
| Time to result | ≤ 60 min, including in-vial or in-chamber incubation | brief |
| Range | nominal ULOQ ≥ 1000 pg/mL | brief |
| Pumped flows | ≥ BSM minimum (1 µL/min); loop matches injection mode | model's own check, docs/04 §3.4 |
| Loop flush | ≥ 2 loop volumes | loop model validated only there (docs/02 table) |
| Isolated tubing | ≥ 0.01 m | trap or bed screwed into the valve ports; `ma.design_levers.min_isolated_connection_length` |
| Bead loading flow | ≤ 100 µL/min | trap efficiency 0.9 is assumed (UNVERIFIED) only at the baseline flow, so higher flow would gain by artefact; `ma.design_levers.max_bead_loading_flow` |
| Trap length | ≥ 1 mm | magnet zone; UNVERIFIED design rule |
| Washes | post-capture wash ≥ 1 min; wash after conjugate ≥ 2 min | wash efficiency is not modelled, so shorter washes would gain by artefact |
| Chip channel | ≥ 3 mm | IDA plus margins |
| Bed pressure drop | ≤ 10 MPa (Kozeny–Carman) | `hw.reactors.packed_microbed_10uL.pressure_limit` |
| Injection | installed 100 µL loop, full-loop injection (`FL_100`), 100 µL injected | brief, installed configuration; user decision 2: the limit applies to the injected volume |

**Model bug found and worked around.** `elisa_sim.montecarlo.used_keys` records parameter accesses on the copy
made by `apply_design`. For any architecture with a non-empty `with_design(...)`, it therefore returns no keys.
**Monte Carlo then samples nothing**, and P jumps to 0 or 1. `sensitivity.one_at_a_time` has the same problem.
* Reproduce: `used_keys(B-mag1-IDA.with_design(accumulation_time=10))` returns 0 keys against 100 for the plain
  architecture.
* The docs/04 §3.7 design table used nominal values only, so it is not affected.
* Workaround in `design_lib.mc`: apply the design to the parameter set first, then run the Monte Carlo on the
  architecture without a design. The workaround reproduces the baseline exactly (median 2.32, P 0.21 for both).
* **Fix needed in src (owner: the model task):** probe the accessed keys on `apply_design(arch, ps)`. I did not
  change src, because this task may only add physics there.

### 1.2 Results

`results/design/optimisation_baseline.md`, audited parameters, n = 2000:

| Format | Baseline: nominal / median [5–95 %] / P(LOD≤1) / P(success) | Optimised: nominal / median [5–95 %] / P(LOD≤1) / P(success) | ULOQ (pg/mL) | Time to result (min) |
|---|---|---|---|---|
| OS one-step | 0.56 / 2.1 [0.44–36] / 0.25 / 0.21 | **0.32 / 1.3 [0.30–21] / 0.38 / 0.35** | 1800 | 59.5 |
| SQ sequential | 2.6 / 13 [1.4–150] / 0.02 / 0.02 (60.5 min: infeasible) | **0.30 / 1.5 [0.37–12] / 0.33 / 0.31** | 1400 | 58.5 |
| FRB packed micro-bed | 19 / 49 [5.1–600] / 0 / 0 | 0.94 / 3.6 [0.60–42] / 0.14 / 0.12; final version (ID 0.5 mm, 10 µL/min): **0.74 / 2.8 [0.52–31] / 0.19 / 0.16** | 1000 | 51.5 |
| FRC chip bead bed | 8.7 / 34 [3.7–500] / 0 / 0 | 0.95 / 3.8 [0.64–46] / 0.12 / 0.10 | 1000 | 45.0 |
| CAP capillary | 25 / 88 [14–710] / 0 / 0 | 2.0 / 6.7 [1.1–65] / 0.04 / 0.04 | 3000 | 50.0 |

**Choice of detector, at the optimum.**
* The flow IDA is best everywhere: thin-layer cells are 1.1–1.5× worse, coulometric 1.2–1.7× worse, and the
  confined wall-jet 3–6× worse.
* At these optima the cell matters more than in docs/04 because the blank is smaller. It is still second-order.

**Optimised design variables** (`results/design/optimum_<FMT>__baseline.json`):

| Variable | OS | SQ | FRB (final) | FRC |
|---|---|---|---|---|
| Isolated tubing (m) | **0.01** (was 0.1) | **0.01** | **0.01** | (integrated chip) |
| Beads per 100 µL | 5×10⁵ | **1.5×10⁶** | – | – |
| Bead-trap volume and inside diameter | 2 µL, **1.5 mm** (length 1.1 mm) | **0.5 µL, 0.75 mm** (length 1.1 mm) | – | – |
| Bed volume, particle diameter, column inside diameter | – | – | **0.5 µL, 50 µm, 0.5 mm** (column/particle ratio 10) | **0.1 µL, 10 µm, 0.2 mm** |
| Conjugate | **0.3 nM** in vial | **3 nM**, 20 µL plug, **3 min** stop | 1 nM, 20 µL, **2 min** stop | **10 µL**, **2 min** stop |
| In-vial incubation (min) | **35** | **35** | – | – |
| Sample load flow; loop flush | 100 µL/min; **2** volumes | 100 µL/min; **4** volumes | **10 µL/min; 2** volumes | **10 µL/min; 2** volumes |
| Accumulation; sweep flow; read window | **15 min; 10 µL/min; 1 min** | **5 min; 10 µL/min; 1 min** | **15 min; 10 µL/min; 1 min** | **7.5 min**; stopped IDA |

Bold marks a change from baseline.

**Active constraints at the optimum** (`results/design/edge_checks.md`):
* OS: time to result (59.5 min), isolated tubing ≥ 0.01 m, bead loading flow ≤ 100 µL/min, flush ≥ 2, trap
  length ≥ 1 mm, and the range (with 1 nM conjugate, ULOQ would fall to 794 pg/mL).
* SQ: time to result, isolated tubing, loading flow, range (trap 0.25 µL or 10 nM conjugate would violate it).
* FRB: time to result. Loading at 5 µL/min would give 1.9 median but takes 91.5 min.
* FRC: chip channel ≥ 3 mm.

### 1.3 Where the gains come from, and what they rest on

The table summarises `results/design/gain_decomposition.md` (cumulative, n = 1000).

| Gain | Size | Physics behind it | Rests on |
|---|---|---|---|
| Isolated tubing 0.1 → 0.01 m | OS ×1.2; **SQ ×4** (median 7.0 → 1.9); FRB ×1.5 | geometric: less conjugate-exposed area whose product reaches the cell | direction certain; size scales with the tubing surface factor (3, range 1–30, **UNVERIFIED**) |
| Lower load flow for fixed beds, 100 → 10 µL/min | FRB ×3–4 | verified transport (capture per unit area rises as flow falls, B ∝ Q at fixed kA/Q) | Wilson–Geankoplis coefficient (recalled), capture k_on and density (sampled) |
| Smaller bed / larger particles | FRB ×2–3; FRC ×3 (0.1 µL) | less NSB area per captured molecule | packed-bed surface factor (**UNVERIFIED**); single-pass capture model |
| Bead number 1.5×10⁶ (SQ) | ×1.25 | faster in-vial capture against bead NSB area | unstirred capture factor (**UNVERIFIED**) and bead surface factor |
| Lower one-step conjugate, 1 → 0.3 nM | LOD neutral, ×0.9; **needed for ULOQ ≥ 1000** | linear NSB vs saturating labelling | linear NSB (**UNVERIFIED**) and the phosphate K_i (2 µM, INHERITED, unchecked; range 1–540 µM) |
| Longer accumulation (OS) | ×1.2 | more product against free HQ and drift | free HQ impurity and drift (**UNVERIFIED**) |
| Sweep 10 µL/min and 1 min window | ×1.1–1.4 | higher IDA generator conversion at low flow | slit solution (verified limits) × IDA gain held independent of flow (empirical) |
| In-vial 30 → 35 min | ×1.05 | capture continues | linear NSB in time (**UNVERIFIED**) |

**What is verified and what is assumed.**
* Verified physics alone gives the fixed-bed gains: flow, bed size, and loop transfer at low flow (validated
  against the Task 2 table). Their absolute size still depends on the packed-bed surface factor.
* The largest bead-format gain, the isolated tubing, is a geometric certainty in direction. Its size depends on an
  unverified surface factor: at factor 1 it is negligible, at 30 it is large.
* No gain depends on the trap-efficiency or wash-efficiency artefacts, because both were excluded by constraint.

### 1.4 Optima on bounds: re-checks

`results/design/edge_checks.md` moves each edge variable one step past its bound.

**One-step:** the optimum is flat at every edge, so none of its gain comes from an artefact.
* Removing the isolated tubing completely gives no gain.
* Loading at 150–200 µL/min would gain 1.4 → 1.3 median, but only because trap efficiency is held constant. That
  is excluded.
* A 0.5-min wash would gain nothing, and is excluded anyway.

**Sequential:** zero tubing would give 1.5 → 1.2 median. That is not buildable.

**Packed micro-bed:**
* The first optimum (50 µm particles in a 0.25 mm column) breaks the column/particle ratio of at least 10, which
  is a packing rule of thumb rather than a model constraint.
* The ratio-compliant 0.5 mm column gives the same LOD (0.98 vs 0.94 nominal). With 10 µL/min and 2 flush volumes
  it improves to 0.74. This is the final backup.
* Loading at 5 µL/min would help further (median 1.9) but breaks the 60-min limit.

**Chip bead bed:** a 2 mm channel would gain nothing meaningful (3.7 → 3.5).

### 1.5 The range constraint is set by an unchecked parameter

The nominal ULOQ of the one-step format is set entirely by phosphate inhibition of ALP. HQDP releases 2 Pi per
hydroquinone, with K_i = 2 µM (`chem.enzymes.alp.phosphate_inhibition_Ki`, INHERITED from OBrien2002/Coburn1998,
not re-checked).
* With the detection reagent screened (more enzyme per analyte), the baseline one-step ULOQ falls to 607 pg/mL.
  With K_i at its high bound it is 34 000 pg/mL. With 5 mM HQDP it is 2300 pg/mL.
* The range criterion used here (log-slope ≥ 0.8) is also stricter than a monotonic 4PL calibration needs.

Range failures in this report are therefore soft. Designing to 3 mM HQDP, or 7.5–10 min accumulation, keeps
ULOQ ≥ 1000 pg/mL in every scenario. Bench item U6 below measures K_i.

## 2. Levers outside the present model

For each lever: what it does, the evidence, a bounded gain, its cost, the bench test, and whether it is
represented in the model. Gains were run as scenarios where an existing parameter can carry them
(`scripts/robustness.py --part levers` → `results/design/levers.md`, on the optimised designs). The bounded inputs
are in `params/model_assumptions.yaml` § `design_levers`, all **UNVERIFIED** magnitudes. No new physics was added
to src: no lever had a sourced quantitative parameter that would justify a model element and a test.

| Lever | Mechanism | Evidence | Bounded gain | Hardware / automation cost | Bench test | In model? |
|---|---|---|---|---|---|---|
| L1 Inert/coated wetted path (PEG/BSA-passivated PEEK trap and stubs) | lower tubing and trap-wall NSB | PEG-diacrylate cut antibody adsorption to < 5 % of uncoated polymer (Larsen2014, Biomicrofluidics); PEG on silicon −80 % (Popat2004, Biosens Bioelectron); BSA coating −88 % on PMMA (Xian2023). All against **uncoated** surfaces, whereas our tubing factor is relative to blocked beads | tubing factor 3 → 1: OS ×1.0, **SQ ×1.25** (P 0.31 → 0.40), FRB ×1.1 | coated tubing or trap; nil automation | conjugate-exposure series on PEEK vs coated 1 cm segments (U4) | yes (scenario on `surface_factor_tubing`) |
| L2 Clean-zone re-trap | release beads after washing and re-trap them in a second trap never exposed to conjugate | geometric argument only | OS ×1.0 (walls are already < 10 % of NSB); SQ ×1.35 | +1 valve position, +1 magnet, +2 min | NSB with vs without re-trap (U4) | scenario (`surface_factor_tubing` → 0.01) |
| L3 Fab′- or F(ab′)₂-ALP conjugate | smaller, Fc-free label, less NSB per molecule and no Fc-mediated binding | Ishikawa group: purified Fab′ conjugates gave lower background (Hashida1985, doi:10.1080/01971528508063024); NSB of a Fab′ conjugate suppressed with normal F(ab′)₂, LOD 5× lower together with other changes (Ruan1986, doi:10.1177/000456328602300106). No paired IgG vs Fab′ number found | NSB ×0.5 (0.2–1): OS median 1.3 → 0.99, P 0.35 → 0.48 | reagent choice only | IgG-ALP vs F(ab′)₂-ALP of the same clone: blank vs exposure on beads (part of U1) | bounded estimate via label factor |
| L4 Immune-complex transfer | capture on phase 1, wash, elute the complex (biotin displacing desthiobiotin), recapture on a clean phase 2; phase-1 NSB stays behind | Ishikawa1990 (doi:10.1016/0009-8981(90)90303-a): 600 molecules ferritin; Hashida1997 (doi:10.1002/(SICI)1098-2825(1997)11:5<267::AID-JCLA5>3.0.CO;2-4): transfer "minimized" conjugate NSB, 10–300× over conventional ELISA; desthiobiotin–streptavidin release by biotin (Hirsch2002, doi:10.1016/s0003-2697(02)00201-4). docs/01 already lists the principle | NSB ×0.1 (0.01–0.5), signal ×0.7 (0.4–0.9): OS median 1.3 → 0.75, P 0.63; **FRB 2.8 → 0.94**. Robust to the NSB scenarios, which other levers are not | second trap or bed, elution reagent line, +5–10 min (time budget is tight: needs the 7.5 min accumulation) | two-stage transfer on beads in tubes: blank and 10 pg/mL with and without transfer (U8) | bounded estimate |
| L5 Reference-channel subtraction (non-immune beads read in parallel) | cancels the correlated part of NSB run-to-run variation | general principle (Frutiger2021 Chem Rev, review); no number for the correlation of conjugate NSB between bead populations | SD × √(2(1−ρ)): ρ = 0.8 gives ×0.63, LOD median 1.3 → 1.1. **No gain for ρ < 0.5** | parallel trap and IDA, needs 3–4 potentiostat channels | blanks on immune and non-immune beads in the same run, 20 runs, compute ρ | bounded estimate via CV |
| L6 Detection reagent screened to t½ ≥ 1 h | more label retained, labelling not equilibrium-limited | Chang2012 range; Kamat2021 high-affinity anti-Fc exists | OS 1.3 → 0.94, P 0.35 → 0.50 | screening only | BLI/SPR (U2) | yes (`koff_detection`) |
| L7 Substrate purified (free HQ ≤ 10⁻⁶) | lower impurity background | Wilson2004 (stable, qualitative) | OS P 0.35 → 0.41 at 10⁻⁶; **at 10⁻³ every design fails** | recrystallisation or lot QC | HPLC-EC of the HQDP lot (U3) | yes (`free_product_impurity`) |
| Washing stringency (reversible NSB) | if part of NSB is reversible, washes remove it | adsorption is partly reversible and becomes less so with time (Wahlgren1995; Marsh2002); surfactant displaces some (Marsh2002; Zhang2020). All at monolayer coverage | 50 % removed: OS 1.3 → 0.99; FRB 2.8 → 1.6 | +1–2 min of 0.05–0.1 % Tween wash | U1 wash-series arm | scenario S3a |
| Conjugate from a dedicated path (SIA module, not the SM-FL loop) | sharp, reproducible conjugate dose; **no conjugate in the SM-FL needle or loop**, so no conjugate carry-over into the next sample | docs/02 §2.4c (carry-over route); BSM lines unsuitable for protein (docs/02 §1.2) | carry-over already small in the model; the gain is reproducibility of exposure (part of the 10 % NSB CV), not quantifiable | the SIA module the primary design adds anyway | blank-after-1000 pg/mL test (U9) | partly (carry-over only) |
| Amplification that spares NSB | proximity (dual-epitope) labels; enzyme channelling | Rishpon1997 (channelling, separation-free); none at fM in flow | unknown; ≤ the L4 class | new reagents | not recommended for this project stage | no |
| Releasing the label before readout (read only the supernatant) | already the case: the soluble product is read, not the surface | – | none beyond L2/L4 | – | – | – |

**Reading.**
* The only levers that move the probability **robustly** (in every NSB scenario, not just the favourable ones) are
  L4 (immune-complex transfer) and L3 (Fab′ label). Both act on NSB per unit specific signal, the term that
  dominates every blank.
* L6 and L7 are screening steps that remove the two biggest tails.
* L1, L2 and L5 are second-order once the trap is integrated at the valve.

## 3. Robustness

`results/design/robustness.md` and `final_designs.md`, n = 2000. Values are median LOD (pg/mL) / P(success).

| Scenario | One-step in sample vial (reference, inadmissible) | **Primary: one-step, chamber** | Sequential mode, chamber | Sequential beads in vial (reference, inadmissible) | **Backup: packed micro-bed** |
|---|---|---|---|---|---|
| S0 audited | 1.3 / 0.35 | 2.0 / ~0.28 | 1.7 / ~0.28 | 1.5 / 0.31 | 2.8 / 0.16 |
| S1 old NSB rate (×25) | 23 / 0.01 | 32 / 0 | 32 / ~0 | 28 / 0 | 62 / 0 |
| S2a detection reagent screened | 0.94 / 0.50 | **1.1 / ~0.44** | 1.5 / ~0.32 | 1.3 / 0.34 | 2.4 / 0.18 |
| S2b capture reagent unscreened | 1.8 / 0.28 | 3.3 / ~0.21 | 2.7 / ~0.21 | 2.1 / 0.23 | 3.8 / 0.12 |
| S3a NSB 50 % reversible | 0.99 / 0.48 | 1.4 / ~0.39 | 1.1 / ~0.42 | 1.0 / 0.45 | 1.6 / 0.27 |
| S3b NSB irreversible, tubing factor 30 | 1.7 / 0.29 | 2.5 / ~0.23 | 4.0 / ~0.10 | 3.5 / 0.10 | 4.2 / 0.09 |
| S4a free HQ 10⁻³ | 11 / 0.03 | 23 / ~0 | 9.3 / ~0.01 | 8.5 / 0.02 | 9.2 / 0.01 |
| S4b free HQ 10⁻⁷ | 1.1 / 0.42 | 1.4 / ~0.35 | 1.4 / ~0.34 | 1.3 / 0.36 | 2.6 / 0.19 |
| S5 ≤ 100 µL drawn (PLNO 75 µL) — settled by user decision 2, shown for completeness | 1.4 / 0.35 | 2.1 / ~0.26 | 1.9 / ~0.25 | 1.7 / 0.28 | 3.7 / 0.12 |
| L6 + L7 (screening passed) | 0.80 / 0.57 | **0.93 / ~0.55** | 1.2 / ~0.38 | 1.1 / 0.41 | 2.2 / 0.21 |
| L1 + L3 + L6 + L7 | 0.61 / 0.73 | 0.70 / ~0.72 | 0.76 / ~0.66 | 0.67 / 0.68 | 1.2 / 0.37 |
| L4 immune-complex transfer | 0.75 / 0.63 | 0.95 / ~0.53 | 0.76 / ~0.63 | 0.71 / 0.66 | 0.94 / 0.49 |
| admissible under user decision 1? | no (reagent in sample vial) | **yes** | yes | no (beads in sample vial) | **yes** |

"~": chamber approximation (`scripts/inline_chamber.py`). Sequential-mode chamber rows are design `S-chamb` in
`results/design/final_designs.md`.

**How the decision behaves.**
* **One-step vs sequential.** With unscreened detection reagents, the one-step chamber has a long upper tail
  (95th percentile 73 pg/mL). The cause is the 6.6-min emptying of the chamber, during which a t½ ≈ 13 min
  detection antibody dissociates. The sequential mode has a 95th percentile of 15 and the same P. With a screened
  reagent, one-step wins (P 0.44 vs 0.32). That is why the platform supports both modes and U2 picks the mode.
  Neither mode wins only in the favourable scenario: they differ by ≤ 0.17 in P in every scenario run. The bead
  platform beats the fixed bed in median in every scenario except S4a (free HQ 10⁻³: one-step chamber 23 vs fixed
  bed 9.2 pg/mL, both failing) — a further reason why U3 gates the design.
* **Wall NSB scenario (S3b).** The sequential modes lose most (P 0.10), because their conjugate contacts the trap
  walls. One-step loses least. This is a further reason to prefer one-step once U2 passes.
* **S1 (old NSB) and S4a (free HQ 10⁻³) kill every design,** the fixed bed included. These are the two measurements
  that decide whether the project can reach 1 pg/mL at all, not which design to build.
* **S5 (drawn-volume reading)** is settled by user decision 2 (injected volume counts). It would have cost ≤ 0.02 in
  P for beads and 0.04 for the fixed bed, so the decision never depended on it.
* **Admissibility (user decision 1)** removes the two in-vial reference columns. Among admissible designs the ranking
  is: one-step chamber ≈ sequential chamber > fixed micro-bed, in every scenario except S4a.

## 4. Decision

### 4.0 Recovering simultaneous incubation by automated means (user decision 1)

The one-step format led because sample, beads and conjugate incubate together for ~30 min in a small volume at full
conjugate concentration (labelled fraction 0.1–0.3, against 0.01–0.06 for labelling in flow). The routes below keep
that while leaving the sample vial untouched. `scripts/recovery_options.py` → `results/design/recovery_options.md`
(n = 2000; "~" = chamber approximation of `scripts/inline_chamber.py`, LOD × 1/0.96 for the extra transfer).

| Route | Added hardware | Unattended with Empower + Python? | Model: median [5–95 %], P(success), today | Same after U1–U3 (L6 + L7) | Verdict |
|---|---|---|---|---|---|
| **A. Dispenser + stirred in-line cup** (SIA: syringe pump + 8-port selection valve doses beads + conjugate from a stirred, cooled reservoir; the SM-FL/BSM pushes the sample into the cup; the syringe pump empties the cup through the trap) | SIA module, cup (~0.5 mL, vented, low-bind), V4 (6-port) | **Yes.** Empower runs one sample line (injection + BSM programme); Python, triggered by Inject Start, drives the SIA module (serial), V2–V4, magnet and Gamry. Proven concept: sequential-injection immunoassay with magnetic beads (Pollema1992) | 2.0 [0.36–73], ~0.28 | 0.93 [0.23–4.9], ~0.55 | **Primary** |
| B. Second SM-FL injection from a **shared** bead/conjugate reagent vial into the cup, then the sample | cup, V4, a pump to empty the cup (the SM-FL/BSM cannot aspirate) | Yes in principle, but the SM-FL cannot resuspend beads (docs/02 §2.3), so the bead dose drifts as beads settle over a run. Modelled as bead-dose CV at its high bound 0.15 | 2.6 [0.44–86], ~0.20 | 1.1 [0.30–8.0], ~0.43 | Fallback for A only if the SIA reservoir fails; test in U5 |
| C. Held-up zone: sample and reagent plugs parked in an unstirred holding coil | one valve + coil | Yes, but no mixing: capture relies on diffusion and settling. Modelled as capture factor 0.09 (YAML low bound 0.2 / 2.2 dilution) | 8.8 [0.95–350], ~0.06 | 2.8 [0.56–23], ~0.16 | Rejected |
| D. Merge with a bead/conjugate stream from a BSM line | none | **No**: protein and bead suspensions must not pass BSM pump heads, check valves and mixer (docs/02 §1.2: adsorption, hold-up, blockage) | not evaluated | – | Inadmissible |
| E. External dispenser adding reagent to sample vials in the SM-FL tray | liquid handler | No: the SM-FL compartment is closed, and reagent in the sample vial is excluded by decision 1 anyway | – | – | Inadmissible |
| S. Route A hardware, **sequential mode** (beads only into the cup; conjugate injected from a shared SM-FL vial onto the trapped beads) | as A | Yes (conjugate injection is an ordinary Empower line) | 1.7 [0.39–15], ~0.28 | 1.2 [0.31–8.5], ~0.38 | In-platform fallback |

**Conclusion.** Route A recovers most of the one-step advantage: P ~0.28 against 0.35 for the inadmissible in-vial
reference. The loss comes from the longer emptying of the cup (6.6 min), during which an unscreened detection
antibody (t½ ≈ 13 min) dissociates. With a screened detection reagent the gap closes (0.93 vs 0.80 median). The
sequential mode on the same hardware has the same P today with a much shorter upper tail.

### 4.1 Primary design: timed one-step bead assay with an in-line chamber, integrated trap and flow IDA

**Capture and renewal.**
* Streptavidin superparamagnetic beads, 2.8 µm, 5×10⁵ per assay, loaded with biotinylated anti-human-IgG-Fc
  capture antibody, oriented (Chang2012 density about 1×10¹⁶ m⁻², active fraction ≥ 0.5).
* Beads are renewed every run (Pollema1992 principle). No regeneration chemistry.

**Antibody pair and acceptance criteria.** Bench item U2 measures these by BLI/SPR at 25 °C in assay buffer.

| Reagent | Format | k_on | k_off | Other criteria |
|---|---|---|---|---|
| Capture | mouse mAb or affinity-purified goat F(ab′)₂ anti-human Fc, cross-adsorbed (bovine, mouse) | ≥ 3×10⁵ M⁻¹s⁻¹ | ≤ 1.9×10⁻⁴ s⁻¹ (t½ ≥ 1 h) | – |
| Detection | ALP-labelled **F(ab′)₂ or chicken IgY** anti-human Fab/κ+λ (asymmetric epitope; does not bind the capture antibody or mammalian Fc) | ≥ 3×10⁵ M⁻¹s⁻¹ | target ≤ 1.9×10⁻⁴ s⁻¹ (t½ ≥ 1 h) for one-step mode. If none is found: t½ ≥ 10 min and switch to sequential mode | ALP:Ab 0.5–2. Detection-on-capture: blank on capture beads ≤ 1.2× blank on non-immune beads (Qu1998 risk) |

**Label and substrate.**
* ALP and HQDP at 1 mM; 3 mM if needed to keep ULOQ above 1000 (§1.5). pH 9.5 with Mg²⁺, IgG-free blockers.
* Lot acceptance: free hydroquinone ≤ 10⁻⁵ mol/mol; hydrolysis ≤ 10⁻⁹ s⁻¹ at room temperature over the run.
* HQ does not foul the electrode (Wilson2004), so the electrode is reused.

**Detector and potentiostat.**
* Custom flow IDA cell: Au or Pt thin film, 50 finger pairs, 5 µm fingers and 5 µm gaps, 1 mm long, in a
  25 µm × 0.5 mm channel (docs/02 §5.2). PEEK body, external Ag/AgCl reference via side arm, Pt counter electrode
  downstream.
* Channel 1 (Reference 600+): generator at +0.35 V vs Ag/AgCl (HQ → BQ; DellaCiana1996 and Wilson2004b via
  docs/01).
* Channel 2 (a Reference 620; pairing with the 600+ is UNVERIFIED, docs/02 Q10, so buy a matched 620 pair if Gamry
  will not support the mix): collector reducing BQ. Set its potential from a CV at the bench, expected around
  −0.1 to −0.2 V (UNVERIFIED).
* Chronoamperometry during the 1 min sweep. Charge is integrated with baseline windows before and after.
* A thin-layer GC cell is an acceptable single-channel fall-back at 1.1× the LOD.

**Plumbing.** All tubing PEEK; any steel only upstream of the grounded union.

```
BSM (A1 wash buffer = Tris-buffered saline + 0.05 % Tween-20, NO phosphate; A2 water/MeOH; B1 HQDP substrate;
  B2 spare) -> restrictor(s) -> SM-FL (100 uL loop, full loop)
  -> V4 (6-port, 2-pos): A = SM-FL outlet -> incubation cup ; B = SM-FL outlet -> tee -> V2
SIA module: syringe pump (1 mL) + 8-port selection valve: port 1 bead reservoir (beads only, stirred, 4-8 C),
  port 2 cup bottom outlet, port 3 wash buffer (TBS + Tween, no phosphate), port 4 waste, port 5 line -> tee -> V2,
  port 6 conjugate reservoir (conjugate only, 4-8 C, dark, not stirred), ports 7-8 spare (e.g. a second cup)
V2 (10-port, 2-pos, reactor isolation, Scheme B): magnetic trap (1.5 mm ID PEEK, ~1.1 mm magnet zone, 2 uL)
  screwed directly into ports 2/3 (<= 5 mm stubs each side)
V3 (6-port, 2-pos): EC IDA cell in / bypass -> waste. Optical detector (TUV) connected after V3 only for bead-free
  tracer experiments (E2.1, E2.4), never in the bead path
Magnet: actuated permanent magnet on the trap (TTL), or electromagnet
```

(Plumbing revised after final review: A1 composition (B1), separate bead and conjugate reservoirs on their own
selection-valve ports (B4), TUV out of the bead path (W3); docs/08 §10.)

**Valve count:**
* three external 2-position valves (V2 10-port, V3 6-port, V4 6-port);
* one SIA selection valve (8-port);
* plus the SM-FL injection valve.

**Per-cycle step table** on the installed system, one-step mode. Python owns V2/V3/V4, the SIA module, the magnet
and the Gamry. Empower owns the BSM programme and the SM-FL.

| t (min) | Step | V4 / V2 / V3 | Flow, solvent | Notes |
|---|---|---|---|---|
| −1 → 0 | SIA doses 10 µL of bead suspension (5×10⁵ beads) from the bead reservoir, flushes the common channel with 50 µL wash buffer to waste, then doses 10 µL of 6.6 nM conjugate from the separate conjugate reservoir into the clean cup (gives 0.3 nM conjugate and 5×10⁵ beads in the final ~220 µL) (revised after final review: beads and conjugate no longer share a reservoir, B4) | – | SIA | can overlap the previous cycle |
| 0 → 1 | SM-FL aspirates the sample (full loop, 2× overfill: ~200 µL drawn, 100 µL injected) | A / isolate / bypass | BSM 100 µL/min A1 (TBS + Tween, no phosphate; revised after final review, B1) | Empower line L1 starts |
| 1 → 3 | Inject Start t₀: 2 loop volumes (200 µL) of sample pushed into the cup | A / isolate / bypass | 100 µL/min A1 | sample transfer ~0.96 |
| 3 → 33 | **Incubation 30 min**, mixed by SIA aspirate/dispense (50 µL every 2 min) | B / isolate / bypass | BSM 100 µL/min A1 to waste via the shunt (a previous sample's readout can run here only with a second cup; with one cup there is no overlap — revised after final review, W10) | timed exactly; same for every sample in the queue |
| 33 → 39.6 | Magnet on; SIA pushes the cup contents plus 2 rinses through the trap | B / perfuse / bypass | SIA 99 µL/min (653 µL) + BSM programmed to its minimum, 1 µL/min A1, which joins at the tee: trap flow 100 µL/min (revised after final review, S2: two pumps into one tee add their flows; log BSM pressure and trap flow in E2.1) | bead capture in trap |
| 39.6 → 40.6 | Wash | B / perfuse / bypass | BSM 100 µL/min A1 (TBS + Tween, no phosphate; revised after final review, B1) | ≥ 50 trap volumes |
| 40.6 → 41.6 | Substrate fill (A1 → B1 step) | B / perfuse / bypass | 200 µL/min B1 | |
| 41.6 → 51.6 | **Accumulation 10 min**, trap sealed | B / isolate / detect | 10 µL/min B1 via shunt and cell, the readout flow, so the baseline windows sit at the readout flow (revised after final review, W5) | substrate blank current recorded |
| 51.6 → 52.6 | **Readout**: sweep the trap contents through the IDA | B / perfuse / detect | 10 µL/min B1 | integrate charge on both channels |
| 52.6 → 56.1 | Magnet off, beads to waste at 300 µL/min (V3 bypass → waste, not through the TUV); SM-FL needle wash (no injection) while the BSM flushes the loop, which stays in line after the injection, and the trap; SIA rinses the cup 3× (revised after final review, S3: the earlier "cleaning injection" was a second injection that neither the automation nor the Empower plan declared) | B / perfuse / bypass | 300 µL/min A1 | |

Time to result: **56.1 min**. With a second cup (one more selection port), consecutive samples overlap and
throughput is about 30 min per sample.

**Sequential mode.** Beads only into the cup. After the trap wash, an SM-FL injection of 3 nM ALP conjugate (20 µL)
is stopped on the trapped beads for 3 min, followed by a 2 min wash. Accumulation 5 min. Time to result 58.1 min.

**End-to-end automation.**
* The customer loads plain sample vials and a reagent pack (bead reservoir, separate conjugate reservoir, HQDP
  bottle) (revised after final review, B4).
* An Empower sample set holds one line per sample; its BSM programme carries the A1/B1 steps.
* The SM-FL Inject Start signal triggers the Python cycle table (docs/02 §3.2 primary scheme), which drives the SIA
  module (serial), the valves (serial/TTL), the magnet (TTL) and the Gamry worker (ToolkitPy).
* A watchdog parks V2 = isolate and V3 = bypass on any fault. Every run after a fault is flagged invalid until an
  automatic recovery cycle (magnet off, 300 µL/min flush of the trap, cup rinse) has completed and been logged
  (revised after final review, S12).
* No manual step occurs between loading and result.
* Blanks and a mid-range control are interleaved every 10 samples. That also tracks NSB drift.

**Predicted LOD** (model, chamber approximation):
* 0.56 pg/mL nominal; median 2.0 [0.36–73]; P(LOD ≤ 1) ~0.29; P(success) ~0.28.
* With reagent screening and substrate QC passed (L6 + L7): median 0.93 [0.23–4.9], P ~0.55.
* With the F(ab′)₂ label and coated trap as well: median 0.70, P ~0.72.

### 4.2 Backup design: fixed packed micro-bed (no beads, no reagent mixing with the sample)

**Capture.**
* 0.5 µL bed of 50 µm non-porous particles carrying covalently oriented anti-human-Fc capture antibody (particle
  supplier UNVERIFIED), in a 0.5 mm ID × 2.5 mm PEEK column screwed into V2 ports 2/3.
* Kozeny–Carman pressure drop 0.001 MPa.
* Same detection reagent, substrate, IDA cell and potentiostat use as the primary.
* Valves: V2 10-port and V3 6-port. No V4 and no SIA module.

**Step table** (cycle = time to result = 51.5 min):

| Step | Duration (min) | Conditions |
|---|---|---|
| Sample injection | 1 | full loop |
| Load | 20 | 10 µL/min A1, 2 loop volumes. The I-Class BSM is specified only from 0.2 mL/min (docs/02), so the low-flow precision must be checked. Needs a narrower restrictor for ≥ 1000 psi |
| Wash | 1 | |
| Conjugate | 6 | 20 µL of 1 nM via SM-FL; 2 min stop, 2 min wash |
| Substrate fill | 1 | |
| Accumulation | 15 | |
| Readout | 1 | 10 µL/min |
| Regeneration | 6.5 | 100 µL glycine-HCl pH 2 injection, then re-equilibration |

**Regeneration and reuse.**
* At 0.5 %/cycle capacity loss (`chem.regeneration.activity_loss_per_cycle`) the slope drifts 10 % in about 21
  cycles, so a calibration check is needed every ~20 cycles.
* The column is replaced after the qualified cycle number (Kamat2021 reports 300 cycles for anti-Fc surfaces).

**Predicted LOD:**
* 0.74 nominal; median 2.8 [0.52–31]; P(success) 0.16.
* With L6 + L7: median 2.2, P 0.21.
* With immune-complex transfer (L4): median 0.94, P 0.49.

**When to use it:** if bead dosing or trapping fails its acceptance (U5), or if the SIA module cannot be made
reliable.

### 4.3 Why in-vial pre-mixing would fail anyway (timing), and what it is still useful for

User decision 1 rules out reagent in the sample vial. Independently, the timing analysis shows the in-vial format
could not have worked unattended. `scripts/incubation_queue.py` → `results/design/incubation_queue.md`, optimised
one-step design, nominal:

| In-vial time (min) | 20 | 30 | 35 (design) | 60 | 120 | 240 |
|---|---|---|---|---|---|---|
| Calibration slope relative to design | 0.52 | 0.85 | 1.00 | 1.55 | 2.08 | 2.28 |
| Blank mean relative to design | 0.61 | 0.87 | 1.00 | 1.65 | 3.20 | 6.30 |
| LOD (blanks at the same time, pg/mL) | 0.39 | 0.33 | 0.32 | 0.34 | 0.50 | 0.89 |

A ±2 min timing error changes the slope by −5.8 %/+5.6 %. With 20 queued vials, the k-th sample would incubate
about (k−1) × 25 min longer than the first, biasing its result by up to 2×. Capture and labelling are not near
equilibrium within any time compatible with 60 min. The chamber of section 4.0 fixes this because its incubation
starts at injection and is identical for every sample.

The in-vial format remains useful **only as a bench tool** (the developer, not a customer, mixes and times one vial):
it needs no dispenser, so it is the quickest way to measure U1, U5 and an integrated LOD early in Stage 1. Its model
numbers (median 1.3, P 0.35) are a reference for what the chamber should approach, not a deliverable.

### 4.4 Predicted LOD and probability, in one place

| | Model median [5–95 %] (pg/mL) | Model P(success) | Real-world judgement |
|---|---|---|---|
| Primary as specified today (unscreened detection reagent, unknown HQDP lot) | 2.0 [0.36–73] | ~0.28 | **~15 %** |
| Primary after U1–U3 pass (L6 + L7, NSB ≤ anchor) | 0.93 [0.23–4.9] | ~0.55 | **~40–50 %** |
| Primary plus F(ab′)₂ label and coated trap | 0.70 [0.16–2.4] | ~0.72 | ~50–60 % |
| In-platform fallback (sequential mode, same hardware) | 1.7 [0.39–15]; 1.2 after U1–U3 | ~0.28; ~0.38 | ~15 %; ~35 % |
| Backup as specified | 2.8 [0.52–31] | 0.16 | ~8 % |
| Backup plus immune-complex transfer | 0.94 [0.23–6.5] | 0.49 | ~25 % |

### 4.5 Why my judgement is below the model

The model does not capture:
1. **Human-IgG contamination** at 100 fg per sample (Parry1997). It is nominally 0 in the model and sampled only up
   to 3 fM.
2. **Detection-on-capture cross-reaction** of anti-IgG reagents, which are themselves IgG (Qu1998: up to 15× when not
   suppressed). The residual factor is 1–3 in the model.
3. **Bead-handling losses and variability** (dose CV, trap efficiency, settling), which are UNVERIFIED in the model.
4. Real **run-to-run NSB CV** in an integrated flow system can exceed the 10 % taken from plate and Simoa data.
5. **Temperature** is not controlled (no thermostat; docs/02 R12).
6. **HQDP availability** (commercial supply UNVERIFIED, docs/01).
7. The **chamber is a new hardware element** with no precedent at fM levels.

Each of these is more likely to hurt than to help.

## 5. Kill criteria and the ordered list of unknowns

Ordered by value of information per unit bench effort. Each item becomes a Stage 1–2 experiment in the bench plan
(Task 5).

**U1. Conjugate NSB on blocked streptavidin beads: rate, linearity in time, reversibility.**
* Value: decides whether 1 pg/mL is reachable at all (scenario S1).
* Effort: 1–2 weeks, tubes, no flow system.
* Measurement:
  * 5×10⁵ blocked beads (non-immune biotin-IgG loaded) in 200 µL; the candidate ALP conjugate (IgG and F(ab′)₂
    versions) at 0.1, 0.3, 1 and 3 nM × 10, 30 and 60 min;
  * then 3 magnetic washes; then a wash-stringency arm (0, 3, 10 washes; ± 0.1 % Tween; ± 5 min hold);
  * read bound ALP by HQDP or pNPP turnover against an ALP standard curve (enzymes per bead).
  * Convert to the label factor: k_eff = N_ALP / (A_beads · ∫C dt · N_A), factor = k_eff / 4×10⁻¹¹ m/s.
* **Confirm primary:** factor ≤ 0.04 (nominal), linear or sub-linear in exposure.
* **Kill the 1 pg/mL target** (all formats; go to the L4 transfer development): factor > 0.15, which is about
  blank-equivalent > 4 pg/mL on beads (model at 0.15: primary median 5.9, P 0.06; backup 9.8, P 0.02).
* (revised after final review, B3) The two thresholds above are superseded by one rule on the model P(success) with
  the bench value entered as `model_feedback` enters it (coupled NSB factors pinned): GO ≥ 0.30, GO-WITH-LEVER
  0.10–0.30, STOP < 0.10 (docs/06 §4.11, `results/design/g1_decision_table.md`). Evaluated that way, factor 0.04
  gives the primary P 0.23 (median 2.0) and 0.15 gives P 0.05 (median 5.1); the implied screen is GO ≤ 0.02,
  STOP ≥ 0.10.
* Also: ≥ 30 % removed by stringent washes → add the wash step (S3a). The F(ab′)₂/IgG ratio sets L3.

**U2. Capture and detection antibody k_on and k_off (BLI/SPR).**
* Value: picks one-step vs sequential mode; removes the largest single sensitivity (k_off,detection, −0.4/+2
  decades).
* Effort: 1 week, a few candidates.
* **Confirm one-step mode:** both t½ ≥ 1 h and k_on ≥ 3×10⁵ M⁻¹s⁻¹.
* **Sequential mode:** detection t½ 10–60 min.
* **Reject the pair:** capture t½ < 1 h, or detection t½ < 10 min.

**U3. Free hydroquinone and hydrolysis in the HQDP lot.**
* Value: decides reachability (scenario S4a: free HQ 10⁻³ kills every design).
* Effort: days.
* Measurement: HPLC-EC or flow-cell amperometry of 1 mM HQDP against an HQ standard (0.1–100 nM); 8 h at 22 °C in the
  B1 line.
* **Confirm:** ≤ 10⁻⁵ mol/mol and ≤ 10⁻⁹ s⁻¹.
* **Purify or change lot:** 10⁻⁵ to 10⁻⁴.
* **Kill the substrate:** > 10⁻⁴ after purification (model at 10⁻⁴: primary median 3.8, P 0.12; at 10⁻⁵: 1.7, P 0.30). Then test AAP or p-hydroxyphenyl phosphate in the same way.
* (revised after final review, B3) Decided by the same P rule as U1; with the revised designs the primary gives P 0.06
  at 10⁻⁴ and 0.16 at 10⁻⁵ (`results/design/kill_thresholds.md`, n = 1000).

**U4. NSB on the trap and stub materials (PEEK vs coated) and the clean-zone effect.**
* Value: sets L1/L2; matters most for sequential mode.
* Effort: 1 week on the flow system.
* Measurement: 1 cm trap segments and stubs exposed to 1 nM conjugate in flow (the one-step wall exposure: 100 µL
  at 100 µL/min), washed, sealed with substrate for 10 min, swept to the cell.
* **Confirm:** wall product ≤ 10 % of bead NSB product.
* **Coat or re-trap:** wall product > 30 %.

**U5. Bead dose and trap efficiency.**
* Measurement:
  * SIA dosing from a stirred reservoir: dose CV over 20 doses by bead counting or by a fixed-ALP-bead signal;
  * trap retention at 50 and 100 µL/min vs trap length (1–3 mm) and inside diameter (0.75–1.5 mm), using the TUV
    or the downstream counted fraction;
  * cup carry-over of beads after 3 rinses.
* **Confirm:** dose CV ≤ 5 %, retention ≥ 90 % at 100 µL/min, residual beads ≤ 10⁻³.
* **Go to backup (fixed bed):** dose CV > 10 % or retention < 70 % after two trap iterations.

**U6. ALP inhibition by phosphate in the assay buffer (sets the ULOQ).**
* Effort: days, cuvette.
* **Confirm:** K_i ≥ 2 µM at 1 mM HQDP.
* **Adjust:** 3–5 mM HQDP or shorter accumulation if the ULOQ < 1000 pg/mL.

**U7. Integrated blank statistics on the primary platform** (Stage 2).
* Measurement: 20 blanks and 5 × 1 pg/mL in random order, plus blank after 1000 pg/mL.
* **Confirm:** CV_blank ≤ 10 %, LOD (mean + 3 SD) ≤ 1 pg/mL, carry-over ≤ 10⁻³.
* If CV_blank > 15 %: test L5 (reference beads, measure ρ).

**U8. Immune-complex transfer** (only if U1 lands between 0.04 and 0.15, or U7 misses by 1–3×).
* Measurement: desthiobiotin-capture antibody; elution with 2 mM biotin; recapture on fresh beads carrying a second
  anti-human-IgG antibody. Blank and 10 pg/mL, with and without transfer.
* **Adopt:** blank reduced ≥ 5× with ≥ 50 % specific recovery.

**U9. Human-IgG contamination of blanks.**
* Measurement: blank vials prepared by different operators and with dedicated consumables, compared to sealed
  instrument blanks.
* **Confirm:** contribution ≤ 0.1 pg/mL equivalent.

## 6. How to reproduce every number

```bash
pip install -e . && python -m pytest -q                    # 63 passed (run 2026-11-11 after this task's YAML additions)
python scripts/optimise_designs.py --scenario baseline      # ~35 min; optimum_*__baseline.json, optimisation_baseline.md, trajectories
python scripts/optimise_designs.py --scenario dab_screened --formats OS SQ FRB FRC   # optimisation_dab_screened.md
python scripts/edge_checks.py                               # edge_checks.md (section 1.4)
python scripts/gain_decomposition.py                        # gain_decomposition.md (section 1.3)
python scripts/robustness.py                                # robustness.md / levers.md (sections 2, 3)
python scripts/inline_chamber.py                            # inline_chamber.md (chamber approximation)
python scripts/final_designs.py                             # final_designs.md (sections 0, 3, 4)
python scripts/incubation_queue.py                          # incubation_queue.md (section 4.3)
python scripts/recovery_options.py                          # recovery_options.md (section 4.0)
python scripts/kill_thresholds.py                           # kill_thresholds.md (section 5 thresholds)
```

All outputs are in `results/design/`. Seed 20261111. The calibration grid is refined to 61 points: a numerical
setting that leaves the LOD unchanged and gives finer ULOQ resolution. That is why the baseline P(success) reads 0.21
here, against the 0.18 implied by the 31-point grid.

## 7. Issues found and what could not be verified

* **Bug in `src/elisa_sim/montecarlo.used_keys`** (and therefore `sensitivity.one_at_a_time`) for architectures
  with a design (section 1.1). It is worked around in `scripts/design_lib.py`. src needs the one-line fix and a test.
* **My own optimiser bug,** found and fixed before the reported runs: `np.isclose` with the default atol treated all
  sub-nM concentrations as equal, so the conjugate concentration was never searched. All reported runs use
  rtol-only comparison.
* **The chamber variant is an approximation** with existing parameters:
  * stirred capture factor 0.45 = 1.0 / 2.2 dilution;
  * emptying represented as 6.6 flush volumes;
  * 2 min transfer added through the wash time;
  * a 0.96 transfer factor applied to the LOD.
  Its P values are therefore marked "~".
* **Lever magnitudes L3, L4, L5 and S3a are UNVERIFIED bounded estimates.** The cited papers support the
  mechanisms qualitatively; none gives the number used.
* **Not verified in this session:**
  * the IDA collector potential;
  * whether the Reference 600+/620 pairing is supported;
  * HQDP commercial supply;
  * a 50 µm non-porous antibody-particle supplier;
  * BSM precision at 10 µL/min;
  * every UNVERIFIED parameter listed in docs/04 §10.

## References added by this task

Consensus-indexed papers have no DOI in the plan used; they are listed by title.

* Ishikawa E, Hashida S, Kohno T, Hirota K. Ultrasensitive enzyme immunoassay. Clin Chim Acta 1990;194:51–72.
  doi:10.1016/0009-8981(90)90303-a (PubMed abstract)
* Hashida S, Hashinaka K, Ishikawa S, Ishikawa E. More reliable diagnosis of infection with HIV-1 … immune complex
  transfer enzyme immunoassay: a review. J Clin Lab Anal 1997;11:267–86.
  doi:10.1002/(SICI)1098-2825(1997)11:5<267::AID-JCLA5>3.0.CO;2-4 (PubMed abstract)
* Hashida S, Imagawa M, Ishikawa E, Freytag JW. A simple method for the conjugation of affinity-purified Fab′ to
  HRP and β-D-galactosidase. J Immunoassay 1985;6:111–23. doi:10.1080/01971528508063024 (PubMed abstract)
* Ruan K, Hashida S, Yoshitake S, et al. A more sensitive and less time-consuming sandwich enzyme immunoassay for
  insulin … Ann Clin Biochem 1986;23:54–8. doi:10.1177/000456328602300106 (PubMed abstract)
* Hirsch JD, Eslamizar L, Filanoski BJ, et al. Easily reversible desthiobiotin binding to streptavidin, avidin, and
  other biotin-binding proteins. Anal Biochem 2002;308:343–57. doi:10.1016/s0003-2697(02)00201-4 (PubMed abstract)
* Larsen EKU, et al. Protein and cell patterning in closed polymer channels by photoimmobilizing proteins on
  photografted PEG diacrylate. Biomicrofluidics 2014 (Consensus abstract)
* Popat K, et al. Poly(ethylene glycol) interfaces: an approach for enhanced performance of microfluidic systems.
  Biosens Bioelectron 2004 (Consensus abstract)
* Xian Z, et al. Inhibition of non-specific protein adsorption on PMMA surface. J Saudi Chem Soc 2023 (Consensus
  abstract)
* Wahlgren M, et al. The adsorption of lysozyme to hydrophilic silicon oxide surfaces. J Colloid Interface Sci 1995
  (Consensus abstract)
* Marsh RJ, et al. Adsorption and displacement of a globular protein on hydrophilic and hydrophobic surfaces.
  Colloids Surf B 2002 (Consensus abstract)
* Zhang Z, et al. Adsorption of non-ionic surfactant and monoclonal antibody on siliconized surface studied by
  neutron reflectometry. J Colloid Interface Sci 2020 (Consensus abstract)
* Frutiger A, et al. Nonspecific binding — fundamental concepts and consequences for biosensing applications. Chem
  Rev 2021 (Consensus abstract)
* Rishpon J, et al. An amperometric enzyme-channeling immunosensor. Biosens Bioelectron 1997 (Consensus abstract)
