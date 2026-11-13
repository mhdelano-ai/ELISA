"""PNG views of the lower bay (matplotlib painter via common.render_png, plus 2-D plan/section drawings)."""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Polygon as MPoly  # noqa: E402
from shapely.geometry import Point, box  # noqa: E402

from .. import common as C  # noqa: E402
from .. import interface as I  # noqa: E402
from . import assy  # noqa: E402
from . import geom as G  # noqa: E402
from . import parts as P  # noqa: E402

C._VIEW_DIRS.setdefault("iso_below", (1, -1, -1))   # extra camera (added at run time; common.py unchanged)
C._VIEW_DIRS.setdefault("iso_front_left", (-1, -1, 0.8))


def _cut(items, keep_box):
    kb = P.boxc(*keep_box[0], *keep_box[1])
    out = []
    for n, s, m, k in items:
        bb = s.val().BoundingBox() if hasattr(s, "val") else s.BoundingBox()
        (x0, y0, z0), (x1, y1, z1) = keep_box
        if bb.xmax < x0 or bb.xmin > x1 or bb.ymax < y0 or bb.ymin > y1 or bb.zmax < z0 or bb.zmin > z1:
            continue
        try:
            c = s.intersect(kb)
            if c.val().Volume() > 1e-6:
                out.append((n, c, m, k))
        except Exception:  # noqa: BLE001
            pass
    return out


def _r(items, path, view, title, annotate=None, xlim=None, ylim=None, tol=0.05, size=(10, 7)):
    C.render_png([(s, m) for n, s, m, k in items], path, view=view, title=title, annotate=annotate, xlim=xlim,
                 ylim=ylim, tol=tol, size=size)


def _patch(ax, geom, **kw):
    for g in getattr(geom, "geoms", [geom]):
        ax.add_patch(MPoly(list(g.exterior.coords), closed=True, **kw))
        for h in g.interiors:
            ax.add_patch(MPoly(list(h.coords), closed=True, fc="white", ec=kw.get("ec", "k"), lw=0.3))


def anvil_plan(path):
    """To-scale plan of the anvil top and underside features (card coords)."""
    fig, ax = plt.subplots(figsize=(13, 9.5), dpi=150)
    _patch(ax, box(G.ANVIL_X[0], G.ANVIL_Y[0], G.ANVIL_X[1], G.ANVIL_Y[1]), fc="#c9ccd3", ec="k", lw=0.6)
    _patch(ax, G.pocket_poly(), fc="#9aa3b5", ec="#334", lw=0.5, alpha=0.8)
    for nm, b in (("island boss (DEV-L3)", G.ISLAND_BOSS), ("P_a2 boss", G.P_A2_BOSS), ("P_s boss (DEV-L3)", G.P_S_BOSS)):
        ax.text((b[0] + b[2]) / 2, b[1] - 0.9, nm, fontsize=5, ha="center")
    cc, cp = G.COLD_CUTOUT, G.COLD_PLATE
    _patch(ax, box(cc["x"][0], cc["y"][0], cc["x"][1], cc["y"][1]), fc="#e8d7b0", ec="k", lw=0.4)
    _patch(ax, box(cp["x"][0], cp["y"][0], cp["x"][1], cp["y"][1]), fc="#8fc3ff", ec="k", lw=0.4)
    _patch(ax, G.slot_poly(), fc="white", ec="r", lw=0.5)
    _patch(ax, G.slot_poly_interface(), fc="none", ec="b", lw=0.4, ls="--")
    for c in I.WINDOWS.values():
        _patch(ax, G.window_poly(c), fc="white", ec="r", lw=0.6)
    _patch(ax, G.contact_poly(), fc="white", ec="r", lw=0.6)
    _patch(ax, G.mw_recess_poly(), fc="#f5b7b1", ec="r", lw=0.5)
    for k in G.LIQ_PORTS:
        x, y = I.PORTS[k].xy
        _patch(ax, Point(x, y).buffer(G.PORT_BORE_D / 2), fc="#d9b26f", ec="k", lw=0.4)
        _patch(ax, Point(x, y).buffer(G.TUBE_OD / 2), fc="#555", ec="none")
        ax.text(x, y + 2.0, k, fontsize=5, ha="center")
    for vid, v in I.VALVES.items():
        _patch(ax, Point(v.xy).buffer(v.tip_d / 2), fc="#2e7d32" if v.klass != "slot" else "#f39c12", ec="none")
        ax.text(v.xy[0] + 0.6, v.xy[1] + 0.5, vid, fontsize=4, color="#1b5e20")
    for (x, y) in I.DATUM_A_PINS + [I.DATUM_B_PIN]:
        _patch(ax, Point(x, y).buffer(I.DATUM_PIN_D / 2), fc="#eee", ec="k", lw=0.5)
    for (x, y) in G.GUIDE_BUSH["pins"]:
        _patch(ax, Point(x, y).buffer(G.GUIDE_BUSH["bush_od"] / 2), fc="#c87533", ec="k", lw=0.5)
    for (x, y) in G.GUTTER["drains"]:
        _patch(ax, Point(x, y).buffer(G.GUTTER["drain_d"] / 2), fc="#5dade2", ec="k", lw=0.4)
    for pth in (I.DRAG_PATH["IC1"], I.DRAG_PATH["IC2"], I.BEAD_OUT_PATH):
        ax.plot(*zip(*pth), color="m", lw=0.5)
    e = G.EBAY
    _patch(ax, box(e["x"][0], e["y"][0], e["x"][1], e["y"][1]), fc="none", ec="#7d3c98", lw=0.8, ls=":")
    ax.text(e["x"][1] + 0.5, e["y"][1] + 0.5, "electrode bay (below)", fontsize=5, color="#7d3c98")
    ax.plot([0, I.CARD_L, I.CARD_L, 0, 0], [0, 0, I.CARD_W, I.CARD_W, 0], "k--", lw=0.4)
    ax.text(-11, 63, "grey: anvil (15 mm thick); blue-grey: bottom pocket -> 5-mm plate; white/red: through openings "
                     "(slot red = as built, blue dashed = interface.py); beige: PEEK break; light blue: cold plate;\n"
                     "brown discs: port inserts D3.3 + tube; green: anvil/cold valve tips; orange: slot valves; "
                     "magenta: M_d paths; copper: head guide bushes; light blue dots: gutter drains", fontsize=6,
            va="top")
    ax.set_xlim(G.ANVIL_X[0] - 1, G.ANVIL_X[1] + 1)
    ax.set_ylim(G.ANVIL_Y[0] - 1, G.ANVIL_Y[1] + 1)
    ax.set_aspect("equal")
    ax.set_title("Anvil plan (card coords, mm): top features, pocket, ports, valve tips, slot as built vs interface",
                 fontsize=8)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def render_all(out):
    paths = []
    # 1 nest/anvil from above
    st = assy.state_items("load", card=False)
    nest = [it for it in st if it[0] in ("anvil", "nest_frame", "peek_break_frame", "cold_block", "M_w_magnet")
            or it[0].startswith(("datum_pin", "pusher", "guide_bush", "gasket_", "card_presence"))]
    p = out / "nest_anvil_iso.png"
    _r(nest, p, "iso", "Nest + anvil from above (no card): datum pins A1/A2/B, pushers, lead-in, gutter, windows W1/W2, "
       "drag slot, contact opening, M_w, 11 face seals, cold plate in PEEK break frame", tol=0.05)
    paths.append(p)
    # 2 underside of the anvil
    under = [it for it in st if it[0] in ("anvil", "peek_break_frame", "cold_block", "M_w_magnet")
             or it[0].startswith(("insert_", "ret_"))]
    p = out / "anvil_underside.png"
    _r(under, p, "iso_below", "Anvil from below: 15-mm thick zones, bottom pocket (5-mm plate) with W1/W2, slot, contact "
       "opening; port inserts + retainer plates; cold block (heater footprints: see anvil_plan / STEP)", tol=0.05)
    paths.append(p)
    p = out / "anvil_plan.png"
    anvil_plan(p)
    paths.append(p)
    # 3 magnet bay with the anvil hidden
    for stn in ("gather_IC1", "collect_IC1"):
        st = assy.state_items(stn, card=False)
        hide = ("anvil", "nest_frame", "bay_frame", "foam_insulation", "exhaust_duct", "fan_env", "peek_break_frame",
                "cold_block", "heatsink_env", "peltier_module", "CARD")
        bay = [it for it in st if not it[0].startswith(hide) and not it[0].startswith(("heater_", "datum", "pusher",
                                                                                         "guide_bush", "gasket"))]
        p = out / f"magnet_bay_iso_{stn}.png"
        _r(bay, p, "iso", f"Magnet bay, anvil/frame/cold stack hidden, state '{stn}': M_c1/M_c2 parallelogram units, "
           "M_d post on X-Y stage (envelopes), electrode bay, tubes", tol=0.1)
        paths.append(p)
    # 4 section through W1 with M_c up (plane x = 40, keep x >= 40, look from -x)
    st = assy.state_items("collect_IC1")
    sec = _cut(st, ((40.0, -60, -135), (47.0, 130, 10)))
    p = out / "section_W1_Mc_up.png"
    _r(sec, p, "left", "Section x = 40 through W1/W2 (looking +x): M_c1 UP (flange on the plate underside, gap 0.16), "
       "M_c2 parked (swing R 64.5), card envelope on the anvil", xlim=(-112, 62), ylim=(-85, 12), tol=0.03,
       annotate=[((40, 38, 3), "card"), ((40, 38, -2.6), "M_c1 up"), ((40, 46, -2.5), "5-mm plate"),
                 ((40, 62, -23.5), "links R 64.5"), ((40, -6.7, -48), "M_c2 parked"), ((40, 25, -68), "M_d Z unit (park)"),
                 ((40, 25, -10), "island boss")])
    paths.append(p)
    # 5 section along the WLc/drag slot with M_d at hold (plane y = 25)
    st = assy.state_items("hold_RC")
    sec = _cut(st, ((-50, 25.0, -135), (140, 31.0, 10)))
    p = out / "section_drag_slot_Md_hold.png"
    _r(sec, p, "front", "Section y = 25 along J -> RC (looking +y): M_d holder in the 3.4 slot under the RC (hold), "
       "post D4 on the Z unit, island inserts (left), P_s side (right)", xlim=(20, 75), ylim=(-90, 10), tol=0.03,
       annotate=[((56.8, 25, 3), "card"), ((60, 25, -45), "M_d post D4"), ((56.8, 25, -71), "Z unit"),
                 ((30, 25, -10), "island inserts"), ((70, 25, -40), "Gamry cable")])
    paths.append(p)
    st = assy.state_items("beadout_end")
    sec = _cut(st, ((57.85, -60, -135), (63.0, 130, 10)))
    p = out / "section_beadout_Mw_ebay.png"
    _r(sec, p, "left", "Section x = 57.85 along the bead-out leg (looking +x): M_d at the bead-out stop, M_w in its "
       "recess under BW, electrode bay with pogo block raised (right)", xlim=(-42, -12), ylim=(-62, 8), tol=0.02,
       annotate=[((58, 21.5, -20), "M_d post"), ((58, 17.2, -6.5), "M_w"), ((58, 32.6, -50), "electrode bay"),
                 ((58, 31.5, -12), "pogo block")])
    paths.append(p)
    # 6 section through a port insert and face seal (plane y = 25: P_a, P_b; zoom)
    st = assy.state_items("collect_IC1")
    sec = _cut(st, ((-50, 25.0, -40), (45, 28.0, 10)))
    p = out / "section_port_insert.png"
    _r(sec, p, "front", "Section y = 25 through P_a (x 28) and P_b (x 37.5): PEEK insert D3.3 with bonded 1/16 in tube, "
       "flat gasket in the 0.38 counterbore, retainer plate, card envelope", xlim=(24, 42), ylim=(-22, 4), tol=0.01,
       annotate=[((33, 25, 2), "card (envelope)"), ((28, 25, -8), "insert P_a"), ((37.5, 25, -8), "insert P_b"),
                 ((33, 25, -16.5), "retainer plate"), ((33, 25, -7), "anvil (island boss)"), ((28, 25, -20), "tube")])
    paths.append(p)
    # 7 electrode bay section (plane y = 30.6 through WE1/WE2/CE pins)
    for up in (True, False):
        stn = "hold_RC" if up else "load"
        st = assy.state_items(stn, card=up)
        sec = _cut(st, ((40, 30.6, -70), (100, 36.0, 10)))
        p = out / f"section_ebay_pogo_{'up' if up else 'down'}.png"
        _r(sec, p, "front", f"Section y = 30.6 through WE1/WE2/CE pogo pins (looking +y), block {'UP: tips on the pads '
           '(z 0.34)' if up else 'DOWN: tips at z -1.66 (loading)'}; wedge + cylinder (E), relay, gland, leak electrode",
           xlim=(50, 92), ylim=(-62, 8), tol=0.02,
           annotate=[((58, 30.6, -16), "pogo block"), ((64, 30.6, -26), "wedge"), ((80, 30.6, -26), "cylinder"),
                     ((58, 30.6, -44), "WE relay"), ((80, 30.6, -45), "shielded cable"), ((70, 30.6, -8), "anvil E block")])
        paths.append(p)
    # 8 cold plate / Peltier stack section (plane y = 20)
    st = assy.state_items("collect_IC1")
    sec = _cut(st, ((-50, 20.0, -70), (40, 27.0, 10)))
    p = out / "section_cold_stack.png"
    _r(sec, p, "front", "Section y = 20 through the reagent cold stack (looking +y; revised after review): cold block, break x 20-24 "
       "= 1.5-mm PEEK lip over foam,\n2-mm W gap (lip + foam), TEC 07111 30x30x5.1, heat sink, foam, anvil (right), tubes below", xlim=(-42, 40), ylim=(-66, 8), tol=0.03,
       annotate=[((10, 20, -8), "cold block 4-8 C"), ((22, 20, -8), "foam"), ((22, 20, -0.7), "PEEK lip"), ((5, 20, -22.7), "Peltier"),
                 ((5, 20, -40), "heat sink"), ((-34, 20, -40), "wall W"), ((32, 20, -8), "anvil 25 C"),
                 ((-20, 20, -62), "west tubes")])
    paths.append(p)
    # 9 exploded view
    st = assy.state_items("load", card=True)
    groups = [("CARD", 60), ("nest_frame", 30), ("datum", 30), ("pusher", 30), ("guide_bush", 18), ("gasket", 8),
              ("anvil", 0), ("insert", -22), ("ret_", -30), ("tube_", -45), ("heater", -12),
              ("peek_break", 0), ("cold_block", -15), ("peltier", -30), ("heatsink", -42), ("fan", -42),
              ("exhaust", -42), ("foam", -20), ("ebay", -40), ("pogo", -28), ("WE_relay", -40), ("RH_", -40),
              ("gamry", -40), ("Mc", -30), ("Md_", -60), ("M_w", 10), ("thermistor", -12)]
    ex = []
    for n, s, m, k in st:
        if n.startswith(("bay_frame", "Md_stage", "Md_adapter", "card_presence")):
            continue
        dz = next((d for g, d in groups if n.startswith(g)), 0)
        ex.append((n, s.translate((0, 0, dz)), m, k))
    p = out / "exploded_iso.png"
    _r(ex, p, "iso", "Exploded view (z offsets only): card / nest frame + pins + pushers / gaskets / anvil / inserts, "
       "retainers, tubes / cold stack / electrode bay + pogo / M_c units / M_d post + Z unit", tol=0.1, size=(11, 9))
    paths.append(p)
    return paths
