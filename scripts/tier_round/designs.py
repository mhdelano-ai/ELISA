"""Design dictionaries of the three tiers (docs/26, docs/30) for scripts/tier_round/tierkit.py.

Geometry from docs/28 (MicruX brochures; chamber height UNVERIFIED): both MicruX flow add-ons are wall-jet cells.
  SPE cell  (AIO-SPE + flow add-on): O-ring 8 mm I.D., inlet bore 0.8 mm, working electrode 3 mm; the vendor states
            < 5 uL (gap <= 0.1 mm); the user states 10 uL (gap 0.2 mm) -> 0.2 mm nominal, 0.1 and 0.5 mm as scenarios.
  TF cell   (AIO + flow add-on FC-2.0): O-ring 2.0 mm I.D., inlet bore 0.5 mm, working electrode 1 mm (SE1);
            the vendor states < 0.5 uL (gap <= 0.16 mm) -> 0.16 mm nominal, 0.1 and 0.3 mm as scenarios.
Every time, flow, volume and concentration below is a design choice (not sampled in the Monte Carlo).
"""
from __future__ import annotations

import copy

import numpy as np

SPE_CELL = dict(flow_geometry="radial", h=0.2e-3, R=4.0e-3, bore_radius=0.4e-3, bore_length=5.0e-3,
                lid_factor_key="tr.nsb.surface_factor_lid")
TF_CELL = dict(flow_geometry="radial", h=0.16e-3, R=1.0e-3, bore_radius=0.25e-3, bore_length=5.0e-3,
               lid_factor_key="tr.nsb.surface_factor_lid")
C21 = dict(kind="printed", area=np.pi * (1.5e-3) ** 2, we_factor_key="tr.nsb.surface_factor_printed_electrode",
           floor_factor_key="tr.nsb.surface_factor_printed_electrode")
SE1_AU = dict(kind="thinfilm", area=np.pi * (0.5e-3) ** 2, we_factor_key="tr.nsb.surface_factor_gold_oeg",
              floor_factor_key="tr.nsb.surface_factor_glass_blocked")

OVERHEAD = 1.0          # min per SM-FL injection (docs/02 section 2.2: about 1 min, UNVERIFIED)


def _steps_tier1(t_load, t_wash1, t_conj_flow, t_conj_stop, t_wash2, t_fill, t_wait, t_read, preread=True):
    s = []
    if preread:
        s += [("pre-run: buffer flush, substrate fill, background read on the fresh electrode, buffer flush", 8.0,
               False)]
    s += [("sample injection (SM-FL aspirate and load)", OVERHEAD, True),
          ("sample pumped through the cell", t_load, True),
          ("wash 1", t_wash1, True),
          ("conjugate injection (SM-FL)", OVERHEAD, True),
          ("conjugate pumped into the cell", t_conj_flow, True),
          ("conjugate stopped in the cell", t_conj_stop, True),
          ("wash 2", t_wash2, True),
          ("substrate fill (BSM A1 -> B1)", t_fill, True),
          ("flow stopped, electrode settles, impurity electrolysed", t_wait / 60.0, True),
          ("read window", t_read / 60.0, True)]
    return s


def tier1(electrode="C21", h=None, Q_load=5.0, t_load=27.0, C_conj=3.0, V_conj=100.0, Q_conj=20.0, t_conj_stop=3.0,
          t_wash1=1.5, t_wash2=3.0, t_fill=2.0, t_wait=90.0, t_read=300.0, read_mode="steady", preread=True,
          ring_width=0.0, site_key=None, Q_read=1.0, name=None):
    """Tier 1: capture on the working electrode of the wall-jet cell, product read at the same electrode."""
    cell = copy.deepcopy(SPE_CELL if electrode == "C21" else TF_CELL)
    if h is not None:
        cell["h"] = h
    el = copy.deepcopy(C21 if electrode == "C21" else SE1_AU)
    t_conj_flow = V_conj / Q_conj
    steps = _steps_tier1(t_load, t_wash1, t_conj_flow, t_conj_stop, t_wash2, t_fill, t_wait, t_read, preread)
    # dissociation clocks (s): from the middle of the step to the middle of the read window
    after_conj = (t_wash2 + t_fill) * 60.0 + t_wait + 0.5 * t_read
    after_load = (t_wash1 + OVERHEAD + t_conj_flow + t_conj_stop) * 60.0 + after_conj
    d = dict(
        name=name or f"T1 {electrode} {read_mode}", tier=1, chemistry="alp_hqdp", steps=steps, preread=preread,
        exposure_s=dict(capture_to_read=0.5 * t_load * 60.0 + after_load,
                        label_to_read=0.5 * (t_conj_flow + t_conj_stop) * 60.0 + after_conj),
        cell=cell, electrode=el,
        capture=dict(site_factor_key=site_key or "tr.capture.site_factor_streptavidin_biotin", ring_width=ring_width),
        sample=dict(Q_uL_min=Q_load, t_load_min=t_load, V_transit_uL=8.0, mode="flow"),
        conjugate=dict(C_nM=C_conj, V_uL=V_conj, Q_uL_min=Q_conj, t_stop_min=t_conj_stop),
        read=dict(mode=read_mode, t_wait_s=t_wait, t_read_s=t_read, t_acc_s=t_wait, Q_read_uL_min=Q_read),
    )
    return d


def tier2(d_p=20e-6, V_bed_uL=0.15, column_id=0.5e-3, Q_load=5.0, t_load=27.0, C_conj=3.0, V_conj=100.0,
          Q_conj=20.0, t_conj_stop=0.0, t_wash1=1.5, t_wash2=3.0, t_fill=2.0, t_acc=600.0, Q_read=5.0, t_read=90.0,
          read_mode="swept", electrode="C21", h=None, bed_factor_key="ma.nsb.surface_factor_packed_bed",
          retainer_area=5e-6, bore_wall=True, V_dead_uL=None, t_extra=0.0, name=None, preread=True):
    """Tier 2: single-use flow-through micro-bed screwed into the inlet port of the wall-jet cell.

    retainer_area: wetted area (m^2) of the bed retainer (screen or frit) at surface factor tr.nsb.surface_factor_frit.
    bore_wall: True  - the bed sits in a fitting on the inlet port; the wall of the cell's inlet bore (between bed
                       and electrode) is conjugate-exposed area whose product travels with the plug (volume V_dead);
               False - the bed is packed in a capillary that passes through the port and ends just above the
                       electrode, so the bore is not in the path (V_dead_uL = capillary volume below the bed).
    t_extra: minutes of added steps between wash 2 and the substrate fill (tier 3: elution and re-capture)."""
    cell = copy.deepcopy(SPE_CELL if electrode == "C21" else TF_CELL)
    if h is not None:
        cell["h"] = h
    el = copy.deepcopy(C21 if electrode == "C21" else SE1_AU)
    rb, Lb = cell["bore_radius"], cell["bore_length"]
    V_dead = np.pi * rb ** 2 * Lb if V_dead_uL is None else V_dead_uL * 1e-9
    t_conj_flow = V_conj / Q_conj
    steps = [("pre-run: buffer flush, substrate background peak on the fresh electrode, buffer flush", 8.0, False),
             ("sample injection (SM-FL aspirate and load)", OVERHEAD, True),
             ("sample pumped through the bed", t_load, True),
             ("wash 1", t_wash1, True),
             ("conjugate injection (SM-FL)", OVERHEAD, True),
             ("conjugate pumped through the bed", t_conj_flow, True),
             ("conjugate stopped in the bed", t_conj_stop, True),
             ("wash 2", t_wash2, True)]
    if t_extra > 0:
        steps += [("elution from the capture bed, re-capture on the read bed, wash (tier 3)", t_extra, True)]
    steps += [("substrate fill (BSM A1 -> B1)", t_fill, True),
             ("flow stopped: product accumulates in the bed", t_acc / 60.0, True),
             ("sweep through the cell and read", t_read / 60.0, True)]
    after_conj = (t_wash2 + t_extra + t_fill) * 60.0
    after_load = (t_wash1 + OVERHEAD + t_conj_flow + t_conj_stop) * 60.0 + after_conj
    d = dict(
        name=name or f"T2 bed {V_bed_uL} uL of {d_p * 1e6:.0f} um beads, {read_mode}", tier=2, chemistry="alp_hqdp",
        steps=steps, preread=preread,
        exposure_s=dict(capture_to_read=0.5 * t_load * 60.0 + after_load,
                        label_to_read=0.5 * (t_conj_flow + t_conj_stop) * 60.0 + after_conj),
        bed=dict(d_p=d_p, eps=0.4, V_bed=V_bed_uL * 1e-9, column_id=column_id, surface_factor_key=bed_factor_key,
                 extra_area=retainer_area, extra_factor_key="tr.nsb.surface_factor_frit", V_dead=V_dead,
                 bore_area=(2.0 * np.pi * rb * Lb if bore_wall else 0.0),
                 bore_factor_key="tr.nsb.surface_factor_lid"),
        cell=cell, electrode=el,
        capture=dict(site_factor_key="tr.capture.site_factor_streptavidin_biotin"),
        sample=dict(Q_uL_min=Q_load, t_load_min=t_load, V_transit_uL=4.0),
        conjugate=dict(C_nM=C_conj, V_uL=V_conj, Q_uL_min=Q_conj, t_stop_min=t_conj_stop),
        read=dict(mode=read_mode, t_acc_s=t_acc, Q_read_uL_min=Q_read, t_read_s=t_read, sigma_uL=1.0, n_tanks=3.0),
    )
    return d
