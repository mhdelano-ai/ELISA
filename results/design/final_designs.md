# Final candidate designs under the decisive scenarios

n = 2000, seed 20261111. '~': chamber approximation (P computed before the 1/0.96 transfer factor, so slightly optimistic).

| Design | Scenario | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD<=1) | P(success) | ULOQ nominal | time to result (min) | constraint flags |
|---|---|---|---|---|---|---|---|---|
| P-vial | S0 audited baseline | 0.32 | 1.3 [0.3-21] | 0.38 | 0.35 | 1.8e+03 | 59.5 | ok |
| P-vial | S2a detection reagent screened (koff 1e-4, <=1.9e-4 /s) | 0.14 | 0.94 [0.24-6.1] | 0.55 | 0.50 | 7.9e+02 | 59.5 | nominal ULOQ 794 < 1000 pg/mL |
| P-vial | S2b capture reagent unscreened (koff to 8.3e-3 /s) | 0.32 | 1.8 [0.38-48] | 0.30 | 0.28 | 1.8e+03 | 59.5 | ok |
| P-vial | S1 old NSB rate (label factor 1.0, 0.3-3; x25) | 7.9 | 23 [2.3-4.1e+02] | 0.01 | 0.01 | 1.8e+03 | 59.5 | ok |
| P-vial | S3a NSB partly reversible, fraction removed by washes = ma.design_levers.nsb_fra | 0.17 | 0.99 [0.22-13] | 0.51 | 0.48 | 1.8e+03 | 59.5 | ok |
| P-vial | S3b NSB irreversible and surfaces at high bound (tubing factor 30) | 0.51 | 1.7 [0.37-29] | 0.32 | 0.29 | 1.8e+03 | 59.5 | ok |
| P-vial | S4a free HQ in substrate 1e-3 (high bound) | 6.2 | 11 [1.2-1.8e+02] | 0.04 | 0.03 | 1.8e+03 | 59.5 | ok |
| P-vial | S4b free HQ in substrate 1e-7 (low bound) | 0.32 | 1.1 [0.27-18] | 0.44 | 0.42 | 1.8e+03 | 59.5 | ok |
| P-vial | S5 <=100 uL DRAWN: PLNO 75 uL on the 100 uL loop | 0.33 | 1.4 [0.32-27] | 0.36 | 0.35 | 3e+03 | 59.5 | ok |
| P-vial | L6+L7 (reagent + substrate screening) | 0.13 | 0.8 [0.19-4.5] | 0.61 | 0.57 | 7.9e+02 | 59.5 | nominal ULOQ 794 < 1000 pg/mL |
| P-vial | L1+L3+L6+L7 | 0.065 | 0.61 [0.14-2.1] | 0.77 | 0.73 | 7.9e+02 | 59.5 | nominal ULOQ 794 < 1000 pg/mL |
| P-vial | L4 immune-complex transfer: NSB x0.1 / signal x0.7 => label factor x0.14 [OUTSID | 0.08 | 0.75 [0.14-8.3] | 0.66 | 0.63 | 1.8e+03 | 59.5 | ok |
| P-chamb | S0 audited baseline | 0.56 | 2 [0.36-73] | ~0.29 | ~0.28 | 5.2e+03 | 56.1 | ok |
| P-chamb | S2a detection reagent screened (koff 1e-4, <=1.9e-4 /s) | 0.19 | 1.1 [0.28-9.1] | ~0.46 | ~0.44 | 1.8e+03 | 56.1 | ok |
| P-chamb | S2b capture reagent unscreened (koff to 8.3e-3 /s) | 0.56 | 3.3 [0.45-2.1e+02] | ~0.22 | ~0.21 | 5.2e+03 | 56.1 | ok |
| P-chamb | S1 old NSB rate (label factor 1.0, 0.3-3; x25) | 13 | 32 [3.2-1.3e+03] | ~0.00 | ~0.00 | 5.2e+03 | 56.1 | ok |
| P-chamb | S3a NSB partly reversible, fraction removed by washes = ma.design_levers.nsb_fra | 0.32 | 1.4 [0.29-56] | ~0.40 | ~0.39 | 5.2e+03 | 56.1 | ok |
| P-chamb | S3b NSB irreversible and surfaces at high bound (tubing factor 30) | 0.87 | 2.5 [0.44-99] | ~0.24 | ~0.23 | 5.2e+03 | 56.1 | ok |
| P-chamb | S4a free HQ in substrate 1e-3 (high bound) | 16 | 23 [2-7.9e+02] | ~0.01 | ~0.00 | 5.2e+03 | 56.1 | ok |
| P-chamb | S4b free HQ in substrate 1e-7 (low bound) | 0.53 | 1.4 [0.3-44] | ~0.36 | ~0.35 | 5.2e+03 | 56.1 | ok |
| P-chamb | S5 <=100 uL DRAWN: PLNO 75 uL on the 100 uL loop | 0.58 | 2.1 [0.4-80] | ~0.27 | ~0.26 | 6.8e+03 | 56.1 | ok |
| P-chamb | L6+L7 (reagent + substrate screening) | 0.18 | 0.93 [0.23-4.9] | ~0.57 | ~0.55 | 1.8e+03 | 56.1 | ok |
| P-chamb | L1+L3+L6+L7 | 0.087 | 0.7 [0.16-2.4] | ~0.74 | ~0.72 | 1.8e+03 | 56.1 | ok |
| P-chamb | L4 immune-complex transfer: NSB x0.1 / signal x0.7 => label factor x0.14 [OUTSID | 0.19 | 0.95 [0.18-41] | ~0.54 | ~0.53 | 5.2e+03 | 56.1 | ok |
| B-bed | S0 audited baseline | 0.74 | 2.8 [0.52-31] | 0.19 | 0.16 | 1e+03 | 51.5 | ok |
| B-bed | S2a detection reagent screened (koff 1e-4, <=1.9e-4 /s) | 0.62 | 2.4 [0.48-26] | 0.21 | 0.18 | 7.9e+02 | 51.5 | nominal ULOQ 794 < 1000 pg/mL |
| B-bed | S2b capture reagent unscreened (koff to 8.3e-3 /s) | 0.74 | 3.8 [0.59-92] | 0.14 | 0.12 | 1e+03 | 51.5 | ok |
| B-bed | S1 old NSB rate (label factor 1.0, 0.3-3; x25) | 19 | 62 [6.5-8.1e+02] | 0.00 | 0.00 | 1e+03 | 51.5 | ok |
| B-bed | S3a NSB partly reversible, fraction removed by washes = ma.design_levers.nsb_fra | 0.39 | 1.6 [0.39-17] | 0.31 | 0.27 | 1e+03 | 51.5 | ok |
| B-bed | S3b NSB irreversible and surfaces at high bound (tubing factor 30) | 1.4 | 4.2 [0.71-42] | 0.11 | 0.09 | 1e+03 | 51.5 | ok |
| B-bed | S4a free HQ in substrate 1e-3 (high bound) | 3.2 | 9.2 [1.4-76] | 0.02 | 0.01 | 1e+03 | 51.5 | ok |
| B-bed | S4b free HQ in substrate 1e-7 (low bound) | 0.74 | 2.6 [0.47-28] | 0.21 | 0.19 | 1e+03 | 51.5 | ok |
| B-bed | S5 <=100 uL DRAWN: PLNO 75 uL on the 100 uL loop | 0.99 | 3.7 [0.59-40] | 0.14 | 0.12 | 1.4e+03 | 51.5 | ok |
| B-bed | L6+L7 (reagent + substrate screening) | 0.62 | 2.2 [0.44-23] | 0.25 | 0.21 | 7.9e+02 | 51.5 | nominal ULOQ 794 < 1000 pg/mL |
| B-bed | L1+L3+L6+L7 | 0.3 | 1.2 [0.27-11] | 0.42 | 0.37 | 7.9e+02 | 51.5 | nominal ULOQ 794 < 1000 pg/mL |
| B-bed | L4 immune-complex transfer: NSB x0.1 / signal x0.7 => label factor x0.14 [OUTSID | 0.15 | 0.94 [0.23-6.5] | 0.54 | 0.49 | 1e+03 | 51.5 | ok |
| F-seq | S0 audited baseline | 0.3 | 1.5 [0.37-12] | 0.33 | 0.31 | 1.4e+03 | 58.5 | ok |
| F-seq | S2a detection reagent screened (koff 1e-4, <=1.9e-4 /s) | 0.25 | 1.3 [0.35-9.9] | 0.38 | 0.34 | 1e+03 | 58.5 | ok |
| F-seq | S2b capture reagent unscreened (koff to 8.3e-3 /s) | 0.3 | 2.1 [0.43-63] | 0.24 | 0.23 | 1.4e+03 | 58.5 | ok |
| F-seq | S1 old NSB rate (label factor 1.0, 0.3-3; x25) | 7.5 | 28 [3.4-2.6e+02] | 0.00 | 0.00 | 1.4e+03 | 58.5 | ok |
| F-seq | S3a NSB partly reversible, fraction removed by washes = ma.design_levers.nsb_fra | 0.16 | 1 [0.26-7.3] | 0.48 | 0.45 | 1e+03 | 58.5 | ok |
| F-seq | S3b NSB irreversible and surfaces at high bound (tubing factor 30) | 1.3 | 3.5 [0.66-32] | 0.12 | 0.10 | 1.4e+03 | 58.5 | ok |
| F-seq | S4a free HQ in substrate 1e-3 (high bound) | 3.7 | 8.5 [1.2-75] | 0.03 | 0.02 | 1.4e+03 | 58.5 | ok |
| F-seq | S4b free HQ in substrate 1e-7 (low bound) | 0.3 | 1.3 [0.3-11] | 0.39 | 0.36 | 1.4e+03 | 58.5 | ok |
| F-seq | S5 <=100 uL DRAWN: PLNO 75 uL on the 100 uL loop | 0.35 | 1.7 [0.38-15] | 0.30 | 0.28 | 1.8e+03 | 58.5 | ok |
| F-seq | L6+L7 (reagent + substrate screening) | 0.25 | 1.1 [0.27-8.2] | 0.44 | 0.41 | 1e+03 | 58.5 | ok |
| F-seq | L1+L3+L6+L7 | 0.1 | 0.67 [0.17-2.6] | 0.71 | 0.68 | 1e+03 | 58.5 | ok |
| F-seq | L4 immune-complex transfer: NSB x0.1 / signal x0.7 => label factor x0.14 [OUTSID | 0.069 | 0.71 [0.17-3.7] | 0.70 | 0.66 | 1e+03 | 58.5 | ok |
| S-chamb | S0 audited baseline | 0.36 | 1.7 [0.39-15] | ~0.30 | ~0.28 | 1.4e+03 | 58.1 | ok |
| S-chamb | S2a detection reagent screened (koff 1e-4, <=1.9e-4 /s) | 0.3 | 1.5 [0.35-11] | ~0.35 | ~0.32 | 1e+03 | 58.1 | ok |
| S-chamb | S2b capture reagent unscreened (koff to 8.3e-3 /s) | 0.36 | 2.7 [0.46-1.1e+02] | ~0.22 | ~0.21 | 1.4e+03 | 58.1 | ok |
| S-chamb | S1 old NSB rate (label factor 1.0, 0.3-3; x25) | 9 | 32 [4-2.9e+02] | ~0.00 | ~0.00 | 1.4e+03 | 58.1 | ok |
| S-chamb | S3a NSB partly reversible, fraction removed by washes = ma.design_levers.nsb_fra | 0.19 | 1.1 [0.28-9] | ~0.45 | ~0.42 | 1.4e+03 | 58.1 | ok |
| S-chamb | S3b NSB irreversible and surfaces at high bound (tubing factor 30) | 1.5 | 4 [0.7-35] | ~0.11 | ~0.10 | 1.4e+03 | 58.1 | ok |
| S-chamb | S4a free HQ in substrate 1e-3 (high bound) | 4.3 | 9.3 [1.5-82] | ~0.02 | ~0.01 | 1.4e+03 | 58.1 | ok |
| S-chamb | S4b free HQ in substrate 1e-7 (low bound) | 0.36 | 1.4 [0.35-11] | ~0.36 | ~0.34 | 1.4e+03 | 58.1 | ok |
| S-chamb | S5 <=100 uL DRAWN: PLNO 75 uL on the 100 uL loop | 0.41 | 1.9 [0.44-16] | ~0.26 | ~0.25 | 1.8e+03 | 58.1 | ok |
| S-chamb | L6+L7 (reagent + substrate screening) | 0.3 | 1.2 [0.31-8.5] | ~0.41 | ~0.38 | 1e+03 | 58.1 | ok |
| S-chamb | L1+L3+L6+L7 | 0.12 | 0.76 [0.17-2.9] | ~0.70 | ~0.66 | 1e+03 | 58.1 | ok |
| S-chamb | L4 immune-complex transfer: NSB x0.1 / signal x0.7 => label factor x0.14 [OUTSID | 0.082 | 0.76 [0.17-5.4] | ~0.66 | ~0.63 | 1.4e+03 | 58.1 | ok |
