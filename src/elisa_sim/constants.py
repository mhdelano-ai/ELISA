"""Physical and mathematical constants.

Only exact SI defining constants and analytic (mathematical) results of classical transport problems live
here.  Every empirical coefficient (correlations, fitted constants) is a parameter in
``params/model_assumptions.yaml`` so that it carries a source, bounds and a confidence.
"""
import math

# SI defining constants (exact, 2019 SI)
AVOGADRO = 6.02214076e23          # 1/mol
FARADAY = 96485.33212             # C/mol (= e * N_A)
GAS_CONSTANT = 8.314462618        # J/(mol K)

# Analytic transport results (mathematical constants of the stated boundary-value problems)
# Leveque solution for the average flux to a perfectly absorbing wall strip in a parabolic channel flow,
# expressed as the Levich channel-electrode equation (Compton & Unwin; Levich 1962):
#   I = 0.925 n F c w x_e^(2/3) D^(2/3) (V_f / (h^2 d))^(1/3), h = channel HALF-height, d = channel width.
# The coefficient is the analytic Leveque constant; it is checked against an independent finite-difference
# solution in tests/test_transport.py.
LEVICH_CHANNEL_COEFF = 0.925

# Graetz problem, perfect-sink wall, fully developed Poiseuille flow in a tube (mixing-cup concentration):
#   c_b/c_0 = sum_k G_k exp(-lambda_k * x*), x* = pi D z / (4 Q)   (Shah & London 1978 eigen-solution)
GRAETZ_TUBE_COEFFS = (0.819050, 0.097527, 0.032504, 0.015440, 0.008788)
GRAETZ_TUBE_EXPONENTS = (14.6272, 89.2223, 212.2550, 388.3720, 617.5130)
GRAETZ_TUBE_NUSSELT_INF = 3.6568   # = lambda_1 / 4

LN2 = math.log(2.0)
