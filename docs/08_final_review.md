# 08 — Final independent review of the in silico phase

Status: 2026-11-11. Reviewer independent of all earlier tasks. Scope: docs/00–07, `params/`, `src/elisa_sim/`,
`tests/`, `scripts/`, `results/`, `automation/`. docs/00–05 were not edited (CLAUDE.md); every issue in them is a
recommendation. Small, clear errors in docs/06 and `automation/` were fixed and are listed in §5.

---

## 1. Verdict

**Fit to start bench Stage 0 now. Fit to start Stage 1 once the four blocking items in §2 are resolved.** Two of
them are fixed in this review. The other two are edits to the G1 decision rule and one added experimental arm,
about a day of desk work. None of them needs a purchase.

Why the package is close to ready:
* The decision numbers can be reproduced exactly. `scripts/final_designs.py`, `kill_thresholds.py`,
  `recovery_options.py`, `inline_chamber.py` and `incubation_queue.py` were re-run on a clean snapshot of HEAD.
  The outputs are byte-identical to the committed `results/design/*.md` and `final_designs.csv`.
* The Monte Carlo fix (commit 6cbf85e) changes no reported number. §3.2 gives the check.
* Stage 1 is cheap and buys no custom hardware. It also measures the two quantities that dominate every design:
  conjugate NSB on beads (U1) and free hydroquinone (U3).

What has to change first:
1. The G1 rule gives two contradictory instructions for the same quantity. The kill threshold's quoted
   probability is also not the one the bench measurement will imply (B3).
2. The primary design stores beads and conjugate together in one reservoir for hours. Nothing in the model or the
   bench plan measures what that does to the blank (B4).
3. Stage 1 data would have been corrupted by phosphate in the assay buffer (B1, fixed).
4. A gate would have passed falsely because of a ratio formed on raw signals (B2, fixed).

Beyond Stage 1, the design rests on more momentum than evidence in two places (§2, S9 and S4):
* the interdigitated cell with a second potentiostat, whose modelled benefit is ≤ 0.04 in P;
* the one-step mode, which in the model is no better than the sequential mode until the detection reagent's
  t½ exceeds about 30 min, and which carries the reservoir risk.

## 2. Findings ranked by consequence

Each finding gives its evidence and a specific change. "Fixed" means changed in this review (§5).

### Blocking (resolve before Stage 1 data are taken)

**B1. Phosphate in the Stage-1 assay buffer would inhibit the enzyme being counted. Fixed in docs/06.**
* Evidence:
  * docs/06 §4.0 defined the assay buffer (AB) as "PBS pH 7.4 (or 50 mM Tris…)".
  * `params/chemistry.yaml` `chem.enzymes.alp.phosphate_inhibition_Ki` = 2 µM, with the note "NO PBS in lines
    that reach the enzyme step".
  * docs/02 §1.2 also offers "PBS or Tris" for the A1 line.
* Size of the effect: a few µL of PBS left on the beads in 50 µL of substrate gives about 0.5 mM phosphate. With
  K_m = 0.1 mM, S = 0.3 mM and K_i = 2 µM, v/V falls from 0.75 to about 0.01.
* Consequence: the U1 label factor (E1.3), the conjugate standard series and E1.8 would all be biased by a
  variable amount.
* Change made: AB is now Tris-buffered saline only, with the reason stated (docs/06 §4.0).
* Still recommended:
  * A1 in docs/05 §4.1 and docs/02 §1.2 should be "Tris/TBS + Tween, no phosphate".
  * The M-280 stock (PBS) must be washed 3× in TBS before use; docs/06 §4.0 already washes 3×.

**B2. The detection-on-capture ratio (E1.4) was computed on raw signals and would pass falsely. Fixed.**
* Evidence:
  * `automation/elisa_auto/analyze.py` `detection_on_capture` formed mean(capture)/mean(non-immune) on raw
    signals.
  * The template had no background rows.
  * At the design point (5×10⁵ beads, 0.3 nM) docs/06 E1.4 itself expects about 0.8 nM HQ from the beads on top of
    about 3 nM free HQ.
  * Consequence: a true conjugate-borne excess of 1.5× reads as (3 + 1.2)/(3 + 0.8) = 1.1, which is a PASS.
* Change made:
  * Rows with `bead_type` = `background` are averaged and subtracted. A warning is printed if there are none, and
    the item is reported as unresolvable if a corrected arm is ≤ 0.
  * Background rows were added to `templates/detection_on_capture.csv`.
  * A regression test was added (`test_detection_on_capture_subtracts_background`).
* Also recommended (should fix): run E1.4 by default at 5×10⁶ beads and 1 nM. The §12.3 power calculation
  assumes a 15 % CV, which a 0.8 nM signal on a 3 nM background with a 1 nM readout LOD cannot reach.

**B3. The G1 decision rule is internally inconsistent, and the quoted kill probability is not the one the bench
value will imply.** Reproduce with the snippet in §3.3.
* Coupling. The model's conjugate NSB rate is `ma.nsb.label_factor_igg_enzyme_conjugate` ×
  `chem.nsb.nsb_effective_rate_constant` (sampled 8×10⁻¹² to 4×10⁻¹⁰ m/s) × `ma.nsb.surface_factor_magnetic_beads`
  (1–3). E1.3 measures the product directly (docs/06 §9.3; `model_feedback.COUPLED`).
* `kill_thresholds.py` pins only the label factor, so the reported P at the threshold is still spread over the
  other two factors. With all three pinned, which is how `model_feedback` will evaluate a real bench value, the
  primary (P-chamb, n = 1000) gives:

  | label factor | as reported in docs/05/06: median / P | bench-consistent (coupled factors pinned): median / P |
  |---|---|---|
  | 0.01 | 1.13 / 0.44 | 0.94 / 0.54 |
  | 0.04 (go) | 2.13 / 0.25 | 1.29 / 0.39 |
  | 0.08 | 3.59 / 0.15 | 1.96 / 0.25 |
  | 0.15 (kill) | 5.92 / 0.06 | 3.17 / 0.11 |

  * The backup bed changes little: 0.15 → P 0.01 instead of 0.02.
  * The sequential chamber: 0.15 → P 0.05 instead of 0.04; 0.04 → P 0.39 instead of 0.24.
* The two G1 rows contradict each other. B (the tube blank-equivalent, E1.8) is proportional to the label factor:
  B ≈ 24 × factor, so B = 0.96 pg/mL at 0.04. In docs/06 §4.11:
  * the U1 row says "0.04–0.15: proceed and run Stage 1C in parallel";
  * the tube-B row says "1–4 pg/mL: proceed only if the model gives P ≥ 0.3".
  * With the coupled factors pinned, P ≥ 0.3 holds only up to a label factor of about 0.06 (B ≈ 1.5 pg/mL).
  * So a label factor of 0.1 with a consistent B of 2.4 pg/mL is "proceed" by one row and "stop" by the other.
* Change recommended:
  * Restate G1 in one place, on the bench-consistent model:
    * go if P-chamb or S-chamb P(success) ≥ 0.3 with all Stage-1 values entered;
    * L4 track (Stage 1C) if 0.1 ≤ P < 0.3;
    * stop hardware purchases if P < 0.1 for every admissible design including L4.
  * Keep the label-factor and B thresholds only as fast screens.
  * Re-run `kill_thresholds.py` with the coupled factors pinned and quote those numbers in docs/05 §5, docs/06 E1.3
    and docs/06 §4.11.
  * Fix the rule in writing before the U1 data exist (pre-registration).

**B4. The one-step primary keeps beads and conjugate together in one stirred reservoir for hours. That
pre-exposure is neither modelled nor measured.**
* Evidence:
  * docs/05 §4.1 plumbing: "8-port selection valve: bead/conjugate reservoir (stirred, 4-8 C)".
  * docs/05 §4.1 end-to-end automation: "reagent pack (bead/conjugate reservoir…)".
  * docs/07 §5.5: "Stirred, cooled bead/conjugate reservoir … dose CV ≤ 5 % over 8 h".
  * `automation/config/cycle_primary.yaml`: `from: reservoir`.
  * docs/06 §7.7: sequences run for > 24 h.
* Size of the problem:
  * The 20 µL dose must carry 0.3 nM final in 220 µL, so the reservoir holds about 3.3 nM conjugate with the beads.
  * After 8 h the conjugate exposure of the beads is about 3.3 nM × 480 min ≈ 1600 nM·min. The modelled in-cup
    exposure is about 0.3 nM × 36.6 min ≈ 11 nM·min, about 150× less.
  * The model's NSB is linear and irreversible in exposure (docs/04 §3.6), so taken at face value the blank would
    grow about 150× over a day. Cooling slows this, but by an unknown factor.
  * Any human IgG in the conjugate also forms complete sandwiches on the capture beads in the reservoir. Examples
    are human IgG leached from the affinity column used to purify an anti-human-IgG reagent (UNVERIFIED for these
    lots), or contamination.
  * E1.3 covers only 10–60 min at 22 °C. E2.2 tests dose CV with beads only.
  * The blank would also drift through the sequence. docs/06 §7.7 would catch that only at validation, at week 28.
* Change recommended. Pick one:
  * **(a)** Hold beads and conjugate in **separate** SIA reservoirs (one extra selection-valve port; the 8-port
    valve has spare ports) and dose both into the cup immediately before the sample. This is the minimal change.
  * **(b)** Make the sequential mode the default (see S4).
  * In either case, add a Stage-1 arm to E1.3: capture and non-immune beads held with 3.3 nM conjugate at 4 °C and
    22 °C for 0, 2, 8 and 24 h, then diluted 11× and processed as E1.3. It costs about one bench day and decides
    whether option (a) is required.
  * Update docs/07 §5.5, `cycle_primary.yaml` (two dispense actions) and `hardware_lab.example.yaml` (a port for
    each reservoir).

### Should fix before the bench

**S1. Earlier documents still state superseded conclusions without a warning.** Recommendation: a one-paragraph
status banner at the top of each, added by the orchestrator. CLAUDE.md forbids edits to docs/00–05.
* docs/03:
  * §10 point 1 says "No architecture reaches LOD ≤ 1 pg/mL … best 17 pg/mL nominal, P = 0.4 %".
  * §1 says "54 tests: 51 pass, 3 strict-xfail".
  * Both are pre-audit. docs/04 §1 overturns the headline: NSB rate about 25× too high.
* docs/02:
  * §2.4 table and §6/§7 recommend a "250 µL loop + 500 µL syringe; PLNO 82 µL" and an I-Class minimum flow of
    10 µL/min (§1.2).
  * §2.4(d) proposes pre-dispensed reagent vials.
  * §7.4 gives a timeline for the 250 µL loop.
  * All are superseded by docs/00 (installed 100 µL full loop, BSM to 1 µL/min, no reagent in vials).
* docs/00:
  * "Installed configuration" still says whether the 100 µL limit is injected or consumed volume "is to be
    confirmed with the user". The "Decisions" section below it settles that.
  * "Fixed equipment" lists "an extra externally triggerable switching valve" as if it were in hand, but the valve
    is not yet bought.
  * Only the user or orchestrator should touch docs/00.
* docs/05:
  * §1.1 and §7 still say "Fix needed in src". It is done (commit 6cbf85e, with a test).
  * §6 says "63 passed"; it is now 64.
* docs/04 §1 and `results/baseline_table.md` headline the in-vial one-step format (B-mag1-IDA), which user
  decision 1 makes inadmissible. docs/05 says so, docs/04 does not.

**S2. The trap-loading step does not say what the BSM does. If the BSM keeps flowing, the trap sees about
200 µL/min.**
* Evidence:
  * docs/05 §4.1 plumbing: the SIA line and the SM-FL outlet (V4 position B) join at a tee upstream of V2.
  * Step "33 → 39.6": SIA pushes 660 µL at 100 µL/min, and the BSM column is "–".
  * `cycle_primary.yaml` step `load_trap` has no `empower` entry and no V4 position.
  * Two positive-displacement pumps into one tee add their flows. The trap then runs at about 200 µL/min, double
    the ≤ 100 µL/min constraint in docs/05 §1.1. That constraint exists because trap efficiency 0.9 is assumed only
    at the baseline flow.
* Change recommended: state the BSM programme for 33–39.6 min explicitly, e.g. 1 µL/min A1 (user's minimum), and
  check the pressure. Alternatively give the SIA line its own V2 inlet. Add `empower:` and `V4:` to the YAML step.
  E2.1 should log the trap flow.

**S3. The step table's "cleaning injection through loop and trap" is a second SM-FL injection that the
automation and the Empower plan do not represent.**
* Evidence:
  * docs/05 §4.1 step 52.6–56.1.
  * `cycle_primary.yaml` (`clean` step) declares only one injection (`injects: sample`).
  * The sequencer faults on an unexpected Inject Start (`sequencer._poll_injects`).
* Change recommended. Either:
  * replace it with the SM-FL needle wash plus a BSM flush (no injection); or
  * make it an explicit second Empower line from a wash vial, declared as a second `injects` entry with its own
    line code.

**S4. The one-step vs sequential choice and the 1-h detection threshold are not where the model puts them.**
* Model, n = 1000, detection k_off pinned:

  | detection t½ | P-chamb median / P | S-chamb median / P |
  |---|---|---|
  | 13 min | 3.2 / 0.17 | 1.8 / 0.29 |
  | 30 min | 1.7 / 0.33 | 1.6 / 0.32 |
  | 60 min | 1.3 / 0.38 | 1.5 / 0.33 |
  | 120 min | 1.2 / 0.41 | 1.5 / 0.34 |

  * The modes cross at about 30 min.
  * Above that, one-step gains only 0.05–0.07 in P, while carrying the B4 reservoir risk.
* E1.6 asks for a "global 1:1 fit" on BLI/SPR. The reagents selected in docs/07 (goat F(ab′)₂ capture, goat F(ab′)₂
  ALP detection) are **polyclonal and bivalent**. A 1:1 k_off of a polyclonal is ill-defined: it is heterogeneous
  and avidity-dependent. E1.5, the on-bead dissociation with scavenger, measures the quantity that matters.
* Change recommended:
  * Make E1.5 the decisive U2 measurement for the mode. Use BLI for k_on screening and monoclonal candidates only.
  * Report heterogeneous fits for polyclonals.
  * Move the mode boundary to about 30 min, or state that between 30 and 60 min the choice is made on B4 and
    carry-over grounds, not on LOD.

**S5. Human-IgG contamination is underweighted relative to the source the documents themselves cite.**
* docs/05 §4.5 point 1 says "100 fg per sample (Parry1997)". That is 1 pg/mL in 100 µL, the whole LOD budget.
* The model samples `ma.nsb.blank_igg_contamination_equivalent` only up to 3 fM (0.45 pg/mL), with nominal 0.
* The Parry1997 abstract (PubMed 9126687) gives no amount. It reports human IgG in at least a third of tip-cone
  eluates in every one of 19 labs, so "100 fg" has no source.
* E1.9 cannot resolve 0.1 pg/mL. docs/06 §12.4 says so honestly, and the amplified-handling arm helps.
* Missing: contamination carried by the **reagents** themselves (conjugate, capture antibody, BSA lot), which
  reaches every sample, blanks included, and which B4 amplifies.
* Change recommended:
  * Remove "100 fg" or source it.
  * Widen the model bound to at least 1 pg/mL-equivalent as a scenario.
  * In E1.4 and the new B4 arm, compare capture beads with non-immune beads after long conjugate pre-incubation.
    A reagent-borne human IgG signal grows with pre-incubation time on capture beads only.

**S6. A carry-over limit of 10⁻³ after 1000 pg/mL allows 1 pg/mL in the next sample, which is the LOD itself. E1.10
cannot test its own criterion.**
* Evidence:
  * docs/05 §5 U7, docs/06 §7.6, `gates.yaml` `carryover: 1e-3`.
  * docs/06 §8.4 flags any blank-after-high above mean + 3 SD, i.e. about 1 pg/mL at SD 0.33. So a system that
    passes the carry-over gate can still trip the flag.
  * E1.10 measures "blank-after-100 / 100 pg/mL". 10⁻³ × 100 pg/mL = 0.1 pg/mL, below what the tube format
    resolves (S7).
* Change recommended:
  * Set the criterion at ≤ 1×10⁻⁴ for the analyte path, or make a cleaning cycle mandatory after any sample above
    100 pg/mL.
  * Run the E1.10 carry-over arm with 10 ng/mL, so that 10⁻⁴ gives 1 pg/mL.

**S7. Two Stage-1 readouts are below their own resolution at the design point.**
* E1.8 (tube B):
  * docs/06 says 1 pg/mL gives about 0.8–1.6 nM HQ over about 10 nM free HQ at 1 mM HQDP, with an E1.1 acceptance
    of LOD_HQ ≤ 1 nM.
  * The confirm level B ≤ ~1 pg/mL is therefore a sub-1-nM increment on a 10 nM background with a 10 % CV.
* E1.4: see B2.
* Change recommended:
  * Run E1.8 with 0.3 mM HQDP (3 nM background), a 20–30 µL substrate volume and 120 min turnover.
  * Make the U1 decision rest on E1.3, which is well resolved (8 nM over 3 nM), with E1.8 as a consistency check
    only.

**S8. A faster go/no-go exists inside Stage 1.**
* Only E1.1 → E1.2 (U3) and E1.3 (U1) bear on reachability. By the schedule in docs/06 §10, both can be done by
  about week 5. G1 waits until week 7–8 for E1.4–E1.10 and the BLI service.
* Change recommended:
  * Add a "G1a" at week 5 that applies the B3 rule to U1 and U3 alone.
  * Book the BLI/SPR service and order NISTmAb only after G1a passes. Both are spent before G1 today and are
    useless if U1 kills.
  * Add the B4 reservoir arm to G1a.

**S9. The interdigitated cell and second potentiostat are carried forward by momentum.**
* Evidence:
  * docs/05 §1.2: thin-layer cells 1.1–1.5× worse in LOD.
  * Model, n = 1000, same seed, with `replace(arch, detector="thin_layer")`:

    | | IDA flow cell | single-channel thin-layer cell |
    |---|---|---|
    | P-chamb, today | 0.25 | 0.23 |
    | P-chamb, L6 + L7 | 0.52 | 0.48 |
    | S-chamb, today | 0.27 | 0.19 |
    | S-chamb, L6 + L7 | 0.35 | 0.28 |

  * The IDA is the longest-lead, custom, unverified-pairing item. docs/06 §2 still invites ordering it at G1 "at
    the user's risk".
* Gamry's bipotentiostat page lists 620+620 and 620+3000 pairs. The same page also shows the Reference 600+ in its
  specifications and a video captioned "Bipotentiostat with 2 600+ Potentiostats". So the docs/07 statement "the
  600+ is not listed" is inaccurate, and a 600+ pair may also be possible (ask Gamry, S0.2).
* Change recommended:
  * Make a commercial single-channel thin-layer (or wall-jet) cell the Stage-3 default.
  * Buy the IDA and a second channel only if the G2 data show that electrochemical noise is a material part of the
    blank SD. docs/06 §5 already suggests this, but §0, §2 and docs/07 §3 do not follow it.
  * Remove the "order at G1 at the user's risk" sentence.

**S10. Several sources are cited with more weight than they carry.** Full table in §4.
* Qu1998 "up to 15×" is the overall LOD gain (39 → 2.5 pg/mL), not the detection-on-capture factor.
* Hashida1985 compares conjugation methods, not Fab′ with IgG.
* Wilson2004b used +420 mV on IrOx, not +0.35 V. Della Ciana1996 used +350 mV and supports the value.
* The phosphate K_i comes from E. coli AP (O'Brien2002), applied to a calf-intestinal ALP conjugate.
* Pollema1992 shows bead renewal at 155 ng/mL with a competitive fluorescence readout. It is not a precedent for fM
  sandwich work.
* Change recommended: correct the wording in docs/01 and docs/05 (the orchestrator) and tag the L3 magnitude as
  unsupported. E1.7 already measures K_i.

**S11. HQDP stability is tested for 8 h, but sequences run for more than 24 h.**
* docs/06 E1.2 step 3 covers 0–8 h.
* docs/06 §7.7 and E3.6 run unattended for more than 24 h, with HQDP in the B1 line through the BSM's steel heads
  and mixer (docs/02 §1.1 wetted materials).
* Change recommended:
  * Extend E1.2 to 0, 1, 2, 4, 8, 24 and 30 h.
  * Add an aliquot pumped through the BSM and loop, sampled at the outlet.

**S12. Sequencer behaviour after a fault leaves beads in the trap for the next sample.**
* The safe state sets the magnet on (`cycle_primary.yaml` `safe_state`). A fault during `clean` therefore retains
  that run's beads.
* Nothing latches the fault across runs: `run_sim.simulate` arms the next cycle regardless, and Empower keeps
  injecting.
* Change recommended: add a fault latch. After a fault, every subsequent run is flagged invalid until a recovery
  cycle has completed (magnet off, 300 µL/min flush, cup rinse) and been logged. The run report should show the
  latch.

**S13. The chamber approximation hides two small optimisms.**
* The stirred-capture factor is pinned at 0.45 and not sampled (`final_designs.py` `chamber_ps`).
* P values are computed before the 1/0.96 transfer factor. Corrected: P-chamb 0.268 vs 0.281 reported; S-chamb
  0.267 vs 0.281.
* Mixing by a 50 µL aspirate/dispense every 2 min (docs/05 §4.1) is not the "well mixed" factor 1.0 that 0.45
  assumes.
* Change recommended: sample the factor over [0.2, 1.0]/2.2 and apply 1/0.96 before computing P. Expect P to fall
  by a few hundredths. E3.3 is the right bench check.

### Worth knowing

* **W1. Two definitions of time to result.** docs/05 measures from aspiration start to cycle end: 56.1 min. The
  automation measures from Inject Start to the end of the post-baseline window: 52.1 min (`test_analyze`). Both
  are ≤ 60 min. The validation report should state which one it uses.
* **W2. The U1 analysis averages all exposures.** `analyze.u1` reports the geometric mean over all 12
  standard-wash exposure points. The design-relevant figure is the 0.3 nM × 30 min cell (with β). If NSB is not
  linear, the two differ.
* **W3. Beads pass through the optical detector.** In the clean step, beads go "to waste at 300 µL/min" through
  V3 bypass → TUV. Route them to waste before the optical cell.
* **W4. Substrate fill may not be fully switched.** The 200 µL substrate fill (1 min at 200 µL/min) is about the
  BSM dwell volume (≤ 100 µL, `hw.bsm.delay_volume_to_injector_outlet`) plus the 100 µL loop if it stays in line.
  The trap may receive partly switched A1/B1. Use Loop Offline, or lengthen the fill, and check it in E2.1.
* **W5. The baseline windows may sit at a different flow from the readout.** The pre-baseline lies inside the
  accumulation step at "10–50 µL/min", while the readout runs at 10 µL/min. A flow step on an amperometric cell
  shifts the background. Fix the shunt flow at 10 µL/min for the last 0.5 min before readout.
* **W6. The IDA collector potential is marginal.** The collector at −0.15 V vs Ag/AgCl (pH 9.5) lies only about
  0.1 V beyond the estimated HQ/BQ formal potential, and Au/Pt reduce dissolved O₂ there. E3.1 should measure the
  O₂ background and the sensitivity to reference drift over a day.
* **W7. Monte Carlo noise.** P at n = 1000 differs from n = 2000 by up to 0.03 for the same design: P-chamb 0.25
  vs 0.28. Differences in P below about 0.05 between designs in docs/05 are within sampling noise. docs/05 §1.1
  says "about ±0.01"; that is 1 SE, not a 95 % range.
* **W8. Non-immune beads do not match the capture format.** E1.3 uses biotinylated normal goat **IgG**, while the
  capture reagent is goat **F(ab′)₂**. Use normal goat F(ab′)₂ so that the non-immune beads differ only in
  specificity.
* **W9. An alternative substrate exists.** p-Hydroxyphenyl phosphate (Della Ciana1996: HQ LOD 0.12 nM, free ALP
  1.2 fM) releases one Pi per HQ instead of two, which halves the phosphate that sets the ULOQ. No supplier was
  found in this session either. The single-supplier HQDP risk remains, as docs/06 §11 states.
* **W10. Overlap needs a second cup.** docs/05 §4.1 says "previous sample's readout can run here" during
  incubation. With one cup the cycle cannot overlap, so throughput is one sample per 56 min until a second cup
  exists (docs/05 itself says so a few lines later).

## 3. Reproduction

### 3.1 Commands re-run (clean snapshot of HEAD in the scratchpad; Python 3.13)

| Command (docs/05 §6) | Result |
|---|---|
| `python scripts/final_designs.py` | `final_designs.md` and `.csv` **byte-identical** to the committed files; every number in docs/05 §0, §3 and §4.4 checked against it matches |
| `python scripts/kill_thresholds.py` | identical (P-chamb 0.15 → median 5.9, P 0.06; free HQ 10⁻⁴ → 0.12; 10⁻⁵ → 0.30) |
| `python scripts/recovery_options.py` | identical (route A 2.0 [0.36–73] ~0.28; after L6 + L7 0.93 [0.23–4.9] ~0.55) |
| `python scripts/inline_chamber.py` | identical |
| `python scripts/incubation_queue.py` | identical |
| `python scripts/run_baseline.py --n 1000` | `results/baseline_table.md` identical (see §3.4 for the default-n caveat) |
| `optimise_designs.py`, `edge_checks.py`, `gain_decomposition.py`, `robustness.py` | not re-run (about 35 min or more each); their optima feed `final_designs.py` through the committed JSON, which reproduces |

### 3.2 The Monte Carlo fix does not change docs/05

* Commit 6cbf85e makes `ParameterSet.with_values` share the access log, so `montecarlo.run` now samples
  architectures built with `with_design()`.
* For all five final designs (P-vial, P-chamb, B-bed, F-seq, S-chamb) at n = 2000 and seed 20261111, the per-draw
  LODs of the fixed `montecarlo.run(arch_with_design)` and of the docs/05 workaround `design_lib.mc` are
  identical: max |ΔLOD| = 0.0, with the same 48–49 sampled keys.
* The workaround and the fix are therefore equivalent. docs/05 numbers stand, and either path is right.

### 3.3 Additional model runs made for this review

All run with `scripts/design_lib.py` on the committed parameters:
* the B3 table, with `L.pin(ps0, label_factor=x, nsb_effective_rate_constant=4e-11,
  surface_factor_magnetic_beads=1)`;
* S4, with `chem.antibodies.koff_detection` pinned;
* S9, with `replace(arch, detector="thin_layer")`;
* S13, the 1/0.96 correction applied before thresholding.

The scripts are in the review's scratchpad (`kill_pinned.py`, `alt.py`, `cmp_mc.py`), not in the repository; each
is under 40 lines and can be rebuilt from this description.

### 3.4 Baseline

* `python scripts/run_baseline.py --n 1000`, the command docs/04 §5 states, gives `results/baseline_table.md`
  **identical** to the committed file. That file headlines B-mag1-IDA/alp_hqdp at 0.56 nominal, 2.3 [0.39–35],
  P(LOD ≤ 1) 0.246.
* `python scripts/run_baseline.py` without `--n` now uses `monte_carlo.default_samples` = 2000 (raised by Task 4)
  and gives 2.1 [0.44–36], P 0.247. That matches docs/05's baseline row (2.1 [0.44–36]) but not the committed
  `results/` files.
* docs/05 §1.1 quotes "median 2.32, P 0.21". That mixes the n = 1000 median with the n = 2000 / 61-point
  P(success).
* Recommendation: state `--n 1000` wherever the committed baseline is cited (docs/03 §1 says so, CLAUDE.md does
  not), or regenerate `results/` at n = 2000.
* The pre-audit docs/03 §9 table (17 pg/mL headline) is not reproducible from the current parameters, by design:
  docs/04 superseded it (S1).

## 4. Sourcing check (20 claims)

Checked against PubMed abstracts, PMC full text or vendor pages in this session.

| # | Claim (where) | Source | Verdict |
|---|---|---|---|
| 1 | Simoa blank about 1 % active beads; detection Ab about 1 nM × 45 min; SβG 1–50 pM × 30 min; 2.7 µm beads (docs/04 §3.1) | Rissin2010, PMC2919230 | **Holds** |
| 2 | Commercial ELISA "NSB level equivalent to 85 fM", LOD 21 fM (docs/04 §3.1, the label-factor anchor) | Rissin2010 | **Holds** (quoted). The derived 8 % CV (docs/04 §3.8) is an inference |
| 3 | k_on 9×10⁴–1.2×10⁶ M⁻¹s⁻¹, k_off 3×10⁻⁶–1.3×10⁻³ s⁻¹ (docs/06 E1.6) | Chang2012, PMC3327511 | **Holds** |
| 4 | 13 % of complexes labelled at 15 pM SβG × 30 min | Chang2012 | **Holds** |
| 5 | Capture density about 1×10¹⁶ m⁻² (docs/05 §4.1) | Chang2012: 274 000 Ab per 2.5 µm bead → 1.4×10¹⁶ m⁻² | **Holds** |
| 6 | Effective K_D < 10⁻¹¹ M with rebinding (docs/06 E1.5) | Chang2012 | **Holds** |
| 7 | Detection k_off nominal 8.6×10⁻⁴ s⁻¹, "Chang2012; Kamat2020" | Chang2012 gives a PSA mAb in solution; its on-bead fit is "~10⁻⁴ s⁻¹" | **Holds, but the YAML note itself cites the on-bead 10⁻⁴.** The nominal is the conservative solution value; docs/05 should say so. Polyclonal reagents: see S4 |
| 8 | Mouse anti-human-Fc mAbs with t½ 1.4–3.3 min (docs/06 E1.6) | Kamat2020 (PubMed 31926892) | **Holds**. The same abstract reports sub-nM goat AHC pAbs, which supports the goat capture choice |
| 9 | 300 capture–regeneration cycles (docs/05 §4.2) | Kamat2021 (PubMed 34788604) | **Holds**, for Biacore surfaces; transfer to pH 2 regeneration of a streptavidin–biotin bed is UNVERIFIED |
| 10 | Human IgG on lab equipment (docs/05 §4.5, docs/06 §8.1) | Parry1997 (PubMed 9126687) | **Holds qualitatively**: ≥ 1/3 of tip-cone eluates in every lab. **"100 fg per sample" is not in the source** (S5) |
| 11 | Detection-on-capture "up to 15× when not suppressed" (docs/05 §4.1, §4.5) | Qu1998 (PubMed 9618193) | **Misquoted.** The mechanism holds ("specific aspecificity", mouse serum 0.25 % fixes it). 39 → 2.5 pg/mL is the overall LOD change, which also includes the electrochemical upgrade and blocking |
| 12 | HQ FIA-EC LOD 0.12 nM at +350 mV; free ALP 1.2 fM (docs/06 E1.1) | DellaCiana1996 (PubMed 8690930) | **Holds**. The substrate there was p-hydroxyphenyl phosphate (W9) |
| 13 | HQDP does not foul electrodes; "excellent hydrolytic stability" (docs/05 §4.1) | Wilson2004 (PubMed 15308232) | **Holds qualitatively**, on IrOx electrodes. "So the electrode is reused" for a day on Au/Pt is an extrapolation |
| 14 | Generator +0.35 V vs Ag/AgCl "DellaCiana1996 and Wilson2004b" (docs/05 §4.1) | Wilson2004b (PubMed 14709387) used +420 mV | **Partly misquoted**: DellaCiana supports +350 mV, Wilson2004b does not |
| 15 | Phosphate K_i about 1–2 µM (`chem.enzymes.alp.phosphate_inhibition_Ki`) | O'Brien2002 (PubMed 11863460) | **Holds for E. coli AP.** Applied to a calf-intestinal ALP conjugate without a source; INHERITED tag correct; E1.7 measures it |
| 16 | Sequential-injection immunoassay with renewable magnetic beads (docs/05 §4.0 "proven concept") | Pollema1992 (PubMed 1503215) | **Holds as a concept** (electromagnet bead reactor, beads discharged each run). The precedent is 155 ng/mL competitive fluorescence, so "proven" is too strong for fM |
| 17 | Immune complex transfer detected 600 molecules of ferritin (docs/05 L4) | Ishikawa1990 (PubMed 2073754) | **Holds** |
| 18 | Transfer "minimized" conjugate NSB; 10–300× over conventional ELISA (docs/05 L4) | Hashida1997 (PubMed 9292394) | **Holds**. That scheme used DNP/anti-DNP elution and β-gal, not desthiobiotin |
| 19 | Desthiobiotin–streptavidin reversed by biotin (docs/05 L4) | Hirsch2002 (PubMed 12419349) | **Holds** |
| 20 | Fab′ conjugates gave lower background (docs/05 L3) | Hashida1985 (PubMed 3926824) | **Misread**: it compares an improved with an older conjugation method, both Fab′. Ruan1986 (PubMed 3532911): LOD 0.1 → 0.02 mU/L (5×) with Fab′-HRP plus normal F(ab′)₂ **holds**, but does not compare with IgG. L3's ×0.5 has no quantitative support (docs/05 says so) |
| 21 | Gamry bipotentiostat pairs; "600+ not listed" (docs/07 §3, docs/06 §0) | gamry.com/potentiostats/bipotentiostat | **Partly wrong**: 620+620 and 620+3000 are listed, but the page also shows the 600+ in its specifications and a "Bipotentiostat with 2 600+ Potentiostats" video (S9) |
| 22 | Metrohm DropSens HQDP DRP-HQDP-0.5G, no purity specification (docs/07) | metrohm.com product page | **Holds** (500 mg and 1 g; purity, free HQ and storage not stated) |
| 23 | M-280 capacity about 10 µg biotinylated IgG per mg (`chem.surfaces…capacity`) | Thermo user guide and brochure (search summary) | **Holds** ("up to 10 µg/mg") |

Not reached: Coburn1998 (the second K_i source), Larsen2014, Popat2004, Xian2023, Wahlgren1995, Marsh2002,
Zhang2020, Frutiger2021, Rishpon1997; Waters I-Class BSM and SM-FL specification pages; the CLSI EP17 primary
document; the M-280 beads-per-mg figure, which was not re-checked.

## 5. Fixes made in this review

| Location | Fix |
|---|---|
| `automation/elisa_auto/analyze.py` `detection_on_capture` | ratio formed on background-subtracted signal; warns if no background rows; unresolvable if a corrected arm is ≤ 0 (B2) |
| `automation/templates/detection_on_capture.csv` | 4 `background` rows (synthetic, like the rest of the template) |
| `automation/tests/test_analyze.py` | new test `test_detection_on_capture_subtracts_background` |
| `docs/06_bench_plan.md` §4.0 | assay buffer changed from PBS to TBS, with the reason (B1) |
| `docs/06_bench_plan.md` S0.6 | "only matters for the backup bed" corrected: the primary reads out at 10 µL/min |

Tests as run after the fixes: see §8.

## 6. Checked and found sound

* **Numbers:** docs/05 §0, §3 and §4.4 tables against `final_designs.md`, and docs/06 E1.2 and E1.3 quotes against
  `kill_thresholds.md`. All match.
* **Arithmetic:**
  * E1.3 hand example: factor 0.040.
  * Bead area π·d².
  * HQ per 10⁴ enzymes: 1.2 nM in 50 µL in 60 min.
  * Conjugate excess: 1.2×10¹⁰ molecules.
  * docs/06 §12 statistics: χ² intervals of the SD, 1.51 SD at n = 8, power 0.82 at n = 12, 0.63·SD for n = 5.
* **Consistency with user decisions:**
  * docs/05–07 and `automation/` assume the 100 µL loop with full-loop injection, no reagent in sample vials, and
    valves to be bought.
  * PLNO appears only as a Stage-1 FIA readout tool in docs/06 E1.1, not in the product.
* **Gate thresholds:** `gates.yaml` matches docs/05 §5 and docs/06 §4.11, §5 and §6 value by value. The B3 issue is
  in the logic, not in the transcription.
* **LOD code:** `stats.lod` implements the brief's definition: mean blank + 3 SD with n − 1, through the low-range
  calibration with the intercept fixed at the blank mean. It also reports the free-intercept and UCL variants
  (docs/06 §7.4).
* **Stage-1 conversion:** `stats.label_factor` implements docs/05 §5 exactly.
* **Model feedback:** `model_feedback` pins the coupled NSB factors correctly, and never writes to `params/`.
* **Sequencer:**
  * timing anchored to each Inject Start;
  * watchdog on late, early, unexpected and wrong-code injects;
  * every safe-state item attempted independently;
  * the PC-death limitation is stated honestly.
* **Hardware stubs:**
  * every vendor call raises `NotImplementedError` with what is missing;
  * no invented commands;
  * the LabJack U3-HV analog-only FIO0–3 lines are avoided in the example config.
* **Gamry worker:** the Python 3.7, standard-library-only constraint is tested.
* **Bench plan:** Stage 1 buys no instrument-class item. Its replicate sizing is derived from the gate statistic,
  not habit (with the exceptions in S6 and S7). Contamination hygiene starts on day 1.

## 7. What could not be checked

* Bench reality of any UNVERIFIED parameter.
* Whether the IDEX, Hamilton and LabJack command sets and the ToolkitPy API match the stubs. The manuals were not
  read here either.
* Empower Toolkit capability and SM-FL rear-panel event I/O.
* The I-Class BSM at 1–10 µL/min.
* The four long optimisation scripts (§3.1) were not re-run. Their outputs were taken as given through the JSON
  optima, which do reproduce downstream.
* Sources listed as not reached in §4.
* The automation on Windows and with real hardware.
* Physical behaviour of the stirred cup and trap.

## 8. Test results as run

Run in /home/user/ELISA after the fixes in §5:
* `python -m pytest -q` → **64 passed**. No src or params change was made.
* `python -m pytest -q automation/tests` → **32 passed**: the 31 at hand-over plus the new E1.4 test.

CLAUDE.md still says "31 passed at hand-over". The orchestrator may update that; this review does not edit
CLAUDE.md.

Nothing was committed or pushed.
