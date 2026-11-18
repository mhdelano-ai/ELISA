import json, os
ART = os.path.dirname(os.path.abspath(__file__))
INK = '#14213D'; CARD = '#FFFDF8'; SAND = '#ECE7DB'; STEEL = '#9AA5B8'; SLATE = '#5E6B85'
BLUE = '#1F5A96'; PBLUE = '#E3EBF5'; ORANGE = '#D9773F'; GOLD = '#C9A227'; CARBON = '#2B2F3A'
PTEAL = '#CFE5DF'; BEAD = '#8A5A3C'
J = 'stroke-linejoin="round" stroke-linecap="round"'


def f(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')


def rect(x, y, w, h, fill, stroke=None, sw=3):
    s = f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}" {J}'
    return s + '/>'


def line(x1, y1, x2, y2, col=INK, sw=2, extra=''):
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{col}" stroke-width="{sw}" {J}{extra}/>'


def path(d, col, sw, fill='none', extra=''):
    return f'<path d="{d}" fill="{fill}" stroke="{col}" stroke-width="{sw}" {J}{extra}/>'


def arrow(d):
    return path(d, BLUE, 4, extra=' marker-end="url(#ah)"')


def leader(x1, y1, x2, y2):
    return line(x1, y1, x2, y2, SLATE, 2)


def base(variant):
    o = []
    o.append('<defs><marker id="ah" viewBox="0 0 12 12" refX="6" refY="6" markerWidth="12" markerHeight="12" '
             'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L12,6 L0,12 Z" fill="' + BLUE + '"/></marker></defs>')
    # lid block with bore and outlet cut out (drawn as pieces)
    o.append(rect(170, 150, 450, 292, CARD, INK, 3))
    # strip
    o.append(rect(170, 470, 450, 50, SAND, INK, 3))
    # gap liquid
    o.append(rect(200, 442, 390, 28, PBLUE))
    # bore liquid
    o.append(rect(359, 150, 72, 292, PBLUE))
    # outlet liquid in block
    o.append(rect(527, 150, 26, 292, PBLUE))
    # waste tube above block: outer ink then lumen
    wd = 'M540,152 L540,140 Q540,110 570,110 L780,110'
    o.append(path(wd, INK, 30))
    o.append(path(wd, PBLUE, 24))
    o.append(rect(529, 140, 22, 14, PBLUE))
    # walls of bore and outlet
    for x in (359, 431, 527, 553):
        o.append(line(x, 150, x, 442, INK, 3))
    # lid underside segments
    for a, b in ((170, 359), (431, 527), (553, 620)):
        o.append(line(a, 442, b, 442, INK, 3))
    # top edge of block (between openings)
    # electrode layer
    we = GOLD if variant == 1 else CARBON
    o.append(rect(195, 470, 70, 12, CARBON, INK, 2))
    o.append(rect(285, 470, 220, 12, we, INK, 2))
    o.append(rect(525, 470, 70, 12, STEEL, INK, 2))
    return o


def orings():
    return [f'<circle cx="{x}" cy="452" r="18" fill="{SLATE}" stroke="{INK}" stroke-width="3"/>' for x in (200, 590)]


def flow_common(o, bore_from, bore_to):
    o.append(arrow(f'M395,{bore_from} L395,{bore_to}'))
    o.append(arrow('M380,456 L300,456'))
    o.append(arrow('M410,456 L512,456'))
    o.append(arrow('M540,420 L540,190'))


def t1():
    o = base(1)
    # inlet tube 22 px from top edge to block top
    o.append(rect(384, 0, 22, 152, PBLUE))
    o.append(line(385, 0, 385, 150, INK, 2)); o.append(line(405, 0, 405, 150, INK, 2))
    # orange conjugate
    oc = f' stroke-width="5"'
    o.append(line(388.5, 2, 388.5, 150, ORANGE, 5)); o.append(line(401.5, 2, 401.5, 150, ORANGE, 5))
    o.append(line(362.5, 152, 362.5, 440, ORANGE, 5)); o.append(line(427.5, 152, 427.5, 440, ORANGE, 5))
    for a, b in ((218, 359), (431, 527), (553, 572)):
        o.append(line(a, 445.5, b, 445.5, ORANGE, 5))
    # antibodies
    xs = [296 + i * 25 for i in range(9)]
    held = {1, 4, 7}
    for i, x in enumerate(xs):
        o.append(path(f'M{x},470 L{x},461 L{x-7},450 M{x},461 L{x+7},450', SLATE, 3))
        if i in held:
            o.append(f'<circle cx="{x}" cy="451" r="6" fill="{BLUE}" stroke="{INK}" stroke-width="2"/>')
    o += orings()
    o.append(arrow('M395,175 L395,425'))
    o.append(arrow('M286,456 L262,456'))
    o.append(arrow('M504,456 L540,456 L540,190'))
    # dimension mark across the gap
    o.append(line(236, 445, 236, 467, INK, 2)); o.append(line(230, 444, 242, 444, INK, 2))
    o.append(line(230, 468, 242, 468, INK, 2))
    # leaders
    o.append(leader(384, 45, 366, 45))            # inlet line
    o.append(leader(365, 215, 168, 215))          # bore
    o.append(leader(362.5, 330, 168, 330))        # conjugate walls
    o.append(leader(232, 446, 232, 470) if False else '')
    o.append(leader(168, 425, 236, 425)); o.append(leader(236, 425, 236, 442))   # gap, clear of the O-ring
    o.append(leader(608, 444, 632, 412))          # O-ring
    o.append(leader(612, 500, 632, 500))          # strip
    o.append(leader(346, 484, 346, 532))          # antibody on WE
    o.append(leader(740, 123, 740, 132) if False else '')
    labels = [
        dict(key='inlet_line', text='inlet line from the autosampler', x=150, y=15, w=208, align='right'),
        dict(key='bore', text='inlet bore, 0.8 mm', x=4, y=185, w=156, align='right'),
        dict(key='conjugate', text='conjugate sticks to these walls too (orange)', x=4, y=270, w=156, align='right'),
        dict(key='gap', text='gap: 0.2 mm assumed (not to scale)', x=4, y=410, w=156, align='right'),
        dict(key='capture', text='capture antibody on the gold working electrode', x=190, y=540, w=410, align='center'),
        dict(key='oring', text='O-ring, 8 mm', x=640, y=382, w=160, align='left'),
        dict(key='waste', text='to waste', x=650, y=132, w=140, align='left'),
        dict(key='strip', text='printed strip', x=640, y=470, w=160, align='left'),
    ]
    return o, labels


def t2():
    o = base(2)
    # sleeve
    o.append(rect(359, 150, 16, 250, SAND, INK, 2)); o.append(rect(415, 150, 16, 250, SAND, INK, 2))
    # capillary walls
    o.append(rect(375, 0, 12, 400, PBLUE, INK, 2)); o.append(rect(403, 0, 12, 400, PBLUE, INK, 2))
    # lumen
    o.append(rect(388, 0, 14, 316, PBLUE))
    o.append(rect(388, 316, 14, 70, PTEAL))
    o.append(line(375, 400, 415, 400, INK, 2))
    # beads
    y = 321.0; row = 0
    while y <= 382:
        cx = [391, 399] if row % 2 == 0 else [395]
        for x in cx:
            o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="4" fill="{BEAD}" stroke="{INK}" stroke-width="1.5"/>')
        y += 6.8; row += 1
    # frit
    o.append(rect(387, 386, 16, 14, SLATE))
    o.append(rect(386.5, 383.5, 17, 17, 'none', ORANGE, 3))
    # orange on lumen walls above bed
    o.append(line(389.5, 150, 389.5, 314, ORANGE, 5)); o.append(line(400.5, 150, 400.5, 314, ORANGE, 5))
    # redraw capillary wall outlines over orange edge
    o.append(line(387, 0, 387, 400, INK, 2)); o.append(line(403, 0, 403, 400, INK, 2))
    o += orings()
    o.append(arrow('M395,30 L395,130'))
    o.append(arrow('M395,408 L395,436'))
    o.append(arrow('M380,456 L300,456'))
    o.append(arrow('M410,456 L512,456'))
    o.append(arrow('M540,420 L540,190'))
    o.append(leader(375, 40, 366, 40))       # capillary
    o.append(leader(366, 175, 168, 175))     # sleeve
    o.append(leader(388, 352, 168, 262))     # bed
    o.append(leader(387, 393, 168, 372))     # frit
    o.append(leader(380, 405, 168, 440))     # tip
    o.append(leader(440, 482, 440, 532))     # WE
    labels = [
        dict(key='capillary', text='capillary, 0.2 mm bore', x=150, y=15, w=208, align='right'),
        dict(key='sleeve', text='sleeve', x=4, y=160, w=156, align='right'),
        dict(key='bed', text='bed: 1 million beads of 2.8 µm, 0.6 mm long', x=4, y=202, w=156, align='right'),
        dict(key='frit', text='frit', x=4, y=357, w=156, align='right'),
        dict(key='tip', text='tip 1 mm above the electrode', x=4, y=410, w=156, align='right'),
        dict(key='conjugate', text='orange: conjugate on the walls above the bed and on the frit', x=640, y=230, w=156, align='left'),
        dict(key='waste', text='to waste', x=650, y=132, w=140, align='left'),
        dict(key='we', text='printed carbon working electrode', x=170, y=545, w=450, align='center'),
    ]
    return o, labels


ARIA = {
    'cell_t1': 'Cross-section of a wall-jet flow cell on a printed strip: liquid runs down a central bore, spreads through a thin gap over a gold working electrode carrying capture antibodies, and leaves up an outlet to waste; conjugate coats the tube, bore and gap ceiling.',
    'cell_t2': 'The same flow cell with a glass capillary in the bore holding a packed bead bed on a frit just above a carbon working electrode; conjugate coats the capillary walls above the bed and the frit.',
}
for name, fn in (('cell_t1', t1), ('cell_t2', t2)):
    o, labels = fn()
    for l in labels:
        l.setdefault('size', 24); l.setdefault('weight', 400)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600" role="img" '
           f'aria-label="{ARIA[name]}">' + ''.join(x for x in o if x) + '</svg>')
    open(os.path.join(ART, name + '.svg'), 'w').write(svg)
    json.dump(labels, open(os.path.join(ART, name + '.labels.json'), 'w'), ensure_ascii=False, indent=1)
