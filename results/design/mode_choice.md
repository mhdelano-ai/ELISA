# Mode choice against the detection reagent off-rate (docs/08 S4)

n = 2000, seed 20261111; k_off,detection pinned; final_designs default designs. Monte Carlo noise on a P difference between two designs evaluated with common random numbers is smaller than on each P, but differences below ~0.05 are not decision-grade (docs/08 W7).

| detection t1/2 (min) | k_off (1/s) | P-chamb (one-step) median / P | S-chamb (sequential) median / P | P difference (one-step - sequential) |
|---|---|---|---|---|
| 10 | 0.0012 | 7.1 / 0.04 | 3.1 / 0.12 | -0.08 |
| 13 | 0.00089 | 5 / 0.07 | 2.8 / 0.12 | -0.06 |
| 20 | 0.00058 | 3.3 / 0.12 | 2.6 / 0.13 | -0.02 |
| 30 | 0.00039 | 2.5 / 0.16 | 2.5 / 0.14 | +0.02 |
| 45 | 0.00026 | 2.1 / 0.19 | 2.4 / 0.14 | +0.05 |
| 60 | 0.00019 | 1.9 / 0.22 | 2.4 / 0.15 | +0.07 |
| 120 | 9.6e-05 | 1.7 / 0.25 | 2.3 / 0.15 | +0.10 |
