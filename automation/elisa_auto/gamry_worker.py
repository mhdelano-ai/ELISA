"""Gamry worker process — runs in GAMRY'S OWN PYTHON (Echem ToolkitPy ships a curated Python 3.7.9, 32-bit;
docs/02 s4.3 [V: GAMRY_TKPY_QSG]).

Why a separate process: the orchestrator needs Python >= 3.10 (64-bit, NumPy 2, the model package), while ToolkitPy
is tied to Gamry's 32-bit Python 3.7 and must not be mixed with another Python 3.7 32-bit installation. The two talk
over a local TCP socket (127.0.0.1 only) with one JSON object per line. This file therefore:
  * uses ONLY the Python standard library (no NumPy, no PyYAML, no pip install in Gamry's Python), and
  * uses only Python 3.7 syntax (checked by automation/tests/test_gamry_worker.py with ast feature_version 3.7).

Backends:
  * "sim"       — synthetic currents (background + drift + noise + an optional product peak); used by tests.
  * "toolkitpy" — STUB. Every place a ToolkitPy call belongs is marked TODO. The ToolkitPy module, class and method
                  names were NOT verified in this session (the manual could not be read), so none is written here.

Run:   <Gamry python.exe> gamry_worker.py --backend sim --port 50555
Protocol (request -> reply, each a JSON line):
  {"cmd": "hello"}                                  -> {"ok": true, "backend": ..., "python": "3.7.9", "bits": 32}
  {"cmd": "time"}                                   -> {"ok": true, "t": <worker monotonic s>}
  {"cmd": "configure", "channels": {...}, "sample_period_s": 0.1}
  {"cmd": "set_true_charge", "q_C": 5e-9}          (sim only: area of the product peak)
  {"cmd": "start"} / {"cmd": "mark", "label": "readout"} / {"cmd": "stop"} -> data
  {"cmd": "cell_off"} / {"cmd": "shutdown"}
"""
import argparse
import json
import math
import random
import socketserver
import sys
import threading
import time


class SimBackend(object):
    name = "sim"

    def __init__(self, seed=0, baseline_A=5e-11, drift_A_per_s=1e-14, noise_rms_A=4e-13, collector_fraction=-0.8):
        self.rng = random.Random(seed)
        self.baseline_A = baseline_A
        self.drift = drift_A_per_s
        self.noise = noise_rms_A
        self.collector_fraction = collector_fraction
        self.channels = {}
        self.sample_period_s = 0.1
        self.t_start = None
        self.marks = []
        self.q_C = 0.0

    def configure(self, channels, sample_period_s):
        self.channels = dict(channels)
        self.sample_period_s = float(sample_period_s)

    def set_true_charge(self, q_C):
        self.q_C = float(q_C)

    def start(self):
        self.t_start = time.monotonic()
        self.marks = [[self.t_start, "start"]]

    def mark(self, label):
        if self.t_start is None:
            raise RuntimeError("mark before start")
        self.marks.append([time.monotonic(), label])

    def stop(self):
        if self.t_start is None:
            raise RuntimeError("stop before start")
        t_stop = time.monotonic()
        n = int(math.floor((t_stop - self.t_start) / self.sample_period_s)) + 1
        t = [self.t_start + k * self.sample_period_s for k in range(n)]
        labels = [m[1] for m in self.marks]
        a = b = None
        if "readout" in labels:
            i = labels.index("readout")
            a = self.marks[i][0]
            b = self.marks[i + 1][0] if i + 1 < len(self.marks) else t_stop
        shape = [0.0] * n
        if a is not None and b > a:
            w = 0.8 * (b - a)
            for k, tk in enumerate(t):
                if a <= tk <= a + w:
                    shape[k] = math.sin(math.pi * (tk - a) / w) ** 2
        area = 0.0
        for k in range(1, n):
            area += 0.5 * (shape[k] + shape[k - 1]) * (t[k] - t[k - 1])
        scale = self.q_C / area if area > 0 else 0.0
        ch1, ch2 = [], []
        for k, tk in enumerate(t):
            bg = self.baseline_A + self.drift * (tk - self.t_start)
            pk = scale * shape[k]
            ch1.append(bg + pk + self.rng.gauss(0.0, self.noise))
            ch2.append(0.2 * bg + self.collector_fraction * pk + self.rng.gauss(0.0, self.noise))
        two = ("2" in self.channels) or (2 in self.channels)
        out = {"t": t, "ch1": ch1, "ch2": ch2 if two else None, "marks": self.marks + [[t_stop, "stop"]]}
        self.t_start = None
        return out

    def cell_off(self):
        pass


class ToolkitPyBackend(object):
    """STUB for real Gamry instruments through Echem ToolkitPy (Gamry software >= 7.10.4; docs/02 s4.3).

    Everything here is TODO because the ToolkitPy API was not verified in this session:
      * open the instrument(s): channel 1 = Reference 600+ (generator), channel 2 = second instrument (collector).
        A second channel is needed only for the optional IDA (docs/08 S9; default is one channel). Gamry's
        bipotentiostat page lists Reference 620+620, 3000+3000, 620+3000 (and Interface pairs) and shows a video of
        two 600+ units; a 600+/620 pair is not shown (docs/08 s9 C11). Whether one ToolkitPy process can drive two
        instruments is UNVERIFIED (S0.2).
      * cell on, set the DC potential of each channel (vs Ag/AgCl), choose a fixed current range (60 pA-6 nA region
        expected; autoranging would add steps to the integrated charge), set the sampling mode (Noise Reject or
        Surface averaging over whole mains cycles, docs/02 s4.4).
      * continuous chronoamperometry from start() to stop(), samples buffered with the instrument time base; record
        the worker monotonic time at the acquisition start so the orchestrator can align clocks.
      * mark(): store (time.monotonic(), label); no instrument call needed.
      * cell_off(): cell switch off (safe state) — must work even if an acquisition is running.
      * reading the Misc. I/O TTL inputs from ToolkitPy is UNVERIFIED (docs/02 s4.2); Inject Start therefore goes to
        the separate DAQ, not to the Gamry.
    """
    name = "toolkitpy"

    def __init__(self, **kw):
        raise NotImplementedError("ToolkitPy backend not implemented: see the TODO list in ToolkitPyBackend "
                                  "(API names UNVERIFIED; read the Echem ToolkitPy manual installed with Gamry "
                                  "software)")


def make_handler(backend, stop_event):
    class Handler(socketserver.StreamRequestHandler):
        def handle(self):
            for raw in self.rfile:
                line = raw.decode("utf-8").strip()
                if not line:
                    continue
                try:
                    req = json.loads(line)
                    rep = dispatch(backend, req, stop_event)
                except Exception as e:  # report every failure to the client; the client goes to safe state
                    rep = {"ok": False, "error": "%s: %s" % (type(e).__name__, e)}
                self.wfile.write((json.dumps(rep) + "\n").encode("utf-8"))
                self.wfile.flush()
                if stop_event.is_set():
                    return
    return Handler


def dispatch(backend, req, stop_event):
    cmd = req.get("cmd")
    if cmd == "hello":
        return {"ok": True, "backend": backend.name, "python": "%d.%d.%d" % sys.version_info[:3],
                "bits": 64 if sys.maxsize > 2 ** 32 else 32}
    if cmd == "time":
        return {"ok": True, "t": time.monotonic()}
    if cmd == "configure":
        backend.configure(req.get("channels", {}), req.get("sample_period_s", 0.1))
        return {"ok": True}
    if cmd == "set_true_charge":
        if not hasattr(backend, "set_true_charge"):
            raise RuntimeError("set_true_charge is a simulation-only command")
        backend.set_true_charge(req["q_C"])
        return {"ok": True}
    if cmd == "start":
        backend.start()
        return {"ok": True}
    if cmd == "mark":
        backend.mark(req.get("label", ""))
        return {"ok": True}
    if cmd == "stop":
        return {"ok": True, "data": backend.stop()}
    if cmd == "cell_off":
        backend.cell_off()
        return {"ok": True}
    if cmd == "shutdown":
        stop_event.set()
        return {"ok": True}
    raise ValueError("unknown command %r" % (cmd,))


def serve(backend, host="127.0.0.1", port=50555, ready_file=None):
    stop_event = threading.Event()
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer((host, port), make_handler(backend, stop_event))
    if ready_file:
        with open(ready_file, "w") as f:
            f.write(str(server.server_address[1]))
    server.timeout = 0.2
    while not stop_event.is_set():
        server.handle_request()
    server.server_close()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Gamry worker (run in Gamry's Python 3.7, 32-bit)")
    ap.add_argument("--backend", choices=["sim", "toolkitpy"], default="sim")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=50555)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--ready-file", default=None, help="write the bound port here when listening (tests)")
    a = ap.parse_args(argv)
    if a.host not in ("127.0.0.1", "localhost"):
        ap.error("the worker only listens on the local machine")
    backend = SimBackend(seed=a.seed) if a.backend == "sim" else ToolkitPyBackend()
    serve(backend, a.host, a.port, a.ready_file)


if __name__ == "__main__":
    main()
