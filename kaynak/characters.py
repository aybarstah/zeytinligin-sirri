"""Recurring cast: Zeynep (ziraat mühendisi) and Zeyto (talking olive). Vector-drawn with PIL, 2x supersampled."""
import math
from functools import lru_cache
from PIL import Image, ImageDraw
from brand import OLIVE, DARK, CREAM, SUN, RED, LEAF, LEAF2, BROWN, ellipse_poly, leaf_poly, font, F_BOLD

SKIN = (232, 176, 138)
SKIN_SH = (212, 150, 112)
HAIR = (58, 38, 24)
SHIRT = (246, 243, 236)
JEANS = (59, 91, 140)
BOOT = (92, 60, 36)
HAT = (232, 199, 122)
HAT_SH = (205, 168, 92)
VEST = (78, 107, 46)
VEST_SH = (60, 86, 34)
CHEEK = (240, 130, 120, 110)
MOUTH = (150, 40, 50)

ZW, ZH = 800, 1100  # Zeynep canvas (feet at bottom); body centred at x=ZCX
ZCX = 300
SS = 2


def _limb(d, p0, p1, w, col):
    d.line([p0, p1], fill=col, width=int(w))
    for (x, y) in (p0, p1):
        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=col)


@lru_cache(maxsize=512)
def zeynep(mouth=0, blink=False, arm=70, look=0):
    """mouth: 0 closed smile, 1 open, 2 wide open. arm: right arm angle in degrees (90 = straight down, 0 = horizontal, negative = up)."""
    s = SS
    im = Image.new("RGBA", (ZW * s, ZH * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    S = lambda *v: [x * s for x in v]

    # hair behind (ponytail over shoulder)
    d.polygon([(x * s, y * s) for x, y in ellipse_poly(372, 360, 44, 130, -12)], fill=HAIR)
    # legs + boots
    for x0 in (212, 318):
        d.rounded_rectangle(S(x0, 690, x0 + 72, 1010), radius=20 * s, fill=JEANS)
        d.rounded_rectangle(S(x0 - 8, 985, x0 + 86, 1085), radius=26 * s, fill=BOOT)
        d.rectangle(S(x0 - 8, 1060, x0 + 86, 1085), fill=(70, 44, 26))
    # belt line
    d.rectangle(S(200, 680, 400, 712), fill=(70, 44, 26))
    # torso (shirt)
    d.rounded_rectangle(S(170, 385, 430, 715), radius=70 * s, fill=SHIRT)
    # vest panels
    d.polygon([(x * s, y * s) for x, y in [(175, 450), (240, 395), (282, 405), (270, 712), (175, 712)]], fill=VEST)
    d.polygon([(x * s, y * s) for x, y in [(425, 450), (360, 395), (318, 405), (330, 712), (425, 712)]], fill=VEST)
    d.rounded_rectangle(S(190, 560, 252, 618), radius=8 * s, fill=VEST_SH)
    d.rounded_rectangle(S(348, 560, 410, 618), radius=8 * s, fill=VEST_SH)
    # badge
    d.rounded_rectangle(S(346, 460, 404, 512), radius=8 * s, fill=SUN)
    d.ellipse(S(366, 474, 384, 492), fill=DARK)
    # collar
    d.polygon([(x * s, y * s) for x, y in [(262, 388), (300, 430), (338, 388), (320, 380), (300, 405), (280, 380)]], fill=(225, 222, 214))
    # neck
    d.rounded_rectangle(S(274, 330, 326, 400), radius=14 * s, fill=SKIN_SH)

    # left arm holding clipboard
    _limb(d, (190 * s, 430 * s), (175 * s, 560 * s), 62 * s, SHIRT)
    _limb(d, (175 * s, 560 * s), (225 * s, 640 * s), 54 * s, SHIRT)
    d.rounded_rectangle(S(150, 560, 270, 720), radius=10 * s, fill=BROWN)
    d.rectangle(S(162, 578, 258, 708), fill=(252, 252, 248))
    for k in range(4):
        d.line(S(174, 605 + k * 25, 246 - (k % 2) * 25, 605 + k * 25), fill=(170, 170, 170), width=5 * s)
    d.rounded_rectangle(S(190, 552, 230, 572), radius=4 * s, fill=(160, 160, 160))
    d.ellipse(S(206, 625, 246, 665), fill=SKIN)

    # right arm (articulated)
    sh = (410, 430)
    a = math.radians(arm)
    el = (sh[0] + math.cos(a) * 125, sh[1] + math.sin(a) * 125)
    a2 = math.radians(arm - (25 if arm < 60 else 0))
    hd = (el[0] + math.cos(a2) * 120, el[1] + math.sin(a2) * 120)
    _limb(d, (sh[0] * s, sh[1] * s), (el[0] * s, el[1] * s), 62 * s, SHIRT)
    _limb(d, (el[0] * s, el[1] * s), (hd[0] * s, hd[1] * s), 54 * s, SHIRT)
    d.ellipse([(hd[0] - 22) * s, (hd[1] - 22) * s, (hd[0] + 22) * s, (hd[1] + 22) * s], fill=SKIN)
    if arm < 60:  # pointing finger
        f = (hd[0] + math.cos(a2) * 40, hd[1] + math.sin(a2) * 40)
        d.line([(hd[0] * s, hd[1] * s), (f[0] * s, f[1] * s)], fill=SKIN, width=14 * s)
        d.ellipse([(f[0] - 7) * s, (f[1] - 7) * s, (f[0] + 7) * s, (f[1] + 7) * s], fill=SKIN)

    # head
    cx, cy = 300, 255
    d.ellipse(S(cx - 104, cy - 112, cx + 104, cy + 104), fill=SKIN)
    d.ellipse(S(cx - 122, cy - 8, cx - 88, cy + 40), fill=SKIN)
    d.ellipse(S(cx + 88, cy - 8, cx + 122, cy + 40), fill=SKIN)
    # fringe
    d.chord(S(cx - 110, cy - 128, cx + 110, cy + 40), 180, 360, fill=HAIR)
    d.polygon([(x * s, y * s) for x, y in [(cx - 108, cy - 40), (cx - 60, cy - 70), (cx - 20, cy - 30), (cx + 30, cy - 72), (cx + 108, cy - 40), (cx + 108, cy - 80), (cx - 108, cy - 80)]], fill=HAIR)
    # hat
    d.ellipse(S(cx - 190, cy - 118, cx + 190, cy - 52), fill=HAT_SH)
    d.ellipse(S(cx - 186, cy - 124, cx + 186, cy - 60), fill=HAT)
    d.rounded_rectangle(S(cx - 92, cy - 200, cx + 92, cy - 90), radius=40 * s, fill=HAT)
    d.rectangle(S(cx - 92, cy - 128, cx + 92, cy - 102), fill=OLIVE)
    d.polygon([(x * s, y * s) for x, y in leaf_poly(cx + 70, cy - 132, 70, 22, -40)], fill=LEAF2)
    # brows
    d.arc(S(cx - 70, cy - 38, cx - 22, cy - 8), 200, 330, fill=HAIR, width=7 * s)
    d.arc(S(cx + 22, cy - 38, cx + 70, cy - 8), 210, 340, fill=HAIR, width=7 * s)
    # eyes
    for ex in (cx - 42, cx + 42):
        if blink:
            d.arc(S(ex - 18, cy - 4, ex + 18, cy + 22), 200, 340, fill=HAIR, width=6 * s)
        else:
            d.ellipse(S(ex - 15 + look, cy - 8, ex + 15 + look, cy + 26), fill=(40, 28, 22))
            d.ellipse(S(ex - 6 + look, cy - 2, ex + 3 + look, cy + 8), fill=(255, 255, 255))
    # cheeks + nose
    ch = Image.new("RGBA", im.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(ch)
    cd.ellipse(S(cx - 84, cy + 28, cx - 48, cy + 50), fill=CHEEK)
    cd.ellipse(S(cx + 48, cy + 28, cx + 84, cy + 50), fill=CHEEK)
    im.alpha_composite(ch)
    d.arc(S(cx - 10, cy + 20, cx + 10, cy + 40), 20, 160, fill=SKIN_SH, width=5 * s)
    # mouth
    my = cy + 58
    if mouth == 0:
        d.arc(S(cx - 30, my - 22, cx + 30, my + 12), 20, 160, fill=MOUTH, width=7 * s)
    else:
        h = 20 if mouth == 1 else 32
        d.chord(S(cx - 28, my - 14, cx + 28, my + h), 0, 180, fill=MOUTH)
        d.ellipse(S(cx - 14, my + h * 0.35, cx + 14, my + h + 2), fill=(230, 110, 110))
        d.line(S(cx - 26, my + 2, cx + 26, my + 2), fill=MOUTH, width=4 * s)
    return im.resize((ZW, ZH), Image.LANCZOS)


YW, YH = 420, 500  # Zeyto canvas


@lru_cache(maxsize=512)
def zeyto(color=(128, 158, 52), mouth=0, blink=False, mood="happy", look=0, arms=0):
    """Talking olive. mood: happy | worried | wow. arms: 0 down, 1 up (excited)."""
    s = SS
    im = Image.new("RGBA", (YW * s, YH * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    S = lambda *v: [x * s for x in v]
    cx, cy = 210, 260
    dark = tuple(max(0, c - 30) for c in color)
    # legs
    for lx in (cx - 50, cx + 50):
        d.line(S(lx, cy + 150, lx, cy + 215), fill=DARK, width=12 * s)
        d.ellipse(S(lx - 30, cy + 200, lx + 26, cy + 232), fill=DARK)
    # arms
    for side in (-1, 1):
        x0 = cx + side * 130
        if arms:
            x1, y1 = cx + side * 190, cy - 80
        else:
            x1, y1 = cx + side * 185, cy + 70
        d.line(S(x0, cy + 10, x1, y1), fill=DARK, width=12 * s)
        d.ellipse(S(x1 - 18, y1 - 18, x1 + 18, y1 + 18), fill=DARK)
    # body
    d.ellipse(S(cx - 145, cy - 175, cx + 145, cy + 175), fill=dark)
    d.ellipse(S(cx - 140, cy - 175, cx + 136, cy + 165), fill=color)
    d.polygon([(x * s, y * s) for x, y in ellipse_poly(cx - 100, cy - 70, 26, 13, -60)], fill=(255, 255, 255, 120))
    # stem + leaf
    d.line(S(cx + 5, cy - 172, cx + 20, cy - 225), fill=BROWN, width=10 * s)
    d.polygon([(x * s, y * s) for x, y in leaf_poly(cx + 70, cy - 228, 120, 40, -15)], fill=LEAF)
    # eyes
    ey = cy - 30
    for ex in (cx - 52, cx + 52):
        d.ellipse(S(ex - 40, ey - 44, ex + 40, ey + 44), fill=(255, 255, 255))
        if blink:
            d.rectangle(S(ex - 41, ey - 45, ex + 41, ey + 4), fill=color)
            d.line(S(ex - 38, ey + 4, ex + 38, ey + 4), fill=DARK, width=6 * s)
        else:
            d.ellipse(S(ex - 18 + look, ey - 12, ex + 18 + look, ey + 26), fill=(25, 22, 28))
            d.ellipse(S(ex - 8 + look, ey - 6, ex + 2 + look, ey + 4), fill=(255, 255, 255))
    # brows
    if mood == "worried":
        d.line(S(cx - 90, ey - 58, cx - 22, ey - 74), fill=DARK, width=9 * s)
        d.line(S(cx + 22, ey - 74, cx + 90, ey - 58), fill=DARK, width=9 * s)
    elif mood == "wow":
        d.arc(S(cx - 92, ey - 90, cx - 14, ey - 48), 200, 340, fill=DARK, width=8 * s)
        d.arc(S(cx + 14, ey - 90, cx + 92, ey - 48), 200, 340, fill=DARK, width=8 * s)
    # mouth
    my = cy + 62
    if mouth == 0:
        if mood == "worried":
            d.arc(S(cx - 30, my, cx + 30, my + 30), 200, 340, fill=DARK, width=7 * s)
        else:
            d.arc(S(cx - 34, my - 26, cx + 34, my + 14), 20, 160, fill=DARK, width=7 * s)
    else:
        h = 24 if mouth == 1 else 40
        if mood == "wow":
            d.ellipse(S(cx - 20, my - 10, cx + 20, my + h), fill=(70, 20, 30))
        else:
            d.chord(S(cx - 32, my - 16, cx + 32, my + h), 0, 180, fill=(70, 20, 30))
            d.ellipse(S(cx - 15, my + h * 0.3, cx + 15, my + h), fill=(230, 110, 110))
    return im.resize((YW, YH), Image.LANCZOS)


if __name__ == "__main__":
    sheet = Image.new("RGBA", (ZW * 3 + YW * 3, ZH), (200, 225, 240, 255))
    sheet.alpha_composite(zeynep(0, False, 80), (0, 0))
    sheet.alpha_composite(zeynep(2, False, 10), (ZW, 0))
    sheet.alpha_composite(zeynep(1, True, -30), (ZW * 2, 0))
    sheet.alpha_composite(zeyto((128, 158, 52), 0), (ZW * 3, 500))
    sheet.alpha_composite(zeyto((110, 52, 84), 2, mood="worried", arms=1), (ZW * 3 + YW, 500))
    sheet.alpha_composite(zeyto((45, 36, 48), 1, mood="wow", blink=False), (ZW * 3 + YW * 2, 500))
    sheet.convert("RGB").resize((sheet.width // 2, sheet.height // 2)).save("/home/claude/dt/chk/cast.png")


HAIR_M = (112, 72, 40)
CAP = (70, 128, 58)
CAP_SH = (48, 96, 40)
HAIR_M_SH = (88, 56, 30)
VEST_M = (78, 107, 46)
BOOK = (31, 58, 26)


@lru_cache(maxsize=512)
def muhendis(mouth=0, blink=False, arm=70, look=0):
    """Male agricultural engineer: green baseball cap, long brown hair tucked inside the cap (no visible bun), no beard,
    olive vest, green field notebook ('Mühendisin Defteri'). Same signature as the old zeynep()."""
    s = SS
    im = Image.new("RGBA", (ZW * s, ZH * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    S = lambda *v: [x * s for x in v]
    P = lambda pts: [(x * s, y * s) for x, y in pts]

    # legs + boots
    for x0 in (206, 322):
        d.rounded_rectangle(S(x0, 690, x0 + 76, 1010), radius=18 * s, fill=JEANS)
        d.rounded_rectangle(S(x0 - 10, 985, x0 + 90, 1085), radius=24 * s, fill=BOOT)
        d.rectangle(S(x0 - 10, 1060, x0 + 90, 1085), fill=(70, 44, 26))
    d.rectangle(S(196, 680, 404, 714), fill=(70, 44, 26))
    d.rounded_rectangle(S(286, 684, 314, 710), radius=4 * s, fill=SUN)
    # torso: broad shoulders tapering to waist
    d.polygon(P([(150, 450), (190, 392), (410, 392), (450, 450), (420, 715), (180, 715)]), fill=SHIRT)
    d.ellipse(S(146, 388, 236, 478), fill=SHIRT)
    d.ellipse(S(364, 388, 454, 478), fill=SHIRT)
    # rolled sleeves line + vest
    d.polygon(P([(160, 455), (235, 398), (280, 410), (268, 714), (182, 714)]), fill=VEST_M)
    d.polygon(P([(440, 455), (365, 398), (320, 410), (332, 714), (418, 714)]), fill=VEST_M)
    d.rounded_rectangle(S(194, 560, 254, 616), radius=8 * s, fill=VEST_SH)
    d.rounded_rectangle(S(346, 560, 406, 616), radius=8 * s, fill=VEST_SH)
    d.line(S(204, 576, 244, 576), fill=VEST, width=4 * s)
    d.line(S(356, 576, 396, 576), fill=VEST, width=4 * s)
    # pen in pocket + badge
    d.rounded_rectangle(S(372, 532, 382, 576), radius=4 * s, fill=RED)
    d.rounded_rectangle(S(344, 462, 404, 512), radius=8 * s, fill=SUN)
    d.polygon(P(leaf_poly(374, 487, 40, 16, -30)), fill=DARK)
    # collar + open neck
    d.polygon(P([(258, 388), (300, 436), (342, 388), (322, 380), (300, 410), (278, 380)]), fill=(225, 222, 214))
    d.rounded_rectangle(S(270, 326, 330, 404), radius=16 * s, fill=SKIN_SH)
    d.polygon(P([(284, 392), (300, 420), (316, 392)]), fill=SKIN_SH)

    # left arm holding the green field notebook
    _limb(d, (186 * s, 440 * s), (166 * s, 565 * s), 66 * s, SHIRT)
    _limb(d, (166 * s, 565 * s), (166 * s, 600 * s), 58 * s, SKIN)          # rolled sleeve forearm
    _limb(d, (166 * s, 600 * s), (220 * s, 645 * s), 54 * s, SKIN)
    d.rounded_rectangle(S(132, 560, 268, 730), radius=12 * s, fill=BOOK)
    d.rectangle(S(132, 560, 150, 730), fill=(22, 44, 18))
    d.rounded_rectangle(S(160, 590, 256, 640), radius=6 * s, fill=CREAM)
    d.polygon(P(ellipse_poly(196, 615, 14, 10, 20)), fill=(128, 158, 52))
    d.polygon(P(leaf_poly(222, 610, 30, 11, -30)), fill=LEAF)
    d.rectangle(S(240, 560, 252, 700), fill=RED)   # ribbon bookmark
    d.ellipse(S(198, 628, 242, 672), fill=SKIN)

    # right arm (articulated), rolled sleeve
    sh = (414, 438)
    a = math.radians(arm)
    el = (sh[0] + math.cos(a) * 125, sh[1] + math.sin(a) * 125)
    a2 = math.radians(arm - (25 if arm < 60 else 0))
    hd = (el[0] + math.cos(a2) * 120, el[1] + math.sin(a2) * 120)
    _limb(d, (sh[0] * s, sh[1] * s), (el[0] * s, el[1] * s), 66 * s, SHIRT)
    _limb(d, (el[0] * s, el[1] * s), (hd[0] * s, hd[1] * s), 54 * s, SKIN)
    d.ellipse([(el[0] - 34) * s, (el[1] - 34) * s, (el[0] + 34) * s, (el[1] + 34) * s], fill=(232, 228, 218))
    d.ellipse([(hd[0] - 25) * s, (hd[1] - 25) * s, (hd[0] + 25) * s, (hd[1] + 25) * s], fill=SKIN)
    if arm < 60:
        f = (hd[0] + math.cos(a2) * 42, hd[1] + math.sin(a2) * 42)
        d.line([(hd[0] * s, hd[1] * s), (f[0] * s, f[1] * s)], fill=SKIN, width=15 * s)
        d.ellipse([(f[0] - 8) * s, (f[1] - 8) * s, (f[0] + 8) * s, (f[1] + 8) * s], fill=SKIN)

    # head: slightly squarer jaw
    cx, cy = 300, 255
    d.rounded_rectangle(S(cx - 102, cy - 108, cx + 102, cy + 100), radius=88 * s, fill=SKIN)
    d.ellipse(S(cx - 88, cy + 20, cx + 88, cy + 112), fill=SKIN)
    d.ellipse(S(cx - 122, cy - 6, cx - 88, cy + 42), fill=SKIN)
    d.ellipse(S(cx + 88, cy - 6, cx + 122, cy + 42), fill=SKIN)
    # long hair swept back: sideburns + strands at temples and nape (rest tucked in the hat)
    d.polygon(P([(cx - 104, cy - 70), (cx - 104, cy + 6), (cx - 90, cy + 14), (cx - 84, cy - 40), (cx - 40, cy - 74)]), fill=HAIR_M)
    d.polygon(P([(cx + 104, cy - 70), (cx + 104, cy + 6), (cx + 90, cy + 14), (cx + 84, cy - 40), (cx + 40, cy - 74)]), fill=HAIR_M)
    d.chord(S(cx - 104, cy - 112, cx + 104, cy + 10), 180, 360, fill=HAIR_M)
    d.arc(S(cx - 80, cy - 100, cx + 20, cy - 30), 200, 300, fill=HAIR_M_SH, width=6 * s)
    d.arc(S(cx - 10, cy - 100, cx + 90, cy - 30), 240, 340, fill=HAIR_M_SH, width=6 * s)
    # baseball cap: dome crown + front visor
    d.chord(S(cx - 114, cy - 178, cx + 114, cy - 4), 180, 360, fill=CAP)
    d.rectangle(S(cx - 114, cy - 92, cx + 114, cy - 66), fill=CAP)
    d.arc(S(cx - 60, cy - 176, cx + 60, cy - 10), 190, 350, fill=CAP_SH, width=5 * s)   # panel seams
    d.line(S(cx, cy - 178, cx, cy - 92), fill=CAP_SH, width=5 * s)
    d.ellipse(S(cx - 13, cy - 190, cx + 13, cy - 166), fill=CAP_SH)                    # top button
    # logo patch: cream disc with olive + leaf
    d.ellipse(S(cx - 34, cy - 150, cx + 34, cy - 84), fill=CREAM)
    d.polygon(P(ellipse_poly(cx - 6, cy - 112, 16, 12, 20)), fill=(128, 158, 52))
    d.polygon(P(leaf_poly(cx + 14, cy - 128, 34, 12, -35)), fill=LEAF)
    # band + visor (slightly toward camera, offset to one side)
    d.rectangle(S(cx - 114, cy - 70, cx + 114, cy - 60), fill=CAP_SH)
    d.chord(S(cx - 132, cy - 92, cx + 150, cy - 26), 0, 180, fill=CAP_SH)
    d.chord(S(cx - 128, cy - 96, cx + 146, cy - 34), 0, 180, fill=CAP)
    d.arc(S(cx - 104, cy - 86, cx + 122, cy - 44), 20, 160, fill=CAP_SH, width=4 * s)  # visor stitching
    # thick brows
    d.line(S(cx - 72, cy - 26, cx - 22, cy - 32), fill=HAIR_M_SH, width=11 * s)
    d.line(S(cx + 22, cy - 32, cx + 72, cy - 26), fill=HAIR_M_SH, width=11 * s)
    # eyes
    for ex in (cx - 44, cx + 44):
        if blink:
            d.arc(S(ex - 18, cy - 2, ex + 18, cy + 22), 200, 340, fill=(40, 28, 22), width=6 * s)
        else:
            d.ellipse(S(ex - 14 + look, cy - 6, ex + 14 + look, cy + 26), fill=(40, 28, 22))
            d.ellipse(S(ex - 6 + look, cy, ex + 3 + look, cy + 9), fill=(255, 255, 255))
    # nose (a bit stronger) + light cheek tone
    d.arc(S(cx - 14, cy + 14, cx + 14, cy + 46), 20, 160, fill=SKIN_SH, width=6 * s)
    ch = Image.new("RGBA", im.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(ch)
    cd.ellipse(S(cx - 86, cy + 32, cx - 52, cy + 50), fill=(225, 130, 110, 60))
    cd.ellipse(S(cx + 52, cy + 32, cx + 86, cy + 50), fill=(225, 130, 110, 60))
    im.alpha_composite(ch)
    # mouth
    my = cy + 66
    if mouth == 0:
        d.arc(S(cx - 32, my - 22, cx + 32, my + 12), 20, 160, fill=MOUTH, width=7 * s)
    else:
        h = 20 if mouth == 1 else 32
        d.chord(S(cx - 30, my - 14, cx + 30, my + h), 0, 180, fill=MOUTH)
        top = (my - 14 + my + h) / 2
        d.chord(S(cx - 26, top - 4, cx + 26, top + 14), 0, 180, fill=(255, 255, 255))
        d.ellipse(S(cx - 14, my + h * 0.35, cx + 14, my + h + 2), fill=(230, 110, 110))
    return im.resize((ZW, ZH), Image.LANCZOS)


zeynep_old = zeynep
zeynep = muhendis


# ---------------------------------------------------------------- Ulu: the thousand-year-old olive tree
BARK = (132, 116, 92)
BARK_D = (96, 82, 64)
BARK_L = (160, 144, 118)
CANOPY = (118, 140, 96)
CANOPY_L = (150, 170, 120)
UW, UH = 1000, 1700


@lru_cache(maxsize=256)
def ulu(mouth=0, open_eyes=1.0, blink=False, look=0):
    """Gnarled olive trunk with a face. Feet (ground) at bottom, face centre around (500, 1000)."""
    import random as _r
    rnd = _r.Random(11)
    s = SS
    im = Image.new("RGBA", (UW * s, UH * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    S = lambda *v: [x * s for x in v]
    P = lambda pts: [(x * s, y * s) for x, y in pts]
    # canopy (top, wider than trunk)
    for k in range(26):
        cx, cy = rnd.uniform(60, 940), rnd.uniform(60, 520)
        r = rnd.uniform(120, 200)
        d.ellipse(S(cx - r, cy - r * 0.7, cx + r, cy + r * 0.7), fill=CANOPY)
    for k in range(16):
        cx, cy = rnd.uniform(100, 900), rnd.uniform(40, 440)
        r = rnd.uniform(70, 130)
        d.ellipse(S(cx - r, cy - r * 0.6, cx + r, cy + r * 0.6), fill=CANOPY_L)
    for k in range(40):
        cx, cy = rnd.uniform(80, 920), rnd.uniform(80, 560)
        col = [(45, 36, 48), (110, 52, 84), (128, 158, 52)][k % 3]
        d.ellipse(S(cx - 16, cy - 12, cx + 16, cy + 12), fill=col)
    # trunk: twisted, wide base
    trunk = [(170, 1700), (230, 1500), (300, 1260), (290, 1050), (330, 820), (300, 620), (360, 520),
             (640, 520), (700, 620), (670, 820), (710, 1050), (700, 1260), (770, 1500), (840, 1700)]
    d.polygon(P(trunk), fill=BARK)
    # roots
    for x0, x1 in [(170, 40), (260, 150), (740, 880), (820, 980)]:
        d.polygon(P([(x0, 1600), (x0 + 60, 1600), (x1, 1700), (x1 - 60, 1700)]), fill=BARK_D)
    # branches into canopy
    for (x0, y0, x1, y1, w) in [(380, 560, 220, 330, 60), (620, 560, 800, 300, 60), (500, 540, 520, 260, 50)]:
        d.line(S(x0, y0, x1, y1), fill=BARK, width=w * s)
    # bark grooves
    for k in range(14):
        x = 300 + k * 30 + rnd.uniform(-10, 10)
        pts = [(x + math.sin(j / 2.0 + k) * 26, 560 + j * 80) for j in range(15)]
        d.line(P(pts), fill=BARK_D if k % 2 else BARK_L, width=(7 if k % 2 else 4) * s, joint="curve")
    # hollow (kovuk) low on the trunk
    d.ellipse(S(560, 1330, 680, 1500), fill=(58, 44, 34))
    d.ellipse(S(570, 1345, 670, 1490), fill=(40, 30, 24))
    # face plate (smoother bark around eyes/mouth)
    d.ellipse(S(330, 860, 670, 1240), fill=BARK_L)
    # brows: heavy ridges
    d.polygon(P([(350, 950), (480, 920), (485, 945), (360, 975)]), fill=BARK_D)
    d.polygon(P([(650, 950), (520, 920), (515, 945), (640, 975)]), fill=BARK_D)
    # eyes
    for ex in (420, 580):
        ey = 1015
        d.ellipse(S(ex - 52, ey - 34, ex + 52, ey + 34), fill=(250, 244, 226))
        d.ellipse(S(ex - 20 + look, ey - 22, ex + 20 + look, ey + 22), fill=(52, 70, 34))
        d.ellipse(S(ex - 9 + look, ey - 10, ex + 9 + look, ey + 10), fill=(20, 18, 16))
        d.ellipse(S(ex - 5 + look, ey - 12, ex + 2 + look, ey - 5), fill=(255, 255, 255))
        o = 0.0 if blink else open_eyes
        lid = int(68 * (1 - o))
        if lid > 0:
            d.rectangle(S(ex - 56, ey - 38, ex + 56, ey - 38 + lid), fill=BARK_L)
            d.line(S(ex - 52, ey - 36 + lid, ex + 52, ey - 36 + lid), fill=BARK_D, width=6 * s)
        d.arc(S(ex - 56, ey - 38, ex + 56, ey + 38), 200, 340, fill=BARK_D, width=6 * s)
    # nose: knot
    d.ellipse(S(470, 1060, 530, 1120), fill=BARK)
    d.arc(S(470, 1060, 530, 1120), 20, 160, fill=BARK_D, width=5 * s)
    # mouth: crack that opens
    my = 1170
    if mouth == 0:
        d.arc(S(430, my - 30, 570, my + 20), 20, 160, fill=(58, 44, 34), width=9 * s)
    else:
        h = 30 if mouth == 1 else 52
        d.ellipse(S(440, my - 12, 560, my + h), fill=(58, 44, 34))
        d.ellipse(S(470, my + h * 0.45, 530, my + h - 4), fill=(110, 70, 60))
    # moss beard
    for k in range(9):
        x = 420 + k * 20
        d.ellipse(S(x - 18, 1215 + (k % 3) * 8, x + 18, 1250 + (k % 3) * 8), fill=(120, 150, 80))
    return im.resize((UW, UH), Image.LANCZOS)


# ---------------------------------------------------------------- Sinsi: olive fly villain
SW_, SH_ = 440, 420


@lru_cache(maxsize=256)
def sinsi(mouth=0, wing=0.0, blink=False):
    s = SS
    im = Image.new("RGBA", (SW_ * s, SH_ * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    S = lambda *v: [x * s for x in v]
    P = lambda pts: [(x * s, y * s) for x, y in pts]
    cx, cy = 220, 270
    # wings (translucent, banded tips) — angle by `wing`
    wl = Image.new("RGBA", im.size, (0, 0, 0, 0))
    wd = ImageDraw.Draw(wl)
    for side in (-1, 1):
        ang = -35 - wing * 30
        a = math.radians(ang if side > 0 else 180 - ang)
        ox, oy = cx + side * 30, cy - 40
        wd.polygon(P(ellipse_poly(ox + math.cos(a) * 95, oy + math.sin(a) * 95, 110, 42, math.degrees(a))), fill=(220, 236, 244, 150))
        wd.polygon(P(ellipse_poly(ox + math.cos(a) * 160, oy + math.sin(a) * 160, 34, 26, math.degrees(a))), fill=(70, 60, 50, 170))
    im.alpha_composite(wl)
    # legs
    for k in (-1, 0, 1):
        for side in (-1, 1):
            d.line(S(cx + side * 40, cy + 40 + k * 20, cx + side * 95, cy + 95 + k * 22), fill=(40, 30, 24), width=7 * s)
    # abdomen + thorax
    d.polygon(P(ellipse_poly(cx, cy + 50, 70, 88, 0)), fill=(196, 120, 48))
    for k in range(3):
        d.chord(S(cx - 66, cy + 30 + k * 34, cx + 66, cy + 70 + k * 34), 0, 180, fill=(120, 70, 30))
    d.ellipse(S(cx - 62, cy - 50, cx + 62, cy + 40), fill=(150, 92, 40))
    d.ellipse(S(cx - 16, cy - 30, cx + 16, cy - 4), fill=(250, 240, 220))   # white scutellum spot
    # head + huge red eyes
    d.ellipse(S(cx - 70, cy - 150, cx + 70, cy - 30), fill=(176, 110, 46))
    for ex in (cx - 48, cx + 48):
        d.ellipse(S(ex - 38, cy - 150, ex + 38, cy - 70), fill=(196, 30, 40))
        if blink:
            d.chord(S(ex - 38, cy - 150, ex + 38, cy - 70), 180, 360, fill=(176, 110, 46))
        else:
            d.ellipse(S(ex - 14, cy - 128, ex + 4, cy - 110), fill=(255, 210, 210))
    # sly brows
    d.line(S(cx - 82, cy - 166, cx - 18, cy - 140), fill=(40, 30, 24), width=9 * s)
    d.line(S(cx + 82, cy - 166, cx + 18, cy - 140), fill=(40, 30, 24), width=9 * s)
    # antennae
    for side in (-1, 1):
        d.line(S(cx + side * 20, cy - 148, cx + side * 50, cy - 196), fill=(40, 30, 24), width=6 * s)
        d.ellipse(S(cx + side * 50 - 9, cy - 205, cx + side * 50 + 9, cy - 187), fill=(40, 30, 24))
    # smirk / mouth
    my = cy - 52
    if mouth == 0:
        d.arc(S(cx - 30, my - 18, cx + 30, my + 12), 10, 120, fill=(40, 30, 24), width=6 * s)
    else:
        h = 14 if mouth == 1 else 24
        d.chord(S(cx - 24, my - 8, cx + 24, my + h), 0, 180, fill=(70, 20, 30))
    return im.resize((SW_, SH_), Image.LANCZOS)


SUIT = (96, 100, 110)
SUIT_SH = (74, 78, 88)


@lru_cache(maxsize=256)
def beton(mouth=0, blink=False, look=0):
    """Beton Bey: pushy contractor. White hard hat, grey suit over a big belly, red tie, thick moustache, blueprint roll."""
    s = SS
    im = Image.new("RGBA", (ZW * s, ZH * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    S = lambda *v: [x * s for x in v]
    P = lambda pts: [(x * s, y * s) for x, y in pts]
    # legs + shoes
    for x0 in (210, 318):
        d.rounded_rectangle(S(x0, 700, x0 + 78, 1020), radius=16 * s, fill=(60, 62, 70))
        d.rounded_rectangle(S(x0 - 14, 1010, x0 + 92, 1080), radius=24 * s, fill=(30, 28, 30))
    # body: belly
    d.ellipse(S(150, 400, 450, 760), fill=SUIT)
    d.rounded_rectangle(S(170, 390, 430, 560), radius=60 * s, fill=SUIT)
    d.polygon(P([(258, 392), (300, 640), (342, 392)]), fill=(245, 245, 245))      # shirt
    d.polygon(P([(288, 410), (312, 410), (318, 600), (300, 630), (282, 600)]), fill=(200, 40, 50))  # tie
    d.polygon(P([(258, 392), (300, 470), (240, 520), (220, 420)]), fill=SUIT_SH)   # lapels
    d.polygon(P([(342, 392), (300, 470), (360, 520), (380, 420)]), fill=SUIT_SH)
    for y in (620, 680):
        d.ellipse(S(330, y, 346, y + 16), fill=(40, 40, 46))
    d.rounded_rectangle(S(360, 470, 410, 490), radius=4 * s, fill=(240, 240, 240))  # pocket square
    # arms: left holds blueprint roll, right on belly
    _limb(d, (175 * s, 440 * s), (150 * s, 600 * s), 70 * s, SUIT)
    d.rounded_rectangle(S(80, 560, 240, 610), radius=24 * s, fill=(70, 130, 200))
    d.ellipse(S(70, 560, 110, 610), fill=(230, 240, 250))
    d.ellipse(S(140, 570, 190, 620), fill=SKIN)
    _limb(d, (425 * s, 440 * s), (440 * s, 600 * s), 70 * s, SUIT)
    _limb(d, (440 * s, 600 * s), (360 * s, 640 * s), 60 * s, SUIT)
    d.ellipse(S(330, 620, 380, 670), fill=SKIN)
    # head
    cx, cy = 300, 260
    d.rounded_rectangle(S(274, 330, 326, 400), radius=14 * s, fill=SKIN_SH)
    d.ellipse(S(cx - 110, cy - 110, cx + 110, cy + 115), fill=SKIN)
    d.ellipse(S(cx - 130, cy - 4, cx - 96, cy + 46), fill=SKIN)
    d.ellipse(S(cx + 96, cy - 4, cx + 130, cy + 46), fill=SKIN)
    # double chin line
    d.arc(S(cx - 70, cy + 70, cx + 70, cy + 130), 20, 160, fill=SKIN_SH, width=5 * s)
    # hard hat
    d.chord(S(cx - 125, cy - 190, cx + 125, cy - 10), 180, 360, fill=(250, 250, 245))
    d.rounded_rectangle(S(cx - 150, cy - 108, cx + 150, cy - 80), radius=12 * s, fill=(235, 235, 228))
    d.rounded_rectangle(S(cx - 16, cy - 190, cx + 16, cy - 100), radius=8 * s, fill=(225, 225, 218))
    # brows (arrogant)
    d.line(S(cx - 78, cy - 46, cx - 22, cy - 34), fill=(40, 30, 26), width=12 * s)
    d.line(S(cx + 22, cy - 34, cx + 78, cy - 46), fill=(40, 30, 26), width=12 * s)
    for ex in (cx - 46, cx + 46):
        if blink:
            d.arc(S(ex - 18, cy - 10, ex + 18, cy + 14), 200, 340, fill=(40, 28, 22), width=6 * s)
        else:
            d.ellipse(S(ex - 13 + look, cy - 12, ex + 13 + look, cy + 16), fill=(40, 28, 22))
            d.ellipse(S(ex - 5 + look, cy - 6, ex + 2 + look, cy + 2), fill=(255, 255, 255))
    d.ellipse(S(cx - 20, cy + 14, cx + 20, cy + 52), fill=SKIN_SH)   # big nose
    # mouth under moustache
    my = cy + 82
    if mouth:
        h = 22 if mouth == 1 else 36
        d.chord(S(cx - 34, my - 16, cx + 34, my + h), 0, 180, fill=MOUTH)
    else:
        d.arc(S(cx - 30, my - 22, cx + 30, my + 8), 20, 160, fill=MOUTH, width=7 * s)
    d.polygon(P([(cx - 80, my - 6), (cx - 30, my - 34), (cx, my - 24), (cx + 30, my - 34), (cx + 80, my - 6), (cx + 40, my - 14), (cx, my - 10), (cx - 40, my - 14)]), fill=(46, 34, 28))
    return im.resize((ZW, ZH), Image.LANCZOS)
