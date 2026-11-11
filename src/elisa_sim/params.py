"""Parameter loading, unit-checked access, and Monte Carlo sampling.

Three YAML files are read and namespaced:

* ``params/chemistry.yaml``          -> keys ``chem.<section>.<name>``      (Task 1, read-only)
* ``params/hardware.yaml``           -> keys ``hw.<section>.<name>``        (Task 2, read-only)
* ``params/model_assumptions.yaml``  -> keys ``ma.<section>.<name>``        (this task)

Any mapping that has a ``value`` field is a parameter (value, low, high, unit, source, confidence, note).
``model_assumptions.yaml`` may also contain an ``overrides`` section whose entries replace a ``chem.*`` or
``hw.*`` parameter (used where this task questions a Task 1/2 value; the original is kept for reference).

Sampling distribution (stated assumption, see docs/03 section 7):
    a parameter with low == high is fixed;
    if low > 0 and high/low >= ``LOG_RATIO_THRESHOLD`` it is sampled log-triangular(low, value, high)
    (triangular in ln x, mode at the best estimate), otherwise triangular(low, value, high) in x.
Design variables (timings, flows, volumes, reagent concentrations chosen by the designer) are excluded from
sampling via the ``monte_carlo.fixed_patterns`` list in model_assumptions.yaml.
"""
from __future__ import annotations

import copy
import fnmatch
import os
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import yaml

from .units import convert, parse_unit, UnitError

ROOT = Path(__file__).resolve().parents[2]
PARAM_DIR = ROOT / "params"
FILES = {
    "chem": PARAM_DIR / "chemistry.yaml",
    "hw": PARAM_DIR / "hardware.yaml",
    "ma": PARAM_DIR / "model_assumptions.yaml",
}


@dataclass
class Param:
    key: str
    value: float
    low: float
    high: float
    unit: str
    source: str = ""
    confidence: str = ""
    note: str = ""
    origin: str = ""
    overridden_from: "Param | None" = None

    @property
    def is_fixed(self) -> bool:
        return self.low == self.high

    @property
    def unverified(self) -> bool:
        return "UNVERIFIED" in f"{self.source} {self.note}"


def _is_param(d) -> bool:
    return isinstance(d, dict) and "value" in d


def _flatten(prefix: str, d: dict, out: dict, origin: str):
    for k, v in d.items():
        if k == "meta":
            continue
        key = f"{prefix}.{k}"
        if _is_param(v):
            try:
                val = float(v["value"])
                lo = float(v.get("low", val))
                hi = float(v.get("high", val))
            except (TypeError, ValueError) as e:
                raise ValueError(f"non-numeric parameter {key}: {v}") from e
            out[key] = Param(key=key, value=val, low=lo, high=hi, unit=str(v.get("unit", "")),
                             source=str(v.get("source", "")), confidence=str(v.get("confidence", "")),
                             note=str(v.get("note", "")).strip(), origin=origin)
        elif isinstance(v, dict):
            _flatten(key, v, out, origin)
        # strings (names, product labels) are not parameters


def load_raw(files: dict | None = None) -> tuple[dict, dict]:
    """Return (params dict key->Param, extra config dict from model_assumptions)."""
    files = files or FILES
    params: dict[str, Param] = {}
    extra: dict = {}
    for ns in ("chem", "hw", "ma"):
        with open(files[ns], "r") as fh:
            data = yaml.safe_load(fh)
        if ns == "ma":
            extra["monte_carlo"] = data.pop("monte_carlo", {})
            overrides = data.pop("overrides", {}) or {}
            _flatten(ns, data, params, origin=str(files[ns]))
            for okey, entry in overrides.items():
                if okey not in params:
                    raise KeyError(f"override for unknown parameter {okey}")
                tmp = {}
                _flatten("x", {"p": entry}, tmp, origin=str(files[ns]) + " (override)")
                newp = tmp["x.p"]
                newp.key = okey
                newp.overridden_from = params[okey]
                params[okey] = newp
        else:
            _flatten(ns, data, params, origin=str(files[ns]))
    return params, extra


def validate(params: dict[str, Param]) -> list[str]:
    """Return a list of problems (bounds ordering, unparseable units)."""
    problems = []
    for k, p in params.items():
        if not (p.low <= p.value <= p.high):
            problems.append(f"{k}: value {p.value} outside [{p.low}, {p.high}]")
        try:
            parse_unit(p.unit)
        except UnitError as e:
            problems.append(f"{k}: unit {p.unit!r} not parseable ({e})")
    return problems


class ParameterSet:
    """Parameter values (scalars or equal-length arrays) with unit-checked access.

    ``get(key, unit)`` returns the current value converted to ``unit`` and records the access so that the
    Monte Carlo sampler can find which parameters a model actually uses.
    """

    def __init__(self, params: dict[str, Param], extra: dict | None = None, values: dict | None = None,
                 n: int | None = None):
        self.params = params
        self.extra = extra or {}
        self.values = values if values is not None else {k: p.value for k, p in params.items()}
        self.n = n  # None for scalar (nominal) sets
        self.accessed: set[str] = set()
        self.pinned: set[str] = set()   # keys set explicitly (architecture design values): never sampled

    # ---- construction -------------------------------------------------------------------------------
    @classmethod
    def load(cls, files: dict | None = None) -> "ParameterSet":
        params, extra = load_raw(files)
        problems = validate(params)
        bad = [p for p in problems if "outside" in p]
        if bad:
            raise ValueError("parameter bound errors:\n" + "\n".join(bad))
        return cls(params, extra)

    def copy(self) -> "ParameterSet":
        ps = ParameterSet(self.params, self.extra, dict(self.values), self.n)
        ps.pinned = set(self.pinned)
        return ps

    def with_values(self, updates: dict) -> "ParameterSet":
        """New set with some values replaced (values given in the parameter's own YAML unit)."""
        ps = self.copy()
        for k, v in updates.items():
            if k not in self.params:
                raise KeyError(f"unknown parameter {k}")
            ps.values[k] = v
            ps.pinned.add(k)
        return ps

    def with_si(self, updates: dict) -> "ParameterSet":
        """Like with_values but each update is (value, unit) and is converted to the YAML unit."""
        conv = {k: convert(v, u, self.params[k].unit) for k, (v, u) in updates.items()}
        return self.with_values(conv)

    # ---- access -------------------------------------------------------------------------------------
    def get(self, key: str, unit: str):
        if key not in self.params:
            raise KeyError(f"unknown parameter {key}")
        self.accessed.add(key)
        return convert(self.values[key], self.params[key].unit, unit)

    def raw(self, key: str):
        self.accessed.add(key)
        return self.values[key]

    def __contains__(self, key):
        return key in self.params

    # ---- sampling -----------------------------------------------------------------------------------
    def fixed_patterns(self) -> list[str]:
        return list(self.extra.get("monte_carlo", {}).get("fixed_patterns", []))

    def is_design_variable(self, key: str) -> bool:
        return any(fnmatch.fnmatch(key, pat) for pat in self.fixed_patterns())

    def sampleable(self, keys) -> list[str]:
        return sorted(k for k in keys if not self.params[k].is_fixed and not self.is_design_variable(k)
                      and k not in self.pinned)

    def sample(self, n: int, rng: np.random.Generator, keys) -> "ParameterSet":
        """Return a set whose sampleable ``keys`` are arrays of n draws; everything else stays nominal."""
        log_ratio = float(self.extra.get("monte_carlo", {}).get("log_ratio_threshold", 3.0))
        ps = self.copy()
        ps.n = n
        for k in self.sampleable(keys):
            ps.values[k] = sample_param(self.params[k], n, rng, log_ratio)
        return ps


def sample_param(p: Param, n: int, rng: np.random.Generator, log_ratio_threshold: float = 3.0) -> np.ndarray:
    lo, mode, hi = p.low, p.value, p.high
    if lo == hi:
        return np.full(n, mode)
    if lo > 0 and hi / lo >= log_ratio_threshold:
        a, c, b = np.log(lo), np.log(mode), np.log(hi)
        return np.exp(rng.triangular(a, c, b, size=n))
    return rng.triangular(lo, mode, hi, size=n)


def distribution_name(p: Param, log_ratio_threshold: float = 3.0) -> str:
    if p.low == p.high:
        return "fixed"
    if p.low > 0 and p.high / p.low >= log_ratio_threshold:
        return "log-triangular"
    return "triangular"
