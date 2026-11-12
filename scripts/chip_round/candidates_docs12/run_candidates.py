#!/usr/bin/env python3
"""Nearest-model estimates for the docs/12 chip candidates. Runs ONLY in the scratchpad copy of the repo.

Every override is a design value or scenario on an EXISTING architecture (no physics added). See docs/12 s.8.
Usage: python run_candidates.py [--n 2000] [--only KEY]
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "elisa_copy"
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

import numpy as np                      # noqa: E402
import design_lib as L                  # noqa: E402
import final_designs as F               # noqa: E402
from elisa_sim.model import evaluate    # noqa: E402
from elisa_sim import transport as tr   # noqa: E402

STIR = "ma.capture.in_vial_unstirred_rate_factor"


def stir(dil):
    """chamber stirred-capture factor, same shape as final_designs (S13) but divided by dilution `dil`."""
    return lambda p: L.with_bounds(p, STIR, value=1.0 / dil, low=0.2 / dil, high=1.0 / dil)


def chain(*fns):
    def f(p):
        for g in fns:
            p = g(p)
        return p
    return f


def pin(**kv):
    return lambda p: p.with_values({k.replace("__", "."): v for k, v in kv.items()})


def pinkv(d):
    return lambda p: p.with_values(d)


def l6l7(p):
    name, fn, _ = F.scen("L6+L7")
    return fn(p)


def scen(lbl):
    return F.scen(lbl)[1]


ps0 = L.load_ps()
os_rec = json.load(open(L.OUT / "optimum_OS__baseline.json"))["design"]
fr_rec = json.load(open(L.OUT / "optimum_FRB__baseline.json"))["design"]
fc_rec = json.load(open(L.OUT / "optimum_FRC__baseline.json"))["design"]

# ---------------- reference: gen-1 primary as in final_designs (review variant) ----------------
REF = {k: (a, pm, f) for k, a, pm, f in F.designs(ps0, "review")}

# ---------------- A: magnetic bead-transfer multi-run cartridge (nearest: P-chamb) ----------------
os_opt = L.base_arch("OS").with_design(**os_rec)
A_design = {"ma.timing.in_vial_incubation": 30, "hw.timing.accumulation_time": 15,
            "hw.smfl.loop_flush_volumes_for_transfer": 6.6,   # 7-min block: collect + drain/rinse + drag (time);
            # convective bead transfer 0.96 kept (A: collect 0.95 x drag 0.95 = 0.90, with trap 0.9 -> model 0.86)
            "ma.timing.post_sample_wash": 1.5,                 # 1.5 loop volumes pushed into the chamber
            "hw.timing.substrate_fill": 0.5,                   # RC pre-filled in parallel (min bound)
            "ma.timing.bead_flush_and_clean": 2.0,             # RC drag-out + flush (min bound)
            "hw.timing.readout_time": 1.0}
A_arch = replace(os_opt.with_design(**A_design), detector="thin_layer", name="A-nearest")
A_clean = pinkv({"ma.nsb.surface_factor_tubing": 0.01})        # RC walls never see conjugate solution (L2 repr.)
A_preel = pinkv({"ma.chemistries.alp_hqdp.free_product_impurity": 1e-7})  # pre-electrolysis credit (low bound)
A_SCALE = 1.0 / 0.90                                           # 1.5 loop volumes -> 0.90 transfer (docs/09 s1.2)

# ---------------- B: indexed single-use fresh micro-bed cells (nearest: B-bed, thin layer) ----------------
B_design = dict(fr_rec)
B_design.update({"hw.reactors.packed_microbed_10uL.bed_volume": 0.1,
                 "hw.reactors.packed_microbed_10uL.bead_diameter": 10,
                 "ma.geometry.packed_bed_column_inner_diameter": 0.2,
                 "hw.timing.sample_load_flow": 6,              # recirculation 150 uL over 25 min -> Q_eq = V/t
                 "hw.smfl.loop_flush_volumes_for_transfer": 1.5,
                 "ma.geometry.reactor_connection_length": 0.002,   # 2 mm on-chip channel bed -> RC
                 "chem.antibodies.conc_detection_antibody_typical": 1e-9,
                 "ma.delivery.conjugate_injection_volume": 20,
                 "hw.timing.conjugate_stopped_flow_incubation": 3,
                 "hw.timing.accumulation_time": 15, "hw.timing.readout_time": 1, "ma.readout.sweep_flow": 10,
                 "hw.timing.regeneration_and_reequilibration": 1.0})   # index next cell + head flush
B_arch = replace(L.base_arch("FRB").with_design(**B_design), detector="thin_layer", name="B-nearest")
B_fresh0 = pinkv({"chem.regeneration.residual_label_carryover_fraction": 1e-6,
                 "chem.regeneration.activity_loss_per_cycle": 0.0,
                 "ma.chemistries.alp_hqdp.substrate_concentration": 3e-3})
B_fresh = B_fresh0
B_spe = lambda p: L.with_bounds(p, "ma.noise.electrode_sensitivity_cv_nonfouling", value=0.10, low=0.04, high=0.18)

# ---------------- C: permanent glass chip, regenerated bed + stopped IDA (nearest: C-bed-IDA / FRC) --------
fc_arch = L.base_arch("FRC").with_design(**fc_rec)
C_arch = fc_arch.with_design(**{"hw.timing.accumulation_time": 15})
C_prot = pinkv({"ma.nsb.surface_factor_chip": 0.01})           # IDA channel protected by side outlet (L2 repr.)
C_nonfoul = lambda p: L.with_bounds(L.with_bounds(p, "ma.noise.electrode_sensitivity_cv_fouling",
                                                  value=0.02, low=0.005, high=0.05),
                                    "ma.reuse.electrode_sensitivity_loss_per_cycle_fouling",
                                    value=0.001, low=0.0, high=0.005)
C_repack = pinkv({"chem.regeneration.residual_label_carryover_fraction": 1e-6,
                  "chem.regeneration.activity_loss_per_cycle": 0.0,
                  "hw.timing.regeneration_and_reequilibration": 3.0})

ident = lambda p: p
IMP = "ma.chemistries.alp_hqdp.free_product_impurity"
# pre-electrolysis: exhaustive oxidation of the fresh RC fill before beads arrive; residual = unelectrolysed
# volume fraction, ASSUMED 1 % (UNVERIFIED) -> impurity x 0.01 on value and bounds (still sampled)
def pre_el(p):
    if IMP in p.pinned:          # scenario pinned the impurity (S4a, L7): scale the pinned value
        v = float(np.asarray(p.values[IMP]).reshape(-1)[0])
        return p.with_values({IMP: v * 0.01})
    return L.with_bounds(p, IMP, value=1e-7, low=1e-9, high=1e-5)
hq3 = pinkv({"ma.chemistries.alp_hqdp.substrate_concentration": 3e-3})
l4 = L.l4_transfer
B_big = dict(B_design)
B_big.update({"hw.reactors.packed_microbed_10uL.bed_volume": 0.5,
              "hw.reactors.packed_microbed_10uL.bead_diameter": 50,
              "ma.geometry.packed_bed_column_inner_diameter": 0.5})
B_arch = replace(L.base_arch("FRB").with_design(**B_big), detector="thin_layer", name="B-nearest")
B_small = replace(L.base_arch("FRB").with_design(**B_design), detector="thin_layer", name="B-small")
bedcv = lambda p: L.with_bounds(p, "chem.nsb.blank_CV_analog_electrochemical", value=0.14, low=0.05, high=0.25)
C15 = C_arch
C_arch = fc_arch
RUNS = [
    ("REF P-chamb S0", REF["P-chamb"][0], REF["P-chamb"][1], REF["P-chamb"][2], "gen-1 primary"),
    ("REF P-chamb L6+L7", REF["P-chamb"][0], chain(l6l7, REF["P-chamb"][1]), REF["P-chamb"][2], ""),
    ("REF S-chamb S0", REF["S-chamb"][0], REF["S-chamb"][1], REF["S-chamb"][2], ""),
    ("A0 S0", A_arch, chain(stir(1.7), A_clean), A_SCALE, ""),
    ("A0 no clean zone", A_arch, stir(1.7), A_SCALE, "trap-wall factor as tubing"),
    ("A0 dil 2.2, 2 LV", A_arch, chain(stir(2.2), A_clean), 1 / 0.96, "gen-1 dilution"),
    ("A0 acc 10", A_arch.with_design(**{"hw.timing.accumulation_time": 10}), chain(stir(1.7), A_clean), A_SCALE, ""),
    ("A1 pre-el", A_arch, chain(stir(1.7), A_clean, pre_el), A_SCALE, ""),
    ("A1 pre-el HQDP 3 mM", A_arch, chain(stir(1.7), A_clean, pre_el, hq3), A_SCALE, ""),
    ("A0 L6+L7", A_arch, chain(l6l7, stir(1.7), A_clean), A_SCALE, ""),
    ("A1 L6+L7 pre-el 3 mM", A_arch, chain(l6l7, stir(1.7), A_clean, pre_el, hq3), A_SCALE, ""),
    ("A0 S4a", A_arch, chain(scen("S4a"), stir(1.7), A_clean), A_SCALE, ""),
    ("A1 S4a pre-el", A_arch, chain(scen("S4a"), stir(1.7), A_clean, pre_el), A_SCALE, "1e-3 x 0.01"),
    ("A0 S3b no clean zone", A_arch, chain(scen("S3b"), stir(1.7)), A_SCALE, ""),
    ("A0 C1", A_arch, chain(scen("C1"), stir(1.7), A_clean), A_SCALE, ""),
    ("A1 L4 pre-el 3 mM", A_arch, chain(l4, stir(1.7), A_clean, pre_el, hq3), A_SCALE, "outside model"),
    ("REF B-bed L6+L7", REF["B-bed"][0], chain(l6l7, REF["B-bed"][1]), REF["B-bed"][2], ""),
    ("REF B-bed S0", REF["B-bed"][0], REF["B-bed"][1], REF["B-bed"][2], "gen-1 backup"),
    ("B0 S0", B_arch, B_fresh, 1.0, ""),
    ("B0 SPE cv", B_arch, chain(B_fresh, B_spe), 1.0, ""),
    ("B0 bed CV", B_arch, chain(B_fresh, bedcv), 1.0, ""),
    ("B1 pre-el", B_arch, chain(B_fresh, pre_el), 1.0, ""),
    ("B0 L6+L7", B_arch, chain(l6l7, B_fresh), 1.0, ""),
    ("B1 L6+L7 pre-el", B_arch, chain(l6l7, B_fresh, pre_el), 1.0, ""),
    ("B0 bed factor 1", B_arch, chain(B_fresh, pinkv({"ma.nsb.surface_factor_packed_bed": 1.0})), 1.0, ""),
    ("B0 bed factor 10", B_arch, chain(B_fresh, pinkv({"ma.nsb.surface_factor_packed_bed": 10.0})), 1.0, ""),
    ("B0 small bed", B_small, B_fresh, 1.0, "0.1 uL / 10 um"),
    ("B0 S4a", B_arch, chain(scen("S4a"), B_fresh), 1.0, ""),
    ("B0 L4", B_arch, chain(l4, B_fresh), 1.0, "outside model"),
    ("REF FRC S0", fc_arch, ident, 1.0, "C-bed-IDA old optimum, review params"),
    ("C1 protected", C_arch, C_prot, 1.0, ""),
    ("C2 protected nonfouling", C_arch, chain(C_prot, C_nonfoul), 1.0, ""),
    ("C2 pre-el", C_arch, chain(C_prot, C_nonfoul, pre_el), 1.0, ""),
    ("C2 L6+L7", C_arch, chain(l6l7, C_prot, C_nonfoul), 1.0, ""),
    ("C2 acc15 3 mM", C15, chain(C_prot, C_nonfoul, hq3), 1.0, ""),
    ("C3 repack", C_arch, chain(C_prot, C_nonfoul, C_repack), 1.0, ""),
    ("C2 residual 1e-2", C_arch, chain(C_prot, C_nonfoul,
                                        pinkv({"chem.regeneration.residual_label_carryover_fraction": 1e-2})), 1.0, ""),
    ("C2 bed factor 10", C_arch, chain(C_prot, C_nonfoul, pinkv({"ma.nsb.surface_factor_packed_bed": 10.0})), 1.0, ""),
    ("C2 L4", C_arch, chain(l4, C_prot, C_nonfoul), 1.0, "outside model"),
]


def b_scale(arch, ps):
    """B: the model loads the loop at the (equivalent) 6 uL/min; the real push is 150 uL at 100 uL/min ->
    transfer 0.90 (docs/09 s1.2). Return model_transfer / 0.90 so LOD is scaled to the real transfer."""
    r = evaluate(arch, ps)
    return float(np.mean(r.diagnostics["loop_transfer"])) / 0.90, float(np.mean(r.diagnostics["loop_transfer"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    out = []
    for key, arch, pm, f, note in RUNS:
        if a.only and not key.startswith(a.only):
            continue
        ps = pm(ps0)
        extra = ""
        if key.startswith("B"):
            f, mt = b_scale(arch, ps)
            extra = f"model loop transfer {mt:.3f}; lod_scale {f:.3f}"
        why = L.constraint_violations(arch, ps)
        r = evaluate(arch, ps)
        s = L.mc(arch, ps, n=a.n, lod_scale=f)
        d = r.diagnostics
        vf = r.variance_fractions() if hasattr(r, "variance_fractions") else {}
        row = dict(key=key, nominal=s["lod_nominal"], median=s["lod_median"], p05=s["lod_p05"], p95=s["lod_p95"],
                   p_lod=s["p_lod_only"], p=s["p_success"], uloq=s["uloq_nominal"], t=s["time_to_result_min"],
                   flags="; ".join(why), note=note + (" " + extra if extra else ""),
                   enz1=float(np.mean(d["enzymes_at_1pg"])), nsb=float(np.mean(d["N_nsb"])),
                   bead_share=float(np.mean(d["bead_share_of_nsb"])) if np.size(d["bead_share_of_nsb"]) else 0.0,
                   capture=float(np.mean(d["capture_fraction_low"])), label=float(np.mean(d["label_fraction_low"])),
                   vacc=float(np.mean(d["accumulation_volume_uL"])), carry_top=float(np.mean(d["carryover_after_top_pgml"])),
                   nsb_area_mm2=float(np.mean(d["nsb_area_eff_m2"])) * 1e6, cap_area_mm2=float(np.mean(d["capture_area_m2"])) * 1e6,
                   steps=d["timeline_min"], vf={k: round(float(v), 3) for k, v in vf.items()})
        out.append(row)
        print(json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in row.items()}), flush=True)
    Path(__file__).with_name(f"candidates_out{a.only.replace(' ','_')}.json").write_text(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
