# 14 — Second-generation cartridge: the alternatives B and C in depth

Status: 2026-11-12, written after the user checkpoint of docs/12 §9. Candidate A goes to detailed design in docs/13
(not touched here). This document (i) tries to make candidate C (permanent glass chip, stopped-flow IDA, daily reagent
pack) viable, as the user asked, and (ii) tightens candidate B (single-use cells) into a fallback dossier. Inputs:
docs/00, 05, 08, 09, 10, 11, 12, `params/*.yaml`, `src/elisa_sim/`, `scripts/`, and the literature and vendor
documents read in this session (§C7). No other file was changed; the model was run on a copy in the session scratchpad.

**Sourcing conventions** (as docs/10–12). Every number names its source: a repository section or parameter key, a
literature key with DOI, or a vendor document with URL. Verification tags for sources read **in this session**:
**[V-abs]** PubMed abstract/metadata; **[V-full]** full text read through the fetch tool's summary (numbers quoted
by the tool, not seen as a table by me); **[V-vendor]** vendor document whose text I extracted and read;
**[V-sec]** search-engine or Consensus summary only. Sources carried from docs/10–12 keep their tags there.
**Derived** = calculated here with the arithmetic shown. **[assessment]** = engineering judgement. **UNVERIFIED** =
not checked against a source in this session. Confidence: high / medium / low as in docs/10.

---

## 0. Summary

**C as specified in docs/12 is not viable**, and the reason is now sharper than "only 92 % found": the reversible
part of an IgG–affinity bond is stripped essentially completely by acid in 2 min (human IgG leaves protein G at pH 2.5
with k_d = 0.17–0.37 s⁻¹, Anguizola2018 → residual exp(−0.166 × 120) ≈ 2×10⁻⁹, Derived), so whatever stays behind is
a **non-eluting sub-population** (denatured/aggregated IgG, non-specific adsorption, avidity), which repetition does
not remove geometrically and which no source quantifies below ~10⁻². Glycine regeneration of a permanent capture
surface therefore has **no evidence path to 10⁻⁴**, and correction cannot close a gap of 800× (§C1.5). The busiest
on-chip valve also needs ≈ 24× the only thermoplastic membrane-valve endurance figure.

**Revised C (C′) — viable with conditions.** Keep the permanent glass chip, the side outlet and the stopped-flow IDA;
change two things:

1. **Renew, do not regenerate**: the 0.1 µL capture bed is a **renewable micro-bed** (bead-injection principle:
   Pollema1994, Willumsen1997, Grate2009, Fu2011) packed from the daily pack before every injection and back-flushed
   out after the read, followed by an acid strip of the empty cavity. Carry-over then becomes a **product of
   independent removal steps** — residual-bead fraction × fraction of analyte surviving the strip on those beads
   (+ wall terms) — instead of one regeneration efficiency. A DNA-directed whole-layer renewal (Biacore CAP
   principle: capture reagent + ligand + analyte removed every cycle, ≥ 150 cycles per surface) is the second option.
2. **No valve on the chip**: all switching moves to the dock — one rotary selector (IDEX MX Series II class, rated
   "tens of thousands of cycles", ≈ 3000 needed per 300 runs), PEEK/PTFE isolation solenoids (≥ 10⁷ cycles rated) on
   the two outlets, pinch valves on replaceable tubing for the bead lines (valve ≥ 2×10⁶, C-Flex tubing > 2×10⁵).
   The IDA channel is protected as a **dead-end branch with a 1 mm guard channel**; the diffusive loss of product
   into the four port channels is ≤ 5 % (Derived), LOD-neutral.

Nearest-model estimate (n = 2000; §C3.6): **C′1 median 2.1 pg/mL, P 0.16 as specified; 1.8 / 0.21 after U1–U3
screening; 37.5 min injection → result, cycle 45.5 min.** The decisive parameter is the packed-bed NSB factor
(P 0.43 at ×1, 0.30 at ×2, 0.23 at ×3, 0.06 at ×10), which C′ shares with B. Carry-over of residual analyte costs
LOD steeply: with a 1000 pg/mL previous sample, a residual fraction of 3×10⁻⁴ moves the nominal LOD 0.64 → 1.1 pg/mL
and 10⁻³ to 3.1 pg/mL. **Conditions** (bench, before any glass): end-to-end carry-over ≤ 1×10⁻⁴ after a 10 ng/mL
challenge on a renewable-bed mock-up (with ≤ 10⁻³ residual beads as the intermediate gate), packed-bed NSB factor ≤ 2,
and blank CV ≤ 12 % over 20 repacks.

**B** stays the fallback: single-use cells remove the carry-over and valve-endurance questions by construction; it
is decided by the same packed-bed NSB factor, by cell-to-cell CV and by dried-reagent behaviour (Part B).

**Three-way verdict** (§F): A remains the recommendation of docs/12 because it keeps the one-step format (best gain
from reagent screening) and does not rest on the packed-bed factor. B or C′ become preferable only if the packed-bed
NSB factor comes back ≤ 2 **and** A's residual-bead or mixing risks fail; C′ in addition needs the carry-over test.

---

# PART C — making the permanent-chip candidate viable

## C1. Regeneration of a permanent capture surface: what the literature shows

### C1.1 Quantitative evidence found in this session

| Key | System | Regeneration reagent | Removal / residual | Cycles, capacity | Tag / conf. | Source |
|---|---|---|---|---|---|---|
| Andersson1999 | Biacore, 13 antibody–antigen systems, multivariate regeneration cocktails | 6 stock solutions (acidic, basic, ionic, chaotropic, detergent, solvent) and mixtures; EDTA found to be a good additive to chaotrope/high-ionic cocktails | "removed more than 90 % of the bound analyte in a 30 s pulse" in 9 of 13 systems; "regenerated the surface completely" in 5 | not in abstract | V-abs / high | doi:10.1021/ac981271j |
| Goode2015 | systematic review + meta-analysis of biosensor regeneration | acid, base, detergent, chaotrope, etc. | only "∼60 % of the reported studies analyzed were deemed a success" under a working definition | — | V-abs / high (qualitative) | doi:10.1021/la503533g |
| Anguizola2018 | protein G affinity microcolumn, rabbit/goat/**human**/mouse IgG | 0.067 M phosphate pH 2.5 elution; pH 7.4 re-equilibration 10 min (≥ 5 min sufficient, 5 vs 20 min < 2 % different) | human IgG k_d at pH 2.5 = **0.166 ± 0.001 s⁻¹** (0.5 mL/min) to 0.374 s⁻¹ (2 mL/min); at pH 3.0 k_d 3.1× lower; **% not eluted: not reported** | capacity varied **< 1 % (0.3–0.9 %) between cycles over up to 50 cycles**; columns stable ≈ 200 cycles / 1 year | V-full / high for k_d | doi:10.1016/j.ymeth.2018.03.013 (PMC6114083) |
| Nelson2009 | immunoaffinity HPAC (anti-2,4-D mAb) | pH 2.5 | analyte k_d at pH 2.5 = 0.056–0.17 s⁻¹; antibody re-folding after elution first-order, 2.4×10⁻⁴ s⁻¹ (t½ ≈ 48 min, Derived: ln2/2.4×10⁻⁴ = 2888 s) | — | V-sec (Consensus) / medium | https://consensus.app/papers/details/w:3b451f21-2b11-4b81-8506-44fa3ea8fb1e/ |
| Sun2008 (docs/10) | epoxy affinity monolith in PMMA, FITC-HSA | — | 92 % mean elution | — | V-abs (docs/10) | doi:10.1021/ac800322f |
| Beattie2022 | used industrial protein A resin (MabSelect SuRe) | process elution + CIP | static capacity 35.8 (used inlet) / 40.2 (outlet) vs **70.4 mg/mL** unused; "one foulant is **irreversibly bound mAb**" (confirmed by MS) | capacity halved over the resin's use (cycle number not in abstract) | V-sec (Consensus) / medium | https://consensus.app/papers/details/w:012c6b2f-9e56-49c3-9c50-94cbe6b57897/ |
| Şerban2026 | engineered rProtein A resin | 0.5 M NaOH CIP | — | 88 % DBC after 120 cycles | V-sec (Consensus) / medium | https://consensus.app/papers/details/w:9638afb6-e570-4c57-989e-d45fd53618d5/ |
| Tereshin2024 | protein A mutant resin | 0.1 M NaOH | — | effective after 100 bind/elute/sanitise cycles | V-sec / medium | https://consensus.app/papers/details/w:39b64dfa-42d1-4755-8c08-173b8ba73947/ |
| Park2021, Jeon2018 | Z-domain oriented antibody layers, SPR (CRP) | pH/detergent optimised | signal difference < 10 % (Park) / < 2 % (Jeon) over **5** cycles | 5 | V-sec / medium | https://consensus.app/papers/details/w:d2ab0cd3-4629-4bbd-93f0-56d38e893b88/ ; https://consensus.app/papers/details/w:93e88c92-dd25-4362-8949-4a558d603125/ |
| Foubert2018 | capacitive flow immunosensor | glycine-HCl pH 2.4 | — | 13 regeneration cycles | V-sec / medium | https://consensus.app/papers/details/w:6d883f63-c729-43e4-997b-7cdb70f7280d/ |
| Meyer2015 | regenerated antigen microarray, flow CL | glycine-SDS pH 2.5 or 8 M GuHCl best | — | 25 cycles over 4 days | V-sec / medium | https://consensus.app/papers/details/w:0b7b13d4-ff0b-4997-b4fd-6edfbf9c935d/ |
| Kamat2021 (docs/01, docs/08 §9 C8) | Biacore anti-human-Fc mAb surfaces | (as docs/08) | — | > 300 cycles | docs/08 / high for Biacore | PubMed 34788604 |
| Uthuppu2015, Sun2026 (docs/10) | in-channel immunosorbent / flow cell | — | — | 51 / 14 cycles | docs/10 | doi:10.1039/c4an01576b ; doi:10.1016/j.talanta.2025.129122 |

**Not found** (searched PubMed with "protein A chromatography carryover", "immunoaffinity elution residual",
"SPR regeneration residual percent", and Consensus with a combined regeneration-efficiency query): any measured
residual of a captured protein after regeneration below 10⁻² that is stated as a number, and any demonstration of
≥ 99.99 % removal. "Complete" regeneration in SPR (Andersson1999) is certified only to the instrument's resolution:
for a captured layer of 1500–3000 RU (the Biacore CAP capacity for a 150 kDa ligand, CAP_IFU) an assumed resolution of
≈ 1 RU (**UNVERIFIED**) means "complete" ≤ 1/1500–1/3000 ≈ 3–7×10⁻⁴ — SPR cannot certify 10⁻⁴ (Derived).

### C1.2 Reading: kinetics are not the limit, the non-eluting fraction is

* **Derived.** If captured IgG behaved as a single population with the measured acid off-rate, 2 min of pH 2.5 would
  leave exp(−k_d t) = exp(−0.166 × 120) = exp(−19.9) = 2.3×10⁻⁹ (Anguizola2018, protein G, human IgG; 0.5 mL/min).
  Even 30 s leaves exp(−5.0) = 7×10⁻³. Kinetically, 10⁻⁴ is reached after t = ln(10⁴)/0.166 = 55 s.
* Measured eluted fractions are far below this (92 %, Sun2008; "> 90 %" in 9/13 systems, Andersson1999), and used
  protein A resin carries **irreversibly bound mAb** (Beattie2022). The residual is therefore set by a
  sub-population that does not elute on the time scale of the step — denatured or aggregated protein, protein adsorbed
  on the support rather than bound to the ligand, or multivalent (avidity) binding to a dense anti-Fc layer
  [assessment]. Its size for anti-human-Fc mAb particles and human IgG at 10 ng/mL is **unknown**.
* Consequence: **repeating the regeneration does not converge geometrically.** If the 8 % of Sun2008 were all
  "kinetically slow but reversible", n = ln(10⁻⁴)/ln(0.08) = 3.6 → 4 regenerations would reach 10⁻⁴ (Derived); if a
  fraction φ is irreversible, the floor is φ after any number of cycles. No source gives φ.
* Capacity: < 1 %/cycle over 50 cycles (Anguizola2018), ≈ 0.1 %/cycle over 120 cycles (Şerban2026: (0.88)^(1/120) =
  0.99894, Derived) and > 300 cycles (Kamat2021) are consistent with the model's 0.5 %/cycle
  (`chem.regeneration.activity_loss_per_cycle`, 0–7 %). **Capacity is not the problem; carry-over is.**
* Best reagents found: glycine-HCl pH 2–2.5 (most common), glycine-SDS pH 2.5 or 8 M GuHCl (Meyer2015), chaotrope or
  high-ionic cocktails with EDTA (Andersson1999), NaOH (protein A/G resins, Şerban2026, Tereshin2024). No source
  compares their residual at the 10⁻⁴ level.

### C1.3 Alternative renewal strategies that keep a permanent chip

The principle: **renew the whole capture layer** (or the whole capture solid) every run, so the previous analyte
leaves *with* the layer, and add a chemical strip of what remains. Carry-over then multiplies over independent
removal mechanisms.

| Strategy | Evidence found this session | Reagent per run [assessment unless sourced] | Time added to the 45-min cycle | Effect on 37.5 min injection → result | Carry-over reachable | Fit for human IgG analyte |
|---|---|---|---|---|---|---|
| **R0 glycine regeneration of a covalent anti-Fc bed** (docs/12 C) | §C1.1: > 90 % / 92 % removal; no number < 10⁻² | 100 µL glycine pH 2 (docs/12 §5.6) | 0 (as docs/12: 6.5 min) | none | **unknown floor φ; best found 8×10⁻²** | yes, but carry-over unproven |
| **R1 renewable micro-bed** (bead injection: beads packed per run, flushed out after) | FIRSI: "automated renewal of solid phase for each measurement, which avoids the need for regeneration" (Pollema1994 doi:10.1021/ac00083a008; Willumsen1997 doi:10.1021/ac970268h) [V-abs]; **sandwich** immunoassay on a 3.6 µL renewable Sepharose column, 10 pM in < 20 min, beads "released and replaced with fresh beads" after each measurement (Grate2009 doi:10.1039/b900794f) [V-abs]; **microfabricated** pillar-filter + pneumatic-valve bead trap that traps and releases beads, full assay 10 min, LOD 0.08 ng/mL (TCP) (Fu2011 doi:10.1021/ac1032116) [V-abs]; beads discarded through a 6-port rotary valve in a bead-injection CL sensor (Domínguez-Romero2018 doi:10.1016/j.talanta.2018.01.091) [V-abs]; residual-bead fraction after release: **not reported in any abstract** | 0.1 µL bed = 1.15×10⁵ particles of 10 µm (Derived below) in ≈ 1–2 µL slurry; 40 µL strip acid; 10 µL A1 back-flush | +0.5 min vs R0 (pack 3.0 + flush-out 1.0 + strip 2.0 + re-equilibration 1.0 = 7.0 vs 6.5 min) | none (packing before Inject Start) | **r_b × s + walls** (§C3.8): 10⁻⁴ needs r_b ≤ 1.25×10⁻³ at the worst strip survival s = 0.08 | yes: SA particles with biotin-cAb, the gen-1 reagent |
| **R2 DNA-directed whole-layer renewal** (oligo-coated permanent bed; SA–oligo or cAb–oligo hybridised each run; chaotrope/NaOH dehybridises) | Biacore Biotin CAPture kit: modified streptavidin captured via deoxy-oligonucleotides on Sensor Chip CAP; "Regeneration of the surface after each analysis cycle removes Biotin CAPture Reagent as well as the ligand and any bound analyte. Fresh Biotin CAPture Reagent is attached to the surface for each cycle"; regeneration 6 M GuHCl + 0.25 M NaOH (3 vol 8 M GuHCl + 1 vol 1 M NaOH, Derived), 2 min at 5–30 µL/min; extra 30 % acetonitrile in 0.25 M NaOH if needed; "at least 150 assay cycles per flow cell" (CAP_IFU) [V-vendor / high]; DDI layers "very stable and well suited to recycling by dehybridization" (search summary only) [V-sec / low] | ≈ 10 µL SA–oligo (or cAb–oligo) + 10 µL biotin-cAb; 40 µL GuHCl/NaOH | +2 min (layer loading, if not overlapped) | none if loaded before Inject Start | residual of the old layer × analyte surviving GuHCl/NaOH, + base-surface NSB; **not quantified** (SPR-certified only, §C1.1) | yes; needs an oligo conjugate (new reagent) and NaOH/GuHCl tolerance of glass bed and seals (UNVERIFIED) |
| **R3 desthiobiotin–streptavidin displaced by biotin** | desthiobiotin binds SA "less tightly", "easily dissociated under physiological conditions by either biotin or desthiobiotin" (Hirsch2002 doi:10.1016/s0003-2697(02)00201-4) [V-abs]; SPR chip: desthiobiotin surface + wt-SA bridge + biotinylated bait; bait "very stable" over many regeneration cycles with HCl, Na₂CO₃, glycine or SDS; SA + bait "completely removed by 3 min injections of biotin, guanidinium thiocyanate, pepsin, and SDS"; chip life 2–3 weeks (Knoglinger2017 doi:10.1016/j.bios.2017.07.033) [V-abs] | 10 µL SA + biotin-cAb (pre-complexed); biotin + GuSCN/SDS strip | +3 to +4 min (strip sequence) | none | not quantified ("completely" = SPR-level) | yes; mild for the base layer; SA leaching during the 28-min capture/accumulation window UNVERIFIED (k_off of desthiobiotin–SA not checked) |
| **R4 His-tag / NTA** | Co(II)-NTA FO-SPR: His6-scFv removed by 100 mM EDTA + 500 mM imidazole + 0.5 % SDS pH 8 for 1 min, then 0.5 M NaOH 3 min; 10 cycles (Qu2021) [V-sec]; tris-NTA SPR sensor regenerated ≥ 20 times (Jiang2022) [V-sec]; His6-SA on Ni-NTA stable over 5 experiments in 2 days (Hanson2024) [V-sec] | His-tagged capture reagent (not the docs/05 pair), metal recharge, EDTA/imidazole/SDS + NaOH | +5 to +6 min | none | not quantified | **poor**: needs a recombinant His-tagged capture reagent; EDTA residue near an ALP label (a Mg/Zn enzyme, UNVERIFIED here) and metal leaching are new risks |
| **R5 Protein A/G-captured capture antibody, stripped and reloaded** | protein G binds human IgG directly (human IgG k_d measured on protein G, Anguizola2018); protein A binds human IgG1/2/4 Fc (Şerban2026) | — | — | — | — | **excluded**: the analyte itself binds protein A/G, so the format collapses into direct protein A/G capture regenerated by acid (= R0) |
| **R6 cleavable linkers** (photo-, disulfide-cleavable) | **not searched** in this session (quota kept for R0–R2); no evidence claimed | — | — | — | — | open |
| **R7 blank subtraction / carry-over correction** | §C1.5 | none | 0 | none | cannot meet 10⁻⁴ alone (§C1.5) | — |

**Derived (R1 particle count).** Bed 0.1 µL at ε = 0.4 (docs/12 §5.3) → solids 0.06 µL = 6×10⁷ µm³; one 10 µm
particle = π/6 × 10³ = 523.6 µm³ → 6×10⁷/523.6 = **1.15×10⁵ particles**. A residual of 10⁻³ is ≈ 115 particles —
countable by fluorescence through the glass chip, which makes r_b a direct, cheap bench observable.

**Derived (R1 settling in the pack).** 2.8 µm beads settle ≈ 7 mm/h (docs/07 §5.5 via docs/11 §4); Stokes ∝ d², so
10 µm particles of similar density settle ≈ 7 × (10/2.8)² = 89 mm/h (density UNVERIFIED) — the slurry vial in the
dock pack must be stirred or recirculated before each dose (gen-1 dock-vial approach, docs/11 §4 option 4).

### C1.4 Ranking

1. **R1 renewable micro-bed** — the only option with a precedent for a **sandwich** immunoassay on a renewed
   surface in flow (Grate2009) and a microfabricated trap/release element (Fu2011); uses the gen-1 reagent (SA beads +
   biotin-cAb); carry-over is two independent factors, each separately measurable (bead count; strip survival).
2. **R2 DNA-directed whole-layer renewal** — the strongest *lifetime* evidence for a permanent base (≥ 150 cycles,
   CAP_IFU) and removal of analyte with the layer, but needs a new conjugate and harsh GuHCl/NaOH on glass every run.
3. R3 desthiobiotin — mild, plausible, evidence only SPR-level and 2–3 weeks of chip life.
4. R0 glycine — kept only as a **comparison arm** in the same bench mock-up (it costs nothing extra to measure φ).
5. R4 excluded on reagent grounds, R5 excluded on principle.

### C1.5 Why blank subtraction or carry-over correction alone cannot meet 10⁻⁴

Correction would subtract r̂ × S_prev from the next result, with r̂ a calibrated residual fraction and S_prev the
previous signal. Four reasons, each sufficient:

1. **The challenge is outside the range.** The 10 ng/mL carry-over challenge (docs/08 S6) is 10× above the nominal
   ULOQ of C (1040 pg/mL, docs/12 §5.9); S_prev is not quantified there, so r̂ × S_prev is unknown.
2. **Precision demanded of r̂.** Residual error = (r − r̂) × S_prev. To bring r = 8×10⁻² down to 10⁻⁴, r̂ must be
   right to 10⁻⁴/8×10⁻² = 1.25×10⁻³ relative (0.125 %) every run (Derived). Run-to-run regeneration variation is not
   reported anywhere near that; ≈ 40 % of published regenerations fail a success criterion at all (Goode2015).
3. **The carried analyte is re-measured with the assay's own CV.** Even with r known exactly, the carried-over analyte
   is re-captured and re-labelled with the same variability as a sample; at a blank-level CV of 10 %
   (`chem.nsb.blank_CV_analog_electrochemical` 0.10, 0.03–0.20) the residual after correction is ≈ 0.1 × r. Correction
   therefore buys ≈ 10×: it can reach 10⁻⁴ only if the raw r ≤ ≈ 10⁻³ (Derived).
4. **It adds variance to every blank.** Subtracting an estimated term adds its uncertainty to the blank SD, i.e. to
   the LOD (model terms in docs/09 §4.1); §C3.6 shows that an unremoved residual of 10⁻³ of a 1000 pg/mL predecessor
   already moves the nominal LOD of C′ from 0.64 to 3.1 pg/mL.

The useful role of correction is as a **second layer**: flag any result that follows a sample above a threshold and,
if r is ≤ 10⁻³ by measurement, subtract or re-run; a sacrificial blank cycle after any sample > 100 pg/mL
(docs/08 S6 alternative) costs one 45-min cycle.

## C2. Valving: no membrane valve on the chip

### C2.1 The problem in numbers

docs/12 §5.7: 6 on-chip glass–FEP–glass valves, ≈ 12 actuations per run, ≈ 3600 per 300 runs, **≈ 1200 on the
busiest valve (Vs)**, with protein, particles nearby and pH 2. Published endurance: thermoplastic (eCOC) membranes
"> 50 times without failure" (CHILDERS2024, docs/11 §3); FEP membrane valves "maintain performance over extended use"
with no number (Grover2008, docs/10 §7); ≥ 10⁶ only for PDMS in clean liquids, secondary source (docs/10 §7). The
busiest valve needs 1200/50 = **24×** the only thermoplastic figure (Derived; docs/12 says ≈ 20×). No vendor rating
for moulded or glass membrane valves was found in docs/11 (§3, §8) and none was found now.

### C2.2 Rated lifetimes of dock-side alternatives (checked this session)

| Valve class | Rated life (as stated) | Internal volume | Pressure | Wetted | Tag / conf. | Source |
|---|---|---|---|---|---|---|
| IDEX MX Series II rotary module (the gen-1 V2–V4 family, docs/07) | "With normal use the MX II Module will provide **tens of thousands of cycles**"; main failure cause "abrasive particles in the sample and/or mobile phase or crystallization of buffer solutions"; MXP/MXT rebuildable (RheBuild kits); "long life (**up to 1 million actuations**) MXX models", not user-serviceable | not stated in the manual; MXP9900 0.30 mm passages (docs/07) | MXP9900/9960 (PEEK) 34 MPa; MXX777-xxx (RPC-7) **0.9 MPa** | PEEK, RPC-7, DuraLife | V-vendor / high | MX Series II Operating Manual 2321497F (07/16/2025), https://www.idex-hs.com/docs/uploads/2018/11/MX-Series-II-Operating-Manual.pdf (URL from docs/07) |
| Bio-Chem Valve isolation solenoid (PTFE/PEEK/PPS body; PTFE, EPDM or FFKM diaphragm) | "actuation mechanism … rated to **over 20 million cycles**" (mechanism, not diaphragm) | 18 µL (038T2B, 0.032″ orifice) to 296 µL | 10–30 psi (0.07–0.21 MPa) | PTFE/PEEK + chosen diaphragm | V-vendor / medium (catalogue drawing text) | https://flowchem.readthedocs.io/en/latest/_downloads/231c5bc79e4b696e0c0a09219608bcd0/biochem_solenoids.pdf |
| The Lee Co. LFN 2-way isolation solenoid | "**10 M Cycles Min**", typical on water, application-dependent | **9 µL**, "zero dead volume" | vacuum to 30 psig (0.21 MPa) | PEEK head; FKM, EPDM or FFKM diaphragm | V-vendor (product page via fetch summary) / medium | https://www.theleeco.com/product/lfn-series-2-way-isolation-solenoid-valves |
| Parker Series 1/2 miniature inert PTFE isolation valves | "Cycles per Lifetime: 10 Million" | not read | not read | PTFE | V-sec (search summary; page returned 403) / low | https://ph.parker.com/ca/en/series-1-and-2-miniature-inert-ptfe-isolation-valve |
| Bio-Chem Valve pinch valves (075P/100P) | valve "designed to last for a minimum of **2 million** open and close cycles"; "Silicone tubing is rated for over **500,000** cycles and C-Flex tubing is rated for over **200,000** cycles"; tubing IDs 0.3–3.2 mm | = tubing (0.8 mm ID: 0.5 µL/mm, Derived) | not read | tubing only | V-vendor / high | Bio-Chem Fluidics Pinch Valve Brochure, https://cdn.shopify.com/s/files/1/0651/4779/7727/files/Pinch_Valve_Brochure_111110.pdf |

Silicone tubing is excluded from any path that carries HQ/BQ (PDMS absorbs small hydrophobic molecules, TOEPKE2006,
docs/11 §6.2); C-Flex is used for the bead lines only.

### C2.3 Redesign: what replaces each on-chip valve

| docs/12 valve | Function | C′ replacement | Actuations per run → per 300 runs | Rated | Margin |
|---|---|---|---|---|---|
| Vin, Vb | sample in / BSM park | dock **V_in**: 2-position 6-port MX II (gen-1 V4 role): SM-FL → selector, or → bypass | 2 → 600 | tens of thousands | ≥ 30× (at 2×10⁴, Derived) |
| Vr | reagent selection | dock **V_sel**: MX II-class 6-position selector (model UNVERIFIED): sample line, A1, conjugate, HQDP (guard cell), strip reagent, blocked | ≈ 9 → 2700 | tens of thousands (MXP); 10⁶ (MXX, 0.9 MPa, enough here: bed Δp 0.14 MPa) | ≥ 7× at 2×10⁴ |
| Vs | side outlet open/closed | dock **V_W**: 3-way isolation solenoid (waste ↔ syringe S2 for back-flush) at the end of the side-outlet line | ≈ 5 → 1500 | 10⁷ (LFN) / 2×10⁷ mechanism (Bio-Chem) | > 6000× |
| Vi | IDA protection | **no valve**: 1 mm guard channel + 0.5 µL/min substrate counter-flow from the IDA side whenever liquid flows past N2 (§C2.4) | 0 | — | — |
| Vo | IDA outlet / back-fill | dock **V_O**: 3-way isolation solenoid (IDA outlet ↔ waste / ↔ HQDP counter-flow syringe S3 via the guard cell) | ≈ 4 → 1200 | 10⁷ | > 8000× |
| (new) | bead slurry in / out | **P_Bin, P_Bout**: pinch valves on C-Flex 0.8 mm ID at a dock tee on the chip-inlet line (beads never pass the rotor: abrasive particles are the main rotor failure cause, MX manual) | 2 each → 600 | valve 2×10⁶, tubing > 2×10⁵ | > 300× (tubing, Derived 2×10⁵/600) |

**Result: zero membrane valves on the chip**; every dock valve has ≥ 7× margin on its rated life over a 300-run
chip life (Derived above). Endurance no longer limits the chip life; the chip life is set by the IDA and the bed
cavity (§C3.9). Pressure: V_W and V_O sit downstream of the bed and see only the waste-line pressure; the back-flush
through the bed runs at ≤ 5 µL/min → 0.14 MPa × 5/10 = 0.07 MPa (Kozeny–Carman ∝ Q, docs/12 §5.3) = 10 psi, inside
the 20–30 psi isolation-valve ratings (Derived).

### C2.4 Dead volume and its effect on the stopped-flow readout

With the valves in the dock, the stopped volume is bounded by **closed valves at the ends of tubing**, not at the
chip. Three effects, each Derived:

1. **Diffusive product loss into the port channels.** Each chip port reaches the stopped zone through an on-chip
   restrictor channel. Loss from a zone at concentration c into a semi-infinite channel of cross-section A in time t
   is ≤ c A √(4Dt/π). With D_HQ = 9×10⁻¹⁰ m²/s (`chem.substrates.HQ.diffusion_coefficient`) and t = 450 s:
   √(4 × 9×10⁻¹⁰ × 450/π) = 7.2×10⁻⁴ m. Port P_in (40 × 40 µm, wide enough for 10 µm particles, [assessment]):
   1.6×10⁻⁹ m² × 7.2×10⁻⁴ m = 1.15 nL-equivalent; P_W and P_O (20 × 50 µm): 0.72 nL each. Total 2.6 nL against
   V_acc = 55 nL → **≤ 4.7 %** of the product, specific and NSB alike → LOD-neutral (NSB-limited, docs/09 §4.1),
   ULOQ −5 %.
2. **Compliance.** Water compressibility ≈ 4.6×10⁻¹⁰ Pa⁻¹ (textbook value, UNVERIFIED this session) × 0.14 MPa (bed
   Δp at 10 µL/min) × ≈ 5 µL of upstream line = 0.32 nL released after the stop, 0.6 % of V_acc, once, before the
   accumulation clock starts (10 s settle). Thermal: 2.1×10⁻⁴ K⁻¹ (UNVERIFIED) × 0.05 K × 1 µL = 10 pL. Negligible.
3. **Swept volumes outside the stopped zone.** Inlet line 0.3 m × 100 µm ID = 2.4 µL; V_O + 0.3 m line ≈ 9 + 2.4 =
   11 µL to back-fill the IDA; V_W + line ≈ 11 µL. They add ≈ 12 µL of HQDP per run and ≈ 0.25 min of flushing per
   reagent switch at 10 µL/min (2.4 µL / 10 µL/min = 0.24 min); they do not enter V_acc. Galvanic isolation (F20)
   is kept: the closed dock valves break the liquid path and PEEK ≥ 0.3 m stays on each side
   (`hw.tubing.peek_isolation_length_each_side_of_cell`).

**IDA protection without Vi.** (a) Dead-end diffusion: analyte (D = 3.89×10⁻¹¹ m²/s,
`chem.analyte.diffusion_coefficient`) during the 20-min load: 2√(Dt) = 2√(3.89×10⁻¹¹ × 1200) = 0.43 mm, so at the
end of a 1 mm guard c/c₀ = erfc(1/0.43) = erfc(2.3) ≈ 1×10⁻³; conjugate (taken as IgG-like D) in 6 min: erfc(1/0.24)
≈ 10⁻⁸. (b) Acid would reach the IDA by diffusion (HCl, D ≈ 3×10⁻⁹ m²/s UNVERIFIED: √(2Dt) = 0.85 mm in 2 min), so
during conjugate and strip steps a **counter-flow of 0.5 µL/min of substrate** is pushed from S3 through V_O, the IDA
channel and the guard into N2 and out through V_W: guard velocity 8.3×10⁻¹² m³/s / 1×10⁻⁹ m² = 8.3 mm/s, Péclet
u L/D = 8.3×10⁻³ × 10⁻³ / 3×10⁻⁹ ≈ 2800 ≫ 1, so no back-diffusion (Derived). Cost ≈ 12.5 µL HQDP per run.
(c) Conjugate swept from the guard into the IDA when the flow reverses: ≤ c₀ A √(4Dt/π) = 1 nM × 10⁻⁹ m² ×
1.3×10⁻⁴ m = 1.3×10⁻¹⁹ mol ≈ 80 molecules (Derived, before counter-flow), ≤ 1.6 % of the ≈ 5000 NSB enzymes of a
blank (docs/12 §4.8 order of magnitude), and constant, not variable. The counter-flow is an [assessment] with no
precedent found; it is bench item C′-R4.

---

## C3. Revised candidate C′ — permanent glass chip, renewable micro-bed, dock-side valves, stopped-flow IDA

### C3.1 Concept

The glass chip stays in the dock for its qualified life and contains **no moving parts**: a 0.1 µL bed cavity behind
a 5 µm weir, a side outlet at the bed exit, a 1 mm guard channel and a sealed 25 µm IDA channel. Before every
injection the dock packs a **fresh bed of streptavidin particles pre-loaded with biotinylated capture antibody** from
the daily pack (the gen-1 capture reagent in particle form); the sample is loaded through the bed by the BSM at
10 µL/min, labelled sequentially, the bed is filled with pre-electrolysed substrate and sealed, the product is pushed
into the IDA and read by stopped-flow redox cycling on two potentiostat channels; the bed is then back-flushed to
waste and the empty cavity and inlet path are stripped (glycine pH 2; option R2: GuHCl/NaOH). The only consumable is
the daily reagent pack (particle slurry, conjugate, HQDP, strip reagent). Precedents: renewable-surface sandwich
immunoassay in flow (Grate2009), microfabricated trap/release bead cell (Fu2011), stopped-flow IDA in 70 nL (Chen2011,
docs/10 §4.1), the model's `C-bed-IDA` FRC optimum (docs/05 §1.2).

### C3.2 Block diagram

```
 DOCK                                                           PERMANENT GLASS CHIP (IMT-class, RT-bonded, no valves)
 =====================================================================================================================
 SM-FL --PEEK--> [V_in 2-pos MX II] --load--> [V_sel 6-pos rotary] --+--> tee T1 --100 um ID, 0.3 m--> P_in (40x40 um)
                        '--park--> bypass waste      ^ ports:         |       ^                              |
 S2 syringe (A1) ------------------------------------| A1             |   [P_Bin] pinch, C-Flex <-- particle   v
 conjugate 1 nM (pack, 4-8 C) -----------------------| conjugate      |      slurry (pack, stirred)    N1 bed inlet
 HQDP 1 mM -> GUARD CELL ----------------------------| HQDP           |   [P_Bout] pinch, C-Flex --> waste     |
 strip: glycine-HCl pH 2 (R2: 6 M GuHCl/0.25 M NaOH)-| strip          |                    BED 0.1 uL, 10 um SA-cAb
                                                     | blocked        |                    particles, 0.3 x 0.1 x 3.7 mm
                                                                                            5 um weir
                                                                                              |
 waste <--[V_W 3-way isolation, 10^7]<--100 um, 0.3 m<-- P_W (20x50 um) <---- side outlet ---- N2
            '<-- S2 back-flush                                                                |
                                                                          guard 20x50 um x 1 mm (1 nL)
                                                                                              |
                                                     IDA channel 25 um x 0.2 mm x 3 mm (15 nL), 50 pairs 5/5 um Pt
                                                     Ag/AgCl (or Au QRE) + Pt CE at the outlet end
 waste <--[V_O 3-way isolation, 10^7]<--100 um, 0.3 m<-- P_O (20x50 um) <-------------------------'
            '<-- S3 syringe: HQDP via guard cell (IDA back-fill and 0.5 uL/min counter-flow)
 pogo pins: generator (Ref 600+, +0.35 V), collector (2nd channel, -0.1 to -0.2 V, UNVERIFIED), RE, CE
 Peltier: chip 25.0 C, pack rack 4-8 C.  Pressure sensor on the V_sel common line (bed-packing check, part UNVERIFIED)
 V_acc (sealed: V_sel blocked, pinches, V_W, V_O closed) = bed void 0.04 uL + guard 0.001 + IDA 0.015 = 56 nL
```

### C3.3 Dimensions

| Element | Dimension | Reasoning / source |
|---|---|---|
| Bed cavity | 0.3 × 0.1 mm × 3.7 mm isotropic etch, 0.1 µL; 10 µm particles, ε 0.4; capture area 36 mm² | docs/12 §5.3 (FRC optimum); 1.15×10⁵ particles per bed (§C1.3, Derived) |
| Weir | 5 µm etched step | holds 10 µm particles (docs/12 §5.3); must also release them on back-flush (bench C′-R1) |
| Bed Δp | 0.14 MPa at 10 µL/min; 0.07 MPa at 5 µL/min back-flush | docs/12 §5.3 Kozeny–Carman, scaled ∝ Q |
| Port channels | P_in 40 × 40 µm × 5 mm; P_W, P_O 20 × 50 µm × 5 mm | §C2.4: ≤ 4.7 % product loss |
| Guard | 20 × 50 µm × 1 mm = 1 nL | §C2.4 |
| IDA channel | 25 µm × 0.2 mm × 3 mm = 15 nL; 50 pairs 5/5 µm Pt | docs/12 §5.3; IMT ≥ 2 µm rules (IMT_FLYER); Micrux IDA6 catalogue prototype (BASI_IDA) |
| Chip | ≈ 15 × 45 mm glass, 4 ports | docs/12 §5.3 (DARWIN_SERP format) |
| Dock lines | 100 µm ID PEEK, 0.3 m each (2.4 µL; ≈ 0.02 MPa at 10 µL/min by Hagen–Poiseuille: 8 µ L Q/(π r⁴) = 8 × 10⁻³ × 0.3 × 1.67×10⁻¹⁰ / (π × 6.25×10⁻¹⁸) = 2.0×10⁴ Pa, Derived; µ = 1 mPa·s assumed) | §C2.4 |

### C3.4 Step table (t = 0 at Inject Start; cycle 45.5 min)

| t (min) | Step | Flow / volume | Dock state | Potentiostat |
|---|---|---|---|---|
| −4.0 → −1.0 | **Pack fresh bed**: slurry 2 µL (≈ 1.2×10⁵ particles) at 2 µL/min through P_Bin → P_in → bed → N2 → V_W; A1 condition 5 µL; **Δp check** at 5 µL/min (packed length) | 7 µL | P_Bin, V_W open | – |
| −1.0 → 0 | SM-FL aspirates (full loop, 2× overfill) | BSM 1 µL/min → bypass | V_in park | – |
| 0 → 20.0 | **Load** 2 loop volumes through the bed (`hw.smfl.loop_flush_volumes_for_transfer` 2) | BSM 10 µL/min, 200 µL → V_W | V_in load, V_sel sample, V_W waste | – |
| 20.0 → 21.0 | Post-capture wash | A1 10 µL/min | V_sel A1 | – |
| 21.0 → 27.0 | Conjugate 10 µL of 1 nM (fill 1, stop 2, wash 2, overhead 1); IDA counter-flow on | ≤ 20 µL/min; S3 0.5 µL/min | V_sel conj → A1; V_O ← S3 | – |
| 27.0 → 28.0 | Substrate fill of the bed (guard-cell HQDP) 20 µL → V_W; counter-flow stops at 27.5; **pre-electrolysis** of the IDA fill 27.5 → 28.0 | 20 µL/min | V_sel HQDP; V_O closed at 27.5 | gen +0.35 V, 30 s |
| 28.0 → 35.5 | **Accumulation 7.5 min**, stopped, 56 nL | 0 | all closed | OCP |
| 35.5 → 35.75 | **Transfer**: 60 nL of HQDP pushes the bed-void product through the guard into the IDA channel | 0.24 µL/min | V_sel HQDP, V_O waste | – |
| 35.75 → 37.5 | **Readout**: stopped-flow redox cycling, charge over 1.75 min | 0 | all closed | gen +0.35 V, coll −0.1 to −0.2 V |
| **37.5** | **Result** (38.5 min from aspiration) | | | |
| 37.5 → 38.5 | **Bed flush-out**: S2 back-flush A1 V_W → N2 → weir → bed → P_in → T1 → P_Bout → waste | 5 µL at 5 µL/min | V_W ← S2, P_Bout open | – |
| 38.5 → 40.5 | **Strip** empty cavity, P_in, T1 and V_sel common path: glycine-HCl pH 2 (R2: GuHCl/NaOH) 40 µL; counter-flow on | 20 µL/min | V_sel strip → V_W and P_Bout | – |
| 40.5 → 41.5 | A1 re-equilibration | 20 µL | V_sel A1 | – |
| 41.5 → 45.5 | next cycle's pack (−4.0) and aspiration (−1.0) | | | |

Time to result **37.5 min** (as docs/12 C); cycle **45.5 min** (docs/12 C: 45.0), ≈ 10 per 8 h (480/45.5 = 10.5,
Derived). The docs/12 C step table did not state how the product of the 40 nL bed void reaches the 15 nL IDA
channel; C′ adds the explicit 15-s transfer push (unmodelled; slight product dispersion, direction worse).

### C3.5 Detector and its gain assumptions

Stopped-flow redox cycling on a 5/5 µm Pt IDA (Scheme C, two potentiostat channels), unchanged from docs/12 §5.
Gain evidence (docs/10 §4.1): planar µm-gap IDAs 4–65× (Thomas2004 4× at 1.6 µm; Odijk2008 65× at 1 µm; Lewis2010
7.6× at 25 µm gaps in a 22 µm channel; Ito2023 4.79×), Chen2011 97 % recycling and pAP LOD 10⁻¹⁰ M in 70 nL static;
flow destroys it (Kamath2014 37 → 4 at 500 nL/s) — the read is therefore stopped. For 5/5 µm in a 25 µm channel a gain
of ≈ 5–10× is my expectation [assessment]; the model uses `ma.detection.ida_stopped_efficiency` 0.5 (0.2–1,
UNVERIFIED). **The gain does not move the LOD** while the blank is NSB-limited (EC noise 3–5 % of the blank variance,
docs/12 §2.3, docs/08 S9); C′ keeps the IDA because the permanent die amortises it and because it reads a 15 nL
volume. Collector at −0.1 to −0.2 V is marginal against O₂ reduction (docs/08 W6); glass walls limit O₂ ingress
(docs/11 §6.5, UNVERIFIED). HQ rather than pAP for a reused electrode (Matylitskaya2018 pAP films; Wilson2004).
The electrode never sees protein solution, low pH or particles (guard + counter-flow), which is what justifies the
non-fouling electrode class used in the model (scenario, not measurement).

### C3.6 Reagent pack (daily, 4–8 °C dock rack)

| Item | Per run | Per day (10 runs + 2 priming + 1 recovery = 13) | Storage / note |
|---|---|---|---|
| SA particles (10 µm) with biotin-cAb, blocked, slurry | 2 µL (≈ 1.2×10⁵ particles) | 26 µL + vial dead volume → 0.2 mL vial | stirred (settling ≈ 89 mm/h, Derived §C1.3); capture reagent the same as gen-1 (docs/05 §4.1) on a different particle (bench C′-R2) |
| Conjugate ALP-F(ab′)₂ 1 nM | 10 µL | 130 µL → 0.5 mL vial | liquid, 8-h default life (docs/07 §5.5) |
| HQDP 1 mM via guard cell | 20 (bed) + 12.5 (counter-flow) + 12 (IDA back-fill path) + 0.06 ≈ 45 µL | 0.6 mL | pre-electrolysed (docs/12 §2.3) |
| Strip reagent | 40 µL | 0.5 mL | glycine-HCl pH 2 (stable); R2: GuHCl/NaOH "use within 2 days" (CAP_IFU) |
| A1 (dock S2) | ≈ 50 µL + back-flush 5 µL | 0.7 mL | dock bottle |
| BSM A1 | 200 µL load | – | Waters bottle |

### C3.7 Nearest-model performance estimate

**Method** as docs/12 §8 / Appendix A, on a copy in the scratchpad (nothing written in the repository); n = 2000,
seed 20261111; ΔP < 0.05 not decision-grade (docs/08 W7). Base: `C-bed-IDA` FRC optimum with docs/12's C2 overrides
(side outlet: `ma.nsb.surface_factor_chip` 0.01; non-fouling electrode class). **C′ representation**: renewal block
`hw.timing.regeneration_and_reequilibration` 7.0 min (pack 3 + flush-out 1 + strip 2 + re-equilibration 1); fresh
capture layer `chem.regeneration.activity_loss_per_cycle` 0; residual label after the strip
`chem.regeneration.residual_label_carryover_fraction` 10⁻⁴ (10⁻⁶–10⁻³, with the model's ALP inactivation); C′1 adds
pre-electrolysis (impurity ×0.01, docs/12 §2.3, UNVERIFIED). Residual **analyte** carry-over is not a model term
(docs/12 §5.8); it is represented here through the blank-contamination term
(`ma.nsb.blank_igg_contamination_equivalent` pinned at r × C_prev), which enters the blank variance.

| Run (nearest-model estimate) | Nominal LOD | Median [5–95 %] (pg/mL) | P(success) | P(LOD ≤ 1) | ULOQ | Model time (min) |
|---|---|---|---|---|---|---|
| REF docs/12 C2 (reproduced) | 0.64 | 2.4 [0.48–25] | 0.16 | 0.21 | 1040 | 45.0 |
| **C′0** fresh bed per run, dock valves | 0.64 | 2.4 [0.50–26] | 0.15 | 0.20 | 1040 | 45.5 |
| **C′1** = C′0 + pre-electrolysis | 0.64 | **2.1 [0.46–23]** | **0.16** | 0.22 | 1040 | 45.5 |
| C′1 + L6 + L7 (U1–U3 screening) | 0.53 | **1.8 [0.42–21]** | **0.21** (ULOQ 794 flagged) | 0.27 | 794 | 45.5 |
| C′1, accumulation 15 min, 3 mM HQDP | 0.62 | 2.0 [0.43–23] | 0.19 | 0.24 | 1360 | 53.0 |
| C′1 under S4a (free HQ 10⁻³) | 0.64 | 2.2 [0.47–26] | 0.17 | 0.23 | 1040 | 45.5 |
| C′1, bed-packing CV → blank CV 0.14 (0.05–0.25), scenario | 0.86 | 2.8 [0.55–31] | 0.13 | 0.17 | 1040 | 45.5 |

**Packed-bed NSB-factor sensitivity** (`ma.nsb.surface_factor_packed_bed` pinned; nominal 3, range 1–30, UNVERIFIED):

| Factor | Nominal LOD | Median [5–95 %] | P(success) | P(LOD ≤ 1) |
|---|---|---|---|---|
| 1 | 0.27 | 0.95 [0.26–5.4] | **0.43** | 0.53 |
| 2 | 0.45 | 1.2 [0.35–9] | **0.30** | 0.38 |
| 3 | 0.64 | 1.6 [0.42–12] | 0.23 | 0.30 |
| 5 | 1.0 | 2.4 [0.54–20] | 0.14 | 0.19 |
| 10 | 2.0 | 4.4 [0.83–40] | 0.06 | 0.08 |
| 30 | 6.0 | 13 [1.7–120] | 0.01 | 0.02 |

The G1 GO threshold (P ≥ 0.30, docs/06 §4.11) is reached by C′ only at a packed-bed factor ≤ 2 (Derived from the
table). Pinning the factor at 3 gives P 0.23 against 0.16 when it is sampled over 1–30: the uncertainty itself costs
0.07.

**Residual-analyte carry-over** (r = fraction of the previous sample's analyte that survives renewal; previous
sample C_prev pinned):

| r | C_prev 1000 pg/mL: nominal LOD / median / P | C_prev 100 pg/mL: nominal / median / P |
|---|---|---|
| 1×10⁻⁵ | 0.64 / 2.1 / 0.24 | 0.64 / 2.1 / 0.24 |
| 1×10⁻⁴ | 0.70 / 2.1 / 0.22 | 0.64 / 2.1 / 0.24 |
| 3×10⁻⁴ | 1.1 / 2.3 / 0.07 | 0.64 / 2.1 / 0.24 |
| 1×10⁻³ | 3.1 / 3.7 / 0.00 | 0.70 / 2.1 / 0.22 |
| 1×10⁻² | 30 / 30 / 0.00 | 3.1 / 3.7 / 0.00 |
| 8×10⁻² (glycine, Sun2008) | 260 / 240 / 0.00 | 24 / 24 / 0.00 |

Caveat on this table: whenever the contamination term is non-zero, the Monte Carlo's P baseline is 0.24 instead of
0.16 (the 10⁻⁵ row is effectively zero contamination yet reads 0.24; a run with the term enabled at an upper bound of
10⁻³⁰ M gave the same 0.24). This is an artefact of how the term enters the sampled parameter set, not a physical
gain; **compare P only within this table and read the nominal LOD**. The nominal values are unaffected and show the
point: after a top-of-range sample, r ≈ 10⁻⁴ costs ≈ 10 % in LOD, 3×10⁻⁴ nearly doubles it, 10⁻³ fails, and the
glycine-only 8×10⁻² is two orders of magnitude out.

**Unrepresented chip effects and direction** (docs/09 §5.4): per-run bed packing (amount, length) enters capture and
NSB (**worse**, shown as the blank-CV scenario); transfer push bed → IDA (**slightly worse**, dispersion); port
diffusion loss ≤ 4.7 % (neutral on LOD); bed-cavity walls ≤ ×1.2 NSB (**worse**, as docs/12); counter-flow
substrate traces in the bed exit during conjugate (product washed out; neutral if washed, UNVERIFIED); residual
analyte (above; **decisive**); IDA finger length vs channel (model optimistic, LOD-neutral); fresh capture surface
each run removes the capacity-drift and recalibration overhead of docs/12 C (**better**: no recalibration every 20
runs); temperature control (better).

### C3.8 Carry-over budget against 1×10⁻⁴ (10 ng/mL challenge, docs/08 S6)

| # | Path | Mechanism | Estimate / evidence | Allocation |
|---|---|---|---|---|
| 1 | SM-FL needle and loop | protein film | `hw.smfl.carryover_protein_conjugate` 10⁻⁴ (10⁻⁵–10⁻³), UNVERIFIED — common to A, B, C′ | 3×10⁻⁵ (needs a needle wash better than nominal; measured on gen-1, Stage 2) |
| 2 | V_in, V_sel rotor, inlet line, T1, P_in | sample film on dock-side wetted path | unquantified; every cycle passes 40 µL strip + 25 µL A1 through the same path (§C3.4) | 2×10⁻⁵ |
| 3 | Residual particles after flush-out × analyte surviving the strip on them | r_b × s | r_b UNVERIFIED (no number in Grate2009, Fu2011, Pollema1994 abstracts); s ≤ 0.08 (Sun2008) — s is exactly the R0 regeneration residual φ | 3×10⁻⁵: e.g. r_b ≤ 10⁻³ **and** s ≤ 3×10⁻², or r_b ≤ 3.75×10⁻⁴ at s = 0.08 |
| 4 | Active label on residual particles | r_b × (1 − ALP inactivation) | inactivation by pH ~2: 1 (0.5–1), UNVERIFIED (`chem.enzymes.alp.inactivation_by_low_pH_regeneration`); at 0.5 and r_b = 10⁻³ it would be 5×10⁻⁴ → the strip must kill ALP (≥ 0.99) or include NaOH/GuHCl | 1×10⁻⁵ |
| 5 | Analyte on cavity walls, weir, guard mouth | adsorption surviving the strip | unquantified (glass, ≈ 2.2 mm², docs/12 §5.8) | 1×10⁻⁵ |
| | **Total** | | | **1.0×10⁻⁴** |

Compared with docs/12 C (one path at 8×10⁻² that nothing could reduce), C′ converts carry-over into **five paths,
each with an independent removal mechanism and a separate measurement**: r_b by particle count (115 particles = 10⁻³),
s by the R0 arm, 4 by an IDA read of the stripped cavity, 1–2 by the gen-1 Stage-2 SM-FL test, and the sum by the
10 ng/mL challenge → blanks.

### C3.9 Requirements F1–F20 (changes against docs/12 §5.5 only)

| # | C′ | Status |
|---|---|---|
| F3 | capture phase dosed per run from a stirred pack vial; bed packed into a geometry-defined cavity, Δp check each run | open (risk C′-R3) |
| F13 | guard + counter-flow instead of Vi; electrode sees substrate/product only | met by design (C′-R4) |
| F14 | renewal by replacement of the bed + strip of the empty cavity | open (C′-R1) |
| F15 | §C3.8 budget; five separately measurable paths | open, decisive (C′-R1) |
| F16 | dock valves: isolation solenoids normally closed, pinch valves normally closed, selector to "blocked"; chip stays wet | met |
| F17 | recovery = flush-out + double strip + repack (≈ 9 min), costs one bed | met |
| F18 | 2 blanks + 1 control per pack day; **no recalibration every 20 runs** (fresh capture each run) | met, cheaper than docs/12 C |
| Others | as docs/12 §5.5 | – |

Chip life: no valve and no regenerated capture surface on the chip, so life is set by the IDA (HQ/BQ, 300 strip
exposures of the guard mouth under counter-flow, Ti undercut at pH 2 — docs/12 C4) and the weir (particle wear).
Target ≥ 300 runs is unchanged; repacking replaces docs/12's "repack at 70 % capacity".

### C3.10 Risks and the experiments that decide C′

| # | Risk | Bench experiment | Pass threshold |
|---|---|---|---|
| C′-R1 | carry-over > 10⁻⁴ (residual particles, strip survival, walls) | **Mock-up**: 0.1 µL cavity with 5 µm weir in a milled COC (or Micronit-class glass) channel, dock pinch/solenoid valves, catalogue Micrux IDA6 die downstream. (a) 20 pack/flush-out cycles with fluorescent 10 µm SA particles, count residual particles; (b) **R0 arm**: same cavity, particles left in place, 10 ng/mL human IgG, strip, re-label, read → s (= φ); (c) end-to-end: 10 ng/mL challenge → 3 blanks through the low-range slope (docs/06 E2.7 / E3.4 criterion) | (a) r_b ≤ 10⁻³ (≤ 115 particles) in 20/20; (b) s ≤ 3×10⁻²; (c) **≤ 1×10⁻⁴** |
| C′-R2 | packed-bed NSB factor ≥ 3 | U4-type conjugate exposure series (0.3–3 nM × 2–30 min) on 0.1 µL beds of 10 µm SA particles vs M-280 beads (docs/12 B1/C3) — **shared with B** | factor ≤ 2 (P ≥ 0.30 in §C3.7) |
| C′-R3 | bed packing not reproducible | 20 repacks: Δp, particle count, blank and 10 pg/mL | blank CV ≤ 12 % (P 0.13 at 0.14, §C3.7) |
| C′-R4 | IDA contaminated without Vi (conjugate, acid) | dead-end + counter-flow test: fluorescent conjugate and pH indicator at the guard end, 50 cycles; IDA HQ response before/after | conjugate at IDA ≤ 10⁻⁴ of c₀; IDA HQ slope drift ≤ 2 % over 50 strips |
| C′-R5 | stopped IDA read / transfer push not as assumed | E3.1-type (docs/06) on IDA6 in a 25 µm channel with the 60 nL transfer | product recovery in IDA ≥ 0.8; gain ≥ 4 |

### C3.11 Is revised C viable?

**Viable with conditions.** Neither of docs/12's two blocking problems survives the redesign as an
*unanswerable* question: valve endurance is removed (no on-chip valve; every dock valve ≥ 7× its rated life), and
regeneration carry-over is replaced by a renewal scheme whose carry-over is a product of separately measurable
factors with a 10⁻⁴ budget. The conditions are three bench results on a mock-up costing no glass:

1. **C′-R1(c): end-to-end carry-over ≤ 1×10⁻⁴** after a 10 ng/mL challenge (with r_b ≤ 10⁻³ and s ≤ 3×10⁻² as
   intermediate gates). If it fails, C′ is not viable.
2. **C′-R2: packed-bed NSB factor ≤ 2.** At the nominal 3 C′ is no better than gen-1 (P 0.16 vs 0.16); the factor
   decides whether C′ has any LOD case at all.
3. **C′-R3: blank CV ≤ 12 % over 20 repacks.**

What C′ cannot change: it keeps in-flow sequential labelling (label fraction 0.5 %, docs/12 §5.9), so it gains
little from reagent screening (C′1 + L6 + L7: P 0.21 vs A1 + L6 + L7 0.39), and its throughput is one sample per
45.5 min (no staggering with one bed; a second lane needs two more potentiostat channels). Its advantages are the
shortest time to result (37.5 min), the lowest consumable cost and no per-run consumable solid other than ≈ 10⁵
particles.

---

# PART B — fallback dossier: indexed single-use capture-and-read cells

Concept, block diagram, step table (result 50.0 min, ≈ 26 min per sample with two heads), F1–F20 table and model
mapping are in docs/12 §4 and are not repeated. This part tightens the five items that decide whether B can be built
and calibrated.

## B1. Cell layout and count per card

| Item | Value | Source / reasoning |
|---|---|---|
| Card | microtiter footprint 85.48 × 127.76 mm, ≈ 10 mm body, injection-moulded COC/COP | CS_EXPLAINED; docs/12 §4.3 |
| Cells | **16 = 2 rows × 8**, one row per dock head | docs/12 §4.3; 13 samples + 2 blanks + 1 control per card |
| Cell pitch | **14.0 mm** along the long side: 8 × 14 = 112 mm, margins (127.76 − 112)/2 = 7.9 mm | Derived |
| Cell footprint | ≈ 13 × 34 mm: W1 (Ø 6 mm, 250 µL), W2 (250 µL), W3 (50 µL, dried conjugate), W4 (50 µL), W5 (20 µL), bed 0.5 × 0.5 × 2 mm with two frits, RC 4 × 10 mm × 50 µm | docs/12 §4.3 volumes; layout [assessment] |
| Electrode strip | one glass strip per row: 8 WEs 3.8 × 9.8 mm at 14 mm pitch + per-cell CE/RE pads, ≈ 115 × 12 mm | docs/12 §4.3 (2 strips per card); IMT/Micrux rules (IMT_FLYER, MICRUX_TF) |
| Ports per cell | 5 face-seal through-holes (1.4 mm, 0.6 µL each) under a pierceable foil | docs/12 §4.3; CS_EXPLAINED |
| Pinch points per cell | 5 foil membrane valves closed by dock plungers, each ≤ 3 actuations in its life | docs/12 §4.7 (inside single-use evidence, CS_1367, CHILDERS2024) |

## B2. Changer / indexing mechanism in the dock

docs/12 used two x–y heads. A simpler mechanism with fewer axes [assessment]:

* **One linear axis** carries the card along its long side in 14.0 mm steps (Zaber-class stage, Python library
  ZABER_SW; model UNVERIFIED); **two fixed heads**, one above each row, each on a spring-loaded z-clamp. The x-stage
  sets only the coarse position; **two kinematic pins per cell** in the head engage tapered holes in the card, so the
  1.4 mm port-to-seal registration (± 0.1 mm required [assessment]) is set by moulded geometry, not by stage accuracy.
* Head contents: 5 face seals + piercing needles, 3 pogo pins (WE, CE, RE) per cell, 5 pinch plungers (spring-closed),
  thermal contact pad (Peltier, 25.0 °C) under the engaged cell.
* **Engagement checks per cell** (≈ 2 min, docs/12 §4.4 −3.0 → −1.0): pressure-hold leak test of the 5 seals;
  electrode continuity (open-circuit potential and a small-amplitude impedance point, [assessment]); bed Δp at
  10 µL/min against the lot value; any failure → cell marked used, next cell, no sample lost (the SM-FL has not
  aspirated yet).
* Staggering: SM-FL outlet → dock 2-position valve (MX II, docs/07) → head 1 or head 2 (docs/12 §4.4); the two heads
  never move simultaneously with a cell engaged [assessment].
* **Magazine**: card elevator holding 4 cards = 64 cells ≈ 52 samples unattended (docs/12 §4.3 assessment); used
  cards to a drawer.
* Actuations: ≈ 10 dock solenoid operations per determination ≈ 10⁴ per month (docs/12 §4.7) — dock solenoids are
  rated ≥ 10⁷ (LFN) / 2×10⁷ (Bio-Chem mechanism) (§C2.2); face seals: 16 engagements per card, service item.

## B3. Dried-conjugate rehydration uniformity

Evidence: release from a dried spot is asymmetric without mixing (83 % of the dAb in one half of the stream, 52 %
after a 9-loop Dean mixer, Gervais2011 doi:10.1016/j.bios.2011.06.016, docs/10 §6.1); inkjet-spotted conjugate
reconstitutes into 5–30 % of a 1 µL sample (Hitzbleck2011); dried ALP is humidity- and temperature-cycling-sensitive
(Ford1994); dried HRP conjugate keeps ≈ 80 % after > 5 months at 45 °C (Ramachandran2014).

Design (tightened from docs/12 §4.3): 20 fmol spot in W3 → 20 µL A1 → **10 pressure pulses + 2 min dwell + 10 pulses**
before the 20 µL passes the bed (reconstitution starts at t = 20.0, 7.5 min before use); spot area ≤ 50 % of the W3
floor so the pulses sweep it [assessment]; the volume pushed (20 µL) is the whole well content, so incomplete *mixing*
matters less than incomplete *release* [assessment].

Effect on the LOD (Derived): in sequential labelling both the specific label and the conjugate NSB are ∝ dose in the
linear regime, so dose CV adds in quadrature to the blank CV: √(0.10² + 0.05²) = 0.112 at 5 % dose CV and
√(0.10² + 0.10²) = 0.141 at 10 % (blank CV `chem.nsb.blank_CV_analog_electrochemical` 0.10). Model: B1 at blank CV
0.14 (0.05–0.25) gives median 2.7 pg/mL, P 0.13 vs 2.1 / 0.17 (§B6). **Requirement: delivered conjugate dose CV
≤ 5 % cell-to-cell** (bench B-E3). The same dose CV also scatters the slope, which enters the lot calibration (§B4).

## B4. Per-cell electrode variation and calibration strategy

* **Exhaustive coulometric read** (docs/12 §2.3): charge = nF × moles of product, independent of WE area; the
  background charge (∝ area) is measured on the same fill by PE1. Model: electrode CV 0.02 (cancellation) → B0 P 0.15;
  0.10 (SPE-class, no cancellation, `ma.noise.spe_sensor_to_sensor_cv`) → P 0.12 (docs/12 §4.9). Conversion ≥ 0.95 is
  UNVERIFIED (risk B5).
* **Three-level calibration** [assessment, numbers Derived]:
  1. **Factory lot calibration** per manufacturing lot (bed batch × conjugate lot × strip batch): 6 standards
     (0, 1, 3, 10, 100, 1000 pg/mL) × 3 cells + 6 extra blanks = 24 cells (1.5 cards) per lot; lot slope and blank
     encoded on the card (2-D code read by the dock).
  2. **Per card on the instrument**: 2 blanks + 1 control (≈ 10 pg/mL) = 3/16 = **19 % overhead**; the per-card blank
     mean replaces the lot blank; the control must fall within ± 20 % of the lot curve [assessment], else the card is
     rejected and the lot flagged.
  3. **Per cell**: PE1 background charge, contact check, bed Δp — not calibration, but exclusion criteria.
* Per-cell calibration is impossible by construction, so cell-to-cell CV enters every blank (risk B2): requirement
  blank CV ≤ 10 % across the 20 cells of a batch (bench B-E2).

## B5. Cost class per determination

No prices were seen (docs/11: Micrux and IMT prices on request; ChipShop MOQ 100). A proxy that needs no price —
**lithographic electrode consumed per determination** (Derived from the architectures): B one WE = 1/8 of a strip;
A one die per 16 determinations (1/16); C′ one IDA die per ≥ 300 runs (≤ 1/300). Plus, per determination: B a
moulded cell with packed bed, dried capture and dried conjugate and pierceable foil (1/16 card); A 1/16 of a moulded
filled cartridge; C′ ≈ 1.2×10⁵ particles + ≈ 0.2 mL of pack reagents. **Cost class: B high, A medium, C′ low**
[assessment, as docs/12 §6]. B also has the highest manufacturing QC load (bed packing, drying, spotting per cell).

## B6. Model numbers for B (reproduced and extended; method docs/12 Appendix A, scratch copy, n = 2000)

| Run (nearest-model estimate) | Nominal | Median [5–95 %] | P(success) | P(LOD ≤ 1) | ULOQ | Model time |
|---|---|---|---|---|---|---|
| B0 (reproduces docs/12) | 0.63 | 2.3 [0.52–23] | 0.15 | 0.20 | 1360 | 52.0 |
| B1 = B0 + pre-electrolysis (reproduces docs/12) | 0.63 | 2.1 [0.49–21] | 0.17 | 0.22 | 1360 | 52.0 |
| B1, packed-bed factor 1 | 0.30 | 1.0 [0.28–5.0] | **0.38** | 0.47 | 1360 | 52.0 |
| B1, packed-bed factor 2 | 0.45 | 1.3 [0.37–8.3] | **0.28** | 0.36 | 1360 | 52.0 |
| B1, packed-bed factor 3 | 0.63 | 1.6 [0.44–11] | 0.22 | 0.28 | 1360 | 52.0 |
| B1, blank CV 0.14 (dose / cell CV scenario) | 0.85 | 2.7 [0.56–28] | 0.13 | 0.17 | 1360 | 52.0 |
| B1 + L6 + L7 (docs/12) | 0.51 | 1.8 [0.45–17] | 0.20 | 0.26 | 1040 | 52.0 |

## B7. What would trigger switching from A to B

Switch to B when **one A-side failure** and **both B-side conditions** hold:

* **A-side (any one)**: (i) residual beads in the readout or incubation chamber > 1×10⁻⁴ of the dose that rinse/
  flush redesign cannot fix (A1 mock-up, or PE2 in operation showing persistent residual activity); (ii) chamber
  mixing factor near the 0.2 lower bound (A2), i.e. capture too slow for 30 min; (iii) on-card bead dose CV > 5 %
  over 8 h (A3); (iv) membrane valves or gates fail below 3× life (≈ 210 cycles, A4) **and** the dock-side valve
  approach of §C2 cannot be transferred to A (§C2 shows the endurance problem is solvable off-chip, so (iv) alone
  should not trigger B).
* **B-side (both)**: packed-bed NSB factor ≤ 2 (B-E1: P 0.28–0.38 at ×2–×1, §B6) and cell-to-cell blank CV ≤ 10 %
  (B-E2).
* Independently of A's risks: if the user or a later regulatory context demands **carry-over zero by construction**,
  B is the only candidate that provides it.

## B8. The three bench experiments that decide B

| # | Experiment | Measures | Pass |
|---|---|---|---|
| **B-E1** (= C′-R2, one experiment for both) | U4-type conjugate exposure series (0.3–3 nM × 2–30 min) on 0.5 µL beds of 50 µm SA particles (and 0.1 µL of 10 µm for C′) vs blocked M-280 beads in tubes | packed-bed NSB factor (`ma.nsb.surface_factor_packed_bed`) as enzymes per mm² per nM·min relative to M-280 | **≤ 2** (P ≥ 0.28) |
| **B-E2** | 20 hand-packed cells from one batch on a milled 4-cell card with catalogue Micrux single electrodes; blanks and 10 pg/mL | bed mass CV, blank CV, slope CV, WE-to-WE background charge | blank CV **≤ 10 %**, slope CV ≤ 10 % |
| **B-E3** | dried capture (on-particle) and dried conjugate: reconstitution with/without pulse mixing; ageing 0–8 weeks at 4/25/37 °C with humidity control (Ford1994 risk); 8 h open on the dock after piercing | delivered dose CV, activity and NSB vs wet reagents | dose CV **≤ 5 %**; activity ≥ 80 % and NSB ≤ 1.2× wet after 8 weeks at 4 °C + 8 h open |

docs/12 risks B4 (recirculating capture rate) and B5 (exhaustive read on a shared strip) follow if B-E1–E3 pass.

---

# F. Updated three-way comparison

A numbers are taken from docs/12 (§3.9, §6) unchanged; B from docs/12 and §B6; C′ from §C3.7. All are
nearest-model estimates (n = 2000, success = L_eff ≤ 1); ΔP < 0.05 is not decision-grade (docs/08 W7).

| | **A** bead-transfer multi-run (docs/12) | **B** single-use cells (fallback) | **C** as in docs/12 | **C′** revised permanent chip (this document) |
|---|---|---|---|---|
| Capture renewal | beads per run (liquid) | fresh factory cell per run | glycine regeneration of a covalent bed | **fresh particle bed packed per run + strip of the empty cavity** |
| Labelling / detector | one-step chamber; single WE, stopped, exhaustive | sequential in flow; single WE per cell, exhaustive | sequential in flow; stopped IDA, 2 channels | same as C |
| Median / P as specified | 2.3 / 0.20; **pre-el. 1.9 / 0.25** | 2.3 / 0.15; pre-el. 2.1 / 0.17 | 2.4 / 0.16 | 2.4 / 0.15; **pre-el. 2.1 / 0.16** |
| After U1–U3 screening (L6 + L7) | **1.1 / 0.39** (3 mM, pre-el.) | 1.8 / 0.20 | 1.9 / 0.20 | 1.8 / 0.21 |
| Packed-bed NSB factor ×1 / ×2 / ×10 | not applicable (beads) | 0.38 / 0.28 / 0.06 (B0 ×10, docs/12) | 0.06 at ×10 | **0.43 / 0.30 / 0.06** |
| Inject Start → result | 54.0 min | 50.0 min | 37.5 min | **37.5 min** |
| Throughput | 27.5 min/sample (2 chambers) | ≈ 26 min/sample (2 heads) | 45 min | 45.5 min |
| Carry-over vs 10⁻⁴ | residual beads, **measured every run (PE2)** | **0 by construction** except SM-FL and head bore | needs ≥ 99.99 % glycine elution; best found 92 %; kinetics show the residual is a non-eluting fraction | product of 5 measurable paths, budget 10⁻⁴ (§C3.8); unproven |
| Valves on the consumable / chip | 21; busiest ≈ 70 actuations (1.4× published thermoplastic evidence) | 80 pinch points per card, ≤ 3 each | 6; busiest ≈ 1200 (24×) | **0 on chip**; dock valves ≥ 7× margin on rated life |
| Electrode consumed per determination | 1/16 die | 1/8 strip (one WE) | ≤ 1/300 IDA die | ≤ 1/300 IDA die |
| Consumable cost class [assessment] | medium | high | low | low |
| Dock complexity [assessment] | high | highest | medium | medium–high (selector, 2 solenoids, 2 pinch, 2–3 syringes, guard cell, stirred slurry vial, 2-channel potentiostat) |
| Recalibration | lot + 3 QC per 16 | lot + 3 QC per 16 | every ≈ 20 runs (capacity drift) | 2 blanks + 1 control per day (fresh capture each run) |
| Evidence strength | medium | strongest format precedent (Gyrolab, Ella, i-STAT) | weakest | medium-low: renewable-surface sandwich in flow (Grate2009), microfabricated trap/release (Fu2011); no residual-bead number found |
| Decisive bench result | A1 residual beads, A2 mixing | B-E1 bed factor, B-E2 cell CV, B-E3 dried reagents | carry-over (fatal at 8×10⁻²) | C′-R1 carry-over ≤ 10⁻⁴, C′-R2 bed factor ≤ 2, C′-R3 repack CV |
| Verdict | **recommended** (docs/12) | **fallback** | **not viable** | **viable with conditions** |

## F1. What would have to be true for B or C′ to be preferred over A

**For B over A**: the packed-bed NSB factor ≤ 2 (B-E1) **and** cell-to-cell blank CV ≤ 10 % and dried-reagent dose
CV ≤ 5 % (B-E2, B-E3) **and** at least one of A's own risks fails (residual beads > 10⁻⁴, mixing factor near 0.2, or
bead dose CV > 5 %). B alone also wins if carry-over must be zero by construction. Even then B's LOD case after reagent
screening (P 0.20) is weaker than A's (0.39), because sequential in-flow labelling labels ≈ 1.7 % of the captured
analyte; B wins on robustness, not sensitivity.

**For C′ over A**: everything B needs on the bed factor (≤ 2, shared experiment) **plus** end-to-end carry-over
≤ 1×10⁻⁴ on the renewable-bed mock-up (C′-R1) **plus** repack blank CV ≤ 12 % (C′-R3), **and** the user values
time to result (37.5 vs 54.0 min) and cost per determination (≤ 1/300 of a die) above throughput (45.5 vs 27.5 min
per sample) and above the reagent-screening upside that only the one-step format (A) captures. If the reagent screen
(U2/E1.5) finds no detection reagent with an on-bead t½ ≥ 30 min, A's one-step advantage shrinks (A run sequentially
≈ gen-1 S-chamb, P 0.13, docs/12 §10) and C′'s shorter time and lower cost weigh more.

**Shared cheapest next step**: B-E1 = C′-R2 (packed-bed NSB factor) is one tube-format experiment that decides
whether B or C′ have any LOD case; it needs no flow hardware and can run alongside Stage 1. C′-R1 needs only a milled
mock-up and dock valves already of the gen-1 type. Neither should precede G1a/G1 spending decisions (docs/06 §4.11).

---

## C7. Sources located and read in this session (2026-11-12)

| Key | Identifier | What was read |
|---|---|---|
| Andersson1999 | doi:10.1021/ac981271j (PubMed 10405611) | abstract: regeneration cocktails, > 90 % in 9/13 |
| Goode2015 | doi:10.1021/la503533g (PubMed 25402969) | abstract: ≈ 60 % regeneration success |
| Anguizola2018 | doi:10.1016/j.ymeth.2018.03.013 (PMC6114083) | full text via fetch summary: k_d table, capacity over cycles |
| Nelson2009 | https://consensus.app/papers/details/w:3b451f21-2b11-4b81-8506-44fa3ea8fb1e/ | Consensus abstract |
| Beattie2022 | https://consensus.app/papers/details/w:012c6b2f-9e56-49c3-9c50-94cbe6b57897/ | Consensus abstract |
| Şerban2026 | https://consensus.app/papers/details/w:9638afb6-e570-4c57-989e-d45fd53618d5/ | Consensus abstract |
| Tereshin2024 | https://consensus.app/papers/details/w:39b64dfa-42d1-4755-8c08-173b8ba73947/ | Consensus abstract |
| Park2021, Jeon2018, Foubert2018, Meyer2015, Qu2021, Jiang2022, Hanson2024 | Consensus links in §C1.1/§C1.3 | Consensus abstracts |
| Hirsch2002 | doi:10.1016/s0003-2697(02)00201-4 (PubMed 12419349) | abstract |
| Knoglinger2017 | doi:10.1016/j.bios.2017.07.033 (PubMed 28734694) | abstract |
| Pollema1994 | doi:10.1021/ac00083a008 (PubMed 8030788) | abstract |
| Willumsen1997 | doi:10.1021/ac970268h (PubMed 9286161) | abstract |
| Grate2009 | doi:10.1039/b900794f (PubMed 19381395) | abstract |
| Warner2009 | doi:10.1016/j.bios.2009.06.031 (PubMed 19643593) | abstract: renewable-surface rotating-rod cell, 5 pM BoNT fragment |
| Fu2011 | doi:10.1021/ac1032116 (PubMed 21366237) | abstract |
| Domínguez-Romero2018 | doi:10.1016/j.talanta.2018.01.091 (PubMed 29501151) | abstract |
| CAP_IFU | Cytiva Biotin CAPture Kit Instructions for Use, https://d3.cytivalifesciences.com/prod/IFU/28924234.pdf | text extracted: principle, regeneration, ≥ 150 cycles |
| MXII_MAN | IDEX MX Series II Operating Manual 2321497F, https://www.idex-hs.com/docs/uploads/2018/11/MX-Series-II-Operating-Manual.pdf | text extracted: pressures, maintenance/cycle statements |
| BIOCHEM_PINCH | https://cdn.shopify.com/s/files/1/0651/4779/7727/files/Pinch_Valve_Brochure_111110.pdf | text extracted: valve and tubing cycle ratings, tubing IDs |
| BIOCHEM_ISO | https://flowchem.readthedocs.io/en/latest/_downloads/231c5bc79e4b696e0c0a09219608bcd0/biochem_solenoids.pdf | text extracted: isolation valve volumes, pressures, > 20 M cycles |
| LEE_LFN | https://www.theleeco.com/product/lfn-series-2-way-isolation-solenoid-valves | product page via fetch summary |
| PARKER_S1 | https://ph.parker.com/ca/en/series-1-and-2-miniature-inert-ptfe-isolation-valve | search summary only (403) |

Searched with no usable hit: PubMed "protein A chromatography carryover …", "immunoaffinity … residual …", "SPR …
residual … after regeneration", "DNA-directed immobilization antibody regenerable …" (0 hits each); one WebSearch on
DNA-directed regenerable immunosensors returned no cycle numbers. Cleavable linkers (R6) were not searched.

## Appendix — model runs (scratchpad copy, not in the repository)

```python
# sys.path -> COPY/scripts, COPY/src ; same helpers as docs/12 Appendix A (L = design_lib, F = final_designs)
fc = json.load(open(L.OUT / "optimum_FRC__baseline.json"))["design"]
C  = L.base_arch("FRC").with_design(**fc)
Cp = C.with_design(**{"hw.timing.regeneration_and_reequilibration": 7.0})          # C' renewal block
def Cp_ps(p):                                                                       # C2 overrides + fresh layer
    p = C_ps(p).with_values({"chem.regeneration.activity_loss_per_cycle": 0.0})
    return L.with_bounds(p, "chem.regeneration.residual_label_carryover_fraction", value=1e-4, low=1e-6, high=1e-3)
s = L.mc(Cp, pre_el(Cp_ps(ps0)), n=2000)                                            # C'1
# bed factor: .with_values({"ma.nsb.surface_factor_packed_bed": f}); residual analyte r after C_prev:
# .with_values({"ma.nsb.blank_igg_contamination_equivalent": r * C_prev * 1e-12/1.5e5*1e3})   # M
# B: docs/12 Appendix A B and B_ps, lod_scale 0.996/0.90, + pre_el, + bed factor / blank-CV variants
```
