# Three-tier round: model results (scripts/tier_round/run_tiers.py)

## 1. The three implementations, as specified

Monte Carlo n = 2000, seed 20261111. Tier 3 carries the immune-complex transfer at the bounded, UNVERIFIED magnitudes of ma.design_levers (non-specific label x0.1 [0.01-0.5], specific x0.7 [0.4-0.9]), sampled.

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | ULOQ nominal | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| Tier 1: thin-film gold electrode, capture on the electrode, read under 1 uL/min substrate flow | 3.1 | 16 [2.1-1.6e+02] | 0.01 | 0.37 | 1e+05 | baseline_drift / nsb_variability (0.38) | 53.0 |
| Tier 2: capillary micro-bed above a printed carbon electrode, stopped accumulation, swept read | 0.75 | 3 [0.51-45] | 0.18 | 0.78 | 54 | nsb_variability / nsb_variability (0.74) | 58.0 |
| Tier 3: tier 2 bed behind valves + immune-complex transfer to a second bed | 0.33 | 1.4 [0.28-43] | 0.38 | 0.84 | 93 | substrate_background / substrate_background (0.35) | 58.0 |

## 2. Scenarios - Tier 1: thin-film gold electrode, capture on the electrode, read under 1 uL/min substrate flow

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | ULOQ nominal | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| as specified | 3.1 | 16 [2.1-1.6e+02] | 0.01 | 0.37 | 1e+05 | baseline_drift / nsb_variability (0.38) | 53.0 |
| detection reagent and substrate lot pass screening (L6 + L7) | 2.1 | 10 [1.6-74] | 0.01 | 0.50 | 1e+05 | baseline_drift / baseline_drift (0.44) | 53.0 |
| F(ab')2 conjugate (L3) | 2.8 | 13 [1.7-1.4e+02] | 0.02 | 0.43 | 1e+05 | baseline_drift / baseline_drift (0.46) | 53.0 |
| L3 + L6 + L7 | 1.9 | 7.9 [1.3-64] | 0.03 | 0.57 | 1e+05 | baseline_drift / baseline_drift (0.55) | 53.0 |
| non-specific binding x25 (S1) | 39 | 1.3e+02 [15-1.3e+03] | 0.00 | 0.02 | 1e+05 | nsb_variability / nsb_variability (0.92) | 53.0 |
| free hydroquinone 1e-3 in the substrate (S4a) | 49 | 94 [11-9e+02] | 0.00 | 0.04 | 1e+05 | substrate_background / substrate_background (0.95) | 53.0 |
| blank contamination up to 1 pg/mL (C1) | 3.1 | 16 [2.5-1.6e+02] | 0.00 | 0.37 | 1e+05 | baseline_drift / nsb_variability (0.36) | 53.0 |

## 2. Scenarios - Tier 2: capillary micro-bed above a printed carbon electrode, stopped accumulation, swept read

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | ULOQ nominal | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| as specified | 0.75 | 3 [0.51-45] | 0.18 | 0.78 | 54 | nsb_variability / nsb_variability (0.74) | 58.0 |
| detection reagent and substrate lot pass screening (L6 + L7) | 0.48 | 1.7 [0.4-16] | 0.31 | 0.90 | 32 | nsb_variability / nsb_variability (0.81) | 58.0 |
| F(ab')2 conjugate (L3) | 0.39 | 1.8 [0.37-26] | 0.28 | 0.87 | 54 | nsb_variability / nsb_variability (0.59) | 58.0 |
| L3 + L6 + L7 | 0.24 | 1 [0.26-8] | 0.48 | 0.96 | 32 | nsb_variability / nsb_variability (0.66) | 58.0 |
| non-specific binding x25 (S1) | 25 | 71 [6.7-1.3e+03] | 0.00 | 0.09 | 93 | nsb_variability / nsb_variability (0.99) | 58.0 |
| free hydroquinone 1e-3 in the substrate (S4a) | 11 | 22 [2.6-2.7e+02] | 0.00 | 0.29 | 54 | substrate_background / substrate_background (0.90) | 58.0 |
| blank contamination up to 1 pg/mL (C1) | 0.75 | 3.3 [0.71-45] | 0.10 | 0.78 | 54 | nsb_variability / nsb_variability (0.63) | 58.0 |

## 2. Scenarios - Tier 3: tier 2 bed behind valves + immune-complex transfer to a second bed

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | ULOQ nominal | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| as specified | 0.33 | 1.4 [0.28-43] | 0.38 | 0.84 | 93 | substrate_background / substrate_background (0.35) | 58.0 |
| with a reference channel as well (L5) | 0.32 | 1.3 [0.27-42] | 0.39 | 0.84 | 93 | substrate_background / substrate_background (0.36) | 58.0 |
| detection reagent and substrate lot pass screening (L6 + L7) | 0.11 | 0.74 [0.18-3] | 0.67 | 0.99 | 54 | nsb_variability / contamination (0.51) | 58.0 |
| F(ab')2 conjugate (L3) | 0.29 | 1.2 [0.25-40] | 0.43 | 0.86 | 93 | substrate_background / substrate_background (0.39) | 58.0 |
| L3 + L6 + L7 | 0.092 | 0.64 [0.15-1.9] | 0.76 | 1.00 | 54 | baseline_drift / contamination (0.60) | 58.0 |
| non-specific binding x25 (S1) | 4.5 | 12 [0.97-4.1e+02] | 0.05 | 0.47 | 93 | nsb_variability / nsb_variability (0.87) | 58.0 |
| free hydroquinone 1e-3 in the substrate (S4a) | 24 | 41 [3.8-1.1e+03] | 0.00 | 0.17 | 93 | substrate_background / substrate_background (0.99) | 58.0 |
| blank contamination up to 1 pg/mL (C1) | 0.33 | 2 [0.41-43] | 0.22 | 0.84 | 93 | substrate_background / contamination (0.40) | 58.0 |
| transfer does not work (same timing, no transfer) | 1.2 | 4.4 [0.62-1.2e+02] | 0.12 | 0.69 | 93 | nsb_variability / nsb_variability (0.77) | 58.0 |

## 3. Tier 1 - alternatives and hardware scenarios

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | ULOQ nominal | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| primary (gap 0.16 mm) | 3.1 | 16 [2.1-1.6e+02] | 0.01 | 0.37 | 1e+05 | baseline_drift / nsb_variability (0.38) | 53.0 |
| gap 0.10 mm | 2.7 | 15 [2-1.5e+02] | 0.01 | 0.38 | 1e+05 | baseline_drift / nsb_variability (0.37) | 53.0 |
| gap 0.30 mm | 4 | 18 [2.5-1.7e+02] | 0.00 | 0.33 | 1e+05 | baseline_drift / baseline_drift (0.42) | 53.0 |
| pump minimum is 10 uL/min: read at 10 uL/min | 3.4 | 19 [2.3-2.3e+02] | 0.01 | 0.33 | 1e+05 | baseline_drift / substrate_background (0.37) | 53.0 |
| flow can be stopped: stopped read, 30 s wait + 120 s | 7.9 | 30 [4.1-2.6e+02] | 0.00 | 0.20 | 1e+05 | nsb_variability / nsb_variability (0.90) | 50.5 |
| 1 mM substrate instead of 0.3 mM | 3.3 | 18 [2.4-2.5e+02] | 0.01 | 0.32 | 1e+05 | baseline_drift / substrate_background (0.40) | 53.0 |
| no pre-read on the electrode | 5.2 | 26 [3-4.7e+02] | 0.00 | 0.26 | 1e+05 | electrode_sensitivity / nsb_variability (0.26) | 53.0 |
| conjugate 3 nM for 5 min + 3 min stop, load 36 min | 4.3 | 20 [2.4-3.3e+02] | 0.01 | 0.32 | 1e+05 | baseline_drift / nsb_variability (0.40) | 56.0 |
| printed gold strip (AU10) in the SPE cell, same chemistry | 5.3 | 15 [2.4-1.3e+02] | 0.01 | 0.36 | 1e+05 | baseline_drift / nsb_variability (0.65) | 53.0 |
| printed carbon strip (C21), adsorbed streptavidin | 9.4 | 25 [3.6-2.5e+02] | 0.00 | 0.23 | 1e+05 | nsb_variability / nsb_variability (0.79) | 53.0 |
| printed carbon strip, SPE cell gap 0.10 mm | 6.6 | 19 [2.7-2e+02] | 0.01 | 0.30 | 1e+05 | nsb_variability / nsb_variability (0.79) | 53.0 |
| printed carbon strip, SPE cell gap 0.50 mm | 16 | 37 [5.4-3.7e+02] | 0.00 | 0.14 | 1e+05 | nsb_variability / nsb_variability (0.79) | 53.0 |
| thin-film gold, chemical redox cycling in the stopped cell (UNVERIFIED on gold) | 11 | 64 [6.9-8.8e+02] | 0.00 | 0.09 | 1e+05 | nsb_variability / nsb_variability (0.54) | 53.0 |

## 4. Tier 2 - alternatives and hardware scenarios

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | ULOQ nominal | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| primary (SPE cell gap 0.20 mm) | 0.75 | 3 [0.51-45] | 0.18 | 0.78 | 54 | nsb_variability / nsb_variability (0.74) | 58.0 |
| SPE cell gap 0.10 mm | 0.75 | 3 [0.5-45] | 0.18 | 0.78 | 54 | nsb_variability / nsb_variability (0.74) | 58.0 |
| SPE cell gap 0.50 mm | 0.76 | 3 [0.53-45] | 0.17 | 0.78 | 54 | nsb_variability / nsb_variability (0.73) | 58.0 |
| flow cannot be stopped: continuous read at 1 uL/min | 1.6 | 6.1 [1-68] | 0.05 | 0.64 | 1e+05 | nsb_variability / nsb_variability (0.78) | 58.5 |
| flow cannot be stopped and pump minimum is 10 uL/min | 3.2 | 15 [1.9-2.2e+02] | 0.01 | 0.38 | 1e+05 | nsb_variability / nsb_variability (0.56) | 58.5 |
| half the beads (5e5) | 0.9 | 3.9 [0.57-68] | 0.14 | 0.72 | 54 | nsb_variability / nsb_variability (0.73) | 58.0 |
| twice the beads (2e6) | 0.85 | 3 [0.53-39] | 0.16 | 0.79 | 32 | nsb_variability / nsb_variability (0.78) | 58.0 |
| bed in a fitting on the inlet port (bore wall in the path) | 0.72 | 3.3 [0.57-39] | 0.14 | 0.78 | 7.9e+02 | nsb_variability / nsb_variability (0.78) | 58.0 |
| 20 um polystyrene streptavidin beads, 0.15 uL, on the port, 5 mm2 retainer | 1.7 | 7 [0.97-80] | 0.05 | 0.60 | 7.9e+02 | nsb_variability / nsb_variability (0.90) | 58.0 |
| retainer (frit or screen) wetted area 1 mm2 instead of 5 mm2 | 0.36 | 1.8 [0.38-23] | 0.28 | 0.88 | 54 | nsb_variability / nsb_variability (0.61) | 58.0 |
| retainer wetted area 20 mm2 (0.5 mm silicate frit) | 2.3 | 7.2 [0.84-1.4e+02] | 0.07 | 0.57 | 54 | nsb_variability / nsb_variability (0.87) | 58.0 |
| conjugate 10 nM for 2 min | 0.67 | 2.8 [0.5-34] | 0.19 | 0.81 | 32 | nsb_variability / nsb_variability (0.76) | 55.0 |
| short accumulation of 30 s (range read) | 1.8 | 7.2 [0.96-1.4e+02] | 0.06 | 0.58 | 4.6e+02 | substrate_background / substrate_background (0.42) | 51.5 |
| parked read instead of swept | 1.3 | 4.9 [0.76-69] | 0.09 | 0.68 | 54 | nsb_variability / nsb_variability (0.89) | 58.5 |
| thin-film gold cell as detector | 0.75 | 3 [0.51-45] | 0.17 | 0.78 | 54 | nsb_variability / nsb_variability (0.73) | 58.0 |
| accumulation 15 min, load 28 min | 0.84 | 3.3 [0.52-52] | 0.16 | 0.76 | 32 | nsb_variability / nsb_variability (0.81) | 58.0 |

## 5. Tier 3 - alternatives

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | ULOQ nominal | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| primary (with transfer) | 0.33 | 1.4 [0.28-43] | 0.38 | 0.84 | 93 | substrate_background / substrate_background (0.35) | 58.0 |
| transfer + F(ab')2 conjugate + screened reagents (L3 + L6 + L7) | 0.092 | 0.64 [0.15-1.9] | 0.76 | 1.00 | 54 | baseline_drift / contamination (0.60) | 58.0 |
| the same with a reference channel (L5) | 0.09 | 0.63 [0.15-1.8] | 0.77 | 1.00 | 54 | baseline_drift / contamination (0.61) | 58.0 |
| valves only: tier 2 chemistry with an isolated bed (no transfer) | 0.71 | 2.9 [0.5-40] | 0.18 | 0.79 | 54 | nsb_variability / nsb_variability (0.73) | 57.0 |
| transfer at its pessimistic bounds (non-specific x0.5, specific x0.4) | 1.6 | 6.5 [0.83-1.8e+02] | 0.07 | 0.61 | 1.6e+02 | nsb_variability / nsb_variability (0.71) | 58.0 |
| transfer at its optimistic bounds (non-specific x0.01, specific x0.9) | 0.22 | 0.91 [0.18-31] | 0.54 | 0.90 | 93 | substrate_background / contamination (0.43) | 58.0 |
| accumulation 12 min instead of 7 (bed isolated by the valve), load 24 min | 0.26 | 1.3 [0.26-36] | 0.41 | 0.86 | 54 | nsb_variability / nsb_variability (0.36) | 58.0 |

## 6. One-at-a-time sensitivity of the three implementations

LOD (pg/mL) with one parameter at its low and at its high bound, all others at their best estimate; the eight largest swings.


**Tier 1: thin-film gold electrode, capture on the electrode, read under 1 uL/min substrate flow** (nominal 3.1 pg/mL)

| Parameter | value [low-high] | LOD at low | LOD at high |
|---|---|---|---|
| `chem.antibodies.koff_detection` | 0.00086 [3e-06-0.0083] 1/s | 2 | 1.3e+02 |
| `chem.enzymes.alp.kcat_conjugate_assay_conditions` | 1000 [100-6000] 1/s | 27 | 1.6 |
| `ma.chemistries.alp_hqdp.free_product_impurity` | 1e-05 [1e-07-0.001] mol/mol | 3.1 | 49 |
| `ma.chemistries.alp_hqdp.hydrolysis_rate` | 1e-10 [1e-12-1e-08] 1/s | 3.1 | 42 |
| `chem.antibodies.kon_detection` | 390000 [90000-1.2e+06] 1/(M*s) | 11 | 1.5 |
| `tr.noise.drift_area_exponent` | 1 [0-1] dimensionless | 23 | 3.1 |
| `chem.nsb.nsb_effective_rate_constant` | 4e-11 [8e-12-4e-10] m/s | 2.7 | 16 |
| `tr.nsb.surface_factor_gold_oeg` | 3 [0.5-30] fold | 2.7 | 14 |

**Tier 2: capillary micro-bed above a printed carbon electrode, stopped accumulation, swept read** (nominal 0.75 pg/mL)

| Parameter | value [low-high] | LOD at low | LOD at high |
|---|---|---|---|
| `chem.antibodies.koff_detection` | 0.00086 [3e-06-0.0083] 1/s | 0.46 | 48 |
| `chem.nsb.nsb_effective_rate_constant` | 4e-11 [8e-12-4e-10] m/s | 0.19 | 8.6 |
| `tr.nsb.surface_factor_frit` | 10 [1-100] fold | 0.31 | 5.8 |
| `ma.chemistries.alp_hqdp.free_product_impurity` | 1e-05 [1e-07-0.001] mol/mol | 0.75 | 11 |
| `ma.nsb.label_factor_igg_enzyme_conjugate` | 0.04 [0.01-0.15] fold | 0.22 | 3 |
| `chem.antibodies.kon_detection` | 390000 [90000-1.2e+06] 1/(M*s) | 2.9 | 0.33 |
| `chem.surfaces.igg_surface_density_monolayer` | 1e+16 [2e+15-1.5e+16] molecules/m^2 | 2.1 | 0.67 |
| `ma.labelling.detection_on_capture_residual_factor` | 1 [1-3] fold | 0.75 | 2.3 |

**Tier 3: tier 2 bed behind valves + immune-complex transfer to a second bed** (nominal 0.33 pg/mL)

| Parameter | value [low-high] | LOD at low | LOD at high |
|---|---|---|---|
| `chem.antibodies.koff_detection` | 0.00086 [3e-06-0.0083] 1/s | 0.14 | 4.8e+02 |
| `ma.chemistries.alp_hqdp.free_product_impurity` | 1e-05 [1e-07-0.001] mol/mol | 0.25 | 24 |
| `chem.enzymes.alp.kcat_conjugate_assay_conditions` | 1000 [100-6000] 1/s | 2.8 | 0.18 |
| `chem.antibodies.kon_detection` | 390000 [90000-1.2e+06] 1/(M*s) | 1.3 | 0.15 |
| `chem.nsb.nsb_effective_rate_constant` | 4e-11 [8e-12-4e-10] m/s | 0.28 | 1.7 |
| `ma.noise.background_current_relative_noise` | 0.01 [0.002-0.05] fraction | 0.25 | 1.1 |
| `tr.nsb.surface_factor_frit` | 10 [1-100] fold | 0.29 | 1.2 |
| `ma.nsb.blank_igg_contamination_equivalent` | 0 [0-3e-15] M | 0.33 | 1.4 |

## 7. Step tables used for the timing


**Tier 1: thin-film gold electrode, capture on the electrode, read under 1 uL/min substrate flow** - 53.0 min from Inject Start to result

| Step | min | counts |
|---|---|---|
| pre-run: buffer flush, substrate fill, background read on the fresh electrode, buffer flush | 8.0 | no (before injection) |
| sample injection (SM-FL aspirate and load) | 1.0 | yes |
| sample pumped through the cell | 39.0 | yes |
| wash 1 | 1.5 | yes |
| conjugate injection (SM-FL) | 1.0 | yes |
| conjugate pumped into the cell | 2.0 | yes |
| conjugate stopped in the cell | 0.0 | yes |
| wash 2 | 2.0 | yes |
| substrate fill (BSM A1 -> B1) | 1.5 | yes |
| flow stopped, electrode settles, impurity electrolysed | 1.0 | yes |
| read window | 4.0 | yes |

**Tier 2: capillary micro-bed above a printed carbon electrode, stopped accumulation, swept read** - 58.0 min from Inject Start to result

| Step | min | counts |
|---|---|---|
| pre-run: buffer flush, substrate background peak on the fresh electrode, buffer flush | 8.0 | no (before injection) |
| sample injection (SM-FL aspirate and load) | 1.0 | yes |
| sample pumped through the bed | 36.0 | yes |
| wash 1 | 1.5 | yes |
| conjugate injection (SM-FL) | 1.0 | yes |
| conjugate pumped through the bed | 5.0 | yes |
| conjugate stopped in the bed | 0.0 | yes |
| wash 2 | 3.0 | yes |
| substrate fill (BSM A1 -> B1) | 2.0 | yes |
| flow stopped: product accumulates in the bed | 7.0 | yes |
| sweep through the cell and read | 1.5 | yes |

**Tier 3: tier 2 bed behind valves + immune-complex transfer to a second bed** - 58.0 min from Inject Start to result

| Step | min | counts |
|---|---|---|
| pre-run: buffer flush, substrate background peak on the fresh electrode, buffer flush | 8.0 | no (before injection) |
| sample injection (SM-FL aspirate and load) | 1.0 | yes |
| sample pumped through the bed | 29.0 | yes |
| wash 1 | 1.5 | yes |
| conjugate injection (SM-FL) | 1.0 | yes |
| conjugate pumped through the bed | 5.0 | yes |
| conjugate stopped in the bed | 0.0 | yes |
| wash 2 | 2.0 | yes |
| elution from the capture bed, re-capture on the read bed, wash (tier 3) | 8.0 | yes |
| substrate fill (BSM A1 -> B1) | 2.0 | yes |
| flow stopped: product accumulates in the bed | 7.0 | yes |
| sweep through the cell and read | 1.5 | yes |
