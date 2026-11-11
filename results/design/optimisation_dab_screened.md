
### Scenario: dab_screened (n = 2000, seed 20261111; optimiser n = 300)

| Design | LOD nominal (pg/mL) | LOD MC median [5-95 %] (pg/mL) | P(LOD<=1) | P(LOD<=1 and ULOQ>=1000) | ULOQ nominal (pg/mL) | Time to result (min) |
|---|---|---|---|---|---|---|
| OS baseline (B-mag1-IDA/alp_hqdp) | 0.25 | 1.3 [0.35-9.7] | 0.36 | 0.30 | 6.1e+02 | 51.5 |
| **OS optimised** | 0.14 | 0.95 [0.24-6.2] | 0.54 | 0.49 | 1e+03 | 59.0 |
| OS optimised, detector thin_layer | 0.14 | 1 [0.24-7.3] | 0.50 | 0.46 | 1e+03 | 59.0 |
| OS optimised, detector coulometric | 0.16 | 1.1 [0.31-7.2] | 0.46 | 0.42 | 1e+03 | 59.0 |
| OS optimised, detector wall_jet_sencell | 1.2 | 2.4 [0.54-18] | 0.18 | 0.15 | 1e+03 | 59.0 |
| SQ baseline (B-mag-IDA/alp_hqdp) | 2 | 10 [1.3-1.1e+02] | 0.03 | 0.03 | 8.9e+03 | 60.5 |
| **SQ optimised** | 0.39 | 2 [0.45-19] | 0.25 | 0.24 | 1.4e+03 | 60.0 |
| SQ optimised, detector thin_layer | 0.45 | 2.5 [0.48-21] | 0.20 | 0.18 | 1.4e+03 | 60.0 |
| SQ optimised, detector coulometric | 0.44 | 2.5 [0.56-20] | 0.18 | 0.17 | 1.4e+03 | 60.0 |
| SQ optimised, detector wall_jet_sencell | 4.7 | 9.1 [1.3-75] | 0.03 | 0.02 | 1.4e+03 | 60.0 |
| FRB baseline (B-bed-IDA/alp_hqdp) | 15 | 38 [4.5-4.4e+02] | 0.00 | 0.00 | 4e+03 | 33.5 |
| **FRB optimised** | 0.8 | 3 [0.56-34] | 0.16 | 0.13 | 1e+03 | 42.3 |
| FRB optimised, detector thin_layer | 1.2 | 4.5 [0.88-37] | 0.07 | 0.06 | 1e+03 | 42.3 |
| FRB optimised, detector coulometric | 1.9 | 6.8 [1.2-59] | 0.03 | 0.02 | 1e+03 | 42.3 |
| FRB optimised, detector wall_jet_sencell | 24 | 34 [5.2-3.4e+02] | 0.00 | 0.00 | 1e+03 | 42.3 |
| FRC baseline (C-bed-IDA/alp_hqdp) | 6.8 | 29 [2.9-3.4e+02] | 0.00 | 0.00 | 1.8e+03 | 33.5 |
| **FRC optimised** | 1.5 | 6.7 [0.94-78] | 0.06 | 0.05 | 1e+03 | 35.5 |
