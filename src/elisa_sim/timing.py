"""Assay-cycle timeline per architecture (docs/02 section 7.4 extended to every scheme).

Durations come from hw.timing.*, hw.smfl.* and ma.timing.*; the sample-load time is computed as
n_flush x V_loop / Q_load instead of using the pre-computed hw.timing.sample_load_time.
Also returns the exposure windows used by the dissociation (retention) terms:

* capture_exposure_s: from the middle of sample capture until the reactor is sealed with substrate
  (stopped schemes) or until the middle of the read window (Scheme A, dissociated label is washed away);
* label_exposure_s: from the middle of the (last) labelling incubation to the same end point.
"""
from __future__ import annotations

import numpy as np


def _scalar(x):
    a = np.asarray(x, dtype=float)
    return float(a.reshape(-1)[0]) if a.size else float(a)


def cycle_timeline(arch, p) -> dict:
    t_inj = _scalar(p("hw.smfl.injection_overhead_time", "min"))
    V_loop = _scalar(p("hw.smfl.loop_volume_recommended", "uL"))
    n_flush = _scalar(p("hw.smfl.loop_flush_volumes_for_transfer", "loop volumes"))
    Q_load = _scalar(p("hw.timing.sample_load_flow", "uL/min"))
    t_load = n_flush * V_loop / Q_load
    t_wash_s = _scalar(p("ma.timing.post_sample_wash", "min"))
    t_fill = _scalar(p("ma.timing.conjugate_fill", "min"))
    t_conj = _scalar(p("hw.timing.conjugate_stopped_flow_incubation", "min"))
    t_wash_c = _scalar(p("hw.timing.wash_after_conjugate", "min"))
    t_sub_fill = _scalar(p("hw.timing.substrate_fill", "min"))
    t_acc = _scalar(p("hw.timing.accumulation_time", "min"))
    t_read = _scalar(p("hw.timing.readout_time", "min"))
    t_regen = _scalar(p("hw.timing.regeneration_and_reequilibration", "min"))
    t_second = _scalar(p("ma.timing.second_label_incubation", "min"))
    t_inj_sub = _scalar(p("ma.timing.injected_substrate_extra", "min"))
    t_bead = _scalar(p("ma.timing.bead_flush_and_clean", "min"))
    t_stab = _scalar(p("ma.timing.continuous_stabilisation", "min"))
    t_vial = _scalar(p("ma.timing.in_vial_incubation", "min")) if arch.capture == "magnetic_beads" else 0.0
    t_age = _scalar(p("ma.timing.substrate_reservoir_age", "min"))
    from .architectures import CHEMISTRIES
    two_step = CHEMISTRIES[arch.chemistry]["labelling"] == "two_step"

    steps = {}
    steps["sample_injection_overhead"] = t_inj
    steps["sample_load"] = t_load
    steps["post_sample_wash"] = t_wash_s
    if arch.labelling_format == "one_step_in_vial":
        lab_steps = []          # conjugate already in the vial
    elif arch.scheme == "A":
        # no isolation: conjugate plug pushed through the loop and the bed at the loading flow
        lab_steps = [("conjugate", t_inj + t_load, 0.0)]
        if two_step:
            lab_steps.append(("second_label", t_inj + t_load, 0.0))
    else:
        lab_steps = [("conjugate", t_inj + t_fill + t_conj + t_wash_c, t_conj)]
        if two_step:
            lab_steps.append(("second_label", t_inj + t_fill + t_second + t_wash_c, t_second))
    for name, dur, _inc in lab_steps:
        steps[name] = dur
    if arch.scheme == "A":
        steps["substrate_fill"] = t_sub_fill
        steps["stabilisation"] = t_stab
        steps["readout"] = t_read
    else:
        if arch.substrate_delivery == "injected":
            steps["substrate_injection_extra"] = t_inj_sub
        steps["substrate_fill"] = t_sub_fill
        steps["accumulation"] = t_acc
        steps["readout"] = t_read
    steps["regeneration" if arch.regenerated else "bead_release_and_cleaning"] = t_regen if arch.regenerated else t_bead
    cycle = sum(steps.values())

    # exposure windows: event times (min) measured from the start of sample loading
    t = t_load + t_wash_s
    first_label_end = None                 # end of first labelling incubation (dissociation starts)
    for i, (name, dur, inc) in enumerate(lab_steps):
        if arch.scheme == "A":
            mid = t + t_inj + 0.5 * t_load     # conjugate passes the bed in flow (no koff in the exposure)
            if i == 0:
                first_label_end = mid
        else:
            if i == 0:
                first_label_end = t + t_inj + t_fill + inc
        t += dur
    if arch.substrate_delivery == "injected" and arch.scheme != "A":
        t += t_inj_sub
    t += t_sub_fill
    t_seal = t + (t_stab + 0.5 * t_read if arch.scheme == "A" else 0.0)
    if arch.capture == "magnetic_beads":
        capture_ref = -t_inj               # vial incubation (with koff) ends before the injection
    else:
        capture_ref = 0.5 * t_load         # flow-through capture formula has no koff: mid-load
    if first_label_end is None:            # one-step in vial: labelling ended with the vial incubation
        first_label_end = -t_inj
    capture_to_seal = t_seal - capture_ref
    label_exposure = t_seal - first_label_end

    return dict(
        steps_min=steps,
        cycle_min=cycle,
        time_to_result_min=cycle + t_vial,
        in_vial_s=t_vial * 60.0,
        capture_exposure_s=capture_to_seal * 60.0,
        label_exposure_s=label_exposure * 60.0,
        conj_incubation_s=t_conj * 60.0,
        second_incubation_s=t_second * 60.0,
        accumulation_s=t_acc * 60.0,
        readout_s=t_read * 60.0,
        reservoir_age_s=t_age * 60.0,
    )
