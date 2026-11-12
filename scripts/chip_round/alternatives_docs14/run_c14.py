"""docs/14 runs: revised candidate C (C') on the FRC optimum. Run from the scratch COPY only."""
import sys, json, time
COPY = "/tmp/claude-0/-home-user-ELISA/04a7436b-08e5-5186-a749-bb6e7aad5fa5/scratchpad/copy"
sys.path[:0] = [COPY + "/scripts", COPY + "/src"]
import design_lib as L, final_designs as F

ps0 = L.load_ps()
IMP = "ma.chemistries.alp_hqdp.free_product_impurity"
PB = "ma.nsb.surface_factor_packed_bed"
CONT = "ma.nsb.blank_igg_contamination_equivalent"
PG_M = 1e-12 / 1.5e5 * 1e3          # 1 pg/mL as M (final_designs.CONTAMINATION_1PG_M)

def pre_el(p):
    if IMP in p.pinned: return p.with_values({IMP: float(p.values[IMP]) * 0.01})
    return L.with_bounds(p, IMP, value=1e-7, low=1e-9, high=1e-5)

fc = json.load(open(L.OUT / "optimum_FRC__baseline.json"))["design"]
C = L.base_arch("FRC").with_design(**fc)
def C_ps(p):   # docs/12 C2: side outlet + non-fouling electrode class
    p = p.with_values({"ma.nsb.surface_factor_chip": 0.01})
    p = L.with_bounds(p, "ma.noise.electrode_sensitivity_cv_fouling", value=0.02, low=0.005, high=0.05)
    return L.with_bounds(p, "ma.reuse.electrode_sensitivity_loss_per_cycle_fouling", value=0.001, low=0.0, high=0.005)

# C': fresh capture layer each run (renewable bed or whole-layer renewal), dock-side valves only.
# renewal block = flush-out 1.0 + empty-cavity strip 2.0 + re-equilibration 1.0 + bed pack 3.0 = 7.0 min
Cp = C.with_design(**{"hw.timing.regeneration_and_reequilibration": 7.0})
def Cp_ps(p):
    p = C_ps(p).with_values({"chem.regeneration.activity_loss_per_cycle": 0.0})
    return L.with_bounds(p, "chem.regeneration.residual_label_carryover_fraction", value=1e-4, low=1e-6, high=1e-3)
Cp15 = C.with_design(**{"hw.timing.regeneration_and_reequilibration": 7.0, "hw.timing.accumulation_time": 15})
mM3 = lambda p: p.with_values({"ma.chemistries.alp_hqdp.substrate_concentration": 3e-3})
L67 = F.scen("L6+L7")[1]; S4a = F.scen("S4a")[1]
def carry(r):   # residual analyte fraction r x previous sample (uniform 0..1000 pg/mL) -> blank contamination
    hi = r * 1000 * PG_M
    return lambda p: L.with_bounds(p, CONT, value=hi / 2, low=0.0, high=hi)
pb = lambda f: (lambda p: p.with_values({PB: f}))
cv = lambda p: L.with_bounds(p, "chem.nsb.blank_CV_analog_electrochemical", value=0.14, low=0.05, high=0.25)

runs = [
    ("REF C2 (docs/12)", C, C_ps(ps0)),
    ("C'0 fresh layer, dock valves", Cp, Cp_ps(ps0)),
    ("C'1 = C'0 + pre-electrolysis", Cp, pre_el(Cp_ps(ps0))),
    ("C'1 + L6+L7", Cp, L67(pre_el(Cp_ps(ps0)))),
    ("C'1 acc 15 min, 3 mM", Cp15, mM3(pre_el(Cp_ps(ps0)))),
    ("C'1 under S4a", Cp, pre_el(S4a(Cp_ps(ps0)))),
    ("C'1 bed-dose CV (blank CV 0.14)", Cp, cv(pre_el(Cp_ps(ps0)))),
]
for f in (1, 2, 3, 5, 10, 30):
    runs.append((f"C'1 packed-bed factor {f}", Cp, pb(f)(pre_el(Cp_ps(ps0)))))
for r in (1e-4, 1e-3, 1e-2, 8e-2):
    runs.append((f"C'1 residual analyte {r:g}", Cp, carry(r)(pre_el(Cp_ps(ps0)))))
for r in (1e-4, 1e-3):
    runs.append((f"C'1+L6+L7 residual analyte {r:g}", Cp, carry(r)(L67(pre_el(Cp_ps(ps0))))))

out = []
for lab, a, p in runs:
    t0 = time.time()
    s = L.mc(a, p, n=2000)
    d = s["_mc"].nominal.diagnostics
    row = dict(run=lab, nominal=s["lod_nominal"], median=s["lod_median"], p05=s["lod_p05"], p95=s["lod_p95"],
               P=s["p_success"], Plod=s["p_lod_only"], uloq=s["uloq_nominal"], t=s["time_to_result_min"],
               label_frac=float(d.get("label_fraction_low", float("nan"))),
               carry_top=float(d.get("carryover_after_top_pgml", float("nan"))))
    out.append(row)
    print(f"| {lab} | {L.fmt(row['nominal'])} | {L.fmt(row['median'])} [{L.fmt(row['p05'])}-{L.fmt(row['p95'])}] | "
          f"{row['P']:.2f} | {row['Plod']:.2f} | {L.fmt(row['uloq'],3)} | {row['t']:.1f} | carry_top {L.fmt(row['carry_top'])} | {time.time()-t0:.0f}s", flush=True)
json.dump(out, open(COPY + "/../c14_runs.json", "w"), indent=1)
