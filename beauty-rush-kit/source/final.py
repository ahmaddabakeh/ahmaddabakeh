"""Final Beauty Rush mark: italic BEAUTY RUSH in front, hot-pink sparkle behind the Y, one keyline.

Everything is solid filled geometry (no strokes): the keyline and gaps are real outlines made with
path booleans, so the files print and cut cleanly. Spacing is built from one unit (the keyline gap).

Usage: python3 final.py <fonts-dir> <out-dir>
Writes, for each of dark / bright:
  beauty-rush-sparkle-<v>.svg            transparent-background master (no backdrop)
  tiktok-profile-sparkle-<v>.svg         1080 x 1080 profile picture with backdrop, sized for the circle crop
"""
import math
import os
import sys

import pathops

from carve import text_path, to_d
from pfp import sparkle
from pfp3 import centred
from pfp5 import var, width

PINK, HOT, INK, WHITE = "#F5B8C9", "#FF3D8B", "#141012", "#FFFFFF"
VARIANTS = {
    # name: (backdrop, letters, symbol, keyline)
    "dark": (INK, PINK, HOT, PINK),
    "bright": (PINK, INK, HOT, INK),
}

U = 10                 # spacing unit: the black gap between shapes and the keyline
GAP, LINE = U, U * 0.6  # keyline = gap, then a line 0.6 of the gap
C_GAP, C_LINE = U * 0.7, U * 0.35  # finer outline where the word crosses the sparkle
LINE_GAP = 3 * U       # space between BEAUTY and RUSH: room for both gaps, so the keyline wraps as one shape


def stroke_outline(p, w):
    """Outline of path p grown by w/2 on every side (round joins), as a filled path."""
    s = pathops.Path(p)
    s.stroke(w, pathops.LineCap.ROUND_CAP, pathops.LineJoin.ROUND_JOIN, 4)
    s.convertConicsToQuads()
    return pathops.op(p, s, pathops.PathOp.UNION)


def _band(p, w):
    s = pathops.Path(p)
    s.stroke(w, pathops.LineCap.ROUND_CAP, pathops.LineJoin.ROUND_JOIN, 4)
    s.convertConicsToQuads()
    return pathops.op(s, pathops.Path(), pathops.PathOp.UNION)


def dilate(p, d):
    return pathops.op(p, _band(p, 2 * d), pathops.PathOp.UNION)


def erode(p, d):
    return pathops.op(p, _band(p, 2 * d), pathops.PathOp.DIFFERENCE)


def closing(p, c):
    """Fill notches and slivers narrower than 2c, rounding inside corners."""
    return erode(dilate(p, c), c)


def opening(p, o):
    """Remove bits thinner than 2o, rounding outside corners."""
    return dilate(erode(p, o), o)


def name_path(font, target_w):
    """BEAUTY over RUSH at one optical width; RUSH shifted left to follow the italic slant."""
    track = 14
    top = text_path(font, ["BEAUTY"], 100, [0], track=track, cx=0)
    bot = text_path(font, ["RUSH"], 100, [0], track=track, cx=0)
    k = target_w / width(top)
    s = width(top) / width(bot)
    top = text_path(font, ["BEAUTY"], 100 * k, [0], track=track, cx=0)
    bot = text_path(font, ["RUSH"], 100 * k * s, [0], track=track, cx=0)
    ht, hb = top.bounds[3] - top.bounds[1], bot.bounds[3] - bot.bounds[1]
    slant = math.tan(math.radians(9.5))  # Montserrat Italic slant: keep the left edges on one italic line
    top = centred(top, 0, ht / 2)
    bot = centred(bot, -slant * (ht / 2 + LINE_GAP + hb / 2), ht + LINE_GAP + hb / 2)
    out = pathops.Path()
    out.addPath(top)
    out.addPath(bot)
    return pathops.op(out, pathops.Path(), pathops.PathOp.UNION), ht


def sparkle_path(cx, cy, r):
    """Big sparkle + a small one on the 45-degree diagonal up-right, in the empty quadrant between two points."""
    p = pathops.Path()
    from fontTools.svgLib.path import parse_path
    small_r = r * 0.3
    off = r * 0.78  # along the diagonal: clear of the big sparkle's curves, with room for the keyline
    tension = 0.17  # fuller, softer points than a needle-thin star
    parse_path(sparkle(cx, cy, r, tension) + " " + sparkle(cx + off, cy - off, small_r, tension), p.getPen())
    return pathops.op(p, pathops.Path(), pathops.PathOp.UNION)


def build(font):
    name, cap_top = name_path(font, 760)
    x0, y0, x1, y1 = name.bounds
    r = cap_top * 1.02                      # big sparkle radius ~ BEAUTY's cap height
    # The sparkle's bottom-left corner (the curve between its left and bottom points) wraps the Y's
    # top-right corner: the word sits in front, all four points stay visible around it.
    sym = sparkle_path(x1 + r * 0.06, y0 - r * 0.30, r)
    # Outer silhouette, with its inside corners (where the sparkle meets the word) rounded off.
    raw = pathops.op(name, sym, pathops.PathOp.UNION)
    union = closing(raw, 1.4 * U)
    # Only around the overlap (the Y's top and the sparkle's corner) bridge the notches fully, so the
    # outer line runs in one clean sweep there; everywhere else the outline still hugs the letters.
    overlap = pathops.op(name, dilate(sym, U), pathops.PathOp.INTERSECTION)
    zone = dilate(overlap, 5 * U)
    bridged = pathops.op(closing(raw, 3.5 * U), zone, pathops.PathOp.INTERSECTION)
    union = pathops.op(union, bridged, pathops.PathOp.UNION)
    inner = dilate(union, GAP)
    outer = dilate(union, GAP + LINE)
    outer_ring = pathops.op(outer, inner, pathops.PathOp.DIFFERENCE)
    # Inside the overlap: one thin, clean line between the word and the sparkle.
    word_gap = dilate(name, C_GAP)
    word_line = dilate(name, C_GAP + C_LINE)
    inner_line = pathops.op(pathops.op(word_line, word_gap, pathops.PathOp.DIFFERENCE),
                            dilate(sym, C_GAP + C_LINE + 1),
                            pathops.PathOp.INTERSECTION)  # wherever the sparkle meets the word
    # Join the lines: fill any sliver between the inner line and the outer ring so they meet as one.
    ring = closing(pathops.op(outer_ring, inner_line, pathops.PathOp.UNION), 0.55 * U)
    ring = pathops.op(pathops.op(ring, word_gap, pathops.PathOp.DIFFERENCE), outer, pathops.PathOp.INTERSECTION)
    # The sparkle fills right up to the line (its own points stay sharp).
    sym_visible = pathops.op(sym, word_line, pathops.PathOp.DIFFERENCE)
    return name, sym_visible, ring, outer


def place(paths, outer, size, frac):
    """Scale and centre so the outer silhouette's diagonal is `frac` of `size` (fits the circle crop)."""
    x0, y0, x1, y1 = outer.bounds
    s = size * frac / math.hypot(x1 - x0, y1 - y0)
    tx = size / 2 - (x0 + x1) / 2 * s
    ty = size / 2 - (y0 + y1) / 2 * s - size * 0.01  # optical centre: a touch above geometric centre
    return [p.transform(s, 0, 0, s, tx, ty) for p in paths]


def svg(path, w, h, body, title):
    with open(path, "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" '
                f'role="img" aria-labelledby="t"><title id="t">{title}</title>{body}</svg>\n')


if __name__ == "__main__":
    fonts, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    font = var(os.path.join(fonts, "Montserrat-Italic[wght].ttf"), wght=900)
    name, sym, ring, outer = build(font)
    for v, (bg, fg, sc, kl) in VARIANTS.items():
        art = lambda n, s, r: (f'<path fill="{kl}" d="{to_d(r)}"/><path fill="{sc}" d="{to_d(s)}"/>'
                               f'<path fill="{fg}" d="{to_d(n)}"/>')
        # Transparent master, cropped to the outer silhouette with 1 unit of padding per 10% of height.
        x0, y0, x1, y1 = outer.bounds
        pad = (y1 - y0) * 0.08
        W, H = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
        n, s, r = (p.transform(1, 0, 0, 1, pad - x0, pad - y0) for p in (name, sym, ring))
        svg(os.path.join(out, f"beauty-rush-sparkle-{v}.svg"), round(W), round(H), art(n, s, r),
            f"Beauty Rush logo, {v}")
        # Profile picture with backdrop, sized for TikTok's circle.
        n, s, r = place([name, sym, ring], outer, 1080, 0.9)
        svg(os.path.join(out, f"tiktok-profile-sparkle-{v}.svg"), 1080, 1080,
            f'<rect width="1080" height="1080" fill="{bg}"/>' + art(n, s, r), f"Beauty Rush profile picture, {v}")
