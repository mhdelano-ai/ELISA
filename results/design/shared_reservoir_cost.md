# Cost of a shared bead + conjugate reservoir (counterfactual; docs/08 B4)

Primary design P-chamb (final_designs default), n = 2000, seed 20261111. Reservoir conjugate 3.3 nM; in-cup exposure 11 nM*min. A reservoir filled once and used for 8 h gives a mean hold of 4 h (worst sample 8 h); for a 24-h sequence 12 h (worst 24 h). Linear irreversible NSB assumed (UNVERIFIED); saturation, aggregation and reagent-borne human IgG are outside the model. The primary design now uses separate reservoirs (hold time 0 by construction).

| mean hold time in the shared reservoir (h) | NSB slowing at 4-8 C | bead NSB multiplier M | LOD nominal | LOD median [5-95 %] | P(success) |
|---|---|---|---|---|---|
| 0 | none | 1 | 0.6 | 3.5 [0.51-1.6e+02] | ~0.16 |
| 0.5 | none | 10 | 5 | 21 [1.9-8.8e+02] | ~0.01 |
| 2 | none | 37.1 | 18 | 75 [6-3.3e+03] | ~0.00 |
| 4 | none | 73.1 | 37 | 1.5e+02 [12-6.5e+03] | ~0.00 |
| 8 | none | 145 | 73 | 2.9e+02 [23-1.3e+04] | ~0.00 |
| 12 | none | 217 | 1.1e+02 | 4.5e+02 [33-2.1e+04] | ~0.00 |
| 24 | none | 434 | 2.3e+02 | 9e+02 [70-4.6e+04] | ~0.00 |
| 0.5 | x0.25 (illustrative) | 3.25 | 1.7 | 8.1 [0.89-3.2e+02] | ~0.06 |
| 2 | x0.25 (illustrative) | 10 | 5 | 21 [1.9-8.8e+02] | ~0.01 |
| 4 | x0.25 (illustrative) | 19 | 9.5 | 39 [3.2-1.7e+03] | ~0.00 |
| 8 | x0.25 (illustrative) | 37.1 | 18 | 75 [6-3.3e+03] | ~0.00 |
| 12 | x0.25 (illustrative) | 55.1 | 27 | 1.1e+02 [8.9-4.9e+03] | ~0.00 |
| 24 | x0.25 (illustrative) | 109 | 55 | 2.2e+02 [17-9.9e+03] | ~0.00 |
