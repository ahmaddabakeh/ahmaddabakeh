"""Eye-catching TikTok profile pictures: big name, strong contrast, one bold move each.

Usage: python3 pfp2.py <path-to-Montserrat-variable.ttf>
"""
import math
import sys

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import OverlapMode, instantiateVariableFont

from carve import text_path, to_d
from pfp import BURG, D, INK, PINK, doc, fit, line, sparkle

HOT = "#FF3D8B"  # brighter "Rush Pink" accent for the feed


def stacked(font, width, gap=22):
    """BEAUTY over RUSH at one shared width, centred on the canvas; returns (path, height)."""
    cb, cr = fit(font, "BEAUTY", width), fit(font, "RUSH", width)
    total = cb + gap + cr
    top = (D - total) / 2
    p = line(font, "BEAUTY", cb, top + cb)
    p.addPath(line(font, "RUSH", cr, top + cb + gap + cr))
    return p, total


def max_width(font, circle_frac):
    """Largest shared width whose stacked block still fits inside a circle of D*circle_frac."""
    w = 400
    while True:
        p, _ = stacked(font, w + 10)
        x0, y0, x1, y1 = p.bounds
        if math.hypot(x1 - x0, y1 - y0) > D * circle_frac:
            return w
        w += 10


if __name__ == "__main__":
    font = instantiateVariableFont(TTFont(sys.argv[1]), {"wght": 800}, overlap=OverlapMode.REMOVE)

    # A — Pop: hot pink, huge black name filling the circle.
    name, _ = stacked(font, max_width(font, 0.94))
    doc("pfp2-a-pop.svg", f'<rect width="{D}" height="{D}" fill="{HOT}"/><path fill="{INK}" d="{to_d(name)}"/>',
        "Beauty Rush profile picture, pop")

    # B — Night: black, huge candy-pink name, one glint. Black stands out in a feed of photos.
    w = max_width(font, 0.88)
    name, total = stacked(font, w)
    x1, y0 = name.bounds[2], name.bounds[1]
    doc("pfp2-b-night.svg",
        f'<rect width="{D}" height="{D}" fill="{INK}"/><path fill="{PINK}" d="{to_d(name)} {sparkle(x1 - 8, y0 - 62, 40)}"/>',
        "Beauty Rush profile picture, night")

    # C — Sticker: the name on a tilted black label over pink, like a price sticker slapped on a live drop.
    w = max_width(font, 0.74)
    name, total = stacked(font, w)
    x0, y0, x1, y1 = name.bounds
    pad = 56
    label = (f'<rect x="{x0 - pad:.1f}" y="{y0 - pad:.1f}" width="{x1 - x0 + 2 * pad:.1f}" '
             f'height="{y1 - y0 + 2 * pad:.1f}" rx="36" fill="{INK}"/>')
    doc("pfp2-c-sticker.svg",
        f'<rect width="{D}" height="{D}" fill="{PINK}"/><g transform="rotate(-8 {D / 2} {D / 2})">{label}'
        f'<path fill="{PINK}" d="{to_d(name)}"/></g>',
        "Beauty Rush profile picture, sticker")
