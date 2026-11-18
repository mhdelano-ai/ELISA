# scripts/tier_round — calculation kit and design scripts of the three-tier round (docs/26–32)

| File | Content |
|---|---|
| `tierkit.py` | the kit: capture on the electrode of a wall-jet or channel cell, product transport in the stopped thin layer, bed formats, blank statistics, Monte Carlo |
| `tier_params.yaml` | parameters added by this round (namespace `tr.`), schema of `params/*.yaml`; all UNVERIFIED unless a source is named |
| `designs.py` | geometry of the two MicruX cells (docs/28) and the design builders `tier1()`, `tier2()` and `tier3()` |
| `run_tiers.py` | the implementations of docs/30 (tier 1, tier 2, tier 3 with one valve, tier 3 with the transfer) with scenarios, alternatives, hardware cases and sensitivities → `results/tier_round/tiers.md`, `tiers.json` |
| `doc_tables.py` | prints the result tables of docs/30 from `tiers.json`; `--check` compares them with the document |
| `earlier_designs_halflife.py` | the designs of docs/05 in the audited model with the hydroquinone half-life of this round → `results/tier_round/earlier_designs_halflife.md` |
| `check_tierkit.py` | 36 checks of the kit against analytic limits, an independent derivation and the audited model → `results/tier_round/check_tierkit.md` |
| `crosscheck_model.py` | the kit's bed format run on the model's `B-bed-TL/alp_hqdp` inputs |
| `cell_geometries.py` | follow-up (docs/33): other flow-cell geometries put into the unchanged designs of `run_tiers.py` — gap of the radial cell, cross-flow channel with and without walls upstream of the electrode, adjustable confined wall jet, free wall jet, porous flow-through electrode, ideal bound; own solver for product released from a channel wall upstream of the electrode, with checks → `results/tier_round/cell_geometries.md`, `cell_geometries.json` |
| `review_numbers.py`, `review_chemistry_calc.py`, `review_feasibility_calc.py`, `review2_numbers.py`, `review2_consistency.py` | the reviewers' own calculations behind `results/tier_round/review_*.md` and `review2_*.md` (record; written against the first version and against Revision B of the designs, docs/31) |

```bash
pip install -e .                                   # the model package (elisa_sim)
python scripts/tier_round/check_tierkit.py         # 36 of 36 checks pass; exits non-zero otherwise (about 1 min)
python scripts/tier_round/run_tiers.py             # Monte Carlo n = 2000, seed 20261111 (about 2 min)
python scripts/tier_round/doc_tables.py --check    # the tables of docs/30 against tiers.json
python scripts/tier_round/cell_geometries.py       # docs/33: flow-cell geometries (about 4 min; --doc prints its tables)
```

The kit imports `elisa_sim` and changes nothing in `src/` or `params/`. Design choices (geometry, flows, times,
concentrations) are in the design dictionaries and are never sampled; uncertain quantities are parameters.
`run_tiers.py` gives one model parameter other bounds for this round without editing `params/`: the half-life of
hydroquinone at pH 9.5, 600 s [120–7200] instead of 7200 s (docs/31 C5).

The kit was revised after the independent review and again after the second pass (docs/31). The terms added are
marked "(review)" and "(second pass)" below.

## What the kit computes

`evaluate_planar(design, ps)` — tier 1. `evaluate_bed(design, ps)` — tiers 2 and 3. Both return a `TierResult` with
the calibration curve, blank mean and SD, LOD (blank + 3 SD through the curve), upper limit, the variance terms and
the intermediate quantities (molecules captured, enzymes, currents). `monte_carlo(evaluate, design, ps)` samples
every parameter the evaluation read, by the rules of `elisa_sim.params` (log-triangular for ranges ≥ 3×, else
triangular; design variables and pinned values fixed). `one_at_a_time` gives the LOD with each parameter at its
bounds.

### A. Delivery
Molecules leaving the loop = vial molecules × delivered fraction × (1 − adsorptive loss) × loop transfer
(`elisa_sim.transport.loop_transfer_interp`, β = D·V_loop/(Q·r²), flush volume = Q·t_load − transit volume).

### B. Capture on a reactive patch
*Channel cell.* `planar_flow_capture`: exact slit solution of the model (`transport.conversion("slit", ξ, Da)`,
one reactive wall, ξ = L·D·w/(Q·h), Da = k_r·h/D, k_r = k_on × active site density) for the lane of the stream above
the patch. A disc is taken as a square of equal area: the Lévêque flux to a disc is ∫(chord)^(2/3) dy =
2^(2/3)·B(1/2, 4/3)·a^(5/3) = 2.671 a^(5/3) against π^(5/6) a^(5/3) = 2.596 a^(5/3) for the square, a ratio of 1.03
(check B6).

*Wall-jet cell with a thin gap* (both MicruX flow add-ons, docs/28). The stream enters through the bore above the
electrode centre and leaves radially through the gap h. For creeping parabolic flow the mean radial velocity is
Q/(2πrh), and with the swept area s = π(r² − r₀²) the convection–diffusion equation
u(r, y)·∂c/∂r = D·∂²c/∂y² becomes (Q/h)·6η(1−η)·∂c/∂s = D·∂²c/∂y², which is the slit equation with w·x replaced by
s. `cell_conversion` therefore uses the slit solution with ξ = D·s/(Q·h): **all of the stream passes over a centred
electrode**, and no lane factor applies. The stagnation zone under the bore (r < r₀) is not counted. Independent
check (R1): Lighthill's solution for a thin boundary layer with wall shear β(r) = 3Q/(πrh²) on an axisymmetric
surface, j(r) = D·c·√(β r) / [Γ(4/3)·(9D∫√β·r^(3/2) dr)^(1/3)], integrates to
3.147·c·D^(2/3)·Q^(1/3)·h^(−2/3)·(a² − r₀²)^(2/3); the kit agrees within 1.2 %.
Validity: gap much smaller than the electrode radius; laminar; radial diffusion neglected.

### C. Capture in a stopped slab
`slab_capture_fraction`: Crank, *The Mathematics of Diffusion*, eq. 4.53 (plane sheet with surface evaporation),
roots of β·tanβ = Bi = k_r·h/D. Used for stop-and-go loading (`sample.mode = 'stop_go'`), which is not used in
the designs: slow continuous flow passes the whole sample over the electrode in the time available.

### D. Bed
Film coefficient by Wilson–Geankoplis as in the model, in series with k_r; captured fraction 1 − exp(−k·A/Q);
pressure drop by Kozeny–Carman (`kozeny_carman_dp`).

### E. Labelling and non-specific label
Exposure integral of the conjugate plug = C·V/Q (exact for any dispersion) + C·dilution·t_stop. Labelled fraction
by pseudo-first-order binding at the mean concentration over the exposure time, then dissociation of label and of
analyte until the middle of the read. Non-specific label on each surface = k_nsb × label factor × surface factor ×
area × exposure. Surfaces: electrode, floor around it, lid (planar); bed, retainer, inlet-bore wall below the bed
(bed). (review) Walls upstream of the electrode or bed that saw the conjugate are counted as well: the inlet bore
and the transfer line in the planar format (`design["upstream"]`), the capillary above the bed and the transfer
line in the bed format (`bed["upstream_area"]`).

### F. Immune-complex transfer (tier 3) (review; second pass)
`design["transfer"]`: specific label × released fraction (`tr.transfer.elution_efficiency`, 0.35 [0.05–0.74],
UNVERIFIED) × re-captured fraction on the read bed; non-specific label of the first bed, its retainer and its loop
× the lever of docs/05 (`ma.design_levers.immune_complex_transfer_nsb_factor`, UNVERIFIED).
Re-capture (second pass): every capture antibody carries the tag, so the read bed has to take all that is
released. A fixed bed with N = k·A₂/Q transfer units (the bed equation of D at the push flow, with the diffusion
coefficient of the conjugate) and a feed of τ = (released antibody)/(sites) lets the fraction
ln(e^{N(τ−1)} + 1 − e^{−N}) / (N·τ) escape (Bohart–Adams; it tends to e^{−N} for τ → 0). `bed2_factor` is the size
of the read bed relative to the capture bed (3 in the design), `coat` the antibody load of the capture bed relative
to the model's monolayer density. The formula reproduces the second reviewer's 200-slice simulation (0.83 at
τ = 1/1.22, 0.36 at τ = 1/0.36).

### F2. Free product of the working substrate solution (second pass)
`_free_product`: with `tr.detection.reservoir_background_decays` = 1 the product half-life holds in the substrate
reservoir as it does in the bed. The lot's impurity decays over the reservoir age, and the hydrolysis product
stands at k_hyd·S₀·(1 − e^{−kt})/k. With 0 the impurity is `free_product_impurity` × S₀ at the time of use and the
hydrolysis product is k_hyd·S₀·t, as in the audited model; `run_tiers.py` carries this as the scenario "no decay"
and `crosscheck_model.py` sets it.

### G. Product transport and the electrode
`ThinLayer`: backward-Euler finite volumes for diffusion in the stopped liquid disc (radius R, height h) over an
electrode disc of radius a, with the inlet bore as part of the liquid. The electrode is "on" (zero concentration:
transport-limited potential) or "off". Sources of unit strength (on the electrode, on the floor ring, on the lid,
in the volume, or an initial uniform concentration) are run separately and superposed. Checks G1–G9 and R2–R3: mass
balance to 10⁻⁹, exhaustive thin-layer electrolysis, time lag h²/2D, surface concentration under a floor source,
Cottrell flux (4 % high at 2 s: backward Euler and edge diffusion), grid convergence 1.2 %.

Read modes of the planar format:
* `steady_flow` — electrode held at potential while substrate flows: enzyme on the electrode is collected in full
  (the product forms at the sink); the floor ring is downstream and contributes nothing; product formed on the lid
  above the electrode is counted at half the inlet-stream conversion (an upper estimate, docs/31 N10); the impurity
  arrives with the stream (nF·η·Q·c). (review) Product of the conjugate on the inlet bore and the transfer line
  arrives mixed into the stream and is collected at the stream conversion η; for the bore wall this is an upper
  estimate, because its product enters the gap along the lid (docs/31 M6). (second pass) `read.buffer_step_A`:
  difference in background current between the reference liquid and the substrate buffer when the two are not
  matched; it is carried over by the pre-run like the substrate background. `electrode.collection_key`: fraction of
  the transport-limited current a coated electrode delivers, a lumped factor on every current through it.
* `steady` — the same in the stopped cell: the impurity above the electrode is electrolysed away, product from the
  floor ring and the lid diffuses in (kernels of `ThinLayer`). (review) Product formed on the wall of the inlet bore
  diffuses out of the bore onto the electrode (`ThinLayer.source_bore_wall`); the transfer line does not count.
* `accumulate_step` — electrode off, then stepped on; carries a step background charge (`tr.detection.step_*`).
* `cycling` — a reductant regenerates the product in solution; total product is conserved and the current is
  nF·A·c_surface·√(D·k)·tanh(h/μ), μ = √(D/k) (checked against a 1-D reaction–diffusion solution, G12). Unverified on
  the MicruX electrode materials (docs/29 A.2).
* `ida` — interdigitated array, Aoki steady-state current of the model, optional one-channel efficiency.

Read modes of the bed format: `swept` (plug swept over the electrode: charge = nF × product × cell conversion ×
eluted fraction; the cell's own non-specific enzyme gives a steady baseline that the baseline windows remove;
(review) product of the upstream walls that stood in substrate during the stop follows the plug and is counted in
full; with `read.baseline_step` the impurity current is absent before the peak and present after it, and the part
of that step left after subtracting the pre-run trace is `tr.noise.swept_step_residual_cv` × the impurity charge;
(second pass) with `read.V_transit_uL` the peak has a laminar tail: of a thin slab the fraction (V_t/2V)² has not
arrived after the volume V; with `read.count_sweep_production` the enzymes keep working in fresh substrate during
the sweep and what they make before T − V_t/Q arrives in the window; with `read.count_steady` the steady currents of
conjugate on the electrode and on walls that stay in flowing substrate enter the background, so that their relative
noise counts while their mean is removed by the baseline. Without these keys the swept read is that of the audited
model, which the cross-check uses),
`parked` (plug stopped over the electrode; the cell's own non-specific enzyme counts), `continuous` (no stop:
steady current of the bed's turnover; enzyme on the electrode and the lid counts).

### I. Blank statistics
As docs/03 §3.6 (`elisa_sim.model.evaluate`), with two additions for single-use consumables: a unit-to-unit CV of
the non-specific label (`tr.nsb.unit_to_unit_cv_planar`, `_bed`) added in quadrature to the model's blank CV, and
the sensor-to-sensor CV of printed or thin-film electrodes, replaced by `tr.noise.preread_residual_cv` when the
design reads the substrate background on the same electrode before the sample. Baseline drift is scaled with
electrode area (`tr.noise.drift_area_exponent`, 0.5 [0–1]; 0 reproduces the model). (review) The unremoved drift is
f_res × drift × T_span / 2 integrated over the read window, where T_span is the time between the centres of the two
reference windows that bracket the read (`read.t_span_s`; the read window itself if not given, as in the model).
With `read.reference_far` the substrate background comes from a pre-run read before the sample, and
`tr.noise.preread_residual_cv` × (impurity + hydrolysis charge) is added to the substrate-background term.

## Cross-check with the audited model
`crosscheck_model.py` gives the kit the geometry, flows and times of `B-bed-TL/alp_hqdp` and switches off what the
model does not have (unit-to-unit term, area-scaled drift, fresh bed). Captured fraction, enzymes at 1 pg/mL and
signal at 1 pg/mL agree to 10⁻⁹; LOD 19.9 against 19.4 pg/mL (the kit counts the carry-over uptake on the bed only).

## Limits
* Geometry of the MicruX cells is from brochures; the gap height and the bore length are not published (docs/28).
  `run_tiers.py` runs the gap at its bounds; the bore is taken as 5 mm long.
* The wall-jet mapping (B) is exact for lubrication flow with radial diffusion neglected. Check R1 compares two
  forms of that same assumption and does not test it. The assumption is fair for the strip cell (annulus 1.1 mm
  against a 0.2 mm gap) and marginal for the thin-film cell (0.25 mm against 0.16 mm). The stagnation disc under the
  bore is left out, which understates capture and collection by 0–30 % in the thin-film cell (docs/31 N9).
* The diffusion coefficient of the product is held at its best estimate inside the thin-layer kernels and in the
  cell conversion; the age of the substrate reservoir is fixed at 4 h; the analyte diffusion coefficient is fixed
  (docs/31 N12).
* The swept read takes its baseline from the 30 s before the sweep (end of the stop, or before the valve opens).
  In tier 2 the walls above the bed go from stopped to flowing at the sweep; their product is counted in full as
  blank. Product that diffuses from the bed to the electrode during the stop (at most 5 %, Derived by the second
  reviewer) is not counted, in signal and blank alike.
* In tier 3 the substrate standing in the closed loop loses part of its free product during the accumulation; the
  dip this leaves in the baseline when the valve opens is not modelled (it is systematic, and absent when the
  reservoir background has decayed).
* Wash efficiency, bed channelling, protein fouling of the electrode and temperature are not modelled.
* The release step of the immune-complex transfer and the non-specific label that comes along are bounded
  parameters (UNVERIFIED), not physics; only the re-capture is computed. The site density and valency of the read
  bed are taken as those of the capture bed.
* Design inputs that are uncertain but not sampled: cell gap, bore length, frit area, loop walls, the volume
  between bed and electrode, the transit volume. `run_tiers.py` shows them as cases.
* Every turnover of the enzyme is counted as one hydroquinone (two electrons). docs/31 C1 questions this for
  hydroquinone diphosphate; `run_tiers.py` carries the scenario "1 % of the turnovers give an electroactive
  product".
