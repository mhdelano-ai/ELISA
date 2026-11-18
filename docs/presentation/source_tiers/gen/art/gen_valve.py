import math, json, os
ART = os.path.dirname(os.path.abspath(__file__))
INK = "#14213D"; CARD = "#FFFDF8"; SAND = "#ECE7DB"; SANDB = "#D9D2C2"; STEEL = "#9AA5B8"
SLATE = "#5E6B85"; BLUE = "#1F5A96"; PBLUE = "#E3EBF5"; MBLUE = "#B9CCE3"; TEAL = "#2F8072"
PTEAL = "#CFE5DF"; BEAD = "#8A5A3C"
CY = 270; R = 110; RG = 80
ANG = {1: 120, 2: 180, 3: 240, 4: 300, 5: 0, 6: 60}

def f(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")

def pol(cx, r, a):
    t = math.radians(a)
    return cx + r * math.cos(t), CY - r * math.sin(t)

def arrow(x, y, dx, dy, col=BLUE, s=11):
    n = math.hypot(dx, dy); dx /= n; dy /= n
    px, py = -dy, dx
    tip = (x + dx * s, y + dy * s)
    b1 = (x - dx * s + px * s * 0.85, y - dy * s + py * s * 0.85)
    b2 = (x - dx * s - px * s * 0.85, y - dy * s - py * s * 0.85)
    pts = " ".join(f(a) + "," + f(b) for a, b in (tip, b1, b2))
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (pts, col, col)

def groove(cx, a, b, col, w):
    # a -> b (degrees), going the short way
    p0 = pol(cx, 97, a); p1 = pol(cx, RG, a); p2 = pol(cx, RG, b); p3 = pol(cx, 97, b)
    sweep = 0 if (b - a) % 360 < 180 else 1  # ccw in math = sweep 0 on screen
    d = "M%s %s L%s %s A%d %d 0 0 %d %s %s L%s %s" % (f(p0[0]), f(p0[1]), f(p1[0]), f(p1[1]), RG, RG, sweep,
                                                       f(p2[0]), f(p2[1]), f(p3[0]), f(p3[1]))
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%d" stroke-linecap="round" stroke-linejoin="round"/>' % (d, col, w)

def groove_arrow(cx, amid, ccw):
    x, y = pol(cx, RG, amid)
    t = math.radians(amid)
    dx, dy = -math.sin(t), -math.cos(t)
    if not ccw:
        dx, dy = -dx, -dy
    return arrow(x, y, dx, dy, s=10)

def line(pts, col, w):
    d = "M" + " L".join("%s %s" % (f(x), f(y)) for x, y in pts)
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%d" stroke-linecap="round" stroke-linejoin="round"/>' % (d, col, w)

def panel(cx, mode):
    o = []
    p = {k: pol(cx, R, a) for k, a in ANG.items()}
    loopcol = BLUE if mode == "in" else TEAL
    # plumbing
    o.append(line([(cx - 200, 105), (p[1][0], 105), (p[1][0], p[1][1] - 13)], BLUE, 6))
    o.append(line([(p[6][0], p[6][1] - 13), (p[6][0], 105), (cx + 168, 105)], BLUE, 6))
    o.append(line([(p[2][0] - 13, CY), (cx - 190, CY), (cx - 190, 460), (cx - 85, 460)], loopcol, 6))
    o.append(line([(cx + 85, 460), (cx + 190, 460), (cx + 190, CY), (p[5][0] + 13, CY)], loopcol, 6))
    # flow cell icon
    # a block with the end of a printed strip showing, as on the cover
    o.append('<rect x="%s" y="99" width="36" height="12" fill="%s" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (f(cx + 208), SAND, INK))
    for px in (230, 237):
        o.append('<rect x="%s" y="102" width="4" height="6" fill="%s"/>' % (f(cx + px), STEEL))
    o.append('<rect x="%s" y="88" width="46" height="34" rx="6" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (f(cx + 168), PBLUE, INK))
    o.append('<circle cx="%s" cy="105" r="7" fill="%s" stroke="%s" stroke-width="2"/>' % (f(cx + 196), "#C9A227", INK))
    # bed
    bx, by = cx - 85, 445
    o.append('<rect x="%s" y="%s" width="170" height="30" rx="4" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (f(bx), by, PBLUE if mode == "in" else PTEAL, INK))
    for ri, yy in enumerate((452.5, 460, 467.5)):
        x0 = bx + 5.5 + (4.25 if ri % 2 else 0)
        x = x0
        while x <= bx + 116:
            o.append('<circle cx="%s" cy="%s" r="4" fill="%s"/>' % (f(x), f(yy), BEAD))
            x += 8.5
    o.append('<rect x="%s" y="447" width="12" height="26" fill="%s"/>' % (f(bx + 120), SLATE))
    # valve body
    o.append('<circle cx="%s" cy="%d" r="%d" fill="%s" stroke="%s" stroke-width="3"/>' % (f(cx), CY, R, CARD, INK))
    o.append('<circle cx="%s" cy="%d" r="10" fill="%s" stroke="%s" stroke-width="2"/>' % (f(cx), CY, SAND, INK))
    # grooves
    if mode == "in":
        o.append(groove(cx, 120, 180, MBLUE, 14)); o.append(groove(cx, 120, 180, BLUE, 6))
        o.append(groove(cx, 0, 60, MBLUE, 14)); o.append(groove(cx, 0, 60, BLUE, 6))
        o.append(groove(cx, 240, 300, STEEL, 12))
    else:
        o.append(groove(cx, 120, 60, MBLUE, 14)); o.append(groove(cx, 120, 60, BLUE, 6))
        o.append(groove(cx, 180, 240, PTEAL, 14)); o.append(groove(cx, 180, 240, TEAL, 6))
        o.append(groove(cx, 300, 360, PTEAL, 14)); o.append(groove(cx, 300, 360, TEAL, 6))
    # plugs on 3 and 4
    for k in (3, 4):
        t = math.radians(ANG[k])
        ux, uy = math.cos(t), -math.sin(t)
        s0 = (p[k][0] + ux * 13, p[k][1] + uy * 13); s1 = (p[k][0] + ux * 25, p[k][1] + uy * 25)
        o.append(line([s0, s1], INK, 4))
        qx, qy = -uy, ux
        o.append(line([(s1[0] + qx * 9, s1[1] + qy * 9), (s1[0] - qx * 9, s1[1] - qy * 9)], INK, 6))
    # ports
    for k in range(1, 7):
        o.append('<circle cx="%s" cy="%s" r="13" fill="%s" stroke="%s" stroke-width="3"/>' % (f(p[k][0]), f(p[k][1]), CARD, INK))
        if (mode == "in" and k not in (3, 4)) or k in (1, 6):
            o.append('<circle cx="%s" cy="%s" r="5" fill="%s"/>' % (f(p[k][0]), f(p[k][1]), BLUE))
        elif k in (2, 3, 4, 5):
            o.append('<circle cx="%s" cy="%s" r="5" fill="%s"/>' % (f(p[k][0]), f(p[k][1]), TEAL if mode == "out" else STEEL))
    # arrows
    o.append(arrow(cx - 125, 105, 1, 0))
    o.append(arrow(p[1][0], 132, 0, 1))
    o.append(arrow(p[6][0], 132, 0, -1))
    o.append(arrow(cx + 120, 105, 1, 0))
    if mode == "in":
        o.append(groove_arrow(cx, 150, True))
        o.append(groove_arrow(cx, 30, True))
        o.append(arrow(cx - 190, 370, 0, 1))
        o.append(arrow(cx - 135, 460, 1, 0))
        o.append(arrow(cx + 135, 460, 1, 0))
        o.append(arrow(cx + 190, 370, 0, -1))
    else:
        o.append(groove_arrow(cx, 90, False))
    return o

body = []
body += panel(250, "in")
body += panel(750, "out")
body.append('<path d="M500 70 L500 520" stroke="%s" stroke-width="2" stroke-linecap="round"/>' % SANDB)
# leaders to "plugged"
body.append(line([(189, 394), (199, 405)], SLATE, 2))
body.append(line([(311, 394), (301, 405)], SLATE, 2))

svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="540" viewBox="0 0 1000 540" role="img" '
       'aria-label="Two positions of a six-port valve with a packed bead bed in its loop: in position IN the stream runs through the bed, in position OUT the stream bypasses it and the bed is closed at both ends.">'
       + "".join(body) + "</svg>")
open(os.path.join(ART, "valve.svg"), "w").write(svg)

L = []
def lab(key, text, x, y, w, align="center", size=24, weight=400):
    L.append(dict(key=key, text=text, x=x, y=y, w=w, align=align, size=size, weight=weight))
lab("title_in", "IN: stream passes through bed", 20, 12, 460, size=28, weight=600)
lab("title_out", "OUT: bed closed and bypassed", 520, 12, 460, size=28, weight=600)
POS = {1: (160, 160), 2: (100, 243), 3: (150, 350), 4: (350, 350), 5: (400, 243), 6: (340, 160)}
for mode, off in (("in", 0), ("out", 500)):
    for k, (x, y) in POS.items():
        lab("p%d_%s" % (k, mode), str(k), x + off - 15, y - 15, 30, weight=600)
lab("autosampler", "from the autosampler", 40, 60, 280, align="left")
lab("cell_in", "to the cell", 395, 134, 90)
lab("cell_out", "to the cell", 895, 134, 90)
lab("plugged", "plugged", 200, 392, 100)
lab("bed_in", "bead bed and frit in the loop", 40, 496, 420)
lab("bed_out", "product collects in the closed bed", 520, 496, 460)
json.dump(L, open(os.path.join(ART, "valve.labels.json"), "w"), indent=1)
print(len(svg))
