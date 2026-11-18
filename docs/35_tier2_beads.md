# 35 — Alternative capture beads for the tier-2 cell

Status: desk work, 2026-11-18. Follow-up to docs/34 (tier-2 flow cell with the bed inside). Question from the user:
which bead gives the lowest LOD, most likely through the lowest non-specific binding (NSB) of the conjugate; iterate
with an independent reviewer until the answer stops changing. Nothing is ordered; docs/30 and docs/34 are not
changed. Numbers from `scripts/tier_round/tier2_beads.py` → `results/tier_round/tier2_beads.md` (Monte Carlo
n = 2000). Desk research behind §2–3: `results/tier_round/beads_vendors.md` (vendors, about 20 products, tagged
references R1–R24) and `results/tier_round/beads_nsb_evidence.md` (published NSB evidence, tables a–e).
Tags: [V] read this session in the cited page or full text; [S] secondary (search summary, distributor page, abstract
only where noted); UNVERIFIED not checked or a judgement; Derived computed here.

## 0. Summary

**The bead is a small lever in this cell.** In the docs/34 cell with M-280 the beads carry about a third of the
non-specific enzyme of the blank (nominal); the rest sits on the line and the empty bore above the bed (38 %), the
retainer and washer hole (24 %) and the exit bore (5 %) (§1). Even beads with no NSB at all would take the nominal
LOD only from 1.9 to 1.3 pg/mL at the same bead area, and to 1.0 pg/mL with four times the beads (median 3.0
[0.55–34], P(LOD ≤ 1) 0.17). That is the ceiling of anything a bead can do here.

**Recommendation: Dynabeads M-270 Streptavidin (65305) as a drop-in for M-280, with Agilent LodeStars 2.7 µm
Streptavidin as its equal; settle the choice with a blank-bed test, not on paper.** Both are streptavidin beads on a
hydrophilic carboxyl surface without BSA, so the coating, retainer, cell and protocol of docs/34 stay as they are.
Model: nominal 1.9 → 1.7 pg/mL, median 7.9 → 7.1 (§4). The gain rests entirely on a judged NSB factor (M-270 two
thirds of M-280, UNVERIFIED); no paper compares conjugate NSB on these beads (§3).

**A low-fouling brush on the bead (carboxybetaine or POEGMA grafted in house) is the only bead with a larger
predicted gain** — nominal 1.5, median 5.6, with three times the beads — and it is a chemistry project, not a
product; its gain is limited by NSB on the capture antibody layer itself, which no bead surface removes (§3, §5).
Worth starting only if the blank-bed test shows that the beads dominate the blank.

**Covalent coupling (LodeStars Carboxyl, M-270 Epoxy) is worse in the model**, not better: random orientation is
taken to leave fewer active capture sites (0.4 of the oriented layer, UNVERIFIED), and buying them back with more
beads brings the NSB back (nominal 2.3 at twice the beads). 10 µm beads (Spherotech, micromod streptavidin, silica)
gain nothing; the micromod streptavidin bead is worse (sub-monolayer streptavidin). 1 µm beads (MyOne C1, Sera-Mag)
equal M-270 per area but need a retainer that is not designed.

**Correction to docs/34 §0 and §3:** M-280 is not "the surface on which the project's non-specific rate is defined".
`chem.nsb.nsb_effective_rate_constant` comes from Rissin et al. 2010, who used 2.7 µm carboxyl magnetic beads from
Varian with covalently coupled capture antibody and SuperBlock T-20 [V, full text, doi:10.1038/nbt.1641]; that bead
is most likely today's Agilent LodeStars 2.7 Carboxyl [S]. The model's `surface_factor_magnetic_beads` = 1 for
M-280 is therefore an assumption, not a definition.

## 1. Where the blank comes from in the docs/34 cell

Nominal model, M-280 cell (`tier2_beads.md` §1): non-specific enzyme = area × surface factor.

| Surface | Area (mm²) | Factor | Share |
|---|---|---|---|
| Beads (1×10⁶ M-280) | 24.4 | 3 (`ma.nsb.surface_factor_packed_bed`, 1–30, UNVERIFIED) | 33 % |
| Retainer (membrane, screen) and washer hole | 5.3 | 10 (`tr.nsb.surface_factor_frit`) | 24 % |
| Exit bore | 3.5 | 3 (`tr.nsb.surface_factor_lid`) | 5 % |
| Bore above the bed and the line upstream | 27.4 | 3 (`ma.nsb.surface_factor_tubing`) | 38 % |

The blank's variance is 95 % NSB variability, so the LOD follows the total non-specific enzyme. Two consequences:
(1) a bead with lower NSB helps by a third at most at the same area; (2) a bead with lower NSB also allows more
beads — more capture (65 % at 1×10⁶ M-280, reaction-limited, k_r 4.2×10⁻⁶ m/s against k_m 1.0×10⁻⁴ m/s) without
more NSB — and that is where most of the ceiling of §0 comes from. The larger lever outside the beads is the line
and the empty bore upstream of the bed; it is outside this question and is noted in §6.

## 2. Candidates

From the vendor survey (`beads_vendors.md`; references there). Only beads ≥ 1 µm, monodisperse, non-porous.

| Bead | Ø (µm) | Surface | Capture | Why considered | Tag |
|---|---|---|---|---|---|
| Dynabeads M-280 Streptavidin 11205D (current) | 2.8 | tosyl-activated, hydrophobic; stock 0.1 % BSA | biotin-F(ab')₂ | reference | [V R1, R2] |
| Dynabeads M-270 Streptavidin 65305 | 2.8 | hydrophilic, carboxylic-acid base, no BSA | biotin-F(ab')₂ | vendor's alternative where M-280's BSA gives background | [V R1, R2] |
| Agilent LodeStars 2.7 µm Streptavidin PL6727-1001 | 2.7 | polymer shell, carboxyl base; "ultralow non-specific binding" (vendor) | biotin-F(ab')₂; > 1200 pmol biotin/mg, > 5 µg biotin-IgG/mg | the Rissin bead family with streptavidin | [V R5] |
| Agilent LodeStars 2.7 µm Carboxyl PL6727-0001 | 2.7 | as above, COOH | F(ab')₂ by EDC/NHS | the Rissin 2010 surface itself | [V R5]; identity [S] |
| Dynabeads M-270 Epoxy 14301 | 2.8 | hydrophilic epoxy | F(ab')₂ covalent | no streptavidin, no BSA; vendor claims very low protein NSB | [S R9] |
| micromod micromer-M PEG-COOH 10 µm 08-56-104 | 10 | PEG (length not stated) | F(ab')₂ covalent | only catalogue PEG-surface monodisperse bead found ≥ 2 µm; screen alone holds it | [V R10, 2010 data sheet] |
| Carboxybetaine / POEGMA brush on M-270 Amine (in house) | 2.8 | polymer brush | F(ab')₂ into the brush | best published low-fouling evidence (flat surfaces; beads in Lin 2024) | literature, §3 |
| micromod micromer-M Streptavidin 10 µm 08-19-104 | 10 | polystyrene, streptavidin ~38 ng/cm² (≈ a tenth of a monolayer, Derived) | biotin-F(ab')₂ | magnetic, 10 µm, screen alone | [V R10] |
| Spherotech SVP-100-4 (docs/34 fallback) | 10–14 | polystyrene, streptavidin | biotin-F(ab')₂ | the existing fallback | [V R16] |
| Streptavidin silica 5 µm, non-porous (Bangs CS01002 type) | 5 | silica | biotin-F(ab')₂ | hydrophilic alternative | [S R18] |
| Dynabeads MyOne Streptavidin C1 65001 | 1.0 | as M-270 | biotin-F(ab')₂ | M-270 chemistry at 1 µm | [V R1] |

Rejected without modelling: MyOne T1 (same tosyl/BSA chemistry as M-280); porous silica (sicastar), Sepharose,
agarose and POROS (internal area open to a 200–300 kDa conjugate); TentaGel and other PEG resins (swelling gels made
for synthesis); Ademtech, nanomag, Turbobeads (< 1 µm); Sera-Mag SpeedBeads 1 µm (as C1, retainer not designed;
vendor claims low NSB from a protein-free block [V R12]). No catalogue zwitterionic bead was found [S].

## 3. NSB factors (all UNVERIFIED judgement)

No paper compares the NSB of an antibody–enzyme conjugate across M-280, M-270, MyOne or LodeStars beads under the
same conditions (`beads_nsb_evidence.md` §0). The anchors:

- Rissin 2010 (c1 [V]) defines the project's rate on carboxyl beads with covalent antibody and SuperBlock; its blank
  (about 1 % active beads) checks against the model's rate (4×10⁻¹¹ m/s × 15 pM × 30 min gives 6.5×10⁻⁴ /µm²
  against 4.4×10⁻⁴ /µm² measured; Derived).
- Chang 2012 (c2 [V]): in that format "all of the background signals seem to arise from the interaction of the
  labeling reagents with the capture antibodies". If that holds here, every bead carries the same floor and the bead
  surface only acts on the rest.
- Vendor: M-280 is hydrophobic and its background "might be caused by nonspecific binding to the BSA on the bead
  surface"; M-270 is the hydrophilic alternative [V R2]. Water contact angle 120° (tosyl) against 10° (carboxyl) on
  the MyOne pair [V a1].
- Brushes: carboxybetaine brushes give undetectable adsorption from plasma even after antibody coupling (Yang 2009,
  abstract [S]); a POEGMA brush gave an IL-6 LOD 100× lower than blocked nitrocellulose (Hucknall 2009 [V]); IgG
  adsorbs weakly on PEG already (Hua 2014 [V]); POEGMA on M-270 beads beat serum blocking, no fold given (Lin 2024
  [V]); a PEG-3400 brush on organosilica beads cut non-target antibody binding about 8× (Chen 2009 [V]).

Factors relative to the Rissin surface (`beads_nsb_evidence.md` §2), and as used in the model, relative to M-280:

| Surface | f vs Rissin (low–high) | Used: × M-280 | Bed factor in the model (low–high) |
|---|---|---|---|
| M-280 Streptavidin, BSA | 1.5 (1–5) | 1 | 3 (1–30), unchanged from docs/34 |
| M-270 Streptavidin, LodeStars Streptavidin and Carboxyl, M-270 Epoxy, MyOne C1 | 1.0 (0.5–3) | 0.67 | 2.0 (0.55–26) |
| micromod PEG-COOH | 0.6 (0.2–2) | 0.4 | 1.2 (0.25–16) |
| Brush (carboxybetaine, POEGMA) | 0.3 (0.05–1) | 0.2 | 0.6 (0.07–8.1) |
| Polystyrene streptavidin (Spherotech, micromod), silica | 2 (1–10) | 1.33 | 4.0 (1.1–66) |

The packed-bed factor of docs/34 (3, 1–30: beads in a column against beads in a tube) is kept for every bead; the
bead's own range is added to it on a log scale (`tier2_beads.py`, `combine`).

Capture sites (relative to the oriented monolayer of `chem.surfaces`): streptavidin–biotin as in the kit (1, 0.4–1);
covalent F(ab')₂ 0.4 (0.15–0.8); the micromod streptavidin bead 0.4 (0.1–0.8). Both new values are UNVERIFIED.

## 4. Model results

Docs/34 cell, only the beads changed; LOD in pg/mL (`tier2_beads.md` §2, §3). "Best amount" = lowest nominal LOD
over 0.5–8 × the bead area of 1×10⁶ M-280, within the washer-lift check of docs/34 at 80 µL/min and the 2.5 mm bore.

| Bead | Same area: nominal; median [5–95 %]; P(≤ 1) | Best amount (beads) | Best: nominal; median [5–95 %]; P(≤ 1) |
|---|---|---|---|
| M-280 Streptavidin (current) | 1.9; 7.9 [0.96–93]; 0.06 | 1× (1.0×10⁶) | same |
| **M-270 Streptavidin** | **1.7; 7.1 [0.87–82]; 0.07** | 1× (1.0×10⁶) | same |
| LodeStars 2.7 Streptavidin | 1.7; 7.1 [0.87–82]; 0.07 | 1× (1.1×10⁶) | same |
| MyOne C1 (retainer not designed) | 1.7; 7.0 [0.87–82]; 0.07 | 1× (7.8×10⁶) | same |
| LodeStars 2.7 Carboxyl, covalent | 2.7; 12 [1.2–150]; 0.04 | 2× (2.1×10⁶) | 2.3; 9.3 [1.0–120]; 0.04 |
| M-270 Epoxy, covalent | 2.7; 12 [1.2–150]; 0.04 | 2× (2.0×10⁶) | 2.3; 9.3 [1.0–120]; 0.04 |
| micromod PEG-COOH 10 µm, covalent | 2.2; 9.4 [1.0–120]; 0.05 | 3× (2.3×10⁵) | 1.7; 6.6 [0.85–79]; 0.07 |
| Brush on M-270 Amine, covalent | 2.2; 9.1 [0.97–120]; 0.05 | 3× (3.0×10⁶) | **1.5; 5.6 [0.74–64]; 0.08** |
| Spherotech SVP-100-4 | 2.0; 8.8 [1.0–110]; 0.05 | 1× (5.4×10⁴) | same |
| Silica 5 µm | 2.1; 9.3 [1.1–110]; 0.04 | 1× (3.1×10⁵) | same |
| micromod Streptavidin 10 µm | 3.2; 16 [1.5–250]; 0.02 | 1.5× (1.2×10⁵) | 3.0; 14 [1.4–230]; 0.03 |
| No NSB on the beads (ceiling) | 1.3 | 4× | 1.0; 3.0 [0.55–34]; 0.17 |

The M-280 row reproduces docs/34 §6.1 exactly. Every gain lies inside the spread of the Monte Carlo; the ranking is
set by the judged factors of §3 and by the site density, not by anything measured.

## 5. Ranking and what would change it

1. **M-270 Streptavidin** (or LodeStars 2.7 Streptavidin): small expected gain, no cost in design, protocol or risk.
2. **Brush on M-270 Amine**: largest gain in the model, but a development project; its benefit is capped by NSB on
   the capture antibody layer (Chang 2012), which the model does not separate from the bead surface.
3. M-280 (current), Spherotech, silica: within the uncertainty of each other.
4. Covalent beads: worse unless covalent F(ab')₂ keeps more than about 0.7 of the oriented sites (then equal to
   M-270), which would have to be shown.

What would change the ranking: a measured blank-bed NSB per bead (test below); a measured share of the blank that
comes from the beads at all (if the line and retainer dominate, no bead matters); a measured active-site density
for covalent coupling.

**Bench test (extends T2-1 of docs/30 and C-2 of docs/34; informational, not a gate):** coat M-280, M-270 and
LodeStars 2.7 Streptavidin identically with the biotinylated capture F(ab')₂ (and one set without capture
antibody), block in IgG-free BSA, and run the docs/34 blank sequence (no analyte) on each bed in the same cell,
n ≥ 5 per bead. Readouts: blank charge and its SD per bead; with and without capture antibody, to separate the bead
surface from the capture layer. A bead that lowers the blank by less than its SD between runs is not worth the
change.

## 6. Open points

- Whether the bead or the line upstream dominates the blank is the first thing the test above shows. The line and
  bore above the bed (38 % of the nominal NSB) are a larger lever than any bead, outside this question.
- Choice for the user: keep M-280 (docs/34) or switch the first choice to M-270 Streptavidin now; whether to add
  LodeStars 2.7 Streptavidin and a brush bead to the bench test.

## 7. Review and iteration

(Filled in as the review rounds proceed.)

## 8. Sources

Full reference lists with tags: `results/tier_round/beads_vendors.md` (R1–R24) and
`results/tier_round/beads_nsb_evidence.md`. The ones used above:

| Ref | Source | Tag |
|---|---|---|
| Rissin 2010 | Rissin DM et al., Nat Biotechnol 28:595 (2010), doi:10.1038/nbt.1641, Methods | [V] full text |
| Chang 2012 | Chang L et al., J Immunol Methods 378:102 (2012), doi:10.1016/j.jim.2012.02.011 | [V] full text |
| R1, R2 | Thermo Fisher Dynabeads trial-kit manual and FAQ pages for M-280 / M-270 Streptavidin (URLs in beads_vendors.md) | [V] |
| R5 | Agilent LodeStars brochure (2016) | [V] |
| R9 | Thermo Fisher M-270 Epoxy product page (Japanese, via search) | [S] |
| R10 | micromod data sheets (2010 copies) | [V] |
| R12 | Cytiva Sera-Mag SpeedBeads Streptavidin-Blocked procedure, IFU 29513808 | [V] |
| R16, R18 | Spherotech SVP-100-4; Bangs CS01002 | [V]; [S] |
| a1 | Trømborg et al., Dynal poster on MyOne beads (Thermo document) | [V] |
| Yang 2009 | Yang W et al., Langmuir 25:11911, doi:10.1021/la9015788 | abstract |
| Hucknall 2009 | Hucknall A et al., Adv Mater 21:1968, doi:10.1002/adma.200803125 | [V] |
| Hua 2014 | Hua B et al., Nat Methods 11:1233, doi:10.1038/nmeth.3143 | [V] |
| Lin 2024 | Lin P et al., Front Bioeng Biotechnol 12:1462203, doi:10.3389/fbioe.2024.1462203 | [V] |
| Chen 2009 | Chen et al., Langmuir 25:13510, doi:10.1021/la903148n | [V] |
