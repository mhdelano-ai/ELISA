"""Nearest-model estimates for docs/13 Revision B (scratch copy of the repository; n = 2000, seed of L.mc default
20261111). Builds on the docs/12/13 helpers (runs.py of the review session)."""
import sys, time, json
sys.argv = ["x", "none"]
exec(open("/tmp/claude-0/-home-user-ELISA/04a7436b-08e5-5186-a749-bb6e7aad5fa5/scratchpad/runs.py").read())

def AarchB(t_inc=24.25, t_acc=13.0, vol=1.34):
    d = {"ma.timing.in_vial_incubation": t_inc, "hw.timing.accumulation_time": t_acc,
         "hw.smfl.loop_flush_volumes_for_transfer": 6.6, "ma.timing.post_sample_wash": 1.5,
         "hw.timing.substrate_fill": 0.5, "ma.timing.bead_flush_and_clean": 2.0, "hw.timing.readout_time": 1.0,
         "ma.geometry.magnetic_trap_volume": vol}
    return replace(L.base_arch("OS").with_design(**os_rec).with_design(**d), detector="thin_layer")
DIL = 1.80   # 150 + 10 + 6 + 10 uL + 3.45 uL BSM parked flow after the pre-switch = 179.5 uL per 100 uL loop
Bps = lambda p, dil=DIL: S3(stir(dil)(p).with_values({"ma.nsb.surface_factor_tubing": 0.01}))
NO = "hw.gamry.noise_rms_flow"
B0 = AarchB()
rows = [
  # reference rows (docs/13 as published; docs/15 reproductions)
  ("ref: docs/13 A (credit x0.01)", Aarch(1.0), S3(pre_el(A_ps(ps0)))),
  ("ref: docs/13 A, no credit", Aarch(1.0), S3(A_ps(ps0))),
  # step-by-step from docs/13 to Revision B, no credit
  ("step: no credit, dilution /1.80", Aarch(1.0), Bps(ps0)),
  ("step: + incubation 24.25 (eff.), acc 15, RC 1.0", AarchB(24.25, 15.0, 1.0), Bps(ps0)),
  ("step: + accumulation 13", AarchB(24.25, 13.0, 1.0), Bps(ps0)),
  ("REV B, no credit (headline)", B0, Bps(ps0)),
  ("REV B, credit x0.01", B0, pre_el(Bps(ps0))),
  ("REV B, credit x0.08 (stubs 1 mm)", B0, pre_el(Bps(ps0), 0.08)),
  ("REV B + L6+L7, no credit", B0, Bps(L67(ps0))),
  ("REV B + L6+L7, credit x0.01", B0, pre_el(Bps(L67(ps0)))),
  ("REV B S4a, no credit", B0, Bps(S4a(ps0))),
  ("REV B S4a, credit x0.01", B0, pre_el(Bps(S4a(ps0)))),
  ("REV B S4a, credit x0.08", B0, pre_el(Bps(S4a(ps0)), 0.08)),
  ("REV B, no credit, stirred 22 only (pause = 0 capture)", AarchB(22.0), Bps(ps0)),
  ("REV B, no credit, no tidal pauses (26.5)", AarchB(26.5), Bps(ps0)),
  ("REV B, no credit, dilution /2.2 (gen-1 mixing)", B0, Bps(ps0, 2.2)),
  ("REV B, no credit, bead dose CV 0.05", B0, Bps(ps0).with_values({"ma.capture.bead_dose_cv": 0.05})),
  ("REV B, no credit, bead dose CV 0.10", B0, Bps(ps0).with_values({"ma.capture.bead_dose_cv": 0.10})),
]
for sd in (0.023, 0.05, 0.08, 0.155, 0.30):
    rows.append((f"REV B, no credit, read SD(Q_net) {sd} nC (i_ref {sd/7.746*1e3:.1f} pA)", B0, Bps(ps0).with_values({NO: sd * 1e-9 / 7.746})))
rows.append(("REV B + L6+L7, no credit, read SD 0.05 nC", B0, Bps(L67(ps0)).with_values({NO: 0.05e-9 / 7.746})))
which = sys.argv_sel if hasattr(sys, "argv_sel") else None
out = []
for lab, a, p in rows:
    t = time.time(); s = L.mc(a, p, n=2000, lod_scale=1/0.90)
    r = dict(label=lab, nom=s["lod_nominal"], med=s["lod_median"], p05=s["lod_p05"], p95=s["lod_p95"], P=s["p_success"],
             P_lod=s["p_lod_only"], uloq=s["uloq_nominal"])
    out.append(r)
    print(f"{lab:62s} nom {r['nom']:.2f} med {r['med']:.2f} [{r['p05']:.2f}-{r['p95']:.1f}] P {r['P']:.3f} "
          f"P(LOD<=1) {r['P_lod']:.3f} ULOQ {r['uloq']:.0f} ({time.time()-t:.0f}s)", flush=True)
json.dump(out, open("runB.json", "w"), indent=1)
