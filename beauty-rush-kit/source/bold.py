"""Beauty Rush Bold: outlined wordmark (horizontal + stacked) and BR monogram. Writes into the current directory.

Usage: python3 bold.py <path-to-Montserrat-variable.ttf>
"""
import math
import sys

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import OverlapMode, instantiateVariableFont

from build import INK, svg
from carve import text_path, to_d


def bounds_shift(path, w, h):
    """Translate path so its bounds are centred on a w×h canvas."""
    x0, y0, x1, y1 = path.bounds
    return path.transform(1, 0, 0, 1, (w - (x1 - x0)) / 2 - x0, (h - (y1 - y0)) / 2 - y0)


if __name__ == "__main__":
    font = instantiateVariableFont(TTFont(sys.argv[1]), {"wght": 800}, overlap=OverlapMode.REMOVE)

    # Horizontal wordmark: cap height 96, tracking 40 units, cropped to 256 height with even padding.
    h = text_path(font, ["BEAUTY RUSH"], 96, [0], track=40, cx=0)
    x0, _, x1, _ = h.bounds
    w = math.ceil(x1 - x0 + 64)
    svg("bold-horizontal.svg", f'<path fill="{INK}" d="{to_d(bounds_shift(h, w, 256))}"/>', w=w,
        title="Beauty Rush logo")

    # Stacked wordmark: BEAUTY over RUSH; RUSH is set larger so both lines share one width.
    top = text_path(font, ["BEAUTY"], 64, [0], track=40, cx=0)
    bw = top.bounds[2] - top.bounds[0]
    probe = text_path(font, ["RUSH"], 64, [0], track=40, cx=0)
    rush_cap = 64 * bw / (probe.bounds[2] - probe.bounds[0])
    bot = text_path(font, ["RUSH"], rush_cap, [24 + rush_cap], track=40, cx=0)
    top.addPath(bot)
    sw = math.ceil(bw + 64)
    svg("bold-stacked.svg", f'<path fill="{INK}" d="{to_d(bounds_shift(top, sw, 256))}"/>', w=sw,
        title="Beauty Rush stacked logo")

    # BR monogram for the profile picture and small sizes.
    br = text_path(font, ["BR"], 104, [0], track=20, cx=0)
    svg("bold-br.svg", f'<path fill="{INK}" d="{to_d(bounds_shift(br, 256, 256))}"/>',
        title="Beauty Rush BR monogram")
