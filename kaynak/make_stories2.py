"""15 sn'lik Instagram hikâye duyuruları — Sezon 2."""
import os, subprocess, sys
import make_stories as ms
from make_s2 import TITLES, FILES
from PIL import ImageDraw
from brand import font, F_BOLD, SUN, CREAM


def build(n):
    base = FILES[n]
    ms.EP[100 + n] = (base, TITLES[n])
    orig_card = ms.card

    def card(bg_png, _n, title, final=False):
        im = orig_card(bg_png, n, title, final=(n == 20))
        d = ImageDraw.Draw(im)
        f = font(F_BOLD, 54)
        t = "SEZON 2"
        d.text(((1080 - f.getlength(t)) / 2, 560), t, font=f, fill=SUN, stroke_width=5, stroke_fill=(0, 0, 0))
        return im
    ms.card = card
    out = ms.build(100 + n)
    ms.card = orig_card
    final = f"out/hikaye/hikaye_s2_bolum_{n:02d}.mp4"
    os.replace(out, final)
    return final


if __name__ == "__main__":
    for x in sys.argv[1:]:
        print(build(int(x)))
