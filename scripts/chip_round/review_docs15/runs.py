import sys, json, time
R = "/tmp/claude-0/-home-user-ELISA/04a7436b-08e5-5186-a749-bb6e7aad5fa5/scratchpad/repo"
sys.path[:0] = [R + "/scripts", R + "/src"]
from dataclasses import replace
import design_lib as L, final_designs as F

ps0 = L.load_ps()
STIR = "ma.capture.in_vial_unstirred_rate_factor"; IMP = "ma.chemistries.alp_hqdp.free_product_impurity"
stir = lambda dil: (lambda p: L.with_bounds(p, STIR, value=1/dil, low=0.2/dil, high=1/dil))
def pre_el(p, f=0.01):
    if IMP in p.pinned: return p.with_values({IMP: float(p.values[IMP]) * f})
    return L.with_bounds(p, IMP, value=1e-5*f, low=1e-7*f, high=1e-3*f)
os_rec = json.load(open(L.OUT / "optimum_OS__baseline.json"))["design"]
def Aarch(vol=None):
    d = {"ma.timing.in_vial_incubation": 30, "hw.timing.accumulation_time": 15,
         "hw.smfl.loop_flush_volumes_for_transfer": 6.6, "ma.timing.post_sample_wash": 1.5,
         "hw.timing.substrate_fill": 0.5, "ma.timing.bead_flush_and_clean": 2.0, "hw.timing.readout_time": 1.0}
    if vol: d["ma.geometry.magnetic_trap_volume"] = vol
    return replace(L.base_arch("OS").with_design(**os_rec).with_design(**d), detector="thin_layer")
A_ps = lambda p: stir(1.7)(p).with_values({"ma.nsb.surface_factor_tubing": 0.01})
S3 = lambda p: p.with_values({"ma.chemistries.alp_hqdp.substrate_concentration": 3e-3})
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
fc = json.load(open(L.OUT / "optimum_FRC__baseline.json"))["design"]
C = L.base_arch("FRC").with_design(**fc)
C_ps = lambda p: L.with_bounds(L.with_bounds(p.with_values({"ma.nsb.surface_factor_chip": 0.01}),
    "ma.noise.electrode_sensitivity_cv_fouling", value=0.02, low=0.005, high=0.05),
    "ma.reuse.electrode_sensitivity_loss_per_cycle_fouling", value=0.001, low=0.0, high=0.005)
Cp = C.with_design(**{"hw.timing.regeneration_and_reequilibration": 7.0})
def Cp_ps(p):
    p = C_ps(p).with_values({"chem.regeneration.activity_loss_per_cycle": 0.0})
    return L.with_bounds(p, "chem.regeneration.residual_label_carryover_fraction", value=1e-4, low=1e-6, high=1e-3)
L67 = F.scen("L6+L7")[1]; S4a = F.scen("S4a")[1]
CONT = "ma.nsb.blank_igg_contamination_equivalent"
M = lambda pg: pg * 1e-12 / 1.5e5 * 1e3

which = sys.argv[1] if len(sys.argv) > 1 else "all"
runs = []
if which in ("A", "all"):
    A1v = Aarch(1.0); A2 = Aarch()
    runs += [
      ("A0 (docs12)", A2, A_ps(ps0), 1/0.9),
      ("A1 (docs12)", A2, pre_el(A_ps(ps0)), 1/0.9),
      ("A1 3mM RC2 (docs12/13)", A2, S3(pre_el(A_ps(ps0))), 1/0.9),
      ("docs13 A 3mM RC1", A1v, S3(pre_el(A_ps(ps0))), 1/0.9),
      ("docs13 A 1mM RC1", A1v, pre_el(A_ps(ps0)), 1/0.9),
      ("docs13 A L6+L7", A1v, S3(pre_el(A_ps(L67(ps0)))), 1/0.9),
      ("docs13 A S4a", A1v, S3(pre_el(A_ps(S4a(ps0)))), 1/0.9),
      ("docs13 A dose cv 0.10", A1v, S3(pre_el(A_ps(ps0))).with_values({"ma.capture.bead_dose_cv": 0.10}), 1/0.9),
      ("docs13 A noise 20 pA", A1v, S3(pre_el(A_ps(ps0))).with_values({"hw.gamry.noise_rms_flow": 2e-11}), 1/0.9),
      ("REVIEW A RC1 3mM escape 0.04", A1v, S3(pre_el(A_ps(ps0), 0.04)), 1/0.9),
      ("REVIEW A RC1 3mM no pre-el", A1v, S3(A_ps(ps0)), 1/0.9),
      ("REVIEW A RC1 3mM no pre-el S4a", A1v, S3(A_ps(S4a(ps0))), 1/0.9),
      ("REVIEW A RC1 3mM escape 0.04 S4a", A1v, S3(pre_el(A_ps(S4a(ps0)), 0.04)), 1/0.9),
      ("REVIEW A RC1 3mM pre-el, tubing factor NOT pinned", A1v, S3(pre_el(stir(1.7)(ps0))), 1/0.9),
      ("REVIEW A RC1 3mM pre-el, stir /2.2", A1v, S3(pre_el(stir(2.2)(ps0).with_values({"ma.nsb.surface_factor_tubing": 0.01}))), 1/0.9),
    ]
if which in ("B", "all"):
    runs += [("B0", B, B_ps(ps0), 0.996/0.9), ("B1", B, pre_el(B_ps(ps0)), 0.996/0.9),
             ("B1 escape 0.05 (guard cell 0.95)", B, pre_el(B_ps(ps0), 0.05), 0.996/0.9)]
if which in ("C", "all"):
    runs += [("C'1", Cp, pre_el(Cp_ps(ps0)), 1.0),
             ("C'1 cont pinned 1e-30 (docs14 method)", Cp, pre_el(Cp_ps(ps0)).with_values({CONT: 1e-30}), 1.0),
             ("C'1 r=1e-4 Cprev 1000 pinned (docs14)", Cp, pre_el(Cp_ps(ps0)).with_values({CONT: M(1e-4*1000)}), 1.0),
             ("C'1 r=1e-4 Cprev 1000 ADDED to default", Cp, L.with_bounds(pre_el(Cp_ps(ps0)), CONT, value=M(0.1), low=M(0.1), high=3e-15+M(0.1)), 1.0),
             ("C'1 r=3e-4 Cprev 1000 ADDED", Cp, L.with_bounds(pre_el(Cp_ps(ps0)), CONT, value=M(0.3), low=M(0.3), high=3e-15+M(0.3)), 1.0)]
for lab, a, p, f in runs:
    t = time.time()
    s = L.mc(a, p, n=2000, lod_scale=f)
    print(f"{lab:55s} nom {s['lod_nominal']:.2f} med {s['lod_median']:.2f} [{s['lod_p05']:.2f}-{s['lod_p95']:.1f}] "
          f"P {s['p_success']:.3f} P(LOD<=1) {s['p_lod_only']:.3f} ULOQ {s['uloq_nominal']:.0f} ({time.time()-t:.0f}s)", flush=True)
