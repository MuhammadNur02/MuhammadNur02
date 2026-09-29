"""Generate assets/generated/arsenal.svg - Digital Arsenal tech stack row.

Reads data/arsenal.json; edit that file to change the tools shown.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from theme import *  # noqa
from text2path import text_group

ROOT = os.path.join(os.path.dirname(__file__), "..")
TOOLS = json.load(open(os.path.join(ROOT, "data", "arsenal.json")))["tools"]

W, PAD, GAP = CANVAS_W, 20, 10
PER_ROW = 7
rows_n = -(-len(TOOLS) // PER_ROW)
TW = (W - 2 * PAD - GAP * (PER_ROW - 1)) / PER_ROW
TH = 92
H = 56 + rows_n * (TH + GAP) + 10
TEK = FONT_DIR + "Tektur-Medium.ttf"

title_g, _ = text_group("Digital Arsenal", FONT_DIR + "BigShoulders-Bold.ttf", 21, PAD, 36, WASHI)

tiles = []
for i, t in enumerate(TOOLS):
    x = PAD + (i % PER_ROW) * (TW + GAP)
    y = 56 + (i // PER_ROW) * (TH + GAP)
    cx = x + TW / 2
    ab, _ = text_group(t["abbr"], TEK, 20, cx, y + 44, t["color"], anchor="middle")
    nm, _ = text_group(t["name"], TEK, 10.5, cx, y + 76, WASHI, anchor="middle")
    tiles.append(
        f'<rect x="{x:.1f}" y="{y}" width="{TW:.1f}" height="{TH}" rx="10" fill="{INK_2}" stroke="{INK_3}" stroke-width="1.5"/>'
        f'<rect x="{x + 10:.1f}" y="{y}" width="{TW - 20:.1f}" height="2" rx="1" fill="{t["color"]}" opacity="0.8"/>'
        f'<circle cx="{cx:.1f}" cy="{y + 38}" r="20" fill="none" stroke="{t["color"]}" stroke-width="1.2" opacity="0.35"/>'
        + ab + nm)

svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Digital Arsenal - tech stack">
<defs>
  <linearGradient id="da-bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{INK_2}"/><stop offset="100%" stop-color="{INK}"/>
  </linearGradient>
</defs>
<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="14" fill="url(#da-bg)" stroke="{INK_3}" stroke-width="1.5"/>
{title_g}
{"".join(tiles)}
</svg>'''

out = os.path.join(ROOT, "assets", "generated", "arsenal.svg")
open(out, "w", encoding="utf-8").write(svg)
print("wrote", out, len(svg))
