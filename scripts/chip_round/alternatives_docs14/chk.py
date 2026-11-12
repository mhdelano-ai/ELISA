exec(open("run_c14.py").read().split("runs = [")[0])
base = pre_el(Cp_ps(ps0))
for lab, p in [("base", base), ("cont tiny", L.with_bounds(base, CONT, value=0.0, low=0.0, high=1e-30)),
               ("cont 1e-4 pinned", base.with_values({CONT: 1e-4*1000*PG_M})),
               ("cont 1e-4 fixed C1-style high only", L.with_bounds(base, CONT, high=1e-4*1000*PG_M)),
               ("cont 1e-3 pinned", base.with_values({CONT: 1e-3*1000*PG_M}))]:
    s = L.mc(Cp, p, n=2000)
    print(lab, L.fmt(s["lod_nominal"]), L.fmt(s["lod_median"]), L.fmt(s["lod_p05"]), L.fmt(s["lod_p95"]), round(s["p_success"],2), flush=True)
