# 04 — Independent audit of the LOD simulation (Task 3 model)

Status: 2026-11-11. Auditor: independent of the model author. Scope: `src/elisa_sim/`, `tests/`,
`scripts/run_baseline.py`, `params/model_assumptions.yaml`, `results/`, against docs/00–03 and primary sources.
docs/01–03, `params/chemistry.yaml` and `params/hardware.yaml` were not edited. Every correction to a value in those
two files is an entry in the `overrides` section of `params/model_assumptions.yaml` (section 5 lists them).

## 1. Verdict

**The headline does not survive as stated.** The claim was: "none of 83 architectures reaches 1 pg/mL; best is
17 pg/mL nominal, Monte Carlo median 80 [5.6–4200] pg/mL, P(LOD ≤ 1) = 0.4 %". Three things drove most of that
pessimism. Two of them are not supported by the sources the model cites:

1. **The NSB rate for an IgG–enzyme conjugate was about 25× too high.** The NSB rate constant was derived from
   15 pM streptavidin-β-galactosidase (SβG) on Simoa beads. It was then applied unchanged (factor 1, range 0.3–3)
   to a 1 nM IgG–ALP conjugate. That contradicts the source experiment itself. The same beads were also exposed
   to about 1 nM biotinylated detection IgG for 45 min, and at the model's rate that IgG alone would light about
   19 % of the beads, against about 1 % observed for the whole blank. It also contradicts the independent
   plate-ELISA blank, which was the model's own strict xfail. Anchoring the IgG-conjugate NSB to both published
   blanks lowers every LOD by about 25×. Section 3.1 has the derivation.
2. **The Monte Carlo sampled capture antibodies the design rejects.** It drew capture-antibody off-rates up to
   8.3×10⁻³ s⁻¹ (t½ 1.4 min). docs/01 §f rejects any capture reagent with t½ < 1 h. This widened the upper tail
   and lowered P(LOD ≤ 1). It is now a separate scenario.
3. **The installed plumbing was not modelled.** The user's system uses a 100 µL loop with full-loop injection, not
   a 250 µL loop with PLNO. Taken alone, this lowers LODs by 1.1–1.4× and shortens every cycle by 4.5 min.

After these and four smaller code fixes, the audited baseline is:

* **Best architecture:** the one-step magnetic-bead format (beads and conjugate pre-dispensed in the vial, flow
  IDA, ALP/HQDP). Nominal LOD 0.56 pg/mL; Monte Carlo median 2.3 pg/mL [5–95 %: 0.39–35]; P(LOD ≤ 1) = 0.25.
  Instrument cycle 21.5 min, 51.5 min to result.
* **Other architectures:**
  * Sequential bead formats: 2.6–4 pg/mL nominal, median 12–30, P ≤ 2 %.
  * Chip bead bed: 8.7 pg/mL nominal.
  * Packed-bed Scheme B: 19 pg/mL nominal (pre-audit 620–870).

So **1 pg/mL is plausible but not assured for the one-step bead format, and unlikely for all other formats.** What
decides it is the conjugate NSB actually measured on the chosen surfaces. That quantity is now pinned by published
anchors only to within roughly ±4× (section 6).

Parts of the headline that **survive**:

* The blank is set by conjugate NSB and its run-to-run variability, not by electrochemical noise. This holds for
  every leading architecture. For sequential bead formats with a thin-layer cell, baseline drift now competes.
* The detection cell matters little.
* The ranking is unchanged: one-step beads, then sequential beads, then chip bead bed, then packed bed, then
  capillary, monolith and planar chip.

## 2. Installed configuration (docs/00, user statement 2026-11-11) and its effect alone

| Item | Model baseline before | Installed (now baseline) | How recorded |
|---|---|---|---|
| Sample loop | 250 µL (`hw.smfl.loop_volume_recommended`) | 100 µL | override, confidence high |
| Injection | PLNO 82 µL (f_del 0.82) | full loop, 100 µL injected, 2× overfill (≈ 200 µL drawn), f_del 1.0 (0.97–1.0) | new mode `FL_100`, `ma.delivery.delivered_fraction_full_loop_100` |
| BSM minimum flow | 10 µL/min | 1 µL/min (user; confirm at bench) | override `hw.bsm.flow_min`; model now rejects any pumped flow below it |
| External valve | one given 6-/10-port | none bought; type and number free | no numeric parameter. Scheme A ("one valve, reactor not isolable") is no longer forced by the hardware, and Schemes B/C are fully purchasable. |
| Pre-mixing in vial | open question | allowed only if automated (pre-filled vials or an added dispenser) | the one-step bead format must ship as pre-filled bead + conjugate vials |

Recomputed for the 100 µL loop:

* **Sample load and transfer time:** 3 loop volumes take 3.0 min instead of 7.5 min, so every cycle is 4.5 min
  shorter. The Scheme B reference goes from 38.0 to 33.5 min.
* **Sample transfer:** 0.93 for beads (was 0.86) and 0.996 for IgG (was 0.999).
* **Conjugate plug:** a 20 µL conjugate plug is smeared over about one loop volume. Its peak at the reactor rises
  from 0.12 to 0.31 of the vial concentration. Labelled fraction in the sequential formats: 1.2 % → 3.1 %.

Effect of the installed configuration alone (pre-audit NSB factor 1 and pre-audit capture-k_off range kept;
`scratchpad steps.py`, n = 1000, seed 20261111):

| Architecture | Nominal LOD, 250 µL PLNO → 100 µL FL (pg/mL) | MC median, 250 → 100 (pg/mL) | Cycle / to result (min) |
|---|---|---|---|
| B-mag1-IDA/alp_hqdp | 18.3 → 13.8 | 96 → 68 | 26.0/56.0 → 21.5/51.5 |
| B-mag-IDA/alp_hqdp | 80 → 61 | 536 → 396 | 35.0/65.0 → 30.5/60.5 |
| C-bed-IDA/alp_hqdp | 278 → 244 | 1420 → 1190 | 38.0 → 33.5 |
| B-bed-TL/alp_hqdp | 622 → 546 | 2090 → 1730 | 38.0 → 33.5 |

Step 0 of this table includes the bead-share fix of section 3.4, which is why it reads 18.3 and not the original
17.4. The installed configuration alone **does not change the headline**. It is worth a factor of 1.1–1.4, and it
brings the sequential-bead format within the 60 min limit (60.5 min, marginal).

**Open point on sample consumption:** full loop with 2× overfill *draws* about 200 µL. If the brief's ≤ 100 µL
limit applies to the volume drawn, the 100 µL loop allows at most PLNO 75 µL (90 µL drawn). Variants `*/PLNO75`
give that case:
* one-step beads: 0.57 pg/mL nominal, median 2.3, P = 0.24;
* sequential beads: 3.5 pg/mL nominal.

The difference is small for beads, because they capture in the vial before injection.

## 3. Findings, ranked by effect on the predicted LOD

Categories: **(i)** code/equation error; **(ii)** parameter wrong or mis-transcribed or mis-derived; **(iii)**
defensible modelling choice that drives the result; **(iv)** untuned design setting.

### 3.1 (ii) NSB rate of an IgG–enzyme conjugate taken from SβG data — ×25 on every LOD

Evidence:

* **How the rate was derived.** `chem.nsb.nsb_effective_rate_constant` = 4×10⁻¹¹ m/s ("derived: Rissin2010")
  attributes the whole Simoa blank to SβG exposure: 15 pM × 30 min on 2×10⁵ 2.7 µm beads. The validation closure
  check `validation.simoa_blank` reproduces this: N_nsb ≈ 3000, i.e. 1.5 % of beads active.
* **How it was applied.** `model.py` applies it to a 1 nM IgG–ALP conjugate with
  `ma.nsb.label_factor_igg_enzyme_conjugate` = 1.0 (0.3–3, UNVERIFIED).
* **What the sources say (full texts re-read in this audit).**
  * Rissin2010 (PMC2919230): detection antibody "typically around 1 nM for 45 min", SβG 1–50 pM for 30 min, and
    "a typical background signal of 1% active beads".
  * Chang2012 (PMC3327511): "only 13% of the complexes are labeled with an enzyme" at 15 pM SβG for 30 min; a
    "noise floor of about 100 active beads in … 25,000" (≈ 0.3–0.4 %); and "backgrounds were dominated by the
    interactions between the labeling reagents and the immobilized capture antibodies". In other words, both
    reagents contribute.
* **Reproducing calculation** (`validation.simoa_detection_antibody_consistency`; test
  `test_simoa_blank_including_detection_antibody_nsb_within_3x`):
  * The dAb exposure is 1 nM × 2700 s, which is 67× the SβG exposure.
  * At factor 1, the non-specifically bound dAb, labelled at 13 %, would make 19.4 % of beads active, plus 1.5 %
    from SβG. That is 21× the observed 1 % and 70× Chang's 0.3 %.
  * Even if *all* of the observed blank came from the dAb, the IgG factor must be ≤ 0.052 (1 % active) or ≤ 0.016
    (0.3 %).
* **Independent anchor.** Rissin2010 states that the best commercial TNF-α ELISA "has an NSB level equivalent to
  85 fM". This is a background equivalent, not an LOD; that ELISA's LOD is quoted separately as 21 fM.
  * At factor 1 the model over-predicted this blank by 9× (1 nM label) to 35× (10 nM). That was the strict xfail.
  * The k_nsb that reproduces 85 fM is 1.2×10⁻¹² m/s (10 nM label) to 4.4×10⁻¹² m/s (1 nM), i.e. factor
    0.029–0.11.
* **The two anchors agree**, and they come from different formats (beads with digital readout; a plate with
  optical readout). Neither depends on the 1 pg/mL target.

Change: `ma.nsb.label_factor_igg_enzyme_conjugate` = **0.04 (0.01–0.15)**, giving k_eff = 1.6×10⁻¹² m/s
(0.4–6×10⁻¹² m/s). The SβG rate itself is kept, because it remains consistent with its own source (closure ratio
1.6). The two former strict xfails are now passing tests:
* plate blank: ratio 0.37 at 1 nM label and 1.39 at 10 nM;
* Simoa including the dAb: ratio 2.3.

The pre-audit assumption is kept as the scenario "SβG-equivalent NSB".

Effect: B-mag1-IDA/alp_hqdp goes from 13.8 to 0.56 pg/mL nominal (installed plumbing); B-bed-TL from 546 to 19.

Remaining weakness (iii): the 0.01–0.15 band still spans about 4× either way. Moreover, both anchors are for
*blocked* reference surfaces. The flow-path surfaces carry unverified surface factors:
* PEEK tubing ×3 (1–30);
* packed bed ×3 (1–30);
* chip ×10 (1–100).

The **0.1 m of PEEK sealed with the bead trap is the largest NSB area in every bead architecture.** It is about 20×
the bead area. One-at-a-time, the tubing factor at its high bound raises the one-step LOD by 0.59 decades. Section 8
gives the bench measurement that closes this.

### 3.2 (iii → corrected) Monte Carlo sampled capture reagents that the design rejects — MC median ×1.3–1.5, P(LOD ≤ 1) +6 points

* `chem.antibodies.koff_capture` had its high bound at 8.3×10⁻³ s⁻¹. That is Kamat2020's fast commercial
  anti-Fc mAb, t½ 1.4–3.3 min.
* docs/01 §f makes t½ ≥ 1 h (k_off ≤ 1.9×10⁻⁴ s⁻¹) an acceptance criterion for the capture reagent. Sampling
  rejected reagents mixed a screening failure into "parameter uncertainty". Before the audit this was the largest
  one-at-a-time sensitivity: ×2000 on the LOD at the bound.
* The override keeps value 1×10⁻⁴ s⁻¹ and low bound 3×10⁻⁶ s⁻¹ (Chang2012), and sets the high bound to
  1.9×10⁻⁴ s⁻¹. The nominal LOD is unchanged.
* Scenario "unscreened capture reagent" gives, for the one-step format, a median of 3.1 instead of 2.3 pg/mL and
  P = 0.19 instead of 0.25. The test `test_capture_koff_sampled_only_within_reagent_acceptance` checks the new
  bound.

### 3.3 (iii, not changed) The detection antibody is now the largest single sensitivity — up to ×90 at the bound

* `chem.antibodies.koff_detection` = 8.6×10⁻⁴ s⁻¹ (t½ 13 min). This is Chang2012's PSA detection mAb, with
  K_D 2.2 nM. It is sampled up to 8.3×10⁻³ s⁻¹.
* One-at-a-time on the leader, the LOD changes by −0.39/+1.96 decades.
* In the sequential formats, the conjugate reaches the reactor at about 0.3 nM, i.e. below K_D. Labelling
  therefore equilibrates at about 10 % within about 17 min, while linear NSB keeps growing. This is why a longer
  conjugate incubation makes the model's LOD *worse* (section 3.6).
* docs/01 gives no k_off criterion for the detection reagent, so the auditor did not impose one.
* Scenario "detection reagent also screened" (mode 1×10⁻⁴, high 1.9×10⁻⁴ s⁻¹):
  * one-step: 0.25 pg/mL nominal, median 1.3 [0.31–11], P = 0.39;
  * B-mag-IDA: median 10 pg/mL;
  * B-bed-TL: median 34 pg/mL.
* **Detection-antibody affinity is the second reagent-selection lever** and should get its own acceptance
  criterion.
* No anti-human-IgG k_on/k_off could be verified. Kamat2021 (doi:10.1016/j.ab.2021.114455) reports
  "high affinity" mouse anti-human-Fc mAbs and 300 capture–regeneration cycles, but the abstract gives no rate
  constants. **UNVERIFIED.**

### 3.4 (i) Code errors — small effect on the leaders, fixed

1. **One-step bead share of NSB** (`model.py`, `N_nsb_beads_part`).
   * The bead part was computed with the in-flow conjugate exposure `exposure1` (C × peak × 5 min), not the
     in-vial exposure `exposure_vial` (C × 30 min). That is 55× too small, so the bead-dose CV term and the
     carry-over "wall share" were wrong.
   * Effect: one-step LOD +5 % (13.2 → 13.8 pg/mL at pre-audit NSB).
   * Test: `test_one_step_bead_share_uses_in_vial_exposure`. With no tubing NSB, the bead share must be 1; it was
     about 0.02.
2. **Label NSB factor applied twice** in the bead part for direct chemistries (`label_factor × eff_exposure`, where
   `eff_exposure` already contains it).
   * Invisible at factor 1. It would have mis-weighted the bead-dose CV after finding 3.1.
   * Test: `test_bead_share_of_nsb_not_double_scaled_by_label_factor`.
3. **Two-step chemistries: dAb NSB at the SβG rate.** The non-specifically bound biotinylated dAb (an IgG) was given
   the unscaled SβG/SA-polyHRP rate.
   * It now takes the IgG factor. This affects only the SβG and SA-polyHRP rows, which remain far from the target.
   * Test: `test_two_step_dab_nsb_uses_igg_factor`.
4. **Plumbing consistency was not checked.**
   * Any injection mode could be combined with any loop. For example, `PLNO_100` ran on the 250 µL loop: it used
     the 100 µL-loop delivered fraction but the 250 µL loop for transfer and timing.
   * Flows below the BSM minimum were also accepted.
   * Now `_check_loop_and_flows` raises in both cases. Tests: `test_injection_mode_must_match_fitted_loop` and
     `test_flows_below_bsm_minimum_rejected`.
5. **Scenario helper** (in the new `run_baseline.py` code). Copying a parameter set with new bounds dropped the
   pinned values, so they were silently re-sampled. Found and fixed during the audit, before any results were
   written.

### 3.5 (ii, interpretation) Enzyme turnover: the published ALP LODs are lower bounds on k_cat — no change

* The model's comparison treated "the k_cat at which the detector-LOD amount of product is made by the
  published-LOD amount of enzyme" as an *estimate*:
  * DellaCiana1996 (doi:10.1016/0022-1759(96)00044-0): 1.2 fM ALP, 10 min, HQ LOD 0.12 nM → 180 s⁻¹;
  * Thompson1991 (doi:10.1016/0003-2697(91)90190-5): 0.05 µg/L ALP, 15 min, pAP 7 nM → 23 s⁻¹.
* An enzyme LOD is limited by the product-detector LOD *or by anything larger* (free product in the substrate,
  hydrolysis, injection noise). The implied value is therefore a **lower bound** on the effective k_cat × S/(K_m + S).
* Thompson1991 also does not state the ALP source or specific activity. Its mass unit (µg/L of an unspecified
  preparation) carries an unknown factor.
* Both bounds lie below the nominal 1000 s⁻¹ and inside the 100–6000 s⁻¹ range. The strict xfails were replaced by
  `test_published_alp_lods_are_lower_bounds_on_kcat_consistent_with_model`.
* A direct value for ALP–antibody conjugate turnover at RT in non-DEA buffer was **not found (UNVERIFIED)**.
* Because the blank is NSB-borne enzyme, k_cat cancels to first order. One-at-a-time on the leader: +0.39 decades
  at 100 s⁻¹, −0.01 at 6000 s⁻¹.

### 3.6 (iii) NSB modelled as linear and irreversible in conjugate exposure — decides which design levers work

* `N_nsb = k·A·∫C dt`, with no saturation and no removal by washing.
* Sources: Rissin2010 ("decreased label concentration greatly reduces NSB") and Chang2012 ("higher concentrations …
  higher non-specific binding") support the direction only. Linearity in time and irreversibility are
  **UNVERIFIED**.
* Consequence: the specific signal and the NSB both scale with exposure while labelling is far from saturation. So
  the analyte-equivalent blank B does not depend on conjugate plug volume, concentration or incubation time, and
  wash stringency has no effect at all.
* The author's point that "1.2 % labelling cancels in B" is therefore correct within the model. **The pessimism did
  not come from the untuned plug.** The design study in section 3.7 confirms this: a 100 µL conjugate plug or 10 nM
  conjugate does not help, and with a weak dAb it hurts.
* If real NSB is partly reversible or saturable, as is typical for blocked surfaces, a stringent wash and a short,
  concentrated label pulse would gain. The model cannot show this. This is the first bench experiment in section 8.

### 3.7 (iv) Design settings

Nominal LOD in pg/mL, audited parameters, one change at a time. This is design exploration, not the baseline.

| Change | B-mag1-IDA/alp_hqdp | B-mag-IDA/alp_hqdp | C-bed-IDA/alp_hqdp | B-bed-TL/alp_hqdp |
|---|---|---|---|---|
| audited baseline | 0.56 | 2.6 | 8.7 | 19 |
| connection tubing sealed with reactor 0.1 → 0.02 m | 0.46 | **1.5** | 8.7 | 19 |
| 1×10⁶ beads instead of 5×10⁵ | 0.55 | 1.6 | — | — |
| in-vial incubation 30 → 45 min | 0.52 (66.5 min to result) | 2.0 (> 60 min) | — | — |
| conjugate 100 µL (full loop) instead of 20 µL | — | 2.5 | 9.1 | 20 |
| conjugate 100 µL at 10 nM | 1.9 | 3.8 | 16 | 35 |
| conjugate incubation 5 → 15 min | — | 3.4 | 12 | 27 |
| one-step conjugate 1 → 0.5 nM / 3 nM | 0.53 / 0.81 | — | — | — |
| trap 2 → 1 µL, 0.25 mm ID | 0.56 | 2.6 | — | — |

Reading the table:

* The conjugate plug volume and concentration were not a hidden handicap.
* The real untuned setting is the **length of tubing isolated with the bead trap** (`ma.geometry.reactor_connection_length`
  = 0.1 m). This was inherited from a 10-port valve layout. Now that no valve has been bought, the layout is free:
  integrate the trap at the valve port.
* For sequential formats, a higher-affinity detection antibody is the other lever (section 3.3).

### 3.8 (iii, supported) Run-to-run NSB CV = 10 %

`chem.nsb.blank_CV_analog_electrochemical` = 0.10 (0.03–0.2) dominates the blank SD. Two independent published
LOD/background ratios support it:

* Rissin2010's commercial ELISA: LOD 21 fM against background 85 fM, giving 3·CV ≈ 0.25, i.e. CV ≈ 8 %.
* Simoa PSA: 0.4 fM against about 1.2 fM, giving CV ≈ 11 %.

Not changed. Sensitivity on the leader: −0.30/+0.26 decades over its range.

### 3.9 Correlation constants and detector questions — no effect on the leaders

* **Thin-layer conversion.** The model computes 0.36 at 50 µL/min with the 51 µm gasket, from the exact slit
  solution (Lévêque limit 1.468 ζ^{2/3}, ζ = 0.17). hardware.yaml lists 0.05. Re-running the same expression at
  1 mL/min gives 0.06. **The listed 0.05 is an HPLC-flow figure, and the model's 0.36 is right for the flow used.**
  The hardware value is not read by the code, so no override is needed.
* **Wilson–Geankoplis** (Sh = (1.09/ε) Re^{1/3} Sc^{1/3}, 0.0016 < Re < 55). The coefficient and validity range
  could not be checked against the 1966 paper in this session (**UNVERIFIED**). Packed-bed capture is
  reaction-limited at these flows, so one-at-a-time over 0.9–1.3 changes log LOD by < 0.001.
* **Wall-jet coefficient** (0.898 Yamada–Matsuda / 1.597 Albery–Brett). The scaling D^{2/3} ν^{−5/12} a^{−1/2}
  R^{3/4} Q^{3/4} is standard. The audit could not read the coefficient from a primary text: Compton et al.
  J Appl Electrochem 1993;23:98 was read but does not restate it. **UNVERIFIED.** No leading architecture uses a
  wall-jet cell.
* **Aoki IDA constants** (0.637, 2.55, 0.19). The equation form is cited in the IDA literature, but the constants
  could not be confirmed (Aoki et al. 1988, doi:10.1016/0022-0728(88)87003-7, not accessible).
  **UNVERIFIED.** They are used only by Scheme C stopped-IDA rows, where NSB limits.
* **Chemical redox-cycling gain** (`chem.substrates.pAP.chemical_redox_cycling_gain`, defined as "fold LOD
  improvement" but used as a current gain). This is a semantic mismatch. It only matters where electrochemical
  noise limits, which is nowhere among the leaders. Left as is and documented.
* **Checked and found consistent:**
  * unit handling, including the strict unit checker;
  * the LOD statistic (net signal = 3 SD of the blank, equivalent to mean blank + 3 SD through the curve);
  * white-noise charge variance i_n²·T/(2B) × 2 for baseline subtraction;
  * drift residual;
  * enzyme ODE conservation;
  * the one-step sandwich ODE;
  * loop-transfer re-implementation against the Task 2 table (max |Δ| 0.006).

## 4. Before/after baseline (leading architectures)

Monte Carlo n = 1000, seed 20261111. "Before" is `results/` as delivered by the model author (250 µL PLNO,
pre-audit parameters). "After" is the audited baseline (`results/baseline_table.md`, `results/scenarios.md`).

| Architecture | Before: nominal / median [5–95 %] / P(≤1) | After: nominal / median [5–95 %] / P(≤1) | After, cycle / to result (min) | Limiting term (after) |
|---|---|---|---|---|
| B-mag1-IDA/alp_hqdp | 17 / 80 [5.6–4200] / 0.004 | **0.56 / 2.3 [0.39–35] / 0.25** | 21.5 / 51.5 | NSB variability |
| B-mag1-IDA/alp_hqdp/PLNO75 (≤ 100 µL drawn) | — | 0.57 / 2.3 [0.47–39] / 0.24 | 21.5 / 51.5 | NSB variability |
| B-mag1-IDA/hrp_tmb | 24 / 130 [9.2–5900] / 0.000 | 0.81 / 4.3 [0.66–70] / 0.12 | 21.5 / 51.5 | electrode sensitivity |
| B-mag1-IDA/alp_papp | 24 / 130 [11–5900] / 0.000 | 1.0 / 6.8 [0.88–130] / 0.08 | 21.5 / 51.5 | electrode sensitivity |
| B-mag-IDA/alp_hqdp | 80 / 520 [38–28000] / 0.000 | 2.6 / 12 [1.5–170] / 0.02 | 30.5 / 60.5 | NSB variability |
| B-mag-TL/alp_hqdp | 80 / 510 [45–36000] / 0.000 | 3.9 / 18 [2.3–170] / 0.01 | 30.5 / 60.5 | baseline drift |
| C-bed-IDA/alp_hqdp | 280 / 1300 [100–24000] / 0.000 | 8.7 / 34 [3.4–430] / 0.004 | 33.5 / 33.5 | NSB variability |
| B-bed-TL/alp_hqdp | 620 / 1900 [180–41000] / 0.000 | 19 / 44 [5.6–580] / 0.000 | 33.5 / 33.5 | NSB variability |

The order of the leaders is unchanged. The one-step bead format is still first, by about 5× over sequential beads.
The sequential-bead formats at 60.5 min to result exceed the 60 min limit by 0.5 min; shortening the in-vial step
fixes this at a small cost in LOD.

## 5. Changes made

**Parameters** (`params/model_assumptions.yaml`):

* Overrides:
  * `hw.smfl.loop_volume_recommended` 250 → 100 µL (installed);
  * `hw.bsm.flow_min` 10 → 1 µL/min (user statement, confirm at bench);
  * `chem.antibodies.koff_capture` high bound 8.3×10⁻³ → 1.9×10⁻⁴ s⁻¹ (docs/01 §f acceptance criterion; value and
    low bound unchanged).
* Changed entry: `ma.nsb.label_factor_igg_enzyme_conjugate` 1.0 (0.3–3, UNVERIFIED) → 0.04 (0.01–0.15), derived
  from Rissin2010 + Chang2012 and the Rissin2010 plate anchor.
* New entries:
  * `ma.delivery.delivered_fraction_full_loop_100` (1.0, 0.97–1.0);
  * `ma.validation.simoa_sbg_labelling_efficiency` (0.13, Chang2012);
  * `ma.validation.simoa_blank_active_bead_fraction` (0.01, 0.003–0.015; Rissin2010 / Chang2012).

**Code:**

* `architectures.py`: added the injection mode `FL_100`, which is now the default. Every mode carries its loop
  volume. The variants `*/PLPA97` (250 µL loop) are replaced by `*/PLNO75`, the drawn-volume-limited case, which
  is added for B-bed-TL, B-mag-IDA and B-mag1-IDA. The registry now has 84 architectures.
* `model.py`:
  * loop/flow consistency check;
  * one-step bead-share fix;
  * double-factor fix;
  * two-step dAb NSB factor;
  * new diagnostic `bead_share_of_nsb`.
* `validation.py`:
  * kcat comparisons report `implied_kcat_lower_bound`;
  * the plate-blank comparison uses the IgG-conjugate factor;
  * new `simoa_detection_antibody_consistency`.
* `scripts/run_baseline.py`: the "plate-calibrated NSB" column is replaced by "SβG-equivalent NSB (pre-audit)". The
  script also writes a new `results/scenarios.md` (audited, SβG-equivalent NSB, and unscreened capture reagent for
  the leading architectures).
* `results/`: all files regenerated with `python scripts/run_baseline.py --n 1000` (129 s, log in
  `results/baseline_log.txt`).

**Tests** (each fails on the pre-audit code or parameters):

* new: `test_installed_configuration_is_the_baseline`, `test_injection_mode_must_match_fitted_loop`,
  `test_flows_below_bsm_minimum_rejected`, `test_conjugate_plug_dilution_recomputed_for_100uL_loop`,
  `test_one_step_bead_share_uses_in_vial_exposure`, `test_bead_share_of_nsb_not_double_scaled_by_label_factor`,
  `test_two_step_dab_nsb_uses_igg_factor`, `test_capture_koff_sampled_only_within_reagent_acceptance`,
  `test_simoa_blank_including_detection_antibody_nsb_within_3x` (it also asserts that the pre-audit factor gives
  > 10×), `test_published_alp_lods_are_lower_bounds_on_kcat_consistent_with_model`;
* former strict xfail, now passing: `test_conventional_elisa_blank_within_3x[1 nM, 10 nM]`;
* updated: `test_scheme_b_baseline_cycle_time_matches_task2_timeline`, which checks 38.0 min for the Task 2
  250 µL configuration and 33.5 min for the installed one.

The three strict xfails are gone. `python -m pytest -q` gives **63 passed, 0 xfailed** (section 9).

## 6. Scenarios that remain open (kept side by side, not resolved by choosing one)

Values are for the leader, B-mag1-IDA/alp_hqdp, from `results/scenarios.md` and the audit runs.

| Scenario | Nominal | MC median [5–95 %] | P(LOD ≤ 1) |
|---|---|---|---|
| Audited baseline (IgG-conjugate NSB factor 0.04; capture t½ ≥ 1 h) | 0.56 | 2.3 [0.39–35] | 0.25 |
| SβG-equivalent NSB (pre-audit factor 1; contradicted by both anchors, kept as worst case) | 14 | 51 [5.8–770] | 0.001 |
| Unscreened capture reagent (k_off to 8.3×10⁻³ s⁻¹) | 0.56 | 3.1 [0.46–72] | 0.19 |
| Detection reagent also screened to t½ ≥ 1 h (mode 1×10⁻⁴ s⁻¹) | 0.25 | 1.3 [0.31–11] | 0.39 |
| Sample drawn ≤ 100 µL (PLNO 75 µL instead of full loop) | 0.57 | 2.3 [0.47–39] | 0.24 |

Two further questions are unresolved by any source:

* **NSB linear vs saturable/reversible.** This is a model-structure question; section 3.6 explains why it decides
  whether wash and label-pulse design can help.
* **Surface factors for PEEK, packed-bed and chip surfaces** (all UNVERIFIED, 1–30× or 1–100×).

## 7. How far the results can be trusted

* **Ranking: fairly robust.** It follows from analyte-equivalent blank ∝ (NSB area × exposure)/(captured, labelled
  analyte), which is geometric. Neither audit change reordered the leaders. Renewed beads with in-vial capture and
  labelling are favoured by more than 5× over every flow-through capture format.
* **Absolute LODs: uncertain to about ±1 decade.** They scale almost linearly with the conjugate NSB rate on the
  actual surfaces. The two published anchors fix that rate only on blocked reference surfaces, and only to about
  ±4×. Surface factors and detection-antibody affinity add about another half-decade each.
  * The Monte Carlo 5–95 % intervals are scenario ranges built from plausible bounds with independent sampling, not
    confidence intervals.
  * The nominal sits near the 20th percentile because most bounds are asymmetric (log-triangular with long upper
    tails).
* **Bottom line:** "≤ 1 pg/mL is achievable" is about a coin flip for the one-step bead format. It is more likely
  if a high-affinity detection reagent is chosen and the trap is integrated into the valve. It is not credible for
  the packed-bed or chip formats unless bench NSB is more than 10× below the plate anchor.

## 8. What would settle it (bench, first)

1. **Blank signal vs conjugate exposure** (concentration × time, and a wash-stringency series) on blocked beads,
   PEEK tubing and the trap. This measures the IgG–ALP NSB rate, its linearity and its reversibility directly, and
   replaces the 0.01–0.15 factor and the surface factors.
2. **k_off of candidate capture and detection anti-human-IgG reagents** (BLI/SPR), with t½ ≥ 1 h for both.
3. Free hydroquinone in the HQDP lot (`free_product_impurity`, 10⁻⁷–10⁻³, UNVERIFIED). This is the third-largest
   sensitivity for the leader.

## 9. Test results as run

```
$ python -m pytest -q
...............................................................          [100%]
63 passed
```

(Before the audit: 51 passed, 3 xfailed.)

## 10. Sources checked in this audit

* Rissin DM et al. Nat Biotechnol 2010;28:595 (PMC2919230), full text: background 1 % active beads; dAb about
  1 nM for 45 min; SβG 1–50 pM for 30 min; commercial ELISA NSB level 85 fM and LOD 21 fM; LOD = background + 3 SD.
* Chang L et al. J Immunol Methods 2012;378:102 (PMC3327511), full text: 13 % SβG labelling at 15 pM for 30 min;
  background dominated by labelling reagents interacting with capture antibodies; noise floor about 100 active
  beads in 25 000; PSA capture and detection rate constants (2.67×10⁵ M⁻¹s⁻¹ / 3.13×10⁻⁶ s⁻¹;
  3.92×10⁵ / 8.57×10⁻⁴ s⁻¹); effective K_D < 10⁻¹¹ M.
* Thompson RQ et al. Anal Biochem 1991;192:90 (doi:10.1016/0003-2697(91)90190-5) and Della Ciana L et al.
  J Immunol Methods 1996;193:51 (doi:10.1016/0022-1759(96)00044-0): PubMed abstracts.
* Kamat V et al. Anal Biochem 2021;640:114455 (doi:10.1016/j.ab.2021.114455): PubMed abstract (no rate constants).
* Compton RG et al. J Appl Electrochem 1993;23:98: read; does not restate the wall-jet coefficient.

**UNVERIFIED after this audit:**
* Wilson–Geankoplis coefficient and range;
* wall-jet coefficient;
* Aoki IDA constants;
* ALP–conjugate k_cat under assay conditions (only lower bounds);
* anti-human-IgG k_on/k_off;
* linearity and reversibility of NSB;
* all surface factors;
* HQDP free-product fraction.
