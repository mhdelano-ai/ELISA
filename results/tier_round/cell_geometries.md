# Flow-cell geometries on the tier implementations (scripts/tier_round/cell_geometries.py)

Monte Carlo n = 2000, seed 20261111, parameters and scenarios of run_tiers.py. Model predictions, not measurements. Geometry of cells other than the MicruX cells is a design input (UNVERIFIED unless docs/02 section 5 or docs/28 gives it) and is not sampled.

## 0. Checks

| Check | value | reference | pass |
|---|---|---|---|
| uniform inlet, floor sink of length xi = 0.01: conversion against elisa_sim.transport | 0.0658772 | 0.0659819 | yes |
| uniform inlet, floor sink of length xi = 0.1: conversion against elisa_sim.transport | 0.291545 | 0.292058 | yes |
| uniform inlet, floor sink of length xi = 1: conversion against elisa_sim.transport | 0.918854 | 0.921325 | yes |
| floor source, xi_up = xi_el = 0.05: released amount / xi_up | 1 | 1 | yes |
| floor source, xi_up = xi_el = 0.05: (collected + leaving) / released | 1 | 1 | yes |
| floor source: collected fraction, grid 300 x 800 against 600 x 1600 | 0.476109 | 0.476813 | yes |
| floor source followed by a very long sink (xi_el = 30): everything is collected | 1 | 1 | yes |
| lid source, xi_up = xi_el = 0.05: released amount / xi_up | 1 | 1 | yes |
| lid source, xi_up = xi_el = 0.05: (collected + leaving) / released | 1 | 1 | yes |
| lid source: collected fraction, grid 300 x 800 against 600 x 1600 | 0.0261781 | 0.0258631 | yes |
| lid source followed by a very long sink (xi_el = 30): everything is collected | 1 | 1 | yes |
| floor source, thin boundary layer (xi = 1e-4), sink as long as the source: collected fraction; second number: double-channel-electrode efficiency for a generator at uniform concentration (recalled formula; a uniform-flux source releases more of its product near the sink, so the solver must be above it) | 0.446288 | 0.413 | yes |
| unchanged design reproduces tiers.json: Tier 1: capture on a printed gold strip, read at the electrode under fast substrate flow | 3.61552 | 3.61552 | yes |
| unchanged design reproduces tiers.json: Tier 2: capillary micro-bed above a printed carbon strip, stop and sweep | 2.06548 | 2.06548 | yes |
| unchanged design reproduces tiers.json: Tier 3: the capture bed in the loop of one valve | 1.2493 | 1.2493 | yes |
| role_a('radial', 0.2 mm) is tier 1 of docs/30 | 3.61552 | 3.61552 | yes |
| role_b(tier 2, strip cell 0.2 mm, 5 uL/min) is the design of docs/30 | 2.06548 | 2.06548 | yes |
| role_b(tier 3, strip cell 0.2 mm, 5 uL/min) is the design of docs/30 | 1.2493 | 1.2493 | yes |

## 1. Role A - the electrode is the capture surface (tier 1 of docs/30 with another cell)

Printed gold strip (3 mm) or thin-film gold chip (1 mm), everything else as tier 1 of docs/30: load 2.86 uL/min for 44 min, 20 nM conjugate, read 60 s under substrate flow. 'Captured' = fraction of the IgG in the vial that ends on the electrode. 'Stream collected' = fraction of the product arriving with the stream (walls upstream, free hydroquinone) that the electrode oxidises at 200 uL/min. 'Upstream floor / lid collected' = fraction of the product of the channel walls between inlet and electrode that the electrode oxidises (section 0 solver). Pressure drop over the chamber at the read flow (Derived; laminar).

| Cell | gap (um) | captured | k_m (um/s) | stream collected at 200 | upstream floor / lid collected | LOD nominal, read at 200 / 300 / 500 uL/min (pg/mL) | median [5-95 %] at 200 | P(LOD <= 1) at 200 | median [5-95 %] at 500 | 1 % electroactive, nominal at 200 / 500 | no decay, nominal at 200 / 500 | pressure drop at 200 / 500 uL/min (kPa) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| radial thin gap (wall-jet inlet), MicruX strip cell, 3 mm gold | 500 | 0.049 | 0.47 | 0.033 | - | 5.6 / 5 / 4.5 | 22 [3.9-1.6e+02] | 0.00 | 19 [3.3-1.3e+02] | 3.3e+02 / 2.1e+02 | 7 / 7.2 | 0.0001 / 0.00026 |
| radial thin gap (wall-jet inlet), MicruX strip cell, 3 mm gold (docs/30) | 200 | 0.082 | 0.85 | 0.061 | - | 3.6 / 3.2 / 2.9 | 16 [2.8-1.1e+02] | 0.00 | 13 [2.3-94] | 2e+02 / 1.3e+02 | 5.9 / 6.7 | 0.0016 / 0.0041 |
| radial thin gap (wall-jet inlet), MicruX strip cell, 3 mm gold | 100 | 0.118 | 1.32 | 0.096 | - | 2.8 / 2.4 / 2.2 | 13 [2.3-1e+02] | 0.01 | 11 [1.9-81] | 1.4e+02 / 88 | 5.8 / 7 | 0.013 / 0.033 |
| radial thin gap (wall-jet inlet), MicruX strip cell, 3 mm gold | 50 | 0.161 | 2.06 | 0.150 | - | 2.3 / 2 / 1.8 | 12 [2-95] | 0.01 | 9.7 [1.7-78] | 1e+02 / 65 | 6.3 / 7.9 | 0.1 / 0.26 |
| radial thin gap (wall-jet inlet), MicruX strip cell, 3 mm gold | 25 | 0.209 | 3.16 | 0.235 | - | 2.2 / 1.9 / 1.6 | 13 [2-1e+02] | 0.01 | 9.4 [1.6-85] | 78 / 51 | 7.3 / 9.4 | 0.83 / 2.1 |
| radial thin gap (wall-jet inlet), MicruX thin-film cell, 1 mm gold (docs/30) | 160 | 0.015 | 1.82 | 0.014 | - | 4.1 / 3.4 / 2.8 | 21 [3.3-1.6e+02] | 0.00 | 16 [2.6-1.1e+02] | 3.5e+02 / 2.3e+02 | 7.2 / 8.2 | 0.0019 / 0.0048 |
| radial thin gap (wall-jet inlet), MicruX thin-film cell, 1 mm gold | 50 | 0.023 | 3.90 | 0.031 | - | 3.1 / 2.5 / 2.1 | 19 [2.9-1.5e+02] | 0.00 | 14 [2.3-1.1e+02] | 2.3e+02 / 1.5e+02 | 8.9 / 11 | 0.063 / 0.16 |
| radial thin gap (wall-jet inlet), MicruX thin-film cell, 1 mm gold | 25 | 0.028 | 6.14 | 0.049 | - | 3 / 2.4 / 2 | 20 [3-1.7e+02] | 0.00 | 15 [2.3-1.3e+02] | 2e+02 / 1.3e+02 | 11 / 15 | 0.5 / 1.3 |
| cross-flow channel 2.7 mm wide, 3 mm gold, electrode at the channel entrance | 100 | 0.124 | 1.48 | 0.101 | - | 2.7 / 2.4 / 2.1 | 13 [2.2-96] | 0.01 | 10 [1.8-79] | 1.3e+02 / 84 | 5.7 / 7 | 0.062 / 0.16 |
| cross-flow channel 2.7 mm wide, 3 mm gold, electrode at the channel entrance | 50 | 0.171 | 2.35 | 0.158 | - | 2.3 / 2 / 1.7 | 12 [2-91] | 0.01 | 9.3 [1.6-76] | 95 / 62 | 6.2 / 7.8 | 0.5 / 1.2 |
| cross-flow channel 2.7 mm wide, 3 mm gold, electrode at the channel entrance | 25 | 0.222 | 3.72 | 0.246 | - | 2.1 / 1.8 / 1.5 | 12 [1.9-99] | 0.01 | 9 [1.5-81] | 74 / 49 | 7.2 / 9.3 | 4 / 10 |
| cross-flow channel 2.7 mm wide, 3 mm gold, electrode 2 mm downstream of the inlet | 100 | 0.124 | 1.48 | 0.101 | 0.50 / 0.000 | 4.4 / 4.1 / 3.8 | 20 [3.3-1.5e+02] | 0.00 | 17 [3-1.4e+02] | 1.3e+02 / 84 | 6.7 / 7.7 | 0.089 / 0.22 |
| cross-flow channel 2.7 mm wide, 3 mm gold, electrode 2 mm downstream of the inlet | 50 | 0.171 | 2.35 | 0.158 | 0.51 / 0.007 | 3.6 / 3.2 / 3 | 17 [2.8-1.4e+02] | 0.00 | 15 [2.4-1.2e+02] | 95 / 62 | 6.8 / 8.2 | 0.71 / 1.8 |
| cross-flow channel 2.7 mm wide, 3 mm gold, electrode 2 mm downstream of the inlet | 25 | 0.222 | 3.72 | 0.246 | 0.52 / 0.067 | 3.2 / 2.8 / 2.5 | 16 [2.5-1.5e+02] | 0.01 | 14 [2.1-1.2e+02] | 74 / 49 | 7.6 / 9.6 | 5.7 / 14 |
| cross-flow channel 5.0 mm wide, 3 mm gold, electrode 2 mm downstream of the inlet | 50 | 0.145 | 1.90 | 0.126 | 0.52 / 0.057 | 4.1 / 3.7 / 3.4 | 19 [3.1-1.5e+02] | 0.00 | 16 [2.7-1.3e+02] | 1.1e+02 / 72 | 6.8 / 8 | 0.38 / 0.95 |

### 1a. The same Monte Carlo draws with a 0.2 mm and with a 50 um gap (strip cell, read at 200 uL/min)

LOD at 50 um divided by LOD at 0.2 mm, draw by draw: median 0.75 [0.54-1.20]; above 1 (the thin gap is worse) in 0.16 of the draws, above 0.9 in 0.27. Correlation of log ratio with log parameter, six largest: `chem.antibodies.kon_capture` -0.42; `chem.surfaces.igg_surface_density_monolayer` -0.36; `tr.nsb.surface_factor_gold_oeg` -0.32; `ma.nsb.surface_factor_tubing` +0.26; `tr.detection.monolayer_collection_efficiency` +0.21; `ma.chemistries.alp_hqdp.hydrolysis_rate` +0.21.

### 1b. Capture transport of other shapes at the load flow (no LOD)

Mean flux to the capture surface per unit inlet concentration, k_eff = captured fraction x Q / area (reaction and transport in series), at 2.86 uL/min, with the reaction velocity k_r of tier 1. The specific label per area of electrode, and with it the ratio to the electrode's own non-specific label, scales with k_eff; its ceiling is k_r.

| Shape | area (mm2) | captured fraction of what enters | k_eff (um/s) | k_eff / k_r | product of the stream collected at 200 uL/min |
|---|---|---|---|---|---|
| radial thin gap 200 um over a 3 mm disc | 7.07 | 0.104 | 0.70 | 0.17 | 0.061 |
| radial thin gap 25 um over a 3 mm disc | 7.07 | 0.265 | 1.79 | 0.42 | 0.235 |
| tubular electrode, bore 0.25 mm, length 9.0 mm (no part identified) | 7.07 | 0.141 | 0.95 | 0.22 | 0.090 |
| tubular electrode, bore 0.25 mm, length 1.0 mm (no part identified) | 0.79 | 0.028 | 1.68 | 0.40 | 0.022 |
| tubular electrode, bore 0.10 mm, length 22.5 mm (no part identified) | 7.07 | 0.212 | 1.43 | 0.34 | 0.159 |
| tubular electrode, bore 0.10 mm, length 2.5 mm (no part identified) | 0.79 | 0.038 | 2.32 | 0.55 | 0.040 |
| porous or packed electrode with the surface of the tier-2 bed, at 3.4 uL/min (no part identified) | 24.43 | 0.832 | 1.93 | 0.46 | 1.000 |

## 2. Role B - the cell detects the product of a bed: tier 3, the bed in the loop of one valve

The bed, its loop and the valve are those of docs/30; only the detector differs. 'As specified' = sweep at 5 uL/min for 90 s (porous cell: at its minimum flow). 'Best sweep' = lowest nominal LOD over 2-100 uL/min with the same swept volume (window at least 6 s, result within 60 min). Scenario '1 %' = only 1 % of the enzyme turnovers give an electroactive product (docs/31 C1); 'no decay' = the substrate's free hydroquinone persists (docs/31 C5, M2).

| Detector | electrode (mm2) | product oxidised at 5 / 50 uL/min | as specified: LOD nominal | median [5-95 %] | P(LOD <= 1) | no decay, nominal | 1 %: nominal as specified | 1 %: best sweep (uL/min, s) | 1 %: median [5-95 %] at the best sweep | 1 % and no decay: best sweep |
|---|---|---|---|---|---|---|---|---|---|---|
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.5 mm | 7.07 | 0.36 / 0.08 | 1.3 | 5.2 [0.83-58] | 0.08 | 1.3 | 35 | 20 (20, 22) | 39 [5.9-4.1e+02] | 38 (10, 45) |
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.2 mm (docs/30) | 7.07 | 0.62 / 0.15 | 1.2 | 5.1 [0.78-58] | 0.09 | 1.3 | 20 | 11 (20, 22) | 25 [3.7-2.6e+02] | 34 (10, 45) |
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.1 mm | 7.07 | 0.84 / 0.23 | 1.2 | 5 [0.76-58] | 0.10 | 1.3 | 15 | 7.3 (20, 22) | 19 [2.9-1.9e+02] | 32 (5, 90) |
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.05 mm | 7.07 | 0.97 / 0.36 | 1.2 | 4.9 [0.76-58] | 0.10 | 1.3 | 13 | 5 (20, 22) | 15 [2.3-1.5e+02] | 31 (5, 90) |
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.025 mm | 7.07 | 1.00 / 0.55 | 1.2 | 4.9 [0.76-58] | 0.10 | 1.3 | 13 | 3.7 (50, 9) | 13 [1.9-1.4e+02] | 31 (5, 90) |
| radial thin gap, MicruX thin-film cell, 1 mm electrode, gap 0.16 mm | 0.79 | 0.16 / 0.04 | 1.3 | 5.1 [0.82-58] | 0.08 | 1.3 | 26 | 15 (20, 22) | 32 [4.8-3.4e+02] | 36 (10, 45) |
| radial thin gap, MicruX thin-film cell, 1 mm electrode, gap 0.05 mm | 0.79 | 0.34 / 0.08 | 1.2 | 5 [0.76-58] | 0.10 | 1.3 | 12 | 7.3 (20, 22) | 19 [2.9-2e+02] | 31 (5, 90) |
| radial thin gap, MicruX thin-film cell, 1 mm electrode, gap 0.025 mm | 0.79 | 0.52 / 0.12 | 1.2 | 4.9 [0.73-58] | 0.10 | 1.3 | 8.2 | 4.7 (20, 22) | 15 [2.3-1.5e+02] | 30 (5, 90) |
| radial thin gap, adjustable (Antec SenCell type): 2 mm glassy carbon, working volume 100 nL = gap 32 um | 3.14 | 0.93 / 0.30 | 1.2 | 4.9 [0.73-58] | 0.10 | 1.3 | 9.1 | 4 (20, 22) | 13 [2-1.4e+02] | 30 (5, 90) |
| cross-flow thin-layer channel (BASi type): 3 mm glassy carbon, gasket 127 um, channel 3 mm wide | 7.07 | 0.73 / 0.20 | 1.2 | 5 [0.77-58] | 0.09 | 1.3 | 17 | 8.5 (20, 22) | 21 [3.1-2.1e+02] | 33 (10, 45) |
| cross-flow thin-layer channel (BASi type): 3 mm glassy carbon, gasket 51 um, channel 3 mm wide | 7.07 | 0.87 / 0.36 | 1.2 | 5 [0.76-58] | 0.10 | 1.3 | 14 | 5.1 (20, 22) | 15 [2.3-1.6e+02] | 32 (5, 90) |
| cross-flow thin-layer channel (BASi type): 3 mm glassy carbon, gasket 13 um, channel 3 mm wide | 7.07 | 0.89 / 0.73 | 1.2 | 5 [0.76-58] | 0.10 | 1.3 | 14 | 2.9 (50, 9) | 11 [1.7-1.3e+02] | 32 (5, 90) |
| free wall jet, large gap (DropSens FLWCL type): 4 mm printed carbon, nozzle 0.3 mm; wall-jet equation, outside its validity at these flows | 12.57 | 0.05 / 0.03 | 3.7 | 11 [1.9-94] | 0.01 | 3.8 | 3.4e+02 | 85 (100, 6) | 1.4e+02 [19-1.7e+03] | 96 (100, 6) |
| porous flow-through graphite (Dionex 6011RS type): conversion 0.95, wetted area 100 mm2, 4.3 uL, flow >= 300 uL/min | 100.00 | 0.95 / 0.95 | 1.2 | 5.2 [0.76-59] | 0.10 | 1.9 | 6 | 6 (300, 6) | 23 [2.8-3.4e+02] | 1.3e+02 (300, 6) |
| bound: every product molecule oxidised, 3 mm electrode | 7.07 | 1.00 / 1.00 | 1.2 | 4.9 [0.76-58] | 0.10 | 1.3 | 13 | 2 (100, 6) | 9.9 [1.5-1.3e+02] | 31 (5, 90) |
| bound: every product molecule oxidised, 1 mm electrode | 0.79 | 1.00 / 1.00 | 1.2 | 4.9 [0.7-58] | 0.11 | 1.3 | 4.4 | 1.4 (100, 6) | 8.1 [1.1-1.2e+02] | 29 (2, 225) |

## 3. Role B - the cell detects the product of a bed: tier 2, capillary bed, stop and sweep

'Bed position': 'tip' = the capillary tip sits in the cell's straight inlet bore 1 mm above the chamber (docs/30); 'port' = the bed sits in a fitting on the inlet port and the inlet passage (taken as 0.8 mm x 5 mm for every such cell, UNVERIFIED) lies between bed and electrode. 'As specified' = sweep at 5 uL/min for 90 s (porous cell: at its minimum flow). 'Best sweep' = lowest nominal LOD over 2-100 uL/min with the same swept volume (window at least 6 s, result within 60 min). Scenario '1 %' = only 1 % of the enzyme turnovers give an electroactive product (docs/31 C1); 'no decay' = the substrate's free hydroquinone persists (docs/31 C5, M2).

| Detector | bed position | electrode (mm2) | product oxidised at 5 / 50 uL/min | as specified: LOD nominal | median [5-95 %] | P(LOD <= 1) | no decay, nominal | 1 %: nominal as specified | 1 %: best sweep (uL/min, s) | 1 %: median [5-95 %] at the best sweep | 1 % and no decay: best sweep |
|---|---|---|---|---|---|---|---|---|---|---|---|
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.5 mm | tip | 7.07 | 0.36 / 0.08 | 2.1 | 8.5 [1.1-1e+02] | 0.04 | 2.2 | 21 | 13 (20, 22) | 33 [5-3.7e+02] | 74 (2, 225) |
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.2 mm (docs/30) | tip | 7.07 | 0.62 / 0.15 | 2.1 | 8.4 [1-1e+02] | 0.05 | 2.2 | 13 | 7.4 (20, 22) | 24 [3.8-2.7e+02] | 64 (2, 225) |
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.1 mm | tip | 7.07 | 0.84 / 0.23 | 2.1 | 8.4 [1-1e+02] | 0.05 | 2.2 | 9.4 | 5.1 (20, 22) | 21 [3-2.3e+02] | 62 (2, 225) |
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.05 mm | tip | 7.07 | 0.97 / 0.36 | 2.1 | 8.4 [0.99-1e+02] | 0.05 | 2.2 | 8.2 | 3.7 (20, 22) | 18 [2.6-2.1e+02] | 62 (2, 225) |
| radial thin gap, MicruX strip cell, 3 mm printed carbon, gap 0.025 mm | tip | 7.07 | 1.00 / 0.55 | 2.1 | 8.4 [0.99-1e+02] | 0.05 | 2.2 | 8 | 3.1 (50, 9) | 17 [2.4-2e+02] | 62 (2, 225) |
| radial thin gap, MicruX thin-film cell, 1 mm electrode, gap 0.16 mm | tip | 0.79 | 0.16 / 0.04 | 2.1 | 8.5 [1-1e+02] | 0.05 | 2.2 | 16 | 9.8 (20, 22) | 29 [4.4-3.2e+02] | 63 (2, 225) |
| radial thin gap, MicruX thin-film cell, 1 mm electrode, gap 0.05 mm | tip | 0.79 | 0.34 / 0.08 | 2.1 | 8.5 [0.98-1e+02] | 0.05 | 2.2 | 7.7 | 5 (20, 22) | 21 [3.1-2.4e+02] | 54 (2, 225) |
| radial thin gap, MicruX thin-film cell, 1 mm electrode, gap 0.025 mm | tip | 0.79 | 0.52 / 0.12 | 2.1 | 8.5 [0.98-1e+02] | 0.05 | 2.2 | 5.3 | 3.6 (20, 22) | 17 [2.5-2.1e+02] | 53 (2, 225) |
| radial thin gap, adjustable (Antec SenCell type): 2 mm glassy carbon, working volume 100 nL = gap 32 um | port | 3.14 | 0.93 / 0.30 | 2.3 | 9.5 [1.1-1.1e+02] | 0.04 | 2.4 | 6.5 | 3.5 (20, 22) | 18 [2.7-2.2e+02] | 66 (2, 225) |
| cross-flow thin-layer channel (BASi type): 3 mm glassy carbon, gasket 127 um, channel 3 mm wide | port | 7.07 | 0.73 / 0.20 | 2.3 | 9.5 [1.2-1.1e+02] | 0.04 | 2.4 | 12 | 6.1 (20, 22) | 24 [3.5-2.6e+02] | 75 (2, 225) |
| cross-flow thin-layer channel (BASi type): 3 mm glassy carbon, gasket 51 um, channel 3 mm wide | port | 7.07 | 0.87 / 0.36 | 2.3 | 9.5 [1.1-1.1e+02] | 0.04 | 2.4 | 10 | 4.1 (20, 22) | 20 [2.9-2.3e+02] | 75 (2, 225) |
| cross-flow thin-layer channel (BASi type): 3 mm glassy carbon, gasket 13 um, channel 3 mm wide | port | 7.07 | 0.89 / 0.73 | 2.3 | 9.5 [1.1-1.1e+02] | 0.04 | 2.4 | 9.8 | 3 (50, 9) | 17 [2.5-2.2e+02] | 75 (2, 225) |
| free wall jet, large gap (DropSens FLWCL type): 4 mm printed carbon, nozzle 0.3 mm; wall-jet equation, outside its validity at these flows | port | 12.57 | 0.05 / 0.03 | 3.3 | 13 [2-1.3e+02] | 0.01 | 3.4 | 2.2e+02 | 57 (100, 6) | 1e+02 [14-1.4e+03] | 1.1e+02 (50, 9) |
| porous flow-through graphite (Dionex 6011RS type): conversion 0.95, wetted area 100 mm2, 4.3 uL, flow >= 300 uL/min | port | 100.00 | 0.95 / 0.95 | 2.3 | 9.9 [1.2-1.1e+02] | 0.04 | 4.4 | 5.4 | 5.4 (300, 6) | 31 [3.6-5.7e+02] | 3.8e+02 (300, 6) |
| bound: every product molecule oxidised, 3 mm electrode | tip | 7.07 | 1.00 / 1.00 | 2.1 | 8.4 [0.99-1e+02] | 0.05 | 2.2 | 8 | 2.5 (100, 6) | 15 [2-2.3e+02] | 62 (2, 225) |
| bound: every product molecule oxidised, 1 mm electrode | tip | 0.79 | 1.00 / 1.00 | 2.1 | 8.4 [0.98-1e+02] | 0.05 | 2.2 | 3.3 | 2.2 (50, 9) | 14 [1.8-1.9e+02] | 53 (2, 225) |

All checks pass.

