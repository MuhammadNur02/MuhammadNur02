import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from theme import *  # noqa
from text2path import text_group

ROOT = os.path.join(os.path.dirname(__file__), "..")
D = json.load(open(os.path.join(ROOT, "data", "contributions.json")))

W, H = 284, 210

rows = [
    (str(D["total_contributions"]), "Total Kontribusi", TORII),
    (f'{D["current_streak"]} hari', "Streak Berjalan", EMBER),
    (f'{D["longest_streak"]} hari', "Rekor Terpanjang", GOLD),
]

title_g, _ = text_group("Battle Stats", FONT_DIR + "BigShoulders-Bold.ttf", 21, 20, 34, WASHI)

row_h = 54
y0 = 68
body = []
for i, (num, label, accent) in enumerate(rows):
    y = y0 + i * row_h
    body.append(f'<rect x="20" y="{y - 20}" width="3" height="34" rx="1.5" fill="{accent}"/>')
    num_g, _ = text_group(num, FONT_DIR + "Tektur-Medium.ttf", 26, 34, y + 4, WASHI)
    lbl_g, _ = text_group(label, FONT_DIR + "Tektur-Medium.ttf", 10, 34, y + 20, MIST, tracking=0.02)
    body.append(num_g)
    body.append(lbl_g)
    if i < len(rows) - 1:
        body.append(f'<line x1="20" y1="{y + 30}" x2="{W - 20}" y2="{y + 30}" stroke="{INK_3}" stroke-width="1"/>')

svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Battle Stats">
<defs>
  <linearGradient id="bs-bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{INK_2}"/><stop offset="100%" stop-color="{INK}"/>
  </linearGradient>
</defs>
<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="14" fill="url(#bs-bg)" stroke="{INK_3}" stroke-width="1.5"/>
{title_g}
{"".join(body)}
</svg>'''

out = os.path.join(ROOT, "assets", "generated", "battle-stats.svg")
open(out, "w", encoding="utf-8").write(svg)
print("wrote", out, len(svg))
