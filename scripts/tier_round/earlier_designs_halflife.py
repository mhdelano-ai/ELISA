#!/usr/bin/env python3
"""Effect of a 10 min hydroquinone half-life (review finding C5) on the earlier designs of docs/05.

  python scripts/tier_round/earlier_designs_halflife.py   ->  results/tier_round/earlier_designs_halflife.md

Runs the audited model (src/elisa_sim, via scripts/final_designs.py and design_lib.py; nothing is edited) for the
primary design of docs/05 (P-chamb) and its backup (B-bed), as specified, with the model's product half-life
(7200 s [1800-72000]) and with the one used in the tier round (600 s [120-7200]).  Monte Carlo n = 2000, seed
20261111, success criterion of docs/05 (LOD x max(1, 1000 / ULOQ) <= 1 pg/mL).
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import design_lib as L  # noqa: E402
import final_designs as F  # noqa: E402

HALF = "ma.chemistries.alp_hqdp.product_half_life"
OUT = ROOT / "results" / "tier_round" / "earlier_designs_halflife.md"


def main():
    warnings.simplefilter("ignore")
    ps0 = L.load_ps()
    rows = ["# Earlier designs of docs/05 with the hydroquinone half-life of the tier round",
            "",
            "Audited model (`src/elisa_sim`), designs of `scripts/final_designs.py` (variant after the final review), "
            "as specified (scenario S0), n = 2000, seed 20261111. P(success) is the criterion of docs/05.",
            "",
            "| Design | Half-life of hydroquinone | LOD nominal (pg/mL) | LOD median [5-95 %] | P(LOD <= 1) | P(success) |",
            "|---|---|---|---|---|---|"]
    for key, arch, pmod, f in F.designs(ps0):
        if key not in ("P-chamb", "B-bed"):
            continue
        for label, mod in (("7200 s [1800-72000] (model)", lambda p: p),
                           ("600 s [120-7200] (tier round)",
                            lambda p: L.with_bounds(p, HALF, value=600.0, low=120.0, high=7200.0))):
            s = F.summarise(arch, mod(pmod(ps0)), f, L.N_FINAL)
            rows.append(f"| {key} | {label} | {s['lod_nominal']:.3g} | {s['lod_median']:.3g} "
                        f"[{s['lod_p05']:.3g}-{s['lod_p95']:.3g}] | {s['p_lod_only']:.3f} | {s['p_success']:.3f} |")
            print(rows[-1], flush=True)
    OUT.write_text("\n".join(rows) + "\n")
    print("written", OUT)


if __name__ == "__main__":
    main()
