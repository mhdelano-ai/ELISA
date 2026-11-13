"""Lower-bay assembly per machine state (geom.STATES). Items: (name, solid, material, kind); kind in
custom | catalogue | envelope | reference (the card envelope)."""
from __future__ import annotations

from functools import lru_cache

from .. import interface as I
from . import geom as G
from . import parts as P


@lru_cache(maxsize=None)
def static_items():
    """Parts that do not move between states (cached)."""
    it = [("anvil", P.anvil(), "anodised", "custom"), ("nest_frame", P.nest_frame(), "anodised", "custom"),
          ("peek_break_frame", P.peek_break_frame(), "PEEK", "custom"), ("cold_block", P.cold_block(), "cold", "custom"),
          ("peltier_module", P.peltier(), "envelope", "catalogue"), ("heatsink_env", P.heatsink(), "aluminium", "envelope"),
          ("fan_env", P.fan(), "envelope", "envelope"), ("exhaust_duct", P.duct(), "PEEK", "custom"),
          ("foam_insulation", P.foam_shell(), "envelope", "custom"), ("M_w_magnet", P.m_w_magnet(), "NdFeB", "catalogue"),
          ("bay_frame", P.bay_frame(), "aluminium", "custom"), ("ebay_enclosure", P.ebay_enclosure(), "aluminium", "custom"),
          ("gamry_cable", P.gamry_cable(), "copper", "catalogue"),
          ("card_presence_env", P.card_presence_sensor(), "envelope", "envelope")]
    it += P.latch_brackets() + P.hinge_pedestals()     # revised at integration (docs/23)
    for k, s in P.anvil_heaters():
        it.append((f"heater_{k}", s, "heater", "envelope"))
    for k, s in P.datum_pins():
        it.append((k, s, "PTFE", "catalogue"))
    for k, s in P.guide_bushes():
        it.append((k, s, "copper", "custom"))
    for k in G.LIQ_PORTS:
        it.append((f"insert_{k}", P.port_insert(k), "PEEK", "custom"))
        it.append((f"gasket_{k}", P.gasket(k), "elastomer", "custom"))
        it.append((f"tube_{k}", P.tube_solid(k), "TPE", "catalogue"))   # PEEK tube, drawn orange
    for k in G.RETAINERS:
        it.append((k, P.retainer(k), "aluminium", "custom"))
    for k, s, m, kind in P.ebay_internals():
        it.append((k, s, m, kind))
    for k, s, m in P.thermistors():
        it.append((f"thermistor_{k}", s, m, "catalogue"))
    return tuple(it)


def state_items(state, card=True):
    th1, th2, mdxy, mdup, pogo_up = G.STATES[state]
    it = list(static_items())
    it += P.mc_unit(1, th1) + P.mc_unit(2, th2)
    it += P.md_moving(mdxy, mdup) + P.md_carriage(mdxy) + P.md_stages(mdxy)
    it.append(("pogo_block", P.pogo_block(pogo_up), "PEEK", "custom"))
    it.append(("pogo_probes", P.pogo_probes(pogo_up, card), "gold", "catalogue"))
    it += [(n, s, m, k) for n, s, m, k in P.pogo_guide_and_wedge(pogo_up)]
    it += [(n, s, "PEEK", "catalogue") for n, s in P.pushers(card)]
    if card:
        it.append(("CARD_envelope_ref", P.card_envelope(), "COC", "reference"))
    return it
