"""ElevenLabs backend for the story voices. Key is read from the ELEVEN_API_KEY environment variable
(or dt/.eleven_key), never written into videos, logs or scripts."""
import hashlib
import json
import os
import subprocess
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "voice_cache_eleven")
os.makedirs(CACHE, exist_ok=True)
API = "https://api.elevenlabs.io/v1"
MODEL = os.environ.get("ELEVEN_MODEL", "eleven_v3")
CAST_FILE = os.path.join(HERE, "eleven_cast.json")   # {"zeynep": voice_id, "zeyto": ..., "ulu": ..., "sinsi": ...}

# per-character delivery + light post effects on top of the chosen voice
# v3 only accepts stability 0.0 (creative), 0.5 (natural), 1.0 (robust)
STYLE = {
    "zeynep": dict(stability=0.5, fx="loudnorm=I=-16:TP=-1.5:LRA=7"),
    "zeyto": dict(stability=0.0, fx="loudnorm=I=-16:TP=-1.5:LRA=7"),
    "ulu": dict(stability=0.5, fx="aecho=0.8:0.6:70|140:0.16|0.08,loudnorm=I=-16:TP=-1.5:LRA=7"),
    "beton": dict(stability=0.5, fx="loudnorm=I=-16:TP=-1.5:LRA=7"),
    "sinsi": dict(stability=0.0, fx="vibrato=f=16:d=0.08,loudnorm=I=-17:TP=-1.5:LRA=7"),
}


def key():
    k = os.environ.get("ELEVEN_API_KEY")
    if not k and os.path.exists(os.path.join(HERE, ".eleven_key")):
        k = open(os.path.join(HERE, ".eleven_key")).read().strip()
    return k


def available():
    return bool(key()) and os.path.exists(CAST_FILE)


def _req(path, body=None, accept="application/json"):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(API + path, data=data, method="POST" if body is not None else "GET",
                               headers={"xi-api-key": key(), "Content-Type": "application/json", "Accept": accept})
    with urllib.request.urlopen(r, timeout=120) as resp:
        return resp.read()


def list_voices():
    return json.loads(_req("/voices"))["voices"]


def line_wav(speaker, text, tag=None):
    cast = json.load(open(CAST_FILE))
    spoken = (f"[{tag}] " if tag else "") + text
    st = STYLE[speaker]
    vid = cast[speaker]
    h = hashlib.md5(f"{MODEL}|{vid}|{json.dumps(st, sort_keys=True)}|{spoken}".encode()).hexdigest()[:16]
    out = os.path.join(CACHE, f"{speaker}_{h}.wav")
    if os.path.exists(out):
        return out
    body = {"text": spoken, "model_id": MODEL, "language_code": "tr",
            "voice_settings": {"stability": st["stability"]}}
    try:
        audio = _req(f"/text-to-speech/{vid}?output_format=mp3_44100_128", body, accept="audio/mpeg")
    except urllib.error.HTTPError as e:
        if e.code == 400 and "language_code" in e.read().decode(errors="ignore"):
            body.pop("language_code")
            audio = _req(f"/text-to-speech/{vid}?output_format=mp3_44100_128", body, accept="audio/mpeg")
        else:
            raise
    mp3 = out[:-4] + ".mp3"
    open(mp3, "wb").write(audio)
    af = st["fx"] + ",silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp3, "-af", af, "-ar", "44100", "-ac", "1", out], check=True)
    return out
