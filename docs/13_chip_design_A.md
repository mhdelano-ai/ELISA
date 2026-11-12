# 13 — Cartridge A: detailed concept design (multi-run bead-transfer cartridge)

Status: 2026-11-12, first complete pass after the user checkpoint of docs/12 §9. Inputs: docs/00, 02, 06, 07, 09, 10,
11, 12; `params/*.yaml`; `automation/`. This document changes no earlier document, parameter or code. The
nearest-model estimates quoted here were run on a **scratch copy** of the repository outside it (method of docs/12 §8
and Appendix A; script in Appendix A of this document); no file in the repository was generated or modified.

**User decisions this design rests on (checkpoint of docs/12 §9).** Candidate A goes to detailed design; decisions
rest on the nearest-model estimates of docs/12 (no extension of `src/` or `params/`); reagent placement is compared in
two variants — **V1**: beads, conjugate and HQDP all liquid on the card, cooled by the dock; **V2**: conjugate and
substrate on the card, bead stock in a cooled stirred vial in the dock, metered by a syringe pump — and one is
recommended (§5); pre-electrolysis of the substrate fill is part of the cartridge but **UNVERIFIED** until the gen-1
bench test docs/06 E1.2b reports (weeks 5–7, docs/06 §10).

**Sourcing conventions** (as docs/12). Every number names its source: repository section (`docs/09 §2.2 F8`),
parameter key (`ma.capture.bead_dose_cv`), or a literature/vendor key already cited with DOI/URL in docs/10 or docs/11
(Wang2013 = doi:10.1039/c3an01166f; CS_1367, CS_EXPLAINED, … = docs/11 §9). **Derived** = calculated here, arithmetic
shown. **[assessment]** = engineering judgement. **UNVERIFIED** = not traceable to a checked source (this includes
every physical constant I use that is not in the repository, e.g. the magnetic moment of an M-280 bead, the
double-layer capacitance of thin-film gold, NdFeB remanence). **Nearest-model estimate** = output of the existing model
on an existing architecture with stated overrides (docs/12 §8); it is not a prediction of the cartridge.

---

## 1. Design summary and what changed from docs/12

### 1.1 The design in one paragraph

A 75.5 × 50 mm, 6 mm thick injection-moulded COC card (double-slide footprint, CS_EXPLAINED; thickness custom) with a
140 µm COC foil floor (magnet and Peltier side), a laminated TPE valve membrane and a top frame, and a 10 × 6 mm glass
thin-film electrode die bonded face-down into a top pocket. Two stirred 176 µL incubation chambers (IC1, IC2) receive
the SM-FL plug (1.5 loop volumes) through on-card valves; beads (V2: from a cooled, rocked dock vial through a
face-seal port) and conjugate (on-card cooled tank, fill-to-vent 10.0 µL meter) are dosed into the chamber just before
injection; after a 30-min one-step incubation with tangential-jet tidal mixing, a dock magnet carriage collects the
beads, gathers them to the chamber throat, the chamber is drained, rinsed twice and refilled with clean buffer, and a small high-gradient magnet
**drags the pellet at 0.20 mm/s through a 20 mm buffer-filled wash lane into a 1.0 µL, 0.20 mm high readout chamber
(RC)** whose ceiling is the working electrode (WE1, 2.5 × 1.9 mm). The RC was filled with HQDP substrate and
pre-electrolysed before the beads arrive, and its residual activity was measured (carry-over monitor). Accumulation
15 min, sealed, at open circuit; readout by a **double potential step** (background-subtracted exhaustive
chronocoulometry). A second electrode WE2 in a 50 µm flow channel downstream of the RC is a built-in fallback read
mode (gen-1-type swept read). Beads leave to an on-card bead-waste pocket held by a fixed dock magnet. Cadence 31.0
min per sample (two chambers staggered), result 58.0 min after Inject Start, 16 determinations per cartridge (≈ 8.3 h).
The BSM flushes the loop and inlet line to a bypass after every transfer, then Loop Offline (carry-over, §3.1).

### 1.2 Changes from docs/12 candidate A, with reasons

| # | docs/12 (§3) | docs/13 | Reason |
|---|---|---|---|
| D1 | RC 4 × 10 mm × 50 µm = 2 µL; WE 37 mm² | **RC 2.6 × 2.0 mm × 0.20 mm = 1.04 µL; WE1 2.5 × 1.9 mm = 4.75 mm²**; 3 mM HQDP | A step read on a 37 mm² WE carries a double-layer charge of ≈ 2.6 µC against a 1.5 nC signal at 1 pg/mL (§3.5.4, Derived): the subtraction would need a repeatability of 2×10⁻⁵. Cutting the area 7.8× (thicker layer, half the volume) and the step height (0.35 → 0.15 V) lowers the charge to ≈ 0.14 µC (needed repeatability 3.5×10⁻⁴). Exhaustive collection is kept: τ = 18 s, 90-s steps collect 99.5 % (§3.5.2). The model is neutral to the volume change (P 0.26 at 1 and 2 µL, 3 mM; ULOQ 3040 vs 6810 pg/mL; §3.5.6) |
| D2 | single step read; background "measured on the same fill" by PE1 | **double-step read** (E_rest → E_det 90 s, back 15 s, E_det 90 s again) with Q_net = Q_a − Q_b; E_rest instead of open circuit before each step | the charging and oxide charge of the second step cancels that of the first on the same electrode within 2 min; PE1 happens 25 min earlier from an undefined open-circuit potential and cannot cancel it [assessment] |
| D3 | no fallback read mode | **WE2 thin-layer flow detector (1.0 × 3.0 mm channel, 50 µm) downstream of the RC on the same die** | if the double-step background (mock-up M5, §10.3) fails, the RC contents are swept at 10 µL/min over WE2 held at constant potential — the gen-1 readout that the model actually represents (thin-layer conversion 0.78 at 10 µL/min, docs/09 §5.2) — without a new die |
| D4 | CE and RE at the end of a dead-end 2 mm × 0.1 × 0.05 mm side channel (R = 250 kΩ) | **CE/RE in a 0.024 µL pocket behind a 0.2 × 0.2 × 0.5 mm neck, flushed at every fill through its own valve**; R_u ≈ 12 kΩ | a dead-end branch accumulates CE reaction products over 20 runs next to the reference; R_u·C_dl = 250 kΩ × 7.4 µF = 1.9 s would have overlapped the 1.1-s thin-layer collection (Derived, §3.5.5) |
| D5 | collection magnets M1a/M1b + drag carriage M2 | **one carriage with a collection magnet (10 × 10 × 5 mm) and a drag magnet (2 × 2 × 4 mm), plus a fixed-position hold magnet under the RC and a permanent magnet under the bead-waste pocket** | field arithmetic §3.3: a block that collects from 3.7 mm height in seconds cannot drag a pellet precisely, and a small magnet with ≈ 350 T/m lateral gradient cannot collect from the far wall of an 8 mm chamber |
| D6 | gates G1–G4 (type unspecified) | **flat-floor gates, actuated from the top through the TPE membrane** | the magnet path runs under the foil floor, so the gate plungers cannot be there; a flat floor has no seat ridge for beads to catch on (docs/10 §7: no data on bead trapping at seats) |
| D7 | V1 placement (beads on the card, tidal-resuspended tank) | **V2 recommended** (§5): bead stock in a cooled, rocked dock vial, metered by a Cavro/PSD-class pump | removes the least-evidenced element (on-board liquid bead suspension; docs/10 §9.3, §6.1) and the shelf-storage bead cake; reuses gen-1's reservoir and its E2.2 dose-CV data; −3 card valves and one pressure channel |
| D8 | HQDP tank 2 mL at 4–8 °C | **HQDP tank 1.5 mL in the 25 °C assay zone during use** (cold only in storage) | 8 h at 25 °C makes ≤ 0.17 µM Pi at 3 mM even at the acceptance-limit k_h (§5.3), and the HQ formed is removed by pre-electrolysis; filling a 0.2 mm RC with 4 °C liquid that warms to 25 °C invites bubble nucleation [assessment; gas solubility values not in the repository, UNVERIFIED] |
| D9 | 21 valves; 7 actuations per run for the tidal valves | **16 membrane valves + 4 gates = 20**; tidal mixing by dedicated dock syringes behind floor-port valves that stay open during incubation | busiest valve 2 cycles per run, **40 per cartridge** (60 in the fallback read mode), ≈ 360 in total (§4) vs 70 / 520 in docs/12 — inside the only thermoplastic endurance figure (> 50, CHILDERS2024) |
| D10 | bead pellet in a 1 × 1 mm pocket at the RC end; beads to a 16-dose bead-waste pocket | pellet held under WE1 by the hold magnet; **bead-waste pocket flushed every run** through its own valve; beads held there by a fixed magnet | product made by spent beads in a stagnant pocket would otherwise leak back into the RC when G4 opens (§3.8) |
| D11 | cadence 27.5 min; result 54.0 min | **cadence 31.0 min; result 58.0 min** | double-step reads (3.25 min each), 90-s steps, gather step and 2.0-min drag lengthen the transfer and RC occupancy (29.75 min of every 31, §7.1); still ≤ 60 min (docs/00); 16 samples ≈ 8.3 h |
| D12 | — | RS/RCj **factory-filled only if shelf-life data allow**; default: filled by the dock at insertion from dock bottles | at the acceptance-limit k_h a factory-filled 3 mM HQDP reaches the 1 µM Pi limit in 1.9 days (docs/12 §2.3, Derived again §5.3); no conjugate data beyond 24 h (docs/06 E1.3) |
| D13 | the 10 % plug tail goes to the bypass | **BSM keeps 100 µL/min to the bypass for 2 more min (3.5 loop volumes in all), then Loop Offline** | without it the inlet line holds loop-tail liquid that would carry ≈ 7×10⁻³ of a sample into the next chamber (§3.1, Derived) |

**What did not change:** chemistry, antibody pair and doses of docs/05 §4.1 (5×10⁵ beads, 0.3 nM conjugate in the
chamber, HQDP pH 9.5); one-step format with sequential mode possible from the same stores; Waters interface of docs/12
§2.1 (BSM delivers only A1, parked at 1 µL/min to a bypass; Inject Start contact closure); lifetime one 8-h block;
16 determinations (13 samples + 2 blanks + 1 control) per card.

### 1.3 Nearest-model estimates for this design (scratch copy, n = 2000, seed 20261111)

Base = docs/12 run "A1" (P-chamb optimum with the chamber, accumulation and timing overrides of docs/12 §8,
pre-electrolysis credit ×0.01, `lod_scale` 1/0.90) with `ma.chemistries.alp_hqdp.substrate_concentration` 3 mM and
`ma.geometry.magnetic_trap_volume` = 1.0 µL (the RC volume of D1). The read-mode change (D2/D3) and the step-read
background are **not** represented by the model; the noise rows show how sensitive P is to them.

| Run | Nominal LOD | Median [5–95 %] (pg/mL) | P(success) | ULOQ nominal (pg/mL) |
|---|---|---|---|---|
| docs/12 A1, 3 mM, RC 2 µL (reproduced) | 0.40 | 1.91 [0.38–57] | 0.26 | 6810 |
| **docs/13 A, 3 mM, RC 1 µL** | 0.40 | **1.88 [0.37–54]** | **0.26** | 3040 |
| same, 1 mM | 0.40 | 1.83 [0.37–53] | 0.23 | 1360 |
| same, 3 mM, after U1–U3 screening (L6 + L7) | 0.15 | 1.12 [0.28–7] | 0.37 | 1040 |
| same, 3 mM, S4a (free HQ 10⁻³ before pre-electrolysis) | 0.41 | 1.95 [0.41–51] | 0.22 | 3040 |
| bead dose CV pinned 0.05 (V2 target, docs/06 E2.2) | 0.40 | 1.72 [0.37–40] | 0.26 | 3040 |
| bead dose CV pinned 0.10 | 0.49 | 2.11 [0.42–50] | 0.20 | 3040 |
| bead dose CV pinned 0.15 | 0.61 | 2.60 [0.47–62] | 0.17 | 3040 |
| bead transfer (`ma.capture.magnetic_trap_efficiency`) pinned 0.80 | 0.40 | 1.81 [0.37–47] | 0.25 | 3040 |
| EC noise `hw.gamry.noise_rms_flow` pinned 20 pA (≈ 0.11 nC charge SD) | 0.58 | 2.34 [0.47–53] | 0.17 | 3040 |
| EC noise pinned 100 pA (≈ 0.55 nC charge SD) | 2.19 | 5.88 [0.92–123] | 0.05 | 3040 |

Reading (Derived from the rows): (i) halving the RC volume is LOD-neutral and keeps ULOQ ≥ 1000 pg/mL only at 3 mM —
**3 mM HQDP is now a requirement, not an option**; (ii) the bead-dose CV is the reagent-placement parameter the model
does see: CV 0.05 → 0.10 costs 0.06 in P (decision-relevant for V1 vs V2, §5); (iii) bead loss in the transfer barely
matters for the LOD (NSB is carried by the beads too) — it matters for carry-over (§3.3.5); (iv) **the read
background is a first-order risk**: a charge SD of 0.11 nC (equivalent noise, mapping in §3.5.4) already costs 0.09
in P. Charge-equivalent mapping: the model integrates white noise as σ_Q = i_rms × √(T/2B) (param note of
`ma.noise` bandwidth, T = `hw.timing.readout_time` 60 s, B ≈ 1 Hz) → 3 pA ↔ 0.016 nC, 20 pA ↔ 0.11 nC, 100 pA ↔
0.55 nC (Derived).

---

## 2. Layer stack and layout

### 2.1 Card format and layer stack

| Layer | Material / thickness | Function | Source / reasoning |
|---|---|---|---|
| L0 floor foil | COC foil 140 µm (100 µm Topas option), thermally or solvent bonded | floor of every chamber, channel and tank; magnet-side wall (beads sit on it); Peltier contact face | 140 µm COC lid (DARWIN_CS4CH), 100 µm Topas foil (CS_1367); requirement ≤ 0.5 mm (docs/09 F8) |
| L1 body | COC (Topas class), injection-moulded, **6.0 mm**; chambers and tanks open to the bottom; channels as grooves in the bottom face; valve windows and die pocket from the top | all fluidics | moulding of COC/COP, MOQ 100, ISO 7 (CS_FAB); body ≥ 3–5 mm for 250 µL chambers (docs/11 §0); 6 mm is outside the 2 mm catalogue double slide (CS_EXPLAINED) → custom mould [assessment] |
| L2 membrane | TPE sheet 0.3–0.5 mm (thickness UNVERIFIED), laminated over the valve and gate windows | membrane valves V1–V16 and gates G1–G4, pressed down by dock plungers | ChipShop moulds TPE and bonds multi-layer stacks (CS_FAB); principle of the mechanically closed membrane-valve chip (CS_1367); TPE–COC bond under cycling UNVERIFIED |
| L2b vents | PTFE membrane discs (Ø 4 mm), heat-staked | IC1/IC2 headspace vents, conjugate-meter stop vent, RS/RCj tank vents | hydrophobic vent required for a chamber filled while closed (docs/09 F1); wet-out by Tween/BSA buffers UNVERIFIED (§9) |
| L3 frame | COC 1.5 mm, ultrasonic- or laser-welded | holds L2 down at the valve rims; plunger windows; locating holes; die retention | [assessment]; laser welding offered by Goodfellow (GOODFELLOW_MF), process for COC UNVERIFIED |
| D electrode die | borosilicate glass, 10.0 × 6.0 mm (thickness to foundry standard, UNVERIFIED), Au 150 nm on 50 nm Ti (Pt option), SU-8 or polyimide passivation; WE1, WE2, CE, RE, contact-check loop; pads on the part of the die outside the wetted area | RC ceiling and flow-detector ceiling | Micrux custom thin-film (Au/Pt 150 ± 15 nm, ≥ 5 µm, SU-8/PI; MICRUX_TF); IMT (≥ 2 µm; IMT_FLYER); 10 × 6 mm is the Micrux die support size (PALMSENS_IDA) |
| die bond | UV-curing or thermal adhesive bead outside the wetted footprint, plus the RC web as a mechanical stop | sets the RC height | adhesive leachables and HQ/BQ sorption UNVERIFIED (docs/11 §6.2) |

Card outline: 75.5 × 50.0 mm (double-slide footprint, CS_EXPLAINED), 6.0 + 0.14 + 0.5 + 1.5 ≈ **8.1 mm** total.
Coordinates below: origin at the lower-left corner seen **from the top** (die side), x along 75.5 mm, y along 50 mm.
Zones: **reagent zone** x = 0–20 mm (4–8 °C), **thermal break** x = 20–24 mm (through-slot in L1 except two 3 mm
bridges carrying channels), **assay zone** x = 24–75.5 mm (25.0 ± 0.2 °C, docs/07 §5.1 / docs/12 §2.5). The die and
pogo-pin area (x = 55–70 mm) lies entirely in the assay zone, ≥ 35 mm from the cold zone (dew-point reason, §6.6).

### 2.2 Plan view (top view, die side; not to scale; coordinates in mm)

```
 y=50 +------------------------------------------------------------------------------------------------+
      |  REAGENT ZONE 4-8 C   ||                    ASSAY ZONE 25.0 C                                     |
      |                       ||        P_in(40,46)o--[V1]--.          P_byp(48,46)o<--[V3]--+            |
      |  RCj conj tank        ||                            |                               |            |
      |  (2-12, 34-44)  P_c o ||   [V2]---------------------+-------------------------------'            |
      |   |vent               ||    |      P_b(28,40)o--+--[V4]--.                                        |
      |  [V8]                 ||    |                   '--[V5]-------.                                    |
      |   |                   ||    |   .---------.  G1                |                                   |
      |  MC 10.0 uL (14,30)---========>| IC1 (34,32)|==]=== WL1 ======.  |      DIE 10 x 6 (pocket 56-66, 21-27)|
      |   stop vent P_mv o    ||  [V6] | d 8, 5 deep|               \\ |     +-----------------------------+   |
      |                       ||    |  '---o-----'                 \\|     | RC 2.6x2.0x0.20 (60.0,24.0) |   |
      |                       ||    |   P_d1(30,27)[V9]   P_w(52,28)o-[V11]-J(52,24)=G3=[RC]=G4=>BW(68,24)  |
      |                       ||    |   .---------.             //  |  WL out [V12]->P_wo(52,20)  |  [V16]   |
      |                       ||    '>| IC2 (34,16)|==]=== WL2 ===='   |  RS-[V13]-> RC  RC-[V14]->WE2->P_s  |
      |                       ||  [V7] | d 8, 5 deep| G2               |  CE/RE branch -[V15]-> P_s(70,30)    |
      |                       ||       '---o-----'                     +-----------------------------+   |
      |                       ||   P_d2(30,11)[V10]           RS HQDP tank 1.5 mL (40-60, 3-9), vented      |
 y=0  +------------------------------------------------------------------------------------------------+
     x=0                    x=20-24                                                                  x=75.5
  ==  wash lane (magnet path, beads move, liquid still)      o  face-seal port (1.4 mm through-hole)
  [Vn] membrane valve (spring-closed in the dock)            G1-G4 flat-floor gates (top-actuated)
```

### 2.3 Feature table

Volumes Derived from the listed dimensions (V = L × W × D; cylinder V = π r² D). "Floor" = L0 foil.

| ID | Feature | Centre (x, y) mm | Footprint | Depth / height | Volume | Notes |
|---|---|---|---|---|---|---|
| IC1, IC2 | incubation chambers | (34, 32), (34, 16) | Ø 8.0 mm, cylindrical, floor = foil; throat taper on the +x side from Ø 8 to 0.5 mm over 3 mm | 5.0 mm | **251 µL total**, 170 µL working (fill height 3.4 mm) | docs/12 §3.3; wetted area at 170 µL: floor 50.3 + wall π·8·3.4 = 85.4 → **136 mm²** |
| P_d1, P_d2 | tidal / drain / rinse floor ports | (30, 27), (30, 11) | nozzle 0.5 × 0.5 mm entering IC tangentially at floor level, opposite the throat | 0.5 mm | channel 0.5 × 0.5 × 6 mm = 1.5 µL each | tangential jet → swirl (§3.2.2) |
| TS1, TS2 | tidal buffer serpentines (dock side of V9/V10) | under IC ports, y-offset 4 mm | 0.8 × 0.5 mm × 150 mm | 0.5 mm | **60 µL** each | holds the 50 µL aspirated stroke on the card (docs/12 §3.3) |
| WL1, WL2 | wash-lane branches IC throat → J | (39.5,31)→(52,24); (39.5,17)→(52,24) | 0.5 mm wide, 14.3 mm long each | 0.20 mm | 1.43 µL each | foil floor; bends with ≥ 3 mm radius (magnet must follow) |
| WLc | common lane J → G3 | (52,24)→(57.5,24) | 0.5 × 5.5 mm | 0.20 mm | 0.55 µL | total drag path IC throat → RC centre ≈ **20.3 mm** |
| RC | readout chamber | (60.0, 24.0) | 2.6 × 2.0 mm | **0.20 mm** (thin web under the die, tolerance ±0.02 mm UNVERIFIED) | **1.04 µL** | floor = foil; ceiling = die; WE1 covers 91 % of the ceiling |
| WE1 | working electrode | over RC | 2.5 × 1.9 mm = 4.75 mm² | — | — | Au (Pt option) |
| RC inlet/outlet | G3 side and G4 side lanes | x 57.5–58.7 and 61.3–62.5 | 0.5 mm wide | 0.20 mm | 0.12 µL each | |
| SF | substrate feed channel RS → V13 → RC (side entry, −y) | RC −y side | 0.3 × 4 mm | 0.20 mm | 0.24 µL | |
| WE2 channel | flow detector downstream of RC via V14 | (63.5, 25.5) | 1.0 × 3.0 mm, WE2 1.0 × 2.0 mm | **50 µm** (moulded boss) | 0.15 µL | fallback read (D3); conversion not computed for this geometry |
| CER | CE/RE neck + pocket | from the RC +y edge | neck 0.2 × 0.2 × 0.5 mm; pocket 0.6 × 0.4 mm with CE (0.4 × 0.3 mm) and RE (0.15 × 0.15 mm) pads on the die | neck 0.20, pocket 0.10 mm | 0.02 + 0.024 = 0.044 µL | outlet via V15 to P_s; flushed every fill (§3.5.5) |
| BW | bead-waste pocket | (68, 24) | 2.0 × 2.0 mm | 0.5 mm | 2.0 µL | fixed dock magnet below; flushed via V16 |
| RCj | conjugate tank | (7, 39) | 10 × 10 mm | 5.0 mm | 0.50 mL (0.30 mL fill) | reagent zone; PTFE vent; dock pressure port P_c |
| MC | conjugate meter | (14, 30) | 2.0 × 1.0 × 5.0 mm cavity | 1.0 mm | **10.0 µL** | fill-to-vent (PTFE stop at the far end, vent port P_mv) |
| RS | HQDP tank | (50, 6) | 20 × 15 mm | 5.0 mm | 1.5 mL (1.2 mL fill) | assay zone (D8); PTFE vent |
| manifold M_in | sample inlet manifold P_in → V1/V2/V3 | (40, 40) | 0.5 mm wide, 22 mm total | 0.30 mm | 3.3 µL | |
| bead manifold | P_b → V4/V5 → IC1/IC2 | (28, 40) | 0.4 mm wide, 10 mm to each valve + 8 mm to IC | 0.30 mm | 1.2 + 1.0 µL | V2 only |
| conj line | MC → V6/V7 → IC1/IC2 | | 0.3 mm wide, 8 mm each | 0.30 mm | 0.7 µL each | |

### 2.4 Channel cross-sections

```
 wash lane / RC inlet (0.5 x 0.20 mm)       RC (2.6 x 0.20 mm, section through WE1)       WE2 channel (1.0 x 0.05 mm)
      |       L1 COC        |                ===== glass die, WE1 on the underside =====       ===== die, WE2 =====
      |____        _________|                |##|=====================================|##|      |##|___________|##| <- boss
          |  0.5  | 0.20                     |##|      liquid 0.20 mm  (1.04 uL)      |##|         liquid 0.05
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~ L0 foil 140 um  ~~~~~~~~~~~ beads on the foil ~~~~~~~~~~~~~~~~      ~~~~~~~~~~~~~~~~~~~~~
          [drag magnet below foil]                     [hold magnet below foil]

 flat-floor gate (closed)                       membrane valve V (closed; seat ridge, from the top)
   plunger v                                         plunger v
  ==TPE membrane pushed down into the lane==        ==TPE== pushed onto a 0.2 mm wide seat ridge between two channels
  ~~~~~~~~~~ L0 foil (no ridge) ~~~~~~~~~~
```

Gate seal against a flat foil across a 0.5 × 0.2 mm rectangular lane requires the TPE to conform into the corners;
leak rate UNVERIFIED (gate requirement in §4.2).

### 2.5 Ports (card ↔ dock)

All dock ports are 1.4 mm through-holes with a dock-side flat face seal (internal volume 0.6 µL, CS_EXPLAINED); no
Mini Luer (16.5 µL) in any sample, bead or product path (docs/11 §1.2 assessment). Factory-fill ports are capped
Mini Luer (only on RCj and RS, only if factory fill is used, D12).

| Port | Type | Connects | Dead volume (port + channel to first valve) | Liquid |
|---|---|---|---|---|
| P_in | face seal, 1/16″ PEEK from the SM-FL "to column" outlet (≥ 0.3 m, `hw.tubing.peek_isolation_length_each_side_of_cell`) | M_in → V1/V2/V3 | 0.6 + 1.2 = 1.8 µL | sample + A1 |
| P_byp | face seal | V3 → dock waste | 0.6 + 0.9 µL | A1 (BSM parked flow) |
| P_b | face seal (V2) | dock bead line → V4/V5 | 0.6 + 1.2 µL | bead suspension, chased |
| P_d1, P_d2 | face seal | V9/V10 + serpentines → dock syringes S_IC1, S_IC2 | 0.6 + 1.5 + 60 µL serpentine | IC contents (tidal), A1 rinse |
| P_w | face seal | dock S_RC (A1 position) → V11 → J | 0.6 + 0.3 µL | A1 (WL refresh) |
| P_wo | face seal | V12 → dock waste | 0.6 µL | A1 |
| P_s | face seal | common outlet of V14, V15, V16 → dock S_RC (pull) | 0.6 + 0.5 µL | substrate, product (fallback read) |
| P_c | face seal (gas) | RCj headspace → dock pressure channel | — | air |
| P_mv | face seal (gas) | MC stop-vent → dock pressure/vent | — | air |
| fill ports (2) | Mini Luer, capped (factory fill) **or** face seal (dock fill at insertion, default D12) | RCj, RS | 16.5 µL each (Mini Luer, outside the reagent path after capping) | conjugate, HQDP |

10 dock face seals + 2 fill ports; pogo pins on the die (6 pads: WE1, WE2, CE, RE, contact-loop ×2).

### 2.6 Swept and dead volumes per path segment

| Path | Segments | Swept volume per run | Dead / hold-up volume | Source |
|---|---|---|---|---|
| sample → ICk | SM-FL loop (100 µL) + PEEK 0.3 m × 127 µm ID (3.8 µL, Derived π·(63.5 µm)²·0.3 m) + P_in 0.6 + M_in to Vk 2.4 + Vk → IC 1.2 | **150 µL** of A1 at 100 µL/min (1.5 loop volumes) | 4.2 µL card hold-up, rinsed by the tail of the 150 µL push and by the parked BSM flow to bypass | docs/12 §2.2 (transfer 0.90 at 1.5 loop volumes, docs/09 §1.2) |
| beads → ICk (V2) | dock vial → holding line → P_b → V4/V5 → IC | 10.0 µL bead slug between 2 µL air gaps + ≈ 6 µL A1 push | dock outlet line 2.5 µL + card 0.6 + 1.2 + 1.0 = 5.3 µL ≤ push | Derived (§5.2) |
| conjugate → ICk | RCj → V8 → MC (10.0) → V6/V7 → IC | 10.0 µL, emptied by air | 0.7 µL channel, air-cleared | Derived |
| tidal mixing | ICk ↔ port ↔ TSk | 50 µL every 30 s | 1.5 µL port channel (inside the stroke) | docs/12 §3.3 |
| wash lane | WLk + WLc | 0 during the drag (still liquid); 10 µL A1 refresh per run | 1.43 + 0.55 µL | Derived |
| RC prep (substrate) | RS → V13 → SF → RC → V14 → WE2 → P_s, then RC → V15 → CER → P_s | 20 µL + 5 µL at 30 µL/min | SF 0.24 + RC 1.04 + WE2 0.15 + CER 0.044 | §3.6 |
| RC + BW flush after read | RS → RC → G4 → BW → V16 → P_s | 20 µL | BW 2.0 | §3.8 |
| fallback read (WE2) | RC → V14 → WE2 → P_s | 10 µL at 10 µL/min | WE2 channel 0.15 | gen-1 readout flow (`cycle_primary.yaml` `readout`) |

---
## 3. Functional units

### 3.1 Sample reception and metering of the dispersed plug

* **Volume and flow.** Empower method per line: A1 at 100 µL/min for 1.5 min into ICk (V_k open, V3 closed): 150 µL
  = 1.5 loop volumes, analyte transfer 0.90 (docs/09 §1.2 table; loop ID 0.5 mm UNVERIFIED); the chamber then holds
  150 + 10 (beads) + 6 (A1 push behind the bead slug, §5.2) + 10 (conjugate) = **176 µL**; capture gain vs gen-1
  (0.90/1.76)/(0.96/2.2) = **×1.17** (Derived as docs/12 §2.2, which used 170 µL → ×1.21).
* **Metering is by time × BSM flow**, not by a card meter: 100 µL/min × 1.5 min. BSM accuracy at 100 µL/min is
  assumed 1–3 % (`hw.bsm.flow_accuracy`, low-flow bound a guess) and precision 1 % RSD (`hw.bsm.flow_precision_rsd_low_flow`,
  UNVERIFIED); a 1 % volume error changes the chamber dilution by ≈ 0.9 % and the transfer fraction slightly (both
  identical for calibrators and samples). Gravimetric check of the 150 µL: Stage C1 (§10), as docs/06 S0.6.
* **Hydraulics.** The inlet path (0.5 × 0.3 mm, ≈ 25 mm) has R = 12ηL/(w h³ (1 − 0.63 h/w)) = 12 × 0.89×10⁻³ ×
  0.025 / (5×10⁻⁴ × 2.7×10⁻¹¹ × 0.62) = 3.2×10¹⁰ Pa·s/m³ → **53 Pa at 100 µL/min** (Derived; η from
  `ma` fluid viscosity 0.89 mPa·s). The chamber is vented, so the card adds < 0.1 kPa; the BSM back-pressure question
  at 1–100 µL/min is unchanged from gen-1 (restrictors upstream of the injector, docs/09 §1.2; open bench item docs/08 §10).
* **The 10 % tail and line flush (change D13 from docs/12).** After 1.5 min V_k closes and V3 opens; the BSM keeps
  **100 µL/min for 2.0 more min to the bypass** (200 µL; the loop has then seen 3.5 loop volumes, > 0.997 out, docs/09
  §1.2), then the SM-FL **Loop Offline** event takes the loop out of the path (`hw.smfl.loop_offline_supported`) and the
  BSM parks at 1 µL/min to the bypass. Reason (Derived): without this flush the PEEK line + manifold (3.8 + 2.4 = 6.2 µL)
  would hold loop-tail liquid at ≈ 0.12 C₀ (slope of the transfer curve between 1.5 and 2 loop volumes, (0.96 − 0.90)/50
  µL × 100 µL) when the next sample is injected: 6.2 × 0.12 / 100 = **7×10⁻³ carry-over** into the next chamber — 70×
  the 1×10⁻⁴ criterion. After the flush, the line content is clean A1 for ≥ 26 min (26 µL ≈ 4 line volumes);
  residual liquid-phase carry-over is then < 10⁻⁵ by the same arithmetic (UNVERIFIED for wall-adsorbed IgG). The
  Loop Offline pressure blip (docs/09 §1.3) happens while the RC is sealed. A1 from the BSM per determination:
  150 + 200 + 26 ≈ **0.38 mL**.
* **Adsorption.** Sample-contact area: inlet path ≈ 2 × 25 × (0.5 + 0.3) = 40 mm² + chamber 136 mm². Upper bound
  (Derived): if the chamber walls were a perfect sink, mass transfer k_m ≈ D/δ = 3.9×10⁻¹¹ m²/s (`chem.analyte`
  IgG diffusion coefficient in `params/chemistry.yaml`) / 100 µm = 3.9×10⁻⁷ m/s; k_m·A/V = 3.9×10⁻⁷ × 1.36×10⁻⁴ /
  1.73×10⁻⁷ = 3.1×10⁻⁴ s⁻¹ → 43 % of the analyte lost in 30 min. Real loss on BSA/Tween-blocked COC is far lower but
  **unmeasured** (`chem.analyte.adsorptive_loss_fraction_untreated_tube` 0.5 is for untreated tubes) — measured in mock-up
  M2 (§10) as spike recovery vs a LoBind tube. Same issue in the gen-1 cup; not credited by the model.

### 3.2 Stirred incubation chambers IC1, IC2

**3.2.1 Geometry.** Ø 8.0 × 5.0 mm (251 µL), 176 µL working (fill height 3.5 mm), flat foil floor, PTFE vent in the
roof, tangential floor port P_dk opposite the throat, throat taper Ø 8 → 0.5 mm over 3 mm on the +x side leading into
gate G_k and the wash lane.

**3.2.2 Mixing.** Dock syringe S_ICk (one per chamber, A1 working fluid, 1 mL syringe) behind the open floor valve V9/V10
aspirates 50 µL into the 60 µL on-card serpentine TSk and dispenses it back **every 30 s**, 2 s per half-stroke.
* Jet (Derived): 50 µL / 2 s = 25 µL/s through 0.5 × 0.5 mm → 0.10 m/s; Re = 1000 × 0.10 × 5×10⁻⁴ / 0.89×10⁻³ = **56**;
  the tangential entry sets the chamber swirling about its axis [assessment: swirl lifts beads off the floor; not
  computed].
* Settling between strokes: 7 mm/h (`ma.capture.in_vial_unstirred_rate_factor` note) × 30 s = **58 µm**, i.e. beads
  are re-suspended long before they reach the floor from mid-height (1.7 mm, 15 min).
* Beads that enter the serpentine (0.5 mm deep) need 0.5 mm / 7 mm/h = 4.3 min to settle there, ≫ 30 s (Derived).
* The stroke (50 µL) stays within the 60 µL serpentine, so beads and conjugate never reach dock lines; the A1/sample
  interface in the serpentine is identical in every run (timed), its dilution effect ≤ a few µL [assessment].
* Valves are **not** cycled per stroke (V9/V10 stay open during incubation; D9).
* Capture factor relative to a well-mixed tube: **UNVERIFIED** — the model samples 0.2–1.0 (/1.73); the single most
  important unmeasured chamber property (docs/08 §10.2; docs/12 risk A2). Mock-up M2 measures it (E3.3 analogue).

**3.2.3 Drain.** After collection, S_ICk aspirates the chamber through P_dk at 300 µL/min (≈ 0.6 min for 176 µL) and
dispenses to waste through its selection valve. The port is 8 mm from the pellet (throat side), so flow near the
pellet is negligible [assessment]. Residual after draining: wetted area 136 mm² × film 10–30 µm (UNVERIFIED) = 1.4–4.1
µL + corner meniscus → **≤ 5 µL** design assumption (docs/12 §3.8; gen-1 cup spec ≤ 2 µL, docs/07 §5.1).

**3.2.4 Bubble handling.** Liquids enter at the floor below the meniscus; air leaves through the PTFE vent; A1 comes
from a dock bottle at room temperature into a 25 °C chamber (≈ 3 K warming; small supersaturation) [assessment];
beads and conjugate arrive by air-push or chase into a vented chamber. The vent membrane must not wet out with 0.05 %
Tween + 1 % BSA (UNVERIFIED; §9 FM8).

**3.2.5 Wall area and NSB budget.** Conjugate-exposed IC wall 136 mm² × 0.3 nM × 30 min (docs/12 §3.8) — **not in the
product path**; it enters only through (i) analyte loss (§3.1), (ii) free conjugate carried into the RC (§3.4),
(iii) wall-adsorbed conjugate/analyte desorbing into the next incubation of the same chamber 62 min later (unknown;
cleaning cycle §3.2.6). Beads: 5×10⁵ × π (2.8 µm)² = **12.3 mm²** (docs/12 §3.8), factor 1
(`ma.nsb.surface_factor_magnetic_beads`), exposure 0.3 nM × ≈ 38 min ≈ 11 nM·min — this carries the blank.

**3.2.6 Cleaning** (after the drag, magnet away from the chamber): 3 × (100 µL A1 in at 200 µL/min, 2 tidal strokes,
drain) = 3 × 1.6 min ≈ 5 min. Bead residue after 3 rinses if not stuck: 0.05 × (5/105)³ = **5×10⁻⁶** of a dose
(Derived as docs/12 §3.8 with the ≤ 5 % left after collection). Extra cleaning (6 rinses) after any sample whose
result is > 100 pg/mL (docs/08 S6 alternative), triggered by Python from the result.

### 3.3 Bead capture and magnet-dragged transfer

**3.3.1 Magnets and actuators.**

| Magnet | Size, grade | Position | Motion | Fail-safe |
|---|---|---|---|---|
| M_c collection | NdFeB block 10 × 10 × 5 mm, magnetised through 5 mm, B_r ≈ 1.3 T (N42 class, UNVERIFIED) | on the X–Y carriage, top face 0.16 mm below the foil (bead plane 0.30 mm above the face) | X–Y carriage + Z lift (5 mm) | spring-up (on) at its last x–y position |
| M_d drag | NdFeB 2 × 2 × 4 mm, magnetised along 4 mm, same grade | on the same carriage, 25 mm from M_c | same carriage, Z lift | spring-up |
| M_h hold | NdFeB 3 × 3 × 4 mm (UNVERIFIED size) | fixed under the RC centre | Z lift only (solenoid, spring-up) | spring-up (beads held in the RC) |
| M_w bead-waste | NdFeB 3 × 3 × 3 mm | fixed under BW, never moved | none | permanent |

**3.3.2 Field and force arithmetic (Derived; inputs UNVERIFIED as marked).** Fields were computed by integrating the
equivalent surface charges of a uniformly magnetised block (B_r = 1.3 T) on a 60 × 60 grid (scratch script, Appendix
A). Bead moment: M-280, V = (4/3)π(1.4 µm)³ = 1.15×10⁻¹⁷ m³; magnetisation at saturation assumed **1×10⁴ A/m
(UNVERIFIED; no bead magnetic data in the repository)** → m = 1.15×10⁻¹³ A·m²; in fields ≥ 0.15 T the bead is assumed
saturated (also UNVERIFIED), so F = m ∇|B|. Stokes drag on a free bead: 6πηr = 6π × 0.89×10⁻³ × 1.4×10⁻⁶ = 2.35×10⁻⁸
N·s/m; a bead sliding on the floor is assumed to see **3×** that (wall correction; textbook order of magnitude,
UNVERIFIED). Buoyant weight from the repository settling velocity: 7 mm/h = 1.94 µm/s × 2.35×10⁻⁸ = 0.046 pN (Derived).

| Situation | |B| (T) | gradient (T/m) | Force (pN) | Consequence |
|---|---|---|---|---|
| M_c, bead at the fill surface above the magnet centre (3.7 mm above the face) | 0.18 | 47 (vertical) | 5.4 | v = 5.4 pN / 2.35×10⁻⁸ = 0.23 mm/s → 3.4 mm in **15 s**; with a 10× weaker bead moment 150 s |
| M_c, bead at the chamber wall (x = 4 mm off-centre, top) | 0.16 | 43 vertical, 16 lateral | 4.9 / 1.8 | reaches the floor in < 20 s, then slides toward the field maximum |
| M_c edge, bead on the floor (0.3 mm), "gather" sweep | 0.57 | 64 lateral, 639 vertical | 7.4 lateral | max follow speed 7.4 / (3 × 2.35×10⁻⁸) = 0.10 mm/s → gather at **0.05 mm/s** (2× margin) |
| M_d edge, bead on the floor (0.3 mm) | 0.37 | **350 lateral**, 630 vertical | **40 lateral**, 73 vertical | max follow speed v_max = 40 / (3 × 2.35×10⁻⁸) = **0.57 mm/s**; drag at **0.20 mm/s** = 0.35 v_max (2.8× margin); Wang2013 dragged > 95 % at 0.7 mm/s (bead type not in abstract) |
| M_d edge at 0.5 mm gap | 0.28 | 214 lateral | 25 | v_max 0.35 mm/s — the dock must hold the magnet-to-foil gap ≤ 0.2 mm (§6.2) |

Two consequences: (i) single-bead dragging works only with a small, close, high-gradient magnet — a 10 mm collection
block has 5× less lateral gradient; (ii) the vertical force (73 pN) presses beads onto the foil 1.8× harder than the
lateral force pulls, so **bead–foil friction/adhesion decides whether beads follow at all** (a friction coefficient
> ≈ 0.5 would immobilise single beads; no value exists for blocked COC with Tween) — mock-up M1 measures the follow
speed and the immobile fraction directly. Aggregated pellets carry a larger moment per drag area and follow better
[assessment].

**3.3.3 Sequence and times** (t from Inject Start of the run in ICk):

| t (min) | Action | Motion |
|---|---|---|
| 31.5–33.5 | collection: M_c under ICk with its +x edge under the throat entrance, Z up | carriage moves at 5 mm/s from park (≤ 10 s) |
| 33.5–35.0 | gather: M_c moves +x by 4 mm at 0.05 mm/s (80 s); the floor pellet follows the edge field maximum into the throat taper | X |
| 35.0–38.0 | drain, 2 rinses, third fill stays (§3.4), M_c holding | — |
| 38.0–39.75 | hand-over: M_d moved under the throat (M_c lowered when M_d is in place, 0.25 min), G_k and G3 open; drag 20.3 mm at **0.20 mm/s** (101 s) along WLk, WLc into the RC; M_h up; M_d lowered; G_k, G3 closed | X–Y path following the lane centre line |
| 39.75 | accumulation starts | carriage free for the other chamber |
| 58.0–58.75 | bead-out: M_h down, M_d under the RC, G4 open, drag 6 mm into BW at 0.5 mm/s (12 s), M_w holds them, G4 closed; RC + BW flush (§3.8) | X |

Transfer block 31.5 → 39.75 = **8.25 min** (docs/12: 7.0 min; gen-1 trap loading + wash 7.6 min).

**3.3.4 Bead loss budget (targets, UNVERIFIED until M1).** Collection ≥ 0.99, gather ≥ 0.99, drag ≥ 0.97 (Wang2013 >
0.95 at 3.5× our speed), arrival and hold ≥ 0.995 → **≥ 0.95 overall** (docs/12 assumed 0.90). LOD sensitivity is
small (transfer 0.80 → P 0.25 vs 0.26, §1.3) because the NSB rides on the same beads; the losses matter for
carry-over (§3.3.5).

**3.3.5 Where lost beads go, and carry-over.**
* Not collected / not gathered (in ICk): cleaned out by 3 rinses (5×10⁻⁶ of a dose, §3.2.6).
* Stranded in WLk: the next run's WL refresh (t = −5, §3.4) pushes branch-k liquid into the empty ICk, which is then
  filled for the next sample — **a stranded bead in branch k carries the previous sample's sandwich into the next
  incubation of chamber k**. Stranded in WLc: flushed to waste through V12 at every refresh.
* Requirement (Derived from docs/08 S6): beads carried into the next determination ≤ 10⁻⁴ of a dose, i.e. **≤ 50 beads**
  per run (of 5×10⁵).
* Control: (a) the refresh of branch k flows **from J toward the IC** only before ICk is filled, and the first chamber
  rinse after it removes those beads (3-rinse arithmetic again: < 10⁻⁵); (b) if M1 finds > 50 stranded beads per pass,
  a **second drag pass** (return at 5 mm/s, second pass at 0.2 mm/s, +1.8 min) is added and accumulation is cut to
  13 min (model: 15 → 10 min costs ≈ 0.01 in P, docs/12 §3.9 rows A0 vs "accumulation 10 min"); (c) beads that do not
  follow even the second pass are, by definition, immobile and stay out of the RC — they matter only if they
  later detach; the 10 ng/mL challenge series (§8.3) measures the net effect.
* Beads left in the RC after bead-out: measured every run by PE2 (§3.6).

### 3.4 Wash

* **Chamber rinses** (pellet held by M_c at the throat, 35.0–38.0 min): drain (0.6 min), 2 × (100 µL A1 in at 300
  µL/min, no tidal strokes, drain) and a third 100 µL fill that **stays as the drag medium** (the pellet must be under
  liquid to enter the lane) ≈ 2.6 min. Free conjugate in the drag medium: (105/5)³ = 9261× dilution → 0.3 nM / 9261 =
  0.032 pM × 105 µL = 2.0×10⁶ molecules (docs/12 used two rinses and the 5 µL residual: 2.1×10⁶, same order).
* **Wash lane**: refreshed with 10 µL A1 at t = −5 min (before the chamber is dosed): S_RC → P_w → V11 → J → WLk →
  open G_k → empty ICk (5 µL, then drained by S_ICk), then J → WLc → V12 → waste (5 µL). The pellet then crosses
  20 mm of clean, still A1.
* **Free conjugate carried into the RC**: Wang2013 substrate carry-over with the beads < 2×10⁻⁵ of the source-well
  content (small molecule; protein UNVERIFIED) × 2.0×10⁶ = **≤ 40 molecules**, against ≈ 5700 NSB enzymes in the nominal
  blank (docs/12 "A0") — the two rinses are essential (≈ 1.8×10⁴ without them, docs/12 §3.8).
* Wash minima of docs/09 C11 (post-capture ≥ 1 min, ≥ 50 accumulation-zone volumes): 200 µL of rinse vs a 1.04 µL RC
  = 190 volumes; 3.0 min.

### 3.5 Readout chamber and electrodes

**3.5.1 Geometry and materials.** RC 2.6 × 2.0 × 0.20 mm = 1.04 µL, foil floor, die ceiling; WE1 Au 2.5 × 1.9 mm
(4.75 mm², 91 % of the ceiling), 50 µm rim. **All four sealing points (G3, G4, V13, V14 seats) lie ≤ 0.2 mm from the RC
edge**, so unelectrolysed stubs are ≤ 0.2 × 0.5 × 0.2 mm = 0.02 µL each. CE/RE: a neck 0.2 × 0.2 × 0.5 mm (0.02 µL)
from the RC +y edge into a pocket 0.6 × 0.4 × 0.10 mm (0.024 µL; 0.1 mm moulded step) whose ceiling carries the CE
(Au, 0.4 × 0.3 mm) and the RE pad (0.15 × 0.15 mm, Ag/AgCl if available, else Au); pocket outlet through V15 to P_s,
flushed at every fill (D4). WE2: Au 1.0 × 2.0 mm in a 1.0 × 3.0 × 0.05 mm channel behind V14 (fallback, §3.5.7).
Contact-check loop: two pads joined by a 50 µm Au line (resistance measured at docking). Passivation SU-8 or polyimide
(MICRUX_TF); pads ≥ 3 mm from any wetted edge.

**3.5.2 Exhaustive collection: time constant (Derived).** In a layer 0 < z < h with the WE at z = h (c = 0 after
the step), an insulating floor at z = 0 and uniform initial product c₀, the collected fraction is
F(t) = 1 − Σₙ 8/((2n+1)²π²) · exp(−(2n+1)² t/τ), τ = 4h²/(π²D).
With h = 0.20 mm and D_HQ = 9×10⁻¹⁰ m²/s (`chem.substrates.HQ.diffusion_coefficient`, 7–11×10⁻¹⁰):
τ = 4 × (2×10⁻⁴)² / (9.87 × 9×10⁻¹⁰) = **18.0 s**; F(90 s) = 1 − 0.811 e⁻⁵·⁰ = **0.9945** (D = 7×10⁻¹⁰: τ = 23.2 s,
F = 0.983; 1.1×10⁻⁹: 0.998). Rim 50 µm: (0.05 mm)²/D = 2.8 s. HQ that diffused into the CE/RE neck and pocket during
accumulation (0.044 µL, 4 % of the RC volume) returns only partly within 90 s; loss ≤ 3 % (Derived: neck exchange
rate D·A/(L·V_pocket) = 9×10⁻¹⁰ × 4×10⁻⁸ / (5×10⁻⁴ × 2.4×10⁻¹¹) = 3×10⁻³ s⁻¹; constant from run to run and
calibrated). With the double-step subtraction (§3.5.4) the uncollected tail of step a is collected in step b and
subtracted: effective collection F_a − (F(180) − F_a) = **0.989** (0.967 at the low D) — constant, calibrated, and
temperature-controlled (D depends on T; ±0.2 °C).

**3.5.3 Charge at 1 pg/mL and in the blank (Derived).** 5708 specific enzymes at 1 pg/mL (docs/12 §2.3, nominal model
"A0") × k_cat 1000 s⁻¹ (`chem.enzymes.alp.kcat_conjugate_assay_conditions`) × S/(K_m+S) = 3/(0.1+3) = 0.968 (K_m
`ma.chemistries.alp_hqdp.Km`, UNVERIFIED) × 900 s = 4.97×10⁹ HQ × 2 e × 1.602×10⁻¹⁹ C = **1.59 nC** (× 0.95 transfer,
× 0.97 collection ≈ 1.47 nC). The nominal blank carries ≈ 5700 NSB enzymes → ≈ 1.5 nC; with the blank CV 0.10
(`chem.nsb.blank_CV_analog_electrochemical`) **SD_blank ≈ 0.15 nC**. Hydrolysis during accumulation adds k_h × t × S₀ ×
V × 2F = 10⁻¹⁰ × 900 × 3 mM × 1.04 µL × 2F = **0.054 nC** at the nominal k_h (`ma.chemistries.alp_hqdp.hydrolysis_rate`)
and 0.54 nC at the acceptance limit 10⁻⁹ s⁻¹ (a blank offset, not removed by pre-electrolysis).

**3.5.4 The background charge of a step read — the design driver (Derived; inputs UNVERIFIED).** A potential step
charges the double layer: Q_dl = C_dl · A · ΔE. With C_dl ≈ 20 µF/cm² (value quoted as UNVERIFIED in the note of
`hw.gamry.noise_capacitive_per_uV_per_uF`):

| Geometry | A | ΔE | Q_dl | Repeatability needed for SD ≤ 0.05 nC |
|---|---|---|---|---|
| docs/12 (WE 3.8 × 9.8 mm, step from open circuit) | 37 mm² | ≈ 0.35 V (open circuit to +0.35 V, assumed) | 2.6 µC | 1.9×10⁻⁵ |
| **docs/13 (WE1 2.5 × 1.9 mm, step from E_rest = E_det − 0.15 V)** | 4.75 mm² | 0.15 V | **0.14 µC** | **3.5×10⁻⁴** |

0.05 nC is the target because it adds ≤ 11 % to the blank variance (0.05²/0.15²); the model's sensitivity rows (§1.3)
show 0.11 nC already costs 0.09 in P and 0.55 nC leaves P = 0.05. Oxide formation adds to Q_dl: gold surface oxidation
begins near the detection potential at pH 9.5 [assessment; potential not in the repository, UNVERIFIED], so **E_det
is set from a CV on the die at the bench** (docs/09 C16) as the lowest potential on the HQ diffusion plateau, and Pt is
not used for WE1 (earlier oxide formation [assessment]).

**Read protocol (D2).** Before each measurement the cell is switched on at E_rest for 15 s; step a: E_det for 90 s
(Q_a); back to E_rest for 15 s; step b: E_det for 90 s (Q_b); **Q_net = Q_a − Q_b**. Q_b contains the same charging,
oxide and steady faradaic background (and drift over 2 min) but almost no product (§3.5.2). E_rest must lie in the
potential window where neither HQ is oxidised nor BQ reduced on Au at pH 9.5 (otherwise BQ made by pre-electrolysis is
reduced back to HQ); that window is UNVERIFIED and is located by CV in M5. Between measurements the cell is off (open
circuit). Total 3.25 min per measurement.

**3.5.5 Reference and counter electrode strategy (chloride issue).**
* The RE pocket sees **only substrate**: the RC is filled with HQDP substrate before every run and the pocket is flushed
  through V15 at every fill; the pellet brings nL of A1 (entrained, ≪ 0.1 % of the RC). The substrate recipe fixes
  Cl⁻ (0.1 M Tris pH 9.5, 1 mM MgCl₂ and a fixed NaCl addition; value to be set, its effect on ALP UNVERIFIED — check in
  an E1.7-type run). A thin-film Ag/AgCl pad then sees constant chloride (Nernst ≈ 59 mV/decade, docs/11 §6.4).
* **Option R-a (preferred if the foundry offers it): thin-film Ag/AgCl pad.** Not in the Micrux custom offer (Au/Pt
  only, MICRUX_TF); IMT lists Au, Pt, ITO, Ti (IMT_FLYER) → availability UNVERIFIED; best drift found < 2 mV over 26 days
  (GO-coated, constant medium; Kim2015, doi:10.3390/s150306469).
* **Option R-b (baseline, available): Au quasi-reference** (Micrux dies carry Au RE and CE, PALMSENS_IDA). Acceptable
  because (i) Q_a and Q_b are measured 105 s apart, so slow drift cancels; (ii) E_det sits on the diffusion plateau;
  requirement: QRE drift ≤ ±20 mV over 8 h and E_det plateau ≥ ±50 mV wide (both own targets, UNVERIFIED; measured in
  M5 against a docked salt-bridge Ag/AgCl, the docs/02 §5.2 approach).
* **CE**: Au on the die in the pocket; reaction products (O₂ reduction / OH⁻) of ≤ 1 µC per run (Derived: 4 steps × 0.14
  µC + faradaic) → ≤ 10 pmol OH⁻ in 0.024 µL ≈ 0.4 mM, against 0.1 M Tris; flushed every run. BQ reduced at the CE
  could return to the WE only through the 0.5 mm neck: (0.5 mm)²/D = 280 s ≫ 90 s, and the CE pocket volume is 2 % of
  the RC [assessment: < 1 % redox-cycling artefact].
* Uncompensated resistance: neck 5×10⁻⁴ / (1.6 S/m × 4×10⁻⁸ m²) = 7.8 kΩ + RC spreading ≈ 4 kΩ ≈ **12 kΩ**
  (κ `hw.tubing.buffer_conductivity` 1.6 S/m, UNVERIFIED for the substrate) → R_u·C = 12 kΩ × 0.95 µF = **11 ms** ≪ τ;
  iR at nA currents < 0.1 mV (Derived). Docs/12's 250 kΩ × 7.4 µF = 1.9 s would have overlapped the collection.

**3.5.6 Model check.** RC 1 µL at 3 mM: P 0.26, ULOQ 3040 pg/mL (§1.3). At 1 mM the ULOQ falls to 1360 (just above
the 1000 pg/mL top of the range), hence 3 mM.

**3.5.7 Fallback read mode R-flow (WE2).** If M5 shows SD(Q_a − Q_b) > 0.05 nC: accumulate as before with WE1
unused (it still does pre-electrolysis), then sweep the RC at 10 µL/min with fresh substrate from RS through V14 over
WE2 held at E_det, with baseline windows before and after at the same flow (gen-1 rule, docs/08 W5). The background is
then a steady current, as in gen-1, with no charging transient. Cost: conversion < 1 (gen-1 thin-layer 0.78 at 10
µL/min, docs/09 §5.2; this channel 1 × 2 mm electrode, 50 µm high, not computed), product dispersion over ≈ 3 RC
volumes, 1 min longer read; substrate +10 µL per run. Potentiostat: WE1/WE2 selected by a dock relay (one channel) or
on a second channel (acceptable, docs/00).

### 3.6 Pre-electrolysis (UNVERIFIED pending docs/06 E1.2b)

* **PE1** (removal): fresh fill → single step at E_det for 90 s (with 15 s at E_rest before). Removes free HQ of the lot:
  10⁻⁵ (`ma.chemistries.alp_hqdp.free_product_impurity`, UNVERIFIED) × 3 mM × 1.04 µL = 3.1×10⁻¹⁴ mol = **6.0 nC**, four
  times the 1 pg/mL signal — this is why the 3 mM choice makes pre-electrolysis more important than it was at 1 mM.
* **Escape fraction (Derived)**: liquid not over WE1 = 4 stubs × 0.02 + neck 0.02 + pocket 0.024 = **0.12 µL (12 %)**, but
  only HQ that is still outside the RC at the last removal step and diffuses back during accumulation counts. The four
  stubs (0.2 mm long) exchange in (0.2 mm)²/D = 44 s and are largely emptied during the 90-s steps; the neck + pocket
  (0.044 µL = 4.2 % of the RC volume) exchange at 3×10⁻³ s⁻¹ (§3.5.2), i.e. 1 − e^(−3×10⁻³ × 900) = 93 % of their HQ
  returns during accumulation. Estimated escape **≤ 4 %, probably 1–4 %** (docs/12 assumed 1 %; the model credit uses
  ×0.01 with bounds that include ×0.04, docs/12 §8). Mitigation built in: PE2 (below) is a
  second removal 2 min before the drag, so HQ that crept back from the stubs between PE1 and PE2 is removed too; what
  remains is only what creeps back during accumulation.
* **PE2** (residual activity = carry-over monitor, docs/12 §3.8): after a 3.25-min hold, a double-step measurement
  (§3.5.4) integrates the product made by anything left in the RC (beads, adsorbed enzyme). Sensitivity: after a 10
  ng/mL sample, 10⁻⁴ of its signal (≈ 5700 enzymes, linear upper estimate, docs/12 §3.8) makes in 3.25 + 1.5 min ≈ 285 s
  5700 × 968 × 285 = 1.57×10⁹ HQ = **0.50 nC** — ten times the 0.05 nC background target: measurable. PE2 also
  removes HQ again just before the drag.
* E1.2b decides at G1 whether the guard principle works (docs/06 §4, row "1A informational"); the cartridge keeps PE1
  and PE2 regardless, because PE2 is also the carry-over monitor.

### 3.7 Waste

* No liquid waste is stored on the card. All liquid leaves through P_byp (BSM bypass), the IC syringes (to their waste
  port), P_wo and P_s (S_RC to its waste port) into one dock waste bottle (≥ 1 L, level sensor, §6).
* Per determination (Derived): BSM A1 0.38 mL (§3.1); dock A1: IC rinses 200 + cleaning 300 + WL 10 µL ≈ 0.51 mL;
  substrate 45 µL; total ≈ **0.94 mL** (gen-1 ≈ 5–6 mL, docs/09 §3.6). 16 runs + 4 extra ≈ 19 mL per cartridge.
* Beads: 20 doses × 5×10⁵ = 10⁷ beads × 11.5 µm³ = 0.12 µL in the 2.0 µL bead-waste pocket BW, held by M_w.

### 3.8 Bead-waste pocket and RC flush

After the read, beads are dragged through G4 into BW (§3.3.3). Spent beads keep making HQ in BW; to stop that HQ
from diffusing back when G4 next opens, **RC and BW are flushed together** right after bead-out: RS → V13 → RC → G4 →
BW → V16 → P_s, 20 µL at 40 µL/min (D10). M_w holds the beads against 40 µL/min through a 2 × 0.5 mm cross-section
(mean 0.67 mm/s; floor shear much lower) [assessment; checked in M1]. The RC is then left filled with fresh substrate
until the next run's prep.

---
## 4. Valve map

All card valves are **membrane valves on the CS_1367 principle** (TPE membrane pressed onto a 0.2 mm seat ridge by a
dock plunger from the top); gates are **flat-floor** (membrane pressed into the lane, no ridge; D6). Membrane open when
not pressed. Plungers are **spring-closed, solenoid-opened** (power to open → fail-closed) except V3, which is
**spring-open, solenoid-closed** (fail-open) so that the BSM, which keeps pumping when the dock loses power, always has
a path to the bypass (a dead-ended BSM would reach the card's ≈ 3 bar rating, CS_1367, long before its own 18 000 psi
limit, `hw.bsm.pressure_max_to_1mLmin`). The Empower method also sets a low pressure limit (value to be set at Stage 0;
existence of the setting on this installation UNVERIFIED).

Cycles = close → open → close. Per cartridge = 20 runs (16 + 2 priming + 2 recovery reserve), i.e. 10 per chamber.

| ID | Type | De-energised | Isolates / function | Open during (t from Inject Start of its run) | Cycles per run | Cycles per cartridge |
|---|---|---|---|---|---|---|
| V1, V2 | membrane | closed | P_in → IC1 / IC2 | 0–1.5 (own chamber) | 1 | 10 each |
| V3 | membrane | **open** | P_in → bypass | always except 0–1.5 of any run | 1 | 20 |
| V4, V5 | membrane | closed | bead port P_b → IC1 / IC2 (V2 variant) | −4.0 to −3.0 | 1 | 10 each |
| V6, V7 | membrane | closed | conjugate meter MC → IC1 / IC2 | −2.5 to −2.0 | 1 | 10 each |
| V8 | membrane | closed | conjugate tank RCj → MC | −3.0 to −2.5 (fill-to-vent) | 1 | 20 |
| V9, V10 | membrane | closed | IC floor port ↔ serpentine ↔ S_IC1 / S_IC2 | −5.0 to 38.0 and 39.75 to 44.75 | 2 | 20 each |
| V11 | membrane | closed | WL refresh inlet P_w → J | −5.0 to −4.5 | 1 | 20 |
| V12 | membrane | closed | WLc → P_wo (refresh outlet) | −4.75 to −4.5 | 1 | 20 |
| V13 | membrane | closed | RS → RC (fill; flush after read) | 29.0–29.6 and 58.25–58.75 | 2 | **40** (60 with R-flow) |
| V14 | membrane | closed | RC → WE2 channel → P_s | 29.0–29.4 (fill) [+ fallback read] | 1 (2) | 20 (40) |
| V15 | membrane | closed | CE/RE pocket → P_s | 29.4–29.6 | 1 | 20 |
| V16 | membrane | closed | BW → P_s | 58.25–58.75 | 1 | 20 |
| G1, G2 | flat-floor gate | closed | IC throat ↔ WL branch | −5.0 to −4.75 (refresh) and 38.0–39.75 (drag) | 2 | 20 each |
| G3 | flat-floor gate | closed | WLc ↔ RC | 38.0–39.75 | 1 | 20 |
| G4 | flat-floor gate | closed | RC ↔ BW | 58.0–58.75 | 1 | 20 |

**Totals (Derived):** 18 cycles per run; **360 per cartridge**; busiest V13 with 40 (60 in fallback). Evidence:
eCOC membrane valves "reproducibly actuated > 50 times without failure" (CHILDERS2024); ChipShop's membrane-valve chip
is single use, tight to 3 bar (CS_1367); ≥ 10⁶ only for PDMS / clean liquids, secondary source (docs/10 §7). The
busiest valve needs 0.8× (1.2× in fallback) the published thermoplastic figure — **bench gate at 3× life = 180 cycles**
for every valve type with the real media (bead suspension, 1 % BSA conjugate buffer, HQDP pH 9.5), leak test at
50 kPa and at 3 bar (§10, M4).

**Requirements per valve** (targets, own; UNVERIFIED feasibility): closed leak ≤ 0.1 µL/min at 20 kPa (would move ≤ 1.5
µL in a 15-min accumulation — still too much for the RC, which is why the RC valves also see no pressure difference
during accumulation: all sources are stopped and the ICs are vented); closed solution resistance ≥ 1 GΩ (gen-1
minimum 15 MΩ, `hw.tubing.peek_isolation_length_each_side_of_cell`); actuation ≤ 0.2 s; **no displacement of RC
liquid on actuation**: the plungers of G3, G4, V13–V15 close with the RC open to nothing, so the membrane stroke volume
(≈ seat area 0.5 × 0.7 mm × 0.2 mm stroke = 0.07 µL, Derived) is displaced out of the seat into whichever side is
compliant — closing order chosen so that the last valve to close on the RC is the one whose stroke pushes away from
the RC (G3 closes after V13/V14/V15 at the end of the drag; docs/09 F9 "valve switching must not push product out").

**Fail-safe state** (dock power lost, PC lost, or sequencer safe state): all valves and gates closed except V3 open;
all magnets up (springs: beads stay where they are and cannot reach the RC through closed gates); syringe pumps stop
(hold position); Gamry cell off; Peltiers off (reagent zone warms; the latch flags the cartridge if > 10 °C,
docs/12 F16); dock hardware watchdog (heartbeat from Python) drives the same state if the PC dies (closes the Stage-2
TODO of `sequencer.py`). In this state nothing drains or siphons: every chamber is either vented and isolated, or
sealed.

---

## 5. Reagent system: V1 versus V2

Both variants keep the conjugate (RCj + MC) and the substrate (RS) on the card. They differ only in where the bead
stock lives. Doses are the docs/05 §4.1 doses (5×10⁵ beads in 10 µL; 10 µL of conjugate per run). Sizing: 20 doses per
cartridge (16 + 2 priming + 2 recovery, docs/12 §3.6).

### 5.1 V1 — beads on the card

On-card bead tank RB (0.5 mL, 5 mm deep, reagent zone 4–8 °C), a 150 µL tidal side reservoir driven by a dock
pressure channel, a 10.0 µL bead meter between two valves emptied by air into the vented IC (docs/12 §3.2–3.3). Card
gains 3 valves (tank, meter outlet, side reservoir), a pressure port and 0.3 mL of factory-filled bead suspension.

### 5.2 V2 — bead stock in the dock

A 2 mL glass or low-binding PP vial (≥ 0.5 mL working; minimum stirred volume UNVERIFIED) in a cooled (4–8 °C)
holder that **rocks or rotates end-over-end** (no magnetic stir bar: it collects paramagnetic beads); a Cavro Centris /
Hamilton PSD/4-class pump S_b (250 µL syringe → ≈ 10 nL/step, docs/11 §5.2) with a selection valve (ports: vial, A1,
card, waste) and a 0.5 mm ID FEP holding coil of ≈ 40 µL that keeps beads out of the syringe (SIA principle of gen-1,
docs/07 §2); outlet line 0.25 mm ID × 50 mm (2.5 µL) to the face-seal port P_b. Per dose: (1) return the vial-to-valve
line content to the vial (beads settled there since the last dose); (2) aspirate 2 µL air, 10.0 µL beads, 2 µL air;
(3) dispense through P_b and V_k into the vented IC followed by ≈ 6 µL A1 (line 2.5 + card 2.8 + margin), so the whole
slug and the dead volumes reach the chamber; (4) rinse the outlet line to waste with A1 (V4/V5 closed, via the
waste port of S_b — the card path is then filled with A1 up to V4/V5).

### 5.3 Quantitative comparison

| Criterion | V1 (beads on card) | V2 (beads in dock vial) | Source / arithmetic |
|---|---|---|---|
| Bead volume per cartridge | 20 × 10 µL = 200 µL + tank/meter dead volume 100 µL (UNVERIFIED) = **0.30 mL** = 1.5×10⁷ beads = 230 µg | 200 µL dosed + line priming 2 × (40 + 2.5) µL ≈ **0.29 mL** per 8 h; the remaining vial stock serves the next cartridge if bead-stock life allows | 5×10⁷ /mL (docs/09 §3.1); 6.5×10¹⁰ /g (`chem.surfaces.magnetic_bead_M280_count_per_mass`) |
| Priming | meter and channel priming 2 doses | holding coil and line priming at day start | docs/12 §3.6 |
| Settling between doses (31 min) | 7 mm/h × 31 min = **3.6 mm** of a 5 mm tank cleared → each dose needs a full resuspension | vial agitated continuously; the 2.5 µL outlet line is purged every dose | `ma.capture.in_vial_unstirred_rate_factor` note; docs/10 §2 (Stokes ≈ 4 mm/h) |
| Resuspension | 3 tidal strokes of 150 µL in a tank whose fill falls from 300 to 100 µL over the cartridge — homogeneity and its **trend with fill level** unmeasured (no on-board liquid-bead data, docs/10 §9.3) | rocking vial = the gen-1 reservoir specification (docs/07 §5.5); **dose CV measured by gen-1 E2.2** (20 doses over 8 h, ≤ 5 % target) | docs/06 E2.2 |
| Shelf storage before use | beads sediment for the whole shelf life (days–weeks) into a cake on the foil of a COC tank; redispersion by pressure tides untested | none: stock prepared in the lab (docs/06 §4.0 protocol) | [assessment] |
| Stability over 8 h at 4–8 °C | not measured (beads with capture antibody, docs/09 §3.1 UNVERIFIED) — identical for both variants | same | docs/09 §3.1 |
| Dose precision | geometry of a moulded 10.0 µL cavity: ±10 µm on 2.0 × 1.0 × 5.0 mm → ±(0.5 + 1.0 + 0.2) % = **±1.7 % systematic per card** (tolerance UNVERIFIED) + suspension inhomogeneity (unknown) | syringe 10 nL/step on 10 µL = 0.1 %; holding-coil and air-gap reproducibility; suspension homogeneity in the vial (E2.2) | Derived; docs/11 §5.2 |
| LOD consequence of dose CV (model) | if CV 0.10: P 0.20; 0.15: 0.17 | if CV 0.05: P 0.26 | §1.3 |
| Conjugate (both) | RCj 0.5 mL tank, 0.30 mL fill (200 µL + 100 µL dead), 4–8 °C, dark; MC 10.0 µL fill-to-vent | same | docs/12 §3.6 |
| Conjugate stability | conjugate-only ageing arm of E1.3: 0/2/8/24 h at 4 and 22 °C; nothing beyond 24 h | same | docs/06 E1.3 |
| HQDP (both): 8 h in use at 25 °C (D8), 3 mM | free HQ formed: k_h·t = 10⁻¹⁰ × 28 800 s = **2.9×10⁻⁶** (nominal) / 2.9×10⁻⁵ at the acceptance limit 10⁻⁹ s⁻¹ → removed per run by PE1/PE2; Pi: 2·k_h·t·S₀ = 2 × 10⁻⁹ × 28 800 × 3 mM = **0.17 µM** at the limit (0.017 µM nominal) vs ≤ 1 µM target → margin ×6 (×60) | same | `ma.chemistries.alp_hqdp.hydrolysis_rate`; acceptance docs/05 §5 U3; target docs/09 §3.4; 2 Pi per HQ (`…phosphate_per_product`) |
| HQDP shelf (factory-filled card, before use) | Pi limit reached after 1 µM / (2 × 10⁻⁹ s⁻¹ × 3 mM) = 1.7×10⁵ s = **1.9 days** at the acceptance-limit k_h (19 days nominal); cooling helps by an unknown factor (no temperature coefficient, docs/09 §5.4 item 11) | same | Derived (docs/12 §2.3 gives 1.9 days at 3 mM) |
| Card complexity | +3 valves, +1 pressure port, +0.8 mL of tanks in the cold zone | +1 face-seal port; −3 valves vs V1 | §2, §4 |
| Dock complexity | one more pressure channel | one more syringe pump + selection valve + cooled rocking vial holder (sourced class: docs/11 §5.2) | |
| Contamination route (C21) | bead fill at the cartridge factory (another human-IgG-clean fill) | lab bead preparation as gen-1 | docs/09 C21 |
| Specific risks | dose drift with tank level; bead cake after shelf; beads adhering to cold COC; meter fill with a settling suspension | one more dock–card interface in the bead path (face seal may trap beads; port dead volume chased); vial line maintenance; dock line state affects the dose | [assessment] |

### 5.4 Recommendation: **V2**

Reasons, in order of weight: (1) V1 puts on the consumable the one element with **no precedent and no data** — an
on-board liquid bead suspension dosed over hours (docs/10 §6.2: "no multi-run cartridge with an on-board liquid bead
suspension was found"; §9.3) — and adds a shelf-stored bead cake to it; (2) the bead-dose CV is the reagent parameter
the model does see (CV 0.05 → 0.10: P 0.26 → 0.20), and V2's dose CV is **measured anyway by gen-1 E2.2** with the same
reservoir concept; (3) V2 is simpler on the card (−3 valves, no cold bead tank) and keeps the bead stock's lifetime
independent of the cartridge's (docs/11 §4 option 4 and §7.2 reached the same conclusion). The price is one more
dock pump and a bead path through one face seal, both testable in mock-up M3.

**Refinement (D12, for the user to confirm): fill RCj and RS at insertion from cooled dock bottles** unless the shelf
data support factory filling: at the acceptance-limit k_h a factory-filled 3 mM HQDP store exceeds the Pi target in
1.9 days, and no conjugate data exist beyond 24 h. Dock filling costs two face-seal fill ports and ~3 min at
docking; the card keeps its reagents "on the card" for the run. If E1.2 measures k_h ≤ 10⁻¹⁰ s⁻¹ and a 4 °C
conjugate ageing series (> 24 h) is flat, factory filling becomes acceptable for ≈ 2 weeks of cold storage (19 days at
nominal k_h, Derived above).

---
## 6. Docking station

### 6.1 Block diagram

```
                     Waters stack (earthed)                                   Lab PC (Windows)
  BSM (A1 only) -> restrictors -> SM-FL (100 uL loop) --PEEK >= 0.3 m-->+     orchestrator (Python >= 3.10)
  SM-FL Inject Start (conn. 1, pins 1-2) ------------------------------+  |      |  JSON/TCP   gamry_worker (Gamry Py 3.7)
                                                                        |  |      |                  |
  +------------------------------------- DOCK ---------------------------|--|------|------------------|--------------+
  |  isolated DAQ (Inject Start, line code) <---------------------------'  |      |                  |              |
  |  dock controller (MCU, to be selected): plungers, Peltier PID,         |   USB/serial          Reference 600+   |
  |    carriage, interlocks, HARDWARE WATCHDOG (heartbeat from Python) <----------'               (floating)         |
  |                                                                         |                        |  cell cable   |
  |  LID (top): 20 plunger actuators (V1-V16, G1-G4) | assay-zone heater    |                 +------+-------+       |
  |       block 25.0 C | Faraday sub-enclosure with 6 pogo pins + WE1/WE2   |                 | pogo head on |       |
  |       reed relay -> Gamry WE / RE / CE                                  |                 | die pads     |       |
  |  CARD NEST: locating pins, face-seal manifold (10 ports) <--------------'  P_in          +--------------+       |
  |  BELOW: reagent-zone Peltier 4-8 C | RS / wall plate 25 C | magnet bay (25 C air):                             |
  |       X-Y-Z carriage (M_c 10x10x5, M_d 2x2x4), M_h lift under RC, fixed M_w under BW                         |
  |  FLUIDICS: S_b (beads, V2) + rocking cooled bead vial | S_IC1, S_IC2 (1 mL) | S_RC (250 uL) on one RS-485 bus;   |
  |       2 pressure channels (P_c conjugate tank, P_mv meter vent) | A1 bottle | (HQDP + conjugate bottles, D12)    |
  |       waste bottle with level sensor | drip tray with leak electrodes | sensors: T x6, RH, P on the P_in line      |
  |  ID: data-matrix scanner (to be selected); lid switch; contact-loop resistance via the pogo head                    |
  +-------------------------------------------------------------------------------------------------------------------+
```

### 6.2 Actuators, sensors and controllers

Candidate parts only as sourced in docs/11; otherwise "to be selected". No part number below is new.

| Item | Function | Specification it must meet | Candidate (docs/11) |
|---|---|---|---|
| Plunger actuators ×20 | close V1–V16 (V3: open), G1–G4 from the top | stroke ≥ 0.3 mm (TPE 0.3–0.5 mm, UNVERIFIED), force to seal 50 kPa and survive 3 bar on a 0.5 × 0.7 mm seat (UNVERIFIED value; set in M4), ≤ 0.2 s, spring-return fail state per §4, position feedback (Hall or switch) | memetis actuators sold for CS_1367 (named on CS_1367, model not read) — to be selected; solenoid plungers alternative [assessment] |
| X–Y–Z magnet carriage | collect, gather, drag, bead-out | travel ≥ 45 × 25 mm (x 30–75, y 12–32), repeatability ≤ 10 µm, speed 0.05–5 mm/s, path following of a ≥ 3 mm radius lane, **magnet-to-foil gap 0.16 ± 0.05 mm** (§3.3.2: v_max drops from 0.57 to 0.35 mm/s at +0.2 mm), Z lift 5 mm spring-up; low-EMI drivers, disabled during reads | Zaber stages with the Zaber Motion Library (Python; ZABER_SW) — model, travel, speed UNVERIFIED |
| M_h lift | hold the pellet under WE1 during accumulation | 4 mm stroke, spring-up | solenoid/spring slide, to be selected (docs/11 §5.4 assessment) |
| Magnets | §3.3.1 | B_r ≥ 1.2 T class, Ni-coated | to be selected |
| Syringe pumps S_b, S_IC1, S_IC2, S_RC | bead dosing; tidal mixing, drain, rinse; WL refresh, RC fill/flush, fallback read at 10 µL/min | ≥ 24 000 steps per stroke (10 nL/step on 250 µL; 42 nL on 1 mL), selection valve with ≥ 4 ports, RS-485 bus, pulsation-free at 10 µL/min for the fallback read | Tecan Cavro Centris (RS-232/485/CAN, up to 16 per bus; TECAN_CENTRIS) or Hamilton PSD/4 (HAMILTON_PSD4; smooth-flow variant HAMILTON_97709 for S_RC) |
| Pressure channels ×2 | conjugate tank headspace (P_c, +5 to +20 kPa) and meter vent/air push (P_mv) | 0–35 kPa, 1 % stability, 30 ms response | Fluigent Flow EZ 345 mbar (FLUIGENT_FLOWEZ, Python SDK FLUIGENT_SDK) or Elveflow OB1 0–200 mbar (ELVEFLOW_OB1); or one regulator + solenoids (docs/11 §5.1 assessment) |
| Flow sensors | verify the 10 µL/min fallback read and the rinse flows | 1–20 µL/min and 50–500 µL/min | Sensirion LG16-0150D (7 µL/min FS water — marginal for 10 µL/min, SENSIRION_LG16) and SLF3S-0600F (SENSIRION_SLF3S); a 10–300 µL/min part was not identified (docs/11 §5.3) |
| Peltier zones ×3 | reagent zone 4–8 °C (RCj, MC, bead vial); assay wall plate and top heater block 25.0 ± 0.2 °C | §6.5 | modules and drivers to be selected (docs/11 §5.4: no datasheet read) |
| Bead vial holder (V2) | 4–8 °C, rocking or end-over-end, low shear, no foaming | dose CV ≤ 5 % over 8 h (docs/06 E2.2 acceptance) | to be selected |
| Isolated DAQ | Inject Start (and line code) into Python | opto-isolated input, timestamp on the PC clock | LabJack U3 as in gen-1 (`hardware_lab.example.yaml`) |
| Dock controller | plungers, Peltier PID, carriage interlocks, sensors, heartbeat watchdog → fail-safe state without the PC | independent of the PC; reports state to Python | to be selected |
| Potentiostat | PE1, PE2, double-step read; fallback CA on WE2 | one channel (two acceptable, docs/00) | Gamry Reference 600+ (in hand; docs/02 §4) |
| WE1/WE2 relay | select the read electrode on one channel | leakage ≤ 0.1 pA at 0.5 V (≥ 5×10¹² Ω, Derived), thermal EMF ≤ 10 µV | low-leakage reed relay, to be selected; or a second channel |
| Sensors | card presence (lid switch + contact loop), card ID, leak, temperatures (6), RH (dew point), P_in line pressure, waste level | §6.6–6.8 | to be selected |

### 6.3 Electrical design for nA-level amperometry

* **Signal levels (Derived):** specific product current is irrelevant in the step read (it is a charge); the step pair
  integrates ≈ 0.14 µC of charging per step (peak ≈ ΔE/R_u = 0.15 V / 12 kΩ = 12 µA, decaying with 11 ms) and 1.5 nC of
  product at 1 pg/mL; the target background SD is 0.05 nC (§3.5.4). The Ref 600+ resolves 20 aA and has 11 current
  ranges 60 pA–600 mA (docs/02 §4.1): the step needs a µA range at the start and a nA range afterwards → **autoranging
  or a fixed 60 µA range** with the charge integrated digitally; which of the two gives the lower charge SD is a bench
  question (M5).
* **Shielding:** the die, pogo head and the first 10 cm of lead sit in a grounded metal sub-enclosure in the lid (Faraday
  cage, docs/02 §4.4); shielded leads ≤ 0.3 m to the Gamry cell-cable connector; shield connection per the Gamry manual
  for floating operation (wording UNVERIFIED, docs/02 §4.4).
* **Contact resistance:** gold-plated spring pins on Au pads (part numbers UNVERIFIED, docs/11 §5.4); mΩ–Ω-scale
  resistance is negligible against R_u = 12 kΩ; what matters is that it does not change during a step pair →
  **no carriage, plunger or pump movement within 0.5 m during a read window** where avoidable (§7.1 "quiet windows");
  contact-loop resistance logged at docking and every hour.
* **Leakage:** pads ≥ 3 mm from any wetted edge, on the dry side of the die bond; SU-8/PI passivation; any leakage path
  to WE ≥ 5×10¹² Ω (Derived from ≤ 0.1 pA at 0.5 V); the die area is kept above the dew point (§6.6).
* **Grounding with the Waters stack:** the Gamry floats (`hw.gamry.floating`; docs/02 §4.4). During PE1, PE2 and the
  read **the RC is closed on all sides** (G3, G4, V13–V16 closed), so the solution path to the earthed BSM is broken at
  closed membranes, not merely lengthened (docs/12 §2.4 F20); requirement ≥ 1 GΩ closed-valve solution resistance
  (§4, measured in M4 by EIS); the 0.3 m PEEK line from the SM-FL stays (`hw.tubing.peek_isolation_length_each_side_of_cell`).
  The dock waste and A1 bottles are plastic; syringe pumps' metal parts are not in the RC path while the RC is sealed.
* **Noise sources in the dock:** stepper drivers (carriage, syringe pumps) and Peltier PWM. Rules: Peltier drives linear
  or PWM ≥ 20 kHz with filtered leads (to be selected); carriage drivers disabled with brake during reads; tidal mixing
  of the other chamber paused during that chamber-independent read window (identical in every run, so no bias between
  samples, C4); separate supplies and star ground at the Gamry chassis point.

### 6.4 Magnet and mechanical datum

The card is pressed by the lid onto three datum pads so that the foil's underside sits at a defined height above the
carriage plane; gap 0.16 ± 0.05 mm (foil 140 µm flatness UNVERIFIED). The foil is not supported under the magnet path
(the magnets must reach it), so the lid must not pressurise the card interior: chambers are vented and the RC is
liquid-filled at ambient pressure.

### 6.5 Thermal design

* **Zones:** reagent zone (x 0–20 mm) 4–8 °C from a bottom Peltier plate on the foil side (tank walls are the thin
  foil, docs/11 §4); assay zone 25.0 ± 0.2 °C (docs/07 §5.1 spec) from (i) a top heater block on the L3 frame over the
  ICs, WL and die region, (ii) a bottom plate under RS and outside the magnet windows, (iii) the magnet bay air held at
  25 °C. Thermal break: through-slot x 20–24 mm with two 3 mm bridges (channels from MC and P_b cross there).
* **Time constants (Derived, COC diffusivity ≈ 1×10⁻⁷ m²/s UNVERIFIED):** through the 6 mm body (3 mm)²/α ≈ 90 s; a 0.2
  mm RC (water, α ≈ 1.4×10⁻⁷ m²/s UNVERIFIED) 0.3 s. Card equilibration at docking ≈ 10 min (priming runs in parallel).
* **Liquids crossing zones:** 10 µL of 4–8 °C conjugate into 166 µL at 25 °C (ΔT of the mix ≈ 1 K, recovered in ≈ 1
  min [assessment]; identical every run); the substrate no longer crosses zones (D8); A1 from room temperature.
* **Effect sizes:** the model has no temperature dependence (docs/03 §11); ±0.2 °C acts on k_on, k_cat, D (collection
  at 90 s, §3.5.2) — calibrated out if constant.

### 6.6 Dew point and condensation

At 22 °C and 50 % RH the dew point is ≈ 11 °C (Magnus approximation; constants UNVERIFIED). The reagent zone (4–8 °C)
is below it: it is enclosed by closed-cell insulation with a dry-gas or desiccant volume and a drip path away from the
card nest; the die and pogo region is ≥ 35 mm away and at 25 °C (above the dew point), with an RH sensor in the lid
logging the margin. Condensate on the pogo pads would short the WE (§6.3 leakage requirement).

### 6.7 Cartridge presence, identity and docking check

Lid-closed switch; contact-loop resistance on the die (< 10 Ω expected, two pins); data-matrix code on the frame read
by a scanner (to be selected) giving card serial, mould/die lot, fill lot and date, expiry and the lot calibration;
Python keeps a usage log per serial (runs used, faults) and refuses expired or exhausted cards. On docking: leak test
(§6.8), CV of WE1 in substrate after the first fill (E_det plateau and C_dl → electrode-area check, §8.1).

### 6.8 Leak detection

(1) Docking pressure-hold test: every liquid port pressurised to 20 kPa against closed valves for 30 s, decay limit
set in M4; (2) drip tray with two interdigitated electrodes (conductivity) and a level switch under the card nest; (3)
syringe-pump stall/pressure faults; (4) volume balance: liquid dispensed vs waste-bottle level per run; (5) P_in line
pressure (dock-side sensor, to be selected) during the 150 µL transfer (blocked card or leaking face seal); any of
these → fault → safe state → latch.

---

## 7. Control and timing

### 7.1 Per-run step table and staggering

Times in minutes from the run's own Inject Start (anchor). Chamber k = 1 for odd runs, 2 for even runs; run n+1 is
injected 31.0 min after run n. Valves not listed are closed (V3 open unless listed closed). "Res." = resource that is
exclusive (checked for overlap at the 31.0-min offset).

| t (min) | Step | Flows / volumes | Valves / gates open | Magnets | Gamry | Res. |
|---|---|---|---|---|---|---|
| −5.0 → −4.75 | WL branch k refresh into the empty ICk | S_RC: 5 µL A1 via P_w at 20 µL/min | V11, G_k, V(9/10)_k | – | – | S_RC |
| −4.75 → −4.5 | WLc refresh to waste | S_RC: 5 µL | V11, V12 | – | – | S_RC |
| −4.5 → −4.0 | drain ICk (refresh liquid) | S_ICk aspirate → waste | V(9/10)_k | – | – | S_ICk |
| −4.0 → −3.0 | **bead dose (V2)**: line return, aspirate air/10 µL/air, dispense + 6 µL A1 push | S_b | V(4/5)_k | – | – | S_b |
| −3.0 → −2.5 | conjugate meter fill-to-vent | P_c +10 kPa (value set in M3) | V8 | – | – | P_c |
| −2.5 → −2.0 | conjugate push into ICk | P_mv air push, 10.0 µL | V(6/7)_k | – | – | P_mv |
| −1.0 → 0 | SM-FL aspirates ≈ 200 µL (Empower) | BSM 1 µL/min → bypass | V3 | – | – | – |
| **0** | **Inject Start** (anchor) | | | | | |
| 0 → 1.5 | transfer 150 µL into ICk | BSM 100 µL/min | V(1/2)_k (V3 closed) | – | – | inlet |
| 1.5 → 3.5 | loop + line flush to bypass; Loop Offline at 3.5 | BSM 100 µL/min, 200 µL | V3 | – | – | inlet |
| 1.5 → 31.5 | **incubation 30 min**, 25.0 °C, tidal 50 µL every 30 s (paused in quiet windows) | S_ICk; BSM 1 µL/min → bypass from 3.5 | V(9/10)_k, V3 | – | – | S_ICk |
| 3.75 → 7.0 and 23.75 → 27.0 | quiet windows: the previous run's PE2 and READ; tidal of this run paused (same times in every run) | | | | | |
| 29.0 → 29.6 | **RC prep**: RC + WE2 channel then CE/RE pocket filled with 20 + 5 µL HQDP (3 mM) | S_RC pull via P_s at 40 µL/min | V13 + V14, then V13 + V15 | M_h down | – | RC, S_RC |
| 29.75 → 31.5 | **PE1** (removal; background logged) | sealed | – | – | E_rest 15 s, E_det 90 s, cell off | RC, Gamry |
| 31.5 → 33.5 | collection in ICk | – | V(9/10)_k (syringe idle) | M_c up under ICk | – | carriage |
| 33.5 → 35.0 | gather to the throat (4 mm at 0.05 mm/s) | – | – | M_c moving | – | carriage |
| 34.75 → 38.0 | **PE2** = residual activity of the RC (carry-over monitor) + removal | sealed | – | – | step pair 15/90/15/90 s | RC, Gamry |
| 35.0 → 38.0 | drain, 2 rinses, third 100 µL fill stays | S_ICk 300 µL/min | V(9/10)_k | M_c holds | – | S_ICk |
| 38.0 → 39.75 | hand-over M_c → M_d, **drag 20.3 mm at 0.20 mm/s** into the RC; M_h up; gates close (V(9/10)_k closed) | no flow | G_k, G3 | M_d, then M_h | – | carriage, RC |
| **39.75 → 54.75** | **accumulation 15 min**, RC sealed, cell off | – | – | M_h holds | off | RC |
| 39.75 → 44.75 | ICk cleaning: 3 × (100 µL, 2 tidal, drain) (+3 if the previous result > 100 pg/mL) | S_ICk | V(9/10)_k | – | – | S_ICk |
| 54.75 → 58.0 | **READ**: step pair; Q_net = Q_a − Q_b (fallback R-flow: WE2 at E_det, 10 µL at 10 µL/min with 0.5-min baselines) | sealed (R-flow: S_RC pull) | – (R-flow: V13, V14) | M_h | step pair (or CA on WE2) | RC, Gamry |
| **58.0** | **result** (58.0 min after Inject Start; 59.0 after aspiration start) | | | | | |
| 58.0 → 58.25 | bead-out to BW (6 mm at 0.5 mm/s) | – | G4 | M_h down, M_d | – | carriage, RC |
| 58.25 → 58.75 | RC + BW flush, RC left filled | S_RC 20 µL at 40 µL/min | V13, G4, V16 | M_w (fixed) | – | RC, S_RC |

**Resource check at the 31.0-min offset (Derived):** RC occupied 29.0 → 58.75 = 29.75 min per run → slack 1.25 min
before the next run's RC prep at its 29.0 (= 60.0 here). Gamry used 29.75–31.5, 34.75–38.0, 54.75–58.0; the next run's
windows fall at 60.75+, 65.75+ and 85.75+ → no overlap. Carriage 31.5–39.75 and 58.0–58.25 (next run 62.5–70.75) → no
overlap. S_RC: −5.0 → −4.5 (= previous run's 26.0–26.5), 29.0–29.6, 58.25–58.75 → no overlap. ICk busy −5.0 → 44.75 (or
≈ 49.5 with extra cleaning) of a 62-min period. **Margin to the 60-min limit: 2.0 min.** Throughput 1.94 samples/h;
16 samples in 15 × 31 + 58 = 523 min (8.7 h from the first Inject Start). Options if the cadence must shrink:
accumulation 13 min (−2 min; model ≈ −0.01 in P) or a 60-s step pair (τ = 18 s: F(60) = 0.96 — calibrated, but more
sensitive to D and temperature).

**Quiet windows:** during the step pairs (PE2, READ) the tidal mixing of the other chamber is paused and no carriage
move is scheduled (only run n's own rinses overlap PE2; PE2's criterion is ten times its background target, §3.6). The pauses take
6.5 min of tidal mixing out of the 30-min incubation, at the same times in every run (C4).

### 7.2 Trigger chain from Empower

1. The operator docks the card and loads the bead vial (and, under D12, the conjugate and HQDP bottles) and the SM-FL
   tray; Python runs the docking checks and two priming runs (no injection) (§8.1).
2. Empower sample set: one line per determination, all with the **same instrument method**: SM-FL full loop 100 µL
   (2× overfill), BSM A1 100 µL/min 0–3.5 min, **Loop Offline at 3.5 min**, 1 µL/min 3.5–30.0 min, run time 30.0 min;
   injection overhead ≈ 1 min (`hw.smfl.injection_overhead_time` 0.25–2, UNVERIFIED) → Inject Start every ≈ 31.0 min
   (measured at Stage 0; the cycle tolerates 30.75–33 min, below 30.75 the RC slack is gone → the watchdog faults the
   early run).
3. SM-FL Inject Start (connector 1, pins 1–2, docs/02 §3.1) → isolated DAQ input → Python timestamps t₀, checks the line
   code if wired (docs/02 §3.2) and the spacing from the previous t₀, assigns the chamber (alternating) and instantiates
   the run table anchored at t₀. Steps before t₀ (−5.0 → −1.0) are executed against the **predicted** next t₀ (previous
   t₀ + measured cadence), exactly as gen-1 doses the cup before the injection (`cycle_primary.yaml`).
4. Python drives the dock (valves, carriage, pumps, pressure), the Gamry worker (steps) and logs everything; Empower
   only pumps and injects (primary scheme "Empower is the fluidic master", docs/02 §3.2). Watchdog: late/early/unexpected
   Inject Start beyond 30 s, device error, leak, temperature excursion → safe state (§4) → fault latch.

### 7.3 Mapping onto the existing `automation/` package

| Existing element (automation/) | Reused as is | Needs change / new |
|---|---|---|
| `cycle.py` step table (start/end, `valves`, `magnet`, `sia`, `potentiostat`, `bsm`, `smfl`, `empower`, `role`) and `validate()` (no gaps, ≤ 60 min, injects declared, SM-FL actions) | schema and checks | **chamber templating** (`{k}` in valve, pump and gate names), a `resources:` list per step and a **periodic overlap check** at the cadence offset; card valves are two-position valves (`open`/`closed`); new `sia`-type actions: `bead_dose`, `tidal_mix`, `drain_chamber`, `rinse_chamber`, `wl_refresh`, `fill_rc`, `flush_rc`; `magnet` becomes `{carriage: path/position, M_h: up/down}`; potentiostat actions `step` and `step_pair` |
| `sequencer.py`: anchors on each Inject Start, watchdog, safe state, run log, fault handling | anchoring, watchdog, safe-state discipline, logging | today one cycle runs at a time; A needs **two interleaved run instances** sharing RC, carriage, Gamry and S_RC → a small **scheduler** that instantiates the run table per Inject Start and merges actions (or one 62-min two-inject "super-cycle" table in steady state, which the current single-sequencer can already run because `Cycle` allows several injects — but the first and last runs of a sample set then need their own tables) |
| `latch.py` fault latch | unchanged; a fault invalidates **both** runs in flight | — |
| `cycle_recovery.yaml` | concept | new `cycle_cartridgeA_recovery.yaml`: bead-out from RC to BW, RC + BW flush, both chambers drained and rinsed 3×, WL refresh both branches, carriage park (≈ 6 min) — docs/09 F17 |
| `devices/base.py` interfaces: `Valve`, `SIAModule`, `Magnet`, `InjectStartInput`, `Potentiostat`, `Empower` | `Valve` (two positions), `InjectStartInput`, `Empower` (passive), `Magnet` for M_h | new classes: `MagnetCarriage` (move_to, follow_path(speed), z), several named `SyringePump`s (the `SIAModule` contract per pump), `PressureChannel`, `DockController` (plungers, Peltier, sensors, heartbeat), `ThermalZone`, `CardReader`, `LeakSensor`; simulators for each in `devices/sim.py` |
| `gamry_worker.py` (JSON-lines protocol, sim backend) | process split (Gamry Python 3.7, 32-bit) and protocol style | new commands `step` / `step_pair` (E_rest, E_det, durations, range) returning the trace and charges; the ToolkitPy calls stay a stub (not verified, docs/02 §4.3) |
| `signal_proc.py` (baseline-corrected charge in a readout window) | used unchanged for the fallback R-flow read | new `step_pair_charge()` (Q_a − Q_b with fixed integration windows) and a PE2 threshold check |
| `stats.py`, `analyze.py`, `gates.yaml` (LOD = 3·SD/b, carry-over 10 ng/mL → B1 → B2, criterion 10⁻⁴) | unchanged | new gate entries for the mock-ups M1–M7 (§10) |
| `model_feedback.py` | unchanged (bench values per docs/06 §9) | — |
| `hardware_sim.yaml` / `hardware_lab.example.yaml` | format | new `hardware_cartridgeA_sim.yaml` with card valves V1–V16, G1–G4, pumps, carriage, sensors |

Sketch of one templated step (illustrative YAML, not a file in the repository):

```yaml
- {name: drag_to_rc, start_min: 38.0, end_min: 39.75, chamber: "{k}", resources: [carriage, RC],
   valves: {"G{k}": open, G3: open, "Vfloor{k}": closed},   # Vfloor1 = V9, Vfloor2 = V10
   carriage: {path: "throat{k}->RC", speed_mm_s: 0.20, magnet: M_d}, hold_magnet: up}
```

---
## 8. Calibration and QC strategy

### 8.1 At docking (per cartridge, ≈ 15 min, no injection)

1. Card ID read, expiry and usage check; lid closed; contact-loop resistance < 10 Ω.
2. Leak test (§6.8); thermal equilibration of both zones (≥ 10 min, §6.5).
3. (D12 default) RS and RCj filled from the dock bottles; priming: holding coil and bead line (S_b), MC (one dose to waste
   through IC1 and its drain), both wash-lane branches and WLc, RC + WE2 + CE/RE pocket.
4. **Electrode QC on the first RC fill:** CV of WE1 in substrate between E_rest − 0.1 V and E_det + 0.1 V (no HQ beyond
   the lot's impurity): double-layer capacitance → effective area check against the lot value (±10 %, own target);
   no unexpected faradaic wave. Then **5 step pairs** on the same fill: SD(Q_a − Q_b) ≤ **0.05 nC** (§3.5.4) — the
   cartridge's own background acceptance; failure → R-flow mode (WE2) for this card or reject.
5. Two priming runs (one per chamber) **without an injection**: the chamber receives 150 µL A1 from S_ICk instead of
   the BSM transfer; checks dosing, collection, drag and read end-to-end; results logged, not used.

### 8.2 Calibration

* **Lot calibration** (per bead lot × conjugate lot × die lot, made by the lab): full curve 0, 1, 3, 10, 30, 100, 300,
  1000 pg/mL in triplicate spread over ≥ 3 cartridges; 4PL and the 0–10 pg/mL linear slope of docs/06 §7.4
  (`automation/elisa_auto/stats.py`).
* **Per cartridge:** 2 blanks (run positions 1 and 16) + 1 mid control (30 pg/mL, position 8) among the 16
  determinations (docs/12 §3.6; ≈ F18's 2 per 10). Acceptance (own targets): blank within the lot blank mean ± 3 SD;
  control within ±20 % of its lot value. Blank 1 vs blank 16 tracks within-cartridge drift (NSB growth on stored
  conjugate, electrode drift).
* **Why lot calibration might suffice:** the exhaustive read makes the specific charge independent of electrode area
  and RC height (docs/12 §2.3 point 1; §3.5.2 here: collection 0.989 ± 0.02 over the D range); bead dose and conjugate
  dose come from the same lot vials. **Assumption to be tested** (M5 on 5 dies, C3 on ≥ 5 cartridges): if the
  cartridge-to-cartridge slope CV > 10 % (`ma.reuse.slope_drift_tolerance` 10 %), switch to a per-cartridge 4-point
  curve (costs 6–7 of 16 determinations, docs/12 §9 decision 6).

### 8.3 Carry-over

* **Per run (automatic):** PE2 net charge is compared with a threshold of **0.10 nC** (2× the background target; ≈ 2×10⁻⁵
  of a 10 ng/mL sample's signal by the §3.6 arithmetic; the same residual would add 0.10 × 900/285 = 0.32 nC ≈ 0.2
  pg/mL-equivalent to a 15-min accumulation, Derived).
  Above threshold: the run is flagged, an extra RC + BW flush and a repeat PE2 run before the drag; persistent → fault.
* **Rule:** any result > 100 pg/mL triggers 6 instead of 3 chamber cleaning rinses (docs/08 S6 alternative) and a
  flag on the next determination in the same chamber.
* **Validation (per lot, not per cartridge):** 3 × (10 ng/mL → B1 → B2) per chamber, read through the low-range slope;
  criterion ≤ 1×10⁻⁴ (`gates.yaml` `carryover`, docs/08 S6), separately for (a) the same chamber (IC + WL branch + RC)
  and (b) the other chamber (inlet manifold + WLc + RC).

---

## 9. Tolerance and failure analysis (top 10, FMEA style)

S = severity, O = occurrence (before mitigation), D = detectability (1 = always detected), each 1–5 [assessment].

| # | Failure mode | Cause | Effect | Detection | Mitigation | S/O/D |
|---|---|---|---|---|---|---|
| FM1 | Step-read background SD > 0.05 nC | double-layer/oxide charge not reproducible between Q_a and Q_b; E_rest window absent; contact or relay instability | LOD × up to 4 (§1.3: 0.55 nC → P 0.05) | docking QC (5 step pairs, §8.1); blank SD | small WE (D1), low ΔE, step pair (D2), quiet windows; **fallback R-flow on WE2 (D3)** | 5/3/2 |
| FM2 | Beads stranded in the wash lane or not following the drag | bead–foil friction/adhesion; gap > 0.2 mm; magnet speed too high | carry-over into the next run of chamber k; signal loss | 10 ng/mL challenge series (§8.3); optical check in mock-ups only | 0.20 mm/s (0.35 v_max), gap 0.16 ± 0.05 mm, flat-floor gates, second pass option, WLc flush each run | 5/3/3 |
| FM3 | Residual activity in the RC > 10⁻⁴ | beads not fully dragged out; enzyme adsorbed on WE/foil; HQ from BW through G4 | carry-over; biased low samples after high ones | **PE2 every run** | bead-out + flush with BW (D10); threshold 0.10 nC; extra flush | 4/3/1 |
| FM4 | Chamber mixing factor near 0.2 | swirl does not lift beads; beads settle on the floor between strokes | capture × 0.2–0.5 → LOD × 2–5 (docs/08 §10.2) | M2 capture-vs-time | tangential jet, 30-s strokes, pauses identical in every run; switch to faster strokes or magnetic agitation with M_c if M2 fails | 4/3/2 (bench) |
| FM5 | Bead dose CV > 5 % or drift over 8 h | vial agitation insufficient; settling in the line; air-gap variation; port trapping | NSB variability → P 0.26 → 0.20 at CV 0.10 | E2.2 (gen-1) and M3 counts; blank 1 vs 16 | V2 (§5.4), line return before each dose, chase volume | 4/2/2 |
| FM6 | Valve or gate leak / failure within 40 (60) cycles; bead trapping at a seat | TPE creep, seat fouling with BSA/beads, bond delamination | RC not sealed (product loss, noise path), cross-talk between chambers | docking leak test; PE2; isolation EIS in M4 only | 3× life endurance gate (M4), flat-floor gates, fail-closed springs | 4/3/3 |
| FM7 | Pre-electrolysis ineffective or harmful | escape > 4 %; E_det oxidises HQDP or forms side products; BQ reduced back at E_rest | free-HQ background as without PE (S4a kill if the lot is bad) | E1.2b (gen-1), M5; PE1 background trend | stubs ≤ 0.2 mm, small CE/RE pocket, PE2 as second removal; lot acceptance U3 still applies | 4/3/2 |
| FM8 | Bubble in the RC or wet-out of a PTFE vent | gas from warming liquids; nucleation at the die edge; Tween wetting the PTFE | RC volume and area wrong (exhaustive read assumes a full layer); vent leaks liquid | CV area check at docking; PE1 charge anomaly; drip tray | HQDP stored at 25 °C (D8), fill at 40 µL/min from the floor side, degassed A1 (option); vent material test in M6 | 4/3/2 |
| FM9 | Reference drift > 20 mV or E_det off-plateau | Au QRE surface change; Cl⁻ change in the pocket; Ag/AgCl dissolution | collection < 1, background changes | step-pair background trend; control at position 8 | substrate-only RE pocket flushed each run; Ag/AgCl if available; E_det chosen mid-plateau; docked Ag/AgCl check in M5 | 3/3/3 |
| FM10 | On-card conjugate or HQDP degraded (shelf or 8 h) | storage time/temperature; Pi from hydrolysis; conjugate aggregation | NSB rise, slope change, ULOQ loss | blank 1 vs 16, control at 8; card expiry | dock fill at insertion (D12) until shelf data exist; 4–8 °C conjugate zone; HQDP ≤ 8 h at 25 °C (≤ 0.17 µM Pi) | 3/3/2 |

Tolerances that matter most (from §2–3; values UNVERIFIED unless derived): RC height 0.20 ± 0.02 mm (affects τ only:
18 ± 3.7 s; F(90 s) ≥ 0.98 even at +0.02 mm and the low D); magnet gap 0.16 ± 0.05 mm (drag margin 2.8× → ≈ 2×); MC
volume ±1.7 % (systematic, calibrated per lot); die position ±0.1 mm in the pocket (rim 50 µm → WE edge must not
leave the RC: requires ±0.05 mm, so the die is located on moulded datum edges, not by the adhesive bead).

---
## 10. Staged development plan with gates

Rule (docs/12 §10, user checkpoint): **no cartridge spend before G1** (docs/06 §4.11, weeks 7–8) unless justified;
mould tooling only after the bead-transfer, valve and readout risks are retired. Risks A1–A5 are those of docs/12
§3.11; A6 (read background, new here) is added.

### 10.1 Stage C0 — desk work and quotes (weeks 0–8, no orders)

* Quotes and lead times only: milled COC prototype bodies and the 6 mm mould insert (ChipShop, CS_FAB: "price on
  request"); custom die with WE1/WE2/CE/RE and an Ag/AgCl option (Micrux custom, MICRUX_TF; IMT, IMT_FLYER); TPE
  membrane lamination; dock items of §6.2.
* Questions to the foundries (§12): TPE/COC bond under cycling; 0.20 mm web tolerance under the die; die datum and
  bonding; Ag/AgCl availability; 50 µm boss for the WE2 channel.
* **Justified exception — M5a, weeks 6–8, cost class low:** step-pair background and collection on a **catalogue**
  Micrux thin-film single electrode (DI_MICRUX_SINGLE, geometry UNVERIFIED) or IDA die used as a single WE (BASI_IDA)
  under a laser-cut 0.2 mm spacer, with the Gamry already in hand and the Stage-1 substrate and HQ standards. Why
  before G1: it decides the read mode (step pair vs flow) for A **and** for the fallback B (same detector), it uses no
  Stage-2 hardware, and its pre-electrolysis arm adds the cell-geometry escape fraction to E1.2b. Run only after
  E1.1/E1.2/E1.2b (it must not delay G1a) and only if the user approves the spend.

### 10.2 What the gen-1 rig answers for A (no cartridge needed)

| Question for A | gen-1 experiment | Feeds |
|---|---|---|
| bead-dose CV of a cooled, agitated bead reservoir over 8 h (V2) | E2.2 (docs/06) | §5, FM5 |
| pre-electrolysis removes free HQ; side effects | E1.2b | §3.6, FM7 |
| U1 conjugate NSB, U3 free HQ / k_h, conjugate reservoir ageing (shelf, D12) | E1.3 (+ ageing arm), E1.2 | G1; §5.3 |
| Inject Start wiring, line code, Empower injection overhead (cadence 31 min), Loop Offline behaviour | S0.3 and Stage-2 commissioning | §7.2 |
| BSM at 1 µL/min into a bypass (back-pressure) | open bench item docs/08 §10 | §3.1 |
| SM-FL + inlet-line carry-over with the 2-min flush (D13) | E1.10 with a 10 ng/mL challenge, extended by the flush programme | §3.1 |
| phosphate tolerance and ULOQ at 3 mM HQDP | E1.7 | §3.5.6 |

### 10.3 Stage C1 — mock-ups (after G1 GO / GO-WITH-LEVER; weeks 9–16, in parallel with gen-1 Stage 2)

Prototype route: CNC-milled COC (or laser-cut PMMA laminate for M1/M2) bodies, 140 µm COC foil, adhesive-tape or
solvent bonding (docs/11 §1.3), CS_1367 catalogue chips for valve tests, magnets on a motorised stage, catalogue
Micrux dies; PDMS only for visualising bead motion, never for electrochemistry (docs/11 §1.4).

| Mock-up | Retires | Method | Acceptance (quantitative) |
|---|---|---|---|
| **M1** bead collection, gather, drag, bead-out, BW hold | A1 | IC + throat + 20 mm lane + RC + BW geometry; M-280 SA beads (blocked, as docs/06 §4.0) counted (fluorescent or hemocytometer, ≥ 400 counted per sample); magnet gap 0.16 mm; speeds 0.1–0.8 mm/s; n = 20 transfers | overall transfer ≥ 0.95 (mean), every run ≥ 0.90; **stranded in lanes ≤ 50 beads per pass (10⁻⁴ of 5×10⁵)**; beads left in RC after bead-out ≤ 50; BW retention at 40 µL/min ≥ 99.9 %; follow speed v_max ≥ 0.5 mm/s (≥ 2.5× design) |
| **M2** chamber mixing and analyte recovery | A2 | E3.3 analogue on the 176 µL foil-floor chamber with tangential tidal jets (with the pause pattern of §7.1) vs rotated tube; IgG spike recovery after 30 min vs LoBind tube | capture at 30 min ≥ 0.80 of the rotated tube (docs/06 E3.3 criterion); analyte recovery ≥ 0.90 |
| **M3** dosing | A3 | V2: 20 bead doses through a face-seal port over 8 h, counted; conjugate fill-to-vent meter: 20 doses read by ALP activity; vent wet-out after 20 fills | bead CV ≤ 5 % and 8-h trend ≤ 5 %; conjugate CV ≤ 5 %; no vent wet-out |
| **M4** valves and gates | A4 | each type (seat valve, flat-floor gate) 180 cycles (3× the busiest valve's life incl. fallback) with bead suspension, 1 % BSA conjugate buffer, 3 mM HQDP pH 9.5; leak at 20 kPa and 50 kPa; burst at 3 bar (CS_1367 rating); EIS across a closed valve; bead count at gate seats | leak ≤ 0.1 µL/min at 20 kPa after 180 cycles; ≥ 1 GΩ closed; ≤ 10 beads retained per gate per 20 passes; no delamination |
| **M5** readout (M5a may run before G1) | A5, A6 | 1 µL / 0.2 mm cell on a die: (a) step pairs on substrate fills, E_rest window and E_det plateau by CV, autorange vs fixed range; (b) HQ standards 1–100 nM, collection; (c) HQDP spiked with 10⁻⁴ HQ before/after PE1 + PE2; (d) 5 dies; (e) Au QRE vs docked Ag/AgCl over 8 h | **SD(Q_a − Q_b) ≤ 0.05 nC** (n ≥ 20, ≥ 3 dies); collection ≥ 0.95, die-to-die slope CV ≤ 5 %; escape ≤ 4 %; QRE drift ≤ 20 mV / 8 h. If the SD criterion fails: same tests in R-flow on a WE2-type channel, baseline-corrected charge SD ≤ 0.05 nC |
| **M6** thermal, bubbles, dew point | FM8, §6.5–6.6 | two-zone dock mock-up with a milled card; 8 h of fills | zones ±0.2 °C (assay) and 4–8 °C (reagent); no bubble in the RC in 20 fills; no condensation at the die |
| **M7** integrated single-chamber mock-up | system | one IC + lane + RC on a milled card with a custom or catalogue die, gen-1 reagents, sample delivered by a syringe pump (no Waters); 10 blanks + 3 × (1, 10, 100, 1000 pg/mL); 3 × (10 ng/mL → B1 → B2) | LOD ≤ 1.5 pg/mL (G2 go threshold, `gates.yaml` G2 `lod_pgml`); carry-over ≤ 1×10⁻⁴; PE2 flags the challenge correctly |

**Gate GC1** (end of C1): M1, M4 and M5 pass (A1, A4, A5/A6 retired); M2/M3 pass or have a defined fix. Enter the
measured mixing factor, dose CV and transfer into the model (docs/06 §9 path; scratch-copy scenario runs for the
chip-specific factors as docs/12 §8). GO → C2.

### 10.4 Stage C2 — prototype cartridges and dock (after GC1 and gen-1 G2, ≈ weeks 17–28)

10–20 milled COC cards with laminated TPE membranes and the custom die; first dock (plunger head, carriage, pumps,
two thermal zones, pogo head, controller with watchdog); automation as §7.3. Tests on the Waters stack: three
16-run cartridges in staggered two-chamber operation. Acceptance (**Gate GC2**): LOD ≤ 1.5 pg/mL per cartridge and
≤ 1.0 pooled (G3 target, `gates.yaml`), blank CV ≤ 0.10, card-to-card slope CV ≤ 10 % (else per-cartridge calibration,
§8.2), carry-over ≤ 1×10⁻⁴ for both paths of §8.3, time to result ≤ 60 min in every run, zero valve failures in 3
cartridges, docking leak test pass rate 100 %. GO → C3.

### 10.5 Stage C3 — moulded pre-series and validation

Mould insert and injection moulding (MOQ 100, CS_FAB), bonded die, factory or dock fill per D12; validation per
docs/06 Stage 4 (G3: LOD ≤ 1 pg/mL, blank CV ≤ 0.10, carry-over ≤ 1×10⁻⁴, ≤ 60 min).

### 10.6 Order relative to gen-1 gates

```
gen-1:  Stage 0/1A ──E1.1─E1.2─E1.3── G1a(wk5) ──E1.2b, E1.4-1.10── G1(wk7-8) ── Stage 2 (wk 9-16) ── G2(wk16) ── Stage 3
cart A: C0 quotes ─────────────────────────── [M5a, wk 6-8, if approved] ──┤ C1 mock-ups M1-M7 ── GC1 ──┤ C2 ── GC2 ── C3
                                              STOP at G1 → no cartridge spend (C0 stays desk work)
```

---

## 11. BOM additions by stage

Cost class [assessment, no prices seen unless stated]: **low** < €1 k, **medium** €1–10 k, **high** > €10 k.

| Stage | Item | Qty | Cost class / price | Source |
|---|---|---|---|---|
| M5a | Micrux catalogue thin-film single electrode or IDA dies (used as single WE) | 5–10 | price on request → low–medium | DI_MICRUX_SINGLE, BASI_IDA, PALMSENS_IDA |
| M5a | laser-cut 0.2 mm spacers, clamp cell (machined PMMA/PEEK), pogo pins | — | low | docs/11 §1.3 |
| C1 | ChipShop membrane-valve chip Fluidic 1367 (valve endurance baseline, M4) | 10 | **€34.40 each from 10** (€42.20 single) | CS_1367 |
| C1 | CNC-milled COC mock-up bodies (IC/lane/RC, valve and gate test coupons), COC foil 140 µm | 20–40 | price on request → medium | CS_FAB, DARWIN_CS4CH |
| C1 | NdFeB magnets (10×10×5, 2×2×4, 3×3×4 mm), motorised X–Y–Z stage | 1 set | stage: medium (Zaber, price not read) | ZABER_SW |
| C1 | bead-dosing pump with selection valve and holding coil; cooled rocking vial holder (V2) | 1 | medium (Cavro Centris / Hamilton PSD/4, price not read) | TECAN_CENTRIS, HAMILTON_PSD4 |
| C1 | pressure controller 2 channels (conjugate tank, meter vent) | 1 | medium (Fluigent Flow EZ / Elveflow OB1, price not read) | FLUIGENT_FLOWEZ, ELVEFLOW_OB1 |
| C1 | catalogue Micrux dies for M7; custom die design (mask) if M7 uses it | — | medium–high (custom: price on request) | MICRUX_TF |
| C2 | custom electrode die (WE1, WE2, CE, RE, contact loop; Au; Ag/AgCl option), wafer run | 1 run | high (price on request) | MICRUX_TF, IMT_FLYER |
| C2 | milled COC prototype cards with TPE membrane lamination and PTFE vents | 10–20 | medium–high | CS_FAB |
| C2 | dock: 20 plunger actuators, X–Y–Z carriage, M_h lift, 4 syringe pumps (S_b, S_IC1, S_IC2, S_RC), 3 Peltier zones with drivers, controller with hardware watchdog, face-seal manifold, pogo head and shielded sub-enclosure, low-leakage relay, sensors (T, RH, leak, pressure, card ID), flow sensors | 1 | high (mostly "to be selected") | docs/11 §5; §6.2 |
| C3 | mould insert, injection-moulded pre-series (MOQ 100), die bonding, fill | 100 | high (price on request) | CS_FAB |
| all | reagents as gen-1 (beads, conjugate, HQDP 3 mM — ≈ 3× the substrate mass of 1 mM per volume, but ≈ 45 µL per run vs ≈ 315 µL in gen-1) | — | as docs/07 | docs/09 §3.3 |

Reused from gen-1 (docs/07): Gamry Reference 600+, LabJack-class isolated DAQ, Python orchestration, SM-FL/BSM;
gen-1's IDEX valves and SIA pump are not needed by the cartridge (the SIA pump class is reused as S_b).

---

## 12. Open questions and UNVERIFIED list

### 12.1 Open questions (for the user or the next agent)

1. Accept **cadence 31 min / result 58.0 min** (vs 27.5 / 54.0 in docs/12), or trade 2 min of accumulation for margin?
2. Accept **D12** (dock fills RCj and RS at insertion) until shelf data exist? It changes the card's fill ports and the
   docking time, not the run.
3. Accept **3 mM HQDP** as a requirement (ULOQ 3040 vs 1360 pg/mL at 1 mM with the 1 µL RC)? It quadruples the free-HQ
   charge that pre-electrolysis must remove (§3.6).
4. Approve **M5a before G1** (§10.1)? It is the only pre-G1 spend proposed.
5. Second potentiostat channel for WE2 (fallback), or a dock relay?
6. Should the gen-1 inlet-line flush finding (D13: 7×10⁻³ carry-over without a post-transfer flush; Derived) be carried
   into gen-1's own step table? Gen-1 pushes 2 loop volumes into the cup and keeps the loop in line during the
   incubation shunt (`cycle_primary.yaml`), so its line is flushed by the 3 mL shunt — probably not affected; to be
   confirmed by whoever owns docs/06.
7. Foundry questions: TPE–COC bond endurance; 0.20 ± 0.02 mm web under a 10 × 6 mm pocket; 50 µm boss; die datum edges;
   Ag/AgCl on the die; PTFE vent heat-staking on COC.
8. Model extensions (docs/09 §5.4 items 1, 2, 3, 6, 8) remain unbuilt by user decision; the read background (§3.5.4)
   is a new item for such an extension (step-read charge noise of a stopped single-WE detector).

### 12.2 UNVERIFIED values used in this document

| Value | Where used | Status |
|---|---|---|
| M-280 saturation magnetisation 1×10⁴ A/m (moment 1.15×10⁻¹³ A·m²); saturation above 0.15 T | §3.3.2 forces | UNVERIFIED (no bead magnetic data in the repository) |
| NdFeB B_r 1.3 T | §3.3.2 | UNVERIFIED |
| near-wall drag factor 3 | §3.3.2 | UNVERIFIED (textbook order) |
| bead–foil friction / adhesion | §3.3.2 | unknown; measured in M1 |
| C_dl ≈ 20 µF/cm² for thin-film Au | §3.5.4 | UNVERIFIED (repository note) |
| E_rest window, E_det plateau, Au oxide onset at pH 9.5 | §3.5.4 | UNVERIFIED; CV in M5 |
| Au QRE drift ≤ 20 mV / 8 h; Ag/AgCl availability on custom dies | §3.5.5 | UNVERIFIED |
| buffer/substrate conductivity 1.6 S/m | §3.5.5 R_u | `hw.tubing.buffer_conductivity`, UNVERIFIED |
| K_m 0.1 mM, k_cat 1000 s⁻¹, free HQ 10⁻⁵, k_h 10⁻¹⁰ s⁻¹ | §3.5.3, §3.6, §5.3 | repository values, UNVERIFIED / low confidence |
| loop ID 0.5 mm; transfer 0.90 at 1.5 loop volumes | §3.1 | `hw.smfl.loop_inner_diameter` UNVERIFIED |
| injection overhead ≈ 1 min (cadence 31 min) | §7.2 | `hw.smfl.injection_overhead_time` UNVERIFIED |
| drain residual ≤ 5 µL; film 10–30 µm | §3.2.3 | UNVERIFIED |
| Wang2013 2×10⁻⁵ carry-over applied to protein | §3.4 | measured for a small molecule; protein UNVERIFIED |
| chamber mixing factor; analyte loss to blocked COC | §3.1, §3.2.2 | UNVERIFIED; M2 |
| valve leak, isolation, endurance beyond 50 cycles; TPE thickness and bond | §4 | UNVERIFIED; M4 |
| PTFE vent wet-out with Tween/BSA | §3.2.4 | UNVERIFIED; M3/M6 |
| moulding tolerances (±10 µm meter, ±0.02 mm web, ±0.05 mm die position) | §5.3, §9 | UNVERIFIED |
| COC thermal diffusivity, water diffusivity, gas solubility vs T, Magnus constants | §6.5–6.6, D8 | UNVERIFIED |
| bead-dose CV of the V2 vial | §5 | to be measured (E2.2, M3) |
| pre-electrolysis efficacy and escape fraction 1–4 % | §3.6 | Derived from geometry; efficacy UNVERIFIED pending E1.2b/M5 |
| NaCl addition to the substrate (fixed Cl⁻) and its effect on ALP | §3.5.5 | UNVERIFIED |
| ToolkitPy step commands; Empower pressure-limit setting | §7.3, §4 | UNVERIFIED (docs/02 §4.3) |
| plunger force to seal; part numbers of actuators, Peltiers, relay, pogo pins, scanner | §6.2 | to be selected |

---

## Appendix A — scratch runs (not in the repository)

Model runs: the docs/12 Appendix A script, run from a copy of the repository in the session scratchpad, with these
additions (n = 2000, seed 20261111):

```python
A13 = Aarch(vol=1.0)          # docs/12 A with "ma.geometry.magnetic_trap_volume": 1.0 added to the design overrides
S3  = lambda p: p.with_values({"ma.chemistries.alp_hqdp.substrate_concentration": 3e-3})
base = lambda p: S3(pre_el(A_ps(p)))
L.mc(A13, base(ps0), n=2000, lod_scale=1/0.90)                                     # docs/13 A
L.mc(A13, base(F.scen("L6+L7")[1](ps0)), n=2000, lod_scale=1/0.90)                 # + screening
L.mc(A13, base(ps0).with_values({"ma.capture.bead_dose_cv": 0.10}), ...)          # dose-CV rows (0.05/0.10/0.15)
L.mc(A13, base(ps0).with_values({"ma.capture.magnetic_trap_efficiency": 0.80}), ...)
L.mc(A13, base(ps0).with_values({"hw.gamry.noise_rms_flow": 2e-11}), ...)         # read-background sensitivity (2e-11, 1e-10)
```

Magnet fields (§3.3.2): uniformly magnetised blocks (B_r = 1.3 T) represented by their two charged pole faces,
B(r) = (B_r/4π) ∬ (r − r′)/|r − r′|³ dA′ summed over the faces (60 × 60 grid), |B| and its gradients by central
differences (±20 µm) at the bead plane 0.30 mm above the magnet face; results quoted in the §3.3.2 table.
