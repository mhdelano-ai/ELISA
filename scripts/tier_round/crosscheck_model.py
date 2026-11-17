"""Cross-check of tierkit.evaluate_bed against the audited model (elisa_sim) on the format both cover:
a 10 uL packed bed whose product is swept through a thin-layer cell (registry architecture B-bed-TL/alp_hqdp).

The kit's bed format has no isolation valve, a fresh bed per determination and unit-to-unit terms; for the
comparison those differences are switched off (see ``NEUTRAL``) and the kit is given the model's geometry, flows
and times.  Used by check_tierkit.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tierkit as tk  # noqa: E402
from elisa_sim.architectures import get  # noqa: E402
from elisa_sim.model import Ctx, evaluate  # noqa: E402
from elisa_sim.timing import cycle_timeline  # noqa: E402


def bed_against_model():
    ps = tk.load_params()
    neutral = {
        "tr.nsb.unit_to_unit_cv_bed": 0.0,                      # the model has no unit-to-unit NSB term
        "tr.noise.drift_area_exponent": 0.0,                    # the model does not scale drift with area
        "tr.noise.thinfilm_sensor_to_sensor_cv": ps.params["ma.noise.electrode_sensitivity_cv_nonfouling"].value,
        "chem.regeneration.residual_label_carryover_fraction": 0.0,   # fresh bed: nothing survives regeneration
    }
    ps = ps.with_values(neutral)
    arch = get("B-bed-TL/alp_hqdp")
    ref = evaluate(arch, ps)
    p = Ctx(ps)
    tl = cycle_timeline(arch, p)
    g = lambda k, u: float(np.asarray(p(k, u)).reshape(-1)[0])
    Q_load = g("hw.timing.sample_load_flow", "uL/min")
    V_loop = g("hw.smfl.loop_volume_recommended", "uL")
    n_flush = g("hw.smfl.loop_flush_volumes_for_transfer", "loop volumes")
    tube_d = g("hw.tubing.id_standard", "m")
    conn_L = g("ma.geometry.reactor_connection_length", "m")
    design = dict(
        name="cross-check B-bed-TL/alp_hqdp", chemistry="alp_hqdp",
        steps=[("all", float(ref.time_to_result_min), True)],
        exposure_s=dict(capture_to_read=tl["capture_exposure_s"], label_to_read=tl["label_exposure_s"]),
        bed=dict(d_p=g("hw.reactors.packed_microbed_10uL.bead_diameter", "m"),
                 eps=g("hw.reactors.packed_microbed_10uL.void_fraction", "fraction"),
                 V_bed=g("hw.reactors.packed_microbed_10uL.bed_volume", "m^3"),
                 column_id=g("ma.geometry.packed_bed_column_inner_diameter", "m"),
                 surface_factor_key="ma.nsb.surface_factor_packed_bed",
                 extra_area=np.pi * tube_d * conn_L, extra_factor_key="ma.nsb.surface_factor_tubing", V_dead=0.0),
        cell=dict(h=g("hw.flow_cells.thin_layer_basi.channel_height", "m"),
                  w_channel=g("ma.geometry.thin_layer_channel_width", "m"), R=3e-3,
                  lid_factor_key="tr.nsb.surface_factor_lid"),
        electrode=dict(kind="thinfilm", area=g("hw.flow_cells.thin_layer_basi.we_area", "m^2"),
                       we_factor_key="tr.nsb.surface_factor_printed_electrode",
                       floor_factor_key="tr.nsb.surface_factor_printed_electrode"),
        capture=dict(site_factor_key="tr.capture.site_factor_streptavidin_biotin"),
        sample=dict(Q_uL_min=Q_load, t_load_min=n_flush * V_loop / Q_load, V_transit_uL=0.0),
        conjugate=dict(C_nM=g("chem.antibodies.conc_detection_antibody_typical", "nM"),
                       V_uL=g("ma.delivery.conjugate_injection_volume", "uL"), Q_uL_min=Q_load,
                       t_stop_min=tl["conj_incubation_s"] / 60.0, count_flow_exposure=False),
        read=dict(mode="swept", t_acc_s=tl["accumulation_s"], Q_read_uL_min=g("ma.readout.sweep_flow", "uL/min"),
                  t_read_s=tl["readout_s"], sigma_uL=g("hw.tubing.product_plug_sigma_reactor_to_cell", "uL"),
                  n_tanks=g("ma.readout.tanks_packed_bed", "tanks")),
    )
    res = tk.evaluate_bed(design, ps)
    return ref, res


if __name__ == "__main__":
    ref, res = bed_against_model()
    for k in ("capture_fraction_low", "enzymes_at_1pg", "signal_at_1pg_C", "blank_equivalent_pgml", "N_nsb"):
        print("model", k, ref.diagnostics[k])
    print("model LOD", ref.lod_pgml, "limiting", ref.limiting_term)
    for k in ("capture_fraction", "enzymes_at_1pg", "signal_at_1pg_C", "blank_equivalent_pgml", "N_nsb_bed",
              "N_nsb_extra"):
        print("kit  ", k, res.diagnostics[k])
    print("kit   LOD", res.lod_pgml, "limiting", res.limiting_term)
