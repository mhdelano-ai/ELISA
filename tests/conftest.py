import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from elisa_sim.params import ParameterSet  # noqa: E402


@pytest.fixture(scope="session")
def ps():
    return ParameterSet.load()
