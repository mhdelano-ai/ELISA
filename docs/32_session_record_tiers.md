# 32 — Session record: three implementations for the lowest LOD on the equipment in hand (2026-11-17/18)

A record of how docs/26–31, `scripts/tier_round/` and `results/tier_round/` came about: what the user asked, every
question put to the user and the answer, which task did what, what went wrong on the way, and where each output is.
It contains no new technical claims. The designs and their numbers are in docs/30; the findings of the review and
what was done about each are in docs/31.

## 1. The request

> "I have the following tools at my disposal: acquity i-class bsm with sm-fl (fixed loop); Gamry 600+; 10uL flow
> cell that can hold any micrux screen printed electrode. Design an assay that uses these items for the absolute
> best LOD of human IgG. Interview me if you need input."

Later messages from the user: "Resume" (after the first agents had stopped, section 4), "Maybe use opus for the
agents?", and "Resume" once more after the session's worker had restarted during the last revision.

## 2. Interview — every question and answer

| # | Question | Answer |
|---|---|---|
| 1 | Besides the BSM, SM-FL, Gamry 600+ and the 10 µL cell, what may the assay add to the set-up: consumables only; passive in-line parts as well; or anything? | "Three different implementations with these categories." One design per category (tiers 1–3) |
| 2 | How much hands-on work is acceptable? | Unattended per sample: preparation at the bench beforehand, each determination unattended from injection to result; a fresh pre-coated electrode per determination is fine |
| 3 | Do the limits of 100 µL injected and 60 min from injection to result still apply? | Both still apply |
| 4 | Which MicruX cell and electrodes? | Both cells are available (printed thick-film strips and 10 × 6 mm thin-film chips); choose whichever gives the best LOD |

No further question was put to the user during the round. The points the orchestrator decided, and the questions
that only the user can answer, are listed in docs/30 §8.

## 3. Who did what

| Step | Done by | Output |
|---|---|---|
| Round brief: request, interview, tier definitions, binding constraints, readings the user may overrule | orchestrator | docs/26 |
| MicruX cells, electrode catalogue, wiring, passive parts, additions for tier 3 (vendor documents opened) | research agent | docs/28 |
| Literature: detection and amplification at one electrode | research agent | docs/29 Part A |
| Literature: capture formats in flow, benchmarks, human IgG as analyte | research agent | docs/29 Parts B and C |
| Fact-check of the Waters stack: zero-flow row, minimum flow, behaviour between lines, restrictor, loop | research agent | docs/27 Appendix A |
| Capability map of the equipment without added hardware; modelling map; instrument checks | orchestrator | docs/27 |
| Calculation kit (wall-jet capture, thin-layer transport, bed formats, blank statistics, Monte Carlo), its 36 checks and the cross-check with the audited model | orchestrator | `scripts/tier_round/tierkit.py`, `tier_params.yaml`, `check_tierkit.py`, `crosscheck_model.py`, `README.md`; `results/tier_round/check_tierkit.md` |
| The three designs, their scenarios, alternatives and sensitivities | orchestrator | `scripts/tier_round/designs.py`, `run_tiers.py`; `results/tier_round/tiers.md`, `tiers.json`; docs/30 (first version) |
| Independent review, three lenses: numbers and physics; chemistry and bench realism; feasibility and consistency | three review agents | `results/tier_round/review_numbers.md`, `review_chemistry.md`, `review_feasibility.md`; `scripts/tier_round/review_*.py` |
| Resolution of the findings: kit and designs changed, all numbers re-run, documents rewritten | orchestrator | docs/30 Revision B, docs/27 Revision B, kit and results as above |
| Second pass on Revision B, two lenses: numbers and physics; consistency and feasibility | two review agents | `results/tier_round/review2_numbers.md`, `review2_consistency.md` |
| Resolution of the second pass: kit changed again, operating points moved, all numbers re-run; the result tables of docs/30 generated from the model output; the earlier designs re-run with the shorter half-life | orchestrator | docs/30 Revision C, docs/27 Revision C, docs/31, `scripts/tier_round/doc_tables.py`, `earlier_designs_halflife.py`, `results/tier_round/earlier_designs_halflife.md` |
| Session record, project guide | orchestrator | docs/32, CLAUDE.md |

All agents that produced a result ran on the Opus model. They wrote only their own files and did not commit.

## 4. What went wrong on the way

* **Agent concurrency.** A workflow runs at most two agents at a time on this machine (four processors). The first
  workflow of six agents was stopped and split into three workflows.
* **Usage limit.** The first six research agents, started on the session's own model, all ended after about 20 min
  on the account's 5-hour usage limit and left only file skeletons. After the user's "Resume" the research was
  redone with four narrowly scoped agents on the Opus model, each with a pre-digested brief and a limit of about 60
  tool calls. The calculation kit, which had been planned as an agent task, was written by the orchestrator.
  The user then asked for Opus agents throughout; every later agent used it.
* **Model cross-check.** The kit's first cross-check against the audited model was off by a factor of 2.8 in the
  enzyme count: the model places a partial reagent plug at the inlet end of the loop
  (`ma.delivery.plug_at_outlet_end`), the kit had not read that parameter. After the correction the two agree to
  10⁻⁹ on the overlapping bed format.
* **The first version of the designs did not survive the review.** Its LODs (3.1, 0.75 and 0.33 pg/mL) left out
  blank terms, and one method step could not work as written (docs/31 §2). Revision B stood at 9.4, 2.6 and 0.62.
* **Revision B did not survive its second pass unchanged either.** The second reviewers confirmed its numbers
  against the kit and found that it treated the hydroquinone of the substrate reservoir differently from that of
  the product, compared two different buffers in the tier-1 read, let the read bed of the transfer fill with
  capture antibody, and still presented the transfer at a release nobody has measured (docs/31 §4). Revision C
  stands at 3.6 (tier 1), 2.1 (tier 2) and 1.2 pg/mL (tier 3 with one valve); the transfer is conditional.
* **Errors found by the orchestrator in its own text** before the second pass: two pressure drops across the bed
  (21 and 33 bar instead of 15 and 25), a collection efficiency quoted for the wrong cell (45 % instead of 99 % at
  1 µL/min), a tier order stated without its exceptions, and vendor part names not written as the vendor writes
  them. Since Revision C the result tables of docs/30 are generated from the model output and checked by
  `scripts/tier_round/doc_tables.py --check`.
* **Revision C was not reviewed again** (docs/31 §1 and §4.3 say what was changed after the second pass and what
  checks it).

## 5. Commits of the round (branch `claude/inspiring-brown-oh0u31`)

| Commit | Content |
|---|---|
| 4f8d8e9 | round brief (docs/26) |
| 520d651 | work in progress: groundwork while the first agents were writing |
| af86266 | groundwork: MicruX hardware (docs/28), literature notes, Waters fact-check, calculation kit |
| 5775ce9 | designs and model runs (`scripts/tier_round`, `results/tier_round`) |
| 7bff783 | first version of docs/30; docs/27; docs/29 |
| d8db228 | the three reviewer reports |
| 0578dfc | Revision B of the kit, designs, results, docs/30 and docs/27 |
| eda7031 | the two second-pass reports; the final revision of the kit and its results |
| the commit that adds this record | docs/30 Revision C, docs/27 Revision C, docs/31, docs/32, CLAUDE.md, README of the kit |

No pull request was opened.

## 6. Where everything is

| Question | Place |
|---|---|
| What was asked and what binds | docs/26 |
| What the three designs are, step by step, and what they are predicted to reach | docs/30 |
| What the equipment can do without added hardware; what to check on the instrument first | docs/27 (§9) |
| What MicruX sells and states; questions for the vendor | docs/28 (§8) |
| What the literature shows | docs/29 |
| What the reviewers found and what was done | docs/31 |
| How the numbers are computed and how to re-run them | `scripts/tier_round/README.md`; docs/30 §9 |
| What the user is asked to decide | docs/30 §8 |
