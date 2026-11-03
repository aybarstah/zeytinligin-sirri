import sys, math
from PIL import Image, ImageDraw
from brand import *
from story import Shot, render_episode, bg_orchard, bg_mill, bg_brand, W

OUT = "/home/claude/dt/out/"
BLUE = (80, 160, 210)


def canvas(S=800):
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def ic_no_stick():
    im, d = canvas()
    d.line([(150, 650), (650, 150)], fill=BROWN, width=44)
    d.ellipse([110, 110, 690, 690], outline=RED, width=56)
    d.line([(205, 205), (595, 595)], fill=RED, width=56)
    return im


def ic_rake_net():
    im, d = canvas()
    d.ellipse([60, 520, 740, 720], fill=(110, 170, 100))
    for k in range(-6, 7):
        d.line([(400 + k * 50, 525), (400 + k * 50 + 40, 715)], fill=(80, 140, 74), width=5)
    d.line([(560, 80), (360, 470)], fill=BROWN, width=34)
    d.rounded_rectangle([230, 440, 500, 490], radius=12, fill=(90, 90, 96))
    for k in range(7):
        x = 245 + k * 40
        d.line([(x, 485), (x - 10, 560)], fill=(90, 90, 96), width=14)
    for k, (x, y) in enumerate([(160, 600), (620, 620), (520, 650), (250, 660)]):
        draw_olive(d, x, y, 34, [BLACKOLIVE, PURPLE, GREEN_OLIVE][k % 3])
    return im


def ic_crate():
    im, d = canvas()
    for k in range(14):
        x, y = 190 + (k % 7) * 70, 300 - (k // 7) * 40 + (k % 2) * 10
        draw_olive(d, x, y + 40, 44, [BLACKOLIVE, PURPLE, GREEN_OLIVE][k % 3])
    d.rounded_rectangle([110, 330, 690, 640], radius=24, fill=(196, 120, 64))
    for row in range(2):
        for k in range(5):
            d.rounded_rectangle([150 + k * 106, 380 + row * 120, 220 + k * 106, 440 + row * 120], radius=10, fill=(150, 88, 44))
    return im


def ic_clock():
    im, d = canvas()
    d.ellipse([110, 110, 690, 690], fill=CREAM, outline=DARK, width=36)
    for k in range(12):
        a = math.radians(k * 30)
        d.line([(400 + math.cos(a) * 230, 400 + math.sin(a) * 230), (400 + math.cos(a) * 260, 400 + math.sin(a) * 260)], fill=DARK, width=14)
    f = font(F_BOLD, 190)
    d.text((400 - f.getlength("24") / 2, 250), "24", font=f, fill=RED)
    f2 = font(F_BOLD, 64)
    d.text((400 - f2.getlength("saat") / 2, 480), "saat", font=f2, fill=DARK)
    return im


def ic_wash():
    im, d = canvas()
    for k, (x, y) in enumerate([(260, 520), (400, 560), (540, 520), (330, 640), (470, 640)]):
        draw_olive(d, x, y, 62, [GREEN_OLIVE, PURPLE, BLACKOLIVE][k % 3])
    for x, y, s in [(250, 200, 1), (420, 140, 1.2), (580, 230, 0.9)]:
        d.polygon([(x, y - 90 * s), (x - 50 * s, y + 10 * s), (x + 50 * s, y + 10 * s)], fill=BLUE)
        d.ellipse([x - 52 * s, y - 40 * s, x + 52 * s, y + 62 * s], fill=BLUE)
    return im


def ic_crush():
    im, d = canvas()
    for cx, cy in [(290, 330), (510, 330)]:
        for k in range(10):
            a = math.radians(k * 36)
            d.polygon(ellipse_poly(cx + math.cos(a) * 130, cy + math.sin(a) * 130, 34, 34, 0), fill=(150, 162, 170))
        d.ellipse([cx - 135, cy - 135, cx + 135, cy + 135], fill=(184, 194, 200))
        d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(120, 130, 138))
    d.ellipse([150, 560, 650, 720], fill=(120, 110, 50))
    d.ellipse([190, 570, 610, 680], fill=(150, 136, 64))
    return im


def ic_malax():
    im, d = canvas()
    d.chord([120, 220, 600, 700], 0, 180, fill=(184, 194, 200))
    d.rectangle([120, 440, 600, 462], fill=(150, 162, 170))
    d.ellipse([140, 400, 580, 500], fill=(150, 136, 64))
    for k in range(3):
        d.arc([220 + k * 60, 410, 420 + k * 60, 490], 180, 360, fill=(110, 100, 40), width=12)
    # thermometer
    d.rounded_rectangle([640, 110, 720, 560], radius=40, fill=(255, 255, 255), outline=DARK, width=12)
    d.ellipse([610, 520, 750, 660], fill=RED, outline=DARK, width=12)
    d.rectangle([668, 300, 692, 560], fill=RED)
    f = font(F_BOLD, 96)
    d.text((240, 110), "27°C", font=f, fill=DARK)
    return im


def ic_centrifuge():
    im, d = canvas()
    d.ellipse([170, 170, 630, 630], outline=(150, 162, 170), width=50)
    for k in range(3):
        a = math.radians(k * 120 - 30)
        x, y = 400 + math.cos(a) * 230, 400 + math.sin(a) * 230
        b = a + math.pi / 2
        d.polygon([(x + math.cos(b) * 70, y + math.sin(b) * 70),
                   (x + math.cos(a) * 55, y + math.sin(a) * 55),
                   (x - math.cos(a) * 55, y - math.sin(a) * 55)], fill=DARK)
    d.polygon(ellipse_poly(330, 400, 50, 72, 0), fill=(200, 180, 40))
    d.polygon(ellipse_poly(470, 400, 50, 72, 0), fill=BLUE)
    return im


def ep1():
    orch = bg_orchard(("p",))
    shots = [
        Shot(orch, [
            ("zeyto", "Brrr! Hava soğudu, dallar sallanıyor... Bana neler oluyor?", {"mood": "worried", "color": GREEN_OLIVE}),
            ("zeynep", "Günaydın Zeyto! Korkma, kasım geldi. Hasat zamanı! Defterime her şeyi yazdım.", {"wave": True}),
            ("zeyto", "Hasat mı?! Yani beni sopayla mı dövecekler?", {"mood": "wow", "arms": True}),
            ("zeynep", "Asla! Doğru hasadın 4 altın kuralı var. Dinle.", {}),
        ], zeynep_x=330, zeyto_x=800, zeynep_enter=True),
        Shot(orch, [
            ("zeynep", "Bir: Dalları sırıkla dövme. Kırılan sürgün, gelecek yılın ürünü demek.", {"step": 0, "point": True}),
            ("zeynep", "İki: Ağacın altına file ser, zeytinleri el tırmığıyla nazikçe tara.", {"step": 1, "point": True}),
            ("zeyto", "Oh be! Tırmık bana masaj gibi gelir.", {"arms": True}),
            ("zeynep", "Üç: Çuval yok! Zeytin çuvalda ezilir, ısınır, yağın asitliği artar. Delikli kasa kullan.", {"step": 2, "point": True}),
            ("zeynep", "Dört: Toplanan zeytin bekletilmeden, mümkünse 24 saat içinde sıkılmalı.", {"step": 3, "point": True}),
        ], zeynep_x=270, zeyto_x=840, steps=[
            ("Sırıkla dövme yok", ic_no_stick()), ("File ve el tırmığı", ic_rake_net()),
            ("Çuval değil kasa", ic_crate()), ("24 saatte sıkım", ic_clock())]),
        Shot(orch, [
            ("zeynep", "Özetle: iyi zeytinyağı, fabrikada değil bahçede başlar. Kaydet, unutma!", {"point": True}),
        ], zeynep_x=270, zeyto_x=840, summary=("HASADIN 4 ALTIN KURALI", [
            "Sırıkla dövme", "File ser, tırmıkla tara", "Çuval değil kasa", "24 saatte sıkım"])),
        Shot(orch, [
            ("zeyto", "Peki Mühendis Abi... ben neden morarmaya başladım? Hasta mıyım?!", {"mood": "worried", "color": PURPLE}),
            ("zeynep", "Onu yarın anlatacağım. Takipte kal!", {"wave": True}),
        ], zeynep_x=330, zeyto_x=800, zeyto_color=PURPLE),
        end_shot("Sıradaki not #2:", "Yeşil mi, siyah mı?", PURPLE),
    ]
    return render_episode(shots, "ZEYTO'NUN NOTLARI #1", OUT + "B1_hasadin_4_altin_kurali.mp4")


def end_shot(l1, l2, ycol, cta="Takip et, kaçırma!"):
    return Shot(bg_brand(OLIVE), [("zeynep", "", {"wave": True, "dur": 3.4})], zeynep_x=330, zeyto_x=790,
                zeyto_color=ycol, layout="end", lead=0.0, tail=0.0, end=[
                    (text_image(l1, 60, CREAM, 960, path=F_MED), 470, 0.1),
                    (text_image(l2, 96, SUN, 980), 600, 0.35),
                    (text_image(cta, 54, DARK, 960, pill=SUN, pad=(40, 18)), 790, 0.7)])


def ep2():
    orch = bg_orchard(("p",))
    shots = [
        Shot(orch, [
            ("zeyto", "Mühendis Abi! Dün yemyeşildim, bugün mosmorum. Hasta mıyım?!", {"mood": "worried", "arms": True}),
            ("zeynep", "Hasta değilsin Zeyto, olgunlaşıyorsun! Rengin, olgunluğunu gösterir.", {"ymood": "wow"}),
            ("zeyto", "Yani yeşil zeytinle siyah zeytin aynı ağaçtan mı çıkıyor?", {"mood": "wow"}),
            ("zeynep", "Evet! Aynı ağaç, farklı zaman. Üç durağı var, bak.", {}),
        ], zeynep_x=330, zeyto_x=800, zeyto_color=PURPLE, zeynep_enter=True),
        Shot(orch, [
            ("zeynep", "Yeşil, yani erken hasat: yağı az ama yoğun aromalı. O acılık ve yakıcılık, bol polifenolden gelir.", {"step": 0, "point": True}),
            ("zeynep", "Mor, yani yarı olgun: yağ miktarı artar, tadı dengelenir.", {"step": 1, "point": True}),
            ("zeyto", "İşte ben buradayım!", {"arms": True}),
            ("zeynep", "Siyah, yani tam olgun: yağ en bol, tadı yumuşak ve tatlımsı.", {"step": 2, "point": True}),
        ], zeynep_x=270, zeyto_x=840, zeyto_color=PURPLE, accent=PURPLE, steps=[
            ("Yeşil: erken hasat", icon_olive(GREEN_OLIVE)), ("Mor: yarı olgun", icon_olive(PURPLE)),
            ("Siyah: tam olgun", icon_olive(BLACKOLIVE))]),
        Shot(orch, [
            ("zeynep", "Yani zeytin olgunlaştıkça yağı artar, acılığı azalır. Tadı seçimine göre toplarız!", {"point": True}),
        ], zeynep_x=270, zeyto_x=840, zeyto_color=PURPLE, accent=PURPLE, summary=("RENK = OLGUNLUK", [
            "Yeşil: az yağ, acı ve aromatik", "Mor: dengeli", "Siyah: bol yağ, yumuşak"])),
        Shot(orch, [
            ("zeyto", "Sen hangi tadı seversin? Yorumlara yaz! Peki ben yağa nasıl dönüşeceğim?", {"arms": True}),
            ("zeynep", "Yarın fabrikaya gidiyoruz!", {"wave": True}),
        ], zeynep_x=330, zeyto_x=800, zeyto_color=PURPLE),
        end_shot("Sıradaki not #3:", "Zeytinden yağa", PURPLE),
    ]
    return render_episode(shots, "ZEYTO'NUN NOTLARI #2", OUT + "B2_yesil_mi_siyah_mi.mp4")


def ep3():
    mill = bg_mill()
    bottle = fit(icon_bottle(), width=230)
    shots = [
        Shot(mill, [
            ("zeyto", "Burası neresi?! Her yer makine, her yer gürültü!", {"mood": "wow", "color": BLACKOLIVE}),
            ("zeynep", "Zeytinyağı fabrikasındayız! Bugün zeytinden yağa yolculuğunu anlatacağım.", {}),
        ], zeynep_x=330, zeyto_x=800, zeyto_color=BLACKOLIVE, zeynep_enter=True),
        Shot(mill, [
            ("zeynep", "Bir: Yapraklar ayrılır, zeytinler yıkanır.", {"step": 0, "point": True}),
            ("zeynep", "İki: Zeytin, çekirdeğiyle birlikte kırılıp hamur olur.", {"step": 1, "point": True}),
            ("zeyto", "Hamur mu?! Ben artık zeytin ezmesi miyim?", {"mood": "wow"}),
            ("zeynep", "Üç: Hamur yavaşça yoğrulur. Isı 27 derecenin altında kalırsa buna soğuk sıkım denir.", {"step": 2, "point": True}),
            ("zeynep", "Dört: Santrifüj; yağı, suyu ve posayı birbirinden ayırır.", {"step": 3, "point": True}),
            ("zeynep", "Beş: Yağ dinlenir, tortusu çöker ve ışık geçirmeyen şişeye dolar.", {"step": 4, "point": True}),
        ], zeynep_x=270, zeyto_x=840, zeyto_color=BLACKOLIVE, steps=[
            ("Yıkama", ic_wash()), ("Kırma", ic_crush()), ("Yoğurma", ic_malax()),
            ("Ayrıştırma", ic_centrifuge()), ("Dinlenme ve şişe", icon_bottle())]),
        Shot(mill, [
            ("zeynep", "Hepsi bu! Bahçeden şişeye beş adım. Kaydet, sofrada anlat!", {"point": True}),
        ], zeynep_x=270, zeyto_x=840, zeyto_color=BLACKOLIVE, summary=("ZEYTİNDEN YAĞA 5 ADIM", [
            "Yıkama", "Kırma", "Yoğurma (27°C altı)", "Ayrıştırma", "Dinlenme ve şişe"])),
        Shot(mill, [
            ("zeyto", "Yani ben artık... yeni sezon zeytinyağıyım!", {"arms": True, "mood": "wow"}),
            ("zeynep", "Hem de taze, yeşil ve hafif yakıcı. Ön sipariş açık, DM'den yazın!", {"wave": True}),
            ("zeyto", "Ama bazı kardeşlerim yağ olmuyor, sofraya gidiyor. Onlar neden o kadar acı?", {"mood": "worried"}),
        ], zeynep_x=330, zeyto_x=760, zeyto_color=BLACKOLIVE, props=[(bottle, 960, 1700)]),
        end_shot("Sıradaki not #4:", "Zeytin neden acı?", GREEN_OLIVE),
    ]
    return render_episode(shots, "ZEYTO'NUN NOTLARI #3", OUT + "B3_zeytinden_yaga.mp4")


if __name__ == "__main__":
    for w in sys.argv[1:] or ["1", "2", "3"]:
        print(globals()["ep" + w]())
