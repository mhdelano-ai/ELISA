"""IDEX Health & Science (Rheodyne) MX Series II 2-position valve driver — STUB.

Verified (docs/07 s2): MXP9960-000 (2-position 10-port PEEK) and MXP9900-000 (2-position 6-port PEEK) exist; the MX
Series II Operating Manual states modules can be operated by push button or remotely by contact closure, I2C,
RS-232 or USB (RS-232 only if factory-set). The serial command set was NOT read in this session.

TODO (bench, Stage 2):
  1. Obtain the "MX Series II Operating Manual" (IDEX document) and transcribe the RS-232/USB command that moves to
     a position and the one that reports the current position, plus baud rate and terminator.
  2. Implement _send() with pyserial and confirm with a loop-back test (move A->B->A 100 times, read back each).
  3. Alternatively drive the valve by contact closure from the DAQ (manual: contact-closure input) and read the
     position output if the model has one (UNVERIFIED).
Nothing below sends a vendor command.
"""
from __future__ import annotations

from .base import DeviceError, Valve


class IdexMxValve(Valve):
    def __init__(self, name, port, positions, position_map, baud=None, timeout_s=2.0):
        self.name, self.port, self.positions = name, port, list(positions)
        self.position_map = dict(position_map)       # logical name -> valve position number (1/2)
        self.baud, self.timeout_s = baud, timeout_s  # baud UNVERIFIED: take from the manual
        self._ser = None
        self._last = None

    def open(self):
        try:
            import serial  # pyserial (optional dependency 'lab')
        except ImportError as e:  # pragma: no cover - lab only
            raise DeviceError("pyserial not installed: pip install -e automation[lab]") from e
        if self.baud is None:
            raise DeviceError(f"{self.name}: baud rate not configured (UNVERIFIED; read the MX Series II manual)")
        self._ser = serial.Serial(self.port, self.baud, timeout=self.timeout_s)

    def _send(self, payload: str) -> str:  # pragma: no cover - lab only
        # TODO: MX Series II command syntax (move-to-position / query-position) from the IDEX manual. UNVERIFIED.
        raise NotImplementedError("IDEX MX Series II serial protocol not transcribed yet (docs/07 s2, UNVERIFIED)")

    def set_position(self, position):
        if position not in self.position_map:
            raise DeviceError(f"{self.name}: unknown position {position}")
        self._send(f"MOVE {self.position_map[position]}")   # placeholder text, NOT a vendor command
        self._last = position

    def get_position(self):
        # TODO: query the valve; until then return the last commanded position.
        return self._last
