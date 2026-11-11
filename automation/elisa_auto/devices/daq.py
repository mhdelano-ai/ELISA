"""USB DAQ for Inject Start (and the 2-bit line code) and TTL outputs (magnet) — STUB.

Verified to exist (docs/07 s0): LabJack U3 with the LabJackPython package (pip install LabJackPython; needs the UD
driver on Windows). Its counter/digital-input calls were seen only in forum snippets — not transcribed here.

TODO (bench, Stage 0, S0.3):
  1. Install the LabJack UD driver and LabJackPython on the orchestrator Python (64-bit, >= 3.10).
  2. Wire SM-FL Inject Start (connector 1 pins 1-2, docs/02 s3.1) through an opto-isolator to a digital line; use a
     hardware counter or edge-capture so a short pulse (width UNVERIFIED) is never missed by polling.
  3. Implement poll(): read the counter; for each new count return InjectEvent(t=clock.now(), line_code=<code
     lines read at the edge, if wired>), then verify against 10 manual injections (S0.3).
  4. Magnet: one digital output line through a driver/relay to the actuator (docs/07 s2).
"""
from __future__ import annotations

from .base import InjectStartInput, Magnet


class LabJackInjectStart(InjectStartInput):
    def __init__(self, clock, line, code_lines=None):
        self.clock, self.line, self.code_lines = clock, line, list(code_lines or [])

    def poll(self):  # pragma: no cover - lab only
        # TODO: LabJackPython counter read (UNVERIFIED call names) -> InjectEvent list.
        raise NotImplementedError("LabJack Inject Start input not implemented (docs/07 s0, UNVERIFIED API)")


class DaqTTLMagnet(Magnet):
    def __init__(self, line):
        self.line, self._on = line, False

    def set(self, on):  # pragma: no cover - lab only
        # TODO: LabJackPython digital output write (UNVERIFIED call names).
        raise NotImplementedError("DAQ TTL output not implemented (UNVERIFIED API)")

    def is_on(self):
        return self._on
