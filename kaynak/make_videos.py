import sys
from brand import *
from video import El, render, is_light, W

OUT = "/home/claude/dt/out/"


def T(text, size, y, bg, delay=0.0, anim="up", path=F_BOLD, color=None, maxw=900, pill=None, pad=(36, 18), **kw):
    col = color or (DARK if is_light(bg) else CREAM)
    return El(text_image(text, size, col, maxw, path=path, pill=pill, pad=pad), y, delay=delay, anim=anim, **kw)


def I(img, y, width, delay=0.0, x=W // 2, anim="pop", **kw):
    return El(fit(img, width=width), y, x=x, delay=delay, anim=anim, **kw)


def video1():
    s = []
    bg = OLIVE
    s.append(dict(bg=bg, dur=3.2, els=[
        I(icon_branch(), 560, 820, 0.0, float_amp=10),
        T("Kasım geldi,", 92, 1000, bg, 0.25),
        T("zeytinler kapkara oldu!", 92, 1180, bg, 0.5, color=SUN),
    ]))
    bg = DARK
    s.append(dict(bg=bg, dur=3.0, els=[
        T("ZEYTİN", 60, 380, bg, 0.1, pill=SUN, color=DARK),
        I(icon_olive(BLACKOLIVE), 720, 520, 0.2, float_amp=10),
        T("Hasat zamanı!", 96, 1080, bg, 0.4),
        T("Yeni sezon zeytinyağı ve sofralık zeytin", 50, 1240, bg, 0.65, path=F_MED, maxw=820),
    ]))
    bg = RED
    s.append(dict(bg=bg, dur=3.0, els=[
        T("MEYVE", 60, 380, bg, 0.1, pill=CREAM, color=RED),
        I(icon_pomegranate(), 720, 520, 0.2, float_amp=10),
        T("Nar · Ayva · Hurma", 84, 1080, bg, 0.4),
        T("Mandalina · Kivi · Elma", 60, 1220, bg, 0.6, path=F_MED),
    ]))
    bg = OLIVE
    s.append(dict(bg=bg, dur=3.0, els=[
        T("SEBZE", 60, 380, bg, 0.1, pill=CREAM, color=OLIVE),
        I(icon_leaf(), 720, 520, 0.2, float_amp=10),
        T("Ispanak · Pırasa", 88, 1080, bg, 0.4),
        T("Karnabahar · Lahana · Havuç", 56, 1220, bg, 0.6, path=F_MED),
    ]))
    bg = CREAM
    s.append(dict(bg=bg, dur=3.0, els=[
        T("ÇİLEK", 60, 380, bg, 0.1, pill=RED, color=CREAM),
        I(icon_strawberry(), 720, 500, 0.2, float_amp=10),
        T("Fideler kışa hazırlanıyor", 80, 1080, bg, 0.4, maxw=900),
        T("Baharda dalından sofrana!", 56, 1260, bg, 0.65, path=F_MED, color=RED),
    ]))
    bg = SUN
    s.append(dict(bg=bg, dur=3.4, els=[
        T("Bu ay her gün", 84, 560, bg, 0.1),
        T("bahçeden yeni bir şey!", 76, 740, bg, 0.3, maxw=1000),
        I(icon_branch((GREEN_OLIVE, BLACKOLIVE, PURPLE, GREEN_OLIVE)), 1040, 600, 0.5),
        T("Takipte kal", 72, 1330, bg, 0.8, pill=DARK, color=CREAM, pulse=0.04),
    ]))
    return render(s, OUT + "01_kasim_bahcede_neler_var.mp4")


def video2():
    s = []
    bg = OLIVE
    both = Image.new("RGBA", (1200, 700), (0, 0, 0, 0))
    both.alpha_composite(icon_olive(GREEN_OLIVE, 700), (0, 0))
    both.alpha_composite(icon_olive(BLACKOLIVE, 700), (500, 0))
    s.append(dict(bg=bg, dur=3.4, els=[
        I(both, 600, 860, 0.0, float_amp=10),
        T("Yeşil zeytin\nve siyah zeytin", 72, 990, bg, 0.3, maxw=960),
        T("AYNI AĞAÇTAN\nçıkar!", 92, 1270, bg, 0.6, color=SUN, maxw=1000),
    ]))
    bg = DARK
    s.append(dict(bg=bg, dur=2.6, els=[
        T("Peki fark ne?", 72, 640, bg, 0.1, path=F_MED),
        T("RENK =", 130, 860, bg, 0.35, color=SUN),
        T("OLGUNLUK", 130, 1030, bg, 0.55, color=SUN),
    ]))
    for bg, oc, tag, title, sub in [
        (GREEN_OLIVE, GREEN_OLIVE, "1", "Erken hasat", "Daha acı, daha aromatik, bol polifenol"),
        (PURPLE, PURPLE, "2", "Yarı olgun", "Dengeli ve meyvemsi"),
        (BLACKOLIVE, BLACKOLIVE, "3", "Tam olgun", "Yumuşak ve tatlımsı"),
    ]:
        icon_bg = CREAM
        s.append(dict(bg=bg, dur=2.8, els=[
            T(tag, 70, 360, bg, 0.05, pill=SUN, color=DARK, pad=(40, 6)),
            I(icon_olive(oc), 700, 480, 0.15, float_amp=10) if bg != oc else
            I(_ring(icon_olive(oc)), 700, 520, 0.15, float_amp=10),
            T(title, 104, 1060, bg, 0.35),
            T(sub, 56, 1220, bg, 0.6, path=F_MED, maxw=820),
        ]))
    bg = SUN
    s.append(dict(bg=bg, dur=3.2, els=[
        T("Sen hangisisin?", 100, 700, bg, 0.1),
        T("Yeşil · Mor · Siyah", 64, 880, bg, 0.35, path=F_MED),
        T("Yorumlara yaz!", 76, 1120, bg, 0.6, pill=DARK, color=CREAM, pulse=0.04),
    ]))
    return render(s, OUT + "02_yesil_mi_siyah_mi.mp4")


def _ring(img):
    """Olive on a cream disc so it stays visible on a same-colour background."""
    S = img.width
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(out).ellipse([20, 20, S - 20, S - 20], fill=CREAM)
    out.alpha_composite(fit(img, width=int(S * 0.8)), (int(S * 0.1), int(S * 0.1)))
    return out


def video3():
    s = []
    bg = SUN
    s.append(dict(bg=bg, dur=3.2, els=[
        I(icon_bottle(), 600, 620, 0.0, float_amp=10),
        T("Dalından şişeye", 76, 1000, bg, 0.3, path=F_MED),
        T("YENİ SEZON\nGELDİ!", 104, 1230, bg, 0.55, color=RED, maxw=1000),
    ]))
    bg = OLIVE
    arrow = icon_arrow()
    s.append(dict(bg=bg, dur=3.6, els=[
        I(icon_branch(), 520, 400, 0.05, x=W // 2 - 300),
        T("Hasat", 56, 760, bg, 0.2, x=W // 2 - 300) if False else El(text_image("Hasat", 56, CREAM, 400), 760, x=W // 2 - 300, delay=0.2),
        I(arrow, 760, 120, 0.5, x=W // 2 - 140, anim="left"),
        I(icon_olive(GREEN_OLIVE), 980, 300, 0.7, x=W // 2),
        El(text_image("Sıkım", 56, CREAM, 400), 1180, x=W // 2, delay=0.85),
        I(arrow, 1180, 120, 1.15, x=W // 2 + 160, anim="left"),
        I(icon_bottle(), 1360, 320, 1.35, x=W // 2 + 300),
        El(text_image("Şişe", 56, CREAM, 400), 1580, x=W // 2 + 300, delay=1.5),
    ]))
    bg = CREAM
    chk = icon_check()
    els = [T("Şişede ne var?", 84, 470, bg, 0.05)]
    for k, line in enumerate(["Soğuk sıkım", "Natürel sızma", "2026 hasadı"]):
        y = 720 + k * 200
        els.append(I(chk, y, 120, 0.3 + k * 0.4, x=230))
        els.append(El(text_image(line, 76, DARK, 700, align="left"), y, x=590, delay=0.35 + k * 0.4, anim="left"))
    s.append(dict(bg=bg, dur=3.4, els=els))
    bg = RED
    s.append(dict(bg=bg, dur=3.6, els=[
        I(icon_bottle(), 600, 480, 0.0, float_amp=10),
        T("Ön sipariş açık!", 100, 1000, bg, 0.25),
        T("Sipariş için DM", 76, 1200, bg, 0.55, pill=CREAM, color=RED, pulse=0.05),
    ]))
    return render(s, OUT + "03_yeni_sezon_zeytinyagi.mp4")


if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    which = sys.argv[1:] or ["1", "2", "3"]
    for w in which:
        print(globals()["video" + w]())
