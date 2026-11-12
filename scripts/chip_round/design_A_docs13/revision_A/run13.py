import sys, json, time
R='/tmp/claude-0/-home-user-ELISA/04a7436b-08e5-5186-a749-bb6e7aad5fa5/scratchpad/repo'
sys.path[:0]=[R+'/scripts', R+'/src']
from dataclasses import replace
import design_lib as L, final_designs as F
ps0 = L.load_ps()
STIR="ma.capture.in_vial_unstirred_rate_factor"; IMP="ma.chemistries.alp_hqdp.free_product_impurity"
stir=lambda dil:(lambda p: L.with_bounds(p, STIR, value=1/dil, low=0.2/dil, high=1/dil))
def pre_el(p):
    if IMP in p.pinned: return p.with_values({IMP: float(p.values[IMP])*0.01})
    return L.with_bounds(p, IMP, value=1e-7, low=1e-9, high=1e-5)
os_rec=json.load(open(L.OUT/"optimum_OS__baseline.json"))["design"]
def Aarch(vol=2.0):
    d={"ma.timing.in_vial_incubation":30,"hw.timing.accumulation_time":15,
      "hw.smfl.loop_flush_volumes_for_transfer":6.6,"ma.timing.post_sample_wash":1.5,
      "hw.timing.substrate_fill":0.5,"ma.timing.bead_flush_and_clean":2.0,"hw.timing.readout_time":1.0}
    if vol!=2.0: d["ma.geometry.magnetic_trap_volume"]=vol
    return replace(L.base_arch("OS").with_design(**os_rec).with_design(**d), detector="thin_layer")
A_ps=lambda p: stir(1.7)(p).with_values({"ma.nsb.surface_factor_tubing":0.01})
S3=lambda p: p.with_values({"ma.chemistries.alp_hqdp.substrate_concentration":3e-3})
runs={}
def go(label, arch, p):
    t=time.time(); s=L.mc(arch,p,n=2000,lod_scale=1/0.90)
    runs[label]=dict(nom=s['lod_nominal'],med=s['lod_median'],p05=s['lod_p05'],p95=s['lod_p95'],P=s['p_success'],Plod=s['p_lod_only'],uloq=s['uloq_nominal'])
    print(f"{label:45s} nom {s['lod_nominal']:.2f} med {s['lod_median']:.2f} [{s['lod_p05']:.2f}-{s['lod_p95']:.0f}] P {s['p_success']:.2f} PLOD {s['p_lod_only']:.2f} ULOQ {s['uloq_nominal']:.0f} ({time.time()-t:.0f}s)", flush=True)
base=lambda p: S3(pre_el(A_ps(p)))
L67=F.scen("L6+L7")[1]; S4a=F.scen("S4a")[1]
go("A1 3mM 2uL (docs/12 repro)", Aarch(2.0), base(ps0))
go("A2 3mM 1uL", Aarch(1.0), base(ps0))
go("A2 1mM 1uL", Aarch(1.0), pre_el(A_ps(ps0)))
go("A2 3mM 1uL + L6+L7", Aarch(1.0), base(L67(ps0)))
go("A2 3mM 1uL S4a", Aarch(1.0), base(S4a(ps0)))
go("A2 bead_dose_cv pinned 0.05", Aarch(1.0), base(ps0).with_values({"ma.capture.bead_dose_cv":0.05}))
go("A2 bead_dose_cv pinned 0.10", Aarch(1.0), base(ps0).with_values({"ma.capture.bead_dose_cv":0.10}))
go("A2 bead_dose_cv pinned 0.15", Aarch(1.0), base(ps0).with_values({"ma.capture.bead_dose_cv":0.15}))
go("A2 trap_eff pinned 0.80", Aarch(1.0), base(ps0).with_values({"ma.capture.magnetic_trap_efficiency":0.80}))
go("A2 noise_rms_flow pinned 2e-11", Aarch(1.0), base(ps0).with_values({"hw.gamry.noise_rms_flow":2e-11}))
go("A2 noise_rms_flow pinned 1e-10", Aarch(1.0), base(ps0).with_values({"hw.gamry.noise_rms_flow":1e-10}))
json.dump(runs, open('/tmp/claude-0/-home-user-ELISA/04a7436b-08e5-5186-a749-bb6e7aad5fa5/scratchpad/runs/run13.json','w'), indent=1)
