# Review round 1 — docs/35 (capture beads for the tier-2 cell)

Reviewer: independent agent, 2026-11-18. No repo file edited. Scratch check script:
`/tmp/claude-0/-home-user-ELISA/3328588a-ee96-55c3-9466-68b6d8fffc81/scratchpad/chk.py`.

## What was checked

- Ran `python scripts/tier_round/tier2_beads.py --quick` (8 s). Every row of the docs/35 §4 table matches
  `results/tier_round/tier2_beads.md` (n = 2000): nominal values exactly, and medians within the expected MC noise
  at n = 200. The M-280 row reproduces docs/34 (1.9; 7.9 [0.96–93]). Diagnostics confirmed: capture 0.652,
  k_r 4.23e-6 m/s, k_m 1.04e-4 m/s. The §1 blank shares (33/24/5/38 %) also match. The Rissin cross-check
  arithmetic (6.5e-4 against 4.4e-4 per µm²) is right.
- `combine` reproduces the stated bed factors. For example M-270: 2 × exp(∓hypot(ln 3, ln 2)) gives 0.55 and
  25.6.
- Code paths in `tier2_cell.cell_design` and `tierkit.evaluate_bed` were followed. The bead diameter does
  propagate to five things: the retainer (membrane below 7 µm, screen alone above it), the bed length, the empty
  bore above the bed (`L_free`, which only moves ≤ 3.8 mm² of the 27 mm² upstream area), k_m (Wilson–Geankoplis)
  and the Kozeny–Carman Δp. Carry-over uptake scales with bed area. None of the "ignored effects" asked about in
  item 1 is ignored outright. The specific gaps are listed below.
- Sources fetched this session:
  - Rissin 2010 (PMC2919230): full text.
  - Chang 2012 (PMC3327511): full text.
  - Thermo M-270 FAQ page (opened; it was not 403).
  - Thermo trial-kit manual MAN0015762: PDF text extracted.
  - Agilent LodeStars brochure 5991-1336EN: PDF text extracted.
  - micromod data sheets 08-56-104 and 08-19-104: PDFs.
  - Hu 2024 (PMC11617200): full text.
  - Chen 2009 (PMC2891774): full text.
  - Yang 2009 (PubMed metadata).
  - Hua 2014 (PMC4245390).
  - MagPlex specifications: search only.

## Findings

### Major

**M1. The brush's rank 2 (§0, §4, §5) is not robust. It rests on treating capture-layer NSB as removable by the
bead surface.**
- Location: docs/35 §0 para 3, §4 brush row, §5 item 2; `tier2_beads.py` `pset`/`combine`.
- Evidence: the model multiplies the whole bead NSB by the bead factor (brush 0.2 × M-280). The study's own key
  source, Chang 2012 [V this session: "all of the background signals seem to arise from the interaction of the
  labeling reagents with the capture antibodies"], says that part is not set by the base surface. I split the
  M-280 bead NSB into a share φ on the capture layer (same for every bead per unit bead area) and (1−φ) scaled by
  the bead factor. Best-amount nominal LOD (pg/mL):

  | φ | M-280 | M-270 | Brush | PEG-10 |
  |---|---|---|---|---|
  | 0 (the model) | 1.90 | 1.69 | 1.53 | 1.74 |
  | 0.5 | 1.90 | 1.79 | 2.19 | 2.18 |
  | 0.8 | 1.90 | 1.86 | 2.53 | 2.43 |

  At φ = 0.5 the brush is worse than the current M-280, because its gain needs 3× the beads and so 3× the
  capture-layer NSB. The same happens to PEG-10. The site factor of the brush (covalent, 0.4) is also unsupported.
  Hu 2024 states that POEGMA's hydroxyl ends make covalent coupling difficult, and it immobilises the antibody by
  vacuum entanglement in a "porous" brush. Loading fell with thicker brushes, which are the ones that foul less.
- Fix:
  - Add a capture-layer floor parameter φ (e.g. 0.5, range 0.1–0.9, UNVERIFIED; it is not separated in any
    source) to `pset`, scaling with bead area. Re-run the ranking with it.
  - State in §0 and §5 that the brush (and PEG-10) gain disappears for φ ≳ 0.3–0.5.
  - Give the brush its own site factor (e.g. 0.3, 0.05–1, entanglement) rather than "covalent".
  - Rephrase "the only bead with a larger predicted gain" as conditional on φ being small.

**M2. The case for M-270 rests on "no BSA", but the project's protocol puts BSA on every bead, and the proposed
bench test removes the difference by design.**
- Location: docs/35 §0 para 2, §3 bullet "Vendor", §5 bench test.
- Evidence:
  - docs/30 §2.1 (lines 121, 124, 137) re-blocks the beads in IgG-free BSA. The conjugate sits in wash buffer
    with 1 % IgG-free BSA. The bench test of §5 blocks all three beads "in IgG-free BSA".
  - The vendor's reason for M-270 [V this session, Thermo FAQ] is background "caused by nonspecific binding to the
    BSA on the bead surface". With BSA present on all beads that argument no longer separates them.
  - What remains is the base hydrophilicity, and the evidence for it is weaker than stated. The 120° contact angle
    (a1) was measured on M-280 *Tosylactivated*, not on M-280 Streptavidin. The Thermo trial-kit manual [V this
    session] describes all its streptavidin Dynabeads as having "a streptavidin monolayer covalently coupled to the
    hydrophilic bead surface". That contradicts the FAQ's "M-280 = hydrophobic".
  - The capacities are equal per mg, and so per area: about 10 µg biotinylated antibody/mg for both, with the same
    6–7×10⁸ beads/mL at 10 mg/mL [V manual]. So M-270 versus M-280 is genuinely a coin-flip on paper.
- Fix:
  - State that the protocol's BSA nullifies the vendor's stated mechanism.
  - Lower the confidence of the 0.67 factor (e.g. 0.8, 0.4–2).
  - Change the recommendation to "keep M-280 as built; M-270 and LodeStars SA in the blank-bed test". Do not
    switch the first choice now. Alternatively keep "drop-in" but say plainly that the expected gain is
    indistinguishable from zero.
  - Run the bench test in two arms: (a) IgG-free BSA block as in docs/30, and (b) each bead's protein-free or
    as-supplied state with a BSA-free conjugate diluent (e.g. casein-free/PVA or Tween only, UNVERIFIED). Otherwise
    it cannot show the effect the vendor describes.

**M3. Citation errors and over-tagged claims (CLAUDE.md sourcing rule).**
- Location: docs/35 §0, §2 table, §3, §8; `beads_nsb_evidence.md` b10; `beads_vendors.md` §0.
- Evidence:
  - (a) "Lin P et al. 2024" is wrong. PubMed 39640065 / PMC11617200, doi:10.3389/fbioe.2024.1462203, has first
    author **Hu J** (Hu, Zhang, Shao, Wang; Johns Hopkins). `beads_vendors.md` R22 is right and docs/35 §3/§8 and
    the evidence note b10 are wrong.
  - (b) Hu 2024 is cited for "F(ab')₂ into the brush" (§2), but the paper uses physical entanglement, not
    covalent coupling (see M1). Its NSB test is FITC-BSA at 1 mg/mL, not an IgG conjugate. Its LOD parity comes from
    a proximity-extension readout, which suppresses NSB background by design, and its MagPEA buffer contains
    1 % BSA. So "no blocking" applies to the bead only.
  - (c) docs/35 §0 states that Rissin 2010 used "covalently coupled capture antibody and SuperBlock T-20 [V, full
    text]". In the full text the beads were "prepared according to the manufacturer's instructions". EDC/NHS
    appears only in the materials list, and SuperBlock is used only in the DNA-bead SβG experiment ("in Superblock
    containing 0.05% Tween-20 for 5 h"). No blocking of the protein-assay beads is described. Covalent attachment
    is stated in Chang 2012 [V: "covalently attached to 2.5-µm diam., carboxyl-terminated paramagnetic beads
    (Varian)"]. SuperBlock as the bead blocker is UNVERIFIED. The same applies to the LodeStars Carboxyl row's
    "SuperBlock-type block (the Rissin 2010 surface)".
- Fix:
  - Correct Lin → Hu J et al. 2024 everywhere.
  - Describe Hu's immobilisation and test conditions correctly.
  - Attribute "covalent" to Chang 2012 [V] (Rissin: inferred from EDC/NHS in the materials) and mark the
    SuperBlock blocking UNVERIFIED.

### Minor

**m1. The MyOne C1 row uses the 1 µm membrane, which does not retain 1 µm beads.**
- I scaled the docs/34 hydraulics to a 0.2 µm track-etched membrane (3×10⁶ pores/mm², UNVERIFIED). Its Δp at
  80 µL/min is about 5.1 bar, and the stack push is 1.53 N against the 0.69 N washer-lift limit. So C1 fails even
  at 1× the beads.
- A 0.4–0.45 µm membrane is marginal (≈ 0.63 N). It also has about 2× the pore-wall area of the 1 µm membrane,
  which adds retainer NSB.
- Fix: mark the C1 row infeasible in this cell, or compute it with a 0.4 µm membrane (area and Δp). "1 µm beads
  equal M-270" (§0) should say "on paper, with a retainer that does not pass the washer check at 0.2 µm".

**m2. LodeStars 2.7 Streptavidin is not shown to be "equal" in capture sites.**
- The brochure [V this session] gives biotinylated IgG > 5.0 µg/mg. Thermo gives about 10 µg/mg for M-280 and
  M-270 at a similar area per mg.
- Capture is reaction-limited (k_r ≪ k_m), so the site density matters as much as the NSB. If LodeStars SA
  carries about half the antibody per area, its LOD is worse than M-270's.
- Fix: give LodeStars SA a site factor of e.g. 0.7 (0.5–1, UNVERIFIED: brochure minimum spec), or state that
  "equal" assumes equal loading. The ranking "M-270 or LodeStars" then becomes "M-270, then LodeStars".

**m3. The site factors are inconsistent across the streptavidin beads.**
- Spherotech SVP-100-4 and the 5 µm silica get "sa" = 1 (0.4–1). The micromod SA 10 µm gets 0.4 because its
  streptavidin density is measured (≈ 38 ng/cm², confirmed from 200 ng/mg × 1.7×10⁶/mg). Spherotech publishes no
  capacity [S-R17], and passively coated polystyrene is likely sub-monolayer too.
- Fix: give SVP and silica the `sub_sa` range, or a wide (0.1–1) one.

**m4. The covalent site factor is a new UNVERIFIED value while the project already has one.**
- `chem.antibodies.oriented_vs_random_capacity_gain` = 3 (1.5–…) exists in params/chemistry.yaml. 0.4 (0.15–0.8)
  is close to 1/3, but use, or cite, the existing parameter.

**m5. The anchor is inconsistent.**
- §3 sets M-280 = 1.5 × the Rissin surface but keeps M-280's bed factor at 3. That implicitly redefines the
  packed-bed (non-chemistry) part as 2 for the Rissin surface.
- The ratios and ranking are unaffected, but the absolute "1.9 → 1.7" depends on this choice.
- Also, M-270's relative range (0.33–2) divides by the M-280 *central* value only, so it ignores M-280's own
  1–5 range.
- Fix: state the anchoring choice. Optionally report P(M-270 LOD < M-280 LOD) from paired draws, which is the
  decision-relevant number, instead of "inside the spread".

**m6. Retainer and bore descriptions.**
- docs/35 §4 says "the 2.5 mm bore". The bed bore is 0.5 mm in diameter and 2.5 mm long (`BED_D`,
  `INLET_FLOOR`).
- The 5 µm silica is given the 1 µm membrane, but a 2–3 µm track-etched membrane would retain it with less
  pore-wall area. The same holds for a 6.5 µm bead (m9).
- The membrane is 1.6 of the 4.85 mm² retainer area, so this is a small effect, but it favours ≥ 5 µm beads.

**m7. Chen 2009 is over-applied.**
- Verified: 0.004 → 4.7×10⁻⁴ non-target molecules/nm², S/N 3.1 → 30.7.
- However, the comparator is bare, unblocked organosilica with physisorbed IgG, not a blocked bead. The "≈ 8×"
  is therefore not a gain over a blocked bead.
- Fix: say so in §3.

**m8. The tags in the two research notes disagree.**
- `beads_nsb_evidence.md` a2 tags the Thermo FAQ statements "search snippets only: UNVERIFIED (pages not
  opened)". `beads_vendors.md` and docs/35 tag them [V R2].
- I opened the FAQ this session and the quoted statements are there, including "nonspecific binding to
  streptavidin".
- Fix: align the tags, and add the manual's "hydrophilic bead surface" wording as a conflicting vendor statement
  (see M2).

**m9. A candidate was missed: Luminex/Diasorin MagPlex.**
- MagPlex is a 6.5 µm carboxylated superparamagnetic microsphere: mode 6.5 ± 0.2 µm, CV < 5 %, density
  ≈ 1.10 g/mL [S, Diasorin product sheet via search].
- MagPlex-Avidin carries a covalently coupled deglycosylated avidin [S].
- It is the most widely used catalogue magnetic bead for low-background sandwich immunoassays, it is monodisperse
  and non-porous, and it sits just below the screen-alone limit. A coarse (≈ 3 µm) membrane would hold it.
- Neutral, deglycosylated avidin also answers the "streptavidin as NSB source" point that the Thermo FAQ raises.
- Fix: add it as a row (deglycosylated-avidin or covalent F(ab')₂ on COOH, d = 6.5 µm, f like LodeStars, site
  factor UNVERIFIED), or state why it was excluded.
- Lesser misses: Dynabeads M-450 (4.5 µm) and Sera-Mag NeutrAvidin (1 µm, already noted in the vendor file).

**m10. Physics that is not modelled but could matter (state as open points).**
- (a) The packed-bed factor 3 (1–30) is kept for 10–14 µm beads. Its physical part (stagnant zones, wash
  efficiency) plausibly falls with larger interstitial channels. This would favour SVP/PEG-10 and is unstated.
- (b) Streptavidin and avidin as NSB sources are given no factor. The covalent beads that remove streptavidin get
  the same 0.67 as the streptavidin beads. This is conservative, but it should be said.
- (c) The doc has no MC correlation statement. Results come from separate runs with the kit seed, so the
  comparisons are effectively paired. This is fine, but say it.

## Item-by-item answers

1. Method:
   - `combine` is a defensible log-quadrature product. Its weakness is the anchoring (m5) and that it treats the
     whole bead NSB as bead-surface NSB (M1).
   - The amount optimisation is fair: the washer-lift and bed-length limits do not bind at any reported optimum.
     This was checked against the §3 scan, where the first bracketed values lie beyond every chosen best.
   - The only wrong limit input is C1's membrane (m1).
   - The diameter does carry through to retainer type and area, `L_free`, k_m and Δp. The coarser membranes for
     5–6.5 µm beads are missing (m6).
   - The checked numbers agree with the output.
2. Physics: the capture-layer floor (M1), protocol BSA (M2), site density per bead (m2, m3), packed-bed physics
   with bead size (m10a) and streptavidin as an NSB source (m10b).
3. Sources:
   - Verified correct: Chang quote; Chen numbers; LodeStars part numbers (-1001/-1003/-1005/-1007;
     -0001/-0003/-0005/-0006/-0007) and capacities; micromod 08-56-104 (PEG-COOH, 10 µm, 1.7×10⁶/mg, 2010
     sheet) and 08-19-104 (200 ng SA/mg); Thermo capacities and BSA statements; Yang 2009; Hua 2014 quote.
   - Wrong or overstated: Lin → Hu; Hu's coupling; Rissin's SuperBlock (M3).
4. Missed candidate: MagPlex / MagPlex-Avidin (m9).
5. Conclusions:
   - "The bead is a small lever" follows from the model and is the most robust statement in the study.
   - The M-270 preference is weaker than presented, given that the protocol's BSA cancels the vendor argument (M2).
   - The brush's rank 2 does not survive a capture-layer floor (M1).
   - The bench test, as specified, cannot reveal the BSA-related difference (M2).

## Verdict

VERDICT: not converged. The open items:
- M1: the capture-layer floor reverses the brush and PEG-10 gains.
- M2: the M-270 rationale is nullified by the protocol's BSA, and the bench test design hides the effect.
- M3: citation errors (Lin → Hu, Hu's immobilisation method, Rissin's SuperBlock tagged [V]).

The headline "the bead is a small lever; settle with a blank-bed test" stands. The specific ranking and the
"switch to M-270 now" do not yet.
