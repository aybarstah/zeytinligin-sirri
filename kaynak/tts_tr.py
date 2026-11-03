"""Offline Turkish TTS: rule-based Turkish G2P (espeak-style IPA) + Piper VITS voices via onnxruntime.
Mühendis = fahrettin (CC0), Zeyto = fettah (CC0) pitched up into a cartoon voice."""
import hashlib
import json
import os
import re
import subprocess
import wave
import numpy as np
import onnxruntime as ort

HERE = os.path.dirname(os.path.abspath(__file__))
VDIR = os.path.join(HERE, "voices")
CACHE = os.path.join(HERE, "voice_cache")
os.makedirs(CACHE, exist_ok=True)

# ------------------------------------------------------------------ text normalisation
ONES = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
TENS = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]


def num_tr(n):
    n = int(n)
    if n == 0:
        return "sıfır"
    out = []
    if n >= 1000:
        k = n // 1000
        out.append("bin" if k == 1 else num_tr(k) + " bin")
        n %= 1000
    if n >= 100:
        h = n // 100
        out.append("yüz" if h == 1 else ONES[h] + " yüz")
        n %= 100
    if n >= 10:
        out.append(TENS[n // 10])
        n %= 10
    if n:
        out.append(ONES[n])
    return " ".join(out)


def normalise(t):
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("…", "...")
    t = re.sub(r"%\s*(\d+),(\d+)", lambda m: "yüzde " + num_tr(m.group(1)) + " virgül " + num_tr(m.group(2)), t)
    t = re.sub(r"%\s*(\d+)", lambda m: "yüzde " + num_tr(m.group(1)), t)
    t = re.sub(r"(\d+)\s*-\s*(\d+)", lambda m: m.group(1) + " ile " + m.group(2), t)
    t = re.sub(r"(\d+)\s*°C", lambda m: m.group(1) + " derece", t)
    t = re.sub(r"(\d+)\s*L\b", lambda m: m.group(1) + " litre", t)
    t = re.sub(r"(\d+)\s*g\b", lambda m: m.group(1) + " gram", t)
    t = re.sub(r"\d+", lambda m: num_tr(m.group(0)), t)
    t = re.sub(r"\bBr+\b", "Bırrr", t)
    t = re.sub(r"\bBz+\b", "Vızzz", t)
    t = re.sub(r"\bHm+\b", "Hımm", t)
    t = re.sub(r"\bDM'den\b", "di emden", t)
    t = re.sub(r"\bDM\b", "di em", t)
    t = t.replace("'", "").replace('"', "")
    t = re.sub(r"\?!+|!\?+", "?", t)
    t = re.sub(r"\.\.\.", ",", t)
    t = re.sub(r"[:;]", ",", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


# ------------------------------------------------------------------ G2P
FRONT = set("eiöü")
BACK = set("aıou")
VOWELS = FRONT | BACK
V_IPA = {"a": "a", "e": "e", "ı": "ɯ", "i": "i", "o": "o", "ö": "ø", "u": "u", "ü": "y", "â": "a", "î": "i", "û": "u"}
C_IPA = {"b": "b", "c": "dʒ", "ç": "tʃ", "d": "d", "f": "f", "h": "h", "j": "ʒ", "m": "m", "n": "n", "p": "p",
         "r": "ɾ", "s": "s", "ş": "ʃ", "t": "t", "v": "v", "y": "j", "z": "z", "x": "ks", "w": "v", "q": "k"}


def lower_tr(s):
    return s.replace("I", "ı").replace("İ", "i").lower()


def word_ipa(w):
    w = lower_tr(w)
    out = []          # list of (ipa, is_vowel)
    for i, ch in enumerate(w):
        nxt = w[i + 1] if i + 1 < len(w) else ""
        prv = w[i - 1] if i else ""
        # nearest vowel for front/back consonant colouring
        near = nxt if nxt in VOWELS else (prv if prv in VOWELS else "")
        if ch in V_IPA:
            out.append((V_IPA[ch], True))
        elif ch == "ğ":
            if prv in VOWELS and nxt not in VOWELS:
                out.append(("ː", False))      # lengthen previous vowel
            elif prv in FRONT and nxt in VOWELS:
                out.append(("j", False))
            # between back vowels it is silent
        elif ch == "k":
            out.append(("c" if near in FRONT else "k", False))
        elif ch == "g":
            out.append(("ɟ" if near in FRONT else "ɡ", False))
        elif ch == "l":
            out.append(("l" if near in FRONT or not near else "ɫ", False))
        elif ch in C_IPA:
            out.append((C_IPA[ch], False))
    if not out:
        return ""
    # final-syllable stress: put ˈ before the onset consonant of the last vowel
    vidx = [i for i, (_, v) in enumerate(out) if v]
    if vidx:
        last = vidx[-1]
        pos = last - 1 if last > 0 and not out[last - 1][1] and out[last - 1][0] != "ː" else last
        if len(vidx) == 1:
            pos = 0
        out.insert(pos, ("ˈ", False))
    return "".join(p for p, _ in out)


ESPEAK = os.path.join(HERE, "espeak", "bin", "espeak-ng")


def espeak_ipa(chunk):
    r = subprocess.run([ESPEAK, "-v", "tr", "-q", "--ipa"], input=chunk, capture_output=True, text=True, check=True)
    return " ".join(l.strip() for l in r.stdout.splitlines() if l.strip())


def to_phonemes(text):
    """Same scheme Piper uses: espeak-ng IPA per clause, clause punctuation kept between them."""
    text = normalise(text)
    out = []
    for chunk, punct in re.findall(r"([^,.!?]+)([,.!?]*)", text):
        chunk = chunk.strip()
        if not chunk:
            continue
        ipa = espeak_ipa(chunk)
        p = (punct[:1] or ",") if punct else ""
        out.append(ipa + p)
    s = " ".join(out).strip()
    if s and s[-1] not in ".!?":
        s = s.rstrip(",") + "."
    return s


def to_phonemes_rules(text):
    text = normalise(text)
    parts = re.findall(r"[A-Za-zÇĞİÖŞÜçğıöşüâîû]+|[,.!?]", text)
    res = []
    for p in parts:
        if p in ",.!?":
            if res and res[-1] == " ":
                res.pop()
            res.append(p)
            res.append(" ")
        else:
            res.append(word_ipa(p))
            res.append(" ")
    s = "".join(res).strip()
    if s and s[-1] not in ".!?":
        s += "."
    return s


# ------------------------------------------------------------------ synthesis
_SESS = {}


def _load(voice):
    if voice not in _SESS:
        base = os.path.join(VDIR, f"tr_TR-{voice}-medium.onnx")
        cfg = json.load(open(base + ".json"))
        opts = ort.SessionOptions()
        opts.intra_op_num_threads = 2
        _SESS[voice] = (ort.InferenceSession(base, opts, providers=["CPUExecutionProvider"]), cfg)
    return _SESS[voice]


def synth_raw(phon, voice, length_scale=1.0, noise=0.6, noise_w=0.7):
    sess, cfg = _load(voice)
    pmap = cfg["phoneme_id_map"]
    ids = [pmap["^"][0], pmap["_"][0]]
    for ch in phon:
        if ch in pmap:
            ids += [pmap[ch][0], pmap["_"][0]]
    ids.append(pmap["$"][0])
    x = np.array([ids], dtype=np.int64)
    audio = sess.run(None, {"input": x, "input_lengths": np.array([x.shape[1]], dtype=np.int64),
                            "scales": np.array([noise, length_scale, noise_w], dtype=np.float32)})[0]
    return audio.squeeze().astype(np.float32), cfg["audio"]["sample_rate"]


SPEAKERS = {
    "ulu": ("fahrettin", 1.0, "asetrate=22050*0.80,aresample=44100,atempo=1.08,lowpass=f=6000,"
                              "aecho=0.8:0.6:70|140:0.22|0.12,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,loudnorm=I=-16:TP=-1.5:LRA=7"),
    "sinsi": ("fettah", 0.95, "asetrate=22050*1.55,aresample=44100,atempo=0.72,vibrato=f=22:d=0.25,highpass=f=250,"
                              "acompressor=threshold=-20dB:ratio=3:attack=5:release=80,loudnorm=I=-17:TP=-1.5:LRA=7"),
    # name: (voice, length_scale, ffmpeg post-filter)
    "zeynep": ("fahrettin", 1.06, "highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,loudnorm=I=-16:TP=-1.5:LRA=7"),
    "zeyto": ("fettah", 0.95, "asetrate=22050*1.42,aresample=44100,atempo=0.68,highpass=f=120,"
                              "acompressor=threshold=-20dB:ratio=3:attack=5:release=80,loudnorm=I=-16:TP=-1.5:LRA=7"),
}


def line_wav(speaker, text):
    """Returns path of a 44.1 kHz mono wav for this line (cached)."""
    voice, ls, filt = SPEAKERS[speaker]
    key = hashlib.md5(f"v6|{speaker}|{text}".encode()).hexdigest()[:16]
    out = os.path.join(CACHE, f"{speaker}_{key}.wav")
    if os.path.exists(out):
        return out
    phon = to_phonemes(text)
    audio, sr = synth_raw(phon, voice, ls)
    raw = out[:-4] + ".raw.wav"
    pcm = np.clip(audio / (np.max(np.abs(audio)) + 1e-6) * 0.9, -1, 1)
    with wave.open(raw, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((pcm * 32767).astype(np.int16).tobytes())
    af = filt + ",silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-af", af, "-ar", "44100", "-ac", "1", out], check=True)
    os.remove(raw)
    return out


def read_wav(path):
    with wave.open(path) as w:
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        return data, w.getframerate()


def envelope(data, sr, fps=30):
    hop = sr // fps
    n = len(data) // hop + 1
    env = np.array([np.sqrt(np.mean(data[i * hop:(i + 1) * hop] ** 2)) if i * hop < len(data) else 0 for i in range(n)])
    return env / (env.max() + 1e-6)


if __name__ == "__main__":
    import sys
    for s in sys.argv[1:] or ["Günaydın Zeyto! Korkma, kasım geldi. Hasat zamanı!"]:
        print(to_phonemes(s))
