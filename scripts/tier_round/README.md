# scripts/tier_round — calculation kit and design scripts of the three-tier round (docs/26–32)

| File | Content |
|---|---|
| `tierkit.py` | the kit: capture on the electrode of a wall-jet or channel cell, product transport in the stopped thin layer, bed formats, blank statistics, Monte Carlo |
| `tier_params.yaml` | parameters added by this round (namespace `tr.`), schema of `params/*.yaml`; all UNVERIFIED unless a source is named |
| `designs.py` | geometry of the two MicruX cells (docs/28) and the design builders `tier1()` and `tier2()` |
| `run_tiers.py` | the three implementations of docs/30 with scenarios, alternatives, hardware cases and sensitivities → `results/tier_round/tiers.md`, `tiers.json` |
| `check_tierkit.py` | 36 checks of the kit against analytic limits, an independent derivation and the audited model → `results/tier_round/check_tierkit.md` |
| `crosscheck_model.py` | the kit's bed format run on the model's `B-bed-TL/alp_hqdp` inputs |

```bash
pip install -e .                                   # the model package (elisa_sim)
python scripts/tier_round/check_tierkit.py         # 36 of 36 checks pass; exits non-zero otherwise (about 1 min)
python scripts/tier_round/run_tiers.py             # Monte Carlo n = 2000, seed 20261111 (about 1 min)
```

The kit imports `elisa_sim` and changes nothing in `src/` or `params/`. Design choices (geometry, flows, times,
concentrations) are in the design dictionaries and are never sampled; uncertain quantities are parameters.

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
roots of β·tanβ = Bi = k_r·h/D. Used for stop-and-go loading, which turns out no better than slow continuous flow
in these cells (docs/30 §3.7).

### D. Bed
Film coefficient by Wilson–Geankoplis as in the model, in series with k_r; captured fraction 1 − exp(−k·A/Q);
pressure drop by Kozeny–Carman (`kozeny_carman_dp`).

### E. Labelling and non-specific label
Exposure integral of the conjugate plug = C·V/Q (exact for any dispersion) + C·dilution·t_stop. Labelled fraction
by pseudo-first-order binding at the mean concentration over the exposure time, then dissociation of label and of
analyte until the middle of the read. Non-specific label on each surface = k_nsb × label factor × surface factor ×
area × exposure. Surfaces: electrode, floor around it, lid (planar); bed, retainer, inlet-bore wall (bed).

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
  above the electrode is counted at half the inlet-stream conversion (approximation); the impurity arrives with the
  stream (nF·η·Q·c).
* `steady` — the same in the stopped cell: the impurity above the electrode is electrolysed away, product from the
  floor ring and the lid diffuses in (kernels of `ThinLayer`).
* `accumulate_step` — electrode off, then stepped on; carries a step background charge (`tr.detection.step_*`).
* `cycling` — a reductant regenerates the product in solution; total product is conserved and the current is
  nF·A·c_surface·√(D·k)·tanh(h/μ), μ = √(D/k) (checked against a 1-D reaction–diffusion solution, G12). Unverified on
  the MicruX electrode materials (docs/29 A.2).
* `ida` — interdigitated array, Aoki steady-state current of the model, optional one-channel efficiency.

Read modes of the bed format: `swept` (plug swept over the electrode: charge = nF × product × cell conversion ×
eluted fraction; the cell's own non-specific enzyme gives a steady baseline that the baseline windows remove),
`parked` (plug stopped over the electrode; the cell's own non-specific enzyme counts), `continuous` (no stop:
steady current of the bed's turnover; enzyme on the electrode and the lid counts).

### I. Blank statistics
As docs/03 §3.6 (`elisa_sim.model.evaluate`), with two additions for single-use consumables: a unit-to-unit CV of
the non-specific label (`tr.nsb.unit_to_unit_cv_planar`, `_bed`) added in quadrature to the model's blank CV, and
the sensor-to-sensor CV of printed or thin-film electrodes, replaced by `tr.noise.preread_residual_cv` when the
design reads the substrate background on the same electrode before the sample. Baseline drift is scaled with
electrode area (`tr.noise.drift_area_exponent`; 0 reproduces the model).

## Cross-check with the audited model
`crosscheck_model.py` gives the kit the geometry, flows and times of `B-bed-TL/alp_hqdp` and switches off what the
model does not have (unit-to-unit term, area-scaled drift, fresh bed). Captured fraction, enzymes at 1 pg/mL and
signal at 1 pg/mL agree to 10⁻⁹; LOD 19.9 against 19.4 pg/mL (the kit counts the carry-over uptake on the bed only).

## Limits
* Geometry of the MicruX cells is from brochures; the gap height is not published (docs/28). `run_tiers.py` runs the
  gap at its bounds.
* The diffusion coefficient of the product is held at its best estimate inside the thin-layer kernels.
* Wash efficiency, bed channelling, protein fouling of the electrode and temperature are not modelled.
* The immune-complex transfer of tier 3 enters as the lever of docs/05 (`ma.design_levers`, UNVERIFIED magnitude),
  not as physics.
