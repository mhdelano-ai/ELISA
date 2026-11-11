"""Reaction kinetics: enzyme turnover in a closed volume, and solution-phase sandwich formation.

All functions are vectorised over numpy broadcasting (parameter samples x calibration concentrations).
Integration is classical fixed-step RK4; step counts come from ``ma.numerics`` and convergence is tested.
"""
from __future__ import annotations

import numpy as np


def rk4(f, y0: list, t_end, steps: int):
    """Fixed-step RK4 for a list of arrays; t_end may be an array (broadcast)."""
    y = [np.asarray(v, dtype=float) for v in y0]
    h = np.asarray(t_end, dtype=float) / steps
    for _ in range(steps):
        k1 = f(y)
        k2 = f([a + 0.5 * h * b for a, b in zip(y, k1)])
        k3 = f([a + 0.5 * h * b for a, b in zip(y, k2)])
        k4 = f([a + h * b for a, b in zip(y, k3)])
        y = [a + h / 6.0 * (b1 + 2 * b2 + 2 * b3 + b4) for a, b1, b2, b3, b4 in zip(y, k1, k2, k3, k4)]
    return y


def enzyme_accumulation(E, S0, kcat, Km, t, *, Ki=np.inf, pi_per_product=1.0, k_hyd=0.0, k_decay=0.0,
                        P_bg0=0.0, steps=200):
    """Product formed by an enzyme in a closed, well-mixed volume (stopped flow).

    E (mol/m^3 enzyme), S0 substrate, Km, Ki (competitive inhibition by the co-product, e.g. phosphate for
    ALP, inhibitor concentration = pi_per_product x total product formed), k_hyd non-enzymatic substrate
    hydrolysis (1/s), k_decay first-order product loss (autoxidation, 1/s), P_bg0 product present at t = 0
    (free-product impurity).  Returns (P_enzymatic, P_background, S) at time t.

        v = kcat E S / (Km (1 + I/Ki) + S),  dS/dt = -v - k_hyd S,  I = pi_per_product (formed product)
    """
    S0 = np.asarray(S0, dtype=float)
    Ki = np.asarray(Ki, dtype=float)
    inv_Ki = np.where(np.isfinite(Ki), 1.0 / np.where(np.isfinite(Ki), Ki, 1.0), 0.0)

    def rhs(y):
        Pe, Pb, S, formed = y
        Sp = np.maximum(S, 0.0)
        v = kcat * E * Sp / (Km * (1.0 + pi_per_product * formed * inv_Ki) + Sp)
        vh = k_hyd * Sp
        return [v - k_decay * Pe, vh - k_decay * Pb, -v - vh, v + vh]

    zeros = np.zeros(np.broadcast(E, S0, kcat, Km, t).shape)
    Pe, Pb, S, _ = rk4(rhs, [zeros, zeros + P_bg0, zeros + S0, zeros], t, steps)
    return Pe, Pb, S


def mm_rate(E, S, kcat, Km):
    return kcat * E * S / (Km + S)


def integrated_mm_time(S0, S, Vmax, Km):
    """Time to go from S0 to S for uninhibited Michaelis-Menten (closed form, used in tests)."""
    return ((S0 - S) + Km * np.log(S0 / S)) / Vmax


def reversible_binding_fraction(k_on_pseudo, k_off, t):
    """Fraction of targets bound after time t for pseudo-first-order binding from zero (ligand in excess)."""
    k = k_on_pseudo + k_off
    return np.where(k > 0, k_on_pseudo / np.where(k > 0, k, 1.0) * (1.0 - np.exp(-k * t)), 0.0)


def one_step_sandwich(A0, C0, D0, kon_c, koff_c, kon_d, koff_d, t, steps=400):
    """Homogeneous one-step sandwich (analyte A, capture sites C, detection conjugate D), all mol/m^3.

    Species AC, AD, ACD; returns (ACD, AC, AD, free A) at time t.  Produces the high-dose hook effect when
    A0 approaches D0 (free analyte occupies the conjugate before it reaches captured analyte).
    """
    zeros = np.zeros(np.broadcast(A0, C0, D0, kon_c, kon_d, t).shape)

    def rhs(y):
        A, C, D, AC, AD, ACD = [np.maximum(v, 0.0) for v in y]
        r1 = kon_c * A * C - koff_c * AC
        r2 = kon_d * A * D - koff_d * AD
        r3 = kon_d * AC * D - koff_d * ACD
        r4 = kon_c * AD * C - koff_c * ACD
        return [-r1 - r2, -r1 - r4, -r2 - r3, r1 - r3, r2 - r4, r3 + r4]

    y = rk4(rhs, [zeros + A0, zeros + C0, zeros + D0, zeros, zeros, zeros], t, steps)
    A, C, D, AC, AD, ACD = y
    return ACD, AC, AD, A
