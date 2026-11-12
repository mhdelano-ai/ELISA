import sys, json
COPY = "/tmp/claude-0/-home-user-ELISA/04a7436b-08e5-5186-a749-bb6e7aad5fa5/scratchpad/copy"
sys.path[:0] = [COPY + "/scripts", COPY + "/src"]
from dataclasses import replace
import design_lib as L, final_designs as F
ps0 = L.load_ps()
IMP = "ma.chemistries.alp_hqdp.free_product_impurity"
def pre_el(p):
    if IMP in p.pinned: return p.with_values({IMP: float(p.values[IMP]) * 0.01})
    return L.with_bounds(p, IMP, value=1e-7, low=1e-9, high=1e-5)
fr = json.load(open(L.OUT / "optimum_FRB__baseline.json"))["design"]
B = replace(L.base_arch("FRB").with_design(**fr).with_design(**{
    "hw.reactors.packed_microbed_10uL.bed_volume": 0.5, "hw.reactors.packed_microbed_10uL.bead_diameter": 50,
    "ma.geometry.packed_bed_column_inner_diameter": 0.5, "hw.timing.sample_load_flow": 6,
    "hw.smfl.loop_flush_volumes_for_transfer": 1.5, "ma.geometry.reactor_connection_length": 0.002,
    "chem.antibodies.conc_detection_antibody_typical": 1e-9, "ma.delivery.conjugate_injection_volume": 20,
    "hw.timing.conjugate_stopped_flow_incubation": 3, "hw.timing.accumulation_time": 15,
    "hw.timing.readout_time": 1, "ma.readout.sweep_flow": 10,
    "hw.timing.regeneration_and_reequilibration": 1.0}), detector="thin_layer")
B_ps = lambda p: p.with_values({"chem.regeneration.residual_label_carryover_fraction": 1e-6,
    "chem.regeneration.activity_loss_per_cycle": 0.0, "ma.chemistries.alp_hqdp.substrate_concentration": 3e-3})
cv = lambda p: L.with_bounds(p, "chem.nsb.blank_CV_analog_electrochemical", value=0.14, low=0.05, high=0.25)
for lab, p in [("B0", B_ps(ps0)), ("B1", pre_el(B_ps(ps0)))] + [(f"B1 factor {f}", pre_el(B_ps(ps0)).with_values({"ma.nsb.surface_factor_packed_bed": f})) for f in (1,2,3)] + [("B1 blank CV 0.14", cv(pre_el(B_ps(ps0))))]:
    s = L.mc(B, p, n=2000, lod_scale=0.996/0.90)
    print(lab, L.fmt(s["lod_nominal"]), L.fmt(s["lod_median"]), L.fmt(s["lod_p05"]), L.fmt(s["lod_p95"]), round(s["p_success"],2), round(s["p_lod_only"],2), L.fmt(s["uloq_nominal"],3), round(s["time_to_result_min"],1), flush=True)
