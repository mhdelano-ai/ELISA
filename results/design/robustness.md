## Robustness of the optimised designs under the open scenarios

n = 2000 Monte Carlo draws, seed 20261111. Success = LOD <= 1 pg/mL and ULOQ >= 1000 pg/mL.

| Design | Scenario | LOD nominal | LOD median [5-95 %] | P(LOD<=1) | P(success) | time to result (min) |
|---|---|---|---|---|---|---|
| OS-base | S0 audited baseline | 0.56 | 2.1 [0.44-36] | 0.25 | 0.21 | 51.5 |
| OS-base | S1 old NSB rate (label factor 1.0, 0.3-3; x25) | 14 | 45 [4.3-7.8e+02] | 0.00 | 0.00 | 51.5 |
| OS-base | S2a detection reagent screened (koff 1e-4, <=1.9e-4 /s) | 0.25 | 1.3 [0.35-9.7] | 0.36 | 0.30 | 51.5 |
| OS-base | S2b capture reagent unscreened (koff to 8.3e-3 /s) | 0.56 | 2.9 [0.49-72] | 0.19 | 0.17 | 51.5 |
| OS-base | S3a NSB partly reversible, fraction removed by washes = ma.design_levers.nsb_fraction_removed_by_wash (OUTSIDE MODEL: label factor x(1-f)) | 0.3 | 1.3 [0.31-19] | 0.39 | 0.35 | 51.5 |
| OS-base | S3b NSB irreversible and surfaces at high bound (tubing factor 30) | 2.2 | 5.1 [0.74-97] | 0.09 | 0.08 | 51.5 |
| OS-base | S4a free HQ in substrate 1e-3 (high bound) | 4 | 8.9 [1.1-1.3e+02] | 0.04 | 0.02 | 51.5 |
| OS-base | S4b free HQ in substrate 1e-7 (low bound) | 0.56 | 1.9 [0.38-33] | 0.29 | 0.25 | 51.5 |
| OS-base | S5 <=100 uL DRAWN: PLNO 75 uL on the 100 uL loop | 0.57 | 2.2 [0.43-38] | 0.25 | 0.22 | 51.5 |
| OS-base | S6 worst plausible: S1 + S4a | 14 | 52 [5.9-8.6e+02] | 0.00 | 0.00 | 51.5 |
| OS-base | S7 favourable: S2a + S4b | 0.25 | 1.2 [0.3-9.1] | 0.42 | 0.35 | 51.5 |
| OS-opt | S0 audited baseline | 0.32 | 1.3 [0.3-21] | 0.38 | 0.35 | 59.5 |
| OS-opt | S1 old NSB rate (label factor 1.0, 0.3-3; x25) | 7.9 | 23 [2.3-4.1e+02] | 0.01 | 0.01 | 59.5 |
| OS-opt | S2a detection reagent screened (koff 1e-4, <=1.9e-4 /s) | 0.14 | 0.94 [0.24-6.1] | 0.55 | 0.50 | 59.5 |
| OS-opt | S2b capture reagent unscreened (koff to 8.3e-3 /s) | 0.32 | 1.8 [0.38-48] | 0.30 | 0.28 | 59.5 |
| OS-opt | S3a NSB partly reversible, fraction removed by washes = ma.design_levers.nsb_fraction_removed_by_wash (OUTSIDE MODEL: label factor x(1-f)) | 0.17 | 0.99 [0.22-13] | 0.51 | 0.48 | 59.5 |
| OS-opt | S3b NSB irreversible and surfaces at high bound (tubing factor 30) | 0.51 | 1.7 [0.37-29] | 0.32 | 0.29 | 59.5 |
| OS-opt | S4a free HQ in substrate 1e-3 (high bound) | 6.2 | 11 [1.2-1.8e+02] | 0.04 | 0.03 | 59.5 |
| OS-opt | S4b free HQ in substrate 1e-7 (low bound) | 0.32 | 1.1 [0.27-18] | 0.44 | 0.42 | 59.5 |
| OS-opt | S5 <=100 uL DRAWN: PLNO 75 uL on the 100 uL loop | 0.33 | 1.4 [0.32-27] | 0.36 | 0.35 | 59.5 |
| OS-opt | S6 worst plausible: S1 + S4a | 10 | 33 [4.3-5.1e+02] | 0.00 | 0.00 | 59.5 |
| OS-opt | S7 favourable: S2a + S4b | 0.13 | 0.8 [0.19-4.5] | 0.61 | 0.57 | 59.5 |
| SQ-opt | S0 audited baseline | 0.3 | 1.5 [0.37-12] | 0.33 | 0.31 | 58.5 |
| SQ-opt | S1 old NSB rate (label factor 1.0, 0.3-3; x25) | 7.5 | 28 [3.4-2.6e+02] | 0.00 | 0.00 | 58.5 |
| SQ-opt | S2a detection reagent screened (koff 1e-4, <=1.9e-4 /s) | 0.25 | 1.3 [0.35-9.9] | 0.38 | 0.34 | 58.5 |
| SQ-opt | S2b capture reagent unscreened (koff to 8.3e-3 /s) | 0.3 | 2.1 [0.43-63] | 0.24 | 0.23 | 58.5 |
| SQ-opt | S3a NSB partly reversible, fraction removed by washes = ma.design_levers.nsb_fraction_removed_by_wash (OUTSIDE MODEL: label factor x(1-f)) | 0.16 | 1 [0.26-7.3] | 0.48 | 0.45 | 58.5 |
| SQ-opt | S3b NSB irreversible and surfaces at high bound (tubing factor 30) | 1.3 | 3.5 [0.66-32] | 0.12 | 0.10 | 58.5 |
| SQ-opt | S4a free HQ in substrate 1e-3 (high bound) | 3.7 | 8.5 [1.2-75] | 0.03 | 0.02 | 58.5 |
| SQ-opt | S4b free HQ in substrate 1e-7 (low bound) | 0.3 | 1.3 [0.3-11] | 0.39 | 0.36 | 58.5 |
| SQ-opt | S5 <=100 uL DRAWN: PLNO 75 uL on the 100 uL loop | 0.35 | 1.7 [0.38-15] | 0.30 | 0.28 | 58.5 |
| SQ-opt | S6 worst plausible: S1 + S4a | 8.4 | 35 [5.9-2.8e+02] | 0.00 | 0.00 | 58.5 |
| SQ-opt | S7 favourable: S2a + S4b | 0.25 | 1.1 [0.27-8.2] | 0.44 | 0.41 | 58.5 |
| FRB-opt | S0 audited baseline | 0.94 | 3.6 [0.6-42] | 0.14 | 0.12 | 51.5 |
| FRB-opt | S1 old NSB rate (label factor 1.0, 0.3-3; x25) | 24 | 82 [8.4-1.1e+03] | 0.00 | 0.00 | 51.5 |
| FRB-opt | S2a detection reagent screened (koff 1e-4, <=1.9e-4 /s) | 0.78 | 3.1 [0.55-34] | 0.16 | 0.14 | 51.5 |
| FRB-opt | S2b capture reagent unscreened (koff to 8.3e-3 /s) | 0.94 | 5.1 [0.67-1.2e+02] | 0.11 | 0.09 | 51.5 |
| FRB-opt | S3a NSB partly reversible, fraction removed by washes = ma.design_levers.nsb_fraction_removed_by_wash (OUTSIDE MODEL: label factor x(1-f)) | 0.49 | 2.1 [0.44-23] | 0.24 | 0.22 | 51.5 |
| FRB-opt | S3b NSB irreversible and surfaces at high bound (tubing factor 30) | 1.8 | 5.5 [0.84-57] | 0.07 | 0.06 | 51.5 |
| FRB-opt | S4a free HQ in substrate 1e-3 (high bound) | 4 | 12 [1.7-1.1e+02] | 0.02 | 0.01 | 51.5 |
| FRB-opt | S4b free HQ in substrate 1e-7 (low bound) | 0.94 | 3.3 [0.55-39] | 0.16 | 0.14 | 51.5 |
| FRB-opt | S5 <=100 uL DRAWN: PLNO 75 uL on the 100 uL loop | 1.3 | 4.9 [0.67-54] | 0.10 | 0.09 | 51.5 |
| FRB-opt | S6 worst plausible: S1 + S4a | 24 | 90 [11-1e+03] | 0.00 | 0.00 | 51.5 |
| FRB-opt | S7 favourable: S2a + S4b | 0.78 | 2.8 [0.5-32] | 0.19 | 0.17 | 51.5 |
| FRC-opt | S0 audited baseline | 0.95 | 3.8 [0.64-46] | 0.12 | 0.10 | 45.0 |
| FRC-opt | S1 old NSB rate (label factor 1.0, 0.3-3; x25) | 24 | 87 [9.3-1.2e+03] | 0.00 | 0.00 | 45.0 |
| FRC-opt | S2a detection reagent screened (koff 1e-4, <=1.9e-4 /s) | 0.79 | 3.4 [0.59-35] | 0.15 | 0.12 | 45.0 |
| FRC-opt | S2b capture reagent unscreened (koff to 8.3e-3 /s) | 0.95 | 5.4 [0.72-1.3e+02] | 0.09 | 0.07 | 45.0 |
| FRC-opt | S3a NSB partly reversible, fraction removed by washes = ma.design_levers.nsb_fraction_removed_by_wash (OUTSIDE MODEL: label factor x(1-f)) | 0.5 | 2.1 [0.48-25] | 0.22 | 0.20 | 45.0 |
| FRC-opt | S3b NSB irreversible and surfaces at high bound (tubing factor 30) | 0.95 | 3.8 [0.64-46] | 0.12 | 0.10 | 45.0 |
| FRC-opt | S4a free HQ in substrate 1e-3 (high bound) | 3.4 | 10 [1.6-80] | 0.01 | 0.01 | 45.0 |
| FRC-opt | S4b free HQ in substrate 1e-7 (low bound) | 0.95 | 3.6 [0.63-37] | 0.13 | 0.11 | 45.0 |
| FRC-opt | S5 <=100 uL DRAWN: PLNO 75 uL on the 100 uL loop | 1.3 | 4.9 [0.84-48] | 0.08 | 0.07 | 45.0 |
| FRC-opt | S6 worst plausible: S1 + S4a | 24 | 90 [11-9.4e+02] | 0.00 | 0.00 | 45.0 |
| FRC-opt | S7 favourable: S2a + S4b | 0.79 | 3 [0.57-29] | 0.16 | 0.13 | 45.0 |
