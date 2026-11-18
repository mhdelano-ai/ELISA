# 35 — Alternative capture beads for the tier-2 cell

Status: desk work, 2026-11-18, Revision B (after review round 1, §7). Follow-up to docs/34 (tier-2 flow cell with
the bed inside). Question from the user: which bead gives the lowest LOD, most likely through the lowest
non-specific binding (NSB) of the conjugate; iterate with an independent reviewer until the answer stops changing.
Nothing is ordered; docs/30 and docs/34 are not changed. Numbers from `scripts/tier_round/tier2_beads.py` →
`results/tier_round/tier2_beads.md` (Monte Carlo n = 2000, paired draws). Desk research behind §2–3:
`results/tier_round/beads_vendors.md` (vendors, about 20 products, references R1–R24) and
`results/tier_round/beads_nsb_evidence.md` (published NSB evidence, tables a–e). Review reports:
`results/tier_round/review_beads_r1.md` and following.
Tags: [V] read this session in the cited page or full text (by the research agents or the reviewer); [S] secondary
(search summary, distributor page, abstract only); UNVERIFIED not checked or a judgement; Derived computed here.

## 0. Summary

**No bead on the market is predicted to lower the LOD of the tier-2 cell by more than a few per cent; keep M-280
Streptavidin as built, and put Dynabeads M-270 Streptavidin (65305) beside it in a blank-bed test.** M-270 is the
only candidate that comes out ahead: nominal 1.9 → 1.8 pg/mL, median 7.9 → 7.8, lower LOD than M-280 in 66 % of
paired draws (§4). It is a drop-in (same size, capacity per area, coating protocol and retainer). The gain rests on a
judged factor (§3); on paper the two beads are close to a coin toss.

**Why the bead is a small lever in this cell (§1).** The beads carry about a third of the non-specific enzyme of
the blank; the line and empty bore above the bed (38 %), the retainer and washer hole (24 %) and the exit bore (5 %)
carry the rest. Part of the beads' own share sits on the capture-antibody layer, which every bead carries (Chang
2012: the background "seem[s] to arise from the interaction of the labeling reagents with the capture antibodies"
[V]). With half of it there (φ = 0.5, UNVERIFIED), a bead surface with no NSB at all would give 1.6 pg/mL at the
same area and 1.5 with 1.5 × the beads; only beads with no NSB of any kind, capture layer included, would reach
1.0 (with 4 × the beads). That is the ceiling of anything a bead can do here.

**Capture sites matter as much as NSB.** Capture is reaction-limited (k_r 4.2×10⁻⁶ m/s against k_m 1.0×10⁻⁴ m/s;
65 % captured at 1×10⁶ M-280), so a bead that carries fewer active capture sites per area loses signal one for one,
and buying it back with more beads brings the NSB back. That is why the covalent beads (LodeStars Carboxyl, M-270
Epoxy: a third of the oriented sites, Peluso 2003 via `chem.antibodies.oriented_vs_random_capacity_gain`) are worse
(nominal 2.8 at twice the beads), why the low-fouling beads with covalent or entangled antibody (micromod PEG-COOH
10 µm, an in-house POEGMA or carboxybetaine brush) are worse (2.4, 2.5), and why the 10 µm streptavidin beads are
worse. A low-fouling surface would only pay if it kept a full oriented streptavidin layer: with the sites of M-280,
a brush bead would give 1.65 and the PEG bead 1.6 (φ = 0.5). No such catalogue product was found.

**Corrections to docs/34 §0 and §3.** M-280 is not "the surface on which the project's non-specific rate is
defined". `chem.nsb.nsb_effective_rate_constant` comes from Rissin et al. 2010, who used 2.7 µm carboxyl magnetic
beads from Varian [V full text, doi:10.1038/nbt.1641]; capture antibody coupled covalently (stated by Chang 2012
[V]; in Rissin 2010 only through EDC/NHS in the materials list); the blocking of those beads is not described
(SuperBlock appears only for a DNA-bead experiment) [V reviewer]. The bead is most likely today's Agilent LodeStars
2.7 Carboxyl [S]. The model's `surface_factor_magnetic_beads` = 1 for M-280 is an assumption, not a definition.

## 1. Where the blank comes from in the docs/34 cell

Nominal model, M-280 cell (`tier2_beads.md` §1): non-specific enzyme = area × surface factor.

| Surface | Area (mm²) | Factor | Share |
|---|---|---|---|
| Beads (1×10⁶ M-280) | 24.4 | 3 (`ma.nsb.surface_factor_packed_bed`, 1–30, UNVERIFIED) | 33 % |
| Retainer (membrane, screen) and washer hole | 5.3 | 10 (`tr.nsb.surface_factor_frit`) | 24 % |
| Exit bore | 3.5 | 3 (`tr.nsb.surface_factor_lid`) | 5 % |
| Bore above the bed and the line upstream | 27.4 | 3 (`ma.nsb.surface_factor_tubing`) | 38 % |

The blank's variance is 95 % NSB variability (nominal), so the LOD follows the total non-specific enzyme. A bead
with a cleaner surface helps on its own share only, and allows more beads (more capture) at the same NSB.

## 2. Candidates

From the vendor survey (`beads_vendors.md`) and review round 1. Beads ≥ 1 µm, monodisperse, non-porous.

| Bead | Ø (µm) | Surface | Capture | Why considered | Tag |
|---|---|---|---|---|---|
| Dynabeads M-280 Streptavidin 11205D (current) | 2.8 | streptavidin on a tosyl-activated base; stock 0.1 % BSA; ≈ 10 µg biotinylated IgG/mg | biotin-F(ab')₂ | reference | [V R1, R2] |
| Dynabeads M-270 Streptavidin 65305 | 2.8 | streptavidin on a carboxylic-acid base; no BSA in the stock; ≈ 10 µg biotinylated IgG/mg, same beads/mg | biotin-F(ab')₂ | vendor's alternative where M-280's BSA gives background | [V R1, R2] |
| Agilent LodeStars 2.7 µm Streptavidin PL6727-1001 | 2.7 | streptavidin on the carboxyl polymer shell; "ultralow non-specific binding" (vendor); > 5 µg biotinylated IgG/mg (brochure minimum) | biotin-F(ab')₂ | the Rissin bead family with streptavidin | [V R5] |
| Luminex MagPlex-Avidin | 6.5 | deglycosylated avidin on a carboxylated magnetic microsphere, CV < 5 % | biotin-F(ab')₂ | catalogue bead of low-background bead immunoassays; neutral avidin | [S, reviewer] |
| Agilent LodeStars 2.7 µm Carboxyl PL6727-0001 | 2.7 | carboxyl | F(ab')₂ by EDC/NHS | the Rissin 2010 surface | [V R5]; identity [S] |
| Dynabeads M-270 Epoxy 14301 | 2.8 | epoxy; vendor claims very low protein NSB | F(ab')₂ covalent | no streptavidin, no BSA | [S R9] |
| micromod micromer-M PEG-COOH 10 µm 08-56-104 | 10 | PEG (length not stated) | F(ab')₂ covalent | only catalogue PEG-surface monodisperse bead ≥ 2 µm found; screen alone holds it | [V R10, 2010 data sheet; reviewer] |
| POEGMA or carboxybetaine brush on M-270 Amine (in house) | 2.8 | polymer brush | antibody entangled in the brush (Hu 2024) or coupled to it | best published low-fouling evidence | literature, §3 |
| micromod micromer-M Streptavidin 10 µm 08-19-104 | 10 | streptavidin ≈ 38 ng/cm² (≈ a tenth of a monolayer, Derived) | biotin-F(ab')₂ | magnetic, 10 µm, screen alone | [V R10; reviewer] |
| Spherotech SVP-100-4 (docs/34 fallback) | 10–14 | streptavidin on polystyrene, capacity not published | biotin-F(ab')₂ | the existing fallback | [V R16] |
| Streptavidin silica 5 µm, non-porous (Bangs CS01002 type) | 5 | silica | biotin-F(ab')₂ | hydrophilic alternative | [S R18] |

Not modelled: MyOne Streptavidin C1 and Sera-Mag SpeedBeads (1 µm): a 0.2 µm membrane that holds them fails the
docs/34 washer-lift check (stack push about 1.5 N against 0.69 N, reviewer's estimate) and a 0.45 µm one is
marginal, so they do not fit this cell; per area they are M-270 chemistry and would equal it. MyOne T1 (the M-280
chemistry at 1 µm). Porous silica (sicastar), Sepharose, agarose, POROS (internal area open to a 200–300 kDa
conjugate). TentaGel and PEG resins (swelling gels made for synthesis). Beads < 1 µm. Dynabeads M-450 (4.5 µm,
tosyl/epoxy, no expected gain over M-270). No catalogue zwitterionic bead was found [S].

## 3. Factors (all UNVERIFIED judgement unless tagged)

**What is known.** No paper compares the NSB of an antibody–enzyme conjugate across these beads under the same
conditions (`beads_nsb_evidence.md` §0). The anchors:

- Rissin 2010 [V] gives the project's rate; its blank (about 1 % active beads) checks against the model's rate
  (4×10⁻¹¹ m/s × 15 pM × 30 min = 6.5×10⁻⁴ /µm² against 4.4×10⁻⁴ /µm² measured; Derived).
- Chang 2012 [V]: background from the labelling reagents on the capture antibodies (above).
- Thermo [V R2, FAQ opened by the reviewer]: M-280 is "hydrophobic" and its background "might be caused by
  nonspecific binding to the BSA on the bead surface" (also "to streptavidin"); M-270 is the hydrophilic
  alternative. But the Thermo manual [V R1] calls every streptavidin Dynabead surface "hydrophilic", and the 120°
  water contact angle in the Dynal poster (a1) was measured on M-280 *Tosylactivated*, not on the streptavidin bead.
  **The project re-blocks every bead in IgG-free BSA and runs the conjugate in 1 % BSA (docs/30 §2.1), which removes
  the vendor's stated mechanism.** What is left between M-280 and M-270 is the base surface under the BSA.
- Brushes: carboxybetaine brushes show undetectable adsorption from plasma, also after antibody coupling (Yang 2009,
  abstract [S]); a POEGMA brush on glass gave an IL-6 LOD 100× below blocked nitrocellulose (Hucknall 2009 [V]); IgG
  adsorbs weakly on PEG already (Hua 2014 [V]); POEGMA grown on M-270 Amine beads beat serum blocking in a FITC-BSA
  test, no fold given, with the antibody entangled in the brush because the hydroxyl ends resist covalent coupling,
  and with a proximity-extension readout that itself suppresses background (Hu J et al. 2024 [V]); a PEG-3400 brush
  on organosilica beads cut non-target antibody binding about 8×, against bare unblocked silica, not a blocked bead
  (Chen 2009 [V]).

**How the model uses it.** The M-280 bed keeps the packed-bed factor of docs/34 (3, 1–30); this is the anchor, and
all other beads are stated relative to it. A share φ of M-280's bead NSB sits on the capture-antibody layer and is
the same per area for every bead: φ = 0.5 (0.1–0.9), not separated in any source. The rest scales with the bead
surface by `rel`. φ and `rel` are drawn independently of the kit's parameters (seed + 1), so every bead is compared
with M-280 on the same draws of everything else; P(< M-280) in §4 is the share of draws in which the bead wins.

| Surface | rel to M-280 (low–high) | Reason |
|---|---|---|
| M-280 Streptavidin (re-blocked in BSA) | 1 | anchor |
| M-270 Streptavidin, LodeStars Streptavidin and Carboxyl, M-270 Epoxy, MagPlex-Avidin | 0.8 (0.4–2) | hydrophilic base, but BSA on every bead in the protocol |
| micromod PEG-COOH | 0.5 (0.15–1.5) | PEG of unknown length, not a brush |
| Brush (POEGMA, carboxybetaine) | 0.25 (0.05–1) | flat-surface and bead evidence above; floor not known |
| Polystyrene streptavidin (Spherotech, micromod), silica | 1.3 (0.7–7) | no vendor surface finish, blocked in BSA |

Active capture sites (relative to the oriented monolayer of `chem.surfaces`):

| Capture | Sites (low–high) | Source |
|---|---|---|
| biotin-F(ab')₂ on M-280 or M-270 streptavidin | kit: 1 (0.4–1) | `tr.capture.site_factor_streptavidin_biotin`; equal capacity per area [V R1] |
| LodeStars Streptavidin | 0.7 (0.5–1) | brochure minimum 5 µg/mg against ≈ 10 for Dynabeads, similar area per mg (UNVERIFIED) |
| MagPlex-Avidin, Spherotech, silica | 0.7 (0.3 or 0.1–1) | capacity not published |
| micromod Streptavidin 10 µm | 0.4 (0.1–0.8) | about a tenth of a streptavidin monolayer (Derived) |
| covalent F(ab')₂ (LodeStars Carboxyl, M-270 Epoxy, PEG-COOH) | 1/3 (1/10–1/1.5) | 1 / `chem.antibodies.oriented_vs_random_capacity_gain` (Peluso 2003) |
| brush, antibody entangled | 0.3 (0.05–1) | loading falls with brush thickness (Hu 2024 [V]) |

Not in the model, stated here: the physical part of the packed-bed factor may fall for 10–14 µm beads (wider
channels, better washing), which would favour them; streptavidin and avidin as NSB sources get no separate factor
(the covalent beads that remove them get no credit); for 5–6.5 µm beads a coarser membrane (2–3 µm) would hold
them with less pore-wall area (the membrane is 1.6 of the 4.9 mm² of retainer, a small effect).

## 4. Model results

Docs/34 cell, only the beads changed; LOD in pg/mL (`tier2_beads.md` §2–4), φ = 0.5. "Best amount" = lowest
nominal LOD over 0.5–8 × the bead area of 1×10⁶ M-280, within the washer-lift check of docs/34 at 80 µL/min and the
bed bore (0.5 mm × 2.5 mm); neither limit binds at any chosen amount.

| Bead | Same area: nominal; median [5–95 %]; P(≤ 1); P(< M-280) | Best amount (beads) | Best: nominal; median [5–95 %]; P(≤ 1); P(< M-280) |
|---|---|---|---|
| M-280 Streptavidin (current) | 1.9; 7.9 [0.96–93]; 0.06; — | 1× (1.0×10⁶) | same |
| **M-270 Streptavidin** | **1.8; 7.8 [0.95–89]; 0.06; 0.66** | 1× (1.0×10⁶) | same |
| LodeStars 2.7 Streptavidin | 2.1; 8.0 [0.98–94]; 0.05; 0.36 | 1.5× (1.6×10⁶) | 2.1; 7.6 [0.97–85]; 0.05; 0.66 |
| MagPlex-Avidin 6.5 µm | 2.1; 9.1 [1.1–110]; 0.04; 0.08 | 1.5× (2.8×10⁵) | 2.1; 8.4 [1.0–100]; 0.05; 0.30 |
| Spherotech SVP-100-4 | 2.2; 14 [1.3–210]; 0.03; 0.02 | 1.5× (8.1×10⁴) | 2.2; 13 [1.3–190]; 0.03; 0.04 |
| Silica 5 µm | 2.3; 14 [1.4–210]; 0.03; 0.00 | 1.5× (4.7×10⁵) | 2.3; 13 [1.4–190]; 0.03; 0.01 |
| micromod PEG-COOH 10 µm, covalent | 2.9; 13 [1.3–180]; 0.03; 0.03 | 2× (1.6×10⁵) | 2.4; 10 [1.1–140]; 0.04; 0.10 |
| Brush on M-270 Amine | 3.3; 15 [1.3–230]; 0.03; 0.06 | 3× (3.0×10⁶) | 2.5; 10 [1.1–140]; 0.04; 0.19 |
| LodeStars 2.7 Carboxyl, covalent | 3.4; 15 [1.4–210]; 0.02; 0.00 | 2× (2.1×10⁶) | 2.8; 12 [1.3–170]; 0.03; 0.00 |
| M-270 Epoxy, covalent | 3.4; 15 [1.4–210]; 0.02; 0.00 | 2× (2.0×10⁶) | 2.8; 12 [1.3–170]; 0.03; 0.00 |
| micromod Streptavidin 10 µm | 3.0; 16 [1.6–250]; 0.02; 0.00 | 1.5× (1.2×10⁵) | 2.8; 15 [1.5–220]; 0.03; 0.01 |
| Bead surface with no NSB, capture layer kept | 1.6 | 1.5× | 1.5 |
| No NSB on the beads at all | 1.3 | 4× | 1.0 |

The M-280 row reproduces docs/34 §6.1 exactly (nominal and median; check in `tier2_beads.md` §0).

Sensitivity (nominal, best amount; `tier2_beads.md` §3 and a one-off run):

| Change | Result |
|---|---|
| φ = 0 (all bead NSB on the bead surface) | brush 1.8 (4×), M-270 1.8, PEG-COOH 2.0, M-280 1.9 |
| φ = 0.8 | M-270 1.9, every other bead ≥ 2.1 |
| brush with the sites of M-280 (1), φ 0 / 0.5 / 0.8 | 1.34 / 1.65 / 1.8 |
| PEG-COOH 10 µm with the sites of M-280, φ 0 / 0.5 / 0.8 | 1.42 / 1.62 / 1.72 |
| covalent beads or LodeStars Streptavidin with the sites of M-280 | equal to M-270 (1.8) |

## 5. Ranking and what would change it

1. **M-270 Streptavidin**: the only bead ahead of M-280 on paper, by a few per cent, at no cost in design or
   protocol. Not worth switching on paper; worth one arm of the blank-bed test.
2. **M-280 Streptavidin** (current), and LodeStars 2.7 Streptavidin if its loading per area matches Dynabeads.
3. Everything else is worse in this cell, mainly through fewer active capture sites.

The ranking turns only if (a) the capture-antibody layer carries little of the bead NSB (φ small) **and** (b) a
low-fouling bead keeps the capture-site density of a streptavidin Dynabead. Then a streptavidin layer on a PEG or
brush bead would give about 1.6 pg/mL — not a catalogue product, and still short of the 1 pg/mL target alone.

**Bench test (extends T2-1 of docs/30 and C-2 of docs/34; informational, not a gate).** Beds of M-280 and M-270
Streptavidin (LodeStars 2.7 Streptavidin optional), coated identically with biotinylated capture F(ab')₂, each also
without capture antibody; the docs/34 blank sequence (no analyte), n ≥ 5 per arm, in the same cell. Two blocking
arms: (a) IgG-free BSA as in docs/30; (b) no protein block, beads as supplied, conjugate in a BSA-free diluent
(e.g. buffer with Tween-20 or PVA, UNVERIFIED) — arm (b) is the only one that can show the BSA effect the vendor
describes. Readouts: blank charge and its SD per arm; the difference with and without capture antibody measures φ;
the bead share of the whole blank (beds against an empty retainer) tells whether the bead matters at all. Load a
1 pg/mL standard on each bead to confirm the capture fraction. A bead that lowers the blank by less than the
run-to-run SD is not worth the change.

## 6. Open points

- The line and bore above the bed (38 % of the nominal NSB) and the retainer (24 %) are larger levers than any bead;
  outside this question.
- Choice for the user: keep M-280 (recommended) or switch the first choice of docs/34 to M-270 Streptavidin; whether
  to add the BSA-free arm and LodeStars to the bench test.

## 7. Review and iteration

| Round | Reviewer verdict | Main findings | Resolution |
|---|---|---|---|
| Draft (Rev A) | — | Recommended switching to M-270 Streptavidin; brush second (1.5 pg/mL) | — |
| 1 | not converged: 3 major, 10 minor (`review_beads_r1.md`) | M1 capture-layer NSB treated as removable by the bead; brush site factor unsupported. M2 the protocol's BSA cancels the vendor's case for M-270; bench test could not show it. M3 Hu (not Lin) 2024, its immobilisation and test; Rissin's SuperBlock over-tagged. Minor: C1 retainer, LodeStars loading, inconsistent site factors, existing covalent parameter, anchor, "2.5 mm bore", Chen 2009 comparator, tags, MagPlex missed, unmodelled physics | All applied (Rev B): φ added and sampled; paired comparison; covalent sites from Peluso 2003; bead-specific sites; brush entangled 0.3; M-270 rel 0.8 (0.4–2); recommendation changed to keep M-280; BSA-free test arm; C1 not modelled; MagPlex added; citations corrected; physics not modelled listed in §3 |

## 8. Sources

Full reference lists with tags: `results/tier_round/beads_vendors.md` (R1–R24) and
`results/tier_round/beads_nsb_evidence.md` (its entry b10 names the 2024 POEGMA paper's first author wrongly as Lin;
it is Hu J). The ones used above:

| Ref | Source | Tag |
|---|---|---|
| Rissin 2010 | Rissin DM et al., Nat Biotechnol 28:595 (2010), doi:10.1038/nbt.1641, Methods | [V] full text |
| Chang 2012 | Chang L et al., J Immunol Methods 378:102 (2012), doi:10.1016/j.jim.2012.02.011 | [V] full text |
| Peluso 2003 | `chem.antibodies.oriented_vs_random_capacity_gain` in params/chemistry.yaml (3, 1.5–10) | as in the file |
| R1, R2 | Thermo Fisher Dynabeads trial-kit manual and FAQ pages for M-280 / M-270 Streptavidin (URLs in beads_vendors.md) | [V] |
| R5 | Agilent LodeStars brochure (2016) | [V] |
| R9 | Thermo Fisher M-270 Epoxy product page (Japanese, via search) | [S] |
| R10 | micromod data sheets (2010 copies) | [V] |
| R16, R18 | Spherotech SVP-100-4; Bangs CS01002 | [V]; [S] |
| MagPlex | Diasorin/Luminex MagPlex and MagPlex-Avidin product sheet (via search, reviewer round 1) | [S] |
| a1 | Trømborg et al., Dynal poster on MyOne beads (Thermo document) | [V] |
| Yang 2009 | Yang W et al., Langmuir 25:11911, doi:10.1021/la9015788 | abstract |
| Hucknall 2009 | Hucknall A et al., Adv Mater 21:1968, doi:10.1002/adma.200803125 | [V] |
| Hua 2014 | Hua B et al., Nat Methods 11:1233, doi:10.1038/nmeth.3143 | [V] |
| Hu 2024 | Hu J et al., Front Bioeng Biotechnol 12:1462203 (2024), doi:10.3389/fbioe.2024.1462203, PMID 39640065 | [V] |
| Chen 2009 | Chen et al., Langmuir 25:13510, doi:10.1021/la903148n | [V] |
