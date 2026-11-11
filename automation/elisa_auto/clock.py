"""Clocks. RealClock for the lab PC (one monotonic clock for every event, docs/02 s3.1 "all events must be
timestamped on one PC clock"); SimClock (virtual time) so a 56-min cycle runs in well under a second in tests."""
from __future__ import annotations

import time
from datetime import datetime, timezone


class RealClock:
    simulated = False

    def now(self) -> float:
        return time.monotonic()

    def sleep(self, seconds: float) -> None:
        if seconds > 0:
            time.sleep(seconds)

    def wall(self) -> str:
        return datetime.now(timezone.utc).isoformat()


class SimClock:
    """Virtual time in seconds. sleep() advances time instantly."""
    simulated = True

    def __init__(self, t0: float = 0.0):
        self._t = float(t0)

    def now(self) -> float:
        return self._t

    def sleep(self, seconds: float) -> None:
        if seconds > 0:
            self._t += seconds

    def wall(self) -> str:
        return f"virtual+{self._t:.3f}s"
