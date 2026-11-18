# Review of docs/30 — lens: numbers and physics

Reviewer: independent review task of the tier round, 2026-11-17. Inputs read: docs/26, docs/30 (all), docs/27 §1–2,
`scripts/tier_round/` (README, tierkit.py, designs.py, run_tiers.py, tier_params.yaml), `results/tier_round/tiers.md`,
`tiers.json`, the relevant parts of `params/*.yaml` and `src/elisa_sim/model.py`. My own script:
`scripts/tier_round/review_numbers.py` (part A recomputes the tier 1 and tier 2 chains from the raw YAML with its own slit
solver, without tierkit or elisa_sim; part B, `--kit`, runs the kit with alternative defaults and prints the sampled
keys). Evidence labels: [V] checked in this session, Derived = my calculation, UNVERIFIED = not checked.

## Verdict

The kit reproduces exactly: `check_tierkit.py` passes 36 of 36. `run_tiers.py` writes back byte-identical `tiers.md` and
`tiers.json`. My independent recomputation matches the nominal chains of tiers 1 and 2 to within 1 % (tier 1 LOD 3.13
vs 3.13 pg/mL, tier 2 0.755 vs 0.753 pg/mL). Every number in the docs/30 tables matches the outputs, apart from a few
wording slips. **The numbers are faithful to the kit, but the kit leaves out physics that sets the blank in tiers 1 and
2, so their nominal LODs are too low.**
* Tier 1 has no reference window next to its read (its reference is the pre-read about 55 min earlier). It also counts
  none of the conjugate that sticks to the inlet bore and the transfer tubing, though product from those walls flows
  straight onto the electrode. The audited model counts those walls in its Scheme A. With these corrected, tier 1 is
  about 30–75 pg/mL as written, not 3.1.
* Tier 2 stops the flow for 7 min. During the stop, product also builds up on every wall upstream of the bed that saw
  conjugate, and the 90 s sweep carries that product straight behind the bed's plug. Its "steady baseline" is also not
  steady: the impurity current steps from about 0 to 100 pA just as the peak arrives.
* My corrected nominal LODs are about 30–75 (tier 1 as written; about 7 if redesigned), 1.3–3.2 (tier 2) and 0.5–1.6
  (tier 3) pg/mL. The order tier 3 < tier 2 < tier 1 still holds. Tier 1 drops out as a below-5 pg/mL candidate unless
  it is redesigned.

## Findings (most severe first)

### N1 — blocking — Tier 1's only reference window is the pre-read, about 55 min before the read; the drift term ignores this
*Place:* docs/30 §3.1 (Read row: "reference window: the same read on the same chip before the sample"), §3.3, §3.4;
`tierkit._noise` and `_finish`.
*Evidence:* The kit's drift variance is `(f_res · ½ · drift · T_read²)²`. `ma.noise.drift_residual_fraction` (0.2) is
defined as "fraction of the baseline drift not removed by interpolating the baseline before/after the readout window"
(params/model_assumptions.yaml). Tier 1 has no window before or after its read: the enzyme starts producing as soon as
the substrate arrives (step to substrate 46.5–48 min, read 49–53 min). The reference window is the pre-read, taken before
Inject Start, so its midpoint lies about 55 min before the read's midpoint. In between, a protein sample and a conjugate
cross the electrode, the buffer changes A1 → B1 → A1 → B1, and the potential is held throughout.
Using the kit's own drift (0.55 pA/min after area scaling) and its own 20 % unpredictable fraction: the offset is
0.2 × 0.555 pA/min × 55 min = 6.1 pA, or 1.47 nC over 240 s, against 64 pC per pg/mL. The LOD from this term alone
is 68.6 pg/mL (Derived, `review_numbers.py`). With only 5 % unpredictable it is 17 pg/mL. The kit's 3.1 pg/mL
(drift = 63 % of the variance) holds only for a reference window next to the read, and the design has none.
*Fix:* add a reference window next to the read and use the pre-read only for the impurity. Two ways:
* Four windows: read (substrate) minus an adjacent window in buffer A1, minus (pre-read in substrate minus pre-read in
  buffer). This adds about 3–4 min, giving about 57 min.
* A two-flow read at 1 and 3 µL/min. The enzyme current on the electrode does not depend on flow; the stream-borne
  impurity scales with Q^(1/3).

In the kit, either give `_noise` the time between windows (Δt) for a referenced read, or drop the "referenced" status
of the drift for `steady_flow`. Restate the tier 1 LOD.

### N2 — blocking — Tier 1 ignores the conjugate on the inlet bore and the transfer tubing, though product from both flows straight onto the electrode
*Place:* docs/30 §1 item 4 ("conjugate stuck to the lid and to the chip … washed downstream and does not count"),
§3.1, §3.4; `tierkit.evaluate_planar` (non-specific surfaces = electrode, floor, lid only).
*Evidence:* In the `steady_flow` read, every surface upstream of the electrode that saw conjugate makes product, and the
stream carries that product onto the electrode. The audited model counts this. `elisa_sim/model.py` (Scheme A):
"every surface between injector and cell that saw the conjugate keeps producing product", with area
π·ID·(injector→reactor + reactor→cell) × `ma.nsb.surface_factor_tubing` (3). The tier kit drops the term.

Derived, with the kit's own non-specific density (1157 enzymes/mm² at surface factor 1 for 20 nM·min) and its collection
η = 0.447 at 1 µL/min:

| Surface | Area | Enzymes | Current in the read | Blank equivalent | LOD with this term |
|---|---|---|---|---|---|
| Electrode itself (kit) | 0.785 mm² × 3 | 2.7×10³ | 0.76 pA (with lid) | 2.9 pg/mL | 3.1 pg/mL |
| Inlet bore, 0.5 mm × 5 mm (designs.py TF_CELL), lid factor 3 | 7.85 mm² | 2.7×10⁴ | 2.9 pA | 10.9 pg/mL | 6.7 pg/mL (CV 18 %) |
| Transfer tubing, 0.127 mm × 0.2 m (docs/30 §2.3), factor 3 | 80 mm² | 2.8×10⁵ | 26 pA (mean over the read; rises as the 2.5 µL tubing fills) | 99 pg/mL | 30 pg/mL (CV 10 %); 59 pg/mL (CV 20 %) |
| 100 µL loop, 0.5 mm ID, if still in line ("in line from Inject Start to Loop Offline", docs/27 §1) | 800 mm² | about 10× the tubing | rises like drift for about 100 min at 1 µL/min | — | — |

The tubing also builds up conjugate from one determination to the next, because only the chip is replaced.
*Fix:* add an upstream-wall term to `evaluate_planar`: bore wall plus tubing (plus loop, unless Loop Offline is set
before the conjugate). Its collection is η, and it builds over the tubing transit time. The design then needs:
* a minimal path from injector to cell (for example 2 cm of 0.0635 mm ID: 4 mm² instead of 80 mm²);
* Loop Offline set before the conjugate reaches the cell;
* a stated bore length.

With the bore term, the tubing removed and the reference of N1 fixed, tier 1 is about 7 pg/mL nominal (Derived).
Restate §0, §3.4, §3.5 and §6.

### N3 — significant (borderline blocking) — Tier 2: product made in the stopped walls upstream of the bed is swept onto the electrode right behind the plug
*Place:* docs/30 §4.1 ("Why at the tip. Every surface between the bed and the electrode … only the frit does"), §4.4;
`evaluate_bed` (no upstream term when `bore_wall=False`).
*Evidence:* The conjugate passes through the loop, the 0.127 mm transfer line and the fritted capillary before it
reaches the beads. All of these stand still with substrate for the same 7 min as the bed.
* Enzyme per volume (Derived; kit density 867 enzymes/mm², tubing factor 3): bed plug 6.0×10⁵/µL, 0.2 mm capillary
  5.2×10⁴/µL, 0.127 mm PEEK 8.2×10⁴/µL. Upstream liquid therefore carries 9–14 % of the plug's blank concentration.
* The read sweeps 7.5 µL in 90 s, while the plug is 0.11 µL dispersed to about 3.5 µL (σ = 1 µL in the kit). The
  upstream product therefore arrives as a plateau that joins the peak with no gap and lasts past the end of the window.
* A straight baseline from "before" to "after" leaves about half the plateau under the peak. That is 1.4× the bed's own
  blank (assuming 30 mm of capillary, UNVERIFIED), and LOD 0.75 → 1.27 pg/mL. With no removal (capillary + PEEK inside
  the window) it is 4.0×, and LOD → 3.0 pg/mL.

docs/30 counts the walls between bed and electrode but forgets that the walls above the bed make product too.
*Fix:* add the upstream wall product as a blank term. Shorten and narrow the path above the bed. Read a shorter window,
and fit plug and plateau with separate shapes. Move the stop to a valve on the bed (tier 3 already does this; the
cheapest version is one valve). Measure it in T2-1, comparing a bed-less capillary with the full path, both stopped
7 min.

### N4 — significant — The swept read's "steady baseline" is not steady: the impurity current steps from about 0 to 100 pA as the peak arrives
*Place:* docs/30 §4.1 ("Swept, the strip's own conjugate gives a steady current that is the same before and after the
peak"), README "Read modes of the bed format"; `evaluate_bed` swept branch (`Q_imp … steady baseline, referenced`,
residual 1 %).
*Evidence:* The electrode is held at potential during the stop, so the stopped thin layer over it loses its free
hydroquinone. Product from the floor ring and the lid diffuses in (√(2Dt) ≈ 0.9 mm in 7 min). At the sweep, fresh
substrate with 10⁻⁵ free hydroquinone brings nF·η·Q·c = 100 pA (Derived: η 0.62, 5 µL/min, 10 nM). The blank peak
averages 52 pA over 90 s. So the baseline "before" (stopped, depleted, plus diffused floor and lid product) and the
baseline "after" (100 pA of impurity plus the electrode's own non-specific current) differ by more than the blank peak,
and the step rises on the same time scale as the peak.
Kit cost of a 5 % residual instead of 1 %: tier 2 0.75 → 0.89 pg/mL; tier 3 0.33 → 1.12 pg/mL (tier 3 is
substrate-limited; its cell is isolated by V2 during the accumulation, so it has the same step).
*Fix:* model the read as a step plus a peak. Raise `ma.noise.background_current_relative_noise` to 3–5 % for swept reads
until T2-2 shows the baseline shape. Better, let substrate flow over the electrode during the stop (only possible in
tier 3, by a bypass to the cell) so that the baseline really is steady.

### N5 — significant — The bed is given the bead factor (1), not the model's packed-bed factor (3)
*Place:* run_tiers.py `t2()` (`bed_factor_key=MB`); docs/30 §4.1 "Why beads of 2.8 µm … surface factor 1".
*Evidence:* `ma.nsb.surface_factor_magnetic_beads` = 1 is defined on blocked beads washed in tubes (Rissin2010, per the
YAML source). `ma.nsb.surface_factor_packed_bed` = 3 [1–30] is the model's value for "non-porous 5–50 µm capture beads
in a column". The tier 2 bed is a packed column of beads that is washed only by through-flow; dead zones at the frit and
the wall are not washed the way a tube is.
Kit: tier 2 0.75 → 1.25 pg/mL; tier 3 0.33 → 0.40 pg/mL.
*Fix:* use the packed-bed factor as nominal, or sample the bead factor over [1–30]. T2-1 decides.

### N6 — significant — Tier 3's transfer efficiency of 0.7 sits at the limit the kit's own bed physics allows; 0.9 is beyond it
*Place:* docs/30 §5.1 (transfer ×0.7, 0.4–0.9), §5.3; `ma.design_levers.immune_complex_transfer_efficiency`.
*Evidence:* With the same bed physics as tier 2 (k_r = 4.2×10⁻⁶ m/s, 24 mm², film coefficient ≫ k_r), re-capture alone
on a 1×10⁶-bead bed 2 at the stated push rate of 5 µL/min is 1 − exp(−k·A/Q) = 0.70 (Derived). This is optimistic,
because the eluted complex (IgG + F(ab′)₂ + conjugate) diffuses more slowly than IgG. The nominal 0.7 therefore
requires 100 % elution from bed 1 in a 5 min biotin hold. The upper bound 0.9 cannot be reached at 5 µL/min.
Hirsch2002 (PMID 12419349, [10.1016/s0003-2697(02)00201-4](https://doi.org/10.1016/s0003-2697(02)00201-4), abstract [V])
says only that desthiobiotin is "easily displaced by biotin"; it gives no rate.
At 0.49 (70 % elution × 70 % re-capture) tier 3 is 0.47 nominal, median 1.85 pg/mL.
*Fix:* write the transfer as elution × re-capture, compute re-capture from the bed physics at the push rate (or push at
2 µL/min: 0.95 re-capture, but 2.5 min more), and bound elution by T3-1. Restate 0.33 as about 0.45–0.5.

### N7 — significant — The most favourable drift scaling is the mode of the distribution
*Place:* tier_params.yaml `tr.noise.drift_area_exponent` (value 1, range 0–1); docs/30 §6.2.
*Evidence:* The drift is scaled by (A/7.07 mm²)^1. For the 1 mm disc this cuts the drift 9-fold. Part of the drift does
not scale with area: the gold pseudo-reference, temperature, and the potentiostat offset. At exponent 0.5 the kit gives
7.7 pg/mL (median 17.7); at 0 it gives 22.5. The best case is the nominal and the mode of the triangular draw. The tier 1
recommendation over the printed gold strip (§3.5, "equal medians") rests on it.
*Fix:* nominal 0.5, range 0–1. Decide by T1-1 (drift of 1 mm and 3 mm electrodes side by side).

### N8 — significant — Tier 2's "upper limit 460 pg/mL" and "2.8 decades" come from a different design
*Place:* docs/30 §4.4 Range.
*Evidence:* The 460 pg/mL is the ULOQ of the separate case "short accumulation of 30 s" (tiers.md §4: LOD 1.8, 51.5 min).
That case has a fresh bed and its own timing. A second stop after the first sweep has 1.5–2.5 min more label
dissociation and a shortened load (33.5 min). Neither is computed. With the long stop alone the range is 1.9 decades
(0.75–54), below the two decades docs/26 §3 asks for.
*Fix:* model the second read as a continuation of the first (label clock and load time), and report its LOD and ULOQ.
State plainly that the primary falls short of two decades.

### N9 — minor — Capture in the wall-jet cell: the slit mapping is exact, but its conditions hold only marginally, and the stagnation disc is dropped
*Place:* README B; `cell_conversion`; docs/30 §1 item 2.
*Evidence:* I derived it myself: u = (Q/2πrh)·6η(1−η) and s = π(r² − r₀²) give (Q/h)·6η(1−η)·∂c/∂s = D·∂²c/∂y². This
is the slit equation, exact for lubrication flow with radial diffusion neglected. The conditions:
* Creeping flow: Re_h = Q/(2πrν) at r = 0.25 mm is 0.04 at 3.25 µL/min and 0.95 at 80 µL/min. Creeping is fair for
  loading and the read, marginal for the washes.
* Thin gap: the gap must be small compared with the annulus width, and here it is not. Tier 1: annulus 0.25 mm vs gap
  0.16 mm. Tier 2: 1.1 mm vs 0.2 mm, which is fine.

My marching solver reproduces the kit's capture to within 0.1 % (f = 0.01756 of what reaches the cell). It meets
Lévêque within 1.5 % at ξ = 10⁻³.
Two effects work in opposite directions:
* The disc under the bore (25 % of the 1 mm electrode, 7 % of the 3 mm one) is an impinging-jet stagnation zone with
  good mass transfer. Leaving it out understates capture and collection by up to 1.33× in tier 1. It also understates the
  impurity current that N1 and N4 deal with.
* Near r₀ the wall shear departs from the lubrication value over about one gap height (±30 % in shear, ±10 % in
  capture).

Net: conservative by 0–30 % for tier 1. The README's 1.2 % check (R1) compares two forms of the same lubrication
assumption; it does not test that assumption.
*Fix:* say so in the README. Bound the stagnation zone (count it at the annulus mean as an upper case).

### N10 — minor — The lid rule in `steady_flow` overcounts; the floor-ring rule is sound
*Evidence:* At 1 µL/min the radial transit over the annulus (r 0.25 → 0.5 mm, 0.16 mm gap) takes 5.6 s, against
h²/D = 28 s to cross the gap. Lid-born product therefore reaches the electrode with much less than half the stream
conversion. "0.5 η" is an overestimate, but the lid adds only 0.46×10³ of 3.2×10³ blank enzymes, so the effect on the
LOD is < 10 %.
The floor ring is downstream: the upstream diffusion length D/u ≈ 30 µm at r = a, so it contributes nothing. That holds.
*Fix:* none needed. Say "upper estimate".

### N11 — minor — Tier 1 impurity normalisation: 1 % residual after a pre-read 55 min earlier is optimistic
*Evidence:* The impurity current (4.3 pA, 76 % of the blank current) scales with the electrode's collection. That
collection changes after protein adsorption, and with flow accuracy at 1 µL/min, which is not specified (docs/27 §2).
Kit: a 5 % residual gives 4.1 pg/mL (3 %: 3.5). The `preread_residual_cv` of 3 % replaces a 5 % sensor CV but applies
only to the non-specific and hydrolysis charge, which hardly matters (0.10 → 3.5 pg/mL).
*Fix:* nominal residual 3 % [1–10 %] for a reference taken 55 min earlier.

### N12 — minor — Optimistic or unstated defaults (each run in the kit, nominal LOD)

| Default | Alternative | Effect |
|---|---|---|
| Retainer 5 mm² | 20 mm² (docs/30's own Derived frit estimate) | T2 0.75 → 2.34; with packed-bed factor 3: 2.88 |
| `unit_to_unit_cv_bed` 0.10 | 0.30 (its high bound) | T2 → 1.65 |
| `unit_to_unit_cv_planar` 0.15 | 0.30 | T1 → 3.84 |
| Thin-film gap 0.16 mm | 0.30 mm | T1 → 4.04 |
| `V_dead` 0.1 µL | 0.4 µL (tip 1 mm above the electrode, 0.2 mm gap → 0.8 mm of 0.8 mm bore below the tip) | T2 0.74: no effect on the LOD, but docs/30 §4.1 "0.1 µL between bed and electrode" does not match the stated geometry |
| Bore length 5 mm | not published | moves N2's bore term in proportion |

Not sampled or without effect in the Monte Carlo (wiring, printed by `review_numbers.py --kit`):
* `chem.substrates.HQ.diffusion_coefficient` is listed as sampled, but the kernels and η use the nominal value
  (`p.nominal`), so the draws have no effect.
* `ma.timing.substrate_reservoir_age` (1–12 h) is fixed at 4 h. It is a multiplier on the hydrolysis term, and the
  hydrolysis-rate high bound alone moves T1 to 42 pg/mL.
* `chem.analyte.diffusion_coefficient` is fixed (range 3.5–4.5×10⁻¹¹).
* `tr.nsb.surface_factor_glass_blocked` is sampled for tier 1 but has no effect (the floor counts zero in
  `steady_flow`).

No design choice is sampled. S0 = 0.3 mM is pinned in tier 1 (correct).
*Fix:* use the sampled D in η, and sample the reservoir age.

### N13 — minor — Text slips and mismatches
* §3.4 "1000 turnovers per second": the rate used is 750 s⁻¹ (0.3 mM, Km 0.1 mM). The number 0.27 pA is right.
* §6.3 "The order tier 3 < tier 2 < tier 1 holds in every row … except where the transfer fails": wrong for S4a (tier 3
  24 > tier 2 11 nominal; medians 41 > 22) and for the pessimistic transfer (1.6 > 0.75).
* §6.2 leaves out large swings: kon_detection (T1 11/1.5, T2 2.9/0.33, T3 1.3/0.15) and, for tier 1, hydrolysis rate
  (3.1/42).
* §1 item 2: "stop-and-go 1.42 % against 1.37 %; 4.5 % against 7.5 %" appears in no output of this round. README
  cites a "docs/30 §3.7" that does not exist.
* §3.4 and §1: "1.4 %" is of the vial; it is 1.76 % of what reaches the cell.
* §5.3: "about 1.7 for the valve-only bed after screening" is not computed.
* Tier 1's ULOQ (grid maximum, 10⁵) is not reported in docs/30, although docs/26 §5 asks for it.
* §3.5 lists the case "printed carbon, adsorbed streptavidin" but runs it with the streptavidin–biotin site factor (1.0),
  so capture is identical to printed gold.

*Fix:* correct the text.

## Checked and found sound
* **Reproduction.** `check_tierkit.py` passes 36 of 36. `run_tiers.py` output is byte-identical to the committed
  `tiers.md` and `tiers.json`. Every number in docs/30 §0, 3.4, 3.5, 4.4, 4.5, 5.3, 6.1 and 6.2 matches the outputs,
  except the items in N13.
* **Independent chains.** Tier 1: 4.01×10⁵ → 3.14×10⁵ → 5.52×10³ captured → labelled 0.357, label still bound 0.679,
  analyte still bound 0.833 → 1113 enzymes, 0.268 pA per pg/mL. Blank: non-specific 0.76 pA, impurity 4.31 pA,
  hydrolysis 0.62 pA (total 5.70 pA), 5.18 pg/mL equivalent. Variance: drift 63 %, non-specific 24 %. LOD 3.13 pg/mL.
* Tier 2: bed captures 0.824 of what reaches it (0.648 of the vial), 3.87×10⁴ enzymes, 2.30×10⁻¹⁴ mol, η 0.621,
  2.76 nC per pg/mL. Non-specific 6.45×10⁴ enzymes, blank 1.71 pg/mL equivalent, LOD 0.755. All within 1 % of the kit.
* **Capture kinetics (h).** k_r = 300 m³ mol⁻¹ s⁻¹ × 1.41×10⁻⁸ mol/m² = 4.2×10⁻⁶ m/s. The site density
  1×10¹⁶ m⁻² × 0.85 is below the M-280 capacity implied by about 10 µg biotinylated IgG per mg (≈ 2.5×10¹⁶ m⁻²; Derived
  from docs/07; bead count per mg UNVERIFIED). It is a fair upper value for an oriented SAM layer.
* **Saturation.** At 1000 pg/mL, occupancy is 0.07 % (tier 1) and 0.1 % (tier 2), so leaving saturation out is right.
* **Bed geometry and pressure.** 1×10⁶ × 2.8 µm beads give 24.4 mm², a 19 nL bed, 0.6 mm long; Kozeny–Carman gives
  1.1 bar at 3.5 µL/min. The bed is reaction-limited (k_m = 1.9×10⁻⁴ ≫ k_r).
* **Timing (e).** The step sums are 53 / 58 / 58 min. The label clock runs to mid-read in tier 1 and to the start of the
  stop in tiers 2 and 3 (defensible: label released during the stop stays in the stopped bed and keeps producing). The
  8 min transfer in tier 3 is charged (label retention 0.473).
* **Inhibition.** Phosphate inhibition (K_i 2 µM) in 0.11 µL limits the ULOQ to 54 pg/mL and is negligible at the blank
  (Pi ≈ 0.6 µM, rate −3 %).
* **Creep after the stop (d).** Restrictor 25 µm × 45 cm: R ≈ 4×10¹⁶ Pa s m⁻³, 560 bar at 80 µL/min. With
  about 150 µL of compliant volume, τ ≈ 3 s and the creep is a few µL. It is over before product builds up, so the peak's
  arrival time is the right test (T2-2). The pump volume is UNVERIFIED.

## What could not be checked
* The MicruX gap heights, bore lengths and wetted materials (not published; docs/28). Whether Loop Offline is set
  during the read, which decides whether the 800 mm² loop adds to N2.
* The real drift behaviour of a 1 mm gold disc against a gold pseudo-reference over 1 h (N1, N7). Needs T1-1 with a
  55 min gap between windows.
* The non-specific factors of PEEK, fused silica, PMMA and frits (all UNVERIFIED in params), which set N2, N3 and N5.
* Desthiobiotin elution kinetics in 5 min: Hirsch2002 abstract has no rate.
* The stagnation-zone mass transfer of a confined creeping jet with h/r₀ ≈ 0.6. Only bounded here, not solved.
* Free phosphate in commercial HQDP lots (with K_i 2 µM, 1 % phosphate in 1 mM HQDP would slow the enzyme by about 30 %).
  Not in the model.

## My corrected nominal estimates (Derived, `review_numbers.py`)

| Tier | docs/30 nominal / median | Reviewer's nominal | Basis | Reviewer's median (where the kit can express it) |
|---|---|---|---|---|
| 1 as written | 3.1 / 16 | **30–75** | N1 + N2 | — |
| 1 redesigned (adjacent reference, minimal tubing, bore counted) | — | about 7 | N2 bore + N11 | ≥ 18 (N7 alone) |
| 2 | 0.75 / 3.0 | **1.3–3.2** | N3 + N5 + N4 | ≥ 7.2 [0.85–109] (packed-bed factor + 5 % residual only, without N3) |
| 3 | 0.33 / 1.4 | **0.5–1.6** | N6 + N5 + N4 | 1.85 (N6 alone); 5.2 [0.54–240] (N4 + N5 + N6) |
