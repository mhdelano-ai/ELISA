# Review of docs/30: chemistry and bench realism (tiers 1 and 2, and the chemistry of the tier-3 transfer)

Reviewer: independent chemistry reviewer, 2026-11-17. Scope: docs/30 §1–5, with docs/26, docs/28 §1/§6, docs/29 and
`scripts/tier_round/tier_params.yaml`. My calculations are in `scripts/tier_round/review_chemistry_calc.py` (run:
`python scripts/tier_round/review_chemistry_calc.py`; every number it prints is Derived). Evidence labels: [V] = I
opened the page or full text in this session; [V-abs] = I read the PubMed abstract; [S] = search summary only;
UNVERIFIED; Derived.

## Verdict

The reagents and geometry of tiers 1 and 2 mostly exist as described: the two Jackson items, the M-280 bead count and
capacity, and the HQDP catalogue item check out on the vendor pages, and the tier-2 bed numbers are right
(1×10⁶ beads = 1.54 µL of stock, 24.6 mm², 1.4 bar at 3.5 µL/min). The chemistry of the read is the weak part. The
signal model credits two electrons per enzyme turnover at an HQ read potential. But alkaline phosphatase is a
non-processive monoesterase, so at the picomolar enzyme amounts of this assay HQDP stops almost entirely at the
monophosphate (HQMP). Unless HQMP is oxidised at the chosen potential, the signal of all three tiers is 10²–10⁵ times
lower than modelled (blocking until a one-day test settles it). Tier 1 also has three unpriced chemistry risks:
hydroquinone is an inner-sphere couple and is slowed by an alkanethiol layer; the same thiol coats the gold
pseudo-reference that carries the dominant drift term; and the 0.6 V gold-in-chloride ceiling may be reached.
Tier 2's main gaps:
* the detection conjugate is not cross-adsorbed against bovine proteins, while the bead stock comes in ordinary 0.1 %
  BSA;
* the MicruX add-on is held by magnets, a few millimetres from a bed of magnetic beads;
* the strip is reused across determinations;
* the read takes the hydroquinone half-life as 2 h, but the half-lives I found extrapolate to about 7 min at pH 9.5.

The tier-3 desthiobiotin release in 5 min has no supporting number. A release time derived from the affinity is
hours, and a Life Technologies paper calls the elution "too slow".

## Findings (most severe first)

### C1 — blocking (until tested): the enzyme product of HQDP at picomolar ALP is the monophosphate, not hydroquinone
* **Where:** docs/30 §0 and §2.2 (HQDP read "at the hydroquinone oxidation plateau"); §3.4 ("1000 turnovers per second,
  2 electrons"); §4.4 (2.3×10⁻¹⁴ mol product in 7 min); `params/model_assumptions.yaml` alp_hqdp
  (phosphate_per_product 2, n_e 2).
* **Evidence:**
  * Alkaline phosphatase hydrolyses one phosphate monoester per catalytic cycle and releases the alcohol. From HQDP
    the released alcohol is hydroquinone monophosphate (HQMP). Making HQ needs a second encounter of HQMP with an
    enzyme, in competition with 1 mM (or 0.3 mM) HQDP.
  * Derived, with Km(HQMP) taken equal to Km(HQDP) (UNVERIFIED) and the docs/30 nominal enzyme counts:
    * Tier 2: 3.9×10⁴ enzymes per pg/mL in 7.6 nL of bed pores is 8.5 pM. The pseudo-first-order HQMP→HQ rate is
      7.8×10⁻⁶ s⁻¹, so after the 7 min stop HQ/HQMP ≈ 1.6×10⁻³ (1.1×10⁻⁴ if the product spreads into 0.11 µL).
    * Tier 1: surface velocity for HQMP 5.8×10⁻¹² m/s against a mass-transfer coefficient of 1.9×10⁻⁶ m/s, so
      3×10⁻⁶ of the HQMP is re-hydrolysed before it is swept away.
  * No paper I found discusses the intermediate:
    * Wilson & Rauh 2004 [V-abs, PMID 15308232, doi:10.1016/j.bios.2004.01.013] used a dense enzyme layer on the
      electrode.
    * Bekhit2021 [V-abs via docs/29, PMID 34637277] used exhaustive coulometry.
    * The Metrohm DRP-HQDP-0.5G page [V] says only that the substrate "generates electrochemically active
      hydroquinone".
  * So either HQMP is itself oxidised at the read potential (HQMP is a para-phosphoryloxy phenol, so its potential is
    plausibly 0.1–0.3 V above HQ: UNVERIFIED), or published HQDP assays at low enzyme read something other than
    modelled.
  * The tier-1 read potential is set "0.25 V above" the wave of an HQ standard (§3.3), and the tier-2 potential
    (+0.30 V vs printed Ag/AgCl) is set from an HQ voltammogram. Neither is set on the product the enzyme actually
    makes.
* **Consequence:** if HQMP is not oxidised at +0.30 V, every signal in docs/30 §3.4, §4.4 and §5.3 is overestimated
  by 10²–10⁵. If it is oxidised but at a higher potential, the read potential moves towards the gold-in-chloride
  limit (C2) and raises the background on carbon.
* **Fix:** add a bench item before T1-1/T2-1 (half a day, no flow hardware):
  * (a) Free ALP conjugate at 1–10 pM in the substrate buffer with 1 mM HQDP for 7 min. Then take a voltammogram of
    the mixture on the printed carbon and on the thin-film gold, and compare it with an HQ standard of the expected
    concentration.
  * (b) Settle the product identity on the I-Class itself: a C18 column, UV at about 290 nm, HQDP / HQMP / HQ
    retention. HQMP as a reference standard is UNVERIFIED as a catalogue item; partial ALP hydrolysis of HQDP gives
    it.
  * Until then, carry a "product electroactivity per turnover" factor in `tier_params.yaml` with a low bound ≤ 0.01.
    Set the read potential from an enzymatically generated product, not from an HQ standard.

### C2 — significant: tier 1 assumes hydroquinone crosses a thiol monolayer and a protein layer with no penalty, and the read window on gold in chloride is narrow
* **Where:** docs/30 §3.1 (surface), §3.6 (the risk is named but not priced), §6.4.
* **Evidence:**
  * Hydroquinone/benzoquinone is a proton-coupled, inner-sphere couple. Yang's group selected ITO precisely because
    inner-sphere couples such as HQ are slow on non-catalytic surfaces [S: Akanda, Choe, Yang, Anal Chem 2012;
    ITO-pretreatment study, via search summary]. The account Akanda 2026 [V-abs, PMID 42178770,
    doi:10.1002/tcr.70177] frames substrate choice by "inner sphere-philic" behaviour.
  * For HQ tethered to gold through thiols, the peak separation rises from < 0.1 V for short linkers to 0.58 V for an
    undecyl linker [S: koreascience / Hokkaido H2QC11SH papers, via search summary].
  * The commonly sold biotin-OEG thiols are C11-alkyl based (UNVERIFIED; docs/30 gives no part number). The only
    support offered, Nishimura2011, used a short tri(ethylene glycol) thiol with p-aminophenol [V-abs in docs/29],
    not HQ, and with no streptavidin–antibody overlayer.
  * docs/28 §4 [V] limits thin-film gold in chloride to −0.3 to +0.6 V. If the HQ wave on the coated chip sits at
    +0.3–0.4 V, "0.25 V above the half-wave" reaches +0.55–0.65 V, at or past that limit. An HQMP read (C1) would push
    it further.
* **Fix:**
  * Specify a short-chain thiol system: an OEG thiol with a C2–C6 alkyl segment, or mercaptohexanol diluent with a
    biotin-PEG thiol, with the part number checked.
  * Add to T1-1 a pass criterion on the HQ wave of the coated chip: E½ ≤ +0.25 V vs the chip reference, and plateau
    current ≥ 70 % of bare gold at 1 µM.
  * Put a "monolayer collection efficiency" factor (0.1–1) in the tier-1 kit instead of leaving it in §6.4.
  * Fallback: the printed carbon strip with adsorbed streptavidin (docs/30 §3.5, 9.4 nominal) needs no monolayer.

### C3 — significant: the thiol and the protein coat cover the gold pseudo-reference that carries tier 1's largest variance term
* **Where:** docs/30 §3.2 step 2 ("The drop covers working, counter and pseudo-reference electrodes alike"); §3.4
  (drift is 63 % of the blank variance).
* **Evidence:**
  * A bare-gold pseudo-reference in a buffer with no defined couple has an ill-defined potential. docs/28 §4 [V]
    gives this for Ag without chloride; for gold it is UNVERIFIED but generic.
  * Covering it with an insulating SAM, streptavidin and antibody lowers its exchange current further, so it is
    noisier and more prone to drift. The HQ/BQ that the read produces then flows over it.
  * The model's drift term (0.55 pA/min) comes from `hw.gamry.baseline_drift` scaled by area. It is not a coated
    pseudo-reference value.
  * A drop cannot be confined to a 1 mm disc inside a 2 mm opening by hand.
* **Fix:**
  * The chip has separate pads, so after assembly remove the thiol selectively from the reference and counter by
    reductive desorption: address each pad as the working electrode at about −1.0 V in 0.1 M NaOH or KOH, a standard
    technique (potential UNVERIFIED for these chips). Do this before the streptavidin step.
  * Better, electroplate Ag on the reference pad and chloridise it. The 150 mM chloride in every buffer then holds it.
  * Add the reference's open-circuit stability against a commercial Ag/AgCl reference to T1-1.
  * Or take the printed gold strip S1PE-AU10, whose Ag/AgCl reference is apart from the working electrode (§3.5), as
    the primary tier-1 electrode.

### C4 — significant: bovine IgG route into the blank: the detection conjugate is not cross-adsorbed, and the bead stock contains ordinary BSA
* **Where:** docs/30 §2.1 (reagent table; "IgG-free BSA" rule), §4.2 step 1.
* **Evidence:**
  * Jackson 109-056-006 page [V]: AP F(ab′)₂ goat anti-human IgG, F(ab′)₂-specific; "reacts with the light chains of
    other human immunoglobulins"; "may cross-react with immunoglobulins from other species". It has no "min X" label
    and is supplied with 15 mg/mL BSA as stabiliser.
  * Jackson 109-066-098 page [V]: biotin-SP F(ab′)₂ goat anti-human IgG, Fcγ-specific, "min X Bov, Hrs, Ms Sr Prot".
    The capture is cross-adsorbed; the detection is not.
  * Thermo user guide MAN0014017 [V, full text]: M-280 Streptavidin is 10 mg/mL (6–7×10⁸ beads/mL) "in PBS pH 7.4,
    with 0.1 % BSA and 0.02 % sodium azide". Ordinary BSA carries bovine IgG (docs/29 C.2), and BSA pre-adsorbed on
    the beads is not removed by three washes.
  * An anti-human F(ab′)₂ (light-chain-reactive) polyclonal that is not adsorbed against bovine Ig can bind bovine
    light chains on every bead. That is non-specific label that the U1 experiment would attribute to "surface
    factor".
  * The goat–goat pair is a lesser concern. A goat anti-human-F(ab′)₂ reagent should be tolerant of goat
    immunoglobulin. The non-immune goat F(ab′)₂ controls already planned (§3.2 step 4, T2-1) measure it.
* **Fix:**
  * Choose a detection conjugate adsorbed against bovine serum proteins. Check Jackson's catalogue for a "min X Bov"
    AP F(ab′)₂ anti-human IgG; any part number is UNVERIFIED until opened.
  * Or include a bead-stock arm in T2-1: beads as supplied against beads stripped (0.1 % Tween, 3 washes) and
    re-blocked with IgG-free BSA.
  * Confirm on the Jackson certificate whether the conjugate's own BSA stabiliser is IgG-free.

### C5 — significant: hydroquinone half-life at pH 9.5 is probably minutes, not 2 h
* **Where:** `params/model_assumptions.yaml` alp_hqdp.product_half_life (7200 s, low 1800 s), used for the tier-2 stop
  (§4.3, §4.6 "in the model as a half-life").
* **Evidence:**
  * Moussavi 1979 via a property compilation [S]: first-order HQ autoxidation half-lives of 111 h, 41 h and 0.84 h
    at pH 7, 8 and 9. The rate is controlled by the HQ dianion [S, review summary].
  * Extrapolating the pH 8–9 slope (−1.69 decades of t½ per pH unit) gives t½ ≈ 7 min at pH 9.5 (Derived), 17×
    below the model value and 4× below its low bound.
  * Effect on tier 2 (Derived): of the product made during the 7 min stop, 73 % is still HQ at the sweep against the
    model's 98 %. That is a signal loss of about 25 %, more if the stop is lengthened (§5.3 "12 min" row).
  * The same chemistry ages the 1 µM HQ locator plug and the 0.1–100 nM HQ standards of T1-1 within minutes in
    pH 9.5 buffer.
  * Benzoquinone reacts with amines and thiols (Tris, protein lysines), so it is lost from the signal and can modify
    the capture layer. Its magnitude is UNVERIFIED.
  * The superoxide-chain mechanism makes the rate at nM HQ uncertain, possibly slower; this needs measurement.
* **Fix:**
  * Set product_half_life to 600 s (low 120 s, high 7200 s), UNVERIFIED, and re-run.
  * Measure it in T2-2: hold 50 nM HQ in substrate buffer in the cell for 0, 3, 7 and 12 min and sweep.
  * Make HQ standards in pH 7 buffer and dilute into substrate buffer immediately before use.
  * Test the sulfite stabilisation noted by Bekhit2021 (docs/30 §4.6) in the same experiment, since it costs
    nothing.

### C6 — significant: the MicruX add-on is clamped by magnets, a few millimetres from a bed of superparamagnetic beads, and the design rejects the magnet as a retainer
* **Where:** docs/30 §4.1 (bed in the inlet bore), §8 choice 3 ("no magnet"); docs/28 §1 table: "add-on held by
  magnets" [V].
* **Evidence:**
  * The fields of the clamping magnets will pull M-280 beads (≈ 12 wt % Fe [S, docs/29]) towards one side of the
    0.2 mm capillary. That makes a dense side and an open side, which is channelling of the kind T2-3 is meant to
    detect, but with a cause the design does not mention.
  * Conversely, docs/29 B.4.1 (Derived) shows a mm-scale NdFeB magnet holds M-280 at 10–100 µL/min.
  * docs/30 itself names the frit as the largest open point. A 20 mm² frit gives 2.3 pg/mL against 0.75 nominal, and
    the frit's internal area is "of the order of 20 mm²" against the assumed 5 mm².
  * A magnet-held plug has no retainer area at all.
* **Fix:**
  * Add a variant: no frit, a small NdFeB magnet (docs/28 §6 lists S-05-05-N [V there]) against the capillary tip,
    and a coarse downstream screen only as a safety stop.
  * Or use non-magnetic streptavidin beads if the bed stays fritted.
  * Measure bead position and effluent bead count with the add-on's own magnets in place (part of T2-1).

### C7 — significant: tier 2 reuses the strip across determinations, but every determination passes conjugate over it
* **Where:** docs/30 §4.1 ("the strip can stay for a series, the bed is new each time"); §2.4 (blanks on different
  consumables).
* **Evidence:**
  * "Everything injected still passes through the cell" (docs/26 §4). Each run deposits the strip's non-specific
    conjugate again, so after n runs the strip carries about n times the single-run enzyme load.
  * The swept read subtracts the strip's steady current, but the noise and drift of that current grow with it.
  * The HQ that the strip's enzyme makes under the lid during the 7 min stop diffuses across a 0.2 mm gap in about
    45 s (h²/D, Derived). It is collected partly during the stop and partly with the plug.
  * Blanks run on one strip are not independent, as docs/26 §3 requires them to be on different consumables. The
    strip is part of the consumable.
* **Fix:** use one strip per determination (printed carbon strips are cheap and are fitted in the same hand step as
  the bed), or limit a strip to a stated number of runs and show in T2-5 that the blank does not trend with run
  number.

### C8 — significant: a 5 min desthiobiotin release (tier 3) is unsupported, and the read bed may be saturated by free capture antibody
* **Where:** docs/30 §5.1 (transfer, specific × 0.7 [0.4–0.9]), §5.4 T3-1.
* **Evidence:**
  * Hirsch 2002 [V-abs, PMID 12419349, doi:10.1016/s0003-2697(02)00201-4]: desthiobiotin is "easily displaced by
    biotin". The abstract gives no rate or time.
  * Ying, Branchaud, Corry, Nanotech 2011 (Life Technologies) [V, full text opened]: "the rate of elution of
    desthiobiotinylated materials is too slow", and rebinding complicates elution.
  * Derived: with Kd ≈ 1×10⁻¹¹ M (vendor statements recalled, UNVERIFIED) and kon 10⁶–10⁸ M⁻¹ s⁻¹, koff is
    10⁻⁵–10⁻³ s⁻¹. One tag then releases 0.3–26 % in 5 min. A F(ab′)₂ carrying two or more tags on a dense
    streptavidin bead needs all of them off without rebinding (0.1–7 %).
  * The bounds 0.4–0.9 are therefore optimistic by up to two orders of magnitude.
  * If the read bed targets a tag on the capture antibody, the bed also has to take the bulk of eluted capture
    F(ab′)₂. Up to 8.4×10¹¹ molecules (1×10⁶ beads × 10 µg/mg, Thermo [V]) compete with 10⁴–10⁵ complexes. Recovery
    is bounded by the bed-2 capacity/eluate ratio: 0.12–0.95 for 10⁵–8×10⁵ sites per bead (Derived).
  * DNP alternative (§5.1): the anti-DNP elution time is UNVERIFIED, as docs/30 says.
* **Fix:**
  * Bound the transfer as specific × 0.05–0.7 until T3-1 measures it at 5 min and room temperature.
  * Tag the capture F(ab′)₂ with desthiobiotin **and** a hapten (DNP or fluorescein), elute with biotin, and
    recapture on an anti-hapten bed. Free biotin does not compete, and this removes the "phase-2 antibody not
    identified" gap. But load bed 1 at ≤ 20 % of its capacity so bed 2 can hold the eluate.
  * Consider a cleavable linker with a chemical release time of minutes instead of an affinity off-rate. Disulfide
    (NHS-SS-biotin, cut with TCEP or DTT) can also reduce the F(ab′)₂ hinge of both antibodies, so test it.
    Photocleavable biotin needs a 365 nm LED (allowed in tier 3). Catalogue numbers are UNVERIFIED.

### C9 — minor: Tris at pH 9.5 is a weak buffer, and the turnover number is not tied to it
* **Where:** docs/30 §2.2 (B1: 0.1 M Tris pH 9.5, 1 mM MgCl₂, 150 mM NaCl); params kcat_conjugate_assay_conditions
  1000 s⁻¹ (100–6000).
* **Evidence:**
  * β(0.1 M Tris, pKa 8.07) at pH 9.5 = 8 mM/pH (Derived). Tris pKa moves about −0.03 per °C (textbook,
    UNVERIFIED), so the substrate pH follows lab temperature.
  * Tris is a phosphate acceptor (transphosphorylation), which raises turnover above non-acceptor buffers. Sigma
    P4653 data [S]: Tris pH 10.2 gives about 2× the glycine activity, and DEA pH 9.8 about 5×.
  * 1000 s⁻¹ is a fair central value for a calf-intestine conjugate at about 25 °C in Tris. It follows from a vendor
    activity of roughly 2000–3000 U/mg at 37 °C in DEA (about 5000–7000 s⁻¹ for 140 kDa, Derived) with ×0.2–0.4 for
    temperature, buffer and conjugation (UNVERIFIED). But it is for p-nitrophenyl phosphate, not HQDP (see C1).
  * 1 mM Mg²⁺ is below the Mg(OH)₂ limit at pH 9.5 (5.6 mM, Derived). Activity after the pH 7.5 wash is not a
    concern: ALP is stable at pH 7.5 with no chelator present (UNVERIFIED, generic).
* **Fix:** compare 0.1 M Tris pH 9.5 with 1 M diethanolamine pH 9.8 (β 370 mM/pH, Derived) in the C1 test,
  keeping the 150 mM NaCl for the reference. Check that DEA gives no background on carbon at +0.30 V. A gain of about
  2× in turnover is plausible [S].

### C10 — minor: buildability of the tier-2 capillary bed
* **Where:** docs/30 §4.1, §4.2.
* **Evidence:**
  * Sleeve: IDEX F-385 is a PEEK sleeve, 1/32″ OD (0.794 mm) × 0.015″ ID, for 325–365 µm tubing [S, vendor listings
    via search]. It is the standard class of part for a 0.36 mm capillary. In the 0.8 mm bore [V docs/28] it leaves
    about 3 µm radial clearance, so it fits only if the PMMA bore is not undersized. Through the ¼″-28 port it needs a
    1/16″ sleeve and nut as well.
  * Frit: no vendor pore size for fused-silica frits was found (one search). Silicate frits retaining 2.8 µm beads
    are plausible, but their retention and internal area are UNVERIFIED (docs/30 already marks this).
  * Bed (Derived): Kozeny–Carman gives 1.4, 8.2, 21 and 33 bar at 3.5, 20, 50 and 80 µL/min, which matches the
    design's 25 bar.
  * A bed drawn in by syringe (≤ 1 bar) will compact at the first 50–80 µL/min flush.
  * 26 % of the 0.2 mm bore cross-section lies within 5 bead diameters of the wall, the loosely packed zone (Derived),
    so the wall bypass that T2-3 measures is real.
  * Pipetting 1.5 µL of suspension by hand gives a bead-count CV of a few percent (generic, UNVERIFIED).
* **Fix:**
  * Pre-compact each bed at 80 µL/min for 1 min before mounting, and check the bed length afterwards.
  * Set the tip-to-electrode distance with a stop (sleeve length) rather than by eye.
  * Prefer the magnet variant of C6, or a keystone-tapered tip (no frit; UNVERIFIED for 2.8 µm beads), to cut
    retainer area.

### C11 — minor: no free-HQ or HQMP specification on the HQDP item
* **Where:** docs/30 §2.1.
* **Evidence:** the Metrohm DRP-HQDP-0.5G page [V] gives 500 mg and 1 g sizes and no purity, free-HQ, storage or
  buffer specification. If HQMP is electroactive (C1), HQMP impurity and spontaneous hydrolysis to HQMP are a second
  background source that the "free hydroquinone 10⁻⁵" parameter does not cover.
* **Fix:** ask the vendor for a certificate of analysis. Measure HQ and HQMP content by HPLC-UV on the I-Class (C1b)
  as part of U3.

### C12 — minor: the tier-1 surface factor and printed gold
* **Where:** `tier_params.yaml` nsb.surface_factor_gold_oeg (3; 0.5–30); docs/30 §3.5.
* **Evidence:**
  * The cited OEG evidence (Nishimura2011 [V-abs in docs/29]; Prime/Whitesides ≈ 2 % of a fibrinogen monolayer [S])
    concerns bare OEG. After streptavidin, capture F(ab′)₂ and BSA, the surface the conjugate meets is the same
    protein stack as on the beads, plus SAM defects at the disc edge and SU-8 boundary.
  * A central value of 1–3 relative to beads is therefore defensible. A low bound of 0.5 (better than the beads) has
    no support, and 30 is a sensible upper bound.
  * Printed gold inks carry binder and are rough. Thiol monolayers on them are expected to be less ordered than on
    evaporated films (UNVERIFIED; one PubMed search found no comparison). docs/30's own caution is right.
* **Fix:** set the low bound to 1. Keep the side-by-side T1-2. Add an electrochemical-desorption charge or a
  ferricyanide blocking test as a SAM-quality check per chip batch.

## Checked and found sound
* Jackson 109-066-098 is biotin-SP F(ab′)₂ goat anti-human IgG, Fcγ-specific, min X Bov/Hrs/Ms serum proteins
  [V vendor page]. Jackson 109-056-006 is AP F(ab′)₂ goat anti-human IgG, F(ab′)₂-specific [V vendor page]. Both exist
  as described (see C4 for the cross-adsorption difference).
* Dynabeads M-280 Streptavidin: 10 mg/mL, about 6–7×10⁸ beads/mL, about 10 µg biotinylated antibody per mg,
  650–900 pmol free biotin per mg [V, MAN0014017]. "About 10 µg per mg" and "1.5 µL for 10⁶ beads" are right (Derived:
  1.54 µL, 15 µg beads, 154 ng F(ab′)₂, 8×10⁵ per bead, 24.6 mm²).
* The Metrohm DRP-HQDP-0.5G item exists [V].
* 0.3 mM HQDP at Km 0.1 mM gives 75 % of Vmax, as stated. 1 mM Mg²⁺ is soluble at pH 9.5.
* The bed's pressure drop and dimensions (19 nL, 0.6 mm) agree with my Kozeny–Carman check.
* The bed CV of 10 % is consistent with Molinero-Fernández 2020: inter-batch 9 % for M-280 bead assays
  [V-full in docs/29].

## What could not be checked
* Whether HQMP is oxidised at +0.30 V on printed carbon or at the tier-1 potential on coated gold (C1). This is the
  decisive gap; no source was found.
* The rate of HQ oxidation through a specific biotin-OEG/OEG thiol monolayer with a protein overlayer. Only indirect
  evidence was found ([S]).
* SAM stability at pH 9.5 and +0.3–0.6 V in 150 mM chloride over 1–2 h (no source opened).
* Desthiobiotin–streptavidin koff and a measured 5-min elution yield. Anti-DNP elution times.
* Human-IgG contamination levels of laboratory blanks (no source opened). The unit-to-unit blank CV of hand-coated
  electrodes (15 %): only signal CVs are in the literature I saw.
* Pore size and internal area of commercial fused-silica frits. The exact bore tolerance of the MicruX PMMA add-on.
* The position and strength of the add-on's clamping magnets relative to the inlet bore (C6).
* The Moussavi 1979 primary source (C5 rests on a compilation quoted by a search summary).

## Changes of chemistry that would most lower the LOD, per tier
* **Tier 1:**
  1. A short-chain OEG thiol, or printed carbon with adsorbed streptavidin, so that HQ (or HQMP) is oxidised at low
     overpotential (C2).
  2. A real Ag/AgCl reference: electroplated on the chip's reference pad, or the S1PE-AU10 strip (C3). This attacks
     the 63 % drift term.
  3. A higher-turnover substrate buffer (DEA, C9) with the read potential set from an enzymatic product (C1).
* **Tier 2:**
  1. Remove the frit: hold the beads with a magnet (C6). The modelled LOD moves from 0.75 towards 0.36 pg/mL (docs/30
     §4.1, 1 mm² row) as the retainer term falls.
  2. A detection conjugate adsorbed against bovine proteins, and beads re-blocked with IgG-free BSA (C4).
  3. A fresh strip per run, plus the product-identity and half-life fixes (C1, C5), which protect the signal rather
     than lower the blank.
* **Tier 3:**
  1. A dual-tag capture (desthiobiotin + hapten) with an anti-hapten read bed, or a chemically cleavable linker,
     instead of a desthiobiotin off-rate (C8).
  2. Load bed 1 at low capacity so bed 2 is not saturated by free capture antibody (C8).
