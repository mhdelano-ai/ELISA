# 26 — Round brief: best-LOD assays on the equipment in hand, in three tiers

Written by the orchestrator on 2026-11-17. This file is the shared source of truth for every task of this round
(docs/26–36, `scripts/tier_round/`, `results/tier_round/`). docs/00 and the fixed decisions in CLAUDE.md still
apply except where section 3 says otherwise.

## 1. The request

> "I have the following tools at my disposal: acquity i-class bsm with sm-fl (fixed loop); Gamry 600+; 10uL flow
> cell that can hold any micrux screen printed electrode. Design an assay that uses these items for the absolute
> best LOD of human IgG. Interview me if you need input."

## 2. Interview (2026-11-17) — every question and answer

| # | Question | Answer |
|---|---|---|
| 1 | Besides the BSM, SM-FL, Gamry 600+ and the 10 µL cell, what may the assay add to the setup? Options offered: (a) consumables only; (b) plus passive in-line parts; (c) anything, as before | **"Three different implementations with these categories."** One design per category (tiers 1–3, section 4) |
| 2 | How much hands-on work is acceptable to get the best LOD? | **Unattended per sample.** Electrodes are coated and reagents made up at the bench beforehand; each determination then runs unattended from injection to result. Swapping in a fresh pre-coated electrode between determinations is fine |
| 3 | Do the 100 µL injected and 60 min injection-to-result limits still apply? | **Both still apply** |
| 4 | Which Micrux cell and electrodes are these? | **Both cells available**: the cell for printed thick-film strips and the cell for 10 × 6 mm thin-film chips. Choose whichever electrode family gives the best LOD |

## 3. What applies to all three tiers

**Objective.** The lowest limit of detection for human IgG in buffer. LOD = mean blank + 3 SD of replicate blanks,
read through a calibration curve (docs/00). Because a fresh electrode (and, where used, a fresh capture element) may
serve each determination, the replicate blanks are blanks on *different* consumables: unit-to-unit variation is
part of the blank SD.

**Equipment in hand (must be used).**
* Waters ACQUITY UPLC I-Class PLUS: BSM (binary pump, lines A1/A2 and B1/B2) and SM-FL with a 100 µL loop, full-loop
  injection with 2× overfill (docs/00, docs/02).
* Gamry Reference 600+ (one potentiostat channel).
* A Micrux flow cell, stated by the user to have a 10 µL volume, in two versions: one holds Micrux printed
  thick-film electrodes (27.5 × 10.1 mm strips), the other Micrux thin-film electrodes (10 × 6 mm glass chips).
  The cell's geometry and the meaning of "10 µL" are not yet verified (task of docs/28).
* Empower runs the Waters stack; the Python layer drives the Gamry (docs/00, `automation/`).

**Constraints that bind.**

| Item | Requirement | Origin |
|---|---|---|
| Sample | one injection, ≤ 100 µL injected (full loop, about 200 µL drawn) | answer 3; docs/00 |
| Time | ≤ 60 min from the sample's Inject Start to the result | answer 3 |
| Sample vial | contains sample only; no reagent pre-filled, none added by hand | CLAUDE.md fixed decision |
| Hands-on | none between the sample injection and the result | answer 2 |
| Matrix | buffer only | docs/00 |
| Proteins and beads | never through BSM pump lines; only by SM-FL injection from tray vials (or, in tier 3, added hardware) | docs/02 §1.2 |

**Relaxed relative to docs/00 (answer 2).**
* The capture surface need not be reusable or renewed automatically: a fresh pre-coated electrode, column or bead
  charge per determination, fitted by hand before the run, is allowed.
* An unattended queue of many samples is not required. Any amount of bench preparation before the injection is
  allowed (coating, blocking, packing, reagent vials in the tray, BSM bottles), as long as the sample is not touched.
* Automated steps before the sample injection (conditioning, a baseline or background read on the mounted
  electrode) are allowed and do not count toward the 60 min.

**Orchestrator's readings — the user may overrule these.**
* *Range.* docs/00 asks for a calibration over about 1–1000 pg/mL. This round optimises the LOD; the upper limit of
  quantification is reported for every design but is not a constraint. A design must still give a monotonic
  calibration over at least two decades above its LOD.
* *Restrictor.* The BSM needs about 1000 psi of back-pressure (docs/02 §1.2). A restrictor capillary upstream of
  the injector is treated as tubing and is allowed in tier 1.
* *Reagent vials.* Conjugate and other reagents may sit in their own vials in the SM-FL tray and be injected by
  further sample-set lines (docs/02 §2.4b; docs/05 §4.0 route S). Only the sample vial is restricted.
* *Potentiostat.* Tiers 1 and 2 use the single Reference 600+ channel. Tier 3 may add a second channel.

**Open hardware facts that decide what is possible without valves** (to be settled or bounded by docs/27, docs/28):
* whether the BSM accepts a 0 mL/min step in a method, and its real minimum flow (vendor documents: 10 µL/min for
  I-Class; the user states 1 µL/min for this I-Class PLUS; docs/02 §1.1);
* the internal geometry of the two Micrux flow add-ons (channel height, footprint, where the inlet and outlet sit
  relative to the working electrode, wetted materials, pressure limit).

## 4. The three tiers

| Tier | May be added to the equipment in hand | Consequence |
|---|---|---|
| **1 — consumables only** | reagents, Micrux electrodes, vials, tubing and fittings (including the restrictor) | capture has to happen on the electrode or inside the 10 µL cell; flow is stopped only by the BSM programme |
| **2 — plus passive in-line parts** | also parts with no controller: a small packed capture column or bead frit, a holding coil, a fixed magnet, a scavenger cartridge. No added valves, pumps or potentiostat channels | capture may move off the electrode; everything injected still passes through the cell |
| **3 — anything** | valves, a dosing pump, a second potentiostat channel, custom parts (docs/05, docs/07, docs/13 show what is possible). The BSM, SM-FL, Gamry and the Micrux cell remain in use | the constraint list of section 3 is all that binds |

Each tier gets one recommended implementation, designed for the lowest LOD that tier allows, with its runners-up
recorded.

## 5. What each design must state

1. Flow path and every consumable (with source and confidence; UNVERIFIED where not checked).
2. Electrode family and type, surface chemistry, antibody pair, label, substrate, buffers.
3. The step table from injection to result (≤ 60 min), with flows, volumes, BSM lines, SM-FL sample-set lines and
   Gamry technique and potentials.
4. Bench preparation before the run.
5. Predicted LOD: nominal, and median with 5–95 % interval from parameter uncertainty, with the limiting term and
   the assumptions that carry it. Calculations as scripts in `scripts/tier_round/` with outputs in
   `results/tier_round/`.
6. What could make it fail, and the bench experiments that decide, in order.

## 6. Files of this round

| File | Content |
|---|---|
| docs/26 | this brief |
| docs/27 | capability map of the equipment in hand without added hardware; modelling map |
| docs/28 | Micrux cells and electrodes; passive in-line parts; additions for tier 3 |
| docs/29 | literature: detection and amplification, capture formats, benchmarks |
| docs/30 | candidates per tier and their selection |
| docs/31, 32, 33 | detailed design of tier 1, tier 2, tier 3 |
| docs/34 | independent review and resolution of findings |
| docs/35 | decision: comparison of the three implementations, bench order, open items |
| docs/36 | session record |
| `scripts/tier_round/`, `results/tier_round/` | calculation kit, design scripts and their outputs |

## 7. Rules for every task of this round

* Sourcing rule of CLAUDE.md: every number carries a source (DOI, URL or vendor document) and a confidence; what
  was not checked in the session is marked **UNVERIFIED**. Never invent a citation, part number, price or vendor
  API call. A search-engine summary is not a checked source: open the page or mark the value accordingly.
* Do not edit docs/00–25, `params/*.yaml`, `src/`, `tests/`, `automation/` or `cad/`. New parameters of this round
  go into `scripts/tier_round/tier_params.yaml` in the schema of the `params/` files.
* Write only to the files assigned to the task. Write to disk early and keep the file complete at every save.
* SI-consistent units on every quantity. State assumptions; separate what was checked from what is inferred.
* Do not commit or push; the orchestrator does that.
