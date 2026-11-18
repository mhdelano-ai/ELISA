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
- Tier round (2026-11-17, docs/26 §2): the equipment in hand is the BSM + SM-FL, the Reference 600+ and a MicruX
  flow cell (both versions: printed strips and thin-film chips). Three implementations by what may be added:
  tier 1 consumables only, tier 2 plus passive in-line parts, tier 3 anything. Unattended per sample (bench
  preparation and a fresh electrode or bed per determination are allowed; no unattended queue required);
  ≤ 100 µL injected and ≤ 60 min still apply.

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
- `docs/18–25` — physical design of cartridge A and its dock (stage C0 desk work, C2 prototype level): interface
  (docs/18, Revision C), card (19), dock lid (20), lower bay (21), base and enclosure (22), integration with the
  authoritative tables of choices, deviations from docs/13 and open items (23), independent review and resolution of
  findings (24, §8), session record (25). docs/13 stays the specification; docs/18–24 list departures as deviations.
- `docs/26–32` — tier round: lowest-LOD assays on the equipment in hand, in three tiers. Brief and interview (26),
  capability map of the Waters stack without added hardware and instrument checks (27, Revision C), MicruX cells,
  electrodes and parts (28), literature (29), **the implementations (30, Revision C)**, the two review rounds and
  the resolution of every finding (31), session record (32).
- `docs/33_flow_cell_geometries.md` — follow-up to the tier round: other flow-cell geometries put into the designs
  of docs/30, and the pick (radial thin-layer cell, gap about 50 µm). Calculations in
  `scripts/tier_round/cell_geometries.py`; not independently reviewed.
- `docs/34_tier2_flow_cell.md` — follow-up: a custom flow cell for tier 2 with the bead bed inside the cell (three
  machined parts, 500 psi, MicruX strip as the electrode). Dimensions in `cad/elisa_cad/tier2_cell/params.py`, CAD
  output in `cad/out/tier2_cell/`, numbers from `scripts/tier_round/tier2_cell.py`; not independently reviewed.
- `docs/35_tier2_beads.md` — follow-up: alternative capture beads for the docs/34 cell (lowest LOD, mainly lowest
  NSB), five rounds with an independent reviewer until converged. Numbers from `scripts/tier_round/tier2_beads.py`,
  research notes and reviews in `results/tier_round/` (`beads_*.md`, `review_beads_r1–r5.md`).
- `scripts/tier_round/` — calculation kit and designs behind docs/30 (`README.md` there; `tierkit.py`,
  `designs.py`, `run_tiers.py`, `tier_params.yaml` with the `tr.*` parameters of the round); outputs and the five
  reviewer reports in `results/tier_round/`. The kit imports `elisa_sim` and edits nothing in `src/` or `params/`.
- `cad/` — parametric CadQuery model behind docs/18–24 (`cad/elisa_cad/interface.py` is the single source of truth
  for interface geometry; packages `card`, `dock_upper`, `dock_lower`, `dock_base`, `assembly`); outputs (STEP, DXF,
  PNG, check results) in `cad/out/`. See `cad/README.md`.
- `scripts/chip_round/` — the agents' working scripts and outputs behind docs/09–16 (record only; see its README).
- `docs/presentation/` — summary slide decks (in silico phase; cartridge round; tier round) as standalone HTML,
  sources, `build.py`; the tier-round deck is generated from the model output (`source_tiers/gen/`).
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
pip install -r cad/requirements.txt && pip install -e cad         # CAD model (CadQuery; no test suite, one-off checks)
python -m elisa_cad.card.build         # card (~1 min); likewise dock_upper, dock_lower, dock_base (`--fast`), assembly (~25 min)
python scripts/tier_round/check_tierkit.py          # tier round: 36 checks of the kit (~1 min)
python scripts/tier_round/run_tiers.py              # tier round: all designs, scenarios, alternatives (~2 min)
python scripts/tier_round/doc_tables.py --check     # tables of docs/30 against results/tier_round/tiers.json
python scripts/tier_round/cell_geometries.py        # docs/33: flow-cell geometries (~4 min; `--doc` prints its tables)
python scripts/tier_round/tier2_cell.py             # docs/34: tier-2 cell with the bed inside: model, pressure, 500 psi (~1 min)
python scripts/tier_round/tier2_beads.py            # docs/35: alternative beads in the docs/34 cell, paired MC (~2 min)
(cd cad && python -m elisa_cad.tier2_cell.build)    # docs/34: STEP files, section, drawing notes, 28 checks (~1 min)
(cd cad && python -m elisa_cad.tier2_cell.drawings) # docs/34: dimensioned A3 drawings T2C-001..004 (PDF + PNG, ~15 s)
python docs/presentation/source_tiers/gen/make_slides.py && python docs/presentation/build.py   # tier-round deck
```
The Gamry worker must run in Gamry's own 32-bit Python 3.7 (ToolkitPy); the orchestrator in Python ≥ 3.10.

## Status (2026-11-18)
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

**Tier round complete as desk work (2026-11-18, docs/26–32):** three implementations on the equipment in hand,
all sequential sandwich assays with the same reagents (docs/30 Revision C; model predictions from
`scripts/tier_round`, not on the same footing as the docs/05 numbers). Tier 1, capture on a printed gold strip in
the MicruX wall-jet cell, read under 200 µL/min substrate flow between two reference windows: nominal 3.6 pg/mL,
median 16 [2.8–110]. Tier 2, 1×10⁶ beads packed against a frit in a capillary whose tip sits in the cell's inlet
bore, stop 5 min and sweep: 2.1, median 8.4 [1.0–100], P(LOD ≤ 1) 0.05. Tier 3, the same bed in the loop of one
6-port valve: 1.2, median 5.1 [0.78–58], P 0.09. An immune-complex transfer to a second bed gives 1.1 at a release
of 0.35 (0.05–0.74, nothing measured) and 0.53 at 0.7; it is conditional on its own test. **Two bench questions
from the review reach the whole project and come before E1.2 (docs/30 §2.6, docs/31 §6):** (1) alkaline
phosphatase should turn hydroquinone diphosphate into the monophosphate, not hydroquinone, at picomolar enzyme
(finding C1; if the monophosphate is not oxidised at the read potential every predicted signal of the project is
10²–10⁵ too high and the substrate has to change); (2) the half-life of hydroquinone at pH 9.5 may be about
10 min, not 2 h (C5, M2; then the substrate's free hydroquinone is gone before use). Recommendation of the round:
the two questions first, then tier 2, with one valve as soon as it can be had. Nothing is ordered; no gate,
kill criterion or order of docs/06 is changed; whether the round's experiments enter the bench plan is the user's
decision (docs/30 §8, with the other open questions). Revision C answers the second review pass but was not
reviewed again (docs/31 §4.3). A 21-slide summary of the round is `docs/presentation/tier_round.html` (charts and
headline figures generated from `tiers.json`; checked twice by independent agents, docs/32 §7).

**Flow-cell geometries (2026-11-18, docs/33; desk work, not reviewed):** the cell shape is not where the LOD is.
The pick is the shape in hand, a radial thin-layer cell (inlet bore centred over the 3 mm electrode), with the gap
at about 50 µm (25–100 µm) instead of the 0.2 mm that docs/30 takes: tier 1 nominal 3.6 → 2.3 pg/mL (median
16 → 12; no gain if the substrate background persists), tiers 2 and 3 unchanged at nominal (2.1, 1.2) but 2–4
times lower if the signal is weak (1 % electroactive, with a faster sweep). A cross-flow channel is equal at equal
gap only if the electrode is the first surface; a large-gap wall jet and a porous flow-through electrode are worse.
No other cell needs to be bought. The gap of the cell in hand is unmeasured (docs/27 §9 item 4; docs/33 §6.2).
Nothing in docs/30 is changed; whether tier 1 takes the thin gap is the user's decision (docs/33 §8).

**Tier-2 flow cell with the bed inside (2026-11-18, docs/34; desk work, not reviewed, nothing ordered):** a stack
of three machined parts, 29 × 44 × 21.9 mm (plate and body acetal copolymer since 2026-11-18, PEEK fallback): body (inlet port whose 2.5 mm floor carries the 0.5 mm bed bore),
nozzle plate (retainer pocket, exit bore, lid of the thin layer, O-ring on the strip), 316L base (strip
pocket; a shim sets the gap, 0.10 mm). Revision B: in the plate's pocket a washer punched from 0.25 mm FKM sheet
presses screen and membrane against the flat body face around the bed bore (no 0.5 mm O-rings; body and plate
face to face; keep flows through the bed ≤ 80 µL/min). Beads stay Dynabeads M-280, 1×10⁶; because catalogue stainless screens are
only nominally rated (1 µm screen absolute at 6–7 µm), the retainer is a 1 µm track-etched membrane on a 2 µm
screen; non-porous 10–14 µm streptavidin polystyrene beads on the screen alone are the fallback. Model: 1.9 pg/mL
nominal, median 7.9 [0.96–93] against 2.1 and 8.4 for the capillary of docs/30; the retainer's conjugate uptake
(2.3–11 mm², UNVERIFIED) moves it between 1.7 and 2.4. Working pressure about 1 bar at 80 µL/min; laid out for
500 psi with a margin of 2.1 on the main screws (M4 0.25 N·m, M2.5 0.05 N·m, set by the acetal), but the O-ring seal on a printed strip at 500 psi needs a proof
test. Every hole ≥ 0.5 mm, so the parts suit a machining service such as Xometry; no quote obtained. Strip settled
by the user: ceramic S1PE strips, 0.38 mm (shim 0.07 mm); positions from MicruX's drawing, confirmed accurate
(electrode centre 8.26 mm from the free end, print to r 3.64 mm; docs/34 §5.4). docs/30 is not changed; the
choices for the user are in docs/34 §8.3. Every tier-2 CAD output file ends in `_v<N>` (`VERSION` in `params.py`, now 2 = the ±0.03 mm set; REV on the
drawings). Dimensioned drawings for ordering (Xometry), mostly at standard
tolerance (none tighter than ±0.03 mm since 2026-11-18, at the user's request): `cad/out/tier2_cell/drawings/` with `ORDERING.md`; tolerance policy in
docs/34 §5.2 (strip pocket at standard tolerance, gap set by a measured shim; second pin hole a slot). The
retainer washer is a cut gasket, T2C-004 (⌀1.4/⌀0.75 × 0.25 FKM; STEP and DXF cut files). The four drawings were
reviewed by an independent agent (19 findings, 17 applied: counterbored M2.5 screws, screw positions, sealing-face
flatness and finish; docs/34 Revision notes). Since then simplified at the user's request: only tolerances tighter
than standard and threads on the views, Ra 1.6 all over, M4 clearance ⌀5.5 (docs/34 §5.2).

**Tier-2 capture beads (2026-11-18, docs/35; desk work, reviewed in five rounds, converged; nothing ordered):** the
bead is a small lever in the docs/34 cell — the beads carry a third of the blank's non-specific enzyme (line and bore
above the bed 38 %, retainer 24 %), and part of their share sits on the capture-antibody layer that every bead carries.
Keep M-280 Streptavidin. Four challengers cluster at a nominal 1.8 pg/mL against 1.9 (M-270 Streptavidin and Vector
MagnaLINK 2.8 µm as drop-ins, micromod PEG-COOH 10 µm with covalent F(ab')₂, an in-house brush); MagnaLINK coated
with 3 × the antibody has the widest range (1.4–2.5). No bead reaches 1 pg/mL (ceiling 1.0 with no bead NSB at all).
Correction: the project's NSB rate comes from Rissin 2010's carboxyl beads, not from M-280 (docs/34 §0/§3 not edited).
A bench test (after C1/C5) is specified in docs/35 §5; whether it enters the bench plan is the user's decision.

## Recording bench results
Put raw data and the filled CSV templates in `bench/<stage>_<experiment>_<date>/` (templates in
`automation/templates/`). Record measured model inputs in `bench/measured_values.yaml` (value, low, high,
source = experiment folder) — do not edit `params/chemistry.yaml` or `params/hardware.yaml`; accepted bench
values go into the `overrides` section of `params/model_assumptions.yaml` with the experiment as source.
**Physical design of cartridge A and its dock complete as desk work (2026-11-13, docs/18–25, `cad/`):** card
75.5 × 50 mm with 21 valves and 11 liquid ports; dedicated bench dock 470 × 420 × 330 mm (388 lid open), ≈ 43 kg,
lab air ≥ 450 kPa. Integrated assembly has 0 unintended interferences (one-off check). Paper budgets hold thinly:
carry-over 9.87e-5 vs 1e-4 (needs 0.0635 mm ID sample line, UNVERIFIED part; shown only by E1.10/M7), 31.0 min
cadence, 3.25 min margin to 60 min, 14 runs per card. Choices the user may overrule: docs/23 §8; deviations from
docs/13: docs/23 §9; open items: docs/23 §10. Nothing is ordered or built: the cartridge still waits for G1 and E1.2b.
