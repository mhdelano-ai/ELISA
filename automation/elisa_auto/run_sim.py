"""Run simulated cycles end to end: `python -m elisa_auto.run_sim [--cycle ...] [--samples ...] [--out ...]`.

Uses a virtual clock, simulated valves/SIA/magnet/Inject Start/Empower/potentiostat. Each sample's 'true' charge
comes from a toy assay response: Q = q_blank * (1 + cv_blank * z) + q_per_pg * C * (1 + 0.05 * z'), with defaults
taken from the model's nominal P-vial diagnostics (5.2 nC per pg/mL at 1 pg/mL; blank-equivalent ~0.96 pg/mL;
blank CV 10 %, chem.nsb.blank_CV_analog_electrochemical). It exercises timing, logging, signal extraction and the
LOD calculation — it is not a model prediction.
"""
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import numpy as np

from .analyze import analyze_folder
from .clock import SimClock
from .cycle import load_cycle
from .hardware import build_sim, load_hw
from .sequencer import Sequencer

CFG = Path(__file__).resolve().parents[1] / "config"


def parse_samples(spec: str) -> list[dict]:
    """'blank:5,1:3,10:3,1000:1,blank:2' -> ordered list of samples."""
    out = []
    for part in spec.split(","):
        what, n = part.split(":")
        for _ in range(int(n)):
            if what == "blank":
                out.append({"type": "blank", "conc_pgml": 0.0})
            else:
                out.append({"type": "standard", "conc_pgml": float(what)})
    for k, s in enumerate(out):
        s["order"] = k
        s["sample_id"] = f"S{k:03d}"
    return out


def simulate(cycle_path, samples, out_dir, hw_path=None, seed=20261111, q_blank=5.0e-9, q_per_pg=5.2e-9,
             cv_blank=0.10, carryover=1e-4):
    cycle = load_cycle(cycle_path)
    hw = load_hw(hw_path or CFG / "hardware_sim.yaml")
    clock = SimClock(0.0)
    dev = build_sim(clock, hw)
    rng = np.random.default_rng(seed)
    out_dir = Path(out_dir)
    results, prev_q = [], 0.0
    for s in samples:
        q = q_blank * (1 + cv_blank * rng.standard_normal()) + q_per_pg * s["conc_pgml"] * (1 + 0.05 * rng.standard_normal())
        q += carryover * prev_q
        prev_q = q
        dev.potentiostat.set_true_charge(q)
        dev.empower.plan_cycle(cycle, t_arm=clock.now())
        seq = Sequencer(cycle, dev, clock, out_dir / f"run_{s['order']:03d}_{s['sample_id']}",
                        metadata={"true_charge_C": q})
        results.append(seq.run(s))
    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description="simulated end-to-end cycles")
    ap.add_argument("--cycle", default=str(CFG / "cycle_primary.yaml"))
    ap.add_argument("--hw", default=None)
    ap.add_argument("--samples", default="blank:10,1:3,2:3,5:3,10:3,100:2,1000:1,blank:2,1000:1,blank:2")
    ap.add_argument("--out", default=None)
    ap.add_argument("--seed", type=int, default=20261111)
    a = ap.parse_args(argv)
    out = a.out or f"bench/sim_runs/{datetime.now():%Y%m%d_%H%M%S}"
    res = simulate(a.cycle, parse_samples(a.samples), out, a.hw, a.seed)
    n_ok = sum(r.status == "ok" for r in res)
    print(f"{n_ok}/{len(res)} simulated cycles completed; runs in {out}")
    print("\n".join(analyze_folder(out)))


if __name__ == "__main__":
    main()
