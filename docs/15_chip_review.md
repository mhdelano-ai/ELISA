# 15 — Independent review of the second-generation cartridge (docs/09–14, docs/06 E1.2b)

Status: 2026-11-12. Reviewer independent of the authors of docs/09–14. Scope: docs/09 (requirements), 10 (literature),
11 (fabrication), 12 (three candidates), 13 (detailed design of A), 14 (B and C′), the E1.2b addition to docs/06, read
against docs/00, 02, 05, 06, 08, `params/*.yaml`, `src/elisa_sim/`, `scripts/design_lib.py`, `automation/config/gates.yaml`.
**No file other than this one was edited; nothing was committed.** All recomputations were done with scripts in the
session scratchpad (outside the repository); model runs used a copy of the repository installed there
(`pip install -e .` in the copy). Nothing was generated in `/home/user/ELISA` except this file.

Conventions as in docs/08: **Derived** = recomputed here, arithmetic or script stated; **UNVERIFIED** = could not be
checked in this session; "src-check" = checked against the cited source in this session (PubMed metadata/abstract or
the vendor page/PDF). Classes: **Blocker** (the design as written cannot be built or its key claim is wrong; fix before
any spend on A), **Significant** (changes a number or decision the documents rely on), **Weakness** (should be fixed
before the stage that depends on it), **Note** (editorial or low consequence).

---

## 0. Summary

* The model numbers are honest in the narrow sense: every nearest-model estimate I re-ran for A, B and C′ reproduces
  to the last digit quoted (§3). The arithmetic of docs/13 is mostly right line by line (diffusion time constant,
  collection, double-layer charge, signal charge, PE2 sensitivity, Pi growth, ULOQ, inlet hydraulics, valve counts;
  my independent field computation reproduces the docs/13 magnet table within ≈ 10 %).
* What is wrong is mostly **between** the lines: the layer stack cannot realise the valves, gates and electrode
  contacts as drawn (A1, A2); the readout-chamber geometry in the feature table contradicts the "≤ 0.2 mm stub" claim
  on which the pre-electrolysis escape rests (S1); the double-step read does not cancel baseline drift and the read
  window collides with another run's actuations (S2, S3); the step table's arithmetic is off (3.5 min, not 3.25, per
  step pair; drag path 22.3 mm, not 20.3), so the 2.0-min margin is ≈ 1.1 min (S4); a stranded-bead path and a
  shared clean/dirty syringe path carry beads and enzyme into the next incubation of the same chamber (S5, S6); the
  bead "gather" as specified cannot bring beads from the far half of the chamber to the throat (S7).
* The pre-electrolysis credit (×0.01) is worth only ≈ +0.06 in P at nominal for A, is irrelevant after U1–U3
  screening (P 0.373 with or without it), and is decisive only for the S4a rescue — where my runs show the rescue
  needs ≤ 1 % escape (P 0.22) and collapses at 4 % (0.16) or at the ≈ 11 % implied by the feature-table geometry
  (0.09). The commercial guard cell (0.95 collection, ≥ 300 µL/min) supports none of the B, C′ or gen-1 guard-cell
  credits at the flows used (S8).
* docs/14's "P baseline artefact" is not an artefact: pinning the contamination key **removes the default 0–3 fM
  environmental contamination**. Done additively, the residual-analyte table drops by ≈ 0.07 in P (r = 10⁻⁴ at
  1000 pg/mL: P 0.15, not 0.22; r = 3×10⁻⁴: 0.006, not 0.07) (S9).
* Comparison tables are stale or mix rows (S10): docs/12 §0 sets A *with* pre-electrolysis beside B *without*;
  docs/14 §F still carries docs/12's A (2 µL RC, 21 valves, 54.0 min, 27.5-min cadence) instead of docs/13's.
* Verdict (§5): **wait for G1 (and E1.2b); keep A as the leading cartridge concept, but docs/13 is not yet a buildable
  design** — two Blockers and nine Significant findings must be corrected before C1 mock-ups are specified. The
  cartridge still has no LOD case: A without the pre-electrolysis credit is P 0.20 vs gen-1 0.16 (not decision-grade).

---

## 1. Findings

### Blockers

**A1 — The layer stack cannot realise top-actuated valves and flat-floor gates on bottom-face channels.**
*Location:* docs/13 §2.1 (L1 "6.0 mm; chambers and tanks open to the bottom; channels as grooves in the bottom face;
valve windows and die pocket from the top"; L2 TPE membrane laminated on top), §2.4 (gate drawn as "TPE membrane pushed
down into the lane" against the L0 foil), §4 ("pressed onto a 0.2 mm seat ridge by a dock plunger from the top"), D6.
*Evidence:* the channels, lanes and RC lie in the bottom face, 5.8 mm below the top surface where the TPE sheet is
laminated; plunger stroke is ≥ 0.3 mm (§6.2). A membrane on the top face cannot reach a seat or a lane 5.8 mm below it.
Either (a) every valve has two vertical vias up to a top-face seat (Ø ≥ 0.5 mm × 5.8 mm ≈ 1.1 µL each, ≈ 2.3 µL per
valve, Derived) — which destroys the "stubs ≤ 0.02 µL" at V13–V15 and puts ≥ 1 µL unelectrolysed wells beside the RC;
or (b) the gates G1–G4 are 5.8-mm-deep liquid-filled windows over the bead lane — dead volume, bead traps on the drag
path and a large unelectrolysed volume at G3/G4. Neither is in the dead-volume table (§2.6) or the escape estimate
(§3.6). The CS_1367 precedent quoted for "the principle" is a chip whose **100 µm Topas lid foil** is pressed (src-check:
product page lists "No membrane", lid "Mcs-foil 124 (Topas, 100 µm)"), i.e. the actuated layer *is* the channel
wall, which is the opposite arrangement.
*Correction:* redesign the stack so that the actuated membrane forms the channel wall at every valve and gate: e.g.
locally thinned body (≤ 0.5 mm) around the RC/lanes/gates with the membrane on the same face as the channels, or
valves/gates on the foil side with the magnet path routed between valve islands, or a two-level body with the RC and
gates in a thin (≈ 1 mm) insert. Then recompute §2.6 dead volumes, the stub volumes of §3.5.1 and the escape of §3.6.

**A2 — The electrode die's contact pads are unreachable as drawn.** *Location:* docs/13 §1.1, §2.1 row D ("bonded
face-down into a top pocket"; "pads on the part of the die outside the wetted area"), §6.1/§6.3 (pogo head in the
**lid**, top). *Evidence:* a die bonded face-down has its WE and pads on the downward face, at the bottom of a 5.8 mm
pocket (the RC ceiling is 0.20 mm above the floor foil, so the die face sits at that level). Pogo pins from the top
touch the bare glass back. Contacting from below conflicts with the foil floor and the M_h/magnet carriage under the
RC. *Correction:* specify the electrical route: through-glass vias (foundry capability UNVERIFIED), a die larger than
the pocket with pads on a ledge reached through openings from below away from the magnet path, a flex-tail bonded to
the pads, or a die mounted face-up as the RC *floor* (then the magnet side must change). Re-check the leakage/dew-point
and shielding arguments (§6.3, §6.6) for the chosen route.

### Significant

**S1 — The RC "stub" geometry contradicts the feature table; pre-electrolysis escape is ≈ 10 %, not 1–4 %.**
*Location:* docs/13 §3.5.1 ("all four sealing points ≤ 0.2 mm from the RC edge … stubs ≤ 0.02 µL"), §3.6 (escape ≤ 4 %,
probably 1–4 %) vs §2.3 feature table (RC inlet/outlet lanes "x 57.5–58.7 and 61.3–62.5 … 0.12 µL each"; SF channel
"RS → V13 → RC, 0.3 × 4 mm, 0.24 µL"; WLc "J → G3 (57.5)"; RC spans x 58.7–61.3). *Evidence:* G3 at x = 57.5 and G4
at 62.5 put 1.2 mm of 0.5 × 0.2 mm lane (0.12 µL) between each gate and the RC. 1-D dead-end diffusion from fill
(29.6 min) through PE1/PE2 to the start of the read (scratchpad `rev15/escape.py`, D = 9×10⁻¹⁰ m²/s, sink at the RC
mouth during and between electrolyses): HQ returned into the RC after PE2 = **6.6 %** of the RC content from the two
1.2 mm lanes, **3.1 %** from the 4 mm SF channel if V13 sits at its tank end, **1.0 %** from the CE/RE neck + pocket,
≈ 0 from genuine 0.2 mm stubs. Escape with the table geometry ≈ 11 %; with the §3.5.1 geometry ≈ 1 %. Model
consequence (my runs, §3): nominal P 0.258 (×0.01) → 0.242 (×0.11) — small — but the S4a rescue goes 0.22 → **0.09**.
*Correction:* make the geometry consistent (gates and V13–V15 seats at the RC edge, which A1 currently prevents), or
carry ×0.1 into the model; state that the S4a rescue requires ≤ 1 % escape **of the real RC**, and set the M5 escape
acceptance to ≤ 1 % (see S8).

**S2 — The double-step read does not cancel baseline drift; the 0.05 nC target needs ≤ 0.5 pA of current change
between windows.** *Location:* docs/13 §3.5.4 (D2: "Q_b contains the same charging, oxide and steady faradaic
background (and drift over 2 min)"), §1.3 noise mapping, §8.1, M5. *Evidence (Derived):* with a linear drift d, two
equal 90-s windows 105 s apart differ by ΔQ = d × 105 s × 90 s = d × 9450 s². The repository's only drift value
`hw.gamry.baseline_drift` 5 pA/min (1–10, UNVERIFIED) gives **0.79 nC** (0.16–1.6 nC) — 3 to 30× the 0.05 nC target.
Equivalently, the target needs the mean current of window b to equal that of window a within 0.05 nC / 90 s =
**0.56 pA**, i.e. ≈ 3×10⁻⁸ of the 12 µA charging peak and ≈ 10⁻⁸ of a fixed 60 µA range (§6.3 proposes "autoranging or
a fixed 60 µA range"); a fixed range's offset stability at that level is implausible (Gamry range-offset specs not
checked, UNVERIFIED). Also, the noise mapping in §1.3 omits the model's factor 2 (signal + baseline window,
`model.py` §9: var = (i·√(T/2B))²·2): 3 pA ↔ 0.023 nC, 20 pA ↔ 0.155 nC, 100 pA ↔ 0.77 nC (×√2 on the docs/13 values).
Separately, the 15 s at E_rest are not integrated: if E_rest lies on the foot of the HQ wave (window UNVERIFIED), product
oxidised during the rest before step a is lost from Q_a. *Correction:* use a three-window scheme (b–a–b′ or a, b, b′ with
linear interpolation, as gen-1's pre/post baselines), integrate the E_rest segments too, switch to a nA range only after
the charging transient (or limit the charging current by a ramp), and add "drift between windows" and "range-offset
stability" to M5's protocol with the 0.05 nC acceptance on the drift-corrected quantity.

**S3 — The READ window collides with another run's actuations; the "no overlap" check covers only adjacent runs.**
*Location:* docs/13 §7.1 resource check and "quiet windows". *Evidence (Derived):* run n's READ is 54.75–58.0 (run-n
time). Run n+2 is injected at 62.0 and executes its WL refresh (−5.0 → −4.5: S_RC dispense, V11, V12, G_k, V9/V10
plunger actuations), its IC drain (−4.5 → −4.0, S_ICk) and starts its bead dose (−4.0, S_b) at **57.0–58.0** run-n time,
i.e. inside step b of run n's read. The §7.1 check compared S_RC with run n−1 only; the quiet-window rule pauses only
tidal mixing and the carriage. Plunger solenoids and stepper drivers next to the die during Q_b corrupt Q_net
directly (S2). PE1 (29.75–31.5) likewise overlaps run n+1's aspiration, Inject Start and V(1/2)/V3 switching.
*Correction:* add a periodic overlap check over **all** run offsets (n ± 1, n ± 2) for every actuator class (not only
"resources"); move the refresh/drain/dose block earlier (e.g. −8 → −5) or treat all dock actuations as excluded during
step pairs; extend `cycle.py`'s planned check (§7.3) accordingly.

**S4 — Step-table arithmetic: the 2.0-min margin is ≈ 1.1 min, and the RC slack ≈ 0.4 min.** *Location:* docs/13
§3.5.4 ("15 + 90 + 15 + 90 s … total 3.25 min"), §2.3 / §3.3.3 (drag path 20.3 mm, window 38.0–39.75), §7.1, §1.1.
*Evidence (Derived):* 15 + 90 + 15 + 90 s = 210 s = **3.5 min**, not 3.25 (PE2 then ends at 38.25, overlapping the drag
start at 38.0; READ ends at 58.25). Drag path from the WL start to the RC centre = WLk 14.3 + WLc 5.5 + G3 → RC centre
2.5 (57.5 → 60.0) = **22.3 mm**, not 20.3; at 0.20 mm/s that is 111.5 s, plus the 0.25-min hand-over = 2.1 min against
a 1.75-min window. Re-timed: drag 38.25–40.36, accumulation to 55.36, READ to **58.9 min** after Inject Start (margin
1.1 min; 59.9 from aspiration start); RC occupied 29.0 → ≈ 59.6 per 31-min cadence → slack ≈ 0.4 min, so the stated
tolerance "30.75–33 min" cadence is wrong at the low end. Bend radii ≥ 3 mm lengthen the path further. §1.1 says
16 determinations ≈ 8.3 h, §7.1 says 523 min = 8.7 h (+ ≈ 15 min docking + 2 priming runs ≈ 9.5 h of reagent life
against the 8-h default conjugate life, docs/07 §5.5, and the 8-h HQDP-at-25 °C basis of D8). *Correction:* re-time
§7.1 (e.g. accumulation 14 min, or 60-s steps, or cadence 32 min), state the margin honestly (≈ 1 min) and size
reagent life for ≥ 9.5 h.

**S5 — Stranded beads in branch k are pushed into the next incubation of chamber k; the "first chamber rinse" does
not exist in the step table.** *Location:* docs/13 §3.3.5(a) vs §7.1 rows −5.0 → −4.0. *Evidence:* run n's stranded
beads in WLk stay there until run n+2's refresh (−5.0, i.e. 57.0 run-n time), which pushes WLk liquid "from J toward
the IC" into the empty ICk; the only following step is a drain of 5 µL refresh liquid (−4.5 → −4.0), then beads,
conjugate and sample are added. Run n's 3-rinse cleaning (39.75–44.75) precedes this push and cannot remove them. With
a ≤ 5 µL residual (§3.2.3) a 5 µL drain removes little; the "< 10⁻⁵ by 3-rinse arithmetic" does not apply. This is a
direct bead-borne carry-over path into run n+2 at up to the M1 acceptance (50 beads = 10⁻⁴), i.e. it alone can use
the whole 10⁻⁴ budget. *Correction:* refresh WLk in the J → IC direction only immediately before the chamber cleaning
of the *same* run (e.g. at 39.75, followed by the 3 rinses), or refresh WLk toward V12/waste (needs a valve at the
IC end of WLk or a waste port at the throat); add the path to the carry-over budget and to M1 (count beads arriving in
ICk after a refresh).

**S6 — Shared clean/dirty syringe paths and the unbudgeted serpentine.** *Location:* docs/13 §2.6, §3.2.2–3.2.3, §3.4,
§3.8, §7.1. *Evidence:* S_ICk drains 176 µL of incubation liquid (0.3 nM conjugate, uncollected beads, sample) at
300 µL/min through the 60 µL serpentine (≈ 150 mm × 2 × (0.8 + 0.5) mm ≈ 390 mm² of COC, ≈ 3× the IC wall area) into the
dock syringe, then delivers the rinse A1 back through the same path. With a 10 µm film on 390 mm² (≈ 4 µL) the
effective rinse dilution is ≈ 105/9 per step instead of 105/5, i.e. free conjugate in the drag medium ≈ 0.19 pM
instead of 0.032 pM (Derived; ≈ 240 molecules carried into the RC instead of ≈ 40 — still < 5 % of the 5700 NSB
enzymes, so LOD-neutral, but the derivation in §3.4 is not conservative). More importantly S_RC *pulls* the RC + BW
flush (spent beads' product, enzyme, any detached beads, fallback-read effluent) through P_s into its syringe, and
the same S_RC dispenses the A1 for the WL refresh **into ICk** (§7.1 −5.0). Neither the serpentine (bead settling,
wall adsorption, bend traps) nor the S_RC path appears in the carry-over budget (§3.3.5, §8.3). *Correction:* separate
pumps (or a holding coil with a defined wash) for clean delivery and waste pull; put the serpentine and the syringe
paths into the carry-over budget and the M7 challenge; give the serpentine a defined cleaning.

**S7 — The bead "gather" as specified cannot bring the far half of the chamber's beads to the throat.**
*Location:* docs/13 §3.3.2 table ("M_c edge … 64 T/m lateral"), §3.3.3 (M_c "+x edge under the throat entrance",
gather "+x by 4 mm at 0.05 mm/s"), §3.3.4 (collection and gather ≥ 0.99 each). *Evidence (Derived, scratchpad
`rev15/mag.py`, surface-charge integration, B_r 1.3 T, bead m = 1.15×10⁻¹³ A·m², docs/13's own inputs):* on the floor
(0.30 mm above a 10 × 10 × 5 mm block) |B| rises from 0.41 T at the block centre to 0.58 T just inside the edge;
lateral force on a bead 2 pN at 2 mm from the centre, 4 pN at 3 mm, 9 pN at 4 mm, against 10–22 pN pressing it onto
the foil. Collected beads therefore migrate (if friction allows) **radially away from the block centre**, i.e. to the
chamber wall all round, not to the throat. With the block spanning chamber x = −6…+4 mm, a +4 mm gather moves the
trailing edge only from −6 to −2 mm: beads at the −x wall end ≈ 6 mm from the throat; beads along the ±y walls stay.
(My numbers otherwise reproduce docs/13: M_c top 0.187 T / 49 T/m vs 0.18 / 47; wall 0.158 T, 17 lateral / 44 vertical
vs 0.16, 16/43; M_d edge 0.38 T, 377 lateral / 636 vertical vs 0.37, 350/630; the lateral gradient just outside the
M_c edge peaks at ≈ 365 T/m, not 64, so the edge follow speed is ≈ 0.6 mm/s rather than 0.10.) A lowered M_c
(Z −5 mm, bead plane 5.3 mm) still gives 0.12 T and 31 T/m (3.6 pN, ≈ 0.15 mm/s settling-equivalent): passing under
the *other* chamber during its incubation (the carriage offset direction is not specified) would collect its beads.
*Correction:* sweep the trailing edge across the whole chamber (≥ 10 mm, ≈ 20–40 s at the real edge follow speed),
or use a collection magnet smaller than the chamber parked under the throat with a sweep from the far wall; specify
the M_c–M_d offset and carriage paths so that no magnet passes under an incubating chamber; and fix the hand-over
order (S7b below).

*S7b (same location):* "M_d moved under the throat, M_c lowered when M_d is in place" is impossible with both magnets on
one X–Y carriage 25 mm apart: putting M_d under the throat moves M_c 25 mm away while still raised, smearing the
pellet across the floor. The order must be: M_c down, carriage move, M_d up (pellet unheld for the move).

**S8 — Pre-electrolysis credits: the guard cell supports none of them at the flows used; the gates are looser than the
credit; the WE2 fallback voids it.** *Location:* docs/12 §2.3, §9 decision 3, §10; docs/14 §C3.2, §C3.6, §C3.7 (C′1,
"C′1 under S4a P 0.17"); docs/12 §4 B ("dock GUARD CELL … + 1 mL holding loop"); docs/13 §3.5.7, D8, M5 ("escape
≤ 4 %"); docs/06 E1.2b. *Evidence:* `hw.flow_cells.thermo_6011rs_coulometric.collection_efficiency` 0.95 (0.8–1.0) and
`min_flow` 300 µL/min (THERMO_6011RS, repository values; vendor document not re-read here). (i) C′ passes HQDP through
the guard cell at ≤ 20 µL/min (bed fill), 5 µL (IDA back-fill) and 0.5 µL/min (counter-flow): all far below the minimum
flow; only the 15 nL IDA fill is electrolysed in place, while the 40 nL bed void (71 % of V_acc) is filled with
guard-cell substrate. The ×0.01 credit of C′1 and its S4a row are unsupported. (ii) B fills a 1 mL holding loop through
the guard cell (feasible at ≥ 300 µL/min) but the loop then ages for up to ≈ 22 runs (≈ 9.5 h): at the acceptance-limit
k_h 10⁻⁹ s⁻¹ HQ re-grows to ≈ 3×10⁻⁵ mol/mol before oxidation (3× the nominal lot impurity); the bed-void substrate
(0.2 µL) is never electrolysed in the RC. My run "B1 with escape 0.05" gives P 0.174, identical to ×0.01 — B's credit is
immaterial at nominal and unsupported under S4a. (iii) Gen-1: fill flow 200 µL/min and baseline/shunt flow 10 µL/min
are below 300 µL/min; electrolysing only the fill creates a **baseline mismatch** (baseline windows read
non-electrolysed substrate, the product plug electrolysed substrate): a negative bias equal to the impurity in the trap
volume, varying with lot and age. (iv) The same mismatch hits A's fallback R-flow read (§3.5.7): WE2 baselines and the
sweep use un-electrolysed RS substrate, which at 25 °C (D8) also gains up to 2.9×10⁻⁵ mol/mol over 8 h at the
acceptance-limit k_h; at 3 mM and 10⁻⁵ the impurity in one RC volume is 6.0 nC (§3.6), i.e. a bias of ≈ 4× the
1 pg/mL signal that drifts over the cartridge. D8 (HQDP at 25 °C) is justified only for the step-read mode.
(v) docs/13 M5 accepts escape ≤ 4 % while the model credit is ×0.01 and E1.2b's PASS threshold is 0.01; my runs:
×0.04 costs nothing at nominal (P 0.254 vs 0.258) but takes S4a from 0.22 to 0.16. *Correction:* state per candidate
which volume is electrolysed in place; drop the guard-cell credit for B, C′ and gen-1 unless the cell runs ≥ 300 µL/min
into a store that is used within minutes and all baseline substrate passes it; set M5's escape acceptance to ≤ 1 %
(or enter the measured value); require cold RS storage (or a separately pre-electrolysed sweep supply) whenever the
R-flow mode is used; under E1.2b INTERMEDIATE/FAIL revert D8 and recheck the 3 mM choice.

**S9 — docs/14's "P baseline artefact" is the removal of the default contamination term; the residual-analyte P
values are ≈ 0.07 too high.** *Location:* docs/14 §C3.7 caveat and residual table; Appendix (`.with_values({
"ma.nsb.blank_igg_contamination_equivalent": r * C_prev …})`). *Evidence:* the key's default is value 0, low 0, high
3×10⁻¹⁵ M (`params/model_assumptions.yaml`, environmental human-IgG contamination up to 0.45 pg/mL, sampled).
`with_values` pins it, deleting that sampled term. Reproduced: C′1 1.0×10⁻³⁰ pinned → P 0.244 (docs/14: 0.24), with
the 5th percentile falling from 0.46 to 0.27 pg/mL (the contamination floor removed). Done additively
(`with_bounds(value = r·C, low = r·C, high = 3 fM + r·C)`): r = 10⁻⁴ after 1000 pg/mL → **P 0.152** (docs/14 0.22),
r = 3×10⁻⁴ → **P 0.006** (docs/14 0.07). Nominal LODs are unaffected (0.70 and 1.10 reproduced). *Correction:* replace
the caveat with the explanation, re-run additively, and drop "artefact". The qualitative conclusion (r must be
≤ 10⁻⁴) is strengthened.

**S10 — The comparison tables are stale and mix rows; the B numbers are both right but compared wrongly.**
*Location:* docs/12 §0 ("A 2.3 / 0.20 (1.9 / 0.25 with pre-electrolysis), B 2.3 / 0.15, C 2.4 / 0.16"); docs/12 §6;
docs/14 §0, §B3/B6, §F. *Evidence:* I reproduce B0 2.33 / 0.153 and B1 (pre-el.) 2.08 / 0.174 exactly, so docs/12's
2.3/0.15 is B0 and docs/14's 2.1/0.17 is B1; both are correct model outputs. docs/12 §0 puts A1 (with credit) next to
B0 (without). Like for like: **A0 2.3/0.20 vs B0 2.3/0.15**, or **A1 1.9/0.25 vs B1 2.1/0.17** — docs/12 §6 and docs/14
§F (which list both) are right; docs/12 §0 is the misleading one. docs/14 §F still carries docs/12's A (2 µL RC, 1 mM,
21 valves, busiest 70, 54.0 min, 27.5 min/sample); docs/13's A is 1.88 / 0.26 (3 mM, 1 µL RC), 20 valves, busiest 40,
58.0 min (≈ 58.9 after S4), 31 min/sample. And no table shows the like-for-like number that matters most for the "is a
cartridge justified" question: **A without the pre-electrolysis credit, 3 mM, RC 1 µL: 2.45 / 0.196** (my run) vs
gen-1 3.5 / 0.16 — +0.04, not decision-grade. *Correction:* one master comparison table (in docs/13 or docs/14) with
A as docs/13, rows with and without credit for every candidate, and docs/12 §0 corrected.

**S11 — The carry-over budget of A is not allocated, and the SM-FL alone uses it at nominal.** *Location:* docs/13
§3.3.5, §8.3; docs/14 §C3.8. *Evidence:* the 10⁻⁴ criterion (gates.yaml `carryover`, docs/08 S6) is end-to-end.
`hw.smfl.carryover_protein_conjugate` nominal is 10⁻⁴ (10⁻⁵–10⁻³, UNVERIFIED); docs/14 assigns it 3×10⁻⁵ "(needs a
needle wash better than nominal)"; docs/13 assigns nothing and lists M1's per-path limits (≤ 50 beads = 10⁻⁴ for the
lanes alone, ≤ 50 in the RC, PE2 threshold ≈ 2×10⁻⁵) whose sum already exceeds 10⁻⁴, before S5/S6 paths and the inlet
manifold dead legs (M_in branches to the non-selected V1/V2 and to V3 are dead-ends during injection; not quantified).
*Correction:* an explicit budget table for A like docs/14 §C3.8 (SM-FL, inlet manifold incl. dead legs, IC residue,
WL branch, serpentine/syringe, RC, BW), with M1/M7 limits derived from it (e.g. ≤ 10 beads per path).

### Weaknesses

**W1 — "Reagents on the cartridge" is no longer true and is not put to the user as such.** docs/13 recommends V2
(bead stock in a dock vial) and D12 (RCj and RS filled at insertion from dock bottles). Together the card carries **no
factory-filled reagent**: all three reagents come from the dock, the card only holds conjugate and HQDP transiently.
docs/09 records the user decision "on-board reagents (capture phase, ALP conjugate, HQDP substrate, wash as needed)".
docs/13 §12.1 Q2 asks only about D12 "until shelf data exist"; docs/12 §9 decision 5 asked about beads. *Correction:*
ask the user one explicit question: "V2 + D12 means no reagent is supplied on the card; is that acceptable, or must at
least conjugate/HQDP be factory-filled (which needs shelf data first)?" Note also the operator now loads a bead vial and
two bottles per card (still before the autosampler, so not a manual step in the docs/00 sense).

**W2 — The 0.95 bead transfer and the "LOD-insensitive" claim.** docs/13 §3.3.4 targets ≥ 0.95 overall; S7 makes the
collection/gather budget optimistic. The model's insensitivity to transfer (0.80 → P 0.25) assumes a *constant*
transfer; run-to-run transfer variability is a dose CV in disguise (CV 0.10 → P 0.20, my run reproduces docs/13).
*Correction:* M1 acceptance on transfer CV (≤ 5 %), not only on the mean.

**W3 — M1 cannot verify ≤ 50 stranded beads by sampling.** "≥ 400 counted per sample" (hemocytometer/fluorescence
of an aliquot) estimates transfer; a 10⁻⁴ residual (≤ 50 beads in a lane) needs whole-lane imaging of every bead.
*Correction:* specify whole-path fluorescence imaging (lane, throat, RC, gates, serpentine) for the stranded counts.

**W4 — The carry-over test cannot resolve 10⁻⁴ at the M7/GC2 LOD.** 10⁻⁴ of a 10 ng/mL challenge is 1 pg/mL; at the
M7 acceptance LOD ≤ 1.5 pg/mL (3 SD) one SD is 0.5 pg/mL, so 3 × (challenge → B1 → B2) cannot distinguish 10⁻⁴ from 0.
(This is inherited from gates.yaml `carryover`, docs/08 S6.) *Correction:* use a 100 ng/mL challenge for the
mock-ups (above ULOQ is irrelevant for the following blank), or n ≥ 10 challenge pairs with a stated power.

**W5 — The Au quasi-reference sits in a pocket whose HQ/BQ ratio changes within every run.** PE converts HQ → BQ in the
pocket; product HQ diffuses in; the CE in the same pocket reduces BQ (or O₂). An Au QRE's potential follows the local
redox couple; docs/13's requirement (drift ≤ 20 mV / 8 h) does not address within-run shifts between E_rest and E_det
steps. The E1.2b undivided-cell arm is on carbon in bulk, not this pocket. *Correction:* add a within-run QRE potential
log (docked Ag/AgCl) to M5(e).

**W6 — Substrate conductivity.** R_u ≈ 12 kΩ uses 1.6 S/m (A1, `hw.tubing.buffer_conductivity`). 0.1 M Tris at
pH 9.5 is ≈ 4 % protonated (pKa ≈ 8.1, UNVERIFIED constant): with 1 mM MgCl₂ and 3 mM HQDP salt, κ ≈ 0.1–0.2 S/m
[assessment] → R_u ≈ 100 kΩ, R_u·C ≈ 0.1 s — still ≪ τ = 18 s, so harmless, unless the "fixed NaCl addition" is set high.
State the NaCl concentration; its ALP effect is an E1.7-type check (as docs/13 says).

**W7 — Chamber alternation creates two calibration populations.** Odd runs use IC1/WL1, even runs IC2/WL2 (different
mixing, lane, gate). The per-card QC has blank 1 (IC1) and blank 16 (IC2) and one control (IC2): no chamber-specific
blank SD or slope can be estimated. *Correction:* lot calibration per chamber, or one blank per chamber at both ends.

**W8 — docs/09 F1 requirement relaxed silently.** docs/09 F1 asks to "capture ≥ 96 % of the injected analyte"; A and B
transfer 1.5 loop volumes (0.90) by design. It is a defensible trade (×1.17 capture rate), but the requirement change
should be recorded. Also the model credit uses dilution /1.7 (170 µL) while docs/13's chamber is 176 µL (Note-level
optimism of ≈ 3 %); with the gen-1 /2.2 dilution my run gives P 0.213 vs 0.258, so the chamber mixing/dilution
assumption is worth ≈ 0.045 in P — as large as the whole cartridge-vs-gen-1 gain.

**W9 — C′ transfer push and IDA recovery acceptance.** docs/14 §C3.4 pushes 60 nL through a 1 nL guard into a 15 nL IDA
channel from a 40 nL bed void: at most ≈ 15/40 of the product *moles* can sit in the IDA at the read; C′-R5's "product
recovery in IDA ≥ 0.8" is impossible as moles (possible only as concentration). LOD-neutral (specific and NSB alike) but
the acceptance must be defined as concentration. Counter-flow consumption is 0.5 µL/min × (6.5 + 2) min ≈ 4.3 µL, not
12.5 µL (harmless). The pinch valves on the bed-inlet tee see the bed Δp (0.14–0.29 MPa); their pressure rating was "not
read" — check before relying on them.

**W10 — Regeneration evidence over-read.** docs/12/14 use Sun2008's "mean elution efficiency of 92 %" (src-check:
FITC-tagged HSA on an anti-FITC epoxy monolith) as an 8×10⁻² carry-over for human IgG on anti-Fc. It is an elution
*recovery* in a different binding system, not a measured surface residual. The conclusion (no evidence of ≤ 10⁻⁴) stands;
"best found 8×10⁻²" should read "no residual measured; one elution recovery of 92 % in a hapten system".

### Notes

* **N1** docs/13 §2.3 MC row: "footprint 2.0 × 1.0 × 5.0 mm cavity, depth 1.0 mm" — inconsistent (2 × 5 × 1 mm gives
  10 µL). IC working volume 170 µL in the feature table vs 176 µL in §3.1/§3.2 (fill height 3.5 mm, wetted area ≈ 138 mm²).
  The conjugate stock concentration for 0.3 nM in 176 µL (5.3 nM) is not stated (docs/12 used 5.1 nM for 170 µL).
* **N2** docs/13 §3.5.5 CE charge "4 steps × 0.14 µC": PE1 + PE2 + READ = 5 forward steps plus the return steps;
  ≈ 1.4 µC; conclusion (≈ 0.6 mM OH⁻ in the pocket, flushed every run) unchanged.
* **N3** docs/13 §3.5.3/D2: Q_net subtracts ≈ 105 s of continuing enzyme turnover collected in step b from the 900 s
  accumulation (≈ −2 %, constant, calibrated); state it.
* **N4** docs/12 §3.1 and docs/10: Otieno2014 (src-check) moves beads to the detection chamber by **removing the magnet
  and switching a valve** (flow), not by magnetic transfer; and it uses 1 µm beads carrying 3×10⁵ HRP — the LOD is not
  comparable. Wording only.
* **N5** docs/10 uses the key "Kim2015" for two different papers (doi:10.1016/j.bios.2014.10.042 and
  doi:10.3390/s150306469). Rename one.
* **N6** Part numbers in docs/14 not traceable to docs/11: Lee LFN, IDEX MXX777-xxx, Bio-Chem 038T2B, 075P/100P pinch
  valves, Parker Series 1/2 (MX Series II and MXP9900 are in docs/07). They are traceable to docs/14 §C7 vendor
  documents (LFN page and the Bio-Chem pinch brochure src-checked: "10 M Cycles Min", 9 µL, vac–30 psig; "minimum of
  2 million … silicone … over 500,000 … C-Flex … over 200,000"). Add them to docs/11 §9 before any BOM use. Parker is
  V-sec/403 only — mark UNVERIFIED in the C2.2 table body, not only in the tag. All docs/13 parts are from docs/11
  (checked by name), and the one price (CS_1367 €34.40 from 10, €42.20 single) is src-checked.
* **N7** docs/13 §4 cites CHILDERS2024 (src-check: eCOC membranes on PC/PETG, 75/350 kPa, "> 50 times without failure")
  and CS_1367 (foil-actuated, "Single use", 3 bar) as endurance evidence for a TPE-on-COC laminate: neither is that
  material system. The M4 gate (180 cycles with real media) is the right answer; say that no evidence exists for the
  chosen material pair.
* **N8** M-280 saturation magnetisation 1×10⁴ A/m (docs/13, UNVERIFIED) is of plausible order (I recall ≈ 1–1.5×10⁴
  A/m from Fonnum et al. 2005, J. Magn. Magn. Mater. — not checked in this session, UNVERIFIED); not in PubMed.
* **N9** docs/06 E1.2b correctly leaves the G1 rule untouched (gates.yaml `informational` block is not read by code;
  `G1_rule` unchanged) and already flags the guard cell's 0.95 / 300 µL/min. It tests carbon at 1 mM in a divided
  bulk cell; the cartridge uses Au, 3 mM and a CE pocket connected to the RC. Add an Au arm at 3 mM (or make M5a the
  geometric/material complement explicitly).
* **N10** The U5 residual-bead criterion is still 10⁻³ in docs/06 E2.4 (gen-1) — the docs/09 §7 inconsistency persists
  in the bench plan; docs/13 M1 uses 10⁻⁴ (consistent with S6); docs/14 C′-R1 uses 10⁻³ only as an intermediate gate
  multiplied by strip survival (consistent).

---

## 2. Arithmetic re-checked and found correct (no finding)

docs/13: τ = 4h²/(π²D) = 18.0 s, F(90 s) = 0.9945, effective two-step collection 0.989; C_dl·A·ΔE = 0.95 µF × 0.15 V =
0.14 µC (docs/12: 7.4 µF × 0.35 V = 2.6 µC), needed repeatability 3.5×10⁻⁴; signal 5708 × 1000 × 0.968 × 900 s × 2e =
1.59 nC; hydrolysis offset 0.054 nC (0.54 at 10⁻⁹ s⁻¹); free HQ in the RC 6.0 nC at 10⁻⁵; PE2 0.50 nC per 10⁻⁴ of a
10 ng/mL sample; neck R = 7.8 kΩ and neck exchange 3×10⁻³ s⁻¹; inlet R = 3.2×10¹⁰ Pa·s/m³ → 53 Pa; analyte-sink bound
43 %; capture gain ×1.17; rinse dilution (105/5)³ = 9261 → 2.0×10⁶ molecules; IC residue 0.05 × (5/105)³ = 5×10⁻⁶;
inlet-line carry-over without the D13 flush 6.2 µL × 0.12 / 100 = 7.4×10⁻³ (as a worst case; whether the parked 1 µL/min
would flush the line before the next injection depends on Loop Offline timing — the D13 fix is sound either way);
jet 0.10 m/s, Re 56; settling 58 µm per 30 s; Pi growth 0.17 µM per 8 h at 3 mM and the acceptance-limit k_h; 1.9 days
to 1 µM; volumes of RS, RCj, MC, serpentine, WL, RC; card thickness 8.1 mm; waste 0.94 mL per run; valve totals 18 per
run, 360 per cartridge, busiest V13 40 (60 fallback). docs/14: k_d kinetics (2.3×10⁻⁹, 55 s), n = 3.6 repeats, particle
count 1.15×10⁵, settling 89 mm/h, port diffusion 4.7 %, compliance 0.32 nL, Hagen–Poiseuille 2.0×10⁴ Pa, guard Péclet
≈ 2800, dead-end erfc values, C′ budget sum 1.0×10⁻⁴, valve margins, B dose-CV quadrature (0.112 / 0.141).

---

## 3. Numbers reproduced vs not reproduced

Model runs: copy of the repository in the scratchpad, `pip install -e .`, docs/12 Appendix A helpers (with
`Aarch(vol)` defined as the docs/12 A design plus `ma.geometry.magnetic_trap_volume`), n = 2000, seed 20261111, script
`runs.py` and `rev15/run2.py` in the scratchpad. "R" = reproduced to the quoted digits.

| Quantity (document) | Quoted | Mine | Status |
|---|---|---|---|
| A0 (docs/12) median / P / ULOQ | 2.3 / 0.20 / 2330 | 2.32 / 0.201 / 2326 | R |
| A1 (docs/12) | 1.9 / 0.25 | 1.88 / 0.250 | R |
| A1 3 mM, RC 2 µL (docs/12, docs/13 row 1) | 1.91 / 0.26 / 6810 | 1.91 / 0.264 / 6813 | R |
| docs/13 A, 3 mM, RC 1 µL | 1.88 [0.37–54] / 0.26 / 3040 | 1.88 [0.37–53.7] / 0.258 / 3043 | R |
| docs/13 A, 1 mM | 1.83 / 0.23 / 1360 | 1.83 / 0.229 / 1359 | R |
| docs/13 A + L6 + L7 | 1.12 / 0.37 / 1040 | 1.12 / 0.373 / 1039 | R |
| docs/13 A, S4a | 1.95 / 0.22 | 1.95 / 0.220 | R |
| docs/13 A, bead-dose CV 0.10 | 2.11 / 0.20 | 2.11 / 0.203 | R |
| docs/13 A, noise 20 pA | 2.34 / 0.17 | 2.34 / 0.172 | R |
| B0 / B1 (docs/12, docs/14) | 2.3 / 0.15; 2.1 / 0.17 | 2.33 / 0.153; 2.08 / 0.174 | R |
| C′1 (docs/14) | 2.1 [0.46–23] / 0.16 | 2.13 [0.46–23.3] / 0.165 | R |
| C′1 contamination pinned 10⁻³⁰ (docs/14 "artefact") | P 0.24 | 0.244 | R — explained in S9 |
| C′1 r = 10⁻⁴, C_prev 1000 (docs/14, pinned) | 0.70 / 2.1 / 0.22 | 0.70 / 2.10 / 0.222 | R; additive: 0.70 / 2.16 / **0.152** |
| C′1 r = 3×10⁻⁴ (docs/14) | 1.1 / 2.3 / 0.07 | additive: 1.10 / 2.50 / **0.006** | not comparable (S9) |
| **New:** A (docs/13) without pre-electrolysis | — | 2.45 [0.43–81] / 0.196 | |
| **New:** A, escape ×0.04 / ×0.11 | — | 0.254 / 0.242 | |
| **New:** A, S4a at escape ×0.04 / ×0.11 / none | — | 0.156 / 0.086 / 0.001 | |
| **New:** A + L6 + L7 without pre-electrolysis | — | 0.373 (identical) | |
| **New:** A, tubing factor not pinned (no "clean zone" credit) | — | 0.248 | credit legitimate and small |
| **New:** A, chamber dilution /2.2 instead of /1.7 | — | 0.213 | |
| **New:** B1 with guard-cell escape 0.05 | — | 0.174 (same as ×0.01) | |
| Magnet table docs/13 §3.3.2 | see S7 | within ≈ 10 %; edge lateral gradient 365 vs 64 T/m | R except one row |
| Thin-layer, charge, Pi, hydraulics, volumes, valve counts | §2 | §2 | R |
| Step-table sums | 58.0 min; 3.25 min per step pair; 20.3 mm | 58.9 min; 3.5 min; 22.3 mm | **not R** (S4) |
| Escape ≤ 4 % (docs/13 §3.6) | ≤ 4 % | ≈ 1 % (text geometry) / ≈ 11 % (table geometry) | depends on S1 |
| Anguizola2018 k_d 0.166 s⁻¹ (docs/14) | — | number not in the abstract | UNVERIFIED |
| THERMO_6011RS 0.95 / 300 µL/min | — | repository param only; vendor doc not re-read | UNVERIFIED here |
| Gamry range offset/accuracy for S2 | — | not checked | UNVERIFIED |
| M-280 magnetisation | 1×10⁴ A/m | — | UNVERIFIED (N8) |

**Override legitimacy (task 2).** (i) Tubing/trap factor pinned 0.01 for A's clean readout zone: legitimate (the RC
never sees conjugate solution; ≈ 40–240 carried molecules), and worth only 0.01 in P. (ii) Pre-electrolysis ×0.01: a
genuine advantage only in the step-read mode and only if the real RC escape is ≤ 1 % (S1, S8); at nominal it is worth
+0.06 (0.196 → 0.258), after L6 + L7 nothing, under S4a everything. (iii) "Exhaustive collection": the model reads A
with the gen-1 thin-layer flow detector (conversion 0.78 × elution), so no exhaustive-collection credit is actually
in the numbers; the step-read *background* (S2) is not in the model either, which flatters A by an unknown amount —
the docs/13 noise rows show 0.155 nC (correctly mapped) already costs ≈ 0.09. (iv) Dilution /1.7: worth ≈ 0.045, rests
entirely on the unmeasured mixing factor. (v) No override gives a zero wall NSB in the product path except (i); IC
walls are outside the path by design, consistently with the model. (vi) docs/14's contamination pinning is wrong (S9).

---

## 4. Sources spot-checked (task 3)

| # | Key (doc) | Claim | Result |
|---|---|---|---|
| 1 | Wang2013 (10, 12, 13) | > 95 % beads in 2 min at 0.7 mm/s; DiFMUP carry-over < 0.002 % | supported (PubMed 24051541); carry-over is the *substrate* (small molecule) — docs mark protein UNVERIFIED, correct |
| 2 | Herrmann2007 (10, 12) | two networks, fluidic bridges, 100 pg/mL, 30 min, no passivation | supported (PubMed 17960284) |
| 3 | Otieno2014 (10, 12) | stirred capture chamber, magnetic transfer, 5/7 fg/mL | numbers supported; transfer is by magnet removal + valve switch (flow) — N4 |
| 4 | Kim2015 Sensors (10, 12, 13) | thin-film Ag/AgCl + GO, < 2 mV over 26 days | supported (PubMed 25789490); key collision N5 |
| 5 | Sun2008 (10, 12, 14) | 92 % mean elution | supported (PubMed 18479142), but FITC-HSA/anti-FITC — W10 |
| 6 | Uthuppu2015 (10, 12, 14) | 51 regeneration cycles (27 without analyte) | supported (PubMed 25626958) |
| 7 | Grate2009 (14) | 3.6 µL renewable Sepharose column, beads replaced, 10 pM in < 20 min | supported (PubMed 19381395) |
| 8 | Fu2011 (14) | pillar filter + pneumatic valve trap/release, 10 min, LOD 0.080 ng/mL | supported (PubMed 21366237) |
| 9 | Andersson1999 (14) | > 90 % in 30 s in 9/13; complete in 5 | supported (PubMed 10405611) |
| 10 | Goode2015 (14) | ≈ 60 % success | supported (PubMed 25402969) |
| 11 | Knoglinger2017 (14) | desthiobiotin surface, SA + bait removed in 3-min injections, chip life 2–3 weeks | supported (PubMed 28734694) |
| 12 | Anguizola2018 (14) | human IgG k_d 0.166 s⁻¹ at pH 2.5 | abstract lacks numbers; UNVERIFIED by me (docs/14 tags V-full) |
| 13 | CHILDERS2024 (11, 12, 13, 14) | eCOC valves, 75/350 kPa, > 50 actuations | supported (PubMed 39171671); material system differs (N7) |
| 14 | CS_1367 (11, 12, 13) | €42.20 / €34.40 from 10, tight to 3 bar, single use | supported (vendor page); "No membrane", 100 µm Topas lid foil (A1) |
| 15 | MICRUX_TF (11, 12, 13) | Au/Pt 150 ± 15 nm, ≥ 5 µm, SU-8/PI, glass; no Ag/AgCl | supported (vendor page); die size not on the page (docs/11 takes 10 × 6 mm from PALMSENS_IDA — consistent) |
| 16 | LEE_LFN (14) | 10 M cycles min, 9 µL, vac–30 psig | supported (vendor page) |
| 17 | BIOCHEM_PINCH (14) | valve ≥ 2×10⁶; silicone > 5×10⁵; C-Flex > 2×10⁵ | supported (brochure PDF text) |

No cited number was found contradicted by its source; three are applied beyond what the source shows (3, 5, 13/14).
Unmarked unsourced numbers: none of consequence found in docs/13/14 beyond those already listed (the docs mark their
physical constants UNVERIFIED consistently).

---

## 5. Verdict

**Honest conclusion: wait for G1 (and E1.2b) before any cartridge spend, as docs/12/13 themselves say — and do not
treat docs/13 as a buildable design yet.** A is still the best of the three concepts (it keeps the one-step format,
moves beads not liquid, has the only per-run carry-over monitor, and needs neither the packed-bed NSB factor nor
regeneration), and nothing found here favours B or C′ over it. But:

1. The cartridge has **no LOD case** in the model: without the pre-electrolysis credit A is P 0.196 vs gen-1 0.16;
   after U1–U3 screening the credit is worth nothing (0.373 either way). Its case is throughput, buffer use and
   automation — the user should decide on that basis explicitly (docs/12 §9 decision 2 says so; docs/13 does not repeat
   it).
2. Two Blockers (A1 layer stack vs valves/gates; A2 die contacts) mean the dead-volume, escape and electrical
   arguments must be redone after a geometry fix.
3. The step read (D2), the design's main departure from the modelled gen-1 readout, has an uncorrected drift term
   (S2) and a scheduling collision (S3); the fallback R-flow read loses the pre-electrolysis credit (S8). M5a is
   therefore well chosen as the single pre-G1 spend, provided its protocol adds drift-corrected acceptance, range-offset
   stability and dock actuations during step pairs.
4. Gate thresholds that would not catch the problems found: M5 escape ≤ 4 % (should be ≤ 1 % to support the credit);
   M1 counting by sampling (W3); M7/GC2 carry-over power (W4); no mock-up runs two staggered chambers before C2 (S3);
   none tests the WL refresh direction or the shared syringe paths (S5, S6). M1 would catch S7 (transfer ≥ 0.95).

Ordering recommendation: C0 desk corrections now (this list); M5a only after user approval and after E1.1/E1.2/E1.2b;
the shared B-E1 = C′-R2 packed-bed NSB tube experiment is cheap and keeps the fallback honest; everything else after G1.

---

## 6. Questions only the user can answer

1. **Reagents on the card:** V2 + D12 leave no reagent supplied on the cartridge. Accept (reagents in dock vials/bottles,
   card as fluidic consumable), or require factory-filled conjugate/HQDP (then shelf-life data are a prerequisite)?
2. **Is the cartridge justified without an LOD gain?** The modelled gain is +0.04 in P (not decision-grade); the case is
   throughput (31 vs 56 min/sample; gen-1 with a second cup ≈ 30), buffer use and automation. Proceed on that basis?
3. **Time margin:** after S4 the result is ≈ 58.9 min (≈ 1 min margin). Accept, or trade 1–2 min of accumulation
   (≈ −0.01 in P per docs/12) for margin?
4. **Carry-over budget:** the SM-FL's nominal 10⁻⁴ (UNVERIFIED) leaves nothing for the cartridge. Accept the docs/08 S6
   alternative (mandatory cleaning cycle after any result > 100 pg/mL) as the primary rule for a multi-run card?
5. **M5a before G1** (catalogue Micrux die, low cost) — approve, with the protocol additions of S2/S3/S8?
6. **Reagent life ≥ 9.5 h per card** (S4): accept an extended conjugate/HQDP in-use life (needs E1.3 ageing beyond 8 h),
   or limit a card to ≈ 14 determinations?

---

## 7. Resolution of findings

Added 2026-11-12 by the session that wrote the decision document (docs/16). Each claimed resolution was checked by
reading the revised text (docs/12 corrections box, docs/13 Revision B, docs/14 revised, docs/06); no model run was
made in this session, so numerical claims of docs/13/14 are recorded as stated there unless a check is named. Status:
**resolved** (the text now does what the finding asked), **resolved on paper** (the design answers it, the bench must
confirm), **partial** (part of the correction is missing), **open** (with the deciding experiment), **superseded**
(by a user decision of 2026-11-12, docs/16 §2).

| ID | Status | Where | Check made / what remains |
|---|---|---|---|
| A1 | resolved on paper | docs/13 §2.1–2.6, §4 | Stack is now foil / 0.175 mm through-cut sheet / TPE ceiling / upper body; every valve presses the TPE onto the foil; zoning keeps valves over the anvil. Open: sealing of a TPE ceiling in a 0.5 × 0.175 mm rectangular channel and the 0.175 mm through-cut sheet as a series part (UNVERIFIED) — **M4** |
| A2 | resolved on paper | docs/13 §2.7, §6.3 | Die face-down on the sheet, pads on the lower face over a dry contact window, pogo pins from below, lid pad reacts the force. Open: pin force, leakage ≥ 5×10¹² Ω — **M5a-7**, C2 |
| S1 | resolved on paper | docs/13 §2.6, §3.6 | Stub rule ≤ 0.3 mm (≤ 0.5 mm at the cell); escape recomputed 0.20 % (D 9×10⁻¹⁰) / 0.49 % (7×10⁻¹⁰) — component sum checked: 0.05 + 0.05 + 0.03 + 0.07 = 0.20; 0.12 + 0.12 + 0.07 + 0.17 = 0.48 (stated 0.49, rounding). M5a/M5 acceptance set to ≤ 1 % as asked. Escape script is scratch only (`escape_b3.py`, not in the repository). Bench: **M5a-4** |
| S2 | resolved on paper; open on the bench | docs/13 §3.5.4, §1.3, §10.1 | Three-window read Q_a − 2Q_b + Q_c, noise mapping with the factor 2 (σ_Q = 7.75 s × i), drift-corrected acceptance, fixed-range vs autorange arm, E_rest charge criterion (M5a-5). **Partial on one point:** the E_rest segments are bounded by an acceptance (≤ 1 % of Q_a) rather than integrated into Q_net as the finding suggested. Bench: **M5a-1/2/5** |
| S3 | resolved (spot-checked) | docs/13 §7.1–7.2 | Periodic check over k = −4…4 offsets by the scratch `sched.py` (not in the repository). Hand spot-check of offsets ±1, ±2 against the step table: no dock actuation in any PE2 or READ window; **two movable steps of run n+2 sit exactly on the ±0.25 min guard** (conjugate fill ends at 52.5 = READ start − 0.25; bead dose starts at 57.0 = READ end + 0.25), so the guard has zero slack at C = 31.0 and relies on the scheduler. Bench: **M8** |
| S4 | resolved | docs/13 §7.1, §5.2 | Checked: PE2 and READ 30 + 3×60 + 2×15 s = 4.0 min; drag 23.3 mm / 0.20 mm/s = 116.5 s within 39.5–41.75; accumulation 41.75–52.75 = 11 min; result 56.75; 12 + 13 × 31 + 56.75 = 471.75 min = 7.86 h for 14 determinations |
| S5 | resolved | docs/13 §3.3.6, §7.1 | WL_k refresh at 41.75–42.35, before the same run's cleaning (42.35–49.85). Bench: M1 (≤ 1 bead in IC_k) |
| S6 | resolved on paper | docs/13 §3.2, §3.4, §8.3, §7.5 | Dispense-only S_A, pull-only S_IC_k and S_RC (enforced in software), rinses through a clean inlet, serpentine one-way; all paths in the §8.3 budget. Bench: M7, M2 |
| S7, S7b | resolved on paper | docs/13 §3.3 | Fixed collection magnet per chamber, three raster passes of the drag magnet, separate units, no magnet under the other chamber. Magnet arithmetic is scratch (`mag_b.py`); M-280 magnetisation still UNVERIFIED (N8). Bench: **M1** |
| S8 | resolved for A, B, C′; **partial for gen-1** | docs/13 §3.5.7, §3.6; docs/14 §B0, §C3.1; docs/12 box item 2 | A: headline without credit, R-flow fallback without pre-electrolysis. B/C′: credit re-derived as ×0.05 with a per-run guard-cell fill at ≥ 300 µL/min, headline without credit. **Gen-1:** docs/06 E1.2b names the guard cell's 300 µL/min minimum flow but not the **baseline mismatch** of S8 (iii) (baseline windows on untreated substrate); recorded as an open item in docs/06 §13 by this session. Bench: E1.2b, M5a-4, C′-R6 |
| S9 | resolved, with a follow-up | docs/14 §0, §C3.7, Appendix | Carry-over now added to the default 0–3 fM term; "artefact" removed. **Follow-up:** docs/14 found this review's own additive redo slightly optimistic, because `sample_param` samples a range with low > 0 and high/low ≥ 3 log-triangularly, which concentrates draws near r·C_prev and under-weights the default term. Figures at r = 10⁻⁴ after a 1000 pg/mL predecessor: **this review P 0.152; docs/14 with linear sampling P 0.10** (r = 3×10⁻⁴: 0.006 in both). **docs/16 uses 0.10.** Not re-run in this session |
| S10 | resolved | docs/16 §1; docs/12 box item 1; docs/14 §F (A column marked interim) | One master table in docs/16 with A from docs/13 Rev B and every candidate with and without credit. Leftovers listed below (docs/14 §C3.11, §F1 "0.37") |
| S11 | resolved on paper; **partial in substance** | docs/13 §8.3; docs/14 §C3.8 | Budget table, sums checked (consecutive 8.2×10⁻⁵, same chamber 1.4×10⁻⁵, worst 9.6×10⁻⁵, post-high 4.6×10⁻⁵, after blank check 1.7×10⁻⁵). It closes only if the SM-FL reaches 3×10⁻⁵ against a nominal 10⁻⁴ (UNVERIFIED); the user's post-high rule is the stated protection otherwise. Bench: **E1.10** + flush programme, M7 |
| W1 | superseded by user decision | docs/13 §5; docs/12 box 9(a); docs/14 §B0 | Dock-supplied reagents accepted 2026-11-12 |
| W2 | resolved | docs/13 §10.3 M1 | transfer CV ≤ 5 % |
| W3 | resolved | docs/13 §10.3 M1 | whole-path fluorescence imaging |
| W4 | resolved for the cartridge; gen-1 unchanged | docs/13 §8.3, §10.3; docs/14 §C3.10 | 100 ng/mL challenge, n = 5 per path class (C′: or ≥ 10 pairs). gen-1 keeps 10 ng/mL with 5 pairs; docs/06 §12.5 argues it resolves 10⁻⁴ at SD_blank 0.33 pg/mL (≈ 5 SE), which holds only if the blank SD is that low — not changed here |
| W5 | open | docs/13 §3.5.5, §10.1 step 6 | within-run QRE log against a docked Ag/AgCl — **M5a-5** |
| W6 | resolved on paper | docs/13 §3.5.5 | NaCl fixed at 50 mM; its effect on ALP UNVERIFIED (E1.7-type arm) |
| W7 | resolved | docs/13 §8.2 | per-chamber lot calibration; blank and control per chamber per card |
| W8 | resolved as a record; **user confirmation open** | docs/13 §3.1, §1.3 (dilution /1.85); docs/14 §B0; docs/12 box 8 | F1 relaxation recorded for A and B; question put to the user in docs/16 §8 Q2 |
| W9 | resolved, **partial** | docs/14 §C3.4, §C3.6, §C3.10 | IDA recovery defined as concentration; counter-flow 4.3 µL. Pinch-valve pressure rating against the bed Δp (0.14–0.29 MPa) still not read — check before C′-R1 |
| W10 | resolved | docs/14 §0, §C1, §C3.8, §F; docs/12 box 5 | "no residual measured; one 92 % elution recovery in a hapten system" |
| N1 | resolved | docs/13 §2.3, §3.1 | MC 2.0 × 1.0 × 5.0 mm = 10.0 µL (checked); chamber 185 µL; stock 5.6 nM |
| N2, N3 | resolved | docs/13 §3.5.4–3.5.5 | 7 forward steps per run; constant turnover cancels to −0.9 % |
| N4 | resolved in docs/12 (box 6); **docs/10 unchanged** | docs/12 box | docs/10 may not be edited; the wording there still reads as before |
| N5 | **partial** | docs/12 box 7; docs/13 cites the DOI | the key collision remains in docs/10 (not editable in this round) |
| N6 | **partial** | docs/14 §C7, §C2.2 | Vendor ratings traced to docs/14 §C7 documents and Parker withdrawn; the part numbers are still **not** in docs/11 §9 (docs/11 not editable) — add them there before any BOM use; none is in docs/07 |
| N7 | resolved | docs/13 §2.1, §4 | no endurance evidence exists for TPE on COC; M4 (100 cycles) decides |
| N8 | open | docs/13 §12.2 | M-280 magnetisation UNVERIFIED; M1 measures follow speed directly |
| N9 | resolved | docs/13 §10.1 | M5a adds Au, 3 mM, the cell geometry |
| N10 | open (user decision) | docs/06 §13 (open item added by this session) | E2.4 residual beads ≤ 10⁻³ vs analyte criterion 10⁻⁴; acceptance **not** changed |
| §4 stretched sources (Otieno2014, Sun2008, CHILDERS2024/CS_1367) | resolved where editable | docs/12 box 5–6; docs/13 §2.1, §4; docs/14 §C1 | docs/10 wording unchanged (not editable) |
| §6 Q1 reagents on the card | superseded by user decision | docs/16 §2 | dock-supplied reagents |
| §6 Q2 cartridge without LOD gain | answered in docs/16 §0 | — | case stated as throughput, automation, buffer use |
| §6 Q3 time margin | superseded by user decision | docs/13 §7.1 | ≥ 3 min; 3.25 min after Inject Start (2.25 after aspiration, docs/16 §8 Q6) |
| §6 Q4 carry-over rule | superseded by user decision | docs/13 §7.4; docs/14 §B0, §C3.8 | 10⁻⁴ kept + mandatory cleaning cycle and blank check after > 100 pg/mL |
| §6 Q5 M5a | superseded by user decision (approved) | docs/06 M5a; docs/13 §10.1 | protocol includes drift-corrected acceptance, range plan arm, dock actuation sources; the slot does not fit the bench load (docs/06 M5a) |
| §6 Q6 reagent life | superseded by user decision | docs/13 §5.2 | card capped at 14 determinations (7.86 h) |

**Leftover inconsistencies between docs/09–14** (found while writing docs/16; docs/09–12 are not edited in this round):
1. docs/14 §C3.11 and §F1 quote A + L6 + L7 as P 0.37 (docs/13 Revision A); Revision B gives 0.328 / 0.330
   (docs/13 §1.3). docs/14 §F already says to read A from docs/16; left as is.
2. docs/14 §B7 (iv): "valves fail below 3× life (≈ 210 cycles)" rests on docs/12 A's busiest ≈ 70; Revision B's busiest
   is 17 per card (31 fallback) and M4 tests 100 cycles. Not changed (number, not a cross-reference).
3. docs/12 box item 4 says docs/13 has 20 valves (Revision A); Revision B has 21 (17 + 4 gates).
4. Capture gain from reduced dilution: ×1.21 (docs/12 §10, box 8) vs ×1.17 (this review §2, W8). Revision B uses the
   dilution /1.85 directly.
5. B time to result: 50.0 min (docs/12 §4.4 step table) vs model time 52.0 (docs/14 §B6) — two definitions.
6. Margin basis: docs/13 states 3.25 min from Inject Start and 2.25 min from aspiration; gen-1 is quoted both ways
   (docs/05 56.1 from aspiration, docs/06 §7.8 52.1 from Inject Start).
7. docs/13 §10.1 says M5a runs "only after E1.1/E1.2/E1.2b", while its approved slot (weeks 6–8) overlaps E1.2b
   (weeks 5–7). Only M5a step 5 (escape) needs E1.2b's chemical floor; docs/06 M5a orders the steps accordingly.
8. docs/09 header records "on-board reagents" and docs/09 F1 "≥ 96 %": both superseded/relaxed (docs/16 §2, §8 Q2).
9. docs/09 §7: U5/E2.4 10⁻³ vs 10⁻⁴ (N10), still open.

**Trivial cross-reference fixes made in docs/13** (marked "(cross-reference updated with docs/16)"): finding map rows
S9 and S10 and §12.1 item 8 said docs/14's contamination pinning and comparison table were "open for their owners";
docs/14 has since been revised and the master table is docs/16 §1. No number was changed. docs/14 needed no
cross-reference fix (it already points to docs/16).
