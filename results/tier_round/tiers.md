# Three-tier round: model results (scripts/tier_round/run_tiers.py)

## 1. The three implementations, as specified

Monte Carlo n = 2000, seed 20261111. Tier 3 carries the transfer lever L4 (UNVERIFIED magnitude, ma.design_levers) in every row.

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | ULOQ nominal | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| Tier 1: thin-film gold electrode, capture on the electrode, read under 1 uL/min substrate flow | 4.3 | 20 [2.4-3.3e+02] | 0.01 | 0.32 | 1e+05 | baseline_drift / nsb_variability (0.40) | 56.0 |
| Tier 2: capillary micro-bed above a printed carbon electrode, stopped accumulation, swept read | 0.36 | 1.8 [0.38-22] | 0.28 | 0.88 | 54 | nsb_variability / nsb_variability (0.61) | 58.0 |
| Tier 3: tier 2 bed behind valves + immune-complex transfer to a second bed (L4) | 0.21 | 1.1 [0.23-34] | 0.47 | 0.89 | 54 | substrate_background / contamination (0.35) | 58.0 |

## 2. Scenarios - Tier 1: thin-film gold electrode, capture on the electrode, read under 1 uL/min substrate flow

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | ULOQ nominal | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| as specified | 4.3 | 20 [2.4-3.3e+02] | 0.01 | 0.32 | 1e+05 | baseline_drift / nsb_variability (0.40) | 56.0 |
| detection reagent and substrate lot pass screening (L6 + L7) | 2.2 | 11 [1.7-79] | 0.01 | 0.48 | 1e+05 | baseline_drift / nsb_variability (0.44) | 56.0 |
| F(ab')2 conjugate (L3) | 3.7 | 15 [1.9-2.8e+02] | 0.01 | 0.38 | 1e+05 | baseline_drift / baseline_drift (0.45) | 56.0 |
| L3 + L6 + L7 | 1.9 | 8.2 [1.3-65] | 0.03 | 0.56 | 1e+05 | baseline_drift / baseline_drift (0.52) | 56.0 |
| non-specific binding x25 (S1) | 59 | 1.7e+02 [18-2.6e+03] | 0.00 | 0.02 | 1e+05 | nsb_variability / nsb_variability (0.93) | 56.0 |
| free hydroquinone 1e-3 in the substrate (S4a) | 63 | 1.1e+02 [12-1.7e+03] | 0.00 | 0.03 | 1e+05 | substrate_background / substrate_background (0.95) | 56.0 |
| blank contamination up to 1 pg/mL (C1) | 4.3 | 20 [2.7-3.3e+02] | 0.00 | 0.32 | 1e+05 | baseline_drift / nsb_variability (0.39) | 56.0 |

## 2. Scenarios - Tier 2: capillary micro-bed above a printed carbon electrode, stopped accumulation, swept read

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | ULOQ nominal | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| as specified | 0.36 | 1.8 [0.38-22] | 0.28 | 0.88 | 54 | nsb_variability / nsb_variability (0.61) | 58.0 |
| detection reagent and substrate lot pass screening (L6 + L7) | 0.22 | 1.1 [0.3-7.1] | 0.46 | 0.97 | 32 | nsb_variability / nsb_variability (0.69) | 58.0 |
| F(ab')2 conjugate (L3) | 0.21 | 1.2 [0.31-16] | 0.40 | 0.92 | 54 | nsb_variability / nsb_variability (0.45) | 58.0 |
| L3 + L6 + L7 | 0.12 | 0.79 [0.2-3.5] | 0.65 | 1.00 | 32 | nsb_variability / nsb_variability (0.50) | 58.0 |
| non-specific binding x25 (S1) | 10 | 35 [3.9-4.6e+02] | 0.00 | 0.19 | 93 | nsb_variability / nsb_variability (0.98) | 58.0 |
| free hydroquinone 1e-3 in the substrate (S4a) | 10 | 19 [2.2-2.5e+02] | 0.01 | 0.32 | 54 | substrate_background / substrate_background (0.95) | 58.0 |
| blank contamination up to 1 pg/mL (C1) | 0.36 | 2.3 [0.56-22] | 0.16 | 0.88 | 54 | nsb_variability / nsb_variability (0.49) | 58.0 |

## 2. Scenarios - Tier 3: tier 2 bed behind valves + immune-complex transfer to a second bed (L4)

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | ULOQ nominal | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| as specified | 0.21 | 1.1 [0.23-34] | 0.47 | 0.89 | 54 | substrate_background / contamination (0.35) | 58.0 |
| with a reference channel as well (L5) | 0.21 | 1 [0.22-33] | 0.49 | 0.90 | 54 | substrate_background / contamination (0.37) | 58.0 |
| detection reagent and substrate lot pass screening (L6 + L7) | 0.069 | 0.6 [0.14-1.5] | 0.81 | 1.00 | 32 | baseline_drift / contamination (0.63) | 58.0 |
| F(ab')2 conjugate (L3) | 0.2 | 0.95 [0.2-29] | 0.53 | 0.90 | 54 | substrate_background / contamination (0.41) | 58.0 |
| L3 + L6 + L7 | 0.061 | 0.54 [0.12-1.2] | 0.87 | 1.00 | 32 | baseline_drift / contamination (0.72) | 58.0 |
| non-specific binding x25 (S1) | 17 | 51 [5.3-1.3e+03] | 0.00 | 0.14 | 1.6e+02 | nsb_variability / nsb_variability (0.98) | 58.0 |
| free hydroquinone 1e-3 in the substrate (S4a) | 17 | 26 [2.4-7e+02] | 0.01 | 0.27 | 54 | substrate_background / substrate_background (1.00) | 58.0 |
| blank contamination up to 1 pg/mL (C1) | 0.21 | 1.7 [0.33-34] | 0.27 | 0.89 | 54 | substrate_background / contamination (0.51) | 58.0 |
| transfer does not work (no L4) | 0.59 | 2.5 [0.44-66] | 0.21 | 0.79 | 54 | nsb_variability / nsb_variability (0.65) | 58.0 |

## 3. Tier 1 - alternatives and hardware scenarios

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | ULOQ nominal | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| primary (gap 0.16 mm) | 4.3 | 20 [2.4-3.3e+02] | 0.01 | 0.32 | 1e+05 | baseline_drift / nsb_variability (0.40) | 56.0 |
| gap 0.10 mm | 3.7 | 19 [2.3-3.1e+02] | 0.01 | 0.33 | 1e+05 | baseline_drift / nsb_variability (0.40) | 56.0 |
| gap 0.30 mm | 5.5 | 22 [2.8-3.3e+02] | 0.00 | 0.28 | 1e+05 | baseline_drift / nsb_variability (0.41) | 56.0 |
| pump minimum is 10 uL/min: read at 10 uL/min | 4.5 | 23 [2.6-4.5e+02] | 0.01 | 0.28 | 1e+05 | baseline_drift / substrate_background (0.36) | 56.0 |
| flow can be stopped: stopped read, 30 s wait + 120 s | 12 | 39 [4.9-5.3e+02] | 0.00 | 0.15 | 1e+05 | nsb_variability / nsb_variability (0.91) | 53.5 |
| 1 mM substrate instead of 0.3 mM | 4.5 | 23 [2.6-4.7e+02] | 0.01 | 0.27 | 1e+05 | baseline_drift / substrate_background (0.39) | 56.0 |
| no pre-read on the electrode | 7 | 32 [3.4-7.4e+02] | 0.00 | 0.22 | 1e+05 | electrode_sensitivity / nsb_variability (0.28) | 56.0 |
| conjugate 10 nM for 2 min, no stop | 3.1 | 16 [2.1-1.6e+02] | 0.01 | 0.37 | 1e+05 | baseline_drift / nsb_variability (0.38) | 53.0 |
| printed gold strip (AU10) in the SPE cell, same chemistry | 7.3 | 19 [2.6-2.6e+02] | 0.01 | 0.30 | 1e+05 | baseline_drift / nsb_variability (0.68) | 56.0 |
| printed carbon strip (C21), adsorbed streptavidin | 14 | 33 [4.1-4.9e+02] | 0.00 | 0.18 | 1e+05 | nsb_variability / nsb_variability (0.81) | 56.0 |
| printed carbon strip, SPE cell gap 0.10 mm | 9.7 | 25 [3.1-3.7e+02] | 0.00 | 0.25 | 1e+05 | nsb_variability / nsb_variability (0.81) | 56.0 |
| printed carbon strip, SPE cell gap 0.50 mm | 23 | 50 [6.2-7.6e+02] | 0.00 | 0.11 | 1e+05 | nsb_variability / nsb_variability (0.81) | 56.0 |
| thin-film gold, chemical redox cycling in the stopped cell (UNVERIFIED on gold) | 16 | 82 [7.8-1.5e+03] | 0.00 | 0.07 | 1e+05 | nsb_variability / nsb_variability (0.57) | 56.0 |

## 4. Tier 2 - alternatives and hardware scenarios

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | ULOQ nominal | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| primary (SPE cell gap 0.20 mm) | 0.36 | 1.8 [0.38-22] | 0.28 | 0.88 | 54 | nsb_variability / nsb_variability (0.61) | 58.0 |
| SPE cell gap 0.10 mm | 0.36 | 1.8 [0.38-22] | 0.28 | 0.88 | 54 | nsb_variability / nsb_variability (0.61) | 58.0 |
| SPE cell gap 0.50 mm | 0.38 | 1.8 [0.4-23] | 0.27 | 0.88 | 54 | nsb_variability / nsb_variability (0.59) | 58.0 |
| flow cannot be stopped: continuous read at 1 uL/min | 1.3 | 4.7 [0.88-52] | 0.07 | 0.70 | 1e+05 | nsb_variability / nsb_variability (0.72) | 58.5 |
| flow cannot be stopped and pump minimum is 10 uL/min | 2.9 | 13 [1.8-2e+02] | 0.01 | 0.41 | 1e+05 | nsb_variability / nsb_variability (0.51) | 58.5 |
| half the beads (5e5) | 0.35 | 2 [0.4-31] | 0.26 | 0.85 | 54 | nsb_variability / nsb_variability (0.55) | 58.0 |
| twice the beads (2e6) | 0.51 | 2 [0.43-23] | 0.24 | 0.87 | 32 | nsb_variability / nsb_variability (0.69) | 58.0 |
| bed in a fitting on the inlet port (bore wall in the path) | 0.72 | 3.3 [0.57-39] | 0.14 | 0.78 | 7.9e+02 | nsb_variability / nsb_variability (0.78) | 58.0 |
| 20 um polystyrene streptavidin beads, 0.15 uL, on the port, 5 mm2 retainer | 1.7 | 7 [0.97-80] | 0.05 | 0.60 | 7.9e+02 | nsb_variability / nsb_variability (0.90) | 58.0 |
| retainer (frit) area 10 mm2 instead of 1 mm2 | 1.3 | 4.4 [0.65-73] | 0.12 | 0.70 | 54 | nsb_variability / nsb_variability (0.81) | 58.0 |
| parked read instead of swept | 0.89 | 3.5 [0.61-41] | 0.13 | 0.77 | 54 | nsb_variability / nsb_variability (0.83) | 58.5 |
| thin-film gold cell as detector | 0.36 | 1.8 [0.38-23] | 0.28 | 0.88 | 54 | nsb_variability / nsb_variability (0.60) | 58.0 |
| accumulation 15 min, load 28 min | 0.38 | 1.8 [0.38-24] | 0.27 | 0.87 | 18 | nsb_variability / nsb_variability (0.68) | 58.0 |

## 5. Tier 3 - alternatives

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | ULOQ nominal | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| primary (transfer, L4) | 0.21 | 1.1 [0.23-34] | 0.47 | 0.89 | 54 | substrate_background / contamination (0.35) | 58.0 |
| transfer + F(ab')2 conjugate + screened reagents (L3 + L4 + L6 + L7) | 0.061 | 0.54 [0.12-1.2] | 0.87 | 1.00 | 32 | baseline_drift / contamination (0.72) | 58.0 |
| the same with a reference channel (L5) | 0.06 | 0.53 [0.12-1.2] | 0.87 | 1.00 | 32 | baseline_drift / contamination (0.73) | 58.0 |
| valves only: tier 2 chemistry with an isolated bed (no transfer) | 0.34 | 1.8 [0.38-21] | 0.28 | 0.89 | 32 | nsb_variability / nsb_variability (0.60) | 57.0 |

## 6. One-at-a-time sensitivity of the three implementations

LOD (pg/mL) with one parameter at its low and at its high bound, all others at their best estimate; the eight largest swings.


**Tier 1: thin-film gold electrode, capture on the electrode, read under 1 uL/min substrate flow** (nominal 4.3 pg/mL)

| Parameter | value [low-high] | LOD at low | LOD at high |
|---|---|---|---|
| `chem.antibodies.koff_detection` | 0.00086 [3e-06-0.0083] 1/s | 2.1 | 1.4e+03 |
| `ma.chemistries.alp_hqdp.free_product_impurity` | 1e-05 [1e-07-0.001] mol/mol | 4.2 | 63 |
| `chem.enzymes.alp.kcat_conjugate_assay_conditions` | 1000 [100-6000] 1/s | 35 | 2.5 |
| `ma.chemistries.alp_hqdp.hydrolysis_rate` | 1e-10 [1e-12-1e-08] 1/s | 4.2 | 54 |
| `chem.antibodies.kon_detection` | 390000 [90000-1.2e+06] 1/(M*s) | 15 | 2.1 |
| `tr.noise.drift_area_exponent` | 1 [0-1] dimensionless | 29 | 4.3 |
| `chem.nsb.nsb_effective_rate_constant` | 4e-11 [8e-12-4e-10] m/s | 3.5 | 24 |
| `tr.nsb.surface_factor_gold_oeg` | 3 [0.5-30] fold | 3.6 | 21 |

**Tier 2: capillary micro-bed above a printed carbon electrode, stopped accumulation, swept read** (nominal 0.36 pg/mL)

| Parameter | value [low-high] | LOD at low | LOD at high |
|---|---|---|---|
| `chem.antibodies.koff_detection` | 0.00086 [3e-06-0.0083] 1/s | 0.22 | 23 |
| `ma.chemistries.alp_hqdp.free_product_impurity` | 1e-05 [1e-07-0.001] mol/mol | 0.35 | 10 |
| `chem.nsb.nsb_effective_rate_constant` | 4e-11 [8e-12-4e-10] m/s | 0.14 | 3.7 |
| `ma.nsb.label_factor_igg_enzyme_conjugate` | 0.04 [0.01-0.15] fold | 0.15 | 1.3 |
| `chem.antibodies.kon_detection` | 390000 [90000-1.2e+06] 1/(M*s) | 1.4 | 0.16 |
| `tr.nsb.surface_factor_frit` | 10 [1-100] fold | 0.28 | 1.3 |
| `ma.nsb.blank_igg_contamination_equivalent` | 0 [0-3e-15] M | 0.36 | 1.4 |
| `chem.enzymes.alp.kcat_conjugate_assay_conditions` | 1000 [100-6000] 1/s | 1.3 | 0.36 |

**Tier 3: tier 2 bed behind valves + immune-complex transfer to a second bed (L4)** (nominal 0.21 pg/mL)

| Parameter | value [low-high] | LOD at low | LOD at high |
|---|---|---|---|
| `chem.antibodies.koff_detection` | 0.00086 [3e-06-0.0083] 1/s | 0.089 | 3.1e+02 |
| `ma.chemistries.alp_hqdp.free_product_impurity` | 1e-05 [1e-07-0.001] mol/mol | 0.15 | 17 |
| `chem.enzymes.alp.kcat_conjugate_assay_conditions` | 1000 [100-6000] 1/s | 2 | 0.086 |
| `chem.antibodies.kon_detection` | 390000 [90000-1.2e+06] 1/(M*s) | 0.81 | 0.093 |
| `ma.nsb.blank_igg_contamination_equivalent` | 0 [0-3e-15] M | 0.21 | 1.4 |
| `ma.noise.background_current_relative_noise` | 0.01 [0.002-0.05] fraction | 0.15 | 0.78 |
| `chem.nsb.nsb_effective_rate_constant` | 4e-11 [8e-12-4e-10] m/s | 0.2 | 0.82 |
| `chem.surfaces.igg_surface_density_monolayer` | 1e+16 [2e+15-1.5e+16] molecules/m^2 | 0.65 | 0.18 |

## 7. Step tables used for the timing


**Tier 1: thin-film gold electrode, capture on the electrode, read under 1 uL/min substrate flow** - 56.0 min from Inject Start to result

| Step | min | counts |
|---|---|---|
| pre-run: buffer flush, substrate fill, background read on the fresh electrode, buffer flush | 8.0 | no (before injection) |
| sample injection (SM-FL aspirate and load) | 1.0 | yes |
| sample pumped through the cell | 36.0 | yes |
| wash 1 | 1.5 | yes |
| conjugate injection (SM-FL) | 1.0 | yes |
| conjugate pumped into the cell | 5.0 | yes |
| conjugate stopped in the cell | 3.0 | yes |
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

**Tier 3: tier 2 bed behind valves + immune-complex transfer to a second bed (L4)** - 58.0 min from Inject Start to result

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
