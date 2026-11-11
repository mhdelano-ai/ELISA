# G1 decision table (bench-consistent evaluation; docs/08 B3)

Table 1: n = 2000, seed 20261111; Table 2: n = 1000. The label factor is entered as a bench value would be (`design_lib.apply_bench_values`, the code `elisa_auto.model_feedback` uses): coupled NSB factors pinned at nominal (4e-11 m/s, bead surface factor 1); every other parameter keeps its prior. Designs: `final_designs.designs()` default (thin-layer cell; chamber stirring factor sampled; 1/0.96 before P). L4 = immune-complex transfer, label factor x 0.1/0.7 (UNVERIFIED lever magnitude). Monte Carlo sampling noise on P: about +/-0.02 (95 %) at n = 2000, +/-0.03 at n = 1000.

Rule (design_lib.g1_decision, fixed before data): GO if max P over admissible designs >= 0.3; GO-WITH-LEVER if below that but max P including L4 >= 0.1; STOP otherwise.

## Table 1 - P(success) and median LOD (pg/mL) against the measured label factor

| label factor | tube blank-equivalent B (P-vial reference, pg/mL) | P-chamb: median / P | P-chamb + L4: median / P | S-chamb: median / P | S-chamb + L4: median / P | B-bed: median / P | B-bed + L4: median / P | G1 rule |
|---|---|---|---|---|---|---|---|---|
| 0.005 | 0.12 | 1.2 / 0.40 | 1.2 / 0.41 | 1.1 / 0.40 | 1.1 / 0.41 | 1.2 / 0.31 | 1.1 / 0.36 | GO |
| 0.01 | 0.24 | 1.3 / 0.37 | 1.2 / 0.41 | 1.2 / 0.36 | 1.1 / 0.41 | 1.4 / 0.25 | 1.1 / 0.35 | GO |
| 0.02 | 0.48 | 1.5 / 0.32 | 1.2 / 0.40 | 1.4 / 0.28 | 1.1 / 0.41 | 1.8 / 0.16 | 1.1 / 0.34 | GO |
| 0.03 | 0.72 | 1.8 / 0.27 | 1.2 / 0.40 | 1.6 / 0.22 | 1.1 / 0.40 | 2.3 / 0.11 | 1.2 / 0.32 | GO-WITH-LEVER |
| 0.04 | 0.96 | 2 / 0.23 | 1.2 / 0.40 | 1.9 / 0.17 | 1.1 / 0.39 | 2.7 / 0.08 | 1.2 / 0.30 | GO-WITH-LEVER |
| 0.05 | 1.2 | 2.3 / 0.19 | 1.2 / 0.39 | 2.2 / 0.14 | 1.1 / 0.38 | 3.2 / 0.07 | 1.3 / 0.28 | GO-WITH-LEVER |
| 0.06 | 1.4 | 2.5 / 0.17 | 1.3 / 0.38 | 2.4 / 0.12 | 1.2 / 0.37 | 3.6 / 0.05 | 1.3 / 0.27 | GO-WITH-LEVER |
| 0.08 | 1.9 | 3.1 / 0.12 | 1.3 / 0.37 | 3 / 0.07 | 1.2 / 0.35 | 4.5 / 0.03 | 1.4 / 0.24 | GO-WITH-LEVER |
| 0.1 | 2.4 | 3.6 / 0.10 | 1.4 / 0.35 | 3.5 / 0.04 | 1.2 / 0.33 | 5.4 / 0.02 | 1.5 / 0.21 | GO-WITH-LEVER (Stage 1C first; Stage-2 order waits for G1') |
| 0.12 | 2.9 | 4.2 / 0.08 | 1.4 / 0.33 | 4.1 / 0.03 | 1.3 / 0.30 | 6.4 / 0.02 | 1.7 / 0.18 | GO-WITH-LEVER (Stage 1C first; Stage-2 order waits for G1') |
| 0.15 | 3.6 | 5.1 / 0.05 | 1.5 / 0.31 | 4.9 / 0.02 | 1.4 / 0.27 | 7.8 / 0.01 | 1.9 / 0.15 | GO-WITH-LEVER (Stage 1C first; Stage-2 order waits for G1') |
| 0.2 | 4.8 | 6.5 / 0.03 | 1.7 / 0.28 | 6.2 / 0.01 | 1.6 / 0.23 | 10 / 0.00 | 2.2 / 0.12 | GO-WITH-LEVER (Stage 1C first; Stage-2 order waits for G1') |
| 0.3 | 7.2 | 9.2 / 0.01 | 2.1 / 0.22 | 8.9 / 0.00 | 2 / 0.17 | 15 / 0.00 | 2.8 / 0.08 | GO-WITH-LEVER (Stage 1C first; Stage-2 order waits for G1') |

Label-factor screen implied by Table 1 (other Stage-1 values at their priors): GO up to 0.02; STOP from none in the grid.

## Table 2 - G1a (U1 + U3): P(success) of P-chamb / S-chamb against label factor and free HQ

| label factor | free HQ 1e-06: P-chamb / S-chamb P | free HQ 1e-05: P-chamb / S-chamb P | free HQ 3e-05: P-chamb / S-chamb P | free HQ 0.0001: P-chamb / S-chamb P |
|---|---|---|---|---|
| 0.01 | 0.48 / 0.40 | 0.43 / 0.39 | 0.33 / 0.35 | 0.14 / 0.22 |
| 0.02 | 0.41 / 0.32 | 0.37 / 0.31 | 0.29 / 0.28 | 0.12 / 0.18 |
| 0.04 | 0.29 / 0.19 | 0.27 / 0.18 | 0.22 / 0.17 | 0.10 / 0.11 |
| 0.06 | 0.21 / 0.10 | 0.19 / 0.10 | 0.16 / 0.09 | 0.07 / 0.06 |
| 0.08 | 0.15 / 0.07 | 0.14 / 0.07 | 0.11 / 0.06 | 0.05 / 0.04 |
| 0.1 | 0.11 / 0.05 | 0.10 / 0.04 | 0.08 / 0.04 | 0.03 / 0.03 |
| 0.15 | 0.05 / 0.02 | 0.05 / 0.02 | 0.04 / 0.01 | 0.02 / 0.01 |
