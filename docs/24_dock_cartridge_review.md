# 24 — Adversarial review of the cartridge A physical design and its dock (docs/18–23, `cad/`)

Status: 2026-11-13, complete. Stage C0 desk work, **independent review** of the physical-design round (docs/18 Rev B, docs/19–23,
`cad/elisa_cad/*`, `cad/out/*`). The reviewer took no part in the design. No file other than this one was edited and
nothing was committed. Scratch scripts: `/tmp/claude-0/-home-user-ELISA/ae894b80-90ba-5a23-9111-4ab00d596982/scratchpad/review/`
(§5). Tags: **Derived** (arithmetic shown or in a named scratch script), [assessment], **UNVERIFIED** (not checked
against a source in this session), **V** = vendor page opened and checked by the reviewer this session (§4).

## 1. Verdict

The design is a **usable basis for a C2 prototype with two blockers and seven significant corrections**. Geometry and
the interface are consistent: the committed outputs rebuild bit-identically. Interface numbers agree across the
modules apart from a few stale Rev A remnants. The catalogue parts sampled exist and match their cited figures.
What matters most:
1. **B1** The paper carry-over budget (docs/13 §8.3: worst 9.6×10⁻⁵, 4×10⁻⁶ under the 1×10⁻⁴ criterion) no longer
   closes once its allocations are scaled with the as-built wetted areas (P_in line ×1.69, C_k ×5.4, tidal coils ×2.5):
   ≈ **1.1×10⁻⁴**. docs/23 lists DEV-1/DEV-B1/DEV-B2 as "absorbed by E1.10/M7" and does not say this.
2. **B2** The reagent cold zone as drawn cannot hold 4–8 °C. The 1-mm PEEK side walls of the cold block are discounted
   by an unexplained factor 0.1, and the −x wall is omitted. The real leak is ≈ 7.1 W, not 1.16 W. The required heat
   sink is 0.32–0.50 K/W, not 0.94 K/W, and that is not reachable with the drawn 32 × 37 mm sink and 25-mm fan.
3. Gate sealing margins are thinner than stated. The G1–G4 land overlap is **negative** in the worst case once kerf
   and thermal shift are added (S1). The 19 µm vs 20 µm foil-deflection "pass" uses a circular-plate formula; a long
   clamped strip gives ≈ 26–30 µm (S2). The spring forces are computed at a closed tip height that cannot occur; at
   the real height the 2.5-N valves exceed the 3.0-N limit with +10 % spring tolerance (S3).
4. The face seal leaves an **unswept 0.11 µL annulus** at every port, including P_in (S4). This contradicts "no anvil
   bore volume is added".

## 2. Findings table

| ID | Location | Finding | Evidence | Required action | Owner |
|---|---|---|---|---|---|
| **B1** | docs/23 §9 DEV-1, DEV-B1, DEV-B2; docs/22 §13; docs/13 §8.3 | The physical deviations enlarge three carry-over paths. Re-scaled with wetted area, the docs/13 worst-determination sum rises from 9.6×10⁻⁵ to ≈ 1.1×10⁻⁴ > 1×10⁻⁴ (a fixed user criterion). docs/23 does not state that the paper budget is now open. | `carryover_seal.py`: area ratios: P_in line + M_in 1.69 (0.523 m × Ø0.127 + 15.7 mm M_in vs 0.3 m + 12 mm), C_k 5.4 (16.2 vs 3.0 mm), coil 2.5 (≈ 150 vs 60 µL of Ø0.508 FEP). Re-scaled sums: consecutive 8.9×10⁻⁵, same chamber 2.1×10⁻⁵ | State it in docs/23 §9/§10 as a top open item. Re-close the budget by design: 0.102-mm-ID P_in line (docs/22 option); S_IC1/S_IC2 beside the bay (docs/22 §15, coils → 60 µL); shorter C_k (or 5 µL chases per docs/18 DEV-1). Or have the user accept that 1×10⁻⁴ rests on E1.10/M7 | docs, base, card |
| **B2** | `dock_lower/calcs.py thermal()` line 198; docs/21 §5.4, CHOICE-L4; docs/18 §8 (10.6 W exhaust) | The cold-zone heat load is under-counted ≈ 3×. The PEEK U-frame is 1.0 mm thick on three sides (`geom.COLD_CUTOUT`/`COLD_PLATE`), but the code multiplies the ±y walls by 0.1 and omits the −x wall. The heat sink required is 0.32–0.50 K/W, which a 32 × 37 mm sink with a 25-mm fan cannot provide [assessment] → reagent zone not at 4–8 °C, conjugate stability (docs/13 §5.2) lost | `calc_checks.py` §4: ±y walls 2.76 W + −x wall 3.45 W + x 20–24 strip 0.86 W = **7.07 W** (k_PEEK 0.25, ΔT 20 K, 15 deep) vs 1.16 W. Total load 8.5 W (design ×1.5: 12.8 W) → TEC 1.7–2.2 A, P_el 11.7–18.7 W, Q_hot 20–32 W | Thicken the PEEK break (≥ 4 mm on all sides) or relieve the anvil around the cold block (air gap and foam). Recompute; size the heat sink (heat pipe to the rear, docs/21 §10) and the LOWER exhaust (docs/18 §8 says 10.6 W). Anvil heater budget +6 W | lower |
| S1 | interface `TOL`; docs/19 §5, §6.4; docs/23 O-1 | The G1–G4 lateral land overlap is 0.15 (Ø0.8 tip on a 0.5 lane) against a 0.14 worst-case error. The 0.14 omits the laser-kerf width tolerance, the cold-zone and CTE shift, the guide-hole position and the pin play. With these included the worst-case overlap is −0.01 to −0.02 mm (RSS still +0.06) | `calc_checks.py` §2: overlap per valve. G1–G4 0.150, V11/V12 0.20, all others ≥ 0.25. Cold-zone contraction 20 mm × 60×10⁻⁶ × 20 K = 0.024 [assessment, α_COC UNVERIFIED]; COC vs Al head 20 → 25 °C at x 55: 0.010 | Narrow the lanes locally to 0.40 under G1–G4 (overlap 0.20), or make the gate pins/tips Ø0.9 in Ø1.2 bores (clearance 0.15). Add kerf, thermal and head-side terms to `TOL` | interface, card |
| S2 | docs/21 §5.1; docs/19 §6.4; docs/23 §4.3, O-2, DEV-L4 | "19 µm ≤ 20 µm (M4 acceptance)" uses the clamped *circular* plate w = Fa²/(16πD) with a = 2.22. The slot is a long strip. For a long clamped rectangle under a central load the coefficient is ≈ 0.0072–0.0079 P b²/D (Timoshenko, recalled, UNVERIFIED) vs 0.00497 for the circle → **26–30 µm at 4.44**, 22–25 µm at 4.0 | `calc_checks.py` §1: D = 7.72×10⁻³ N·m (E 2.6 GPa, t 0.315); circle 19.1 µm, strip 30.3 µm; with E 3.2 GPa (TOPAS TDS, V) 15.5 / 24.6 µm | Do not present 19 µm as a pass; state the model range (15–30 µm). Make the M4 slot variant decisive. Prefer to remove DEV-L4 at G1/G2: round holder + Ø2 × 4 magnet (docs/23 I-7 alternative), or a local slot width ≤ 4.0 there | lower, docs |
| S3 | docs/20 §2.3, §4.1, §4.2; interface `PLUNGER tip_z_closed` 0.17; docs/23 I-13, O-5 | All closing forces and cylinder margins are computed at tip z 0.17. A tip wider than the channel cannot go below the land top + compressed TPE. Rigid translation of the TPE column by 0.175 puts the real closed tip near z ≈ 0.54 (+0.37). I-13 fixes only the hook gap, not the preload | `calc_checks.py` §3: dz 0.20–0.37 → slot 1.29–1.36 N (+10 %: 1.42–1.50, limit 1.5); Ø0.8 anvil (k 1.342) 2.77–3.00 N (+10 %: **3.05–3.30 > 3.0**); Ø1.2 anvil 2.71–2.89 N (+10 %: 2.98–3.18). V14 cylinder margin 1.60 → ≈ 1.45 at 400 kPa, ≈ 1.27 at the 350-kPa trip [Derived from docs/20 §4.2 need = 6.6 N] | Set the preload shims on the reference card at the real closed height (extend I-13 to preload), or lower the nominal preloads/spring rates. Re-run `calcs.py` at a measured closed height; add a tip-height measurement to M4 | upper |
| S4 | interface `FACE_SEAL` (tube OD 1.5875, gasket ID 1.7, counterbore 0.38); docs/18 §6 "No anvil bore volume is added"; docs/21 §3 | The bonded tube sits inside the gasket ID, leaving an annulus 0.056 wide × 0.38 deep at every port, open to the port at the foil whenever the PEEK tube face does not seal hard against the COC foil. It is unswept (diffusion only) | `carryover_seal.py`: 0.110 µL per port (port hole 0.247 µL); IgG diffusion time across 0.38 mm ≈ 1850 s (≈ 1 cycle). At P_in it is a sample reservoir on path 2 (allocation 1×10⁻⁵): order-of-magnitude release 10⁻⁵ [assessment, UNVERIFIED] | Make the gasket ID ≤ tube OD (seal on the tube face), or let the gasket seal the foil directly around the Ø1.0 hole with the tube below it. Correct the docs/18 sentence | interface, lower |
| S5 | docs/23 §5, §10; docs/21 CHOICE-L19; docs/13 §5.2, §8.1 | No docking timeline exists for the physical dock. The 14-run cap assumes first inject ≈ 12 min after insertion (slack to 8 h: 8 min → docking ≤ 20 min keeps 14). The dock adds steps: reagent Peltier enabled only after the lid closes (cold block pulled down every card); cold-box door opened per card (10-min pull-down, docs/22 §7); 15.1 mL prime; leak test 11 ports × 30 s if sequential (5.5 min); ≥ 10 min equilibration; fills on one shared Flow EZ channel | Fill estimate (Derived, Hagen–Poiseuille, 0.254 × 360 mm FEP at 34.5 kPa): RS 0.6 mL ≈ 55 s, RCj 0.26 mL ≈ 25 s, sequential on ch2 | Write the docking sequence with times in docs/23, decide parallelism (leak test vs equilibration vs prime), and verify it at C2 | assembly, docs |
| S6 | docs/23 §7; docs/22 §9.5 | The Gamry cell cable SKU 985-00071 (60 cm) is listed by Gamry for the **Reference 600 and Interface 1000/1010**, not the Reference 600+ (V, orders.gamry.com). docs/22 marks it "verified" for the 600+ | WebFetch of the cited page | Mark the compatibility UNVERIFIED; confirm the 600+ cable and the connector before the bulkhead design (`PASS_THROUGHS['gamry_cell_cable']`) | base |
| S7 | docs/23 §9 DEV-B1; docs/22 DEV-B1 | Volume between loop and chamber: 3.8 + 0.6 + 0.26 = 4.66 µL (docs/13 §2.6) → 7.6 + 1.37 + 1.42 = **10.4 µL**. The fixed 150 µL push therefore clears ≈ 5.7 µL (0.057 loop volumes) less of the loop. The analyte-transfer fraction 0.90 (and the ×1.11 capture gain, docs/13 §3.1) falls, magnitude UNVERIFIED (order 1–2 % [assessment]). docs/22 mentions a re-check; docs/23 omits it | Derived from `tubing_schedule.csv` and docs/18 DEV-1 | Add it to docs/23 §9 with the model input it changes (transfer fraction) and the test (C1 gravimetric/M2), or lengthen the push accordingly (time cost) | docs |
| M1 | docs/20 §4.5 | V3 is energised while **closed**, and docs/13 §4 says it is closed only −3.45 → 3.35 (6.8 min per run). docs/20 writes "all of the run except 6.8 min" (inverted) → pilot heat 1.14 W overstated (harmless) | docs/13 §4 table | Correct the text and the number | upper |
| M2 | docs/20 §2.5 | The SS073B01 length formula is mislabelled. Catalogue (V): L1 = n × 7.2 + 8.8, L2 = n × 7.2 + 14.8. docs/20 writes L1 = n × 7.2 + 14.8 (94.0 / 86.8 = L2, overall) | S070.pdf p. "SS073B01 Dimensions" | Relabel as L2 (overall), check the envelope | upper |
| M3 | Stale Rev A remnants | `interface.py` l. 111 `DATUM_PIN_D` "hardened steel" (now zirconia, docs/21 CHOICE-L9); l. 432 `cylinder_pitch_min` "bore 5"; docs/21 §5.7 "bore 6 at 300 kPa" (supply now 400); docs/18 §6 table P_b "S_b outlet 0.25 ID" (built 0.102, DEV-B3); docs/18 §8 `BASE_cold_compartment` "S_b" (S_b is in the rear pump row); docs/22 §3 partitions "321–323" (code `PART_X` 323–325) | grep (§5) | Update the comments and texts | interface, lower, base |
| M4 | docs/22 §1/§6/§13, docs/23 §5 | Internal number drift: prime 14.9 vs 15.1 mL; P_in "8.0 + 1.05" vs 7.6 µL; flush 25 vs 26 line volumes; 0.102-ID option 5.1 vs 4.9 µL (Derived 4.3 µL + 1 µL sensor = 5.3) | reading | Harmonise from `calcs.py` output | base, docs |
| M5 | docs/22 §9.1 vs docs/21 CHOICE-L16 | BASE lists a **stepper driver** for the pogo lift, while LOWER uses a pneumatic cylinder. No pilot valve for the pogo cylinder (or for the 3/2 fill valves) is allocated in BASE's valve driver (21 channels = lid only) | reading | Allocate the solenoid(s) and drivers; drop the stepper | base |
| M6 | docs/23 §9 DEV-4 | "magnet gaps and forces unchanged" with M_h deleted is unsupported. The hold magnet changes from 3×3×4 fixed (gap by geometry) to 2×2×4 on a stage with a gap chain of WC 82 µm / RSS 32 µm (docs/21 §5.2, O-9). The pellet footprint under WE1 changes | docs/13 §3.3.1 vs docs/21 §5.2 | Replace "unchanged" with the actual change; put the pellet footprint and hold under M1/M5 | docs |
| M7 | docs/21 §5.6 | Bead-out 4.55 mm at 0.20 mm/s = 22.8 s, plus G4 opening (≈ 0.06 s) and M_d Z-down (cam 0.5 s [assessment]) → **23.3 s of the 24-s window** (0.7 s left, not 1.2 s). Nothing slips past PE1 of n+1 (2.45 min slack), but the step table needs the Z-down inside the window | `calc_checks.py` §5 | Account for the Z stroke, or start the bead-out at 56.75 with the gate pre-opened | lower |
| M8 | `assembly/checks.py INTENDED` | The cross-module "0 unintended" uses blanket allow rules (pin × L1/L2, pogo × die, gasket × L0, tube × tube) with no volume bound. A wrong pin length or a pogo over-travel would be classified "intended". The feature checks cover position, not volume | code reading | Fail when an intended overlap departs from its expected volume (e.g. gasket 0.754 ± 10 %) | assembly |
| M9 | `cad/requirements.txt` | `ezdxf` is imported by `card/build.py` but missing from requirements.txt (README says `pip install shapely ezdxf`) | grep | Add `ezdxf` | assembly |
| M10 | docs/20 §2.1 | Lid lock during a run is software-only. The draw latches can be opened mid-run, the card then lifts off 11 seals (spill onto the anvil and electrode bay); only the latched switch reacts | docs/20 §2.1 | For C2 add a latch-closed solenoid lock or at least a latch-open → safe-state test in the commissioning list | upper |
| M11 | docs/19 §5, docs/23 O-1 | The L1-to-L3 budget WC 0.051 > 0.05 relies on laser position 0.010 and post-bond shrink 0.05 % (both UNVERIFIED). The ranking as O-1 is right; S1 adds to it | docs/19 §5 | Coupon test of shrink before the 10–20-card order | card |
| M12 | docs/21 §4 | Pogo spring material is not stated on the PTR 1007.70 page (V); if steel, it sits 5.6 mm from the M_d hold magnet (5.1 mT at the pads). Static, but it should be an incoming check like the other non-magnetic parts | V | Ask PTR for a non-magnetic spring option or include it in the μr incoming check | lower |
| M13 | docs/21 §4 | supermagnete Q-10-10-05-N page (V) lists N42 in the data table but mentions N48 in the description; B_r not on the page | V | Keep B_r UNVERIFIED; fix the grade on order | lower |

Counts: **2 B, 7 S, 13 M.**

## 3. Details

### B1 — carry-over budget
docs/13 §8.3 closes at 9.6×10⁻⁵ against 1×10⁻⁴: consecutive 8.2×10⁻⁵ + same-chamber 1.4×10⁻⁵, a 4×10⁻⁶ margin. Three of
its allocations are areas or volumes that the physical design enlarged:
- path 2: PEEK line + M_in, 1×10⁻⁵;
- path 3: C_k, 1×10⁻⁶;
- path 5: coil, 2×10⁻⁶.

Scaling only those three with wetted area (`carryover_seal.py`) gives 1.1×10⁻⁴; the P_in line alone (+0.69×10⁻⁵)
already exceeds the margin. The scaling is an assumption (the allocations are themselves UNVERIFIED placeholders), but
the direction is certain. docs/23 §9 maps the deviations to "E1.10, M7", which hides that the paper budget, the
document's own basis for "≤ 1×10⁻⁴", no longer closes. The cheapest restorations are already in the documents:
- 0.102-mm-ID P_in line: area ×0.8 of the 0.127 line at the same length; 2.5× ΔP upstream of the card, harmless for
  the BSM.
- S_IC pumps beside the bay (docs/22 §15).
- A shorter C_k rail, or 5 µL chases.

### B2 — cold zone
`geom.COLD_CUTOUT` x 0.6–24 / y 1–49 and `COLD_PLATE` x 1.6–20 / y 2–48 leave 1.0 mm of PEEK on the −x, +y and −y
sides. Everything outside that wall is the 25 °C anvil (x −15…91). `calcs.thermal()` computes
`k_peek·2·(20e-3·15e-3)·ΔT/1e-3·0.1` for the y walls (×0.1 without a source tag) and has no −x wall term. Recomputed
(k 0.25 W/m·K UNVERIFIED as docs/21):

| Term | Recomputed |
|---|---|
| y walls | 2.76 W |
| −x wall | 3.45 W |
| break strip | 0.86 W |
| PEEK total | 7.07 W |
| total load with the other docs/21 terms | 8.5 W |

The TEC model of `calcs.py` (datasheet maxima V: Imax 4.0 A, Qmax 33.4 W, Vmax 15.4 V, DTmax 67 °C) at Th 35 / Tc 3 °C
gives I 1.72 A, Q_hot 20.2 W → R_th ≤ 0.50 K/W; at the ×1.5 design load, 0.32 K/W. docs/21 asks 0.94 K/W of a
"32 × 37 base, 25 × 25 × 10 fan" sink. Even that is optimistic for the size [assessment]; 0.3–0.5 K/W is not
achievable there. Either the leak is cut (≥ 4 mm PEEK or an air gap with foam around the cold block) or the heat
rejection is moved (heat pipe to a rear sink). The front exhaust duct/louvre (docs/18 §8, docs/22 §10) and the anvil
heater (10 W, now with +6 W of leak) must follow.

### S1 — gate land overlap
Chain in docs/19 §5: 0.03 head-to-nest + 0.01 datum pin + 0.05 L3 edge-to-feature + 0.05 L1-to-L3 = 0.14. Missing
terms:
- laser kerf/width tolerance of the 0.5 lane: ±0.02 on the width → 0.02 per side [assessment];
- guide-hole position in the CuSn8 plates relative to the head guide pins: ±0.005–0.01 (docs/20 §3.1);
- pin play: 1–6 µm;
- cold-zone contraction after clamping (the reagent zone is cooled *after* the lid closes, CHOICE-L19): ≤ 0.024;
- CTE of COC vs the Al head over 5 K: 0.010.

Worst case 0.17–0.20 > 0.15 overlap. A flat-floor TPE valve needs positive land on both sides to seal the corner of
the 0.175 channel (docs/13 §2.4). The fix costs nothing in function: lanes 0.40 wide under the gates (drag lane
elsewhere unchanged), or Ø0.9 gate tips.

### S2 — foil deflection
The circular-plate formula is docs/13's own, but docs/13 used it at 4.0 mm with a 5 µm margin. At 4.44 mm the margin
becomes 1 µm, and the boundary model alone changes the result by ×1.45–1.6. The TPE/L3 backing may stiffen the real
laminate, so the answer is M4, but "≤ 20 µm" must not be reported as met. The I-7 alternative (round holder, Ø2 × 4
magnet) removes the widening at G1/G2. It changes docs/13's M_d magnet and needs the user's consent only if the
docs/13 number is considered fixed (it is not one of the docs/16 §2 decisions).

### S3 — closing force at the real tip height
The interface comment itself says `tip_z_closed` = "TPE pressed onto the foil top less ~30 µm residual TPE". That is
only possible for a tip narrower than the channel. Here every tip is wider (overlap 0.15–0.30). Over the lands the
TPE can only be compressed. The lowest physically possible tip height is the land top 0.315 plus the compressed TPE
thickness. The volume-conserving estimate (the TPE column over the channel translates 0.175 into the channel, the
lands compress 44 %) gives z ≈ 0.54. With the docs/20 spring rates the force at that height exceeds the docs/13 3-N
limit for the 2.5-N classes at +10 % tolerance (table §2). docs/20 states that "the preload is shimmed per pin" but
not at which height; I-13 sets only the hook gap on the reference card. 44 % compression of a 0.40 mm TPE on the
lands is also a durability question for M4 (endurance 100 cycles).

### S4 — face-seal annulus
Tube OD 1.5875 inside gasket ID 1.7: radial gap 0.056 mm, height 0.38 mm at 24 % compression → 0.110 µL per port.
The "tube end faced flush with z 0" (docs/21 §3) makes the PEEK tube face bear on the foil around the Ø1.0 hole. Two
hard surfaces do not reliably seal, so the annulus is wetted and unswept. At P_in it holds sample. A diffusion
exchange time of ≈ 1850 s (IgG, 0.38 mm) means about one cycle, so a fraction of each run's sample reaches the next
run's transfer window. With the 4×10⁻⁶ budget margin (B1) this cannot be waved away. Fix in the interface: gasket ID
1.5 (sealing on the tube OD and the foil), or tube recessed 0.1 below a gasket that seals directly on the foil around
the hole (gasket ID ≈ 1.2).

### S5 — docking timeline
docs/13 §5.2 gives the cap (12 + 13 × 31 + 56.75 = 472 min ≤ 480) and calls the docking time UNVERIFIED for C2. The
physical round adds four constraints: the Peltier interlock, a cold box opened per card, a 15.1 mL prime, and the
sequential fills. None of docs/18–23 lists them on a time line. The cap survives a docking of ≤ 20 min.

## 4. Sourcing audit (sample of 30; "V" = opened by the reviewer this session)

| # | Item | Document | Claimed | Found | Status |
|---|---|---|---|---|---|
| 1 | Zaber X-LSM050A travel | docs/18 §7, docs/21 §4 | 50.8 mm | 50.8 mm (zaber.com spec page) | V ✓ |
| 2 | X-LSM050A repeatability / accuracy | docs/21 §4 | < 3 µm / 20 µm | same | V ✓ |
| 3 | X-LSM050A speed range | docs/21 §4 | 0.000029–26 mm/s | same | V ✓ |
| 4 | X-LSM050A thrust, flatness, straightness | docs/21 §4 | 25 N, < 11 µm, < 14 µm | same | V ✓ |
| 5 | X-LSM050A non-back-driving, 0.34 kg; footprint | docs/21 §4 | as stated; footprint UNVERIFIED | same; footprint not on page; built-in controller (relevant to EMI, §6) | V ✓ |
| 6 | PTR 1007.70 pitch, full travel | docs/18 §7, docs/21 §4 | 1.27 / 1.27 | same | V ✓ |
| 7 | PTR 1007.70 forces | docs/21 §5.7 | 0.50 N preload, 1.40 N at full travel | same; working-travel force not on the page (1.21 N is a linear interpolation, Derived) | V ✓ |
| 8 | PTR 1007.70 drill, plunger | docs/21 §4 | 0.87 (0.95 ring), CuBe Au | same; spring material not stated | V ✓ |
| 9 | CTE 12711-5L31-04CL | docs/21 §4 | Imax 4.0, Qmax 33.4, Vmax 15.4, DTmax 67 | same (PDF text) | V ✓ |
| 10 | supermagnete Q-10-10-05-N | docs/21 §4 | 10×10×5 ± 0.1, N42, Ni-Cu-Ni, 80 °C, ≈ 27.5 N | same; page also says N48 in the text; B_r absent | V ✓ (M13) |
| 11 | SMC S070B-5DG meaning | docs/20 §2.5 | 24 VDC, 0.5 W, 0.5 MPa | B base mounted, 5 = 24 VDC, D = 0.5 W / 0.5 MPa / Cv 0.011, G grommet | V ✓ |
| 12 | S070 0.5 W flow / response | docs/20 §2.5 | C 0.042, ≤ 3 ms | C 0.042, b 0.27, ON/OFF ≤ 3 ms at 0.5 MPa | V ✓ |
| 13 | S070 0.35 W limited to 0.3 MPa | docs/20 §2.5 | yes | yes; 0.1 W holding option 0.3 MPa | V ✓ |
| 14 | S070 width, weight | docs/20 §2.5 | 7 mm, 5 g | same | V ✓ |
| 15 | SS073B01 pitch, max stations, length | docs/20 §2.5 | 7.2, 20, L1 = n·7.2 + 14.8 | 7.2, 20; L1 = n·7.2 + 8.8, L2 = n·7.2 + 14.8 | V ✗ label (M2) |
| 16 | Kipp K0045.1541092 | docs/20 §2.7 | stainless form A, F1 2000 N | K0045.1541092 form A, F1 2000 N (stainless column of the K0045 sheet) | V ✓ |
| 17 | Kipp catch plate K0045.9143372 | docs/20 §2.7 | catch plate | listed as catch plate form A | V ✓ |
| 18 | Omega KHLVA-0502/5-P | docs/20 §3.2 | 12.7 × 50.8 × 0.25, 5 W at 28 V, PSA, 150 °C | same (DigiKey) → 156.8 Ω, 3.67 W at 24 V (Derived, matches 7.3 W for two) | V ✓ |
| 19 | TI DRV5055 | docs/20 §2.6 | SOT-23, 20 kHz, ±21…±169 mT, A = drift compensated | same | V ✓ |
| 20 | Tecan Cavro Centris | docs/22 §5.1 | 44.5 × 68.8 × 184.2, 1.3 kg, 24 V, 2.5 A, RS-232/485/CAN, 16 per bus | same | V ✓ |
| 21 | Centris valves | docs/22 §5.1 | 3/4-port; 3/6/9/12 distribution | same (6/9/12 ceramic only) | V ✓ |
| 22 | Fluigent Flow EZ LU-FEZ-0345 | docs/22 §5.1 | 91.9 × 71.8 × 131, 634 g, supply 1100 (max 1300) mbar | supply ✓ (datasheet/LineUP page via search); size/mass apply to the Flow EZ family; R2 120 kPa lies inside 110–130 | ✓ (search summary of the vendor page; 6 W not checked) |
| 23 | Laird/Tark DA-024-24-02-00-00 | docs/22 §7 | 24 W, 24 V, 2.4 A, 0.3 kg, cold 60 × 40 × 14, warm 80 × 60 × 56 | same (catalogue PDF text) | V ✓ |
| 24 | Gamry Reference 600+ size, mass | docs/18 §8 | 9 × 19 × 27 cm, 3 kg | same; floating yes; page marks the 600+ discontinued (in hand, no impact) | V ✓ |
| 25 | Gamry cell cable 985-00071 | docs/22 §9.5 | 60 cm cable for the Ref 600+ | 60 cm, listed for Reference 600 and Interface 1000/1010 only | V ✗ (S6) |
| 26 | TOPAS 5013L-10 | docs/19 §3 | 1020 kg/m³, Tg 134 °C, 3200 MPa | same (TDS PDF text) | V ✓ |
| 27 | MTC PEEK bend radius | docs/21 §4 | ≥ 25 mm | "smallest recommended bend radius for PEEK tubing is 25 mm" | V ✓ |
| 28 | Sensirion SLF3S-0600F | docs/22 §5.1 | 2 mL/min FS, 48 × 15.5 × 8.9 | ±2000 µL/min ✓ (distributor listings); dimensions not found | ✓ range / dimensions UNVERIFIED |
| 29 | COC E 2.6 GPa, ν 0.35 (foil deflection) | docs/13 §2.1, docs/21 §5.1 | UNVERIFIED | grade-dependent; the TOPAS 5013 TDS gives 3.2 GPa | UNVERIFIED (correctly tagged) |
| 30 | Elgiloy-class G 70 GPa; Nitronic 60 μr; Gent seal constants; Roark α(1.5) 0.0843; k_PEEK 0.25 | docs/20, 21 | UNVERIFIED | not checked | correctly tagged UNVERIFIED |

No invented part number was found among those sampled. Two citations are wrong in detail: rows 15 and 25.

## 5. Independent checks run (repeatable)

Scripts are in `/tmp/claude-0/-home-user-ELISA/ae894b80-90ba-5a23-9111-4ab00d596982/scratchpad/review/`, run with
`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/ELISA/cad python <script>`.

| Script / action | Checks | Result |
|---|---|---|
| `calc_checks.py` | foil deflection (circle vs long strip); tip land overlap per valve from `CHANNELS`/`VALVES`; spring force vs real closed height; cold-zone leak and TEC operating point; bead-out time; head packing (collar/spring/button gaps for all 210 pin pairs) | §2 S1, S2, S3, B2, M7; head packing min collar 0.20, spring 0.30, button 0.30 (V11–V12), as docs/20 |
| `slot_checks.py` | 2.6-sq holder swept at 0.02 mm along both drags and the bead-out vs `slot_polygon()`; local slot chord under each slot valve; anvil tips vs slot; pads vs contact window; holder vs electrode bay | holder clearance 0.300 everywhere (exactly the design value); chords G1/G2 4.40–4.41, V11 3.96, G3/G4/V12 3.40; V15 0.25 to the slot; pads 0.30 margin; holder at RC 2.50 to the bay ✓ |
| `carryover_seal.py` | B1 re-scaling; S4 annulus volume and diffusion time | 1.1×10⁻⁴; 0.110 µL, 1850 s |
| Fresh build from `git archive HEAD cad` in scratch | `interface_plan` (9.7 s), `card.build` (29.6 s), `dock_base.build --fast` (13.9 s), `dock_upper.build --fast` (91 s), `dock_lower.build --fast` (7 min 35 s; README says ≈ 2.5 min) | all ran cleanly. `dock_lower` `calcs.json` identical and `checks.json` identical except the `md_sweep` block that `--fast` skips. `card/checks.json`, `dock_base/check_results.json`, `tubing_schedule.csv` **byte-identical** to the committed files; `dock_upper` `checks.txt`/`calcs.txt` identical except timing lines (0 unintended interferences, closed and raised) |
| Analytic recomputation | cell 1.04 + 0.05 + 0.065 + 0.145 + 0.012 = 1.312 µL; IC π·4²·5.575 − 1.2 = 279 µL; M_c swing drift R − √(R² − 5²) = 0.194 at R 64.5; park drop 64.5·sin 45° = 45.6, offset 18.9 | all match docs/19 §6.1 and docs/21 ✓ |
| `git ls-files`, `du` | committed caches, size | no `__pycache__` or `.pyc` committed; `cad/out` 59 MB as stated; `ezdxf` missing from requirements (M9) |
| grep for Rev A remnants (`300 kPa`, `bore 5`, `250 N`, old guide pins, `M_h`, `hardened steel`, `-1.0`) | stale numbers | only the items of M3 (everything else is in explicit "was …" history) |

## 6. Not reviewed, and why

- **Full `assembly.build` (≈ 22 min) and the `--all-states` outputs** were not regenerated. The committed assembly
  checks were read (`checks.json`) and the module checks were reproduced. The cross-module "0 unintended" result
  therefore rests on the committed run, qualified by M8.
- **Renders (PNG)** were not inspected; docs/23 states they were post-processed (palette) after the build.
- **Magnetics** (`mag_b.py` forces, 1.9 mT at the relay, M_w/M_d 0.245 N) were not recomputed. Order-of-magnitude
  dipole check of 1.7–3.4 mT at 31 mm from a 10 × 10 × 5 N42 block is consistent [Derived, dipole approximation].
- **The docs/13 functional model** (P(success), escape, capture) was not re-run for DEV-C2/C4, S7 or the M_h removal.
- **Seal-force physics** (Gent form, TPE strain–force) and the pneumatic dynamics (22–59 ms) were not recomputed
  beyond S3.
- **EMI**: not quantified. Points that need M5a: the Zaber stages carry built-in controllers (V) about 60–120 mm below
  the electrode bay and stay powered during reads with the drivers disabled. Hall ICs and their ADC are polled during
  reads.
- **Priming and debubbling of dead-ends near the cell** (G3/V14/V15 stubs, WE2 channel, CE/RE pocket) is docs/13 §8.1
  territory and has no physical-design counterpart in docs/18–23 (UNVERIFIED).
- The M_d sweep of `dock_lower` (skipped by `--fast`) was not re-run. The holder-in-slot clearance was re-checked in
  2-D (`slot_checks.py`).

## 7. Questions only the user can answer

1. **Carry-over (B1):** should the physical design be changed until the paper budget closes again? The options are a
   0.102-mm P_in line, S_IC pumps beside the bay (larger footprint near the bay) and a shorter C_k. Or do you accept
   that the 1×10⁻⁴ criterion is demonstrated only by E1.10/M7 on the C2 hardware?
2. **Cold zone vs footprint (B2):** a heat sink of 0.3–0.5 K/W does not fit the front duct space. Do you accept a
   heat pipe to a rear sink (rear depth/height grows) or a thicker insulating break (cold block smaller, reagent zone
   unchanged on the card)? Your instruction was to minimise footprint.
3. **Gate geometry (S1/S2):** may docs/13 numbers change locally? The candidates are lanes 0.40 wide under the gates,
   Ø0.9 gate tips, or a round M_d holder with a Ø2 × 4 magnet (the alternative to the widened slot, I-7). docs/13 is
   not edited; each would be a listed deviation.
