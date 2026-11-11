# 02 — Hardware, fluidics and automation

Task 2 of the automated electrochemical ELISA project (human IgG, LOD ≤ 1 pg/mL, ≤ 100 µL sample, ≤ 60 min,
reusable capture surface). Scope: instruments, fluidics, cells, reactors, control and synchronisation.
Chemistry and immunology (antibodies, enzyme label, substrate kinetics) belong to the parallel literature task
and are referred to here only where they constrain the hardware.

Machine-readable parameters for the simulation are in `params/hardware.yaml`. Every key there has a
`source` matching a key in the reference list at the end of this file (§9).

**How to read the evidence labels**

- **[V]** = checked this session against the cited document (vendor spec sheet, manual page, knowledge-base
  article or paper abstract).
- **[S]** = taken from a search-engine summary of the cited page; the page itself could not be opened.
  Treat as medium confidence.
- **UNVERIFIED** = not checked against any source this session (engineering estimate or recollection).
  It must be confirmed before anyone relies on it.
- **Derived** = calculated here from verified inputs; the formula is given.

> **Naming conflict to resolve first (Q1, §8).** The brief calls the sampler "ACQUITY **SM-FL** (Sample
> Manager, **Flow-Through Needle**)". In Waters' naming these are two different modules. The **SM-FTN** has a
> flow-through needle. The **SM-FL** is the *fixed-loop* sampler, which has a puncture needle, a sample needle
> and a loop [V: MANUALSLIB_ICLASS]. This document assumes **SM-FTN**, because that is what the description
> says. Where the FL would behave differently, §2.6 says so. Check the module label or the Empower
> instrument configuration.
>
> **System generation is also unknown.** It could be an ACQUITY UPLC (classic), H-Class Bio with BSM,
> I-Class or I-Class PLUS. The numbers below come from the **I-Class (SM-FTN) specification
> 720003948EN** [V]. Other generations differ in detail: for example, the H-Class FTN has 15 µL and 30 µL
> needle options [V: WKB67734].

---

## 1. Waters ACQUITY Binary Solvent Manager (BSM)

### 1.1 Verified specifications (I-Class BSM, doc 720003948EN) [V: WAT_ICLASS_FTN_SPEC]

| Item | Value |
|---|---|
| Flow-rate range | 0.010–2.000 mL/min in 0.001 mL/min steps (10–2000 µL/min) |
| Maximum pressure | 18 000 psi (1241 bar) up to 1 mL/min; 12 000 psi up to 2 mL/min |
| Flow accuracy | ±1.0 % of set flow at 0.500 mL/min |
| Flow precision | 0.075 % RSD or 0.01 min SD (whichever is greater), **specified only for 0.2–2.0 mL/min** |
| Compositional precision / accuracy | < 0.15 % RSD; ±0.5 % absolute (5–95 % B), both specified for 0.2–2.0 mL/min |
| Solvents | "Up to four, in combination of two, A1 or A2 and B1 or B2" |
| Degassing | Integrated; six lines, two of them allocated to the injector wash and purge solvents |
| Mixer | 50 µL standard; 100 µL and 380 µL optional |
| Total system delay volume | < 100 µL (default configuration, whole system) |
| pH range | 2–12 |
| Seal wash | Programmable active wash of the rear of the high-pressure seals and the plungers |
| Primary wetted materials | 316L stainless steel, UHMWPE blend, MP35N, titanium alloy, gold, sapphire, ruby, zirconia, Nitronic 60, DLC, fluoropolymer, PEEK and PEEK blend |
| Event I/O (system) | "Rear panel contact closure and/or TTL inputs/outputs" |

### 1.2 What this means for an immunoassay

- **Low flow.** The minimum programmable flow is **10 µL/min**. Flows of 1–5 µL/min are not possible with
  this pump. Precision below 0.2 mL/min is **not specified** (UNVERIFIED; expect it to worsen at 10 µL/min,
  where compressibility and check-valve behaviour dominate). Incubation steps that need sub-10 µL/min
  perfusion should therefore use **stopped flow** in the reactor (§7), not slow pumping.
- **Stopped flow.** The BSM spec sheet does not say whether a 0.000 mL/min step is allowed in the gradient
  table (UNVERIFIED). The robust approach does not depend on it. The BSM keeps pumping, for example at
  50–200 µL/min, and the **external switching valve** isolates or bypasses the reactor and/or the cell, so the
  liquid in the reactor is stationary. This also keeps the pump pressurised (next point).
- **Minimum back-pressure.** A Waters knowledge-base article says the check valves "require a certain level
  of back pressure … generally … above 1000 psi" (~69 bar) [S: WKB32564]. A Waters restrictor
  (P/N 205000547, 40 µm × 35 cm PEEKsil) is fitted between the mixer and the injector to add more than
  2000 psi [S: WKB5084].
  - **Design consequence:** put the restrictor **upstream of the injector**. The pump then sees more than
    1000 psi while everything downstream sees only a low pressure: the reactor, the EC cell (0.8–4 MPa limits,
    §5) and the TUV cell (1000 psi). At 10–100 µL/min of aqueous buffer the restrictor alone may give less
    than 1000 psi. Its pressure scales linearly with flow, so it was specified at higher flow
    (UNVERIFIED at our flows). A second restrictor, or a longer or narrower one, may be needed. **Measure the
    pressure at the bench.**
- **Reagent lines.** Only **4 BSM lines** are available (A1, A2, B1, B2), and any two of them can be pumped at
  a time. A2 versus A1 (and B2 versus B1) is selected with a solvent-select valve, not by mixing. A suggested
  allocation:
  - A1: running/wash buffer (e.g. PBS-T or Tris-T)
  - A2: substrate buffer without substrate (e.g. the enzyme buffer for the chosen label)
  - B1: regeneration solution (e.g. glycine-HCl pH 2–2.5; chemistry task to confirm)
  - B2: water/20 % MeOH or a storage/cleaning solution
  
  The **substrate itself should not sit in a BSM line**. Pump heads, the degasser and the mixer add
  millilitres of hold-up, and substrates such as p-aminophenyl phosphate hydrolyse spontaneously. Inject the
  substrate as a plug from a cooled vial through the sampler (§2) instead. If more reagent lines are needed,
  Waters supports an external solvent-select valve on the BSM, wired to event outputs [S: WKB27360]. That
  article is behind a login, so the wiring details are UNVERIFIED.
- **Delay and dwell volume.** The whole system is < 100 µL [V]. For an FTN system the **needle plus any
  extension loop are in the flow path permanently** [V: MANUALSLIB_ICLASS]. A 100 µL extension loop
  therefore adds about 100 µL of dwell between the pump and the reactor.
  - At 10 µL/min that is about 10 min of dead time for every change of BSM buffer, which is
    **unacceptable**.
  - **Mitigation:** run every buffer change at high flow, e.g. 0.3–0.5 mL/min, with the cell bypassed. Use a
    small loop if the sample volume allows. Or route the BSM to the reactor through the external valve so the
    injector loop is bypassed (Scheme B, §7).
- **Wetted materials and compatibility.**
  - **High-salt aqueous buffers and chloride.** The pH range (2–12) covers PBS and glycine pH 2. 316L
    stainless steel in chloride is a known pitting and crevice-corrosion risk when salt is left standing
    (UNVERIFIED for this system). Never leave buffer in the system overnight: flush to water, then
    10–20 % MeOH.
  - **Seal wash.** Waters recommends 90:10 water/methanol for seal wash and advises against 100 % organic. With
    ≥ 100 mM salt, shorten the seal-wash interval. Waters examples give 0.5 min instead of the 5 min default
    for H-Class Bio [S: WKB96281, WKB14943]. The seal wash must never run dry [S].
  - **Low-pH glycine.** pH 2 is the edge of the spec, so keep regeneration exposure short and flush promptly.
  - **Surfactants.** Tween-20 at 0.05 % is commonly used in UPLC. The degasser is fine, but foam in reservoirs
    can make priming awkward (UNVERIFIED).
  - **Proteins.** Protein-rich solutions (BSA blocking, conjugate) should **not** be pumped from BSM lines.
    They adsorb on stainless steel and titanium frits and the mixer, and degrade check valves (UNVERIFIED but
    standard practice). Deliver proteins only by injection.
  - **Enzyme substrates.** Same as proteins: inject them, do not pump them.
  - **Hardware option.** Waters sells bio-inert "Premier/MaxPeak HPS" and "Bio" (titanium/PEEK) flow paths.
    This system's flow-path type is unknown (Q2).

---

## 2. Waters ACQUITY Sample Manager — Flow-Through Needle (SM-FTN)

### 2.1 Verified specifications (I-Class SM-FTN, 720003948EN) [V: WAT_ICLASS_FTN_SPEC]

| Item | Value |
|---|---|
| Injection volume | 0.1–10.0 µL standard; **up to 1000.0 µL with optional extension loop** |
| Accuracy | ±0.2 µL (10 µL injections, 100 µL syringe) |
| Precision | < 1 % area RSD (0.2–1.9 µL); < 0.5 % RSD (2–10 µL) |
| Linearity | > 0.999 |
| Carryover (UV, caffeine) | < 0.004 %; < 0.001 % typical |
| Sample capacity | Any two of: 96/384 plates; 48 × 2 mL vials; 48 × 0.65 mL tubes; 24 × 1.5 mL tubes |
| Sample-compartment temperature | **4.0–40.0 °C**, 0.1 °C steps; accuracy ±0.5 °C, stability ±1.0 °C at sensor |
| Minimum sample | 3 µL residual in a total-recovery 2 mL vial |
| Needle wash | Integrated, active, programmable |
| Advanced functions | **Auto-dilution and auto-addition** |
| Wetted materials | 316L stainless steel, polyimide, PEEK blend, DLC, PPS |

Additional, from the Waters knowledge base:

- H-Class FTN needles of 15 µL (0.1–10 µL injections) and 30 µL (0.1–25 µL) [V: WKB67734].
- Extension loops of 50, 100 and 250 µL, giving "up to" 50/100/250 µL [V: WKB67734]. The 1000 µL loop is
  from the I-Class spec [V].
- Maximum injection: needle volume minus 5 µL without an extension loop; 100 % of the extension loop when
  one is fitted [V: WKB7947]. A general rule of 75 % of needle plus loop is also quoted [V: WKB67734].
- Standard sample syringe: 100 µL, P/N 700002570 [V: WKB60785].

### 2.2 Sample volume

A full **100 µL sample injection** needs an extension loop of at least 100 µL. A 250 µL loop gives headroom
and avoids running at the loop limit, where recovery suffers [S: WKB67734 note on reduced recovery]. The cost
is dwell volume (§1.2). The loop is also stainless steel or PEEK and wetted by every reagent, so it is a
protein-adsorption and carryover surface. Its material depends on the part, which is to be chosen
(UNVERIFIED).

### 2.3 Wash solvents

The FTN has a wash solvent and a purge solvent, on two of the six degasser lines [V: WAT_ICLASS_FTN_SPEC].
For this assay a suggested choice:

- **Purge** = running buffer. The FTN auto-dilution dispenses *purge* solvent into the vial, so the purge must
  be compatible with the sample [V: WKB67492].
- **Wash** = buffer + 0.05 % Tween-20, or a dilute detergent / 10 % MeOH, to strip protein from the needle
  exterior (UNVERIFIED efficacy for IgG; bench test).

### 2.4 Multi-plug, sequential and in-vial operations under Empower

- **Auto-additions** [V: WKB1416]. In the Empower Run Samples window, the Auto-Additions Editor programs extra
  draws by plate/well and volume, with a delay in minutes. The sampler aspirates from several vials into the
  needle (and loop) and **mixes inside the needle** by displacement: Mix Cycles and Mix Stroke Volume,
  0–99 each. It then injects the combined volume as **one** plug.
  - Known issue: the delay is ignored unless at least one mix cycle is programmed [V].
  - Empower 3.6.0 and later add "In-Needle Auto Additions", which list the full draw sequence
    [S: WAT_APPNOTE_720008786; the app note itself could not be opened].
  - **Air gaps** between drawn plugs are **not documented** in anything reached this session (UNVERIFIED).
    Air must not enter a UPLC flow path or an EC thin-layer cell anyway, because a bubble on the working
    electrode is fatal to the baseline.
- **Auto-dilution** [V: WKB67492]. Dispenses a set volume of purge solvent into the vial, waits an optional
  post-dilution delay, then aspirates and injects.
  - In-vial reagent mixing *from another vial* (vial-to-vial transfer) is **not** described by these
    articles (UNVERIFIED). The FTN's auto-addition mixes in the needle, not in a destination vial.
- **Sample, then conjugate, then substrate as separate plugs.** This is done with **separate injections**:
  one sample-set line per plug, each with its own instrument method and run time, run automatically in
  sequence by Empower. A single injection carrying three plugs separated by buffer is *not* a documented FTN
  function, and is UNVERIFIED.
  - Overhead between lines is the injection cycle: "< 15 s inject to inject, with load ahead" for small
    injections [V: WAT_ICLASS_FTN_SPEC].
  - For 100 µL draws, the syringe draw rate dominates. At an assumed draw rate of 10–50 µL/s for viscous
    protein solutions, a 100 µL draw takes about 2–10 s plus needle and wash moves (UNVERIFIED).
  - Budget **≈ 1 min per injection** in the timeline (§7.4) until it is measured.
  - "Cycle Inject Valve" can be programmed as a timed run event [V: WKB9108]. This lets a loop be switched out
    of the flow path mid-run. With the FTN the needle stays in-line, so this does not remove the needle
    volume.
- **In-vial incubation.** The compartment holds 4–40 °C [V], so a homogeneous pre-incubation (sample +
  detection conjugate) can happen in a vial at, for example, 25–37 °C.
  - The reagents can be combined by auto-addition (draw both into the needle, mix, inject), which goes
    straight into the flow path; or by a pre-dispensed vial prepared by the user. The latter is a manual step,
    not allowed by the brief.
  - True in-vial mixing therefore needs either a Waters "Sample Prep" function that dispenses from one vial
    into another (UNVERIFIED; see the app note above and Q3) or a different autosampler.
  - Fall-back: **in-needle/in-loop incubation**. Draw sample + conjugate, mix in the needle, then wait
    (delay) before injecting.

### 2.5 Protein adsorption and dispersion

- **Adsorption.** Stainless steel, PEEK, polyimide and DLC are all wetted [V], and IgG at 1 pg/mL
  (≈ 6.7 fM) is far below the concentration at which surfaces saturate. Losses to the needle, loop and
  tubing walls are therefore plausible.
  - Example: adsorbing 1 % of a monolayer (≈ 2 ng/cm² for IgG monolayer, UNVERIFIED typical value) on about
    1 cm² of needle and loop wall would exceed the 100 fg present in a 100 µL sample by orders of magnitude.
  - **Mitigation (to be validated):** carrier protein (BSA, 0.1–1 %) and Tween in sample diluent and running
    buffer; passivate with a high-concentration BSA injection; consider the Premier/bio-inert flow path. The
    chemistry task to confirm. **This is a key bench risk (R1).**
- **Dispersion of a plug to the capture site.** Use Taylor–Aris dispersion for laminar flow in tubing of
  radius *r*, length *L*, flow *Q*, diffusion coefficient *D*:

  σ_V² = π r⁴ Q L / (24 D)   (volume variance; Taylor 1953 [UNVERIFIED citation details])

  This is valid only when the residence time is much longer than r²/D.

  | Q (µL/min) | IgG (D ≈ 4×10⁻¹¹ m²/s): σ_V (µL) | small molecule (D ≈ 8×10⁻¹⁰ m²/s): σ_V (µL) | residence time (s) |
  |---|---|---|---|
  | 10 | 2.1 | 0.47 | 38 |
  | 100 | 6.7 | 1.5 | 3.8 |
  | 500 | 14.9 | 3.3 | 0.8 |

  (Derived for 0.005″ (127 µm) ID × 0.5 m tubing; D values UNVERIFIED and to come from the chemistry task.)
  - For IgG, r²/D ≈ 100 s exceeds the residence time. The Taylor regime is **not** reached and dispersion is
    convective (parabolic-profile) dominated. The simulation should use a full convection–diffusion model,
    or treat the transfer line as a laminar-flow residence-time distribution.
  - Practical rule: keep the line between injector and reactor at **≤ 0.005″ ID and ≤ 30 cm**
    (≈ 3.8 µL; 12.7 µL/m [Derived]). A 100 µL sample plug then arrives essentially undiluted (≤ 10 %
    broadening).

### 2.6 If the sampler is in fact an SM-FL (fixed loop)

- A fixed-loop design uses partial-loop-with-needle-overfill (PLNO) by default [V: MANUALSLIB_ICLASS p20].
- Full-loop mode consumes the loop volume plus 4× extra [S: WKB198538]. That is unacceptable for a
  100 µL-limited sample, because a 100 µL full-loop would need about 500 µL.
- A web summary gives the FL range as 0.1–250 µL (I-Class PLUS FL, [S: WAT_ICLASS_PLUS_FL]).
- Advantage: the loop can be switched out of the flow path after injection, so there is no permanent loop
  dwell volume.

---

## 3. Controlling Empower from Python

### 3.1 Options

| Option | What it does | Limits | Status |
|---|---|---|---|
| **Empower Toolkit** (COM automation; "Empower Toolkit Programmer's Reference Guide", Waters doc 71500031805 [S]) | Programmatic access to "most of the key data structures and functionality" of Empower and its Oracle database [S: WAT_TOOLKIT_FORUM]. Reported to create or read projects, methods, sample sets and results. | Licensed as an **Empower option** [S]. Whether it can **start acquisition** (run a sample set on a chromatography system) and receive run-state callbacks is **UNVERIFIED**; the manual could not be reached. Windows-only COM; 32/64-bit matching matters (UNVERIFIED). Some objects (e.g. dissolution sample-set methods) cannot be created via the Toolkit [S: TETRA_EMPOWER]. | Ask Waters (Q4) |
| **Pre-built sample-set methods launched by the operator** | The operator loads a sample-set method and presses Run. Empower runs every line (injections, BSM gradients, timed events) unattended. | One manual click per batch is acceptable ("loading the autosampler" is allowed). Python cannot change the sequence mid-run. | Works with any Empower |
| **Sample Set Generator** (Waters add-on) | Automates *creation* of instrument methods, method sets and sample sets [S: WAT_SSG]. | Creation only, not real-time control. | Optional |
| **Third-party connectors** (e.g. Tetra Empower Agent, LIMS connectors) | REST access to sample sets and results [S: TETRA_EMPOWER]. | Also based on the Toolkit; licence and IT effort. | Not recommended |
| **Contact closures and TTL** (hardware) | Empower and the ACQUITY modules emit and accept event signals: "Rear panel contact closure and/or TTL inputs/outputs" [V: WAT_ICLASS_FTN_SPEC]. | Fixed set of signals; needs wiring and a DAQ. Deterministic, version-independent. | **Recommended backbone** |

### 3.2 Rear-panel signals

- **Inject Start** (sample manager): contact-closure output on **connector 1, positions 1 and 2** [V: WKB55803].
  This is the universal t₀ marker for every injection.
- **Run events (timed contact closures).** Waters instrument methods have an events table with timed
  "Switch On/Off" and "Cycle Inject Valve" actions [V: WKB9108; S: WKB3148, WKB21173]. The I-Class BSM has
  event outputs used, for example, for an external solvent-select valve [S: WKB27360]. A facility moved its
  contact-closure cable to the BSM to send a programmed signal from the method [S]. The **exact number of
  BSM event-out channels and their ratings are UNVERIFIED** (Q5). Read the BSM rear panel and the Empower
  BSM "Events" tab.
- **Event inputs** (e.g. "Inject Hold / Start" or "Stop Flow" inputs). These exist on many Waters modules
  (UNVERIFIED for this BSM/SM). Do **not** design the primary scheme around them.
- **Timing.** Contact-closure latency is not specified in anything reached. It is probably 10–100 ms
  (UNVERIFIED). This is irrelevant for assay steps lasting seconds to minutes, but it matters if
  transient peaks are integrated. Timestamp everything on one PC clock.

### 3.3 Recommended synchronisation

**Primary scheme: "Empower is the fluidic master, Python is the listener and the EC/valve master."**

1. The whole assay cycle is written as an Empower **sample-set method**. Each sample-set line is one injection
   (sample, conjugate, substrate, or a "blank" zero-volume line), with its own instrument method. That method
   holds the BSM flow and composition programme and the run time, which is the step duration.
2. The SM-FTN **Inject Start** contact closure is wired to an **opto-isolated digital input** on a USB DAQ owned
   by Python (model to be selected; a generic, isolated 5–24 V input module is needed). Optionally, one BSM
   **event out** per method is wired to a second input to label the step type.
   - The Gamry Misc. I/O also has 4 digital inputs [V: GAMRY_IO_APPNOTE]. These could be used instead, but
     reading them from ToolkitPy while an acquisition runs is UNVERIFIED. A separate DAQ keeps the two
     concerns independent.
3. Python keeps a **cycle table**: step type, offset from Inject Start, and actions. Example actions: switch
   valve to "reactor → cell", start Gamry chronoamperometry, change potential.
   - On each Inject Start edge, Python identifies the step, either by counting edges from the cycle start or by
     the BSM event code, and schedules its actions relative to t₀.
   - The **external valve** is driven by Python over TTL/contact or serial, depending on the valve's
     actuator (Q6).
4. The **Gamry runs continuously** through the whole cycle: one long chronoamperometry, or multi-step
   segments. Data are timestamped with the PC clock, and Python writes event marks into the same file.
   - Optional: the Gamry current-monitor analog output (Reference family: 0–5 V on the Misc. I/O analog out
     [V: GAMRY_IO_APPNOTE]) can be logged in Empower as a second trace through a Waters analog-input
     interface. The analog-input hardware is UNVERIFIED (Q7). This gives a single overlaid record of TUV and
     EC.
5. **Watchdog.** If an expected Inject Start does not arrive within its window (+30 s), Python puts the valve
   into "cell bypass", holds the Gamry at open circuit or a safe potential, and alarms.

Timing diagram for one injection step (text):

```
Empower line n starts ──► SM draws sample (≈ 30–60 s, not timed by Python)
                         │
Inject Start CC  ────────┐_______ (pulse, conn.1 pos.1–2)   t0
                         │
Python  DAQ edge t0 ─────┼─► t0+0 s  valve V = "load/reactor" (if not already)
                         │   t0+Δt_transfer   (dwell volume / Q) plug reaches reactor
                         │   t0+t_stop        valve V = "isolate reactor" (stopped-flow incubation)
                         │   t0+t_stop+t_inc  valve V = "reactor → EC cell"
Gamry CA (continuous) ═══╪═══════════════════════════════ (marks written at each Python action)
BSM programme ───────────┴── flow/composition steps as in instrument method; run ends at t0+T_line
Empower line n+1 starts ──► next injection
```

**Fallback A: Python is master via the Empower Toolkit.** This applies if Waters confirms that the Toolkit can
start sample-set acquisition and report status (Q4). Python then builds or launches each cycle's sample set
through COM, and still uses the Inject Start contact for precise t₀.

**Fallback B: Python is master via contact closure into Empower and the sampler.** This applies if the
sample manager or BSM offers an "external start" or "inject hold" input (UNVERIFIED). Empower sample-set lines
are set to wait for an external start, and Python releases each line by closing a relay. This gives Python
full control of step timing, but depends on an input whose existence and behaviour must be checked (Q5).

**Fallback C: degraded, with no Empower dependency for the EC.** Empower runs open-loop. Python only listens to
Inject Start, drives the valve and the Gamry, and tolerates small timing drift. This is always possible.

---

## 4. Gamry Reference 600+

### 4.1 Verified specifications [V: GAMRY_REF600P_DS, GAMRY_REF600P_LEGACY]

| Item | Value |
|---|---|
| Current ranges | 11 ranges, 60 pA–600 mA (13 with internal 10× and 100× gain); max ±600 mA |
| Current resolution | 0.003 % full scale per bit; minimum current resolution **20 aA** |
| Current accuracy | ±10 pA ± 0.05 % of range ± 0.2 % of value (600 mA–6 nA ranges); 0.75 % of value (600 pA); 1.5 % of value (60 pA) |
| Current-measurement bandwidth | > 10 MHz (600 mA–600 µA); > 0.15 MHz (6 µA). Not stated for nA/pA ranges (much lower; the Gamry note assumes ~30 mHz uncorrected on a 30 pA range with 5 pF input capacitance [V: GAMRY_SMALLSIG_APPNOTE]) |
| Noise and ripple | < 2 µV rms (typical) (voltage) |
| Min. time base | 3.333 µs |
| Min. potential step | 12.5 µV |
| Applied potential | ±11 V; accuracy ±1 mV ± 0.2 % of setting |
| Compliance | > ±22 V |
| Electrometer | > 10¹⁴ Ω ‖ < 0.2 pF; input current < 10 pA; bandwidth > 15 MHz; CMRR > 65 dB (1 MHz) |
| EIS | 10 µHz–5 MHz |
| Isolation | **"Isolated from earth: Yes"** (floating) |
| Cell connections | 2, 3, 4, 5 or 6 (includes aux channel) |
| DSP sampling modes | Fast (end of step), Noise-Reject (average last 20 % of step), Surface (average whole step) |
| I/O | Aux voltage input (BNC); external signal into control amp; 15-pin Misc. I/O with digital I/O (TTL) and voltage out |
| Status | **Discontinued**; successor is Reference 620 [V: GAMRY_REF600P_LEGACY] |

**Techniques.** Licensed software packages: PHE200 (physical electrochemistry: CV, chronoamperometry,
chronocoulometry, multi-step), PV220 (pulse voltammetry: DPV, SWV, NPV), EIS300 (EIS), plus others
[V: GAMRY_REF600P_LEGACY].

**Toolkit interfaces.** The Echem Toolkit exposes, among others:

- IGamryDtaqChrono, IGamryDtaqPv, IGamryDtaqSqwv, IGamryDtaqEis
- IGamrySignalConst, IGamrySignalStep, IGamrySignalMstep (multi-step), IGamrySignalPv, IGamrySignalSqwv

[V: GAMRY_TK_V2]

### 4.2 Misc. I/O and triggers [V: GAMRY_IO_APPNOTE, GAMRY_TRIGGER_APPNOTE]

- **4 digital inputs and 4 digital outputs**, TTL (0/5 V), on a 15-pin high-density D-sub.
- Digital outputs on pins 7–10; ground on pin 6. The full pin-out is in operator-manual Appendix C, Table C-1,
  which was not reached.
- External devices must draw less than 10 µA from the inputs.
- Minimum output pulse width is about 10–50 µs.
- On Reference-family instruments the User I/O is **insulated from earth and from floating ground**.
- Analog output 0–5 V on pin 1.
- Framework scripts can wait on a "Digital Signal In" channel. A ToolkitPy equivalent exists in the Framework
  library (Pstat.SetDigitalOut is documented [S: GAMRY_SETDIGOUT_HELP]). Reading digital inputs from ToolkitPy
  is UNVERIFIED.

### 4.3 Python control

- **Echem ToolkitPy** (official) [V: GAMRY_TKPY_QSG, GAMRY_TKPY_WEB, GAMRY_TKPY_BROCH]:
  - Needs Gamry software ≥ 7.10.4.
  - Ships its own **Python 3.7.9, 32-bit**, with NumPy 1.21.6 and PySide2. Any other Python 3.7 32-bit must be
    uninstalled first.
  - **Windows 10/11 64-bit**; 16 GB RAM required, 32 GB recommended; administrator rights.
  - Data stream into NumPy arrays from a background thread. There is no 262 144-point Framework limit; about
    2 million points maximum in fast mode (< 100 µs sampling).
  - Whether a separate licence is needed: **UNVERIFIED** (Q8).
  - **Consequence:** the orchestration layer either runs inside Gamry's 32-bit Python 3.7, or runs as a
    separate modern Python process that talks to a **Gamry worker process** (32-bit 3.7) over a local socket
    or ZeroMQ. **Recommended: the worker-process split.** It keeps the Waters DAQ and valve code free of the
    3.7 constraint.
- **Echem Toolkit over COM** (GamryCOM: IGamryDeviceList, IGamryPstat, …) [V: GAMRY_TK_V2]. Callable from Python
  via `comtypes` or `pywin32`; third-party examples exist (UNVERIFIED in this session). It requires the Echem
  Toolkit licence packages eChemBasic, eChemDC and eChemAC [V: GAMRY_TK_V2]. Bitness of the COM server and the
  Python interpreter must match (UNVERIFIED).
- **Framework scripts (Explain)** triggered by Python. This is the oldest route and the least integrated.

### 4.4 Floating operation and grounding with a grounded LC stack

- **The problem.** The Waters stack is earthed, with stainless-steel fluid paths at chassis ground (UNVERIFIED
  that every wetted part is bonded, but typical). The buffer is conductive, so the electrolyte in the EC cell
  is connected to earth through the liquid in the tubing.
  - A **floating** potentiostat (the Ref 600+ is isolated from earth [V]) tolerates this. There is no ground
    loop through the instrument.
  - The liquid column still acts as an antenna and a leakage path. Mains-frequency and pump-motor noise couple
    into the cell through the solution resistance and the electrode double-layer capacitance.
- **Solution-path resistance** [Derived]: R = L / (κ·A).

  | Buffer conductivity κ | 0.3 m of 127 µm ID PEEK | 0.3 m of 63.5 µm ID PEEK |
  |---|---|---|
  | ≈ 1.6 S/m (PBS, UNVERIFIED value) | ≈ 15 MΩ | ≈ 59 MΩ |

  Upstream and downstream lines form two such paths. Use **PEEK (not steel) for at least the last 30 cm** each
  side of the cell, and keep the cell's own stainless parts (some cells use a stainless counter electrode,
  e.g. the Metrohm thin-layer cell [V]) away from earth.
- **Recommendations:**
  - Put the cell in a **Faraday cage**, connected to the Gamry floating ground (black lead) when the
    instrument is floating (UNVERIFIED wording; follow the Gamry manual).
  - Keep the cell cable short.
  - Mount the cell away from the BSM and SM power supplies.
  - Insert a **grounded or shielded flow-through "noise trap"** upstream. Standard LC-EC practice is a
    grounded steel union placed **before** a long PEEK section (UNVERIFIED). This defines where the solution
    potential is clamped.
  - Avoid pump pulsation reaching the cell. The BSM is a dual-piston pump, so add a pulse damper or the
    restrictor described in §1.2, or measure in **stopped flow**.
  - Use Noise-Reject or Surface sampling with integration times of a **whole number of mains cycles** (20 ms
    at 50 Hz, 16.7 ms at 60 Hz) to reject line pickup (UNVERIFIED as a Gamry setting name; the principle is
    standard).

### 4.5 Realistic current noise (the detection floor in the model)

| Level | Value | Basis |
|---|---|---|
| Instrument floor (Ref 600+), cage, nA range | **≪ 1 pA**: resolution 20 aA [V]; Gamry states the Ref 620 resolves 1 fA changes and its best input stage has ≈ 50 fA input current [V: GAMRY_SMALLSIG_APPNOTE] | Not the limiting term |
| Commercial LC-EC detector floor (dummy cell) | **≤ 2 pA peak-to-peak**, 300 MΩ / 0.5 µF or 470 pF dummy, 1 nA range, filter off (Antec DECADE Elite) [S: ANTEC_DECADE] → ≈ 0.3–0.5 pA rms if p-p ≈ 5 × rms (Gamry's rule of thumb [V]) | Best-case analog floor of a purpose-built LC-EC amplifier |
| Capacitive (voltage-noise) term | i_n ≈ 2π f e_n C_dl. A 2 mm disk at about 20 µF/cm² has C ≈ 0.63 µF (UNVERIFIED C_dl). At 1 Hz bandwidth, each 1 µV rms of voltage noise gives ≈ 4 pA rms [Derived] | Larsen 2012 model: amplifier-dominated at low C, C-dominated at intermediate C, R-dominated at large C [V: LARSEN2012] |
| Cell-limited LC-EC baseline in flow | Typically **1–10 pA rms** for mm-scale GC thin-layer or wall-jet cells, pump and flow noise included (UNVERIFIED range). Literature reports detection limits of ≈ 6 fmol (dihydroxybenzylamine) at 1 mm electrodes with a 25 µm gasket [V: ROCKLIN1994 abstract] | Use for the "flowing" detection model |
| Stopped flow / quiescent | About 0.5–3 pA rms (UNVERIFIED). Pump noise is removed, but drift (1/f) and background decay dominate | Use for stopped-flow accumulation readout |

**Recommendation for the model:**

- i_noise,rms = **3 pA** in flow (bounds 0.5–20 pA) and **1 pA** in stopped flow (0.3–5 pA), for a
  ≈ 2–3 mm diameter carbon electrode.
- Scale with electrode capacitance per Larsen 2012 when electrode area changes.
- Add a **baseline drift** term of 1–10 pA/min (UNVERIFIED) and a **blank variability** term (substrate
  auto-hydrolysis and non-specific binding, from the chemistry task). In practice the blank SD usually
  dominates the instrument noise.

---

## 5. Electrochemical flow cells and electrodes

All the cells below take ordinary WE/RE/CE leads and are potentiostat-agnostic **unless noted**. The Gamry
needs only banana or pin leads; cells with proprietary detector connectors need an adapter cable
(UNVERIFIED for each).

| Cell | Type | WE material & size | Volume / gap | RE / CE | Pressure limit | Connection | Gamry? | Collection / amplification | Reuse |
|---|---|---|---|---|---|---|---|---|---|
| **Antec SenCell** [S/V: ANTEC_SENCELL] | Confined wall-jet, adjustable spacer (AST; no gaskets) | GC, Pt, Au (2 mm listed) [S] | Working volume adjustable ≈ 0–300 nL [V]; total cell ≈ 0.5 mL [S]; ~25 nL min [S]; "do not operate at position 0" [S] | Salt-bridge Ag/AgCl, ISAAC, or HyREF; aux held at ref potential by voltage clamp [V] | Not found (UNVERIFIED) | (U)HPLC fittings (UNVERIFIED type) | Plausible; 3-electrode leads (UNVERIFIED — Antec designs for its own DECADE detector) | Amperometric, partial conversion (a few % typical for wall-jet, UNVERIFIED) | Excellent; polishable WE |
| **Antec VT-03** (also sold as the Waters 2465 cell; spacers 25 and 50 µm are Waters parts [S]) | Thin-layer | GC, Pt, Au, Ag | Down to 5 nL working volume [S]; 25/50 µm spacers [S] | Salt-bridge Ag/AgCl, ISAAC, HyREF | UNVERIFIED | UNVERIFIED | Plausible (UNVERIFIED) | Thin-layer amperometric | Excellent |
| **Antec FlexCell** | Thin-layer | GC etc. | ≈ 0.7 µL with 50 µm spacer; spacers 50 and 130 µm [S] | HyREF, salt-bridge, ISAAC [V: TOC] | UNVERIFIED | UNVERIFIED | Plausible | — | Good |
| **BASi cross-flow thin-layer** (kit MW-5052, dual 3 mm GC WE MF-1000) [S: BASI_GASKETS] | Thin-layer, single or **dual WE (series/parallel)** | GC 3 mm (dual) | Gaskets 13 µm (MF-1044), 51 µm (MF-1046), 127 µm (MF-1047) [S] | Separate RE (Ag/AgCl), steel CE (UNVERIFIED) | Low (typical thin-layer; UNVERIFIED) | 1/4-28 or 10-32 (UNVERIFIED) | Yes (open leads); **dual-WE needs a bipotentiostat** | Series dual electrode = generator–collector (redox cycling for reversible couples) [V: LUNTE1985 abstract] | Very good; polishable |
| **Metrohm "IC thin-layer cell"** [V: METROHM_TL_MANUAL] | Thin-layer | WE not stated on spec page | **< 0.35 µL (50 µm spacer); < 0.18 µL (25 µm)** | Pd solid-state or Ag/AgCl gel RE; **stainless-steel CE** | **0.8 MPa (200 psi)** | UNVERIFIED | Has "intelligent cell" ID chip, designed for Metrohm IC detector; adapter needed (UNVERIFIED) | — | Good |
| **Metrohm DropSens DRP-FLWCL-PEEK** (also methacrylate and PTFE versions) [V: METROHM_FLWCL] | Wall-jet for standard SPEs (strip electrode in middle); magnetic closure; fittings included | SPE carbon, Au (e.g. 250BT; C223AT 1.6 mm Au), Prussian blue | Not stated | On-strip Ag pseudo-RE, on-strip CE | Not stated (low; magnetic clamp; UNVERIFIED) | Fittings included (type UNVERIFIED) | Yes via DRP-CAC cable "to any kind of potentiostat" [V] | Wall-jet, low conversion | **Disposable** electrode, cheap swap |
| **Thermo Dionex 6011RS ultra** coulometric cell [V: THERMO_6011RS] | Flow-through porous graphite, **dual electrodes in series** | Micro-porous graphitic carbon | **4.3 µL internal** | Pd solid-state RE, built-in CE | **40 bar (4.0 MPa)** at inlet | 10-32 female (nanoViper) | **Not designed for third-party potentiostats** (SmartChip; UltiMate ECD-3000RS) — would need adapter wiring; UNVERIFIED | **Near 100 % conversion** [V]; usable flow > 0.3 mL/min [V] | Good; not polishable |
| **Micrux / BASi thin-film IDA** (MX-ED-IDA1/5/6, Pt or Au, glass) [V: BASI_IDA] | Planar IDA chips (10 × 6 mm format) | Pt or Au: 10/10 µm × 15 fingers (IDA1), 10/5 µm × 50 (IDA5-Pt) or 20 (IDA5-Au), 5/5 µm × 30 (IDA6) | Depends on cell; Micrux AIO base + **flow add-on** (methacrylate; PEEK on demand) [S: MICRUX_AIO] | Integrated RE/CE on some chips | Low (PMMA clamp; UNVERIFIED) | UNVERIFIED | Yes for single WE; **redox cycling needs 2 WEs (bipotentiostat)** | Redox cycling: 2D open IDAs give modest gains; closed or 3D IDAs ≈ 100× [V: HAN2014]; ≈ 25× [V: SHARMA2018]; comb IDA ≈ 3× vs coplanar [V: KIM2004] | Thin-film metal; cleanable electrochemically; limited polishing |
| **Micrux ED-IDRA1** (radial IDA, Pt/Au) [S: MICRUX_IDRA] | Radial IDA "for flow systems" | 12 pairs, 10/10 µm, 2 mm cell diameter, 50/150 nm metal | — | 4-electrode chip | — | — | Bipotentiostat needed | Redox cycling | As above |
| **Custom cell** (recommended development path, §5.2) | Thin-layer channel over IDA or band pair | Carbon (pyrolysed photoresist) or Au/Pt IDA; 2–5 µm gaps | 10–50 µm channel; 50–500 nL | Integrated Pt CE, external Ag/AgCl RE through a side-arm salt bridge | Design for ≥ 1 MPa | Two 10-32 coned ports, 1/16″ PEEK | Yes | Target ≥ 10× | Replaceable chip in a reusable PEEK holder |

### 5.1 Selection notes

- **A second potentiostat channel is mandatory for redox cycling.** Every generator–collector or IDA
  scheme needs two independently controlled working electrodes. The Ref 600+ is one channel.
  - Gamry builds bipotentiostats from **two synchronised Reference-family instruments**, with a sync cable
    (986-00063) and shared RE and CE [S: GAMRY_BIPOT_NOTE].
  - The listed pairings name the **Reference 620** and **Reference 3000**, **not the 600+**. Pairing a 600+
    with a 620 is UNVERIFIED (Q9). Budget is unconstrained, so buy a second Reference 620, or a matched pair
    of 620s.
  - A cheaper option is to hold the collector electrode with a separate floating low-noise potential source
    (UNVERIFIED performance).
- **Coulometric (porous-electrode) cells** convert nearly all of the electroactive product [V: THERMO_6011RS].
  - For a **stopped-flow accumulation** design, the measured quantity is the charge Q = n F N_product.
    Coulometric conversion turns the problem into "count every product molecule". Signal is then independent
    of flow fluctuations.
  - The penalty is a large electrode area: high double-layer capacitance gives higher background and noise.
    The cell is also tied to a vendor connector.
  - It is worth modelling as architecture "COUL".
- **Thin-layer amperometric cells** (BASi, Antec, Metrohm) are the robust baseline. They are cheap,
  polishable and potentiostat-agnostic, and have nL volumes. Conversion efficiency at UPLC flows is low
  (a few %; Derived from Levich/Matsuda channel-electrode theory, with exact values to be computed in the
  simulation).
  - **At 10–50 µL/min and 13–51 µm gaps, conversion rises substantially.** Thin-layer conversion depends on
    h²·U/(D·L), which is the main lever.
- **Disposable SPEs in a wall-jet cell** (DropSens) suit early development because they make fouling
  irrelevant. Electrode-to-electrode variance adds to blank SD (UNVERIFIED magnitude).

### 5.2 What a custom cell would look like

- **Body.** PEEK or PCTFE, clamping a glass or Si chip with a **thin-film IDA**: Au, Pt or pyrolysed carbon,
  2–5 µm bands and gaps, 0.5–2 mm² active area.
- **Channel.** A 10–25 µm laser-cut PET or PTFE gasket defines the flow channel, about 0.5 mm × 3 mm.
- **Fluidics.**
  - Inlet and outlet: 10-32 coned ports for 1/16″ PEEK tubing.
  - A side-arm reference compartment (Ag/AgCl in 3 M KCl behind a porous frit) sits **downstream** of the WE,
    so KCl leakage does not reach it.
  - Pt wire or thin-film CE, also downstream.
- **Electrical.** Pogo-pin contacts to the chip; shielded cable to the Gamry pair (bipotentiostat); the
  housing sits inside a Faraday cage.
- **Ratings.** Design pressure ≥ 1 MPa, with the restrictor upstream of the injector (§1.2) and the outlet
  open to waste so the cell sees only its own hydraulic resistance.
- **Optional integration.** Put a capture reactor (immobilised antibody on the channel lid, or a short bead
  bed) **immediately upstream** of the IDA. Product then travels less than 1 µL to the detector, giving the
  "on-chip accumulation, then measure" geometry used in IDA ELISA papers [V: NIWA1993, HAN2014].

---

## 6. Capture reactor hardware

| Option | Bed volume | Pressure limit | Particle / pore | Notes | Source |
|---|---|---|---|---|---|
| **CIMac monolith, 0.1 mL** (r-Protein A, epoxy, EDA, OH, …; 19 chemistries) | 0.1 mL (5.2 mm ID × 4.95 mm) | Not found for r-Protein A; CIMac QA lists 15 MPa [S] (UNVERIFIED for others) | Channels 1.3, 2 or 6 µm | pH 2–11 working, 2–13 CIP (r-Protein A) [S]; flow 0.2–3 mL/min listed for sibling columns [S] | SARTORIUS_CIMAC |
| **POROS A 20 µm (Protein A) 2.1 × 30 mm** | 0.1 mL | 2400 psi (170 bar) for stainless 2.1 × 30 mm [S]; PEEK version not stated | 20 µm perfusive particles | Capacity ≈ 19 mg/mL [S]; 2–40 °C | THERMO_POROS_A |
| **Empty micro-column or guard hardware** packed with antibody beads (e.g. 1.0–2.1 mm ID × 5–20 mm; 2–10 µm frits) | 4–70 µL (Derived from geometry: π r² L) | Hardware usually ≥ 100 bar (UNVERIFIED; depends on product) | Beads 1–50 µm (agarose, polymer, silica) | Vendor and part to be selected (none verified this session) | UNVERIFIED |
| **Bead-injection or renewable column** (beads delivered and discarded each cycle) | ≈ 3.6 µL in Grate et al.'s rotating-rod cell [V: GRATE2009] | Low | Sepharose beads | Fully renewable surface; sandwich immunoassay in < 20 min [V] | GRATE2009 |
| **Magnetic-bead trapping in flow** | Defined by trap: µL | Low (beads must stay trapped) | 1–3 µm superparamagnetic (typical, UNVERIFIED) | SIA + neodymium magnet; beads introduced, trapped, released; ALP/PAPP amperometric, < 15 min [V: HIRAKAWA2006] | HIRAKAWA2006 |
| **Open-tubular / capillary reactor** (antibody on fused-silica or PEEK wall, 50–250 µm ID) | 0.2–5 µL per 10 cm | High | — | Low capacity and poor mass transport, but very low NSB area. Literature support not checked this session (UNVERIFIED) | — |
| **Inorganic supports used historically**: controlled-pore glass–Protein A immunoreactor (flow-injection electrochemical EIA, acid elution) [V: PALMER1992]; silica immunoreactor, ALP/PAPP, +150 mV, 12 min cycle [V: TRAU1997] | — | — | — | Precedent for regenerable inline capture with EC detection | PALMER1992, TRAU1997 |

**Choosing the reactor.** The trade-off is capture yield versus volume:

- A 0.1 mL column perfused with 100 µL of sample at 10–50 µL/min gives 2–10 min contact time.
- A 5–20 µL packed micro-bed gives higher linear velocity and a smaller product dilution volume. Small bed
  volume matters because **the enzyme product is diluted into the bed void volume** during stopped-flow
  accumulation.
- **Recommendation:** model a 10 µL bed (1 mm ID × 12.7 mm, Derived) and a 100 µL monolith as two cases.

Protein A/G columns allow a "**capture-antibody renewal**" strategy: strip the capture antibody and reload it
each cycle. This is an alternative to regenerating an antigen–antibody bond, and the chemistry task decides.

---

## 7. System-level fluidics

Common elements in all schemes:

- BSM → restrictor (gives > 1000 psi at the pump) → SM-FTN (needle + extension loop) → **external valve V** →
  … → TUV (optional) → waste.
- All lines downstream of the injector are 1/16″ PEEK, 0.005″ ID.
- The TUV flow cell (500 nL, 10 mm path, dispersion ≤ 0.8 µL, **1000 psi max** [S: WAT_TUV]) goes
  **downstream** of the EC cell, or on a separate branch. It is used during development to watch protein
  plugs at 280 nm and enzyme product (e.g. p-aminophenol), and to calibrate plug arrival times.

### 7.1 Scheme A: "Inline column, EC detector in series, bypass valve" (recommended baseline)

The external valve V is a **6-port, 2-position** valve used as a *selector/bypass*:

```
SM-FTN ──► reactor ──► V ─┬─ position 1 (BYPASS): ──► waste       (EC cell isolated, static)
                          └─ position 2 (DETECT): ──► EC cell ──► TUV ──► waste
```

Implementation with a 6-port valve:

A standard 6-port, 2-position valve connects 1–2, 3–4, 5–6 in one position and 2–3, 4–5, 6–1 in the other.

| Port | Connection |
|---|---|
| 1 | reactor outlet (common) |
| 2 | EC cell inlet (cell outlet → TUV → waste, not through the valve) |
| 6 | waste (bypass) |
| 3, 4, 5 | free. Can be used to keep the cell perfused with clean buffer from a second low-flow source while bypassed, or for a second reactor later |

- **Pos 1:** reactor → waste. The cell stands still, closed-in on its own buffer. Used for sample, conjugate
  and regeneration steps (protein and low pH never touch the WE).
- **Pos 2:** reactor → cell → TUV. Used for wash-in of fresh substrate buffer, the substrate step and product
  readout.
- Exact port mapping depends on the valve model (Q6).

Stopped-flow accumulation:

1. Inject the substrate plug (e.g. 10–20 µL) and let it reach the reactor. Arrival is
   t = V_dwell / Q; calibrate with TUV.
2. Set BSM flow to 10 µL/min, or keep a higher flow with V diverting upstream (needs Scheme B), so the reactor
   liquid is nearly stationary for t_acc = 2–10 min.
3. Resume flow at a defined rate with V in pos 2. The product plug (≈ bed void volume) sweeps through the
   EC cell.
4. Integrate the peak charge. A coulometric cell gives the total product directly; a thin-layer cell gives a
   fraction set by conversion efficiency.

**Limitation:** true zero flow is not available without either a 0 µL/min step in the BSM (UNVERIFIED) or a
second valve. 10 µL/min through a 10 µL bed exchanges the bed every minute, which washes out product.
Scheme B removes this.

### 7.2 Scheme B: "10-port valve with isolated reactor loop" (recommended if a 10-port valve is available)

Put the capture reactor **in the loop position** of a 10-port, 2-position valve. Use the other loop position
for a short shunt, so the BSM can keep flowing (pressurised, stable) while the reactor is **isolated with both
ends closed**. That gives true stopped-flow incubation and product accumulation.

| Valve state | Path | Used for |
|---|---|---|
| **State A (perfuse)** | SM-FTN → reactor → EC cell → TUV → waste | Sample load, conjugate, washes, substrate fill, readout. Readout with flow passing through the cell |
| **State B (isolate)** | SM-FTN → shunt → cell-bypass → waste; reactor sealed | Incubations: sample and conjugate stopped-flow binding, **substrate accumulation**, and BSM buffer exchanges at high flow without disturbing the reactor |

- Regeneration is done in state A, with a cell-bypass tee and check valve or a second 6-port valve, so low-pH
  glycine does not pass the EC cell.
  - Alternatively, keep **the EC cell on a separate branch** fed only in state A2. With a 10-port valve a
    third configuration is not possible, so for full separation use **one 10-port valve for the reactor plus
    one 6-port valve for cell bypass**.
  - The brief provides one external valve. A second valve is a purchase, and the budget is unconstrained.
- Dwell to the reactor in state A is the needle + loop + 30 cm line. High-flow exchanges are done in state B,
  so the reactor sees each buffer change already completed.

### 7.3 Scheme C: "Off-line incubation in the sampler, inline capture/readout"

- Sample and the detection conjugate are combined by **auto-addition** (draw both, mix in the needle, delay at
  the sample-compartment temperature) [V: WKB1416]. The complex is then injected onto a streptavidin or
  anti-IgG capture micro-column, followed by a wash and the substrate plug. Detection is as in Scheme A or B.
- **Pros:** homogeneous-phase binding kinetics (faster), fewer injections.
- **Cons:** auto-addition delay reliability [V: known issue]; mixing efficiency inside a 15–30 µL needle at
  100 µL total volume (needs the loop); and excess unbound conjugate must be washed off the column, which sets
  the blank.

### 7.4 Timeline of one assay cycle (Scheme B, sequential sandwich on a 10 µL bed)

| t start (min) | Step | Empower line / BSM | Valve | EC (Gamry) | Duration (min) |
|---|---|---|---|---|---|
| 0.0 | Pre-equilibrate reactor with running buffer (A1) at 200 µL/min | line 1 (no injection or 0 µL) | A | Cell held at E_det, baseline | 2.0 |
| 2.0 | Inject 100 µL sample (≈ 1 min draw + inject) | line 2 | A | baseline | 1.0 |
| 3.0 | Load sample through reactor at 20 µL/min: 100 µL + 20 µL dwell. Sample protein reaches the cell in state A, so add a cell-bypass 6-port or accept exposure (chemistry decides) | line 2 cont. | A | (cell bypassed if 2nd valve) | 6.0 |
| 9.0 | Stopped-flow binding (optional) | — | B | — | 5.0 |
| 14.0 | Wash, 200 µL/min | line 2 cont. | A (bypass cell) | — | 1.5 |
| 15.5 | Inject 20 µL conjugate, load at 20 µL/min | line 3 | A (bypass cell) | — | 2.5 |
| 18.0 | Stopped-flow conjugate binding | — | B | — | 5.0 |
| 23.0 | Stringent wash (≥ 50 bed volumes, 500 µL at 250 µL/min) | line 3 cont. | A (bypass cell) | — | 2.0 |
| 25.0 | Switch BSM to A2 (substrate buffer) in state B at 300 µL/min; wash-in | line 4 | B then A | baseline in substrate buffer | 1.5 |
| 26.5 | Inject 20 µL substrate; fill reactor at 50 µL/min | line 4 | A | record | 1.0 |
| 27.5 | **Product accumulation (stopped flow)** | — | B | baseline recorded (blank drift) | 10.0 |
| 37.5 | **Readout**: elute at a fixed 50 µL/min through EC cell; integrate charge | line 4 cont. | A | CA or pulsed; integrate | 2.0 |
| 39.5 | Regeneration (B1 glycine) | line 5 | A (bypass cell) | cell in buffer | 3.0 |
| 42.5 | Re-equilibration (A1), electrode conditioning pulses if needed | line 5 cont. | A | conditioning | 4.0 |
| 46.5 | **End**, data processing; next cycle | — | — | — | — |

**Total ≈ 47 min**, which fits within 60 min with about 13 min margin for:

- slower sample loading: 100 µL at 10 µL/min adds 4 min;
- a longer accumulation, up to 15 min;
- injection overheads.

All durations except the instrument limits are design choices for the simulation to optimise. Flows are
within 10–2000 µL/min [V]. The 13 µm–127 µm-gasket thin-layer cells must be checked against the
outlet-side pressure at 250 µL/min [Derived: low, because the cell outlet goes to waste].

### 7.5 Volume and dispersion budget (Scheme B)

- Needle 15–30 µL + extension loop 100–250 µL, permanently in line for the FTN [V].
- Injector → valve: 15 cm 0.005″ = 1.9 µL.
- Valve → reactor → valve: 2 × 10 cm = 2.5 µL plus valve internal volume (UNVERIFIED; typically ≤ 1 µL per
  passage in UHPLC valves).
- Reactor bed: 10 µL total, void ≈ 4 µL (porosity ≈ 0.4, UNVERIFIED).
- Valve → EC cell: 10 cm = 1.3 µL.
- EC cell: 0.02–4.3 µL.
- Product-plug broadening between reactor and cell: σ_V ≈ 0.5–1.5 µL for a small molecule at 10–100 µL/min
  over 0.5 m [Derived, §2.5], shorter in practice. The readout peak is therefore set mainly by **bed void
  volume and bed dispersion**, not by tubing.

---

## 8. Risks and open questions

### Questions for the user (Q)

1. **Sampler identity:** SM-FTN or SM-FL? Which ACQUITY generation (classic, H-Class, I-Class, PLUS,
   Premier)? Needle size and installed extension loops?
2. Flow-path type: standard stainless, Bio (titanium) or Premier (MaxPeak HPS)? This affects protein
   adsorption and low-pH corrosion.
3. Empower version (3.x, feature release), and whether the **Sample Prep / In-Needle Auto Additions** features
   (Empower ≥ 3.6.0 [S]) are licensed.
4. Is the **Empower Toolkit** licensed? Can it start acquisition and report run status on this installation
   (Waters to confirm)?
5. **BSM and SM rear-panel I/O:** number of event outputs and inputs, signal type (relay or TTL), and whether
   there is an external start or inject-hold input. Photograph the rear panels.
6. **Exact external valve model**: 6- or 10-port, actuator, trigger interface (TTL contact, BCD, RS-232/USB),
   pressure rating, rotor material (PEEK or Valcon vs. steel) and internal volumes.
7. Optical detector model (TUV, PDA or FLR) and flow-cell pressure rating. Is a Waters analog-input module
   (to log the Gamry analog out in Empower) available?
8. PC and OS for Gamry control: Windows 10/11 64-bit with 16–32 GB RAM, as required by ToolkitPy [V]. Gamry
   software version (≥ 7.10.4 needed). Are the ToolkitPy and Echem Toolkit licences held?
9. Is a **second potentiostat** acceptable (needed for redox cycling)? Gamry to confirm 600+ ↔ 620
   bipotentiostat pairing.

### Bench risks (R)

| ID | Risk | Mitigation / test |
|---|---|---|
| R1 | IgG losses on needle, loop and steel surfaces at fM concentrations | Spike recovery test with fluorescent or ¹²⁵I-free labelled IgG through the injector at 1–1000 pg/mL; carrier protein; bio-inert flow path |
| R2 | Carryover of conjugate into the next cycle (raises the blank). Spec < 0.004 % applies to caffeine [V] and is meaningless for sticky enzyme conjugates | Blank-after-high runs; aggressive needle wash; dedicated conjugate wash |
| R3 | BSM at 10–20 µL/min below its specified precision range; pressure < 1000 psi | Measure flow by weighing; restrictor before injector; prefer stopped flow by valve |
| R4 | Electrode fouling by proteins and low-pH regeneration | Cell bypass (second valve); electrochemical cleaning pulses; disposable SPE during development |
| R5 | Mains and pump noise via grounded steel lines | PEEK isolation lengths, Faraday cage, stopped-flow readout, line-cycle integration |
| R6 | Substrate auto-hydrolysis and the blank current in the reactor | Inject substrate fresh from a 4 °C vial; measure blank accumulation rate |
| R7 | Contact-closure timing and Empower step-timing drift | Timestamp on one clock; calibrate plug arrival by TUV each day |
| R8 | ToolkitPy is locked to 32-bit Python 3.7 | Separate worker process; pin versions |
| R9 | Ref 600+ is discontinued; spares and support | Plan migration to Reference 620 |
| R10 | Air bubbles from degassed lines into thin-layer cells; outgassing on depressurisation | Back-pressure at cell outlet (e.g. a 50–100 psi restrictor, within cell limits) |

---

## 9. References

Waters documents ("Waters" = Waters Corporation, Milford MA).

- **WAT_ICLASS_FTN_SPEC** — "ACQUITY UPLC I-Class System (SM-FTN) Instrument Specifications", 720003948EN
  (2015). Mirror reached: https://ucrf.unist.ac.kr/wp-content/uploads/2024/11/ACQ.-I-Class-PLUS-Sys.-CH-A-wSM-FTN-I-Specification.pdf
  [V]
- **WAT_ICLASS_PLUS_FTN** — "ACQUITY UPLC I-Class PLUS System SM-FTN-I specification", 720006149:
  https://www.waters.com/content/dam/waters/it/library/specifications/2020/waters-specification-ACQUITYUPLCIClassPLUSSystemSMFTNI-720006149.pdf
  [not reachable; S]
- **WAT_ICLASS_PLUS_FL** — "ACQUITY UPLC I-Class PLUS System (SM-FL) Instrument Specifications":
  https://lcms.labrulez.com/paper/14643 [blocked; S]
- **MANUALSLIB_ICLASS** — Waters ACQUITY UPLC I-Class System manual (pp. 19–20):
  https://manualslib.com/manual/2912657/Waters-Acquity-Uplc-I-Class.html?page=19 [V]
- **WKB67734** — "H Class FTN – Injection volumes recommendations":
  https://support.waters.com/KB_Inst/Chromatography/WKB67734_H_Class_FTN_-_Injection_volumes_recomendations [V]
- **WKB7947** — "What is the maximum injection volume on an ACQUITY FTN":
  https://support.waters.com/KB_Inst/Chromatography/WKB7947_What_is_the_maximum_injection_volume_on_a_ACQUITY_Flow_Through_Needle_FTN [V]
- **WKB60785** — "Volume of the sample syringe, I-Class SM-FTN":
  https://support.waters.com/KB_Inst/Chromatography/WKB60785_What_is_the_volume_of_the_sample_syringe_for_the_ACQUITY_UPLC_I-Class_Sample_Manager_-_Flow_Through_Needle [V]
- **WKB1416** — "How to program ACQUITY SM-FTN Auto-Additions in Empower":
  https://support.waters.com/KB_Inst/Chromatography/WKB1416_How_to_program_ACQUITY_SM-FTN_Auto-Additions_in_Empower [V]
- **WKB67492** — "How does the Dilution tab on the Sample Manager FTN work":
  https://support.waters.com/KB_Inst/Chromatography/WKB67492_How_does_the_Dilution_Tab_on_the_Sample_Manager_FTN_work [V]
- **WKB55803** — "Does the ACQUITY Sample Manager have an Inject Start contact closure":
  https://support.waters.com/KB_Inst/Chromatography/WKB55803_Does_the_Acquity_Sample_Manager_have_an_Inject_Start_contact_closure_connection [V]
- **WKB9108** — "How to cycle the injection valve during an injection":
  https://support.waters.com/KB_Inst/Chromatography/WKB9108_How_to_cycle_the_injection_valve_during_an_injection_using_the_ACQUITY_Sample_Manager [V]
- **WKB32564** — "Minimum back pressure required for good UPLC performance":
  https://support.waters.com/KB_Inst/Chromatography/WKB32564_What_is_the_minimun_backpressure_required_for_good_UPLC_performance [S]
- **WKB5084** — "Flow restrictor to increase system backpressure on the ACQUITY BSM or H-Class QSM":
  https://support.waters.com/KB_Inst/Chromatography/WKB5084_What_is_the_part_number_for_the_flow_restrictor_used_to_increase_system_backpressure_on_the_ACQUITY_BSM_or_H-Class_QSM [S]
- **WKB96281** — "How to adjust the seal wash solvent interval":
  https://support.waters.com/KB_Inst/Chromatography/WKB96281_How_to_adjust_the_seal_wash_solvent_interval [S]
- **WKB14943** — "Solvent recommendations for ACQUITY H-Class washes":
  https://support.waters.com/KB_Inst/Chromatography/WKB14943_What_are_the_solvent_recommendations_for_the_ACQUITY_H-Class_washes_seal_wash_wash_solvent_purge_solvent [S]
- **WKB27360** — "How to connect an external Solvent Select Valve to an I-Class BSM":
  https://support.waters.com/KB_Inst/Chromatography/WKB27360_How_to_connect_an_external_Solvent_Select_Valve_SSV_to_an_I-Class_BSM
  [login-gated; S]
- **WKB3148** — "Use events to switch valve positions on the ACQUITY Column Manager":
  https://support.waters.com/KB_Inf/Empower_Breeze/WKB3148_How_to_use_events_to_switch_valve_positions_on_the_ACQUITY_Column_Manager_-_Active_in_advanced_mode [S]
- **WKB21173** — "Connect an external two-position switching valve to an ELS detector controlled by Empower":
  https://support.waters.com/KB_Inst/Chromatography/WKB21173_How_to_connect_an_external_two_position_switching_valve_to_ELS_Detector_controlled_by_Empower [S]
- **WKB198538** — "Sample consumed in Full Loop mode, ACQUITY SM / I-Class SM-FL":
  https://support.waters.com/KB_Inst/Chromatography/WKB198538_How_much_sample_is_consumed_in_Full_Loop_Mode_for_the_ACQUITY_UPLC_Sample_Manager_and_ACQUITY_UPLC_I-Class_Sample_Manager_FL [S]
- **WAT_APPNOTE_720008786** — "Implementing Programmed Injection Techniques in Empower CDS: A Practical Guide"
  (2025):
  https://www.waters.com/nextgen/en/library/application-notes/2025/implementing-programmed-injection-techniques-in-empower-cds-a-practical-guide.html
  [503 / blocked; S]
- **WAT_TUV** — ACQUITY UPLC and ACQUITY Premier Tunable UV Detectors, product page:
  https://www.waters.com/nextgen/us/en/products/chromatography/chromatography-detectors/acquity-uplc-and-acquity-premier-tunable-uv-detectors.html [S]
- **WAT_TOOLKIT_FORUM** — Waters Community forum, "Empower tool kit purpose":
  https://forums.waters.com/discussion/comment/6457/ (cites "Empower Toolkit Programmer's Reference Guide",
  71500031805) [host not reachable from this session; S]
- **WAT_SSG** — "Automated creation of chromatographic methods … using an Empower Sample Set Generator" (2024
  app note):
  https://www.waters.com/nextgen/id/en/library/application-notes/2024/automated-creation-of-chromatographic-methods-for-analytical-method-development-using-an-empower-sample-set-generator.html [S]
- **TETRA_EMPOWER** — Tetra Empower Agent, "Create Sample Set Method Command":
  https://developers.tetrascience.com/docs/tetra-empower-agent-create-sample-set-method-command [S]

Gamry Instruments documents:

- **GAMRY_REF600P_DS** — "Reference 600+ Potentiostat/Galvanostat/ZRA" data sheet (2018):
  https://www.gamry.com/assets/Uploads/Reference-600+2018.pdf [V]
- **GAMRY_REF600P_LEGACY** — "The Reference 600+ has been replaced with the Reference 620" (legacy specs page):
  https://www.gamry.com/support-2/legacy-devices/reference-600plus-legacy/ [V]
- **GAMRY_TKPY_QSG** — "Echem ToolkitPy Installation Quick-Start Guide", 988-00100 Rev 1.0 (2024):
  https://www.gamry.com/assets/988-00100-ToolkitPy-QSG.pdf [V]
- **GAMRY_TKPY_WEB** — Echem ToolkitPy support page:
  https://www.gamry.com/support-2/software/echem-toolkitpy/ [V]
- **GAMRY_TKPY_BROCH** — "Gamry Electrochemistry ToolkitPy" brochure:
  https://cn.gamry.com/assets/Uploads/ToolKitPy-Brochure-final.pdf [V]
- **GAMRY_TK_V2** — "Gamry Electrochemistry Toolkit" (Rev 1.0, 8/31/18):
  https://www.gamry.com/assets/Uploads-v2/Echem-ToolKit-v2.pdf [V]
- **GAMRY_IO_APPNOTE** — "Customizing Experiments Using the I/O Capabilities":
  http://www.gamry.com/application-notes/instrumentation/using-io-capabilities [V]
- **GAMRY_TRIGGER_APPNOTE** — "Trigger a Spectrometer with Gamry Potentiostats":
  https://www.gamry.com/application-notes/software-scripting/trigger-a-spectrometer-gamry-potentiostats/ [V]
- **GAMRY_SMALLSIG_APPNOTE** — "Measurement of Small Electrochemical Signals":
  http://www.gamry.com/application-notes/instrumentation/measurement-of-small-electrochemical-signals [V]
- **GAMRY_SETDIGOUT_HELP** — Framework help, Pstat.SetDigitalOut():
  https://help.gamry.com/Framework/libraryroutines_pstat_setdigitalout().html [S]
- **GAMRY_BIPOT_NOTE** — "BiPotentiostat Installation and Setup":
  https://www.gamry.com/assets/Support-Downloads/Installation-Notes/BiPotentiostat-Installation.pdf and
  https://www.gamry.com/potentiostats/bipotentiostat/ [S]

Flow-cell, electrode and column vendors:

- **ANTEC_SENCELL** — Antec Scientific SenCell product page:
  https://antecscientific.com/products/sencell/ [V]; manual 116.0010 (not reachable, 401) [S]
- **ANTEC_VT03 / ANTEC_FLEXCELL** — Antec product pages and datasheets via
  https://antec.wpdev.go2people.nl/ [S; 401 on direct download]
- **ANTEC_DECADE** — DECADE Elite brochure:
  https://lcms.labrulez.com/labrulez-bucket-strapi-h3hsga3/Decade_Elite_4a672baa85.pdf; and service manual
  noise spec [S]
- **METROHM_TL_MANUAL** — Metrohm "Thin-Layer cell" user manual, Technical specifications p. 26:
  https://www.manualsdir.com/manuals/586940/metrohm-thin-layer-cell.html?page=26 [V]
- **METROHM_FLWCL** — Metrohm DropSens DRP-FLWCL-PEEK scope-of-delivery sheet:
  https://www.metrohm.com/content/metrohm/shared/en/products/d/rp-f/drp-flwcl-peek.download.pdf [V]
- **BASI_GASKETS** — BASi thin-layer cell gaskets: https://basinc.com/products/ec/gaskets; flow cells:
  https://basinc.com/products/ec/flowcells [S]
- **BASI_IDA** — BASi "Thin Film Interdigitated Micro-Array Electrodes":
  https://www.basinc.com/thin-film-interdigitated-micro-array-electrodes_ [V]
- **MICRUX_IDRA / MICRUX_AIO** — Micrux ED-IDRA1 and All-in-One platform:
  https://www.directindustry.com/prod/micrux-fluidic/product-240350-2603297.html;
  https://www.palmsens.com/product/micrux-one-cell/ [S]
- **THERMO_6011RS** — "Thermo Scientific Dionex 6011RS ultra Analytical Cell" product specifications,
  PS70255-EN:
  https://assets.thermofisher.com/TFS-Assets/CMD/Specification-Sheets/PS-70255-LC-Dionex-6011RS-ultra-Analytical-Cell-PN70255-EN.pdf [V]
- **SARTORIUS_CIMAC** — CIMac datasheet: https://sartorius.hr/media/qxap00q3/cimac-datasheet-en-b-sartorius.pdf;
  r-Protein A 0.1 mL product page (110.1004-2) [S]
- **THERMO_POROS_A** — POROS A 20 µm Protein A Affinity HPLC Columns:
  https://www.thermofisher.com/order/catalog/product/1502412 [S]

Papers (DOIs checked via PubMed unless marked):

- **LARSEN2012** — Larsen ST, Heien ML, Taboryski R. "Amperometric noise at thin film band electrodes."
  *Anal. Chem.* 2012, 84, 7744–7749. doi:10.1021/ac301136x [V]
- **NIWA1993** — Niwa O, Xu Y, Halsall HB, Heineman WR. "Small-volume voltammetric detection of 4-aminophenol
  with interdigitated array electrodes and its application to electrochemical enzyme immunoassay."
  *Anal. Chem.* 1993, 65, 1559–1563. doi:10.1021/ac00059a013 [V]
- **HAN2014** — Han D, Kim Y-R, Kang CM, Chung TD. "Electrochemical signal amplification for immunosensor
  based on 3D interdigitated array electrodes." *Anal. Chem.* 2014, 86, 5991–5998. doi:10.1021/ac501120y [V]
- **SHARMA2018** — Sharma D, Lee J, Shin H. *Biosens. Bioelectron.* 2018, 107, 10–16.
  doi:10.1016/j.bios.2018.02.010 [V]
- **KIM2004** — Kim SK, Hesketh PJ, Li C, et al. "Fabrication of comb interdigitated electrodes array (IDA) for a
  microbead-based electrochemical assay system." *Biosens. Bioelectron.* 2004, 20, 887–894.
  doi:10.1016/j.bios.2004.04.004 [V]
- **TRAU1997** — Trau D, et al. "Development of an amperometric flow injection immunoanalysis system for … 2,4-D."
  *Biosens. Bioelectron.* 1997, 12, 499–510. doi:10.1016/s0956-5663(97)00007-9 [V]
- **PALMER1992** — Palmer DA, Edmonds TE, Seare NJ. "Flow injection electrochemical enzyme immunoassay for
  theophylline using a protein A immunoreactor…" *Analyst* 1992, 117, 1679–1682.
  doi:10.1039/an9921701679 [V]
- **HIRAKAWA2006** — Hirakawa K, et al. "Electrochemical immunoassay for vitellogenin based on sequential
  injection using antigen-immobilized magnetic microbeads." *Anal. Sci.* 2006, 22, 81–86.
  doi:10.2116/analsci.22.81 [V]
- **GRATE2009** — Grate JW, et al. "Renewable surface fluorescence sandwich immunoassay biosensor …" *Analyst*
  2009, 134, 987–996. doi:10.1039/b900794f [V]
- **ROCKLIN1994** — Rocklin RD, et al. "Maximizing signal-to-noise ratio in direct current and pulsed
  amperometric detection." *J. Chromatogr. A* 1994 (Consensus record; DOI not retrieved, UNVERIFIED)
- **LUNTE1985** — Lunte CE, et al. "Difference mode detection with thin-layer dual-electrode liquid
  chromatography/electrochemistry." *Anal. Chem.* 1985 (Consensus record; DOI not retrieved, UNVERIFIED)
- **TAYLOR1953** — Taylor GI. "Dispersion of soluble matter in solvent flowing slowly through a tube."
  *Proc. R. Soc. A* 1953, 219, 186–203. doi:10.1098/rspa.1953.0139 (from memory, not checked this session —
  UNVERIFIED)

**Access notes.** These hosts could not be reached or were blocked in this session:

- help.waters.com (403/503)
- labrulez / icpms.cz PDFs (Cloudflare)
- manualshive.com (bot block)
- forums.waters.com and interface.waters.com (outside the session's network allow-list)
- antec.wpdev.go2people.nl downloads (401)
- chemistry.unt.edu and richmondscientific.com (TLS chain / HTML)

Values that depend on them are marked [S] or UNVERIFIED.
