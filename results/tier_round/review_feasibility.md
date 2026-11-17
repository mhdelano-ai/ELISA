# Review of docs/30: instrument feasibility, binding constraints, consistency, tier 3

Reviewer: independent agent, 2026-11-17. Lens: feasibility on the Waters/Gamry/MicruX stack, the constraints of
docs/26 §3–4, consistency across docs/26–30 and `results/tier_round/tiers.md`, tier 3. Calculations:
`scripts/tier_round/review_feasibility_calc.py` (run with `--kit` for the kit cases; sections A–H below refer to its
output). Evidence labels: [V] opened in this session, Derived (formula or script named), UNVERIFIED.

## Verdict

None of the three designs breaks a binding constraint of docs/26 in principle: one 100 µL injection, sample-only
vial, no hands-on step after Inject Start, no protein through the pump. Pre-run steps are outside the 60 min under
docs/26 §3 ("Automated steps before the sample injection ... do not count toward the 60 min"). But all three step
tables are wrong at one point: the step from wash buffer to substrate. No table sets Loop Offline. With the 100 µL
loop still in line, the 100–160 µL of B1 programmed never reaches the electrode or bed (front at 0 %, section C).
docs/08 W4 already raised this for the earlier design. With Loop Offline, the same volumes deliver only 52–82 % B1,
so every table needs 1–2 min more. Tier 1 then takes about 55 min. Tier 2 takes about 59 min. Tier 3, rebuilt from
its own flows and volumes, takes about 61 min and has to shorten its load. Three smaller problems are separate:
(1) the pressure relaxation after the 80× flow steps is computed only for 1000 psi, but the stops start from
5000–8100 psi; (2) the transfer efficiency used for tier 3 (0.7 [0.4–0.9]) cannot be reached with the kit's own
single-pass re-capture at 5 µL/min (0.71 at 100 % elution); (3) the comparison with the docs/05 design is unfair:
it leaves out the docs/05 + L4 row (nominal 0.29, median 1.5, which equals tier 3), and it compares P values
defined by different criteria. The tier order 3 < 2 < 1 survives every change I made. The claim that tier 3 is
better than the docs/05 design does not.

## Findings (most severe first)

### F1 — blocking — No table sets Loop Offline, so the substrate never reaches the cell
*Place:* docs/30 §2.3 (flow path rules), §3.3, §4.3, §5.2 (the "step to substrate" rows); `designs.py` (`t_fill`).
*Evidence:* the delay volume from the BSM to the injector outlet is 85–110 µL with the loop offline. The loop adds
100 µL while it stays in line (docs/02 §1.1 and §2.4; docs/08 W4 l.324–325: "plus the 100 µL loop if it stays in
line ... Use Loop Offline"). In each tier the step to substrate sits inside the method of a line whose loop is in
line: line 2 (conjugate) in tiers 1 and 2, line 3 (eluent) in tier 3. docs/30 never mentions Loop Offline. Volumes
programmed: tier 1 = 80 µL/min × 1.5 min + 1 µL/min × 5 min = 125 µL; tier 2 = 50–80 µL/min × 2 min = 100–160 µL;
tier 3 = 50 µL/min × 2 min = 100 µL. Model used: plug, then the 50 µL mixer as one tank, plus 3.5 µL of tubing and
bore (section C):

| | loop in line | loop offline, dwell 85 µL | loop offline, dwell 110 µL |
|---|---|---|---|
| tier 1, 125 µL | 0.00 | 0.82 | 0.71 |
| tier 2, 100 µL (160 µL) | 0.00 (0–0.35) | 0.71 (0.91) | 0.52 (0.85) |
| tier 3, 100 µL | 0.00 | 0.71 | 0.52 |

What this does. With the loop in line, tier 1 reads in wash buffer at pH 7.5 with no HQDP, and tiers 2 and 3
accumulate in wash buffer: no signal. With the loop offline, tier 1 reads on a still-rising front while its
pre-read was made in full-strength B1. The 15–30 % mismatch in free-hydroquinone background is about 1 pA against a
0.8 pA signal at the LOD. The pH (and so the potential of the gold pseudo-reference and the hydroquinone wave) is
also between the two buffers. Tiers 2 and 3 accumulate at about pH 9 with 0.5–0.7 mM HQDP, and that composition
varies from run to run.
*Fix:* in every table, set Loop Offline in the line's SM-FL method once at least 2 loop volumes have passed after
the reagent: tier 1 at 46.5 min, tier 2 after the conjugate plus 100 µL of wash, tier 3 after the eluent has
reached bed 1. Program at least 215 µL of B1 (95 %; 295 µL for 99 %) at 80 µL/min, which is 2.7–3.7 min instead of
1.5–2 min. Measure the front with a dye or hydroquinone step (docs/27 §9 needs this item; it is not in the list).
Timing: tier 1 ≈ 55 min, tier 2 ≈ 59 min, tier 3 see F3. docs/02 §2.4 notes that the Loop Offline switch itself
disturbs the baseline [S WKB8852]. In tiers 1 and 2 the cell cannot be bypassed, so put the switch before the read
window and allow it at least 60 s to settle.

### F2 — significant — Pressure relaxation after the stops is computed for 1000 psi, but the stops start from 5000–8100 psi
*Place:* docs/27 §2 "Consequences" (1.3 µL, τ ≈ 8 s), docs/30 §3.3 (80 → 1 µL/min, 60 s settle), §4.3
(50–80 µL/min → 0), §4.6 T2-2.
*Evidence:* with the 25 µm × 45 cm restrictor the pump stands at 5050 psi at 50 µL/min and 8080 psi at 80 µL/min
(section A; Hagen–Poiseuille as in docs/27 §3, which I reproduced). The stored volume V·β·ΔP is 6.4–10.2 µL with
water-only compliance of 0.4 mL (τ = 7.7 s; section B). That is 60–100 times the tier-2 product plug (0.11 µL), and
it all passes through the bed in the first ~25 s of the "stop". Real compliance (pump seals, PEEK, mixer) is not
known. At 10× the water value, 64–102 µL creep over about 4 min (τ = 77 s). That fills 55 % of the 7 min
accumulation with flow, and in tier 1 the flow 60 s after the 80 → 1 µL/min step is still 37 µL/min, not 1.03. The
kit credits the full 420 s. At water-only compliance the loss is about 40 s (kit: 0.75 → 0.75 nominal, section H);
the risk is in the unknown compliance. On restart (0 → 5 µL/min, 505 psi, 0.6 µL to recompress) the top of the plug
is 0.1–0.5 µL from the electrode. It therefore arrives 1–6 s after flow resumes, while the flow and the convective
background are still ramping. No steady "baseline before the peak" (docs/30 §4.1, Read) exists.
*Fix:* before each stop, step down to the read flow (5 µL/min, ≤ 505 psi, ≤ 0.6 µL stored) for at least 60 s, and
count the accumulation from the end of that step. In tier 1, read only after the measured pressure has reached
1 µL/min × 100 psi. Add a creep-volume measurement to T2-2: a dye front position, or the pressure trace × measured
compliance. Define the tier-2 baseline from the end of the stop and the tail after the peak, not from "before the
peak". A cheaper alternative is a larger restrictor (40 µm kit, 12 psi per µL/min). It keeps all pressures below
1000 psi and the creep at about 1 µL, at the price of the check-valve back-pressure guidance (docs/27 §3), which is
a lifetime issue, not an accuracy issue [V K32564].

### F3 — significant — Tier 3 does not fit 58 min as described; its eluent "hold" contradicts "the pump never stops"
*Place:* docs/30 §0 ("the valve isolates the bed, the pump never stops"), §5.1 scheme ("eluent: V1 A, hold; then
V2 B"), §5.2 row 39.5–47.5, §6.1 ("Needs the pump to stop: no").
*Evidence:* with V1 in A and the pump running, liquid flows through bed 1, so nothing is held. The hold needs V1 in
B (bed 1 isolated, pump to waste through the V1 bypass and V2 A), or a 0 µL/min row, which tier 3 claims not to
need. Rebuilt from the stated flows (section G): line-3 overhead 1 min; eluent to bed 1 ~0.2 min; hold 5 min; push
~10 µL from bed 1 through two valves and tubing to bed 2 at 5 µL/min, 2 min; wash of bed 2 for at least 2 min
(docs/30 §2.3 rule, since the eluate carries released conjugate). That is 10.2 min against 8 min. Add the corrected
substrate step of F1 (2.5 min at 80 µL/min against 2 min) and the total is 60.7 min. A cut of the load from 29 to
27 min at 4.8 µL/min brings it back to 58.7 min at almost no cost (kit: 0.33 → 0.34 nominal; section H). Tier 3 also
needs three SM-FL lines, each with the 1 min overhead that docs/02 §2.2 marks UNVERIFIED (0.25–2 min). At 2 min per
line the margin is gone.
*Fix:* rewrite the eluent row as: V1 A to load the eluent, V1 B for the 5 min hold, then V1 A + V2 B for the push.
Rebuild the table from flows and volumes, shorten the load to 27 min, and measure the inter-line time
(docs/27 §9 item 3) before tier 3 is committed.

### F4 — significant — The transfer efficiency 0.7 [0.4–0.9] cannot be reached with the kit's own re-capture physics at 5 µL/min and 5 min elution
*Place:* docs/30 §5.1 (Transfer row), §5.3; `run_tiers.py` `t3()` (lever values from `ma.design_levers`).
*Evidence:* the lever was bounded for the tube protocol of docs/06 §4.12: 15 min elution, then 30 min re-capture
on beads. docs/30 uses 5 min elution and one flow-through pass. The kit's own bed equation
(f = 1 − exp(−k_r·A_bed/Q), k_r = 4.23×10⁻⁶ m/s, A_bed = 24.4 mm²) gives single-pass re-capture of 0.71 at
5 µL/min, 0.46 at 10 and 0.96 at 2 (section E). So 0.7 requires 99 % elution in 5 min, and the upper bound of 0.9
is out of reach. The source of the elution rate shows no rate: Hirsch2002 says only that desthiobiotin is "easily
displaced by biotin" ([V-abs], PubMed 12419349, https://doi.org/10.1016/s0003-2697(02)00201-4). The same abstract
says the complex dissociates under physiological conditions, so capture antibody also leaks from bed 1 during the
40 min before elution, a loss that is not modelled. In the kit, with efficiency = 0.71 × elution and bounds
[0.21–0.71]: elution 1.0 gives median 2.1 [0.36–82], P(≤ 1) 0.28; elution 0.8 gives nominal 0.41, median 2.2; 0.5
gives nominal 0.65, median 2.5, P 0.23. docs/30 reports median 1.4, P 0.38.
*Fix:* in the design, efficiency = elution(5 min) × f_recapture(Q_push), with f_recapture from the kit. Push at
1–2 µL/min (re-capture 0.96–1.00; +3–5 min, paid for by a shorter load). Make T3-1 a 5 min elution measured in a
bed, not in a tube, and add a leak-rate arm (desthiobiotin bed held 40 min in buffer).

### F5 — significant — The comparison of tier 3 with the docs/05 design is unfair, and the conclusion "the flow-through bed gains no LOD from a chamber" is not supported
*Place:* docs/30 §0 (third bullet of "Reading of the table"), §5.3 last paragraph, §8 choice 4; `run_tiers.py`
docstring.
*Evidence:* (a) docs/08 §10.1 [V, l.578–590] gives docs/05 primary + L4 as nominal 0.29, median 1.5 [0.28–70],
P 0.33, against tier 3 at 0.33, 1.4 [0.28–43], P 0.38. They are equal within Monte Carlo spread, and docs/30 does
not quote this row. (b) docs/30 compares "valve-only bed" 2.9 / "about 1.7" with docs/05 at 3.5 / 1.3. The "about
1.7" is tier 2's L6 + L7 median, not a valve-only result (none was run). By that comparison docs/05 is better after
screening (1.3 against 1.7) and better nominally as specified (0.60 against 0.71–0.75). (c) The P values are
defined differently: docs/08 uses the docs/05 L_eff criterion (docs/08 l.575: "Success = the docs/05 L_eff
criterion"), tiers.md uses P(LOD ≤ 1 pg/mL). "P 0.16" and "P 0.18" are therefore not comparable. (d) The models
differ too: the tier kit adds unit-to-unit CVs for hand-made consumables and has no reuse or carry-over term. The
`run_tiers.py` docstring says the audited model is run for "the earlier bead-chamber design read in the MicruX
cell", but `main()` never runs it.
*Fix:* run the docs/05 primary (and primary + L4) through the same kit with a fresh bead charge per determination
and the same success criterion, or say plainly that docs/05 + L4 and tier 3 are equal under the available numbers.
Drop "gains no LOD from a chamber". Remove the unused claim from the docstring.

### F6 — significant — "Valves only: an electrode that never sees conjugate" contradicts the tier-2 geometry argument
*Place:* docs/30 §5.1 ("What the valves alone give ... with an electrode that never sees conjugate"), tiers.md §5
"valves only" (0.71).
*Evidence:* without the transfer, the read bed is the capture bed. To keep conjugate off the electrode, a valve
must sit between that bed and the cell. That puts a valve rotor, ports and tubing (conjugate-exposed) between bed
and electrode, which is exactly what docs/30 §4.1 "Why at the tip" rejects (13 mm² of bore wall lifted the LOD
in the kit: "bed in a fitting" 0.72 with a 1 mm² screen, against 0.36 for the screen alone). The kit's valve-only
case is the tier-2 geometry with t_extra = 0. It models neither the valve in the path nor the electrode being free
of conjugate. Even with the transfer, the eluate (carrying released conjugate) passes bed 2 and the cell in V2 B.
*Fix:* model valve-only with the valve's wetted path between bed and electrode (and its accumulation volume), or
drop the claim. In tier 3 say that the electrode sees the eluate.

### F7 — significant — The potentiostat side is not specified, and the automation package cannot do it yet
*Place:* docs/30 §2.3 (Gamry holds the potential and records continuously); `automation/README.md`;
`automation/elisa_auto/gamry_worker.py`; `signal_proc.py`.
*Evidence:* the ToolkitPy backend is a stub ("Everything here is TODO", gamry_worker.py l.103–121 [V]). The
signal definition in the package is a least-squares line through pre- and post-windows (README "Signal and LOD
definitions" [V]). That fits tier 2's peak. It does not fit tier 1's "read minus a pre-read on the same chip an hour
earlier", which needs new code and a drift model across the gap. Current range is not stated in docs/30. Derived
magnitudes: in tier 2, the free-hydroquinone background at 5 µL/min is about nFcQ·η = 2 × 96485 × 1×10⁻⁵ mol m⁻³ ×
8.3×10⁻¹¹ m³ s⁻¹ × 0.62 ≈ 0.1 nA. The plug at 1 pg/mL (2.8 nC) passes in a few seconds, about 0.5–1 nA at the peak.
During the 80 µL/min B1 flush the background reaches several hundred pA. A 600 pA range would clip in tiers 2 and
3, and a 60 pA range would clip in tier 1 during flushes. Auto-ranging adds steps to the integrated charge (stub
note). An overload may also cost potential control and leave a recovery transient in the read. Holding the
potential for about 70 min (8 min pre-run + 55–60 min) on a gold pseudo-reference is expected to shift with pH
(A1 pH 7.5 → B1 pH 9.5) and chloride. F1 makes this worse, because the read is on a partial B1 front.
*Fix:* name one fixed range per tier for the whole record: 600 pA for tier 1 if the flush background is shown to
stay under it, otherwise 6 nA; 6 nA for tiers 2 and 3 (accuracy ±10 pA ± 0.05 % of range, a constant offset,
docs/02 §4 [V there]). Make any range change at a fixed time at least 60 s before a read window. Add the pre-read
reference to `signal_proc` before tier 1 is run. In T1-1, add a 70 min hold across an A1 → B1 → A1 → B1 sequence.

### F8 — minor — Tier 2 geometry: 0.5 µL, not 0.1 µL, between the capillary tip and the electrode
*Place:* docs/30 §4.1 (Position row), §4.4; `run_tiers.t2(V_dead_uL=0.1)`.
*Evidence:* the tip ends about 1 mm above the electrode inside a 0.8 mm bore [V docs/28 §1], so the column holds
π·0.4²·1.0 = 0.50 µL, and 2.5 mm² of PMMA bore wall below the tip is exposed to conjugate in the accumulation
volume. Kit with V_dead = 0.5 µL and the wall added as frit-equivalent area (2.5 mm² × lid factor 3 / frit factor
10): nominal 0.75 → 0.81, median 3.2 → 3.3 (section H, n = 600). In the 1-D diffusion estimate, 6 % of the
product reaches the electrode during the stop and 32 % sits below the tip (section D), so the read must integrate
from the start of the stop.
*Fix:* state 0.5 µL, or bring the tip to 0.2–0.3 mm above the electrode, which brings back about 0.1 µL. Include
the stop in the integration window.

### F9 — minor — Labels and table text that disagree
* tiers.md §7, tier 1: "flow stopped, electrode settles, impurity electrolysed 1.0 min". docs/30 §3.3 has B1 at
  1 µL/min (no stop). The label comes from `designs.py` and is wrong for the steady-flow read.
* docs/30 §1 item 2 "wall-jet cells with a thin gap (docs/28 §1 [V])": the wall jet is [V]. The gap is not
  published (docs/28: "use 0.1–0.5 mm (U)"), so "thin gap" is UNVERIFIED.
* docs/30 §8 item 6 takes the strip-cell gap as 0.2 mm "(the user's 10 µL)". docs/28 Derived gives h ≤ 0.1 mm from
  the vendor's < 5 µL. Both are inside docs/28's 0.1–0.5 mm, and tier 2 is insensitive to the gap (0.75/0.75/0.76).
  Harmless, but the reason given should match docs/28.
* docs/30 §4.1 "a bed three bead-layers per 10 µm long" is not meaningful. The bed is about 210 bead diameters long
  (0.6 mm / 2.8 µm).
* docs/30 §4.1 says the strip "can stay for a series". docs/26 §3 and docs/30 §2.4 define the blank SD on
  different consumables, and the tier-2 pre-run table says "mount bed and strip". With the strip reused, the
  strip-to-strip spread is not in the blanks, and conjugate builds up on the strip from run to run. Choose one.
*Fix:* correct the label in `designs.py`, the evidence labels and the sentences above.

### F10 — minor — The sampler: overfill, inter-line flow, flow-step programming
*Place:* docs/30 §2.3; docs/27 §4, A.3, A.8.
*Evidence:* the Waters default full-loop draw is 5× (500 µL) [V K198538 via docs/27 A.8]. The 2× setting
(200 µL) is UNVERIFIED. Either complies with docs/26 (the limit is on the injected volume), but the vial must hold
it plus dead volume. Flow between lines follows the next method's initial conditions only by "standard behaviour"
(UNVERIFIED, docs/27 A.3). In tiers 1 and 2 that flow runs through the capture surface or electrode, so a pre-run
or post-run method on the instrument could change the wash. Whether a BSM gradient row steps the flow
instantaneously, or follows the row's curve or a flow-ramp setting, is not stated anywhere in docs/27.
*Fix:* add to the docs/27 §9 checks: overfill setting, the flow logged between lines, and a flow-step test
(80 → 1 → 0 → 5 µL/min) with the pressure trace. Delete any Prerun/Postrun inlet methods (docs/27 A.3, K21855).

## Constraint check (docs/26 §3–4)

| | one injection ≤ 100 µL | ≤ 60 min (as written / after F1–F3) | sample-only vial | no hands-on after Inject Start | proteins not through pump | additions within tier |
|---|---|---|---|---|---|---|
| Tier 1 | yes (full loop) | 53 / ≈ 55 | yes | yes | yes (conjugate by SM-FL) | yes |
| Tier 2 | yes | 58 / ≈ 59–60 | yes | yes | yes | yes (frit capillary, sleeve: passive) |
| Tier 3 | yes (eluent is a reagent line) | 58 / ≈ 60.7 unless the load is cut | yes | yes | yes | yes |

Pre-run steps (mounting, cleaning injection, hydroquinone plug, pre-read) are outside the 60 min by the wording of
docs/26 §3, third bullet of "Relaxed". The tables count the aspiration of the sample line inside the 60 min, which
is conservative.

## Missed or under-examined designs

* **Tier 1 classification.** A frit in a union (an LC in-line filter) is arguably a "fitting". If the user counts
  it as one, the tier-2 bed (0.75 nominal) becomes a tier-1 design, against 3.1. Ask the user rather than decide
  silently.
* **Tier 2 without a frit.** I checked a bead plug held by a fixed magnet (allowed in tier 2) as a way to remove the
  retainer, which carries two thirds of the blank (4.3×10⁴ of 6.4×10⁴ enzymes). It fails: the bed's pressure drop
  puts 3.4 nN per bead at 3.5 µL/min and 77 nN at 80 µL/min on the plug (section F), against magnetic forces on an
  M-280 bead of the order of 0.01–0.1 nN (UNVERIFIED order of magnitude). The frit choice of docs/30 stands. The
  real lever is the retainer area (1 mm² → 0.36).
* **Tier 3.** The limiting term is the substrate background (44 % of variance). A pre-electrolysis guard electrode
  on B1, which a second channel allows, attacks exactly that term (kit sensitivity: impurity at 10⁻⁷ gives
  0.33 → 0.25 nominal). docs/30 does not list it. Under CLAUDE.md it waits for E1.2b, but it belongs among the
  runners-up. The docs/05 chamber design + L4 is equal (F5) and is the stronger fallback, because it does not need
  a 5 min elution.
* **Pump lines.** I found no clearly better use of A2/B2 inside a determination: a line change needs a pump-head
  and mixer flush (docs/27 §1).

## Checked and found sound

* Restrictor pressures of docs/27 §3 (Hagen–Poiseuille reproduced: 101 psi per µL/min). All flows stay below the
  18 000 psi limit even with a 23 µm bore (11 300 psi at 80 µL/min). The injector, bed and cell see only their own
  resistance, so loading the loop at 3–5 µL/min puts no load on the loop or valve.
* Bed geometry: 1×10⁶ × 2.8 µm beads = 11.5 nL of solid → 19 nL at ε 0.4 → 0.61 mm in a 0.2 mm bore; bead area
  24.6 mm²; Kozeny–Carman ΔP 1.1–1.3 bar at 3.5 µL/min, about 25 bar at 80 µL/min.
* Loaded volumes: tier 1 126.75 µL, tier 2 126 µL, tier 3 130.5 µL. All are about 1.2–1.3 loop volumes, ≥ 97 %
  out of the loop (docs/27 §4 table).
* Valve scheme of tier 3: realisable with two 2-position 6-port valves, each in "loop bypass" configuration. Inlet
  on port 1, outlet on port 2, bed (or bed 2 + cell) between ports 6 and 3, ports 4 and 5 plugged. Position
  (1-2)(3-4)(5-6) = bypass, loop closed; position (1-6)(2-3)(4-5) = through. The cell outlet must be plumbed back to
  V2 port 3, not to an open waste line. In no listed state is the pump dead-headed. "Pump keeps running to waste"
  during accumulation is consistent (V2 bypass to waste).
* Conjugate carry-over into the next determination: carried as `carryover²` with a cleaning injection between
  determinations. Carry-over of conjugate from the loop into the tier-3 eluent is negligible: about 1.8×10⁷
  molecules × the bed's non-specific uptake of 3.5×10⁻⁷ ≈ 6 enzymes.
* Tier order 3 < 2 < 1 holds in every case I ran.

## What could not be checked

* Whether the I-Class PLUS BSM accepts a 0.000 mL/min row and how flow steps are executed (ramp or curve). Whether
  "Automatic" Loop Offline (WKB221963, [S] in docs/02) takes the loop offline on its own, and when. The real
  inter-line time.
* The real fluidic compliance of the BSM path (it decides F2).
* The desthiobiotin–streptavidin dissociation rate under the tier-3 conditions (Hirsch2002 abstract gives no rate),
  and the existence of the phase-2 antibody.
* Current ranges in which the Reference 600+ stays in potential control on overload. The ToolkitPy API.
* The geometry of the MicruX add-ons (gap, bore length, outlet position): docs/28 §8 questions.
