# 23 — Dock and cartridge A: integration of the four physical-design modules (C2 prototype)

Status: 2026-11-13, **stage C0 desk work**, physical design round, INTEGRATION — **complete for this round**: interface
Revision B written, all four modules rebuilt from it, integrated assembly built and checked with **0 unintended
cross-module interferences**; open items §10. Inputs: docs/13 Rev B (functional design, not edited), docs/18 (now
**Revision B**), docs/19 (card), docs/20 (lid/head), docs/21 (lower bay), docs/22 (base), `cad/elisa_cad/*`.
Nothing is ordered. No source was opened in this step; every number is taken from the repository documents and CAD
(tags as docs/18: docs §, `interface.NAME`, **Derived**, **I-n** = integration choice §8, **UNVERIFIED**, [assessment]).

## 1. Scope

* Four module designs written in parallel (card A, dock upper/lid, dock lower bay, dock base) were made one design:
  every interface change request and every conflict found by reading and by the assembly check was decided, written
  into `cad/elisa_cad/interface.py` **Revision B** (changelog block at its top) and into the module parameters, and
  every module was rebuilt.
* New package `cad/elisa_cad/assembly/` places the REAL card, the lower bay, the lid (closed, head raised, open 85°)
  and the base in dock coordinates, runs the cross-module checks and writes `cad/out/assembly/`.
* User decisions for the round kept: cartridge A only; dedicated bench dock; C2 prototype; parametric CadQuery CAD →
  STEP + renders + documents; no automated test suite (one-off checks, reported here).

## 2. Resolution of the interface change requests (short form; full table with reasons: docs/18 §15)

| # | Conflict | Decision | Changed |
|---|---|---|---|
| 1 | guide pins UPPER (−5, 44)/(80.5, 6) vs LOWER (−7, 46)/(83, 4) | **(−8, 46), (84, 4)**, bush top z 5.0, anvil x −15…91 | IF, UPPER, LOWER |
| 2 | pilot 400 kPa / Ø6 vs BASE 300 kPa | **400 kPa, Ø6**, supply ≥ 450 kPa (lab air 500–700), BASE switch 450, lid switch 350 | IF, UPPER, BASE |
| 3 | clamp 280 (295) N vs 250 N; catch plates; nest top | **300 N** design; 2 LOWER catch brackets (95 N each); nest top z 5.0 (lid ≥ 2.97 mm above) | IF, LOWER |
| 4 | hinge rail vs IR-5 | **LOWER hinge pedestals** (top Z 160); BASE right partition moved +2 mm (lever 3.0 mm) | IF, LOWER, BASE |
| 5 | pass-throughs | exits = LOWER routes (`LIQUID_LINE_EXITS`); BASE re-routed; exhaust louvre; grommet; flange | IF, BASE |
| 6 | LOWER mount | 6 × M6 at X 165/305 + 2 dowels | IF, LOWER, BASE |
| 7 | drag slot | **widened slot** (`slot_polygon()`), square holder kept; foil 19 µm ≤ 20 µm (M4) | IF, LOWER |
| 8 | pogo | tips −1.66 retracted; 7.25 N; pad 12 N kept | IF, LOWER |
| 9 | M_c motion, thick zones | adopted (swing, fail = hold; DEV-L3 zones) | IF |
| 10 | magnetics / materials / relay | non-magnetic list (`MATERIALS`); screened reed relay, 5 mT acceptance | IF, UPPER |
| 11 | card requests | V8 no lead-in; MC Ø1.596; poka chamfer + nest block; tooling holes; WE2 2.9 / cell 1.31 µL; `DIE_WINDOW`; `CER_NECK['len']` | IF, card, LOWER |
| 12 | tip margin rule | 0.5 to openings, 0.3 to gasket seats | IF |
| 13 | README | rewritten | cad/README.md |

## 3. The integrated assembly and how to build everything

### 3.1 Package `cad/elisa_cad/assembly/`
| File | Content |
|---|---|
| `collect.py` | real solids of the four modules in dock coordinates: `card()` (card.parts.all_parts), `lower(state)` (dock_lower.assy.state_items; module card envelope dropped), `upper(config)` ('closed' / 'raised' / 'open', dock_upper.assy.configuration), `base()` (dock_base build solids + tubes), `scene()` |
| `checks.py` | cross-module interference (bbox prefilter + OCC Boolean, module-internal pairs skipped, designed contacts classified) and the feature checks of §4 |
| `zrender.py` | software z-buffer renderer (numpy): exact per-pixel occlusion, part outlines from id/depth discontinuities, translucent second pass, tinted section faces, scale bar, leader labels (I-14) |
| `render.py` | the integrated renders (§3.3) |
| `build.py` | `python -m elisa_cad.assembly.build [--fast] [--no-step] [--no-renders]`: checks → `checks.json/.txt`, STEP (§3.2), renders |

### 3.2 Integrated STEP files (`cad/out/assembly/`)
| File | State | Size |
|---|---|---|
| `dock_closed.step` | closed and latched, head down, read state (M_c parked, M_d holding at the RC, pogo up), real card | 9.1 MB |
| `dock_open_loading.step` | lid open 85°, head raised, lower `load` state, real card 60 mm above the nest | 9.1 MB |

Both are **simplified envelope versions** (full detail stays in the module STEPs): card L3, die and L4 discs real, L0–L2 +
film + seam as one laminate slab; lid head mechanism (pins, springs, buttons, yokes, rods, pistons, Hall ICs, barbs,
standoffs, posts, thrust units) omitted, cylinder-block layers, pilot manifolds, guide plates and spring plate as boxes;
LOWER tubes as cylinder chains, anvil openings simplified to 0.15 mm, heat sink and foil heaters as boxes; BASE rear and
left panels as boxes, only the 11 card lines and the 2 gas lines drawn (all other lines in `base_tubing.step`).
Without simplification each file was 22 MB.

### 3.3 Renders (`cad/out/assembly/*.png`, z-buffer, I-14)
`dock_iso_front_left_closed`, `dock_iso_front_right_closed` (lid cover translucent), `dock_open_loading` (card above the
nest, panels over the well hidden), `section_chamber_full_height` (x_card 40 through IC1/IC2, W1/W2, both M_c units, base
to lid; state collect_IC1), `section_chamber_zoom_collect_IC1`, `section_cell_die_pogo_Md` (x_card 58.0: G4 pin, RC,
die, pogo WE2/LOOP_A, press pad, M_d holder at the RC), `section_port_insert_P_in_P_byp` (x_card 34.2, real card, gasket,
insert, bonded tube), `bench_layout_top`, `exploded_four_modules`. Every PNG was looked at; the painter's-algorithm
artefacts of the module renders do not occur (exact depth per pixel); remaining limits in §3.5.

### 3.4 Output policy and repository size (task D)
Before: `cad/out/` ≈ 120 MB (dock_lower 59 MB with six 7.8 MB state assemblies, dock_upper 36 MB). Now
(`du -sh cad/out`): **59 MB** — interface 2.8, card 7.7, dock_upper 14, dock_lower 9.8, dock_base 5.9, assembly 19 (two 9.1-MB STEPs). Changes: (i) builds write by default only per-part STEPs
and ONE state assembly per module (LOWER `assy_lower_bay_hold_RC.step`, UPPER `lid_assembly_closed.step`, BASE the group
STEPs); `--all-states` regenerates the dropped files (LOWER five other states + six sub-assemblies, UPPER raised/open/head,
BASE `base_assembly_with_claims.step`), documented in `cad/README.md`; (ii) LOWER and BASE tubes are compounds of
cylinders and joint spheres instead of Boolean-fused solids, and the slot outline is simplified at 0.02 mm (STEP size,
same geometry within 0.02 mm); (iii) the integrated STEPs are envelope versions (§3.2); (iv) every PNG is re-saved
as a 256-colour palette PNG (`common.shrink_pngs`, called at the end of each build; 16.1 → 5.7 MB for the module PNGs,
visually unchanged). Note: (iv) was added after the final module builds and applied to their outputs by calling the
same function; a rebuild produces the same result.

### 3.5 Known render limits
Orthographic, flat-shaded; translucent parts are blended order-independently (approximate colour where several
overlap); section faces are tinted only where a cut face is exactly on the plane; labels are placed at 3-D points
(a leader may cross a part in front of the point when the point itself is hidden).

## 4. Cross-module checks (one-off, `assembly/checks.py`, results `cad/out/assembly/checks.json`, `checks.txt`)

### 4.1 Interference (OCC Boolean on bbox-overlapping pairs from different modules, > 1e-4 mm³ counts)
| Scene | Pairs tested | Unintended | Intended (classified) |
|---|---|---|---|
| closed / read (card + LOWER hold_RC + UPPER closed + BASE) | 1127 | **0** | 52 pairs: 20 closed pins into L1 and L2 (nominal tip height, §4.2), 11 gaskets × foil 0.748 mm³ each (= 0.12 compression), pogo tips × die metal/passivation (contact, 0.0002 mm³) |
| open, lid 85°, LOWER load, BASE, no card | 535 | **0** | — |
| card on the loading path, 120 / 60 / 20 / 5 mm above the seat, vs open lid, LOWER load, BASE | — | **0** at every height | — |
| magnet states collect_IC1, collect_IC2, gather_IC1, gather_IC1_low, drag_mid_IC1, beadout_end (card + LOWER + UPPER closed) | 60 each | **0** | — |
| lid sweep 0–85° in 5° steps (raised head) vs LOWER load + BASE + card | 5696 | **0** | moving lid parts X 152.5 (cover) … 320.0 (cam lever) → 3.5 / 3.0 mm to the BASE partitions |

Clashes found during the integration and fixed (owner module in brackets):
1. Guide-pin bushes (LOWER/UPPER): UPPER's GP1 bush at (−5, 44) would cut the nest opening and gutter; LOWER's GP1 bush
   left 0.2 mm to the opening and broke out of the anvil edge (x −12) → I-1.
2. Nest corner block vs LOWER's own card envelope (25 mm³, the envelope had no chamfer) → envelope given the chamfer
   (LOWER); with the real card the block clears the chamfer by 0.30 mm.
3. Anvil-module lift-off (LOWER service check): the new latch bracket stayed with the bay frame and hit the exhaust duct
   at 20–40 mm lift → bracket belongs to the anvil module; re-run 0 hits.
4. BASE re-routing to the real exits: P_d2 ran through the SV_b valve body, P_b and P_cf came within 1.0 / 0.5 mm of the
   S_b holding coil, P_s and P_a2 within 0.66 mm → lanes re-ordered (P_d2 under the other lines at Z 104, P_b x 143,
   P_a x 145, P_cf x 136, P_in x 133, P_a2 over FS2), 0 route/body and 0 tube/tube clashes.
5. Moving cam lever 1.0 mm from the right well partition (IR-5) → BASE partition moved to X 323–325 (3.0 mm); P_rf,
   P_a2 and the HQDP gas line re-routed around it.
6. UPPER sweep check counted its own new hinge-block claims as foreign → claim filter by owner (UPPER checks).
7. Integration-script error found and fixed before reporting (no design change): LOWER items were first collected with
   "no card" pushers/pogo, which showed false 7.4 mm³ pusher and pogo/pad overlaps.

### 4.2 Feature checks on the real geometry (closed state)
| Check | Result |
|---|---|
| 21 lid pins in the real L3 bores | **0** contact; radial clearance 0.15 (Ø1.2 in Ø1.5) / 0.20 (Ø0.8 in Ø1.2); tip centres on the valve xy (error 0.000) |
| tips on their channels | all 20 closed tips: centre over an L1 cut (channel), tip disc fully covered by TPE (8 points at 0.95 r); V3 drawn open (fail-open, tip z 0.97) |
| tip height | nominal z 0.17 (interface) puts 0.02–0.07 mm³ of each tip inside the L1 sheet over the channel lands and 0.2–0.45 mm³ inside the TPE: the real tip stops on compressed TPE above 0.17 → hook gap set on a reference card (I-13, open item O-5) |
| 11 port gaskets vs the real foil port holes | foil hole Ø1.0 present at every port; gasket concentric (0.000); gasket ∩ foil 0.748 mm³ = full annulus × 0.12 (0.754 expected, faceting) → no other foil opening under any gasket; inserts 0 contact |
| pogo pins / contact window / pads | 6 tips at z 0.340 on the 6 pads (1 per pad); 0 contact with L0, L1, L1b, L2, L3, seam (pass the real window) |
| datums, pushers, corner block | A1, A2, B and both pushers touch the real L3 (distance 0.000, no overlap); nest frame to card 0.300 (corner block); card rotated 180° or mirrored → 21.9 mm³ into the block (cannot seat) |
| die-back pad | footprint x 55.5–60.5 / y 29.6–33.1 inside the die; face on the die back (gap 0.000); 0 contact with L3 |
| gas rings P_c, P_mv | centred (0.000); full annulus 18.85 mm² on flat L3 (no bore or lead-in under the ring; V8 without lead-in) |
| vent pockets, head face | heater block, PEEK plate and guide plates 0 contact with L3 and L4 discs (pockets over the real vents) |
| contact areas | head face on the L3 top: heater block 1432 + CuSn8 guide plate 840 + PEEK plate 928 = 3200 mm² of 3349 mm² L3 top (rest: pin bores, vents, gas rings, die window, break slot); under the foil: anvil 2068 + cold block 837 + PEEK break frame 275 = 3180 mm² of 3682 mm² foil (rest: windows, slot, contact opening, ports, gaps) |
| head guide pins | GP1/GP2 concentric with the bushes (0.000), tip z −2.5 inside the bush (top z 5.0), no contact |
| tube hand-over | each of the 11 LOWER tube ends coincides with the BASE route end (gap 0.000) |
| card tooling holes | over the 5-mm plate, 7.8 mm (round) and 11.2 mm (slot) from the nearest anvil opening |

### 4.3 Calculations re-run with the integrated numbers
Anvil plate at 300 N: 4.6 µm (LOWER calcs); face seals 50 ShA 6.7 N × 11 = 74 N, × 1.5 = 110 N ≤ card-face clamp 198 N
(min); latches 2 × 95 N on the catch brackets (22 MPa in the bracket); hinge 111 N on the pedestals; pogo 7.25 N < pad
12 N (net 4.75 N on the die, 0.12 MPa); foil under G1/G2 19 µm (≤ 20 µm M4); lid air 0.36 NmL per actuation at 400 kPa,
free air total ≈ 1.1 L/min (dominated by the UNVERIFIED Flow EZ allowance); guided head travel before the bores 1.26 mm
(air on) / 0.25 mm (air off), unchanged.

## 5. Overall dimensions, mass, power, air, consumables

| Item | Value | Source |
|---|---|---|
| Envelope | 470 W × 420 D × 330 H (lid open 388 H); E-stop/light bar to Y −25 / −6 | docs/22 §1 |
| Bench width | stack 343 + 50 + dock 470 + 10 + Gamry 90 = 963 mm; depth 712 (stack, UNVERIFIED for SM-FL) | docs/22 §11.1 |
| Mass | BASE 34.7 kg (A1 + waste full) + LOWER 2.1 kg (Derived from the solids, stages 0.34 kg each per Zaber) + UPPER (lid) 2.3 kg + card 0.02 kg = **≈ 39 kg modelled**; + fasteners/cables ≈ 10 % [assessment] → ≈ 43 kg (BASE had allowed 13 kg for LOWER + UPPER → 48 kg) | docs/22, docs/20 §2.7, this check |
| Power | DC peak 358 W, average 136 W; mains ≈ 406 / 155 W (η 0.88 UNVERIFIED); lid pilots 1.1 W average, lid heaters ≤ 7.3 W, reagent Peltier 6.7 W, anvil heaters ≈ 10 W (inside the BASE allowance) | docs/22 §9.2, docs/20 §4.5/§4.7, docs/21 §5.4 |
| Air | lab air / N₂ 500–700 kPa (≥ 450 at the inlet), regulated 400 kPa (lid, pogo lift) and 120 kPa (Flow EZ, purge); ≈ 1.1 L/min free air | §2 #2, docs/22 §8 |
| Consumables per card (14 runs) | card A; A1 38 mL; conjugate 0.40 mL; HQDP 0.84 mL; beads 0.24 mL; waste 44 mL; docking prime 14.9 mL (included in A1) | docs/22 §6 (re-computed after the re-route) |
| Wear parts | 11 port gaskets (replaceable from the top), lid gas rings ×2, die-back pad silicone, pogo probes ×6; intervals UNVERIFIED | docs/21, docs/20 |

## 6. Consolidated custom-parts list (C2 build of one dock; per-card parts marked)

| Module | Part (count) | Material | Process |
|---|---|---|---|
| CARD (per card) | L0 foil, L1 channel sheet, L1s WE2 shim, L1b die film, L2 TPE | COC 140/175/150 µm, 25 µm adhesive, TPE 0.40 | laser cut (DXF in `out/card/`), laminated on dowels |
| CARD (per card) | L3 body | COC plate | CNC two-sided |
| CARD (per card) | die | borosilicate 0.70, Au/Ti, SU-8/PI | foundry (mask DXF) |
| CARD (per card) | L4 discs ×5, seam adhesive, label | PTFE membrane, UV adhesive, polyester | cut/dispense |
| UPPER | heater block, lid side plates ×2, front/rear beams, post blocks ×4, bridge + spacers, cylinder block (4 layers), gallery headers ×2, guide ears ×2, hinge blocks ×2, thrust housings ×2, umbilical clamp | Al 6061/6082 | CNC (heater block lapped with the PEEK plate) |
| UPPER | guide plates ×2, V8 bush | CuSn8 | CNC + jig ream H7 |
| UPPER | PEEK pressure plate, standoffs ×6 | PEEK | CNC/turn |
| UPPER | valve pins ×21 | Nitronic 60 (I-10) | Swiss turn + centreless grind |
| UPPER | buttons ×21, yokes ×21, spring plate | 1.4404 (I-10) | cut tube; laser/wire-EDM; laser + grind |
| UPPER | rods ×21, guide posts ×4, cam shaft, press-pad stem, hinge pin | 1.4305 | turn/grind |
| UPPER | eccentrics ×2, guide pins ×2 | 1.2842 hardened | turn/grind |
| UPPER | pistons ×21 | POM-C | turn |
| UPPER | cover | Al 5754 1.5 | sheet metal |
| LOWER | anvil, nest frame (with corner block), cold block, M_c holders/carriers/links/brackets ×2, M_d Z unit/adapter, electrode-bay box, retainers ×7, bay frame, **latch brackets ×2, hinge pedestals ×2** (I-3, I-4) | Al (anvil cast tooling plate, hard-anodised) | CNC, anvil lapped with the cold block |
| LOWER | port inserts ×11, PEEK break frame, pogo block, guide block, wedge, M_d holder, drip umbrella, exhaust duct | PEEK | turn / micro-mill / fold |
| LOWER | head guide bushes ×2 | CuSn8 | turn + ream in place |
| LOWER | M_d post | Ti-6Al-4V | turn |
| LOWER | face gaskets ×11 | EPDM/FFKM 50 ShA | die/laser cut |
| LOWER | leak electrode | FR4/PTFE PCB | PCB |
| BASE | base plate, bay deck, deck spacers ×5, pump shelf + back plate, bottle rack, partitions ×2, rear-low cover, well rear wall, panels, cold-box liner/skin | Al 6082 / 5754 | CNC / sheet metal |
| BASE | drip tray | 316 stainless 1.0 | folded + welded |
| BASE | air-gap waste head, A1 manifold, Peltier exhaust duct extension (I-5) | PEEK | CNC / fold |
| BASE | bead rocker cradle, conjugate holder, HQDP sleeve, Gamry lead duct + junction box | Al | CNC |

## 7. Catalogue parts (verified = vendor page opened by a module agent this round; otherwise UNVERIFIED)

| Part | Use | Status |
|---|---|---|
| SMC S070B-5DG + SS073B01-11C/-10C | 21 lid pilot valves | verified (catalogue); envelope interpretation UNVERIFIED |
| Kipp K0045.1541092 + catch plate K0045.9143372 | lid draw latches | verified (catalogue page); envelope UNVERIFIED |
| Omega KHLVA-0502/5-P ×2 | lid foil heaters | verified (DigiKey page) |
| TI DRV5055 ×21 | piston position | verified |
| Zaber X-LSM050A ×2 | M_d X–Y stage | verified (spec page); footprint UNVERIFIED |
| supermagnete Q-10-10-05-N ×2 | M_c magnets | verified (B_r UNVERIFIED) |
| PTR Hartmann 1007.70 class ×6 | pogo probes | series verified; part number/tip UNVERIFIED |
| Custom Thermoelectric 12711-5L31-04CL | reagent Peltier | verified |
| Tecan Cavro Centris ×5 | pumps | verified (dimensions); front-zone depth UNVERIFIED |
| Fluigent Flow EZ LU-FEZ-0345 ×2 | pressure channels | verified; air consumption, outlet position UNVERIFIED |
| Laird/Tark DA-024-24-02-00-00 | cold box cooler | verified |
| Gamry Reference 600+, 60 cm cell cable 985-00071 | potentiostat | verified |
| Sensirion SLF3S-0600F | FS1 | from docs/11 (not re-opened) |
| Pt100 M222 class, Omron D2F class, YAGEO, Mean Well LRS-350-24, LabJack U3, DURAN bottles, 20 × 20 profile | various | UNVERIFIED (pages 403/404 or listings only) |
| M_d/M_w magnets, pin/clamp/return/pad springs, O-rings, rod seals, gas rings, orifices, barbs, iglidur bushes, marker magnets, pressure switches, M_c worm drives, M_d Z gearmotor, pogo-lift cylinder, WE reed relay + mu-metal can, heat sink, fans, anvil heaters, thermistors, RH/T sensors, zirconia datum pins, spring plungers, card-presence sensor, SV_b, FS2, P_in sensor, levelling pads, isolators, E-stop, light bar, leak/level sensors, FR1/R2, Co-Cr-Ni spring wire, Nitronic 60 bar | — | **UNVERIFIED** (to be selected; specs in the module documents) |

## 8. Consolidated table of ALL choices (what the user reads to overrule)

One line each: what was chosen — why — how to overrule (file / parameter, then rebuild the named module and re-run
`assembly.build`). IF = `cad/elisa_cad/interface.py`. Status: **A** = as chosen by the module, **R** = revised at
integration.

### 8.1 Interface (docs/18)
| # | What | Why | How to overrule |
|---|---|---|---|
| CHOICE-1 | datum C = whole anvil top; A = 2 edge pins (x 12, 63), B = 1 pin (y 25); 5 N pushers | valves need foil support everywhere | IF `DATUM_*`, `PUSHERS`; LOWER nest |
| CHOICE-2 (R) | spring-closed pins, pneumatic cylinders on a 9-mm grid, yokes on 2 tiers, **Ø6 / 400 kPa** | pin pitch 1.6 unreachable by any actuator body; fail-closed by spring | IF `PLUNGER`, `CYLINDERS`; UPPER |
| CHOICE-3 | closing forces 1.2 N slot / 2.5 N other | below docs/13 limits 1.5 / 3 | IF `_v()`; UPPER springs; set by M4 |
| CHOICE-4 | liquid face seal: bonded 1/16″ tube in a PEEK insert + flat gasket 1.7/3.3/0.5; lid gas rings 5/7/1 | no added dead volume, 3.6 port pitch | IF `FACE_SEAL`, `GAS_SEAL_LID`; LOWER, UPPER |
| CHOICE-5 (R) | 5-mm Al plate over the magnet bay, 15-mm port zones (DEV-L3 shapes); tip margin 0.5 to openings, **0.3 to gasket seats** | magnets must reach the foil; inserts need depth | IF `ANVIL_*`, `VALVE_TIP_*`; LOWER |
| CHOICE-6 | M_d on an X–Y stage far below, vertical post, cam Z; park under J lowered | post fits the slot; stage away from the electrode bay | IF `MAGNETS['M_d']`; LOWER |
| CHOICE-7 | Al heater block 10 mm (= pin guide), PEEK top plate, Al cold plate, PEEK break | two thermal zones | IF `THERMAL`; UPPER, LOWER |
| CHOICE-8 (R) | distributed clamp through heater block/PEEK plate; **design 300 N** | uniform foil contact | IF `CLAMP_DESIGN_FORCE`; UPPER cam springs |
| CHOICE-9 (R) | 2 × 3 pads at 1.8; pogo block 3-mm lift (tips −1.66 retracted); 12 N pad | no scrubbing during loading | IF `POGO`, `DIE_PRESS_PAD`; LOWER, UPPER |
| CHOICE-10 | rear hinge, 85° stop, 8-mm vertical head descent by cam | pins enter bores vertically | IF `LID_HINGE_AXIS`; UPPER |
| CHOICE-11 | vertical top-down loading; top-face code read with the lid open | no drawer | IF `ID_CODE`; LOWER/UPPER |
| CHOICE-12 | card bay front-centre, cold left, bottles right, pumps/electronics rear, Gamry right | short lines to SM-FL and Gamry | IF `CARD_ORIGIN_IN_DOCK`, `SPACE_CLAIMS` (all modules) |
| CHOICE-13 | card corners R1.0; laminate 0.2 inside L3 | only milled edges touch datums | IF `CARD_CORNER_R`, `LAMINATE_INSET`; card |
| CHOICE-14 | die window die + 0.05, TPE cut die + 0.10, film die + 0.15, seam adhesive | lanes leaving the die need a ceiling | IF `DIE_*`; card |
| CHOICE-15 | TPE 0.40 | middle of 0.3–0.5 | IF `TPE_T`; card; M4 |
| CHOICE-16 | blind cavities roof 0.5, recessed vents, lid vent pockets Ø6 | flat card top for the clamp | IF `CHAMBER_ROOF_T`, `VENTS`; card, UPPER |
| CHOICE-17 | break bridges y 3.5–6.5 and 43.5–46.5 | away from the conjugate lines | IF `BREAK_BRIDGES_Y`; card |

### 8.2 Card (docs/19)
| # | What | Why | How to overrule |
|---|---|---|---|
| C1 | die window: datum faces flush (x 55.0, y 33.35), free faces +0.10, Ø1.0 corner reliefs (now IF `DIE_WINDOW`) | die lands at its interface position on the datums | IF `DIE_WINDOW`; `card/profiles.py` |
| C2 | MC stop: Ø3.4 counterbore, Ø3.0 PTFE disc on 25 µm ring → stop z 5.14 | keeps 10.0 µL foil-to-stop | `card/profiles.py MC_*` |
| C3 | tank corner radii R1.0 | Ø2 tool at L/D 2.5 | `TANK_CORNER_R` |
| C4 | lamination dowels Ø2 at (59, 42) + slot (59, 5) | free area near J/cell | IF `CARD_TOOLING_HOLES` |
| C5 | WE2 shim 0.01 smaller per side | drop-in fit | `WE2_SHIM_GAP` |
| C6 | L4 discs on 25 µm adhesive rings | 0.2 floor under the recess | `ADH_T` |
| C7 | poka-yoke 4 × 45° chamfer at (75.5, 50) + engraved arrow (nest block added, I-11) | one corner breaks all wrong orientations | IF `CARD_POKA_CHAMFER`, `NEST_POKA_BLOCK` |
| C8 | PTFE disc also on P_c | keeps conjugate out of the gas line | `P_C_DISC` |
| C9 | ID label in a 6.6 × 6.6 × 0.10 recess | label below the clamp plane | `ID_RECESS` |
| C10 | no lead-in at V8 (now IF) | P_mv ring land | IF `PLUNGER['card_bore_lead_in_except']` |
| C11 | V12 and G3 bores merged into the V11/V12 slot | web 0.451 < 0.5 | `card/parts.py` merged bores |
| C12 | single-metal-layer electrode routing, CE/RE via the +x/−y edges, WE2 opening 1.1 wide | no crossings; areas immune to ±0.05 | `card/profiles.py metal()` |
| C13 | RCj wall boss r 1.25 around V8 | web 0.5 | `card/parts.py` |
| C14 | sliver-free cut extensions (throat, nozzle mouths, meter strips) | no knife-edge slivers | `card/profiles.py L1()` |
| C15 | L1 cut on a transfer liner (5 islands) | islands keep position | process note |
| C16 | bonding per interface (thermal press L0–L1; UV/ozone TPE; PSA die; UV seam; PSA L4) | docs/13 §2.1 route | process note (all parameters UNVERIFIED) |
| C17 | TPE compresses 25 µm over the film rim | consequence of CHOICE-14 | IF `Z_L1B` / film size |
| C18 | two-sided machining of deep narrow features | L/D ≤ 2.75 | process note |
| C19 | minimum milled web 0.5 | [assessment] | `MIN_WEB_L3` |

### 8.3 Dock upper — lid and head (docs/20)
| # | What | Why | How to overrule |
|---|---|---|---|
| U1 | rigid head, plates lapped coplanar | one datum for all pins | `dock_upper/params.py` |
| U2 | two CuSn8 guide plates + V8 bush | non-magnetic; Ø0.8 at 1.6 pitch | `GUIDE_PLATE_*` |
| U3 | two foil heaters on vertical fins at ±y | top face full of pins | `HEATER_FIN`, `HEATER` |
| U4 | vent pockets Ø6 × 1 with side grooves | vented sideways | `VENT_*` |
| U5 | springs above the collar on a spring plate at 24.5 | spring below would lift the pin | `SPRING_PLATE_Z` |
| U6 | collar stop 0.2 below closed; button bonded at a 0.20 gauge gap (**set on a reference card**, I-13) | gap independent of part tolerances | `HOOK_GAP`, assembly procedure |
| U7 | V3: open spring + push cylinder with force-limit spring | fail-open by spring, 2.5 N exact | `V3` |
| U8 | 1.0 laser-cut yokes, J-yokes V1/V9, push yoke V3 (**1.4404**, I-10) | short rod–pin offsets | `parts.yoke()` |
| U9 | SMC S070B-5DG on 2 bar manifolds on the head; one-layer galleries; Ø0.15 orifices | 7.2 pitch, 0.5 MPa, 3 ms | `PILOT` |
| U10 | custom 4-layer cylinder block Ø6 | fits the 9-mm grid | `CYL_LAYERS`, IF `PLUNGER` |
| U11 | marker magnet + DRV5055 Hall IC per cylinder + pressure switch | static, sees the mechanics | `PISTON_MAGNET`, `HALL_PCB_Z` |
| U12 | eccentric cam e 4.5 + 2 × 135 N springs, lever 60 | self-locking, 14.5 N hand force | `CAM`, `CLAMP_SPRING` |
| U13 | two Kipp K0045 draw latches, catch plates on LOWER brackets | 95 N each ≪ 2000 N | `LATCH`; IF `LID_LATCH` |
| U14 | no counterbalance | 12 N lift at the handle | add a strut/damper in `parts.py` |
| U15 (R) | guide pins Ø6 at **(−8, 46), (84, 4)** (IF) | diagonal, clear of datums/pushers/opening | IF `HEAD_GUIDE_PINS` |
| U16 | pull valves energised during descent | 1.26 mm guided travel instead of 0.25 | controller sequence |
| U17 | press pad spring 11 N at a 0.5 stop, 2 N/mm | 12 N at DIE_T 0.7 | `PAD_SPRING` |

### 8.4 Dock lower — nest, anvil, magnets, electrode bay (docs/21)
| # | What | Why | How to overrule |
|---|---|---|---|
| L1 (R) | one Al cast-tooling-plate anvil, hard-anodised, lapped with the cold block; **x −15…91** (I-1) | non-magnetic, stable | `dock_lower/geom.py ANVIL_*` |
| L2 | separate 5-mm nest frame (pins, pushers, sensor, bushes, **corner block**) | vertical drop, frame never on the foil | `NEST_*`, `parts.nest_frame()` |
| L3 | one bottom pocket x 32.5–62.5 + bosses | one 5-mm plate for M_c, M_d, ebay | `POCKET_RECT`; IF thick zones |
| L4 | cold block in a PEEK U-frame, one 30 × 30 Peltier, fan + front duct | 8× margin on Qmax | `COLD_*`, `PELTIER`, `DUCT` |
| L5 | inserts from below with retainers; 50 ShA gaskets | gasket swap from the top; seal force within budget | `INSERT`, `RETAINERS` |
| L6 (R) | head guide bushes at the IF positions | shared with UPPER | IF `HEAD_GUIDE_PINS` |
| L7 | perimeter drip gutter + 2 drains | spills never reach the stage | `GUTTER` |
| L8 | 4 foil heaters under the thick frame | no heater near openings | `ANVIL_HEATERS` |
| L9 | zirconia datum pins 0.2 above the anvil | non-magnetic, gutter passes below | `DATUM_PIN_*` |
| L10 | M_c holder flange on the plate underside (gap by geometry) | gap from two machined dimensions | `MC_FLANGE` |
| L11 | 2 × Zaber X-LSM050A X on Y + cam Z | sourced repeatability/speeds | `STAGE`, `MD_ZUNIT` |
| L12 | lowered transits via J | docs/13 §2.2 rule | `TRANSIT_LOWERED` |
| L13 | PEEK drip umbrella on the Z unit | protects the stage | `MD_ZUNIT['umbrella']` |
| L14 | tubes: vertical drop, R 25 bend, staggered levels to walls W/E | only route with R ≥ 25 outside the M_d sweep | `TUBE_*`; IF `LIQUID_LINE_EXITS` |
| L15 | bay frame: walls outside the stage sweep, 4 beams, anvil module on dowels (+ hinge pedestals, I-4) | anvil removable as one unit | `BAY_*`, `HINGE_PEDESTALS` |
| L16 | PEEK pogo block lifted by a 2:1 wedge from a cylinder outside the bay | no coil/motor in the bay | `POGO_*` |
| L17 | relay low in the bay, RH/T, leak PCB + drain, gland E wall | short leads, local leak detection | `RELAY`, `RH_SENSOR` |
| L18 | M_c drive stepper + self-locking worm, flag switches | holds without power | `MC_DRIVE` |
| L19 | condensation: foam + dry-air purge + RH/T; Peltier only with card + lid closed | plate below the lab dew point | `FOAM_T`, controller |

### 8.5 Dock base (docs/22)
| # | What | Why | How to overrule |
|---|---|---|---|
| B1 | Al 10-mm base plate, 20 × 20 profile frame, 2-mm panels; bay deck on 5 spacers | stiff short path for stage + anvil | `dock_base/params.py`, `layout.py` |
| B2 | 5 × Cavro Centris in a rear row, valves to a rear service door | only pump with verified dimensions | `PUMP_*` |
| B3 | A1 500 mL; conjugate + beads in 2-mL tubes in the cold box; HQDP 15 mL dark sleeve; waste 1 L | daily replacement needs small volumes | `DURAN_*`, `TUBE_*` |
| B4 | one air-gap waste head | breaks the liquid path to earth | `NIPPLES` |
| B5 | PU/Al cold box, Laird/Tark DA-024-24 on its rear wall | verified part, ×2.9 margin | `COLD_BOX`, `COOLER` |
| B6 | custom rocking cradle ±20°, 0.2–0.5 Hz | no stir bar | layout `bead_rocker_*` |
| B7 | grounded electronics sub-enclosure, 2 × 24 V 350 W + 12 V low-noise, PWM ≥ 25 kHz LC-filtered | quiet reads | layout electronics |
| B8 | open well over the bay; front doors; top hatch; rear pump door | operator front/top, service rear | `layout.py` panels |
| B9 | whole-footprint stainless tray, sump + level switch, 4 electrode strips | docs/13 §6.8 | `TRAY` |
| B10 | Gamry on the bench right, isolated duct + junction box (star point) | leads ≤ 0.3 m | `GAMRY*`, `BULKHEAD` |
| B11 | bead line PEEK 0.102 ID | ≤ 2.5 µL on a realistic route | `fluidics.TUBES` |
| B12 (R) | lab air/N₂ **500–700 kPa**, FR1 **400 kPa** (lid), R2 120 kPa; no compressor | vibration/noise near reads | `AIR_*`, layout FR1/R2 |
| B13 | 2 × Flow EZ 345 mbar, ch2 shared via 3/2 valves for the fills | fills only at insertion | layout pneumatics |
| B14 | P_in sensor at the upstream wall end; PEEK 0.127 ID | ≥ 0.3 m PEEK isolation | `fluidics` P_in route |
| B15 | FS1 SLF3S-0600F on P_a; FS2 (≥ 20 µL/min, TBD) on P_s | docs/13 §6.2 duties | layout sensors |

### 8.6 Integration (this document)
| # | What | Why | How to overrule |
|---|---|---|---|
| I-1 | guide pins (−8, 46)/(84, 4); anvil x −15…91 | bush walls ≥ 1.2 mm to the nest opening, 2 mm to the anvil edge; neither module's set worked as drawn | IF `HEAD_GUIDE_PINS`; LOWER `ANVIL_X` |
| I-2 | pilot 400 kPa, Ø6; supply ≥ 450 kPa; BASE FR1 400 kPa, supply switch 450 | UPPER's force margin; S070 0.5 W coil rated 0.5 MPa | IF `PLUNGER` |
| I-3 | clamp design 300 N; catch brackets on the anvil front face | covers 295 N max; closes the loop in LOWER | IF `CLAMP_DESIGN_FORCE`, `LID_LATCH`; LOWER `latch_brackets()` |
| I-4 | hinge pedestals in LOWER (top Z 160); BASE right partition X 323–325 | clamp loop inside LOWER + UPPER; lever 3 mm from the partition | IF `HINGE_SUPPORT`; BASE `PART_X` |
| I-5 | line exits = LOWER routes; BASE re-routed; exhaust duct extension + louvre | LOWER exits are geometrically forced | IF `LIQUID_LINE_EXITS`, `PASS_THROUGHS` |
| I-6 | LOWER bolted with 6 × M6 at X 165/305 + 2 dowels | X 235 holes under the stage | IF `LOWER_MOUNT` |
| I-7 | widened drag slot; square M_d holder | 2 × 2 magnet does not fit a round Ø2.6 holder; foil 19 µm ≤ 20 µm (M4) | IF `slot_polygon`, `SLOT_HOLDER_CLEAR` (a round Ø2 × 4 magnet + round holder would allow the docs/18 slot: changes docs/13 M_d) |
| I-8 | pogo retracted tip −1.66; pad 12 N kept | probe travel 1.27 | IF `POGO`, `DIE_PRESS_PAD` |
| I-9 | M_c swing + fail-hold; DEV-L3 zones | spring return collides with the M_d post | IF `MAGNETS` (spring-up needs an M_d interlock and a new collision study) |
| I-10 | non-magnetic parts list; screened reed relay with 5 mT acceptance | work-hardened 1.4310/1.4301 is magnetic; relay must stay near the die | IF `MATERIALS`, `WE_RELAY_FIELD` |
| I-11 | card requests accepted (V8, MC round, poka block, tooling holes, WE2 2.9, `DIE_WINDOW`, `CER_NECK['len']`) | keeps docs/13 numbers (cell −2.1 % only) | IF entries named |
| I-12 | tip-margin rule: 0.5 openings / 0.3 seats | gasket supports the foil | IF `VALVE_TIP_*` |
| I-13 | hook gap 0.20 set with a gauge on a reference card at the real closed height | nominal tip z 0.17 lies inside the L1 lands (§4.2) | UPPER assembly procedure |
| I-14 | integrated renders by a software z-buffer (zrender.py) | painter's artefacts in the module renders | use `common.render_png` instead |
| I-15 | committed STEP policy: per-part files + one state per module; `--all-states` regenerates the rest; tubes as compounds (no Boolean fuse); slot outline simplified at 0.02 | repository size | README flags; `parts.tube_solid`, `slot_polygon` |
| I-16 | `PLUNGER tip_z_open` = closed + stroke = 0.97 (Rev A 1.015, inconsistent with the 0.8 stroke) | the drawn pins already used 0.97 | IF `PLUNGER` |

## 9. Consolidated table of ALL deviations from docs/13 Rev B

Effect on each docs/13 number and the docs/13 bench test that must absorb it (M1–M8, M5a; E-numbers of docs/06).

| # | Deviation | docs/13 number → now | Absorbed by |
|---|---|---|---|
| DEV-1 | planar ladder island (no crossings) | C_k 0.26 → 1.42 µL; bead path 3.3 → 3.54 (CAD 3.60) µL; M_in 1.05 → 1.37 µL; conj. lines 0.6 → 0.73/1.43 µL | M3 (C_k chase ≤ 10⁻³; consider 5 µL chases), M1 |
| DEV-2 | Ø0.8 pins, bores into die-window notches | stubs G3/G4 0.044 → 0.031, V14 0.026 → 0.018, V15 0.016 → 0.024 µL; escape not re-run | M5a escape arm, M5 |
| DEV-3 | lanes arrive at ±40° on R 3 arcs, drag filleted | WL 15.0 → 15.255 mm (1.34 µL); drag 23.3 → 23.41 mm (117.1 s) | M1 (drag), M8 (timing) |
| DEV-4 | square 11.4 windows; M_c leaves outward; M_h deleted, M_d holds at the RC | gaps/forces unchanged; actuator count −1; no 2-s unheld hand-over | M1, M8 |
| DEV-5 | BW at (57.85, 17.2) over M_w; M_d stops 3 mm upstream | bead-out 4.5 → 4.55 mm; hand-over by flow (≈ 8 s of 30 s, UNVERIFIED) | M1 (BW retention) |
| DEV-6 | new port P_a2 for V11 | 10 → 11 liquid ports (+1 seal) | M4 (seal), C2 docking leak test |
| DEV-7 | blind chambers, roof 0.5 + Ø2 vent | IC total 290 → 280 µL (CAD 278.9); working 185 µL kept | M2 |
| DEV-C1 | MC round Ø1.596 (same area) | MC 10.0 µL kept (9.996 + 0.029 ring gap); conj. hold-up +0.03 µL | M3 (conjugate CV), first-article gravimetric MC |
| DEV-C2 | G4 WE1 finger stops 0.25 inside the die edge | WE1 5.35 → 5.13 mm²; Q_dl 0.22 → 0.21 µC; 0.025 µL of the G4 lane not under WE1 | M5 (escape/collection re-run) |
| DEV-C3 | L4 discs on adhesive rings (not heat-staked) | none; leachables UNVERIFIED | M3 (vent wet-out), C2 |
| DEV-C4 | WE2 channel 2.9 long (interface; confirmed I-11) | cell 1.34 → **1.31 µL** (−2.1 %): blank 0.051 → 0.050 nC, lot free HQ 7.8 → 7.6 nC, ULOQ −2 % | per-lot calibration; cell height by PE1 decay at docking; M5 |
| DEV-C5 | tank corners R1, V8 boss | RCj 0.500 → 0.496 mL, RS 0.720 → 0.716 mL (fills unaffected) | none (fills 0.26 / 0.6 mL) |
| DEV-C6 | funnel walls inside the bore | 185 µL fill height 3.68 → 3.71 mm | M2 |
| DEV-U1/U2 | pilot 400 kPa, Ø6 cylinders (docs/18 300 / Ø5) | none (docs/13 forces/stroke/time kept: open ≈ 22–24 ms, close ≈ 59 ms ≪ 0.2 s) | M4 (actuation transient), C2 |
| DEV-U3 | head force 280 N (≤ 295) | none of docs/13 (docs/18 budget only) | C2 |
| DEV-U4 | CuSn8 guides instead of hardened | none | M4 (wear over cycles) |
| DEV-U5 | collar/spring-plate layout | none | — |
| DEV-U6 | pneumatic cylinders with solenoid pilots ("solenoid-opened" in docs/13 §6.2) | none (fail states kept) | M4, C2 |
| DEV-L1 | M_c fail state **hold** instead of spring-up | docs/13 §3.3.1/§4 fail state changes: beads are held by whichever magnet is engaged at a power loss | M1 (power-loss recovery arm), C2 fault-recovery cycle |
| DEV-L2 | M_c parallelogram swing, park top z −45.6 | stray force at the own chamber 0.055 → 0.005 pN (better) | M2 (capture unaffected) |
| DEV-L3 | thick zones changed | none | — |
| DEV-L4 | slot widened to clear the square holder | foil deflection at G1/G2 under 1.5 N 15 → **19 µm** (M4 acceptance ≤ 20 µm) | **M4 slot variant at 4.44 mm span** |
| DEV-L5 | pogo retracted tip −1.66 | none | M5a contact route |
| DEV-L6 | LOWER sub-claims and exits | none | — |
| DEV-B1 | P_in line 0.55 m (8.0 µL; now 0.52 m, **7.6 µL**) instead of 0.3 m / 3.8 µL | unflushed-line carry-over term scales (3.8 + 1.05 → 7.6 + 1.05 µL); D13 flush still ≈ 26 line volumes | E1.10, M7 (carry-over 100 ng/mL challenge); option 0.102 ID → 4.9 µL |
| DEV-B2 | tidal coils 60 → **140 / 160 µL** (0.5 mm FEP to the rear pumps) | requirement "stroke stays in the coil" met with margin; extra dead volume behind the stroke | M2 (mixing), C2 |
| DEV-B3 | bead outlet line 0.25 × 50 mm → 0.102 × 231 mm (**1.87 µL**, volume met) | bead adhesion/clogging in 0.1 mm PEEK unknown | M3, docs/06 E2.2 |
| DEV-B4 | unclaimed space used (now claimed, Rev B) | none | — |

## 10. Open defects and UNVERIFIED items, ranked by consequence

No geometric clash remains in the integrated model (§4). Open items, highest consequence first:

| # | Item | Consequence if wrong | Where it is closed |
|---|---|---|---|
| O-1 | L1-to-L3 registration ±0.05 (laser position, post-bond shrink UNVERIFIED); G1–G4 lateral TPE margin 0.01 at worst case | gate/valve leaks at J and the cell | first cards, inspection (a) docs/19 §4; M4 |
| O-2 | foil deflection 19 µm under G1/G2 at 1.5 N (slot widened, DEV-L4) vs M4 limit 20 µm; COC modulus UNVERIFIED | slot-valve leak or magnet-gap change at J | M4 slot variant at a 4.44-mm span; fallback: rotate-free round holder with a Ø2 × 4 magnet (changes docs/13 M_d) |
| O-3 | WE reed relay in 1.9 mT (M_c1 parked); screened part UNVERIFIED | false switching or leakage on the WE line | incoming test at 5 mT, M5a |
| O-4 | pin/spring/yoke materials non-magnetic: Nitronic 60 / Co-Cr-Ni permeability and spring G, strength UNVERIFIED | closing-force error or field distortion near the chambers | incoming μr check; M4 rig spring fatigue |
| O-5 | real closed tip height (nominal z 0.17 lies inside the L1 lands); hook gap procedure | valve closing force taken by the yoke if the gap is set on the nominal | reference-card gauge procedure (I-13); M4 |
| O-6 | M_c fail state hold (DEV-L1) | beads held by whichever magnet is engaged at power loss; recovery sequence needed | C2 fault-recovery cycle, M1 power-loss arm |
| O-7 | P_in line 7.6 µL vs 3.8 µL (DEV-B1); coils 140/160 µL (DEV-B2); bead line 0.102 mm ID (DEV-B3) | carry-over term, mixing, bead clogging | E1.10, M7; M2; M3 / E2.2 |
| O-8 | seal force/modulus of 50 ShA gaskets (Gent form, UNVERIFIED), HQ/Tween compatibility | clamp budget, leaks | M4, C2 docking leak test |
| O-9 | M_d gap chain worst case 82 µm (RSS 32) vs ±50 µm | drag force at the RC/J | shim at assembly, measure at 5 positions |
| O-10 | catalogue envelopes (S070, K0045, X-LSM footprint, Centris front zone, Flow EZ outlet), heat-sink/fan performance, cooler capacity at 25 K | local re-layout | first article / datasheets |
| O-11 | lid air and Flow EZ consumption allowance; lab air availability ≥ 450 kPa | supply sizing | site survey |
| O-12 | cell volume 1.31 µL (DEV-C4), WE1 5.13 mm² (DEV-C2): escape/collection model not re-run | calibration constants, escape | M5 |
| O-13 | integrated STEP files are envelopes (head mechanism, most tubes omitted) | none for design; documentation only | module STEPs carry full detail |

Full UNVERIFIED lists: docs/19 §11, docs/20 §10, docs/21 §11, docs/22 §16, docs/18 §13.

## 11. Notes for C3 / series
* Card: moulded L3 with cored bores (DEV-C1 reversible: rectangular meter), moulded vent roofs (heat staking), L1 by
  embossing; moulded die pocket; tooling holes moulded (docs/19 §10).
* Lid: pin/spring cassette on two dowels; moulded manifold with integrated galleries; motorised head drive with force
  sensing; single interlocked latch (docs/20 §9). Keep the clamp loop closed inside the bay structure (I-4).
* Lower: compact custom XY; anvil + nest frame + hinge pedestals + latch brackets as one casting; moulded PEEK port
  manifold to two multi-line connectors (removes the 25-mm bend constraint and the BASE lane congestion); pogo lift
  driven by the head descent (docs/21 §10).
* Base: sheet-metal or cast chassis; pumps S_IC1/S_IC2 beside the bay (coils → 60 µL, DEV-B2 removed); one controller
  PCB; OEM pressure module (docs/22 §15).
* Integration: put every cross-module number in interface.py from the start (positions of guide pins, line exits,
  hinge/latch supports were the conflicts of this round); run `assembly.build` after every module change.

## 12. Final build status (this round, 2026-11-13, 4-core container, modules built in parallel)

| Module | Command (from `cad/`) | Run time | Result |
|---|---|---|---|
| interface plans | `python -m elisa_cad.interface_plan` | 9 s | pass (drawings/claims now Rev B) |
| card | `python -m elisa_cad.card.build` | 44 s (25 s alone) | pass; checks unchanged (MC 9.996 µL, 21 tips) |
| dock upper | `python -m elisa_cad.dock_upper.build` | 3 min 41 s | pass; 0 unintended interferences (closed, raised); sweep: no foreign claim; guided travel 1.26/0.25 mm |
| dock lower | `python -m elisa_cad.dock_lower.build` | 8 min 31 s (in parallel; ≈ 5 min alone) | pass; 0 interferences in 8 states; 0 M_d sweep collisions on 14 paths; anvil lift-off 0 hits; holder clearance ≥ 0.30 |
| dock base | `python -m elisa_cad.dock_base.build` | 6 min 3 s | pass; 0 route/body, 0 tube/tube, 0 claim/sweep/loading-path intrusions |
| assembly | `python -m elisa_cad.assembly.build` | 22 min (checks ≈ 2 min, STEP ≈ 3 min, renders ≈ 17 min) | pass; 0 unintended cross-module interferences in every scene (§4) |

No clash remains open. Not done in this round: no automated test suite (user decision); `--all-states` outputs were not
regenerated after the final changes (they are not committed).

## 13. Sources
No vendor or literature source was opened in the integration step. Inputs: docs/13 Rev B, docs/18–22 and their CAD
packages (vendor sources listed in docs/19 §12, docs/20 §12, docs/21 §12, docs/22 §17).
