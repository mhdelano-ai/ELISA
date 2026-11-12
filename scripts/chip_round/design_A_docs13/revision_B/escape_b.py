"""Escape of free HQ back into the read cell after the last removal (PE2), Revision B geometry (scratch).
Method of docs/15 rev15/escape.py: 1-D dead-end diffusion, c = 1 at the fill, sink at the stub mouth from the fill
until the end of PE2 (anything entering the cell before PE2 ends is oxidised by PE2), count the flux into the cell
from the end of PE2 to the start of the READ. D(HQ) = 9e-10 m2/s (chem.substrates.HQ.diffusion_coefficient; 7e-10
also run).  Times (min, own frame) from sched.py: fill = previous run's flush end 27.15, PE2 end 32.10, READ 52.75."""
import numpy as np, sys
mm = 1e-3; uL = 1e-9
def stub(L, A, Vend=0.0, D=9e-10, t_fill=27.15 * 60, t1=32.10 * 60, t2=52.75 * 60, n=50):
    dx = L / n; c = np.ones(n); cend = 1.0; dt = 0.2 * dx * dx / D; t = t_fill; out = 0.0
    while t < t2:
        cl = np.concatenate([[0.0], c, [cend if Vend > 0 else c[-1]]])
        flux = D * A * c[0] / (dx / 2)
        lap = (cl[2:] - 2 * cl[1:-1] + cl[:-2]) / dx ** 2
        lap[0] = (cl[2] - c[0]) / dx ** 2 - c[0] / (dx * dx / 2)
        if Vend > 0:
            cend += D * A * (c[-1] - cend) / dx * dt / Vend
        c = c + D * dt * lap
        if t1 <= t < t2: out += flux * dt
        t += dt
    return out
V_cell = 1.34 * uL   # RC 1.04 + in-die lane fingers 0.05 + 0.10 + WE2 channel 0.15 (electrolysed volume)
h = 0.175 * mm       # lane height under the TPE (channel sheet)
for D in (9e-10, 7e-10):
    print(f"D = {D:.0e} m2/s")
    cases = {
        "G3 stub 0.5 mm (0.5 x 0.175)": stub(0.5 * mm, 0.5 * mm * h, D=D),
        "G4 stub 0.5 mm (0.5 x 0.175)": stub(0.5 * mm, 0.5 * mm * h, D=D),
        "V14 stub 0.5 mm (0.3 x 0.175) behind WE2": stub(0.5 * mm, 0.3 * mm * h, D=D),
        "CE/RE neck 0.3 mm (0.2x0.2) + pocket 0.048 + V15 stub 0.026 uL": stub(0.3 * mm, 0.2 * mm * 0.2 * mm, Vend=0.074 * uL, D=D),
    }
    tot = 0.0
    for k, v in cases.items():
        tot += v; print(f"  {k:66s} {100 * v / V_cell:6.2f} % of the cell's initial free HQ")
    print(f"  TOTAL escape {100 * tot / V_cell:.2f} %")
    # sensitivity: 1.0 mm stubs (tolerance / plunger placement), and CE/RE pocket as in docs/13 (0.024 uL, neck 0.5)
    s1 = 2 * stub(1.0 * mm, 0.5 * mm * h, D=D) + stub(1.0 * mm, 0.3 * mm * h, D=D) + cases[list(cases)[3]]
    print(f"  sensitivity, all three stubs 1.0 mm: {100 * s1 / V_cell:.2f} %")
    # sensitivity: PE2 placed at the end of incubation instead (option B: PE2 end 26.4 with fill 27.15-31 ... not used)
