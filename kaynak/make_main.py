"""Zeytinliğin Sırrı — main story episodes."""
import sys, math, random
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont
from brand import *
from story import Shot, render_episode, bg_orchard, bg_brand, vgrad, _tree, W, H, BGW
from make_story import end_shot, ic_rake_net, ic_crate, ic_clock, canvas

OUT = "/home/claude/dt/out/"
LORA_I = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"


def _blend(im, color, alpha):
    over = Image.new("RGBA", im.size, color + (255,))
    return Image.blend(im, over, alpha)


@lru_cache(maxsize=2)
def bg_sunset():
    im = bg_orchard(("p",)).copy()
    warm = vgrad(BGW, H, (255, 120, 70), (255, 190, 110))
    mask = Image.linear_gradient("L").resize((BGW, H)).point(lambda v: int(150 - v * 0.42))
    warm.putalpha(mask)
    im.alpha_composite(warm)
    d = ImageDraw.Draw(im)
    glow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r, a in [(260, 40), (180, 70), (110, 255)]:
        gd.ellipse([900 - r, 820 - r, 900 + r, 820 + r], fill=(255, 214, 120, a))
    im.alpha_composite(glow)
    return im


@lru_cache(maxsize=2)
def bg_clearing(night=True):
    rnd = random.Random(21)
    top, bot = ((18, 26, 58), (60, 70, 110)) if night else ((170, 214, 236), (255, 238, 205))
    im = vgrad(BGW, H, top, bot)
    d = ImageDraw.Draw(im)
    if night:
        for k in range(120):
            x, y, r = rnd.uniform(0, BGW), rnd.uniform(0, 1000), rnd.choice([1.5, 2, 2.5, 3.5])
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 250, 220))
        d.ellipse([860, 260, 1020, 420], fill=(250, 244, 214))
        d.ellipse([900, 250, 1060, 410], fill=top)          # crescent
    hill1, hill2, ground = ((40, 58, 52), (32, 48, 40), (30, 46, 34)) if night else ((155, 184, 108), (126, 160, 82), (138, 168, 84))
    d.polygon([(0, 1180)] + [(x, 1120 - 70 * math.sin(x / 260)) for x in range(0, BGW + 1, 20)] + [(BGW, 1500), (0, 1500)], fill=hill1)
    d.polygon([(0, 1300)] + [(x, 1260 - 50 * math.sin(x / 190 + 1)) for x in range(0, BGW + 1, 20)] + [(BGW, 1520), (0, 1520)], fill=hill2)
    cols = [(40, 34, 46)] if night else [(110, 52, 84)]
    tmp = Image.new("RGBA", im.size, (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    for x in (650, 900, 1120):
        _tree(td, x, 1290, 0.3, rnd, cols)
    if night:
        tmp = Image.blend(Image.new("RGBA", im.size, (0, 0, 0, 0)), tmp, 1.0)
        dark = Image.new("RGBA", im.size, (20, 30, 50, 0))
        im.alpha_composite(tmp)
        shade = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(shade).rectangle([0, 900, BGW, 1500], fill=(16, 24, 44, 120))
        im.alpha_composite(shade)
    else:
        im.alpha_composite(tmp)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 1480, BGW, H], fill=ground)
    for k in range(70):
        gx, gy = rnd.uniform(0, BGW), rnd.uniform(1520, H)
        d.line([(gx, gy), (gx + 6, gy - 22)], fill=tuple(max(0, c - 14) for c in ground), width=5)
    if night:  # fireflies
        glow = Image.new("RGBA", im.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        for k in range(22):
            x, y = rnd.uniform(0, BGW), rnd.uniform(1100, 1800)
            gd.ellipse([x - 14, y - 14, x + 14, y + 14], fill=(250, 230, 120, 60))
            gd.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(255, 245, 170, 255))
        im.alpha_composite(glow)
    return im


def notebook_page(lines, sign):
    pw, ph = 900, 600
    im = Image.new("RGBA", (pw + 40, ph + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([24, 30, pw + 24, ph + 30], radius=18, fill=(0, 0, 0, 70))
    d.rounded_rectangle([10, 10, pw + 10, ph + 10], radius=18, fill=(246, 234, 204))
    for y in range(110, ph, 64):
        d.line([(50, y), (pw - 30, y)], fill=(196, 206, 214), width=3)
    d.line([(120, 20), (120, ph)], fill=(226, 150, 150), width=3)
    # torn right edge feel
    rnd = random.Random(4)
    pts = [(pw + 10, 10)] + [(pw + 10 - rnd.uniform(0, 14), y) for y in range(10, ph + 10, 18)] + [(pw + 10, ph + 10)]
    d.polygon(pts + [(pw + 40, ph + 10), (pw + 40, 10)], fill=(0, 0, 0, 0))
    f = ImageFont.truetype(LORA_I, 64)
    try:
        f.set_variation_by_name("Bold Italic")
    except Exception:
        pass
    y = 150
    for ln in lines:
        d.text((150, y), ln, font=f, fill=(40, 40, 70))
        y += 96
    f2 = ImageFont.truetype(LORA_I, 52)
    d.text((pw - 40 - f2.getlength(sign), y + 20), sign, font=f2, fill=(40, 40, 70))
    # coffee ring
    d.ellipse([640, 60, 820, 230], outline=(196, 160, 110, 110), width=8)
    return im.rotate(-2, resample=Image.BICUBIC, expand=True)


def ep1():
    sun = bg_sunset()
    night = bg_clearing(True)
    page = notebook_page(["Ağaçları dinlersen,", "onlar da seni dinler."], "— Deden")
    Z, Y, U, S = "zeynep", "zeyto", "ulu", "sinsi"
    shots = [
        Shot(sun, [
            (Z, "Dedemin zeytinliği... Buraya gelmeyeli yirmi yıl olmuş.", {}),
            (Z, "Bir de bu defteri bırakmış bana. İlk sayfada tek bir cümle var.", {"point": True}),
        ], zeynep_x=360, zeynep_enter=True, gap=0.3),
        Shot(sun, [
            (Z, "Ağaçları dinlersen, onlar da seni dinler.", {}),
            (Z, "Ah dede... Sen de amma şairdin ha.", {}),
        ], zeynep_x=360, card=page, gap=0.3),
        Shot(sun, [
            (Y, "Ayy! Sonunda biri geldi!", {"arms": True, "mood": "wow", "tag": "excited"}),
            (Z, "Kim o? Kim konuştu?!", {"tag": "surprised"}),
            (Y, "Aşağı bak. Hayır, daha aşağı... Merhaba! Ben Zeyto.", {"arms": True}),
            (Z, "Bir zeytin... konuşuyor. Tamam, ben çok yorulmuşum.", {"tag": "nervous laugh"}),
            (Y, "Yorgun falan değilsin. Defteri açtın, artık bizi duyabiliyorsun.", {}),
            (Z, "Bizi mi? Siz kaç kişisiniz?", {}),
            (Y, "Bu zeytinlikte iki bin ağaç var. Hepsi seni bekliyordu.", {"arms": True}),
            (Y, "Ama en çok da... Ulu.", {"mood": "worried", "gap": 0.6, "tag": "whispers"}),
        ], zeynep_x=330, zeyto_x=790, zeyto_drop=0.3, gap=0.28),
        Shot(night, [
            (U, "Hoş geldin evlat. Gözlerin, tıpkı deden gibi bakıyor.", {"tag": "warmly"}),
            (Z, "Sen... sen konuşan bir ağaç mısın?", {}),
            (U, "Ben bu zeytinliğin en yaşlısıyım. Tam bin yıldır buradayım.", {}),
            (Y, "Gerçekten! Zeytin ağacı yüzlerce, hatta binlerce yıl yaşayabilir.", {"arms": True}),
            (Z, "Bin yıl... Peki dedem? Dedem size ne anlattı?", {}),
            (U, "Deden gitmeden önce defterinden bir sayfa yırttı. Ve onu sakladı.", {}),
            (U, "O sayfa bulunmazsa, bu zeytinlik bir sonraki baharı göremez.", {}),
            (Z, "Ne demek göremez? Neden?!", {"tag": "alarmed"}),
            (U, "Önce bana kendini kanıtla. Yarın, hasatta görüşürüz.", {"gap": 0.7}),
        ], zeynep_x=830, zeyto_x=610, zeyto_color=GREEN_OLIVE, zeynep_scale=0.66, pan=False, gap=0.28, tint=((30, 40, 90), 0.28),
            actors=[{"kind": "ulu", "x": 280, "feet": 1900, "scale": 0.95, "wake": 0.0}]),
        Shot(night, [
            (S, "Bzzz... Yeni bir mühendis demek.", {"tag": "whispers"}),
            (S, "Bakalım bu zeytinlikte kaç gün dayanacak.", {"tag": "mischievously"}),
            (Y, "Mühendis Abi... O ses neydi?", {"mood": "worried", "tag": "scared"}),
        ], zeynep_x=830, zeyto_x=610, zeynep_scale=0.66, pan=False, gap=0.3, tint=((30, 40, 90), 0.28),
            actors=[{"kind": "ulu", "x": 280, "feet": 1900, "scale": 0.95, "wake": None},
                    {"kind": "sinsi", "x": 760, "y": 820, "scale": 0.9, "appear": 0.0}]),
        end_shot("Bölüm 2 yarın 13:00", "Ulu'nun Sınavı", GREEN_OLIVE, cta="Takip et, hikâyeyi kaçırma!"),
    ]
    return render_episode(shots, "BÖLÜM 1", OUT + "S1B1_dedemin_defteri.mp4")


def ic_net():
    im, d = canvas()
    d.polygon([(60, 560), (740, 560), (700, 720), (100, 720)], fill=(90, 160, 90))
    for k in range(0, 13):
        x = 60 + k * 57
        d.line([(x, 560), (x + (400 - x) * 0.06, 720)], fill=(60, 120, 60), width=6)
    for y in (600, 640, 680):
        d.line([(80, y), (720, y)], fill=(60, 120, 60), width=6)
    d.rectangle([370, 140, 430, 560], fill=BROWN)
    for x, y, r in [(400, 150, 200), (260, 220, 130), (540, 220, 130)]:
        d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=(118, 140, 96))
    for k, (x, y) in enumerate([(200, 620), (330, 650), (480, 610), (600, 660), (420, 690)]):
        draw_olive(d, x, y, 30, [BLACKOLIVE, PURPLE, GREEN_OLIVE][k % 3])
    return im


def ic_rake():
    im, d = canvas()
    d.line([(620, 80), (380, 520)], fill=BROWN, width=36)
    d.rounded_rectangle([210, 500, 520, 560], radius=14, fill=(110, 110, 118))
    for k in range(8):
        x = 225 + k * 40
        d.line([(x, 555), (x - 8, 650)], fill=(110, 110, 118), width=14)
    for k, (x, y) in enumerate([(240, 700), (360, 720), (470, 690)]):
        draw_olive(d, x, y, 36, [BLACKOLIVE, PURPLE, GREEN_OLIVE][k % 3])
    return im


def old_map():
    pw, ph = 900, 640
    im = Image.new("RGBA", (pw + 40, ph + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rnd = random.Random(9)
    tear = [(pw * 0.62 + rnd.uniform(-30, 30), y) for y in range(10, ph + 20, 30)]
    shape = [(10, 10)] + tear + [(10, ph + 10)]
    shadow = [(x + 14, y + 18) for x, y in shape]
    d.polygon(shadow, fill=(0, 0, 0, 70))
    d.polygon(shape, fill=(232, 210, 160))
    for k in range(40):
        x, y = rnd.uniform(20, 500), rnd.uniform(20, ph)
        d.ellipse([x, y, x + rnd.uniform(10, 40), y + rnd.uniform(6, 20)], fill=(220, 194, 140))
    # olive tree glyphs
    for x, y in [(90, 140), (160, 260), (90, 420), (260, 520), (330, 160), (420, 330)]:
        d.rectangle([x - 5, y, x + 5, y + 30], fill=(110, 80, 50))
        d.ellipse([x - 32, y - 40, x + 32, y + 6], fill=(110, 130, 80))
    # the big tree = Ulu
    d.rectangle([220, 300, 240, 360], fill=(90, 64, 40))
    d.ellipse([170, 220, 290, 320], fill=(90, 110, 64))
    # dotted path to the torn edge
    pts = [(230, 370), (300, 420), (380, 440), (450, 400), (520, 380), (570, 340)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for t in range(0, 10, 2):
            a, b = t / 10, (t + 1) / 10
            d.line([(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b)], fill=(150, 40, 40), width=8)
    f = ImageFont.truetype(LORA_I, 46)
    d.text((40, 30), "Zeytinlik, 1987", font=f, fill=(80, 50, 30))
    d.text((150, 560), "Ulu", font=ImageFont.truetype(LORA_I, 40), fill=(80, 50, 30))
    d.text((470, 460), "?", font=ImageFont.truetype(LORA_I, 110), fill=(150, 40, 40))
    return im.rotate(3, resample=Image.BICUBIC, expand=True)


def ep2():
    day = bg_orchard(("p",))
    clear = bg_clearing(False)
    Z, Y, U, S = "zeynep", "zeyto", "ulu", "sinsi"
    ulu_actor = [{"kind": "ulu", "x": 280, "feet": 1900, "scale": 0.95, "wake": None}]
    shots = [
        Shot(day, [
            (Y, "Günaydın Mühendis Abi! Bugün büyük gün. Ulu seni sınava çekecek!", {"arms": True, "tag": "excited"}),
            (Z, "Sınav mı? Ben üniversiteyi bitireli yıllar oldu ama.", {"tag": "laughs"}),
            (Y, "Bu sınav kitapta yok. Zeytinleri toplayacaksın. Ama doğru şekilde!", {}),
        ], zeynep_x=330, zeyto_x=790, zeynep_enter=True, gap=0.28),
        Shot(clear, [
            (U, "Hasat zamanı geldi evlat. Göster bakalım, dedenden ne öğrendin?", {"tag": "warmly"}),
            (Z, "Kolay. Bir sırık bulur, dalları silkelerim.", {"tag": "confident"}),
            (Y, "Hayııır!", {"arms": True, "mood": "wow", "tag": "shouting"}),
            (U, "Sırıkla dövülen dal kırılır. Kırılan her sürgün, gelecek yılın zeytinidir.", {"tag": "seriously"}),
            (Z, "Tamam, tamam. O zaman nasıl toplayacağım?", {}),
        ], zeynep_x=830, zeyto_x=610, zeynep_scale=0.66, pan=False, gap=0.28, actors=ulu_actor),
        Shot(day, [
            (Z, "Dur, dedemin defterinde yazıyor. Bir: Ağacın altına file serilir.", {"step": 0, "point": True}),
            (Z, "İki: Zeytinler el tırmığıyla nazikçe taranır.", {"step": 1, "point": True}),
            (Y, "Gıdıklanıyorum ama hoşuma gidiyor!", {"arms": True, "tag": "giggles"}),
            (Z, "Üç: Çuval değil, delikli kasa. Zeytin nefes almalı, yoksa ezilip ısınır.", {"step": 2, "point": True}),
            (Z, "Dört: Toplanan zeytin, en geç bir gün içinde sıkılır.", {"step": 3, "point": True}),
        ], zeynep_x=270, zeyto_x=840, gap=0.28, steps=[
            ("File ser", ic_net()), ("El tırmığı", ic_rake()), ("Delikli kasa", ic_crate()), ("24 saatte sıkım", ic_clock())]),
        Shot(clear, [
            (U, "Aferin evlat. Deden de tam böyle yapardı.", {"tag": "proudly"}),
            (S, "Vızzz... Toplayın bakalım. Kasanın dibindekileri görünce gülmeyi bırakırsınız.", {"tag": "mischievously"}),
            (Y, "O sinek yine burada! Ne demek istedi?", {"mood": "worried", "tag": "scared"}),
        ], zeynep_x=830, zeyto_x=610, zeynep_scale=0.66, pan=False, gap=0.28,
            actors=ulu_actor + [{"kind": "sinsi", "x": 760, "y": 820, "scale": 0.9, "appear": 2.6}]),
        Shot(day, [
            (Z, "Bir dakika... Defterin arasından bir şey düştü.", {"tag": "curious"}),
            (Z, "Bu bir harita! Ama yarısı yırtılmış...", {"tag": "surprised"}),
        ], zeynep_x=360, zeyto_x=800, card=old_map(), gap=0.3),
        end_shot("Bölüm 3 bu akşam 20:00", "Sinsi'nin Planı", GREEN_OLIVE, cta="Takip et, hikâyeyi kaçırma!"),
    ]
    return render_episode(shots, "BÖLÜM 2", OUT + "S1B2_ulunun_sinavi.mp4")


def ic_yellow_trap(flies=3):
    im, d = canvas()
    d.line([(400, 20), (400, 150)], fill=(90, 90, 90), width=6)
    d.rounded_rectangle([220, 140, 580, 700], radius=18, fill=(250, 220, 40), outline=(200, 170, 20), width=8)
    for k in range(1, 6):
        d.line([(220, 140 + k * 93), (580, 140 + k * 93)], fill=(220, 190, 30), width=4)
        d.line([(220 + k * 60, 140), (220 + k * 60, 700)], fill=(220, 190, 30), width=4)
    rnd = random.Random(5)
    for k in range(flies):
        x, y = rnd.uniform(280, 520), rnd.uniform(220, 640)
        d.ellipse([x - 16, y - 10, x + 16, y + 10], fill=(150, 92, 40))
        d.ellipse([x - 26, y - 20, x - 4, y - 4], fill=(220, 236, 244))
        d.ellipse([x + 4, y - 20, x + 26, y - 4], fill=(220, 236, 244))
        d.ellipse([x - 12, y - 16, x - 2, y - 6], fill=(196, 30, 40))
    return im


def ic_bottle_trap():
    im, d = canvas()
    d.line([(400, 10), (400, 110)], fill=(90, 90, 90), width=6)
    d.rounded_rectangle([370, 100, 430, 160], radius=8, fill=(40, 110, 200))
    d.polygon([(330, 230), (370, 160), (430, 160), (470, 230)], fill=(200, 228, 236))
    d.rounded_rectangle([290, 220, 510, 720], radius=60, fill=(200, 228, 236))
    d.rounded_rectangle([300, 470, 500, 710], radius=50, fill=(230, 200, 90))
    for x, y in [(330, 300), (470, 330), (320, 400), (480, 420)]:
        d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=(60, 60, 70))
    for x, y in [(380, 560), (430, 600), (400, 650)]:
        d.ellipse([x - 14, y - 8, x + 14, y + 8], fill=(150, 92, 40))
    d.polygon(ellipse_poly(320, 300, 12, 80, 0), fill=(255, 255, 255, 110))
    return im


def ic_collect():
    im, d = canvas()
    d.rectangle([0, 600, 800, 800], fill=(150, 120, 80))
    for k, (x, y) in enumerate([(160, 640), (260, 680), (560, 650), (660, 700), (420, 700)]):
        draw_olive(d, x, y, 38, [BLACKOLIVE, PURPLE][k % 2])
        d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(30, 20, 20))
    d.rounded_rectangle([250, 300, 550, 560], radius=30, fill=(196, 120, 64))
    d.arc([250, 160, 550, 440], 180, 360, fill=(150, 88, 44), width=22)
    for k in range(6):
        draw_olive(d, 300 + k * 40, 320, 30, [BLACKOLIVE, PURPLE][k % 2])
    # little worm
    d.line([(560, 640), (585, 625), (610, 640), (635, 625)], fill=(240, 230, 200), width=12, joint="curve")
    return im


def ep3():
    day = bg_orchard(("p",))
    clear = bg_clearing(False)
    Z, Y, U, S = "zeynep", "zeyto", "ulu", "sinsi"
    ulu_actor = [{"kind": "ulu", "x": 280, "feet": 1900, "scale": 0.95, "wake": None}]
    trap = fit(ic_yellow_trap(2), width=300)
    shots = [
        Shot(day, [
            (Y, "Mühendis Abi! Kasanın dibine bak, bazı kardeşlerim delik deşik olmuş!", {"mood": "worried", "arms": True, "tag": "scared"}),
            (Z, "Göster bakayım... Her zeytinde minicik bir delik var. Bu bir sokma izi.", {"tag": "concerned"}),
            (Y, "Sokma mı? Kim sokmuş?", {"mood": "wow"}),
            (Z, "Bunu en iyi Ulu bilir. Hadi gel.", {}),
        ], zeynep_x=330, zeyto_x=790, zeynep_enter=True, gap=0.28),
        Shot(clear, [
            (U, "Bu, zeytin sineğinin işi evlat. Dişisi yumurtasını zeytinin içine bırakır.", {"tag": "seriously"}),
            (U, "Çıkan kurt zeytinin etini yer. Kurtlu zeytinden çıkan yağın da asitliği yükselir.", {}),
            (Y, "Sinsi! O vızıltı oydu!", {"arms": True, "mood": "wow", "tag": "angry"}),
            (Z, "Peki onu nasıl durduracağız?", {}),
            (U, "Deden ne yapardı, defterine bak.", {"tag": "gently"}),
        ], zeynep_x=830, zeyto_x=610, zeynep_scale=0.66, pan=False, gap=0.28, actors=ulu_actor),
        Shot(day, [
            (Z, "Bir: Ağaçlara sarı yapışkan tuzaklar asılır. Sinek sarı renge bayılır.", {"step": 0, "point": True}),
            (Z, "İki: Pet şişeden tuzak yapılır. İçine sineği çeken bir yem konur, kenarına küçük delikler açılır.", {"step": 1, "point": True}),
            (Y, "Yani sinekler için tuzak kafe!", {"arms": True, "tag": "giggles"}),
            (Z, "Üç: Yere düşen kurtlu zeytinler toplanır. Yoksa kurtlar toprakta kışı geçirir.", {"step": 2, "point": True}),
        ], zeynep_x=270, zeyto_x=840, gap=0.28, steps=[
            ("Sarı yapışkan tuzak", ic_yellow_trap()), ("Pet şişe tuzak", ic_bottle_trap()), ("Düşenleri topla", ic_collect())]),
        Shot(clear, [
            (S, "Hey! Bırakın beni! Yapıştım kaldım!", {"tag": "panicked"}),
            (Y, "Hah! Tuzak kafeye hoş geldin Sinsi!", {"arms": True, "tag": "laughs"}),
            (Z, "Söyle bakalım, neden bu zeytinliğe dadandın?", {"tag": "firmly"}),
            (S, "Gülün bakalım... Bu zeytinlik yakında betonun olacak! Beton Bey yarın geliyor!", {"tag": "mischievously"}),
            (Y, "Beton Bey de kim?!", {"mood": "worried", "tag": "scared"}),
        ], zeynep_x=830, zeyto_x=610, zeynep_scale=0.66, pan=False, gap=0.28, props=[(trap, 760, 860)],
            actors=ulu_actor + [{"kind": "sinsi", "x": 760, "y": 860, "scale": 0.7, "appear": 0.0, "stuck": True}]),
        end_shot("Bölüm 4 yarın 13:00", "Beton Bey", GREEN_OLIVE, cta="Takip et, hikâyeyi kaçırma!"),
    ]
    return render_episode(shots, "BÖLÜM 3", OUT + "S1B3_sinsinin_plani.mp4")


def ic_spot_leaf():
    im, d = canvas()
    d.polygon(leaf_poly(400, 400, 680, 220, -30), fill=(96, 128, 70))
    a = math.radians(-30)
    d.line([(400 - 330 * math.cos(a), 400 - 330 * math.sin(a)), (400 + 330 * math.cos(a), 400 + 330 * math.sin(a))], fill=(70, 96, 50), width=10)
    for x, y, r in [(300, 450, 46), (450, 360, 38), (520, 300, 30), (360, 380, 26)]:
        d.ellipse([x - r - 14, y - r - 14, x + r + 14, y + r + 14], fill=(230, 210, 90))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(70, 60, 40))
        d.ellipse([x - r * 0.45, y - r * 0.45, x + r * 0.45, y + r * 0.45], fill=(120, 110, 70))
    return im


def ic_dry_branch():
    im, d = canvas()
    d.line([(120, 600), (420, 360), (680, 200)], fill=(110, 84, 56), width=40, joint="curve")
    d.line([(420, 360), (520, 520)], fill=(140, 120, 100), width=22)
    for k, (x, y) in enumerate([(540, 540), (500, 470)]):
        d.polygon(leaf_poly(x, y, 90, 30, 60 + k * 30), fill=(170, 150, 90))
    for k, (x, y) in enumerate([(600, 230), (680, 180), (520, 290)]):
        d.polygon(leaf_poly(x, y - 40, 110, 36, -40 + k * 20), fill=(110, 140, 80))
    d.line([(440, 420), (520, 440)], fill=RED, width=12)
    d.line([(450, 380), (500, 480)], fill=RED, width=12)
    return im


def ic_saw():
    im, d = canvas()
    d.line([(100, 650), (300, 420), (380, 200)], fill=(110, 84, 56), width=70, joint="curve")
    for x, y in [(300, 420), (200, 540)]:
        d.ellipse([x - 40, y - 26, x + 40, y + 26], fill=(220, 190, 140))
    for k, (x, y, ang) in enumerate([(400, 320, -30), (460, 240, -50), (420, 160, -70)]):
        d.line([(380, 200 + k * 60), (x + 140, y - 30)], fill=(110, 84, 56), width=14)
        d.polygon(leaf_poly(x + 160, y - 40, 120, 40, ang), fill=(130, 170, 80))
    d.polygon([(470, 560), (720, 480), (740, 520), (490, 600)], fill=(190, 196, 204))
    for k in range(8):
        x = 490 + k * 30
        d.polygon([(x, 598 - k * 10), (x + 15, 615 - k * 10), (x + 30, 594 - k * 10)], fill=(150, 156, 164))
    d.rounded_rectangle([690, 450, 770, 540], radius=18, fill=RED)
    return im


def ic_manure():
    im, d = canvas()
    d.rectangle([0, 560, 800, 800], fill=(120, 90, 60))
    d.rectangle([370, 200, 430, 600], fill=(110, 84, 56))
    d.ellipse([200, 80, 600, 320], fill=(118, 140, 96))
    d.ellipse([140, 540, 660, 640], fill=(80, 56, 36))
    for k in range(10):
        x = 180 + k * 50
        d.ellipse([x - 22, 560 - (k % 3) * 8, x + 22, 590 - (k % 3) * 8], fill=(96, 68, 44))
    d.rounded_rectangle([560, 360, 760, 560], radius=20, fill=(220, 200, 150))
    d.text((585, 420), "GÜBRE", font=font(F_BOLD, 40), fill=DARK)
    return im


def ic_copper():
    im, d = canvas()
    d.rounded_rectangle([200, 300, 470, 700], radius=50, fill=(40, 120, 200))
    d.rounded_rectangle([260, 220, 410, 310], radius=20, fill=(30, 90, 160))
    d.line([(470, 360), (620, 250)], fill=(60, 60, 60), width=18)
    d.polygon([(610, 230), (680, 200), (660, 280)], fill=(60, 60, 60))
    for k in range(14):
        x = 690 + (k % 4) * 22 - 20
        y = 160 + (k // 4) * 30 + (k % 2) * 10
        d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=(80, 170, 230))
    d.ellipse([255, 420, 415, 580], fill=(250, 250, 250))
    d.text((290, 455), "Cu", font=font(F_BOLD, 80), fill=(180, 90, 40))
    return im


def ic_open_canopy():
    im, d = canvas()
    d.rectangle([370, 380, 430, 740], fill=(110, 84, 56))
    for x, y, r in [(220, 300, 120), (580, 300, 120), (300, 170, 100), (500, 170, 100)]:
        d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=(118, 140, 96))
    d.ellipse([330, 180, 470, 330], fill=(250, 230, 140))
    for k in range(6):
        a = math.radians(k * 60 + 30)
        d.line([(400 + math.cos(a) * 90, 255 + math.sin(a) * 90), (400 + math.cos(a) * 140, 255 + math.sin(a) * 140)], fill=SUN, width=12)
    return im


def ic_fallen_leaves():
    im, d = canvas()
    d.rectangle([0, 560, 800, 800], fill=(150, 120, 80))
    rnd = random.Random(8)
    for k in range(14):
        x, y = rnd.uniform(80, 720), rnd.uniform(590, 760)
        d.polygon(leaf_poly(x, y, 90, 30, rnd.uniform(-60, 60)), fill=(150, 150, 80))
        d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=(70, 60, 40))
    d.line([(620, 100), (430, 560)], fill=(110, 84, 56), width=30)
    d.rounded_rectangle([300, 540, 560, 590], radius=12, fill=(110, 110, 118))
    for k in range(7):
        d.line([(315 + k * 38, 585), (305 + k * 38, 650)], fill=(110, 110, 118), width=12)
    return im


def ep4():
    day = bg_orchard(("p",))
    clear = bg_clearing(False)
    Z, Y, U, B = "zeynep", "zeyto", "ulu", "beton"
    ulu_actor = [{"kind": "ulu", "x": 280, "feet": 1900, "scale": 0.95, "wake": None}]
    shots = [
        Shot(day, [
            (B, "Merhabalar! Siz yeni mühendis olmalısınız. Ben Beton. Herkes bana Beton Bey der.", {"tag": "confident"}),
            (Z, "Hoş geldiniz. Buyurun, ne istemiştiniz?", {}),
            (B, "Kısa keseyim. Bu araziyi almak istiyorum. Buraya kocaman bir otel yapacağım!", {"tag": "excited"}),
            (Z, "Bu zeytinlik satılık değil.", {"tag": "firmly"}),
            (B, "Bakın, bu ağaçlar zaten yaşlı, bitmiş. Hiçbir işe yaramazlar.", {"tag": "dismissively"}),
            (B, "İyi para veririm. Düşünün, yarın yine gelirim.", {"tag": "smugly", "gap": 0.6}),
        ], zeynep_x=300, zeynep_enter=False, gap=0.28,
            actors=[{"kind": "beton", "x": 790, "scale": 0.84, "enter": True, "appear": 0.0}]),
        Shot(clear, [
            (Y, "Ulu! Ulu! Adam buraya beton dökecekmiş!", {"arms": True, "mood": "worried", "tag": "panicked"}),
            (U, "Sakin ol Zeyto. Zeytin ağacı kolay kolay pes etmez.", {"tag": "calmly"}),
            (Z, "Ama haklı mı? Yaşlı ağaçlar gerçekten bitmiş mi?", {}),
            (U, "Yaşlı ağaç, ölmüş ağaç değildir evlat. Bakılırsa yüzlerce yıl daha meyve verir.", {"tag": "warmly"}),
        ], zeynep_x=830, zeyto_x=610, zeynep_scale=0.66, pan=False, gap=0.28, actors=ulu_actor),
        Shot(day, [
            (Z, "Dedem yaşlı ağaçları nasıl gençleştirirdi, bakalım. Bir: Kuruyan ve hastalanan dallar kesilir.", {"step": 0, "point": True}),
            (Z, "İki: Yaşlı kalın dallar birkaç yıla bölünerek budanır. Ağaç yeni, verimli sürgünler verir.", {"step": 1, "point": True}),
            (Y, "Yani Ulu'ya güzellik bakımı!", {"arms": True, "tag": "giggles"}),
            (Z, "Üç: Ağacın dibi çapalanır, toprağa yanmış hayvan gübresi verilir.", {"step": 2, "point": True}),
        ], zeynep_x=270, zeyto_x=840, gap=0.28, steps=[
            ("Kuru dalları kes", ic_dry_branch()), ("Gençleştirme budaması", ic_saw()), ("Toprağı besle", ic_manure())]),
        Shot(clear, [
            (Y, "Ulu... Yapraklarında bu halka halka lekeler ne?", {"mood": "worried", "tag": "scared"}),
            (U, "Bilmiyorum Zeyto... Kendimi hiç iyi hissetmiyorum.", {"tag": "weakly"}),
            (Z, "Bu bir hastalık. Hemen bir şey yapmalıyız!", {"tag": "alarmed"}),
        ], zeynep_x=830, zeyto_x=610, zeynep_scale=0.66, pan=False, gap=0.3, card=ic_spot_leaf().resize((620, 620)),
            actors=[{"kind": "ulu", "x": 280, "feet": 1900, "scale": 0.95, "wake": None, "eyes": 0.5}]),
        end_shot("Bölüm 5 bu akşam 20:00", "Ulu Hastalandı", GREEN_OLIVE, cta="Takip et, hikâyeyi kaçırma!"),
    ]
    return render_episode(shots, "BÖLÜM 4", OUT + "S1B4_beton_bey.mp4")


def ep5():
    dusk = bg_clearing(True)
    day = bg_orchard(("p",))
    Z, Y, U = "zeynep", "zeyto", "ulu"
    tired = [{"kind": "ulu", "x": 280, "feet": 1900, "scale": 0.95, "wake": None, "eyes": 0.5}]
    glow = Image.new("RGBA", (360, 360), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r, a in [(170, 40), (120, 80), (70, 160), (30, 255)]:
        gd.ellipse([180 - r, 180 - r, 180 + r, 180 + r], fill=(255, 230, 140, a))
    shots = [
        Shot(dusk, [
            (Z, "Buldum! Dedemin defterinde bu lekeler var. Adı halkalı leke hastalığı.", {"tag": "concerned"}),
            (Y, "Hastalık mı? Ulu iyileşecek mi?", {"mood": "worried", "tag": "scared"}),
            (Z, "Merak etme. Bir mantar hastalığı bu. Yağmurlu, nemli havada yayılır ama tedavisi var.", {"tag": "reassuring"}),
            (U, "Deden de böyle derdi... Ellerine güveniyorum evlat.", {"tag": "weakly"}),
        ], zeynep_x=830, zeyto_x=610, zeynep_scale=0.66, pan=False, gap=0.28, tint=((30, 40, 90), 0.2), actors=tired),
        Shot(day, [
            (Z, "Bir: Sonbaharda ve ilkbaharda bakırlı bir ilaçla ilaçlanır. Dozu için tarım müdürlüğüne danışılır.", {"step": 0, "point": True}),
            (Z, "İki: Budamayla ağacın içi açılır. Güneş ve hava girince nem azalır, mantar da azalır.", {"step": 1, "point": True}),
            (Y, "Ulu'nun penceresini açıyoruz yani!", {"arms": True, "tag": "excited"}),
            (Z, "Üç: Yere dökülen hastalıklı yapraklar toplanıp zeytinlikten uzaklaştırılır.", {"step": 2, "point": True}),
        ], zeynep_x=270, zeyto_x=840, gap=0.28, steps=[
            ("Bakırlı ilaç", ic_copper()), ("İçi açık budama", ic_open_canopy()), ("Yaprakları topla", ic_fallen_leaves())]),
        Shot(dusk, [
            (U, "Teşekkür ederim evlat. Deden de beni böyle iyileştirmişti.", {"tag": "warmly"}),
            (U, "Artık sana bir ipucu verebilirim. Kayıp sayfa... en eski kökün altında.", {"tag": "whispers"}),
            (Y, "En eski kök mü? Hangisi?!", {"arms": True, "mood": "wow", "tag": "excited"}),
            (Z, "Şşş... Bakın! Köklerin arasında bir şey parlıyor!", {"tag": "whispers", "gap": 0.7}),
        ], zeynep_x=830, zeyto_x=610, zeynep_scale=0.66, pan=False, gap=0.28, tint=((30, 40, 90), 0.2),
            props_top=[(glow, 470, 1800)], actors=[{"kind": "ulu", "x": 280, "feet": 1900, "scale": 0.95, "wake": None}]),
        end_shot("Bölüm 6 yarın 13:00", "Gece Kazısı", GREEN_OLIVE, cta="Takip et, hikâyeyi kaçırma!"),
    ]
    return render_episode(shots, "BÖLÜM 5", OUT + "S1B5_ulu_hastalandi.mp4")


if __name__ == "__main__":
    for w in sys.argv[1:] or ["1"]:
        print(globals()["ep" + w]())
