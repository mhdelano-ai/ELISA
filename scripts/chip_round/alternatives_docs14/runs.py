import sys, json
from dataclasses import replace
COPY = "/tmp/claude-0/-home-user-ELISA/04a7436b-08e5-5186-a749-bb6e7aad5fa5/scratchpad/copy"
sys.path[:0] = [COPY + "/scripts", COPY + "/src"]
import design_lib as L, final_designs as F
ps0 = L.load_ps()
IMP = "ma.chemistries.alp_hqdp.free_product_impurity"
CONT = "ma.nsb.blank_igg_contamination_equivalent"
def pre_el(p, f):
    if f == 1: return p
    if IMP in p.pinned: return p.with_values({IMP: float(p.values[IMP]) * f})
    return L.with_bounds(p, IMP, value=1e-5*f, low=1e-7*f, high=1e-3*f)
# B (docs/12 Appendix A)
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
BS = 0.996/0.90
# C / C'
fc = json.load(open(L.OUT / "optimum_FRC__baseline.json"))["design"]
C = L.base_arch("FRC").with_design(**fc)
C_ps = lambda p: L.with_bounds(L.with_bounds(p.with_values({"ma.nsb.surface_factor_chip": 0.01}),
    "ma.noise.electrode_sensitivity_cv_fouling", value=0.02, low=0.005, high=0.05),
    "ma.reuse.electrode_sensitivity_loss_per_cycle_fouling", value=0.001, low=0.0, high=0.005)
Cp = C.with_design(**{"hw.timing.regeneration_and_reequilibration": 7.0})
def Cp_ps(p):
    p = C_ps(p).with_values({"chem.regeneration.activity_loss_per_cycle": 0.0})
    return L.with_bounds(p, "chem.regeneration.residual_label_carryover_fraction", value=1e-4, low=1e-6, high=1e-3)
Cp15 = Cp.with_design(**{"hw.timing.accumulation_time": 15})
ID = lambda p: p
L67 = F.scen("L6+L7")[1]; S4a = F.scen("S4a")[1]
bed = lambda f: (lambda p: p.with_values({"ma.nsb.surface_factor_packed_bed": f}))
bcv = lambda p: L.with_bounds(p, "chem.nsb.blank_CV_analog_electrochemical", value=0.14, low=0.05, high=0.25)
mM3 = lambda p: p.with_values({"ma.chemistries.alp_hqdp.substrate_concentration": 3e-3})
M = lambda pgml: pgml * 1e-12 / 1.5e5 * 1e3
def add_cont(r, c):
    return lambda p: L.with_bounds(p, CONT, value=M(r*c), low=M(r*c), high=3e-15 + M(r*c))
def pin_cont(r, c):
    return lambda p: p.with_values({CONT: max(M(r*c), 1e-30)})
def run(lab, arch, cand, scen=ID, post=ID, f=1, scale=1.0):
    p = post(pre_el(cand(scen(ps0)), f))
    s = L.mc(arch, p, n=2000, lod_scale=scale)
    print(f"| {lab} | {L.fmt(s['lod_nominal'])} | {L.fmt(s['leff_median'])} / {L.fmt(s['lod_median'])} [{L.fmt(s['lod_p05'])}-{L.fmt(s['lod_p95'])}] | {s['p_success']:.3f} | {s['p_lod_only']:.3f} | {L.fmt(s['uloq_nominal'],3)} | {s['time_to_result_min']:.1f} |", flush=True)
which = sys.argv[1]
if which == "B":
    for f in (1, 0.3, 0.1, 0.05, 0.01):
        run(f"B x{f}", B, B_ps, f=f, scale=BS)
    for f in (1, 0.05):
        run(f"B L6+L7 x{f}", B, B_ps, scen=L67, f=f, scale=BS)
        run(f"B S4a x{f}", B, B_ps, scen=S4a, f=f, scale=BS)
        run(f"B blankCV0.14 x{f}", B, B_ps, post=bcv, f=f, scale=BS)
        for b in (1, 2, 3, 10):
            run(f"B bed{b} x{f}", B, B_ps, post=bed(b), f=f, scale=BS)
if which == "C":
    run("C2 ref", C, C_ps)
    for f in (1, 0.05, 0.01):
        run(f"C' x{f}", Cp, Cp_ps, f=f)
    for f in (1, 0.05):
        run(f"C' L6+L7 x{f}", Cp, Cp_ps, scen=L67, f=f)
        run(f"C' S4a x{f}", Cp, Cp_ps, scen=S4a, f=f)
        run(f"C' acc15 3mM x{f}", Cp15, lambda p: mM3(Cp_ps(p)), f=f)
        run(f"C' blankCV0.14 x{f}", Cp, Cp_ps, post=bcv, f=f)
if which == "Cbed":
    for f in (1, 0.05):
        for b in (1, 2, 3, 5, 10, 30):
            run(f"C' bed{b} x{f}", Cp, Cp_ps, post=bed(b), f=f)
if which == "Cco":
    run("C'1 pinned 1e-30 (repro)", Cp, Cp_ps, post=pin_cont(0, 1), f=0.01)
    run("C'1 r1e-4 1000 pinned (repro)", Cp, Cp_ps, post=pin_cont(1e-4, 1000), f=0.01)
    run("C'1 r1e-4 1000 additive", Cp, Cp_ps, post=add_cont(1e-4, 1000), f=0.01)
    run("C'1 r3e-4 1000 additive", Cp, Cp_ps, post=add_cont(3e-4, 1000), f=0.01)
    for c in (1000, 100):
        for r in (1e-5, 1e-4, 3e-4, 1e-3, 1e-2, 8e-2):
            run(f"C'0 r{r} Cprev{c} additive", Cp, Cp_ps, post=add_cont(r, c), f=1)
