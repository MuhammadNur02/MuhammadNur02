"""Generate assets/generated/banner.svg - the profile hero banner."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from theme import *  # noqa
from text2path import text_group

W, H = 900, 420
GY = 35  # vertical shift applied to the whole gate group, to clear the kanji above it

kanji_g, kanji_w = text_group("武士道", KANJI_FILE, 110, W / 2, 112, WASHI,
                               ttc_index=0, anchor="middle")
name_g, name_w = text_group("MUHAMMAD NURRAHMAN JULIANSYAH", FONT_DIR + "BigShoulders-Bold.ttf",
                             34, W / 2, 293 + GY, WASHI, anchor="middle", tracking=0.01)
role_g, role_w = text_group("WEB  &  SAAS  DEVELOPER", FONT_DIR + "Tektur-Medium.ttf",
                             13, W / 2, 318 + GY, GOLD, anchor="middle", tracking=0.14)

svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Muhammad Nurrahman Juliansyah - Web and SaaS Developer">
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{INK_2}"/>
    <stop offset="55%" stop-color="{INK}"/>
    <stop offset="100%" stop-color="{INK}"/>
  </linearGradient>
  <linearGradient id="gate" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{TORII}"/>
    <stop offset="100%" stop-color="{TORII_DK}"/>
  </linearGradient>
  <radialGradient id="moon" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="{MOON}" stop-opacity="0.55"/>
    <stop offset="60%" stop-color="{MOON}" stop-opacity="0.12"/>
    <stop offset="100%" stop-color="{MOON}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="lantern-glow" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="{EMBER}" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="{EMBER}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{INK}" stop-opacity="0"/>
    <stop offset="100%" stop-color="{INK_2}" stop-opacity="0.9"/>
  </linearGradient>
  <filter id="ink-bleed" x="-20%" y="-20%" width="140%" height="140%">
    <feTurbulence type="fractalNoise" baseFrequency="0.011 0.04" numOctaves="2" seed="7" result="noise"/>
    <feDisplacementMap in="SourceGraphic" in2="noise" scale="7" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="soft-blur"><feGaussianBlur stdDeviation="5"/></filter>
  <style>
    .lantern-l {{ animation: flicker-l 4.2s ease-in-out infinite; transform-origin: 335px 267px; }}
    .lantern-r {{ animation: flicker-r 3.6s ease-in-out infinite; transform-origin: 565px 267px; }}
    @keyframes flicker-l {{ 0%,100% {{ opacity:.75 }} 45% {{ opacity:1 }} 60% {{ opacity:.6 }} }}
    @keyframes flicker-r {{ 0%,100% {{ opacity:.85 }} 35% {{ opacity:.55 }} 70% {{ opacity:1 }} }}
    @media (prefers-reduced-motion: reduce) {{ .lantern-l, .lantern-r {{ animation: none; opacity: .85; }} }}
  </style>
</defs>

<rect width="{W}" height="{H}" fill="url(#sky)"/>
<circle cx="676" cy="66" r="90" fill="url(#moon)"/>
<circle cx="676" cy="66" r="22" fill="{MOON}" opacity="0.5"/>

<g filter="url(#ink-bleed)">{kanji_g}</g>

<!-- torii gate -->
<g fill="url(#gate)">
  <rect x="298" y="147" width="22" height="240" rx="2"/>
  <rect x="580" y="147" width="22" height="240" rx="2"/>
  <rect x="285" y="231" width="330" height="16" rx="2"/>
  <rect x="440" y="183" width="20" height="48" rx="2"/>
  <path d="M246,155 C246,131 300,119 450,119 C600,119 654,131 654,155
           C654,163 646,167 636,165 C610,145 520,135 450,135
           C380,135 290,145 264,165 C254,167 246,163 246,155 Z"/>
  <path d="M270,175 L630,175 C634,175 636,179 636,185 L636,193 C636,198 634,201 630,201
           L270,201 C266,201 264,198 264,193 L264,185 C264,179 266,175 270,175 Z"/>
</g>
<g fill="{INK}">
  <rect x="240" y="147" width="30" height="12" rx="3"/>
  <rect x="630" y="147" width="30" height="12" rx="3"/>
</g>

<circle class="lantern-l" cx="335" cy="267" r="19" fill="url(#lantern-glow)" filter="url(#soft-blur)"/>
<rect class="lantern-l" x="325" y="251" width="20" height="26" rx="9" fill="{EMBER}"/>
<circle class="lantern-r" cx="565" cy="267" r="19" fill="url(#lantern-glow)" filter="url(#soft-blur)"/>
<rect class="lantern-r" x="555" y="251" width="20" height="26" rx="9" fill="{EMBER}"/>

<rect x="0" y="335" width="{W}" height="85" fill="url(#ground)"/>
{name_g}
{role_g}
</svg>'''

out = os.path.join(os.path.dirname(__file__), "..", "assets", "generated", "banner.svg")
with open(out, "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote", out, len(svg), "bytes; kanji_w", kanji_w, "name_w", name_w)
