#!/usr/bin/env python3
"""Render the 23 November 2026 world-news front page as one 1024x1024 PNG.

Fresh newspaper design for this edition: warm paper, black masthead with a
red top bar, one big lead panel, a 2x3 grid of story cards with small drawn
pictograms, a ticker strip and an honest reporting-window footer.

Deterministic: no network, no randomness, no timestamps. Same news.json in
-> same entry.png bytes out.
"""

import json
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (179, 39, 30)
NAVY = (20, 33, 61)
WHITE = (255, 255, 255)
GREY = (90, 86, 78)
LIGHT_GREY = (210, 205, 192)
CARD = (255, 255, 255)

ACCENTS = {
    "ship": (31, 58, 95),
    "building": (179, 39, 30),
    "badge": (120, 72, 20),
    "flame": (196, 90, 17),
    "capitol": (43, 84, 122),
    "robot": (46, 110, 92),
}


def font(name, size):
    return ImageFont.truetype(
        os.path.join("/usr/share/fonts/truetype/dejavu", name), size
    )


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_icon(draw, kind, x, y, s, color):
    """Small pictogram drawn with plain PIL shapes, size s x s at (x, y)."""
    if kind == "ship":
        # hull
        draw.polygon([(x, y + s * 0.62), (x + s, y + s * 0.62),
                      (x + s * 0.82, y + s * 0.86), (x + s * 0.18, y + s * 0.86)],
                     fill=color)
        # mast + sail
        draw.rectangle([x + s * 0.48, y + s * 0.18, x + s * 0.52, y + s * 0.62],
                       fill=color)
        draw.polygon([(x + s * 0.54, y + s * 0.2), (x + s * 0.54, y + s * 0.56),
                      (x + s * 0.86, y + s * 0.56)], fill=color)
        # smoke
        for cx, cy, r in ((0.30, 0.14, 0.09), (0.22, 0.24, 0.07), (0.38, 0.06, 0.06)):
            draw.ellipse([x + s * (cx - r), y + s * (cy - r),
                          x + s * (cx + r), y + s * (cy + r)], fill=GREY)
        # waves
        for i, wx in enumerate((0.05, 0.38, 0.71)):
            draw.arc([x + s * wx, y + s * 0.9, x + s * (wx + 0.26), y + s * 1.02],
                     0, 180, fill=color, width=3)
    elif kind == "building":
        draw.rectangle([x + s * 0.14, y + s * 0.22, x + s * 0.86, y + s * 0.9],
                       outline=color, width=4)
        for row in range(3):
            for col in range(3):
                wx = x + s * (0.26 + col * 0.22)
                wy = y + s * (0.32 + row * 0.2)
                draw.rectangle([wx, wy, wx + s * 0.1, wy + s * 0.1], fill=color)
        # crack
        draw.line([(x + s * 0.55, y + s * 0.2), (x + s * 0.45, y + s * 0.42),
                   (x + s * 0.58, y + s * 0.6), (x + s * 0.48, y + s * 0.82)],
                  fill=RED, width=4)
    elif kind == "badge":
        # shield
        draw.polygon([(x + s * 0.5, y + s * 0.08), (x + s * 0.88, y + s * 0.22),
                      (x + s * 0.88, y + s * 0.58), (x + s * 0.5, y + s * 0.92),
                      (x + s * 0.12, y + s * 0.58), (x + s * 0.12, y + s * 0.22)],
                     fill=color)
        # star
        cx, cy, r = x + s * 0.5, y + s * 0.46, s * 0.2
        pts = []
        import math
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.45
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        draw.polygon(pts, fill=WHITE)
    elif kind == "flame":
        draw.polygon([(x + s * 0.5, y + s * 0.06), (x + s * 0.72, y + s * 0.38),
                      (x + s * 0.88, y + s * 0.34), (x + s * 0.82, y + s * 0.68),
                      (x + s * 0.62, y + s * 0.92), (x + s * 0.38, y + s * 0.92),
                      (x + s * 0.18, y + s * 0.68), (x + s * 0.14, y + s * 0.4),
                      (x + s * 0.32, y + s * 0.42)], fill=color)
        draw.ellipse([x + s * 0.36, y + s * 0.58, x + s * 0.64, y + s * 0.86],
                     fill=(255, 205, 90))
    elif kind == "capitol":
        # dome
        draw.pieslice([x + s * 0.3, y + s * 0.1, x + s * 0.7, y + s * 0.55],
                      180, 360, fill=color)
        draw.rectangle([x + s * 0.48, y + s * 0.02, x + s * 0.52, y + s * 0.12],
                       fill=color)
        draw.rectangle([x + s * 0.2, y + s * 0.55, x + s * 0.8, y + s * 0.62],
                       fill=color)
        for i in range(4):
            cx = x + s * (0.26 + i * 0.16)
            draw.rectangle([cx, y + s * 0.62, cx + s * 0.07, y + s * 0.88],
                           fill=color)
        draw.rectangle([x + s * 0.16, y + s * 0.88, x + s * 0.84, y + s * 0.94],
                       fill=color)
    elif kind == "robot":
        draw.rectangle([x + s * 0.48, y + s * 0.04, x + s * 0.52, y + s * 0.2],
                       fill=color)
        draw.ellipse([x + s * 0.42, y, x + s * 0.58, y + s * 0.12], fill=RED)
        draw.rounded_rectangle([x + s * 0.16, y + s * 0.2, x + s * 0.84, y + s * 0.66],
                               radius=8, fill=color)
        draw.ellipse([x + s * 0.28, y + s * 0.32, x + s * 0.42, y + s * 0.46],
                     fill=WHITE)
        draw.ellipse([x + s * 0.58, y + s * 0.32, x + s * 0.72, y + s * 0.46],
                     fill=WHITE)
        draw.rectangle([x + s * 0.36, y + s * 0.54, x + s * 0.64, y + s * 0.58],
                       fill=WHITE)
        draw.rectangle([x + s * 0.24, y + s * 0.72, x + s * 0.76, y + s * 0.9],
                       outline=color, width=3)


def draw_globe(draw, cx, cy, r):
    """Lead pictogram: a cracked globe with smoke, for the COP31 story."""
    # smoke puffs
    for sx, sy, sr in ((-52, -78, 16), (-28, -92, 12), (-72, -64, 10)):
        draw.ellipse([cx + sx - sr, cy + sy - sr, cx + sx + sr, cy + sy + sr],
                     fill=(150, 146, 136))
    # globe
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(43, 84, 122),
                 outline=INK, width=3)
    # land blobs
    draw.ellipse([cx - r * 0.7, cy - r * 0.55, cx - r * 0.05, cy + r * 0.05],
                 fill=(96, 150, 90))
    draw.ellipse([cx + r * 0.1, cy + r * 0.15, cx + r * 0.65, cy + r * 0.6],
                 fill=(96, 150, 90))
    draw.ellipse([cx + r * 0.25, cy - r * 0.7, cx + r * 0.7, cy - r * 0.3],
                 fill=(96, 150, 90))
    # crack
    draw.line([(cx - r * 0.5, cy - r * 0.9), (cx - r * 0.2, cy - r * 0.3),
               (cx - r * 0.45, cy + r * 0.1), (cx - r * 0.1, cy + r * 0.55),
               (cx - r * 0.3, cy + r * 0.9)], fill=RED, width=5)
    # NO DEAL stamp
    stamp = Image.new("RGBA", (210, 64), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([3, 3, 206, 60], outline=RED, width=5)
    sd.text((105, 32), "NO DEAL", font=SANS_B(34), fill=RED, anchor="mm")
    stamp = stamp.rotate(10, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (cx + r - 150, cy + r - 60), stamp)


def render(news, out_path):
    global img
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # frame + red top bar
    draw.rectangle([0, 0, W - 1, 13], fill=RED)
    draw.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)

    # ---- masthead ----
    draw.text((W // 2, 52), "THE WORLD TODAY", font=SERIF_B(62),
              fill=INK, anchor="mt")
    draw.line([(70, 122), (W - 70, 122)], fill=INK, width=2)
    draw.text((W // 2, 132), "MONDAY  •  23 NOVEMBER 2026  •  ONE DAY, ONE IMAGE",
              font=SANS_B(19), fill=RED, anchor="mt")

    # ---- lead panel ----
    lx, ly, lw, lh = 28, 168, 968, 196
    draw.rectangle([lx, ly, lx + lw, ly + lh], fill=CARD, outline=INK, width=2)
    draw.rectangle([lx, ly, lx + 10, ly + lh], fill=RED)
    lead = news["lead"]
    tx = lx + 28
    draw.text((tx, ly + 16), lead["tag"] + "  —  " + lead["place"],
              font=SANS_B(17), fill=RED)
    head_lines = wrap(draw, lead["headline"], SERIF_B(32), 600)
    y = draw_lines(draw, head_lines, tx, ly + 42, SERIF_B(32), INK, 40)
    body_lines = wrap(draw, lead["body"], SANS(19), 600)
    draw_lines(draw, body_lines, tx, y + 8, SANS(19), (40, 40, 40), 25)
    draw_globe(draw, lx + lw - 130, ly + lh // 2 + 6, 72)

    # ---- grid 2 x 3 ----
    gx, gy = 28, 380
    cw, ch, gap = 478, 160, 12
    for i, story in enumerate(news["stories"]):
        col, row = i % 2, i // 2
        x = gx + col * (cw + gap)
        y0 = gy + row * (ch + gap)
        accent = ACCENTS[story["icon"]]
        draw.rectangle([x, y0, x + cw, y0 + ch], fill=CARD, outline=INK, width=2)
        draw.rectangle([x, y0, x + cw, y0 + 7], fill=accent)
        draw.text((x + 16, y0 + 18), story["tag"] + "  —  " + story["place"],
                  font=SANS_B(14), fill=accent)
        hl = wrap(draw, story["headline"], SANS_B(21), cw - 104)
        yy = draw_lines(draw, hl[:2], x + 16, y0 + 44, SANS_B(21), INK, 25)
        bl = wrap(draw, story["body"], SANS(15), cw - 104)
        draw_lines(draw, bl[:3], x + 16, yy + 4, SANS(15), (60, 60, 60), 18)
        draw_icon(draw, story["icon"], x + cw - 78, y0 + ch - 74, 58, accent)

    # ---- ticker ----
    ty = 892
    draw.rectangle([28, ty, 996, ty + 44], fill=NAVY)
    ticker = "  •  ".join(news["ticker"])
    draw.text((512, ty + 22), "ALSO TODAY  —  " + ticker, font=SANS_B(14),
              fill=WHITE, anchor="mm")

    # ---- footer ----
    fy = 948
    draw.line([(70, fy), (W - 70, fy)], fill=LIGHT_GREY, width=2)
    draw.text((W // 2, fy + 12),
              news["window"] + "  ·  Sources: Reuters, AP, BBC, AFP, NPR",
              font=SANS(15), fill=GREY, anchor="mt")
    draw.text((W // 2, fy + 36), "THE WORLD TODAY — 23 NOVEMBER 2026",
              font=SANS_B(14), fill=INK, anchor="mt")

    img.save(out_path, format="PNG", optimize=True)


def main():
    with open(os.path.join(HERE, "news.json"), encoding="utf-8") as f:
        news = json.load(f)
    render(news, os.path.join(HERE, "entry.png"))


if __name__ == "__main__":
    main()
