import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from theme import *  # noqa
from text2path import text_group

ROOT = os.path.join(os.path.dirname(__file__), "..")
D = json.load(open(os.path.join(ROOT, "data", "languages.json")))
LANGS = D["languages"]

W, H = 284, 210
LANG_COLORS = [TORII, EMBER, GOLD, MOON, "#7A9E7E", MIST]

title_g, _ = text_group("Jutsu Share", FONT_DIR + "BigShoulders-Bold.ttf", 21, 20, 34, WASHI)

bar_x, bar_y, bar_w, bar_h = 20, 52, W - 40, 14
segs = []
cx = bar_x
for i, lang in enumerate(LANGS):
    w = bar_w * lang["pct"] / 100.0
    color = LANG_COLORS[i % len(LANG_COLORS)]
    segs.append(f'<rect x="{cx:.1f}" y="{bar_y}" width="{w:.1f}" height="{bar_h}" fill="{color}"/>')
    cx += w
bar_group = f'<g clip-path="url(#bar-clip)">{"".join(segs)}</g>'

rows = []
row_h = 20
col_x = [20, 156]
for i, lang in enumerate(LANGS):
    col = i // 3
    r = i % 3
    x = col_x[col]
    y = 100 + r * row_h
    color = LANG_COLORS[i % len(LANG_COLORS)]
    rows.append(f'<rect x="{x}" y="{y - 9}" width="9" height="9" rx="2" fill="{color}"/>')
    name_g, _ = text_group(lang["name"], FONT_DIR + "Tektur-Medium.ttf", 10.5, x + 14, y, WASHI)
    pct_g, _ = text_group(f'{lang["pct"]:.0f}%', FONT_DIR + "Tektur-Medium.ttf", 10.5, x + 118, y, MIST, anchor="end")
    rows.append(name_g)
    rows.append(pct_g)

svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Jutsu Share - bahasa yang paling sering dipakai">
<defs>
  <linearGradient id="js-bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{INK_2}"/><stop offset="100%" stop-color="{INK}"/>
  </linearGradient>
  <clipPath id="bar-clip"><rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="7"/></clipPath>
</defs>
<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="14" fill="url(#js-bg)" stroke="{INK_3}" stroke-width="1.5"/>
{title_g}
{bar_group}
{"".join(rows)}
</svg>'''

out = os.path.join(ROOT, "assets", "generated", "jutsu-share.svg")
open(out, "w", encoding="utf-8").write(svg)
print("wrote", out, len(svg))
