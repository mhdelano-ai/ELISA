# 11 — Second-generation cartridge: fabrication, component and vendor survey

Status: survey written 2026-11-12. Work in progress, extended section by section. It does not change any decision in
docs/00–08.

**Scope.** A microfluidic cartridge that does everything after the SM-FL outlet:
* incubation chamber (~220 µL working, docs/05 §4.1);
* bead trap (~2 µL);
* detection cell (sub-µL; single thin-film WE or IDA);
* on-chip valving;
* on-board bead and conjugate reagents.

It sits in a custom docking station. The station may hold pressure controllers, syringe pumps, magnets, Peltier
cooling, pogo contacts and valve actuators. Three choices stay open: fabrication route, chip lifetime and detector
type. This document is meant to inform them.

**Sourcing.** Every vendor statement carries a source tag (§9) and a confidence:
* **H** = read on the vendor's own page or datasheet this session;
* **M** = read on a reseller or distributor page, or in a search summary of the vendor's page;
* **L** = trade press or an old or indirect source.

Engineering judgements are marked **[assessment]** and numbers computed here **[derived]**. Anything not checked this
session is **UNVERIFIED**. Prices are as displayed on the date of reading, excluding tax.

**Limits of this session.** The web-search quota ran out partway through. micronit.com returned HTTP 429 on every
attempt, so Micronit's own design rules were not read; only reseller listings were. Gaps are listed in §8. After the interruption the survey continued with WebFetch on vendor pages and PubMed, and
§1–§6 were extended.

---

## 0. What the cartridge must do (from docs/05 §4.1 and docs/07 §5), restated as chip requirements

| Function | First-generation implementation | Chip requirement [derived from docs/05/07] |
|---|---|---|
| Sample inlet | SM-FL outlet → V4 → cup, 100 µL/min | 1/16″ OD or 360 µm capillary port. Downstream pressure is low: the cup is vented, and the cell outlet is open to waste through ≤ 0.35–0.7 MPa of tubing (docs/02 §5.1). A port rating of **≥ 0.5 MPa** is ample [assessment]. |
| Incubation | stirred PEEK cup, 0.25–0.5 mL working, ≤ 0.8 mL total, vented | Chamber of 250–500 µL. This is large by chip standards and needs a thick (≥ 3–5 mm) chip body or a moulded "tank". Mixing is needed (SIA aspirate/dispense, stir bar or recirculation). The residual after emptying must be ≤ 2 µL, and residual beads after rinses ≤ 10⁻³ of the dose. |
| Bead trap | 1.5 mm ID × 1.1 mm magnet zone, ≈ 2 µL; wall ≤ 0.5 mm | Chamber of ≈ 1–2 µL. The lid or floor must be **≤ 0.5 mm thick** on the magnet side, so a 100–200 µm foil lid (§1.2) is ideal. Magnet: NdFeB on an actuator in the dock. |
| Detection | thin-layer GC cell (default) or IDA 5/5 µm, 25 µm × 0.5 mm channel, ≤ 0.5 µL | Thin-film Pt/Au on glass or Si. The channel height of 10–50 µm needs a precise spacer, gasket or etched step. The electrode sits < 1 µL downstream of the trap. |
| Reference / counter | external Ag/AgCl side arm, Pt CE downstream | Two options: an on-chip Ag/AgCl pseudo-reference (chloride must then be constant across buffers, §6.4), or a docked salt-bridge reference. CE on chip (Pt or Au film). |
| Reagents | bead reservoir (5×10⁷ /mL, stirred, 4–8 °C) and separate conjugate reservoir (6.6 nM, 4–8 °C, dark) | Per run: 10 µL beads + 10 µL conjugate. For an 8-h block of about 9–16 runs plus priming, **~0.2–0.5 mL of each** is enough [derived]. Wash buffer (A1) and HQDP substrate (B1) still come from the BSM, so they need no on-chip storage. |
| Flow | 1–300 µL/min | Cartridge flow resistance must be low enough that 300 µL/min stays below the port and valve rating (§3). |

**Main consequence [assessment].** The on-board reagent load is small (sub-mL). The fluidic difficulty is not storage
but three other things:
1. a ~0.25–0.5 mL mixed incubation chamber that drains cleanly;
2. a magnet-side wall ≤ 0.5 mm;
3. a 10–50 µm detection gap over a thin-film electrode with pA–nA readout.

These favour a **hybrid**: a polymer fluidic body with a thin foil lid, plus a glass electrode die.

---

## 1. Fabrication routes compared for this chip

### 1.1 Glass (wet-etched / laser / powder-blasted), thin-film Pt/Au electrodes

**Foundry statements**
* Dolomite (historical, L): glass and quartz chips; etch depths quoted as 100 nm–1 mm (one press item says 250 nm–300 µm); channel widths from 3 µm; layer thicknesses 150 µm–5 mm. Electrodes of Pt, Cu, Ti and Au from 2 µm, embedded between thermally bonded glass layers, with optional PECVD oxide or nitride insulation; electrodes may cover up to 50 % of the chip. Turnaround was 6–8 weeks [DOLO_PRESS, L]. **Unchained Labs has discontinued the Dolomite product line** [UL_DOLO_EOS, H], so Dolomite is not a supplier for this project.
* IMT Masken und Teilungen AG (Greifensee, CH): electrodes of Au, Pt, ITO and Ti with features down to 2 µm; nano-patterning of glass to 350 nm; an automated 200 mm glass-wafer line; in-house masks for fast prototypes [IMT_FLYER, M]. A room-temperature, "biocompatible" bonding process was developed with HEIDENHAIN (2020) [IMT_PRESS, L].
* Micrux (Oviedo, ES): makes custom thin-film electrodes on **glass wafers**:
  * Au or Pt, 150 ± 15 nm, features down to 5 µm;
  * SU-8/polyimide passivation;
  * linear or circular IDEs [MICRUX_TF, H].

  This exactly covers a 5/5 µm IDA die; a sub-5 µm gap would need IMT-class lithography. This matters because fusion-bonding glass at about 1000 °C destroys thin-film electrodes [RSC_LTBOND, M].
* Klearia (FR): all-glass chips with a low-temperature bonding process that "allows the integration of new embedded functions" [KLEARIA_MTAS, L]. Electrode capability not confirmed.
* Micronit (NL): glass lab-on-a-chip maker. Custom designs are made in a class-1000 clean room through the "Fluidic PRO" prototyping service [DARWIN_MN, M]. Electrode capability was not confirmed this session: micronit.com returned 429. A 2007 Micronit EOF kit used glass chips "with or without integrated electrodes" [MN_EOF_2007, L].

**Feature sizes.**
* Isotropic wet etch gives depth ≈ ½ the undercut, so a 10–50 µm detection gap is easy and well controlled.
* Electrode lithography to 2 µm is stated by IMT and (historically) Dolomite, so IDA 5/5 µm is comfortably inside these rules.
* Large volumes are a poor fit: a 250 µL chamber would need, for example, a 10 × 10 × 2.5 mm cavity, which is costly in glass.

**Bonding.** Fusion bonding is incompatible with metal films unless the electrodes are embedded or recessed. Low-
temperature, room-temperature or adhesive bonding is needed instead (IMT, Klearia), or a gasket clamp.

**Pressure.** Bonded glass is far above anything this chip sees. Micronit's 4515 holder is rated 100 bar, and 10 bar for
thin-bottom chips [DARWIN_FC4515, M].

**Protein and passivation.** Glass and silica accept silane-PEG and BSA blocking well [assessment; UNVERIFIED for
specific chemistry].

**Optical access.** Excellent.

**Lead time and cost class.** Weeks to months. Cost per prototype design is high (masks, wafer runs)
[assessment; foundry prices not seen].

**Scale-up.** Wafer-level (200 mm at IMT). The per-chip cost of a large-area glass chip stays high.

**Fit [assessment].** Best for the **electrode die** (small, about 10 × 6 to 15 × 45 mm). Poor for the
incubation chamber and reagent tanks.

### 1.2 Injection-moulded or milled COC/COP (and PC, PS, PMMA, PP, TPE) with foil lids

**microfluidic ChipShop (Jena, DE)** [CS_FAB, H]:
* Prototypes are milled from a single piece in PMMA, COC, COP, PS and others. Milled surface roughness ≈ 1 µm.
* Injection moulding uses ultra-precision-milled inserts, in ISO class 7 clean rooms. Materials: COC, COP, PC, PS, PMMA, PP and **TPE**. Moulded roughness < 50 nm RMS. **Typical minimum order: 100 chips.**
* In-house bonding of same-type polymers, hybrid elements and multi-layer stacks.
* **Sensors, electrodes, valves, filtration membranes and biosensors can be integrated** as hybrid elements.
* Blisters of 50–750 µL; dry reagents (lyophilised pellets, dried spots, beads); spotting to pL.
* Formats: microscope slide, double slide, microtiter plate and wafers. No credit-card format is listed on that page.

**ChipShop standard formats** [CS_EXPLAINED, H]:

| Format | Dimensions |
|---|---|
| Microscope slide | 75.5 × 25.5 mm, "various thicknesses" |
| Double slide | 75.5 × 50 × 2 mm |
| Microtiter plate | 85.48 × 127.76 mm |
| Extended platforms I / II | 95.5 / 141 × 16 × 1.5 mm |
| CD | 120 mm × 1.5 mm |
| Diagnostic Platform (Dx) | 135.68 × 67.04 mm |
| Handheld | 104 × 25.5 mm |

Materials: PMMA, PC, PS, COC and COP (Zeonor/Zeonex), plus borosilicate glass and Glassomer. TPE and PP are used
for connectors, plugs and tanks.

**Chip-to-world interfaces and their internal volumes** [CS_EXPLAINED, H]:

| Interface | Pitch | Height | ID | Internal volume |
|---|---|---|---|---|
| Mini Luer | 4.5 mm | 2.5 mm | 2.64 mm | **16.5 µL** |
| Luer | 9 mm | 4 mm | 4.18 mm | 53 µL |
| Olive | — | 4 mm | 1 mm | 2.5 µL |
| Through-hole | — | — | 1.4 mm | **0.6 µL** |

**[assessment]** The internal volumes matter:
* A Mini Luer port holds 16.5 µL, more than the whole trap-to-cell path.
* On the bead and product path use through-holes with a dock-side compression seal, or olive interfaces.
* Reserve (Mini) Luer for reagent filling ports.

**ChipShop catalogue dimensions** [DARWIN_CS4CH, M]: a moulded 4-channel chip has widths of 20–1000 µm and depths of
20–200 µm, with a foil lid of 175 µm (PMMA) or 140 µm (COC). Other lids [CS_1367, CS_155, H]:
* Topas foil 100 µm, Tg 84 °C (membrane-valve chip);
* COP foil 188 µm, Tg 136 °C (turning-valve chip).

**Generic moulding rules** (another vendor, Vantiva PBD guide [VANTIVA_GUIDE, M]):
* machined inserts: minimum width 50 µm, depth 50–500 µm, vias ≥ 0.5 mm, draft 3–7°;
* lithographic inserts: width 5 µm, depth 5–150 µm.

**Electrode integration options [assessment]:**
* (a) **Glass or Si electrode die** bonded or clamped into a pocket of the polymer body (the hybrid of §1.6). This is the only route here that gives lithographic 5 µm IDA quality.
* (b) Thin-film Au/Pt sputtered directly onto COC through a shadow mask or lift-off. Adhesion and annealing are limited by Tg (78–180 °C depending on grade, UNVERIFIED range), and IDA ≤ 10 µm on polymer is rarely offered.
* (c) Screen-printed carbon/Ag/AgCl on the foil lid. Resolution about 100 µm (UNVERIFIED), so suited to WE/CE/RE pads but not IDAs. Lot-to-lot WE variance adds to blank SD (docs/02 §5.1).

**Bonding.** Thermal or solvent-vapour bonding of COC foil to COC body; adhesive tape for prototypes. With adhesive
tape the final depth is the moulded depth plus the tape thickness, and the minimum width cut into tape is 200 µm
[DARWIN_CSTAPE, M].

**Pressure.** ChipShop's membrane-valve chip holds 3 bar inlet pressure [CS_1367, H]. ChipShop's TPE connector set is
quoted at 3.2 bar on a reseller page [DARWIN_FCPRO, M]. That is ≥ 0.3 MPa, enough for this low-pressure,
downstream use [assessment].

**Protein, Tween and HQ compatibility:** see §6. COC/COP are hydrophobic and adsorb protein unless blocked (BSA,
Tween, PEG). ChipShop offers hydrophilisation and silanisation/biofunctional coatings on request [CS_FAB, H].

**Optical.** COC/COP are highly transparent [assessment], which allows a TUV/fluorescence check of the trap.

**Lead time and cost.** Milled prototypes start from one piece (time not stated). Moulding has a 100-chip MOQ
plus insert cost (price on request).

**Scale-up.** This is the **standard IVD cartridge route**: same materials from milled prototype to moulded
part. The 250 µL chamber and sub-mL tanks are easy in a 3–6 mm moulded body [assessment].

### 1.3 PMMA laminate / CNC prototypes (laser-cut layers, adhesive or solvent bonding)

* Potomac Photonics / Goodfellow (US): its "Fast Track" PMMA programme guideline is a minimum channel width of 50 µm and maximum depth of 200 µm, with custom work outside it [DATRON_POTOMAC, M]. Marketing states features down to 1 µm (laser micromachining, unspecified material) and hot-embossing moulds (COC, PMMA, PS, PE) within 24–48 h of the design file. Laser micro-welding is also offered [GOODFELLOW_MF, H].
* **Strengths [assessment]:** days-scale iterations; thick layers make tanks, chambers and magnet pockets easy; a 175–250 µm lid gives a thin magnet wall.
* **Weaknesses [assessment]:**
  * PMMA swells or crazes with some solvents (not an issue here);
  * HQ/BQ partitioning into PMMA and pressure-sensitive adhesive is not quantified (§6);
  * pressure-sensitive adhesive layers creep, which poorly defines a 25 µm detection gap;
  * laser-cut walls are rough.
* **Fit:** rapid first prototypes of the incubation, trap and valve layout, with a clamped glass electrode die (Micrux chip, §2.3) for detection.

### 1.4 PDMS-on-glass (prototype only)

* uFluidix (CA) supplies PDMS and glass devices with expertise in bonding PDMS to slides and cover slips [UFLUIDIX_EE, L].
* **Strengths [assessment]:** Quake-type pneumatic valves are trivial; plasma bonding onto a glass electrode die is easy; prototypes take days.
* **Disqualifying weaknesses for this assay [assessment; mechanism UNVERIFIED for HQ/BQ specifically]:**
  * small hydrophobic molecules partition into PDMS (§6.2);
  * O₂ permeability is high (§6.5);
  * uncured oligomers leach;
  * proteins adsorb.
* HQ is fairly polar (log P ≈ 0.6, UNVERIFIED), so loss may be small. BQ is less polar, and with redox cycling BQ must reach the collector.
* **Use only** for valve and flow-pattern studies with dye and beads, not for LOD-relevant electrochemistry.

### 1.5 3D-printed manifolds

* No 3D-printing service page was read this session (search quota exhausted). Capabilities, resins and resolution are **UNVERIFIED**.
* **[assessment]** SLA/DLP resins can give ~100 µm channels. Their leachables and protein/HQ adsorption are poorly characterised, so print only the **dock-side manifold and tank holders**, not wetted assay surfaces near the trap or electrode.

### 1.6 Hybrid: polymer fluidic body + glass (or Si) electrode die

* Combines a moulded or milled COC/COP body (chamber, trap, valves, reagent tanks, ports) with a 5/5 µm Pt/Au IDA or
  thin-film WE/CE (and optional Ag/AgCl) on glass.
* ChipShop states hybrid-element bonding and electrode integration [CS_FAB, H] and catalogues "Sensor Integration Chips"
  (Topas, PMMA), including turning-valve sensor platforms (Fluidic 673, 1156, 1737) and "Large sensor integration
  area" chips (Fluidic 1004, 1012) [CS_SENSORCHIPS, H — names only; dimensions not read].
* The detection gap is set either by a moulded step in the polymer body over the die or by a laser-cut film spacer
  (docs/07 §5.3 uses a 25 µm PET/PTFE gasket).
* The die can be **permanent in the dock** (the cartridge docks onto it with a gasket) or **bonded into each cartridge**.
  This is the main architectural fork (§7).

---

## 2. Foundries and catalogue parts

### 2.1 Foundries — what they state

| Foundry | Materials / processes stated | Electrodes | Formats / interfaces | Source, conf. |
|---|---|---|---|---|
| **microfluidic ChipShop** (DE) | Milling (PMMA, COC, COP, PS); injection moulding (COC, COP, PC, PS, PMMA, PP, TPE); ISO 7; MOQ 100 moulded | Integrated as hybrid elements (sensors, electrodes, valves, membranes) | Slide, double slide, microtiter plate, wafer; luer, mini-luer and olive interfaces on catalogue chips | CS_FAB, CS_1367, CS_155 (H) |
| **Micronit** (NL) | Glass (borosilicate) chips; Fluidic PRO custom service in a class-1000 clean room | not confirmed this session (2007 EOF kit with electrodes, L) | Functional glass element 45 × 15 mm on catalogue chips (M); topconnect/sideconnect holders | DARWIN_MN, DARWIN_SERP (M) |
| **IMT AG** (CH) | Glass/quartz, 200 mm wafer line, room-temperature bonding | Au, Pt, ITO, Ti, features ≥ 2 µm | custom | IMT_FLYER (M), IMT_PRESS (L) |
| **Klearia** (FR) | All-glass, low-temperature bonding, "embedded functions" | not confirmed | custom | KLEARIA_MTAS (L) |
| **Dolomite** (UK) | Glass; electrodes ≥ 2 µm Pt/Au/Ti/Cu (historical) | — | — | **Product line discontinued** (UL_DOLO_EOS, H) |
| **uFluidix** (CA) | PDMS, glass | not confirmed | slides, cover slips | UFLUIDIX_EE (L) |
| **Potomac / Goodfellow** (US) | Laser micromachining, hot embossing (COC, PMMA, PS, PE), laser welding | not stated | custom | GOODFELLOW_MF (H), DATRON_POTOMAC (M) |
| **Citrogene** | not read this session | — | — | UNVERIFIED |
| **Micrux** (ES) | Thin-film electrodes on glass, PMMA/PEEK cells | Pt/Au 150 nm on 50 nm Ti; IDA to 5/5 µm | 10 × 6 mm chips; AIO platform | §2.3 |
| **Micrux — custom services** (ES) | Custom thin-film electrodes: Au or Pt only, **glass wafers**, features down to **5 µm**, thickness 150 ± 15 nm, **SU-8/polyimide passivation**, linear or circular IDEs; microfluidics: SU-8 on 4″ Si moulds (5 µm min, up to 300 µm single layer, ≤ 2 layers) for PDMS/hot-embossing replication; lead times not stated ("fast") | Au, Pt | custom | MICRUX_TF, MICRUX_MF (H) |
| **Metrohm DropSens** (ES) | Screen-printed and thin-film IDE electrodes; wall-jet flow cells | Au/Pt IDE 5 and 10 µm | §2.3 | METROHM_FLWCL_IDE (H) |

### 2.2 Catalogue fluidic chips that could be reused for breadboarding

| Part | What it is | Stated specs | Price (excl. tax) | Source, conf. |
|---|---|---|---|---|
| ChipShop **Membrane valve chip, Fluidic 1367**, product no. 10002097 | 16 channels, one membrane valve per inlet, **mechanically** closed from below; matching actuators from memetis | tight to **3 bar** inlet; body Mcs-COC 13 (Topas), lid Mcs-foil 124 (Topas, 100 µm, Tg 84 °C); olive interfaces; single use | €42.20; €34.40 from 10; €26.10 from 100 | CS_1367 (H) |
| ChipShop **Turning valve test chip, Fluidic 155**, code 10000183 | valve bodies turned in increments by an instrument (manual actuator sold separately) | COP (mcs-COP 02, lid 188 µm) or PC (lid 175 µm); mini-luer; single use | €128.50; €79.60 from 10; €59.98 from 100 | CS_155 (H) |
| ChipShop Turning Valve Distribution Chip, Fluidic 1671 | two independent valve units | Topas | not read | CS_VALVES (H, name only) |
| ChipShop Blister test chips, Fluidic 289 / 522 / 761 | blisters 50 + 100 µL / 250 µL / 500 µL | Topas; URL numbers 202-2333, 204-2338, 205-2340 (not confirmed as order numbers) | not read | CS_BLISTER (H for volumes; M for numbers) |
| ChipShop Sensor Integration Chips (Fluidic 864, 1005, 862, 1004, 1012, 673, 1156, 1737 …) | platforms for inserting sensors; some with turning valves | Topas or PMMA; dimensions not read | not read | CS_SENSORCHIPS (H, names only) |
| Micronit **Fluidic Connect 4515 chip holder**, MN-11006677 | holder for 45 × 15 mm topconnect glass chips | 6-32 flat-bottom ports for 1/16″ OD; **100 bar** (10 bar thin-bottom chips); 316 stainless; 80 × 55 × 9.5 mm | US$2,000.10 (Darwin) | DARWIN_FC4515 (M) |
| Micronit **Fluidic Connect Pro** holder | Load'n'Seal holder for topconnect chips; 1/16″ or 1/32″ tubing | cartridge MN-11006689; OOC MN-11000750; flow-cell MN-11000746 | US$2,000.10; $2,625.50; $2,743.50 (Darwin) | DARWIN_FCPRO (M) |
| Micronit serpentine microreactor (topconnect) | glass, functional element 45 × 15 mm; 0.3, 1.86 or 15.2 µL | — | not read | DARWIN_SERP (M) |

### 2.3 Catalogue electrode dies (detection)

| Part | Geometry | Notes | Source, conf. |
|---|---|---|---|
| Micrux **MX-ED-IDA1-Pt / -Au** | 10 µm fingers / 10 µm gaps, 15 (pairs) | thin-film IDA, glass | BASI_IDA (H) |
| Micrux **MX-ED-IDA5-Pt / -Au** | 10 µm / 5 µm; **Pt listed with 50, Au with 20** | PalmSens lists "20 pairs 10/5" — discrepancy; confirm before ordering | BASI_IDA (H), PALMSENS_IDA (M) |
| Micrux **MX-ED-IDA6-Pt / -Au** | **5 µm / 5 µm, 30** | closest catalogue match to docs/05's 5/5 µm × 50 × 1 mm | BASI_IDA (H) |
| Micrux IDA family (general) | Au or Pt 150 nm on 50 nm Ti; glass; support **10 × 6 mm**; two individually addressable arrays; Au RE and CE on chip; "one of the Micrux cells is necessary to connect" | price on request | PALMSENS_IDA (M; reseller page) |
| Micrux MX-ED-IDE1-Pt | 10/10 µm, 90 pairs (IDE, not two-comb IDA for redox cycling) | — | BASI_IDE (H, via search summary: M) |
| Micrux ED-IDRA1-Pt/-Au | radial IDA; compatible with Drop, AIO and Multi8x AIO cells | — | DI_IDRA (M) |
| Micrux **AIO platform** | thin-film base 60 × 40 × 30 mm, aluminium base and methacrylate cover; **flow add-on in PMMA or PEEK** (ref. MX-ED-AIO-ADD-ON-FC-PMMA per search summary) | channel volume not found | PALMSENS_AIO (M), DI_AIO (M) |
| Metrohm DropSens **DRP-FLWCL-IDE** | methacrylate **wall-jet** flow cell, magnetic closure, fittings included; for G-IDEAU10, G-IDEAU5, G-IDEPT10, G-IDEPT5, G-IDECONAU10, G-IDECONPT10; Teflon version DRP-FLWCL-IDE-TEF | volume and price not listed ("request quote"). Wall-jet is not the thin-layer geometry the model assumes [assessment] | METROHM_FLWCL_IDE (H) |
| DropSens G-IDEPT5 | 5 µm lines and gaps, Pt, glass | — | search summary (M) |

**[assessment]** For a second-generation cartridge the Micrux 10 × 6 mm glass die is directly usable as the
electrode insert of a hybrid. It is small, already has on-chip RE/CE, comes as Pt or Au, and has a 5/5 µm IDA.
It can be glued or gasketed into a pocket under a 25 µm moulded or laminated channel, with pogo contacts on its pads.
* Pad pitch and position: UNVERIFIED (needs the datasheet).
* The commercial thin-layer single-WE default of docs/08 can use Micrux single thin-film electrodes in the same
  pocket (Micrux "thin-film single-electrodes" catalogue exists [DI_MICRUX_SINGLE, L]; geometry UNVERIFIED).
* A custom 50-pair, 1 mm IDA die (docs/07 §5.3) is a standard 2 µm-rule job for a glass-electrode foundry such as IMT.

---

## 3. On-chip valves a foundry can make and a dock can actuate

| Valve type | Example seen | Actuation in the dock | Bead and protein compatibility [assessment] | Dead volume | Rated cycles |
|---|---|---|---|---|---|
| **Mechanically actuated membrane valve** (COC body, foil or TPE membrane pressed onto a seat) | ChipShop Fluidic 1367: 16 valves, closed by force from below; memetis actuators; tight to 3 bar [CS_1367, H] | plunger, solenoid or SMA actuator per valve | Good if the seat is smooth; beads can be trapped at the seat edge. Seat area low. | small (seat), not stated | not stated; the chip is "single use" → **UNVERIFIED for multi-run use** |
| **Pneumatic membrane valve** (elastomer/TPE membrane between two moulded layers; Quake-type in PDMS) | ChipShop moulds TPE [CS_FAB, H]; no catalogue pneumatic COC/TPE chip read | pressure controller (Fluigent/Elveflow, §5.1) or solenoid manifold | Good; normally-open designs avoid pinching beads | small | not stated (UNVERIFIED) |
| **Turning (rotary) valve on the cartridge** | ChipShop Fluidic 155 and 1671; sensor platforms with turning valves [CS_155, CS_VALVES, H] | rotary drive (stepper) engaging the valve body | Good for distribution; the rotor face may trap beads; sealing under repeated turns UNVERIFIED | channel-sized | not stated; single-use parts |
| **Blister + piercing seat** | ChipShop 50–750 µL blisters with piercing seat [CS_FAB, H] | plunger presses the blister | one-shot release (single-use) | — | 1 |
| **External rotary valve, cartridge-mounted** (e.g. IDEX, docs/07) | first generation | motor | proven with beads in gen-1 plan | µL | high (IDEX rated; UNVERIFIED here) |

**Literature check on thermoplastic membrane valves** (via PubMed):
* **Elastomeric COC (eCOC) membrane** valves [CHILDERS2024, H for abstract]:
  * the membrane can be extruded or injection-moulded;
  * it is UV/ozone-activated and laminated at room temperature onto PC or PETG seats;
  * the bonds held 75 kPa (PC) and 350 kPa (PETG);
  * actuated mechanically and pneumatically, "reproducibly actuated **> 50 times** without failure".
* **Polyurethane membranes** bonded to COC [GU2013, H for abstract]:
  * 3.5–24.5 µm films;
  * a PU valve still worked after 8 months where a PDMS one failed after 2 weeks (evaporation through PDMS);
  * creep was characterised.
* **COC/PDMS/COC** pneumatic valve arrays by corona-grafted bonding [LIU2011, H for abstract].

**Implication [assessment]:** published thermoplastic-membrane valve endurance is demonstrated at tens of cycles,
not the ≥ 10³ a multi-run cartridge needs. Cycle life is therefore a **bench gate** for the multi-run design.
Membrane valves are proven for single-use cartridges.

**Recommendation [assessment].** Use **normally-open mechanically or pneumatically actuated membrane valves** on
a multi-run cartridge. They:
* need no rotating seals;
* are cleanable by flushing;
* have actuators that stay in the dock.

Avoid rotary or turning valves in the bead path unless bead-trapping tests (E2.4-type) pass. Rated cycle life for
moulded membrane valves was **not found from any vendor**. It must be measured: at 9–16 runs/day and ~10 actuations
per valve per run, a cartridge used for a week needs ~10³ cycles [derived].

---

## 4. On-board reagent storage

* **Blisters:** ChipShop integrates 50–750 µL blisters with a piercing seat, and has test chips with 50/100, 250 and
  500 µL blisters [CS_FAB, CS_BLISTER, H].
  * **[assessment]** A blister is one-shot: it empties in one press. That suits a single-use cartridge with one assay.
  * It does not suit metering 10 µL doses from a reservoir over many runs unless the blister empties into an on-chip tank.
* **Dry reagents:** ChipShop integrates lyophilised pellets and dried spots, including beads and buffers [CS_FAB, H].
  * **[assessment]** A lyophilised **conjugate** pellet per run would remove the conjugate-ageing issue (docs/08 B4).
  * Lyophilised **capture beads** need re-dispersion and validation of capture activity. Both are UNVERIFIED for this antibody pair.
* **On-chip tanks with septa or vented caps:** volumes of 0.2–1 mL fit easily in a slide-format body 3–6 mm thick
  [assessment]. ChipShop's 750 µL maximum blister is a stated example of sub-mL volumes on its formats [CS_FAB, H].
  * A microscope slide is about 75 × 25 mm (exact ChipShop slide dimensions not read this session, UNVERIFIED).
  * Two 0.5 mL tanks of 5 mm depth need ≈ 2 × 100 mm² of footprint [derived].
* **Cooled reservoir zone:** a Peltier block in the dock contacting a thin-walled tank area (§5.4); COC's thermal
  conductivity is low, so the tank wall should be the thin foil side [assessment].
* **Keeping beads suspended.** 2.8 µm beads settle at ≈ 7 mm/h (docs/07 §5.5), so a 5 mm tank clears in under 1 h
  [derived]. Options [assessment]:
  1. a magnetic stir bar or rotating-field agitation from the dock;
  2. periodic recirculation by the dock syringe pump (aspirate/dispense, as in gen-1 SIA mixing);
  3. a rocking or orbital dock stage;
  4. **keep the bead stock off-cartridge** in a cooled, stirred vial in the dock and only meter it through the cartridge (gen-1 approach).

  Option 4 keeps the cartridge simple and is the lowest-risk choice for a multi-run design.

---

## 5. Docking-station components

### 5.1 Pressure controllers (drive pneumatic valves, pressure-driven flow)

| Item | Stated specs | Control interface | Source, conf. |
|---|---|---|---|
| **Fluigent Flow EZ** (LineUP) | 0–69, 345, 1000, 2000, 7000 mbar; vacuum −69 and −800 mbar; stability 0.1 % of measured value (above 10 % FS); resolution 0.03 % FS; accuracy 0.25 % FS; response down to 30 ms; works with FLOW UNIT sensors for flow control | standalone or OxyGEN software; SDK | FLUIGENT_FLOWEZ (H) |
| **Fluigent fgt-SDK** (GitHub, v23.0.0) | covers MFCS, LineUP (Link, Flow EZ, Flow Unit, Switch EZ, P-Switch), Flowboard, IPS, ESS, F-OEM, NIFS | **Python package with examples**, plus C++, C#, LabVIEW, MATLAB; Windows x86/x64, Linux x64/ARM/ARM64, macOS x64; Apache-2.0 | FLUIGENT_SDK (H) |
| **Elveflow OB1 MK4** | 1–4 channels; 0–200, 0–2000, 0–8000, −900 to 1000, −900 to 6000 mbar; stability down to 0.005 % FS; response down to 10 ms; MFS/BFS flow sensors, 0.1 µL/min–500 mL/min indicative | USB-B, TTL in/out, M8 sensor ports (UART on request); **SDK for Python**, MATLAB, LabVIEW, C++; ESI software Windows 10/11 | ELVEFLOW_OB1 (H) |

**[assessment]** A pneumatic membrane-valve cartridge needs only on/off pressure per valve. A solenoid manifold fed
from one regulated supply is simpler than a controller channel per valve. Pressure controllers earn their place
only if flow is driven pressurically (low pulsation at 1–10 µL/min) instead of by syringe pump.

### 5.2 Syringe pumps (dock-side SIA, metering of bead and conjugate doses)

| Item | Stated specs | Interface | Source, conf. |
|---|---|---|---|
| **Tecan Cavro Centris** | 6000 steps (normal) / 48 000 (high-resolution); syringes 50 µL–50 mL; up to 16 pumps on one bus | RS-232, RS-485 or CAN; 9600 or 38 400 baud | TECAN_CENTRIS (M; Tecan partner pages via search) |
| **Tecan Cavro XLP 6000** | "<5 µL to 50 mL" | — | TECAN_XLP (M) |
| **Hamilton PSD/4** 54848-01 | 3000 / 24 000 steps | RS-232, RS-485, CAN; 9600/38 400 baud; 16 devices daisy-chained | HAMILTON_PSD4 (M) |
| Hamilton PSD/4 High Valve Torque 99195-01 | 6857 / 54 587 steps | as above; 8N1, half duplex | HAMILTON_99195 (M) |
| Hamilton PSD/4 Smooth Flow 97709-01 | 24 000 / 192 000 steps | as above | HAMILTON_97709 (M) |

**Python support.** No vendor Python SDK was confirmed for Cavro or PSD. Both use documented ASCII serial command
sets (the gen-1 orchestrator already plans a serial driver). [derived] A 250 µL syringe at 24 000 steps gives
≈ 10 nL/step.

### 5.3 Flow sensors

| Item | Stated specs | Source, conf. |
|---|---|---|
| **Sensirion SLF3S-0600F** | full scale 2 mL/min (water, IPA); accuracy 5 % (water); repeatability 0.5 %; **12 bar**; I²C and RS-485; 1/4-28 flat-bottom ports; 3.2–3.8 V; 48 × 15.5 × 8.9 mm; eval kit EK-SLF3S-0600F; Arduino driver on GitHub | SENSIRION_SLF3S (H) |
| **Sensirion LG16-0150D** | full scale 7 µL/min water (≈ 70 µL/min IPA); wetted fused silica, PEEK, FEP (older v4 datasheet); 6-40 UNF for 1/32″ OD | SENSIRION_LG16 (M) |

**[assessment]** 1–300 µL/min spans two sensor ranges. Use an LG16-class sensor on the slow readout path
(10 µL/min) and an SLF3S-0600F on the 100–300 µL/min wash/transfer path. A Sensirion part for 10–300 µL/min with
1/16″ ports was not identified this session (UNVERIFIED).

### 5.4 Magnet actuation, Peltier, contacts, connectors

**Magnet actuation.** Design requirements carry over from docs/07 §5.4:
* TTL, two positions, ≤ 0.5 mm / ≥ 10 mm, ≤ 0.5 s;
* fail-safe = magnet on.

Zaber motorised linear stages are a candidate. Zaber's open-source **Zaber Motion Library** has Python (and MATLAB,
C#, C++, JavaScript, Java, Octave, Swift, LabVIEW) for Windows, Linux and macOS on x64/x86/ARM, plus direct ASCII
over serial or network [ZABER_SW, H]. A specific stage model, travel and speed were not read (UNVERIFIED).

**[assessment]** A stage gives position feedback but is not fail-safe on power loss. A spring-return solenoid or
spring-loaded slide (magnet held "on" by the spring) meets the fail-safe rule more simply; parts UNVERIFIED.

**Peltier cooling** (reagent zone, 4–8 °C, and assay zone 20–25 °C ±0.2 °C): no module datasheet was read
(UNVERIFIED). [assessment] Use separate TEC zones with a thermistor in the dock block under the foil side of the
tanks.

**Electrical contacts for pA–nA amperometry [assessment; vendor parts UNVERIFIED — Mill-Max returned 403]:**
* gold-plated spring pins on the electrode-die pads;
* guarded/shielded traces from pin to a short shielded cable to the Gamry cell leads;
* the whole dock electrode zone in a grounded enclosure (Faraday cage);
* the cartridge body is insulating, so leakage across wet pad gaps is the main risk; keep pads outside the wetted area and away from fluid ports.

Gen-1 grounding rules (docs/02 §4.4) apply unchanged.

**Chip-to-world connector for the SM-FL outlet.**
* ChipShop sells TPE "Tube Tuck" connectors for 1/16″ tubing into Luer or Mini Luer ports (Fluidic 1581, 1579) and for 1/32″ (1580, 997) [CS_CONN, H; pressure not listed].
* A ChipShop TPE connector set with 1/16″ PEEK tubing is quoted at 3.2 bar on a reseller page [DARWIN_FCPRO, M].
* Micronit's 4515 holder takes 1/16″ OD tubing in 6-32 flat-bottom ports at up to 100 bar [DARWIN_FC4515, M].
* No 360 µm capillary chip connector was read this session (UNVERIFIED).
* **[assessment]** The SM-FL → cartridge line sees only the downstream pressure drop of the cartridge plus waste line (≪ 1 MPa at ≤ 300 µL/min, docs/02 §5.1). A dock-side clamped through-hole seal (Micronit-style flat-bottom fitting or an O-ring/face seal) rated a few bar is sufficient and keeps dead volume < 1 µL.

---

## 6. Materials compatibility with the chemistry

*Source status: only the PubMed records cited below were read this session. Everything else here is **[assessment]**
and UNVERIFIED until checked.*

### 6.1 Tween-20 buffers (TBS + 0.05 % Tween)
* Tween adsorbs onto hydrophobic COC/COP/PMMA and helps block protein NSB.
* It can also extract additives from adhesives and some TPEs (UNVERIFIED), so check leachables by blank current.

### 6.2 Hydroquinone / benzoquinone and polymers
* PDMS absorbs hydrophobic small molecules, and partitioning "can significantly change solution concentrations" [TOEPKE2006, H for abstract]. Data for HQ/BQ were not found.
* BQ is more hydrophobic than HQ, so a PDMS wall downstream of the generator could lower collection efficiency.
* COC/COP are generally reported to absorb far less than PDMS (UNVERIFIED).
* Acceptance test [assessment]: hold 10 µM HQ (and BQ) in a test chip for the accumulation time (10 min) and measure recovery by CV/amperometry, against a glass control.

### 6.3 Substrate buffer
* Diethanolamine or Tris at pH ~9–9.8 with Mg²⁺.
* COC/COP/PMMA and borosilicate are compatible at pH ~10 at room temperature (UNVERIFIED).
* Ti adhesion layers under Au/Pt can undercut at long exposure (UNVERIFIED); Micrux uses a 50 nm Ti layer [PALMSENS_IDA, M].

### 6.4 Ag/AgCl pseudo-reference on chip
* Its potential follows chloride activity: about 59 mV per decade at 25 °C [derived, Nernst].
* A1 (TBS ~ 0.14 M NaCl) and B1 (HQDP substrate, chloride content set by the recipe) must have the **same chloride concentration**. Otherwise the reference shifts at the A1 → B1 step, exactly when the substrate blank is being recorded.
* Options [assessment]:
  * match chloride in B1;
  * use a docked salt-bridge Ag/AgCl reference (gen-1 approach);
  * use a Pt or Au quasi-reference and accept drift.
* Micrux dies have Au RE/CE on chip [PALMSENS_IDA, M]. A chlorided Ag pad would have to be added by the electrode foundry (UNVERIFIED availability).

### 6.5 Oxygen
* PDMS is highly O₂-permeable; COC/COP and glass are low (UNVERIFIED values).
* At +0.35 V (HQ oxidation) O₂ is not reduced at the generator, but a collector at −0.1 to −0.2 V (docs/05) may see an O₂-reduction background that depends on wall permeability. This argues against PDMS near the IDA.

---

## 7. Comparison and recommendation

### 7.1 Comparison table (this chip)

| Route | Min feature / depth | Electrodes | Bonding | Pressure | Protein / HQ | Optical | Prototype lead time, cost class | Scale-up | Verdict [assessment] |
|---|---|---|---|---|---|---|---|---|---|
| Glass (etched), thin-film Pt/Au | 2–3 µm lines; nm–1 mm depth (IMT, Dolomite hist.) | best: IDA 5/5 µm easy (IMT ≥ 2 µm) | low-T / RT / adhesive (fusion kills metals) | > 10 bar | good with silane-PEG/BSA | excellent | weeks–months, high | wafer-level; large chips stay costly | **electrode die only** |
| Moulded/milled COC/COP + foil | moulded 20–200 µm depth seen; machined inserts 50–500 µm (Vantiva) | hybrid die; screen-print pads; sputtered films limited by Tg | thermal/solvent; tape for prototypes | ~3 bar (CS 1367) | needs blocking; low small-molecule uptake (UNVERIFIED) | very good | milled from 1 piece; mould MOQ 100 + insert | **IVD standard** | **production body** |
| PMMA laminate / CNC | ≥ 50 µm wide, ≤ 200 µm deep (Potomac Fast Track) | clamped die only | PSA, solvent, laser weld | low–moderate | PSA leachables, HQ partition UNVERIFIED | good | days, low | none (re-design for moulding) | **first prototypes** |
| PDMS-on-glass | µm (soft litho) | on glass base | plasma | low | **absorbs small molecules; O₂-permeable** | good | days, low | poor | valve/flow studies only |
| 3D-printed | ~100 µm (UNVERIFIED) | none | — | — | resin leachables UNVERIFIED | variable | days | none | dock manifolds only |
| **Hybrid COC body + glass die** | as COC + as glass | **5/5 µm IDA or single WE** | die glued/gasketed into pocket | ≥ 1 bar at die gasket (to verify) | as COC/glass | good | weeks | yes (ChipShop states hybrid integration) | **recommended** |

### 7.2 Recommendation

**Prototype route (P):** hybrid with a **CNC-milled COC (or laser-laminated PMMA) fluidic body**, a 100–188 µm COC
foil lid and a **catalogue Micrux 10 × 6 mm glass thin-film die** (single WE first; IDA6 5/5 µm for redox cycling),
clamped with a laser-cut 25 µm spacer and pogo contacts in an aluminium dock.
* Valves: mechanically actuated membrane valves on the ChipShop Fluidic 1367 principle (actuator in the dock).
* Bead stock: stays in a cooled, stirred dock vial, metered by a Cavro/PSD pump through a cartridge port.
* Conjugate: a small cooled on-cartridge tank.

Main risks:
1. the gasketed die gap (25 µm) is not reproducible to the ±10 % the model needs (UNVERIFIED);
2. membrane-valve cycle life and bead trapping at seats unknown;
3. HQ/BQ uptake into PMMA/adhesive;
4. die pad layout and Micrux supply (price on request).

**Production route (Q):** **injection-moulded COC/COP cartridge** (ChipShop-type supplier, MOQ 100) with TPE or foil
membrane valves, a moulded 250–500 µL incubation chamber, a ≤ 0.2 mm foil wall at the trap and an **electrode die
from a glass-electrode foundry** bonded into a pocket. Candidates:
* Micrux custom service (5 µm rules, Au/Pt, SU-8/PI passivation);
* IMT (≥ 2 µm, Au/Pt/ITO/Ti, 200 mm wafers).

Lifetime choice [assessment]:
* **multi-run cartridge** (one 8-h block or one day), with
* the bead stock in a swappable dock vial pack, and
* the electrode die **inside the cartridge**.

This keeps the trap-to-electrode volume < 1 µL. Renewing the electrode with the cartridge also removes the
electrode-ageing term from the long-run blank.

Main risks:
1. carry-over across runs on a multi-run cartridge must meet 1×10⁻⁴ (docs/08);
   * related: thermoplastic membrane-valve endurance is published only at > 50 actuations (CHILDERS2024), against ~10³ needed for a week-long cartridge. If it fails, fall back to a daily cartridge or dock-side valves;
2. per-cartridge electrode variability enters calibration (one calibration per cartridge needed);
3. insert tooling cost and lead time (price on request);
4. polymer–glass bond integrity under repeated pressure cycles.

**Alternative worth costing:** a **permanent glass electrode chip in the dock** with a swappable polymer cartridge
docking onto it via a gasket. This is cheaper per run and gives one calibration per electrode, but it puts a
compliant seal in the 25 µm detection gap.

---

## 8. Open items (not checked this session)

* Micronit own design rules, electrode capability, 45 × 15 mm format details (site returned 429).
* Citrogene capabilities; Klearia electrode integration; uFluidix lead times.
* ChipShop: slide/credit-card format dimensions, pneumatic COC/TPE valve chips, membrane-valve cycle life, Fluidic 1004/1012 dimensions.
* Micrux die pad layout, AIO flow add-on channel volume, prices; Micrux custom-electrode lead time.
* Specific magnet stage/solenoid, Peltier modules, pogo-pin part numbers (Mill-Max page 403), 360 µm chip connectors (IDEX page gave no product data).
* Literature for §6: COC/COP O₂ permeability, HQ/BQ partitioning into COC/PMMA/adhesives, on-chip Ag/AgCl stability (PubMed searches returned nothing).
* Rated cycle life of moulded membrane or turning valves from any vendor.

---

## 9. Sources read this session (2026-11-12)

| Tag | URL | What was read |
|---|---|---|
| CS_FAB | https://www.microfluidic-chipshop.com/content/19-fabrication-services | ChipShop processes, materials, MOQ, blisters, dry reagents, formats |
| CS_VALVES | https://www.microfluidic-chipshop.com/16-valve-chips | valve chip list (names) |
| CS_1367 | https://www.microfluidic-chipshop.com/valve-chips/1235-2672-membrane-valve-chip-fluidic-1367.html | membrane valve chip specs, price |
| CS_155 | https://www.microfluidic-chipshop.com/valve-chips/142-2186-turning-valve-test-chip-valving-strategy-evaluation-fluidic-155.html | turning valve chip specs, price |
| CS_BLISTER | https://www.microfluidic-chipshop.com/17-blister-chips | blister test chip volumes |
| CS_SENSORCHIPS | https://www.microfluidic-chipshop.com/15-sensor-integration-chips | sensor integration chip list |
| DARWIN_CS4CH | https://uk.darwin-microfluidics.com/products/straight-channel-chip-h-200-m-w-1000-m-channel-fluidic-152/ (search summary) | ChipShop channel widths/depths, lid thickness |
| DARWIN_CSTAPE | https://darwin-microfluidics.com/content/pdfs/Open-chips-with-adhesiv-tape_ApIFOCV1-1.pdf (search summary) | tape depth rule, 200 µm min width |
| VANTIVA_GUIDE | https://microfluidics.vantiva.com/wp-content/uploads/2023/08/Vantiva-PBD_Manufacturing-Guide_rev1.pdf (search summary) | moulding design rules |
| DARWIN_MN | https://darwin-microfluidics.com/micronit | Micronit catalogue list |
| DARWIN_SERP | https://darwin-microfluidics.com/products/serpentine-microreactor-topconnect-pack-of-3 (search summary) | 45 × 15 mm functional glass element |
| DARWIN_FC4515 | https://us.darwin-microfluidics.com/products/fluidic-connect-4515-chip-holder | 4515 holder specs, price |
| DARWIN_FCPRO | https://darwin-microfluidics.com/products/fluidic-connect-pro-chip-holder | Pro holder part numbers, prices |
| MN_EOF_2007 | https://www.technologynetworks.com/tn/product-news/micronit-introduces-microfluidic-eof-kit-220093 (search summary) | EOF kit with electrodes |
| UL_DOLO_EOS | https://go.unchainedlabs.com/Dolomite_EndofSupport | Dolomite line discontinued |
| DOLO_PRESS | https://www.selectscience.net/article/dolomite-develops-lab-on-a-chip-device-with-integrated-electrodes (search summary) | historical Dolomite glass/electrode capabilities |
| IMT_FLYER | https://www.heidenhain.us/wp-content/uploads/2022/07/20180702_IMT_Flyer_LSD_Esc.pdf (search summary) | IMT electrodes, feature sizes |
| IMT_PRESS | https://medical-technology.h5mag.com/medical_technology_aug19/imt (search summary) | IMT production, bonding |
| RSC_LTBOND | https://www.rsc.org/images/loc/2012/pdf/T.5.125.pdf (search summary) | fusion bonding ~1000 °C excludes electrodes |
| KLEARIA_MTAS | https://microtasconferences.org/microtas2016/exhibit/support/klearia.html (search summary) | Klearia low-T bonding |
| UFLUIDIX_EE | https://www.environmental-expert.com/companies/ufluidix-91456/products (search summary) | uFluidix PDMS/glass |
| GOODFELLOW_MF | https://www.goodfellow.com/usa/services/microfabrication | features ≥ 1 µm, embossing 24–48 h |
| DATRON_POTOMAC | https://www.datron.com/resources/case-studies/potomac-photonics-case-study/ (search summary) | Fast Track 50 µm / 200 µm |
| BASI_IDA | https://www.basinc.com/thin-film-interdigitated-micro-array-electrodes_ | Micrux IDA part numbers and geometry |
| BASI_IDE | https://www.basinc.com/thin-film-interdigitated-electrodes (search summary) | MX-ED-IDE1-Pt |
| PALMSENS_IDA | https://www.palmsens.com/product/micrux-ed-ida-thin-film-interdigitated-microelectrode-array/ | IDA layer stack, substrate, size |
| PALMSENS_AIO | https://www.palmsens.com/product/micrux-one-cell/ (search summary) | AIO base dimensions |
| DI_AIO | https://pdf.directindustry.com/pdf/micrux-fluidic/all-in-one-platform-thin-film-electrodes/240350-975871.html (search summary) | AIO flow add-on PMMA/PEEK |
| DI_IDRA | https://www.directindustry.com/prod/micrux-fluidic/product-240350-2603297.html (search summary) | IDRA cell compatibility |
| DI_MICRUX_SINGLE | https://pdf.directindustry.com/pdf/micrux-fluidic/thin-film-single-electrodes/240350-975915.html (search hit only) | existence of single thin-film electrode catalogue |
| METROHM_FLWCL_IDE | https://www.metrohm.com/en/products/d/rp-f/drp-flwcl-ide.html | IDE wall-jet flow cell |
| FLUIGENT_FLOWEZ | https://www.fluigent.com/research/instruments/pressure-flow-controllers/flow-ez/ | Flow EZ specs |
| FLUIGENT_SDK | https://github.com/Fluigent/fgt-SDK | SDK languages, platforms, devices |
| ELVEFLOW_OB1 | https://www.elveflow.com/microfluidic-products/microfluidics-flow-control-systems/ob1-pressure-controller/ | OB1 MK4 specs |
| TECAN_CENTRIS | https://partnering.tecan.com/cavro-centris-pump-for-oem-liquid-handling (search summary) | Centris interfaces, steps, syringes |
| TECAN_XLP | https://partnering.tecan.com/cavro-xlp-6000-pump-for-oem-liquid-handling (search summary) | XLP range |
| HAMILTON_PSD4 | https://www.hamiltoncompany.com/product-specs/54848-01 (search summary) | PSD/4 steps, comms |
| HAMILTON_99195 | https://www.hamiltoncompany.com/product-specs/99195-01 (search summary) | high-torque variant |
| HAMILTON_97709 | https://www.hamiltoncompany.com/product-specs/97709-01 (search summary) | smooth-flow variant |
| SENSIRION_SLF3S | https://sensirion.com/products/catalog/SLF3S-0600F | SLF3S-0600F specs |
| CS_EXPLAINED | https://www.microfluidic-chipshop.com/content/15-chips-explained | formats, interface dimensions and internal volumes, materials |
| CS_CONN | https://www.microfluidic-chipshop.com/20-connectors | connector list, tubing sizes |
| CS_PLATFORMS | https://www.microfluidic-chipshop.com/29-interface-platforms | slide/double-slide interface platforms (PMMA; olive, Mini Luer, through-hole) |
| MICRUX_TF | https://www.micruxfluidic.com/es/soluciones-personalizadas/fabricacion-electrodos-thin-film/ | custom thin-film electrode capabilities |
| MICRUX_MF | https://www.micruxfluidic.com/es/soluciones-personalizadas/fabricacion-microfluidica/ | SU-8 mould capabilities |
| ZABER_SW | https://www.zaber.com/software | Zaber Motion Library languages/OS |
| TOEPKE2006 | Toepke & Beebe, Lab Chip 2006, 6, 1484–6, https://doi.org/10.1039/b612140c (PubMed 17203151) | PDMS absorbs small hydrophobic molecules |
| CHILDERS2024 | Childers et al., Lab Chip 2024, 24, 4422–4439, https://doi.org/10.1039/d4lc00501e (PubMed 39171671) | eCOC membrane valves, 75/350 kPa, > 50 actuations |
| GU2013 | Gu, Nishida, Fan, Electrophoresis 2014, 35, 289–97, https://doi.org/10.1002/elps.201300160 (PubMed 23868507) | PU membrane valves on COC, 8-month function |
| LIU2011 | Liu et al., J Colloid Interface Sci 2011, 365, 289–95, https://doi.org/10.1016/j.jcis.2011.09.004 (PubMed 21962541) | COC/PDMS/COC pneumatic valve arrays |
| SENSIRION_LG16 | https://sensirion.com/products/catalog/LG16-0150D (search summary of product page and datasheets) | LG16-0150D range, wetted materials |
