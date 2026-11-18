# Earlier designs of docs/05 with the hydroquinone half-life of the tier round

Audited model (`src/elisa_sim`), designs of `scripts/final_designs.py` (variant after the final review), as specified (scenario S0), n = 2000, seed 20261111. P(success) is the criterion of docs/05.

| Design | Half-life of hydroquinone | LOD nominal (pg/mL) | LOD median [5-95 %] | P(LOD <= 1) | P(success) |
|---|---|---|---|---|---|
| P-chamb | 7200 s [1800-72000] (model) | 0.598 | 3.49 [0.512-157] | 0.172 | 0.156 |
| P-chamb | 600 s [120-7200] (tier round) | 0.62 | 3.46 [0.515-137] | 0.174 | 0.154 |
| B-bed | 7200 s [1800-72000] (model) | 0.854 | 3.41 [0.654-32.8] | 0.123 | 0.085 |
| B-bed | 600 s [120-7200] (tier round) | 0.989 | 3.89 [0.752-34] | 0.101 | 0.062 |
