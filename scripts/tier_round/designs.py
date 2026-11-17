"""Design dictionaries of the three tiers (docs/26, docs/30) for scripts/tier_round/tierkit.py.

Geometry from docs/28 (MicruX brochures; chamber height UNVERIFIED): both MicruX flow add-ons are wall-jet cells.
  SPE cell  (AIO-SPE + flow add-on): O-ring 8 mm I.D., inlet bore 0.8 mm, working electrode 3 mm; the vendor states
            < 5 uL (gap <= 0.1 mm); the user states 10 uL (gap 0.2 mm) -> 0.2 mm nominal, 0.1 and 0.5 mm as scenarios.
  TF cell   (AIO + flow add-on FC-2.0): O-ring 2.0 mm I.D., inlet bore 0.5 mm, working electrode 1 mm (SE1);
            the vendor states < 0.5 uL (gap <= 0.16 mm) -> 0.16 mm nominal, 0.1 and 0.3 mm as scenarios.
  Bore length 5 mm is assumed for both (not published).
Every time, flow, volume and concentration below is a design choice (not sampled in the Monte Carlo).

Revised after the review (docs/31): Loop Offline before every step to substrate and 215 uL of substrate for the
step (F1); conjugate passed for two loop volumes; the walls upstream of the electrode or bed that saw conjugate
are counted (N2, N3); tier 1 reads at a fast, constant flow between two buffer windows (N1, N2); tier 2 steps
down to 5 uL/min before the stop (F2) and counts the 1 mm of bore below the capillary tip (F8).
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
AU10 = dict(kind="printed", area=np.pi * (1.5e-3) ** 2, we_factor_key="tr.nsb.surface_factor_gold_oeg",
            floor_factor_key="tr.nsb.surface_factor_printed_electrode")
SE1_AU = dict(kind="thinfilm", area=np.pi * (0.5e-3) ** 2, we_factor_key="tr.nsb.surface_factor_gold_oeg",
              floor_factor_key="tr.nsb.surface_factor_glass_blocked")
ELECTRODES = {"C21": (SPE_CELL, C21), "AU10": (SPE_CELL, AU10), "SE1": (TF_CELL, SE1_AU)}

OVERHEAD = 1.0                               # min per SM-FL injection (docs/02 section 2.2: about 1 min, UNVERIFIED)
LINE_ID, LINE_LENGTH = 50e-6, 0.15           # transfer line injector -> cell: 50 um I.D. x 15 cm (design choice)
LINE_AREA = np.pi * LINE_ID * LINE_LENGTH    # 23.6 mm^2 of wall that sees conjugate and, later, substrate
V_STEP = 215.0                               # uL of new liquid for a 95 % composition step (docs/31 F1)


def tier1(electrode="AU10", h=None, Q_load=3.0, t_load=42.0, C_conj=10.0, V_conj=100.0, Q_conj=50.0, t_conj=4.0,
          t_wash1=1.5, t_wash2=2.0, read_mode="steady_flow", Q_read=150.0, t_read=120.0, t_ref=30.0,
          t_wait=30.0, preread=True, ring_width=0.0, site_key=None, line_area=LINE_AREA, name=None):
    """Tier 1: capture on the working electrode of the wall-jet cell, product read at the same electrode.

    read_mode 'steady_flow': substrate flows at Q_read; the read window is bracketed by two buffer windows at the
    same flow (A - B - A), and the same sequence on the fresh electrode before the sample gives the substrate
    background.  read_mode 'steady': the step to substrate is followed by a step-down and a stop (needs a
    zero-flow row); wait t_wait, read t_read; bracketed likewise by stopped buffer windows."""
    cell0, el0 = ELECTRODES[electrode]
    cell, el = copy.deepcopy(cell0), copy.deepcopy(el0)
    if h is not None:
        cell["h"] = h
    if read_mode == "steady_flow":
        t_front = V_STEP / Q_read                                   # min for each composition step at the read flow
        after = [("substrate front (BSM A1 -> B1 at the read flow)", t_front, True),
                 ("read window, substrate flowing", t_read / 60.0, True),
                 ("buffer front (B1 -> A1)", t_front, True),
                 ("second reference window, buffer flowing", t_ref / 60.0, True)]
        to_read_mid = t_front + 0.5 * t_read / 60.0
        t_span = t_read + 2.0 * (t_front * 60.0 + 0.5 * t_ref)
    else:
        t_fill = V_STEP / 80.0
        after = [("step to substrate at 80 uL/min", t_fill, True),
                 ("step down to 5 uL/min, then stop", 1.0, True),
                 ("stopped: wait", t_wait / 60.0, True),
                 ("stopped: read window", t_read / 60.0, True),
                 ("flush to buffer, step down, stop, second reference window", t_fill + 1.0 + t_ref / 60.0, True)]
        to_read_mid = t_fill + 1.0 + (t_wait + 0.5 * t_read) / 60.0
        t_span = t_read + 2.0 * ((t_fill + 1.0) * 60.0 + t_wait + 0.5 * t_ref)
    steps = []
    if preread:
        steps.append(("pre-run: cleaning injection, hydroquinone locator plug, the same read sequence on the fresh "
                      "electrode", 12.0, False))
    steps += [("sample injection (SM-FL aspirate and load)", OVERHEAD, True),
              ("sample pumped through the cell", t_load, True),
              ("wash 1 (Loop Offline at its start)", t_wash1, True),
              ("conjugate injection (SM-FL)", OVERHEAD, True),
              ("conjugate through the cell, two loop volumes, then Loop Offline", t_conj, True),
              ("wash 2 at the read flow; its last 30 s are the first reference window", t_wash2, True)] + after
    d = dict(
        name=name or f"T1 {electrode} {read_mode}", tier=1, chemistry="alp_hqdp", steps=steps, preread=preread,
        exposure_s=dict(capture_to_read=(0.5 * t_load + t_wash1 + OVERHEAD + t_conj + t_wash2 + to_read_mid) * 60.0,
                        label_to_read=(0.5 * t_conj + t_wash2 + to_read_mid) * 60.0),
        cell=cell, electrode=el,
        capture=dict(site_factor_key=site_key or "tr.capture.site_factor_streptavidin_biotin", ring_width=ring_width),
        sample=dict(Q_uL_min=Q_load, t_load_min=t_load, V_transit_uL=4.0, mode="flow"),
        conjugate=dict(C_nM=C_conj, V_uL=V_conj, Q_uL_min=Q_conj, t_stop_min=0.0),
        read=dict(mode=read_mode, t_wait_s=t_wait, t_read_s=t_read, t_acc_s=t_wait, Q_read_uL_min=Q_read,
                  t_span_s=t_span, reference_far=preread),
        upstream=dict(bore_factor_key="tr.nsb.surface_factor_lid", line_area=line_area,
                      line_factor_key="ma.nsb.surface_factor_tubing"),
    )
    return d


def tier2(d_p=2.8e-6, V_bed_uL=0.019, column_id=200e-6, Q_load=3.4, t_load=37.0, C_conj=10.0, V_conj=100.0,
          Q_conj=50.0, t_conj=4.0, t_wash1=1.5, t_wash2=2.0, t_fill=V_STEP / 80.0, t_down=1.0, t_acc=420.0,
          Q_read=5.0, t_read=90.0, read_mode="swept", electrode="C21", h=None,
          bed_factor_key="ma.nsb.surface_factor_packed_bed", retainer_area=5e-6, bore_below_tip_mm=1.0,
          capillary_above_bed_mm=20.0, line_area=LINE_AREA, V_dead_uL=0.1, t_extra=0.0, name=None, preread=True):
    """Tier 2: single-use bed packed against a frit in a capillary whose tip sits in the inlet bore of the cell.

    retainer_area         wetted area (m^2) of the frit or screen, at tr.nsb.surface_factor_frit.
    bore_below_tip_mm     length of inlet bore between the capillary tip and the chamber: its wall saw conjugate
                          and lies between bed and electrode.  5.0 = bed in a fitting on the port (whole bore).
    capillary_above_bed_mm, line_area   walls upstream of the bed that saw conjugate and stand in substrate during
                          the stop; their product follows the plug into the read window (docs/31 N3).
    t_down                minutes at the read flow before the stop, so that the pump pressure has relaxed (F2).
    t_extra               minutes of added steps between wash 2 and the substrate (tier 3)."""
    cell0, el0 = ELECTRODES[electrode]
    cell, el = copy.deepcopy(cell0), copy.deepcopy(el0)
    if h is not None:
        cell["h"] = h
    rb = cell["bore_radius"]
    continuous = read_mode == "continuous"
    steps = [("pre-run: cleaning injection; the same substrate step, stop and sweep on the fresh bed and strip",
              14.0, False),
             ("sample injection (SM-FL aspirate and load)", OVERHEAD, True),
             ("sample pumped through the bed", t_load, True),
             ("wash 1 (Loop Offline at its start)", t_wash1, True),
             ("conjugate injection (SM-FL)", OVERHEAD, True),
             ("conjugate through the bed, two loop volumes, then Loop Offline", t_conj, True),
             ("wash 2", t_wash2, True)]
    if t_extra > 0:
        steps.append(("eluent injection, hold on bed 1, push through bed 2, wash of bed 2 (tier 3)", t_extra, True))
    steps.append(("step to substrate, 215 uL at 80 uL/min", t_fill, True))
    if continuous:
        steps += [("step down to the read flow and settle", t_down, True),
                  ("read window, substrate flowing through bed and cell", t_read / 60.0, True)]
        to_seal = t_fill + t_down
    else:
        steps += [("step down to 5 uL/min so that the pump pressure relaxes", t_down, True),
                  ("accumulation: product collects in the bed", t_acc / 60.0, True),
                  ("sweep over the electrode and read", t_read / 60.0, True)]
        to_seal = t_fill + t_down
    after_conj = (t_wash2 + t_extra + to_seal) * 60.0
    after_load = (t_wash1 + OVERHEAD + t_conj) * 60.0 + after_conj
    d = dict(
        name=name or f"T2 bed {V_bed_uL} uL of {d_p * 1e6:.1f} um beads, {read_mode}", tier=2, chemistry="alp_hqdp",
        steps=steps, preread=preread,
        exposure_s=dict(capture_to_read=0.5 * t_load * 60.0 + after_load,
                        label_to_read=0.5 * t_conj * 60.0 + after_conj),
        bed=dict(d_p=d_p, eps=0.4, V_bed=V_bed_uL * 1e-9, column_id=column_id, surface_factor_key=bed_factor_key,
                 extra_area=retainer_area, extra_factor_key="tr.nsb.surface_factor_frit", V_dead=V_dead_uL * 1e-9,
                 bore_area=2.0 * np.pi * rb * bore_below_tip_mm * 1e-3, bore_factor_key="tr.nsb.surface_factor_lid",
                 upstream_area=np.pi * column_id * capillary_above_bed_mm * 1e-3 + line_area,
                 upstream_factor_key="ma.nsb.surface_factor_tubing"),
        cell=cell, electrode=el,
        capture=dict(site_factor_key="tr.capture.site_factor_streptavidin_biotin"),
        sample=dict(Q_uL_min=Q_load, t_load_min=t_load, V_transit_uL=2.0),
        conjugate=dict(C_nM=C_conj, V_uL=V_conj, Q_uL_min=Q_conj, t_stop_min=0.0),
        read=dict(mode=read_mode, t_acc_s=t_acc, Q_read_uL_min=Q_read, t_read_s=t_read, sigma_uL=1.0, n_tanks=3.0,
                  baseline_step=(read_mode == "swept")),
    )
    return d


def tier3(Q_load=5.0, t_load=25.0, t_acc=420.0, t_hold=5.0, Q_push=2.0, V_push_uL=8.0, elution_key=None,
          transfer=True, **kw):
    """Tier 3: two beds in the loops of two 6-port valves; the complex is released from bed 1, re-captured on
    bed 2, and bed 2 is the bed that is read.  The cell stays in the flow all the time, so the read has a steady
    baseline (no step), and the walls upstream of bed 2 give a steady current, not a plug.  Bed 2, its retainer
    and 10 mm^2 of valve passages and loop tubing see only the eluate."""
    t_extra = (OVERHEAD + 0.5 + t_hold + V_push_uL / Q_push + 2.0) if transfer else 0.0
    base = dict(Q_load=Q_load, t_load=t_load, t_acc=t_acc, t_extra=t_extra, t_down=0.0, bore_below_tip_mm=0.0,
                capillary_above_bed_mm=0.0, line_area=10e-6)
    base.update(kw)
    d = tier2(**base)
    d["tier"] = 3
    d["read"]["baseline_step"] = False
    d["read"]["sigma_uL"] = 1.5                       # valve passage and line between bed 2 and the electrode
    if transfer:
        d["transfer"] = dict(elution_key=elution_key or "tr.transfer.elution_efficiency",
                             nsb_factor_key="ma.design_levers.immune_complex_transfer_nsb_factor",
                             Q_push_uL_min=Q_push)
    else:
        # valves only: the capture bed is the read bed; the upstream walls give a steady baseline, the walls of
        # the loop (valve passages, tubing) saw conjugate and count in full
        pass
    return d
