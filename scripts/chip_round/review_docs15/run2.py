import sys; sys.argv=["x","none"]
exec(open("/tmp/claude-0/-home-user-ELISA/04a7436b-08e5-5186-a749-bb6e7aad5fa5/scratchpad/runs.py").read())
A1v=Aarch(1.0)
for lab,p in [("escape 0.11 nominal", S3(pre_el(A_ps(ps0),0.11))), ("escape 0.11 S4a", S3(pre_el(A_ps(S4a(ps0)),0.11))),
              ("escape 0.11 L6+L7", S3(pre_el(A_ps(L67(ps0)),0.11))), ("no pre-el L6+L7", S3(A_ps(L67(ps0))))]:
    s=L.mc(A1v,p,n=2000,lod_scale=1/0.9)
    print(f"{lab:30s} nom {s['lod_nominal']:.2f} med {s['lod_median']:.2f} [{s['lod_p05']:.2f}-{s['lod_p95']:.1f}] P {s['p_success']:.3f} ULOQ {s['uloq_nominal']:.0f}",flush=True)
