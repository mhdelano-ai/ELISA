# 16 — Second-generation cartridge: decision

Status: 2026-11-12. Closes the cartridge design round (docs/09–15). Inputs: docs/00, 05, 06, 07, 08 §9–§10, 09, 10,
11, 12 (with its corrections box), 13 **Revision B**, 14 (revised after review), 15 (review; its "Resolution of
findings" section was added with this document). No model run was made for this document: every number is quoted from
the section named next to it (nearest-model estimates, n = 2000, seed 20261111, success = L_eff ≤ 1, docs/05
convention). ΔP < 0.05 is not decision-grade (docs/06 §12.6, docs/08 W7). **UNVERIFIED** = not traceable to a checked
source; **Derived** = arithmetic shown here; **[assessment]** = judgement.

---

## 0. Summary and decision (one page)

**Decision.**
* **A — multi-run bead-transfer cartridge (docs/13 Revision B) is the leading concept.** It is not yet a buildable
  design: its layer stack, contact route, read scheme and schedule were redesigned after the review on paper only
  (docs/15 A1, A2, S2, S3), and every one of those fixes has a bench check (§6).
* **B — indexed single-use cells (docs/12 §4, docs/14 Part B) is the fallback.** Switch to B only when one A-side
  failure **and** both B-side conditions hold (docs/14 §B7): A-side — residual beads > 1×10⁻⁴ of the dose that a
  rinse/flush redesign cannot fix (M1, or PE2 showing persistent residual activity), chamber mixing factor near its
  0.2 lower bound (M2), or bead dose CV > 5 % over 8 h (E2.2/M3); B-side — packed-bed NSB factor ≤ 2 (B-E1) **and**
  cell-to-cell blank CV ≤ 10 % (B-E2). B is also the only candidate if carry-over must be zero by construction.
  Valve failure on A alone does not trigger B (docs/14 §B7 (iv)).
* **C′ — permanent glass chip with a renewable micro-bed and dock-side valves (docs/14 Part C) is kept alive** on
  three bench conditions (docs/14 §C3.11): (1) end-to-end carry-over ≤ 1×10⁻⁴ on a renewable-bed mock-up (C′-R1(c),
  100 ng/mL challenge or ≥ 10 challenge pairs; r_b ≤ 10⁻³ and strip survival s ≤ 3×10⁻² as intermediate gates);
  (2) packed-bed NSB factor ≤ 2 (≲ 1.7 for P ≥ 0.30 without credit; C′-R2 = B-E1); (3) blank CV ≤ 12 % over 20
  repacks (C′-R3). A fourth condition applies only to the S4a protection (guard-cell escape ≤ 0.05, C′-R6/E1.2b).
  docs/12's C (regenerated covalent bed) is not viable (docs/14 §0).

**The honest statement.** **No candidate has a decision-grade LOD advantage over gen-1.** Without the
pre-electrolysis credit: gen-1 primary 3.5 pg/mL, P 0.16; A Rev B 3.67, P 0.150; B 2.3, P 0.15; C′ 2.4, P 0.15.
After U1–U3 screening: gen-1 1.3 / 0.32; A 1.34 / 0.328; B 1.8 / 0.20; C′ 1.8 / 0.21 (§1). The pre-electrolysis
credit is worth +0.065 for A at nominal (0.150 → 0.215), nothing after screening, and decides only the S4a scenario
(lot free HQ 10⁻³: A 0.000 → 0.171) — and it is UNVERIFIED until E1.2b and M5a (docs/13 §1.3). **The case for a
cartridge rests on throughput, automation and buffer use**: one result every 31 min instead of every 56 min
(docs/13 §7.1; docs/12 §6), ≈ 1.9 mL of liquid per determination instead of ≈ 5–6 mL (docs/13 §3.7; docs/09 §3.6),
a fluidic path the dock can run without tubing changes, and a carry-over monitor in every run (PE2, docs/13 §3.6).
A's own case among the cartridges is that it keeps the one-step format (the only one that profits from reagent
screening: A 0.328 vs B 0.20, C′ 0.21) and does not depend on the unmeasured packed-bed NSB factor.

**What is decided.** A leads, B is the fallback with the triggers above, C′ is kept alive on its conditions; the
user decisions of §2 are fixed; **the only cartridge bench work before G1 is M5a** (§6.1); everything else for the
cartridge waits for G1 (docs/06 §4.11) and E1.2b; the gen-1 G1 rule is unchanged and no cartridge result is a G1a/G1
input.

**What is not decided.** Whether a cartridge is built at all (that follows GC1, §6.3, and needs a G1 GO or
GO-WITH-LEVER first); A's read mode (step read vs R-flow fallback: M5a); whether the pre-electrolysis credit exists
(E1.2b + M5a-4); B vs C′ as the second line (B-E1 = C′-R2); the fabrication route for series (C3); the model
extensions of docs/09 §5.4 (left for a later round, §8). The M5a slot in weeks 6–8 does not fit the bench load as
planned (docs/06 M5a; §6.1 here) — the user must choose how to place it (§8 Q1).

---

## 1. The comparison table (single authoritative version)

This table supersedes docs/12 §0 and §6 and docs/14 §0 and §F for every A value (docs/15 S10). A is docs/13
**Revision B**. "Credit" = pre-electrolysis factor on `ma.chemistries.alp_hqdp.free_product_impurity`: ×0.01 for A's
in-cell electrolysis (escape computed 0.2–0.5 %, docs/13 §3.6), ×0.05 for B and C′ (per-run guard-cell fill at
≥ 300 µL/min, docs/14 §B0, §C3.1); all credits UNVERIFIED pending E1.2b (docs/06) and, for A, M5a-4. Gen-1 has no
admissible credit as designed (guard cell below its minimum flow and a baseline mismatch, docs/15 S8 (iii)).

| | **Gen-1 primary** (reference) | **A** Rev B — leading | **B** — fallback | **C′** — kept alive |
|---|---|---|---|---|
| Median LOD [5–95 %] / P as specified, **no credit** | 3.5 [0.51–157] / 0.16 (docs/12 §8 REF row; docs/08 §10.1 gives 0.51–158) | **3.67 [0.53–126] / 0.150** (docs/13 §1.3) | 2.3 [0.52–23] / 0.15 (docs/14 §B6 B0) | 2.4 [0.50–26] / 0.15 (docs/14 §C3.7 C′0) |
| Same, **with credit** (scenario) | — (not admissible, docs/15 S8 (iii)) | 2.33 [0.44–63] / 0.215 (×0.01) | 2.1 [0.50–21] / 0.17 (×0.05) | 2.1 [0.47–23] / 0.16 (×0.05) |
| After U1–U3 screening (L6 + L7): median / P, no credit | 1.3 [0.34–9.3] / 0.32 (docs/08 §10.1) | 1.34 [0.33–9.0] / 0.328 | 1.8 [0.45–17] / 0.20 | 1.8 [0.42–21] / 0.21 (ULOQ 794 flagged) |
| Same, with credit | — | 1.33 [0.33–8.9] / 0.330 | 1.8 / 0.20 | 1.8 / 0.21 |
| Under S4a (lot free HQ 10⁻³): P no credit / with credit | not re-run with the review corrections (docs/05 §0: ≤ 0.03, pre-review) | 0.000 / 0.171 (0.056 if stubs are 1 mm) | 0.007 / 0.13 | 0.015 / 0.14 |
| Inject Start → result | 52.1 min (docs/06 §7.8; 56.1 from aspiration, docs/05 §4.1) | **56.75 min** (57.75 from aspiration; margin 3.25 min) (docs/13 §7.1) | 50.0 min (51.0 from aspiration) (docs/12 §4.4; model time 52.0, docs/14 §B6) | 37.5 min (38.5 from aspiration) (docs/14 §C3.4) |
| Cadence (one result every …) | ≈ 56 min; ≈ 30 with a second cup (docs/12 §6) | 31.0 min (2 staggered chambers; feasible 30.0–33.0) (docs/13 §7.1) | ≈ 26 min (2 heads) (docs/12 §4.4) | 45.5 min; + ≈ 55 min per carry-over trigger (docs/14 §C3.4, §C3.8) |
| Determinations per card / per 8 h | no card; ≈ 8.6 per 8 h (Derived 480/56) | **14 per card** (10 samples + 4 QC) in 7.86 h from insertion (docs/13 §5.2, §8.2); a result > 100 pg/mL costs one slot (§7.4) | 16 cells per card (13 samples + 3 QC) (docs/14 §B1); ≈ 18 per 8 h (Derived 480/26) | no card; ≈ 10 per 8-h pack day (480/45.5 = 10.5, docs/14 §C3.4); 10 runs + 2 priming + 1 recovery per pack (docs/14 §C3.6) |
| Valves; max actuations | 3 external valves + 8-port SIA (docs/12 §6) | 21 on the card (17 valves + 4 gates); 16 actuations per run (18 fallback); busiest 17 per card (31 fallback) (docs/13 §4) | 80 pinch points per card, ≤ 3 actuations each; ≈ 10 dock solenoid operations per determination (docs/14 §B1, §B2) | 0 on the chip; dock selector ≈ 3000 actuations per 300 runs vs "tens of thousands" rated; solenoids ≥ 10⁷ (docs/14 §0, §C2) |
| Carry-over vs 1×10⁻⁴ (criterion kept + cleaning cycle and blank check after any result > 100 pg/mL) | criterion tested E1.10/E2.7/E3.4 (docs/06); residual-bead acceptance 10⁻³ in E2.4 is inconsistent (docs/09 §7; open, docs/06 §13) | budget 9.6×10⁻⁵ allocated (docs/13 §8.3), **closes only if the SM-FL reaches 3×10⁻⁵** (nominal 10⁻⁴, UNVERIFIED); PE2 monitor every run; post-high cycle costs one slot (§7.4) | 0 by construction except SM-FL and head bore (docs/14 §B0) | five-path budget 1.0×10⁻⁴, unproven (docs/14 §C3.8); at r = 10⁻⁴ after a 1000 pg/mL predecessor P 0.15 → 0.10 (docs/14 §C3.7); ≤ 0.01 cost for r ≤ 3×10⁻⁴ under the user's rule |
| Liquid per determination | ≈ 5–6 mL waste, A1 ≈ 4.3 mL (docs/09 §3.6, §3.4) | ≈ 1.9 mL (docs/13 §3.7) | not stated in docs/12/14 | not stated as a total; pack ≈ 0.2 mL + A1 ≈ 0.25 mL (docs/14 §C3.6) |
| Consumable cost class [assessment] | reagents only (docs/12 §6) | medium (docs/14 §B5) | high | low |
| Evidence strength [assessment] | medium (docs/12 §6) | medium: every element has a precedent, no multi-run liquid-bead cartridge precedent; no endurance evidence for TPE on COC (docs/12 §6, docs/13 §4) | strongest format precedent (Gyrolab, Ella, i-STAT) but optical and ≥ 10 pg/mL (docs/12 §6) | medium-low: renewable-surface sandwich in flow (Grate2009), trap/release (Fu2011); no residual-bead number found (docs/14 §F) |
| Biggest unknown | U1/U3 (docs/12 §6) | step-read background SD(Q_net) ≤ 0.05 nC (M5a), residual beads ≤ 10 per path (M1), chamber mixing factor (M2), TPE flat-floor valve (M4) | packed-bed NSB factor (P 0.33 at ×1 ↔ 0.06 at ×10), cell-to-cell CV, dried reagents | carry-over ≤ 10⁻⁴ (C′-R1) and the packed-bed NSB factor |

**Numbers checked against their source sections and the inconsistencies found.**
* A: every A figure above is docs/13 Rev B (§1.3, §3.7, §4, §5.2, §7.1, §8.3); docs/12 §0/§6 (2.3/0.20, 54.0 min,
  27.5 min, 21 valves, busiest ≈ 70) and docs/14 §0/§F/§C3.11/§F1 (2.45/0.20, 1.12/0.37, ≈ 58.9 min, 20 valves) are
  superseded designs. docs/14 §F says so itself; docs/14 §C3.11 and §F1 still quote "0.37 for A + L6 + L7" — the Rev B
  value is **0.328** (no credit) / 0.330 (credit).
* Gen-1 interval: docs/08 §10.1 prints 3.5 [0.51–158], docs/12 §8 and docs/14 §F 3.5 [0.51–157] (rounding of the same
  run); either is fine.
* B time to result: 50.0 min is the step-table time (docs/12 §4.4); 52.0 is the model's own timeline (docs/14 §B6).
  The table uses the step table, as for A and C′.
* A margin: 3.25 min after Inject Start, 2.25 min after the start of aspiration (docs/13 §7.1). docs/00 defines the
  limit "injection to result", so the user's "≥ 3 min margin" is met on the Inject Start basis only (§8 Q6).
* C′ residual analyte at r = 10⁻⁴ after 1000 pg/mL: docs/15 S9 gave P 0.152 (additive, but log-triangular sampling of
  the default 0–3 fM term); docs/14 §C3.7 re-ran it with linear sampling and gets **0.10**. This document uses 0.10
  (docs/15 Resolution, S9).
* Capture gain from the smaller chamber dilution: ×1.21 (docs/12 §10, box item 8) vs ×1.17 (docs/15 §2, W8); Rev B
  uses the real dilution /1.85 in its runs (docs/13 §1.3), so neither factor enters the table.

---

## 2. Fixed user decisions (verbatim as recorded, 2026-11-11/12)

Do not reopen without the user.

1. **Scope** (interview, 2026-11-12; docs/09 header): cartridge with fluidic path + on-chip valving + reagents;
   docking station may contain anything; second generation (gen-1 tubing rig is built first); assay format reopened;
   criteria unchanged; decisions on nearest-model estimates (no model extension this round).
2. **At the candidate checkpoint** (docs/12 §9): A to detailed design, B fallback, C kept alive (→ C′);
   pre-electrolysis added to the gen-1 plan as a bench TEST only (E1.2b, informational, not a G1a/G1 input).
3. **After the review** (docs/15 §6):
   * dock-supplied reagents accepted (beads in a cooled agitated dock vial; conjugate and substrate tanks on the
     card filled from dock bottles at insertion) — supersedes "reagents on the cartridge";
   * card capped at ~14 determinations with ≥ 3 min margin to 60 min;
   * carry-over criterion 1e-4 kept plus mandatory cleaning cycle and blank check after any result > 100 pg/mL;
   * the read-background test M5a on a catalogue electrode die with the existing Gamry is approved before G1
     (weeks 6–8);
   * everything else for the cartridge waits for G1 and E1.2b.

The docs/00 decisions continue to apply: sample vials contain sample only; 100 µL injected (full loop, ≈ 200 µL
drawn); Python orchestrates, Empower runs the Waters stack; a second potentiostat channel is acceptable. The operator
loads a bead vial and two reagent bottles per card before loading the autosampler; that is not a manual step between
autosampler loading and result in the docs/00 sense (docs/13 §5).

---

## 3. A in brief (details: docs/13 Revision B)

* **Architecture.** A 75.5 × 50 mm card, two stirred incubation chambers (IC1, IC2, 185 µL working) that alternate,
  one shared 1.34 µL, 0.200 mm high readout cell whose ceiling is the working electrode of a glass die. One-step
  incubation (beads + conjugate + sample) 28.5 min; fixed collection magnet per chamber; drag magnet gathers the
  pellet, holds it through six partial-drain rinses and drags it 23.3 mm at 0.20 mm/s along a wash lane into the
  cell; 11-min sealed accumulation in fresh 3 mM HQDP; three-window potential-step read Q_net = Q_a − 2Q_b + Q_c;
  beads to an on-card bead-waste pocket. Fallback read: gen-1-type flow read over WE2, without pre-electrolysis
  (docs/13 §1.1, §3).
* **Layer stack** (docs/13 §2.1): 140 µm COC floor foil (magnets and Peltier below) / 0.175 mm COC channel sheet with
  every channel cut through / 0.3–0.5 mm TPE ceiling that is the membrane of every valve and gate / ≈ 5.5 mm moulded
  COC upper body. Valves are flat-floor: a plunger presses the TPE onto the foil. Plan-view zoning keeps valves over an
  anvil and magnets under windows and a 4 mm drag slot. The die lies face-down and is contacted from below through a
  dry contact window (docs/13 §2.7).
* **Cycle** (docs/13 §7.1): Inject Start every 31.0 min; result 56.75 min after Inject Start; PE2 (residual-activity
  monitor) at 30.1–34.1 and READ at 52.75–56.75 are quiet windows in which no dock actuation of any run happens
  (checked over all run offsets; docs/15 Resolution S3 for the hand spot-check).
* **Dock** (docs/13 §6): 21 plungers, anvil with 9 face seals, two collection-magnet Z units, X–Y–Z drag-magnet
  carriage, hold and waste magnets, five syringe pumps (clean pump dispense-only, waste pumps pull-only), three
  thermal zones (reagent 4–8 °C, assay 25.0 °C), shielded electrode bay with pogo block, hardware watchdog; the
  Reference 600+ (in hand) reads the cell.
* **Reagents** (docs/13 §5): bead stock in a cooled, rocked dock vial; conjugate and HQDP tanks on the card filled from
  dock bottles at insertion; no factory-filled reagent; 8-h in-use life sets the 14-determination cap.

---

## 4. Consolidated risk register (A, B, C′), ranked

Rank = consequence for the cartridge decision × likelihood [assessment]. "Shared" names the experiment that answers
the risk for more than one candidate (or for gen-1 too). Sources: docs/13 §9, §10; docs/14 §C3.10, §B8; docs/12 §3.11,
§4.11; docs/15.

| Rank | Risk | Candidates | Retired by (acceptance) | Shared? |
|---|---|---|---|---|
| 1 | U1 conjugate NSB on beads or U3 free HQ too high (G1 STOP) | all, and gen-1 | gen-1 E1.3, E1.2 → G1a/G1 rule | **shared by everything**: a G1 STOP stops all cartridge spend |
| 2 | Stopped-flow read background SD(Q_net) > 0.05 nC (drift curvature, range offsets, dock EMI) | A (step read); B (single 30-s step read on the PE1 background, docs/12 §4.4) | **M5a** (M5a-1: ≤ 0.05 nC drift-corrected; M5a-2; M5a-6), then M5 on the custom die | **shared A and B**; C′ reads by redox cycling (C′-R5) |
| 3 | Packed-bed NSB factor ≥ 3 | B, C′ | **B-E1 = C′-R2** tube exposure series (≤ 2) | **shared B and C′**; decides whether either has any LOD case (P 0.39/0.33 at ×1 ↔ 0.05/0.06 at ×10) |
| 4 | Residual beads / bead transfer (stranded on lane, cell, chamber) → carry-over and dose CV | A | M1 (transfer ≥ 0.95, CV ≤ 5 %; ≤ 10 beads per pass at J/WLc and in the cell; ≤ 1 bead in IC_k after refresh + cleaning) | C′ has the analogue r_b (C′-R1(a), ≤ 10⁻³) |
| 5 | SM-FL needle/loop protein carry-over ≥ 10⁻⁴ (nominal 10⁻⁴, UNVERIFIED) | all, and gen-1 | gen-1 E1.10 extended by the flush programme (A needs 3×10⁻⁵) | **shared by all**: if ≥ 10⁻⁴, no candidate meets 10⁻⁴ end-to-end (docs/14 §C3.8) and only the post-high rule protects |
| 6 | Chamber mixing factor near 0.2 (capture too slow) | A | M2 (capture ≥ 0.80 of rotated tube); gen-1 E3.3 measures the cup analogue | partly shared with gen-1 E3.3 |
| 7 | Flat-floor TPE valve leaks, sticks or delaminates (no endurance evidence for TPE on COC) | A | M4 (≤ 0.1 µL/min at 20 kPa after 100 cycles, ≥ 1 GΩ, transient ≤ 5 kPa) | B uses single-use pinch points (inside evidence); C′ none on chip |
| 8 | Pre-electrolysis credit not real (chemical floor, or geometric escape > 1 %) | A (×0.01), B and C′ (×0.05) | **E1.2b** (chemical floor, ≤ 0.01) **shared**; then A: M5a-4 (≤ 1 %); B/C′: guard-cell flow test at ≥ 300 µL/min (C′-R6) | shared chemistry; geometry per candidate. Matters for S4a only |
| 9 | C′ end-to-end carry-over > 10⁻⁴ | C′ | C′-R1 (a) r_b ≤ 10⁻³, (b) s ≤ 3×10⁻², (c) ≤ 1×10⁻⁴ with 100 ng/mL challenge | — |
| 10 | Bead dose CV > 5 % from a cooled, rocked dock vial with pauses | A (and gen-1) | gen-1 **E2.2** (with intermittent agitation, docs/13 §10.2), then M3 | shared with gen-1 |
| 11 | Card-to-card slope CV > 10 % (lot calibration insufficient) | A, B | A: M5 on 5 dies, C2 on ≥ 5 cards; B: B-E2 (blank and slope CV ≤ 10 %) | similar test, separate hardware |
| 12 | Dried-conjugate rehydration dose CV > 5 % | B | B-E3 (or avoid: liquid conjugate from the dock, docs/14 §B0) | — |
| 13 | Two-chamber schedule: actuations inside read windows; cadence outside 30–33 min | A | M8 (zero actuations in windows over 20 runs); Stage 0 injection overhead | — |
| 14 | Au quasi-reference shifts within a run | A | M5a step 6 (≤ 20 mV / 8 h, ≤ 2 mV between windows) | — |
| 15 | Bubbles, condensation, vent wet-out | A | M6, M3 | — |
| 16 | IDA contamination without isolation valve; transfer push | C′ | C′-R4, C′-R5 (concentration ≥ 0.8) | — |

---

## 5. Model gaps left for a later round (docs/09 §5.4)

By user decision no model extension was built this round; every number is a nearest-model estimate. The gaps that
matter for the cartridge decision, with the candidate affected (docs/09 §5.4 item numbers; directions from docs/12
§8 and docs/14 §C3.7):

| docs/09 §5.4 item | Gap | Affects | Direction of the omitted effect |
|---|---|---|---|
| 1 | on-chip incubation chamber (mixing, dilution, wall NSB) | A | rests on a sampled factor; the mixing/dilution assumption is worth ≈ 0.045 in P (docs/15 W8; Rev B /2.2 row: 0.135 vs 0.150) |
| 2 | magnetic beads inside a chip (transfer, residual beads) | A | approximated by the gen-1 trap keys |
| 3 | single-WE stopped detector; **step-read background** (white noise, drift curvature, range offsets) | A, B | not represented; entered only through pinned noise rows (docs/13 §1.3; §12.1 item 9) |
| 4 | conjugate delivered on board | A, B, C′ | neutral (docs/12 §8) |
| 5 | decoupled flows | B, C′ | ≈ neutral |
| 6 | zone-resolved NSB | all | A approximated by pinning the tubing factor at 0.01 (worth 0.01 in P, docs/15 §3); B/C′ bed-channel walls worse ≤ ×1.2–1.4 |
| 7 | storage terms (substrate hydrolysis in tanks, conjugate ageing, bead store) | all | worse, unknown |
| 8 | multi-run residuals (residual beads, residual analyte) | A, C′ | C′ represented through the contamination term (docs/14 §C3.7); A not at all |
| 9 | electrode-to-electrode variation | A, B | partly cancelled by the exhaustive read (better) |
| 10 | throughput of staggered chambers | A, B | scratch scripts only (docs/13 `sched.py`) |
| 11 | temperature | all | thermostatted cartridges better, unmodelled |
| 12–14 | wash efficiency / NSB reversibility; pressure budget; HQ sorption and O₂ | all | unknown |

A later round should build items 1, 2, 3 (with the step-read background), 6 and 8 before C2/tooling spend (docs/12 §9
decision 8), and enter the M5a/M1/M2 values there rather than in scratch runs.

---

## 6. Staged plan and gates for the cartridge, relative to the gen-1 gates

```
gen-1 : Stage 0/1A -- G1a (wk 5) -- E1.2b, E1.4-E1.10 -- G1 (wk 7-8) -- Stage 2 (wk 9-16) -- G2 (wk 16) -- Stage 3 -- G3
cart. : C0 desk (now) ---- M5a (approved pre-G1; placement: docs/06 M5a, §8 Q1) --|-- C1 mock-ups -- GC1 --|-- C2 -- GC2 -- C3
                                       G1 STOP or no GO -> no C1 spend ------------'            needs gen-1 G2 --'
```

### 6.1 Pre-G1: M5a only

* **What:** read background on a catalogue Micrux Au die in a clamp cell that reproduces the Rev B stack, with the
  existing Gamry Reference 600+, dock noise sources switched on and off, drift-corrected acceptance (docs/13 §10.1;
  docs/06 M5a). Informational for the cartridge track; **not a G1a/G1 input**; the G1 rule is unchanged.
* **Acceptance (fixed before data, docs/13 §10.1):** M5a-1 SD(Q_net) ≤ 0.05 nC (three-window, n ≥ 30 per die,
  ≥ 3 dies); M5a-2 curvature residual ≤ 0.025 nC in ≥ 95 % of reads, day-to-day mean shift ≤ 0.05 nC; M5a-3 read weight
  0.92 ± 0.05, die-to-die slope CV ≤ 5 %; M5a-4 escape ≤ 1 % with 0.5 mm stubs (1.0 mm cell ≥ 3 %); M5a-5 E_rest charge
  ≤ 1 % of Q_a, QRE ≤ 20 mV / 8 h and ≤ 2 mV between windows; M5a-6 SD with sources in E_rest ≤ 1.2 × quiet; M5a-7
  leakage ≥ 5×10¹² Ω, contact drift ≤ 0.1 Ω over 8 h.
* **Consequence:** M5a-1/2/3 pass → step read retained; any fails → R-flow read (no credit; headline unchanged).
  M5a-4 fails → credit dropped; S4a then has no rescue on A. **Not a kill** on its own; the kill is in §6.3.
* **Schedule:** the approved slot (weeks 6–8) collides with Stage 1 for one bench scientist and one Gamry; docs/06
  M5a states the load and three options. No option slips G1 silently.

### 6.2 After G1 (GO or GO-WITH-LEVER) and E1.2b: C0 corrections and C1 mock-ups (≈ weeks 9–16)

Entry condition: G1 verdict GO or GO-WITH-LEVER **and** an E1.2b outcome recorded (PASS, INTERMEDIATE or FAIL — FAIL
removes the credit, it does not stop C1). G1 STOP (or G1′ STOP) → no C1 spend; C0 stays desk work.

| Step | Content | Acceptance (docs/13 §10.3 unless stated) |
|---|---|---|
| C0 | desk: quotes for laminate parts, dock pumps and stage; open items of docs/15 Resolution | — |
| Shared tube test | **B-E1 = C′-R2** packed-bed NSB factor (no flow hardware) | factor ≤ 2 keeps B and C′ open; > 3 → B and C′ have no LOD case (docs/14 §C3.11, §B8) |
| M1 | collection, gather, drag, bead-out, whole-path imaging | transfer ≥ 0.95, CV ≤ 5 %; floor ≤ 1 %; ≤ 10 beads per pass at J + WLc and in the cell; ≤ 1 bead in IC_k; BW ≥ 99.9 % |
| M2 | chamber mixing, recovery, wash | capture ≥ 0.80 of rotated tube; recovery ≥ 0.90; free conjugate ≤ 2×10⁻⁴ |
| M3 | dosing | bead CV ≤ 5 %, 8-h trend ≤ 5 %; conjugate CV ≤ 5 %; C_k residue ≤ 10⁻³ |
| M4 | laminate valve, 100 cycles, real media | leak ≤ 0.1 µL/min at 20 kPa; ≥ 1 GΩ; transient ≤ 5 kPa; deflection ≤ 20 µm; ≤ 2 beads per gate per 20 passes |
| M5 | readout on the custom die (+ R-flow channel) | M5a acceptances; R-flow SD ≤ 0.05 nC |
| M6 | thermal, bubbles, dew point | ±0.2 °C and 4–8 °C; no bubble in 20 fills; RH margin ≥ 5 K |
| M7 | integrated single chamber | LOD ≤ 1.5 pg/mL; raw carry-over ≤ 1×10⁻⁴ (100 ng/mL challenge, n = 5); PE2 flags every challenge |
| M8 | two-chamber timing, 20 runs | zero actuations in read windows; result ≤ 57.0 min every run; SD under schedule ≤ 1.2 × M5a quiet |
| C′ mock-up (only if B-E1 ≤ 2) | C′-R1 (a)–(c), C′-R3 | r_b ≤ 10⁻³ in 20/20; s ≤ 3×10⁻²; end-to-end ≤ 1×10⁻⁴; repack blank CV ≤ 12 % |

### 6.3 Gate GC1 and kill criteria

**GC1 pass** (docs/13 §10.3): M1, M4, M5 and M8 pass; M2/M3 pass or have a defined fix; measured mixing factor,
dose CV, transfer, read SD and escape entered into scratch model runs (credit only if M5a-4 and M5 passed).

**Proposed model check at GC1 (derived here, fixed before C1 data; user to confirm, §8 Q4):** with the same gen-1
bench values entered for both, A must not be worse than the gen-1 primary by a decision-grade margin
(P_A ≥ P_gen-1 − 0.05) and must stay out of the STOP band (P_A ≥ 0.10). Reason: the cartridge is justified by
throughput and automation, so it may not cost LOD.

**Kill / switch criteria** (any one; derived from the acceptances above and docs/14 §B7):
* G1 or G1′ STOP → no cartridge work beyond C0 (all candidates).
* Read background: both the step read (M5a/M5) and the R-flow read (M5) above **0.155 nC** — the level at which A's
  P falls to 0.097, below the 0.10 STOP band (docs/13 §1.3) → kill A's readout; B shares the risk (rank 2) → no single-
  WE stopped read; C′ (IDA) remains only if its conditions hold.
* M1 residual beads > 10⁻⁴ of the dose (> 50 beads per pass) after two iterations, or transfer < 0.80 → A fails its
  carry-over case → switch to B if B-E1 ≤ 2 and B-E2 ≤ 10 %; else stop the cartridge track.
* M2 capture < 0.50 of the rotated tube after two jet iterations (mixing factor toward the 0.2 bound) → same switch
  rule [threshold derived here from docs/14 §B7 (ii); UNVERIFIED as a model input until entered].
* M4 leak > 0.1 µL/min at 20 kPa after 100 cycles in two material iterations → A's on-card valving fails (gates
  cannot move to the dock) → switch rule as above.
* M7 LOD > 3 pg/mL with all measured values (the gen-1 G2 stop line, `gates.yaml` G2 `lod_pgml`) → stop C2.
* B-E1 > 3 → B and C′ closed (no LOD case); C′-R1(c) > 10⁻⁴ → C′ closed.
* E1.10 SM-FL carry-over ≥ 10⁻⁴ does not kill a candidate but means the 10⁻⁴ criterion cannot be met end-to-end by
  any design; the user's post-high rule is then the only protection (report to the user).

### 6.4 C2 prototype and C3 tooling

* **C2** (after GC1 **and** gen-1 G2; ≈ weeks 17–28; docs/13 §10.4): 10–20 laminated cards, custom die, first full
  dock. **GC2:** LOD ≤ 1.5 pg/mL per card and ≤ 1.0 pooled; blank CV ≤ 0.10; card-to-card slope CV ≤ 10 % per
  chamber; carry-over ≤ 1×10⁻⁴ (100 ng/mL challenge, both path classes); result ≤ 57 min in every run; zero
  actuations in read windows; zero valve failures in 3 cards; docking leak test 100 %. Kill: card-to-card slope CV
  > 10 % forcing a per-card 4-point curve per chamber (8 of 14 determinations) ends A's throughput case (docs/13 §8.2).
* **C3** (after GC2): upper-body mould (MOQ 100), series lamination, bonded die; validation per docs/06 Stage 4
  (G3: LOD ≤ 1 pg/mL, blank CV ≤ 0.10, carry-over ≤ 1×10⁻⁴, ≤ 60 min). No mould before M1 and M4 pass (docs/12 §10).

---

## 7. Gen-1 bench results that would change the cartridge decision

| Gen-1 result | Effect on the cartridge decision |
|---|---|
| **U1** (E1.3) label factor ≥ 0.10 / G1 STOP | stops every candidate (all are NSB-limited the same way, docs/12 §9 decision 1) |
| U1 label factor ≤ 0.02 (GO) | all candidates improve; A gains most (one-step format) |
| **U3** (E1.2) free HQ in the purify band or at S4a | the pre-electrolysis credit becomes decisive: with E1.2b PASS and M5a-4 ≤ 1 %, A keeps P 0.171 under S4a while B/C′ need a guard-cell flow test; without it every candidate fails under S4a |
| **U2** (E1.5) on-bead detection t½,eff < 30 min → sequential mode | A's one-step advantage shrinks (A sequential ≈ gen-1 S-chamb, P 0.13, docs/12 §10); C′'s shorter time and lower cost weigh more (docs/14 §F1) |
| **E1.2b** PASS / INTERMEDIATE / FAIL | PASS: credit stays a scenario pending M5a-4; INTERMEDIATE: credit reduced to the measured f_esc, no S4a rescue; FAIL: every with-credit row is void, headline (no credit) stands, 3 mM re-checked for A (docs/13 §3.6) |
| **E2.2** bead dose CV over 8 h with pauses | > 5 % is a B-switch trigger (docs/14 §B7 (iii)); CV 0.10 → A P 0.124 (docs/13 §1.3) |
| **E1.10** SM-FL carry-over | ≥ 10⁻⁴: A's budget (needs 3×10⁻⁵) cannot close; affects all candidates (§6.3) |
| E1.3 conjugate ageing arm | ageing beyond 8 h would allow more than 14 determinations per card (docs/13 §5.2); faster ageing lowers the cap |
| E1.7 K_i (+ NaCl arm) | sets whether 3 mM HQDP holds ULOQ ≥ 1000 pg/mL in the 1.34 µL cell; NaCl 50 mM effect on ALP |
| E3.3 chamber stirring factor (gen-1 cup) | first measured value of the factor that is worth ≈ 0.045 in P for A (docs/15 W8) |
| G2 LOD₂ and the IDA row | a single-channel LOD₂ > 3 pg/mL stops gen-1 Stage 3 and C2 alike |
| Stage 0 injection overhead | sets A's cadence (feasible 30.0–33.0 min) and so the card cap |

---

## 8. Open questions for the user

1. **M5a placement** (docs/06 M5a, schedule): the approved weeks 6–8 do not fit the bench load; choose (a) shift
   the Gamry-bound part of M5a to weeks 8–10 (set-up in weeks 6–8 by the second person; no G1 slip; recommended), (b)
   keep weeks 6–8 and accept G1 slipping by ≈ 1.5–2 weeks, or (c) a second potentiostat channel for M5a.
2. **F1 relaxation** (docs/09 F1 "capture ≥ 96 % of the injected analyte"): A and B transfer 1.5 loop volumes (0.90 of
   the analyte) by design (docs/13 §3.1, docs/14 §B0). Accept as a requirement change?
3. **Residual-bead acceptance vs carry-over** (docs/09 §7): gen-1 U5/E2.4 accepts residual beads ≤ 10⁻³ while the
   analyte carry-over criterion is 10⁻⁴; A's M1 uses ≤ 10 beads per path. Should E2.4 be tightened? (Open item in
   docs/06 §13; not changed.)
4. **GC1 model check** (§6.3): accept "P_A ≥ P_gen-1 − 0.05 and ≥ 0.10 with the same bench values" as the rule?
5. **Blank-check mode** after a high result: mode A (Empower Toolkit inserts a buffer line; UNVERIFIED) or mode B
   (injection n+2 diverted, sample n+2 re-queued) (docs/13 §7.4, §12.1 Q2).
6. **Margin basis**: A's 3.25 min margin is from Inject Start (2.25 min from aspiration). Confirm Inject Start as the
   reference for the ≥ 3 min margin (docs/00 "injection to result").
7. **QC per card**: 4 slots (blank and control per chamber, 10 samples) or 3 (11 samples) (docs/13 §12.1 Q3).
8. **B-E1 timing**: may the cheap shared tube test (packed-bed NSB factor) run in the Stage-2 lead time right after
   G1, or only after E1.2b is analysed as well?
9. **Model extensions** (§5): which items to build in the next round, and before which stage.

---

## 9. UNVERIFIED decision-critical inputs

| Input | Value used | Where it decides | Resolved by |
|---|---|---|---|
| Pre-electrolysis escape (chemical floor) | ×0.01 (A), ×0.05 (B, C′) | credit rows; S4a rescue | E1.2b; M5a-4; C′-R6 |
| Step-read background SD(Q_net), drift curvature, Gamry range-offset stability | ≤ 0.05 nC target; `hw.gamry.baseline_drift` 5 pA/min (1–10) | A's read mode; P 0.150 → 0.097 at 0.155 nC | M5a, M5 |
| SM-FL protein carry-over | nominal 10⁻⁴ (10⁻⁵–10⁻³); A needs 3×10⁻⁵ | every carry-over budget | E1.10 + flush programme |
| Chamber mixing factor and dilution | sampled; /1.85 | A's P (≈ 0.045) | M2; gen-1 E3.3 |
| Packed-bed NSB factor | nominal 3 (1–30) | B and C′ LOD case | B-E1 = C′-R2 |
| Unstirred capture factor during tidal pauses | 0.5 (`ma.capture.in_vial_unstirred_rate_factor`) | A's 25.33 min effective incubation | M2 |
| TPE-on-COC flat-floor valve leak and endurance | none in the literature | A's buildability | M4 |
| M-280 magnetisation, NdFeB remanence, bead–foil friction | 1×10⁴ A/m; 1.3 T | gather, drag speed margin | M1 |
| Laminate tolerances (0.175 mm sheet, 25 µm film), die position | ±10 % gap → τ ± 21 % | cell height, read weight, stubs ≤ 0.5 mm (escape) | M5, C2 |
| Injection overhead (cadence 31 min); docking time 12 min | ≈ 1 min; 12 min | card cap 14, schedule feasibility | Stage 0; C2 |
| Conjugate and HQDP in-use life | 8 h | card cap | E1.3 ageing arm; E1.2 |
| HQDP hydrolysis k_h, free HQ | 10⁻¹⁰ s⁻¹; 10⁻⁵ | substrate tank at 25 °C; S4a | E1.2 |
| K_i of the conjugate's ALP; NaCl effect | 2 µM (0.2 µM–1 mM) | ULOQ at 3 mM in 1.34 µL | E1.7 (+ NaCl arm) |
| Guard-cell collection 0.95, minimum flow 300 µL/min (THERMO_6011RS) | repository values; vendor document not re-read | B and C′ credit design | C′-R6 flow test |
| Anguizola2018 acid off-rate; residual particle fraction r_b | k_d 0.17–0.37 s⁻¹; no number | C′ carry-over | C′-R1 |
| Empower Toolkit sample-set insertion | — | post-high blank-check mode A | Waters question (docs/02 Q5) |
| Micrux die geometry, pad layout, price | catalogue; "price on request" | M5a build | quote (docs/07 §8) |
