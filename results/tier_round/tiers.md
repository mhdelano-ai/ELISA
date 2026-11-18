# Three-tier round: model results (scripts/tier_round/run_tiers.py)

## 1. The three implementations, as specified

Monte Carlo n = 2000, seed 20261111. The transfer is carried as release (0.35 [0.05-0.74], UNVERIFIED) x re-capture on a read bed of three times the beads (bed equation with site depletion at the push flow) and non-specific label x0.1 [0.01-0.5] (ma.design_levers, UNVERIFIED).

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | upper limit by the slope criterion / curve rises up to (pg/mL) | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| Tier 1: capture on a printed gold strip, read at the electrode under fast substrate flow | 3.6 | 16 [2.8-1.1e+02] | 0.00 | 0.33 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.68) | 57.1 |
| Tier 2: capillary micro-bed above a printed carbon strip, stop and sweep | 2.1 | 8.4 [1-1e+02] | 0.05 | 0.54 | 1.4e+03 / 1e+05 | nsb_variability / nsb_variability (0.97) | 56.7 |
| Tier 3: the capture bed in the loop of one valve | 1.2 | 5.1 [0.78-58] | 0.09 | 0.69 | 2.7e+02 / 1e+05 | nsb_variability / nsb_variability (0.91) | 56.7 |
| Tier 3 with the immune-complex transfer to a second bed | 1.1 | 5.8 [0.64-2.8e+02] | 0.12 | 0.61 | 2.7e+02 / 1e+05 | nsb_variability / nsb_variability (0.62) | 58.2 |

## 2. Scenarios - Tier 1: capture on a printed gold strip, read at the electrode under fast substrate flow

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | upper limit by the slope criterion / curve rises up to (pg/mL) | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| as specified | 3.6 | 16 [2.8-1.1e+02] | 0.00 | 0.33 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.68) | 57.1 |
| detection reagent and substrate lot pass screening (L6 + L7) | 2.7 | 12 [2.3-79] | 0.00 | 0.42 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.67) | 57.1 |
| credit for the F(ab')2 conjugate (L3) | 2.5 | 11 [1.9-79] | 0.01 | 0.47 | 1e+05 / 1e+05 | baseline_drift / nsb_variability (0.52) | 57.1 |
| L3 + L6 + L7 | 1.9 | 8.3 [1.7-52] | 0.01 | 0.57 | 1e+05 / 1e+05 | baseline_drift / nsb_variability (0.51) | 57.1 |
| non-specific binding x25 (S1) | 76 | 2.5e+02 [36-2.1e+03] | 0.00 | 0.00 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.99) | 57.1 |
| no decay in the reservoir: background 1e-5 of the substrate at the time of use | 5.9 | 31 [4.6-3.9e+02] | 0.00 | 0.18 | 1e+05 / 1e+05 | substrate_background / substrate_background (0.49) | 57.1 |
| no decay and screened reagents (L6 + L7) | 2.9 | 16 [2.8-1.2e+02] | 0.00 | 0.35 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.57) | 57.1 |
| background 1e-3 of the substrate, no decay (S4a) | 3.9e+02 | 6.7e+02 [1e+02-4.9e+03] | 0.00 | 0.00 | 1e+05 / 1e+05 | substrate_background / substrate_background (1.00) | 57.1 |
| blank contamination up to 1 pg/mL | 3.6 | 16 [3-1.1e+02] | 0.00 | 0.33 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.67) | 57.1 |
| only 1 % of the turnovers give an electroactive product (review C1) | 2e+02 | 5.3e+02 [63-5.4e+03] | 0.00 | 0.00 | 1e+05 / 1e+05 | baseline_drift / baseline_drift (0.78) | 57.1 |
| only 1 % of the turnovers electroactive, and no decay in the reservoir | 5e+02 | 1.8e+03 [1.5e+02-3.6e+04] | 0.00 | 0.00 | 1e+05 / 1e+05 | substrate_background / substrate_background (0.72) | 57.1 |
| only 0.1 % of the turnovers give an electroactive product | 2e+03 | 5.3e+03 [6e+02-5.4e+04] | 0.00 | 0.00 | 1e+05 / 1e+05 | baseline_drift / baseline_drift (0.79) | 57.1 |

## 2. Scenarios - Tier 2: capillary micro-bed above a printed carbon strip, stop and sweep

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | upper limit by the slope criterion / curve rises up to (pg/mL) | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| as specified | 2.1 | 8.4 [1-1e+02] | 0.05 | 0.54 | 1.4e+03 / 1e+05 | nsb_variability / nsb_variability (0.97) | 56.7 |
| detection reagent and substrate lot pass screening (L6 + L7) | 1.4 | 6 [0.9-56] | 0.06 | 0.65 | 7.9e+02 / 1e+05 | nsb_variability / nsb_variability (0.96) | 56.7 |
| credit for the F(ab')2 conjugate (L3) | 1 | 4.3 [0.66-50] | 0.11 | 0.72 | 1.4e+03 / 1e+05 | nsb_variability / nsb_variability (0.91) | 56.7 |
| L3 + L6 + L7 | 0.7 | 3 [0.61-27] | 0.15 | 0.82 | 7.9e+02 / 1e+05 | nsb_variability / nsb_variability (0.89) | 56.7 |
| non-specific binding x25 (S1) | 57 | 2.3e+02 [23-2.6e+03] | 0.00 | 0.01 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (1.00) | 56.7 |
| no decay in the reservoir: background 1e-5 of the substrate at the time of use | 2.2 | 12 [1.4-1.3e+02] | 0.02 | 0.45 | 1.4e+03 / 1e+05 | nsb_variability / nsb_variability (0.76) | 56.7 |
| no decay and screened reagents (L6 + L7) | 1.4 | 6.3 [0.96-58] | 0.05 | 0.64 | 7.9e+02 / 1e+05 | nsb_variability / nsb_variability (0.91) | 56.7 |
| background 1e-3 of the substrate, no decay (S4a) | 67 | 1.1e+02 [16-1.1e+03] | 0.00 | 0.02 | 1.4e+03 / 1e+05 | substrate_background / substrate_background (0.96) | 56.7 |
| blank contamination up to 1 pg/mL | 2.1 | 8.5 [1.3-1e+02] | 0.02 | 0.54 | 1.4e+03 / 1e+05 | nsb_variability / nsb_variability (0.92) | 56.7 |
| only 1 % of the turnovers give an electroactive product (review C1) | 13 | 29 [4.5-2.8e+02] | 0.00 | 0.19 | 1e+05 / 1e+05 | baseline_drift / baseline_drift (0.37) | 56.7 |
| only 1 % of the turnovers electroactive, and no decay in the reservoir | 73 | 1.7e+02 [12-5.5e+03] | 0.00 | 0.04 | 1e+05 / 1e+05 | substrate_background / substrate_background (0.87) | 56.7 |
| only 0.1 % of the turnovers give an electroactive product | 1.2e+02 | 2e+02 [26-2.5e+03] | 0.00 | 0.00 | 1e+05 / 1e+05 | baseline_drift / baseline_drift (0.54) | 56.7 |

## 2. Scenarios - Tier 3: the capture bed in the loop of one valve

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | upper limit by the slope criterion / curve rises up to (pg/mL) | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| as specified | 1.2 | 5.1 [0.78-58] | 0.09 | 0.69 | 2.7e+02 / 1e+05 | nsb_variability / nsb_variability (0.91) | 56.7 |
| with a reference channel as well (L5) | 1.1 | 4.4 [0.7-49] | 0.11 | 0.71 | 2.7e+02 / 1e+05 | nsb_variability / nsb_variability (0.88) | 56.7 |
| detection reagent and substrate lot pass screening (L6 + L7) | 0.88 | 3.7 [0.71-34] | 0.11 | 0.77 | 2.7e+02 / 1e+05 | nsb_variability / nsb_variability (0.91) | 56.7 |
| credit for the F(ab')2 conjugate (L3) | 0.65 | 2.7 [0.52-28] | 0.18 | 0.82 | 2.7e+02 / 1e+05 | nsb_variability / nsb_variability (0.81) | 56.7 |
| L3 + L6 + L7 | 0.46 | 2 [0.49-16] | 0.23 | 0.90 | 1.6e+02 / 1e+05 | nsb_variability / nsb_variability (0.79) | 56.7 |
| non-specific binding x25 (S1) | 36 | 1.4e+02 [13-1.6e+03] | 0.00 | 0.03 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.99) | 56.7 |
| no decay in the reservoir: background 1e-5 of the substrate at the time of use | 1.3 | 6.7 [0.98-79] | 0.06 | 0.62 | 2.7e+02 / 1e+05 | nsb_variability / nsb_variability (0.74) | 56.7 |
| no decay and screened reagents (L6 + L7) | 0.89 | 4 [0.73-34] | 0.10 | 0.76 | 2.7e+02 / 1e+05 | nsb_variability / nsb_variability (0.88) | 56.7 |
| background 1e-3 of the substrate, no decay (S4a) | 27 | 52 [6.6-5.5e+02] | 0.00 | 0.10 | 2.7e+02 / 1e+05 | substrate_background / substrate_background (0.93) | 56.7 |
| blank contamination up to 1 pg/mL | 1.2 | 5.2 [1-58] | 0.05 | 0.69 | 2.7e+02 / 1e+05 | nsb_variability / nsb_variability (0.83) | 56.7 |
| only 1 % of the turnovers give an electroactive product (review C1) | 20 | 34 [5.1-3e+02] | 0.00 | 0.16 | 3.4e+04 / 1e+05 | baseline_drift / baseline_drift (0.54) | 56.7 |
| only 1 % of the turnovers electroactive, and no decay in the reservoir | 35 | 1e+02 [9.4-2.7e+03] | 0.00 | 0.06 | 3.4e+04 / 1e+05 | substrate_background / substrate_background (0.69) | 56.7 |
| only 0.1 % of the turnovers give an electroactive product | 2e+02 | 3e+02 [38-2.8e+03] | 0.00 | 0.00 | 1e+05 / 1e+05 | baseline_drift / baseline_drift (0.61) | 56.7 |

## 2. Scenarios - Tier 3 with the immune-complex transfer to a second bed

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | upper limit by the slope criterion / curve rises up to (pg/mL) | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| as specified | 1.1 | 5.8 [0.64-2.8e+02] | 0.12 | 0.61 | 2.7e+02 / 1e+05 | nsb_variability / nsb_variability (0.62) | 58.2 |
| with a reference channel as well (L5) | 0.94 | 5.2 [0.6-2.6e+02] | 0.13 | 0.63 | 2.7e+02 / 1e+05 | nsb_variability / nsb_variability (0.57) | 58.2 |
| detection reagent and substrate lot pass screening (L6 + L7) | 0.43 | 3 [0.48-42] | 0.19 | 0.79 | 93 / 1e+05 | nsb_variability / nsb_variability (0.60) | 58.2 |
| credit for the F(ab')2 conjugate (L3) | 0.65 | 3.4 [0.5-1.6e+02] | 0.19 | 0.72 | 2.7e+02 / 1e+05 | nsb_variability / nsb_variability (0.53) | 58.2 |
| L3 + L6 + L7 | 0.26 | 1.8 [0.37-21] | 0.28 | 0.89 | 93 / 1e+05 | nsb_variability / nsb_variability (0.49) | 58.2 |
| non-specific binding x25 (S1) | 27 | 1.4e+02 [7.8-8.5e+03] | 0.00 | 0.07 | 4.6e+02 / 1e+05 | nsb_variability / nsb_variability (0.74) | 58.2 |
| no decay in the reservoir: background 1e-5 of the substrate at the time of use | 1.3 | 9.9 [0.89-6.4e+02] | 0.06 | 0.50 | 2.7e+02 / 1e+05 | nsb_variability / substrate_background (0.50) | 58.2 |
| no decay and screened reagents (L6 + L7) | 0.44 | 3.4 [0.52-46] | 0.16 | 0.76 | 93 / 1e+05 | nsb_variability / nsb_variability (0.54) | 58.2 |
| background 1e-3 of the substrate, no decay (S4a) | 58 | 1.4e+02 [10-6.4e+03] | 0.00 | 0.05 | 2.7e+02 / 1e+05 | substrate_background / substrate_background (0.98) | 58.2 |
| blank contamination up to 1 pg/mL | 1.1 | 5.8 [0.94-2.8e+02] | 0.06 | 0.61 | 2.7e+02 / 1e+05 | nsb_variability / nsb_variability (0.58) | 58.2 |
| only 1 % of the turnovers give an electroactive product (review C1) | 42 | 88 [7.4-3.5e+03] | 0.00 | 0.08 | 3.4e+04 / 1e+05 | baseline_drift / baseline_drift (0.59) | 58.2 |
| only 1 % of the turnovers electroactive, and no decay in the reservoir | 73 | 3e+02 [15-2.7e+04] | 0.00 | 0.03 | 3.4e+04 / 1e+05 | substrate_background / substrate_background (0.71) | 58.2 |
| only 0.1 % of the turnovers give an electroactive product | 4.2e+02 | 8.5e+02 [64-3.4e+04] | 0.00 | 0.00 | 1e+05 / 1e+05 | baseline_drift / baseline_drift (0.62) | 58.2 |

## 3. Tier 1 - alternatives and hardware cases

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | upper limit by the slope criterion / curve rises up to (pg/mL) | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| primary: printed gold AU10, strip-cell gap 0.20 mm, read 60 s at 200 uL/min, 0.3 mM substrate, 20 nM conjugate | 3.6 | 16 [2.8-1.1e+02] | 0.00 | 0.33 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.68) | 57.1 |
| printed carbon C21 with adsorbed streptavidin (same cell and read) | 11 | 32 [4.4-3.4e+02] | 0.00 | 0.17 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.80) | 57.1 |
| thin-film gold chip SE1 in the thin-film cell (same read) | 4.1 | 21 [3.3-1.6e+02] | 0.00 | 0.27 | 1e+05 / 1e+05 | baseline_drift / nsb_variability (0.47) | 57.1 |
| strip-cell gap 0.10 mm | 2.8 | 13 [2.3-1e+02] | 0.01 | 0.39 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.70) | 57.1 |
| strip-cell gap 0.50 mm | 5.6 | 22 [3.9-1.6e+02] | 0.00 | 0.23 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.65) | 57.1 |
| read at 80 uL/min (load 41 min) | 5.9 | 25 [4.2-1.9e+02] | 0.00 | 0.20 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.61) | 57.4 |
| read at 40 uL/min (load 36 min) | 11 | 42 [7-4.2e+02] | 0.00 | 0.10 | 1e+05 / 1e+05 | baseline_drift / nsb_variability (0.52) | 57.8 |
| read at 300 uL/min | 3.2 | 14 [2.5-1e+02] | 0.00 | 0.37 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.69) | 56.4 |
| read 120 s at 150 uL/min, 10 nM conjugate, load 42 min (operating point of Revision B) | 5.7 | 22 [3.5-1.8e+02] | 0.00 | 0.24 | 1e+05 / 1e+05 | baseline_drift / baseline_drift (0.50) | 56.9 |
| conjugate 10 nM | 4.1 | 18 [2.9-1.4e+02] | 0.00 | 0.31 | 1e+05 / 1e+05 | baseline_drift / nsb_variability (0.52) | 57.1 |
| conjugate 40 nM | 4.5 | 18 [3.3-1.3e+02] | 0.00 | 0.29 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.81) | 57.1 |
| substrate 0.1 mM | 4.2 | 19 [3.2-1.4e+02] | 0.00 | 0.29 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.57) | 57.1 |
| substrate 1 mM | 3.5 | 15 [2.7-1.2e+02] | 0.00 | 0.34 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.70) | 57.1 |
| stopped read (needs a zero-flow row), 30 s wait + 120 s | 13 | 49 [7.5-4.6e+02] | 0.00 | 0.08 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.65) | 56.9 |
| transfer line 0.127 mm x 20 cm instead of 0.05 mm x 15 cm | 4.6 | 20 [3.4-1.4e+02] | 0.00 | 0.26 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.75) | 57.1 |
| no pre-read on the electrode | 4 | 18 [3.4-1.3e+02] | 0.00 | 0.30 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.59) | 57.1 |
| stop-and-go loading: 13 portions of 10 uL held 190 s each (needs a zero-flow row) | 6 | 23 [4-1.6e+02] | 0.00 | 0.22 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.68) | 57.1 |
| coated gold delivers 30 % of the transport-limited current | 7.2 | 19 [3.5-1.2e+02] | 0.00 | 0.29 | 1e+05 / 1e+05 | baseline_drift / nsb_variability (0.59) | 57.1 |
| detection conjugate with 5 [2-10] enzymes per antibody (poly-enzyme label, UNVERIFIED reagent; binding and non-specific count per conjugate unchanged) | 3.1 | 11 [1.9-87] | 0.01 | 0.47 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.90) | 57.1 |
| printed carbon C21, stopped read | 27 | 76 [10-8.8e+02] | 0.00 | 0.05 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.74) | 56.9 |
| reference windows in wash buffer pH 7.5: background step of 100 pA against the substrate buffer | 4.9 | 25 [4.7-1.7e+02] | 0.00 | 0.19 | 1e+05 / 1e+05 | substrate_background / substrate_background (0.53) | 57.1 |
| reference windows in wash buffer pH 7.5: background step of 300 pA | 11 | 48 [8-3.7e+02] | 0.00 | 0.08 | 1e+05 / 1e+05 | substrate_background / substrate_background (0.78) | 57.1 |
| substrate 1 mM, no decay in the reservoir | 13 | 51 [6-9.5e+02] | 0.00 | 0.12 | 1e+05 / 1e+05 | substrate_background / substrate_background (0.68) | 57.1 |
| printed carbon C21, no decay in the reservoir | 15 | 78 [8.3-1.3e+03] | 0.00 | 0.06 | 1e+05 / 1e+05 | substrate_background / substrate_background (0.53) | 57.1 |
| no pre-read on the electrode, no decay in the reservoir | 18 | 58 [6.9-1.1e+03] | 0.00 | 0.09 | 1e+05 / 1e+05 | electrode_sensitivity / electrode_sensitivity (0.66) | 57.1 |

## 4. Tier 2 - alternatives and hardware cases

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | upper limit by the slope criterion / curve rises up to (pg/mL) | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| primary (strip-cell gap 0.20 mm) | 2.1 | 8.4 [1-1e+02] | 0.05 | 0.54 | 1.4e+03 / 1e+05 | nsb_variability / nsb_variability (0.97) | 56.7 |
| strip-cell gap 0.10 mm | 2.1 | 8.4 [1-1e+02] | 0.05 | 0.54 | 1.4e+03 / 1e+05 | nsb_variability / nsb_variability (0.97) | 56.7 |
| strip-cell gap 0.50 mm | 2.1 | 8.5 [1.1-1e+02] | 0.04 | 0.54 | 1.4e+03 / 1e+05 | nsb_variability / nsb_variability (0.96) | 56.7 |
| pump cannot stop: continuous read at 1 uL/min | 2.8 | 11 [1.5-1.2e+02] | 0.01 | 0.47 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.92) | 59.2 |
| pump cannot stop and cannot go below 10 uL/min | 4.1 | 15 [2.2-1.5e+02] | 0.01 | 0.37 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.83) | 59.2 |
| bed binds conjugate like beads washed in tubes (factor 1 instead of 3) | 1.6 | 6.5 [0.82-76] | 0.07 | 0.62 | 1.4e+03 / 1e+05 | nsb_variability / nsb_variability (0.95) | 56.7 |
| retainer wetted area 1 mm2 instead of 5 mm2 | 1.7 | 7.3 [0.89-89] | 0.06 | 0.58 | 1.4e+03 / 1e+05 | nsb_variability / nsb_variability (0.96) | 56.7 |
| retainer wetted area 20 mm2 (0.5 mm silicate frit) | 3.4 | 13 [1.4-1.5e+02] | 0.03 | 0.43 | 1.4e+03 / 1e+05 | nsb_variability / nsb_variability (0.98) | 56.7 |
| no conjugate-exposed wall upstream of the bed (bound) | 1.1 | 4.4 [0.67-53] | 0.11 | 0.71 | 1.4e+03 / 1e+05 | nsb_variability / nsb_variability (0.91) | 56.7 |
| transfer line 0.127 mm x 20 cm | 3.5 | 14 [1.5-1.8e+02] | 0.02 | 0.41 | 1.4e+03 / 1e+05 | nsb_variability / nsb_variability (0.99) | 56.7 |
| transfer line 0.025 mm x 15 cm | 1.8 | 7.3 [0.93-85] | 0.06 | 0.59 | 1.4e+03 / 1e+05 | nsb_variability / nsb_variability (0.96) | 56.7 |
| walls above the bed bind like blocked beads (tubing factor 1, e.g. a coated capillary) | 1.4 | 5.1 [0.77-61] | 0.09 | 0.67 | 1.4e+03 / 1e+05 | nsb_variability / nsb_variability (0.93) | 56.7 |
| bed in a fitting on the inlet port (whole bore between bed and electrode) | 2.3 | 9.7 [1.2-1.2e+02] | 0.04 | 0.50 | 1.4e+03 / 1e+05 | nsb_variability / nsb_variability (0.97) | 56.7 |
| half the beads (5e5) | 2.5 | 11 [1.2-1.4e+02] | 0.04 | 0.47 | 2.3e+03 / 1e+05 | nsb_variability / nsb_variability (0.97) | 56.7 |
| twice the beads (2e6) | 2.3 | 8.1 [1.1-91] | 0.05 | 0.55 | 1.4e+03 / 1e+05 | nsb_variability / nsb_variability (0.97) | 56.7 |
| stop 7 min instead of 5 (load 35 min) | 2.1 | 8.7 [1-1.1e+02] | 0.05 | 0.53 | 4.6e+02 / 1e+05 | nsb_variability / nsb_variability (0.97) | 56.7 |
| stop 3 min instead of 5 (load 39 min) | 2 | 8.2 [1-99] | 0.05 | 0.55 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.96) | 56.7 |
| stop 30 s | 2.1 | 8.8 [1.2-96] | 0.04 | 0.54 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.93) | 52.2 |
| parked read instead of swept | 2.8 | 12 [1.4-1.4e+02] | 0.02 | 0.46 | 2.7e+02 / 1e+05 | nsb_variability / nsb_variability (0.97) | 57.2 |
| conjugate 10 nM | 2.3 | 9.5 [1.1-1.1e+02] | 0.04 | 0.51 | 7.9e+02 / 1e+05 | nsb_variability / nsb_variability (0.98) | 56.7 |
| conjugate 3 nM | 2 | 8.2 [1-97] | 0.05 | 0.56 | 2.3e+03 / 1e+05 | nsb_variability / nsb_variability (0.95) | 56.7 |
| conjugate 3 nM, stop 3 min, load 39 min (lowest nominal) | 2 | 8 [1-93] | 0.05 | 0.56 | 1e+05 / 1e+05 | nsb_variability / nsb_variability (0.94) | 56.7 |
| the same, only 1 % of the turnovers electroactive | 27 | 50 [7-5.4e+02] | 0.00 | 0.09 | 1e+05 / 1e+05 | baseline_drift / baseline_drift (0.47) | 56.7 |

## 5. Tier 3 - alternatives

| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | upper limit by the slope criterion / curve rises up to (pg/mL) | limiting term nominal / most frequent in Monte Carlo (share) | min to result |
|---|---|---|---|---|---|---|---|
| one valve, no transfer (primary of tier 3) | 1.2 | 5.1 [0.78-58] | 0.09 | 0.69 | 2.7e+02 / 1e+05 | nsb_variability / nsb_variability (0.91) | 56.7 |
| one valve, accumulation 7 min instead of 3 (load 36 min) | 1.3 | 5.4 [0.76-64] | 0.09 | 0.67 | 93 / 1e+05 | nsb_variability / nsb_variability (0.93) | 56.7 |
| one valve, conjugate 10 nM | 1.4 | 5.6 [0.8-64] | 0.08 | 0.66 | 1.6e+02 / 1e+05 | nsb_variability / nsb_variability (0.94) | 56.7 |
| one valve, conjugate 3 nM | 1.2 | 4.9 [0.79-55] | 0.09 | 0.69 | 4.6e+02 / 1e+05 | nsb_variability / nsb_variability (0.88) | 56.7 |
| one valve, loop walls 30 mm2 instead of 10 mm2 | 1.7 | 7.3 [0.93-82] | 0.06 | 0.60 | 2.7e+02 / 1e+05 | nsb_variability / nsb_variability (0.95) | 56.7 |
| transfer as specified (release 0.35 [0.05-0.74], read bed of three times the beads) | 1.1 | 5.8 [0.64-2.8e+02] | 0.12 | 0.61 | 2.7e+02 / 1e+05 | nsb_variability / nsb_variability (0.62) | 58.2 |
| transfer: release 0.7 in 5 min, as docs/05 assumed for its tube protocol | 0.53 | 2 [0.37-87] | 0.28 | 0.81 | 1.6e+02 / 1e+05 | nsb_variability / nsb_variability (0.56) | 58.2 |
| transfer: release 0.74, non-specific x0.01 (optimistic bounds) | 0.24 | 1.1 [0.24-27] | 0.47 | 0.90 | 1.6e+02 / 1e+05 | baseline_drift / substrate_background (0.42) | 58.2 |
| transfer: release 0.05, non-specific x0.5 (pessimistic bounds) | 34 | 1.2e+02 [9.7-4.8e+03] | 0.00 | 0.05 | 2.3e+03 / 1e+05 | nsb_variability / nsb_variability (0.98) | 58.2 |
| transfer with desthiobiotin and biotin, 5 min (release 0.1 [0.003-0.26]) | 3.7 | 32 [1.9-2.1e+03] | 0.02 | 0.28 | 7.9e+02 / 1e+05 | nsb_variability / nsb_variability (0.66) | 58.2 |
| transfer, release 0.7, read bed the same size as the capture bed (sites/feed 1.2) | 0.65 | 3.4 [0.46-1.5e+02] | 0.20 | 0.72 | 1.6e+02 / 1e+05 | nsb_variability / nsb_variability (0.60) | 58.2 |
| transfer, release 0.7, same size, capture bed coated at the vendor's capacity (sites/feed 0.36) | 1.5 | 7.4 [0.81-3.3e+02] | 0.08 | 0.56 | 2.7e+02 / 1e+05 | nsb_variability / nsb_variability (0.64) | 58.2 |
| transfer, screened reagents (L6 + L7) | 0.43 | 3 [0.48-42] | 0.19 | 0.79 | 93 / 1e+05 | nsb_variability / nsb_variability (0.60) | 58.2 |
| transfer, release 0.7, screened reagents (L6 + L7) | 0.21 | 1.2 [0.29-11] | 0.41 | 0.94 | 54 / 1e+05 | nsb_variability / nsb_variability (0.51) | 58.2 |
| transfer + screened reagents + F(ab')2 credit (L3 + L6 + L7) | 0.26 | 1.8 [0.37-21] | 0.28 | 0.89 | 93 / 1e+05 | nsb_variability / nsb_variability (0.49) | 58.2 |
| the same with a reference channel (L5) | 0.24 | 1.7 [0.36-19] | 0.30 | 0.90 | 93 / 1e+05 | baseline_drift / nsb_variability (0.45) | 58.2 |

## 6. One-at-a-time sensitivity of the three implementations

LOD (pg/mL) with one parameter at its low and at its high bound, all others at their best estimate; the twelve largest swings.


**Tier 1: capture on a printed gold strip, read at the electrode under fast substrate flow** (nominal 3.6 pg/mL)

| Parameter | value [low-high] | LOD at low | LOD at high |
|---|---|---|---|
| `chem.antibodies.koff_detection` | 0.00086 [3e-06-0.0083] 1/s | 2.6 | 61 |
| `chem.nsb.nsb_effective_rate_constant` | 4e-11 [8e-12-4e-10] m/s | 2.1 | 30 |
| `tr.nsb.surface_factor_gold_oeg` | 3 [1-30] fold | 2.5 | 23 |
| `chem.enzymes.alp.kcat_conjugate_assay_conditions` | 1000 [100-6000] 1/s | 20 | 3.1 |
| `ma.nsb.label_factor_igg_enzyme_conjugate` | 0.04 [0.01-0.15] fold | 2.1 | 12 |
| `tr.detection.monolayer_collection_efficiency` | 1 [0.1-1] fraction | 20 | 3.6 |
| `chem.antibodies.kon_detection` | 390000 [90000-1.2e+06] 1/(M*s) | 11 | 2.3 |
| `tr.nsb.unit_to_unit_cv_planar` | 0.15 [0.05-0.4] fraction | 2.8 | 7.1 |
| `ma.labelling.detection_on_capture_residual_factor` | 1 [1-3] fold | 3.6 | 9.3 |
| `ma.delivery.adsorptive_loss_fraction_with_carrier` | 0.2 [0.02-0.6] fraction lost | 3 | 7.2 |
| `ma.chemistries.alp_hqdp.hydrolysis_rate` | 1e-10 [1e-12-1e-08] 1/s | 3.6 | 8.2 |
| `ma.nsb.surface_factor_tubing` | 3 [1-30] fold | 3.4 | 7.4 |

**Tier 2: capillary micro-bed above a printed carbon strip, stop and sweep** (nominal 2.1 pg/mL)

| Parameter | value [low-high] | LOD at low | LOD at high |
|---|---|---|---|
| `chem.antibodies.koff_detection` | 0.00086 [3e-06-0.0083] 1/s | 1.3 | 94 |
| `chem.nsb.nsb_effective_rate_constant` | 4e-11 [8e-12-4e-10] m/s | 0.43 | 22 |
| `ma.nsb.label_factor_igg_enzyme_conjugate` | 0.04 [0.01-0.15] fold | 0.53 | 7.9 |
| `chem.antibodies.kon_detection` | 390000 [90000-1.2e+06] 1/(M*s) | 8.2 | 0.84 |
| `ma.nsb.surface_factor_tubing` | 3 [1-30] fold | 1.4 | 11 |
| `ma.nsb.surface_factor_packed_bed` | 3 [1-30] fold | 1.6 | 7.9 |
| `tr.nsb.surface_factor_frit` | 10 [1-100] fold | 1.7 | 6 |
| `chem.surfaces.igg_surface_density_monolayer` | 1e+16 [2e+15-1.5e+16] molecules/m^2 | 5.6 | 1.8 |
| `ma.labelling.detection_on_capture_residual_factor` | 1 [1-3] fold | 2.1 | 6.3 |
| `tr.nsb.unit_to_unit_cv_bed` | 0.1 [0.03-0.3] fraction | 1.6 | 4.5 |
| `ma.delivery.adsorptive_loss_fraction_with_carrier` | 0.2 [0.02-0.6] fraction lost | 1.7 | 4.1 |
| `chem.antibodies.kon_capture` | 300000 [90000-1.2e+06] 1/(M*s) | 4.1 | 1.7 |

**Tier 3: the capture bed in the loop of one valve** (nominal 1.2 pg/mL)

| Parameter | value [low-high] | LOD at low | LOD at high |
|---|---|---|---|
| `chem.antibodies.koff_detection` | 0.00086 [3e-06-0.0083] 1/s | 0.84 | 36 |
| `chem.nsb.nsb_effective_rate_constant` | 4e-11 [8e-12-4e-10] m/s | 0.32 | 13 |
| `ma.nsb.label_factor_igg_enzyme_conjugate` | 0.04 [0.01-0.15] fold | 0.37 | 4.8 |
| `chem.antibodies.kon_detection` | 390000 [90000-1.2e+06] 1/(M*s) | 5 | 0.51 |
| `ma.nsb.surface_factor_packed_bed` | 3 [1-30] fold | 0.86 | 6.8 |
| `tr.nsb.surface_factor_frit` | 10 [1-100] fold | 0.89 | 5 |
| `ma.nsb.surface_factor_tubing` | 3 [1-30] fold | 1.1 | 3.5 |
| `ma.labelling.detection_on_capture_residual_factor` | 1 [1-3] fold | 1.2 | 3.8 |
| `chem.surfaces.igg_surface_density_monolayer` | 1e+16 [2e+15-1.5e+16] molecules/m^2 | 3.3 | 1.1 |
| `tr.nsb.unit_to_unit_cv_bed` | 0.1 [0.03-0.3] fraction | 0.95 | 2.7 |
| `ma.delivery.adsorptive_loss_fraction_with_carrier` | 0.2 [0.02-0.6] fraction lost | 1 | 2.5 |
| `chem.antibodies.kon_capture` | 300000 [90000-1.2e+06] 1/(M*s) | 2.4 | 1.1 |

**Tier 3 with the immune-complex transfer to a second bed** (nominal 1.1 pg/mL)

| Parameter | value [low-high] | LOD at low | LOD at high |
|---|---|---|---|
| `chem.antibodies.koff_detection` | 0.00086 [3e-06-0.0083] 1/s | 0.38 | 8.1e+03 |
| `chem.nsb.nsb_effective_rate_constant` | 4e-11 [8e-12-4e-10] m/s | 0.47 | 10 |
| `tr.transfer.elution_efficiency` | 0.35 [0.05-0.74] fraction | 7.5 | 0.5 |
| `ma.design_levers.immune_complex_transfer_nsb_factor` | 0.1 [0.01-0.5] fold | 0.51 | 4.8 |
| `ma.nsb.label_factor_igg_enzyme_conjugate` | 0.04 [0.01-0.15] fold | 0.49 | 3.7 |
| `chem.antibodies.kon_detection` | 390000 [90000-1.2e+06] 1/(M*s) | 3.9 | 0.52 |
| `ma.nsb.surface_factor_packed_bed` | 3 [1-30] fold | 0.81 | 5.1 |
| `chem.surfaces.igg_surface_density_monolayer` | 1e+16 [2e+15-1.5e+16] molecules/m^2 | 4.2 | 0.9 |
| `tr.nsb.surface_factor_frit` | 10 [1-100] fold | 0.83 | 3.8 |
| `chem.enzymes.alp.kcat_conjugate_assay_conditions` | 1000 [100-6000] 1/s | 4.3 | 1 |
| `chem.antibodies.kon_capture` | 300000 [90000-1.2e+06] 1/(M*s) | 2.6 | 0.76 |
| `ma.nsb.surface_factor_tubing` | 3 [1-30] fold | 0.94 | 2.9 |

## 7. Step tables used for the timing


**Tier 1: capture on a printed gold strip, read at the electrode under fast substrate flow** - 57.1 min from Inject Start to result

| Step | min | counts |
|---|---|---|
| pre-run: cleaning injection, hydroquinone locator plug, the same read sequence on the fresh electrode | 12.0 | no (before injection) |
| sample injection (SM-FL aspirate and load) | 1.0 | yes |
| sample pumped through the cell | 44.0 | yes |
| wash 1 (Loop Offline at its start) | 1.5 | yes |
| conjugate injection (SM-FL) | 1.0 | yes |
| conjugate through the cell, two loop volumes, then Loop Offline | 4.0 | yes |
| wash 2 at the read flow in substrate buffer without substrate; its last 30 s are the first reference window | 2.0 | yes |
| substrate front (BSM A2 -> B1 at the read flow) | 1.1 | yes |
| read window, substrate flowing | 1.0 | yes |
| front back to the substrate buffer without substrate (B1 -> A2) | 1.1 | yes |
| second reference window | 0.5 | yes |

**Tier 2: capillary micro-bed above a printed carbon strip, stop and sweep** - 56.7 min from Inject Start to result

| Step | min | counts |
|---|---|---|
| pre-run: cleaning injection; the same substrate step, stop and sweep on the fresh bed and strip; back to buffer | 17.0 | no (before injection) |
| sample injection (SM-FL aspirate and load) | 1.0 | yes |
| sample pumped through the bed | 37.0 | yes |
| wash 1 (Loop Offline at its start) | 1.5 | yes |
| conjugate injection (SM-FL) | 1.0 | yes |
| conjugate through the bed, two loop volumes, then Loop Offline | 4.0 | yes |
| wash 2 | 2.0 | yes |
| step to substrate, 215 uL at 80 uL/min | 2.7 | yes |
| step down to 5 uL/min so that the pump pressure relaxes | 1.0 | yes |
| accumulation: product collects in the bed | 5.0 | yes |
| sweep over the electrode and read | 1.5 | yes |

**Tier 3: the capture bed in the loop of one valve** - 56.7 min from Inject Start to result

| Step | min | counts |
|---|---|---|
| pre-run: cleaning injection; substrate over the strip with the beds bypassed (response check); back to buffer | 10.0 | no (before injection) |
| sample injection (SM-FL aspirate and load) | 1.0 | yes |
| sample pumped through the bed | 40.0 | yes |
| wash 1 (Loop Offline at its start) | 1.5 | yes |
| conjugate injection (SM-FL) | 1.0 | yes |
| conjugate through the bed, two loop volumes, then Loop Offline | 4.0 | yes |
| wash 2 | 2.0 | yes |
| step to substrate, 215 uL at 80 uL/min | 2.7 | yes |
| accumulation: product collects in the bed, closed by its valve; the cell stays in flow | 3.0 | yes |
| sweep over the electrode and read | 1.5 | yes |

**Tier 3 with the immune-complex transfer to a second bed** - 58.2 min from Inject Start to result

| Step | min | counts |
|---|---|---|
| pre-run: cleaning injection; substrate over the strip with the beds bypassed (response check); back to buffer | 10.0 | no (before injection) |
| sample injection (SM-FL aspirate and load) | 1.0 | yes |
| sample pumped through the bed | 25.0 | yes |
| wash 1 (Loop Offline at its start) | 1.5 | yes |
| conjugate injection (SM-FL) | 1.0 | yes |
| conjugate through the bed, two loop volumes, then Loop Offline | 4.0 | yes |
| wash 2 | 2.0 | yes |
| eluent injection (1), eluent to bed 1 (0.5), hold with bed 1 closed (5; the last minute at the push flow), push through bed 2 (4), wash of bed 2 (2) | 12.5 | yes |
| step to substrate, 215 uL at 80 uL/min | 2.7 | yes |
| accumulation: product collects in the bed, closed by its valve; the cell stays in flow | 7.0 | yes |
| sweep over the electrode and read | 1.5 | yes |
