"""Assemble the slide sources into one self-contained HTML file that opens in any browser.

Usage:  python docs/presentation/build.py
Reads   docs/presentation/source/deck.json and source/slides/<id>.html
Writes  docs/presentation/in_silico_summary.html
"""
import json
import pathlib

here = pathlib.Path(__file__).parent
deck = json.loads((here / "source" / "deck.json").read_text(encoding="utf-8"))
slides = "\n".join(
    (here / "source" / "slides" / f"{sid}.html").read_text(encoding="utf-8").strip()
    for sid in deck["order"]
)
fonts = "\n".join(
    f'<link rel="stylesheet" href="{face["href"]}">' for face in deck["faces"].values() if "href" in face
)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{deck["title"]}</title>
{fonts}
<style>
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
</script>
</body>
</html>
"""
(here / "in_silico_summary.html").write_text(page, encoding="utf-8")
print(f"wrote {here / 'in_silico_summary.html'} ({len(deck['order'])} slides)")
