# Literature note A — Detection and amplification of an enzyme (or other) label at one working electrode in a small stopped or slowly flowing cell

Status: COMPLETE as a literature note (2026-11-17), searched in one budget-limited session. This note becomes Part A of docs/29.

Evidence labels: **[V-abs]** read in this session in the PubMed abstract/metadata; **[V-full]** read in this
session in the full text; **[S]** search-engine summary only; **UNVERIFIED** engineering estimate; **Derived**
(formula given). Keys already in docs/01 (Das2007, Kwon2008, Akanda2011a, Han2014, Fanjul2005, DellaCiana1996,
Thomas2004, Wilson2004, Preechaworapun2008 ...) are cited by key and not re-described. In docs/01 "Akanda2011" is
doi:10.1021/ac200447b; here it is **Akanda2011a**, and the ECC paper is **Akanda2011b**.

Caution on LOD definitions. Almost every immunosensor abstract below gives "detection limit" without saying how it
was computed. Where the abstract does not say, the table writes "def. not stated". The Yang-group papers usually
compute it as blank + 3 SD from a calibration fit (Akanda2011b: "calculated from the anodic charges"), but this was
not checked in full text in this session. None of them uses blanks on different electrodes in the sense of
docs/26 §3. Treat every number as an upper bound on what the read-out can do, not as a prediction for this round.

## A.0 The question and the yardstick

What the read-out must do (Derived from docs/26 numbers):

| Quantity | Value | Basis |
|---|---|---|
| IgG at 1 pg/mL in 100 µL | 4e5 molecules (0.67 amol) | docs/26 |
| Labels on the electrode at the LOD | 1e3–1e5 (capture yield × labels per IgG) | task statement |
| ALP turnover | ~1e3 s⁻¹ (docs/01 b) | docs/01 |
| Product per label in 10 min | 6e5 molecules = 1e-18 mol | Derived: 1e3 s⁻¹ × 600 s |
| Product from 1e3 labels, 10 min | 1e-15 mol; in 10 µL → 0.1 nM; in 1 µL thin layer → 1 nM | Derived |
| Product from 1e5 labels, 10 min | 1e-13 mol; in 10 µL → 10 nM | Derived |
| Charge if all of it is oxidised once (n = 2) | 1e-15 mol → 0.19 nC; 1e-13 mol → 19 nC | Derived: Q = nFN |
| Same charge as a mean current over 60 s | 3 pA (1e3 labels) to 0.3 nA (1e5 labels) | Derived |

So at the low end the read-out has to resolve a few pA (or ~0.2 nC) on top of the background of a 1–7 mm² electrode
in an air-saturated buffer that also contains 0.1–1 mM substrate. Product LODs reported for FIA (0.12 nM HQ,
DellaCiana1996) are of the same order as the 1e3-label case in 10 µL. Hence the three routes this note examines:
(i) raise the signal per product molecule (chemical or electrode redox cycling, A.2, A.3); (ii) raise the signal per
label by accumulating an insoluble product or a metal on the electrode and stripping it (A.5); (iii) keep the
product in a small volume and count it exhaustively (A.4). Noise and background (A.7) decide which wins.

## A.1 Enzyme-product electrochemistry (question 4)

### A.1.1 ALP products on carbon, gold and platinum

| Product (substrate) | E for oxidation | Behaviour on carbon / Au | Numbers found | Ev. / source |
|---|---|---|---|---|
| Hydroquinone (HQDP) | +0.35 V vs Ag/AgCl on GC (docs/01 b); +0.42 V on IrOx (Wilson2004b) | reversible 2e⁻/2H⁺; **no passivation on repeated use** (Wilson2004a) | HQDP response 117 µA/cm² vs 31 (phenyl P) and 27 (1-naphthyl P) on IrOx; "excellent hydrolytic stability" (Wilson2004a). **Km(HQDP) = 87 µM** at pH 10.00, GC (Bekhit2021). Sulfite stabilises the HQ anodic current at high pH (Bekhit2021). HQ ECC cycling with TCEP + Ru(NH₃)₆³⁺ is faster than pAP cycling, and HQDP side reactions are "negligible compared to the APP case" (Akanda2013) | V-abs: doi:10.1016/j.bios.2004.01.013 (PMID 15308232); doi:10.1021/acs.analchem.1c03372 (PMID 34637277); doi:10.1021/ac3028855 (PMID 23327094) |
| Ascorbate (AAP) | ~+0.4 V GC (docs/01 b); fast on bare ITO (Akanda2011a) | irreversible 2e⁻ (to DHA): no reversible IDA cycling | 100 µM AA: 24.8 µA/cm² (GC), 12.0 (screen-printed C), **48.0 (Au)**; largest of 7 ALP products on all three (Preechaworapun2008) | V-abs, doi:10.1016/j.talanta.2008.03.025 (PMID 18585301) |
| p-Aminophenol (pAPP) | +0.15–0.33 V (docs/01 b) | adsorbs and electropolymerises on printed C and Au; signal tracks electroactive area; cannot be cleaned off (Buckey2022) | consistent only at ≤ 3.8 µM | V-abs, PMID 36144780 |
| 1-Naphthol (1-NP) | ~+0.4–0.5 V (UNVERIFIED) | irreversible; rapid passivation, "complete loss of electrode signal" (Wilson2004a) | — | V-abs |
| Indigo / indigo carmine (3-IP) | IC reversible at **−0.15 V vs Ag pseudo-ref on SPCE** after solubilisation in fuming H₂SO₄ (Fanjul2004) | indigo is insoluble | "picomolar levels" of ALP and HRP in solution; 3-IP serves both enzymes (Fanjul2004) | V-abs, doi:10.1016/j.talanta.2004.03.003 (PMID 18969625) |

Product detection limits at the nM level that matters (A.0): only DellaCiana1996 (HQ 0.12 nM, GC wall-jet FIA,
docs/01) was found with a stated number. No paper was found that gives the HQ or ascorbate LOD by amperometry or
DPV/SWV on printed carbon or thin-film Au in a stopped thin layer. Settles it: HQ calibration 0.1–100 nM in the
Micrux cell on C, graphene and Au strips and on the thin-film Au/Pt chips, DPV and CA at +0.2 to +0.4 V,
n ≥ 5 blanks on different strips.

### A.1.2 Substrate purity and spontaneous hydrolysis
* HQDP: "excellent hydrolytic stability" (Wilson2004a, qualitative); HQDP side reactions in ECC cycling negligible
  vs APP (Akanda2013, qualitative). No number for free HQ in commercial HQDP or for its hydrolysis rate at pH 9–10
  was found. Settles it: substrate-blank amperometry of fresh and 24 h-aged 1 mM HQDP, pH 9.5, in the cell.
* pAPP: free pAP impurity and hydrolysis unquantified (docs/01 b, critical); unchanged by this search.
* AAP: chosen by Akanda2011a for "easy dissolution and high signal-to-background"; no number found.

### A.1.3 Who sells HQDP
* **Metrohm DropSens, catalogue DRP-HQDP-0.5G**: "Hydroquinone Diphosphate is a substrate of Alkaline Phosphatase
  that generates electrochemically active hydroquinone"; 500 mg and 1 g; no purity, storage, free-HQ content or
  price on the page ("Request quote") [V, https://www.metrohm.com/en/products/d/rp-h/drp-hqdp-0_5g.html, opened
  2026-11-17]. Vendor question: certificate of analysis with free HQ (mol %) and storage conditions.
* No second commercial source was found in one search; academic groups synthesised it (Wilson2004a).

### A.1.4 Verdict (question 4)
* **Printed carbon:** HQDP → HQ stays first: reversible (works for IDA cycling and for ECC chemical cycling,
  Akanda2013), non-fouling, Km 87 µM, commercial. AAP → ascorbate is the choice only if TCEP chemical cycling
  (Akanda2011a) is adopted; on printed carbon its current per molecule is not clearly higher (12.0 µA/cm² per
  100 µM, Preechaworapun2008).
* **Thin-film gold:** ascorbate gives the largest current on Au (Preechaworapun2008), but every reductant used for
  cycling has a high background on Au (Kwon2008). HQ is the choice for Au or Pt IDA cycling (reversible).
  pAP is excluded on both materials (Buckey2022).

### A.1.5 Horseradish peroxidase read-outs (question 3)

| Key | Substrate / read | Electrode, cell | Result | Ev. |
|---|---|---|---|---|
| Fanjul2005 | TMB/H₂O₂, TMB(ox) reduced at **+0.1 V vs Ag pseudo-ref** | bare SPCE in a home-made flow cell; carrier 0.5 M H₂SO₄ at 4.3 mL/min | HRP 2e-14 M after 15 min incubation; commercial IL-6 kit read without change | V-abs, doi:10.1007/s00216-005-3084-9, PMID 15891870 |
| Freitas2022 | HRP-Ab, TMB/H₂O₂, amperometry | SPCE, 30 min assay | ovotransferrin LOD 16 ng/mL | V-abs, doi:10.3390/bios12121109, PMID 36551075 |
| Tallapragada2017 | SA-HRP, TMB, CV | SPE | HER2 LOD 4 ng/mL | V-abs, PMID 28692846 |
| Bazsefidpar2023 | HRP-Ab on Fe₃O₄@Au beads, TMB, chronoamperometry | SPCE, 1 h | E. coli 20 CFU/mL | V-abs, PMID 37232928 |
| (search summary) | TMB redox cycling on an IDA, CEA | Au IDA | ×3 vs single comb CV; >×10 in CA with a commercial ELISA kit (2018 ACS Sens) | [S] PMID 28456281 |

* The best HRP number (Fanjul2005) is an off-line FIA read of a solution in strong acid at mL/min, i.e. the
  conditions of the project's gen-1 readout, not an on-electrode stopped read. On-strip HRP/TMB protein LODs found
  are ng/mL.
* TMB(ox) is reduced near 0 V, where O₂ reduction on carbon is small but H₂O₂ reduction on Au and Pt is large
  (docs/01 b: H₂O₂ background). Precipitating TMB and 4-chloro-1-naphthol give signal-off or impedance reads (A.5.2).
* Substrate stability in a pump line or vial: no quantitative source found (TMB autoxidation rate UNVERIFIED,
  docs/01). H₂O₂ is a small molecule and may sit on a BSM line; TMB is poorly soluble in water and ready-made TMB
  solutions contain organic co-solvent (UNVERIFIED). Settles it: blank current of TMB/H₂O₂ from a BSM line after
  0, 4, 24 h.
* Poly-HRP: see A.6.
* Verdict: HRP/TMB is a fallback with good reagent supply. It has no documented advantage over ALP/HQDP at one
  electrode; on Au or Pt thin films the H₂O₂ background argues against it.

## A.2 Chemical redox cycling at one working electrode

### A.2.1 Scheme
EC redox cycling: the enzyme product P is oxidised at the electrode to P⁺; a reductant R in the solution (in large
excess) reduces P⁺ back to P near the electrode; each P molecule gives many electrons during the read. Gain needs:
fast P⁺ + R reaction; slow direct oxidation of R at the electrode (background); slow R + O₂ and R + substrate
reactions. ECC adds an outer-sphere mediator (Ru(NH₃)₆³⁺) that oxidises P in solution so that the electrode only
has to oxidise the mediator; CC/ECC adds a chemical cycle that runs during the incubation (Akanda2011b).

### A.2.2 Reports from Haesik Yang's group (KAIST/Pusan) and others

| Key | Label / substrate → product | Reductant (+ mediator) | Electrode | Technique | Analyte, LOD (def.) | Gain claimed | Ev. |
|---|---|---|---|---|---|---|---|
| Das2007 | ALP / pAPP → pAP | hydrazine | ITO + 0.5 % Fc-dendrimer | CV/amperometry, 10 min substrate | mouse IgG 100 fg/mL (10 pg/mL without hydrazine); def. not stated | LOD ×100 from cycling; another ×100 from low-Fc (low background) layer | V-abs, doi:10.1021/ac062291l |
| Kwon2008 | ALP / pAPP → pAP | NADH (no diaphorase) | Au + long-chain mixed SAM + Fc-dendrimer | — | mouse IgG 1 pg/mL; def. not stated | — ; bare Au rejected: "high background current caused by the redox reaction of the agent at highly electrocatalytic Au" | V-abs, doi:10.1039/b806302h |
| Akanda2011a | ALP / AAP → ascorbate | TCEP | bare ITO (also micropatterned ITO) | chronocoulometry | cTnI in serum 10 fg/mL (100 fg/mL without TCEP); def. not stated | LOD ×10 from TCEP; AAP best of 4 substrates for S/B | V-abs, doi:10.1021/ac200447b |
| Akanda2011b | ALP / pAPP → pAP | TCEP + Ru(NH₃)₆³⁺ (CC during incubation + ECC at read) | ITO ("highly OSR-philic") | chronocoulometry beats CV | cTnI in serum ca. 10 fg/mL, "calculated from the anodic charges" | triple amplification; no number in abstract | V-abs, doi:10.1021/ac202638y, PMID 22208164 |
| Seo2017 | ALP / 1-amino-2-naphthyl phosphate → 1A2N | ammonia-borane (H₃N-BH₃) | bare ITO | — | CK-MB ~80 fg/mL; def. not stated | 9 products and 4 reductants screened; 1A2N + AB "very high S/B"; AB also stops O₂ oxidation/polymerisation of 1A2N | V-abs, doi:10.1021/acssensors.7b00407, PMID 28806067 |
| Kang2017 | DT-diaphorase / 4-nitroso-1-naphthol → 4-amino-1-naphthol | NADH (EC + EN cycling) | ITO | — | PTH in PBS; value cut from abstract excerpt | — | V-abs, doi:10.1021/acs.analchem.7b01223, PMID 28696095 |
| Park2022b | tyrosinase / 4-methoxyphenol | ammonia-borane | ITO (modified) | — | PTH 2 pg/mL (phenol + AB: 300 pg/mL) | AB oxidises slowly at the low applied potential | V-abs, doi:10.1021/acssensors.1c02346, PMID 35195397 |
| Prayikaputri2023 | DT-diaphorase amide hydrolysis → oAN | NADH + Ru(NH₃)₆³⁺ ("five redox-cycling reactions") | ITO | — | PTH ~1 pg/mL | low background from slow NADH oxidation on ITO | V-abs, doi:10.1016/j.bios.2022.115058, PMID 36630744 |
| Singh2013 | glucose oxidase label | glucose + Ru(NH₃)₆³⁺ (EN cycling, label regenerated) | ITO | chronocoulometry | CA-125 ~0.1 U/mL with 0–10 min incubation | signal grows from t = 0: no incubation needed | V-abs, doi:10.1021/ac400573j, PMID 23663141 |
| Park2025 | diaphorase / Os(bpy)₂Cl₂ mediator | NADH | micropatterned ITO, **two-electrode, no reference** (WE and auxiliary 1.0 mm apart) | — | PSA 20 pg/mL in serum | shows a two-electrode, reference-free cell works with a robust mediator | V-abs, doi:10.1021/acssensors.5c02930, PMID 41211975 |

Points the abstracts make explicitly:
* The electrode is chosen for *slow* inner-sphere kinetics: ITO oxidises TCEP, hydrazine, NADH and ammonia-borane
  slowly, so the background stays low while the outer-sphere couple (Ru(NH₃)₆³⁺/²⁺, or P/P⁺ via a sparse ferrocene
  mediator) still reacts (Akanda2011b, Das2007, Prayikaputri2023). Gold is "not generally suitable ... because of
  the high background current" from the reductant (Kwon2008) and needs a long-chain SAM.
* The gain in LOD from the reductant is ×10 (Akanda2011a, AAP/TCEP) to ×100 (Das2007, pAP/hydrazine) relative to the
  same electrode without the reductant. Gains are not given as a current ratio per product molecule in the abstracts.
* Chronocoulometry (integrated charge) gives lower LODs than CV (Akanda2011b, Singh2013).
* The reductant also protects the product from air oxidation (hydrazine: Das2007; ammonia-borane: Seo2017).

### A.2.3 Electrode materials other than ITO: what was found
* **Printed carbon, thin-film gold, platinum, boron-doped diamond.** Two targeted searches (PubMed; web) found **no
  report of EC/ECC chemical redox cycling with hydrazine, TCEP, NaBH₄, ammonia-borane or NADH on screen-printed
  carbon, thin-film Au, Pt or BDD** in an immunoassay [searches 2026-11-17; absence of evidence, not proof]. The
  Yang group moved from Fc-dendrimer ITO and SAM/Fc-Au (2007–2008) to bare ITO (2011 onwards) precisely because the
  reductant's direct oxidation is the background (Kwon2008, Akanda2011b). BDD has the right property (slow
  inner-sphere kinetics, low capacitive background) but no immunoassay redox-cycling report was found.
* **pAP on printed electrodes.** On commercial carbon and gold screen-printed electrodes the pAP oxidation signal
  "results from its adsorption", varies with the electroactive area, cannot be restored by cleaning, and repeated
  oxidation electropolymerises pAP; lowering pAP to 3.8 µM improved consistency (Buckey2022, V-abs,
  doi:10.3390/molecules27186046, PMID 36144780). For a single-use electrode at nM product levels this is less severe,
  but it argues against pAP as the cycled species on printed carbon.

### A.2.4 Verdict for this round (question 1)
* Chemical redox cycling is the best-documented way to gain ×10–×100 in LOD at **one** working electrode and needs
  only reagents (tier 1 compatible). The reductant can be supplied in the substrate injection (TCEP, hydrazine,
  ammonia-borane are small molecules; no protein through the pump, so they may even sit on a BSM line).
* It has been demonstrated on **ITO** (bare or sparse-ferrocene) and on **SAM-blocked gold**; not on the Micrux
  materials. On printed carbon the reductant background is unknown (UNVERIFIED; bench test: CV/CA of 1–10 mM TCEP,
  ammonia-borane and hydrazine on Micrux C, graphene and Au strips at +0.1 to +0.4 V vs Ag/AgCl, 10 min stopped).
* HQ itself is cyclable: Akanda2013 found ECC cycling of HQ (TCEP + Ru(NH₃)₆³⁺) faster than that of pAP, with
  negligible HQDP side reactions, on ITO; Akanda2026 (review) calls HQDP-based systems superior. So the project's
  HQDP chemistry can take a TCEP arm without a substrate change.
* Best candidate pairing for Micrux carbon (UNVERIFIED, Derived from the abstracts' selection rules): AAP → ascorbate
  with TCEP (Akanda2011a; ascorbate oxidises fast on bare carbon and ITO, TCEP is an inner-sphere reductant that
  should oxidise slowly on carbon) or 1-amino-2-naphthyl phosphate with ammonia-borane (Seo2017). HQDP → HQ is
  cyclable in principle by TCEP but no report was found.
* Thin-film gold or platinum: expect a high reductant background (Kwon2008); usable only with a long-chain SAM,
  which then also slows the product. Not recommended for the first bench test.
* Micrux ITO is not in the electrode list for this round; if Micrux or another vendor supplies an ITO chip that fits
  the thin-film cell (10 × 6 mm), it is the material with the evidence (vendor question for docs/28).

## A.3 Electrode–electrode redox cycling on interdigitated arrays, and one-channel variants (question 5)

### A.3.1 Gains reported

| Key | Array | Mode | Gain / result | Ev. |
|---|---|---|---|---|
| Niwa1993 | IDA, pAP, ALP EIA of mouse IgG | two combs, generator–collector | steady-state pAP signal amplified vs single electrode; 1–1000 µM linear; 0.8 µL minimum sample; assay 10–1000 ng/mL | V-abs, doi:10.1021/ac00059a013, PMID 8328672 |
| Niwa1995 | carbon-film IDA in microbore LC | generator–collector | DA 32 amol, DOPAC 57 amol; **background noise 0.1 pA**; total anodic charge exceeded one oxidation per molecule | V-abs, doi:10.1016/0378-4347(95)00145-9, PMID 7493080 |
| Liu2000a, b | carbon-film interdigitated ring array, 2 µm bands, ~1 µm gap, thin-layer radial flow cell | generator–collector | collection 65–84 %, redox cycles Rc 1.7–3.7 (catechol); dopamine 15 nM; run-to-run and **detector-to-detector RSD < 10 %** | V-abs, doi:10.1016/s0021-9673(00)00632-4 (PMID 10999634); doi:10.1021/ac990825v (PMID 10740876) |
| Niwa2000 | IDA (2 µm band and gap) in a 0.042–15 nL wall-jet cell | generator–collector | cycling enhanced the current only at flow < 100 nL/min | V-abs, doi:10.1021/ac990709s, PMID 10739197 |
| Thomas2004 | Pt IDA 1.6 µm gap, beads on IDA, 20 µL drop | generator–collector | ×4, 87 % collection (docs/01) | V-abs (docs/01) |
| Han2014 | 3D IDA (ITO top and bottom of a channel) | generator–collector, thin-layer confined | ~×100; mouse IgG ~10 fg/mL (docs/01) | V-abs via Consensus (docs/01) |
| Borchers2021 | interdigitated **bipolar** electrodes (5–35 µm gaps) with a shared driving electrode, ECL read | one driving pair, BPEs floating | LOD ×10 lower as gap went from 35 to 5 µm | [S] doi:10.1002/celc.202100523 |
| Ma2014 | recessed ring-disk nanopore arrays | generator–collector, low electrolyte | ~×20 from cycling; up to ×2000 with ion enrichment (no supporting electrolyte) | [S] JACS 136:7225 |
| Ma2015 | nanopore recessed disk + unbiased planar bipolar electrode | **self-induced redox cycling** (floating electrode) | ~×30 current amplification at the disk | [S] doi:10.1039/c5sc00433k (full text returned 403) |

### A.3.2 What sets the gain (Derived)
* Time for a molecule to cross a gap g: t ≈ g²/(2D). With D(HQ) ≈ 7e-10 m²/s (UNVERIFIED, typical small
  molecule) and g = 5 µm, t ≈ 18 ms; with g = 10 µm, t ≈ 70 ms. A molecule held in the cycling zone gives about
  n/t ≈ 2/(2t) electrons per second at each comb, i.e. ~50 e⁻/s (5 µm) or ~14 e⁻/s (10 µm), against 2 e⁻ in total
  for a single oxidation. Over a 60 s read this is ~3000 and ~900 e⁻ per molecule.
* Only molecules within roughly (w + g) of the array cycle. In an open drop most product is far away, so measured
  gains are ×2–×4 (Liu2000, Thomas2004, Niwa1993). In a thin layer whose height is comparable to the gap, all
  product cycles: ×100 (Han2014). In the Micrux cell the channel height is not yet known (docs/28). For an assumed
  100 µm channel and 15 µm cycling zone, ~15 % of the product cycles (Derived, UNVERIFIED geometry).
* For an **on-electrode assay on the IDA itself**, the product is made inside the cycling zone, so a larger
  fraction is cycled before it diffuses away, provided the flow is stopped (Niwa2000: cycling only at < 100 nL/min).

### A.3.3 One potentiostat channel
* **Two-electrode connection.** Comb A = working electrode; comb B = combined counter and reference (Gamry RE and
  CE leads tied to comb B). The cell voltage (e.g. +0.3 to +0.5 V) drives HQ → BQ at A; B must carry the same
  current as a reduction: O₂ at first, then BQ arriving from A. The current is then a redox-cycling current but the
  potential of each comb floats with the HQ/BQ ratio and O₂ (UNVERIFIED behaviour; no immunoassay example found).
  Park2025 (Yang group, V-abs) shows a reference-free two-electrode ITO immunosensor working with a robust mediator,
  but with electrodes 1.0 mm apart (no cycling). No verified example of two-electrode biamperometric IDA cycling
  for an enzyme product was found in this session.
* **Floating comb (self-induced redox cycling).** Bohn's group showed ~×30 with an unbiased bipolar electrode next
  to a nanopore disk (Ma2015) and Borchers2021 drove interdigitated bipolar electrodes from one pair. Both need
  a driving voltage across the electrolyte or a nanometre-scale geometry; not shown on a commercial 5–10 µm IDA. A
  floating comb of a Micrux IDA connected to nothing would only cycle if its potential settles between the HQ
  and BQ potentials; with no current path it carries no net current (Derived). Not recommended without a test.
* **Generator–collector with two channels (tier 3)** is the proven mode: collector held at about −0.1 to 0 V,
  generator stepped or held at +0.3 to +0.4 V vs Ag/AgCl (Thomas2004 used +290/−300 mV for pAP).
* **Micrux IDA geometry** [S, distributor pages, not opened successfully]: Pt or Au ~150 nm on 50 nm Ti on glass,
  10 × 6 × 0.75 mm chip, 3.5 mm circular cell area, band/gap 10/10, 10/5 and 5/5 µm with 90, 120 and 180 pairs;
  SU-8 insulation (https://www.palmsens.com/product/micrux-ed-ide-interdigitated-electrodes;
  https://www.environmental-expert.com/products/thin-film-platinum-interdigitated-electrode-5-5-m-846957). Pair
  counts disagree between distributors; whether the chip carries reference and counter electrodes is not stated.
  Vendor questions: per-comb contacts, presence of on-chip RE/CE, exact gap and finger length.

### A.3.4 Verdict (question 5)
* The physics favours a thin-film IDA with 5 µm gaps and a stopped cell: ×10–×1000 more charge per product
  molecule than one oxidation, if the product stays in the cycling zone (Derived). Demonstrated gains in open cells
  are only ×2–×4; ×100 needs thin-layer confinement (Han2014).
* With one channel the only reasonably safe mode is the two-electrode connection, which is unverified for this use.
  It is cheap to test (tier 1: the IDA chip is a consumable). Two-channel generator–collector is the tier-3 mode.

## A.4 Stopped thin-layer accumulation, pulse techniques and exhaustive coulometry (question 6)

| Key | Format | Result | Ev. |
|---|---|---|---|
| Bekhit2021 | ALP + HQDP incubated 20 min with a 1 µL sample, then **coulometry on a commercial glucose test strip** (thin-layer, exhaustive); charge difference ΔQ as signal | ALP 0.064 U/L in 1 µL serum; RSD < 7 %; Km(HQDP) 87 µM; sulfite stabilises HQ at pH 10 | V-abs, PMID 34637277 |
| Akanda2011b, Singh2013 | on-electrode, chronocoulometry after incubation | chronocoulometry gave lower LODs than CV | V-abs |
| DellaCiana1996 | off-line FIA of a 10 min incubation | HQ 0.12 nM; ALP 1.2 fM (docs/01) | V-abs (docs/01) |

Derived from Bekhit2021: 0.064 U/L × 1 µL × 20 min = 1.3e-12 mol product if the unit (1 µmol/min, defined under
the vendor's conditions, usually pNPP) applies to HQDP → 0.25 µC at n = 2. This is about ×13 above the 1e5-label
case of A.0 (19 nC) and ×1300 above the 1e3-label case: exhaustive coulometry in a µL layer is proven at the µC
level, not at the nC level.

Derived design rules for a stopped Micrux cell:
* Exhaustive electrolysis of a thin layer of height h takes ~h²/(2D): 100 µm → 7 s; 300 µm → 64 s (D = 7e-10 m²/s,
  UNVERIFIED). A 10 µL cell over a 3 mm working electrode (7 mm²) is not a thin layer unless the channel height is
  ≤ ~0.3 mm over the electrode and the rest of the volume is outside the diffusion field (docs/28).
* The coulometric signal is the product charge minus the background charge integrated over the same window; for
  a 60 s window the background current must be stable to well below 3 pA (1e3 labels) or 0.3 nA (1e5 labels).
  Background charge from double-layer and surface oxide formation after a potential step on a 7 mm² carbon
  electrode is of order µC (UNVERIFIED: ~10–50 µF/cm² × 0.07 cm² × 0.3 V ≈ 0.2–1 µC), so the step must be applied
  before the product accumulates (hold the electrode at the read potential during the stopped period and integrate
  the faradaic excess), or a blank-step subtraction must be reproducible to < 0.1 %. This is the key reason to
  prefer continuous amperometry at a held potential, or a differential pulse read, over a single step.
* No paper was found that reaches the nC (1e-14 mol) level by coulometry on a printed electrode in a stopped
  µL cell. Settles it: HQ standards 1–100 nM in the stopped cell, held-potential amperometry for 5–15 min, charge
  integration, n ≥ 5 blanks on different strips (this is the E1.1-type experiment, docs/06).

## A.5 Enzyme-catalysed metal deposition, precipitation and metal labels with stripping (question 2)

### A.5.1 ALP / 3-indoxyl phosphate / Ag⁺ (Oviedo) and descendants

| Key | Scheme | Electrode | Read | Analyte, LOD (def.) | Time | Ev. |
|---|---|---|---|---|---|---|
| Fanjul2007 | ALP + 3-IP + Ag⁺: indoxyl reduces Ag⁺ to Ag⁰ localised at the label | streptavidin-SPCE (genosensor) | ASV of the deposited Ag | DNA; Ag stripping "14-fold more sensitive" than direct indigo-carmine voltammetry | — | V-abs, doi:10.1021/ac070624o, PMID 17569504 |
| Escamilla2009 | same, biotin-Ab + SA-ALP | SPCE, screen-printed Au, SPCE-nanoAu compared; nanoAu-SPCE most repeatable | ASV | free and total PSA (no LOD in abstract) | — | V-abs, doi:10.1016/j.bios.2009.01.043, PMID 19261459 |
| Alves2015 | same | AuNP-modified SPCE | stripping | Ara h 6 LOD 0.27 ng/mL, LOQ 0.88 ng/mL | — | V-abs, doi:10.1007/s00216-015-8879-8, PMID 26164307 |
| Alves2014 | same | AuNP-SPCE | stripping | Ara h 1 LOD 3.8 ng/mL | whole assay 3 h 50 min | V-abs, PMID 25173734 |
| Silva2020 | same | SPE | stripping | p60 protein LOD 1.5 ng/mL | < 3 h | V-abs, PMID 32456897 |
| Lai2011 | ALP-Ab on Au NPs; ALP and AuNP both catalyse Ag deposition from 3-IP + Ag⁺ | chitosan-SPCE array | anodic stripping **in KCl** | **human IgG 4.8 pg/mL**, mouse IgG 6.1 pg/mL; def. not stated; 4 decades linear | — | V-abs, doi:10.1021/ac103283p, PMID 21370869 |
| Bhatia2019 (Yang) | DT-diaphorase / 4-nitroso-1-naphthol + NADH: enzymatic + CC + CN redox cycling deposits Ag fast | (ITO type; not stated in abstract) | Ag oxidation | PTH ~100 fg/mL; def. not stated | "fast" | V-abs, doi:10.1021/acssensors.9b00456, PMID 31188576 |
| Bhatia2021 (Yang) | diaphorase + 1,4-naphthoquinone + Ag⁺, **no washing step** between deposition and stripping | — | Ag oxidation | TSH ~100 fg/mL in artificial serum | — | V-abs, doi:10.1016/j.bios.2021.113773, PMID 34763152 |
| Chao2025 (Au, not Ag) | GOx label, H₂O₂ reduces AuCl₄⁻ to Au on the immunoelectrode | MWCNT-GC | ASV of Au in 8 µL 1 M HBr–Br₂, ~6 min | human IgG 0.25 fg/mL (**S/N = 3**, not blank SD) | — | V-abs, doi:10.3390/bios15100689, PMID 41149340 |

What the abstracts show and what they do not:
* **Amplification:** ×14 over the soluble indigo-carmine read for the same label (Fanjul2007). No number was found
  for Ag atoms per ALP per minute or for the non-enzymatic Ag background (3-IP/Ag⁺ blank). Lai2011 co-catalysis by
  gold means bare Au electrodes (thin-film Au, printed Au) will **catalyse non-enzymatic deposition** too
  (Derived from Lai2011's statement that Au NPs catalyse the deposition; UNVERIFIED on bulk gold). Printed carbon is
  the natural substrate.
* **Protein LODs on printed carbon with plain ALP/3-IP/Ag:** 0.27–3.8 ng/mL (Alves2014, 2015; Silva2020) — no
  better than soluble-product reads. The pg/mL and fg/mL claims need extra catalysis (Au NPs, Lai2011) or the Yang
  redox-cycling deposition (Bhatia2019, 2021). None of them reports blank + 3 SD on different electrodes.
* **Chloride:** Ag⁺ precipitates as AgCl, so deposition must be done in a chloride-free buffer (chemistry fact).
  Lai2011 strips in KCl (a solid-state Ag → AgCl stripping peak). In the Micrux cell this means two solutions:
  chloride-free deposition mix, then a KCl stripping solution — possible from a second BSM line in tier 1.
* **Silver pseudo-reference on the same strip:** dissolved Ag⁺ (typically 0.1–1 mM in these protocols, UNVERIFIED)
  sets the potential of a bare Ag pseudo-reference and will also plate on any exposed Ag; the potential drifts as
  Ag⁺ and Cl⁻ change between the deposition and stripping solutions. No paper was found that addresses this.
  Settles it: OCP of Micrux Ag and Ag/AgCl pseudo-references vs an external Ag/AgCl in deposition mix and in KCl.
* **Flow cell:** no report of enzymatic Ag deposition in a flow cell was found (PubMed and web searches). Silver
  enhancement solutions are light-sensitive and self-nucleate (UNVERIFIED for 3-IP/Ag⁺); a vial or BSM line holding
  the mix for hours is untested. Settles it: blank Ag-stripping charge from a mix aged 0, 2, 8 h in an amber vial.
* **Time:** deposition in these papers is typically 10–20 min (UNVERIFIED; full texts not opened). Fits 60 min.

### A.5.2 Precipitating HRP substrates
4-chloro-1-naphthol and similar HRP precipitates are read by impedance or by blocking a redox probe (signal-off;
Yang2013/24419078 LOD 0.33 pg/mL AFP; Hou2013/23567634 0.64 pg/mL CEA; both on modified GC, def. not stated) [V-abs].
Signal-off reads have a blank at full signal; their electrode-to-electrode SD on printed strips is unlikely to
support a 3 SD LOD at the 1e3-label level (UNVERIFIED). Not recommended.

### A.5.3 Verdict (question 2)
Ag deposition is the only scheme found that makes the label leave a **permanent, integrable** deposit on the
electrode, so it is immune to product dilution by flow and suits a stopped cell with an exchange of solutions. On
plain printed carbon the demonstrated protein LODs are ng/mL; the pg/mL results need Au-NP co-catalysts or Yang's
diaphorase chemistry. The silver pseudo-reference, chloride handling and blank deposition are unaddressed. Rank:
tier-2/3 option or a tier-1 runner-up after bench tests of the blank; not the lead.

## A.6 Labels that put more signal on one binding event

* **Poly-HRP / poly-ALP streptavidin.** docs/01 lists ThermoPolyHRP21140 (inherited, not re-checked). No PubMed hit
  for poly-HRP in an electrochemical TMB immunosensor was found with two queries. Gain per binding event equals the
  number of active enzymes per conjugate (vendor statements, UNVERIFIED); NSB scales with conjugate size and
  stickiness, so the net LOD gain is set by the blank, not by the signal (docs/01 d). Settles it: NSB of SA-polyHRP
  vs SA-HRP on blocked Micrux strips at equal enzyme activity.
* **Nanoparticle carriers** with many enzymes (ALP-Ab/AuNP, Lai2011; GOx/AuNP, Chao2025) give the fg/mL claims
  above. They are hand-made reagents with batch variation and are outside what docs/26 calls well characterised.
* **Enzymes that regenerate the cycled species themselves** (GOx + Ru(NH₃)₆³⁺, Singh2013; diaphorase + Os mediator,
  Park2025) remove the incubation step: signal grows from t = 0. Attractive for the 60 min limit, but the
  demonstrated LODs (0.1 U/mL CA-125; 20 pg/mL PSA) are not better than ALP schemes.

## A.7 Noise, drift and background at the electrode (question 7)

| Item | Value | Source |
|---|---|---|
| Carbon-film IDA background noise in LC | 0.1 pA | Niwa1995, V-abs |
| Carbon IDRA detector-to-detector RSD | < 10 % | Liu2000a, V-abs |
| pAP signal on printed C and Au | varies with electroactive area; not restorable | Buckey2022, V-abs |
| Reductant background on Au | "high", needs long-chain SAM | Kwon2008, V-abs |
| Reductant background on ITO | low (TCEP, hydrazine with sparse Fc, NADH, ammonia-borane) | Das2007, Akanda2011a/b, Seo2017, Prayikaputri2023, V-abs |
| Printed-carbon background current, drift and strip-to-strip SD at +0.1 to +0.4 V in pH 9–10 buffer | **not found** | — |
| Gamry Reference 600+ current noise floor | not checked in this session (docs/02 holds the instrument facts) | — |

Derived: a 7 mm² electrode with ~20 µF/cm² double layer (UNVERIFIED) has C ≈ 1.4 µF; a potential drift of
1 µV/s then gives 1.4 pA of capacitive current, already of the order of the 1e3-label signal (A.0). Temperature
drift of the faradaic background and of the pseudo-reference (Ag in chloride-free buffer) adds to this. So: hold the
electrode at the read potential for ≥ 10 min before the stopped period (allowed before injection, docs/26 §3),
control temperature, and prefer the smallest electrode area that still holds the capture layer. A thin-film Au/Pt
1 mm disk (0.8 mm²) has ~9× less capacitance than a 3 mm disk. Strip-to-strip SD of the background is part of the
blank SD in this round (docs/26 §3) and has to be measured: n ≥ 10 strips per material, held-potential amperometry
in substrate buffer, 15 min.

## A.8 Summary table and ranking for the three tiers (question 8)

Signal per label per minute is Derived: ALP kcat ~1e3 s⁻¹ (docs/01) → 6e4 products/min; × electrons per product in
the read; × fraction collected. "Works in 10 µL flow cell" means the read happens in the Micrux cell with flow
stopped.

| Scheme | e⁻ per label per min (Derived, order) | Best demonstrated LOD (def.) | Main background | Electrode material | One channel | 10 µL cell | Evidence |
|---|---|---|---|---|---|---|---|
| ALP/HQDP → HQ, held-potential amperometry or coulometry, stopped | 1e5 (×2 e⁻, partial collection) | HQ 0.12 nM FIA; ALP 1.2 fM in 10 min (DellaCiana1996); on-electrode IgG ng/mL (Wilson2004b, 8 ng/mL) | substrate free HQ; carbon oxidation; capacitive drift | printed C, graphene, Au | yes | yes | V-abs; on-strip nM LOD not found |
| + chemical cycling (TCEP, ± Ru(NH₃)₆³⁺; or AAP/TCEP; 1A2N-P/ammonia-borane) | 1e6–1e7 (×10–×100) | cTnI 10 fg/mL (Akanda2011a/b), CK-MB 80 fg/mL (Seo2017); def. not stated, ITO | direct reductant oxidation (low on ITO, high on Au, **unknown on printed C**) | ITO proven; C untested; Au with SAM | yes | yes | V-abs (ITO only) |
| IDA generator–collector, HQ, stopped thin layer | 1e6–1e8 (×10–×1000 if confined) | ×100, IgG ~10 fg/mL (Han2014, 3D IDA); ×2–4 open (Thomas2004, Niwa1993) | collector O₂ reduction; comb leakage | Au/Pt thin-film IDA | **no** (two-electrode mode unverified) | yes | V-abs (open); Consensus (3D) |
| IDA two-electrode (comb B = CE+RE) | as above, unknown | none found | O₂ at comb B; floating potentials | Au/Pt IDA | yes | yes | UNVERIFIED |
| ALP/3-IP/Ag⁺ deposition + stripping | permanent deposit; ×14 vs indigo (Fanjul2007) | human IgG 4.8 pg/mL with AuNP co-catalysis (Lai2011); plain SPCE 0.27–3.8 ng/mL | non-enzymatic Ag deposition; Ag pseudo-ref; Cl⁻ | printed C | yes | yes, with a solution change; no flow report | V-abs |
| Diaphorase/quinone Ag deposition (Yang) | high | PTH, TSH ~100 fg/mL (Bhatia2019, 2021) | — | ITO type | yes | not reported | V-abs |
| HRP/TMB, reduction near 0 V | 2e3 s⁻¹ kcat (docs/01) | HRP 2e-14 M FIA (Fanjul2005); on-strip ng/mL | H₂O₂ reduction (Au, Pt); TMB autoxidation | printed C | yes | yes | V-abs |
| Precipitate, impedance (signal-off) | — | 0.3–0.6 pg/mL on modified GC | full-signal blank | GC | yes | yes | V-abs |

### Ranking (reasoned; to be confirmed by bench tests, A.9)

**Tier 1 (consumables only, one channel, capture on the electrode):**
1. **ALP/HQDP on a printed carbon (or graphene) strip, stopped-flow held-potential amperometry with charge
   integration**, plus a **TCEP chemical-cycling arm** in the substrate solution (HQ cycling by TCEP shown by
   Akanda2013 in ECC with Ru(NH₃)₆³⁺; on carbon untested). Lowest-risk route that keeps the project's chemistry;
   the TCEP arm is the cheapest possible ×10.
2. Thin-film Au IDA (5/5 µm) in the two-electrode connection with HQ: the highest ceiling, but unverified with one
   channel, and Au needs an immobilisation chemistry for capture. Worth one bench day.
3. Ag deposition on printed carbon: robust signal storage; needs chloride-free deposition then KCl strip from a
   second BSM line; reference drift and blank deposition untested.

**Tier 2 (passive parts; capture may be off-electrode, product carried into the cell):** the product is diluted
into the cell volume and the label is no longer on the electrode, so Ag deposition (needs the label on the
electrode) drops out. Rank: (1) HQ accumulated in a stopped capture column, then pushed as a slug and parked in a
thin-layer cell over a printed carbon electrode, held-potential coulometry; (2) the same with TCEP cycling in the
slug; (3) IDA two-electrode read of the parked slug.

**Tier 3 (anything, second channel allowed):** (1) **thin-layer confined IDA generator–collector with two
channels** reading HQ from a stopped slug or an on-chip assay (Han2014-type ×100), optionally with TCEP; (2)
tier-1 lead with temperature control; (3) Ag deposition with a separate external reference.

## A.9 Open questions and the bench tests that settle them

1. Reductant background on Micrux printed carbon, graphene and Au: TCEP, ammonia-borane, hydrazine 1–10 mM at
   +0.1 to +0.4 V vs the strip reference, 10 min stopped. Decides whether chemical cycling exists in tier 1.
2. HQ calibration 0.1–100 nM in the stopped Micrux cell, held potential, charge integration, n ≥ 5 strips per
   point and ≥ 10 blank strips: gives the real product LOD and the strip-to-strip blank SD (A.4, A.7).
3. Free HQ in DropSens HQDP (DRP-HQDP-0.5G) and its hydrolysis at pH 9–10 over 24 h in a vial: vendor CoA plus
   substrate-blank amperometry.
4. Micrux IDA chip: per-comb contacts, on-chip RE/CE, exact gaps; then a two-electrode HQ cycling test (comb B as
   CE+RE) against generator–collector with two channels borrowed for a day.
5. Micrux cell geometry (channel height over the WE): decides thin-layer coulometry and IDA confinement (docs/28).
6. Ag route: OCP of the Micrux Ag pseudo-reference in deposition mix and KCl; blank Ag deposition of 3-IP/Ag⁺ after
   0, 2, 8 h in an amber vial.
7. Gamry Reference 600+ noise and drift at 1–100 pA on a dummy cell of 1.4 µF (docs/02).
8. Full-text checks not done in this session: how Akanda2011a/b, Seo2017 and Lai2011 defined their LODs and how
   many blank electrodes they used.

## A.R References

All PubMed records were read in this session as abstract/metadata (V-abs) unless marked [S].

| Key | Reference |
|---|---|
| Akanda2011a | Akanda MR et al. Anal Chem 2011;83:3926–33. doi:10.1021/ac200447b, PMID 21486093 |
| Akanda2011b | Akanda MR et al. "Outer-sphere to inner-sphere" redox cycling for ultrasensitive immunosensors. Anal Chem 2012;84:1049–55 (online 2011). doi:10.1021/ac202638y, PMID 22208164 |
| Akanda2013 | Akanda MR et al. Hydroquinone diphosphate as a phosphatase substrate in enzymatic amplification combined with ECC redox cycling for E. coli O157:H7. Anal Chem 2013;85:1631–6. doi:10.1021/ac3028855, PMID 23327094 |
| Akanda2026 | Akanda MR. Redox cycling-based signal amplification in electrochemical immunosensors: a personal account. Chem Rec 2026;26:e70177. doi:10.1002/tcr.70177, PMID 42178770 (states HQDP-based systems "offered superior performance") |
| Alves2014 | Alves et al. Biosens Bioelectron 2014;64:19–24. doi:10.1016/j.bios.2014.08.026, PMID 25173734 |
| Alves2015 | Alves et al. Anal Bioanal Chem 2015;407:7157–63. doi:10.1007/s00216-015-8879-8, PMID 26164307 |
| Bazsefidpar2023 | Bazsefidpar S et al. Biosensors 2023;13:567. doi:10.3390/bios13050567, PMID 37232928 |
| Bekhit2021 | Bekhit M, Blazek T, Gorski W. Anal Chem 2021;93:14280–6. doi:10.1021/acs.analchem.1c03372, PMID 34637277 |
| Bhatia2019 | Bhatia et al. ACS Sens 2019;4:1641–7. doi:10.1021/acssensors.9b00456, PMID 31188576 |
| Bhatia2021 | Bhatia et al. Biosens Bioelectron 2021;197:113773. doi:10.1016/j.bios.2021.113773, PMID 34763152 |
| Borchers2021 | Borchers et al. ChemElectroChem 2021. doi:10.1002/celc.202100523 [S] |
| Buckey2022 | Buckey G et al. Molecules 2022;27:6046. doi:10.3390/molecules27186046, PMID 36144780 |
| Chao2025 | Chao L et al. Biosensors 2025;15:689. doi:10.3390/bios15100689, PMID 41149340 |
| Das2007, DellaCiana1996, Fanjul2005, Han2014, Kwon2008, Thomas2004, Preechaworapun2008 | see docs/01 R; Fanjul2005 doi:10.1007/s00216-005-3084-9 (PMID 15891870); Kwon2008 PMID 18936839; Das2007 PMID 17311407; Preechaworapun2008 doi:10.1016/j.talanta.2008.03.025 (PMID 18585301) |
| Escamilla2009 | Escamilla-Gómez et al. Biosens Bioelectron 2009;24:2678–83. doi:10.1016/j.bios.2009.01.043, PMID 19261459 |
| Fanjul2004 | Fanjul-Bolado P et al. Talanta 2004;64:452–7. doi:10.1016/j.talanta.2004.03.003, PMID 18969625 |
| Fanjul2007 | Fanjul-Bolado P et al. Alkaline phosphatase-catalyzed silver deposition for electrochemical detection. Anal Chem 2007;79:5272–7. doi:10.1021/ac070624o, PMID 17569504 |
| Freitas2022 | Freitas M et al. Biosensors 2022;12:1109. doi:10.3390/bios12121109, PMID 36551075 |
| Hou2013 | Hou L et al. Biosens Bioelectron 2013;47:149–56. doi:10.1016/j.bios.2013.02.035, PMID 23567634 |
| Kang2017 | Kang et al. Anal Chem 2017;89:7974–80. doi:10.1021/acs.analchem.7b01223, PMID 28696095 |
| Lai2011 | Lai G et al. Anal Chem 2011;83:2726–32. doi:10.1021/ac103283p, PMID 21370869 |
| Liu2000a | Liu Z et al. J Chromatogr A 2000;891:149–56. doi:10.1016/s0021-9673(00)00632-4, PMID 10999634 |
| Liu2000b | Liu Z et al. Anal Chem 2000;72:1315–21. doi:10.1021/ac990825v, PMID 10740876 |
| Ma2014 | Ma C, Contento NM, Bohn PW. J Am Chem Soc 2014;136:7225–8 [S] |
| Ma2015 | Ma C, Zaino LP, Bohn PW. Chem Sci 2015;6:3173–9. doi:10.1039/c5sc00433k [S] |
| MetrohmHQDP | Metrohm DropSens, Hydroquinone Diphosphate, DRP-HQDP-0.5G. https://www.metrohm.com/en/products/d/rp-h/drp-hqdp-0_5g.html [V, opened 2026-11-17] |
| MicruxIDE | Micrux thin-film IDE, distributor pages: https://www.palmsens.com/product/micrux-ed-ide-interdigitated-electrodes ; https://www.environmental-expert.com/products/thin-film-platinum-interdigitated-electrode-5-5-m-846957 [S] |
| Niwa1993 | Niwa O, Xu Y, Halsall HB, Heineman WR. Anal Chem 1993;65:1559–63. doi:10.1021/ac00059a013, PMID 8328672 |
| Niwa1995 | Niwa O et al. J Chromatogr B 1995;670:21–8. doi:10.1016/0378-4347(95)00145-9, PMID 7493080 |
| Niwa2000 | Niwa O et al. Anal Chem 2000;72:949–55. doi:10.1021/ac990709s, PMID 10739197 |
| Park2022b | Park et al. ACS Sens 2022;7:790–6. doi:10.1021/acssensors.1c02346, PMID 35195397 |
| Park2025 | Park et al. ACS Sens 2025;10:8917–24. doi:10.1021/acssensors.5c02930, PMID 41211975 |
| Prayikaputri2023 | Prayikaputri et al. Biosens Bioelectron 2023;224:115058. doi:10.1016/j.bios.2022.115058, PMID 36630744 |
| Seo2017 | Seo et al. ACS Sens 2017;2:1240–6. doi:10.1021/acssensors.7b00407, PMID 28806067 |
| Silva2020 | Silva NFD et al. Talanta 2020;216:120976. doi:10.1016/j.talanta.2020.120976, PMID 32456897 |
| Singh2013 | Singh et al. Anal Chem 2013;85:4863–8. doi:10.1021/ac400573j, PMID 23663141 |
| Tallapragada2017 | Tallapragada SD et al. Bioelectrochemistry 2017;118:25–30. doi:10.1016/j.bioelechem.2017.06.009, PMID 28692846 |
| Wilson2004a | Wilson MS, Rauh RD. Biosens Bioelectron 2004;20:276–83. doi:10.1016/j.bios.2004.01.013, PMID 15308232 |
| Wilson2004b | Wilson MS, Rauh RD. Biosens Bioelectron 2004;19:693–9. doi:10.1016/s0956-5663(03)00275-6, PMID 14709387 |
| Yang2013 | Yang F et al. Biosens Bioelectron 2014;55:360–5 (online 2013). doi:10.1016/j.bios.2013.12.040, PMID 24419078 |
