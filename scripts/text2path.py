"""Convert text to outlined SVG <path> glyphs at generation time.

Every asset in this project ships as a self-contained SVG with zero external
font dependencies: headline / label / stat-number text is baked to vector
paths here, once, when the script runs. Handles both a single TTF and a
TTC collection (for selecting one face out of Noto Serif CJK).
"""
from fontTools.ttLib import TTFont, TTCollection
from fontTools.pens.svgPathPen import SVGPathPen

_cache = {}


def _load_face(font_path, ttc_index=0):
    key = (font_path, ttc_index)
    if key in _cache:
        return _cache[key]
    if font_path.endswith(".ttc"):
        face = TTCollection(font_path).fonts[ttc_index]
    else:
        face = TTFont(font_path)
    _cache[key] = face
    return face


def text_group(text, font_path, size, x, y, fill, ttc_index=0,
                tracking=0.0, anchor="start", extra_attrs=""):
    """Return an SVG <g> string rendering `text` as outlined paths.

    size: font size in px (CSS-equivalent). x, y: SVG baseline position.
    tracking: extra letter-spacing in font-size units (e.g. 0.02 = 2% of size).
    anchor: 'start' | 'middle' | 'end' - like text-anchor, applied via a
    pre-computed x shift since paths have no native anchor behaviour.
    """
    face = _load_face(font_path, ttc_index)
    upm = face["head"].unitsPerEm
    scale = size / upm
    cmap = face.getBestCmap()
    gs = face.getGlyphSet()
    hmtx = face["hmtx"]

    parts = []
    cum = 0.0
    total_adv = 0.0
    for ch in text:
        if ch == " ":
            adv = upm * 0.30
            cum += adv + tracking * upm
            total_adv = cum
            continue
        gname = cmap.get(ord(ch))
        if gname is None:
            continue
        pen = SVGPathPen(gs)
        gs[gname].draw(pen)
        d = pen.getCommands()
        adv = hmtx[gname][0]
        if d:
            parts.append(f'<path transform="translate({cum:.1f},0)" d="{d}"/>')
        cum += adv + tracking * upm
        total_adv = cum

    width_px = total_adv * scale
    shift = 0.0
    if anchor == "middle":
        shift = -width_px / 2
    elif anchor == "end":
        shift = -width_px

    g = (f'<g transform="translate({x + shift:.1f},{y:.1f}) scale({scale:.6f},{-scale:.6f})" '
         f'fill="{fill}" {extra_attrs}>' + "".join(parts) + "</g>")
    return g, width_px


if __name__ == "__main__":
    # quick self-test
    g, w = text_group("Muhammad", "/mnt/skills/examples/canvas-design/canvas-fonts/BigShoulders-Bold.ttf",
                       64, 0, 0, "#111")
    print("width", w, "len(g)", len(g))
