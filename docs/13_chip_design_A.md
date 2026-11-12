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
thin-film electrode die bonded face-down into a top pocket. Two stirred 170 µL incubation chambers (IC1, IC2) receive
the SM-FL plug (1.5 loop volumes) through on-card valves; beads (V2: from a cooled stirred dock vial through a
face-seal port) and conjugate (on-card cooled tank, fill-to-vent 10.0 µL meter) are dosed into the chamber just before
injection; after a 30-min one-step incubation with tangential-jet tidal mixing, a dock magnet carriage collects the
beads, gathers them to the chamber throat, the chamber is drained and rinsed twice, and a small high-gradient magnet
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
| D1 | RC 4 × 10 mm × 50 µm = 2 µL; WE 37 mm² | **RC 2.6 × 2.0 mm × 0.20 mm = 1.04 µL; WE1 2.5 × 1.9 mm = 4.75 mm²**; 3 mM HQDP | A step read on a 37 mm² WE carries a double-layer charge of ≈ 2.6 µC against a 1.5 nC signal at 1 pg/mL (§3.5.4, Derived): the subtraction would need a repeatability of 2×10⁻⁵. Cutting the area 7.8× (thicker layer, half the volume) and the step height (0.35 → 0.15 V) lowers the charge to ≈ 0.14 µC (needed repeatability 3.5×10⁻⁴). Exhaustive collection is kept: τ = 18 s, 90-s steps collect 99.5 % (§3.5.3). The model is neutral to the volume change (P 0.26 at 1 and 2 µL, 3 mM; ULOQ 3040 vs 6810 pg/mL; §3.5.6) |
| D2 | single step read; background "measured on the same fill" by PE1 | **double-step read** (E_rest → E_det 90 s, back 15 s, E_det 90 s again) with Q_net = Q_a − Q_b; E_rest instead of open circuit before each step | the charging and oxide charge of the second step cancels that of the first on the same electrode within 2 min; PE1 happens 25 min earlier from an undefined open-circuit potential and cannot cancel it [assessment] |
| D3 | no fallback read mode | **WE2 thin-layer flow detector (1.0 × 3.0 mm channel, 50 µm) downstream of the RC on the same die** | if the double-step background (gate M5b) fails, the RC contents are swept at 10 µL/min over WE2 held at constant potential — the gen-1 readout that the model actually represents (thin-layer conversion 0.78 at 10 µL/min, docs/09 §5.2) — without a new die |
| D4 | CE and RE at the end of a dead-end 2 mm × 0.1 × 0.05 mm side channel (R = 250 kΩ) | **CE/RE in a 0.024 µL pocket behind a 0.2 × 0.2 × 0.5 mm neck, flushed at every fill through its own valve**; R_u ≈ 12 kΩ | a dead-end branch accumulates CE reaction products over 20 runs next to the reference; R_u·C_dl = 250 kΩ × 7.4 µF = 1.9 s would have overlapped the 1.1-s thin-layer collection (Derived, §3.5.5) |
| D5 | collection magnets M1a/M1b + drag carriage M2 | **one carriage with a collection magnet (10 × 10 × 5 mm) and a drag magnet (2 × 2 × 4 mm), plus a fixed-position hold magnet under the RC and a permanent magnet under the bead-waste pocket** | field arithmetic §3.3: a block that collects from 3.7 mm height in seconds cannot drag a pellet precisely, and a small magnet with ≈ 350 T/m lateral gradient cannot collect from the far wall of an 8 mm chamber |
| D6 | gates G1–G4 (type unspecified) | **flat-floor gates, actuated from the top through the TPE membrane** | the magnet path runs under the foil floor, so the gate plungers cannot be there; a flat floor has no seat ridge for beads to catch on (docs/10 §7: no data on bead trapping at seats) |
| D7 | V1 placement (beads on the card, tidal-resuspended tank) | **V2 recommended** (§5): bead stock in a cooled, rocked dock vial, metered by a Cavro/PSD-class pump | removes the least-evidenced element (on-board liquid bead suspension; docs/10 §9.3, §6.1) and the shelf-storage bead cake; reuses gen-1's reservoir and its E2.2 dose-CV data; −2 card valves and one pressure channel |
| D8 | HQDP tank 2 mL at 4–8 °C | **HQDP tank 1.5 mL in the 25 °C assay zone during use** (cold only in storage) | 8 h at 25 °C makes ≤ 0.17 µM Pi at 3 mM even at the acceptance-limit k_h (§5.3), and the HQ formed is removed by pre-electrolysis; filling a 0.2 mm RC with 4 °C liquid that warms to 25 °C invites bubble nucleation [assessment; gas solubility values not in the repository, UNVERIFIED] |
| D9 | 21 valves; 7 actuations per run for the tidal valves | **16 membrane valves + 4 gates = 20**; tidal mixing by dedicated dock syringes behind normally-open floor-port valves (valve not cycled per stroke) | busiest valve ≈ 4 actuations per run, ≈ 40 per cartridge (§4) vs 70 in docs/12 — inside the only thermoplastic endurance figure (> 50, CHILDERS2024) |
| D10 | bead pellet in a 1 × 1 mm pocket at the RC end; beads to a 16-dose bead-waste pocket | pellet held under WE1 by the hold magnet; **bead-waste pocket flushed every run** through its own valve; beads held there by a fixed magnet | product made by spent beads in a stagnant pocket would otherwise leak back into the RC when G4 opens (§3.8) |
| D11 | cadence 27.5 min; result 54.0 min | **cadence 31.0 min; result 58.0 min** | double-step reads (3.25 min each), 90-s steps, gather step and 2.0-min drag lengthen the transfer and RC occupancy (29.75 min of every 31, §7.1); still ≤ 60 min (docs/00); 16 samples ≈ 8.3 h |
| D13 | the 10 % plug tail goes to the bypass | **BSM keeps 100 µL/min to the bypass for 2 more min (3.5 loop volumes in all), then Loop Offline** | without it the inlet line holds loop-tail liquid that would carry ≈ 7×10⁻³ of a sample into the next chamber (§3.1, Derived) |
| D12 | — | RS/RCj **factory-filled only if shelf-life data allow**; default: filled by the dock at insertion from dock bottles | at the acceptance-limit k_h a factory-filled 3 mM HQDP reaches the 1 µM Pi limit in 1.9 days (docs/12 §2.3, Derived again §5.3); no conjugate data beyond 24 h (docs/06 E1.3) |

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
matters for the LOD (NSB is carried by the beads too) — it matters for carry-over (§3.3.6); (iv) **the read
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
| beads → ICk (V2) | dock vial → holding line → P_b → V4/V5 → IC | 10.0 µL bead slug + 3.0 µL A1 chase | 0.6 + 1.2 + 1.0 = 2.8 µL ≤ chase | Derived |
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
  150 + 10 (beads) + 3 (bead chase) + 10 (conjugate) = **173 µL**; capture gain vs gen-1 0.90/1.73 vs 0.96/2.2 =
  **×1.19** (Derived as docs/12 §2.2, which used 170 µL → ×1.21).
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

**3.2.1 Geometry.** Ø 8.0 × 5.0 mm (251 µL), 173 µL working (fill height 3.44 mm), flat foil floor, PTFE vent in the
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

**3.2.3 Drain.** After collection, S_ICk aspirates the chamber through P_dk at 200 µL/min (≈ 0.9 min for 173 µL) and
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
| 35.0–38.0 | drain + 2 rinses with M_c holding (§3.4) | — |
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

* **Chamber rinses** (pellet held by M_c at the throat): drain (0.9 min), then 2 × (100 µL A1 at 200 µL/min, no tidal
  strokes, drain) ≈ 3.0 min. Free conjugate left: (105/5)² = 441× dilution → 0.3 nM / 441 = 0.7 pM in ≤ 5 µL =
  2.1×10⁶ molecules (docs/12 §3.8).
* **Wash lane**: refreshed with 10 µL A1 at t = −5 min (before the chamber is dosed): S_RC → P_w → V11 → J → WLk →
  open G_k → empty ICk (5 µL, then drained by S_ICk), then J → WLc → V12 → waste (5 µL). The pellet then crosses
  20 mm of clean, still A1.
* **Free conjugate carried into the RC**: Wang2013 substrate carry-over with the beads < 2×10⁻⁵ of the source-well
  content (small molecule; protein UNVERIFIED) × 2.1×10⁶ = **≤ 42 molecules**, against ≈ 5700 NSB enzymes in the nominal
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
