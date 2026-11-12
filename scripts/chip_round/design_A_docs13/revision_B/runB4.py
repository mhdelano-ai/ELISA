exec(open("runB.py").read().split("B0 = AarchB()")[0])
EFF = 22.15 + 0.5 * 6.35
rows = [("step1: docs/13 A no credit, dilution /1.85", Aarch(1.0), Bps(ps0, 1.85)),
        ("step2: + incubation 25.33 eff (acc 15, RC 1.0)", AarchB(EFF, 15.0, 1.0), Bps(ps0, 1.85)),
        ("step3: + accumulation 11", AarchB(EFF, 11.0, 1.0), Bps(ps0, 1.85)),
        ("step4: + cell 1.34 uL (= FINAL)", AarchB(EFF, 11.0, 1.34), Bps(ps0, 1.85))]
for lab, a, p in rows:
    s = L.mc(a, p, n=2000, lod_scale=1/0.90)
    print(f"{lab:52s} nom {s['lod_nominal']:.2f} med {s['lod_median']:.2f} [{s['lod_p05']:.2f}-{s['lod_p95']:.1f}] P {s['p_success']:.3f} ULOQ {s['uloq_nominal']:.0f}", flush=True)
