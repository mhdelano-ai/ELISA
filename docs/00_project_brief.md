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
- Waters ACQUITY **SM-FL** (Sample Manager, Flow-Through Needle) — sample and reagent injection
- **Gamry Reference 600+** potentiostat — electrochemical detection
- Waters **Empower** CDS
- An extra externally triggerable **switching valve** (6- or 10-port)
- A Waters **optical detector** (TUV/PDA/FLR) for orthogonal checks during development

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
