"""Abstract device interfaces used by the sequencer. Every real driver and every simulator implements these."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class DeviceError(RuntimeError):
    """Raised by a driver on any communication or state error; the sequencer goes to the safe state."""


class Valve(ABC):
    name: str
    positions: list

    @abstractmethod
    def set_position(self, position: str) -> None: ...

    @abstractmethod
    def get_position(self) -> str: ...


class SIAModule(ABC):
    """Syringe pump + selection valve (docs/05 s4.0 route A): doses beads/conjugate, mixes and empties the cup."""

    @abstractmethod
    def execute(self, command: dict) -> None:
        """command: the step-table 'sia' dict, e.g. {'action': 'dispense', 'from': 'reservoir', 'to': 'cup',
        'volume_uL': 20}. Must return quickly (start the move) — long moves run in the device."""

    @abstractmethod
    def stop(self) -> None: ...

    @abstractmethod
    def is_busy(self) -> bool: ...


class Magnet(ABC):
    @abstractmethod
    def set(self, on: bool) -> None: ...

    @abstractmethod
    def is_on(self) -> bool: ...


@dataclass
class InjectEvent:
    t: float                 # clock time of the edge
    line_code: int | None    # 2-bit code from BSM event outputs if wired (docs/02 s3.2 point 2), else None


class InjectStartInput(ABC):
    """SM-FL Inject Start contact closure (connector 1, pins 1-2; docs/02 s3.1) on an isolated DAQ input."""

    @abstractmethod
    def poll(self) -> InjectEvent | None:
        """Return the next unread edge (oldest first) or None. Must not block."""


class Potentiostat(ABC):
    """One or two synchronised channels (generator, collector). Real implementation: GamryWorkerPotentiostat."""

    @abstractmethod
    def configure(self, channels: dict, sample_period_s: float) -> None: ...

    @abstractmethod
    def start_acquisition(self) -> None: ...

    @abstractmethod
    def mark(self, label: str) -> None: ...

    @abstractmethod
    def stop_acquisition(self) -> dict:
        """Stop and return {'t': [...], 'ch1': [...], 'ch2': [...] or None, 'marks': [(t, label), ...]}
        with t on the orchestrator clock (seconds)."""

    @abstractmethod
    def cell_off(self) -> None: ...


class Empower(ABC):
    """The Waters side. In the primary scheme (docs/02 s3.2) Empower is the master and Python only listens, so the
    default implementation is passive."""

    @abstractmethod
    def describe(self) -> str: ...

    def start_sample_set(self, name: str) -> None:  # optional (docs/02 Fallback A)
        raise NotImplementedError("Python does not start Empower in the primary scheme (docs/02 s3.2)")
