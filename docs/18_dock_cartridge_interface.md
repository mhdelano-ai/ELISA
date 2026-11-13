# 18 — Cartridge A ↔ dock: interface control document — Revision B (after integration)

Status: 2026-11-13, **stage C0 desk work**. **Revision B (after integration)**: the four module designs (docs/19–22)
were integrated in docs/23; every interface change request is resolved in **§15** (request → decision → modules
changed) and the changed values are written into the sections below (marked "Rev B"). Revision A text that no longer
holds is struck through only where the old number matters; otherwise it is replaced. Revision A inputs: docs/00, 09, 11 §3/§5, 13 Revision B (all),
16 §2/§3/§6.4; `scripts/chip_round/design_A_docs13/revision_B/` (`mag_b.py`, `sched.py`). Nothing is ordered.
This document changes no other document. **Machine-readable source of truth: `cad/elisa_cad/interface.py`**; every
table below is generated from or checked against it. Drawings: `cad/out/interface/` (`card_interface_plan`,
`dock_overlay_plan`, `zoom_island`, `zoom_cell_J` as PNG + SVG; `card_envelope.step`, `dock_space_claims.step`).

Source tags as in docs/13: docs section | **Derived** (arithmetic shown) | **CHOICE-n** (§9, open point decided here)
| **DEV-n** (§10, docs/13 geometry not buildable as written) | **UNVERIFIED** | [assessment]. Units mm, N, °C.

## 1. Scope

* Cartridge A only (docs/13 Rev B), drawn for the **C2 prototype** (docs/16 §6.4): laminated card (laser-cut
  L0/L1/L1b/L2 sheets, CNC-milled COC upper body L3, custom glass die), prototype dock from catalogue actuators and
  machined parts. A dedicated dock stands beside the Waters stack (short PEEK line from the SM-FL outlet).
* This phase fixes everything two downstream CAD agents must agree on: coordinates, card features the dock touches,
  the channel network the valves sit on, all dock-side contact/opening geometry, force budgets and space claims.
  Downstream: CARD (L0–L4, die), DOCK UPPER (lid/head), DOCK LOWER (nest, anvil, magnet and electrode bays,
  thermal), DOCK BASE (frame, pumps, bottles, electronics, enclosure, routes). Ownership: `cad/README.md`.
* docs/13's functional numbers are kept unless §10 says otherwise.

## 2. Coordinate systems

| System | Origin | Axes | Source |
|---|---|---|---|
| CARD | lower-left corner of the card seen from the top; **z = 0 = foil (L0) underside = anvil top plane (datum C)** | x along 75.5, y along 50, z up into the card | docs/13 §2.1; z-origin CHOICE-1 |
| DOCK | front-left corner of the dock base at bench level | X to the operator's right, Y away from the operator, Z up | CHOICE-12 |
| Transform | P_dock = P_card + **(190.0, 75.0, 170.0)**, no rotation | card x ∥ X, y ∥ Y | CHOICE-12 |

Card insertion: lid open, card held by its long edges, top face up, reagent zone (x = 0) on the operator's left,
**lowered vertically (−Z)** into the nest; spring pushers then seat it on datums A/B; the lid is closed and the head
descends vertically (§8). Card occupies dock X 190–265.5, Y 75–125, Z 170–176.215.
**Rev B:** the back-right corner (75.5, 50) carries a 4 × 45° poka-yoke chamfer (docs/19 CHOICE-C7,
`CARD_POKA_CHAMFER`); the nest has a matching corner block 0.3 clear of it (`NEST_POKA_BLOCK`, LOWER), so a card in
any of the three wrong orientations cannot seat (checked on the real card, docs/23 §4).

## 3. Card envelope, layer stack, datums

| Item | Value | Source |
|---|---|---|
| Outline | 75.5 × 50.0, corner R 1.0 (L3); L0–L2 outline 0.2 inside L3 | docs/13 §1.1; CHOICE-13 |
| L0 foil | z 0–0.140 COC | docs/13 §2.1 |
| L1 channel sheet | z 0.140–0.315 (all channels through-cut, **one layer → network must be planar**) | docs/13 §2.1 |
| L1b die film | z 0.315–0.340, die outline + 0.15 (seam cover) | docs/13 §2.1; CHOICE-14 |
| L2 TPE | z 0.315–0.715 (0.40 of 0.3–0.5) | CHOICE-15 (thickness UNVERIFIED) |
| L3 body | z 0.715–6.215, milled COC; cavities blind from below, roof 0.5 | docs/13 §2.1; CHOICE-16 |
| Card thickness | **6.215** (Derived 0.14 + 0.175 + 0.40 + 5.5) | docs/13 "≈ 6.2" |
| Die | x 55.0–61.0, y 23.35–33.35, z 0.340–1.040 (thickness 0.70 UNVERIFIED) | docs/13 §2.7 |
| L3 die window (Rev B) | x 55.00–61.10, y 23.25–33.35: datum faces x = 55.0 and y = 33.35 flush with the die, free faces + 0.10, Ø1.0 corner reliefs (`DIE_WINDOW`) | docs/19 CHOICE-C1 |
| Tooling holes (Rev B) | Ø2.0 at (59, 42) and slot 2.0 × 3.0 (along y) at (59, 5), open in L0–L2, blind 3.0 into L3; over the 5-mm anvil plate, 7.8 / 11.2 mm from the nearest opening (`CARD_TOOLING_HOLES`) | docs/19 CHOICE-C4 |
| Thermal zones | reagent x 0–20; break x 20–24 (L3 slot, bridges y 3.5–6.5 and 43.5–46.5); assay x 24–75.5 | docs/13 §2.1; CHOICE-17 |

**Datum scheme (CHOICE-1).** C = foil underside on the lapped anvil top (assay anvil and reagent cold plate coplanar,
flatness 0.02 UNVERIFIED target). A = front edge y = 0 against two Ø4 pins touching at x = 12.0 and 63.0. B = left
edge x = 0 against one Ø4 pin touching at y = 25.0. Pins protrude 5.0 above z = 0 and touch milled L3 only. Spring
pushers 5 N at (37.75, 50) → −y and (75.5, 25) → −x [assessment]. Tolerances: feature-to-edge ±0.05 (milled), **L1-to-L3
registration ±0.05 required** at the J and cell clusters (stub rule; achievability UNVERIFIED), die in window ±0.05
(docs/13 §2.7), head-to-nest ±0.03 [assessment].

## 4. Card features the dock touches (card coords)

Full list with comments in `interface.py`; channel polylines in `CHANNELS` (the CARD agent cuts exactly these).

| Feature | Geometry | Source |
|---|---|---|
| IC1, IC2 | Ø8.0 at (40, 38), (40, 12); blind, roof 0.5, total 280 µL (185 µL working unchanged) | docs/13 §2.3 |
| RCj / RS / MC | 10×10 at (8, 38) / 12×12 at (68, 10) / MC **Rev B: round Ø1.596** (same 2.000 mm² as 2.0 × 1.0) at (16, 30), 10.0 µL foil-to-stop | docs/13 §2.3; DEV-C1 |
| BW | 2.5×2.5 at **(57.85, 17.2)** | DEV-5 |
| RC, WE2 channel | 2.6×2.0 at (56.8, 25.0), h 0.200; WE2 channel x 58.1–61.0 (**2.9 long, Rev B confirmed**; docs/13 "3.0" nominal), w 1.0, h 0.05 → cell 1.31 µL in the card CAD (docs/13 1.34) | docs/13 §2.3; DEV-C4 |
| CE/RE pocket, neck | pocket x 55.3–55.7, y 23.45–23.85; neck x 55.5–55.9, y 23.85–24.0 (length 0.15, key `len`; height = cell 0.200) | docs/13 §2.3; DEV-2 |
| Lane fingers | G3: x 55.0–55.5 at y 25; G4: x 57.85, y 23.35–24.0 | docs/13 §2.3; DEV-2 |
| WL1, WL2 | from (44, ±) heading +x: arc R 3 cw to −77.05°, straight 9.28, arc R 3 to −40°, end J (50, 25); **15.255 mm** each (mirror for WL2) | docs/13 §2.3; DEV-3 |
| WLc | J → die edge (55.0, 25); drag path apex → RC centre **23.41 mm** (fillet at J) | docs/13 §2.3; DEV-3 |
| Contact window, pads | x 55.3–60.7, y 29.8–33.2 through L1+L0; pads 1.2×1.0 at x 56.2/58.0/59.8, y 30.6/32.4 (WE1 WE2 CE / RE LOOP_A LOOP_B) | docs/13 §2.7; CHOICE-9 |
| Vents (L4) | Ø4 discs recessed in Ø4.4×0.3 at IC1 (40, 38), IC2 (40, 12), RS (70, 13) | docs/13 §2.1; CHOICE-16 |
| ID code | 6×6 data matrix on the top face at x 44–50, y 0.8–6.8 | docs/13 §6.7; CHOICE-11 |

## 5. Plunger interface (21 valves and gates)

**Principle (CHOICE-2).** Each valve is a steel pin guided in the lid head's 10-mm aluminium heater block, entering a
coaxial L3 bore. **A compression spring per pin sets the closing force** (fail-closed, independent of the actuator);
a single-acting pneumatic cylinder (**Rev B: Ø6 bore, 400 kPa pilot** via SMC S070B-5DG 3/2 valves, 0.5 W coil rated
0.5 MPa — docs/20 DEV-U1/U2; Rev A: Ø5 / 300 kPa) **lifts the pin through a horizontal yoke blade** to open. V3 is inverted: a spring
holds it open, the cylinder closes it through a 2.5 N force-limiting spring (fail-open, docs/13 §4). Stroke 0.8
(≥ 0.5 required, docs/13 §6.2); tip z closed ≈ 0.17, open ≈ 0.97 (Rev B: = closed + stroke; Rev A wrote 1.015). Pin Ø1.2 / flat tip Ø1.0 in Ø1.5
bores (docs/13 §2.6), except the J and cell clusters: pin and tip Ø0.8 in Ø1.2 bores. Bore lead-in 0.3×45°, **except V8 (none, edge break; Rev B,
docs/19 CHOICE-C10)** so the P_mv gas ring OD 7.0 keeps 0.14 mm of flat land.

**Why a fan-out.** The minimum pin pitch the stub rule produces is **1.60 mm** (V11–V12; G1–G2 1.87, V12–G3 1.65).
No catalogue actuator found this session fits that: the memetis part listed is a 5 × 8 mm SMA *microvalve* without a
plunger force/stroke spec (german-pavilion MD&M page); the Lee LHD 3/2 solenoid valve is "7 mm" with 45 psig
operating and 15 psid maximum differential in its standard version (theleeco.com). Cylinders therefore sit on a
**9.0 mm grid** above the head and reach their pins through yoke blades (1.0 × 4.0, plan clearance ≥ 0.3) at two
tiers. Assignment (minimum Σ offset², `scipy` `linear_sum_assignment`) and tier order (blade over another pin's hook →
higher; blade under another cylinder's rod → lower; crossing blades → different tiers) form an acyclic graph:
**2 tiers suffice**; offsets 0.7–10.9 mm, rms 6.8 mm. Head stack (card z): heater block 6.215–16.215, pin collars
16.415–16.915 (Rev B), pin springs to 24.5, spring plate 24.5–26.0 (Rev B), tiers 27–31 and 32–36, cylinder block 38–68.
**Rev B materials** (within ≈ 40 mm of a magnet, `MATERIALS`): pins Nitronic 60 (fallback 1.4404 annealed; μr ≤ 1.02
incoming check), pin springs Co-Cr-Ni (Elgiloy class), yokes/spring plate/buttons 1.4404, guides CuSn8. **Hook gap**
(0.20) is set with a gauge on a reference card at the real closed height (docs/23 I-13).

| ID | Tip centre (x, y) | Tip/pin Ø | Class, F_nom / F_max (N) | Fail | Cylinder (x, y), tier | Function |
|---|---|---|---|---|---|---|
| V1 | 31.00, 29.95 | 1.0/1.2 | anvil 2.5/3 | closed | 32.0, 32.5, 0 | M_in → C1 |
| V2 | 31.00, 20.05 | 1.0/1.2 | anvil 2.5/3 | closed | 32.0, 14.5, 0 | M_in → C2 |
| V3 | 33.00, 21.10 | 1.0/1.2 | anvil 2.5/3 | **open** | 32.0, 23.5, 0 | M_in → bypass (in-line) |
| V4 | 37.50, 29.95 | 1.0/1.2 | anvil 2.5/3 | closed | 41.0, 32.5, 0 | beads → C1 |
| V5 | 37.50, 20.05 | 1.0/1.2 | anvil 2.5/3 | closed | 41.0, 14.5, 0 | beads → C2 |
| V6 | 25.90, 31.00 | 1.0/1.2 | anvil 2.5/3 | closed | 23.0, 41.5, 0 | MC → C1 (in-line at rail head) |
| V7 | 25.90, 19.00 | 1.0/1.2 | anvil 2.5/3 | closed | 23.0, 14.5, 0 | MC → C2 |
| V8 | 12.00, 31.80 | 1.0/1.2 | cold 2.5/3 | closed | 5.0, 32.5, 0 | RCj → MC |
| V9 | 32.50, 41.00 | 1.0/1.2 | anvil 2.5/3 | closed | 32.0, 41.5, 0 | IC1 nozzle ↔ P_d1 |
| V10 | 32.50, 9.00 | 1.0/1.2 | anvil 2.5/3 | closed | 32.0, 5.5, 0 | IC2 nozzle ↔ P_d2 |
| V11 | 51.30, 25.95 | 0.8/0.8 | slot 1.2/1.5 | closed | 50.0, 23.5, 1 | S_A (P_a2) → WLc tee |
| V12 | 52.90, 25.95 | 0.8/0.8 | slot 1.2/1.5 | closed | 50.0, 32.5, 0 | WLc tee → P_wo |
| V14 | 61.75, 25.00 | 0.8/0.8 | anvil 2.5/3 | closed | 68.0, 32.5, 0 | WE2 → P_s |
| V15 | 55.50, 22.60 | 0.8/0.8 | anvil 2.5/3 | closed | 59.0, 14.5, 0 | RS → CE/RE pocket |
| V16 | 60.55, 17.20 | 1.0/1.2 | anvil 2.5/3 | closed | 68.0, 14.5, 0 | BW → P_s |
| V17 | 28.00, 29.95 | 1.0/1.2 | anvil 2.5/3 | closed | 23.0, 32.5, 1 | S_A (P_a) → C1 |
| V18 | 28.00, 20.05 | 1.0/1.2 | anvil 2.5/3 | closed | 23.0, 23.5, 0 | S_A (P_a) → C2 |
| G1 | 49.26, 25.93 | 0.8/0.8 | slot 1.2/1.5 | closed | 41.0, 23.5, 0 | WL1 ↔ J |
| G2 | 49.26, 24.07 | 0.8/0.8 | slot 1.2/1.5 | closed | 50.0, 14.5, 0 | WL2 ↔ J |
| G3 | 54.25, 25.00 | 0.8/0.8 | slot 1.2/1.5 | closed | 59.0, 23.5, 1 | WLc ↔ cell |
| G4 | 57.85, 22.60 | 0.8/0.8 | slot 1.2/1.5 | closed | 68.0, 23.5, 0 | cell ↔ BW |

Force limits and fail states: docs/13 §4. Nominal preloads 1.2 / 2.5 N are CHOICE-3 placeholders until M4.
Card bores: G1/G2 and V11/V12 merged into 1.2 × ~3 slots; G3, G4, V14, V15 open into notches of the die window
(DEV-2). Position feedback per yoke: sensor type to be selected (UNVERIFIED); minimum a pilot-line pressure switch.

## 6. Ports, face seals, clamp force budget

| Port | (x, y) | Kind | Connects | Dock side |
|---|---|---|---|---|
| P_in | 34.2, 27.3 | liquid | SM-FL → M_in | 1/16″ PEEK ≥ 0.3 m |
| P_byp | 34.2, 23.3 | liquid | V3 → waste | waste, air gap |
| P_b | 37.5, 25.0 | liquid | bead rung → V4/V5 | S_b outlet 0.25 ID |
| P_a | 28.0, 25.0 | liquid | A1 rung → V17/V18 | S_A port 1 |
| **P_a2** | 51.3, 36.5 | liquid | → V11 | S_A port 2 (DEV-6) |
| P_d1 / P_d2 | 29.5, 41.0 / 29.5, 9.0 | liquid | V9/V10 ↔ nozzles | FEP coil → S_IC1/2 |
| P_wo | 66.0, 35.5 | liquid | V12 → waste | waste |
| P_s | 63.0, 20.5 | liquid | V14, V16 → S_RC | S_RC (pull only) |
| P_rf | 72.5, 5.5 | liquid | RS floor | HQDP bottle, pressure fill |
| P_cf | 5.0, 35.0 | liquid | RCj floor | conjugate bottle (cooled) |
| P_c / P_mv | 8.0, 41.5 / 16.0, 30.0 | gas (top) | RCj headspace / MC stop vent | pressure channels 1/2 |

**Liquid face seal (CHOICE-4):** port hole Ø1.0 through L0+L1 (0.24 µL, docs/13 §2.5); in the anvil a 1/16″ PEEK tube
bonded into a replaceable PEEK port insert, tube end flush with z = 0 under the hole; flat elastomer annulus ID 1.7 /
OD 3.3 / 0.50 thick in a 0.38-deep counterbore (24 % compression) [assessment; material FFKM or EPDM, HQ/Tween
compatibility UNVERIFIED]. No anvil bore volume is added. Port pitch ≥ 3.6; valve tips ≥ 0.3 outside a seat
(**Rev B: `VALVE_TIP_SEAT_MARGIN` 0.3 governs gasket seats; `VALVE_TIP_EDGE_MARGIN` 0.5 governs through-openings**).
Gasket 50 ShA (docs/21 CHOICE-L5): 6.7 N per seal (Gent form, moduli UNVERIFIED) → 74 N for 11 seals.
**Gas seals (lid):** ring ID 5.0 / OD 7.0 / 1.0 around P_c and P_mv, ≈ 5 N each [assessment].

**Clamp budget (Derived, `interface.clamp_budget()`):**

| Load | per item | total |
|---|---|---|
| liquid seals pushing the card up | 3–10 N (0.5–1.5 MPa × 6.3 mm², UNVERIFIED) | 11 × → 33–110 N |
| card clamp, lid → card top (×1.5 margin on seals) | — | **≥ 50–165 N** |
| plunger springs (react on the head; push the card down) | 20 × ≤ 3 N or 1.5 N, + V3 3 N | 51 + 3 N |
| pogo pins (up on the die) — reacted by the press pad | 6 × 1.5 N | 9 N (pad 12 N) |
| lid gas seals | 2 × 5 N | 10 N |
| **latch / hinge total** | | **126–241 N → Rev A rated ≥ 250 N (CHOICE-8)** |
| **Rev B as built (docs/20 §4.6)** | head force 280 N (265–295); card-face clamp 213 N (≥ 198) | **design value 300 N** (`CLAMP_DESIGN_FORCE`); latches 2 × 95 N on LOWER catch brackets, hinge 111 N on LOWER pedestals |

Clamp application (CHOICE-8): distributed through the flat L3 top — Al heater block over the assay zone, PEEK
plate over the reagent zone — minus pockets for vents (Ø6, vented sideways), gas seals, pins, die window/press pad.

## 7. Magnet, electrical, thermal and optical interfaces

**Anvil openings (dock side, card coords).** Windows W1/W2 **11.4 × 11.4 square, R 1.0**, centred on the chambers
(DEV-4). Drag slot = union of buffers: 4.0 wide around apex → WL1/WL2 → J; 3.4 wide around J → RC centre and the
bead-out leg (56.8, 25) → (57.85, 25) → (57.85, 21.5) (DEV-5), **Rev B: ∪ the axis-aligned 2.6-sq M_d holder swept
along every drag/bead-out path + 0.30 (`slot_polygon()`, docs/21 DEV-L4); max local width 4.44 at G1/G2 → foil
deflection 19 µm under a 1.5 N slot valve (docs/13 15 µm; M4 acceptance ≤ 20 µm)**. M_w recess 3.4 × 3.4 × 3.2 at (57.85, 17.2). Contact
opening = contact window. Anvil: 5-mm Al top plate over the magnet bay (Rev B: bottom pocket x 32.5–62.5, y 0–50);
15-mm thick zones for port inserts (Rev B, docs/21 DEV-L3): island boss x 24–40.5 / y 19–31, west strip x 24–32.5,
east block x 62.5–75.5, P_a2 boss x 49–53.5 / y 34.5–39, P_s boss x 60.3–62.5 / y 17.8–23.2 (CHOICE-5). Tip-edge margin to any opening ≥ 0.5 (V15: 0.25, accepted, CHOICE-5).

| Magnet | Size (mm), axis | Position / motion | Gap / travel | Source |
|---|---|---|---|---|
| M_c,1 / M_c,2 | 10×10×5 NdFeB, through 5; holder 10.6 sq with a flange seating on the plate underside | under W1/W2 centre; **Rev B: parallelogram swing R 64.5 outward (one self-locking worm per unit), parked centre (40, 56.7) / (40, −6.7), top z −45.6; fail state HOLD** (Rev A: Z 25 + retract 18, spring-up) | up: top z −0.16 (gap by geometry) | docs/13 §3.3.1; DEV-4; docs/21 DEV-L1/L2 |
| M_d | 2×2×4, along 4; holder 2.6 sq | on a vertical post **from below** (X–Y stage, spring-up Z pulled down by a back-drivable cam, 8 mm); tip travel x 35.0–59.6, y 6.0–44.0; drag 0.20, gather 0.30 mm/s; **holds at the RC during accumulation and READ**; parks lowered under J | up: top z −0.16 ± 0.05 | docs/13 §3.3, §6.2; DEV-4 |
| M_w | 3×3×3 | fixed in the recess under BW | top z −0.16 | docs/13 §3.3.1; DEV-5 |
| M_h | — | **not built** (function by M_d) | — | DEV-4 |

Transit rule: lowered M_d moves only via J (x ≥ 44), never under the electrode bay; ≥ 8 mm below and ≥ 6 mm
laterally from an incubating chamber (docs/13 §2.2). Stage candidate class: Zaber X-LSM050A (zaber.com spec page:
travel 50.8 mm, repeatability < 3 µm, 26 mm/s max, non-back-driving, 0.34 kg; footprint not listed → UNVERIFIED).

**Electrical (CHOICE-9).** Six pogo pins on the pad centres (pitch 1.8, barrel ≤ 1.6 UNVERIFIED), working travel
≈ 1.0, ≤ 1.5 N each (Rev A class value PTR 1064; **Rev B: PTR series 1007.70 class, 1.27 pitch, 0.50 N preload,
1.40 N at 1.27 → 1.21 N at 1.0, 7.25 N for six**, part number UNVERIFIED). Pogo block on a 3 mm Z lift: tips at
**z −1.66 (Rev B; Rev A −1.0 was inconsistent with a 1.34 free tip)** while loading, raised to the pad plane
z 0.340 after the head is down (no sliding on the pads).
Die-back press pad (lid): x 55.5–60.5, y 29.6–33.1 on the die back (z 1.04), 1 mm silicone on a grounded stem,
12 N, 1 mm compliance for the die thickness (Rev B: kept; 12 N > 7.25 N pogo, net 4.75 N on the die). Electrode bay
(grounded enclosure): card x 54.0–62.5, y 28.8–36.5, z −70–0; relay inside (**Rev B: |B| ≤ 1.9 mT there with M_c1
parked → magnetically screened reed relay + 0.3 mm mu-metal can, accepted at 5 mT applied, `WE_RELAY_FIELD`**); shielded leads ≤ 0.3 m via a bulkhead on the +X wall to the Gamry cell cable (docs/13 §6.3).

**Thermal (CHOICE-7).** Bottom: cold plate (Al 5 mm, Peltier, 4–8 °C) x 0–20; PEEK insulator in the 4-mm anvil gap
x 20–24; heated Al anvil 25.0 °C x 24–75.5 minus openings. Top: PEEK pressure plate x 0–20 (no heater); Al heater
block 10 mm (25.0 °C, also the pin guide) x 24–75.5. Contact = the card top minus pockets.

**Optical/ID (CHOICE-11).** Top-face data matrix (§4) read by a down-looking reader on the nest front frame with the
lid open; lid-closed switch and contact-loop resistance as docs/13 §6.7.

## 8. Dock space claims (dock coords, mm) and pass-throughs

| Claim | Box (X, Y, Z) | Owner / content |
|---|---|---|
| UPPER_lid_closed | 150–320, 30–200, 176.2–300 | DOCK UPPER: head, cylinders, pilot manifold, cover, hinge, latch |
| LOWER_nest_anvil | 150–320, 20–185, 155–176 | DOCK LOWER: anvil, cold plate, datum pins, pushers, head guide bushes |
| LOWER_bay | 150–320, 20–200, 40–155 | DOCK LOWER: M_c units, M_d stage + post, electrode bay, Peltier stack, tube corridors |
| BASE_drip_tray | 0–470, 0–420, 0–15 | DOCK BASE |
| BASE_cold_compartment | 10–145, 20–200, 15–220 | conjugate bottle, bead vial rocker, S_b; SM-FL line entry |
| BASE_under_bay | 150–320, 20–200, 15–40 | leak electrodes, low items |
| BASE_bottles | 325–465, 10–200, 15–260 | A1, HQDP, waste |
| BASE_rear_low | 150–320, 205–315, 15–180 | under the opened lid: pressure controller, flow sensors, regulator |
| BASE_right_rear | 325–465, 205–315, 15–260 | spare |
| BASE_pumps | 150–465, 320–415, 15–280 | S_A, S_IC1, S_IC2, S_RC (Cavro/PSD envelopes UNVERIFIED) |
| BASE_electronics | 5–145, 205–415, 15–320 | controller + watchdog, drivers, PSUs, DAQ |
| BENCH_gamry | 480–570, 90–360, 0–190 | Reference 600+, 9 × 19 × 27 cm W × H × D, 3 kg (gamry.com legacy page) |

**Rev B claims added** (IR-3, ICR-U3): `BASE_front_strip` 0–470 × 0–20 × 15–330 (cold-box door, Peltier exhaust
extension; E-stop/light bar may protrude to Y −25/−6); `BASE_lane_gap` 145–325 × 200–205 × 15–178; `LOWER_hinge_pedestal_L/R`
150–154 / 316–320 × 185–200 × 44–160; `UPPER_hinge_block_L/R` 150–153.8 / 316.2–320 × 185–200 × 160–199.

LOWER sub-claims (card coords, owned by DOCK LOWER; Rev B per docs/21 DEV-L6): electrode bay as §7; reagent Peltier
stack incl. heat sink, fan and exhaust duct x −12–20, y −55–55, z −85–0; tube corridors W/E as built (vertical drops at
the ports, R 25 bends, runs at z −55…−62 to the walls); M_c units x 28–52, y −55–106, z −77–0; M_d stage x −28–123,
y −50–100, z −126…−62 (post rises from z −62).

Pass-throughs (**Rev B**, ICR-6 / IR-2/4/6): every card liquid line leaves the LOWER claim at its own point
(`LIQUID_LINE_EXITS`, from the LOWER routes; BASE grommets in the well partitions):

| Line | Exit (dock X, Y, Z) | Line | Exit (dock X, Y, Z) |
|---|---|---|---|
| P_in | 150, 102.3, 114 | P_rf | 320, 80.5, 112 |
| P_byp | 150, 98.3, 112 | P_s | 320, 95.5, 112 |
| P_b | 150, 100.0, 108 | P_wo | 320, 110.5, 115 |
| P_a | 150, 100.0, 110 | P_a2 | 320, 161.5, 112 |
| P_d1 / P_d2 | 150, 116 / 84, 112 | P_cf | 150, 110.0, 112 |

Cable window (motors, heaters, sensors, Peltier, pogo-cylinder air) X 150, Y 150–195, Z 60–140; LOWER Peltier exhaust
(10.6 W) leaves at Y 20, X 186–210, Z 118–144 into a BASE duct to a louvre in the front-bay panel; lid umbilical at dock
(235, 200, 190), BASE hand-over grommet X 236–262, Y 205–211, Z 180 (P_c X 240, P_mv 248, air 258) — UPPER owns the
loop; Gamry cable bulkhead on the LOWER +X wall at (320, 107, 135), flange ≤ 16 × 20 (Y × Z), connector UNVERIFIED;
SM-FL PEEK line through the left wall at (0, 110, 160) (Waters stack on the left). LOWER bay base plate (dock Z 40–44)
bolts to the BASE deck with 6 × M6 at X 165/305 × Y 35/110/185, dowels Ø6 at (165, 50) round and (305, 50) slot
(`LOWER_MOUNT`). Lid latches: catch plates on two LOWER brackets on the anvil front face, keep-outs X 173–199 and
271–297, Y 34–55, Z 161–176 (`LID_LATCH`); lid hinge blocks on two LOWER pedestals (top Z 160, `HINGE_SUPPORT`).
Head guide pins (`HEAD_GUIDE_PINS`, Rev B): Ø6 at card (−8, 46) and (84, 4), CuSn8 bushes Ø10 H7 in nest + anvil, bush
top z 5.0 = nest frame top (`NEST_FRAME_TOP_Z`); pin tip z 5.5 raised, −2.5 down.

**Lid (CHOICE-10).** Hinge axis ∥ X through dock (Y 195, Z 190); opening **85°** to a stop (beyond 90° the lid's top
face sweeps down behind the hinge into the rear claims). Swept bounding box X 150–320, Y 29.4–305, Z 175.3–388.3
(Derived, `lid_sweep_bbox()`); the enclosure is open above the card bay. After closing, a cam latch lowers the head
8 mm vertically on two guide pins located in the nest, so the pins enter the card bores vertically (they protrude
≈ 5.7 below the head face). Rev B: lowest lid material over the nest during the sweep Z 177.97 (docs/20 §4.8) vs nest
frame top Z 175.0 → 2.97 mm. Operator loading path: clear box X 175–285, Y 55–145, Z 176.2–330.

## 9. Table of choices (open in docs/13; user may overrule)

| # | Open point | Chosen | Why | Alternatives / how to overrule |
|---|---|---|---|---|
| CHOICE-1 | datum scheme | anvil plane C + edge pins A (2) and B (1) + spring pushers | valves need support everywhere outside openings (docs/13 §2.1); no card holes in crowded areas | 3 raised pads (as §6.4 wording) or tooling holes in L3 |
| CHOICE-2 | plunger drive, fan-out | spring-closed pins, pneumatic cylinders on a 9-mm grid, yokes on 2 tiers; **Rev B Ø6 / 400 kPa** (Rev A Ø5 / 300) | closing force set by a spring (≤ 1.5/3 N exact), fail-closed by construction, no coils near the die, pin pitch 1.6 unreachable by any actuator body | direct miniature solenoids (≥ ~12 mm pitch, longer yokes); SMA (no plunger spec found); motor + cam |
| CHOICE-3 | closing forces | 1.2 N slot / 2.5 N other (max 1.5 / 3) | below docs/13 limits with margin | set by M4 |
| CHOICE-4 | face seals | bonded 1/16″ tube in PEEK insert + flat elastomer annulus; lid gas rings | no added dead volume, 3.6-mm port pitch | 6-32 flat-bottom fittings (≥ 6 mm pitch, +0.4 µL bore) |
| CHOICE-5 | anvil build | 5-mm Al top plate over the magnet bay, 15-mm thick port zones (Rev B zones per DEV-L3); tip margin 0.5 to openings (V15 0.25), **0.3 to gasket seats (Rev B)** | magnets must reach the foil; port inserts need depth | ceramic/Ti plate; other margins |
| CHOICE-6 | M_d stage, park | X–Y stage far below, vertical post, spring-up cam Z; park under J lowered | post fits the 3.4/4.0 slot; stage free of the electrode bay | side-entry arm (conflicts with ports/electrode bay, tested and rejected) |
| CHOICE-7 | thermal parts | Al heater block 10 mm (= pin guide), PEEK top plate, Al cold plate 5 mm, PEEK in break gap | simple, two zones as docs/13 §6.5 | heated pressure pads instead of a block |
| CHOICE-8 | clamp | distributed via heater block/PEEK plate, latch ≥ 250 N (**Rev B design value 300 N**, head force 280 N) | uniform foil contact on the anvil | point pads (needs stiffer L3 analysis) |
| CHOICE-9 | contacts | pads 2×3 at 1.8 pitch; pogo block with 3-mm lift (Rev B tips −1.66 retracted, 7.25 N); 12 N press pad | no pad scrubbing at loading; pad layout fits the contact window with 0.3 margin | fixed pogos (card rests on tips while loading) |
| CHOICE-10 | lid motion | rear hinge, 85° stop, vertical 8-mm head descent by cam latch | pins must enter bores vertically; rear claims clear | vertical-lift lid (taller dock) |
| CHOICE-11 | loading, ID | vertical top-down loading; top-face code read with lid open | no drawer mechanism | edge code + side reader |
| CHOICE-12 | dock layout, coords | card bay front-centre, cold compartment left, bottles right, pumps and electronics rear, Gamry on the bench right | short lines to SM-FL (left) and Gamry (right); lid sweep clear | user may mirror the layout |
| CHOICE-13 | card outline | R 1.0 corners; laminate 0.2 inside L3 | only milled edges touch datums | — |
| CHOICE-14 | die seam | window = die + 0.05; TPE cut = die + 0.10; L1b film = die + 0.15 as seam cover, seam filled with adhesive; die datum edges x = 55.0 (y 27–33.35) and y = 33.35 | lanes leaving the die need a ceiling in the seam (not addressed in docs/13) | TPE butt joint (leak risk) |
| CHOICE-15 | TPE thickness | 0.40 | middle of 0.3–0.5 | M4 |
| CHOICE-16 | cavities, vents | blind cavities (roof 0.5), vents recessed, lid vent pockets Ø6; MC L3 depth 4.425 (10.0 µL foil-to-stop) | flat card top for the clamp | through-bores with stuck-on lids |
| CHOICE-17 | break bridges | y 3.5–6.5 and 43.5–46.5 | away from the conjugate lines | — |

## 10. Deviations from docs/13 Revision B

| # | What cannot be built as written | Change | Effect on docs/13 numbers |
|---|---|---|---|
| DEV-1 | Island I with 4 supply lines to two inlet channels cannot be routed **without crossings** in one cut layer, with ports where tubes can leave | planar ladder: rails C1/C2 (y 31 / 19) with V6/V7 in-line at the rail heads, V17/V18 and V4/V5 on rungs at x 28 and 37.5, M_in as a hairpin bridged to the rails by V1/V2 and ending in-line at V3 | C_k 0.26 → **1.42 µL** (16.2 mm); a 3 µL chase is 2.1 volumes instead of 11 — the cleaning still sweeps C_k with 900 µL, but M3's "≤ 10⁻³ of a dose left after a 3 µL chase" is at risk → consider 5 µL chases (+4 µL in the chamber: /1.85 → /1.87); bead path 3.3 → **3.54 µL** (< 4 µL chase, kept); M_in 1.05 → 1.37 µL (flushed by D13); conjugate lines 0.6 → 0.73 / 1.43 µL (air-cleared) |
| DEV-2 | G3, G4, V14, V15 seals 0.3–0.5 mm from the die edge leave no room for an L3 wall between Ø1.5 bores and the die window | Ø0.8 pins/tips; bores open into notches of the die window; stubs **0.35** from the die edge (G3, G4, V14), V15 **0.45** from the pocket (0.10 inside the die); G4 lane moved to x 57.85, pocket to x 55.3–55.7 | stub volumes G3/G4 0.044 → 0.031 µL, V14 0.026 → 0.018 µL, V15 0.016 → 0.024 µL; escape total ≈ unchanged (0.2–0.5 %, not re-run); cell 1.34 µL unchanged |
| DEV-3 | WL1/WL2 meeting at J with G1/G2 0.3 mm from J and pins ≥ 1.4 mm apart is not achievable with straight lanes | lanes arrive at ±40° on R 3 arcs; G1/G2 1.2 mm (arc length) before J; drag trajectory filleted at J (≤ 0.21 mm off the lane centreline) | WL 15.0 → **15.255 mm** (1.34 µL each); drag path 23.3 → **23.41 mm** (117.1 s vs 116.5 s); G_k′ stub ≈ 0.25–0.40 mm (0.3); V11 tee 1.5 → 1.3 mm after J |
| DEV-4 | (a) a 10 × 10 M_c (diagonal 14.1) does not pass a Ø12 window; (b) M_c (Z-only under the window) and the M_d post compete for the same column below the window; (c) a fixed M_h lift under the RC blocks the M_d post that must reach the RC and BW | (a) square 11.4 windows; (b) M_c leaves the window outward and down (Rev A: lowers 25 then retracts ±y 18; **Rev B: parallelogram swing R 64.5, fail state hold**, docs/21 DEV-L1/L2); (c) M_h deleted, M_d holds the pellet at the RC (carriage busy 34.2–57.15 of each run; next use at 65.2 → no conflict) | magnet gaps and forces unchanged; the ≈ 2 s unheld hand-over of §3.3.3 disappears; actuator count −1 |
| DEV-5 | M_w fixed under BW and M_d reaching BW centre occupy the same place | BW at (57.85, 17.2) over M_w; M_d stops at (57.85, 21.5), 3 mm upstream of BW; the flush (40 µL/min) carries the beads into BW; slot 3.4 wide on axis-aligned legs | bead-out path 4.5 → 4.55 mm; hand-over by flow (floor speed ≈ 0.36 mm/s, Derived by scaling docs/13 §3.3.6 0.18 mm/s at 20 µL/min → 3 mm in ≈ 8 s of the 30 s flush) — UNVERIFIED, add to M1 (BW retention) |
| DEV-6 | V11 (S_A → WLc) cannot be fed from P_a inside island I without crossing WL1/WL2 | new liquid port **P_a2** (51.3, 36.5) on S_A's second valve port | 11 liquid + 2 gas ports (docs/13 §2.5 table lists 10 liquid, text says 9); +1 face seal in the clamp budget |
| DEV-7 | chamber bore "through L3" cannot carry a Ø4 vent | blind bore, roof 0.5 with Ø2 vent hole | total 290 → 280 µL; working 185 µL unchanged |

## 11. One-off consistency checks run (scratch `check_if.py`, `act.py`, shapely 2D)

| Check | Result |
|---|---|
| Pin pitch vs rule (0.8–0.8 ≥ 1.4, mixed ≥ 1.6, 1.2–1.2 ≥ 1.8) | 0 failures; minimum **1.60** (V11–V12), then V12–G3 1.65, G1–G2 1.87, V11–G1 2.04 |
| Pin pitch vs actuator envelope | 1.6 mm ≪ 9.0 mm cylinder pitch → fan-out (§5): 21 sites assigned, acyclic, 2 tiers |
| Anvil-class tips vs openings | margins 0.50 (V16) … 21.9; V15 0.25 (accepted) |
| Slot-class tips inside the slot | G1–G4, V11, V12 fully inside (edge margins 0.35–1.60) |
| Each tip on its channel | all 21 centred (0.000) on the intended channel |
| Planarity (all channel pairs) | only intended junctions touch (J, rails/rungs/bridges, conj fork, P_s join, die edge) |
| Stubs | rails/M_in bridges 0.30/0.30; G3, G4, V14 0.35; V15 0.45; G1/G2 0.25 (arc) – 0.40 (straight-line bound); V11/V12 0.30 |
| Drag trajectory | 23.41 mm; deviation from lane centrelines ≤ 0.214 mm (lane half-width 0.25) |
| Port pitch / seats | min 3.71 (P_byp–P_b) ≥ 3.6; every liquid port in a thick zone or the cold plate; P_a2 seat 0.80 from the slot |
| Pads / contact window | all six pads inside with 0.30 margin; wetted edge → contact window 3.8 (docs/13 ≥ 3.8) |
| M_d holder vs electrode bay | ≥ 1.96 (diagonal of the 2.6 holder) |
| Space claims | no pairwise overlap; lid sweep (0–85°) clears every claim except its own (nest claim cut to Y ≤ 185) |
| CAD helpers | STEP export/reimport of an assembly (2 solids), SVG, PNG all produced headless |

## 12. Warnings for the downstream agents (Revision A; superseded where §15 decides otherwise)

* **CARD:** cut exactly `CHANNELS` (single layer, planar); L1-to-L3 registration ±0.05 at J and the cell; merged bores
  (G1/G2, V11/V12) and die-window notches (G3, G4, V14, V15); seam cover (CHOICE-14); blind cavities; MC depth 4.425.
* **DOCK UPPER:** Ø0.8 pins at 1.6 pitch need a hardened, reamed guide; V3 yoke must push (force-limited) and lift;
  pilot valves ≥ 400 kPa (the standard Lee LHD is 15 psid differential); head descends vertically 8 mm; keep the
  hinge-side lower edge ≥ 2 mm above the nest during opening; vent pockets and gas rings at §4/§6 positions.
* **DOCK LOWER:** no M_h; M_c units lower **and** retract outward; slot widths 4.0 / 3.4; M_w recess web to the slot
  end ≥ 0.6; electrode bay must not extend below y 28.8 (M_d post); pogo lift; port inserts only in thick zones.
* **DOCK BASE:** respect the lid sweep (keep Z ≤ 180 in Y 205–315 behind the card bay); pump envelopes unverified;
  Gamry on the right with ≤ 0.3 m leads; 11 liquid lines (S_A has two card outputs).

## 13. Open items / UNVERIFIED

Actuator and sensor parts (pilot valves, cylinder seals, yoke sensors, pogo pins ≤ 1.8 mm pitch, pogo lift,
Peltier modules, stage footprint), seal stress and material, anvil flatness, die thickness, laminate registration,
TPE thickness, gasket compression forces; hand-over BW (DEV-5) and the C_k chase ratio (DEV-1) → M1/M3; escape not
re-run for DEV-2 stubs (expected ≤ docs/13); Tecan Cavro Centris dimensions not found (no Tecan datasheet reached).
**C3 (moulding) notes:** L3 cavities and bores moulded (draft ≥ 0.5° on cavity walls, cored bores; merged bores and
die notches favour moulding), L1 by embossing/moulding (0.175 through-cut UNVERIFIED, docs/13 §2.1); seam adhesive
replaced by a moulded TPE lip or overmoulding; port insert and datums unchanged; card edges become mould-defined.

## 14. Sources opened this session (2026-11-13)

* Lee LHD 3-way solenoid valve: https://www.theleeco.com/product/lhd-series-3-way-control-solenoid-valve/
* memetis SMA microvalve (5 × 8 mm): https://mdmwest.german-pavilion.com/en/sites/products-services/214473
* Gamry Reference 600+ legacy page: https://www.gamry.com/support-2/legacy-devices/reference-600plus-legacy/
* PTR Hartmann series 1064 probes: https://ptr.ptr-hartmann.com/en/testing-technology/test-probes/battery-probes/series-1064/
* Zaber X-LSM series and X-LSM050A specs: https://www.zaber.com/products/linear-stages/X-LSM ,
  https://www.zaber.com/products/linear-stages/X-LSM/specs?part=X-LSM050A
* Not reachable: Mill-Max datasheet (HTTP 403). Not found: Tecan Cavro Centris dimensions.

## 15. Revision B — resolution of interface change requests (integration, docs/23)

Rule applied where two requests conflicted: keep docs/13's functional numbers, then the least change. `I-n` = the
integration choice listed in docs/23 §8 (with how to overrule it). Every value is in `interface.py` Revision B.

| # | Request(s) | Decision (Rev B value) | Why | Modules changed |
|---|---|---|---|---|
| 1 | head guide pins: UPPER ICR-U1 (−5, 44)/(80.5, 6); LOWER ICR-1 (−7, 46)/(83, 4), bush top z 5.0 | `HEAD_GUIDE_PINS` GP1 **(−8, 46)**, GP2 **(84, 4)**, Ø6 h6 in CuSn8 bushes Ø10 H7, bush top z 5.0, pin tip z 5.5 raised / −2.5 down; anvil widened to x −15…91 | UPPER's bush at (−5, 44) cut into the nest opening and gutter; LOWER's left 0.2 mm to the opening and 0 mm to the anvil edge; 1 mm outward gives 1.2/1.7 mm and 2 mm walls; guided travel before the bores unchanged (1.26 / 0.25 mm) because the pin tip follows the real bush top (5.0, was assumed 6.0) | interface, UPPER params, LOWER geom |
| 2 | pilot air: UPPER DEV-U1/U2, ICR-U5 (400 kPa, Ø6, supply ≥ 450) vs BASE 300 kPa | `PLUNGER` pilot **400 kPa**, bore **6**, lid switch 350 kPa, supply ≥ **450 kPa** at the dock inlet; BASE FR1 set to 400, lab air spec 500–700 kPa, BASE low-supply switch 450 kPa; air per lid actuation 0.36 NmL (BASE budget corrected) | Ø5/300 kPa fails on the worst channel (margin 0.82); force margin 1.60 needs both | interface, UPPER params, BASE params/layout/calcs/fluidics/render |
| 3 | clamp: UPPER DEV-U3/ICR-U4 (280 N, 295 max) vs 250; latch keep-outs ICR-U2; ICR-9 | `CLAMP_DESIGN_FORCE` **300 N**; latch catch plates on two LOWER brackets on the anvil front face (`LID_LATCH`, 95 N each); `NEST_FRAME_TOP_Z` 5.0 | re-checked at 300 N: anvil plate 4.6 µm (was 3.8), card-face clamp ≥ 198 N vs 1.5 × 74 N of 50-ShA seals = 110 N, M_c gap set by the flange (insensitive), M_d gap chain RSS 32 µm unchanged, lowest lid part over the nest 2.97 mm above the frame | interface, LOWER geom/parts/assy/checks |
| 4 | hinge: UPPER ICR-U3 (rail) vs BASE IR-5 (≥ 3 mm inside X 150–320) | UPPER hinge blocks (Z 160–199) bolt on two **LOWER hinge pedestals** X 150–154 / 316–320, Y 185–200, Z 44–160; claims added; BASE right partition moved to X 323–325 so the moving cam lever (X ≤ 320) keeps 3.0 mm, left side 3.5 mm; fixed hinge blocks 1.0 mm from the left partition (no relative motion) | closes the clamp loop (card → anvil → bay frame → pedestals → hinge; latches → anvil) inside LOWER + UPPER; BASE has no structure above the deck there | interface, LOWER, BASE params/fluidics, UPPER checks |
| 5 | pass-throughs: BASE IR-2/IR-4/IR-6 vs LOWER ICR-6 | exits = the LOWER routes (`LIQUID_LINE_EXITS`, table §8); BASE re-routed to them (grommet windows in the partitions), cable window, Peltier exhaust duct extension + front-bay louvre, umbilical grommet, Gamry flange 16 × 20; tubing schedule re-issued with the real LOWER lengths (docs/22 §5.3) | LOWER's exits follow from the port positions, R 25 bends and the M_d sweep (no freedom); BASE lanes are free | interface, BASE params/parts/layout/fluidics |
| 6 | LOWER mount IR-1 | `LOWER_MOUNT`: 6 × M6 at X 165/305 × Y 35/110/185, dowels (165, 50) round, (305, 50) slot | the X 235 holes lie under the M_d stage | interface, LOWER parts (base plate), BASE params |
| 7 | drag slot ICR-2 / DEV-L4 | widened slot `slot_polygon()` (buffers ∪ swept 2.6-sq holder + 0.30); square holder kept | a round holder cannot hold the 2 × 2 magnet (diagonal 2.83); keeps docs/13 magnet and gap; foil 19 µm at G1/G2 ≤ 20 µm (M4 acceptance) | interface, LOWER geom |
| 8 | pogo ICR-3; pogo 7.25 N vs pad 11–12 N | `POGO` tip_z_retracted **−1.66**, 1.21 N/pin (7.25 N); pad 12 N kept | −1.0 needed 1.66 mm compression > 1.27 travel; pad must exceed pogo (net 4.75 N on the die) | interface, LOWER geom |
| 9 | M_c motion ICR-4 / DEV-L1/L2; thick zones ICR-5 / DEV-L3 | adopted: swing R 64.5, parks (40, 56.7)/(40, −6.7), top −45.6, fail state **hold**; thick zones as built | spring-up would drive M_c into the M_d post; 10× lower stray force at the own chamber | interface |
| 10 | magnetics/materials ICR-8; UPPER pins/springs 1.4310; WE relay 1.9 mT | pins Nitronic 60 (fallback 1.4404 annealed, μr ≤ 1.02 checked), pin springs Co-Cr-Ni, yokes/spring plate/buttons 1.4404, guides CuSn8, datum pins zirconia, head guide pins 1.2842 (≥ 45 mm from magnets); relay stays in the bay, screened reed relay + mu-metal can, 5 mT acceptance (`WE_RELAY_FIELD`) | work-hardened 1.4310/1.4301 is partly martensitic; leads ≤ 0.3 m forbid moving the relay out | interface `MATERIALS`, UPPER params/parts (docs) |
| 11 | card: P_mv ring vs V8 lead-in; MC shape; poka chamfer; tooling holes; WE2 2.9/3.0; DIE_WINDOW_CLEAR; CER_NECK | no lead-in at V8 (ring OD 7.0 kept); MC Ø1.596; `CARD_POKA_CHAMFER` + LOWER nest corner block (`NEST_POKA_BLOCK`); `CARD_TOOLING_HOLES` (no anvil feature); WE2 **2.9** confirmed, cell **1.31 µL**; `DIE_WINDOW` explicit; `CER_NECK['len']` | keeps every docs/13 functional number except the cell volume (−2.1 %, DEV-C4, calibrated) | interface, card profiles, LOWER parts |
| 12 | tip margin ICR-7 | `VALVE_TIP_EDGE_MARGIN` 0.5 to through-openings; `VALVE_TIP_SEAT_MARGIN` 0.3 to gasket seats (V3 → P_byp 0.36 passes) | the compressed gasket supports the foil; an opening does not | interface |
| 13 | cad/README.md out of date | rewritten (packages, build commands, flags, output policy) | — | README |
| 14 | (found at integration) `PLUNGER tip_z_open` 1.015 ≠ closed 0.17 + stroke 0.8 | **0.97** | the lid CAD already drew 0.97 | interface |

Not requested but found by the integration (docs/23 §4): the nominal closed tip height z 0.17 lies 0.145 below the L1
top over the channel lands (the real tip stops on compressed TPE) → hook gap set on a reference card (I-13); see docs/23
§4 for the cross-module check results and §9 for the open defects.

## 16. Revision history
* Revision A (2026-11-13): interface phase.
* Revision B (2026-11-13): integration of docs/19–22 (this §15; `interface.py` changelog block).
