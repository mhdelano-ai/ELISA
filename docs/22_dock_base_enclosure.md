# 22 — Dock base: frame, fluidics, electronics, enclosure (cartridge A, C2 prototype)

Status: 2026-11-13, **stage C0 desk work**, physical design round, DOCK BASE agent; **revised at integration**
(docs/23, interface.py Revision B): lid air 400 kPa, exact LOWER line exits and re-routed lines, re-issued tubing
schedule, Peltier exhaust duct + louvre, right well partition moved to X 323–325, `base_assembly_with_claims.step` only
with `--all-states`; all §14 requests resolved (docs/18 §15). Inputs: docs/00, 02 §3–§4, 11 §5,
13 Revision B (§2.5–§2.6, §3.1, §3.7, §5, §6, §7.3), 16 §2–§3, 18 (binding ICD), `cad/elisa_cad/interface.py`
(imported, not edited), `automation/config/hardware_lab.example.yaml`. Nothing is ordered. docs/13 and docs/18 are not
edited; departures are listed in §13, interface change requests in §14.
CAD: `cad/elisa_cad/dock_base/` (`python -m elisa_cad.dock_base.build` from `cad/`, ≈ 5 min, `--fast` without
renders ≈ 15 s). Outputs: `cad/out/dock_base/` (STEP, PNG/SVG, `tubing_schedule.csv`, `check_results.json`).

Source tags as docs/18: docs section | `interface.NAME` | **Derived** (arithmetic shown or in `calcs.py`) |
**CHOICE-Bn** (§12) | **DEV-Bn** (§13) | **IR-n** (§14) | **UNVERIFIED** | [assessment] | **V:key** = vendor page
opened this session (§17). Units mm, kg, W, °C. Coordinates: DOCK (interface.py §1): X to the operator's right,
Y away from the operator, Z up, origin front-left at bench level.

**Revision C (revised after review, docs/24 §8).** (B1) P_in line **PEEK 1/16″ × 0.0635 mm (0.0025″) ID** (2.66 µL incl.
1 µL sensor; was 0.127 mm, 7.63 µL), P_in sensor range 0–25 bar; **S_IC1/S_IC2 moved beside the bay** (front of the
left-rear zone, X 54–144, Y 208–299, valves facing −Y): tidal coils **78.5 / 76.3 µL** (387 / 376 mm; were 140 / 160);
the electronics are re-arranged in three grounded boxes (main, side, rear in the two vacated pump-row slots); new
routed A1/waste lines for S_IC1/S_IC2; carry-over budget re-computed by `calcs.carryover_budget()` (docs/23 §9.1).
(S6) the 60-cm cable 985-00071 is listed by Gamry for the Reference 600 only; on a 600+ it needs Gamry's IE correction
file → conditional (§9.5). (M3/M4) stale numbers harmonised from `calcs.py` (prime 15.0 mL). (M5) pogo-lift 3/2 valve,
its air line to G_C and an 8-channel aux valve driver allocated; the stepper for the pogo lift dropped. Rebuilt; all
checks pass (§11).

## 1. Summary

| Item | Value | Source |
|---|---|---|
| Overall envelope | **470 W × 420 D × 330 H** (= `interface.DOCK_FOOTPRINT`); E-stop and light bar protrude 25 / 6 mm at the front; lid open → 388 H | CHOICE-12; Derived (`lid_sweep_bbox()`) |
| Bench width with stack and Gamry | 343 (stack) + 50 + 470 + 10 + 90 (Gamry) = **963 mm**; depth 712 (stack) | §11.1 |
| Mass | DOCK BASE 34.7 kg (A1 full, waste full); + allowance LOWER 8 kg, UPPER 5 kg (UNVERIFIED) → **≈ 48 kg**; Gamry 3 kg separate | `calcs.mass_cog` |
| Centre of gravity | X 232, Y 208, Z 126 (full); ≥ 178 mm inside the foot rectangle | §11 |
| Power | DC peak 358 W, average 136 W; mains ≈ 406 W peak / 155 W average (η 0.88 UNVERIFIED); 2 × 24 V 350 W + 12 V low-noise | §9.2 |
| Air | lab air / N₂ **500–700 kPa (≥ 450 kPa at the inlet)**, ≈ 1.1 L/min free air (dominated by an UNVERIFIED Flow EZ allowance); lid pilots **400 kPa** (revised at integration, was 300) | §8 |
| Liquids per card (14 runs) | A1 38 mL, waste 45 mL, conjugate 0.40 mL, HQDP 0.85 mL, beads 0.24 mL (prime **15.0 mL**, revised after review: one value from `calcs.prime_volume`) | §6 |
| Card plane | Z 170 → 1070 mm above the floor on a 900 mm bench (UNVERIFIED bench height) | `interface.ANVIL_TOP_Z_DOCK` |

Key decisions: five Tecan Cavro Centris (envelope verified): S_b, S_A, S_RC in a rear bank facing a rear service door,
S_IC1/S_IC2 beside the bay (revised after review); insulated cold
box front-left with a direct-to-air Peltier assembly (Laird/Tark DA-024-24, verified) and a rocked bead vial; S_b's
6-port selection valve on top of the cold box so the bead line is 1.9 µL; all liquid waste into one air-gap head on a
1 L waste bottle; electronics in a grounded sub-enclosure left-rear (noisy zone), cell leads 0.13 m in an isolated duct
to a junction box on the right wall (quiet zone), Gamry on the bench to the right; whole-footprint stainless drip tray.
All one-off checks pass (§11): no intrusion into UPPER/LOWER claims, lid sweep or loading path; no tube clash.

## 2. Scope

Everything outside the card bay: base plate, frame, bay deck (interface to LOWER), fluidics (pumps, valves, bottles,
coils, pressure channels, flow sensors, waste, SM-FL line), cold compartment, electronics, Gamry placement and cell-lead
route, enclosure, drip tray. Pumps, valves, bottles, sensors, PSUs, boards and the cooler are **placed envelope bodies**
(outer dimensions, ports/connector faces marked); plates, frame, deck, tray, partitions, panels, cold-box shell, pump
shelf/spine, holders, duct and junction box are real parts. LOWER_* and UPPER_* claims, the lid sweep and the loading
path are keep-outs.

## 3. Layout (dock coordinates)

| Zone (claim) | Content | Key coordinates |
|---|---|---|
| BASE_drip_tray (Z 0–15) | 4 levelling pads (Z 0–5), Al base plate 10 mm (Z 5–15); stainless tray sits on the plate (Z 15–28, rim 13) | feet at (30, 30), (440, 30), (30, 390), (440, 390) |
| BASE_under_bay (Z 15–40) | bay deck Al 10 mm (Z 30–40) on 5 spacers; waste/purge raceway at Z 24–27; tray sump + level switch at X 245–285, Y 150–190 | deck = LOWER_bay footprint X 150–320, Y 20–200 |
| BASE_cold_compartment | cold box X 24–122, Y 2–150, Z 17–150 (door Y 2–20); cooler warm side X 43–103, Y 150–206; above the box (Z 150–220): P_in sensor, SM-FL PEEK line, SV_b; strip X 122–145: rocker motor, tube verticals to gland G_W | §7 |
| BASE_electronics | (revised after review) S_IC1/S_IC2 on a front shelf X 52–145, Y 207–300 (valves facing −Y at Y 208); electronics in a main box X 4–144, Y 302–396 and a side box X 4–50, Y 207–300, Z 35–318 | §5, §9 |
| BASE_rear_low (Z ≤ 180) | Flow EZ ×2 (X 160–306, Y 212–304), 3/2 valve manifold and FS1 on top, cover Z 178–180 | §5, §8 |
| BASE_pumps | shelf + spine, S_b, S_A, S_RC at X 172/352/412, bodies Y 325–394, valves face +Y (rear door); the slots X 200–325 hold the rear electronics box (drivers, LINK) (revised after review) | CHOICE-B2 |
| BASE_bottles | front row: A1 500 mL (X 337–423, Y 10–96), HQDP 15 mL in a dark sleeve (X 428–458); rear row: FR1, R2, pressure switch, A1 manifold, purge restrictor, FS2; Gamry duct crosses at Y 99–115, Z 125–145 | CHOICE-B3 |
| BASE_right_rear | waste 1 L (X 335–436, Y 208–309) with air-gap head and level sensor | CHOICE-B4 |
| BENCH_gamry | Reference 600+ at X 480–570, Y 90–360, front panel toward the operator | CHOICE-B10 |
| Well (open top) | X 150–320, Y 0–312 open above the card bay for the lid; partitions X 147–149 / 323–325 (revised after review, docs/24 M3: was written 321–323; code `PART_X` 323–325 since integration), rear wall Y 312–314 | §10 |

Plan, elevations and views: `plan_top_labelled.png/.svg`, `view_front_elevation.png`,
`view_right_elevation_lid_sweep.png`, `view_iso_front_left.png`, `view_iso_front_right.png`, `view_rear.png`,
`view_fluidics_no_enclosure.png`, `view_fluidics_rear_left.png`, `view_cold_compartment.png`,
`view_electronics_bay.png`, `plan_bench_layout.png`, `fluidic_schematic.png/.svg`.

## 4. Structure, bay interface, stiffness

* **Base plate** Al 6082-T6 10 mm, 470 × 420, CNC: M10 bores for the levelling screws (adjusted from above, ±3 mm),
  sump pocket under the tray sump, tapped holes for posts, spacers, isolators, PE stud. Mass 5.3 kg (Derived).
* **Frame** 20 × 20 slot-6 profile (class, part UNVERIFIED): four corner posts (Z 16–308), top rails at Z 308–328 on
  the left, right, rear and over the left/right columns at the front, a rear rail over the well (Y 318–338). No rail
  crosses the card-bay opening (operator access from the front/top).
* **Bay deck (IR-1).** Al 10 mm, top face = LOWER_bay bottom (Z 40), carried by five 30 × 30 Al spacers clamped through
  the tray to the base plate (short, stiff path; stage and anvil on one rigid body). Offered pattern: **9 × M6 at X 165 /
  235 / 305 × Y 35 / 110 / 185, dowel Ø6 H7 at (165, 50), slot 6 × 12 at (305, 50)**; LOWER may use any subset.
* **Stiffness [assessment, Derived].** Base plate as a beam on the foot lines (span 410, I = 420 × 10³/12 = 35 000 mm⁴,
  E 69 GPa): all 468 N distributed → δ = 5WL³/384EI = 0.17 mm; LOWER 100 N at mid-span → 0.06 mm; first-mode estimate
  f ≈ (1/2π)√(g/δ) = (1/2π)√(9810/0.23) ≈ **33 Hz** for the bare plate; corner posts, partitions and panels form a box
  that raises it [assessment, not computed]. Relative motion M_d ↔ anvil is small because both sit on the deck. All
  steppers, pumps and the rocker are idle in read windows (docs/13 §7.2); the pump shelf stands on four elastomer
  isolators (UNVERIFIED part). Series option: 15 mm plate or a ribbed casting (§15).

## 5. Fluidics

### 5.1 Components

| Item | Choice | Envelope / spec | Source |
|---|---|---|---|
| S_b, S_A, S_IC1, S_IC2, S_RC | Tecan Cavro Centris ×5, one RS-485 bus (S_IC1/S_IC2 beside the bay, revised after review) | **44.5 W × 68.8 D × 184.2 H, 1.3 kg, 24 VDC ±10 %, 2.5 A peak**; RS-232/485/CAN, 16 per bus; syringes 50 µL–12.5 mL; 3/4-port and 3/6/9/12-port distribution valves; front zone (valve + syringe) 22 mm deep UNVERIFIED | V:TECAN_CENTRIS_P |
| Syringes | S_b 250 µL, S_A 1 mL, S_IC 1 mL, S_RC 250 µL | — | docs/13 §3.2.2, §5.1, §6.1; S_A [assessment] |
| Valve use | S_b 3-port (A1, coil, bypass); S_A 4-port (A1, P_a, P_a2, waste); S_IC_k, S_RC 3-port (card, waste, A1) | — | docs/13 §5.1, §6.1 |
| SV_b | 6-port low-volume selection valve: vial, P_b, waste, air (0.2 µm filter), A1, coil | envelope 40 × 40 × 45 **UNVERIFIED** (no datasheet found) | docs/13 §5.1 |
| Pressure channels | Fluigent Flow EZ LU-FEZ-0345 ×2 (ch1 P_c, ch2 P_mv + bottles via 3/2 valves) | **91.9 × 71.8 × 131 mm, 634 g, 6 W, supply 1100 mbar (max 1300)**; outlet position UNVERIFIED (modelled on top) | V:FLUIGENT_FEZ_P |
| LINK (USB) | in the electronics bay | ≈ 79 × 57 × 96, 219 g (store listing via search, not opened) UNVERIFIED | — |
| FS1 | Sensirion SLF3S-0600F on the S_A → P_a line (rinse flows) | 48 × 15.5 × 8.9, 2 mL/min FS | docs/11 §5.3 |
| FS2 | flow sensor on P_s → S_RC (fallback sweep 10 µL/min), FS ≥ 20 µL/min | part **UNVERIFIED** (LG16-0150D 7 µL/min marginal, docs/11 §5.3) | — |
| P_in sensor | flow-through, ≤ 1 µL swept, **0–25 bar** (revised after review: 1.2 MPa at the sensor with the 0.0635-mm line at 100 µL/min), non-metallic wetted path, at the left wall (upstream end) | UNVERIFIED part | docs/13 §6.1, §6.8 |
| Waste air-gap head | GL45 cap, 7 used + 2 spare drip nipples ending 10 mm above a funnel, charcoal vent | custom PEEK | CHOICE-B4 |

### 5.2 Routing principles

* (revised at integration) Every card line meets its LOWER tube at the exact exit point of `interface.LIQUID_LINE_EXITS`
  (west X 150, Y 84–116, Z 108–114; east X 320, Y 80.5–110.5, Z 112–115, P_a2 at Y 161.5) through grommet windows in
  the well partitions (**G_W** Y 82–118 / Z 106–116; **G_E** Y 78–113 / Z 110–117; P_a2 crosses the right partition at
  Y 193, Z 122). P_b and P_a share Y 100 (Z 108/110): the deeper line takes the lane further west (x 143 vs 145), so no
  vertical crosses a horizontal; P_d2 runs at Z 104 under the other lines. The LOWER-internal length is now the real
  LOWER route (`dock_lower.geom.tube_route`), no longer a Manhattan estimate.
* (revised after review) S_IC1/S_IC2 coils leave the −Y valve faces at Z 209.2 and run straight to the west strip
  (P_d1 over the S_IC2 lines at Z 216, X 126; P_d2 at the valve height, X 129); their A1 lines come from the manifold
  through the lane gap at Y 201 / 203 (Z 170 / 167), their waste lines drop to the tray raceway (Y 204 / 205, Z 20 / 22)
  and run east to the air-gap head.
* Rear-bank pump lines leave the valves upward, run forward over the pump bodies at Z 232, drop at Y 316.5 (between the well
  rear wall and the pump spine) to lanes at **Z 156–174 ≤ 180** (docs/18 §12: keep Z ≤ 180 behind the bay), run along
  Y 203 (gap between LOWER and rear_low) to the cold-claim strip X 126–143, and down to G_W. East pump lines run along
  X 330/331.5 at Z 100–125 through the bottle bay to G_E.
* Waste lines run in a raceway under the deck (Z 24–30) or over the pumps and end in air at the head (Z 259).
* Tubes: liquid 1/16″ OD (PEEK or FEP); gas 1/8″ × 1/16″ PTFE; air PU 6 × 4 and 4 × 2.5.

### 5.3 Tubing schedule (from the CAD routing; `tubing_schedule.csv`)

Length = DOCK BASE routed polyline + LOWER-internal length (revised at integration: the real LOWER route, card port →
wall exit, `dock_lower.geom.tube_route`) + external. Rows 1–11 re-issued at integration (`tubing_schedule.csv`). Volume = π/4·ID²·length (mm³ = µL) + 1 µL per inline sensor (UNVERIFIED).

| # | Line | From → to | Tube OD × ID | Base | LOWER est. | Ext. | Total mm | µL | docs/13 assumption | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | P_in | SM-FL → P_in sensor → P_in | **PEEK 1.59 × 0.0635** (revised after review; Rev B 0.127, 7.63 µL) | 204 | 119 | 200 | 523 | **2.66** | PEEK 0.3 m, 3.8 µL; ≥ 0.3 m isolation | **DEV-B1** (isolation met: sensor → port 0.32 m; volume now below docs/13) |
| 2 | P_b | SV_b → P_b | PEEK 1.59 × 0.102 | 102 | 129 | 0 | 231 | **1.87** | 0.25 × 50 mm = 2.5 µL | volume met (DEV-B3 geometry) |
| 3 | P_cf | conjugate tube → P_cf | FEP 1.59 × 0.254 | 265 | 92 | 0 | 357 | 18.1 | dead ≈ 100 µL in the fill | OK |
| 4 | P_d1 coil | S_IC1 ↔ P_d1 | FEP 1.59 × 0.508 | 270 | 117 | 0 | 387 | **78.5** | 60 µL coil | ≥ 60 OK (revised after review; Rev B 689 mm / 140 µL) |
| 5 | P_d2 coil | S_IC2 ↔ P_d2 | FEP 1.59 × 0.508 | 259 | 117 | 0 | 376 | **76.3** | 60 µL coil | ≥ 60 OK (Rev B 791 / 160) |
| 6 | P_a | S_A → FS1 → P_a | PEEK 1.59 × 0.254 | 673 | 117 | 0 | 790 | 41.0 | clean A1 | OK (prime) |
| 7 | P_byp | P_byp → air-gap head | FEP 1.59 × 0.762 | 939 | 121 | 0 | 1061 | 484 | waste, air gap | OK |
| 8 | P_s | P_s → FS2 → S_RC | PEEK 1.59 × 0.254 | 555 | 114 | 0 | 669 | 34.9 | pull to waste | OK |
| 9 | P_a2 | S_A → P_a2 | PEEK 1.59 × 0.254 | 441 | 165 | 0 | 606 | 30.7 | clean A1 (docs/18 DEV-6) | OK |
| 10 | P_wo | P_wo → air-gap head | FEP 1.59 × 0.762 | 584 | 108 | 0 | 692 | 316 | waste | OK |
| 11 | P_rf | HQDP tube → P_rf | FEP 1.59 × 0.254 | 256 | 105 | 0 | 360 | 18.3 | dead ≈ 200 µL in the fill | OK |
| 12 | P_c gas | Flow EZ ch1 → umbilical grommet | PTFE 3.18 × 1.59 | 108 | UPPER | 0 | 108 | 214 | gas | + UPPER loop |
| 13 | P_mv gas | ch2 → 3/2 valve → grommet | PTFE 3.18 × 1.59 | 63 | UPPER | 0 | 63 | 125 | gas | + UPPER loop |
| 14 | gas → conjugate tube | 3/2 valve → cap | PTFE 3.18 × 1.59 | 445 | — | — | 445 | 881 | fill at insertion | OK |
| 15 | gas → HQDP tube | 3/2 valve → cap | PTFE 3.18 × 1.59 | 510 | — | — | 510 | 1009 | fill at insertion | OK |
| 16 | S_b holding coil | S_b → SV_b | FEP 1.59 × 0.508 | 468 | — | — | 468 | 94.8 | ≈ 40 µL coil | ≥ 40 OK (larger) |
| 17 | vial line | SV_b ↔ bead vial | FEP 1.59 × 0.508 | 113 | — | — | 113 | 22.9 | returned to the vial | OK |
| 18–27 | A1 → each pump; each pump → waste | manifold → valve; valve → head | FEP 1.59 × 0.762 | 286–711 | — | — | — | 130–324 | supply / waste | OK |
| 28 | A1 bottle → manifold | cap → 1-in/6-out block | FEP 1.59 × 0.762 | 124 | — | — | 124 | 56.6 | supply | OK |
| 29 | lab air → FR1 | right-panel push-in (behind the Gamry) | PU 6 × 4 | 300 | — | — | 300 | — | — | — |
| 30 | FR1 400 kPa → lid | → umbilical grommet | PU 4 × 2.5 | 144 | UPPER | — | 144 | — | — | — |
| 31 | R2 120 kPa → Flow EZ | tee to both supplies | PU 4 × 2.5 | 375 | — | — | 375 | — | — | — |
| 33 | dry-air purge | restrictor → cold box | FEP 1.59 × 0.762 | 540 | — | — | 540 | — | ≈ 0.1 L/min | — |
| 34 | cell leads | LOWER bulkhead → junction box | shielded | 132 | (LOWER) | — | 132 | — | ≤ 0.3 m | OK (§9.5) |

Pressure drops (Hagen–Poiseuille, η 0.89 mPa·s, Derived in `fluidics.dp_kPa`): P_in **1.94 MPa** at 100 µL/min with the
0.0635-mm line (revised after review; Rev B 128 kPa with 0.127 mm) — upstream of the card, on the BSM/SM-FL side (UPLC
class, ≫ 2 MPa), the card sees only the vented-chamber pressure; 19 kPa at the parked 1 µL/min; P_b 135 kPa at 100 µL/min → dispense beads at ≤ 50 µL/min (67 kPa at the pump; the card sees only
the vented-chamber pressure); P_d coils 10–11 kPa at the 25 µL/s tidal stroke, 3.6 kPa at the 500 µL/min drain;
P_s 1.1 kPa at 10 µL/min.

## 6. Liquid budget and bottle sizing (Derived, `calcs.liquid_budget`)

Per card = 14 runs (docs/13 §5.2) + 2 recovery/post-high cycles (docs/13 §4 allowance, 1 mL A1 each [assessment]) +
docking prime (3 × all routed line volumes 3.84 mL + syringes 3.5 mL = **15.0 mL**; revised after review: one value
throughout, Rev B also quoted 14.9). Per day = 3 cards (24-h worst case
[assessment]).

| Liquid | Per card | Per day | Container | Fills last | Note |
|---|---|---|---|---|---|
| A1 (dock) | 14 × 1.52 + 2 × 1.0 + 15.1 = **38.4 mL** | 115 mL | **500 mL** GL45 (Ø86 × 181, listings UNVERIFIED) | 11.7 cards at 90 % | docs/13 §3.7 1.52 mL/run |
| Conjugate | 0.26 fill + 2 × 21 µL line + 0.10 dead = **0.40 mL** | per card | 2 mL screw tube + 2-port cap, in the cold box | fresh per card (daily, docs/13 §5) | — |
| HQDP | 0.60 + 2 × 23 µL + 0.20 = **0.85 mL** (fallback 1.00) | per card | 15 mL conical tube in a dark Al sleeve, ambient | fresh per card | docs/13 §5.2 |
| Beads | 14 × 10 µL + 2 × 1.9 µL + 0.10 dead = **0.24 mL** | per card | 2 mL screw tube on the rocker | fresh per card | docs/13 §5.1 |
| Waste | 14 × 1.9 + 2 + 15.1 + 0.48 (BSM parked 1 µL/min × 8 h) + 0.5 = **44.7 mL** | 134 mL | **1 L** GL45 (Ø101 × 230 UNVERIFIED), level alarm at 800 mL | 17.9 cards | docs/13 §3.7 (≥ 1 L, level sensor) |

Drip tray: 464 × 414 × 13 gross ≈ 2.5 L, ≈ 2.0 L after displacement [assessment] ≥ 1.1 × the largest container (1 L).

## 7. Cold compartment

* **Construction (CHOICE-B5).** Box 98 × 148 × 133 (X 24–122, Y 2–150, Z 17–150): 1.5 mm Al liner, 20 mm PU foam,
  1 mm Al skin; inner 58 × 110 × 93. Front wall = hinged insulated door (Y 2–20, magnetic gasket) behind an opening in
  the front-left panel. Liner low corner drains to the tray; dry-air purge 0.1 L/min (from R2 via a restrictor) keeps the
  box slightly over-pressured (docs/13 §6.6 "dry-gas or desiccant volume").
* **Contents.** Bead vial (2 mL) clamped in an Al cradle on a horizontal shaft (axis X at Y 47, Z 72), rocked ±20° at
  0.2–0.5 Hz by a micro gear motor outside the +X wall (CHOICE-B6), paused in read windows (docs/13 §7.2); vial line to
  SV_b through the roof with a flexible loop. Conjugate tube in an Al block bolted to the liner floor (conduction);
  2-port pressure cap (gas in, liquid out to P_cf). Operator loads both through the door (per card).
* **Cooler.** Laird/Tark **DA-024-24-02-00-00** direct-to-air assembly (24 W rated, 24 V, 2.4 A, 0.3 kg; cold side
  Lc 60 × Wc 40 × Hc 14, warm side Lw 80 × Ww 60 × Hw 56; specs at 32 °C ambient, V:LAIRD_TCA_CAT): cold plate on the
  liner rear wall via a 20 mm Al spacer through the insulation, warm side + fan behind the box (Y 150–206) exhausting
  −X through the left-panel louvre (not toward the card bay).
* **Heat load (Derived, `calcs.cold_box_heat`).** ΔT = 30 °C (dock interior, [assessment]) − 5 °C = 25 K. Walls:
  k 0.025 W/m·K (UNVERIFIED) × A_mean √(0.0944 × 0.0440) = 0.0645 m² × 25 / 0.020 = **2.01 W**; door/gasket +50 %
  1.01 W; rocker shaft (Ø4 stainless) 0.25 W; tubes 0.004 W; purge 1.2 × 1005 × 1.67×10⁻⁶ × 25 = 0.05 W → **3.3 W**.
  Capacity at ≈ 25 K across the module ≈ 40 % of 24 W = 9.6 W [assessment] → margin ×2.9. Pull-down 22 → 5 °C of
  ≈ 270 J/K: ≈ **10 min** (within the ≈ 12 min docking, docs/13 §7.3). Drive: PWM ≥ 25 kHz with LC filter, constant
  through reads (docs/13 §6.3).
* **Condensation.** Skin ΔT = (2.0 W / 0.094 m²) / 8 W/m²K = 2.7 K → skin ≥ 19.3 °C > dew point 11 °C at 22 °C/50 %
  (docs/13 §6.6). Liner condensate from door openings drains to the tray (leak electrode 1 sits beside, not under,
  the drain → the drain goes to the sump via a tube to avoid a false leak alarm).

## 8. Pneumatics and air supply (CHOICE-B12, B13)

(revised at integration) Lab air or N₂, **500–700 kPa (≥ 450 kPa at the inlet, `PLUNGER air_supply_min_kPa`)**, oil-free,
dry, inlet push-in on the right panel at (470, 380, 45) behind the Gamry → **FR1** filter-regulator 5 µm, **400 kPa** → lid
pilot manifold via the umbilical (`interface.PLUNGER` 400 kPa, Rev B; SMC S070 0.5 W pilots rated 0.5 MPa, docs/20) and
the LOWER pogo-lift cylinder (revised after review, docs/24 M5: through a 3/2 solenoid valve in the west strip,
X 130–140, Y 160–180, driven by the aux valve driver; PU 4 × 2.5 line routed under the deck to gland G_C) → tee to **R2** precision regulator 120 kPa → Flow EZ supplies (LU-FEZ-0345 needs
1100 mbar, max 1300, V:FLUIGENT_FEZ_P) and the purge restrictor. Low-supply pressure switch **< 450 kPa** → fault (the
lid switch trips at 350 kPa; plungers are spring-closed and V3 spring-open, so air loss is fail-safe, docs/13 §4).

| Consumer | Free air | Derived |
|---|---|---|
| lid cylinders | 0.012 L/h | (revised at integration) 90 mm³ per actuation × 400/101.3 = 0.36 NmL (docs/20 §4.4) × 17 actuations per 31-min run |
| pogo-lift cylinder (LOWER) | < 0.001 L/h | Ø6 × 6 + 50 mm³ dead, 2 actuations per 8-h card |
| purge | 6 L/h | 0.1 L/min [assessment] |
| Flow EZ ×2 | 60 L/h | **UNVERIFIED allowance** 0.5 L/min each (consumption not on the page) |
| total | **≈ 66 L/h ≈ 1.1 L/min** | 8-h card without supply: 530 L → an 88 L tank at 7 bar; therefore lab air, not a tank |

No compressor in the dock (vibration and noise near nA reads). Fallback if no lab air: off-dock oil-free compressor
with ≥ 20 L receiver on the floor, cycling not synchronised with reads (effect UNVERIFIED → measure in M5a-type test).
The lid agent sizes the pilot manifold; this supply offers 400 kPa at ≥ 10 L/min (FR1 class, UNVERIFIED).

## 9. Electronics

### 9.1 Blocks (revised after review: main box X 4–144, Y 302–396; side box X 4–50, Y 207–300; rear box X 200–325, Y 325–416, Z 37–228 in the vacated pump slots; `view_electronics_bay.png`)

(revised after review, docs/24 B1/M5) Placement: main box — PSU_M, PSU_T (standing), USB hub, mains filter, LabJack,
intake grille, 80-mm fan; side box — PSU_L, controller + watchdog, relay/interlock board; rear box — DIN plate,
Fluigent LINK, 21-ch pilot driver, **8-ch aux valve driver (new: pogo-lift 3/2 valve, 3 × 3/2 fill/P_mv switch valves,
spare)**, stepper and thermal drivers. Contents as before:
PSU_M 24 V 350 W (motion, valves, logic) and PSU_T 24 V 350 W (thermal) — Mean Well LRS-350-24 class, 215 × 115 × 30,
0.76 kg (search listings; datasheet 403 → UNVERIFIED); PSU_L 12 V low-noise 15 W; mains filter + fuses + K1 safety
contactor; DIN mounting plate at X 74–76; dock controller + **independent hardware watchdog** (heartbeat from Python,
docs/13 §6.2); relay/interlock board (E-stop loop, lid switch, leak inputs, safe-state relays); 6 stepper drivers
(M_c ×2, M_d cam Z, rocker, 2 spare — the pogo lift is a pneumatic cylinder, docs/21 CHOICE-L16; Rev B listed a
stepper for it; disabled in read windows); 4 Peltier/heater channels PWM ≥ 25 kHz + LC
(CHOICE-B7); 21-channel pilot-valve driver (cable via the umbilical); LabJack U3 (75 × 115 × 30, listings, UNVERIFIED)
behind an opto-isolated Inject Start input (SM-FL connector 1 pins 1–2, docs/02 §3.1); isolated USB hub (controller,
U3, LINK, USB–RS-485 for the pumps); Fluigent LINK. All parts except the Centris, Flow EZ and cooler are to be selected.

### 9.2 Power budget (Derived, `calcs.power_budget`; allowances UNVERIFIED)

| Load | Rail | Peak W | Avg W |
|---|---|---|---|
| 5 Centris (2 moving at once, 2.5 A peak each, V:TECAN_CENTRIS_P) | M | 120 | 15 |
| 2 Flow EZ (6 W) + LINK | M | 14 | 14 |
| 21 pilot valves (≤ 10 on, 1 W UNVERIFIED) | M | 10 | 4 |
| steppers (LOWER parts) / M_d stage | M | 40 / 20 | 8 / 6 |
| aux valves (pogo-lift 3/2, 3 × 3/2 fill/P_mv; ≤ 2 on, 1 W each UNVERIFIED; revised after review M5) | M | 2 | 0.2 |
| fans | M | 4 | 4 |
| logic, DAQ, sensors, scanner | L | 12 | 10 |
| cold-box Peltier DA-024-24 (2.4 A × 24 V) | T | 57.6 | 35 |
| reagent-zone Peltier (LOWER), anvil + lid heaters | T | 80 | 40 |
| **total** (revised after review) | | **360** | **136** |

Rails: M 210 W / 350, T 138 W / 350, L 12 / 15. Mains (η 0.88 UNVERIFIED): 409 W peak, 155 W average (revised after review: + aux valves).

### 9.3 Heat and airflow

Bay dissipation ≈ PSU losses 19 W + driver losses 9 W + logic 10 W = **38 W** → 0.0031 m³/s = **187 L/min (6.6 cfm)**
for a 10 K rise. One 80 mm fan (part UNVERIFIED) on the box rear wall exhausts through the rear-panel louvre; passive
filtered intake on the left panel (Y 331–394). Cooler exhaust −X through the left panel. **No fan blows on the card bay
or electrode bay** (all air paths stay in X < 145 and leave left/rear); fans run at constant speed, never switched in a
read window. Pumps cool by convection through the rear door louvre.

### 9.4 Grounding and EMC partition

* **Protective earth:** IEC inlet PE → one PE stud on the base plate; panels, frame, tray, pump spine, electronics box
  bonded (star washers/braids). PSU 0 V bonded to PE at one point in the electronics box (SELV).
* **Measurement ground (docs/13 §6.3, docs/02 §4.4):** the Gamry floats. Cell-lead duct and junction box are Al,
  **isolated from the frame** (nylon standoffs) and bonded only at the junction box, which is the **star point** tied by
  a short braid to the Gamry ground terminal named in its manual for floating operation (wording UNVERIFIED) and to the
  electrode-bay shield (LOWER) and the lid cover (UPPER) through the bay.
* **Zones:** noisy = electronics bay (left rear), pumps (rear), cooler, Flow EZ solenoids; quiet = electrode bay
  (LOWER), duct, junction box, Gamry (right). Motor/heater cables enter LOWER via gland G_C on the −X wall (Y 150–195);
  the cell leads leave via the +X bulkhead → ≥ 170 mm (bay width) between them. Peltier/heater leads twisted, shielded;
  PC ↔ dock via the isolated hub (no USB ground loop); Inject Start opto-isolated.

### 9.5 Gamry placement and cell-lead route (CHOICE-B10)

Reference 600+ on the bench at `BENCH_gamry` (9 × 19 × 27 cm, 3 kg, docs/18), front panel toward the operator. Leads:
LOWER bulkhead (320, 107, 135) → duct X 320.5–440 → junction box (X 440–468, Y 91–123, Z 115–155) = **132 mm** + ≈ 20 mm
inside the box; LOWER part (electrode bay card x 54–62.5 → dock X 244–252.5 to X 320) ≈ 70–100 mm → total ≈ 0.25 m
≤ 0.3 m (docs/13 §6.3). A 60 cm cell cable runs from the Gamry front panel to the right-panel gland at (470, 107, 135):
≈ 0.11 m Manhattan, slack coiled. **(revised after review, docs/24 S6) Cable compatibility is conditional:** the Gamry
order page for SKU 985-00071 (60 cm) lists it "For Reference 600 and Interface 1000/1010" only (V:GAMRY_CABLE_60,
re-opened) — the reviewer is right that Rev B's "verified for the 600+" was wrong. A Gamry instruction document
(V:GAMRY_600P_STD_CABLE, PDF text read) describes using the 60 cm Standard Cell Cable PN 985-00071 on a Reference 600+
**only with the Gamry-supplied IE correction file REF600P_CID14.IECOR and a re-calibration with that cable**. The C2
plan therefore: order 985-00071 together with that correction file from Gamry (or a Gamry-confirmed 600+ cable),
confirm the 25-pin connector and lead identities before the bulkhead design (`PASS_THROUGHS['gamry_cell_cable']`);
performance of the corrected set-up against the 600+ specification UNVERIFIED.

### 9.6 Connector panel (rear, X 24–140)

IEC inlet + switch + fuse, PE stud, USB-B ×3 (controller, DAQ via isolator, LINK), Ethernet (spare), Inject Start
(2-pin, from SM-FL connector 1 pins 1–2), E-stop aux contact, RS-485 (spare). Lab-air push-in on the right panel.

## 10. Enclosure, access, safety

1. **Panels** 2 mm Al 5754 powder-coated on the frame, inside the footprint; well partitions X 147–149 / **323–325**
   (right one moved +2 mm at integration: the moving cam lever reaches X 320.0 → 3.0 mm, IR-5) and rear wall Y 312–314
   (to Z 328); rear-low cover Z 178–180 (Y 202–312) with the umbilical grommet slot X 236–262.
2. **Openings:** top open over X 150–320, Y 0–312 (lid sweep and loading path); front-bay panel only to Z 165 (louvre X 186–210, Z 118–144 for the LOWER Peltier exhaust, fed by a 24 × 26 PEEK duct
   extension Y 2–20, revised at integration; card
   plane 170) so the card is reached from the front/top; cold-box door (front-left); bottle door (front-right, X
   327–465, Z 20–255); waste hatch in the top-right panel (Y 200–317) — the waste bottle lifts out vertically; rear pump
   service door (X 152–463, Z 20–301); left panel removable for the electronics; top-left panel removable for SV_b and
   (revised after review) for the valve heads/syringes of S_IC1/S_IC2 (tops at Z 221, 87 mm below the panel).
3. **Service reach:** pump valve heads and syringes face the rear door, 15.5 mm between bodies, door removal gives free
   access; isolators let the whole shelf slide out after the lines are unplugged. SV_b, P_in sensor reached from the top
   (top-left panel); Flow EZ and FS1 by lifting the rear-low cover (with the lid open).
4. **Drip tray (CHOICE-B9):** 316 stainless 1 mm, folded, rim 13, corner notches around the posts, sump 40 × 40 × 8
   with a level switch; four interdigitated electrode strips (under the cold box drain area, bay, pumps, bottles);
   parts that pierce the tray (spacers, isolators, posts) clamp it with sealing washers. Electronics on 20 mm standoffs.
   Leak → fault → safe state → latch (docs/13 §6.8).
5. **E-stop** Ø40 mushroom front-left (Z 265–305) opens K1 (safe state, docs/13 §4). **Status light bar** on the
   front-left top: green run, blue read window ("do not touch"), amber operator action, red fault latch.
6. **Labels:** mains/PE; pinch point (lid); cold surface/condensate; HQ/BQ waste; compressed air 700 kPa max; "read
   window — no actuation" next to the light; card orientation arrow on the nest frame (LOWER).
7. **Ergonomics:** card plane 170 mm above the bench (1070 mm on a 900 mm bench, UNVERIFIED) at Y 75–125 from the
   front edge; operator loading path X 175–285 clear to Z 330; lid top open 388 mm → shelf above the bench ≥ 400 mm.
8. **Operator sequence per card:** open lid; cold door → swap bead vial and conjugate tube (caps stay on their lines);
   bottle door → swap HQDP tube, check A1; insert card; close lid. Waste weekly via the top hatch (alarm at 800 mL).

## 11. One-off checks (run by `build.py`; results in `check_results.json`)

| Check | Method | Result |
|---|---|---|
| Intrusion into UPPER_lid_closed, LOWER_nest_anvil, LOWER_bay | OCC boolean common of every base body and tube with the claim boxes (> 0.5 mm³ flags) | **0 intrusions** |
| Lid sweep 0–85° | sweep = union of the UPPER box rotated about the hinge in 1° steps (convex hulls of consecutive positions, shapely), extruded X 150–320; YZ bounds 29.4–305.0 / 175.3–388.3 = `lid_sweep_bbox()` | **0 intrusions**; clearances to the claim sweep: rear-low cover 1.94, well rear wall 6.98, top rails 22.8, top-rear panel 24.5, left partition / top-left panel 1.0, **right partition / top-right panel 3.0** (revised at integration). Real lid parts (docs/23 §4): 3.5 mm left (cover), 3.0 mm right (cam lever) |
| Loading path | common with `OPERATOR_LOADING_PATH.clear_box` | **0** |
| Base-body overlaps | pairwise AABB (assemblies such as tube-in-holder excluded) | **0** |
| Tube routes vs bodies | each segment sampled every 0.5 mm, swept tube radius vs every body box (its end devices/walls allowed) | **0** |
| Tube–tube | sampled centre-line distance ≥ sum of radii | **0** clashes |
| Containment | cold-box contents inside the liner; boards inside one of the three electronics boxes (revised after review) | pass |
| Footprint | every base body inside `DOCK_FOOTPRINT` | pass except E-stop (Y −25) and light bar (Y −6) |
| Pump/valve service reach | §10.3 | rear door; 15.5 mm gaps; shelf removable |
| Bottle capacities | §6 | A1 11.7 cards; waste 17.9 cards; per-card tubes ≥ 4× need |
| Tube lengths vs docs/13 | §5.3 | (revised after review) P_in 2.66 vs 3.8 µL (DEV-B1); P_b 1.87 ≤ 2.5 µL; coils 78.5/76.3 ≥ 60 µL (DEV-B2); fill dead volumes 18/18 µL ≪ 100/200 µL |
| Carry-over budget (revised after review, docs/24 B1) | `calcs.carryover_budget()`: docs/13 §8.3 allocations × as-built area/volume ratios | Rev B 1.09×10⁻⁴ (open), **Rev C 9.87×10⁻⁵ ≤ 10⁻⁴** (docs/23 §9.1) |
| Cell leads | §9.5 | 0.13 m base + ≈ 0.1 m LOWER ≤ 0.3 m |
| CoG | mass-weighted centroids (+ LOWER 8 kg, UPPER 5 kg allowances) | full (X 232, Y 208, Z 126), margin to the foot rectangle **178 mm**; base only (231, 245, 117), margin 145; lateral force at the top edge to tip forward ≈ 250 N |
| Footprint vs bench | §11.1 bench plan | 963 mm wide, 712 deep (stack) ≤ 750 bench depth (UNVERIFIED) |

### 11.1 Bench layout (`plan_bench_layout.png`, to scale)

ACQUITY stack 343 W × 712 D × 711 H (Waters I-Class BSM + SM-FTN + CH-A spec sheet, PDF text, V:WATERS_ICLASS_SPEC;
the BSM + SM-FL stack of this lab assumed the same footprint — I-Class PLUS SM-FL page returned 503 → **UNVERIFIED**)
at X −393…−50, gap 50 (PEEK line), dock 0–470, gap 10, Gamry 480–570.

## 12. Table of choices (open points decided here; user may overrule)

| # | Open point | Chosen | Why | Alternatives |
|---|---|---|---|---|
| CHOICE-B1 | structure | Al 10 mm base plate on 4 levelling pads, 20 × 20 profile posts/rails, 2 mm panels; bay on its own deck on 5 spacers | short stiff path for stage + anvil; C2 machinable | welded steel chassis; 15 mm plate (series) |
| CHOICE-B2 | pumps | 5 × Cavro Centris: S_b, S_A, S_RC in a rear row (valves to the rear door), **S_IC1/S_IC2 beside the bay on a front shelf, valves facing −Y, service through the removable top-left panel (revised after review, docs/24 B1)** | only pump with dimensions verified this session; one bus; west-going lines on the left | Hamilton PSD/4 (spec page 403; search: 107 D × 127 H × 44 W, UNVERIFIED) |
| CHOICE-B3 | containers | A1 500 mL GL45; conjugate + beads in 2 mL tubes in the cold box (fresh per card); HQDP 15 mL in a dark sleeve at ambient; waste 1 L | daily replacement (docs/13 §5) needs small volumes; 500 mL lasts ≈ 12 cards | A1 1 L (docs/18 note) needs a deeper bay; HQDP cooled (less hydrolysis, more box) |
| CHOICE-B4 | waste | one air-gap head, every line ends in air | breaks the liquid path to earth (docs/02 §4.4), no siphon or back-pressure | individual drip funnels |
| CHOICE-B5 | cold box | PU/Al box, DA-024-24 on the rear wall, warm side out left, dry purge, top at Z 150 | verified part, 2.9× margin; leaves Z 150–220 for SV_b and the SM-FL line | air-to-air AA-024 (needs more height); Peltier under a cold plate holding both tubes |
| CHOICE-B6 | bead agitation | custom rocking cradle ±20°, 0.2–0.5 Hz, motor outside the insulation | no stir bar (docs/13 §5); low heat in the box | end-over-end rotator (taller); commercial mini rocker (no source found) |
| CHOICE-B7 | electronics | grounded sub-enclosure, 2 × 24 V 350 W + 12 V low-noise, PWM ≥ 25 kHz LC-filtered thermal drivers, constant fans, isolated USB | separate supplies and quiet reads (docs/13 §6.3); efficiency vs linear | linear Peltier drivers (≈ 25 W more heat per channel) |
| CHOICE-B8 | access | open well over the bay; front doors (cold left, bottles right); top hatch (waste); rear pump door; removable left/top-left panels | operator tasks from the front/top, service from the rear | side doors (blocked by the stack and the Gamry) |
| CHOICE-B9 | leak | whole-footprint stainless tray, sump + level switch, 4 electrode strips | docs/13 §6.8 | per-zone trays |
| CHOICE-B10 | Gamry | bench right, isolated duct + junction box as star point, 60 cm standard cable | leads ≤ 0.3 m; quiet side away from electronics | Gamry on a shelf above the dock (longer cable) |
| CHOICE-B11 | bead line | PEEK 0.102 mm ID (0.004″), 0.24 m | keeps ≤ 2.5 µL with a realistic route | 0.127 mm ID (3.0 µL, chase 5 µL) |
| CHOICE-B12 | air | lab air/N₂ 500–700 kPa; FR1 **400 kPa** (revised at integration), R2 120 kPa; no compressor in the dock | vibration/noise near reads | off-dock compressor + receiver |
| CHOICE-B13 | pressure channels | 2 × Flow EZ 345 mbar; ch2 shared via 3/2 valves for the bottle fills | fills only at insertion, P_mv idle then (docs/13 §7.1) | third channel |
| CHOICE-B14 | SM-FL line | P_in flow-through sensor at the upstream (wall) end; PEEK **0.0635 mm** ID (revised after review; Rev B 0.127) | ≥ 0.3 m PEEK between sensor and card | sensor at the card (breaks isolation if wetted metal) |
| CHOICE-B15 | flow sensors | FS1 SLF3S-0600F on P_a; FS2 (≥ 20 µL/min FS, TBD) on P_s | docs/13 §6.2 duties | sensors on the waste side |

## 13. Deviations from docs/13 Rev B / docs/18

| # | What | Change | Effect |
|---|---|---|---|
| DEV-B1 | P_in PEEK 0.3 m / 3.8 µL (docs/13 §2.6) is not reachable: stack beside the dock + routing to the bay centre | 0.52 m (0.2 m outside UNVERIFIED, 0.20 m base, 0.12 m LOWER). **(revised after review, docs/24 B1/M4) 0.0635 mm ID → 1.66 µL + 1 µL sensor = 2.66 µL** (Rev B 0.127 mm: 6.63 + 1 = 7.63 µL; the "8.0 + 1.05" and "5.1 / 4.9 µL" of Rev B are superseded; 0.102 mm would give 4.24 + 1 = 5.24 µL) | wetted area of line + M_in ×0.96 of docs/13 (Rev B ×1.72) → carry-over path 2 back to its allocation (docs/23 §9.1); D13 flush (200 µL) = 75 line volumes (Rev B 26); ΔP 1.94 MPa at 100 µL/min upstream of the card; 1/16″ × 0.0025″ PEEK availability and clogging (64 µm bore) UNVERIFIED → E1.10/C2 |
| DEV-B2 | 60 µL tidal coils | (revised after review, docs/24 B1) **78.5 / 76.3 µL** with S_IC1/S_IC2 beside the bay (Rev B 140 / 160 µL to the rear pumps) | stroke stays in the coil (≥ 60); wall area ×1.31 of a 60 µL coil (Rev B ×2.67); ΔP 5–6 kPa at 25 µL/s |
| DEV-B3 | S_b outlet line 0.25 mm × 50 mm (docs/13 §5.1) | 0.102 mm × 231 mm, **1.87 µL** (volume met; revised at integration); holding coil 95 µL (≥ 40) | bead clogging/adhesion in 0.1 mm PEEK unknown → add to M3 / E2.2; fallback CHOICE-B11 alternative |
| DEV-B4 | docs/18 claims: unclaimed space used | cold-box door in the front strip Y 2–20; P_in sensor at X 4–10; tube lanes in the gap Y 200–205; E-stop/light bar outside the footprint (Y −25/−6) | see IR-3 |

## 14. Interface change requests (for the next interface revision; interface.py and docs/18 not edited)

(revised at integration) All resolved in interface.py Revision B (docs/18 §15): IR-1 → `LOWER_MOUNT` (6 of the 9 holes
used, X 235 holes under the M_d stage); IR-2 → `LIQUID_LINE_EXITS` (LOWER's exits; BASE re-routed); IR-3 → claims
`BASE_front_strip`, `BASE_lane_gap`; IR-4 → `PASS_THROUGHS['lid_umbilical']['base_grommet_dock']`; IR-5 → right
partition moved to X 323–325 (lever 3.0 mm), left side 3.5 mm (cover); hinge blocks are fixed (1.0 mm, no motion) on
LOWER hinge pedestals; IR-6 → `PASS_THROUGHS['gamry_cell_cable']['flange_YZ']` 16 × 20 (connector UNVERIFIED).

| # | Name | Current | Needed | Why |
|---|---|---|---|---|
| IR-1 | new `LOWER_MOUNT` (or note on `SPACE_CLAIMS["LOWER_bay"]`) | none | deck top Z 40; 9 × M6 at X 165/235/305 × Y 35/110/185; dowel Ø6 H7 (165, 50), slot (305, 50) | LOWER must bolt to the base |
| IR-2 | `PASS_THROUGHS` | west/east points inside LOWER (212/265, 100, 110) | add wall glands `G_W` X 150, Y 95–125, Z 100–125 (line Y/Z per `fluidics.GW`), `G_E` X 320, Y 60–92, Z 100–125 (`fluidics.GE`), `G_C` cables X 150, Y 150–195, Z 60–140 | base lines cannot reach a point inside LOWER; one Y per line avoids crossings |
| IR-3 | `SPACE_CLAIMS` | front strip Y 0–20 and gap Y 200–205 (X 145–325) unclaimed | add `BASE_front_strip` (0–470, 0–20, 15–330) and `BASE_lane_gap` (145–325, 200–205, 15–178); allow front controls to Y −25 | used for the cold-box door and the tube lanes |
| IR-4 | `PASS_THROUGHS["lid_umbilical"]` | (235, 200, 190) | add base hand-over: grommet slot X 236–262, Y 205–211, Z 180; P_c at X 240, P_mv 248, pilot air 258, cable bundle; UPPER owns the flexible loop to (235, 200, 190) | Z ≤ 180 rule behind the bay |
| IR-5 | UPPER lid width | lid claim X 150–320 touches the well partitions (1.0 mm clearance) | lid hardware ≥ 3 mm inside X 150–320 (or claims narrowed 3 mm) | rubbing/pinch risk |
| IR-6 | `PASS_THROUGHS["gamry_cell_cable"]` | point (320, 107, 135) | bulkhead flange ≤ 16 × 20 mm on that axis (duct inner section) and connector type | duct mates the bulkhead |

No error found in interface.py; the Z ≤ 180 rule is confirmed by the swept solid (1.94 mm to the cover).

## 15. Series-dock notes

Sheet-metal or cast chassis with a 15 mm ribbed base and 6 feet; one PCB for controller, watchdog, stepper, thermal and
pilot drivers; OEM pressure module instead of Flow EZ + LINK (Fluigent F-OEM appeared in search, not opened); moulded
insulated cold drawer with keyed reagent tubes (RFID/2-D code) and a moulded bottle bay; pumps stay Centris-class (OEM
already); (done in Rev C: S_IC1/S_IC2 beside the bay, coils 76–79 µL); internal diaphragm
compressor + receiver only if users lack lab air, run outside read windows on isolators; target footprint ≈ 420 × 400.

## 16. Open items / UNVERIFIED
(revised after review) 1/16″ × 0.0025″ PEEK tubing (availability, clogging) and a 0–25 bar flow-through P_in sensor;
Centris operation with the valve facing −Y on the front shelf (mounting UNVERIFIED as for the rear bank); latch
switches and pogo-lift valve parts; Gamry 600+ cable/IECOR file (§9.5).

Pump front-zone depth and mounting holes; SV_b part and envelope; Flow EZ outlet position and air consumption; LINK
dimensions; FS2 part (≥ 20 µL/min); P_in flow-through sensor part; LRS-350-24 datasheet (403); LabJack U3 enclosure
size and isolation; DURAN bottle dimensions (listings only); 20 × 20 profile data; PU foam k; cooler capacity at ΔT
25 K (curve not extracted); levelling pads, isolators, fans, E-stop, light bar, level/leak sensors; SM-FL outlet to dock
length (0.2 m); bench depth/height; I-Class PLUS SM-FL stack footprint; Gamry ground-terminal wording for floating
operation; bead adhesion in 0.1 mm PEEK (DEV-B3); LOWER-internal line lengths are estimates; masses of LOWER/UPPER are
allowances; plate first mode not computed with the frame.

## 17. Sources opened this session (2026-11-13)

* Tecan Cavro Centris OEM page: https://partnering.tecan.com/cavro-centris-pump-for-oem-liquid-handling
* Fluigent Flow EZ: https://fluigent.com/research/instruments/pressure-flow-controllers/lineup-series/flow-ez/ and the
  datasheet PDF via https://www.fluigent.com/resources-support/support-tools/downloads/technical-datasheets/flow-ez-datasheet/
* Laird/Tark thermoelectric cooler assemblies catalogue (DA-024-24-02-00-00):
  https://tark-solutions.com/sites/default/files/fields/media.file.field_media_file/2023-09/Thermoelectric-Cooler-Assemblies-Catalog.pdf
* Waters ACQUITY UPLC I-Class (SM-FTN) specification sheet (PDF text):
  https://ucrf.unist.ac.kr/wp-content/uploads/2024/11/ACQ.-I-Class-PLUS-Sys.-CH-A-wSM-FTN-I-Specification.pdf
* Gamry Reference 600 cell cable 60 cm: https://orders.gamry.com/reference-600-cell-cable-60-cm.html (re-opened after
  review: "For Reference 600 and Interface 1000/1010")
* Gamry, Instructions for installing Standard Cable on Reference 600+ (PDF):
  https://cn.gamry.com/assets/Uploads/Instructions-for-using-a-Standard-Cable-on-a-Reference-600+.pdf (opened after review)
* Not reachable / not containing the numbers: Hamilton PSD/4 spec page (403), Mean Well LRS-350-24 (403), DWK/Bartelt
  DURAN pages (403/truncated), labjack.com U3 page (no dimensions), Waters I-Class PLUS pages (503), norelem profile page
  (truncated). Search-result summaries for these are marked UNVERIFIED above.

## 18. Files

`cad/elisa_cad/dock_base/`: `params.py` (constants, sources), `layout.py` (106 placed bodies with mass, source,
spec), `fluidics.py` (34 routes, schedule, ΔP, clash checks), `parts.py` (solids, lid-sweep solid), `calcs.py` (budgets,
mass/CoG, checks), `render.py` (views, plans, schematic), `build.py`.
`cad/out/dock_base/`: `base_frame.step`, `base_enclosure_panels.step`, `base_drip_tray.step`, `base_brackets.step`,
`base_cold_compartment.step`, `base_pumps.step`, `base_bottles_pneumatics.step`, `base_electronics.step`,
`base_sensors.step`, `base_gamry_route_bench.step`, `base_tubing.step`; `base_assembly_with_claims.step` (claims and
the lid sweep as translucent placeholders; 5 MB) only with `--all-states` (revised at integration); PNG/SVG views listed in §3; `tubing_schedule.csv`,
`check_results.json`.
