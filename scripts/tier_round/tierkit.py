"""tierkit - calculation kit of the three-tier round (docs/26).

The audited model (src/elisa_sim, docs/03, docs/04) covers bead and packed-bed formats behind isolation valves.
This kit adds, with the same parameters and the same blank statistics, the formats that the equipment in hand
allows without valves:

* ``evaluate_planar``  - capture on (or next to) the working electrode in a thin-layer flow cell; the enzyme
                         product is read at that electrode in the stopped cell (tier 1).
* ``evaluate_bed``     - capture on a small flow-through bed directly upstream of the cell; the product formed in
                         the stopped bed is swept through, or parked in, the cell (tier 2).

Tier 3 formats (valves, dosing, bead chamber) are evaluated with elisa_sim itself (scripts/tier_round/run_tiers.py).

Everything is SI inside.  Parameters come from params/*.yaml through elisa_sim.ParameterSet plus the new entries of
scripts/tier_round/tier_params.yaml (namespace ``tr.``).  Design choices (geometry, flows, times, reagent
concentrations) are passed in a plain dict and are never sampled.  Equations and validity limits: README.md.
"""
from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np
import yaml
from scipy.optimize import brentq
from scipy.sparse import coo_matrix, diags
from scipy.sparse.linalg import splu

from elisa_sim import constants as K
from elisa_sim import kinetics as kin
from elisa_sim import transport as tr
from elisa_sim.architectures import CHEMISTRIES
from elisa_sim.model import _blank_equiv, _interp_at, _lod_and_range, calibration_grid
from elisa_sim.params import ParameterSet, _flatten, validate
from elisa_sim.units import convert

NA = K.AVOGADRO
FARADAY = K.FARADAY
HERE = Path(__file__).resolve().parent
TIER_PARAMS = HERE / "tier_params.yaml"
UL = 1e-9            # m^3 per microlitre
ULMIN = 1e-9 / 60.0  # m^3/s per uL/min


# ----------------------------------------------------------------------------------------------------
# parameters
# ----------------------------------------------------------------------------------------------------
def load_params() -> ParameterSet:
    """Repository parameters (chem.*, hw.*, ma.*) plus this round's parameters (tr.*)."""
    base = ParameterSet.load()
    with open(TIER_PARAMS, "r") as fh:
        data = yaml.safe_load(fh)
    extra: dict = {}
    _flatten("tr", data, extra, origin=str(TIER_PARAMS))
    problems = [p for p in validate(extra) if "outside" in p]
    if problems:
        raise ValueError("tier_params.yaml bound errors:\n" + "\n".join(problems))
    params = dict(base.params)
    params.update(extra)
    return ParameterSet(params, base.extra)


class Ctx:
    """Parameter accessor; Monte Carlo arrays are reshaped to (n, 1) to broadcast against the calibration grid."""

    def __init__(self, ps: ParameterSet):
        self.ps = ps
        self.n = ps.n

    def __call__(self, key, unit):
        v = self.ps.get(key, unit)
        if isinstance(v, np.ndarray) and v.ndim == 1 and self.n:
            return v.reshape(-1, 1)
        return v

    def nominal(self, key, unit):
        """Best-estimate value regardless of sampling (used where a kernel is computed once per design)."""
        self.ps.accessed.add(key)
        prm = self.ps.params[key]
        return float(convert(prm.value, prm.unit, unit))


# ----------------------------------------------------------------------------------------------------
# B. capture on a planar patch under laminar flow;  C. capture in a stopped slab
# ----------------------------------------------------------------------------------------------------
def planar_flow_capture(D, k_r, h, w_channel, patch_length, patch_width, Q):
    """Fraction of ALL molecules passing the channel that is captured on a reactive patch on one wall.

    Rectangular channel (height h << width w_channel), fully developed laminar flow, patch of length
    patch_length (flow direction) and width patch_width <= w_channel, first-order surface reaction with velocity
    k_r = kon * (active sites per area) [m/s].  The stream lane above the patch (fraction patch_width / w_channel
    of the flow) is treated with the exact slit solution of elisa_sim.transport.conversion (one reactive wall):
    xi = L D w_ch / (Q h), Da = k_r h / D.  Lateral diffusion into the lane and side-wall effects are neglected
    (valid for w_channel >> h and patch_width >> h).  A disc of area A is represented by a square of side sqrt(A)
    (the Leveque flux to the disc is 1.03x that of the square, README B).
    """
    xi = patch_length * D * w_channel / (Q * h)
    Da = k_r * h / D
    lane = np.minimum(1.0, patch_width / w_channel)
    return tr.conversion("slit", xi, Da) * lane


def leveque_mass_transfer_coefficient(D, h, w_channel, patch_length, Q):
    """Average mass-transfer coefficient (m/s) to a perfectly absorbing strip, Leveque limit:
    k_m = 0.8076 (gamma D^2 / L)^(1/3) with wall shear rate gamma = 6 Q / (w h^2)."""
    gamma = 6.0 * Q / (w_channel * h ** 2)
    return 0.8076 * (gamma * D ** 2 / patch_length) ** (1.0 / 3.0)


def _robin_roots(Bi: float, n: int = 60) -> np.ndarray:
    """First n positive roots of beta tan(beta) = Bi."""
    roots = []
    for k in range(n):
        lo = k * np.pi + 1e-12
        hi = k * np.pi + 0.5 * np.pi - 1e-12
        roots.append(brentq(lambda b: b * np.tan(b) - Bi, lo, hi))
    return np.array(roots)


def slab_capture_fraction(D, k_r, h, t):
    """Fraction of the solute initially uniform in a stopped slab of height h that is taken up in time t by a
    reactive floor (first-order surface reaction k_r, m/s); the ceiling is inert.

    Crank, The Mathematics of Diffusion, eq. 4.53 (plane sheet with surface evaporation; half-sheet = slab with one
    reactive face):  1 - sum_n 2 Bi^2 exp(-b_n^2 D t / h^2) / (b_n^2 (b_n^2 + Bi^2 + Bi)),  b_n tan b_n = Bi = k_r h / D.
    Scalar D, k_r, h; t may be an array.
    """
    Bi = float(k_r * h / D)
    b = _robin_roots(Bi)
    T = np.asarray(t, float)[..., None] * D / h ** 2
    rem = np.sum(2.0 * Bi ** 2 * np.exp(-b ** 2 * T) / (b ** 2 * (b ** 2 + Bi ** 2 + Bi)), axis=-1)
    return 1.0 - rem


def kozeny_carman_dp(mu, u_superficial, d_p, eps, length):
    """Pressure drop (Pa) over a packed bed (Kozeny-Carman, laminar): 150 mu u (1-eps)^2 L / (eps^3 d_p^2)."""
    return 150.0 * mu * u_superficial * (1.0 - eps) ** 2 * length / (eps ** 3 * d_p ** 2)


# ----------------------------------------------------------------------------------------------------
# G. product transport in a stopped thin layer above a disc electrode (axisymmetric finite volumes)
# ----------------------------------------------------------------------------------------------------
class ThinLayer:
    """Diffusion in the stopped liquid layer 0 < r < R, 0 < z < h above a floor that carries a working-electrode
    disc of radius a (centre r = 0).  Ceiling and outer wall are inert.  Optionally an inlet bore of radius
    bore_radius < a and length bore_length opens through the ceiling above the electrode centre (wall-jet cells):
    it is part of the stopped liquid.  The electrode is either 'off' (no flux, open circuit) or 'on'
    (concentration zero at its surface: mass-transport-limited potential).

    Backward-Euler finite volumes (mass-conserving).  Linear problem: each source is run with unit strength and
    the results are superposed by the caller.
    """

    def __init__(self, a, h, R, D, bore_radius=0.0, bore_length=0.0, nr_in=36, nz=18, z_ratio=1.22,
                 r_growth=1.10, nz_bore=14):
        if R < a:
            raise ValueError("R must be >= a")
        has_bore = bore_radius > 0 and bore_length > 0
        if has_bore and not bore_radius < a:
            raise ValueError("bore_radius must be smaller than the electrode radius")
        self.a, self.h, self.R, self.D = float(a), float(h), float(R), float(D)
        self.rb, self.Lb = (float(bore_radius), float(bore_length)) if has_bore else (0.0, 0.0)
        if has_bore:
            n1 = max(4, int(round(nr_in * bore_radius / a)))
            inner = np.concatenate([np.linspace(0.0, bore_radius, n1 + 1),
                                    np.linspace(bore_radius, a, max(4, nr_in - n1) + 1)[1:]])
        else:
            inner = np.linspace(0.0, a, nr_in + 1)
        dr = a / nr_in
        faces = list(inner)
        step = dr
        while faces[-1] < R - 1e-12:
            step = min(step * r_growth, max(dr, R / 12.0))
            faces.append(min(R, faces[-1] + step))
        if len(faces) > len(inner) + 1 and faces[-1] - faces[-2] < 0.3 * dr:
            faces.pop(-2)
        self.rf = np.array(faces)
        self.rc = 0.5 * (self.rf[:-1] + self.rf[1:])
        g = z_ratio ** np.arange(nz)
        dz = h * g / g.sum()
        if has_bore:
            gb = 1.35 ** np.arange(nz_bore)
            dz = np.concatenate([dz, bore_length * gb / gb.sum()])
        self.nz_layer = nz
        self.zf = np.concatenate([[0.0], np.cumsum(dz)])
        self.zc = 0.5 * (self.zf[:-1] + self.zf[1:])
        self.dz = dz
        self.nr, self.nz = len(self.rc), len(dz)
        self.ring = np.pi * (self.rf[1:] ** 2 - self.rf[:-1] ** 2)          # floor area of each radial cell
        self.on_we = self.rf[1:] <= a * (1 + 1e-9)
        active = np.ones((self.nr, self.nz), bool)
        if has_bore:
            active[self.rf[1:] > bore_radius * (1 + 1e-9), nz:] = False      # above the ceiling only the bore is liquid
        self.active = active
        self.map = -np.ones((self.nr, self.nz), int)
        self.map[active] = np.arange(int(active.sum()))
        self.n = int(active.sum())
        self.vol = (self.ring[:, None] * dz[None, :])[active]
        self._build()
        self._lu = {}

    def _build(self):
        nr, nz, D, m = self.nr, self.nz, self.D, self.map
        rows, cols, vals = [], [], []
        diag = np.zeros(self.n)

        def link(k1, k2, G):
            rows.extend([k1, k2]); cols.extend([k2, k1]); vals.extend([-G, -G])
            diag[k1] += G; diag[k2] += G

        for i in range(nr):
            for j in range(nz):
                if m[i, j] < 0:
                    continue
                if i + 1 < nr and m[i + 1, j] >= 0:
                    link(m[i, j], m[i + 1, j],
                         D * 2.0 * np.pi * self.rf[i + 1] * self.dz[j] / (self.rc[i + 1] - self.rc[i]))
                if j + 1 < nz and m[i, j + 1] >= 0:
                    link(m[i, j], m[i, j + 1], D * self.ring[i] / (self.zc[j + 1] - self.zc[j]))
        self.L_off = (coo_matrix((vals, (rows, cols)), shape=(self.n, self.n)) + diags(diag)).tocsc()
        gs = np.zeros(self.n)
        for i in range(nr):
            if self.on_we[i]:
                gs[m[i, 0]] = D * self.ring[i] / (0.5 * self.dz[0])
        self.g_sink = gs
        self.L_on = (self.L_off + diags(gs)).tocsc()
        self.we_area = float(self.ring[self.on_we].sum())
        self.we_cells = np.array([m[i, 0] for i in range(nr) if self.on_we[i]])
        self.we_w = self.ring[self.on_we] / self.we_area

    def _solver(self, mode, dt):
        key = (mode, round(float(dt), 12))
        if key not in self._lu:
            L = self.L_on if mode == "on" else self.L_off
            self._lu[key] = splu((diags(self.vol / dt) + L).tocsc())
        return self._lu[key]

    # ---- sources (unit strength) -------------------------------------------------------------------
    def source_surface(self, where, r1, r2):
        """Uniform surface source of total strength 1 mol/s on the floor ('floor') or ceiling ('ceiling') between
        radii r1 and r2 (cells are weighted by their overlap with the annulus)."""
        lo = np.clip(self.rf[:-1], r1, r2)
        hi = np.clip(self.rf[1:], r1, r2)
        w = np.pi * (hi ** 2 - lo ** 2)
        if w.sum() <= 0:
            raise ValueError("empty source region")
        w = w / w.sum()
        s = np.zeros(self.n)
        j = 0 if where == "floor" else self.nz_layer - 1
        s[self.map[:, j]] = w
        return s

    def source_bore_wall(self):
        """Uniform source of total strength 1 mol/s on the wall of the inlet bore (over its modelled length)."""
        if self.rb <= 0:
            raise ValueError("no bore")
        i_b = int(np.max(np.nonzero(self.rf[1:] <= self.rb * (1 + 1e-9))[0]))
        s = np.zeros(self.n)
        w = self.dz[self.nz_layer:] / self.dz[self.nz_layer:].sum()
        s[self.map[i_b, self.nz_layer:]] = w
        return s

    def source_volume(self):
        """Uniform volumetric source of 1 mol/(m^3 s) everywhere in the liquid (layer and bore)."""
        return self.vol.copy()

    @property
    def volume(self):
        return float(self.vol.sum())

    # ---- time stepping -----------------------------------------------------------------------------
    def run(self, phases, source=None, c0=0.0, dt0=0.02, growth=1.12, steps_min=60):
        """phases: list of (mode, duration_s), mode 'on' or 'off'.  source: mol/s per cell (constant) or None.
        c0: initial uniform concentration (mol/m^3).  Returns dict of arrays over the step ends:
        t, rate (mol/s into the electrode), cum (mol collected), csurf (mean concentration in the cell layer on
        the electrode, mol/m^3), cint (time integral of csurf, mol s / m^3), mass (mol in the liquid)."""
        c = np.full(self.n, float(c0))
        src = np.zeros(self.n) if source is None else np.asarray(source, float)
        t, cum, cint = 0.0, 0.0, 0.0
        out = dict(t=[0.0], rate=[0.0], cum=[0.0], csurf=[float(self.we_w @ c[self.we_cells])], cint=[0.0],
                   mass=[float(self.vol @ c)])
        for mode, dur in phases:
            dt_max = dur / steps_min
            dt = min(dt0, dt_max)
            t_end = t + dur
            while t < t_end - 1e-9:
                step = min(dt, t_end - t)
                lu = self._solver(mode, step)
                c_old_surf = float(self.we_w @ c[self.we_cells])
                c = lu.solve(self.vol / step * c + src)
                rate = float(self.g_sink @ c) if mode == "on" else 0.0
                cs = float(self.we_w @ c[self.we_cells])
                t += step
                cum += rate * step
                cint += 0.5 * (c_old_surf + cs) * step
                for k, v in (("t", t), ("rate", rate), ("cum", cum), ("csurf", cs), ("cint", cint),
                             ("mass", float(self.vol @ c))):
                    out[k].append(v)
                dt = min(dt * growth, dt_max)
        return {k: np.array(v) for k, v in out.items()}


def _between(run, key, t1, t2):
    """Increase of a cumulative series (cum or cint) between t1 and t2."""
    return float(np.interp(t2, run["t"], run[key]) - np.interp(t1, run["t"], run[key]))


@lru_cache(maxsize=64)
def thin_layer_kernels(a, h, R, D, phases, regions, bore_radius=0.0, bore_length=0.0):
    """Unit-strength responses of a ThinLayer for a read protocol.

    phases: tuple of (mode, duration); regions: tuple of (name, where, r1, r2) surface sources.  Always adds
    'volume' (uniform volumetric source) and 'initial' (uniform initial concentration 1 mol/m^3).
    Returns (ThinLayer, {name: run dict}).
    """
    tl = ThinLayer(a, h, R, D, bore_radius, bore_length)
    runs = {}
    for name, where, r1, r2 in regions:
        runs[name] = tl.run(list(phases), source=tl.source_surface(where, r1, r2))
    if bore_radius > 0 and bore_length > 0:
        runs["bore"] = tl.run(list(phases), source=tl.source_bore_wall())
    runs["volume"] = tl.run(list(phases), source=tl.source_volume())
    runs["initial"] = tl.run(list(phases), c0=1.0)
    return tl, runs


def cycling_surface_velocity(D, k_reg, h):
    """Chemical (homogeneous) redox cycling at one electrode in a layer of height h.

    The product R is oxidised at the electrode and the oxidised form is reduced back in solution with the
    pseudo-first-order rate constant k_reg (1/s).  Total product (R + O) then only diffuses and is not consumed;
    where its concentration c_tot varies slowly over the reaction layer mu = sqrt(D / k_reg), the electrode flux
    is c_tot * sqrt(D k_reg) * tanh(h / mu)  (steady reaction-diffusion of R between an absorbing floor and an
    inert ceiling; limits: sqrt(D k_reg) for mu << h, k_reg h for mu >> h).  Returns the velocity (m/s).
    """
    mu = np.sqrt(D / k_reg)
    return np.sqrt(D * k_reg) * np.tanh(h / mu)


# ----------------------------------------------------------------------------------------------------
# result container and shared pieces of the assay chain
# ----------------------------------------------------------------------------------------------------
@dataclass
class TierResult:
    name: str
    conc_pgml: np.ndarray
    net_signal: np.ndarray
    blank_mean: np.ndarray
    blank_sd: np.ndarray
    lod_pgml: np.ndarray
    lod_slope_pgml: np.ndarray
    uloq_pgml: np.ndarray
    time_to_result_min: float
    variance_terms: dict
    diagnostics: dict = field(default_factory=dict)

    @property
    def limiting_term(self):
        names = list(self.variance_terms)
        stack = np.stack([np.broadcast_to(np.asarray(self.variance_terms[k], float), np.shape(self.blank_sd))
                          for k in names])
        return np.asarray(names, dtype=object)[np.argmax(stack, axis=0)]


def timing(design) -> tuple[float, list]:
    """Sum of the step table.  design['steps'] is a list of (name, minutes, counts) where counts is False for
    steps before the sample's Inject Start.  Returns (minutes from injection to result, the list)."""
    steps = design["steps"]
    total = sum(m for _n, m, counts in steps if counts)
    if total > 60.0 + 1e-9:
        warnings.warn(f"{design['name']}: {total:.1f} min from injection to result exceeds 60 min")
    return float(total), steps


def _sq(x):
    return np.squeeze(np.asarray(x, float), axis=-1) if np.ndim(x) and np.shape(x)[-1] == 1 else np.asarray(x, float)


def _delivery(design, p, conc):
    """Molecules of the calibration grid that leave the loop toward the capture zone during the loading step."""
    M = p("chem.analyte.molar_mass", "g/mol")
    V_s = p("ma.delivery.sample_volume", "m^3")
    C = convert(conc, "pg/mL", "g/m^3") / M                                   # mol/m^3
    N_vial = C * V_s * NA
    f_del = p("ma.delivery.delivered_fraction_full_loop_100", "fraction")
    loss = p("ma.delivery.adsorptive_loss_fraction_with_carrier", "fraction")
    V_loop = p("hw.smfl.loop_volume_recommended", "m^3")
    r_loop = 0.5 * p("hw.smfl.loop_inner_diameter", "m")
    D_igg = p("chem.analyte.diffusion_coefficient", "m^2/s")
    s = design["sample"]
    Q = s["Q_uL_min"] * ULMIN
    V_pass = Q * s["t_load_min"] * 60.0 - s.get("V_transit_uL", 0.0) * UL       # volume pushed through the loop
    n_flush = V_pass / V_loop
    beta = D_igg * V_loop / (Q * r_loop ** 2)
    at_outlet = bool(np.all(np.asarray(p("ma.delivery.plug_at_outlet_end", "boolean")) > 0.5))
    f_tr, _peak = tr.loop_transfer_interp(beta, n_flush, 1.0, at_outlet)       # full loop: position irrelevant
    cont = p("ma.nsb.blank_igg_contamination_equivalent", "mol/m^3") * V_s * NA
    return dict(N_vial=N_vial, N_in=N_vial * f_del * (1.0 - loss) * f_tr, f_del=f_del, loss=loss, f_transfer=f_tr,
                n_flush=n_flush, beta=beta, Q=Q, D_igg=D_igg, N_cont_vial=cont, V_loop=V_loop, r_loop=r_loop,
                chain=f_del * (1.0 - loss) * f_tr)


def _labelling(design, p, chem):
    """Labelled fraction of captured analyte, conjugate exposure integral and retention factors."""
    c = design["conjugate"]
    kon_d = p("chem.antibodies.kon_detection", "m^3/(mol*s)")
    koff_d = p("chem.antibodies.koff_detection", "1/s")
    koff_c = p("chem.antibodies.koff_capture", "1/s")
    C_vial = c["C_nM"] * 1e-6                                                # mol/m^3
    V = c["V_uL"] * UL
    Qc = c["Q_uL_min"] * ULMIN
    V_loop = p("hw.smfl.loop_volume_recommended", "m^3")
    r_loop = 0.5 * p("hw.smfl.loop_inner_diameter", "m")
    D_conj = p("chem.antibodies.diffusion_coefficient_IgG_ALP_conjugate", "m^2/s")
    pf = round(float(min(1.0, V / np.mean(np.asarray(V_loop, float)))), 2)
    at_outlet = bool(np.all(np.asarray(p("ma.delivery.plug_at_outlet_end", "boolean")) > 0.5))
    _f, peak = tr.loop_transfer_interp(D_conj * V_loop / (Qc * r_loop ** 2), 3.0, pf, at_outlet)
    dil = np.minimum(1.0, peak) * p("ma.delivery.tubing_dilution_factor", "fraction")
    t_stop = c.get("t_stop_min", 0.0) * 60.0
    t_flow = V / Qc                                                          # passage time of the plug
    exposure = C_vial * V / Qc + C_vial * dil * t_stop                       # mol s / m^3 (flow part exact)
    t_tot = t_flow + t_stop
    if not c.get("count_flow_exposure", True):                               # cross-check with elisa_sim only
        exposure, t_tot = C_vial * dil * t_stop, t_stop
    C_eff = exposure / t_tot
    f_label = kin.reversible_binding_fraction(kon_d * C_eff, koff_d, t_tot)
    ret_label = np.exp(-koff_d * design["exposure_s"]["label_to_read"])
    ret_capture = np.exp(-koff_c * design["exposure_s"]["capture_to_read"])
    enz = p(chem["enzymes_per_label"], "count")
    N_inj = C_vial * V * NA * enz
    return dict(f_label=f_label, exposure=exposure, ret_label=ret_label, ret_capture=ret_capture, enz=enz,
                N_conj_injected=N_inj, dilution=dil, C_eff=C_eff)


def _chem(p, chem):
    out = dict(kcat=p(chem["kcat"], "1/s"), Km=p(chem["Km"], "mol/m^3"), S0=p(chem["S0"], "mol/m^3"),
               imp=p(chem["impurity"], "mol/mol"), k_hyd=p(chem["hydrolysis"], "1/s"),
               k_dec=K.LN2 / p(chem["half_life"], "s"), n_e=p(chem["n_e"], "e-/molecule"),
               D_prod=p.nominal(chem["D_product"], "m^2/s"))
    if chem["Ki"]:
        out["Ki"] = p(chem["Ki"], "mol/m^3"); out["ppp"] = p(chem["pi_per_product"], "count")
    else:
        out["Ki"], out["ppp"] = np.inf, 1.0
    return out


def _free_product(p, ch):
    """Free (electroactive) product in the working substrate solution at the time of use, mol/m^3:
    (what is left of the lot's impurity, hydrolysis product formed in the reservoir).

    With tr.detection.reservoir_background_decays = 1 the product half-life at pH 9.5 holds in the reservoir as
    it does in the bed: the impurity decays over the reservoir age and the hydrolysis product stands at
    k_hyd S0 (1 - exp(-k t)) / k.  With 0 the impurity is free_product_impurity x S0 at the time of use and the
    hydrolysis product is k_hyd S0 t (audited model, docs/03)."""
    age = p("ma.timing.substrate_reservoir_age", "s")
    decays = bool(np.all(np.asarray(p("tr.detection.reservoir_background_decays", "boolean")) > 0.5))
    if decays:
        f = np.exp(-ch["k_dec"] * age)
        return ch["imp"] * ch["S0"] * f, ch["k_hyd"] * ch["S0"] * (1.0 - f) / ch["k_dec"]
    return ch["imp"] * ch["S0"], ch["k_hyd"] * ch["S0"] * age


def _noise(design, p, area, stopped, T_read, noise_factor=1.0, T_span=None):
    """Current noise and drift.  T_span: time between the centres of the two reference windows that bracket the
    read (default: the read window itself, as in the model).  The unremoved drift current is taken as
    f_res * drift * T_span / 2 and is integrated over the read window."""
    T_span = T_read if T_span is None else T_span
    i_ref = p("hw.gamry.noise_rms_stopped_flow" if stopped else "hw.gamry.noise_rms_flow", "A")
    A_ref = p("ma.noise.reference_electrode_area", "m^2")
    alpha = p("ma.noise.area_exponent", "dimensionless")
    floor = p("hw.gamry.antec_decade_floor_pp", "A") / p("ma.noise.pp_to_rms", "dimensionless")
    i_n = np.maximum(floor, i_ref * (area / A_ref) ** alpha) * noise_factor
    B = p("ma.noise.reference_bandwidth", "Hz")
    var_ec = (i_n * np.sqrt(T_read / (2.0 * B))) ** 2 * 2.0                   # signal window + reference window
    drift = p("hw.gamry.baseline_drift", "A/min") / 60.0 * (area / A_ref) ** p("tr.noise.drift_area_exponent",
                                                                                "dimensionless")
    var_drift = (p("ma.noise.drift_residual_fraction", "fraction") * 0.5 * drift * T_span * T_read) ** 2
    return i_n, var_ec, var_drift


def _sensor_cv(design, p):
    """Unit-to-unit CV of the electrode response (single-use electrodes) and whether a pre-read on the same
    electrode references it."""
    kind = design["electrode"]["kind"]
    if design.get("preread", False):
        return p("tr.noise.preread_residual_cv", "fraction")
    if kind == "printed":
        return p("ma.noise.spe_sensor_to_sensor_cv", "fraction")
    return p("tr.noise.thinfilm_sensor_to_sensor_cv", "fraction")


def _finish(design, p, conc, Q, enz, N_blank_enz, T_read, area, stopped, cv_unit, referenced, extra_diag,
            noise_factor=1.0):
    """Blank statistics (docs/03 section 3.6 with the unit-to-unit terms of single-use consumables), LOD, range.

    Q: dict of charges (C): spec (n, nc), nsb, carry, hyd, imp, cont, other_bg.  enz: charge per blank enzyme."""
    cv_nsb = p("chem.nsb.blank_CV_analog_electrochemical", "fraction")
    inj_rsd = p("hw.smfl.injection_precision_rsd_large", "fraction")
    cv_sub = p("ma.noise.substrate_background_cv", "fraction")
    rel_bg = p("ma.noise.background_current_relative_noise", "fraction")
    cv_carry = p("ma.noise.carryover_cv", "fraction")
    cv_sens = _sensor_cv(design, p)
    rd = design["read"]
    i_n, var_ec, var_drift = _noise(design, p, area, stopped, T_read, noise_factor, rd.get("t_span_s"))
    bg = Q["imp"] + Q["other_bg"]
    terms = {}
    terms["nsb_variability"] = (cv_nsb ** 2 + cv_unit ** 2 + inj_rsd ** 2) * Q["nsb"] ** 2
    terms["label_counting"] = enz ** 2 * N_blank_enz
    terms["carryover"] = (cv_carry * Q["carry"]) ** 2
    if referenced:
        terms["substrate_background"] = (cv_sub * Q["hyd"]) ** 2 + (rel_bg * (bg + Q["hyd"])) ** 2
        terms["electrode_sensitivity"] = (cv_sens * (Q["nsb"] + Q["carry"] + Q["hyd"])) ** 2
    else:
        terms["substrate_background"] = (cv_sub * (bg + Q["hyd"])) ** 2 + (rel_bg * (bg + Q["hyd"])) ** 2
        terms["electrode_sensitivity"] = (cv_sens * (Q["nsb"] + Q["carry"] + Q["hyd"] + bg)) ** 2
    if referenced and rd.get("reference_far", False):
        # the substrate background is taken from a pre-read on the same electrode, made before the sample: its
        # transfer over that time (protein now on the electrode, flow, reference) is not exact
        terms["substrate_background"] = terms["substrate_background"] + (
            p("tr.noise.preread_residual_cv", "fraction") * (bg + Q["hyd"])) ** 2
    if rd.get("baseline_step", False):
        # swept read after a stop in a cell whose electrode was on: the impurity current is absent before the
        # peak and present after it; the step is removed with the trace of the pre-run, not exactly
        terms["substrate_background"] = terms["substrate_background"] + (
            p("tr.noise.swept_step_residual_cv", "fraction") * Q["imp"]) ** 2
    terms["electrochemical_noise"] = var_ec + 0.0 * Q["nsb"]
    terms["baseline_drift"] = var_drift + 0.0 * Q["nsb"]
    terms["contamination"] = Q["cont"] ** 2
    terms = {k: _sq(v) for k, v in terms.items()}
    blank_sd = np.sqrt(sum(terms.values()))
    blank_mean = _sq(Q["nsb"] + Q["carry"] + Q["hyd"] + Q["cont"] + (0.0 if referenced else bg))
    net = np.asarray(Q["spec"], float)
    net = net - net[..., :1]
    k_sd = p("ma.statistics.k_sd", "dimensionless")
    lod, lod_slope, uloq = _lod_and_range(conc, net, k_sd * blank_sd,
                                          p("ma.statistics.uloq_min_log_slope", "dimensionless"))
    total_min, _steps = timing(design)
    diag = dict(extra_diag)
    diag.update(noise_rms_A=_sq(i_n), signal_at_1pg_C=_interp_at(conc, net, 1.0),
                blank_equivalent_pgml=_blank_equiv(conc, net, blank_mean), sensor_cv=_sq(cv_sens),
                Q_nsb_C=_sq(Q["nsb"]), Q_imp_C=_sq(Q["imp"]), Q_hyd_C=_sq(Q["hyd"]), Q_other_bg_C=_sq(Q["other_bg"]),
                Q_carry_C=_sq(Q["carry"]))
    diag = {k: (np.squeeze(v) if isinstance(v, np.ndarray) else v) for k, v in diag.items()}
    return TierResult(name=design["name"], conc_pgml=conc, net_signal=net, blank_mean=blank_mean, blank_sd=blank_sd,
                      lod_pgml=lod, lod_slope_pgml=lod_slope, uloq_pgml=uloq, time_to_result_min=total_min,
                      variance_terms=terms, diagnostics=diag)


def _grid(p, conc):
    conc = calibration_grid(p) if conc is None else np.asarray(conc, float)
    if conc[0] != 0.0:
        conc = np.concatenate([[0.0], conc])
    return conc


# ----------------------------------------------------------------------------------------------------
# tier 1: capture on the working electrode, read in the stopped cell
# ----------------------------------------------------------------------------------------------------
def cell_conversion(cell, D, area, Q):
    """Fraction of a solute stream that reacts at a transport-limited electrode of the given area.

    'radial' (wall-jet cell with a thin gap, the Micrux flow add-ons): the whole stream enters through the bore
    above the electrode centre and leaves radially through the gap of height h.  For creeping parabolic flow the
    convection-diffusion problem in the swept area s = pi (r^2 - r_bore^2) is identical to the slit problem in
    w x (README B), so the exact slit solution is used with xi = D s / (Q h); the stagnation zone under the bore
    is not counted.  'channel': cross-flow thin-layer cell, elisa_sim.transport.thin_layer_conversion.
    """
    h = cell["h"]
    if cell.get("flow_geometry", "radial") == "radial":
        s_eff = max(area - np.pi * cell.get("bore_radius", 0.0) ** 2, 0.0)
        return tr.conversion("slit", D * s_eff / (Q * h), np.inf)
    side = np.sqrt(area)
    return tr.thin_layer_conversion(D, side, side, h, cell["w_channel"], Q)


def evaluate_planar(design: dict, ps: ParameterSet, conc_pgml=None) -> TierResult:
    """Capture antibody on the working electrode (and optionally on the floor around it); the enzyme product is
    read at that electrode (tier 1).

    design keys (all SI unless the name carries a unit):
      name, steps, exposure_s{capture_to_read, label_to_read}, chemistry
      cell      : flow_geometry ('radial' wall-jet thin gap, default | 'channel'), h (gap height),
                  R (radius of the liquid layer = O-ring inner radius), bore_radius, bore_length (inlet bore above
                  the electrode; radial only), w_channel (channel only), lid_factor_key (NSB factor of the lid)
      electrode : kind ('printed' | 'thinfilm'), area, we_factor_key (NSB factor of the electrode surface),
                  floor_factor_key (NSB factor of the floor around it), collection_key (optional: parameter with
                  the fraction of the transport-limited current a coated electrode delivers)
      capture   : site_factor_key (parameter: active capture sites relative to an oriented monolayer),
                  ring_width (m; capture coating also on the floor ring a < r < a + ring_width; 0 = electrode only)
      sample    : Q_uL_min, t_load_min, V_transit_uL, mode ('flow' | 'stop_go'), dwell_s (stop_go)
      conjugate : C_nM, V_uL, Q_uL_min, t_stop_min
      read      : mode ('steady' stopped, electrode on | 'steady_flow' electrode on, substrate flowing |
                  'accumulate_step' | 'cycling' | 'ida'), t_wait_s (electrode on before the read window),
                  t_acc_s (accumulate_step), t_read_s, Q_read_uL_min (steady_flow), k_reg (cycling, 1/s),
                  ida (dict m, b, w, g; mode 'ida'), two_electrode (bool)
      preread   : bool - a substrate background read on the same electrode before the sample injection
      upstream  : optional dict(bore_factor_key, line_area, line_factor_key) - walls between injector and
                  electrode that saw the conjugate: the inlet bore (area from the cell geometry) and the transfer
                  line.  Their product reaches the electrode with the stream (collected at the stream conversion)
                  or, in a stopped cell, by diffusion out of the bore.
      read also : t_span_s (time between the centres of the two reference windows that bracket the read),
                  reference_far (True if the substrate background comes from a pre-read before the sample)
    """
    p = Ctx(ps)
    chem = CHEMISTRIES[design["chemistry"]]
    conc = _grid(p, conc_pgml)
    cell, el, cap, rd = design["cell"], design["electrode"], design["capture"], design["read"]
    A_we = el["area"]
    a = np.sqrt(A_we / np.pi)
    h, R = cell["h"], cell["R"]
    radial = cell.get("flow_geometry", "radial") == "radial"
    rb = cell.get("bore_radius", 0.0) if radial else 0.0
    Lb = cell.get("bore_length", 0.0) if radial else 0.0

    # 1-2. delivery and capture
    d = _delivery(design, p, conc)
    gamma = (p("chem.surfaces.igg_surface_density_monolayer", "molecules/m^2")
             * p("chem.surfaces.active_fraction_oriented", "fraction") / NA) * p(cap["site_factor_key"], "fraction")
    k_r = p("chem.antibodies.kon_capture", "m^3/(mol*s)") * gamma
    ring_w = cap.get("ring_width", 0.0)
    A_patch = np.pi * (a + ring_w) ** 2
    Da = k_r * h / d["D_igg"]
    stop_go = design["sample"].get("mode", "flow") == "stop_go"
    if stop_go:
        dwell = design["sample"]["dwell_s"]
        D0 = p.nominal("chem.analyte.diffusion_coefficient", "m^2/s")
        k0 = float(np.mean(np.asarray(k_r, float)))
        V_seg = np.pi * R ** 2 * h if radial else (np.sqrt(A_patch) * cell["w_channel"] * h)
        foot = np.pi * R ** 2 if radial else np.sqrt(A_patch) * cell["w_channel"]
        f_patch = slab_capture_fraction(D0, k0, h, dwell) * min(1.0, A_patch / foot) + 0.0 * k_r
        share_we = A_we / A_patch
        need = np.max(np.asarray(d["n_flush"], float)) * float(np.mean(np.asarray(d["V_loop"], float))) / V_seg \
            * (dwell + V_seg / d["Q"]) / 60.0
        if need > design["sample"]["t_load_min"] * 1.02:
            warnings.warn(f"{design['name']}: stop-and-go needs {need:.0f} min for the plug, more than t_load")
        k_m = np.nan
    elif radial:
        s_we = max(A_we - np.pi * rb ** 2, 0.0)
        s_patch = A_patch - np.pi * rb ** 2
        f_we = tr.conversion("slit", d["D_igg"] * s_we / (d["Q"] * h), Da)
        f_patch = tr.conversion("slit", d["D_igg"] * s_patch / (d["Q"] * h), Da) if ring_w > 0 else f_we
        share_we = f_we / f_patch
        k_m = tr.conversion("slit", d["D_igg"] * s_we / (d["Q"] * h), np.inf) * d["Q"] / A_we
    else:
        side = np.sqrt(A_patch)
        w_c = cell["w_channel"]
        f_patch = planar_flow_capture(d["D_igg"], k_r, h, w_c, side, min(w_c, side), d["Q"])
        share_we = A_we / A_patch
        k_m = leveque_mass_transfer_coefficient(d["D_igg"], h, w_c, side, d["Q"])
    N_cap = f_patch * d["N_in"]

    # 3-4. labelling and retention
    lab = _labelling(design, p, chem)
    N_spec = N_cap * lab["ret_capture"] * lab["f_label"] * lab["ret_label"] * lab["enz"]
    N_spec_we, N_spec_ring = N_spec * share_we, N_spec * (1.0 - share_we)

    # 5. non-specific label on the electrode, the floor around it and the lid
    k_nsb = p("chem.nsb.nsb_effective_rate_constant", "m/s") * p(chem["label_nsb_factor"], "fold") \
        * p("ma.labelling.detection_on_capture_residual_factor", "fold")
    per_area = k_nsb * lab["exposure"] * NA * lab["enz"]                       # enzymes per m^2 at surface factor 1
    sf_we = p(el["we_factor_key"], "fold")
    A_floor = np.pi * R ** 2 - A_we
    A_lid = np.pi * (R ** 2 - rb ** 2)
    N_nsb_we = per_area * sf_we * A_we
    N_nsb_floor = per_area * p(el["floor_factor_key"], "fold") * A_floor
    N_nsb_lid = per_area * p(cell["lid_factor_key"], "fold") * A_lid
    up = design.get("upstream") or {}
    N_up_bore = per_area * p(up["bore_factor_key"], "fold") * 2.0 * np.pi * rb * Lb if (up and rb > 0) else 0.0
    N_up_line = per_area * p(up["line_factor_key"], "fold") * up.get("line_area", 0.0) if up else 0.0

    # 6. conjugate carried into the next determination's sample injection (fresh electrode each time)
    c_inj = p("hw.smfl.carryover_protein_conjugate", "fraction")
    uptake = 1.0 - np.exp(-k_nsb * sf_we * A_we / d["Q"])
    N_carry = c_inj ** 2 * lab["N_conj_injected"] * uptake

    # 7. enzyme turnover (substrate in large excess at the surface; product stays far below Ki)
    ch = _chem(p, chem)
    v = ch["kcat"] * ch["S0"] / (ch["Km"] + ch["S0"])                          # product molecules per enzyme per s
    nF = ch["n_e"] * FARADAY
    c_imp, c_hyd_res = _free_product(p, ch)                                   # mol/m^3 in the working solution
    hyd = ch["k_hyd"] * ch["S0"]                                              # mol/(m^3 s) inside the cell

    # 8. read
    mode = rd["mode"]
    T = rd["t_read_s"]
    regions = (("we", "floor", 0.0, a), ("floor", "floor", a, R), ("lid", "ceiling", rb, R))
    if ring_w > 0:
        regions = regions + (("ring", "floor", a, min(R, a + ring_w)),)
    other_bg, noise_factor, stopped = 0.0, 1.0, True
    if mode == "steady":
        t1 = rd.get("t_wait_s", 0.0)
        _tl, kr = thin_layer_kernels(a, h, R, ch["D_prod"], (("on", t1 + T),), regions, rb, Lb)
        g = {k: _between(r, "cum", t1, t1 + T) for k, r in kr.items()}        # mol collected per unit source
        col = dict(we=T, floor=g["floor"], lid=g["lid"], ring=g.get("ring", 0.0), bore=g.get("bore", 0.0), line=0.0)
        q_vol, q_init = nF * g["volume"], nF * g["initial"]
    elif mode == "steady_flow":
        Qr = rd["Q_read_uL_min"] * ULMIN
        eta = float(cell_conversion(cell, ch["D_prod"], A_we, Qr))
        # product formed on the lid above the electrode crosses the gap while it is carried outward: about half
        # of the inlet-stream conversion (approximation); the floor ring is downstream of the electrode
        col = dict(we=T, floor=0.0, lid=0.5 * eta * T * max(A_we - np.pi * rb ** 2, 0.0) / A_lid, ring=0.0,
                   bore=eta * T, line=eta * T)        # product of upstream walls arrives mixed into the stream
        q_init = nF * eta * Qr * T                                             # free product arrives with the stream
        q_vol = 0.0                                                            # no residence in the cell
        stopped = False
        # reference windows in a liquid other than the substrate buffer: the difference in background current
        # is part of what the pre-run has to carry over (second review, finding M1); 0 for matched buffers
        other_bg = rd.get("buffer_step_A", 0.0) * T
    elif mode == "accumulate_step":
        t_acc = rd["t_acc_s"]
        _tl, kr = thin_layer_kernels(a, h, R, ch["D_prod"], (("off", t_acc), ("on", T)), regions, rb, Lb)
        g = {k: _between(r, "cum", t_acc, t_acc + T) for k, r in kr.items()}
        col = dict(we=g["we"], floor=g["floor"], lid=g["lid"], ring=g.get("ring", 0.0), bore=g.get("bore", 0.0),
                   line=0.0)
        q_vol, q_init = nF * g["volume"], nF * g["initial"]
        other_bg = p("tr.detection.step_background_charge_density", "C/m^2") * A_we
    elif mode in ("cycling", "ida"):
        t1 = rd.get("t_wait_s", 0.0)
        _tl, kr = thin_layer_kernels(a, h, R, ch["D_prod"], (("off", t1 + T),), regions, rb, Lb)
        ci = {k: _between(r, "cint", t1, t1 + T) for k, r in kr.items()}      # integral of surface conc per unit source
        if mode == "cycling":
            k_reg = p("tr.detection.chemical_cycling_rate_constant", "1/s") if rd.get("k_reg") is None else rd["k_reg"]
            per_conc = nF * cycling_surface_velocity(ch["D_prod"], k_reg, h) * A_we        # A per (mol/m^3)
            other_bg = p("tr.detection.reductant_background_current_density", "A/m^2") * A_we * T
            noise_factor = p("tr.detection.cycling_noise_factor", "fold")
        else:
            ida = rd["ida"]
            eff = p("ma.detection.ida_stopped_efficiency", "fraction")
            if rd.get("two_electrode", False):
                eff = eff * p("tr.detection.ida_two_electrode_efficiency", "fraction")
            per_conc = tr.aoki_ida_current_per_conc(
                ch["n_e"], ch["D_prod"], ida["m"], ida["b"], ida["w"], ida["g"],
                p("ma.detection.aoki_c1", "dimensionless"), p("ma.detection.aoki_c2", "dimensionless"),
                p("ma.detection.aoki_c3", "dimensionless")) * eff
        col = {k: per_conc * ci[k] / nF for k in ("we", "floor", "lid")}       # "mol collected" equivalents
        col["ring"] = per_conc * ci.get("ring", 0.0) / nF
        col["bore"], col["line"] = per_conc * ci.get("bore", 0.0) / nF, 0.0
        q_vol, q_init = per_conc * ci["volume"], per_conc * ci["initial"]
    else:
        raise ValueError(mode)

    # coated electrode (review finding C2): fraction of the transport-limited current that the electrode still
    # delivers through the monolayer and the protein layer at the read potential.  A lumped factor on every
    # current through the electrode: signal, non-specific label, impurity and hydrolysis alike; 1 if not coated.
    f_el = p(el["collection_key"], "fraction") if el.get("collection_key") else 1.0
    col = {k: val * f_el for k, val in col.items()}
    q_vol, q_init = q_vol * f_el, q_init * f_el

    rate = v / NA                                                              # mol/s per enzyme
    Q_spec = nF * rate * (N_spec_we * col["we"] + N_spec_ring * col["ring"])
    Q_nsb = nF * rate * (N_nsb_we * col["we"] + N_nsb_floor * col["floor"] + N_nsb_lid * col["lid"]
                         + N_up_bore * col["bore"] + N_up_line * col["line"])
    Q_carry = nF * rate * N_carry * col["we"]
    eff_low = N_spec[..., 1:2] / np.maximum(d["N_vial"][..., 1:2], 1e-300)
    Q_cont = nF * rate * d["N_cont_vial"] * eff_low * share_we * col["we"]
    Q_hyd = hyd * q_vol + c_hyd_res * q_init
    Q_imp = c_imp * q_init
    N_blank_enz = (N_nsb_we + N_nsb_floor * col["floor"] / col["we"] + N_nsb_lid * col["lid"] / col["we"]
                   + N_up_bore * col["bore"] / col["we"] + N_up_line * col["line"] / col["we"] + N_carry)
    q_per_enzyme = nF * rate * col["we"]
    diag = dict(capture_fraction=_sq(f_patch * d["chain"]), k_m=_sq(k_m), k_r=_sq(k_r),
                N_captured_at_1pg=_interp_at(conc, N_cap + 0.0 * conc, 1.0),
                enzymes_on_we_at_1pg=_interp_at(conc, N_spec_we + 0.0 * conc, 1.0),
                N_nsb_we=_sq(N_nsb_we), N_nsb_floor=_sq(N_nsb_floor), N_nsb_lid=_sq(N_nsb_lid),
                collected_floor=col["floor"] / col["we"], collected_lid=col["lid"] / col["we"],
                N_up_bore=_sq(N_up_bore), N_up_line=_sq(N_up_line), collected_upstream=col["line"] / col["we"],
                collected_bore=col["bore"] / col["we"],
                f_label=_sq(lab["f_label"]), ret_label=_sq(lab["ret_label"]), ret_capture=_sq(lab["ret_capture"]),
                exposure_nM_min=_sq(lab["exposure"]) * 1e6 / 60.0, loop_transfer=_sq(d["f_transfer"]),
                n_flush=_sq(d["n_flush"]), current_per_enzyme_A=_sq(q_per_enzyme) / T,
                mean_current_at_1pg_A=_interp_at(conc, Q_spec + 0.0 * conc, 1.0) / T,
                mean_blank_current_A=_sq(Q_nsb + Q_imp + Q_hyd + other_bg) / T)
    Qs = dict(spec=Q_spec + 0.0 * conc, nsb=Q_nsb, carry=Q_carry, hyd=Q_hyd, imp=Q_imp, cont=Q_cont,
              other_bg=other_bg)
    return _finish(design, p, conc, Qs, q_per_enzyme, N_blank_enz, T, A_we, stopped,
                   p("tr.nsb.unit_to_unit_cv_planar", "fraction"), design.get("preread", False), diag, noise_factor)


# ----------------------------------------------------------------------------------------------------
# tier 2: capture on a flow-through bed upstream of the cell, product swept through or parked in the cell
# ----------------------------------------------------------------------------------------------------
def evaluate_bed(design: dict, ps: ParameterSet, conc_pgml=None) -> TierResult:
    """Flow-through capture bed directly upstream of the thin-layer cell (no valves).

    design keys:
      bed       : d_p, eps, V_bed, column_id (packed bed);  surface_factor_key;
                  extra_area (m^2 of retainer wetted by conjugate inside the accumulation volume) and
                  extra_factor_key;  bore_area and bore_factor_key (wall of the cell inlet bore);
                  V_dead (liquid volume between bed and electrode that moves with the plug)
      cell      : h, w_channel, R;  electrode: kind, area
      sample, conjugate, exposure_s, chemistry, steps as in evaluate_planar
      read      : mode ('swept' | 'parked' | 'continuous'), t_acc_s, Q_read_uL_min, t_read_s, sigma_uL (dispersion
                  between bed and electrode, standard deviation), n_tanks (bed)
      transfer  : optional dict(elution_key, nsb_factor_key, Q_push_uL_min) - immune-complex transfer to a second
                  bed (tier 3)
      bed also  : upstream_area, upstream_factor_key - conjugate-exposed walls upstream of the bed that stand in
                  substrate during the stop;  read also: baseline_step (cell stopped with the electrode on)
    """
    p = Ctx(ps)
    chem = CHEMISTRIES[design["chemistry"]]
    conc = _grid(p, conc_pgml)
    bed, cell, el, rd = design["bed"], design["cell"], design["electrode"], design["read"]
    A_we = el["area"]
    a = np.sqrt(A_we / np.pi)
    h, R = cell["h"], cell["R"]

    d = _delivery(design, p, conc)
    gamma = (p("chem.surfaces.igg_surface_density_monolayer", "molecules/m^2")
             * p("chem.surfaces.active_fraction_oriented", "fraction") / NA) \
        * p(design["capture"]["site_factor_key"], "fraction")
    k_r = p("chem.antibodies.kon_capture", "m^3/(mol*s)") * gamma
    A_bed = 6.0 * (1.0 - bed["eps"]) / bed["d_p"] * bed["V_bed"]
    nu = p("ma.fluid.viscosity", "Pa*s") / p("ma.fluid.density", "kg/m^3")
    A_col = np.pi * (0.5 * bed["column_id"]) ** 2
    u_s = d["Q"] / A_col
    k_m, _Re = tr.wilson_geankoplis_k(d["D_igg"], bed["d_p"], bed["eps"], u_s, nu,
                                      p("ma.correlations.wilson_geankoplis_coefficient", "dimensionless"))
    k_tot = 1.0 / (1.0 / k_m + 1.0 / k_r)
    f_bed = 1.0 - np.exp(-k_tot * A_bed / d["Q"])
    N_cap = f_bed * d["N_in"]
    dp_bed = kozeny_carman_dp(p("ma.fluid.viscosity", "Pa*s"), u_s, bed["d_p"], bed["eps"], bed["V_bed"] / A_col)

    lab = _labelling(design, p, chem)
    N_spec = N_cap * lab["ret_capture"] * lab["f_label"] * lab["ret_label"] * lab["enz"]

    k_nsb = p("chem.nsb.nsb_effective_rate_constant", "m/s") * p(chem["label_nsb_factor"], "fold") \
        * p("ma.labelling.detection_on_capture_residual_factor", "fold")
    per_area = k_nsb * lab["exposure"] * NA * lab["enz"]
    N_nsb_bed = per_area * p(bed["surface_factor_key"], "fold") * A_bed
    N_nsb_extra = per_area * p(bed["extra_factor_key"], "fold") * bed.get("extra_area", 0.0)
    if bed.get("bore_area", 0.0) > 0:                       # wall of the cell's inlet bore between bed and electrode
        N_nsb_extra = N_nsb_extra + per_area * p(bed["bore_factor_key"], "fold") * bed["bore_area"]
    if bed.get("upstream_area", 0.0) > 0:
        # walls upstream of the bed that saw conjugate and stand in substrate during the stop (capillary above
        # the bed, transfer line): their product follows the plug onto the electrode inside the read window
        N_nsb_extra = N_nsb_extra + per_area * p(bed["upstream_factor_key"], "fold") * bed["upstream_area"]
    transfer_eff = 1.0
    if design.get("transfer"):
        # immune-complex transfer to a second, clean bed that is the one read (tier 3).  Specific complexes:
        # released fraction (parameter, UNVERIFIED) x re-captured fraction on the second bed, the latter from the
        # same bed equation at the push flow with the diffusion coefficient of the conjugate.  Non-specific label
        # of the first bed that comes along: bounded lever of docs/05 (ma.design_levers, UNVERIFIED).
        t_ = design["transfer"]
        Qp = t_["Q_push_uL_min"] * ULMIN
        D_c = p("chem.antibodies.diffusion_coefficient_IgG_ALP_conjugate", "m^2/s")
        k_m2, _ = tr.wilson_geankoplis_k(D_c, bed["d_p"], bed["eps"], Qp / A_col, nu,
                                         p("ma.correlations.wilson_geankoplis_coefficient", "dimensionless"))
        release = p(t_["elution_key"], "fraction")
        A2 = A_bed * t_.get("bed2_factor", 1.0)                # read bed relative to the capture bed
        N_u = (1.0 / (1.0 / k_m2 + 1.0 / k_r)) * A2 / Qp       # number of transfer units of the read bed
        # Every capture antibody carries the tag, with or without analyte, so the read bed has to take all that
        # is released (second review, finding M3).  Fixed bed with site depletion (Bohart-Adams): fraction of a
        # finite feed that escapes = ln(exp(N (tau - 1)) + 1 - exp(-N)) / (N tau), tau = feed / sites.
        n_rel = release * p("chem.surfaces.igg_surface_density_monolayer", "molecules/m^2") / NA \
            * t_.get("coat", 1.0) * A_bed                      # mol of tagged capture antibody in the eluate
        tau = n_rel / (gamma * A2)
        recapture = 1.0 - np.log(np.exp(N_u * (tau - 1.0)) + 1.0 - np.exp(-N_u)) / (N_u * tau)
        transfer_eff = release * recapture
        N_spec = N_spec * transfer_eff
        f_nsb = p(t_["nsb_factor_key"], "fold")
        N_nsb_bed, N_nsb_extra = N_nsb_bed * f_nsb, N_nsb_extra * f_nsb
    N_nsb = N_nsb_bed + N_nsb_extra
    c_inj = p("hw.smfl.carryover_protein_conjugate", "fraction")
    uptake = 1.0 - np.exp(-k_nsb * (p(bed["surface_factor_key"], "fold") * A_bed) / d["Q"])
    N_carry = c_inj ** 2 * lab["N_conj_injected"] * uptake
    N_blank_enz = N_nsb + N_carry

    ch = _chem(p, chem)
    nF = ch["n_e"] * FARADAY
    read_bed = design["transfer"].get("bed2_factor", 1.0) if design.get("transfer") else 1.0
    V_acc = bed["eps"] * bed["V_bed"] * read_bed + bed.get("V_dead", 0.0)
    c_imp, c_hyd_res = _free_product(p, ch)                 # free product of the working substrate solution
    c_free = c_imp + c_hyd_res
    t_acc = rd["t_acc_s"]
    steps = int(p("ma.numerics.enzyme_ode_steps", "count"))

    def product(N_enz):
        E = N_enz / NA / V_acc
        Pe, Pb, _S = kin.enzyme_accumulation(E, ch["S0"], ch["kcat"], ch["Km"], t_acc, Ki=ch["Ki"],
                                             pi_per_product=ch["ppp"], k_hyd=ch["k_hyd"], k_decay=ch["k_dec"],
                                             P_bg0=0.0, steps=steps)
        return Pe * V_acc, Pb * V_acc

    eff_low = N_spec[..., 1:2] / np.maximum(d["N_vial"][..., 1:2], 1e-300)
    n_tot, _ = product(N_spec + N_blank_enz)
    n_blank, n_hyd = product(N_blank_enz)
    n_cont, _ = product(N_blank_enz + d["N_cont_vial"] * eff_low)
    n_cont = n_cont - n_blank
    T = rd["t_read_s"]
    sigma = rd.get("sigma_uL", 1.0) * UL
    n_eff = V_acc ** 2 / (V_acc ** 2 / rd.get("n_tanks", 3.0) + sigma ** 2)
    V_plug = np.sqrt(V_acc ** 2 + 12.0 * sigma ** 2)                           # width of the dispersed plug
    other_bg = 0.0
    if rd["mode"] == "swept":
        Qr = rd["Q_read_uL_min"] * ULMIN
        eta = cell_conversion(cell, ch["D_prod"], A_we, Qr)
        v_fresh = ch["kcat"] * ch["S0"] / (ch["Km"] + ch["S0"]) / NA           # mol/s per enzyme, fresh substrate
        if rd.get("V_transit_uL") is not None:
            # laminar transit from the bed to the electrode without radial mixing: of a thin slab the fraction
            # (V_t / 2V)^2 has not arrived after the volume V (second review, finding M5)
            V_t = rd["V_transit_uL"] * UL
            eluted = 1.0 - min(1.0, V_t / (2.0 * Qr * T)) ** 2
        else:
            V_t = 0.0
            eluted = tr.tanks_in_series_eluted(Qr * T / V_acc, n_eff)          # as the audited model (cross-check)
        if rd.get("count_sweep_production", False):
            # the enzymes keep working in fresh substrate while the plug is swept; what they make in the last
            # V_t / Q of the window does not arrive in it
            t_sw = max(T - V_t / Qr, 0.0)
            n_tot = n_tot + (N_spec + N_blank_enz) * v_fresh * t_sw
            n_blank = n_blank + N_blank_enz * v_fresh * t_sw
            n_cont = n_cont + d["N_cont_vial"] * eff_low * v_fresh * t_sw
        q_per_mol = nF * eta * eluted
        stopped = False
        Q_imp = nF * eta * Qr * c_free * T                                     # steady baseline, referenced
        referenced = True
        cell_blank = 0.0
        if rd.get("count_steady", False):
            # steady currents of conjugate that sits on the electrode (collected in full) and on walls that stay
            # in flowing substrate (collected at eta): removed by the baseline, their relative noise counts
            # like that of the free-product current (second review, findings M4, M7)
            steady = nF * v_fresh * per_area * (
                p(el["we_factor_key"], "fold") * A_we
                + eta * (p(cell["lid_factor_key"], "fold") * rd.get("steady_bore_area", 0.0)
                         + p("ma.nsb.surface_factor_tubing", "fold") * rd.get("steady_wall_area", 0.0)))
            other_bg = steady * T
    elif rd["mode"] == "parked":
        phases = (("on", T),)
        rb, Lb = cell.get("bore_radius", 0.0), cell.get("bore_length", 0.0)
        regions = (("we", "floor", 0.0, a), ("floor", "floor", a, R), ("lid", "ceiling", rb, R))
        _tl, kr = thin_layer_kernels(a, h, R, ch["D_prod"], phases, regions, rb, Lb)
        V_coll = kr["initial"]["cum"][-1]                                       # m^3 swept clean by the electrode in T
        V_layer = np.pi * R ** 2 * h
        frac = min(1.0, V_coll / max(V_plug, 1e-30)) if V_plug <= V_layer else min(1.0, V_coll / V_plug)
        eta, eluted = frac, 1.0
        q_per_mol = nF * frac
        stopped = True
        Q_imp = nF * c_free * V_coll                                            # free product in the parked plug
        referenced = design.get("preread", False)
        # non-specific enzyme left by the conjugate on the cell surfaces works during the parked read
        g = {k: r["cum"][-1] for k, r in kr.items()}
        sf_we, sf_floor, sf_lid = (p(el["we_factor_key"], "fold"), p(el["floor_factor_key"], "fold"),
                                   p(cell["lid_factor_key"], "fold"))
        v = ch["kcat"] * ch["S0"] / (ch["Km"] + ch["S0"]) / NA
        cell_blank = nF * v * per_area * (sf_we * A_we * T + sf_floor * (np.pi * R ** 2 - A_we) * g["floor"]
                                           + sf_lid * np.pi * R ** 2 * g["lid"])
    elif rd["mode"] == "continuous":
        # no stop: substrate flows through the bed and the cell; the steady current is the enzyme turnover
        Qr = rd["Q_read_uL_min"] * ULMIN
        eta = cell_conversion(cell, ch["D_prod"], A_we, Qr)
        v = ch["kcat"] * ch["S0"] / (ch["Km"] + ch["S0"]) / NA                # mol/s per enzyme (fresh substrate)
        eluted, stopped = 1.0, False
        q_enz = nF * eta * v * T                                              # C per upstream enzyme
        n_tot, n_blank = (N_spec + N_blank_enz) * q_enz / (nF * eta), N_blank_enz * q_enz / (nF * eta)
        n_cont = d["N_cont_vial"] * eff_low * q_enz / (nF * eta)
        n_hyd = Qr * T * c_hyd_res
        q_per_mol = nF * eta
        Q_imp = nF * eta * Qr * c_imp * T
        referenced = design.get("preread", False)
        rb = cell.get("bore_radius", 0.0)
        A_lid = np.pi * (R ** 2 - rb ** 2)
        # conjugate left on the electrode and on the lid above it works in the same stream
        cell_blank = nF * v * T * per_area * (p(el["we_factor_key"], "fold") * A_we
                                               + p(cell["lid_factor_key"], "fold") * 0.5 * eta
                                               * max(A_we - np.pi * rb ** 2, 0.0))
    else:
        raise ValueError(rd["mode"])
    Q_spec = q_per_mol * (n_tot - n_blank)
    Q_blank = q_per_mol * n_blank
    share_nsb = N_nsb / np.maximum(N_blank_enz, 1e-300)
    Q_nsb = Q_blank * share_nsb + cell_blank
    Q_carry = Q_blank * (1.0 - share_nsb)
    Q_hyd = q_per_mol * n_hyd
    Q_cont = q_per_mol * n_cont
    q_per_enzyme = Q_blank / np.maximum(N_blank_enz, 1e-300)
    diag = dict(capture_fraction=_sq(f_bed * d["chain"]), k_m=_sq(k_m), k_r=_sq(k_r), bed_area_m2=A_bed,
                bed_dp_Pa=_sq(dp_bed), N_captured_at_1pg=_interp_at(conc, N_cap + 0.0 * conc, 1.0),
                enzymes_at_1pg=_interp_at(conc, N_spec + 0.0 * conc, 1.0), N_nsb_bed=_sq(N_nsb_bed),
                N_nsb_extra=_sq(N_nsb_extra), f_label=_sq(lab["f_label"]), ret_label=_sq(lab["ret_label"]),
                exposure_nM_min=_sq(lab["exposure"]) * 1e6 / 60.0, loop_transfer=_sq(d["f_transfer"]),
                n_flush=_sq(d["n_flush"]), cell_conversion=_sq(eta), eluted=_sq(eluted),
                V_acc_uL=V_acc / UL, V_plug_uL=V_plug / UL, cell_blank_C=_sq(cell_blank),
                transfer_efficiency=_sq(transfer_eff), steady_current_A=_sq(other_bg) / T,
                free_product_M=_sq(c_free) * 1e-3,
                mean_current_at_1pg_A=_interp_at(conc, Q_spec + 0.0 * conc, 1.0) / T)
    Qs = dict(spec=Q_spec + 0.0 * conc, nsb=Q_nsb, carry=Q_carry, hyd=Q_hyd, imp=Q_imp, cont=Q_cont,
              other_bg=other_bg)
    return _finish(design, p, conc, Qs, q_per_enzyme, N_blank_enz, T, A_we, stopped,
                   p("tr.nsb.unit_to_unit_cv_bed", "fraction"), referenced, diag)


# ----------------------------------------------------------------------------------------------------
# I. Monte Carlo
# ----------------------------------------------------------------------------------------------------
def monte_carlo(evaluate, design, ps, n=None, seed=None, target=1.0):
    """Propagate parameter uncertainty (elisa_sim sampling rules: log-triangular for ranges >= 3x, else
    triangular; design variables and pinned values are not sampled).  Returns a summary dict."""
    cfg = ps.extra.get("monte_carlo", {})
    n = int(n or cfg.get("default_samples", 2000))
    seed = int(seed if seed is not None else cfg.get("seed", 0))
    probe = ps.copy()
    probe.accessed = set()
    nominal = evaluate(design, probe)
    keys = sorted(probe.accessed)
    sampled = ps.sample(n, np.random.default_rng(seed), keys)
    res = evaluate(design, sampled)
    lod = np.asarray(res.lod_pgml, float)
    q = lambda x, a: float(np.nanpercentile(np.where(np.isfinite(x), x, 1e30), a))
    lim = res.limiting_term
    names, counts = np.unique(lim, return_counts=True)
    tot = sum(np.asarray(v, float) for v in res.variance_terms.values())
    out = dict(name=design["name"], lod_nominal=float(nominal.lod_pgml), lod_median=q(lod, 50), lod_p05=q(lod, 5),
               lod_p95=q(lod, 95), p_lod_le_target=float(np.mean(lod <= target)),
               p_lod_le_3=float(np.mean(lod <= 3.0)), p_lod_le_10=float(np.mean(lod <= 10.0)),
               uloq_nominal=float(nominal.uloq_pgml),
               blank_equiv_nominal=float(nominal.diagnostics["blank_equivalent_pgml"]),
               time_to_result_min=nominal.time_to_result_min,
               limiting_term_nominal=str(nominal.limiting_term),
               limiting_term_mc_mode=str(names[np.argmax(counts)]),
               limiting_term_mc_share=float(np.max(counts) / len(lim)),
               n=n, seed=seed, n_sampled_keys=len(ps.sampleable(keys)))
    for k, v in res.variance_terms.items():
        out[f"varfrac_median_{k}"] = float(np.median(np.asarray(v, float) / tot))
    out["_nominal"], out["_mc"], out["_keys"] = nominal, res, ps.sampleable(keys)
    out["_samples"] = {k: np.asarray(sampled.values[k]) for k in ps.sampleable(keys)}
    return out


def one_at_a_time(evaluate, design, ps, keys=None):
    """LOD with each sampled parameter at its low and high bound (others nominal).  Returns list of
    (key, lod_low, lod_high) sorted by the size of the swing."""
    probe = ps.copy()
    probe.accessed = set()
    base = float(evaluate(design, probe).lod_pgml)
    keys = keys or ps.sampleable(sorted(probe.accessed))
    rows = []
    for k in keys:
        prm = ps.params[k]
        lo = float(evaluate(design, ps.with_values({k: prm.low})).lod_pgml)
        hi = float(evaluate(design, ps.with_values({k: prm.high})).lod_pgml)
        rows.append((k, lo, hi))
    rows.sort(key=lambda r: -abs(np.log(max(r[2], 1e-12) / max(r[1], 1e-12))))
    return base, rows
