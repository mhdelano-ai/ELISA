# Review round 3 — docs/35 Revision C (tier-2 capture beads)

Reviewer: independent, adversarial. Date 2026-11-18. Ran `python scripts/tier_round/tier2_beads.py --quick` (rc 0,
nominals identical to the committed output) and my own scripts in the scratchpad (`s1.py`, `s2.py`, importing the
module; n = 400 and 2000). No repo file edited.

## What I checked and found correct
- Every number in docs/35 §0 and §4 against `results/tier_round/tier2_beads.md` (n = 2000): all four cluster rows
  (1.8; 7.8/8.0/7.0/6.4; P 0.66/0.54/0.83 (0.65)/0.79), medians 6.4–8.0 vs 7.9, blank shares 33/24/5/38 %, the
  limits 1.6 / 1.5 / 1.3 / 1.0, the φ = 0 and 0.8 rows, the covalent 1/3 (2.4; 10; 0.10 / 2.8; 12; 0.00) and 1
  (1.6; 6.6; 0.98) rows and the MagnaLINK rows (1.9/1.7/2.5/1.4/2.5) all match the output as published.
- k_r = 3×10⁵ M⁻¹s⁻¹ × 1×10¹⁶ × 0.85 / N_A = 4.2×10⁻⁶ m/s (kit), as stated.
- P(rel < 1) for M-270's log-triangular (0.4, 0.8, 2) = 0.674, so "0.66 ≈ 0.67" is right.
- Round-2 findings M1 (covalent penalty now a judgement 0.7 with 1/3 and 1 as sensitivity), M2 (MagnaLINK added),
  m1–m6 are addressed in the text.
- Spot-checks of sources:
  - MagnaLINK M-1003 (vectorlabs.com/products/magnalink-streptavidin-mag-beads-2-8-m/, read this session): 2.8 ± 0.2 µm,
    < 5 % CV, "hydrophilic polymer–encapsulated", 10 mg/mL in water + 0.05 % azide (no BSA), biotin-IgG
    "750 pmol/mg (113 µg/mg)" against a competitor's "60 pmol/mg (10 µg/mg)", free biotin "≥ 10 nmol/mg" (the
    overview says "at least 12"), $369 for 1 mL; no bead count per mg, porosity not stated. Also states streptavidin is
    "covalently cross-linked … using SoluLINK" and claims "lower background from nonspecific binding". docs/35's
    quotation is correct.
  - micromod 08-56-104 (2010 datasheet, funakoshi mirror, read this session): micromer-M, PEG-COOH, 10 µm, CV < 10 %,
    1.1 g/cm³, 1.7×10⁶ particles/mg, 50 mg/mL; PEG length not given. Matches beads_vendors.md row 4. Current
    availability not confirmed (only 2010 copies and distributor listings of sister numbers found).

## Findings

### Major

**MJ1. Monte Carlo double-counts the `load` term for every bead with load ≠ 1 (code error; medians and P values of
the brush, micromod SA and all MagnaLINK high-load variants are wrong).**
- Location: `tier2_beads.py`, `paired_mc`: `base = pset(ps, dict(c, rel=(1.0, 1.0, 1.0)))`. `pset` multiplies the
  packed-bed factor by `bead_mult(c, 0.5) = 0.5·load + 0.5·rel`; with rel forced to 1 this is 1 only when load = 1.
  The sampled factor is then multiplied again by `φ·load + (1 − φ)·rel`. So the base is 0.65 × M-280 for the brush,
  0.70 for micromod SA and 2.0 for MagnaLINK at load 3, and the load enters twice. Nominal LODs (`pset(ps, c)`) are
  correct; only the paired MC is affected. The comment ("packed-bed factor of M-280") states the intent.
- Evidence (n = 2000, base set with load = 1, everything else unchanged; `s2.py`):

  | Case | Published median; P(< M-280) | Corrected median [5–95 %]; P(< M-280); P same area |
  |---|---|---|
  | Brush, 4× | 6.4; 0.79 (0.79) | 7.4 [0.92–94]; 0.60; 0.72 |
  | micromod SA 10 µm, 2× | 11; 0.13 | 13 [1.3–190]; 0.04; 0.07 |
  | MagnaLINK 3× Ab, sites 2, NSB × 3 | 9.9; 0.05 | 7.6 [0.93–90]; 0.56; 0.94 |
  | MagnaLINK 3× Ab, sites 3, NSB × 3 | 8.7; 0.28 | 6.8 [0.86–76]; 0.95; 0.96 |
  | MagnaLINK 3× Ab, sites 1 | 15; 0.00 | 10 [1.2–130]; 0.01 |
  | Brush load 1 (variant) | unaffected (10; 0.19) | — |

- Consequences: §0 "medians 6.4–8.0" becomes 7.0–8.0 and the brush row 1.8; 7.4; 0.60 (same area 0.72) — the brush
  is no longer the best median of the cluster; PEG-COOH (7.0) is. §0 "If it grows with the load the gain is gone
  (1.7–2.5)" is wrong at the median: with the capture-layer NSB tripled, MagnaLINK at 3× antibody and half the
  beads still beats M-280 in 56 % (all antibody 2/3 active) to 95 % (all active) of draws; the gain goes only if the
  extra antibody is inaccessible. MagnaLINK's high-load case is therefore the most robust upside, not a fragile one.
  The recommendation (keep M-280, test challengers incl. MagnaLINK at 3× antibody) stands; the text about MagnaLINK
  and the brush changes, and headline medians move by up to 16 % (brush) and 25 % (variants).
- Fix: `base = pset(ps, dict(c, rel=(1.0, 1.0, 1.0), load=1.0))`; add a check that the base packed-bed factor of
  every candidate equals M-280's; rerun and update §0, §4, §5(b).

**MJ2. The bench decision rule cannot be met by the effect sizes the study predicts, and it cannot detect the
study's own "largest upside".**
- Location: docs/35 §5, "M-280 stays unless a challenger lowers the blank by at least 1.5 × … without losing capture".
- Evidence: in the model the beads carry 33 % of the blank (§1). Removing all bead NSB at the same area lowers the
  total blank by 33 %, i.e. exactly 1.5×; the cluster beads are predicted to lower it by ~5–10 %. So the rule, applied
  to the total blank, can only fire if the packed-bed factor is far above its nominal 3 — the test is decided by the
  study's own model before it is run. Second, MagnaLINK at 3× antibody and half the beads gains through capture,
  not blank (bead NSB 0.5 × (0.5·3 + 0.5·0.8) = 0.95 of M-280's, Derived): the rule rejects it even if its 1.4
  materialises. Third, the LOD scales with blank SD / capture, not blank alone. With the model's blank CV
  (≈ 0.14 = 0.1 ⊕ 0.1 bed, `chem.nsb.blank_CV_analog_electrochemical`, `tr.nsb.unit_to_unit_cv_bed`) n = 5 per arm
  resolves ~25 % (1.8 × CV), so a 1.5× threshold is also not what the power statement supports.
- Fix: decide on an LOD proxy measured in the same runs — (blank SD or blank × CV) / signal of the 1 pg/mL standard —
  with a threshold of ≥ 1.3× (resolvable at n = 5 if the CV is ≤ 15 %), or state the rule on the bead-attributable
  blank (bead arm minus the empty-retainer arm, which the test already contains, with its larger variance and the
  n that follows). Say explicitly that a 1.5× total-blank threshold is only reachable if bead NSB is ≥ ~2× the model's
  share.

### Minor

- m1. `load` is applied inconsistently: LodeStars Streptavidin gets sites 0.7 *because it binds less antibody*
  (brochure 5 vs ≈ 10 µg/mg), yet load = 1; the micromod SA bead with the same logic gets load = sites = 0.4. With
  load 0.7, LodeStars SA goes 2.07 → 1.93 nominal, P(< M-280) 0.68 → 0.91 (n = 400, `s1.py`), i.e. tied with M-280
  rather than behind it. Covalent beads keep load 1 at sites 0.7, which is defensible (inactive antibody still
  present) but should be stated as such; with load 0.7 they would be 1.93. Fix: set LodeStars load = 0.7 (0.5–1)
  or state why the capture layer of a less-loaded bead carries M-280's NSB; one sentence on the covalent case.
- m2. Brush ranking hinges on its site factor 0.3 (entangled); with the kit's sites it would be 1.36 nominal
  (`s1.py`). It is a development project so the ranking is not affected, but §5's list of "what would turn the
  ranking" omits it.
- m3. Stale text: `tier2_beads.py` docstring still says covalent coupling = 1/3 from Peluso 2003 (Revision B). §0
  "the gain is gone (1.7–2.5)": 1.7 is still below M-280's 1.9 even nominally; "gone" is too strong (and see MJ1).
- m4. Sourcing: MagnaLINK is not in `beads_vendors.md` and §8 gives "vectorlabs.com product page" without a URL;
  add https://vectorlabs.com/products/magnalink-streptavidin-mag-beads-2-8-m/ and note that the vendor's
  comparison is against an unnamed bead, the two free-biotin figures (≥ 10 / ≥ 12 nmol/mg) and the covalent
  SoluLINK streptavidin layer. 11× streptavidin per mg at the same size means a 3D layer with mostly free
  streptavidin when coated at 10 µg/mg — the rel upper bound 3 covers it, but say so in §3.
- m5. micromod 08-56-104: only a 2010 datasheet is cited; current orderability is unconfirmed. Add "availability
  UNVERIFIED; ask micromod" before it enters the bench test.
- m6. Bench-test size is not stated: 5 bead arms × 3 preparations (capture, non-immune, quenched) + 2 BSA-free arms
  + empty retainer, n ≥ 5 each, ≈ 90 runs in one cell. State the run count and the time, or prioritise (e.g.
  quenched-bead arms only for M-280 and the winner).
- m7. The script's edge check covers candidates only, not the variants (MagnaLINK variants pick 0.5×; fine now, but
  the check should include them).

## Answers to the three questions
1. The `load` term is a fair idea but is double-counted in the MC (MJ1) and applied unevenly (m1). Its nominal use
   and the values 0.3 / 0.4 / 3 are reasonable judgements; the covalent site factor 0.7 is a declared judgement
   bracketed by 1/3 and 1, acceptable.
2. "Small lever, no bead reaches 1 pg/mL", "cluster of four at 1.8 against 1.9", "keep M-280" follow from the
   nominal numbers and survive the fixes. The MagnaLINK sentence and the brush median do not (MJ1). The bench
   decision rule is inconsistent with the predicted effects (MJ2).
3. No missing candidate or source error found that would change the recommendation; MagnaLINK and micromod claims
   check out.

VERDICT: not converged
- MJ1: MC double-counts `load` (brush, micromod SA, MagnaLINK high-load variants); fix one line, rerun, update §0/§4/§5.
- MJ2: bench decision rule (≥ 1.5× lower total blank) is unreachable by the predicted effects and blind to
  capture-driven gains; restate on an LOD proxy or the bead-attributable blank.
Both fixes are mechanical; the recommendation (keep M-280; test M-270, MagnaLINK incl. 3× antibody, PEG-COOH 10 µm)
should stand, with MagnaLINK at high load as the strongest challenger.
