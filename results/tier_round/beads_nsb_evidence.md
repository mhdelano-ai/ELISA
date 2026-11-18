# Conjugate NSB versus bead surface: published evidence and proposed surface factors

Session 2026-11-18. Desk research for the choice of capture beads (docs/34 §3; `params/model_assumptions.yaml` `nsb.*`;
`params/chemistry.yaml` `nsb_effective_rate_constant` = 4e-11 m/s, derived from Rissin 2010). No repo file edited.

Tags: **[V]** = read this session (full text = FT, abstract = Abs). **UNVERIFIED** = not read this session, or my own judgement.
Tools: PubMed (search, metadata, PMC full text via E-utilities), WebSearch. Consensus was not available: the free monthly
allowance was used up, and its message says it resets on 1 December
(https://consensus.app/continue?from=mcp&client=claude_desktop&intent=upgrade).
ScienceDirect, ACS full texts and the Whitesides-group PDFs could not be opened (403 or access denied).

## 0. Main finding

**No paper I found compares conjugate NSB across commercial bead types (M-280 / M-270 / MyOne / Simoa beads) under the
same assay conditions with numbers.** The vendor material is qualitative, and the digital-ELISA papers vary bead number,
reagent concentration and time, not bead chemistry. Every per-bead factor below is therefore judgement, anchored on:
(i) the absolute NSB level of the Rissin/Chang Simoa beads; (ii) the Quanterix finding that **background is dominated
by the labelling reagents binding the capture-antibody layer, not the bead base material**; (iii) flat-surface
low-fouling data (SPR or ellipsometry; mostly plasma or single proteins, little on dilute IgG conjugates); (iv) surface
properties of the Dynabeads (contact angle, charge).

A point that bears on the model: **the Rissin 2010 reference beads are not Dynabeads M-280.** They are 2.7 µm
carboxyl-terminated magnetic beads (Varian), with antibody coupled by EDC/NHS and SuperBlock T-20 as blocker.
M-280 Streptavidin is a hydrophobic tosyl/polystyrene-type bead (water contact angle 120° for M-280 Tosylactivated)
carrying streptavidin and BSA. So "M-280 = factor 1" in `surface_factor_magnetic_beads` is itself an assumption.

## 1. Evidence table

### (c) Digital ELISA / single-molecule bead assays (the reference surface)

| # | Paper | Condition | Value | Tag |
|---|---|---|---|---|
| c1 | Rissin DM et al. 2010, Nat Biotechnol 28:595, doi:10.1038/nbt.1641 (PMC2919230) | Beads: "2.7-µm-diam. carboxyl-terminated magnetic beads … Varian"; SuperBlock T-20; 200 000 beads/100 µL; detection Ab ~1 nM, 45 min; SβG 1–50 pM, 30 min; 3 + 6 washes PBS/0.1 % Tween-20 | "typical background signal of 1 % active beads"; "backgrounds in digital ELISA arise from non-specific binding (NSB) of detection antibody and enzyme conjugate to the capture bead surface (Supplementary Table 2)"; "excessive bead concentrations can lead to … increases in non-specific binding" | [V] FT (Supp. Table 2 itself not read) |
| c2 | Chang L, Rissin DM, … Duffy DC 2012, J Immunol Methods 378:102–115, doi:10.1016/j.jim.2012.02.011 (PMC3327511) | Simoa PSA; SβG 15 pM, 30 min labels only ~13 % of complexes (deliberate under-labelling) | Background "equivalent to adding 1 fM of analyte … (AEB < 0.005)"; noise floor "about 100 active beads in … 25,000, … AEB = 0.004". **"all of the background signals seem to arise from the interaction of the labeling reagents with the capture antibodies"**; "those background signals are dominated by the interaction of the labeling reagents with the capture antibody immobilized on beads"; "We have not observed significant background signals from matrix proteins" | [V] FT |
| c3 | Kan CW, … Rissin DM, … Duffy DC 2020, Lab Chip 20:2122, doi:10.1039/d0lc00267d | Fewer capture beads (≤ 5000 vs ~500 000), higher read efficiency | LOD gains of up to 437× (IL-17A, 0.7 aM); for PSA no gain "due to … increased non-specific binding" | [V] Abs |
| c4 | Wu C, Dougan TJ, Walt DR 2022, ACS Nano 16:1025, doi:10.1021/acsnano.1c08675 (PMC9499451) (MOSAIC) | Beads from Quanterix and Bangs; 100 000 → 2000 assay beads | Signal-to-background rises as bead number falls (≈10× LOD gain for IL-10), not for IL-6/IL-1β. Simoa uses "helper beads" (400 000 unconjugated + 100 000 assay beads) "for improved signal-to-background". Authors expect further gains from "optimization of surface chemistries across all beads to minimize nonspecific binding" (no data) | [V] FT |

Reading of (c): NSB per bead is set by the labelling reagents meeting the capture-antibody layer, and roughly scales with
bead area; it is not fixed by the bead's base chemistry. Consistency check against the model (my arithmetic): 1 % on
beads ≈ 0.01 enzyme per 2.7 µm bead (22.9 µm²) ≈ 4.4×10⁻⁴ µm⁻². k_nsb·C·t = 4e-11 m/s × 15 pM (9×10¹⁵ m⁻³) × 1800 s
≈ 6.5×10⁸ m⁻² = 6.5×10⁻⁴ µm⁻², the same order. The chemistry.yaml value is consistent with the source.

### (a) Commercial magnetic beads

| # | Source | Condition | Value | Tag |
|---|---|---|---|---|
| a1 | Trømborg H, Aksnes E, … (Dynal Biotech / Future Diagnostics), poster "New optimised one micron magnetic bead platform…", Thermo Fisher document https://documents.thermofisher.com/TFS-Assets/CMD/posters/Automated_immunoassays.pdf (no year printed) | Contact angle on dry bead layer; zeta-potential pI | M-280 Tosylactivated **120°**, pI 7.0 uncoated / 4.9 antibody-coated / 5.1 streptavidin-coated; MyOne prototype 120°; MyOne Carboxylic Acid **10°**, pI 2.7 / 5.2 / 4.1. "the protein immobilised may determine the Isoelectric point". MyOne ≈ 2.5× surface per mass. Signal-to-noise Table 2 is an image (numbers not extractable); text says MyOne S/N "excellent", comparable to M-280 | [V] FT (poster) |
| a2 | Thermo Fisher FAQs for M-280 Streptavidin (11205D) and M-270 Streptavidin / Carboxylic Acid | Vendor statements | M-280 hydrophobic, M-270 hydrophilic; M-280 background "might be caused by nonspecific binding to the BSA on the bead surface" or to streptavidin; M-270 SA "not coated with BSA and are hydrophilic"; carboxyl surface "may attract positively charged proteins" | Search snippets only: UNVERIFIED (pages not opened) |
| a3 | ACS Omega 2017/18, doi:10.1021/acsomega.7b01427 (cell isolation, 5 bead types) | Cell capture, not proteins | Snippet: M-270 lowest nonspecific capture | UNVERIFIED (not opened; cells, not relevant to conjugate) |

There are no published numbers for conjugate NSB on M-280 vs M-270 vs MyOne T1/C1 in the same immunoassay.

### (b) Low-fouling coatings (flat surfaces and beads)

| # | Paper | Condition | Value | Tag |
|---|---|---|---|---|
| b1 | Prime KL, Whitesides GM 1991, Science 252:1164, doi:10.1126/science.252.5009.1164 | Mixed SAMs on gold; fibrinogen and others | Adsorption varies monotonically with SAM composition; hexa(EG) SAMs most resistant (no numbers in abstract) | [V] Abs |
| b2 | Ostuni E, Chapman RG, Holmlin RE, Takayama S, Whitesides GM 2001, Langmuir 17:5605 | SPR survey of SAM end groups | % monolayer of fibrinogen and lysozyme per group (numbers not obtained) | UNVERIFIED (PDF not accessible) |
| b3 | Chen S, Zheng J, Li L, Jiang S 2005, JACS 127:14473, doi:10.1021/ja054169u | Phosphorylcholine SAMs | "strong resistance … to protein adsorption" (no numbers in abstract) | [V] Abs |
| b4 | Zhang Z, Chen S, Jiang S 2006, Biomacromolecules 7:3311, doi:10.1021/bm060750m | pCBMA brush 10–15 nm on gold, SPR; fibrinogen, lysozyme, hCG | "very largely prevented" NSB; after anti-hCG immobilisation still "high resistance to nonspecific protein adsorption" | [V] Abs |
| b5 | Ladd J, Zhang Z, Chen S, Hower JC, Jiang S 2008, Biomacromolecules 9:1357, doi:10.1021/bm701301s | 6 polymer and SAM coatings, serum and plasma | ATRP polymer brushes resist better than SAMs; zwitterionic as good as PEG (numbers not in abstract; ng/cm² values in full text not read) | [V] Abs |
| b6 | Yang W, Xue H, Li W, Zhang J, Jiang S 2009, Langmuir 25:11911, doi:10.1021/la9015788 | pCBAA ~21 nm, SPR, undiluted serum and plasma, 25 and 37 °C | Adsorption "undetectable"; still undetectable after antibody immobilisation. (SPR detection limit ≈ 0.3 ng/cm² is often quoted for this setup: UNVERIFIED) | [V] Abs |
| b7 | Rodriguez Emmenegger C, Brynda E, Riedel T, Sedlakova Z, Houska M, Alles AB 2009, Langmuir 25:6328, doi:10.1021/la900083s | SPR: OEG/COOH SAMs, PEG on SAM, pCBMA, pSBMA, pMPC; plasma and single proteins (HSA, **IgG**, fibrinogen, lysozyme) | pCBMA "completely prevented the deposition from plasma"; the other zwitterionic brushes prevented single-protein adsorption (IgG included) but not plasma deposition; PEG fouled only from > 350 kDa fractions (ng/cm² not in abstract) | [V] Abs |
| b8 | Hucknall A, … Chilkoti A 2009, Adv Mater 21:1968, doi:10.1002/adma.200803125 (PMC6516072) | POEGMA brush 100 nm on glass vs nitrocellulose; antibody microarray; biotin-detection Ab 10 µg/mL (~67 nM) 1 h, SA-Cy5 | Background on POEGMA "showed no increase … upon completion" (only glass autofluorescence) with no blocking step; IL-6 LOD **100 fg/mL on POEGMA vs 10 pg/mL on blocked nitrocellulose (100×)**; capture-Ab density and background both higher on nitrocellulose | [V] FT |
| b9 | Hua B, … Ha T 2014, Nat Methods 11:1233, doi:10.1038/nmeth.3143 (PMC4245390) | Single-molecule spot counts per 2500 µm², labelled proteins at nM, PEG vs DDS-Tween-20 glass | DT20 cuts NSB "typically 10-fold and up to 30-fold" vs PEG for most proteins, but **"IgG is not highly sticky to the PEG surface, so the DT20 and PEG surfaces performed roughly the same"** for antibodies | [V] FT |
| b10 | Lin P et al. 2024, Front Bioeng Biotechnol 12:1462203, doi:10.3389/fbioe.2024.1462203 (PMC11617200) | POEGMA brush grown on amine M-270 Dynabeads; FITC-BSA 1 mg/mL, 2 h; confocal per-bead intensity | POEGMA beads below goat-serum-blocked beads (p = 0.019); fluorescence decreases with longer ATRP (thicker brush). No fold value in text (figures only). IL-8 MagPEA without blocking or washing, LOD 18.5 fg/mL, same as carboxyl-bead MagPEA | [V] FT |
| b11 | Sulfobetaine/PEG-COOH composite magnetic beads, Microchem J 2026 (pii S0026265X26031383) | Chemiluminescence immunoassay | Snippet: "2.7-fold reduction in background" against the authors' earlier beads | UNVERIFIED (403; authors and DOI not seen) |
| b12 | Huber D et al. 2009, Anal Bioanal Chem 394:539, doi:10.1007/s00216-009-2698-8 | Blockers on microtitre plates | PVA and Ficoll "did as well as BSA" (no casein-vs-BSA number) | [V] Abs |

Casein vs BSA for conjugate NSB: I found no quantitative head-to-head comparison this session. The commonly quoted ranking
(casein ≥ BSA) is UNVERIFIED.

### (d) Packed-bed, porous and resin supports

| # | Paper | Condition | Value | Tag |
|---|---|---|---|---|
| d1 | Trinkle-Mulcahy L et al. 2008, J Cell Biol 183:223, doi:10.1083/jcb.200805092 (PMC2568020) | SILAC "bead proteomes": Protein G Sepharose vs agarose vs Dynabeads, HeLa extracts, 30 min and 18 h | "we did not observe a single bead matrix that gave universally lower levels of contaminants"; magnetic beads lower in nuclear extract, Sepharose or agarose lower in cytoplasmic extract; "affinity matrices constitute a major source of nonspecific protein binding". No single fold factor; per bead volume, not per area | [V] FT |
| d2 | TentaGel on-bead screening (Chen et al., "On-bead screening of combinatorial libraries: reduction of nonspecific binding by decreasing surface ligand density", PMID 19397369; and the CONA on-bead affinity paper, PMID 22829563) | One-bead-one-compound screening | Snippets: NSB lowered with ~10× lower surface ligand loading; TentaGel "susceptible to swelling and protein entrapment" | UNVERIFIED (abstracts not read) |
| d3 | Superporous agarose beads as microfluidic immunoassay support, Ultramicroscopy 2008 (pii S0304399108001459) | Goat IgG assay | Flow through the bead interior; no NSB number seen | UNVERIFIED |

No published packed-bed immunoassay compares conjugate NSB across PS, silica, agarose and PEG resin under the same
conditions.

### (e) Conjugate format (brief)

| # | Paper | Value | Tag |
|---|---|---|---|
| e1 | Imagawa M, Hashida S, Ishikawa E, et al. 1984, J Biochem 96:659, doi:10.1093/oxfordjournals.jbchem.a134882 | Fab'-HRP gave "lower nonspecific bindings" than Fab'-β-gal on IgG-coated PS balls (no fold in abstract) | [V] Abs |
| e2 | Imagawa M, Hashida S, Ohta Y, Ishikawa E 1984, Ann Clin Biochem 21:310, doi:10.1177/000456328402100414 | Same ranking of the enzymes for AFP and hCG | [V] Abs |
| e3 | Ruan K, Hashida S, … Ishikawa E 1986, Ann Clin Biochem 23:54, doi:10.1177/000456328602300106 | Normal F(ab')2 added during the conjugate step to reduce conjugate NSB: insulin LOD 0.1 → 0.02 mU/L (5×; NSB and other changes combined) | [V] Abs |
| e4 | Inoue S, Hashida S, … Ishikawa E 1985, J Biochem 98:1387, doi:10.1093/oxfordjournals.jbchem.a135406 | Affinity-purified Fab'-β-gal conjugate: hCG LOD 30× better than before purification (non-specific conjugate removed) | [V] Abs |
| e5 | Hashida S et al. 1985, J Immunoassay 6:111, doi:10.1080/01971528508063024 | Less non-specific conjugate gives lower background | [V] Abs |
| e6 | Ishikawa E, Hashida S, Kohno T, Hirota K 1990, Clin Chim Acta 194:51, doi:10.1016/0009-8981(90)90303-a | Review: NSB of labelled reactants to the solid phase is "one of the greatest obstacles"; immune-complex transfer detects 1 zmol (600 molecules) of ferritin | [V] Abs |

The IgG-enzyme vs Fab'-enzyme fold difference in NSB was not found as a number this session (Ishikawa 1983 J Immunoassay
4:209, doi:10.1080/15321818308057011, is the likely source; abstract not available): UNVERIFIED. Within (e), the
largest documented levers are enzyme choice, affinity purification of the conjugate (30×) and carrier F(ab')2. These
are as large as, or larger than, plausible bead-surface effects.

## 2. Proposed surface factors (relative to the Rissin 2010 blocked bead = 1; conjugate at nM, buffer only)

These are per unit **geometric (outer) bead area**, the quantity the model multiplies. All values are judgement:
**UNVERIFIED**.

Reasoning used throughout:
- (R1) On a well-blocked, antibody-coated bead the floor is set by the labelling reagents binding the capture-antibody layer (c2). A better base chemistry can only remove the part that sits on gaps between antibodies. Expected gain from coating alone is therefore ≤ 3–10×, not the 100–1000× seen on flat surfaces without antibody (b6, b8).
- (R2) Hydrophobic bases (M-280, MyOne T1, plain PS; 120° contact angle, a1) rely entirely on the BSA/blocker layer. That layer can exchange with or be bridged by a nM IgG conjugate, so they sit above the hydrophilic carboxyl Simoa-type bead.
- (R3) Porous or swelling supports (agarose, TentaGel) expose internal area and trap conjugate. This raises NSB per geometric area by roughly the accessible internal area, and slows the wash.
- (R4) A model factor of 1 for M-280 is not supported by a source; the Rissin bead is a hydrophilic carboxyl bead (c1).

| Surface | Value | Low | High | Note |
|---|---|---|---|---|
| Rissin/Simoa carboxyl bead, covalent Ab + SuperBlock (reference) | 1 | — | — | c1, c2 |
| **Dynabeads M-280 Streptavidin, BSA-blocked (current)** | **1.5** | 1 | 5 | R2, R4. The current model range 1–3 fits but is centred low; suggest widening `high` to 5 |
| M-270 Streptavidin (hydrophilic carboxyl base, no BSA) | 1.0 | 0.5 | 3 | Closest to the Rissin bead (a1: carboxyl surface 10°). Carboxyl charge repels a net-negative conjugate (antibody-coated pI ≈ 5, a1; ALP conjugate pI UNVERIFIED), but cationic impurities can bind. Needs Tween + blocker |
| MyOne T1 (1 µm, hydrophobic, BSA-blocked) | 1.5 | 1 | 5 | Same chemistry as M-280 per area; 2.5× area per mass (a1). Per bead bed of equal mass the total NSB rises with area, so judge at equal *area* |
| MyOne C1 (1 µm, carboxyl, no BSA) | 1.0 | 0.5 | 3 | As M-270 |
| Carboxybetaine (pCB) or POEGMA/PEG brush bead, capture Ab coupled into brush | 0.3 | 0.05 | 1 | b4–b10; floor set by R1. Flat brushes with no antibody reach "undetectable" (b6, b8) but IgG is already weakly adsorbed on PEG (b9). Gain over a good blocked bead is uncertain. Custom or non-catalogue; antibody coupling density may drop (b10: thicker brush, less protein immobilised) |
| PEG-grafted resin (TentaGel, swelling PS-PEG, 10–300 µm) | 3 | 1 | 30 | R3: swelling and protein entrapment (d2, UNVERIFIED). Large beads give little area per bed |
| Silica (non-porous, BSA-blocked; bare silanol binds IgG via lysines, UNVERIFIED) | 2 | 1 | 10 | Bare silica bad; after silanisation/PEG it could approach 0.5. Treat as ≈ blocked PS |
| Porous agarose (Sepharose 4B/CL-4B type), per geometric bead area | 10 | 3 | 100 | R3: IgG-ALP (~200–300 kDa) enters 4 % agarose. Per *true* area the polysaccharide is hydrophilic (≈1), but the internal area per outer area is ≫ 10 and the wash is diffusion-limited. d1: in cell lysates, NSB is the same order as magnetic beads per bead volume |
| Plain BSA-blocked polystyrene (non-porous, e.g. 10–14 µm SA PS beads, docs/34 fallback) | 2 | 1 | 10 | R2; same class as M-280 but no vendor surface finish; Ishikawa's PS balls needed Fab' and purified conjugates (e1–e6) |

Points for the model and for the bench:
1. The bed factor `surface_factor_packed_bed` (3, 1–30) is a product of surface chemistry (above) and bed effects
   (stagnant zones, retainer area, slower wash). No source separates these. Keep it UNVERIFIED and test it.
2. On the evidence, the bead change most likely to help is **M-280 SA → M-270 SA (or C1)**: the same supplier and
   size, a hydrophilic surface like the Rissin bead, no BSA. Expected factor about 1.5 → 1.0, which is small compared
   with the reagent levers in (e).
3. A brush-coated bead may give 3× (0.05–1) but is custom. Test it only if the bench shows conjugate NSB on the bed
   dominates the blank.
4. A bench test settles this: blank beds (no IgG) of M-280 SA, M-270 SA and MyOne C1 with the same capture antibody
   load and conjugate at the working concentration and time. Read ALP activity per bead area (it fits the existing
   E1.3 "U1 conjugate NSB" experiment).
