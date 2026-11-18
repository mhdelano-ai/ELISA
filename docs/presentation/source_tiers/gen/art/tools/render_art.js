// Render one illustration with its labels the way a slide will show it.
//   node render_art.js <dir> <name> [background]
// reads <dir>/<name>.svg and, if present, <dir>/<name>.labels.json; writes <dir>/<name>.preview.png
// labels: [{ "key", "text", "x", "y", "w", "align": "left|center|right", "size": 24, "weight": 400 }]
// (x, y = top-left corner of the label box in the svg's own pixel coordinates; w = box width)
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
(async () => {
  const [dir, name, bg = '#F6F3EC'] = process.argv.slice(2);
  const svg = fs.readFileSync(path.join(dir, name + '.svg'), 'utf8');
  const m = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
  if (!m) throw new Error('no viewBox="0 0 W H"');
  const W = Math.round(+m[1]), H = Math.round(+m[2]);
  const lp = path.join(dir, name + '.labels.json');
  const labels = fs.existsSync(lp) ? JSON.parse(fs.readFileSync(lp, 'utf8')) : [];
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
  const ps = labels.map((l) => `<p style="position:absolute;left:${l.x}px;top:${l.y}px;width:${l.w}px;` +
    `text-align:${l.align || 'left'};font-size:${l.size || 24}px;font-weight:${l.weight || 400};` +
    `line-height:1.25;margin:0;color:${l.color || '#14213D'}">${esc(l.text)}</p>`).join('\n');
  const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    body{margin:0;background:${bg};font-family:'IBM Plex Sans',Arial,sans-serif}
    #host{position:relative;width:${W}px;height:${H}px;margin:24px;outline:1px dashed #9AA5B8}
    #host svg{position:absolute;left:0;top:0}</style></head><body><div id="host">${svg}${ps}</div></body></html>`;
  const browser = await chromium.launch({ args: ['--host-resolver-rules=MAP * ^NOTFOUND'] });
  const ctx = await browser.newContext({ javaScriptEnabled: false, viewport: { width: W + 48, height: H + 48 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.setContent(html);
  await page.screenshot({ path: path.join(dir, name + '.preview.png') });
  await browser.close();
  const bytes = Buffer.byteLength(svg, 'utf8');
  const bad = [/<text[\s>]/, /<style[\s>]/, /<script[\s>]/, /<foreignObject/, /<image[\s>]/, /href="http/, /<!--/].filter((r) => r.test(svg));
  console.log(JSON.stringify({ name, W, H, bytes, labels: labels.length, forbidden: bad.map(String) }));
})();
