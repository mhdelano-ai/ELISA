# Summary presentations

## In silico phase (2026-11-11)

- `in_silico_summary.html` — the 14-slide deck as one self-contained file. Download it and open it in any
  browser; use the arrow keys or the Back / Next buttons. Fonts load from Google Fonts when online and fall back to
  Arial offline. Printing from the browser gives one slide per page.
- `source/` — the slide sources (`deck.json` for order and titles, one file per slide in `source/slides/`,
  speaker notes in each slide's `<aside>`).
- `build.py` — rebuilds both decks from their sources: `python docs/presentation/build.py`.

The numbers on the slides are those of docs/05 and docs/08 §10 at the end of the in silico phase (2026-11-11).
If the model or the design changes, update the slide sources and rebuild.

## Cartridge design round (2026-11-12)

- `cartridge_round.html` — the 18-slide deck on the second-generation cartridge round as one self-contained file
  (same viewer: arrow keys or Back / Next; print gives one slide per page). It covers the brief, how the agent work
  was organised, the interview decisions, the survey findings, the three candidates, cartridge A (layer stack, plan
  view, assay cycle), the alternatives B and C′, the review and Revision B, performance against gen-1, the deciding
  unknowns, the gate plan and the decision.
- `source_cartridge/` — its sources: `deck.json`, `deck.css` (shared styles) and one file per slide in `slides/`,
  with sources and caveats in each slide's `<aside>`.

Its numbers are those of docs/16 (comparison table), docs/13 Revision B and docs/14 as revised, all nearest-model
estimates. The diagrams are simplified schematics, not to scale and not fabrication drawings. On the "unknowns"
slide the read-repeatability and bead-dose panels use figures from the first design of A (before the review, with the
pre-electrolysis credit); they were not re-run for Revision B.
