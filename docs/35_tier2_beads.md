# 35 — Alternative capture beads for the tier-2 cell

Status: desk work, 2026-11-18, Revision E (after review rounds 1–4, §7). Follow-up to docs/34 (tier-2 flow cell with
the bed inside). Question from the user: which bead gives the lowest LOD, most likely through the lowest
non-specific binding (NSB) of the conjugate; iterate with an independent reviewer until the answer stops changing.
Nothing is ordered; docs/30 and docs/34 are not changed. Numbers from `scripts/tier_round/tier2_beads.py` →
`results/tier_round/tier2_beads.md` (Monte Carlo n = 2000, paired draws). Desk research behind §2–3:
`results/tier_round/beads_vendors.md` (vendors, about 20 products, references R1–R24) and
`results/tier_round/beads_nsb_evidence.md` (published NSB evidence, tables a–e). Review reports:
`results/tier_round/review_beads_r1.md` to `review_beads_r5.md`.
Tags: [V] read this session in the cited page or full text (by the research agents or the reviewer); [S] secondary
(search summary, distributor page, abstract only); UNVERIFIED not checked or a judgement; Derived computed here.

## 0. Summary

**The bead is a small lever in this cell, and no bead reaches 1 pg/mL. Keep M-280 Streptavidin as built; put three
challengers beside it in one blank-bed test, after the two substrate questions of docs/30 §2.6.** Four beads form a
cluster at a nominal 1.8 pg/mL against 1.9 for M-280 (§4), with medians 7.0–8.0 against 7.9:

| Bead | Nominal; median | P(LOD below M-280's) | Change to docs/34 |
|---|---|---|---|
| Dynabeads M-270 Streptavidin (65305) | 1.8; 7.8 | 0.66 | none (drop-in) |
| Vector MagnaLINK Streptavidin 2.8 µm (M-1003), coated as docs/30 | 1.8; 8.0 | 0.54 | none (drop-in) |
| micromod micromer-M PEG-COOH 10 µm (08-56-104), F(ab')₂ coupled covalently, 1.5 × the bead area | 1.8; 7.0 | 0.83 (0.65 against M-280 at the same area) | covalent coupling; screen alone holds the beads (no membrane) |
| POEGMA or carboxybetaine brush grafted on M-270 Amine, 4 × the area | 1.8; 7.4 | 0.60 (0.72 at the same area) | a chemistry project; bed Δp 2.5 bar at 80 µL/min |

Agilent LodeStars 2.7 µm Streptavidin is level with them except on rounded nominal (1.93 against 1.80–1.84):
median 7.1, P 0.79 at 1.5 × the beads (0.68 at the same area). The P values restate judged inputs more than they
measure anything: for M-270, 0.66 is close to the judged chance that its surface is cleaner than M-280's (0.67). None
of these is worth a change on paper.

**Why the lever is small (§1).** The beads carry a third of the non-specific enzyme of the blank; the line and
empty bore above the bed (38 %), the retainer and washer hole (24 %) and the exit bore (5 %) carry the rest. Part of
the beads' share sits on the capture-antibody layer, which every bead carries (Chang 2012: background from "the
interaction of the labeling reagents with the capture antibodies" [V]). With half of it there (φ = 0.5, UNVERIFIED),
a bead surface with no NSB at all gives 1.6 pg/mL at the same area and 1.5 at 1.5 × the beads; only no NSB of any
kind on the beads, capture layer included, gives 1.0 (4 × the beads, at the edge of what the retainer holds).

**Capture sites matter as much as NSB.** Capture is reaction-limited (k_r 4.2×10⁻⁶ m/s against k_m 1.0×10⁻⁴ m/s;
65 % captured at 1×10⁶ M-280), so fewer active sites per area cost signal one for one, and buying it back with more
beads brings NSB back. The ranking of the covalent and low-fouling beads therefore hangs on how many active sites
covalent coupling keeps: at 0.7 of the streptavidin–biotin layer (Revision C, judgement) the PEG bead is in the
cluster; at 1/3 (Revision B) it falls to 2.4; at 1 it leads with 1.6, median 6.6 (§4 sensitivity).

**The largest upside on paper** is MagnaLINK coated with three times the antibody, at half the beads (the vendor
states 113 µg biotinylated IgG per mg against ≈ 10 for Dynabeads [V vendor page, review round 2]). If the
capture-layer NSB grows with the antibody load: nominal 1.9, median 7.6, P 0.56 with 2 × the active sites, and 1.7,
median 6.8, P 0.95 if all the extra antibody is active; if it does not grow with the load, 1.4, median 5.7. If the
extra antibody is inaccessible it is worse (2.5). That makes it the challenger with the widest range, both ways;
the bench test can check it.

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
| Vector MagnaLINK Streptavidin M-1003 | 2.8 ± 0.2, CV < 5 % | streptavidin on a hydrophilic polymer encapsulation; stock in water + azide, no BSA stated; ≥ 10 nmol free biotin/mg; 113 µg biotinylated IgG/mg (vendor, against 10 for "a similar 2.8 µm bead"); porosity not stated | biotin-F(ab')₂ | high capacity per area, protein-free stock | [V vendor page, review round 2] |
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
tosyl/epoxy, no expected gain over M-270). Polysciences ProMag 3 Streptavidin (86056 [S]) and ProMag HP Streptavidin
(25508; "low nonspecific binding in protein-based systems", capacity not stated [V reviewer]) and Ocean NanoTech
Mono Mag 3 µm (MV3000 [S]): hydrophilic streptavidin beads of the same class as M-270, without published capacity;
they would sit with M-270 in the model. No catalogue zwitterionic bead, and no catalogue PEG- or brush-surface bead
with a full streptavidin layer, was found by the research agent or by reviewer 2 [S].

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
all other beads are stated relative to it. A share φ of M-280's bead NSB sits on the capture-antibody layer: φ = 0.5
(0.1–0.9), not separated in any source. That part scales with the capture antibody loaded per area relative to M-280
coated as in docs/30 (`load`: 1 for the beads coated at 10 µg/mg, 0.3 for the entangled brush, 0.4 for the
sub-monolayer micromod streptavidin bead, 0.7 for LodeStars Streptavidin at its brochure loading, 3 for MagnaLINK
coated with 3 × the antibody); the rest scales with the bead surface by `rel`. Bed factor = 3 × (φ·load + (1 − φ)·rel). φ and `rel` are drawn independently of the kit's parameters (seed + 1), so every bead is compared
with M-280 on the same draws of everything else; P(< M-280) in §4 is the share of draws in which the bead wins.

| Surface | rel to M-280 (low–high) | Reason |
|---|---|---|
| M-280 Streptavidin (re-blocked in BSA) | 1 | anchor |
| M-270 Streptavidin, LodeStars Streptavidin and Carboxyl, M-270 Epoxy, MagPlex-Avidin | 0.8 (0.4–2) | hydrophilic base, but BSA on every bead in the protocol |
| MagnaLINK | 0.8 (0.4–3) | hydrophilic polymer; 11 × the biotin-IgG capacity per mg at the same size means a 3D streptavidin layer, mostly free streptavidin when coated at 10 µg/mg; the upper end allows that layer to take up conjugate |
| micromod PEG-COOH | 0.5 (0.15–1.5) | PEG of unknown length, not a brush |
| Brush (POEGMA, carboxybetaine) | 0.25 (0.05–1) | flat-surface and bead evidence above; floor not known |
| Polystyrene streptavidin (Spherotech, micromod), silica | 1.3 (0.7–7) | no vendor surface finish, blocked in BSA |

Active capture sites (relative to the oriented monolayer of `chem.surfaces`):

| Capture | Sites (low–high) | Source |
|---|---|---|
| biotin-F(ab')₂ on M-280 or M-270 streptavidin | kit: 1 (0.4–1) | `tr.capture.site_factor_streptavidin_biotin`; equal capacity per area [V R1] |
| MagnaLINK coated as docs/30 | kit: 1 (0.4–1) | the coating step offers 10 µg antibody per mg, as for M-280 |
| LodeStars Streptavidin | 0.7 (0.5–1); load 0.7 | brochure minimum 5 µg/mg (store page now > 3.6 [S]) against ≈ 10 for Dynabeads, similar area per mg (UNVERIFIED); less antibody also means less capture layer |
| MagPlex-Avidin, Spherotech, silica | 0.7 (0.3 or 0.1–1) | capacity not published |
| micromod Streptavidin 10 µm | 0.4 (0.1–0.8) | about a tenth of a streptavidin monolayer (Derived) |
| covalent F(ab')₂ (LodeStars Carboxyl, M-270 Epoxy, PEG-COOH) | 0.7 (0.3–1) | judgement. Revision B used 1/3 from `chem.antibodies.oriented_vs_random_capacity_gain` (Peluso 2003), but both arms of that paper are on streptavidin (site-specific against random biotinylation) [V abstract, reviewer 2], and the project's biotin-SP F(ab')₂ is the random arm; no source compares covalent coupling with it. 1/3 and 1 are run as sensitivity. Covalent beads keep load 1: the inactive antibody is still on the bead |
| brush, antibody entangled | 0.3 (0.05–1) | loading falls with brush thickness (Hu 2024 [V]) |

Not in the model, stated here: the physical part of the packed-bed factor may fall for 10–14 µm beads (wider
channels, better washing), which would favour them; streptavidin and avidin as NSB sources get no separate factor
(the covalent beads that remove them get no credit); for 5–6.5 µm beads a coarser membrane (2–3 µm) would hold
them with less pore-wall area (the membrane is 1.6 of the 4.9 mm² of retainer, a small effect).

## 4. Model results

Docs/34 cell, only the beads changed; LOD in pg/mL (`tier2_beads.md` §2–4), φ = 0.5. "Best amount" = lowest
nominal LOD over 0.25–8 × the bead area of 1×10⁶ M-280, within the washer-lift check of docs/34 at 80 µL/min and the
bed bore (0.5 mm × 2.5 mm); neither limit binds at any candidate's chosen amount (the 'no NSB at all' line is
limit-bound).

| Bead | Same area: nominal; median [5–95 %]; P(≤ 1); P(< M-280) | Best amount (beads) | Best: nominal; median [5–95 %]; P(≤ 1); P(< M-280); P(< M-280 at the same area) |
|---|---|---|---|
| M-280 Streptavidin (current) | 1.9; 7.9 [0.96–93]; 0.06; — | 1× (1.0×10⁶) | same |
| **M-270 Streptavidin** | **1.8; 7.8 [0.95–89]; 0.06; 0.66** | 1× (1.0×10⁶) | same |
| **MagnaLINK Streptavidin, coated as docs/30** | **1.8; 8.0 [0.98–93]; 0.05; 0.54** | 1× (1.0×10⁶) | same |
| **micromod PEG-COOH 10 µm, covalent** | 1.9; 7.8 [0.92–95]; 0.06; 0.48 | 1.5× (1.2×10⁵) | **1.8; 7.0 [0.90–84]; 0.06; 0.83; 0.65** |
| **Brush on M-270 Amine** | 2.8; 13 [1.2–200]; 0.03; 0.13 | 4× (4.0×10⁶) | **1.8; 7.4 [0.92–94]; 0.06; 0.60; 0.72** |
| LodeStars 2.7 Streptavidin | 2.0; 7.7 [0.95–90]; 0.06; 0.56 | 1.5× (1.6×10⁶) | 1.9; 7.1 [0.93–80]; 0.06; 0.79; 0.68 |
| MagPlex-Avidin 6.5 µm | 2.1; 9.1 [1.1–110]; 0.04; 0.08 | 1.5× (2.8×10⁵) | 2.1; 8.4 [1.0–100]; 0.05; 0.30; 0.18 |
| LodeStars 2.7 Carboxyl, covalent | 2.1; 9.1 [1.1–110]; 0.04; 0.09 | 1.5× (1.6×10⁶) | 2.1; 8.4 [1.0–100]; 0.05; 0.30; 0.18 |
| M-270 Epoxy, covalent | 2.1; 9.1 [1.1–110]; 0.04; 0.09 | 1.5× (1.5×10⁶) | 2.1; 8.4 [1.0–100]; 0.05; 0.30; 0.18 |
| Spherotech SVP-100-4 | 2.2; 14 [1.3–210]; 0.03; 0.02 | 1.5× (8.1×10⁴) | 2.2; 13 [1.3–190]; 0.03; 0.04; 0.03 |
| Silica 5 µm | 2.3; 14 [1.4–210]; 0.03; 0.00 | 1.5× (4.7×10⁵) | 2.3; 13 [1.4–190]; 0.03; 0.01; 0.00 |
| micromod Streptavidin 10 µm | 2.7; 15 [1.4–230]; 0.03; 0.01 | 2× (1.6×10⁵) | 2.4; 13 [1.3–190]; 0.03; 0.04; 0.07 |
| Bead surface with no NSB, capture layer kept | 1.6 | 1.5× | 1.5 |
| No NSB on the beads at all | 1.3 | 4× (edge of the allowed amounts) | 1.0 |

The M-280 row reproduces docs/34 §6.1 exactly (nominal and median; check in `tier2_beads.md` §0).

Sensitivity (φ = 0.5 unless stated; best amount; `tier2_beads.md` §3, §3a):

| Change | Nominal; median; P(< M-280) |
|---|---|
| φ = 0 (all bead NSB on the bead surface) | PEG-COOH 1.6, brush, M-270 and MagnaLINK 1.8, M-280 1.9 (nominal) |
| φ = 0.8 | M-270, MagnaLINK, PEG-COOH, brush 1.9; M-280 1.9 (nominal) |
| covalent sites 1/3 (Revision B): PEG-COOH; LodeStars Carboxyl | 2.4; 10; 0.10 — 2.8; 12; 0.00 |
| covalent sites 1 (as good as streptavidin–biotin): PEG-COOH | 1.6; 6.6; 0.98 |
| MagnaLINK, 3 × antibody, half the beads, sites 2 (0.7–3), capture-layer NSB × 3 | 1.9; 7.6; 0.56 |
| the same, sites 3 | 1.7; 6.8; 0.95 |
| the same, sites 1 (extra antibody inaccessible) | 2.5; 10; 0.01 |
| the same, sites 3, capture-layer NSB not growing with the load | **1.4; 5.7; 1.00** |
| MagnaLINK as docs/30, its surface 3 × M-280 (3D layer takes up conjugate) | 2.5; 12; 0.00 |
| brush with the capture layer per area of M-280 (load 1) | 2.5; 10; 0.19 |
| brush with the sites and load of M-280 (antibody fully active in the brush) | 1.7; 6.1; 0.99 |

## 5. Ranking and what would change it

1. **Cluster at 1.8 pg/mL**: M-270 Streptavidin and MagnaLINK (drop-ins), micromod PEG-COOH 10 µm (covalent),
   brush (development); LodeStars 2.7 Streptavidin level on median (1.9 nominal). Within the uncertainty of each other and of M-280; their order depends on judged inputs.
2. **M-280 Streptavidin** (current, 1.9) and MagnaLINK with 3 × the antibody (1.4–2.5, the widest range).
3. Everything else 2.1–2.4, mainly through fewer active capture sites or an unfinished polystyrene surface.

What would turn the ranking, in the order a bench test can find it: (a) the capture fraction of covalent F(ab')₂
on PEG-COOH beads (at 1 of the streptavidin layer the PEG bead leads, 1.6); (b) whether MagnaLINK's extra capacity
is active and whether capture-layer NSB grows with antibody load (1.4 at best, 2.5 at worst); (c) the active sites of an
antibody entangled in a brush (with the sites of M-280 the brush gives 1.7, median 6.1); (d) φ — if the capture
layer carries most of the bead NSB, no bead surface matters. Nothing on the list closes the gap to 1 pg/mL alone.

**Bench test (extends T2-1 of docs/30 and C-2 of docs/34; informational, not a gate; after the two substrate
questions C1 and C5 of docs/30 §2.6, without which no blank is meaningful).** Decide in advance on an LOD proxy built
from means, not on the blank alone and not on per-arm SDs: for each capture bead, (mean blank of the arm × the blank
CV pooled over all arms) / (net signal per pg/mL from a 10–30 pg/mL standard, inside the linear range; upper limit
of the docs/34 cell about 1400 pg/mL). M-280 stays unless a challenger lowers that proxy by at least 1.3 ×, and any
winner is confirmed in a second, independent set of n = 5 before it replaces M-280. With a pooled blank CV ≤ 15 %, a
1.3 × difference of means is resolvable at n = 5 (reviewer 3, Derived); a proxy built from each arm's own SD and a
1 pg/mL standard is not (a 1.3 × false "win" between identical beads in 31–37 % of tests, a true one found in about
half; simulation by reviewer 4), and with four challengers the confirmation run keeps the chance of a false switch
low. The pooled CV assumes that the bead does not change the run-to-run CV; that is not tested at this n. The blank
alone cannot decide: the beads carry a third of it, so even a bead with no NSB lowers it by only 1.5 ×, and
MagnaLINK's gain would come from capture, not from the blank.

- Arms: M-280, M-270 Streptavidin, MagnaLINK (coated as docs/30, and with 3 × the antibody at half the beads),
  micromod PEG-COOH 10 µm with covalent F(ab')₂ (screen alone).
- Per bead: the capture beads; the non-immune biotinylated F(ab')₂ beads already planned in docs/30 §4.2 step 1
  (same load, no specific capture: φ control); biotin-quenched beads without antibody (bead surface alone).
- Two blocking arms for M-280 and M-270: (a) IgG-free BSA as docs/30; (b) no protein block, conjugate in a BSA-free
  diluent (e.g. Tween-20 or PVA, UNVERIFIED) — the only arm that can show the BSA effect the vendor describes.
- The docs/34 blank sequence (no analyte), n ≥ 5 per arm, arm order randomised in the one cell, a fresh retainer
  per run (the retainer carries a quarter of the blank). An empty-retainer run gives the share of the blank that is
  not on the beads.
- A 10–30 pg/mL standard on each capture bead gives its capture fraction and the slope of the LOD proxy (this is
  what decides covalent coupling and MagnaLINK's extra capacity).
- Size: 5 bead arms × 3 preparations, 2 BSA-free arms, the empty retainer and 5 standards = 23 arms, n = 5 each:
  about 115 runs of about 1 h in one cell (UNVERIFIED time), plus the confirmation set. To shorten it, run the non-immune and quenched preparations only
  for M-280 and for the best challenger.
- The micromod PEG-COOH 10 µm bead is cited from a 2010 data sheet; whether it can still be ordered is
  UNVERIFIED (ask micromod) before it enters the test.

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
| 2 | not converged: 2 major, 6 minor (`review_beads_r2.md`); model code confirmed correct, every number matched | M1 Peluso 2003 misapplied (both arms on streptavidin), the covalent penalty unsupported. M2 a catalogue bead missed: MagnaLINK 2.8 µm, 113 µg biotin-IgG/mg. Minor: P(< M-280) of M-270 restates the prior; best-amount rows compared with M-280 at 1×; capture-layer NSB should scale with antibody load; bench test cannot resolve a few per cent and its φ control is confounded; ceiling limit-bound; LodeStars capacity now > 3.6 µg/mg | All applied (Rev C): covalent sites 0.7 (0.3–1) as judgement with 1/3 and 1 as sensitivity; MagnaLINK added with its high-load variants; `load` term; P against M-280 at the same area; bench test rewritten (decision rule, non-immune and quenched controls, randomised order, fresh retainers, after C1/C5); ProMag and Mono Mag listed. The summary changed from "keep M-280, M-270 the only bead ahead" to "a cluster of four at 1.8, keep M-280, test three challengers" |
| 3 | not converged: 2 major, 7 minor (`review_beads_r3.md`); every number in §0/§4 matched; MagnaLINK and micromod claims checked [V] | MJ1 the paired Monte Carlo applied `load` twice (medians and P wrong for brush, micromod SA, MagnaLINK high-load; nominal right). MJ2 the bench decision rule (≥ 1.5 × lower blank) could not fire on the predicted effects and was blind to capture gains. Minor: LodeStars load; brush site sensitivity; stale text; MagnaLINK URL and vendor note; micromod availability; test size; edge check for variants | All applied (Rev D): reference bed with load 1, check added; rerun; decision on an LOD proxy at 1.3 ×; LodeStars load 0.7; brush and covalent statements; test size and shortening; sources. Recommendation unchanged; MagnaLINK at high load now the widest-range challenger (P 0.56–0.95 instead of 0.05–0.28) |
| 4 | not converged on the bench rule only: model converged, every number matched, round-3 fixes in place (`review_beads_r4.md`) | MJ1 the LOD proxy (3 × per-arm SD / 1 pg/mL signal) cannot resolve 1.3 × at n = 5 and the attribution to reviewer 3 was misapplied. Minor: LodeStars left out of the cluster on rounding; the new check was tautological; caption formula without `load`; test size 115 not 90; MagnaLINK competitor figure in the vendor note was free biotin, not IgG; r4 file missing | All applied (Rev E, text and check only, no model number changed): proxy on means with a pooled CV and a 10–30 pg/mL standard, confirmation run; LodeStars named with the cluster; the check now compares each bead's sampled factor with M-280's draw (fails if `load` is double-counted, tested); caption; 115 runs; vendor note corrected |

## 8. Sources

Full reference lists with tags: `results/tier_round/beads_vendors.md` (R1–R24) and
`results/tier_round/beads_nsb_evidence.md` (its entry b10 names the 2024 POEGMA paper's first author wrongly as Lin;
it is Hu J). The ones used above:

| Ref | Source | Tag |
|---|---|---|
| Rissin 2010 | Rissin DM et al., Nat Biotechnol 28:595 (2010), doi:10.1038/nbt.1641, Methods | [V] full text |
| Chang 2012 | Chang L et al., J Immunol Methods 378:102 (2012), doi:10.1016/j.jim.2012.02.011 | [V] full text |
| R1, R2 | Thermo Fisher Dynabeads trial-kit manual and FAQ pages for M-280 / M-270 Streptavidin (URLs in beads_vendors.md) | [V] |
| R5 | Agilent LodeStars brochure (2016) | [V] |
| R9 | Thermo Fisher M-270 Epoxy product page (Japanese, via search) | [S] |
| R10 | micromod data sheets (2010 copies) | [V] |
| R16, R18 | Spherotech SVP-100-4; Bangs CS01002 | [V]; [S] |
| MagPlex | Diasorin/Luminex MagPlex and MagPlex-Avidin product sheet (via search, reviewer round 1) | [S]; avidin [V] reviewer 2 |
| MagnaLINK | Vector Laboratories MagnaLINK Streptavidin Magnetic Beads M-1003, https://vectorlabs.com/products/magnalink-streptavidin-mag-beads-2-8-m/ (capacity compared with an unnamed "similar 2.8 µm bead"; free biotin given as ≥ 10 and ≥ 12 nmol/mg in two places; covalent streptavidin layer) | [V] reviewers 2 and 3 |
| ProMag | Polysciences ProMag HP Streptavidin 25508 product page; ProMag 3 Streptavidin 86056 | [V]; [S] (reviewer 2) |
| Peluso 2003 (abstract) | Peluso P et al., Anal Biochem 312:113 (2003), PubMed 12531195 | [V] abstract, reviewer 2 |
| a1 | Trømborg et al., Dynal poster on MyOne beads (Thermo document) | [V] |
| Yang 2009 | Yang W et al., Langmuir 25:11911, doi:10.1021/la9015788 | abstract |
| Hucknall 2009 | Hucknall A et al., Adv Mater 21:1968, doi:10.1002/adma.200803125 | [V] |
| Hua 2014 | Hua B et al., Nat Methods 11:1233, doi:10.1038/nmeth.3143 | [V] |
| Hu 2024 | Hu J et al., Front Bioeng Biotechnol 12:1462203 (2024), doi:10.3389/fbioe.2024.1462203, PMID 39640065 | [V] |
| Chen 2009 | Chen et al., Langmuir 25:13510, doi:10.1021/la903148n | [V] |
