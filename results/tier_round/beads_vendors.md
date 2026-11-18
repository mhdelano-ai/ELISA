# Capture beads with plausibly lower conjugate NSB than Dynabeads M-280 Streptavidin

Desk research, 2026-11-18. Purpose: candidate beads for the tier-2 packed micro-bed (docs/34 §2) that may give a
lower LOD through lower non-specific binding (NSB) of an IgG- or F(ab')2-ALP conjugate (~200–300 kDa, ~nM).
Nothing here was measured; no vendor gives NSB data for an ALP conjugate on any of these beads.

Tags: **[V]** read this session on the page or PDF cited; **[S]** from a secondary source (search-engine summary,
distributor listing, or a vendor page that could not be opened); **UNVERIFIED** not checked; **Derived** computed
here from tagged numbers. Many manufacturer pages (thermofisher.com product pages, agilent.com store,
cytiva.com, neb.com, sigmaaldrich.com, fishersci.com) returned 403/503 or were truncated by JavaScript. Those numbers
come from manuals or PDFs that could be opened, or they are tagged [S].

## 0. Key finding: which bead defines the project's NSB rate constant

- Rissin et al. 2010 (Nat Biotechnol 28:595, doi:10.1038/nbt.1641, PMC2919230), Methods: *"2.7-µm-diam.
  carboxyl-terminated magnetic beads were purchased from Varian, Inc. (Lake Forest, CA)"*. The capture antibodies
  were coupled covalently "according to the manufacturer's instructions" with EDC/sulfo-NHS, and the beads were
  blocked with **SuperBlock T-20** (Thermo). The detection antibody (~1 nM) was biotinylated. The label was
  streptavidin-β-galactosidase at 1–50 pM, and the wash buffer was PBS + 0.1 % Tween-20. **[V]** (PMC full text)
- **There is no streptavidin bead and no Dynabead in the assay that defines `nsb_effective_rate_constant`
  (params/chemistry.yaml)**. The surface is a hydrophilic carboxyl polymer bead carrying covalent capture IgG and
  blocked with SuperBlock. The NSB measured there is that of the detection antibody plus SβG. docs/34 §2 says
  M-280 is "the surface on which the project's non-specific rate is defined". By this source, that is not
  correct.
- Chang et al. 2012 (J Immunol Methods 378:102, doi:10.1016/j.jim.2012.02.011) describes the same bead as
  *"2.5-µm diam., carboxyl-terminated paramagnetic beads (Varian)"*. **[V]** (PMC3327511 text already present in
  the scratchpad). The 2.5 vs 2.7 µm discrepancy is in the sources.
- Identity of the Varian bead: Varian was acquired by Agilent in 2010 (UNVERIFIED in this session). The
  Merck/Quanterix AAPS 2014 Simoa poster states *"Conjugated to paramagnetic beads (Agilent LodeStars 2.7
  carboxyl)"* **[V]** (PDF text). The Quanterix Homebrew kit (item 101354) SDS lists *"Homebrew Carboxylated
  Paramagnetic Beads … Carboxylated paramagnetic beads (microparticles), 2.7 um"*, with Quanterix Corporation as
  manufacturer **[V]**. It does not name the bead's origin. A search summary says the SDS names Agilent as
  supplier **[S]**, but I could not find that text. **Conclusion: Agilent LodeStars 2.7 Carboxyl (PL6727-000x) is
  the commercial product closest to the k_nsb surface (identity high-probability, [S]).**

## 1. Candidate table

Per-area numbers are Derived for smooth spheres (geometric area). "Fits bed" refers to the docs/34 retainer: a 1 µm
track-etched membrane on a 2 µm screen holds ≥ 2.8 µm beads, and the screen alone holds ≥ ~7–8 µm beads.

| # | Vendor / product (cat. no.) | Ø, CV | Material, surface | Porous? | Magnetic, density | Capacity | Vendor NSB statement | Price | Fits bed | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| ref | Thermo Dynabeads **M-280 Streptavidin** (11205D) | 2.8 µm [V-R1]; CV not on pages read | Polystyrene/Fe oxide, tosyl-activated, "hydrophobic" [V-R2]; supplied in PBS + **0.1 % BSA** [V-R1] | no | yes; 1.4 g/cm³ [V-R2] | 650–900 pmol free biotin/mg; ~10 µg biot. Ab/mg; 6–7×10⁸ beads/mL at 10 mg/mL [V-R1] → ≈16 cm²/mg, ≈0.6 µg Ab/cm² (Derived) | high background "might be caused by nonspecific binding to the BSA on the bead surface" [V-R2] | — | yes | current |
| 1 | **Agilent LodeStars 2.7 µm Carboxyl** (PL6727-0001 2 mL, -0003 10 mL, -0005 100 mL, -0006 400 mL, -0007 800 mL) | 2.7 µm, "monodispersed" [V-R5]; CV not given | Polystyrene with Fe oxide dispersed throughout + polymer shell, COOH; "hydrophilic" [S-R6] | no (not stated; UNVERIFIED) | yes; 20 % Fe [V-R5]; density UNVERIFIED | mouse IgG immunocapture > 4.0 µg/mg [V-R5]; ~3 % w/v [S-R6] | "ultralow non-specific binding"; "minimizes non-specific binding" [V-R5] | 2 mL $334, 10 mL $1,247 (Agilent DE store) [S-R6] | yes (same retainer as M-280) | **top**: the surface the model's k_nsb comes from (§0) |
| 1b | **Agilent LodeStars 2.7 µm Streptavidin** (PL6727-1001 2 mL, -1003, -1005, -1007) | 2.7 µm [V-R5] | as 1, with streptavidin | no (UNVERIFIED) | yes | biotin > 1,200 pmol/mg; biotinylated IgG > 5.0 µg/mg [V-R5] | as 1; i-PTH CLIA comparison with an "alternative 2.7 µm bead" (no numbers in text) [V-R5] | UNVERIFIED | yes | drop-in alternative keeping biotin-F(ab')2 |
| 1c | Quanterix Simoa Homebrew carboxylated paramagnetic beads (kit 101354; beads item 100451 [S-R8]) | 2.7 µm [V-R7] | carboxylated paramagnetic; "≈10¹⁰ microbeads" per 5 mL bottle [S-R8] | — | yes | — | — | UNVERIFIED | yes | same bead as 1 in practice (likely), plus Quanterix bead blocking buffer [V-R7] |
| 2 | Thermo **Dynabeads M-270 Streptavidin** (65305) | 2.8 µm [V-R1] | "hydrophilic… carboxylic acid chemistry", **not BSA-coated**; supplied in PBS + 0.09 % azide [V-R1,R2]; negatively charged, pI 4.5 [V-R2] | no | yes; 1.6 g/cm³ [V-R2] | ≥ 950 pmol biotin/mg, ~10 µg biot. Ab/mg, 6–7×10⁸ beads/mL [V-R1] | listed as the alternative where M-280 gives BSA-related background [V-R2]; recommended for "applications that are incompatible with BSA" [V-R1] | UNVERIFIED | yes | **strong**: drop-in, already the T2-1 comparator |
| 3 | Thermo Dynabeads **M-270 Epoxy** (14301) / **M-270 Carboxylic Acid** (14305D) | 2.8 µm [S-R9] | hydrophilic; epoxy (couples amine/thiol) or COOH (EDC) [S-R9] | no | yes | — | Epoxy: "very low protein and dye nonspecific binding", less need for blocking agents [S-R9, Japanese product page via search] | UNVERIFIED | yes | **strong**: covalent F(ab')2, no streptavidin and no BSA. Closest Thermo analogue of the Rissin surface |
| 4 | micromod **micromer-M PEG-COOH** 2 µm (08-56-203) and 10 µm (08-56-104); PEG-NH2 (08-55-203, 08-55-104) | 2 µm CV < 5 %; 10 µm CV < 10 % [V-R10] | styrene–maleic-acid copolymer + nano Fe oxide [S-R11]; PEG-COOH / PEG-NH2 surface (PEG length not stated) [V-R10] | no (UNVERIFIED) | yes; 1.1 g/cm³; 3.0 emu/g [V-R10] | 2 µm: 2.3×10⁸ particles/mg (≈29 cm²/mg Derived); 10 µm: 1.7×10⁶/mg (≈5.3 cm²/mg) [V-R10] | none on datasheet | UNVERIFIED | 10 µm on the screen alone; 2 µm needs < 1 µm membrane | **worth a test**: the only catalogue PEG-surface monodisperse bead found in the 2–10 µm range |
| 4b | micromod **micromer-M streptavidin** 2/3/4/5/8/10 µm (08-19-203, -303, -403, -503, -803, -104) | CV < 5 % (2–8 µm), < 10 % (10 µm) [V-R10] | as 4, streptavidin (blocking not stated) | no (UNVERIFIED) | yes; 1.1 g/cm³ | 800 ng SA/mg at 2 µm (≈28 ng SA/cm², Derived) … 200 ng SA/mg at 10 µm (≈38 ng/cm²) [V-R10] | none | UNVERIFIED | 8–10 µm on screen alone | magnetic and monodisperse at 8–10 µm. SA density ~10× below a monolayer (Derived; UNVERIFIED) |
| 4c | micromod **micromer** (non-magnetic PS) streptavidin 2 µm (01-19-203), 10 µm (01-19-104) | CV < 5 % / < 10 % [V-R10] | polystyrene, streptavidin | no | no; 1.03 g/cm³ | 900 ng SA/mg (2 µm); 200 ng SA/mg, 1.9×10⁶/mg (10 µm) [V-R10] | none | UNVERIFIED | 10 µm screen alone | monodisperse alternative to Spherotech SVP-100-4 |
| 5 | Cytiva **Sera-Mag SpeedBeads Streptavidin-Blocked** (21152104011150 1 mL, 21152104010150 5 mL, 21152104010350 100 mL) | 1 µm nominal, "monodispersed" [V-R12] | PS/acid-monomer core, two magnetite layers, polymer encapsulation; SA covalent; **"blocked with a non-surfactant, non-protein-based method"** [V-R12,R13] | "non-porous" [V-R12] | yes; ~2.0 g/cm³ [V-R12] | ~3500 pmol biotin-fluorescein/mg [V-R12]; ≈9.5×10⁸ beads/mg, ≈30 cm²/mg (Derived) | "low nonspecific binding (NSB)"; "non-specific binding is very low" (MS-compatible) [V-R12] | UNVERIFIED | needs a 0.2–0.45 µm membrane (docs/34 rejects MyOne for this reason) | protein-free block. Size is the drawback |
| 5b | Cytiva Sera-Mag SpeedBead **NeutrAvidin**-Coated (78152104011150 …) | 1 µm | NeutrAvidin, pI 6.3, deglycosylated: "generally lower nonspecific binding than avidin and streptavidin" [V-R13] | no | yes | — | as stated | UNVERIFIED | as 5 | — |
| 6 | Thermo Dynabeads **MyOne Streptavidin C1** (65001) | 1.0 µm [V-R1] | hydrophilic, COOH-based, not BSA-blocked, PBS + 0.01 % Tween [V-R1] | no | yes; ~1.8 g/cm³ [V-R2] | ≥ 2500 pmol biotin/mg; ~20 µg biot. Ab/mg; 7–12×10⁹ beads/mL [V-R1] → ≈22–38 cm²/mg | as M-270 | UNVERIFIED | needs < 1 µm membrane | NSB chemistry of M-270 at 1 µm. No gain in the model (docs/34) |
| 6b | Dynabeads MyOne Streptavidin **T1** (65601) | 1.0 µm | "tosyl-activated, hydrophobic" [S], PBS + **0.1 % BSA** [V-R1] | no | yes | 1100–1700 pmol/mg; ~20 µg Ab/mg [V-R1] | — | — | — | **no** (same chemistry as M-280) |
| 7 | Ocean NanoTech **Mono Mag Streptavidin 3 µm, hydrophilic** (MV3000) [S-R15] | 3 µm [S] | polymer-coated; "Pre-blocked with a layer of polymer"; SA monolayer covalent [V-R14 for carboxyl line; S for MV3000] | — | yes; ~25 % Fe at 3 µm [S] | UNVERIFIED | "Mono Mag has the lowest non-specific binding" (BSA-uptake figure, carboxyl MC1000) [V-R14] | UNVERIFIED | yes | second-tier: vendor NSB data are BSA adsorption only |
| 8 | Spherotech **SVP-100-4** streptavidin PS | 10.0–14.0 µm; 0.5 % w/v; 4 mL [V-R16] | polystyrene, SA (blocking not stated) | no | no; ~1.05 g/cm³ (UNVERIFIED) | not published for this size [S-R17] | none | **$360** [V-R16] | screen alone | current fallback. ≈1×10⁶ beads/mg (Derived) → ~400 beds per vial |
| 9 | micromod **sicastar-M streptavidin** 1.5 µm (39-19-153) | 1.5 µm | magnetic silica; 2.5 g/cm³; 1.4–1.6 µg SA/mg [V-R10] | not stated | yes | — | none | UNVERIFIED | needs < 1 µm membrane | silica, hydrophilic. Size marginal |
| 10 | micromod **sicastar** streptavidin 3 µm (43-19-303), 10 µm (43-19-104) | 3 µm SD < 0.85 µm; 10 µm SD < 2.5 µm [V-R10] | amorphous silica, **"porous"**, "spherical with irregularities" | **yes** | no; 1.8 g/cm³ | 70 / 67 ng SA/cm² stated [V-R10] | none | UNVERIFIED | 10 µm yes | **no**: porous, irregular, broad |
| 11 | Bangs Labs streptavidin silica 5.0 µm (CS01002) [S-R18]; streptavidin PS (CP01 series) [S] | 5 µm; CV ~10–15 % (Polysciences silica) [S] | non-porous SiO2 [S] | no | no; ~2 g/cm³ (UNVERIFIED) | per-lot CoA [S] | ProActive SA: made to maximise capacity "while minimizing nonspecific binding" [S] | UNVERIFIED | 5 µm needs the membrane | possible hydrophilic silica option. No data |
| 12 | Thermo **Pierce Streptavidin Magnetic Beads** (88816) | 1 µm [S] | "pre-blocked" [S] | — | yes | ~55 µg biot. rabbit IgG/mg; ~3500 pmol biotin-fluorescein/mg [S] | "low nonspecific binding" [S] | UNVERIFIED | needs < 1 µm membrane | no data. Size drawback |
| 13 | NEB **Hydrophilic Streptavidin Magnetic Beads** (S1421S) | 2–3 µm [S] | "hydrophilic" (undefined) [S] | — | yes; 4 mg/mL [S] | ≥ 30 µg biot. Ab/mg [S] | aimed at nucleic acids [S] | UNVERIFIED | yes | second-tier (page 403) |
| 14 | Rapp Polymere **TentaGel M NH2** 10 µm (M301002), 20 µm (M302002), 30 µm (M303002) | "narrow particle size distribution" [V-R19] | PEG-grafted PS (composition not on page; UNVERIFIED) | swelling gel (UNVERIFIED) | no | 0.15–0.35 mmol/g amine [V-R19] | none (made for organic synthesis) | €136 per 1 g [V-R19] | screen alone | **no / research only**: gel-type, the conjugate may partly enter, not made for proteins |
| 15 | Cytiva **Streptavidin Sepharose High Performance** (17511301) | ~34 µm d50V [S] | 6 % cross-linked agarose | **yes** (macroporous; IgG-size molecules enter, exclusion limit UNVERIFIED) | no | > 300 nmol biotin/mL; 6 mg biot-BSA/mL [S] | — | UNVERIFIED | soft | **no** (docs/34: internal area, slow release, compressible) |
| 16 | POROS (Thermo) streptavidin | — | perfusion PS-DVB | yes | no | no streptavidin POROS product found [S] | — | — | — | **no / not found** |
| — | Ademtech Bio-Adembeads / MasterBeads streptavidin, StreptaDivin | 200–500 nm (CV max 20 %) [S] | — | — | yes | > 600–3000 pmol/mg [S] | StreptaDivin: neutral avidin, pI 6.3, "very low non-specific binding" [S] | 0.5 mL €170 (PLUS 200 nm) [S] | **too small** | excluded (< 1 µm) |
| — | Turbobeads, micromod nanomag-D PEG-COOH 500 nm (09-56-502 [V-R10]) | nm-scale | — | — | yes | — | — | — | too small | excluded |
| — | Zwitterionic (carboxy/sulfobetaine) bead | — | — | — | — | — | — | — | — | **no catalogue product found** [S-R20]. Literature preparations only |

## 2. Notes per candidate

**1. Agilent LodeStars 2.7 Carboxyl / Streptavidin.** From the 2016 brochure 5991-1336EN (distributor copy, read
in full) [V-R5]: polystyrene microparticles with microcrystalline ferric oxide dispersed throughout, coated in a
polymer shell that "minimizes non-specific interactions". The surface is "highly controlled to provide ultralow
non-specific binding … and to reduce non-covalent biomolecule attachment". Iron content 20 %, susceptibility
> 60 m³/kg. Streptavidin version: > 1,200 pmol biotin/mg and > 5.0 µg biotin-IgG/mg. Carboxyl version: > 4.0 µg/mg
immunocapture. The brochure reports an i-PTH chemiluminescence comparison against an unnamed "Alternative 2.7 µm
bead", but the figures are graphics and give no numbers. Why it ranks first: it is the bead whose NSB the project
already uses (§0). Coupling F(ab')2 covalently to the carboxyl version and blocking without IgG reproduces the
Rissin surface in a bed of the same size as M-280. Note that Rissin's 1 % active-bead background is an NSB of the
**SβG and detection antibody at 1–50 pM / 1 nM**, not of an ALP–IgG conjugate at nM. Agilent store pages returned 403,
so current availability and price are [S]. The 2016 brochure lists the part numbers.

**2–3. Dynabeads M-270 family.** The vendor text that bears on the choice [V-R2]: M-280 = hydrophobic,
BSA-blocked; M-270 = hydrophilic, carboxylic acid-based, not BSA-coated, pI 4.5, negatively charged (can be
"sticky"/aggregate; wash in Tween-20). The trial-kit manual [V-R1] says M-270 and C1 suit "immunoassays using small
biotinylated antigens, and applications that are incompatible with … BSA". The Streptavidin version keeps the
project's biotin-F(ab')2 route. Epoxy and Carboxylic Acid remove streptavidin entirely (streptavidin itself is a
named NSB source in the Thermo FAQ [V-R2]). The Epoxy NSB claim is [S] from a search summary of the Japanese
product page. No independent M-270 vs M-280 NSB comparison was found.

**4. micromod micromer-M PEG-COOH / PEG-NH2 and streptavidin.** The datasheets are 2010 versions mirrored by
Funakoshi (micromod's own site 404'd), so check them against the current ones. The PEG chain length and grafting
density are not given. They are the only catalogue monodisperse PEG-surface magnetic beads found at 2–10 µm. The
10 µm grade would sit on the 2 µm screen alone (absolute 7–8 µm, docs/34) with magnetic handling kept. The
streptavidin grades carry only 200–900 ng SA/mg. By geometric area that is ≈ 30–40 ng/cm², well below a packed
monolayer (Derived; the monolayer value is UNVERIFIED). Whether that helps or hurts NSB is unknown.

**5. Sera-Mag SpeedBeads Streptavidin-Blocked.** The Cytiva procedure and IFU 29513808 AA were read [V-R12,R13]. Its
attraction is the protein-free proprietary block, which removes BSA and with it the risk of IgG traces in the BSA.
The drawback is the 1 µm size. The current retainer would not hold it, and docs/34 rejects 1 µm beads for pressure
and membrane reasons.

**7. Ocean NanoTech.** Their catalogue PDF [V-R14] states "Pre-blocked with a layer of polymer … significantly low
non-specific binding" and "Mono Mag has the lowest non-specific binding". The only data shown are a BSA-adsorption
figure for the carboxyl bead MC1000. The same table lists all Mono Mag carboxyl sizes as "1 µm" and "Hydrophobic",
which looks like an error in the PDF. The MV3000 3 µm hydrophilic streptavidin product is [S].

**Evidence that PEG brushes cut IgG NSB on beads (not catalogue products):**
- Chen et al. 2009, Langmuir 25:13510 (doi:10.1021/la903148n) [V-R21]. In-house 4.6 µm organosilica beads grafted
  with PEG 3400 (> 0.17 chains/nm², brush regime). Non-target antibody binding fell from ~0.004 to 4.7×10⁻⁴
  molecules/nm² (~8×) and S/N rose from 3.1 to 30.7 (~10×). Target binding was unchanged.
- Hu et al. 2024, Front Bioeng Biotechnol 12:1462203 (doi:10.3389/fbioe.2024.1462203) [V-R22]. POEGMA brushes grown
  by ARGET-ATRP on **Dynabeads M-270 Amine** suppressed FITC-BSA adsorption, more so with thicker brushes. Capture
  antibody was physically entangled in the brush. The assay ran without blocking and gave an IL-8 PEA LOD of
  18.5 fg/mL.
- Kan et al. 2020, Lab Chip 20:2122 (doi:10.1039/d0lc00267d) [V abstract]. In Simoa with ≤ 5000 beads, PSA did not
  improve "due to … increased non-specific binding". NSB per bead is a limit in that format too.
- Cheng et al. 2025/26, ACS Sens 11:696 (doi:10.1021/acssensors.5c03653) [V abstract]. "Engineered beads to
  reduce nonspecific binding" in a Simoa-like platform. Bead chemistry not read.

## 3. Ranking for this project (by expected NSB gain × fit to the bed)

1. LodeStars 2.7 Carboxyl, covalent F(ab')2, SuperBlock-type IgG-free block. It matches the k_nsb source and
   keeps the M-280 retainer.
2. Dynabeads M-270 Streptavidin. Drop-in, BSA-free, hydrophilic; already the T2-1 comparator.
3. Dynabeads M-270 Epoxy (or Carboxylic Acid). Covalent, no streptavidin, no BSA; same size and magnetism.
4. LodeStars 2.7 Streptavidin. Keeps biotin capture on the Simoa-lineage polymer.
5. micromod micromer-M PEG-COOH 10 µm (or 2 µm). PEG surface, monodisperse. The 10 µm grade needs no membrane.
6. Sera-Mag SpeedBeads Streptavidin-Blocked. Protein-free block, but 1 µm.
7. In-house PEG/POEGMA brush on M-270 Amine. Best literature evidence (~8–10× NSB reduction), but it is a
   chemistry project.
8. micromod micromer (non-magnetic) streptavidin 10 µm. A monodisperse replacement for Spherotech SVP-100-4.

Rejected: MyOne T1 (same chemistry as M-280), porous silica (sicastar 3/10 µm), agarose/Sepharose, POROS,
TentaGel/ChemMatrix-type gels (porous or swelling; made for synthesis), and everything below 1 µm (Ademtech,
nanomag, Turbobeads).

## 4. References

- R1 Thermo Fisher, Dynabeads Streptavidin Trial Kit 65801D, MAN0015762 Rev B.0 —
  https://documents.thermofisher.com/TFS-Assets/LSG/manuals/dynabeads_savtrial_kit_man.pdf [V]
- R2 Thermo Fisher, Dynabeads M-270 Streptavidin FAQs — https://www.thermofisher.com/order/catalog/product/65305/faqs [V]
- R3 Rissin DM et al. 2010, Nat Biotechnol 28:595–599, doi:10.1038/nbt.1641 (PMC2919230) [V full text]
- R4 Chang L et al. 2012, J Immunol Methods 378:102–115, doi:10.1016/j.jim.2012.02.011 (PMC3327511) [V full text]
- R5 Agilent, "LodeStars superparamagnetic particles" brochure 5991-1336EN (2016), distributor copy
  https://b2b.wagnermunz.com/download/Agilent/LodeStars.en.pdf [V]
- R6 Agilent store PL6727-0001 https://www.agilent.com/store/de_DE/Prod-PL6727-0001/PL6727-0001 (403 here; specs/price
  from search summary) [S]
- R7 Quanterix, Homebrew Assay Development Kit SDS 101354 —
  https://www.quanterix.com/wp-content/uploads/2021/01/Homebrew-Assay-Development-Kit-Bead-SDS-101354.pdf [V];
  Merck AAPS 2014 Simoa poster https://www.quanterix.com/wp-content/uploads/2020/12/AAPS_2014_Merck_Simoa_Poster.pdf [V]
- R8 Fisher listing NC0789719 / Quanterix single-plex bead SDS (item 100451) — via search [S]
- R9 Thermo Dynabeads M-270 Epoxy 14301 (JP page), M-270 Carboxylic Acid 14305D manual — via search [S]
- R10 micromod technical datasheets (2010), mirrored at https://fnkprddata.blob.core.windows.net/domestic/data/datasheet/MPT/<no>.pdf
  for 08-19-203/303/403/503/803/104, 08-55-203/104, 08-56-203/104, 01-19-203/104, 39-19-153, 43-19-103/303/104/502,
  43-02-303, 59-02-603, 09-56-502 [V]
- R11 Gentaur/Maxanim micromer-M listing https://maxanim.com/magnetic-particles/micromer-m-08-55-104 [V]
- R12 Cytiva, Sera-Mag SpeedBeads Streptavidin-Blocked procedure, https://cdn.cytivalifesciences.com/api/public/content/Vfip9mdbH0WOaEODfV0miw-pdf [V]
- R13 Cytiva IFU 29513808 AA (Sera-Mag streptavidin/NeutrAvidin), https://pdf.dutscher.com/doc/800344/800344_MEen.pdf [V]
- R14 Ocean NanoTech, "Magnetic Beads for Immunoassay and Immunoprecipitation" PDF,
  https://oceannanotech.com/web/upload/pdfs/technical/Magnetic%20Beads%20for%20Immunoassay%20and%20Immunoprecipitation%20(IP).pdf [V]
- R15 Ocean NanoTech MV3000 — via search (Ocean catalogue; Bio-Connect listing) [S]
- R16 Spherotech coated polystyrene particles price list https://spherotech.com/coa_pol_par.htm [V]
- R17 Spherotech quick particle data sheet; CDC stacks 119172 (capacity methods) — via search [S]
- R18 Bangs Labs PDS 702 (Clinisciences copy), Polysciences silica listings — via search [S]
- R19 Rapp Polymere TentaGel M NH2 page https://www.rapp-polymere.com/products/resins/narrow-particle-size-microspheres-for-solid-phase-organic-synthesis/narrow-particle-size-microspheres-with-amino-functions/tentagel-m-nh2-narrow-particle-size-amino-tentagel-microspheres [V]
- R20 Zwitterionic bead search (no commercial product) — search only [S]
- R21 Chen A et al. 2009, Langmuir 25:13510, doi:10.1021/la903148n (PMC2891774) [V]
- R22 Hu J et al. 2024, Front Bioeng Biotechnol 12:1462203, doi:10.3389/fbioe.2024.1462203 [V full text, methods/results]
- R23 Kan CW et al. 2020, Lab Chip 20:2122, doi:10.1039/d0lc00267d [V abstract, PubMed]
- R24 Cheng Y et al., ACS Sens 11:696, doi:10.1021/acssensors.5c03653 [V abstract, PubMed]
- Not opened (403/503/JS): thermofisher.com product pages 65305/65601/65001; agilent.com store; cytiva.com product page;
  neb.com S1421; sigmaaldrich/merckmillipore Sera-Mag article; fishersci; amsbio MagSi-STA PDF; Spherotech STN-21.

## Addendum (review rounds 2–3, 2026-11-18)

| Vendor / product (cat. no.) | Ø, CV | Surface | Capacity | Stock | Tag |
|---|---|---|---|---|---|
| Vector Laboratories **MagnaLINK Streptavidin Magnetic Beads 2.8 µm** (M-1003), https://vectorlabs.com/products/magnalink-streptavidin-mag-beads-2-8-m/ | 2.8 ± 0.2 µm, < 5 % CV | hydrophilic polymer encapsulation, no exposed iron; covalent streptavidin layer | free biotin ≥ 10 (elsewhere ≥ 12) nmol/mg; biotinylated IgG 750 pmol/mg (113 µg/mg) against 0.90 nmol/mg and 10 µg/mg for an unnamed "similar 2.8 µm bead" | 1 % solids (10 mg/mL) in nuclease-free water + 0.05 % azide, no BSA stated; $369 (unit size not stated) | [V] reviewers 2, 3 |
| Luminex/Diasorin **MagPlex-Avidin** | 6.5 µm, CV < 5 % [S] | deglycosylated avidin on carboxylated magnetic microspheres [V] | not checked | — | reviewers 1, 2 |
| Polysciences **ProMag HP Streptavidin** (25508); ProMag 3 Series Streptavidin (86056) | ~3 µm | "A unique surface means low nonspecific binding in protein-based systems" (HP) | not stated | — | [V] / [S] reviewer 2 |
