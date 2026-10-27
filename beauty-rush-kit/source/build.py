"""Build Beauty Rush concept SVGs (black masters) into the current directory.

Usage: python3 build.py <path-to-Montserrat-variable.ttf>
"""
import math
import sys

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

INK = "#141012"


def svg(name, body, w=256, title="Beauty Rush logo"):
    with open(name, "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 256" width="{w}" height="256" '
                f'role="img" aria-labelledby="title"><title id="title">{title}</title>{body}</svg>\n')


def circle_intersections(c1, r1, c2, r2):
    (x1, y1), (x2, y2) = c1, c2
    d = math.dist(c1, c2)
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(r1 * r1 - a * a)
    xm, ym = x1 + a * (x2 - x1) / d, y1 + a * (y2 - y1) / d
    return [(round(xm + s * h * (y2 - y1) / d, 2), round(ym - s * h * (x2 - x1) / d, 2)) for s in (1, -1)]


def polar(cx, cy, r, deg):
    t = math.radians(deg)
    return round(cx + r * math.cos(t), 2), round(cy + r * math.sin(t), 2)


# A — B-Bubble: B whose bottom-left corner pulls out into a chat tail.
# Stem x56-100; upper bowl circle (130,82) r46; lower bowl circle (138,166) r54; corner radius 20.
up_c, up_r, lo_c, lo_r = (130, 82), 46, (138, 166), 54
waist = max(circle_intersections(up_c, up_r, lo_c, lo_r), key=lambda p: p[0])
a_path = (f"M76 36H130A46 46 0 0 1 {waist[0]} {waist[1]}A54 54 0 0 1 138 220H98Q72 222 34 246Q56 228 56 190V56A20 20 0 0 1 76 36Z "
          "M100 62H120A21 21 0 0 1 120 104H100Z M100 132H130A31 31 0 0 1 130 194H100Z")
a = f'<path transform="translate(12 -11)" fill="{INK}" fill-rule="evenodd" d="{a_path}"/>'

# B — Gloss Bubble: round bubble (128,118) r96 with a curled tail; a gloss streak + dot cut out at upper left.
cx, cy, r = 128, 118, 96
t1, t2 = polar(cx, cy, r, 112), polar(cx, cy, r, 148)
bubble = (f"M{t1[0]} {t1[1]}A{r} {r} 0 1 0 {t2[0]} {t2[1]}"
          f"C{t2[0] - 4} {t2[1] + 30} 34 230 22 238C58 240 84 228 {t1[0]} {t1[1]}Z")
ro, ri, s0, s1 = 74, 50, 194, 236  # gloss streak: ring segment with round caps
p0o, p1o, p1i, p0i = polar(cx, cy, ro, s0), polar(cx, cy, ro, s1), polar(cx, cy, ri, s1), polar(cx, cy, ri, s0)
cap = (ro - ri) / 2
streak = (f"M{p0o[0]} {p0o[1]}A{ro} {ro} 0 0 1 {p1o[0]} {p1o[1]}A{cap} {cap} 0 0 1 {p1i[0]} {p1i[1]}"
          f"A{ri} {ri} 0 0 0 {p0i[0]} {p0i[1]}A{cap} {cap} 0 0 1 {p0o[0]} {p0o[1]}Z")
dot_c = polar(cx, cy, 62, 258)
dot = f"M{dot_c[0] - 12} {dot_c[1]}A12 12 0 1 0 {dot_c[0] + 12} {dot_c[1]}A12 12 0 1 0 {dot_c[0] - 12} {dot_c[1]}Z"
b = f'<path transform="translate(5 0)" fill="{INK}" fill-rule="evenodd" d="{bubble} {streak} {dot}"/>'

# C — Heart Bubble: heart from two r54 lobes; the point swings left and down into a chat tail.
c_path = ("M128 72C112 40 76 34 54 52C28 74 32 112 58 140C78 162 100 180 112 192"
          "C104 210 88 226 66 234C100 236 124 222 136 204C150 190 176 166 198 140"
          "C224 112 228 74 202 52C180 34 144 40 128 72Z")
c = f'<path transform="translate(0 -10)" fill="{INK}" d="{c_path}"/>'


def wordmark(font_path, text="BEAUTY RUSH", wght=800, track=40, height=256, cap_px=64, x0=0, baseline=160):
    """Outline `text` from a variable font at `wght`; returns (svg path, advance width in px)."""
    font = instantiateVariableFont(TTFont(font_path), {"wght": wght})
    gs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
    cap = font["OS/2"].sCapHeight
    k = cap_px / cap
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
    x = 0
    for ch in text:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, x0 + x * k, baseline)))
        x += hmtx[g][0] + track
    return pen.getCommands(), (x - track) * k


if __name__ == "__main__":
    font_path = sys.argv[1]
    marks = {"a": ("B-Bubble", a), "b": ("Gloss Bubble", b), "c": ("Heart Bubble", c)}
    for key, (name, body) in marks.items():
        svg(f"{key}-symbol.svg", body, title=f"Beauty Rush {name} symbol")
    wm, wm_w = wordmark(font_path, x0=0, baseline=160)
    svg("wordmark.svg", f'<path fill="{INK}" d="{wm}"/>', w=math.ceil(wm_w), title="Beauty Rush wordmark")
    # Horizontal lockups: symbol at 256 height, gap 40, wordmark cap height 64 centred on the symbol.
    for key, (name, body) in marks.items():
        wm, wm_w = wordmark(font_path, x0=256 + 24, baseline=128 + 32)
        svg(f"{key}-lockup.svg", f"<g id=\"symbol\">{body}</g><path id=\"wordmark\" fill=\"{INK}\" d=\"{wm}\"/>",
            w=math.ceil(256 + 24 + wm_w + 8), title=f"Beauty Rush {name} horizontal logo")
