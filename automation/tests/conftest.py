import sys
from pathlib import Path

import pytest

AUTO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AUTO))

CFG = AUTO / "config"


@pytest.fixture
def primary():
    from elisa_auto.cycle import load_cycle
    return load_cycle(CFG / "cycle_primary.yaml")


@pytest.fixture
def sequential():
    from elisa_auto.cycle import load_cycle
    return load_cycle(CFG / "cycle_sequential.yaml")


@pytest.fixture
def hw_sim():
    from elisa_auto.hardware import load_hw
    return load_hw(CFG / "hardware_sim.yaml")
