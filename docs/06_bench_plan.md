# 06 — Staged bench plan (Task 5)

> **Revised after the final review (docs/08 §10).** The G1 decision rule is now one rule on the model P(success)
> evaluated with the bench values entered, fixed before any data (§4.11, B3); an early gate G1a at week 5 applies it
> to U1 + U3 (§4.10, S8); beads and conjugate have separate reservoirs and E1.3 has a reservoir-ageing arm (B4); the
> Stage-3 default detector is a commercial single-channel thin-layer cell, the IDA and second channel are bought only
> if Stage 2 shows a need (S9); the carry-over criterion is 1×10⁻⁴ with a 10 ng/mL challenge (S6). Revised passages
> are marked "(revised after final review)". Model numbers quoted here are the revised ones (thin-layer cell, S13
> corrections, K_i override); docs/05 numbers are kept only where marked "docs/05".

Status: 2026-11-11. Inputs: docs/00–05, `params/*.yaml`, `results/design/`, `src/elisa_sim/`. This document plans
the bench phase for the design chosen in docs/05 (primary: renewable streptavidin magnetic beads, SIA dispenser
and stirred in-line cup, bead trap on the 10-port isolation valve, ALP/HQDP, a commercial single-channel thin-layer
cell by default (flow IDA on two potentiostat channels only if Stage 2 shows a need — revised after final review);
in-platform fallback: sequential mode; backup: fixed packed micro-bed). Purchases are listed by stage in
`docs/07_bill_of_materials.md`; the lab-PC software is in `automation/`.

Conventions. "Model" numbers come from the audited model and docs/05 (Monte Carlo scenario ranges, not confidence
intervals). Gate thresholds are quoted from docs/05 with the section; thresholds that are **derived in this
document** are marked "(derived here)" with the reasoning. Anything not checked against a source is UNVERIFIED.
Tiers: **T0** = no flow system (tubes, magnet, rotator, a drop on a screen-printed electrode with the Gamry);
**T1** = Waters stack with simple plumbing (BSM → SM-FL → commercial cell → TUV → waste, no external valves);
**T2** = purchased valves/syringe pump/simple trap on the Waters stack; **T3** = full custom primary platform.

---

## 0. Summary

| Stage | Tier | Weeks (from start) | Resolves | Gate | Bought only after the gate passes |
|---|---|---|---|---|---|
| 0 Set-up and facts | T0/T1 | 0–2 | instrument facts, noise floor, PC, vendor answers | G0: lab PC runs the simulated cycle; Inject Start seen; Stage-1 reagents in hand | Stage-1 reagents are ordered in week 0 (they gate everything) |
| **1 Reachability** | **T0 + T1** | 2–8 | **U1** conjugate NSB (+ reservoir ageing), **U3** free HQ, **U2** off-rates, detection-on-capture, U6, U9, SM-FL recovery, a tube-format integrated blank-equivalent | **G1a (wk 5, U1 + U3) and G1 (wk 7–8): GO / GO-WITH-LEVER / STOP on model P(success)** (revised after final review) | valves, SIA pump, magnet actuator, prototype cup and trap parts (Stage 2); BLI/SPR service and NISTmAb only after G1a |
| (1A, informational) HQDP pre-electrolysis test E1.2b (added 2026-11-12) | T0 | 5–7 | whether pre-electrolysis removes free HQ to ≤ 1 % without side effects (docs/12 "guard cell") | none; not a G1a/G1 input; outcome decides at G1: guard cell considered at Stage 2 / kept in the cartridge design / dropped | nothing (no guard cell in the hardware before the result) |
| 1C Immune-complex transfer (conditional) | T0 | +3–4 | U8 | adopt / abandon L4 | second trap position, elution line |
| 2 Flow path on the Waters | T2 | 8–16 | U5 dosing/trap, U4 wall NSB, cup transfer, first in-flow blanks | **G2: build primary / go to backup** | commercial thin-layer cell, machined cup, integrated trap (Stage 3) — or the backup bed parts; custom IDA cell and second potentiostat channel **only if** G2 shows electrochemical noise is a material part of the blank SD (revised after final review, S9) |
| 3 Full primary platform | T3 | 16–28 | **U7** integrated blank statistics, unattended operation; IDA gain and two-channel readout only if bought | G3: start validation | nothing new (validation consumables) |
| 4 Validation | T3 | 28–32 | the success criteria of docs/00 | final report | — |

**What Stage 1 decides.** docs/05 §0 and §3 show that two measurements decide whether 1 pg/mL is reachable at all,
for every format: the IgG–ALP conjugate NSB on blocked streptavidin beads (U1) and the free hydroquinone in the HQDP
lot (U3). They are entered into the model at G1a (week 5) and the single decision rule of §4.11 is applied to the
resulting P(success): GO ≥ 0.30, GO-WITH-LEVER 0.10–0.30, STOP < 0.10 (revised after final review, B3/S8; fast
screens: label factor ≤ 0.02 GO, > 0.10 STOP; free HQ ≤ 10⁻⁵ accept, > 10⁻⁴ after purification STOP). Both are measured in Stage 1 in tubes,
with a magnet and the Gamry, plus the Waters stack only as a flow-injection electrochemical (FIA-EC) reader with a
purchased wall-jet cell. No valve, pump, cup, trap or custom cell is bought before G1.

**Stage 1 cost.** About 6 weeks of one bench scientist (≈ 25 bench days, schedule §10; + 4 days for the
informational E1.2b, added 2026-11-12), plus 1–3 weeks lead time
for reagents. Purchases: antibodies (capture, two detection conjugates, non-immune IgG), streptavidin beads, a
magnet rack, IgG-free BSA, HQDP (Metrohm DropSens), HQ standard, NISTmAb and a polyclonal human IgG standard,
screen-printed electrodes with connector and a wall-jet flow cell, a small divided bulk-electrolysis cell with
carbon working, counter and reference electrodes and benzoquinone (E1.2b), LoBind tubes and low-binding vials, a USB DAQ for
Inject Start, plus an external BLI/SPR service (docs/07 §0–1). Indicative list prices seen in this session (not
quotes): NISTmAb ≈ 1 900 USD, magnet rack ≈ 880 USD, M-280 beads 2 mL ≈ 590 USD (offer ended 2024), IgG-free BSA
50 g ≈ 570 USD; all other prices (antibodies, HQDP, electrodes, flow cell, DAQ, BLI service) were not checked.
No instrument-class item is bought in Stage 1.

**Long-lead items** (quote in Stage 0, order at the gate): machined stirred cup and integrated trap (4–6 weeks,
UNVERIFIED), IDEX valves and Hamilton/Tecan syringe pump (lead time UNVERIFIED), a commercial thin-layer flow cell
(lead time UNVERIFIED). The custom IDA flow cell (8–12 weeks, UNVERIFIED) and a second potentiostat channel are
**conditional** Stage-3 items: quoted in Stage 2, ordered only if G2 data show that electrochemical noise is a
material part of the blank SD (model, `results/design/final_designs_ida.md` vs `final_designs.md`: the IDA gains
0.02–0.05 in P over a thin-layer cell as specified today, but 0.07–0.09 for the one-step chamber and up to 0.18 for
the sequential chamber once reagent screening and the other levers pass; so the IDA is worth more if Stage 1 goes
well, and the G2 noise data decide). Gamry's bipotentiostat page (re-read 2026-11-11) lists Interface
1010/5000 pairs, Reference 620 + 620, 3000 + 3000 and 620 + 3000; it names the Reference 600+ in its specifications
section and shows a video "Bipotentiostat with 2 600+ Potentiostats"; a 600+/620 mixed pair is not shown (docs/08
§9 C11; ask Gamry, S0.2) (revised after final review, S9).

---

## 1. Planning principles

1. **Order by value of information per unit effort** (docs/05 §5): U1 and U3 can each kill the target for every
   design; they are cheap (tubes, days). U2 decides the operating mode and removes the largest single sensitivity.
   Everything that only chooses between hardware variants (U4, U5, IDA vs thin layer) waits until G1 has passed.
2. **Measure the model's inputs, not just "the LOD".** Each experiment returns a number in the units of a YAML
   key; `python -m elisa_auto.model_feedback` re-runs the final designs with the bench value and its uncertainty
   (§9). The model then picks the next experiment (largest remaining sensitivity) and the operating mode.
3. **Scale the readout, not the physics.** NSB per unit bead area is what U1 needs. Using 10× the design bead number
   raises the signal 10× without changing the quantity measured (conjugate is never depleted: 0.1 nM × 200 µL =
   1.2×10¹⁰ molecules ≫ 10⁶ bound). One arm at the design bead number checks proportionality.
4. **Calibrate with the label itself.** Enzymes per bead are counted against a dilution series of the same
   conjugate lot in the same substrate, volume, time and readout. This cancels k_cat (UNVERIFIED for HQDP), HQ air
   oxidation and electrode sensitivity, and the conjugate's molar mass (it enters both N and C, so the label factor
   is independent of it).
5. **Replicates are sized from the statistic the gate needs** (§12), not by habit.
6. **Contamination hygiene from day 1** (§8): human IgG is the analyte and is on every lab surface (Parry1997).
7. **No manual step survives into the product.** Manual tube steps are allowed only as measurement tools in Stages
   1–2 (docs/05 §4.3 says the developer-mixed vial is a bench tool, not a deliverable).

---

## 2. Stage map, dependencies and what is bought when

```
Stage 0 (wk 0-2) --order Stage-1 reagents (wk 0)--> Stage 1A T0 tubes/drop (wk 2-7)
        \--quotes only for Stage 2/3 items           Stage 1B T1 FIA-EC on Waters (wk 3-7)
         \--BLI/SPR service booked (wk 0)  --------> U2 results (wk 4-7)
                                                      |
                         G1a (wk 5: U1 + U3 + reservoir ageing) --STOP--> Stage 1C (L4 in tubes) --> G1'
                                                      | GO / GO-WITH-LEVER: book BLI/SPR, order NISTmAb
                                                    G1 (wk 7-8) --STOP--> Stage 1C (L4 in tubes) --> G1'
                                                      | GO (or GO-WITH-LEVER + Stage 1C in parallel); mode chosen
                                    order Stage 2 parts (valves, SIA pump, magnet actuator, trap/cup prototypes)
                                                      v
                                    Stage 2 T2 (wk 9-16): plumbing+automation, U5, U4, cup, first flow blanks
                                                      |
                                                    G2 (wk 16) --U5 fail--> backup bed parts --> Stage 3B
                                                      | go
                                    order Stage 3: commercial thin-layer cell, machined cup, trap
                                    (custom IDA + 2nd channel only if G2 shows EC noise matters)
                                                      v
                                    Stage 3 T3 (wk 17-28): U7, unattended runs (IDA only if bought)
                                                      |
                                                    G3 (wk 28) --> Stage 4 validation (wk 28-32) --> report
```

Critical path: Stage-1 reagent delivery → U1/U3 → G1a → G1 → valve/pump delivery → U5 → G2 → machined cup and
trap → U7 → validation. The custom IDA cell is no longer on the critical path: it is designed and quoted during
Stage 2 and ordered only if the G2 data show that electrochemical noise is a material part of the blank SD
(revised after final review, S9; the earlier invitation to order it at G1 is withdrawn).

---

## 3. Stage 0 — set-up and facts (weeks 0–2)

No gate-critical science; this stage removes "unknown installed configuration" items and puts the measuring tools
in place. Bench time ≈ 5 days.

| ID | Task | How | Output / acceptance |
|---|---|---|---|
| S0.1 | Installed facts (docs/02 §8 Q1–Q10) | Read Empower version (Help → About), BSM/SM-FL firmware (Empower instrument console), photograph BSM and SM-FL rear panels, confirm loop 100 µL and syringe size, list Gamry software version and licences (Gamry Framework → About) | A filled `bench/S0_facts/facts.md`. Needed by automation config (§9) |
| S0.2 | Vendor questions | Gamry: (a) can a Reference 600+ be synchronised as a bipotentiostat with a second 600+ (the bipotentiostat page shows a video "Bipotentiostat with 2 600+ Potentiostats") or with a Reference 620 (not listed)? — needed only if the IDA option is taken (revised after final review, S9) (b) is a separate ToolkitPy licence needed? (c) can ToolkitPy run two instruments from one process? Waters: (d) can the Empower Toolkit start a sample set and report run state on this Empower version? (e) event I/O of BSM/SM-FL | Written answers filed. (a) decides docs/07 §3 option A vs B |
| S0.3 | Inject Start wiring | Wire SM-FL Inject Start (connector 1, pins 1–2, docs/02 §3.1 [V: WKB55803]) to an isolated digital input of the USB DAQ (docs/07 §0). Run `python -m elisa_auto.watch_inject` (README) and make 10 injections of buffer | Every injection logged with time stamp; pulse width recorded (UNVERIFIED today) |
| S0.4 | Lab PC | Install per `automation/README.md`; run `python -m pytest -q automation/tests` and the simulated cycle | Tests pass on the lab PC (gate G0) |
| S0.5 | Electrochemical floor | Gamry 600+: (i) dummy cell, (ii) carbon SPE with a 50 µL drop of substrate buffer, (iii) same SPE in the DropSens wall-jet cell at 50 µL/min from the BSM. Chronoamperometry at +0.35 V vs on-strip Ag, 10 min, Faraday cage | RMS noise and drift per configuration → compare with `ma.noise` and docs/02 §4.5 (3 pA in flow, 1 pA stopped; UNVERIFIED) |
| S0.6 | BSM low-flow check (the primary also depends on it: readout sweep at 10 µL/min and accumulation shunt at 10–50 µL/min, docs/05 §4.1; the backup loads at 10 µL/min — corrected by the final review, docs/08) | Gravimetric: 1, 10, 20, 100 µL/min into a weighed vial, 30 min each, 3 repeats, with the restrictor fitted | Flow error and CV; confirms or refutes `hw.bsm.flow_min` = 1 µL/min (docs/00 user statement) |
| S0.7 | Clean-handling set-up | §8.1: dedicated pipettes, filter tips, LoBind tubes, "IgG-free" bench area, glove changes, sealed blank stock | SOP written into `bench/SOP_clean_handling.md` |
| S0.8 | Orders and quotes | Order the Stage-1A items needed for E1.1–E1.3, E1.2b and E1.7 (docs/07 §1); ask the BLI/SPR provider for a quote and slot, and ask for quotes and lead times for Stage 2/3 items, without ordering. **The BLI/SPR booking and the NISTmAb order wait for G1a** (week 5): both are useless if U1 or U3 stops the project (revised after final review, S8) | Purchase log |

**G0 (week 2):** automation tests pass on the lab PC; Inject Start edges are logged; Stage-1 reagents delivered or
dated. G0 has no "stop" outcome.

---

## 4. Stage 1 — reachability, no custom hardware (weeks 2–8)

### 4.0 Common materials and conditions for Stage 1

* **Assay buffer (AB):** 50 mM Tris-HCl pH 7.4, 150 mM NaCl (**no phosphate**: phosphate is a competitive ALP
  inhibitor, K_i 2 µM nominal, and `chem.enzymes.alp.phosphate_inhibition_Ki` states "NO PBS in lines that reach the
  enzyme step"; residual PBS carried into the substrate would inhibit ALP variably — corrected from "PBS" by the final
  review, docs/08), 1 % (w/v) IgG-free BSA (docs/07),
  0.05 % Tween-20, made in LoBind tubes or glass, 0.22 µm filtered. No azide (azide is irrelevant to ALP but
  keep reagents HRP-compatible for fallback chemistry tests).
* **Substrate buffer (SB):** 0.1 M Tris (or diethanolamine-free carbonate) pH 9.5, 1 mM MgCl₂ (docs/05 §4.1:
  pH 9.5 with Mg²⁺). **HQDP working solution:** dissolve fresh, in the dark, at 0.3 mM (Stage-1 readout default,
  lower free-HQ background) or 1 mM (design concentration). Model Km 0.1 mM (UNVERIFIED,
  `ma.chemistries.alp_hqdp.Km`), so 0.3 mM gives ≈ 75 % of V_max.
* **Beads:** streptavidin superparamagnetic beads 2.8 µm (Dynabeads M-280 Streptavidin, docs/07 §1;
  6.5×10¹⁰ beads/g, `chem.surfaces.magnetic_bead_M280_count_per_mass`, INHERITED). 5×10⁵ beads = 7.7 µg = 0.77 µL of
  the 10 mg/mL stock. The stock buffer contains BSA on some lot documents (docs/07 §1) — see bovine-IgG control E1.4.
* **Bead loading:** load biotinylated antibody at ≈ 80 % of the stated capacity (10 µg biotin-IgG per mg beads,
  `chem.surfaces.magnetic_bead_M280_SA_capacity_biotinylated_IgG`, INHERITED) for 30 min at 22 °C rotating, wash 3×
  in AB, quench free streptavidin with 10 µM free D-biotin 10 min, wash 3×, block 30 min in AB. **Non-immune beads**
  are made identically with biotinylated **normal goat F(ab′)₂** (the capture reagent's species and fragment format,
so that non-immune beads differ from capture beads only in specificity; was "non-immune IgG" — revised after final
review, W8) at the same mass loading. The M-280 stock is supplied in PBS: wash the beads 3× in AB (TBS) before
loading so no phosphate is carried into any step (revised after final review, B1).
* **Temperature:** 22 ± 1 °C, recorded (no thermostat exists; docs/05 §4.5 point 5). Use a rotator, not a shaker,
  for bead suspensions.
* **Readout (chosen in E1.1):** either R-drop (T0: 50 µL drop on a carbon SPE, chronoamperometry or square-wave
  voltammetry with the Gamry) or R-FIA (T1: 30 µL PLNO injection of the supernatant into SB carrier at 50 µL/min
  through the DropSens wall-jet cell at +0.35 V vs on-strip Ag; peak area). Both read hydroquinone (HQ).
* **Enzyme counting:** every readout batch includes a **conjugate standard series**: the same conjugate lot diluted
  in AB to 0, 1×10⁴, 3×10⁴, 1×10⁵, 3×10⁵, 1×10⁶, 3×10⁶ molecules per tube (molar concentration from the vendor
  mg/mL and nominal molar mass; the molar mass cancels in the label factor, §1 point 4), incubated in the same SB
  volume and time as the samples. N_ALP of a sample = interpolation on this series. Conjugate standards at
  ≤ 10⁶ molecules in 50 µL (≤ 33 fM) are adsorption-prone: prepare serially in AB (1 % BSA carrier) in LoBind tubes
  immediately before use, and include one level in triplicate to see the scatter.
* **Bead transfer before substrate:** after the last wash, resuspend beads in 100 µL AB and **transfer to a fresh
  LoBind tube**, then remove the buffer on the magnet and add SB. This removes conjugate bound to the incubation-tube
  wall, which would otherwise be counted as bead NSB.

### E1.1 — Readout qualification (prerequisite of E1.2–E1.9)

* **Purpose.** Choose the HQ readout and establish its limit of detection, because the U1 and U3 numbers are only as
  good as the HQ measurement. Tier: T0 (drop) and T1 (FIA-EC).
* **Materials.** Gamry 600+, carbon SPEs + DRP-CAC connector, DropSens wall-jet flow cell, HQ standard, HQDP lot 1,
  SB; Waters BSM + SM-FL (100 µL loop) + TUV for the FIA route.
* **Procedure.**
  1. HQ stock 10 mM in 10 mM HCl (slows oxidation), fresh daily; dilute in SB to 0, 1, 3, 10, 30, 100, 300 nM.
  2. Matrix: (a) SB alone, (b) SB + 0.3 mM HQDP, (c) SB + 1 mM HQDP (standard addition — the HQDP lot contributes
     its own free HQ; that is E1.2's measurement and the offset here).
  3. R-drop: 50 µL drop, new SPE per drop (and, separately, one SPE reused for 10 drops with a buffer rinse to see
     the electrode term); pre-condition 60 s at 0 V, then square-wave voltammetry −0.2 → +0.5 V (amplitude 25 mV,
     step 4 mV, 25 Hz; settings to be optimised) and chronoamperometry at +0.35 V for 60 s (charge 10–60 s).
  4. R-FIA: BSM 50 µL/min SB (A1), restrictor, SM-FL PLNO 30 µL injections, cell at +0.35 V, run time 4 min per
     injection; TUV at 290 nm downstream as a plug marker (not quantitative at nM).
  5. Replicates: 10 blanks (matrix a) and triplicates of each level per matrix, per route.
* **Measurement → parameter.** Slope (A·s per nM) and LOD_HQ = 3·SD(10 blanks)/slope. Informs `ma.noise.*` for the
  chosen cell type and the readout-noise term in U1/U3 error propagation.
* **Acceptance.** LOD_HQ ≤ 1 nM in matrix (b) for the chosen route (derived here: U1 needs ±1 nM resolution on a
  ≈ 3 nM free-HQ background, see E1.3 expectations; U3's confirm limit 10⁻⁵ in 1 mM is 10 nM).
* **Model / literature expectation.** FIA-EC on glassy carbon reached 0.12 nM HQ (DellaCiana1996, docs/01 a.1);
  SPE in a drop is UNVERIFIED and is expected to be worse (capacitive background of a 4 mm carbon disk).
* **Time.** 2 days.
* **Outcomes.** If R-drop meets ≤ 1 nM, Stage 1 stays fully T0. If only R-FIA does, use R-FIA (T1, simple
  plumbing only). If neither: try the gold SPE, a polished glassy-carbon disk in a thin-layer cell, or longer
  integration; do not run U1 until a readout passes (U1 at the kill level still produces ≥ 25 nM, so a 3-nM readout
  can still make the kill decision — record this as a degraded mode).

### E1.2 — U3: free hydroquinone, hydrolysis and HQ stability of the HQDP lot

* **Purpose.** Resolve U3 (docs/05 §5): decides reachability (scenario S4a: free HQ 10⁻³ kills every design;
  P(success) 0.12 at 10⁻⁴, 0.30 at 10⁻⁵, `results/design/kill_thresholds.md`). Tier: T0 or T1 (E1.1 route).
* **Materials.** HQDP (Metrohm DropSens DRP-HQDP, ≥ 2 lots if obtainable; no purity or free-HQ specification is
  published on the product page, docs/07), HQ standard, SB, amber glass vials, PEEK tubing piece (simulating the B1
  line), the Gamry readout.
* **Procedure.**
  1. Dissolve HQDP at 1 mM in SB at t = 0 (weighed; record the lot, CoA and solid appearance).
  2. Free HQ at t = 0: standard addition of HQ 0, 3, 10, 30 nM into aliquots of the 1 mM solution, triplicate
     each; intercept/slope gives [HQ]₀. Repeat with 0.3 mM to confirm linear scaling with HQDP (impurity, not
     electrode artefact).
  3. Time course at 22 °C in (a) amber glass, (b) a PEEK tube filled and capped (B1-line surrogate), (c) the BSM B1
     reservoir bottle if the solvent line is used: 0, 1, 2, 4, 8, **24 and 30 h**, triplicate reads (sequences run
     > 24 h, §7.7). (d) **Pumped aliquot:** HQDP in the B1 line pumped through the BSM heads and mixer and the loop at
     10 µL/min, sampled at the outlet at 0, 8, 24 and 30 h (steel and mixer contact, docs/02 §1.1 wetted materials)
     (revised after final review, S11; T1).
  4. HQ stability: HQ 30 nM spiked into SB without HQDP and into 1 mM HQDP, same time points (oxidation
     half-life, `ma.chemistries.alp_hqdp.product_half_life`, UNVERIFIED 2 h).
  5. Controls: SB alone at every time point (electrode drift); a sealed, N₂-purged HQDP aliquot (does oxygen drive the
     change?).
* **Measurement → parameters.**
  * f_free = [HQ]₀ / [HQDP] (mol/mol) → `ma.chemistries.alp_hqdp.free_product_impurity`.
  * Hydrolysis k_h from d[HQ]/dt = k_h·[HQDP] − k_ox·[HQ], with k_ox = ln2/t½ from step 4 →
    `ma.chemistries.alp_hqdp.hydrolysis_rate`.
  * t½ of HQ → `ma.chemistries.alp_hqdp.product_half_life`.
  * Run-to-run CV of the substrate background → `ma.noise.substrate_background_cv`.
* **Acceptance (docs/05 §5 U3).** Confirm: f_free ≤ 10⁻⁵ and k_h ≤ 10⁻⁹ s⁻¹. Purify or change lot: 10⁻⁵–10⁻⁴.
  Kill the substrate: > 10⁻⁴ after purification; then test AAP or p-hydroxyphenyl phosphate the same way.
* **Model expectation.** Prior f_free 10⁻⁵ (10⁻⁷–10⁻³), i.e. 10 nM (0.1 nM–1 µM) HQ in 1 mM; k_h 10⁻¹⁰ s⁻¹
  (10⁻¹²–10⁻⁸), i.e. +0.3 nM (0.003–29 nM) per 8 h in 1 mM before oxidation losses. Wilson2004 reports "excellent
  hydrolytic stability" without a number.
* **Time.** 3 days per lot plus the 24/30-h reads (the time course spans two days; the pumped arm runs on the T1
  set-up alongside E1.1).
* **Outcomes.** Confirm → G1 U3 item passed. Purify range → ask the vendor for a lower-HQ lot and try a clean-up
  (UNVERIFIED route; for example recrystallisation or removal of the phenolic impurity by solid-phase extraction,
  to be designed with a chemist), re-run E1.2 on the purified material. Kill → E1.2 on the alternative substrates
  (docs/07 §1 lists 4-aminophenyl phosphate and ascorbic-acid-2-phosphate; p-hydroxyphenyl phosphate supply
  UNVERIFIED); re-run the model with `ma.chemistries.alp_aap` / `alp_papp` and their measured values.
  Also: if k_h > 10⁻⁹ s⁻¹ but f_free passes, deliver substrate from a 4 °C vial instead of the B1 line (docs/02 R8)
  and re-check the cycle time.

### E1.2b — Pre-electrolysis of the HQDP substrate ("guard cell" test; added 2026-11-12, user decision; bench test only)

* **Status and scope.** Added by user decision after docs/12. **A bench test only**: no guard cell is added to the
  gen-1 flow hardware, the step tables or the hardware design until this result is in and the decision below has
  been taken. Numbered E1.2b so that no existing experiment number (cited in docs/08–12) changes. **Not a G1a/G1
  input**: the G1 rule (§4.11) is unchanged and is applied with the free HQ of the lot *as delivered* (E1.2),
  because gen-1 has no guard cell. Tier: T0 (Gamry 600+ and a small stirred cell; no Waters, no flow hardware).
* **Purpose and the model question it answers.** docs/12 §2.3 point 2 derives that electrolysing the substrate
  once at the read potential before accumulation removes the lot's free HQ (oxidised to benzoquinone, BQ, which is
  not oxidised again at the read). It represents this in the model as `ma.chemistries.alp_hqdp.free_product_impurity`
  × 0.01 (value 10⁻⁷, bounds 10⁻⁹–10⁻⁵; docs/12 §8 table, row "all"), resting on the **assumption that 1 % of the
  fill escapes electrolysis (UNVERIFIED**; docs/12 §2.3, §8, §10). With that credit the S4a kill scenario (free HQ
  10⁻³) becomes the nominal 10⁻⁵ case (docs/12 §3.9: A0 under S4a 19 pg/mL, P 0.00 → A1 under S4a 1.9 pg/mL,
  P 0.22; nearest-model estimates), and docs/12 §9 decision 3 / §10 calls the idea portable to gen-1 as a
  flow-through coulometric guard cell on the substrate line. The questions: (1) is a residual of ≤ 1 % of the free
  HQ **chemically** reachable at the chosen potential, or is there a floor (HQ re-formed from BQ, an
  electrogenerated product read as HQ, HQDP converted at the electrode)? (2) does free HQ re-grow after electrolysis
  faster than the lot's own hydrolysis within the time to the end of accumulation? (3) does electrolysis harm
  anything the model does not represent (HQDP consumption, BQ or its products inhibiting ALP or changing the
  readout)? (4) does the counter electrode re-form HQ when it shares the solution? **What it does not answer:** the
  geometric escape of a real guard cell or readout chamber (ports, valve seats, dead volume; the origin of the 1 %
  in docs/12). In a stirred, divided bulk cell the mass-transfer escape exp(−p·t) is driven far below 1 %, so the
  measured escape is the chemical floor; the geometric escape is measured only on a real cell (gen-1: Stage 2, if the
  decision below calls for it; cartridge: docs/12 risk A5).
* **Materials.** Gamry 600+ (potentiostatic chronoamperometry / bulk electrolysis); a divided bulk-electrolysis
  cell, 5–10 mL glass, with the counter electrode in a fritted compartment; large-area carbon working electrode
  (reticulated vitreous carbon or graphite felt, ≈ 1 cm³); Pt or graphite counter; Ag/AgCl (3 M KCl) reference
  with frit; magnetic stirrer and PTFE stir bar; carbon SPEs (for the CVs in step 1); HQDP lot(s) of E1.2, HQ
  standard, 1,4-benzoquinone (BQ) for the BQ-spike control, SB, amber glass vials, N₂; the conjugate D1 and its
  standard series (§4.0) for the ALP-rate arm; the E1.1 readout (R-drop or R-FIA). New items: docs/07 §1.2 (rows
  marked E1.2b); none has a checked part number.
* **Choice of potential (reasoning).** Default **E_pre = +0.35 V vs Ag/AgCl, the read potential**
  (`chem.substrates.HQ.detection_potential` 0.35 V, 0.30–0.42; DellaCiana1996 on glassy carbon): pre-electrolysis
  then removes exactly what the read would count as HQ and nothing that the read cannot see. Thermodynamics is not
  limiting (derived here): the HQ/BQ formal potential at pH 9.5 lies near 0 to −0.1 V vs Ag/AgCl (estimate used for
  the IDA collector in E3.1, UNVERIFIED), so at +0.35 V the Nernst ratio [HQ]/[BQ] at the electrode is
  exp(−2F·0.35 V/RT) ≈ 10⁻¹², far below 10⁻². A **higher** potential raises the risk of oxidising HQDP itself or
  the matrix (onset potential of HQDP on carbon not found, **UNVERIFIED**; step 1 measures it); a **lower** one risks
  incomplete removal on a high-area carbon with slow kinetics. Rule (judgement, applied to the step-1 CVs): keep
  +0.35 V if the HQ wave reaches its mass-transport plateau by ≤ +0.30 V on the electrolysis carbon and 1 mM HQDP
  shows no current above SB alone below +0.50 V; otherwise take the midpoint of the window and record why.
* **Procedure.**
  1. *Windows (½ day).* CV and SWV (−0.4 → +0.8 V, 20 mV/s; E1.1 SWV settings) on a carbon SPE and on the
     electrolysis carbon in the cell: SB alone, SB + 1 mM HQDP (unspiked), SB + 10 µM HQ, SB + 10 µM BQ. Output: HQ
     plateau potential, HQDP onset potential, BQ reduction potential (for the counter-electrode argument).
  2. *Spiked solutions.* 1 mM HQDP in SB (lot of E1.2, fresh, dark) spiked with HQ to **10⁻⁴ (100 nM) and 10⁻³
     (1 µM) mol/mol** immediately before use (docs/12 risk A5 asks for 10⁻⁴–10⁻³), plus the unspiked lot. The 10⁻³
     spike is the S4a level and makes the 1 % residual 10 nM — ten times the E1.1 acceptance LOD (≤ 1 nM), so 1 %
     is resolvable; the residual of the unspiked lot (≈ 0.1 nM at 10⁻⁵) is not, and only confirms "≤ LOD".
  3. *Electrolysis (divided cell, stirred, 22 °C, air).* 5.0 mL in the cell; SB-only pre-electrolysis of the
     carbon at E_pre until the current is flat (conditioning, recorded); then the solution, E_pre applied, current
     logged at 1 s. Sample 3 × 100 µL at **10 and 30 min** with the potential still applied. From the background-
     corrected current fit i(t) − i_bg = i₀·exp(−p·t) → p (s⁻¹) and the predicted mass-transfer escape exp(−p·t)
     (expected minutes to exhaustion; p not known for this cell, UNVERIFIED). If the measured residual is far above
     exp(−p·t) and does not fall from 10 to 30 min, it is a floor (chemistry), not mass transfer.
  4. *Same-cell open-circuit control* for every spike level and day: the same solution stirred in the same cell for
     the same time with the potential off. Escape is formed against this control, which removes air oxidation of HQ
     during the electrolysis (HQ t½ 2 h, `ma.chemistries.alp_hqdp.product_half_life`, UNVERIFIED) from the result.
  5. *Residual free HQ.* Each aliquot read by **standard addition** of HQ 0, 3, 10, 30 nM, triplicate reads, on the
     E1.1 route — the E1.2 method, so residuals and E1.2's f_free are on the same scale. Open-circuit controls at
     10⁻³ are diluted 1:10 in SB before the read (the standard addition absorbs the matrix change).
  6. *Arms and replicates.* Independent electrolyses (fresh solution, conditioned electrode) per condition:
     10⁻³ at +0.35 V **n = 3**; 10⁻⁴ at +0.35 V n = 3; unspiked at +0.35 V n = 3; 10⁻³ at **+0.25 and +0.45 V**,
     n = 2 each (does the residual plateau with potential; does a higher potential create HQ-like products);
     **undivided cell** (counter in the same solution), 10⁻³ at +0.35 V, n = 2 (does the cathode reduce BQ back to
     HQ — the question any guard cell or in-chamber pre-electrolysis with a nearby counter must answer); SB alone at
     +0.35 V, n = 3 (background charge and electrode drift); **repeat electrolysis** of one unspiked solution
     (10 min, then 60 min, then a second 10-min run): any HQDP-borne current above SB is converted to the fraction
     of HQDP consumed (Q / (2F·n_HQDP)).
  7. *Re-growth after electrolysis.* Electrolysed unspiked and 10⁻³ solutions transferred to amber glass at 22 °C
     and read (standard addition, triplicate) at **0, 0.5, 1, 2, 4 and 8 h**; the same lot non-electrolysed at the
     same times (control; the E1.2 time course on the same day). Fit d[HQ]/dt = k_h·[HQDP] − k_ox·[HQ] with k_ox from
     E1.2 step 4 → k_h,post (electrolysed) vs k_h,control. Starting from ≈ 0 instead of the lot's free HQ, k_h,post
     is the more sensitive estimate of the lot's hydrolysis (nominal 10⁻¹⁰ s⁻¹ gives ≈ 2.9 nM in 8 h at 1 mM before
     oxidation; 30 min gives 0.18 nM, below any readout).
  8. *Side effects of BQ and of electrolysis.* (a) SWV (−0.4 → +0.6 V) of the electrolysed 10⁻³ solution against
     the unspiked, non-electrolysed lot: any new peak, and the apparent HQ at the read potential that it causes.
     (b) **BQ-spike control:** 1 µM BQ (the BQ an electrolysed 10⁻³ solution holds) added to the unspiked lot,
     without electrolysis, read at 0, 0.5, 2 and 8 h (does BQ or its alkaline decomposition products read as HQ or
     re-form HQ?; BQ fate at pH 9.5 is UNVERIFIED). (c) **ALP rate:** the conjugate standard series (§4.0; 0,
     1×10⁵, 1×10⁶, 3×10⁶ molecules, duplicate) incubated 60 min in electrolysed 10⁻³ substrate, in the BQ-spike
     substrate and in non-electrolysed unspiked substrate; slope ratio = (electrolysed or BQ) / control. (d) HQ
     standard-addition slope electrolysed / control (readout sensitivity unchanged by BQ).
* **Measured quantities → model inputs.**
  * **Escape fraction f_esc** = residual HQ (electrolysed) / HQ (open-circuit control, same time), with its 95 % CI
    (log scale, t with n − 1). **No parameter key exists** for this quantity (params/*.yaml checked: there is no
    pre-electrolysis or escape key; docs/12 applies it as a multiplier on `ma.chemistries.alp_hqdp.free_product_impurity`
    in a scratch copy, its §8 and Appendix A `pre_el`). Record it in `bench/S1_E1.2b_<date>/results.yaml` as
    `pre_electrolysis_escape_fraction: {value, low, high, e_pre_V, electrolysis_min, cell: divided, source}` and as a
    **comment line** in `bench/measured_values.yaml` — **not as a key**: `model_feedback` rejects any key that is
    not a model parameter (`design_lib.apply_bench_values` raises KeyError), and the value must not enter G1. It is
    used only in scenario runs of the guard-cell / cartridge variants: free_product_impurity × f_esc (and its
    bounds) in place of docs/12's × 0.01.
  * **k_h,post** → `ma.chemistries.alp_hqdp.hydrolysis_rate` — the same quantity of the same lot as E1.2. It is
    entered (at G1, not G1a) only if E1.2's time course could not resolve k_h and the two are consistent; this is a
    better measurement of an existing G1 input, not a new input, and the rule is unchanged.
  * HQ t½ in electrolysed substrate → consistency check of `ma.chemistries.alp_hqdp.product_half_life` (E1.2 keeps
    the entered value).
  * CV of the residual background over replicate electrolyses → informs `ma.noise.substrate_background_cv` for the
    pre-electrolysed variants only (scenario runs; not entered at G1).
  * p (s⁻¹), charge per electrolysis, fraction of HQDP consumed, ALP-rate ratio, readout-slope ratio, new-peak
    current: no key; recorded in the folder (needed to size a guard cell and to judge side effects).
* **Acceptance (derived here from docs/12's arithmetic; thresholds fixed before data).** The U3 acceptance for free
  HQ is 10⁻⁵ mol/mol and its kill line 10⁻⁴ (docs/05 §5 U3; `gates.yaml` G1 free_hq_mol_per_mol). docs/12's credit
  "S4a (10⁻³) → nominal (10⁻⁵)" requires f_esc ≤ 10⁻⁵ / 10⁻³ = **10⁻²**, which is the 1 % assumption itself. A
  guard cell that cannot bring even a lot at the kill line into acceptance needs f_esc > 10⁻⁵ / 10⁻⁴ = **10⁻¹**,
  and then has no use for any lot that E1.2 does not already accept. Hence:
  * **PASS** (pre-electrolysis chemically supports the docs/12 credit): upper 95 % bound of f_esc ≤ **0.01** at the
    10⁻³ spike, divided cell, E_pre, 30 min; **and** all side-effect criteria below. (With n = 3 and a 20 % CV of
    the residual the upper bound is ≈ 1.6× the point estimate, so a pass needs a point estimate ≲ 0.006.)
  * **INTERMEDIATE**: 0.01 < f_esc ≤ 0.1 (point estimate), side effects pass — the S4a scenario is not rescued, a lot
    in the purify band (10⁻⁵–10⁻⁴) is.
  * **FAIL**: f_esc > 0.1 (point estimate), **or** any side-effect criterion fails.
  * Side-effect criteria (each must pass for PASS or INTERMEDIATE):
    (i) re-growth: k_h,post ≤ **10⁻⁹ s⁻¹** (the U3 hydrolysis acceptance; derived: over a 30-min window — guard cell
    to end of accumulation, gen-1 fill + accumulation + readout = 12 min, docs/12 A 15-min accumulation, plus line
    dwell — it re-forms ≤ 1.8×10⁻⁶ mol/mol, ≤ 18 % of the 10⁻⁵ acceptance) **and** k_h,post ≤ 2 × k_h,control
    (derived: electrolysis must not create an HQ source; ×2 is about what two triplicate slope fits at a few nM can
    resolve, UNVERIFIED until E1.1 gives the readout CV);
    (ii) no HQ-like product: any new SWV peak, and the BQ-spike control, add ≤ **1 nM HQ-equivalent** at the read
    potential in 1 mM HQDP (derived: 10⁻⁶ mol/mol, 10 % of the 10⁻⁵ acceptance; also ≈ the E1.1 LOD);
    (iii) ALP rate ratio and HQ readout-slope ratio within **0.85–1.15** (derived: about what a duplicate/triplicate
    ratio resolves at 10–20 % readout CV, §12.2; on the platform a smaller common factor scales specific and NSB
    signal alike);
    (iv) HQDP consumed per electrolysis ≤ **1 %** (derived: keeps the substrate concentration, and so v/V_max and the
    ULOQ, within the weighing tolerance of the solution).
  * Informational, no pass/fail: undivided/divided escape ratio (> 2 → any guard or in-chamber pre-electrolysis
    needs a counter electrode separated from, or downstream of, the treated volume); residual at +0.25 and
    +0.45 V (chooses E_pre if +0.35 V fails a side-effect criterion that a lower potential passes).
* **Model / literature expectation.** Assumption to be tested: 1 % escape (docs/12, **UNVERIFIED**; geometric in
  origin, so a stirred divided cell is expected to do better unless a chemical floor exists). Nernst floor at
  +0.35 V ≈ 10⁻¹² (derived above). Re-growth at the nominal k_h 10⁻¹⁰ s⁻¹ (`hydrolysis_rate`, UNVERIFIED): 0.18 nM
  in 30 min, 2.9 nM in 8 h at 1 mM before oxidation. A commercial flow-through coulometric cell — the guard-cell
  candidate named in docs/12 §9 decision 3 — is specified at collection efficiency 0.95 (0.8–1.0;
  `hw.flow_cells.thermo_6011rs_coulometric.collection_efficiency`, THERMO_6011RS "near 100 %"), i.e. a single-pass
  escape of ≈ 5 %, which by itself would be INTERMEDIATE here; its two porous-graphite electrodes in series could
  do better (UNVERIFIED), and its minimum flow of 300 µL/min (`…min_flow`) is above the gen-1 fill flow of
  200 µL/min (`cycle_primary.yaml` substrate_fill). Both are Stage-2 questions; this test only says whether the
  chemistry allows ≤ 1 %.
* **Time.** 4 bench days (½ day windows; 2 days of electrolyses with reads; 1 day for re-growth reads and the
  ALP/BQ arms; ½ day analysis), plus the 8-h reads. Weeks 5–7, after G1a (§10): it does not compete with E1.2/E1.3
  for the G1a critical path, and it is reported at G1 (weeks 7–8) so the Stage-2 order list can include or omit a
  guard-cell quote. It runs whatever the G1a verdict, unless the project is reported non-reachable.
* **Data.** `bench/S1_E1.2b_<YYYY-MM-DD>/` (§9.1) with the Gamry files (CVs, i(t) of every electrolysis), the
  filled `automation/templates/pre_electrolysis.csv` and `results.yaml`. `python -m elisa_auto.analyze` has no
  handler for this template (it ignores the file); the residuals are standard-addition intercepts computed as in
  E1.2 (`stats.standard_addition`).
* **Decision that follows each outcome** (taken at G1, by the user; none changes the G1 rule):
  * **PASS** → *included in the cartridge design*: docs/12's pre-electrolysis step (PE1) is kept, with the
    measured f_esc replacing the assumed 0.01 in its nearest-model runs; the readout chamber's own geometric escape
    remains docs/12 risk A5. *Gen-1: guard cell considered at Stage 2* — quoted with the Stage-2 orders and built and
    tested in flow (geometric escape of the real cell at the gen-1 fill flow, with the same thresholds) only if
    (a) E1.2 places the lot above 10⁻⁵ (purify band or above: the guard cell then replaces purification or a
    substrate change as the first remedy), or (b) a model run of the primary with free_product_impurity × f_esc
    gains ≥ 0.05 in P (the decision-grade margin, §12.6). Otherwise gen-1 stays without a guard cell.
  * **INTERMEDIATE** → cartridge: PE1 kept only as a background-recording step, with the credit in the model reduced
    to the measured f_esc (no S4a rescue claimed). Gen-1: guard cell considered at Stage 2 only under (a), and only
    for a lot whose f_free × f_esc ≤ 10⁻⁵.
  * **FAIL** → *dropped* from gen-1 and from the cartridge design; the docs/12 rows with pre-electrolysis (A1, B1,
    C2 pre-electrolysis, A1 under S4a) are void and the corresponding rows without it apply; S4a remains a kill
    scenario and U3 is handled only by E1.2's purify/replace route. If only +0.45 V or only the undivided cell
    fails, the outcome is decided on the arm that passes and the restriction (potential ceiling, separated counter)
    is recorded as a design requirement.

### E1.3 — U1: conjugate NSB on blocked streptavidin beads (rate, linearity, reversibility, IgG vs F(ab′)₂)

* **Purpose.** Resolve U1 (docs/05 §5), the measurement that decides whether 1 pg/mL is reachable at all (scenario
  S1). Measures `ma.nsb.label_factor_igg_enzyme_conjugate` directly, its linearity in exposure (docs/04 §3.6:
  linearity UNVERIFIED), its reversibility (S3a) and the F(ab′)₂/IgG ratio (lever L3). Tier: T0.
* **Materials.** Non-immune blocked beads (§4.0); conjugates D1 = ALP-F(ab′)₂ goat anti-human IgG F(ab′)₂-specific
  and D2 = the whole-IgG ALP conjugate of the same specificity (or the Mabtech MT78-ALP of kit 3850-1AD-6 if no
  same-specificity whole-IgG conjugate is available; docs/07 §1); AB; AB + 0.1 % Tween-20 (stringent wash); SB +
  0.3 mM HQDP; magnet; rotator; LoBind tubes.
* **Procedure (per conjugate).**
  1. **Exposure series.** 5×10⁶ non-immune beads per tube in 200 µL AB containing conjugate at 0.1, 0.3, 1 and
     3 nM, for 10, 30 and 60 min at 22 °C, rotating; duplicate → 24 tubes.
  2. **Design-number arm.** 5×10⁵ beads, 1 nM, 30 min, triplicate (checks NSB ∝ bead area).
  3. Wash 3× with 500 µL AB on the magnet (1 min each), transfer to a fresh tube (§4.0), remove buffer.
  4. **Wash-stringency arm** at 1 nM × 30 min (docs/05 §5): 3 vs 10 washes × (AB vs AB + 0.1 % Tween) × (no hold vs
     5 min hold in the last wash), duplicate → 16 tubes.
  5. Add 50 µL SB + 0.3 mM HQDP, rotate 60 min at 22 °C, magnet, read 30–50 µL of supernatant (E1.1 route).
  6. Controls each day: no-bead SB blank (n = 6; sets the free-HQ background), beads without conjugate (n = 3; bead
     and reagent ALP-like background), conjugate standard series (§4.0, duplicate), conjugate exposure without beads
     in a tube taken through the washes (n = 3; checks carry-through of free conjugate — must read as no-bead blank).
* **Measurement → parameter.**
  * N_ALP per tube from the conjugate standard series (minus the no-conjugate bead control).
  * k_eff = N_ALP / (A_beads · C · t · N_A), with A_beads = n_beads · π·d² (2.46×10⁻¹¹ m² per 2.8 µm bead), C in
    mol/m³, t in s. **Label factor = k_eff / 4×10⁻¹¹ m/s** (docs/05 §5; `chem.nsb.nsb_effective_rate_constant`).
    Hand example: 6.4×10⁴ enzymes on 5×10⁶ beads (A = 1.23×10⁻⁴ m²) after 0.3 nM × 1800 s gives
    k_eff = 6.4×10⁴ / (1.23×10⁻⁴ × 3×10⁻⁷ × 1800 × 6.022×10²³) = 1.6×10⁻¹² m/s → factor 0.040.
    `python -m elisa_auto.analyze` does this from the CSV template (`automation/templates/u1_nsb.csv`).
  * Linearity: fit log N = log α + β·log(C·t) over the 12 exposure points; β and its 95 % CI.
  * Reversibility f_rev = 1 − N(10 washes, Tween, hold) / N(3 washes, AB, no hold) →
    `ma.design_levers.nsb_fraction_removed_by_wash` (scenario only; see note).
  * L3 ratio = factor(D1 F(ab′)₂) / factor(D2 IgG) → `ma.design_levers.fab_conjugate_nsb_factor`.
  * Note: the factor measured after the chosen wash protocol already contains the reversible part removed by that
    protocol. Enter it as the label factor and **do not** also apply S3a, or the wash gain is counted twice.
* **Acceptance (revised after final review, B3).** The decision is the G1a/G1 rule of §4.11 on the model P(success)
  with the measured factor entered. Fast screen (other values at their priors, `results/design/g1_decision_table.md`):
  factor ≤ 0.02 → GO; 0.03–0.08 → GO-WITH-LEVER (Stage 1C in parallel); ≥ 0.10 → STOP (Stage 1C in tubes, then G1′).
  The docs/05 levels 0.04 / 0.15 are superseded: evaluated the way a bench value is entered, factor 0.04 gives P 0.23
  for the primary (not a "confirm") and 0.15 gives P 0.05. Linearity: β ≤ 1.1 ("not super-linear" within the CI,
  derived here). Add the stringent wash step if ≥ 30 % is removed by stringent washes (S3a). The F(ab′)₂/IgG ratio
  sets L3. The U1 decision rests on this experiment (well resolved: ≈ 8 nM over ≈ 3 nM), not on E1.8 (S7).
* **Reservoir-ageing arm (added after final review, B4; decided at G1a).** Purpose: measure what holding beads with
  conjugate does to the blank, and whether reagent-borne human IgG builds complete sandwiches. Capture beads and
  non-immune beads (5×10⁶ each) held with **3.3 nM** D1 in AB (the conjugate concentration a shared 20-µL dose
  reservoir would hold) at **4 °C and 22 °C** for **0, 2, 8 and 24 h**, rotating; then diluted 11× into AB (0.3 nM, as
  in the cup), 30 min at 22 °C, and processed as steps 3–5; duplicate per cell (2 bead types × 2 temperatures × 4
  times × 2 = 32 tubes, one bench day plus the 24-h point). Also: **conjugate-only ageing**: D1 held at 6.6 nM in the
  conjugate-reservoir material (glass or PP, 4 °C, dark) for 0, 8, 24 and 30 h, then used at 0.3 nM × 30 min on fresh
  non-immune beads (n = 3 per time) — checks that the separate conjugate reservoir does not age into higher NSB
  (aggregates). Read-outs: label factor against hold time (model: linear irreversible NSB would grow it by
  1 + 3.3 nM × t / 11 nM·min, i.e. ×37 at 2 h and ×145 at 8 h at 22 °C, `results/design/shared_reservoir_cost.md`);
  the capture/non-immune ratio against hold time (a ratio rising with time on capture beads only = reagent-borne
  human IgG or detection-on-capture, docs/08 S5). Decision: the primary design already uses **separate** reservoirs;
  if the 4 °C 8-h factor is within ×1.5 of the 0-h factor the shared reservoir could be reconsidered as a
  simplification (it is not needed); a rising capture/non-immune ratio sends the reagents to E1.4-type lot testing;
  conjugate-only ageing > ×1.5 at 24 h sets a maximum conjugate-reservoir life (refill per 8 h sequence block).
* **Model expectation** (number of nonspecifically bound conjugates on 5×10⁶ beads; nominal factor 0.04, range
  0.01–0.15; 10× the per-assay numbers of the design, where the model gives N_nsb = 6.4×10³ at 0.3 nM × 30 min on
  5×10⁵ beads, `results/` diagnostics of P-vial):

  | C (nM) | 10 min | 30 min | 60 min |
  |---|---|---|---|
  | 0.1 | 7.1×10³ (1.8×10³–2.7×10⁴) | 2.1×10⁴ (5.3×10³–8.0×10⁴) | 4.3×10⁴ (1.1×10⁴–1.6×10⁵) |
  | 0.3 | 2.1×10⁴ (5.3×10³–8.0×10⁴) | 6.4×10⁴ (1.6×10⁴–2.4×10⁵) | 1.3×10⁵ (3.2×10⁴–4.8×10⁵) |
  | 1 | 7.1×10⁴ (1.8×10⁴–2.7×10⁵) | 2.1×10⁵ (5.3×10⁴–8.0×10⁵) | 4.3×10⁵ (1.1×10⁵–1.6×10⁶) |
  | 3 | 2.1×10⁵ (5.3×10⁴–8.0×10⁵) | 6.4×10⁵ (1.6×10⁵–2.4×10⁶) | 1.3×10⁶ (3.2×10⁵–4.8×10⁶) |

  At k_cat ≈ 1000 s⁻¹ (UNVERIFIED for HQDP) each 10⁴ enzymes make ≈ 1.2 nM HQ in 50 µL in 60 min; the
  conjugate standard series replaces this estimate with a measurement. The nominal 0.3 nM × 30 min point (6.4×10⁴)
  is ≈ 8 nM over a ≈ 3 nM free-HQ background (0.3 mM HQDP at 10⁻⁵); the kill level (0.15) is ≈ 29 nM.
* **Time.** 2 days per conjugate for the exposure series (+1 day for the wash arm) → 6 bench days for D1 and D2,
  plus 1 repeat day of the decisive cells (0.3 nM × 30 min and 1 nM × 30 min), plus 1.5 days for the
  reservoir-ageing arm. The factor entered at G1a is the design cell (0.3 nM × 30 min, standard wash), not the
  average over all exposures; `analyze` prints both (revised after final review, W2).
* **Outcomes.** See G1 (§4.11). Additional branches: β > 1.1 (super-linear: e.g. aggregates in the conjugate) →
  centrifuge/filter the conjugate (0.22 µm low-binding, or 10 min at 16 000 g) and repeat the 1 and 3 nM points;
  bead-number arm not proportional (± 30 %) → NSB is not area-limited (tube walls, carry-over); repeat with two
  transfers before substrate.

### E1.4 — Detection-on-capture and bovine-IgG cross-reaction

* **Purpose.** docs/05 §4.1 acceptance "blank on capture beads ≤ 1.2× blank on non-immune beads" (Qu1998 shows the
  mechanism and its suppression by normal serum; its 39 → 2.5 pg/mL is the overall LOD change, not a
  detection-on-capture factor — corrected after final review, docs/08 §9 C1); docs/05 §4.5 points 1–2. Tier: T0.
* **Materials.** Capture beads (biotinylated anti-human-Fc), non-immune beads, D1, AB made with (a) IgG-free BSA,
  (b) a standard BSA grade (bovine IgG present per vendor, `chem.nsb.bovine_IgG_in_BSA`), (c) the bead stock buffer
  carried over vs beads washed 3× before loading.
* **Procedure.** No analyte. **5×10⁶ beads and D1 at 1 nM** (revised after final review, B2 remainder: at 5×10⁵
  beads and 0.3 nM the bead signal, ≈ 0.8 nM HQ, sits on ≈ 3 nM free HQ and cannot reach the 15 % CV that §12.3
  assumes; at 5×10⁶ and 1 nM N ≈ 2×10⁵, comfortably measurable; NSB per area is unchanged, §1 point 3), 30 min, the
  E1.3 wash/transfer/substrate steps; readout E1.1. Arms: capture vs non-immune beads in AB(a), **n = 12 each**
  (power 0.8 to see a true 1.2× ratio at 15 % CV, §12.3); capture beads in AB(b) n = 5; unwashed bead stock n = 5;
  **background rows** (no-conjugate beads or no-bead substrate, n ≥ 3; `analyze` subtracts them, docs/08 B2).
  Include the conjugate standard series. Reagent-borne human IgG (docs/08 S5): a capture/non-immune ratio that grows
  with conjugate pre-incubation time is measured in the E1.3 reservoir-ageing arm.
* **Measurement → parameter.** Ratio R = N(capture)/N(non-immune) with 95 % CI (log scale) →
  `ma.labelling.detection_on_capture_residual_factor` (model 1, range 1–3). Bovine-BSA ratio → choice of blocker.
* **Acceptance.** R ≤ 1.2 (docs/05 §4.1), read as point estimate ≤ 1.2 with the upper 95 % bound < 1.5 (derived here: n = 12 cannot prove ≤ 1.2 more tightly). Standard BSA ≤ 1.2× IgG-free BSA, else IgG-free blockers only.
* **Model expectation.** R = 1 (1–3) in the model for a suppressed pair; at 5×10⁶ beads and 1 nM × 30 min
  N ≈ 2.1×10⁵ (E1.3 table), ≈ 25 nM HQ in 50 µL over 60 min, well above the ≈ 3 nM free-HQ background.
* **Time.** 2 days.
* **Outcomes.** R ≤ 1.2: pair accepted. R > 1.2: change the capture species (e.g. goat F(ab′)₂ capture with goat
  detection; docs/01 §d point 3) or add 0.25 % normal serum of the capture species to AB (Qu1998), re-test. R > 3:
  reject the pair.

### E1.5 — U2 (bench part): dissociation of the sandwich on beads

* **Purpose.** Effective off-rate of the labelled complex on beads, which is what matters during the chamber
  emptying (6.6 min) and washes (docs/05 §3: detection t½ ≈ 13 min drives the one-step upper tail). Complements BLI
  (E1.6). **Since the final review this is the decisive U2 measurement for the mode** (S4): the selected reagents
  (goat F(ab′)₂ capture, goat F(ab′)₂-ALP detection) are polyclonal and bivalent, so a solution 1:1 k_off from BLI
  is heterogeneous and avidity-dependent, whereas E1.5 measures the on-bead loss that the model's k_off stands for.
  Tier: T0.
* **Procedure.** 5×10⁶ capture beads + NISTmAb 100 pg/mL in 1 mL AB, 30 min; wash; D1 1 nM 30 min; wash 3×,
  transfer. Resuspend in 1 mL AB containing an unlabelled scavenger for released conjugate (10 µg/mL normal human
  IgG — binds released detection reagent and prevents re-binding) at 22 °C, rotating. Remove aliquots of beads at 0,
  15, 30, 60, 120 and 240 min (triplicate tubes per time point, set up in parallel; 240 min added so t½ of 30–60 min
is resolved), wash, substrate, read.
  Control: non-immune beads treated the same (NSB decay).
* **Measurement → parameter.** Fit N(t) = N₀·exp(−k_eff·t) (+ NSB control) → effective k_off of the complex. If
  t½,eff ≥ 1 h, both k_off,capture and k_off,detection ≤ 1.9×10⁻⁴ s⁻¹ (bound only — the loss rate is their sum).
  Updates `chem.antibodies.koff_detection` (and capture) bounds with BLI.
* **Acceptance (revised after final review, S4; `results/design/mode_choice.md`).** The complex t½ on beads bounds
  the detection t½ from below (the loss rate is the sum of both off-rates). The modelled modes cross at t½ ≈ 25 min
  (P one-step − sequential: −0.06 at 13 min, −0.02 at 20, +0.02 at 30, +0.05 at 45 min). **One-step mode:** t½,eff
  ≥ 30 min and k_on ≥ 3×10⁵ M⁻¹s⁻¹ (k_on from BLI); between 30 and 45 min the modes are LOD-equivalent within the
  model's noise and one-step is chosen because it keeps conjugate out of the SM-FL needle and loop (no conjugate
  carry-over; the B4 reservoir risk is removed by the separate reservoirs). **Sequential mode:** 10–30 min.
  **Reject:** detection t½,eff < 10 min, or a capture reagent whose bead-bound analyte decays with t½ < 1 h (the
  non-immune and no-detection controls separate capture loss from detection loss). Docs/05's 1-h boundary is
  superseded.
* **Model expectation.** k_off,detection 8.6×10⁻⁴ s⁻¹ (t½ 13 min; sampled to 8.3×10⁻³), k_off,capture
  1×10⁻⁴ s⁻¹ (t½ 1.9 h). Effective on-bead dissociation is slower than in solution because of rebinding
  (Chang2012: effective K_D < 10⁻¹¹ M); the scavenger limits that, so this is a conservative estimate.
* **Time.** 2 days.

### E1.6 — U2 (service): k_on, k_off of capture and detection reagents by BLI/SPR

* **Purpose.** U2 (docs/05 §5): solution k_on and k_off of each candidate at 25 °C in AB. External service or a
  core facility (no instrument in the fixed list).
* **Design.** Anti-human-IgG Fc (AHC-type) or streptavidin biosensors; load biotin-capture antibody on SA sensors,
  associate NISTmAb at 5 concentrations (e.g. 3–100 nM) for 300 s, dissociate 1800 s (needed to resolve t½ ≥ 1 h:
  1800 s at k_off 1.9×10⁻⁴ s⁻¹ gives 29 % decay; shorter dissociations cannot distinguish 10⁻⁴ from 10⁻⁵). For the
  detection reagent: capture NISTmAb on the loaded sensor, then associate the conjugate (or unlabelled detection
  antibody) at 5 concentrations, dissociate 1800 s. Two to four candidates per role. **Fits (revised after final
  review, S4):** 1:1 global fits only for monoclonal candidates; for the polyclonal reagents report a heterogeneous
  (two-state or 2:1 heterogeneous-ligand) fit with the fraction in each state and the residuals of the 1:1 fit, and use
  BLI for **k_on screening** and candidate ranking only — the mode is decided on E1.5.
* **Measurement → parameters.** `chem.antibodies.kon_capture`, `koff_capture`, `kon_detection`, `koff_detection`
  (value = fit, low/high = 95 % CI or the spread of repeats).
* **Acceptance.** k_on ≥ 3×10⁵ M⁻¹s⁻¹ (docs/05 §4.1); k_off criteria apply only to monoclonal candidates (as E1.5).
* **Model expectation.** Generic ELISA-grade antibodies: k_on 9×10⁴–1.2×10⁶ M⁻¹s⁻¹, k_off 3×10⁻⁶–1.3×10⁻³ s⁻¹
  (Chang2012); some commercial anti-human-Fc mAbs have t½ 1.4–3.3 min (Kamat2020) — those would be rejected.
* **Time.** 1 week elapsed (service), ≈ 1 day of preparation.

### E1.7 — U6: phosphate inhibition of the ALP conjugate (sets ULOQ)

* **Purpose.** U6 (docs/05 §5, §1.5): K_i of phosphate for the conjugate at the HQDP concentration. Tier: T0.
* **Procedure.** Conjugate at 3×10⁻¹³ M (fixed, ≈ 10⁷ enzymes in 50 µL) in SB with HQDP 0.3, 1 and 3 mM ×
  added KH₂PO₄/K₂HPO₄ (pH-adjusted to 9.5) 0, 2, 10, 50, 200 µM; product HQ after 5, 10 and 20 min (initial rate),
  duplicate. Also read HQ standards in each phosphate level (phosphate must not change the electrode response).
* **Measurement → parameter.** Fit competitive inhibition v = V·S/(Km(1 + I/K_i) + S) → K_i and Km →
  `chem.enzymes.alp.phosphate_inhibition_Ki`, `ma.chemistries.alp_hqdp.Km`.
* **Acceptance (docs/05 §5 U6).** Confirm: K_i ≥ 2 µM at 1 mM HQDP. Adjust: 3–5 mM HQDP or a shorter accumulation if
  the predicted ULOQ < 1000 pg/mL (re-run the model; §9).
* **Model expectation.** K_i 2 µM (1–540 µM, INHERITED, unchecked); Km 0.1 mM (0.02–1 mM, UNVERIFIED).
* **Time.** 1.5 days.

### E1.8 — Tube-format integrated assay: blank-equivalent and slope (the developer-mixed reference)

* **Purpose.** First end-to-end number: blank-equivalent B (pg/mL) = blank signal / calibration slope on beads, and
  enzymes captured and labelled per pg/mL. docs/05 §4.3: the developer-mixed vial is "the quickest way to measure
  U1, U5 and an integrated LOD early in Stage 1". Checks U1's conversion: B should equal N_nsb / (enzymes per
  pg/mL). Tier: T0.
* **Materials.** Capture beads, D1 (or the U2 winner), NISTmAb (RM 8671) and the polyclonal human IgG standard,
  AB, SB + 1 mM HQDP (design concentration), LoBind tubes, rotator, magnet; readout E1.1.
* **Standards.** NISTmAb 10 mg/mL → gravimetric serial dilution in AB in LoBind tubes, ≥ 4 steps of ≤ 100×, each
  step ≥ 100 µL into ≥ 900 µL, prepared fresh in a clean area (§8.1), to 1, 3, 10, 30, 100, 1000 pg/mL. Record
  every mass. Polyclonal standard at 100 pg/mL (subclass coverage check).
* **Procedure.** Per tube: 10 µL beads (5×10⁵) and 10 µL conjugate (to give 0.3 nM final), added separately from
  their own stocks just before the sample, + 200 µL standard or blank (AB from the sealed blank stock), 30 min
  rotating at 22 °C (docs/05 §4.1 incubation), wash 3×, transfer, **25 µL SB + 0.3 mM HQDP for 120 min**, read
  (revised after final review, S7: at 1 mM HQDP, 50 µL and 60 min the 1 pg/mL increment was a sub-1-nM step on
  ≈ 10 nM free HQ; now ≈ 1.8–2.4 nM on ≈ 3 nM, allowing for HQ oxidation with t½ 2 h). Blanks **n = 10**, each standard level n = 3, polyclonal n = 3, plus the
  conjugate standard series and no-bead SB blanks (n = 4). Randomise tube order; record times.
* **Measurement → parameters.** Slope b (enzymes per pg/mL) from a weighted linear fit over 0–30 pg/mL; B = (mean
  blank − no-bead SB blank)/b; LOD_tube = 3·SD_blank/b (indicative only: tube handling adds variance the instrument
  will not have). Captured-and-labelled fraction = b / (IgG molecules per pg/mL in 200 µL = 8.0×10⁵; 1 pg/mL of a
  150 kDa IgG is 4.0×10⁵ molecules per 100 µL, docs/00) → compare with the model (P-vial reference: 6.8×10³ labelled
  enzymes per pg/mL for 100 µL of sample, i.e. a captured-and-labelled fraction of ≈ 1.7 %, with label retention
  0.77 and capture retention 0.97 in the model diagnostics).
* **Acceptance (revised after final review, B3/S7).** E1.8 is a **consistency check, not a decision item**: B must
  lie within a factor 2 of N_nsb(E1.3, same exposure) / b (derived here); otherwise a term is missing
  (contamination, detection-on-capture, bead ALP background) and E1.4/E1.9 must explain it before G1. B ≈ 24 ×
  label factor (pg/mL) in the model, so B carries no information beyond E1.3 for the G1 rule.
* **Model expectation.** P-vial reference nominal: B = 0.96 pg/mL, N_nsb = 6.4×10³, 6.8×10³ enzymes at 1 pg/mL,
  LOD 0.32 pg/mL nominal (median 1.3 [0.30–21] with model readout noise, docs/05 §1.2). In the tube with the revised
  readout (25 µL, 0.3 mM HQDP, 120 min, k_cat 1000 s⁻¹ UNVERIFIED, v/V_max 0.75), 1 pg/mL is ≈ 2.4 nM HQ before and
  ≈ 1.8 nM after oxidation losses (HQ t½ 2 h, UNVERIFIED) over ≈ 3 nM free HQ — the tube LOD is still
  readout-limited; B and b are the quantities that transfer to the flow platform.
* **Time.** 3 days (one assay day, one repeat day, one day for standards preparation and checks).

### E1.9 — U9: human-IgG contamination of blanks and reagents

* **Purpose.** U9 (docs/05 §5; Parry1997). Tier: T0, run inside E1.8's blank budget.
* **Procedure.** Blank arms in the E1.8 format, n = 8 each: (a) sealed blank stock opened in the clean area with
  dedicated pipette and filter tips; (b) the same AB handled by normal bench practice (shared pipette, open rack);
  (c) **amplified handling**: (a) plus 10 extra transfers through fresh tips and tubes handled with gloved hands
  that touched the bench; (d) AB made from a second carrier-protein lot.
* **Measurement.** Mean difference in pg/mL-equivalent (using E1.8 slope) with 95 % CI. Contamination per handling
  step = ((c) − (a))/10.
* **Acceptance (docs/05 §5 U9).** Contribution ≤ 0.1 pg/mL equivalent. Honest limit: with n = 8 per arm the
  smallest detectable difference (80 % power) is ≈ 1.5 SD of the blank (§12.4), i.e. not 0.1 pg/mL directly; the amplified arm
  (c) makes a 0.1 pg/mL-per-step contamination a 1 pg/mL difference, which is resolvable.
* **Model expectation.** `ma.nsb.blank_igg_contamination_equivalent` 0 (0–3 fM = 0–0.45 pg/mL); Parry1997: human IgG
  in ≥ 1/3 of tip-cone eluates in every lab tested, **with no amount given** (the "100 fg per sample" of docs/05 §4.5
  has no source, docs/08 §9 C6). Scenario C1 (up to 1 pg/mL-equivalent) lowers the primary's P from 0.16 to 0.09
  (`results/design/final_designs.md`). Contamination carried by the **reagents** (conjugate, capture antibody, BSA
  lot) reaches blanks too: arm (d) and the E1.3 reservoir-ageing arm cover it (revised after final review, S5).
* **Time.** Within E1.8 (+0.5 day).
* **Outcome.** > 0.1 pg/mL per handling step → tighten §8.1 (sealed single-use blank aliquots, separate
  pipettes) and carry the measured value into the model (`ma.nsb.blank_igg_contamination_equivalent`).

### E1.10 — SM-FL passage: analyte recovery and analyte carry-over through needle and loop (T1)

* **Purpose.** Adsorptive loss of fM IgG on vial, needle, loop (docs/02 R1; `ma.delivery.adsorptive_loss_fraction_with_carrier`
  0.2, range 0.02–0.6, UNVERIFIED) and analyte carry-over in the injector — both with the installed full-loop
  injection, before any flow hardware is bought. Tier: T1.
* **Procedure.** BSM 100 µL/min of **AB without protein** (proteins are never pumped through the BSM,
  docs/02 §1.2); sample diluent = AB with 1 % IgG-free BSA. Full-loop 100 µL injections (2× overfill) of NISTmAb 10
  and 100 pg/mL from (a) Waters QuanRecovery vials, (b) standard PP vials; collect the outlet into LoBind tubes for
  3 loop volumes (300 µL, 3 min). Then inject a blank and collect it. n = 3 per arm. **Carry-over arm (revised after
final review, S6):** inject NISTmAb at **10 ng/mL**, then two blanks (B1, B2), n = 5 sequences; at 10⁻⁴ the B1 excess
is 1 pg/mL, resolvable in the tube format (a 100 pg/mL challenge gives 0.01 pg/mL at 10⁻⁴, below any readout). Assay the collected fractions
  in the E1.8 tube format (add beads + conjugate to the collected 300 µL; adjust the standard curve to the same
  volume) against identical standards that did not pass the injector.
* **Measurement → parameters.** Recovery = signal(passed)/signal(not passed) → 1 − `adsorptive_loss_fraction_with_carrier`
  and `ma.delivery.delivered_fraction_full_loop_100`; analyte carry-over = (B1 − B2 in pg/mL) / 10 000 pg/mL.
* **Acceptance (derived here; revised after final review, S6).** Recovery ≥ 0.8 (the model nominal); injector
  carry-over ≤ 1×10⁻⁴ (`gates.yaml` G1 injector_carryover). The docs/05 §5 U7 criterion 10⁻³ is superseded: after a
  1000 pg/mL sample it allows 1 pg/mL — the LOD itself — in the next sample.
* **Time.** 2 days.
* **Outcome.** Recovery < 0.6 → change vials, raise carrier to 2 % or add 0.01 % Tween to the diluent, consider a
  PEEK/HPS loop (docs/02 R1); re-test before Stage 2 depends on it.

### 4.10 Gate G1a (week 5) — early reachability check on U1 + U3 (added after final review, S8)

E1.1 → E1.2 (U3) and E1.3 with its reservoir-ageing arm (U1) are the only Stage-1 items that bear on reachability,
and they can be complete by about week 5. At G1a, enter the measured label factor (design cell, with its 95 % CI)
and the free-HQ fraction (and k_h) into `bench/measured_values.yaml` and run `python -m elisa_auto.model_feedback`;
apply the rule of §4.11 to the printed P. **STOP → no BLI/SPR booking, no NISTmAb order, no Stage-2 purchase**;
Stage 1C in tubes, then G1′. GO or GO-WITH-LEVER → book BLI/SPR and order NISTmAb (S0.8), continue Stage 1.
Indicative values (`results/design/g1_decision_table.md` Table 2, other parameters at priors): factor 0.02 with free
HQ 10⁻⁵ → P 0.37 (GO); 0.04 with 10⁻⁵ → 0.27 (GO-WITH-LEVER); 0.04 with 10⁻⁴ → 0.10 (borderline); 0.10 with
10⁻⁵ → 0.10 (borderline STOP).

### 4.11 Gate G1 (end of week 7–8) — is 1 pg/mL reachable, and in which mode?

Evaluate with `python -m elisa_auto.analyze bench/` (prints every quantity below with its CI) and
`python -m elisa_auto.model_feedback bench/measured_values.yaml` (model P(success) of the primary, the sequential
fallback and the backup with the measured values).

**Decision rule (revised after final review, B3; fixed 2026-11-11, before any Stage-1 data exist).** Let P be the
largest model P(success) among the admissible designs (one-step chamber P-chamb, sequential chamber S-chamb, backup
bed B-bed) printed by `model_feedback` with **all** Stage-1 values measured so far entered (label factor with the
coupled NSB factors pinned at nominal; default thin-layer cell; chamber corrections of docs/08 S13; n = 2000 if P is
within 0.03 of a threshold).
* **GO** if P ≥ 0.30 → order Stage 2.
* **GO-WITH-LEVER** if 0.10 ≤ P < 0.30 → order Stage 2 **and** run Stage 1C (L4 immune-complex transfer, U8) in
  parallel; adopt L4 if it meets its U8 criterion.
* **STOP** if P < 0.10 → no hardware purchase. Run Stage 1C in tubes (cheap) and re-apply the rule at **G1′** with the
  measured L4 blank reduction and recovery entered; if still < 0.10, or L4 fails U8, report to the user that 1 pg/mL
  is not reachable with this chemistry (or replace the substrate/pair first if U3/U2 drove the result).
* The modelled L4 magnitude (×0.1/0.7, UNVERIFIED) never counts toward a decision; only measured L4 values do at G1′.

Reasoning. 0.30 is the docs/05 as-specified level (~0.28): GO means the bench data put the design at least where the
priors put it before any measurement. Even a perfect label factor leaves P ≈ 0.40 (`g1_decision_table.md`, factor
0.005), because detection off-rate, free HQ and noise remain uncertain, so a threshold much above 0.30 would be
unreachable at G1 by construction. Below 0.10 the model median LOD is ≥ 3.5 pg/mL (label factor ≥ 0.10): a > 3×
gap that no lever in the model except the unmeasured L4 closes, and Stages 2–4 (≈ 24 weeks plus custom parts)
would be spent on a < 1-in-10 model chance. P is a fraction of Monte Carlo scenarios, not a probability of
success; the rule uses it as a pre-registered ranking, and the bands are wider than the Monte Carlo noise
(±0.02 at n = 2000). The one-dimensional thresholds below are fast screens with the other values at their priors;
where a screen and the rule disagree, the rule decides. This replaces the two contradicting rows of the earlier
table (U1 "0.04–0.15 proceed" and tube-B "1–4 pg/mL proceed only if P ≥ 0.3").

| Item | Go (screen) | Switch / lever | Stop (screen) | Source |
|---|---|---|---|---|
| **Model P(success), all Stage-1 values entered** | **≥ 0.30** | **0.10–0.30: Stage 2 + Stage 1C** | **< 0.10: Stage 1C only, G1′** | **this rule; `gates.yaml` G1_rule** |
| U1 label factor (design cell) | ≤ 0.02, β ≤ 1.1 | 0.03–0.08 | ≥ 0.10 | `results/design/g1_decision_table.md` (supersedes docs/05 §5 U1 0.04/0.15) |
| U3 free HQ / hydrolysis | ≤ 10⁻⁵ and ≤ 10⁻⁹ s⁻¹ | 10⁻⁵–10⁻⁴: purify or change lot, re-test | > 10⁻⁴ after purification: change substrate (AAP / p-HPP), repeat E1.2 and the model | docs/05 §5 U3 |
| U2 off-rates (E1.5 on-bead t½,eff decides; BLI gives k_on) | t½,eff ≥ 30 min and k_on ≥ 3×10⁵ → **one-step mode** (30–45 min LOD-neutral; one-step for no conjugate in the SM-FL path) | detection t½,eff 10–30 min → **sequential mode** (same hardware) | capture t½ < 1 h or detection t½,eff < 10 min → reject the pair, screen the next candidate (repeat E1.5/E1.6 only) | revised after final review, S4; `results/design/mode_choice.md` (docs/05 §5 U2's 1 h superseded) |
| Detection-on-capture R | ≤ 1.2 | 1.2–3: change species/add serum, re-test | > 3: reject pair | docs/05 §4.1 |
| Tube blank-equivalent B (E1.8) | consistency check only: B within ×2 of N_nsb(E1.3)/b | otherwise a term is missing: E1.4/E1.9 must explain it before G1 | — (no stop on B; it is near the tube readout limit, S7) | revised after final review, B3/S7 |
| U6 K_i | ≥ 2 µM | lower: design 3–5 mM HQDP / shorter accumulation | — | docs/05 §5 U6 |
| SM-FL recovery | ≥ 0.8 | 0.6–0.8: mitigation, proceed | < 0.6 after mitigation: re-plan sample path | derived here |

**Other items.** A pair rejected on U2 or detection-on-capture, or a substrate stopped on U3, is replaced and
re-measured before the rule is applied; a U3 lot in the purify band must be resolved before the first in-flow
blanks (E2.7), not before the order. The model re-run at G1 also decides: one-step vs sequential (compare P-chamb and
S-chamb with the measured k_off), whether the stringent wash is added (U1 reversibility), and whether the F(ab′)₂
label is adopted (L3 ratio).

### 4.12 Stage 1C (conditional) — U8 immune-complex transfer in tubes (T0, 3–4 weeks)

* **Trigger (revised after final review, B3).** G1a/G1 verdict GO-WITH-LEVER (run in parallel with Stage 2) or STOP
  (run alone, then G1′), or later U7 misses by 1–3× (docs/05 §5 U8).
* **Materials.** Capture antibody labelled with NHS-desthiobiotin (Thermo 16129, docs/07 §1.4) on streptavidin beads;
  D1; elution buffer AB + 2 mM D-biotin (docs/05 §5 U8); phase-2 beads carrying a second anti-human-IgG antibody
  whose epitope is not occupied by the capture or detection antibody and that does not bind the goat (or mouse)
  reagents. **The phase-2 antibody is not yet identified (UNVERIFIED)**: a candidate is a biotinylated mouse
  anti-human-IgG Fc mAb of a different epitope than the polyclonal capture; check by E1.4-type tests that it binds
  NISTmAb already carrying capture + detection antibodies.
* **Procedure.** E1.8 format with blank and 10 pg/mL (n = 6 each), with and without transfer: phase 1 as E1.8; after
  washing, elute 15 min in 50 µL elution buffer at 22 °C; magnet; transfer the eluate onto 5×10⁵ phase-2 beads in
  150 µL AB, 30 min; wash 3×, transfer, substrate, read. Also measure elution efficiency separately (conjugate
  remaining on phase-1 beads).
* **Acceptance (docs/05 §5 U8).** Adopt: blank reduced ≥ 5× with ≥ 50 % specific recovery.
* **Model expectation.** L4: NSB ×0.1 (0.01–0.5), signal ×0.7 (0.4–0.9), UNVERIFIED magnitudes
  (`ma.design_levers.immune_complex_transfer_*`); primary median 2.0 → 0.95 pg/mL, backup 2.8 → 0.94 (docs/05 §3).
* **Outcome.** Adopt → the Stage-3 hardware gets a second trap position and an elution line (+5–10 min; needs the
  7.5 min accumulation to stay ≤ 60 min, docs/05 §2). At G1′ the measured blank reduction and recovery are entered
  into the model and the §4.11 rule is re-applied. Fail (U8 criterion missed, or P still < 0.10) → **report
  non-reachability** with the
  data; the project stops before custom hardware is bought.

---

## 5. Stage 2 — the flow path on the Waters stack with purchased parts (weeks 9–16, T2)

Bought at G1 (docs/07 §2): V2 10-port and V3, V4 6-port PEEK valves, the SIA module (syringe pump + selection valve),
a magnet actuator, PEEK tubing/fittings for a simple trap, a stirred bead-reservoir holder and a separate cooled
conjugate reservoir (revised after final review, B4) and a prototype cup (a LoBind
tube in a 3-D printed or machined holder with a vent and a bottom port). Detection: the commercial single-channel
cell from Stage 1 (DropSens wall-jet) or a commercial thin-layer cell; the Gamry 600+ single channel. The
orchestration layer runs with real drivers from here on (`automation/`, §9).

| ID | Experiment (unknown) | Procedure (summary) | Measurement → parameter | Acceptance / branch (source) | Model expectation | Time |
|---|---|---|---|---|---|---|
| E2.1 | Plumbing, timing, automation | Build docs/05 §4.1 plumbing with V2, V3, V4, the prototype cup and the commercial cell (no IDA). Run the step table `automation/config/cycle_primary.yaml` with buffer only, 10 cycles; TUV at 280 nm (bead-free runs only; W3) marks protein-free tracer plugs (e.g. a dye) to time plug arrival; pressure log; force faults (unplug a valve, withhold Inject Start). Added after final review: (i) **trap flow during load_trap** measured gravimetrically at the trap outlet with the BSM at 1 µL/min A1 and the SIA at 99 µL/min, and the BSM pressure logged at 1 µL/min (S2); (ii) completeness of the A1 → B1 switch at the trap during the 1-min substrate fill, by a dye in B1 read on the TUV (W4; if incomplete, lengthen the fill or take the loop off-line, UNVERIFIED Empower option); (iii) after a forced fault, the next run is flagged invalid and the automatic recovery cycle clears the latch (S12) | step timing error, plug arrival, watchdog response, trap flow, latch behaviour | every step within ±2 s of the table; safe state reached ≤ 1 s after a fault; trap flow 100 ± 5 µL/min; B1 ≥ 95 % at the trap by the end of the fill; latch set/cleared as logged; no leaks at the restrictor pressure (derived here) | cycle 56.1 min (docs/05 §4.1) | 1 week |
| E2.2 | U5 dose CV | SIA doses 10 µL from the stirred, cooled (4–8 °C) **bead-only** reservoir (5×10⁷ beads/mL so 10 µL carries 5×10⁵) into tubes, 20 doses spread over 8 h; count by hemocytometer (n ≥ 400 beads counted per dose for ≤ 5 % Poisson CV) or by a fixed-ALP-bead signal. Also 10 doses of 10 µL from the separate conjugate reservoir, read by ALP activity (revised after final review, B4) | dose CV → `ma.capture.bead_dose_cv` | confirm ≤ 5 %; backup (fixed bed) if > 10 % (docs/05 §5 U5); conjugate dose CV ≤ 5 % | 0.05 (0.02–0.15), UNVERIFIED | 2 days |
| E2.3 | U5 trap retention | Trap = PEEK tube 0.75, 1.0, 1.5 mm ID, magnet zone 1–3 mm (actuated NdFeB block); push 5×10⁵ beads in 660 µL at 50 and 100 µL/min; collect effluent; count escaped beads (or measure ALP-bead signal in the effluent) | retention → `ma.capture.magnetic_trap_efficiency` | confirm ≥ 90 % at 100 µL/min; backup if < 70 % after two trap iterations (docs/05 §5 U5) | 0.9 (0.5–0.99), UNVERIFIED | 1 week |
| E2.4 | Cup transfer and carry-over | Sample transfer: inject 100 µL of 10 ng/mL fluorescent or UV-visible tracer into the cup by the docs/05 timing, measure fraction in the cup; bead residue after 3 SIA rinses (count in a 4th rinse) | sample transfer → chamber factor (docs/05 §4.0, 0.96); residual beads | transfer ≥ 0.95, residual beads ≤ 10⁻³ (docs/05 §5 U5) | 0.96 (docs/05 §7 chamber approximation) | 3 days |
| E2.5 | U4 wall NSB of trap and stubs | 1 cm segments (PEEK; PEG- or BSA-coated PEEK) in the trap position; one-step wall exposure: 100 µL of 1 nM conjugate at 100 µL/min, wash 1 min, seal with substrate 10 min, sweep to the cell; n = 4 per material; compare with the bead NSB product of 5×10⁵ non-immune beads in the same run | wall/bead product ratio → `ma.nsb.surface_factor_tubing` | confirm ≤ 10 % of bead NSB product; coat or re-trap if > 30 % (docs/05 §5 U4) | tubing factor 3 (1–30), UNVERIFIED; walls < 10 % of NSB in one-step mode (docs/05 §2 L2) | 1 week |
| E2.6 | Trap accumulation and readout calibration | Beads carrying a counted number of conjugates (from Stage-1 calibration, 10³–10⁶) loaded into the trap, substrate fill, 10 min sealed accumulation, 1 min sweep at 10 µL/min through the cell | charge per enzyme; cell conversion vs model (`cell_conversion` diagnostic); substrate blank current during accumulation | linear over 3 decades (r² ≥ 0.99, derived here); conversion within ×2 of the model's thin-layer/wall-jet value | P-vial diagnostics: 5.2 nC at 1 pg/mL for the IDA; thin layer 1.1–1.5× worse in LOD (docs/05 §1.2) | 3 days |
| E2.7 | First in-flow integrated runs (prototype cup) | Full one-step cycle (or sequential if G1 chose it) with automated SIA dosing: 10 blanks and 3 × (1, 10, 100, 1000 pg/mL) in random order, then 3 × (10 ng/mL challenge → B1 → B2) (S6) | B_flow, SD_blank, slope; LOD₂ = 3·SD/slope; carry-over | see G2 | primary chamber, thin-layer cell: median 3.5 [0.51–158] pg/mL today, 1.3 [0.34–9.3] after U1–U3 pass (`results/design/final_designs.md`, revised after final review; docs/05 §4.4 gave 2.0 and 0.93 with the IDA and before the S13/K_i corrections) | 1 week |

Sequential mode only (if G1 chose it): add E2.8 — conjugate carry-over in the SM-FL needle/loop into the next
injection (docs/02 §2.4c, R2): inject conjugate (3 nM, 20 µL), then the needle wash and 3 min BSM flush of the loop
at 300 µL/min that the cycle uses (no cleaning injection; revised after final review, S3), then a buffer injection
(a separate Empower line of this test, not part of the cycle) collected and assayed for ALP; acceptance ≤ 10⁻⁵ of the conjugate dose (derived here: keeps
carried enzyme below 10 % of the blank NSB at the design point). Python never needs to start Empower in either mode.

**Gate G2 (week 16).**

| Item | Go: build primary (Stage 3) | Switch | Stop / re-plan | Source |
|---|---|---|---|---|
| U5 dose CV, retention | ≤ 5 %, ≥ 90 % | 5–10 % / 70–90 %: second trap iteration | > 10 % or < 70 % after two iterations → **backup fixed micro-bed** (Stage 3B) | docs/05 §5 U5 |
| U4 wall product | ≤ 10 % of bead NSB | 10–30 %: proceed; > 30 %: coated trap (L1) or clean-zone re-trap (L2) | — | docs/05 §5 U4 |
| LOD₂ (10 blanks, commercial single-channel cell) | ≤ 1.5 pg/mL | 1.5–3 pg/mL: proceed only with a lever the model says closes the gap (L3 F(ab′)₂ label, L4 transfer, stringent wash) and re-run the model | > 3 pg/mL with all levers in the model: stop and report | derived here: the IDA gains at most ×1.1–1.5 over a thin-layer cell (docs/05 §1.2), so a single-channel LOD above 1.5 cannot reach 1 by the cell alone; 10 blanks give the SD only to −31/+83 % (§12.1), hence a factor-2 band before stopping |
| IDA + second channel (revised after final review, S9) | not needed if the electrochemical noise (S0.5/E2.6 baseline SD in the readout window, in pg/mL-equivalent) is < 30 % of the blank SD | buy (docs/07 §3 conditional items) if ≥ 30 %: then the cell term materially sets the LOD | — | derived here: blank SD adds in quadrature, so a 30 % noise share contributes ≤ 5 % of the SD; the model IDA gain is 0.02–0.05 in P today, 0.07–0.18 in favourable scenarios |
| Carry-over (10 ng/mL challenge, revised after final review, S6) | ≤ 1×10⁻⁴ | 10⁻⁴–10⁻³: add rinse volume or a cleaning cycle (SIA flush of the trap) after any sample above 1000 pg/mL | — | docs/08 S6 (supersedes docs/05 §5 U7 10⁻³) |

At G2 the model is re-run with all Stage-1 and Stage-2 values (§9); together with the IDA row above it decides
whether the IDA is worth its lead time at the measured noise and blank. The default is the commercial thin-layer
cell (revised after final review, S9).

---

## 6. Stage 3 — full primary platform (weeks 17–28, T3)

Bought at G2 (docs/07 §3; revised after final review, S9): a commercial single-channel thin-layer flow cell read by
the Reference 600+, machined stirred incubation cup, integrated bead trap screwed into V2 ports 2/3, magnet actuator
in its final form. **Only if the G2 IDA row says so:** custom flow IDA cell (or the commercial IDE chip and flow cell
as an interim) and a second potentiostat channel (a second 600+ if Gamry confirms a 600+ pair; otherwise a matched
620 pair). Backup branch (Stage 3B) instead buys the 38–52 µm streptavidin particles and column hardware.

| ID | Experiment | Procedure (summary) | Measurement → parameter | Acceptance (source) | Time |
|---|---|---|---|---|---|
| E3.1 | Cell characterisation (thin-layer default; IDA only if bought) | Thin-layer: HQ standards 1–300 nM at 10 µL/min, noise and drift per hour. IDA (conditional): CV of HQ on each finger set to set the collector potential (expected −0.1 to −0.2 V vs Ag/AgCl, UNVERIFIED, docs/05 §4.1); the collector lies only ≈ 0.1 V beyond the estimated HQ/BQ formal potential, so also measure the O₂-reduction background at the collector (air-saturated vs N₂-sparged substrate) and the sensitivity of the collector current to a ±20 mV reference shift over one day (added after final review, W6); generator-only vs generator–collector | collection efficiency, redox-cycling gain, noise per channel → `ma.geometry.ida_*`, `ma.noise.*` | gain ≥ model value used in docs/05 (flow IDA ×1.1–1.5 better than thin layer in LOD) | 1 week |
| E3.2 | Two-channel synchronisation | Two channels started from one worker (or two workers with a shared clock); square-wave test signal; time skew | skew, crosstalk | skew ≤ 10 ms (derived here: 1 % of the 1 s integration bin) | 2 days |
| E3.3 | Cup and SIA mixing | Aspirate/dispense 50 µL every 2 min (docs/05 §4.1); bead suspension homogeneity by sampling top/bottom at 0, 15, 30 min | settling; capture rate vs tube (E1.8 time course) | capture after 30 min ≥ 80 % of the rotated-tube value (derived here). Since the final review the model samples the chamber's stirred-capture factor over 0.09–0.45 of the well-mixed rate (mode 0.45, docs/08 S13); E3.3 measures it: enter (capture rate in the cup / well-mixed rate) / 2.2 as `ma.capture.in_vial_unstirred_rate_factor` for the chamber designs | 3 days |
| **E3.4** | **U7 integrated blank statistics** | 20 blanks + 5 × 1 pg/mL in random order, plus 5 × (10 ng/mL challenge → B1 → B2), unattended | CV_blank → `chem.nsb.blank_CV_analog_electrochemical`; B; LOD (mean + 3 SD); carry-over → `chem.regeneration.residual_label_carryover_fraction` | confirm CV_blank ≤ 10 %, LOD ≤ 1 pg/mL, carry-over ≤ 1×10⁻⁴ (revised after final review, S6); if CV_blank > 15 %: test L5 (reference beads, measure ρ) (docs/05 §5 U7) | 1 week |
| E3.5 | Optimisation loop | Model-chosen changes (accumulation 7.5–15 min, HQDP 1–3 mM, conjugate 0.3–1 nM, sweep flow) one at a time, 10 blanks + 3 × 3 pg/mL each | as E3.4 | improvement where the model predicts it; stop when LOD stops improving | 2–3 weeks |
| E3.6 | Unattended dry run | 24 h unattended: 20 samples with blanks/controls interleaved every 10 (docs/05 §4.1), alarms on; one forced fault mid-sequence | faults, trap clogging, drift, fault latch | zero manual interventions; mid control within ±15 % (derived here); runs between the forced fault and the logged recovery cycle flagged invalid (S12) | 2 days |

**Stage 3B (backup, only if G2 sends it).** Fixed packed micro-bed per docs/05 §4.2: 0.5 µL of 38–52 µm streptavidin
polystyrene particles (docs/07 §3B; non-porosity UNVERIFIED) loaded with the biotinylated capture antibody, in a
0.5 mm ID × 2.5 mm PEEK column screwed into V2; load at 10 µL/min (needs S0.6 to confirm BSM precision at 10 µL/min
and a narrower restrictor); glycine-HCl pH 2 regeneration by injection. Additional experiments: regeneration
capacity loss per cycle over 50 cycles (`chem.regeneration.activity_loss_per_cycle`, docs/05 §4.2: calibration check
every ~20 cycles), packed-bed NSB factor (`ma.nsb.surface_factor_packed_bed`), and whether streptavidin–biotin
survives pH 2 (UNVERIFIED). Gate as G3 with the backup's model numbers (median 2.8, P 0.16; with L4 0.94, P 0.49).

**Gate G3 (week 28).** E3.4 passes all three criteria in two independent runs on different days → Stage 4. One run
fails by ≤ 1.5× → E3.5 and repeat. Fails by > 1.5× after E3.5 → levers in model order (L3, L4, L5); if none closes
it, report the best demonstrated LOD with the evidence package of §7.

---

## 7. Stage 4 — validation protocol (weeks 28–32)

The protocol demonstrates each success criterion of docs/00 on the final, unattended configuration. Everything is
run from Empower sample sets plus the orchestration layer; the operator only loads vials and the reagent pack.

**7.1 Materials and standards.** NISTmAb RM 8671 (primary calibrator, traceable concentration; docs/01 §f) and
the polyclonal human IgG standard (subclass check). Gravimetric dilution in AB with IgG-free carrier, fresh each day,
in the clean area, in low-binding vials (QuanRecovery or the vial chosen in E1.10). Blank = sealed single-use
aliquots of the same diluent lot. At least two bead/conjugate lot combinations if available.

**7.2 Blanks.** **60 blank determinations over ≥ 3 days** (≥ 20 per day), spread through the sequences (§12.1:
with n = 60 the SD is known to −15/+22 % at 95 %; with n = 20 to −24/+46 %). CLSI EP17 verification uses ≥ 20 blank
replicates over ≥ 3 days (secondary source, docs/07 §7); 60 is used here because the claim is an establishment,
not a verification.

**7.3 Calibration design.** Levels 0, 1, 2, 5, 10, 30, 100, 300, 1000 pg/mL, triplicate per day, 3 days, run in
randomised order with a blank after every 1000 pg/mL. Fit (a) a weighted (1/y²) four-parameter logistic over the
full range for quantitation; (b) a weighted linear fit over 0–10 pg/mL (slope b) for the LOD. Acceptance (derived
here): back-calculated standards within ±20 % (±30 % at 1 and 2 pg/mL); 4PL monotonic over 1–1000 pg/mL; the
log-slope criterion of the model (`ma.statistics.uloq_min_log_slope` 0.8) reported, not imposed.

**7.4 LOD calculation (as the brief defines it; implemented in `automation/elisa_auto/stats.py`).**
* Per run signal S = baseline-corrected charge of the generator channel over the readout window (§9.2).
* Threshold y_LOD = mean(S_blank) + 3·SD(S_blank) (SD with n − 1).
* LOD = (y_LOD − a)/b from the low-range linear fit S = a + b·C, which equals 3·SD/b when the fit intercept equals
  the blank mean; the code reports both and uses the fit through the blank mean (intercept fixed at the blank mean)
  as the primary value. The 4PL inverse at y_LOD is reported for comparison.
* Also reported: LOD with the one-sided 95 % upper confidence bound of SD (χ², factor 1.18 at n = 60), the CLSI-style
  LoB = mean + 1.645·SD and LoD = LoB + 1.645·SD at 1 pg/mL, and the detection rate of 20 replicates at 1 pg/mL.
* **Pass:** LOD (point estimate, brief definition) ≤ 1.0 pg/mL on the pooled 60 blanks and on each day's 20 blanks
  using that day's calibration; the UCL-based LOD is reported (a "robust" claim if also ≤ 1.0).

**7.5 Precision.** Controls at 3, 30 and 300 pg/mL, 5 replicates per day × 5 days (design choice): repeatability
and within-lab CV by one-way ANOVA. Acceptance (derived here): CV ≤ 20 % at 3 pg/mL, ≤ 15 % at 30 and 300.

**7.6 Carry-over (revised after final review, S6).** Sequence H → B1 → B2, repeated 5 times, with H = **10 ng/mL**
NISTmAb (a challenge above the calibrated range). Carry-over = ((mean B1 − mean B2) / b) / 10 000 pg/mL, with b the
low-range slope (`stats.carryover_challenge`). Pass ≤ 1×10⁻⁴: after the top standard (1000 pg/mL) the next sample
then carries ≤ 0.1 pg/mL, a tenth of the LOD. (The docs/05 criterion 10⁻³ allowed 1 pg/mL, the LOD itself, and a
1000 pg/mL challenge cannot resolve 10⁻⁴.) n = 5 resolves 10⁻⁴ at ≈ 5σ when SD_blank ≈ 0.33 pg/mL-equivalent
(§12.5). The 1000 pg/mL → B1 → B2 sequence is still run in §7.3 and reported as indicative.

**7.7 Reuse/renewal over an unattended sequence.** One Empower sample set of ≥ 40 determinations (blanks, standards,
controls, interleaved blank + mid control every 10 samples), started once and not touched (> 24 h with overlap,
docs/05 §4.1). Pass: all determinations produce a result; no manual intervention; no trap blockage; slope of
interleaved controls drifts ≤ 10 % over the sequence (`ma.reuse.slope_drift_tolerance`); blank mean drift within
±1 SD; time from Inject Start to result ≤ 60 min for every sample (from the run log).

**7.8 Sample volume and time.** Injected volume 100 µL per determination from the Empower method (full loop);
time to result from the run log (Inject Start t₀ to computed result) for every run: max ≤ 60 min. **Definition used
(added after final review, W1):** Inject Start to the end of the post-readout baseline window (52.1 min in the
primary step table, as `automation` computes it). docs/05 quotes 56.1 min from aspiration start to cycle end; both
are ≤ 60 min, and the report states the definition next to the number.

**7.9 Specificity checks (analyte-specific).** Blank spiked with bovine IgG 1 µg/mL and mouse IgG 1 µg/mL (n = 5
each): response ≤ LOD; polyclonal human IgG standard recovery 80–120 % against NISTmAb at 10 and 100 pg/mL
(derived here) — confirms subclass and light-chain coverage beyond IgG1κ.

**7.10 The validation report (evidence).** Generated by `python -m elisa_auto.analyze bench/S4_validation/
--report` and completed by hand: system configuration (instrument IDs, firmware, Empower and Gamry versions,
automation git commit), reagent lots and CoAs, standards' gravimetric records, the full run log (every Inject Start,
valve change, fault), raw current traces of every run (stored per §9.2 with SHA-256 checksums), the blank table and
statistics, calibration fits with residuals, LOD by every definition above with confidence bounds, precision ANOVA,
carry-over, unattended-sequence summary, specificity, deviations, and a statement per success criterion (pass/fail,
the number, the data file). Raw data are never edited; exclusions only by pre-stated rules (instrument fault logged
by the watchdog), listed in the report.

---

## 8. Controls specific to human IgG at fM levels (apply in every stage)

**8.1 Human IgG contamination (Parry1997; docs/05 §4.5 point 1).**
* Dedicated pipettes and filter tips for blanks and low standards; separate pipettes for ≥ 100 pg/mL and for the
  10 mg/mL stock (stock opened in a different room or hood from blank preparation).
* Gloves changed before blank handling; no touching of face, hair or phone; lab coat sleeves closed.
* Blank diluent prepared in bulk once per lot, aliquoted into sealed single-use low-binding vials, and used as the
  "sealed instrument blank" reference (docs/05 U9).
* Order of handling always blank → low → high. High standards never share a rack with blanks.
* Every sequence contains ≥ 2 sealed blanks; a rising blank trend triggers a contamination search before data
  are accepted.

**8.2 Bovine IgG in blockers.** IgG-free BSA only (docs/07); bead stock buffers may contain BSA (docs/07 §1, M-280
lot documents) — wash beads 3× before loading; E1.4 measures the effect of a standard BSA grade. Casein and milk
(bovine) are not used unless tested as in E1.4. Capture and detection reagents cross-adsorbed against bovine IgG
("min X Bov" grades, docs/07).

**8.3 Detection reagent binding the capture antibody (Qu1998).** Same-species polyclonal pair (goat F(ab′)₂ capture,
goat F(ab′)₂ detection) or IgY detection; E1.4 acceptance R ≤ 1.2; repeated whenever a reagent lot changes (n = 6
per arm as a lot-release check).

**8.4 Carry-over between high and low samples.** Analyte path: SM-FL needle and loop (E1.10), cup and trap (E2.4,
E3.4); label path: conjugate never passes the SM-FL in one-step mode (SIA module), and in sequential mode E2.8 applies.
Every sequence: blank after the highest standard; the analysis flags any blank-after-high above the blank mean + 3 SD.
With the 10⁻⁴ criterion (§7.6) a passing system leaves ≤ 0.1 pg/mL after 1000 pg/mL, so this flag and the carry-over
gate no longer contradict each other (revised after final review, S6).

**8.5 Adsorptive loss at fM.** Low-binding PP vials/tubes (Eppendorf Protein LoBind; Waters QuanRecovery with MaxPeak
HPS, docs/07), 1 % IgG-free BSA carrier in every diluent ≤ 1 ng/mL, ≤ 1 h between dilution and injection (record),
PEEK wetted path after the injector, E1.10 recovery through the injector, and a "standards stability" control (1 and
10 pg/mL kept 0, 2, 6 h at 8 °C in the SM-FL tray, n = 3) during Stage 3.

**8.6 Others.** Temperature logged every run (no thermostat, docs/02 R12); substrate age logged (E1.2 sets the
maximum); electrode conditioning logged.

---

## 9. Data recording and the model feedback loop

**9.1 Where results go.** `bench/<stage>_<experiment>_<YYYY-MM-DD>/` with `README.md` (what, who, lots, deviations),
raw instrument files, and the filled CSV template from `automation/templates/` (u1_nsb.csv, u3_free_hq.csv,
blanks_calibration.csv, carryover.csv, dissociation.csv, bli.csv; pre_electrolysis.csv for E1.2b, not parsed by
`analyze`). Automated runs are written by the sequencer to
`bench/runs/<run_id>/` (trace, metadata, event log). `bench/measured_values.yaml` collects every model input the bench
has measured:

```yaml
ma.nsb.label_factor_igg_enzyme_conjugate: {value: 0.031, low: 0.022, high: 0.044, source: "bench/S1_E1.3_2026-12-07"}
```

**9.2 Per-run signal.** The orchestration layer stores the full current trace of both channels (time, current,
range) with metadata (run ID, sample ID from the Empower line, step table hash, reagent lots, temperature). Signal =
charge of the generator channel integrated over the readout window minus a linear baseline fitted to 30 s windows
before and after (docs/05 §4.1 "charge is integrated with baseline windows before and after"); the collector charge
is stored as a second quantity (redox-cycling check). Same code in `automation/elisa_auto/signal_proc.py` for every stage.

**9.3 Which value, which key, which re-run, which decision.**

| Bench quantity (experiment) | YAML key | Re-run | Decision it informs |
|---|---|---|---|
| label factor (design cell), β (E1.3) | `ma.nsb.label_factor_igg_enzyme_conjugate` | `python -m elisa_auto.model_feedback` (P-chamb, S-chamb, B-bed; prints the G1 verdict); `scripts/g1_decision_table.py` | G1a/G1 rule (§4.11); L4 needed? |
| wash-removable fraction (E1.3) | `ma.design_levers.nsb_fraction_removed_by_wash` (scenario only) | `scripts/robustness.py` | add stringent wash step |
| F(ab′)₂/IgG ratio (E1.3) | `ma.design_levers.fab_conjugate_nsb_factor` | `scripts/robustness.py --part levers` | label choice (L3) |
| detection-on-capture R (E1.4) | `ma.labelling.detection_on_capture_residual_factor` | model_feedback | pair acceptance |
| k_on, k_off (E1.5/E1.6) | `chem.antibodies.kon_capture`, `koff_capture`, `kon_detection`, `koff_detection` | model_feedback | one-step vs sequential mode |
| free HQ, hydrolysis, HQ t½ (E1.2) | `ma.chemistries.alp_hqdp.free_product_impurity`, `.hydrolysis_rate`, `.product_half_life` | model_feedback; `scripts/kill_thresholds.py` | substrate accept/purify/replace; B1 line vs vial |
| pre-electrolysis escape fraction f_esc, side-effect ratios (E1.2b, added 2026-11-12) | **no key**: `results.yaml` in the E1.2b folder and a comment line in `measured_values.yaml` (a non-parameter key would make `model_feedback` stop); k_h,post → `ma.chemistries.alp_hqdp.hydrolysis_rate` only as described in E1.2b | scenario runs only: `free_product_impurity` × f_esc for the guard-cell / cartridge variants (docs/12 §8 method, scratch copy) | guard cell considered at Stage 2 / kept in the cartridge design / dropped — **not** G1a/G1 |
| K_i, Km (E1.7) | `chem.enzymes.alp.phosphate_inhibition_Ki`, `ma.chemistries.alp_hqdp.Km` | `scripts/optimise_designs.py` (HQDP, accumulation) | ULOQ ≥ 1000: HQDP 1 vs 3 mM |
| B, slope (E1.8) | consistency check of the above (no key) | — | G1 consistency |
| contamination (E1.9) | `ma.nsb.blank_igg_contamination_equivalent` | model_feedback | handling SOP |
| SM-FL recovery (E1.10) | `ma.delivery.adsorptive_loss_fraction_with_carrier` | model_feedback | vials / carrier |
| dose CV, trap efficiency (E2.2/E2.3) | `ma.capture.bead_dose_cv`, `ma.capture.magnetic_trap_efficiency` | model_feedback | G2 primary vs backup |
| wall NSB (E2.5) | `ma.nsb.surface_factor_tubing` | model_feedback; robustness L1/L2 | coating / re-trap |
| noise, conversion (S0.5, E2.6, E3.1) | `ma.noise.*`, `ma.geometry.ida_*` | `scripts/final_designs.py` | IDA vs thin layer (lead-time decision) |
| CV_blank (E3.4) | `chem.nsb.blank_CV_analog_electrochemical` | model_feedback | L5 reference channel |
| carry-over (E3.4) | `chem.regeneration.residual_label_carryover_fraction` | model_feedback | rinse volume |

`model_feedback` narrows each parameter to the measured value and its interval on a copy of the parameter set (it
never edits `params/`). **Coupling found while building it:** the model's conjugate NSB rate is
`ma.nsb.label_factor_igg_enzyme_conjugate` × `chem.nsb.nsb_effective_rate_constant` (4×10⁻¹¹ m/s, sampled 8×10⁻¹² to
4×10⁻¹⁰) × `ma.nsb.surface_factor_magnetic_beads` (1–3), and the docs/05 Monte Carlo samples all three. E1.3
measures the product k_eff on the real beads, so when the label factor is entered the other two are pinned at
their nominal values (otherwise the bench value is re-spread over ~50×); the script prints a note when it does this.
The coupling code is shared with the G1 decision table (`scripts/design_lib.apply_bench_values`, revised after
final review, B3). (The example run quoted here before the review — median 2.1 → 0.82 pg/mL, P ~0.25 → ~0.64 — used
the pre-review designs and is superseded; re-run it with the current designs if needed.)
It applies the chamber approximation exactly as `scripts/final_designs.py` (thin-layer default, S13 corrections),
prints the G1 verdict of §4.11, and prints
nominal LOD, median [5–95 %] and P(success) for the primary (one-step chamber), the sequential mode and the backup,
plus a one-at-a-time ranking of the remaining sampled parameters — the largest one is the next experiment to run.
Accepted values are then entered by a model maintainer into the `overrides` section of
`params/model_assumptions.yaml` with the bench folder as source, and `python -m pytest -q` and
`scripts/final_designs.py` are re-run (the model tests must still pass; any failing validation test is a finding,
not something to tune away).

---

## 10. Schedule

One bench scientist full time, a second person part time for Stage 2–3 fabrication and wiring. Calendar weeks
counted from the Stage-0 start (assumed 2026-11-16); holidays not included.

| Weeks | Activity | Depends on | Bench days |
|---|---|---|---|
| 0 | Order Stage-1A items; BLI/SPR quote only; vendor questions | — | 1 |
| 0–2 | Stage 0 (S0.1–S0.7) | DAQ delivery for S0.3 | 5 |
| 2–3 | E1.1 readout qualification | SPEs, HQDP, HQ | 2 |
| 2–4 | E1.2 U3 (2 lots if available) | E1.1 | 3–6 |
| 3–5 | E1.3 U1 (D1, D2, repeats, reservoir-ageing arm) | E1.1, beads, conjugates | 8.5 |
| 5 | **G1a** (U1 + U3 into the model; §4.10); on GO/GO-WITH-LEVER book BLI/SPR and order NISTmAb | E1.2, E1.3 | 0.5 |
| 5–7 | E1.4, E1.5, E1.7 | E1.3 method; NISTmAb for E1.5 | 5.5 |
| 5–8 | E1.6 BLI/SPR (external) | G1a; antibodies shipped to service | 1 |
| 5–7 | E1.8 + E1.9 tube integrated assay | E1.3, NISTmAb | 3.5 |
| 5–7 | E1.2b HQDP pre-electrolysis test (informational, not a G1a/G1 input; added 2026-11-12) | E1.1 route, E1.2 lot and k_ox, D1 standard series | 4 |
| 6–7 | E1.10 SM-FL recovery | E1.8 format | 2 |
| 7–8 | **G1**, model feedback, Stage-2 orders | all Stage-1 | 1 |
| 8–12 | (Stage 1C if triggered, 3–4 weeks, in parallel with Stage-2 lead time) | G1 | 10–15 |
| 9–16 | Stage 2: E2.1–E2.7 (valve/pump lead time assumed ≤ 3 weeks, UNVERIFIED) | G1 orders | 25 |
| 12–16 | IDA cell design and quote (conditional item); Gamry decision | S0.2 answer, E2.6 | (desk) |
| 16 | **G2**; order Stage 3 | E2.2–E2.7 | 1 |
| 16–26 | IDA cell fabrication (8–12 weeks, UNVERIFIED) — only if the G2 IDA row says so | G2 | — |
| 17–24 | Stage 3 with the interim commercial IDE chip/thin-layer cell: cup, trap, E3.2, E3.3, E3.4 first pass | G2 parts (4–6 weeks for machined parts, UNVERIFIED) | 25 |
| 24–28 | E3.1 (thin-layer; custom IDA if bought), E3.4 repeat, E3.5, E3.6; **G3** | thin-layer cell (IDA delivery only if bought) | 20 |
| 28–32 | Stage 4 validation and report | G3 | 18 |

Total ≈ 32 weeks if every gate passes first time; Stage 1 answers the reachability question in ≈ 8 weeks for the
cost of reagents and a BLI service. Each failed trap/cell iteration adds 2–4 weeks; Stage 1C adds ≈ 4 weeks but runs
during the Stage-2 lead time.

---

## 11. Main risks and mitigations

| Risk | Stage hit | Likelihood (judgement) | Mitigation |
|---|---|---|---|
| U1 label factor ≥ 0.10 or model P < 0.10 at G1a/G1 (revised after final review) | G1a/G1 | moderate (docs/08 §10: model P 0.16 as specified) | Stage 1C (L4) before any hardware; F(ab′)₂ label; stringent wash; stop early if L4 fails |
| HQDP lot with free HQ > 10⁻⁴; single supplier (Metrohm DropSens) | G1 | unknown (no specification published) | test two lots; purification; AAP/pAPP alternatives tested with the same method (E1.2) |
| No detection reagent with on-bead t½ ≥ 30 min (revised after final review, S4) | G1 | moderate | sequential mode on the same hardware (docs/05 §4.0 route S); screen 3–4 candidates by BLI |
| Stage-1 readout cannot reach 1 nM HQ | Stage 1 | low–moderate | FIA-EC route (T1); gold SPE; glassy-carbon thin-layer cell; larger bead numbers |
| Bead dose CV / trap retention fail | G2 | moderate (no precedent at fM) | two trap iterations; electromagnet; backup micro-bed |
| A second channel is needed (G2 IDA row) and the 600+ cannot be paired | Stage 3 | unknown (Gamry lists 620+620, 3000+3000, 620+3000 and shows two 600+ units in a video; no 600+/620 pair) | buy a matched 620 pair; keep the 600+ for Stage 1–2 and as a third channel for L5 (revised after final review, S9) |
| ToolkitPy constraints (32-bit Python 3.7, Windows, admin rights) | Stage 2 | certain constraint | separate worker process (automation/README); pin versions; test early (S0.4) |
| Empower cannot be driven from Python | any | likely irrelevant | primary scheme does not need it (docs/02 §3.2): Empower is master, Python listens to Inject Start |
| Run-to-run NSB CV in flow > 15 % | G3 | moderate | L5 reference beads on a third channel; temperature control of cup and trap (Peltier) |
| Human-IgG contamination | all | high without SOP | §8.1; sealed blanks; E1.9 quantifies |
| Custom IDA lead time slips | Stage 3 | low (the IDA is now conditional) | thin-layer cell is the default; IDA only on the G2 condition (revised after final review, S9) |
| Temperature drift (no thermostat) | Stage 3–4 | moderate | log temperature; Peltier block on cup/trap if CV_blank correlates with temperature |

---

## 12. Statistics used to size replicates

**12.1 Blank SD.** For normally distributed blanks the relative standard error of a sample SD is ≈ 1/√(2(n − 1)),
and the 95 % χ² interval of σ is s·[√((n−1)/χ²₀.₉₇₅), √((n−1)/χ²₀.₀₂₅)] (computed with scipy for this plan):

| n blanks | rel. SE of SD | 95 % CI of σ (× s) | one-sided 95 % UCL (× s) |
|---|---|---|---|
| 5 | 35 % | 0.60–2.87 | 2.37 |
| 10 | 24 % | 0.69–1.83 | 1.65 |
| 20 | 16 % | 0.76–1.46 | 1.37 |
| 30 | 13 % | 0.80–1.34 | 1.28 |
| 60 | 9 % | 0.85–1.22 | 1.18 |

A 3-SD LOD inherits the SD's uncertainty directly. Ten blanks (Stage-2 screening) can tell 1 from 3 pg/mL but not 1
from 1.5; twenty (U7, docs/05 §5) bound the LOD to −24/+46 %; the validation claim uses 60 (§7.2).

**12.2 Gate quantities that are ratios of means** (label factor, recovery) use duplicates or triplicates: their
CV is set by the readout (≈ 10–20 %), and the label-factor screens are factor-of-5 apart (0.02 vs 0.10), so a triplicate CV of
15 % (SE ≈ 9 %) is enough; the decisive cells are repeated on a second day to catch day effects.

**12.3 Detection-on-capture ratio 1.2 (E1.4).** Log-normal CV 15 % per tube, two-sided α = 0.05: power to detect a
true ratio of 1.2 is 0.40 at n = 5, 0.73 at n = 10, **0.82 at n = 12** per arm → n = 12.

**12.4 Mean differences between blank arms (E1.9).** Minimum detectable difference at 80 % power, α = 0.05:
1.51 SD at n = 8 per arm, 1.02 SD at n = 16, 0.91 SD at n = 20. A 0.1 pg/mL contamination cannot be seen
directly when SD_blank ≈ 0.33 pg/mL (it would need ≈ 170 per arm); the amplified-handling arm multiplies it.

**12.5 Carry-over (§7.6, revised after final review, S6).** SD of (mean B1 − mean B2) with n = 5 pairs is
0.63·SD_blank; at SD_blank = 0.33 pg/mL-equivalent that is 0.21 pg/mL, and the criterion 10⁻⁴ × 10 000 pg/mL =
1 pg/mL is ≈ 5 of those. (With a 1000 pg/mL challenge 10⁻⁴ is 0.1 pg/mL, half an SD: not testable.)

**12.6 Monte Carlo is not statistics.** Model intervals quoted here are scenario ranges from the YAML bounds
(docs/05 header); they say where a bench result is expected to fall, not how certain it is. Sampling noise on a
model P is about ±0.02 (95 %) at n = 2000 and ±0.03 at n = 1000 (docs/05 §1.1's "±0.01" is one SE); differences in
P below ≈ 0.05 between designs are not decision-grade (added after final review, W7).

---

## 13. What this plan could not verify (carry into Stage 0)

* Whether the HQDP sold by Metrohm DropSens has a free-HQ specification or CoA, its lead time and lot-to-lot
  variation (product page checked: catalogue number and pack sizes only; docs/07).
* Only if the IDA option is taken: whether a Reference 600+ can be paired with a second 600+ (video on Gamry's page)
  or with a Reference 620 (not listed; Gamry lists 620+620, 3000+3000, 620+3000 and Interface pairs); whether
  ToolkitPy needs a separate licence or can drive two instruments from one process.
* Whether the Empower Toolkit can start a sample set (not needed by the primary scheme).
* Rear-panel event I/O of the installed BSM/SM-FL; Inject Start pulse width.
* HQ LOD of a drop on a carbon SPE (E1.1 measures it); collector potential of the IDA.
* A commercial anti-human-IgG detection reagent with t½ ≥ 1 h (none with published k_off found; docs/04 §3.3).
* The phase-2 antibody for immune-complex transfer (Stage 1C).
* Non-porosity of the 38–52 µm streptavidin particles for the backup; streptavidin–biotin stability at pH 2.
* Lead times for the IDEX valves, the syringe pump, machined parts and the custom IDA cell.
* CLSI EP17 replicate numbers were read only from secondary sources (docs/07 §7).
