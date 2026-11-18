# Second review of docs/30 Revision B: numbers and physics

Reviewer: independent second pass, 2026-11-17. Lens: numbers and physics of Revision B (docs/30 Rev B, the kit in
`scripts/tier_round/`, `results/tier_round/tiers.md` and `tiers.json`). Script: `scripts/tier_round/review2_numbers.py`
(`--no-mc` skips the Monte Carlo key listing; about 2 min; it writes nothing). `run_tiers.py` was not run.
Evidence labels: [V] checked in this session (file, line or command named); Derived (own calculation, formula given);
UNVERIFIED.

## Verdict

The kit reproduces: `check_tierkit.py` passes 36 of 36 [V], and the nominal LODs match `tiers.json` (9.356, 2.551,
0.6205 pg/mL) [V]. My own recomputation from the raw YAML values, with my own slit solver, bed equation, labelling,
enzyme ODE and variance terms, agrees with the kit to +0.2 % (tier 1), −1.4 % (tier 2) and −0.3 % (tier 3) [V,
script Part B]. Every number in docs/30 §0, 3.4, 3.5, 4.4, 4.5, 5.3 and 6.1–6.3 matches tiers.md/tiers.json. The only
problems are a column mix-up in two rows of §4.5 and two small inconsistencies about the earlier design (R10).
The physics has four gaps. (1) Tier 1 has no term for the background difference between the buffer windows (A1, pH 7.5)
and the substrate window (B1, pH 9.5), and that difference can dominate. (2) The 600 s hydroquinone half-life is
applied in the bed but not to the substrate reservoir. If it holds there, the free hydroquinone that "limits tier 1" is
gone and tier 1 falls to 5.6–5.8 pg/mL. (3) At the model's own site density, bed 2 of tier 3 is 82 % full with released capture
antibody, so re-capture is 0.83, not 0.95. (4) Tier 3 leaves out the steady enzyme currents of the electrode and the
5 mm inlet bore. My corrected nominal estimates: tier 1 9–11 pg/mL as the chemistry is modelled (5.6 if the half-life
holds in the reservoir; unbounded until the A1/B1 step is measured); tier 2 2.6, unchanged within ±5 %; tier 3
about 0.75 (0.71–0.79), or 1.6 if bed 1 is coated at the vendor's capacity and bed 2 at the model's density.

## Findings

### R1 — significant — Tier 1: the background step between buffer A1 and substrate buffer B1 is not counted

Place: `scripts/tier_round/tierkit.py` `_finish` lines 496–506 (`bg = Q["imp"] + Q["other_bg"]`) and
`evaluate_planar` `steady_flow` branch lines 681–690; docs/30 §3.1 "Read", §3.3 rows 49.5–56.9, §3.6 T1-1.

Evidence: The read is current in substrate (B1: 0.1 M Tris pH 9.5, 1 mM MgCl₂) minus the mean of two windows in wash
buffer (A1: Tris-HCl pH 7.5, Tween 20) (docs/30 §2.2, §3.1) [V]. A gold electrode under an OEG thiol at a held
potential has a background current that depends on pH and on buffer composition. It is not in the kit. The pre-run
removes the part of it that repeats, but the kit applies the pre-run residual (`tr.noise.preread_residual_cv`, 3 %)
only to impurity + hydrolysis + `other_bg` (= 0 in `steady_flow`) [V, tierkit.py 502–506]. The 95 % composition
front (215 µL) also leaves the last 5 % of the B1 step, and its rising free-hydroquinone current, inside the read
window. Derived: with the same 3 % residual, a step Δi adds (0.03 · Δi · 120 s)² to the blank variance. The break-even
step, where this term equals the present blank SD of 0.61 nC, is 168 pA. LOD with a step of 30 / 100 / 300 / 1000 pA:
9.5 / 10.9 / 19 / 57 pg/mL (script Part C (b)). The size of the step on coated printed gold is UNVERIFIED.

Fix: Take the reference windows in substrate buffer without HQDP: BSM line B2 = B1 minus HQDP, so that A1 is used
only for washes. Then the windows differ from the read only by the substrate. Until T1-1 measures the A1/B1
background difference on coated gold and its run-to-run repeatability, add it to the kit as a parameter
(`other_bg` in `steady_flow`).

### R2 — significant — The 600 s hydroquinone half-life is applied in the bed but not in the substrate reservoir

Place: `scripts/tier_round/run_tiers.py` `base_params` (override 600 s [120–7200]); `tierkit.py` lines 688–689
(`q_init`, `q_vol = q_init * age`), 863, 877, 895; docs/30 §0 "What limits it" (tier 1), §3.1, §3.4.

Evidence: The override (finding C5: hydroquinone autoxidises within minutes at pH 9.5; docs/30 §2.2) enters only
`kin.enzyme_accumulation` in tiers 2–3 [V, tierkit.py 842–844]. In tier 1 it is sampled but has no effect [V, script
Part A, MC listing]. The substrate's free hydroquinone (10⁻⁵ × S0) and the hydrolysis product, which builds up as
k_hyd · S0 · age with age = 4 h, are taken as stable in the B1 bottle. B1 is the same air-saturated pH 9.5 solution.
Derived: at t½ = 600 s, the impurity left after 4 h is exp(−ln2 · 14 400/600) = 6×10⁻⁸ of its initial value, and the
hydrolysis product sits at its steady state k_hyd · S0 / k_dec (866 s instead of 14 400 s). Tier 1's substrate
background then falls from 122 pA to 0.9 pA, and its LOD from 9.4 to 5.8 pg/mL (5.6 with R6) (script Part C (e)).
Tiers 2 and 3 change little: 2.48 and 0.547. If the reverse holds and hydroquinone is stable at 7200 s, they are 2.49
and 0.578. A side effect in tier 3 (Derived): the substrate standing 7 min in the closed loop of bed 2 loses
1 − exp(−k_dec · 420) = 38 % of its free hydroquinone. When V2 opens, this gives a dip of 0.23–0.92 nC in the 100 pA
baseline for a 0.5–2 µL loop, against a signal of 0.93 nC per pg/mL. This contradicts the "flat baseline" of §5.1.
The dip is systematic, but its spread is not modelled.

Fix: Use one hydroquinone stability for the whole liquid path. Either (a) apply the decay to the reservoir (impurity
decays, hydrolysis product at steady state), which makes tier 1's limiting term drift and nonspecific label, not the
substrate's hydroquinone; or (b) state why the bottle differs from the bed (deoxygenated, no catalyst) and then
question 600 s in the bed. Measure the free hydroquinone of B1 over 0–8 h in the T1-1/T2-2 runs, and add the
closed-loop dip to the tier-3 baseline model.

### R3 — significant — Tier 3: bed 2 is near saturation at the stated numbers; re-capture is 0.83, not 0.95

Place: `tierkit.py` `evaluate_bed` lines 813–827 (first-order `recapture`); docs/30 §5.1 "Transfer" row and the
"Capacity" bullet; §5.3 first row.

Evidence: At the model's site density, bed 1 (24.4 mm²) holds 1×10¹⁶ m⁻² × 24.4 mm² = 2.44×10¹¹ capture F(ab′)₂.
2.08×10¹¹ of them are active. Release 0.7 puts 1.7×10¹¹ into the eluate. All of them carry the hapten, so bed 2,
at the same density, offers 2.08×10¹¹ sites (Derived). I ran a plug-flow bed of 200 slices with site depletion. The
local flux per area is C/(1/k_m + 1/(k_on Γ_free)), with k_m from Wilson–Geankoplis at 2 µL/min and D of the
conjugate, and the eluate is 8 µL. It gives a recovery of 0.830 against the kit's first-order 0.951. If bed 1 is
coated as docs/30 §4.2 describes, at the vendor's 10 µg/mg (8.2×10¹¹ F(ab′)₂ per 10⁶ beads, Derived from docs/28 R32
as quoted in docs/30 §2.1), and bed 2 is at the model's density, the recovery is 0.362. Tier 3 then loses to one
valve alone (Derived: LOD ≈ 0.62 × 0.951/0.362 ≈ 1.6 pg/mL against 1.5). With 3× the sites on bed 2 the recovery is
0.999. LOD with the 0.83 recovery: 0.71 pg/mL (script Part C (d), Part D). docs/30 states the condition but the
nominal 0.62 and every tier-3 row in §5.3 assume it is met.

Fix: Make the capacity part of the design. Either make the streptavidin bed the read bed (docs/30 §5.1 option, 6–8×10¹²
sites, ratio > 10) or fix the bed-1 coating density below the bed-2 capacity, and state the ratio in §5.1. Put the
site-depletion re-capture into `evaluate_bed` (a few lines, as in `capacity_recovery` of the script). If the design
stays as written, rerun §5.3 with recovery 0.83.

### R4 — minor — Tier 3: steady enzyme currents in the read are not counted at all

Place: `tierkit.py` `evaluate_bed` swept branch line 865 (`cell_blank = 0.0`); `designs.py` `tier3`
(`bore_below_tip_mm=0.0`); docs/30 §5.1 "What one valve changes" bullets 1–2.

Evidence: In tier 3 the conjugate passes V1, the V2 bypass and the whole cell. The electrode (printed carbon, factor 10,
7.07 mm²) and the full 5 mm inlet bore (12.6 mm², no capillary in it) therefore carry conjugate. With 1156 enzymes per
mm² at factor 1 (Derived from the kit's bed numbers) these are 8.2×10⁴ and 4.4×10⁴ enzymes. In flowing 1 mM substrate
they give about 32 pA (electrode in full, bore at η = 0.62), next to the 100 pA free-hydroquinone baseline. The kit
counts neither, and the bore wall is not counted anywhere in tier 3. docs/30 §5.1 says the baseline removes them.
Counted like the free-hydroquinone current (1 % of the background charge), they raise the LOD from 0.62 to 0.67
(0.68 with another 5×10⁴ enzymes on the V2 bypass and the line) (script Part C (d)).

Fix: Add the steady current to `bg` (as `other_bg`) in the swept and continuous branches whenever the cell saw
conjugate. Also count it in tier 2, see R7.

### R5 — minor — Dispersion between bed and electrode: "eluted = 1.0" is right for tier 2, about 7 % high for tier 3; the tank formula is unphysical

Place: `tierkit.py` lines 853–861 (`n_eff`, `tanks_in_series_eluted`); `designs.py` `tier2` `sigma_uL=1.0`, `tier3`
`sigma_uL=1.5`.

Evidence: n_eff = V_acc² / (V_acc²/3 + σ²) = 0.0115 tanks for V_acc = 0.108 µL and σ = 1 µL [V, script Part B]. That is a
gamma distribution with its mode at zero and a long tail, not a dispersed plug. It gives 0.996–1.0 only because the
7.5 µL window is long. Physically, transport from the bed to the electrode is laminar convection. In the 0.8 mm bore
the radial diffusion time is r²/D = 186 s, against 6 s of residence at 5 µL/min. For an initially thin slab the
fraction not yet through after a volume V is (V_t / 2V)² (Derived). In tier 2 the transit is about 0.6 µL, so 0.2 %
is lost and eluted ≈ 1.0 is right. In tier 3 the transit is about 4 µL (the 5 mm bore, 2.5 µL, plus the V2 passages
and the line), so about 7 % falls outside the window. With R3 and R4 this moves tier 3 to 0.79. Product made by the bed
during the 90 s sweep (fresh substrate) arrives within the window and adds about 28 % to signal and bed blank alike
(Derived: rate × 88 s against the 420 s accumulation with 0.79 product survival). The kit omits it. It moves the
tier-3 LOD down by about 10 % (Part D: 0.79 → 0.71) and tier 2 by under 1 %.

Fix: Replace the tank-in-series elution by transit volume plus laminar tail (or a Taylor–Aris form where it applies),
with V_t from the geometry of each tier. Count the sweep-time production.

### R6 — minor — Tier 1: product of the inlet-bore wall is collected at about 0, not at the stream's 7.4 %

Place: `tierkit.py` line 686–687 (`bore=eta * T, line=eta * T`); docs/30 §3.1 "(i)", §3.4 row "Conjugate on bore
and transfer line".

Evidence: In the wall jet, the streamlines next to the bore wall turn at the corner and run along the lid, across the
0.2 mm gap from the electrode. During the 0.53 s passage over the electrode at 150 µL/min, product diffuses
√(2Dt) = 31 µm (Derived). During the 1.0 s in the bore it diffuses 43 µm of the 400 µm radius, so it stays near the
wall. Bore product (4.4×10⁴ enzymes) is therefore collected at well below η. Line product (50 µm bore, 0.12 s, 14 µm)
is partly mixed, and η is an upper estimate for it too. Removing the bore term: 9.36 → 9.30 pg/mL (script Part C (a)).
The term is conservative and has no effect on the conclusions.

Fix: In §3.4, call the 1.4 pg/mL equivalent an upper estimate. No change to the kit is needed.

### R7 — minor — Tier 2: the uncounted terms net to under ±5 %

Place: `tierkit.py` swept branch lines 857–865; `designs.py` `tier2` (`V_dead_uL=0.1`); docs/30 §4.1 "Why at the tip".

Evidence (script Part C (c), Derived):
* The electrode's own conjugate (8.2×10⁴ enzymes at factor 10) and the lid above it (7×10³ effective) give 26 pA, or
  2.3 nC in the read, against the kit's Q_nsb of 15.4 nC. The pre-run on the fresh strip does not hold it, so it stays
  in the "trace minus pre-run trace". Counted with the planar unit-to-unit CV: LOD 2.52 → 2.56 (+1.6 %). The floor
  ring is downstream in the sweep and contributes only to the stopped baseline.
* The walls above the bed: the kit computes their product in the bed's 0.108 µL with the phosphate of the whole bed
  blank (K_i 2 µM). In their own 0.92 µL it is 7 % higher (6.27 against 5.86×10⁻¹⁴ mol).
* Product made during the sweep: +28 % to signal and blank alike; LOD −0.5 %.
* During the stop, product diffuses down through the 1 mm of bore to the electrode, which is on. A 1D upper estimate
  is 5 % of the product (erfc average over 420 s, half of it going down), in signal and blank alike. LOD effect under 1 %.
* docs/30 §4.1 gives 0.5 µL of bore between tip and electrode, but `V_dead_uL` is 0.1. This changes only the
  dilution of phosphate (a 0.4 µL case was run in round 1).

Fix: Count the electrode term, or take the last 30 s of the stop as a second baseline. List the others in the README
under Limits. The tier-2 nominal 2.6 stands.

### R8 — minor — Tier 1: reservoir age is fixed although the parameter file bounds it, and hydrolysis grows between the pre-run and the read

Place: `params/model_assumptions.yaml` line 977 (`substrate_reservoir_age` 4 h [1–12]); `tierkit.py` line 689.

Evidence: The age is read but not sampled in tier 1 [V, script Part A]. LOD at 1 / 4 / 12 h: 8.7 / 9.4 / 11.9 pg/mL
[V, script]. The hydrolysis current grows by 3.5 pA in the 55 min between the pre-run and the read (Derived: 15.3 pA ×
55/240). That is 2.2 pg/mL equivalent. It is systematic, so it lands in the blank mean, but the pre-run does not
remove it. This finding depends on R2: with a 600 s half-life in the reservoir the growth stops after about an hour.

Fix: Sample the age, or say in docs/30 §3 that B1 is replaced at a fixed age. Settle R2 first.

### R9 — minor — Monte Carlo wiring: the listed keys are wired; geometric uncertainties named in the text are not sampled

Place: `tierkit.py` `monte_carlo` lines 933–964; docs/30 §0 "Median [5–95 %]".

Evidence [V, `tk.monte_carlo(..., n=200)` and the accessed keys, script Part A]:

| Key | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| tr.transfer.elution_efficiency | not read | not read | sampled |
| ma.design_levers.immune_complex_transfer_nsb_factor | not read | not read | sampled |
| tr.noise.preread_residual_cv | sampled | sampled | sampled |
| tr.noise.swept_step_residual_cv | not read (correct) | sampled | not read (correct) |
| tr.noise.drift_area_exponent | sampled (no effect at 7.07 mm² = A_ref) | sampled | sampled |
| tr.nsb.surface_factor_gold_oeg | sampled | not read | not read |
| tr.nsb.surface_factor_frit | not read | sampled | sampled |
| ma.nsb.surface_factor_tubing | sampled | sampled | sampled |
| ma.nsb.surface_factor_packed_bed | not read | sampled | sampled |
| ma.chemistries.alp_hqdp.product_half_life | sampled, no effect (R2) | sampled | sampled |

Number of sampled keys: 42, 46, 46. Every key the text calls uncertain that enters a tier is sampled. Not sampled,
although docs/30 calls them uncertain: the frit's wetted area (5 mm² "taken", 1–20 mm² in §4.1; LOD 2.1–4.3), the
10 mm² of loop wall, the gap (0.1–0.5 mm), the bore length (5 mm, "assumed"), `V_dead` and σ, the reservoir age (R8),
and the bed-2 capacity (R3). The 5–95 % ranges are therefore narrower than the text's own uncertainty. docs/30 calls
them scenario ranges, which is fair, but the omissions are not listed.

Fix: Sample the frit area and the gap (as design-uncertain parameters), or list the omitted quantities under §0.

### R10 — minor — docs/30 text against tiers.md / tiers.json

Place: docs/30 §4.5 rows "frit 1 mm² / 20 mm²" and "half / twice the beads"; §0 bullet 3 and §5.5.

Evidence [V, tiers.md lines 81–87, docs/30 lines 376, 378, 43, 523]:
* §4.5, column "P(≤ 1) / P(≤ 10)": "frit 1 mm² / 20 mm²" shows 0.03 / 0.01, which are P(≤ 1) of the two cases. In the
  column's sense they should read 0.03 / 0.47 and 0.01 / 0.34. "half / twice the beads" shows 0.01 / 0.02 for
  0.01 / 0.35 and 0.02 / 0.44.
* §0 says the earlier design is "reproduced here: 3.49, 0.156", and §5.5 says that re-run with the 10 min half-life it
  is "unchanged (median 3.46)". docs/31 line 142 gives nominal 0.60 → 0.62 and P 0.156 → 0.154 for that re-run, so
  it did change, slightly. Not re-run here.
* Every other number checked matches: §0 table and bullets (including 3.6× and 4.2× between tiers, 45 % / 13 %, and
  1.7× = 2.551/1.491); §1 facts 3–5 (7.9 %; 0.86 and 4.2×10⁻⁶ m/s; 66 %; η 0.988 / 0.621 / 0.0736 [V, own solver]);
  §3.1 (36 mm², 1.25×10⁵, 5.4 min = T_span 322 s, 107 pA, 61 %); §3.4; §3.5 (all 13 rows); §4.1 (2.8×10⁵ enzymes split
  45/31/21/3 %, 170 pA, 1.0 / 15 / 25 bar); §4.4; §4.5 (other rows); §5.1 (0.95, 4.1); §5.3 (all 13 rows and the chain);
  §6.1; §6.2 (all listed pairs); §6.3 (exceptions, 630/60/33, 71/100/14, 2.1/1.5/2.8).

Fix: Correct the two §4.5 rows. In §5.5, write "0.60 → 0.62 nominal, median 3.49 → 3.46".

## My corrected nominal LODs

| Tier | Revision B | Reviewer | Basis |
|---|---|---|---|
| 1 | 9.4 | 9.3 as modelled; 10.8 with a 100 pA A1/B1 step; 5.6 if the 600 s half-life holds in the reservoir (7.9 with the step) | R6 (bore removed), R1 (step size UNVERIFIED, so no upper bound until T1-1), R2 |
| 2 | 2.6 | 2.6 (±5 %) | R7: the uncounted terms roughly cancel |
| 3 | 0.62 | about 0.75 (0.71 capacity; 0.76 + steady currents; 0.79 + plug tail; 0.71 with the sweep-time product). 1.6 if bed 1 is coated at the vendor's capacity and bed 2 at the model's density | R3, R4, R5 (script Part D) |

The order of the tiers and the main conclusions of docs/30 §0 stand. The one-valve case of tier 3 (1.5) is not
affected by R3, which makes it more attractive as the first tier-3 build.

## Checked and found sound

* `check_tierkit.py`: 36 of 36 pass [V].
* The nominal LODs and diagnostics of the three primaries reproduce `tiers.json` exactly [V, script Part A].
* Independent chains (script Part B; agreement with the kit). Tier 1: N_in 3.14×10⁵, slit capture 0.101 of N_in
  (7.9 % of the vial), labelled 0.357, ret_label 0.718, ret_capture 0.826, 6.7×10³ enzymes, 1.61 pA per pg/mL,
  η(150) 0.0736, impurity 106.5 pA, hydrolysis 15.3 pA, blank equivalent 14.65, T_span 322 s; LOD 9.376 against
  9.356 (+0.2 %). Tier 2: bed capture 0.832 of N_in, 5.24×10⁴ enzymes, η(5) 0.621, 2.70 nC per pg/mL, blank
  enzymes 8.47/5.78/0.87/12.5×10⁴; LOD 2.515 against 2.551 (−1.4 %). Tier 3: re-capture 0.951, transfer 0.666,
  1.58×10⁴ enzymes, 0.932 nC per pg/mL; LOD 0.6185 against 0.6205 (−0.3 %). One valve at 5 µL/min × 25 min: 1.679
  against 1.705 (−1.5 %). No difference exceeds 5 %. A first pass of my script was 7.7 % low in tier 2 because it let
  phosphate decay with the product; the kit tracks phosphate as formed product (`kinetics.py` lines 39–44), which is
  right.
* Drift: T_span = t_read + 2(t_front + t_ref/2) = 322 s; formula f · drift · T_span/2 · T as the kit defines it. A_ref =
  7.07 mm² (`model_assumptions.yaml` line 840), so the area exponent has no effect on the tier-1 nominal, as docs/31
  says for N7 [V].
* Pre-run residual 3 % on impurity + hydrolysis (tier 1), step residual 4 % of the impurity charge (tier 2): wired as
  documented [V, tierkit.py 502–511]. In tier 2 the step term is 2.7 % of the variance and not sensitive.
* Product survival over the 420 s stop at 600 s: 0.792 (Derived, (1 − e^−kt)/kt). It scales signal and blank alike.
* Pressures: Kozeny–Carman 1.0 bar at 3.4 µL/min, 15 bar at 50 and 25 bar at 80 µL/min; restrictor 67 psi per µL/min
  (Hagen–Poiseuille, 25 µm × 30 cm, 0.89 mPa·s); transfer line 24 bar at 150 µL/min (Derived).
* Step tables: the sums give 56.9, 58.7 and 58.2 min [V, tiers.md §7].
* Round-1 findings N1–N5, N7, N8, N10–N13 are resolved as docs/31 §3 states. The drift and wall terms now in the kit
  are as described. Not resolved: N6 (resolved only "as a model"; the capacity gap is R3) and N12 (bounded; see R8, R9).

## What could not be checked

* The size of the A1/B1 background step on OEG-coated printed gold (R1) and the stability of free hydroquinone in the
  B1 reservoir (R2): bench quantities, UNVERIFIED.
* The bed-2 site density and valency of an anti-hapten bead, and the release rate (R3): UNVERIFIED. My capacity
  simulation uses k_on of the capture antibody for the anti-hapten binding.
* The real flow pattern of the MicruX wall-jet cell (gap, bore length) and the transit volumes of the valve passages
  (R5): geometry UNVERIFIED (docs/28).
* The re-run of the earlier design (`crosscheck_model.py`) was not repeated. The "(small)" entries of §6.2 (outside
  the top nine) were not checked.
* The availability of the 25 µm restrictors and of fritted 0.2 mm capillaries: outside this lens.
