# 09 — Second-generation cartridge: requirements, interfaces and modelling map

Status: 2026-11-12. Draft written for the cartridge design agents. Inputs: docs/00, 02, 04, 05, 06, 07, 08,
`params/*.yaml`, `src/elisa_sim/`, `scripts/`, `automation/config/`. This document does not change any earlier
document, parameter or code. The first-generation build (docs/05 §4.1, tubing + valves + SIA module) is still
built first. The cartridge replaces everything **downstream of the SM-FL outlet**.

**How to read the sources.** Every number names where it comes from in this repository: a document section
(`docs/05 §4.1`), a parameter key (`hw.bsm.flow_min`, `ma.capture.magnetic_trap_efficiency`, `chem.…`), a
script or results file. The confidence attached to a parameter is the one in the YAML file. **UNVERIFIED** means
the repository itself marks the value as an unchecked estimate, or that I could not trace it to a source in the
repository. "Derived" means calculated here from the cited inputs; the arithmetic is shown. No new external
source was consulted for this document.

**User decisions that frame the cartridge (interview, 2026-11-12).**
* The cartridge carries the fluidic path (incubation/mixing, capture zone, electrochemical cell), on-chip valving
  and on-board reagents (capture phase, ALP conjugate, HQDP substrate, wash as needed).
* The docking station may contain anything (pressure controllers, syringe pumps, magnets, heaters/coolers,
  pogo-pin contacts, valve actuators). Only the consumable has to be simple.
* The assay format is reopened: one-step beads, sequential beads, fixed packed or monolithic bed, wall-coated
  capture or other on-chip formats.
* Left open for the design agents: fabrication route, chip lifetime (single-use, multi-run, permanent),
  detector (single thin-layer WE vs IDA with redox cycling; a second potentiostat channel is acceptable), batch
  size per reagent load, parallel or staggered incubation.
* Unchanged (docs/00): LOD ≤ 1 pg/mL (mean blank + 3 SD of replicate blanks, through a calibration curve);
  calibration about 1–1000 pg/mL; ≤ 100 µL injected per determination (full-loop, ~200 µL drawn, accepted);
  ≤ 60 min from injection to result; sample vials contain sample only; no manual step between loading the
  autosampler and the result; capture surface reusable or automatically renewed; buffer matrix only; Python
  orchestrates the added hardware, Empower runs the Waters stack.

---

## 1. System boundary

### 1.1 Where the boundary is

```
BSM (A1/A2, B1/B2) -> mixer -> restrictor(s) -> SM-FL 6-port injection valve (100 uL loop, full loop)
   -> "to column" port of the SM-FL  ==>  CARTRIDGE INLET (this document)
CARTRIDGE: incubation/mixing, capture, washing, substrate, accumulation, electrochemical readout, valving,
   on-board reagents  ==>  waste outlet(s);  electrical signal to the Gamry via the dock
```

In gen-1 (docs/05 §4.1) the SM-FL outlet feeds V4 (6-port), which sends the sample either to the incubation cup
(position A) or to a tee in front of V2 (position B). Everything after that point is the cartridge's job.

### 1.2 What arrives at the SM-FL outlet

| Quantity | Value | Source (repo) | Confidence / note |
|---|---|---|---|
| BSM flow range | 1–2000 µL/min (user figure); vendor I-Class spec 10–2000 µL/min | `hw.bsm.flow_min` overridden to 1 µL/min in `ma.overrides` (docs/00 "Installed configuration"); `hw.bsm.flow_max` | 1 µL/min is the user's statement, to be confirmed at the bench (docs/00; docs/08 §10 "left open") |
| Flow step | 1 µL/min | `hw.bsm.flow_step` | high |
| Flow precision | 0.075 % RSD, specified only for 0.2–2.0 mL/min | `hw.bsm.flow_precision_rsd_spec_range` | high, but outside the range used by the assay |
| Flow precision at 10–100 µL/min | 1 % RSD (0.2–5 %) | `hw.bsm.flow_precision_rsd_low_flow` | **UNVERIFIED**; measure gravimetrically (docs/02 R6, docs/06 S0.6) |
| Flow accuracy | ±1 % at 0.5 mL/min (1–3 % assumed at low flow) | `hw.bsm.flow_accuracy` | medium; low-flow bound is a guess |
| Pressure pulsation | ≤ 0.4 % or 25 psi (Premier spec; not stated for I-Class) | `hw.bsm.pressure_pulsation` | medium |
| Max. pump pressure | 18 000 psi (I-Class) to 1 mL/min | `hw.bsm.pressure_max_to_1mLmin` | high |
| Back-pressure the **pump** needs | ≥ 1000 psi recommended | `hw.bsm.min_backpressure_recommended` (WKB32564) | high. It is produced by restrictor(s) **upstream** of the injector; the cartridge sees only its own hydraulic resistance (docs/02 §1.2) |
| Restrictor pressure drop | ≈ 12 psi per µL/min (9–16) for one Waters 40 µm × 35 cm restrictor | `hw.bsm.restrictor_dp_per_flow` | medium (Derived, Hagen–Poiseuille). At 1–10 µL/min one restrictor gives only 12–120 psi; the pump is then far below its recommended back-pressure (open bench item, docs/08 §10) |
| Pressure at the cartridge inlet | = flow × cartridge hydraulic resistance + outlet line; no pressure is imposed by the Waters stack | docs/02 §1.2, §5.1 | Design rule: EC cell outlet open to waste through ≤ 50–100 psi of tubing; commercial thin-layer cell rated 0.8 MPa (`hw.flow_cells.metrohm_thin_layer.pressure_limit`); custom cell design ≥ 1 MPa (docs/02 §5.2) |
| BSM-to-outlet delay (dwell) volume | 90 µL (60–110) with the loop offline | `hw.bsm.delay_volume_to_injector_outlet` | medium. A step A1 → B1 reaches the outlet after this volume (+ loop 100 µL if the loop stays in line, docs/08 W4) |
| Line change within a channel (A1 → A2, B1 → B2) | needs ≈ 500 µL (200–1000) flush of pump head and mixer | `hw.bsm.line_change_flush_volume` | **UNVERIFIED** |
| Number of solvent lines | 4, two pumped at a time (A1 or A2 with B1 or B2) | `hw.bsm.solvent_lines` | high |
| pH range of the BSM | 2–12 (I-Class) | `hw.bsm.ph_min`, `hw.bsm.ph_max` | high |
| Mixer | 50 µL standard | `hw.bsm.mixer_volume` | high |

**Composition of the BSM stream (gen-1 allocation; the cartridge may change it).**

| Line | Content | Source |
|---|---|---|
| A1 | Wash/running buffer: **Tris-buffered saline + 0.05 % Tween-20, no phosphate, no protein** | docs/05 §4.1 plumbing (revised after final review, B1); docs/08 B1, §10 |
| A2 | Water or 10–20 % methanol (storage, end-of-day flush; salt must not stand in steel parts) | docs/02 §1.2 |
| B1 | HQDP substrate, 1 mM (3 mM if needed for the ULOQ), pH 9.5 with Mg²⁺, IgG-free | docs/05 §4.1 "Label and substrate"; `ma.chemistries.alp_hqdp.substrate_concentration` (1 mM, design range 0.1–5 mM) |
| B2 | spare (regeneration only if a regenerated bed is used; docs/02 prefers injecting glycine pH 2 rather than pumping it, because pH 2 is the I-Class limit) | docs/02 §1.2 |

Constraints that come with the BSM stream:
* **No protein or bead suspension may pass the BSM** (pump heads, check valves, mixer): adsorption, hold-up,
  blockage (docs/02 §1.2; docs/05 §4.0 route D "inadmissible"). Protein and beads reach the cartridge only from
  the SM-FL loop (sample) or from the cartridge's own reservoirs.
* **No phosphate anywhere that reaches the enzyme step** (docs/08 B1; `chem.enzymes.alp.phosphate_inhibition_Ki`
  note). §3.4 gives the numbers.
* HQDP in B1 stands in the BSM steel heads and lines for > 24 h in unattended sequences; its stability there is
  measured only by docs/06 E1.2 (0–30 h plus a pumped aliquot, docs/08 S11). On-cartridge substrate storage
  removes this exposure but creates a storage requirement (§3).
* The Waters fluid path is earthed and contains metal (I-Class BSM: 316L, MP35N, titanium; docs/02 §1.1). The
  conductive buffer couples mains and pump noise into the cell. Gen-1 rule: PEEK for ≥ 0.3 m on each side of the
  cell (`hw.tubing.peek_isolation_length_each_side_of_cell`, ≈ 15 MΩ per 0.3 m of 127 µm ID at κ ≈ 1.6 S/m,
  `hw.tubing.buffer_conductivity` **UNVERIFIED**), a defined earth point upstream, Faraday cage (docs/02 §4.4).
  **The cartridge must provide an equivalent solution-path resistance between the SM-FL outlet and the cell,
  and between the cell and any earthed waste path**, or accept the noise penalty.

**The sample plug.**

| Quantity | Value | Source | Note |
|---|---|---|---|
| Loop volume | 100 µL (installed) | `hw.smfl.loop_volume_recommended` overridden to 100 in `ma.overrides` (docs/00) | high |
| Injection mode | full loop, 2× overfill: 100 µL injected, ≈ 200 µL drawn | docs/00 decisions; `ma.delivery.delivered_fraction_full_loop_100` = 1.0 (0.97–1.0); `hw.smfl.full_loop_overfill_factor_100uL` = 2.0 | Loop contains only sample, no air, no weak wash (docs/02 §2.1) |
| Loop inner diameter | 0.5 mm (0.25–0.76) | `hw.smfl.loop_inner_diameter` | **UNVERIFIED** (docs/02 Q2). Sets dispersion and adsorption area |
| Injection precision | 0.5 % RSD (0.25–1 %) | `hw.smfl.injection_precision_rsd_large` | medium; > 50 µL not specified by Waters |
| Fraction of the plug out of the loop after n loop volumes of flush (100 µL loop, 0.5 mm ID, 100 µL/min, IgG) | 0.77 (1 V), 0.90 (1.5 V), 0.96 (2 V), 0.997 (3 V) | docs/02 §2.4(c) table (2-D convection–diffusion); model: `elisa_sim.transport.loop_transfer_interp`, `hw.smfl.loop_flush_volumes_for_transfer` (3; 2–5) | Loop ID UNVERIFIED. At 0.25 mm ID transfer is faster. Beads are not involved (sample only) |
| Consequence for the cartridge | the 100 µL sample arrives **spread over 200–300 µL** of A1 (≈ 2–3× dilution); ≥ 2 loop volumes (200 µL) are needed for 96 % transfer, ≥ 3 (300 µL) for 99.7 % | Derived from the row above | gen-1 pushes 2 loop volumes (200 µL) into the cup and takes the 4 % loss: LOD × 1/0.96 (`scripts/final_designs.py` `CHAMBER_TRANSFER`) |
| Time to push 2 loop volumes | 2 min at 100 µL/min | docs/05 §4.1 step "1 → 3" | |
| Analyte loss upstream of the cartridge (vial, needle, loop) with IgG-free carrier | 0.2 (0.02–0.6) | `ma.delivery.adsorptive_loss_fraction_with_carrier` | **UNVERIFIED**; the cartridge cannot recover it but must not add to it |
| Analyte amount at 1 pg/mL | 6.7 fM ≈ 4×10⁵ molecules (0.67 amol) in 100 µL | docs/00 | |
| SM-FL carry-over of protein into the next injection | 1×10⁻⁴ (1×10⁻⁵–1×10⁻³) | `hw.smfl.carryover_protein_conjugate` | **UNVERIFIED** (small-molecule spec 1×10⁻⁵ is a lower bound, `hw.smfl.carryover_small_molecule`). With sample-only injections, this concerns sample → sample carry-over |
| Sample compartment temperature | 4–40 °C, ±0.5 °C | `hw.smfl.compartment_temp_min/max` | high |

### 1.3 Timing signals available

| Signal | What it gives | Source | Status |
|---|---|---|---|
| SM-FL **Inject Start** contact closure (connector 1, positions 1–2) | t₀ of each injection; the gen-1 sequencer anchors every step to it | docs/02 §2.3, §3.1 (WKB55803) | verified; pulse width **UNVERIFIED**; latency assumed 0.05 min (`hw.timing.contact_closure_latency`, **UNVERIFIED**) |
| BSM / SM-FL timed event outputs (2-bit line code at t₀ + 3 s) | which kind of line started | docs/02 §3.2 | number, type and rating of outputs **UNVERIFIED** (docs/02 Q6) |
| Event inputs (inject hold, external start) | would let Python release injections | docs/02 §3.2 Fallback B | **UNVERIFIED**; not relied on |
| Empower Toolkit start/stop of a sample set | Python as master | docs/02 §3.1 Fallback A | licence held (docs/00); capability **UNVERIFIED** |
| Aspiration before Inject Start | ≈ 1 min (0.25–2) per injection | `hw.smfl.injection_overhead_time` | **UNVERIFIED** |
| Loop Offline (loop returns to load after a set time) | removes the loop from the flow path | `hw.smfl.loop_offline_supported` | supported; causes a small pressure blip (docs/02 §2.4c), so the cell should be isolated at that moment |

Synchronisation model the cartridge must fit (docs/02 §3.2, docs/05 §4.1, `automation/elisa_auto/sequencer.py`):
Empower runs one sample-set line per sample (injection + BSM programme); Python receives Inject Start through
an isolated DAQ input and runs the cycle table for the docking station and the Gamry. A watchdog faults on a
late, early, unexpected or wrong-code Inject Start and drives the safe state (§2.10).

### 1.4 What the cartridge must return

| Output | Requirement | Source |
|---|---|---|
| Waste | All liquid to a waste outlet (or an on-cartridge waste store sized for N determinations, §3.6). Beads leave to waste every run in bead formats. The waste path must not be electrically shorting the cell to earth (§1.2) and must not route beads through the optical detector (docs/08 W3) | docs/05 §4.1 step 52.6–56.1 |
| Electrochemical signal | WE/RE/CE (and WE2 for an IDA) to the Gamry through the dock; the Gamry is floating (`hw.gamry.floating`) | docs/02 §4.1, §4.4, §5.2 (pogo pins proposed there) |
| Quantity reported | integrated charge over the readout window with baseline windows before and after, at the same flow (docs/08 W5); chronoamperometry | docs/05 §4.1; `automation/elisa_auto/signal_proc.py` |
| Timing | result ≤ 60 min after Inject Start; gen-1 primary 52.1 min from Inject Start to end of the post-baseline window (56.1 min from aspiration start) | docs/08 W1; docs/06 §7.8 |
| State information | cartridge/dock faults and sensor readings to Python (for the fault latch, §2.10); the run log records each step | `automation/elisa_auto/latch.py`, `runlog.py` |
| Optional optical tap | bead-free tracer experiments only (TUV cell ≈ 500 nL, 1000 psi max, docs/02 §7) | docs/05 §4.1 |

---

## 2. Function list: what gen-1 does downstream of the SM-FL, and the on-chip requirement

Gen-1 reference: docs/05 §4.1 (primary, one-step mode; sequential mode as in-platform fallback),
`automation/config/cycle_primary.yaml` (step table as executed, revised after the final review),
`cycle_sequential.yaml`, `cycle_recovery.yaml`, docs/07 §5 (custom-part specifications). Times are cycle minutes
with t = 0 at aspiration start and Inject Start at t = 1.0 (`cycle_primary.yaml` header).

### 2.1 Gen-1 cycle in one table (one-step mode)

| Cycle min | Step | Volumes and flows | Source |
|---|---|---|---|
| −1.0 → −0.6 | dose 10 µL bead suspension (5×10⁵ beads) from the bead-only reservoir into the cup | SIA 10 µL | `cycle_primary.yaml` `dose_beads` |
| −0.6 → −0.4 | flush the common SIA channel to waste | 50 µL wash | `flush_sia_channel` |
| −0.4 → 0 | dose 10 µL of 6.6 nM ALP conjugate from the separate conjugate reservoir into the cup (0.3 nM in ≈ 220 µL) | SIA 10 µL | `dose_conjugate`; docs/08 B4 |
| 0 → 1 | SM-FL aspirates ≈ 200 µL of sample | BSM 100 µL/min A1 | `aspirate_sample` |
| 1 → 3 | Inject Start; 2 loop volumes push the sample into the cup | 200 µL at 100 µL/min | `transfer_sample_to_cup` |
| 3 → 33 | **incubation 30 min**, mixed by SIA aspirate/dispense 50 µL every 2 min | BSM 100 µL/min A1 to waste via shunt (3 mL) | `incubation` |
| 33 → 39.6 | magnet on; cup contents + 2 rinses through the trap | SIA 653 µL at 99 µL/min + BSM 1 µL/min = **100 µL/min at the trap** | `load_trap`; docs/08 S2 |
| 39.6 → 40.6 | wash (≥ 50 trap volumes) | 100 µL A1 | `wash`; docs/05 §4.1 |
| 40.6 → 41.6 | substrate fill (A1 → B1 step) | 200 µL B1 at 200 µL/min | `substrate_fill`; docs/08 W4 (switch completeness at the trap UNVERIFIED) |
| 41.6 → 51.6 | **accumulation 10 min**, trap sealed (V2 isolate); fresh substrate through shunt and cell, substrate blank current recorded | 100 µL B1 at 10 µL/min | `accumulation`; docs/08 W5 |
| 51.1 → 51.6 | pre-baseline window (inside accumulation) | – | `signal.pre_baseline` |
| 51.6 → 52.6 | **readout**: trap contents swept through the cell, charge integrated | 10 µL B1 at 10 µL/min | `readout` |
| 52.6 → 53.1 | post-baseline (trap sealed, fresh substrate through the cell) | 5 µL B1 | `post_baseline` |
| 53.1 → 56.1 | magnet off, beads to waste; SM-FL needle wash (no injection); SIA rinses the cup 3× | 900 µL A1 at 300 µL/min | `clean`; docs/08 S3, W3 |

Time to result: 56.1 min from aspiration start; 52.1 min from Inject Start to the end of the post-baseline window
(docs/08 W1). Throughput: one sample per 56 min with one cup; ≈ 30 min per sample with a second cup (docs/05 §4.1;
docs/08 W10).

**Sequential mode** (fallback on the same hardware): beads only into the cup; after the trap wash, 20 µL of 3 nM
ALP conjugate stopped on the trapped beads for 3 min, then a 2 min wash; accumulation 5 min; time to result
58.1 min (docs/05 §4.1). The mode boundary is a detection-reagent **on-bead** half-life of about 30 min (docs/08 S4
resolution; `scripts/mode_choice.py`): one-step wins above, sequential below; between 30 and 45 min the choice is
LOD-neutral.

**Backup fixed micro-bed** (docs/05 §4.2): 0.5 µL bed of 50 µm particles in a 0.5 mm ID column; sample loaded at
10 µL/min (2 loop volumes, 20 min); 20 µL of 1 nM conjugate, 2 min stop, 2 min wash; accumulation 15 min; glycine
pH 2 regeneration 6.5 min; 51.5 min; recalibration every ≈ 20 cycles at 0.5 %/cycle capacity loss
(`chem.regeneration.activity_loss_per_cycle`).

### 2.2 Function-by-function requirements

| # | Gen-1 function | Gen-1 quantitative specification | Source | On-chip requirement (what the cartridge must achieve) |
|---|---|---|---|---|
| F1 | **Sample reception** (V4 position A → cup) | 200 µL (2 loop volumes) at 100 µL/min; analyte transfer 0.96 at 2 loop volumes, 0.997 at 3 | docs/05 §4.1; docs/02 §2.4(c) | Accept 200–300 µL of BSM-driven flow at 10–100 µL/min (or whatever flow the cartridge resistance allows at ≤ the cell's pressure rating) and capture ≥ 96 % of the injected analyte. Every µL of sample-contact surface counts as fM-level adsorption area: no untreated hydrophobic surfaces in the sample path (`ma.delivery.adsorptive_loss_fraction_with_carrier`, `chem.analyte.adsorptive_loss_fraction_untreated_tube` 0.5 (0.1–0.9) for untreated). A vent or compliant volume is needed if the chamber is filled while closed |
| F2 | **Incubation/mixing chamber** (the cup) | working volume 0.25–0.5 mL, design fill ≈ 220 µL; total ≤ 0.8 mL; residual after emptying ≤ 2 µL; mixing 50 µL aspirate/dispense every 2 min; optional Peltier 20–25 °C ±0.2 °C | docs/07 §5.1; docs/05 §4.1 | Hold sample + capture phase (+ conjugate in one-step mode) for a **fixed, identical time for every sample** (incubation starts at injection; ±2 min changes the calibration slope by −5.8/+5.6 %, docs/05 §4.3). **Active mixing that keeps 2.8 µm beads suspended** (settling ≈ 7 mm/h, `ma.capture.in_vial_unstirred_rate_factor` note). The model's capture rate relative to a well-mixed suspension is sampled 0.2–1.0 divided by the 2.2× dilution (docs/08 S13); this single factor moved the primary's median LOD from 2.0 to 3.0 pg/mL (docs/08 §10.2), so mixing quality is a first-order requirement. A smaller chamber (less dilution) raises the capture rate per bead in the model (§5) |
| F3 | **Bead dosing** (SIA, port 1) | 10 µL of 5×10⁷ beads/mL = 5×10⁵ beads; dose CV ≤ 5 % (U5 confirm; go to backup if > 10 %); model `ma.capture.bead_dose_cv` 0.05 (0.02–0.15, **UNVERIFIED**) | docs/07 §5.5; docs/05 §5 U5 | Meter the capture phase into the chamber with CV ≤ 5 % from a store where beads stay suspended (or are resuspended before dosing) over the whole cartridge life; beads must never sit in conjugate before the timed incubation (F4) |
| F4 | **Conjugate dosing** (SIA, port 6, separate from beads) | 10 µL of 6.6 nM → 0.3 nM in ≈ 220 µL (one-step); 20 µL of 3 nM onto trapped beads (sequential); dose CV ≤ 5 % | docs/07 §5.5; docs/05 §4.1; docs/08 B4 | Separate conjugate store; dose CV ≤ 5 %; **no shared bead + conjugate compartment**: under the model a 30 min mean hold of beads in 3.3 nM conjugate multiplies bead NSB ×10 and takes the primary's P from 0.16 to 0.01 (`results/design/shared_reservoir_cost.md`). Conjugate should not pass through anything that later lies in the product path (F8) |
| F5 | **SIA common channel flush** between bead and conjugate doses | 50 µL wash to waste | `cycle_primary.yaml` `flush_sia_channel` | Any shared on-chip channel or valve that carries beads and conjugate must be flushed between them, or the two paths must be fully separate |
| F6 | **V4** (6-port): SM-FL outlet → cup, or → tee/V2 | 2 positions; sends BSM flow to waste through the shunt during incubation (3 mL A1 per run) | docs/05 §4.1 | On-chip valve (or dock-side valve) that routes the BSM stream either into the chamber or past it to waste. The gen-1 design wastes 3 mL of A1 per run during incubation; a cartridge can instead park the BSM at its minimum flow (1 µL/min, if the user's figure holds) or shunt it in the dock |
| F7 | **Bead transfer chamber → capture zone** | 653 µL at 99 µL/min (cup + 2 rinses) + 1 µL/min BSM = 100 µL/min at the trap; 6.6 min; bead transfer modelled 1 − 1/(4 × 6.6) = 0.96 | `cycle_primary.yaml` `load_trap`; `scripts/inline_chamber.py` docstring | Move ≥ 96 % of the beads (and the bound analyte) into the capture/accumulation zone; total flow at the capture zone ≤ 100 µL/min unless retention is shown at higher flow (`ma.design_levers.max_bead_loading_flow`); two pumps into one junction add their flows (docs/08 S2) — the cartridge must declare the flow through the capture zone in every step |
| F8 | **Magnetic trap** (bead capture zone, also the accumulation volume) | 1.5 mm ID, 1.1 mm magnet zone, ≈ 2 µL (`ma.geometry.magnetic_trap_volume` 2 µL, 1–10, **UNVERIFIED**; `ma.geometry.magnetic_trap_tube_inner_diameter` design 1.5 mm); retention ≥ 90 % at 100 µL/min (`ma.capture.magnetic_trap_efficiency` 0.9, 0.5–0.99, **UNVERIFIED**); trap length ≥ 1 mm (design rule, **UNVERIFIED**); wall ≤ 0.5 mm; NdFeB on an actuated slide, fail-safe = magnet on; pressure ≥ 1 MPa; PEEK, optional PEG/BSA coat | docs/07 §5.2, §5.4; docs/05 §1.1 | Retain ≥ 90 % (target from U5) of the capture phase at the loading flow; release ≥ 99.9 % (residual beads ≤ 10⁻³, U5) — **but see carry-over F13: the 10⁻⁴ criterion needs ≤ 10⁻⁴ residual activity**; capture-zone wall product ≤ 10 % of bead NSB product (U4 confirm; coat or re-trap if > 30 %). In the gen-1 model the beads carry 92 % of the NSB and the trap wall + 1 cm of stubs 8 % (P-chamb nominal, `evaluate(...).diagnostics['bead_share_of_nsb']` = 0.92, computed for this document) |
| F9 | **V2** (10-port reactor isolation) | trap screwed into ports 2/3 with ≤ 5 mm stubs each side (isolated tubing 0.01 m, `ma.design_levers.min_isolated_connection_length`); shunt with similar resistance (docs/02 §7.2) | docs/05 §1.1, §4.1 | **Seal the accumulation volume** (true stopped flow, no product leaving) for 5–15 min while fresh substrate can still flow past it to the cell for the blank baseline. Minimise conjugate-exposed area that is sealed with the capture zone: the isolated tubing length was the single largest gain for sequential beads (×4 in median, docs/05 §1.3). Valve switching must not push product out of the sealed zone (no pumping displacement) |
| F10 | **Washing** | post-capture wash ≥ 1 min; wash after conjugate ≥ 2 min (constraints because wash efficiency is not modelled); trap wash 100 µL at 100 µL/min (≥ 50 trap volumes) | `scripts/design_lib.py` `constraint_violations`; docs/05 §4.1 | Remove free conjugate to below its contribution to the blank. The model gives no number for "enough" washing; keep ≥ 50 accumulation-zone volumes and the time minima above until bench data exist (U1 wash-stringency arm, docs/06 E1.3) |
| F11 | **Substrate delivery** (BSM B1) | 200 µL at 200 µL/min fill, then 10 µL/min; HQDP 1 mM (3 mM if ULOQ needs it) | `cycle_primary.yaml`; docs/05 §1.5, §4.1 | Fill the accumulation zone with substrate that has **no A1 left in it** (phosphate-free in any case, but A1 dilution changes the substrate concentration; docs/08 W4) and provide fresh substrate to the cell for baselines. The substrate source can stay on the BSM (B1) or move onto the cartridge (§3) |
| F12 | **Accumulation and readout** | accumulation 10 min (one-step), 5 min (sequential), 15 min (bed); readout 1 min at 10 µL/min; baseline windows 0.5 min before and after at the same flow; potential +0.35 V vs Ag/AgCl (generator) | docs/05 §4.1; `cycle_primary.yaml` `signal`, `potentiostat` | Sealed accumulation volume of known size; then a transfer of ≥ 99 % of the product to the electrode within the read window (gen-1 model: eluted fraction 0.993, cell conversion 0.78 for the thin-layer cell at 10 µL/min — P-chamb nominal diagnostics computed for this document), or read in place (Scheme C). Baselines at the readout flow |
| F13 | **V3** (cell in / bypass) and the **cell** | V3 6-port: cell in the path only for accumulation baseline, readout and post-baseline; protein, beads, glycine bypass the cell. Default cell (Stage 3): commercial single-channel thin-layer, GC or Au, ≤ 1 µL, ≥ 1 MPa, external Ag/AgCl; optional IDA (50 pairs, 5/5 µm, 1 mm, 25 µm × 0.5 mm channel, Au/Pt) with a second channel only if G2 shows EC noise ≥ 30 % of blank SD | docs/07 §3, §5.3; docs/08 S9 | Electrode protected from protein, beads and low pH except where the format deliberately reads in place (Scheme C: then electrode fouling/sensitivity CV 0.1 (0.03–0.3) and 1 %/cycle loss apply in the model, `ma.noise.electrode_sensitivity_cv_fouling`, `ma.reuse.electrode_sensitivity_loss_per_cycle_fouling`). Reference: Ag/AgCl with KCl leakage **downstream** of the WE, CE downstream (docs/02 §5.2). Pressure at the cell ≤ its rating (0.8 MPa commercial). Electrical isolation as §1.2 |
| F14 | **Bead release, flush and cup rinse** | magnet off; 900 µL A1 at 300 µL/min; cup rinsed 3×; residual beads ≤ 10⁻³ of the dose after 3 rinses (U5); cycle step 3.0 min (model `ma.timing.bead_flush_and_clean` 3.5 min, 2–6) | `cycle_primary.yaml` `clean`; docs/05 §5 U5 | Remove all capture phase and label from every surface in the analyte path before the next sample (renewal by replacement). For a fixed bed: regeneration (glycine pH 2, 6.5 min in gen-1 backup) with ≤ 0.5 %/cycle capacity loss (`chem.regeneration.activity_loss_per_cycle`, 0–7 %, low confidence) and residual label ≤ 10⁻⁴ of the previous run (`chem.regeneration.residual_label_carryover_fraction`, 10⁻⁶–10⁻², **UNVERIFIED**) |
| F15 | **Carry-over control** | analyte path ≤ 1×10⁻⁴, tested with a 10 ng/mL challenge read through the low-range slope (`automation/config/gates.yaml` `carryover`, `injector_carryover`; docs/08 S6); alternative: a mandatory cleaning cycle after any sample > 100 pg/mL | docs/08 S6, §10 | ≤ 1×10⁻⁴ for everything the cartridge adds (chamber, valves, capture zone, cell), on top of the SM-FL's own carry-over (`hw.smfl.carryover_protein_conjugate` 10⁻⁴, **UNVERIFIED**). Note: the gen-1 U5 acceptance of residual beads ≤ 10⁻³ is **ten times looser** than the 10⁻⁴ criterion if those beads carry the previous sample's sandwich (Derived) — a multi-run cartridge must meet ≤ 10⁻⁴ residual bead-borne signal, or run the cleaning cycle after high samples |
| F16 | **Fault safe state** | V2 isolate, V3 bypass, V4 B, magnet on (beads held), SIA stop, potentiostat cell off; Inject Start tolerance 30 s; first inject may wait 3600 s | `cycle_primary.yaml` `safe_state`, `watchdog` | Every actuator in the dock has a defined, fail-safe state reachable without the PC (docs/08 §6 notes the PC-death limitation is stated honestly in the sequencer); the cartridge must not drain, siphon or let beads escape toward the cell in that state |
| F17 | **Fault latch and recovery** | after any fault every subsequent run is executed but flagged invalid until a recovery cycle completes and is logged: magnet off, 900 µL at 300 µL/min through the trap, cup rinse (≈ 5 min) | `automation/elisa_auto/latch.py`; `cycle_recovery.yaml`; docs/08 S12 | The cartridge must have a recovery operation that returns it to a clean, known state from any step (including mid-incubation and mid-accumulation), report completion to Python, and consume a known amount of on-board wash/reagent (reserve it in the N-determination sizing) |
| F18 | **Blanks and controls** | blanks and a mid-range control every 10 samples (tracks NSB drift) | docs/05 §4.1 | Reserve reagent for 2 extra determinations per 10 samples (Derived: 20 % overhead) |
| F19 | **Temperature** | none in gen-1 (22 ± 1 °C recorded in Stage 1); Peltier for cup and trap is conditional (docs/07 §3) | docs/06 §4.0; docs/05 §4.5 point 5 | The dock may thermostat the chamber and capture zone (open choice). The model has no temperature dependence (docs/03 §11) |
| F20 | **Electrical isolation / noise** | PEEK ≥ 0.3 m each side of the cell; Faraday cage; earth point upstream | docs/02 §4.4 | Equivalent solution-path resistance on the cartridge (long narrow channel or air gap/valve break), shielding of the cell contacts in the dock |

### 2.3 Time budget for a cartridge cycle

The 60-min limit is from injection to result (docs/00). Gen-1 spends (one-step): 2 min sample transfer, 30 min
incubation, 6.6 min bead transfer, 1 min wash, 1 min substrate fill, 10 min accumulation, 1 min readout, 0.5 min
post-baseline (docs/05 §4.1). The 30-min incubation and 10-min accumulation are the model's design values; the
in-vial optimum was 35 min incubation and 15 min accumulation, limited by the 60-min constraint (docs/05 §1.2,
"active constraints"). Every minute a cartridge saves in transfer, wash and fill can be spent on incubation or
accumulation, where the model shows a gain (in-vial 30 → 35 min ×1.05; longer accumulation ×1.2 for one-step,
docs/05 §1.3). Throughput (parallel or staggered chambers) is not limited by the 60-min criterion; gen-1 needs a
second cup to overlap samples (docs/08 W10).

---

## 3. Reagent inventory per determination

All figures are per determination in the gen-1 design unless marked otherwise. "Derived" volumes follow from the
step table. For a cartridge holding N determinations, add the dead volume of each store, the recovery-cycle
consumption (F17) and the controls overhead (F18).

### 3.1 Capture phase (magnetic beads)

| Item | Value | Source |
|---|---|---|
| Bead type | streptavidin superparamagnetic, 2.8 µm (Dynabeads M-280 Streptavidin) | docs/07 §1.1; `ma.geometry.magnetic_bead_diameter` |
| Beads per determination | 5×10⁵ (primary); 1.5×10⁶ at the sequential optimum; literature optimum 2×10⁵–1×10⁶ per 100 µL | docs/05 §1.2; `chem.surfaces.bead_number_per_100uL_digital_ELISA` (Rissin2010) |
| Mass | 5×10⁵ beads = 7.7 µg (6.5×10¹⁰ beads/g, INHERITED) | docs/06 §4.0; `chem.surfaces.magnetic_bead_M280_count_per_mass` |
| Capture antibody | biotinylated goat F(ab′)₂ anti-human IgG Fcγ-specific, loaded at ≈ 80 % of 10 µg/mg capacity (≈ 0.06 µg per determination, Derived: 7.7 µg × 10 µg/mg × 0.8) | docs/06 §4.0; docs/07 §1.1; `chem.surfaces.magnetic_bead_M280_SA_capacity_biotinylated_IgG` |
| Bead preparation | stock washed 3× in TBS (stock is in PBS — phosphate), loaded 30 min, quenched with 10 µM biotin, washed, blocked 30 min in AB | docs/06 §4.0; docs/08 B1 |
| Dosing suspension | 5×10⁷ beads/mL in TBS + 1 % IgG-free BSA + 0.05 % Tween; 10 µL per dose | docs/07 §5.5 |
| Storage | 4–8 °C, dark, low-shear stirring or rocking that keeps beads suspended without foaming; settling ≈ 7 mm/h | docs/07 §5.5; `ma.capture.in_vial_unstirred_rate_factor` note |
| Stability constraints | dose CV ≤ 5 % over 8 h (E2.2 acceptance); bead storage life with capture antibody loaded: **not measured, UNVERIFIED**; the bead stock contains BSA on some lots (bovine-IgG risk, E1.4) | docs/07 §1.1, §5.5 |
| Non-immune beads (only if a reference channel, lever L5) | same, with biotinylated normal goat F(ab′)₂ | docs/06 §4.0; docs/05 §2 L5 (needs 3–4 potentiostat channels) |

### 3.2 Detection conjugate (ALP)

| Item | Value | Source |
|---|---|---|
| Reagent | ALP-labelled F(ab′)₂ goat anti-human IgG F(ab′)₂-specific (asymmetric to the Fc capture) | docs/07 §1.1; docs/05 §4.1 |
| One-step mode | 10 µL of 6.6 nM per determination → 0.3 nM in ≈ 220 µL; = 66 fmol (Derived: 6.6×10⁻⁹ M × 10⁻⁵ L) | docs/07 §5.5; `cycle_primary.yaml` |
| Sequential mode | 20 µL of 3 nM, 3 min stop on the trapped beads; = 60 fmol (Derived) | docs/05 §4.1 |
| Backup bed | 20 µL of 1 nM, 2 min stop | docs/05 §4.2 |
| Model design concentration | `chem.antibodies.conc_detection_antibody_typical` 1 nM nominal, design values 0.3 nM (one-step) and 3 nM (sequential); lower one-step conjugate (1 → 0.3 nM) is needed to keep ULOQ ≥ 1000 pg/mL | docs/05 §1.2, §1.3 |
| Enzyme:antibody ratio | 1 (0.5–2), **UNVERIFIED**; acceptance ALP:Ab 0.5–2 | `chem.antibodies.enzyme_to_antibody_ratio_ALP`; docs/05 §4.1 |
| Buffer | TBS + 1 % IgG-free BSA; **no phosphate, no azide** | docs/07 §5.5 |
| Storage | 4–8 °C, dark, not stirred, sealed, low-binding glass or PP; **never together with beads** | docs/07 §5.5; docs/08 B4 |
| Stability constraints | conjugate-only ageing arm of E1.3 (D1 at 6.6 nM, 4 and 22 °C, 0/2/8/24 h): if the blank rises > ×1.5 at 24 h, a maximum reservoir life is set; default refill per 8-h block. **No measured value yet.** Reservoir-ageing with beads (B4) is the reason stores are separate | docs/06 E1.3 (lines ≈ 293–307); docs/07 §5.5 |
| Detection kinetics that set the mode | detection k_off nominal 8.6×10⁻⁴ s⁻¹ (t½ ≈ 13 min; conservative solution value), range 3×10⁻⁶–8.3×10⁻³; mode boundary at on-bead t½ ≈ 30 min | `chem.antibodies.koff_detection`; docs/08 §9 C9, S4 |
| Reagent-borne human IgG | possible (e.g. leached from affinity columns), **UNVERIFIED for these lots**; grows with pre-incubation on capture beads; measured in E1.3 ageing and E1.9 | docs/08 B4, S5 |

### 3.3 Substrate (HQDP)

| Item | Value | Source |
|---|---|---|
| Composition | HQDP 1 mM (0.3 mM Stage-1 readout default; 3 mM option for the ULOQ; model design range 0.1–5 mM) in 0.1 M Tris pH 9.5, 1 mM MgCl₂ | docs/06 §4.0 (SB); `ma.chemistries.alp_hqdp.substrate_concentration` |
| Gen-1 consumption via B1 | ≈ 315 µL per determination (Derived from `cycle_primary.yaml`: fill 200 + accumulation shunt 100 + readout 10 + post-baseline 5 µL) plus BSM line hold-up (0.5–1 mL per cycle, docs/02 §1.2, **UNVERIFIED** estimate) | as stated |
| Minimum on-chip need | accumulation volume (2 µL trap in gen-1) × fill factor + cell priming + baseline flows (≈ 10 µL/min × baseline time); the fill factor that removes A1 completely is not specified (docs/08 W4) | Derived |
| Free hydroquinone in the lot | acceptance ≤ 10⁻⁵ mol/mol; model 10⁻⁵ (10⁻⁷–10⁻³, **UNVERIFIED**); at 10⁻³ every design fails (S4a) | docs/05 §5 U3; `ma.chemistries.alp_hqdp.free_product_impurity` |
| Hydrolysis | acceptance ≤ 10⁻⁹ s⁻¹ at room temperature; model 10⁻¹⁰ (10⁻¹²–10⁻⁸, **UNVERIFIED**) | docs/05 §4.1; `ma.chemistries.alp_hqdp.hydrolysis_rate` |
| HQ (product) half-life at pH 9.5 in air | 2 h (0.5–20 h), **UNVERIFIED** | `ma.chemistries.alp_hqdp.product_half_life` |
| **Storage consequence (Derived)** | at the acceptance limit k_h = 10⁻⁹ s⁻¹, a stored 1 mM solution gains 8.6×10⁻⁵ mol/mol of HQ per day before oxidation — about **9× the free-HQ acceptance limit** in one day; with HQ oxidising at t½ 2 h the steady state is ≈ k_h × t½/ln2 ≈ 1×10⁻⁵ mol/mol. At the nominal 10⁻¹⁰ s⁻¹ it is 8.6×10⁻⁶ per day. Liquid HQDP stored on a cartridge for days is therefore near or above the free-HQ limit unless k_h is at the nominal value or below, or the substrate is cooled, kept dry and dissolved on demand, or measured per run. The model does not represent this storage term for stopped-flow schemes (§5.4) | Derived from the two rows above |
| Measured stability horizon | E1.2: 0, 1, 2, 4, 8, 24, 30 h at 22 °C in amber glass, PEEK, B1 bottle, and pumped through the BSM; sealed N₂-purged control | docs/06 E1.2; docs/08 S11 |
| Light / oxygen | amber vials, dark; oxygen role tested by the N₂ arm | docs/06 E1.2 |
| Supply | Metrohm DropSens DRP-HQDP-0.5G; **no purity or free-HQ specification published**; single supplier; commercial availability flagged UNVERIFIED in `chem.substrates.HQDP_and_HQP.commercial_availability_HQDP` | docs/07 §1.1; docs/08 W9 |
| Alternatives | p-hydroxyphenyl phosphate (one Pi per HQ, halves the phosphate that sets the ULOQ; no supplier found); 4-aminophenyl phosphate (fouling product); ascorbic-acid 2-phosphate (irreversible product, no IDA cycling) | docs/08 W9; `ma.chemistries.alp_papp`, `alp_aap`; `chem.substrates.pAP.fouling` |

### 3.4 Buffers and the phosphate issue

| Item | Value | Source |
|---|---|---|
| Wash/running buffer (A1) | TBS (50 mM Tris-HCl pH 7.4, 150 mM NaCl) + 0.05 % Tween-20, no protein, no phosphate | docs/05 §4.1; docs/06 §4.0 |
| Assay buffer (reagent diluent) | the same + 1 % IgG-free BSA, 0.22 µm filtered, no azide | docs/06 §4.0 |
| Gen-1 wash consumption per determination | BSM A1 ≈ 4.4 mL (Derived: 300 µL to t = 3, 3000 µL during incubation shunt, 6.6 µL during trap loading, 100 µL wash, 900 µL clean); SIA wash 50 µL channel flush + cup rinses (volume not stated) + 653 µL cup emptying (part is sample) | `cycle_primary.yaml` |
| Phosphate inhibition of ALP | K_i 2 µM nominal, **UNVERIFIED for calf-intestinal ALP at pH 9.5**, bounds 0.2 µM–1 mM (final-review override); competitive | `ma.overrides` `chem.enzymes.alp.phosphate_inhibition_Ki`; docs/08 §9 C4 |
| Size of the effect | 0.5 mM phosphate (a few µL of PBS left on beads in 50 µL of substrate) takes v/V from 0.75 to ≈ 0.01 at S 0.3 mM | docs/08 B1 |
| Tolerable residual phosphate (Derived) | at S = 1 mM, K_m 0.1 mM (`ma.chemistries.alp_hqdp.Km`, **UNVERIFIED**), K_i 2 µM: 1 µM Pi lowers the rate by ≈ 4 %, 10 µM by ≈ 30 %. Target ≤ 1 µM in the accumulation volume from all sources other than the reaction itself (stored reagents, bead stock, carry-in) | Derived (competitive Michaelis–Menten) |
| Phosphate made by the reaction | HQDP releases 2 Pi per HQ (`ma.chemistries.alp_hqdp.phosphate_per_product`); this sets the upper end of the range. Nominal ULOQ of the primary at 1 mM HQDP: 5200 pg/mL at K_i 2 µM, 2300 at 1 µM, 460 at 0.2 µM. **A smaller accumulation volume concentrates both product and phosphate**, so it raises signal per enzyme but lowers the ULOQ unless HQDP is raised or accumulation shortened | `ma.overrides` note; docs/05 §1.5; model `kinetics.enzyme_accumulation` |

### 3.5 Other reagents (only for some formats)

| Reagent | Format | Value | Source |
|---|---|---|---|
| Glycine-HCl pH 2 | regenerated fixed bed / wall capture | 100 µL injection; 2 min elution + re-equilibration (6.5 min step); pH 2 is the I-Class BSM limit, so inject or store on cartridge | docs/05 §4.2; `chem.regeneration.elution_glycine_HCl_pH`; `hw.bsm.ph_min` |
| Desthiobiotin capture antibody + 2 mM biotin elution + phase-2 beads | lever L4 (immune-complex transfer) | +5–10 min; NSB ×0.1 (0.01–0.5), signal ×0.7 (0.4–0.9), both **UNVERIFIED** | docs/05 §2 L4, §5 U8; `ma.design_levers.immune_complex_transfer_*` |
| Tween 0.05–0.1 % stringent wash | if NSB is partly reversible (S3a) | +1–2 min | docs/05 §2 |
| Mouse serum / blocking additives | detection-on-capture suppression | not specified | docs/08 §9 C1 (Qu1998 mechanism only) |

### 3.6 Sizing a cartridge for N determinations (template)

Per determination (one-step gen-1 equivalents): 5×10⁵ beads in 10 µL; 66 fmol conjugate in 10 µL; HQDP ≥ the
accumulation volume plus fill and baseline volumes (gen-1 uses ≈ 315 µL from the BSM); wash as needed (gen-1:
≈ 4.4 mL from the BSM, most of it shunted to waste during incubation). For N runs add: controls (2 per 10 samples,
F18); one recovery cycle per expected fault (F17); priming and dead volume of every store (not specified anywhere
in the repository); the conjugate store's maximum life (default 8 h, docs/07 §5.5); bead suspension mixing losses.
Waste per determination in gen-1 is ≈ 5–6 mL (Derived: A1 ≈ 4.4 mL + B1 ≈ 0.3 mL + SIA volumes), dominated by
the incubation shunt; a cartridge that does not shunt the BSM during incubation needs far less.

(Sections 4–6 follow.)
