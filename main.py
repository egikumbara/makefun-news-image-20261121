#!/usr/bin/env python3
"""News image for Saturday 21 November 2026.

Draws a one-page newspaper front page summing up six real stories
reported on 21 November 2026, as a single 1024x1024 PNG.
Pure standard library only: hand-rolled PNG writer and bitmap font.
Deterministic: no clock, no randomness, no network.
"""
import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (163, 22, 33)
BLUE = (29, 78, 137)
GOLD = (176, 132, 34)
GREY = (90, 88, 80)
LIGHT = (232, 226, 210)
WHITE = (255, 255, 255)
SKY = (178, 205, 228)
GREEN = (46, 110, 62)
ORANGE = (214, 110, 30)

# ---------------------------------------------------------------- font ----
# 5x7 bitmap glyphs, '#' = ink pixel. Uppercase text only.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    '"': ("01010", "01010", "01010", "00000", "00000", "00000", "00000"),
    '*': ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
}


def text_width(text, scale):
    return len(text) * 6 * scale - scale


def draw_text(px, x, y, text, scale, color):
    """Draw uppercase text; unknown chars become spaces."""
    cx = x
    for ch in text.upper():
        glyph = FONT.get(ch, FONT[' '])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == '1':
                    for dy in range(scale):
                        for dx in range(scale):
                            set_px(px, cx + col * scale + dx,
                                   y + row * scale + dy, color)
        cx += 6 * scale
    return cx


def wrap_text(text, max_chars):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= max_chars:
            cur += " " + w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_para(px, x, y, text, scale, color, max_chars, leading):
    lines = wrap_text(text, max_chars)
    for i, line in enumerate(lines):
        draw_text(px, x, y + i * (7 * scale + leading), line, scale, color)
    return y + len(lines) * (7 * scale + leading)


def centered(px, y, text, scale, color, cx=512):
    w = text_width(text, scale)
    draw_text(px, cx - w // 2, y, text, scale, color)


# ---------------------------------------------------------------- canvas --
def new_canvas():
    return bytearray(PAPER * W * H)


def set_px(px, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        px[i], px[i + 1], px[i + 2] = color


def fill_rect(px, x, y, w, h, color):
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    for yy in range(y0, y1):
        base = yy * W * 3
        for xx in range(x0, x1):
            i = base + xx * 3
            px[i], px[i + 1], px[i + 2] = color


def rect_border(px, x, y, w, h, color, t=2):
    fill_rect(px, x, y, w, t, color)
    fill_rect(px, x, y + h - t, w, t, color)
    fill_rect(px, x, y, t, h, color)
    fill_rect(px, x + w - t, y, t, h, color)


def hline(px, x, y, w, color, t=2):
    fill_rect(px, x, y, w, t, color)


def fill_circle(px, cx, cy, r, color):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                set_px(px, xx, yy, color)


def fill_triangle(px, pts, color):
    (x0, y0), (x1, y1), (x2, y2) = pts
    ymin, ymax = min(y0, y1, y2), max(y0, y1, y2)
    for yy in range(ymin, ymax + 1):
        xs = []
        for (ax, ay), (bx, by) in (((x0, y0), (x1, y1)),
                                   ((x1, y1), (x2, y2)),
                                   ((x2, y2), (x0, y0))):
            if ay == by:
                continue
            if min(ay, by) <= yy < max(ay, by) or yy == ymax and yy in (ay, by):
                t = (yy - ay) / (by - ay)
                xs.append(ax + t * (bx - ax))
        if len(xs) >= 2:
            for xx in range(int(min(xs)), int(max(xs)) + 1):
                set_px(px, xx, yy, color)


def star(px, cx, cy, r, color):
    # 8-point burst: four triangles crossing at the centre.
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        tip = (cx + int(r * math.cos(a)), cy + int(r * math.sin(a)))
        a2 = math.radians(ang + 22)
        a3 = math.radians(ang - 22)
        p2 = (cx + int(r * 0.28 * math.cos(a2)),
              cy + int(r * 0.28 * math.sin(a2)))
        p3 = (cx + int(r * 0.28 * math.cos(a3)),
              cy + int(r * 0.28 * math.sin(a3)))
        fill_triangle(px, [tip, p2, p3], color)


# ---------------------------------------------------------------- motifs --
def motif_strikes(px, x, y, w, h):
    fill_rect(px, x, y, w, h, (24, 32, 54))
    fill_circle(px, x + w - 40, y + 34, 22, (240, 214, 130))
    for i, (sx, sy, r) in enumerate([(50, 70, 26), (120, 45, 18), (180, 85, 22)]):
        star(px, x + sx, y + sy, r, (240, 170, 40) if i % 2 == 0 else (220, 60, 40))
        fill_circle(px, x + sx, y + sy, 6, WHITE)
    # ground line + skyline
    fill_rect(px, x, y + h - 26, w, 26, (10, 14, 26))
    for bx, bw, bh in [(10, 34, 34), (58, 26, 48), (98, 40, 30), (150, 30, 44)]:
        fill_rect(px, x + bx, y + h - 26 - bh, bw, bh, (52, 60, 84))


def motif_court(px, x, y, w, h):
    fill_rect(px, x, y, w, h, (232, 226, 210))
    # scales of justice: pillar + beam + two pans
    fill_rect(px, x + w // 2 - 4, y + 30, 8, h - 60, INK)
    fill_rect(px, x + 28, y + 38, w - 56, 6, INK)
    fill_triangle(px, [(x + 34, y + 44), (x + 14, y + 78), (x + 54, y + 78)], GOLD)
    fill_triangle(px, [(x + w - 34, y + 44), (x + w - 54, y + 78),
                       (x + w - 14, y + 78)], GOLD)
    fill_rect(px, x + w // 2 - 30, y + h - 26, 60, 8, INK)
    fill_circle(px, x + w // 2, y + 26, 10, GOLD)


def motif_market(px, x, y, w, h):
    fill_rect(px, x, y, w, h, WHITE)
    fill_rect(px, x, y + h - 18, w, 2, GREY)
    bars = [38, 62, 48, 78, 55, 30, 18]
    bw = (w - 40) // len(bars)
    for i, v in enumerate(bars):
        bx = x + 20 + i * bw
        col = RED if i >= 4 else BLUE
        fill_rect(px, bx, y + h - 18 - v, bw - 6, v, col)
    # falling arrow: stepped diagonal line, high left to low right
    for i in range(w - 60):
        fill_rect(px, x + 22 + i, y + 12 + i // 12, 4, 4, RED)
    fill_triangle(px, [(x + w - 40, y + 36), (x + w - 40, y + 54),
                       (x + w - 22, y + 45)], RED)


def motif_handshake(px, x, y, w, h):
    fill_rect(px, x, y, w, h, SKY)
    fill_circle(px, x + 44, y + h // 2, 30, BLUE)
    fill_circle(px, x + w - 44, y + h // 2, 30, RED)
    fill_rect(px, x + 74, y + h // 2 - 6, w - 148, 12, GOLD)
    draw_text(px, x + 33, y + h // 2 - 7, "UK", 2, WHITE)
    draw_text(px, x + w - 55, y + h // 2 - 7, "EU", 2, WHITE)


def motif_climate(px, x, y, w, h):
    fill_rect(px, x, y, w, h, (214, 232, 214))
    fill_circle(px, x + w // 2, y + 30, 22, (240, 190, 60))
    fill_rect(px, x + 20, y + h - 26, w - 40, 12, (90, 150, 190))
    # small clouds under the hot sun
    fill_circle(px, x + 60, y + 58, 10, WHITE)
    fill_circle(px, x + w - 60, y + 58, 10, WHITE)


def motif_quake(px, x, y, w, h):
    fill_rect(px, x, y, w, h, (226, 214, 196))
    # cracked ground + mountain
    fill_triangle(px, [(x + 10, y + h - 8), (x + w // 2, y + 4),
                       (x + w - 10, y + h - 8)], (120, 110, 96))
    fill_triangle(px, [(x + w // 2 - 14, y + 22), (x + w // 2, y + 4),
                       (x + w // 2 + 14, y + 22)], WHITE)
    for i, cx in enumerate([30, 90, 150]):
        fill_rect(px, x + cx, y + h - 22, 4, 22, INK)
        fill_rect(px, x + cx + 4, y + h - 12, 26, 4, INK)


# ---------------------------------------------------------------- layout --
def kicker(px, x, y, label, color=RED):
    draw_text(px, x, y, label, 2, color)
    return y + 20


def story_block(px, x, y, w, h, tag, headline, body, motif):
    rect_border(px, x, y, w, h, INK, 2)
    fill_rect(px, x, y, w, 26, INK)
    draw_text(px, x + 10, y + 6, tag, 2, WHITE)
    motif(px, x + 10, y + 36, w - 20, 80)
    hy = y + 126
    hy = draw_para(px, x + 10, hy, headline, 2, INK, (w - 20) // 12, 4)
    draw_para(px, x + 10, hy + 6, body, 1, (50, 48, 44), (w - 20) // 6, 3)


def main():
    px = new_canvas()
    # outer frame
    rect_border(px, 8, 8, W - 16, H - 16, INK, 4)
    hline(px, 24, 22, W - 48, INK, 2)

    # masthead
    centered(px, 34, "THE WORLD TODAY", 8, INK)
    centered(px, 104, "ONE DAY  -  ONE PAGE  -  THE NEWS THAT MATTERED", 2, GREY)
    hline(px, 24, 132, W - 48, INK, 3)
    # date line - the day this page sums up
    fill_rect(px, 24, 142, W - 48, 44, RED)
    centered(px, 152, "SATURDAY 21 NOVEMBER 2026", 4, WHITE)
    hline(px, 24, 194, W - 48, INK, 3)

    # ---- lead story: Russia / Poland
    lx, ly, lw, lh = 24, 204, W - 48, 200
    rect_border(px, lx, ly, lw, lh, INK, 3)
    fill_rect(px, lx, ly, lw, 30, INK)
    draw_text(px, lx + 12, ly + 8, "LEAD STORY  -  WAR IN EUROPE", 2, WHITE)
    motif_strikes(px, lx + 12, ly + 40, 300, 150)
    hx = lx + 330
    draw_para(px, hx, ly + 44,
              "RUSSIA HITS UKRAINE WITH 400 DRONES AND 110 MISSILES; TWO LAND IN POLAND",
              3, INK, 34, 6)
    draw_para(px, hx, ly + 138,
              "Strikes killed at least eight in Kyiv and hit bridges and rail stations. Poland said two missiles landed on its soil; PM Tusk called it a deliberate provocation.",
              2, (50, 48, 44), 55, 5)

    # ---- middle grid: 2 x 2
    gy = 414
    gw = (W - 48 - 16) // 2
    gh = 230
    story_block(px, 24, gy, gw, gh, "JUSTICE  -  THE HAGUE",
                "COURT FINDS MYANMAR GUILTY OF GENOCIDE AGAINST THE ROHINGYA",
                "The International Court of Justice ruled Myanmar responsible for genocide. Survivors welcomed the landmark judgment, though return home remains distant.",
                motif_court)
    story_block(px, 24 + gw + 16, gy, gw, gh, "MARKETS  -  NEW YORK",
                "AI SELL-OFF PUSHES S AND P 500 INTO CORRECTION",
                "US stocks fell 3.7% as AI and chip shares slid. The S and P 500 and the Dow both entered correction territory in a sharp Friday rout.",
                motif_market)
    gy2 = gy + gh + 10
    story_block(px, 24, gy2, gw, gh, "POLITICS  -  BRUSSELS",
                "UK AND EU SIGN BIGGEST POST-BREXIT DEALS YET",
                "Three agreements ease food trade, link carbon markets and open youth mobility. Leaders called it the biggest reset of ties since Brexit.",
                motif_handshake)
    story_block(px, 24 + gw + 16, gy2, gw, gh, "CLIMATE  -  ANTALYA",
                "COP31 TALKS RUN PAST DEADLINE OVER FOSSIL FUELS",
                "The UN climate summit in Antalya ran into overtime as nearly 200 nations failed to agree. Pacific states warned starkly over fossil fuels.",
                motif_climate)

    # ---- bottom story: Peru quake, full width
    by = gy2 + gh + 10
    bw = W - 48
    rect_border(px, 24, by, bw, 88, INK, 2)
    fill_rect(px, 24, by, bw, 26, BLUE)
    draw_text(px, 34, by + 6, "DISASTER  -  PERU", 2, WHITE)
    motif_quake(px, 34, by + 32, 170, 50)
    draw_para(px, 220, by + 36,
              "MAGNITUDE 6.8 QUAKE SHAKES PERU'S ANDES",
              2, INK, 60, 4)
    draw_para(px, 220, by + 60,
              "The strong quake sent residents of Lima onto the streets. No major casualties were reported in early accounts.",
              1, (50, 48, 44), 108, 3)

    # footer
    centered(px, 992, "SIX STORIES FROM SATURDAY 21 NOVEMBER 2026  -  REPORTED THAT DAY AROUND THE WORLD",
             1, GREY)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    write_png(px, path)


def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(px, path):
    raw = bytearray()
    for yy in range(H):
        raw.append(0)
        raw.extend(px[yy * W * 3:(yy + 1) * W * 3])
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    data = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
