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
- Cartridge round (2026-11-11/12, docs/16 §2): second-generation cartridge after the gen-1 tubing rig; dock may
  contain anything; criteria unchanged; nearest-model estimates only (no model extension). A leads, B fallback,
  C′ kept alive. Pre-electrolysis is a gen-1 bench TEST only (E1.2b, informational). Reagents are dock-supplied
  (beads in a cooled agitated dock vial; conjugate and HQDP tanks on the card filled at insertion). Card ≤ ~14
  determinations with ≥ 3 min margin to 60 min. Carry-over 1×10⁻⁴ kept + mandatory cleaning cycle and blank check
  after any result > 100 pg/mL. M5a (read background, catalogue die, existing Gamry) approved before G1; everything
  else for the cartridge waits for G1 and E1.2b.

## Sourcing rule
Every number carries a source (DOI/URL/vendor document) and a confidence. Anything not checked in the session is
marked **UNVERIFIED**. Never invent a citation, part number, price or vendor API call.

## Repository layout
- `docs/00–05` — brief, literature, hardware, model, audit, design decision (in silico phase; do not edit; docs/05
  carries a few passages marked "(revised after final review)").
- `docs/08_final_review.md` — final review, corrections to earlier documents (§9), resolution of findings (§10).
- `docs/09–15` — cartridge round: requirements, literature, fabrication, candidates (corrections box), design A
  (Revision B), alternatives B and C′ (revised), review with resolution of findings (§7). Do not edit docs/09–12.
- `docs/16_chip_decision.md` — cartridge decision, authoritative comparison table, cartridge gates and kill criteria.
- `docs/17_session_record.md` — trail of the cartridge round: every question and answer, agent tasks, commits.
- `scripts/chip_round/` — the agents' working scripts and outputs behind docs/09–16 (record only; see its README).
- `docs/presentation/` — summary slide decks (in silico phase; cartridge round) as standalone HTML, sources, `build.py`.
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
python -m pytest -q                    # model tests (71 passed after the review findings were resolved)
python scripts/final_designs.py        # re-evaluate the final designs (see docs/05 §6 for every script)
python scripts/g1_decision_table.py    # the G1 decision table (docs/06 §4.11; ~8 min)
pip install -e automation              # orchestration package (simulation works on any OS)
python -m pytest -q automation/tests   # automation tests (50 passed after the review findings were resolved)
python -m elisa_auto.run_sim --cycle automation/config/cycle_primary.yaml   # simulated cycle, virtual clock
python -m elisa_auto.analyze bench/<folder>         # gate quantities from bench results
python -m elisa_auto.model_feedback bench/measured_values.yaml   # re-run the model with bench values
```
The Gamry worker must run in Gamry's own 32-bit Python 3.7 (ToolkitPy); the orchestrator in Python ≥ 3.10.

## Status (2026-11-12)
In silico phase complete; the final review's findings are resolved or listed as open in docs/08 §10. **Next:
bench Stage 0 (instrument facts, ordering) and Stage 1A (E1.1 readout, E1.2 U3 free HQ, E1.3 U1 conjugate NSB with
the reservoir-ageing arm; plus E1.2b HQDP pre-electrolysis "guard cell" test, weeks 5–7, informational, not a G1a/G1
input — no guard cell in the hardware until its result)** — no flow hardware needed. **G1a (week 5)** applies the G1 rule to U1 + U3; BLI/SPR and
NISTmAb are ordered only after it. **G1 rule (fixed before data, docs/06 §4.11, `gates.yaml` G1_rule):** model
P(success) with all Stage-1 values entered by `model_feedback` — GO ≥ 0.30, GO-WITH-LEVER 0.10–0.30 (Stage 2 +
Stage 1C), STOP < 0.10 (no hardware; Stage 1C, then G1′). Current model (thin-layer default cell, review corrections):
primary median 3.5 pg/mL, P 0.16 as specified; 1.3 pg/mL, P 0.32 after reagent + substrate screening (docs/08 §10).
Design changes from the review: separate bead and conjugate reservoirs; commercial single-channel thin-layer cell
by default (IDA + second channel only if Stage 2 shows a need); carry-over criterion 1×10⁻⁴ with a 10 ng/mL
challenge; fault latch + recovery cycle in the sequencer; phosphate K_i UNVERIFIED (0.2 µM–1 mM).
**Cartridge design round complete (2026-11-12, docs/16):** A (multi-run bead-transfer card, docs/13 Rev B) leads,
B (single-use cells) is the fallback, C′ (permanent chip, renewable micro-bed) is kept alive. No candidate has a
decision-grade LOD advantage: A Rev B without pre-electrolysis credit median 3.67 pg/mL, P 0.150 (credit, UNVERIFIED:
2.33, P 0.215); after screening 1.34, P 0.328 — vs gen-1 3.5 / 0.16 and 1.3 / 0.32. The case is throughput (31 vs
56 min per result), automation and buffer use. **Approved before G1: only M5a** (docs/06; informational, not a
G1a/G1 input; its weeks 6–8 slot does not fit the bench load — options in docs/06 M5a). Everything else for the
cartridge waits for G1 and E1.2b.

## Recording bench results
Put raw data and the filled CSV templates in `bench/<stage>_<experiment>_<date>/` (templates in
`automation/templates/`). Record measured model inputs in `bench/measured_values.yaml` (value, low, high,
source = experiment folder) — do not edit `params/chemistry.yaml` or `params/hardware.yaml`; accepted bench
values go into the `overrides` section of `params/model_assumptions.yaml` with the experiment as source.
