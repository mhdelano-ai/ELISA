import sys, time
sys.path.insert(0, "/tmp/claude-0/-home-user-ELISA/04a7436b-08e5-5186-a749-bb6e7aad5fa5/scratchpad/copy/scripts")
import design_lib as L, final_designs as F
from elisa_sim.model import evaluate
ps0 = L.load_ps()
ds = F.designs(ps0)
for k,a,pm,f in ds:
    if k in ("P-chamb","B-bed"):
        t=time.time(); s=L.mc(a, pm(ps0), n=2000, lod_scale=f); print(k, round(time.time()-t,1),"s", s['lod_median'], s['p_success'])
        r = evaluate(a, pm(ps0))
        d=r.diagnostics
        for kk in ["accumulation_volume_uL","capture_area_m2","nsb_area_eff_m2","bead_share_of_nsb","cell_conversion","eluted_fraction","capture_fraction_low","label_fraction_low","enzymes_at_1pg","N_nsb","blank_equivalent_pgml","conjugate_peak_dilution","loop_transfer","timeline_min"]:
            print("  ",kk, d[kk])
        print("  limiting", r.limiting_term, r.time_to_result_min)
        print("  varfrac", {k2: round(float(v),3) for k2,v in r.variance_fractions().items()})
# FRC
import json
rec=json.load(open(L.OUT/"optimum_FRC__baseline.json"))["design"]
a=L.base_arch("FRC").with_design(**rec)
t=time.time(); s=L.mc(a, ps0, n=2000); print("FRC", round(time.time()-t,1), s['lod_nominal'], s['lod_median'], s['lod_p05'], s['lod_p95'], s['p_success'], s['time_to_result_min'])
r=evaluate(a, ps0); d=r.diagnostics
for kk in ["accumulation_volume_uL","capture_area_m2","nsb_area_eff_m2","capture_fraction_low","label_fraction_low","blank_equivalent_pgml","N_nsb","N_carry","enzymes_at_1pg","timeline_min"]:
    print("  ",kk,d[kk])
print("  varfrac", {k2: round(float(v),3) for k2,v in r.variance_fractions().items()})
print("  dp", L.reactor_pressure_drop_mpa(a, ps0))
