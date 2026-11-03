"""Procedural soundtrack for Mühendisin Defteri: cheerful plucked loop + pop / ding / whoosh effects.
Everything is synthesised with numpy (no samples, no network)."""
import json
import sys
import wave
import numpy as np

SR = 44100
rng = np.random.default_rng(7)


def note_hz(n):  # MIDI note -> Hz
    return 440.0 * 2 ** ((n - 69) / 12)


def pluck(freq, dur, amp=0.3, bright=0.5):
    """Karplus-Strong plucked string (ukulele / guitar feel)."""
    n = int(SR * dur)
    period = max(2, int(SR / freq))
    buf = rng.uniform(-1, 1, period)
    out = np.empty(n)
    decay = 0.996
    for i in range(n):
        out[i] = buf[i % period]
        nxt = buf[(i + 1) % period]
        buf[i % period] = decay * 0.5 * (out[i] + nxt)
    env = np.minimum(1, np.linspace(0, 40, n)) * np.exp(-np.linspace(0, 3.2, n))
    return out * env * amp


def tone(freq, dur, amp=0.2, kind="sine", attack=0.005, release=0.25):
    t = np.arange(int(SR * dur)) / SR
    if kind == "sine":
        w = np.sin(2 * np.pi * freq * t)
    else:
        w = 2 * (t * freq % 1) - 1
    env = np.minimum(1, t / attack) * np.exp(-t / release)
    return w * env * amp


def add(buf, sig, at):
    i = int(at * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i]


# --------------------------------------------------------------- music
CHORDS = [  # C  G  Am  F  (MIDI root + triad) — sunny I-V-vi-IV
    (48, [60, 64, 67]), (43, [59, 62, 67]), (45, [57, 60, 64]), (41, [57, 60, 65])]
MELODY = [  # one 4-bar phrase, (beat, midi) on an 8th-note grid
    (0, 76), (1, 74), (1.5, 72), (2, 74), (3, 76), (4, 74), (5, 71), (6, 72), (7, 74),
    (8, 72), (9, 72), (10, 69), (11, 72), (12, 74), (13, 72), (14, 69), (15, 67)]


def music(total, bpm=112):
    beat = 60 / bpm
    bar = 4 * beat
    out = np.zeros(int(SR * (total + 2)))
    cache = {}

    def pl(m, d, a, b=0.5):
        k = (m, round(d, 2), a)
        if k not in cache:
            cache[k] = pluck(note_hz(m), d, a, b)
        return cache[k]

    t, bar_i = 0.0, 0
    while t < total:
        root, triad = CHORDS[bar_i % 4]
        # bass on 1 and 3
        for b in (0, 2):
            add(out, tone(note_hz(root), beat * 1.6, 0.08, "sine", release=0.3), t + b * beat)
        # strummed chord on off-beats (ukulele feel)
        for b in (0.5, 1.5, 2.5, 3.0, 3.5):
            for k, m in enumerate(triad):
                add(out, pl(m, beat * 1.2, 0.13), t + b * beat + k * 0.012)
        # melody every other 4-bar phrase, quieter so it sits under speech
        phrase_pos = bar_i % 8
        if phrase_pos < 4:
            for bt, m in MELODY:
                if phrase_pos * 4 <= bt / 2 < phrase_pos * 4 + 4:
                    add(out, pl(m, beat * 0.9, 0.11, 0.6), t + (bt / 2 - phrase_pos * 4) * beat)
        # soft shaker on 8ths
        for k in range(8):
            sh = rng.normal(0, 1, int(SR * 0.05)) * np.exp(-np.linspace(0, 9, int(SR * 0.05)))
            add(out, sh * (0.02 if k % 2 else 0.012), t + k * beat / 2)
        t += bar
        bar_i += 1
    out = out[: int(SR * total)]
    fade = int(SR * 1.2)
    out[-fade:] *= np.linspace(1, 0, fade)
    out[: int(SR * 0.3)] *= np.linspace(0, 1, int(SR * 0.3))
    return out


# --------------------------------------------------------------- effects
def sfx_pop():
    t = np.arange(int(SR * 0.09)) / SR
    f = 500 + 900 * (t / t[-1])
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.03) * 0.22


def sfx_ding():
    return tone(1568, 0.6, 0.12, release=0.25) + tone(2093, 0.6, 0.07, release=0.18)


def sfx_whoosh():
    n = int(SR * 0.4)
    noise = rng.normal(0, 1, n)
    # sweep a simple one-pole low-pass cutoff up then down
    cut = np.sin(np.linspace(0, np.pi, n)) * 0.25 + 0.02
    y = np.zeros(n)
    acc = 0.0
    for i in range(n):
        acc += cut[i] * (noise[i] - acc)
        y[i] = acc
    return y * np.sin(np.linspace(0, np.pi, n)) * 0.35


def sfx_end():
    out = np.zeros(int(SR * 1.2))
    for k, m in enumerate([72, 76, 79, 84]):
        add(out, tone(note_hz(m), 0.6, 0.10, release=0.3), k * 0.09)
    return out


def soundtrack(ev):
    total = ev["total"]
    n = int(SR * total)
    voices = ev.get("voice", [])
    bg = music(total)
    bg = bg / (np.max(np.abs(bg)) + 1e-9)
    fx = np.zeros(n)
    pop, ding, whoosh = sfx_pop(), sfx_ding(), sfx_whoosh()
    if not voices:  # silent-dialogue version keeps the bubble pops
        for ln in ev["lines"]:
            add(fx, pop, ln["t"])
    for c in ev["cards"]:
        add(fx, ding * 0.8, c)
    for c in ev["cuts"]:
        add(fx, whoosh * 0.8, max(0, c - 0.12))
    if "end" in ev:
        add(fx, sfx_end(), ev["end"] + 0.1)
    speech = np.zeros(n)
    active = np.zeros(n)
    for v in voices:
        with wave.open(v["wav"]) as w:
            d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
        add(speech, d, v["t"])
        i = int(v["t"] * SR)
        active[i:min(n, i + len(d))] = 1.0
    if voices:
        # smooth the ducking curve (~150 ms attack/release)
        k = int(SR * 0.15)
        kern = np.ones(k) / k
        active = np.convolve(active, kern, mode="same")
        music_gain = 0.30 - 0.20 * active        # music: 0.30 alone, 0.10 under speech
        mix = bg * music_gain + fx * 0.6 + speech * 0.95
    else:
        mix = bg * 0.45 + fx
    mix = np.tanh(mix * 1.2) / 1.2  # gentle limiter
    peak = np.max(np.abs(mix)) or 1
    mix = mix / peak * 0.89
    st = np.stack([mix, mix], axis=1)
    return (st * 32767).astype(np.int16)


def write_wav(path, data):
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


if __name__ == "__main__":
    for evp in sys.argv[1:]:
        ev = json.load(open(evp))
        wav = evp.replace(".events.json", ".wav")
        write_wav(wav, soundtrack(ev))
        print(wav)
