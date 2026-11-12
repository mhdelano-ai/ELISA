# 12 — Second-generation cartridge: three candidate architectures

Status: 2026-11-12, first complete pass for the user checkpoint (§9). Inputs: docs/00, 05 §4, 08 §10, 09, 10, 11,
`params/*.yaml`, `src/elisa_sim/`, `scripts/`. This document changes no earlier document, parameter or code.

**Sourcing conventions.** Every number names its source: a repository section (`docs/09 §2.2 F8`), a parameter key
(`ma.capture.magnetic_trap_efficiency`), or a literature/vendor key already cited with its DOI/URL in docs/10 or
docs/11 (e.g. Wang2013 = doi:10.1039/c3an01166f, CS_1367). **Derived** = calculated here, arithmetic shown.
**[assessment]** = engineering judgement. **UNVERIFIED** = not traceable to a checked source. **Nearest-model
estimate** = output of the existing model run on an existing architecture with stated overrides; it is not a
prediction of the candidate, and the direction of every unrepresented chip effect is stated next to it.

## 0. Summary

Three genuinely different cartridges, one per renewal principle the surveys support or leave open:

* **A — multi-run bead-transfer cartridge** (one 8-h block, 16 determinations). One-step incubation in a 170 µL
  stirred on-card chamber; magnet collection, two rinses, magnet **drag of the bead pellet into a sealed 2 µL
  thin-layer readout chamber that never sees conjugate solution**; substrate pre-filled and **pre-electrolysed**;
  stopped accumulation 15 min; exhaustive single-WE read. Two staggered chambers, 27.5 min per sample, result 54.0
  min after Inject Start. 21 card valves.
* **B — indexed single-use cells** (16 per card, automatic changer). Fresh factory-made 0.5 µL streptavidin bed with
  pre-loaded capture antibody, dried conjugate and its own electrode per determination; recirculating capture,
  sequential labelling in flow, stopped exhaustive read. No regeneration, no residual beads; carry-over ≈ 0 by
  construction. Result 50.0 min; ≈ 26 min per sample with two dock heads.
* **C — permanent glass chip + daily reagent pack**. Regenerated 0.1 µL covalent anti-Fc bed (glycine pH 2), side
  outlet protecting a stopped-flow IDA channel, two potentiostat channels. Result 37.5 min; 45 min per sample.

**Nearest-model estimates** (existing architectures with overrides, n = 2000; §8), median / P(success):
gen-1 primary 3.5 / 0.16 → **A 2.3 / 0.20** (1.9 / 0.25 with pre-electrolysis), **B 2.3 / 0.15**, **C 2.4 / 0.16**.
After U1–U3 screening: gen-1 1.3 / 0.32 → **A 1.1 / 0.39**, B 1.8 / 0.20, C 1.9 / 0.20. **No candidate beats gen-1 by
a decision-grade margin as specified**; A gains modestly after screening because it keeps the one-step format. The
largest single lever found — removing the substrate's free hydroquinone by electrolysing the fill before accumulation
(turns the S4a kill scenario 19 → 1.9 pg/mL) — is a derivation (UNVERIFIED) and is **portable to gen-1**.

**Recommendation**: A (B as fallback; C not pursued), justified by automation, reagent use, throughput and per-run
carry-over monitoring rather than by LOD; no cartridge spend before G1a/G1, and the pre-electrolysis test first.
The decisions the user must take are listed in §9.

---

## 1. Why these three: the design space the surveys reveal

The surveys reduce the space to three questions, and the three candidates take **different answers to each**:

| Question | Evidence | A | B | C |
|---|---|---|---|---|
| How is the capture surface renewed (docs/00 "reusable or automatically renewed")? | Fresh surface per run is the pattern of every commercial high-sensitivity cartridge found (Gyrolab, Ella, Simoa, i-STAT, Minicare; docs/10 §9.2 item 1); on-chip regeneration has ≤ 51 cycles of evidence and none for a sandwich IgG assay (docs/10 §3.2) | **renewed by replacement, as a liquid**: magnetic beads dosed per run | **renewed by replacement, as a solid**: a factory-made fresh micro-bed + electrode cell per run, indexed automatically | **regenerated in place**: covalent capture bed, glycine pH 2 each run, permanent chip |
| Where does labelling happen and how is binding separated from signal? | Separating the binding compartment from the signal compartment and **moving beads, not liquid** is the best-evidenced low-background pattern (Herrmann2007, Rusling capture→detection chamber, Wang2013 bead drag with < 2×10⁻⁵ carry-over; docs/10 §1.2, §9.2 item 2) | one-step in a stirred chamber, beads **dragged by a magnet** into a clean readout chamber that never sees conjugate solution | sequential, in flow through the bed; side outlet keeps conjugate out of the readout chamber | sequential, in flow through the bed; side outlet keeps conjugate out of the IDA channel |
| Detector | IDA gain 4–65× only in stopped flow (Kamath 37 → 4 under flow; docs/10 §4.1); the blank is NSB-limited, EC noise ≈ 5 % of blank variance (docs/09 §4.1) | single thin-film WE, **stopped, exhaustive (coulometric) thin layer** | single thin-film WE per cell (one strip die per card), stopped, exhaustive | **IDA redox cycling, stopped** (Scheme C, second potentiostat channel) |
| Lifetime | multi-run cartridge defensible only with agitated beads and measured carry-over (docs/10 §9.4); membrane-valve endurance published at > 50 actuations (CHILDERS2024) | **multi-run cartridge, one 8-h block** | **single-use cells on a 16-cell card, automatic changer** | **permanent chip + daily swappable reagent pack** |

What the three deliberately do *not* vary, because the evidence or the user fixed it: ALP/HQDP chemistry and the
antibody pair of docs/05 §4.1 (the reagent gates U1–U3 apply to every candidate unchanged); Waters BSM + SM-FL
in front, Python orchestration (docs/00); full-loop 100 µL injection (docs/00).

---

## 2. Elements common to all three candidates

### 2.1 Interface to the Waters stack

* **Inlet**: SM-FL "to column" outlet → 1/16″ PEEK → dock-side flat-bottom compression seal onto a 1.4 mm
  through-hole port of the consumable (internal volume 0.6 µL, CS_EXPLAINED). Not a Mini Luer (16.5 µL,
  CS_EXPLAINED) anywhere in the sample or product path (docs/11 §1.2 assessment).
* **The BSM delivers only A1** (TBS + 0.05 % Tween-20, no phosphate; docs/09 §1.2) in all three candidates. HQDP
  substrate moves off the BSM into a cooled on-board (A) or dock/pack (B, C) store. Reasons: (i) no A1 → B1 line
  switch and its 90 µL dwell (`hw.bsm.delay_volume_to_injector_outlet`) inside a step table that stagger-schedules
  two samples; (ii) HQDP no longer stands > 24 h in BSM steel (docs/09 §1.2; E1.2 measures that exposure);
  (iii) §2.3 shows the storage penalty of on-board HQDP is removed by pre-electrolysis. B1 becomes spare.
* **BSM between transfers**: parked at its minimum flow to a dock-side bypass to waste (1 µL/min user figure,
  `hw.bsm.flow_min` override; 10 µL/min vendor figure) instead of gen-1's 3 mL shunt per run (docs/09 §2.2 F6).
  The pump back-pressure question at 1–10 µL/min (≥ 1000 psi recommended, `hw.bsm.min_backpressure_recommended`;
  one restrictor gives 12–120 psi, `hw.bsm.restrictor_dp_per_flow`) is an open gen-1 bench item (docs/08 §10) and
  is not changed by any candidate.
* **Timing**: Inject Start contact closure → Python cycle table, as gen-1 (docs/09 §1.3). Empower runs one
  isocratic A1 method with a timed flow programme per sample.

### 2.2 Sample reception: 1.5 loop volumes into a smaller volume (A and B)

The 100 µL plug arrives spread over 200–300 µL of A1 (docs/09 §1.2: 0.77 of the analyte out of the loop after
1 loop volume, 0.90 after 1.5, 0.96 after 2, 0.997 after 3; loop ID 0.5 mm, **UNVERIFIED**). In a stirred chamber
(A) and in recirculating capture (B) the captured fraction in the small-capture limit is ∝ (analyte delivered) ×
(capture rate ∝ 1/working volume). **Derived:** gen-1 pushes 2 loop volumes into ≈ 220 µL: 0.96/2.2 = 0.436; A
pushes 1.5 loop volumes into 170 µL (150 µL + 10 µL beads + 10 µL conjugate): 0.90/1.7 = 0.529, i.e. **×1.21**;
the remaining 10 % of the plug goes to the bypass. The model run "A0 dil 2.2, 2 LV" vs "A0 S0" (§8) confirms the
size (nominal LOD 0.47 → 0.41 pg/mL). A smaller fill (1 loop volume, 0.77) would gain little more (0.77/1.2 = 0.64,
×1.47) and makes the transfer depend on the loop ID, which is UNVERIFIED; 1.5 is chosen. C loads directly through
its bed (no chamber, 2 loop volumes at 10 µL/min, as the gen-1 backup, docs/05 §4.2).

### 2.3 Stopped, exhaustive thin-layer readout with substrate pre-electrolysis (A and B; C uses it with its IDA)

**Geometry.** The product is read in a sealed thin layer of height h = 50 µm whose floor is almost entirely
working electrode. **Derived:** diffusion time constant τ = 4h²/(π²D) with D_HQ = 9×10⁻¹⁰ m²/s
(`chem.substrates.HQ.diffusion_coefficient`, 7–11×10⁻¹⁰): τ = 4 × (50×10⁻⁶)² / (9.87 × 9×10⁻¹⁰) = **1.1 s**;
99 % conversion after 4.6 τ ≈ 5 s. A 30 s potential step at +0.35 V vs Ag/AgCl (docs/05 §4.1, DellaCiana1996 via
docs/08 §9 C3) therefore collects essentially all hydroquinone in the layer (chronocoulometry). Edge regions not
over the WE (≤ 0.1 mm wide) are reached by lateral diffusion in (0.1 mm)²/D ≈ 11 s (Derived). Conversion ≥ 0.95 is
my estimate, **UNVERIFIED** until measured (risk A5).

**Three consequences (Derived; none is represented in the model, docs/09 §5.4 item 3):**
1. *Charge = n F × moles of product*, independent of electrode area, layer height and flow. Electrode-to-electrode
   (cartridge-to-cartridge, cell-to-cell) area variation drops out of the specific signal; only the background
   charge (double-layer, oxide, impurities) still varies with area and is measured on the same fill (pre-read).
   Conversion itself does not move the LOD while the blank is NSB-limited: it multiplies the specific charge and the
   NSB charge alike (docs/09 §4.1: EC noise ≈ 5 % of the blank variance).
2. **Pre-electrolysis removes the free-HQ impurity before accumulation starts.** The readout chamber is filled with
   fresh substrate *before* the capture phase arrives and is electrolysed once (30 s at +0.35 V). The free HQ of the
   lot (`ma.chemistries.alp_hqdp.free_product_impurity` 10⁻⁵, 10⁻⁷–10⁻³, **UNVERIFIED**) is oxidised to BQ, which is
   not oxidised again at the read. At 1 mM HQDP and 10⁻⁵ impurity the fill holds 10 nM HQ, against ≈ 3.9 nM of
   enzyme product at 1 pg/mL (Derived for A: 5708 enzymes at 1 pg/mL from the nominal model run × 1000 s⁻¹
   (`chem.enzymes.alp.kcat_conjugate_assay_conditions`) × S/(K_m+S) = 0.91 (K_m 0.1 mM, `ma.chemistries.alp_hqdp.Km`,
   **UNVERIFIED**) × 900 s = 4.7×10⁹ HQ = 7.8×10⁻¹⁵ mol in 2 µL = 3.9 nM, i.e. 1.5 nC; ignoring Pi inhibition and
   product decay). Gen-1 subtracts this impurity via baseline windows (residual `ma.noise.background_current_relative_noise`
   1 %, `ma.noise.substrate_background_cv` 5 %); pre-electrolysis removes it instead. HQ re-formed by hydrolysis during
   a 15-min accumulation is 10⁻¹⁰ s⁻¹ × 900 s = 9×10⁻⁸ mol/mol (`ma.chemistries.alp_hqdp.hydrolysis_rate`), ≈ 1 % of
   the nominal impurity. **Assumption** (UNVERIFIED): 1 % of the fill volume (ports, valve seats) escapes
   electrolysis, so the impurity is represented in the model as ×0.01 (value 10⁻⁷, bounds 10⁻⁹–10⁻⁵). This turns
   scenario S4a (free HQ 10⁻³, which kills every gen-1 design, docs/05 §3) into the nominal 10⁻⁵ case.
3. **On-board liquid HQDP becomes tolerable.** docs/09 §3.3 showed that at k_h = 10⁻⁹ s⁻¹ one day of storage makes
   ≈ 9× the free-HQ acceptance limit. Pre-electrolysis removes that HQ every run. What remains is the **phosphate**
   released by hydrolysis (2 Pi per HQDP, `ma.chemistries.alp_hqdp.phosphate_per_product`), which is not removed.
   **Derived:** Pi growth = 2 × k_h × t × S₀ = 2 × 10⁻⁹ × 86 400 s × 1 mM = 0.17 µM per day at the acceptance-limit
   k_h; against the ≤ 1 µM residual-Pi target (docs/09 §3.4) that allows ≈ 5.8 days at 1 mM (1.9 days at 3 mM); at the
   nominal 10⁻¹⁰ s⁻¹, ≈ 58 days. Cooling slows both (no temperature coefficient exists in the repository, docs/09 §5.4
   item 11). An 8-h liquid store is therefore safe by a factor of > 15 on Pi even at the acceptance limit.

**Why a single WE and not an IDA for A and B.** The IDA multiplies product current, i.e. specific *and* NSB
charge; it helps only where EC noise or drift matters (docs/08 S9: +0.02–0.05 in P as specified). Exhaustive
coulometry already collects all product, needs one potentiostat channel, has no collector potential marginal
against O₂ reduction (docs/08 W6), and tolerates electrode-area variation (point 1). C keeps the IDA to span the
detector choice and because a permanent chip amortises the lithographic die.

### 2.4 Electrodes, reference and electrical isolation

* **Electrode die**: thin-film Au or Pt (150 nm on 50 nm Ti) on glass, from a thin-film foundry: Micrux custom
  (≥ 5 µm features, Au/Pt, SU-8/polyimide passivation; MICRUX_TF) or IMT (≥ 2 µm, Au/Pt/ITO/Ti; IMT_FLYER). Bonded
  or gasketed into a pocket of the polymer body (docs/11 §1.6).
* **Reference**: the readout chamber holds only substrate during pre-read and read, so a thin-film Ag/AgCl pad sees a
  constant chloride activity if the substrate recipe fixes Cl⁻ (Nernst ≈ 59 mV/decade; docs/11 §6.4). Ag/AgCl pads
  are not in the Micrux custom offer (Au/Pt only, MICRUX_TF): availability **UNVERIFIED**; fall-back is an Au
  quasi-reference checked against a docked salt-bridge Ag/AgCl at each cartridge start (docs/02 §5.2 gen-1 approach).
  Best on-chip Ag/AgCl drift found: < 2 mV over 26 days, GO-coated, constant medium (Kim2015, doi:10.3390/s150306469).
* **Electrical isolation (F20)**: during the read the readout chamber is closed by valves (A, C) or dock pinch points
  (B); the solution path to the earthed Waters stack is then broken at the closed valve, not merely lengthened. Seat
  leakage resistance of a closed membrane valve is **UNVERIFIED** (bench item, part of each candidate's EC noise
  test). PEEK ≥ 0.3 m each side of the cartridge stays as in gen-1 (`hw.tubing.peek_isolation_length_each_side_of_cell`).
* **Contacts**: gold spring pins on die pads outside the wetted area, shielded traces, Faraday cage around the dock
  electrode zone (docs/11 §5.4, assessment; part numbers UNVERIFIED).

### 2.5 Dock (common hardware)

Peltier zones (reagent zone 4–8 °C; assay zone 25.0 ± 0.2 °C, docs/07 §5.1 spec for the cup) with thermistors, the
tank/chamber wall on the thin foil side (docs/11 §4); syringe pump(s) of the Cavro Centris / Hamilton PSD/4 class
(serial ASCII, ≈ 10 nL/step on a 250 µL syringe, docs/11 §5.2); a regulated pressure source with solenoid manifold
for valve actuation and headspace drives (Fluigent Flow EZ / Elveflow OB1 class, Python SDKs; docs/11 §5.1);
low-flow sensor on the readout-side path (Sensirion LG16 class, docs/11 §5.3); a dock A1 bottle for the syringe
pump's working fluid; waste bottle. Fail-safe states are listed per candidate (F16).

---

## 3. Candidate A — multi-run bead-transfer cartridge ("move beads, not liquid")

### 3.1 Concept

One-step capture and labelling in a small stirred on-card chamber (beads and conjugate from separate on-card stores,
metered volumetrically); after the timed incubation a magnet collects the beads, the chamber is rinsed, and a
magnet carriage **drags the bead pellet through a buffer-filled wash lane into a sealed 2 µL thin-layer readout
chamber that never sees conjugate solution**; the readout chamber was filled with substrate and pre-electrolysed
before the beads arrive; accumulation is stopped-flow at open circuit, and the product is read in place by one
potential step (exhaustive coulometry, §2.3). Two incubation chambers share one readout chamber and are staggered.
One cartridge serves one 8-h block (16 determinations). Precedent for each element: stirred capture chamber with
magnetic transfer to a detection chamber (Rusling: Otieno2014, doi:10.1016/j.bios.2013.09.054); bead drag between
wells, > 95 % in 2 min, substrate carry-over < 2×10⁻⁵ (Wang2013, doi:10.1039/c3an01166f); two compartments joined
by valved bridges, beads moved by magnet (Herrmann2007, doi:10.1039/b707883h).

### 3.2 Block diagram

```
 CONSUMABLE (COC body ~6 mm, 100-140 um COC foil = BOTTOM face, glass WE die in a top pocket)        DOCK
 ======================================================================================================================
 SM-FL --PEEK 0.3 m--[face seal]--> P_in (through-hole, 0.6 uL)
                                      |--[V1]--> IC1  incubation chamber 170 uL work / 250 uL total, vented (PTFE)
                                      |--[V2]--> IC2  (identical, staggered by 27.5 min)
                                      '--[V3]--> P_byp --------------------------------------------> dock waste
 RB  bead tank 0.5 mL  (4-8 C) --[V8]--> MB bead meter 10.0 uL --[V9]--+--[V4]--> IC1   <- tidal resuspension RB<->side
                                                                       '--[V6]--> IC2      reservoir, dock pressure ch.1
 RCj conjugate tank 0.5 mL (4-8 C, dark) --[V10]--> MC meter 10.0 uL --[V11]--+--[V5]--> IC1
                                                                              '--[V7]--> IC2   (separate ports: F5)
 IC1 floor --[V12]-- tidal serpentine 60 uL --> P_d1 <====> dock pressure ch.2 / syringe S2 (mix, drain, rinse A1)
 IC2 floor --[V13]-- tidal serpentine 60 uL --> P_d2 <====> dock pressure ch.3 / S2
 IC1 throat ==[G1]==.                                                                     M1a/M1b: collection magnets
                     >== WL wash lane 0.5 x 0.2 x 20 mm (A1, 2 uL) ==[G3]==> RC ==[G4]==> bead-waste pocket (16 doses)
 IC2 throat ==[G2]=='     WL refresh: S2 --[V14]--> WL --[V15]--> waste       |                 under the foil
                                                                                |  M2: magnet carriage under the foil,
 RS  HQDP tank 2.0 mL (4-8 C, dark) --[V16]--> RC (4 x 10 mm x 50 um = 2 uL) --[V17]--> waste     IC throat -> RC -> pocket
                                      RC ceiling = glass die: WE 3.8 x 9.8 mm (Au/Pt thin film)
                                      side channel 2 mm x 0.1 x 0.05 mm --> CE + Ag/AgCl (or Au QRE) pads
 Pogo pins: WE, CE, RE -> Gamry Reference 600+ (one channel).  Peltier: reagent zone 4-8 C, assay zone 25.0 C.
 ====  magnet path (beads move, liquid does not)      [Vn] normally-open membrane valve, closed by a spring plunger in
                                                      the dock (fail-closed);  [Gn] gate valve on the magnet path
```

### 3.3 First-pass geometry

| Element | Dimension | Reasoning / source |
|---|---|---|
| Incubation chamber IC1, IC2 | Ø 8.0 mm × 5.0 mm deep = 251 µL total; working 170 µL (fill height 3.4 mm); flat foil floor; vented through a hydrophobic PTFE membrane in the lid | 150 µL sample transfer (1.5 loop volumes, §2.2) + 10 µL beads + 10 µL conjugate; headroom for tidal mixing; vent required when filled while closed (docs/09 F1). Wetted area Derived: floor 50.3 mm² + wall π × 8 × 3.4 = 85 mm² → **≈ 135 mm²** |
| Tidal mixing serpentine (per IC) | 0.8 × 0.5 mm × 150 mm = 60 µL | 50 µL aspirate/dispense every 30 s (gen-1 does 50 µL every 2 min, docs/09 F2) stays on the card, so beads never reach dock lines [assessment] |
| Bead meter MB, conjugate meter MC | 10.0 µL each (e.g. 2.0 × 1.0 × 5.0 mm), between two valves, emptied by air into the vented IC | volumetric metering from geometry, not pump steps; separate meters and IC ports (docs/09 F4, F5). Dose CV ≤ 5 % is a requirement (docs/09 F3), **UNVERIFIED** for this meter |
| Tanks RB, RCj, RS | 0.5 / 0.5 / 2.0 mL, 5 mm deep (footprint ≈ 100 / 100 / 400 mm²) on the foil side over the 4–8 °C Peltier | sizing §3.6; footprint as docs/11 §4 (2 × 0.5 mL ≈ 2 × 100 mm²) |
| Bead resuspension | pressure-driven tidal flow between RB and a 150 µL side reservoir, 3 strokes before each dose | 2.8 µm beads settle ≈ 7 mm/h (`ma.capture.in_vial_unstirred_rate_factor` note), a 5 mm tank clears in < 1 h (docs/11 §4); no stir bar, which would collect paramagnetic beads [assessment] |
| Wash lane WL | 0.5 mm wide × 0.2 mm deep × 20 mm = 2.0 µL, foil floor | path for the drag; refreshed with 10 µL A1 every run |
| Readout chamber RC | 4.0 × 10.0 mm × 50 µm = **2.0 µL** | V_acc kept at the gen-1 trap volume (`ma.geometry.magnetic_trap_volume` 2 µL): smaller barely helps the LOD and costs ULOQ (docs/09 §5.3: 0.5 µL → ULOQ 1360 pg/mL); h = 50 µm gives τ = 1.1 s (§2.3); bead pellet 5×10⁵ × 11.5 µm³ = **5.7 nL** (Derived) in a 1 × 1 mm pocket at the downstream end |
| Working electrode | Au or Pt thin film 3.8 × 9.8 mm = 37 mm² (93 % of the floor) on glass | exhaustive read (§2.3); Micrux custom/IMT rules (MICRUX_TF, IMT_FLYER) |
| CE and RE | pads at the end of a 2 mm × 0.1 mm × 0.05 mm side channel off the RC | keeps BQ reduced at the CE from cycling back to the WE during the 30 s read: diffusion time (2 mm)²/D = 4.4×10³ s (Derived); iR drop Derived: R = 2 mm / (1.6 S/m × 5×10⁻⁹ m²) = 250 kΩ (κ from `hw.tubing.buffer_conductivity`, **UNVERIFIED**) × ≈ 2 nA = 0.5 mV |
| Magnet-side wall | COC foil 100 µm (Topas, CS_1367) to 140 µm (DARWIN_CS4CH) | requirement ≤ 0.5 mm (docs/09 F8); beads sit on the foil, 50 µm below the WE face, so the WE never touches beads |
| Inlet / outlets | 1.4 mm through-holes with dock face seals (0.6 µL); factory-fill ports Mini-Luer, capped | CS_EXPLAINED internal volumes; docs/11 §1.2 assessment |
| Card | ≈ 75 × 50 mm (double-slide footprint, CS_EXPLAINED) × ≈ 6 mm moulded body | IC depth 5 mm needs ≥ 6 mm body ("≥ 3–5 mm" docs/11 §0); thickness outside the catalogue (2 mm) → custom mould [assessment] |

### 3.4 Per-cycle step table (one sample in IC1; t = 0 at Inject Start)

Valves not listed are closed. BSM = A1 only. "S2" = dock syringe (A1 working fluid); "pc" = dock pressure channel.

| t (min) | Step | Flow / volume | Open valves | Magnets | Potentiostat |
|---|---|---|---|---|---|
| −4.0 → −2.0 | Bead tank resuspension (3 tidal strokes, pc1), meter 10 µL beads, air-push into IC1 | ≈ 150 µL strokes; 10 µL dose | V8 → V9, V4 | – | – |
| −2.0 → −1.0 | Meter 10 µL conjugate (5.1 nM → 0.3 nM in 170 µL), air-push into IC1 | 10 µL | V10 → V11, V5 | – | – |
| −1.0 → 0 | SM-FL aspirates ≈ 200 µL (full loop, 2× overfill; Empower) | BSM 1 µL/min → bypass | V3 | – | – |
| 0 → 1.5 | **Inject Start**; 150 µL A1 carries the plug into IC1 (transfer 0.90) | BSM 100 µL/min, 150 µL | V1 | – | – |
| 1.5 → 31.5 | **Incubation 30 min**, 25.0 °C, tidal mixing 50 µL every 30 s | BSM 1 µL/min → bypass; pc2 tidal | V3, V12 | – | – |
| 29.5 → 30.5 | RC prep (RC empty of the previous run's beads): HQDP from RS through RC | 40 µL at 40 µL/min (20 RC volumes) | V16, V17 | – | – |
| 30.5 → 31.0 | **Pre-electrolysis PE1** (removes free HQ; records background charge) | sealed | – | – | +0.35 V, 30 s |
| 31.5 → 33.5 | Bead collection at the IC1 throat | – | V3 | M1a on | – |
| 33.5 → 36.5 | Drain IC1; 2 rinses (100 µL A1 in, mix, out) — free conjugate ×440 lower (Derived §3.8) | S2 ≈ 100 µL/min | V12 | M1a on | – |
| 35.5 → 36.0 | **PE2 residual-activity read**: product made by anything left in RC during the 4.5 min since PE1 (carry-over monitor, §3.8) | sealed | – | – | +0.35 V, 30 s |
| 36.0 → 36.5 | WL refresh | 10 µL A1 | V14, V15 | M1a on | – |
| 36.5 → 38.5 | **Drag**: M2 takes the pellet from M1a and moves 20 mm at 0.25 mm/s through WL into the RC pocket; gates close | no flow | G1, G3 | M1a off, M2 | – |
| 38.5 → 53.5 | **Accumulation 15 min**, RC sealed, open circuit. In parallel: IC1 cleaned (magnet off, 3 × 100 µL A1 with tidal mixing → waste) | S2 for IC1 | V12 (IC1 side only) | M2 holds | OCP |
| 53.5 → 54.0 | **Readout**: potential step, 30 s chronocoulometry; Q_net = Q − Q(PE background) | sealed | – | M2 | +0.35 V |
| **54.0** | **Result** (55.0 min from aspiration start) | | | | |
| 54.0 → 55.5 | Beads dragged into the bead-waste pocket; RC flushed with 40 µL HQDP and left filled | 40 µL | G4, then V16, V17 | M2 | – |

Time budget vs gen-1 (docs/09 §2.3): transfer 1.5 (gen-1 2.0) + incubation 30 + collect/rinse/drag 7.0 (gen-1
trap loading + wash 7.6) + substrate fill 0 (done in parallel; gen-1 1.0) + accumulation **15** (gen-1 10) + read 0.5
(gen-1 1.5 incl. post-baseline) = 54.0 min. The 5 extra accumulation minutes are the parallel substrate fill and the
short exhaustive read. **Staggering**: IC2's sample is injected at t = 27.5; its RC prep (its t = 29.5 = 57.0 here)
starts after RC release at 55.5. Cadence **27.5 min per sample** (≈ 2.2 /h; 16 samples in 7.3 h). Every sample gets
an identical 30-min incubation from its own Inject Start (C4). The BSM method is identical for every Empower line:
100 µL/min for 1.5 min, then 1 µL/min to the bypass; all rinses use the dock syringe, so overlapping lines never
compete for the BSM.

### 3.5 Requirements F1–F20 (docs/09 §2.2)

| # | How A meets it | Status |
|---|---|---|
| F1 | 150 µL at 100 µL/min into a vented 170 µL chamber; 0.90 transfer, 10 % tail to bypass; net capture gain ×1.21 vs gen-1 (§2.2). Sample-contact area ≈ 135 mm² blocked COC (adsorption at fM **UNVERIFIED**) | met by design; adsorption open |
| F2 | timed from Inject Start, identical for all samples; tidal mixing 4× more often than gen-1; thermostatted | mixing factor UNVERIFIED (E3.3 analogue, risk A2) |
| F3 | on-card tank + volumetric meter, tidal resuspension before each dose | CV ≤ 5 % UNVERIFIED (risk A3) |
| F4, F5 | separate tank, meter, channel and chamber port; beads and conjugate meet only in IC at the start of the timed incubation | met |
| F6 | on-card V1/V2/V3; BSM parked at 1 µL/min to bypass (≈ 30 µL per run instead of 3 mL) | met |
| F7 | magnet collection + drag; **no flow through the capture zone during transfer**; efficiency ≈ 0.95 (collection, UNVERIFIED) × 0.95 (Wang2013) = 0.90 (model uses 0.96 × 0.9 = 0.86) | partly (risk A1) |
| F8 | the RC pocket replaces the trap: beads held statically on the foil (no loading flow, so the Zaini 2021 flow limit does not apply); release by drag to the pocket | met by design; bench check |
| F9 | RC sealed by G3, G4, V16, V17 **before** accumulation; no valve moves while product exists | met |
| F10 | 2 chamber rinses (×440 dilution of free conjugate, Derived) + transfer through a fresh wash lane; carried-in conjugate ≈ 42 enzymes vs ≈ 5700 NSB enzymes at blank (§3.8) | met by derivation; wash-efficiency not modelled (C11) |
| F11 | RC filled from the on-card HQDP tank; RC never contains A1 (only nL entrained with the pellet) — removes the A1 → B1 switch question (docs/08 W4) | met |
| F12 | 15 min accumulation in 2 µL; exhaustive 30 s read; pre-read on the same fill as baseline | met by design; conversion UNVERIFIED (risk A5) |
| F13 | electrode sees substrate and product only; beads 50 µm away on the foil; no protein solution, no low pH | met |
| F14 | beads to an on-card pocket (no bead slurry through valves); IC 3 rinses; RC flush | partly: residual ≤ 10⁻⁴ UNVERIFIED (risk A1) |
| F15 | paths in §3.8; **every run measures residual activity in RC (PE2)** | open (bench) |
| F16 | dock plungers spring-closed (fail-closed valves), magnets spring-on, cell off, Peltier off → latch flags the cartridge if the reagent zone exceeds 10 °C [assessment] | met by dock design |
| F17 | recovery: magnets off → beads to pocket, RC flush 40 µL, IC 3 rinses, WL refresh (≈ 4 min); 2 recovery reserves in the sizing | met |
| F18 | 2 blanks + 1 mid control per 16-run cartridge (≈ F18's 2 per 10) | met |
| F19 | assay zone 25.0 ± 0.2 °C, reagent zone 4–8 °C | met (model has no T) |
| F20 | RC galvanically isolated by closed valves during the read; leakage resistance UNVERIFIED | partly |

### 3.6 Reagent strategy, batch size and lifetime

| Store | Content | Per run | Per cartridge (16 runs + 2 priming + 2 recovery = 20 doses) + dead volume | Storage |
|---|---|---|---|---|
| RB | M-280 SA beads 5×10⁷/mL with biotin-cAb, TBS + 1 % IgG-free BSA + 0.05 % Tween (docs/07 §5.5) | 10 µL (5×10⁵ beads) | 200 µL + 100 µL dead (UNVERIFIED) = **0.3 mL** (1.5×10⁷ beads = 230 µg at 6.5×10¹⁰/g, `chem.surfaces.magnetic_bead_M280_count_per_mass`) | liquid, 4–8 °C, resuspended before each dose |
| RCj | ALP-F(ab′)₂ conjugate 5.1 nM in TBS + 1 % IgG-free BSA, no azide, no phosphate | 10 µL | 200 + 100 = **0.3 mL** | liquid, 4–8 °C, dark, unstirred; never with beads (C7) |
| RS | HQDP 1 mM (3 mM option) in 0.1 M Tris pH 9.5, 1 mM MgCl₂, fixed Cl⁻ | 40 µL fill + 40 µL flush | 20 × 80 µL = 1.6 mL + dead volume → **2.0 mL** tank (dead volume UNVERIFIED) | liquid, 4–8 °C, dark; pre-electrolysed per run (§2.3) |
| BSM A1 | TBS + Tween | 150 µL + 30 µL bypass | – | Waters bottle |
| Dock S2 A1 | same | ≈ 600 µL (rinses, cleaning, WL) | – | dock bottle |

A1 per determination ≈ 0.8 mL against gen-1 ≈ 4.3 mL (docs/09 §3.4); substrate ≈ 80 µL against ≈ 315 µL.

**Lifetime: multi-run cartridge for one 8-h block (16 determinations).** Reasons: (i) the conjugate store's default
life is 8 h until the E1.3 conjugate-only ageing arm says otherwise (docs/07 §5.5); (ii) no quantitative data
exist for on-board liquid bead suspensions (docs/10 §9.3), and 8 h is the E2.2 dose-CV horizon; (iii) the busiest
valve then sees ≈ 70 actuations, just above the only thermoplastic-membrane endurance figure (> 50, CHILDERS2024),
whereas a week-long cartridge needs ~10³ (docs/11 §3); (iv) wall build-up in the chambers is reset daily. Extension
to 2–3 days is a later decision gated by E1.3 (conjugate ageing at 4 °C) and on-card dose CV over time.
**Calibration**: exhaustive coulometry removes electrode-area variation (§2.3), so a lot calibration (bead and
conjugate lot) plus the per-cartridge blanks and control carry the calibration; this is an assumption to be
tested (risk A5), not a repository value (docs/09 §6 Q9).

### 3.7 Valves and actuations

21 valves (17 membrane valves V1–V17 + 4 gates G1–G4); 16 if one incubation chamber. Per run (Derived from §3.4):
1 actuation for most valves, 2 for V8 and V16/V17, up to 7 for the tidal/drain valves V12/V13. Per cartridge life
(20 runs; per-chamber valves see 10): busiest valve ≈ 70, shared valves 20–40, **≈ 520 actuations in total**.
Evidence: thermoplastic (eCOC) membrane valves > 50 actuations without failure (CHILDERS2024); ChipShop's
mechanically closed membrane-valve chip is sold as single use, tight to 3 bar (CS_1367); ≥ 10⁶ only for PDMS and
clean liquids, secondary source (docs/10 §7). **The busiest valve needs ≈ 1.4× the published thermoplastic figure —
bench gate at 3× life (≈ 210 cycles) with bead and protein media** (risk A4). Gates G1–G4 must pass beads in a
magnetic field, not in flow (Herrmann2007 pattern); their seat must not trap beads (UNVERIFIED).

### 3.8 NSB surface budget and carry-over paths

**NSB budget** (conjugate exposure in the zones that end up in the product path):

| Surface | Area | In product path? | Conjugate exposure | Source |
|---|---|---|---|---|
| Beads (5×10⁵ × π d², d = 2.8 µm) | **12.3 mm²** (Derived), factor 1 (`ma.nsb.surface_factor_magnetic_beads`) | yes | 0.3 nM × ≈ 37 min ≈ 11 nM·min (one-step, docs/09 §4.1) | model "A0": 10.9 mm² after transfer losses |
| RC walls + WE | 2 × 40 mm² = 80 mm² | yes | carried-in free conjugate ≈ 42 molecules total (below) → effectively 0 | Derived |
| Wash lane | 2 × (0.5 + 0.2) × 20 = 28 mm² | no (refreshed; beads pass) | entrained liquid only | Derived |
| IC walls | ≈ 135 mm², chip factor 10 (`ma.nsb.surface_factor_chip`, 1–100) | **no** | 0.3 nM × 30 min | Derived; enters only carry-over and analyte loss |

Model effective NSB area: gen-1 primary 38.9 mm² (beads 92 % of the NSB product), A 11.0 mm² (beads ≈ 100 %).
Because gen-1's beads already carry 92 %, removing the wall share gains little (nominal LOD 0.43 → 0.41, §8); it
matters in the high-wall-factor scenario S3b (P 0.15 without the clean zone).

**Free conjugate carried into RC (Derived):** IC drained to ≤ 5 µL residual (assumption; gen-1 cup spec ≤ 2 µL,
docs/07 §5.1) and rinsed twice with 100 µL: dilution (105/5)² = 441 → 0.3 nM/441 = 0.7 pM; content left in IC
0.7 pM × 5 µL = 3.5×10⁻¹⁸ mol = 2.1×10⁶ molecules; drag carry-over < 2×10⁻⁵ (Wang2013, small molecule; protein
UNVERIFIED) → **≤ 42 conjugate molecules** against ≈ 5700 NSB enzymes in the nominal blank (model "A0"). Without the
rinses it would be ≈ 1.8×10⁴, three blanks' worth: the rinses are essential.

**Carry-over paths vs the 1×10⁻⁴ criterion** (10 ng/mL challenge read through the low-range slope, docs/08 S6):

| Path | Mechanism | Estimate | Control |
|---|---|---|---|
| SM-FL needle/loop | outside the cartridge | `hw.smfl.carryover_protein_conjugate` 10⁻⁴ (10⁻⁵–10⁻³, UNVERIFIED) | needle wash (gen-1) |
| Inlet manifold, V1/V2 seats | sample film | not quantified (no protein carry-over data for reusable channels, docs/10 §8) | 1.5 min of A1 behind every plug + IC rinses |
| Beads left in IC (≤ 5 % not collected/dragged, Wang2013) | carry the previous sandwich into the next incubation | 0.05 × (1/21)³ = **5×10⁻⁶** after 3 cleaning rinses if beads do not stick (Derived) | 3 rinses with tidal mixing, magnet off |
| Beads left in RC after drag-out | produce product in the next accumulation | unknown; gen-1 U5 accepts 10⁻³, which is **10× too loose** (docs/09 F15) | drag-out + 40 µL flush; **PE2 measures it every run** |
| Wall-adsorbed analyte/conjugate in IC | desorbs into the next incubation | unknown | daily cartridge; cleaning cycle after any sample > 100 pg/mL (docs/08 S6 alternative) |

**PE2 sensitivity (Derived):** at 10 ng/mL the specific signal is ≈ 10⁴ × 5700 = 5.7×10⁷ enzymes (linear
extrapolation, an upper estimate); 10⁻⁴ of that is 5700 enzymes, which in the 4.5-min PE2 hold make 5700 × 910 s⁻¹ ×
270 s = 1.4×10⁹ HQ = 0.45 nC — about one third of the 1 pg/mL read (1.5 nC in 15 min), i.e. measurable. So every
run checks its own readout chamber at the 10⁻⁴ level.

### 3.9 First-order performance (nearest-model estimates)

Nearest architecture: gen-1 primary P-chamb (`final_designs.designs()`, review variant: one-step chamber
approximation, thin-layer cell) with design overrides, run in a scratch copy (§8). n = 2000, seed 20261111; ±0.02 in
P; ΔP < 0.05 is not decision-grade (docs/08 W7).

| Run (nearest-model estimate) | Nominal LOD | Median [5–95 %] (pg/mL) | P(success) | ULOQ nominal | Model time (min) |
|---|---|---|---|---|---|
| gen-1 primary P-chamb, as specified | 0.60 | 3.5 [0.51–157] | 0.16 | 5200 | 56.1 |
| **A0** as specified (dilution 1.7, transfer 0.90, acc 15 min, clean RC) | 0.41 | **2.3 [0.43–73]** | **0.20** | 2300 | 57.6 |
| A0 with gen-1 dilution (2.2) and 2 loop volumes | 0.47 | 2.7 [0.46–86] | 0.18 | 3000 | 57.6 |
| A0 with 10 min accumulation | 0.43 | 2.6 [0.46–86] | 0.19 | 4000 | 52.6 |
| A0 without the clean readout zone (trap-wall factor as tubing) | 0.43 | 2.5 [0.45–79] | 0.19 | 2300 | 57.6 |
| **A1** = A0 + pre-electrolysis (free HQ ×0.01) | 0.40 | **1.9 [0.38–54]** | **0.25** | 2300 | 57.6 |
| A1 at 3 mM HQDP | 0.40 | 1.9 [0.38–57] | 0.26 | 6800 | 57.6 |
| gen-1 primary after U1–U3 screening (L6 + L7) | 0.19 | 1.3 [0.34–9.3] | 0.32 | 1800 | 56.1 |
| A0 + L6 + L7 | 0.15 | 1.1 [0.29–7] | 0.36 (ULOQ 794 flagged) | 794 | 57.6 |
| **A1 + L6 + L7, 3 mM HQDP** | 0.15 | **1.1 [0.29–7]** | **0.39** | 2300 | 57.6 |
| A0 under S4a (free HQ 10⁻³) | 8.3 | 19 | 0.00 | 2300 | 57.6 |
| A1 under S4a (pre-electrolysis → 10⁻⁵) | 0.41 | 1.9 [0.39–50] | 0.22 | 2300 | 57.6 |
| A0 under S3b without clean zone (wall factor 30) | 0.67 | 3.2 | 0.15 | 2300 | 57.6 |
| A0 under C1 (contamination up to 1 pg/mL-eq.) | 0.41 | 2.8 | 0.10 | 2300 | 57.6 |
| A1 + L4 immune-complex transfer, 3 mM (lever outside the model, unmeasured) | 0.12 | 0.91 [0.19–15] | 0.53 | 6800 | 57.6 |

Model time 57.6 min includes a 1-min overhead block and 2 min of RC cleaning after the result; the step table gives
54.0 min from Inject Start.

**Where A's gain comes from:** ×1.21 from less dilution (§2.2), ≈ ×1.1 from 15 instead of 10 min accumulation,
≈ ×1.05 from the clean readout zone, and — the largest and least certain — the pre-electrolysis credit, which also
removes the S4a kill scenario. Only the first three are chip-specific; **pre-electrolysis is portable to gen-1** as a
flow-through coulometric guard cell on the substrate line (§10).

**Chip effects the model cannot represent (docs/09 §5.4) and their direction:**

| Effect | §5.4 item | Direction for A |
|---|---|---|
| Real chamber: mixing factor, dilution computed, chamber-wall analyte adsorption | 1 | mixing: either way (sampled 0.2–1.0/1.7); wall adsorption: **worse** |
| Beads read in a chip pocket; drag efficiency 0.90 vs model's 0.86 | 2 | slightly **better** (×1.04) |
| Exhaustive single-WE stopped read: conversion ≈ 1 (model 0.78 × 0.99) but WE 37 mm² vs 7 mm² → EC noise ×(37/7)^0.5 = 2.3 (`ma.noise.area_exponent` 0.5) | 3 | conversion neutral (NSB-limited); noise **slightly worse** (EC noise 3 % of the blank variance in "A0") |
| On-board conjugate dosing (not through the loop) | 4 | neutral (one-step: conjugate never passed the loop in the model either) |
| Decoupled flows / zone-resolved NSB | 5, 6 | neutral to **better** (walls outside the product path, already approximated) |
| On-board storage: conjugate and bead ageing over 8 h, HQDP Pi growth (≤ 0.06 µM in 8 h at the acceptance-limit k_h, §2.3) | 7 | **worse**, size unknown (E1.3) |
| Residual beads as carry-over; within-cartridge drift | 8 | **worse** if residual > 10⁻⁴; monitored by PE2 |
| Cartridge-to-cartridge electrode variation | 9 | mostly cancelled by exhaustive coulometry (**better** than a flow cell would be) |
| Temperature control | 11 | **better** (lower NSB CV), not quantifiable |

### 3.10 Fabrication route (docs/11 §7.2)

Prototype: CNC-milled COC body (ChipShop milling, CS_FAB) or laser-cut PMMA laminate for the first bead-drag and
mixing studies (docs/11 §1.3); 100 µm Topas foil lid (CS_1367); catalogue Micrux glass die for first electrochemistry
(single thin-film electrodes, DI_MICRUX_SINGLE, geometry UNVERIFIED), then a custom 4 × 10 mm WE die (Micrux custom
or IMT); mechanically actuated membrane valves on the CS_1367 principle with dock plungers; 50 µm laser-cut spacer
around the die. PDMS only for bead-drag visualisation, never for electrochemistry (docs/11 §1.4). Production:
injection-moulded COC/COP (MOQ 100, CS_FAB), die bonded into a pocket, factory fill of the three tanks under
human-IgG-clean conditions (C21) and foil-sealed.

### 3.11 Top 5 risks and the experiment that retires each

| # | Risk | Retiring bench experiment |
|---|---|---|
| A1 | Residual beads in IC or RC > 10⁻⁴ of the dose (carry-over), or drag efficiency < 0.9 | PMMA/COC mock-up with fluorescent or counted M-280 beads: collection + drag efficiency (n = 20), residual after drag-out and flush; then the 10 ng/mL challenge → blank series read by PE2 (U5 analogue at 10⁻⁴, docs/06 E2.7 criterion) |
| A2 | Chamber mixing gives a capture factor near the 0.2 lower bound | E3.3 analogue on the 170 µL foil-floor chamber: capture vs time with tidal mixing every 30 s vs well-mixed tube reference |
| A3 | On-card bead dose CV > 5 % over 8 h (settling, meter fill) | 8-h dosing series from the on-card tank with tidal resuspension, bead count per dose (E2.2 analogue) |
| A4 | Membrane valve or gate fails, leaks or traps beads within ≈ 70 (busiest) actuations | endurance rig: 210 cycles per valve with bead suspension and 1 % BSA buffer; leak test at 3 bar (CS_1367 rating); bead count at seats |
| A5 | Exhaustive read and pre-electrolysis do not behave as derived (conversion < 0.95, background-charge SD too large, BQ/Pi effects, free HQ not removed to ≤ 1 %) | on the Micrux die in a 50 µm gasket cell: HQ standards 1–100 nM (conversion, background SD over 20 fills), HQDP lots spiked with 10⁻⁴–10⁻³ HQ before/after pre-electrolysis; same measurement on 5 dies (area-independence) |

Project-wide gates (U1 conjugate NSB on beads, U3 free HQ, E1.5 on-bead t½) apply to A unchanged and are not
repeated here.

---

## 4. Candidate B — indexed single-use capture-and-read cells (fresh micro-bed + own electrode per determination)

### 4.1 Concept

A card carries 16 identical, foil-sealed, **single-use cells**. Each cell holds a factory-packed 0.5 µL bed of
streptavidin particles pre-loaded with biotinylated capture antibody and dried, a dried conjugate spot, and its own
2 µL thin-layer readout chamber over one working electrode of a shared glass electrode strip. The cell has **no
moving parts except dock-actuated pinch points on its foil**: a dock head (face-seal ports + pogo pins on an x–y stage)
engages one cell at a time, receives the SM-FL plug into the cell's well, shuttles it back and forth through the bed by
headspace pressure (recirculating capture), labels in flow, accumulates stopped and reads exhaustively. After the
result the head lifts and indexes to the next cell: **renewal by replacement of the whole capture-and-read element**,
no regeneration, no residual beads, no cleaning. This is the Gyrolab/Ella pattern (fresh nL bed or nano-reactor per
assay; Honda2005, doi:10.1373/clinchem.2005.053348; Aldo2016, doi:10.1111/aji.12512) combined with the i-STAT pattern
(dried ALP conjugate on a single-use amperometric cartridge; FDA K031739/K240984 via docs/10 §6.2).

### 4.2 Block diagram (one cell; 16 per card)

```
 DOCK HEAD (x-y stage, 2 heads for staggering)                       CELL k (COC/COP card, foil-sealed, single use)
 ===============================================================================================================
 SM-FL --PEEK--[dock 2-pos selector: head 1 / head 2]--> port a -----> W1 reception well 150 uL work / 250 uL total
 pressure ch. A (shuttle, vent)  ----------------------> port a'        |
                                                                        [P0] bed inlet manifold <-- W3 dried conjugate
 A1 (dock syringe) -------------------------------------> port c -----> W3 (50 uL) --capillary stop--'    (20 fmol ALP-Ab)
 HQDP 3 mM via dock GUARD CELL (2 porous-graphite         port d -----> W5 (20 uL, substrate entry to bed manifold)
   electrodes in series) + 1 mL holding loop -----------> port e --[P4]--> RC fill
                                                                        |
                                                  BED: 0.5 uL, 50 um SA particles, 0.5 x 0.5 x 2.0 mm, frits both ends
                                                                        |
                                                                        J --[P3]--> W2 counter-well 250 uL <-- port b
                                                                        |                (shuttle / drain to dock waste)
                                                                       [P1]
                                                                        v
                                                  RC 4 x 10 mm x 50 um = 2 uL, ceiling = WE k of the glass strip
                                                                        |--[P2]--> W4 overflow 50 uL (vented)
                                                  CE/RE: pads at the end of a 2 mm side channel (as A, §3.3)
 pogo pins: WE k, CE k, RE k -> Gamry (one channel, relay multiplexer per head)
 pinch plungers P0-P4 (dock, spring-closed when de-energised)
```

### 4.3 First-pass geometry

| Element | Dimension | Reasoning / source |
|---|---|---|
| W1 reception well | Ø 6 mm × 9 mm (≈ 250 µL), 150 µL working | 1.5 loop volumes (§2.2) |
| W2 counter-well | 250 µL | receives the shuttled sample |
| Capture bed | **0.5 µL** of 50 µm non-porous SA particles, ε 0.4, in a 0.5 × 0.5 mm channel × 2.0 mm, retained by two track-etched membrane frits (pore ≤ 20 µm; filtration membranes as hybrid elements, CS_FAB) | the gen-1 backup bed geometry (docs/05 §4.2: 0.5 µL, 50 µm, 0.5 mm, column/particle ratio 10); capture area 6(1−ε)/d × V = **36 mm²** (Derived); void 0.2 µL = accumulation volume; Kozeny–Carman 0.001 MPa at 10 µL/min (docs/05 §4.2). The smaller FRC-type bed (0.1 µL, 10 µm) was rejected: void 0.04 µL → nominal ULOQ 271 pg/mL even at 3 mM HQDP (run "B0 small bed", §8) |
| Conjugate well W3 | 50 µL with a dried spot of 20 fmol ALP-F(ab′)₂ (20 µL × 1 nM, the gen-1 backup dose, docs/05 §4.2); reconstituted in 20 µL A1, mixed by 10 pressure pulses | dried conjugate pattern (Hitzbleck2011, doi:10.1039/c1lc20282k; i-STAT); release is asymmetric without mixing (Gervais2011, doi:10.1016/j.bios.2011.06.016) |
| Readout chamber RC | 4.0 × 10.0 mm × 50 µm = 2.0 µL, WE 3.8 × 9.8 mm | as A (§2.3, §3.3); product from the 0.2 µL bed void is pushed in with 0.6 µL (3 void volumes) of substrate before the read |
| Electrode strip | glass, 8 WEs + per-cell CE/RE pads, 2 strips per card | one lithographic die per 8 cells instead of one per cell; WE-to-WE variation on one die **UNVERIFIED** (SPE value 0.10, 0.04–0.18, `ma.noise.spe_sensor_to_sensor_cv`, is the pessimistic bound) |
| Pinch points P0–P4 | foil membrane valves closed by dock plungers (CS_1367 principle) | 5 per cell |
| Ports | 5 face-seal through-holes per cell under a pierceable foil (piercing-seat principle of CS_FAB blisters); cells stay sealed until engaged | dry-reagent protection (Ford1994 humidity sensitivity of dried ALP, doi:10.1006/biol.1994.1026) |
| Card | microtiter-plate footprint 85.48 × 127.76 mm (CS_EXPLAINED), 2 rows × 8 cells, ≈ 10 mm body | 16 cells ≈ one 8-h block; a dock magazine of 4 cards = 64 determinations unattended [assessment] |

### 4.4 Per-cycle step table (cell k on head 1; t = 0 at Inject Start)

| t (min) | Step | Flow / volume | Pinch points open | Potentiostat |
|---|---|---|---|---|
| −3.0 → −1.0 | head 1 engages cell k (pierce, seal, pressure-hold leak test, contact check); RC filled from the holding loop (guard-cell-electrolysed HQDP 3 mM) | 20 µL at 20 µL/min | P4, P2 | – |
| −1.0 → 0 | SM-FL aspirates; dock selector → head 1 | BSM 1 µL/min → bypass | – | – |
| 0 → 1.5 | **Inject Start**; 150 µL A1 carries the plug into W1 | BSM 100 µL/min | – (W1 vented) | – |
| 1.5 → 26.5 | **Recirculating capture 25 min** at 25.0 °C: W1 ⇄ bed ⇄ W2 by headspace pressure, 10 µL/min, 120 µL strokes (≈ 1.7 passes of the sample) | 250 µL total shuttle | P0, P3 | – |
| 20.0 → 26.5 | (parallel) W3 reconstitution: 20 µL A1, 10 pulses | – | – | – |
| 25.5 → 26.0 | **Pre-electrolysis PE1** of the RC fill (removes the residual HQ the guard cell left, and that formed in the loop) | sealed | – | +0.35 V, 30 s |
| 26.5 → 27.5 | Drain W1/W2 to dock waste; post-capture wash 50 µL A1 through the bed to W2 | 50 µL/min | P0, P3 | – |
| 27.5 → 28.0 | Conjugate: 20 µL from W3 through the bed (capillary stop breaks at the head pressure) | 40 µL/min | P0, P3 | – |
| 28.0 → 31.0 | Conjugate stop 3 min (RC protected: P1 closed) | 0 | – | – |
| 31.0 → 33.0 | Wash 2 min (≥ 2 min after conjugate, C11) | 100 µL A1 at 50 µL/min → W2 | P0, P3 | – |
| 33.0 → 34.0 | Substrate fill of the bed from W5 (guard-cell HQDP), 100 bed-void volumes, no A1 left | 20 µL at 20 µL/min → W2 | P0, P3 | – |
| 34.0 → 49.0 | **Accumulation 15 min**, bed void sealed | 0 | – | OCP |
| 49.0 → 49.5 | Transfer: 0.6 µL substrate pushes the bed-void product through J into RC (RC far end overflows 0.6 µL of pre-electrolysed substrate to W4) | 1.2 µL/min | P0, P1, P2 | – |
| 49.5 → 50.0 | **Readout**: 30 s step, exhaustive; Q_net = Q − Q(PE1 background) | sealed | – | +0.35 V |
| **50.0** | **Result** (51.0 min from aspiration) | | | |
| 50.0 → 51.0 | head lifts, flushes its inlet bore and the dock selector with 100 µL A1; indexes to the next free cell | 100 µL/min | – | – |

**Staggering**: two heads, the SM-FL outlet switched between them by a dock 2-position valve; head 2's injection at
t = 26; the shuttle and readout of the two cells never coincide (reads at 49.5 and 75.5). Cadence ≈ 26 min per
sample (≈ 2.3 /h). Cells are independent, so parallel incubation needs only more heads and pressure channels.

### 4.5 Requirements F1–F20

| # | How B meets it | Status |
|---|---|---|
| F1 | 150 µL into a fresh, never-used well; 0.90 transfer; sample path: head bore 0.6 µL + dock selector + one cell | met |
| F2 | "chamber" = W1 ⇄ W2 recirculation through the bed for exactly 25 min from Inject Start; no bead suspension to keep mixed | met by design; capture rate in recirculation UNVERIFIED (risk B4) |
| F3 | capture phase dosed at manufacture (bed packing), not at run time | moves to manufacturing QC (risk B2) |
| F4, F5 | dried conjugate in its own well; meets the capture surface only after the sample is washed out (sequential) | met |
| F6 | dock selector + head; BSM parked to bypass | met (dock-side) |
| F7 | no bead transfer: the capture element stays in place | n/a (met) |
| F8 | packed bed instead of a trap; retention by frits, both flow directions | met by design |
| F9 | bed void sealed by P0, P1, P3 during accumulation; P1 opens only for the transfer | met |
| F10 | 1 min post-capture wash, 2 min after conjugate (C11); bed void exchanged 100× | met (wash efficiency not modelled) |
| F11 | substrate from a dock store through a guard cell, pre-electrolysed again in RC | met |
| F12 | 15 min accumulation in 0.2 µL; transfer 0.6 µL into RC; exhaustive read | met by design |
| F13 | P1 stays closed during the shuttle, labelling and washes, so the electrode sees only substrate and product; electrode used once | met |
| F14 | renewal by replacement of the cell | met |
| F15 | no capture-surface carry-over by construction; remaining paths: SM-FL, dock selector, head bore (§4.8) | largely met; head bore to be measured |
| F16 | plungers spring-closed, head spring-retract with cell sealed (pinch points closed), cell off | met |
| F17 | recovery = discard the current cell (mark it used), flush the head; consumes one cell | met (costs a cell) |
| F18 | 2 blanks + 1 control per card (16 cells) | met |
| F19 | dock Peltier under the engaged cell; card at room temperature (dried reagents) | met |
| F20 | RC sealed by pinch points during the read | partly (leakage UNVERIFIED) |

### 4.6 Reagent strategy, batch size and lifetime

| Reagent | Form and place | Per determination | Storage |
|---|---|---|---|
| Capture | biotin-cAb pre-loaded on SA particles, blocked, dried in the bed at manufacture | one bed | card in foil pouch with desiccant, 2–8 °C; stability of dried immuno-surfaces up to 6 months at RT reported for other chemistries (Asghar2016, doi:10.1038/srep21163) — **UNVERIFIED for this pair** |
| Conjugate | dried spot, 20 fmol | one spot | as above; dried ALP is sensitive to humidity and to temperature cycling (Ford1994) |
| HQDP 3 mM | liquid, dock bottle 4–8 °C, guard cell + 1 mL holding loop | ≈ 45 µL | 8-h bottle (Pi growth ≤ 0.17 µM per day at the acceptance-limit k_h ×3 for 3 mM = 0.5 µM/day, §2.3) |
| A1 | BSM (sample carrier) + dock bottle (washes, reconstitution) | 150 µL + ≈ 300 µL | – |

3 mM HQDP is required here: with the 0.2 µL accumulation volume the nominal ULOQ is 464 pg/mL at 1 mM and
1359 pg/mL at 3 mM (§8). **Lifetime: single-use cells, 16 per card; card open on the dock for ≤ 8 h** (the
dried-reagent humidity exposure after piercing is the limiting factor, **UNVERIFIED**). **Calibration**: per
manufacturing lot (bed batch × conjugate lot × electrode-strip batch), verified by the 3 control cells of every card;
a per-cell calibration is impossible by construction, so cell-to-cell CV enters every blank (risk B2).

### 4.7 Valves and actuations

On the consumable: 5 pinch points per cell × 16 = 80 per card, each actuated ≤ 3 times in its life (single use),
plus one capillary stop per cell (one-shot; burst point a few kPa, Hitzbleck2012, doi:10.1039/c2lc00015f; detergent
shifts burst points, Mark2009, doi:10.1039/b914415c — the reconstitution buffer contains Tween, so the stop is
opened by head pressure, not relied on to hold). This is inside the published single-use evidence (CS_1367 single
use; CHILDERS2024 > 50). In the dock: per head ≈ 8 solenoid valves for ports and plungers, ≈ 10 actuations per
determination, i.e. ~10⁴ per month — dock solenoids, not membrane valves; elastomer face seals of the head see
16 engagements per card and are a service item [assessment].

### 4.8 NSB surface budget and carry-over

| Surface | Area | In product path? | Conjugate exposure | Source |
|---|---|---|---|---|
| Bed particles | **36 mm²** × packed-bed factor 3 (1–30, `ma.nsb.surface_factor_packed_bed`, UNVERIFIED) | yes | 1 nM, 3 min stop + fill (≈ 3–4 nM·min) | Derived; model "B0" effective NSB area 110 mm² |
| Bed channel walls (COC) | 4 × 0.5 × 2.0 = 4 mm² × chip factor 10 (1–100) | yes | same | Derived; **not in the model** (worse, ≤ ×1.4 on NSB at factor 10) |
| J + RC | 1 + 80 mm² | yes | none (P1 closed during labelling) | by design |
| W1, W2, W3 | ≈ 400 mm² | no | – | single use: only analyte loss matters (sample-contact area, F1) |

Compared with A (beads 12.3 mm² at factor 1, but 11 nM·min of one-step exposure), B exposes 3× the area at a 3×
higher factor for about one third of the exposure; the model's NSB enzyme count is similar (≈ 5000 vs ≈ 5700), but B
labels only 1.7 % of the captured analyte in flow against 10 % in A's one-step incubation (model "label fraction"),
which is why B gains so little from a better detection reagent.

**Carry-over paths**: capture surface, conjugate, RC and electrode are new for every determination (zero by
construction); SM-FL (10⁻⁴ UNVERIFIED, needle wash); dock selector valve and head inlet bore (0.6 µL), flushed with
100 µL A1 after every cell — residual liquid 0.6/100 → < 10⁻⁶ after a 167-volume flush if it behaves as a stirred
volume (Derived; adsorbed protein **UNVERIFIED**). B is the only candidate where the 10⁻⁴ criterion does not depend
on a cleaning step inside the consumable.

### 4.9 First-order performance (nearest-model estimates)

Nearest architecture: gen-1 backup B-bed (`B-bed-IDA` optimum with the final 0.5 mm column, thin-layer detector),
with: sample-load flow 6 µL/min and 1.5 loop volumes as the single-pass equivalent of 25 min of recirculation of
150 µL (Q_eq = V/t = 150/25, Derived; the model's loop-transfer at 6 µL/min (0.996) is rescaled to the real 0.90 by
`lod_scale` 1.106); regeneration replaced by a 1-min index step; residual label 10⁻⁶ and capacity loss 0 (fresh
cell); 20 µL of 1 nM conjugate, 3-min stop; accumulation 15 min; HQDP 3 mM; isolated connection 2 mm. The script's
gen-1 constraint flags "isolated connection < 0.01 m" and "loop flush < 2" refer to valve-port plumbing and to the
loop model's validated range and do not apply to this mapping.

| Run (nearest-model estimate) | Nominal | Median [5–95 %] | P(success) | ULOQ | Model time |
|---|---|---|---|---|---|
| gen-1 backup B-bed, as specified | 0.85 | 3.4 [0.65–33] | 0.09 | 1040 | 51.5 |
| **B0** as specified (electrode CV 0.02 — exhaustive read cancels area variation) | 0.63 | **2.3 [0.52–23]** | **0.15** | 1360 | 52.0 |
| B0 with SPE-class electrode CV 0.10 (no cancellation) | 0.85 | 3.1 [0.61–30] | 0.12 | 1360 | 52.0 |
| B0 with +10 % cell-to-cell NSB CV (blank CV 0.14, 0.05–0.25; scenario) | 0.85 | 2.9 [0.59–30] | 0.12 | 1360 | 52.0 |
| **B1** = B0 + pre-electrolysis (guard cell + in-RC) | 0.63 | **2.1 [0.49–21]** | **0.17** | 1360 | 52.0 |
| gen-1 backup after L6 + L7 | 0.71 | 2.8 [0.59–23] | 0.11 | 794 | 51.5 |
| B0 + L6 + L7 | 0.51 | 1.8 [0.45–17] | 0.19 | 1040 | 52.0 |
| B1 + L6 + L7 | 0.51 | 1.8 [0.45–17] | 0.20 | 1040 | 52.0 |
| B0, packed-bed factor 1 | 0.30 | 1.2 [0.30–7] | 0.33 | 1360 | 52.0 |
| B0, packed-bed factor 10 | 1.95 | 4.3 [0.82–37] | 0.06 | 1360 | 52.0 |
| B0, small bed 0.1 µL / 10 µm | 0.59 | 2.0 [0.47–20] | 0.12 | **271** | 52.0 |
| B0 under S4a (free HQ 10⁻³) | 4.7 | 10 | 0.01 | 1360 | 52.0 |
| B0 + L4 (outside the model, unmeasured) | 0.23 | 1.0 [0.27–6] | 0.40 | 1360 | 52.0 |

**Where B's gain over the gen-1 backup comes from**: longer capture (25 min recirculation instead of 20 min single
pass; captured fraction 0.57 vs 0.43), no regeneration (no residual label, no 6.5-min regeneration step), and 15 min
accumulation. **What decides B**: the packed-bed NSB factor (P 0.33 at factor 1, 0.06 at factor 10) — the same
UNVERIFIED parameter that made the gen-1 backup the backup.

**Chip effects the model cannot represent, and direction:** recirculating capture modelled as one pass at Q_eq
(neutral: lower per-pass efficiency at the real 10 µL/min vs higher film transfer; §5.4 item 5); single-WE exhaustive
read per cell (item 3; conversion neutral, electrode CV shown both ways); conjugate dosed on-board, not dispersed
through the loop (item 4; neutral, labelling and NSB both ∝ concentration in this linear regime); bed-channel walls
(item 6; **worse**, ≤ ×1.4 NSB); dried-reagent ageing (item 7; **worse**, unknown); cell-to-cell variation (item 9;
**worse**, shown as a scenario); per-cell manufacturing contamination with human IgG (C21; **worse**); temperature
control (item 11; better).

### 4.10 Fabrication route

Single use forces the production route early: injection-moulded COC/COP card (ChipShop-type, MOQ 100, CS_FAB) on
the microtiter footprint; beds packed from slurry and closed by membrane frits; capture loading, blocking and drying
on-card; conjugate spotting (ChipShop dry reagents and pL spotting, CS_FAB); glass electrode strips (Micrux custom or
IMT, MICRUX_TF/IMT_FLYER) bonded into pockets; pierceable foil seal (blister piercing-seat principle, CS_FAB).
Prototype: milled COC 4-cell card, beds packed by hand, Micrux catalogue single electrodes, dock head from a 3-axis
stage. The dock is the complex part (two heads, pressure channels, guard cell, selector).

### 4.11 Top 5 risks and retiring experiments

| # | Risk | Retiring bench experiment |
|---|---|---|
| B1 | Packed-bed (SA particle) NSB factor ≥ 3 relative to blocked M-280 beads | U4-type conjugate exposure series (0.3–3 nM × 3–30 min) on 0.5 µL beds of 2–3 candidate particle types vs M-280 beads in tubes; blank enzymes per mm² per nM·min |
| B2 | Cell-to-cell CV of bed amount, capture activity after drying, conjugate spot > 10 % (blank SD, lot calibration) | 20 cells from one batch: bed mass, blank and 10 pg/mL CV; capture activity after drying vs wet |
| B3 | Dried conjugate / dried capture lose activity or gain NSB on storage; reconstitution inhomogeneous | ageing 0–8 weeks at 4, 25, 37 °C with humidity control (Ford1994 risk); reconstitution CV with and without pulse mixing (Gervais2011) |
| B4 | Recirculating capture slower than the single-pass equivalent | capture vs time at 5, 10, 20 µL/min shuttle, 10–1000 pg/mL, against the model's B-bed curve |
| B5 | Exhaustive read on a shared strip: WE-to-WE CV, product transfer bed → RC, pre-electrolysis | HQ standards in all 16 RCs of 3 strips; ALP-loaded bed product transfer with 0.3–1.2 µL pushes; spiked-HQ removal |

---

## 5. Candidate C — permanent glass chip with a regenerated micro-bed and stopped-flow IDA, swappable reagent pack

### 5.1 Concept

A small all-glass chip stays in the dock for its qualified life. It carries an etched 0.1 µL bed of 10 µm particles
with covalently oriented anti-human-Fc capture antibody behind a 5 µm etched weir, a **side outlet at the bed exit**
that takes sample, conjugate and glycine to waste, and a sealed 25 µm IDA channel that receives only substrate and
product (Scheme C of the model, with the electrode protected). The sample is loaded straight through the bed by the
BSM at 10 µL/min (no chamber), labelled sequentially, the bed + IDA channel are sealed for 7.5 min, the product is
read by stopped-flow redox cycling on two potentiostat channels, and the bed is regenerated with glycine-HCl pH 2.
The only consumable is a **daily reagent pack** (conjugate, glycine, HQDP, particle slurry) in a cooled dock rack.
Nearest precedent: regenerated in-channel immunosorbent with amperometry, 51 cycles (Uthuppu2015,
doi:10.1039/c4an01576b); stopped-flow IDA reading of pAP in 70 nL (Chen2011, docs/10 §4.1); the model's own
`C-bed-IDA` optimum (docs/05 §1.2, FRC).

### 5.2 Block diagram

```
 DOCK                                                     PERMANENT GLASS CHIP (IMT-class, RT-bonded; FEP membrane
                                                          valve layer, pneumatic manifold in the dock)
 ==================================================================================================================
 SM-FL --PEEK 0.3 m--> [Vin] --------------------------> bed inlet node N1
   BSM A1 10 uL/min (load) / 1 uL/min (park) --[Vb]--> waste
 REAGENT PACK (4-8 C rack):                              N1 --> BED 0.1 uL, 10 um anti-Fc particles,
   conjugate 1 nM (vial)  \                                     0.3 x 0.1 mm etched channel x 3.7 mm, 5 um weir
   glycine-HCl pH 2       |-- dock rotary selector --[Vr]--> N1      |
   HQDP 1 mM -> GUARD CELL|   + syringe pump (gen-1 SIA)              N2 (bed exit) --[Vs]--> side outlet --> waste
   A1, particle slurry    /                                           |
                                                                    [Vi]
                                                                      v
                                                     IDA channel 25 um x 0.2 mm x 3 mm (15 nL), 50 pairs 5/5 um Pt,
                                                     fingers 0.2 mm across the channel; Ag/AgCl (or Au QRE) + Pt CE
                                                     at the outlet end --[Vo]--> waste
 pogo pins: generator (Ref 600+, +0.35 V), collector (second channel, -0.1 to -0.2 V, UNVERIFIED), RE, CE
 V_acc (sealed: Vr, Vin, Vs, Vo closed; Vi open) = bed void 0.04 uL + IDA channel 0.015 uL = 55 nL
```

### 5.3 First-pass geometry

| Element | Dimension | Reasoning / source |
|---|---|---|
| Bed | 0.1 µL of 10 µm particles (ε 0.4) in an isotropically etched 0.3 × 0.1 mm channel × 3.7 mm; capture area **36 mm²** (Derived) | the model's FRC optimum (0.1 µL, 10 µm, 0.2 mm ID; `results/design/optimum_FRC__baseline.json`); etch depth ≈ ½ undercut (docs/11 §1.1); column/particle ratio ≥ 10 (docs/05 §1.4) |
| Weir | 5 µm etched step at the bed exit | glass etch depths from 100 nm (docs/11 §1.1); holds 10 µm particles |
| Bed pressure drop | 0.14 MPa at 10 µL/min, 0.29 MPa at 20 µL/min (Derived, Kozeny–Carman: 150 µ u L (1−ε)²/(ε³ d²) with u = Q / 0.031 mm², L 3.2 mm) | washes and glycine ≤ 20 µL/min; bonded glass ≫ this (docs/11 §1.1); FEP valve rating **UNVERIFIED** |
| IDA channel | 25 µm × 0.2 mm × 3 mm = 15 nL; IDA 50 pairs, 5 µm fingers and gaps, Pt | FRC optimum channel (3 × 0.2 mm, `ma.geometry.chip_channel_height` 25 µm); IDA rules ≥ 2 µm (IMT_FLYER); Micrux IDA6 (5/5 µm, 30 pairs) is the catalogue prototype (BASI_IDA). The model's `ma.geometry.ida_finger_length_chip` (0.5 mm) is longer than the 0.2 mm channel — the model's IDA current is optimistic; neutral on the NSB-limited LOD |
| Accumulation volume | 55 nL | model diagnostic; nominal ULOQ 1040 pg/mL at 7.5 min / 1 mM; at 15 min it falls to 464 unless HQDP is 3 mM (§8) |
| Valves | 6: Vin, Vb, Vr, Vs, Vi, Vo; normally closed glass–FEP–glass membrane valves, pneumatic | Grover2006 (doi:10.1039/b518362f), FEP membrane Grover2008 (doi:10.1039/b800600h): best chemical inertness found (docs/10 §7) — chosen because pH 2 glycine and protein pass the valves every run |
| Chip | ≈ 15 × 45 mm glass (Micronit-class functional element, DARWIN_SERP) | small: no chamber, no reagent tanks |

### 5.4 Per-cycle step table (t = 0 at Inject Start)

| t (min) | Step | Flow / volume | Valves open | Potentiostat |
|---|---|---|---|---|
| −1.0 → 0 | SM-FL aspirates | BSM 1 µL/min → bypass | Vb | – |
| 0 → 20.0 | **Load**: 2 loop volumes through the bed (transfer as model, `hw.smfl.loop_flush_volumes_for_transfer` 2) | BSM **10 µL/min**, 200 µL → side outlet | Vin, Vs | – |
| 20.0 → 21.0 | Post-capture wash | A1 10 µL/min | Vin, Vs | – |
| 21.0 → 27.0 | Conjugate 10 µL of 1 nM from the pack (fill 1, stop 2, wash 2, + 1 overhead) | syringe ≤ 20 µL/min | Vr, Vs | – |
| 26.5 → 27.0 | IDA channel pre-filled backwards through Vo from a dock substrate port (guard-cell HQDP) and pre-electrolysed by the generator | 5 µL | Vo | +0.35 V, 30 s |
| 27.0 → 28.0 | Substrate fill of the bed (guard-cell HQDP), Vi opened only at the end so the IDA channel sees substrate, never conjugate | 20 µL at 20 µL/min → side outlet, last 1 µL into the IDA channel | Vr, Vs → Vr, Vi, Vo | – |
| 28.0 → 35.5 | **Accumulation 7.5 min**, bed + IDA channel sealed (55 nL) | 0 | Vi | OCP |
| 35.5 → 37.5 | **Readout**: stopped-flow redox cycling, steady-state generator/collector currents, charge over 2 min | 0 | Vi | gen +0.35 V, coll −0.1 to −0.2 V |
| **37.5** | **Result** (38.5 min from aspiration) | | | |
| 37.5 → 44.0 | **Regeneration**: glycine-HCl pH 2, 100 µL, 2 min contact, A1 re-equilibration (docs/05 §4.2: 6.5 min); IDA channel closed (Vi) | ≤ 20 µL/min → side outlet | Vr, Vs | – |
| 44.0 | ready for the next injection (cycle 45 min, model) | | | |

No staggering is possible with one bed; throughput **1 per 45 min** (≈ 1.3 /h; 10–11 per 8-h pack day). A second
bed + IDA lane would double it at the cost of two more potentiostat channels.

### 5.5 Requirements F1–F20

| # | How C meets it | Status |
|---|---|---|
| F1 | plug loaded directly through the bed at 10 µL/min (BSM at 10 µL/min: precision 1 % RSD **UNVERIFIED**, `hw.bsm.flow_precision_rsd_low_flow`; back-pressure open item, docs/08 §10) | partly |
| F2 | no chamber: capture is single-pass in flow (20 min); no mixing problem | met (by avoiding it) |
| F3 | capture phase is the permanent bed; renewal by regeneration (or repacking from the pack slurry, variant C3) | n/a |
| F4, F5 | conjugate from the pack after the sample, never mixed with capture phase in a store | met |
| F6 | Vin/Vb on chip; BSM parked to bypass outside the load | met |
| F7 | no bead transfer | n/a |
| F8 | bed retained by the weir | met |
| F9 | sealed 55 nL (Vi open, all others closed); valves move before accumulation only | met |
| F10 | 1 min after capture, 2 min after conjugate (C11) at 10–20 µL/min = 250–500 bed-void volumes | met (wash efficiency not modelled) |
| F11 | guard-cell HQDP from the pack, no A1 in the IDA channel | met |
| F12 | 7.5 min accumulation; stopped-flow IDA read in place (Scheme C) | met by design; stopped-IDA efficiency `ma.detection.ida_stopped_efficiency` 0.5 (0.2–1) **UNVERIFIED** |
| F13 | the side outlet keeps sample, conjugate and pH 2 out of the IDA channel | met by design (seat leakage UNVERIFIED) |
| F14 | glycine pH 2 regeneration each run, ≤ 0.5 %/cycle capacity loss assumed (`chem.regeneration.activity_loss_per_cycle` 0–7 %, low) | open (risk C2) |
| F15 | **residual analyte and label after glycine must be ≤ 10⁻⁴** (§5.8) | open, decisive (risk C1) |
| F16 | valves normally closed (fail-closed), cell off; the bed stays wet (no drain path) | met |
| F17 | recovery = double regeneration + A1 flush (≈ 8 min) | met |
| F18 | blanks + control every 10 + recalibration every ≈ 20 runs (10 % slope drift at 0.5 %/cycle, docs/05 §4.2) | met, costly (§5.6) |
| F19 | dock Peltier under the chip | met |
| F20 | sealed channel during the read (valve break) | partly |

### 5.6 Reagent strategy, batch size and lifetime

Reagent pack (daily, 4–8 °C rack in the dock, vials): conjugate 1 nM, 10 µL per run → 0.5 mL covers ≈ 20 runs +
priming (liquid, 8-h default life, docs/07 §5.5); glycine-HCl pH 2, 100 µL per run (stable, not on the BSM because
pH 2 is the I-Class limit, `hw.bsm.ph_min`); HQDP 1 mM through the guard cell, ≈ 30 µL per run; particle slurry for
repacking (variant C3). **Lifetime**: chip permanent (target ≥ 300 runs, which equals the best regeneration evidence
for anti-Fc surfaces, Kamat2021 SPR > 300 cycles via docs/10 §3.2, but on chip only ≤ 51 cycles are documented,
Uthuppu2015); bed regenerated every run; recalibration every ≈ 20 runs; repack the bed from the slurry when the
capacity has fallen to ≈ 70 % ((1 − 0.005)ⁿ = 0.7 → n ≈ 71 runs, Derived) or when the carry-over check fails.
**Batch**: ≈ 10–11 determinations per pack day. **Calibration cost (Derived)**: a 5-point curve + 2 blanks every 20
runs = 35 % of determinations, or a 1-point slope check every 10 runs = 10 % if the curve shape is stable.

### 5.7 Valves and actuations

6 on-chip valves; per run: Vs ≈ 4, Vr ≈ 3, Vb 2, Vin, Vi, Vo 1–2 → ≈ 12 actuations per run; over 300 runs
**≈ 3600 actuations, ≈ 1200 on the busiest valve**, with protein, particles nearby and pH 2. Evidence: FEP membrane
valves "maintain performance over extended use" (Grover2008, no number); latching variants (Grover2006); ≥ 10⁶ only
for PDMS in clean liquids (secondary, docs/10 §7); thermoplastic membranes > 50 (CHILDERS2024). **C needs ≈ 20× the
published thermoplastic figure** — a valve-endurance gate at ≥ 3000 cycles in glycine and protein (risk C5). Dock
rotary selector: gen-1 SIA hardware (IDEX-type, rated life UNVERIFIED here, docs/11 §3).

### 5.8 NSB surface budget and carry-over

| Surface | Area | In product path? | Exposure | Source |
|---|---|---|---|---|
| Bed particles | **36 mm²** × packed-bed factor 3 | yes | 1 nM × 2 min stop + fill | Derived; model "C1/C2" effective 108 mm² |
| Bed channel walls (glass) | ≈ 0.6 mm perimeter × 3.7 mm ≈ 2.2 mm² × chip factor 10 | yes | same | Derived; **not in the model** (worse ≤ ×1.2) |
| IDA channel + electrodes | 2 × 0.2 × 3 = 1.2 mm² | yes | none (side outlet) | model "C1" sets the chip factor to 0.01 for this (the L2 representation, docs/05 §2) |

**Carry-over paths** (10⁻⁴ criterion):
1. **Residual analyte on the regenerated bed** — not represented in the model at all (the model's
   `chem.regeneration.residual_label_carryover_fraction` covers label, 10⁻⁶–10⁻², UNVERIFIED; ALP is largely
   inactivated by pH 2, `chem.enzymes.alp.inactivation_by_low_pH_regeneration`, so residual *label* barely matters:
   P 0.16 → 0.15 at 10⁻² in run "C2 residual 1e-2"). Captured IgG that glycine fails to elute is labelled again in
   the next run: carry-over = 1 − elution efficiency. The only chip elution number found is 92 % (FITC-HSA on an
   affinity monolith, Sun2008, doi:10.1021/ac800322f), i.e. **8×10⁻² — 800× the criterion**. C is viable only if
   glycine removes ≥ 99.99 % of captured human IgG from the anti-Fc bed; no source in docs/10 shows that.
2. SM-FL (10⁻⁴, UNVERIFIED) and Vin/N1 seats (sample film) — as A.
3. Conjugate adsorbed on bed walls and valve seats near N1/N2 that survives glycine — part of the residual-label term.
Mitigation: double regeneration after any sample > 100 pg/mL (docs/08 S6 alternative), +6.5 min.

### 5.9 First-order performance (nearest-model estimates)

Nearest architecture: the model's own `C-bed-IDA` FRC optimum (`results/design/optimum_FRC__baseline.json`), which
docs/05 evaluated before the review and which was **not re-evaluated after the review** (docs/09 §5.2); here with the
review parameters. Variants: side-outlet protection (chip factor of the IDA channel → 0.01); non-fouling electrode
class (the model forces the fouling CV 0.10 and 1 %/cycle on every Scheme C design; with HQ (non-fouling, Wilson2004
via docs/05 §4.1) and no protein over the IDA the non-fouling class 0.02 / 0.1 %/cycle applies — a scenario, not a
measurement).

| Run (nearest-model estimate) | Nominal | Median [5–95 %] | P(success) | ULOQ | Model time |
|---|---|---|---|---|---|
| FRC optimum, review parameters (unprotected, fouling class) | 0.95 | 3.8 [0.64–47] | 0.09 | 1040 | 45.0 |
| C1: + side outlet | 0.86 | 3.4 [0.60–37] | 0.11 | 1040 | 45.0 |
| **C2**: + non-fouling electrode class (as specified) | 0.64 | **2.4 [0.48–25]** | **0.16** | 1040 | 45.0 |
| C2 + pre-electrolysis (guard cell + generator) | 0.64 | 2.2 [0.45–24] | 0.18 | 1040 | 45.0 |
| C2 + L6 + L7 | 0.53 | 1.9 [0.41–18] | 0.20 (ULOQ 794 flagged) | 794 | 45.0 |
| C2, accumulation 15 min, 3 mM HQDP | 0.62 | 2.3 [0.46–26] | 0.18 | 1360 | 52.5 |
| C3: bed repacked every run instead of regenerated | 0.64 | 2.4 [0.48–24] | 0.16 | 1040 | 41.5 |
| C2, residual label 10⁻² | 0.64 | 2.4 [0.50–26] | 0.15 | 1040 | 45.0 |
| C2, packed-bed factor 10 | 2.0 | 4.7 [0.83–44] | 0.06 | 1040 | 45.0 |
| C2 + L4 (outside the model, unmeasured) | 0.19 | 0.94 [0.23–7] | 0.43 | 1040 | 45.0 |

**Reading**: C's as-specified number matches gen-1 only after the protection and non-fouling credits, which are
design intentions; its in-flow sequential labelling (label fraction 0.5 % in the model) leaves almost nothing for a
better detection reagent to gain (L6 + L7: 0.20 vs gen-1's 0.32), and its LOD is set by the packed-bed factor, as for B.

**Unrepresented chip effects and direction:** residual analyte after regeneration (**worse, potentially fatal**,
§5.8); bed-channel walls (**worse**, ≤ ×1.2); IDA finger length vs channel width (model optimistic, LOD-neutral);
conjugate from the pack, not through the loop (§5.4 item 4; neutral); BSM flow precision at 10 µL/min enters capture
CV (**worse**); collector O₂-reduction background (docs/08 W6; **worse**); capacity drift between recalibrations
(item 8; **worse**, handled by recalibration cost); temperature control (item 11; better).

### 5.10 Fabrication route

Glass from a thin-film/glass foundry (IMT: Au/Pt/Ti ≥ 2 µm, 200 mm wafers, room-temperature bonding, IMT_FLYER /
IMT_PRESS); FEP-membrane valve layer clamped against a glass pneumatic manifold (Grover2008 architecture); permanent in
an aluminium dock with flat-bottom 1/16″ fittings (Micronit Fluidic Connect class, 100 bar, DARWIN_FC4515). Prototype:
catalogue Micrux IDA6 die (5/5 µm, 30 pairs; BASI_IDA) under a milled COC channel with a hand-packed bed and CS_1367
valves, to test regeneration chemistry and the stopped IDA read before any glass run. Lead time weeks–months, high
cost per design (docs/11 §1.1); lowest cost per determination.

### 5.11 Top 5 risks and retiring experiments

| # | Risk | Retiring bench experiment |
|---|---|---|
| C1 | Glycine leaves > 10⁻⁴ of captured human IgG (and label) on the anti-Fc bed → carry-over | 0.1 µL anti-Fc bed in a PEEK/COC mock-up: 10 ng/mL challenge, 1× and 2× regeneration, then 3 blanks through the low-range slope (E2.7 criterion) |
| C2 | Capacity loss > 0.5 %/cycle or non-linear; capture-antibody leaching (reagent-borne IgG) | 100 cycles alternating blank / 100 pg/mL; slope and blank vs cycle |
| C3 | Packed-bed NSB factor ≥ 3 (as B1), plus glass wall share | U4-type exposure series on 10 µm covalent particles |
| C4 | Stopped IDA read: efficiency, collector O₂ background, Ti undercut at pH 2, HQ/BQ on Pt over 300 cycles | E3.1 (docs/06) on the Micrux IDA6 in a 25 µm channel; 300 glycine exposures of the die |
| C5 | FEP valve endurance < 3000 cycles in glycine/protein; BSM at 10 µL/min (precision, back-pressure) | endurance rig; gravimetric BSM test at 10 µL/min into the chip resistance (docs/06 S0.6) |

---

## 6. Side-by-side comparison

All performance figures are **nearest-model estimates** (§8), n = 2000, success = L_eff ≤ 1 (docs/05 convention);
ΔP < 0.05 is not decision-grade (docs/08 W7). Gen-1 numbers are docs/08 §10.1 (reproduced in the same runs).

| | Gen-1 primary (reference) | **A** bead-transfer multi-run | **B** single-use cells | **C** permanent regenerated chip |
|---|---|---|---|---|
| Capture renewal | beads per run | beads per run | fresh factory cell per run | glycine regeneration |
| Labelling | one-step, chamber | one-step, chamber | sequential, in flow | sequential, in flow |
| Detector | thin-layer flow cell (IDA option) | single WE, stopped, exhaustive | single WE per cell, stopped, exhaustive | IDA, stopped redox cycling, 2 channels |
| Median [5–95 %] / P, as specified | 3.5 [0.51–157] / 0.16 | 2.3 [0.43–73] / 0.20; **with pre-electrolysis 1.9 / 0.25** | 2.3 [0.52–23] / 0.15; with pre-el. 2.1 / 0.17 | 2.4 [0.48–25] / 0.16; with pre-el. 2.2 / 0.18 |
| After U1–U3 screening (L6 + L7) | 1.3 / 0.32 | **1.1 / 0.39** (3 mM, pre-el.) | 1.8 / 0.20 | 1.9 / 0.20 |
| With L4 (outside the model; does not count for G1) | 1.5 / 0.33 | 0.91 / 0.53 | 1.0 / 0.40 | 0.94 / 0.43 |
| Decisive model parameter | bead NSB, chamber mixing | bead NSB, chamber mixing | packed-bed NSB factor: P 0.33 (×1) ↔ 0.06 (×10) | packed-bed NSB factor (0.06 at ×10) |
| Inject Start → result | 52.1 min | 54.0 min | 50.0 min | 37.5 min |
| Throughput | 56 min/sample (≈ 30 with a 2nd cup) | 27.5 min (2 chambers) | ≈ 26 min (2 heads) | 45 min |
| Valves on the consumable; actuations | 3 external + 8-port SIA (gen-1 hardware) | 21; ≈ 520 per card, busiest ≈ 70 (1.4× published thermoplastic evidence) | 80 pinch points per card, ≤ 3 each (inside single-use evidence) | 6; ≈ 3600 per 300 runs, busiest ≈ 1200 (≈ 20× published) |
| Consumable cost class [assessment, no prices seen] | reagents only | medium: 1/16 of a moulded, filled card with a glass die per determination | **high**: one cell with bed, dried reagents and 1/8 of an electrode strip per determination | **low**: reagent vials; chip amortised |
| Dock complexity [assessment] | – | high (magnet carriage, 3 pressure channels, syringe, 2 Peltier zones) | highest (2 x–y heads, guard cell, selector, pressure, magazine) | medium (pneumatic manifold, selector + syringe, guard cell, 2-channel potentiostat) |
| Carry-over ≤ 10⁻⁴ | U5 accepts 10⁻³ (10× too loose) | depends on residual beads; **measured every run (PE2)** | **by construction** except head and SM-FL | needs ≥ 99.99 % glycine elution; only 92 % found |
| Evidence strength | medium | medium: every element precedented (Rusling chamber→detection; Wang2013 drag; Herrmann2007 bridges), no multi-run liquid-bead cartridge precedent | strongest format precedent (Gyrolab, Ella, i-STAT), but optical and ≥ 10 pg/mL | weakest (≤ 51 chip regeneration cycles, none for sandwich IgG) |
| Biggest unknown | U1/U3 | residual beads ≤ 10⁻⁴ and chamber mixing factor | bed NSB factor and cell-to-cell CV | elution completeness (carry-over) |

---

## 7. The four open choices, answered per candidate

| Choice | A | B | C |
|---|---|---|---|
| **Chip lifetime** | multi-run cartridge for **one 8-h block** (conjugate store default life 8 h; valve evidence ≈ 50–70 cycles; daily reset of chamber walls) | **single-use cell** inside a 16-cell card with an **automatic changer** (dock x–y head; magazine of 4 cards) | **permanent chip + daily swappable reagent pack**; bed regenerated each run, repacked from the pack at ≈ 70 % capacity |
| **Detector** | **single thin-film WE, stopped flow, exhaustive** (one channel): all product collected; area variation cancels; IDA gain would multiply NSB charge too | same, one WE per cell on a lithographic strip (one channel, relay multiplexer) | **IDA redox cycling, stopped flow** (two channels), justified only because the die is permanent; the model gives it no LOD advantage once the electrode is protected |
| **Batch size per reagent load** | 16 determinations (13 samples + 2 blanks + 1 control); stores sized for 20 doses (+2 priming, +2 recovery) | 16 cells per card (13 + 3 QC); HQDP bottle per 8 h | 10–11 per pack day; recalibration every ≈ 20 runs (10–35 % overhead) |
| **Parallel / staggered incubation** | **2 staggered chambers sharing one readout chamber**, cadence 27.5 min; identical 30-min incubation from each Inject Start | **2 heads, staggered by 26 min**; cells independent, so more heads scale linearly | **none** (single bed; a second lane needs 2 more potentiostat channels) |

Why stopped and exhaustive rather than IDA for A and B: docs/10 §4.1 shows the IDA gain survives only in stopped flow;
docs/08 S9 and §8 here show EC noise is 3–5 % of the blank variance; a gain factor that multiplies the NSB charge as
much as the specific charge cannot move an NSB-limited LOD. Exhaustive coulometry gives the same "all product counted"
with one channel and without the marginal collector potential (docs/08 W6).

---

## 8. Model runs: method, all results, and what the model cannot represent

**Method.** The repository was copied to the session scratchpad (outside the repository); the existing package and
scripts were imported from the copy; nothing in `src/`, `params/`, `scripts/` or `results/` was changed or written
in the repository. Each candidate is an **existing architecture** with `Architecture.with_design(...)` overrides and
parameter-set modifiers, evaluated with `scripts/design_lib.mc(arch, ps, n=2000, lod_scale=…)` (seed 20261111), the
same path as `scripts/final_designs.py` (docs/09 §5.5 "recommended way"). The overrides (every value is a design
choice of this document or a stated representation of an unmodelled effect):

| Candidate | Base | Overrides | Representation of chip features |
|---|---|---|---|
| A | `final_designs` P-chamb optimum (B-mag1, OS optimum), detector `thin_layer` | `ma.timing.in_vial_incubation` 30; `hw.timing.accumulation_time` 15; `hw.smfl.loop_flush_volumes_for_transfer` 6.6 (7-min collect/rinse/drag block, bead transfer 0.96); `ma.timing.post_sample_wash` 1.5; `hw.timing.substrate_fill` 0.5; `ma.timing.bead_flush_and_clean` 2; `hw.timing.readout_time` 1 | chamber stirring factor log-triangular on [0.2, 1.0]/**1.7** (mode 1/1.7; final_designs uses /2.2); `lod_scale` 1/0.90 (1.5 loop volumes); clean readout zone: `ma.nsb.surface_factor_tubing` pinned 0.01 (the docs/05 L2 representation) |
| B | `final_designs` B-bed (FRB optimum, 0.5 mm column), detector `thin_layer` | bed 0.5 µL, 50 µm, 0.5 mm; `hw.timing.sample_load_flow` 6 and 1.5 loop volumes (Q_eq = 150 µL / 25 min); `ma.geometry.reactor_connection_length` 0.002; conjugate 1 nM, 20 µL, 3-min stop; accumulation 15; `hw.timing.regeneration_and_reequilibration` 1 (index step) | fresh cell: `chem.regeneration.residual_label_carryover_fraction` 10⁻⁶, `…activity_loss_per_cycle` 0; HQDP 3 mM; `lod_scale` = model loop transfer (0.996) / 0.90 = 1.106 |
| C | `C-bed-IDA` FRC optimum (0.1 µL, 10 µm, 0.2 mm, channel 3 × 0.2 mm, 10 µL/min, 10 µL conjugate, 2-min stop, 7.5-min accumulation) | — | side outlet: `ma.nsb.surface_factor_chip` pinned 0.01; non-fouling class: `ma.noise.electrode_sensitivity_cv_fouling` → 0.02 (0.005–0.05) and `ma.reuse.electrode_sensitivity_loss_per_cycle_fouling` → 0.001 (0–0.005) |
| all | — | pre-electrolysis variants: `ma.chemistries.alp_hqdp.free_product_impurity` × 0.01 (value 10⁻⁷, bounds 10⁻⁹–10⁻⁵; a pinned scenario value is multiplied by 0.01) | §2.3 assumption: 1 % of the fill escapes electrolysis (UNVERIFIED) |

Scenarios L6 + L7, S3b, S4a, C1 and lever L4 are the functions of `scripts/robustness.py`, `final_designs.py` and
`design_lib.l4_transfer`, unchanged. A compact version of the run script is in Appendix A.

**All runs** (nominal LOD; median [5–95 %]; P(success); P(LOD ≤ 1); nominal ULOQ; model time to result):

| Run | Nominal | Median [5–95 %] | P | P(LOD≤1) | ULOQ | t (min) |
|---|---|---|---|---|---|---|
| REF gen-1 P-chamb S0 | 0.60 | 3.5 [0.51–157] | 0.16 | 0.17 | 5200 | 56.1 |
| REF gen-1 P-chamb L6+L7 | 0.19 | 1.3 [0.34–9.0] | 0.32 | 0.35 | 1780 | 56.1 |
| REF gen-1 S-chamb S0 | 0.42 | 3.0 [0.56–26] | 0.13 | 0.16 | 1360 | 58.1 |
| A0 S0 | 0.41 | 2.3 [0.43–73] | 0.20 | 0.23 | 2330 | 57.6 |
| A0 without clean zone | 0.43 | 2.5 [0.45–79] | 0.19 | 0.22 | 2330 | 57.6 |
| A0 dilution 2.2, 2 loop volumes | 0.47 | 2.7 [0.46–86] | 0.18 | 0.21 | 3040 | 57.6 |
| A0 accumulation 10 min | 0.43 | 2.6 [0.46–86] | 0.19 | 0.21 | 3980 | 52.6 |
| A1 (pre-electrolysis) | 0.40 | 1.9 [0.38–54] | 0.25 | 0.28 | 2330 | 57.6 |
| A1, 3 mM | 0.40 | 1.9 [0.38–57] | 0.26 | 0.28 | 6810 | 57.6 |
| A0 L6+L7 | 0.15 | 1.1 [0.29–6.7] | 0.36 | 0.43 | 794 | 57.6 |
| A1 L6+L7, 3 mM | 0.15 | 1.1 [0.29–7] | 0.39 | 0.42 | 2330 | 57.6 |
| A0 S4a | 8.3 | 19 [1.8–542] | 0.00 | 0.01 | 2330 | 57.6 |
| A1 S4a | 0.41 | 1.9 [0.39–50] | 0.22 | 0.26 | 2330 | 57.6 |
| A0 S3b, no clean zone | 0.67 | 3.2 [0.51–102] | 0.15 | 0.18 | 2330 | 57.6 |
| A0 C1 | 0.41 | 2.8 [0.61–73] | 0.10 | 0.12 | 2330 | 57.6 |
| A1 + L4, 3 mM | 0.12 | 0.91 [0.19–15] | 0.53 | 0.54 | 6810 | 57.6 |
| REF gen-1 B-bed S0 | 0.85 | 3.4 [0.65–33] | 0.09 | 0.12 | 1040 | 51.5 |
| REF gen-1 B-bed L6+L7 | 0.71 | 2.8 [0.59–23] | 0.11 | 0.15 | 794 | 51.5 |
| B0 S0 | 0.63 | 2.3 [0.52–23] | 0.15 | 0.20 | 1360 | 52.0 |
| B0 SPE-class electrode CV | 0.85 | 3.1 [0.61–30] | 0.12 | 0.15 | 1360 | 52.0 |
| B0 cell-to-cell NSB CV +10 % | 0.85 | 2.9 [0.59–30] | 0.12 | 0.16 | 1360 | 52.0 |
| B1 (pre-electrolysis) | 0.63 | 2.1 [0.49–21] | 0.17 | 0.23 | 1360 | 52.0 |
| B0 L6+L7 | 0.51 | 1.8 [0.45–17] | 0.19 | 0.26 | 1040 | 52.0 |
| B1 L6+L7 | 0.51 | 1.8 [0.45–17] | 0.20 | 0.26 | 1040 | 52.0 |
| B0 bed factor 1 | 0.30 | 1.2 [0.30–7] | 0.33 | 0.42 | 1360 | 52.0 |
| B0 bed factor 10 | 1.95 | 4.3 [0.82–37] | 0.06 | 0.08 | 1360 | 52.0 |
| B0 small bed (0.1 µL, 10 µm) | 0.59 | 2.0 [0.47–20] | 0.12 | 0.23 | 271 | 52.0 |
| B0 S4a | 4.7 | 10 [1.6–88] | 0.01 | 0.01 | 1360 | 52.0 |
| B0 + L4 | 0.23 | 1.0 [0.27–6] | 0.40 | 0.49 | 1360 | 52.0 |
| REF FRC optimum, review parameters | 0.95 | 3.8 [0.64–47] | 0.09 | 0.12 | 1040 | 45.0 |
| C1 side outlet | 0.86 | 3.4 [0.60–37] | 0.11 | 0.15 | 1040 | 45.0 |
| C2 side outlet + non-fouling | 0.64 | 2.4 [0.48–25] | 0.16 | 0.21 | 1040 | 45.0 |
| C2 pre-electrolysis | 0.64 | 2.2 [0.45–24] | 0.18 | 0.23 | 1040 | 45.0 |
| C2 L6+L7 | 0.53 | 1.9 [0.41–18] | 0.20 | 0.26 | 794 | 45.0 |
| C2 acc 15 min, 3 mM | 0.62 | 2.3 [0.46–26] | 0.18 | 0.22 | 1360 | 52.5 |
| C3 repack per run | 0.64 | 2.4 [0.48–24] | 0.16 | 0.22 | 1040 | 41.5 |
| C2 residual label 10⁻² | 0.64 | 2.4 [0.50–26] | 0.15 | 0.20 | 1040 | 45.0 |
| C2 bed factor 10 | 2.0 | 4.7 [0.83–44] | 0.06 | 0.08 | 1040 | 45.0 |
| C2 + L4 | 0.19 | 0.94 [0.23–7] | 0.43 | 0.53 | 1040 | 45.0 |

The reference rows reproduce `results/design/final_designs.md` (P-chamb 3.5 / 0.16, L6 + L7 1.3 / 0.32, B-bed 3.4 /
0.09, S-chamb 3.0 / 0.13), which checks the copy and the call path.

**Model limitations that apply to all three (docs/09 §5.4) and their net direction:**

| §5.4 item | A | B | C |
|---|---|---|---|
| 1 chamber element (mixing, dilution, wall adsorption) | approximated; wall adsorption worse | n/a (recirculation as Q_eq) | n/a |
| 2 beads in a chip | drag 0.90 vs 0.86 (better) | n/a | n/a |
| 3 single-WE stopped detector | conversion neutral; EC noise ×2.3 (slightly worse) | same | n/a (IDA chip exists; finger length optimistic) |
| 4 on-board conjugate | neutral | neutral | neutral |
| 5 decoupled flows | neutral | recirculation ≈ neutral | neutral |
| 6 zone-resolved NSB | walls outside product path (better, approximated) | bed-channel walls (worse ≤ ×1.4) | bed-channel walls (worse ≤ ×1.2) |
| 7 storage terms | 8-h liquid stores (worse, unknown) | dried reagents (worse, unknown) | daily pack (worse, unknown) |
| 8 multi-run / residual | residual beads (worse unless ≤ 10⁻⁴) | n/a | **residual analyte after glycine (worse, possibly fatal)**; capacity drift |
| 9 cartridge-to-cartridge electrode | cancelled by exhaustive read (better) | shown both ways | permanent (better) |
| 11 temperature | thermostatted (better) | better | better |
| 12 wash efficiency / NSB reversibility | relies on rinses + drag (unquantified) | relies on in-flow washes | relies on in-flow washes |

Net: the unmodelled effects push **A and B down modestly**, and **C down possibly decisively** (residual analyte).
None of the candidates is favoured by an effect the model omits, except the electrode-variation cancellation of the
exhaustive read and temperature control, which help all three.

---

## 9. Decisions for the user at the checkpoint

1. **Which candidate goes to detailed design** (recommendation §10: A, with B as the documented fallback; C not
   pursued). Alternative: postpone any cartridge spend until G1a/G1 (docs/06 §4.11) — none of the three changes the
   G1 rule's inputs (U1, U3, E1.5); all three fail with gen-1 if U1 fails (S1), and under S4a unless
   pre-electrolysis works (A0 S4a P 0.00 → A1 0.22).
2. **Accept that the cartridge is not justified by LOD.** The best as-specified gain (A0, +0.04 in P) is below the
   decision-grade threshold; A1's +0.09 comes mostly from pre-electrolysis, which gen-1 can also have. The case for a
   cartridge is automation, reagent use (wash buffer ≈ 0.8 vs 4.3 mL per determination), throughput (27.5 vs 56 min per sample
   with one chamber) and a two-compartment layout that makes L4 (immune-complex transfer) cheap to add later.
3. **Pre-electrolysis on gen-1 now?** Add a flow-through coulometric guard cell on the substrate line (porous
   graphite, `hw.flow_cells.thermo_6011rs_coulometric.collection_efficiency` 0.95, min flow 300 µL/min) or an in-trap
   variant, and a bench test (risk A5's spiked-HQ arm) in Stage 1/2. This is a docs/06 change the user must approve.
4. **Move HQDP off the BSM** (B1 spare) into a cooled on-card (A) or dock (B, C) store, relying on pre-electrolysis
   and a ≤ 8-h store (Pi growth ≤ 0.06 µM, §2.3).
5. **On-board liquid reagents for one 8-h block** (A: beads, conjugate, HQDP on the card, cooled) vs dried reagents
   (B). The user fixed on-board reagents; docs/11 §4 suggested keeping the bead stock in a dock vial — A puts it on
   the card; confirm.
6. **Calibration policy**: lot calibration + 3 QC determinations per 16-run cartridge (A, B), relying on
   exhaustive-read area cancellation (untested), versus a per-cartridge curve (≈ 6–7 of 16 determinations).
7. **Bench mock-up programme before any mould** (A1–A5; B1 if B stays as fallback): order and timing relative to
   Stage 1 (it needs no Waters hardware; it competes for the same bench time as E1.x).
8. **Model extensions**: whether docs/09 §5.4 items 1 (chamber), 2 (beads in a chip), 3 (stopped single-WE detector),
   6 (zones) and 8 (residual beads) are built — `src/` changes under the model task's rules — before tooling.
9. **Second potentiostat channel**: not needed by A or B; needed only by C (or by an IDA option).

---

## 10. Recommendation

**Recommended: candidate A (multi-run bead-transfer cartridge, one 8-h block, single WE stopped and exhaustive, two
staggered chambers), with B as the documented fallback if A's carry-over or bead-handling risks fail. C is not
recommended.**

Reasoning, including where the honest answer is unfavourable:

* **No candidate is predicted to beat gen-1 on LOD by a decision-grade margin as specified.** A0 is +0.04 in P (2.3
  vs 3.5 pg/mL median), B0 −0.01, C2 0.00 — all within the ±0.05 that docs/08 W7 calls not decision-grade. The chip's
  own physical advantages (less dilution ×1.21, 5 more minutes of accumulation, a clean readout zone) are real but
  small, because gen-1's blank is already 92 % bead NSB and the cartridge does not change the bead NSB per specific
  signal.
* **A is the only candidate that keeps the one-step format**, which is the format that profits from a screened
  detection reagent (A + L6 + L7: P 0.39 vs gen-1 0.32; B and C stay at 0.20 because in-flow sequential labelling
  labels only 0.5–1.7 % of the captured analyte). If U2/E1.5 finds a reagent with on-bead t½ ≥ 30 min, A is the best
  platform in the model; if not, A can run sequentially from the same stores (as gen-1's S-chamb, P 0.13).
* **The largest modelled gain is pre-electrolysis** (A1 P 0.25; and it removes the S4a kill: 19 → 1.9 pg/mL). It is
  a derivation resting on an assumed 1 % unelectrolysed volume and is untested; and **it is portable to gen-1** as a
  guard cell. It should be tested first, on the bench, independent of any cartridge (decision 3).
* **A follows the best-evidenced low-background pattern** (separate binding and signal compartments, move beads not
  liquid: Herrmann2007, Rusling, Wang2013) and makes **carry-over measurable in every run** (PE2) — the property
  that a multi-run cartridge most needs, because its 10⁻⁴ criterion has no precedent for reusable immunoassay
  channels (docs/10 §8).
* **B is the safest on carry-over and valve endurance** (single use) and has the strongest format precedent, but it
  inherits the gen-1 backup's weakness: everything rests on the packed-bed NSB factor (P 0.33 at 1, 0.06 at 10), it
  gains little from reagent screening, and it has the highest consumable cost and dock complexity. It becomes the
  better choice if B1 (bed NSB factor ≤ 1–2) and B2 (cell CV ≤ 10 %) come back favourable while A1 (residual beads)
  fails.
* **C is not recommended**: weakest evidence (≤ 51 regeneration cycles on chip, none for a sandwich IgG), a carry-over
  path the model does not even represent (92 % elution would mean 8×10⁻² carry-over), ≈ 20× the published valve
  endurance, and no gain from reagent screening. Its only advantages are the lowest cost per run and the shortest
  time to result.
* **My judgement below the model**: the real-world probability of reaching 1 pg/mL with A is about the gen-1
  figure of docs/08 §10.4 (≈ 10 % today, ≈ 30 % if U1–U3 are favourable), perhaps a few points higher if
  pre-electrolysis works — not more, because every unmodelled chip effect except the electrode-area cancellation
  points the wrong way (§8).

**Order of work if the user accepts A:** (1) G1a/G1 as planned (cartridge spend only after GO or GO-WITH-LEVER);
(2) pre-electrolysis bench test (A5 spiked-HQ arm) in parallel with Stage 1, because it pays off for gen-1 too;
(3) A1–A4 on milled/laminated mock-ups with a catalogue Micrux die; (4) model extensions §5.4 items 1, 2, 3, 6, 8;
(5) mould tooling only after A1 (residual beads ≤ 10⁻⁴) and A4 (valve endurance) pass.

---

## Appendix A — compact run script (scratchpad, not in the repository)

```python
# run from a COPY of the repository; sys.path -> copy/scripts and copy/src
import json; from dataclasses import replace
import design_lib as L, final_designs as F
ps0 = L.load_ps()
REF = {k: (a, pm, f) for k, a, pm, f in F.designs(ps0, "review")}
STIR = "ma.capture.in_vial_unstirred_rate_factor"; IMP = "ma.chemistries.alp_hqdp.free_product_impurity"
stir = lambda dil: (lambda p: L.with_bounds(p, STIR, value=1/dil, low=0.2/dil, high=1/dil))
def pre_el(p):                      # pre-electrolysis: impurity x 0.01
    if IMP in p.pinned: return p.with_values({IMP: float(p.values[IMP]) * 0.01})
    return L.with_bounds(p, IMP, value=1e-7, low=1e-9, high=1e-5)
os_rec = json.load(open(L.OUT / "optimum_OS__baseline.json"))["design"]
A = replace(L.base_arch("OS").with_design(**os_rec).with_design(**{
    "ma.timing.in_vial_incubation": 30, "hw.timing.accumulation_time": 15,
    "hw.smfl.loop_flush_volumes_for_transfer": 6.6, "ma.timing.post_sample_wash": 1.5,
    "hw.timing.substrate_fill": 0.5, "ma.timing.bead_flush_and_clean": 2.0, "hw.timing.readout_time": 1.0}),
    detector="thin_layer")
A_ps = lambda p: stir(1.7)(p).with_values({"ma.nsb.surface_factor_tubing": 0.01})
s = L.mc(A, A_ps(ps0), n=2000, lod_scale=1/0.90)              # A0;  A1: pre_el(A_ps(ps0))
fr = json.load(open(L.OUT / "optimum_FRB__baseline.json"))["design"]
B = replace(L.base_arch("FRB").with_design(**fr).with_design(**{
    "hw.reactors.packed_microbed_10uL.bed_volume": 0.5, "hw.reactors.packed_microbed_10uL.bead_diameter": 50,
    "ma.geometry.packed_bed_column_inner_diameter": 0.5, "hw.timing.sample_load_flow": 6,
    "hw.smfl.loop_flush_volumes_for_transfer": 1.5, "ma.geometry.reactor_connection_length": 0.002,
    "chem.antibodies.conc_detection_antibody_typical": 1e-9, "ma.delivery.conjugate_injection_volume": 20,
    "hw.timing.conjugate_stopped_flow_incubation": 3, "hw.timing.accumulation_time": 15,
    "hw.timing.readout_time": 1, "ma.readout.sweep_flow": 10,
    "hw.timing.regeneration_and_reequilibration": 1.0}), detector="thin_layer")
B_ps = lambda p: p.with_values({"chem.regeneration.residual_label_carryover_fraction": 1e-6,
    "chem.regeneration.activity_loss_per_cycle": 0.0, "ma.chemistries.alp_hqdp.substrate_concentration": 3e-3})
s = L.mc(B, B_ps(ps0), n=2000, lod_scale=0.996/0.90)          # B0
fc = json.load(open(L.OUT / "optimum_FRC__baseline.json"))["design"]
C = L.base_arch("FRC").with_design(**fc)
C_ps = lambda p: L.with_bounds(L.with_bounds(p.with_values({"ma.nsb.surface_factor_chip": 0.01}),
    "ma.noise.electrode_sensitivity_cv_fouling", value=0.02, low=0.005, high=0.05),
    "ma.reuse.electrode_sensitivity_loss_per_cycle_fouling", value=0.001, low=0.0, high=0.005)
s = L.mc(C, C_ps(ps0), n=2000)                                 # C2
# scenarios: F.scen("L6+L7")[1], F.scen("S4a")[1], ...; L4: L.l4_transfer(ps) applied first
```
