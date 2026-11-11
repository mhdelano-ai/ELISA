"""Run log and raw-data storage: one folder per run with
   events.jsonl  (every action, inject edge, warning and fault, with clock and cycle time)
   trace.csv     (t_s, ch1_A, ch2_A — raw current, never edited)
   metadata.json (sample, cycle file + sha256, devices, reagent lots, temperature, trace sha256)
   result.json   (per-run signal as defined in signal_proc.py)
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


class RunLog:
    def __init__(self, run_dir: str | Path, clock):
        self.dir = Path(run_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.clock = clock
        self.events = []
        self._fh = open(self.dir / "events.jsonl", "w", encoding="utf-8")

    def event(self, kind: str, cycle_min: float | None = None, **details):
        rec = {"t": self.clock.now(), "wall": self.clock.wall(), "kind": kind,
               "cycle_min": None if cycle_min is None else round(cycle_min, 6), **details}
        self.events.append(rec)
        self._fh.write(json.dumps(rec, default=str) + "\n")
        self._fh.flush()
        return rec

    def write_trace(self, trace: dict) -> str:
        p = self.dir / "trace.csv"
        with open(p, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["t_s", "ch1_A", "ch2_A"])
            ch2 = trace.get("ch2")
            for k, t in enumerate(trace["t"]):
                w.writerow([f"{t:.4f}", repr(float(trace["ch1"][k])), "" if ch2 is None else repr(float(ch2[k]))])
        return hashlib.sha256(p.read_bytes()).hexdigest()

    def write_json(self, name: str, obj: dict):
        (self.dir / name).write_text(json.dumps(obj, indent=2, default=str), encoding="utf-8")

    def close(self):
        if not self._fh.closed:
            self._fh.close()


def read_trace(run_dir: str | Path) -> dict:
    t, c1, c2 = [], [], []
    with open(Path(run_dir) / "trace.csv", newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            t.append(float(row["t_s"]))
            c1.append(float(row["ch1_A"]))
            c2.append(float(row["ch2_A"]) if row["ch2_A"] else None)
    return {"t": t, "ch1": c1, "ch2": None if all(v is None for v in c2) else c2}
