## Levers represented by existing parameters (scenario runs)

n = 2000 Monte Carlo draws, seed 20261111. Success = LOD <= 1 pg/mL and ULOQ >= 1000 pg/mL.

| Design | Scenario | LOD nominal | LOD median [5-95 %] | P(LOD<=1) | P(success) | time to result (min) |
|---|---|---|---|---|---|---|
| OS-opt | L0 none (optimised design) | 0.32 | 1.3 [0.3-21] | 0.38 | 0.35 | 59.5 |
| OS-opt | L1 inert/coated wetted path: tubing + trap-wall surface factor at its low bound (1) | 0.31 | 1.3 [0.29-20] | 0.40 | 0.37 | 59.5 |
| OS-opt | L2 clean-zone re-trap: wall NSB term removed (tubing factor 0.01) [OUTSIDE MODEL as physics] | 0.3 | 1.3 [0.29-20] | 0.40 | 0.37 | 59.5 |
| OS-opt | L3 Fab'-ALP conjugate: label NSB x fab_conjugate_nsb_factor (0.5) [OUTSIDE MODEL, bounded estimate] | 0.17 | 0.99 [0.22-13] | 0.51 | 0.48 | 59.5 |
| OS-opt | L4 immune-complex transfer: NSB x0.1 / signal x0.7 => label factor x0.14 [OUTSIDE MODEL] | 0.08 | 0.75 [0.14-8.3] | 0.66 | 0.63 | 59.5 |
| OS-opt | L5 reference-channel subtraction, rho = 0.8: CV_NSB x sqrt(2(1-rho)) = 0.63 [OUTSIDE MODEL] | 0.24 | 1.1 [0.26-17] | 0.44 | 0.41 | 59.5 |
| OS-opt | L6 detection reagent screened (t1/2 >= 1 h) | 0.14 | 0.94 [0.24-6.1] | 0.55 | 0.50 | 59.5 |
| OS-opt | L7 substrate purified: free HQ pinned at 1e-6 | 0.32 | 1.1 [0.27-18] | 0.44 | 0.41 | 59.5 |
| OS-opt | L8 bench-measured NSB at the plate anchor low end (label factor 0.029) | 0.24 | 1.1 [0.25-15] | 0.46 | 0.43 | 59.5 |
| OS-opt | L6+L7 (reagent + substrate screening) | 0.13 | 0.8 [0.19-4.5] | 0.61 | 0.57 | 59.5 |
| OS-opt | L1+L6+L7 | 0.13 | 0.77 [0.18-4.1] | 0.63 | 0.59 | 59.5 |
| OS-opt | L1+L3+L6+L7 | 0.065 | 0.61 [0.14-2.1] | 0.77 | 0.73 | 59.5 |
| SQ-opt | L0 none (optimised design) | 0.3 | 1.5 [0.37-12] | 0.33 | 0.31 | 58.5 |
| SQ-opt | L1 inert/coated wetted path: tubing + trap-wall surface factor at its low bound (1) | 0.24 | 1.2 [0.3-8.8] | 0.43 | 0.40 | 58.5 |
| SQ-opt | L2 clean-zone re-trap: wall NSB term removed (tubing factor 0.01) [OUTSIDE MODEL as physics] | 0.2 | 1.1 [0.29-8.3] | 0.45 | 0.42 | 58.5 |
| SQ-opt | L3 Fab'-ALP conjugate: label NSB x fab_conjugate_nsb_factor (0.5) [OUTSIDE MODEL, bounded estimate] | 0.16 | 1 [0.26-7.3] | 0.48 | 0.45 | 58.5 |
| SQ-opt | L4 immune-complex transfer: NSB x0.1 / signal x0.7 => label factor x0.14 [OUTSIDE MODEL] | 0.069 | 0.71 [0.17-3.7] | 0.70 | 0.66 | 58.5 |
| SQ-opt | L5 reference-channel subtraction, rho = 0.8: CV_NSB x sqrt(2(1-rho)) = 0.63 [OUTSIDE MODEL] | 0.21 | 1.2 [0.31-9.5] | 0.41 | 0.38 | 58.5 |
| SQ-opt | L6 detection reagent screened (t1/2 >= 1 h) | 0.25 | 1.3 [0.35-9.9] | 0.38 | 0.34 | 58.5 |
| SQ-opt | L7 substrate purified: free HQ pinned at 1e-6 | 0.3 | 1.3 [0.3-11] | 0.39 | 0.36 | 58.5 |
| SQ-opt | L8 bench-measured NSB at the plate anchor low end (label factor 0.029) | 0.22 | 1.2 [0.31-8.4] | 0.42 | 0.39 | 58.5 |
| SQ-opt | L6+L7 (reagent + substrate screening) | 0.25 | 1.1 [0.27-8.2] | 0.44 | 0.41 | 58.5 |
| SQ-opt | L1+L6+L7 | 0.19 | 0.91 [0.23-5] | 0.56 | 0.52 | 58.5 |
| SQ-opt | L1+L3+L6+L7 | 0.1 | 0.67 [0.17-2.6] | 0.71 | 0.68 | 58.5 |
| FRB-opt | L0 none (optimised design) | 0.94 | 3.6 [0.6-42] | 0.14 | 0.12 | 51.5 |
| FRB-opt | L1 inert/coated wetted path: tubing + trap-wall surface factor at its low bound (1) | 0.88 | 3.2 [0.55-39] | 0.16 | 0.14 | 51.5 |
| FRB-opt | L2 clean-zone re-trap: wall NSB term removed (tubing factor 0.01) [OUTSIDE MODEL as physics] | 0.85 | 3.1 [0.54-39] | 0.17 | 0.15 | 51.5 |
| FRB-opt | L3 Fab'-ALP conjugate: label NSB x fab_conjugate_nsb_factor (0.5) [OUTSIDE MODEL, bounded estimate] | 0.49 | 2.1 [0.44-23] | 0.24 | 0.22 | 51.5 |
| FRB-opt | L4 immune-complex transfer: NSB x0.1 / signal x0.7 => label factor x0.14 [OUTSIDE MODEL] | 0.18 | 1.1 [0.26-8.8] | 0.47 | 0.43 | 51.5 |
| FRB-opt | L5 reference-channel subtraction, rho = 0.8: CV_NSB x sqrt(2(1-rho)) = 0.63 [OUTSIDE MODEL] | 0.63 | 2.6 [0.51-29] | 0.19 | 0.17 | 51.5 |
| FRB-opt | L6 detection reagent screened (t1/2 >= 1 h) | 0.78 | 3.1 [0.55-34] | 0.16 | 0.14 | 51.5 |
| FRB-opt | L7 substrate purified: free HQ pinned at 1e-6 | 0.94 | 3.3 [0.55-39] | 0.16 | 0.14 | 51.5 |
| FRB-opt | L8 bench-measured NSB at the plate anchor low end (label factor 0.029) | 0.69 | 2.6 [0.52-28] | 0.20 | 0.18 | 51.5 |
| FRB-opt | L6+L7 (reagent + substrate screening) | 0.78 | 2.8 [0.5-32] | 0.19 | 0.17 | 51.5 |
| FRB-opt | L1+L6+L7 | 0.73 | 2.5 [0.46-30] | 0.22 | 0.19 | 51.5 |
| FRB-opt | L1+L3+L6+L7 | 0.38 | 1.4 [0.32-15] | 0.35 | 0.32 | 51.5 |
| FRC-opt | L0 none (optimised design) | 0.95 | 3.8 [0.64-46] | 0.12 | 0.10 | 45.0 |
| FRC-opt | L1 inert/coated wetted path: tubing + trap-wall surface factor at its low bound (1) | 0.95 | 3.8 [0.64-46] | 0.12 | 0.10 | 45.0 |
| FRC-opt | L2 clean-zone re-trap: wall NSB term removed (tubing factor 0.01) [OUTSIDE MODEL as physics] | 0.95 | 3.8 [0.64-46] | 0.12 | 0.10 | 45.0 |
| FRC-opt | L3 Fab'-ALP conjugate: label NSB x fab_conjugate_nsb_factor (0.5) [OUTSIDE MODEL, bounded estimate] | 0.5 | 2.1 [0.48-25] | 0.22 | 0.20 | 45.0 |
| FRC-opt | L4 immune-complex transfer: NSB x0.1 / signal x0.7 => label factor x0.14 [OUTSIDE MODEL] | 0.22 | 1.1 [0.3-9.7] | 0.46 | 0.41 | 45.0 |
| FRC-opt | L5 reference-channel subtraction, rho = 0.8: CV_NSB x sqrt(2(1-rho)) = 0.63 [OUTSIDE MODEL] | 0.8 | 3.3 [0.6-39] | 0.14 | 0.12 | 45.0 |
| FRC-opt | L6 detection reagent screened (t1/2 >= 1 h) | 0.79 | 3.4 [0.59-35] | 0.15 | 0.12 | 45.0 |
| FRC-opt | L7 substrate purified: free HQ pinned at 1e-6 | 0.95 | 3.6 [0.63-37] | 0.13 | 0.11 | 45.0 |
| FRC-opt | L8 bench-measured NSB at the plate anchor low end (label factor 0.029) | 0.7 | 2.7 [0.55-29] | 0.17 | 0.14 | 45.0 |
| FRC-opt | L6+L7 (reagent + substrate screening) | 0.79 | 3 [0.57-29] | 0.16 | 0.13 | 45.0 |
| FRC-opt | L1+L6+L7 | 0.79 | 3 [0.57-29] | 0.16 | 0.13 | 45.0 |
| FRC-opt | L1+L3+L6+L7 | 0.42 | 1.7 [0.4-14] | 0.29 | 0.25 | 45.0 |
