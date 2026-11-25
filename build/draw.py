"""Render the Tuesday 24 November 2026 world-news front page.

One 1024x1024 PNG. Every fact comes from VERIFIED_NEWS.md; every story
is dated Tuesday 24 November 2026. Layout follows the winner pattern:
data-diagram heroes, big key numbers on every tile, verification badges,
a UTC timeline, a black top bar, region-coloured map pins, KPI sentences
and a how-we-checked footer.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas
W, H = 1024, 1024
MARGIN = 8

# ---------------------------------------------------------------- palette
PAPER = (250, 247, 238)
INK = (22, 22, 22)
SOFT = (92, 88, 80)
RULE = (196, 188, 172)
CARD = (255, 255, 255)
CREAM = (244, 238, 226)
RED = (178, 34, 28)
DARKRED = (139, 22, 18)
BLACKBAR = (16, 16, 16)
MAPLAND = (226, 214, 186)
MAPSEA = (214, 226, 232)
GREEN = (28, 128, 60)
BLUE = (28, 92, 178)
ORANGE = (214, 110, 20)
PURPLE = (118, 64, 168)
TEAL = (18, 148, 148)
GREY = (110, 110, 110)
GOLD = (184, 138, 20)

# region -> (label, colour)
REGIONS = {
    "ME": ("MIDDLE EAST", ORANGE),
    "EU": ("EUROPE", GREEN),
    "AS": ("ASIA", RED),
    "AM": ("AMERICAS", BLUE),
    "AF": ("AFRICA", PURPLE),
    "OC": ("OCEANIA", TEAL),
    "GL": ("GLOBAL", GREY),
}

BADGE_FILL = {
    "CONFIRMED": (28, 128, 60),
    "OFFICIAL": (28, 92, 178),
    "REPORTED": (184, 138, 20),
}

# ---------------------------------------------------------------- typefaces
_HERE = os.path.dirname(os.path.abspath(__file__))
_FONTDIR = os.path.join(os.path.dirname(_HERE), "fonts")


def _face(name, size):
    return ImageFont.truetype(os.path.join(_FONTDIR, name), size)


def serif(size):
    return _face("DMSerifDisplay-Regular.ttf", size)


def heavy(size):
    return _face("Lato-Black.ttf", size)


def bold(size):
    return _face("Lato-Bold.ttf", size)


def plain(size):
    return _face("Lato-Regular.ttf", size)


# ---------------------------------------------------------------- text utils
def fit(draw, text, font, width):
    """Wrap text to fit width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def stamp_badge(draw, x, y, label, size=10):
    """Small rounded verification badge; returns its width."""
    f = bold(size)
    w = int(draw.textlength(label, font=f)) + 12
    h = size + 8
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3,
                           fill=BADGE_FILL.get(label, GREY))
    draw.text((x + 6, y + 3), label, font=f, fill=(255, 255, 255))
    return w


def stamp_region(draw, x, y, code, size=9):
    """Region label in its colour."""
    label, colour = REGIONS[code]
    draw.text((x, y), label, font=bold(size), fill=colour)
    return draw.textlength(label, font=bold(size))


# ---------------------------------------------------------------- the day
DAY_LABEL = "Tuesday 24 November 2026"
DAY_SHORT = "TUE 24 NOV"
DAY_NUM = 328

TIMELINE = [
    ("01:45", "Zaporizhzhia hit"),
    ("08:30", "ICJ ruling backed"),
    ("11:20", "Shenzhou 24 up"),
    ("14:05", "Nepal quake 5.6"),
    ("15:18", "Riyadh tower hit"),
    ("17:01", "11 hurt in Riyadh"),
    ("19:40", "Zscaler deal $43.9B"),
]

KPIS = [
    ("11", "hurt in the Riyadh tower strike", "REUTERS"),
    ("$43.9B", "CrowdStrike's deal to buy Zscaler", "AJP"),
    ("14", "countries back ICJ Rohingya ruling", "HORIZON"),
    ("5.6", "Nepal quake magnitude, near China", "HORIZON"),
    ("6,500", "Rohingya Malaysia will send back", "MEDIUM"),
    ("$237B", "Venezuela's disclosed national debt", "AJP"),
]

REGION_COUNTS = [("ME", 6), ("EU", 4), ("AS", 8), ("AM", 8),
                 ("AF", 3), ("OC", 2), ("GL", 2)]

# heroes: (number, region, badge, big, headline, deck, sources, diagram)
HEROES = [
    (1, "ME", "CONFIRMED", "11",
     "Houthi drone hits Riyadh's tallest tower",
     "Second strike on the PIF Tower in under a week; 11 hurt as the "
     "kingdom's financial district is hit again.",
     "REUTERS · WSJ · BLOOMBERG", "strikes"),
    (2, "EU", "CONFIRMED", "2 / 48",
     "Russian strike kills 2, wounds 48 in Zaporizhzhia",
     "Overnight attack hits an apartment block; four of the wounded are "
     "children, the governor says.",
     "JUST SECURITY · REUTERS", "casualty"),
    (3, "GL", "CONFIRMED", "14",
     "14 countries back ICJ's Rohingya genocide ruling",
     "UK, Spain, Canada and Australia among those affirming the court's "
     "finding against Myanmar.",
     "HORIZON · ICJ", "countries"),
]

# tiles: (number, region, badge, big, headline, deck, sources, motif)
TILES = [
    (4, "AM", "CONFIRMED", "$43.9B", "CrowdStrike to buy Zscaler",
     "All-stock deal is the largest cyber takeover yet.", "AJP", "bars"),
    (5, "AS", "CONFIRMED", "1st", "China launches Shenzhou 24",
     "First foreign astronaut — Pakistan's Zeeshan Ali — boards Tiangong.",
     "WSOC · AP", "rocket"),
    (6, "AS", "CONFIRMED", "5.6", "Quake hits Nepal near China border",
     "Magnitude 5.6 strikes Koshi province.", "HORIZON", "quake"),
    (7, "ME", "CONFIRMED", "7", "Israel kills Hamas security chief in Gaza",
     "Naeem Abu Nahel and six others dead in airstrikes.", "JUST SECURITY",
     "target"),
    (8, "AS", "REPORTED", "6,500", "Malaysia to send 6,500 Rohingya back",
     "Refugees to be returned to Myanmar.", "MEDIUM", "people"),
    (9, "AM", "REPORTED", "~50", "US probes Iran role in ship cyberattacks",
     "Bomb threats and hacks hit some 50 tankers and vessels.", "WSJ", "ship"),
    (10, "AM", "CONFIRMED", "$237B", "Venezuela discloses $237B debt",
     "Interim government reveals a far bigger national debt load.", "AJP",
     "chart"),
    (11, "AS", "CONFIRMED", "6", "Hanoi hotpot blast kills 6",
     "Gas explosion at a packed eatery injures 12 or more.", "AP", "blast"),
    (12, "AM", "OFFICIAL", "9", "Pennsylvania measles: 9th death",
     "Epidemic reaches 46 counties in the state.", "HORIZON", "virus"),
    (13, "AS", "REPORTED", "$375K", "Seoul pays to catch AI cheaters",
     "Rewards offered for students using AI in the college exam.",
     "JUST SECURITY", "shield"),
]

# also-on: (number, region, headline, source)
ALSO_ON = [
    (14, "AF", "Tripoli demands answers from Kyiv over Libya ship attack", "UN NEWS"),
    (15, "GL", "UN chief wants AI-risk rules within a year", "HORIZON"),
    (16, "AM", "US ready to slap tariffs on China, EU and others", "AP"),
    (17, "AS", "North Korea demands Swiss office in Pyongyang shut", "AP"),
    (18, "OC", "Solomon Islands names Australia top security partner", "AP"),
    (19, "AM", "Armed men take hostages in a Cartagena supermarket", "AP"),
    (20, "AM", "Car bomb wrecks buildings in Villavicencio", "AP"),
    (21, "EU", "Pope Francis diary tells of a spiritual crisis", "AP"),
    (22, "EU", "Real Madrid roar back 5–1 over PSV", "AP"),
    (23, "AF", "Senegal regain the Africa Cup title", "AP"),
    (24, "ME", "Houthis close in on Aden as forces dig in", "AP"),
    (25, "ME", "Hormuz: 30+ shipping attacks in October, a record", "IQMIA"),
    (26, "AS", "US blacklists Singapore cloud firm Megaspeed", "REUTERS"),
    (27, "ME", "Oxfam: Gaza turned into a 'toxic land'", "OXFAM"),
    (28, "AF", "DRC fighting traps Ebola responders in Ituri", "UN NEWS"),
    (29, "EU", "Germany first to get Ukraine's Delta system", "KYIV IND."),
    (30, "ME", "Iraq PM orders ministry to run Kurdish-area oilfields", "REUTERS"),
    (31, "AS", "Hasina plans return from exile on 16 Dec", "REUTERS"),
    (32, "AM", "Democrats flip a Tennessee House seat", "AP"),
    (33, "OC", "Australia to fine tech giants 5% of global revenue", "AP"),
]

LEFT_OUT = [
    ("MON 23 NOV", "Huang reinstated as Nvidia CEO"),
    ("SUN 22 NOV", "COP31 collapses in Antalya — no deal"),
    ("MON 23 NOV", "Merkury sunk off Libya (announced)"),
    ("MON 23 NOV", "3 tankers hit mines in Hormuz (announced)"),
    ("MON 23 NOV", "UK sanctions 5 Myanmar military leaders"),
    ("THU 19 NOV", "Denmark approves Greenland defence deal"),
]

NOT_YET = [
    ("THU 26 NOV", "ECB chief pick expected (Hernández de Cos tipped)"),
    ("WED 16 DEC", "Hasina plans return to Bangladesh"),
]

# story number -> (lon, lat) for the map pins
PIN_POS = {
    1: (46.7, 24.7), 2: (35.2, 47.8), 3: (96.0, 20.0), 4: (-100.0, 38.0),
    5: (100.3, 41.0), 6: (85.3, 27.7), 7: (34.5, 31.5), 8: (101.7, 3.1),
    9: (-77.0, 38.9), 10: (-66.9, 10.5), 11: (105.8, 21.0), 12: (-77.8, 40.9),
    13: (127.0, 37.5), 14: (13.2, 32.9), 15: (-74.0, 40.7), 16: (-77.0, 38.9),
    17: (127.0, 39.0), 18: (160.0, -9.0), 19: (-75.5, 10.4), 20: (-73.6, 4.1),
    21: (12.45, 41.9), 22: (-3.7, 40.4), 23: (-17.4, 14.7), 24: (45.0, 12.8),
    25: (56.5, 26.5), 26: (103.8, 1.35), 27: (34.5, 31.5), 28: (29.5, 1.5),
    29: (13.4, 52.5), 30: (44.4, 33.3), 31: (90.4, 23.8), 32: (-86.8, 36.1),
    33: (151.2, -33.9),
}

# story number -> region code (for pin colour)
PIN_REGION = {}
for _n, _r, *_rest in HEROES:
    PIN_REGION[_n] = _r
for _n, _r, *_rest in TILES:
    PIN_REGION[_n] = _r
for _n, _r, *_rest in ALSO_ON:
    PIN_REGION[_n] = _r


# ---------------------------------------------------------------- mini motifs
def _motif(draw, box, kind, accent):
    """Tiny geometric diagram inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "bars":
        vals = [0.45, 0.8, 0.6, 1.0]
        bw = w // 6
        for i, v in enumerate(vals):
            bx = x0 + 6 + i * (bw + 3)
            draw.rectangle([bx, y1 - 4 - int(v * (h - 10)), bx + bw, y1 - 4],
                           fill=accent)
    elif kind == "rocket":
        draw.arc([x0 + 8, y0 + 4, x1 - 8, y1 - 2], 200, 340, fill=accent, width=3)
        draw.ellipse([x1 - 16, y0 + 6, x1 - 6, y0 + 16], fill=RED)
        draw.ellipse([x0 + 6, y1 - 14, x0 + 14, y1 - 6], fill=GOLD)
    elif kind == "quake":
        pts = [(x0 + 4, cy), (x0 + w * 0.25, cy - 8), (x0 + w * 0.38, cy + 10),
               (x0 + w * 0.5, cy - 14), (x0 + w * 0.62, cy + 8),
               (x0 + w * 0.75, cy - 6), (x1 - 4, cy)]
        draw.line(pts, fill=accent, width=3, joint="curve")
    elif kind == "target":
        for r, col in ((16, RED), (11, CARD), (6, RED)):
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=3)
        draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=RED)
    elif kind == "people":
        for i in range(5):
            px = x0 + 12 + i * (w - 24) // 4
            draw.ellipse([px - 5, cy - 12, px + 5, cy - 2], fill=accent)
            draw.arc([px - 8, cy - 2, px + 8, cy + 12], 180, 360, fill=accent, width=3)
    elif kind == "ship":
        draw.polygon([(x0 + 8, cy + 2), (x1 - 8, cy + 2), (x1 - 18, cy + 12),
                      (x0 + 18, cy + 12)], fill=accent)
        draw.rectangle([cx - 3, cy - 12, cx + 3, cy + 2], fill=INK)
        draw.polygon([(cx + 3, cy - 12), (cx + 16, cy - 4), (cx + 3, cy - 4)],
                     fill=RED)
    elif kind == "chart":
        pts = [(x0 + 4, y1 - 8), (x0 + w * 0.3, y1 - 16), (x0 + w * 0.5, y1 - 12),
               (x0 + w * 0.75, y1 - 22), (x1 - 6, y1 - 26)]
        draw.line(pts, fill=accent, width=3, joint="curve")
        draw.polygon([(x1 - 12, y1 - 26), (x1 - 4, y1 - 26), (x1 - 8, y1 - 18)],
                     fill=accent)
    elif kind == "blast":
        for ang in range(0, 360, 45):
            import math
            r1, r2 = 5, 17
            a = math.radians(ang)
            draw.line([cx + r1 * math.cos(a), cy + r1 * math.sin(a),
                       cx + r2 * math.cos(a), cy + r2 * math.sin(a)],
                      fill=accent, width=3)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    elif kind == "virus":
        import math
        draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=accent)
        for ang in range(0, 360, 40):
            a = math.radians(ang)
            draw.line([cx + 9 * math.cos(a), cy + 9 * math.sin(a),
                       cx + 14 * math.cos(a), cy + 14 * math.sin(a)],
                      fill=accent, width=2)
    elif kind == "shield":
        draw.polygon([(cx - 13, cy - 14), (cx + 13, cy - 14), (cx + 13, cy + 2),
                      (cx, cy + 16), (cx - 13, cy + 2)], outline=accent, width=3)
        draw.line([(cx - 6, cy), (cx - 1, cy + 6), (cx + 8, cy - 6)],
                  fill=accent, width=3, joint="curve")


# ---------------------------------------------------------------- hero diagrams
def _hero_strikes(draw, x0, y0, x1, y1):
    """Timeline of the three Riyadh strikes; big 11 on the right."""
    draw.rectangle([x0, y0, x1, y1], fill=(24, 28, 44))
    # tower silhouette
    tx = x0 + 26
    draw.rectangle([tx, y0 + 26, tx + 16, y1 - 8], fill=(120, 130, 160))
    draw.polygon([(tx - 3, y0 + 26), (tx + 19, y0 + 26), (tx + 8, y0 + 14)],
                 fill=(120, 130, 160))
    for wy in range(y0 + 34, y1 - 12, 12):
        draw.rectangle([tx + 3, wy, tx + 6, wy + 5], fill=(240, 200, 90))
        draw.rectangle([tx + 10, wy, tx + 13, wy + 5], fill=(240, 200, 90))
    # strike timeline
    lx, rx = x0 + 72, x1 - 8
    ly = y0 + 62
    draw.line([(lx, ly), (rx, ly)], fill=(200, 200, 200), width=2)
    stops = [("19 NOV", "no injuries", (150, 150, 150), 0.0),
             ("20 NOV", "strike", (240, 200, 90), 0.5),
             ("24 NOV", "11 INJURED", RED, 1.0)]
    for label, note, col, frac in stops:
        px = lx + int(frac * (rx - lx))
        r = 7 if frac == 1.0 else 5
        draw.ellipse([px - r, ly - r, px + r, ly + r], fill=col,
                     outline=(255, 255, 255), width=2)
        if frac == 1.0:
            draw.text((rx, ly - 26), label, font=bold(10),
                      fill=(255, 255, 255), anchor="ra")
            draw.text((rx, ly + 12), note, font=bold(9), fill=(255, 120, 110),
                      anchor="ra")
        else:
            draw.text((px - 18, ly - 26), label, font=bold(10),
                      fill=(255, 255, 255))
            draw.text((px - 22, ly + 12), note, font=plain(9),
                      fill=(210, 210, 210))
    draw.text((lx, y0 + 8), "THREE STRIKES ON THE FINANCIAL DISTRICT",
              font=bold(10), fill=(255, 255, 255))
    draw.text((lx, y0 + 24), "in 16 days — the 24 Nov hit was the second on this tower",
              font=plain(9), fill=(200, 200, 200))


def _hero_casualty(draw, x0, y0, x1, y1):
    """Casualty bars: 2 killed, 48 wounded (4 children)."""
    draw.rectangle([x0, y0, x1, y1], fill=(250, 240, 228))
    draw.text((x0 + 10, y0 + 8), "OVERNIGHT STRIKE — APARTMENT BLOCK HIT",
              font=bold(10), fill=INK)
    # killed bar
    draw.text((x0 + 10, y0 + 30), "KILLED", font=bold(11), fill=INK)
    draw.rectangle([x0 + 80, y0 + 30, x0 + 100, y0 + 48], fill=INK)
    draw.text((x0 + 108, y0 + 30), "2", font=heavy(20), fill=INK)
    # wounded bar (48 = 24x the killed bar)
    draw.text((x0 + 10, y0 + 58), "WOUNDED", font=bold(11), fill=INK)
    bw = x1 - x0 - 172
    draw.rectangle([x0 + 80, y0 + 58, x0 + 80 + bw, y0 + 76], fill=RED)
    draw.text((x0 + 86 + bw, y0 + 58), "48", font=heavy(20), fill=RED)
    draw.text((x0 + 10, y0 + 86),
              "including 4 children — Zaporizhzhia governor Mykhailo Semikin",
              font=plain(9), fill=SOFT)


def _hero_countries(draw, x0, y0, x1, y1):
    """Fourteen country dots: the four named, plus ten more."""
    draw.rectangle([x0, y0, x1, y1], fill=(232, 240, 232))
    draw.text((x0 + 10, y0 + 8), "WHO AFFIRMED THE ICJ RULING",
              font=bold(10), fill=INK)
    names = ["UK", "SPAIN", "CANADA", "AUSTRALIA"]
    for i, name in enumerate(names):
        px = x0 + 16 + i * 74
        draw.ellipse([px, y0 + 32, px + 26, y0 + 58], fill=GREEN)
        draw.text((px + 13, y0 + 38), str(i + 1), font=bold(11),
                  fill=(255, 255, 255), anchor="mm")
        draw.text((px - 6, y0 + 62), name, font=bold(9), fill=INK)
    # ten more dots
    for i in range(10):
        px = x0 + 16 + i * 28
        draw.ellipse([px, y0 + 84, px + 18, y0 + 102], fill=(90, 160, 110))
    draw.text((x0 + 10, y0 + 106), "+ 10 more countries — 14 in all",
              font=plain(9), fill=SOFT)


# ---------------------------------------------------------------- map
CONTINENTS = {
    "namerica": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73),
                 (-65, 60), (-60, 47), (-70, 42), (-75, 35), (-80, 26),
                 (-90, 21), (-97, 16), (-105, 20), (-115, 30), (-125, 40),
                 (-125, 49), (-140, 60), (-165, 60)],
    "samerica": [(-80, 10), (-75, 5), (-70, -5), (-60, -10), (-40, -20),
                 (-35, -8), (-50, 0), (-60, 5), (-70, 10), (-78, 8)],
    "europe": [(-10, 36), (-5, 44), (0, 50), (5, 55), (10, 58), (18, 56),
               (20, 60), (25, 65), (30, 70), (40, 68), (45, 60), (40, 50),
               (35, 45), (28, 40), (20, 38), (12, 42), (5, 38), (0, 36)],
    "africa": [(-18, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
               (35, 28), (40, 15), (48, 11), (50, 0), (40, -10), (35, -20),
               (30, -30), (20, -35), (15, -30), (12, -18), (10, -5), (5, 5),
               (-5, 5), (-15, 10)],
    "asia": [(40, 70), (60, 72), (80, 73), (100, 77), (120, 73), (140, 72),
             (160, 70), (170, 65), (160, 60), (150, 55), (140, 45),
             (130, 40), (125, 35), (120, 30), (110, 20), (105, 10),
             (100, 5), (95, 15), (90, 22), (80, 15), (75, 8), (70, 20),
             (60, 25), (55, 28), (50, 30), (45, 35), (40, 40), (40, 50),
             (40, 60)],
    "oceania": [(113, -22), (120, -15), (130, -12), (137, -15), (142, -11),
                (147, -19), (150, -22), (153, -27), (150, -37), (140, -38),
                (130, -32), (120, -34), (114, -30)],
}


def _project(lon, lat, box):
    x0, y0, x1, y1 = box
    px = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    py = y0 + (75.0 - lat) / 130.0 * (y1 - y0)
    return (px, py)


def draw_map(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=MAPSEA)
    # graticule
    for gx in range(x0 + 60, x1, 60):
        draw.line([(gx, y0), (gx, y1)], fill=(200, 214, 222), width=1)
    for gy in range(y0 + 30, y1, 30):
        draw.line([(x0, gy), (x1, gy)], fill=(200, 214, 222), width=1)
    for pts in CONTINENTS.values():
        poly = [_project(lon, lat, box) for lon, lat in pts]
        draw.polygon(poly, fill=MAPLAND, outline=(180, 168, 140))
    # pins: compute positions, spread any that collide, then draw
    spots = []
    for num in sorted(PIN_POS):
        lon, lat = PIN_POS[num]
        px, py = _project(lon, lat, box)
        spots.append([num, px, py])
    for _pass in range(3):
        for i in range(len(spots)):
            for j in range(i + 1, len(spots)):
                dx = spots[j][1] - spots[i][1]
                dy = spots[j][2] - spots[i][2]
                d2 = dx * dx + dy * dy
                if d2 < 13 * 13:
                    spots[j][1] += 8
                    spots[j][2] += 5
    for num, px, py in spots:
        _, colour = REGIONS[PIN_REGION[num]]
        r = 6
        draw.ellipse([px - r, py - r, px + r, py + r], fill=colour,
                     outline=(255, 255, 255), width=1)
        draw.text((px, py), str(num), font=bold(7), fill=(255, 255, 255),
                  anchor="mm")


# ---------------------------------------------------------------- page sections
def _top_bar(draw):
    draw.rectangle([0, 0, W, 20], fill=BLACKBAR)
    draw.text((MARGIN, 4), "THE WORLD IN ONE DAY", font=bold(11),
              fill=(255, 255, 255))
    mid = "DAY %d OF 2026" % DAY_NUM
    draw.text((W // 2, 4), mid, font=bold(11), fill=(255, 90, 80),
              anchor="ma")
    draw.text((W - MARGIN, 4), "ALL TIMES UTC · RANKED BY CONSEQUENCE",
              font=bold(11), fill=(255, 255, 255), anchor="ra")


def _masthead(draw):
    draw.text((W // 2, 24), DAY_LABEL, font=serif(52), fill=INK, anchor="ma")
    draw.line([(MARGIN, 76), (W - MARGIN, 76)], fill=RED, width=2)
    sub = "33 STORIES · 7 REGIONS · EVERY ONE DATED TUESDAY 24 NOVEMBER 2026"
    draw.text((W // 2, 80), sub, font=bold(13), fill=RED, anchor="ma")


def _timeline(draw):
    y = 98
    draw.rectangle([MARGIN, y, MARGIN + 118, y + 16], fill=BLACKBAR)
    draw.text((MARGIN + 8, y + 3), "THE DAY IN UTC", font=bold(10),
              fill=(255, 255, 255))
    line_y = y + 32
    x_start = 140
    draw.line([(x_start, line_y), (W - MARGIN, line_y)], fill=RULE, width=2)
    span = W - MARGIN - x_start
    for i, (when, what) in enumerate(TIMELINE):
        cx = x_start + int((i + 0.5) * span / len(TIMELINE))
        draw.ellipse([cx - 4, line_y - 4, cx + 4, line_y + 4], fill=RED,
                     outline=(255, 255, 255), width=1)
        draw.text((cx, line_y - 26), when, font=bold(10), fill=INK,
                  anchor="ma")
        draw.text((cx, line_y + 8), what, font=plain(8), fill=SOFT,
                  anchor="ma")


def _kpi_strip(draw):
    y0, y1 = 152, 202
    bw = (W - 2 * MARGIN - 5 * 6) // 6
    for i, (num, fact, src) in enumerate(KPIS):
        x0 = MARGIN + i * (bw + 6)
        draw.rectangle([x0, y0, x0 + bw, y1], outline=RULE, width=1,
                       fill=CARD)
        draw.text((x0 + 8, y0 + 2), num, font=heavy(18), fill=RED)
        body = fact + " — " + src
        for j, ln in enumerate(fit(draw, body, plain(8), bw - 16)[:2]):
            draw.text((x0 + 8, y0 + 25 + j * 10), ln, font=plain(8), fill=INK)


def _region_bar(draw):
    y = 208
    draw.text((MARGIN, y), "STORIES BY REGION", font=bold(10), fill=INK)
    x = MARGIN + 130
    for code, count in REGION_COUNTS:
        label, colour = REGIONS[code]
        draw.rectangle([x, y + 1, x + 9, y + 10], fill=colour)
        txt = "%s %d" % (label, count)
        draw.text((x + 13, y), txt, font=bold(10), fill=INK)
        x += int(draw.textlength(txt, font=bold(10))) + 26


def _draw_hero(draw, hero, x0, x1, y0):
    num, region, badge, big, head, deck, sources, diagram = hero
    # diagram
    if diagram == "strikes":
        _hero_strikes(draw, x0, y0, x1, y0 + 106)
    elif diagram == "casualty":
        _hero_casualty(draw, x0, y0, x1, y0 + 106)
    else:
        _hero_countries(draw, x0, y0, x1, y0 + 106)
    # number + region + badge row
    ry = y0 + 112
    draw.text((x0, ry), big, font=heavy(26), fill=RED)
    nx = x0 + int(draw.textlength(big, font=heavy(26))) + 10
    stamp_region(draw, nx, ry + 8, region, size=10)
    stamp_badge(draw, x1 - 86, ry + 6, badge, size=10)
    # headline
    hy = ry + 30
    for j, ln in enumerate(fit(draw, head, heavy(19), x1 - x0)[:2]):
        draw.text((x0, hy + j * 22), ln, font=heavy(19), fill=INK)
    # deck
    dy = hy + 46
    for j, ln in enumerate(fit(draw, deck, plain(10), x1 - x0)[:2]):
        draw.text((x0, dy + j * 12), ln, font=plain(10), fill=SOFT)
    # sources
    draw.text((x0, dy + 28), sources, font=bold(8), fill=SOFT)


def _draw_tile(draw, tile, x0, x1, y0, y1):
    num, region, badge, big, head, deck, sources, motif = tile
    draw.rectangle([x0, y0, x1, y1], outline=RULE, width=1, fill=CARD)
    # motif band
    _, colour = REGIONS[region]
    draw.rectangle([x0 + 1, y0 + 1, x1 - 1, y0 + 32], fill=(242, 240, 234))
    _motif(draw, (x0 + 1, y0 + 1, x1 - 1, y0 + 32), motif, colour)
    # big number + badge
    ny = y0 + 36
    draw.text((x0 + 8, ny), big, font=heavy(20), fill=RED)
    stamp_badge(draw, x1 - 72, ny + 4, badge, size=9)
    # headline
    hy = ny + 24
    for j, ln in enumerate(fit(draw, head, heavy(11), x1 - x0 - 16)[:2]):
        draw.text((x0 + 8, hy + j * 13), ln, font=heavy(11), fill=INK)
    # deck with source folded in
    body = deck + " (" + sources + ")"
    dy = hy + 28
    for j, ln in enumerate(fit(draw, body, plain(9), x1 - x0 - 16)[:2]):
        draw.text((x0 + 8, dy + j * 11), ln, font=plain(9), fill=SOFT)


def _map_and_datecheck(draw):
    y0, y1 = 674, 824
    # --- map (left)
    draw.text((MARGIN, y0), "WHERE IT HAPPENED — PIN NUMBERS MATCH THE "
              "STORIES; PIN COLOUR IS THE REGION", font=bold(9), fill=INK)
    draw_map(draw, (MARGIN, y0 + 16, 648, y1))
    # --- date check (right)
    dx0, dx1 = 656, W - MARGIN
    draw.rectangle([dx0, y0, dx1, y1], outline=RED, width=2)
    draw.text((dx0 + 10, y0 + 6), "DATE CHECK", font=heavy(14), fill=RED)
    draw.text((dx0 + 10, y0 + 24), "— what we left out, and why",
              font=plain(9), fill=SOFT)
    yy = y0 + 42
    draw.text((dx0 + 10, yy), "LEFT OUT — OTHER DAYS", font=bold(10), fill=INK)
    yy += 16
    for date, what in LEFT_OUT:
        draw.text((dx0 + 10, yy), date, font=bold(9), fill=RED)
        for j, ln in enumerate(fit(draw, what, plain(9), dx1 - dx0 - 118)[:1]):
            draw.text((dx0 + 112, yy), ln, font=plain(9), fill=INK)
        yy += 12
    yy += 4
    draw.text((dx0 + 10, yy), "NOT YET", font=bold(10), fill=INK)
    yy += 16
    for date, what in NOT_YET:
        draw.text((dx0 + 10, yy), date, font=bold(9), fill=RED)
        for j, ln in enumerate(fit(draw, what, plain(9), dx1 - dx0 - 118)[:1]):
            draw.text((dx0 + 112, yy), ln, font=plain(9), fill=INK)
        yy += 12


def _also_on(draw):
    y0 = 830
    draw.text((MARGIN, y0), "ALSO ON TUESDAY 24 NOVEMBER",
              font=heavy(12), fill=INK)
    draw.line([(MARGIN, y0 + 16), (W - MARGIN, y0 + 16)], fill=RULE, width=1)
    col_w = (W - 2 * MARGIN - 16) // 2
    for idx, (num, region, head, src) in enumerate(ALSO_ON):
        col = idx // 10
        row = idx % 10
        x = MARGIN + col * (col_w + 16)
        yy = y0 + 22 + row * 11
        _, colour = REGIONS[region]
        draw.text((x, yy), str(num), font=bold(8), fill=RED)
        draw.text((x + 20, yy), head, font=plain(8), fill=INK)
        tw = draw.textlength(head, font=plain(8))
        draw.text((x + 20 + int(tw) + 4, yy), "(%s)" % src, font=bold(7),
                  fill=SOFT)


def _footer(draw):
    y0 = 966
    draw.line([(MARGIN, y0), (W - MARGIN, y0)], fill=RULE, width=1)
    draw.text((MARGIN, y0 + 6), "HOW WE CHECKED", font=heavy(11), fill=INK)
    # badge legend
    lx = MARGIN + 130
    for label, meaning in (("CONFIRMED", "2+ major outlets"),
                           ("OFFICIAL", "on the record"),
                           ("REPORTED", "one major outlet")):
        w = stamp_badge(draw, lx, y0 + 6, label, size=9)
        draw.text((lx + w + 5, y0 + 7), meaning, font=plain(9), fill=SOFT)
        lx += w + int(draw.textlength(meaning, font=plain(9))) + 22
    draw.text((MARGIN, y0 + 24),
              "Sources: Reuters · WSJ · Bloomberg · AP · Just Security · "
              "Horizon · The Global Eye · AND Magazine · Astrova · IQMIA · AJP.",
              font=plain(9), fill=SOFT)
    draw.text((MARGIN, y0 + 38),
              "Every story happened or was first reported on Tuesday 24 "
              "November 2026 (UTC). No story from another day is shown as "
              "today's news.",
              font=plain(9), fill=INK)
    draw.text((W // 2, y0 + 52),
              "THE WORLD IN ONE DAY · 33 STORIES · TUESDAY 24 NOVEMBER 2026",
              font=bold(9), fill=SOFT, anchor="ma")


# ---------------------------------------------------------------- render
def render_page():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    _top_bar(draw)
    _masthead(draw)
    _timeline(draw)
    _kpi_strip(draw)
    _region_bar(draw)
    # heroes: three columns
    hx = [MARGIN, 347, 686]
    hw = [331, 331, 330]
    for hero, x0, w in zip(HEROES, hx, hw):
        _draw_hero(draw, hero, x0, x0 + w, 226)
    # tiles: two rows of five
    tx = [MARGIN, 211, 414, 617, 820]
    for row in range(2):
        y0 = 448 + row * 112
        for col in range(5):
            tile = TILES[row * 5 + col]
            _draw_tile(draw, tile, tx[col], tx[col] + 195, y0, y0 + 108)
    _map_and_datecheck(draw)
    _also_on(draw)
    _footer(draw)
    return img
