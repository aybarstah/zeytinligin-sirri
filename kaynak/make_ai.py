"""AI-image episodes: one still per line (scene images supplied by the user), Ken Burns motion,
crossfades, 'BÖLÜM N' header bar, karaoke subtitles (current word yellow), ElevenLabs voices, soundtrack."""
import glob
import json
import math
import os
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import story
from story import line_wav, read_wav, envelope
from brand import CREAM, SUN, DARK, RED, OLIVE

W, H, FPS = 1080, 1920, 30
XF = 0.35
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
NAMES = {"zeynep": ("Mühendis", (120, 170, 80)), "zeyto": ("Zeyto", (240, 120, 120)), "ulu": ("Ulu", (200, 160, 110)),
         "sinsi": ("Sinsi", (230, 140, 60)), "beton": ("Beton Bey", (180, 184, 196)), "muhtar": ("Muhtar", (200, 170, 120))}


def ease(p):
    return 1 - (1 - p) ** 3


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def load_scene(path, overlay=None):
    im = Image.open(path).convert("RGB")
    im = ImageOps.fit(im, (int(W * 1.12), int(H * 1.12)), Image.LANCZOS, centering=(0.5, 0.45))
    im = im.convert("RGBA")
    if overlay:
        overlay(im)
    # soft vignette + darker bottom for subtitles
    vig = Image.new("L", im.size, 0)
    vd = ImageDraw.Draw(vig)
    for k in range(40):
        a = int(150 * (k / 40) ** 2)
        vd.rectangle([0, int(im.height * (0.72 + 0.28 * k / 40)), im.width, im.height], fill=a)
    shade = Image.new("RGBA", im.size, (0, 0, 0, 255))
    shade.putalpha(vig)
    im.alpha_composite(shade)
    return im


def kb_frame(img, p, direction):
    """Ken Burns: slow zoom 1.0 -> 1.08 with a small drift."""
    z = 1.0 + 0.08 * ease(p)
    cw, ch = W / z * 1.0, H / z * 1.0
    base_w, base_h = img.size
    sx = base_w / (W * 1.12)
    cw, ch = cw * sx * 1.0, ch * sx
    dx = (base_w - cw) * (0.5 + 0.18 * direction * (p - 0.5))
    dy = (base_h - ch) * (0.45 - 0.08 * (p - 0.5))
    return img.crop((int(dx), int(dy), int(dx + cw), int(dy + ch))).resize((W, H), Image.BILINEAR)


def header(label):
    bar = Image.new("RGBA", (W, 170), (0, 0, 0, 255))
    d = ImageDraw.Draw(bar)
    size = 88
    f = ImageFont.truetype(SERIF, size)
    while f.getlength(label) > W - 90 and size > 40:
        size -= 4
        f = ImageFont.truetype(SERIF, size)
    tw = f.getlength(label)
    d.text(((W - tw) / 2 + 3, 40 + 4), label, font=f, fill=(60, 60, 60))
    d.text(((W - tw) / 2, 40), label, font=f, fill=(255, 255, 255))
    return bar


def word_times(text, vlen, env):
    """Spread words over the audio by character weight, starting where the voice actually starts."""
    words = text.split()
    voiced = [i for i, e in enumerate(env) if e > 0.12]
    t0 = (voiced[0] / 30) if voiced else 0.0
    t1 = ((voiced[-1] + 1) / 30) if voiced else vlen
    weights = [len(w) + 2 for w in words]
    tot = sum(weights)
    out, acc = [], t0
    for w, wt in zip(words, weights):
        dur = (t1 - t0) * wt / tot
        out.append((w, acc, acc + dur))
        acc += dur
    return out


def chunks(words, maxchars=22):
    groups, cur = [], []
    for w in words:
        if cur and (sum(len(x[0]) + 1 for x in cur) + len(w[0]) > maxchars):
            groups.append(cur)
            cur = []
        cur.append(w)
        if w[0][-1] in ".?!":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return groups


FSUB = ImageFont.truetype(SANS, 76)
FNAME = ImageFont.truetype(SANS, 38)


def draw_subtitle(frame, speaker, group, lt, y0=1560):
    d = ImageDraw.Draw(frame)
    words = [g[0] for g in group]
    space = FSUB.getlength(" ")
    widths = [FSUB.getlength(w) for w in words]
    total = sum(widths) + space * (len(words) - 1)
    lines, cur, cw = [], [], 0
    for i, w in enumerate(widths):
        if cur and cw + space + w > W - 120:
            lines.append(cur)
            cur, cw = [], 0
        cur.append(i)
        cw += (space if len(cur) > 1 else 0) + w
    lines.append(cur)
    y = y0 - (len(lines) - 1) * 96
    name, col = NAMES[speaker]
    nw = FNAME.getlength(name) + 40
    d.rounded_rectangle([(W - nw) / 2, y - 78, (W + nw) / 2, y - 22], radius=26, fill=col + (235,))
    d.text(((W - nw) / 2 + 20, y - 76), name, font=FNAME, fill=(25, 25, 25))
    for ln in lines:
        lw = sum(widths[i] for i in ln) + space * (len(ln) - 1)
        x = (W - lw) / 2
        for i in ln:
            w, a, b = group[i]
            on = a <= lt < b + 0.05
            past = lt >= b
            fill = SUN if on else (255, 255, 255)
            d.text((x, y), w, font=FSUB, fill=fill, stroke_width=7, stroke_fill=(0, 0, 0))
            x += widths[i] + space
        y += 96


def end_card(img, l1, l2, cta, p):
    frame = img.copy()
    dark = Image.new("RGBA", frame.size, (0, 0, 0, int(150 * clamp(p * 2))))
    frame.alpha_composite(dark)
    d = ImageDraw.Draw(frame)
    for k, (txt, size, col, y, delay) in enumerate([(l1, 64, (255, 255, 255), 720, 0.0), (l2, 104, SUN, 840, 0.15), (cta, 56, (255, 255, 255), 1010, 0.3)]):
        a = clamp((p - delay) * 3)
        if a <= 0:
            continue
        f = ImageFont.truetype(SANS, size)
        tw = f.getlength(txt)
        d.text(((W - tw) / 2, y + (1 - a) * 40), txt, font=f, fill=col + (int(255 * a),), stroke_width=6, stroke_fill=(0, 0, 0, int(255 * a)))
    return frame


def build(lines, mapping, img_dir, label, out_path, end=None, overlays=None, lead=0.4):
    """lines: [(speaker, text, opts)], mapping: scene id per line ('S01'...), end=(l1, l2, cta)."""
    overlays = overlays or {}
    scenes = {}
    for sid in sorted(set(mapping)):
        path = sorted(glob.glob(os.path.join(img_dir, sid + ".*")))[0]
        scenes[sid] = load_scene(path, overlays.get(sid))
    # timeline
    tl, t = [], lead
    for (sp, text, opts), sid in zip(lines, mapping):
        path = line_wav(sp, text, opts.get("tag"))
        data, sr = read_wav(path)
        vlen = len(data) / sr
        env = envelope(data, sr)
        gap = opts.get("gap", 0.3)
        tl.append(dict(sp=sp, text=text, sid=sid, t=t, vlen=vlen, dur=vlen + gap, env=env, wav=path,
                       groups=chunks(word_times(text, vlen, env))))
        t += vlen + gap
    end_len = 3.6 if end else 0.0
    total = t + 0.3 + end_len
    # scene segments (consecutive same image = one segment)
    segs = []
    for item in tl:
        if segs and segs[-1]["sid"] == item["sid"]:
            segs[-1]["t1"] = item["t"] + item["dur"]
        else:
            segs.append(dict(sid=item["sid"], t0=item["t"] if segs else 0.0, t1=item["t"] + item["dur"]))
    segs[-1]["t1"] = t + 0.3
    for k, s in enumerate(segs):
        s["dir"] = 1 if k % 2 == 0 else -1
    # events for the soundtrack
    ev = {"lines": [{"t": round(i["t"], 2), "dur": round(i["dur"], 2), "speaker": i["sp"], "text": i["text"]} for i in tl],
          "cards": [], "cuts": [s["t0"] for s in segs[1:]], "total": total,
          "voice": [{"t": round(i["t"], 3), "wav": i["wav"], "len": round(i["vlen"], 3)} for i in tl]}
    if end:
        ev["end"] = t + 0.3
    json.dump(ev, open(out_path[:-4] + ".events.json", "w"), ensure_ascii=False, indent=1)

    bar = header(label)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
           out_path[:-4] + ".part.mp4"]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(total * FPS)
    last_seg_frame = None
    for f in range(n):
        T = f / FPS
        if end and T >= t + 0.3:
            p = (T - t - 0.3) / end_len
            frame = end_card(last_seg_frame, *end, p)
        else:
            k = max(i for i, s in enumerate(segs) if s["t0"] <= T or i == 0)
            s = segs[k]
            p = clamp((T - s["t0"]) / max(0.1, s["t1"] - s["t0"]))
            frame = kb_frame(scenes[s["sid"]], p, s["dir"])
            if k > 0 and T - s["t0"] < XF:
                ps = segs[k - 1]
                prev = kb_frame(scenes[ps["sid"]], 1.0, ps["dir"])
                frame = Image.blend(prev, frame, ease((T - s["t0"]) / XF))
            last_seg_frame = frame
            # subtitle
            li = max([i for i, it in enumerate(tl) if it["t"] <= T] or [0])
            it = tl[li]
            lt = T - it["t"]
            if 0 <= lt < it["dur"]:
                g = next((g for g in it["groups"] if lt < g[-1][2] + 0.05), it["groups"][-1])
                if lt < it["vlen"] + 0.25:
                    frame = frame.copy()
                    draw_subtitle(frame, it["sp"], g, lt)
        frame = frame.copy()
        frame.alpha_composite(bar, (0, 0))
        proc.stdin.write(frame.convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait() == 0:
        os.replace(out_path[:-4] + ".part.mp4", out_path)
    return out_path, total


def capture_lines(module, ep):
    """Reuse the dialogue (texts, tags, gaps) of an existing scripted episode."""
    cap = {}
    module.render_episode = lambda shots, label, out: cap.setdefault("s", shots)
    getattr(module, ep)()
    lines = []
    for sh in cap["s"]:
        for sp, text, opts in sh.lines:
            if text:
                o = dict(opts)
                o.setdefault("gap", 0.3)
                lines.append((sp, text, o))
    return lines
