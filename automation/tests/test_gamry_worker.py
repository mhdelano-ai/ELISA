"""Gamry worker: Python 3.7 syntax, stdlib only, and the socket protocol end to end (sim backend)."""
import ast
import subprocess
import sys
import time
from pathlib import Path

import pytest

from elisa_auto.clock import RealClock
from elisa_auto.devices.gamry_client import GamryWorkerPotentiostat

WORKER = Path(__file__).resolve().parents[1] / "elisa_auto" / "gamry_worker.py"


def test_worker_is_python37_syntax_and_stdlib_only():
    src = WORKER.read_text()
    tree = ast.parse(src, feature_version=(3, 7))     # fails on 3.8+ syntax (walrus, pos-only args, ...)
    allowed = {"argparse", "json", "math", "random", "socketserver", "sys", "threading", "time"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert {a.name.split(".")[0] for a in node.names} <= allowed
        if isinstance(node, ast.ImportFrom):
            assert node.module.split(".")[0] in allowed
        assert not isinstance(node, ast.NamedExpr)


def test_worker_protocol_sim(tmp_path):
    ready = tmp_path / "port.txt"
    proc = subprocess.Popen([sys.executable, str(WORKER), "--backend", "sim", "--port", "0", "--ready-file", str(ready)])
    try:
        for _ in range(100):
            if ready.exists() and ready.read_text():
                break
            time.sleep(0.05)
        port = int(ready.read_text())
        pot = GamryWorkerPotentiostat(RealClock(), port=port)
        info = pot.connect()
        assert info["backend"] == "sim"
        pot.configure({1: {"role": "generator"}, 2: {"role": "collector"}}, 0.01)
        pot.set_true_charge(2e-12)
        pot.start_acquisition()
        time.sleep(0.2)
        pot.mark("readout")
        time.sleep(0.5)
        pot.mark("post_baseline")
        time.sleep(0.2)
        d = pot.stop_acquisition()
        assert len(d["t"]) > 50 and d["ch2"] is not None
        assert abs(d["t"][0] - RealClock().now()) < 5          # converted to the orchestrator clock
        pot.cell_off()
        pot.shutdown()
        proc.wait(timeout=5)
    finally:
        if proc.poll() is None:
            proc.kill()


def test_toolkitpy_backend_is_an_explicit_stub():
    import importlib.util
    spec = importlib.util.spec_from_file_location("gw", WORKER)
    gw = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gw)
    with pytest.raises(NotImplementedError):
        gw.ToolkitPyBackend()
