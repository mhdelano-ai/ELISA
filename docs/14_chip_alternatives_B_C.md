# 14 — Second-generation cartridge: the alternatives B and C in depth

Status: 2026-11-12, written after the user checkpoint of docs/12 §9. Candidate A goes to detailed design in docs/13
(not touched here). This document (i) tries to make candidate C (permanent glass chip, stopped-flow IDA, daily reagent
pack) viable, as the user asked, and (ii) tightens candidate B (single-use cells) into a fallback dossier. Inputs:
docs/00, 05, 08, 09, 10, 11, 12, `params/*.yaml`, `src/elisa_sim/`, `scripts/`, and the literature and vendor
documents read in this session (§C7). No other file was changed; the model was run on a copy in the session scratchpad.

> **Revised after review (docs/15), 2026-11-12.** The independent review docs/15 found that the C′ residual-analyte
> table had deleted the model's default contamination term, that the guard-cell pre-electrolysis credit of B and C′ is
> not supported at the flows used, and that the comparison table mixed rows. The affected passages were rewritten and
> the model re-run on a fresh scratchpad copy (n = 2000, seed 20261111; nothing generated in the repository). **B and
> C′ are now quoted without pre-electrolysis credit as the headline**; the credit is a re-derived, UNVERIFIED
> scenario pending E1.2b (docs/06). User decisions of 2026-11-12 are applied (dock-supplied reagents accepted;
> carry-over rule = 1×10⁻⁴ criterion kept **plus** a mandatory cleaning cycle and blank check after any
> result > 100 pg/mL).
>
> | docs/15 finding | What changed | Sections |
> |---|---|---|
> | S9 (contamination term deleted) | residual-analyte table redone with the carry-over **added** to the default 0–3 fM term; "artefact" caveat removed; conclusions and §0 rewritten | §0, §C1.5 item 4, §C3.7, Appendix |
> | S8 (guard-cell credit unsupported) | credit removed from the headline; re-derived as a ×0.05 scenario that needs a per-run guard-cell fill at ≥ 300 µL/min; C′ in-IDA "pre-electrolysis" shown to give no credit; B's 1 mL holding loop replaced | §0, §C3.1, §C3.2, §C3.4, §C3.6, §C3.7, §C3.11, §B0 (new), §B3, §B6, §F |
> | S10 (tables inconsistent) | every candidate with and without credit; A column marked as to be read from docs/13 Revision B (finalised by docs/16) | §0, §F, §F1 |
> | S11 (carry-over budget vs SM-FL) | SM-FL allocation and the user's cleaning rule stated | §C3.8 |
> | W4 (challenge cannot resolve 10⁻⁴) | C′-R1(c) challenge raised to 100 ng/mL or n ≥ 10 pairs | §C3.10 |
> | W8 (docs/09 F1 relaxed) | B's 0.90 transfer recorded as a requirement change | §B0 |
> | W9 (transfer push, counter-flow volume, pinch-valve pressure) | IDA recovery defined as concentration; counter-flow 4.3 µL; pinch-valve pressure rating flagged | §C2.3, §C2.4, §C3.6, §C3.10 |
> | W10 + §4 #5 (Sun2008 over-read) | 92 % qualified as one elution recovery in a hapten system, not a residual | §0, §C1.1, §C1.2, §C1.3, §C1.5, §C3.7, §C3.8, §F |
> | §4 #12, §3 (Anguizola2018 k_d) and N6 (part numbers) | k_d marked UNVERIFIED for decisions; vendor ratings marked verified/UNVERIFIED as docs/15 found them; Parker replaced by a generic description | §0, §C1.1, §C1.2, §C2.2, §C2.3, §C7 |
> | User decisions 2026-11-12 | cleaning rule applied to B (no design change) and C′ (interaction with the repack cycle); dock-supplied reagents | §C1.5, §C3.8, §C3.11, §B0, §F |

**Sourcing conventions** (as docs/10–12). Every number names its source: a repository section or parameter key, a
literature key with DOI, or a vendor document with URL. Verification tags for sources read **in this session**:
**[V-abs]** PubMed abstract/metadata; **[V-full]** full text read through the fetch tool's summary (numbers quoted
by the tool, not seen as a table by me); **[V-vendor]** vendor document whose text I extracted and read;
**[V-sec]** search-engine or Consensus summary only. Sources carried from docs/10–12 keep their tags there.
**Derived** = calculated here with the arithmetic shown. **[assessment]** = engineering judgement. **UNVERIFIED** =
not checked against a source in this session. Confidence: high / medium / low as in docs/10.

---

## 0. Summary

**C as specified in docs/12 is not viable.** No source found measures the residual of captured protein after
regeneration below ~10⁻²; the only chip number is one elution recovery of 92 % in a hapten system (FITC-HSA on an
anti-FITC monolith, Sun2008 — not an IgG sandwich and not a measured surface residual; docs/15 W10). If the acid
off-rate reported for human IgG on protein G (k_d ≈ 0.17–0.37 s⁻¹ at pH 2.5, Anguizola2018 — read in this document's
session via a fetch summary, not confirmable from the abstract in docs/15, so **UNVERIFIED for decisions**) applies,
the reversible part is stripped essentially completely in 2 min (exp(−0.166 × 120) ≈ 2×10⁻⁹, Derived), and whatever
stays behind is a **non-eluting sub-population** (denatured/aggregated IgG, non-specific adsorption, avidity), which
repetition does not remove geometrically. Glycine regeneration of a permanent capture surface therefore has **no
evidence path to 10⁻⁴**, and correction cannot close a gap of unknown but likely ≥ 100× (§C1.5). The busiest on-chip
valve also needs ≈ 24× the only thermoplastic membrane-valve endurance figure.

**Revised C (C′) — viable with conditions.** Keep the permanent glass chip, the side outlet and the stopped-flow IDA;
change two things:

1. **Renew, do not regenerate**: the 0.1 µL capture bed is a **renewable micro-bed** (bead-injection principle:
   Pollema1994, Willumsen1997, Grate2009, Fu2011) packed from the daily pack before every injection and back-flushed
   out after the read, followed by an acid strip of the empty cavity. Carry-over then becomes a **product of
   independent removal steps** — residual-bead fraction × fraction of analyte surviving the strip on those beads
   (+ wall terms) — instead of one regeneration efficiency. A DNA-directed whole-layer renewal (Biacore CAP
   principle: capture reagent + ligand + analyte removed every cycle, ≥ 150 cycles per surface) is the second option.
2. **No valve on the chip**: all switching moves to the dock — one rotary selector (IDEX MX Series II class, rated
   "tens of thousands of cycles", ≈ 3000 needed per 300 runs), isolation solenoids (≥ 10⁷ cycles rated) on the two
   outlets, pinch valves on replaceable tubing for the bead lines (valve ≥ 2×10⁶, C-Flex tubing > 2×10⁵; pressure
   rating not read, see §C2.3). The IDA channel is protected as a **dead-end branch with a 1 mm guard channel**; the
   diffusive loss of product into the four port channels is ≤ 5 % (Derived), LOD-neutral.

Nearest-model estimates (n = 2000; §C3.7), **headline without pre-electrolysis credit**: **C′0 median 2.4 pg/mL
[0.50–26], P 0.15 as specified; 1.8 / 0.21 after U1–U3 screening; 37.5 min injection → result, cycle 45.5 min.**
With the re-derived guard-cell credit (×0.05, needs a per-run guard-cell fill at ≥ 300 µL/min; **UNVERIFIED** pending
E1.2b and a guard-cell flow test): 2.1 / 0.16 as specified, 1.8 / 0.21 after screening. The credit is worth ≈ +0.01
at nominal and matters only under S4a (free HQ 10⁻³: P 0.015 → 0.14). The decisive parameter is the packed-bed NSB
factor (without credit P 0.39 at ×1, 0.27 at ×2, 0.21 at ×3, 0.05 at ×10), which C′ shares with B. Carry-over of
residual analyte (added to the model's default 0–3 fM contamination term, docs/15 S9): after a 1000 pg/mL
predecessor, r = 10⁻⁴ takes P 0.15 → **0.10** and r = 3×10⁻⁴ → **0.006**; after a ≤ 100 pg/mL predecessor r ≤ 3×10⁻⁴
costs ≤ 0.01. Under the user's rule (cleaning cycle + blank check after any result > 100 pg/mL) no real sample follows
a predecessor above 100 pg/mL, so the second case applies to samples — but the 1×10⁻⁴ end-to-end criterion is kept
and remains the hard condition. **Conditions** (bench, before any glass): end-to-end carry-over ≤ 1×10⁻⁴ on a
renewable-bed mock-up (100 ng/mL challenge or ≥ 10 challenge pairs, docs/15 W4; ≤ 10⁻³ residual particles as the
intermediate gate), packed-bed NSB factor ≤ 2 (≲ 1.7 for P ≥ 0.30 without credit), and blank CV ≤ 12 % over 20
repacks.

**B** stays the fallback: single-use cells remove the carry-over and valve-endurance questions by construction; it
is decided by the same packed-bed NSB factor, by cell-to-cell CV and by dried-reagent behaviour (Part B). Headline
without credit: **B0 2.3 [0.52–23] / P 0.15; 1.8 / 0.20 after screening**; with the re-derived ×0.05 credit
(UNVERIFIED) 2.1 / 0.17 and 1.8 / 0.20. The user's cleaning rule changes nothing in B's design.

**Three-way verdict** (§F): A remains the leading concept (docs/12, docs/15 §5) because it keeps the one-step format
(best gain from reagent screening) and does not rest on the packed-bed factor; A's numbers must be read from docs/13
Revision B (finalised by docs/16), not from docs/12. Without any credit **neither B nor C′ beats gen-1 (P 0.16)** as
specified. B or C′ become preferable only if the packed-bed NSB factor comes back ≤ 2 (better ≲ 1.5) **and** A's
residual-bead or mixing risks fail; C′ in addition needs the carry-over test.

---

# PART C — making the permanent-chip candidate viable

## C1. Regeneration of a permanent capture surface: what the literature shows

### C1.1 Quantitative evidence found in this session

| Key | System | Regeneration reagent | Removal / residual | Cycles, capacity | Tag / conf. | Source |
|---|---|---|---|---|---|---|
| Andersson1999 | Biacore, 13 antibody–antigen systems, multivariate regeneration cocktails | 6 stock solutions (acidic, basic, ionic, chaotropic, detergent, solvent) and mixtures; EDTA found to be a good additive to chaotrope/high-ionic cocktails | "removed more than 90 % of the bound analyte in a 30 s pulse" in 9 of 13 systems; "regenerated the surface completely" in 5 | not in abstract | V-abs / high | doi:10.1021/ac981271j |
| Goode2015 | systematic review + meta-analysis of biosensor regeneration | acid, base, detergent, chaotrope, etc. | only "∼60 % of the reported studies analyzed were deemed a success" under a working definition | — | V-abs / high (qualitative) | doi:10.1021/la503533g |
| Anguizola2018 | protein G affinity microcolumn, rabbit/goat/**human**/mouse IgG | 0.067 M phosphate pH 2.5 elution; pH 7.4 re-equilibration 10 min (≥ 5 min sufficient, 5 vs 20 min < 2 % different) | human IgG k_d at pH 2.5 = **0.166 ± 0.001 s⁻¹** (0.5 mL/min) to 0.374 s⁻¹ (2 mL/min); at pH 3.0 k_d 3.1× lower; **% not eluted: not reported** | capacity varied **< 1 % (0.3–0.9 %) between cycles over up to 50 cycles**; columns stable ≈ 200 cycles / 1 year | V-full (fetch-tool summary, numbers not seen as a table) / medium; **docs/15: abstract lacks the numbers → UNVERIFIED** (revised after review) | doi:10.1016/j.ymeth.2018.03.013 (PMC6114083) |
| Nelson2009 | immunoaffinity HPAC (anti-2,4-D mAb) | pH 2.5 | analyte k_d at pH 2.5 = 0.056–0.17 s⁻¹; antibody re-folding after elution first-order, 2.4×10⁻⁴ s⁻¹ (t½ ≈ 48 min, Derived: ln2/2.4×10⁻⁴ = 2888 s) | — | V-sec (Consensus) / medium | https://consensus.app/papers/details/w:3b451f21-2b11-4b81-8506-44fa3ea8fb1e/ |
| Sun2008 (docs/10) | epoxy affinity monolith in PMMA, FITC-tagged HSA on anti-FITC (hapten system) | — | 92 % mean **elution recovery** (not a measured surface residual; not an IgG sandwich; docs/15 W10) | — | V-abs (docs/10; confirmed docs/15) | doi:10.1021/ac800322f |
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

* **Derived.** If captured IgG behaved as a single population with the reported acid off-rate, 2 min of pH 2.5 would
  leave exp(−k_d t) = exp(−0.166 × 120) = exp(−19.9) = 2.3×10⁻⁹ (Anguizola2018, protein G, human IgG; 0.5 mL/min;
  k_d **UNVERIFIED** for decisions, see §C1.1). Even 30 s leaves exp(−5.0) = 7×10⁻³. Kinetically, 10⁻⁴ is reached
  after t = ln(10⁴)/0.166 = 55 s.
* The eluted fractions actually reported are far below this ("> 90 %" in a 30 s pulse in 9/13 Biacore systems,
  Andersson1999; one 92 % elution recovery in a hapten system, Sun2008, which is not a measured residual), and used
  protein A resin carries **irreversibly bound mAb** (Beattie2022). The residual is therefore plausibly set by a
  sub-population that does not elute on the time scale of the step — denatured or aggregated protein, protein adsorbed
  on the support rather than bound to the ligand, or multivalent (avidity) binding to a dense anti-Fc layer
  [assessment]. Its size for anti-human-Fc mAb particles and human IgG at 10 ng/mL is **unknown: no residual has been
  measured for this or any comparable IgG sandwich surface**.
* Consequence: **repeating the regeneration need not converge geometrically.** Illustration only: if a non-eluted 8 %
  (the complement of Sun2008's recovery, used as an order of magnitude) were all "kinetically slow but reversible",
  n = ln(10⁻⁴)/ln(0.08) = 3.6 → 4 regenerations would reach 10⁻⁴ (Derived); if a fraction φ is irreversible, the floor
  is φ after any number of cycles. No source gives φ.
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
| **R0 glycine regeneration of a covalent anti-Fc bed** (docs/12 C) | §C1.1: > 90 % removal in 9/13 Biacore systems; one 92 % elution recovery in a hapten system (Sun2008); no residual < 10⁻² measured | 100 µL glycine pH 2 (docs/12 §5.6) | 0 (as docs/12: 6.5 min) | none | **unknown floor φ; no residual measured** (one 92 % elution recovery in a hapten system, Sun2008) | yes, but carry-over unproven |
| **R1 renewable micro-bed** (bead injection: beads packed per run, flushed out after) | FIRSI: "automated renewal of solid phase for each measurement, which avoids the need for regeneration" (Pollema1994 doi:10.1021/ac00083a008; Willumsen1997 doi:10.1021/ac970268h) [V-abs]; **sandwich** immunoassay on a 3.6 µL renewable Sepharose column, 10 pM in < 20 min, beads "released and replaced with fresh beads" after each measurement (Grate2009 doi:10.1039/b900794f) [V-abs]; **microfabricated** pillar-filter + pneumatic-valve bead trap that traps and releases beads, full assay 10 min, LOD 0.08 ng/mL (TCP) (Fu2011 doi:10.1021/ac1032116) [V-abs]; beads discarded through a 6-port rotary valve in a bead-injection CL sensor (Domínguez-Romero2018 doi:10.1016/j.talanta.2018.01.091) [V-abs]; residual-bead fraction after release: **not reported in any abstract** | 0.1 µL bed = 1.15×10⁵ particles of 10 µm (Derived below) in ≈ 1–2 µL slurry; 40 µL strip acid; 10 µL A1 back-flush | +0.5 min vs R0 (pack 3.0 + flush-out 1.0 + strip 2.0 + re-equilibration 1.0 = 7.0 vs 6.5 min) | none (packing before Inject Start) | **r_b × s + walls** (§C3.8): 10⁻⁴ needs r_b ≤ 1.25×10⁻³ at an illustrative strip survival s = 0.08 (s unmeasured) | yes: SA particles with biotin-cAb, the gen-1 reagent |
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
2. **Precision demanded of r̂.** Residual error = (r − r̂) × S_prev. To bring an illustrative r = 8×10⁻² (the
   complement of Sun2008's hapten-system recovery; no IgG residual is measured) down to 10⁻⁴, r̂ must be right to
   10⁻⁴/8×10⁻² = 1.25×10⁻³ relative (0.125 %) every run (Derived). Run-to-run regeneration variation is not
   reported anywhere near that; ≈ 40 % of published regenerations fail a success criterion at all (Goode2015).
3. **The carried analyte is re-measured with the assay's own CV.** Even with r known exactly, the carried-over analyte
   is re-captured and re-labelled with the same variability as a sample; at a blank-level CV of 10 %
   (`chem.nsb.blank_CV_analog_electrochemical` 0.10, 0.03–0.20) the residual after correction is ≈ 0.1 × r. Correction
   therefore buys ≈ 10×: it can reach 10⁻⁴ only if the raw r ≤ ≈ 10⁻³ (Derived).
4. **It adds variance to every blank.** Subtracting an estimated term adds its uncertainty to the blank SD, i.e. to
   the LOD (model terms in docs/09 §4.1); §C3.7 shows that an unremoved residual of 10⁻⁴ of a 1000 pg/mL predecessor
   already takes P from 0.15 to 0.10, and 10⁻³ moves the nominal LOD of C′ from 0.64 to 3.1 pg/mL (P 0.00).

The useful role of correction is as a **second layer**. The user decided (2026-11-12) the layer: the 1×10⁻⁴
criterion is kept, **plus a mandatory cleaning cycle and blank check after any result > 100 pg/mL** (the docs/08 S6
alternative made mandatory). For C′ this costs one extra flush-out + double strip and one blank determination on a
fresh bed (≈ 9 + 45.5 min) per triggering result (§C3.8).

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
| IDEX MX Series II rotary module (the gen-1 V2–V4 family, docs/07) | "With normal use the MX II Module will provide **tens of thousands of cycles**"; main failure cause "abrasive particles in the sample and/or mobile phase or crystallization of buffer solutions"; MXP/MXT rebuildable (RheBuild kits); "long life (**up to 1 million actuations**) MXX models", not user-serviceable | not stated in the manual; MXP9900 0.30 mm passages (docs/07) | MXP9900/9960 (PEEK) 34 MPa; MXX777-xxx (RPC-7) **0.9 MPa** | PEEK, RPC-7, DuraLife | V-vendor / high (this session; not re-checked in docs/15) | MX Series II Operating Manual 2321497F (07/16/2025), https://www.idex-hs.com/docs/uploads/2018/11/MX-Series-II-Operating-Manual.pdf (URL from docs/07) |
| Bio-Chem Valve isolation solenoid (PTFE/PEEK/PPS body; PTFE, EPDM or FFKM diaphragm) | "actuation mechanism … rated to **over 20 million cycles**" (mechanism, not diaphragm) | 18 µL (038T2B, 0.032″ orifice) to 296 µL | 10–30 psi (0.07–0.21 MPa) | PTFE/PEEK + chosen diaphragm | V-vendor / medium (catalogue drawing text; not re-checked in docs/15) | https://flowchem.readthedocs.io/en/latest/_downloads/231c5bc79e4b696e0c0a09219608bcd0/biochem_solenoids.pdf |
| The Lee Co. LFN 2-way isolation solenoid | "**10 M Cycles Min**", typical on water, application-dependent | **9 µL**, "zero dead volume" | vacuum to 30 psig (0.21 MPa) | PEEK head; FKM, EPDM or FFKM diaphragm | V-vendor (product page via fetch summary) / medium; **verified in docs/15** (src-check: "10 M Cycles Min", 9 µL, vac–30 psig) | https://www.theleeco.com/product/lfn-series-2-way-isolation-solenoid-valves |
| Further all-PTFE miniature isolation valve (second source; **to be selected**) | **UNVERIFIED** (a 10⁷-cycle figure was seen only in a search-engine summary; the vendor page was not readable, so no part or rating is claimed; revised after review, docs/15 N6) | UNVERIFIED | UNVERIFIED | PTFE | UNVERIFIED | – |
| Bio-Chem Valve pinch valves (075P/100P) | valve "designed to last for a minimum of **2 million** open and close cycles"; "Silicone tubing is rated for over **500,000** cycles and C-Flex tubing is rated for over **200,000** cycles"; tubing IDs 0.3–3.2 mm | = tubing (0.8 mm ID: 0.5 µL/mm, Derived) | **not read — UNVERIFIED**; must be ≥ 0.3 MPa (bed Δp 0.14–0.29 MPa at the bed-inlet tee, docs/15 W9) | tubing only | V-vendor / high; **verified in docs/15** (brochure text) | Bio-Chem Fluidics Pinch Valve Brochure, https://cdn.shopify.com/s/files/1/0651/4779/7727/files/Pinch_Valve_Brochure_111110.pdf |

Silicone tubing is excluded from any path that carries HQ/BQ (PDMS absorbs small hydrophobic molecules, TOEPKE2006,
docs/11 §6.2); C-Flex is used for the bead lines only.

*Part numbers (revised after review, docs/15 N6).* The part designations above that are not in docs/11 — Lee LFN,
Bio-Chem 038T2B and 075P/100P, IDEX MXX777-xxx — are kept only because each comes from a vendor document read in this
session with the rating quoted (§C7: LEE_LFN, BIOCHEM_ISO, BIOCHEM_PINCH, MXII_MAN); docs/15 re-checked LEE_LFN and
BIOCHEM_PINCH. The Parker designation was removed (no readable source). None of them is a selection: each must be
added to docs/11 §9 with its source before any BOM use, and prices were not seen.

### C2.3 Redesign: what replaces each on-chip valve

| docs/12 valve | Function | C′ replacement | Actuations per run → per 300 runs | Rated | Margin |
|---|---|---|---|---|---|
| Vin, Vb | sample in / BSM park | dock **V_in**: 2-position 6-port MX II (gen-1 V4 role): SM-FL → selector, or → bypass | 2 → 600 | tens of thousands | ≥ 30× (at 2×10⁴, Derived) |
| Vr | reagent selection | dock **V_sel**: MX II-class 6-position selector (model UNVERIFIED): sample line, A1, conjugate, HQDP (guard cell), strip reagent, blocked | ≈ 9 → 2700 | tens of thousands (MXP); 10⁶ (MXX, 0.9 MPa, enough here: bed Δp 0.14–0.29 MPa) | ≥ 7× at 2×10⁴ |
| Vs | side outlet open/closed | dock **V_W**: 3-way isolation solenoid (waste ↔ syringe S2 for back-flush) at the end of the side-outlet line | ≈ 5 → 1500 | 10⁷ (LFN) / 2×10⁷ mechanism (Bio-Chem) | > 6000× |
| Vi | IDA protection | **no valve**: 1 mm guard channel + 0.5 µL/min substrate counter-flow from the IDA side whenever liquid flows past N2 (§C2.4) | 0 | — | — |
| Vo | IDA outlet / back-fill | dock **V_O**: 3-way isolation solenoid (IDA outlet ↔ waste / ↔ HQDP counter-flow syringe S3 via the guard cell) | ≈ 4 → 1200 | 10⁷ | > 8000× |
| (new) | bead slurry in / out | **P_Bin, P_Bout**: pinch valves on C-Flex 0.8 mm ID at a dock tee on the chip-inlet line (beads never pass the rotor: abrasive particles are the main rotor failure cause, MX manual) | 2 each → 600 | valve 2×10⁶, tubing > 2×10⁵; **pressure rating not read (UNVERIFIED)** — P_Bout sees the bed Δp (0.14–0.29 MPa) during load and fills | > 300× (tubing, Derived 2×10⁵/600) |

**Result: zero membrane valves on the chip**; every dock valve has ≥ 7× margin on its rated life over a 300-run
chip life (Derived above). Endurance no longer limits the chip life; the chip life is set by the IDA and the bed
cavity (§C3.9). Pressure: V_W and V_O sit downstream of the bed and see only the waste-line pressure; the back-flush
through the bed runs at ≤ 5 µL/min → 0.14 MPa × 5/10 = 0.07 MPa (Kozeny–Carman ∝ Q, docs/12 §5.3) = 10 psi, inside
the 20–30 psi isolation-valve ratings (Derived). The pinch valves on the bed-inlet tee are the exception: during
sample load (10 µL/min) and fills (≤ 20 µL/min) they hold the full bed Δp of 0.14–0.29 MPa (docs/12 §5.3) and their
pressure rating was not read (docs/15 W9): check it before relying on them; if it is below ≈ 0.3 MPa, move the tee
behind a rated isolation valve or limit fills to 10 µL/min.

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
u L/D = 8.3×10⁻³ × 10⁻³ / 3×10⁻⁹ ≈ 2800 ≫ 1, so no back-diffusion (Derived). Cost 0.5 µL/min × (6.5 + 2) min
≈ 4.3 µL HQDP per run (corrected after review, docs/15 W9; previously 12.5 µL). This substrate is displaced from
the IDA by the transfer push before the read and needs no guard-cell treatment.
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
10 µL/min, labelled sequentially, the bed is filled with substrate and sealed, the product is pushed
into the IDA and read by stopped-flow redox cycling on two potentiostat channels; the bed is then back-flushed to
waste and the empty cavity and inlet path are stripped (glycine pH 2; option R2: GuHCl/NaOH). The only consumable is
the daily reagent pack (particle slurry, conjugate, HQDP, strip reagent). Precedents: renewable-surface sandwich
immunoassay in flow (Grate2009), microfabricated trap/release bead cell (Fu2011), stopped-flow IDA in 70 nL (Chen2011,
docs/10 §4.1), the model's `C-bed-IDA` FRC optimum (docs/05 §1.2).

**Substrate pre-treatment — what is and is not electrolysed (revised after review, docs/15 S8).** The first version of
C′ claimed the docs/12 ×0.01 pre-electrolysis credit. It does not hold: (i) the commercial coulometric guard cell named
in docs/12 §9 (`hw.flow_cells.thermo_6011rs_coulometric`: collection efficiency 0.95, 0.8–1.0; minimum flow 300 µL/min;
repository values, vendor document not re-read — UNVERIFIED) was run at ≤ 20 µL/min (bed fill), 5 µL (IDA back-fill)
and 0.5 µL/min (counter-flow), all far below its minimum flow; (ii) even at its rated flow it leaves 5 % (0–20 %) of
the free HQ, i.e. ×0.05, not ×0.01; (iii) the only volume electrolysed in place was the 15 nL IDA fill, and the
transfer push **replaces** that fill with bed-void content (bed fill + push substrate) before the read — so the in-IDA
step gives no credit at all. What the read volume contains is the substrate that filled the bed. Re-derived design
(this revision): the guard cell fills a **per-run holding coil** (≈ 30 µL PEEK, 3 coil volumes at ≥ 300 µL/min ≈ 90 µL
in 18 s, ≤ 2 min before the bed fill) that feeds the V_sel HQDP port for the bed fill and the transfer push; free HQ
re-formed in the coil in ≤ 10 min is ≤ 10⁻⁹ s⁻¹ × 600 s = 6×10⁻⁷ mol/mol at the acceptance-limit k_h (Derived;
`ma.chemistries.alp_hqdp.hydrolysis_rate` high bound), ≈ 0.06 of the nominal lot impurity. Model representation of
the credit: impurity × **0.05** (scenario, **UNVERIFIED** until E1.2b (docs/06) shows the chemical floor and a flow test
of the guard cell gives its real escape). The headline numbers carry **no credit**. The generator step on the IDA
fill (27.5 → 28.0) is kept only to condition the electrode and record its background charge.

### C3.2 Block diagram

```
 DOCK                                                           PERMANENT GLASS CHIP (IMT-class, RT-bonded, no valves)
 =====================================================================================================================
 SM-FL --PEEK--> [V_in 2-pos MX II] --load--> [V_sel 6-pos rotary] --+--> tee T1 --100 um ID, 0.3 m--> P_in (40x40 um)
                        '--park--> bypass waste      ^ ports:         |       ^                              |
 S2 syringe (A1) ------------------------------------| A1             |   [P_Bin] pinch, C-Flex <-- particle   v
 conjugate 1 nM (pack, 4-8 C) -----------------------| conjugate      |      slurry (pack, stirred)    N1 bed inlet
 HQDP 1 mM -> GUARD CELL (>=300 uL/min) -> 30 uL coil| HQDP           |   [P_Bout] pinch, C-Flex --> waste     |
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
            '<-- S3 syringe: HQDP, untreated (IDA back-fill and 0.5 uL/min counter-flow; displaced before the read)
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
| 26.0 → 26.5 | (parallel) guard cell fills the 30 µL HQDP coil: 90 µL at ≥ 300 µL/min, excess → waste (§C3.1) | 300 µL/min, 18 s | dock coil valve | guard cell on |
| 27.0 → 28.0 | Substrate fill of the bed from the coil, 20 µL → V_W; counter-flow stops at 27.5; generator conditioning of the IDA fill 27.5 → 28.0 (background record; **no impurity credit**, the fill is displaced by the transfer) | 20 µL/min | V_sel HQDP; V_O closed at 27.5 | gen +0.35 V, 30 s |
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
channel; C′ adds the explicit 15-s transfer push (unmodelled; slight product dispersion, direction worse). Note
(docs/15 W9): pushing 60 nL from a 40 nL bed void through a 1 nL guard into a 15 nL channel leaves at most ≈ 15/40 of
the product **moles** in the IDA; the read is a concentration read, so this is LOD-neutral (specific and NSB product
alike) and costs ULOQ/signal only, and every acceptance on the transfer is stated as concentration (C′-R5).

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
| HQDP 1 mM | 90 (guard-cell coil fill, includes the 20 µL bed fill and the 0.06 µL push) + 4.3 (counter-flow) + 12 (IDA back-fill path) ≈ 106 µL | 1.4 mL → 2 mL vial | guard-cell treatment per run (credit UNVERIFIED, §C3.1; revised after review, docs/15 S8/W9) |
| Strip reagent | 40 µL | 0.5 mL | glycine-HCl pH 2 (stable); R2: GuHCl/NaOH "use within 2 days" (CAP_IFU) |
| A1 (dock S2) | ≈ 50 µL + back-flush 5 µL | 0.7 mL | dock bottle |
| BSM A1 | 200 µL load | – | Waters bottle |

All pack reagents are dock-supplied, which the user accepted on 2026-11-12; sample vials still contain sample only
(docs/00). A cleaning cycle triggered by the carry-over rule (§C3.8) consumes one extra bed, ≈ 80 µL strip reagent and
one blank determination's reagents; the "+ 1 recovery" in the per-day column covers one trigger per day.

### C3.7 Nearest-model performance estimate

*(Revised after review, docs/15 S8, S9, S10: all runs below were redone on a fresh scratchpad copy; the headline
carries no pre-electrolysis credit; the residual-analyte table adds the carry-over to the default contamination term.)*

**Method** as docs/12 §8 / Appendix A, on a copy in the scratchpad (nothing written in the repository); n = 2000,
seed 20261111; ΔP < 0.05 not decision-grade (docs/08 W7). Base: `C-bed-IDA` FRC optimum with docs/12's C2 overrides
(side outlet: `ma.nsb.surface_factor_chip` 0.01; non-fouling electrode class). **C′ representation**: renewal block
`hw.timing.regeneration_and_reequilibration` 7.0 min (pack 3 + flush-out 1 + strip 2 + re-equilibration 1); fresh
capture layer `chem.regeneration.activity_loss_per_cycle` 0; residual label after the strip
`chem.regeneration.residual_label_carryover_fraction` 10⁻⁴ (10⁻⁶–10⁻³, with the model's ALP inactivation).
**C′0 = headline, no pre-electrolysis credit.** Credit scenario (§C3.1, **UNVERIFIED**, pending E1.2b and a guard-cell
flow test): `ma.chemistries.alp_hqdp.free_product_impurity` × 0.05 (value 5×10⁻⁷, bounds 5×10⁻⁹–5×10⁻⁵; a pinned
scenario value such as S4a's 10⁻³ is multiplied by 0.05). Residual **analyte** carry-over is not a model term
(docs/12 §5.8); it is represented through the blank-contamination term `ma.nsb.blank_igg_contamination_equivalent`,
**added** to that term's default (value 0, sampled triangular 0–3 fM, `params/model_assumptions.yaml`) — see the
residual-analyte paragraph below for how.

| Run (nearest-model estimate) | Nominal LOD | Median [5–95 %] (pg/mL) | P(success) | P(LOD ≤ 1) | ULOQ | Model time (min) |
|---|---|---|---|---|---|---|
| REF docs/12 C2 (reproduced) | 0.64 | 2.4 [0.48–25] | 0.16 | 0.21 | 1040 | 45.0 |
| **C′0** fresh bed per run, dock valves, **no credit (headline)** | 0.64 | **2.4 [0.50–26]** | **0.15** | 0.20 | 1040 | 45.5 |
| C′0 + L6 + L7 (U1–U3 screening) | 0.53 | **1.8 [0.42–21]** | **0.21** (ULOQ 794 flagged) | 0.27 | 794 | 45.5 |
| C′0, accumulation 15 min, 3 mM HQDP | 0.62 | 2.3 [0.47–27] | 0.17 | 0.21 | 1360 | 53.0 |
| C′0 under S4a (free HQ 10⁻³) | 3.3 | 8.6 [1.3–64] | 0.015 | 0.03 | 1040 | 45.5 |
| C′0, bed-packing CV → blank CV 0.14 (0.05–0.25), scenario | 0.86 | 3.0 [0.57–36] | 0.12 | 0.16 | 1040 | 45.5 |
| *Credit scenario (UNVERIFIED):* C′0 + guard-cell credit ×0.05 | 0.64 | 2.1 [0.47–23] | 0.16 | 0.22 | 1040 | 45.5 |
| *Credit scenario:* + L6 + L7 | 0.53 | 1.8 [0.42–21] | 0.21 | 0.27 | 794 | 45.5 |
| *Credit scenario:* accumulation 15 min, 3 mM | 0.62 | 2.0 [0.43–23] | 0.19 | 0.23 | 1360 | 53.0 |
| *Credit scenario:* under S4a (×0.05 → 5×10⁻⁵) | 0.66 | 2.4 [0.51–26] | 0.14 | 0.19 | 1040 | 45.5 |
| *Credit scenario:* under S4a at ×0.1 (coil re-growth at the acceptance-limit k_h) | 0.71 | 2.7 [0.60–28] | 0.12 | 0.17 | 1040 | 45.5 |
| *Credit scenario:* blank CV 0.14 | 0.86 | 2.8 [0.55–31] | 0.13 | 0.17 | 1040 | 45.5 |
| Superseded first version "C′1" (credit ×0.01, unsupported; reproduced) | 0.64 | 2.1 [0.46–23] | 0.165 | 0.22 | 1040 | 45.5 |

Reading: the credit is worth ≈ +0.01 in P at nominal (0.15 → 0.16, ×0.01 and ×0.05 alike) and nothing after
screening (0.21 either way); it matters only under S4a, where without it C′ fails (P 0.015) and with it keeps
0.12–0.14. **Without credit C′ as specified equals gen-1 (P 0.16) and has no LOD case.**

**Packed-bed NSB-factor sensitivity** (`ma.nsb.surface_factor_packed_bed` pinned; nominal 3, range 1–30, UNVERIFIED):

| Factor | Nominal LOD | No credit: median [5–95 %] / P / P(LOD ≤ 1) | Credit ×0.05 (UNVERIFIED): median / P / P(LOD ≤ 1) |
|---|---|---|---|
| 1 | 0.27 | 1.0 [0.29–6.9] / **0.39** / 0.48 | 0.96 [0.27–5.4] / 0.43 / 0.53 |
| 2 | 0.45 | 1.3 [0.37–11] / **0.27** / 0.35 | 1.2 [0.35–9] / 0.30 / 0.38 |
| 3 | 0.64 | 1.7 [0.44–14] / 0.21 / 0.27 | 1.6 [0.42–12] / 0.23 / 0.30 |
| 5 | 1.0 | 2.5 [0.57–21] / 0.13 / 0.18 | – |
| 10 | 2.0 | 4.6 [0.85–40] / 0.05 / 0.08 | – |
| 30 | 6.0 | 13 [1.9–120] / 0.01 / 0.02 | – |

The G1 GO threshold (P ≥ 0.30, docs/06 §4.11) is reached by C′ without credit only at a packed-bed factor ≲ 1.7
(linear interpolation between the ×1 and ×2 runs, Derived), with the credit at ≤ 2. Pinning the factor at 3 gives
P 0.21 against 0.15 when it is sampled over 1–30: the uncertainty itself costs 0.06.

**Residual-analyte carry-over** (r = fraction of the previous sample's analyte that survives renewal; previous
sample C_prev). *How it is represented (corrected after review, docs/15 S9):* the first version pinned
`ma.nsb.blank_igg_contamination_equivalent` at r × C_prev, which **deleted** the model's default environmental
contamination term (sampled 0–3 fM ≈ 0–0.45 pg/mL) and so raised P to 0.24 in every row; the "artefact" explanation
given then was wrong. Here the carry-over is added to that term: contamination = r × C_prev + triangular(0, 0, 3 fM).
docs/15 did this with `with_bounds(value = low = r·C, high = 3 fM + r·C)`; because the model samples a range with
low > 0 and high/low ≥ 3 log-triangularly (`src/elisa_sim/params.py`, `sample_param`), that version concentrates draws
near r·C and under-weights the default term (its r = 10⁻⁵ row gives P 0.20, above the no-carry-over 0.15). The table
therefore samples the term linearly (r × C_prev + triangular(0, 0, 3 fM)) by a sampler patch in the scratch process
only (`src/` untouched; same random-number consumption, so all other draws are identical). docs/15's numbers were
reproduced with its method (credit ×0.01: r = 10⁻⁴ → P 0.152, r = 3×10⁻⁴ → 0.006) and are shown for traceability.

| r | C_prev 1000 pg/mL: nominal LOD / median / P | C_prev 100 pg/mL: nominal / median / P |
|---|---|---|
| 0 (C′0) | 0.64 / 2.4 / 0.15 | 0.64 / 2.4 / 0.15 |
| 1×10⁻⁵ | 0.64 / 2.4 / 0.15 | 0.64 / 2.4 / 0.15 |
| 3×10⁻⁵ | 0.64 / 2.4 / 0.14 | – |
| 1×10⁻⁴ | 0.70 / 2.5 / **0.10** | 0.64 / 2.4 / 0.15 |
| 3×10⁻⁴ | 1.1 / 2.7 / **0.006** | 0.64 / 2.4 / 0.14 |
| 1×10⁻³ | 3.1 / 4.3 / 0.00 | 0.70 / 2.5 / 0.10 |
| 1×10⁻² | 30 / 31 / 0.00 | 3.1 / 4.3 / 0.00 |
| 8×10⁻² (illustrative only: complement of Sun2008's hapten-system recovery; no IgG residual measured) | 260 / 240 / 0.00 | 24 / 25 / 0.00 |
| *docs/15 method, credit ×0.01:* 1×10⁻⁴ / 3×10⁻⁴ | 0.70 / 2.2 / 0.152; 1.1 / 2.5 / 0.006 (reproduced) | – |

Further rows at C_prev 1000, r = 10⁻⁴: with credit ×0.05 P 0.11 (3×10⁻⁴: 0.006); after L6 + L7 P 0.15 (vs 0.21
without carry-over); at packed-bed factor 2 P 0.18 (vs 0.27).

**Conclusions (rewritten after review).** (1) After a top-of-range (1000 pg/mL) predecessor, r = 10⁻⁴ — exactly the
criterion — already costs ≈ 0.05 in P (one third of C′'s P), and r = 3×10⁻⁴ removes success almost entirely (the
contamination floor r × C_prev = 0.3 pg/mL pushes the 5th-percentile LOD above 1 pg/mL); 10⁻³ fails and the
illustrative 8×10⁻² is two to three orders of magnitude out. The 10⁻⁴ requirement is therefore not conservative for
C′; it is the edge. (2) After a ≤ 100 pg/mL predecessor, r ≤ 3×10⁻⁴ costs ≤ 0.01 and 10⁻³ costs 0.05. (3) Under the
user's rule (cleaning cycle + blank check after any result > 100 pg/mL, §C3.8) a real sample never follows a
predecessor above 100 pg/mL, so case (2) is what samples see: the rule makes C′'s LOD tolerant of r up to ≈ 3×10⁻⁴.
It does not relax the kept 1×10⁻⁴ end-to-end criterion (C′-R1(c)), which remains a hard condition. (4) The routine
blank check cannot itself verify 10⁻⁴: after a 1000 pg/mL result it would read 0.1 pg/mL, below C′'s nominal LOD
(0.64 pg/mL); it detects only r ≳ LOD/C_prev ≈ 6×10⁻⁴ (Derived) and is a gross-failure check, not a measurement.

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
| 1 | SM-FL needle and loop | protein film | `hw.smfl.carryover_protein_conjugate` 10⁻⁴ (10⁻⁵–10⁻³), UNVERIFIED — common to A, B, C′ | 3×10⁻⁵ (needs a needle wash ≥ 3× better than the nominal 10⁻⁴, which alone would use the whole budget, docs/15 S11; measured on gen-1, Stage 2) |
| 2 | V_in, V_sel rotor, inlet line, T1, P_in | sample film on dock-side wetted path | unquantified; every cycle passes 40 µL strip + 25 µL A1 through the same path (§C3.4) | 2×10⁻⁵ |
| 3 | Residual particles after flush-out × analyte surviving the strip on them | r_b × s | r_b UNVERIFIED (no number in Grate2009, Fu2011, Pollema1994 abstracts); s unmeasured (s is exactly the R0 regeneration residual φ; 0.08 is used only as an illustrative order of magnitude from Sun2008's hapten-system recovery, docs/15 W10) | 3×10⁻⁵: e.g. r_b ≤ 10⁻³ **and** s ≤ 3×10⁻², or r_b ≤ 3.75×10⁻⁴ at s = 0.08 |
| 4 | Active label on residual particles | r_b × (1 − ALP inactivation) | inactivation by pH ~2: 1 (0.5–1), UNVERIFIED (`chem.enzymes.alp.inactivation_by_low_pH_regeneration`); at 0.5 and r_b = 10⁻³ it would be 5×10⁻⁴ → the strip must kill ALP (≥ 0.99) or include NaOH/GuHCl | 1×10⁻⁵ |
| 5 | Analyte on cavity walls, weir, guard mouth | adsorption surviving the strip | unquantified (glass, ≈ 2.2 mm², docs/12 §5.8) | 1×10⁻⁵ |
| | **Total** | | | **1.0×10⁻⁴** |

Compared with docs/12 C (one regeneration path with no measured residual and no means of reduction), C′ converts
carry-over into **five paths, each with an independent removal mechanism and a separate measurement**: r_b by particle
count (115 particles = 10⁻³), s by the R0 arm, 4 by an IDA read of the stripped cavity, 1–2 by the gen-1 Stage-2 SM-FL
test, and the sum by the challenge → blanks (C′-R1(c)). If the Stage-2 SM-FL measurement comes back at its nominal
10⁻⁴ (UNVERIFIED), the end-to-end criterion fails for every candidate (A, B, C′) regardless of the chip (docs/15 S11).

**Carry-over rule (user decision 2026-11-12) and the repack cycle.** The 1×10⁻⁴ criterion above is kept, and after
any result > 100 pg/mL a **mandatory cleaning cycle and blank check** follow before the next sample. In C′ every run
already renews the bed and strips the empty cavity, so the cleaning cycle is the F17 recovery sequence run once more
on top of the normal post-read block: an extra flush-out, a **double strip** of the empty cavity, T1, P_in and the
V_sel common path (glycine pH 2; R2: GuHCl/NaOH), A1 re-equilibration (≈ 9 min), then a **fresh bed** packed for the
blank check, which is a full determination (45.5 min) of a blank from the autosampler's QC blank vials. Effects:
(i) paths 3 and 4 (residual particles) get a second flush-out and a second bed, so their contribution to the sample
after the blank is ≈ squared; paths 2 and 5 get the second strip; path 1 (SM-FL) is cleaned only by the needle wash
and the blank injection itself. (ii) Because the next real sample always follows a predecessor ≤ 100 pg/mL, the
model cost of r ≤ 3×10⁻⁴ is ≤ 0.01 in P (§C3.7), against 0.05–0.15 without the rule. (iii) Cost: one bed, ≈ 80 µL
strip reagent and ≈ 55 min of instrument time per trigger; at one trigger per pack day the day holds ≈ 9 instead of
10 samples. (iv) The blank check is a gross-failure check (it resolves only r ≳ 6×10⁻⁴ after a 1000 pg/mL result,
§C3.7), not a substitute for the C′-R1(c) measurement.

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
| C′-R1 | carry-over > 10⁻⁴ (residual particles, strip survival, walls) | **Mock-up**: 0.1 µL cavity with 5 µm weir in a milled COC (or Micronit-class glass) channel, dock pinch/solenoid valves, catalogue Micrux IDA6 die downstream. (a) 20 pack/flush-out cycles with fluorescent 10 µm SA particles, count residual particles; (b) **R0 arm**: same cavity, particles left in place, 10 ng/mL human IgG, strip, re-label, read → s (= φ); (c) end-to-end: **100 ng/mL** challenge → 3 blanks through the low-range slope (docs/06 E2.7 / E3.4 criterion), or the 10 ng/mL challenge with n ≥ 10 challenge–blank pairs and a stated power — at 10 ng/mL, 10⁻⁴ is 1 pg/mL, which a single triplet cannot resolve from 0 at a bench LOD of 1–1.5 pg/mL (docs/15 W4); the challenge above the ULOQ does not matter for the following blank | (a) r_b ≤ 10⁻³ (≤ 115 particles) in 20/20; (b) s ≤ 3×10⁻²; (c) **≤ 1×10⁻⁴** |
| C′-R2 | packed-bed NSB factor ≥ 3 | U4-type conjugate exposure series (0.3–3 nM × 2–30 min) on 0.1 µL beds of 10 µm SA particles vs M-280 beads (docs/12 B1/C3) — **shared with B** | factor ≤ 2 (P 0.27 without credit, 0.30 with; GO-level P ≥ 0.30 without credit needs ≲ 1.7, §C3.7) |
| C′-R3 | bed packing not reproducible | 20 repacks: Δp, particle count, blank and 10 pg/mL | blank CV ≤ 12 % (P 0.12 at 0.14 without credit, §C3.7) |
| C′-R4 | IDA contaminated without Vi (conjugate, acid) | dead-end + counter-flow test: fluorescent conjugate and pH indicator at the guard end, 50 cycles; IDA HQ response before/after | conjugate at IDA ≤ 10⁻⁴ of c₀; IDA HQ slope drift ≤ 2 % over 50 strips |
| C′-R5 | stopped IDA read / transfer push not as assumed | E3.1-type (docs/06) on IDA6 in a 25 µm channel with the 60 nL transfer | product **concentration** in the IDA ≥ 0.8 × the bed-void concentration before the push (as moles ≤ 15/40 is geometric, docs/15 W9); gain ≥ 4 |
| C′-R6 | guard-cell credit not real (needed only for the S4a protection) | E1.2b (docs/06, chemical floor) plus a flow test of the guard cell at ≥ 300 µL/min into the 30 µL coil: spiked HQ 10⁻⁴–10⁻³ before/after, and re-growth over 10 min | escape ≤ 0.05 (the scenario's ×0.05); otherwise C′ is quoted without credit only |

### C3.11 Is revised C viable?

*(Verdict revised after review, docs/15 S8–S10.)* **Buildable in principle, with conditions — but without the
pre-electrolysis credit it has no LOD case as specified.** Neither of docs/12's two blocking problems survives the
redesign as an *unanswerable* question: valve endurance is removed (no on-chip valve; every dock valve ≥ 7× its rated
life), and regeneration carry-over is replaced by a renewal scheme whose carry-over is a product of separately
measurable factors with a 10⁻⁴ budget. What the review changed: the headline is P 0.15 (C′0), equal to gen-1 (0.16);
the credit was unsupported as designed and, re-derived (×0.05, per-run guard-cell coil), is worth only ≈ +0.01 at
nominal; and residual analyte at the criterion itself (r = 10⁻⁴ after a 1000 pg/mL predecessor) already costs
≈ 0.05 in P. The user's cleaning rule removes that cost for real samples (§C3.8) at ≈ 55 min per trigger. The
conditions are three bench results on a mock-up costing no glass, plus one for the credit:

1. **C′-R1(c): end-to-end carry-over ≤ 1×10⁻⁴** (100 ng/mL challenge or ≥ 10 pairs; r_b ≤ 10⁻³ and s ≤ 3×10⁻² as
   intermediate gates). If it fails, C′ is not viable.
2. **C′-R2: packed-bed NSB factor ≤ 2** (≲ 1.7 for P ≥ 0.30 without credit). At the nominal 3 C′ is no better than
   gen-1 (P 0.15 vs 0.16); the factor decides whether C′ has any LOD case at all.
3. **C′-R3: blank CV ≤ 12 % over 20 repacks.**
4. (only for S4a protection) **C′-R6 / E1.2b**: guard-cell escape ≤ 0.05 at ≥ 300 µL/min.

What C′ cannot change: it keeps in-flow sequential labelling (label fraction 0.5 %, docs/12 §5.9), so it gains
little from reagent screening (C′0 + L6 + L7: P 0.21, with or without credit, vs 0.37 for A + L6 + L7 as quoted for
docs/13 by docs/15 §3 — read the final A value from docs/13 Revision B / docs/16), and its throughput is one sample
per 45.5 min (no staggering with one bed; a second lane needs two more potentiostat channels), less ≈ 55 min per
carry-over trigger. Its advantages are the shortest time to result (37.5 min), the lowest consumable cost and no
per-run consumable solid other than ≈ 10⁵ particles.

---

# PART B — fallback dossier: indexed single-use capture-and-read cells

Concept, block diagram, step table (result 50.0 min, ≈ 26 min per sample with two heads), F1–F20 table and model
mapping are in docs/12 §4 and are not repeated. This part tightens the five items that decide whether B can be built
and calibrated.

## B0. Changes to docs/12 §4 after review (docs/15) and the user decisions of 2026-11-12

* **Substrate path and pre-electrolysis credit (docs/15 S8).** docs/12 §4 fills a **1 mL holding loop** through the
  dock guard cell and uses it for up to ≈ 22 runs (≈ 9.5 h); at the acceptance-limit k_h (10⁻⁹ s⁻¹) HQ re-grows in
  the loop to ≈ 3×10⁻⁵ mol/mol (1×10⁻⁹ × 34 200 s, Derived) — three times the nominal lot impurity — before it is
  used, and the guard cell (`hw.flow_cells.thermo_6011rs_coulometric`: collection 0.95, minimum flow 300 µL/min;
  repository values, vendor document not re-read, UNVERIFIED) leaves 5 % even when fed correctly. The ×0.01 credit of
  docs/12 "B1" is therefore unsupported. **Replaced by**: two per-cell coil fills from the guard cell at ≥ 300 µL/min
  (one just before the RC fill at −3.0, one just before the bed fill at 33.0; ≈ 60 µL each, excess to waste), so no
  treated substrate ages more than minutes. What is electrolysed in place: the 2 µL RC fill by PE1 (escape set by the
  RC's ports and pinch points, unmeasured; docs/15 S1 found ≈ 1–11 % for a comparable RC). What is not: the 0.6 µL
  pushed in at the transfer (bed void + push substrate, guard-cell treated only), i.e. 30 % of the read volume.
  Effective impurity ≈ 0.7 × (0.01–0.1) + 0.3 × 0.05 ≈ ×0.02–0.09 (Derived) → represented as **×0.05, a scenario,
  UNVERIFIED** until E1.2b (docs/06) and a guard-cell flow test. **Headline numbers carry no credit (B0).** The model
  shows B is insensitive to the factor at nominal (P 0.153 / 0.167 / 0.172 / 0.174 / 0.174 at ×1 / 0.3 / 0.1 / 0.05 /
  0.01) and sensitive only under S4a (P 0.007 without, 0.13 at ×0.05, 0.10 at ×0.1).
* **Sample transfer (docs/15 W8).** B transfers 1.5 loop volumes (0.90 of the analyte) by design, below the docs/09
  F1 requirement "capture ≥ 96 % of the injected analyte". The trade (less dilution in W1, docs/12 §2.2) is kept and
  recorded here as a **change of requirement F1 for B**, to be confirmed by the user with the cartridge decision.
* **Dock-supplied reagents (user decision 2026-11-12: accepted).** B's capture phase stays in the cell (the bed is
  the cell's identity). The decision opens an option not adopted here [assessment]: deliver the conjugate as liquid
  from a cooled dock vial through head port c (as C′ does) instead of a dried spot in W3. It would remove the
  dried-conjugate arm of B-E3 and the rehydration dose-CV problem (§B3), at the cost of a conjugate line and its
  8-h in-use life (docs/07 §5.5) in the dock; it does not change the model numbers (conjugate dose and stop time are
  the same). To be decided with the user if B is ever activated.
* **Carry-over rule (user decision 2026-11-12: 1×10⁻⁴ criterion kept + mandatory cleaning cycle and blank check
  after any result > 100 pg/mL).** **Nothing changes in B's design**: capture surface, conjugate, RC and electrode
  are new for every determination, so the only paths the cleaning cycle acts on are the SM-FL needle/loop and the
  head bore/dock selector, which B flushes after every cell anyway. Operationally a trigger consumes one cell (the
  blank check, 1/16 card) and one head slot (≈ 26 min of cadence).

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
√(0.10² + 0.10²) = 0.141 at 10 % (blank CV `chem.nsb.blank_CV_analog_electrochemical` 0.10). Model: B0 at blank CV
0.14 (0.05–0.25) gives median 3.0 pg/mL, P 0.12 vs 2.3 / 0.15 (with the ×0.05 credit scenario 2.7 / 0.13 vs
2.1 / 0.17; §B6; revised after review, docs/15 S8/S10). **Requirement: delivered conjugate dose CV
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

*(Revised after review, docs/15 S8/S10: re-run on a fresh scratchpad copy; B0 = no credit is the headline; the
credit is the re-derived ×0.05 scenario of §B0, UNVERIFIED. docs/12's "B1" used ×0.01; at nominal both give P 0.174.)*

| Run (nearest-model estimate) | Nominal | Median [5–95 %] | P(success) | P(LOD ≤ 1) | ULOQ | Model time |
|---|---|---|---|---|---|---|
| **B0** no credit (reproduces docs/12) — **headline** | 0.63 | **2.3 [0.52–23]** | **0.15** | 0.20 | 1360 | 52.0 |
| B0 + L6 + L7 (U1–U3 screening) | 0.51 | **1.8 [0.45–17]** | **0.20** | 0.26 | 1040 | 52.0 |
| B0, packed-bed factor 1 | 0.30 | 1.2 [0.30–6.9] | **0.33** | 0.42 | 1360 | 52.0 |
| B0, packed-bed factor 2 | 0.46 | 1.4 [0.39–9.6] | **0.25** | 0.32 | 1360 | 52.0 |
| B0, packed-bed factor 3 | 0.63 | 1.8 [0.47–13] | 0.20 | 0.26 | 1360 | 52.0 |
| B0, packed-bed factor 10 | 2.0 | 4.3 [0.83–37] | 0.06 | 0.08 | 1360 | 52.0 |
| B0, blank CV 0.14 (dose / cell CV scenario) | 0.85 | 3.0 [0.60–30] | 0.12 | 0.16 | 1360 | 52.0 |
| B0 under S4a (free HQ 10⁻³) | 4.7 | 10 [1.6–88] | 0.007 | 0.01 | 1360 | 52.0 |
| *Credit scenario ×0.05 (UNVERIFIED)* | 0.63 | 2.1 [0.50–21] | 0.17 | 0.22 | 1360 | 52.0 |
| *Credit scenario* + L6 + L7 | 0.51 | 1.8 [0.45–17] | 0.20 | 0.26 | 1040 | 52.0 |
| *Credit scenario*, packed-bed factor 1 / 2 / 3 / 10 | 0.30 / 0.45 / 0.63 / 2.0 | 1.0 / 1.3 / 1.6 / 4.1 | 0.38 / 0.28 / 0.22 / 0.06 | 0.47 / 0.36 / 0.28 / 0.09 | 1360 | 52.0 |
| *Credit scenario*, blank CV 0.14 | 0.85 | 2.7 [0.56–28] | 0.13 | 0.17 | 1360 | 52.0 |
| *Credit scenario* under S4a (×0.05 / ×0.1) | 0.67 / 0.78 | 2.4 / 2.9 | 0.13 / 0.10 | 0.18 / 0.14 | 1360 | 52.0 |
| Superseded docs/12 "B1" (credit ×0.01; reproduced) | 0.63 | 2.1 [0.49–21] | 0.174 | 0.22 | 1360 | 52.0 |

The G1 GO threshold (P ≥ 0.30) is reached by B without credit only at a packed-bed factor ≲ 1.4 (linear
interpolation between the ×1 and ×2 runs, Derived); with the credit at ≲ 1.8.

## B7. What would trigger switching from A to B

Switch to B when **one A-side failure** and **both B-side conditions** hold:

* **A-side (any one)**: (i) residual beads in the readout or incubation chamber > 1×10⁻⁴ of the dose that rinse/
  flush redesign cannot fix (A1 mock-up, or PE2 in operation showing persistent residual activity); (ii) chamber
  mixing factor near the 0.2 lower bound (A2), i.e. capture too slow for 30 min; (iii) on-card bead dose CV > 5 %
  over 8 h (A3); (iv) membrane valves or gates fail below 3× life (≈ 210 cycles, A4) **and** the dock-side valve
  approach of §C2 cannot be transferred to A (§C2 shows the endurance problem is solvable off-chip, so (iv) alone
  should not trigger B).
* **B-side (both)**: packed-bed NSB factor ≤ 2 (B-E1: P 0.25–0.33 at ×2–×1 without credit, 0.28–0.38 with; §B6) and cell-to-cell blank CV ≤ 10 %
  (B-E2).
* Independently of A's risks: if the user or a later regulatory context demands **carry-over zero by construction**,
  B is the only candidate that provides it.

## B8. The three bench experiments that decide B

| # | Experiment | Measures | Pass |
|---|---|---|---|
| **B-E1** (= C′-R2, one experiment for both) | U4-type conjugate exposure series (0.3–3 nM × 2–30 min) on 0.5 µL beds of 50 µm SA particles (and 0.1 µL of 10 µm for C′) vs blocked M-280 beads in tubes | packed-bed NSB factor (`ma.nsb.surface_factor_packed_bed`) as enzymes per mm² per nM·min relative to M-280 | **≤ 2** (P ≥ 0.25 without credit; GO-level 0.30 needs ≲ 1.4 for B, ≲ 1.7 for C′) |
| **B-E2** | 20 hand-packed cells from one batch on a milled 4-cell card with catalogue Micrux single electrodes; blanks and 10 pg/mL | bed mass CV, blank CV, slope CV, WE-to-WE background charge | blank CV **≤ 10 %**, slope CV ≤ 10 % |
| **B-E3** | dried capture (on-particle) and dried conjugate: reconstitution with/without pulse mixing; ageing 0–8 weeks at 4/25/37 °C with humidity control (Ford1994 risk); 8 h open on the dock after piercing | delivered dose CV, activity and NSB vs wet reagents | dose CV **≤ 5 %**; activity ≥ 80 % and NSB ≤ 1.2× wet after 8 weeks at 4 °C + 8 h open |

docs/12 risks B4 (recirculating capture rate) and B5 (exhaustive read on a shared strip) follow if B-E1–E3 pass.

---

# F. Updated three-way comparison

*(Revised after review, docs/15 S8/S10.)* B, C and C′ numbers are from §B6, docs/12 §5.9/§8 and §C3.7; all are
nearest-model estimates (n = 2000, success = L_eff ≤ 1); ΔP < 0.05 is not decision-grade (docs/08 W7). Every
candidate is shown **without** pre-electrolysis credit (the headline) and **with** it (a scenario, UNVERIFIED until
E1.2b, docs/06). **The A column must be read from docs/13 Revision B, to be finalised by the decision document
docs/16 — not from docs/12.** The A values below are only an interim orientation: docs/13 (3 mM HQDP, 1 µL RC) as
reproduced by docs/15 §3, before the Revision-B corrections. Gen-1 primary reference: 3.5 [0.51–157] / P 0.16 as
specified, 1.3 / 0.32 after L6 + L7 (docs/08 §10.1).

| | **A** bead-transfer multi-run (**read docs/13 Rev B / docs/16**; interim values) | **B** single-use cells (fallback) | **C** as in docs/12 (superseded by C′) | **C′** revised permanent chip (this document) |
|---|---|---|---|---|
| Capture renewal | beads per run (liquid) | fresh factory cell per run | glycine regeneration of a covalent bed | **fresh particle bed packed per run + strip of the empty cavity** |
| Labelling / detector | one-step chamber; single WE, stopped step read | sequential in flow; single WE per cell, exhaustive | sequential in flow; stopped IDA, 2 channels | same as C |
| Median [5–95 %] / P as specified, **no credit** | 2.45 [0.43–81] / 0.20 (docs/15 §3) | **2.3 [0.52–23] / 0.15** | 2.4 [0.48–25] / 0.16 | **2.4 [0.50–26] / 0.15** |
| Same, **with credit** (scenario, UNVERIFIED) | 1.88 / 0.26 (×0.01 in the RC, step-read mode only; real RC escape 1–11 %, docs/15 S1) | 2.1 / 0.17 (×0.05, §B0) | 2.2 / 0.18 (docs/12 ×0.01; guard cell below its minimum flow — unsupported) | 2.1 / 0.16 (×0.05, §C3.1) |
| After U1–U3 screening (L6 + L7), no credit / with credit | 1.12 / 0.37 either way (docs/15 §3) | 1.8 / 0.20 either way | 1.9 / 0.20 (no credit; with credit not run) | 1.8 / 0.21 either way |
| Under S4a (free HQ 10⁻³): P no credit / with credit | 0.001 / 0.22 at ×0.01 (0.16 at ×0.04, 0.09 at ×0.11; docs/15 §3) | 0.007 / 0.13 | not run | 0.015 / 0.14 |
| Packed-bed NSB factor ×1 / ×2 / ×10 (P, no credit) | not applicable (beads) | 0.33 / 0.25 / 0.06 | 0.06 at ×10 (docs/12) | **0.39 / 0.27 / 0.05** |
| Inject Start → result | ≈ 58.9 min (docs/13 58.0 re-timed by docs/15 S4) | 50.0 min | 37.5 min | **37.5 min** |
| Throughput | ≈ 31 min/sample (2 chambers, docs/13) | ≈ 26 min/sample (2 heads) | 45 min | 45.5 min (+ ≈ 55 min per carry-over trigger) |
| Carry-over vs 10⁻⁴ (criterion kept + cleaning cycle and blank check after any result > 100 pg/mL, user 2026-11-12) | residual beads, measured every run (PE2); budget not yet allocated (docs/15 S5, S6, S11) | **0 by construction** except SM-FL and head bore; the rule changes nothing in the design | no residual measured (one 92 % elution recovery in a hapten system, Sun2008); not viable | product of 5 measurable paths, budget 10⁻⁴ (§C3.8), unproven; at r = 10⁻⁴ after 1000 pg/mL P 0.15 → 0.10; with the rule ≤ 0.01 for r ≤ 3×10⁻⁴ |
| Valves on the consumable / chip | 20 (docs/13; layer stack under redesign, docs/15 A1) | 80 pinch points per card, ≤ 3 each | 6; busiest ≈ 1200 (24×) | **0 on chip**; dock valves ≥ 7× margin on rated life (pinch-valve pressure rating to be checked) |
| Electrode consumed per determination | 1/16 die | 1/8 strip (one WE) | ≤ 1/300 IDA die | ≤ 1/300 IDA die |
| Consumable cost class [assessment] | medium | high | low | low |
| Dock complexity [assessment] | high | highest | medium | medium–high (selector, 2 solenoids, 2 pinch, 2–3 syringes, guard cell + coil, stirred slurry vial, 2-channel potentiostat) |
| Recalibration | lot + QC per card (per-chamber blanks, docs/15 W7) | lot + 3 QC per 16 | every ≈ 20 runs (capacity drift) | 2 blanks + 1 control per day (fresh capture each run) |
| Evidence strength | medium | strongest format precedent (Gyrolab, Ella, i-STAT) | weakest | medium-low: renewable-surface sandwich in flow (Grate2009), microfabricated trap/release (Fu2011); no residual-bead number found |
| Decisive bench result | per docs/13 Rev B (M1 residual beads, M5a step read) | B-E1 bed factor, B-E2 cell CV, B-E3 dried reagents | carry-over (no residual measured) | C′-R1 carry-over ≤ 10⁻⁴, C′-R2 bed factor ≤ 2, C′-R3 repack CV; C′-R6/E1.2b for the credit |
| Verdict | **leading concept, not yet a buildable design** (docs/15 §5) | **fallback** | **not viable** | **viable with conditions; no LOD case without credit** |

## F1. What would have to be true for B or C′ to be preferred over A

**For B over A**: the packed-bed NSB factor ≤ 2 (B-E1) **and** cell-to-cell blank CV ≤ 10 % and dried-reagent dose
CV ≤ 5 % (B-E2, B-E3) **and** at least one of A's own risks fails (residual beads > 10⁻⁴, mixing factor near 0.2, or
bead dose CV > 5 %). B alone also wins if carry-over must be zero by construction. Even then B's LOD case after reagent
screening (P 0.20, with or without credit) is weaker than A's (0.37 as quoted for docs/13 by docs/15; final value in
docs/13 Rev B / docs/16), because sequential in-flow labelling labels ≈ 1.7 % of the captured analyte; B wins on
robustness, not sensitivity.

**For C′ over A**: everything B needs on the bed factor (≤ 2, shared experiment) **plus** end-to-end carry-over
≤ 1×10⁻⁴ on the renewable-bed mock-up (C′-R1) **plus** repack blank CV ≤ 12 % (C′-R3), **and** the user values
time to result (37.5 vs ≈ 58.9 min for A, docs/15 S4) and cost per determination (≤ 1/300 of a die) above throughput
(45.5 vs ≈ 31 min per sample, less ≈ 55 min per carry-over trigger) and above the reagent-screening upside that only
the one-step format (A) captures. If the reagent screen
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
| Anguizola2018 | doi:10.1016/j.ymeth.2018.03.013 (PMC6114083) | full text via fetch summary: k_d table, capacity over cycles (numbers not in the abstract; docs/15 could not confirm them → UNVERIFIED for decisions) |
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
| BIOCHEM_PINCH | https://cdn.shopify.com/s/files/1/0651/4779/7727/files/Pinch_Valve_Brochure_111110.pdf | text extracted: valve and tubing cycle ratings, tubing IDs (re-checked in docs/15; pressure rating not read) |
| BIOCHEM_ISO | https://flowchem.readthedocs.io/en/latest/_downloads/231c5bc79e4b696e0c0a09219608bcd0/biochem_solenoids.pdf | text extracted: isolation valve volumes, pressures, > 20 M cycles |
| LEE_LFN | https://www.theleeco.com/product/lfn-series-2-way-isolation-solenoid-valves | product page via fetch summary (re-checked in docs/15) |
| (PARKER_S1, withdrawn) | vendor page returned 403; only a search summary was seen | no part or rating is cited from it (revised after review, docs/15 N6) |

Searched with no usable hit: PubMed "protein A chromatography carryover …", "immunoaffinity … residual …", "SPR …
residual … after regeneration", "DNA-directed immobilization antibody regenerable …" (0 hits each); one WebSearch on
DNA-directed regenerable immunosensors returned no cycle numbers. Cleavable linkers (R6) were not searched.

## Appendix — model runs (scratchpad copy, not in the repository)

Revised after review (docs/15 S8, S9): headline runs carry no credit; the credit scenario uses ×0.05; residual
analyte is added to the default contamination term with linear sampling.

```python
# sys.path -> COPY/scripts, COPY/src ; same helpers as docs/12 Appendix A (L = design_lib, F = final_designs)
IMP = "ma.chemistries.alp_hqdp.free_product_impurity"; CONT = "ma.nsb.blank_igg_contamination_equivalent"
def credit(p, f):                                    # f = 1 (headline, no credit) or 0.05 (scenario)
    if f == 1: return p
    if IMP in p.pinned: return p.with_values({IMP: float(p.values[IMP]) * f})        # e.g. S4a
    return L.with_bounds(p, IMP, value=1e-5 * f, low=1e-7 * f, high=1e-3 * f)
fc = json.load(open(L.OUT / "optimum_FRC__baseline.json"))["design"]
C  = L.base_arch("FRC").with_design(**fc)
Cp = C.with_design(**{"hw.timing.regeneration_and_reequilibration": 7.0})          # C' renewal block
def Cp_ps(p):                                                                       # C2 overrides + fresh layer
    p = C_ps(p).with_values({"chem.regeneration.activity_loss_per_cycle": 0.0})
    return L.with_bounds(p, "chem.regeneration.residual_label_carryover_fraction", value=1e-4, low=1e-6, high=1e-3)
s = L.mc(Cp, credit(Cp_ps(scen(ps0)), f), n=2000)                                  # C'0 (f=1) / credit (f=0.05)
# bed factor: .with_values({"ma.nsb.surface_factor_packed_bed": b})
# residual analyte r after C_prev (pg/mL -> M: x 1e-12 / 1.5e5 x 1e3), ADDED to the default 0-3 fM term:
M = lambda c: c * 1e-12 / 1.5e5 * 1e3
p = L.with_bounds(p, CONT, value=M(r * C_prev), low=M(r * C_prev), high=3e-15 + M(r * C_prev))
# ... and sampled linearly (r*C_prev + triangular(0, 0, 3 fM)): in the scratch process only, ParameterSet.sample is
# wrapped so that CONT uses rng.triangular(low, value, high) instead of the log-triangular branch that
# elisa_sim.params.sample_param takes when low > 0 and high/low >= 3 (same rng consumption; src/ unchanged).
# B: docs/12 Appendix A B and B_ps, lod_scale 0.996/0.90, credit(f) as above, bed factor / blank-CV variants
```
