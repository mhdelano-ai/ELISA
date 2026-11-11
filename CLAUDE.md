# CLAUDE.md — project guide for Claude Code sessions

Automated electrochemical ELISA for **human IgG in buffer** on a Waters ACQUITY I-Class PLUS (BSM + SM-FL,
Empower with Toolkit licence) and a Gamry Reference 600+. Read `docs/00_project_brief.md` first; it is the
shared source of truth.

## Goal and success criteria (docs/00)
LOD ≤ 1 pg/mL (≈ 6.7 fM; mean blank + 3 SD of replicate blanks, through a calibration curve); calibration
≈ 1–1000 pg/mL; ≤ 100 µL **injected** per determination; ≤ 60 min injection to result; capture surface reusable
or automatically renewed; buffer matrix only; no manual step between loading the autosampler and the result.

## Fixed user decisions (docs/00, do not reopen without the user)
- Sample vials contain **sample only**: no pre-filled reagent vials, no reagent added by the end user.
- The 100 µL limit is the injected volume (full-loop injection, 2× overfill, ~200 µL drawn, is accepted).
- One custom Python orchestration layer drives the Gamry and the added hardware; Empower runs the Waters stack.
- A second potentiostat channel is acceptable. Budget for purchases/custom parts is not the constraint.

## Sourcing rule
Every number carries a source (DOI/URL/vendor document) and a confidence. Anything not checked in the session is
marked **UNVERIFIED**. Never invent a citation, part number, price or vendor API call.

## Repository layout
- `docs/00–05` — brief, literature, hardware, model, audit, design decision (in silico phase; do not edit).
- `docs/06_bench_plan.md` — staged bench plan with gates; `docs/07_bill_of_materials.md` — BOM by stage.
- `params/*.yaml` — model parameters (`chem.*`, `hw.*`, `ma.*`; schema in the file headers).
- `src/elisa_sim/` — simulation package; `tests/` — its tests; `scripts/` — design scripts (`design_lib.py`).
- `results/`, `results/design/` — model outputs.
- `automation/` — lab-PC orchestration skeleton (simulated devices, sequencer, data analysis, gate report,
  model feedback). See `automation/README.md`.
- `bench/` — **where bench results go** (create it; one sub-folder per experiment, layout in docs/06 §9).

## How to run
```bash
pip install -e .                       # model package
python -m pytest -q                    # model tests (64 passed at the end of the in silico phase)
python scripts/final_designs.py        # re-evaluate the final designs (see docs/05 §6 for every script)
pip install -e automation              # orchestration package (simulation works on any OS)
python -m pytest -q automation/tests   # automation tests (32 passed after the final review)
python -m elisa_auto.run_sim --cycle automation/config/cycle_primary.yaml   # simulated cycle, virtual clock
python -m elisa_auto.analyze bench/<folder>         # gate quantities from bench results
python -m elisa_auto.model_feedback bench/measured_values.yaml   # re-run the model with bench values
```
The Gamry worker must run in Gamry's own 32-bit Python 3.7 (ToolkitPy); the orchestrator in Python ≥ 3.10.

## Status (2026-11-11)
In silico phase complete pending final review. **Next: bench Stage 0 (instrument facts, ordering) and Stage 1
(U1 conjugate NSB on beads, U3 free hydroquinone in HQDP, U2 antibody off-rates)** — no flow hardware needed;
Gate G1 decides whether 1 pg/mL is reachable before any custom hardware is bought (docs/06 §2–3).

## Recording bench results
Put raw data and the filled CSV templates in `bench/<stage>_<experiment>_<date>/` (templates in
`automation/templates/`). Record measured model inputs in `bench/measured_values.yaml` (value, low, high,
source = experiment folder) — do not edit `params/chemistry.yaml` or `params/hardware.yaml`; accepted bench
values go into the `overrides` section of `params/model_assumptions.yaml` with the experiment as source.
