"""Story engine for 'Mühendisin Defteri' Reels: backgrounds, dialogue bubbles, step cards, crossfades."""
import math
import random
import subprocess
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter
from brand import *
from characters import zeynep, zeyto, ZW, ZH, ZCX, YW, YH, ulu, UW, UH, sinsi, SW_, SH_
from tts_tr import line_wav as _piper_wav, read_wav, envelope
import tts_eleven as _eleven


def line_wav(speaker, text, tag=None):
    if _eleven.available():
        return _eleven.line_wav(speaker, text, tag)
    return _piper_wav(speaker, text)
import os as _os
VOICE = _os.environ.get("DT_VOICE", "1") == "1"
SUBS = _os.environ.get("DT_SUBS", "1") == "1"

W, H, FPS = 1080, 1920, 30
BGW = 1200
XFADE = 0.35
CPS = 32  # typing speed (chars / second)

SKY_TOP, SKY_BOT = (170, 214, 236), (255, 238, 205)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(p):
    return 1 - (1 - p) ** 3


def ease_back(p, s=1.7):
    p -= 1
    return p * p * ((s + 1) * p + s) + 1


def lerp(a, b, t):
    return a + (b - a) * t


def vgrad(w, h, c0, c1):
    g = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / (h - 1)
        g.putpixel((0, y), tuple(int(lerp(c0[i], c1[i], t)) for i in range(3)))
    return g.resize((w, h)).convert("RGBA")


# ---------------------------------------------------------------- backgrounds
def _tree(d, x, base_y, sc, rnd, olive_col):
    trunk = [(x - 40 * sc, base_y), (x - 18 * sc, base_y - 220 * sc), (x - 50 * sc, base_y - 380 * sc),
             (x - 10 * sc, base_y - 400 * sc), (x + 20 * sc, base_y - 240 * sc), (x + 45 * sc, base_y)]
    d.polygon(trunk, fill=(118, 88, 60))
    d.line([(x + 5 * sc, base_y - 300 * sc), (x + 110 * sc, base_y - 420 * sc)], fill=(118, 88, 60), width=int(28 * sc))
    blobs = []
    for k in range(13):
        bx = x + rnd.uniform(-230, 230) * sc
        by = base_y - 470 * sc + rnd.uniform(-130, 110) * sc
        r = rnd.uniform(90, 150) * sc
        blobs.append((bx, by, r))
    for bx, by, r in blobs:
        d.ellipse([bx - r, by - r * 0.75, bx + r, by + r * 0.75], fill=(110, 138, 80))
    for bx, by, r in blobs[:9]:
        r2 = r * 0.7
        d.ellipse([bx - r2 - 10 * sc, by - r2 * 0.7 - 18 * sc, bx + r2 - 10 * sc, by + r2 * 0.7 - 18 * sc], fill=(150, 172, 112))
    for k in range(26):
        bx, by, r = blobs[k % len(blobs)]
        ox, oy = bx + rnd.uniform(-r, r) * 0.7, by + rnd.uniform(-r, r) * 0.45
        col = olive_col[k % len(olive_col)]
        d.ellipse([ox - 13 * sc, oy - 10 * sc, ox + 13 * sc, oy + 10 * sc], fill=col)


@lru_cache(maxsize=4)
def bg_orchard(olive_cols=("g",)):
    cols = {"g": [(128, 158, 52)], "p": [(110, 52, 84), (128, 158, 52), (45, 36, 48)]}[olive_cols[0]]
    rnd = random.Random(7)
    im = vgrad(BGW, H, SKY_TOP, SKY_BOT)
    d = ImageDraw.Draw(im)
    d.ellipse([820, 380, 1000, 560], fill=(255, 236, 170))
    # clouds
    for cx, cy, s in [(200, 520, 1.0), (760, 700, 0.8)]:
        for dx, dy, r in [(-60, 10, 50), (0, -10, 70), (70, 10, 55)]:
            d.ellipse([cx + dx * s - r * s, cy + dy * s - r * s, cx + dx * s + r * s, cy + dy * s + r * s], fill=(255, 255, 255))
    # hills
    d.polygon([(0, 1180)] + [(x, 1120 - 70 * math.sin(x / 260)) for x in range(0, BGW + 1, 20)] + [(BGW, 1400), (0, 1400)], fill=(155, 184, 108))
    d.polygon([(0, 1300)] + [(x, 1260 - 50 * math.sin(x / 190 + 1)) for x in range(0, BGW + 1, 20)] + [(BGW, 1500), (0, 1500)], fill=(126, 160, 82))
    for x in (90, 380, 650, 980):
        _tree(d, x, 1290 + rnd.uniform(-10, 10), 0.32, rnd, cols)
    # ground
    d.rectangle([0, 1480, BGW, H], fill=(138, 168, 84))
    d.polygon([(0, 1500), (BGW, 1470), (BGW, 1540), (0, 1560)], fill=(124, 154, 74))
    for k in range(70):
        gx, gy = rnd.uniform(0, BGW), rnd.uniform(1560, H)
        d.line([(gx, gy), (gx + 6, gy - 22)], fill=(110, 140, 66), width=5)
    _tree(d, 170, 1560, 1.0, rnd, cols)
    # harvest net under tree + crate
    net = Image.new("RGBA", (BGW, H), (0, 0, 0, 0))
    nd = ImageDraw.Draw(net)
    nd.ellipse([-80, 1520, 520, 1640], fill=(70, 140, 70, 120))
    im.alpha_composite(net)
    d.rounded_rectangle([930, 1530, 1150, 1650], radius=10, fill=(196, 120, 64))
    for k in range(3):
        d.rectangle([950 + k * 70, 1555, 990 + k * 70, 1575], fill=(150, 88, 44))
    for k in range(9):
        ox = 955 + k * 22
        d.ellipse([ox, 1508, ox + 30, 1534], fill=cols[k % len(cols)])
    return im


@lru_cache(maxsize=2)
def bg_mill():
    rnd = random.Random(3)
    im = vgrad(BGW, H, (245, 236, 214), (226, 212, 184))
    d = ImageDraw.Draw(im)
    # windows
    for x in (120, 520, 920):
        d.rounded_rectangle([x, 330, x + 200, 620], radius=20, fill=(190, 222, 238))
        d.line([(x + 100, 330), (x + 100, 620)], fill=(226, 212, 184), width=12)
    # floor
    d.rectangle([0, 1450, BGW, H], fill=(186, 168, 138))
    for k in range(0, BGW, 120):
        d.line([(k, 1450), (k - 160, H)], fill=(170, 152, 122), width=4)
    # machines
    steel, steel2 = (184, 194, 200), (150, 162, 170)
    d.polygon([(40, 1460), (90, 900), (330, 900), (380, 1460)], fill=steel)        # hopper / washer
    d.rectangle([60, 860, 360, 910], fill=steel2)
    d.rounded_rectangle([430, 1050, 760, 1460], radius=30, fill=steel)             # malaxer
    d.ellipse([480, 1000, 710, 1100], fill=steel2)
    d.rounded_rectangle([820, 1150, 1180, 1460], radius=24, fill=steel)            # decanter
    d.ellipse([780, 1220, 880, 1380], fill=steel2)
    d.line([(360, 960), (470, 1060)], fill=steel2, width=26)
    d.line([(760, 1200), (830, 1240)], fill=steel2, width=26)
    # oil drip
    d.rounded_rectangle([1000, 1460, 1060, 1500], radius=6, fill=steel2)
    d.polygon(ellipse_poly(1030, 1530, 14, 22, 0), fill=(176, 170, 40))
    for k in range(40):
        x, y = rnd.uniform(0, BGW), rnd.uniform(1470, H)
        d.ellipse([x, y, x + 6, y + 4], fill=(170, 152, 122))
    return im


@lru_cache(maxsize=2)
def bg_brand(color=OLIVE):
    im = Image.new("RGBA", (BGW, H), color + (255,))
    d = ImageDraw.Draw(im)
    deco = tuple(min(255, c + 16) for c in color)
    for bx, by, r in [(140, 380, 200), (1050, 700, 260), (180, 1500, 280), (1000, 1750, 180)]:
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=deco)
    return im


# ---------------------------------------------------------------- UI pieces
def name_tag(speaker):
    label, col = {"zeynep": ("Mühendis", OLIVE), "zeyto": ("Zeyto", RED), "ulu": ("Ulu", (110, 84, 56)),
                  "sinsi": ("Sinsi", (60, 52, 46)), "beton": ("Beton Bey", (90, 96, 104))}[speaker]
    return text_image(label, 34, CREAM, 600, pill=col, pad=(26, 8))


@lru_cache(maxsize=256)
def bubble_layout(text, size, maxw):
    fnt = font(F_BOLD, size)
    lines = wrap(text, fnt, maxw)
    asc, desc = fnt.getmetrics()
    lh = int((asc + desc) * 1.12)
    return lines, lh


def draw_bubble(frame, speaker, text, shown, cx, top, tail_x, tail_dir, scale=1.0, size=50, maxw=840):
    lines, lh = bubble_layout(text, size, maxw)
    bw = maxw + 90
    bh = lh * len(lines) + 70
    im = Image.new("RGBA", (bw + 20, bh + 120), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    oy = 40
    d.rounded_rectangle([10, oy, bw + 10, oy + bh], radius=46, fill=(255, 255, 255), outline=DARK, width=6)
    tx = clamp(tail_x - (cx - bw / 2), 80, bw - 80)
    if tail_dir == "down":
        d.polygon([(tx - 34, oy + bh - 6), (tx + 34, oy + bh - 6), (tx + 10, oy + bh + 70)], fill=(255, 255, 255), outline=None)
        d.line([(tx - 34, oy + bh - 3), (tx + 10, oy + bh + 70), (tx + 34, oy + bh - 3)], fill=DARK, width=6, joint="curve")
    fnt = font(F_BOLD, size)
    left = shown
    for i, l in enumerate(lines):
        if left <= 0:
            break
        part = l[:left]
        d.text((55, oy + 36 + i * lh), part, font=fnt, fill=DARK)
        left -= len(l) + 1
    tag = name_tag(speaker)
    im.alpha_composite(tag, (50, 0 if oy - tag.height // 2 < 0 else oy - tag.height // 2))
    if scale < 0.999:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    frame.alpha_composite(im, (int(cx - im.width / 2), int(top + (1 - scale) * bh / 2)))
    return top + bh + 40


def step_card(num, total, title, icon, accent=OLIVE):
    cw, ch = 940, 560
    im = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 10, cw, ch], radius=48, fill=(0, 0, 0, 40))
    d.rounded_rectangle([0, 0, cw, ch - 10], radius=48, fill=CREAM, outline=accent, width=8)
    d.ellipse([40, 40, 170, 170], fill=RED)
    nt = text_image(str(num), 86, CREAM, 200)
    im.alpha_composite(nt, (105 - nt.width // 2, 105 - nt.height // 2))
    tt = text_image(title, 64, DARK, 700, align="left")
    im.alpha_composite(tt, (200, 105 - tt.height // 2))
    if icon is not None:
        bb = icon.getbbox()
        ic = icon.crop(bb) if bb else icon
        ic = fit(ic, height=320)
        if ic.width > 700:
            ic = fit(ic, width=700)
        im.alpha_composite(ic, ((cw - ic.width) // 2, 200))
    for k in range(total):
        x = cw - 60 - (total - 1 - k) * 34
        r = 10 if k == num - 1 else 7
        d.ellipse([x - r, 70 - r, x + r, 70 + r], fill=accent if k <= num - 1 else (200, 200, 190))
    return im


def summary_card(title, items, accent=OLIVE):
    cw = 940
    rows = [text_image(it, 50, DARK, 700, align="left") for it in items]
    ch = 170 + sum(r.height + 34 for r in rows) + 30
    im = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 10, cw, ch], radius=48, fill=(0, 0, 0, 40))
    d.rounded_rectangle([0, 0, cw, ch - 10], radius=48, fill=CREAM, outline=accent, width=8)
    tp = text_image(title, 46, CREAM, 860, pill=accent, pad=(30, 12))
    im.alpha_composite(tp, ((cw - tp.width) // 2, 40))
    y = 160
    chk = fit(icon_check(), width=70)
    for r in rows:
        im.alpha_composite(chk, (60, y + r.height // 2 - 35))
        im.alpha_composite(r, (160, y))
        y += r.height + 34
    return im


# ---------------------------------------------------------------- shots
class Shot:
    """lines: list of (speaker, text, opts). opts keys: mood, color, arms, point, step (index into steps)."""

    def __init__(self, bg, lines, zeynep_x=None, zeyto_x=None, zeyto_color=GREEN_OLIVE, zeynep_enter=False,
                 steps=None, accent=OLIVE, summary=None, props=None, layout="talk", lead=0.35, tail=0.5, end=None,
                 gap=0.55, card=None, actors=None, tint=None, zeyto_drop=None, pan=True, bubble_top=400, zeynep_scale=None):
        self.bg, self.lines = bg, lines
        self.tint = tint
        self.actors, self.ydrop, self.do_pan, self.btop, self.zsc = actors or [], zeyto_drop, pan, bubble_top, zeynep_scale
        self.zx, self.yx, self.ycol = zeynep_x, zeyto_x, zeyto_color
        self.enter, self.steps, self.accent, self.summary = zeynep_enter, steps, accent, summary
        self.props, self.layout, self.end = props or [], layout, end
        self.timing, t = [], lead + (0.5 if zeynep_enter else 0)
        self.voice = []  # per line: (wav path, seconds, 30fps envelope) or None
        for sp, text, opts in lines:
            v = None
            if VOICE and text:
                path = line_wav(sp, text, opts.get("tag"))
                data, sr = read_wav(path)
                v = (path, len(data) / sr, envelope(data, sr))
            self.voice.append(v)
            if v:
                dur = opts.get("dur", v[1] + opts.get("gap", gap))
            else:
                dur = opts.get("dur", 0.9 + len(text) / 16.0)
            self.timing.append((t, dur))
            t += dur
        self.dur = t + tail
        self._step_imgs = {}
        self._summary_img = summary_card(*summary, accent=accent) if summary else card

    def current(self, t):
        idx = 0
        for i, (st, du) in enumerate(self.timing):
            if t >= st:
                idx = i
        return idx

    def render(self, t, T):
        pan = int(ease(clamp(t / max(self.dur, 0.1))) * (BGW - W)) if self.do_pan else (BGW - W) // 2
        frame = self.bg.crop((pan, 0, pan + W, H))
        li = self.current(t)
        st, du = self.timing[li]
        speaker, text, opts = self.lines[li]
        lt = t - st
        v = self.voice[li]
        if v:
            vlen, env = v[1], v[2]
            shown = int(len(text) * clamp(lt / max(vlen * 0.92, 0.2))) if lt >= 0 else 0
            talking = 0 <= lt < vlen
            if talking:
                e = env[min(len(env) - 1, int(lt * 30))]
                flap = 2 if e > 0.55 else (1 if e > 0.18 else 0)
            else:
                flap = 0
        else:
            shown = int(lt * CPS) if lt >= 0 else 0
            talking = lt >= 0 and shown < len(text) + 6
            flap = [1, 2, 1, 0][int(T * 10) % 4] if talking else 0

        card_mode = self.steps is not None or self._summary_img is not None
        if self.layout == "end":
            card_mode = False
        z_scale = self.zsc or (0.62 if card_mode else 0.84)
        y_scale = 0.78 if card_mode else 1.0
        feet = 1880

        # step card / summary card
        if self.steps is not None:
            k = opts.get("step")
            if k is None:
                k = max([self.lines[j][2].get("step", -1) for j in range(li + 1)] + [-1])
            if k >= 0:
                if k not in self._step_imgs:
                    title, icon = self.steps[k]
                    self._step_imgs[k] = step_card(k + 1, len(self.steps), title, icon, self.accent)
                card = self._step_imgs[k]
                first = min(j for j in range(len(self.lines)) if self.lines[j][2].get("step") == k)
                ct = t - self.timing[first][0] + 0.15
                p = ease_back(clamp(ct / 0.45)) if ct < 0.45 else 1.0
                c = card if p >= 0.999 else card.resize((max(1, int(card.width * p)), max(1, int(card.height * p))), Image.BILINEAR)
                frame.alpha_composite(c, (int(W / 2 - c.width / 2), int(250 + card.height / 2 - c.height / 2)))
        if self._summary_img is not None:
            p = ease_back(clamp(t / 0.5))
            c = self._summary_img
            if p < 0.999:
                c = c.resize((max(1, int(c.width * p)), max(1, int(c.height * p))), Image.BILINEAR)
            frame.alpha_composite(c, (int(W / 2 - c.width / 2), int(250 + self._summary_img.height / 2 - c.height / 2)))

        for img, x, y in self.props:
            frame.alpha_composite(img, (int(x - img.width / 2), int(y - img.height / 2)))

        # characters
        heads = {}
        for a in self.actors:
            kind = a["kind"]
            if t < a.get("appear", 0):
                continue
            am = flap if speaker == kind else 0
            if kind == "ulu":
                wake = a.get("wake", 0)
                o = clamp((t - wake) / 0.8) if wake is not None else 1.0
                blink = o >= 1 and (T + 0.9) % 4.1 < 0.15
                img = ulu(am, round(o, 1), blink, -8 if a["x"] > W / 2 else 8)
                sc = a.get("scale", 1.0)
                if sc != 1.0:
                    img = img.resize((int(UW * sc), int(UH * sc)), Image.BILINEAR)
                x0, y0 = a["x"] - img.width / 2, a.get("feet", 1880) - img.height
                frame.alpha_composite(img, (int(x0), int(y0)))
                heads["ulu"] = (a["x"], y0 + 900 * sc)
            elif kind == "sinsi":
                tt = t - a.get("appear", 0)
                if a.get("stuck"):
                    x = a["x"] + math.sin(T * 9) * 4
                    y = a["y"] + math.sin(T * 7) * 3
                else:
                    fly_in = 1 - ease(clamp(tt / 0.7))
                    x = a["x"] + math.sin(T * 1.7) * 40 + fly_in * 500
                    y = a["y"] + math.sin(T * 3.1) * 25
                img = sinsi(am, round(abs(math.sin(T * 40)), 1), (T % 3.0) < 0.12)
                sc = a.get("scale", 1.0)
                img = img.resize((int(SW_ * sc), int(SH_ * sc)), Image.BILINEAR)
                frame.alpha_composite(img, (int(x - img.width / 2), int(y - img.height / 2)))
                heads["sinsi"] = (x, y + img.height / 2)
        if self.zx is not None:
            zx = self.zx
            if self.enter:
                zx = lerp(-350, self.zx, ease(clamp(t / 0.85)))
            arm = 82
            if opts.get("point") and speaker == "zeynep":
                arm = lerp(82, -25, ease(clamp(lt / 0.35)))
            elif opts.get("wave") and speaker == "zeynep":
                arm = -30 + 18 * math.sin(T * 8)
            blink = (T * 1.0 + 0.3) % 3.4 < 0.13
            zm = flap if speaker == "zeynep" else 0
            bob = math.sin(T * 2.4) * 5 + (abs(math.sin(T * 9)) * 6 if (self.enter and t < 0.85) else 0)
            zi = zeynep(zm, blink, int(round(arm / 3) * 3), 4 if (self.yx or 9999) > self.zx else -4)
            zi = fit(zi, width=int(ZW * z_scale)) if abs(z_scale - 1) > 0.01 else zi
            x0 = zx - ZCX * z_scale
            y0 = feet - ZH * z_scale + bob
            frame.alpha_composite(zi, (int(x0), int(y0)))
            heads["zeynep"] = (zx, y0 + 60 * z_scale)
        if self.yx is not None:
            mood = opts.get("mood", "happy") if speaker == "zeyto" else self.lines[li][2].get("ymood", "happy")
            col = opts.get("color", self.ycol)
            arms = 1 if (speaker == "zeyto" and opts.get("arms")) or self.layout == "end" else 0
            blink = (T * 1.0 + 1.7) % 2.9 < 0.13
            ym = flap if speaker == "zeyto" else 0
            yi = zeyto(col, ym, blink, mood, -6 if (self.zx or -1) < self.yx else 6, arms)
            sq = 1 + (0.035 * math.sin(T * 12) if speaker == "zeyto" and talking else 0)
            hop = abs(math.sin(T * 3.0)) * 18 if (speaker == "zeyto" and talking) or self.layout == "end" else math.sin(T * 2) * 4
            w, h = int(YW * y_scale / sq ** 0.5), int(YH * y_scale * sq)
            yi = yi.resize((w, h), Image.BILINEAR)
            drop = 0.0
            if self.ydrop is not None:
                if t < self.ydrop:
                    drop = None
                else:
                    drop = -1100 * (1 - ease_back(clamp((t - self.ydrop) / 0.6), 1.2))
            if drop is not None:
                frame.alpha_composite(yi, (int(self.yx - w / 2), int(feet - h - hop + drop)))
                heads["zeyto"] = (self.yx, feet - h - hop + 40 + drop)

        if self.tint:
            col, a = self.tint
            ov = Image.new("RGBA", frame.size, col + (int(255 * a),))
            frame.alpha_composite(ov)

        # end card text
        if self.end:
            for img, y, delay in self.end:
                p = clamp((t - delay) / 0.45)
                if p <= 0:
                    continue
                im = img.copy()
                im.putalpha(im.getchannel("A").point(lambda v: int(v * p)))
                frame.alpha_composite(im, (int(W / 2 - im.width / 2), int(y - im.height / 2 + (1 - ease(p)) * 60)))
            return frame

        # karaoke subtitle (voiced lines) — falls back to the speech bubble
        if SUBS and lt >= 0 and text and v and self.layout != "end":
            import make_ai
            if not hasattr(self, "_groups"):
                self._groups = {}
            if li not in self._groups:
                self._groups[li] = make_ai.chunks(make_ai.word_times(text, v[1], v[2]))
            groups = self._groups[li]
            if lt < v[1] + 0.25:
                g = next((g for g in groups if lt < g[-1][2] + 0.05), groups[-1])
                if card_mode:
                    ch = self._summary_img.height if self._summary_img is not None else 560
                    y0 = 250 + ch + 130
                else:
                    y0 = 470
                make_ai.draw_subtitle(frame, speaker, g, lt, y0)
            return frame
        # speech bubble
        if lt >= 0 and text:
            bp = ease_back(clamp(lt / 0.22))
            hx, hy = heads.get(speaker, (W / 2, 1400))
            if card_mode:
                top = (250 + (self._summary_img.height if self._summary_img else 560) + 30)
                size, maxw = 44, 840
            else:
                top = self.btop
                size, maxw = 52, 840
            draw_bubble(frame, speaker, text, shown, W / 2, top, hx, "down", scale=max(0.05, bp), size=size, maxw=maxw)
        return frame


def series_chip(ep_label):
    return text_image(ep_label, 30, CREAM, 1000, pill=(0, 0, 0, 110), pad=(24, 8))


def handle_badge():
    fnt = font(F_MED, 32)
    w = int(fnt.getlength(HANDLE)) + 64
    im = Image.new("RGBA", (w, 52), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, 51], radius=26, fill=(255, 255, 255, 200))
    draw_olive(d, 26, 27, 13, GREEN_OLIVE)
    d.text((46, 6), HANDLE, font=fnt, fill=DARK)
    return im


def episode_events(shots):
    """Timeline used for the soundtrack and the voice-over script."""
    ev, acc = {"lines": [], "cards": [], "cuts": [], "total": 0.0}, 0.0
    for i, sh in enumerate(shots):
        if i > 0:
            ev["cuts"].append(acc)
        if sh._summary_img is not None:
            ev["cards"].append(acc + 0.05)
        seen = set()
        for (sp, text, opts), (st, du) in zip(sh.lines, sh.timing):
            if text:
                ev["lines"].append({"t": round(acc + st, 2), "dur": round(du, 2), "speaker": sp, "text": text})
        for (sp, text, opts), (st, du), v in zip(sh.lines, sh.timing, sh.voice):
            if v:
                ev.setdefault("voice", []).append({"t": round(acc + st, 3), "wav": v[0], "len": round(v[1], 3)})
            k = opts.get("step")
            if k is not None and k not in seen:
                seen.add(k)
                ev["cards"].append(acc + st + 0.15)
        if sh.layout == "end":
            ev["end"] = acc
        acc += sh.dur
    ev["total"] = acc
    return ev


@lru_cache(maxsize=1)
def _grade():
    """Warm cinematic grade: soft vignette + faint warm wash."""
    g = Image.new("RGBA", (W, H), (255, 190, 130, 14))
    m = Image.new("L", (W // 4, H // 4), 0)
    md = ImageDraw.Draw(m)
    for k in range(30):
        a = int(110 * (k / 30) ** 2.2)
        inset = 30 - k
        md.ellipse([-W // 8 + inset * 4, -H // 8 + inset * 6, W // 4 + W // 8 - inset * 4, H // 4 + H // 8 - inset * 6], outline=a, width=6)
    m = m.resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(40))
    v = Image.new("RGBA", (W, H), (20, 12, 6, 255))
    v.putalpha(m)
    g.alpha_composite(v)
    return g


@lru_cache(maxsize=8)
def _bar(label):
    import make_ai
    return make_ai.header(label)


def render_episode(shots, ep_label, out_path):
    import json
    with open(out_path[:-4] + ".events.json", "w") as f:
        json.dump(episode_events(shots), f, ensure_ascii=False, indent=1)
    total = sum(s.dur for s in shots)
    n = int(total * FPS)
    chip, badge = series_chip(ep_label), handle_badge()
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-shortest", "-movflags", "+faststart", out_path[:-4] + ".part.mp4"]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    starts, acc = [], 0.0
    for s in shots:
        starts.append(acc)
        acc += s.dur
    for f in range(n):
        T = f / FPS
        i = max(k for k in range(len(shots)) if starts[k] <= T)
        t = T - starts[i]
        frame = shots[i].render(t, T)
        if i > 0 and t < XFADE:
            prev = shots[i - 1].render(shots[i - 1].dur - 0.01 + t, T)
            frame = Image.blend(prev, frame, ease(t / XFADE))
        frame.alpha_composite(_grade())
        if SUBS and ep_label:
            frame.alpha_composite(_bar(ep_label), (0, 0))
            proc.stdin.write(frame.convert("RGB").tobytes())
            continue
        d = ImageDraw.Draw(frame)
        d.rounded_rectangle([40, 64, W - 40, 74], radius=5, fill=(255, 255, 255, 140))
        d.rounded_rectangle([40, 64, 40 + (W - 80) * (T / total), 74], radius=5, fill=(255, 255, 255))
        if shots[i].layout != "end" and ep_label:
            frame.alpha_composite(chip, ((W - chip.width) // 2, 100))
        proc.stdin.write(frame.convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait() == 0:
        import os
        os.replace(out_path[:-4] + ".part.mp4", out_path)
    return out_path, total
