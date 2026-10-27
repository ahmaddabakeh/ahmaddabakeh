"""Labeled catalog of every Beauty Rush logo variation, as PNG pages plus one PDF.

Usage: python3 catalog.py <scratchpad-dir> <out-dir>
"""
import io
import os
import sys

import cairosvg
from PIL import Image, ImageDraw, ImageFont

W_PAGE, COLS, TILE_W, TILE_H, LABEL_H, PAD = 1600, 4, 360, 300, 64, 24
F_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
CARDS3 = [(60, 536), (563, 1037), (1066, 1540)]  # card columns on the 1600-wide comparison boards


def svg_tile(path, bg="white"):
    png = cairosvg.svg2png(url=path, output_width=1200)
    im = Image.open(io.BytesIO(png)).convert("RGBA")
    im.thumbnail((TILE_W - 20, TILE_H - 20))
    tile = Image.new("RGB", (TILE_W, TILE_H), bg)
    tile.paste(im, ((TILE_W - im.width) // 2, (TILE_H - im.height) // 2), im)
    return tile


def crop_tile(path, box):
    im = Image.open(path).convert("RGB").crop(box)
    im.thumbnail((TILE_W, TILE_H))
    tile = Image.new("RGB", (TILE_W, TILE_H), "white")
    tile.paste(im, ((TILE_W - im.width) // 2, (TILE_H - im.height) // 2))
    return tile


def board(path, names, y0=168, y1=640):
    return [(n, lambda i=i: crop_tile(path, (CARDS3[i][0], y0, CARDS3[i][1], y1))) for i, n in enumerate(names)]


def svgs(base, items):
    return [(n, lambda f=f: svg_tile(os.path.join(base, f))) for n, f in items]


def rounds(S):
    sk, kit = os.path.join(S, "skill"), os.path.join(S, "beauty-rush-kit")
    grid = []
    for r, (k, kn) in enumerate([("sparkle", "Sparkle"), ("bow", "Bow"), ("lipstick", "Lipstick"), ("heart", "Finger heart")]):
        for c, (st, sn) in enumerate([("outline", "Outline"), ("tint", "Tint"), ("solid", "Solid"), ("cutout", "Cut-out")]):
            grid.append((f"{'ABCD'[r]}{c + 1} {kn} · {sn}", f"pfp11-{k}-{st}.svg"))
    sym4 = [("sparkle", "Sparkle"), ("bow", "Bow"), ("lipstick", "Lipstick"), ("heart", "Finger heart")]
    return [
        ("R1", "First concepts (greyscale)", board(os.path.join(S, "br", "concepts.png"),
                                                 ["Glint B", "Swept R", "br. Live Dot"], 150, 640)),
        ("R2", "Pink & classic", board(os.path.join(S, "br2", "concepts.png"), ["Maison", "Signature", "Seal"])),
        ("R3", "Clean wordmarks (Rhode / Huda feel)", board(os.path.join(S, "br3", "concepts.png"), ["Milk", "Bold", "Rosé"])),
        ("R4", "Rosé + icon", board(os.path.join(S, "br4", "icons.png"), ["Glint", "Live Bubble", "Bow"], 168, 600)),
        ("R5", "Bold + icon", board(os.path.join(S, "br5", "icons.png"), ["Glint", "Live Bubble", "Bow"], 168, 600)),
        ("R6", "Bold + cuter bubble", board(os.path.join(S, "br6", "bubbles.png"), ["Heart Pop", "Puffy", "Bubble Pop"], 168, 600)),
        ("R7", "Bubble concepts (skill redo)", svgs(sk, [("B-Bubble", "a-lockup.svg"), ("Gloss Bubble", "b-lockup.svg"),
                                                         ("Heart Bubble", "c-lockup.svg")])),
        ("R8", "Heart Bubble with carved name", svgs(sk, [("Carved name", "c1-carved-name.svg"), ("Carved BR", "c2-carved-br.svg"),
                                                          ("Plain heart", "c3-plain.svg")])),
        ("R9", "Bold logo kit (current kit masters)", svgs(sk, [("Horizontal", "bold-horizontal.svg"), ("Stacked", "bold-stacked.svg"),
                                                                ("BR monogram", "bold-br.svg")])
         + svgs(os.path.join(kit, "logo"), [("BR app icon", "beauty-rush-br-app-icon.svg")])),
        ("R10", "Profile pictures: first set", svgs(os.path.join(kit, "social"), [("BR", "tiktok-profile.svg"),
                                                                                  ("Full name", "tiktok-profile-full-name.svg"),
                                                                                  ("Split", "tiktok-profile-split.svg")])
         + svgs(sk, [("Live Ring", "pfp-b-ring.svg"), ("Monogram Pattern", "pfp-c-pattern.svg")])),
        ("R11", "Eye-catching", svgs(sk, [("Pop", "pfp2-a-pop.svg"), ("Night", "pfp2-b-night.svg"), ("Sticker", "pfp2-c-sticker.svg")])),
        ("R12", "More life", svgs(sk, [("Script Rush", "pfp3-a-script.svg"), ("Die-cut Sticker", "pfp3-b-diecut.svg"),
                                       ("3D Pop", "pfp3-c-3d.svg")])),
        ("R13", "Script, refined", svgs(sk, [("Noir", "pfp4-a-noir.svg"), ("Blush", "pfp4-b-blush.svg"), ("Hot Pink", "pfp4-c-hot.svg")])),
        ("R14", "No script", svgs(sk, [("Editorial", "pfp5-a-editorial.svg"), ("Motion", "pfp5-b-motion.svg"),
                                       ("Maison", "pfp5-c-maison.svg")])),
        ("R15", "Motion + outlined symbol behind", svgs(sk, [("Sparkle", "pfp6-a-sparkle.svg"), ("Bow", "pfp6-b-bow.svg"),
                                                             ("Lipstick", "pfp6-c-lipstick.svg")])),
        ("R16", "BR with carved symbol", svgs(sk, [("Sparkle R", "pfp7-sparkle.svg"), ("Bow R", "pfp7-bow.svg"),
                                                   ("Lipstick R", "pfp7-lipstick.svg")])),
        ("R17", "Wordmark with carved R", svgs(sk, [("Sparkle R", "pfp8-sparkle.svg"), ("Bow R", "pfp8-bow.svg"),
                                                    ("Lipstick R", "pfp8-lipstick.svg")])),
        ("R18", "Symbol overlaps Y, overlap flips black", svgs(sk, [("Sparkle", "pfp9-sparkle.svg"), ("Bow", "pfp9-bow.svg"),
                                                                    ("Lipstick", "pfp9-lipstick.svg")])),
        ("R19", "Y grows into the symbol", svgs(sk, [("Sparkle", "pfp10-sparkle.svg"), ("Bow", "pfp10-bow.svg"),
                                                     ("Lipstick", "pfp10-lipstick.svg")])),
        ("R20", "Symbol in front of Y: 4 symbols x 4 styles", svgs(sk, grid)),
        ("R21", "Tint + cut-out", svgs(sk, [(n, f"pfp11-{k}-tintcut.svg") for k, n in sym4])),
        ("R22", "Tint + pink cut (1 light, 2 deep)",
         svgs(sk, [(f"{'ABCD'[i]}1 {n} · light", f"pfp11-{k}-tintpink.svg") for i, (k, n) in enumerate(sym4)]
              + [(f"{'ABCD'[i]}2 {n} · deep", f"pfp11-{k}-tintpink-deep.svg") for i, (k, n) in enumerate(sym4)])),
        ("R23", "Word in front, hot-pink symbol behind", svgs(sk, [(n, f"pfp11-{k}-behind.svg") for k, n in sym4])),
        ("R24", "Final mark v1 (sparkle partly behind the Y)",
         svgs(os.path.join(sk, "final-v1"), [("Dark", "tiktok-profile-sparkle-dark.svg"), ("Bright", "tiktok-profile-sparkle-bright.svg")])),
        ("R25", "Final mark v2 (all four sparkle points showing)",
         svgs(os.path.join(sk, "final-v2"), [("Dark", "tiktok-profile-sparkle-dark.svg"), ("Bright", "tiktok-profile-sparkle-bright.svg")])),
        ("R26", "Final mark v3 (sparkle's bottom-left corner wraps the Y)",
         svgs(os.path.join(sk, "final-v3"), [("Dark", "tiktok-profile-sparkle-dark.svg"), ("Bright", "tiktok-profile-sparkle-bright.svg")])),
        ("R27", "Final mark v4 (fuller sparkle, one clean outline through the overlap)",
         svgs(os.path.join(sk, "final-v4"), [("Dark", "tiktok-profile-sparkle-dark.svg"), ("Bright", "tiktok-profile-sparkle-bright.svg")])),
        ("R28", "Final mark v5 (sparkle and word outlines interlock) — current",
         svgs(os.path.join(kit, "social"), [("Dark", "tiktok-profile-sparkle-dark.svg"), ("Bright", "tiktok-profile-sparkle-bright.svg")])),
    ]


def code_for(rid, i, name):
    """Grid-style names already carry a code (A1, B2…); otherwise use letters A, B, C…"""
    head = name.split(" ")[0]
    if len(head) == 2 and head[0] in "ABCD" and head[1].isdigit():
        return f"{rid}-{head}", name[3:]
    return f"{rid}-{'ABCDEFGHIJ'[i]}", name


def render(S, out):
    os.makedirs(out, exist_ok=True)
    fb, fb_s, fr = ImageFont.truetype(F_B, 30), ImageFont.truetype(F_B, 20), ImageFont.truetype(F_R, 17)
    pages, page, y = [], None, 0
    max_h = 2200

    def new_page():
        nonlocal page, y
        if page is not None:
            pages.append(page.crop((0, 0, W_PAGE, y + PAD)))
        page, y = Image.new("RGB", (W_PAGE, max_h + 600), "#F7F7F4"), 40

    new_page()
    d = ImageDraw.Draw(page)
    d.text((40, y), "Beauty Rush — every logo variation", fill="#141012", font=ImageFont.truetype(F_B, 40))
    y += 60
    d.text((40, y), "Reply with the codes you like (for example R11-C, R20-A2).", fill="#6b6b6b", font=fr)
    y += 50
    for rid, title, items in rounds(S):
        rows = (len(items) + COLS - 1) // COLS
        need = 56 + rows * (TILE_H + LABEL_H + PAD)
        if y + need > max_h:
            new_page()
            d = ImageDraw.Draw(page)
        d.text((40, y), f"{rid} · {title}", fill="#141012", font=fb)
        y += 50
        for i, (name, make) in enumerate(items):
            r, c = divmod(i, COLS)
            x = 40 + c * (TILE_W + 22)
            ty = y + r * (TILE_H + LABEL_H + PAD)
            try:
                tile = make()
            except Exception as e:  # keep going if one source is missing
                tile = Image.new("RGB", (TILE_W, TILE_H), "#eee")
                ImageDraw.Draw(tile).text((10, 10), f"missing: {e}", fill="#900", font=fr)
            page.paste(tile, (x, ty))
            d.rectangle((x, ty, x + TILE_W - 1, ty + TILE_H - 1), outline="#e2e2dc")
            code, label = code_for(rid, i, name)
            d.text((x + 4, ty + TILE_H + 8), code, fill="#141012", font=fb_s)
            d.text((x + 4, ty + TILE_H + 34), label, fill="#555", font=fr)
        y += rows * (TILE_H + LABEL_H + PAD) + 10
    pages.append(page.crop((0, 0, W_PAGE, y + PAD)))
    paths = []
    for i, p in enumerate(pages, 1):
        f = os.path.join(out, f"beauty-rush-variations-{i}.png")
        p.save(f)
        paths.append(f)
    pages[0].save(os.path.join(out, "beauty-rush-variations.pdf"), save_all=True, append_images=pages[1:], resolution=150)
    print("\n".join(paths))


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
