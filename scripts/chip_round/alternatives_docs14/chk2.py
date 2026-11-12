exec(open("run_c14.py").read().split("runs = [")[0])
base = pre_el(Cp_ps(ps0))
for prev in (1000, 100):
  for r in (1e-5, 1e-4, 3e-4, 1e-3, 1e-2, 8e-2):
    s = L.mc(Cp, base.with_values({CONT: r*prev*PG_M}), n=2000)
    print(prev, r, L.fmt(s["lod_nominal"]), L.fmt(s["lod_median"]), round(s["p_success"],2), flush=True)
