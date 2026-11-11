"""Small numerical helpers kept compatible with NumPy 1.24+ and 2.x."""
import numpy as np

trapz = getattr(np, "trapezoid", None) or np.trapz  # np.trapz was renamed np.trapezoid in NumPy 2.0
