"""Dalından Taze - shared brand drawing helpers (fonts, colors, icons, text)."""
import math
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

FD = "/usr/share/fonts/truetype/google-fonts/"
F_BOLD = FD + "Poppins-Bold.ttf"
F_MED = FD + "Poppins-Medium.ttf"
F_REG = FD + "Poppins-Regular.ttf"

OLIVE = (78, 107, 46)
DARK = (31, 58, 26)
CREAM = (255, 246, 224)
RED = (232, 57, 74)
SUN = (246, 194, 62)
BLACKOLIVE = (45, 36, 48)
PURPLE = (110, 52, 84)
GREEN_OLIVE = (128, 158, 52)
BROWN = (110, 78, 48)
LEAF = (92, 128, 60)
LEAF2 = (140, 168, 90)

HANDLE = "@muhendisindefteri"


@lru_cache(maxsize=64)
def font(path, size):
    return ImageFont.truetype(path, size)


def ellipse_poly(cx, cy, rx, ry, ang_deg, n=60):
    a = math.radians(ang_deg)
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    return pts


def leaf_poly(cx, cy, length, width, ang_deg, n=40):
    """Pointed leaf shape (lens) centred at cx,cy."""
    a = math.radians(ang_deg)
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (t - 0.5) * length
        y = math.sin(math.pi * t) * width / 2
        pts.append((x, y))
    for i in range(n, -1, -1):
        t = i / n
        x = (t - 0.5) * length
        y = -math.sin(math.pi * t) * width / 2
        pts.append((x, y))
    return [(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)) for x, y in pts]


def _canvas(S=800):
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def draw_olive(d, cx, cy, r, color, ang=20):
    d.polygon(ellipse_poly(cx, cy, r, r * 0.75, ang), fill=color)
    d.polygon(ellipse_poly(cx - r * 0.35, cy - r * 0.25, r * 0.28, r * 0.14, ang), fill=(255, 255, 255, 90))


def icon_olive(color, S=800):
    im, d = _canvas(S)
    draw_olive(d, S / 2, S / 2 + 30, S * 0.34, color)
    d.line([(S / 2 + 40, S / 2 - S * 0.22), (S / 2 + 90, S * 0.12)], fill=BROWN, width=18)
    d.polygon(leaf_poly(S * 0.66, S * 0.16, 220, 70, -25), fill=LEAF)
    return im


def icon_branch(olive_colors=(BLACKOLIVE, PURPLE, BLACKOLIVE, GREEN_OLIVE), S=800):
    im, d = _canvas(S)
    # stem
    pts = [(S * 0.08 + i * S * 0.084, S * 0.30 + math.sin(i / 10 * math.pi) * 60) for i in range(11)]
    d.line(pts, fill=BROWN, width=16, joint="curve")
    leaves = [(0.18, -1), (0.30, 1), (0.42, -1), (0.55, 1), (0.66, -1), (0.78, 1), (0.88, -1)]
    for i, (fx, side) in enumerate(leaves):
        x = S * fx
        y = S * 0.30 + math.sin(fx * math.pi) * 60
        ang = -40 if side < 0 else 40
        col = LEAF if i % 2 else LEAF2
        d.polygon(leaf_poly(x + 50, y + side * 45, 200, 58, ang), fill=col)
    for i, fx in enumerate([0.24, 0.48, 0.62, 0.82]):
        x = S * fx
        y = S * 0.30 + math.sin(fx * math.pi) * 60
        d.line([(x, y), (x + 5, y + 90)], fill=BROWN, width=8)
        draw_olive(d, x + 5, y + 160, 78, olive_colors[i % len(olive_colors)], ang=80)
    return im


def icon_strawberry(S=800):
    im, d = _canvas(S)
    cx, cy = S / 2, S / 2 + 40
    pts = []
    for i in range(80):
        t = 2 * math.pi * i / 80
        x = math.sin(t) * (0.82 + 0.18 * math.cos(t))
        y = -math.cos(t)
        w = 1.0 if y < 0 else (1 - 0.55 * y ** 1.4)
        pts.append((cx + x * 260 * w, cy + y * 280))
    d.polygon(pts, fill=RED)
    for row in range(5):
        for col in range(-3, 4):
            yy = cy - 170 + row * 85
            span = 220 * (1 - max(0, (yy - cy)) / 380)
            xx = cx + col * 70 + (35 if row % 2 else 0)
            if abs(xx - cx) < span - 30:
                d.polygon(ellipse_poly(xx, yy, 11, 18, 0, 16), fill=SUN)
    for k in range(5):
        ang = -90 + (k - 2) * 38
        a = math.radians(ang)
        d.polygon(leaf_poly(cx + math.cos(a) * 85, cy - 270 + math.sin(a) * 40 + 40, 190, 64, ang), fill=LEAF)
    d.line([(cx, cy - 290), (cx + 20, cy - 390)], fill=LEAF, width=20)
    return im


def icon_pomegranate(S=800):
    im, d = _canvas(S)
    cx, cy = S / 2, S / 2 + 40
    d.ellipse([cx - 280, cy - 270, cx + 280, cy + 290], fill=(176, 30, 52))
    crown = [(cx - 90, cy - 250), (cx - 110, cy - 350), (cx - 50, cy - 300), (cx, cy - 370),
             (cx + 50, cy - 300), (cx + 110, cy - 350), (cx + 90, cy - 250)]
    d.polygon(crown, fill=(150, 24, 44))
    d.polygon(ellipse_poly(cx - 120, cy - 110, 80, 40, -35), fill=(255, 255, 255, 70))
    return im


def icon_leaf(S=800):
    im, d = _canvas(S)
    d.polygon(leaf_poly(S / 2, S / 2, 640, 340, -40), fill=LEAF2)
    a = math.radians(-40)
    d.line([(S / 2 - 300 * math.cos(a), S / 2 - 300 * math.sin(a)),
            (S / 2 + 320 * math.cos(a), S / 2 + 320 * math.sin(a))], fill=DARK, width=14)
    for k in (-2, -1, 0, 1, 2):
        bx, by = S / 2 + k * 90 * math.cos(a), S / 2 + k * 90 * math.sin(a)
        for s in (1, -1):
            b = a + s * math.radians(45)
            d.line([(bx, by), (bx + 110 * math.cos(b), by + 110 * math.sin(b))], fill=DARK, width=8)
    return im


def icon_bottle(S=800):
    im, d = _canvas(S)
    cx = S / 2
    d.rounded_rectangle([cx - 150, 270, cx + 150, 760], radius=70, fill=DARK)
    d.polygon([(cx - 150, 340), (cx - 55, 190), (cx + 55, 190), (cx + 150, 340)], fill=DARK)
    d.rectangle([cx - 55, 110, cx + 55, 200], fill=DARK)
    d.rounded_rectangle([cx - 68, 50, cx + 68, 125], radius=14, fill=RED, outline=DARK, width=10)
    d.rounded_rectangle([cx - 120, 420, cx + 120, 650], radius=24, fill=CREAM)
    draw_olive(d, cx - 20, 540, 56, GREEN_OLIVE)
    d.polygon(leaf_poly(cx + 55, 490, 120, 40, -30), fill=LEAF)
    d.polygon(ellipse_poly(cx - 110, 400, 18, 90, 0), fill=(255, 255, 255, 50))
    return im


def icon_check(S=400, color=SUN):
    im, d = _canvas(S)
    d.ellipse([10, 10, S - 10, S - 10], fill=color)
    d.line([(S * 0.27, S * 0.52), (S * 0.44, S * 0.68), (S * 0.75, S * 0.34)], fill=DARK, width=int(S * 0.1), joint="curve")
    return im


def icon_arrow(S=400, color=CREAM):
    im, d = _canvas(S)
    d.line([(S * 0.15, S / 2), (S * 0.75, S / 2)], fill=color, width=int(S * 0.12))
    d.polygon([(S * 0.62, S * 0.25), (S * 0.92, S / 2), (S * 0.62, S * 0.75)], fill=color)
    return im


def wrap(text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if fnt.getlength(test) <= maxw:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_image(text, size, color, maxw, path=F_BOLD, align="center", line_gap=1.12, pill=None, pad=(36, 18)):
    """Render (possibly multi-line) text to a tight RGBA image. pill=(r,g,b) puts it on a rounded badge."""
    fnt = font(path, size)
    lines = []
    for part in text.split("\n"):
        lines += wrap(part, fnt, maxw)
    asc, desc = fnt.getmetrics()
    lh = int((asc + desc) * line_gap)
    w = int(max(fnt.getlength(l) for l in lines)) + 4
    h = lh * len(lines)
    px, py = pad if pill else (0, 0)
    im = Image.new("RGBA", (w + 2 * px, h + 2 * py), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if pill:
        d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=min(im.height // 2, 60), fill=pill)
    for i, l in enumerate(lines):
        lw = fnt.getlength(l)
        x = px + (w - lw) / 2 if align == "center" else px
        d.text((x, py + i * lh), l, font=fnt, fill=color)
    return im


def fit(im, width=None, height=None):
    if width:
        height = int(im.height * width / im.width)
    elif height:
        width = int(im.width * height / im.height)
    return im.resize((max(1, int(width)), max(1, int(height))), Image.LANCZOS)
