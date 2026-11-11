"""Fault latch across runs (final review docs/08 S12).

After a fault the safe state keeps the magnet ON, so that run's beads stay in the trap, and Empower keeps injecting
the next samples. Nothing used to stop the next run from reading those beads. The latch is a small JSON file in the
sequence folder:
  * a fault in any run SETS it (run id, reason, time);
  * while it is set, every run is executed but flagged INVALID in its metadata and result (analysis excludes it);
  * only a recovery cycle (config/cycle_recovery.yaml: magnet off, 300 uL/min flush of the trap, cup rinse) that
    completes with status 'ok' CLEARS it, and the clearing is logged with the recovery run's id.
The file survives a restart of the orchestrator, so a crash after a fault cannot silently clear it.
"""
from __future__ import annotations

import json
import time
from pathlib import Path


class FaultLatch:
    FILE = "fault_latch.json"

    def __init__(self, folder):
        self.path = Path(folder) / self.FILE
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def state(self) -> dict:
        if self.path.exists():
            return json.loads(self.path.read_text(encoding="utf-8"))
        return {"set": False, "history": []}

    @property
    def is_set(self) -> bool:
        return bool(self.state().get("set"))

    def _write(self, st: dict):
        self.path.write_text(json.dumps(st, indent=2), encoding="utf-8")

    def set(self, run_id: str, reason: str):
        st = self.state()
        if not st.get("set"):
            st.update(set=True, since_run=run_id, reason=reason, set_wall=time.time())
        st.setdefault("history", []).append({"event": "set", "run": run_id, "reason": reason, "wall": time.time()})
        self._write(st)

    def clear(self, recovery_run_id: str):
        st = self.state()
        st.setdefault("history", []).append({"event": "cleared", "run": recovery_run_id, "wall": time.time(),
                                             "was_set_by": st.get("since_run")})
        st.update(set=False, since_run=None, reason=None, cleared_by=recovery_run_id)
        self._write(st)
