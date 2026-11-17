# Three-tier round: model results (scripts/tier_round/run_tiers.py)

## 1. The three implementations, as specified

Monte Carlo n = 2000, seed 20261111. Tier 3 carries the immune-complex transfer as release (0.7 [0.2-0.95], UNVERIFIED) x re-capture (bed equation at the push flow) and non-specific label x0.1 [0.01-0.5] (ma.design_levers, UNVERIFIED).

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | upper limit by the slope criterion / curve rises up to (pg/mL) | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| Tier 1: capture on a printed gold strip, read at the electrode under fast substrate flow | 9.4 | 35 [4.4-5.6e+02] | 0.00 | 0.16 | 1e+05 / 1e+05 | substrate_background / substrate_background (0.56) | 56.9 |
| Tier 2: capillary micro-bed above a printed carbon strip, stop and sweep | 2.6 | 13 [1.4-1.7e+02] | 0.02 | 0.43 | 32 / 1e+05 | nsb_variability / nsb_variability (0.85) | 58.7 |
| Tier 3: two beds behind two valves, immune-complex transfer to the read bed | 0.62 | 4.8 [0.54-2.6e+02] | 0.15 | 0.64 | 93 / 1e+05 | nsb_variability / nsb_variability (0.54) | 58.2 |

## 2. Scenarios - Tier 1: capture on a printed gold strip, read at the electrode under fast substrate flow

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | upper limit by the slope criterion / curve rises up to (pg/mL) | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| as specified | 9.4 | 35 [4.4-5.6e+02] | 0.00 | 0.16 | 1e+05 / 1e+05 | substrate_background / substrate_background (0.56) | 56.9 |
| detection reagent and substrate lot pass screening (L6 + L7) | 4.5 | 16 [2.6-1.3e+02] | 0.00 | 0.34 | 1e+05 / 1e+05 | baseline_drift / nsb_variability (0.53) | 56.9 |
| credit for the F(ab')2 conjugate (L3) | 9 | 28 [3.4-5.3e+02] | 0.00 | 0.22 | 1e+05 / 1e+05 | substrate_background / substrate_background (0.64) | 56.9 |
| L3 + L6 + L7 | 4.1 | 11 [2-1e+02] | 0.01 | 0.45 | 1e+05 / 1e+05 | baseline_drift / nsb_variability (0.38) | 56.9 |
| non-specific binding x25 (S1) | 71 | 2.8e+02 [38-2.4e+03] | 0.00 | 0.00 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.88) | 56.9 |
| free hydroquinone 1e-3 in the substrate (S4a) | 6.3e+02 | 9.2e+02 [1.4e+02-6.5e+03] | 0.00 | 0.00 | 1e+05 / 1e+05 | substrate_background / substrate_background (1.00) | 56.9 |
| blank contamination up to 1 pg/mL (C1) | 9.4 | 35 [4.6-5.6e+02] | 0.00 | 0.16 | 1e+05 / 1e+05 | substrate_background / substrate_background (0.56) | 56.9 |
| only 1 % of the turnovers give an electroactive product (review C1) | 8.9e+02 | 2.3e+03 [1.7e+02-5.2e+04] | 0.00 | 0.00 | 1e+05 / 1e+05 | substrate_background / substrate_background (0.77) | 56.9 |

## 2. Scenarios - Tier 2: capillary micro-bed above a printed carbon strip, stop and sweep

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | upper limit by the slope criterion / curve rises up to (pg/mL) | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| as specified | 2.6 | 13 [1.4-1.7e+02] | 0.02 | 0.43 | 32 / 1e+05 | nsb_variability / nsb_variability (0.85) | 58.7 |
| detection reagent and substrate lot pass screening (L6 + L7) | 1.7 | 7.4 [1-78] | 0.05 | 0.58 | 32 / 1e+05 | nsb_variability / nsb_variability (0.98) | 58.7 |
| credit for the F(ab')2 conjugate (L3) | 1.3 | 7.1 [0.85-94] | 0.07 | 0.60 | 32 / 1e+05 | nsb_variability / nsb_variability (0.76) | 58.7 |
| L3 + L6 + L7 | 0.81 | 3.6 [0.64-36] | 0.13 | 0.78 | 18 / 1e+05 | nsb_variability / nsb_variability (0.92) | 58.7 |
| non-specific binding x25 (S1) | 1e+02 | 3.9e+02 [33-6.2e+03] | 0.00 | 0.00 | 2.7e+02 / 1e+05 | nsb_variability / nsb_variability (0.99) | 58.7 |
| free hydroquinone 1e-3 in the substrate (S4a) | 60 | 1e+02 [13-1.2e+03] | 0.00 | 0.03 | 32 / 1e+05 | substrate_background / substrate_background (0.93) | 58.7 |
| blank contamination up to 1 pg/mL (C1) | 2.6 | 13 [1.6-1.7e+02] | 0.01 | 0.42 | 32 / 1e+05 | nsb_variability / nsb_variability (0.81) | 58.7 |
| only 1 % of the turnovers give an electroactive product (review C1) | 36 | 76 [6.2-2.9e+03] | 0.00 | 0.10 | 2.3e+03 / 1e+05 | substrate_background / substrate_background (0.70) | 58.7 |

## 2. Scenarios - Tier 3: two beds behind two valves, immune-complex transfer to the read bed

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | upper limit by the slope criterion / curve rises up to (pg/mL) | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| as specified | 0.62 | 4.8 [0.54-2.6e+02] | 0.15 | 0.64 | 93 / 1e+05 | nsb_variability / nsb_variability (0.54) | 58.2 |
| with a reference channel as well (L5) | 0.56 | 4.4 [0.53-2.5e+02] | 0.17 | 0.65 | 93 / 1e+05 | nsb_variability / nsb_variability (0.51) | 58.2 |
| detection reagent and substrate lot pass screening (L6 + L7) | 0.22 | 1.5 [0.32-23] | 0.34 | 0.88 | 32 / 1e+05 | nsb_variability / nsb_variability (0.65) | 58.2 |
| credit for the F(ab')2 conjugate (L3) | 0.45 | 3.3 [0.44-2e+02] | 0.22 | 0.70 | 93 / 1e+05 | substrate_background / nsb_variability (0.41) | 58.2 |
| L3 + L6 + L7 | 0.14 | 1.1 [0.25-12] | 0.45 | 0.94 | 32 / 1e+05 | nsb_variability / nsb_variability (0.50) | 58.2 |
| non-specific binding x25 (S1) | 14 | 70 [3.7-4.2e+03] | 0.01 | 0.16 | 1.6e+02 / 1e+05 | nsb_variability / nsb_variability (0.94) | 58.2 |
| free hydroquinone 1e-3 in the substrate (S4a) | 33 | 91 [5.9-3.9e+03] | 0.00 | 0.09 | 93 / 1e+05 | substrate_background / substrate_background (0.98) | 58.2 |
| blank contamination up to 1 pg/mL (C1) | 0.62 | 5 [0.77-2.6e+02] | 0.08 | 0.64 | 93 / 1e+05 | nsb_variability / nsb_variability (0.49) | 58.2 |
| only 1 % of the turnovers give an electroactive product (review C1) | 37 | 1.5e+02 [7.4-1.5e+04] | 0.00 | 0.07 | 1.2e+04 / 1e+05 | substrate_background / substrate_background (0.58) | 58.2 |

## 3. Tier 1 - alternatives and hardware cases

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | upper limit by the slope criterion / curve rises up to (pg/mL) | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| primary: printed gold AU10, strip-cell gap 0.20 mm, read at 150 uL/min, 0.3 mM substrate | 9.4 | 35 [4.4-5.6e+02] | 0.00 | 0.16 | 1e+05 / 1e+05 | substrate_background / substrate_background (0.56) | 56.9 |
| printed carbon C21 with adsorbed streptavidin (same cell and read) | 17 | 78 [8.8-1.1e+03] | 0.00 | 0.06 | 1e+05 / 1e+05 | nsb_variability / substrate_background (0.48) | 56.9 |
| thin-film gold chip SE1 in the thin-film cell (same read) | 13 | 48 [5.5-8.9e+02] | 0.00 | 0.12 | 1e+05 / 1e+05 | substrate_background / substrate_background (0.59) | 56.9 |
| strip-cell gap 0.10 mm | 9.1 | 36 [4.1-6.7e+02] | 0.00 | 0.17 | 1e+05 / 1e+05 | substrate_background / substrate_background (0.62) | 56.9 |
| strip-cell gap 0.50 mm | 12 | 39 [5.5-5.1e+02] | 0.00 | 0.12 | 1e+05 / 1e+05 | baseline_drift / substrate_background (0.45) | 56.9 |
| read at 80 uL/min | 11 | 39 [5.5-5.7e+02] | 0.00 | 0.13 | 1e+05 / 1e+05 | baseline_drift / substrate_background (0.46) | 56.4 |
| read at 40 uL/min (load cut to 34 min) | 20 | 56 [7.7-7.6e+02] | 0.00 | 0.07 | 1e+05 / 1e+05 | baseline_drift / nsb_variability (0.39) | 56.8 |
| substrate 0.1 mM | 8.8 | 30 [4.2-3.5e+02] | 0.00 | 0.18 | 1e+05 / 1e+05 | baseline_drift / substrate_background (0.39) | 56.9 |
| substrate 1 mM | 21 | 61 [6.2-1.4e+03] | 0.00 | 0.10 | 1e+05 / 1e+05 | substrate_background / substrate_background (0.74) | 56.9 |
| stopped read (needs a zero-flow row), 30 s wait + 120 s | 15 | 39 [5.7-3.5e+02] | 0.00 | 0.12 | 1e+05 / 1e+05 | baseline_drift / nsb_variability (0.67) | 56.9 |
| transfer line 0.127 mm x 20 cm instead of 0.05 mm x 15 cm | 9.8 | 40 [5.3-5.7e+02] | 0.00 | 0.13 | 1e+05 / 1e+05 | substrate_background / substrate_background (0.51) | 56.9 |
| no pre-read on the electrode | 27 | 75 [7.9-1.7e+03] | 0.00 | 0.07 | 1e+05 / 1e+05 | electrode_sensitivity / electrode_sensitivity (0.71) | 56.9 |
| printed carbon C21, stopped read | 27 | 77 [10-8.8e+02] | 0.00 | 0.05 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.73) | 56.9 |

## 4. Tier 2 - alternatives and hardware cases

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | upper limit by the slope criterion / curve rises up to (pg/mL) | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| primary (strip-cell gap 0.20 mm) | 2.6 | 13 [1.4-1.7e+02] | 0.02 | 0.43 | 32 / 1e+05 | nsb_variability / nsb_variability (0.85) | 58.7 |
| strip-cell gap 0.10 mm | 2.6 | 13 [1.4-1.7e+02] | 0.02 | 0.43 | 32 / 1e+05 | nsb_variability / nsb_variability (0.85) | 58.7 |
| strip-cell gap 0.50 mm | 2.6 | 13 [1.4-1.7e+02] | 0.02 | 0.43 | 32 / 1e+05 | nsb_variability / nsb_variability (0.85) | 58.7 |
| pump cannot stop: continuous read at 1 uL/min | 3 | 12 [1.6-1.2e+02] | 0.01 | 0.44 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.92) | 59.2 |
| pump cannot stop and cannot go below 10 uL/min | 4.2 | 20 [2.8-2.3e+02] | 0.00 | 0.29 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.74) | 59.2 |
| bed binds conjugate like beads washed in tubes (factor 1 instead of 3) | 2 | 9.9 [1.1-1.2e+02] | 0.04 | 0.50 | 32 / 1e+05 | nsb_variability / nsb_variability (0.82) | 58.7 |
| retainer wetted area 1 mm2 instead of 5 mm2 | 2.1 | 11 [1.2-1.5e+02] | 0.03 | 0.47 | 32 / 1e+05 | nsb_variability / nsb_variability (0.83) | 58.7 |
| retainer wetted area 20 mm2 (0.5 mm silicate frit) | 4.3 | 19 [1.8-2.4e+02] | 0.01 | 0.34 | 32 / 1e+05 | nsb_variability / nsb_variability (0.88) | 58.7 |
| no conjugate-exposed wall upstream of the bed (bound) | 1.4 | 6.9 [0.96-92] | 0.06 | 0.59 | 32 / 1e+05 | nsb_variability / nsb_variability (0.76) | 58.7 |
| transfer line 0.127 mm x 20 cm | 4.5 | 22 [2.1-3e+02] | 0.01 | 0.30 | 54 / 1e+05 | nsb_variability / nsb_variability (0.89) | 58.7 |
| bed in a fitting on the inlet port (whole bore between bed and electrode) | 2.9 | 15 [1.6-1.9e+02] | 0.02 | 0.39 | 32 / 1e+05 | nsb_variability / nsb_variability (0.86) | 58.7 |
| half the beads (5e5) | 3 | 18 [1.7-2.4e+02] | 0.01 | 0.35 | 54 / 1e+05 | nsb_variability / nsb_variability (0.84) | 58.7 |
| twice the beads (2e6) | 2.9 | 12 [1.4-1.5e+02] | 0.02 | 0.44 | 32 / 1e+05 | nsb_variability / nsb_variability (0.87) | 58.7 |
| stop 3 min instead of 7 (load 41 min) | 2.5 | 13 [1.5-1.7e+02] | 0.02 | 0.42 | 93 / 1e+05 | nsb_variability / nsb_variability (0.78) | 58.7 |
| stop 30 s (range read) | 4.7 | 21 [2.2-4.1e+02] | 0.01 | 0.30 | 4.6e+02 / 1e+05 | substrate_background / nsb_variability (0.54) | 52.2 |
| parked read instead of swept | 3.3 | 14 [1.6-2e+02] | 0.02 | 0.41 | 32 / 1e+05 | nsb_variability / nsb_variability (0.96) | 59.2 |
| conjugate 3 nM | 2.3 | 13 [1.4-1.8e+02] | 0.02 | 0.43 | 93 / 1e+05 | nsb_variability / nsb_variability (0.73) | 58.7 |

## 5. Tier 3 - alternatives

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | upper limit by the slope criterion / curve rises up to (pg/mL) | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| primary (transfer by a cleavable link, release 0.7 [0.2-0.95]) | 0.62 | 4.8 [0.54-2.6e+02] | 0.15 | 0.64 | 93 / 1e+05 | nsb_variability / nsb_variability (0.54) | 58.2 |
| valves only: the capture bed is read, no transfer | 1.5 | 6.9 [0.87-85] | 0.06 | 0.61 | 32 / 1e+05 | nsb_variability / nsb_variability (0.88) | 56.7 |
| valves only, screened reagents (L6 + L7) | 1.1 | 4.3 [0.72-46] | 0.10 | 0.72 | 18 / 1e+05 | nsb_variability / nsb_variability (0.95) | 56.7 |
| transfer with desthiobiotin and biotin, 5 min (release 0.1 [0.003-0.26]) | 4.3 | 56 [2.5-4e+03] | 0.01 | 0.19 | 7.9e+02 / 1e+05 | nsb_variability / nsb_variability (0.60) | 58.2 |
| transfer: release 0.95, non-specific x0.01 (optimistic bounds) | 0.27 | 1.2 [0.23-76] | 0.43 | 0.84 | 54 / 1e+05 | substrate_background / substrate_background (0.40) | 58.2 |
| transfer: release 0.2, non-specific x0.5 (pessimistic bounds) | 9 | 48 [3.6-2.2e+03] | 0.00 | 0.18 | 4.6e+02 / 1e+05 | nsb_variability / nsb_variability (0.85) | 58.2 |
| transfer + screened reagents + F(ab')2 credit (L3 + L6 + L7) | 0.14 | 1.1 [0.25-12] | 0.45 | 0.94 | 32 / 1e+05 | nsb_variability / nsb_variability (0.50) | 58.2 |
| the same with a reference channel (L5) | 0.13 | 1.1 [0.24-10] | 0.47 | 0.95 | 32 / 1e+05 | baseline_drift / nsb_variability (0.46) | 58.2 |
| accumulation 12 min instead of 7 (load 20 min) | 0.63 | 5 [0.53-2.8e+02] | 0.15 | 0.63 | 54 / 1e+05 | nsb_variability / nsb_variability (0.60) | 58.2 |

## 6. One-at-a-time sensitivity of the three implementations

LOD (pg/mL) with one parameter at its low and at its high bound, all others at their best estimate; the nine largest swings.


**Tier 1: capture on a printed gold strip, read at the electrode under fast substrate flow** (nominal 9.4 pg/mL)

| Parameter | value [low-high] | LOD at low | LOD at high |
|---|---|---|---|
| `ma.chemistries.alp_hqdp.free_product_impurity` | 1e-05 [1e-07-0.001] mol/mol | 6.1 | 6.3e+02 |
| `chem.antibodies.koff_detection` | 0.00086 [3e-06-0.0083] 1/s | 6.4 | 2.4e+02 |
| `chem.enzymes.alp.kcat_conjugate_assay_conditions` | 1000 [100-6000] 1/s | 89 | 3.2 |
| `ma.chemistries.alp_hqdp.hydrolysis_rate` | 1e-10 [1e-12-1e-08] 1/s | 8.5 | 1.9e+02 |
| `chem.antibodies.kon_detection` | 390000 [90000-1.2e+06] 1/(M*s) | 34 | 4.5 |
| `ma.chemistries.alp_hqdp.Km` | 0.0001 [2e-05-0.001] M | 7.7 | 29 |
| `chem.antibodies.enzyme_to_antibody_ratio_ALP` | 1 [0.5-2] mol/mol | 18 | 5.3 |
| `chem.nsb.nsb_effective_rate_constant` | 4e-11 [8e-12-4e-10] m/s | 8.9 | 30 |
| `tr.nsb.surface_factor_gold_oeg` | 3 [1-30] fold | 9 | 23 |

**Tier 2: capillary micro-bed above a printed carbon strip, stop and sweep** (nominal 2.6 pg/mL)

| Parameter | value [low-high] | LOD at low | LOD at high |
|---|---|---|---|
| `chem.antibodies.koff_detection` | 0.00086 [3e-06-0.0083] 1/s | 1.6 | 1.1e+02 |
| `chem.nsb.nsb_effective_rate_constant` | 4e-11 [8e-12-4e-10] m/s | 0.6 | 35 |
| `ma.chemistries.alp_hqdp.free_product_impurity` | 1e-05 [1e-07-0.001] mol/mol | 2.5 | 60 |
| `ma.nsb.label_factor_igg_enzyme_conjugate` | 0.04 [0.01-0.15] fold | 0.7 | 11 |
| `ma.nsb.surface_factor_tubing` | 3 [1-30] fold | 1.8 | 16 |
| `chem.antibodies.kon_detection` | 390000 [90000-1.2e+06] 1/(M*s) | 9.3 | 1.2 |
| `ma.nsb.surface_factor_packed_bed` | 3 [1-30] fold | 2 | 11 |
| `tr.nsb.surface_factor_frit` | 10 [1-100] fold | 2.1 | 8.2 |
| `ma.labelling.detection_on_capture_residual_factor` | 1 [1-3] fold | 2.6 | 8.6 |

**Tier 3: two beds behind two valves, immune-complex transfer to the read bed** (nominal 0.62 pg/mL)

| Parameter | value [low-high] | LOD at low | LOD at high |
|---|---|---|---|
| `chem.antibodies.koff_detection` | 0.00086 [3e-06-0.0083] 1/s | 0.22 | 4.7e+03 |
| `ma.chemistries.alp_hqdp.free_product_impurity` | 1e-05 [1e-07-0.001] mol/mol | 0.55 | 33 |
| `chem.nsb.nsb_effective_rate_constant` | 4e-11 [8e-12-4e-10] m/s | 0.38 | 5.3 |
| `chem.surfaces.igg_surface_density_monolayer` | 1e+16 [2e+15-1.5e+16] molecules/m^2 | 4.1 | 0.5 |
| `chem.antibodies.kon_detection` | 390000 [90000-1.2e+06] 1/(M*s) | 2.3 | 0.3 |
| `chem.enzymes.alp.kcat_conjugate_assay_conditions` | 1000 [100-6000] 1/s | 3.7 | 0.52 |
| `ma.design_levers.immune_complex_transfer_nsb_factor` | 0.1 [0.01-0.5] fold | 0.37 | 2.6 |
| `ma.nsb.surface_factor_packed_bed` | 3 [1-30] fold | 0.5 | 2.7 |
| `chem.antibodies.kon_capture` | 300000 [90000-1.2e+06] 1/(M*s) | 2.2 | 0.42 |

## 7. Step tables used for the timing


**Tier 1: capture on a printed gold strip, read at the electrode under fast substrate flow** - 56.9 min from Inject Start to result

| Step | min | counts |
|---|---|---|
| pre-run: cleaning injection, hydroquinone locator plug, the same read sequence on the fresh electrode | 12.0 | no (before injection) |
| sample injection (SM-FL aspirate and load) | 1.0 | yes |
| sample pumped through the cell | 42.0 | yes |
| wash 1 (Loop Offline at its start) | 1.5 | yes |
| conjugate injection (SM-FL) | 1.0 | yes |
| conjugate through the cell, two loop volumes, then Loop Offline | 4.0 | yes |
| wash 2 at the read flow; its last 30 s are the first reference window | 2.0 | yes |
| substrate front (BSM A1 -> B1 at the read flow) | 1.4 | yes |
| read window, substrate flowing | 2.0 | yes |
| buffer front (B1 -> A1) | 1.4 | yes |
| second reference window, buffer flowing | 0.5 | yes |

**Tier 2: capillary micro-bed above a printed carbon strip, stop and sweep** - 58.7 min from Inject Start to result

| Step | min | counts |
|---|---|---|
| pre-run: cleaning injection; the same substrate step, stop and sweep on the fresh bed and strip | 14.0 | no (before injection) |
| sample injection (SM-FL aspirate and load) | 1.0 | yes |
| sample pumped through the bed | 37.0 | yes |
| wash 1 (Loop Offline at its start) | 1.5 | yes |
| conjugate injection (SM-FL) | 1.0 | yes |
| conjugate through the bed, two loop volumes, then Loop Offline | 4.0 | yes |
| wash 2 | 2.0 | yes |
| step to substrate, 215 uL at 80 uL/min | 2.7 | yes |
| step down to 5 uL/min so that the pump pressure relaxes | 1.0 | yes |
| accumulation: product collects in the bed | 7.0 | yes |
| sweep over the electrode and read | 1.5 | yes |

**Tier 3: two beds behind two valves, immune-complex transfer to the read bed** - 58.2 min from Inject Start to result

| Step | min | counts |
|---|---|---|
| pre-run: cleaning injection; the same substrate step, stop and sweep on the fresh bed and strip | 14.0 | no (before injection) |
| sample injection (SM-FL aspirate and load) | 1.0 | yes |
| sample pumped through the bed | 25.0 | yes |
| wash 1 (Loop Offline at its start) | 1.5 | yes |
| conjugate injection (SM-FL) | 1.0 | yes |
| conjugate through the bed, two loop volumes, then Loop Offline | 4.0 | yes |
| wash 2 | 2.0 | yes |
| eluent injection, hold on bed 1, push through bed 2, wash of bed 2 (tier 3) | 12.5 | yes |
| step to substrate, 215 uL at 80 uL/min | 2.7 | yes |
| step down to 5 uL/min so that the pump pressure relaxes | 0.0 | yes |
| accumulation: product collects in the bed | 7.0 | yes |
| sweep over the electrode and read | 1.5 | yes |
