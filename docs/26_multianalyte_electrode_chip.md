# 26 — Multi-analyte affinity electrode chip for bioreactor samples (exploratory concept)

Status: 2026-11-13. **Exploratory desk note, outside the scope of docs/00.** It records a discussion with the user about
using the platform for more than total IgG, for example on a bioreactor sample, with "anything an affinity approach can
measure". It changes no decision, gate or parameter, orders nothing and is not an input to G1a/G1. No model run was made:
`src/elisa_sim` has no element for a planar capture site, a multi-electrode die or a culture-medium matrix, so there is
no P(success) and no LOD estimate here.

Conventions as in docs/16: **UNVERIFIED** = not traceable to a source checked in this session; **Derived** = arithmetic
shown here; **[assessment]** = judgement; **[V-abs]** = checked against an abstract or search summary only, not the full
text. Potentials are vs Ag/AgCl unless stated.

---

## 0. Summary

* The electrode in the current design is analyte-blind: it detects hydroquinone (HQ) made by ALP. Specificity lives in
  the capture phase. One analyte per injection therefore needs no new chip, only more reagents. **Several analytes from
  one injection need position encoding:** one capture site and one working electrode per analyte, read with the flow
  stopped.
* The user's choices for this concept: keep the gen-1 tubing rig and valves (no cartridge microfluidics); give up the
  1 pg/mL detection limit (precision is still wanted); bind the affinity ligands on the die instead of on beads; place
  each ligand zone next to the metal, not on it.
* Resulting chip (§3): a thin-film die of roughly today's size with about eight working electrodes in one thin-layer
  channel, each with a ligand zone on the adjacent glass, plus reference and control sites and a shared CE/RE.
* The main new problem is surface renewal (§4). The preferred answer is to strip and reload the ligands every run
  through DNA-directed immobilisation, with regeneration by acid as the simpler alternative.
* The metal still sees every sample and will foul. It is cleaned electrochemically in place, during the strip step
  while no ligand is present. **Estimated cleaning pulses are in §5.3**; they are starting values for a bench test, not
  validated settings.
* What this concept departs from in docs/00 is listed in §7. The first bench test is in §8.

---

## 1. Why the electrode has to change at all

| Case | Chip | Rig | Cost |
|---|---|---|---|
| One analyte per injection, analytes run in turn | unchanged | one bead and one conjugate reservoir per analyte on the SIA selection valve | one full cycle per analyte (≈ 56 min, docs/05 §4.1) |
| Several analytes from one injection | multi-site die (this note) | simpler than gen-1 (§2) | lower sensitivity; renewal and cleaning become design problems |

Every ALP conjugate gives the same product, so a mixed bead population read on one electrode returns one summed signal.
Distinguishing analytes by different enzyme labels and potentials is limited to two or three labels [assessment] and is
not pursued.

## 2. What ligands on the die remove from the rig

With the ligands on the die there are no beads, so these gen-1 elements are not needed: the magnet and bead trap on V2,
the cooled agitated bead reservoir and its dosing sequence, and the stirred incubation cup (docs/05 §4.1). The sample
plug goes from the SM-FL straight over the die, slowly or back and forth. The rig becomes

```
SM-FL injector → detector valve → die (thin-layer cell) → waste
                      ↑
        selection valve: conjugate cocktail, wash, substrate, strip solution, ligand reload mix
```

Product forms at the electrode, so accumulation can be about 1 min instead of 11–15 min, and at ng/mL levels the
28-min incubation is not needed. A cycle of 10–15 min is an **[assessment]**, not a schedule.

## 3. The die

```
 flow →  ┌───────────────────────────────────────────────────────────────┐
  inlet ═╪═ [L1|WE1] [L2|WE2] [L3|WE3] … [L8|WE8] ── [CE] [RE] ═════════╪═ outlet
         │   L = ligand zone on glass, directly upstream of / between    │
         │       the fingers of its working electrode                    │
         │   pads at one end: WE1…WE8, CE, RE, contact loop ×2           │
         └───────────────────────────────────────────────────────────────┘
```

| Feature | Value | Basis |
|---|---|---|
| Substrate and metal | glass, thin-film Pt or Au | same technology as the docs/13 die; Micrux custom offer is Au/Pt (docs/13 §3.5.5, MICRUX_TF) |
| Channel | one straight thin-layer channel, 0.200 mm high | docs/13 §2.7 gap; exhaustive electrolysis τ = 18 s (docs/13 §1.2 D1) |
| Sites | 8 working electrodes, each ≈ 1 × 1.5 mm, pitch ≈ 1.5–2 mm | own layout; pitch from the cross-talk estimate below |
| Use of the 8 sites | 3 analytes in duplicate + 1 non-immune reference + 1 positive control; or 6 analytes on a 16-site die | precision is still required (user); reference = lever L5 of docs/05 |
| Ligand zone | on the glass beside or between the electrode fingers, silane chemistry | keeps the metal bare for HQ electron transfer and for cleaning (§5) |
| CE and RE | shared, downstream of the last site | CE products never pass a working electrode |
| Pads | ≈ 12 (8 WE, CE, RE, contact loop ×2) vs 6 today | docs/13 §2.5 |
| Die size | ≈ 6 × 15–20 mm vs 6 × 10 mm today | Derived from 8 sites at 1.5–2 mm plus CE/RE and pad field |

**Cross-talk.** HQ made at one site spreads by diffusion while the flow is stopped. With D = 9.0×10⁻¹⁰ m²/s
(`chem` HQ `diffusion_coefficient`, **UNVERIFIED** in the project file as well), the rms distance √(2Dt) is 1.27 mm in
15 min and 0.33 mm in 1 min (Derived). A 1-min accumulation therefore allows a pitch of about 1.5 mm (≈ 4–5 rms
distances) without barriers. If longer accumulation is wanted, a guard strip between sites held at the detection
potential would electrolyse stray product — the pre-electrolysis idea of docs/13 §3.6, itself UNVERIFIED pending E1.2b.

**Capture area.** A 1.5 mm² zone is about one eighth of the capture area of the gen-1 bead dose: 5×10⁵ beads × π ×
(2.8 µm)² = 12.3 mm² (Derived; bead dose from docs/05 §4.1). Sites saturate sooner, which limits the upper range.

**Operating point for precision.** Run each site far from saturation, with a short sample contact. The amount captured
is then set by concentration and flow, and depends little on how much ligand is left, which makes the signal tolerant of
ligand loss between runs [assessment]. Keep the exhaustive thin-layer charge read: it is nearly independent of electrode
area (read weight 0.92 ± 0.07, docs/13 §8.2).

**Electronics.** The Reference 600+ has one channel. Options:
* A multiplexer reading the sites in turn. Gamry's ECM8 switched up to eight **cells** sequentially, with a local
  potentiostat holding inactive cells; it is discontinued and replaced by the IMX8
  (https://www.gamry.com/support-2/legacy-devices/ecm8-electrochemical-multiplexer/, checked 2026-11-13). Whether either
  unit supports eight working electrodes sharing one CE/RE in one cell, and its leakage against the ≥ 5×10¹² Ω pad
  requirement of docs/13 §2.7, are **UNVERIFIED**.
* A multichannel potentiostat with a shared CE/RE (no vendor checked; UNVERIFIED).

With sequential reading, later sites accumulate longer; the read order and timing must be fixed and calibrated per site.

**Label-free option.** Ligands near an electrode allow an impedance read without conjugate or substrate. Impedance
responds to anything that adsorbs, and the user still wants precision, so this stays a side experiment [assessment].

## 4. Renewing the capture surface

docs/00 requires a capture surface that is reusable or automatically renewed. Beads gave this for free.

| Option | How | Evidence | Weakness |
|---|---|---|---|
| **Reload (preferred)** | each site carries its own DNA strand; ligands carry the complement; strip and reload from one mixed reagent every run | HRP conjugates on microelectrode arrays were removed by washing and the electrodes reloaded, restoring the amperometric response (Fruk et al., Chem Eur J 2007, doi:10.1002/chem.200601793, [V-abs]); DNA-encoded antibodies on sensor arrays (PubMed 21438633, [V-abs]); review: Meyer et al., Curr Opin Chem Biol 2014 ([V-abs]) | strip conditions, number of cycles and antibody data **not found**; reload reproducibility sets the precision |
| Regenerate | acid strip of the analyte and conjugate after each run (glycine pH 2, `chem.regeneration`) | 5 to 300 cycles reported; activity loss 0.5 %/cycle (0–7 %, low confidence); only ≈ 60 % of reported regenerations met their own success definition (Goode2015, [V-abs], all from `params/chemistry.yaml`) | differs per ligand; residual label carry-over UNVERIFIED (docs/09 F14) |
| Disposable die | replace after a set number of runs | — | a manual step; per-die calibration |

With reloading, one generic die serves any panel and the panel is defined by the reagents. With fixed ligands the die is
panel-specific and has a shelf life.

Calibration under any option: reference and control sites on every die, and a calibrator injection every few samples to
correct slow drift [assessment].

## 5. Keeping the bare metal stable: electrochemical cleaning

### 5.1 Why the metal drifts with the ligand off it

The metal sees every sample. Three things build up [assessment, general electrochemistry]:
* medium components — protein on any bare metal; thiols on gold. DMEM contains ≈ 0.2 mM L-cystine and ≈ 0.9 mM
  phosphate (Thermo Fisher and Sigma-Aldrich DMEM formulation tables, checked 2026-11-13; production CHO media are
  proprietary, UNVERIFIED);
* conjugate adsorbed on the metal, which raises the blank;
* a film from the HQ oxidation itself over many reads (`chem` HQ `fouling` is 0 in the model; UNVERIFIED for hundreds of
  reads).

### 5.2 Rules that follow from the sources

| Rule | Source |
|---|---|
| Clean in protein-free buffer, not in the sample. Anodic cleaning (1.5 V vs SCE, 10–15 s) returned BSA-fouled electrodes to baseline impedance in PBS but had no effect while they sat in the BSA solution. A water rinse alone did not help | Sommakia, Rickus, Otto, IEEE EMBC 2009, pp. 7139–7142 (iridium sites, 40 µm; full text read) |
| Alternate oxidising and reducing steps, with flow. A triple pulse of +1.6 / 0.0 / −0.8 V vs SCE, 100 ms per step, in flowing 100 mM phosphate pH 7.4 gave a reproducible gold surface; roughness fell faster at higher flow and rose without flow | Hoogvliet, Dijksma, Kamp, van Bennekom, Anal Chem 2000, 72, 2016–2021 ([V-abs]) |
| Oxidative cleaning wears gold. In pulsed amperometric detection, positive cleaning potentials cause a gradual signal loss from electrode recession; the four-potential waveform (detect +0.1 V 400 ms; −2.0 V 10 ms; +0.6 V 10 ms; −0.1 V 60 ms; 2 Hz; gold disc in ≈ 18 mM NaOH) minimises it by cleaning reductively | Thermo Fisher Technical Note 70670 (update of TN21; full text read) |
| Prolonged pulsing electropolishes gold: an effect was seen after 2000–5000 s of pulsing | Hoogvliet 2000 ([V-abs]) |
| A potential sweep in neutral buffer has been used as a cleaning step on Pt: 21 cycles, −0.5 to +0.9 V, 100 mV/s, in flowing PBS pH 7.4 | US patent 10,314,527 (Pt black; search summary only; reference electrode not seen → **UNVERIFIED**) |
| For gold, a KOH potential sweep left the cleanest surface of nine methods | Fischer et al., Microelectron Eng 2009, 86, 1282–1285, doi:10.1016/j.mee.2008.11.045 ([V-abs]); needs a strong base in the rig, not adopted |

Not used: Lee et al., ACS Omega 2022 (doi:10.1021/acsomega.2c06851), a two-step electrochemical cleaning with five
reuses of gold immunosensors — the article is marked **retracted** on PubMed Central.

### 5.3 Estimated cleaning pulses

**All values in this section are own starting estimates for a bench test (UNVERIFIED as applied to this die).** They are
bracketed by the sources in §5.2 but none of those used a thin-film die, this buffer or this matrix. SCE values
convert to Ag/AgCl (sat. KCl) by adding ≈ 0.045 V (standard electrode potentials, UNVERIFIED here).

Conditions for every clean: ligands stripped; chloride-free cleaning buffer flowing (for example 10–100 mM phosphate
pH 7.4, about 50 µL/min, own value); cell never sealed, so gas cannot stay in the 0.2 mm channel.

| | Platinum | Gold |
|---|---|---|
| **Routine clean, every cycle** | | |
| Anodic step | +1.0 V, 0.5 s | +1.2 V, 0.2 s |
| Cathodic step | −0.5 V, 0.5 s | −0.4 V, 0.2 s |
| Repeats | 10 (10 s in total) | 10 (4 s in total) |
| Settle | 30 s at the rest potential, flowing | same |
| **Hard clean, only when the health check fails** | | |
| Waveform | sweep −0.5 ↔ +0.9 V at 100 mV/s, 20 cycles (28 s each, 9.3 min) | triple pulse +1.6 / 0.0 / −0.8 V, 100 ms per step, 60 s |
| Anchor | patent 10,314,527 | Hoogvliet 2000 (+0.045 V if referred to Ag/AgCl) |
| **Limits not to exceed** | hydrogen and oxygen evolution onsets found by CV on the die | same, and no anodic step above ≈ +0.9 V if chloride is present (gold dissolves as chloride complexes; UNVERIFIED value) |

How the numbers were set:
* *Anodic step* — high enough to form surface oxide and oxidise adsorbates, below the sources' strongest values
  (+1.5 V on Ir for 10–15 s; +1.6 V vs SCE on Au).
* *Cathodic step* — reduces the oxide and restores the metal; kept short of hydrogen evolution, because a bubble in a
  0.2 mm channel is a failure. The −2.0 V step of the PAD waveform lasts only 10 ms in a flowing detector and is not
  copied.
* *Duration* — the gold budget matters. A 4-s routine clean at 100 cycles per day is 400 s of pulsing per day, the same
  order as the 2000–5000 s at which Hoogvliet saw electropolishing of bulk gold (Derived). A thin film of 100–200 nm
  has little to give; its life under this regime is **unknown** and is a result of the bench test.
* *Local pH during a clean* — forming one oxide layer on a 1.5 mm² Pt site takes about 6.6 µC (440 µC/cm², textbook
  value, UNVERIFIED here), releasing 6.8×10⁻¹¹ mol H⁺ into the 0.3 µL above the site = 0.23 mM (Derived). In 10 mM
  phosphate at pH 7.4 (buffer capacity ≈ 5.5 mM per pH unit, Derived) that is ≈ 0.04 pH units per step without flow,
  reversed by the cathodic step. Harmless to the die, but one more reason to clean before the ligand is reloaded.
* *Reference electrode* — the docs/13 baseline is an on-die Au quasi-reference whose potential is not fixed
  (docs/13 §3.5.5, docs/15 W5). The potentials above must be re-expressed against features of a CV on the die (oxide
  onset, oxide reduction peak, hydrogen onset), or the die needs a Ag/AgCl reference.

**Metal choice.** Platinum tolerates repeated oxide cycling better and does not bind thiols as gold does [assessment].
Against that, docs/13 §3.5.4 excludes Pt for WE1 because of earlier oxide formation [assessment there] — a concern for
the background of a 1 pg/mL step read that weighs less at ng/mL. Open; the bench test should run both.

**Health check after every clean** (reuses docs/13 §8.1): double-layer capacitance from a short CV, within ±10 % of the
die's starting value (docs/13 own target); current decay time of an HQ standard or of the first substrate fill, within
20 % of the starting value (own target). A slower decay is the first sign of fouling, before the charge changes, because
the exhaustive read still completes. A failed check triggers the hard clean; two failed hard cleans retire the die.

**Software.** The Gamry worker needs a multi-step potential command with the cleaning table as parameters and a logged
health check. `automation/` has only the planned `step_triple` (docs/13 §7.5); nothing is implemented for this note.

## 6. What a site could carry

| Target class | Format | Typical bioreactor level |
|---|---|---|
| Product titer | Protein A/L or anti-Fc ligand, sandwich | g/L |
| Active product | antigen as ligand | g/L |
| Host cell protein | polyclonal anti-HCP sandwich | ng/mL–µg/mL |
| Growth factors, insulin, transferrin | sandwich | ng/mL–µg/mL |
| Small molecules | competitive, ALP-labelled analogue (signal falls with concentration) | varies |
| Glycoforms, Fc-receptor binding | lectin or receptor as ligand | relative read |
| Host DNA | hybridisation probe or aptamer | pg–ng/mL |

Levels and formats are general bioprocess knowledge, **UNVERIFIED**. Titer at g/L is about 10⁹ above the current
1–1000 pg/mL range (Derived) and needs heavy dilution or a deliberately insensitive site; the Waters UV detector with a
Protein A column may be the better tool for titer [assessment].

## 7. Departures from docs/00 and risks

| docs/00 item | This concept |
|---|---|
| Analyte: human IgG | panel of several analytes |
| LOD ≤ 1 pg/mL | given up (user). Expected limit tens of pg/mL to low ng/mL — **UNVERIFIED**, general literature, no model |
| Buffer matrix only | culture medium: ≈ 0.9 mM phosphate (ALP inhibitor; K_i UNVERIFIED, 0.2 µM–1 mM), phosphatases from lysed cells, electroactive and thiol species. The wash must remove these before substrate |
| Capture surface reusable or renewed | by reload or regeneration (§4), not by fresh beads |
| ≤ 100 µL injected, ≤ 60 min, no manual step | expected to hold [assessment] |

Further risks: a cocktail of ALP conjugates raises non-specific binding with every added analyte; product IgG at g/L
loads every site to some degree (the reference site is there to show it); site-to-site and die-to-die variation.

## 8. First bench tests (not scheduled, not approved)

1. **Clean and reload on a catalogue die** (the M5a arrangement: catalogue Micrux die, existing Gamry, docs/13 §10.1).
   One ligand; 20 cycles of sample in medium → conjugate → read → strip → routine clean → health check → reload.
   Log signal, blank, decay time and capacitance. Run Pt and Au. Own targets: run-to-run CV ≤ 10 %; decay time within
   20 %; no trend in the blank. Also gives the thin-film life under the pulse regime of §5.3.
2. **Two-site die**: cross-talk at 1 and 5 min accumulation, with and without a guard strip.
3. Only then an eight-site die.

Beforehand, the same panel can be run analyte by analyte on the unchanged gen-1 rig (§1, first row); this tests the
reagents and the matrix without any new chip.

## 9. Open questions

* Pt or Au for the working electrodes (§5.3).
* Strip chemistry and cycle life for DNA-directed reloading; antibody data were not found (§4).
* Multiplexer or multichannel potentiostat for a shared-CE/RE multi-electrode cell (§3).
* Reference electrode on the die: Ag/AgCl availability on custom dies is already UNVERIFIED (docs/13 §12.2).
* Whether this concept is to be pursued at all, and when, relative to G1 — a user decision.

## 10. Sources checked in this session (2026-11-13)

* Sommakia S, Rickus JL, Otto KJ. Effects of adsorbed proteins, an antifouling agent and long-duration DC voltage pulses
  on the impedance of silicon-based neural microelectrodes. 31st IEEE EMBS Conf 2009, 7139–7142. Full text.
* Thermo Fisher Scientific, Technical Note 70670, Pulsed amperometric detection waveforms for carbohydrate
  determinations (updates TN21). Full text.
* Hoogvliet JC, Dijksma M, Kamp B, van Bennekom WP. Electrochemical pretreatment of polycrystalline gold electrodes to
  produce a reproducible surface roughness for self-assembly. Anal Chem 2000;72:2016–2021. Abstract level.
* Fischer LM, et al. Gold cleaning methods for electrochemical detection applications. Microelectron Eng
  2009;86:1282–1285. doi:10.1016/j.mee.2008.11.045. Abstract level.
* Fruk L, et al. (Niemeyer group). Chem Eur J 2007. doi:10.1002/chem.200601793. Abstract level.
* Meyer R, Giselbrecht S, Rapp BE, Hirtz M, Niemeyer CM. Advances in DNA-directed immobilization. Curr Opin Chem Biol
  2014. Abstract level.
* PubMed 21438633 (DNA-encoded antibodies on multiplexed sensor arrays, 2011). Abstract level.
* US patent 10,314,527, Sensors for analyte detection and methods of manufacture thereof. Search summary only.
* Gamry Instruments, ECM8 legacy page (URL in §3).
* DMEM formulation tables: Thermo Fisher technical resources (media formulation) and Sigma-Aldrich technical article.
