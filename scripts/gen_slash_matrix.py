"""Generate assets/generated/slash-matrix.svg - when in the day the ronin strikes.

Reads data/activity_matrix.json (grid[day][daypart], level 0..4). Each cell is
a katana slash: longer, brighter and thicker with more activity.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from theme import *  # noqa
from text2path import text_group

ROOT = os.path.join(os.path.dirname(__file__), "..")
D = json.load(open(os.path.join(ROOT, "data", "activity_matrix.json")))
DAYS, PARTS, GRID = D["days"], D["dayparts"], D["grid"]

W, H = 284, 210
SCALE = ["#2A2019", "#5C3A1A", EMBER_DIM, EMBER, "#FFD37A"]
GX, GY, CW, RH = 58, 52, 29, 22
TEK = FONT_DIR + "Tektur-Medium.ttf"

title_g, _ = text_group("Shadow Slash", FONT_DIR + "BigShoulders-Bold.ttf", 21, 20, 34, WASHI)

body = []
for r, part in enumerate(PARTS):
    y = GY + r * RH
    g, _ = text_group(part, TEK, 9, 20, y + 14, MIST)
    body.append(g)
    for c in range(len(DAYS)):
        lv = GRID[c][r]
        cx, cy = GX + c * CW + CW / 2, y + RH / 2
        if lv == 0:
            body.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="1.6" fill="{INK_3}"/>')
            continue
        half = 3 + lv * 1.9          # slash half-length grows with level
        sw = 1.2 + lv * 0.35
        x1, y1, x2, y2 = cx - half, cy + half * 0.55, cx + half, cy - half * 0.55
        if lv >= 3:
            body.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                        f'stroke="{SCALE[lv]}" stroke-width="{sw + 3:.1f}" stroke-linecap="round" opacity="0.22"/>')
        body.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'stroke="{SCALE[lv]}" stroke-width="{sw:.1f}" stroke-linecap="round"/>')

for c, day in enumerate(DAYS):
    g, _ = text_group(day, TEK, 9, GX + c * CW + CW / 2, GY + len(PARTS) * RH + 12, MIST, anchor="middle")
    body.append(g)

svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Shadow Slash Matrix - jam paling aktif ngoding">
<defs>
  <linearGradient id="ss-bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{INK_2}"/><stop offset="100%" stop-color="{INK}"/>
  </linearGradient>
</defs>
<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="14" fill="url(#ss-bg)" stroke="{INK_3}" stroke-width="1.5"/>
{title_g}
{"".join(body)}
</svg>'''

out = os.path.join(ROOT, "assets", "generated", "slash-matrix.svg")
open(out, "w", encoding="utf-8").write(svg)
print("wrote", out, len(svg))
