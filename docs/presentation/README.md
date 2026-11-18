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

## Tier round (2026-11-18)

- `tier_round.html` — the 21-slide deck on the three-tier round (docs/26–32) as one self-contained file (same
  viewer: arrow keys or Back / Next; print gives one slide per page). It covers the request and the interview, how
  the session ran, what sets the detection limit on the equipment in hand, the shared assay, the three designs with
  cross-sections of the cell and the valve in both positions, how each design reads, the hour of one determination,
  the predicted limits and what limits them, the two review rounds and what they did to the numbers, the scenarios,
  the conditional transfer to a second bed, the two bench questions, the bench order and the questions for the user.
- `source_tiers/` — its sources: `deck.json`, `deck.css` (shared styles) and one file per slide in `slides/`, with
  sources and caveats in each slide's `<aside>`. The slide files are generated; do not edit them by hand.
- `source_tiers/gen/` — how the slides are made:
  - `templates/<id>.html` — the text and layout of each slide, with placeholders for drawings, charts and numbers;
  - `make_slides.py` — fills the templates: charts and numbers are read from `results/tier_round/tiers.json` and
    `chart_extra.json`, drawings from `art/`; it also checks every slide against the limits of the slide format
    (element counts, text sizes, drawing sizes);
  - `chart_extra.py` — computes, with the round's kit, what the model output does not hold: the transfer design
    against the released fraction, the conversion of the electrode against flow, and where the blank's enzymes sit;
  - `art/` — the nine drawings (`*.svg`), their labels (`*.labels.json`) and the scripts that drew eight of them
    (`gen_*.py`; `kit.svg` has no script); `art/tools/render_art.js` renders a drawing with its labels (needs
    Playwright).

To change a slide: edit its template (or a drawing script, then run it), then

```bash
python docs/presentation/source_tiers/gen/chart_extra.py    # only if the model or the kit changed (needs `pip install -e .`)
python docs/presentation/source_tiers/gen/make_slides.py
python docs/presentation/build.py
```

Its numbers are those of docs/30 Revision C: model predictions, not measurements. The charts and the headline
figures (limits, medians, ranges, chances, times, captured shares) are read from the model output when the slides
are made. Typed by hand, from docs/30 and docs/31: the other numbers in the slide texts and notes, the
first-version and Revision-B figures on the "revisions" slide and the finding counts on the "review" slide. The
drawings (equipment, cell cross-sections, valve, sandwich, product scheme, trace sketches) are schematics made for
the deck: not to scale, not pictures of the instruments, and the traces are sketches of the expected signal, not
data.
