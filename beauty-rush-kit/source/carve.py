"""Heart Bubble with letters carved out (true boolean, one clean path). Writes into the current directory.

Usage: python3 carve.py <path-to-Montserrat-variable.ttf>
"""
import sys

import pathops
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import OverlapMode, instantiateVariableFont

from build import INK, c_path, svg

HEART_SCALE = 1.1  # scaled about (128,128) so the name has room


def heart():
    p = pathops.Path()
    s = HEART_SCALE
    parse_path(c_path, TransformPen(p.getPen(), (s, 0, 0, s, 128 - 128 * s, 118 - 128 * s)))
    return p


def text_path(font, lines, cap_px, baselines, track=40, cx=128):
    """Outline each line of text centred on cx; returns a pathops.Path."""
    gs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
    k = cap_px / font["OS/2"].sCapHeight
    out = pathops.Path()
    for line, base in zip(lines, baselines):
        width = sum(hmtx[cmap[ord(ch)]][0] + track for ch in line) - track
        x = cx / k - width / 2
        for ch in line:
            g = cmap[ord(ch)]
            gs[g].draw(TransformPen(out.getPen(glyphSet=gs), (k, 0, 0, -k, x * k, base)))
            x += hmtx[g][0] + track
    return out


def carve(font, lines, cap_px, baselines, track=40):
    return pathops.op(heart(), text_path(font, lines, cap_px, baselines, track), pathops.PathOp.DIFFERENCE)


def to_d(path):
    pen = SVGPathPen(None, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
    path.draw(pen)
    return pen.getCommands()


if __name__ == "__main__":
    font = instantiateVariableFont(TTFont(sys.argv[1]), {"wght": 800}, overlap=OverlapMode.REMOVE)
    named = carve(font, ["BEAUTY", "RUSH"], 24, [107, 141])
    svg("c1-carved-name.svg", f'<path fill="{INK}" d="{to_d(named)}"/>', title="Beauty Rush heart with carved name")
    mono = carve(font, ["BR"], 58, [134], track=10)
    svg("c2-carved-br.svg", f'<path fill="{INK}" d="{to_d(mono)}"/>', title="Beauty Rush heart with carved BR")
    plain = heart()
    svg("c3-plain.svg", f'<path fill="{INK}" d="{to_d(plain)}"/>', title="Beauty Rush heart small-size cut")
