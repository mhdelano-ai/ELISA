"""Gate thresholds (config/gates.yaml) and verdict text for the quantities docs/06 asks for at G1-G3."""
from __future__ import annotations

from pathlib import Path

import yaml

DEFAULT_GATES = Path(__file__).resolve().parents[1] / "config" / "gates.yaml"


def load_gates(path=None) -> dict:
    return yaml.safe_load(Path(path or DEFAULT_GATES).read_text(encoding="utf-8"))


def verdict(g: dict, value: float) -> str:
    """Generic reading of a threshold dict. Keys: confirm_max/confirm_min, kill_min, stop_min/stop_max,
    backup_min/backup_max, reject_min, coat_min, add_wash_min, l5_min, go_max, max, min."""
    if value is None or value != value:
        return "no data"
    src = g.get("source", "")
    if "kill_min" in g and value > g["kill_min"]:
        return f"KILL (> {g['kill_min']:g}; {src})"
    if "reject_min" in g and value > g["reject_min"]:
        return f"REJECT (> {g['reject_min']:g}; {src})"
    if "stop_min" in g and value > g["stop_min"]:
        return f"STOP (> {g['stop_min']:g}; {src})"
    if "stop_max" in g and value < g["stop_max"]:
        return f"STOP (< {g['stop_max']:g}; {src})"
    if "backup_min" in g and value > g["backup_min"]:
        return f"GO TO BACKUP (> {g['backup_min']:g}; {src})"
    if "backup_max" in g and value < g["backup_max"]:
        return f"GO TO BACKUP (< {g['backup_max']:g}; {src})"
    if "confirm_max" in g:
        return (f"PASS (<= {g['confirm_max']:g}; {src})" if value <= g["confirm_max"]
                else f"INTERMEDIATE (> {g['confirm_max']:g}; see docs/06 gate table; {src})")
    if "confirm_min" in g:
        return (f"PASS (>= {g['confirm_min']:g}; {src})" if value >= g["confirm_min"]
                else f"INTERMEDIATE (< {g['confirm_min']:g}; see docs/06 gate table; {src})")
    if "go_max" in g:
        return f"GO (<= {g['go_max']:g}; {src})" if value <= g["go_max"] else f"INTERMEDIATE ({src})"
    if "max" in g:
        return f"PASS (<= {g['max']:g})" if value <= g["max"] else f"FAIL (> {g['max']:g}; {src})"
    if "min" in g:
        return f"PASS (>= {g['min']:g})" if value >= g["min"] else f"FAIL (< {g['min']:g}; {src})"
    return "no threshold"


def detection_t_half_verdict(g: dict, t_half_min: float) -> str:
    if t_half_min >= g["one_step_min"]:
        return f"ONE-STEP MODE (t1/2 >= {g['one_step_min']} min; {g['source']})"
    if t_half_min >= g["sequential_min"]:
        return f"SEQUENTIAL MODE ({g['sequential_min']}-{g['one_step_min']} min; {g['source']})"
    return f"REJECT PAIR (t1/2 < {g['sequential_min']} min; {g['source']})"
