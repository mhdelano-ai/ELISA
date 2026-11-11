# Effect of the final-review corrections on the headline predictions

n = 2000, seed 20261111. Steps are cumulative (see the script docstring). Row 'a' reproduces docs/05 and results/design/final_designs.md as committed before the review.

| Design | Scenario | Step | LOD nominal | LOD median [5-95 %] | P(success) | ULOQ nominal |
|---|---|---|---|---|---|---|
| P-chamb | S0 | a docs/05 as published | 0.56 | 2 [0.36-73] | ~0.28 | 5.2e+03 |
| P-chamb | S0 | b + transfer factor before P (S13) | 0.56 | 2 [0.36-73] | ~0.27 | 5.2e+03 |
| P-chamb | S0 | c + stirring factor sampled (S13) | 0.56 | 3 [0.51-1.3e+02] | ~0.19 | 5.2e+03 |
| P-chamb | S0 | d + thin-layer cell default (S9) | 0.6 | 3.5 [0.51-1.6e+02] | ~0.17 | 5.2e+03 |
| P-chamb | S0 | e + Ki override UNVERIFIED 0.2 uM-1 mM (S10) = revised | 0.6 | 3.5 [0.51-1.6e+02] | ~0.16 | 5.2e+03 |
| P-chamb | L6+L7 | a docs/05 as published | 0.18 | 0.93 [0.23-4.9] | ~0.55 | 1.8e+03 |
| P-chamb | L6+L7 | b + transfer factor before P (S13) | 0.18 | 0.93 [0.23-4.9] | ~0.53 | 1.8e+03 |
| P-chamb | L6+L7 | c + stirring factor sampled (S13) | 0.18 | 1.2 [0.3-9.4] | ~0.41 | 1.8e+03 |
| P-chamb | L6+L7 | d + thin-layer cell default (S9) | 0.19 | 1.3 [0.34-9.3] | ~0.34 | 1.8e+03 |
| P-chamb | L6+L7 | e + Ki override UNVERIFIED 0.2 uM-1 mM (S10) = revised | 0.19 | 1.3 [0.34-9.3] | ~0.32 | 1.8e+03 |
| S-chamb | S0 | a docs/05 as published | 0.36 | 1.7 [0.39-15] | ~0.28 | 1.4e+03 |
| S-chamb | S0 | b + transfer factor before P (S13) | 0.36 | 1.7 [0.39-15] | ~0.27 | 1.4e+03 |
| S-chamb | S0 | c + stirring factor sampled (S13) | 0.36 | 2.4 [0.5-23] | ~0.19 | 1.4e+03 |
| S-chamb | S0 | d + thin-layer cell default (S9) | 0.42 | 2.9 [0.56-26] | ~0.14 | 1.4e+03 |
| S-chamb | S0 | e + Ki override UNVERIFIED 0.2 uM-1 mM (S10) = revised | 0.42 | 3 [0.56-26] | ~0.13 | 1.4e+03 |
| S-chamb | L6+L7 | a docs/05 as published | 0.3 | 1.2 [0.31-8.5] | ~0.38 | 1e+03 |
| S-chamb | L6+L7 | b + transfer factor before P (S13) | 0.3 | 1.2 [0.31-8.5] | ~0.36 | 1e+03 |
| S-chamb | L6+L7 | c + stirring factor sampled (S13) | 0.3 | 1.7 [0.38-16] | ~0.28 | 1e+03 |
| S-chamb | L6+L7 | d + thin-layer cell default (S9) | 0.34 | 2.1 [0.49-16] | ~0.19 | 1e+03 |
| S-chamb | L6+L7 | e + Ki override UNVERIFIED 0.2 uM-1 mM (S10) = revised | 0.34 | 2.1 [0.49-16] | ~0.17 | 1e+03 |
| B-bed | S0 | a docs/05 as published | 0.74 | 2.8 [0.52-31] | 0.16 | 1e+03 |
| B-bed | S0 | b + transfer factor before P (S13) | 0.74 | 2.8 [0.52-31] | 0.16 | 1e+03 |
| B-bed | S0 | c + stirring factor sampled (S13) | 0.74 | 2.8 [0.52-31] | 0.16 | 1e+03 |
| B-bed | S0 | d + thin-layer cell default (S9) | 0.85 | 3.4 [0.65-33] | 0.10 | 1e+03 |
| B-bed | S0 | e + Ki override UNVERIFIED 0.2 uM-1 mM (S10) = revised | 0.85 | 3.4 [0.65-33] | 0.09 | 1e+03 |
| B-bed | L6+L7 | a docs/05 as published | 0.62 | 2.2 [0.44-23] | 0.21 | 7.9e+02 |
| B-bed | L6+L7 | b + transfer factor before P (S13) | 0.62 | 2.2 [0.44-23] | 0.21 | 7.9e+02 |
| B-bed | L6+L7 | c + stirring factor sampled (S13) | 0.62 | 2.2 [0.44-23] | 0.21 | 7.9e+02 |
| B-bed | L6+L7 | d + thin-layer cell default (S9) | 0.71 | 2.8 [0.59-23] | 0.12 | 7.9e+02 |
| B-bed | L6+L7 | e + Ki override UNVERIFIED 0.2 uM-1 mM (S10) = revised | 0.71 | 2.8 [0.59-23] | 0.11 | 7.9e+02 |
