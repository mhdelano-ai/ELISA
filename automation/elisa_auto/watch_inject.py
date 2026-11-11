"""Stage-0 tool (docs/06 S0.3): print every Inject Start edge seen by the DAQ, with time stamps.

    python -m elisa_auto.watch_inject --hw automation/config/hardware_lab.yaml
    python -m elisa_auto.watch_inject --demo          # no hardware: three simulated edges

With the lab configuration this calls the LabJack stub, which raises NotImplementedError until the DAQ driver is
written (devices/daq.py TODO list)."""
from __future__ import annotations

import argparse
import time

from .clock import RealClock, SimClock
from .devices.sim import SimInjectStart


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--hw", default=None)
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--seconds", type=float, default=600)
    a = ap.parse_args(argv)
    if a.demo or not a.hw:
        clock = SimClock()
        inp = SimInjectStart(clock)
        for t in (5.0, 65.0, 125.0):
            inp.schedule(t, 1)
    else:  # pragma: no cover - lab only
        from .devices.daq import LabJackInjectStart
        from .hardware import load_hw
        hw = load_hw(a.hw)
        clock = RealClock()
        inp = LabJackInjectStart(clock, hw["inject_start"]["line"], hw["inject_start"].get("code_lines"))
    t_end = clock.now() + a.seconds
    n = 0
    while clock.now() < t_end:
        ev = inp.poll()
        if ev:
            n += 1
            print(f"Inject Start #{n}: t = {ev.t:.3f} s  line code = {ev.line_code}  ({clock.wall()})", flush=True)
        clock.sleep(0.01 if not clock.simulated else 0.5)
    print(f"{n} edges in {a.seconds:g} s")


if __name__ == "__main__":
    main()
