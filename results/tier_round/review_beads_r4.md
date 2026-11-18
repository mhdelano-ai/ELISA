# Review round 4 — docs/35 Revision D (tier-2 capture beads)

Reviewer: independent, adversarial. Date 2026-11-18. Ran `python scripts/tier_round/tier2_beads.py --quick`
(rc 0, 24 s; all four checks pass; nominals identical to the committed output). Own script `power.py` in the
scratchpad. Re-read the MagnaLINK product page this session. No repo file edited.

## 1. Round-3 fixes — verified

- **MJ1 (load double-counted):** `paired_mc` now builds the base with `rel=1, load=1`; the sampled factor is
  `phi·load + (1−phi)·rel` applied once. Correct. Committed json (n = 2000) has the corrected values (brush 1.8; 7.4;
  0.60/0.72; MagnaLINK 3× variants 7.6/0.56, 6.8/0.95, 10/0.01, 5.7/1.00; micromod SA 13; 0.04).
- **New check** passes, but it is tautological (see m2).
- **LodeStars load 0.7:** in CANDIDATES and §3; nominal 2.0 → 1.9 at 1.5×, median 7.1, P 0.79 / 0.68.
- **Bench rule on an LOD proxy at 1.3×:** present, but the power claim attached to it is wrong (MJ1 below).
- **Test size:** stated (≈ 90 runs), slightly under-counted (m4).
- **Numbers:** every number in §0, §4 (both tables) and §5 matches — nominals with the quick run, medians, 5–95 %,
  P(≤ 1), P(< M-280) and same-area P with `tier2_beads.json` (n = 2000): cluster 1.8 (1.835/1.835/1.803/1.822) vs
  1.899; medians 7.8/8.0/7.0/7.4 vs 7.9; P 0.66/0.54/0.83 (0.65)/0.60 (0.72); limits 1.6/1.5/1.3/1.0; φ rows;
  covalent 1/3 (2.4; 10; 0.10 / 2.8; 12; 0.00) and 1 (1.6; 6.6; 0.98); MagnaLINK and brush variants. Blank shares
  33/24/5/38 %. M-280 reproduces docs/34 (1.899 / 7.871).

## 2. Findings

### Major

**MJ1. The bench decision rule's power claim is wrong: the LOD proxy as defined cannot resolve 1.3× at n = 5, and
the "reviewer 3, Derived" attribution misapplies a statement about blank *means*.**
- Location: docs/35 §5, "for each capture bead, 3 × the blank SD divided by the net signal of the 1 pg/mL
  standard. M-280 stays unless a challenger lowers that proxy by at least 1.3 × (resolvable at n = 5 per arm,
  reviewer 3, Derived)."
- Evidence: reviewer 3's "~25 % resolvable at n = 5 if CV ≤ 15 %" is the standard error of a difference of two
  *mean* blanks (0.14/√5·√2 ≈ 9 %). The proxy uses the *sample SD* of 5 blanks (relative SE ≈ 1/√(2·4) ≈ 35 %) and
  the net signal of a 1 pg/mL standard, which at the model's nominal LOD (1.9) is only ≈ 1.6 blank SD (CV of a
  5-vs-5 net signal ≈ 40 %; at the median LOD 7.9 it is ≈ 0.4 SD and is ≤ 0 in 27 % of runs). Simulation
  (`power.py`, blank CV 0.14, n = 5, 20 000 trials): with two identical beads the proxy ratio exceeds 1.3 in
  31–37 % of tests; with a true 1.3× improvement it is detected in only ~50 % (25 % at the median LOD with the
  1 pg/mL standard). With four challengers, P(at least one false "win") ≈ 0.8. The rule would decide on noise, so
  the round-3 MJ2 is not actually resolved, and the bench step that the recommendation rests on ("test three
  challengers") cannot deliver its verdict as written.
- Fix: define the proxy on means: (mean blank of the arm × a pooled blank CV across all arms) / (net capture
  signal per pg/mL from a standard high enough to measure precisely, e.g. 10–30 pg/mL, in the linear range).
  Then 1.3× is resolvable at n ≈ 5 if the CV ≤ 15 % (reviewer 3's statement applies). Alternatively keep the SD
  but state the n it needs (order 100+ per arm) — i.e. not feasible. Drop "resolvable at n = 5, reviewer 3" from
  the current wording; state the false-positive rate across the 4–5 challengers or require a confirmation run of
  any winner.
- Does not change the bead recommendation or any model number; it changes the bench rule text.

### Minor

- **m1. LodeStars Streptavidin is out of the cluster and the recommended test on nominal rounding only.** Its
  median 7.1 and P(< M-280) 0.79 (0.68 at the same area) are better than M-270 (7.8; 0.66) and MagnaLINK (8.0; 0.54);
  only its nominal (1.93 vs 1.84, 5 %) is worse, and that gap is partly an artefact of comparing a mid-range site
  mode (0.7 in 0.5–1) with the kit's site mode at the top of its range (1 in 0.4–1). §5 item 2 places it with M-280.
  Not a change to the recommendation (it is offered as a user option in §6), but §5 should say that on median and
  P it ties the cluster, and why it is still left optional (lower stated capacity, 1.5× beads).
- **m2. The new check is tautological.** It evaluates `pset(ps, dict(c, rel=1, load=1))` itself, not the line in
  `paired_mc`; reverting the fix in `paired_mc` would still pass. Fix: have `paired_mc` return the base packed-bed
  value it used (`float(base.params[PB].value)`) and check that.
- **m3. Stale formula in the generated report:** `tier2_beads.md` §2 caption "Bed factor = … × (φ + (1 − φ) × rel)"
  omits `load` (the next paragraph mentions it). Write `(φ·load + (1 − φ)·rel)`. docs/35 §3's list of `load`
  values omits LodeStars 0.7 (it is in the sites table only).
- **m4. Test size under-counted.** 5 bead arms × 3 preparations (15) + 2 BSA-free + empty retainer + 5 standards
  = 23 arms × n = 5 ≈ 115 runs, not ≈ 90 (90 omits the standards). With MJ1's fix a second standard level may be
  needed.
- **m5. Sourcing slip in `beads_vendors.md` addendum (MagnaLINK row):** the competitor's "0.90 nmol/mg" is its
  *free-biotin* capacity, not biotinylated IgG; the competitor's IgG figure is 60 pmol/mg (10 µg/mg); price is
  $369 for a 1 mL unit (vendor page re-read this session). The vendor's IgG figure is for IgG with 4 biotins per
  molecule (degree of biotinylation of Jackson 109-066-098 not checked). The 113 vs 10 µg/mg used in docs/35 is
  correct, so no conclusion changes.
- **m6. Status line** cites `review_beads_r4.md`, which is not in the repo yet; add it when this report is filed.

## 3. Would anything change the recommendation, the cluster or a headline number by > 10 %?

No model issue found. The paired MC is now consistent; the nominal and MC numbers match the text; the claims of §0
("small lever", "no bead reaches 1 pg/mL", P(≤ 1) ≈ 0.06 for every bead, MagnaLINK at 3× antibody as the
widest-range challenger 1.4–2.5) are supported as stated and appropriately hedged as judgements. Keep M-280 and
test M-270, MagnaLINK (incl. 3× antibody) and PEG-COOH 10 µm with covalent F(ab')₂ stands. LodeStars (m1) is the only
cluster-boundary question and is within 5 % nominal.

VERDICT: not converged
- MJ1: bench decision rule — the SD-based LOD proxy with a 1 pg/mL standard cannot resolve 1.3× at n = 5
  (false-win rate ≈ 1/3 per challenger, power ≈ 0.5); the "reviewer 3, Derived" attribution is misapplied.
  Text-only fix (mean-based proxy, higher standard, or stated n); no model rerun needed.
- Minor m1–m6 as listed. The model side (recommendation, cluster, headline numbers) has converged.
