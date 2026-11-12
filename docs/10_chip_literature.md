# 10 — Literature survey for a second-generation microfluidic cartridge

Status: first complete pass (2026-11-12). Abstract-level verification only; no full texts read.

Scope: everything after the autosampler on a cartridge (incubation/mixing, capture, washing, enzymatic
amplification, electrochemical readout, on-chip valving, on-board reagents) for human IgG in buffer at
≤ 1 pg/mL (≈ 6.7 fM), ≤ 100 µL injected, ≤ 60 min. First-generation design: docs/05 §4. Precedent already in
docs/01 (Rissin2010/Chang2012, Xu1989, Jenkins1988, DellaCiana1996, Thomas2004, Kim2003, Niwa1993, Das2007,
Akanda2011, Han2014, Pollema1992/1994, Wilson2004, Qu1998, deFrutos1993, …) is **referenced, not repeated**.

## Conventions

* **Verification tags** (as in docs/01): **[V-abs]** read in this session from the PubMed abstract/metadata;
  **[V-sec]** read only in a search-engine/secondary summary (named); **[V-vendor]** vendor or regulatory document
  read via search summary; **UNVERIFIED** recalled, not checked in this session.
* **Confidence**: high = number stated in the primary abstract; medium = stated in abstract but conditions unclear,
  or secondary source; low = derived/indirect.
* **Unit conversion** (derived, not literature): c[fM] = c[pg/mL] / MW[kDa] × 1000. IgG 150 kDa → 1 pg/mL = 6.7 fM.
  Other MWs used: IL-6 ≈ 21 kDa, IL-8 ≈ 8.4 kDa, cTnI ≈ 24 kDa, ovalbumin ≈ 45 kDa, CEA ≈ 180 kDa, PTH ≈ 9.4 kDa,
  AFP ≈ 70 kDa (typical literature MWs, UNVERIFIED individually; they only set the order of magnitude).
* "Consensus" URLs are the record links returned by the Consensus search tool (the free plan does not return DOIs).
* Tool notes: PubMed via NCBI E-utilities (esearch/efetch, abstracts only), Consensus (rate- and quota-limited:
  93 % of the month's quota used during this session), WebSearch. No full texts were read in this session, so
  geometry details that are only in full texts are marked "not in abstract".

---

## 1. Microfluidic magnetic-bead immunoassays with electrochemical (and benchmark optical) readout

### 1.1 Table

| Key | Format, how beads retained / mixed / released | Label / readout | Reported LOD (→ pg/mL, fM) | Sample vol. | Time | Verif. / conf. | Source |
|---|---|---|---|---|---|---|---|
| Choi2002 | Glass "microfluidic motherboard", surface-mounted magnetic **biofilter** (bead trap) + EC immunosensor; beads are both solid phase and carrier | enzyme EC (not in abstract) | not in abstract | < 50 µL wasted over 5 repeated assays | < 20 min incl. incubation | V-abs / med | doi:10.1039/b107540n |
| Do2008 | Injection-moulded / hot-embossed **COC** chip; on-chip magnetic separator + **IDA** microelectrode | enzyme-labelled ECIA, chronoamperometry | mouse IgG 16.4 ng/mL (≈ 1.1×10⁵ fM) | not in abstract | 35 min | V-abs / high | doi:10.1039/b715569g |
| Herrmann2006 | PDMS, stop-flow chambers, **internal magnetic mixing** of beads; immune complex formed off-chip | fluorescence (enzymatic) | anti-streptavidin Ab 0.1–6.7 pM range (≈ 15 pg/mL lower end, ~100 fM) | not in abstract | not in abstract | V-abs / med | doi:10.1039/b516031f |
| Herrmann2007 | PDMS **not passivated**; immune-complex formation and enzyme reaction in **two separate channel networks** joined by pressure-valved "fluidic bridges"; beads magnetically transferred between them | fluorescence (enzymatic) | model Ab 100 pg/mL (660 fM, authors' figure), linear to 4 ng/mL | not in abstract | 30 min | V-abs / high | doi:10.1039/b707883h |
| Purushothama2001 (Heineman/Halsall group) | Bead sandwich, readout in a **microdrop with rotating-disk electrode** to avoid product dilution | ALP / pAPP → pAP | ovalbumin 0.1 ng/mL (≈ 2 pM) | microdrop | not in abstract | V-abs / high | doi:10.1039/b006798i |
| Sista2008a | **Digital microfluidics (EWOD)**; beads held by permanent magnet, supernatant split off by electrowetting; resuspension by moving the droplet over 5 electrodes | chemiluminescence (UNVERIFIED for label; not in abstract) | insulin, IL-6 standard curves (LOD not in abstract) | droplets | **7 min** total | V-abs / high (for process data) | doi:10.1039/b807855f |
| Sista2008b | Same DMF cartridge (PCB), whole blood | — | cTnI assay (LOD not in abstract) | — | < 8 min | V-abs / med | doi:10.1039/b814922d |
| Shamsi2014 | DMF with Au sensing + Ag counter/pseudo-reference electrodes in the ITO top plate; magnetic microparticles | HRP / TMB amperometry | TSH 2.4 µIU/mL | droplets | not in abstract | V-abs / high | doi:10.1039/c3lc51063h |
| Otieno2014 (Rusling) | Modular PDMS; **stirred on-line capture chamber**, beads held magnetically during capture/wash, magnet removed + valve switch sends beads to an 8-sensor AuNP-film detection chamber | 1 µm beads carrying ~3×10⁵ HRP + 4×10⁴ Ab; amperometry | IL-6 5 fg/mL (≈ 0.24 fM), IL-8 7 fg/mL (≈ 0.8 fM), **serum** | not in abstract (5 µL in sister papers) | 30 min | V-abs / high | doi:10.1016/j.bios.2013.09.054 |
| Malhotra2012 (Rusling) | Off-line capture on beads with 4×10⁵ HRP and ~10⁵ Ab, then injection into an 8-sensor array | multi-HRP amperometry | IL-6, IL-8, VEGF, VEGF-C 5–50 fg/mL, diluted serum | — | 50 min | V-abs / high | doi:10.1021/ac301392g |
| Krause2015 (Rusling) | Same capture-chamber concept, 1 µm beads | multi-HRP | 10–40 fg/mL; 2.5–10 zmol (≈ 1500 molecules) | 5 µL serum | 30 min | V-abs / high | doi:10.1007/s00216-015-8873-1 |
| Otieno2016 (Rusling) | Same | multi-HRP | PTHrP 150 aM | 5 µL serum | 30 min | V-abs / high | doi:10.1021/acs.analchem.6b02637 |
| Sharafeldin2017 | Fe₃O₄@GO particles capture then deliver to 8-sensor chamber | particle peroxidase-like / H₂O₂ | PSA 15 fg/mL, PSMA 4.8 fg/mL | — | not in abstract | V-abs / med | doi:10.1016/j.bios.2016.12.052 |
| Freitas2019, Baldo2021 | Disposable EC microfluidic device; MB-HRP capture then EC sandwich on graphene-oxide electrode | HRP / HQ + H₂O₂ | 0.3 fg/mL (CTV capsid), 0.2 fg/mL (ovalbumin) | — | — | V-abs / low (extraordinary claims; blank analysis not in abstract) | doi:10.1016/j.talanta.2019.07.005; doi:10.1016/j.talanta.2021.122447 |
| Wang2001 | Glass chip: pre-column ALP-Ab + antigen reaction, **electrophoretic** separation of free vs bound conjugate, post-column pAPP reaction, amperometry | ALP / pAPP | mouse IgG 2.5×10⁻¹⁶ g/mL (1.7×10⁻¹⁸ M) — authors' figure | — | ~6 min migration | V-sec (Consensus abstract) / low (homogeneous competitive-type format; not reproduced) | Consensus: https://consensus.app/papers/details/w:94857d5a-cdcb-4189-87d7-e48965241d1c/ |
| Messina2008 | Controlled-pore-glass packed in central channel (bead bed, not magnetic); sandwich with SA-ALP | ALP / pAPP on Au at 0.10 V | IL-6 1.56 pg/mL EIA (≈ 74 fM); pAP detection 0.41 pg/mL-equiv; CV < 6.5 % | — | — | V-sec (Consensus abstract) / med | https://consensus.app/papers/details/w:ac89d9d4-ec0e-42bf-9f05-a4e789b70a2b/ |
| Ito2021 | Magnetic beads in tube, LAL cascade label, **nanogap redox-cycling** device | endotoxin label → pAP | goat IgG 70 fg/mL (470 aM); 10 pg/mL without redox cycling | — | > 1 h (LAL) | V-sec (Consensus) / med | https://consensus.app/papers/details/w:28dc402b-d6f6-45f2-a794-78363cd3362d/ |
| Phurimsak2016 (Pamme) | Magnetic **particle plug** trapped in a channel; reagents and washes flushed over the plug | fluorescence | CRP, P4 clinically relevant (LOD not given in abstract) | low µL | **15 min** | V-abs / med | doi:10.3390/mi7050077 |
| Pereiro2017 | **Magnetic fluidized bed** of 1–5 µm beads, 0.1–5 µL/min, < 100 mbar | fluorescence immunocapture | 0.2 ng/mL | **200 µL** | not in abstract | V-sec (Consensus) / med | https://consensus.app/papers/details/w:1cc3ba31-c015-45bc-9c41-65e7ad7a57d3/ |
| Kim2015 | Magnet drags beads through oil/water interfaces stabilised by micro-pillars | fluorescence | oligomeric Aβ ~10 pg/mL | — | 45 min | V-abs / med | doi:10.1016/j.bios.2014.10.042 |
| Rissin2013 (Simoa disc) | Beads in fL wells on a microfluidic disc, oil-sealed (digital, optical) | SβG / RGP | sub-fM, 4-plex in plasma | — | — | V-abs / high | doi:10.1039/c3lc50416f |
| Dittmer2008 / Bruls2009 / Dittmer2010 (Philips Magnotech, later Minicare) | **One-step**, no fluid exchange: 300–500 nm magnetic particle labels carrying tracer Ab actuated through the sample by electromagnets above/below the chip; magnetic "wash" pulls unbound labels away from the sensor | GMR (2008) / frustrated TIR optics (2009–10) | PTH 0.8 pM in 15 min (2008); cTnI sub-pM "in a few minutes" (2009); cTnI 0.03 ng/mL (≈ 1.3 pM) in **5 min**, blank + 3 SD, plasma (2010) | finger-prick | 1–15 min | V-abs / high | doi:10.1016/j.jim.2008.07.001; doi:10.1039/b913960e; doi:10.1016/j.cca.2010.03.001 |

### 1.2 Reading
* **No electrochemical bead chip with an enzyme label and plain buffer has a verified ≤ 1 pg/mL IgG-class result
  with a blank analysis in the abstracts read.** The sub-fM claims (Rusling 5–50 fg/mL; Freitas/Baldo 0.2–0.3 fg/mL)
  all use **massive-label beads** (10⁵–10⁶ HRP per bead) captured on a second antibody layer on the electrode, i.e.
  a two-surface format; the blank-limiting NSB is that of a label-loaded bead on an antibody-coated electrode.
  Whether the same holds for a 150 kDa IgG analyte where many anti-IgG reagents cross-react is not shown.
* The best-evidenced integrated **enzyme + bead + EC** chips (Choi2002, Do2008) are 3–4 orders of magnitude above the
  target (16 ng/mL IgG). The gain since then came from labels (multi-enzyme beads), not from fluidics.
* **Separation of the binding phase from the signal phase** is the recurring design pattern for low background:
  Herrmann2007 (two channel networks, bead transfer), Rusling (capture chamber → detection chamber), Wang2013
  (bead drag between wells, < 0.002 % substrate carry-over; §2), and docs/01's Ishikawa immune-complex-transfer
  principle. Herrmann2007 achieved this **without any passivation of PDMS**.
* Time: integrated magnetic formats reach answers in 5–35 min (Dittmer2010 5 min, Sista 7 min, Rusling 30 min),
  but at pM, not fM. The ≤ 60 min, ~fM regime is held only by Simoa-type digital readout (docs/01) and by the
  multi-label Rusling arrays (serum, 5 µL, 30 min).

---

## 2. On-chip bead manipulation

| Topic | Finding | Verif. / conf. | Source |
|---|---|---|---|
| Trapping vs flow (permanent magnet, PDMS chamber, 4.5 µm beads) | Trapping efficiency 92.1 % (1 magnet) / 95.2 % (2 magnets) at 5 µL/min, but only 20.6 % / 15.9 % at 20 µL/min | V-sec (Consensus abstract) / med | Zaini 2021, Evergreen, https://consensus.app/papers/details/w:6183462d-45ee-487d-a56c-dbb181e6b62c/ |
| Trapping vs flow in a chamber (DNA-library chip, simulation + experiment) | Inlet 0.02 → 0.16 m/s and magnet spacing 1.2 → 1.8 mm: capture 100 % → 35 %; bead coverage 17 → 64 %; release by combined flow + field, 100 % within 12 s | V-sec (Consensus) / med | Song 2025, Micromachines, https://consensus.app/papers/details/w:9ef79fa1-fa4a-4fd8-b879-16d796d4bb4e/ |
| Edge-limited trapping | With two magnets in attraction around a channel, beads trap mainly at the magnet edges; a laser-ablated magnetic-track array in PET spreads capture along the magnet: +300 % trapped beads | V-sec (Consensus) / med | Abonnenc 2009, Anal Bioanal Chem, https://consensus.app/papers/details/w:2864255b-8d2c-46e1-a1d3-6522c353604c/ |
| Design theory | Capture efficiency depends on two dimensionless groups (dipole strength, particle size/susceptibility, viscosity, velocity, channel height, magnet distance) | V-sec (Consensus) / high (qualitative) | Nandy 2007 JMMM, https://consensus.app/papers/details/w:13137fbc-1fd9-45a6-b34e-9fbc80e67114/; Sinha 2007 Phys Fluids, https://consensus.app/papers/details/w:8fcf3a0a-f8b2-4b9d-beec-22598b6cc773/ |
| Soft-magnetic packed trap | Bed of 6–8 µm iron beads against a restriction (0.8 nL dead volume) focuses an external field: 30 nm particles trapped/released in 20 s at 100 µL/h, preconcentration 4000× | V-abs / high | Teste2011, doi:10.1039/c0lc00510j |
| Bead retention during washing (DMF) | ~100 % bead retention after a 7776-fold dilution wash | V-abs / high | Sista2008a, doi:10.1039/b807855f |
| Bead transfer instead of fluid washing | Beads dragged by a moving magnet between two wells through a tapered channel: > 95 % transferred in 2 min at 0.7 mm/s; **carry-over of DiFMUP substrate < 0.002 %** (2×10⁻⁵) | V-abs / high | Wang2013, doi:10.1039/c3an01166f |
| Mixing: internal magnetic actuation | Beads used for stop-flow mixing in channels (Herrmann2006); rotating permanent magnet forms flagella-like chains that travel across laminar streams (Karle2010; sample 0.75 µL/s) | V-abs / med | doi:10.1039/b516031f; doi:10.1039/c0lc00129e |
| Mixing: on-chip electromagnets | Philips: electromagnets above/below the cartridge actuate 300–500 nm particles for capture, sensor binding and magnetic wash (no fluid exchange) | V-abs / high | Dittmer2008, Bruls2009 (above) |
| Resuspension: acoustic | Langevin transducer + horn into a disposable polymer chip, 20 µL chambers: resuspension of a magnet-collected bead pellet; fluid mixing in < 1 s, cell lysis in 25 s; Peltier + fan to keep < physiological temperature | V-abs / high | Iranmanesh2016, doi:10.1007/s10544-016-0097-4 |
| Fluidised bed | Magnetic fluidised bed: continuous bead recirculation at 0.1–5 µL/min, < 100 mbar | V-sec / med | Pereiro2017 (§1) |
| Bead collection on a disc | Multiphysics model with M-270 beads: collection is a bottleneck repeated at every step and causes **cumulative bead loss**; collection time depends linearly on magnet distance (2–6 mm) and exponentially on rpm | V-sec / med | Wimmer 2026, RSC Adv, https://consensus.app/papers/details/w:a0f3cc07-fe50-40bb-a48f-bb9c5ecda370/ |
| Bead settling in on-board reservoirs | **No quantitative source found in this session.** Stokes estimate for 2.8 µm, ρ ≈ 1.6 g/cm³ (UNVERIFIED density): ~1 µm/s, i.e. ~4 mm/h — reservoirs must be agitated or beads stored dry (derived, low) | — | — |

**Reading.** For the 2.8 µm beads of docs/05, trap efficiency falls steeply above a few µL/min in a single
magnet/chamber geometry (92 % → 21 % between 5 and 20 µL/min, Zaini 2021): a cartridge trap must either run slowly,
use multiple/soft-magnetic focusing elements (Teste2011, Abonnenc 2009), or avoid flow-through capture altogether
by moving beads rather than liquid (Wang2013, Philips, DMF). Bead transfer has a measured carry-over of < 2×10⁻⁵ for a
small-molecule substrate — the only quantitative carry-over number for bead-transfer formats found here.

---

## 3. Bead-free (or fixed-bed) on-chip capture formats and their regeneration

### 3.1 Table

| Key | Capture format | Analyte / readout | Reported performance | Time / volume | Reuse data | Verif. / conf. | Source |
|---|---|---|---|---|---|---|---|
| Sato2000 | Polystyrene beads packed in a glass microchannel (bead bed behind a dam; geometry not in abstract) | s-IgA, colloidal-gold label, thermal lens | antigen–antibody reaction time cut to 1/90; total < 1 h vs 24 h | — | single use | V-abs / high | doi:10.1021/ac991151r |
| Sato2001 | Same bead-bed, 3-antibody sandwich | CEA in serum | LOD "dozens of times lower" than ELISA (number not in abstract); r = 0.917 vs ELISA (n = 13) | **35 min** vs 45 h | single use | V-abs / med | doi:10.1021/ac000991z |
| Honda2005 (Gyrolab) | **Streptavidin particle micro-column** on a centrifugal CD; biotin-capture Ab loaded per run; flow set by rpm | AFP, IL-6, CEA; Alexa-647 detection | LOD AFP 0.15 pM (≈ 10 pg/mL), IL-6 1.25 pM (≈ 26 pg/mL), CEA 1.31 pM; CV < 10 % inter, < 20 % intra above 5 pM | 200 nL sample through the column in 240 s; 104 assays in 50 min | single-use CD | V-abs / high | doi:10.1373/clinchem.2005.053348 |
| Fraley2013 (Gyrolab) | 15 nL streptavidin bead bed per microstructure | mAb in NHP plasma | validated 5–250 µg/mL | — | single use | V-abs / high | doi:10.4155/bio.13.145 |
| Gyros vendor | 15 nL column; "brief contact" claimed to minimise NSB; low pg/mL only with the 4000 nL-sample CD; 3–4 log range | — | — | 20–4000 nL | — | V-vendor (search summary) / low | https://mesalabs.com/hubfs/GPT/pdfs/3-Gyros/Marketing%20material/PIS/D0012493%20PIS-Gyrolab-Bioaffy-CDs.pdf |
| Ella / Simple Plex | Glass nano-reactors (GNR) coated with capture Ab, 2–3 per channel → triplicates; single-use cartridge | cytokines; fluorescence | "pg/mL"; GFP cartridge 0.71 pg/mL in 90 min (vendor); correlation with ELISA/Luminex | 25 µL class | single use | V-abs (Aldo2016: qualitative only) + V-vendor / low for numbers | doi:10.1111/aji.12512; https://rndsystems.com/products/simple-plex-green-fluorescent-protein-cartridge_spckb-ot-002820 |
| Kang2013 | Poly(GMA-co-EGDMA) **porous polymer monolith**, UV-polymerised in PDMS | IgG (direct) / H1N1 (sandwich), fluorescence | IgG 4 ng/mL; H1N1 < 10 pg/mL | 5 µL sample | not stated | V-abs / med | doi:10.1039/c3an36744d |
| Liu2010 | GMA/ethoxylated-TMPTA monolith in silica capillary, anti-IgG | FITC-IgG (direct) | linear 0.1–50 ng/mL in 5 min; 1 µL injections → mass LOD 100 pg (~700 amol) | 5 min | — | V-abs / high | doi:10.1016/j.bios.2010.06.007 |
| Wiederoder2015 | Monolith in capillary; packed glass beads in thermoplastic channel | human IgG, silver enhancement + index matching | 0.1 ng/mL, 5-log range; direct assay 10 min | — | — | V-abs / high | doi:10.1039/c5an00988j |
| Yu2001 | Photo-patterned monolith in chip (SPE) | — | low flow resistance: up to 10 µL/min, 50 mm/s linear velocity; ~10³ preconcentration | — | — | V-abs / high (hydraulics) | doi:10.1021/ac0106288 |
| Sun2008 | Epoxy affinity monolith in PMMA chip | FITC-HSA | 92 % mean elution efficiency | — | elution shown | V-abs / high | doi:10.1021/ac800322f |
| Messina2008 | Aminopropyl controlled-pore glass packet in central channel | IL-6, SA-ALP / pAPP, Au 0.10 V | 1.56 pg/mL (≈ 74 fM) | — | single use (implied) | V-sec / med | (§1) |
| Uthuppu2015 | Immunosorbent immobilised in channel of a modular µFIA chip, amperometric | BAM (hapten), competitive | IC50 0.25 µg/L | — | **51 regeneration cycles** (27 without analyte) "high long-term stability" | V-abs / high | doi:10.1039/c4an01576b |
| Sun2026 | Ab on AuNP electrode in a flow cell | adiponectin, EC | LOD 9.3 pg/mL; sensitivity 3.03 µA/decade over **14 regeneration cycles** | — | 14 cycles | V-abs / high | doi:10.1016/j.talanta.2025.129122 |
| Tseng2009 | Photo-acid (o-NBA) local pH drop 7 → 3.5 in 20 s under UV for regeneration | optical | 2 cycles, < 8 min per cycle | — | 2 cycles | V-abs / med | doi:10.1039/b823449c |
| Zinggeler2017 | Cryogel monolith arrays in capillary, capillary flow | IL-6 | "high sensitivity" (number not in abstract) | — | — | V-abs / low | doi:10.1021/acs.analchem.7b01182 |

### 3.2 Reading
* **Fixed beds / monoliths give fast capture** (minutes; Sato 1/90 reaction time, Liu2010 5 min, Honda 240 s
  through 15 nL) but in every case found the readout was optical and the LOD in the 10 pg/mL–ng/mL range; no
  monolith/bed + EC + enzyme result at ≤ 1 pg/mL was found.
* The commercial architectures that carry **streptavidin beds or glass nano-reactors (Gyrolab, Ella) are single-use**
  and use a fresh capture surface per sample (Gyrolab loads biotinylated capture Ab onto the SA bed for each run).
  This is the same "renewed surface" principle as docs/01 (Pollema), executed as a disposable microstructure rather
  than as injected beads.
* **Regeneration data on chip are thin**: 51 cycles (hapten, competitive, Uthuppu2015), 14 cycles (Sun2026), 2 cycles
  (Tseng2009). The best regeneration number remains the SPR anti-Fc surface (> 300 cycles, Kamat2021 in docs/01). No
  per-cycle loss for a sandwich IgG assay on a microfluidic bed was found. Loss per cycle in the model (0.5 %/cycle,
  docs/05 §4.2) remains UNVERIFIED for chips.
* Pillar arrays: only a droplet/magnet aid (Kim2015) and generic micropillar papers were located; no quantitative
  pillar-capture sub-pg/mL EC result was found in this session.

---

## 4. On-chip electrochemical detection for ALP (and related) products

### 4.1 Redox cycling (IDA / nanogap) — amplification vs geometry

| Key | Geometry | Species | Amplification / collection | Conditions | Verif. / conf. | Source |
|---|---|---|---|---|---|---|
| Thomas2004, Niwa1993, Kim2003 | (see docs/01) Pt IDA 1.6 µm gap: 4×, 87 % | pAP | — | — | — | docs/01 |
| Lewis2010 | Au microbands 50 µm wide, **25 µm gaps**, in a 22 µm × 600 µm channel; on-chip pseudo-reference | ferrocyanide | up to **7.6×** in confined static solution | static | V-sec (Consensus) / high | https://consensus.app/papers/details/w:7cca42b2-02c0-4083-aec1-8bbfba2a439a/ |
| Chen2011 | IDA **10 µm** spacing in a microfluidic channel | pAP from β-gal/PAPG | **97 % recycling**; pAP LOD **1.0×10⁻¹⁰ M** in **70 nL**, linear 10⁻⁹–10⁻⁵ M; anti-fouling step needed | perfectly static flow | V-sec (Consensus) / high | https://consensus.app/papers/details/w:b9c8451f-4d3c-469e-929e-ec65f4fc9295/ |
| Odijk2008 | IDA **1 µm** spacing (FEM + experiment) | — | **65×** | — | V-sec / med | https://consensus.app/papers/details/w:ffcaccfb-a3e7-4d88-94f6-f2b277827e93/ |
| Kamath2014 | 3D pyrolysed-carbon IDEA | — | 37× at width/gap 1.58, height 1.1 µm; 9× at 0.22 µm height; **37 → 4 at 500 nL/s flow** | flow vs no-flow | V-sec / high | https://consensus.app/papers/details/w:d69b2f6e-46a6-4760-acae-09881d99afd9/ |
| Heo2013 | 1:1 aspect-ratio carbon IDA nanoelectrodes in PDMS channel | — | up to **1116×**; channel height and aspect ratio matter | static | V-sec / med | https://consensus.app/papers/details/w:ab288907-cb4a-42df-9c83-108b8b1fe66b/ |
| Goluch2009 | IDA in a **nanofluidic channel** | paracetamol | ~100×; rejects irreversible interferent (ascorbate) | — | V-abs / high | doi:10.1007/s00216-008-2575-x |
| Zevenbergen2009 | 50 nm cavity between two parallel electrodes | Fc(MeOH)₂ | "mechanically robust and stable over time" | — | V-abs / med | doi:10.1021/ja902331u |
| Matylitskaya2018 | nanogap IDA, **100 nm** gap | FcMeOH; **pAP** | > 160× with FcMeOH; inverse gap–amplification relation; **pAP forms a polymer film during redox cycling → lower amplification**; cleaning by O₂ plasma + CV | — | V-sec / high | https://consensus.app/papers/details/w:ae1f7110-ee22-492f-a9d7-020d2ccad811/ |
| Dotan2023 | IDA 5–10 µm, 3D + 1D model + experiment | — | regime transition velocity v[mm/s] = 0.335/L[µm] + 0.04 (L = electrode width/spacing scale): below it redox-cycling-limited, above it convection-limited | flow | V-sec / med | https://consensus.app/papers/details/w:a83399a3-adb6-4d54-9b72-fff114005972/ |
| Romero-Soto2025 | Au IDE 10, 5, 2 µm gaps | MB, ferri/ferro | flow lowers RA (∝ cube root of flow) but raises signal; vibration ×4–8 signal | — | V-sec / med | https://consensus.app/papers/details/w:582241f5-3677-4c68-956b-f6f2f2980325/ |
| Ito2023 | IDA device | pAP | 79.8 % cycling, 4.79× | — | V-sec / med | https://consensus.app/papers/details/w:99c7cb98-20ce-4fbf-aba7-d48ea3e05a1c/ |
| Borchers2021 | interdigitated bipolar electrodes 35 → 5 µm | — | LOD improved 10× over that gap range | — | V-sec / med | https://consensus.app/papers/details/w:f2415bb9-500a-476e-8050-63004a5a9a0c/ |

**Reading.** (1) Amplification scales inversely with gap and with how well the volume is confined: µm-gap planar IDAs
give 4–65×, sub-µm/nanochannel devices 100–1100×. (2) **Flow destroys most of the gain** (Kamath 37 → 4 at
500 nL/s; Dotan's transition velocity for 5 µm features ≈ 0.1 mm/s): the IDA should be read in **stopped flow**,
which also matches Chen2011's best pAP LOD (10⁻¹⁰ M in 70 nL, static). This is a direct caution for docs/05's
"sweep the trap contents through the IDA at 10 µL/min" readout. (3) **pAP polymerises on nanogap IDAs**
(Matylitskaya2018; Buckey2022 in docs/01), supporting HQ/HQDP (Wilson2004, docs/01) for a reused electrode; no
direct HQ-on-IDA fouling data were found in this session.

### 4.2 Stopped-flow accumulation in small chambers
* Chen2011: 70 nL static volume, pAP LOD 1×10⁻¹⁰ M (V-sec / high) → 7×10⁻¹⁸ mol (≈ 4×10⁶ molecules) in the
  chamber (derived). At kcat ≈ 1000 s⁻¹ (docs/01) that is ~70 enzyme-minutes of product — i.e. a 70 nL chamber read
  by IDA could resolve ~10–100 enzymes in a few minutes **if** the substrate blank allows (derived, low).
* Purushothama2001: microdrop + rotating disk to avoid product dilution (V-abs). Herrmann2006: stop-flow chambers.
* Digital limit: Simoa fL wells (Rissin2010/2013) — single enzymes, optical. No electrochemical digital-ELISA with
  ALP and HQ was located in this session (searched; no hit).

### 4.3 On-chip reference electrodes and electrode reuse

| Item | Finding | Verif. / conf. | Source |
|---|---|---|---|
| Thin-film Ag/AgCl with graphene-oxide protective layer | potential drift < 2 mV over 26 days | V-abs / high | Kim2015, doi:10.3390/s150306469 |
| Sputtered thin-film Ag/AgCl | "stable potentials in concentrated chloride solutions for a long period" (no number) | V-abs / med | Hiratsuka2001, doi:10.1039/b008036p |
| Ag/AgCl on Pt quasi-reference on chip | improved stability over bare Pt (no drift number in abstract) | V-abs / med | Branch2017, doi:10.1021/acs.analchem.7b00258 |
| DMF Ag pseudo-reference | used in amperometric TSH assay | V-abs / med | Shamsi2014 |
| Pseudo-reference in 1.5 nL valved volumes | OCP stability measured vs commercial Ag/AgCl (values not in abstract) | V-abs / low | Tomar2021, doi:10.3390/mi12070762 |
| Electrode cleaning for reuse | O₂ plasma + CV cleaning restores nIDA after pAP films | V-sec / med | Matylitskaya2018 |

A thin-film Ag/AgCl drifts little only while the chloride activity is constant: a cartridge using Cl⁻-free
carbonate/borate substrate buffer (docs/05 uses TBS wash, pH 9.5 substrate) needs a fixed Cl⁻ in every solution
that touches the reference, or a junction-protected reference (inference, low).

---

## 5. Non-specific adsorption on chip materials and passivation

### 5.1 Table

| Material / coating | Finding (number as given) | Verif. / conf. | Source |
|---|---|---|---|
| PLL-g-PEG on TiO₂ | no protein adsorption within ellipsometry LOD from full plasma (30 min), vs ~350 ng/cm² on bare Ti | V-abs / high | Tosatti2003, doi:10.1016/s0142-9612(03)00420-4 |
| Polyacrylamide brush (SI-ATRP, Au) | single proteins < 3 pg/mm² (= 0.3 ng/cm², SPR LOD); 10 % plasma 5, 100 % serum 28 pg/mm²; "comparable to PEG and pSBMA, the best antifouling materials" | V-abs / high | Liu2012, doi:10.1021/bm201814p |
| pSBMA / pCBMA on glass (ATRP) | fibrinogen adsorption reduced to PEG-like level (ELISA; number not in abstract) | V-abs / med | Zhang2006, doi:10.1021/la062175d |
| Zwitterionic vs amphiphilic peptide SAM (Au) | 1.97–11.78 ng/cm² (single proteins) | V-abs / high | Ye2015, doi:10.1021/acsami.5b06500 |
| Parylene-C-caulked PDMS | BSA adsorbed under 2 µL/min flow = 35.2 % of pristine PDMS; after 60 min PBS wash residual 4.5 % of pristine | V-sec / high | Liu 2016 Biomicrofluidics, https://consensus.app/papers/details/w:fc5f2574-cf2f-4f1c-bf58-0d8f2d51bda4/ |
| PMMA: BSA coating / O₂ plasma / PEG | FITC-BSA NSA reduced 87.6 % (BSA coat), 86.1 % (plasma); PEG less stable | V-sec / med | Xian 2023, https://consensus.app/papers/details/w:72ffa97d-1255-489d-befc-4a58e7ea4e2d/ |
| CYTOP, silica, SU-8 | silica adsorbs more BSA than S-grade CYTOP despite hydrophilicity (fixed positive charge); SU-8 lowest | V-sec / med | Rashid 2021, https://consensus.app/papers/details/w:b46a79c7-ce51-4842-a024-549640291ba4/ |
| COC vs glass (µFFE, flow) | protein peak broadening ~20 s on COC vs minutes on glass → lower adsorption on COC | V-sec / med | Douma 2023, https://consensus.app/papers/details/w:3e7e8ed2-2ca7-4d53-89ee-a2429fbd128c/ |
| COC + amphiphilic PEG/NHS adlayer | "very low" IgG NSA vs bare COC; sandwich LOD 1–10 ng/mL | V-abs / med | Sung2011, doi:10.1016/j.bios.2011.03.005 |
| COC silanised (APTES + PDITC) | human IgG sandwich LOD 0.1 ng/mL, RSD 15 % | V-abs / high | Raj2009, doi:10.1016/j.bios.2009.01.026 |
| PDMS + Pluronic F127 (bulk-embedded, migrates to surface) | "significantly" reduced protein NSA (number not in abstract) | V-abs / low | Wu2009, doi:10.1039/b901651a |
| PDMS + PDMS-PEG / zwitterionic surface-segregating additives | albumin, lysozyme, IgG NSA reduced; hydrophilicity kept 20 months (PEG) / 6 months (zwitterionic, 0.025 wt %) | V-sec / med | Gökaltun 2019, https://consensus.app/papers/details/w:da8a5309-de7d-4697-81c6-2d8e1d34da51/ ; Gökaltun 2023, https://consensus.app/papers/details/w:0a5f0698-09a9-42b3-b005-126d122421b9/ |
| PDMS/quartz: F108, PLL-PEG, DDM/MC | dynamic DDM/MC and F108 best; static F108 as good as dynamic | V-sec / med | Viefhues 2011, https://consensus.app/papers/details/w:89d0a7c1-0932-48c0-91ce-6006492445f1/ |
| PEGylated magnetic PGMA beads | PEG 30 kDa: −45 % protein NSA, −74 % cells; less adhesion to PDMS and COC walls | V-abs / high | Kucerova2014, doi:10.1016/j.msec.2014.04.011 |
| ALP adsorption kinetics on device surfaces | transport-resolved adsorption model applied to ALP and GOx (rate constants not in abstract) | V-abs / low | Jenkins2004, doi:10.1016/j.ab.2004.03.072 |
| Non-passivated PDMS with phase separation | bead transfer between two networks gave 100 pg/mL without any passivation | V-abs / high | Herrmann2007 (§1) |
| PEEK | no quantitative protein-adsorption data for PEEK microfluidics found in this session | — | — |

### 5.2 Reading (with a derived scale check)
* Best "non-fouling" surfaces are quoted at **< 0.3 ng/cm² (< 3 pg/mm²)** — the SPR detection limit, measured with
  mg/mL protein. Derived: 3 pg/mm² of a ~290 kDa IgG–ALP conjugate ≈ 6×10⁶ molecules/mm² (derived, low). The
  1 pg/mL signal in docs/05 is ~10⁵ bound labels. **SPR-grade "ultralow fouling" therefore cannot certify the
  conjugate NSB this project needs**; it must be measured at assay level, at the working conjugate concentration
  (0.3 nM), on the actual wetted area (inference; consistent with docs/01 §d).
* Relative numbers transfer better than absolute ones: coatings cut NSA by 45–96 % (Kucerova, Xian, Liu 2016), i.e.
  ≤ ~25×; the Rissin/Chang NSB floor (docs/01) was reached by low label concentration, not by surface chemistry.
* Architectural lever with the best evidence: **keep the conjugate-exposed wall area out of the signal volume**
  (Herrmann2007 two networks; Rusling capture → detection chamber; Wang2013 bead transfer). Then wall NSB only
  matters if wall-adsorbed conjugate desorbs or is swept into the readout.
* COC/COP and PEG- or zwitterion-coated surfaces are the usual best candidates; PDMS needs bulk additives or
  parylene and absorbs small hydrophobic molecules (§8) — relevant to HQ/BQ carry-over.

---

## 6. On-board reagent storage and commercial cartridge architectures

### 6.1 Storage and release

| Item | Finding | Verif. / conf. | Source |
|---|---|---|---|
| Review | Methods to integrate and release dry and liquid reagents in microfluidics (active, passive, hybrid) | V-abs / high (qualitative) | Hitzbleck2013, doi:10.1039/c3cs60118h |
| Inkjet-spotted dry reagent integrators | ~100 pg HRP and 450 pg labelled dAb reconstituted into ~5–30 % of a 1 µL sample, footprint < 1 mm² | V-abs / high | Hitzbleck2011, doi:10.1039/c1lc20282k |
| Spotted dAb + Dean mixer | 10.6 nL spot; asymmetric release: 83 % of dAb in one half of the stream before the mixer, 52 % after a 9-loop Dean mixer — i.e. **dried-reagent release is not homogeneous without mixing** | V-abs / high | Gervais2011, doi:10.1016/j.bios.2011.06.016 |
| Dry HRP conjugate | ~80 % activity after > 5 months at 45 °C; DAB substrate no loss over 3 months at 45 °C | V-abs / high | Ramachandran2014, doi:10.1039/c3an02296j |
| Freeze-dried ALP | activity lost at 37/45 °C with humidity over 12 months; **fluctuating temperature worse than constant high temperature**; residual moisture 0.4 % (treated stoppers) vs 1–4 % (untreated) | V-abs / high | Ford1994, doi:10.1006/biol.1994.1026 |
| Immuno-functionalised chip surfaces | multilayer immunochemistry stabilised for up to 6 months at room temperature | V-abs / high | Asghar2016, doi:10.1038/srep21163 |
| Lyophilised PCR reagents in chip | used routinely in microfluidic PCR (Wang2021) | V-abs / med | doi:10.3390/mi12040384 |
| Liquid blister pouches | burst force 25–35 N depending on foil; **shelf life depends strongly on reagent–foil combination**; metering structure needed | V-sec (search summary of abstract) / med | Smith 2016, Microfluid Nanofluid, doi:10.1007/s10404-016-1830-2 |
| pAPP solution stability | vendor: prepare same day; −20 °C ≤ 1 month. **No peer-reviewed non-enzymatic hydrolysis rate found** (same gap as docs/01) | V-vendor / low | https://hellobio.com/4-aminophenylphosphate-sodium-salt.html |
| HQDP hydrolytic stability | "excellent" (Wilson2004) | — | docs/01 |
| Bead suspension in liquid reservoir | no quantitative on-cartridge bead-settling or dose-drift data found (see §2) | — | — |

### 6.2 Commercial architectures — what they teach

| System | Capture | Reagent storage | Detection | Lifetime | Lesson | Verif. / conf. | Source |
|---|---|---|---|---|---|---|---|
| Gyrolab | 15 nL SA-particle column per structure; biotin-capture loaded each run; centrifugal flow | reagents from a microplate (not on CD) | fluorescence | single-use CD (up to 104 assays/CD/50 min) | fresh nL bed per sample; brief contact; pg/mL only with larger sample (4 µL) | V-abs + V-vendor / med | doi:10.1373/clinchem.2005.053348; Gyros PIS (above) |
| Ella / Simple Plex | Ab-coated glass nano-reactors, triplicate per channel | on-cartridge reagents (details not in abstracts read) | fluorescence | single-use cartridge | glass + small fixed reactors; vendor pg/mL, 90 min | V-abs / low (numbers vendor) | doi:10.1111/aji.12512 |
| Simoa (Quanterix) | beads, fL wells on disc | instrument reagents | digital fluorescence | single-use disc | sub-fM requires single-enzyme counting + low label conc. | V-abs / high | doi:10.1039/c3lc50416f; docs/01 |
| i-STAT cTnI / hs-TnI | Ab on Si-chip sensor (cTnI) → **Ab on paramagnetic microparticles** (hs-TnI); ALP conjugate **dried on chip** | **substrate (aminophenyl phosphate) carried in the wash fluid** | amperometric (ALP product) | single-use; ~16–22 µL; 14–15 min | ALP + amperometry + dry conjugate + liquid substrate/wash pack is a mass-produced pattern | V-vendor (FDA 510(k) summaries via search) / med | https://fda.innolitics.com/device/K031739 ; https://fda.innolitics.com/device/K240984 |
| Philips Minicare (Magnotech) | 500 nm magnetic labels, one-step, electromagnets above/below | dry reagents on board | FTIR optics | single-use | magnetic actuation replaces washing; 5 min, ~1 pM cTnI | V-abs / high | doi:10.1016/j.cca.2010.03.001 |
| GenMark ePlex | DNA capture probes on Au electrodes | — | AC voltammetry of ferrocene labels; **electrowetting on PCB** | single-use | DMF + EC on PCB is manufacturable | V-vendor (FDA K163652 via search) / med | https://fda.innolitics.com/device/K163652 |
| GeneXpert (patents only) | magnetic/solid-phase capture | radial chambers around a central syringe barrel, instrument-driven **rotary valve** | optical PCR | single-use | one rotary valve + one syringe addresses all chambers | V-sec (patent search summary) / low | e.g. https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9050594 |

**Reading.** Every commercial system found with pg/mL-class or ALP-amperometric immunoassay uses a **single-use**
cartridge/disc with a fresh capture surface. The two recurring storage patterns are: (a) **dry conjugate on the
chip + liquid substrate/wash in a pack** (i-STAT; Philips dry reagents), and (b) **reagents held in the instrument**
with a disposable capture microstructure (Gyrolab, Simoa). No multi-run cartridge with an on-board *liquid* bead
suspension was found. Dried ALP is sensitive to humidity and temperature cycling (Ford1994); dried HRP conjugates
survive 5 months at 45 °C (Ramachandran2014).

---

## 7. On-chip valving

| Valve type | Data | Bead/protein suitability | Verif. / conf. | Source |
|---|---|---|---|---|
| Multilayer soft-lithography (Quake) PDMS valves and pumps | device area > 100× smaller than Si valves (numbers on dead volume/leak not in abstract) | PDMS NSB and small-molecule absorption (§5, §8) | V-abs / high | Unger2000, doi:10.1126/science.288.5463.113 |
| Monolithic membrane valves (Mathies; PDMS membrane between glass) | normally closed; latching versions held by 120 ms pulses for minutes; n pneumatic lines → 2^(n−1) valves | glass channels; membrane is the only PDMS | V-abs / high | Grover2006, doi:10.1039/b518362f |
| Same with FEP Teflon membrane | chemically inert, "maintain performance over extended use" | best chemical inertness found | V-abs / med | Grover2008, doi:10.1039/b800600h |
| Valve lifetime | ≥ 10⁶ actuations without failure reported for a PDMS valve (thick-membrane design) and for other elastomer/3D-printed membranes | — | V-sec (search summary) / low | https://mdpi.com/2072-666X/16/6/657 ; https://engrxiv.org/preprint/download/8053/13066/11320 |
| Wax-coated PDMS peristaltic valves | no degradation after multiple open/close cycles; gas-tight | — | V-abs / med | Ren2010, doi:10.1021/ac100830t |
| Pressure-valved "fluidic bridges" for bead transfer | bead transfer between networks | **beads pass a valve region in a magnetic field, not in flow** | V-abs / high | Herrmann2007 |
| Pinch valves on polymer cartridges | automatic fluid sealing (Do2008 polymer LOC); two pinch-valve manifolds driving a sealed all-in-one PCR cartridge (Xu2010) | robust; actuator in instrument | V-abs / med | doi:10.1039/b811169c; doi:10.1039/c005265e |
| Centrifugo-pneumatic valve | burst 8.5 ± 0.6 to 27.9 ± 2.0 Hz depending on surface tension (0.01–10 % detergent, ethanol) — **detergent shifts the burst point** | single-use | V-abs / high | Mark2009, doi:10.1039/b914415c |
| Capillary soft valve | capillary barrier "a few kPa", 0.6 mm² footprint, opened by pressing the soft cover | single-use | V-abs / high | Hitzbleck2012, doi:10.1039/c2lc00015f |
| Rotary valve + syringe (GeneXpert-type) | instrument-actuated rotary valve on the cartridge | used with magnetic/solid-phase capture in commercial cartridges | V-sec (patents) / low | §6.2 |
| Blister + frangible seal | 25–35 N burst | single-use | V-sec / med | Smith2016 |

**Reading.** For a cartridge that must pass protein and bead suspensions repeatedly, the evidence favours
(i) valves whose wetted part is a glass/thermoplastic seat with an inert membrane (Mathies/Grover FEP), or
(ii) instrument-side pinch or rotary actuation of a thermoplastic cartridge; and **moving beads by magnet across a
valve rather than pumping bead slurry through it** (Herrmann2007, Wang2013). Burst/capillary valves are one-shot and
detergent-sensitive (Mark2009), so they suit single-use cartridges only. No study found reports bead-induced valve
leakage or protein fouling of valve seats quantitatively — a gap for a multi-run design.

---

## 8. Carry-over in reusable microfluidic channels

| Setting | Carry-over number | Verif. / conf. | Source |
|---|---|---|---|
| Bead transfer by magnet between wells through a tapered channel | DiFMUP substrate carried with beads < 0.002 % (2×10⁻⁵) | V-abs / high | Wang2013, doi:10.1039/c3an01166f |
| PDMS channel, hydrophobic dye TMR, 4 min exposure then 4 min wash | residual < 2×10⁻⁵ of initial concentration; desorption time constants 10–42 s; TMR adsorbs up to 4× more on PDMS than glass/PS | V-sec / high | Li 2009 SLAS Discov., https://consensus.app/papers/details/w:d54c363f-6e52-4f67-875f-a07db8d39054/ |
| Parylene-C PDMS, BSA, 60 min wash | residual 4.5 % of pristine-PDMS residual (relative only) | V-sec / med | Liu 2016 (§5) |
| Gravity siphon multistep ELISA | "no reagent overlap or carry-over" (qualitative) | V-abs / low | Reis2021, doi:10.1021/acssensors.1c01524 |
| Protein A/G IgG microseparation cassette | "minimal matrix carry-over" (qualitative) | V-abs / low | Porycka2026, doi:10.1016/j.talanta.2026.129682 |
| Regenerated in-channel immunosorbent (µFIA) | 51 cycles, no carry-over number | V-abs / low | Uthuppu2015 |

**Reading.** The project criterion (residual ≤ 1×10⁻⁴ after a 10 ng/mL challenge, i.e. ≤ 1 pg/mL-equivalent,
derived) has **no direct precedent for a reusable immunoassay channel** in the sources found. The only quantitative
≤ 10⁻⁴ numbers are for small molecules (bead-transfer 2×10⁻⁵; PDMS wash 2×10⁻⁵ for a dye that PDMS absorbs). For
protein/conjugate, adsorption–desorption on the wall (Liu 2016: tens of % of adsorbed BSA remains after 60 min
washing on PDMS) means wash-only carry-over control is unlikely to reach 10⁻⁴ on elastomer surfaces (inference,
low). Single-use capture/readout elements avoid the question; a multi-run cartridge needs its own E-level
measurement.

---

## 9. Synthesis

### 9.1 What has actually shown ≤ 1 pg/mL-class performance (any analyte) with ≤ 60 min and ≤ 100 µL

| Combination | LOD | Time / volume | EC? | Caveats | Source |
|---|---|---|---|---|---|
| Magnetic beads with ~10⁵–10⁶ HRP labels, captured in a stirred chamber, transferred to an Ab-coated AuNP sensor array (Rusling) | 5–50 fg/mL cytokines (≈ 0.2–2 fM), 150 aM PTHrP | 30–50 min / 5 µL serum | yes (amperometry, HRP) | two-surface format; single-use arrays; massive labels; small analytes; blank statistics not in abstracts | Otieno2014, Malhotra2012, Krause2015, Otieno2016 |
| CPG packed channel + SA-ALP / pAPP on Au | IL-6 1.56 pg/mL (≈ 74 fM) | time not in abstract | yes (ALP) | ~10× above target in molar terms for IgG-equivalent | Messina2008 |
| Simoa digital ELISA on disc | sub-fM | hours (docs/01 version) | no (optical) | label counting; in docs/01 | Rissin2010/2013 |
| Fixed SA bead bed (Gyrolab) / glass nano-reactor (Ella) | ~10–30 pg/mL (Gyrolab, 200 nL); vendor sub-pg/mL (Ella GFP, 90 min) | single-use, nL–25 µL | no | vendor numbers | Honda2005; vendor |
| One-step magnetic nanoparticle labels (Philips) | ~1 pM cTnI in 5 min | finger-prick | no (optical) | 3 orders above target | Dittmer2010 |

**No source found demonstrates the project's exact combination** — enzyme (ALP) label, IgG analyte (150 kDa,
anti-human-IgG reagent pair), electrochemical readout, ≤ 1 pg/mL (6.7 fM), ≤ 60 min, ≤ 100 µL, on an integrated
cartridge, with a blank-based LOD. The closest are the Rusling arrays (EC, fM, 30 min) and Messina2008 (ALP/EC,
1.6 pg/mL IL-6).

### 9.2 Best-evidenced design patterns
1. **Fresh capture surface per determination** (beads or a nL bed/reactor loaded each run): used by every
   commercial high-sensitivity cartridge found (Gyrolab, Ella, Simoa, i-STAT, Minicare). Regeneration on chip has
   ≤ 51 cycles of evidence and none at pg/mL.
2. **Separate the binding compartment from the signal compartment and move beads, not liquid** (Herrmann2007,
   Rusling capture → detection chamber, Wang2013 bead drag with 2×10⁻⁵ carry-over, Philips magnetic wash).
3. **Stopped-flow readout in a nL–µL volume with redox cycling**: IDA gains 4–65× (µm gaps) up to 10²–10³ (nanogaps),
   largely lost under flow (37 → 4 at 500 nL/s). pAP films nanogap IDAs; HQ (Wilson2004) is the better reused-electrode
   product.
4. **Dry conjugate on board + liquid substrate/wash from a pack or the instrument** (i-STAT), with an explicit mixing
   element after reconstitution (Gervais2011: release asymmetry 83 % → 52 %).
5. **Trap at low flow or with field-focusing structures**: single-magnet chamber traps drop from ~92–95 % at 5 µL/min
   to ~16–21 % at 20 µL/min (4.5 µm beads); soft-magnetic beds/tracks raise capture several-fold.
6. **Inert valve seats and instrument-side actuation** (Mathies membrane valves with FEP; pinch/rotary valves);
   avoid pumping bead slurry through valves.

### 9.3 Still undemonstrated (gaps for docs/05 follow-up / bench)
* A **multi-run cartridge with on-board liquid bead suspension** (settling, dose drift over hours/days): no data.
* **Carry-over ≤ 10⁻⁴ for protein/conjugate** in a reusable microchannel: no data; only small-molecule 2×10⁻⁵.
* **Conjugate NSB at assay concentration** on COC/COP/glass with PEG/zwitterion/BSA passivation, expressed as
  analyte-equivalent: no data at pg level; SPR "ultralow fouling" (< 3 pg/mm²) is ≥ 10× too coarse (derived).
* **HQDP/HQ on an IDA in a chip immunoassay**; long-term stability of thin-film Ag/AgCl in Cl⁻-variable buffers
  (best found: < 2 mV over 26 days, GO-coated, constant medium).
* **Non-enzymatic hydrolysis rate of pAPP/HQDP** in on-board liquid storage at 4 °C and RT: still no peer-reviewed
  numbers (also open in docs/01).
* **Valve lifetime with bead/protein media**: lifetime figures (~10⁶ cycles) exist only for clean liquids and are
  secondary-source.
* Monolith/bead-bed **regeneration loss per cycle for a sandwich IgG assay**: not found.

### 9.4 Implications for the open choices (inference, to be tested)
* **Chip lifetime:** the literature supports a **single-use capture/readout element** (bead dose or fresh nL bed per
  run) inside a longer-lived cartridge or docking station; a permanent regenerated capture surface has the weakest
  evidence. A multi-run cartridge is defensible only if beads are dry-stored or agitated and if carry-over is
  measured.
* **Detector:** IDA redox cycling gives a real gain (4–65× at µm gaps) only in stopped flow; a single WE in a
  quiescent µL chamber plus long accumulation may be nearly as good when the substrate blank, not the electrode,
  limits (docs/01 reading of FIA LODs; inference).
* **Reagent strategy:** dry conjugate on board (with a mixer) + liquid HQDP pack follows the i-STAT pattern; bead
  dosing from liquid needs agitation (acoustic or magnetic resuspension has been shown on disposables).
* **Parallel/staggered incubation:** Gyrolab-style parallel structures and Rusling multi-chambers show it is
  practical; no source addresses timing bias between staggered cartridges (docs/05 §4.3 finding stands).

## References (located in this session)
All DOIs and URLs are given inline in the tables above; keys are first-author + year. Consensus records:
https://consensus.app/papers/details/… links as listed. Search engines used: PubMed (E-utilities), Consensus,
WebSearch (2026-11-12).
