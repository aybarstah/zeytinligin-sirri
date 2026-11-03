"""Tiny scene-based animation engine: renders brand Reels (1080x1920) to mp4 via ffmpeg."""
import math
import subprocess
from PIL import Image, ImageDraw
from brand import font, F_BOLD, F_MED, CREAM, DARK, HANDLE, draw_olive, GREEN_OLIVE

W, H, FPS = 1080, 1920, 30
WIPE = 0.38


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out_cubic(p):
    return 1 - (1 - p) ** 3


def ease_out_back(p, s=1.9):
    p -= 1
    return p * p * ((s + 1) * p + s) + 1


def shade(c, k):
    return tuple(int(clamp(v + k, 0, 255)) for v in c)


def is_light(c):
    return sum(c) / 3 > 160


class El:
    def __init__(self, img, y, x=W // 2, delay=0.0, anim="up", float_amp=0, pulse=0.0):
        self.img, self.x, self.y, self.delay = img, x, y, delay
        self.anim, self.float_amp, self.pulse = anim, float_amp, pulse
        self._cache = {}

    def scaled(self, s):
        k = round(s, 2)
        if k not in self._cache:
            w, h = max(1, int(self.img.width * k)), max(1, int(self.img.height * k))
            self._cache[k] = self.img.resize((w, h), Image.LANCZOS)
        return self._cache[k]

    def draw(self, frame, t):
        te = t - self.delay
        if te < 0:
            return
        p = clamp(te / 0.45)
        scale, alpha, dy = 1.0, 1.0, 0.0
        if self.anim == "up":
            alpha, dy = p, (1 - ease_out_cubic(p)) * 90
        elif self.anim == "pop":
            scale, alpha = max(0.01, ease_out_back(p)), clamp(p * 2.5)
        elif self.anim == "left":
            alpha = p
            dx = -(1 - ease_out_cubic(p)) * 140
        if self.float_amp and p >= 1:
            dy += math.sin(te * 2.2) * self.float_amp
        if self.pulse and p >= 1:
            scale *= 1 + self.pulse * (0.5 + 0.5 * math.sin(te * 6))
        im = self.scaled(scale) if abs(scale - 1) > 0.005 else self.img
        if alpha < 0.999:
            im = im.copy()
            a = im.getchannel("A").point(lambda v: int(v * alpha))
            im.putalpha(a)
        x = int(self.x - im.width / 2 + (dx if self.anim == "left" else 0))
        y = int(self.y - im.height / 2 + dy)
        frame.alpha_composite(im, (max(-im.width, x), y) if x >= 0 else (0, y))


def _handle_badge(dark_text):
    col = DARK if dark_text else CREAM
    fnt = font(F_MED, 34)
    w = int(fnt.getlength(HANDLE)) + 70
    im = Image.new("RGBA", (w, 56), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    draw_olive(d, 22, 30, 16, GREEN_OLIVE)
    d.text((48, 4), HANDLE, font=fnt, fill=col)
    return im


def render(scenes, out_path):
    """scenes: list of dict(bg=(r,g,b), dur=float, els=[El,...])."""
    total = sum(s["dur"] for s in scenes)
    n = int(total * FPS)
    starts, acc = [], 0.0
    for s in scenes:
        starts.append(acc)
        acc += s["dur"]
    badges = {True: _handle_badge(True), False: _handle_badge(False)}
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-shortest", "-movflags", "+faststart", out_path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(n):
        T = f / FPS
        i = max(k for k in range(len(scenes)) if starts[k] <= T)
        sc, t = scenes[i], T - starts[i]
        bg = sc["bg"]
        frame = Image.new("RGBA", (W, H), scenes[i - 1]["bg"] + (255,) if i > 0 else bg + (255,))
        d = ImageDraw.Draw(frame)
        if i > 0 and t < WIPE:
            r = ease_out_cubic(t / WIPE) * math.hypot(W, H)
            d.ellipse([W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r], fill=bg)
        else:
            d.rectangle([0, 0, W, H], fill=bg)
        # drifting decorative blobs
        deco = shade(bg, -14 if is_light(bg) else 16)
        for k, (bx, by, br) in enumerate([(0.12, 0.2, 170), (0.9, 0.36, 230), (0.15, 0.78, 260), (0.85, 0.9, 150)]):
            ox = math.sin(T * 0.6 + k) * 30
            oy = math.cos(T * 0.5 + k * 2) * 30
            d.ellipse([bx * W - br + ox, by * H - br + oy, bx * W + br + ox, by * H + br + oy], fill=deco)
        for el in sc["els"]:
            el.draw(frame, t)
        # story-style progress bar + handle
        light = is_light(bg)
        barc = DARK if light else CREAM
        seg_w = (W - 80 - 10 * (len(scenes) - 1)) / len(scenes)
        for k in range(len(scenes)):
            x0 = 40 + k * (seg_w + 10)
            d.rounded_rectangle([x0, 70, x0 + seg_w, 80], radius=5, fill=shade(bg, -35 if light else 40))
            fillp = 1.0 if k < i else (clamp(t / sc["dur"]) if k == i else 0)
            if fillp > 0:
                d.rounded_rectangle([x0, 70, x0 + seg_w * fillp, 80], radius=5, fill=barc)
        b = badges[light]
        frame.alpha_composite(b, ((W - b.width) // 2, 110))
        proc.stdin.write(frame.convert("RGB").tobytes())
    proc.stdin.close()
    proc.wait()
    return out_path
