"""Mass-transport sub-models.

1. ``march_conversion`` - steady laminar convection-diffusion in a tube (Poiseuille) or a slit channel
   (plane Poiseuille, one active wall, opposite wall inert), axial diffusion neglected (Pe >> 1), wall
   either a perfect sink (detection electrode) or a first-order reactive wall (capture surface, Robin
   condition D dc/dn = k_r c).  Solved by implicit marching (theta scheme) on a wall-clustered grid.
   One march gives the single-pass conversion as a function of the dimensionless length
       tube: xi = z D / (U R^2) = pi z D / Q          slit: xi = x D / (U H^2) = x D w / (Q H)
   for one Damkoehler number Da = k_r R / D (tube) or k_r H / D (slit).  Results are tabulated and
   interpolated (``conversion``).
2. ``loop_transfer`` - transient 2-D axisymmetric transport of an injected plug out of the sample loop
   (Poiseuille advection, TVD van Leer flux limiter; radial diffusion implicit).  Re-implementation of the
   Task 2 calculation (docs/02 section 2.4c).
3. Algebraic correlations: packed-bed mass-transfer coefficient (Wilson-Geankoplis), diffusion-limited
   collision rate to a sphere (Smoluchowski), Levich channel equation, Yamada-Matsuda wall-jet equation,
   Aoki interdigitated-array steady-state current, tanks-in-series elution.

Validity limits are stated in docs/03_simulation_model.md section 3.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.interpolate import RegularGridInterpolator
from scipy.linalg import solve_banded
from scipy.special import gammainc

from . import constants as K


# --------------------------------------------------------------------------------------------------
# 1. steady marching solver
# --------------------------------------------------------------------------------------------------
def _clustered_grid(n: int, wall_spacing: float) -> np.ndarray:
    """Points s in [0, 1] clustered near s = 0 (geometric stretching), first spacing ~ wall_spacing."""
    # find growth ratio r such that wall_spacing * (r^(n-1) - 1)/(r - 1) = 1
    lo, hi = 1.0 + 1e-9, 2.0
    for _ in range(200):
        r = 0.5 * (lo + hi)
        total = wall_spacing * (r ** (n - 1) - 1.0) / (r - 1.0)
        if total > 1.0:
            hi = r
        else:
            lo = r
    steps = wall_spacing * r ** np.arange(n - 1)
    s = np.concatenate([[0.0], np.cumsum(steps)])
    return s / s[-1]


def _set_row(ab, i, nb, coef):
    """Make row i of a banded tridiagonal matrix read  c_i + coef * c_nb = rhs_i."""
    n = ab.shape[1]
    ab[1, i] = 1.0
    if i + 1 < n:
        ab[0, i + 1] = 0.0
    if i - 1 >= 0:
        ab[2, i - 1] = 0.0
    if nb == i + 1:
        ab[0, i + 1] = coef
    else:
        ab[2, i - 1] = coef


def march_conversion(geometry: str, Da: float, xi_out: np.ndarray, n_grid: int = 220,
                     wall_spacing: float = 2e-5, n_steps: int = 1600, xi_start: float = 1e-10) -> np.ndarray:
    """Single-pass conversion (fraction of incoming solute removed at the wall) at the lengths ``xi_out``.

    geometry: "tube" or "slit".  Da = inf gives a perfect sink.
    """
    if geometry not in ("tube", "slit"):
        raise ValueError(geometry)
    s = _clustered_grid(n_grid, wall_spacing)          # distance from the active wall, 0..1
    if geometry == "tube":
        x = 1.0 - s[::-1]                               # radius rho: 0 (centre) .. 1 (wall)
        u = 2.0 * (1.0 - x ** 2)
        w = x.copy()                                    # cylindrical metric
        wall_idx, far_idx = len(x) - 1, 0
    else:
        x = s.copy()                                    # eta: 0 (active wall) .. 1 (inert wall)
        u = 6.0 * x * (1.0 - x)
        w = np.ones_like(x)
        wall_idx, far_idx = 0, len(x) - 1
    n = len(x)
    # mixing-cup weights (trapezoid on u*w)
    dx = np.diff(x)
    trap = np.zeros(n)
    trap[:-1] += 0.5 * dx
    trap[1:] += 0.5 * dx
    cup_w = trap * u * w
    cup_w /= cup_w.sum()

    # Laplacian operator L (tridiagonal), conservative finite volume with metric w
    lower = np.zeros(n)
    diag = np.zeros(n)
    upper = np.zeros(n)
    for i in range(1, n - 1):
        hm = x[i] - x[i - 1]
        hp = x[i + 1] - x[i]
        hc = 0.5 * (hm + hp)
        wm = 0.5 * (w[i] + w[i - 1])
        wp = 0.5 * (w[i] + w[i + 1])
        wi = w[i]
        a = wm / (hm * hc * wi)
        c = wp / (hp * hc * wi)
        lower[i] = a
        upper[i] = c
        diag[i] = -(a + c)

    c_now = np.ones(n)
    if not np.isfinite(Da):
        c_now[wall_idx] = 0.0
    xis = np.concatenate([[0.0], np.geomspace(xi_start, max(xi_out.max(), xi_start * 10), n_steps)])
    conv_hist = np.zeros(len(xis))
    conv_hist[0] = 0.0

    for k in range(1, len(xis)):
        dxi = xis[k] - xis[k - 1]
        theta = 1.0 if k < 20 else 0.5
        # rows: u/dxi c_new - theta L c_new = u/dxi c_old + (1-theta) L c_old
        # banded storage for solve_banded((1,1)): ab[0, j] = a[j-1, j], ab[1, j] = a[j, j], ab[2, j] = a[j+1, j]
        Lc = np.zeros(n)
        Lc[1:-1] = lower[1:-1] * c_now[:-2] + diag[1:-1] * c_now[1:-1] + upper[1:-1] * c_now[2:]
        ab = np.zeros((3, n))
        ab[1, :] = u / dxi - theta * diag
        ab[0, 1:] = -theta * upper[:-1]
        ab[2, :-1] = -theta * lower[1:]
        rhs = u / dxi * c_now + (1.0 - theta) * Lc
        # active wall (u = 0): algebraic Robin / Dirichlet condition
        nb = wall_idx + 1 if wall_idx == 0 else wall_idx - 1
        h = abs(x[nb] - x[wall_idx])
        coef = -1.0 / (1.0 + Da * h) if np.isfinite(Da) else 0.0
        _set_row(ab, wall_idx, nb, coef)
        rhs[wall_idx] = 0.0
        if geometry == "slit":
            # inert wall (u = 0): zero gradient
            _set_row(ab, far_idx, far_idx - 1, -1.0)
            rhs[far_idx] = 0.0
        else:
            # tube axis: L c = 4 (c1 - c0)/h^2 (L'Hopital), convective node
            h0 = x[1] - x[0]
            a0 = 4.0 / h0 ** 2
            ab[1, 0] = u[0] / dxi + theta * a0
            ab[0, 1] = -theta * a0
            rhs[0] = u[0] / dxi * c_now[0] + (1.0 - theta) * a0 * (c_now[1] - c_now[0])
        c_now = solve_banded((1, 1), ab, rhs)
        conv_hist[k] = 1.0 - float(cup_w @ c_now)
    return np.interp(xi_out, xis, conv_hist)


# tabulation grids (numerical settings, not physics)
_XI_TABLE = np.geomspace(1e-7, 50.0, 241)
_DA_TABLE = np.concatenate([np.geomspace(1e-4, 1e4, 33)])


CACHE_DIR = Path(__file__).resolve().parents[2] / "results" / "cache"


def _cached(name: str, builder):
    """Load an array table from results/cache (regenerable, git-ignored) or build and store it."""
    path = CACHE_DIR / f"{name}.npy"
    if path.exists():
        try:
            return np.load(path)
        except Exception:
            pass
    arr = builder()
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        np.save(path, arr)
    except OSError:
        pass
    return arr


@lru_cache(maxsize=None)
def _table(geometry: str):
    def build():
        rows = [march_conversion(geometry, float(da), _XI_TABLE) for da in _DA_TABLE]
        rows.append(march_conversion(geometry, np.inf, _XI_TABLE))
        return np.array(rows)
    arr = np.clip(_cached(f"march_{geometry}_v1", build), 1e-15, 1.0 - 1e-15)
    y = np.log(-np.log(1.0 - arr))                    # smooth transform
    da_axis = np.log10(np.concatenate([_DA_TABLE, [1e8]]))
    return RegularGridInterpolator((da_axis, np.log10(_XI_TABLE)), y, bounds_error=False, fill_value=None)


def conversion(geometry: str, xi, Da):
    """Interpolated single-pass wall conversion for arrays xi, Da (Da = inf -> perfect sink).

    Outside the tabulated xi range the conversion is extrapolated with the asymptotic power laws
    (kinetic or Leveque) through the smooth transform; xi above the table gives the tabulated end value
    extrapolated linearly in ln(-ln(1-f)) which tends to complete conversion.
    """
    xi = np.asarray(xi, dtype=float)
    Da = np.asarray(Da, dtype=float)
    xi_b, da_b = np.broadcast_arrays(xi, Da)
    lda = np.log10(np.where(np.isfinite(da_b), np.clip(da_b, _DA_TABLE[0], 1e8), 1e8))
    lxi = np.log10(np.clip(xi_b, 1e-12, 1e6))
    pts = np.stack([lda.ravel(), lxi.ravel()], axis=-1)
    y = _table(geometry)(pts).reshape(xi_b.shape)
    f = 1.0 - np.exp(-np.exp(y))
    # kinetic limit for very small Da below the table (f -> 1 - exp(-a Da xi)); a = 2 (tube) or 1 (slit)
    a = 2.0 if geometry == "tube" else 1.0
    small = np.isfinite(da_b) & (da_b < _DA_TABLE[0])
    if np.any(small):
        f = np.where(small, 1.0 - np.exp(-a * da_b * xi_b), f)
    return f


def leveque_slit_conversion(zeta):
    """Small-zeta (Leveque/Levich) limit of the slit perfect-sink conversion: 1.468 zeta^(2/3).

    Derived from the Levich channel equation with h = H/2 and electrode width = channel width.
    """
    return K.LEVICH_CHANNEL_COEFF * 4.0 ** (1.0 / 3.0) * np.asarray(zeta) ** (2.0 / 3.0)


def graetz_tube_remaining(x_star):
    """Perfect-sink Graetz series: mixing-cup c/c0 after dimensionless length x* = pi D z / (4 Q)."""
    x_star = np.asarray(x_star, dtype=float)
    out = np.zeros_like(x_star)
    for g, lam in zip(K.GRAETZ_TUBE_COEFFS, K.GRAETZ_TUBE_EXPONENTS):
        out = out + g * np.exp(-lam * x_star)
    return out


# --------------------------------------------------------------------------------------------------
# 2. loop transfer (transient)
# --------------------------------------------------------------------------------------------------
def loop_transfer(beta: float, plug_fraction: float, plug_at_outlet: bool, n_volumes,
                  nr: int = 24, nz: int = 320, cfl: float = 0.8, return_mass: bool = False):
    """Fraction of an injected plug that has left a laminar loop after n loop volumes of flushing, and the
    peak outlet (mixing-cup) concentration relative to the plug concentration.

    beta = D * V_loop / (Q * R^2) = (loop residence time) / (radial diffusion time); plug_fraction = plug
    volume / loop volume; plug_at_outlet: plug adjacent to the loop outlet (else at the far/inlet end).
    Dimensionless: z in [0, 1] (loop length), r in [0, 1] (radius), t in loop residence times.
    """
    n_volumes = np.atleast_1d(np.asarray(n_volumes, dtype=float))
    t_end = float(n_volumes.max())
    dr = 1.0 / nr
    r = (np.arange(nr) + 0.5) * dr                      # cell centres
    u = 2.0 * (1.0 - r ** 2)                            # Poiseuille, mean 1
    area = 2.0 * r * dr                                 # annulus area fraction (sum = 1)
    dz = 1.0 / nz
    zc = (np.arange(nz) + 0.5) * dz
    c = np.zeros((nr, nz))
    if plug_at_outlet:
        c[:, zc >= 1.0 - plug_fraction] = 1.0
    else:
        c[:, zc <= plug_fraction] = 1.0
    total0 = float((area[:, None] * c).sum() * dz)

    # implicit radial diffusion matrix (finite volume, no-flux at wall and axis)
    dt = cfl * dz / u.max()
    rf = np.arange(nr + 1) * dr                         # faces
    coef_lo = beta * dt * rf[:-1] / (r * dr * dr)
    coef_hi = beta * dt * rf[1:] / (r * dr * dr)
    coef_hi[-1] = 0.0                                   # wall no-flux
    coef_lo[0] = 0.0                                    # axis
    ab = np.zeros((3, nr))
    ab[1] = 1.0 + coef_lo + coef_hi
    ab[0, 1:] = -coef_hi[:-1]
    ab[2, :-1] = -coef_lo[1:]

    exited = 0.0
    t = 0.0
    times = [0.0]
    exited_hist = [0.0]
    cout_hist = [0.0]
    while t < t_end - 1e-12:
        # advection with van Leer limiter, inflow c = 0 at z = 0, outflow at z = 1
        cpad = np.concatenate([np.zeros((nr, 2)), c, c[:, -1:]], axis=1)   # ghost cells
        d1 = cpad[:, 1:-1] - cpad[:, :-2]
        d2 = cpad[:, 2:] - cpad[:, 1:-1]
        with np.errstate(divide="ignore", invalid="ignore"):
            rr = np.where(np.abs(d2) > 1e-30, d1 / d2, 0.0)
        phi = (rr + np.abs(rr)) / (1.0 + np.abs(rr))
        # face values at right faces of cells -1..nz-1 (upwind = left cell since u > 0)
        cface = cpad[:, 1:-1] + 0.5 * phi * d2 * (1.0 - u[:, None] * dt / dz)
        flux = u[:, None] * cface                         # faces: left of cell 0 ... right of cell nz-1
        out_flux = flux[:, -1]
        c = c - dt / dz * (flux[:, 1:] - flux[:, :-1])
        exited += float((area * out_flux).sum() * dt)
        # radial diffusion (implicit, all columns at once)
        c = solve_banded((1, 1), ab, c)
        t += dt
        times.append(t)
        exited_hist.append(exited)
        cout_hist.append(float((area * out_flux).sum()))  # flow-weighted outlet conc (u mean = 1)
    times = np.array(times)
    frac = np.interp(n_volumes, times, np.array(exited_hist)) / total0
    peak = float(np.max(cout_hist))
    if return_mass:
        remaining = float((area[:, None] * c).sum() * dz)
        return frac, peak, dict(initial=total0, exited=exited, remaining=remaining)
    return np.clip(frac, 0.0, 1.0), peak


_BETA_TABLE = np.geomspace(1e-3, 3.0, 13)
_NVOL_TABLE = np.linspace(0.25, 6.0, 47)


@lru_cache(maxsize=None)
def _loop_table(plug_fraction: float, plug_at_outlet: bool):
    def build():
        out = np.zeros((len(_BETA_TABLE), len(_NVOL_TABLE) + 1))
        for i, b in enumerate(_BETA_TABLE):
            out[i, :-1], out[i, -1] = loop_transfer(float(b), plug_fraction, plug_at_outlet, _NVOL_TABLE)
        return out
    tab = _cached(f"loop_pf{plug_fraction:.3f}_{'out' if plug_at_outlet else 'far'}_v1", build)
    return tab[:, :-1], tab[:, -1]


def loop_transfer_interp(beta, n_volumes, plug_fraction: float, plug_at_outlet: bool):
    """Vectorised lookup of (fraction transferred, peak outlet concentration ratio)."""
    pf = round(float(plug_fraction), 3)
    fr, pk = _loop_table(pf, bool(plug_at_outlet))
    beta = np.clip(np.asarray(beta, dtype=float), _BETA_TABLE[0], _BETA_TABLE[-1])
    n_volumes = np.clip(np.asarray(n_volumes, dtype=float), _NVOL_TABLE[0], _NVOL_TABLE[-1])
    interp = RegularGridInterpolator((np.log10(_BETA_TABLE), _NVOL_TABLE), fr)
    b, nv = np.broadcast_arrays(beta, n_volumes)
    frac = interp(np.stack([np.log10(b).ravel(), nv.ravel()], axis=-1)).reshape(b.shape)
    peak = np.interp(np.log10(beta), np.log10(_BETA_TABLE), pk)
    return frac, peak


def convective_loop_recovery(n_volumes):
    """D -> 0 limit for a loop initially full of sample: 1 - 1/(4 n) for n >= 1/2, else n (exact)."""
    n = np.asarray(n_volumes, dtype=float)
    return np.where(n >= 0.5, 1.0 - 1.0 / (4.0 * np.maximum(n, 1e-12)), n)


# --------------------------------------------------------------------------------------------------
# 3. correlations and closed-form expressions
# --------------------------------------------------------------------------------------------------
def wilson_geankoplis_k(D, d_p, eps, u_superficial, nu, coeff):
    """Packed-bed liquid-film mass-transfer coefficient (m/s): Sh = (coeff/eps) Re^(1/3) Sc^(1/3)."""
    Re = u_superficial * d_p / nu
    Sc = nu / D
    Sh = coeff / eps * Re ** (1.0 / 3.0) * Sc ** (1.0 / 3.0)
    return Sh * D / d_p, Re


def smoluchowski_rate(D, radius):
    """Diffusion-limited collision rate constant to a perfectly absorbing sphere, m^3/s per sphere."""
    return 4.0 * np.pi * D * radius


def levich_channel_current_per_conc(n_e, D, electrode_length, electrode_width, channel_height,
                                    channel_width, Q):
    """Levich channel-electrode limiting current per unit concentration (A per mol/m^3)."""
    h_half = 0.5 * channel_height
    return (K.LEVICH_CHANNEL_COEFF * n_e * K.FARADAY * electrode_width * electrode_length ** (2.0 / 3.0)
            * D ** (2.0 / 3.0) * (Q / (h_half ** 2 * channel_width)) ** (1.0 / 3.0))


def thin_layer_conversion(D, electrode_length, electrode_width, channel_height, channel_width, Q):
    """Single-pass conversion of a channel (thin-layer) electrode from the exact slit solution.

    zeta = D L w_ch / (Q H) for an electrode spanning the channel width; an electrode narrower than the
    channel converts the fraction (w_e / w_ch) of that (edge effects neglected).
    """
    zeta = D * electrode_length * channel_width / (Q * channel_height)
    f = conversion("slit", zeta, np.inf)
    return f * np.minimum(1.0, electrode_width / channel_width)


def wall_jet_conversion(D, nu, nozzle_diameter, electrode_radius, Q, coeff):
    """Wall-jet (Yamada-Matsuda form) conversion efficiency i/(n F c Q), capped at 1."""
    eta = (coeff * D ** (2.0 / 3.0) * nu ** (-5.0 / 12.0) * nozzle_diameter ** (-0.5)
           * electrode_radius ** 0.75 * Q ** (-0.25))
    return np.minimum(eta, 1.0)


def aoki_ida_current_per_conc(n_e, D, n_fingers, finger_length, finger_width, gap, c1, c2, c3):
    """Steady-state generator-collector current of an IDA per unit concentration (A per mol/m^3).

    i = m b n F c D [c1 ln(c2 (1 + w/g)) - c3 / (1 + w/g)^2]   (Aoki et al. 1988 fit; m = finger pairs).
    """
    ratio = 1.0 + finger_width / gap
    shape = c1 * np.log(c2 * ratio) - c3 / ratio ** 2
    return n_fingers * finger_length * n_e * K.FARADAY * D * shape


def tanks_in_series_eluted(volume_ratio, n_tanks):
    """Fraction eluted from a tanks-in-series (gamma) residence-time distribution after volume_ratio
    = V_flushed / V_void."""
    n_tanks = np.maximum(np.asarray(n_tanks, dtype=float), 1.0)
    return gammainc(n_tanks, n_tanks * np.asarray(volume_ratio, dtype=float))
