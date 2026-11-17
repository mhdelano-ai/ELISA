# Fact-check: what the Waters stack can do without a valve

Written 2026-11-17 for the tier round (docs/26). Scope: ACQUITY UPLC I-Class PLUS, BSM + SM-FL (100 µL loop).
Evidence labels: [V] opened this session; [S] search summary only; UNVERIFIED; Derived.
Facts already held in docs/02 are not re-derived (see the task statement).


## Sources opened this session (short keys used below)
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

## 1. Can the method stop the flow (0.000 mL/min step)?
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

## 2. Real minimum flow; accuracy and pulsation below 0.2 mL/min
- Settable minimum: 0.010 mL/min (I-Class, older firmware) or 0.001 mL/min (Premier; I-Class PLUS fw >= 1.71)
  [V K8407, ICspec, PRspec; S for I-Class PLUS]. The user's statement of 1 µL/min fits the second value.
- Flow accuracy is specified only at 0.500 mL/min (±1.0 %); flow precision (0.075 % RSD) and composition specs only
  from 0.2 to 2.0 mL/min [V ICspec, PRspec]. No Waters statement found on accuracy or pulsation at 1-100 µL/min.
- Older text calls the BSM flow "steady (pulse-free) at analytical flow rates" [V OG p. 1-6]; no number.
- Bench test: timed gravimetric collection (>= 30 min, sealed vial, 0.01 mg balance) at 1, 3, 10, 30 µL/min behind
  the chosen restrictor; log the BSM pressure trace (analog out, see Q5) for ripple. Accept if mean error < 5 % and
  ripple does not show in the amperometric baseline.

## 3. Pump behaviour between sample-set lines
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

## 4. Several flow steps and long low-flow holds in one method
- Specs list 11 gradient curves (linear, 2 step, 4 concave, 4 convex) [V ICspec]. No Waters text found on the maximum
  number of gradient-table rows or the maximum run time. Waters application notes run 85-93 min gradients on
  I-Class PLUS / H-Class PLUS [S; https://www.waters.com/nextgen/en/library/application-notes/2018/acquity-uplc-i-class-plus-system-methods-employ-long-shallow-gradients.html].
  A 60 min method is therefore within ordinary use.
- Bench test: build a BSM method with 25 rows (flow steps 0.010 -> 0.001 -> 0.200 mL/min, 30 min hold) and save it;
  the editor's limit, if any, shows at row entry.

## 5. Timed outputs a potentiostat can read
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

## 6. Running below 1000 psi; restrictor placement
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

## 7. Particles through the SM-FL
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

## 8. Full loop on 100 µL; partial-loop reagent injections
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

## Remaining UNVERIFIED (summary)
0 mL/min method row; I-Class PLUS minimum flow and switch count; flow accuracy below 0.2 mL/min; gradient-row limit;
idle flow between Empower lines; SM-FL needle/tubing IDs and internal filters; bead injection; full-loop overfill 2x.
