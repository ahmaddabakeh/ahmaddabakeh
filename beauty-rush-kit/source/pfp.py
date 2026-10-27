"""Three richer TikTok profile pictures around the unchanged Bold wordmark. Writes into the current directory.

Usage: python3 pfp.py <path-to-Montserrat-variable.ttf>
"""
import sys

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import OverlapMode, instantiateVariableFont

from carve import text_path, to_d

PINK, INK, BURG = "#F5B8C9", "#141012", "#6B1F35"
D = 1080


def doc(name, body, title):
    with open(name, "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {D} {D}" width="{D}" height="{D}" role="img" '
                f'aria-labelledby="t"><title id="t">{title}</title>{body}</svg>\n')


def sparkle(cx, cy, r, k=0.12):
    q = r * k
    return (f"M{cx} {cy - r}Q{cx + q} {cy - q} {cx + r} {cy}Q{cx + q} {cy + q} {cx} {cy + r}"
            f"Q{cx - q} {cy + q} {cx - r} {cy}Q{cx - q} {cy - q} {cx} {cy - r}Z")


def line(font, text, cap, baseline, track=40):
    return text_path(font, [text], cap, [baseline], track=track, cx=D / 2)


def fit(font, text, width, track=40):
    """Cap height that makes `text` exactly `width` px wide."""
    p = text_path(font, [text], 100, [0], track=track, cx=0)
    return 100 * width / (p.bounds[2] - p.bounds[0])


if __name__ == "__main__":
    font = instantiateVariableFont(TTFont(sys.argv[1]), {"wght": 800}, overlap=OverlapMode.REMOVE)
    W = 760  # shared line width, keeps every corner inside the circular crop

    # A — Split: BEAUTY in black on pink, RUSH in pink on a black band. Two-tone and graphic.
    cb, cr = fit(font, "BEAUTY", W), fit(font, "RUSH", W)
    beauty = line(font, "BEAUTY", cb, 500)
    rush = line(font, "RUSH", cr, 600 + cr + 10)
    doc("pfp-a-split.svg",
        f'<rect width="{D}" height="{D}" fill="{PINK}"/><rect y="560" width="{D}" height="{D - 560}" fill="{INK}"/>'
        f'<path fill="{INK}" d="{to_d(beauty)}"/><path fill="{PINK}" d="{to_d(rush)}"/>',
        "Beauty Rush profile picture, split")

    # B — Live Ring: a bold black ring like TikTok's LIVE ring, with two glints by the name.
    W2 = 640
    cb2, cr2 = fit(font, "BEAUTY", W2), fit(font, "RUSH", W2)
    gap = 26
    total = cb2 + gap + cr2
    top = (D - total) / 2
    name = line(font, "BEAUTY", cb2, top + cb2)
    name.addPath(line(font, "RUSH", cr2, top + cb2 + gap + cr2))
    ring = (f"M{D / 2} 40A500 500 0 1 1 {D / 2 - 0.01} 40Z M{D / 2} 86A454 454 0 1 0 {D / 2 + 0.01} 86Z")
    glints = sparkle(830, top - 78, 44) + " " + sparkle(250, top + total + 78, 30)
    doc("pfp-b-ring.svg",
        f'<rect width="{D}" height="{D}" fill="{PINK}"/><path fill="{INK}" fill-rule="evenodd" d="{ring}"/>'
        f'<path fill="{INK}" d="{to_d(name)} {glints}"/>',
        "Beauty Rush profile picture, live ring")

    # C — Monogram pattern: tone-on-tone BR pattern (like printed packaging), name on a black pill.
    tile = text_path(font, ["BR"], 80, [0], track=20, cx=0)
    tw = tile.bounds[2] - tile.bounds[0]
    step_x, step_y = tw + 90, 150
    pattern = []
    for row in range(8):
        off = 0 if row % 2 == 0 else step_x / 2
        for col in range(-1, 8):
            t = tile.transform(1, 0, 0, 1, 40 + col * step_x + off, 110 + row * step_y)
            x0, y0, x1, y1 = t.bounds
            if x0 >= 0 and y0 >= 0 and x1 <= D and y1 <= D:  # whole tiles only, nothing spills off the canvas
                pattern.append(to_d(t))
    W3 = 600
    cb3, cr3 = fit(font, "BEAUTY", W3), fit(font, "RUSH", W3)
    total3 = cb3 + 24 + cr3
    top3 = (D - total3) / 2
    name3 = line(font, "BEAUTY", cb3, top3 + cb3)
    name3.addPath(line(font, "RUSH", cr3, top3 + cb3 + 24 + cr3))
    pill = f'<rect x="{(D - W3) / 2 - 70}" y="{top3 - 60}" width="{W3 + 140}" height="{total3 + 120}" rx="60" fill="{INK}"/>'
    doc("pfp-c-pattern.svg",
        f'<rect width="{D}" height="{D}" fill="{PINK}"/><path fill="#EFA3B8" d="{" ".join(pattern)}"/>'
        f'{pill}<path fill="{PINK}" d="{to_d(name3)}"/>',
        "Beauty Rush profile picture, monogram pattern")
