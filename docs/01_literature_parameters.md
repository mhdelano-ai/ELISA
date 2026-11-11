# 01 — Literature and parameter database (Task 1)

Status: complete for this pass (2026-11-11). Machine-readable values: `params/chemistry.yaml` (source keys below resolve in the reference list at the end).

Verification convention used in this document:
- **[V-abs]** value read in this session from the PubMed abstract / metadata of the primary paper.
- **[V-full]** value read in this session from the full text (PMC) of the primary paper.
- **[V-sec]** value read in this session only via a secondary source (review table, vendor page) — the secondary source is named.
- **[INHERITED]** value carried over from the previous agent's unreviewed draft; source key plausible but not re-checked in this session.
- **UNVERIFIED** no source checked; engineering estimate.

## a. Published precedent

### a.1 Summary table

| Key | Format (automatable?) | Label / substrate | Electrode / technique | Reported LOD | Sample vol. | Assay time | What limited LOD (as stated by authors) | Verif. |
|---|---|---|---|---|---|---|---|---|
| Rissin2010 / Chang2012 | Paramagnetic beads (2.7 µm, 2–10e5 per 100 µL), then femtolitre wells — digital (optical, not EC) | Streptavidin-β-gal (SβG) / resorufin-β-gal | fluorescence imaging | PSA 14 fg/mL in serum (0.4 fM); ~10–20 labelled complexes per 100 µL detectable | 100 µL (25% serum) | ~6 h (2 h capture, 45 min dAb, 30 min SβG) | NSB of detection Ab + SβG on capture beads, ≡ 1.2 fM PSA / 1.8 fM TNF-α ("typically ~1 fM") — *not* label detection | V-full |
| Xu1989 | Solid-phase sandwich, FIA-EC readout of product | ALP / pAPP → pAP | GC thin-layer, amperometric FIA | mouse IgG 0.81 pg/mL (30 min substrate incubation); pAP 24 nM | (well format) | >1 h | FIA detection limit set by capacitive transient from ionic-strength mismatch sample vs carrier | V-abs |
| Jenkins1988 | Solid-phase sandwich, LC-EC readout | ALP / phenyl phosphate → phenol | carbon paste, +0.895 V | (attomole-level ALP) | — | — | Background from **NSB of enzyme conjugate**; Tween 20 + BSA blocking cut NSB 96 % | V-abs |
| Thompson1991 | Solution ALP assay, LC-EC | ALP / pAPP | amperometric | pAP 7 nM; ALP 0.05 µg/L after 15 min (1.1 mL) | 1.1 mL | 15 min | — | V-abs |
| DellaCiana1996 | Sandwich EIA, FIA readout (wall-jet) | ALP / p-hydroxyphenyl phosphate → hydroquinone | GC +350 mV vs Ag/AgCl | HQ 1.2e-10 M; free ALP 1.2e-15 M (≈36 000 molecules) in 10 min; AFP 0.07 ng/mL | — | — | Immunoassay LOD ≫ enzyme LOD → immunochemistry/NSB limited | V-abs |
| Bauer1996 | FIA readout of ALP product with bienzyme recycling biosensor | ALP / phenyl phosphate | tyrosinase + GDH Clark electrode, 350× recycling | 3.2 fM ALP (320 zmol/100 µL) after 57.5 min | 100 µL | ~1 h | "no measurable blank" from sensor; competitive assay for 2,4-D | V-abs |
| Kokado2000 | FIA readout | ALP / ascorbic acid 2-phosphate → AA | GC +400 mV | ALP 160 amol/assay (7 amol/injection); hCG 2 mIU/mL | — | 4 h | comparable to pAPP and phenyl phosphate | V-abs (Consensus) |
| deFrutos1993 | **Flow-through fused-silica capillary (100 µm i.d.) with protein G — captures human IgG**; stop-flow incubation | F(ab)-anti-hIgG-ALP / pNPP (optical) | absorbance 405 nm | 333 zmol human IgG | — | — | (1) slow complex formation in capillary → preform complex (100× gain); (2) mass-transfer-limited capture → stop-flow; (3) **NSB of F(ab)-ALP** → reduce conjugate amount | V-abs |
| Kaneki1994 | Antibody-coated glass capillary (20 µL) + FIA-EC | ALP / pAPP | amperometric | digoxin 10 pg/mL (260 amol) | 20 µL | ~15 min binding | — | V-abs (Consensus) |
| Pollema1992; Pollema1994 | **Sequential-injection / renewable surface**: magnetic or non-magnetic beads trapped in flow cell, discarded after each assay | (fluorescence) | — | 155 ng/mL (competitive, model) | µL | 2 min reaction | Concept paper: shows bead renewal removes regeneration problem | V-abs |
| Thomas2004 | Paramagnetic microbead sandwich; beads magnetically positioned on IDA | β-gal / pAPG → pAP | Pt IDA, 1.6 µm gap; +290/−300 mV vs Ag/AgCl; 4× gain, 87 % collection | 3.5e-15 mol mouse IgG; 1000 beads in 20 µL | 20 µL drop | 10 min | — | V-abs |
| Kim2003 (MEMS conf.) | comb IDA + magnetic beads | β-gal / pAPG | comb IDA 2.4 µm gap | 70 amol β-gal in <1 min | — | <1 min | — | V-abs (Consensus) |
| Niwa1993 | IDA in 800 nL cell | ALP / pAPP | IDA redox cycling | mouse IgG 10–1000 ng/mL | 10 µL | — | — | V-abs |
| Das2007 | On-electrode sandwich (ITO, Fc-dendrimer) | ALP / pAPP, **hydrazine** chemical redox cycling | ITO, low background | mouse IgG 100 fg/mL (10 pg/mL without hydrazine) | — | 10 min substrate | Background current from electrode/mediator; hydrazine also protects pAP from air oxidation | V-abs |
| Kwon2008 | On-electrode (Au SAM + Fc-dendrimer) | ALP / pAPP, NADH redox cycling | Au | mouse IgG 1 pg/mL | — | — | Au catalyses reductant oxidation → long-chain SAM needed | V-abs |
| Akanda2011 | On-electrode (ITO, avidin adsorbed) | ALP / **AAP → AA**, TCEP redox cycling | bare ITO, no mediator | cTnI 10 fg/mL (100 fg/mL without TCEP) in serum | — | — | AAP chosen for high S/B among 4 substrates; binding at 4 °C needed for reproducibility | V-abs |
| Han2014 | Chip microchannel with 3D IDA (ITO top + bottom) | sandwich ELISA, enzyme/substrate not stated in abstract; chronocoulometry | 3D IDA ~100× | mouse IgG ~10 fg/mL; cTnI 100 fg/mL in serum | µL | — | — | V-abs (Consensus) |
| Selvaraju2008 | Magnetic beads, Au-nanocatalyst label | AuNP / p-nitrophenol + NaBH4 | Fc-D ITO | mouse IgG 1 fg/mL (CV) | — | — | — | V-abs |
| Fanjul2005 | FIA readout of commercial ELISA | HRP / TMB (ox) reduction | bare SPCE +0.1 V vs Ag pseudo-ref; 0.5 M H2SO4 carrier 4.3 mL/min | HRP 2e-14 M after 15 min | — | 15 min | — | V-abs |
| Malhotra2010 | On-electrode SWCNT forest | MWCNT–HRP (106 HRP/100 nm) / H2O2 + mediator | amperometry | IL-6 0.5 pg/mL (25 fM) in 10 µL serum | 10 µL | — | — | V-abs |
| Mani2009 | On-electrode AuNP film | 1 µm magnetic bead with 7500 HRP + Ab2 | amperometry | PSA 0.5 pg/mL in 10 µL serum | 10 µL | — | — | V-abs |

**Reading of the precedent.** (1) Enzyme *label* detection is not the bottleneck: FIA-EC readouts reach 1e-15 M ALP (DellaCiana1996), 3 fM ALP (Bauer1996) and 2e-14 M HRP (Fanjul2005), and digital ELISA detects ~10 enzymes. (2) Every group that analysed its blank found that **non-specific binding of the enzyme conjugate** sets the LOD (Jenkins1988, deFrutos1993, Rissin2010). (3) Flow-through capillary/column formats are mass-transfer limited for capture of a 150 kDa analyte; stop-flow or pre-formed complexes recover ~100× (deFrutos1993). (4) Many sub-pg/mL electrochemical claims (Das2007, Selvaraju2008, Han2014, Akanda2011) are for one-shot, disposable, manually prepared electrodes with mouse IgG model systems; blank replicate statistics are thin and none is a reusable automated flow system. Treat them as evidence that the *electrochemistry* can reach 10–100 fg/mL equivalents, not that a flow system can.


Additional precedent (verified abstracts): Qu1998 — FIA-EC (GC +325 mV) ALP/pAPP sandwich for chicken LH; background dominated by biotinylated secondary Ab binding the *capture antibody* ("specific aspecificity") plus solid-phase NSB; suppressing both improved LOD 39 → 2.5 pg/mL. Masson1995 — β-gal/pAPG FIA at +200 mV, β-gal 100 fM, mouse IgG 700 fM, PAP and PAPG stable at pH 7. Wang2001 — microchip electrophoretic separation of free/bound ALP-anti-mouse IgG then pAPP, claimed 2.5e-16 g/mL mouse IgG (one-off, not replicated here). Ishikawa1978 — "immune complex transfer" (capture on one solid phase, elute, re-capture on a second) detected 600 molecules of ferritin by removing NSB of the first solid phase: a principle directly applicable to a two-column flow system.

### a.2 Implications for this project
- A reusable flow architecture must **separate the capture step from the signal-generation volume** or keep the enzyme product in a small, quiescent volume (stop-flow), because product dilution in a flowing stream is the main signal loss.
- Capture of a 150 kDa analyte from 100 µL in ≤ 30 min needs either a high antibody concentration in suspension (beads: k = kon·[Ab] ≈ 3e5 × 2.3e-9 ≈ 7e-4 s⁻¹ → ~70 % in 30 min, derived from Chang2012) or a packed bed with short diffusion distances and low flow (stop-flow/recirculation).
- Fresh capture surface per run (bead injection, Pollema1992/1994) avoids regeneration drift and carry-over, at the cost of bead-dosing precision (a CV term).

## b. Label / substrate systems

Values and bounds are in `params/chemistry.yaml` (`enzymes.*`, `substrates.*`). Summary:

| System | kcat (s⁻¹) | Km | pH opt. | Product, E_det (vs Ag/AgCl), n | D product (m²/s) | Substrate background | Fouling / reuse | Verif. |
|---|---|---|---|---|---|---|---|---|
| ALP / pAPP → pAP | 1300–6100 for bovine IAP isozymes (Manes1998, conditions not in abstract); conjugate at RT in Tris/carbonate est. ~1000 (low 100) | 56 µM (Tris pH 9.0, Thompson1991) | 9–10; Mg²⁺/Zn²⁺; Pi inhibits (Ki ~µM, inherited) | pAP → QI, 2e⁻/2H⁺, reversible; +0.15–0.33 V | 1.03e-9 (inherited) | **free pAP impurity and non-enzymatic hydrolysis — no quantitative source found (UNVERIFIED, critical)**; pAP air-oxidises at alkaline pH (protected by hydrazine, Das2007) | pAP adsorbs/electropolymerises on carbon/Au; cleaning does not restore (Buckey2022) — problematic for a reused electrode unless a renewable or IDA geometry with µM levels | V-abs |
| ALP / AAP → ascorbate | (ALP as above) | 2.77 mM apparent (inherited, low conf.) | 9–10 | AA → DHA, 2e⁻, chemically irreversible; +0.4 V GC; fast on bare ITO | — | AAP: "easy dissolution, high S/B" (Akanda2011); commercial and cheap (Preechaworapun2008) | AA gives largest current of 7 ALP products, GC/SPC/Au (Preechaworapun2008); chemical cycling with TCEP | V-abs |
| ALP / p-hydroxyphenyl phosphate or HQDP → hydroquinone | (ALP) | — | 9.5 borate | HQ → BQ, 2e⁻, reversible; +0.35 V GC | ~9e-10 (UNVERIFIED) | HQDP "excellent hydrolytic stability" (Wilson2004) | **No passivation even with repeated use** (Wilson2004) — best fit for a reusable flow electrode; FIA LOD HQ 1.2e-10 M, ALP 1.2 fM (DellaCiana1996) | V-abs |
| ALP / phenyl or 1-naphthyl phosphate | (ALP) | 36 µM (PP) | 9–10 | phenol / naphthol, irreversible, high potential (+0.9 V phenol) | — | — | rapid, complete passivation (Wilson2004): **reject** | V-abs |
| HRP / TMB + H₂O₂ | 4.0e3 (TMB), 3.48e3 (H₂O₂) at pH 3.5, 40 °C (Gao2007 via GaoL2017); RT pH 5 est. ~2e3 | TMB 0.434 mM, H₂O₂ 3.7 mM | ~5 (substrate), read in acid | TMB(ox) reduction, ≤2e⁻; +0.1–0.33 V | — | H₂O₂ reduction background at low potential; TMB autoxidation (rate UNVERIFIED); TMB(ox) can precipitate on electrodes | azide inactivates HRP (Mabtech datasheet); HRP 2e-14 M FIA (Fanjul2005) | V-sec/V-abs |
| β-gal / pAPG → pAP | 730 (single-molecule RGP, English2006, inherited) | pAPG unknown (UNVERIFIED) | ~7.3, Mg²⁺ | pAP as above | 1.03e-9 | PAP and PAPG stable at pH 7 (Masson1995) — lower background expected than pAPP at pH 10 | pAP fouling as above, but neutral pH; IDA cycling 4× (Thomas2004), 70 amol β-gal (Kim2003) | V-abs |
| Poly-HRP / SA-polyHRP | ~20 HRP per SA polymer (Sigma S9420, inherited); research labels 106–7500 HRP (Malhotra2010, Mani2009) | — | — | — | ~2e-11 (derived) | larger labels → more NSB | — | V-abs / inherited |
| GOx | ~500 (UNVERIFIED) | 33–110 mM glucose (inherited) | — | H₂O₂, needs high potential or 2nd enzyme | — | O₂ dependence | not recommended | low |
| AuNP + ASV (non-enzyme) | — | — | — | 1.7e5 Au atoms per 18 nm NP; Au(III) LOD 5e-9 M | — | — | IgG LOD 3 pM in 35 µL (Dequaire2000): ~500× short | V-abs |

**Key numbers for the simulation (derived, not literature):** with ~1e5 bound ALP labels (≈ 25–50 % of the 4e5 IgG molecules at 1 pg/mL in 100 µL) and kcat ≈ 1000 s⁻¹, 10 min of turnover gives ~6e10 product molecules (1e-13 mol). Accumulated in 10 µL that is ~10 nM pAP; in 2 µL ~50 nM. FIA-EC LODs for pAP are 7–50 nM (Thompson1991, Xu1989, Masson1995) and for HQ 0.12 nM (DellaCiana1996). Hence (i) the product must be accumulated in a few µL (stop-flow in the capture bed, or a small closed cell) and/or amplified (IDA 4–100×, chemical cycling ~10×); (ii) **a substrate blank of 1e-4 free pAP in 1 mM pAPP (100 nM) would exceed the signal** — substrate purity, concentration (use ~4–5 Km ≈ 0.2–0.3 mM) and hydrolysis rate must be measured; the hydroquinone and AAP routes may be safer but their blank rates are also unquantified.

## c. Immunochemistry parameters

- **Rate constants.** Generic ELISA-grade antibodies (BLI, 5 antibodies): kon 9e4–1.2e6 M⁻¹s⁻¹, koff 3e-6–1.3e-3 s⁻¹, KD 12 pM–1 nM (Chang2012, V-full). Anti-human-IgG specific: goat anti-human-Fc polyclonals sub-nM; one commercial mouse anti-human-Fc mAb KD 5.5–36.3 nM with t½ 1.4–3.3 min (koff 3.5e-3–8.3e-3 s⁻¹) (Kamat2020, V-abs) — such a reagent would lose most captured IgG during a 10-min wash/substrate step. High-affinity mouse anti-human-Fc mAbs (REGN7942/7943) exist (Kamat2021) but are not known to be commercially available (UNVERIFIED). No kon/koff for anti-kappa, anti-Fab or Protein A/G full-length reagents were verified in this session; protein G B1 domain KD 4.9e-7 M is inherited unchecked.
- **Effective dissociation on dense surfaces** is slower than solution koff because of rebinding: effective KD of captured complex < 1e-11 M on digital-ELISA beads (Chang2012).
- **Surface densities.** ~274 000 Ab per 2.5 µm bead → ~1.4e16 m⁻² (Chang2012, derived). Active fraction: 23 ± 6 % for adsorbed Ab vs 91 ± 19 % via protein A (Tripathi2018); oriented Fab′ ~90 % active, up to 10× capacity gain (Peluso2003). Adsorbed polyclonal capture Abs were 8–16× more effective than mAbs in Butler1986 (older bovine-Ig model). Bead counts: 2e5–1e6 per 100 µL optimal for digital ELISA (Rissin2010). Porous protein G / NHS media: 10–30 mg IgG/mL (inherited vendor values).
- **Diffusion coefficients.** IgG 3.89e-11 m²/s; SβG ≈ β-gal 2.7e-11 m²/s (Chang2012); IgG–ALP conjugate ~3.1e-11 (derived); SA-polyHRP ~2e-11 (derived).
- **Conjugate stoichiometry.** HRP:IgG 1–3 (vendor statements, inherited), ALP:IgG ~1 (UNVERIFIED). Detection Ab ~1 nM and SβG 1–50 pM in digital ELISA vs ~10 nM in conventional assays — lower label concentration is the main NSB lever (Rissin2010).
- **Symmetric sandwich.** Butler1986 showed steric hindrance when capture and detection are both heavy-chain specific for monomeric IgG; asymmetric anti-Fab conjugates avoid it. Note however that the commercial Mabtech pair (MT145 capture, MT78 detection) uses two Fc-specific mAbs and achieves a 0.1–10 ng/mL plate range (Mabtech3850_1H).

## d. Non-specific binding and blank variability

**What sets the LOD.** For a blank-limited assay, LOD (as concentration) ≈ 3 × SD_blank / slope ≈ 3 × CV_blank × B, where B is the blank expressed as analyte-equivalent concentration (derived, simple model; also add Poisson and electrode noise terms in the simulation). Published B values:

| Setting | B (analyte-equivalent) | Source |
|---|---|---|
| Optimised digital ELISA beads, 1 nM dAb, 1–50 pM SβG | 1.2 fM (PSA), 1.8 fM (TNF-α); "typically ~1 fM" | Rissin2010, Chang2012 (V-full) |
| Commercial conventional TNF-α ELISA | 85 fM | Rissin2010 (V-full) |
| Electrochemical solid-phase EIA, BSA+Tween blocking | conjugate NSB reduced 96 % (absolute not in abstract) | Jenkins1988 |
| Protein G capillary, F(ab)-ALP | LOD improved when F(ab)-ALP amount reduced (NSB) | deFrutos1993 |

With CV_blank = 10 % (inherited range 3–20 %; capillary EIA intra/inter-assay 6–10 %, Jiang1995), LOD ≤ 6.7 fM requires **B ≤ ~20 fM-equivalent** — i.e. within ~10–20× of best-in-class Simoa and ~4× better than a commercial ELISA. This is the single most important design constraint.

**Blocking.** Tween 20 + BSA (Jenkins1988); casein outperformed BSA and gelatin for blocking IgG and second-antibody NSB, and blocked human IgG adsorption (Kenna1985); skimmed milk best in Suzawa1993. For an anti-human-IgG system **use IgG-free BSA or non-mammalian/IgG-free blockers**: many BSA grades contain bovine IgG that cross-reacting secondaries recognise (Jackson ImmunoResearch technical note, vendor statement). Casein and milk are bovine products too; their IgG content was not checked (UNVERIFIED).

**Human-IgG-specific pitfalls at pg/mL.**
1. *Environmental/operator contamination*: human IgG detected in ≥ 1/3 of micropipettor tip-cone eluates in every one of 19 labs; only 14 % of 222 eluates clean (Parry1997). Skin, saliva and dust carry IgG (UNVERIFIED for amounts); 1 pg/mL in 100 µL is only 100 fg — gloves, dedicated tips/vials, closed fluidics, and blank injections between samples are mandatory.
2. *Cross-reactivity with bovine IgG* in BSA/serum-derived reagents (above) — choose anti-human reagents cross-adsorbed against bovine (and mouse, if mouse mAbs are used) IgG.
3. *Detection Ab binding the capture Ab*: e.g. a goat anti-human IgG detection polyclonal will usually not bind a goat capture Ab, but a polyclonal anti-human IgG may cross-react with mouse capture mAbs, and anti-human-Fab/light-chain reagents can recognise conserved light-chain or framework epitopes on other species' IgG (UNVERIFIED generalisation). Qu1998 showed this "specific aspecificity" was the dominant background in an EC-EIA. The capture and detection antibodies are themselves IgGs — the analyte class — so this risk is inherent to anti-IgG assays.
4. *Protein A/G capture binds the detection antibody too* (mammalian IgG Fc) unless F(ab′)₂/Fab or chicken IgY detection reagents are used (Bird2009; deFrutos1993 used F(ab)-ALP). Chicken IgY also avoids rheumatoid factor/HAMA-type interference (Karlsson2004).
5. *Carry-over*: with a 3-log range, a blank after a 1000 pg/mL standard needs residual label/analyte < 1e-3–1e-4 (UNVERIFIED target; measure). Sample-manager needle/loop carry-over is an instrument parameter (Task 2).
6. *Adsorptive loss* of fM IgG to vials, loop and tubing (inherited estimate 10–90 %, low confidence): add IgG-free carrier protein to standards; verify by spike-recovery.

## e. Regeneration and reuse

- **Elution chemistry.** Glycine-HCl at pH ~1.5–2.5 is widely used (glycine is among Goode2015's indexed regeneration agents; 'most common' not verified); 0.1 M glycine-HCl pH 1.75 in 50 % ethylene glycol, or 0.05 M "tetraethylamine" (as written in the abstract) in 50 % ethylene glycol pH 11, or 50 % ethanol (Wijesuriya1994). Protein G releases human IgG around pH ~3 (inherited, unchecked).
- **Cycle life.** Anti-human-Fc mAb SPR surfaces: > 300 capture–regeneration cycles reproducibly (Kamat2021). Liposome FIIA immunoreactor column regenerated "hundreds of times over 3 months" without measurable loss (LocascioBrown1990). Polyclonal rabbit anti-goat on optical fibre: 70 % signal after 5 cycles (Wijesuriya1994). Only ~60 % of reported regeneration studies met a consistent success definition (Goode2015). Free ALP/HRP exposed to pH 2 will lose activity (UNVERIFIED) — irrelevant if labels are stripped, a carry-over risk if not.
- **Reloadable capture.** Protein A/G or anti-Fc "capture-of-capture": the anti-human-IgG capture antibody itself is reloaded each run, but for a human-IgG analyte a protein A/G or anti-human-Fc base layer would bind the analyte directly — usable only as a direct (non-sandwich) capture with non-binding detection reagents (Fab/IgY). Streptavidin–biotinylated capture Ab on beads is effectively irreversible (koff 5e-9 s⁻¹, Chang2012) → reload beads, not ligands.
- **Renewable surfaces.** Sequential-injection immunoassay with magnetically trapped beads discarded after each analysis (Pollema1992) and FIRSI (Pollema1994) remove regeneration drift entirely; the bead dose CV becomes a noise term.
- **Orientation chemistries.** Protein A/G-mediated or site-specific biotinylation: ~90 % active vs ~23 % for adsorption (Tripathi2018, Peluso2003).

## f. Recommended analyte standard and antibody format

**Analyte standard (choice open; recommendation).**
1. *Primary development standard:* **NISTmAb RM 8671** (humanized IgG1κ, nominal 10 mg/mL, reference value 10.003 mg/mL for lot 14HB-D-002, 12.5 mM histidine pH 6.0; Schiel2018 and NIST RMIS via search). Single molecular species with a traceable concentration — ideal for calibrating fM dilutions and for kinetic measurements. Limitation: one subclass and one light-chain type (κ); a λ- or other-subclass-blind pair would pass with it.
2. *Polyclonal "native" human IgG check standard:* e.g. the purified human IgG standard supplied with Mabtech 3850 kits (calibrated against a NIBSC standard: 1 µg = 11 mU; Mabtech3850_1H), to confirm the pair sees all subclasses/light chains. Purified human serum IgG from other vendors exists but specific catalogue numbers were not verified here.
3. Dilution to 1 pg/mL (~1e10-fold) must be gravimetric, in low-bind plastic with IgG-free carrier protein, prepared freshly and protected from operator contamination.

**Antibody pair format.**
- *Capture:* high-affinity anti-human-IgG-Fc (mouse mAb, cross-adsorbed; or affinity-purified goat F(ab′)₂ anti-human Fc), oriented via biotin–streptavidin on beads. Screen koff: reject reagents with t½ < 1 h (Kamat2020 shows some commercial anti-human-Fc mAbs have t½ of minutes).
- *Detection:* asymmetric epitope — anti-human Fab/κ+λ, ideally **F(ab′)₂ or chicken IgY** so that it binds neither protein A/G nor a mammalian capture antibody, cross-adsorbed against bovine IgG; ALP- or β-gal-labelled, used at ≤ 1 nM.
- *Verified commercial off-the-shelf option for early work:* **Mabtech 3850 series** (MT145 capture mAb, MT78 detection mAb, both Fc-specific; ALP version 3850-1AD-6, SA-ALP high-sensitivity 3850-1A-6, SA-HRP high-sensitivity 3850-1H-6 with 0.1–10 ng/mL range; azide-free buffers required for HRP). Existence and composition verified from Mabtech datasheets/web pages; kinetics not published.

## g. Most promising chemistries and open risks

1. **ALP label + hydroquinone-generating phosphate (p-hydroxyphenyl phosphate or HQDP) with amperometric/IDA detection at ~+0.35 V.** Best documented combination of low product LOD (0.12 nM HQ, 1.2 fM ALP in 10 min; DellaCiana1996), substrate hydrolytic stability, and **no electrode passivation on repeated use** (Wilson2004) — the property a reusable flow electrode needs. Risk: HQDP commercial supply unverified; HQ also air-oxidises (rate unverified).
2. **ALP + AAP → ascorbate with TCEP chemical redox cycling on ITO (or a mediator-poor carbon).** Lowest verified immunoassay LODs among electrochemical enzyme systems (10 fg/mL cTnI, Akanda2011), cheap stable commercial substrate, highest current of 7 ALP products. Risk: product oxidation is irreversible (no IDA cycling); TCEP/AA background on the chosen electrode; Km of AAP is mM.
3. **β-gal + pAPG → pAP at neutral pH with IDA redox cycling, bead-based (Thomas2004/Kim2003 lineage), SβG labelling as in digital ELISA.** Neutral pH reduces substrate hydrolysis and pAP autoxidation; reuses the Simoa reagent logic whose NSB floor (~1 fM) is the best documented. Risk: pAP fouling on reused electrodes (Buckey2022); pAPG Km/kcat not verified.
4. **ALP + pAPP → pAP with chemical cycling (hydrazine/TCEP) or IDA.** Most published; 0.8 pg/mL mouse IgG by FIA as early as Xu1989; 100 fg/mL with hydrazine (Das2007). Risks: substrate impurity/hydrolysis background (unquantified), Pi inhibition, pAP fouling.
5. **HRP/poly-HRP + TMB** as a fallback with the deepest commercial reagent support (SA-polyHRP, Mabtech kit), 2e-14 M HRP by FIA (Fanjul2005). Risks: H₂O₂ reduction background, TMB(ox) precipitation/fouling, azide sensitivity, acid read-out step.

**Architectural recommendation from the chemistry side** (for Task 3 to test): capture on streptavidin magnetic beads (renewed each run) in solution with stop-flow enzyme accumulation in a small volume, then flush to an IDA or wall-jet electrode; or immune-complex transfer between two stages to suppress first-surface NSB (Ishikawa1978 principle).

**Main open risks (ranked by LOD impact).**
1. Blank-equivalent NSB B and its run-to-run CV on the chosen surface — need B ≤ ~20 fM-equivalent at CV 10 % (only Simoa-grade optimisation has demonstrated ~1 fM).
2. Substrate blank: free product impurity and non-enzymatic hydrolysis of pAPP/AAP/HQDP — no quantitative literature found.
3. Anti-human-IgG reagent quality: koff of commercial capture Abs (some t½ of minutes), cross-reactivity with capture Ab species and with bovine IgG in blockers.
4. Human IgG contamination and adsorptive loss at the 100 fg-per-sample level.
5. Electrode fouling by pAP / TMB(ox) on a reused electrode and its drift.
6. Carry-over across the 3-log range and regeneration drift (if a regenerated rather than renewed surface is used).
7. kcat of the actual conjugate under assay conditions (vendor activity → turnover conversion has ~10× uncertainty).

## h. Changes to the inherited `chemistry.yaml`

- **Parsing bug fixed:** values written like `3.0e5` (no exponent sign) were parsed by PyYAML as *strings*, not numbers (e.g. kon, surface density, HRP kcat). All such exponents now carry a sign (`3.0e+5`); a check confirms all 118 value/low/high fields are numeric and low ≤ value ≤ high.
- Every note now starts with a verification tag ([V-full]/[V-abs]/[V-sec]/[INHERITED]/[UNVERIFIED]); inherited, unchecked sources are explicitly marked and their confidence lowered where they matter (protein G B1 KD and elution pH, conjugate ratios, Pemberton1999, deSouza2020, Kulys1980, Sun2005, Watanabe2009, Gajos2020, Cytiva/Thermo vendor values, RocheCIAP).
- **Corrected:** ALP kcat now anchored to Manes1998 (bovine IAP isozymes 1300–6100 s⁻¹) instead of a vendor-activity conversion; inherited low bound 9.7 s⁻¹ (Brooke2023, unchecked) replaced by 100 s⁻¹. Free-pAP-impurity note: the inherited citation of Ghindilis1995 as evidence of pAPP impurity was a misreading (that background was laccase-catalysed oxidative dephosphorylation); removed. pAP fouling source upgraded from conference abstract to Buckey2022 (Molecules). HRP kinetics source corrected to the review actually read (GaoL2017, Theranostics) citing Gao2007. Azide-HRP source changed to the Mabtech datasheet read here. Kim2004 (thesis) replaced by Kim2003 (MEMS conference) for the 70 amol β-gal IDA result.
- **Widened:** koff and KD capture upper bounds (Kamat2020 fast-dissociating commercial anti-human-Fc mAb). Regeneration cycles and loss per cycle updated with Kamat2021 (300 cycles) and LocascioBrown1990.
- **Added:** NISTmAb standard; Mabtech NIBSC calibration; effective KD with rebinding; SA–biotin kon; bead numbers; HQ detection potential and FIA LOD; pAPG stability; β-gal FIA LOD; chemical redox-cycling gain; IDA gain range; NSB reduction by blocking (Jenkins1988); detection-on-capture cross-reaction (Qu1998); protein A/G binding of detection Abs; symmetric-sandwich penalty (placeholder); conventional-ELISA blank 85 fM (Rissin2010).
- **Unchanged but still UNVERIFIED (high LOD impact):** pAPP free-pAP fraction and hydrolysis rate, pAP autoxidation rate, carry-over fraction, regeneration time, adsorptive loss, blank CV on a reused flow electrode.

## Tools and access notes
PubMed (search, metadata, PMC full text via WebFetch), Consensus (rate-limited; several calls returned "rate limit exceeded" and were retried or replaced by PubMed), WebSearch and WebFetch were used. The Jackson ImmunoResearch BSA page URL in the inherited file returned 404; the vendor statement was confirmed only through search snippets. Full texts were read only for Chang2012 and Rissin2010 (and a review table for HRP kinetics); all other primary values are from abstracts. Mabtech datasheet 3850-1H-6 was read in full (PDF).

## R. References

Keys used in `params/chemistry.yaml`. "INHERITED" entries were cited by the previous draft and not re-checked in this session; they are listed so keys resolve, without DOI where it was not confirmed.

| Key | Reference |
|---|---|
| Akanda2011 | Akanda MR, Aziz MA, Jo K, Tamilavan V, Hyun MH, Kim S, Yang H. Optimization of phosphatase- and redox cycling-based immunosensors and its application to ultrasensitive detection of troponin I. Anal Chem 2011;83:3926–33. doi:10.1021/ac200447b |
| Balbaied2020 | Balbaied T, et al. Electrochemical detection and capillary electrophoresis: comparative studies for ALP release from living cells. Biosensors 2020 (abstract via Consensus; DOI not confirmed) |
| Bauer1996 | Bauer CG, Eremenko AV, Ehrentreich-Förster E, Bier FF, Makower A, Halsall HB, Heineman WR, Scheller FW. Zeptomole-detecting biosensor for alkaline phosphatase in an electrochemical immunoassay for 2,4-D. Anal Chem 1996;68:2453–8. doi:10.1021/ac960218x |
| Bird2009 | Bird C, et al. Purification of immunoglobulin Y (IgY) from chicken eggs. In: Protein Protocols Handbook (Springer), 2009 (abstract via Consensus; DOI not confirmed) |
| Buckey2022 | Buckey G, et al. Adsorption and electropolymerization of p-aminophenol reduces reproducibility of electrochemical immunoassays. Molecules 2022 (via Consensus; DOI not confirmed) |
| Butler1986 | Butler JE, et al. The immunochemistry of sandwich ELISAs—I. Binding characteristics of immunoglobulins to monoclonal and polyclonal capture antibodies… Mol Immunol 1986 (via Consensus; DOI not confirmed) |
| Chang2012 | Chang L, Rissin DM, Fournier DR, Piech T, Patel PP, Wilson DH, Duffy DC. Single molecule enzyme-linked immunosorbent assays: theoretical considerations. J Immunol Methods 2012;378:102–15. doi:10.1016/j.jim.2012.02.011 (PMC3327511) |
| Chen2011 | Chen I, et al. High-sensitivity electrochemical enzyme-linked assay on a microfluidic interdigitated microelectrode. Biosens Bioelectron 2011 (via Consensus; DOI not confirmed) |
| Das2007 | Das J, Jo K, Lee JW, Yang H. Electrochemical immunosensor using p-aminophenol redox cycling by hydrazine combined with a low background current. Anal Chem 2007;79:2790–6. doi:10.1021/ac062291l |
| deFrutos1993 | de Frutos M, Paliwal SK, Regnier FE. Liquid chromatography based enzyme-amplified immunological assays in fused-silica capillaries at the zeptomole level. Anal Chem 1993;65:2159–63. doi:10.1021/ac00063a040 |
| DellaCiana1996 | Della Ciana L, Bernacca G, De Nitti C, Massaglia A. Highly sensitive amperometric enzyme immunoassay for alpha-fetoprotein in human serum. J Immunol Methods 1996;193:51–62. doi:10.1016/0022-1759(96)00044-0 |
| Dequaire2000 | Dequaire M, Degrand C, Limoges B. An electrochemical metalloimmunoassay based on a colloidal gold label. Anal Chem 2000;72:5521–8. doi:10.1021/ac000781m |
| English2006 | English BP, Min W, van Oijen AM, et al., Xie XS. Ever-fluctuating single enzyme molecules: Michaelis-Menten equation revisited. Nat Chem Biol 2006;2:87–94. doi:10.1038/nchembio759 (kcat value INHERITED, not in abstract) |
| Fanjul2005 | Fanjul-Bolado P, González-García MB, Costa-García A. Amperometric detection in TMB/HRP-based assays. Anal Bioanal Chem 2005;382:297–302. doi:10.1007/s00216-005-3084-9 |
| Gao2007 | Gao L, et al. Intrinsic peroxidase-like activity of ferromagnetic nanoparticles. Nat Nanotechnol 2007;2:577–83 (values read via GaoL2017) |
| GaoL2017 | Gao L, Fan K, Yan X. Iron oxide nanozyme: a multifunctional enzyme mimetic for biomedical applications. Theranostics 2017;7:3207–27. doi:10.7150/thno.19738 |
| Ghindilis1995 | Ghindilis A, et al. Determination of p-aminophenol and catecholamines at picomolar concentrations based on recycling enzyme amplification. Anal Chim Acta 1995 (via Consensus) |
| Goode2015 | Goode JA, Rushworth JVH, Millner PA. Biosensor regeneration: a review of common techniques and outcomes. Langmuir 2015;31:6267–76. doi:10.1021/la503533g |
| Han2014 | Han D, et al. Electrochemical signal amplification for immunosensor based on 3D interdigitated array electrodes. Anal Chem 2014 (via Consensus; DOI not confirmed) |
| Ishikawa1978 | Ishikawa E, et al. Ultrasensitive enzyme immunoassay. Scand J Immunol (review; via Consensus; year as listed by Consensus, not confirmed) |
| JacksonBSA | Jackson ImmunoResearch, BSA technical information, https://www.jacksonimmuno.com/technical/products/groups/bsa (vendor statement read via search snippets) |
| Jenkins1988 | Jenkins SH, Heineman WR, Halsall HB. Extending the detection limit of solid-phase electrochemical enzyme immunoassay to the attomole level. Anal Biochem 1988;168:292–9. doi:10.1016/0003-2697(88)90321-1 |
| Jiang1995 | Jiang T, et al. Capillary enzyme immunoassay with electrochemical detection for the determination of atrazine in water. J Agric Food Chem 1995 (via Consensus) |
| Kamat2020 | Kamat V, Rafique A, Huang T, Olsen O, Olson W. The impact of different human IgG capture molecules on the kinetics analysis of antibody-antigen interaction. Anal Biochem 2020;593:113580. doi:10.1016/j.ab.2020.113580 |
| Kamat2021 | Kamat V, Boutot C, Rafique A, et al., Huang T. High affinity human Fc specific monoclonal antibodies for capture kinetic analyses of antibody-antigen interactions. Anal Biochem 2021;640:114455. doi:10.1016/j.ab.2021.114455 |
| Kaneki1994 | Kaneki N, et al. Electrochemical enzyme immunoassay using sequential saturation technique in a 20-µl capillary: digoxin as a model analyte. Anal Chim Acta 1994 (via Consensus) |
| Karlsson2004 | Karlsson M, et al. Chicken IgY: utilizing the evolutionary advantage. World's Poultry Sci J 2004 (via Consensus) |
| Kenna1985 | Kenna J, et al. Methods for reducing non-specific antibody binding in enzyme-linked immunosorbent assays. J Immunol Methods 1985 (via Consensus) |
| Kim2003 | Kim SK, et al. Comb interdigitated arrays (IDA) electrodes for more rapid and sensitive bead-based immunoassay. Proc. IEEE MEMS 2003, Kyoto (via Consensus) |
| Kokado2000 | Kokado A, et al. New electrochemical assay of alkaline phosphatase using ascorbic acid 2-phosphate and its application to enzyme immunoassay. Anal Chim Acta 2000 (via Consensus) |
| Kwon2008 | Kwon SJ, Yang H, Jo K, Kwak J. An electrochemical immunosensor using p-aminophenol redox cycling by NADH on a SAM and ferrocene-modified Au electrodes. Analyst 2008;133:1599–604. doi:10.1039/b806302h |
| LocascioBrown1990 | Locascio-Brown L, Plant AL, Horváth V, Durst RA. Liposome flow injection immunoassay: implications for sensitivity, dynamic range, and antibody regeneration. Anal Chem 1990;62:2587–93. doi:10.1021/ac00222a013 |
| Mabtech3850_1H | Mabtech AB. Human IgG high sensitivity ELISA development kit, product code 3850-1H-6, datasheet (updated 2020-03-31), https://www.mabtech.com/sites/default/files/datasheets/3850-1H-6.pdf ; related 3850-1AD-6 and 3850-1A-6 product pages at mabtech.com |
| Malhotra2010 | Malhotra R, Patel V, Vaqué JP, Gutkind JS, Rusling JF. Ultrasensitive electrochemical immunosensor for oral cancer biomarker IL-6 using carbon nanotube forest electrodes and multilabel amplification. Anal Chem 2010;82:3118–23. doi:10.1021/ac902802b |
| Manes1998 | Manes T, Hoylaerts MF, Müller R, Lottspeich F, Hölke W, Millán JL. Genetic complexity, structure, and characterization of highly active bovine intestinal alkaline phosphatases. J Biol Chem 1998;273:23353–60. doi:10.1074/jbc.273.36.23353 |
| Mani2009 | Mani V, Chikkaveeraiah BV, Patel V, Gutkind JS, Rusling JF. Ultrasensitive immunosensor for cancer biomarker proteins using gold nanoparticle film electrodes and multienzyme-particle amplification. ACS Nano 2009;3:585–94. doi:10.1021/nn800863w |
| Masson1995 | Masson M, et al. Immunosensing with amperometric detection, using galactosidase as label and p-aminophenyl-β-D-galactopyranoside as substrate. Anal Chim Acta 1995 (via Consensus) |
| Niwa1993 | Niwa O, Xu Y, Halsall HB, Heineman WR. Small-volume voltammetric detection of 4-aminophenol with interdigitated array electrodes and its application to electrochemical enzyme immunoassay. Anal Chem 1993;65:1559–63. doi:10.1021/ac00059a013 |
| Parry1997 | Parry JV, Mortimer PP, Friderich P, Connell JA. Faulty washers and soiled micropipettors may generate false positive serological results. Clin Diagn Virol 1997;7:173–81. doi:10.1016/s0928-0197(97)00268-7 |
| Peluso2003 | Peluso P, Wilson DS, Do D, et al. Optimizing antibody immobilization strategies for the construction of protein microarrays. Anal Biochem 2003;312:113–24. doi:10.1016/s0003-2697(02)00442-6 |
| Pollema1992 | Pollema CH, Ruzicka J, Christian GD, Lernmark A. Sequential injection immunoassay utilizing immunomagnetic beads. Anal Chem 1992;64:1356–61. doi:10.1021/ac00037a010 |
| Pollema1994 | Pollema CH, Ruzicka J. Flow injection renewable surface immunoassay: a new approach to immunoanalysis with fluorescence detection. Anal Chem 1994;66:1825–31. doi:10.1021/ac00083a008 |
| Preechaworapun2008 | Preechaworapun A, et al. Investigation of the enzyme hydrolysis products of the substrates of alkaline phosphatase in electrochemical immunosensing. Talanta 2008 (via Consensus) |
| Qu1998 | Qu Y, et al. An electrochemical enzyme immunoassay for chicken luteinizing hormone: extension of the detection limit by adequate control of the nonspecific adsorption. Anal Biochem 1998 (via Consensus) |
| Reddy2013 | Reddy P, et al. Evaluation of IgY capture ELISA for sensitive detection of alpha hemolysin of S. aureus without staphylococcal protein A interference. J Immunol Methods 2013 (via Consensus) |
| Rissin2010 | Rissin DM, Kan CW, Campbell TG, et al., Duffy DC. Single-molecule enzyme-linked immunosorbent assay detects serum proteins at subfemtomolar concentrations. Nat Biotechnol 2010;28:595–9. doi:10.1038/nbt.1641 (PMC2919230) |
| Schiel2018 | Schiel JE, Turner A, Mouchahoir T, et al. The NISTmAb Reference Material 8671 value assignment, homogeneity, and stability. Anal Bioanal Chem 2018;410:2127–39. doi:10.1007/s00216-017-0800-1 (concentration values via search summary of this paper/NIST RMIS) |
| Selvaraju2008 | Selvaraju T, Das J, Han SW, Yang H. Ultrasensitive electrochemical immunosensing using magnetic beads and gold nanocatalysts. Biosens Bioelectron 2008;23:932–8. doi:10.1016/j.bios.2007.09.010 |
| Suzawa1993 | Suzawa T, et al. New approach for sensitization of solid-phase immunoassay based on controlling of nonspecific binding. Anal Sci 1993 (via Consensus) |
| Thomas2004 | Thomas JH, Kim SK, Hesketh PJ, Halsall HB, Heineman WR. Microbead-based electrochemical immunoassay with interdigitated array electrodes. Anal Biochem 2004;328:113–22. doi:10.1016/j.ab.2004.02.020 |
| Thompson1991 | Thompson RQ, Barone GC, Halsall HB, Heineman WR. Comparison of methods for following alkaline phosphatase catalysis: spectrophotometric versus amperometric detection. Anal Biochem 1991;192:90–5. doi:10.1016/0003-2697(91)90190-5 |
| Tripathi2018 | Tripathi K, Driskell JD. Quantifying bound and active antibodies conjugated to gold nanoparticles. ACS Omega 2018;3:8253–9. doi:10.1021/acsomega.8b00591 |
| Wang2001 | Wang J, et al. Electrochemical enzyme immunoassays on microchip platforms. Anal Chem 2001 (via Consensus) |
| Wijesuriya1994 | Wijesuriya D, Breslin K, Anderson G, Shriver-Lake L, Ligler FS. Regeneration of immobilized antibodies on fiber optic probes. Biosens Bioelectron 1994;9:585–92. doi:10.1016/0956-5663(94)80051-0 |
| Wilson2004 | Wilson MS, Rauh RD. Hydroquinone diphosphate: an alkaline phosphatase substrate that does not produce electrode fouling in electrochemical immunoassays. Biosens Bioelectron 2004;20:276–83. doi:10.1016/j.bios.2004.01.013 |
| Wilson2004b | Wilson MS, Rauh RD. Novel amperometric immunosensors based on iridium oxide matrices. Biosens Bioelectron 2004;19:693–9. doi:10.1016/s0956-5663(03)00275-6 |
| Wollenberger1994 | Wollenberger U, et al. Interdigitated array microelectrodes for the determination of enzyme activities. Analyst 1994 (via Consensus) |
| Xu1989 | Xu Y, Halsall HB, Heineman WR. Solid-phase electrochemical enzyme immunoassay with attomole detection limit by flow injection analysis. J Pharm Biomed Anal 1989;7:1301–11. doi:10.1016/0731-7085(89)80136-0 |
| Ying2024 | Ying X, et al. Electrochemical lateral flow immunoassay with built-in electrodes… Anal Chem 2024 (via Consensus) |
| project_brief | docs/00_project_brief.md |

INHERITED keys (cited in the previous draft, **not re-checked**; treat as unconfirmed): Brooke2023, Coburn1998, CytivaProteinG, Dixit2011, Ecke2023, Foubert2019, Gajos2020, Gao2021, Hethey2026, Ilchmann1990, Bright1990, Kandimalla2004, Kulys1980, OBrien2002, Pei2002, Pemberton1999, RocheCIAP, SigmaGOx, SigmaS9420, Simopoulos1994, Storri1998, Sun2005, Tenu1971, ThermoM280, ThermoPolyHRP21140, OriGeneHRPkit, Trau1997, Watanabe2009, Yuan1994, Zhang2023microtube, deSouza2020, Chu2005, Beitello2025, Josephy1983, Han2014 (abstract seen via Consensus only).
