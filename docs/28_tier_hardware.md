# 28 — Hardware of the round: Micrux cells and electrodes, passive in-line parts, additions for tier 3

Status: 2026-11-17. Written for the tier round (docs/26). Vendor brochures (PDF) and product pages were downloaded and
read in this session; each fact names the document. The company is MicruX Technologies, Gijón (Asturias), Spain
(address on every brochure [V]); earlier project notes said Oviedo.

**Evidence labels.**

| Label | Meaning |
|---|---|
| **[V]** | Checked in this session against the cited document (vendor page or PDF read in full; papers: abstract or full text stated). |
| **[S]** | Search-engine summary only; the page was not opened. |
| **UNVERIFIED** | Engineering estimate, not checked against any source. |
| **Derived** | Calculated here from cited inputs; formula given. |

Reference keys [R1]… are listed in §9. Questions to the vendor and dimensions for the user are in §8.

---

## 1. The two flow cells

### 1.1 What the vendor states

| Item | (a) AIO-SPE cell + flow-cell add-on (thick-film strips) | (b) AIO cell + flow-cell add-on (thin-film chips) | Source |
|---|---|---|---|
| Base part no. | ED-AIO-SPE-CELL (-1x / -2x with one or two add-ons) | ED-AIO-CELL (-1x / -2x) | [R1] [R2] [V] |
| Flow add-on part no. | ED-AIO-SPE-ADD-ON-FC-PMMA (PalmSens lists it as "Flow Cell PMMA-3.5", ref. MX-ED-AIO-ADD-ON-FC-PMMA) | ED-AIO-ADD-ON-FC-PMMA-2.0 (SE, mSE, IDA, IDRA); -FC-PMMA-3.5 (IDE only); PEEK versions -FC-PEEK-2.0/-3.5 on request | [R1] [R3] [R4] [R5] [V] |
| Thin-layer add-on | none listed | "Thin Layer PMMA-1.0" and "Thin Layer PEEK-1.0" are options on the PalmSens page; **not** on the MicruX site or in the 2025 add-on brochure; no geometry published | [R5] [V]; [R3] [R4] [V] |
| Flow geometry | **wall-jet**: "inlet flow is perpendicular to the working electrode surface" | **wall-jet**, same wording | [R1] [R2] [V] |
| Inlet channel | 0.8 mm I.D. | 0.5 mm I.D. | [R1] [R2] [V] |
| Stated internal volume | **< 5 µL**, "limited by an O-ring (8 mm I.D.)" | **< 500 nL**, "limited by an O-ring (2 or 3.5 mm I.D.)" | [R1] [R2] [V] |
| Seal | O-ring 8 mm I.D. pressed on the strip; add-on held by magnets | O-ring 2.0 mm I.D. (or 3.5 mm for IDE) on the SU-8 opening; magnets | [R1] [R3] [V] |
| O-ring cross-section and material | not stated | not stated | — |
| Ports | ¼″-28 UNF flat-bottom (standard fluidic ports) | ¼″-28 UNF | [R1] [R3] [V] |
| Tubing (vendor packs) | 1/16″ OD PTFE, 0.8 mm ID standard (0.3, 0.5, 1.0 mm on request); PP nuts; SS/PTFE ferrules "rated up to 1000 psi (69 bar)" | same | [R6] [V] |
| Wetted materials | PMMA add-on, O-ring (material not stated), electrode strip (PET or Al₂O₃ substrate, printed inks, dielectric) | PMMA or PEEK add-on, O-ring, glass, SU-8/PI resin, Ti/Au or Ti/Pt | [R1] [R2] [R3] [R7] [V] |
| Base | aluminium, 60 × 40 × 15 mm (30 mm with add-on) | aluminium base + methacrylate cover, 60 × 40 × 30 mm | [R1] [R2] [V] |
| Pressure limit of the cell | **not stated** anywhere | **not stated** | — |
| Electrical | ED-SPE-CABLE (4 pads → 2 mm banana, 50 cm) | integrated mini-USB-type connector with pogo pins → universal cable to 2 mm banana | [R1] [R2] [R8] [V] |

### 1.2 Which one is "10 µL"?

Neither. The vendor states < 5 µL (SPE flow cell) and < 500 nL (thin-film flow cell) [R1] [R2] [V]. "10 µL" appears in
MicruX documents only as a *drop* volume: 1–10 µL on the drop cell / AIO base [R2] [V], 2–10 µL for IDE chips [R9] [V].
Possible readings, in order of likelihood (UNVERIFIED): (i) the user's figure is the drop-cell volume; (ii) it is the
SPE flow cell plus its inlet and outlet bores (an 0.8 mm bore of 10 mm length holds 5.0 µL, Derived: π·0.4²·10 mm³);
(iii) a custom or older add-on. **The user should measure it (§8).** For the calculation kit, the SPE flow cell is
taken as < 5 µL chamber + bores, and the thin-film flow cell as < 0.5 µL chamber + bores.

### 1.3 Geometry implied by the stated numbers (Derived, then bounded)

Wall-jet: the jet leaves the inlet bore at the centre of the O-ring and strikes the electrode across a gap *h*; the
chamber is the O-ring disc of diameter *D* and height *h*; the outlet sits elsewhere in the add-on (position not
published). If the O-ring disc is the whole chamber, *h* = V/(π D²/4).

| Quantity | (a) SPE flow cell | (b) thin-film flow cell (2.0) | (b′) thin-film IDE flow cell (3.5) |
|---|---|---|---|
| O-ring I.D. *D* | 8 mm [V] | 2.0 mm [V] | 3.5 mm [V] |
| Disc area | 50.3 mm² (Derived) | 3.14 mm² (Derived) | 9.62 mm² (Derived) |
| Stated V | < 5 µL [V] | < 0.5 µL [V] | < 0.5 µL [V] |
| Implied *h* | ≤ 0.099 mm (Derived) | ≤ 0.159 mm (Derived) | ≤ 0.052 mm (Derived) |
| Nozzle bore | 0.8 mm [V] | 0.5 mm [V] | 0.5 mm [V] |
| WE in chamber | 3 mm Ø carbon disc, 7.07 mm², centred under jet (UNVERIFIED centring) | SE: 1 mm Ø WE, 0.785 mm² (Derived from [R10]); IDA/IDRA: arrays inside 2 mm Ø opening | IDE fingers in 3.5 mm Ø opening |

The SPE result (*h* ≤ 0.1 mm under an 8 mm O-ring) is thinner than an O-ring gap normally allows, so the stated
"< 5 µL" probably excludes part of the chamber or the O-ring sits in a recess (UNVERIFIED). Bound for use:
*h* = 0.1–0.5 mm, chamber 5–25 µL for (a); *h* = 0.1–0.3 mm, 0.3–1 µL for (b) (UNVERIFIED). A height of 0.2 mm under
8 mm would give 10 µL (Derived), which would match the user's figure — measure it.

### 1.4 Consequences for the design (UNVERIFIED engineering reading)

* Both cells are wall-jets, not cross-flow thin layers. In stopped flow the chamber is a closed thin disc: the
  diffusion layer reaches the lid after t ≈ h²/(2D) = 0.1 mm → ≈ 7 s, 0.5 mm → ≈ 170 s for D = 7.5e-10 m²/s (Derived;
  D of hydroquinone order of magnitude, UNVERIFIED here). Thin chambers favour stopped-flow accumulation of
  hydroquinone over a capture surface on the WE.
* The PMMA add-on with a magnet-loaded O-ring is not rated for pressure. Put the restrictor that gives the BSM its
  back-pressure **upstream** of the injector or between injector and cell, and run the cell at the outlet near
  atmospheric pressure. The cell's real limit must be measured (§8).
* The SPE cell exposes 50 mm² of strip (WE + CE + RE + dielectric) to the liquid: all of it adsorbs protein and
  carries non-specific conjugate. The thin-film 2 mm cell exposes 3.1 mm².

---

## 2. Electrode catalogue

### 2.1 Thick-film (screen-printed) strips — fit the AIO-SPE cell

Common data [R11] [R12] [V]: strip 27.5 × 10.1 mm; substrate white PET 250 µm or Al₂O₃ ceramic 380 µm (PalmSens
states 0.4 mm overall and 350–380 µm layers [R13] [V]); WE disc 3 mm Ø, **7.1 mm²**; four contact pads (Micrux SPE
port); 50 per pack; sample drop 20–50 µL. The dielectric (insulation) ink and the opening it defines are **not
published**. MicruX part numbers start "ED-"; PalmSens adds "MX-" and spells graphene "GC" [R13] [V].

| Part (MicruX) | Substrate | WE | CE (AE) | RE | Note |
|---|---|---|---|---|---|
| ED-S1PE-C10 / -C10C | PET / ceramic | carbon, "high performance" | carbon | Ag | [R11] [V] |
| ED-S1PE-C20 / -C20C | PET / ceramic | carbon, "low cost" | carbon | Ag | [R11] [V] |
| ED-S1PE-C21 / -C21C | PET / ceramic | carbon, low cost | carbon | **Ag/AgCl** | [R11] [V] |
| ED-S1PE-CG20 / -CG20C | PET / ceramic | graphene | graphene | Ag | [R11] [V] |
| ED-S1PE-CG21 / -CG21C | PET / ceramic | graphene | graphene | **Ag/AgCl** | on MicruX page, not on PalmSens list [R11] [V] |
| ED-S1PE-Au10 / -Au10C | PET / ceramic | gold | gold | Ag | [R11] [V] |
| ED-S1PE-Pt20 | PET | platinum | platinum | Ag | MicruX page only [R11] [V] |
| ED-S1PE-C20/FeCN, /PB, /CoPc; ED-S1PE-C30/MB | PET | carbon + ferricyanide, Prussian blue, Co-phthalocyanine, Meldola blue | carbon | Ag | mediated, for enzyme sensors [R14] [V] |
| ED-D2PE-C10, ED-D2PE-Au10 | PET 250 µm | two WEs, each 1.0 × 2.5 mm (stated 2.3 mm²) | carbon / gold | Ag (shared) | dual; fits AIO-SPE flow add-on [R15] [R4] [V] |

Ag/AgCl reference is offered with carbon and graphene only [R11] [V]. Silver also appears as a printed material
("Silver / Silver-Silver Chloride") [R11] [V]. No ITO or bismuth electrode is offered by MicruX; none was found.

### 2.2 Thin-film chips (10 × 6 × 0.7 mm glass) — fit the AIO cell

Common data [R10] [R16] [R7] [V]: glass substrate; 50 nm Ti adhesion layer + 150 nm Au or Pt (custom: 150 ± 15 nm
[R17] [V]); SU-8/PI resin passivation opens a 2 mm Ø cell (3.5 mm Ø for IDE), or no passivation on request; RE and AE
are thin films of the same metal (Pt for the Au-WE bimetal chip); 50 per pack; drop volume 1–5 µL.

| Part | WE | Geometry (vendor) | Area or count | Source |
|---|---|---|---|---|
| ED-SE1-Au / -Pt | Au / Pt disc | 1 mm Ø in 2 mm Ø opening; RE, AE same metal | 0.785 mm² (Derived, π·0.5²) | [R10] [V] |
| ED-SE1-AuPt | Au WE, Pt RE and AE | 1 mm Ø | 0.785 mm² (Derived) | [R18] [V] |
| ED-mSE1 | microelectrode array | **no data found** (listed in add-on compatibility only) | — | [R3] [V] |
| ED-IDA1-Au/-Pt | 2 interdigitated WEs | width 10 µm, gap 10 µm, 15 pairs | finger length not published | [R16] [V] |
| ED-IDA5-Au/-Pt | " | 10 µm / 5 µm, 20 pairs (BASi lists 50 for -Pt, likely an error) | " | [R16] [R19] [V] |
| ED-IDA6-Au/-Pt | " | 5 µm / 5 µm, 30 pairs | " | [R16] [V] |
| ED-IDRA1-Au/-Pt | 2 radial interdigitated WEs, "designed for flow" | 10 µm / 10 µm, 12 pairs | " | [R20] [V] |
| ED-IDE1/2/3-Au/-Pt | 2 interdigitated strips, no RE/AE | 10/10 µm 90 pairs; 10/5 µm 120 pairs; 5/5 µm 180 pairs; 3.5 mm Ø opening | " | [R9] [V] |
| On demand: ED-BS1 (dual), ED-TS1 (triple), cIDE, IDRE, dIDE, dIDRE | Au / Pt | BS1: 2 WEs of 0.8 mm²; TS1: 3 WEs of 0.3 mm² in 1.5 mm Ø cells; delivery 7–8 weeks | as stated | [R17] [V] |

Vendor redox-cycling data (ferrocyanide or ferrocene methanol, dual mode): IDA1 Rc 2.0, collection < 70 %;
IDA5 Rc 2.5, > 80–85 %; IDA6 Rc 3.0, > 80–85 %; IDRA1 Rc 2.5 ± 0.5, 70 ± 5 % [R16] [R20] [V]. The amplification by
redox cycling of these arrays is therefore only 2–3×.

IDA area estimate (UNVERIFIED, finger length L assumed 1 mm within the 2 mm opening): per WE, n·w·L = 0.15 mm²
(IDA1), 0.20 mm² (IDA5), 0.15 mm² (IDA6); array width 2n(w+g) = 0.6 mm for all three (Derived). Settle L from a
microscope image of one chip (§8).

**Custom service.** Printed: PET (white 125/250/350 µm, transparent 125/175 µm) or alumina 380 µm; carbon (graphite,
graphene), Ag, Ag/AgCl, Au, Pt; minimum feature 500 µm [R21] [V]. Thin film: glass, Au or Pt, features down to 5 µm,
SU-8/PI passivation [R17] [V]. Custom add-ons "can be customized (design & materials)" [R2] [V].

---

## 3. Electrical connection to the Reference 600+

| Item | Fact | Source |
|---|---|---|
| SPE cell cable | ED-SPE-CABLE: four pads → 2 mm banana leads, 50 cm; female ends (with male adapter) or male ends (with crocodile clips) | [R1] [R8] [V] |
| Thin-film cell | mini-USB-type connector with pogo pins on the AIO base → "universal cable" → 2 mm bananas; replacement PCB-DC/AIO and miniUSB-AIO-CABLE | [R2] [R22] [V] |
| Pad order | S1PE: WE, AE, RE pads; D2PE / IDA / IDRA: WE1, WE2, RE, AE pads. Lead labels or colours of the MicruX cables: **not published** | [R11] [R16] [V] |
| Gamry leads | green = working, blue = working sense, white = reference, red = counter, orange = counter sense, black = floating ground (to the Faraday cage) | [R23] [S] |
| Gamry 600+ | isolated from earth; 2–6 cell connections; 11 current ranges 60 pA–600 mA (13 with gain) | [R24] [V] |

Wiring (UNVERIFIED until a continuity check): green + blue → WE lead; white → RE lead; red + orange → AE lead; black
→ the aluminium base or a Faraday cage. For IDA, IDRA, D2PE and BS1 on one channel, use WE1 alone (WE2 open) or tie
WE1 and WE2 together as one WE; generator–collector redox cycling needs a second channel (§7). Identify each MicruX
banana with a multimeter against the pads of a strip or chip before the first run.

---

## 4. Practical electrochemistry of these electrodes

**Silver pseudo-reference.** A bare printed Ag reference in a chloride buffer becomes an Ag/AgCl electrode whose
potential follows the local chloride activity: −59 mV per decade at 25 °C (Derived, Nernst). Example: Ag/AgCl in
0.1 M KCl is ≈ +0.288 V vs SHE against ≈ +0.197 V for saturated KCl, so it reads ≈ +90 mV vs a saturated Ag/AgCl
reference (Derived from textbook E°, UNVERIFIED in this session). A read at "+0.35 V vs Ag/AgCl (sat.)" is therefore
≈ +0.26 V vs a printed Ag/AgCl in 0.1 M Cl⁻. In a chloride-free buffer (e.g. diethanolamine or carbonate without
NaCl) the Ag potential is undefined and drifts; a search summary reports ± 2.2 mV stability for screen-printed
Ag/AgCl of optimised composition and drift from side reactions on bare Ag [R25] [S].
Rules for the designs (UNVERIFIED): (1) prefer C21/CG21 (printed Ag/AgCl); (2) give every solution that reaches the
cell the same chloride (≥ 0.1 M) — wash, conjugate, substrate — so that the step to substrate does not shift the
reference; (3) pH 7.4 → 9.5–10 does not change Ag/AgCl directly but changes the HQ/BQ formal potential by about
−59 mV/pH (2 H⁺, 2 e⁻; Derived), so set the read potential in the substrate buffer, not in the wash buffer.

**Gold thin films and chloride.** MicruX warns that gold thin film "is peeled off ... with chlorides when it is used in
a potential window out of the range −0.3 – 0.6 V" (pH dependent) [R10] [V]. The HQ read (+0.1 to +0.35 V) is inside
this window; electrochemical pre-cleaning of Au chips must be done in a chloride-free acid. Pre-cleaning by CV:
Pt −1.5 to +1.5 V (≥ 10 cycles), Au −1.0 to +1.3 V (≥ 12 cycles), 0.1 V/s [R10] [V].

**Chemical resistance** (no vendor data except where cited):

| Material | Alkaline buffer pH 9.5–10, ≤ 1 h | 0.1 M acid | Source |
|---|---|---|---|
| PMMA add-on | expected resistant; avoid alcohols, ketones (crazing) | expected resistant | UNVERIFIED; vendor offers PEEK "where high mechanical and chemical resistance is required" [R3] [V] |
| PEEK add-on | resistant | resistant | UNVERIFIED |
| SU-8/PI passivation | cross-linked epoxy, expected resistant | expected resistant | UNVERIFIED |
| PET substrate | slow hydrolysis in strong alkali; negligible at pH 10, room temperature, 1 h | resistant | UNVERIFIED |
| Printed dielectric ink | **unknown** (composition not published) | unknown | vendor question (§8) |
| Glass, Ti/Au, Ti/Pt | resistant; Au see chloride note | resistant | [R7] [V] for materials |

**Reproducibility.** Vendor data, CV peak current between different electrodes: S1PE-C10 RSD 3 % (n = 5,
ferrocyanide) and 2 % (n = 5, ferrocene methanol) [R12] [V]; thin-film SE1-Pt RSD 4 % (n = 5), SE1-Au 6 % (n = 4)
[R10] [V]. A bead-based procalcitonin sandwich read on disposable screen-printed carbon reported RSD < 9 %, LOD
0.1 ng/mL in 25 µL, < 20 min (Molinero-Fernández 2020, listed on the MicruX publication page) [R26] [V abstract].
These are faradaic, not blank-signal, figures: the unit-to-unit SD of the *blank* of an immunoassay on fresh
electrodes is not published for these products and must be measured (docs/26 §3).

**Use under flow (literature).** MicruX lists flow work with its cells, e.g. Trindade et al. 2018 (flow cell with the
RE in a separate compartment against bubbles) [R27] [V abstract; whether MicruX parts were used is not stated in the
abstract] and Herl & Matysik 2017 (flow cells with disposable electrodes coupled to MS) [R28] [listed only, not
opened]. No paper giving the internal geometry of the AIO flow add-ons was found.

---

## 5. Geometry table for the calculation kit

Confidence: V = vendor document; D = Derived from V; U = UNVERIFIED estimate (range to be used in Monte Carlo).

| Combination | Chamber (D × h) | Volume | WE area, position | Inlet | Confidence |
|---|---|---|---|---|---|
| A. AIO-SPE flow + S1PE-C21 (or CG21) | D = 8 mm (V); h ≤ 0.1 mm (D) — use 0.1–0.5 mm (U) | < 5 µL (V); 5–25 µL (U) | 7.1 mm² disc, under the jet, centred (U) | 0.8 mm bore, wall-jet (V) | geometry U |
| A′. AIO-SPE flow + D2PE | as A | as A | 2 × 2.3 mm² (V), off-centre (U) | as A | U |
| B. AIO flow FC-2.0 + SE1-Au/Pt | D = 2.0 mm (V); h ≤ 0.16 mm (D) — use 0.1–0.3 mm (U) | < 0.5 µL (V); 0.3–1 µL (U) | 0.785 mm² (D), centred (U) | 0.5 mm bore, wall-jet (V) | U |
| C. AIO flow FC-2.0 + IDA1/5/6 or IDRA1 | as B | as B | per WE 0.15–0.20 mm² (U), array 0.6 mm wide (D) | as B | U |
| D. AIO flow FC-3.5 + IDE | D = 3.5 mm (V); h 0.05–0.3 mm (U) | < 0.5 µL (V); 0.5–3 µL (U) | 90–180 finger pairs in 3.5 mm opening (V) | as B | U |
| E. AIO thin-layer add-on 1.0 | **no data** | — | — | — | listed by PalmSens only [R5] |
| F. Drop cell / AIO base, no add-on | drop on 2 mm opening | 1–10 µL drop (V) | as chip | none (static) | V |

Exposed non-WE area (adsorbs conjugate): A ≈ 50 mm² minus WE (D); B, C ≈ 3.1 mm² minus WE (D).

---

## 6. Passive in-line parts for tier 2

| Class | Example | Key data | Evidence |
|---|---|---|---|
| (a) Frit / micro-column | IDEX/Upchurch M-560-1 precolumn MicroFilter, 0.5 µm PEEK frit, 1/16″ | part no., frit, porosity [V, title only]; swept volume 0.5 µL, 4000 psi | [R29] [S] |
| (a) | Upchurch in-line MicroFilter, PEEK frit, total void volume 240 nL | [S]; part no. not confirmed | [R30] [S] |
| (a) | Biotech Fluidics A-431 in-line filter, SS body, 0.5 µm | swept volume 5.9 µL | [R31] [S] |
| (a) bed holder | A 1/16″ union or short 0.5–0.8 mm ID PEEK tube packed against a frit: bed 0.2–10 µL ↔ 0.5 mm ID × 1–50 mm (Derived: πr²L) | — | UNVERIFIED |
| (b) Superparamagnetic 1–3 µm | Dynabeads M-280 Streptavidin (11205D): 2.8 µm; 10 mg/mL ≈ 6–7 × 10⁸ beads/mL; ~10 µg biotinylated antibody per mg; 650–900 pmol free biotin per mg | | [R32] [V full text] |
| (b) 10–50 µm streptavidin particles | Spherotech SVP-200-4, streptavidin polystyrene 18.0–24.9 µm, 0.5 % w/v, 4 mL; SVP-100-4 10.0–14.0 µm; SVP-150-4 14.0–17.9 µm | | [R33] [S] |
| (b) | POROS-type perfusion media are 20–50 µm (POROS GoPure XS column page opened: 50 µm PS-DVB, 30 bar) — streptavidin POROS not opened | | [R34] [V for the SP column only] |
| (c) Magnet | supermagnete S-05-05-N: NdFeB N45 disc 5 × 5 mm, Ni-Cu-Ni, axial, ≈ 9.2 N adhesive force, 80 °C max | | [R35] [V] |
| (c) | Any N42–N52 disc or block 3–10 mm against 0.25–0.5 mm ID tubing holds 1–3 µm beads at µL/min flows | | UNVERIFIED; bench test E-capture |

---

## 7. Additions for tier 3

* **Second channel from Gamry.** Gamry's bipotentiostat is "two fully-functional Gamry potentiostats with their timing
  synchronized"; listed pairs: Interface 1010/5000, Reference 620, Reference 3000 and mixes [R36] [V]. The page names
  the Reference 620 and (in its specifications) the "Reference 600+"; Gamry's legacy page states that the 600+ has
  been replaced by the 620 [R37] [S]. Whether the user's 600+ can be paired with a new 620, the sync cable, the
  software (Framework scripts or Toolkit) and grounding rules are not stated: Gamry question. Both channels are
  isolated from earth [R24] [V], which is what allows two working electrodes in one cell.
* **MicruX bipotentiostat.** ECStat (ECSTAT2020), USB-powered workstation, 5 fA resolution on the 100 pA range,
  75 µV DC accuracy; ECSTAT-USB-CABLE plugs straight into the AIO platform's mini-USB connector [R38] [R22] [V].
  ECSens-BIPOT also exists (brochure not read). With an IDA/IDRA this gives generator–collector mode (Rc 2–3, §2.2).
* Other tier-3 parts (valves, dosing pump, custom add-on with a defined thin-layer channel) follow docs/05, docs/07,
  docs/13; MicruX offers custom add-ons and microfluidic chips [R2] [R39] [V].

---

## 8. Questions for MicruX and dimensions to read off the cell in hand

**To MicruX (send as is).**
1. ED-AIO-SPE-ADD-ON-FC-PMMA and ED-AIO-ADD-ON-FC-PMMA-2.0: drawing with chamber height (O-ring compression gap),
   nozzle-to-electrode distance, outlet position and bore, and how "< 5 µL" and "< 500 nL" were defined.
2. "Thin Layer PMMA-1.0 / PEEK-1.0" add-on (PalmSens listing): does it exist, geometry (channel height, width, length,
   inlet/outlet over the WE), volume?
3. O-ring material, cross-section and compression for each add-on; spares part numbers.
4. Maximum pressure for each flow add-on (we need the cell at ≤ 1–2 bar at 10–200 µL/min).
5. Dielectric ink of the S1PE strips: composition, opening dimensions around WE, CE, RE; resistance to pH 10 carbonate
   and 0.1 M HCl for 1 h.
6. Lot-to-lot and strip-to-strip SD of WE area or capacitance for C10/C21/CG21 and of SE1/IDA thin-film chips.
7. ED-mSE1: disc diameter, number, pitch. IDA/IDRA: finger length and total area per WE.
8. Pinout and lead labels of ED-SPE-CABLE and the AIO universal cable.
9. Custom thin-film chip with a 1 mm Ø WE and Ag/AgCl reference (thin-film Ag?), and custom add-on with a defined
   50–100 µm thin-layer channel: feasibility, lead time, price.

**Read off the cell in hand (user).**

| Dimension | How |
|---|---|
| O-ring I.D., cross-section, recess depth | calipers; O-ring gauge |
| Chamber height under load | depth gauge on the add-on face vs O-ring proud height; or fill with water and weigh (V = Δm/ρ, 1 mg ≈ 1 µL) |
| Total internal volume inlet port → outlet port | weigh dry and filled; or tracer step (ferrocyanide) at known flow: V = Q·t₅₀ |
| Inlet and outlet bore diameters and lengths; outlet position relative to WE | pin gauges; photograph through the transparent PMMA |
| Where the jet hits relative to the WE | photograph through PMMA with a strip in place |
| Pressure limit | stepwise flow increase with a pressure gauge until weeping (do on a spare strip) |
| Strip part number in hand (C10/C21/CG21/Au10) and chip type | label on the pack |

---

## 9. References

| Key | Document | URL |
|---|---|---|
| R1 | MicruX, All-in-One SPE platform brochure (2025) | https://www.micruxfluidic.com/wp-content/uploads/MicruX_AIO-SPE-cell.pdf |
| R2 | MicruX, All-in-One platform for thin-film electrodes brochure (2025) | https://www.micruxfluidic.com/wp-content/uploads/MicruX_AIO-cell.pdf |
| R3 | MicruX, Add-ons for AIO platform brochure (2025) | https://www.micruxfluidic.com/wp-content/uploads/MicruX_AIO-Add-ons.pdf |
| R4 | MicruX product pages: AIO platform; AIO add-ons; AIO-SPE platform; AIO-SPE add-ons | https://www.micruxfluidic.com/product/all-in-one-platform/ ; https://www.micruxfluidic.com/product/all-in-one-plataform-add-ons/ ; https://www.micruxfluidic.com/product/all-in-one-spe-plataform/ ; https://www.micruxfluidic.com/product/all-in-one-spe-plataform-add-ons/ |
| R5 | PalmSens pages: AIO drop-cell base; AIO add-on; AIO-SPE platform | https://www.palmsens.com/product/micrux-one-cell/ ; https://www.palmsens.com/product/add-on-for-micrux-all-in-one-drop-cell/ ; https://www.palmsens.com/product/micrux-all-in-one-spe-platform/ |
| R6 | MicruX, Flow system accessories brochure (2025) | https://www.micruxfluidic.com/wp-content/uploads/MicruX_flow_system_accessories.pdf |
| R7 | MicruX FAQ (materials, SU-8 layer) | https://www.micruxfluidic.com/support/faq/ |
| R8 | MicruX, accessories and cables data sheet | https://www.micruxfluidic.com/product/spe-connectors/ ; https://www.micruxfluidic.com/product/thin-film-connectors/ |
| R9 | MicruX, IDE product page | https://www.micruxfluidic.com/product/interdigitated-electrodes-ide/ |
| R10 | MicruX, thin-film single electrodes brochure | https://www.micruxfluidic.com/wp-content/uploads/MicruX_thin-film_SE_electrodes.pdf |
| R11 | MicruX, S1PE single electrodes page | https://www.micruxfluidic.com/product/single-electrodes-s1pe/ |
| R12 | MicruX, thick-film carbon S1PE brochure | https://www.micruxfluidic.com/wp-content/uploads/MicruX_thick-film_S1PE_carbon-electrodes.pdf |
| R13 | PalmSens, Micrux thick-film electrodes | https://www.palmsens.com/product/micrux-thick-film-electrodes/ |
| R14 | MicruX, mediated S1PE page | https://www.micruxfluidic.com/product/mediated-single-electrodes-s1pe/ |
| R15 | MicruX, D2PE page | https://www.micruxfluidic.com/product/dual-electrodes-d2pe/ |
| R16 | MicruX, thin-film IDA brochure and page | https://www.micruxfluidic.com/wp-content/uploads/MicruX_thin-film_IDA_electrodes.pdf ; https://www.micruxfluidic.com/product/interdigitated-microelectrodes-array-ida/ |
| R17 | MicruX, thin-film sensors on demand brochure; custom thin-film page | https://www.micruxfluidic.com/wp-content/uploads/MicruX_thin-film_sensors.pdf ; https://www.micruxfluidic.com/custom-solutions/thin-film-electrodes-manufacturing/ |
| R18 | MicruX, SE Au/Pt brochure | https://www.micruxfluidic.com/wp-content/uploads/MicruX_thin-film_SE_AuPt_electrodes.pdf |
| R19 | BASi, thin-film IDA page | https://www.basinc.com/thin-film-interdigitated-micro-array-electrodes_ |
| R20 | MicruX, IDRA1 brochure | https://www.micruxfluidic.com/wp-content/uploads/MicruX_thin-film_IDRA1_electrodes.pdf |
| R21 | MicruX, custom printed electrodes | https://www.micruxfluidic.com/custom-solutions/printed-electrodes-manufacturing/ |
| R22 | MicruX, replacements; device accessories | https://www.micruxfluidic.com/product/replacements-for-platforms/ ; https://www.micruxfluidic.com/product/device-accessories/ |
| R23 | Gamry, cell cable integrity note (colours via search summary) | https://www.gamry.com/application-notes/instrumentation/checking-the-integrity-of-a-gamry-cell-cable/ |
| R24 | Gamry, Reference 600+ data sheet (2018) | https://www.gamry.com/assets/Uploads/Reference-600+2018.pdf |
| R25 | Search results on printed pseudo-references (USN open archive; Southampton theses) | https://openarchive.usn.no/usn-xmlui/handle/11250/2591002 |
| R26 | Molinero-Fernández et al., Biosensors 2020, 10, 66 (PMID 32560303) | https://doi.org/10.3390/bios10060066 |
| R27 | Trindade et al., Anal. Chem. 2018, 90, 10917 (PMID 30125484) | https://doi.org/10.1021/acs.analchem.8b02438 |
| R28 | MicruX publication list (Herl & Matysik, tm 2017, 84, 672) | https://www.micruxfluidic.com/publications/ |
| R29 | IDEX M-560-1 precolumn MicroFilter | https://www.idex-hs.com/store/product-detail/precolumn_microfilter_0_5_m_peek_for_1_16_od_1_peek_frit ; https://biotechfluidics.com/product/precolumn-microfilter-0-5a%C2%B5m-peek-for-116-od-1-peek-frit/ |
| R30 | Avantor, Upchurch precolumn and in-line MicroFilters | https://www.avantorsciences.com/us/en/product/16132928/precolumn-and-inline-microfilters-upchurch-scientific |
| R31 | Biotech Fluidics in-line filter assembly | https://biotechfluidics.com/product/inline-filter-assembly-0-5a%c2%b5m/ |
| R32 | Thermo Fisher, Dynabeads M-280 Streptavidin user guide MAN0014017 | https://assets.thermofisher.com/TFS-Assets/LSG/manuals/MAN0014017_Dynabeads_M280_Streptavidin_UG.pdf |
| R33 | Spherotech coated particles (catalogue PDF; Fisher NC0708720) | https://spherotech.com/coa_pol_par.htm ; https://www.fishersci.com/shop/products/streptavidin-5-wv-18-24-9-4ml/NC0708720 |
| R34 | Thermo Fisher, POROS GoPure XS column 4481317 | https://www.thermofisher.com/order/catalog/product/4481317 |
| R35 | supermagnete S-05-05-N | https://www.supermagnete.de/eng/disc-magnets-neodymium/disc-magnet-diameter-5mm-height-5mm-neodymium-n45-nickel-plated_S-05-05-N |
| R36 | Gamry, bipotentiostat | https://www.gamry.com/potentiostats/bipotentiostat/ |
| R37 | Gamry, Reference 600+ legacy page | https://www.gamry.com/support-2/legacy-devices/reference-600plus-legacy/ |
| R38 | MicruX, ECStat brochure | https://www.micruxfluidic.com/wp-content/uploads/MicruX_ECStat.pdf |
| R39 | MicruX, custom microfluidic manufacturing | https://www.micruxfluidic.com/custom-solutions/microfluidic-manufacturing/ |
