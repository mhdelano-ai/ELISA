"""Collect the REAL solids of the four modules in DOCK coordinates (docs/23 §3).

Every item is a dict: module, name, shape (cq.Shape), material, kind. Nothing is redefined here: the card comes from
card.parts.all_parts(), the lower bay from dock_lower.assy.state_items(), the lid from dock_upper.assy.configuration()
and the base from dock_base.build.build_solids()/build_tubes(). Module-internal card envelopes are NOT used.
"""
from __future__ import annotations

from functools import lru_cache

import cadquery as cq

from .. import common as C
from .. import interface as I

ORIGIN = I.CARD_ORIGIN_IN_DOCK


def _sh(o):
    s = C._shape(o)
    return s


def _item(module, name, shape, material, kind="part"):
    return {"module": module, "name": name, "shape": shape, "material": material, "kind": kind}


@lru_cache(maxsize=None)
def card():
    from ..card import parts as Q
    out = []
    for n, w, m in Q.all_parts():
        out.append(_item("CARD", n, _sh(w).translate(cq.Vector(*ORIGIN)), m))
    return tuple(out)


@lru_cache(maxsize=None)
def lower(state):
    from ..dock_lower import assy
    out = []
    card_in = state != "load"          # pushers retracted and pogo tips on the pads only with a card in the nest
    for n, s, m, k in assy.state_items(state, card=card_in):
        if k == "reference":           # LOWER's own card envelope: replaced by the real card
            continue
        out.append(_item("LOWER", n, _sh(s).translate(cq.Vector(*ORIGIN)), m, k))
    return tuple(out)


@lru_cache(maxsize=None)
def upper(config):
    """config: 'closed' (latched, head down), 'raised' (closed, head up), 'open' (85 deg, head up)."""
    from ..dock_upper import assy
    c = assy.configuration(config)
    out = []
    for n, s, m, k in c["rotating"]:
        out.append(_item("UPPER", n, _sh(s), m, k))
    for n, s, m, k in c["fixed"]:
        out.append(_item("UPPER", n, _sh(s), m, "fixed"))
    return tuple(out)


@lru_cache(maxsize=None)
def base(with_tubes=True):
    from ..dock_base import build as B
    from ..dock_base import layout as L
    from ..dock_base import parts as PT
    from ..dock_base import fluidics as F
    sol = B.build_solids()
    out = [_item("BASE", it.name, _sh(sol[it.name]), it.material, it.group) for it in L.ITEMS]
    if with_tubes:
        tubes = B.build_tubes(1.0)
        for r in F.ROUTES:
            if tubes[r.name] is not None:
                out.append(_item("BASE", "tube:" + r.name, _sh(tubes[r.name]), PT.tube_color(r), "tube"))
    return tuple(out)


def scene(lid="closed", lower_state="hold_RC", with_card=True, with_base=True, with_tubes=True):
    items = []
    if with_card:
        items += list(card())
    items += list(lower(lower_state))
    items += list(upper(lid))
    if with_base:
        items += list(base(with_tubes))
    return items


def by_name(items, module, name):
    for it in items:
        if it["module"] == module and it["name"] == name:
            return it
    raise KeyError((module, name))
