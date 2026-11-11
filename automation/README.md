# automation — lab-PC orchestration skeleton

What it is: the Python layer that will run one assay cycle on the instrument (docs/02 §3.2, docs/05 §4.1). Empower
runs the Waters stack as usual; this software listens for the SM-FL **Inject Start** signal, switches the added
valves, drives the bead dispenser (SIA syringe pump), the trap magnet and the Gamry, logs everything, stores the raw
current traces and computes the result. Today **every device is simulated**, so the whole cycle runs and is tested
without hardware. The real-hardware drivers are stubs: each says which vendor call belongs where and what is not
yet verified (they raise `NotImplementedError` instead of guessing a command).

## Contents

| Path | What |
|---|---|
| `config/cycle_primary.yaml` | step table of the primary design, one-step mode (docs/05 §4.1), 56.1 min |
| `config/cycle_sequential.yaml` | in-platform fallback, sequential mode (docs/05 §4.1), 58.1 min |
| `config/cycle_recovery.yaml` | recovery cycle after a fault (magnet off, 300 µL/min trap flush, cup rinse; docs/08 S12) |
| `config/hardware_sim.yaml` | all-simulated devices (used by tests and `run_sim`) |
| `config/hardware_lab.example.yaml` | template for the real instrument (fill in after Stage 0) |
| `config/gates.yaml` | gate thresholds of docs/06 with their sources; `G1_rule` = the G1 decision rule (docs/06 §4.11) |
| `elisa_auto/cycle.py` | loads and checks a step table (no gaps, valid valve positions, ≤ 60 min; since the final review also: trap flow where SIA and BSM meet at the tee ≤ 100 µL/min, every SM-FL injection declared, SIA ports exist) |
| `elisa_auto/latch.py` | fault latch: after a fault, runs are flagged invalid until the recovery cycle completes (docs/08 S12) |
| `elisa_auto/sequencer.py` | runs a cycle: timing from each Inject Start, watchdog, safe state, run log |
| `elisa_auto/devices/` | interfaces (`base.py`), simulators (`sim.py`), stubs (`idex_mx.py`, `syringe_pump.py`, `daq.py`, `empower.py`), Gamry client (`gamry_client.py`) |
| `elisa_auto/gamry_worker.py` | the Gamry worker that runs in **Gamry's own Python** (see below) |
| `elisa_auto/signal_proc.py` | per-run signal: baseline-corrected charge in the readout window |
| `elisa_auto/stats.py` | blank statistics, calibration, LOD (mean + 3 SD), carry-over, Stage-1 conversions |
| `elisa_auto/analyze.py` | `python -m elisa_auto.analyze <folder>`: prints the gate quantities |
| `elisa_auto/model_feedback.py` | `python -m elisa_auto.model_feedback <yaml>`: re-runs the model with bench values |
| `elisa_auto/run_sim.py` | `python -m elisa_auto.run_sim`: simulated cycles end to end |
| `elisa_auto/watch_inject.py` | Stage-0 tool: print Inject Start edges |
| `templates/` | CSV templates for Stage-1/2 experiments (filled with **synthetic example numbers** — replace them) |
| `tests/` | tests (`python -m pytest -q automation/tests`) |

## The Gamry constraint and how it is handled

Gamry's Echem ToolkitPy installs its own **Python 3.7.9, 32-bit** and must be the only Python 3.7 32-bit on the PC
(docs/02 §4.3, Gamry quick-start guide 988-00100). The rest of this software (and the model) needs **Python ≥ 3.10,
64-bit**. They are therefore two processes:

```
orchestrator (Python 3.10+ 64-bit)  <-- JSON lines over TCP 127.0.0.1 -->  gamry_worker.py (Gamry Python 3.7 32-bit)
 sequencer, valves, pump, DAQ, data                                          ToolkitPy -> Reference 600+ (+ optional 2nd channel)
```

`gamry_worker.py` uses only the Python standard library (nothing to install in Gamry's Python) and only Python 3.7
syntax; a test checks both. Its `sim` backend works today; its `toolkitpy` backend is a stub listing what must be
written once the ToolkitPy manual is at hand (open the instruments, set potentials, continuous chronoamperometry,
cell off). A second channel is needed only for the optional IDA (docs/08 S9); pairing the 600+ with a second instrument is UNVERIFIED (docs/07 §3).

## Setup on the lab PC (Windows) — step by step

You need administrator rights only for installing Python and the Gamry software.

1. **Install Python 3.12 (64-bit)** from python.org. In the installer tick "Add python.exe to PATH". Do not remove or
   change the Gamry Python.
2. **Install Git for Windows** (git-scm.com) with default options.
3. Open **PowerShell** (Start menu → type "PowerShell" → Enter). Every command below is typed there, then Enter.
4. Get the project (replace the URL with the repository address you were given):
   ```powershell
   cd $HOME\Documents
   git clone <repository-URL> ELISA
   cd ELISA
   ```
5. Create a private Python environment for this project and switch it on (you must repeat the second line each
   time you open a new PowerShell window):
   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell refuses to run the script, run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, answer
   `Y`, and repeat the line. The prompt now starts with `(.venv)`.
6. Install the model and the automation package with their test tools:
   ```powershell
   python -m pip install --upgrade pip
   pip install -e ".[test]"
   pip install -e ".\automation[test]"
   ```
7. Check that everything works (both lines must end with "passed"):
   ```powershell
   python -m pytest -q
   python -m pytest -q automation\tests
   ```
8. Run a simulated series of cycles (takes seconds; the virtual clock skips the waiting):
   ```powershell
   python -m elisa_auto.run_sim --out bench\sim_runs\first_try
   ```
   It prints the blank statistics, calibration slope, LOD, carry-over and time to result computed from the
   simulated runs. The run folders contain `events.jsonl` (every action), `trace.csv` (raw current),
   `metadata.json` and `result.json`. Open them with any text editor or Excel.
9. **Gamry worker test** (once Gamry software with ToolkitPy is installed): find Gamry's `python.exe` (look in the
   Gamry installation folder; the exact path is UNVERIFIED) and run, in a second PowerShell window:
   ```powershell
   & "C:\path\to\Gamry\python.exe" automation\elisa_auto\gamry_worker.py --backend sim --port 50555
   ```
   It waits silently. In the first window: `python -m pytest -q automation\tests\test_gamry_worker.py` tests the same
   protocol with your normal Python. Stop the worker with Ctrl+C.

On Linux/macOS (for desk work) the same commands work with `python3 -m venv .venv` and `source .venv/bin/activate`.

## Daily use during the bench phase

* **Stage 1 (no flow system):** fill a copy of the matching template from `templates/` with your numbers, save it
  in a new folder `bench/S1_<experiment>_<date>/`, then
  ```powershell
  python -m elisa_auto.analyze bench\S1_E1.3_2026-12-07
  ```
  The printout gives the label factor, linearity, wash-removable fraction, free HQ, hydrolysis, off-rates,
  detection-on-capture ratio, recovery, with the gate verdict and the source of each threshold (docs/06 §4.11).
* **Feed the model:** write the measured values into `bench\measured_values.yaml` (format:
  `templates\measured_values.example.yaml`) and run
  ```powershell
  python -m elisa_auto.model_feedback bench\measured_values.yaml --rank
  ```
  It prints the model's LOD and P(success) for the primary, the sequential mode and the backup before and after
  your values, **the G1 verdict** (GO ≥ 0.30, GO-WITH-LEVER 0.10–0.30, STOP < 0.10; docs/06 §4.11), and which
  remaining parameter matters most (the next experiment). It never changes `params/`.
* **Stage 2 onwards (real devices):** copy `config/hardware_lab.example.yaml` to `config/hardware_lab.yaml`, fill in
  COM ports and DAQ lines, and implement the stubs (below). `python -m elisa_auto.watch_inject --hw
  automation\config\hardware_lab.yaml` checks the Inject Start wiring (docs/06 S0.3).

## What the sequencer does

* Arms the cycle, performs the steps before the injection (SIA dose into the cup), then waits for Inject Start.
* Times every later step from the **actual** Inject Start edge (and, in sequential mode, from the second edge of
  the conjugate injection), so Empower timing drift does not accumulate.
* **Watchdog → safe state** (V2 isolate, V3 bypass, V4 B, SIA stop, magnet on, cell off; docs/05 §4.1) if: an
  Inject Start is late beyond its tolerance (30 s; docs/02 §3.2), arrives early or unexpected, has the wrong line
  code, or any device reports an error. Each safe-state item is attempted even if another fails, and the raw trace
  recorded so far is still saved. Python never starts or stops Empower; the BSM keeps flowing to waste through the
  shunt and the bypass. If the PC itself crashes the valves stay where they are — a hardware heartbeat is a Stage-2
  TODO (docs/06 E2.1).
* **Fault latch** (docs/08 S12): a fault sets `fault_latch.json` in the sequence folder; every later run is still
  executed but flagged `valid: false` (metadata, result, log) and excluded by `analyze` until the recovery cycle
  (`config/cycle_recovery.yaml`) has completed. `run_sim` runs the recovery automatically after a fault; on the lab
  PC the same call is made by the orchestrator before the next cycle is armed.
* Writes the run log and raw data, computes the signal (generator charge minus a straight baseline fitted to the
  windows before and after the readout) and the time to result.

## Real-hardware stubs: what is missing (all UNVERIFIED until done at the bench)

| Device | File | Missing |
|---|---|---|
| IDEX MX Series II valves (MXP9960-000, MXP9900-000) | `devices/idex_mx.py` | RS-232/USB command syntax and baud rate from the MX Series II Operating Manual; or contact-closure wiring |
| SIA syringe pump (Hamilton PSD/6 or Tecan Centris) | `devices/syringe_pump.py` | the pump's OEM command language; mapping of dose/mix/empty/rinse to commands |
| LabJack U3 DAQ (Inject Start, line code, magnet TTL) | `devices/daq.py` | LabJackPython counter/digital I/O calls; Inject Start pulse width |
| Gamry (two channels) | `gamry_worker.py` (`ToolkitPyBackend`) | ToolkitPy calls; whether one process can drive two instruments; 600+/620 pairing |
| Empower | `devices/empower.py` | nothing for the primary scheme (passive); Toolkit control only if Waters confirms it can start a sample set |

## Signal and LOD definitions (identical to the validation protocol, docs/06 §7.4)

* Run signal S = ∫(i − baseline) dt over the readout window, baseline = least-squares line through the pre- and
  post-readout windows (`config/cycle_*.yaml`, `signal:`).
* Threshold = mean(blank S) + 3·SD (n − 1); LOD = 3·SD / b, with b the slope of the 0–10 pg/mL linear calibration
  through the blank mean. Also reported: free-intercept value, value with the 95 % upper bound of SD, 4PL inverse.
* Carry-over: for a 10 ng/mL challenge H → B1 → B2 (the criterion's test since the final review, S6),
  ((mean B1 − mean B2)/b)/10 000 pg/mL; after 1000 pg/mL standards (mean B1 − mean B2)/(mean H − mean B2), indicative.
* Hand-computed examples of each are in `tests/test_stats.py` and `tests/test_signal.py`.

## Deviation from docs/05 in the step tables

The 3.5-min cleaning step after the readout is split into 0.5 min of post-readout baseline (trap sealed, cell in
detect, fresh substrate) and 3.0 min of cleaning, so the charge can be corrected "with baseline windows before and
after" as docs/05 §4.1 requires. 3.0 min is inside the model range of `ma.timing.bead_flush_and_clean` (2–6 min);
the cycle length is unchanged. To be confirmed in E2.1.
