#!/usr/bin/env python3
"""Re-check every optimum that sits on the edge of its design grid or on a constraint (docs/05 s.1.4).

For each optimised design (results/design/optimum_<FMT>__baseline.json) and each listed probe, the design
variable is moved one step beyond the edge and re-evaluated (n = 1000).  The table says whether the probe is
blocked by a hard constraint (and which), and what the model would credit if the constraint were lifted, so
that the reader can see which "gains" are model artefacts.  Also evaluates packed-bed variants that respect
the column/particle diameter ratio >= 10 (wall-effect rule of thumb, not a model constraint).

Usage: python scripts/edge_checks.py   -> results/design/edge_checks.md
"""
from __future__ import annotations

import json

import design_lib as L
from design_lib import fmt

PROBES = {
    "OS": [("ma.geometry.reactor_connection_length", 0.0, "isolated tubing removed completely"),
           ("ma.geometry.reactor_connection_length", 0.005, "isolated tubing 5 mm"),
           ("hw.timing.sample_load_flow", 150, "bead loading 150 uL/min (trap efficiency held constant!)"),
           ("hw.timing.sample_load_flow", 200, "bead loading 200 uL/min (trap efficiency held constant!)"),
           ("hw.smfl.loop_flush_volumes_for_transfer", 1.5, "1.5 loop volumes"),
           ("ma.timing.post_sample_wash", 0.5, "0.5 min wash (wash efficiency not modelled)"),
           ("hw.timing.accumulation_time", 20, "20 min accumulation"),
           ("ma.geometry.magnetic_trap_tube_inner_diameter", 2.0, "trap ID 2 mm"),
           ("ma.readout.sweep_flow", 5, "sweep 5 uL/min"),
           ("hw.timing.readout_time", 0.5, "readout 0.5 min"),
           ("chem.antibodies.conc_detection_antibody_typical", 2e-10, "conjugate 0.2 nM"),
           ("chem.antibodies.conc_detection_antibody_typical", 1e-9, "conjugate 1 nM (baseline)")],
    "SQ": [("ma.geometry.reactor_connection_length", 0.0, "isolated tubing removed completely"),
           ("hw.timing.sample_load_flow", 150, "bead loading 150 uL/min (trap efficiency held constant!)"),
           ("hw.timing.wash_after_conjugate", 1, "1 min wash after conjugate (wash efficiency not modelled)"),
           ("ma.geometry.magnetic_trap_volume", 0.25, "trap 0.25 uL"),
           ("hw.smfl.loop_flush_volumes_for_transfer", 5, "5 loop volumes"),
           ("ma.timing.in_vial_incubation", 40, "40 min in vial"),
           ("chem.antibodies.conc_detection_antibody_typical", 1e-8, "conjugate 10 nM")],
    "FRB": [("hw.reactors.packed_microbed_10uL.bead_diameter", 75, "75 um beads"),
            ("ma.geometry.packed_bed_column_inner_diameter", 0.15, "0.15 mm column"),
            ("ma.geometry.reactor_connection_length", 0.0, "isolated tubing removed completely"),
            ("hw.timing.sample_load_flow", 10, "load 10 uL/min"),
            ("hw.timing.sample_load_flow", 5, "load 5 uL/min"),
            ("hw.timing.accumulation_time", 20, "20 min accumulation"),
            ("hw.timing.conjugate_stopped_flow_incubation", 1, "1 min conjugate incubation")],
    "FRC": [("ma.geometry.chip_channel_length", 2, "chip channel 2 mm"),
            ("hw.timing.sample_load_flow", 10, "load 10 uL/min"),
            ("hw.timing.conjugate_stopped_flow_incubation", 1, "1 min conjugate incubation")],
}

# packed beds that respect column ID >= 10 x particle diameter (wall effect)
FRB_PACKING_VARIANTS = [
    {"hw.reactors.packed_microbed_10uL.bead_diameter": 20, "ma.geometry.packed_bed_column_inner_diameter": 0.25},
    {"hw.reactors.packed_microbed_10uL.bead_diameter": 50, "ma.geometry.packed_bed_column_inner_diameter": 0.5},
    {"hw.reactors.packed_microbed_10uL.bead_diameter": 35, "ma.geometry.packed_bed_column_inner_diameter": 0.5},
]


def main():
    ps = L.load_ps()
    out = ["# Edge and constraint re-checks of the optimised designs\n",
           "n = 1000 Monte Carlo draws per row. 'Blocked by' lists the hard constraint the probe violates; the LOD "
           "columns show what the model would credit if it were allowed.\n",
           "| Format | Probe | Blocked by | LOD nominal | LOD median | P(LOD<=1) | P(success) | time (min) |",
           "|---|---|---|---|---|---|---|---|"]
    for key, probes in PROBES.items():
        try:
            rec = json.load(open(L.OUT / f"optimum_{key}__baseline.json"))
        except FileNotFoundError:
            continue
        opt = L.base_arch(key).with_design(**rec["design"])
        s = L.mc(opt, ps, n=1000)
        out.append(f"| {key} | optimum as found | - | {fmt(s['lod_nominal'])} | {fmt(s['lod_median'])} | "
                   f"{s['p_lod_only']:.2f} | {s['p_success']:.2f} | {s['time_to_result_min']:.1f} |")
        for var, val, label in probes:
            a = opt.with_design(**{var: val})
            why = L.constraint_violations(a, ps)
            try:
                s = L.mc(a, ps, n=1000)
            except ValueError as e:
                out.append(f"| {key} | {label} | model refuses: {e} | | | | | |")
                continue
            out.append(f"| {key} | {label} | {'; '.join(why) or 'none'} | {fmt(s['lod_nominal'])} | "
                       f"{fmt(s['lod_median'])} | {s['p_lod_only']:.2f} | {s['p_success']:.2f} | "
                       f"{s['time_to_result_min']:.1f} |")
            print(out[-1], flush=True)
        if key == "FRB":
            for v in FRB_PACKING_VARIANTS:
                a = opt.with_design(**v)
                why = L.constraint_violations(a, ps)
                s = L.mc(a, ps, n=1000)
                lab = f"packing-ratio-compliant: d_p {v['hw.reactors.packed_microbed_10uL.bead_diameter']} um, " \
                      f"ID {v['ma.geometry.packed_bed_column_inner_diameter']} mm"
                out.append(f"| FRB | {lab} | {'; '.join(why) or 'none'} | {fmt(s['lod_nominal'])} | "
                           f"{fmt(s['lod_median'])} | {s['p_lod_only']:.2f} | {s['p_success']:.2f} | "
                           f"{s['time_to_result_min']:.1f} |")
                print(out[-1], flush=True)
    (L.OUT / "edge_checks.md").write_text("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
