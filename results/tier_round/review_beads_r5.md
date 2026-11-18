# Review round 5 (convergence check) — docs/35 Revision E (tier-2 capture beads)

Reviewer: independent. Date 2026-11-18. Ran `python scripts/tier_round/tier2_beads.py --quick` (rc 0; four checks
pass; nominals as committed). Ran a mutated scratch copy (`base = pset(ps, dict(c, rel=1))`, i.e. `load` applied
in the reference bed and again in the sampled factor): rc 1, the new check FAILS. Own simulation of the bench rule
in the scratchpad (`rule_sim.py`, 40 000 trials per case). No repo file edited.

## 1. Round-4 findings — verification

| R4 item | Status |
|---|---|
| MJ1 bench rule | Rewritten as (mean blank × pooled CV) / (net signal per pg/mL of a 10–30 pg/mL standard), 1.3× threshold, confirmation set of n = 5. Rule now works (see §2); the resolvability wording is still too strong (m1). |
| m1 LodeStars | Named in §0 and §5 item 1 with median 7.1, P 0.79 / 0.68; matches json (1.934; 7.08; 0.793; 0.676). Resolved. |
| m2 tautological check | Check now compares each candidate's sampled `_pb` with M-280's draw × (φ·load + (1−φ)·rel). Mutation test: double-counted `load` makes it fail (LodeStars, brush, micromod SA have load ≠ 1). Resolved. Variants are covered only by the key check (m5). |
| m3 caption | `tier2_beads.md` §2 caption now "(φ·load + (1 − φ)·rel)"; docs/35 §3 lists LodeStars 0.7. Resolved. |
| m4 test size | 23 arms × 5 = 115 runs plus confirmation set. Resolved (but see m4 below on the BSA-free arms). |
| m5 vendor note | `beads_vendors.md` MagnaLINK row: 750 vs 60 pmol/mg (113 vs 10 µg/mg), 0.90 nmol/mg labelled as free biotin, $369 per 1 mL, 4 biotins per IgG. Arithmetic consistent (60 pmol × 150 kDa ≈ 9 µg). Resolved. |
| m6 r4 file | Filed. Status line now cites r5 (file this report). |

Numbers: §0, §4 and §5 match `tier2_beads.json` (n = 2000) — cluster 1.835/1.835/1.803/1.822 vs 1.899; medians
7.75/7.99/6.98/7.40; P 0.66/0.54/0.83 (0.65)/0.60 (0.72); MagnaLINK 3× variants 1.90/7.57/0.56, 1.69/6.78/0.95,
2.45/10.3/0.01, 1.40/5.72/1.00; ceilings 1.03 and 1.55. M-280 reproduces docs/34 (1.899 / 7.871).

## 2. Statistics of the new rule (own check)

Model: per arm n = 5 blanks and n = 5 standards, normal noise; blank CV 0.15 (docs/30 T2-1 criterion); standard
CV 0.10 or 0.15; net signal at concentration C = 3·CV_b·C/LOD in blank units (LOD 1.9 = model nominal, 7.9 = model
median, i.e. weak signal). Challenger effect split equally between blank and slope. Note: the pooled CV is the same
for all arms and cancels in every ratio — the rule is in effect mean blank / slope.

| C, LOD | SD of ln(proxy ratio) | null: P(>1.3) single | any of 5, stage 1 | false switch after confirmation (5 challengers) | true 1.3×: confirmed | true 1.5× | true 2× |
|---|---|---|---|---|---|---|---|
| 30, 1.9 | 0.13–0.15 | 0.02–0.04 | 0.11–0.20 | 0.002–0.010 | 0.25 | 0.68–0.75 | 1.00 |
| 10, 1.9 | 0.16–0.19 | 0.05–0.09 | 0.24–0.36 | 0.014–0.036 | 0.25 | 0.61–0.68 | 0.98–1.00 |
| 30, 7.9 | 0.18–0.21 | 0.08–0.11 | 0.32–0.45 | 0.028–0.061 | 0.25 | 0.59–0.64 | 0.98–0.99 |
| 10, 7.9 | 0.32–0.39 | 0.21–0.24 | 0.68–0.75 | **0.19–0.26** | 0.25 | 0.45–0.49 | 0.85–0.91 |

Reading: the blank-mean term alone has SD 0.095 (reviewer 3's statement is right for blank means), but the slope
term dominates; ln 1.3 = 0.26 is 0.7–2 SD of the proxy ratio, not "resolvable". Because the threshold equals the
effect, a true 1.3× gain passes stage 1 in 50 % and is confirmed in 25 % at any n. The confirmation run does
control false switches across 4–5 challengers (≤ 6 %) **with a 30 pg/mL standard**, but not at 10 pg/mL if the
signal is as weak as the model median (19–26 %). n per arm for SD(ln ratio) ≤ 0.105 (1.3× detected at one-sided
α 0.05, power 0.8): ≈ 13 (30 pg/mL, nominal signal), ≈ 20 (10 pg/mL, nominal), ≈ 30 (30 pg/mL, weak), > 40 (10 pg/mL,
weak). Practical consequence: at n = 5 the rule safely keeps M-280 unless a challenger is ≥ ~1.5× better; this is
fit for the decision (the model's predicted gains are mostly < 1.3×, the default is the safe one), so not major.

## 3. Findings

No major finding. Recommendation, cluster and headline numbers are unchanged and supported.

Minor:
- **m1. §5 still overstates resolution and allows the weak end of the standard.** "a 1.3 × difference of means is
  resolvable at n = 5 (reviewer 3)" is true of blank means only; the proxy ratio has SD 0.13–0.39 in ln. Fix: fix the
  standard at 30 pg/mL (or 30–100, inside the 1400 pg/mL linear range), and state what n = 5 delivers: false switch
  across five challengers ≤ ~6 %, a true 1.5× confirmed in ~0.6–0.75, a true 1.3× in ~0.25; resolving 1.3× needs
  n ≈ 13–30 per arm.
- **m2. Confirmation set:** say that M-280 is re-run in the same randomised block (otherwise the second ratio reuses
  stage-1 M-280 data and the two stages are not independent).
- **m3. Controls for the covalent PEG-COOH arm:** "non-immune biotinylated F(ab')₂" and "biotin-quenched beads" do not
  apply to a bead without streptavidin; use non-immune F(ab')₂ coupled covalently and a bead blocked without antibody.
- **m4. §6 vs §5:** §6 makes the BSA-free arm the user's choice, §5 counts it in the 23 arms / 115 runs; reconcile.
- **m5. Check scope:** the `_pb` identity is checked for candidates only; variants only for keys. Low impact (a
  global regression is caught through the load ≠ 1 candidates); extend to variants or say so.
- **m6. Nits:** §4 row "the same, sites 1" has best amount 0.75×, not half the beads; the pooled CV cancels in the
  ratio (say the rule compares mean blank / slope); the status line cites r5 — file this report.

## 4. Would anything change the recommendation, the cluster or a headline number by > 10 %?

No. Keep M-280; test M-270, MagnaLINK (incl. 3× antibody), micromod PEG-COOH 10 µm, optionally LodeStars SA; no bead
reaches 1 pg/mL. The bench rule can decide (false switches controlled with a 30 pg/mL standard); its stated
resolution is optimistic (m1).

VERDICT: converged
- m1 resolvability wording and the 10 pg/mL end of the standard (text; 30 pg/mL fixes the false-switch rate)
- m2 re-run M-280 in the confirmation block
- m3 controls for the covalent arm
- m4 BSA-free arm: §5 vs §6
- m5 check covers variants by keys only
- m6 nits (0.75× row, CV cancels, r5 file)
