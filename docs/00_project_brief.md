# Project brief — automated electrochemical ELISA for human IgG at 1 pg/mL

This file is the shared source of truth for every task in the project. Read it before starting work.

## Goal

Detect human IgG in buffer at **1 pg/mL (≈ 6.7 fM, MW ≈ 150 kDa)** with an enzyme-linked immunoassay read out
electrochemically. In a 100 µL sample that is ≈ 4 × 10^5 molecules (≈ 0.67 amol).

## Success criteria

| Item | Requirement |
|---|---|
| Sensitivity | LOD ≤ 1 pg/mL, defined as mean blank + 3 SD of blank, from replicate blanks and a calibration curve |
| Range | Calibration over about 1–1000 pg/mL (3 logs) |
| Reuse | Capture surface regenerable/reusable for unattended sequential runs (or automatically renewable) |
| Sample | ≤ 100 µL per determination |
| Time | ≤ 60 min per sample, injection to result |
| Matrix | Buffer only (no serum/plasma requirement at this stage) |
| Automation | The whole method must be automatable — no manual steps between loading the autosampler and the result |

## Fixed equipment

- Waters ACQUITY **BSM** (Binary Solvent Manager) — pumping / reagent delivery
- Waters ACQUITY **SM-FL** (Sample Manager, **Fixed Loop** — not the flow-through-needle SM-FTN) — sample and reagent injection
- **Gamry Reference 600+** potentiostat — electrochemical detection
- Waters **Empower** CDS
- An extra externally triggerable **switching valve** (6- or 10-port)
- A Waters **optical detector** (TUV/PDA/FLR) for orthogonal checks during development

## Installed configuration (stated by the user, 2026-11-11)

These statements take precedence over generic vendor figures in docs/02 and params/hardware.yaml.

- System is an **ACQUITY UPLC I-Class PLUS**. The user states the BSM can flow down to **1 µL/min**
  (docs/02 lists 10 µL/min for I-Class from vendor documents — use the user's figure, confirm at the bench).
- SM-FL has a **100 µL sample loop**; the user injects the **full 100 µL by full-loop injection with 2× overfill**
  (so about 200 µL of sample is drawn per injection; 100 µL is the injected volume — whether the ≤ 100 µL limit
  applies to injected or consumed volume is to be confirmed with the user).
- The **external switching valve is not yet in hand**; model and port count are open and can be specified by the design
  (more than one valve may be purchased).
- **Empower Toolkit licence: yes.** Empower version unknown (to be checked later).
- A **second potentiostat channel is acceptable** (e.g. for interdigitated-electrode redox cycling).
- **Pre-mixing sample with conjugate/beads in the vial** is acceptable only if it is automated: the end user
  (a customer) must not have to do the addition by hand. The SM-FL cannot add reagents to vials (docs/02), so this
  needs either vials supplied pre-filled with reagent (the user only adds sample) or an added dispensing device.

## Open design choices (to be decided by the in silico work)

- Where the immunoassay happens: inline capture column/microreactor, on the working electrode, or
  offline in vials/wells/beads handled by the SM-FL
- Electrochemical flow cell and electrode (none in hand; anything may be purchased or custom made — budget unconstrained)
- Analyte standard and assay format (antibody pair, capture orientation)
- Enzyme label, substrate, and any amplification scheme
- Electrochemical technique (amperometry, pulsed methods, redox cycling, stripping, …)

## Control architecture (decided)

A single **custom Python orchestration layer** drives the Gamry and controls or triggers the Waters stack
(Empower in hand). The mechanism for the Waters side (Empower Toolkit, contact closure, etc.) is to be worked out.

## Phasing

1. **In silico (now):** literature-grounded parameters, a Python simulation (binding kinetics, mass transport,
   enzyme turnover, electrode response, noise) that predicts LOD per architecture, a ranked design choice,
   bill of materials, and a staged bench protocol / DoE.
2. **Bench (later):** execute the staged plan in the most efficient order to reach the goal.

## Rules for all contributors

- Every numerical parameter carries a source (citation with DOI/URL or vendor document) and a confidence
  level. If a value could not be verified against a source in this session, mark it `UNVERIFIED` — never invent
  a citation, a part number, or a specification.
- State assumptions explicitly; separate what was checked from what is inferred.
- SI-consistent units, stated on every quantity.
- Write only to the files assigned to your task.
