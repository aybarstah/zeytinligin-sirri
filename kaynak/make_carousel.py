import os
from PIL import Image, ImageDraw
from brand import *

W, H = 1080, 1350
OUT = "/home/claude/dt/out/K1_iyi_zeytinyagi_5_isaret/"
N = 7


def icon_calendar(S=800):
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([90, 150, 710, 720], radius=60, fill=CREAM, outline=DARK, width=24)
    d.rounded_rectangle([90, 150, 710, 320], radius=60, fill=OLIVE)
    d.rectangle([90, 260, 710, 320], fill=OLIVE)
    for x in (230, 570):
        d.rounded_rectangle([x - 22, 90, x + 22, 220], radius=20, fill=DARK)
    f = font(F_BOLD, 120)
    txt = "KASIM"
    d.text((400 - f.getlength(txt) / 2, 370), txt, font=f, fill=DARK)
    f2 = font(F_BOLD, 150)
    d.text((400 - f2.getlength("2026") / 2, 500), "2026", font=f2, fill=RED)
    return im


def base(bg, idx):
    im = Image.new("RGBA", (W, H), bg + (255,))
    d = ImageDraw.Draw(im)
    light = sum(bg) / 3 > 160
    deco = tuple(max(0, min(255, v + (-14 if light else 16))) for v in bg)
    d.ellipse([-160, -160, 260, 260], fill=deco)
    d.ellipse([W - 220, H - 300, W + 200, H + 120], fill=deco)
    fg = DARK if light else CREAM
    # handle + page dots
    f = font(F_MED, 32)
    d.text((60, H - 92), HANDLE, font=f, fill=fg)
    for k in range(N):
        x = W - 60 - (N - 1 - k) * 30
        r = 9 if k == idx else 6
        col = fg if k == idx else tuple(int(v * 0.5 + b * 0.5) for v, b in zip(fg, bg))
        d.ellipse([x - r, H - 72 - r, x + r, H - 72 + r], fill=col)
    return im, d, fg


def paste_c(im, src, cx, cy):
    im.alpha_composite(src, (int(cx - src.width / 2), int(cy - src.height / 2)))


def cover():
    bg = OLIVE
    im, d, fg = base(bg, 0)
    paste_c(im, text_image("KAYDET, ALIŞVERİŞTE AÇ", 34, DARK, 900, pill=SUN, pad=(30, 12)), W / 2, 150)
    paste_c(im, fit(icon_bottle(), width=420), W / 2, 470)
    paste_c(im, text_image("Market rafında kanma!", 92, SUN, 960), W / 2, 830)
    paste_c(im, text_image("İyi zeytinyağının 5 işareti", 58, CREAM, 960, path=F_MED), W / 2, 1010)
    t = text_image("Kaydır", 40, CREAM, 400, path=F_MED)
    paste_c(im, t, W / 2 - 40, 1140)
    paste_c(im, fit(icon_arrow(), width=70), W / 2 + t.width / 2 + 10, 1142)
    return im


def tip(idx, num, title, body, icon):
    bg = CREAM
    im, d, fg = base(bg, idx)
    d.ellipse([60, 80, 200, 220], fill=RED)
    paste_c(im, text_image(str(num), 92, CREAM, 200), 130, 152)
    paste_c(im, text_image(title, 84, DARK, 760, align="left"), 230 + text_image(title, 84, DARK, 760, align="left").width / 2, 152)
    paste_c(im, icon, W / 2, 560)
    paste_c(im, text_image(body, 50, DARK, 900, path=F_MED, line_gap=1.25), W / 2, 1005)
    return im


def acid_visual():
    im = Image.new("RGBA", (700, 460), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 699, 459], radius=60, fill=OLIVE)
    f = font(F_BOLD, 200)
    t = "≤ %0,8"
    d.text((350 - f.getlength(t) / 2, 60), t, font=f, fill=SUN)
    f2 = font(F_MED, 46)
    t2 = "serbest asitlik"
    d.text((350 - f2.getlength(t2) / 2, 330), t2, font=f2, fill=CREAM)
    return im


def cta():
    bg = RED
    im, d, fg = base(bg, N - 1)
    from characters import muhendis, zeyto
    m = muhendis(1, False, -30)
    m = m.crop(m.getbbox())
    m = fit(m, height=720)
    im.alpha_composite(m, (40, H - 120 - m.height))
    z = fit(zeyto(GREEN_OLIVE, 0, False, "happy", -6, 1), height=330)
    im.alpha_composite(z, (W - 60 - z.width, H - 150 - z.height))
    paste_c(im, text_image("Bizim şişede\nbeşi de var.", 92, CREAM, 960), W / 2, 230)
    paste_c(im, text_image("Yeni sezon ön sipariş için DM", 46, RED, 960, pill=CREAM, pad=(40, 18)), W / 2, 450)
    paste_c(im, text_image("Kaydet · Paylaş · Etiketle", 38, CREAM, 600, path=F_MED), W - 330, 590)
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    slides = [cover()]
    slides.append(tip(1, 1, "Kokusu", "Taze çimen, yeşil elma ya da enginar gibi kokar. Küf, sirke veya şarap kokusu kötü işarettir.", fit(icon_leaf(), width=500)))
    slides.append(tip(2, 2, "Acılığı", "Boğazda hafif yakma ve acılık kusur değil; tazeliğin ve polifenolün işaretidir.", fit(icon_olive(GREEN_OLIVE), width=500)))
    slides.append(tip(3, 3, "Şişesi", "Işık yağı bozar. Koyu renkli cam ya da teneke ambalajı seç.", fit(icon_bottle(), width=480)))
    slides.append(tip(4, 4, "Hasat tarihi", "Son kullanma tarihine değil, hasat tarihine bak. Yeni sezon en tazesidir.", fit(icon_calendar(), width=480)))
    slides.append(tip(5, 5, "Asit oranı", "Natürel sızmada serbest asitlik en fazla %0,8'dir. Ne kadar düşükse o kadar iyi.", acid_visual()))
    slides.append(cta())
    paths = []
    for k, s in enumerate(slides, 1):
        p = f"{OUT}slayt_{k}.png"
        s.convert("RGB").save(p, optimize=True)
        paths.append(p)
    print("\n".join(paths))


if __name__ == "__main__":
    main()
