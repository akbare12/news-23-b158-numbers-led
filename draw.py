#!/usr/bin/env python3
"""Render THE WORLD TODAY — Monday 23 November 2026 (31 stories).
Numbers-led front page: big number grid first, then masthead, heroes,
cards, map + ALSO, DATE CHECK, footer. Output: entry.png 1024x1024."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
INK = (18, 18, 18)
PAPER = (250, 248, 243)
NAVY = (13, 27, 62)
NAVY2 = (24, 48, 96)
GOLD = (201, 162, 39)
GOLD_DK = (176, 138, 20)
RED = (178, 34, 34)
RED_BG = (252, 235, 235)
GRAY = (110, 110, 108)
LGRAY = (232, 230, 225)
GREEN = (31, 122, 63)
TEAL = (14, 110, 110)

F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_w(draw, s, fnt):
    return draw.textlength(s, font=fnt)


# ---------------------------------------------------------------- data
NUMBERS = [
    ("-3.3%", "KOSPI"),
    ("5.3", "US-CHINA GAP"),
    ("11,762", "EBOLA CASES DRC"),
    ("10T WON", "SEOUL FUND"),
    ("2%", "BILLIONAIRE TAX"),
    ("$450M", "SKUBAL DEAL"),
    ("165", "MISSILES / WEEK"),
    ("12,000", "CLEARED MANCHESTER"),
    ("264 KG", "EXPLOSIVES SEIZED"),
    ("$107.3B", "ANTHROPIC IPO"),
]

HEROES = [
    dict(
        kicker="ASIA MARKETS",
        head="AI ROUT HITS ASIA",
        body="Kospi -3.3% closes 4,708.54, sheds 161 pts, intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
        src="REUTERS", chip="REPORTED",
    ),
    dict(
        kicker="AI SUMMIT",
        head="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
        body="Bridgetown summit, Barbados. 150 delegates back a risk framework; blueprint, not treaty.",
        src="AP", chip="REPORTED",
    ),
    dict(
        kicker="POWER INDEX",
        head="US LEAD OVER CHINA AT RECORD LOW",
        body="Asia Power Index 2026: US 78.9, China 73.6, gap 5.3 narrowest since 2018. India 3rd, 40.5.",
        src="BLOOMBERG", chip="REPORTED",
    ),
]

CARDS = [
    ("MARKETS", "Bessent demands Nvidia answers", "REUTERS", "REPORTED"),
    ("CYBER", "FBI probes NCIC police-database hack", "AP", "REPORTED"),
    ("MIDDLE EAST", "Trump: Iran strikes may resume in New Year", "REUTERS", "REPORTED"),
    ("MARKETS", "Nasdaq futures +3% in holiday week", "BLOOMBERG", "REPORTED"),
    ("SPORT", "Skubal $450M Mets deal, largest ever for a pitcher", "AP", "REPORTED"),
    ("OBITUARY", "Tom Jackson dies at 75", "AP", "REPORTED"),
    ("TECH", "States sue SpaceX over AI safety claims", "REUTERS", "REPORTED"),
    ("TECH", "Anthropic IPO $107.3B at $83 a share", "BLOOMBERG", "REPORTED"),
    ("EUROPE", "Poland: 3 Russian Kh-101 missiles crossed airspace", "WSJ", "CLAIM"),
    ("DEFENCE", "Intel warns of Russian nuclear satellite", "WSJ", "CLAIM"),
]

ALSO = [
    "Paris 100+ back 2% billionaire tax",
    "Manchester 12,000 cleared",
    "Zelenskyy: 165 Russian missiles in a week",
    "COP31: the day after Antalya pact rejected",
    "Israel unity talks resume",
    "Gaza: two killed in Israeli strike",
    "West Bank settler attacks",
    "Iran war: no deal in sight",
    "Lebanon seizes 264 kg explosives",
    "Bahrain: Iranian strike hits plant, 2 hurt",
    "Benghazi: UN demands port probe [CLAIM]",
    "Sudan: drones downed in Khartoum [CLAIM]",
    "DRC: fighting traps Ebola teams",
    "Bangladesh: Hasina jailed if she returns",
    "Seoul minister quits over AI exam chaos",
    "SK Telecom -7.3%",
    "China eases margin rules (cuts to 80%)",
    "Seoul readies 10T-won stabilisation fund",
]

# map pins: (label, x, y) — absolute image coords, all inside the map box
# x 24..486, y 768..888, spread so no two centres are closer than 22 px
PINS = [
    ("1 Seoul", 440, 815),
    ("2 Bridgetown", 175, 852),
    ("3 Beijing", 415, 795),
    ("4 Washington", 110, 805),
    ("5 New York", 140, 788),
    ("6 Paris", 258, 822),
    ("7 London", 240, 805),
    ("8 Manchester", 222, 790),
    ("9 Kyiv", 292, 798),
    ("10 Beirut", 348, 818),
    ("11 Gaza", 332, 842),
    ("12 Khartoum", 318, 866),
    ("13 Kinshasa", 288, 872),
]

LEFT_OUT = [
    "Democrats reach 258 (22 Nov)",
    "Sparta II fire (22 Nov)",
    "El Chapo Isidro captured (22 Nov)",
    "EU-Indonesia pact (21 Nov)",
    "Nigeria boat (21 Nov)",
    "ICJ Myanmar ruling (19 Nov)",
]
NOT_YET = [
    "Dymer search continues (14 missing)",
    "4 House races uncalled",
    "COP32 venue not set",
    "WHO evacuating trapped Ebola staff",
]


def draw_scene_kospi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # skyline: buildings with lit windows
    base = y + h
    heights = [62, 88, 54, 96, 70, 84, 48, 78]
    bw = w // len(heights)
    for i, bh in enumerate(heights):
        bx = x + i * bw + 2
        d.rectangle([bx, base - bh, bx + bw - 4, base], fill=(30, 52, 96))
        for wy in range(base - bh + 8, base - 6, 14):
            for wx in range(bx + 5, bx + bw - 9, 12):
                if (wx * 7 + wy * 3) % 5 < 2:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 120))
    # falling chart line, kept in the upper zone, clear of the big number
    pts = [(x + 14, y + 26), (x + 70, y + 38), (x + 130, y + 30),
           (x + 190, y + 48), (x + 250, y + 44), (x + w - 14, y + 62)]
    d.line(pts, fill=(255, 140, 40), width=4)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 140, 40))
    f_big = font(F_SANS_B, 34)
    d.text((x + 14, y + h - 52), "-3.3%", font=f_big, fill=(255, 255, 255))
    f_cap = font(F_SANS, 12)
    d.text((x + 14, y + h - 16), "KOSPI 4,708.54  -161 PTS",
           font=f_cap, fill=(200, 210, 235))


def draw_scene_guterres(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 42, 84))
    # globe kept right of the gold caption so the two never touch
    cx, cy, r = x + w // 2 + 34, y + 52, 36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 130, 190))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(140, 200, 240), width=2)
    d.arc([cx - r + 12, cy - r, cx + r - 12, cy + r], 90, 270,
          fill=(140, 200, 240), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(140, 200, 240), width=2)
    d.ellipse([cx - 26, cy - 18, cx - 8, cy + 2], fill=(74, 160, 90))
    d.ellipse([cx + 6, cy + 6, cx + 24, cy + 26], fill=(74, 160, 90))
    f_g = font(F_SANS_B, 15)
    d.text((x + 14, y + h - 46), "150 DELEGATES", font=f_g, fill=GOLD)
    d.text((x + 14, y + h - 26), "BRIDGETOWN, BARBADOS",
           font=font(F_SANS, 12), fill=(220, 225, 240))
    # small flags row along the bottom edge, clear of the gold text
    fx = x + w - 74
    for c in [(200, 40, 40), (40, 90, 200), (240, 200, 40), (40, 140, 80)]:
        d.rectangle([fx, y + h - 14, fx + 14, y + h - 4], fill=c)
        fx += 18


def draw_scene_bars(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 241, 232))
    d.text((x + 14, y + 8), "ASIA POWER INDEX 2026",
           font=font(F_SANS_B, 13), fill=INK)
    rows = [("US", 78.9, NAVY2), ("CHINA", 73.6, RED), ("INDIA", 40.5, GOLD)]
    ry = y + 28
    for name, val, col in rows:
        d.text((x + 14, ry), name, font=font(F_SANS_B, 11), fill=GRAY)
        bw = int((w - 110) * val / 80.0)
        d.rectangle([x + 14, ry + 14, x + 14 + bw, ry + 30], fill=col)
        lab = f"{val}"
        f_v = font(F_SANS_B, 13)
        d.text((x + 14 + bw + 6, ry + 15), lab, font=f_v, fill=INK)
        ry += 32


SCENES = [draw_scene_kospi, draw_scene_guterres, draw_scene_bars]


def chip(d, x, y, label, claim=False):
    f = font(F_SANS_B, 10)
    tw = text_w(d, label, f)
    w = tw + 10
    col = RED if claim else GREEN
    d.rounded_rectangle([x, y, x + w, y + 16], radius=8, fill=col)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 24
    # ---- number grid (first) -------------------------------------------
    d.text((MX, 10), "THE DAY IN NUMBERS", font=font(F_SANS_B, 12), fill=RED)
    cell_w, cell_h = 193, 44
    for i, (val, lab) in enumerate(NUMBERS):
        row, col = divmod(i, 5)
        cx = MX + col * (cell_w + 3)
        cy = 30 + row * (cell_h + 4)
        d.rectangle([cx, cy, cx + cell_w, cy + cell_h], fill=(255, 255, 255),
                    outline=LGRAY)
        d.text((cx + 10, cy + 4), val, font=font(F_SANS_B, 21), fill=NAVY)
        d.text((cx + 10, cy + 28), lab, font=font(F_SANS_B, 10), fill=GRAY)
    d.line([MX, 126, W - MX, 126], fill=INK, width=2)

    # ---- masthead -------------------------------------------------------
    d.text((W // 2, 136), "THE WORLD TODAY", font=font(F_SERIF_B, 42),
           fill=INK, anchor="ma")
    d.text((W // 2, 186), "MONDAY 23 NOVEMBER 2026  |  ONE DAY, 31 STORIES",
           font=font(F_SANS_B, 13), fill=GRAY, anchor="ma")
    d.text((W // 2, 208),
           "Asia's AI rout, a call to regulate AI, and a power shift in Asia.",
           font=font(F_SANS_I, 13), fill=GRAY, anchor="ma")
    # region bar
    d.line([MX, 232, W - MX, 232], fill=LGRAY, width=1)
    d.text((W // 2, 238),
           "ASIA-PACIFIC 7   ·   AMERICAS 8   ·   MIDDLE EAST 6   ·   "
           "EUROPE 5   ·   AFRICA 3   ·   WORLD 2",
           font=font(F_SANS_B, 12), fill=INK, anchor="ma")
    d.line([MX, 260, W - MX, 260], fill=LGRAY, width=1)

    # ---- heroes ---------------------------------------------------------
    d.text((MX, 270), "TOP STORIES", font=font(F_SANS_B, 12), fill=RED)
    hero_w, hero_x0 = 312, MX
    scene_h = 126
    for i, hero in enumerate(HEROES):
        hx = hero_x0 + i * (hero_w + 12)
        sy = 290
        SCENES[i](d, hx, sy, hero_w, scene_h)
        # black strip above headline is the scene bottom edge; keep a gap
        hy = sy + scene_h + 10
        d.text((hx, hy), hero["kicker"], font=font(F_SANS_B, 10), fill=RED)
        f_h = font(F_SANS_B, 16)
        lines = wrap(d, hero["head"], f_h, hero_w)
        ly = hy + 15
        for ln in lines[:2]:
            d.text((hx, ly), ln, font=f_h, fill=INK)
            ly += 19
        f_b = font(F_SANS, 11)
        blines = wrap(d, hero["body"], f_b, hero_w)
        by = ly + 2
        for ln in blines[:2]:
            d.text((hx, by), ln, font=f_b, fill=(60, 60, 60))
            by += 14
        sy2 = sy + scene_h + 118
        d.text((hx, sy2 + 2), hero["src"], font=font(F_SANS_B, 10), fill=GRAY)
        chip(d, hx + 78, sy2, hero["chip"], claim=(hero["chip"] == "CLAIM"))

    # ---- cards ----------------------------------------------------------
    cy0 = 566
    d.text((MX, cy0), "MORE OF THE DAY", font=font(F_SANS_B, 12), fill=RED)
    card_w, card_h = 193, 74
    for i, (cat, head, src, cl) in enumerate(CARDS):
        row, col = divmod(i, 5)
        cx = MX + col * (card_w + 3)
        cy = cy0 + 20 + row * (card_h + 6)
        d.rectangle([cx, cy, cx + card_w, cy + card_h], fill=(255, 255, 255),
                    outline=LGRAY)
        d.text((cx + 8, cy + 5), cat, font=font(F_SANS_B, 9), fill=RED)
        f_h = font(F_SANS_B, 12)
        lines = wrap(d, head, f_h, card_w - 16)
        ly = cy + 19
        for ln in lines[:2]:
            d.text((cx + 8, ly), ln, font=f_h, fill=INK)
            ly += 14
        # source + chip pinned to the card bottom, clear of the headline
        by = cy + card_h - 20
        d.text((cx + 8, by + 2), src, font=font(F_SANS_B, 9), fill=GRAY)
        chip(d, cx + card_w - 62, by, cl, claim=(cl == "CLAIM"))

    # ---- map + ALSO -----------------------------------------------------
    my0 = 748
    d.text((MX, my0), "WHERE IT HAPPENED", font=font(F_SANS_B, 12), fill=RED)
    d.text((MX + 486, my0), "ALSO ON MONDAY", font=font(F_SANS_B, 12), fill=RED)
    map_x, map_y, map_w, map_h = MX, my0 + 20, 462, 120
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h],
                fill=(238, 240, 244), outline=LGRAY)
    # stylised continents
    d.ellipse([map_x + 16, map_y + 18, map_x + 176, map_y + 102], fill=(205, 212, 205))
    d.ellipse([map_x + 191, map_y + 12, map_x + 276, map_y + 72], fill=(205, 212, 205))
    d.ellipse([map_x + 246, map_y + 62, map_x + 326, map_y + 118], fill=(205, 212, 205))
    d.ellipse([map_x + 296, map_y + 22, map_x + 436, map_y + 102], fill=(205, 212, 205))
    for label, px, py in PINS:
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=NAVY2,
                  outline=(255, 255, 255), width=2)
        num = label.split()[0]
        f_n = font(F_SANS_B, 9)
        tw = text_w(d, num, f_n)
        d.text((px - tw / 2, py - 6), num, font=f_n, fill=(255, 255, 255))
    # pin legend (2 lines, explicit)
    d.text((map_x, map_y + map_h + 4),
           "Pins 1-7: Seoul, Bridgetown, Beijing, Washington, New York, Paris, London",
           font=font(F_SANS, 10), fill=GRAY)
    d.text((map_x, map_y + map_h + 17),
           "Pins 8-13: Manchester, Kyiv, Beirut, Gaza, Khartoum, Kinshasa",
           font=font(F_SANS, 10), fill=GRAY)
    # ALSO list, 2 columns x 9 rows
    ax0 = MX + 486
    f_a = font(F_SANS, 11)
    for i, item in enumerate(ALSO):
        col, row = divmod(i, 9)
        ax = ax0 + col * 244
        ay = my0 + 20 + row * 15
        bullet = "• "
        # split [CLAIM] out so it renders red
        if item.endswith("[CLAIM]"):
            core = item[:-7].strip()
            d.text((ax, ay), bullet + core, font=f_a, fill=INK)
            cw = text_w(d, bullet + core, f_a)
            d.text((ax + cw + 2, ay), "[CLAIM]",
                   font=font(F_SANS_B, 10), fill=RED)
        else:
            d.text((ax, ay), bullet + item, font=f_a, fill=INK)

    # ---- DATE CHECK -----------------------------------------------------
    dy = 922
    d.rectangle([MX, dy, W - MX, dy + 62], fill=RED_BG, outline=RED, width=2)
    d.text((MX + 10, dy + 6), "DATE CHECK — LEFT OUT (NOT 23 NOV)",
           font=font(F_SANS_B, 12), fill=RED)
    f_d = font(F_SANS, 11)
    lo = "  ·  ".join(LEFT_OUT)
    d.text((MX + 10, dy + 24), lo, font=f_d, fill=INK)
    d.text((MX + 10, dy + 42), "NOT YET:  " + "  ·  ".join(NOT_YET),
           font=f_d, fill=INK)

    # ---- footer ---------------------------------------------------------
    fy = 994
    d.line([MX, fy, W - MX, fy], fill=LGRAY, width=1)
    d.text((MX, fy + 6),
           "Sources: Reuters, AP, Bloomberg, WSJ.  REPORTED = confirmed by wires; "
           "CLAIM = one side's claim.",
           font=font(F_SANS, 10), fill=GRAY)
    d.text((W - MX, fy + 6), "THE WORLD TODAY",
           font=font(F_SANS_B, 10), fill=GRAY, anchor="ra")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
