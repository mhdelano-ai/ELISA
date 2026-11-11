"""Simulated devices. Deterministic (seeded) so tests can check timing and signal processing exactly."""
from __future__ import annotations

import math

import numpy as np

from ..numutil import trapz
from .base import (DeviceError, Empower, InjectEvent, InjectStartInput, Magnet, Potentiostat, SIAModule,
                   Valve)


class SimValve(Valve):
    def __init__(self, name, positions, initial=None, clock=None, fail_on=None):
        self.name, self.positions = name, list(positions)
        self._pos = initial or self.positions[0]
        self.clock = clock
        self.history = []          # (t, position)
        self.fail_on = fail_on     # position name that raises DeviceError (fault injection for tests)

    def set_position(self, position):
        if position not in self.positions:
            raise DeviceError(f"{self.name}: no position {position!r}")
        if self.fail_on is not None and position == self.fail_on:
            raise DeviceError(f"{self.name}: simulated actuator fault moving to {position}")
        self._pos = position
        self.history.append((self.clock.now() if self.clock else None, position))

    def get_position(self):
        return self._pos


class SimSIA(SIAModule):
    def __init__(self, clock=None, ports=None):
        self.clock = clock
        self.commands = []
        self.stopped = False
        self.ports = dict(ports or {})      # name -> selection-valve port number (empty = not checked)

    def execute(self, command):
        if self.ports:
            for k in ("from", "to", "port"):
                if command.get(k) and command[k] not in self.ports:
                    raise DeviceError(f"SIA: no selection-valve port named {command[k]!r}")
        self.commands.append((self.clock.now() if self.clock else None, dict(command)))

    def stop(self):
        self.stopped = True
        self.commands.append((self.clock.now() if self.clock else None, {"action": "stop"}))

    def is_busy(self):
        return False


class SimMagnet(Magnet):
    def __init__(self, clock=None):
        self.clock, self._on, self.history = clock, False, []

    def set(self, on):
        self._on = bool(on)
        self.history.append((self.clock.now() if self.clock else None, self._on))

    def is_on(self):
        return self._on


class SimInjectStart(InjectStartInput):
    """Fires Inject Start edges at scheduled clock times (set by the simulated Empower 'schedule')."""

    def __init__(self, clock):
        self.clock = clock
        self._pending = []     # (t, code)

    def schedule(self, t, line_code=None):
        self._pending.append((float(t), line_code))
        self._pending.sort(key=lambda x: x[0])

    def poll(self):
        if self._pending and self._pending[0][0] <= self.clock.now() + 1e-12:
            t, code = self._pending.pop(0)
            return InjectEvent(t=t, line_code=code)
        return None


class SimEmpower(Empower):
    """Plays the Empower sample-set role in simulation: schedules Inject Start edges as Empower would."""

    def __init__(self, inject_input: SimInjectStart, delay_s: float = 0.0):
        self.inject_input, self.delay_s = inject_input, delay_s

    def describe(self):
        return "simulated Empower (schedules Inject Start edges)"

    def plan_cycle(self, cycle, t_arm: float, omit: set | None = None, extra_delay: dict | None = None):
        """Schedule the cycle's inject edges relative to the arm time (cycle time = cycle.start_min at t_arm)."""
        omit, extra_delay = omit or set(), extra_delay or {}
        for inj in cycle.injects:
            if inj.name in omit:
                continue
            t = t_arm + (inj.at_min - cycle.start_min) * 60.0 + self.delay_s + extra_delay.get(inj.name, 0.0)
            self.inject_input.schedule(t, inj.line_code)


class SimPotentiostat(Potentiostat):
    """Generates a two-channel current trace on stop: background + drift + white noise, plus a product peak
    between the 'readout' mark and the next mark whose area (charge) is set per run by ``set_true_charge``."""

    def __init__(self, clock, baseline_A=5e-11, drift_A_per_s=1e-14, noise_rms_A=4e-13, collector_fraction=-0.8,
                 seed=0):
        self.clock = clock
        self.baseline_A, self.drift, self.noise = baseline_A, drift_A_per_s, noise_rms_A
        self.collector_fraction = collector_fraction
        self.rng = np.random.default_rng(seed)
        self.sample_period_s = 0.1
        self.channels = {}
        self._t_start = None
        self._marks = []
        self.true_charge_C = 0.0
        self.cell_is_off = True

    def configure(self, channels, sample_period_s):
        self.channels, self.sample_period_s = dict(channels), float(sample_period_s)

    def set_true_charge(self, q_C: float):
        self.true_charge_C = float(q_C)

    def start_acquisition(self):
        self._t_start = self.clock.now()
        self._marks = [(self._t_start, "start")]
        self.cell_is_off = False

    def mark(self, label):
        if self._t_start is None:
            raise DeviceError("mark before start_acquisition")
        self._marks.append((self.clock.now(), label))

    def stop_acquisition(self):
        if self._t_start is None:
            raise DeviceError("stop before start")
        t_stop = self.clock.now()
        n = int(math.floor((t_stop - self._t_start) / self.sample_period_s)) + 1
        t = self._t_start + np.arange(n) * self.sample_period_s
        bg = self.baseline_A + self.drift * (t - self._t_start)
        peak = np.zeros(n)
        labels = [m[1] for m in self._marks]
        if "readout" in labels:
            i = labels.index("readout")
            a = self._marks[i][0]
            b = self._marks[i + 1][0] if i + 1 < len(self._marks) else t_stop
            # smooth peak shape (sin^2) occupying the first 80 % of the readout window, unit area * charge
            w = 0.8 * (b - a)
            inside = (t >= a) & (t <= a + w)
            shape = np.zeros(n)
            shape[inside] = np.sin(np.pi * (t[inside] - a) / w) ** 2
            shape_area = trapz(shape, t) if shape.any() else 1.0
            peak = self.true_charge_C * shape / shape_area
        ch1 = bg + peak + self.rng.normal(0.0, self.noise, n)
        ch2 = None
        if 2 in self.channels or "2" in self.channels:
            ch2 = 0.2 * bg + self.collector_fraction * peak + self.rng.normal(0.0, self.noise, n)
        out = {"t": t.tolist(), "ch1": ch1.tolist(), "ch2": None if ch2 is None else ch2.tolist(),
               "marks": list(self._marks) + [(t_stop, "stop")]}
        self._t_start = None
        return out

    def cell_off(self):
        self.cell_is_off = True
