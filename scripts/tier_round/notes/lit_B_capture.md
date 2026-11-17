# Part B — Capture of IgG from 100 µL in a flow system: on the electrode, in the cell, on a passive in-line element, on beads

Status: COMPLETE for this pass (2026-11-17). B.1 and B.2 kept from the interim draft; B.3–B.9 and Part C added in the second pass.
Destination: Part B of docs/29. Written under docs/26 (round brief). docs/01, docs/10 and `params/chemistry.yaml`
are cited by key and not repeated.

## B.0 Conventions and scale numbers

**Evidence labels** (docs/02 scheme, with the reading depth added as docs/26 asks):

| Label | Meaning |
|---|---|
| **[V-full]** | checked in this session in the full text of the cited paper (source of the text named in B.R) |
| **[V-abs]** | checked in this session in the PubMed abstract or record of the cited paper |
| **[S]** | search-engine summary only; the page was not opened or could not be opened |
| **UNVERIFIED** | engineering estimate or recalled value, not checked |
| **Derived** | calculated here from cited inputs; formula given |

Confidence: high = number in the primary text read; medium = abstract only, or conditions differ from ours;
low = derived with assumptions, [S] or UNVERIFIED.

**Scale numbers used throughout (Derived).**
* 1 pg/mL IgG = 6.67 fM (docs/01); 100 µL holds 6.67×10⁻¹⁵ mol/L × 1×10⁻⁴ L × 6.022×10²³ = 4.0×10⁵ molecules.
* IgG diffusion coefficient D = 3.89×10⁻¹¹ m²/s (Chang2012, docs/01). Diffusion time across a liquid layer of
  height H to an absorbing wall: τ = 4H²/(π²D) → 26 s (50 µm), 104 s (100 µm), 11 min (250 µm), 43 min (500 µm).
* Reaction-side capture velocity of an antibody-coated wall: k_r = k_on·b_m. With k_on = 3×10⁵ M⁻¹s⁻¹
  (`antibodies.kon_capture`) and b_m = 2.5×10¹⁵ active sites/m² (1×10¹⁶ IgG/m² × 0.25 active,
  `surfaces.*`): k_r = 1.25×10⁻⁶ m/s. Oriented layer (0.85 active): 4.2×10⁻⁶ m/s.

## B.1 Sandwich immunoassays with the capture antibody on the working electrode or the cell wall, under flow or stop-flow

(interim — see B.6 for the transport numbers; table of precedent to be completed)

Verified precedent so far:

| Key | Capture surface and cell | Flow regime during capture | Label / substrate / read | LOD and how defined | Time, volume | Evidence |
|---|---|---|---|---|---|---|
| Pemberton2001 | mAb adsorbed on SPCE in a thin-layer flow cell (competitive, progesterone) | flowing sample gave **7 %** of the response of quiescent pre-incubation; stop-flow (quiescent binding, then flow) restored low-noise amperograms | ALP / 1-naphthyl phosphate, +0.3 V vs Ag/AgCl | range 0–25 ng/mL; CV 12.5 % (5 replicates of milk) | not in abstract | [V-abs] |
| Rossier2001 | antibody adsorbed on the walls of a 40 nL photoablated polymer microchannel with integrated electrodes | static incubations of 5 min each | HRP conjugate; D-dimer | 0.1–100 nM range | 5 min per step | [V-abs] |
| Hoegger2007 | 8 parallel 65 nL polymer microchannels with microelectrodes (commercial cartridge) | hydrodynamic loading, programmable flow/stop | amperometric | folic acid inhibition assay in 5 min | 65 nL channels | [V-abs] |
| Nishimura2011 | Au electrode in a PDMS microchannel, tri(ethylene glycol) short alkanethiol SAM | on-chip | ALP / pAPP → pAP | leptin 13.6 pg/mL (definition not in abstract) | 30 min | [V-abs] |
| Dong2007 | screen-printed electrodes in a sealed microchannel, antibody on electropolymerised polypyrrole propylic acid | in-channel incubation | ALP / pAPP | mouse IgG 10 ng/mL (67 pM) | not in abstract | [V-abs] |
| Wilson2005; WilsonNie2006 | IrOx thin-film electrodes on glass (1 mm; 0.78 mm²), capture Ab covalent (APTES/glutaraldehyde) or adsorbed | static wells | ALP / HQDP → HQ | goat/mouse IgG 1–2 ng/mL; human IgG 3 ng/mL; interassay CV 1.9–8.2 % | — | [V-abs] |
| Duan1994; Meyerhoff1995 | capture mAb on a thioctic-acid SAM on a gold-coated microporous membrane that is also the WE | static, sample + conjugate incubated together 30 min; substrate fed from the back side | ALP / pAPP, +0.19 V vs Ag/AgCl | hCG, PSA (LOD not in abstract) | 30 min + < 1 min read | [V-abs] |
| Arevalo2011 | antigen on cysteamine SAM on electrodeposited Au in a microfluidic cell (competitive) | flow | HRP / catechol, −0.15 V | citrinin 0.1 ng/mL; ≥ 80 determinations per sensor | 45 min | [V-abs] |

## B.2 Immobilisation chemistries for the Micrux electrode materials and the non-electrode surfaces

(interim)

* Adsorbed streptavidin on pre-oxidised SPCE (drop, overnight, 4 °C), then biotinylated antibody: rabbit IgG LOD
  5×10⁻¹¹ M (7 ng/mL), sensors stable 5 months at 4 °C (DiazGonzalez2005a, [V-abs]).
* Diazonium electrografting of antibody adducts on screen-printed graphite: IgG coupled to 4-carboxymethylaniline,
  diazotised and electro-addressed; 50 fmol anti-rabbit IgG detected; reproducibility > 80 % (Corgier2005,
  Corgier2007, [V-abs]); density control and little spontaneous grafting (Polsky2008, [V-abs]).
* DTSP on gold: N-succinimidyl-3-thiopropionate coverage ≈ 1.3×10⁻¹⁰ mol/cm² (as printed in the abstract; unit
  inferred), immobilised active HRP ≈ 1.5×10⁻¹¹ mol/cm² (Darder1999, [V-abs]).
* Antibody on silica/glass: adsorbed 1.45–2.9 mg/m² depending on pH; antigen binding peaks at ≈ 1.5 mg/m² antibody;
  rinsing a physically adsorbed layer on silica with 0.15 M NaCl left ≈ 0.3 mg/m², a covalently attached layer
  (mercaptosilane + GMBS) kept 1.5 mg/m² (Zhao2012, [V-full]).

## B.3 Blocking and antifouling layers that keep electron transfer

(interim)

* mAb layer on SPCE halves the heterogeneous rate constant of pAP (6.5×10⁻⁴ → 3.0×10⁻⁴ cm/s) and hinders its
  diffusion; 1-naphthol is not affected (Pemberton1999, [V-abs]).
* Tri(ethylene glycol) short-chain alkanethiol SAMs on gold suppress protein adsorption without loss of pAP
  electroactivity (Nishimura2011, [V-abs]).
* Zwitterionic phenyl layers from aryl diazonium salts on glassy carbon resist BSA and cytochrome c as well as
  OEG SAMs, with impedance two orders of magnitude lower (Gui2013, [V-abs]).
* Cross-linked BSA with gold nanowires (or AuNP, CNT): 88 % of signal kept after 1 month in plasma
  (SabateDelRio2019, [V-abs]); BSA + pentaamine-graphene dip coating in < 1 min (Timilsina2022, [V-abs]).

**Measured non-specific densities found in this session.**

| Surface | Probe | Non-specific level | Evidence |
|---|---|---|---|
| tri(ethylene glycol)-terminated alkanethiol SAM on Au | fibrinogen (high concentration, SPR) | ≈ 2 % of a monolayer (attributed to SAM defects) | [S] (PrimeWhitesides1993 and Mrksich1995 as quoted by a patent and the Mrksich group PDF; paper not opened) |
| EG3 film on Si(111) | fibrinogen | ≈ 30 % of a monolayer | [S] (patent summary) |
| streptavidin beads, digital ELISA, 1 nM detection Ab, 1–50 pM SβG | blank expressed as analyte | 1.2 fM PSA, 1.8 fM TNF-α, "typically ≈ 1 fM" | Rissin2010, Chang2012 (docs/01, [V-full]) |
| conventional plate ELISA | blank expressed as analyte | ≈ 85 fM | Rissin2010 (docs/01) |
| solid-phase EC-EIA, BSA + Tween 20 | ALP conjugate NSB | reduced by 96 % vs unblocked (absolute not given) | Jenkins1988 (docs/01, [V-abs]) |
| FIA-EC sandwich, chicken LH | detection Ab binding the capture Ab + solid-phase NSB | suppressing both: LOD 39 → 2.5 pg/mL | Qu1998 (docs/01, [V-abs]) |
| blocked SPCE (BSA, casein or milk) | ALP or HRP conjugate, molecules per area | **not found** in this session | — |

**What NSB density an electrode can afford (Derived).** docs/01 §d sets the blank budget at B ≤ ≈ 20 fM-equivalent
for CV_blank 10 %. 20 fM in 100 µL = 1.2×10⁶ molecules; with capture yield η = 0.5 the bound-label equivalent is
≈ 6×10⁵ labels on the whole capture surface. Spread over a working electrode of 1–10 mm² (Micrux WE area
UNVERIFIED, docs/28) this is ≤ 6×10⁴–6×10⁵ labels/mm² = 6×10¹⁰–6×10¹¹ m⁻². A full IgG-size monolayer is
≈ 1×10¹⁶ m⁻² (docs/01). **The electrode may carry at most 10⁻⁵–10⁻⁴ of a monolayer of conjugate**, i.e. 200–2000×
below the best OEG SAM figure above (which was measured at mg/mL protein, so the gap at nM conjugate is smaller,
but no number at nM was found). Beads reach the ≈ 1 fM level only with nM detection antibody and pM enzyme
label, extensive washing, and a large bead area (2×10⁵ × 2.0×10⁻¹¹ m² ≈ 4 mm² for 2.7 µm beads, Derived) that is
comparable with an electrode area. The conclusion is not that beads bind less per area, but that their published
blank is measured; for blocked SPCE in a flow cell the per-area NSB at nM conjugate must be measured (bench: ALP
conjugate 0.1–1 nM, 10 min, wash, HQDP read, on 10 electrodes; report labels/mm² from an ALP calibration).

**Blockers that keep electron transfer to HQ or pAP (ranking from the sources above).**
1. Short OEG or tri(ethylene glycol) alkanethiol SAM on Au thin-film chips: protein-resistant without loss of pAP
   electroactivity (Nishimura2011, [V-abs]); requires the gold Micrux chip.
2. Zwitterionic or OEG aryl-diazonium layer on carbon: protein resistance like OEG SAMs with impedance 100× lower
   (Gui2013, [V-abs]); applicable to SPCE.
3. BSA + Tween 20 (Jenkins1988) or casein (Kenna1985), IgG-free grades only (docs/01); a protein layer slows HQ/pAP
   kinetics modestly (mAb layer halves k⁰ of pAP, Pemberton1999) — acceptable for amperometry at +0.35 V.
4. Cross-linked BSA composites (SabateDelRio2019) — built for antifouling in plasma, thicker; not needed in buffer.

## B.4 Passive in-line capture elements (tier 2)

### B.4.1 Superparamagnetic beads held by a fixed magnet in a flow system

| Key | Set-up | Beads and how they are held | Assay, label, read | LOD (definition) | Time | Evidence |
|---|---|---|---|---|---|---|
| Biscay2014 | FIA; commercial-type flow cell for screen-printed electrodes with a magnet **integrated under the WE** | streptavidin beads (incubated off-line 15 min with analyte and conjugate, washed), then **100 µL bead suspension injected** and held on the WE; 30 s later 100 µL TMB injected | competitive biotin, HRP / TMB, −0.2 V | linear 0.01–1 nM (LOD definition not in abstract) | FIA read < 1 min after capture | [V-abs] |
| Dominguez2012 | automated flow system; **beads injected onto an SPCE** and held there; incubation, washing and reading programmed | antigen-coated magnetic beads | indirect competitive, ALP 2° Ab / 1-naphthyl phosphate | okadaic acid 0.15 µg/L (definition not in abstract) | automated; time not in abstract | [V-abs] |
| Hirakawa2006 | SIA; syringe pump + selection valve; **neodymium magnet on an "immunoreaction cell" upstream** of a separate amperometric detector | beads introduced, trapped and released "by the neodymium magnet and by adjusting the flow" | competitive, ALP / pAPP → pAP read downstream at +0.2 V | range 0–500 ppb (no LOD in abstract) | < 15 min | [V-abs] |
| Soh2004 | SIA, Sm–Co magnet under a flow cell, chemiluminescence | anti-Vg mAb on epoxy-agarose magnetic beads | **sandwich**, HRP; optimum 20 min per immunoreaction step | Vg ≈ 2 ng/mL | ≈ 45 min | [V-abs] |
| Zhang2007 (Imato group) | SIA, Nd magnet beneath a flow-through cell; beads discarded after each run | mAb on polylactate-coated beads | competitive, HRP-CL | IC80 ≈ 10 ppb | < 15 min | [V-abs] |
| Sole1998 | beads held on the transducer inside a flow system; "renewed for each analysis" | rabbit IgG model | electrochemical | µM range | < 30 min | [V-abs] (in draft) |
| Choi2001 | Heineman/Halsall/Ahn microfluidic motherboard; "biofilter" with planar electromagnet, separate EC sensor | beads used as carriers and capture surface | sandwich-type, EC | not in abstract | < 20 min, < 50 µL wasted per run | [V-abs] |
| MolineroFernandez2020 | glass microchip, magnet on top of the channel, electrokinetic pumping (no pressure flow) | M-280 streptavidin beads; immunocomplex formed off-chip | procalcitonin sandwich, HRP / HQ + H₂O₂, −0.2 V | 0.04 ng/mL (3·s/m, s of lowest standard, n = 10); intra-assay CV 5 %, inter-batch 9 % | < 20 min | [V-full] |
| Thomas2004 (docs/01) | beads magnetically positioned on a Pt IDA | 1000 beads in 20 µL | β-gal / pAPG, redox cycling | 3.5×10⁻¹⁵ mol mouse IgG | 10 min | docs/01 [V-abs] |

**What the precedent shows.**
* Holding a bead plug on an SPCE with a magnet in a flow cell is established (Biscay2014; Dominguez2012). In both,
  the **immune reaction ran off-line or in a stirred volume**; the flow cell only collected the beads and read the
  product. No paper found runs the analyte capture itself as a slow flow-through of 100 µL over a magnetically held
  bead plug and reports the capture efficiency. **Not found** — bench measurement: spike 10 pg/mL, run the plug at
  2–3 flow rates, measure bead-bound vs. breakthrough IgG by a reference ELISA.
* Systems that capture in flow over held beads (Soh2004, Imato group) needed **≈ 20 min per immunoreaction step**
  with a stopped or slowly moving zone and reached only ng/mL. Their LODs were set by chemiluminescence and
  low-affinity reagents, not by the format.
* Two product paths exist: beads **on the WE** (Biscay2014, Dominguez2012: product forms at the electrode; stopped
  flow makes it accumulate in the cell volume) and beads **upstream** (Hirakawa2006: product carried to the
  detector, diluted by dispersion). For a 10 µL cell, on-WE beads plus stopped flow is the stronger choice.
* Renewal: beads released by removing the magnet or by high flow, i.e. by an actuator or a hand step. With a
  fixed magnet (tier 2) the bead plug stays until the cell is opened; that is acceptable here because a fresh
  consumable per determination is allowed (docs/26 §3).

**Flow at which beads stay (Derived, low confidence).** Force on a saturated bead F = m_sat·∇B. M-280: Fe
12 wt % (vendor, [S], thermofisher.com Dynabeads technical FAQ); as maghemite (70 % Fe) 17 wt % of a
1.6×10⁻¹⁴ kg bead (Ø 2.8 µm, 1.4 g/cm³ dry, [S]); M_s of maghemite 60–74 A·m²/kg (UNVERIFIED textbook range;
Fonnum2005 gives intrinsic 340 kA/m, [S]) → m_sat ≈ 1.7–2.0×10⁻¹³ A·m². Gradient of a mm-scale NdFeB magnet:
10 T/m at a few mm, 100–300 T/m within ≈ 0.5 mm of its face (UNVERIFIED engineering estimate). F = 2–60 pN;
magnetophoretic velocity v_m = F/(6πμr) = 0.06–2 mm/s. A bead crossing a 0.1–0.5 mm channel gap over a 2 mm
long magnet needs mean flow velocity u < v_m·L/H. For H = 0.1 mm, cross-section 0.1 × 2 mm, v_m = 0.6 mm/s:
u < 12 mm/s → Q < 140 µL/min. Beads held at flows of ~10–100 µL/min are therefore plausible; the true limit is
set by the magnet position relative to the Micrux channel (docs/28) and must be measured (bead count in effluent
vs. flow). MyOne (1 µm) beads carry ≈ 10–20× less moment and see 3× less drag: v_m ≈ 4–7× lower (Derived,
scaling m ∝ r³ at similar Fe content — UNVERIFIED for MyOne Fe content).

**Capture efficiency of a held bead plug (Derived).** A packed plug of N beads of radius a in volume V_p has
transport distances of ≈ a few µm; capture of IgG during flow-through is then reaction-limited: fraction captured
≈ 1 − exp(−k_on·[Ab]_plug·τ_res), with [Ab]_plug = N·n_Ab/(N_A·V_p) and τ_res = V_p·ε/Q. For 2×10⁶ M-280 beads
(≈ 0.13 mg, ≈ 1.1×10⁻¹¹ m³ = 11 nL solid, plug ≈ 25 nL at ε 0.4) with 2.7×10⁵ Ab/bead (Chang2012, docs/01):
[Ab]_plug = 5.4×10¹¹ Ab / (N_A × 10 nL of liquid in the plug) ≈ 90 µM; with 50 % active sites
(docs/01, Tripathi2018 range 23–91 %) k_on·[Ab] ≈ 3×10⁵ × 4.5×10⁻⁵ = 13.5 s⁻¹; τ_res at 10 µL/min =
10 nL/(0.167 µL/s) = 0.06 s → 1 − e⁻⁰·⁸ ≈ 0.55 per pass; at 2 µL/min (τ 0.3 s): 0.98. This is the
monolith/packed-bed regime of Clarke2001 and Jiang2005 (95 % in ≈ 0.1 s). **Caveat:** a magnetically held plug
on a flat electrode is a thin mound, not a packed column; most of the flow can bypass it in the 10 µL cell
(channel cross-section ≫ plug). Bypass is the dominant uncertainty (UNVERIFIED; settle by the breakthrough
measurement above).

### B.4.2 Packed micro-columns and capillary immunoreactors with electrochemical detection

| Key | Reactor | Assay, label, read | LOD | Time, volume | Evidence |
|---|---|---|---|---|---|
| deAlwis1985 | "rapid sub-picomole" EC enzyme immunoassay for IgG (reactor details not in record) | EC EIA | sub-pmol IgG (title) | "rapid" | [V-abs] title only; no abstract in PubMed |
| deAlwis1987 | heterogeneous competitive EC immunoassay, glucose oxidase label (MeSH) | GOx | IgG in the pmol range (title) | "rapid" | [V-abs] title only |
| Zhang1999 (Heineman/Halsall) | antibody covalently on the inner wall of a **22 µL microcapillary** | competitive, ALP / pAPP, product read by amperometric FIA | phenobarbital 30 µg/L (2.8 pmol); 4 µL serum | 1.5 h competition | [V-abs] |
| Xu1990 (Heineman/Halsall) | well/solid-phase sandwich, FIA-EC read of 4-aminophenol | ALP / pAPP | AFP 0.163 µg/L; interassay CV < 8.2 % | — | [V-abs] |
| deFrutos1993 (docs/01) | fused-silica capillary 100 µm i.d., protein G, captures human IgG; stop-flow | F(ab)-ALP / pNPP (optical) | 333 zmol human IgG | stop-flow; pre-formed complex gave 100× | docs/01 [V-abs] |
| HageKao1991 (draft) | HPLC immunoaffinity column, sandwich | acridinium ester, CL | 16 amol PTH; 66 µL plasma | 6 min/injection after 1 h pre-incubation | [V-abs] |
| Bange2005 (review) | survey of microfluidic immunosensors | — | — | — | [V-abs] |

**Verdict B.4.** A packed column or a magnet-held bead plug collects IgG in seconds of residence when the analyte
passes through the bed, but every flow precedent that reached low LODs pre-incubated the analyte with label or
beads in a stirred volume (HageKao1991, deFrutos1993: pre-formed complex = 100×; Biscay2014). In tier 2 the
sample vial holds sample only, so pre-incubation must happen in a holding coil after zone stacking (B.5) or in the
bed itself under slow or stopped flow. The best tier-2 format is: beads (pre-coated) held on the WE by a magnet
under the Micrux cell, sample pumped through at 2–10 µL/min (≈ 10–50 min for 100 µL), conjugate zone, wash,
substrate, stopped-flow accumulation, read. Capture yield per pass and plug bypass are the bench unknowns.

## B.5 Mixing without valves

**What the sequential-injection literature offers.** Zone penetration between stacked zones in a holding coil is
governed mainly by **flow reversal**: "increasing the number of flow reversals ... increases mutual zone penetration,
but the first flow reversal and its length are most effective" (Gubeli1991, Anal Chem, doi:10.1021/ac00021a005,
[S] abstract via aggregator). The BSM pumps in one direction only, so in tiers 1–2 the only mixing mechanisms are
axial (Taylor–Aris) dispersion at the zone boundary and diffusion during stopped flow.

**Boundary mixing of two consecutive 100 µL zones (Derived).** Taylor–Aris D_eff = D + u²a²/(48D). Tube ID
0.25 mm (a = 0.125 mm), Q = 5 µL/min → u = 1.7 mm/s; protein D = 4×10⁻¹¹ m²/s: D_eff ≈ 2.3×10⁻⁵ m²/s. Valid only
for t ≫ a²/D ≈ 6.5 min. A 100 µL zone in this tube is 2.0 m long. After 10 min of travel the boundary spreads by
σ = √(2·D_eff·t) ≈ 0.17 m ≈ 8 µL. **Only ≈ 10 % of each zone mixes with its neighbour**; the bulk of a 100 µL
sample zone never meets a following conjugate zone in a coil. Wider tubing increases D_eff (∝ a²) but also
lengthens transit; a coiled tube reduces dispersion further (secondary flow). Consecutive SM-FL injections are
also separated by carrier pumped during the injector cycle (cycle time UNVERIFIED; docs/27).

**Consequences.**
* Sample and conjugate cannot be premixed in a tier-1 or tier-2 coil. Use the **sequential (two-step) sandwich**:
  sample zone over the capture surface, then conjugate zone, then wash, then substrate. This forgoes the 100×
  gain of a pre-formed complex (deFrutos1993) but that gain applied to a capillary with poor mass transfer.
* Stopped-flow incubation works on the part of a zone that sits in the cell or bed: the 10 µL cell holds 10 % of
  the sample. To present all 100 µL, flow must continue (B.6), or the sample must be parked in steps (move 10 µL,
  stop t_s, move the next 10 µL). With 10 steps and 50 min available, t_s ≈ 4–5 min per step; in a cell of height
  H = 100 µm, τ_diff ≈ 104 s (B.0), so each parked slice is ≈ 90 % depleted (Derived, if the wall is the sink and
  the capture rate is not reaction-limited, B.0 k_r). Stepped stop-flow is therefore the tier-1 capture programme,
  provided the BSM accepts stop and step commands at µL resolution (docs/26 §3 open fact).
* In a bead bed (tier 2) a stopped plug equilibrates in milliseconds (B.4.1), so stopping adds nothing for capture;
  it matters only for **substrate accumulation** (product held in the bed and cell for minutes before the read).

## B.6 Kinetics, transport limits and the best flow rate for a fixed volume and time

Squires2008 ([V-full]) for a sensor of length L and width W_s on one wall of a channel of height H, width W_c,
flow Q: Pe_H = Q/(D·W_c); Pe_s = 6λ²Pe_H with λ = L/H; total flux J_D = D·c₀·W_s·F with
F ≈ 0.81·Pe_s^(1/3) + 0.71·Pe_s^(−1/6) − 0.2·Pe_s^(−1/3) for Pe_s ≫ 1; F ≈ Pe_H (every molecule collected) for
Pe_H ≪ 1; Damköhler number Da = k_on·b_m·L/(D·F). "Flow rates must be increased 1,000-fold to enhance flux by a
factor of ten." Collected fraction in the thin-depletion-layer regime = F·D·W_s/Q ∝ Q^(−2/3).

## B.7 Bead handling by an autosampler

**Settling in a vial (Derived, Stokes, v = 2Δρ·g·r²/(9μ), μ = 1.0 mPa·s, 20 °C).** Densities are vendor "dry
substance" values ([S], thermofisher.com Dynabeads FAQ, quoted by search summary: M-280 1.4 g/cm³, MyOne
1.8 g/cm³); the hydrated density in buffer is lower, so these velocities are upper bounds.

| Bead | Δρ (kg/m³) | v (mm/h) | Time to clear 2 mm (top of a draw zone) | Time to clear 10 mm (vial height) |
|---|---|---|---|---|
| MyOne, Ø 1.0 µm | 800 | 1.6 | 1.3 h | 6.4 h |
| M-280, Ø 2.8 µm | 400 | 6.2 | 0.33 h | 1.6 h |
| M-270, Ø 2.8 µm (if 1.6 g/cm³, UNVERIFIED) | 600 | 9.2 | 0.22 h | 1.1 h |

Consequences (Derived). A needle that draws ≈ 200 µL from a fixed depth sees the concentration near its tip
change once the settling front passes: for M-280, within ≈ 20 min of the last mixing a 2 mm top layer is
depleted and the dose drifts; for MyOne the same happens after ≈ 1.3 h. The SM-FL has no vial shaker (UNVERIFIED
for this I-Class PLUS configuration; vendor question: "does the SM-FL support a mix or aspirate–dispense
pre-injection step for a vial?"). Practical rule: use 1 µm beads for any autosampler-dosed bead charge, place
the bead vial so its draw happens < 30 min after the vial was mixed by hand, and run the draw from near the vial
bottom only if the settled fraction is resuspended. Bead dose CV becomes a term in the blank SD (docs/01,
Pollema1992/1994); bench measurement: count beads (or measure ALP-labelled bead signal) in 10 successive
injections from one vial at t = 0, 30, 60, 120 min.

**Reports of beads injected through a valve or loop.**
* Biscay2014 injected **100 µL of bead suspension** through the FIA injection valve onto the magnet-equipped SPCE
  flow cell ([V-abs]); bead loss in the loop and valve is not reported in the abstract.
* Dominguez2012 "injected" OA-coated beads onto the SPCE in an automated flow system ([V-abs]); loss not reported.
* Ruzicka's bead injection / lab-on-valve line (Carroll2002, Carroll2003, Ruzicka2006) meters 30–100 µm
  Sepharose beads with a syringe pump through a selection valve; this proves bead metering through valves, but
  for much larger, non-magnetic beads and with a syringe pump, not a needle autosampler ([V-abs]).
* Imato group (Soh2004, Zhang2007, Hirakawa2006) moved magnetic beads through a syringe pump and selection valve;
  trapping and release by magnet and flow ([V-abs]).
* **Not found:** any report of superparamagnetic beads drawn by a fixed-loop needle autosampler (Waters SM-FL or
  similar), and any quantified bead loss in PEEK or stainless-steel tubing and rotor seals. Settle by the bench
  count above, plus a loss test: inject a known bead charge, collect everything leaving the injector with the
  magnet removed, count.

**Mechanisms of bead loss to expect (UNVERIFIED, engineering).** (1) Settling in horizontal tubing at low flow:
an M-280 bead falls 0.25 mm (half of a 0.5 mm ID) in ≈ 2.4 min, so any segment where the zone rests for minutes
loses beads to the wall; (2) remanence or stray fields near the injector are negligible for superparamagnetic
beads; (3) nonspecific adhesion of protein-coated beads to stainless steel and to the rotor seal; (4) trapping in
dead volumes of fittings. Blocked beads (BSA/Tween or the vendor's buffer) and continuous flow during transfer
minimise (1)–(4).

**Verdict B.7.** Beads can be delivered by an injection, but dose precision depends on vial settling (minutes for
2.8 µm, about an hour for 1 µm) and on unquantified loss in the injector. For tiers 1–2 the safer route is to
**load the bead charge by hand into the cell or bed before the run** (allowed by docs/26 §3) and to inject only
the sample and soluble reagents.

## B.8 Summary table and ranking of capture formats for tier 1 and tier 2 (100 µL, ≤ 60 min)

Capture yield η is the fraction of the 4×10⁵ IgG molecules (1 pg/mL) that end up labelled on the read surface.
Values are Derived from B.0, B.4, B.5, B.6 with the inputs stated; they are planning numbers, not measurements.

| Rank | Format | Tier | Capture programme | η (Derived) | Product path to WE | NSB surface | Main risk | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | Pre-coated streptavidin/biotin-Ab beads (2.8 µm, ≈ 10⁶–10⁷) loaded by hand onto the WE, held by a fixed magnet under the Micrux cell | 2 | sample through at 2–5 µL/min (20–50 min), conjugate zone, wash, HQDP, stop 5–10 min, read | 0.5–0.95 per pass if no bypass; **bypass unknown** | product made on the WE, accumulates in the 10 µL cell during stop | beads + WE + cell walls | flow bypassing a thin bead mound; bead loss at > 50 µL/min (B.4.1) | best tier-2 option; bench-test breakthrough first |
| 2 | Packed micro-column (porous NHS/protein-G-type or bead frit, 0.1–1 µL bed) upstream of the cell, stop-flow for substrate, product swept to the WE | 2 | sample through at 5–10 µL/min; conjugate; wash; HQDP stopped 5–10 min in the bed; push the product plug (≈ 1–2 µL) into the cell | 0.9–1 (residence ≫ 0.1 s; Clarke2001, Jiang2005) | product plug dispersed by ≈ 2–10× on the way to the cell (Derived, UNVERIFIED for the fittings) | large internal area: NSB per run larger | column NSB; dispersion of the product plug | strong on capture; LOD set by column blank |
| 3 | Capture Ab on the WE (oriented, OEG or diazonium antifouling), cell height ≈ 50–100 µm, stepped stop-flow (10 × 10 µL, ≈ 4–5 min each) | 1 | B.5 stepped programme; then conjugate, wash, HQDP stop, read | 0.1–0.5 (WE covers only part of the cell floor; depends on area ratio, UNVERIFIED until docs/28) | direct | WE only (smallest NSB area) | BSM stop/step resolution; WE/cell area ratio; slope CV between electrodes | the tier-1 format |
| 4 | Capture Ab on the WE, continuous slow flow (no stops) | 1 | 100 µL at 2 µL/min, 50 min | ≈ 0.05–0.2 (Squires2008, B.6: WE 2 × 2 mm, H 100 µm, Q 2 µL/min → Pe_s ≈ 10⁶, F ≈ 82, transport-limited 0.19, Da ≈ 0.8 → ≈ 0.1; η ∝ Q^(−2/3)) | direct | WE only | low η | fallback only |
| 5 | Beads injected by the SM-FL from a tray vial | 1–2 | injection of beads, then as rank 1 | as rank 1 × dose fraction | — | — | settling and loss (B.7) | avoid unless hand loading is impossible |

**Ranking logic.** At the LOD, signal ∝ η while the blank ∝ NSB area × per-area NSB. Ranks 1 and 2 raise η by
5–20× over rank 3–4 at the cost of more surface. Beads are justified because their large area is pre-blocked and
washed in a packed state; the per-run blank must be measured, not assumed (B.3).

## B.9 Findings that most change the design; open questions

1. **No precedent captures an analyte from 100 µL by flow-through over a magnet-held bead plug and reports η.**
   All magnetic-flow immunoassays found pre-incubated off-line or stopped for ≈ 20 min per step (Biscay2014,
   Dominguez2012, Soh2004 [V-abs]). The tier-2 design depends on a breakthrough measurement.
2. **Sample and conjugate cannot be premixed without valves:** two consecutive 100 µL zones mix only ≈ 10 % at their
   boundary in a coil (Derived, Taylor–Aris; flow reversal, the SIA mixing tool, is not available; Gubeli1991 [S]).
   The assays are sequential two-step sandwiches.
3. **Stepped stop-flow is the tier-1 capture programme:** ten 10 µL slices parked ≈ 4–5 min each in a ≤ 100 µm
   cell deplete each slice (Derived, B.5). Whether the BSM can execute it is the gating hardware fact (docs/27).
4. **Electrode NSB must stay below ≈ 10⁻⁵–10⁻⁴ of a monolayer of conjugate** to meet the docs/01 blank budget
   (Derived, B.3); the best OEG SAMs are quoted at ≈ 2 % of a fibrinogen monolayer at high concentration ([S]).
   No per-area NSB at nM conjugate on blocked SPCE was found: measure it first.
5. **Bead dosing through the SM-FL is not established:** M-280 settles ≈ 6 mm/h, MyOne ≈ 1.6 mm/h (Derived, vendor
   density [S]); no report of beads through a fixed-loop needle autosampler was found. Load beads by hand.
6. **Beads stay under a mm-scale NdFeB magnet up to ≈ 10–100 µL/min in a thin channel** (Derived, inputs
   UNVERIFIED); this covers the 2–10 µL/min capture flows but must be checked in the Micrux geometry.
7. **Product on the WE + stopped flow** is the right product path in a 10 µL cell; upstream reactors dilute the
   product on its way to the detector (Hirakawa2006 vs Biscay2014, [V-abs]).

**Open questions (bench or vendor).** (a) Breakthrough of IgG through a magnet-held bead plug vs flow (2, 5,
10 µL/min). (b) Bead count in the effluent vs flow in the Micrux cell with a magnet under the WE. (c) ALP-conjugate
NSB per mm² on blocked SPCE and on OEG-gold chips at 0.1–1 nM, 10 min. (d) Can the BSM execute 0 µL/min steps and
10 µL moves at 1–10 µL/min (docs/27)? (e) Micrux channel height and WE/cell-floor area ratio (docs/28).
(f) SM-FL injector cycle time between consecutive injections and its carrier volume.

# Part C — Benchmarks and what is credible

Conversions (Derived, M = 1.5×10⁵ g/mol): 1 pg/mL IgG = 6.7 fM; 1 fg/mL = 6.7 aM = 4.0 molecules per µL;
0.25 fg/mL ≈ 1 molecule per µL.

## C.1 Lowest electrochemical-immunoassay LODs reported for IgG

"Flow/auto" marks a flow or automated element. "S/N=3" means the LOD was taken from noise or a slope
extrapolation, not from replicate blanks through the calibration curve.

| Key | IgG | Format; label and amplification | Electrode; read | LOD (definition) | Sample vol.; time | Flow/auto | Evidence |
|---|---|---|---|---|---|---|---|
| Zhang2015 | human | sandwich on electrode; AuNR self-assembly + silver deposition, ASV | not in abstract; stripping | 0.08 fg/mL (definition not in abstract) | — | no | [V-abs] |
| Chao2025 | human | sandwich on MWCNT/GC; GOx-catalysed Au staining, ASV in 8 µL HBr–Br₂ | GC; ASV ≈ 6 min | 0.25 fg/mL (S/N=3; "≈ 1 IgG per µL") | µL | no | [V-abs] |
| TangMa2016 | human | sandwich; ratiometric metal-nanocomposite probes | — ; voltammetry | 0.26 fg/mL (definition not in abstract) | — | no | [V-abs] |
| Qin2016 | human | sandwich on GC; Au label, Cu staining + galvanic replacement, ASV | GC; ASV | 0.3 fg/mL (S/N=3; "7 IgG molecules in 6 µL") | 6 µL | no | [V-abs] |
| Wang2001 (docs/01) | mouse | microchip electrophoresis of free/bound ALP-Ab, then pAPP | chip; amperometric | 2.5×10⁻¹⁶ g/mL (claimed) | — | microchip | docs/01 [V-abs] |
| Selvaraju2008 (docs/01) | mouse | magnetic beads; AuNP catalyst label, p-nitrophenol + NaBH₄ | Fc-D ITO; CV | 1 fg/mL | — | no | docs/01 [V-abs] |
| Han2014 (docs/01) | mouse | chip microchannel with 3D IDA (ITO) | chronocoulometry | ≈ 10 fg/mL | µL | chip | docs/01 [V-abs] |
| Das2007 (docs/01) | mouse | ALP / pAPP + hydrazine chemical redox cycling | ITO | 100 fg/mL (10 pg/mL without cycling) | — ; 10 min substrate | no | docs/01 [V-abs] |
| Xu1989 (docs/01) | mouse | well sandwich; ALP / pAPP; product read by FIA-EC | GC thin-layer, amperometric | 0.81 pg/mL (30 min substrate) | — ; > 1 h | **FIA readout** | docs/01 [V-abs] |
| Kwon2008 (docs/01) | mouse | ALP / pAPP + NADH cycling | Au | 1 pg/mL | — | no | docs/01 [V-abs] |
| deFrutos1993 (docs/01) | human | protein-G capillary, F(ab)-ALP; optical, not EC | absorbance | 333 zmol | — ; stop-flow | **flow capillary** | docs/01 [V-abs] |
| Wilson2005 / WilsonNie2006 | human | sandwich on IrOx thin film; ALP / HQDP | IrOx; amperometric | 3 ng/mL; interassay CV 1.9–8.2 % | — | no | [V-abs] (B.1) |

**Reading.** Every sub-pg/mL claim for human IgG is a manually prepared GC or ITO electrode with nanoparticle
amplification and an S/N- or slope-based LOD. Claims of ≈ 1 molecule per µL (Chao2025, Qin2016) are below the
level any blank set by NSB of a conjugate can support (Rissin2010 floor ≈ 1 fM = 0.15 pg/mL with the best
optimised digital bead assay; docs/01). They show the read chemistry can resolve tiny label amounts, not that the
assay blank allows it. The only flow or automated precedents in the table are at ≈ 1 pg/mL (Xu1989, FIA readout of
a well assay, > 1 h) or optical.

## C.2 Human IgG as the analyte

* **Environmental contamination.** Human IgG was found in ≥ 1/3 of micropipettor tip-cone eluates in all of 19 labs;
  only 14 % of 222 eluates were clean (Parry1997, docs/01). At 1 pg/mL the whole sample holds 100 fg. Skin flakes,
  saliva and dust are plausible carriers; **no quantitative value per mg dust or per skin flake was found** in this
  session (bench: run 20 buffer blanks handled with and without gloves, closed vials, dedicated tips).
* **Reagent contamination.** "Most commercial preparations of BSA, including some of the highest purity grades,
  contain contaminating bovine IgG" (Jackson ImmunoResearch technical pages, [S] vendor text via search summary,
  jacksonimmuno.com/technical/products/groups/bsa). This matters when an anti-human reagent cross-reacts with
  bovine IgG; use IgG-free BSA, or non-mammalian blockers, and cross-adsorbed reagents (docs/01).
* **Cross-reactivity.** Anti-human IgG polyclonals (goat, rabbit, donkey) bind conserved epitopes of other species'
  IgG unless cross-adsorbed against bovine, mouse and goat IgG (vendor practice; numeric cross-reactivity not
  found). The capture and detection antibodies are themselves IgG: detection Ab binding the capture Ab was the
  dominant blank in Qu1998 (docs/01, 39 → 2.5 pg/mL after suppression).
* **Epitope choice.** Capture on Fc and detection on Fab, κ+λ light chain, or with an F(ab′)₂ or chicken IgY
  conjugate avoids (i) symmetric-sandwich hindrance (Butler1986, docs/01) and (ii) protein A/G binding the
  detection reagent (deFrutos1993 used F(ab)-ALP). A κ-only detector misses λ IgG; NISTmAb (κ) would not reveal it
  (docs/01).
* **Affinity of commercial anti-human-IgG reagents.** One commercial mouse anti-human-Fc mAb: K_D 5.5–36 nM,
  t½ 1.4–3.3 min (Kamat2020, docs/01 [V-abs]) — unusable for a wash step of minutes. Goat anti-human-Fc
  polyclonals are sub-nM (docs/01). Rebinding on dense bead surfaces lowers the effective K_D below 10⁻¹¹ M
  (Chang2012). Screen capture reagents for k_off (t½ > 1 h).

## C.3 Unit-to-unit variability of disposable-electrode immunoassays

| Source | System | Between-unit CV | Evidence |
|---|---|---|---|
| WilsonNie2006 | IrOx thin-film immunosensors, ALP/HQ | interassay 1.9–8.2 % | [V-abs] |
| Xu1990 | FIA-EC sandwich EIA (AFP) | interassay < 8.2 % | [V-abs] |
| MolineroFernandez2020 | M-280 bead assay on chip | intra 5 % (one bead batch), inter 9 % (bead batches) | [V-full] |
| Babamiri2025 | screen-printed carbon MIP sensors | 9.7–11.7 % without QC → 1.4–2.1 % with fabrication QC on an embedded Prussian-blue signal (5 sensors per group; 36–44 % of electrodes passed) | [V-full] |
| docs/01 (Jiang1995) | capillary EIA | 6–10 % | docs/01 |

**Methods that reduce it.** (1) **Pre-read on the same electrode**: background chronoamperogram and a short
HQ or ferro/ferricyanide calibration pulse before the sample, used to normalise slope; allowed before injection
(docs/26 §3). Caveat: the printed Ag/AgCl pseudo-reference of SPEs drifts in ferri/ferrocyanide (Khor2025, [S]);
use HQ itself as the probe. (2) **QC gating of electrodes** by an embedded or pre-read signal (Babamiri2025: CV
≈ 10 % → ≈ 2 %, at the cost of discarding ≈ 60 % of units). (3) **Dual electrodes** (second WE without capture Ab as
an NSB reference) need a second channel or a bipotentiostat: tier 3 only. (4) Ratiometric internal probes
(TangMa2016) — nanomaterial-specific, not transferable to ALP/HQ without redesign.

## C.4 Realistic LOD per tier (sober estimate)

Model: LOD ≈ 3·CV_blank·B, B = blank as analyte-equivalent (docs/01 §d). Anchors: best documented blank
≈ 1 fM (0.15 pg/mL; digital bead assay with nM detection Ab, pM label, Rissin2010); conventional plate ELISA
≈ 85 fM (13 pg/mL). B scales inversely with capture yield η (same NSB, less specific signal).

| Tier | η (B.8) | Expected B | CV_blank (unit-to-unit, C.3) | 3·CV·B (Derived) | Adopted estimate | Reasoning |
|---|---|---|---|---|---|---|
| 1 | 0.1–0.5 | 20–200 fM (3–30 pg/mL): electrode NSB unmeasured, low η inflates B | 10–20 % | 0.9–18 pg/mL | **≈ 2–20 pg/mL** | no premixing (B.5); electrode carries all NSB; η limited by cell geometry; pre-read normalisation needed for the low end |
| 2 | 0.5–0.95 (if no bypass) | 5–30 fM (0.8–5 pg/mL): pre-blocked, washed beads | 5–10 % (bead-batch CV 9 %, MolineroFernandez2020) | 0.1–1.4 pg/mL | **≈ 0.5–5 pg/mL** | higher η; bead NSB is the better-documented surface; adopted range widened for bypass, bead-dose CV and electrode noise |
| 3 | 0.7–0.95 with mixing, transfer and valve-controlled washes | 1–10 fM | ≈ 5 % | 0.02–0.2 pg/mL | **≈ 0.5–3 pg/mL** | premixed capture, immune-complex transfer (Ishikawa1978, docs/01), dual WE possible; the project's Monte-Carlo model, with its own NSB and reagent distributions, gives medians 1.3–3.5 pg/mL for the gen-1 valve system (CLAUDE.md status), so the simple formula is too optimistic |

The simple formula understates the LOD because B itself is uncertain by ≥ 10× before bench data, and other
noise terms (Poisson at < 10⁴ labels, electrode background, bead dose) add to the blank SD. The 1 pg/mL goal is credible only in tier 3, and possibly in tier 2 if bead-plug bypass is small and the blank
approaches 5 fM. Sub-fg/mL literature values (C.1) are not evidence for any tier.

## B.R References (Parts B and C)

Keys marked "docs/01" are resolved in docs/01_literature_parameters.md and not repeated (Chang2012, Rissin2010,
Thomas2004, deFrutos1993, Xu1989, Das2007, Kwon2008, Selvaraju2008, Han2014, Wang2001, Jenkins1988, Kenna1985,
Qu1998, Parry1997, Kamat2020, Butler1986, Tripathi2018, Pollema1992, Pollema1994, Ishikawa1978, Jiang1995).
Keys of B.1–B.3 cited in the interim draft without a DOI here (Rossier2001, Hoegger2007, Nishimura2011, Dong2007,
Wilson2005, WilsonNie2006, Duan1994, Meyerhoff1995, Arevalo2011, DiazGonzalez2005a, Corgier2005, Corgier2007,
Polsky2008, Darder1999, Gui2013, SabateDelRio2019, Timilsina2022, Clarke2001, Jiang2005, Sole1998) were read as
PubMed abstracts in the first pass; their DOIs were not re-collected in this pass (open item).

| Key | Reference |
|---|---|
| Squires2008 | Squires TM, Messinger RJ, Manalis SR. Nat Biotechnol 2008;26:417–26. doi:10.1038/nbt1388 |
| Pemberton2001 | Pemberton RM, Hart JP, Mottram TT. Biosens Bioelectron 2001;16:715–23. doi:10.1016/s0956-5663(01)00212-3 |
| Pemberton1999 | Pemberton RM, Hart JP, Stoddard P, Foulkes JA. Biosens Bioelectron 1999;14:495–503. doi:10.1016/s0956-5663(99)00019-6 |
| HageKao1991 | Hage DS, Kao PC. Anal Chem 1991;63:586–95. doi:10.1021/ac00006a008 |
| Zhao2012 | Zhao X, et al. J R Soc Interface 2012;9:2457–67. doi:10.1098/rsif.2012.0148 (PMC3427501) |
| Biscay2014 | Biscay J, González García MB, Costa García A. Talanta 2014;131:706–11. doi:10.1016/j.talanta.2014.08.013 (PMID 25281162) |
| Dominguez2012 | Dominguez RB, Hayat A, Sassolas A, Alonso GA, Munoz R, Marty JL. Talanta 2012;99:232–7. doi:10.1016/j.talanta.2012.05.045 (PMID 22967546) |
| Hirakawa2006 | Hirakawa K, Katayama M, Soh N, Nakano K, Imato T. Anal Sci 2006;22:81–6. doi:10.2116/analsci.22.81 (PMID 16429778) |
| Soh2004 | Soh N, Nishiyama H, Asano Y, Imato T, Masadome T, Kurokawa Y. Talanta 2004;64:1160–8. doi:10.1016/j.talanta.2004.06.001 (PMID 18969724) |
| Zhang2007 | Zhang R, Nakajima H, Soh N, et al. Anal Chim Acta 2007;600:105–13. doi:10.1016/j.aca.2007.02.052 (PMID 17903471) |
| Choi2001 | Choi JW, Oh KW, Thomas JH, Heineman WR, Halsall HB, et al. Lab Chip 2002;2:27–30. doi:10.1039/b107540n (PMID 15100857) |
| MolineroFernandez2020 | Molinero-Fernández Á, Moreno-Guzmán M, López MÁ, Escarpa A. Biosensors 2020;10:66. doi:10.3390/bios10060066 (PMC7344519) |
| TekinGijs2013 | Tekin HC, Gijs MAM. Lab Chip 2013;13:4711–39. doi:10.1039/c3lc50477h (PMID 24145920) — review, background only |
| Bange2005 | Bange A, Halsall HB, Heineman WR. Biosens Bioelectron 2005;20:2488–503. doi:10.1016/j.bios.2004.10.016 (PMID 15854821) |
| Zhang1999 | Zhang J, Heineman WR, Halsall HB. J Pharm Biomed Anal 1999;19:145–52. doi:10.1016/s0731-7085(98)00053-3 (PMID 10698576) |
| Xu1990 | Xu Y, Halsall B, Heineman WR. Clin Chem 1990;36:1941–4. PMID 1700742 |
| Bauer1996 | Bauer CG, et al. Anal Chem 1996;68:2453–8. doi:10.1021/ac960218x (PMID 8694255) |
| deAlwis1985 | de Alwis WU, Wilson GS. Anal Chem 1985;57:2754–6. doi:10.1021/ac00291a004 (PMID 4083488; no abstract) |
| deAlwis1987 | de Alwis U, Wilson GS. Anal Chem 1987;59:2786–9. doi:10.1021/ac00150a013 (PMID 3434806; no abstract) |
| Carroll2002 | Carroll AD, Scampavia L, Ruzicka J. Analyst 2002;127:1228–32. doi:10.1039/b205898g (PMID 12375849) |
| Carroll2003 | Carroll AD, Scampavia L, Luo D, Lernmark A, Ruzicka J. Analyst 2003;128:1157–62. doi:10.1039/b302786d (PMID 14529023) |
| Ruzicka2006 | Ruzicka J, Carroll AD, Lähdesmäki I. Analyst 2006;131:799–808. doi:10.1039/b603768b (PMID 16802025) |
| Gubeli1991 | Gübeli T, Christian GD, Ruzicka J. Anal Chem 1991 (volume and pages not checked). doi:10.1021/ac00021a005 ([S]) |
| PrimeWhitesides1993 | Prime KL, Whitesides GM. J Am Chem Soc 1993;115:10714–21. doi:10.1021/ja00076a032 ([S]; number as quoted by secondary sources) |
| Mrksich1995 | Mrksich M, Sigal GB, Whitesides GM. Langmuir 1995 (SPR of OEG SAMs; group PDF, mrksichgroup.northwestern.edu) ([S]) |
| Fonnum2005 | Fonnum G, et al. J Magn Magn Mater 2005;293:41–7. doi:10.1016/j.jmmm.2005.01.041 ([S]) |
| ThermoDynabeads | Thermo Fisher Dynabeads product pages and FAQ (M-280 1.4 g/cm³ dry, MyOne 1.8 g/cm³ dry, M-280 Fe 12 wt %): thermofisher.com/order/catalog/product/65002 ([S]) |
| JacksonBSA | Jackson ImmunoResearch, BSA technical page: jacksonimmuno.com/technical/products/groups/bsa ([S]) |
| Zhang2015 | Zhang H, Ning D, Ma L, Zheng J. Anal Chim Acta 2015;902:82–8. doi:10.1016/j.aca.2015.10.028 (PMID 26703256) |
| Chao2025 | Chao L, Wu Z, Qi S, Xu A, Huang Z, Yan D. Biosensors 2025;15:689. doi:10.3390/bios15100689 (PMID 41149340) |
| TangMa2016 | Tang Z, Ma Z. Sci Rep 2016;6:35440. doi:10.1038/srep35440 (PMID 27739493) |
| Qin2016 | Qin X, Xu A, Wang L, et al. Biosens Bioelectron 2016;79:914–21. doi:10.1016/j.bios.2016.01.024 (PMID 26802573) |
| Babamiri2025 | Babamiri B, Farrokhnia M, Mohammadi M, Sanati Nezhad A. Sci Rep 2025;15:8859. doi:10.1038/s41598-025-93025-1 (PMC11909151) |
| Khor2025 | Khor et al. Front Chem 2025. doi:10.3389/fchem.2025.1602365 ([S]; authors not checked) |
