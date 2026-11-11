
### Scenario: baseline (n = 2000, seed 20261111; optimiser n = 300)

| Design | LOD nominal (pg/mL) | LOD MC median [5-95 %] (pg/mL) | P(LOD<=1) | P(LOD<=1 and ULOQ>=1000) | ULOQ nominal (pg/mL) | Time to result (min) |
|---|---|---|---|---|---|---|
| OS baseline (B-mag1-IDA/alp_hqdp) | 0.56 | 2.1 [0.44-36] | 0.25 | 0.21 | 1.4e+03 | 51.5 |
| **OS optimised** | 0.32 | 1.3 [0.3-21] | 0.38 | 0.35 | 1.8e+03 | 59.5 |
| OS optimised, detector thin_layer | 0.33 | 1.4 [0.31-25] | 0.35 | 0.33 | 1.8e+03 | 59.5 |
| OS optimised, detector coulometric | 0.36 | 1.6 [0.39-24] | 0.33 | 0.30 | 1.8e+03 | 59.5 |
| OS optimised, detector wall_jet_sencell | 2.4 | 3.8 [0.64-60] | 0.14 | 0.11 | 1.8e+03 | 59.5 |
| SQ baseline (B-mag-IDA/alp_hqdp) | 2.6 | 13 [1.4-1.5e+02] | 0.02 | 0.02 | 1.2e+04 | 60.5 |
| **SQ optimised** | 0.3 | 1.5 [0.37-12] | 0.33 | 0.31 | 1.4e+03 | 58.5 |
| SQ optimised, detector thin_layer | 0.36 | 1.8 [0.41-14] | 0.26 | 0.24 | 1.4e+03 | 58.5 |
| SQ optimised, detector coulometric | 0.49 | 2.3 [0.56-17] | 0.19 | 0.17 | 1.4e+03 | 58.5 |
| SQ optimised, detector wall_jet_sencell | 5.3 | 8.3 [1.4-69] | 0.02 | 0.01 | 1.4e+03 | 58.5 |
| FRB baseline (B-bed-IDA/alp_hqdp) | 19 | 49 [5.1-6e+02] | 0.00 | 0.00 | 5.2e+03 | 33.5 |
| **FRB optimised** | 0.94 | 3.6 [0.6-42] | 0.14 | 0.12 | 1.4e+03 | 51.5 |
| FRB optimised, detector thin_layer | 1.1 | 4.4 [0.78-43] | 0.08 | 0.07 | 1.4e+03 | 51.5 |
| FRB optimised, detector coulometric | 1.4 | 6.1 [1-58] | 0.05 | 0.03 | 1.4e+03 | 51.5 |
| FRB optimised, detector wall_jet_sencell | 15 | 23 [3.4-2.3e+02] | 0.00 | 0.00 | 1.4e+03 | 51.5 |
| FRC baseline (C-bed-IDA/alp_hqdp) | 8.7 | 34 [3.7-5e+02] | 0.00 | 0.00 | 1.8e+03 | 33.5 |
| **FRC optimised** | 0.95 | 3.8 [0.64-46] | 0.12 | 0.10 | 1e+03 | 45.0 |
| CAP baseline (B-cap-TL/alp_hqdp) | 25 | 88 [14-7.1e+02] | 0.00 | 0.00 | 2.6e+04 | 33.5 |
| **CAP optimised** | 2 | 6.7 [1.1-65] | 0.04 | 0.04 | 3e+03 | 50.0 |
| CAP optimised, detector ida_flow | 1.9 | 6.5 [0.91-68] | 0.06 | 0.06 | 3e+03 | 50.0 |
