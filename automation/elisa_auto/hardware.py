"""Build the device set from a hardware YAML (config/hardware_sim.yaml or hardware_lab.yaml)."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .devices import sim
from .devices.base import Empower, InjectStartInput, Magnet, Potentiostat, SIAModule


@dataclass
class Devices:
    valves: dict
    sia: SIAModule
    magnet: Magnet
    inject: InjectStartInput
    potentiostat: Potentiostat
    empower: Empower
    extra: dict = field(default_factory=dict)

    def valve_positions(self) -> dict:
        return {k: list(v.positions) for k, v in self.valves.items()}


def load_hw(path: str | Path) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def build_sim(clock, hw: dict, fail_valve: tuple | None = None) -> Devices:
    """All-simulated devices. fail_valve = (valve, position) makes that move raise (fault-injection tests)."""
    s = hw.get("sim", {})
    valves = {}
    for name, v in hw["valves"].items():
        fo = fail_valve[1] if (fail_valve and fail_valve[0] == name) else None
        valves[name] = sim.SimValve(name, v["positions"], v.get("initial"), clock, fail_on=fo)
    inj = sim.SimInjectStart(clock)
    pot = sim.SimPotentiostat(clock, baseline_A=s.get("baseline_current_A", 5e-11),
                              drift_A_per_s=s.get("drift_A_per_s", 1e-14), noise_rms_A=s.get("noise_rms_A", 4e-13),
                              collector_fraction=s.get("collector_fraction", -0.8), seed=s.get("seed", 0))
    return Devices(valves=valves, sia=sim.SimSIA(clock), magnet=sim.SimMagnet(clock), inject=inj,
                   potentiostat=pot, empower=sim.SimEmpower(inj, s.get("inject_delay_s", 0.0)))


def build_lab(clock, hw: dict) -> Devices:  # pragma: no cover - lab only
    """Real devices. Every driver is a stub today (raises NotImplementedError at the vendor call)."""
    from .devices.daq import DaqTTLMagnet, LabJackInjectStart
    from .devices.empower import PassiveEmpower
    from .devices.gamry_client import GamryWorkerPotentiostat
    from .devices.idex_mx import IdexMxValve
    from .devices.syringe_pump import CavroTypeSIA
    valves = {n: IdexMxValve(n, v["port"], v["positions"], v["position_map"], v.get("baud"))
              for n, v in hw["valves"].items()}
    s = hw["sia"]
    p = hw["potentiostat"]
    return Devices(valves=valves,
                   sia=CavroTypeSIA(s["port"], s.get("baud", 9600), s.get("syringe_uL", 1000), s.get("ports")),
                   magnet=DaqTTLMagnet(hw["magnet"]["line"]),
                   inject=LabJackInjectStart(clock, hw["inject_start"]["line"], hw["inject_start"].get("code_lines")),
                   potentiostat=GamryWorkerPotentiostat(clock, p.get("host", "127.0.0.1"), p.get("port", 50555)),
                   empower=PassiveEmpower())
