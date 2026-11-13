# 21 — Dock LOWER bay: nest, anvil, magnet bay, electrode bay, reagent cold plate (C2 prototype)

Status: 2026-11-13, **stage C0 desk work**, physical design round, DOCK LOWER — design and checks complete for this round;
**revised at integration** (docs/23, interface.py Revision B): guide bushes at (−8, 46)/(84, 4), anvil x −15…91, nest
corner block for the card's poka-yoke chamfer, two latch catch brackets, two hinge pedestals, bolt/dowel holes to the
BASE deck, clamp design 300 N, interface now holds the slot, pogo, M_c and thick-zone values of §8/§9 (all §9 requests
resolved, docs/18 §15); by default only `assy_lower_bay_hold_RC.step` is written (`--all-states` for the rest). Cartridge A only (docs/13 Rev B),
dedicated bench dock, **C2 prototype** (catalogue actuators + machined parts). Inputs: docs/18 (binding),
`cad/elisa_cad/interface.py` (imported, not edited), docs/13 §2.2/§2.5/§2.7/§3.3/§3.8/§6/§7.2, docs/11 §5.4, docs/16
§2–§3, `mag_b.py`/`mag_far.py`. Nothing is ordered. This document changes no other document.
CAD: `cad/elisa_cad/dock_lower/` — `cd cad && python -m elisa_cad.dock_lower.build` (≈ 5 min; `--fast` skips the
M_d sweep, ≈ 2.5 min; `--all-states` adds the five other state assemblies and the sub-assemblies) → `cad/out/dock_lower/`
(STEP in **dock** coordinates, PNG in card coordinates, `calcs.json`, `checks.json`, `build_summary.json`). The
module checks use the interface card envelope (now with the poka chamfer); the real card is checked in docs/23.

Source tags as docs/13/18: docs § | `I.NAME` (interface.py) | **Derived** (arithmetic shown or in `calcs.py`) |
**CHOICE-Ln** (§7) | **DEV-Ln** (§8) | **ICR-n** (§9) | **UNVERIFIED** | [assessment]. Units mm, N, °C, card coords
(z = 0 = anvil top = datum C) unless "dock" is written.

**Revision C (revised after review, docs/24 §8; interface Rev C).** (B2) cold zone re-designed after the corrected
heat budget (§5.4): cold block x 2.6–20 / y 3–47 behind a 2-mm gap bridged only by a 1.5-mm PEEK lip + 4 PEEK pads,
foam below and 7.5 mm round the block; TEC **Custom Thermoelectric 07111-5L31-03CL** (spec sheet opened) instead of
12711-5L31-04CL; heat sink 24 × 73 base (fins to z −52) with the fan at its −y end; required sink R_th ≤ 1.6 K/W; no
envelope change. (S2) round Ø2.6 M_d holder with a Ø2 × 4 magnet; slot arms 3.4; every slot-valve span 3.40 (§5.1).
(S4) gasket installed ID = tube OD (free ID 1.50). (M7) bead-out step incl. G4 and Z stroke (§5.6). (M12, M13)
incoming checks (§4). Rebuilt (full build incl. the M_d sweep).

## 1. Summary

* **Anvil** — one Al plate (x −15…91 (revised at integration; was −12…90), y −16…66, 15 thick) carrying the nest frame on top and the cold zone in a
  cut-out; a bottom pocket (x 32.5–62.5, y 0–50) leaves the **5-mm plate** over the magnet bay with windows W1/W2
  (11.4 sq), the drag slot (interface slot ∪ holder sweep + 0.30, DEV-L4), the contact opening and the M_w recess.
  Ten PEEK port inserts (+ P_cf in the cold block) with bonded 1/16″ PEEK tubes and flat gaskets, inserted from
  below and held by seven retainer plates; gaskets replaceable from the top.
* **Nest** — anodised Al frame 5 mm on the anvil: zirconia datum pins A1/A2/B, two spring pushers, 1.5 × 45° lead-in
  for a vertical drop, 1.8 mm clearance with a perimeter **drip gutter** and two drains, card-presence sensor, two
  bronze bushes for the lid head guide pins at interface `HEAD_GUIDE_PINS` (−8, 46) / (84, 4) (revised at integration;
  ICR-1 asked (−7, 46)/(83, 4)), and a **corner block** 0.3 clear of the card's 4 × 45° poka-yoke chamfer at (75.5, 50)
  (revised at integration, `NEST_POKA_BLOCK`: a card in any wrong orientation lands on it, checked with the real card).
* **Integration parts** (revised at integration): two Al **latch catch brackets** on the anvil front face carrying the
  Kipp K0045.9143372 catch plates of the lid latches (95 N each up; 22 MPa bending, Derived); two Al **hinge pedestals**
  (dock X 150–154 / 316–320, Y 185–200, Z 44–160) on the bay base plate carrying the lid hinge blocks; bay base plate
  bolted to the BASE deck with 6 × M6 (dock X 165/305 × Y 35/110/185) + 2 dowels (`LOWER_MOUNT`).
* **Cold zone** (revised after review) — Al cold block (x 2.6–20, y 3–47) behind a 2-mm insulation gap (PEEK lip 1.5 mm +
  foam; break x 20–24 the same), one 30 × 30 Peltier (Custom Thermoelectric **07111-5L31-03CL**), heat sink 24 × 73
  + fan exhausting forward through a duct, 7.5-mm foam, dry-air purge; heat load **2.31 W (3.47 W design)**; at a sink
  of 1.6 K/W and 30 °C air: Th 49.7 °C, 1.72 A, 8.9 W electrical, 12.3 W exhausted. Rev B (1-mm full-depth PEEK walls)
  leaked 7.07 W, not 1.16 W (reviewer, confirmed §5.4).
* **M_c units** — magnet holder with a **flange that seats on the plate underside** (gap 0.160 set by geometry, not
  by an actuator), on a **parallelogram swing (R 64.5)** driven by a self-locking worm: up ↔ parked at (40, 56.7) /
  (40, −6.7), top z −45.6 (DEV-L1, DEV-L2). Fail state: hold (worm), not spring-up — a spring return would hit the
  M_d post in the window.
* **M_d** — two Zaber X-LSM050A (opened: < 3 µm repeatability, 0.000029–26 mm/s) stacked X on Y on the bay base
  plate, a cam/spring Z unit (8 mm, spring-up, up-stop screw sets the gap), Ti post Ø4 / neck Ø2, PEEK holder
  **Ø2.6 round with a Ø2 × 4 magnet** (revised after review; was 2.6 sq with 2 × 2 × 4).
  CAD sweep of every drag, gather, bead-out and lowered-transit path: **0 collisions** (§6).
* **Electrode bay** — grounded Al box (x 54–62.5, y 28.8–36.5, z −58…−5) with a PEEK pogo block (6 × PTR 1007.70-class
  probes, 1.21 N each) lifted 3 mm by a 2:1 wedge from a pneumatic cylinder outside the box (no electrical actuator in
  the bay); the block's nose and shoulder locate it in the contact opening and on the plate (no scrub); reed relay,
  RH/T sensor, leak electrode and drain inside; shielded cable to the Gamry bulkhead (dock 320, 107, 135).
* Departures: 6 deviations (DEV-L1…L6), 9 interface change requests (ICR-1…9, §9). Biggest: the M_c motion and
  fail state, the slot width, the pogo retracted tip height, the head guide pin positions and the tube exits.

## 2. Assembly description

Stack (card z): nest frame 0…5.0 | anvil top 0 (lapped) | thin plate −5…0 | thick zones −15…0 | heaters −15.3…−15 |
retainers −18…−15 | M_c links −31…−16 (up) | electrode bay −58…−5 | tubes −62…−15 | M_d Z unit −80…−62 | X stage
−104…−82 | Y stage −126…−104 | bay base plate −130…−126 (= dock Z 40, `LOWER_bay` floor). Everything inside
`LOWER_nest_anvil` (z −15…+6) and `LOWER_bay` (z −130…−15), x −40…130, y −55…125.

**Anvil module** (lifts off the bay frame on four dowels as one unit, §6.6): anvil + nest frame + pins/pushers/bushes,
11 inserts/gaskets/tubes/retainers, heaters, cold stack (PEEK frame, cold block, Peltier, heat sink, fan, duct,
foam), electrode bay with pogo/wedge/cylinder/relay/RH/leak electrode, both M_c units (brackets bolted under the
anvil's N and S edges), thermistors.
**Bay frame** (stays): base plate, walls W (x −38…−30) and E (x 124…130) outside the X-stage sweep, four beams
under the anvil corners; open-top U-slots in the walls for the tubes and the cable.
**M_d system** (stays): Y stage, X stage, adapter, Z unit + umbrella, post, holder + magnet.

States modelled (`geom.STATES`, STEP `assy_lower_bay_<state>.step`; revised at integration: only `hold_RC` written by
default, the others and the sub-assemblies with `--all-states`): `load` (M_c parked, M_d parked lowered under
J, pogo down, pushers extended, no card) · `collect_IC1` (M_c1 up) · `gather_IC1` (M_d up at pass-1 start) ·
`drag_mid_IC1` · `hold_RC` · `beadout_end`; plus `collect_IC2`, `gather_IC1_low` for the checks.
Sub-assemblies: `sub_nest_anvil`, `sub_cold_stack`, `sub_Mc_units`, `sub_Md_system`, `sub_electrode_bay`,
`sub_tubes`. Renders: `nest_anvil_iso`, `anvil_underside`, `anvil_plan`, `magnet_bay_iso_{gather_IC1,collect_IC1}`,
`section_W1_Mc_up`, `section_drag_slot_Md_hold`, `section_beadout_Mw_ebay`, `section_port_insert`,
`section_ebay_pogo_{up,down}`, `section_cold_stack`, `exploded_iso`.

## 3. Custom parts

| Part | Material | Key dimensions | Critical tolerances | How made |
|---|---|---|---|---|
| Anvil | Al cast tooling plate (stress-relieved class, UNVERIFIED grade) — non-magnetic, hard-anodised 25 µm after machining | 106 × 82 × 15 (revised at integration); pocket x 32.5–62.5 / y 0–50 to z −5; openings per `I.WINDOWS`, slot (DEV-L4), `I.ANVIL_CONTACT_OPENING`, `I.M_W_RECESS`; 10 × Ø3.3 H7 insert bores; 2 × Ø10 bush bores; gutter 1.5 × 1.0; 4 dowel holes | top lapped flat **0.010** over the card area (with cold block and PEEK frame lapped as one, target 0.02 total, `I.TOL`); thin plate 5.000 ± 0.005 measured after anodising (sets the M_c gap); openings ± 0.02 to the datum-pin bores of the frame (dowelled) | CNC mill, stress relieve, anodise, lap top as an assembly |
| Nest frame | Al 6061 hard-anodised | 106 × 82 × 5, opening card + 1.8, lead-in 1.5 × 45°; half-open reamed Ø4 bores for the pins; pusher bores Ø4; corner block (poka-yoke) z 0.2–5.0 with 1.5 lead-in (revised at integration) | pin bores ± 0.01 (`I.TOL` datum_pin_position) to the anvil dowels | CNC mill + ream |
| PEEK break frame | PEEK unfilled | U-frame in the cut-out x 0.6–24 / y 1–49, 15 deep; 4.0 wide at x 20–24, 1.0 elsewhere | top coplanar with anvil after lapping | CNC |
| Cold block | Al 6061 | top 18.4 × 46 × 22 deep + spreader 30 × 30 × 5 (x −10…20, y 2…32) under the module; Ø3.3 bore for P_cf; thermistor well | top coplanar (lapped with the anvil) | CNC |
| Port insert (×11) | PEEK | Ø3.29 × 14.62 (anvil) / 21.6 (P_cf); bore Ø1.60 for the bonded tube; top at z −0.38 | length ± 0.01 (sets seal compression 0.12); tube end faced flush with z 0 in a fixture | turn; bond tube (adhesive UNVERIFIED), face |
| Flat gasket (×11) | EPDM or FFKM **50 ShA** (HQ/Tween compatibility UNVERIFIED) | free ID 1.50, stretched over the tube (installed ID 1.5875) / OD 3.3 / 0.50 (`I.FACE_SEAL`, revised after review; Rev B ID 1.7) | thickness ± 0.02 | laser- or die-cut sheet |
| Retainer plates (×7) | Al 6061 | 3 thick, Ø2 tube holes, 2 × M2 each | flat seat at z −15 | CNC |
| Head guide bush (×2) | CuSn8 bronze | Ø10 × 20, bore Ø6 H7, top z 5.0 | position ± 0.01, bore H7 | turn + ream in place |
| M_c holder (×2) | Al 6061 (or Ti) | column 10.6 sq × 4.84 above a 12.6 × 13 × 2 flange; pocket for the 10 × 10 × 5 magnet | flange face → magnet top **4.840 ± 0.010** (magnet bonded against a fixture flat, then checked) | CNC + bonding fixture |
| M_c carrier, links, brackets | Al 6061 | carrier 8 × 8; links 2 × 3 × 5 per side, pivot pitch 64.5, 10 apart; side plates 4.5 thick | pivot pitch equal within 0.02 (parallelogram keeps the holder level) | CNC, reamed pivots, Ø4 shafts in bronze bushes |
| M_d holder | PEEK (or Ti) | **Ø2.6 round** × 4.44, magnet bore Ø2.04 × 4 (revised after review; Rev B 2.6 sq, pocket 2 × 2 × 4) | magnet top at holder top ± 0.01 | turn + bond |
| M_d post | Ti-6Al-4V | Ø4 × 66 + neck Ø2 × 1.4; holder screws on top (M1.6) so it can be fitted through the slot from above | straightness 0.02 | turn |
| M_d Z unit, adapter, umbrella | Al / PEEK | 16 × 16 × 18 block, 2 × Ø3 guide pins, cam + gearmotor (UNVERIFIED); umbrella 20 × 20 × 2 | up-stop M3 × 0.35 screw sets the 0.16 gap (gauge, 5 positions) | CNC |
| Electrode bay box | Al 6061, conversion-coated, grounded to the star point | 8.5 × 7.7 × 53, walls 0.8; gland Ø5 E wall z −45; wedge slot; drain Ø2 | flat top seating on the plate underside | CNC / wire-EDM |
| Pogo block | PEEK unfilled (volume resistivity class > 1e14 Ω m, UNVERIFIED) | nose 5.2 × 3.2 × 4.84 (0.1 radial in the 5.4 × 3.4 opening), shoulder 6.3 × 3.4, body to z −24; 6 × Ø0.87 probe bores on the pad centres (`I.POGO`) | probe bores ± 0.02 to the nose; shoulder-to-nose-top 4.84 (tips free at z 1.34 when up) | micro-mill, ream |
| Pogo guide block, wedge | PEEK | wedge 2:1 ramp, 6 mm stroke → 3 mm lift | ramp angle | CNC |
| Leak electrode | FR4/PTFE PCB, ENIG interdigitated | 6.9 × 6.1 | — | PCB |
| Exhaust duct | PEEK / ABS sheet | 24 × 26 duct, y −55…−14, to the front panel | — | fold/print |
| Bay frame | Al 6061 | base 170 × 180 × 4 (6 × M6 counterbored + 2 × Ø6 dowel holes to the BASE deck, revised at integration); walls 8 / 6 thick; beams 8 × 10; dowels Ø4 | dowel positions ± 0.02 | CNC |
| Latch catch bracket (×2, revised at integration) | Al 6061 | shelf 26 × 25 × 5 + flange 26 × 4 × 11, 2 × M5 into the anvil front face | catch-plate position ± 0.2 to the latch | CNC |
| Hinge pedestal (×2, revised at integration) | Al 6061 | 4 × 15 × 116, top at dock Z 160 (hinge blocks of the lid bolt on), 2 × M5 from below + gusset | top height ± 0.05 (hinge axis) | CNC |

## 4. Catalogue parts

| Item | Maker / part (only if opened) | Spec to meet | Status |
|---|---|---|---|
| M_c magnet ×2 | supermagnete **Q-10-10-05-N** (page opened; the page also names N48 in its text — grade fixed as N42 on the order, B_r UNVERIFIED; revised after review, docs/24 M13): 10 × 10 × 5 ± 0.1, N42, Ni-Cu-Ni, magnetised through 5, 80 °C, ≈ 27.5 N adhesive | B_r ≈ 1.3 T (not on the page → UNVERIFIED) | opened |
| M_d magnet **Ø2 × 4** (axial; revised after review, was 2 × 2 × 4), M_w 3 × 3 × 3 | — | NdFeB N42 class, Ni-coated; charge-sheet model at the bead plane 0.30: \|B\| 0.97×, max lateral ∇B² 0.96×, axial ∇B² 1.06× of the 2 × 2 × 4 (Derived, same B_r) | UNVERIFIED part |
| X–Y stage | **Zaber X-LSM050A** ×2 (spec page opened): travel 50.8, accuracy 20 µm, repeatability < 3 µm, 0.000029–26 mm/s, thrust 25 N cont., flatness < 11 µm, straightness < 14 µm, pitch/roll/yaw 0.03°, non-back-driving, 0.34 kg | footprint not published on the pages opened → **allocation envelope 150 × 40 × 22 per axis, UNVERIFIED**; X–Y bracket and coordinated motion (streams) UNVERIFIED | opened (spec), envelope UNVERIFIED |
| M_c drive ×2 | — | stepper + self-locking worm gearbox, ≥ 0.6 N·m at the shaft, 45° in ≤ 5 s, envelope ≤ 26 × 12 × 30 | UNVERIFIED |
| M_d Z gearmotor | — | back-drivable (≤ 30:1), 4-mm eccentric, 12 N·mm | UNVERIFIED |
| Pogo probe ×6 | **PTR Hartmann series 1007.70** class (page opened): centre 1.27 mm, full travel 1.27, preload 0.50 N, 1.40 N at full travel, drill 0.87 (0.95 with press ring), CuBe Au plunger, ≤ 25 mΩ | fits the 1.8 pitch; tip style and length UNVERIFIED (plunger exposure 1.5 assumed); **spring material not stated on the page (revised after review, docs/24 M12): ask PTR for a non-magnetic spring option, else include the probes in the μr incoming check (≤ 1.02) like the other parts near M_d** | opened (series), part number not chosen |
| Pogo lift cylinder | — | single-acting spring-return, bore 6–8, stroke ≥ 6, **non-magnetic piston (no sensor magnet)** | UNVERIFIED |
| WE relay | — | reed, 1 Form A, insulation ≥ 1e13 Ω, internal mu-metal screen; Pickering "Series X, Y & Z > 1e13 Ω" seen only in a search snippet (page 403) | UNVERIFIED |
| Peltier | **Custom Thermoelectric 07111-5L31-03CL** (spec sheet PDF opened 2026-11-13, revised after review): 30.0 × 30.0 × 5.1 lapped, 71 couples, Imax 3.0 A, Qmax 15.8 W, Vmax 8.6 V, DTmax 68 °C (Th 27 °C curves). Rev B: 12711-5L31-04CL (127 couples, Imax 4.0, Qmax 33.4, Vmax 15.4, DTmax 67) | — | opened |
| Heat sink, fan | — | R_th ≤ **1.6 K/W** at ≤ 12.3 W (revised after review; fins along y, 24 × 73 base, fins to z −52); 25 × 25 × 10 axial fan class at the −y end | UNVERIFIED (catalogue reference Fischer LAM 3 75 ≈ 1.18 K/W, listing via search, not a fit) |
| Anvil foil heaters ×4 | — | polyimide, 0.3 thick, ≈ 10 W total, cut-outs per `parts.anvil_heaters()` | UNVERIFIED |
| Thermistors ×4, RH/T sensors ×2 | — | 10 kΩ NTC class; digital RH/T (one in the electrode bay, one in the nest W wall) | UNVERIFIED |
| Datum pins ×3 | — | zirconia dowel Ø4 m6 × 4.8 (non-magnetic) | UNVERIFIED |
| Pushers ×2 | — | spring plunger Ø4 body, POM tip, 5 N at 1.5 mm stroke (`I.PUSHERS`) | UNVERIFIED |
| Card-presence sensor | — | reflective IR, ≤ 5 × 4 × 3 | UNVERIFIED |
| 1/16″ PEEK tube | — | OD 1.5875, ID 0.25 (P_b 0.25 per `I.PORTS`), **bend radius ≥ 25 mm** (MTC KB opened) | opened (bend rule) |
| L12 linear actuator (considered, not used) | Firgelli/Actuonix **L12** datasheet (opened): 30-mm stroke closed length 82 mm hole-to-hole, 100:1 12 mm/s, 23 N, back-drive 40 N, ±0.2 mm | rejected: 82-mm body does not fit the M_c column or the y space (CHOICE-L18) | opened |

## 5. Calculations (Derived; full numbers in `cad/out/dock_lower/calcs.json`)

**5.1 Anvil plate deflection.** Whole latch force **300 N** (`I.CLAMP_DESIGN_FORCE`, revised at integration; was 250)
on the assay zone (2575 mm²) → q = 0.117 N/mm². Thin plate between thick zones b = 30 (x), a = 50 (y), t = 5, E 69 GPa;
simply supported rectangle α(1.5) = 0.0843 (Roark, recalled, UNVERIFIED): w = α q b⁴/(E t³) = **0.9 µm**, × 5 for the
openings [assessment] = **4.6 µm** (was 3.8 at 250 N). Local upward loads (M_c preload 6 N + pogo shoulder ≈ 10 N) 0.25 µm. Against the
0.16 ± 0.05 gap: negligible. **Foil span under the slot valves (revised after review, docs/24 S2).** The slot is a long
strip, so the clamped long-rectangle coefficient applies: w = 0.00791 F b²/D (Timoshenko, recalled by the reviewer,
UNVERIFIED), D = 7.72×10⁻³ N·m (E 2.6 GPa UNVERIFIED, t 0.315); the circular-plate formula of docs/13 (w = F a²/(16πD))
under-estimates by ×1.4. Rev B: G1/G2 span 4.44 → 30 µm at 1.5 N (strip), 19 µm (circle) — **does not pass** 20 µm.
Rev C (round holder, arms 3.4): min chord through every slot-valve tip **3.39–3.41** → strip **15.6–15.8 µm at 1.32 N**
(1.2 N + 10 %, the force at the real height, docs/20 §4.1 Rev C; margin 4.2 µm) and **17.8–17.9 µm at the 1.5 N limit**
(margin 2.1 µm); circle 11.2 µm. With E 3.2 GPa (TOPAS 5013 TDS) 12.7 / 14.5 µm. The TPE/L3 backing can only stiffen
the laminate; M4 slot variant at a 3.4-mm span decides.

**5.2 Gap tolerance chains.** M_c (geometric stop): anvil flatness 20 + plate thickness 5 + flange-to-magnet 10 +
magnet face 5 → worst **40 µm**, RSS 24 µm ≤ 50 ✓. M_d (stage-referenced): flatness 20 + 2 × stage flatness 11 +
2 × pitch/roll over a 20-mm lever 10 + up-stop 10 + bond 10 → worst 82 µm ✗, **RSS 32 µm** ✓ → measure the M_d gap
at 5 positions at assembly with a gauge through the windows; if any > ± 0.05, shim the Z unit (open item).

**5.3 Face seals.** (revised after review, docs/24 S4) The gasket is cut at ID 1.50 and stretched over the 1/16″ tube
(installed ID = tube OD 1.5875, radial interference 0.044 [assessment]): it seals on the tube OD and on the foil round
the Ø1.0 port hole, so **no annulus is open to the port** (Rev B: ID 1.7 left 0.056 × 0.38 = 0.110 µL per port,
unswept — confirmed). Annulus 6.57 mm² (Rev B 6.28), compression 0.12/0.50 = 24 %, shape factor 0.86; E_c =
E(1 + 2·0.6·S²) (Gent form, k and E UNVERIFIED): **50 ShA 7.4 N, 60 ShA 13.3 N, 70 ShA 17.8 N** per seal. 11 seals at
50 ShA: 81 N; × 1.5 = 122 N ≤ card-face clamp ≥ 198 N (docs/20) → margin 76 N; 60 ShA (1.5 × 146 = 220 N) now exceeds
it → 50 ShA required (CHOICE-L5). Tube end faced flush with z 0 inside the stretched gasket.

**5.4 Thermal (cold zone) — revised after review (docs/24 B2).** *Rev B error, confirmed:* `calcs.thermal()` multiplied
the ±y PEEK walls by an untagged 0.1 and omitted the −x wall; with every wall (1.0 mm PEEK, 15 deep, k 0.25, ΔT 20 K):
±y 2.76 W + −x 3.45 W + break 0.86 W = **7.07 W** (not 1.16 W); total 8.5 W, and the 12711 module would have needed a
0.32–0.50 K/W sink (reviewer) — not reachable in the drawn space. *Rev C geometry (same footprint, no envelope change):*
cold block x 2.6–20 / y 3–47; every gap (W, S, N 2 mm; E break 4 mm) bridged only by a **1.5-mm PEEK lip** (foil
support, z −1.5…0) with closed-cell foam below (z −15…−1.5) and 4 PEEK locating pads 3 × 3; foam round the block
7.5 mm (was 5). *Heat budget* (k PEEK 0.25, COC 0.15, foam 0.035 W/m·K, all UNVERIFIED; ΔT 20 K; `calcs.json`
"thermal", every term Derived):

| Path | Rev B as computed | Rev B corrected | Rev C |
|---|---|---|---|
| W/S/N walls (gap) | 0.31 (×0.1, no −x) | 6.21 | 0.67 (lip 2 × 1.5 / 2 + foam 13.5 / 2 per metre × 78.8 mm) |
| E break strip | 0.86 | 0.86 | 0.20 (lip + foam, 4 wide) |
| PEEK pads 4 × (3 × 3), 2 mm | — | — | 0.09 |
| card laminate + L3 bridges at the break | 0.05 | 0.05 | 0.05 |
| card L3 lateral from the warm y strips (y < 3, > 47) | — | — | 0.19 |
| card top via the PEEK lid plate (10 mm) | 0.50 | 0.50 | 0.50 |
| foam shell (6×10⁻³ m² [assessment]) | 0.84 | 0.84 | 0.56 (7.5 mm) |
| P_cf line and fill | 0.05 | 0.05 | 0.05 |
| **total / design × 1.5** | 2.6 / 3.9 | 8.5 / 12.8 | **2.31 / 3.47** |

*TEC:* **07111-5L31-03CL** (customthermoelectric.com spec sheet opened: 30 × 30 × 5.1 lapped, 71 couples, Imax 3.0 A,
Qmax 15.8 W, Vmax 8.6 V, DTmax 68 °C at Th 27 °C) → S = 0.0287 V/K, R = 2.22 Ω, K = 0.147 W/K (Derived from the
maxima). The 12711 module (K 0.357 W/K) spends most of its current on its own back-conduction at this load. Spreader
3.2 mm (was 5), module x −7…23 centred on the sink, sink top unchanged at z −25.3. *Sink requirement* (self-consistent
hot side Th = T_air + R (Q + P_el), `calcs.json` "sink_sweep"):

| R_sink (K/W) | 25 °C air: Th / I / P_el / Q_hot | 30 °C air: Th / I / P_el / Q_hot |
|---|---|---|
| 1.0 | 32.6 °C / 1.19 A / 4.1 W / 7.6 W | 39.1 / 1.38 / 5.6 / 9.1 |
| 1.4 | 37.0 / 1.31 / 5.1 / 8.6 | 45.0 / 1.56 / 7.3 / 10.8 |
| **1.6** | 39.8 / 1.40 / 5.8 / 9.3 | **49.7 / 1.72 / 8.9 / 12.3** |
| 2.0 | 49.5 / 1.71 / 8.8 / 12.2 | runaway (load not reached) |

Acceptance [assessment]: Th ≤ 50 °C and I ≤ 0.6 Imax at 30 °C air → **R_sink ≤ 1.6 K/W, exhaust ≤ 12.3 W**
(`interface.PASS_THROUGHS['peltier_exhaust']` Rev C). *Sink chosen:* custom extruded Al fin block 24 × 73 base, fins
to z −52 (26.7 total), fan 25 × 25 × 10 at the −y end pulling air along the fins into the front duct (fins limited
by the west tubes at z −56 and the beam_SW lift-off path) — **R_th UNVERIFIED**. Nearest catalogue reference (not a
fit): Fischer Elektronik LAM 3 75 (30 × 30 × 75 + 30-mm fan) ≈ 1.18 K/W and LAM 3 50 1.52–1.94 K/W (distributor
listings via search, not opened → UNVERIFIED); the drawn block has ≈ 0.9× the LAM 3 75 fin volume [assessment] →
expected 1.2–1.6 K/W [assessment]. Verification: first-article thermal test (measure R_sink and Th at 1.7 A) before
C2 assembly; fallback if > 1.6 K/W: heat pipe from the spreader to a sink in the front duct (dock Y 2–20; envelope
unchanged) [assessment]. Anvil heater: loss to the cold zone now 0.96 W (was 7.1 corrected) → 10 W foil heaters keep
their margin (the reviewer's "+6 W" is not needed).
**Dew point** (Magnus, constants UNVERIFIED): 22 °C/50 % → 11.1 °C, 25/60 → 16.7, 22/70 → 16.3. The cold plate
(4–8 °C) is always below → closed foam, dry-air purge (CHOICE-L19); electrode bay at 25 °C has ≥ 8 K margin at
25/60, logged by its RH/T sensor.

**5.5 Magnetics** (`calcs.magnetics()`, method of mag_b.py). Bead force at the own chamber floor during incubation:
M_c parked (this design) **0.005 pN**; interface park (25 mm down + 18 out) 0.026; docs/13 Z-only 25 mm 0.055 — the
swing is 10× better. M_c1 up → other chamber 0.083 pN (unchanged, docs/13 §3.3.2). |B| at the WE relay: M_c1 parked
**1.9 mT**, M_c1 up 1.0, M_c2 up 0.7, M_d hold 0.04, M_w 0.06 mT → static during reads, but ≈ mT: relay with
mu-metal screen and an operate field ≫ 2 mT required (UNVERIFIED, open item). |B| at the pads: M_c1 up 7.9 mT,
M_d hold 5.1 mT (static, no induced signal). Forces: M_w on M_d at the bead-out stop **0.245 N** in +y (repulsive,
side-by-side), −0.065 N in z; at the hold 0.031 N → post (Ti Ø4 × 56, k = 23.6 N/mm) deflects **10 µm** — inside the
0.30 slot clearance; the Z spring (3 N) holds against −0.065 N. M_c1 up on the parked M_d: 0.024 N down. M_c1 up on
M_c2 parked: 0.005 N. Valve pins (lid) at V4 next to W1: |B| 0.10 T, ∇|B| 12 T/m → austenitic pin (χ 0.01) 5×10⁻⁵ N,
a ferromagnetic saturated pin 0.10 N (4 % of 2.5 N) → **UPPER: annealed austenitic or Ti pins**, docs/18 §12 note.
Steel near magnets: X-LSM stages ≥ 60 mm below M_d; M_c drives 50–60 mm from the parked magnet (force ≪ 0.01 N
[assessment]); datum pins zirconia.

**5.6 Motion budget vs docs/13 §7.1** (speeds `I.MAGNETS["M_d"]["speeds"]`; cam 0.5 s per stroke [assessment]):

| Step (window) | Needed | Window | Result |
|---|---|---|---|
| M_c up (30.0–30.1) | 5 s (spec ≤ 5 s) | 6 s | ✓ |
| M_c park (34.1–34.2) | 5 s | 6 s | ✓ |
| park → gather start lowered, 3 passes at 0.30, 2 lowered returns, 6 cam strokes (34.2–36.2) | 71 s | 120 s | ✓ |
| drag 23.41 at 0.20 + 2 gates (39.5–41.75) | 117.5 s | 135 s | ✓ |
| bead-out 4.55 at 0.20 + G4 open 0.06 s + M_d Z-down cam 0.5 s (56.75–57.15) (revised after review, docs/24 M7) | 23.3 s | 24 s | ✓ (0.7 s margin; Rev B wrote 1.2 s without the Z stroke; nothing slips past PE1 of run n+1, 2.45 min slack) |
| M_d down + transit to park | 2.8 s | 30 s | ✓ |

Repeatability < 3 µm (≤ 10 µm required); 0.05–5 mm/s inside 0.000029–26 mm/s; R 3 lane arcs followed by
PC-sequenced 0.5-mm chords (chord error 10 µm) unless Zaber coordinated streams are confirmed (UNVERIFIED). Quiet
windows (docs/13 §7.2): stage drivers disabled (non-back-driving lead screws hold), M_c worm self-locking, pogo
cylinder pressurised (no electrical actuation), M_d Z held up by its spring with the cam off contact.

**5.7 Pogo.** Linear spring between 0.50 N preload and 1.40 N at 1.27 mm: 1.21 N at the 1.0 mm working travel →
**7.25 N** for 6 pins (budget 9 N, press pad 12 N ✓). Wedge 2:1: cylinder ≥ 4.5 N horizontal for 7.25 N + 2 N
margin (bore 6 at 400 kPa gives 11.3 N (revised after review, docs/24 M3: the supply is 400 kPa since Rev B; at
300 kPa 8.5 N), UNVERIFIED friction). Shoulder bears on the plate underside with the
surplus; the die reaction goes through the press pad to the lid (docs/18 §7).

## 6. One-off CAD checks (method and results; `checks.json`)

| # | Check | Method | Result |
|---|---|---|---|
| 6.1 | Interference inside the lower assembly, 8 states | OCC boolean intersection of every solid pair (bbox pre-filter), tolerance 0.001 mm³; designed fits listed in `checks.ALLOWED` | **0 interferences** in all 8 states (`load`, `collect_IC1/IC2`, `gather_IC1`, `gather_IC1_low`, `drag_mid_IC1`, `hold_RC`, `beadout_end`); with the card envelope only the 11 gaskets (0.12 compression, by design) and the pogo tips (by design) touch it |
| 6.2 | M_d swept volume: holder + magnet + neck + post + Z unit + umbrella vs every static part, both M_c parked | 14 paths (drag IC1/IC2, 3 gather passes × 2, bead-out, 5 lowered transits), ≈ 60 samples each, up/lowered as used | **0 collisions** on all 14 paths (incl. the 0.30 slot clearance, M_c units parked, electrode bay, P_s boss 0.45 from the post at the bead-out stop, tubes, M_c carriers ≥ 1.4 above/beside the Z unit) |
| 6.2b (revised after review) | M_d post vs the anvil under the plate | same sweep | with the Rev C 3.4 slot the through-slot no longer carved the P_a2 boss and the post (Ø4) hit it on the WL1 arc (9 samples, ≤ 1.0 mm³); Rev B had **zero clearance** there (0.003 mm³, below the tolerance). Fix: the bottom pocket also clears every M_d up-path by r 2.3 (post + 0.3); wall to the P_a2 insert bore 0.63 → re-run: see `checks.json` md_sweep |
| 6.3 | Holder plan clearance in the plate openings | shapely, Ø2.6 round holder (Rev C; Rev B 2.6 sq) at 0.25-mm steps | drag ≥ **0.34**, gather 0.90, bead-out 0.30 (interface slot alone: **0.03** at the J fillet, 0.16 on the 45° arcs, corners outside the round end cap → DEV-L4) |
| 6.4 | Tube bend radii | circumradius of consecutive route points | all 11 routes **25.0** (≥ 25, MTC rule) |
| 6.5 | Valve tips vs anvil-top features | shapely: tip edge to openings, M_w recess, gasket seats, cold-zone seams | anvil/cold class min: V15 **0.25** (accepted, CHOICE-5), V3 → P_byp seat **0.36** (≥ 0.3 face-seal rule, < 0.5 generic, ICR-7), V16 0.50, others ≥ 0.5; slot-class tips inside the slot (as docs/18 §11) |
| 6.6 | Service: can the anvil be removed? (revised at integration: latch brackets belong to the anvil module; re-run 0 hits) | anvil module translated +5 … +120 mm in z (state `load`) against the bay frame and M_d system | first run: fan + duct hit the SW beam at 5–40 mm → fan/duct moved to x ≥ −4, beam ends at x −5; **re-run: 0 hits at 5, 10, 20, 40, 60, 90, 120 mm** (prerequisites: card out, M_c parked, M_d parked lowered, tube unions outside the walls opened, Gamry cable unplugged at the bulkhead, heater/sensor/fan/cylinder connectors and the purge line unplugged) |
| 6.7 | Port insert replacement | by construction | gasket: from the top, card out, no tools beyond tweezers. Insert: lift the anvil module (6.6), unscrew the retainer (2 × M2), push the insert down; insert + bonded tube + wall union are one spare "port line" (11 spares) |

## 7. Choices (open points decided here; the user may overrule)

| # | Open point | Chosen | Why | Alternative |
|---|---|---|---|---|
| CHOICE-L1 | anvil outline, material, finish | one Al plate x −12…90 / y −16…66; cast tooling plate, hard-anodised, top lapped with the cold block | non-magnetic, stable after pocketing, insulating top | Ti plate (stiffer, costlier); ceramic |
| CHOICE-L2 | nest construction | separate 5-mm frame on the anvil holds pins, pushers, sensor, bushes; card + 1.8 opening with lead-in | vertical drop, frame never touches the foil; gutter visible | pins pressed into the anvil |
| CHOICE-L3 | pocket / thick-zone layout | one bottom pocket x 32.5–62.5, y 0–50, bosses for island, P_a2, P_s | M_c flange, M_d sweep and electrode bay share one 5-mm plate | separate pockets per window |
| CHOICE-L4 (revised after review) | cold zone | cold block x 2.6–20 / y 3–47 behind a 2-mm gap with a 1.5-mm PEEK lip over foam, 4 PEEK pads; TEC 07111-5L31-03CL under a 3.2-mm spreader; 24 × 73 sink with the 25-mm fan at its −y end + front duct; required R_th ≤ 1.6 K/W | corrected heat budget §5.4 (Rev B: PEEK U-frame, 12711 module, leak 7.1 W) | heat pipe to a front/rear sink; thicker gaps (cold plate under RCj shrinks) |
| CHOICE-L5 | port inserts, gasket | insert from below, retainer plates, 50 ShA gasket | gasket swap from the top; seal force ≤ budget | 6-32 fittings (pitch) |
| CHOICE-L6 | head guide pins | Ø6 pins at (−8, 46) and (84, 4) (revised at integration, interface `HEAD_GUIDE_PINS`; was (−7, 46)/(83, 4) with a 0.2-mm wall to the nest opening and 0 mm to the anvil edge), bronze bushes in anvil + frame | diagonal = best rotational location; outside card, ports, pushers | 3 pins |
| CHOICE-L7 | drips | perimeter gutter 1.5 × 1 with drains at both front corners → BASE drip tray; umbrella on the Z unit | spills never reach the magnet bay stage | drip pan |
| CHOICE-L8 | anvil heating | 4 polyimide foil heaters under the thick frame, PID on thermistors at W1 and the RC | no heater near openings | cartridge heaters |
| CHOICE-L9 | datum pins | zirconia, held in the frame, 0.2 above the anvil (gutter passes under) | non-magnetic, hard, insulating | hardened steel (magnetic) |
| CHOICE-L10 | M_c gap | holder flange seats on the plate underside (preload 6 N) | gap by two machined dimensions, not by an actuator | actuator end stop |
| CHOICE-L11 | M_d stage | 2 × X-LSM050A X on Y, cam Z unit, up-stop screw | sourced repeatability/speeds; spring-up Z per CHOICE-6 | custom XY |
| CHOICE-L12 | lowered transits | park → (44, 30/20) → gather start; bead-out → (57.85, 25) → J | via J, away from the electrode bay and the incubating chamber (docs/13 §2.2) | — |
| CHOICE-L13 | drip umbrella | 20 × 20 PEEK on the Z unit | protects the stage | bellows |
| CHOICE-L14 | tube routing | vertical drop to z −30…−37, R 25 bend, staggered levels, west lines under the heat sink to wall W, east to wall E, P_a2 north then east | only route that keeps R ≥ 25 and stays out of the M_d sweep | moulded manifold (series) |
| CHOICE-L15 | bay frame | walls outside the stage sweep, 4 beams, anvil module on dowels, U-slots | anvil removable as one module | posts (collide with the X stage) |
| CHOICE-L16 | pogo lift | PEEK block, nose + 2 pins, 2:1 wedge, pneumatic cylinder outside the box, shoulder stop on the plate | no coil/motor in the bay; no lateral motion; fail = down | solenoid in the bay |
| CHOICE-L17 | bay contents | relay low in the bay, RH/T on the W wall, leak PCB + Ø2 drain in the floor, gland E wall z −45 | short leads, Faraday box, leak detection local | relay outside the bay |
| CHOICE-L18 | M_c drive | stepper + self-locking worm on the upper link shaft, optical flag switches UP/PARK | compact, holds without power, 45° in 5 s | L12 linear (82 mm body does not fit), pneumatic (fail-state ordering) |
| CHOICE-L19 | condensation | foam + dry-air purge (pilot air via a restrictor, dew point UNVERIFIED) + RH/T in the nest W wall; Peltier enabled only with card present and lid closed | the plate is always below the lab dew point | desiccant cartridge |

## 8. Deviations from docs/13 Rev B or docs/18

| # | What | Change | Effect |
|---|---|---|---|
| DEV-L1 | M_c "spring-up (on)" (docs/13 §3.3.1, docs/18 §7) | fail state = **hold** (self-locking worm) | a spring return would drive M_c into the M_d post while M_d gathers/holds/drags from the window (34.2–39.5); beads are held by whichever magnet is engaged at a power loss |
| DEV-L2 | M_c "Z down 25, then retract ±y 18" (docs/18 DEV-4) | **parallelogram swing R 64.5**; drift while in the window ≤ 0.19 (< 0.40 holder clearance); parked (40, 56.7)/(40, −6.7), top z −45.6 | lower field at the own chamber (0.005 vs 0.055 pN); only one actuator per unit |
| DEV-L3 | thick zones (`I.ANVIL_THICK_ZONES`) | island boss to x 40.5 (P_b bore wall 0.35 → 1.35); P_s boss x 60.3–62.5, y 17.8–23.2; west strip x 32.5 at the windows | inserts fully supported; M_c flange clears |
| DEV-L4 (superseded after review by interface DEV-IF-C2: round Ø2.6 holder, Ø2 × 4 magnet, arms 3.4, every slot-valve span 3.40) | drag slot (`I.SLOT_*`) | Rev B: slot ∪ swept 2.6-sq holder + 0.30; max local width 4.44 at G1/G2 | holder clearance ≥ 0.30 everywhere; foil span under G1/G2 19 µm at 1.5 N (docs/13 15 µm) |
| DEV-L5 | pogo tips retracted z −1.0 (`I.POGO`) | **−1.66** (lift 3.0 kept) | otherwise 1.66 compression > 1.27 full travel of the class probe |
| DEV-L6 | LOWER sub-claims (`I.LOWER_SUBCLAIMS_CARD`) and west/east pass-throughs | M_d stage z −126…−62; M_c units y −55…106, z to −77; tubes leave through wall W (card x −40) at z −56…−62 and wall E (x 130) at z −55…−58 | internal to DOCK LOWER except the wall exits (ICR-6) |

## 9. Interface change requests (interface.py / docs/18 not edited)

(revised at integration) All resolved in interface.py Revision B (docs/18 §15): ICR-1 → `HEAD_GUIDE_PINS` (−8, 46)/
(84, 4), bush top `NEST_FRAME_TOP_Z` 5.0; ICR-2 → `slot_polygon()` (widened slot adopted); ICR-3 → `POGO
tip_z_retracted` −1.66; ICR-4 → `MAGNETS` M_c swing, parks, fail = hold; ICR-5 → `ANVIL_THICK_ZONES`; ICR-6 →
`LIQUID_LINE_EXITS`, `PASS_THROUGHS` (cable window, Peltier exhaust: BASE adds a duct extension + louvre); ICR-7 →
`VALVE_TIP_SEAT_MARGIN` 0.3 / `VALVE_TIP_EDGE_MARGIN` 0.5; ICR-8 → `MATERIALS`; ICR-9 → nest top 5.0 confirmed.

| ICR | Name | Current | Needed | Why |
|---|---|---|---|---|
| ICR-1 | new `HEAD_GUIDE_PINS` | absent | Ø6 at card (−7, 46) and (83, 4); bush top z 5.0; pin tip ≥ 1.0 above the anvil when the head is down | UPPER and LOWER must share them (docs/18 §8 names them, no position) |
| ICR-2 | `SLOT_W`, `SLOT_W_WLC`, `SLOT_W_BEADOUT`, `SLOT_CENTERLINES` | round-capped buffers 4.0 / 3.4 | slot = buffers ∪ swept 2.6-sq holder + 0.30 (`dock_lower.geom.slot_poly`) or a round holder | 0.03 mm clearance at J; corners outside the bead-out end cap |
| ICR-3 | `POGO["tip_z_retracted"]` | −1.0 | −1.66 (or `block_lift_stroke` 2.34) | lift 3.0 − 1.34 free tip = 1.66 compression > 1.27 full travel |
| ICR-4 | `MAGNETS["M_c1"/"M_c2"]` motion, `parked_xy`, `z_top_down` | Z 25 + y 18, (40, 56)/(40, −6), −25.16, "spring returns to UP" | swing R 64.5, (40, 56.7)/(40, −6.7), top −45.6, fail = hold | DEV-L1/L2 |
| ICR-5 | `ANVIL_THICK_ZONES` | island x ≤ 39.5; no P_s boss; west strip to 33.5 | as DEV-L3 | insert bore walls; M_c flange |
| ICR-6 | `PASS_THROUGHS["liquid_lines_west"/"east"]`, `LOWER_SUBCLAIMS_CARD` | points (22, 25, −60), (75, 25, −60) | west lines exit dock X 150, Y 84–116, Z 108–114; east lines dock X 320, Y 80.5/95.5/110.5/161.5, Z 112–115; Peltier exhaust duct outlet at dock Y 20, X 186–210, Z 118–144 (10.6 W) | BASE must take the lines and the exhaust there |
| ICR-7 | `VALVE_TIP_EDGE_MARGIN` vs `FACE_SEAL` | 0.5 "any opening/gasket" vs 0.3 "outside a seat" | state which governs; V3 → P_byp seat is 0.36 | geometry from interface |
| ICR-8 | `DATUM_PIN` comment "hardened steel" / `MATERIALS["pins"]` | steel | datum pins zirconia; valve pins annealed austenitic or Ti (UPPER) | magnet bay field 0.1 T at V4 |
| ICR-9 | docs/18 §8 `LOWER_nest_anvil` "anvil … up to z = card top only outside the card" | — | confirm nest frame top 5.0 and M_c bracket stubs below z −15 | lid sweep min Z 175.3 (z 5.3) |

## 10. Series-dock notes (C3 and later)

Replace the two X-LSM stages and adapter by a compact custom XY (two small lead-screw or linear-motor axes, ≈ 60 % of
the height); cast the anvil + nest frame as one machined casting with lapped top; mould the 11 inserts as a PEEK
manifold plate with short moulded channels to two multi-line connectors (removes the 25-mm bend constraint and the
corridor congestion); integrate the M_c swing into the casting with one geared motor per unit; replace the pogo wedge
and cylinder by a lid-driven cam (head descent lifts the block); stamped shield can + flex PCB for the electrode bay;
one 30 × 30 Peltier on a heat pipe to a rear heat sink (no front duct).

## 11. Open items / UNVERIFIED

(revised after review) Heat-sink R_th ≤ 1.6 K/W (first-article test), foam/lip conductivities, cold-block pull-down
time; M_d Ø2 × 4 magnet part and its drag/hold force (0.96× Derived; M1); M4 slot variant at 3.4 mm; pogo spring
material (M12); Q-10-10-05-N grade on the order (M13). Stage footprint and coordinated-path capability; M_c drive, Z gearmotor, pogo cylinder, relay (operate field vs
1.9 mT at the relay), RH/T sensors, heat sink/fan, heaters, pushers, presence sensor, zirconia pins (all
UNVERIFIED parts); probe length/tip style; gasket modulus and HQ/Tween compatibility; PEEK/COC/foam conductivities;
Roark coefficients; B_r and bead moment (docs/13); M_d gap at 5 positions (shim); bead hand-over to BW against the
0.245-N M_w/M_d interaction (DEV-5 M1 test); anodise thickness effect on the 5.000 plate; dry-air dew point.
(revised at integration) The interference with the REAL card was run in docs/23 §4: pogo tips land on the six pads
through the real contact window, gaskets compress only the foil around the real port holes, datum pins and pushers
touch the real L3 edges, the corner block clears the chamfer by 0.3; no unintended contact in any magnet state.

## 12. Sources opened this session (2026-11-13)

* Zaber X-LSM050A specs: https://www.zaber.com/products/linear-stages/X-LSM/specs?part=X-LSM050A ; X-LSM series:
  https://www.zaber.com/products/linear-stages/X-LSM ; XY systems: https://www.zaber.com/products/xy-xyz-gantry-systems/X-XY-LSM
* Firgelli/Actuonix L12 datasheet: https://cdn.robotshop.com/media/f/fir/rb-fir-25/pdf/l12_datasheet.pdf
* supermagnete Q-10-10-05-N: https://www.supermagnete.de/eng/block-magnets-neodymium/block-magnet-10mm-10mm-5mm_Q-10-10-05-N
* PTR Hartmann series 1007.70: https://ptr.ptr-hartmann.com/en/testing-technology/test-probes/standard-test-probes/series-100770/
* Custom Thermoelectric 12711-5L31-04CL: https://customthermoelectric.com/media/wysiwyg/TEC_spec_sheets/12711-5L31-04CL_spec_sht.pdf (Rev B part)
* (revised after review) Custom Thermoelectric 07111-5L31-03CL spec sheet: https://customthermoelectric.com/media/wysiwyg/TEC_spec_sheets/07111-5L31-03CL_spec_sht.pdf
* MTC/MicroSolv PEEK bend radius: https://www.mtc-usa.com/kb-article/bend-radius-for-tubing
* Not reachable: Actuonix product page (403), Pickering low-leakage page (403), GlobalSpec Zaber datasheet (403),
  Edmund Optics stage pages (403), dajiqun Zaber PDF (503). Search snippets only (not used as sources): SMC CJ2/CJP2
  dimensions, Pickering > 1e13 Ω.
