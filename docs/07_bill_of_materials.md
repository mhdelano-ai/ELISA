# 07 — Bill of materials by stage (Task 5)

> **Revised after the final review (docs/08 §10):** separate bead and conjugate reservoirs (B4, §2 and §5.5); the
> Stage-3 default detector is a commercial single-channel thin-layer cell and the custom IDA cell and second
> potentiostat channel are conditional on G2 data (S9, §3); Gamry bipotentiostat statement corrected (docs/08 §9
> C11); non-immune beads made with normal goat F(ab′)₂ (W8). BLI/SPR and NISTmAb are ordered after G1a (S8).

> **Added 2026-11-12:** §8, cartridge track — only the M5a items are purchasable now; post-G1 stages by cost class
> only (docs/16).

Status: 2026-11-11. Companion to `docs/06_bench_plan.md`; stages and gates are defined there. **Nothing in a later
stage is ordered before its gate passes**; quotes and lead times for later stages are requested in Stage 0 so the
order can be placed on the gate day.

**Verification tags (this session).**
* **[V]** the product and part number were seen on the manufacturer's page or listing (URL in §7).
* **[D]** seen only on distributor or third-party listings (manufacturer page not reached) — confirm on ordering.
* **[S]** seen only in a search-engine summary or accessory list.
* **UNVERIFIED** not checked; no part number is given for these and none must be invented.
Prices are given only where a listing showed one, as dated indications (they are not quotes); everything else:
price not checked. Lead times are UNVERIFIED unless stated.

---

## 0. Stage 0 — set-up (order in week 0)

| Item | Specification | Purpose (docs/06) | Qty | Candidate supplier / part | Alternatives | Lead time / notes |
|---|---|---|---|---|---|---|
| USB DAQ | ≥ 4 digital inputs with counter/edge capture, ≥ 2 digital outputs, Python library | Inject Start + 2-bit line code; magnet TTL (S0.3) | 1 (+1 spare) | LabJack U3 (U3-HV variant) with LabJackPython **[V]** (labjack.com support pages; note: on the U3-HV, FIO0–3 are analog-only) | NI USB-6001, Measurement Computing USB-1208 (UNVERIFIED) | stock item (UNVERIFIED) |
| Opto-isolator / relay input module | isolates the SM-FL contact closure from the DAQ | S0.3 | 2 | UNVERIFIED (any DIN-rail opto-input module rated for dry contacts) | — | — |
| SM-FL I/O cable | mating connector for SM-FL connector 1 (Inject Start, pins 1–2, docs/02 §3.1) | S0.3 | 1 | UNVERIFIED (ask Waters; connector type not documented in reachable pages) | — | — |
| Faraday cage | grounded mesh enclosure for the cell | S0.5 and all EC work | 1 | UNVERIFIED (Gamry or generic) | home-made Cu mesh box | — |
| Analytical balance access, weighed vials | gravimetric BSM flow check | S0.6 | — | in-house | — | — |
| Flow restrictor | ≥ 1000 psi back-pressure for the BSM (docs/02 §1.2) | T1 plumbing | 1–3 | Waters restrictor kit 205000547 (40 µm × 35 cm PEEK-SIL) — docs/02 [V: WKB5084] | narrower PEEKsil restrictor (UNVERIFIED) | check if already installed |

## 1. Stage 1 — reachability (order in week 0; no flow hardware)

### 1.1 Reagents

| Item | Specification | Purpose | Qty (Stage 1) | Candidate supplier / part | Alternatives | Notes |
|---|---|---|---|---|---|---|
| Streptavidin magnetic beads | 2.8 µm, superparamagnetic, 10 mg/mL | capture/non-immune beads (E1.3–E1.10) | 2 × 2 mL (≈ 15 mg used in Stage 1; same lot for Stage 2) | Thermo Fisher Dynabeads M-280 Streptavidin **11205D [V]** (2 mL; PBS + 0.02 % NaN₃; some lot documents list 0.1 % BSA — bovine IgG risk, E1.4; indicative US price 586.38 USD in an offer that ended 16-Dec-2024) | Dynabeads M-270 Streptavidin (BSA-free, hydrophilic; part number not checked) | Thermo states background may come from BSA on the M-280 surface — the M-270 is the first alternative if E1.4 shows bovine effects |
| Capture antibody, biotinylated | anti-human IgG **Fcγ-specific**, F(ab′)₂, affinity-purified, min. cross-reactivity bovine/horse/mouse | capture beads | 1 unit | Jackson ImmunoResearch Biotin-SP AffiniPure F(ab′)₂ goat anti-human IgG, Fcγ-specific **109-066-098 [D]** (Biozol listing; Fc specificity wording to be checked on the datasheet) | Mabtech MT145 (in kit 3850 series) biotinylated in-house (biotinylation reagent UNVERIFIED part) | k_off unknown → E1.6 |
| Detection conjugate D1 | ALP-labelled F(ab′)₂ goat anti-human IgG **F(ab′)₂/Fab-specific** (asymmetric to the Fc capture; same species as capture) | U1, all assays | 2 units | Jackson ImmunoResearch AP AffiniPure F(ab′)₂ fragment goat anti-human IgG, F(ab′)₂ fragment specific **109-056-006 [D]** (reacts with Fab, not Fc, per listing) | chicken IgY anti-human IgG-ALP (UNVERIFIED supplier) | Do not confuse with the Fc-specific AP conjugate **109-056-190 [V]** (Jackson page seen; 0.5 mL) — symmetric with an Fc capture |
| Detection conjugate D2 | whole-IgG ALP conjugate of the same specificity (for the L3 F(ab′)₂/IgG ratio) | U1 L3 arm | 1 unit | Jackson whole-IgG AP anti-human IgG F(ab′)₂-specific — a SelectScience listing exists, **part number UNVERIFIED** | Mabtech kit **3850-1AD-6** (ALP version, MT145/MT78; docs/01 [V]) | — |
| Non-immune biotinylated F(ab′)₂ | biotinylated **normal goat F(ab′)₂** (same species and fragment format as the capture F(ab′)₂, so non-immune beads differ only in specificity; revised after final review, W8) | non-immune beads (E1.3, E1.4) | 1 unit | UNVERIFIED (normal goat F(ab′)₂ fragment and its biotin conjugate: part numbers not checked) | biotinylate normal goat F(ab′)₂ in-house | — |
| Analyte primary standard | NISTmAb RM 8671, humanized IgG1κ, 10 mg/mL, 800 µL | calibrators (E1.5, E1.8, E1.10, validation); **order after G1a** (revised after final review, S8) | 1 | NIST RM 8671 via Merck/Sigma **nist8671 [D]** (indicative 1,900 USD per unit, US listing) | — | gravimetric dilution, docs/06 E1.8 |
| Polyclonal human IgG standard | NIBSC-calibrated human IgG | subclass/light-chain check | 1 | standard supplied in Mabtech 3850 kits (docs/01 [V]) | — | — |
| IgG-free BSA | bovine IgG not detected, protease-free | blocker and carrier in every buffer | 50 g | Jackson ImmunoResearch **001-000-162 [V]** (indicative 569.45 USD via a distributor) | — | standard BSA grade only as the E1.4 comparator (any lot) |
| HQDP | hydroquinone diphosphate, ALP substrate | substrate (E1.2, all assays) | 2 × 0.5 g, two lots if possible | Metrohm DropSens **DRP-HQDP-0.5G [V]** (500 mg; 1 g also listed); **no purity or free-HQ specification on the product page** | 4-aminophenyl phosphate (Abcam ab141899 [D]); ascorbic acid 2-phosphate (supplier UNVERIFIED); p-hydroxyphenyl phosphate (supplier UNVERIFIED) | ask for CoA and lot history; lead time UNVERIFIED |
| Hydroquinone standard | ≥ 99 % | HQ calibration (E1.1, E1.2) | 5 g | Sigma-Aldrich **H9003 [V]** (ReagentPlus ≥ 99 %) | — | carcinogen cat. 2 — handle per SDS |
| pNPP | 4-nitrophenyl phosphate disodium salt hexahydrate | optional optical cross-check of conjugate activity | 1 | Sigma-Aldrich **71768** or **N4645 [D]** | — | optional |
| ALP enzyme (free) | bovine intestinal, ≥ 10 DEA U/mg solid | optional readout check | 1 | Sigma-Aldrich **P7640 [D]** | — | optional; the conjugate itself is the standard (docs/06 §1 point 4) |
| Buffers, Tween-20, MgCl₂, Tris, D-biotin, phosphate salts, HCl | analytical grade | AB, SB, quench, E1.7 | — | any (generic) | — | made in glass or LoBind |
| 1,4-Benzoquinone | ≥ 98 %, reference standard | BQ-spike control and peak identification in the pre-electrolysis test (docs/06 E1.2b, added 2026-11-12) | 1 small pack | to be selected — supplier and part number not checked (UNVERIFIED); price on request | — | toxic/irritant — handle per SDS; dissolve fresh, dark |

### 1.2 Consumables and small hardware

| Item | Specification | Purpose | Qty | Candidate supplier / part | Notes |
|---|---|---|---|---|---|
| Magnet rack | for 1.5–2 mL tubes, Dynabeads 1–4.5 µm | all tube work | 1 | Thermo Fisher DynaMag-2 **12321D [V]** (indicative 878 USD) | — |
| Low-binding tubes | 1.5 mL Protein LoBind | everything ≤ 1 ng/mL | 4 × 100 | Eppendorf Protein LoBind **0030108116 [V]** (one Eppendorf page lists this number as 2.0 mL and 1.5 mL as 0030108094 — check on ordering) | — |
| Low-binding autosampler vials | 300 µL, 12 × 32 mm, MaxPeak HPS | SM-FL injections (E1.10, later all) | 2 × 100 | Waters QuanRecovery with MaxPeak HPS **186009186 [V]** (cap configuration differs between listings) | standard PP vials as E1.10 comparator |
| Filter tips, dedicated pipettes | — | clean handling (docs/06 §8.1) | — | in-house | — |
| Tube rotator | end-over-end, 22 °C | bead incubations | 1 | any | — |
| Screen-printed electrodes, carbon | DropSens carbon SPE (e.g. DRP-110) | R-drop and wall-jet cell | 2 × 75 | Metrohm DropSens DRP-110 — product page **not reached (UNVERIFIED)** | gold SPE DRP-250BT (docs/02 [V]) |
| SPE connector | cable connector, any potentiostat | Gamry ↔ SPE | 1 | Metrohm DropSens **DRP-CAC [V]** | — |
| Wall-jet flow cell for SPEs | PEEK, magnetic closure | R-FIA (T1) | 1 | Metrohm DropSens **DRP-FLWCL-PEEK** (docs/02 [V]) | BASi cross-flow thin-layer cell (docs/02 [S]) |
| PEEK tubing and fittings | 1/16″ OD, 127 µm ID; 10-32 coned | T1 plumbing | 3 m, 20 fittings | any LC supplier | — |
| Divided bulk-electrolysis cell | glass, 5–10 mL working compartment, counter electrode in a fritted glass compartment, ports for WE, reference and N₂, stir bar | HQDP pre-electrolysis test (docs/06 E1.2b, added 2026-11-12) | 1 (+1 spare frit compartment) | to be selected (UNVERIFIED; no part number checked); price on request | the undivided arm of E1.2b uses the same cell without the frit compartment |
| Large-area carbon working electrode | reticulated vitreous carbon or graphite felt, ≈ 1 cm³, with a carbon or Pt current collector | E1.2b | 3 pieces | to be selected (UNVERIFIED); price on request | conditioned by pre-electrolysis in SB before each use |
| Counter electrode | Pt wire/mesh or graphite rod | E1.2b | 1 | to be selected (UNVERIFIED) | — |
| Reference electrode | Ag/AgCl, 3 M KCl, with frit, fits the cell port | E1.2b | 1 (+1 spare) | to be selected (UNVERIFIED) | the Stage-3 reference electrode (§3) is a separate, later item |
| Magnetic stirrer | small, low heat output, constant speed | E1.2b | 1 | any (in-house if available) | — |

### 1.3 Services

| Item | Specification | Purpose | Notes |
|---|---|---|---|
| BLI or SPR kinetics | streptavidin or anti-human-Fc sensors; 25 °C; AB; dissociation ≥ 1800 s; k_on screening of all candidates; k_off only for monoclonal candidates, heterogeneous fits for polyclonals (docs/06 E1.6) | E1.6 (U2) | provider UNVERIFIED (core facility or CRO); quote in week 0, **book after G1a** (revised after final review, S8) |

### 1.4 Stage 1C (only if G1 triggers U8)

| Item | Specification | Qty | Candidate | Notes |
|---|---|---|---|---|
| NHS-desthiobiotin | amine-reactive, 50 mg | 1 | Thermo Scientific EZ-Link NHS-Desthiobiotin **16129 [V]** (indicative 298–323 USD) | elution by free biotin (docs/05 §5 U8) |
| D-biotin | ≥ 99 % | 1 g | generic | 2 mM elution buffer |
| Phase-2 capture antibody | anti-human IgG, epitope not used by capture/detection, no reactivity to goat IgG | 1 | **UNVERIFIED** — to be identified (docs/06 §4.12) | screen by E1.4-type test |
| Desalting columns | for removing free desthiobiotin | 5 | UNVERIFIED part | — |

## 2. Stage 2 — flow path on the Waters stack (order at G1)

| Item | Specification | Purpose | Qty | Candidate supplier / part | Alternatives | Lead time / notes |
|---|---|---|---|---|---|---|
| V2 reactor-isolation valve | 2-position, **10-port**, PEEK wetted, 10-32 ports, remote control | trap isolation (docs/05 §4.1) | 1 | IDEX Health & Science MX Series II **MXP9960-000 [V]** (PEEK, 0.25 mm stator passages, 5000 psi per IDEX/Chromtech; one listing says 6000 psi) | VICI/Valco 10-port (UNVERIFIED part) | control: push button, contact closure, I²C, RS-232 or USB (MX Series II manual [V]); serial command set not read — driver stub |
| V3 cell bypass and V4 cup valve | 2-position, **6-port**, PEEK | EC cell in/bypass; SM-FL → cup / → tee | 2 | IDEX MX Series II **MXP9900-000 [V]** (PEEK, 0.30 mm passages) | — | as V2 |
| SIA syringe pump with distribution valve | 1 mL syringe, ≥ 8-port distribution valve, RS-232, inert wetted path | bead dosing and conjugate dosing from **separate** reservoirs (ports 1 and 6), cup mixing and emptying, wash, waste, line to the trap (6 of 8 ports; 2 spare, e.g. a second cup) (docs/05 §4.1, revised after final review, B4) | 1 (+1 spare valve) | Hamilton PSD/6 (e.g. **99196-01**) with 8-port distribution valve **59943-01** (Hamaflon plug) or **59943-02D** (ceramic) **[V spec sheet; a distributor lists a different ceramic number]** | Tecan Cavro Centris (RS-232/485; distribution valves 3/6/9/12 ports — **no 8-port listed**, use 9-port) [V] | syringe part and command language UNVERIFIED; driver stub |
| Prototype incubation cup | LoBind tube in a holder with bottom port and vent (§5.1, simplified) | E2.4, E2.7 | 3 | in-house (3-D print/machining) | — | — |
| Prototype magnetic trap | PEEK tube segments 0.75/1.0/1.5 mm ID, NdFeB magnets on a slide (§5.2, simplified) | E2.3, E2.5 | 3 variants × 2 | in-house; PEEK tube and NdFeB magnets from any supplier (UNVERIFIED parts) | electromagnet | — |
| Magnet actuator | TTL-driven linear actuator or solenoid, ±0.1 mm repeatability | trap on/off | 1 | UNVERIFIED (§5.4) | electromagnet with driver | — |
| Stirred cooled bead reservoir | 2–5 mL, 4–8 °C, gentle stirring, sealed; **beads only** (§5.5) | E2.2 | 1 | in-house + small Peltier and stirrer (UNVERIFIED parts) | — | — |
| Cooled conjugate reservoir | 1–2 mL, 4–8 °C, dark, low-binding glass or PP, sealed, not stirred; **conjugate only** (§5.5) (added after final review, B4) | E2.2 (conjugate dose), E2.7 | 1 | in-house; shares the Peltier block with the bead reservoir (UNVERIFIED parts) | — | — |
| PEG/BSA coating materials | for coated-PEEK arm of U4 | E2.5 | — | UNVERIFIED (method from docs/05 L1 references) | — | — |
| Fluorescent/UV tracer | protein-free tracer for plug timing | E2.1, E2.4 | — | any (e.g. a dye with TUV absorbance) | — | — |

## 3. Stage 3 — full primary platform (order at G2)

| Item | Specification | Purpose | Qty | Candidate supplier / part | Alternatives | Lead time / notes |
|---|---|---|---|---|---|---|
| **Default detector (Stage 3)** | commercial single-channel thin-layer flow cell, glassy carbon or Au, PEEK body, ≤ 1 µL internal volume, rated ≥ 1 MPa, external Ag/AgCl; read with the Reference 600+ alone | primary and backup detector (revised after final review, S9) | 1 (+ spare WE block) | BASi cross-flow thin-layer cell (docs/02 [S]; part number not checked) or the DropSens wall-jet cell already used in Stage 1 | Antec/other thin-layer cells (UNVERIFIED) | lead time UNVERIFIED |
| Second potentiostat channel (**conditional**: only if G2 shows electrochemical noise is a material part of the blank SD, docs/06 §5) | Gamry Reference 620, or a second Reference 600+ if Gamry confirms a 600+ pair | IDA collector (docs/05 §4.1) | Option A: 1 (a second 600+ — Gamry's bipotentiostat page shows the 600+ in its specifications section and a video "Bipotentiostat with 2 600+ Potentiostats"; ask Gamry); Option B: 2 Reference 620 (the page lists Reference 620 + 620, 3000 + 3000 and 620 + 3000 pairs, and Interface 1010/5000 pairs; no 600+/620 mixed pair is shown) (corrected after final review, docs/08 §9 C11) | Gamry Reference 620 **[V]** (Gamry: "the Reference 600+ has been replaced with the Reference 620") | Reference 3000 as the partner | bipotentiostat sync cable/kit part UNVERIFIED; ask Gamry (docs/06 S0.2); keep the 600+ for Stage 1–2 and as a third channel (L5) |
| Interim commercial IDA (**conditional**, as the second channel) | Au IDE on glass, 5 µm, with flow cell and connector | E3.1 before a custom cell arrives | 10 chips + 1 cell | Metrohm DropSens **G-IDEAU5** chips, "Flow cell for interdigitated electrodes" (FLWCL-IDE) and IDE cable connector CACIDE — **[S]** (accessory page; finger count, channel height and pressure rating not seen) | BASi/Micrux Pt IDA MX-ED-IDA5-Pt (10 µm width/5 µm gap listed) [S] | channel geometry differs from docs/05; enter its geometry into `ma.geometry.ida_*` |
| Custom flow IDA cell (**conditional**, as the second channel) | §5.3 | optional upgrade of the detector | 1 body + 10 chips | custom (thin-film fab + machining; supplier UNVERIFIED) | — | long lead: plan 8–12 weeks (UNVERIFIED); design/quote during Stage 2, order only on the G2 condition |
| Machined incubation cup | §5.1 | primary | 2 (+1 spare) | custom | — | 4–6 weeks (UNVERIFIED) |
| Integrated bead trap | §5.2 (final variant from E2.3) | primary | 2 (+2 spare) | custom | — | 4–6 weeks (UNVERIFIED) |
| Reference electrode and Pt counter | miniature Ag/AgCl (3 M KCl, frit) side-arm; Pt wire | IDA cell | 2 each | UNVERIFIED parts | leak-free Ag/AgCl micro reference (UNVERIFIED) | — |
| Temperature control (conditional) | Peltier block for cup and trap, ±0.2 °C | if CV_blank correlates with temperature (docs/06 §11) | 1 | UNVERIFIED | column heater module (UNVERIFIED for this geometry) | — |

### 3B. Backup — fixed packed micro-bed (order only if G2 sends the project to the backup)

| Item | Specification | Qty | Candidate | Notes |
|---|---|---|---|---|
| Capture particles | ~50 µm, non-porous, streptavidin (to carry the biotinylated capture antibody) | 4 mL | Spherotech streptavidin polystyrene particles **SVP-400** (38–52 µm, 0.5 % w/v, 4 mL) **[D]** (CHEM/Proscitech listing AU$ 762, 2-week lead time; Gentaur listing) — **non-porosity not stated** | docs/05 §4.2 asked for covalently oriented anti-Fc on 50 µm non-porous particles: no such ready product found (UNVERIFIED) |
| Column body | 0.5 mm ID × 2.5 mm bed (0.5 µL), PEEK, frits retaining ≥ 38 µm particles, screwed into V2 ports 2/3 (§5.6) | 4 | custom | — |
| Glycine-HCl pH 2 | regeneration injections | — | generic | streptavidin–biotin stability at pH 2 UNVERIFIED (docs/06 §6) |

## 4. Stage 4 — validation consumables (order at G3)

| Item | Qty | Notes |
|---|---|---|
| NISTmAb RM 8671 (second unit, if the first is below 50 % or expired) | 1 | same part as §1 |
| Beads, capture antibody, conjugate: a second lot of each if available | 1 each | lot-to-lot evidence (docs/06 §7.1) |
| HQDP | 2 × 0.5 g of the accepted lot | substrate QC per lot (E1.2 short form) |
| QuanRecovery vials, LoBind tubes, filter tips | as used | — |
| Bovine IgG and mouse IgG (specificity, docs/06 §7.9) | 1 each | suppliers UNVERIFIED |

---

## 5. Specifications for custom parts (for a machinist or vendor quote)

### 5.1 Stirred in-line incubation cup (primary; docs/05 §4.0 route A, §4.1)
* Working volume 0.25–0.5 mL (design fill ≈ 220 µL sample + reagent, plus rinses up to 660 µL pass-through);
  total internal volume ≤ 0.8 mL; conical bottom (60–90° included angle) ending in a central outlet.
* Material: PEEK (preferred) or virgin PP; internal surface polished (Ra ≤ 0.4 µm, UNVERIFIED requirement) for low
  protein adsorption; compatible with BSA/PEG coating; no metal wetted.
* Ports: bottom outlet 10-32 coned (1/16″ OD tubing) to the SIA selection valve, dead volume ≤ 2 µL; side inlet
  10-32 coned from V4, entering ≤ 2 mm above the cone so the sample is injected into the liquid; top vent through a
  0.2 µm hydrophobic membrane (no pressure build-up; atmospheric operation).
* Residual liquid after the SIA empties the cup ≤ 2 µL; residual beads after 3 rinses ≤ 10⁻³ of the dose
  (docs/05 §5 U5) — acceptance test E2.4.
* Mixing: by SIA aspirate/dispense (50 µL every 2 min, docs/05 §4.1); optional pocket for a 2 × 5 mm PTFE stir bar
  driven from below (option on the quote).
* Thermal: optional aluminium jacket with Peltier mount, 20–25 °C, ±0.2 °C; thermistor well.
* Quantity: 3 (one spare); a second cup per instrument allows overlap of consecutive samples (docs/05 §4.1).

### 5.2 Integrated magnetic bead trap (primary; docs/05 §1.2, §4.1)
* Trap chamber: inside diameter 1.5 mm (final design; also 0.75 and 1.0 mm variants for E2.3), magnet zone length
  1.1 mm (≈ 2 µL at 1.5 mm ID; variants 1–3 mm), with conical transitions to 0.25 mm ID channels.
* Connection: a PEEK block whose two channels end in 1/16″ OD PEEK stubs (0.25 mm ID, ≤ 5 mm free length each) with
  10-32 finger-tight fittings that screw **directly into V2 ports 2 and 3** (docs/05: isolated tubing 0.01 m total).
* Wall between chamber and magnet ≤ 0.5 mm; magnet pocket for an NdFeB block (e.g. 3 × 3 × 5 mm, grade N50 or
  higher — UNVERIFIED sizing) on an actuated slide that moves ≥ 10 mm away for release.
* Pressure rating ≥ 1 MPa (downstream of the restrictor; the cell side is near atmospheric).
* Wetted materials PEEK only; optional PEG or BSA coating (lever L1).
* Acceptance: retention ≥ 90 % of 5×10⁵ 2.8 µm beads at 100 µL/min (docs/05 §5 U5).

### 5.3 Flow interdigitated-array (IDA) cell (primary detector; docs/05 §4.1, docs/02 §5.2)
* Electrodes: Au or Pt thin film on glass (or Si/SiO₂), **50 finger pairs, 5 µm fingers, 5 µm gaps, 1 mm finger
  overlap**, two separately contacted combs (generator, collector), plus 2 spare pads.
* Channel: **25 µm high × 0.5 mm wide**, ≈ 3 mm long over the array (inlet/outlet margins ≥ 1 mm), defined by a
  laser-cut PET/PTFE gasket or SU-8; internal volume ≤ 0.5 µL including ports.
* Body: PEEK (or PCTFE) clamp; 10-32 coned inlet/outlet for 1/16″ PEEK; replaceable chip.
* Reference: external Ag/AgCl (3 M KCl behind a ceramic frit) in a side arm **downstream** of the array;
  counter: Pt wire downstream.
* Electrical: spring-loaded (pogo) contacts, shielded leads to both potentiostat channels; mountable in a Faraday
  cage; body isolated from earth.
* Ratings: design pressure ≥ 1 MPa; flow 5–300 µL/min.
* Cleaning: electrochemical (potential cycling in buffer); chips exchangeable; order ≥ 10 chips.

### 5.4 Magnet actuator
* TTL input (5 V) from the DAQ; two positions (on: magnet ≤ 0.5 mm from the trap wall; off: ≥ 10 mm away);
  switching ≤ 0.5 s; repeatability ±0.1 mm; position feedback switch (optional) read by the DAQ; fail-safe position
  = **on** (beads held; docs/06 safe state).

### 5.5 SIA reagent reservoirs: beads and conjugate held SEPARATELY (revised after final review, B4)
Beads and conjugate are never stored together: holding beads in ~3.3 nM conjugate for hours would expose them to
~1600 nM·min of conjugate over 8 h against ~11 nM·min in the cup (docs/08 B4; `results/design/shared_reservoir_cost.md`).
* **Bead reservoir (SIA port 1):** 2–5 mL glass or PP vial, sealed with a septum or capped port to the SIA selection
  valve; capture beads at 5×10⁷ /mL in TBS + 1 % IgG-free BSA + 0.05 % Tween (10 µL per dose = 5×10⁵ beads);
  4–8 °C (Peltier); low-shear stirring or rocking that keeps 2.8 µm beads suspended (settling ≈ 7 mm/h, docs/05
  model note) without foaming; dark. Acceptance: bead dose CV ≤ 5 % over 8 h (E2.2).
* **Conjugate reservoir (SIA port 6):** 1–2 mL low-binding glass or PP vial, sealed, 4–8 °C, dark, not stirred;
  ALP conjugate at 6.6 nM in TBS + 1 % IgG-free BSA (10 µL per dose → 0.3 nM in ~220 µL). No phosphate, no azide.
  Maximum life set by the conjugate-only ageing arm of E1.3 (default: refill per 8-h block). Acceptance: conjugate
  dose CV ≤ 5 % (E2.2, by ALP activity of the dispensed dose).
* Between the two doses the SIA flushes its common channel with 50 µL wash buffer to waste (docs/05 §4.1).

### 5.6 Backup micro-bed column
* Bed 0.5 µL: 0.5 mm ID × 2.5 mm bore in PEEK; frits/screens at both ends retaining ≥ 38 µm particles (pore
  10–20 µm, UNVERIFIED); 10-32 male ends screwing into V2 ports 2/3; pressure rating ≥ 1 MPa (Kozeny–Carman drop
  0.001 MPa at 10 µL/min, docs/05 §4.2). Quantity 4.

---

## 6. Open items that docs/05 lists as unverified — status after this task

| Item (docs/05 §7) | What was found in this session | Still open |
|---|---|---|
| HQDP substrate supply | Metrohm DropSens sells HQDP, DRP-HQDP-0.5G (500 mg; 1 g also listed) [V] | purity, free-HQ content, CoA, lead time, second source; p-hydroxyphenyl phosphate supplier not found |
| Pairing a second channel with the Reference 600+ (only needed for the conditional IDA option) | Gamry's bipotentiostat page (re-read 2026-11-11) lists Interface 1010+1010, 5000+5000, 1010+5000, Reference 620+620, 3000+3000, 620+3000; it names the 600+ in the specifications section and shows a video "Bipotentiostat with 2 600+ Potentiostats"; no 600+/620 pair shown; 600+ replaced by 620 [V] (corrected after final review) | Gamry's answer (docs/06 S0.2); if negative, buy two 620s |
| 50 µm antibody particles (backup) | Spherotech streptavidin polystyrene 38–52 µm (SVP-400) on distributor listings [D] | non-porosity; covalently oriented anti-Fc particles of this size not found |
| Interdigitated flow cell | Commercial Au/Pt IDE chips and an IDE flow cell exist (DropSens G-IDEAU5, FLWCL-IDE; BASi/Micrux MX-ED-IDA) [S] | their channel geometry and pressure rating; a fabricator for the custom cell |
| Valves | IDEX MXP9960-000 (10-port PEEK) and MXP9900-000 (6-port PEEK), remote RS-232/USB/contact closure [V] | serial command set; lead time |
| Dispenser (SIA pump) | Hamilton PSD/6 with 8-port distribution valve; Tecan Cavro Centris (3/6/9/12-port valves) [V] | command language; bead compatibility of the valve; dose CV (E2.2) |
| Stirred cup | none commercial identified | custom (§5.1) |
| Bead trap | none commercial identified | custom (§5.2) |
| Gamry ToolkitPy | ships curated Python 3.7.9 32-bit; existing 3.7 32-bit must be removed (docs/02 [V]) | licence terms; two instruments from one process; TTL input reading |
| Empower Toolkit | licensed (docs/00) | whether it can start a sample set (not needed by the primary scheme) |
| BSM precision at 10 µL/min (backup only) | — | S0.6 gravimetric test |

---

## 7. Sources checked in this session

* Metrohm HQDP: https://www.metrohm.com/en/products/d/rp-h/drp-hqdp-0_5g.html
* Metrohm DRP-CAC: https://www.metrohm.com/en/products/d/rp-c/drp-cac.html
* Metrohm IDE flow cell accessory listing (page later returned 404): https://metrohm.com/en_us/products/f/lwcl/flwcl-ide.html
* Thermo Fisher Dynabeads M-280 Streptavidin 11205D: https://www.thermofisher.com/order/catalog/product/11205D ;
  user guide https://assets.thermofisher.com/TFS-Assets/LSG/manuals/MAN0014017_Dynabeads_M280_Streptavidin_UG.pdf
* Thermo Fisher DynaMag-2 12321D: https://thermofisher.com/order/catalog/product/12321D
* Thermo Fisher EZ-Link NHS-Desthiobiotin 16129: https://thermofisher.com/order/catalog/product/16129
* Jackson ImmunoResearch 001-000-162: https://jacksonimmuno.com/catalog/products/001-000-162 ; 109-056-190:
  https://jacksonimmuno.com/catalog/products/109-056-190 ; 109-056-006: https://www.jacksonimmuno.com/catalog/products/109-056-006 ;
  109-066-098 (distributor): https://biozol.de/en/product/jim-109-066-098
* NISTmAb RM 8671 (Merck listing): https://www.sigmaaldrich.com/US/en/product/sial/nist8671
* Sigma-Aldrich hydroquinone H9003: https://www.sigmaaldrich.com/product/sial/h9003 ; P7640:
  https://www.sigmaaldrich.com/product/sigma/p7640 ; 4-nitrophenyl phosphate 71768: https://sigmaaldrich.com/MD/en/product/sigma/71768
* Abcam 4-aminophenyl phosphate ab141899: https://www.abcam.com/en-us/products/biochemicals/4-aminophenyl-phosphate-monosodium-salt-alkaline-phosphatase-substrate-ab141899
* Eppendorf Protein LoBind 0030108116: https://eppendorf.com/gb-en/Products/Laboratory-Consumables/Tubes/Protein-LoBind-Tubes-p-0030108116
* Waters QuanRecovery 186009186: https://www.waters.com/nextgen/us/en/shop/vials-containers--collection-plates/186009186-quanrecovery-with-maxpeak-hps-12-x-32-mm-screw-neck-vial-300--l-.html
* IDEX MXP9900-000: https://www.idex-hs.com/store/product-detail/mx_series_ii_2_position_6_port_peek_switching_valve/mxp9900-000 ;
  MX Series II manual: https://www.idex-hs.com/docs/uploads/2018/11/MX-Series-II-Operating-Manual.pdf ;
  MXP9960-000 listing: https://biotechfluidics.com/product/mx-series-iitm-2-position10-port-peek-switching-valve/
* Hamilton PSD/6 spec sheet: https://assets-oem.hamiltoncompany.com/File-Uploads/PSD-6-SpecSheet_R8-1.pdf
* Tecan Cavro Centris: https://partnering.tecan.com/cavro-centris-pump-for-oem-liquid-handling
* LabJackPython: https://support.labjack.com/docs/labjackpython-for-ud-exodriver-u12-windows-mac-lin
* Gamry Reference 620 and bipotentiostat: https://www.gamry.com/potentiostats/reference-620/ ;
  https://www.gamry.com/potentiostats/bipotentiostat/ ; legacy 600+: https://www.gamry.com/support-2/legacy-devices/reference-600plus-legacy/
* Gamry ToolkitPy support page: https://www.gamry.com/support-2/software/echem-toolkitpy/
* Spherotech SVP-400 (distributors): https://gentaur.com/spherotech/streptavidin-polystyrene-particles-05wv-38-52m-4ml-01025713024 ;
  https://proscitech.com.au/pages/coated-particles
* BASi MX-ED-IDA5-Pt: https://basinc.com/products/MX-ED-IDA5-Pt
* CLSI EP17 replicate numbers (secondary sources only): https://metricgate.com/docs/clsi-ep17-detection-limit/ ;
  https://www.westgard.com/probit-part-one.htm

---

## 8. Cartridge track (second generation; added 2026-11-12, docs/16)

Only the items of the approved pre-G1 test **M5a** (docs/06 M5a; docs/13 §10.1) are purchasable now. Nothing in this
section is bought for gen-1, and nothing beyond M5a is ordered before a G1 GO or GO-WITH-LEVER and the E1.2b result
(docs/16 §6). Sources are the docs/11 keys (URLs in docs/11 §9); no part number or price below was checked in this
session beyond what docs/11 records.

### 8.1 M5a — purchasable now

| Item | Specification | Purpose (docs/06 M5a) | Qty | Candidate supplier / part | Price / notes |
|---|---|---|---|---|---|
| Catalogue Au thin-film electrode dies | glass, Au 150 nm on 50 nm Ti, support 10 × 6 mm, Au RE and CE on the die; IDA with both combs joined as one WE, or single thin-film electrodes | the WE of the clamp cell | 5–10 | Micrux IDA family, e.g. **MX-ED-IDA6-Au** (5/5 µm, 30 pairs) or MX-ED-IDA1-Au **[S/D as docs/11 §2.3: BASI_IDA (H), PALMSENS_IDA (M)]**; Micrux thin-film single electrodes (catalogue existence only, DI_MICRUX_SINGLE, L; geometry and part numbers UNVERIFIED) | **price on request** (docs/11 §2.3); pad pitch and position UNVERIFIED — get the datasheet before the clamp cell is drawn |
| Die holder / connection | Micrux connection platform ("one of the Micrux cells is necessary to connect", PALMSENS_IDA): AIO platform, optional flow add-on in PMMA or PEEK | incoming CV check of each die; reference connection before mounting in the M5a clamp | 1 | Micrux AIO platform (PALMSENS_AIO, DI_AIO, M); flow add-on ref. "MX-ED-AIO-ADD-ON-FC-PMMA" seen only in a search summary (docs/11 §2.3) — **confirm on quote** | price on request; the M5a clamp itself (pogo from below through a contact window) is custom, below |
| Clamp-cell laminate parts | 140 µm COC foil; laser-cut 0.175 mm COC sheet; 25 µm double-sided adhesive film; TPE coupons 0.3–0.5 mm; PMMA/PEEK clamp with a contact window | reproduces the docs/13 §2 stack; one cell with 0.5 mm, one with 1.0 mm stubs | 1 clamp + 10 laminate sets | in-house laser cutting or a laminate supplier (docs/11 §1.3; COC foil thickness DARWIN_CS4CH); materials UNVERIFIED | cost class low (docs/13 §11); no prices seen |
| Spring-loaded (pogo) contacts | gold-plated, low-leakage mounting (≥ 5×10¹² Ω pad-to-WE target) | contact from below | 1 set (6–10 pins) | to be selected (Mill-Max page returned 403, docs/11 §5.4) — UNVERIFIED | low |
| Grounded Faraday box, 25.0 °C block | as Stage 0 Faraday cage; small Peltier or heated block | shielding, temperature | 1 | Stage 0 cage reused if it fits; block UNVERIFIED | low |
| Docked Ag/AgCl reference + high-impedance voltage input (≥ 10¹² Ω) | salt-bridge reference; electrometer-grade input logged by the PC | QRE drift log (M5a-5) | 1 | Stage-1 E1.2b reference electrode type (§1.2) may be reused; voltage input to be selected (UNVERIFIED) | low |
| Noise-source kit | solenoid plunger, small stepper with chopper driver + 2 × 2 × 4 mm NdFeB magnet, syringe pump (gen-1 class, or borrowed), Peltier module on PWM, reed relay | M5a noise-source arms | 1 | to be selected (docs/13 §11: "low, to be selected") — no part numbers | low |
| HQDP at 3 mM, NaCl | Stage-1 HQDP lot (§1.1 DRP-HQDP-0.5G), NaCl analytical grade | substrate of the reads | — | from Stage-1 stock | — |

Reused, not bought: Gamry Reference 600+ (in hand), Stage-1 HQ standards and SB components.

### 8.2 Post-G1 cartridge stages — cost class only

Cost class [assessment, docs/13 §11]: **low** < €1 k, **medium** €1–10 k, **high** > €10 k. Item lists: docs/13 §11;
stage contents and gates: docs/16 §6. No item is ordered before its gate.

| Stage (docs/16 §6) | Gate before ordering | Content (summary) | Cost class |
|---|---|---|---|
| Shared tube test B-E1 = C′-R2 | G1 GO / GO-WITH-LEVER | 10 µm and 50 µm streptavidin particles vs M-280 beads in tubes (gen-1 reagents) | low (particles as §3B; price not checked for 10 µm) |
| C1 mock-ups M1–M8 | G1 GO / GO-WITH-LEVER and E1.2b recorded | laminate coupons and mock-up cards, milled upper bodies, anvil with windows and slot, magnets, Z units and a motorised stage, syringe pumps, 2-channel pressure controller; optional ChipShop Fluidic 1367 reference chips (€34.40 each from 10, CS_1367, docs/11 §2.2) | medium |
| C′ mock-up (only if B-E1 ≤ 2) | B-E1 | milled 0.1 µL cavity with weir, dock pinch/solenoid valves, catalogue IDA die | medium |
| C2 prototype cards and dock | GC1 and gen-1 G2 | custom electrode die wafer run, 10–20 laminated cards, full dock (21 plungers, carriage, 5 pumps, 3 thermal zones, electrode bay) | high (price on request) |
| C3 moulded pre-series | GC2 | upper-body mould (MOQ 100), series lamination, die bonding | high (price on request) |
