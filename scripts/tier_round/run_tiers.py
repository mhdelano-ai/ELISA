#!/usr/bin/env python3
"""Evaluate the three implementations of docs/30 and their alternatives, scenarios and sensitivities.

  python scripts/tier_round/run_tiers.py [--n 2000] [--quick]
writes results/tier_round/tiers.md (tables) and results/tier_round/tiers.json (all numbers).

Tier 1 and tier 2 use scripts/tier_round/tierkit.py; tier 3 uses the kit for the two-bed transfer design and the
audited model (elisa_sim, through scripts/design_lib.py and scripts/final_designs.py) for the earlier bead-chamber
design read in the MicruX cell.  Monte Carlo: n = 2000, seed 20261111 (repository settings).
"""
from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))
import designs as D  # noqa: E402
import tierkit as tk  # noqa: E402
import design_lib as L  # noqa: E402

OUT = ROOT / "results" / "tier_round"
MB = "ma.nsb.surface_factor_magnetic_beads"
LF = "ma.nsb.label_factor_igg_enzyme_conjugate"
S0 = "ma.chemistries.alp_hqdp.substrate_concentration"
IMP = "ma.chemistries.alp_hqdp.free_product_impurity"
AU10 = dict(kind="printed", area=np.pi * (1.5e-3) ** 2, we_factor_key="tr.nsb.surface_factor_gold_oeg",
            floor_factor_key="tr.nsb.surface_factor_printed_electrode")


# ---- the designs -----------------------------------------------------------------------------------------
def t1(electrode="SE1", **kw):
    """Tier 1 primary: capture on a thin-film gold electrode, product read at the electrode while substrate flows
    at the pump's minimum."""
    base = dict(read_mode="steady_flow", Q_read=1.0, Q_load=3.25, t_load=39.0, C_conj=10.0, V_conj=100.0,
                Q_conj=50.0, t_conj_stop=0.0, t_wash1=1.5, t_wash2=2.0, t_fill=1.5, t_wait=60.0, t_read=240.0)
    base.update(kw)
    d = D.tier1(electrode, **base)
    d["ps_values"] = {S0: 3.0e-4}                       # 0.3 mM HQDP: about 3 Km, a third of the impurity current
    return d


def t1_printed_gold(**kw):
    d = t1("C21", **kw)
    d["electrode"] = dict(AU10)
    return d


def t2(**kw):
    """Tier 2 primary: 1e6 streptavidin beads of 2.8 um packed in a fritted capillary whose tip sits in the inlet
    bore just above a printed carbon electrode; stopped accumulation, then the plug is swept over the electrode."""
    base = dict(d_p=2.8e-6, V_bed_uL=0.019, column_id=200e-6, bed_factor_key=MB, retainer_area=5e-6, bore_wall=False,
                V_dead_uL=0.1, Q_load=3.5, t_load=36.0, t_acc=420.0, Q_read=5.0, t_read=90.0)
    base.update(kw)
    return D.tier2(**base)


TRANSFER = dict(efficiency_key="ma.design_levers.immune_complex_transfer_efficiency",
                nsb_factor_key="ma.design_levers.immune_complex_transfer_nsb_factor")


def t3(transfer=True, **kw):
    """Tier 3 primary: the tier 2 bed behind valves plus an immune-complex transfer to a second, clean bed, which
    is the bed that is read.  The transfer enters with the bounded magnitudes of docs/05 (lever L4)."""
    base = dict(Q_load=4.5, t_load=29.0, t_extra=8.0, t_acc=420.0, t_wash2=2.0)
    base.update(kw)
    d = t2(**base)
    d["tier"] = 3
    if transfer:
        d["transfer"] = dict(TRANSFER)
    return d


# ---- scenarios (parameter-set modifiers) -------------------------------------------------------------------
def lv(ps, name):
    return float(ps.params[f"ma.design_levers.{name}"].value)


def scale(ps, key, f):
    p = ps.params[key]
    return L.with_bounds(ps, key, value=p.value * f, low=p.low * f, high=p.high * f)


def L6(ps):   # detection reagent screened to a half-life of at least 1 h
    return L.with_bounds(ps, "chem.antibodies.koff_detection", value=1.0e-4, low=3.0e-6, high=1.9e-4)


def L7(ps):   # substrate lot purified or selected: free hydroquinone 1e-6
    return L.pin(ps, **{IMP: 1e-6})


def L3(ps):   # F(ab')2 or Fab' conjugate
    return scale(ps, LF, lv(ps, "fab_conjugate_nsb_factor"))


def L5(ps):   # reference channel (tier 3 only)
    return scale(ps, "chem.nsb.blank_CV_analog_electrochemical",
                 (2 * (1 - lv(ps, "nsb_reference_channel_correlation"))) ** 0.5)


def S1(ps):   # non-specific binding at the rate the model assumed before its audit (x25)
    return L.with_bounds(ps, LF, value=1.0, low=0.3, high=3.0)


def S4a(ps):  # substrate lot with 1e-3 free hydroquinone
    return L.pin(ps, **{IMP: 1e-3})


def C1(ps):   # human IgG contamination of blanks up to 1 pg/mL equivalent
    return L.with_bounds(ps, "ma.nsb.blank_igg_contamination_equivalent", high=1e-12 / 1.5e5 * 1e3)


def chain(*fns):
    def f(ps):
        for fn in fns:
            ps = fn(ps)
        return ps
    return f


SCENARIOS = [("as specified", lambda ps: ps),
             ("detection reagent and substrate lot pass screening (L6 + L7)", chain(L6, L7)),
             ("F(ab')2 conjugate (L3)", L3),
             ("L3 + L6 + L7", chain(L3, L6, L7)),
             ("non-specific binding x25 (S1)", S1),
             ("free hydroquinone 1e-3 in the substrate (S4a)", S4a),
             ("blank contamination up to 1 pg/mL (C1)", C1)]


# ---- evaluation ---------------------------------------------------------------------------------------------
def run(design, ps, n, evaluate=None):
    evaluate = evaluate or (tk.evaluate_planar if design["tier"] == 1 else tk.evaluate_bed)
    if design.get("ps_values"):
        ps = ps.with_values(design["ps_values"])
    s = tk.monte_carlo(evaluate, design, ps, n=n)
    nom = s["_nominal"]
    dg = nom.diagnostics
    g = lambda k: float(np.asarray(dg[k]).reshape(-1)[0]) if k in dg else None
    keep = {k: v for k, v in s.items() if not k.startswith("_")}
    keep["diagnostics"] = {k: g(k) for k in (
        "capture_fraction", "N_captured_at_1pg", "enzymes_on_we_at_1pg", "enzymes_at_1pg", "f_label", "ret_label",
        "ret_capture", "exposure_nM_min", "N_nsb_we", "N_nsb_floor", "N_nsb_lid", "N_nsb_bed", "N_nsb_extra",
        "collected_floor", "collected_lid", "mean_current_at_1pg_A", "mean_blank_current_A", "signal_at_1pg_C",
        "blank_equivalent_pgml", "noise_rms_A", "loop_transfer", "n_flush", "cell_conversion", "eluted", "k_m",
        "k_r", "bed_area_m2", "bed_dp_Pa", "V_acc_uL", "sensor_cv")}
    tot = sum(np.asarray(v, float) for v in nom.variance_terms.values())
    keep["variance_fractions_nominal"] = {k: float(np.asarray(v, float) / tot) for k, v in nom.variance_terms.items()}
    keep["steps"] = [(a, float(b), bool(c)) for a, b, c in design["steps"]]
    return keep, s


def fmt(x, nd=2):
    if x is None:
        return "-"
    if not np.isfinite(x) or x > 1e29:
        return "inf"
    return f"{x:.{nd}g}"


def row(label, k):
    return (f"| {label} | {fmt(k['lod_nominal'])} | {fmt(k['lod_median'])} [{fmt(k['lod_p05'])}-{fmt(k['lod_p95'])}] | "
            f"{k['p_lod_le_target']:.2f} | {k['p_lod_le_10']:.2f} | {fmt(k['uloq_nominal'])} | "
            f"{k['limiting_term_nominal']} / {k['limiting_term_mc_mode']} ({k['limiting_term_mc_share']:.2f}) | "
            f"{k['time_to_result_min']:.1f} |")


HEAD = ("| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | ULOQ nominal | "
        "limiting term nominal / most frequent in Monte Carlo (share) | min to result |\n|---|---|---|---|---|---|---|---|")


def sensitivity(design, ps, top=8):
    evaluate = tk.evaluate_planar if design["tier"] == 1 else tk.evaluate_bed
    if design.get("ps_values"):
        ps = ps.with_values(design["ps_values"])
    base, rows = tk.one_at_a_time(evaluate, design, ps)
    return base, rows[:top]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--quick", action="store_true", help="primaries and scenarios only")
    args = ap.parse_args(argv)
    warnings.simplefilter("ignore")
    ps0 = tk.load_params()
    n = args.n
    out, md = {}, []

    def table(title, cases, note=""):
        md.append(f"\n## {title}\n")
        if note:
            md.append(note + "\n")
        md.append(HEAD)
        for label, design, mod in cases:
            k, _s = run(design, mod(ps0), n)
            out.setdefault(title, {})[label] = k
            md.append(row(label, k))
            print(md[-1], flush=True)

    prim = [("Tier 1: thin-film gold electrode, capture on the electrode, read under 1 uL/min substrate flow", t1()),
            ("Tier 2: capillary micro-bed above a printed carbon electrode, stopped accumulation, swept read", t2()),
            ("Tier 3: tier 2 bed behind valves + immune-complex transfer to a second bed", t3())]
    ident = lambda ps: ps
    table("1. The three implementations, as specified",
          [(lab, d, ident) for lab, d in prim],
          f"Monte Carlo n = {n}, seed 20261111. Tier 3 carries the immune-complex transfer at the bounded, UNVERIFIED "
          "magnitudes of ma.design_levers (non-specific label x0.1 [0.01-0.5], specific x0.7 [0.4-0.9]), sampled.")

    for lab, d in prim:
        cases = [(name, d, fn) for name, fn in SCENARIOS]
        if d["tier"] == 3:
            cases.insert(1, ("with a reference channel as well (L5)", d, L5))
            cases.append(("transfer does not work (same timing, no transfer)", t3(transfer=False), ident))
        table(f"2. Scenarios - {lab}", cases)

    if not args.quick:
        # ---- tier 1 alternatives and hardware scenarios ----
        table("3. Tier 1 - alternatives and hardware scenarios", [
            ("primary (gap 0.16 mm)", t1(), lambda ps: ps),
            ("gap 0.10 mm", t1(h=0.10e-3), lambda ps: ps),
            ("gap 0.30 mm", t1(h=0.30e-3), lambda ps: ps),
            ("pump minimum is 10 uL/min: read at 10 uL/min", t1(Q_read=10.0), lambda ps: ps),
            ("flow can be stopped: stopped read, 30 s wait + 120 s", t1(read_mode="steady", t_wait=30.0, t_read=120.0),
             lambda ps: ps),
            ("1 mM substrate instead of 0.3 mM", {**t1(), "ps_values": {S0: 1.0e-3}}, lambda ps: ps),
            ("no pre-read on the electrode", t1(preread=False), lambda ps: ps),
            ("conjugate 3 nM for 5 min + 3 min stop, load 36 min", t1(C_conj=3.0, Q_conj=20.0, t_conj_stop=3.0,
                                                                    t_load=36.0, Q_load=3.5), lambda ps: ps),
            ("printed gold strip (AU10) in the SPE cell, same chemistry", t1_printed_gold(), lambda ps: ps),
            ("printed carbon strip (C21), adsorbed streptavidin", t1("C21"), lambda ps: ps),
            ("printed carbon strip, SPE cell gap 0.10 mm", t1("C21", h=0.10e-3), lambda ps: ps),
            ("printed carbon strip, SPE cell gap 0.50 mm", t1("C21", h=0.50e-3), lambda ps: ps),
            ("thin-film gold, chemical redox cycling in the stopped cell (UNVERIFIED on gold)",
             t1(read_mode="cycling", t_wait=60.0, t_read=240.0), lambda ps: ps),
        ])
        # ---- tier 2 alternatives and hardware scenarios ----
        table("4. Tier 2 - alternatives and hardware scenarios", [
            ("primary (SPE cell gap 0.20 mm)", t2(), lambda ps: ps),
            ("SPE cell gap 0.10 mm", t2(h=0.10e-3), lambda ps: ps),
            ("SPE cell gap 0.50 mm", t2(h=0.50e-3), lambda ps: ps),
            ("flow cannot be stopped: continuous read at 1 uL/min",
             t2(read_mode="continuous", Q_read=1.0, t_acc=0.0, t_read=300.0, t_load=40.0, Q_load=3.2), lambda ps: ps),
            ("flow cannot be stopped and pump minimum is 10 uL/min",
             t2(read_mode="continuous", Q_read=10.0, t_acc=0.0, t_read=300.0, t_load=40.0, Q_load=3.2), lambda ps: ps),
            ("half the beads (5e5)", t2(V_bed_uL=0.0095), lambda ps: ps),
            ("twice the beads (2e6)", t2(V_bed_uL=0.038), lambda ps: ps),
            ("bed in a fitting on the inlet port (bore wall in the path)",
             t2(column_id=0.5e-3, bore_wall=True, V_dead_uL=None, retainer_area=1e-6), lambda ps: ps),
            ("20 um polystyrene streptavidin beads, 0.15 uL, on the port, 5 mm2 retainer",
             D.tier2(Q_load=3.5, t_load=36.0, t_acc=420.0), lambda ps: ps),
            ("retainer (frit or screen) wetted area 1 mm2 instead of 5 mm2", t2(retainer_area=1e-6), lambda ps: ps),
            ("retainer wetted area 20 mm2 (0.5 mm silicate frit)", t2(retainer_area=20e-6), lambda ps: ps),
            ("conjugate 10 nM for 2 min", t2(C_conj=10.0, Q_conj=50.0), lambda ps: ps),
            ("short accumulation of 30 s (range read)", t2(t_acc=30.0), lambda ps: ps),
            ("parked read instead of swept", t2(read_mode="parked", t_read=120.0), lambda ps: ps),
            ("thin-film gold cell as detector", t2(electrode="SE1"), lambda ps: ps),
            ("accumulation 15 min, load 28 min", t2(t_acc=900.0, t_load=28.0, Q_load=4.6), lambda ps: ps),
        ])
        # ---- tier 3 alternatives ----
        table("5. Tier 3 - alternatives", [
            ("primary (with transfer)", t3(), ident),
            ("transfer + F(ab')2 conjugate + screened reagents (L3 + L6 + L7)", t3(), chain(L3, L6, L7)),
            ("the same with a reference channel (L5)", t3(), chain(L3, L5, L6, L7)),
            ("valves only: tier 2 chemistry with an isolated bed (no transfer)",
             t3(transfer=False, t_extra=0.0, t_load=36.0, Q_load=3.5), ident),
            ("transfer at its pessimistic bounds (non-specific x0.5, specific x0.4)", t3(),
             lambda ps: L.pin(ps, **{"ma.design_levers.immune_complex_transfer_nsb_factor": 0.5,
                                     "ma.design_levers.immune_complex_transfer_efficiency": 0.4})),
            ("transfer at its optimistic bounds (non-specific x0.01, specific x0.9)", t3(),
             lambda ps: L.pin(ps, **{"ma.design_levers.immune_complex_transfer_nsb_factor": 0.01,
                                     "ma.design_levers.immune_complex_transfer_efficiency": 0.9})),
            ("accumulation 12 min instead of 7 (bed isolated by the valve), load 24 min",
             t3(t_acc=720.0, t_load=24.0, Q_load=5.4), ident),
        ])

    # ---- sensitivities of the primaries ----
    md.append("\n## 6. One-at-a-time sensitivity of the three implementations\n")
    md.append("LOD (pg/mL) with one parameter at its low and at its high bound, all others at their best estimate; "
              "the eight largest swings.\n")
    for lab, d in prim:
        psx = ps0
        base, rows = sensitivity(d, psx)
        md.append(f"\n**{lab}** (nominal {fmt(base)} pg/mL)\n\n| Parameter | value [low-high] | LOD at low | LOD at high |"
                  "\n|---|---|---|---|")
        out.setdefault("sensitivity", {})[lab] = []
        for key, lo, hi in rows:
            prm = psx.params[key]
            md.append(f"| `{key}` | {prm.value:g} [{prm.low:g}-{prm.high:g}] {prm.unit} | {fmt(lo)} | {fmt(hi)} |")
            out["sensitivity"][lab].append(dict(key=key, value=prm.value, low=prm.low, high=prm.high, unit=prm.unit,
                                                lod_low=lo, lod_high=hi))

    # ---- step tables ----
    md.append("\n## 7. Step tables used for the timing\n")
    for lab, d in prim:
        total, steps = tk.timing(d)
        md.append(f"\n**{lab}** - {total:.1f} min from Inject Start to result\n\n| Step | min | counts |\n|---|---|---|")
        for name, m, c in steps:
            md.append(f"| {name} | {m:.1f} | {'yes' if c else 'no (before injection)'} |")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "tiers.md").write_text("# Three-tier round: model results (scripts/tier_round/run_tiers.py)\n"
                                  + "\n".join(md) + "\n")
    (OUT / "tiers.json").write_text(json.dumps(out, indent=1, default=float))
    print("written", OUT / "tiers.md")


if __name__ == "__main__":
    main()
