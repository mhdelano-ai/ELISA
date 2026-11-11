"""Analysis entry point: `python -m elisa_auto.analyze <folder> [--report]`.

Scans a folder of bench results and prints the quantities the gates of docs/06 ask for, with the verdict against
config/gates.yaml. Recognised inputs (anywhere below the folder):
  * automated runs written by the sequencer: <run>/result.json + <run>/metadata.json
    (metadata.sample: {'type': 'blank'|'standard'|'control', 'conc_pgml': x, 'order': k})
  * the CSV templates of automation/templates/: u1_nsb.csv, u3_free_hq.csv, dissociation.csv, bli.csv,
    blanks_calibration.csv, detection_on_capture.csv, carryover.csv, recovery.csv
All calculations are the functions of stats.py (the validation protocol's definitions, docs/06 s7.4).
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

from . import gates as G
from . import stats as S


def _rows(p: Path) -> list[dict]:
    with open(p, newline="", encoding="utf-8") as f:
        return [{k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in r.items()}
                for r in csv.DictReader(f) if any((v or "").strip() for v in r.values())]


def _f(x, default=float("nan")):
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def _find(folder: Path, name: str) -> list[Path]:
    return sorted(folder.rglob(name))


# ---- automated runs -----------------------------------------------------------------------------------------
def collect_runs(folder: Path, invalid: list | None = None) -> list[dict]:
    """Completed, VALID automated runs. Runs flagged invalid by the fault latch (docs/08 S12) are excluded and, if
    a list is passed, appended to it as (run dir, reason)."""
    runs = []
    for r in _find(folder, "result.json"):
        m = r.parent / "metadata.json"
        res = json.loads(r.read_text())
        meta = json.loads(m.read_text()) if m.exists() else {}
        if meta.get("status", "ok") != "ok":
            continue
        if meta.get("valid", True) is False or res.get("valid", True) is False:
            if invalid is not None:
                invalid.append((str(r.parent), meta.get("invalid_reason") or res.get("invalid_reason")))
            continue
        smp = res.get("sample") or meta.get("sample") or {}
        runs.append({"dir": str(r.parent), "S": float(res["S_C"]), "type": smp.get("type"),
                     "conc": _f(smp.get("conc_pgml"), 0.0), "order": _f(smp.get("order"), len(runs)),
                     "ttr": res.get("time_to_result_min")})
    runs.sort(key=lambda x: x["order"])
    return runs


def blanks_calibration(rows: list[dict], label: str, gates: dict, out: list[str], gate_key="G3"):
    blanks = [r["S"] for r in rows if r["type"] == "blank"]
    stds = [(r["conc"], r["S"]) for r in rows if r["type"] == "standard"]
    if len(blanks) < 2 or len(stds) < 2:
        out.append(f"[{label}] need >= 2 blanks and >= 2 standards (have {len(blanks)}, {len(stds)})")
        return None
    c, s = zip(*stds)
    L = S.lod(blanks, c, s)
    b = L["blank"]
    out.append(f"[{label}] blanks n={b['n']} mean={b['mean']:.4g} SD={b['sd']:.3g} CV={b['cv']:.3f} "
               f"(SD 95% CI {b['sd_ci95'][0]:.3g}-{b['sd_ci95'][1]:.3g})")
    out.append(f"[{label}] low-range slope b={L['slope']:.4g} per pg/mL ({L['n_low_standards']} standards <= 10 pg/mL)")
    out.append(f"[{label}] LOD (mean + 3 SD, docs/00) = {L['lod']:.3g} pg/mL; free-intercept {L['lod_free_intercept']:.3g}; "
               f"with SD UCL95 {L['lod_ucl95']:.3g} pg/mL")
    out.append(f"[{label}] blank-equivalent (blank mean / slope, needs a zero-signal reference to be absolute): "
               f"{b['mean'] / L['slope']:.3g} pg/mL")
    g = gates.get(gate_key, {})
    if "lod_pgml" in g:
        out.append(f"[{label}] gate {gate_key} LOD: {G.verdict(g['lod_pgml'], L['lod'])}")
    if "blank_cv" in g:
        out.append(f"[{label}] gate {gate_key} CV_blank: {G.verdict(g['blank_cv'], b['cv'])}")
    try:
        p = S.fit_4pl(c, s)
        out.append(f"[{label}] 4PL a={p['a']:.4g} b={p['b']:.3g} c50={p['c50']:.4g} d={p['d']:.4g}; "
                   f"LOD via 4PL inverse = {S.inverse_4pl(L['threshold'], p):.3g} pg/mL")
    except Exception as e:  # 4PL is a cross-check only
        out.append(f"[{label}] 4PL fit not available ({type(e).__name__})")
    for lev, d in S.cv_by_level(c, s).items():
        out.append(f"[{label}]   level {lev:g} pg/mL: n={d['n']} mean={d['mean']:.4g} CV={d['cv']:.3f}")
    return L


CHALLENGE_PGML = 10000.0   # carry-over challenge level (docs/06 s7.6, revised after the final review, S6)


def carryover_from_sequence(rows: list[dict], out: list[str], gates: dict, top: float = 1000.0,
                            slope: float | None = None):
    """H -> B1 -> B2 triplets. Standards at >= 10 ng/mL are the S6 challenge: evaluated through the low-range slope
    against the nominal concentration (their own signal is above the calibrated range). Standards at 1000 pg/mL
    are still reported with the signal ratio, but 1e-4 x 1000 pg/mL = 0.1 pg/mL is below what that test resolves."""
    for lo, hi in ((top, CHALLENGE_PGML), (CHALLENGE_PGML, float("inf"))):
        H, B1, B2, C = [], [], [], []
        for i, r in enumerate(rows):
            if r["type"] == "standard" and lo <= r["conc"] < hi and i + 2 < len(rows):
                if rows[i + 1]["type"] == "blank" and rows[i + 2]["type"] == "blank":
                    H.append(r["S"]); B1.append(rows[i + 1]["S"]); B2.append(rows[i + 2]["S"]); C.append(r["conc"])
        if not H:
            continue
        if lo >= CHALLENGE_PGML and slope:
            co = S.carryover_challenge(B1, B2, slope, float(np.mean(C)))
            out.append(f"[runs] carry-over after a {np.mean(C):g} pg/mL challenge (n={len(H)}): {co['carryover']:.2e} "
                       f"(B1 excess {co['excess_pgml']:.3g} pg/mL) -> {G.verdict(gates['G3']['carryover'], co['carryover'])}")
        elif lo < CHALLENGE_PGML:
            co = S.carryover(H, B1, B2)
            out.append(f"[runs] carry-over after {lo:g} pg/mL (n={len(H)}): {co['carryover']:.2e} -> "
                       f"{G.verdict(gates['G3']['carryover'], co['carryover'])} (indicative only: at 1e-4 the B1 "
                       f"excess is {1e-4 * float(np.mean(C)):.2g} pg/mL; the criterion is tested with a "
                       f"{CHALLENGE_PGML:g} pg/mL challenge, docs/06 s7.6)")


# ---- Stage-1 templates ---------------------------------------------------------------------------------------
def u1(p: Path, gates: dict, out: list[str]):
    rows = _rows(p)
    std = [(_f(r["molecules"]), _f(r["signal"])) for r in rows if r.get("kind") == "standard"]
    bb = [_f(r["signal"]) for r in rows if r.get("kind") == "bead_blank"]
    smp = [r for r in rows if r.get("kind") == "sample"]
    if len(std) < 2 or not smp:
        out.append(f"[U1] {p}: need standard rows and sample rows")
        return
    fit = S.linear_fit(*zip(*std))
    bg = float(np.mean(bb)) if bb else fit["a"]
    g = gates["G1"]
    by_conj = {}
    for r in smp:
        n_alp = (_f(r["signal"]) - bg) / fit["b"]
        lf = S.label_factor(n_alp, _f(r["n_beads"]), _f(r["conc_nM"]), _f(r["time_min"]))
        by_conj.setdefault(r.get("conjugate", "?"), []).append({**r, "n_alp": n_alp, **lf})
    factors_at_design = {}
    for conj, lst in by_conj.items():
        std_wash = [x for x in lst if x.get("wash", "standard") in ("standard", "")]
        fac = [x["label_factor"] for x in std_wash if x["label_factor"] > 0]
        if not fac:
            continue
        gm = float(math.exp(np.mean(np.log(fac))))
        factors_at_design[conj] = gm
        out.append(f"[U1] {conj}: label factor (geometric mean of {len(fac)} standard-wash points) = {gm:.3g} "
                   f"[{min(fac):.3g}-{max(fac):.3g}] -> {G.verdict(g['label_factor'], gm)}")
        # design cell (0.3 nM x 30 min, standard wash): the value to enter at G1a/G1 (docs/08 W2: if NSB is not
        # linear in exposure the all-points mean differs from it)
        cell = [x["label_factor"] for x in std_wash if abs(_f(x["conc_nM"]) - 0.3) < 1e-9
                and abs(_f(x["time_min"]) - 30) < 1e-9 and x["label_factor"] > 0]
        if cell:
            gc = float(math.exp(np.mean(np.log(cell))))
            factors_at_design[conj] = gc
            out.append(f"[U1] {conj}: label factor at the DESIGN CELL 0.3 nM x 30 min (n={len(cell)}) = {gc:.3g} "
                       f"-> {G.verdict(g['label_factor'], gc)}; enter this value in measured_values.yaml "
                       "(the G1 rule is on model P, docs/06 s4.11)")
        pos = [x for x in std_wash if x["n_alp"] > 0]
        if len({x['exposure_mol_s_m3'] for x in pos}) >= 3:
            pl = S.power_law_fit([x["exposure_mol_s_m3"] for x in pos], [x["n_alp"] / x["area_m2"] for x in pos])
            out.append(f"[U1] {conj}: linearity beta = {pl['beta']:.3f} (95% CI {pl['beta_ci95'][0]:.3f}-"
                       f"{pl['beta_ci95'][1]:.3f}) -> {G.verdict(g['nsb_linearity_beta'], pl['beta'])}")
        strg = [x["n_alp"] for x in lst if x.get("wash") == "stringent"]
        ref = [x["n_alp"] for x in std_wash if abs(_f(x["conc_nM"]) - 1.0) < 1e-9 and abs(_f(x["time_min"]) - 30) < 1e-9]
        if strg and ref:
            frac = 1 - float(np.mean(strg)) / float(np.mean(ref))
            out.append(f"[U1] {conj}: fraction removed by stringent wash = {frac:.2f} -> "
                       f"{'ADD STRINGENT WASH' if frac >= g['wash_removed_frac']['add_wash_min'] else 'no wash step needed'}"
                       f" ({g['wash_removed_frac']['source']})")
    fmt_of = {r.get("conjugate"): r.get("format") for r in smp}
    fab = [c for c, f in fmt_of.items() if f == "fab2" and c in factors_at_design]
    igg = [c for c, f in fmt_of.items() if f == "igg" and c in factors_at_design]
    if fab and igg:
        ratio = factors_at_design[fab[0]] / factors_at_design[igg[0]]
        out.append(f"[U1] F(ab')2/IgG NSB ratio (lever L3, ma.design_levers.fab_conjugate_nsb_factor) = {ratio:.2f}")


def u3(p: Path, gates: dict, out: list[str]):
    rows = _rows(p)
    g = gates["G1"]
    sa = [r for r in rows if r.get("kind") == "std_add"]
    by_c = {}
    for r in sa:
        by_c.setdefault(_f(r["hqdp_mM"]), []).append((_f(r["added_nM"]), _f(r["signal"])))
    slope_at = {}
    for c, pts in sorted(by_c.items()):
        sa_res = S.standard_addition(*zip(*pts))
        f_free = S.free_hq_fraction(sa_res["x0_nM"], c)
        slope_at[c] = sa_res["slope"]
        out.append(f"[U3] HQDP {c:g} mM: free HQ = {sa_res['x0_nM']:.3g} nM -> {f_free:.2e} mol/mol -> "
                   f"{G.verdict(g['free_hq_mol_per_mol'], f_free)}")
    stab = [r for r in rows if r.get("kind") == "hq_stability"]
    t_half_h = None
    if len(stab) >= 2:
        d = S.decay_half_life([_f(r["t_h"]) * 60 for r in stab], [_f(r["signal"]) for r in stab])
        t_half_h = d["t_half_min"] / 60
        out.append(f"[U3] HQ half-life in substrate = {t_half_h:.3g} h (ma.chemistries.alp_hqdp.product_half_life)")
    tc = [r for r in rows if r.get("kind") == "timecourse"]
    if len(tc) >= 3 and slope_at:
        c = _f(tc[0]["hqdp_mM"])
        k = slope_at.get(c) or next(iter(slope_at.values()))
        hq = [_f(r["signal"]) / k for r in tc]
        h = S.hydrolysis_rate([_f(r["t_h"]) for r in tc], hq, c, t_half_h or 2.0)
        out.append(f"[U3] hydrolysis k_h = {h['k_h_per_s']:.2e} 1/s (HQ t1/2 used {t_half_h or 2.0:.3g} h) -> "
                   f"{G.verdict(g['hydrolysis_per_s'], h['k_h_per_s'])}")


def dissociation(p: Path, gates: dict, out: list[str]):
    rows = _rows(p)
    d = S.decay_half_life([_f(r["t_min"]) for r in rows], [_f(r["signal"]) - _f(r.get("nsb_signal"), 0.0) for r in rows])
    out.append(f"[U2 bead] complex t1/2 on beads = {d['t_half_min']:.3g} min -> "
               f"{G.detection_t_half_verdict(gates['G1']['detection_t_half_min'], d['t_half_min'])} "
               f"(loss rate = capture + detection off-rates; a bound on each)")


def bli(p: Path, gates: dict, out: list[str]):
    g = gates["G1"]
    for r in _rows(p):
        kon, koff = _f(r["kon_M_s"]), _f(r["koff_s"])
        th = math.log(2) / koff / 60 if koff > 0 else float("inf")
        if r.get("role") == "capture":
            v = G.verdict(g["capture_t_half_min"], th)
        else:
            v = G.detection_t_half_verdict(g["detection_t_half_min"], th)
        out.append(f"[U2 BLI] {r.get('reagent')} ({r.get('role')}): kon={kon:.2e} M-1s-1 "
                   f"({G.verdict(g['kon_M_s'], kon)}), koff={koff:.2e} 1/s, t1/2={th:.3g} min -> {v}")


def detection_on_capture(p: Path, gates: dict, out: list[str]):
    rows = _rows(p)
    # The ratio must be formed on the conjugate-borne signal, not on raw signals: at the design point the bead
    # signal (~0.8 nM HQ) sits on a ~3 nM free-HQ background (docs/06 E1.4), which would pull a raw ratio towards 1
    # and pass the gate falsely. Rows with bead_type 'background' (no-conjugate beads or no-bead substrate blank,
    # same substrate, volume and time) are averaged and subtracted from both arms (added by the final review,
    # docs/08).
    bgv = [_f(r["signal"]) for r in rows if r.get("bead_type") in ("background", "bead_blank", "no_bead")]
    cap = np.array([_f(r["signal"]) for r in rows if r.get("bead_type") == "capture"])
    non = np.array([_f(r["signal"]) for r in rows if r.get("bead_type") == "nonimmune"])
    if cap.size < 2 or non.size < 2:
        return
    if bgv:
        bg = float(np.mean(bgv))
        cap, non = cap - bg, non - bg
    else:
        out.append("[E1.4] WARNING: no 'background' rows; ratio formed on raw signals is biased towards 1 "
                   "(add no-conjugate bead or no-bead substrate blanks)")
    if cap.mean() <= 0 or non.mean() <= 0:
        out.append("[E1.4] background-corrected signal <= 0 in one arm: not resolvable at this bead number "
                   "(repeat at 5e6 beads and 1 nM, docs/06 E1.4)")
        return
    lr = math.log(cap.mean() / non.mean())
    se = math.sqrt(cap.var(ddof=1) / cap.size / cap.mean() ** 2 + non.var(ddof=1) / non.size / non.mean() ** 2)
    R = math.exp(lr)
    out.append(f"[E1.4] detection-on-capture ratio R = {R:.2f} (95% CI {math.exp(lr - 1.96 * se):.2f}-"
               f"{math.exp(lr + 1.96 * se):.2f}; n={cap.size}/{non.size}) -> "
               f"{G.verdict(gates['G1']['detection_on_capture_ratio'], R)}")


def carryover_csv(p: Path, gates: dict, out: list[str]):
    rows = _rows(p)
    pick = lambda k: [_f(r["signal"]) for r in rows if r.get("role") == k]
    co = S.carryover(pick("H"), pick("B1"), pick("B2"))
    out.append(f"[carry-over] {co['carryover']:.2e} -> {G.verdict(gates['G3']['carryover'], co['carryover'])}")


def recovery(p: Path, gates: dict, out: list[str]):
    rows = _rows(p)
    a = [_f(r["signal"]) for r in rows if r.get("passed") == "yes"]
    b = [_f(r["signal"]) for r in rows if r.get("passed") == "no"]
    if a and b:
        rec = float(np.mean(a) / np.mean(b))
        out.append(f"[E1.10] SM-FL recovery = {rec:.2f} -> {G.verdict(gates['G1']['smfl_recovery'], rec)}")


HANDLERS = {"u1_nsb.csv": u1, "u3_free_hq.csv": u3, "dissociation.csv": dissociation, "bli.csv": bli,
            "detection_on_capture.csv": detection_on_capture, "carryover.csv": carryover_csv,
            "recovery.csv": recovery}


def analyze_folder(folder, gates_path=None) -> list[str]:
    folder = Path(folder)
    gates = G.load_gates(gates_path)
    out = [f"Analysis of {folder} (gates: {gates_path or G.DEFAULT_GATES})"]
    for name, fn in HANDLERS.items():
        for p in _find(folder, name):
            try:
                fn(p, gates, out)
            except Exception as e:
                out.append(f"[{name}] {p}: could not analyse ({type(e).__name__}: {e})")
    for p in _find(folder, "blanks_calibration.csv"):
        rows = [{"S": _f(r["signal"]), "type": r.get("sample_type"), "conc": _f(r.get("conc_pgml"), 0.0)}
                for r in _rows(p)]
        blanks_calibration(rows, f"manual {p.parent.name}", gates, out, gate_key="G2")
    invalid = []
    runs = collect_runs(folder, invalid)
    if invalid:
        out.append(f"[runs] {len(invalid)} run(s) EXCLUDED as invalid (fault latch set, no recovery cycle yet; "
                   f"docs/08 S12): " + "; ".join(f"{Path(d).name}: {why}" for d, why in invalid))
    for lp in _find(folder, "fault_latch.json"):
        st = json.loads(lp.read_text())
        out.append(f"[runs] fault latch {lp}: {'SET since run ' + str(st.get('since_run')) if st.get('set') else 'clear'}"
                   f" ({len(st.get('history', []))} events)")
    if runs:
        out.append(f"[runs] {len(runs)} completed automated runs")
        Lr = blanks_calibration(runs, "runs", gates, out, gate_key="G3")
        carryover_from_sequence(runs, out, gates, slope=Lr["slope"] if Lr else None)
        ttr = [r["ttr"] for r in runs if r["ttr"] is not None]
        if ttr:
            out.append(f"[runs] time to result max = {max(ttr):.2f} min -> "
                       f"{G.verdict(gates['G3']['time_to_result_min'], max(ttr))}")
    if len(out) == 1:
        out.append("no recognised result files found")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("folder")
    ap.add_argument("--gates", default=None, help="gates YAML (default automation/config/gates.yaml)")
    ap.add_argument("--report", action="store_true", help="also write analysis_report.md into the folder")
    a = ap.parse_args(argv)
    lines = analyze_folder(a.folder, a.gates)
    print("\n".join(lines))
    if a.report:
        Path(a.folder, "analysis_report.md").write_text("# Analysis report\n\n```\n" + "\n".join(lines) + "\n```\n")


if __name__ == "__main__":
    main()
