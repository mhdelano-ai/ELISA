# 06 — Staged bench plan (Task 5)

Status: 2026-11-11. Inputs: docs/00–05, `params/*.yaml`, `results/design/`, `src/elisa_sim/`. This document plans
the bench phase for the design chosen in docs/05 (primary: renewable streptavidin magnetic beads, SIA dispenser
and stirred in-line cup, bead trap on the 10-port isolation valve, ALP/HQDP, flow IDA on two potentiostat channels;
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
| **1 Reachability** | **T0 + T1** | 2–8 | **U1** conjugate NSB, **U3** free HQ, **U2** off-rates, detection-on-capture, U6, U9, SM-FL recovery, a tube-format integrated blank-equivalent | **G1: go / switch mode / L4 only / stop** | valves, SIA pump, magnet actuator, prototype cup and trap parts (Stage 2) |
| 1C Immune-complex transfer (conditional) | T0 | +3–4 | U8 | adopt / abandon L4 | second trap position, elution line |
| 2 Flow path on the Waters | T2 | 8–16 | U5 dosing/trap, U4 wall NSB, cup transfer, first in-flow blanks | **G2: build primary / go to backup** | custom IDA cell, Reference 620, machined cup, integrated trap (Stage 3) — or the backup bed parts |
| 3 Full primary platform | T3 | 16–28 | IDA gain, two-channel readout, **U7** integrated blank statistics, unattended operation | G3: start validation | nothing new (validation consumables) |
| 4 Validation | T3 | 28–32 | the success criteria of docs/00 | final report | — |

**What Stage 1 decides.** docs/05 §0 and §3 show that two measurements decide whether 1 pg/mL is reachable at all,
for every format: the IgG–ALP conjugate NSB on blocked streptavidin beads (U1; kill at label factor > 0.15) and the
free hydroquinone in the HQDP lot (U3; kill at > 10⁻⁴ after purification). Both are measured in Stage 1 in tubes,
with a magnet and the Gamry, plus the Waters stack only as a flow-injection electrochemical (FIA-EC) reader with a
purchased wall-jet cell. No valve, pump, cup, trap or custom cell is bought before G1.

**Stage 1 cost.** About 6 weeks of one bench scientist (≈ 25 bench days, schedule §10), plus 1–3 weeks lead time
for reagents. Purchases: antibodies (capture, two detection conjugates, non-immune IgG), streptavidin beads, a
magnet rack, IgG-free BSA, HQDP (Metrohm DropSens), HQ standard, NISTmAb and a polyclonal human IgG standard,
screen-printed electrodes with connector and a wall-jet flow cell, LoBind tubes and low-binding vials, a USB DAQ for
Inject Start, plus an external BLI/SPR service (docs/07 §0–1). Indicative list prices seen in this session (not
quotes): NISTmAb ≈ 1 900 USD, magnet rack ≈ 880 USD, M-280 beads 2 mL ≈ 590 USD (offer ended 2024), IgG-free BSA
50 g ≈ 570 USD; all other prices (antibodies, HQDP, electrodes, flow cell, DAQ, BLI service) were not checked.
No instrument-class item is bought in Stage 1.

**Long-lead items** (quote in Stage 0, order at the gate): custom IDA flow cell (thin-film fabrication; lead time
UNVERIFIED, plan 8–12 weeks), Gamry Reference 620 (lead time UNVERIFIED; 600+/620 pairing UNVERIFIED — Gamry lists
620+620 and 620+3000 bipotentiostat pairs only, docs/07 §3), machined stirred cup and integrated trap (4–6 weeks,
UNVERIFIED), IDEX valves and Hamilton/Tecan syringe pump (lead time UNVERIFIED).

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
                                                    G1 (wk 7-8) --kill--> stop or Stage 1C (L4 in tubes) --> G1'
                                                      | go (one-step or sequential mode chosen)
                                    order Stage 2 parts (valves, SIA pump, magnet actuator, trap/cup prototypes)
                                                      v
                                    Stage 2 T2 (wk 9-16): plumbing+automation, U5, U4, cup, first flow blanks
                                                      |
                                                    G2 (wk 16) --U5 fail--> backup bed parts --> Stage 3B
                                                      | go
                                    order Stage 3: custom IDA cell, Ref 620 (or matched pair), machined cup, trap
                                                      v
                                    Stage 3 T3 (wk 17-28): IDA, two channels, U7, unattended runs
                                                      |
                                                    G3 (wk 28) --> Stage 4 validation (wk 28-32) --> report
```

Critical path: Stage-1 reagent delivery → U1/U3 → G1 → valve/pump delivery → U5 → G2 → custom IDA cell
fabrication → U7 → validation. The IDA cell is the longest single lead; its design and quote are done during Stage 2
so it can be ordered the day G2 passes (or earlier at the user's risk: it is needed by every bead and bed variant,
so it is the one Stage-3 item whose purchase does not depend on which branch G2 takes — only on G1).

---

## 3. Stage 0 — set-up and facts (weeks 0–2)

No gate-critical science; this stage removes "unknown installed configuration" items and puts the measuring tools
in place. Bench time ≈ 5 days.

| ID | Task | How | Output / acceptance |
|---|---|---|---|
| S0.1 | Installed facts (docs/02 §8 Q1–Q10) | Read Empower version (Help → About), BSM/SM-FL firmware (Empower instrument console), photograph BSM and SM-FL rear panels, confirm loop 100 µL and syringe size, list Gamry software version and licences (Gamry Framework → About) | A filled `bench/S0_facts/facts.md`. Needed by automation config (§9) |
| S0.2 | Vendor questions | Gamry: (a) can a Reference 600+ and a Reference 620 be synchronised as a bipotentiostat? (b) is a separate ToolkitPy licence needed? (c) can ToolkitPy run two instruments from one process? Waters: (d) can the Empower Toolkit start a sample set and report run state on this Empower version? (e) event I/O of BSM/SM-FL | Written answers filed. (a) decides docs/07 §3 option A vs B |
| S0.3 | Inject Start wiring | Wire SM-FL Inject Start (connector 1, pins 1–2, docs/02 §3.1 [V: WKB55803]) to an isolated digital input of the USB DAQ (docs/07 §0). Run `python -m elisa_auto.watch_inject` (README) and make 10 injections of buffer | Every injection logged with time stamp; pulse width recorded (UNVERIFIED today) |
| S0.4 | Lab PC | Install per `automation/README.md`; run `python -m pytest -q automation/tests` and the simulated cycle | Tests pass on the lab PC (gate G0) |
| S0.5 | Electrochemical floor | Gamry 600+: (i) dummy cell, (ii) carbon SPE with a 50 µL drop of substrate buffer, (iii) same SPE in the DropSens wall-jet cell at 50 µL/min from the BSM. Chronoamperometry at +0.35 V vs on-strip Ag, 10 min, Faraday cage | RMS noise and drift per configuration → compare with `ma.noise` and docs/02 §4.5 (3 pA in flow, 1 pA stopped; UNVERIFIED) |
| S0.6 | BSM low-flow check (the primary also depends on it: readout sweep at 10 µL/min and accumulation shunt at 10–50 µL/min, docs/05 §4.1; the backup loads at 10 µL/min — corrected by the final review, docs/08) | Gravimetric: 1, 10, 20, 100 µL/min into a weighed vial, 30 min each, 3 repeats, with the restrictor fitted | Flow error and CV; confirms or refutes `hw.bsm.flow_min` = 1 µL/min (docs/00 user statement) |
| S0.7 | Clean-handling set-up | §8.1: dedicated pipettes, filter tips, LoBind tubes, "IgG-free" bench area, glove changes, sealed blank stock | SOP written into `bench/SOP_clean_handling.md` |
| S0.8 | Orders and quotes | Order all Stage-1 items (docs/07 §1); book BLI/SPR; ask for quotes and lead times for Stage 2/3 items without ordering | Purchase log |

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
  are made identically with biotinylated non-immune IgG of the capture antibody's species at the same mass loading.
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
     reservoir bottle if the solvent line is used: 0, 1, 2, 4, 8 h, triplicate reads.
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
* **Time.** 3 days per lot (time course over one day; the rest is preparation and repeats).
* **Outcomes.** Confirm → G1 U3 item passed. Purify range → ask the vendor for a lower-HQ lot and try a clean-up
  (UNVERIFIED route; for example recrystallisation or removal of the phenolic impurity by solid-phase extraction,
  to be designed with a chemist), re-run E1.2 on the purified material. Kill → E1.2 on the alternative substrates
  (docs/07 §1 lists 4-aminophenyl phosphate and ascorbic-acid-2-phosphate; p-hydroxyphenyl phosphate supply
  UNVERIFIED); re-run the model with `ma.chemistries.alp_aap` / `alp_papp` and their measured values.
  Also: if k_h > 10⁻⁹ s⁻¹ but f_free passes, deliver substrate from a 4 °C vial instead of the B1 line (docs/02 R8)
  and re-check the cycle time.

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
* **Acceptance (docs/05 §5 U1).** Confirm primary: factor ≤ 0.04, linear or sub-linear in exposure (β ≤ 1.1, derived
  here as "not super-linear" within the CI). Kill the 1 pg/mL target for all formats (go to L4 transfer, Stage
  1C): factor > 0.15. Between: proceed with L4 development in parallel (U8). Add the stringent wash step if ≥ 30 %
  is removed by stringent washes (S3a). The F(ab′)₂/IgG ratio sets L3.
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
  plus 1 repeat day of the decisive cells (0.3 nM × 30 min and 1 nM × 30 min).
* **Outcomes.** See G1 (§4.11). Additional branches: β > 1.1 (super-linear: e.g. aggregates in the conjugate) →
  centrifuge/filter the conjugate (0.22 µm low-binding, or 10 min at 16 000 g) and repeat the 1 and 3 nM points;
  bead-number arm not proportional (± 30 %) → NSB is not area-limited (tube walls, carry-over); repeat with two
  transfers before substrate.

### E1.4 — Detection-on-capture and bovine-IgG cross-reaction

* **Purpose.** docs/05 §4.1 acceptance "blank on capture beads ≤ 1.2× blank on non-immune beads" (Qu1998: up to
  15× when not suppressed); docs/05 §4.5 points 1–2. Tier: T0.
* **Materials.** Capture beads (biotinylated anti-human-Fc), non-immune beads, D1, AB made with (a) IgG-free BSA,
  (b) a standard BSA grade (bovine IgG present per vendor, `chem.nsb.bovine_IgG_in_BSA`), (c) the bead stock buffer
  carried over vs beads washed 3× before loading.
* **Procedure.** No analyte. 5×10⁵ beads (design number), D1 at 0.3 nM, 30 min, the E1.3 wash/transfer/substrate
  steps; readout E1.1. Arms: capture vs non-immune beads in AB(a), **n = 12 each** (power 0.8 to see a true 1.2× ratio at 15 % CV, §12.3); capture beads in
  AB(b) n = 5; unwashed bead stock n = 5. Include the conjugate standard series.
* **Measurement → parameter.** Ratio R = N(capture)/N(non-immune) with 95 % CI (log scale) →
  `ma.labelling.detection_on_capture_residual_factor` (model 1, range 1–3). Bovine-BSA ratio → choice of blocker.
* **Acceptance.** R ≤ 1.2 (docs/05 §4.1), read as point estimate ≤ 1.2 with the upper 95 % bound < 1.5 (derived here: n = 12 cannot prove ≤ 1.2 more tightly). Standard BSA ≤ 1.2× IgG-free BSA, else IgG-free blockers only.
* **Model expectation.** R = 1 (1–3) in the model for a suppressed pair; at the design point N ≈ 6.4×10³ on 5×10⁵
  beads (≈ 0.8 nM in 50 µL at 0.3 mM HQDP over 60 min) — near the E1.1 limit; therefore if the readout cannot
  resolve it, repeat at 5×10⁶ beads and 1 nM (≈ 2×10⁵, comfortably measurable).
* **Time.** 2 days.
* **Outcomes.** R ≤ 1.2: pair accepted. R > 1.2: change the capture species (e.g. goat F(ab′)₂ capture with goat
  detection; docs/01 §d point 3) or add 0.25 % normal serum of the capture species to AB (Qu1998), re-test. R > 3:
  reject the pair.

### E1.5 — U2 (bench part): dissociation of the sandwich on beads

* **Purpose.** Effective off-rate of the labelled complex on beads, which is what matters during the chamber
  emptying (6.6 min) and washes (docs/05 §3: detection t½ ≈ 13 min drives the one-step upper tail). Complements BLI
  (E1.6). Tier: T0.
* **Procedure.** 5×10⁶ capture beads + NISTmAb 100 pg/mL in 1 mL AB, 30 min; wash; D1 1 nM 30 min; wash 3×,
  transfer. Resuspend in 1 mL AB containing an unlabelled scavenger for released conjugate (10 µg/mL normal human
  IgG — binds released detection reagent and prevents re-binding) at 22 °C, rotating. Remove aliquots of beads at 0,
  15, 30, 60, 120 min (triplicate tubes per time point, set up in parallel), wash, substrate, read.
  Control: non-immune beads treated the same (NSB decay).
* **Measurement → parameter.** Fit N(t) = N₀·exp(−k_eff·t) (+ NSB control) → effective k_off of the complex. If
  t½,eff ≥ 1 h, both k_off,capture and k_off,detection ≤ 1.9×10⁻⁴ s⁻¹ (bound only — the loss rate is their sum).
  Updates `chem.antibodies.koff_detection` (and capture) bounds with BLI.
* **Acceptance (docs/05 §5 U2).** One-step mode: t½ ≥ 1 h (both reagents) and k_on ≥ 3×10⁵ M⁻¹s⁻¹ (k_on from BLI).
  Sequential mode: detection t½ 10–60 min. Reject: capture t½ < 1 h or detection t½ < 10 min.
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
  antibody) at 5 concentrations, dissociate 1800 s. Global 1:1 fit; report χ² and residuals. Two to four candidates
  per role.
* **Measurement → parameters.** `chem.antibodies.kon_capture`, `koff_capture`, `kon_detection`, `koff_detection`
  (value = fit, low/high = 95 % CI or the spread of repeats).
* **Acceptance.** As E1.5 (docs/05 §5 U2; §4.1 table: k_on ≥ 3×10⁵ M⁻¹s⁻¹, k_off ≤ 1.9×10⁻⁴ s⁻¹).
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
* **Procedure.** Per tube: 20 µL bead + conjugate mix (5×10⁵ beads, conjugate to give 0.3 nM final) + 200 µL standard
  or blank (AB from the sealed blank stock), 30 min rotating at 22 °C (docs/05 §4.1 incubation), wash 3×, transfer,
  50 µL SB + 1 mM HQDP for 60 min, read. Blanks **n = 10**, each standard level n = 3, polyclonal n = 3, plus the
  conjugate standard series and no-bead SB blanks (n = 4). Randomise tube order; record times.
* **Measurement → parameters.** Slope b (enzymes per pg/mL) from a weighted linear fit over 0–30 pg/mL; B = (mean
  blank − no-bead SB blank)/b; LOD_tube = 3·SD_blank/b (indicative only: tube handling adds variance the instrument
  will not have). Captured-and-labelled fraction = b / (IgG molecules per pg/mL in 200 µL = 8.0×10⁵; 1 pg/mL of a
  150 kDa IgG is 4.0×10⁵ molecules per 100 µL, docs/00) → compare with the model (P-vial reference: 6.8×10³ labelled
  enzymes per pg/mL for 100 µL of sample, i.e. a captured-and-labelled fraction of ≈ 1.7 %, with label retention
  0.77 and capture retention 0.97 in the model diagnostics).
* **Acceptance (docs/05 §0 and §5 U1 in blank-equivalent form).** Confirm: B ≤ ~1 pg/mL on beads. Kill-level:
  B > 4 pg/mL. Consistency (derived here): B within a factor 2 of N_nsb(E1.3, same exposure) / b; otherwise a term
  is missing (contamination, detection-on-capture, bead ALP background) and E1.4/E1.9 must explain it before G1.
* **Model expectation.** P-vial reference nominal: B = 0.96 pg/mL, N_nsb = 6.4×10³, 6.8×10³ enzymes at 1 pg/mL,
  LOD 0.32 pg/mL nominal (median 1.3 [0.30–21] with model readout noise, docs/05 §1.2). In the tube with a 50 µL
  readout, 1 pg/mL is ≈ 0.8–1.6 nM HQ (6.8×10³–1.4×10⁴ enzymes, 60 min, k_cat 1000 s⁻¹ UNVERIFIED) over a ≈ 10 nM free-HQ background at 1 mM HQDP — the tube LOD is
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
  in ≥ 1/3 of tip-cone eluates in every lab tested.
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
  3 loop volumes (300 µL, 3 min). Then inject a blank and collect it. n = 3 per arm. Assay the collected fractions
  in the E1.8 tube format (add beads + conjugate to the collected 300 µL; adjust the standard curve to the same
  volume) against identical standards that did not pass the injector.
* **Measurement → parameters.** Recovery = signal(passed)/signal(not passed) → 1 − `adsorptive_loss_fraction_with_carrier`
  and `ma.delivery.delivered_fraction_full_loop_100`; analyte carry-over = blank-after-100 / 100 pg/mL.
* **Acceptance (derived here).** Recovery ≥ 0.8 (the model nominal), analyte carry-over ≤ 10⁻³ (docs/05 §5 U7
  criterion applied to the injector alone).
* **Time.** 2 days.
* **Outcome.** Recovery < 0.6 → change vials, raise carrier to 2 % or add 0.01 % Tween to the diluent, consider a
  PEEK/HPS loop (docs/02 R1); re-test before Stage 2 depends on it.

### 4.11 Gate G1 (end of week 7–8) — is 1 pg/mL reachable, and in which mode?

Evaluate with `python -m elisa_auto.analyze bench/` (prints every quantity below with its CI) and
`python -m elisa_auto.model_feedback bench/measured_values.yaml` (model P(success) of the primary, the sequential
fallback and the backup with the measured values).

| Item | Go (primary) | Switch | Kill / stop | Source |
|---|---|---|---|---|
| U1 label factor | ≤ 0.04, β ≤ 1.1 | 0.04–0.15: proceed **and** run Stage 1C (L4 transfer, U8) in parallel with Stage 2 | > 0.15: stop hardware purchases; Stage 1C only; if L4 fails its criterion, report to the user that 1 pg/mL is not reachable with this chemistry | docs/05 §5 U1 |
| U3 free HQ / hydrolysis | ≤ 10⁻⁵ and ≤ 10⁻⁹ s⁻¹ | 10⁻⁵–10⁻⁴: purify or change lot, re-test | > 10⁻⁴ after purification: change substrate (AAP / p-HPP), repeat E1.2 and the model | docs/05 §5 U3 |
| U2 off-rates | both t½ ≥ 1 h and k_on ≥ 3×10⁵ → **one-step mode** | detection t½ 10–60 min → **sequential mode** (same hardware) | capture t½ < 1 h or detection t½ < 10 min → reject the pair, screen the next candidate (repeat E1.5/E1.6 only) | docs/05 §5 U2 |
| Detection-on-capture R | ≤ 1.2 | 1.2–3: change species/add serum, re-test | > 3: reject pair | docs/05 §4.1 |
| Tube blank-equivalent B | ≤ ~1 pg/mL and consistent with U1 | 1–4 pg/mL: proceed only if the model with all Stage-1 values gives P(success) ≥ 0.3 for some admissible design (derived here) | > 4 pg/mL | docs/05 §0, §5 U1 |
| U6 K_i | ≥ 2 µM | lower: design 3–5 mM HQDP / shorter accumulation | — | docs/05 §5 U6 |
| SM-FL recovery | ≥ 0.8 | 0.6–0.8: mitigation, proceed | < 0.6 after mitigation: re-plan sample path | derived here |

**Decision rule.** No "Kill" and U1, U3 in their "Go" or "Switch" band → order Stage 2 (docs/07 §2); a U3 lot in the
purify band must be resolved before the first in-flow blanks (E2.7), not before the order. Any "Kill" → no Stage-2
purchase; Stage 1C or substrate/pair replacement first. The tube-B "Switch" rule uses P(success) ≥ 0.3, i.e. not
worse than the docs/05 as-specified level (~0.28) once the Stage-1 values replace the priors. The model re-run at G1 also decides: one-step vs sequential (compare P-chamb and
S-chamb with the measured k_off), whether the stringent wash is added (U1 reversibility), and whether the F(ab′)₂
label is adopted (L3 ratio).

### 4.12 Stage 1C (conditional) — U8 immune-complex transfer in tubes (T0, 3–4 weeks)

* **Trigger.** U1 factor 0.04–0.15 or > 0.15, or later U7 misses by 1–3× (docs/05 §5 U8).
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
  7.5 min accumulation to stay ≤ 60 min, docs/05 §2). Fail and U1 > 0.15 → **report non-reachability** with the
  data; the project stops before custom hardware is bought.

---

## 5. Stage 2 — the flow path on the Waters stack with purchased parts (weeks 9–16, T2)

Bought at G1 (docs/07 §2): V2 10-port and V3, V4 6-port PEEK valves, the SIA module (syringe pump + selection valve),
a magnet actuator, PEEK tubing/fittings for a simple trap, a stirred-reservoir holder and a prototype cup (a LoBind
tube in a 3-D printed or machined holder with a vent and a bottom port). Detection: the commercial single-channel
cell from Stage 1 (DropSens wall-jet) or a commercial thin-layer cell; the Gamry 600+ single channel. The
orchestration layer runs with real drivers from here on (`automation/`, §9).

| ID | Experiment (unknown) | Procedure (summary) | Measurement → parameter | Acceptance / branch (source) | Model expectation | Time |
|---|---|---|---|---|---|---|
| E2.1 | Plumbing, timing, automation | Build docs/05 §4.1 plumbing with V2, V3, V4, the prototype cup and the commercial cell (no IDA). Run the step table `automation/config/cycle_primary.yaml` with buffer only, 10 cycles; TUV at 280 nm marks protein-free tracer plugs (e.g. 0.1 mg/mL BSA or a dye) to time plug arrival; pressure log; force faults (unplug a valve, withhold Inject Start) | step timing error, plug arrival, watchdog response | every step within ±2 s of the table; safe state reached ≤ 1 s after a fault; no leaks at the restrictor pressure (derived here) | cycle 56.1 min (docs/05 §4.1) | 1 week |
| E2.2 | U5 dose CV | SIA doses 20 µL from the stirred, cooled (4–8 °C) reservoir of capture beads (design concentration ×11 so 20 µL carries 5×10⁵) into tubes, 20 doses spread over 8 h; count by hemocytometer (n ≥ 400 beads counted per dose for ≤ 5 % Poisson CV) or by a fixed-ALP-bead signal | dose CV → `ma.capture.bead_dose_cv` | confirm ≤ 5 %; backup (fixed bed) if > 10 % (docs/05 §5 U5) | 0.05 (0.02–0.15), UNVERIFIED | 2 days |
| E2.3 | U5 trap retention | Trap = PEEK tube 0.75, 1.0, 1.5 mm ID, magnet zone 1–3 mm (actuated NdFeB block); push 5×10⁵ beads in 660 µL at 50 and 100 µL/min; collect effluent; count escaped beads (or measure ALP-bead signal in the effluent) | retention → `ma.capture.magnetic_trap_efficiency` | confirm ≥ 90 % at 100 µL/min; backup if < 70 % after two trap iterations (docs/05 §5 U5) | 0.9 (0.5–0.99), UNVERIFIED | 1 week |
| E2.4 | Cup transfer and carry-over | Sample transfer: inject 100 µL of 10 ng/mL fluorescent or UV-visible tracer into the cup by the docs/05 timing, measure fraction in the cup; bead residue after 3 SIA rinses (count in a 4th rinse) | sample transfer → chamber factor (docs/05 §4.0, 0.96); residual beads | transfer ≥ 0.95, residual beads ≤ 10⁻³ (docs/05 §5 U5) | 0.96 (docs/05 §7 chamber approximation) | 3 days |
| E2.5 | U4 wall NSB of trap and stubs | 1 cm segments (PEEK; PEG- or BSA-coated PEEK) in the trap position; one-step wall exposure: 100 µL of 1 nM conjugate at 100 µL/min, wash 1 min, seal with substrate 10 min, sweep to the cell; n = 4 per material; compare with the bead NSB product of 5×10⁵ non-immune beads in the same run | wall/bead product ratio → `ma.nsb.surface_factor_tubing` | confirm ≤ 10 % of bead NSB product; coat or re-trap if > 30 % (docs/05 §5 U4) | tubing factor 3 (1–30), UNVERIFIED; walls < 10 % of NSB in one-step mode (docs/05 §2 L2) | 1 week |
| E2.6 | Trap accumulation and readout calibration | Beads carrying a counted number of conjugates (from Stage-1 calibration, 10³–10⁶) loaded into the trap, substrate fill, 10 min sealed accumulation, 1 min sweep at 10 µL/min through the cell | charge per enzyme; cell conversion vs model (`cell_conversion` diagnostic); substrate blank current during accumulation | linear over 3 decades (r² ≥ 0.99, derived here); conversion within ×2 of the model's thin-layer/wall-jet value | P-vial diagnostics: 5.2 nC at 1 pg/mL for the IDA; thin layer 1.1–1.5× worse in LOD (docs/05 §1.2) | 3 days |
| E2.7 | First in-flow integrated runs (prototype cup) | Full one-step cycle (or sequential if G1 chose it) with automated SIA dosing: 10 blanks and 3 × (1, 10, 100, 1000 pg/mL) in random order, blank after each 1000 | B_flow, SD_blank, slope; LOD₂ = 3·SD/slope; carry-over | see G2 | primary chamber median 2.0 [0.36–73] today, 0.93 [0.23–4.9] after U1–U3 pass (docs/05 §4.4) | 1 week |

Sequential mode only (if G1 chose it): add E2.8 — conjugate carry-over in the SM-FL needle/loop into the next
injection (docs/02 §2.4c, R2): inject conjugate (3 nM, 20 µL), then the cleaning injection, then a buffer
"substrate" plug collected and assayed for ALP; acceptance ≤ 10⁻⁵ of the conjugate dose (derived here: keeps
carried enzyme below 10 % of the blank NSB at the design point). Python never needs to start Empower in either mode.

**Gate G2 (week 16).**

| Item | Go: build primary (Stage 3) | Switch | Stop / re-plan | Source |
|---|---|---|---|---|
| U5 dose CV, retention | ≤ 5 %, ≥ 90 % | 5–10 % / 70–90 %: second trap iteration | > 10 % or < 70 % after two iterations → **backup fixed micro-bed** (Stage 3B) | docs/05 §5 U5 |
| U4 wall product | ≤ 10 % of bead NSB | 10–30 %: proceed; > 30 %: coated trap (L1) or clean-zone re-trap (L2) | — | docs/05 §5 U4 |
| LOD₂ (10 blanks, commercial single-channel cell) | ≤ 1.5 pg/mL | 1.5–3 pg/mL: proceed only with a lever the model says closes the gap (L3 F(ab′)₂ label, L4 transfer, stringent wash) and re-run the model | > 3 pg/mL with all levers in the model: stop and report | derived here: the IDA gains at most ×1.1–1.5 over a thin-layer cell (docs/05 §1.2), so a single-channel LOD above 1.5 cannot reach 1 by the cell alone; 10 blanks give the SD only to −31/+83 % (§12.1), hence a factor-2 band before stopping |
| Carry-over after 1000 pg/mL | ≤ 10⁻³ | 10⁻³–10⁻²: add rinse volume or a cleaning injection | — | docs/05 §5 U7 |

At G2 the model is re-run with all Stage-1 and Stage-2 values (§9); it also tells whether the IDA is worth its lead
time at the measured noise and blank (if the measured blank SD is ≫ the electrochemical noise, as the model expects,
the IDA gain is small and a thin-layer cell may be kept, saving the longest lead item — a decision the model makes
from data rather than the plan).

---

## 6. Stage 3 — full primary platform (weeks 17–28, T3)

Bought at G2 (docs/07 §3): custom flow IDA cell (or the commercial IDE chip and flow cell as an interim), second
potentiostat channel (Reference 620 — paired with the 600+ only if Gamry confirms; otherwise a matched 620 pair),
machined stirred incubation cup, integrated bead trap screwed into V2 ports 2/3, magnet actuator in its
final form. Backup branch (Stage 3B) instead buys the 38–52 µm streptavidin particles and column hardware.

| ID | Experiment | Procedure (summary) | Measurement → parameter | Acceptance (source) | Time |
|---|---|---|---|---|---|
| E3.1 | IDA characterisation | CV of HQ on each finger set to set the collector potential (expected −0.1 to −0.2 V vs Ag/AgCl, UNVERIFIED, docs/05 §4.1); HQ standards 1–300 nM at 10 µL/min; generator-only vs generator–collector | collection efficiency, redox-cycling gain, noise per channel → `ma.geometry.ida_*`, `ma.noise.*` | gain ≥ model value used in docs/05 (flow IDA ×1.1–1.5 better than thin layer in LOD) | 1 week |
| E3.2 | Two-channel synchronisation | Two channels started from one worker (or two workers with a shared clock); square-wave test signal; time skew | skew, crosstalk | skew ≤ 10 ms (derived here: 1 % of the 1 s integration bin) | 2 days |
| E3.3 | Cup and SIA mixing | Aspirate/dispense 50 µL every 2 min (docs/05 §4.1); bead suspension homogeneity by sampling top/bottom at 0, 15, 30 min | settling; capture rate vs tube (E1.8 time course) | capture after 30 min ≥ 80 % of the rotated-tube value (derived here: chamber approximation uses 0.45 of the tube rate, docs/05 §7, so this is a check of that assumption) | 3 days |
| **E3.4** | **U7 integrated blank statistics** | 20 blanks + 5 × 1 pg/mL in random order, plus 3 × (blank after 1000 pg/mL), unattended | CV_blank → `chem.nsb.blank_CV_analog_electrochemical`; B; LOD (mean + 3 SD); carry-over → `chem.regeneration.residual_label_carryover_fraction` | confirm CV_blank ≤ 10 %, LOD ≤ 1 pg/mL, carry-over ≤ 10⁻³; if CV_blank > 15 %: test L5 (reference beads, measure ρ) (docs/05 §5 U7) | 1 week |
| E3.5 | Optimisation loop | Model-chosen changes (accumulation 7.5–15 min, HQDP 1–3 mM, conjugate 0.3–1 nM, sweep flow) one at a time, 10 blanks + 3 × 3 pg/mL each | as E3.4 | improvement where the model predicts it; stop when LOD stops improving | 2–3 weeks |
| E3.6 | Unattended dry run | 24 h unattended: 20 samples with blanks/controls interleaved every 10 (docs/05 §4.1), alarms on | faults, trap clogging, drift | zero manual interventions; mid control within ±15 % (derived here) | 2 days |

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

**7.6 Carry-over.** Sequence H (1000 pg/mL) → B1 → B2, repeated 5 times. Carry-over = (mean B1 − mean B2)/(mean H −
mean B2). Pass ≤ 10⁻³ (docs/05 §5 U7). n = 5 resolves 10⁻³ at ≈ 5σ when SD_blank ≈ 0.33 pg/mL-equivalent (§12.5).

**7.7 Reuse/renewal over an unattended sequence.** One Empower sample set of ≥ 40 determinations (blanks, standards,
controls, interleaved blank + mid control every 10 samples), started once and not touched (> 24 h with overlap,
docs/05 §4.1). Pass: all determinations produce a result; no manual intervention; no trap blockage; slope of
interleaved controls drifts ≤ 10 % over the sequence (`ma.reuse.slope_drift_tolerance`); blank mean drift within
±1 SD; time from Inject Start to result ≤ 60 min for every sample (from the run log).

**7.8 Sample volume and time.** Injected volume 100 µL per determination from the Empower method (full loop);
time to result from the run log (Inject Start t₀ to computed result) for every run: max ≤ 60 min.

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
blanks_calibration.csv, carryover.csv, dissociation.csv, bli.csv). Automated runs are written by the sequencer to
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
| label factor, β (E1.3) | `ma.nsb.label_factor_igg_enzyme_conjugate` | `python -m elisa_auto.model_feedback` (P-chamb, S-chamb, B-bed); `scripts/kill_thresholds.py` | G1 reachability; L4 needed? |
| wash-removable fraction (E1.3) | `ma.design_levers.nsb_fraction_removed_by_wash` (scenario only) | `scripts/robustness.py` | add stringent wash step |
| F(ab′)₂/IgG ratio (E1.3) | `ma.design_levers.fab_conjugate_nsb_factor` | `scripts/robustness.py --part levers` | label choice (L3) |
| detection-on-capture R (E1.4) | `ma.labelling.detection_on_capture_residual_factor` | model_feedback | pair acceptance |
| k_on, k_off (E1.5/E1.6) | `chem.antibodies.kon_capture`, `koff_capture`, `kon_detection`, `koff_detection` | model_feedback | one-step vs sequential mode |
| free HQ, hydrolysis, HQ t½ (E1.2) | `ma.chemistries.alp_hqdp.free_product_impurity`, `.hydrolysis_rate`, `.product_half_life` | model_feedback; `scripts/kill_thresholds.py` | substrate accept/purify/replace; B1 line vs vial |
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
With the example values in `automation/templates/measured_values.example.yaml` (factor 0.031, free HQ 8×10⁻⁶,
k_off,det 3×10⁻⁴ s⁻¹ — illustrative numbers, not data) the primary moves from median 2.1 to 0.82 pg/mL and
P(success) ~0.25 → ~0.64 (n = 500), and the ranking then names k_on of the detection reagent, human-IgG
contamination and k_on of the capture reagent as the next most informative measurements — i.e. E1.6 and E1.9.
It applies the docs/05 chamber approximation exactly as `scripts/final_designs.py`, and prints
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
| 0 | Order Stage-1 items; book BLI/SPR; vendor questions | — | 1 |
| 0–2 | Stage 0 (S0.1–S0.7) | DAQ delivery for S0.3 | 5 |
| 2–3 | E1.1 readout qualification | SPEs, HQDP, HQ | 2 |
| 2–4 | E1.2 U3 (2 lots if available) | E1.1 | 3–6 |
| 3–5 | E1.3 U1 (D1, D2, repeats) | E1.1, beads, conjugates | 7 |
| 4–6 | E1.4, E1.5, E1.7 | E1.3 method | 5.5 |
| 4–7 | E1.6 BLI/SPR (external) | antibodies shipped to service | 1 |
| 5–7 | E1.8 + E1.9 tube integrated assay | E1.3, NISTmAb | 3.5 |
| 6–7 | E1.10 SM-FL recovery | E1.8 format | 2 |
| 7–8 | **G1**, model feedback, Stage-2 orders | all Stage-1 | 1 |
| 8–12 | (Stage 1C if triggered, 3–4 weeks, in parallel with Stage-2 lead time) | G1 | 10–15 |
| 9–16 | Stage 2: E2.1–E2.7 (valve/pump lead time assumed ≤ 3 weeks, UNVERIFIED) | G1 orders | 25 |
| 12–16 | IDA cell design and quote; Gamry decision | S0.2 answer, E2.6 | (desk) |
| 16 | **G2**; order Stage 3 | E2.2–E2.7 | 1 |
| 16–26 | IDA cell fabrication (8–12 weeks, UNVERIFIED) | G2 | — |
| 17–24 | Stage 3 with the interim commercial IDE chip/thin-layer cell: cup, trap, E3.2, E3.3, E3.4 first pass | G2 parts (4–6 weeks for machined parts, UNVERIFIED) | 25 |
| 24–28 | E3.1 with the custom IDA, E3.4 repeat, E3.5, E3.6; **G3** | IDA delivery | 20 |
| 28–32 | Stage 4 validation and report | G3 | 18 |

Total ≈ 32 weeks if every gate passes first time; Stage 1 answers the reachability question in ≈ 8 weeks for the
cost of reagents and a BLI service. Each failed trap/cell iteration adds 2–4 weeks; Stage 1C adds ≈ 4 weeks but runs
during the Stage-2 lead time.

---

## 11. Main risks and mitigations

| Risk | Stage hit | Likelihood (judgement) | Mitigation |
|---|---|---|---|
| U1 label factor > 0.15 (NSB at the old SβG level, scenario S1) | G1 | moderate (docs/05: ~15 % overall success today) | Stage 1C (L4) before any hardware; F(ab′)₂ label; stringent wash; stop early if L4 fails |
| HQDP lot with free HQ > 10⁻⁴; single supplier (Metrohm DropSens) | G1 | unknown (no specification published) | test two lots; purification; AAP/pAPP alternatives tested with the same method (E1.2) |
| No commercial detection reagent with t½ ≥ 1 h | G1 | moderate | sequential mode on the same hardware (docs/05 §4.0 route S); screen 3–4 candidates by BLI |
| Stage-1 readout cannot reach 1 nM HQ | Stage 1 | low–moderate | FIA-EC route (T1); gold SPE; glassy-carbon thin-layer cell; larger bead numbers |
| Bead dose CV / trap retention fail | G2 | moderate (no precedent at fM) | two trap iterations; electromagnet; backup micro-bed |
| 600+/620 cannot be paired | Stage 3 | unknown (Gamry lists 620+620, 620+3000 only) | buy a matched 620 pair; keep the 600+ for Stage 1–2 and as a third channel for L5 |
| ToolkitPy constraints (32-bit Python 3.7, Windows, admin rights) | Stage 2 | certain constraint | separate worker process (automation/README); pin versions; test early (S0.4) |
| Empower cannot be driven from Python | any | likely irrelevant | primary scheme does not need it (docs/02 §3.2): Empower is master, Python listens to Inject Start |
| Run-to-run NSB CV in flow > 15 % | G3 | moderate | L5 reference beads on a third channel; temperature control of cup and trap (Peltier) |
| Human-IgG contamination | all | high without SOP | §8.1; sealed blanks; E1.9 quantifies |
| Custom IDA lead time slips | Stage 3 | moderate | interim commercial IDE chip + flow cell or thin-layer cell (≤ 1.5× LOD penalty); IDA decision by the model at G2 |
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
CV is set by the readout (≈ 10–20 %), and the gates are factor-of-4 apart (0.04 vs 0.15), so a triplicate CV of
15 % (SE ≈ 9 %) is enough; the decisive cells are repeated on a second day to catch day effects.

**12.3 Detection-on-capture ratio 1.2 (E1.4).** Log-normal CV 15 % per tube, two-sided α = 0.05: power to detect a
true ratio of 1.2 is 0.40 at n = 5, 0.73 at n = 10, **0.82 at n = 12** per arm → n = 12.

**12.4 Mean differences between blank arms (E1.9).** Minimum detectable difference at 80 % power, α = 0.05:
1.51 SD at n = 8 per arm, 1.02 SD at n = 16, 0.91 SD at n = 20. A 0.1 pg/mL contamination cannot be seen
directly when SD_blank ≈ 0.33 pg/mL (it would need ≈ 170 per arm); the amplified-handling arm multiplies it.

**12.5 Carry-over (§7.6).** SD of (mean B1 − mean B2) with n = 5 pairs is 0.63·SD_blank; at SD_blank =
0.33 pg/mL-equivalent that is 0.21 pg/mL, and the criterion 10⁻³ × 1000 pg/mL = 1 pg/mL is ≈ 5 of those.

**12.6 Monte Carlo is not statistics.** Model intervals quoted here are scenario ranges from the YAML bounds
(docs/05 header); they say where a bench result is expected to fall, not how certain it is.

---

## 13. What this plan could not verify (carry into Stage 0)

* Whether the HQDP sold by Metrohm DropSens has a free-HQ specification or CoA, its lead time and lot-to-lot
  variation (product page checked: catalogue number and pack sizes only; docs/07).
* Whether a Reference 600+ can be paired with a Reference 620 (Gamry lists only 620+620 and 620+3000 pairs); whether
  ToolkitPy needs a separate licence or can drive two instruments from one process.
* Whether the Empower Toolkit can start a sample set (not needed by the primary scheme).
* Rear-panel event I/O of the installed BSM/SM-FL; Inject Start pulse width.
* HQ LOD of a drop on a carbon SPE (E1.1 measures it); collector potential of the IDA.
* A commercial anti-human-IgG detection reagent with t½ ≥ 1 h (none with published k_off found; docs/04 §3.3).
* The phase-2 antibody for immune-complex transfer (Stage 1C).
* Non-porosity of the 38–52 µm streptavidin particles for the backup; streptavidin–biotin stability at pH 2.
* Lead times for the IDEX valves, the syringe pump, machined parts and the custom IDA cell.
* CLSI EP17 replicate numbers were read only from secondary sources (docs/07 §7).
