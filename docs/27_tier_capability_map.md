# 27 — Capability map: what the equipment in hand can do without added hardware, and the modelling map

Status: 2026-11-17. Written by the orchestrator from docs/02 (hardware), a fact-check of the Waters stack made in
this round by an agent (Appendix A, sources opened in the session) and calculations with `scripts/tier_round/`.
Scope: tiers 1 and 2 of docs/26 (no valves, no added pump). Tier 3 may add anything; section 7 points to what
docs/02, docs/05, docs/07 and docs/13 already specify.

Evidence labels as in docs/02: **[V]** checked in this session against the cited document; **[S]** search summary
only; **UNVERIFIED**; **Derived** (formula or script given). Keys in square brackets (K8407, OG, …) resolve in
Appendix A; docs/28 holds the MicruX references.

## 1. Flow path and volumes

```
BSM (A1/A2, B1/B2) -> mixer 50 uL -> restrictor -> SM-FL injection valve (100 uL loop, in line from Inject Start
to Loop Offline) -> transfer tubing -> [tier 2: capture bed] -> MicruX wall-jet cell (electrode) -> waste
```

| Segment | Volume | Source |
|---|---|---|
| BSM to injector, composition step A -> B | < 100 µL system delay (default configuration) | docs/02 §1.1 [V there] |
| A1 <-> A2 or B1 <-> B2 line change | pump head and mixer must be flushed; not used inside a determination | docs/02 §1.2 |
| Sample loop | 100 µL; 0.5 mm I.D. assumed | docs/00; `hw.smfl.loop_inner_diameter` (UNVERIFIED I.D.) |
| Transfer tubing injector -> cell, 0.127 mm I.D. × 0.2 m | 2.5 µL | Derived (πr²L) |
| Inlet bore of the cell | 0.8 mm I.D. (strip cell) or 0.5 mm I.D. (thin-film cell); length not published, 5 mm assumed: 2.5 µL or 1.0 µL | docs/28 §1 [V for the bore diameter]; length UNVERIFIED |
| Cell chamber | < 5 µL (strip cell, 8 mm O-ring) or < 0.5 µL (thin-film cell, 2 mm O-ring) per the vendor; the user states 10 µL | docs/28 §1 |

A composition step therefore needs 100–200 µL of flow before the cell sees the new liquid at full strength (delay
plus mixer wash-out; Derived): 1.3–2.5 min at 80 µL/min. Buffer changes are done at 50–80 µL/min, never at the
loading flow.

## 2. What the pump can and cannot do

| Question | Answer | Evidence |
|---|---|---|
| Minimum programmable flow | 0.010 mL/min on the I-Class in vendor documents; 0.001 mL/min on Premier and, per a search summary, on I-Class PLUS with firmware ≥ 1.71. The user states 1 µL/min for this instrument (docs/00) | [V K8407, ICspec, PRspec]; [S] for I-Class PLUS |
| Flow accuracy and pulsation below 0.2 mL/min | not specified by Waters | [V ICspec, PRspec] (absence) |
| A 0.000 mL/min row in a method (programmed stop) | **not settled.** No Waters text allows or forbids it. The console accepts 0.000 and has a Stop Flow button only when idle; the rear "Stop Flow In" input is a fault input that ends the run | [V OGE]; [S WKB92593]; Appendix A.1 |
| Low-pressure limit during low-flow steps | must stay at 0 or the pump shuts down | [V K30741] |
| Flow between two sample-set lines | follows the pre-run or post-run method if one is set; that a plain sample set idles at the next method's initial conditions is standard behaviour but UNVERIFIED | [V K21855] |
| Long methods with many flow steps | no stated limit; 85–93 min gradients are in Waters application notes | [S]; Appendix A.4 |
| Timed contact closures to the outside | original ACQUITY: BSM Switch 1–3 Out, sample manager Inject Start Out and Switch 1–4 Out, Inject Hold In; count on the I-Class PLUS UNVERIFIED | [V OG]; docs/02 §3 |

**Consequences.**
* A design must not depend on stopping the flow unless it names its fallback. Tier 1 reads the electrode while
  substrate flows at the pump's minimum, so it never needs a stop. Tier 2 needs one stop of 7 min (product
  accumulation in the bed); its fallback is a continuous read at the minimum flow (docs/30 §4.6). Tier 3 uses a
  valve and does not need the pump to stop.
* After a stop the liquid upstream of the restrictor relaxes through it. With about 0.4 mL at 1000 psi the stored
  volume is V·β·ΔP ≈ 1.3 µL and the time constant R·C ≈ 8 s (Derived: water compressibility 4.6×10⁻¹⁰ Pa⁻¹,
  restrictor 1000 psi at 10 µL/min; the 0.4 mL is UNVERIFIED). About 1 µL creeps through the cell in the first
  20 s of a stop. This matters for a 0.1 µL product plug (tier 2: the accumulation starts when the creep has ended)
  and not for tier 1.

## 3. Restrictor and pressure window

Waters: the check valves need back-pressure, "generally above 1000 psi", to work efficiently over their life
[V K32564]; no effect on flow accuracy is stated. The Waters restrictor (40 µm × 35 cm PEEK-SIL, kit 205000547) sits
between mixer and injector [V K5084], so the injector, the bed and the cell see only their own resistance. With one
fixed restrictor, pressure is proportional to flow (Hagen–Poiseuille, water, 25 °C, Derived):

| Restrictor | psi per µL/min | 1 µL/min | 3.25 µL/min | 50 µL/min | 80 µL/min | Highest flow (18 000 psi) |
|---|---|---|---|---|---|---|
| 40 µm × 35 cm (Waters kit) | 12 | 12 psi | 39 psi | 600 psi | 960 psi | 1500 µL/min |
| 25 µm × 45 cm | 100 | 100 psi | 330 psi | 5000 psi | 8100 psi | 180 µL/min |
| 20 µm × 45 cm | 250 | 250 psi | 800 psi | 12 300 psi | (19 800 psi, over) | 73 µL/min |

No single restrictor keeps 1000 psi at 1–3 µL/min and stays below the limit at the flush flows. The designs use
**25 µm × 45 cm** (availability of this size UNVERIFIED) and accept 100–330 psi during loading and reading; flushes
run at 50–80 µL/min. Whether the BSM delivers a steady 1–3 µL/min at such pressures is the first instrument fact to
measure (section 8, item 1). If it does not, the fallback is the 20 µm restrictor with flushes at ≤ 70 µL/min.

Pressure at the cell: the MicruX add-ons are PMMA held by magnets on an O-ring and have no stated pressure limit
(docs/28 §1). Downstream of the cell only a short open waste line. The tier-2 bed adds 1.1 bar at 3.5 µL/min and
about 25 bar at 80 µL/min upstream of the cell (Kozeny–Carman, `tierkit.kozeny_carman_dp`; 1×10⁶ beads of 2.8 µm in
a 0.2 mm bore); its fittings must be PEEK, not the vendor's polypropylene nuts.

## 4. What the autosampler contributes

* One vial per injection; no in-needle mixing, no reagent addition to a vial (docs/02 §2.3). Sample and reagents are
  separate injections, each a sample-set line with its own method. Zones of consecutive injections do not mix: two
  100 µL zones overlap by about 10 % at their boundary (docs/29 B.5). **Tiers 1 and 2 are therefore sequential
  sandwiches:** sample first, conjugate second. A simultaneous (one-step) incubation needs added hardware (docs/05
  §4.0).
* Per-line overhead about 1 min (aspirate, wash, load; docs/02 §2.2, UNVERIFIED); Load Ahead is not used between
  lines with different methods [V OG], so every reagent line pays it.
* Sample: one full-loop 100 µL injection. The Waters default for full loop draws the sample volume plus four times
  that (about 500 µL) [V K198538]; docs/00 records the user's setting of 2× overfill (about 200 µL drawn). The setting
  on this instrument should be read off the method (section 8, item 6).
* Moving the sample out of the loop is slow for a protein. Fraction of a full 100 µL IgG plug that has left a
  0.5 mm I.D. loop (`elisa_sim.transport.loop_transfer_interp`, as used by the model):

  | Flow (µL/min) | 1.0 loop volume | 1.2 | 1.5 | 2.0 | 3.0 |
  |---|---|---|---|---|---|
  | 3.25 | 0.93 | 0.98 | 1.00 | 1.00 | 1.00 |
  | 5 | 0.91 | 0.97 | 1.00 | 1.00 | 1.00 |
  | 10 | 0.88 | 0.94 | 0.99 | 1.00 | 1.00 |
  | 20 | 0.84 | 0.91 | 0.97 | 1.00 | 1.00 |
  | 50 | 0.80 | 0.86 | 0.93 | 0.98 | 1.00 |
  | 100 | 0.78 | 0.83 | 0.90 | 0.96 | 1.00 |

  At the slow loading flows of this round radial diffusion keeps the plug compact: 1.2 loop volumes (120 µL) move
  98 % of the sample. This is what lets a 100 µL sample be pumped at 3–5 µL/min inside 60 min.
* Reagent injections: full loop (100 µL) or partial loop with needle overfill, 10–75 µL [V OGE, PRspec]. The designs
  inject the conjugate as a full loop: no dilution at the plug centre, and the 200 µL drawn costs little at 3–10 nM.
* Proteins and beads never go through the pump lines (docs/02 §1.2). Beads are not injected through the SM-FL
  either: no report of bead suspensions through an ACQUITY fixed-loop sampler was found, and 2.8 µm beads settle at
  about 6 mm/h in a vial (docs/29 B.7). Capture beads are packed by hand before the run.
* Conjugate left in needle and loop reaches the next determination's sample injection; the model carries it as
  `hw.smfl.carryover_protein_conjugate` squared (two injections apart). A blank line with a full-loop wash injection
  between determinations costs 2 min and is in the step tables' pre-run.

## 5. Electrochemistry on the one channel

* Reference 600+: chronoamperometry, pulse and stripping techniques, 60 pA lowest range, floating operation (docs/02
  §4). Realistic current noise 1 pA rms stopped and 3 pA rms in flow at a 3 mm carbon electrode, drift 1–10 pA/min
  (docs/02 §4.5; all UNVERIFIED model values). The designs read by **holding the potential and integrating the
  current**; potential steps and pulse techniques are avoided because the charging and surface charge of a step
  (about 1 µC on a 3 mm printed electrode) is 10³ times the signal at the LOD (docs/29 A.4).
* Start and marks: SM-FL Inject Start contact closure into the Python layer (`automation/elisa_auto/watch_inject.py`),
  which runs the Gamry worker; one timed BSM or sample-manager switch marks the read window.
* Redox cycling needs either a reductant in solution (shown only on ITO and SAM-covered gold, docs/29 A.2) or two
  working electrodes. A one-channel two-electrode connection of an interdigitated array has no verified example for
  an enzyme product (docs/29 A.3), and MicruX states only 2–3× for its arrays in open cells (docs/28 §2.2). Neither
  is used in tiers 1 and 2.
* The printed strips with a carbon working electrode exist with a printed Ag/AgCl reference (S1PE-C21, -CG21); the
  thin-film chips have a gold or platinum pseudo-reference. Every solution that reaches the cell carries the same
  chloride (0.15 M), so the printed reference does not move when the substrate arrives (docs/28 §4).

## 6. Operations available to the three tiers

| Operation | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Pump sample through the capture zone at 3–5 µL/min | yes | yes | yes |
| Simultaneous incubation of sample, capture phase and conjugate | no | no | yes, with a dosing pump and chamber (docs/05 §4.1) |
| Hold a reagent on the capture zone | only if the pump accepts a zero-flow row; otherwise pass it slowly | the same | yes (valve) |
| Keep conjugate away from the electrode | no: everything injected passes through the cell | no | yes (cell bypass) |
| Accumulate product, then read | not needed (read at the electrode) | needs the zero-flow row; fallback continuous read | yes (bed isolated by a valve) |
| Second, clean capture phase (immune-complex transfer) | no | no | yes |
| Reference electrode or reference bed read in the same run | no | no | yes, with a second channel |

## 7. Tier 3: where the added hardware is already specified

| Addition | Where |
|---|---|
| 2-position 6-port and 10-port PEEK valves (IDEX MX Series II), serial control | docs/07 §2 [V there]; docs/02 §7 |
| Dosing pump with selection valve, stirred incubation chamber, magnetic trap | docs/05 §4.1; docs/07 §2 |
| Second potentiostat channel | docs/02 §5.1 (Gamry pairing with a 600+ UNVERIFIED); docs/28 §7: MicruX ECStat bipotentiostat plugs into the cell [V] |
| Interdigitated arrays for redox cycling | docs/28 §2.2 (MicruX IDA1/5/6); docs/02 §5; gain only when confined in a thin layer (docs/29 A.3) |
| Immune-complex transfer chemistry and its tube experiment | docs/05 §2 (L4), docs/06 §4.12 (Stage 1C) |

## 8. Modelling map

The audited model (`src/elisa_sim`, docs/03, docs/04) covers bead and packed-bed formats behind valves. For the
valve-less formats this round adds `scripts/tier_round/tierkit.py`, which reuses the model's parameters, kinetics,
loop transfer, slit solution, bed correlation and blank statistics, and adds what was missing:

| Step | Function | Parameters the LOD leans on (value [low–high], confidence) |
|---|---|---|
| Sample out of the loop | `elisa_sim.transport.loop_transfer_interp` | `ma.delivery.adsorptive_loss_fraction_with_carrier` 0.2 [0.02–0.6], low |
| Capture on the electrode under the wall jet | `tierkit.cell_conversion` (radial thin gap = slit solution in the swept area; checked against an independent Lighthill–Lévêque result, README) | `chem.antibodies.kon_capture` 3×10⁵ M⁻¹s⁻¹ [0.9–12×10⁵], medium; site density 1×10¹⁶ m⁻² × 0.85, medium; gap height (design input, UNVERIFIED) |
| Capture in a bed | `elisa_sim.transport.wilson_geankoplis_k`, `tierkit.evaluate_bed` | as above; bed is reaction-limited |
| Labelling and dissociation | `elisa_sim.kinetics.reversible_binding_fraction` | `chem.antibodies.koff_detection` 8.6×10⁻⁴ s⁻¹ [3×10⁻⁶–8.3×10⁻³], medium: the largest single sensitivity in all three tiers |
| Non-specific label | rate × label factor × surface factor × area × exposure | `chem.nsb.nsb_effective_rate_constant` 4×10⁻¹¹ m/s [0.8–40×10⁻¹¹], low; `ma.nsb.label_factor_igg_enzyme_conjugate` 0.04 [0.01–0.15], low; surface factors of electrode, lid, retainer (`tr.nsb.*`, 1–100, UNVERIFIED) |
| Enzyme turnover | `elisa_sim.kinetics.enzyme_accumulation` | `chem.enzymes.alp.kcat_conjugate_assay_conditions` 1000 s⁻¹ [100–6000], low |
| Product to the electrode in the stopped cell | `tierkit.ThinLayer` (axisymmetric finite volumes: electrode disc, lid, inlet bore) | hydroquinone diffusion coefficient 9×10⁻¹⁰ m²/s, held at its best estimate |
| Product swept over the electrode | `tierkit.cell_conversion`, `elisa_sim.transport.tanks_in_series_eluted` | — |
| Substrate background | impurity and hydrolysis, referenced by a pre-read on the same electrode | `ma.chemistries.alp_hqdp.free_product_impurity` 1×10⁻⁵ [10⁻⁷–10⁻³], low; hydrolysis 10⁻¹⁰ s⁻¹ [10⁻¹²–10⁻⁸], low |
| Noise, drift, unit-to-unit terms | `tierkit._finish` (docs/03 §3.6 plus single-use terms) | `hw.gamry.*` noise and drift, low; `ma.noise.spe_sensor_to_sensor_cv` 0.10; `tr.noise.*`, `tr.nsb.unit_to_unit_cv_*` (UNVERIFIED) |

Not represented, to be read with care: mixing in the stagnation zone under the jet; bypass through an unevenly packed
bed; the effect of the conjugate plug's dispersion on its exposure (the exposure integral is exact, the labelling is
computed at the mean concentration); wash efficiency (washes are fixed at ≥ 1.5 min and ≥ 2 min as in docs/05 §1.1);
electrode fouling by protein (single-use electrodes); temperature.

## 9. Instrument facts to check before the first run (bench Stage 0 of this round)

1. **Low flow.** Gravimetric flow at 1, 3 and 10 µL/min behind the chosen restrictor, 30 min each, with the pressure
   trace. Pass: mean within 5 %, no pressure ripple visible in the amperometric baseline.
2. **Zero-flow row.** Enter 0.000 mL/min as a gradient-table row with a 5 min hold between two 0.010 mL/min rows;
   record whether the editor accepts it, whether the run completes and how the pressure decays.
3. **Between lines.** Run two lines with different methods (3 µL/min, then 50 µL/min) and log flow, pressure and the
   time from the end of line 1 to Inject Start of line 2.
4. **Cell geometry.** Measure the gap of the mounted add-on (feeler or O-ring cross-section and recess depth), the
   bore length and where the outlet sits; weigh the cell dry and filled (docs/28 §8).
5. **Cell pressure.** Step the flow to 100 µL/min with a spare electrode and look for leaks at the O-ring.
6. **Full-loop draw.** Read the overfill factor in the SM-FL method; weigh a vial before and after one injection.
7. **Outputs.** Photograph the rear terminal blocks of the BSM and SM-FL; list the switches in the Events tab.
8. **Reference.** Open-circuit potential of the strip's printed Ag/AgCl and of the chip's gold pseudo-reference
   against a laboratory Ag/AgCl electrode in wash buffer and in substrate buffer, over 1 h.

---

## Appendix A — Fact-check of the Waters stack (agent report, 2026-11-17)

Written 2026-11-17 for the tier round (docs/26). Scope: ACQUITY UPLC I-Class PLUS, BSM + SM-FL (100 µL loop).
Evidence labels: [V] opened this session; [S] search summary only; UNVERIFIED; Derived.
Facts already held in docs/02 are not re-derived (see the task statement).


### A.Sources opened this session (short keys used below)
- [K8407] WKB8407, I-Class min/max flow: https://support.waters.com/KB_Inst/Chromatography/WKB8407_What_is_the_minimum_and_maximum_flowrate_limit_on_ACQUITY_I-Class — opened [V].
- [K21855] WKB21855, flow between runs (H-Class, MassLynx): https://support.waters.com/KB_Inf/MassLynx/WKB21855_The_flow_rate_changes_from_what_is_in_the_method_in_between_runs_on_an_ACQUITY_H-Class_in_MassLynx — opened [V].
- [ICspec] ACQUITY UPLC I-Class System (SM-FTN) specification, Waters 720003948EN (2015), copy at https://ucrf.unist.ac.kr/wp-content/uploads/2024/11/ACQ.-I-Class-PLUS-Sys.-CH-A-wSM-FTN-I-Specification.pdf — full text [V].
- [PRspec] ACQUITY Premier System specification, Waters 720007029EN (2022), https://kr-support.waters.com/@api/deki/files/20438/Premier_specs_720007029en.pdf?revision=1 — full text [V]. Premier, not I-Class PLUS: same BSM/SM-FL family, used as nearest vendor text.
- The I-Class PLUS specification 720006149 (waters.com) returned "Access Denied"/503 here; its contents are [S] only.
- [K5084] WKB5084 restrictor: https://support.waters.com/KB_Inst/Chromatography/WKB5084_What_is_the_part_number_for_the_flow_restrictor_used_to_increase_system_backpressure_on_the_ACQUITY_BSM_or_H-Class_QSM — opened [V].
- [K32564] WKB32564 minimum back-pressure: https://support.waters.com/KB_Inst/Chromatography/WKB32564_What_is_the_minimun_backpressure_required_for_good_UPLC_performance — opened [V].
- [K30741] WKB30741 low-pressure limit: https://support.waters.com/KB_Inst/Chromatography/WKB30741_What_is_the_low_pressure_limit_in_an_Acquity_instrument_method — opened [V].
- [K198538] WKB198538 full-loop sample consumption, ACQUITY SM and I-Class SM-FL: https://support.waters.com/KB_Inst/Chromatography/WKB198538_How_much_sample_is_consumed_in_Full_Loop_Mode_for_the_ACQUITY_UPLC_Sample_Manager_and_ACQUITY_UPLC_I-Class_Sample_Manager_FL — opened [V].
- [OG] ACQUITY UPLC System Operator's Guide 71500082502 Rev C (2006, original ACQUITY BSM + fixed-loop SM, the SM-FL's predecessor), copy at https://acmerevival.com/wp-content/uploads/2021/08/ACQUITY-UPLC-System-Operators-Guide-.pdf — full text [V] (pp. 1-5 to 1-7, 2-37 to 2-41, 3-22 to 3-25).
- [OGE] Same guide, Revision E (2010), copy at https://condor.depaul.edu/jmaresh/instruments/Instruments/HPLC/UPLC%20manual.pdf — full text [V] (sections 3-25, 4-4, Equilibrate to Method, Conditioning the column).
- Not reachable here: forums.waters.com (DNS blocked in this session), help.waters.com and waters.com PDFs (503 / Access Denied), incl. the BSM PLUS Overview and Maintenance Guide 715005706 v04.

Caveat on [OG]/[OGE]: they describe the original ACQUITY (2004-2010), not the I-Class PLUS. They are the nearest
Waters text found for control-panel limits, rear-panel I/O and injection modes. Each answer says where the I-Class
PLUS may differ.

### A.1. Can the method stop the flow (0.000 mL/min step)?
- No Waters text found that allows or forbids 0.000 mL/min as a gradient-table row. Not found in WKBs, specs or guides.
- The documented settable range is 0.010-2.000 mL/min in 0.001 mL/min steps (I-Class) [V, K8407, ICspec]; Premier and,
  per search summary, I-Class PLUS with firmware >= 1.71: 0.001-2.000 mL/min [V PRspec; S for I-Class PLUS 720006149].
- The BSM console control panel accepts 0.000-2.000 mL/min when idle and has a Stop Flow button [V, OGE p. 4-4]. That
  is manual console control, not a method row.
- A hardware "Stop Flow In" contact input exists on the BSM rear panel, meant to halt flow on another instrument's
  error [V, OG p. 2-38]. In practice it raises a "Stop flow input activated" error and halts the run [S, WKB108155,
  WKB92593: https://support.waters.com/KB_Inst/Mass_Spectrometry/WKB92593_Acquity_BSM_stop_flow_input_activated_error].
  It is a fault input, not a stop/resume step: not usable as a programmed hold.
- If a 0 or near-0 step works, the method's low-pressure limit must stay at 0 (its default), or the pump shuts down
  when pressure falls below it [V, K30741].
- Bench test: in Empower, enter 0.000 mL/min in a BSM gradient row (with a 1 min hold, then 0.010). Record whether the
  editor accepts it, whether the run completes, and the pressure trace. Fallback: hold at the lowest accepted value
  (0.001 or 0.010 mL/min = 1 or 10 µL/min).

### A.2. Real minimum flow; accuracy and pulsation below 0.2 mL/min
- Settable minimum: 0.010 mL/min (I-Class, older firmware) or 0.001 mL/min (Premier; I-Class PLUS fw >= 1.71)
  [V K8407, ICspec, PRspec; S for I-Class PLUS]. The user's statement of 1 µL/min fits the second value.
- Flow accuracy is specified only at 0.500 mL/min (±1.0 %); flow precision (0.075 % RSD) and composition specs only
  from 0.2 to 2.0 mL/min [V ICspec, PRspec]. No Waters statement found on accuracy or pulsation at 1-100 µL/min.
- Older text calls the BSM flow "steady (pulse-free) at analytical flow rates" [V OG p. 1-6]; no number.
- Bench test: timed gravimetric collection (>= 30 min, sealed vial, 0.01 mg balance) at 1, 3, 10, 30 µL/min behind
  the chosen restrictor; log the BSM pressure trace (analog out, see Q5) for ripple. Accept if mean error < 5 % and
  ripple does not show in the amperometric baseline.

### A.3. Pump behaviour between sample-set lines
- Between runs the flow follows whatever the pre-/post-run inlet method sets; if none, the method conditions continue.
  Waters fixes an unexpected between-run flow by deleting the Prerun/Postrun inlet method [V K21855; MassLynx, H-Class].
  That a plain Empower sample set idles at the next method's initial flow and composition: UNVERIFIED (standard
  behaviour, no Waters text opened).
- Empower sample sets can hold an "Equilibrate/Condition Column" function row, run at a method's conditions without
  injection or events; its run time equals the gradient-table run time [V OGE, Conditioning the column].
  The system-startup "Equilibrate to Method" tab allows 0.1-2.0 mL/min only [V OGE] (original ACQUITY).
- Load Ahead is not used for the first injection of a set nor between lines with different methods [V OG p. 3-23,
  OGE]. Every reagent line with its own method therefore pays full sample-preparation time before injection.
- FL cycle time "≤15 s inject-to-inject" [V PRspec; Premier, conditions not stated].
- Bench test: run two lines with different methods (10 µL/min, then 1 µL/min) and log flow, pressure and the time from
  end of run 1 to Inject Start of run 2.

### A.4. Several flow steps and long low-flow holds in one method
- Specs list 11 gradient curves (linear, 2 step, 4 concave, 4 convex) [V ICspec]. No Waters text found on the maximum
  number of gradient-table rows or the maximum run time. Waters application notes run 85-93 min gradients on
  I-Class PLUS / H-Class PLUS [S; https://www.waters.com/nextgen/en/library/application-notes/2018/acquity-uplc-i-class-plus-system-methods-employ-long-shallow-gradients.html].
  A 60 min method is therefore within ordinary use.
- Bench test: build a BSM method with 25 rows (flow steps 0.010 -> 0.001 -> 0.200 mL/min, 30 min hold) and save it;
  the editor's limit, if any, shows at row entry.

### A.5. Timed outputs a potentiostat can read
- Original ACQUITY rear panels [V OG pp. 2-37 to 2-41]:
  | Module | Outputs | Inputs |
  |---|---|---|
  | BSM | Switch 1-3 Out (time-based contact closures), Run Stopped Out, two 0-2 V analog outs (flow, pressure, %A/%B) | Start Gradient In, Stop Flow In |
  | Sample manager | Inject Start Out, Switch 1-4 Out, Run Stopped Out, 0-2 V analog out | Inject Hold In |
- Switches are set On/Off/Pulse at times in the instrument method's Events table [S; nanoACQUITY protocol
  https://tephra.gs.washington.edu/docs/protocols05/QEplus_nanoAcquity_ContactClosure.pdf; WKB3148].
- I-Class PLUS: spec says only "rear panel contact closure and/or TTL inputs/outputs" [V PRspec, ICspec]; the count of
  switches on the I-Class BSM and SM-FL is UNVERIFIED. Inject Start on the SM is in docs/02 (WKB55803).
- Use: Inject Start -> Gamry digital input (t = 0); one timed BSM or SM switch -> second Gamry input to mark the
  stop-flow/read window. "Inject Hold In" lets an outside device delay an injection [V OG] (tier 3 handshake).
- Bench/vendor check: photograph the I-Class PLUS BSM and SM-FL rear terminal blocks; open the Events tab in Empower.

### A.6. Running below 1000 psi; restrictor placement
- Waters: check valves "require a certain level of back pressure to operate efficiently over their life cycle";
  "generally ... above 1000 psi" [V K32564]. No consequence for flow accuracy is stated; the stated risk is wear.
- Waters restrictor kit 205000547: 40 µm x 35 cm PEEK-SIL, installed "between the solvent manager mixer and the sample
  manager injector", adds "> 2000 psi on average" (flow not stated) [V K5084]. So yes: upstream of the injector is
  Waters' own placement, out of the sample path.
- Derived (Hagen-Poiseuille, ΔP = 128 µ L Q / (π d⁴), water µ = 0.89 mPa s, 25 °C):
  | Restrictor | 1 µL/min | 10 µL/min | 200 µL/min |
  |---|---|---|---|
  | 40 µm x 35 cm (kit) | 12 psi | 120 psi | 2400 psi |
  | 25 µm x 45 cm | 100 psi | 1010 psi | 20 000 psi (over limit) |
  | 15 µm x 58 cm | 1000 psi | 10 000 psi | over limit |
  The kit gives < 1000 psi below about 85 µL/min. A restrictor sized for 1000 psi at the hold flow caps every flush
  at about 18x that flow (18 000 psi limit [V ICspec]). Low-flow holds and fast flushes conflict; choose per tier.
  Part availability for 15-25 µm ID PEEK-SIL lengths: UNVERIFIED.
- Bench test: run 1-10 µL/min with and without the restrictor and compare gravimetric flow (Q2); record whether the
  BSM reports pressure ripple or prime loss.

### A.7. Particles through the SM-FL
- Needle and tubing IDs of the SM-FL: not found. Part numbers seen: needle carriage 700006065, optional 10 µL steel
  needle 700005924 [S; WKB101960 and waters.com shop]. The standard needle volume is 15 µL in one WKB example [S, WKB9454].
- No in-line filter between needle and loop is mentioned in any opened text; the sample path is needle -> injection
  valve -> loop [V OG p. 1-7]. UNVERIFIED that none exists in the SM-FL.
- Waters ties SM-FL "Sample fluidics over pressure" errors to clogged loops or needles (debris, precipitate) and advises
  automatic needle placement to avoid aspirating debris [S, WKB7433, WKB27524].
- No report found of bead suspensions injected through an ACQUITY fixed-loop sampler. A Waters protein-A bead note
  added measures (a magnet under the plate) to keep beads out of the LC [S, app note 720007343].
- Bench test: 50 x full-loop injections of the chosen bead suspension (e.g. 1 µm, 1 mg/mL) with sample-pressure
  logging; count beads delivered vs drawn (hemocytometer) and inspect carry-over in a following blank.

### A.8. Full loop on 100 µL; partial-loop reagent injections
- Default full-loop draw on the FL samplers: "the sample volume plus four times the sample volume" [V K198538], i.e.
  5 x 100 = 500 µL drawn per 100 µL full-loop injection by default. This contradicts docs/02's 2x / ~200 µL unless
  the overfill factor is set lower. The factor is settable (forum: up to 25x in newer drivers) [S, forums.waters.com
  not reachable]; whether 2x is accepted: UNVERIFIED. Vendor/bench: open SM-FL method > Advanced, set overfill 2x.
- Modes: Full Loop, Partial Loop, Partial Loop with Needle Overfill (PLUNO, default) [V PRspec, OG].
- PLUNO: optimum 10-75 % of measured loop volume [V OGE p. 3-25]; SM-FL linearity spec 20-75 % of loop [V PRspec].
  On a 100 µL loop: 10-75 µL (20-75 µL inside the linearity spec). Partial Loop: <= 50 % (<= 50 µL) [V OG].
  PLUNO draws injection volume plus a fixed overfill (15 µL default, needle-dependent) [S, WKB11277].
- Injection volume range 0.1-250 µL; loops 1-250 µL [V PRspec]. Loop changes are a hardware swap, so reagent and sample
  injections share the 100 µL loop.
- Bench test: gravimetric draw per injection at full-loop 2x and PLUNO 10/50/75 µL; dye injection into the cell for
  delivered fraction.

### A.Remaining UNVERIFIED (summary)
0 mL/min method row; I-Class PLUS minimum flow and switch count; flow accuracy below 0.2 mL/min; gradient-row limit;
idle flow between Empower lines; SM-FL needle/tubing IDs and internal filters; bead injection; full-loop overfill 2x.
