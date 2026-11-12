import sys, json
exec(open("runB.py").read().split("B0 = AarchB()")[0])
EFF = 22.15 + 0.5 * 6.35      # stirred + ma.capture.in_vial_unstirred_rate_factor (0.5) x paused
F = AarchB(EFF, 11.0, 1.34); dl = 1.85
NO = "hw.gamry.noise_rms_flow"
rows = [
  ("FINAL no credit (headline)", F, Bps(ps0, dl)),
  ("FINAL credit x0.01", F, pre_el(Bps(ps0, dl))),
  ("FINAL credit x0.07 (stubs 1 mm)", F, pre_el(Bps(ps0, dl), 0.07)),
  ("FINAL + L6+L7 no credit", F, Bps(L67(ps0), dl)),
  ("FINAL + L6+L7 credit x0.01", F, pre_el(Bps(L67(ps0), dl))),
  ("FINAL S4a no credit", F, Bps(S4a(ps0), dl)),
  ("FINAL S4a credit x0.01", F, pre_el(Bps(S4a(ps0), dl))),
  ("FINAL S4a credit x0.07", F, pre_el(Bps(S4a(ps0), dl), 0.07)),
  ("FINAL no credit, tidal allowed during reads (eff 28.5)", AarchB(28.5, 11.0, 1.34), Bps(ps0, dl)),
  ("FINAL no credit, unstirred = 0 capture (22.15)", AarchB(22.15, 11.0, 1.34), Bps(ps0, dl)),
  ("FINAL no credit, dilution /2.2", F, Bps(ps0, 2.2)),
  ("FINAL no credit, bead CV 0.05", F, Bps(ps0, dl).with_values({"ma.capture.bead_dose_cv": 0.05})),
  ("FINAL no credit, bead CV 0.10", F, Bps(ps0, dl).with_values({"ma.capture.bead_dose_cv": 0.10})),
  ("FINAL no credit, transfer 0.80", F, Bps(ps0, dl).with_values({"ma.capture.magnetic_trap_efficiency": 0.80})),
]
for sd in (0.023, 0.05, 0.08, 0.155, 0.30):
    rows.append((f"FINAL no credit, read SD {sd} nC", F, Bps(ps0, dl).with_values({NO: sd * 1e-9 / 7.746})))
rows.append(("FINAL credit x0.01, read SD 0.05 nC", F, pre_el(Bps(ps0, dl)).with_values({NO: 0.05e-9 / 7.746})))
rows.append(("FINAL + L6+L7, read SD 0.05 nC", F, Bps(L67(ps0), dl).with_values({NO: 0.05e-9 / 7.746})))
out = []
for lab, a, p in rows:
    s = L.mc(a, p, n=2000, lod_scale=1/0.90)
    r = dict(label=lab, nom=s["lod_nominal"], med=s["lod_median"], p05=s["lod_p05"], p95=s["lod_p95"], P=s["p_success"], uloq=s["uloq_nominal"])
    out.append(r)
    print(f"{lab:58s} nom {r['nom']:.2f} med {r['med']:.2f} [{r['p05']:.2f}-{r['p95']:.1f}] P {r['P']:.3f} ULOQ {r['uloq']:.0f}", flush=True)
json.dump(out, open("runB3.json", "w"), indent=1)
