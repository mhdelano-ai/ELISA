#!/usr/bin/env python3
"""Build the slide files of the tier-round summary deck.

Reads the slide templates (gen/templates/<id>.html), the drawings (gen/art/<name>.svg with <name>.labels.json),
the model output of the round (results/tier_round/tiers.json) and gen/chart_extra.json (made by chart_extra.py),
replaces every {{...}} placeholder of a template and writes slides/<id>.html, one file per slide of deck.json.

    {{art:NAME}}      a drawing with its labels pinned over it
    {{chart:NAME}}    a chart built here from the model output
    {{n:KEY}}         one number of the model output, rounded as in docs/30 (two significant figures)

No number of a chart is typed by hand.  The slide format is the one of the earlier decks (see ../../README.md):
one <section> per file, the notes in an <aside> at its end, shared rules in ../deck.css.

Usage:  python docs/presentation/source_tiers/gen/make_slides.py     (then: python docs/presentation/build.py)
"""
import html
import json
import math
import os
import pathlib
import re
import sys
from html.parser import HTMLParser

HERE = pathlib.Path(__file__).resolve().parent
DECK = HERE.parent
TEMPL, ART, OUT = HERE / "templates", HERE / "art", DECK / "slides"


def find_repo():
    env = os.environ.get("ELISA_REPO")
    for c in ([pathlib.Path(env)] if env else []) + list(HERE.parents):
        if (c / "results" / "tier_round" / "tiers.json").exists():
            return c
    raise SystemExit("results/tier_round/tiers.json not found; set ELISA_REPO to the repository root")


REPO = find_repo()
TIERS = json.loads((REPO / "results" / "tier_round" / "tiers.json").read_text(encoding="utf-8"))
EXTRA = json.loads((HERE / "chart_extra.json").read_text(encoding="utf-8"))

# ---------------------------------------------------------------- the model output, by short keys
LABEL = {
    "t1": "Tier 1: capture on a printed gold strip, read at the electrode under fast substrate flow",
    "t2": "Tier 2: capillary micro-bed above a printed carbon strip, stop and sweep",
    "t3": "Tier 3: the capture bed in the loop of one valve",
    "t3t": "Tier 3 with the immune-complex transfer to a second bed",
}
BASE = TIERS["1. The three implementations, as specified"]
D = {k: BASE[v] for k, v in LABEL.items()}
SCEN = {k: TIERS["2. Scenarios - " + v] for k, v in LABEL.items()}
SCENARIO = {
    "spec": "as specified",
    "L67": "detection reagent and substrate lot pass screening (L6 + L7)",
    "L367": "L3 + L6 + L7",
    "S1": "non-specific binding x25 (S1)",
    "ND": "no decay in the reservoir: background 1e-5 of the substrate at the time of use",
    "S4": "background 1e-3 of the substrate, no decay (S4a)",
    "P01": "only 1 % of the turnovers give an electroactive product (review C1)",
    "P001": "only 0.1 % of the turnovers give an electroactive product",
}
ALT = {   # named cases of the alternatives tables: key -> (section, label)
    "t1.carbon": ("3. Tier 1 - alternatives and hardware cases",
                  "printed carbon C21 with adsorbed streptavidin (same cell and read)"),
    "t1.gap010": ("3. Tier 1 - alternatives and hardware cases", "strip-cell gap 0.10 mm"),
    "t1.gap050": ("3. Tier 1 - alternatives and hardware cases", "strip-cell gap 0.50 mm"),
    "t2.nowall": ("4. Tier 2 - alternatives and hardware cases",
                  "no conjugate-exposed wall upstream of the bed (bound)"),
    "t2.frit1": ("4. Tier 2 - alternatives and hardware cases", "retainer wetted area 1 mm2 instead of 5 mm2"),
    "t2.frit20": ("4. Tier 2 - alternatives and hardware cases",
                  "retainer wetted area 20 mm2 (0.5 mm silicate frit)"),
    "t2.nostop": ("4. Tier 2 - alternatives and hardware cases", "pump cannot stop: continuous read at 1 uL/min"),
    "t3.loop30": ("5. Tier 3 - alternatives", "one valve, loop walls 30 mm2 instead of 10 mm2"),
    "t3t.rel07": ("5. Tier 3 - alternatives",
                  "transfer: release 0.7 in 5 min, as docs/05 assumed for its tube protocol"),
    "t3t.rel07s": ("5. Tier 3 - alternatives", "transfer, release 0.7, screened reagents (L6 + L7)"),
    "t3t.pess": ("5. Tier 3 - alternatives", "transfer: release 0.05, non-specific x0.5 (pessimistic bounds)"),
    "t3t.opt": ("5. Tier 3 - alternatives", "transfer: release 0.74, non-specific x0.01 (optimistic bounds)"),
}


def f2(x):
    """Two significant figures, plain decimal, as scripts/tier_round/doc_tables.py prints them."""
    v = float(f"{float(x):.2g}")
    if v >= 10:
        return f"{v:.0f}"
    if v >= 1:
        return f"{v:.1f}"
    if v >= 0.1:
        return f"{v:.2f}"
    return f"{v:.2g}"


def case_values(prefix, c, into):
    into[prefix + ".nom"] = f2(c["lod_nominal"])
    into[prefix + ".med"] = f2(c["lod_median"])
    into[prefix + ".p05"] = f2(c["lod_p05"])
    into[prefix + ".p95"] = f2(c["lod_p95"])
    into[prefix + ".p1"] = f"{c['p_lod_le_target']:.2f}"
    into[prefix + ".p10"] = f"{c['p_lod_le_10']:.2f}"


VALUES = {}
for _k, _d in D.items():
    case_values(_k, _d, VALUES)
    VALUES[_k + ".min"] = f"{_d['time_to_result_min']:.1f}"
    VALUES[_k + ".cap"] = f2(100 * _d["diagnostics"]["capture_fraction"])
    VALUES[_k + ".blank"] = f2(_d["blank_equiv_nominal"])
    VALUES[_k + ".nsbvar"] = f"{100 * _d['variance_fractions_nominal']['nsb_variability']:.0f}"
    for _s, _lab in SCENARIO.items():
        case_values(f"{_k}.{_s}", SCEN[_k][_lab], VALUES)
for _key, (_sec, _lab) in ALT.items():
    case_values(_key, TIERS[_sec][_lab], VALUES)

# ---------------------------------------------------------------- colours of the deck
INK, CREAM, CARD, SAND, BORDER = "#14213D", "#F6F3EC", "#FFFDF8", "#ECE7DB", "#D9D2C2"
STEEL, SLATE, BLUE, MIDBLUE, PALEBLUE = "#9AA5B8", "#5E6B85", "#1F5A96", "#B9CCE3", "#E3EBF5"
ORANGE, RUST, TEAL, SOFT, GRID = "#D9773F", "#A8481A", "#2A9D8F", "#4A5568", "#E4DFD3"
REV = ["#7C9FCB", "#4877AF", "#173F6E"]          # first version, Revision B, Revision C


def esc(s):
    return html.escape(str(s), quote=False)


def pin(cls, x, y, w, text, align="left", extra=""):
    """A line of words pinned in its host: left, top and width in px."""
    st = f"left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px"
    if align != "left":
        st += f";text-align:{align}"
    if extra:
        st += ";" + extra
    return f'<p class="{cls}" style="{st}">{text}</p>'


def svg_open(w, h, label):
    return (f'<svg style="position:absolute;left:0;top:0" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'aria-label="{html.escape(label, quote=True)}">')


def smooth(pts):
    """A smooth path through the points (Catmull-Rom segments written as cubic Beziers)."""
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d


# ---------------------------------------------------------------- drawings
def art(name, plate=False, dx=0, dy=0, w=None, h=None):
    """A drawing of gen/art with its labels: a host of fixed size, the svg first, the words pinned over it."""
    svg = (ART / f"{name}.svg").read_text(encoding="utf-8").strip()
    m = re.match(r"<svg\b[^>]*>", svg)
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', m.group(0))
    W, H = int(float(vb.group(1))), int(float(vb.group(2)))
    aria = re.search(r'aria-label="([^"]*)"', m.group(0))
    root = (f'<svg style="position:absolute;left:{dx}px;top:{dy}px" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" aria-label="{aria.group(1) if aria else name}">')
    body = svg[m.end():]
    assert not re.search(r"<(text|style|script|foreignObject|image)\b|<!--|https?://(?!www\.w3\.org)", body), name
    ps = []
    for lab in json.loads((ART / f"{name}.labels.json").read_text(encoding="utf-8")):
        cls = "lab strong" if lab.get("weight", 400) >= 600 else "lab"
        extra = f"font-size:{lab['size']}px" if lab.get("size", 24) != 24 else ""
        ps.append(pin(cls, lab["x"] + dx, lab["y"] + dy, lab["w"], esc(lab["text"]), lab.get("align", "left"), extra))
    cls = "host plate" if plate else "host"
    pad = 4 if plate else 0                       # the plate's border lies inside its box
    return (f'<div class="{cls}" style="width:{(w or W + 2 * dx) + pad}px;height:{(h or H + 2 * dy) + pad}px">'
            f'\n{root}{body}\n'
            + "\n".join(ps) + "\n</div>")


def pict(kind):
    """Three small pictures for the tier cards: where the IgG is captured."""
    o = f'stroke="{INK}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"'
    ab = lambda x, y: (f'<path d="M{x} {y}v-14M{x} {y - 14}l-9 -11M{x} {y - 14}l9 -11" fill="none" '
                       f'stroke="{SLATE}" stroke-width="4" stroke-linecap="round"/>')
    beads = lambda x0, y0, nx, ny, r=6: "".join(
        f'<circle cx="{x0 + i * 2 * r + (r if j % 2 else 0)}" cy="{y0 + j * (2 * r - 2)}" r="{r}" fill="#8A5A3C" '
        f'stroke="{INK}" stroke-width="1.5"/>' for j in range(ny) for i in range(nx))
    if kind == "t1":
        label = "A printed strip; antibodies stand on its gold working electrode."
        body = (f'<rect x="20" y="78" width="280" height="44" rx="8" fill="{SAND}" {o}/>'
                f'<rect x="92" y="70" width="136" height="12" rx="3" fill="#C9A227" {o}/>'
                + "".join(ab(x, 68) for x in (110, 135, 160, 185, 210))
                + f'<path d="M160 8v26M160 34l-8 -10M160 34l8 -10" fill="none" stroke="{BLUE}" stroke-width="4" '
                  f'stroke-linecap="round" stroke-linejoin="round"/>')
    elif kind == "t2":
        label = "A capillary with a packed bed of beads ends just above the electrode of a printed strip."
        body = (f'<rect x="20" y="96" width="280" height="30" rx="8" fill="{SAND}" {o}/>'
                f'<rect x="92" y="88" width="136" height="12" rx="3" fill="#2B2F3A" {o}/>'
                f'<rect x="138" y="4" width="44" height="72" rx="4" fill="{PALEBLUE}" {o}/>'
                + beads(146, 34, 3, 3)
                + f'<rect x="141" y="62" width="38" height="8" fill="{SLATE}" stroke="{INK}" stroke-width="1.5"/>'
                  f'<path d="M160 76v8" fill="none" stroke="{BLUE}" stroke-width="4" stroke-linecap="round"/>')
    else:
        label = "A six-port valve with the bed of beads in its loop; its outlet leads to the electrode of a strip."
        ports = "".join(
            f'<circle cx="{92 + 40 * math.cos(math.radians(a)):.1f}" cy="{64 - 40 * math.sin(math.radians(a)):.1f}" '
            f'r="7" fill="{CARD}" {o}/>' for a in (0, 60, 120, 180, 240, 300))
        line = f'fill="none" stroke="{BLUE}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"'
        body = (f'<rect x="200" y="112" width="112" height="28" rx="8" fill="{SAND}" {o}/>'
                f'<rect x="226" y="104" width="60" height="12" rx="3" fill="#2B2F3A" {o}/>'
                f'<path d="M6 12H72V30M112 30V12H256V86" {line}/>'
                f'<path d="M248 82L256 98L264 82Z" fill="{BLUE}" stroke="{BLUE}" stroke-width="2" '
                f'stroke-linejoin="round"/>'
                f'<path d="M52 64H22V136H162V64H132" {line}/>'
                f'<circle cx="92" cy="64" r="52" fill="{CARD}" {o}/>' + ports
                + f'<rect x="50" y="124" width="84" height="24" rx="4" fill="{PALEBLUE}" {o}/>'
                + beads(60, 131, 5, 2, 5)
                + f'<rect x="116" y="127" width="8" height="18" fill="{SLATE}" stroke="{INK}" stroke-width="1.5"/>')
    return (f'<svg width="320" height="152" viewBox="0 0 320 152" aria-label="{label}" style="display:block">'
            f"{body}</svg>")


# ---------------------------------------------------------------- charts
def chart_conv():
    """Share of the product that the electrode collects, against flow (docs/30 section 1, fact 5)."""
    pts = EXTRA["conversion_vs_flow"]
    W, H = 900, 476
    x0, x1, yt, yb = 120, 850, 100, 372
    lx = lambda q: x0 + math.log10(q) / math.log10(200) * (x1 - x0)
    ly = lambda f: yb - f * (yb - yt)
    at = {q: f for q, f in pts}
    s = [svg_open(W, H, "Line chart. Product made on the electrode is collected in full at every flow. Product "
                        "that arrives with the stream is collected less and less as the flow rises: "
                        f"{100 * at[1]:.0f} % at 1, {100 * at[5]:.0f} % at 5 and {f2(100 * at[200])} % at "
                        "200 microlitres per minute.")]
    for f in (0, 0.25, 0.5, 0.75, 1):
        s.append(f'<path d="M{x0} {ly(f):.1f}H{x1}" stroke="{GRID}" stroke-width="2"/>')
    for q in (1, 2, 5, 10, 20, 50, 100, 200):
        s.append(f'<path d="M{lx(q):.1f} {yb}v8" stroke="{STEEL}" stroke-width="2"/>')
    s.append(f'<path d="M{x0} {yb}H{x1}" stroke="{STEEL}" stroke-width="2"/>')
    s.append(f'<path d="M{x0} {ly(1):.1f}H{x1}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    s.append(f'<path d="{smooth([(lx(q), ly(f)) for q, f in pts])}" fill="none" stroke="{BLUE}" stroke-width="4" '
             f'stroke-linecap="round" stroke-linejoin="round"/>')
    s.append(f'<path d="M{lx(200):.1f} 282V{ly(at[200]) - 16:.1f}" stroke="{SLATE}" stroke-width="2"/>')
    for q in (5, 200):
        s.append(f'<circle cx="{lx(q):.1f}" cy="{ly(at[q]):.1f}" r="10" fill="{BLUE}" stroke="{CARD}" '
                 f'stroke-width="3"/>')
    s.append("</svg>")
    out = ["".join(s)]
    out.append(pin("lab strong", 28, 16, 840, "Share of the product that the 3 mm electrode collects"))
    out.append(pin("lab", 250, 62, 600, "made on the electrode itself: all of it, at any flow", "right"))
    for f in (0, 0.25, 0.5, 0.75, 1):
        out.append(pin("tick", 20, ly(f) - 15, 88, f"{100 * f:.0f}" + (" %" if f == 1 else ""), "right"))
    for q in (1, 2, 5, 10, 20, 50, 100, 200):
        out.append(pin("tick", lx(q) - 40, yb + 12, 80, str(q), "center"))
    out.append(pin("tick", x0, yb + 50, x1 - x0, "flow through the cell, µL/min (log scale)", "center"))
    out.append(pin("lab", lx(5) + 22, ly(at[5]) - 72, 484,
                   f"arriving with the stream: <b>{100 * at[5]:.0f} %</b> at 5 µL/min, the sweep of tiers 2 and 3"))
    out.append(pin("lab", 510, 214, 340, f"<b>{f2(100 * at[200])} %</b> at 200 µL/min, the read of tier 1", "right"))
    return f'<div class="host plate" style="width:{W + 4}px;height:{H + 4}px">\n' + "\n".join(out) + "\n</div>"


HEADS = [("Tier 1", "on the electrode"), ("Tier 2", "bed at the inlet"), ("Tier 3", "one valve"),
         ("Tier 3", "with transfer")]
TIER_NAMES = [("t1", "Tier 1", "capture on the electrode"), ("t2", "Tier 2", "bead bed at the cell inlet"),
              ("t3", "Tier 3, one valve", "the bed in a valve loop"),
              ("t3t", "Tier 3 with transfer", "second bed, conditional")]


def chart_lod():
    """Predicted detection limits: nominal, median and 5-95 % range on a log axis (docs/30 section 0)."""
    PW, ROW, AX = 872, 84, 56
    lx = lambda v: 20 + (math.log10(v) + 1) * 200
    s = [svg_open(PW, 4 * ROW + AX,
                  "Range chart on a logarithmic axis from 0.1 to 1000 pg/mL. " + " ".join(
                      f"{n}: nominal {VALUES[k + '.nom']}, median {VALUES[k + '.med']}, 5 to 95 % of the draws "
                      f"{VALUES[k + '.p05']} to {VALUES[k + '.p95']}." for k, n, _ in TIER_NAMES)
                  + " The target is 1 pg/mL.")]
    for i in range(1, 4):
        s.append(f'<path d="M0 {i * ROW}H{PW}" stroke="{GRID}" stroke-width="2"/>')
    for v in (0.1, 10, 100, 1000):
        s.append(f'<path d="M{lx(v):.0f} 0V{4 * ROW}" stroke="{GRID}" stroke-width="2"/>')
    s.append(f'<path d="M0 {4 * ROW}H{PW}" stroke="{STEEL}" stroke-width="2"/>')
    s.append(f'<path d="M{lx(1):.0f} 0V{4 * ROW + 8}" stroke="{RUST}" stroke-width="4"/>')
    labels = [pin("lab strong", lx(1) - 212, 4, 200, "target: 1 pg/mL", "right", f"color:{RUST}")]
    for i, (k, _, _) in enumerate(TIER_NAMES):
        d, y = D[k], i * ROW + 56
        a, b, m, n = lx(d["lod_p05"]), lx(d["lod_p95"]), lx(d["lod_median"]), lx(d["lod_nominal"])
        s.append(f'<rect x="{a:.1f}" y="{y - 12}" width="{b - a:.1f}" height="24" rx="6" fill="{MIDBLUE}"/>')
        s.append(f'<rect x="{m - 3:.1f}" y="{y - 22}" width="6" height="44" rx="2" fill="{INK}"/>')
        s.append(f'<circle cx="{n:.1f}" cy="{y}" r="12" fill="{BLUE}" stroke="{CREAM}" stroke-width="3"/>')
        if abs(n - lx(1)) < 44:                 # keep the number clear of the target line
            labels.append(pin("lab strong", lx(1) + 10, y - 50, 100, VALUES[k + ".nom"]))
        else:
            labels.append(pin("lab strong", n - 50, y - 50, 100, VALUES[k + ".nom"], "center"))
    for v, t in ((0.1, "0.1"), (1, "1"), (10, "10"), (100, "100"), (1000, "1000")):
        labels.append(pin("tick", lx(v) - 50, 4 * ROW + 14, 100, t, "center"))
    s.append("</svg>")
    plot = (f'<div class="host" style="width:{PW}px;height:{4 * ROW + AX}px">\n' + "".join(s) + "\n"
            + "\n".join(labels) + "\n</div>")

    def column(width, head, cells, align="left"):
        st = f"width:{width}px;gap:0" + (";text-align:" + align if align != "left" else "")
        rows = "".join(f'<div class="col fix" style="height:{ROW}px;gap:2px;justify-content:center">{c}</div>'
                       for c in cells)
        return (f'<div class="col fix" style="{st}"><p class="small strong" style="height:48px">{head}</p>'
                f"{rows}</div>")

    names = column(290, "", [f'<p class="strong">{n}</p><p class="small soft">{sub}</p>' for _, n, sub in TIER_NAMES])
    med = column(230, "Median [5–95 %]", [
        f'<p class="small">{VALUES[k + ".med"]} [{VALUES[k + ".p05"]}–{VALUES[k + ".p95"]}]</p>'
        for k, _, _ in TIER_NAMES])
    prob = column(200, "P(≤ 1 pg/mL)", [f'<p class="strong">{VALUES[k + ".p1"]}</p>' for k, _, _ in TIER_NAMES])
    mid = (f'<div class="col fix" style="width:{PW}px;gap:0"><p class="small strong" style="height:48px">'
           f"Model prediction of the detection limit, pg/mL (log scale)</p>{plot}</div>")
    return f'<div class="row" style="gap:24px">\n{names}\n{mid}\n{med}\n{prob}\n</div>'


def chart_timeline():
    """One row per design, 22 px per minute, from the step tables of the model output."""
    PX, LABW = 20, 300
    plans = {   # (category, number of steps of the model's table it covers, words in the bar)
        "t1": [("sample", 2, "Sample over the electrode: 44 min at 2.86 µL/min"), ("wash", 1, ""), ("conj", 2, ""),
               ("wash2ref", 1, ""), ("sub", 1, ""), ("read", 1, ""), ("wash", 1, ""), ("read", 1, "")],
        "t2": [("sample", 2, "Sample through the bead bed: 37 min at 3.4 µL/min"), ("wash", 1, ""), ("conj", 2, ""),
               ("wash", 1, ""), ("sub", 2, ""), ("wait", 1, "Stop"), ("read", 1, "")],
        "t3": [("sample", 2, "Sample through the bed: 40 min at 3.15 µL/min"), ("wash", 1, ""),
               ("conj", 2, ""), ("wash", 1, ""), ("sub", 1, ""), ("wait", 1, ""), ("read", 1, "")],
        "t3t": [("sample", 2, "Sample: 25 min at 5 µL/min"), ("wash", 1, ""), ("conj", 2, ""), ("wash", 1, ""),
                ("move", 1, "To bed 2"), ("sub", 1, ""), ("wait", 1, "Closed"), ("read", 1, "")],
    }
    css = {"sample": "c-blue", "wash": "c-steel", "conj": "c-orange", "sub": "c-slate", "wait": "c-teal",
           "read": "c-rust", "move": "c-ink"}
    rows = []
    ticks = "".join(
        f'<p class="small soft fix" style="width:{10 * PX}px;border-left:3px solid {STEEL};padding-left:8px;'
        f'box-sizing:border-box">{t}</p>' for t in ("0 min", "10", "20", "30", "40", "50"))
    rows.append(f'<div class="row" style="gap:0"><div class="fix" style="width:{LABW}px"></div>{ticks}'
                f'<p class="small strong fix" style="width:120px;padding-left:11px;box-sizing:border-box;'
                f'color:{RUST}">60 min</p></div>')
    for k, name, _ in TIER_NAMES:
        steps = [st for st in D[k]["steps"] if st[2]]
        assert abs(sum(st[1] for st in steps) - D[k]["time_to_result_min"]) < 1e-6, k
        segs, i, t = [], 0, 0.0
        for cat, n, words in plans[k]:
            dur = sum(st[1] for st in steps[i:i + n])
            i += n
            parts = [("wash", dur - 0.5), ("read", 0.5)] if cat == "wash2ref" else [(cat, dur)]
            for c, dd in parts:
                a, b = round(t * PX), round((t + dd) * PX)
                t += dd
                w = b - a - 2
                assert len(words) * 14.5 + 16 <= w or not words, (k, words, w)
                segs.append(f'<p class="seg {css[c]}" style="width:{w}px">{words}</p>' if words
                            else f'<div class="seg {css[c]}" style="width:{w}px"></div>')
        assert i == len(steps), (k, i, len(steps))
        rows.append(f'<div class="row" style="gap:0;align-items:center"><div class="col fix" style="width:{LABW}px;'
                    f'gap:0"><p class="small strong">{name}</p><p class="small soft">{VALUES[k + ".min"]} min</p>'
                    f'</div><div class="row" style="gap:2px">' + "".join(segs) + "</div></div>")
    line = (f'<div style="position:absolute;left:{LABW + 60 * PX}px;top:0;width:3px;height:{32 + 4 * 77}px;'
            f'background:{RUST}"></div>')
    return (f'<div class="col" style="gap:12px;position:relative">\n' + "\n".join(rows) + "\n" + line + "\n</div>")


def chart_blank():
    """Where the blank of each design comes from (nominal): shares of its current or of its enzymes."""
    TW = 1300
    d1 = D["t1"]["diagnostics"]
    we = d1["N_nsb_we"]
    up = (d1["N_up_bore"] + d1["N_up_line"]) * d1["collected_upstream"]
    lid = d1["N_nsb_lid"] * d1["collected_lid"]
    conj = d1["Q_nsb_C"] / (d1["Q_nsb_C"] + d1["Q_imp_C"] + d1["Q_hyd_C"])
    t1 = [("c-ink", "on the electrode", conj * we / (we + up + lid)),
          ("c-orange", "bore and line", conj * up / (we + up + lid)),
          ("c-sand", "", conj * lid / (we + up + lid)),
          ("c-teal", "", 1 - conj)]
    rows = [("Tier 1", "by blank current", t1)]
    for k, name in (("t2", "Tier 2"), ("t3", "Tier 3, one valve")):
        sp = EXTRA["blank_split"][k]
        tot = sum(sp.values())
        rows.append((name, "by enzymes of the blank",
                     [("c-ink", "on the beads", sp["beads"] / tot), ("c-slate", "on the frit", sp["frit"] / tot),
                      ("c-orange", "walls above the bed" if k == "t2" else "valve loop", sp["walls"] / tot),
                      ("c-sand", "", sp["bore"] / tot)]))
    out = []
    for name, sub, parts in rows:
        segs, x = [], 0.0
        for cls, words, share in parts:
            if share <= 0.002:
                continue
            a, b = round(x * TW), round((x + share) * TW)
            x += share
            w = b - a - 2
            text = f"{words} {100 * share:.0f} %" if words else (f"{100 * share:.0f} %" if w >= 64 else "")
            if (len(text) * 14.5 + 12) > w:
                text = f"{100 * share:.0f} %" if w >= 64 else ""
            segs.append(f'<p class="part {cls}" style="width:{w}px">{text}</p>')
        assert abs(x - 1) < 1e-6, (name, x)
        out.append(f'<div class="row" style="gap:24px;align-items:center"><div class="col fix" style="width:300px;'
                   f'gap:0"><p class="strong">{name}</p><p class="small soft">{sub}</p></div>'
                   f'<div class="row" style="gap:2px">' + "".join(segs) + "</div></div>")
    return '<div class="col" style="gap:18px">\n' + "\n".join(out) + "\n</div>"


def chart_review():
    """Findings of the two review rounds by severity (docs/31 sections 3 and 4)."""
    PXF = 30
    rounds = [("Round 1", "first version, three reviewers", [("sev-3", "blocking", 4), ("sev-2", "significant", 19),
                                                              ("sev-1", "minor", 12)]),
              ("Round 2", "Revision B, two reviewers", [("sev-2", "significant", 11), ("sev-1", "minor", 13)])]
    out = []
    for name, sub, parts in rounds:
        segs = []
        for cls, word, n in parts:
            w = n * PXF - 2
            text = f"{n} {word}" if (len(f"{n} {word}") * 14.5 + 12) <= w else str(n)
            segs.append(f'<p class="part {cls}" style="width:{w}px">{text}</p>')
        total = sum(n for _, _, n in parts)
        out.append(f'<div class="row" style="gap:24px;align-items:center"><div class="col fix" style="width:330px;'
                   f'gap:0"><p class="strong">{name}</p><p class="small soft">{sub}</p></div>'
                   f'<div class="row" style="gap:2px">' + "".join(segs) + "</div>"
                   f'<p class="strong">{total} findings</p></div>')
    return '<div class="col" style="gap:18px">\n' + "\n".join(out) + "\n</div>"


def chart_revisions():
    """Nominal detection limit of each design through the three versions (docs/31 section 2)."""
    series = [("Tier 1", [3.1, 9.4, D["t1"]["lod_nominal"]], "redesigned twice"),
              ("Tier 2", [0.75, 2.6, D["t2"]["lod_nominal"]], "same design, new blank terms"),
              ("Tier 3, one valve", [None, 1.5, D["t3"]["lod_nominal"]], "became the tier-3 design"),
              ("Tier 3 with transfer", [0.33, 0.62, D["t3t"]["lod_nominal"]], "release 0.7, 0.7, then 0.35")]
    W, H, GUT = 392, 388, 72
    xs = [GUT + 46, GUT + 150, GUT + 254]
    ly = lambda v: 320 - (math.log10(v) - math.log10(0.2)) * 150
    panels = []
    for name, vals, note in series:
        said = ", ".join(f"{t} {f2(v)}" for t, v in zip(("first version", "Revision B", "Revision C"), vals) if v)
        s = [svg_open(W, H, f"{name}: nominal detection limit in pg/mL, {said}.")]
        for v in (0.3, 3, 10):
            s.append(f'<path d="M{GUT} {ly(v):.1f}H{W - 16}" stroke="{BORDER}" stroke-width="2"/>')
        s.append(f'<path d="M{GUT} {ly(1):.1f}H{W - 16}" stroke="{RUST}" stroke-width="3"/>')
        pts = [(x, ly(v)) for x, v in zip(xs, vals) if v]
        s.append('<path d="M' + " L".join(f"{x} {y:.1f}" for x, y in pts) + f'" fill="none" stroke="{INK}" '
                 'stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>')
        labs = []
        for j, (x, v) in enumerate(zip(xs, vals)):
            if not v:
                labs.append(pin("tick", x - 56, ly(1) - 66, 112, "not computed", "center"))
                continue
            s.append(f'<circle cx="{x}" cy="{ly(v):.1f}" r="11" fill="{REV[j]}" stroke="{CREAM}" stroke-width="3"/>')
            near = [u for u in (vals[j - 1] if j else None, vals[j + 1] if j < 2 else None) if u]
            above = all(v >= u for u in near)
            labs.append(pin("lab strong", x - 45, ly(v) - 48 if above else ly(v) + 18, 90, f2(v), "center"))
        for v in (0.3, 1, 3, 10):
            labs.append(pin("tick", 0, ly(v) - 15, GUT - 12, f"{v:g}", "right"))
        for x, t in zip(xs, ("first", "B", "C")):
            labs.append(pin("tick", x - 50, 340, 100, t, "center"))
        s.append("</svg>")
        panels.append(f'<div class="col fix" style="width:{W}px;gap:8px"><p class="strong">{name}</p>'
                      f'<div class="host" style="width:{W}px;height:{H}px">\n' + "".join(s) + "\n" + "\n".join(labs)
                      + f'\n</div><p class="small soft">{note}</p></div>')
    return '<div class="row" style="gap:32px">\n' + "\n".join(panels) + "\n</div>"


def chart_heat():
    """Nominal detection limit of every design in seven cases; darker means a higher limit."""
    rows = [("spec", "As specified"), ("L67", "Slow-releasing detection antibody, purer substrate"),
            ("L367", "The same, and a conjugate that sticks less (assumed)"),
            ("ND", "The substrate’s background does not decay"),
            ("S1", "Conjugate sticks 25 times more than assumed"),
            ("S4", "Substrate carries 10⁻³ oxidisable impurity"),
            ("P01", "Only 1 % of the enzyme’s product is electroactive")]

    def shade(v):
        return "h-1" if v <= 1 else "h-2" if v <= 3 else "h-3" if v <= 10 else "h-4" if v <= 100 else "h-5"

    cells = ['<p class="colhead"></p>'] + [f'<p class="colhead">{a}<br>{b}</p>' for a, b in HEADS]
    for s, words in rows:
        cells.append(f'<p class="rowhead">{words}</p>')
        for k, _, _ in TIER_NAMES:
            v = SCEN[k][SCENARIO[s]]["lod_nominal"]
            cells.append(f'<p class="cell {shade(float(f2(v)))}">{f2(v)}</p>')
    return '<div class="grid4">\n' + "\n".join(cells) + "\n</div>"


def chart_transfer():
    """Nominal detection limit of the transfer design against the released fraction (chart_extra.py)."""
    a, b = EXTRA["transfer_vs_release"], EXTRA["transfer_vs_release_screened"]
    one, one_s = EXTRA["one_valve"], EXTRA["one_valve_screened"]
    W, H = 1000, 512
    x0, x1, yt, yb = 120, 790, 60, 420
    lx = lambda r: x0 + r * (x1 - x0)
    ly = lambda v: yb - (math.log10(v) + 1) * (yb - yt) / 2
    va, vb = dict(map(tuple, a)), dict(map(tuple, b))
    cross = next(r0 + (r1 - r0) * (v0 - one) / (v0 - v1) for (r0, v0), (r1, v1) in zip(a, a[1:]) if v0 >= one > v1)
    s = [svg_open(W, H, "Line chart of the nominal detection limit of the transfer design against the share of the "
                        f"complex released in 5 minutes. As specified it falls from {f2(va[0.05])} pg/mL at 5 % to "
                        f"{f2(va[0.35])} at 35 % and {f2(va[0.7])} at 70 %; with screened reagents it is "
                        f"{f2(vb[0.7])} at 70 %. One valve without a transfer gives {f2(one)}, and {f2(one_s)} "
                        f"with screened reagents; as specified, the transfer is better above a release of about "
                        f"{100 * cross:.0f} %.")]
    s.append(f'<rect x="{lx(0.05):.0f}" y="{yt}" width="{lx(0.74) - lx(0.05):.0f}" height="{yb - yt}" fill="#F3EFE6"/>')
    for v in (0.1, 0.3, 1, 3, 10):
        s.append(f'<path d="M{x0} {ly(v):.1f}H{x1}" stroke="{GRID}" stroke-width="2"/>')
    for r in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
        s.append(f'<path d="M{lx(r):.0f} {yb}v8" stroke="{STEEL}" stroke-width="2"/>')
    s.append(f'<path d="M{x0} {yb}H{x1}" stroke="{STEEL}" stroke-width="2"/>')
    s.append(f'<path d="M{x0} {ly(one):.1f}H{x1}" stroke="{BLUE}" stroke-width="2"/>')
    s.append(f'<path d="M{x0} {ly(one_s):.1f}H{x1}" stroke="{ORANGE}" stroke-width="2"/>')
    for data, col in ((a, BLUE), (b, ORANGE)):
        s.append(f'<path d="{smooth([(lx(r), ly(v)) for r, v in data])}" fill="none" stroke="{col}" '
                 f'stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append(f'<path d="M{lx(cross):.1f} {ly(one):.1f}V{yb}" stroke="{SLATE}" stroke-width="2"/>')
    for r, vals, col in ((0.35, va, BLUE), (0.7, va, BLUE), (0.7, vb, ORANGE)):
        s.append(f'<circle cx="{lx(r):.1f}" cy="{ly(vals[r]):.1f}" r="10" fill="{col}" stroke="{CARD}" '
                 f'stroke-width="3"/>')
    s.append("</svg>")
    out = ["".join(s)]
    out.append(pin("lab strong", 28, 14, 700, "Detection limit of tier 3 with transfer, pg/mL (log scale)"))
    for v, t in ((0.1, "0.1"), (0.3, "0.3"), (1, "1"), (3, "3"), (10, "10")):
        out.append(pin("tick", 20, ly(v) - 15, 88, t, "right"))
    for r in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
        out.append(pin("tick", lx(r) - 50, yb + 18, 100, f"{100 * r:.0f} %", "center"))
    out.append(pin("tick", x0, yb + 52, x1 - x0, "share of the complex released in 5 min", "center"))
    out.append(pin("tick", lx(0.24), yt + 6, 330, "range sampled: 5 % to 74 %; nothing is measured"))
    out.append(pin("lab", x1 + 10, ly(one) - 30, W - x1 - 14, f"one valve: <b>{f2(one)}</b>"))
    out.append(pin("lab", x1 + 10, ly(one_s), W - x1 - 14, f"screened: <b>{f2(one_s)}</b>"))
    out.append(pin("lab strong", lx(0.35) - 35, ly(one) - 36, 70, f2(va[0.35]), "center"))
    out.append(pin("lab strong", lx(0.7) - 86, ly(va[0.7]) + 14, 76, f2(va[0.7]), "right"))
    out.append(pin("lab strong", lx(0.7) - 30, ly(vb[0.7]) + 16, 90, f2(vb[0.7])))
    out.append(pin("lab", lx(cross) + 10, yb - 40, 220, f"pays above ≈ {100 * cross:.0f} %"))
    return f'<div class="host plate" style="width:{W + 4}px;height:{H + 4}px">\n' + "\n".join(out) + "\n</div>"


CHARTS = {"conv": chart_conv, "lod": chart_lod, "timeline": chart_timeline, "blank": chart_blank,
          "review": chart_review, "revisions": chart_revisions, "heat": chart_heat, "transfer": chart_transfer}
ART_OPTS = {"kit": dict(plate=True, dx=30, dy=0, h=360), "trace_t1": dict(plate=True), "trace_t2": dict(plate=True),
            "trace_t3": dict(plate=True)}


def expand(text):
    def one(m):
        kind, name = m.group(1), m.group(2)
        if kind == "art":
            return art(name, **ART_OPTS.get(name, {}))
        if kind == "pict":
            return pict(name)
        if kind == "chart":
            return CHARTS[name]()
        return VALUES[name]
    return keep_units(re.sub(r"\{\{(art|pict|chart|n):([A-Za-z0-9_.]+)\}\}", one, text))


UNIT = r"(?:%|µL/min|µL|nL|mm²|mm|µm|min|pg/mL|nM|mM|pM|µC|nC|pA|bar|psi|V|h|s)(?![A-Za-z0-9])"


def keep_units(text):
    """A no-break space between a number and its unit, and after "pH", in the words of a slide (not in tags)."""
    parts = re.split(r"(<[^>]*>)", text)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r"(?<=\d) (?=" + UNIT + ")", "\u00a0", parts[i])
        parts[i] = parts[i].replace("pH ", "pH\u00a0")
    return "".join(parts)


# ---------------------------------------------------------------- checks of what the slide format allows
class Count(HTMLParser):
    VOID = {"br", "hr", "img", "path", "rect", "circle", "line", "polygon", "polyline", "ellipse", "use", "stop"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.n, self.depth, self.maxdepth, self.stack, self.insvg = 0, 0, 0, [], 0
        self.pinned, self.sizes, self.problems = {}, [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "svg":
            self.insvg += 1
            self.n += 1
        elif not self.insvg:
            self.n += 1
        if self.insvg and tag in ("text", "style", "script", "foreignobject", "image"):
            self.problems.append(f"<{tag}> inside an svg")
        style, cls = a.get("style") or "", a.get("class") or ""
        for m in re.finditer(r"font-size:\s*([\d.]+)px", style):
            if float(m.group(1)) < 24:
                self.problems.append(f"font-size {m.group(1)}px on <{tag}>")
        if not self.insvg or tag == "svg":
            if "position:absolute" in style.replace(" ", "") or re.search(r"\b(lab|tick)\b", cls):
                host = next((i for i in reversed(self.stack) if i[0] == "div"), None)
                key = id(host) if host else 0
                self.pinned[key] = self.pinned.get(key, 0) + 1
        if tag == "div":
            self.depth += 1
            self.maxdepth = max(self.maxdepth, self.depth)
        if tag not in self.VOID:
            self.stack.append([tag])

    def handle_endtag(self, tag):
        if tag == "svg":
            self.insvg -= 1
        if tag == "div":
            self.depth -= 1
        if any(i[0] == tag for i in self.stack):
            while self.stack[-1][0] != tag:
                self.stack.pop()
            self.stack.pop()


def check(sid, text):
    out = []
    if not re.fullmatch(rf'<section id="{sid}"[^>]*>.*</aside>\s*</section>\s*', text, flags=re.S):
        out.append("not one <section> that ends with its <aside>")
    if "{{" in text:
        out.append("unreplaced placeholder")
    c = Count()
    c.feed(text)
    out += c.problems
    if c.n > 200:
        out.append(f"{c.n} elements (limit 200)")
    if c.maxdepth > 15:
        out.append(f"{c.maxdepth} nested divs (limit 15)")
    if c.pinned and max(c.pinned.values()) > 24:
        out.append(f"{max(c.pinned.values())} pinned children in one box (limit 24)")
    for m in re.finditer(r"<svg\b.*?</svg>", text, flags=re.S):
        if len(m.group(0).encode("utf-8")) > 52000:
            out.append(f"an svg of {len(m.group(0).encode('utf-8'))} bytes (limit 52 KB)")
    notes = re.search(r"<aside>(.*?)</aside>", text, flags=re.S)
    if notes and len(notes.group(1)) > 4000:
        out.append(f"notes of {len(notes.group(1))} characters (limit 4000)")
    for m in re.finditer(r"z-index|clip-path|float:|<style|<script|data:image|\son[a-z]+=",
                         re.sub(r"<svg\b.*?</svg>", "", text, flags=re.S)):
        out.append(f"not allowed in a slide: {m.group(0)}")
    return c, out


def main():
    order = json.loads((DECK / "deck.json").read_text(encoding="utf-8"))["order"]
    OUT.mkdir(exist_ok=True)
    bad = 0
    for sid in order:
        src = TEMPL / f"{sid}.html"
        if not src.exists():
            print(f"{sid:10s} no template yet")
            continue
        text = expand(src.read_text(encoding="utf-8")).strip() + "\n"
        c, problems = check(sid, text)
        (OUT / f"{sid}.html").write_text(text, encoding="utf-8")
        most = max(c.pinned.values()) if c.pinned else 0
        print(f"{sid:10s} {len(text.encode('utf-8')):6d} bytes  {c.n:3d} elements  divs {c.maxdepth:2d} deep  "
              f"pinned {most:2d}" + ("" if not problems else "   PROBLEMS: " + "; ".join(problems)))
        bad += len(problems)
    extra = sorted(p.stem for p in TEMPL.glob("*.html") if p.stem not in order)
    if extra:
        print("templates not in deck.json:", extra)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
