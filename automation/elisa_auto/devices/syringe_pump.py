"""SIA module driver (syringe pump + distribution valve) — STUB.

Candidates verified to exist (docs/07 s2): Hamilton PSD/6 (RS-232/RS-485/CAN, 9600 or 38400 baud; 8-port
distribution valve listed in the PSD/6 spec sheet) and Tecan Cavro Centris (RS-232/485, 9600/38400 baud;
distribution valves with 3, 6, 9, 12 ports). Their command languages were NOT read in this session.

TODO (bench, Stage 2):
  1. Pick the pump; obtain its OEM communication manual; transcribe: initialise, select valve port, aspirate volume
     at speed, dispense volume at speed, query busy/ready, terminate.
  2. Map the step-table actions: dispense (reservoir -> cup), mix (aspirate/dispense 50 uL at the cup port),
     empty_cup_through_trap (aspirate cup, dispense to_trap at 100 uL/min), rinse_cup (wash -> cup -> waste x3).
  3. Measure the delivered volume gravimetrically (E2.2) and the bead dose CV.
"""
from __future__ import annotations

from .base import DeviceError, SIAModule


class CavroTypeSIA(SIAModule):
    def __init__(self, port, baud=9600, syringe_uL=1000, ports=None):
        self.port, self.baud, self.syringe_uL = port, baud, syringe_uL
        self.ports = dict(ports or {})
        self._busy = False

    def _send(self, cmd: str) -> str:  # pragma: no cover - lab only
        # TODO: vendor command string and reply parsing (UNVERIFIED; do not guess).
        raise NotImplementedError("syringe-pump command set not transcribed yet (docs/07 s2, UNVERIFIED)")

    def execute(self, command):
        action = command.get("action")
        if action not in ("dispense", "mix", "empty_cup_through_trap", "rinse_cup", "aspirate", "flush_channel",
                          "flush_trap"):
            raise DeviceError(f"unknown SIA action {action}")
        # TODO: translate each action into the vendor's command sequence (see module docstring).
        self._send(repr(command))

    def stop(self):
        # TODO: vendor 'terminate' command. Must be safe to call at any time (safe state).
        self._send("TERMINATE")

    def is_busy(self):
        return self._busy
