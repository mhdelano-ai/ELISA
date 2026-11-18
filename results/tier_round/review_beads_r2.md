# Review round 2 — docs/35 Revision B (capture beads for the tier-2 cell)

Reviewer: independent agent, 2026-11-18. No repo file edited. Scratch scripts (import `tier2_beads.py`, nothing
written to the repo): `/tmp/claude-0/-home-user-ELISA/3328588a-ee96-55c3-9466-68b6d8fffc81/scratchpad/v1.py`
(amounts, covalent sites), `v2.py` (capture-layer share scaled by antibody load), `v3.py` (high-capacity bead).
Tags: [V] page/abstract read this session; [S] search summary only; UNVERIFIED judgement; Derived computed here.

## What was checked

- `python scripts/tier_round/tier2_beads.py --quick` (15 s): checks pass; `git status` clean afterwards.
- Every number in docs/35 §1 and §4 matches `results/tier_round/tier2_beads.md` (n = 2000); the M-280 row
  reproduces docs/34 (1.899 nominal, 7.871 median) exactly.
- Pairing (`paired_mc`): every candidate samples the same sorted key list with the kit seed; numpy's `triangular`
  consumes one uniform per draw whatever the bounds or the log/linear choice, so draws are comonotone across beads
  (also for the site parameter, whose bounds differ by bead). φ and rel come from a second stream (seed + 1), φ
  first, so φ is identical for every bead; rel for M-280 is fixed (no draw consumed) and φ + (1 − φ)·1 = 1, so M-280
  gets exactly the kit's sampling. The multiplication is applied to the *sampled* packed-bed factor, as intended.
  No bias in P(< M-280) from the mechanics. But see m1: for M-270, P(< M-280) = 0.66 is essentially
  P(rel < 1) of the judged prior, which is 0.67 for log-triangular (0.4, 0.8, 2) (Derived) — it restates the input.
- Round-1 findings: M1 (φ), M2 (BSA, recommendation, BSA-free arm), M3 (Hu 2024, Rissin), m1–m10 are applied as
  stated in docs/35 §7. One round-1 fix introduced an error (m4 → Peluso, finding M1 below).

## Findings

### Major

**M1. The covalent site penalty (1/3 from Peluso 2003) is a misreading of the source; with it removed a catalogue
low-fouling bead overtakes M-270.**
- Location: docs/35 §0 para 3, §3 sites table row "covalent F(ab')₂", §4, §5 item 3; `tier2_beads.py` `COV`.
- Evidence: Peluso et al. 2003, Anal Biochem 312:113, doi:10.1016/s0003-2697(02)00442-6 [V abstract, PubMed
  12531195]: "We compare randomly versus specifically oriented capture agents … Each comparison was performed using
  … two types of **streptavidin-coated** monolayer surfaces … up to 10-fold improvements over surfaces with randomly
  oriented capture agents." Both arms sit on streptavidin; the gain is site-specific (hinge-thiol) biotinylation
  over random (lysine) biotinylation. The project's capture reagent is Jackson 109-066-098, biotin-SP F(ab')₂
  (docs/30 line 119), i.e. lysine-NHS biotinylation — Peluso's *random* arm. Peluso therefore gives no ratio
  between random biotin on streptavidin and random EDC/NHS coupling; `oriented_vs_random_capacity_gain` does not
  separate these two. (It suggests instead that the kit's site factor 1 with `active_fraction_oriented` 0.85 is
  optimistic for every streptavidin bead alike — a project-wide point, neutral to the ranking.)
- Effect (Derived, n = 2000, paired, φ = 0.5):

  | Covalent sites (rel. to biotin-F(ab')₂ on SA) | PEG-COOH 10 µm best: nominal; median; P(< M-280) | M-270 Epoxy / LodeStars COOH |
  |---|---|---|
  | 1/3 (1/10–1/1.5) — docs/35 | 2.4 (×2); 10; 0.10 | 2.8; 12; 0.00 |
  | 0.7 (0.3–1), UNVERIFIED | 1.8 (×1.5); 7.0; 0.83 | 2.1; 8.4; 0.30 |
  | 1 (0.4–1), equal to SA | 1.62 (×1); 6.6; 0.98 | 1.83; 7.75; 0.66 (= M-270) |

  At any covalent site factor ≥ 0.7, the micromod PEG-COOH 10 µm (a catalogue bead) beats M-270 Streptavidin
  (1.83; 7.75; 0.66). This contradicts §0 "No bead on the market is predicted to lower the LOD … by more than a
  few per cent" and "No such catalogue product was found".
- Fix: drop Peluso as the source for covalent vs streptavidin; give covalent random F(ab')₂ its own UNVERIFIED
  factor relative to random biotin-F(ab')₂ on streptavidin (e.g. 0.7, 0.3–1; direct coupling to a PEG-COOH end can
  be lower or higher — state it), re-run, and rewrite §0/§5 conditionally: "PEG-COOH 10 µm with covalent F(ab')₂
  wins if its active loading per area is ≥ ~0.6 of the streptavidin beads' — unknown, test it". Add it (2 mg,
  catalogue) to the bench test. Flag the kit's 0.85 "oriented" active fraction for random-biotin F(ab')₂ as an
  open project-wide point (docs/08 style), not to be changed here.

**M2. Missed catalogue bead that the study's own logic favours: Vector Laboratories MagnaLINK Streptavidin Magnetic
Beads, 2.8 µm (M-1003).**
- Evidence [V vectorlabs.com product page, read this session]: "2.8 ± 0.2 microns", "<5% CV", "hydrophilic
  polymer–encapsulated (no exposed iron)", supplied "at 1% solids (10 mg/mL) in nuclease-free water with 0.05%
  sodium azide" (no BSA stated), free biotin "≥ 10 nmol/mg", biotinylated IgG "750 pmol/mg (113 µg/mg)" against an
  unnamed "similar 2.8 µm bead" at 0.90 nmol/mg and 10 µg/mg (the Dynabeads figures). Price $369 (unit size not
  stated). Porosity, bead count per mg and how the capacity per area is reached: UNVERIFIED (11× the Dynabeads
  value per mg at the same size implies a 3D streptavidin/polymer layer; vendor comparison not independently
  checked).
- Why it matters: docs/35 §0 says capture is reaction-limited and "a bead that carries fewer active capture sites
  per area loses signal one for one". The converse holds: more accessible sites per area allow fewer beads (less
  bead NSB) at the same capture. Model with a judged site factor (Derived; nominal, best amount over an extended
  grid 0.1–3×; φ = 0.5):

  | Sites (UNVERIFIED) | φ same per area: best, nominal; median; P(< M-280) | φ scaled with antibody load: nominal |
  |---|---|---|
  | 1.5 (0.5–3) | ×0.75, 1.64; 6.3; 0.98 | 1.75 |
  | 2 (0.7–5) | ×0.75, 1.52; 5.4; 1.00 | 1.73 |
  | 3 (1–10) | ×0.5, 1.40; 4.9; 1.00 | 1.69 |

  Even with the capture-layer NSB scaled up by the antibody load, it is at least equal to M-270 and better at the
  median. The other 3 µm hydrophilic streptavidin beads (Polysciences ProMag 3 Series Streptavidin 86056 [S],
  ProMag HP Streptavidin 25508 — "A unique surface means low nonspecific binding in protein-based systems",
  capacity not stated [V polysciences.com]; Ocean NanoTech Mono Mag 3 µm MV3000, already in `beads_vendors.md`
  row 7 but neither modelled nor excluded in docs/35) would be modelled like LodeStars SA and do not change the
  ranking, but they should be listed.
- Also: the amount grid (0.5–8×) and the edge check (only 0.5×) cannot find a lower optimum for a high-capacity
  bead; extend the grid down to 0.1× and check both allowed edges.
- Fix: add MagnaLINK as a row (rel 0.8, 0.4–2; sites UNVERIFIED, e.g. 1.5, 0.5–3, with the ≥ 3 case as
  sensitivity), list ProMag 3 / ProMag HP / Mono Mag MV3000 in §2 (or exclusions), and put MagnaLINK into the
  blank-bed test with a capture check at 1 pg/mL and at a lower bead number (e.g. 5×10⁵).

### Minor

**m1. P(< M-280) for M-270 is the prior.** 0.66 ≈ P(rel < 1) = 0.67 of the judged distribution (Derived). State
it in §0/§4 ("the 66 % is our judgement of the surface, not a model output"). The recommendation (keep M-280,
test M-270) is defensible as neutral because nothing is ordered, but then say plainly that the choice is a
coin toss and buy both for the test.

**m2. Best-amount rows are compared with M-280 at 1×, but the objective (nominal) and the reported statistic
(median, P) disagree.** M-280 itself at 1.5×: nominal 1.97 but median 7.51 against 7.87 at 1×, P 0.65 (Derived,
`v1.py`); M-270 at 1.5×: median 7.24, P 0.73. So LodeStars SA at its best (median 7.6, P 0.66) "beats" M-280 only
through more beads — and on the table looks equal to M-270, which conflicts with §0 "M-270 is the only
candidate that comes out ahead". Fix: report P(< M-280) against M-280 at the same amount (or at its own
median-optimal amount), and note for docs/34 that the median prefers about 1.5×10⁶ beads (nominal prefers 1×10⁶).

**m3. Capture-layer NSB "same per area" is biased against low-load beads.** If the share φ scales with the
amount of capture antibody (it is the labelling reagent meeting the capture antibody, Chang 2012), low-load beads
improve (nominal best, Derived `v2.py`): brush 2.52 → 1.82, micromod SA 10 µm 2.79 → 2.39, LodeStars SA
2.07 → 1.93, MagPlex 2.08 → 1.94, SVP 2.18 → 2.04. For covalent beads with full protein load but 1/3 active the
per-area assumption is right. No catalogue ranking changes, but the brush ties M-270 under this reading; add it as
a sensitivity row and soften "why the brush is worse" in §0.

**m4. Bench test cannot resolve the predicted differences and the φ control is confounded.**
- n ≥ 5 per arm detects a blank difference of roughly ≥ 1.8 × the run-to-run CV (two-sided, 80 % power,
  Derived); the model predicts 4 % between M-270 and M-280. State that the test can only find large (≥ 1.5–2×)
  differences, and decide in advance that otherwise M-280 stays.
- "Without capture antibody" leaves bare streptavidin exposed (and free biotin pockets), so the difference is not
  the capture-layer share. Use the non-immune biotinylated normal goat F(ab')₂ beads the project already plans
  (docs/30 §4.2 step 1, docs/30 line 298) as the φ control, plus biotin-quenched beads without antibody.
- Randomise the arm order in the one cell, use a fresh retainer per run (the retainer carries 24 % of the blank),
  and include the M1/M2 beads (PEG-COOH 10 µm with covalent F(ab')₂; MagnaLINK).
- Say that the test comes after the two project-wide substrate questions (C1, C5 of docs/30 §2.6 / CLAUDE.md).

**m5. The ceiling "1.0 with 4× the beads" sits at the edge of the allowed amounts** (6× fails the limits; LOD is
flat 1.0 from 3× to 8×). §4's "neither limit binds at any chosen amount" is true for the candidates only; say the
ceiling is limit-bound.

**m6. Source details.**
- LodeStars 2.7 Streptavidin: the Agilent store listing for PL6727-1001/-1005 gives biotinylated IgG
  "> 3.6 µg/mg" (search summary [S]; page 403 here), lower than the 2016 brochure's "> 5.0 µg/mg" [S, Wagner Munz
  copy]. The site factor 0.7 (0.5–1) may be optimistic; widen to 0.5 (0.35–1) or note the conflict.
- MagPlex-Avidin: the Luminex further-manufacturing sheet [V PDF text] says "deglycosylated avidin-coupled magnetic
  polystyrene microparticles", supplied at 2.5×10⁶ beads/mL [S]; the 6.5 µm size is not on that sheet (stays [S]).
  The best amount (2.8×10⁵ beads) needs about 0.11 mL of stock — feasible, state it.
- Hucknall 2009: confirmed [V PMC6516072]: IL-6 LOD 100 fg/mL on POEGMA vs 10 pg/mL on nitrocellulose, in undiluted
  FBS; capture antibody printed and "noncovalently absorb[ed] into the 100 nm thick polymer brush". docs/35 says
  "blocked nitrocellulose" — blocking of the comparator not checked by me; say "nitrocellulose" unless verified.
  The non-covalent absorption supports the brush site treatment.
- M-270 Epoxy NSB claim confirmed [V thermofisher.com/order/catalog/product/14301]: "nonporous, hydrophilic, pH
  neutral beads", "extremely low nonspecific binding of proteins and dyes", "typically 5–10 μg IgG per milligram";
  docs/35 tags it [S R9] — can be upgraded to [V].
- Peluso 2003: see M1; docs/35 §8 lists it only as "as in the file" — cite doi:10.1016/s0003-2697(02)00442-6 and
  what it compares.

## Answers to the questions asked

1. Model: pairing correct; φ/rel applied correctly to the sampled factor; M-280 exactly the kit; no mechanical
   bias in P. φ-per-area is a judgement that penalises low-load beads (m3). Best-amount search: grid too coarse at
   the low end and nominal-vs-median objective mismatch (M2, m2). Numbers in docs/35 match the output.
2. Overreach: §0 "no bead on the market … more than a few per cent" and "no such catalogue product" do not
   survive M1 and M2. "Keep M-280" is neutral but should be stated as a coin toss on a judged prior (m1). The bench
   test is useful but underpowered for the predicted effects and its φ control is confounded (m4).
3. Missed beads: MagnaLINK 2.8 µm (high capacity, hydrophilic polymer, no BSA) changes the ranking under the
   study's own logic; ProMag 3 / ProMag HP / Mono Mag 3 µm should be listed. No catalogue PEG-, brush- or
   zwitterion-surface bead with a full streptavidin layer was found by me either [S].
4. Spot checks: Peluso (misapplied), MagPlex (avidin [V], size [S]), M-270 Epoxy (claim [V]), Hucknall (numbers
   [V]), LodeStars (capacity now > 3.6 µg/mg [S]).

VERDICT: not converged
- M1: covalent site penalty from Peluso 2003 misapplied; with a defensible value the micromod PEG-COOH 10 µm beats
  M-270 (nominal 1.6–1.8, median 6.6–7.0, P(< M-280) 0.83–0.98).
- M2: missed catalogue bead (Vector MagnaLINK Streptavidin 2.8 µm, ~11× biotin-IgG capacity per mg [V vendor
  claim]) that would beat M-270 under the study's reaction-limited logic.
The headline "the bead is a small lever; no bead reaches 1 pg/mL" still stands; the ranking and "no catalogue
bead does better than a few per cent" do not.
