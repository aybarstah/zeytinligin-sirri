"""Zeytinliğin Sırrı — Sezon 2: Kayıp Fidan (20 bölüm, her gün 20:00)."""
import sys
from brand import *
from story import Shot, render_episode, bg_orchard, bg_mill
from make_main import bg_sunset, bg_clearing, end_shot, notebook_page, OUT, ic_collect
from make_main2 import ulu, with_ulu, duo, steps, summary, card, glow, NIGHT, Z, Y, U, S, B, M
from make_story2 import ic_throat
import scenes2 as sc
import scenes3 as s3

LABEL = "SEZON 2 · BÖLÜM {}"
TITLES = {1: "Haritanın Sırrı", 2: "Muhtar'ın Hikâyesi", 3: "Kaçak Yolcu", 4: "Dere Geçidi", 5: "Terk Edilmiş Bahçe",
          6: "Boş Çukur", 7: "Kovalamaca", 8: "Ateşin Başında", 9: "Eski Okul", 10: "Kepçe Karşısında",
          11: "İmzasız İzin", 12: "Gece Nöbeti", 13: "Gövdedeki Yazı", 14: "Laboratuvar Sonucu", 15: "Köy Toplantısı",
          16: "Eski Anahtar", 17: "Sinsi'nin Seçimi", 18: "Beton'un Sırrı", 19: "Hasta Yapraklar", 20: "Kayıp Fidan"}
FILES = {n: f"S2B{n}_{t}" for n, t in {1: "haritanin_sirri", 2: "muhtarin_hikayesi", 3: "kacak_yolcu", 4: "dere_gecidi",
         5: "terk_edilmis_bahce", 6: "bos_cukur", 7: "kovalamaca", 8: "atesin_basinda", 9: "eski_okul", 10: "kepce_karsisinda",
         11: "imzasiz_izin", 12: "gece_nobeti", 13: "govdedeki_yazi", 14: "laboratuvar_sonucu", 15: "koy_toplantisi",
         16: "eski_anahtar", 17: "sinsinin_secimi", 18: "betonun_sirri", 19: "hasta_yapraklar", 20: "kayip_fidan"}.items()}


def END(n):
    return end_shot(f"Bölüm {n} yarın 20:00", TITLES[n], GREEN_OLIVE, cta="Takip et, hikâyeyi kaçırma!")


def R(n, shots):
    return render_episode(shots, LABEL.format(n), OUT + FILES[n] + ".mp4")


def sinsi_at(x=760, y=800, scale=0.85, appear=0.0):
    return {"kind": "sinsi", "x": x, "y": y, "scale": scale, "appear": appear}


def beton_at(x=760, scale=0.8, enter=False, appear=0.0, look=None):
    a = {"kind": "beton", "x": x, "scale": scale, "enter": enter, "appear": appear}
    if look is not None:
        a["look"] = look
    return a


def muhtar_at(x=210, scale=0.78, look=1):
    return {"kind": "muhtar", "x": x, "scale": scale, "look": look}


# ---------------------------------------------------------------- 1
def ep1():
    clear = bg_clearing(False)
    shots = [
        card(clear, [
            (Y, "Mühendis Abi, haritayı Ulu'ya gösterelim! O her şeyi bilir.", {"arms": True, "tag": "excited"}),
            (Z, "Haklısın. Ulu, bu dere ve bu dağlar sana tanıdık geliyor mu?", {"tag": "curious"}),
        ], sc.new_map()),
        with_ulu(clear, [
            (U, "Hımm... Bu dağ yolunu yıllardır görmedim. Deden bir bahar sabahı benim dalımdan bir çelik kesti.", {"tag": "nostalgic"}),
            (U, "Onu dağdaki eski bahçeye dikti. O fidan benim tek yavrum.", {"tag": "softly"}),
            (Y, "Ulu'nun bebeği mi var?! Kardeşim olur o zaman!", {"arms": True, "mood": "wow", "tag": "excited"}),
        ]),
        steps(clear, [
            (Z, "Bir: Çelikten büyüyen fidan, ana ağacın tıpatıp aynısıdır. Aynı çeşit, aynı yaprak, aynı meyve.", {"step": 0, "point": True}),
            (Z, "İki: Çekirdekten çıkan ağaç ise farklı olur, çoğu zaman yabaniye döner.", {"step": 1, "point": True}),
            (U, "Benim çeşidim bu köyde tek kaldı. O fidan yaşıyorsa, soyum sürer.", {"tag": "hopeful"}),
        ], [("Çelik: aynı çeşit", sc.ic_cutting()), ("Çekirdek: farklı ağaç", sc.ic_seed())]),
        with_ulu(clear, [
            (B, "Dünyada tek bir çeşit, ha? O fidan servet eder... Önce ben bulacağım!", {"tag": "whispers"}),
        ], actors=[ulu(), beton_at(1000, 0.62, appear=0.0, look=-1)], zeynep_x=None, zeyto_x=None),
        END(2),
    ]
    return R(1, shots)


# ---------------------------------------------------------------- 2
def ep2():
    cafe = sc.bg_coffee()
    shots = [
        Shot(cafe, [
            (M, "Dağdaki bahçe mi? Orası otuz yıldır terk edilmiş evlat.", {"tag": "surprised"}),
            (Z, "Neden terk edildi Muhtar Amca?", {"tag": "curious"}),
            (M, "Doksan altı kışında ayaz vurdu. Genç ağaçların çoğu dondu. Deden çok üzülmüştü.", {"tag": "sadly"}),
        ], zeynep_x=830, zeynep_scale=0.72, zeyto_x=620, gap=0.28, actors=[muhtar_at(260, 0.8)]),
        steps(cafe, [
            (Z, "Bir: Zeytin soğuğu sevmez. Eksi yedi derecenin altında yaprak ve dallar zarar görebilir.", {"step": 0, "point": True}),
            (Z, "İki: Genç fidan çok daha hassastır. Gövdesi çuval ya da özel bezle sarılır.", {"step": 1, "point": True}),
            (Y, "Ağaca atkı örüyoruz yani!", {"arms": True, "tag": "giggles"}),
            (Z, "Üç: Dibine toprak doldurulur, soğuk rüzgâr alan yere dikilmez.", {"step": 2, "point": True}),
        ], [("−7 °C sınırı", s3.ic_snow()), ("Gövdeyi sar", s3.ic_wrap_trunk()), ("Rüzgârdan koru", s3.ic_mountain())]),
        Shot(cafe, [
            (M, "Bir şey daha var. Beton dün bana dağ yolunu sordu. Elinde de bir kürek vardı.", {"tag": "worried"}),
            (Y, "Beton Bey de fidanı arıyor! Yarın sabah yola çıkıyoruz!", {"mood": "worried", "arms": True, "tag": "urgent", "gap": 0.6}),
        ], zeynep_x=830, zeynep_scale=0.72, zeyto_x=620, gap=0.28, actors=[muhtar_at(260, 0.8)]),
        END(3),
    ]
    return R(2, shots)


# ---------------------------------------------------------------- 3
def ep3():
    mt = s3.bg_mountain()
    shots = [
        duo(mt, [
            (Y, "Mühendis Abi, sırt çantan kendi kendine vızıldıyor!", {"mood": "wow", "tag": "surprised"}),
            (Z, "Vızıldıyor mu? Dur, açıyorum...", {"tag": "suspicious"}),
        ]),
        Shot(mt, [
            (S, "Vızzz... Sürpriz! Ben de geliyorum!", {"tag": "playfully"}),
            (Z, "Sinsi! Sana nasıl güvenelim? Geçen sezon raporu sen çalmıştın.", {"tag": "annoyed"}),
            (S, "Özür diledim ya! Bu dağları yukarıdan ben görürüm. Size yol gösteririm.", {"tag": "pleading"}),
            (Y, "Bir şans verelim Abi. Herkes değişebilir.", {"tag": "gently"}),
        ], zeynep_x=300, zeyto_x=520, gap=0.28, actors=[sinsi_at(820, 820, 0.85)]),
        steps(mt, [
            (S, "Bilginiz olsun, ben bu kadar yükseğe pek çıkmam. Zeytin de çıkmaz!", {"tag": "matter-of-fact"}),
            (Z, "Doğru. Bir: Zeytin genelde yedi yüz metrenin altında iyi yetişir.", {"step": 0, "point": True}),
            (Z, "İki: Bol güneş ister. Üç: Suyu tutmayan, süzek toprağı sever.", {"step": 1, "point": True}),
        ], [("~700 m altı", s3.ic_mountain()), ("Bol güneş, süzek toprak", s3.ic_sun_hours())]),
        Shot(mt, [
            (S, "Eyvah! Öndeki köprü yıkılmış!", {"tag": "alarmed"}),
            (Y, "Peki karşıya nasıl geçeceğiz?", {"mood": "worried", "tag": "scared", "gap": 0.6}),
        ], zeynep_x=300, zeyto_x=520, gap=0.28, actors=[sinsi_at(820, 760, 0.85)]),
        END(4),
    ]
    return R(3, shots)


# ---------------------------------------------------------------- 4
def ep4():
    rv = s3.bg_river()
    shots = [
        duo(rv, [
            (Z, "Taşların üstünden atlayacağız. Zeyto, sen cebime gir.", {"tag": "determined"}),
            (Y, "Hayır, ben de atlarım! Bir... iki... Aaa! Suya düştüm!", {"mood": "worried", "tag": "panicked"}),
            (Y, "Aa... Ben yüzüyormuşum! Zeytin suyun üstünde kalırmış!", {"arms": True, "mood": "wow", "tag": "laughing"}),
        ], zeyto_drop=0.4),
        steps(rv, [
            (Z, "Sen yüzersin ama zeytin ağacının kökleri suda boğulur. Bir: Su biriken toprakta kökler çürür.", {"step": 0, "point": True}),
            (Z, "İki: Bu yüzden zeytinlikte su yolu açılır, toprak süzek olmalı.", {"step": 1, "point": True}),
            (Z, "Üç: Yine de ilk yıllarda ve kurak yazlarda sulama ister. En iyisi damla sulama.", {"step": 2, "point": True}),
        ], [("Kök suda boğulur", s3.ic_roots_water()), ("Süzek toprak", s3.ic_drop(bad=True)), ("Damla sulama", s3.ic_drip())]),
        duo(rv, [
            (Y, "Karşıya geçtik! Ama bak, çamurda kocaman ayak izleri var.", {"mood": "worried", "tag": "curious"}),
            (Z, "Bunlar çizme izi. Ve daha yeni... Beton Bey bizden önde.", {"tag": "tense", "gap": 0.6}),
        ]),
        END(5),
    ]
    return R(4, shots)


# ---------------------------------------------------------------- 5
def ep5():
    rn = s3.bg_ruin()
    shots = [
        duo(rn, [
            (Y, "Burası mı dedenin bahçesi? Her yer diken ve çalı!", {"mood": "worried", "tag": "disappointed"}),
            (Z, "Otuz yıl bakımsız kalınca zeytinlik böyle olur. Bak, her yer delice dolmuş.", {"tag": "sadly"}),
            (Y, "Delice mi? Ağaçlar delirmiş mi?", {"mood": "wow", "tag": "confused"}),
        ]),
        steps(rn, [
            (Z, "Delice, yabani zeytindir. Bir: Yaprakları küçük, dalları dikenlidir.", {"step": 0, "point": True}),
            (Z, "İki: Meyvesi minicik olur, yağı azdır.", {"step": 1, "point": True}),
            (Z, "Üç: Ama kökü çok güçlüdür. Üzerine iyi bir çeşit aşılanırsa verimli bir ağaca dönüşür.", {"step": 2, "point": True}),
        ], [("Küçük yaprak, diken", s3.ic_wild_leaf()), ("Minik meyve", sc.ic_seed()), ("Aşıyla değerlenir", sc.ic_graft())]),
        Shot(rn, [
            (S, "Buraya gelin! Haritadaki çarpı burası!", {"tag": "excited"}),
            (Y, "Ama burada fidan yok... Sadece boş bir çukur ve üstünde bin dokuz yüz doksan altı yazan bir taş!", {"mood": "worried", "tag": "shocked", "gap": 0.6}),
        ], zeynep_x=300, zeyto_x=520, gap=0.28, actors=[sinsi_at(820, 820, 0.8)], props_top=[(fit(s3.stone_marker(), width=420), 760, 1650)]),
        END(6),
    ]
    return R(5, shots)


# ---------------------------------------------------------------- 6
def ep6():
    rn = s3.bg_ruin()
    shots = [
        Shot(rn, [
            (Z, "Çok geç kaldık... Beton Bey fidanı söküp götürmüş.", {"tag": "devastated"}),
            (Y, "Dur Abi! Bu çukur yeni değil. Üstünde yosun var, otlar bile büyümüş.", {"mood": "wow", "tag": "thoughtful"}),
            (Z, "Haklısın... Bu çukur yıllar önce kazılmış!", {"tag": "surprised"}),
        ], zeynep_x=330, zeyto_x=560, gap=0.28, props_top=[(fit(s3.stone_marker(), width=380), 820, 1660)]),
        card(rn, [
            (Y, "Taşın altında bir kâğıt var!", {"arms": True, "tag": "excited"}),
            (Z, "Dedemin yazısı! Fidanı soğuktan kaçırdım. Yerini limonla yazdım.", {"tag": "reading"}),
        ], notebook_page(["Fidanı soğuktan", "kaçırdım. Yerini", "limonla yazdım."], "— Deden, 1996")),
        steps(rn, [
            (Z, "Demek dedem fidanı taşımış. Bir: Fidan, ağaç dinlenmedeyken taşınır. Yani kışın ya da erken baharda.", {"step": 0, "point": True}),
            (Z, "İki: Kökler toprağıyla birlikte, top halinde sökülür. Üç: Dikilince hemen bol can suyu verilir.", {"step": 1, "point": True}),
        ], [("Dinlenme döneminde taşı", s3.ic_snow()), ("Kök topuyla sök", s3.ic_root_ball())]),
        Shot(rn, [
            (B, "Hah! Demek fidan burada değil. Ver o haritayı bana!", {"tag": "shouting"}),
            (Y, "Abi, Beton Bey haritayı kaptı! Kaçıyor!", {"mood": "worried", "arms": True, "tag": "panicked", "gap": 0.6}),
        ], zeynep_x=300, zeyto_x=520, gap=0.28, actors=[beton_at(800, 0.78, enter=True)]),
        END(7),
    ]
    return R(6, shots)


# ---------------------------------------------------------------- 7
def ep7():
    rn = s3.bg_ruin()
    shots = [
        Shot(rn, [
            (S, "Ben yakalarım! Vızzz! Kulağına konuyorum!", {"tag": "battle cry"}),
            (B, "Ay! Çekil şuradan sinek! Ahh, kayıyorum!", {"tag": "panicked"}),
        ], zeynep_x=None, zeyto_x=None, gap=0.28, actors=[beton_at(560, 0.8), sinsi_at(700, 700, 0.8)]),
        card(rn, [
            (S, "Harita ikiye yırtıldı! Yarısı bende, yarısı Beton'da kaldı.", {"tag": "out of breath"}),
            (Y, "Aferin Sinsi! Sen artık bizim takımdansın!", {"arms": True, "tag": "excited"}),
        ], s3.half_map()),
        steps(rn, [
            (Z, "Beton Bey kayınca bütün toprak aşağı aktı. Dağ zeytinliklerinde bu yüzden teras yapılır.", {"tag": "thoughtful"}),
            (Z, "Bir: Taş duvarlı teraslar toprağı tutar, yağmur toprağı süpürüp götüremez.", {"step": 0, "point": True}),
            (Z, "İki: Ağaç diplerindeki ot örtüsü de toprağı korur. Çıplak toprak kolay akar.", {"step": 1, "point": True}),
        ], [("Teraslar toprağı tutar", s3.ic_terrace()), ("Ot örtüsü korur", sc.ic_hoe())]),
        duo(s3.bg_mountain(True), [
            (Y, "Hava karardı... Bizim yarımızda hiçbir yazı yok ki.", {"mood": "worried", "tag": "sadly"}),
            (Z, "Dedem limonla yazdım demişti... Zeyto, ateş yakalım!", {"tag": "realizing", "gap": 0.6}),
        ], tint=None),
        END(8),
    ]
    return R(7, shots)


# ---------------------------------------------------------------- 8
def ep8():
    mn = s3.bg_mountain(True)
    fire = s3.campfire(380)
    shots = [
        card(mn, [
            (Z, "Limon suyuyla yazılan yazı görünmez. Ama ısıtınca kâğıt o yerlerde kararır.", {"tag": "whispers"}),
            (Y, "Harfler çıkıyor! Okul bahçesi, kuyunun yanı!", {"arms": True, "mood": "wow", "tag": "amazed"}),
        ], s3.half_map(reveal=True), props_top=[(fire, 540, 1720)]),
        steps(mn, [
            (Y, "Brrr... Çok soğuk. Zeytin ağaçları kışın üşümüyor mu?", {"mood": "worried", "tag": "shivering"}),
            (Z, "Biraz üşümeleri iyidir! Bir: Zeytin, çiçek açmak için kışın bir süre serinlik ister.", {"step": 0, "point": True}),
            (Z, "İki: Kışı çok ılık geçen yıllarda çiçeklenme azalabilir.", {"step": 1, "point": True}),
            (Y, "Yani biraz üşümek, bol zeytin demek!", {"arms": True, "tag": "cheerful"}),
        ], [("Kışın serinlik ister", s3.ic_chill()), ("Ilık kış, az çiçek", s3.ic_sun_hours())], props_top=[(fit(fire, width=260), 560, 1800)]),
        Shot(mn, [
            (S, "Vızzz... Kötü haber. Beton'u telefonda konuşurken duydum.", {"tag": "whispers"}),
            (S, "Okul arazisini satın almış! Yarın oraya kepçe gönderiyor!", {"tag": "urgent", "gap": 0.6}),
        ], zeynep_x=300, zeyto_x=520, gap=0.28, actors=[sinsi_at(820, 820, 0.8)], props_top=[(fit(fire, width=260), 760, 1780)]),
        END(9),
    ]
    return R(8, shots)


# ---------------------------------------------------------------- 9
def ep9():
    sch = s3.bg_school()
    shots = [
        duo(sch, [
            (Y, "Eski okul! Kuyunun yanında kocaman bir zeytin ağacı var!", {"arms": True, "mood": "wow", "tag": "excited"}),
            (Z, "Bu... bu kayıp fidan! Otuz yılda koca bir ağaç olmuş!", {"tag": "amazed"}),
            (Y, "Merhaba kardeşim! Seni çok aradık!", {"arms": True, "tag": "happy"}),
        ], zeynep_x=700, zeyto_x=900, pan=False),
        steps(sch, [
            (Y, "Peki fidan kaç yılda ağaç olur?", {"tag": "curious"}),
            (Z, "Bir: Aşılı ya da çelikten bir fidan genelde üç ile beş yılda ilk meyvesini verir.", {"step": 0, "point": True}),
            (Z, "İki: Tam verime ulaşması on yılı bulur. Üç: Ve iyi bakılırsa yüzlerce yıl yaşar.", {"step": 1, "point": True}),
        ], [("3-5 yılda ilk meyve", s3.ic_years()), ("Yüzlerce yıl ömür", sc.ic_big_text("100+", "yıl"))]),
        duo(sch, [
            (Y, "Abi... Bu gürültü ne?", {"mood": "worried", "tag": "scared"}),
            (Z, "Kepçe sesi. Beton Bey geliyor!", {"tag": "alarmed", "gap": 0.6}),
        ], zeynep_x=700, zeyto_x=900, pan=False),
        END(10),
    ]
    return R(9, shots)


# ---------------------------------------------------------------- 10
def ep10():
    sch = s3.bg_school()
    exc = fit(sc.excavator(), width=600)
    shots = [
        Shot(sch, [
            (B, "Çekil kenara mühendis! Bu ağacı söküp satacağım. Dünyada tek bir çeşit, kim bilir kaç para eder!", {"tag": "greedy"}),
            (Z, "Bu ağaç bir yere gitmiyor Beton Bey.", {"tag": "firmly"}),
        ], zeynep_x=560, zeyto_x=760, gap=0.28, pan=False, props=[(exc, 900, 1500)], actors=[beton_at(1000, 0.7, look=-1)]),
        summary(sch, (Z, "Zeytin ağacı keyfe göre sökülüp taşınamaz. Kanun bunu izne bağlar.", {"point": True}),
                "ZEYTİN AĞACI KORUNUR", ["Kesmek ve sökmek izne tabidir", "İzinsiz söküme ceza vardır", "Önce resmî izin, sonra iş"]),
        card(sch, [
            (B, "İzin mi? İşte izin kâğıdım! Hah!", {"tag": "smugly"}),
            (Y, "Abi... Kâğıdın altına bak! İmza yeri boş!", {"mood": "wow", "tag": "surprised", "gap": 0.6}),
        ], s3.permit()),
        END(11),
    ]
    return R(10, shots)


# ---------------------------------------------------------------- 11
def ep11():
    sch = s3.bg_school()
    exc = fit(sc.excavator(), width=600)
    shots = [
        Shot(sch, [
            (Z, "Bu izin imzasız. Geçersiz bir kâğıtla tek dal koparamazsınız.", {"tag": "calmly"}),
            (B, "Bir günde imzalatırım! Yarın akşam bu ağaç burada olmayacak!", {"tag": "angry"}),
            (Y, "Abi, bir günde ne yapabiliriz?", {"mood": "worried", "tag": "worried"}),
        ], zeynep_x=560, zeyto_x=760, gap=0.28, pan=False, props=[(exc, 900, 1500)], actors=[beton_at(1000, 0.7, look=-1)]),
        steps(sch, [
            (Z, "Kanıtlayacağız. Bu ağacın, Ulu'nun yavrusu ve başka yerde olmayan bir çeşit olduğunu.", {"tag": "determined"}),
            (Z, "Bir: Zeytin çeşitleri yaprağa, meyveye ve çekirdeğin şekline bakılarak ayırt edilir.", {"step": 0, "point": True}),
            (Z, "İki: En kesin sonuç DNA analiziyle alınır. İki ağacın yaprağı karşılaştırılır.", {"step": 1, "point": True}),
        ], [("Yaprak, meyve, çekirdek", s3.ic_silver_leaf()), ("DNA analizi", s3.ic_dna())]),
        duo(bg_mill(), [
            (Z, "Yaprakları laboratuvara bıraktım. Ama sonuç üç gün sürecekmiş.", {"tag": "worried"}),
            (Y, "Üç gün mü? Beton Bey yarın gelecek! Bu gece ağacın başında nöbet tutacağız!", {"arms": True, "tag": "determined", "gap": 0.6}),
        ]),
        END(12),
    ]
    return R(11, shots)


# ---------------------------------------------------------------- 12
def ep12():
    sch = s3.bg_school(True)
    shots = [
        Shot(sch, [
            (Y, "Nöbetteyiz! Gözlerim açık... Çok açık... Hıh, uyumadım!", {"tag": "sleepy"}),
            (S, "Ben gece de görürüm, siz dinlenin. Vızzz.", {"tag": "softly"}),
            (Z, "Sağ ol Sinsi. Bu gece çok soğuk. Termosumdaki çay bile soğudu.", {"tag": "shivering"}),
        ], zeynep_x=700, zeyto_x=900, pan=False, gap=0.28, tint=NIGHT, actors=[sinsi_at(560, 760, 0.7)]),
        steps(sch, [
            (Y, "Mutfaktaki zeytinyağı da soğukta donmuş! Bozuldu mu?", {"mood": "worried", "tag": "worried"}),
            (Z, "Hayır! Bir: Zeytinyağı soğukta bulanıklaşır, buzdolabında katılaşabilir.", {"step": 0, "point": True}),
            (Z, "İki: Oda sıcaklığında yavaşça eski haline döner. Tadı, kalitesi bozulmaz.", {"step": 1, "point": True}),
        ], [("Soğukta donar", s3.ic_snow()), ("Oda sıcaklığında çözülür", s3.ic_cloudy())], tint=NIGHT),
        Shot(sch, [
            (S, "Şşşt! Biri geliyor! Elinde fener ve testere var!", {"tag": "whispers"}),
            (Z, "Beton Bey sabahı beklemedi... Hemen kalk Zeyto!", {"tag": "urgent", "gap": 0.6}),
        ], zeynep_x=700, zeyto_x=900, pan=False, gap=0.28, tint=NIGHT, actors=[sinsi_at(560, 760, 0.7)],
            props_top=[(glow(220), 140, 1350)]),
        END(13),
    ]
    return R(12, shots)


# ---------------------------------------------------------------- 13
def ep13():
    sch = s3.bg_school(True)
    shots = [
        Shot(sch, [
            (S, "Vızzz! Vızzz! Geri çekil!", {"tag": "battle cry"}),
            (B, "Yine mi bu sinek! Tamam, tamam, gidiyorum!", {"tag": "panicked"}),
        ], zeynep_x=None, zeyto_x=None, gap=0.28, pan=False, tint=NIGHT, actors=[beton_at(700, 0.72), sinsi_at(820, 700, 0.75)]),
        card(sch, [
            (Y, "Abi, Beton'un feneri gövdeyi aydınlattı. Kabukta bir yazı var!", {"mood": "wow", "tag": "whispers"}),
            (Z, "Torunum için. Ve bir ok... Aşağıyı, kökü gösteriyor.", {"tag": "emotional"}),
        ], notebook_page(["Torunum için.", "Köke bak."], "— Deden"), tint=NIGHT),
        steps(sch, [
            (Z, "Kökün yanında bir kavanoz! İçinde dedemin aşı notları var.", {"tag": "excited"}),
            (Z, "Bir: Aşı, iki bitkiyi birleştirmektir. Alttaki kök anaçtır, üste takılan dal kalemdir.", {"step": 0, "point": True}),
            (Z, "İki: Zeytinde aşı en çok ilkbaharda, özsu yürüdüğünde yapılır. Kabuk kolay kalkar.", {"step": 1, "point": True}),
            (Y, "Ağaçlar da organ nakli yapıyor yani!", {"arms": True, "tag": "giggles"}),
        ], [("Anaç + kalem", s3.ic_graft_cut()), ("İlkbaharda aşı", s3.ic_sun_hours())]),
        duo(sch, [
            (Z, "Telefon! Laboratuvar arıyor... Sonuç erken çıkmış!", {"tag": "surprised"}),
            (Y, "Ne diyorlar? Ne diyorlar?!", {"arms": True, "tag": "impatient", "gap": 0.6}),
        ], zeynep_x=700, zeyto_x=900, pan=False, tint=NIGHT),
        END(14),
    ]
    return R(13, shots)


# ---------------------------------------------------------------- 14
def ep14():
    lab = sc.bg_lab()
    shots = [
        card(lab, [
            (Z, "Okul ağacı ile Ulu yüzde yüz eşleşiyor. Ve kayıtlı hiçbir çeşide benzemiyor!", {"tag": "amazed"}),
            (Y, "Kardeşim gerçekten Ulu'nun yavrusuymuş!", {"arms": True, "tag": "joyful"}),
        ], s3.lab_result()),
        summary(lab, (Z, "Yerel çeşitler çok değerlidir. Kaybolurlarsa bir daha geri gelmezler.", {"point": True}),
                "YEREL ÇEŞİT NEDEN ÖNEMLİ?", ["Yüzlerce yılda iklime uyum sağlamıştır", "Hastalığa dayanıklı genler taşır", "Kendine has tadı ve aroması vardır"]),
        duo(bg_sunset(), [
            (Z, "Muhtar Amca'ya haber verdim. Ağacı korumak için köy toplantısı yapacağız.", {"tag": "hopeful"}),
            (B, "Toplantı mı? Ben de geleceğim! Elimde bir sürprizim var!", {"tag": "smugly", "gap": 0.6}),
        ], actors=[beton_at(1000, 0.66, look=-1)]),
        END(15),
    ]
    return R(14, shots)


# ---------------------------------------------------------------- 15
def ep15():
    sq = sc.bg_square()
    shots = [
        Shot(sq, [
            (M, "Köylüler! Okul bahçesindeki zeytin, Ulu'nun yavrusu çıktı. Dünyada bir tane!", {"tag": "proudly"}),
            (B, "Çok güzel. Ama bu yağın litresi neden bu kadar pahalı, onu da konuşalım!", {"tag": "mockingly"}),
        ], zeynep_x=830, zeynep_scale=0.72, zeyto_x=620, gap=0.28, actors=[muhtar_at(210, 0.78), beton_at(470, 0.78)]),
        steps(sq, [
            (Z, "Hemen anlatayım. Bir: Bir litre zeytinyağı için beş ile yedi kilo zeytin gerekir.", {"step": 0, "point": True}),
            (Z, "İki: Hasat çoğunlukla elle yapılır, çok emek ister. Üç: Erken hasatta verim daha da düşer.", {"step": 1, "point": True}),
            (Y, "Yani her şişede kocaman bir sepet zeytin var!", {"arms": True, "tag": "excited"}),
        ], [("1 litre = 5-7 kg zeytin", sc.ic_big_text("5-7", "kg zeytin")), ("Emek ve zaman", ic_collect())]),
        Shot(sq, [
            (B, "Neyse... Asıl sürprizim şu: Okul arazisinin tapusu artık benim!", {"tag": "triumphant"}),
            (M, "Ne? Okul arazisi satılamaz ki! Bir yanlışlık olmalı.", {"tag": "shocked", "gap": 0.6}),
        ], zeynep_x=830, zeynep_scale=0.72, zeyto_x=620, gap=0.28, actors=[muhtar_at(210, 0.78), beton_at(470, 0.78)]),
        END(16),
    ]
    return R(15, shots)


# ---------------------------------------------------------------- 16
def ep16():
    sch = s3.bg_school()
    box = fit(s3.safe_box(), width=300)
    shots = [
        duo(sch, [
            (M, "Evlat, deden bu araziyi okula bağışlamıştı. Bir senet yazdırmıştı ama kimse bulamadı.", {"tag": "thoughtful"}),
            (Y, "Okulun içinde eski bir kasa var! Ama kilitli.", {"arms": True, "tag": "excited"}),
        ], actors=[muhtar_at(200, 0.74)], zeynep_x=560, zeyto_x=770, pan=False, props_top=[(box, 970, 1690)]),
        duo(sch, [
            (Z, "Kilitli mi? Geçen sezon teneke kutudan çıkan anahtar hâlâ cebimde!", {"tag": "excited"}),
            (Y, "Dön... Dön... Klik! Açıldı!", {"arms": True, "mood": "wow", "tag": "thrilled"}),
        ], zeynep_x=560, zeyto_x=770, pan=False, props_top=[(box, 970, 1690)]),
        card(sch, [
            (Z, "Bağış senedi! Bu arazi okul içindir. Zeytin ağacı asla kesilemez.", {"tag": "reading"}),
            (Y, "Beton Bey'in tapusu boşa çıktı!", {"arms": True, "tag": "cheering"}),
        ], notebook_page(["BAĞIŞ SENEDİ", "Bu arazi okul içindir.", "Zeytin kesilemez."], "— Deden, 1997")),
        Shot(sch, [
            (B, "O kâğıdı ver bana! Vızıltılı arkadaşın yok, kimse kurtaramaz seni!", {"tag": "shouting"}),
            (Y, "Senedi kaptı! Sinsi neredesin?!", {"mood": "worried", "tag": "panicked", "gap": 0.6}),
        ], zeynep_x=420, zeyto_x=640, pan=False, gap=0.28, actors=[beton_at(880, 0.74, enter=True)]),
        END(17),
    ]
    return R(16, shots)


# ---------------------------------------------------------------- 17
def ep17():
    sch = s3.bg_school()
    shots = [
        Shot(sch, [
            (B, "Sinsi! Senedi al ve benimle gel. Sana sıcacık bir kış evi yaparım, söz!", {"tag": "persuasive"}),
            (S, "Kış evi... Hep istediğim şey...", {"tag": "hesitant"}),
            (Y, "Sinsi, lütfen... Sen bizim arkadaşımızsın.", {"mood": "worried", "tag": "pleading"}),
        ], zeynep_x=None, zeyto_x=300, gap=0.28, pan=False, actors=[beton_at(800, 0.74), sinsi_at(560, 700, 0.85)]),
        Shot(sch, [
            (S, "Hayır Beton Bey. Yalanla yapılan ev, sıcak olmaz. Senet Muhtar'ın!", {"tag": "determined"}),
            (M, "Aldım! Bu senet köyün malıdır artık. Okul da ağaç da güvende.", {"tag": "firmly"}),
        ], zeynep_x=None, zeyto_x=None, gap=0.28, pan=False, actors=[muhtar_at(260, 0.78), sinsi_at(560, 720, 0.85), beton_at(860, 0.74)]),
        steps(sch, [
            (Z, "Sinsi, sana bir ev sözü de ben veriyorum. Ama zeytinliğe zarar vermeden.", {"tag": "warmly"}),
            (Z, "Çünkü bahçede bir denge vardır. Bir: Uğur böceği, kuşlar ve yarasalar zararlıları doğal yoldan azaltır.", {"step": 0, "point": True}),
            (Z, "İki: Gereksiz ilaç bu dostları da öldürür. Üç: Çiçekli kenarlar onlara yuva olur.", {"step": 1, "point": True}),
        ], [("Doğal dostlar", s3.ic_ladybug()), ("Gereksiz ilaç yok", s3.ic_drop(bad=True))]),
        duo(sch, [
            (Y, "Beton Bey oturdu kaldı. Ağlıyor mu o?", {"mood": "wow", "tag": "surprised"}),
            (Z, "Galiba bu işin altında başka bir hikâye var.", {"tag": "thoughtful", "gap": 0.6}),
        ], zeynep_x=640, zeyto_x=880, pan=False, actors=[beton_at(250, 0.72, look=1)]),
        END(18),
    ]
    return R(17, shots)


# ---------------------------------------------------------------- 18
def ep18():
    sch = s3.bg_school()
    shots = [
        Shot(sch, [
            (B, "Ben de bu okulda okudum. Bu ağacın gölgesinde oynardım.", {"tag": "sadly"}),
            (B, "Sonra köyden gittim, hep para peşinde koştum. Para olunca herkes saygı duyar sandım.", {"tag": "regretful"}),
            (Y, "Beton Bey de çocukmuş bir zamanlar...", {"mood": "worried", "tag": "softly"}),
        ], zeynep_x=640, zeyto_x=880, pan=False, gap=0.3, actors=[beton_at(250, 0.74, look=1)]),
        Shot(sch, [
            (Z, "Hâlâ geç değil Beton Bey. Bu ağaçtan yüzlerce fidan üretebiliriz. Bize yardım eder misiniz?", {"tag": "warmly"}),
            (B, "Ben mi? Ben... Kepçe yerine kürek tutmayı öğrenirim herhalde.", {"tag": "touched"}),
        ], zeynep_x=640, zeyto_x=880, pan=False, gap=0.3, actors=[beton_at(250, 0.74, look=1)]),
        summary(sch, (Z, "Bir zeytinlik, birlikte bakılınca yaşar. Kooperatif de böyle kurulur.", {"point": True}),
                "BİRLİKTE ÜRETMEK", ["Ekipman ve sıkım ortak", "Bilgi paylaşılır", "Ürün değerinde satılır"]),
        duo(sch, [
            (Y, "Abi! Ağacın yaprakları... Bazıları sararmış!", {"mood": "worried", "tag": "alarmed"}),
            (Z, "Bunu dün fark etmemiştim. Hemen bakmam lazım.", {"tag": "concerned", "gap": 0.6}),
        ], zeynep_x=640, zeyto_x=880, pan=False),
        END(19),
    ]
    return R(18, shots)


# ---------------------------------------------------------------- 19
def ep19():
    sch = s3.bg_school()
    clear = bg_clearing(False)
    shots = [
        steps(sch, [
            (Z, "Yaprak sararmasının birkaç nedeni olur. Bir: Kökte su birikmesi. Bu kuyu dibinde toprak çok ıslak.", {"step": 0, "point": True}),
            (Z, "İki: Besin eksikliği. En sık azot eksikliğidir. Toprak analizi yaptırılır.", {"step": 1, "point": True}),
            (Z, "Üç: Lekeli yapraklar varsa halkalı leke hastalığı olabilir. Bakırlı ilaçla korunur.", {"step": 2, "point": True}),
        ], [("Su birikmesi", s3.ic_roots_water()), ("Besin eksikliği", sc.ic_flask("N")), ("Halkalı leke", s3.ic_silver_leaf())]),
        duo(sch, [
            (Z, "Kuyudan sızan su köklere doluyor. Bir su yolu açıp toprağı havalandıracağız.", {"tag": "determined"}),
            (Y, "Kardeşim iyileşecek mi?", {"mood": "worried", "tag": "worried"}),
            (Z, "İyileşecek. Zeytin dayanıklı bir ağaçtır.", {"tag": "reassuring"}),
        ], zeynep_x=640, zeyto_x=880, pan=False),
        with_ulu(clear, [
            (U, "Yavrumu bir kez görebilsem... Ama ağaçlar yürüyemez.", {"tag": "sadly"}),
            (Y, "Biz getiririz Ulu! Onun bir dalını, buraya, senin yanına!", {"arms": True, "tag": "excited", "gap": 0.6}),
        ]),
        end_shot("Yarın 20:00 · Sezon Finali", TITLES[20], GREEN_OLIVE, cta="Takip et, finali kaçırma!"),
    ]
    return R(19, shots)


# ---------------------------------------------------------------- 20
def ep20():
    clear = bg_clearing(False)
    sun = bg_sunset()
    shots = [
        steps(sun, [
            (Z, "Okul ağacından çelikler aldık. Bir: Genç ve sağlıklı dallardan yaklaşık on beş santimlik parçalar kesilir.", {"step": 0, "point": True}),
            (Z, "İki: Alt yaprakları temizlenir, köklenme hormonuna batırılır. Üç: Sisli, nemli bir ortamda kök salar.", {"step": 1, "point": True}),
            (B, "Saksıları ben taşırım! Kürek de bende!", {"tag": "cheerfully"}),
        ], [("15 cm çelik", sc.ic_cutting()), ("Nemli ortamda köklen", s3.ic_cutting_pot())], actors=[beton_at(1000, 0.6, look=-1)]),
        with_ulu(clear, [
            (Z, "Ulu, işte yavrunun ilk fidanı. Senin hemen yanına dikiyoruz.", {"tag": "emotional"}),
            (U, "Otuz yıl bekledim... Yaprakları tıpkı benimkiler gibi. Hoş geldin yavrum.", {"tag": "crying"}),
            (Y, "Ben de dibine düşeceğim. Belki bir gün ben de böyle bir fidan olurum!", {"arms": True, "tag": "hopeful"}),
        ], props_top=[(fit(s3.pot_row(1), width=520), 620, 1760)]),
        summary(sun, (Z, "Yeni sezon zeytinyağımız hâlâ hazır. Sipariş için DM'den yazmanız yeterli!", {"point": True, "tag": "cheerfully"}),
                "MÜHENDİSİN DEFTERİ", ["Natürel sızma, yeni hasat", "Doğrudan üreticiden", "Sipariş: DM"]),
        duo(sun, [
            (Y, "Sezon bitti mi şimdi? Ben daha yeni ısındım!", {"mood": "worried", "tag": "whining"}),
            (Z, "Sezon 3 yakında Zeyto. Siz de yorumlara yazın: Sezon 3'te ne olsun?", {"wave": True, "tag": "cheerfully", "gap": 0.7}),
        ]),
        end_shot("Sezon 3 yakında", "Yorumlara fikrini yaz!", GREEN_OLIVE, cta="Takip et, kaçırma!"),
    ]
    return R(20, shots)


if __name__ == "__main__":
    for w in sys.argv[1:]:
        print(globals()["ep" + w]())
