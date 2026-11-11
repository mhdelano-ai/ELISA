# 03 — Simulation model (Task 3)

Status: first complete version, 2026-11-11. Package `src/elisa_sim/`, tests `tests/`, driver
`scripts/run_baseline.py`, outputs `results/`, added parameters `params/model_assumptions.yaml`.

This document gives the equations, assumptions and validity limits of every sub-model, how parameters map to
the YAML files, the validation against published numbers, the baseline predictions with their uncertainty,
and the known weaknesses. It does **not** choose the design (that is the next task); section 10 says plainly
what the model indicates.

---

## 1. How to run

```bash
pip install -e .            # or: pip install numpy scipy pyyaml matplotlib pytest
python -m pytest -q         # 54 tests: 51 pass, 3 strict-xfail (documented model/publication disagreements)
python scripts/run_baseline.py --n 1000   # ~2 min; writes results/*.csv, results/*.png
```

The first call builds the transport look-up tables (finite-difference solutions, ~30 s) and stores them in
`results/cache/` (git-ignored, regenerated automatically).

Programmatic use (what the ranking / design task needs):

```python
from elisa_sim.params import ParameterSet
from elisa_sim import architectures as A, montecarlo, sensitivity
from elisa_sim.model import evaluate

ps = ParameterSet.load()                                   # chemistry.yaml + hardware.yaml + model_assumptions.yaml
arch = A.get("B-mag1-IDA/alp_hqdp")                        # or build one: A.Architecture(name=..., scheme="B", ...)
r = evaluate(arch, ps)                                     # nominal: r.lod_pgml, r.blank_sd, r.variance_fractions(), ...
arch2 = arch.with_design(**{"hw.timing.accumulation_time": 15})   # change a design variable (YAML units)
mc = montecarlo.run(arch2, ps, n=2000); print(mc.summary())        # median, 5-95 %, P(LOD <= 1 pg/mL)
oat = sensitivity.one_at_a_time(arch2, ps); glob = sensitivity.global_indices(mc)
```

`Result` fields: `conc_pgml`, `net_signal` (C), `blank_mean` (C), `blank_sd` (C), `lod_pgml` (mean blank +
3 SD through the calibration curve), `lod_slope_pgml` (3 SD / low-end slope), `uloq_pgml`,
`dynamic_range_decades`, `cycle_time_min`, `time_to_result_min`, `variance_terms` (C², per blank source),
`limiting_term`, `diagnostics` (every intermediate: delivered fraction, loop transfer, capture fraction,
label fraction, enzymes per pg/mL, NSB enzymes, cell conversion, carry-over after the top standard, …).

## 2. Package structure

| Module | Content |
|---|---|
| `units.py` | Strict unit parser/converter (SI + count dimension); every parameter is read *in a requested unit* and a dimension mismatch raises. |
| `params.py` | Loads the three YAML files (`chem.*`, `hw.*`, `ma.*` keys), `overrides`, bound checks, unit-checked access with access recording, Monte Carlo sampling. |
| `constants.py` | SI defining constants; analytic constants of the Lévêque/Levich and Graetz problems. |
| `transport.py` | Marching FD solver (tube/slit, perfect-sink or reactive wall), tabulated conversions; transient loop-transfer solver; Wilson–Geankoplis, Smoluchowski, Levich channel, wall-jet, Aoki IDA, tanks-in-series. |
| `kinetics.py` | RK4; enzyme accumulation (Michaelis–Menten, substrate depletion, competitive Pi inhibition, hydrolysis, product decay); reversible binding; one-step sandwich (hook effect). |
| `architectures.py` | `Architecture` dataclass, chemistry/capture/detector descriptors, compatibility `check`, registry of 83 runnable combinations. |
| `timing.py` | Cycle timeline per scheme and the dissociation exposure windows. |
| `model.py` | `evaluate(arch, ps)` – the common interface (sections 3.1–3.9). |
| `montecarlo.py` | `run(arch, ps, n)` and `MCResult.summary()`. |
| `sensitivity.py` | One-at-a-time, Spearman rank correlation, first-order (correlation-ratio) index. |
| `validation.py` | Published-value comparisons used by tests and this document. |

## 3. Sub-models: equations, assumptions, validity

Notation: N = molecule numbers, C = concentration (mol/m³ internally), Q = volumetric flow, D = diffusion
coefficient, N_A Avogadro, F Faraday. Every symbol's parameter key is given in brackets.

### 3.1 Sample delivery (fixed-loop SM-FL)

N_sample = C·V_s·N_A, V_s = 100 µL [`ma.delivery.sample_volume`].

Delivered analyte: N_del = N_sample · f_del · (1 − L_ads) · f_tr

* f_del per injection mode [`hw.smfl.delivered_fraction_plno_250loop` 0.82, `…plpa_250loop` 0.97,
  `…plno_100loop` 0.75].
* L_ads adsorptive loss [`ma.delivery.adsorptive_loss_fraction_with_carrier` 0.2 (0.02–0.6), UNVERIFIED;
  untreated option `chem.analyte.adsorptive_loss_fraction_untreated_tube`]. Scales signal, not blank.
* f_tr loop transfer after n_flush loop volumes [`hw.smfl.loop_flush_volumes_for_transfer` = 3]: transient
  2-D axisymmetric convection–diffusion in the loop (Poiseuille u = 2U(1−r²/R²), van Leer TVD advection,
  implicit radial diffusion, no-flux wall), controlled by β = D·V_loop/(Q·R²) and the plug fraction/position.
  Tabulated in β and n. Loop ID [`hw.smfl.loop_inner_diameter`, UNVERIFIED] is sampled. Beads (magnetic
  architectures) use the D → 0 limit.
* The same solver gives the **peak outlet concentration** of a small reagent plug; the conjugate concentration
  stopped in the reactor is C_vial × peak × [`ma.delivery.tubing_dilution_factor`]. For a 20 µL conjugate plug
  in a 250 µL loop at 100 µL/min the peak is only 0.12 of the vial concentration – a design-relevant finding
  (the plug is smeared over about one loop volume).

Validity: straight tube (coiling adds mixing → conservative), axial molecular diffusion neglected
(Pe ≫ 1), PLNO plug position assumed at the far end (`ma.delivery.plug_at_outlet_end` = 0, the slower
case of the Task 2 table). Sample-loop dilution matters for capture only through residence time (below).

### 3.2 Capture

Active capture-antibody density Γ = ρ_Ab·φ_act/N_A [`chem.surfaces.igg_surface_density_monolayer`,
`chem.surfaces.active_fraction_oriented`]; surface reaction rate constant k_r = k_on,c·Γ_free (m/s)
[`chem.antibodies.kon_capture`], with Γ_free = Γ(1 − θ) and θ the occupancy (fixed-point iteration → site
saturation at high dose).

**Flow-through reactors (single pass, plug flow):**

* Packed bed (non-porous beads d_p, porosity ε, column ID): area A = 6(1−ε)V_bed/d_p; film mass transfer
  Wilson–Geankoplis Sh = (1.09/ε)Re^(1/3)Sc^(1/3) [`ma.correlations.wilson_geankoplis_coefficient`];
  k = (1/k_m + 1/k_r)⁻¹; **f_cap = 1 − exp(−k·A/Q)**. Validity: 0.0016 < Re < 55 (the assay runs at
  Re ≈ 0.01–0.1); internal porosity of real media not modelled.
* Open-tubular capillary and monolith (bundle of straight channels): exact steady Graetz problem with a
  reactive wall, `conversion("tube", ξ, Da)`, ξ = πLD/Q (per channel), Da = k_r R/D, from the marching FD
  solver (tabulated over Da 10⁻⁴–10⁴ and ∞). Limits: Da → ∞ Graetz/Lévêque; Da → 0 kinetic 1 − exp(−2Da ξ).
* Chip planar capture (Scheme C): same with a slit channel, one active wall, ξ = LDw/(QH), Da = k_r H/D.

Capture happens during loading at Q = [`hw.timing.sample_load_flow`] (100 µL/min).

**Magnetic beads (renewed every run, pre-dispensed in the sample vial):** pseudo-first-order rate
k = f_unstirred · n_b · k_D k_R/(k_D + k_R) with Smoluchowski k_D = 4πDa and k_R = k_on·sites/N_A per bead
[`chem.surfaces.bead_number_per_100uL_digital_ELISA`, `ma.geometry.magnetic_bead_diameter`,
`ma.capture.in_vial_unstirred_rate_factor` 0.5 (UNVERIFIED; the SM-FL cannot mix a vial)];
**f_cap = k/(k + k_off)·(1 − e^{−(k+k_off)t_vial})**. Then f_del · f_tr · trap efficiency
[`ma.capture.magnetic_trap_efficiency`].

**One-step in-vial format** (beads + conjugate pre-dispensed; needs the user's answer to Task 2 Q4): full
ODE system A + C ⇌ AC, A + D ⇌ AD, AC + D ⇌ ACD, AD + C ⇌ ACD, which produces the high-dose hook effect when
analyte approaches the conjugate concentration (tested; outside the 1–1000 pg/mL range at 1 nM conjugate).

**Retention:** captured analyte dissociates until the reactor is sealed with substrate,
exp(−k_off,c·t_c); detection antibody likewise exp(−k_off,d·t_d) from the end of its incubation
(timing.py). In Scheme A (no sealing) dissociation continues to the middle of the read window. Rebinding on
dense surfaces (Chang2012 effective K_D) is **not** credited – conservative.

### 3.3 Labelling, non-specific binding, carry-over

Labelled fraction (pseudo-first order, conjugate in excess):
f_lab = k_on,d·C/(k_on,d·C + k_off,d)·(1 − e^{−(k_on,d C + k_off,d)t}), C = stopped conjugate concentration
(Schemes B/C), or for Scheme A (flow-through, no stop) an exposure ∫C dt = C_vial·V_inj/Q.
Two-step chemistries (biotin-dAb then SβG or SA-polyHRP): product of the two steps with k_on of
streptavidin–biotin [`chem.antibodies.streptavidin_biotin_kon`] and
[`ma.labelling.effective_biotins_per_detection_antibody`]. Enzymes per label [`chem.antibodies.enzyme_to_antibody_ratio_*`,
`chem.antibodies.poly_HRP_per_streptavidin_polymer`, `ma.labelling.sbg_enzymes_per_conjugate`].
Labelling is reaction-limited (captured targets are sparse, so the transport Damköhler number is ≪ 1).

**Conjugate NSB** (linear, irreversible): N_nsb = k_nsb · Σ(A_i·s_i) · E · N_A · (enzymes per label) · x_cross,
with E = ∫C dt the exposure to the enzyme-carrying reagent [`chem.nsb.nsb_effective_rate_constant`
4×10⁻¹¹ m/s, derived by Task 1 from Rissin2010], surface factors s_i relative to blocked digital-ELISA beads
[`ma.nsb.surface_factor_*`, UNVERIFIED], label factors [`ma.nsb.label_factor_*`] and residual
detection-on-capture cross-reaction [`ma.labelling.detection_on_capture_residual_factor`]. Surfaces counted
are those whose product reaches the electrode: capture surface, reactor walls, and in Scheme B the
reactor connection tubing sealed with the reactor [`ma.geometry.reactor_connection_length`]; in Scheme A the
whole wetted path injector → reactor → cell. For two-step labels the NSB of the biotin-dAb that is then
reached by SA-enzyme is added.

**Carry-over** (enzymes in the accumulation volume of a blank that follows a blank):
(i) injected-substrate variant: c_inj·N_conj·min(1, V_acc/V_loop);
(ii) conjugate carried into the next cycle's sample through an intervening regeneration/cleaning
injection: c_inj²·N_conj·(1 − e^{−k_nsb A_eff/Q}) [`hw.smfl.carryover_protein_conjugate`, UNVERIFIED];
(iii) residual label surviving regeneration: r(1 − inactivation)/(1 − r(1 − inactivation))·(N_nsb + N_carry)
[`chem.regeneration.residual_label_carryover_fraction`, `…inactivation_by_low_pH_regeneration`]; renewable
beads keep only the trap-wall share.
The carry-over after the 1000 pg/mL standard is reported separately (`carryover_after_top_pgml`).

**Environmental IgG contamination of blanks** [`ma.nsb.blank_igg_contamination_equivalent`, 0 nominal,
MC up to 3 fM]: treated as analyte with SD = mean.

### 3.4 Signal generation

**Stopped flow (Schemes B, C):** enzymes N_E (specific + NSB + carry-over) in the accumulation volume V_acc
(bed void, capillary/channel volume or trap volume) for t_acc [`hw.timing.accumulation_time`]:

dP/dt = k_cat·E·S/(K_m(1 + n_Pi·P_formed/K_i) + S) − k_dec·P,  dS/dt = −v − k_hyd·S

[`k_cat`, `K_m`, `K_i` for ALP (phosphate competitive inhibition), `n_Pi` (2 for HQDP), `k_hyd`
non-enzymatic hydrolysis, k_dec = ln2/t½ product autoxidation]; RK4, 200 steps (converged to 10⁻⁶).
Free product impurity in the substrate (fraction × S₀) is present from t = 0 but is measured by the
baseline of the same run (Scheme B flowing substrate; Scheme C fill-time baseline). The signal is the
net product formed by the specific enzymes (S(total) − S(blank enzymes)), so substrate depletion and Pi
inhibition shared with NSB enzymes are handled consistently. Pi inhibition is what bends the ALP
calibration above ~10³ pg/mL.

**Continuous flow (Scheme A, reactor not isolable):** steady turnover current
i = n F η(Q) G · Σ N_E k_cat S₀/(K_m + S₀)/N_A, integrated over the read window. The substrate background
(impurity + hydrolysis during the reservoir age [`ma.timing.substrate_reservoir_age`]) flows continuously and
cannot be referenced within the run.

### 3.5 Transfer to the electrode and readout

* Flow-through cells (Scheme B): product plug swept at Q_read [`ma.readout.sweep_flow` 50 µL/min; ≥
  `hw.flow_cells.thermo_6011rs_coulometric.min_flow` for the coulometric cell]; fraction eluted in the read
  window from a tanks-in-series residence-time distribution, N_eff = V_acc²/(V_acc²/N + σ_t²)
  [`ma.readout.tanks_*`, `hw.tubing.product_plug_sigma_reactor_to_cell`]. Charge
  **Q = n F η f_el n_P G**. Because the conversion η of a partial-conversion cell is independent of
  concentration, dispersion changes only the window length needed (and therefore the noise), not the charge.
* **Thin-layer channel cell:** η from the exact slit solution (perfect sink), ζ = D L w/(Q H); in the
  Lévêque regime this equals the **Levich channel equation** I = 0.925 nFcw x_e^{2/3}D^{2/3}(Q/(h²d))^{1/3}
  (h = half-height), and η → 1 (coulometric) at low flow. 3 mm disk treated as an equal-area square.
  (At 50 µL/min, 51 µm gasket: η ≈ 0.36; Task 2 listed 0.05 (0.01–0.5) UNVERIFIED.)
* **Wall-jet** (SenCell, DropSens SPE): η = C D^{2/3} ν^{−5/12} a^{−1/2} R^{3/4} Q^{−1/4}
  [`ma.detection.walljet_coefficient` 0.898–1.597, nozzle `ma.geometry.walljet_nozzle_diameter`]. η ≈ 0.017
  (SenCell) and 0.03 (SPE), inside Task 2's 0.5–20 % ranges. Valid for a free jet (confined cells deviate).
* **Coulometric porous cell:** η = [`hw.flow_cells.thermo_6011rs_coulometric.collection_efficiency`] 0.95.
* **Flow IDA:** generator conversion (slit solution over the IDA) × redox-cycling amplification
  [`hw.flow_cells.ida_redox_cycling.amplification`, 3–100].
* **Stopped IDA in the chip (Scheme C):** Aoki steady-state generator–collector current
  i = m b n F c D[0.637 ln(2.55(1 + w/g)) − 0.19/(1 + w/g)²] × efficiency [`ma.detection.aoki_*`,
  `ma.detection.ida_stopped_efficiency`], c = n_P/V_acc, charge = i·T_read (cycling does not consume product).
* Chemical redox cycling (TCEP with AAP): gain G [`chem.substrates.pAP.chemical_redox_cycling_gain`] applied
  to every product (specific and background alike) and a noise penalty [`ma.chemistries.alp_aap.tcep_noise_factor`].
  Note: Task 1 states the gain as "fold improvement in LOD"; it is used here as a current gain – it
  can only improve the LOD where electrochemical noise limits.

### 3.6 Noise and blank statistics

Blank variance = sum of independent terms (each reported; the largest is the "limiting term"):

| Term | Expression |
|---|---|
| `nsb_variability` | (CV_nsb·Q_nsb)² + (RSD_inj·Q_nsb)² + (CV_bead·Q_nsb,beads)² [`chem.nsb.blank_CV_analog_electrochemical`, `hw.smfl.injection_precision_rsd_large`, `ma.capture.bead_dose_cv`] |
| `label_counting` | q_e²·N_blank-enzymes (Poisson) |
| `carryover` | (CV_carry·Q_carry)² [`ma.noise.carryover_cv`] |
| `substrate_background` | B/C: (CV_sub·Q_hyd)² + (ε_bg·(Q_imp + Q_hyd))²; A: (CV_sub² + ε_bg²)(Q_imp + Q_hyd)² [`ma.noise.substrate_background_cv`, `ma.noise.background_current_relative_noise`] |
| `electrode_sensitivity` | (CV_sens·Q_unreferenced)², CV_sens = non-fouling / fouling (pAP, TMB, or any Scheme C chip) / disposable SPE [`ma.noise.electrode_sensitivity_cv_*`, `ma.noise.spe_sensor_to_sensor_cv`] |
| `electrochemical_noise` | 2·i_n²·T/(2B), i_n = max(floor, i_ref (A/A_ref)^α) [`hw.gamry.noise_rms_flow` / `…stopped_flow`, `ma.noise.area_exponent`, floor `hw.gamry.antec_decade_floor_pp`/`ma.noise.pp_to_rms`] |
| `baseline_drift` | (f_res·½·d·T²)² [`hw.gamry.baseline_drift`, `ma.noise.drift_residual_fraction`] |
| `contamination` | Q_cont² |

LOD = concentration at which the net calibration signal equals 3·SD_blank [`ma.statistics.k_sd`] (log–log
interpolation on the calibration grid 0.01–10⁵ pg/mL; linear extrapolation below), plus the slope form
3·SD/slope. ULOQ = highest concentration up to which d ln S/d ln C ≥ 0.8. Signal variance at the LOD is not
included (the brief's blank-based definition).

Blank-limited LOD ≈ 3·CV_nsb·B, where B is the analyte-equivalent blank (diagnostic
`blank_equivalent_pgml`); with CV = 10 %, LOD ≤ 1 pg/mL needs B ≲ 3 pg/mL (20 fM), as Task 1 noted.

### 3.7 Timing

Per docs/02 §7.4: sample = overhead + n_flush·V_loop/Q_load + wash; labelling step = overhead + fill +
stopped incubation + wash (Scheme A: plug pushed through at the loading flow); substrate fill +
accumulation + readout (Scheme A: fill + stabilisation + readout); regeneration (6.5 min) or, for renewable
beads, bead release + cleaning injection [`ma.timing.bead_flush_and_clean`]. Injected substrate adds
6 min. In-vial bead incubation [`ma.timing.in_vial_incubation` 30 min] is added to **time-to-result**
(not to instrument occupancy, since it overlaps the previous sample). The Scheme B baseline reproduces
Task 2's 38 min exactly (test).

### 3.8 Reuse

Per cycle: capture capacity loss [`chem.regeneration.activity_loss_per_cycle`] for regenerated surfaces (0 for
renewed beads), electrode sensitivity loss [`ma.reuse.electrode_sensitivity_loss_per_cycle_*`], residual
label per cycle (3.3 iii). `results/reuse.csv` gives the cycles until the slope has drifted by 10 %
[`ma.reuse.slope_drift_tolerance`] – the recalibration interval – and the carry-over after the top
standard.

## 4. Architectures covered

Scheme (A/B/C, docs/02 §7) × capture (packed bed, monolith, capillary, magnetic beads sequential or
one-step, chip planar, chip bead bed) × detector (thin-layer, wall-jet SenCell, wall-jet SPE, coulometric,
flow IDA, stopped IDA) × chemistry (Task 1 list: ALP/HQDP, ALP/AAP + TCEP, biotin-dAb + SβG/pAPG,
ALP/pAPP, IgG-HRP/TMB, biotin-dAb + SA-polyHRP/TMB) = 14 base configurations × 6 chemistries; 5
combinations are rejected by `check` (IDA with irreversible ascorbate; `results/skipped_architectures.csv`),
plus 4 plumbing variants (injected substrate, PLPA 97 µL, untreated sample, PLPA for beads): **83
architectures**. Names read `<scheme>-<capture>-<detector>/<chemistry>[/variant]`; `mag1` = one-step
in-vial.

## 5. Units and parameter mapping

All numbers come from `params/*.yaml`; the code requests each parameter in an explicit unit and
`units.convert` checks the dimension (the checker caught a count-vs-ratio inconsistency and a percent bug
during development). Only SI defining constants and analytic transport constants live in code
(`constants.py`). Numerical settings (RK4 steps, grid sizes) are in `ma.numerics`. Design variables are
listed in `monte_carlo.fixed_patterns` and never sampled; an architecture can pin them with
`Architecture.with_design(...)`.

## 6. Parameters added or questioned

### 6.1 Added (`params/model_assumptions.yaml`)

All entries carry source/confidence; those marked UNVERIFIED are this task's estimates. The ones with the
largest leverage on the predictions are in **bold**.

* Fluid: viscosity, density (standard values).
* Delivery: **adsorptive loss with carrier protein (0.2, 0.02–0.6, UNVERIFIED)**, plug position, conjugate
  injection volume, tubing dilution.
* Geometry (design choices): column ID, monolith/capillary/chip/IDA/trap dimensions, thin-layer channel
  width (UNVERIFIED), wall-jet nozzle (UNVERIFIED), coulometric electrode area (UNVERIFIED), **reactor
  connection length (0.1 m, from docs/02 §7.5)**.
* Capture: **in-vial unstirred rate factor (0.5, UNVERIFIED)**, magnetic trap efficiency, bead dose CV.
* Labelling: SA-polyHRP concentration, biotins per dAb, SβG enzymes per conjugate, residual
  detection-on-capture factor.
* NSB: **surface factors per surface type (beads 1, bed/monolith/capillary/tubing 3 (1–30), chip 10
  (1–100); all UNVERIFIED)**, label factors, dAb NSB labelling, contamination.
* Chemistry gaps: HQDP K_m, **free-product impurity and hydrolysis for HQDP, AAP, pAPG, TMB (all
  UNVERIFIED, 4 orders of magnitude wide)**, product half-lives, AA and TMB(ox) D, TCEP noise penalty,
  β-gal/HRP inactivation by regeneration, fouling flags.
* Detection: wall-jet coefficient (0.898–1.597), Aoki constants (recalled, not verified this session), IDA
  stopped efficiency.
* Correlations: Wilson–Geankoplis coefficient (recalled, not verified this session).
* Readout: sweep and continuous flows, tanks-in-series numbers (UNVERIFIED).
* Noise: reference electrode area, **area exponent**, p-p/rms factor, bandwidth, **drift residual fraction**,
  **background relative noise**, **substrate background CV**, **electrode sensitivity CVs**, SPE CV,
  carry-over CV.
* Timing: post-sample wash, conjugate fill, second-label incubation, injected-substrate extra, bead
  flush/clean, continuous stabilisation, substrate reservoir age, in-vial incubation.
* Reuse: electrode sensitivity loss per cycle; slope tolerance. Statistics: k = 3, ULOQ criterion, targets.
* Validation scenario inputs (section 8).

### 6.2 Missing in Task 1/2 and filled here

HQDP K_m and blank rates; AAP/pAPG/TMB impurity and hydrolysis; wall-jet nozzle and thin-layer channel
width; trap geometry; how fast beads capture in an unstirred SM-FL vial.

### 6.3 Questioned (Task 1/2 files not edited)

1. **ALP k_cat in assay conditions** (`chem.enzymes.alp.kcat_conjugate_assay_conditions` = 1000 s⁻¹, 100–6000).
   Two published ALP detection limits imply a lower effective turnover: DellaCiana1996 → 180 s⁻¹,
   Thompson1991 → 23 s⁻¹ (below the Task 1 low bound). Because the predicted LODs are NSB-limited, k_cat
   cancels to first order (it scales signal and NSB blank alike), so this does not change the ranking; it
   matters for electrochemical-noise-limited variants.
2. **NSB rate constant** (`chem.nsb.nsb_effective_rate_constant` = 4×10⁻¹¹ m/s, derived from digital-ELISA
   beads at 15 pM SβG). Extrapolated linearly to a conventional plate ELISA with 1–10 nM label it predicts a
   blank of 0.78–2.9 pM, 9–35× the 85 fM reported (Rissin2010). NSB is probably sub-linear (saturable) in
   label exposure, or plate surfaces are cleaner. The baseline therefore also reports a
   **"plate-calibrated NSB"** scenario with k_nsb = 4.4×10⁻¹² m/s (the value that reproduces 85 fM at 1 nM
   label) – this is below Task 1's low bound (8×10⁻¹²).
3. **Thin-layer / wall-jet collection efficiencies** in hardware.yaml (UNVERIFIED) are replaced by computed
   values (thin-layer 0.36 at 50 µL/min vs 0.05 listed).
4. `chem.substrates.pAP.chemical_redox_cycling_gain` is defined as "fold improvement in LOD"; used as a current
   gain (section 3.5).
5. `hw.timing.sample_load_time` is not used; the load time is computed from loop volume, flush volumes and flow.

## 7. Monte Carlo and sensitivity

* Inputs: every parameter the architecture reads (recorded by `ParameterSet.get`), except design variables
  and fixed (low = high) entries – 40–55 parameters per architecture.
* Distribution (stated assumption): **log-triangular(low, value, high) when low > 0 and high/low ≥ 3, else
  triangular(low, value, high)**; independent draws (k_on and k_off sampled independently; K_D not used).
  Bounds in the YAML files are "plausible", not confidence limits, so the intervals are scenario ranges,
  not statistical confidence intervals.
* Outputs: median and 5–95 % of LOD, P(LOD ≤ 1 pg/mL), P(LOD ≤ 1 and ULOQ ≥ 1000), limiting-term mode.
* Sensitivity: one-at-a-time (each parameter at its low/high bound; Δlog₁₀ LOD), Spearman rank correlation
  with log LOD, first-order index Var(E[log LOD|X])/Var(log LOD) from 20 equal-count bins
  (`results/sensitivity_*.csv`, `results/fig_tornado.png`).

## 8. Validation

Physics limits (tests, all pass): mass conservation (enzyme ODE, loop transfer, one-step sandwich species);
Lévêque/Levich channel limit (2 %), Graetz series (1 %), tube Lévêque (3 %), kinetic limits of the reactive
wall (1 %), thin-layer → coulometric at low flow, convective loop limit 1 − V_loop/(4V) (1 %); zero-order,
first-order and exact (Lambert-W) integrated Michaelis–Menten; reversible-binding equilibrium limit; hook
effect in the one-step ODE; wall-jet Q^(3/4) scaling; no-analyte case gives exactly the blank; the blank
with NSB/carry-over/substrate removed equals the closed-form electrochemical noise + drift; calibration
monotonic below 1000 pg/mL for all 83 architectures; LOD from the curve = 3 SD/slope in the linear regime;
MC with nominal "samples" reproduces the scalar result; Scheme B timeline = 38 min.

Published / worked values (`results/validation.csv`, `tests/test_validation.py`):

| Comparison | Model | Published | Model/published | Status |
|---|---|---|---|---|
| Task 1 estimate: 10⁵ ALP, 10 min, 10 µL → ~10 nM product | 9.4 nM | 10 nM | 0.94 | agrees |
| Task 2 loop-transfer table (6 cases × 4 flush volumes) | — | — | max abs. diff 0.006 | agrees |
| HQ FIA LOD, GC wall-jet + Task 2 noise (DellaCiana1996) | 0.26 nM | 0.12 nM | 2.2 | agrees within the unknown flow/electrode size |
| Free-ALP LOD, 10 min, HQ (DellaCiana1996) | 0.22 fM | 1.2 fM | 0.18 | model 5.5× optimistic; implied k_cat 180 s⁻¹ (strict xfail for 2×) |
| ALP LOD, 15 min, pAPP, 7 nM pAP (Thompson1991) | 0.0012 µg/L | 0.05 µg/L | 0.023 | **disagrees 44×**; implied k_cat 23 s⁻¹ (strict xfail) |
| Bead capture 30 min, 5×10⁵ beads (Chang2012-derived 70 %) | 0.49 | 0.70 | 0.70 | agrees within 35 %; lower because the model includes the 0.85 active fraction, bead diffusion and k_off (the Task 1 formula alone gives 0.71) |
| Simoa blank equivalent (Rissin2010, closure check – same source as k_nsb) | 2.4 fM | 1.5 fM | 1.6 | consistent (not independent) |
| Conventional plate-ELISA blank (Rissin2010 85 fM), 10 nM / 1 nM label | 2.9 / 0.78 pM | 85 fM | 35 / 9.2 | **disagrees** (strict xfail); see 6.3(2) |

Not usable quantitatively (missing conditions in the abstracts): Xu1989 (0.81 pg/mL mouse IgG, well
format), Kokado2000, Masson1995, deFrutos1993 (qualitatively reproduced: open-capillary single-pass capture
is mass-transfer limited, 2.8 % at 100 µL/min in a 10 cm × 100 µm capillary).

## 9. Baseline results

`python scripts/run_baseline.py --n 1000` (seed 20261111; log in `results/baseline_log.txt`). Full table:
`results/baseline_results.csv` (83 rows, 60 columns incl. variance shares and diagnostics); condensed:
`results/baseline_table.md`. Figures: `results/fig_lod_intervals.png` (all architectures),
`fig_calibration.png`, `fig_blank_breakdown.png`, `fig_tornado.png`.

Rows sorted by Monte Carlo median LOD. "inf" = 3 SD not reached within the 10⁵ pg/mL calibration grid. "Plate-calibrated NSB" = nominal LOD with k_nsb = 4.4×10⁻¹² m/s (section 6.3(2)). Limiting term = largest blank-variance term at nominal parameters. All values are model predictions with the stated parameter uncertainty, not measurements.

| Architecture | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD<=1) | LOD, plate-calibrated NSB (pg/mL) | Blank equiv. B (pg/mL) | ULOQ (pg/mL) | Cycle / to result (min) | Limiting term |
|---|---|---|---|---|---|---|---|---|
| B-mag1-IDA/alp_hqdp | 17 | 80 [5.6-4.2e+03] | 0.004 | 1.9 | 57 | 2.3e+03 | 26.0 / 56.0 | nsb_variability |
| B-mag1-IDA/hrp_tmb | 24 | 1.3e+02 [9.2-5.9e+03] | 0.000 | 2.7 | 57 | 3.4e+04 | 26.0 / 56.0 | electrode_sensitivity |
| B-mag1-IDA/alp_papp | 24 | 1.3e+02 [11-5.9e+03] | 0.000 | 3 | 58 | 6.8e+03 | 26.0 / 56.0 | electrode_sensitivity |
| B-mag-IDA/alp_hqdp/PLPA97 | 67 | 4.4e+02 [32-2.4e+04] | 0.000 | 7.9 | 2.2e+02 | 3.4e+04 | 35.0 / 65.0 | nsb_variability |
| B-mag-TL/alp_hqdp | 80 | 5.1e+02 [45-3.6e+04] | 0.000 | 14 | 2.6e+02 | 3.4e+04 | 35.0 / 65.0 | nsb_variability |
| B-mag-IDA/alp_hqdp | 80 | 5.2e+02 [38-2.8e+04] | 0.000 | 9.3 | 2.6e+02 | 3.4e+04 | 35.0 / 65.0 | nsb_variability |
| B-mag-TL/hrp_tmb | 1.1e+02 | 8.7e+02 [68-6.2e+04] | 0.000 | 15 | 2.7e+02 | 1e+05 | 35.0 / 65.0 | electrode_sensitivity |
| B-mag-IDA/hrp_tmb | 1.1e+02 | 8.9e+02 [69-4.6e+04] | 0.000 | 14 | 2.7e+02 | 1e+05 | 35.0 / 65.0 | electrode_sensitivity |
| B-mag-TL/alp_aap | 1.1e+02 | 1e+03 [69-6.4e+04] | 0.000 | 76 | 2.8e+02 | 2e+04 | 35.0 / 65.0 | nsb_variability |
| B-mag-TL/alp_papp | 1.2e+02 | 1.1e+03 [88-5.2e+04] | 0.000 | 23 | 2.8e+02 | 1e+05 | 35.0 / 65.0 | electrode_sensitivity |
| B-mag-IDA/alp_papp | 1.2e+02 | 1.1e+03 [99-5.9e+04] | 0.000 | 21 | 2.8e+02 | 1e+05 | 35.0 / 65.0 | electrode_sensitivity |
| C-bed-IDA/alp_hqdp | 2.8e+02 | 1.3e+03 [1e+02-2.4e+04] | 0.000 | 29 | 6.7e+02 | 6.8e+03 | 38.0 / 38.0 | nsb_variability |
| C-bed-IDA/alp_papp | 2.7e+02 | 1.4e+03 [1.2e+02-2.5e+04] | 0.000 | 30 | 6.4e+02 | 2e+04 | 38.0 / 38.0 | electrode_sensitivity |
| C-bed-IDA/hrp_tmb | 2.6e+02 | 1.4e+03 [1.3e+02-2.3e+04] | 0.000 | 29 | 6.2e+02 | 1e+05 | 38.0 / 38.0 | electrode_sensitivity |
| B-bed-TL/alp_hqdp/PLPA97 | 5.3e+02 | 1.6e+03 [1.5e+02-3.5e+04] | 0.000 | 54 | 1.8e+03 | 2e+04 | 38.0 / 38.0 | nsb_variability |
| B-bed-TL/alp_hqdp | 6.2e+02 | 1.9e+03 [1.8e+02-4.1e+04] | 0.000 | 64 | 2.1e+03 | 2e+04 | 38.0 / 38.0 | nsb_variability |
| B-bed-IDA/alp_hqdp | 6.2e+02 | 2e+03 [2e+02-3.4e+04] | 0.000 | 64 | 2.1e+03 | 2e+04 | 38.0 / 38.0 | nsb_variability |
| B-bed-COUL/alp_hqdp | 6.2e+02 | 2e+03 [2e+02-3.4e+04] | 0.000 | 64 | 2.1e+03 | 2e+04 | 38.0 / 38.0 | nsb_variability |
| B-bed-WJ/alp_hqdp | 6.2e+02 | 2e+03 [2e+02-3.3e+04] | 0.000 | 82 | 2.1e+03 | 2e+04 | 38.0 / 38.0 | nsb_variability |
| B-bed-TL/alp_aap | 6.4e+02 | 2.2e+03 [2.2e+02-3.2e+04] | 0.000 | 74 | 2.2e+03 | 2e+04 | 38.0 / 38.0 | nsb_variability |
| B-bed-COUL/alp_aap | 6.4e+02 | 2.2e+03 [1.8e+02-2.8e+04] | 0.000 | 74 | 2.2e+03 | 2e+04 | 38.0 / 38.0 | nsb_variability |
| B-bed-WJ/alp_aap | 6.4e+02 | 2.3e+03 [2e+02-3.1e+04] | 0.000 | 74 | 2.2e+03 | 2e+04 | 38.0 / 38.0 | nsb_variability |
| B-cap-TL/alp_hqdp | 5.3e+02 | 2.4e+03 [2.5e+02-4.2e+04] | 0.000 | 80 | 1.7e+03 | 1e+05 | 38.0 / 38.0 | nsb_variability |
| B-bed-TL/alp_hqdp/injected-substrate | 8.8e+02 | 2.7e+03 [2.3e+02-5e+28] | 0.000 | 92 | 3e+03 | 3.4e+04 | 44.0 / 44.0 | nsb_variability |
| B-bed-SPE/alp_papp | 8.3e+02 | 2.8e+03 [2.9e+02-4.1e+04] | 0.000 | 95 | 2e+03 | 5.8e+04 | 38.0 / 38.0 | electrode_sensitivity |
| B-bed-SPE/hrp_tmb | 8.1e+02 | 2.9e+03 [3.4e+02-4.8e+04] | 0.000 | 90 | 1.9e+03 | 1e+05 | 38.0 / 38.0 | electrode_sensitivity |
| B-bed-SPE/alp_hqdp | 8.7e+02 | 2.9e+03 [3e+02-5.1e+04] | 0.000 | 95 | 2.1e+03 | 2e+04 | 38.0 / 38.0 | nsb_variability |
| B-bed-WJ/alp_papp | 8.3e+02 | 3e+03 [2.9e+02-4.3e+04] | 0.000 | 1e+02 | 2e+03 | 5.8e+04 | 38.0 / 38.0 | electrode_sensitivity |
| B-bed-TL/hrp_tmb | 8.1e+02 | 3e+03 [3.1e+02-6.2e+04] | 0.000 | 89 | 1.9e+03 | 1e+05 | 38.0 / 38.0 | electrode_sensitivity |
| B-bed-IDA/alp_papp | 8.3e+02 | 3e+03 [2.9e+02-4.5e+04] | 0.000 | 91 | 2e+03 | 5.8e+04 | 38.0 / 38.0 | electrode_sensitivity |
| B-bed-COUL/alp_papp | 8.3e+02 | 3e+03 [2.9e+02-4.5e+04] | 0.000 | 91 | 2e+03 | 5.8e+04 | 38.0 / 38.0 | electrode_sensitivity |
| B-bed-WJ/hrp_tmb | 8.1e+02 | 3.1e+03 [3.2e+02-5.1e+04] | 0.000 | 92 | 1.9e+03 | 1e+05 | 38.0 / 38.0 | electrode_sensitivity |
| B-bed-IDA/hrp_tmb | 8.1e+02 | 3.2e+03 [2.8e+02-5e+04] | 0.000 | 89 | 1.9e+03 | 1e+05 | 38.0 / 38.0 | electrode_sensitivity |
| B-bed-COUL/hrp_tmb | 8.1e+02 | 3.2e+03 [2.8e+02-5e+04] | 0.000 | 89 | 1.9e+03 | 1e+05 | 38.0 / 38.0 | electrode_sensitivity |
| B-bed-TL/alp_papp | 8.3e+02 | 3.2e+03 [3.1e+02-4.9e+04] | 0.000 | 91 | 2e+03 | 5.8e+04 | 38.0 / 38.0 | electrode_sensitivity |
| B-bed-TL/alp_hqdp/untreated-sample | 9.9e+02 | 3.2e+03 [2.8e+02-5.7e+04] | 0.000 | 1e+02 | 3.3e+03 | 3.4e+04 | 38.0 / 38.0 | nsb_variability |
| B-bed-SPE/alp_aap | 8.9e+02 | 3.2e+03 [2.7e+02-4.1e+04] | 0.000 | 98 | 2.2e+03 | 2e+04 | 38.0 / 38.0 | electrode_sensitivity |
| B-cap-TL/alp_aap | 5.6e+02 | 3.5e+03 [2.9e+02-5.6e+04] | 0.000 | 1.7e+02 | 1.8e+03 | 5.8e+04 | 38.0 / 38.0 | nsb_variability |
| B-cap-TL/alp_papp | 7.4e+02 | 4e+03 [4.5e+02-6.9e+04] | 0.000 | 1.1e+02 | 1.8e+03 | 1e+05 | 38.0 / 38.0 | electrode_sensitivity |
| B-cap-TL/hrp_tmb | 7.3e+02 | 4.3e+03 [4.7e+02-7.5e+04] | 0.000 | 86 | 1.7e+03 | 1e+05 | 38.0 / 38.0 | electrode_sensitivity |
| A-bed-TL/alp_hqdp | 9.3e+02 | 5.1e+03 [5.3e+02-inf] | 0.000 | 5.8e+02 | 5.7e+03 | 1e+05 | 29.5 / 29.5 | nsb_variability |
| C-planar-IDA/alp_papp | 4.7e+03 | 1.6e+04 [1.2e+03-inf] | 0.000 | 5.2e+02 | 1.1e+04 | 1e+05 | 38.0 / 38.0 | electrode_sensitivity |
| C-planar-IDA/alp_hqdp | 4.8e+03 | 1.6e+04 [9e+02-inf] | 0.000 | 5e+02 | 1.1e+04 | 1e+05 | 38.0 / 38.0 | nsb_variability |
| C-planar-IDA/hrp_tmb | 4.6e+03 | 1.9e+04 [1.1e+03-inf] | 0.000 | 5.1e+02 | 1.1e+04 | 1e+05 | 38.0 / 38.0 | electrode_sensitivity |
| B-mag-IDA/sa_polyhrp_tmb | 3.2e+03 | 2.3e+04 [9.8e+02-inf] | 0.000 | 3.7e+02 | 7.6e+03 | 1e+05 | 44.0 / 74.0 | electrode_sensitivity |
| B-mag1-IDA/sa_polyhrp_tmb | 3.9e+03 | 2.3e+04 [1.1e+03-inf] | 0.000 | 4.3e+02 | 9.4e+03 | 1e+05 | 26.0 / 56.0 | nsb_variability |
| B-mag-TL/sa_polyhrp_tmb | 3.2e+03 | 2.4e+04 [1.1e+03-inf] | 0.000 | 3.7e+02 | 7.6e+03 | 1e+05 | 44.0 / 74.0 | electrode_sensitivity |
| A-bed-COUL/alp_hqdp | 8.6e+03 | 2.9e+04 [2e+03-inf] | 0.000 | 8.6e+03 | 5.4e+04 | 1e+05 | 29.5 / 29.5 | substrate_background |
| C-bed-IDA/sbg_papg | 3.5e+03 | 3.1e+04 [2.1e+03-inf] | 0.000 | 1.9e+03 | 7e+03 | 1e+05 | 47.0 / 47.0 | electrode_sensitivity |
| C-bed-IDA/sa_polyhrp_tmb | 7.7e+03 | 4.5e+04 [2.2e+03-inf] | 0.000 | 8.4e+02 | 1.8e+04 | 1e+05 | 47.0 / 47.0 | nsb_variability |
| B-mag1-IDA/sbg_papg | 8.7e+03 | 4.8e+04 [3e+03-inf] | 0.000 | 1e+03 | 2.1e+04 | 1e+05 | 26.0 / 56.0 | electrode_sensitivity |
| A-bed-TL/hrp_tmb | 8.8e+03 | 4.9e+04 [3.8e+03-inf] | 0.000 | 8.2e+03 | 2.6e+04 | 1e+05 | 29.5 / 29.5 | electrode_sensitivity |
| B-bed-IDA/sbg_papg | 1e+04 | 6.3e+04 [4.4e+03-inf] | 0.000 | 5e+03 | 2.2e+04 | 1e+05 | 47.0 / 47.0 | electrode_sensitivity |
| B-bed-TL/sbg_papg | 1e+04 | 6.4e+04 [5e+03-inf] | 0.000 | 5.3e+03 | 2.2e+04 | 1e+05 | 47.0 / 47.0 | electrode_sensitivity |
| B-bed-COUL/sbg_papg | 1e+04 | 6.4e+04 [4.7e+03-inf] | 0.000 | 5e+03 | 2.2e+04 | 1e+05 | 47.0 / 47.0 | electrode_sensitivity |
| B-bed-SPE/sa_polyhrp_tmb | 2.4e+04 | 7.4e+04 [5.1e+03-inf] | 0.000 | 2.6e+03 | 5.6e+04 | 1e+05 | 47.0 / 47.0 | nsb_variability |
| B-mag-IDA/sbg_papg | 1.1e+04 | 8e+04 [3.1e+03-inf] | 0.000 | 1e+04 | 4.8e+03 | 1e+05 | 44.0 / 74.0 | substrate_background |
| B-bed-WJ/sa_polyhrp_tmb | 2.4e+04 | 8.4e+04 [5.3e+03-inf] | 0.000 | 2.6e+03 | 5.6e+04 | 1e+05 | 47.0 / 47.0 | nsb_variability |
| B-bed-IDA/sa_polyhrp_tmb | 2.4e+04 | 8.6e+04 [5.4e+03-inf] | 0.000 | 2.6e+03 | 5.6e+04 | 1e+05 | 47.0 / 47.0 | nsb_variability |
| B-bed-COUL/sa_polyhrp_tmb | 2.4e+04 | 8.6e+04 [5.4e+03-inf] | 0.000 | 2.6e+03 | 5.6e+04 | 1e+05 | 47.0 / 47.0 | nsb_variability |
| B-bed-TL/sa_polyhrp_tmb | 2.4e+04 | 9.6e+04 [6e+03-inf] | 0.000 | 2.6e+03 | 5.6e+04 | 1e+05 | 47.0 / 47.0 | nsb_variability |
| B-mag-TL/sbg_papg | 1.3e+04 | 9.7e+04 [5.3e+03-inf] | 0.000 | 1.3e+04 | 4.8e+03 | 1e+05 | 44.0 / 74.0 | substrate_background |
| B-bed-SPE/sbg_papg | 2.8e+04 | 9.9e+04 [1e+04-inf] | 0.000 | 2.6e+04 | 2.2e+04 | 1e+05 | 47.0 / 47.0 | baseline_drift |
| A-bed-COUL/alp_aap | inf | inf [5.7e+04-inf] | 0.000 | inf | inf | 1e+05 | 29.5 / 29.5 | substrate_background |
| A-bed-COUL/sbg_papg | inf | inf [inf-inf] | 0.000 | inf | inf | 1e+05 | 38.0 / 38.0 | electrode_sensitivity |
| A-bed-COUL/alp_papp | inf | inf [inf-inf] | 0.000 | inf | inf | 1e+05 | 29.5 / 29.5 | electrode_sensitivity |
| A-bed-COUL/hrp_tmb | inf | inf [2.6e+04-inf] | 0.000 | inf | inf | 1e+05 | 29.5 / 29.5 | electrode_sensitivity |
| A-bed-COUL/sa_polyhrp_tmb | inf | inf [inf-inf] | 0.000 | inf | inf | 1e+05 | 38.0 / 38.0 | electrode_sensitivity |
| A-bed-TL/alp_aap | 4e+04 | inf [5.4e+03-inf] | 0.000 | 4e+04 | inf | 1e+05 | 29.5 / 29.5 | substrate_background |
| A-bed-TL/sbg_papg | inf | inf [inf-inf] | 0.000 | inf | inf | 1e+05 | 38.0 / 38.0 | electrode_sensitivity |
| A-bed-TL/alp_papp | 2.5e+04 | inf [8.2e+03-inf] | 0.000 | 2.4e+04 | 7.3e+04 | 1e+05 | 29.5 / 29.5 | electrode_sensitivity |
| A-bed-TL/sa_polyhrp_tmb | inf | inf [5.2e+04-inf] | 0.000 | inf | inf | 1e+05 | 38.0 / 38.0 | electrode_sensitivity |
| B-bed-WJ/sbg_papg | 4.3e+04 | inf [1.2e+04-inf] | 0.000 | 4.2e+04 | 2.2e+04 | 1e+05 | 47.0 / 47.0 | baseline_drift |
| B-mono-TL/alp_hqdp | 4.5e+04 | inf [1.2e+04-inf] | 0.000 | 4.2e+03 | inf | 1e+05 | 38.0 / 38.0 | nsb_variability |
| B-mono-TL/alp_aap | 4.8e+04 | inf [1.3e+04-inf] | 0.000 | 4.3e+03 | inf | 1e+05 | 38.0 / 38.0 | nsb_variability |
| B-mono-TL/sbg_papg | inf | inf [inf-inf] | 0.000 | 9.6e+04 | inf | 1e+05 | 47.0 / 47.0 | electrode_sensitivity |
| B-mono-TL/alp_papp | 5.7e+04 | inf [1.8e+04-inf] | 0.000 | 5.8e+03 | inf | 1e+05 | 38.0 / 38.0 | electrode_sensitivity |
| B-mono-TL/hrp_tmb | 5.2e+04 | inf [1.8e+04-inf] | 0.000 | 5.7e+03 | inf | 1e+05 | 38.0 / 38.0 | nsb_variability |
| B-mono-TL/sa_polyhrp_tmb | inf | inf [inf-inf] | 0.000 | inf | inf | 1e+05 | 47.0 / 47.0 | nsb_variability |
| B-cap-TL/sbg_papg | 5.1e+04 | inf [2.1e+04-inf] | 0.000 | 5.1e+04 | 2.3e+04 | 1e+05 | 47.0 / 47.0 | baseline_drift |
| B-cap-TL/sa_polyhrp_tmb | 2.1e+04 | inf [6.9e+03-inf] | 0.000 | 2.4e+03 | 5e+04 | 1e+05 | 47.0 / 47.0 | electrode_sensitivity |
| C-planar-IDA/sbg_papg | 7.3e+04 | inf [3.3e+04-inf] | 0.000 | 5.1e+04 | inf | 1e+05 | 47.0 / 47.0 | substrate_background |
| C-planar-IDA/sa_polyhrp_tmb | inf | inf [1.9e+04-inf] | 0.000 | 1.5e+04 | inf | 1e+05 | 47.0 / 47.0 | nsb_variability |


## 10. What the model indicates (not a design decision)

1. **No architecture reaches LOD ≤ 1 pg/mL with the current parameter values.** Best nominal LOD is
   17 pg/mL (one-step in-vial magnetic beads + flow IDA, ALP/HQDP); Monte Carlo median 80 pg/mL,
   5–95 % 5.6–4200 pg/mL, P(LOD ≤ 1) = 0.4 %. All other architectures have P ≈ 0.
2. **The blank is set by conjugate NSB, not by the electrochemistry.** In ~all architectures the
   `nsb_variability` term (or `electrode_sensitivity` acting on the same NSB-borne charge, for fouling
   products) carries > 95 % of the blank variance. Electrochemical noise and drift are 10³–10⁶ × smaller.
   Consequently the detection cell (thin-layer vs coulometric vs IDA vs wall-jet) barely changes the LOD of
   a given capture/labelling configuration (B-bed rows are within 2×) – a better cell only helps once the
   blank is fixed.
3. **What matters is analyte-equivalent blank B = (NSB area × exposure)/(captured, labelled analyte per
   concentration).** Ranking by capture geometry: renewed magnetic beads (small area) < chip bead bed <
   packed bed ≈ capillary (big area or poor capture) ≪ planar chip (0.2 % capture) ≪ monolith (0.12 m²
   area). The 10 µL packed bed captures 65 % of the delivered analyte but its 1.8×10⁻³ m² of surface
   gives B ≈ 2000 pg/mL. In the bead architectures the **0.1 m of PEEK tubing sealed with the trap is the
   dominant NSB surface** (more than the beads) – shortening it is a design lever.
4. **Labelling yield is low in flow (1.2 %)** because the 20 µL conjugate plug reaches the reactor at only
   12 % of its vial concentration and incubates 5 min. This cancels in B (NSB scales the same way) but
   makes Scheme A (no stop: 0.5 %) and the two-step SβG/polyHRP chemistries (product of two low yields;
   ≤ 1 enzyme per pg/mL) the worst options as configured. The one-step in-vial format wins by labelling
   28 % of captured analyte at full conjugate concentration for 30 min.
5. **Antibody off-rates are the largest parameter sensitivities** (one-at-a-time, best architecture):
   k_off,capture at its high bound (Kamat2020 fast commercial anti-Fc mAb) raises the LOD 2000×, k_off,detection
   700×; then k_nsb (±1 log), tubing surface factor, antibody density, k_on,d, label NSB factor, CV_NSB.
   Reagent screening for k_off (Task 1's t½ > 1 h criterion) is decisive.
6. If NSB is as low as a commercial plate ELISA implies (scenario 6.3(2)), the best architecture reaches
   **1.9 pg/mL** nominal, and the ALP/HQDP bead and chip-bed variants reach 8–30 pg/mL – still above 1 pg/mL
   without further design changes (longer/larger conjugate exposure, shorter tubing, more beads/longer
   in-vial capture, lower CV_NSB).
7. Time: Scheme B baseline 38 min; bead architectures 26–35 min instrument time, 56–65 min to result
   including the 30 min in-vial incubation (sequential-bead variants exceed 60 min to result;
   one-step is 56 min). Two-step labels add 9 min. Range: ALP calibrations bend above ~2×10³ pg/mL (Pi
   inhibition; 2 Pi per HQ from HQDP), HRP above 3×10⁴ – all cover 1000 pg/mL at the top. Carry-over after
   the 1000 pg/mL standard: ≈ 0.1 pg/mL for beads (trap-wall residual), negligible for acid-regenerated
   ALP surfaces (ALP inactivated). Reuse: renewed beads have no capacity drift; a reused electrode with pAP
   or TMB(ox) products would drift 10 % in ~10 cycles at the assumed 1 %/cycle fouling (HQ: ~100 cycles).

## 11. Known weaknesses

* **NSB sub-model is the weakest and the most important link**: linear in exposure, one rate constant from one
  digital-ELISA dataset, UNVERIFIED surface factors; it disagrees 9–35× with the conventional-ELISA blank.
  All absolute LODs inherit this uncertainty; relative rankings (area × exposure / capture) are more robust.
  First bench measurement to make: blank signal vs conjugate exposure on the chosen surface.
* Substrate impurity/hydrolysis rates are unknown for every substrate (4-decade bounds) – they decide Scheme A
  and the SβG/pAPG route, but not the current leaders.
* Antibody rate constants are generic (no anti-human-IgG k_on), sampled independently; rebinding not credited.
* Beads in an unstirred SM-FL vial (settling, aspiration of a settling suspension, trap efficiency) are
  modelled by three UNVERIFIED factors; bead injection through the SM-FL is itself unverified (Task 2).
* Plug-flow assumptions for the packed bed; non-porous beads (porous media would add NSB area);
  monolith as straight channels.
* Electrochemical noise values are Task 2 estimates; noise is white + linear drift; no capacitive transients
  (avoided in Scheme B by constant ionic strength), no bubbles, no fouling dynamics within a run.
* The IDA amplification in flow is an empirical factor; Aoki's formula assumes semi-infinite solution above
  the IDA (in a 25 µm channel it is approximate).
* Loop model: straight tube, plug position assumed; conjugate peak stop time assumed ideal.
* Temperature effects (no thermostat) and enzyme activity loss over the run are not modelled.
* LOD uses blank SD only (brief's definition); signal-side variance (capture, adsorption, injection) is not
  in the LOD but would widen calibration uncertainty.
* Wilson–Geankoplis, wall-jet and Aoki coefficients were recalled from the literature, not re-verified in
  this session.

## 12. References added by this task

(Not re-verified online in this session; listed so that keys resolve.)
Aoki K, Morita M, Niwa O, Tabei H. J Electroanal Chem 1988;256:269–282 (IDA steady-state currents).
Wilson EJ, Geankoplis CJ. Ind Eng Chem Fundam 1966;5:9–14 (packed-bed liquid mass transfer).
Yamada J, Matsuda H. J Electroanal Chem 1973;44:189 (wall-jet electrode); Albery WJ, Brett CMA. J
Electroanal Chem 1983;148:201.
Shah RK, London AL. Laminar Flow Forced Convection in Ducts, Academic Press 1978 (Graetz series).
Compton RG, Unwin PR. J Electroanal Chem 1986;205:1 (Levich channel-electrode equation).
All other keys: docs/01 and docs/02 reference lists.
