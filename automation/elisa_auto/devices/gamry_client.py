"""Client side of the Gamry worker (gamry_worker.py), implementing the Potentiostat interface.

The worker runs in Gamry's 32-bit Python 3.7; this client runs in the orchestrator's Python. Times returned by
the worker are converted to the orchestrator clock with an offset measured at configure() (round-trip midpoint).
"""
from __future__ import annotations

import json
import socket
import subprocess

from .base import DeviceError, Potentiostat


class GamryWorkerPotentiostat(Potentiostat):
    def __init__(self, clock, host="127.0.0.1", port=50555, timeout_s=30.0):
        if clock.simulated:
            raise DeviceError("the Gamry worker runs in real time; use SimPotentiostat with a SimClock")
        self.clock, self.host, self.port, self.timeout_s = clock, host, port, timeout_s
        self._sock = None
        self._file = None
        self.offset = 0.0
        self.info = {}

    # ---- transport ------------------------------------------------------------------------------------
    def connect(self):
        try:
            self._sock = socket.create_connection((self.host, self.port), timeout=self.timeout_s)
        except OSError as e:
            raise DeviceError(f"cannot reach Gamry worker at {self.host}:{self.port}: {e}") from e
        self._file = self._sock.makefile("rwb")
        self.info = self._call({"cmd": "hello"})
        return self.info

    def _call(self, req: dict) -> dict:
        if self._file is None:
            raise DeviceError("Gamry worker not connected")
        try:
            self._file.write((json.dumps(req) + "\n").encode())
            self._file.flush()
            line = self._file.readline()
        except OSError as e:
            raise DeviceError(f"Gamry worker I/O error: {e}") from e
        if not line:
            raise DeviceError("Gamry worker closed the connection")
        rep = json.loads(line)
        if not rep.get("ok"):
            raise DeviceError(f"Gamry worker error: {rep.get('error')}")
        return rep

    def _sync_clock(self):
        t0 = self.clock.now()
        tw = self._call({"cmd": "time"})["t"]
        t1 = self.clock.now()
        self.offset = 0.5 * (t0 + t1) - tw

    # ---- Potentiostat interface -------------------------------------------------------------------------
    def configure(self, channels, sample_period_s):
        if self._file is None:
            self.connect()
        self._sync_clock()
        self._call({"cmd": "configure", "channels": {str(k): v for k, v in channels.items()},
                    "sample_period_s": sample_period_s})

    def set_true_charge(self, q_C):  # simulation backend only
        self._call({"cmd": "set_true_charge", "q_C": q_C})

    def start_acquisition(self):
        self._call({"cmd": "start"})

    def mark(self, label):
        self._call({"cmd": "mark", "label": label})

    def stop_acquisition(self):
        d = self._call({"cmd": "stop"})["data"]
        d["t"] = [t + self.offset for t in d["t"]]
        d["marks"] = [(t + self.offset, lab) for t, lab in d["marks"]]
        return d

    def cell_off(self):
        self._call({"cmd": "cell_off"})

    def shutdown(self):
        try:
            self._call({"cmd": "shutdown"})
        finally:
            if self._sock:
                self._sock.close()
            self._sock = self._file = None


def launch_worker(python_exe: str, worker_py: str, port: int, backend: str = "sim", ready_file: str | None = None):
    """Start the worker as a child process (on the lab PC python_exe is Gamry's python.exe)."""
    cmd = [python_exe, worker_py, "--backend", backend, "--port", str(port)]
    if ready_file:
        cmd += ["--ready-file", ready_file]
    return subprocess.Popen(cmd)
