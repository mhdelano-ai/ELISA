import sys
exec(open("runB.py").read().split("B0 = AarchB()")[0])
rows = [
  ("split 26.5/13: eff 24.25, acc 13, /1.80", AarchB(24.25, 13.0), Bps(ps0, 1.80)),
  ("split 28/11.5: eff 25.08, acc 11.5, /1.81", AarchB(22.15 + 0.5 * 5.85, 11.5), Bps(ps0, 1.81)),
  ("split 29.5/10: eff 25.83, acc 10, /1.82", AarchB(22.15 + 0.5 * 7.35, 10.0), Bps(ps0, 1.82)),
  ("split 30.5/9: eff 26.33, acc 9, /1.83", AarchB(22.15 + 0.5 * 8.35, 9.0), Bps(ps0, 1.83)),
  ("split 31.5/8: eff 27.0, acc 8, /1.80", AarchB(22.5 + 0.5 * 9.0, 8.0), Bps(ps0, 1.80)),
  ("split 29.5/10 + L6+L7", AarchB(22.15 + 0.5 * 7.35, 10.0), Bps(L67(ps0), 1.82)),
  ("relaxed (tidal allowed in reads) 29.5/10: eff 29.5", AarchB(29.5, 10.0), Bps(ps0, 1.82)),
]
for lab, a, p in rows:
    s = L.mc(a, p, n=2000, lod_scale=1/0.90)
    print(f"{lab:55s} nom {s['lod_nominal']:.2f} med {s['lod_median']:.2f} [{s['lod_p05']:.2f}-{s['lod_p95']:.1f}] P {s['p_success']:.3f} ULOQ {s['uloq_nominal']:.0f}", flush=True)
