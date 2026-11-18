#!/usr/bin/env python3
"""Evaluate the three implementations of docs/30 with their scenarios, alternatives and sensitivities.

  python scripts/tier_round/run_tiers.py [--n 2000] [--quick]
writes results/tier_round/tiers.md (tables) and results/tier_round/tiers.json (all numbers).

All three tiers are evaluated with scripts/tier_round/tierkit.py (which reuses the parameters, kinetics, transport
and blank statistics of the audited model, src/elisa_sim).  Monte Carlo: n = 2000, seed 20261111.
The earlier valve-and-chamber design of docs/05 is not re-evaluated here; its numbers are in docs/08 section 10.

Revised after the review and after the second pass (docs/31).  One model parameter is given other bounds for this
round, without editing params/: the half-life of hydroquinone at pH 9.5 (600 s [120-7200] instead of 7200 s
[1800-72000]; finding C5).  The same half-life holds in the substrate reservoir (finding M2); the scenario "no
decay" restores the assumption of the audited model.
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
KCAT = "chem.enzymes.alp.kcat_conjugate_assay_conditions"
HALF = "ma.chemistries.alp_hqdp.product_half_life"
DECAY = "tr.detection.reservoir_background_decays"
REL = "tr.transfer.elution_efficiency"
TNSB = "ma.design_levers.immune_complex_transfer_nsb_factor"
MONO = "tr.detection.monolayer_collection_efficiency"
RATIO = "chem.antibodies.enzyme_to_antibody_ratio_ALP"


def base_params():
    ps = tk.load_params()
    return L.with_bounds(ps, HALF, value=600.0, low=120.0, high=7200.0)


# ---- the designs -----------------------------------------------------------------------------------------
def t1(electrode="AU10", s0=3.0e-4, **kw):
    """Tier 1: capture on a printed strip in the strip cell; the product is read at the electrode while substrate
    flows at 200 uL/min, between two reference windows at the same flow.  'AU10': printed gold with a biotin-OEG
    monolayer (lowest model LOD of the tier); 'C21': printed carbon with adsorbed streptavidin (no thiol chemistry;
    10 nM conjugate, because carbon is limited by non-specific label); 'SE1': thin-film gold chip in its own cell."""
    if electrode == "C21":
        kw.setdefault("site_key", "tr.capture.site_factor_adsorbed")
        kw.setdefault("C_conj", 10.0)
    d = D.tier1(electrode, **kw)
    d["ps_values"] = {S0: s0}                 # 0.3 mM HQDP: about 3 Km, a third of the impurity current of 1 mM
    return d


def t2(**kw):
    """Tier 2: 1e6 streptavidin beads of 2.8 um packed against a frit in a capillary whose tip sits in the inlet
    bore, 1 mm above a printed carbon electrode; stop, then sweep."""
    return D.tier2(**kw)


def t3(**kw):
    """Tier 3 with the transfer: two beds in the loops of two valves, immune-complex transfer from the capture bed
    to the read bed (three times the beads)."""
    return D.tier3(**kw)


def t3v(**kw):
    """Tier 3, first step: the capture bed in the loop of one valve, no transfer; the time the transfer would
    take goes into the load (36 min at 3.5 uL/min)."""
    kw.setdefault("t_load", 40.0)
    kw.setdefault("Q_load", 3.15)
    kw.setdefault("t_acc", 180.0)
    return D.tier3(transfer=False, **kw)


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


def L3(ps):   # credit for a F(ab')2 or Fab' conjugate
    return scale(ps, LF, lv(ps, "fab_conjugate_nsb_factor"))


def L5(ps):   # reference channel (tier 3 only)
    return scale(ps, "chem.nsb.blank_CV_analog_electrochemical",
                 (2 * (1 - lv(ps, "nsb_reference_channel_correlation"))) ** 0.5)


def S1(ps):   # non-specific binding at the rate the model assumed before its audit (x25)
    return L.with_bounds(ps, LF, value=1.0, low=0.3, high=3.0)


def NODECAY(ps):  # the oxidisable background of the working solution does not decay in the reservoir
    return L.pin(ps, **{DECAY: 0})


def S4a(ps):  # working substrate solution with 1e-3 oxidisable background that does not decay
    return NODECAY(L.pin(ps, **{IMP: 1e-3}))


def C1(ps):   # human IgG contamination of blanks up to 1 pg/mL equivalent
    return L.with_bounds(ps, "ma.nsb.blank_igg_contamination_equivalent", high=1e-12 / 1.5e5 * 1e3)


def P01(ps):  # only 1 % of the enzyme turnovers give a product the electrode oxidises (review finding C1)
    return scale(ps, KCAT, 0.01)


def P001(ps):  # 0.1 %: the upper end of the reviewer's estimate for hydroquinone per turnover
    return scale(ps, KCAT, 0.001)


def chain(*fns):
    def f(ps):
        for fn in fns:
            ps = fn(ps)
        return ps
    return f


SCENARIOS = [("as specified", lambda ps: ps),
             ("detection reagent and substrate lot pass screening (L6 + L7)", chain(L6, L7)),
             ("credit for the F(ab')2 conjugate (L3)", L3),
             ("L3 + L6 + L7", chain(L3, L6, L7)),
             ("non-specific binding x25 (S1)", S1),
             ("no decay in the reservoir: background 1e-5 of the substrate at the time of use", NODECAY),
             ("no decay and screened reagents (L6 + L7)", chain(NODECAY, L6, L7)),
             ("background 1e-3 of the substrate, no decay (S4a)", S4a),
             ("blank contamination up to 1 pg/mL", C1),
             ("only 1 % of the turnovers give an electroactive product (review C1)", P01),
             ("only 1 % of the turnovers electroactive, and no decay in the reservoir", chain(P01, NODECAY)),
             ("only 0.1 % of the turnovers give an electroactive product", P001)]


# ---- evaluation ---------------------------------------------------------------------------------------------
def run(design, ps, n):
    evaluate = tk.evaluate_planar if design["tier"] == 1 else tk.evaluate_bed
    if design.get("ps_values"):
        ps = ps.with_values(design["ps_values"])
    s = tk.monte_carlo(evaluate, design, ps, n=n)
    nom = s["_nominal"]
    dg = nom.diagnostics
    g = lambda k: float(np.asarray(dg[k]).reshape(-1)[0]) if k in dg and dg[k] is not None else None
    keep = {k: v for k, v in s.items() if not k.startswith("_")}
    keep["diagnostics"] = {k: g(k) for k in (
        "capture_fraction", "N_captured_at_1pg", "enzymes_on_we_at_1pg", "enzymes_at_1pg", "f_label", "ret_label",
        "ret_capture", "exposure_nM_min", "N_nsb_we", "N_nsb_floor", "N_nsb_lid", "N_up_bore", "N_up_line",
        "collected_upstream", "N_nsb_bed", "N_nsb_extra", "collected_floor", "collected_lid",
        "mean_current_at_1pg_A", "mean_blank_current_A", "signal_at_1pg_C", "blank_equivalent_pgml", "noise_rms_A",
        "loop_transfer", "n_flush", "cell_conversion", "eluted", "k_m", "k_r", "bed_area_m2", "bed_dp_Pa", "V_acc_uL",
        "sensor_cv", "transfer_efficiency", "Q_nsb_C", "Q_imp_C", "Q_hyd_C")}
    tot = sum(np.asarray(v, float) for v in nom.variance_terms.values())
    keep["variance_fractions_nominal"] = {k: float(np.asarray(v, float) / tot) for k, v in nom.variance_terms.items()}
    keep["steps"] = [(a, float(b), bool(c)) for a, b, c in design["steps"]]
    # highest concentration up to which the nominal calibration curve rises
    net, conc = np.asarray(nom.net_signal, float), np.asarray(nom.conc_pgml, float)
    rising = np.diff(net[1:]) > 0
    keep["monotonic_to_pgml"] = float(conc[1:][-1] if rising.all() else conc[1:][np.argmin(rising)])
    return keep, s


def fmt(x, nd=2):
    if x is None:
        return "-"
    if not np.isfinite(x) or x > 1e29:
        return "inf"
    return f"{x:.{nd}g}"


def row(label, k):
    return (f"| {label} | {fmt(k['lod_nominal'])} | {fmt(k['lod_median'])} [{fmt(k['lod_p05'])}-{fmt(k['lod_p95'])}] | "
            f"{k['p_lod_le_target']:.2f} | {k['p_lod_le_10']:.2f} | {fmt(k['uloq_nominal'])} / "
            f"{fmt(k['monotonic_to_pgml'])} | {k['limiting_term_nominal']} / {k['limiting_term_mc_mode']} "
            f"({k['limiting_term_mc_share']:.2f}) | {k['time_to_result_min']:.1f} |")


HEAD = ("| Case | LOD nominal (pg/mL) | LOD median [5-95 %] (pg/mL) | P(LOD <= 1) | P(LOD <= 10) | upper limit by the "
        "slope criterion / curve rises up to (pg/mL) | limiting term nominal / most frequent in Monte Carlo (share) | "
        "min to result |\n|---|---|---|---|---|---|---|---|")


def sensitivity(design, ps, top=12):
    evaluate = tk.evaluate_planar if design["tier"] == 1 else tk.evaluate_bed
    if design.get("ps_values"):
        ps = ps.with_values(design["ps_values"])
    base, rows = tk.one_at_a_time(evaluate, design, ps)
    return base, rows[:top], rows


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--quick", action="store_true", help="primaries and scenarios only")
    args = ap.parse_args(argv)
    warnings.simplefilter("ignore")
    ps0 = base_params()
    n = args.n
    out, md = {}, []
    ident = lambda ps: ps

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

    prim = [("Tier 1: capture on a printed gold strip, read at the electrode under fast substrate flow", t1()),
            ("Tier 2: capillary micro-bed above a printed carbon strip, stop and sweep", t2()),
            ("Tier 3: the capture bed in the loop of one valve", t3v()),
            ("Tier 3 with the immune-complex transfer to a second bed", t3())]
    table("1. The three implementations, as specified", [(lab, d, ident) for lab, d in prim],
          f"Monte Carlo n = {n}, seed 20261111. The transfer is carried as release (0.35 [0.05-0.74], UNVERIFIED) x "
          "re-capture on a read bed of three times the beads (bed equation with site depletion at the push flow) "
          "and non-specific label x0.1 [0.01-0.5] (ma.design_levers, UNVERIFIED).")

    for lab, d in prim:
        cases = [(name, d, fn) for name, fn in SCENARIOS]
        if d["tier"] == 3:
            cases.insert(1, ("with a reference channel as well (L5)", d, L5))
        table(f"2. Scenarios - {lab}", cases)

    if not args.quick:
        table("3. Tier 1 - alternatives and hardware cases", [
            ("primary: printed gold AU10, strip-cell gap 0.20 mm, read 60 s at 200 uL/min, 0.3 mM substrate, 20 nM "
             "conjugate", t1(), ident),
            ("printed carbon C21 with adsorbed streptavidin (same cell and read)", t1("C21"), ident),
            ("thin-film gold chip SE1 in the thin-film cell (same read)", t1("SE1"), ident),
            ("strip-cell gap 0.10 mm", t1(h=0.10e-3), ident),
            ("strip-cell gap 0.50 mm", t1(h=0.50e-3), ident),
            ("read at 80 uL/min (load 41 min)", t1(Q_read=80.0, t_load=41.0, Q_load=3.07), ident),
            ("read at 40 uL/min (load 36 min)", t1(Q_read=40.0, t_load=36.0, Q_load=3.5), ident),
            ("read at 300 uL/min", t1(Q_read=300.0), ident),
            ("read 120 s at 150 uL/min, 10 nM conjugate, load 42 min (operating point of Revision B)",
             t1(Q_read=150.0, t_read=120.0, C_conj=10.0, t_load=42.0, Q_load=3.0), ident),
            ("conjugate 10 nM", t1(C_conj=10.0), ident),
            ("conjugate 40 nM", t1(C_conj=40.0), ident),
            ("substrate 0.1 mM", t1(s0=1.0e-4), ident),
            ("substrate 1 mM", t1(s0=1.0e-3), ident),
            ("stopped read (needs a zero-flow row), 30 s wait + 120 s", t1(read_mode="steady", t_read=120.0,
                                                                              t_load=37.0, Q_load=3.4), ident),
            ("transfer line 0.127 mm x 20 cm instead of 0.05 mm x 15 cm", t1(line_area=np.pi * 127e-6 * 0.2), ident),
            ("no pre-read on the electrode", t1(preread=False), ident),
            ("stop-and-go loading: 13 portions of 10 uL held 190 s each (needs a zero-flow row)",
             t1(load_mode="stop_go", dwell_s=190.0, Q_load=50.0), ident),
            ("coated gold delivers 30 % of the transport-limited current",
             t1(), lambda ps: L.pin(ps, **{"tr.detection.monolayer_collection_efficiency": 0.3})),
            ("detection conjugate with 5 [2-10] enzymes per antibody (poly-enzyme label, UNVERIFIED reagent; "
             "binding and non-specific count per conjugate unchanged)",
             t1(), lambda ps: L.with_bounds(ps, "chem.antibodies.enzyme_to_antibody_ratio_ALP", value=5.0, low=2.0,
                                            high=10.0)),
            ("printed carbon C21, stopped read", t1("C21", read_mode="steady", t_read=120.0, t_load=37.0, Q_load=3.4),
             ident),
            ("reference windows in wash buffer pH 7.5: background step of 100 pA against the substrate buffer",
             t1(buffer_step_pA=100.0), ident),
            ("reference windows in wash buffer pH 7.5: background step of 300 pA", t1(buffer_step_pA=300.0), ident),
            ("substrate 1 mM, no decay in the reservoir", t1(s0=1.0e-3), NODECAY),
            ("printed carbon C21, no decay in the reservoir", t1("C21"), NODECAY),
            ("no pre-read on the electrode, no decay in the reservoir", t1(preread=False), NODECAY),
        ])
        table("4. Tier 2 - alternatives and hardware cases", [
            ("primary (strip-cell gap 0.20 mm)", t2(), ident),
            ("strip-cell gap 0.10 mm", t2(h=0.10e-3), ident),
            ("strip-cell gap 0.50 mm", t2(h=0.50e-3), ident),
            ("pump cannot stop: continuous read at 1 uL/min", t2(read_mode="continuous", Q_read=1.0, t_acc=0.0,
                                                                  t_read=300.0, t_load=41.0, Q_load=3.1), ident),
            ("pump cannot stop and cannot go below 10 uL/min", t2(read_mode="continuous", Q_read=10.0, t_acc=0.0,
                                                                    t_read=300.0, t_load=41.0, Q_load=3.1), ident),
            ("bed binds conjugate like beads washed in tubes (factor 1 instead of 3)", t2(bed_factor_key=MB), ident),
            ("retainer wetted area 1 mm2 instead of 5 mm2", t2(retainer_area=1e-6), ident),
            ("retainer wetted area 20 mm2 (0.5 mm silicate frit)", t2(retainer_area=20e-6), ident),
            ("no conjugate-exposed wall upstream of the bed (bound)", t2(capillary_above_bed_mm=0.0, line_area=0.0),
             ident),
            ("transfer line 0.127 mm x 20 cm", t2(line_area=np.pi * 127e-6 * 0.2), ident),
            ("transfer line 0.025 mm x 15 cm", t2(line_area=np.pi * 25e-6 * 0.15), ident),
            ("walls above the bed bind like blocked beads (tubing factor 1, e.g. a coated capillary)",
             t2(), lambda ps: L.pin(ps, **{"ma.nsb.surface_factor_tubing": 1.0})),
            ("bed in a fitting on the inlet port (whole bore between bed and electrode)", t2(bore_below_tip_mm=5.0),
             ident),
            ("half the beads (5e5)", t2(V_bed_uL=0.0095), ident),
            ("twice the beads (2e6)", t2(V_bed_uL=0.038), ident),
            ("stop 7 min instead of 5 (load 35 min)", t2(t_acc=420.0, t_load=35.0, Q_load=3.6), ident),
            ("stop 3 min instead of 5 (load 39 min)", t2(t_acc=180.0, t_load=39.0, Q_load=3.23), ident),
            ("stop 30 s", t2(t_acc=30.0), ident),
            ("parked read instead of swept", t2(read_mode="parked", t_read=120.0), ident),
            ("conjugate 10 nM", t2(C_conj=10.0), ident),
            ("conjugate 3 nM", t2(C_conj=3.0), ident),
            ("conjugate 3 nM, stop 3 min, load 39 min (lowest nominal)", t2(C_conj=3.0, t_acc=180.0, t_load=39.0,
                                                                          Q_load=3.23), ident),
            ("the same, only 1 % of the turnovers electroactive", t2(C_conj=3.0, t_acc=180.0, t_load=39.0, Q_load=3.23),
             P01),
        ])
        table("5. Tier 3 - alternatives", [
            ("one valve, no transfer (primary of tier 3)", t3v(), ident),
            ("one valve, accumulation 7 min instead of 3 (load 36 min)", t3v(t_acc=420.0, t_load=36.0, Q_load=3.5),
             ident),
            ("one valve, conjugate 10 nM", t3v(C_conj=10.0), ident),
            ("one valve, conjugate 3 nM", t3v(C_conj=3.0), ident),
            ("one valve, loop walls 30 mm2 instead of 10 mm2", t3v(line_area=30e-6), ident),
            ("transfer as specified (release 0.35 [0.05-0.74], read bed of three times the beads)", t3(), ident),
            ("transfer: release 0.7 in 5 min, as docs/05 assumed for its tube protocol", t3(),
             lambda ps: L.pin(ps, **{REL: 0.7})),
            ("transfer: release 0.74, non-specific x0.01 (optimistic bounds)", t3(),
             lambda ps: L.pin(ps, **{REL: 0.74, TNSB: 0.01})),
            ("transfer: release 0.05, non-specific x0.5 (pessimistic bounds)", t3(),
             lambda ps: L.pin(ps, **{REL: 0.05, TNSB: 0.5})),
            ("transfer with desthiobiotin and biotin, 5 min (release 0.1 [0.003-0.26])",
             t3(elution_key="tr.transfer.elution_efficiency_desthiobiotin"), ident),
            ("transfer, release 0.7, read bed the same size as the capture bed (sites/feed 1.2)",
             t3(bed2_factor=1.0), lambda ps: L.pin(ps, **{REL: 0.7})),
            ("transfer, release 0.7, same size, capture bed coated at the vendor's capacity (sites/feed 0.36)",
             t3(bed2_factor=1.0, coat=3.3), lambda ps: L.pin(ps, **{REL: 0.7})),
            ("transfer, screened reagents (L6 + L7)", t3(), chain(L6, L7)),
            ("transfer, release 0.7, screened reagents (L6 + L7)", t3(), chain(L6, L7, lambda ps: L.pin(ps, **{REL: 0.7}))),
            ("transfer + screened reagents + F(ab')2 credit (L3 + L6 + L7)", t3(), chain(L3, L6, L7)),
            ("the same with a reference channel (L5)", t3(), chain(L3, L5, L6, L7)),
        ])

    md.append("\n## 6. One-at-a-time sensitivity of the three implementations\n")
    md.append("LOD (pg/mL) with one parameter at its low and at its high bound, all others at their best estimate; "
              "the twelve largest swings.\n")
    for lab, d in prim:
        base, rows, allrows = sensitivity(d, ps0)
        md.append(f"\n**{lab}** (nominal {fmt(base)} pg/mL)\n\n| Parameter | value [low-high] | LOD at low | LOD at high |"
                  "\n|---|---|---|---|")
        for key, lo, hi in rows:
            prm = ps0.params[key]
            md.append(f"| `{key}` | {prm.value:g} [{prm.low:g}-{prm.high:g}] {prm.unit} | {fmt(lo)} | {fmt(hi)} |")
        out.setdefault("sensitivity", {})[lab] = [                      # every parameter, largest swing first
            dict(key=key, value=ps0.params[key].value, low=ps0.params[key].low, high=ps0.params[key].high,
                 unit=ps0.params[key].unit, lod_low=lo, lod_high=hi, base=base) for key, lo, hi in allrows]

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
