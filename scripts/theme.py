"""Shared design tokens - Samurai / Torii Gate theme for MuhammadNur02's GitHub profile.
Every generator script imports from here so all SVGs stay visually consistent.
"""

# -- Color palette --------------------------------------------------------
INK       = "#140F0C"   # base background - warm sumi-ink black (not a flat #0B0B0B)
INK_2     = "#1E1712"   # raised panel background
INK_3     = "#2A2019"   # card / stroke-on-dark background
TORII     = "#C9432A"   # shuiro (朱色) - real torii-gate lacquer vermilion
TORII_DK  = "#8F2E1C"   # shadowed vermilion (gradients, gate-in-shade)
EMBER     = "#E8A33D"   # lantern / ember glow, warm gold-orange
EMBER_DIM = "#8A5A22"   # low / unlit ember state
GOLD      = "#B8935A"   # muted antique brass - fine linework, kanji accents
WASHI     = "#EDE3D3"   # warm paper off-white - primary text on dark
MIST      = "#8C8176"   # desaturated secondary text
MOON      = "#7A8FA6"   # cool moonlight - used once, in the hero only

# -- Type -------------------------------------------------------------------
import os as _os
FONT_DIR   = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "fonts") + _os.sep
F_NAME     = "BigShoulders-Bold"        # identity: name, section headers
F_HUD      = "Tektur-Medium"            # game-HUD numbers / labels / badges
F_KANJI    = "Noto Serif CJK JP Black"  # exact fontconfig family name (verified via fc-list)
KANJI_FILE = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Black.ttc"

CANVAS_W = 900  # standard GitHub profile README content width
