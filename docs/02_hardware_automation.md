# 02 — Hardware, fluidics and automation

Task 2 of the automated electrochemical ELISA project (human IgG in buffer, LOD ≤ 1 pg/mL, ≤ 100 µL sample,
≤ 60 min, reusable capture surface). Scope: instruments, fluidics, flow cells, capture reactors, control and
synchronisation. Chemistry and immunology (antibodies, label, substrate kinetics) belong to the parallel
literature task (`docs/01_literature_parameters.md`, `params/chemistry.yaml`) and appear here only where they
constrain hardware.

Machine-readable parameters for the simulation: `params/hardware.yaml`. Every `source` key there matches a key
in the reference list (§9).

**Evidence labels used in this document**

| Label | Meaning |
|---|---|
| **[V]** | Checked in this session against the cited document (spec sheet, manual page, knowledge-base article, PubMed record). |
| **[S]** | Taken from a search-engine summary of the cited page; the page itself could not be opened. Medium confidence. |
| **[P]** | Carried over from the previous (interrupted) draft, which reported it as checked; **not re-checked in this session**. Medium confidence. |
| **UNVERIFIED** | Not checked against any source (engineering estimate). Must be confirmed before anyone relies on it. |
| **Derived** | Calculated here from cited inputs; formula or script given. |

> **Note on the sample manager (correction of the inherited draft).** The previous draft was written under a
> wrong instruction that the sampler is a flow-through-needle (FTN) design, in which the needle and an
> extension loop sit permanently in the high-pressure flow path. The fixed equipment is the **ACQUITY SM-FL
> (Sample Manager – Fixed Loop)**. In the SM-FL the sample is aspirated by a syringe through a sample needle
> and pushed into a **fixed sample loop on a 6-port injection valve**; the needle is never in the
> high-pressure flow path, and the loop is in the flow path only while the valve is in the inject position
> [V: WAT_INJ_MODES; P: MANUALSLIB_ICLASS]. Every statement about sampling, injection volumes, carryover,
> dwell volume, dispersion, adsorption and the cycle timeline in this document has been redone from SM-FL
> documentation. The FTN-specific functions the draft relied on (auto-addition, auto-dilution, in-needle
> mixing) are **not available on the SM-FL** [V: WKB13017; V: WAT_PREMIER_SPEC lists only "Load Ahead and
> Loop Offline mode, valve cycle timed event" for the SM-FL].

> **System generation is unknown (Q1, §8).** A BSM + fixed-loop sampler exists in three Waters generations:
> the original ACQUITY UPLC (BSM + "ACQUITY Sample Manager", a fixed-loop design), the ACQUITY UPLC I-Class /
> I-Class PLUS (BSM + SM-FL), and ACQUITY Premier (BSM + SM-FL, MaxPeak HPS surfaces). Waters knowledge-base
> articles treat the original ACQUITY Sample Manager and the I-Class SM-FL together for injection-mode
> questions [V: WKB198538, WKB56017, WKB9108]. Numbers below are given per generation where they differ.

---

## 1. Waters ACQUITY Binary Solvent Manager (BSM)

### 1.1 Specifications

| Item | I-Class BSM [V: WAT_ICLASS_SPEC] | Premier BSM [V: WAT_PREMIER_SPEC] | Original ACQUITY UPLC BSM |
|---|---|---|---|
| Flow-rate range | 0.010–2.000 mL/min, 0.001 mL/min steps | **0.001–2.000 mL/min**, 0.001 mL steps (firmware ≥ 1.71) | 0.010–2.000 mL/min [S: search summary of Waters spec] |
| Max. pressure | 18 000 psi (1241 bar) to 1 mL/min; 12 000 psi to 2 mL/min | 15 000 psi to 1.0 mL/min; 9000 psi to 2.0 mL/min | 15 000 psi to 1 mL/min; 9000 psi to 2 mL/min [S] |
| Flow accuracy | ±1.0 % at 0.500 mL/min | same | UNVERIFIED |
| Flow precision | 0.075 % RSD or 0.01 min SD, **only specified 0.2–2.0 mL/min** | ≤ 0.075 % RSD, 0.2–2.0 mL/min | UNVERIFIED |
| Composition precision / accuracy | < 0.15 % RSD; ±0.5 % abs. (5–95 % B), 0.2–2.0 mL/min | ≤ 0.15 % RSD; ±0.5 % abs. | UNVERIFIED |
| Pressure pulsation | not stated | ≤ 0.4 % or 25 psi, whichever is greater | UNVERIFIED |
| Solvents | "Up to four, in combination of two, A1 or A2 and B1 or B2" | same | same (UNVERIFIED) |
| Degassing | six lines, two for injector wash solvents | five chambers, one for injector purge solvent | UNVERIFIED |
| Mixer | 50 µL std; 100 and 380 µL optional | 50 µL std; 340 µL optional | UNVERIFIED |
| System delay / dwell volume | total system delay < 100 µL (default configuration) | **gradient delay ≤ 85 µL, dwell ≤ 110 µL, default FL configuration** | UNVERIFIED |
| Bandspread (5σ) | 6–9 µL (system) | ≤ 11 µL (FL configuration) | — |
| pH range | 2–12 | **1–12.5** | UNVERIFIED |
| Seal wash | programmable active wash of seals and plungers | same | UNVERIFIED |
| Wetted materials | 316L stainless steel, UHMWPE blend, MP35N, titanium alloy, gold, sapphire, ruby, zirconia, Nitronic 60, DLC, fluoropolymer, PEEK, PEEK blend | titanium, PPS, fluoropolymer, fluoroelastomer, UHMWPE blend, sapphire, ruby, zirconia, Nitronic 60, DLC, PEEK, Inconel 600, FEP | UNVERIFIED |
| Event I/O | "Rear panel contact closure and/or TTL inputs/outputs" | same | UNVERIFIED |

### 1.2 What the BSM means for an immunoassay

- **Low flow.** The minimum programmable flow is **10 µL/min** on I-Class (1 µL/min on Premier). Precision is
  specified only from 0.2 mL/min upwards; below that it is UNVERIFIED and should be measured gravimetrically
  at the bench. Do not design incubation steps around slow pumping: use **stopped flow by valve isolation**
  (§7), and keep the pump at a stable 20–300 µL/min.
- **Zero flow.** Whether a 0.000 mL/min step is accepted in the BSM gradient table is UNVERIFIED. The schemes
  in §7 do not depend on it.
- **Minimum back-pressure.** Waters: "the pump assemblies, especially the check valves, require a certain level
  of back pressure… Generally, the back pressure is expected to be above 1000 psi" [V: WKB32564]. Waters' flow
  restrictor kit 205000547 is "a 40 µm × 35 cm capillary with PEEK-SIL coating", installed "between the
  solvent manager mixer and the sample manager injector", adding "greater than 2000 psi on average"
  [V: WKB5084].
  - Derived (Hagen–Poiseuille, water at 25 °C, µ = 0.89 mPa·s): ΔP = 8µLQ/(πr⁴) ≈ **0.83 bar (12 psi) per
    µL/min** for one restrictor → ≈ 1200 psi at 100 µL/min, ≈ 600 psi at 50 µL/min, ≈ 240 psi at 20 µL/min.
    At the assay flows (20–100 µL/min) **one restrictor is not enough**; two or three in series, or a narrower
    restrictor, are needed to reach 1000 psi at 50 µL/min. Measure pressure at the bench.
  - Because the restrictor sits upstream of the injector, everything downstream (loop, reactor, EC cell,
    optical cell) sees only its own hydraulic resistance. This is essential: EC cells are rated 0.8–4 MPa (§5).
- **Reagent lines.** Four lines, two at a time (A1 or A2 with B1 or B2) [V]. A1/A2 and B1/B2 are selected by
  solvent-select valves upstream of each pump, so a line change requires flushing the pump head and mixer;
  an A→B composition change only needs the downstream delay volume (≤ 85–100 µL [V]). Recommended
  allocation (to be confirmed with the chemistry task):

  | Line | Content | Why |
  |---|---|---|
  | A1 | Running / wash buffer (e.g. PBS or Tris with 0.05 % Tween-20, no protein) | Main carrier |
  | A2 | Water or 10–20 % methanol (storage, end-of-day flush) | Avoid salt standing in steel/titanium parts |
  | B1 | Substrate buffer without substrate (or **complete substrate solution**, see below) | Instant A→B switch gives a sharp, low-delay change to substrate conditions |
  | B2 | Regeneration solution (e.g. glycine-HCl pH 2–2.5), *or* nothing if regeneration is injected | — |

  - **Substrate in a BSM line (option).** Putting the complete substrate solution on B1 gives a clean,
    reproducible step into the reactor (delay ≤ 100 µL, no plug dispersion) and removes the carryover problem
    of injecting substrate through the same loop as the conjugate (§2.5). The cost is that the substrate sits
    in the B pump head, degasser and line at ambient temperature for hours, and consumes ≈ 0.5–1 mL per cycle
    (UNVERIFIED estimate). It is acceptable only if the chosen substrate's spontaneous hydrolysis at room
    temperature is low enough (chemistry task to decide). Otherwise inject the substrate from a 4 °C vial (§2).
  - **Regeneration by injection (option).** A 100 µL glycine pH 2 plug injected from a vial keeps low-pH
    solution out of the BSM (pH 2 is the lower limit of the I-Class spec [V]) and leaves B2 free.
  - More lines: Waters supports an external solvent-select valve on the BSM driven by event outputs
    [S: WKB27360, login-gated; wiring UNVERIFIED].
- **Delay volume.** With the SM-FL loop switched offline (§2.4) the BSM-to-reactor delay is the mixer, the
  restrictor, the injection-valve passage and the transfer tubing: ≈ 85 µL on Premier [V] and < 100 µL on
  I-Class [V] in default configuration, plus whatever tubing is added for the reactor and external valve. At
  200–300 µL/min this is a ≈ 20–30 s lag; do buffer changes at high flow with the reactor isolated (§7).
- **Wetted materials and compatibility.**
  - *High-salt aqueous buffers / chloride.* The I-Class BSM has 316L stainless steel and MP35N wetted [V];
    Premier replaces steel by titanium [V]. Chloride pitting/crevice corrosion of 316L when salt is left
    standing is a general materials risk (UNVERIFIED for this instrument). Never leave buffer in the system
    idle: flush to water, then 10–20 % methanol (A2).
  - *Seal wash.* Use 90:10 water/methanol; with ≥ 100 mM salt, shorten the seal-wash interval; never let it
    run dry [S: WKB96281, WKB14943].
  - *Low-pH glycine.* pH 2 is at the limit of the I-Class range [V] (Premier: pH 1 [V]). Keep exposure short,
    flush promptly, or inject regeneration rather than pumping it.
  - *Surfactants.* Tween-20 at 0.05 % is routine in LC buffers; foaming during priming is a nuisance
    (UNVERIFIED).
  - *Proteins and enzyme substrates.* Do **not** pump protein solutions (BSA, conjugate) from BSM lines:
    adsorption on pump surfaces and frits and long hold-up (UNVERIFIED but standard practice). Deliver proteins
    only by SM-FL injection.

---

## 2. Waters ACQUITY Sample Manager – Fixed Loop (SM-FL)

### 2.1 How the SM-FL works (verified from Waters' injection-mode training slides)

The SM-FL has a puncture needle, a sample needle, a **sample (metering) syringe** whose system fluid is the
**weak wash solvent**, a wash syringe, a pressure-relief/wash block, and a 6-port injection valve carrying a
**fixed sample loop** [V: WAT_INJ_MODES; P: MANUALSLIB_ICLASS]. The internal valve passage is 0.100 µL
[V: WAT_INJ_MODES]. In the load position the loop is connected to the needle/syringe side and the pump flows
directly to the column outlet port; in the inject position the pump flow passes through the loop.

Three injection modes [V: WKB22445, WAT_INJ_MODES]:

| Mode | What is drawn and what ends up in the loop | Loop contents at injection | Waters' summary |
|---|---|---|---|
| **Full loop (FL, "Full Loop Using Pressure Assist")** | Air gap + sample (with overfill factor 1–4) drawn; loop pressurised; loop overfilled with sample | "Sample loop contains only sample, no air gaps, no weak wash" | Best accuracy and precision; uses multiple loop volumes of extra sample |
| **Partial loop with pressure assist (PLPA / PLUPA)** | Weak wash–air gap–sample–air gap–weak wash; pressurised and positioned in loop | "Sample loop contains sample, air gaps and weak wash" — **the whole loop, including air gaps and weak wash, is injected** | Short cycle time; sample volume conserved; recommended for large loop injections; accuracy lower; performance depends on weak wash matching mobile phase |
| **Partial loop with needle overfill (PLNO / PLUNO, default)** | Air gap (≈ 1 µL) – pre-volume buffer (≈ 14 µL of sample) – sample – post-volume buffer (≈ 1 µL); sample pulled past the valve and pushed back into the loop | Loop contains sample with mobile phase on both sides; **no air and no weak wash injected** | Recommended for partial-loop injections; accuracy lower than full loop; needs extra cushion sample per injection |

### 2.2 Loops, volumes and sample consumption

**Loop options** (I-Class PLUS / Premier SM-FL): 0.1–250.0 µL injection range in 0.1 µL steps; **10 µL loop
standard**, 1, 2, 5, 20, 50, 100 and 250 µL loops optional [V: WAT_PREMIER_SPEC; S: WAT_ICLASS_PLUS_FL]. Loop
availability for the original ACQUITY Sample Manager is UNVERIFIED (loop kits of 50, 100 and 250 µL exist for
"ACQUITY Sample Manager" [V: WKB3589]).

**Sample syringe.** Standard sample syringe: 100 µL (P/N 700002570) for UPLC, H-Class and I-Class sample
managers [V: WKB110704]. **The 50 µL and 100 µL loops require a 250 µL sample syringe; the 250 µL loop
requires a 500 µL syringe** [V: WKB2345 table]. Kits: 250 µL syringe + 100 µL loop (176001792); 500 µL
syringe + 250 µL loop (176001780); 250 µL syringe + 50 µL loop (176000857) [V: WKB3589].

**Injection volume and sample used per mode** (Waters table, verbatim values) [V: WKB2345]:

| Loop (µL) | PLNO injection (µL) | PLNO sample used (µL) | Partial loop (PLPA) injection (µL) | PLPA sample used (µL) | Full loop injection (µL) | Default overfill factor | Full loop sample used (µL) |
|---|---|---|---|---|---|---|---|
| 1 | 0.1–0.8 | 15.1–15.9 | NR | NR | ~1 | 5.8 | 6 |
| 2 | 0.2–1.5 | 15.2–16.5 | NR | NR | ~2 | 5.6 | 12 |
| 5 | 0.5–3.8 | 15.5–18.8 | NR | NR | ~5 | 5.0 | 25 |
| 10 | 1.0–7.5 | 16.0–22.5 | 1.0–5.0 | 1.0–5.0 | ~10 | 4.0 | 40 |
| 20 | 2.0–15.0 | 17.0–30.0 | 2.0–10 | 2.0–10.0 | ~20 | 3.0 | 60 |
| 50 | 5.0–37.0 | 20.0–45.0 | 5.0–25.0 | 5.0–25.0 | ~50 | 2.0 | 100 |
| **100** | **10.0–75.0** | **25.0–90.0** | **10.0–50.0** | **10.0–50.0** | ~100 | 2.0 | 200 |
| **250** | **25.0–188.0** | **39.0–203.0** | **25.0–125.0** | **25.0–125.0** | ~250 | 1.5 | 375 |

NR = not recommended. Rules of thumb that follow: **PLNO max = 75 % of loop and consumes injection + ≈ 15 µL**
(Waters: "the specified injection volume plus 15.0 µL (14.0-µL pre-sample volume and 1.0-µL post sample
volume)" with the default "automatic" setting [V: WKB11277]; the pre-sample volume is 7 µL for a 10 µL needle
and 10 µL for a 20 µL needle [V: WKB11277]). **PLPA max = 50 % of loop and consumes only the injected
volume.** Full-loop consumption is "the sample volume plus four times the sample volume" by default
[V: WKB198538]; the WKB2345 table gives loop-dependent factors (1.5–5.8) instead — the two Waters statements
differ, and the table is used here. **Minimum residual in the vial: 3 µL** in a Total Recovery 2 mL vial
[V: WAT_PREMIER_SPEC].

**Precision and linearity** (Premier SM-FL) [V: WAT_PREMIER_SPEC]: < 1 % area RSD for 0.2–1.9 µL; < 0.5 % for
2–10 µL; ≤ 0.25 % for 5–50 µL; linearity ≥ 0.999 from 20 % to 75 % of loop in PLNO. No precision is stated for
> 50 µL injections or for PLPA; Waters states PLPA accuracy is lower than PLNO and full loop
[V: WAT_INJ_MODES]. Use 0.5–1 % RSD (UNVERIFIED) for 75–100 µL injections in the model.

**Carryover** (Premier SM-FL): ≤ 0.001 % caffeine (UV), ≤ 0.001 % sulphadimethoxine (MS) [V: WAT_PREMIER_SPEC].
A Waters application note measured 0.00052 % (omeprazole) on the I-Class FL [S: WAT_CARRYOVER_APPNOTE]. Waters
attributes SM-FL carryover to PLNO and recommends switching to PLPA [V: WKB56017]; a timed "Cycle Inject
Valve" event reduces PLNO carryover and has no significant effect in PLPA [V: WKB9108]. **These figures are
for small molecules and are not meaningful for sticky proteins** (§2.5).

**Needle wash.** "Integrated, active, programmable, dual wash" [V: WAT_PREMIER_SPEC]. Weak wash = "mobile
phase composition, initial composition recommended for gradient (salt not included)"; strong wash = "solvent
strong enough to dissolve the sample (salt not included)"; weak:strong volume ratio ≈ 3:1; left port washes
the needle inside with weak wash before aspiration; the right port washes inside with strong wash from the
top while pushing weak wash from below (cleaning the outside); wash volumes are set in the Empower instrument
method [V: WKB205077].

**Sample compartment.** 4.0–40.0 °C in 0.1 °C steps, ±0.5 °C accuracy, ±1.0 °C stability at sensor; holds
19 °C below ambient; cool-down ambient→4 °C ≤ 60 min. Capacity: any two of 96/384-well plates, 48 × 2 mL vial
plates, 48 × 0.65 mL tubes, 24 × 1.5 mL tubes; "768 in two 384-well plates, or 96 in 2-mL vial holders, plus
four additional positions" [V: WAT_PREMIER_SPEC].

**Cycle time.** "≤ 15 s inject-to-inject for FL" (Premier, small injections) [V: WAT_PREMIER_SPEC]. "Load
Ahead" aspirates and loads the next sample ≈ 30 s before the end of the current run and requires the loop to
be taken offline [V: WAT_LOADAHEAD; S: WKB8852]. Syringe draw rates for 75–100 µL draws are UNVERIFIED; budget
**≈ 1 min per injection** (range 0.25–2 min) until measured.

**Wetted materials (sample path)** — Premier SM-FL: UHMWPE blend, DLC, titanium alloy, gold, sapphire, ruby,
zirconia, Nitronic 60, fluoropolymer, PEEK, PEEK blend, fluoroelastomer, HPS [V: WAT_PREMIER_SPEC]. I-Class
SM-FL and original SM: UNVERIFIED (stainless-steel loops are typical). Loop internal diameter and material for
the 100 and 250 µL loops: UNVERIFIED (Q2).

### 2.3 Advanced functions under Empower — what the SM-FL can and cannot do

| Function | SM-FL | Source |
|---|---|---|
| Auto-addition (draw from several vials, mix in needle, inject together) | **No** — "not compatible with fixed loop such as Sample Manager SM-FL" | V: WKB13017 |
| Auto-dilution | Not listed for the SM-FL; listed only for the flow-through-needle manager | V: WAT_PREMIER_SPEC (absence); UNVERIFIED as a positive statement |
| Empower "Sample Prep / In-Needle Auto Additions" (Empower ≥ 3.6.0) | Not shown to support the SM-FL | S: WAT_APPNOTE_720008786 (not opened) |
| Load Ahead | Yes | V: WAT_PREMIER_SPEC, WAT_LOADAHEAD |
| Loop Offline (loop returned to load position after a set time) | Yes | V: WAT_PREMIER_SPEC; S: WKB221963, WKB8852 |
| Valve-cycle timed event ("Cycle Inject Valve" in the Events table) | Yes; allow ≈ 2 s; excessive cycling reduces valve life | V: WKB9108 |
| Timed contact-closure events from the sampler method | Plausible (Events tab exists) — number of outputs UNVERIFIED | V: WKB9108 (Events tab) |
| Inject Start contact-closure output | Yes, connector 1, positions 1–2 ("ACQUITY Sample Manager") | V: WKB55803 |
| Vial-to-vial transfer / in-vial mixing / reagent addition to a vial | **No documented function** | UNVERIFIED (none found) |
| Several plugs (sample, conjugate, substrate) in one injection | **No** (one vial per injection, no auto-addition) | V: WKB13017; WAT_INJ_MODES |

### 2.4 Design consequences of the fixed-loop sampler

**(a) How much of a 100 µL sample can reach the reactor.** Define the delivered fraction
f_del = V_injected / V_sample in vial (losses to surfaces excluded; see (d)). From the Waters table:

| Configuration | Max injection from a 100 µL vial (µL) | f_del | Loop flush volume for ≥ 99.5 % transfer (3 V_loop, see (c)) | Notes |
|---|---|---|---|---|
| 100 µL loop, 250 µL syringe, **PLNO** | 75 (uses 90; 3 µL residual fits) | **0.75** | 300 µL | No air, no weak wash injected; best-characterised mode |
| 250 µL loop, 500 µL syringe, **PLNO** | 82 (82 + 15 + 3 = 100) | **0.82** | 750 µL | Works at 33 % of loop, inside the 20–75 % linear range |
| 250 µL loop, 500 µL syringe, **PLPA** | ≈ 97 (97 + 3 residual) | **0.97** | 750 µL | Injects air gaps and ≈ 150 µL of weak wash with the sample |
| 100 µL loop, **full loop** | 100 µL needs 200 µL sample | — | 300 µL | **Not possible** within the 100 µL budget |
| 50 µL loop, PLNO, two injections | 2 × 37 = 74 (uses 2 × 52 = 104) | ≈ 0.70 | 2 × 150 µL | Repeated injections lose ≈ 15 µL each time; no benefit |

Conclusions:

- **One injection is better than repeated injections**: each PLNO injection wastes ≈ 15 µL of sample as
  needle-overfill cushion, so splitting a 100 µL sample over several injections lowers f_del.
- **PLPA with a 250 µL loop delivers the most analyte (f_del ≈ 0.97)** but puts the air gaps and weak wash
  into the flow path. The air-gap volume is not stated in any document reached (UNVERIFIED; the PLNO slide
  shows ≈ 1 µL air gaps). Under > 1000 psi the air is compressed and partly dissolved in degassed buffer, but
  it can re-form as a bubble where the pressure drops — i.e. in the reactor or the EC cell. **Route the first
  plug of every PLPA injection away from the EC cell (cell bypassed during loading — §7) and test for bubbles
  in the reactor.** The weak wash must equal the running buffer (it is injected) and must not contain protein.
- **PLNO with a 100 µL loop (f_del = 0.75) or a 250 µL loop (f_del = 0.82)** avoids air and weak wash
  entirely. The analyte cost relative to PLPA is 1.2–1.3× in molecules delivered (≈ 0.1 log in LOD at best).
- Recommended baseline for the model: **250 µL loop + 500 µL syringe; PLNO 82 µL (f_del 0.82) as default,
  PLPA 97 µL (f_del 0.97) as the high-recovery option**; 100 µL loop PLNO 75 µL as the fast option (smaller
  flush volume).

**(b) Separate plugs need separate injections and separate Empower lines.** Without auto-addition the SM-FL
injects exactly one vial's content per injection. Sample, conjugate, substrate (if injected) and
regeneration (if injected) are therefore **separate injections, each a separate sample-set line with its own
instrument method and run time**, executed unattended in sequence by Empower. Overhead per line: aspiration
and wash (≈ 1 min budget, UNVERIFIED) plus Empower's acquisition set-up between lines (UNVERIFIED; measure).
Load Ahead can hide the aspiration of the next line inside the current one (requires Loop Offline).

**(c) The loop is in the flow path only between injection and Loop Offline.** After the valve switches to
inject, the pump flow carries the sample out of the loop toward the reactor; when the Loop Offline time
elapses, the valve returns to load and the pump bypasses the loop. Consequences:

- *Transfer from loop to reactor is slow for a protein.* Flow in the loop is laminar and IgG diffuses slowly
  (D ≈ 3.9 × 10⁻¹¹ m²/s [chemistry.yaml: Chang2012]); radial diffusion time r²/D ≈ 26 min for a 0.5 mm ID
  loop. In the purely convective limit the fraction recovered after flushing volume V is 1 − V_loop/(4V)
  (Derived) — only 95 % after 5 loop volumes. Diffusion helps: a 2-D axisymmetric convection–diffusion
  calculation (Poiseuille profile, explicit finite differences with upwind axial convection and radial
  diffusion, no-flux walls; straight tube, conservative because coiling adds secondary mixing; the script
  was run in this session's scratch space and is not a deliverable — the simulation task should reimplement
  it) gives the fraction of the plug that has left the loop after n loop volumes:

  | Case (IgG) | 1 V_loop | 1.5 V_loop | 2 V_loop | 3 V_loop |
  |---|---|---|---|---|
  | 250 µL, 0.5 mm ID, full plug, 50 µL/min | 0.84 | 0.97 | 0.997 | 1.000 |
  | 250 µL, 0.5 mm ID, 85 µL plug at far end, 50 µL/min | 0.62 | 0.91 | 0.99 | 1.000 |
  | 250 µL, 0.5 mm ID, full plug, 200 µL/min | 0.78 | 0.91 | 0.97 | 0.9985 |
  | 250 µL, 0.5 mm ID, 85 µL plug at far end, 200 µL/min | 0.57 | 0.78 | 0.91 | 0.996 |
  | 100 µL, 0.5 mm ID, full plug, 100 µL/min | 0.77 | 0.90 | 0.96 | 0.997 |
  | 100 µL, 0.25 mm ID, 75 µL plug at outlet end, 50 µL/min | 0.95 | 0.998 | 1.000 | 1.000 |

  (Loop IDs are assumptions — UNVERIFIED; the model reproduces the analytic D → 0 limit exactly.) **Design rule:
  keep the loop online for ≥ 3 loop volumes of flush (≥ 99.5 % transfer)**: 300 µL for a 100 µL loop,
  750 µL for a 250 µL loop. At the reactor-loading flow this sets the sample-loading time:
  t_load = 3 V_loop / Q (e.g. 6 min for 100 µL at 50 µL/min; 15 min for 250 µL at 50 µL/min; 7.5 min for
  250 µL at 100 µL/min). The sample is diluted ≈ 3-fold during transfer; for a flow-through capture reactor
  this matters only through the residence time per element, which the simulation handles.
- *Dispersion of reagent plugs.* The same laminar spreading makes an injected substrate or conjugate plug
  arrive with a long tail. For substrate this means the concentration in the reactor at the moment flow is
  stopped is not a clean plateau unless the plug is ≫ the reactor volume and the stop time is calibrated
  (TUV, §7). This favours delivering substrate as a BSM step (§1.2).
- *Dwell volume.* Once offline, the loop adds nothing to the BSM-to-reactor delay (≈ 85–100 µL [V]). Loop
  Offline switching can cause a small baseline/pressure disturbance [S: WKB8852] — keep the EC cell bypassed
  or isolated at the switching moment.
- *Carryover between injections.* While offline, the loop sits on the syringe side and is washed only by
  what passes through it during the next load. Protein adsorbed in the loop or the needle (sample needle,
  needle-overfill path to the valve) can desorb into the **next injection**. With the assay order sample →
  conjugate → substrate, **conjugate left in the loop and needle is carried into the substrate injection,
  which then sits in the reactor during product accumulation — any carried-over enzyme that sticks to the
  reactor produces signal directly.** At 0.001 % carryover a 1 µg/mL conjugate leaves ≈ 10 pg/mL of enzyme
  conjugate in the next plug (Derived, using the small-molecule spec as a lower bound; protein carryover is
  likely higher, UNVERIFIED). Mitigations, in order of preference:
  1. Deliver substrate from the BSM (B1) so no injection follows the conjugate before readout.
  2. Insert a **loop/needle cleaning injection** (e.g. 100 µL of detergent or glycine pH 2) between the
     conjugate and the substrate, diverted to waste with the reactor isolated (§7).
  3. Strong wash with detergent/organic; PLPA mode; programmed valve cycling (effective in PLNO only
     [V: WKB9108]).
- *Protein adsorption.* At 6.7 fM (1 pg/mL) IgG is far below any surface-saturation concentration, so even a
  tiny fraction of a monolayer on the vial, needle, needle-to-valve tubing and loop removes a large fraction of
  the 4 × 10⁵ molecules. Area of a 250 µL, 0.5 mm ID loop ≈ π·d·L ≈ 19 cm² (Derived, ID assumed); of a 100 µL,
  0.25 mm ID loop ≈ 16 cm². Mitigation: carrier protein in sample diluent (chemistry task), Premier/HPS or
  PEEK loops, and a **spike-recovery test through the injector** (R1). Use the chemistry task's
  `adsorptive_loss_fraction` for the model.

**(d) In-vial incubation is not automatable on the SM-FL.** The SM-FL cannot add conjugate to a sample vial
or transfer between vials (§2.3). Homogeneous pre-incubation (sample + detection conjugate in the vial) is
only possible if the user loads the sample into a vial already containing conjugate (pre-dispensed vials).
Whether that counts as "loading the autosampler" is a question for the user (Q4). If allowed, the 4–40 °C
compartment can hold the incubation, but the incubation time then depends on queue position and must be
fixed by method timing. The schemes in §7 assume **no in-vial incubation**.

**(e) What the SM-FL does well.** The needle is never in the high-pressure path, so loop volume does not
add permanent dwell volume; the loop can be switched out; the injection valve can be cycled by a timed event;
Inject Start gives a clean t₀ signal; the sample compartment is cooled (reagent vials for conjugate and
substrate at 4 °C).

---

## 3. Controlling Empower and the Waters stack from Python

### 3.1 Options

| Option | What it does | Limits | Status |
|---|---|---|---|
| **Empower Toolkit** (COM automation; "Empower Toolkit Programmer's Reference Guide", Waters 71500031805 [S]) | Programmatic access to "most of the key data structures and functionality" of Empower: projects, methods, sample sets, results [S: WAT_TOOLKIT_FORUM] | Licensed Empower option [S]. Whether it can **start acquisition** of a sample set on a chromatographic system and report run state is **UNVERIFIED** (manual not reachable; a targeted search found no public statement). Windows-only COM; bitness matching UNVERIFIED. Some objects cannot be created via the Toolkit [S: TETRA_EMPOWER] | Ask Waters (Q5) |
| **Pre-built sample-set method, started by the operator** | Operator loads a sample-set method (one block of lines per assay cycle) and presses Run; Empower then executes injections, BSM programmes and timed events unattended | One click per batch (acceptable: "loading the autosampler"). Python cannot change the sequence mid-run | Works with any Empower |
| **Sample Set Generator** (Waters add-on) | Automates creation of methods and sample sets [S: WAT_SSG] | Creation only, not real-time control | Optional |
| **Third-party connectors** (e.g. Tetra Empower Agent) | REST access to sample sets/results [S: TETRA_EMPOWER] | Built on the Toolkit; licence and IT effort | Not recommended |
| **Contact closures / TTL** (hardware) | ACQUITY modules: "Rear panel contact closure and/or TTL inputs/outputs" [V: WAT_ICLASS_SPEC, WAT_PREMIER_SPEC]. SM Inject Start output: connector 1, positions 1 and 2 [V: WKB55803] | Fixed signal set; needs wiring and an isolated DAQ. Deterministic and independent of Empower version | **Recommended backbone** |

Signals: **Inject Start** (SM-FL) is verified [V: WKB55803]; its pulse width is not stated (UNVERIFIED). BSM
and SM-FL method **Events** tabs provide timed events (verified for the SM-FL: "Cycle Inject Valve" under Run
Events [V: WKB9108]); the number, type (relay or TTL) and ratings of event outputs and any event *inputs*
(e.g. inject hold, external start, stop flow) on this BSM/SM-FL are **UNVERIFIED** — photograph the rear
panels and read the Empower instrument-method Events tabs (Q6). Latency of contact closures is not specified
(assume 10–100 ms, UNVERIFIED); irrelevant for minute-scale steps, but all events must be timestamped on one
PC clock.

### 3.2 Recommended synchronisation

**Primary scheme — "Empower is the fluidic master; Python listens, drives the valves and owns the EC."**

1. One assay cycle = a block of Empower sample-set lines (§7.4): L1 sample injection; L2 conjugate injection
   whose method also contains the wash, the BSM substrate step, accumulation and readout; L3 regeneration
   injection and re-equilibration. If substrate is injected instead of pumped, two lines are added between L2
   and L3 (cleaning injection to waste, substrate injection). Each line has its own instrument method: BSM flow/composition programme,
   SM-FL injection mode/volume, **Loop Offline time**, run time (= step duration) and, if available, timed
   event outputs.
2. SM-FL **Inject Start** (connector 1, pos. 1–2) → opto-isolated digital input of a USB DAQ owned by Python.
   If the BSM has ≥ 2 event outputs, program them at t = 0.05 min of each method as a 2-bit **line code**
   (sample / conjugate / substrate / regeneration) → two more isolated inputs. Python therefore knows *which*
   step started, not only *that* one started. (The Gamry Misc. I/O has 4 TTL inputs [V: GAMRY_IO_APPNOTE], but
   reading them from ToolkitPy during an acquisition is UNVERIFIED; a separate DAQ keeps concerns separate.)
3. Python holds a **cycle table**: step type, offsets from t₀, valve states, Gamry actions. On each Inject
   Start edge it checks the line code and expected time window, then schedules: external valve(s) to the
   step's states, Gamry technique changes, marks.
4. **External valves** (the given 6/10-port plus, recommended, a second one — §7) are driven by Python through
   their actuator interface (contact/TTL or serial; model-dependent, Q7). Alternative if the BSM has spare
   event outputs: let Empower drive the valves directly from the instrument-method Events table, and Python
   only mirrors the lines on its DAQ. This puts all fluidic timing in one validated place, but needs one
   event output per valve (UNVERIFIED availability).
5. **Gamry runs continuously** through the cycle (one long chronoamperometry, or a sequence of segments —
   pulsed/DPV readout during the readout window), timestamped on the PC clock with event marks in the same
   file. Optionally feed the Gamry analog current output (0–5 V on Misc. I/O pin 1, Reference family
   [V: GAMRY_IO_APPNOTE]) into a Waters analog input so Empower records EC and TUV side by side (analog-input
   hardware UNVERIFIED, Q8).
6. **Watchdog**: if an expected Inject Start is late by > 30 s, or the line code is wrong, Python sets the
   valves to "reactor isolated / cell bypassed", holds the electrode at a safe potential or open circuit,
   and alarms. Python never needs to start or stop Empower.

Timing diagram for one injection line (text):

```
time ──────────────────────────────────────────────────────────────────────────────►
Empower line n:  [acq. set-up][SM-FL aspirate/wash ≈1 min]│ run time T_n ...................│ line n+1
SM-FL Inject Start CC:                                    ┌┐ t0
BSM event outs (line code):                               └┴─ code set at t0+3 s
SM-FL valve:                       load ──────────────────┤ inject ───────────┤ load (Loop Offline at t0+t_off,
                                                          │                   │       t_off ≥ 3·V_loop/Q)
Python DAQ:                                               ● edge read, code checked
External valve V10 (reactor):  isolate ──── t0−5 s ►perfuse ─────────────────────► isolate at t0+t_off+t_wash
External valve V6 (cell):      bypass ───────────────────────────────────────────── (detect only in readout)
Gamry:            ════ continuous CA at E_det (marks at every Python action) ═════════════════════════
BSM programme:    initial conditions ─► flow/composition table of method n ─────────────► end of run
```

The SM-FL aspiration starts before Inject Start, so Python sets the valves for line n slightly before t₀ only
when it can predict t₀ from the end of line n−1 (run times are deterministic); otherwise it sets them in the
first seconds after t₀, which is harmless because the plug needs ≥ (tubing volume)/Q ≈ 10–30 s to reach the
reactor (Derived).

**Fallback A — Python is master through the Empower Toolkit.** Only if Waters confirms that the Toolkit can
create/start a sample set and report status on this installation (Q5). Python then builds each cycle's lines
(e.g. adapting accumulation time to the previous signal) and still uses Inject Start for t₀.

**Fallback B — Python releases each line through an Empower/SM event input.** Only if an "inject hold" or
"external start" input exists and Empower can be set to wait for it (UNVERIFIED, Q6). Gives Python full step
timing.

**Fallback C — open loop.** Empower runs the sample set; Python only listens to Inject Start, drives valves
and Gamry, and tolerates drift. Always possible.

---

## 4. Gamry Reference 600+

### 4.1 Specifications [V: GAMRY_REF600P_DS, GAMRY_REF600P_LEGACY]

| Item | Value |
|---|---|
| Current ranges | 11 ranges, 60 pA–600 mA (13 with internal 10× and 100× gain); max ±600 mA |
| Current resolution | 0.003 % full scale per bit; minimum current resolution **20 aA** |
| Current accuracy | ±10 pA ± 0.05 % of range ± 0.2 % of value (600 mA–6 nA ranges); or 0.75 % of value (600 pA); or 1.5 % of value (60 pA) |
| Current-measurement bandwidth | > 10 MHz (600 mA–600 µA); > 0.15 MHz (6 µA); not stated for nA/pA ranges (far lower) |
| Noise and ripple | < 2 µV rms typical (potential) |
| Rise time | < 250 ns |
| Min. time base | 3.333 µs |
| Min. potential step | 12.5 µV |
| Applied potential / compliance | ±11 V / > ±22 V |
| Electrometer | > 10¹⁴ Ω input impedance; < 10 pA input current; > 15 MHz bandwidth; CMRR > 65 dB (1 MHz) |
| EIS | 10 µHz–5 MHz |
| Isolation | "Isolated from earth: Yes" (floating) |
| Cell connections | 2, 3, 4, 5 or 6 (includes aux channel) |
| DSP sampling modes | Fast (end of step), Noise Reject (average of last 20 % of step), Surface (average of whole step) |
| I/O | BNC aux voltage input; external signal into control amplifier; 15-pin connector with TTL digital I/O and a voltage output |
| Status | **Discontinued; successor Reference 620** |

**Techniques** (licensed packages) [V: GAMRY_REF600P_LEGACY]: PHE200 (CV, chronoamperometry,
chronopotentiometry and derivatives; multi-step), PV220 (pulse, square-wave and stripping voltammetry — DPV,
SWV, NPV), EIS300 (EIS, Mott–Schottky), ESA410/EN120 (electrochemical noise), eChemDC/eChemAC Toolkit
licences. Toolkit signal/data classes include chronoamperometry, pulse voltammetry, square wave, EIS and
multi-step signals [P: GAMRY_TK_V2].

### 4.2 Misc. I/O and triggers [V: GAMRY_IO_APPNOTE]

- **4 digital inputs and 4 digital outputs** (0/5 V); digital outputs on pins 7–10 (pin 7 = channel 0),
  digital ground pin 6; analog output pin 1 (0–5 V on Reference instruments), ground pin 2.
- Connected devices must draw < 10 µA from the inputs.
- "All of the User I/O signals are insulated from both earth ground and the instrument floating ground"
  (Reference family) — the trigger wiring does not create a ground loop.
- Framework sequences can wait on a "Digital Signal In" channel; ToolkitPy support for reading digital inputs
  is UNVERIFIED. Minimum output pulse width ≈ 10–50 µs [P: GAMRY_TRIGGER_APPNOTE].

### 4.3 Python control

- **Echem ToolkitPy** (official) [V: GAMRY_TKPY_QSG, GAMRY_TKPY_BROCH]: requires Gamry software ≥ 7.10.4; ships a
  curated **Python 3.7.9 (32-bit)** with NumPy 1.21.6 and PySide2 5.15.2; an existing Python 3.7 32-bit must be
  removed first; installation needs administrator rights; **Windows 10, 11 or higher**; supports Reference
  600/600+/620. Runs acquisition in a background thread with data into NumPy; no 262 144-point Framework
  limit, ≈ 2 million points in fast mode (< 100 µs sampling). RAM requirement 16 GB (32 GB recommended)
  [S: GAMRY_TKPY_WEB]. Separate licence needed or not: **UNVERIFIED** (Q9).
  - Consequence: run a **Gamry worker process** in Gamry's 32-bit Python 3.7 and talk to it over a local
    socket/ZeroMQ from the main orchestrator (modern 64-bit Python with the DAQ and valve drivers).
- **Echem Toolkit over COM** (GamryCOM) via `comtypes`/`pywin32`; requires eChemBasic/eChemDC/eChemAC licences
  [V: GAMRY_REF600P_LEGACY lists eChemDC/eChemAC; P: GAMRY_TK_V2]. Bitness matching UNVERIFIED.
- **Framework (Explain) scripts** launched by Python — oldest, least integrated route.

### 4.4 Floating operation and grounding with a grounded LC stack

- The Waters stack is earthed and its fluid path contains metal (I-Class BSM: steel/MP35N/titanium;
  Premier: titanium [V]). The buffer is conductive, so the cell electrolyte is connected to earth through
  the liquid in the tubing. The Ref 600+ is isolated from earth [V], so there is no DC ground loop through
  the instrument, but the liquid column couples mains and pump-motor noise into the cell.
- **Solution-path resistance** (Derived, R = L/(κA)): with κ ≈ 1.6 S/m (PBS, UNVERIFIED value), 0.3 m of
  127 µm ID PEEK ≈ 15 MΩ; 0.3 m of 63.5 µm ID ≈ 59 MΩ. Use **PEEK (not steel) for at least the last 30 cm on
  both sides of the cell**; keep any steel part of the cell (e.g. a stainless counter electrode) isolated from
  earth.
- Recommendations: cell in a **Faraday cage** connected per the Gamry manual for floating operation
  (UNVERIFIED wording); short cell cable; cell away from BSM/SM-FL power supplies; a defined earth point in
  the fluid path upstream (a grounded metal union before the long PEEK section — standard LC-EC practice,
  UNVERIFIED); damp pump pulsation (Premier: ≤ 0.4 % or 25 psi [V]) with the restrictor or measure in
  stopped flow; integrate over whole mains cycles (20 ms at 50 Hz) using Noise Reject/Surface sampling.

### 4.5 Realistic current noise (detection floor in the model)

| Level | Value | Basis |
|---|---|---|
| Instrument floor (Ref 600+, caged, nA range) | ≪ 1 pA (20 aA resolution [V]; electrometer input current < 10 pA is a DC offset, not noise) | Not limiting |
| Purpose-built LC-EC amplifier, dummy cell | ≤ 2 pA peak-to-peak, 1 nA range, filter off (Antec DECADE Elite) → ≈ 0.3–0.5 pA rms using p-p ≈ 5 × rms [S: ANTEC_DECADE] | Best-case analog floor |
| Capacitive (voltage-noise) term | i_n ≈ 2π f e_n C_dl; a 2 mm disk at ≈ 20 µF/cm² (UNVERIFIED C_dl) has C ≈ 0.63 µF → ≈ 4 pA rms per µV rms of voltage noise at 1 Hz bandwidth [Derived]; electrode noise is amplifier-dominated at low C and capacitance-dominated at intermediate C [V: LARSEN2012 (PubMed record)] | Scales with electrode area |
| Cell-limited LC-EC baseline in flow | 1–10 pA rms for mm-scale carbon thin-layer/wall-jet cells, pump and flow noise included (UNVERIFIED range) | "Flowing" detection model |
| Stopped flow / quiescent | ≈ 0.5–3 pA rms (UNVERIFIED); pump noise removed, drift and background decay dominate | Stopped-flow readout |

**Model recommendation:** i_noise,rms = **3 pA** in flow (bounds 0.5–20 pA) and **1 pA** in stopped flow
(0.3–5 pA) for a 2–3 mm carbon electrode; scale with electrode capacitance when area changes; add baseline
drift 1–10 pA/min (UNVERIFIED). In practice the blank SD (substrate auto-hydrolysis, non-specific conjugate
binding, carryover — chemistry task and §2.4) is expected to exceed the instrument noise.

---

## 5. Electrochemical flow cells and electrodes

All cells below take ordinary WE/RE/CE leads unless noted; vendor-specific detector connectors need adapter
cables (UNVERIFIED for each).

| Cell | Type | WE material & size | Volume / gap | RE / CE | Pressure limit | Connection | Gamry? | Collection / amplification | Reuse |
|---|---|---|---|---|---|---|---|---|---|
| **Antec SenCell** [V: ANTEC_SENCELL] | Confined wall-jet with adjustable spacer (no gaskets) | GC, Pt, Au (2 mm) [S] | Working volume adjustable ≈ 0–300 nL [V] | Salt-bridge Ag/AgCl, ISAAC (in-situ Ag/AgCl) or HyREF [V] | Not stated (UNVERIFIED) | UHPLC fittings (UNVERIFIED) | Plausible with 3 leads; designed for Antec DECADE (UNVERIFIED) | Partial conversion (few %, UNVERIFIED) | Excellent; polishable |
| **Antec VT-03** (also sold for Waters 2465) | Thin layer | GC, Pt, Au, Ag [P] | ≥ 5 nL; 25/50 µm spacers [S] | Salt bridge, ISAAC, HyREF | UNVERIFIED | UNVERIFIED | Plausible | Thin-layer amperometric | Excellent |
| **Antec FlexCell** | Thin layer | GC etc. | ≈ 0.7 µL with 50 µm spacer; 50/130 µm spacers [S] | HyREF, salt bridge, ISAAC [P] | UNVERIFIED | UNVERIFIED | Plausible | — | Good |
| **BASi cross-flow thin-layer** (dual 3 mm GC) [S: BASI_GASKETS] | Thin layer, single or **dual WE** (series/parallel) | GC 3 mm | Gaskets 13, 51, 127 µm [S] | Ag/AgCl RE, steel CE (UNVERIFIED) | Low (UNVERIFIED) | UNVERIFIED | Yes; **dual WE needs a bipotentiostat** | Series dual electrode = generator–collector for reversible couples [P: LUNTE1985] | Very good; polishable |
| **Metrohm thin-layer cell** [V: METROHM_TL_MANUAL] | Thin layer | WE not stated on spec page | < 0.35 µL (50 µm spacer); < 0.18 µL (25 µm) | Pd solid-phase or Ag/AgCl gel RE; **stainless-steel CE** (installed) | **0.8 MPa** (manual prints "(200 psi)", which is inconsistent — use 0.8 MPa) | UNVERIFIED | Designed for Metrohm IC detector; adapter needed (UNVERIFIED) | — | Good |
| **Metrohm DropSens DRP-FLWCL-PEEK** [V: METROHM_FLWCL] | Wall-jet cell for standard screen-printed electrodes; magnetic closure; fittings included | SPE carbon, Au (e.g. DRP-250BT: Au WE, Pt aux, Ag ref), Prussian blue | Not stated | On-strip Ag pseudo-RE and CE | Not stated (low; UNVERIFIED) | Fittings included (type UNVERIFIED) | **Yes** via DRP-CAC cable "to any kind of potentiostat" [V] | Wall-jet, low conversion | **Disposable** electrode |
| **Thermo Dionex 6011RS ultra** [V: THERMO_6011RS] | Flow-through porous graphite, **dual electrodes in series** | Micro-porous graphitic carbon | **4.3 µL** internal | Pd solid-state RE, built-in CE | **40 bar (4.0 MPa)** at inlet | nanoViper (UNVERIFIED thread) | Designed for UltiMate ECD-3000RS (SmartChip); third-party wiring UNVERIFIED | **Near 100 % (coulometric)** [V]; usable flow **> 0.3 mL/min** [V] | Good; not polishable |
| **Thin-film IDA chips** (BASi/Micrux, Pt or Au on glass) [P: BASI_IDA] | Planar interdigitated arrays | Pt/Au, 10/10 µm × 15 fingers; 10/5 µm × 50 (Pt); 5/5 µm × 30 | Set by the flow add-on (PMMA; PEEK on request) [S: MICRUX_AIO] | Integrated RE/CE on some chips | Low (UNVERIFIED) | UNVERIFIED | Single WE yes; **redox cycling needs 2 WEs** | 2-D open IDA: modest gain; closed/3-D IDA ≈ 100× [V: HAN2014 (PubMed)]; ≈ 25× [P: SHARMA2018]; comb IDA ≈ 3× vs coplanar [P: KIM2004] | Cleanable electrochemically |
| **Micrux ED-IDRA1** (radial IDA) [S: MICRUX_IDRA] | Radial IDA "for flow systems" | 12 pairs, 10/10 µm, 2 mm cell | — | 4-electrode chip | — | — | Bipotentiostat needed | Redox cycling | As above |
| **Custom cell** (§5.2) | Thin-layer channel over IDA or band pair | Carbon (pyrolysed photoresist) or Au/Pt IDA, 2–5 µm gaps | 10–50 µm channel; 50–500 nL | Integrated Pt CE; external Ag/AgCl RE via side-arm salt bridge | Design ≥ 1 MPa | 10-32 coned ports, 1/16″ PEEK | Yes | Target ≥ 10× | Replaceable chip in reusable PEEK holder |

### 5.1 Selection notes

- **Redox cycling needs a second potentiostat channel.** Gamry builds bipotentiostats from two synchronised
  Reference-family instruments with a sync cable and shared RE/CE [S: GAMRY_BIPOT_NOTE]; the listed pairings
  name Reference 620 and 3000, not the 600+ — pairing a 600+ with a 620 is UNVERIFIED (Q10). Budget is
  unconstrained: buy a Reference 620 (or a matched pair).
- **Coulometric porous cell** (6011RS) converts nearly all product [V]. For stopped-flow accumulation the
  signal becomes the charge Q = nF·N_product, independent of flow. Penalties: large area → high background
  and noise; vendor connector; specified only above 0.3 mL/min [V] — readout of a 4–10 µL product plug at
  ≥ 0.3 mL/min is a 1–2 s peak (Derived). Model as architecture "COUL".
- **Thin-layer amperometric cells** (BASi, Antec, Metrohm) are the robust baseline: polishable,
  potentiostat-agnostic, nL volumes. Conversion depends on h²U/(DL) (channel height h, mean velocity U,
  electrode length L): at 10–50 µL/min with 13–51 µm gaps it rises substantially (simulation to compute).
- **Disposable SPEs in a wall-jet cell** (DropSens) suit early development; electrode-to-electrode variance
  adds to blank SD (UNVERIFIED magnitude).
- **Pressure.** All EC cells must be downstream of the restrictor and the reactor, with the outlet open to
  waste through ≤ 50–100 psi of tubing (keeps bubbles dissolved, within the 0.8 MPa = 116 psi Metrohm limit).

### 5.2 What a custom cell would look like

- **Body**: PEEK or PCTFE clamping a glass/Si chip with a thin-film IDA (Au, Pt or pyrolysed carbon, 2–5 µm
  bands and gaps, 0.5–2 mm² active area).
- **Channel**: 10–25 µm laser-cut PET/PTFE gasket, ≈ 0.5 mm × 3 mm.
- **Fluidics**: 10-32 coned ports for 1/16″ PEEK; side-arm Ag/AgCl RE (3 M KCl behind a frit) and Pt CE
  **downstream** of the WE so KCl leakage does not reach it.
- **Electrical**: pogo-pin contacts; shielded cable to the two Gamry channels; Faraday cage.
- **Ratings**: design pressure ≥ 1 MPa.
- **Optional integration**: capture zone on the channel lid or a short bead bed **immediately upstream** of
  the IDA — product travels < 1 µL to the detector, the "accumulate on chip, then measure" geometry of IDA
  ELISA papers [V: NIWA1993, HAN2014 (PubMed records)]. Then protein and regeneration steps pass over the
  electrode (fouling risk R4) — this is Scheme C (§7.3).

---

## 6. Capture reactor hardware

| Option | Bed volume | Pressure limit | Particle / pore | Notes | Source |
|---|---|---|---|---|---|
| **CIMac monolith 0.1 mL** (r-Protein A, epoxy, EDA, OH, …) | 0.1 mL (5.2 mm ID × 4.95 mm) | CIMac QA 15 MPa [S]; others UNVERIFIED | Channels 1.3, 2 or 6 µm | r-Protein A: pH 2–11 working, 2–13 CIP [S]; 0.2–3 mL/min for siblings [S] | SARTORIUS_CIMAC [S] |
| **POROS A 20 µm 2.1 × 30 mm** (Protein A) | 0.1 mL | 2400 psi (stainless) [S] | 20 µm perfusive particles | Capacity ≈ 19 mg/mL [S] | THERMO_POROS_A [S] |
| **Empty micro-column / guard hardware** packed with antibody beads (1.0–2.1 mm ID × 5–20 mm; 2–10 µm frits) | 4–70 µL (Derived: πr²L) | Hardware typically ≥ 100 bar (UNVERIFIED) | Beads 1–50 µm | Vendor/part to be selected (none verified) | UNVERIFIED |
| **Renewable bead column** (beads delivered and discarded each cycle) | ≈ 3.6 µL rotating-rod cell | Low | Sepharose | Sandwich immunoassay < 20 min | [P: GRATE2009; PubMed record V] |
| **Magnetic-bead trapping in flow** | µL (trap-defined) | Low | 1–3 µm superparamagnetic (UNVERIFIED) | SIA + magnet; ALP/PAPP amperometric, < 15 min | [P: HIRAKAWA2006; PubMed record V] |
| **Open-tubular / capillary reactor** (antibody on wall, 50–250 µm ID) | 0.2–5 µL per 10 cm | High | — | Low capacity, slow mass transport, very low NSB area | UNVERIFIED |
| **Historical inline immunoreactors**: CPG–Protein A, acid elution, flow-injection EC EIA; silica immunoreactor, ALP/PAPP, 12 min cycle | — | — | — | Precedent for regenerable inline capture with EC detection | [P: PALMER1992; P: TRAU1997, PubMed record V] |

**Bead loading with the SM-FL.** A renewable bead bed (fresh capture beads every cycle) would need the beads
to be injected; bead suspensions settle in vials and in a 100–250 µL loop (UNVERIFIED behaviour in the SM-FL
syringe path; risk of needle/valve blockage). Not recommended through the SM-FL without a bench test.

**Choosing the reactor.** A 5–20 µL packed bed gives high linear velocity and a small product-dilution volume
(the enzyme product is diluted into the bed void during stopped-flow accumulation). **Model a 10 µL bed
(1 mm ID × 12.7 mm, void ≈ 4 µL, porosity ≈ 0.4 UNVERIFIED) and a 100 µL monolith as two cases.** Protein A/G
columns allow "capture-antibody renewal" (strip and reload the capture antibody each cycle) — the
chemistry task decides.

The capture reactor should be **thermostatted** (binding kinetics; the fixed equipment list has no column
heater — a column heater/manager or a simple Peltier block is a purchase, UNVERIFIED need).

---

## 7. System-level fluidics around the fixed-loop sampler

Common elements of all schemes:

```
BSM (A1/A2, B1/B2) ─► mixer ─► restrictor(s) (≥1000 psi at pump) ─► SM-FL 6-port injection valve
                                                                     (loop online only from inject to Loop Offline)
                                                                   ─► "to column" port ─► external valve(s) ─► reactor / EC cell ─► optical detector ─► waste
```

- All tubing after the injection valve: 1/16″ PEEK, 0.005″ (127 µm) ID — 12.7 µL/m (Derived); at least the
  last 30 cm on each side of the EC cell in PEEK (§4.4).
- **Optical detector** (TUV/PDA/FLR): last in line, after the EC cell, so it sees every step. TUV flow cell
  ≈ 500 nL, 10 mm path, 1000 psi max [S: WAT_TUV] (PDA/FLR cell limits UNVERIFIED). Development uses: watch
  protein plugs at 280 nm (sample/conjugate breakthrough, loop-flush completeness, §2.4 c), measure plug
  arrival times, check the substrate step and the product plug (e.g. 4-aminophenol absorbs in the UV;
  wavelength from the chemistry task), detect bubbles.
- **Weak wash** = running buffer without protein (it is the syringe fluid and, in PLPA, is injected);
  **strong wash** = detergent or 10–20 % organic in water (no salt) [V: WKB205077 guidance], chosen to strip
  protein (efficacy UNVERIFIED; bench test R2).
- **Vials** (sample compartment at 4–8 °C): samples; conjugate (one 2 mL vial serves ≈ 50 PLNO injections of
  20 µL: 20 + 15 µL each; Derived); cleaning solution; regeneration (if injected); substrate (if injected).
- Recommended SM-FL configuration: **250 µL loop + 500 µL syringe** (kit 176001780 [V: WKB3589]); PLNO 82 µL
  default, PLPA 97 µL option (§2.4 a).

Valve port conventions used below (standard 2-position rotors; actual numbering depends on the model, Q7):
6-port — position A connects 1-2, 3-4, 5-6; position B connects 2-3, 4-5, 6-1. 10-port — position A
connects 1-2, 3-4, 5-6, 7-8, 9-10; position B connects 2-3, 4-5, 6-7, 8-9, 10-1.

### 7.1 Scheme A — one 6-port valve as EC-cell bypass (minimum hardware: the given valve only)

```
SM-FL ─► reactor ─► V6 port 2
V6 pos A (DETECT): 2→1 ─► EC cell ─► 4→3 ─► optical det. ─► waste
V6 pos B (BYPASS): 2→3 ─► optical det. ─► waste      cell between ports 1 and 4, closed via 6 and 5
                                                    (ports 5/6: plugged, or an auxiliary low-flow buffer
                                                     source in 6 and waste from 5 to keep the cell perfused)
```

- Sample, conjugate, washes and regeneration in BYPASS: protein and low pH never reach the electrode.
- Substrate step and readout in DETECT.
- **Limitation:** no true stopped flow in the reactor. Options: (i) BSM at a 0.000 mL/min step (UNVERIFIED);
  (ii) slow perfusion at the BSM minimum (10 µL/min I-Class, 1 µL/min Premier [V]) — with a 4 µL bed void the
  bed is exchanged every 0.4 min (I-Class) or 4 min (Premier), so product is continuously washed out
  (Derived). Scheme A therefore suits a **continuous-flow readout**: with substrate flowing, the outlet
  product flux equals the total enzyme turnover in the bed, so with a coulometric cell the steady-state
  current is i = nF·(product generation rate) independent of Q (Derived; requires flow ≥ 0.3 mL/min for the
  6011RS [V], which shortens bed residence). A thin-layer cell collects only a fraction (conversion
  efficiency, to be computed).

### 7.2 Scheme B — 10-port reactor isolation + 6-port cell bypass (recommended; buy one extra valve)

```
                       V10 pos A (PERFUSE)                         V10 pos B (ISOLATE)
SM-FL ─► V10 port 1 ─► 1→2 ─► REACTOR ─► 3→4 ─► V6 port 2          1→10 ─► SHUNT ─► 5→4 ─► V6 port 2
                       shunt (10…5) dead-ended via 9 and 6         reactor ends 2 and 3 joined (2-3): no net flow
V6 as in Scheme A: pos A = through EC cell, pos B = cell bypassed; both end at the optical detector.
Ports 6–9 of V10 plugged (or used later for a second reactor).
```

The shunt should have roughly the reactor's hydraulic resistance (a short restrictor) to avoid pressure
steps when switching (UNVERIFIED need; measure).

| State | V10 | V6 | Path | Used for |
|---|---|---|---|---|
| Load | A | B | inlet → reactor → bypass → optical → waste | Sample and conjugate perfusion; washes; regeneration |
| Incubate / accumulate | B | A | inlet → shunt → **EC cell** → optical → waste; reactor sealed | Stopped-flow binding; **substrate product accumulation**; meanwhile the cell sees fresh substrate from the BSM (substrate blank current measured in real time); buffer changes at high flow without disturbing the reactor; loop flushing to waste |
| Readout | A | A | inlet → reactor → **EC cell** → optical → waste | Product plug swept from the bed into the cell |
| Park | B | B | inlet → shunt → bypass | Cleaning injections to waste; idle |

- **True stopped flow** in the reactor with the BSM kept at a stable flow and pressure.
- **Electrode protected**: protein, low pH and the PLPA air gaps are routed around the cell.
- **Substrate background measured continuously** during accumulation, giving a per-cycle blank-drift
  reference.
- **If only one external valve is allowed**: use the 10-port (Scheme B-1): the cell is then always
  downstream of the reactor in state A, so sample, conjugate and regeneration pass the electrode; hold it at
  open circuit or a mild potential during those steps and plan electrochemical cleaning (R4).

### 7.3 Scheme C — integrated capture–detection chip, stopped-flow readout in the cell

The capture surface (antibody on the channel wall or a short bead bed) sits **immediately upstream of, or
on, the IDA / thin-layer electrode** inside one custom cell (§5.2). The 10-port valve isolates the chip
(as the reactor in Scheme B). Product accumulates in the sealed channel and is measured **in stopped flow
directly at the electrode** (no elution, no dilution into tubing); redox cycling between IDA fingers
amplifies a reversible product [V: NIWA1993, HAN2014]. The price: every protein and regeneration step
passes over the electrode (fouling, R4), the electrode is part of the reusable capture surface, and capture
area is small. Model as the "on-electrode" architecture; the bench order is Scheme B first.

### 7.4 Timeline of one assay cycle (Scheme B, 250 µL loop, 10 µL bed)

Baseline assumptions: sample 82 µL PLNO (f_del = 0.82), loaded at 100 µL/min (3 loop volumes = 750 µL);
conjugate 20 µL PLNO; **substrate delivered as a BSM step from B1**; regeneration by a 100 µL glycine
injection. Each injection overhead (aspirate + wash + Empower set-up) budgeted at 1.0 min (UNVERIFIED).

| t start (min) | Step | Empower line | V10 / V6 | Flow, solvent | EC (Gamry) | Dur. (min) |
|---|---|---|---|---|---|---|
| 0.0 | Aspirate sample (overlaps previous cycle if Load Ahead is used) | L1 | B / B | 200 µL/min A1 | Baseline in buffer (cell static) | 1.0 |
| 1.0 | **Inject Start t₀(L1)**; sample through reactor; loop online for 750 µL | L1 | A / B | 100 µL/min A1 | — | 7.5 |
| 8.5 | Loop Offline; wash 20 bed volumes | L1 | A / B | 200 µL/min A1 | — | 1.0 |
| 9.5 | Aspirate conjugate (hidden by Load Ahead if enabled) | L2 | A / B | 200 µL/min A1 | — | 1.0 |
| 10.5 | **t₀(L2)**; conjugate plug into reactor (stop time calibrated by TUV) | L2 | A / B | 100 µL/min A1 | — | 1.0 |
| 11.5 | Stopped-flow conjugate binding; loop flush to waste via shunt (750 µL) | L2 | B / B | 150 µL/min A1 | — | 5.0 |
| 16.5 | Loop Offline; stringent wash (50 bed volumes) | L2 | A / B | 250 µL/min A1 | — | 2.0 |
| 18.5 | Step to 100 % B1 (substrate); fill reactor (≥ 25 bed volumes) | L2 | A / B→A at end | 200 µL/min B1 | Cell fills with substrate; baseline | 1.0 |
| 19.5 | **Product accumulation** (reactor sealed) | L2 | B / A | 50 µL/min B1 through shunt and cell | Substrate blank current recorded | 10.0 |
| 29.5 | **Readout**: sweep product plug into cell; integrate charge | L2 | A / A | 50 µL/min B1 (pusher) | CA (or pulsed); integrate | 2.0 |
| 31.5 | Aspirate regeneration plug | L3 | A / B | 200 µL/min A1 | Electrode conditioning (optional) | 1.0 |
| 32.5 | **t₀(L3)**; 100 µL glycine pH 2 through reactor; loop flush 750 µL | L3 | A / B | 300 µL/min A1 | — | 2.5 |
| 35.0 | Re-equilibration (≥ 60 bed volumes) | L3 | A / B | 200 µL/min A1 | Baseline | 3.0 |
| 38.0 | **Cycle end** (next cycle's L1 aspiration may overlap) | — | — | — | — | — |

**Total ≈ 38 min.** Variants (Derived from the same step times):

| Variant | Change | Cycle time (min) |
|---|---|---|
| Substrate injected from a 4 °C vial instead of B1 | + cleaning injection to waste (1.0 + 2.5 min) + substrate injection line (1.0 + 1.5 min) | ≈ 44 |
| Sample loaded at 50 µL/min (longer bed residence) | 750 µL at 50 µL/min = 15 min (+7.5) | ≈ 45.5 |
| Sample PLPA 97 µL | same loop flush as PLNO | ≈ 38 |
| 100 µL loop, PLNO 75 µL, 50 µL/min | 300 µL at 50 µL/min = 6 min (−1.5) | ≈ 36.5 |
| Optional stopped-flow sample incubation | + 5 min | + 5 |
| Worst plausible combination | injected substrate + 50 µL/min loading + sample incubation + 15 min accumulation | ≈ 61.5 (**over budget**) |

All variants except the worst combination fit in 60 min. Flow rates are within the BSM range [V]; durations
are design variables for the simulation. Every BSM change (A1 → B1 → A1) is made with the reactor either
perfused at high flow or isolated, so the ≤ 100 µL delay volume [V] costs ≤ 0.5 min per change.

### 7.5 Volume and dispersion budget (Scheme B)

| Segment | Volume (µL) | Basis |
|---|---|---|
| BSM mixer → injection valve (restrictor, tubing) | part of ≤ 85–100 µL system delay | V: WAT_PREMIER_SPEC, WAT_ICLASS_SPEC |
| Sample loop (online only until Loop Offline) | 250 (or 100) | V: WAT_PREMIER_SPEC |
| Injection valve passage | 0.1 | V: WAT_INJ_MODES |
| Injection valve → V10: 15 cm × 127 µm | 1.9 | Derived |
| V10 → reactor → V10: 2 × 5 cm | 1.3 | Derived |
| External valve internal passages | 0.1–1 per pass | UNVERIFIED |
| Reactor bed (10 µL; void ≈ 4 µL) | 10 / 4 | Derived, porosity UNVERIFIED |
| V10 → V6 → EC cell: 10 cm | 1.3 | Derived |
| EC cell | 0.02–4.3 | §5 |
| EC cell → optical detector: 30 cm PEEK | 3.8 | Derived |

Product-plug broadening between reactor and cell: σ_V ≈ 0.5–1.5 µL for a small molecule
(D ≈ 1 × 10⁻⁹ m²/s, UNVERIFIED value) at 10–100 µL/min over ≤ 0.3 m of 127 µm tubing. The transit time
(≈ 2–8 s) is comparable to r²/D ≈ 4 s, so neither the Taylor nor the pure-convection limit applies; the
simulation should use a laminar convection–diffusion model (as in §2.4 c). The readout peak width is set
mainly by the **bed void volume and bed dispersion**, not the tubing. Sample-plug dilution is set by the
**loop** (§2.4 c), not the tubing.

---

## 8. Risks and open questions

### Questions for the user (Q)

1. **Which generation is installed** (original ACQUITY UPLC, I-Class, I-Class PLUS, Premier)? BSM firmware
   version (Premier ≥ 1.71 allows 1 µL/min)? Read the module labels or the Empower instrument configuration.
2. **SM-FL hardware**: installed loop volume, loop material and internal diameter; installed sample syringe
   (100/250/500 µL); needle size (10 or 20 µL — sets the PLNO pre-sample volume 7 or 10 µL [V: WKB11277]).
   Are 250 µL loop + 500 µL syringe kits available or to be bought?
3. Flow-path type: standard steel, Bio (titanium/PEEK) or Premier (MaxPeak HPS)? (Protein adsorption,
   low-pH corrosion.)
4. Is it acceptable that the user loads samples into vials that **already contain** conjugate (only way to
   get an in-vial homogeneous incubation on an SM-FL)?
5. **Empower** version and options: is the **Empower Toolkit** licensed, and can it start a sample set and
   report status on this installation (ask Waters)? Is Loop Offline/Load Ahead visible in the SM-FL
   instrument method?
6. **Rear-panel I/O** of BSM and SM-FL: number and type (relay/TTL) of event outputs and inputs, ratings,
   inject-hold/external-start inputs, Inject Start pulse width. Photograph the rear panels.
7. **External valve** model: 6- or 10-port, actuator, trigger interface (contact/TTL, BCD, RS-232/USB),
   pressure rating, rotor material, internal volumes, switching time. Can a second valve be bought?
8. Optical detector model (TUV/PDA/FLR), flow-cell pressure rating; is a Waters analog-input interface
   available (to log the Gamry analog out in Empower)?
9. PC/OS for Gamry: Windows 10/11, Gamry software ≥ 7.10.4, ToolkitPy and Echem Toolkit licences held?
10. Is a second potentiostat (Reference 620) acceptable for redox cycling, and will Gamry support a
    600+/620 bipotentiostat pair?

### Bench risks (R)

| ID | Risk | Mitigation / test |
|---|---|---|
| R1 | IgG loss on vial, needle, needle-to-valve path and loop at fM concentrations | Spike-recovery of labelled IgG through the SM-FL at 1–1000 pg/mL, PLNO vs PLPA; carrier protein; HPS/PEEK loop |
| R2 | **Conjugate carryover in the loop/needle into the next injection** (substrate or next sample) — raises the blank directly | Substrate from BSM; cleaning injection to waste; detergent strong wash; blank-after-high tests |
| R3 | Incomplete or variable transfer out of the loop (laminar, low D) | Loop online ≥ 3 V_loop; verify with TUV at 280 nm; smaller-ID loop |
| R4 | Electrode fouling by protein and low pH | Cell bypass (Scheme B); EC cleaning pulses; disposable SPE during development |
| R5 | PLPA air gaps forming bubbles in reactor or cell | Use PLNO, or bypass the cell during loading; back-pressure at cell outlet |
| R6 | BSM below specified precision at 20–100 µL/min; pressure < 1000 psi | Gravimetric flow check; restrictors in series |
| R7 | Mains/pump noise via grounded fluid path | PEEK isolation lengths, Faraday cage, stopped-flow readout, mains-cycle integration |
| R8 | Substrate auto-hydrolysis in the BSM line (if B1 = substrate) | Measure blank current vs reservoir age; fall back to injection from a 4 °C vial |
| R9 | Contact-closure timing, Empower inter-line overhead | Timestamp on one clock; measure overhead; calibrate plug arrival by TUV daily |
| R10 | ToolkitPy tied to 32-bit Python 3.7 | Separate worker process; pin versions |
| R11 | Ref 600+ discontinued | Plan Reference 620 |
| R12 | No column heater in the fixed list; reactor temperature drift | Thermostat the reactor (purchase) |

---

## 9. References

Waters documents (Waters Corporation, Milford MA):

- **WAT_PREMIER_SPEC** — "ACQUITY Premier with Binary Solvent Management — Instrument Specifications",
  720007029EN (Nov 2022). Contains BSM, SM-FTN and **SM-FL** specifications. Reached via
  https://kr-support.waters.com/@api/deki/files/20438/Premier_specs_720007029en.pdf?revision=1 [V]
- **WAT_ICLASS_SPEC** — "ACQUITY UPLC I-Class System Instrument Specifications", 720003948EN (configuration
  with the flow-through-needle sampler; used here **only for the BSM and system values**). Mirror:
  https://ucrf.unist.ac.kr/wp-content/uploads/2024/11/ACQ.-I-Class-PLUS-Sys.-CH-A-wSM-FTN-I-Specification.pdf [V]
- **WAT_ICLASS_PLUS_FL** — "ACQUITY UPLC I-Class PLUS System (SM-FL) Instrument Specifications":
  https://lcms.labrulez.com/paper/14643 (blocked; values from search summary) [S]
- **WAT_INJ_MODES** — "ACQUITY UPLC Injection Modes" (Waters training slides, 20 pp., attached to WKB22445):
  https://support.waters.com/@api/deki/files/30235/ACQUITY_UPLC_Injection_Modes.pdf?revision=1 [V]
- **WAT_LOADAHEAD** — "ACQUITY Cycle Time Definition w load ahead" (attached to WKB8852):
  https://support.waters.com/@api/deki/files/1478/ACQUITY_Cycle_Time_Definition_w_load_ahead.pdf?revision=1 [V]
- **WKB2345** — "What is the minimum and maximum injection volume for each sample loop size used with the
  ACQUITY Sample Manager" (table image MAX_injection_volume.PNG):
  https://support.waters.com/KB_Inst/Chromatography/WKB2345_What_is_the_minimum_and_maximum_injection_volume_for_each_sample_loop_size_used_with_the_ACQUITY_Sample_Manager [V]
- **WKB22445** — "What are the injection modes with an ACQUITY UPLC?":
  https://support.waters.com/KB_Inst/Chromatography/WKB22445_What_are_the_different_injection_modes_in_Acquity_UPLC [V]
- **WKB11277** — "How much sample is consumed using the partial loop with needle overfill injection mode on
  the ACQUITY UPLC Sample Manager":
  https://support.waters.com/KB_Inst/Chromatography/WKB11277_How_much_sample_is_consumed_using_the_partial_loop_with_needle_overfill_injection_mode_on_the_ACQUITY_UPLC_Sample_Manager [V]
- **WKB198538** — "How much sample is consumed in Full Loop Mode for the ACQUITY UPLC Sample Manager and
  ACQUITY UPLC I-Class Sample Manager FL":
  https://support.waters.com/KB_Inst/Chromatography/WKB198538_How_much_sample_is_consumed_in_Full_Loop_Mode_for_the_ACQUITY_UPLC_Sample_Manager_and_ACQUITY_UPLC_I-Class_Sample_Manager_FL [V]
- **WKB56017** — "Carryover seen with an ACQUITY I-Class SM-FL":
  https://support.waters.com/KB_Inst/Chromatography/WKB56017_Carryover_seen_with_an_ACQUITY_I-Class_SM-FL [V]
- **WKB9108** — "How to cycle the injection valve during an injection using the ACQUITY Sample Manager":
  https://support.waters.com/KB_Inst/Chromatography/WKB9108_How_to_cycle_the_injection_valve_during_an_injection_using_the_ACQUITY_Sample_Manager [V]
- **WKB205077** — "ACQUITY UPLC Sample Manager: How to clean the needle using a strong wash solvent and a weak
  wash solvent":
  https://support.waters.com/KB_Inst/Chromatography/WKB205077_ACQUITY_UPLC_Sample_Manager_How_to_clean_the_needle_using_a_strong_wash_solvent_and_a_weak_wash_solvent [V]
- **WKB3589** — "What are the ACQUITY Sample Manager syringe and loop kit part numbers":
  https://support.waters.com/KB_Inst/Chromatography/WKB3589_What_are_the_ACQUITY_Sample_Manager_syringe_and_loop_kit_part_numbers [V]
- **WKB110704** — "What is the part number for the (I-)Class ACQUITY SM sample syringe":
  https://support.waters.com/KB_Inst/Chromatography/WKB110704_What_is_the_part_number_for_the_Class_Acquity_SM_sample_syringe [V]
- **WKB13017** — "How to set up auto addition in MassLynx" (states auto-addition is not compatible with the
  SM-FL): https://support.waters.com/KB_Inf/MassLynx/WKB13017_How_to_set_up_auto_addition_in_MassLynx [V]
- **WKB8852** — "Is there documentation that explains the load ahead option with the ACQUITY UPLC Sample
  Manager": https://support.waters.com/KB_Inst/Chromatography/WKB8852_Is_there_documentation_that_explains_the_load_ahead_option_with_the_ACQUITY_UPLC_Sample_Manager [S for text; attachment V]
- **WKB221963** — "What does the Automatic setting of Loop Offline mean":
  https://support.waters.com/KB_Inst/Chromatography/WKB221963_What_does_the_Automatic_setting_of_Loop_Offline_mean [S]
- **WKB55803** — "Does the ACQUITY Sample Manager have an Inject Start contact closure connection":
  https://support.waters.com/KB_Inst/Chromatography/WKB55803_Does_the_Acquity_Sample_Manager_have_an_Inject_Start_contact_closure_connection [V]
- **WKB32564** — "What is the minimum backpressure required for good UPLC performance":
  https://support.waters.com/KB_Inst/Chromatography/WKB32564_What_is_the_minimun_backpressure_required_for_good_UPLC_performance [V]
- **WKB5084** — "Part number for the flow restrictor used to increase system backpressure on the ACQUITY BSM
  or H-Class QSM":
  https://support.waters.com/KB_Inst/Chromatography/WKB5084_What_is_the_part_number_for_the_flow_restrictor_used_to_increase_system_backpressure_on_the_ACQUITY_BSM_or_H-Class_QSM [V]
- **WKB96281** — "How to adjust the seal wash solvent interval":
  https://support.waters.com/KB_Inst/Chromatography/WKB96281_How_to_adjust_the_seal_wash_solvent_interval [S]
- **WKB14943** — "Solvent recommendations for ACQUITY H-Class washes":
  https://support.waters.com/KB_Inst/Chromatography/WKB14943_What_are_the_solvent_recommendations_for_the_ACQUITY_H-Class_washes_seal_wash_wash_solvent_purge_solvent [S]
- **WKB27360** — "How to connect an external Solvent Select Valve to a Solvent Manager" (login-gated):
  https://support.waters.com/KB_Inst/Chromatography/WKB27360_How_to_connect_an_external_Solvent_Select_Valve_SSV_to_an_I-Class_BSM [S]
- **WAT_CARRYOVER_APPNOTE** — "ACQUITY UPLC I-Class: Minimizing carryover to enhance LC-MS/MS quantitative
  range" (2011):
  https://www.waters.com/nextgen/is/en/library/application-notes/2011/acquity-uplc-i-class-minimizing-carryover-enhance-lc-ms-ms-quantitative-range.html [S]
- **WAT_APPNOTE_720008786** — "Implementing Programmed Injection Techniques in Empower CDS: A Practical Guide"
  (2025):
  https://www.waters.com/nextgen/en/library/application-notes/2025/implementing-programmed-injection-techniques-in-empower-cds-a-practical-guide.html [S; not opened]
- **WAT_TUV** — ACQUITY UPLC / Premier Tunable UV detectors product page:
  https://www.waters.com/nextgen/us/en/products/chromatography/chromatography-detectors/acquity-uplc-and-acquity-premier-tunable-uv-detectors.html [S]
- **WAT_TOOLKIT_FORUM** — Waters Community, "Empower tool kit purpose" (cites the Empower Toolkit
  Programmer's Reference Guide 71500031805): https://forums.waters.com/discussion/comment/6457/ [S]
- **WAT_SSG** — "Automated creation of chromatographic methods … using an Empower Sample Set Generator" (2024):
  https://www.waters.com/nextgen/id/en/library/application-notes/2024/automated-creation-of-chromatographic-methods-for-analytical-method-development-using-an-empower-sample-set-generator.html [S]
- **TETRA_EMPOWER** — Tetra Empower Agent, "Create Sample Set Method Command":
  https://developers.tetrascience.com/docs/tetra-empower-agent-create-sample-set-method-command [S]
- **MANUALSLIB_ICLASS** — Waters ACQUITY UPLC I-Class System manual (pp. 19–20, SM-FL description):
  https://manualslib.com/manual/2912657/Waters-Acquity-Uplc-I-Class.html?page=19 [P; p. 20 partially V]

Gamry Instruments:

- **GAMRY_REF600P_DS** — "Reference 600+ Potentiostat/Galvanostat/ZRA" data sheet (2018):
  https://www.gamry.com/assets/Uploads/Reference-600+2018.pdf [V]
- **GAMRY_REF600P_LEGACY** — Reference 600+ legacy specifications page:
  https://www.gamry.com/support-2/legacy-devices/reference-600plus-legacy/ [V]
- **GAMRY_TKPY_QSG** — "Echem ToolkitPy Installation Quick-Start Guide", 988-00100 Rev 1.0:
  https://www.gamry.com/assets/988-00100-ToolkitPy-QSG.pdf [V]
- **GAMRY_TKPY_BROCH** — "Electrochemistry ToolkitPy" brochure, Rev 1.0 (11/4/2024):
  https://cn.gamry.com/assets/Uploads/ToolKitPy-Brochure-final.pdf [V]
- **GAMRY_TKPY_WEB** — Echem ToolkitPy support page: https://www.gamry.com/support-2/software/echem-toolkitpy/ [S]
- **GAMRY_TK_V2** — "Gamry Electrochemistry Toolkit" (Rev 1.0, 2018):
  https://www.gamry.com/assets/Uploads-v2/Echem-ToolKit-v2.pdf [P]
- **GAMRY_IO_APPNOTE** — "Customizing Experiments Using the I/O Capabilities":
  https://www.gamry.com/application-notes/instrumentation/using-io-capabilities/ [V]
- **GAMRY_TRIGGER_APPNOTE** — "Trigger a Spectrometer with Gamry Potentiostats":
  https://www.gamry.com/application-notes/software-scripting/trigger-a-spectrometer-gamry-potentiostats/ [P]
- **GAMRY_SMALLSIG_APPNOTE** — "Measurement of Small Electrochemical Signals":
  https://www.gamry.com/application-notes/instrumentation/measurement-of-small-electrochemical-signals [P]
- **GAMRY_BIPOT_NOTE** — "BiPotentiostat Installation and Setup":
  https://www.gamry.com/assets/Support-Downloads/Installation-Notes/BiPotentiostat-Installation.pdf [S]

Flow cells, electrodes, columns:

- **ANTEC_SENCELL** — https://antecscientific.com/products/sencell/ [V]
- **ANTEC_DECADE** — DECADE Elite brochure:
  https://lcms.labrulez.com/labrulez-bucket-strapi-h3hsga3/Decade_Elite_4a672baa85.pdf [S]
- **METROHM_TL_MANUAL** — Metrohm Thin-Layer cell manual, technical specifications p. 26:
  https://www.manualsdir.com/manuals/586940/metrohm-thin-layer-cell.html?page=26 [V]
- **METROHM_FLWCL** — DRP-FLWCL-PEEK scope-of-delivery sheet:
  https://www.metrohm.com/content/metrohm/shared/en/products/d/rp-f/drp-flwcl-peek.download.pdf [V]
- **BASI_GASKETS** — https://basinc.com/products/ec/gaskets ; https://basinc.com/products/ec/flowcells [S]
- **BASI_IDA** — https://www.basinc.com/thin-film-interdigitated-micro-array-electrodes_ [P]
- **MICRUX_IDRA / MICRUX_AIO** — https://www.directindustry.com/prod/micrux-fluidic/product-240350-2603297.html ;
  https://www.palmsens.com/product/micrux-one-cell/ [S]
- **THERMO_6011RS** — Dionex 6011RS ultra Analytical Cell specifications, PS70255-EN:
  https://assets.thermofisher.com/TFS-Assets/CMD/Specification-Sheets/PS-70255-LC-Dionex-6011RS-ultra-Analytical-Cell-PN70255-EN.pdf [V]
- **SARTORIUS_CIMAC** — https://sartorius.hr/media/qxap00q3/cimac-datasheet-en-b-sartorius.pdf [S]
- **THERMO_POROS_A** — https://www.thermofisher.com/order/catalog/product/1502412 [S]

Papers (bibliographic details matched to PubMed records in this session where marked; content claims
carried from the previous draft are [P]):

- **LARSEN2012** — Larsen ST, Heien ML, Taboryski R. Amperometric noise at thin film band electrodes. *Anal.
  Chem.* 2012, 84, 7744–7749. doi:10.1021/ac301136x (PMID 22928986) [V record]
- **NIWA1993** — Niwa O, Xu Y, Halsall HB, Heineman WR. Small-volume voltammetric detection of 4-aminophenol
  with interdigitated array electrodes and its application to electrochemical enzyme immunoassay. *Anal.
  Chem.* 1993, 65, 1559–1563. doi:10.1021/ac00059a013 (PMID 8328672) [V record]
- **HAN2014** — Han D, Kim Y-R, Kang CM, Chung TD. Electrochemical signal amplification for immunosensor based
  on 3D interdigitated array electrodes. *Anal. Chem.* 2014, 86, 5991–5998. doi:10.1021/ac501120y
  (PMID 24842332) [V record]
- **HIRAKAWA2006** — Hirakawa K, et al. Electrochemical immunoassay for vitellogenin based on sequential
  injection using antigen-immobilized magnetic microbeads. *Anal. Sci.* 2006, 22, 81–86.
  doi:10.2116/analsci.22.81 (PMID 16429778) [V record]
- **GRATE2009** — Grate JW, et al. Renewable surface fluorescence sandwich immunoassay biosensor … *Analyst*
  2009, 134, 987–996. doi:10.1039/b900794f (PMID 19381395) [V record]
- **TRAU1997** — Trau D, et al. Development of an amperometric flow injection immunoanalysis system … *Biosens.
  Bioelectron.* 1997, 12, 499–510. doi:10.1016/s0956-5663(97)00007-9 (PMID 9253154) [V record]
- **SHARMA2018** — Sharma D, Lee J, Shin H. *Biosens. Bioelectron.* 2018, 107, 10–16.
  doi:10.1016/j.bios.2018.02.010 [P]
- **KIM2004** — Kim SK, Hesketh PJ, et al. Fabrication of comb interdigitated electrodes array (IDA) for a
  microbead-based electrochemical assay system. *Biosens. Bioelectron.* 2004, 20, 887–894.
  doi:10.1016/j.bios.2004.04.004 [P]
- **PALMER1992** — Palmer DA, Edmonds TE, Seare NJ. Flow injection electrochemical enzyme immunoassay for
  theophylline using a protein A immunoreactor … *Analyst* 1992, 117, 1679–1682. doi:10.1039/an9921701679 [P]
- **LUNTE1985** — Lunte CE, et al. Difference mode detection with thin-layer dual-electrode liquid
  chromatography/electrochemistry. *Anal. Chem.* 1985 (DOI not retrieved, UNVERIFIED)
- **Chang2012** — diffusion coefficient of IgG, via `params/chemistry.yaml` (Task 1 reference list).

**Access notes (this session).** Not reachable: help.waters.com PDFs (403/redirect), Waters application-note
pages (503), labrulez/icpms.cz/gcms.cz PDF mirrors (bot block), manualshive.com (bot block),
chemistry.unt.edu and condor.depaul.edu ACQUITY manuals (TLS chain not trusted — not bypassed), login-gated
Waters KB articles (WKB27360). Values that depend on them are marked [S] or UNVERIFIED. The ACQUITY rear-panel
I/O pin tables were not found in any reachable document.
