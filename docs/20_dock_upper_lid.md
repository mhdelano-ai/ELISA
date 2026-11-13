# 20 — Dock upper part (lid and head) for cartridge A, C2 prototype

Status: 2026-11-13, **stage C0 desk work**, physical design round, DOCK UPPER (complete for this round). Inputs: docs/18 (binding),
`cad/elisa_cad/interface.py`, docs/13 Rev B §2.1, §2.7, §4, §6, §7.2; docs/11 §3, §5; docs/16 §2–§3, §6.4. Nothing
is ordered. This document changes no other document. CAD: `cad/elisa_cad/dock_upper/` (regenerate with
`cd cad && python -m elisa_cad.dock_upper.build`, ≈ 3 min; `--fast` skips STEP/PNG, ≈ 1.5 min); outputs
`cad/out/dock_upper/` (STEP, PNG, `calcs.txt`, `checks.txt` — every number in §4–§5 is printed there).

Source tags as in docs/18: docs section | `interface.NAME` | **Derived** (arithmetic shown or in `calcs.py`) |
**CHOICE-Un** (§6) | **DEV-Un** (§7) | **UNVERIFIED** | [assessment] | vendor document opened this session (§12).
Units mm, N, kPa, °C. Coordinates: CARD (z = 0 foil underside) for the head, DOCK for the lid frame;
P_dock = P_card + (190, 75, 170) (`interface.CARD_ORIGIN_IN_DOCK`).

## 1. Summary

* **Head** (moves 8 mm vertically inside the lid frame): Al heater block 10 mm (assay zone, 25.0 °C) with two
  bearing-bronze guide plates, PEEK pressure plate (reagent zone), 4 mm open break between them; 21 spring-closed pins
  (Ø0.8 / Ø1.2) with collars, coil springs and bonded buttons; a stainless spring plate; 21 yoke blades on two tiers;
  a four-layer Al cylinder block with **21 Ø6 single-acting cylinders** on the 9 mm grid of `interface.CYLINDERS`,
  single-layer air galleries, piston marker magnets read by 21 linear Hall ICs; a bridge carrying the cam thrust
  units, four guide posts and two SMC S070 pilot-valve manifolds (21 stations); two Ø6 guide pins into the nest;
  die-back press pad 12 N; two gas rings (P_c, P_mv); three vent pockets; two foil heaters, two Pt100.
* **Lid frame** (hinged): two side plates on a rear hinge (axis `interface.LID_HINGE_AXIS`, 85° stop on fixed
  blocks), front/rear beams, four post bearing blocks, eccentric cam shaft (e 4.5, stroke 9 = 8 drop + 1 spring
  overtravel) with a right-hand lever, two Kipp K0045 draw latches at the front, grounded Al cover, handle,
  latched switch, umbilical clamp at the docs/18 pass-through.
* **Key results** (`calcs.txt`, `checks.txt`): TPE closing force 1.03–1.37 N (slot, limit 1.5) and 2.20–2.80 N
  (others, limit 3.0) with ±10 % springs and guide friction; V3 closes with 1.94–2.66 N through a force-limiting
  spring; cylinder margin (force / need incl. friction) **≥ 1.60 at 400 kPa** (1.20 at 300 kPa → DEV-U1/U2);
  open ≈ 22–24 ms, close ≈ 59 ms incl. 3 ms valve response (≤ 0.2 s required); air 0.36 NmL per actuation,
  ≈ 0.1 NL/day; pilot heat 1.1 W average, 3 W peak, on the head bridge 30 mm above the heater block (0.05 W reaches
  it); head force 280 N (265–295), card-face clamp 213 N (≥ 198) vs ≥ 165 N required; heater 7.3 W max vs 0.56 W
  worst-case loss, in-plane gradient 0.04 K, warm-up ≈ 70 s (block), card ≈ 10 min (docs/13 §6.5).
* **Checks**: closed and head-raised assemblies (251 solids incl. the card envelope) have **0 unintended
  interferences**; lid sweep 0–85° stays inside the docs/18 sweep box and touches no other claim except the
  intended ICR items (§8); loading-path box clear at 85°; pin tips ≥ 1.75 mm above the card while the lid closes;
  guide pins engage 1.26 mm (air on) / 0.25 mm (air off) before any pin reaches a bore lead-in.
* **Deviations**: pilot pressure 400 kPa and Ø6 bores instead of 300 kPa / Ø5 (DEV-U1, DEV-U2); head force
  280 N > 250 N design value (DEV-U3); "hardened" guides replaced by bearing bronze (DEV-U4). **Interface change
  requests** ICR-U1…U5 (§8): nest bushes for the guide pins, latch catch plates, hinge rail, clamp design force,
  PLUNGER constants.

## 2. Assembly description

### 2.1 Configurations (CAD: `assy.configuration()`)

| Config | Lid | Head | Valves | STEP |
|---|---|---|---|---|
| closed | closed, latches drawn, cam at BDC (lever forward) | down: face on the card top (dock Z 176.215) | de-energised (all closed, V3 open) | `lid_assembly_closed.step` |
| raised | closed, cam at TDC (lever back) | up 8 mm (face at Z 184.215) | no card: pins at the 0.2 drop stop | `lid_assembly_raised.step` |
| open | 85° on the stop | raised | as raised | `lid_assembly_open.step` |

Operating sequence: (1) lid open, card lowered into the nest (docs/18 §2). (2) Controller energises the 20 pull
valves (pins lifted, "docking state") while the latched switch reads open. (3) Operator closes the lid (head raised,
pin tips ≥ 1.75 above the card on the whole arc), closes the two draw latches, turns the lever 180° forward: the head
descends 8 mm on the four posts; the guide pins enter the nest bushes 1.26 mm before the first pin reaches a bore
lead-in; the head lands on the card and the clamp springs take the last 1.0 mm. (4) Latched switch closes → the
controller releases the pull valves in sequence (springs close every valve), runs the docking checks (docs/13 §8.1).
Opening is the reverse; the lever cannot be turned back while the controller holds a run (software interlock;
mechanical lock = series item).

### 2.2 Head stack (card z, head down)

| z | Item | Notes |
|---|---|---|
| 6.215–16.215 | heater block (x 24–75.5) / PEEK plate (x 0–20) | `interface.HEAD_Z` heater_block; break x 20–24 open |
| 6.215–9.215 | lower guide plate CuSn8 (inset) | hull of all assay pins + 2.0, reamed H7 holes |
| 14.215–16.215 | upper guide plate CuSn8 (inset) | two-point guidance, span 7 mm |
| 16.215–29.3 | heater fins y 0–2 and 48–50 | one 12.7 × 50.8 foil heater on each outer face |
| 16.415–16.915 | pin collars (closed) | land on the block top at 0.2 below closed (no card) = `PLUNGER` extension limit |
| 16.915–24.5 | pin springs (L 7.585 closed) | `HEAD_Z` pin_spring_zone |
| 24.5–26.0 | spring plate 1.4301, 1.5 | reacts all springs; V3 open stop and V3 button lower stop |
| 27–31 / 32–36 | yoke tiers 0 / 1 | `HEAD_Z`; eye 1.5 thick at the bottom of the tier |
| 28.7–29.5 / 33.7–34.5 | pin buttons tier 0 / 1 (closed) | 0.2 above the eye (hook gap); +0.8 when open |
| 37–68 | cylinder block: cover 37–38, air plate 38–44, bore block 44–62, cap 62–68 | `HEAD_Z` cylinder_block 38–68 (+1 mm cover) |
| 68.5–70.1 | Hall PCB with 21 DRV5055 (SOT-23) | under the bridge window |
| 71–79 | bridge (+ manifold shelf y 50–102) | spacers 68–71 at the block corners |
| 79–92 | thrust units at x −17 / 92.5, y 25 | follower top dock Z 262 (latched) |

Plan of cylinders and yokes: `plan_cylinders_yokes.png`; air galleries: `plan_air_galleries.png`; underside:
`head_underside.png` (+ zoom on the J/cell cluster).

### 2.3 Valve pin, spring, yoke and cylinder (one channel)

* **Pin** (custom, Swiss-turned non-magnetic stainless, e.g. 1.4404 or Nitronic 60 [assessment]): flat tip land
  Ø1.0 on Ø1.2 pins (0.1 × 45° step), Ø0.8 flat on Ø0.8 pins, edges broken 0.05 (`PLUNGER` tip_edge_chamfer);
  shank ground g5-class (−2…−6 µm) in H7 guide holes (0…+6 µm): radial play 1–6 µm [assessment]; collar Ø1.4 / Ø2.0
  × 0.5; neck Ø0.5 / Ø0.8; button = hypotube sleeve Ø1.3/Ø1.8 × 0.8, **bonded (Loctite-class anaerobic) or
  laser-welded after assembly with a 0.20 mm feeler gauge** between eye and button (sets the hook gap) (CHOICE-U6).
* **Retention with the lid open**: the collar cannot pass the Ø0.8/1.2 guide hole (pin cannot fall out); the spring
  pushes the collar onto the block top 0.2 below "closed" (`PLUNGER` pin_extension_limit, collar stop); the button
  then rests on the eye (gap 0) — so with no card the yoke is also at its stop. Pins are removable only after the
  yoke is slid off (fork open away from the rod) and the button removed.
* **Spring** (custom-wound 1.4310, ground ends; catalogue sizes not found this session → UNVERIFIED part, spec here):

| Class | wire d / mean D / n | k (N/mm) | F closed (±10 %) | F open (+0.8) | L free / closed / solid | τ at F_open max | OD |
|---|---|---|---|---|---|---|---|
| slot (G1–G4, V11, V12) | 0.20 / 1.10 / 24 | 0.438 | 1.20 (1.08–1.32) | 1.55 | 10.32 / 7.59 / 5.20 | 764 MPa | 1.30 |
| anvil Ø0.8 (V14, V15) | 0.25 / 1.05 / 22 | 1.342 | 2.50 (2.25–2.75) | 3.57 | 9.45 / 7.59 / 6.00 | 929 MPa | 1.30 |
| anvil/cold Ø1.2 | 0.30 / 1.55 / 18 | 1.057 | 2.50 (2.25–2.75) | 3.35 | 9.95 / 7.59 / 6.00 | 699 MPa | 1.85 |
| V3 open spring | 0.20 / 1.55 / 10 | — | 0.5 up | — | below the collar | low | 1.75 |

  k = G d⁴/(8 D³ n), G 70 GPa (UNVERIFIED handbook value); τ with the Wahl factor. τ/R_m ≈ 0.3–0.45 for 1.4310 wire
  of R_m ≈ 2000–2500 MPa at these diameters (UNVERIFIED) — acceptable for ≈ 10⁴ cycles/year per valve (16 runs/day,
  docs/13 §4), fatigue to be confirmed on the M4 rig. Preload set per pin by shim washers (0.05 steps) under the
  spring plate [assessment]. Card-stack tolerance ±0.06 changes F by 0.03–0.08 N (Derived k × 0.06).
* **Yoke** (laser-cut 1.4310 sheet 1.0, CHOICE-U8): boss Ø3 at the rod, full-height web (4.0) stopping 0.3 short of
  the button, 1.5-thick tongue to an eye (Ø1.5 / Ø1.8) with a fork slot 0.7 / 1.0 open away from the rod. Two
  **J-yokes** where the rod is too close to the pin for a web (V1 L 2.74, V9 L 0.71): tongue under the button, a post
  3 mm behind the rod, a top tab under the rod (tab up to tier top + 1.0). **V3 push yoke**: whole blade at z 28–31
  above its button (the eye pushes the button down).
* **Cylinder** (custom block, CHOICE-U10): Ø6 bore (DEV-U2), piston 2.5 thick with one O-ring (catalogue O-ring
  ~Ø4 × 1 class, part UNVERIFIED), NdFeB marker Ø2 × 1 in the piston top, return spring 0.5 N in the vented upper
  chamber, rod Ø1.5 ground stainless through a bronze bush and a rod seal in the air plate. **Pull cylinders**: air
  under the piston (annulus 26.5 mm²) lifts the yoke 1.0 = hook gap 0.2 + pin stroke 0.8 to a hard stop at the cap.
  **V3**: air above the piston (28.3 mm²) pushes the rod down 1.0 and compresses the 2.1 N / 1.0 N/mm force-limiting
  spring inside the piston by 1.0 (piston stroke 2.0).

### 2.4 Inverted V3 (fail-open), CHOICE-U7

Rest (no air): open spring 0.5 N lifts the pin until the collar touches the spring-plate underside (open stop, tip
z 1.015). Closing: air pushes the piston down 2.0; the rod/eye moves 1.0 (0.2 gap + 0.8 pin travel), the tip lands on
the TPE, the remaining 1.0 compresses the limit spring to 3.1 N → TPE force 3.1 − 0.58 (open spring at closed) −
0.05 = 2.47 N (1.94–2.66 with ±10 % spring tolerance and friction sign; limit 3.0). No card: the V3 button lands on
the spring-plate top 0.2 below "closed". Air or power lost → piston vents → open spring lifts the pin → V3 open.

### 2.5 Air distribution and pilot valves (CHOICE-U9)

* Pilot valves: **SMC S070B-5DG** (3-port N.C. poppet, base mounted, 24 VDC, **0.5 W coil, max 0.5 MPa**, C 0.042
  dm³/(s·bar), Cv 0.011, response ON/OFF ≤ 3 ms at 0.5 MPa, proof 1 MPa, 7 mm width, 5 g) on two **SS073B01** bar
  bases (11 + 10 stations; pitch 7.2, L1 = n × 7.2 + 14.8 = 94.0 / 86.8 mm; max 20 stations per base), all from the
  SMC S070 catalogue (opened, §12). Envelope modelled 7 × 25.5 × 28.5 per station (overall sizes read from the
  catalogue drawing; interpretation UNVERIFIED). The 0.35 W coil is rated 0.3 MPa only → the 0.5 W "D" option is
  required at 400 kPa. Exhaust R port to the lid interior (vented cover).
* Valve OUT barbs → 21 PU tubes Ø3.18/2 (catalogue port size "32") → gallery headers on the rear (18 channels) and
  right (3 channels, column x 68) faces of the air plate.
* Galleries: one layer, 0.6 × 0.6 grooves in the air-plate underside sealed by the 1-mm cover with a laser-cut
  gasket; via Ø0.8 into each annulus at r 1.9 (V3: via outside its bore, vertical passage to a cap groove above the
  V3 piston). Routing rule: lanes between cylinder columns, the cylinder farthest from the exit gets the outermost
  slot (no crossings). Checked (shapely): groove–groove web ≥ 0.50, groove–rod hole ≥ 0.40, groove–other via ≥ 1.5,
  groove–screw/ear ≥ 2.7; longest gallery 50 mm.
* One **Ø0.15 orifice per channel** in the header (laser-drilled jewel or disc, part UNVERIFIED) sets both speeds and
  makes the closing approach of the pin follow the eye down (the pin rides on the eye until it lands on the TPE) →
  limits the closing transient of docs/13 §4 (≤ 5 kPa in the sealed cell; its value vs speed is for M4).
* Supply: one air line in the umbilical from the BASE regulator (`SPACE_CLAIMS BASE_rear_low`), 400 kPa set,
  **pressure switch on the lid manifold, trip 350 kPa** → fault latch (docs/08 sequencer) [assessment].

### 2.6 Position feedback (docs/13 §6.2), CHOICE-U11

Per cylinder: NdFeB Ø2 × 1 marker in the piston, **TI DRV5055** ratiometric linear Hall IC (SOT-23, 3.3/5 V,
20 kHz, A-variants with magnet drift compensation; ti.com product page opened) on a PCB on the cap, 21 analog
channels on two 16-ch ADCs (part to be selected). Measures piston = yoke position (pull 1.0 / V3 2.0 mm stroke)
→ detects: valve not opened (pressure missing, piston stuck), yoke not returned (would leave a pin open), V3 not
closed. Does **not** see a pin stuck in its guide with the yoke returned — that case is covered by the docking leak
test and the per-run pressure signatures (docs/13 §8.1). Rejected: per-yoke optical forks (21 × ~5 mm bodies do not
fit the 9-mm grid with the rods), pressure switches only (do not see mechanics). Hall ICs are DC devices, polled
on a low-level bus — allowed during read windows (docs/13 §7.2); marker field at the beads (≥ 60 mm away) negligible
[assessment].

### 2.7 Clamp, cam, latches, hinge (CHOICE-U12…U14)

* Load path: lever → cam shaft Ø10 in the side plates → two eccentrics (R 10, e 4.5, x −17 / 92.5, y 25, dock Z
  276.5) → follower caps → **clamp springs** (per side preload 135 N, rate 15 N/mm, OD 14, die-spring class, part
  UNVERIFIED) → thrust housings → bridge → spacers → cylinder block → PEEK standoffs (4 + 2) → heater block / PEEK
  plate → card. The eccentric's bottom dead centre is self-locking (force through the shaft axis).
* Reactions: lid frame up at Y 100 → hinge (rear) and two front **Kipp K0045.1541092** draw latches (stainless, form
  A, retaining force F1 2000 N; catalogue page opened; length 109; width/height of the drawing not unambiguously
  readable → envelope 26 × 21 × 109 UNVERIFIED). Catch plates K0045.9143372 belong on the LOWER nest front (ICR-U2).
* Hinge: two fixed blocks (X 150–153.8, 316.2–320, Y 185–200) with a Ø6 pin through the side-plate knuckles (r 5),
  flanged plain bushes (iglidur class, part UNVERIFIED), **85° stop faces** on the fixed blocks; the blocks bolt to
  a hinge rail provided by DOCK BASE in the unclaimed volume Y 185–200, Z 155–176 (ICR-U3).
* Lid mass 2.32 kg (CAD volumes × densities; envelopes at assessed densities), CoM dock (233, 113, 236): closing
  torque 1.88 N·m at 0°, 0 at ≈ 60°, −0.89 N·m at 85° (lid rests on the stop) → **no gas strut**; lift force at the
  handle 12 N. A rotary damper on the hinge is optional (series note).

## 3. Parts list

### 3.1 Custom parts (STEP in `cad/out/dock_upper/parts/`, dock coords, closed configuration)

| Part (file) | Material | Key dimensions | Critical tolerances | How made |
|---|---|---|---|---|
| heater_block | Al 6061-T6 | 51.5 × 50 × 10 + fins 2 × 50.8 × 13.1; pockets for guide plates 3 / 2 deep | face flatness 0.01 lapped together with the PEEK plate on the assembled head; hole positions ±0.01 | CNC, then lap |
| guide_plate_lower / _upper | CuSn8 (bearing bronze) | hull of the pin pattern + 2.0, t 3 / 2 | holes Ø0.8 / Ø1.2 **H7**, position ±0.005 (jig grind/ream as a pair, doweled) | CNC + jig bore/ream |
| peek_plate | PEEK (unfilled) | 20 × 50 × 10; gas grooves OD 7.1 / ID 4.9 × 0.75 | face coplanar with the heater block ±0.01 | CNC |
| V8_bush | CuSn8 | Ø3 × 8.7 (starts 1.5 above the face) | Ø1.2 H7 | turned |
| pin_family (21) | 1.4404 / Nitronic 60 | Ø0.8 or Ø1.2 × ≈ 30–36 | shank g5, tip land square to axis 0.005, length ±0.01 | Swiss turn + centreless grind |
| button_family (21) | stainless hypotube | Ø1.3 or 1.8 × 0.8 | bonded at gauge 0.20 | cut tube |
| spring_plate | 1.4301, 1.5 | 75 × 44 | flatness 0.02 | laser + grind |
| standoff_family | PEEK | Ø6, two lengths | length ±0.01 (pairs ground) | turned |
| yoke_family (21) | 1.4310 sheet 1.0 | per channel, 0.7–10.9 offset | eye-to-boss distance ±0.02; tongue thickness 1.5 ±0.02 | laser/wire-EDM, J-yokes brazed |
| rod_family (21) | 1.4305 ground Ø1.5 | 13–21 long | g6 | cut + grind |
| piston_family (21) | POM-C (or Al) | Ø5.95 × 2.5, O-ring groove | O-ring groove per O-ring maker | turned |
| cyl_block_cover / air_plate / bore_block / cap | Al 6061 | 95.5 × 50 × 1 / 6 / 18 / 6 | bores Ø6 H8 Ra 0.4 honed; gallery grooves 0.6 ± 0.02 | CNC; gasket between cover and air plate |
| gallery_header_rear / _right | Al 6061 | 55 × 6 × 7 / 6 × 24 × 7 | — | CNC, orifices pressed |
| guide_ear_family + guide_pin_family | Al / 1.2842 hardened, Ø6 h6 | ear 8 × 8 × 29; pin protrudes 9.5 | pin position ±0.01 vs the guide-plate holes (doweled) | CNC + ground pin |
| press_pad_stem_foot + silicone | 1.4305 stem Ø4 + Al foot 5 × 3.5 × 2; silicone 40 ShA 1.0 | stem guided in the heater block | stem Ø4 g6 | turned; silicone bonded |
| bridge, bridge_spacers | Al 6082 | 129.5 × 50 × 8, shelf 98 × 52 × 4 | spacer heights ±0.02 | CNC |
| guide_post_family (4) | 1.4305 Ø8 h6 | ≈ 37 | — | ground bar |
| thrust_housing / thrust_cap | Al / 1.4305 | Ø19 / Ø16.8 | — | turned |
| lid_side_plate_L/R | Al 6082, 8 | 138 × 109, knuckle r 5 | hinge bore and shaft bore ±0.02 (machined as a pair) | CNC |
| lid_front_beam, lid_rear_beam, lid_post_block (4) | Al 6082 | — | post bores ±0.02 to each other | CNC |
| cover | Al 5754, 1.5 | 163.5 × 141 × 117 | — | sheet metal, grounded by a strap |
| cam_shaft, cam_eccentrics, cam_lever | 1.4305 / 1.2842 | Ø10 × 166; R 10, e 4.5; lever 60 | e ±0.02 | turned/ground |
| hinge_block_L/R, hinge_pin_D6 | Al / 1.4305 | 3.8 × 15 × 39 | bores in line ±0.02 | CNC |
| lid_handle, umbilical_clamp | 1.4301 / Al | — | — | bent bar / CNC |

### 3.2 Catalogue parts (labelled envelopes `ENV_*` in the CAD)

| Item | Maker / part (seen this session) | Specification it must meet | Status |
|---|---|---|---|
| Pilot valves ×21 | **SMC S070B-5DG** + bar bases **SS073B01-11C**, **-10C** (S070 catalogue) | 3/2 N.C., ≥ 0.45 MPa, ≤ 5 ms, ≤ 0.5 W, ≤ 7.2 mm pitch | sourced; envelope dims UNVERIFIED |
| Foil heaters ×2 | **Omega KHLVA-0502/5-P** (12.7 × 50.8 × 0.25 mm, 5 W at 28 V, polyimide, PSA, 150 °C; DigiKey page) | ≥ 3 W each at ≤ 24 V DC, PSA on Al | sourced (Omega page 403; data from DigiKey) |
| Temperature sensors ×2 | Pt100 thin film, **YAGEO Nexensos (Heraeus) M222** class (2.3 × 2.1 × 0.9 per search snippet of the datasheet; class A order number differs between regional datasheets) | Pt100 class A, ≤ 2.5 × 2.5 | part number UNVERIFIED (datasheet PDFs 404/503) |
| Hall ICs ×21 | **TI DRV5055** (SOT-23 2.92 × 2.37; 20 kHz; ±21…±169 mT ranges) | ratiometric analog, SOT-23 | sourced (variant A1/A2 to be chosen with the marker) |
| Draw latches ×2 + catch plates | **Kipp K0045.1541092** (stainless form A, F1 2000 N) + **K0045.9143372** | ≥ 300 N each, over-centre | sourced; envelope UNVERIFIED |
| Lid switch | Omron D2F-01L class subminiature, 0.1 A gold contact (distributor listings via search; Omron page 403) | SPDT, gold contact, ≤ 13 × 6 × 7 | UNVERIFIED |
| Pin springs, clamp springs, return springs, press-pad spring | custom-wound (spec §2.3, §2.7, §4.6) | — | UNVERIFIED |
| O-rings (pistons), rod seals, gas rings ID 5 / OD 7 / 1.0 | to be selected (FFKM/EPDM per docs/18 CHOICE-4 for gas rings) | — | UNVERIFIED |
| Orifices Ø0.15 | to be selected (jewel orifice class) | — | UNVERIFIED |
| Gas barbs M3 → 1/16″, gallery barbs, PU tube 3.18/2 | to be selected | — | UNVERIFIED |
| Flanged plain bushes (hinge, posts, shaft) | iglidur class | — | UNVERIFIED |
| Marker magnets Ø2 × 1 NdFeB | to be selected | — | UNVERIFIED |
| Pressure switch 350 kPa | to be selected | — | UNVERIFIED |

## 4. Calculations

### 4.1 Closing forces (calcs.pin_springs, cylinder_forces)

TPE force = spring force at closed ± guide friction 0.05 [assessment]: slot 1.03–1.37 N (limit 1.5, docs/13 §4),
anvil/cold 2.20–2.80 N (limit 3.0), V3 1.94–2.66 N. Nominal 1.2 / 2.5 = `Valve.f_close_nom` (CHOICE-3). Spring
force with no card 1.11 / 2.23–2.29 N (collar on the block). Sum of closing forces on the head (nominal, closed):
20 springs 42.2 N (6 × 1.2 + 14 × 2.5) + V3 limit spring 3.1 N = 45.3 N (Derived).

### 4.2 Cylinder force vs spring + friction (margin = F_cyl / need)

need = F_open,max (+10 %) + couple friction (μ 0.15 × 2 F L / 8 mm guide span) + O-ring 0.7 N (UNVERIFIED) + pin
guide 0.05 + return spring 0.5. Pull area Derived π/4 (6² − 1.5²) = 26.5 mm²; V3 push area 28.3 mm².

| p | Ø5 (interface) worst | Ø6 worst | Ø6 best |
|---|---|---|---|
| 300 kPa | 0.82 (V14) — fails | 1.20 (V14) | 1.97 (V3) |
| **400 kPa** | 1.10 (V14) | **1.60 (V14)**, V6 1.66 | 2.63 (V3) |

Worst channels are the long-offset 2.5 N valves (V14 L 9.8, V6 L 10.9, V15 L 8.8). Target ≥ 1.5 [assessment] →
Ø6 at 400 kPa (DEV-U1, DEV-U2). At 350 kPa (pressure-switch trip) the worst margin is 1.40 (Derived 1.60 × 350/400).

### 4.3 Actuation time (calcs.actuation_times)

Chamber volume 90 mm³ (gallery 25, header 15, valve 10 [assessment], dead 13, swept 27). Isothermal fill/exhaust
through the Ø0.15 orifice (Cd 0.8): lifting starts at 7.8 / 12.1 ms (slot / 2.5 N class), full pressure 29.6 ms;
**open ≈ 22–24 ms** incl. 3 ms valve response; exhaust to motion 34.6–46.8 ms, **closed ≈ 59 ms**. Both ≪ 0.2 s
(docs/13 §4). Without the orifice the valve (C 0.042) limits it to < 5 ms; the orifice is a deliberate brake.

### 4.4 Air consumption

0.36 NmL per actuation (90 mm³ × 400/101.3); 17 actuations per run (docs/13 §4: 16 cycles + V3) → 6.0 NmL/run;
16 runs/day → 0.1 NL/day; docking (all 21) 7.5 NmL. Static leakage of 21 O-rings UNVERIFIED (expected ≪ 1 NL/day).
The supply can be a small cylinder or the lab line through a regulator.

### 4.5 Pilot heat and EMI

Energised valve-minutes per run from docs/13 §4: 83.5 (V9/V10 46.5, V17/V18 20.7 dominate) + V3 energised while
**closed** (all of the run except 6.8 min) → 2.3 valves on average × 0.5 W = **1.14 W**, peak ≈ 3 W (6 valves).
Mounted on the bridge shelf 30 mm above the heater block, coupled to it only by the PEEK standoffs and the pin necks
(G = 0.0075 W/K): cylinder block rise ≈ 6 K at 10 W/m²K (Derived), 0.05 W into the heater block — inside the heater
control range. Read windows (docs/13 §7.2): **no valve switches**; valves that stay energised (V3, V9/V10) carry DC
only (no PWM hold, no power-saving circuit: the 0.1 W option is rated 0.3 MPa only); the coils sit ≥ 60 mm above the
die behind the grounded heater block and cover. Heater drive linear DC (no PWM). Hall ICs static.

### 4.6 Clamp and cam (calcs.clamp, latch_reaction)

Head force 2 × 150 − 20 (return springs) = **280 N** (±0.5 mm stack → 265–295). Reactions on the head: springs 42.2
+ V3 3.1 + press pad 12 + gas rings 10 = 67.3 N (Derived; the docs/18 budget uses the 3 N maxima) → **card-face clamp 213 N
(≥ 198 N)** vs docs/18 §6 requirement ≥ 50–165 N. Mean pressure on the L3 top ≈ 0.07 MPa (Derived 213 N / ≈ 3000 mm²);
chamber roofs (0.5 mm COC over Ø8) are inside Ø6 vent pockets. Cam: e 4.5, contact at 141° of rotation, peak shaft
torque 0.87 N·m incl. journal friction → **14.5 N at the 60-mm lever**. Lid reactions at 295 N: latches 186 N
(93 N each vs F1 2000 N), hinge 109 N. Press pad: spring 0.8 / D 6 / 9.4 turns, 2.0 N/mm, 11.0 N at the stop (0.5
below the nominal die back) → 12.0 N at DIE_T 0.70, 10.6–13.8 N over DIE_T 0.5–1.1 (`DIE_PRESS_PAD`) (Derived).

### 4.7 Thermal (calcs.thermal)

Heater block 77 g, C = 69 J/K. Losses at the worst ambient 18 °C (ΔT 7 K): convection 10 W/m²K × 0.0073 m² (top,
sides, fins) + standoffs 0.0013 W/K + pin necks 0.0062 W/K → G = 0.080 W/K → **0.56 W**; bottom face on the card
(card held at 25 °C by the anvil, docs/18 CHOICE-7) ≈ 0. Heaters 2 × 156.8 Ω at 24 V = **7.3 W** max (13 × the loss).
Warm-up of the block 18 → 25 °C ≈ 70 s at full power; passive τ = 860 s; the card follows in ≈ 10 min (docs/13 §6.5).
In-plane gradient ≈ 0.04 K (heat entering at the two fins, P L/(8 k A)) ≪ ±0.2 K. Sensors: control Pt100 at
(58, 38.5, z 11) — 5 mm from the die window, 5 mm from the cell (docs/13: cell 25.0 ± 0.2) — monitor Pt100 at
(30, 46, z 11) near the break; both in Ø3.2 holes drilled from the ±x faces, potted. Controller: PID, linear DC
driver, 0.01 K resolution front end (part to be selected). PEEK plate (reagent zone) is not heated (CHOICE-7).

### 4.8 Kinematics (checks.closing_arc, descent_sequence, sweep_check)

* Hinge axis dock (Y 195, Z 190); lid frame bottom Z 178.215; cover Y 55–196, Z ≤ 295; lever and latches inside
  X 150–320, Y ≥ 34.
* Closing arc (head raised, air off): lowest pin tip 1.75 mm above the card top, at 0° (tip height rises
  monotonically with the angle); guide-pin tips 0.5 above the nest claim top at 0°.
* Head descent: guide pins fully engaged (nose 1.0 passed, bush top assumed at the nest claim top Z 176.0) after
  1.5 mm; pin tips reach the bore lead-in after 2.76 mm with air on (pins lifted; docking state) and after 1.76 mm with
  air off → **guided travel before the bores 1.26 mm (0.25 mm worst case)**; bore capture radius ≥ 0.45 (clearance +
  lead-in, `PLUNGER card_bore_lead_in`) vs head-to-nest tolerance ±0.03 (`TOL`). Pins move only along −Z.
* Sweep 0–85° (5° steps, raised head, all lid solids except the guide pins, which are below the claim only when the
  head is down): CAD sweep box X 152.5–320, Y 33.6–299.7, Z 178.0–378.0, inside `lid_sweep_bbox()` (X 150–320,
  Y 29.4–305, Z 175.3–388.2); **no overlap with any other claim at any angle**; lowest lid material over the nest
  footprint Z 177.97 (≥ 1.97 above the nest claim); hinge blocks are fixed (ICR-U3); operator loading-path box at
  85°: 0 mm³ overlap. See `kinematics_side.png`, `iso_open.png`.

## 5. Interference check, closed state

Method (`checks.interference`, run by build.py): every solid of the closed configuration (head, lid frame, fixed
hinge parts, catalogue envelopes) **plus the card envelope built from interface.py** (L3 body with every pin bore
incl. 0.3 lead-in, die window, vent recesses, break slot; L0–L2 slab; die) — 251 solids; axis-aligned bounding-box
prefilter, then OCC Boolean common volume of every overlapping pair (949 pairs closed, 903 raised); volume
> 10⁻⁴ mm³ counts.
Result: **0 unintended interferences** (closed and head-raised); intended overlaps (listed in `checks.INTENDED`):
rods pressed into pistons (20), guide pins pressed into ears (2), pin tips pressing into the laminate (21; channels
are not in the envelope), shaft–eccentrics/lever, umbilical clamp–bundle. Claim check: outside UPPER only the pins
and press pad (inside the card), the guide pins (nest bushes), and the hinge blocks (ICR-U3); the latch bodies stay
inside the claim, their bails and catch plates use the LOWER keep-out of ICR-U2. Tightest plan
clearances: collar–collar 0.20 and spring–spring 0.30 (V11–V12, pitch 1.60); yoke webs, eyes, buttons, rods and
standoffs are all part of the 3D check. Section views: `section_pin_G4.png`, `section_tightest_pair_V11_V12.png`.

## 6. Choices (open points decided here; user may overrule)

| # | Open point | Chosen | Why | Alternatives |
|---|---|---|---|---|
| CHOICE-U1 | head = rigid or floating plates | rigid head; heater block and PEEK plate lapped coplanar on the assembled head | card is rigid L3; one datum for all pins | spring-floated PEEK plate |
| CHOICE-U2 | pin guidance | two CuSn8 guide plates (3 + 2 mm, span 7) inset in the Al block; V8 bush in PEEK starts 1.5 above the face (P_mv groove) | Ø0.8 at 1.6 pitch: no room for bushes; non-magnetic near M_d | zirconia plates (costly at 1.6 pitch); hardened steel (DEV-U4) |
| CHOICE-U3 | heater placement | two KHLVA-0502 foil heaters on vertical fins at the ±y edges | top face is full of pins; fins symmetric, outside the card | cartridge heaters along y edges; heated pads |
| CHOICE-U4 | vent pockets | Ø6 × 1.0 with 2-mm grooves to the nearest edge (IC1 +y, IC2 −y, RS +x) | `VENT_POCKET_D_LID`, vented sideways (CHOICE-16) | through-holes to the lid interior |
| CHOICE-U5 | spring design | springs above the collar, reacting on a spring plate at 24.5 | a spring below the collar would lift the pin (HEAD_Z wording) | spring in the tier zone |
| CHOICE-U6 | pin retention, hook | collar stop on the block (0.2 drop), button bonded at a 0.20 gauge gap | sets gap and lift independent of part tolerances | integral head + split spring |
| CHOICE-U7 | V3 mechanism | open spring under the collar; push cylinder with a force-limiting spring inside the piston | fail-open by spring; 2.5 N exact; no extra parts in the tier zone | separate limit spring on the pin (no room) |
| CHOICE-U8 | yokes | 1.0 laser-cut blades; J-yokes for V1, V9; push yoke for V3 | rod–pin offsets 0.7 and 2.7 too short for a web | move V9's cylinder to (41, 41.5) (interface change) |
| CHOICE-U9 | pilot valves, air | SMC S070 0.5 W on two bar manifolds on the head; one-layer galleries; Ø0.15 orifices | 7.2 pitch, 0.5 MPa, 3 ms; head-mounted → only one air line flexes | Lee LHD (15 psid std, docs/18 §5); tubes per cylinder |
| CHOICE-U10 | cylinders | custom 4-layer block, Ø6, POM pistons + O-ring, return spring 0.5 N | fits 9-mm grid; catalogue pen cylinders not checked this session | catalogue Ø4–6 cylinders (UNVERIFIED sizes) |
| CHOICE-U11 | position feedback | marker magnet + DRV5055 Hall IC per cylinder, + supply pressure switch | realistic at 9 mm pitch, static, sees the mechanics | optical forks (no room), none |
| CHOICE-U12 | clamp drive | eccentric shaft e 4.5 + 2 × 135 N preloaded springs (15 N/mm), lever 60 | force set by springs, self-locking at BDC, 14.5 N hand force | toggle clamps; pneumatic head drive (series) |
| CHOICE-U13 | lid latch | two Kipp K0045 draw latches at the front, catch plates on the nest | 186 N reaction ≪ 2000 N; standard part | hinge-side lock (cantilever 27 N·m) |
| CHOICE-U14 | counterbalance | none (CoM passes the hinge at ≈ 60°, 12 N lift), optional rotary damper | weight 23 N | gas strut (enters the rear claims) |
| CHOICE-U15 | guide pins | Ø6 on ears at card (−5, 44) and (80.5, 6), protrusion 7.7 below the face; tips 0.5 above the nest claim when raised | diagonal, clear of datums and pushers; engage before the pins | pins in the nest (docs/18 wording "located in the nest" kept: bushes are in the nest) |
| CHOICE-U16 | docking state | pull valves energised (pins lifted) during descent | 1.26 mm guided travel before the bores instead of 0.25 | descend de-energised |
| CHOICE-U17 | press pad | spring 11 N at a stop 0.5 below the die back, rate 2 N/mm, 1 mm silicone | 12.0 N at DIE_T 0.7; 10.6–13.8 over 0.5–1.1 | pneumatic pad |

## 7. Deviations

| # | From | Change | Why / effect |
|---|---|---|---|
| DEV-U1 | docs/18 §5 / `PLUNGER pilot_pressure_kPa` 300 | **400 kPa** (switch trip 350) | margin 1.20 → 1.60 on the worst channel (§4.2); S070 0.5 W coil rated 0.5 MPa |
| DEV-U2 | `PLUNGER cylinder_bore` 5.0 | **Ø6** (pitch 9 kept, walls 3) | Ø5 at 400 kPa gives 1.10; Ø5 at 300 kPa fails (0.82) |
| DEV-U3 | docs/18 §6 `CLAMP_DESIGN_FORCE` 250 | head force **280 N nominal, 295 N max** | card-face clamp ≥ 198 N at the upper seal budget (165 N) needs the extra; LOWER must design the nest/anvil for 300 N |
| DEV-U4 | docs/18 §12 "hardened, reamed guide" | **CuSn8 bearing bronze**, reamed H7 | hardened steels are ferromagnetic 6.4 mm above the M_d drag path (G1–G4, V11, V12 sit over the slot) [assessment] |
| DEV-U5 | docs/18 §5 `HEAD_Z` pin_head_closed_top 25.0 | collar at 16.4–16.9, spring plate 24.5–26.0, buttons in the tier bands | needed for spring-closed pins (CHOICE-U5); envelope `HEAD_Z` bands unchanged |
| DEV-U6 | docs/13 §6.2 "solenoid-opened" plungers | pneumatic cylinders with solenoid pilots | already docs/18 CHOICE-2; listed for completeness |

No departure from docs/13 Rev B functional numbers (forces, stroke ≥ 0.5, ≤ 0.2 s, fail states, 25.0 ± 0.2 °C).
Fail states (docs/13 §4): **loss of air** → pull cylinders vent → springs close V1, V2, V4–V12, V14–V18, G1–G4;
V3 cylinder vents → V3 open. **Loss of power** → S070 N.C. valves exhaust → same state. **Loss of PC** → dock
watchdog de-energises the valves → same. Clamp (manual cam, self-locking) and latches hold in every case.

## 8. Interface change requests

| # | Name | Current | Needed | Why |
|---|---|---|---|---|
| ICR-U1 | new `GUIDE_BUSHES` (LOWER) | "guide-pin bushes" without positions | two bushes Ø6 H7 at card (−5.0, 44.0) and (80.5, 6.0), top ≤ card z 6.0, depth ≥ 9 below, entry chamfer | guide pins of the head (CHOICE-U15) |
| ICR-U2 | new `LID_LATCH_KEEPOUT` (LOWER) | — | two catch plates Kipp K0045.9143372 on the nest front, keep-out X 173–199 and 271–297, Y 34–55, Z 161–176 (dock), each ≥ 300 N up | front reaction of the clamp (CHOICE-U13) |
| ICR-U3 | new `HINGE_RAIL` (BASE) | hinge blocks have nothing to bolt to; Y 185–200, Z 155–176 is unclaimed | rail top Z 160 under X 150–154 and 316–320, Y 185–200, carrying 110 N + 1.9 N·m | hinge blocks reach Z 160 (outside the UPPER claim) |
| ICR-U4 | `CLAMP_DESIGN_FORCE` | 250 | 300 | DEV-U3 |
| ICR-U5 | `PLUNGER pilot_pressure_kPa`, `cylinder_bore`; `HEAD_Z pin_head_closed_top` | 300; 5.0; 25.0 | 400; 6.0; collar 16.915 (spring plate 24.5) | DEV-U1, U2, U5 (UPPER-internal; informs BASE: air supply ≥ 450 kPa to the regulator) |

No error found in docs/18 geometry; note for the architect: `LID_HINGE_AXIS` knuckles (r 5) and the hinge pin end at
Y 200 exactly (claim edge).

## 9. Series-dock notes (C3 and beyond)

* Pins + springs as a replaceable **cassette** (guide plates, pins, springs, spring plate) located by two dowels;
  pins MIM or cold-headed; button by laser weld in a fixture.
* Cylinder block → moulded or diecast manifold with integrated galleries; pistons with lip seals; Hall ICs on the
  pilot-valve PCB; S070 valves replaced by a custom valve board (or piezo valves) with the pressure switch on board.
* Motorised head drive (lead screw or pneumatic) with force sensing instead of the manual cam; single interlocked
  latch; hinge with integrated damper; injection-moulded cover with conductive coating.
* Heater as an etched foil on a single fin ring; sensor bonded in a moulded pocket.

## 10. Open items / UNVERIFIED

O-ring friction (0.7 N assumed), spring material constants and fatigue, catalogue envelopes (S070, K0045, D2F),
M222 order number, orifice part, gas-ring force (5 N, docs/18 [assessment]), TPE force–leak relation (M4), closing
transient vs approach speed (M4), card stack tolerance ±0.06 [assessment], convection coefficient, cover grounding
and shielding effectiveness (M5a/C2), nest bush position (ICR-U1), lid mass ±20 % (envelope densities). Not
modelled: tubes and cables inside the lid, screws, gaskets, O-rings, PCB components except the Hall ICs.

## 11. Output files

`cad/out/dock_upper/`: `lid_assembly_{closed,raised,open}.step` (≤ 7.3 MB each), `subassy_head_closed.step`,
`subassy_lid_frame_closed.step`, `card_envelope_ref.step`, `parts/*.step` (35 files: single custom parts and families);
PNG: `iso_closed`, `iso_head_closed`, `iso_open`, `kinematics_side`, `head_underside` (+ `_zoom_J_cell`),
`section_pin_G4`, `section_tightest_pair_V11_V12`, `plan_cylinders_yokes`, `plan_air_galleries`, `exploded_head`;
`calcs.txt`, `checks.txt`. Package: `cad/elisa_cad/dock_upper/` (`params`, `calcs`, `parts`, `assy`, `checks`, `build`).

## 12. Sources opened this session (2026-11-13)

* SMC S070 series catalogue (specifications, response time, how to order, SS073B01 manifold dimensions):
  https://static.smc.eu/pdf/S070.pdf (opened as PDF, text extracted)
* Omega KHLVA-0502/5-P: https://www.digikey.co.nz/en/products/detail/omega/KHLVA-0502-5-P/25648745 (Omega's own
  page https://omega.com/en-us/p/KHRA-KHLVA-KHA-Series returned 403)
* TI DRV5055: https://www.ti.com/product/DRV5055
* Kipp K0045 latches with draw bail: https://www.marek.eu/data/katalogove-listy/kipp/K0045.pdf
* YAGEO Nexensos M222: search results only (datasheet links 404/503) — dimensions UNVERIFIED
* Omron D2F: search results only (omron page 403) — UNVERIFIED
* Spring catalogues: searched, no 0.2 mm / OD 1.3 catalogue spring found → custom spring spec
