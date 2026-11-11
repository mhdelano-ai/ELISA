"""Small, strict unit handling for the parameter files.

Every parameter in the YAML files carries a free-text ``unit`` string (e.g. ``"1/(M*s)"``, ``"uL/min"``,
``"fraction of 100 uL sample injected"``).  The model always asks for a parameter *in a stated target unit*;
:func:`convert` parses both strings into (SI factor, dimension vector), refuses the conversion if the
dimensions differ, and returns the value in the target unit.  Internally the model works in SI
(m, s, mol, kg, A) plus a "count" dimension for numbers of molecules/beads/labels.

Parsing rules (deliberately simple and documented, so that a unit typo in a parameter file fails loudly):

* A unit string whose first word is a dimensionless descriptor (``fraction``, ``fold``, ``boolean``,
  ``percent`` ...) is dimensionless; ``percent`` has factor 0.01.
* Parenthesised groups that contain anything other than unit symbols, numbers and operators are comments
  and are removed (``"uL (at atmospheric pressure, each of two gaps)"`` -> ``uL``).
* ``per`` means ``/``.  Words that are not unit symbols (``ALP``, ``analyte-equivalent`` ...) are ignored;
  count words (``molecules``, ``beads``, ``labels`` ...) carry the count dimension.
* Adjacent factors multiply and bind tighter than ``/`` (``beads per 100 uL`` = count / (100 uL)).
"""
from __future__ import annotations

import re
from functools import lru_cache

import numpy as np

# dimension vector order
DIM_NAMES = ("m", "s", "mol", "kg", "A", "count")
_ZERO = (0, 0, 0, 0, 0, 0)


def _d(m=0, s=0, mol=0, kg=0, A=0, count=0):
    return (m, s, mol, kg, A, count)


_LEN = _d(m=1)
_TIME = _d(s=1)
_AMOUNT = _d(mol=1)
_MASS = _d(kg=1)
_CURRENT = _d(A=1)
_VOLUME = _d(m=3)
_CONC = _d(m=-3, mol=1)
_CHARGE = _d(s=1, A=1)
_VOLT = _d(m=2, kg=1, s=-3, A=-1)
_FARAD = _d(m=-2, kg=-1, s=4, A=2)
_PRESSURE = _d(m=-1, kg=1, s=-2)
_SIEMENS = _d(m=-2, kg=-1, s=3, A=2)
_COUNT = _d(count=1)

# symbol -> (factor to SI, dimension)
UNIT_TABLE: dict[str, tuple[float, tuple]] = {
    # length
    "m": (1.0, _LEN), "cm": (1e-2, _LEN), "mm": (1e-3, _LEN), "um": (1e-6, _LEN), "nm": (1e-9, _LEN),
    # time
    "s": (1.0, _TIME), "min": (60.0, _TIME), "h": (3600.0, _TIME), "Hz": (1.0, _d(s=-1)),
    # amount
    "mol": (1.0, _AMOUNT), "mmol": (1e-3, _AMOUNT), "umol": (1e-6, _AMOUNT), "nmol": (1e-9, _AMOUNT),
    "pmol": (1e-12, _AMOUNT), "fmol": (1e-15, _AMOUNT), "amol": (1e-18, _AMOUNT),
    # concentration (mol/L -> mol/m^3)
    "M": (1e3, _CONC), "mM": (1.0, _CONC), "uM": (1e-3, _CONC), "nM": (1e-6, _CONC),
    "pM": (1e-9, _CONC), "fM": (1e-12, _CONC),
    # volume
    "L": (1e-3, _VOLUME), "mL": (1e-6, _VOLUME), "uL": (1e-9, _VOLUME), "nL": (1e-12, _VOLUME),
    # mass
    "kg": (1.0, _MASS), "g": (1e-3, _MASS), "mg": (1e-6, _MASS), "ug": (1e-9, _MASS),
    "ng": (1e-12, _MASS), "pg": (1e-15, _MASS), "fg": (1e-18, _MASS), "kDa": (1e3 / 6.02214076e23 * 1e-3, _MASS),
    # electrical
    "A": (1.0, _CURRENT), "mA": (1e-3, _CURRENT), "uA": (1e-6, _CURRENT), "nA": (1e-9, _CURRENT),
    "pA": (1e-12, _CURRENT), "fA": (1e-15, _CURRENT), "aA": (1e-18, _CURRENT),
    "C": (1.0, _CHARGE), "nC": (1e-9, _CHARGE), "pC": (1e-12, _CHARGE),
    "V": (1.0, _VOLT), "mV": (1e-3, _VOLT), "uV": (1e-6, _VOLT),
    "F": (1.0, _FARAD), "uF": (1e-6, _FARAD),
    "S": (1.0, _SIEMENS),
    # pressure
    "Pa": (1.0, _PRESSURE), "kPa": (1e3, _PRESSURE), "MPa": (1e6, _PRESSURE), "bar": (1e5, _PRESSURE),
    "psi": (6894.757293168, _PRESSURE),
    # temperature (absolute only)
    "K": (1.0, _ZERO),
}

COUNT_WORDS = {"molecules", "molecule", "beads", "bead", "labels", "label", "atoms", "enzymes", "enzyme",
               "HRP", "copies", "sites", "conjugate", "conjugates"}

DIMENSIONLESS_PREFIXES = {
    "fraction": 1.0, "fold": 1.0, "boolean": 1.0, "count": 1.0, "relative": 1.0, "dimensionless": 1.0,
    "ph": 1.0, "cycles": 1.0, "mol/mol": 1.0, "e-/molecule": 1.0, "percent": 0.01, "loop": 1.0,
    "vials": 1.0, "1": 1.0, "ratio": 1.0, "mol/mol,": 1.0, "number": 1.0, "tanks": 1.0,
    "bed": 1.0, "capture-regeneration": 1.0, "fractional": 1.0,
}

_TOKEN_RE = re.compile(r"\s*(?:(\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)|([A-Za-z][A-Za-z0-9_\-]*)|(\^)|(\*)|(/)|(\()|(\))|(,)|(\S))")


class UnitError(ValueError):
    pass


def _strip_comment_groups(s: str) -> str:
    """Remove innermost parenthesised groups that contain non-unit words (comments)."""
    pattern = re.compile(r"\(([^()]*)\)")
    changed = True
    while changed:
        changed = False
        for m in pattern.finditer(s):
            inner = m.group(1)
            ok = True
            for tok in _TOKEN_RE.findall(inner):
                num, ident, *_rest = tok
                other = tok[7] or tok[8]
                if other:  # comma or stray symbol
                    ok = False
                    break
                if ident and ident not in UNIT_TABLE and ident not in COUNT_WORDS and ident != "per":
                    ok = False
                    break
            if not ok:
                s = s[: m.start()] + " " + s[m.end():]
                changed = True
                break
    return s


def _tokenize(s: str):
    out = []
    for num, ident, caret, star, slash, lp, rp, comma, other in _TOKEN_RE.findall(s):
        if num:
            out.append(("num", float(num)))
        elif ident:
            if ident == "per":
                out.append(("op", "/"))
            elif ident in UNIT_TABLE:
                out.append(("unit", ident))
            elif ident in COUNT_WORDS:
                out.append(("count", ident))
            # other words are descriptive and ignored
        elif caret:
            out.append(("op", "^"))
        elif star:
            out.append(("op", "*"))
        elif slash:
            out.append(("op", "/"))
        elif lp:
            out.append(("lp", "("))
        elif rp:
            out.append(("rp", ")"))
        elif other == "-":
            out.append(("op", "-"))
        # commas / other symbols are ignored outside comment groups
    return out


def _mul(a, b):
    return (a[0] * b[0], tuple(x + y for x, y in zip(a[1], b[1])))


def _div(a, b):
    return (a[0] / b[0], tuple(x - y for x, y in zip(a[1], b[1])))


def _pow(a, p):
    return (a[0] ** p, tuple(x * p for x in a[1]))


class _Parser:
    def __init__(self, tokens):
        self.t = tokens
        self.i = 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def take(self):
        tok = self.peek()
        self.i += 1
        return tok

    def parse_expr(self):
        val = self.parse_group()
        while True:
            kind, v = self.peek()
            if kind == "op" and v in ("*", "/"):
                self.take()
                rhs = self.parse_group()
                val = _mul(val, rhs) if v == "*" else _div(val, rhs)
            else:
                return val

    def parse_group(self):
        """Adjacent (implicitly multiplied) powered factors; empty group = 1."""
        val = (1.0, _ZERO)
        seen_count = False
        while True:
            kind, v = self.peek()
            if kind in ("num", "unit", "lp", "count"):
                f = self.parse_powered()
                if kind == "count":
                    if seen_count:
                        continue  # "enzyme labels" counts once
                    seen_count = True
                val = _mul(val, f)
            else:
                return val

    def parse_powered(self):
        base = self.parse_factor()
        kind, v = self.peek()
        if kind == "op" and v == "^":
            self.take()
            sign = 1.0
            k2, v2 = self.peek()
            if k2 == "op" and v2 == "-":
                self.take()
                sign = -1.0
            kind3, num = self.take()
            if kind3 != "num":
                raise UnitError("exponent expected")
            return _pow(base, sign * num)
        return base

    def parse_factor(self):
        kind, v = self.take()
        if kind == "num":
            return (v, _ZERO)
        if kind == "unit":
            return UNIT_TABLE[v]
        if kind == "count":
            return (1.0, _COUNT)
        if kind == "lp":
            val = self.parse_expr()
            k2, _ = self.take()
            if k2 != "rp":
                raise UnitError("unbalanced parenthesis")
            return val
        raise UnitError(f"unexpected token {v!r}")


@lru_cache(maxsize=None)
def parse_unit(unit: str) -> tuple[float, tuple]:
    """Return (factor to SI, dimension tuple) for a unit string."""
    if unit is None:
        raise UnitError("missing unit")
    s = str(unit).strip()
    if s == "":
        return (1.0, _ZERO)
    first = s.split()[0].lower().rstrip(",")
    if first in DIMENSIONLESS_PREFIXES:
        return (DIMENSIONLESS_PREFIXES[first], _ZERO)
    if s in ("degC",):
        raise UnitError("affine temperature unit degC is not convertible; use K")
    s2 = _strip_comment_groups(s)
    tokens = _tokenize(s2)
    if not tokens:
        raise UnitError(f"no unit symbols found in {unit!r}")
    p = _Parser(tokens)
    val = p.parse_expr()
    if p.i != len(tokens):
        raise UnitError(f"could not parse unit {unit!r}")
    return val


def dimension_string(dim: tuple) -> str:
    parts = [f"{n}^{e:g}" for n, e in zip(DIM_NAMES, dim) if e != 0]
    return " ".join(parts) if parts else "dimensionless"


def convert(value, from_unit: str, to_unit: str):
    """Convert ``value`` (scalar or array) from ``from_unit`` to ``to_unit``; raise on dimension mismatch."""
    f1, d1 = parse_unit(from_unit)
    f2, d2 = parse_unit(to_unit)
    if any(abs(a - b) > 1e-12 for a, b in zip(d1, d2)):
        raise UnitError(
            f"dimension mismatch: {from_unit!r} [{dimension_string(d1)}] -> {to_unit!r} [{dimension_string(d2)}]")
    return np.asarray(value, dtype=float) * (f1 / f2) if isinstance(value, np.ndarray) else value * (f1 / f2)


def same_dimension(u1: str, u2: str) -> bool:
    return parse_unit(u1)[1] == parse_unit(u2)[1]
