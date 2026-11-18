# Checks of scripts/tier_round/tierkit.py against analytic limits and the audited model

| Check | Kit | Reference | Relative error | Tolerance | Result | Note |
|---|---|---|---|---|---|---|
| B1 Leveque limit of the slit conversion (perfect sink, zeta = 5.0e-04) | 0.0091048 | 0.0092036 | 1.07e-02 | 3e-02 | PASS | 1.4675 zeta^(2/3) |
| B2 k_m L w / Q equals the Leveque conversion | 0.0092037 | 0.0092036 | 4.49e-06 | 2e-03 | PASS |  |
| B3 kinetic limit (Da -> 0): conversion = k_r L w / Q | 0.00012758 | 0.00012768 | 7.94e-04 | 2e-02 | PASS |  |
| B4 a patch half as wide as the channel captures half | 0.043295 | 0.043295 | 0.00e+00 | 1e-09 | PASS |  |
| B5 long thin channel, slow flow: complete capture | 0.99999 | 1 | 1.04e-05 | 1e-02 | PASS |  |
| B6 Leveque flux to a disc / to a square of equal area | 1.0289 | 1.03 | 1.05e-03 | 1e-02 | PASS | justifies sqrt(A) side |
| C1 perfect-sink slab, D t / h^2 = 0.05 | 0.25231 | 0.25231 | 1.54e-08 | 1e-02 | PASS |  |
| C1 perfect-sink slab, D t / h^2 = 0.3 | 0.61324 | 0.61324 | 6.09e-09 | 1e-02 | PASS |  |
| C1 perfect-sink slab, D t / h^2 = 1.0 | 0.93126 | 0.93126 | 1.70e-09 | 1e-02 | PASS |  |
| C2 short time, perfect sink: 2 sqrt(D t / pi) / h | 0.077094 | 0.077094 | 1.01e-08 | 2e-02 | PASS |  |
| C3 slow reaction (Bi -> 0): 1 - exp(-k_r t / h) | 0.17989 | 0.18127 | 7.63e-03 | 1e-02 | PASS |  |
| G0 electrode area on the grid | 7.0686e-06 | 7.0686e-06 | 1.20e-16 | 1e-09 | PASS |  |
| G1 mass conservation, electrode off, floor source 1 mol/s for 300 s | 300 | 300 | 5.13e-14 | 1e-09 | PASS |  |
| G2 mass balance with electrode on: mass + collected = produced | 600 | 600 | 2.50e-14 | 1e-09 | PASS |  |
| G3 exhaustive thin-layer electrolysis, fraction collected at D t / h^2 = 0.4 | 0.69362 | 0.69788 | 6.11e-03 | 1e-02 | PASS |  |
| G4 ceiling source over a full-floor electrode: steady collection rate | 1 | 1 | 4.44e-16 | 1e-03 | PASS |  |
| G5 same: time lag h^2 / (2 D) | 34.722 | 34.722 | 4.07e-14 | 2e-02 | PASS |  |
| G6 floor source, electrode off: surface concentration J t / h + J h / (3 D) | 1.9975e+11 | 1.9976e+11 | 3.88e-05 | 1e-02 | PASS | cell-centre value of the first layer |
| G7 Cottrell flux to the disc at 2 s (layer not yet depleted) | 8.7931e-11 | 8.4599e-11 | 3.94e-02 | 6e-02 | PASS | backward Euler; edge diffusion adds a few % |
| G8 long electrolysis collects the whole layer | 7.0686e-09 | 7.0686e-09 | 6.90e-08 | 3e-02 | PASS |  |
| G9 grid convergence: floor-ring source collected in 600 s (36x18 vs 60x26 grid) | 129.16 | 130.68 | 1.17e-02 | 2e-02 | PASS |  |
| G10 cycling velocity, thin reaction layer: sqrt(D k) | 0.0003 | 0.0003 | 0.00e+00 | 1e-06 | PASS |  |
| G11 cycling velocity, layer thinner than the reaction layer: k h | 1.9997e-08 | 2e-08 | 1.48e-04 | 1e-02 | PASS |  |
| G12 cycling velocity against a 1-D finite-difference reaction-diffusion solution | 3e-05 | 3e-05 | 1.63e-06 | 1e-02 | PASS |  |
| H1 impurity collected in 600 s exceeds the layer above the electrode (lateral in-diffusion) | 1 | 1 | 0.00e+00 | 0e+00 | PASS |  |
| H2 impurity collected in 600 s is below the whole layer | 1 | 1 | 0.00e+00 | 0e+00 | PASS |  |
| H3 hydrolysis source: collected + stored = produced | 4.2412e-06 | 4.2412e-06 | 2.72e-14 | 1e-09 | PASS |  |
| H4 lid source collected fraction lies between 0 and 1 | 1 | 1 | 0.00e+00 | 0e+00 | PASS |  |
| R1 radial thin-gap capture equals the Lighthill-Leveque result for radial outflow | 0.012135 | 0.012285 | 1.22e-02 | 3e-02 | PASS | independent derivation, README B |
| R2 liquid volume of layer + bore on the grid | 1.0917e-09 | 1.0917e-09 | 0.00e+00 | 1e-09 | PASS |  |
| R3 mass balance with a bore | 600 | 600 | 8.39e-14 | 1e-09 | PASS |  |
| D1 Kozeny-Carman, 2.8 um beads, eps 0.4, 24 um cake, 0.21 mm/s | 482.75 | 482.75 | 2.36e-16 | 1e-09 | PASS |  |
| X1 bed format: captured fraction equals the model's B-bed-TL/alp_hqdp | 0.78569 | 0.78569 | 1.18e-11 | 2e-02 | PASS |  |
| X2 bed format: specific enzymes at 1 pg/mL equal the model's | 7825.9 | 7825.9 | 1.22e-09 | 5e-02 | PASS |  |
| X3 bed format: signal at 1 pg/mL equals the model's | 4.7229e-10 | 4.7229e-10 | 1.54e-09 | 5e-02 | PASS |  |
| X4 bed format: LOD within 25 % of the model's (unit-to-unit terms and regeneration differ) | 20.026 | 19.38 | 3.33e-02 | 2e-01 | PASS | kit 20 vs model 19.4 pg/mL |

36 of 36 checks passed.
