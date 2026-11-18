import json, os
ART = os.path.dirname(os.path.abspath(__file__))
INK, SLATE, RUST, STEEL, TEAL = "#14213D", "#5E6B85", "#A8481A", "#9AA5B8", "#2F8072"
SAND, PALE, MID = "#ECE7DB", "#E3EBF5", "#B9CCE3"


def axes():
    return (f'<path d="M50 250 L50 36" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M50 26 L43.5 39 L56.5 39 Z" fill="{INK}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
            f'<path d="M50 250 L494 250" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M506 250 L493 243.5 L493 256.5 Z" fill="{INK}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>')


def band(x0, x1, fill):
    return f'<rect x="{x0}" y="60" width="{x1-x0}" height="190" fill="{fill}"/>'


def trace(d):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>'


def dashed(x0, x1, y):
    return f'<path d="M{x0} {y} L{x1} {y}" fill="none" stroke="{SLATE}" stroke-width="2" stroke-dasharray="8 8"/>'


def leader(x0, y0, x1, y1):
    return f'<path d="M{x0} {y0} L{x1} {y1}" fill="none" stroke="{SLATE}" stroke-width="2" stroke-linecap="round"/>'


def svg(name, aria, body, labels):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="520" height="300" viewBox="0 0 520 300" role="img" '
         f'aria-label="{aria}">{body}</svg>')
    open(os.path.join(ART, name + ".svg"), "w").write(s)
    json.dump(labels, open(os.path.join(ART, name + ".labels.json"), "w"), indent=1)


def L(key, text, x, y, w, align="left", weight=400):
    return {"key": key, "text": text, "x": x, "y": y, "w": w, "align": align, "size": 24, "weight": weight}


common = [L("current", "current", 58, 0, 120), L("time", "time", 424, 262, 80, "right")]

# ---- t1
t1d = "M60 205 L140 205 C170 205 170 115 200 115 L290 115 C320 115 320 203 350 203 L495 203"
arrow = (f'<path d="M245 212 L245 111" fill="none" stroke="{RUST}" stroke-width="3" stroke-linecap="round"/>'
         f'<path d="M245 204 L238.5 215 L251.5 215 Z" fill="{RUST}" stroke="{RUST}" stroke-width="2" stroke-linejoin="round"/>'
         f'<path d="M245 119 L238.5 108 L251.5 108 Z" fill="{RUST}" stroke="{RUST}" stroke-width="2" stroke-linejoin="round"/>')
body = (band(80, 130, SAND) + band(215, 275, PALE) + band(370, 420, SAND) + dashed(130, 370, 204)
        + axes() + trace(t1d) + arrow)
svg("trace_t1", "Sketch of current versus time in continuous flow: a flat reference level, a rise to a plateau read in the middle window, and a return to the reference level, with the signal as the height of the plateau above the reference.",
    body, common + [L("ref1", "reference", 40, 262, 130, "center"), L("read", "read", 205, 262, 80, "center"),
                    L("ref2", "reference", 330, 262, 130, "center"), L("signal", "signal", 195, 70, 100, "center", 600)])

# ---- t2
t2d = ("M80 150 C130 200 180 215 250 215 L330 215 C345 140 352 72 366 72 "
       "C392 72 410 180 470 198 L495 198")
area2 = (f'<path d="M330 215 C345 140 352 72 366 72 C392 72 410 180 470 198 L495 198 L495 215 Z" '
         f'fill="{MID}" opacity="0.6"/>')
body = (f'<rect x="80" y="36" width="250" height="16" fill="{STEEL}"/>' + band(290, 330, SAND) + area2
        + dashed(330, 495, 215) + axes() + trace(t2d) + leader(452, 134, 446, 200))
svg("trace_t2", "Sketch of current versus time with the flow stopped: the current decays to a flat baseline, then the swept product gives a sharp peak whose area above the carried-forward baseline is the signal.",
    body, common + [L("stopped", "flow stopped", 80, 58, 200), L("baseline", "baseline", 214, 262, 110, "right"),
                    L("sweep", "sweep", 336, 262, 80), L("signal", "signal = area", 414, 66, 104, "left", 600)])

# ---- t3
t3d = "M60 200 L330 200 C345 200 355 82 374 82 C400 82 420 190 484 200 L495 200"
area3 = (f'<path d="M330 200 C345 200 355 82 374 82 C400 82 420 190 484 200 L495 200 Z" '
         f'fill="{MID}" opacity="0.6"/>')
body = (f'<rect x="150" y="36" width="180" height="16" fill="{TEAL}"/>' + band(290, 330, SAND) + area3
        + dashed(330, 495, 200) + axes() + trace(t3d) + leader(452, 122, 446, 192))
svg("trace_t3", "Sketch of current versus time with the cell in steady flow: a flat baseline while the bed valve is closed, then a peak when the valve opens, whose area above the baseline is the signal.",
    body, common + [L("closed", "valve closed", 150, 58, 180), L("baseline", "baseline", 214, 262, 110, "right"),
                    L("opens", "valve opens", 336, 4, 150), L("signal", "signal = area", 414, 54, 104, "left", 600)])
