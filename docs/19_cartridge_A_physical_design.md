# 19 — Cartridge A: physical design of the card (C2 laminated prototype)

Status: 2026-11-13, **stage C0 desk work**, physical design round (CARD). Nothing is ordered. Inputs: docs/13 Revision B
(§2–§5), docs/18 (binding interface), `cad/elisa_cad/interface.py` (imported, not edited), docs/11 §1–§4, docs/16
§2–§3/§6.4. This document changes no other document. CAD: `cad/elisa_cad/card/` (CadQuery 2.8); outputs:
`cad/out/card/`; rebuild: `cd cad && python -m elisa_cad.card.build` (≈ 25 s, 35 files).

Source tags as docs/13 and docs/18: docs section | `interface.NAME` | **Derived** (arithmetic shown) | **CHOICE-Cn**
(§7) | **DEV-Cn** (§8) | **UNVERIFIED** | [assessment]. Units mm, µL = mm³, N, g.

## 1. Summary

* The card is drawn as **10 parts** in the docs/18 z-stack: L0 foil, L1 channel sheet, L1s WE2 shim, L1b die film,
  L2 TPE, seam adhesive, L3 milled body, die (glass + metal + passivation), L4 PTFE discs with adhesive rings. All
  21 valve sites, 11 liquid ports, 2 gas ports, chambers, tanks, meter, cell, BW and die are real solids/cuts
  (0.175 channels, 0.05 WE2 channel, 0.2 µm metal).
* Fabrication files for a laminate shop: closed-polyline **DXF + SVG** of L0, L1, L1s, L1b, L2 (finished geometry,
  kerf compensation by the shop); **die mask** DXF (layers DIE_OUTLINE, METAL, PASSIVATION_OPEN) + SVG.
* Checks on the CAD (§6): every docs/13 volume is reproduced within 2 % except where a docs/18 or card deviation
  is listed; all 21 tips land centred on their channel with full TPE cover under the worst-case 0.14 position
  error; minimum milled L3 web 0.5 (by construction); dry mass 20.3 g.
* Main card-level decisions: meter drawn as a **Ø1.596 bore** of the same area (DEV-C1, a 2.0 × 1.0 × 4.4 blind
  rectangle cannot be milled); **V12 and G3 bores merged** (0.45 web); the die electrode pattern is routed in one
  metal layer, which forces the **G4 finger to stop 0.25 inside the die edge** (DEV-C2, WE1 5.13 mm²); a
  **poka-yoke chamfer** at the back-right corner needs a matching nest block (interface change request §9).

## 2. Parts (card coords, z = 0 = foil underside; files in `cad/out/card/`)

### 2.1 Stack

| Part | z (mm) | Outline | Material / stock | File |
|---|---|---|---|---|
| L0 foil | 0–0.140 | L3 outline − 0.2 (`LAMINATE_INSET`), R0.8 corners, chamfer 3.883 | COC foil 140 µm (docs/13 §2.1) | `card_L0_foil.step`, `cut_L0_foil.dxf/.svg` |
| L1 channel sheet | 0.140–0.315 | as L0 | COC sheet 0.175 (docs/13 §2.1) | `card_L1_channel_sheet.step`, `cut_L1_*.dxf/.svg`, `plan_L1.png` |
| L1s WE2 shim | 0.140–0.290 | 2.88 × 0.98 in the WE2 slot | COC 0.150 (docs/13 §2.3) | `card_L1s_WE2_shim.step`, `cut_L1s_*` |
| L1b die film | 0.315–0.340 | die + 0.15 (6.3 × 10.3) | 25 µm double-sided adhesive (docs/13 §2.1) | `card_L1b_die_film.step`, `cut_L1b_*` |
| L2 TPE | 0.315–0.715 | as L0 | TPE 0.40 (`TPE_T`, CHOICE-15) | `card_L2_TPE.step`, `cut_L2_TPE.*` |
| seam adhesive | 0.340–0.715 | ring die … die + 0.10 | UV-curing adhesive (UNVERIFIED grade) | `card_seam_adhesive.step` |
| L3 body | 0.715–6.215 | 75.5 × 50.0, R1.0, chamfer 4 × 45° at (75.5, 50) | COC, CNC-milled | `card_L3_body.step` |
| die | 0.340–1.040 | x 55.0–61.0, y 23.35–33.35 | borosilicate 0.70 (UNVERIFIED), Au/Ti, SU-8/PI | `card_die.step`, `die_mask_*` |
| L4 discs | 5.94–6.14 (vents), 5.14–5.34 (MC stop) | Ø4.0 ×4, Ø3.0 ×1 | PTFE membrane 0.20 (UNVERIFIED) + 25 µm adhesive rings | `card_L4_discs.step` |
| assembly | 0–6.215 | — | — | `card_A_assembly.step` (named, coloured) |

Views: `card_iso_top.png`, `card_iso_bottom.png`, `card_exploded.png`, `plan_L1.png`,
`section_valves_y29.95.png`, `section_chamber_IC1_y38.6.png`, `section_cell_y25.png`, `section_die_x57.85.png`,
`zoom_valve_island.png`, `zoom_junction_cell.png`, `zoom_cell_electrodes.png`. Check results: `checks.json`.

### 2.2 L0 foil
Holes: 11 liquid ports Ø1.0 (`PORTS`, `PORT_HOLE_D`), contact window x 55.3–60.7 / y 29.8–33.2 (`CONTACT_WINDOW`),
lamination dowel holes Ø2.0 at (59, 42) and slot 2.0 × 3.0 at (59, 5) (CHOICE-C4). Nothing else: the foil is the
magnet wall and the datum-C face. Min web 2.4 (Derived, §6.2).

### 2.3 L1 channel sheet
Through-cuts = every polyline of `interface.CHANNELS` at its width (flat caps, round joins, as `interface_plan`)
∪ IC1/IC2 Ø8 minus the funnel walls (L1 kept inside the bore for x_c + 2.0 … x_c + 4.0, taper 2.5 → 0.5, docs/13
§2.3) ∪ RCj 10 × 10 ∪ RS 12 × 12 ∪ MC Ø1.596 (DEV-C1) ∪ BW 2.5 × 2.5 ∪ RC 2.6 × 2.0 ∪ CE/RE pocket + neck
(`CER_POCKET`, `CER_NECK`) ∪ 11 port holes ∪ contact window ∪ dowel holes. Local cut extensions inside other cuts
(CHOICE-C14): funnel throat to x_c + 4.1, nozzle mouths 0.4 into the bore, 0.4-wide strips joining RCj_to_MC and
conj_line to the round meter. The cut network encloses **5 islands** (208.7, 67.3, 32.7, 25.2 mm² and the
P_s/WE2/BW loop) → L1 is cut on a transfer liner and weeded before lamination (CHOICE-C15). Min web 0.23 (cusp at
the P_s port, §6.2).

### 2.4 L1s, L1b, L2, seam
* **L1s:** WE2 slot (x 58.1–61.0, w 1.0, `WE2_CHANNEL`) minus 0.01 per side; 0.15 thick → WE2 channel 0.05 under the
  die (docs/13 §2.3). Side gaps 2 × 0.01 × 0.2 × 2.9 = 0.012 µL (Derived) belong to the WE2 channel volume.
* **L1b:** outline die + 0.15 (docs/18 CHOICE-14); cut = L1 cut pattern ∩ die (cell, fingers, pocket/neck, WE2
  slot, RS_feed and G4 lane ends, contact window). In the 0.15 seam band the film is the ceiling of WLc, G4 lane,
  RS_feed and V14_out. Min web 0.15 (the seam band over a lane).
* **L2:** cut-outs IC1/IC2 Ø8, RCj, RS, MC Ø1.596, BW, die + 0.10, dowel holes; closed over ports, lanes and all
  valve sites. The film rim (die + 0.10 … + 0.15) lies under the TPE: drawn as a 25 µm relief = local TPE
  compression 6 % (CHOICE-C17).
* **Seam:** 0.10-wide ring between die and TPE edge, z 0.34–0.715, 1.2 µL adhesive (Derived from the solid).

### 2.5 L3 upper body (CNC)

| Feature | Geometry | Source |
|---|---|---|
| Chambers IC1, IC2 | Ø8.0 blind from below, z 0.715–5.715 (roof 0.5) | `IC1`, `CHAMBER_ROOF_T` |
| Vents IC1, IC2, RS, P_c | Ø2.0 hole in the roof + Ø4.4 × 0.3 top recess; disc Ø4.0 on a 25 µm ring (OD 4.0/ID 2.6) | `VENTS`, docs/18 §4/DEV-7; P_c CHOICE-C8 |
| RCj | 10 × 10, R1.0 vertical corners, z to 5.715, boss r 1.25 around V8 (web 0.50) | `RCJ`; CHOICE-C3/C13 |
| RS | 12 × 12, R1.0, z to 5.715 | `RS`; CHOICE-C3 |
| MC + stop | Ø1.596 blind to z 5.115; counterbore Ø3.4 from the top to z 5.115; Ø3.0 disc on a 25 µm ring → stop face z 5.140 | DEV-C1, CHOICE-C2, `MC.z` |
| Plunger bores | Ø1.5 (tip 1.0) / Ø1.2 (tip 0.8) through, coaxial with `VALVES`; lead-in 0.3 × 45° (V8: none, CHOICE-C10) | `VALVES`, `PLUNGER` |
| Merged bores | G1+G2 slot 1.2 × 3.06; V11+V12+G3 one slot (V11–V12 per `MERGED_BORES`, V12–G3 web 0.451 < 0.5 → merged, CHOICE-C11) | `MERGED_BORES` |
| Die window | x 55.00–61.10, y 23.25–33.35 through; datum faces x = 55.0 and y = 33.35 flush with the nominal die; free faces +0.10; Ø1.0 corner reliefs | `DIE_*`, CHOICE-C1 |
| Notches | G3 (−x face), V14 (+x), V15 and G4 (−y): bore joined to the window by a strip of bore width | `DIE_NOTCHED_BORES` (DEV-2) |
| Thermal break | through-slot x 20–24 except bridges y 3.5–6.5, 43.5–46.5; R1.0 slot ends | `X_BREAK`, `BREAK_BRIDGES_Y` |
| Dowel holes | Ø2.0 × 3.0 deep and slot 2.0 × 3.0 × 3.0 from below at (59, 42) / (59, 5) | CHOICE-C4 |
| ID area | 6.6 × 6.6 × 0.10 label recess around the 6 × 6 code area at (44, 0.8) | `ID_CODE`; CHOICE-C9 |
| Orientation | 4 × 45° chamfer at (75.5, 50) (all layers), engraved triangle 0.2 deep at (10, 2.5) | CHOICE-C7 |
| Clamp/press areas | the flat top minus the features above; vents and gas ports lie on their docs/18 positions | docs/18 §6 CHOICE-8 |

### 2.6 L4
Four Ø4.0 PTFE discs (IC1, IC2, RS vents; P_c headspace) and one Ø3.0 MC stop disc, each on a 25 µm acrylic
transfer-adhesive ring (C2 fixing, DEV-C3). Disc tops 0.075 below the L3 top (flat clamp face kept).

### 2.7 Die (lower face, card coords seen from the top; mask files mirrored, §2.8)

| Element | Passivation opening (electrode area) | Source |
|---|---|---|
| WE1 | RC − 0.05 per side (2.5 × 1.9) + G3 finger 0.5 × 0.4 (x 55.05–55.55) + G4 finger 0.45 × 0.4 (y 23.60–24.05) = **5.13 mm²** | docs/13 §3.5.1; DEV-C2 |
| WE2 | x 58.6–60.6 × y 24.45–25.55 (wetted 2.0 × 1.0 = 2.0 mm², width set by the channel) | docs/13 §3.5.1; CHOICE-C12 |
| CE | pocket − 0.02, minus the RE corner: L-shape 0.110 mm² | docs/13 0.3 × 0.3; CHOICE-C12 |
| RE | 0.10 × 0.10 at the pocket's −x/−y corner | docs/13 §2.3 |
| Pads | 6 × 1.2 × 1.0 metal at `PADS`; openings 1.1 × 0.9 | `PADS`, `PAD_SIZE` |
| Traces | WE1, WE2 0.20 wide straight up to their pads; CE, RE 0.04 wide down the +x edge (x 60.77 / 60.85), under the WE2 channel past WE2's end, along the −y edge (y 23.50 / 23.42) below the G4 finger to the pocket; RE along the +y edge (y 33.15) above the pad rows; LOOP 0.05 between LOOP_A and LOOP_B | CHOICE-C12 |
| Metal | Au 150 nm on Ti 50 nm, drawn 0.2 µm thick; openings + 0.01 (+0.005 at CE/RE) | docs/13 §2.1 |
| Passivation | SU-8/polyimide, whole face minus openings, drawn 1 µm (UNVERIFIED) | docs/13 §2.1 |

Net-to-net minimum spacing 0.025 (CE–RE at the pocket), ≥ 5 µm Micrux rule (docs/11 §2.1). Traces lie 0.05–0.18
from the die edges (dicing tolerance UNVERIFIED; a chipped RE trace shows as an open RE at docking).

### 2.8 Die mask export
`die_mask_layers.dxf`: die-local mm **looking at the electrode face**, origin at the die corner at card (61.0, 23.35),
u = 61.0 − x, v = y − 23.35. METAL is positive (metal where drawn), PASSIVATION_OPEN are holes in the passivation.

## 3. Materials and stock

| Item | Choice | Source / status |
|---|---|---|
| L3 body | COC plate ≥ 6 mm, milled to 5.5 | COC route docs/11 §1.2; density 1.02 g/cm³, Tg 134 °C, E 3200 MPa for TOPAS 5013L-10 (TDS, topas.com, opened); availability of COC **plate** stock UNVERIFIED |
| L0 | COC foil 140 µm | docs/13 §2.1 (ChipShop lid, DARWIN_CS4CH); sheet product UNVERIFIED |
| L1, L1s | COC sheet 0.175 / 0.150 | docs/13 §2.1, §2.3; thickness tolerance UNVERIFIED (sets the cell height) |
| L1b | 25 µm double-sided adhesive on liners | docs/13 §2.1 (docs/07 §5.3); product, creep, leachables UNVERIFIED |
| L2 | elastomeric COC / TPE 0.40 | docs/13 §2.1; eCOC membrane precedent docs/11 §3 (CHILDERS2024); grade UNVERIFIED |
| Seam | UV-curing adhesive, low viscosity | [assessment]; grade, HQ/BQ compatibility UNVERIFIED |
| L4 | PTFE membrane discs 0.20, adhesive rings 25 µm | docs/13 §2.1; product and wet-out UNVERIFIED |
| Die | borosilicate 6 × 10 × 0.70, Au/Ti, SU-8/PI | docs/13 §2.1, docs/11 §2.1 (Micrux custom); thickness UNVERIFIED |
| Dowels | Ø2.0 h6 stainless pins (fixture) | [assessment] |
| Label | polyester data-matrix label ≤ 0.08 | UNVERIFIED |

## 4. C2 fabrication and assembly sequence (10–20 cards)

1. **Cutting (laminate shop).** L0, L1, L1s, L2 laser-cut from the DXF (finished geometry; the shop applies kerf
   compensation). L1 is cut on a low-tack transfer liner and weeded so the 5 islands keep their positions
   (CHOICE-C15); a UV/short-pulse laser is preferred for the 0.3 channels [assessment]. L1b cut on its liners with the
   top liner cut to die − 0.3 (peel tab reachable through the window). Every laminate carries the two dowel holes.
2. **L3 machining.** Op 1 (bottom): face, dowel holes (become the op-2 datum), blind cavities (IC, RCj, RS, MC),
   through features to half depth. Op 2 (top, on dowels): face to 5.5, through features from the top (two-sided:
   L/D ≤ 2.75 for Ø1.0 tools, CHOICE-C18), counterbores, recesses, lead-ins, label recess, arrow, outline with
   chamfer and datum edges A/B in the same set-up as bores and window (feature-to-edge ±0.05, `TOL`). Deburr, clean.
3. **L0 + L1 (+ L1s).** On the dowel fixture: L0, then L1 transferred from its liner, L1s dropped into the WE2 slot;
   thermal press below Tg (CHOICE-C16; temperature/pressure UNVERIFIED, set on coupons so 0.3 channels do not creep).
4. **L1b.** Placed on the dowels from its carrier; bottom liner off; top inner liner stays.
5. **L2 → L3.** TPE laminated to the L3 underside on the dowels after UV/ozone activation at room temperature (eCOC
   route of docs/11 §3; COC–TPE bond strength UNVERIFIED).
6. **L3/L2 → L0/L1.** L1 top UV/ozone activated; stack pressed on the dowels. The TPE rim compresses over the film
   rim (CHOICE-C17).
7. **Die.** Inner liner peeled through the window; die lowered face-down, pushed by a spring jig against the datum
   faces x = 55.0 and y = 33.35, pressed (force UNVERIFIED).
8. **Seam.** UV adhesive dispensed into the 0.10 seam (free sides from above; datum sides by capillarity under the
   L3 overhang); cure; check through the foil that nothing wicked into the cell or lanes.
9. **L4.** Adhesive rings + PTFE discs into the four Ø4.4 recesses and the MC counterbore, pressed.
10. **Label** in the ID recess; card serial recorded.

**Inspection per card:** (a) measuring microscope through the clear COC: lane edges vs L3 bores at J and the cell
(accept ≤ 0.05, `TOL['L1_to_L3_registration']`), die vs datum faces (≤ 0.05); (b) visual: delamination, adhesive
in channels, island shift; (c) pads: contact-loop resistance and pad-to-WE isolation ≥ 5×10¹² Ω on a pogo
fixture (docs/13 §2.7); (d) **leak test** on a test anvil with plungers: pressure decay at 20 and 50 kPa per path,
valves closed (docs/13 §4 M4 levels; GC2 docking leak test 100 %, docs/16 §6.4); burst at 3 bar on sacrificial
cards only; (e) first article: MC volume gravimetrically, cell height by PE1 decay at docking (docs/13 §2.7).

## 5. Tolerances

| Item | Value | Source |
|---|---|---|
| Tip-to-channel position, worst case | 0.14 = 0.03 head-to-nest + 0.01 datum pin + 0.05 L3 edge-to-feature + 0.05 L1-to-L3 | Derived from `TOL` |
| same, RSS | 0.077 | Derived |
| L1-to-L3 budget (dowels, CHOICE-C4) | WC 0.051 / RSS 0.021: laser 0.010, dowel in L1 hole 0.010, L1 shrink 0.05 % over 20 mm 0.010 (UNVERIFIED), L3 hole position 0.010, dowel in H7 0.006, rotation 0.005 | [assessment]/UNVERIFIED; requirement 0.05 met only if the shrink and laser values hold |
| Stub 0.30 / cell stub 0.35 with RSS error | 0.22–0.38 / 0.27–0.43 (≤ 0.5 rule of docs/13 §2.6 kept) | Derived |
| Die in window | ±0.05 (datum faces flush, CHOICE-C1) | `TOL['die_in_window']` |
| WE1 opening vs RC film edge | 0.05 inset per side → WE1 area unchanged for die offsets ≤ 0.05 | CHOICE-C12 |
| MC bore Ø1.596 H7 (+0/+0.010) | volume +0 … +1.25 % (Derived 2 × 0.010/1.596) | DEV-C1 |
| Cell height 0.200 | L1 + film thickness tolerance UNVERIFIED (±10 % → τ ±21 %, docs/13 §2.7) | docs/13 |
| Card thickness 6.215 | L3 ±0.02 face-milled [assessment] + laminate UNVERIFIED | — |

## 6. Checks run on the CAD (`checks.py`, output `checks.json`)

### 6.1 Volumes from the solids vs docs/13 §2.3 / docs/18

Method: probe prism of the feature − (probe ∩ part solid), on the CadQuery solids.

| Feature | CAD | docs/13 (docs/18) | Note |
|---|---|---|---|
| IC1/IC2 total (foil to roof) | **278.9 µL** | 290 (280, DEV-7) | funnel walls occupy 1.2 µL of the L1 layer |
| IC working 185 µL fill height | 3.706 mm | 3.68 | DEV-C6 (+0.026) |
| C1, C2 (16.2 mm) | 1.415 µL | 0.26 (1.42, DEV-1) | = docs/18 |
| M_in (19.0 mm incl. bypass leg) | 1.653 µL | 1.05 (1.37) | docs/18 counts to V3; same polyline |
| WL1, WL2 (15.255 mm) | 1.335 µL each | 1.31 (1.34) | = docs/18 |
| WLc J → die edge (5.0 mm) | 0.438 µL | 0.39 (to G3, 4.4 mm) | interface runs to x 55.0 |
| RC | 1.040 µL | 1.04 | — |
| lane fingers in die (G3 0.5 + G4 0.65) | 0.050 + 0.065 | 0.115 | — |
| WE2 channel (2.9 × 1.0 × 0.05 + shim gaps) | 0.157 µL | 0.175 incl. "link" | interface length 2.9 (docs/13 text says 3.0) |
| **cell** | **1.312 µL** | **1.34** | −2.1 % (DEV-C4) |
| CE/RE pocket + neck | 0.044 µL | 0.044 | — |
| BW | 3.594 µL | 3.6 | — |
| **MC foil-to-stop** | **9.996 µL** (+0.029 µL adhesive-ring gap) | **10.0** | DEV-C1 |
| RCj L3 / + L1/L2 | 495.7 / 553.2 µL | 500 / 560 | R1 corners, V8 boss (DEV-C5) |
| RS L3 / + L1/L2 | 715.7 / 798.5 µL | 720 usable | R1 corners (DEV-C5) |
| port hole Ø1 × 0.315 | 0.247 µL | 0.24 | — |
| bead path (2.5 line + port + rung + C_k part) | 3.596 µL | (3.54) | < 4 µL chase kept |
| conjugate lines MC → V6 / → V7 | 0.725 / 1.428 µL | (0.73 / 1.43) | = docs/18 |

### 6.2 Minimum webs per layer (opening test with mitre joins; corner cusps < 0.003 mm² ignored)

| Layer | Min web | Where | Limit used | Verdict |
|---|---|---|---|---|
| L0 | 2.40 | P_rf port to edge | — | ok |
| L1 | 0.23 | cusp between V14_out and the P_s port hole | channel ≥ 50 µm guideline (docs/11 §1.3, DATRON_POTOMAC) | ok; bonded to L0 |
| L1b | 0.15 | seam band over the lanes | tape cut width ≥ 0.2 (docs/11 §1.2, DARWIN_CSTAPE) applies to cut widths, smallest film cut 0.30 (RS_feed) | ok, band is liner-supported |
| L2 | 1.30 | RS cut to edge | — | ok |
| L3 bores/cavities | **0.50** V8 ↔ RCj (boss, CHOICE-C13); then 0.76 V2–V3, 0.84 G1G2 ↔ V11V12G3 group, 0.85 V6–V17 / V7–V18 | — | 0.5 milled web 5.5 tall [assessment] (CHOICE-C19) | ok after merging V12–G3 (0.451) |
| L3 to card edge | 1.5 (RS wall at x 74) | — | — | ok |
| L3 thin floors | roofs 0.5; **0.2 under the vent recesses**; MC ledge 0.90 wide | — | — | 0.2 floor → adhesive ring, not heat staking (DEV-C3) |

The opening test also reports 0.24 at the window corner reliefs: a polygonisation cusp where the relief circle meets
the window edge at 90°, not a web.

### 6.3 Millability of L3

| Feature | Tool | Depth | L/D | Process |
|---|---|---|---|---|
| Ø1.5 bores | drill + reamer | 5.5 | 3.7 | from the top |
| Ø1.2 bores, merged slots, notches | drill Ø1.2; end mill Ø1.0 | 5.5 (2 × 2.75) | 2.75 | two-sided (CHOICE-C18) |
| window corner reliefs | end mill Ø1.0 | 2 × 2.75 | 2.75 | two-sided |
| MC Ø1.596 | flat end mill Ø1.5 + interpolation (or reamer) | 4.4 | 2.9 | from below |
| RCj/RS corners R1.0 | end mill Ø2 (rough Ø6) | 5.0 | 2.5 | from below |
| IC Ø8 | end mill Ø6 helical | 5.0 | 0.8 | from below |
| thermal slot | end mill Ø2 | 2 × 2.75 | 1.4 | two-sided |
| recesses / counterbores | Ø3 end mill | ≤ 1.1 | 0.4 | from the top |

### 6.4 Valve tips (all 21, `checks.json` "tips")

All 21: tip centre on the intended channel centreline (≤ 0.0003, the G1/G2 arc-length rounding); tip disc
inside the L3 bore with ≥ 0.15 radial clearance; disc + 0.14 worst-case error entirely on TPE; no other cut under
the tip. Lateral overlap beyond the channel walls: 0.30 (Ø1.0 on 0.4 lines), 0.25 (Ø1.0 on 0.5), 0.20 (V11/V12),
**0.15 for G1–G4 (Ø0.8 on 0.5 lanes) vs 0.14 worst-case error — 0.01 margin**. Tip edge to the nearest TPE cut:
0.25 at G3, G4, V14, V15 (die cut), 0.70 at V8 (RCj), ≥ 0.95 elsewhere.

### 6.5 Lid gas rings (ID 5 / OD 7)
P_c: land clear by 6.2, inner land 0.3 to the disc recess. **P_mv: with the interface lead-in 0.3 at V8 the ring
overlaps the V8 lead-in by 0.16**; with no lead-in at V8 (CHOICE-C10) the land is clear by 0.14 (§9 request).

### 6.6 Registration and the stack at J and the cell
Dowels: round at (59, 42), slot at (59, 5) (19.2 from J, 17.1 from the RC). Budget §5: L1-to-L3 RSS 0.021, WC 0.051
vs required 0.05 — achievable only if laser position and post-bond shrink stay ≤ 0.01 each (UNVERIFIED; measured on
the first cards, inspection (a)).

### 6.7 Mass (Derived from the solids)
COC 18 505 mm³ → 18.88 g (1.02 g/cm³, TOPAS TDS); TPE 1317 mm³ → 1.32 g (1.0 UNVERIFIED); glass 0.09 g (2.23
UNVERIFIED); PTFE 0.03 g; adhesives < 0.01 g → **20.3 g dry**; + 0.86 g of conjugate and HQDP fills (docs/13 §5.2).

## 7. Choices (card level; user may overrule)

| # | Open point | Chosen | Why |
|---|---|---|---|
| CHOICE-C1 | meaning of "window = die + 0.05" | datum faces flush with the nominal die (x 55.0, y 33.35), free faces +0.10, Ø1.0 corner reliefs; TPE cut die + 0.10 all round | puts the die at its interface position when pushed on the datums; same ±0.05 |
| CHOICE-C2 | MC stop | Ø3.4 counterbore from the top to z 5.115, Ø3.0 PTFE disc on a 25 µm ring → stop face z 5.140 | keeps `MC.z` foil-to-stop 5.0; disc insertable from the top |
| CHOICE-C3 | inside corner radii | tanks R1.0, thermal-slot ends R1.0 | Ø2 tool at L/D 2.5; −0.9 % tank volume |
| CHOICE-C4 | lamination registration | Ø2.0 dowels, round (59, 42) + slot along y (59, 5), blind 3.0 in L3 | free areas, close to J/cell, slot along the pin line |
| CHOICE-C5 | WE2 shim | cut 0.01 smaller per side, bonded in the L0/L1 press | docs/13 shim, drop-in fit |
| CHOICE-C6 | L4 fixing | 25 µm acrylic transfer-adhesive ring (see DEV-C3) | 0.2 floor under the recess |
| CHOICE-C7 | wrong insertion | 4 × 45° chamfer at (75.5, 50) on all layers + engraved triangle | one corner breaks all 3 wrong orientations; away from datums and pushers |
| CHOICE-C8 | P_c | PTFE disc like the vents | keeps conjugate out of the dock gas line |
| CHOICE-C9 | ID code | label in a 6.6 × 6.6 × 0.10 recess | label below the clamp plane; laser marking of clear COC has low contrast [assessment] |
| CHOICE-C10 | V8 lead-in | none (edge break) | P_mv gas-ring land (§6.5) |
| CHOICE-C11 | V12–G3 | merged into the V11/V12 slot | web 0.451 < 0.5 |
| CHOICE-C12 | electrode layout and routing | §2.7: single metal layer, CE/RE traces via +x and −y edges, WE2 opening 1.1 wide | no crossings; WE1/WE2 areas immune to ±0.05 die offset |
| CHOICE-C13 | V8 next to RCj | RCj wall boss r 1.25 around V8 (−0.4 µL) | 0.45 → 0.50 web |
| CHOICE-C14 | slivers at cut junctions | throat to x_c + 4.1, nozzle mouths +0.4 into the bore, meter bridging strips | no knife-edge L1 slivers (were 5–110 µm) |
| CHOICE-C15 | L1 islands | cut on a transfer liner, weeded, transferred | 5 enclosed islands |
| CHOICE-C16 | bonding per interface | L0–L1(+L1s): thermal press; L2–L3 and L2–L1: UV/ozone + RT lamination; die: L1b PSA; seam: UV adhesive; L4: PSA ring | docs/13 §2.1, docs/11 §1.2/§3; all parameters UNVERIFIED |
| CHOICE-C17 | film rim under the TPE | TPE compresses 25 µm over the 0.05 band | consequence of docs/18 CHOICE-14 |
| CHOICE-C18 | deep narrow features | two-sided machining on the dowel holes | L/D ≤ 2.75 |
| CHOICE-C19 | minimum milled web | 0.5 at 5.5 height | [assessment] |

## 8. Deviations from docs/13 Rev B (and docs/18)

| # | What | Change | Effect on docs/13 numbers |
|---|---|---|---|
| DEV-C1 | MC 2.0 × 1.0 × 4.425 blind rectangle has R ≥ 0.5 corners when milled (tool ≤ Ø1.0 at L/D 4.4) → 8.9 µL | **Ø1.596 bore**, same 2.000 mm² area, same depth; L1/L2 cut also Ø1.596 | MC 10.0 µL kept (CAD 9.996 + 0.029 ring gap); conjugate line hold-up +0.03 µL; P_mv unchanged |
| DEV-C2 | CE/RE in the pocket are boxed in by WE1 (G3 finger to the die edge, G4 finger to the die edge); one metal layer cannot route them | G4 finger opening starts at y 23.60 (0.25 inside the edge); CE/RE traces run below it | WE1 5.35 → **5.13 mm²** (docs/13's 0.6 mm² for the fingers is 0.46 by its own dimensions); Q_dl per step 0.22 → 0.21 µC (Derived ∝ area); 0.025 µL of the G4 lane (1.9 % of the cell) is not under WE1, diffusion 0.25 mm ≈ 70 s vs τ 18 s → part of it misses one window (constant, calibrated) [assessment]; test in M5 |
| DEV-C3 | heat-staking a Ø4 PTFE disc onto a 0.2 floor (vent recess over the 0.5 roof) risks bulging | C2: 25 µm adhesive rings; C3: heat staking with a thicker moulded roof | none; adhesive leachables UNVERIFIED (headspace only) |
| DEV-C4 | cell volume: WE2 channel per `WE2_CHANNEL` is 2.9 long (docs/13 table says 3.0 / 0.175 µL with "link") | none (drawn as interface) | cell 1.34 → **1.31 µL** (−2.1 %): blank hydrolysis 0.051 → 0.050 nC, lot free HQ 7.8 → 7.6 nC, ULOQ −2 % (all Derived ∝ volume) |
| DEV-C5 | tank corners R1.0, V8 boss | — | RCj 0.500 → 0.496 mL, RS 0.720 → 0.716 mL; fills (0.26 / 0.6 mL) unaffected |
| DEV-C6 | funnel walls inside the bore occupy L1 volume | — | IC total 278.9 µL; 185 µL fill height 3.68 → 3.71 mm |

## 9. Interface change requests (interface.py not edited)

| Name | Current | Needed | Why |
|---|---|---|---|
| `GAS_SEAL_LID["od"]` or `PLUNGER["card_bore_lead_in"]` at V8 | OD 7.0; lead-in 0.3 everywhere | OD ≤ 6.6, **or** record "no lead-in at V8" | ring overlaps the V8 lead-in by 0.16 (§6.5); card uses no lead-in at V8 |
| `MC` (`size`) | (2.0, 1.0) rectangle | round Ø1.596 (same area) | DEV-C1; no dock impact (P_mv centre unchanged) |
| new: card poka-yoke | — | `CARD_POKA_CHAMFER = 4.0` at corner (75.5, 50) | DOCK LOWER must add a matching corner block in the nest, else the chamfer does nothing |
| new: card tooling holes | — | dowel holes Ø2.0 at (59, 42), slot at (59, 5), open in the foil | DOCK LOWER: no anvil feature needed; keep both points off openings (they are) |
| `CER_NECK["h"]` | 0.15 (named "h") | rename to length; the neck height is the cell height 0.200 | naming only |
| `WE2_CHANNEL` | x 58.1–61.0 (2.9) | confirm 2.9 (docs/13 says 1.0 × 3.0) | DEV-C4 |
| `DIE_WINDOW_CLEAR` | 0.05 "die + 0.05" | state the datum interpretation (CHOICE-C1) | dock press-pad footprint unaffected |

## 10. C3 (injection moulding) notes
* L3 moulded with cored bores, merged slots and notches; draft ≥ 0.5° on cavity walls (docs/18 §13; docs/11 §1.2
  quotes 3–7° for machined inserts — Ø1.2 cores 5.5 long with draft change the bore diameter at the top by ≈ 0.1,
  acceptable as clearance); sharp-cornered MC possible with an EDM-made insert, so DEV-C1 can be reversed.
* Vent roofs moulded thicker locally (0.5 under the recess) → heat staking per docs/13; P_c disc likewise.
* Corner reliefs replaced by sharp moulded corners or a moulded die pocket with crush ribs; datum faces moulded.
* L1 hot-embossed/moulded (0.175 through-cut UNVERIFIED, docs/13 §2.1) — islands no longer an issue if L1 is a
  moulded part bonded to L0 with the channels as grooves, which changes the layer concept (then a separate review).
* Seam adhesive replaced by a moulded TPE lip or overmoulding (docs/18 §13); L1b by a die-attach film from reel.
* Dowel holes become moulded tooling holes; label recess becomes a moulded/laser-marked field.

## 11. Open items / UNVERIFIED
Stock grades and tolerances of all sheets (COC 140/175/150 µm, TPE 0.40, adhesive film, PTFE membrane); bonding
parameters (thermal press, UV/ozone TPE–COC bond strength); laser positional accuracy and post-bond shrink (decide
whether L1-to-L3 ±0.05 holds); die thickness, dicing tolerance vs 0.05 trace margins, passivation thickness; seam
adhesive chemistry vs HQ/BQ; wicking of the seam adhesive; G1–G4 lateral margin 0.01 under worst-case error; TPE
compression over the film rim (leak path at the seam); MC reaming; P_c disc effect on the RCj air push (flow
resistance); mass densities of TPE, glass, PTFE. **Not built in CAD:** the lid/dock-side vent pockets, gas rings
(dock parts). Not done: escape/collection model re-run for DEV-C2 (G4 finger strip) — add to M5.

## 12. Sources opened this session (2026-11-13)
* TOPAS 5013L-10 technical data sheet (German), https://topas.com/wp-content/uploads/2023/05/TDS-5013L-10_d.pdf —
  density 1020 kg/m³ (ISO 1183), Tg 134 °C, tensile modulus 3200 MPa.
* Repository: docs/11 §1–§4, docs/13 Rev B §2–§5, docs/16 §2/§3/§6.4, docs/18, `cad/elisa_cad/interface.py`,
  `common.py`, `cad/README.md`.
