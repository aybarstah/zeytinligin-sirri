"""Backgrounds, props and cards for Season 1 episodes 6-20."""
import math
import random
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont
from brand import *
from story import vgrad, _tree, W, H, BGW
from make_main import LORA_I, notebook_page, canvas

INK = (40, 40, 70)


def lora(size):
    f = ImageFont.truetype(LORA_I, size)
    try:
        f.set_variation_by_name("Bold Italic")
    except Exception:
        pass
    return f


# ------------------------------------------------------------------ backgrounds
@lru_cache(maxsize=2)
def bg_coffee():
    rnd = random.Random(31)
    im = vgrad(BGW, H, (196, 150, 100), (150, 104, 64))
    d = ImageDraw.Draw(im)
    for x in range(0, BGW, 90):                       # wood panelling
        d.line([(x, 0), (x, 1300)], fill=(170, 124, 80), width=6)
    d.rounded_rectangle([640, 260, 1060, 760], radius=20, fill=(170, 214, 236), outline=(110, 74, 44), width=26)
    d.line([(850, 260), (850, 760)], fill=(110, 74, 44), width=18)
    d.rectangle([60, 520, 520, 545], fill=(110, 74, 44))           # shelf
    for k in range(6):                                              # tea glasses
        x = 90 + k * 70
        d.polygon([(x, 440), (x + 40, 440), (x + 34, 520), (x + 6, 520)], fill=(190, 60, 40))
        d.rectangle([x - 4, 436, x + 44, 446], fill=(220, 220, 220))
    d.ellipse([140, 230, 300, 390], fill=(240, 236, 220), outline=(90, 60, 36), width=10)   # clock
    d.line([(220, 310), (220, 250)], fill=(40, 30, 20), width=8)
    d.line([(220, 310), (265, 310)], fill=(40, 30, 20), width=8)
    d.rectangle([0, 1300, BGW, H], fill=(120, 80, 50))               # floor
    for y in range(1330, H, 60):
        d.line([(0, y), (BGW, y)], fill=(104, 68, 42), width=4)
    for x0 in (140, 820):                                           # tables with tavla / tea
        d.rectangle([x0, 1240, x0 + 260, 1270], fill=(90, 60, 36))
        d.rectangle([x0 + 120, 1270, x0 + 140, 1440], fill=(90, 60, 36))
        d.rectangle([x0 + 40, 1200, x0 + 200, 1240], fill=(150, 90, 50))
        d.line([(x0 + 120, 1200), (x0 + 120, 1240)], fill=(80, 50, 30), width=4)
    return im


@lru_cache(maxsize=2)
def bg_depot():
    rnd = random.Random(41)
    im = vgrad(BGW, H, (70, 56, 44), (40, 32, 26))
    d = ImageDraw.Draw(im)
    for x in range(0, BGW, 110):
        d.line([(x, 0), (x, 1400)], fill=(84, 66, 50), width=8)
    for y in (420, 760, 1100):                                       # shelves
        d.rectangle([40, y, 1160, y + 26], fill=(110, 80, 52))
        for k in range(11):
            x = 70 + k * 100 + rnd.uniform(-10, 10)
            if rnd.random() < 0.5:
                d.rounded_rectangle([x, y - 150, x + 70, y], radius=10, fill=(150, 156, 160))       # tin
                d.rectangle([x, y - 110, x + 70, y - 60], fill=(70, 110, 50))
            else:
                d.rounded_rectangle([x + 10, y - 170, x + 60, y], radius=14, fill=(40, 70, 40))   # bottle
                d.rectangle([x + 24, y - 200, x + 46, y - 165], fill=(40, 70, 40))
    beam = Image.new("RGBA", im.size, (0, 0, 0, 0))                   # dusty light beam
    ImageDraw.Draw(beam).polygon([(760, 0), (900, 0), (700, H), (300, H)], fill=(255, 230, 170, 45))
    im.alpha_composite(beam)
    d = ImageDraw.Draw(im)
    for k in range(60):
        x, y = rnd.uniform(400, 900), rnd.uniform(0, H)
        d.ellipse([x, y, x + 4, y + 4], fill=(255, 240, 200, 160))
    d.rectangle([0, 1450, BGW, H], fill=(60, 46, 34))
    return im


@lru_cache(maxsize=2)
def bg_lab():
    im = vgrad(BGW, H, (236, 242, 244), (210, 222, 226))
    d = ImageDraw.Draw(im)
    for y in range(820, 1330, 60):
        for x in range(0, BGW, 60):
            d.rectangle([x + 2, y + 2, x + 58, y + 58], fill=(226, 236, 240))
    d.rectangle([60, 600, 1140, 626], fill=(160, 170, 176))
    cols = [(200, 180, 60), (120, 180, 90), (220, 160, 60), (200, 180, 60)]
    for k in range(8):
        x = 100 + k * 130
        c = cols[k % 4]
        d.polygon([(x, 440), (x + 40, 440), (x + 40, 500), (x + 80, 600), (x - 40, 600), (x, 500)], fill=(220, 236, 242), outline=(150, 170, 180), width=4)
        d.polygon([(x - 24, 560), (x + 64, 560), (x + 80, 600), (x - 40, 600)], fill=c)
    d.rectangle([0, 1330, BGW, 1420], fill=(190, 200, 206))
    d.rectangle([0, 1420, BGW, H], fill=(150, 160, 168))
    d.rounded_rectangle([760, 1180, 1100, 1330], radius=14, fill=(60, 70, 80))   # analyser
    d.rectangle([790, 1210, 960, 1290], fill=(120, 220, 160))
    return im


@lru_cache(maxsize=2)
def bg_hollow():
    im = Image.new("RGBA", (BGW, H), (30, 20, 14, 255))
    d = ImageDraw.Draw(im)
    for k in range(18):                                              # wood rings
        r = 1400 - k * 70
        d.ellipse([BGW / 2 - r, 900 - r * 1.3, BGW / 2 + r, 900 + r * 1.3], outline=(60 + k * 2, 42 + k, 28), width=26)
    d.ellipse([440, 120, 760, 360], fill=(120, 150, 190))             # opening to the sky
    d.ellipse([470, 140, 730, 340], fill=(170, 200, 230))
    light = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(light).polygon([(470, 300), (730, 300), (900, H), (300, H)], fill=(255, 240, 200, 40))
    im.alpha_composite(light)
    d = ImageDraw.Draw(im)
    rnd = random.Random(2)
    for k in range(12):                                              # roots
        x = rnd.uniform(0, BGW)
        d.line([(x, H), (x + rnd.uniform(-200, 200), 1500), (x + rnd.uniform(-300, 300), 1300)], fill=(70, 50, 34), width=30, joint="curve")
    d.ellipse([200, 1580, 1000, 1800], fill=(50, 36, 24))
    return im


@lru_cache(maxsize=2)
def bg_square():
    rnd = random.Random(51)
    im = vgrad(BGW, H, (170, 214, 236), (255, 238, 205))
    d = ImageDraw.Draw(im)
    for x, w, h, c in [(0, 300, 520, (236, 226, 206)), (300, 260, 600, (226, 210, 186)), (860, 340, 560, (236, 222, 200))]:
        d.rectangle([x, 1300 - h, x + w, 1300], fill=c)
        d.polygon([(x - 20, 1300 - h), (x + w / 2, 1300 - h - 120), (x + w + 20, 1300 - h)], fill=(176, 92, 64))
        for k in range(2):
            d.rectangle([x + 40 + k * (w - 140), 1300 - h + 90, x + 100 + k * (w - 140), 1300 - h + 190], fill=(120, 160, 190))
    d.rectangle([600, 760, 650, 1300], fill=(120, 90, 60))           # plane tree
    for k in range(14):
        cx, cy, r = 625 + rnd.uniform(-220, 220), 640 + rnd.uniform(-160, 120), rnd.uniform(90, 150)
        d.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7], fill=(110, 150, 80))
    d.rectangle([0, 1300, BGW, H], fill=(196, 186, 170))              # cobbles
    for k in range(260):
        x, y = rnd.uniform(0, BGW), rnd.uniform(1310, H)
        d.ellipse([x, y, x + 50, y + 26], outline=(170, 160, 146), width=3)
    d.rounded_rectangle([60, 1200, 300, 1330], radius=10, fill=(200, 196, 186))  # fountain
    d.rectangle([160, 1160, 200, 1200], fill=(150, 150, 150))
    for k in range(9):                                                # villagers (silhouettes)
        x = 330 + k * 75 + rnd.uniform(-10, 10)
        c = [(80, 70, 90), (120, 70, 60), (60, 80, 100), (100, 90, 60)][k % 4]
        d.ellipse([x - 26, 1150, x + 26, 1202], fill=(60, 50, 50))
        d.rounded_rectangle([x - 34, 1196, x + 34, 1330], radius=24, fill=c)
    return im


# ------------------------------------------------------------------ props
def excavator():
    im = Image.new("RGBA", (900, 700), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([200, 560, 760, 680], radius=60, fill=(50, 50, 54))
    for k in range(6):
        d.ellipse([230 + k * 88, 590, 300 + k * 88, 660], fill=(90, 90, 96))
    d.rounded_rectangle([260, 330, 700, 570], radius=30, fill=(240, 180, 30))
    d.rounded_rectangle([480, 200, 690, 400], radius=20, fill=(240, 180, 30))
    d.rounded_rectangle([510, 230, 660, 340], radius=10, fill=(170, 210, 230))
    d.line([(300, 380), (160, 120), (40, 300)], fill=(240, 180, 30), width=60, joint="curve")
    d.polygon([(0, 300), (110, 280), (100, 420), (10, 400)], fill=(80, 80, 86))
    return im


def tin_box(open_=True):
    im, d = canvas(600)
    d.ellipse([40, 420, 560, 560], fill=(70, 50, 34))
    d.rounded_rectangle([140, 300, 460, 500], radius=16, fill=(150, 140, 120), outline=(110, 100, 86), width=8)
    if open_:
        d.polygon([(140, 300), (460, 300), (500, 180), (180, 180)], fill=(170, 160, 140))
    d.ellipse([260, 380, 340, 440], fill=(110, 80, 50))
    return im


def notebook_cover(title=("MÜHENDİSİN", "DEFTERİ")):
    im = Image.new("RGBA", (620, 820), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([20, 20, 600, 800], radius=30, fill=(31, 70, 30))
    d.rectangle([20, 20, 90, 800], fill=(22, 50, 20))
    d.rectangle([500, 20, 530, 820], fill=RED)
    d.rounded_rectangle([140, 120, 520, 300], radius=16, fill=CREAM)
    draw_olive(d, 280, 210, 50, (128, 158, 52))
    d.polygon(leaf_poly(370, 180, 110, 36, -30), fill=LEAF)
    f = font(F_BOLD, 64)
    for k, t in enumerate(title):
        d.text((330 - f.getlength(t) / 2, 380 + k * 90), t, font=f, fill=SUN if k else CREAM)
    f2 = lora(40)
    d.text((330 - f2.getlength("yazan: torun") / 2, 620), "yazan: torun", font=f2, fill=(200, 210, 190))
    return im


def report():
    im = Image.new("RGBA", (760, 760), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([30, 30, 730, 740], fill=(250, 250, 248), outline=(200, 200, 200), width=4)
    f, fb = font(F_MED, 34), font(F_BOLD, 44)
    d.text((70, 70), "ANALİZ RAPORU", font=fb, fill=DARK)
    d.line([(70, 135), (690, 135)], fill=(200, 200, 200), width=4)
    rows = [("Numune", "2026 hasadı"), ("Serbest asitlik", "% 0,3"), ("Peroksit", "Uygun"), ("Sınıf", "Natürel sızma")]
    for k, (a, b) in enumerate(rows):
        y = 170 + k * 90
        d.text((70, y), a, font=f, fill=(90, 90, 90))
        d.text((380, y), b, font=fb if k == 1 else f, fill=OLIVE if k == 1 else DARK)
    d.ellipse([480, 540, 680, 700], outline=RED, width=10)
    d.text((515, 595), "UYGUN", font=font(F_BOLD, 40), fill=RED)
    return im


def old_photo():
    im = Image.new("RGBA", (760, 820), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([20, 20, 740, 800], fill=(244, 236, 214))
    d.rectangle([60, 60, 700, 660], fill=(176, 150, 112))
    d.rectangle([60, 460, 700, 660], fill=(150, 124, 90))
    d.polygon([(250, 660), (290, 360), (260, 220), (420, 220), (380, 360), (430, 660)], fill=(110, 86, 60))   # tree
    for x, y, r in [(250, 170, 120), (420, 160, 130), (340, 100, 120)]:
        d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=(130, 116, 84))
    d.ellipse([520, 330, 590, 400], fill=(220, 206, 180))             # dede
    d.rectangle([505, 300, 605, 340], fill=(90, 74, 56))
    d.rounded_rectangle([500, 400, 610, 620], radius=30, fill=(110, 92, 70))
    d.text((80, 690), "Ulu ile, 1987", font=lora(56), fill=(90, 70, 50))
    return im.rotate(-4, resample=Image.BICUBIC, expand=True)


def found_page():
    return notebook_page(["ULU — ANIT AĞAÇ", "Tescil başvurusu", "yapıldı, 1987"], "— Deden")


def letter():
    return notebook_page(["Torunum, bu defter", "artık senin.", "Ağaçlara iyi bak."], "— Deden")


def bottle_label():
    im = Image.new("RGBA", (760, 900), (0, 0, 0, 0))
    b = fit(icon_bottle(), width=520)
    im.alpha_composite(b, (120, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([200, 420, 560, 720], radius=24, fill=CREAM, outline=OLIVE, width=8)
    f = font(F_BOLD, 40)
    for k, t in enumerate(["MÜHENDİSİN", "DEFTERİ"]):
        d.text((380 - f.getlength(t) / 2, 450 + k * 52), t, font=f, fill=DARK)
    draw_olive(d, 380, 600, 34, (128, 158, 52))
    f2 = font(F_MED, 28)
    d.text((380 - f2.getlength("Natürel Sızma · 2026") / 2, 660), "Natürel Sızma · 2026", font=f2, fill=OLIVE)
    return im


def new_map():
    pw, ph = 860, 620
    im = Image.new("RGBA", (pw + 40, ph + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([24, 30, pw + 24, ph + 30], fill=(0, 0, 0, 60))
    d.rectangle([10, 10, pw + 10, ph + 10], fill=(232, 214, 168))
    d.line([(60, 500), (200, 380), (360, 420), (520, 300), (700, 220)], fill=(60, 110, 160), width=10, joint="curve")  # river
    for x, y in [(120, 200), (300, 160), (480, 470), (640, 420)]:
        d.polygon([(x, y), (x + 50, y - 90), (x + 100, y)], fill=(150, 140, 110))
    for (x0, y0), (x1, y1) in zip([(150, 520), (330, 470), (500, 380), (640, 300)], [(330, 470), (500, 380), (640, 300), (760, 160)]):
        for t in range(0, 10, 2):
            a, b = t / 10, (t + 1) / 10
            d.line([(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b)], fill=(150, 40, 40), width=8)
    d.line([(740, 130), (790, 180)], fill=RED, width=14)
    d.line([(790, 130), (740, 180)], fill=RED, width=14)
    d.text((40, 30), "Kayıp Fidan", font=lora(60), fill=(80, 50, 30))
    return im.rotate(2, resample=Image.BICUBIC, expand=True)


# ------------------------------------------------------------------ step icons
def ic_seed():
    im, d = canvas()
    d.rectangle([0, 560, 800, 800], fill=(140, 110, 76))
    d.ellipse([340, 600, 460, 660], fill=(170, 130, 90))
    d.line([(400, 600), (400, 420)], fill=(110, 150, 70), width=12)
    d.polygon(leaf_poly(450, 430, 110, 36, -20), fill=(130, 170, 80))
    d.polygon(leaf_poly(350, 450, 100, 34, 200), fill=(130, 170, 80))
    d.line([(150, 150), (650, 650)], fill=RED, width=0)
    d.text((160, 160), "7-8 yıl?", font=font(F_BOLD, 90), fill=RED)
    return im


def ic_cutting():
    im, d = canvas()
    d.polygon([(250, 480), (550, 480), (510, 720), (290, 720)], fill=(190, 110, 70))
    d.rectangle([240, 460, 560, 500], fill=(170, 96, 60))
    d.line([(400, 470), (400, 160)], fill=(110, 84, 56), width=16)
    for k, (y, side) in enumerate([(220, 1), (290, -1), (360, 1)]):
        d.polygon(leaf_poly(400 + side * 70, y, 130, 40, 20 * side), fill=(110, 140, 80))
    for k in range(5):
        d.line([(400, 470), (330 + k * 35, 560)], fill=(240, 230, 210), width=6)
    return im


def ic_graft():
    im, d = canvas()
    d.rectangle([340, 360, 460, 760], fill=(110, 84, 56))
    d.rectangle([360, 140, 440, 380], fill=(140, 120, 80))
    d.rounded_rectangle([320, 330, 480, 420], radius=16, fill=(230, 220, 120))
    for y in (350, 375, 400):
        d.line([(320, y), (480, y)], fill=(190, 180, 80), width=6)
    for k, (y, side) in enumerate([(170, 1), (240, -1)]):
        d.polygon(leaf_poly(400 + side * 80, y, 140, 44, 20 * side), fill=(110, 140, 80))
    return im


def ic_flask(text=None):
    im, d = canvas()
    d.polygon([(330, 100), (470, 100), (470, 330), (640, 680), (160, 680), (330, 330)], fill=(220, 236, 242), outline=DARK, width=14)
    d.polygon([(250, 480), (550, 480), (630, 670), (170, 670)], fill=(200, 180, 60))
    if text:
        f = font(F_BOLD, 110)
        d.text((400 - f.getlength(text) / 2, 180), text, font=f, fill=RED)
    return im


def ic_big_text(t1, t2=""):
    im, d = canvas()
    d.rounded_rectangle([60, 160, 740, 640], radius=60, fill=OLIVE)
    f = font(F_BOLD, 190)
    d.text((400 - f.getlength(t1) / 2, 230), t1, font=f, fill=SUN)
    if t2:
        f2 = font(F_MED, 54)
        d.text((400 - f2.getlength(t2) / 2, 500), t2, font=f2, fill=CREAM)
    return im


def ic_sack_bad():
    im, d = canvas()
    d.polygon([(200, 700), (180, 300), (300, 200), (500, 200), (620, 300), (600, 700)], fill=(200, 170, 120))
    d.line([(300, 200), (500, 200)], fill=(150, 120, 80), width=20)
    for k, (x, y) in enumerate([(320, 640), (420, 660), (520, 630)]):
        draw_olive(d, x, y, 40, BLACKOLIVE)
        d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=(20, 10, 10))
    for k in range(3):
        d.arc([300 + k * 80, 80, 380 + k * 80, 180], 200, 340, fill=(160, 160, 160), width=10)
    return im


def ic_tree_trap():
    im, d = canvas()
    d.rectangle([370, 380, 430, 760], fill=(110, 84, 56))
    for x, y, r in [(250, 300, 150), (550, 300, 150), (400, 200, 150)]:
        d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=(118, 140, 96))
    d.line([(560, 360), (560, 420)], fill=(90, 90, 90), width=4)
    d.rounded_rectangle([520, 420, 600, 540], radius=6, fill=(250, 220, 40))
    d.ellipse([640, 60, 760, 180], fill=SUN)
    f = font(F_BOLD, 54)
    d.text((80, 640), "göz hizası", font=f, fill=DARK)
    return im


def ic_smell():
    im, d = canvas()
    d.polygon([(260, 360), (540, 360), (500, 640), (300, 640)], fill=(40, 110, 200, 200))
    d.ellipse([260, 330, 540, 390], fill=(80, 150, 220))
    d.ellipse([290, 345, 510, 380], fill=(200, 190, 60))
    for k in range(3):
        x = 330 + k * 70
        d.arc([x - 30, 160, x + 30, 330], 100, 260, fill=(120, 170, 90), width=12)
    return im


def ic_sip():
    im, d = canvas()
    d.ellipse([200, 260, 600, 540], fill=(200, 180, 60))
    d.ellipse([250, 300, 550, 500], fill=(220, 200, 80))
    d.rounded_rectangle([560, 360, 760, 440], radius=30, fill=(180, 180, 186))
    f = font(F_BOLD, 60)
    d.text((400 - f.getlength("sssp!") / 2, 600), "sssp!", font=f, fill=DARK)
    return im


def ic_paste():
    im, d = canvas()
    d.rectangle([340, 200, 460, 760], fill=(110, 84, 56))
    d.ellipse([330, 180, 470, 260], fill=(170, 140, 100))
    d.ellipse([340, 190, 460, 250], fill=(80, 60, 50))
    d.line([(600, 80), (470, 210)], fill=(150, 100, 60), width=26)
    d.rounded_rectangle([430, 190, 500, 250], radius=10, fill=(60, 60, 60))
    d.rounded_rectangle([540, 560, 720, 720], radius=20, fill=(60, 90, 140))
    d.text((560, 610), "macun", font=font(F_BOLD, 38), fill=CREAM)
    return im


def ic_soil_pupa():
    im, d = canvas()
    d.rectangle([0, 260, 800, 800], fill=(120, 90, 60))
    d.rectangle([0, 200, 800, 260], fill=(110, 150, 80))
    rnd = random.Random(3)
    for k in range(9):
        x, y = rnd.uniform(100, 700), rnd.uniform(380, 700)
        d.ellipse([x - 26, y - 14, x + 26, y + 14], fill=(200, 150, 80))
        d.line([(x - 18, y), (x + 18, y)], fill=(160, 110, 60), width=4)
    d.text((120, 60), "toprakta kışlar", font=font(F_BOLD, 64), fill=DARK)
    return im


def ic_hoe():
    im, d = canvas()
    d.rectangle([0, 560, 800, 800], fill=(120, 90, 60))
    for k in range(6):
        d.arc([60 + k * 120, 520, 180 + k * 120, 620], 180, 360, fill=(100, 72, 46), width=12)
    d.line([(650, 80), (380, 520)], fill=(150, 100, 60), width=30)
    d.polygon([(330, 500), (450, 470), (430, 600), (310, 610)], fill=(140, 140, 146))
    return im


def ic_tape():
    im, d = canvas()
    d.rectangle([250, 100, 550, 760], fill=(110, 84, 56))
    for k in range(8):
        x = 260 + k * 38
        d.line([(x, 100), (x + 10, 760)], fill=(90, 66, 44), width=6)
    d.ellipse([200, 380, 600, 480], outline=(250, 220, 40), width=26)
    for k in range(12):
        a = math.radians(200 + k * 12)
        x, y = 400 + 200 * math.cos(a), 430 + 50 * math.sin(a)
        d.line([(x, y - 12), (x, y + 12)], fill=DARK, width=4)
    d.text((80, 600), "gövde çevresi", font=font(F_BOLD, 60), fill=CREAM, stroke_width=4, stroke_fill=DARK)
    return im
