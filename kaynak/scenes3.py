"""Backgrounds, props and icons for Season 2 'Kayıp Fidan' and the Zeyto'nun Notları #8+ videos."""
import math
import random
from functools import lru_cache
from PIL import Image, ImageDraw
from brand import *
from story import vgrad, _tree, W, H, BGW
from make_main import notebook_page
from make_story import canvas, BLUE
from scenes2 import lora

SKY = ((150, 200, 232), (250, 236, 210))
NSKY = ((18, 26, 58), (60, 70, 110))


def _stars(d, rnd, n=110, ymax=900):
    for _ in range(n):
        x, y, r = rnd.uniform(0, BGW), rnd.uniform(0, ymax), rnd.choice([1.5, 2, 2.5, 3.5])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 250, 220))


def _grass(d, rnd, ground, y0=1500, n=70):
    for _ in range(n):
        gx, gy = rnd.uniform(0, BGW), rnd.uniform(y0, H)
        d.line([(gx, gy), (gx + 6, gy - 22)], fill=tuple(max(0, c - 16) for c in ground), width=5)


def _night(im):
    sh = Image.new("RGBA", im.size, (14, 22, 50, 120))
    im.alpha_composite(sh)
    return im


# ------------------------------------------------------------------ backgrounds
@lru_cache(maxsize=2)
def bg_mountain(night=False):
    rnd = random.Random(61)
    im = vgrad(BGW, H, *(NSKY if night else SKY))
    d = ImageDraw.Draw(im)
    if night:
        _stars(d, rnd)
        d.ellipse([140, 240, 290, 390], fill=(250, 244, 214))
    # far peaks with snow caps
    peaks = [(-100, 1150, 260, 520, 620), (300, 1150, 640, 430, 700), (720, 1150, 1050, 560, 640)]
    for x0, yb, xp, yp, x1 in peaks:
        col = (70, 84, 110) if night else (150, 160, 190)
        d.polygon([(x0, yb), (xp, yp), (x1 + 200, yb)], fill=col)
        d.polygon([(xp, yp), (xp - 70, yp + 110), (xp - 20, yp + 90), (xp + 20, yp + 120), (xp + 80, yp + 100)],
                  fill=(200, 210, 230) if night else (250, 252, 255))
    hill = (44, 60, 52) if night else (120, 150, 84)
    d.polygon([(0, 1250)] + [(x, 1180 - 90 * math.sin(x / 300 + 0.5)) for x in range(0, BGW + 1, 20)] + [(BGW, 1520), (0, 1520)], fill=hill)
    for x in (120, 380, 980):
        _tree(d, x, 1260, 0.22, rnd, [(40, 34, 46)] if night else [(110, 52, 84)])
    ground = (54, 62, 44) if night else (168, 150, 104)
    d.rectangle([0, 1470, BGW, H], fill=ground)
    path = (70, 70, 58) if night else (206, 186, 140)
    d.polygon([(380, 1470), (700, 1470), (1050, H), (100, H)], fill=path)
    for _ in range(26):                                                  # rocks
        x, y, r = rnd.uniform(0, BGW), rnd.uniform(1490, H), rnd.uniform(14, 40)
        d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=(120, 116, 104) if not night else (60, 60, 54))
    _grass(d, rnd, ground)
    if night:
        _night(im)
    return im


@lru_cache(maxsize=2)
def bg_river():
    rnd = random.Random(62)
    im = vgrad(BGW, H, *SKY)
    d = ImageDraw.Draw(im)
    d.polygon([(0, 1150)] + [(x, 1080 - 60 * math.sin(x / 240)) for x in range(0, BGW + 1, 20)] + [(BGW, 1400), (0, 1400)], fill=(126, 160, 92))
    for x in (100, 300, 900, 1100):
        _tree(d, x, 1180, 0.24, rnd, [(110, 52, 84)])
    d.rectangle([0, 1380, BGW, H], fill=(150, 176, 96))                 # banks
    d.polygon([(0, 1500), (BGW, 1440), (BGW, 1760), (0, 1820)], fill=(90, 156, 200))   # water
    for k in range(40):
        x, y = rnd.uniform(0, BGW), rnd.uniform(1500, 1760)
        d.line([(x, y), (x + 60, y - 4)], fill=(190, 226, 240), width=5)
    for x in (180, 420, 660, 900):                                        # stepping stones
        d.ellipse([x - 70, 1610, x + 70, 1660], fill=(140, 136, 126))
    # broken bridge: two stumps + planks in the water
    d.rectangle([60, 1330, 100, 1520], fill=(110, 78, 48))
    d.rectangle([1100, 1310, 1140, 1490], fill=(110, 78, 48))
    d.polygon([(560, 1560), (760, 1600), (750, 1625), (550, 1585)], fill=(140, 100, 62))
    return im


@lru_cache(maxsize=2)
def bg_ruin():
    rnd = random.Random(63)
    im = vgrad(BGW, H, (190, 206, 214), (236, 226, 200))
    d = ImageDraw.Draw(im)
    d.polygon([(0, 1150)] + [(x, 1110 - 50 * math.sin(x / 210)) for x in range(0, BGW + 1, 20)] + [(BGW, 1450), (0, 1450)], fill=(120, 140, 92))
    # ruined stone hut
    d.polygon([(700, 1380), (700, 980), (860, 900), (1020, 1000), (1020, 1380)], fill=(170, 160, 140))
    for k in range(10):
        x, y = 720 + (k % 3) * 100, 1000 + (k // 3) * 90
        d.rectangle([x, y, x + 80, y + 40], outline=(140, 130, 112), width=4)
    d.rectangle([800, 1180, 900, 1380], fill=(70, 60, 50))
    # overgrown wild trees (spiky)
    for x in (120, 400, 600, 1120):
        _tree(d, x, 1360, 0.26, rnd, [(70, 70, 50)])
    d.rectangle([0, 1440, BGW, H], fill=(132, 140, 90))
    for _ in range(90):                                                  # brambles
        x, y = rnd.uniform(0, BGW), rnd.uniform(1440, H)
        d.line([(x, y), (x + rnd.uniform(-30, 30), y - rnd.uniform(20, 60))], fill=(96, 104, 62), width=6)
    for x, y in [(120, 1520), (980, 1560)]:                               # terrace stones
        for k in range(6):
            d.ellipse([x + k * 46, y, x + k * 46 + 50, y + 34], fill=(156, 150, 134))
    return im


@lru_cache(maxsize=2)
def bg_school(night=False):
    rnd = random.Random(64)
    im = vgrad(BGW, H, *(NSKY if night else SKY))
    d = ImageDraw.Draw(im)
    if night:
        _stars(d, rnd)
    # old school building
    wall = (232, 214, 180)
    d.rectangle([520, 820, 1200, 1400], fill=wall)
    d.polygon([(490, 830), (860, 650), (1230, 830)], fill=(176, 92, 64))
    for x in (580, 760, 1060):
        d.rectangle([x, 920, x + 110, 1080], fill=(120, 160, 190))
        d.line([(x + 55, 920), (x + 55, 1080)], fill=wall, width=8)
    d.rectangle([900, 1180, 1010, 1400], fill=(120, 80, 50))
    f = font(F_BOLD, 40)
    d.rectangle([620, 1110, 1150, 1170], fill=(250, 246, 236))
    d.text((640, 1116), "KÖY İLKOKULU · 1958", font=f, fill=DARK)
    # big lone olive tree by the well (the lost sapling, 30 years later)
    d.polygon([(250, 1440), (300, 1100), (260, 950), (340, 980), (370, 1100), (330, 1440)], fill=(110, 86, 60))
    for k in range(16):
        cx, cy, r = 300 + rnd.uniform(-210, 210), 880 + rnd.uniform(-140, 110), rnd.uniform(80, 130)
        d.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7], fill=(118, 146, 92) if (k % 3) else (150, 170, 120))
    for k in range(10):
        x, y = 300 + rnd.uniform(-200, 200), 880 + rnd.uniform(-100, 120)
        draw_olive(d, x, y, 12, PURPLE)
    # well
    d.ellipse([400, 1400, 560, 1450], fill=(120, 116, 110))
    d.rectangle([400, 1340, 560, 1425], fill=(156, 150, 140))
    d.ellipse([400, 1320, 560, 1370], fill=(60, 60, 64))
    d.line([(410, 1340), (410, 1200), (550, 1200), (550, 1340)], fill=(110, 78, 48), width=12)
    ground = (40, 52, 40) if night else (186, 176, 140)
    d.rectangle([0, 1450, BGW, H], fill=ground)
    _grass(d, rnd, ground)
    if night:
        _night(im)
    return im


# ------------------------------------------------------------------ props / cards
def campfire(size=360):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size / 2
    for r, a in [(c, 40), (c * 0.7, 70)]:
        d.ellipse([c - r, c - r, c + r, c + r], fill=(255, 170, 60, a))
    d.line([(c - 110, c + 110), (c + 110, c + 70)], fill=(110, 70, 40), width=26)
    d.line([(c - 110, c + 70), (c + 110, c + 110)], fill=(90, 60, 34), width=26)
    d.polygon([(c - 70, c + 80), (c, c - 120), (c + 70, c + 80)], fill=(240, 120, 40))
    d.polygon([(c - 40, c + 80), (c, c - 50), (c + 40, c + 80)], fill=(255, 210, 80))
    return im


def stone_marker(text="1996"):
    im, d = canvas(600)
    d.ellipse([60, 430, 540, 560], fill=(80, 60, 40))                    # empty hole
    d.ellipse([110, 450, 490, 540], fill=(50, 36, 24))
    d.rounded_rectangle([380, 170, 560, 470], radius=60, fill=(170, 166, 156))
    f = font(F_BOLD, 64)
    d.text((470 - f.getlength(text) / 2, 260), text, font=f, fill=(90, 86, 80))
    return im


def half_map(reveal=False):
    pw, ph = 760, 600
    im = Image.new("RGBA", (pw + 40, ph + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rnd = random.Random(9)
    edge = [(pw * 0.62 + rnd.uniform(-30, 30), y) for y in range(10, ph + 20, 30)]
    poly = [(10, 10)] + edge + [(10, ph + 10)]
    d.polygon([(x + 14, y + 18) for x, y in poly], fill=(0, 0, 0, 60))
    d.polygon(poly, fill=(232, 214, 168))
    d.line([(40, 460), (160, 360), (300, 400)], fill=(60, 110, 160), width=10)
    d.text((40, 30), "Kayıp Fidan", font=lora(56), fill=(80, 50, 30))
    if reveal:
        f = lora(54)
        for k, t in enumerate(["Okul bahçesi,", "kuyunun yanı."]):
            d.text((40, 160 + k * 74), t, font=f, fill=(150, 90, 40))
    return im.rotate(-3, resample=Image.BICUBIC, expand=True)


def lab_result():
    im = Image.new("RGBA", (780, 780), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([30, 30, 750, 750], fill=(250, 250, 248), outline=(200, 200, 200), width=4)
    f, fb = font(F_MED, 32), font(F_BOLD, 42)
    d.text((70, 70), "DNA ANALİZİ", font=fb, fill=DARK)
    d.line([(70, 135), (710, 135)], fill=(200, 200, 200), width=4)
    rows = [("Numune", "Okul ağacı"), ("Karşılaştırma", "Ulu"), ("Eşleşme", "% 100"), ("Kayıtlı çeşit", "Yok")]
    for k, (a, b) in enumerate(rows):
        y = 170 + k * 90
        d.text((70, y), a, font=f, fill=(90, 90, 90))
        d.text((400, y), b, font=fb if k >= 2 else f, fill=OLIVE if k == 2 else (RED if k == 3 else DARK))
    d.ellipse([440, 560, 700, 720], outline=OLIVE, width=10)
    d.text((478, 612), "YEREL ÇEŞİT", font=font(F_BOLD, 34), fill=OLIVE)
    return im


def permit():
    im = Image.new("RGBA", (760, 700), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([30, 30, 730, 670], fill=(246, 246, 240), outline=(180, 180, 180), width=4)
    fb, f = font(F_BOLD, 46), font(F_MED, 34)
    d.text((70, 70), "SÖKÜM İZNİ", font=fb, fill=DARK)
    for k, t in enumerate(["Arazi: Eski okul", "Ağaç: 1 adet zeytin", "İmza: ............"]):
        d.text((70, 170 + k * 80), t, font=f, fill=(80, 80, 80))
    d.rounded_rectangle([360, 470, 700, 600], radius=16, outline=RED, width=10)
    d.text((392, 505), "İMZASIZ!", font=font(F_BOLD, 56), fill=RED)
    return im


def safe_box():
    im, d = canvas(600)
    d.rounded_rectangle([90, 120, 510, 520], radius=24, fill=(70, 76, 84), outline=(40, 44, 50), width=12)
    d.ellipse([240, 260, 360, 380], fill=(180, 180, 186))
    d.rectangle([292, 300, 308, 360], fill=(40, 44, 50))
    d.rounded_rectangle([100, 520, 160, 560], radius=8, fill=(40, 44, 50))
    d.rounded_rectangle([440, 520, 500, 560], radius=8, fill=(40, 44, 50))
    return im


def pot_row(n=5):
    im = Image.new("RGBA", (900, 420), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k in range(n):
        x = 90 + k * 180
        d.polygon([(x - 60, 260), (x + 60, 260), (x + 44, 400), (x - 44, 400)], fill=(196, 110, 70))
        d.rectangle([x - 66, 248, x + 66, 272], fill=(176, 96, 60))
        d.line([(x, 260), (x, 120)], fill=(110, 86, 60), width=10)
        for j, (dx, dy, a) in enumerate([(-30, 150, 30), (30, 130, -30), (-26, 100, 40), (26, 80, -40)]):
            d.polygon(leaf_poly(x + dx, dy, 60, 18, a), fill=LEAF)
    return im


# ------------------------------------------------------------------ icons (800x800)
def ic_snow():
    im, d = canvas()
    for a in range(0, 180, 30):
        r = math.radians(a)
        dx, dy = 300 * math.cos(r), 300 * math.sin(r)
        d.line([(400 - dx, 400 - dy), (400 + dx, 400 + dy)], fill=BLUE, width=34)
        for s in (1, -1):
            bx, by = 400 + s * dx * 0.6, 400 + s * dy * 0.6
            for b in (40, -40):
                rb = r + math.radians(b) + (0 if s > 0 else math.pi)
                d.line([(bx, by), (bx + 90 * math.cos(rb), by + 90 * math.sin(rb))], fill=BLUE, width=24)
    return im


def ic_wrap_trunk():
    im, d = canvas()
    d.rectangle([340, 180, 460, 700], fill=(110, 86, 60))
    for k in range(6):
        y = 300 + k * 60
        d.polygon([(320, y), (480, y - 30), (480, y + 10), (320, y + 40)], fill=CREAM)
    for dx, dy, a in [(-120, 150, 30), (120, 140, -30), (0, 100, 90)]:
        d.polygon(leaf_poly(400 + dx, dy, 160, 50, a), fill=LEAF)
    d.ellipse([200, 660, 600, 760], fill=(130, 96, 60))
    return im


def ic_mountain():
    im, d = canvas()
    d.polygon([(60, 680), (330, 200), (600, 680)], fill=(140, 150, 180))
    d.polygon([(330, 200), (270, 310), (330, 290), (390, 310)], fill=(255, 255, 255))
    d.polygon([(360, 680), (560, 330), (760, 680)], fill=(110, 120, 150))
    d.line([(60, 560), (760, 560)], fill=RED, width=14)
    f = font(F_BOLD, 64)
    d.text((80, 470), "~700 m", font=f, fill=RED)
    return im


def ic_sun_hours():
    im, d = canvas()
    d.ellipse([250, 250, 550, 550], fill=SUN)
    for a in range(0, 360, 30):
        r = math.radians(a)
        d.line([(400 + 190 * math.cos(r), 400 + 190 * math.sin(r)), (400 + 290 * math.cos(r), 400 + 290 * math.sin(r))], fill=SUN, width=30)
    return im


def ic_drop(bad=False):
    im, d = canvas()
    d.polygon([(400, 120), (580, 420), (220, 420)], fill=BLUE)
    d.ellipse([220, 300, 580, 660], fill=BLUE)
    d.ellipse([290, 420, 370, 500], fill=(190, 226, 240))
    if bad:
        d.line([(160, 160), (640, 640)], fill=RED, width=44)
    return im


def ic_roots_water():
    im, d = canvas()
    d.rectangle([0, 330, 800, 800], fill=(140, 100, 64))
    d.rectangle([0, 560, 800, 800], fill=(90, 156, 200))
    d.rectangle([370, 80, 430, 340], fill=(110, 86, 60))
    for dx in (-200, -90, 90, 200):
        d.line([(400, 340), (400 + dx, 520), (400 + dx * 1.2, 680)], fill=(90, 66, 44), width=22, joint="curve")
    return im


def ic_drip():
    im, d = canvas()
    d.rectangle([60, 300, 740, 340], fill=(40, 40, 44))
    for x in (200, 400, 600):
        d.rectangle([x - 12, 340, x + 12, 380], fill=(40, 40, 44))
        d.polygon(ellipse_poly(x, 470, 30, 46, 0), fill=BLUE)
    d.rectangle([0, 600, 800, 800], fill=(140, 100, 64))
    return im


def ic_wild_leaf():
    im, d = canvas()
    d.line([(150, 650), (650, 150)], fill=(110, 86, 60), width=28)
    for k in range(5):
        t = 0.15 + k * 0.17
        x, y = 150 + 500 * t, 650 - 500 * t
        d.polygon(leaf_poly(x - 60, y - 40, 110, 34, 40), fill=(80, 100, 60))
        d.line([(x, y), (x + 50, y + 60)], fill=(110, 86, 60), width=14)       # thorn
    for k in range(3):
        draw_olive(d, 260 + k * 150, 560 - k * 150, 22, BLACKOLIVE)
    return im


def ic_root_ball():
    im, d = canvas()
    d.rectangle([380, 100, 420, 420], fill=(110, 86, 60))
    for dx, dy, a in [(-90, 180, 30), (90, 160, -30), (0, 110, 90)]:
        d.polygon(leaf_poly(400 + dx, dy, 120, 40, a), fill=LEAF)
    d.ellipse([220, 400, 580, 700], fill=(130, 96, 60))
    for k in range(6):
        d.line([(300 + k * 40, 600), (280 + k * 44, 720)], fill=(90, 66, 44), width=8)
    d.rounded_rectangle([200, 480, 600, 560], radius=20, fill=(200, 180, 140))        # burlap band
    return im


def ic_terrace():
    im, d = canvas()
    for k in range(3):
        y = 260 + k * 160
        x = 80 + k * 140
        d.rectangle([x, y, 800, y + 160], fill=(150, 116, 76))
        for j in range(8):
            d.ellipse([x - 20, y + j * 20, x + 20, y + j * 20 + 30], fill=(156, 150, 134))
        _small_tree(d, x + 220, y)
    return im


def _small_tree(d, x, y):
    d.rectangle([x - 8, y - 70, x + 8, y], fill=(110, 86, 60))
    d.ellipse([x - 60, y - 150, x + 60, y - 50], fill=(118, 146, 92))


def ic_chill():
    im, d = canvas()
    d.rectangle([370, 140, 430, 560], fill=(200, 60, 60))
    d.ellipse([320, 520, 480, 680], fill=(200, 60, 60))
    d.rounded_rectangle([340, 80, 460, 600], radius=60, outline=DARK, width=18)
    for k in range(5):
        d.line([(470, 180 + k * 70), (520, 180 + k * 70)], fill=DARK, width=12)
    f = font(F_BOLD, 70)
    d.text((540, 300), "<10°", font=f, fill=BLUE)
    return im


def ic_years():
    im, d = canvas()
    for k, h in enumerate([120, 220, 340, 480]):
        x = 120 + k * 160
        d.rectangle([x + 50, 680 - h, x + 70, 680], fill=(110, 86, 60))
        d.ellipse([x + 60 - h * 0.35, 680 - h - h * 0.25, x + 60 + h * 0.35, 680 - h + h * 0.25], fill=(118, 146, 92))
    d.line([(60, 690), (760, 690)], fill=DARK, width=10)
    return im


def ic_graft_cut():
    im, d = canvas()
    d.rectangle([350, 420, 450, 760], fill=(110, 86, 60))
    d.polygon([(350, 420), (400, 300), (450, 420)], fill=(110, 86, 60))
    d.rectangle([380, 120, 420, 330], fill=(140, 110, 70))
    d.polygon(leaf_poly(470, 160, 120, 40, -30), fill=LEAF)
    d.rectangle([330, 360, 470, 440], fill=(240, 220, 120))               # tape
    return im


def ic_dna():
    im, d = canvas()
    for k in range(13):
        y = 100 + k * 50
        x1 = 400 + 160 * math.sin(k * 0.6)
        x2 = 400 - 160 * math.sin(k * 0.6)
        d.line([(x1, y), (x2, y)], fill=(200, 200, 200), width=10)
        d.ellipse([x1 - 24, y - 24, x1 + 24, y + 24], fill=OLIVE)
        d.ellipse([x2 - 24, y - 24, x2 + 24, y + 24], fill=RED)
    return im


def ic_map_pin():
    im, d = canvas()
    d.rounded_rectangle([80, 160, 720, 640], radius=30, fill=(232, 214, 168))
    d.line([(120, 520), (300, 400), (480, 440), (680, 260)], fill=(60, 110, 160), width=14)
    d.ellipse([300, 160, 500, 360], fill=RED)
    d.polygon([(320, 300), (480, 300), (400, 470)], fill=RED)
    d.ellipse([360, 220, 440, 300], fill=CREAM)
    return im


def ic_cutting_pot():
    im, d = canvas()
    d.polygon([(220, 420), (580, 420), (530, 740), (270, 740)], fill=(196, 110, 70))
    d.rectangle([200, 400, 600, 450], fill=(176, 96, 60))
    for x in (330, 400, 470):
        d.line([(x, 420), (x, 180)], fill=(110, 86, 60), width=14)
        d.polygon(leaf_poly(x + 30, 200, 90, 28, -40), fill=LEAF)
        d.polygon(leaf_poly(x - 30, 240, 90, 28, 40), fill=LEAF)
    for k in range(6):                                                    # mist
        d.ellipse([150 + k * 90, 80, 200 + k * 90, 130], fill=(190, 226, 240))
    return im


def ic_tomato():
    im, d = canvas()
    d.ellipse([140, 230, 660, 680], fill=(220, 60, 50))
    d.ellipse([220, 300, 320, 380], fill=(250, 140, 120))
    for a in range(0, 360, 60):
        r = math.radians(a)
        d.polygon(leaf_poly(400 + 70 * math.cos(r), 240 + 40 * math.sin(r), 120, 34, -a), fill=LEAF)
    return im


def ic_mandarin():
    im, d = canvas()
    d.ellipse([140, 220, 660, 680], fill=(244, 140, 30))
    for k in range(30):
        a = k * 2.4
        r = 60 + (k * 37) % 180
        x, y = 400 + r * math.cos(a), 450 + r * math.sin(a) * 0.85
        d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(230, 120, 20))
    d.polygon(leaf_poly(470, 200, 200, 70, -20), fill=LEAF)
    d.rectangle([390, 190, 410, 240], fill=(110, 86, 60))
    return im


def ic_scale_heavy():
    im, d = canvas()
    d.rectangle([180, 560, 620, 640], fill=(150, 160, 170))
    d.rounded_rectangle([140, 640, 660, 720], radius=20, fill=(110, 120, 130))
    d.ellipse([260, 300, 540, 580], fill=(244, 140, 30))
    f = font(F_BOLD, 80)
    d.text((400 - f.getlength("AĞIR") / 2, 150), "AĞIR", font=f, fill=RED)
    return im


def ic_bowl_water():
    im, d = canvas()
    d.chord([120, 260, 680, 720], 0, 180, fill=(220, 220, 228))
    d.ellipse([140, 440, 660, 540], fill=(150, 200, 226))
    for k in range(12):
        x, y = 220 + (k % 6) * 72, 470 + (k // 6) * 30
        d.ellipse([x - 16, y - 20, x + 16, y + 20], fill=(200, 30, 60))
    return im


def ic_tap():
    im, d = canvas()
    d.rounded_rectangle([200, 120, 520, 200], radius=30, fill=(170, 176, 184))
    d.rounded_rectangle([440, 160, 520, 320], radius=30, fill=(170, 176, 184))
    for k in range(4):
        d.line([(470 + k * 8 - 12, 340), (470 + k * 8 - 12, 520)], fill=BLUE, width=10)
    d.ellipse([300, 480, 560, 700], fill=(220, 60, 50))
    d.polygon(leaf_poly(430, 480, 100, 30, 0), fill=LEAF)
    return im


def ic_veg_basket():
    im, d = canvas()
    d.polygon([(120, 420), (680, 420), (600, 720), (200, 720)], fill=(196, 150, 90))
    for k in range(4):
        d.line([(150 + k * 10, 470 + k * 60), (650 - k * 10, 470 + k * 60)], fill=(170, 124, 70), width=8)
    d.ellipse([170, 260, 380, 460], fill=(240, 240, 226))                 # cauliflower
    for k in range(8):
        d.ellipse([190 + (k % 4) * 45, 280 + (k // 4) * 60, 250 + (k % 4) * 45, 340 + (k // 4) * 60], fill=(250, 248, 236))
    d.polygon([(430, 440), (470, 160), (520, 160), (540, 440)], fill=(240, 236, 220))   # leek
    d.polygon([(470, 160), (420, 40), (520, 160)], fill=LEAF)
    d.polygon([(520, 160), (600, 50), (540, 200)], fill=LEAF)
    d.polygon([(560, 440), (620, 300), (680, 440)], fill=(240, 120, 40))  # carrot
    return im


def ic_label_gi():
    im, d = canvas()
    d.ellipse([160, 160, 640, 640], fill=(200, 40, 50))
    d.ellipse([200, 200, 600, 600], fill=CREAM)
    f = font(F_BOLD, 54)
    for k, t in enumerate(["COĞRAFİ", "İŞARET"]):
        d.text((400 - f.getlength(t) / 2, 330 + k * 72), t, font=f, fill=(200, 40, 50))
    return im


def ic_silver_leaf():
    im, d = canvas()
    d.polygon(leaf_poly(400, 400, 600, 150, 30), fill=(92, 128, 60))
    d.polygon(leaf_poly(430, 440, 520, 110, 30), fill=(200, 210, 200))
    for k in range(20):
        x, y = 280 + k * 14, 520 - k * 9
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(240, 244, 240))
    return im


def ic_glass_taste():
    im, d = canvas()
    d.polygon([(260, 200), (540, 200), (500, 640), (300, 640)], fill=(40, 70, 130))
    d.polygon([(280, 480), (520, 480), (500, 640), (300, 640)], fill=(170, 160, 40))
    d.ellipse([300, 610, 500, 680], fill=(30, 50, 100))
    return im


def ic_cloudy():
    im, d = canvas()
    d.rounded_rectangle([280, 120, 520, 720], radius=40, fill=(232, 236, 230))
    d.rectangle([280, 300, 520, 700], fill=(196, 186, 80))
    rnd = random.Random(3)
    for _ in range(60):
        x, y = rnd.uniform(300, 500), rnd.uniform(320, 690)
        d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(170, 160, 70))
    d.rectangle([280, 640, 520, 700], fill=(140, 120, 60))
    return im


def ic_pot_tree():
    im, d = canvas()
    d.polygon([(220, 480), (580, 480), (530, 760), (270, 760)], fill=(196, 110, 70))
    d.rectangle([380, 220, 420, 480], fill=(110, 86, 60))
    for k in range(9):
        cx, cy = 400 + 140 * math.cos(k * 0.7), 200 + 90 * math.sin(k * 0.7)
        d.ellipse([cx - 80, cy - 55, cx + 80, cy + 55], fill=(118, 146, 92))
    for k in range(4):
        draw_olive(d, 330 + k * 50, 230 + (k % 2) * 40, 16, BLACKOLIVE)
    return im


def ic_pruning():
    im, d = canvas()
    d.line([(150, 650), (400, 400), (600, 250)], fill=(110, 86, 60), width=34)
    d.line([(400, 400), (560, 520)], fill=(110, 86, 60), width=24)
    d.line([(520, 470), (620, 590)], fill=RED, width=10)
    d.ellipse([560, 120, 720, 280], outline=(170, 176, 184), width=26)
    d.line([(600, 260), (470, 420)], fill=(170, 176, 184), width=26)
    return im


def ic_bucket_blue():
    im, d = canvas()
    d.polygon([(220, 300), (580, 300), (540, 700), (260, 700)], fill=(170, 176, 184))
    d.ellipse([220, 260, 580, 340], fill=(70, 140, 200))
    d.arc([220, 100, 580, 420], 200, 340, fill=DARK, width=14)
    return im


def ic_ladybug():
    im, d = canvas()
    d.ellipse([170, 200, 630, 660], fill=(220, 40, 40))
    d.chord([270, 120, 530, 360], 180, 360, fill=(30, 30, 30))
    d.line([(400, 230), (400, 660)], fill=(30, 30, 30), width=14)
    for x, y in [(290, 340), (510, 340), (270, 500), (530, 500), (360, 580), (440, 580)]:
        d.ellipse([x - 40, y - 40, x + 40, y + 40], fill=(30, 30, 30))
    for s in (-1, 1):
        d.line([(400 + s * 60, 150), (400 + s * 120, 70)], fill=(30, 30, 30), width=10)
    return im
