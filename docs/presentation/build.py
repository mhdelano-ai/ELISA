"""Assemble the slide sources into one self-contained HTML file that opens in any browser.

Usage:  python docs/presentation/build.py
Builds every deck listed in DECKS: reads <source>/deck.json, <source>/slides/<id>.html and, if present,
<source>/deck.css (shared styles), and writes the HTML file named beside it.
"""
import json
import pathlib

here = pathlib.Path(__file__).parent
DECKS = [("source", "in_silico_summary.html"), ("source_cartridge", "cartridge_round.html")]

# Extra rules and script for decks that carry a deck.css: shapes and coordinate connectors.
SHAPES_CSS = """
  x-shape { display: block; }
  x-shape[kind=ellipse] { border-radius: 50%; }
  x-shape[kind=arrow-right] { clip-path: polygon(0 30%, 60% 30%, 60% 0, 100% 50%, 60% 100%, 60% 70%, 0 70%); }
  section hr { border: none; }
  x-connector[x1] { display: none; }
"""
CONNECTOR_JS = """
  document.querySelectorAll('x-connector[x1]').forEach((c) => {
    const g = (k) => +c.getAttribute(k), x1 = g('x1'), y1 = g('y1'), x2 = g('x2'), y2 = g('y2');
    const col = c.style.color || '#14213D', w = parseFloat(c.style.borderWidth) || 2;
    const s = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    s.setAttribute('style', 'position:absolute;left:0;top:0;width:100%;height:100%;overflow:visible');
    let head = '';
    if (c.getAttribute('head') !== 'none') {
      const a = Math.atan2(y2 - y1, x2 - x1), L = w * 3.2;
      const p = (d) => (x2 - L * Math.cos(a + d)) + ',' + (y2 - L * Math.sin(a + d));
      head = '<polygon points="' + x2 + ',' + y2 + ' ' + p(0.45) + ' ' + p(-0.45) + '" fill="' + col + '"/>';
    }
    s.innerHTML = '<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '" stroke="' + col +
      '" stroke-width="' + w + '"/>' + head;
    c.replaceWith(s);
  });
"""


def build(source, target):
    src = here / source
    deck = json.loads((src / "deck.json").read_text(encoding="utf-8"))
    slides = "\n".join(
        (src / "slides" / f"{sid}.html").read_text(encoding="utf-8").strip() for sid in deck["order"]
    )
    fonts = "\n".join(
        f'<link rel="stylesheet" href="{face["href"]}">' for face in deck["faces"].values() if "href" in face
    )
    css_file = src / "deck.css"
    shared_css = css_file.read_text(encoding="utf-8") + SHAPES_CSS if css_file.exists() else ""
    extra_js = CONNECTOR_JS if css_file.exists() else ""
    page = PAGE.format(title=deck["title"], fonts=fonts, slides=slides, shared_css=shared_css, extra_js=extra_js)
    (here / target).write_text(page, encoding="utf-8")
    print(f"wrote {here / target} ({len(deck['order'])} slides)")


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{fonts}
<style>
{shared_css}
  html, body {{ margin: 0; height: 100%; background: #0b161e; overflow: hidden; }}
  #stage {{ position: absolute; left: 50%; top: 50%; width: 1920px; height: 1080px; transform-origin: 0 0; }}
  section {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; box-sizing: border-box;
             overflow: hidden; }}
  section:not(.current) {{ display: none !important; }}
  section *, section *::before, section *::after {{ box-sizing: border-box; }}
  section h1, section h2, section h3, section p {{ margin: 0; }}
  section aside {{ display: none; }}
  section table {{ border-collapse: collapse; width: 100%; }}
  section th, section td {{ padding: 0.35em 0.6em; border-bottom: 1px solid rgba(19, 35, 47, 0.18);
                            vertical-align: top; text-align: left; }}
  x-connector {{ display: block; flex: none; height: 0; border-top-style: solid; position: relative; }}
  x-connector::after {{ content: ""; position: absolute; right: -2px; top: -9px; border-left: 12px solid currentColor;
                        border-top: 7px solid transparent; border-bottom: 7px solid transparent; }}
  #bar {{ position: fixed; left: 0; right: 0; bottom: 0; padding: 8px 16px; display: flex; gap: 16px;
          justify-content: center; align-items: center; font: 14px Arial, sans-serif; color: #b9c7cf; }}
  #bar button {{ font: inherit; color: inherit; background: #13232f; border: 1px solid #44525c; border-radius: 6px;
                 padding: 4px 12px; cursor: pointer; }}
  @media print {{
    html, body {{ overflow: visible; height: auto; background: none; }}
    #bar {{ display: none; }}
    #stage {{ position: static; transform: none !important; width: auto; height: auto; }}
    section, section:not(.current) {{ position: relative; display: flex !important; page-break-after: always; }}
    @page {{ size: 1920px 1080px; margin: 0; }}
  }}
</style>
</head>
<body>
<div id="stage">
{slides}
</div>
<div id="bar"><button id="prev">&#8592; Back</button><span id="count"></span><button id="next">Next &#8594;</button></div>
<script>
  const stage = document.getElementById('stage');
  const slides = Array.from(stage.querySelectorAll('section'));
  let i = Math.max(0, parseInt((location.hash.match(/slide-(\\d+)/) || [])[1] || '1', 10) - 1);
  function fit() {{
    const s = Math.min(innerWidth / 1920, (innerHeight - 44) / 1080);
    stage.style.transform = 'scale(' + s + ') translate(-50%, -50%)';
    stage.style.marginTop = '-22px';
  }}
  function show(n) {{
    i = Math.min(slides.length - 1, Math.max(0, n));
    slides.forEach((el, k) => el.classList.toggle('current', k === i));
    document.getElementById('count').textContent = (i + 1) + ' / ' + slides.length;
    history.replaceState(null, '', '#slide-' + (i + 1));
  }}
  document.getElementById('prev').onclick = () => show(i - 1);
  document.getElementById('next').onclick = () => show(i + 1);
  addEventListener('keydown', (e) => {{
    if (['ArrowRight', 'PageDown', ' '].includes(e.key)) show(i + 1);
    if (['ArrowLeft', 'PageUp'].includes(e.key)) show(i - 1);
    if (e.key === 'Home') show(0);
    if (e.key === 'End') show(slides.length - 1);
  }});
  addEventListener('resize', fit);
  addEventListener('hashchange', () => {{
    const n = parseInt((location.hash.match(/slide-(\\d+)/) || [])[1] || '1', 10) - 1;
    if (n !== i) show(n);
  }});
  fit();
  show(i);
{extra_js}</script>
</body>
</html>
"""

if __name__ == "__main__":
    for source, target in DECKS:
        build(source, target)
