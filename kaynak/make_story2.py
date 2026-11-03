"""Mühendisin Defteri - Bölüm 4-7 (zeytin serisi devamı)."""
import sys, math, random
from functools import lru_cache
from PIL import Image, ImageDraw
from brand import *
from story import Shot, render_episode, bg_orchard, bg_brand, vgrad, W, H, BGW
from make_story import canvas, end_shot, ic_wash, OUT, BLUE

BRINE = (214, 226, 196)
GLASS = (200, 228, 236)


@lru_cache(maxsize=2)
def bg_kitchen():
    rnd = random.Random(5)
    im = vgrad(BGW, H, (250, 240, 220), (240, 226, 200))
    d = ImageDraw.Draw(im)
    # tiles
    for y in range(820, 1330, 70):
        for x in range(0, BGW, 70):
            d.rectangle([x + 3, y + 3, x + 67, y + 67], fill=(236, 244, 236) if (x // 70 + y // 70) % 2 else (226, 236, 226))
    # window
    d.rounded_rectangle([700, 260, 1080, 660], radius=24, fill=(170, 214, 236), outline=(196, 160, 110), width=22)
    d.line([(890, 260), (890, 660)], fill=(196, 160, 110), width=16)
    for x, y, r in [(780, 560, 70), (880, 520, 90), (990, 570, 70)]:
        d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=(130, 160, 90))
    # shelf with jars
    d.rectangle([80, 560, 560, 590], fill=(176, 128, 80))
    for k, x in enumerate((120, 260, 400)):
        d.rounded_rectangle([x, 420, x + 110, 560], radius=18, fill=GLASS)
        d.rectangle([x + 8, 400, x + 102, 428], fill=RED if k == 1 else OLIVE)
        for j in range(5):
            ox, oy = x + 25 + (j % 3) * 30, 490 + (j // 3) * 34
            d.ellipse([ox - 14, oy - 11, ox + 14, oy + 11], fill=[GREEN_OLIVE, BLACKOLIVE, PURPLE][(j + k) % 3])
    # counter
    d.rectangle([0, 1330, BGW, 1420], fill=(196, 150, 100))
    d.rectangle([0, 1420, BGW, H], fill=(160, 112, 70))
    for x in range(0, BGW, 300):
        d.rectangle([x + 20, 1460, x + 280, H - 40], outline=(140, 96, 58), width=8)
        d.rounded_rectangle([x + 130, 1500, x + 170, 1516], radius=6, fill=(110, 76, 44))
    # cutting board with olives
    d.rounded_rectangle([760, 1290, 1120, 1345], radius=20, fill=(222, 180, 120))
    for j in range(6):
        ox = 800 + j * 50
        d.ellipse([ox - 18, 1288 - 14, ox + 18, 1288 + 14], fill=GREEN_OLIVE)
    return im


# ---------------------------------------------------------------- icons
def ic_water():
    im, d = canvas()
    d.chord([110, 260, 690, 720], 0, 180, fill=GLASS)
    d.ellipse([110, 440, 690, 540], fill=(150, 200, 226))
    for k in range(7):
        x, y = 210 + (k % 4) * 120 + (k // 4) * 60, 520 + (k // 4) * 70
        d.ellipse([x - 40, y - 30, x + 40, y + 30], fill=GREEN_OLIVE)
    # refresh arrows (water changed daily)
    d.arc([260, 60, 540, 340], 200, 340, fill=BLUE, width=30)
    d.polygon([(520, 120), (580, 190), (500, 200)], fill=BLUE)
    f = font(F_BOLD, 64)
    d.text((400 - f.getlength("her gün") / 2, 150), "her gün", font=f, fill=DARK)
    return im


def ic_jar(lemon=False, label=None):
    im, d = canvas()
    d.rounded_rectangle([200, 220, 600, 740], radius=60, fill=GLASS)
    d.rounded_rectangle([210, 330, 590, 730], radius=52, fill=BRINE)
    d.rounded_rectangle([230, 130, 570, 230], radius=20, fill=RED)
    for k in range(14):
        x, y = 270 + (k % 4) * 85 + (k // 4 % 2) * 30, 420 + (k // 4) * 80
        if y < 700:
            d.ellipse([x - 38, y - 28, x + 38, y + 28], fill=[GREEN_OLIVE, (110, 140, 44)][k % 2])
    if lemon:
        d.ellipse([390, 380, 500, 490], fill=SUN)
        d.ellipse([405, 395, 485, 475], fill=(255, 236, 140))
        for k in range(6):
            a = math.radians(k * 60)
            d.line([(445, 435), (445 + math.cos(a) * 38, 435 + math.sin(a) * 38)], fill=SUN, width=5)
        d.polygon(leaf_poly(300, 400, 120, 30, -60), fill=LEAF)
        d.polygon(leaf_poly(330, 600, 110, 28, 40), fill=LEAF)
    d.polygon(ellipse_poly(250, 420, 16, 100, 0), fill=(255, 255, 255, 110))
    if label:
        f = font(F_BOLD, 76)
        d.rounded_rectangle([230, 560, 570, 680], radius=20, fill=CREAM)
        d.text((400 - f.getlength(label) / 2, 572), label, font=f, fill=DARK)
    return im


def ic_salt():
    im, d = canvas()
    d.polygon([(130, 690), (400, 300), (670, 690)], fill=(250, 250, 252))
    rnd = random.Random(2)
    for k in range(80):
        x, y = rnd.uniform(200, 600), rnd.uniform(420, 680)
        if abs(x - 400) < (y - 300) * 0.69:
            d.rectangle([x, y, x + 10, y + 10], fill=(214, 220, 228))
    for k, (x, y) in enumerate([(220, 640), (330, 560), (480, 600), (590, 660), (400, 680)]):
        draw_olive(d, x, y, 46, BLACKOLIVE)
    d.rounded_rectangle([120, 690, 680, 730], radius=18, fill=(176, 128, 80))
    return im


def ic_mallet():
    im, d = canvas()
    d.rounded_rectangle([100, 600, 700, 700], radius=24, fill=(222, 180, 120))
    draw_olive(d, 400, 560, 70, GREEN_OLIVE)
    d.line([(400, 500), (380, 600)], fill=DARK, width=8)          # crack
    d.line([(400, 520), (430, 580)], fill=DARK, width=6)
    d.line([(560, 110), (440, 380)], fill=BROWN, width=40)
    d.rounded_rectangle([300, 300, 560, 440], radius=30, fill=(176, 128, 80))
    for x, y in [(290, 470), (520, 470)]:
        d.line([(x, y), (x + (-40 if x < 400 else 40), y - 30)], fill=SUN, width=12)
    return im


def ic_brine_scale():
    im, d = canvas()
    d.rounded_rectangle([120, 260, 420, 700], radius=40, fill=GLASS)
    d.rounded_rectangle([130, 340, 410, 690], radius=34, fill=(150, 200, 226))
    f = font(F_BOLD, 90)
    d.text((270 - f.getlength("1 L") / 2, 450), "1 L", font=f, fill=DARK)
    d.text((440, 400), "+", font=font(F_BOLD, 120), fill=DARK)
    d.polygon([(500, 690), (620, 480), (740, 690)], fill=(250, 250, 252), outline=DARK, width=6)
    f2 = font(F_BOLD, 70)
    d.text((620 - f2.getlength("80 g") / 2, 560), "80 g", font=f2, fill=RED)
    return im


def ic_fridge():
    im, d = canvas()
    d.rounded_rectangle([210, 70, 590, 740], radius=40, fill=(236, 240, 244), outline=(160, 170, 180), width=12)
    d.line([(210, 300), (590, 300)], fill=(160, 170, 180), width=12)
    d.rounded_rectangle([530, 130, 556, 250], radius=10, fill=(160, 170, 180))
    d.rounded_rectangle([530, 360, 556, 520], radius=10, fill=(160, 170, 180))
    for k in range(6):
        a = math.radians(k * 60)
        d.line([(400, 180), (400 + math.cos(a) * 70, 180 + math.sin(a) * 70)], fill=BLUE, width=12)
    f = font(F_BOLD, 80)
    d.text((400 - f.getlength("1-2 hafta") / 2, 470), "1-2 hafta", font=f, fill=DARK)
    return im


def ic_no_sun():
    im, d = canvas()
    d.ellipse([250, 250, 550, 550], fill=SUN)
    for k in range(10):
        a = math.radians(k * 36)
        d.line([(400 + math.cos(a) * 190, 400 + math.sin(a) * 190), (400 + math.cos(a) * 270, 400 + math.sin(a) * 270)], fill=SUN, width=26)
    d.ellipse([100, 100, 700, 700], outline=RED, width=50)
    d.line([(190, 190), (610, 610)], fill=RED, width=50)
    return im


def ic_thermo():
    im, d = canvas()
    d.rounded_rectangle([330, 80, 470, 560], radius=70, fill=(255, 255, 255), outline=DARK, width=16)
    d.ellipse([280, 500, 520, 740], fill=BLUE, outline=DARK, width=16)
    d.rectangle([380, 340, 420, 560], fill=BLUE)
    for k in range(5):
        d.line([(470, 150 + k * 80), (510, 150 + k * 80)], fill=DARK, width=10)
    f = font(F_BOLD, 76)
    d.text((540, 300), "14-18", font=f, fill=DARK)
    d.text((560, 390), "°C", font=f, fill=DARK)
    return im


def ic_cap():
    im = icon_bottle()
    d = ImageDraw.Draw(im)
    d.arc([520, 20, 760, 260], 200, 360, fill=OLIVE, width=24)
    d.polygon([(745, 130), (770, 200), (700, 170)], fill=OLIVE)
    return im


def ic_containers():
    im, d = canvas()
    b = fit(icon_bottle(), width=420)
    im.alpha_composite(b, (40, 40))
    d.rounded_rectangle([420, 300, 740, 740], radius=24, fill=(200, 205, 210), outline=(150, 160, 168), width=10)
    d.rounded_rectangle([540, 240, 620, 310], radius=10, fill=(150, 160, 168))
    d.rounded_rectangle([450, 420, 710, 620], radius=16, fill=OLIVE)
    draw_olive(d, 580, 520, 48, GREEN_OLIVE)
    return im


def ic_pan():
    im, d = canvas()
    d.ellipse([90, 300, 590, 560], fill=(60, 60, 66))
    d.ellipse([120, 315, 560, 530], fill=(200, 180, 60))
    for x, y in [(240, 400), (360, 450), (450, 390)]:
        d.rounded_rectangle([x - 60, y - 22, x + 60, y + 22], radius=18, fill=(236, 190, 100))
    d.rounded_rectangle([570, 400, 780, 450], radius=20, fill=(60, 60, 66))
    for k in range(3):
        x = 220 + k * 120
        d.polygon([(x, 290), (x - 30, 230), (x + 10, 170), (x + 30, 240)], fill=(255, 255, 255, 140))
    f = font(F_BOLD, 76)
    d.text((340 - f.getlength("170-180°C") / 2, 600), "170-180°C", font=f, fill=RED)
    return im


def ic_throat():
    im, d = canvas()
    draw_olive(d, 400, 420, 210, GREEN_OLIVE)
    for k, (x, y) in enumerate([(580, 170), (660, 260), (640, 370)]):
        d.polygon([(x, y - 70), (x - 40, y + 30), (x, y + 10), (x + 40, y + 30)], fill=RED if k % 2 == 0 else SUN)
    f = font(F_BOLD, 80)
    d.text((400 - f.getlength("polifenol") / 2, 650), "polifenol", font=f, fill=DARK)
    return im


def ic_lab():
    im, d = canvas()
    d.polygon([(330, 100), (470, 100), (470, 330), (640, 680), (160, 680), (330, 330)], fill=GLASS, outline=DARK, width=14)
    d.polygon([(260, 480), (540, 480), (630, 670), (170, 670)], fill=(200, 180, 60))
    d.rectangle([310, 80, 490, 120], fill=DARK)
    for x, y, r in [(330, 560, 20), (430, 600, 14), (380, 520, 10)]:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(240, 220, 120))
    return im


# ---------------------------------------------------------------- episodes
def ep4():
    orch = bg_orchard(("g",))
    shots = [
        Shot(orch, [
            ("zeyto", "Mühendis Abi! Biri dalımdaki kardeşimi ısırdı, 'Bu ne acı!' diye bağırdı!", {"mood": "worried"}),
            ("zeynep", "Haklı Zeyto. Dalından koparılan zeytin yenmez, çok acıdır.", {}),
            ("zeyto", "Neden?! Ben aslında çok tatlı biriyim!", {"mood": "wow", "arms": True}),
            ("zeynep", "Acının sebebi oleuropein adında bir madde. Defterimde onu atmanın 3 yolu var.", {}),
        ], zeynep_x=330, zeyto_x=800, zeynep_enter=True),
        Shot(orch, [
            ("zeynep", "Bir: Kırılan ya da çizilen zeytin suya konur. Su her gün değişir, acı yavaş yavaş çıkar.", {"step": 0, "point": True}),
            ("zeynep", "İki: Salamura. Tuzlu suda aylarca bekler, mayalanır ve lezzetlenir.", {"step": 1, "point": True}),
            ("zeyto", "Aylarca mı?! Sabır benim göbek adım olacak.", {"mood": "wow"}),
            ("zeynep", "Üç: Kuru tuzlama. Siyah zeytin kaba tuzla katlanır, tuz acıyı ve suyu çeker. Ege'de buna sele zeytin denir.", {"step": 2, "point": True}),
        ], zeynep_x=270, zeyto_x=840, steps=[
            ("Suda bekletme", ic_water()), ("Salamura", ic_jar()), ("Kuru tuzlama", ic_salt())]),
        Shot(orch, [
            ("zeynep", "Yani sofradaki her zeytin, sabırla tatlandırılmış bir zeytindir. Kaydet!", {"point": True}),
        ], zeynep_x=270, zeyto_x=840, summary=("ACIYI ATMANIN 3 YOLU", [
            "Suda bekletme", "Salamura", "Kuru tuzlama (sele)"])),
        Shot(orch, [
            ("zeyto", "Peki evde kırma zeytin yapabilir miyiz?", {"arms": True}),
            ("zeynep", "Yarın mutfağa geçiyoruz, tarifi birlikte yapacağız!", {"wave": True}),
        ], zeynep_x=330, zeyto_x=800),
        end_shot("Sıradaki not #5:", "Evde kırma zeytin", GREEN_OLIVE),
    ]
    return render_episode(shots, "ZEYTO'NUN NOTLARI #4", OUT + "B4_zeytin_neden_aci.mp4")


def ep5():
    kit = bg_kitchen()
    shots = [
        Shot(kit, [
            ("zeyto", "Burası mutfak! Mühendis Abi, beni ne yapacaksın?", {"mood": "wow"}),
            ("zeynep", "Seni nefis bir kırma zeytin yapacağız! Defterimdeki tarif 5 adım.", {}),
        ], zeynep_x=330, zeyto_x=800, zeynep_enter=True),
        Shot(kit, [
            ("zeynep", "Bir: Yeşil zeytini tahta tokmakla, çekirdeğini kırmadan hafifçe çatlat.", {"step": 0, "point": True}),
            ("zeyto", "Yavaş ol, ben hassas bir zeytinim!", {"mood": "worried"}),
            ("zeynep", "İki: Suya koy, suyunu her gün değiştir. 7-10 gün sonra tadına bak, acı gitti mi?", {"step": 1, "point": True}),
            ("zeynep", "Üç: Salamura hazırla. 1 litre suya yaklaşık 80 gram tuz, yani yüzde 8.", {"step": 2, "point": True}),
            ("zeynep", "Dört: Zeytinleri kavanoza diz, limon dilimi ve kekik ekle, salamurayı üstüne dök.", {"step": 3, "point": True}),
            ("zeynep", "Beş: Buzdolabında 1-2 hafta dinlendir. Servis ederken zeytinyağı gezdir!", {"step": 4, "point": True}),
            ("zeyto", "Hmm, kekik kokusu... Bayıldım!", {"arms": True}),
        ], zeynep_x=270, zeyto_x=840, steps=[
            ("Çatlat", ic_mallet()), ("Suda beklet", ic_water()), ("Salamura", ic_brine_scale()),
            ("Kavanozla", ic_jar(lemon=True)), ("Dinlendir", ic_fridge())]),
        Shot(kit, [
            ("zeynep", "Tarif tamam! Kaydet, hafta sonu dene, yapınca bizi etiketle.", {"point": True}),
        ], zeynep_x=270, zeyto_x=840, summary=("EVDE KIRMA ZEYTİN", [
            "Çekirdeği kırmadan çatlat", "7-10 gün su, her gün değiştir", "1 L su + 80 g tuz",
            "Limon + kekik", "1-2 hafta dinlendir"])),
        Shot(kit, [
            ("zeyto", "Üstüne yağ gezdirdik... Peki o yağ nasıl saklanmalı?", {"mood": "wow"}),
            ("zeynep", "Yarın anlatıyorum. Çoğu evde yanlış yapılıyor!", {"wave": True}),
        ], zeynep_x=330, zeyto_x=800),
        end_shot("Sıradaki not #6:", "Yağ nasıl saklanır?", GREEN_OLIVE),
    ]
    return render_episode(shots, "ZEYTO'NUN NOTLARI #5", OUT + "B5_evde_kirma_zeytin.mp4")


def ep6():
    kit = bg_kitchen()
    bottle = fit(icon_bottle(), width=200)
    shots = [
        Shot(kit, [
            ("zeyto", "Mühendis Abi! Yağ şişesi ocağın dibinde duruyor. Sıcaktan terledi!", {"mood": "worried", "arms": True}),
            ("zeynep", "Eyvah! Zeytinyağının 4 düşmanı var: ışık, sıcak, hava ve yanlış kap.", {}),
        ], zeynep_x=330, zeyto_x=780, zeynep_enter=True, props=[(bottle, 980, 1700)]),
        Shot(kit, [
            ("zeynep", "Bir: Işık yağı bozar. Şişeyi tezgâhta değil, karanlık bir dolapta sakla.", {"step": 0, "point": True}),
            ("zeynep", "İki: Ocaktan ve fırından uzak tut. İdeal sıcaklık 14 ile 18 derece arası.", {"step": 1, "point": True}),
            ("zeynep", "Üç: Hava yağı oksitler. Kullandıktan sonra kapağı hemen kapat.", {"step": 2, "point": True}),
            ("zeynep", "Dört: Koyu cam, teneke ya da paslanmaz çelik kullan. Plastik şişede uzun süre bekletme.", {"step": 3, "point": True}),
            ("zeyto", "Peki yağ ne zamana kadar taze kalır?", {"mood": "wow"}),
            ("zeynep", "Açılan şişeyi birkaç ay içinde bitir. Zeytinyağı şarap değil, bekledikçe güzelleşmez!", {"step": 3}),
        ], zeynep_x=270, zeyto_x=840, steps=[
            ("Işıktan uzak", ic_no_sun()), ("Serin yer", ic_thermo()), ("Kapak kapalı", ic_cap()),
            ("Doğru kap", ic_containers())]),
        Shot(kit, [
            ("zeynep", "Bu dört kurala uyarsan yağın ilk günkü gibi kalır. Kaydet!", {"point": True}),
        ], zeynep_x=270, zeyto_x=840, summary=("YAĞIN 4 DÜŞMANI", [
            "Işık: karanlık dolap", "Sıcak: 14-18 °C", "Hava: kapak kapalı", "Plastik: koyu cam veya teneke"])),
        Shot(kit, [
            ("zeyto", "Teyzem 'zeytinyağıyla kızartma yapılmaz' diyor. Doğru mu?", {"mood": "worried"}),
            ("zeynep", "Yarın efsaneleri tek tek çürütüyoruz!", {"wave": True}),
        ], zeynep_x=330, zeyto_x=800),
        end_shot("Sıradaki not #7:", "Yağ efsaneleri", GREEN_OLIVE),
    ]
    return render_episode(shots, "ZEYTO'NUN NOTLARI #6", OUT + "B6_yag_nasil_saklanir.mp4")


def ep7():
    kit = bg_kitchen()
    shots = [
        Shot(kit, [
            ("zeyto", "Bugün efsane avına çıkıyoruz! Hazır mısın Mühendis Abi?", {"arms": True}),
            ("zeynep", "Defterim hazır! Kulaktan dolma 3 efsane, 3 gerçek.", {}),
        ], zeynep_x=330, zeyto_x=800, zeynep_enter=True),
        Shot(kit, [
            ("zeynep", "Efsane 1: 'Zeytinyağıyla kızartma yapılmaz.' Yanlış! Natürel sızma yaklaşık 190 derecenin üstünde dumanlanır; evde kızartma 170-180 derecede yapılır.", {"step": 0, "point": True}),
            ("zeyto", "Teyzeme hemen haber veriyorum!", {"arms": True}),
            ("zeynep", "Efsane 2: 'Acı yağ bozuktur.' Yanlış! Boğazdaki yakıcılık polifenol, yani tazelik işaretidir. Kötü işaret sirke ya da küf kokusudur.", {"step": 1, "point": True}),
            ("zeynep", "Efsane 3: 'Buzdolabında donan yağ saftır.' Yanlış! Donma bir saflık testi değildir. Saflığı ancak laboratuvar analizi gösterir.", {"step": 2, "point": True}),
        ], zeynep_x=270, zeyto_x=840, accent=RED, steps=[
            ("Kızartma yapılır", ic_pan()), ("Acılık tazeliktir", ic_throat()), ("Donma test değildir", ic_lab())]),
        Shot(kit, [
            ("zeynep", "Bunu kaydet, sofrada efsane duyunca göster!", {"point": True}),
        ], zeynep_x=270, zeyto_x=840, accent=RED, summary=("EFSANE AVCISI", [
            "Zeytinyağıyla kızartma yapılır", "Acılık, tazelik işaretidir", "Donma, saflık testi değildir"])),
        Shot(kit, [
            ("zeyto", "Bir haftada ne çok şey öğrendik! Sen hangi efsaneye inanıyordun? Yorumlara yaz!", {"arms": True}),
            ("zeynep", "Defterin yeni sayfaları pazartesi geliyor. Yeni sezon yağımız için DM'den yazın!", {"wave": True}),
        ], zeynep_x=330, zeyto_x=800),
        end_shot("Yeni sezon zeytinyağı", "Ön sipariş açık!", GREEN_OLIVE, cta="Sipariş için DM"),
    ]
    return render_episode(shots, "ZEYTO'NUN NOTLARI #7", OUT + "B7_3_zeytinyagi_efsanesi.mp4")


if __name__ == "__main__":
    for w in sys.argv[1:] or ["4", "5", "6", "7"]:
        print(globals()["ep" + w]())
