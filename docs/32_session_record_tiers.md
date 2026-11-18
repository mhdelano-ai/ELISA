# 32 — Session record: three implementations for the lowest LOD on the equipment in hand (2026-11-17/18)

A record of how docs/26–31, `scripts/tier_round/` and `results/tier_round/` came about: what the user asked, every
question put to the user and the answer, which task did what, what went wrong on the way, and where each output is.
It contains no new technical claims. The designs and their numbers are in docs/30; the findings of the review and
what was done about each are in docs/31. Section 7 records the summary deck that was made afterwards.

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
| the commit that adds this record (ae7e472) | docs/30 Revision C, docs/27 Revision C, docs/31, docs/32, CLAUDE.md, README of the kit |
| 8731ced | summary deck, first complete version: sources, generator, standalone file; docs/31 §2 corrected (round 2 rated eleven findings significant, not eight) |
| 6708c67 | the deck after its first independent check |
| the commit that adds section 7 | the deck after its second check; section 7; CLAUDE.md |

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
| The round in 21 slides | `docs/presentation/tier_round.html` (section 7) |

## 7. The summary deck (added 2026-11-18)

After the round the user asked: "Summarize this session with a visual html deck. Include charts and diagrams with
representative images." The deck is `docs/presentation/tier_round.html` (21 slides in one self-contained file);
its sources and its generator are in `docs/presentation/source_tiers/` (see `docs/presentation/README.md`). It is
also published as a private slide deck in the user's account. It contains no new technical claim: its numbers are
those of docs/30 Revision C.

| Step | Done by | Output |
|---|---|---|
| Slide texts and layout; charts and headline figures generated from `tiers.json`; three small tier pictures; the two curves and the split of the blank that the model output does not hold | orchestrator | `source_tiers/gen/templates/`, `make_slides.py`, `chart_extra.py`, `chart_extra.json` |
| Nine schematic drawings (equipment, two cell cross-sections, the valve in both positions, the sandwich, the product scheme, three trace sketches), each rendered and checked by its author | five agent tasks | `source_tiers/gen/art/` |
| First check of the deck, five lenses: facts of slides 1–11 and of slides 12–21 against docs/30–32 and `tiers.json`; slide format and charts; pictures; narrative. The findings of the first four were each challenged by a second agent | nine agent tasks | 22 challenged findings (17 confirmed, 4 partly, 1 refuted) and 15 narrative findings |
| Changes after the first check | orchestrator | commit 6708c67 |
| Second check, of the revised deck: the changed statements against the sources; every rendered slide; each finding challenged by a second agent | four agent tasks | 6 findings, all confirmed; none on a number or a statement of fact |
| Changes after the second check | orchestrator | the commit that adds this section |

All agents ran on the Opus model, wrote only their own files and did not commit.

What the first check found. No number on a slide or in a chart disagreed with docs/30 or `tiers.json`. Two things
were wrong: a note that called the 17 min the label waits in the transfer an extra wait (it is the whole wait; with
one valve it is about 5 min), and the small tier-3 picture, which did not show the bed in a closed loop. The tier-2
cross-section showed liquid beside the capillary where the design has a sleeve. The rest: statements stronger
than their source (a half-life "found" where it was extrapolated, judgement ranges not marked as judgement, an
answer marked verbatim that the record does not quote, a charge figure without its "unverified"), a transfer chart
without the fair comparison for screened reagents, leaders that crossed parts or ended on nothing, unlabelled
colours, internal lever names on the slides, the headline limits not marked as predictions on the design slides,
and a slide order that used the transfer before explaining it.

What was changed: the tier-2 cross-section (sleeve down to the capillary tip; labels moved so that no leader
crosses the outlet), a dimension mark for the cell gap, the cell symbol of the valve drawing, the small tier-3
picture, the tier-1 trace sketch, labels for phosphate and hydroxyl on the product scheme; a second reference line
on the transfer chart (one valve with screened reagents, 0.88); "Predicted limit" and the meaning of median and
range on each design slide; the judgement ranges marked as judgement; plain-word names for the scenarios; a card
with the eight choices the user may overrule (docs/30 §8); what went wrong on the way; the earlier design of the
project beside the results; the transfer slide moved to follow tier 3; a title of the timeline slide that no
longer contradicts its own card; a no-break space between each number and its unit. The one refuted finding
(caption contrast of 4.3:1 on one slide; the reference pages state no minimum) was changed all the same.

What the second check found. Every changed statement and every recomputed value agreed with docs/30–32,
`tiers.json` and `chart_extra.json`, and no slide contradicted another. Six points of presentation were confirmed
and changed: the process slide showed eight agent boxes beside the figure 9 (the literature work was two tasks);
the glass walls of the capillary were drawn in the colour of the liquid; a leader touched an O-ring; the small
tier-3 picture had the bed against the valve body; axis and window labels of the trace sketches ran together; the
legend mark of the transfer chart did not match its lines. The state after these six changes was checked by the
orchestrator only (generator checks, rendering, the standalone file opened in a browser with and without the web
fonts), not by a further agent.

What the deck does not have: photographs. The pictures are schematic drawings made for it.

## 8. Follow-up: flow-cell geometries (2026-11-18)

Request, in the same session as the deck: "Why did you choose hydroquinone, alkaline phosphatase, and a wall jet
configuration?" (answered in the conversation from docs/01, docs/28 and docs/03; no file changed), then "Explore
other flow cell geometries and pick the best one." No question was put to the user.

| Step | Done by | Output |
|---|---|---|
| Candidate geometries put into the unchanged designs of `run_tiers.py`; a solver for product released from a channel wall ahead of the electrode; wrappers for a porous electrode, a free wall jet and an ideal bound; 18 checks | orchestrator | `scripts/tier_round/cell_geometries.py`; `results/tier_round/cell_geometries.md`, `cell_geometries.json` |
| Comparison, the pick, limits, open questions, record | orchestrator | docs/33 |
| Entry in the kit's README, project guide | orchestrator | `scripts/tier_round/README.md`, CLAUDE.md |

No agent was used and the result was not independently reviewed. `tierkit.py`, the designs, docs/26–31 and the
deck are unchanged; `check_tierkit.py` (36 of 36) and `doc_tables.py --check` were re-run and pass. What went wrong
on the way is in docs/33 §10.

