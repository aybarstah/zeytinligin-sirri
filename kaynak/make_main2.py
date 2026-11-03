"""Zeytinliğin Sırrı — Season 1, episodes 6-20."""
import sys
from PIL import Image, ImageDraw
from brand import *
from story import Shot, render_episode, bg_orchard, bg_mill
from make_main import bg_sunset, bg_clearing, end_shot, notebook_page, ic_yellow_trap, ic_bottle_trap, ic_collect, ic_copper, \
    ic_dry_branch, ic_open_canopy, OUT
from make_story import ic_wash, ic_crush, ic_malax, ic_centrifuge
from make_story2 import ic_no_sun, ic_thermo, ic_cap, ic_containers, ic_throat, bg_kitchen
import scenes2 as sc

Z, Y, U, S, B, M = "zeynep", "zeyto", "ulu", "sinsi", "beton", "muhtar"
NIGHT = ((30, 40, 90), 0.22)


def ulu(eyes=1.0, wake=None):
    return {"kind": "ulu", "x": 280, "feet": 1900, "scale": 0.95, "wake": wake, "eyes": eyes}


def with_ulu(bg, lines, **kw):
    kw.setdefault("zeynep_x", 830)
    kw.setdefault("zeyto_x", 610)
    kw.setdefault("zeynep_scale", 0.66)
    kw.setdefault("pan", False)
    kw.setdefault("gap", 0.28)
    acts = kw.pop("actors", None) or [ulu()]
    return Shot(bg, lines, actors=acts, **kw)


def duo(bg, lines, **kw):
    kw.setdefault("zeynep_x", 330)
    kw.setdefault("zeyto_x", 790)
    kw.setdefault("gap", 0.28)
    return Shot(bg, lines, **kw)


def steps(bg, lines, items, **kw):
    kw.setdefault("zeynep_x", 270)
    kw.setdefault("zeyto_x", 840)
    kw.setdefault("gap", 0.28)
    return Shot(bg, lines, steps=items, **kw)


def summary(bg, line, title, items, **kw):
    kw.setdefault("zeynep_x", 270)
    kw.setdefault("zeyto_x", 840)
    kw.setdefault("gap", 0.4)
    return Shot(bg, [line], summary=(title, items), **kw)


def card(bg, lines, img, **kw):
    kw.setdefault("zeynep_x", 360)
    kw.setdefault("zeyto_x", 800)
    kw.setdefault("gap", 0.3)
    return Shot(bg, lines, card=img, **kw)


def END(n, when, title):
    return end_shot(f"Bölüm {n} {when}", title, GREEN_OLIVE, cta="Takip et, hikâyeyi kaçırma!")


def glow(size=360):
    g = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    c = size / 2
    for r, a in [(c * 0.95, 40), (c * 0.66, 80), (c * 0.4, 160), (c * 0.17, 255)]:
        gd.ellipse([c - r, c - r, c + r, c + r], fill=(255, 230, 140, a))
    return g


HOLLOW_GLOW = (394, 1630)   # Ulu's hollow on screen with ulu() placement


# ---------------------------------------------------------------- 6
def ep6():
    night = bg_clearing(True)
    day = bg_orchard(("p",))
    box = fit(sc.tin_box(), width=420)
    shots = [
        with_ulu(night, [
            (Z, "Tam burası. Ulu'nun en eski kökü... Kazıyorum!", {"tag": "whispers"}),
            (Y, "Hızlı ol Mühendis Abi, karanlıktan korkuyorum!", {"mood": "worried", "tag": "scared"}),
            (Z, "Bir şeye çarptı! Teneke bir kutu bu!", {"tag": "excited"}),
            (Y, "Aç, aç! Kayıp sayfa içindedir!", {"arms": True, "tag": "excited"}),
        ], tint=NIGHT, props_top=[(box, 600, 1760)]),
        card(night, [
            (Z, "Sayfa yok... Sadece bir zeytin çekirdeği ve kısa bir not.", {"tag": "disappointed"}),
            (Z, "Asıl hazine, sabırla büyür.", {"tag": "softly"}),
            (Y, "Bir çekirdek mi? Ondan ağaç mı çıkacak?", {"mood": "wow"}),
        ], notebook_page(["Asıl hazine,", "sabırla büyür."], "— Deden"), tint=NIGHT),
        steps(day, [
            (Z, "Çıkar ama kolay değil. Bir: Çekirdekten çıkan zeytin yabani olur, meyve vermesi de yıllar sürer.", {"step": 0, "point": True}),
            (Z, "İki: Bu yüzden zeytin çoğunlukla çelikle çoğaltılır. Genç dallar köklendirilip fidan yapılır.", {"step": 1, "point": True}),
            (Y, "Ben de bir dal parçasından mı geldim?", {"mood": "wow", "tag": "curious"}),
            (Z, "Üç: Ya da yabani bir anaca, istenen çeşit aşılanır. Dedem de böyle yapardı.", {"step": 2, "point": True}),
        ], [("Çekirdek: yavaş ve yabani", sc.ic_seed()), ("Çelikle çoğaltma", sc.ic_cutting()), ("Aşıyla çoğaltma", sc.ic_graft())]),
        card(day, [
            (Z, "Dedemin defterinde hâlâ boş sayfalar var. Ben de yazmaya başlıyorum.", {"tag": "determined"}),
            (Y, "Kapağa ne yazdın? Mühendisin Defteri! Artık senin defterin oldu!", {"arms": True, "tag": "excited"}),
        ], sc.notebook_cover()),
        duo(night, [
            (Y, "Mühendis Abi... Kutunun dibinde bir şey parlıyor.", {"mood": "wow", "tag": "whispers"}),
            (Z, "Bu eski bir anahtar! Ama neyin anahtarı?", {"tag": "surprised", "gap": 0.6}),
        ], tint=NIGHT, props_top=[(fit(sc.tin_box(), width=300), 560, 1780)]),
        END(7, "bu akşam 20:00", "İlk Yağ"),
    ]
    return render_episode(shots, "BÖLÜM 6", OUT + "S1B6_gece_kazisi.mp4")


# ---------------------------------------------------------------- 7
def ep7():
    mill = bg_mill()
    shots = [
        duo(mill, [
            (Y, "Burası fabrika! Kardeşlerim yağ olacak!", {"arms": True, "tag": "excited"}),
            (Z, "Zeytinlerimizi topladığımız gün getirdik. İlk yağımız bugün çıkıyor.", {"tag": "proudly"}),
        ], zeyto_color=BLACKOLIVE),
        steps(mill, [
            (Z, "Bir: Yapraklar ayrılır, zeytinler yıkanır.", {"step": 0, "point": True}),
            (Z, "İki: Zeytin, çekirdeğiyle birlikte kırılıp hamur olur.", {"step": 1, "point": True}),
            (Z, "Üç: Hamur yavaşça yoğrulur. Isı yirmi yedi derecenin altında kalırsa buna soğuk sıkım denir.", {"step": 2, "point": True}),
            (Y, "Serin serin, mis gibi!", {"arms": True, "tag": "giggles"}),
            (Z, "Dört: Santrifüj, yağı sudan ve posadan ayırır. İşte ilk yağımız!", {"step": 3, "point": True}),
        ], [("Yıkama", ic_wash()), ("Kırma", ic_crush()), ("Soğuk yoğurma", ic_malax()), ("Ayrıştırma", ic_centrifuge())], zeyto_color=BLACKOLIVE),
        Shot(mill, [
            (B, "Vay vay, yeni mühendisimiz yağ mı sıkıyor? Herkese söyleyeyim, bu yağ bozuk!", {"tag": "mockingly"}),
            (Z, "Ne diyorsunuz? Yağımız tertemiz!", {"tag": "angry"}),
            (B, "Yaşlı ağaçtan iyi yağ çıkmaz. Köyde kimse bunu almaz, görürsünüz.", {"tag": "smugly"}),
        ], zeynep_x=300, gap=0.28, actors=[{"kind": "beton", "x": 790, "scale": 0.84, "enter": True, "appear": 0.0}]),
        duo(bg_orchard(("p",)), [
            (Y, "Mühendis Abi, kötü haber! Köyde kimse yağımızı almak istemiyor!", {"mood": "worried", "tag": "upset"}),
            (Z, "Beton Bey dedikoduyu yaymış. Ama kanıtlayacağız. Bu yağı laboratuvara götürüyorum.", {"tag": "determined", "gap": 0.6}),
        ], zeyto_color=BLACKOLIVE),
        END(8, "yarın 13:00", "Asitlik Testi"),
    ]
    return render_episode(shots, "BÖLÜM 7", OUT + "S1B7_ilk_yag.mp4")


# ---------------------------------------------------------------- 8
def ep8():
    lab = sc.bg_lab()
    shots = [
        duo(lab, [
            (Y, "Burası çok beyaz! Her şey cam! Dokunmuyorum, söz!", {"arms": True, "mood": "wow", "tag": "excited"}),
            (Z, "Laboratuvardayız. Yağımızın kalitesini sayılar söyleyecek.", {}),
        ]),
        steps(lab, [
            (Z, "Bir: En önemli ölçüm serbest asitlik. Yağ ne kadar tazeyse, asitlik o kadar düşüktür.", {"step": 0, "point": True}),
            (Z, "İki: Natürel sızma sayılması için asitlik en fazla yüzde sıfır virgül sekiz olmalı.", {"step": 1, "point": True}),
            (Y, "Peki asitliği ne yükseltir?", {"mood": "wow"}),
            (Z, "Üç: Bekletilen, çuvalda ezilen ya da kurtlu zeytin. Yani dedemin kurallarının hepsi bu yüzden!", {"step": 2, "point": True}),
        ], [("Serbest asitlik", sc.ic_flask()), ("Sınır: %0,8", sc.ic_big_text("%0,8", "natürel sızma")), ("Asitliği yükseltenler", sc.ic_sack_bad())]),
        card(lab, [
            (Z, "Sonuç geldi! Asitlik yüzde sıfır virgül üç. Natürel sızma!", {"tag": "excited"}),
            (Y, "Yaşasın! Beton Bey'e göstereceğiz!", {"arms": True, "tag": "cheering"}),
        ], sc.report()),
        Shot(lab, [
            (Z, "Raporu masaya koymuştum... Nerede bu?", {"tag": "confused"}),
            (S, "Vızzz... Bunu mu arıyordun? Beton Bey buna bayılacak!", {"tag": "mischievously"}),
            (Y, "Sinsi! Tuzaktan kaçmış!", {"mood": "worried", "tag": "shocked", "gap": 0.6}),
        ], zeynep_x=330, zeyto_x=790, gap=0.28, actors=[{"kind": "sinsi", "x": 760, "y": 760, "scale": 0.9, "appear": 2.0}]),
        END(9, "bu akşam 20:00", "Sinsi Kaçtı"),
    ]
    return render_episode(shots, "BÖLÜM 8", OUT + "S1B8_asitlik_testi.mp4")


# ---------------------------------------------------------------- 9
def ep9():
    clear = bg_clearing(False)
    day = bg_orchard(("p",))
    trap = fit(ic_yellow_trap(0), width=300)
    shots = [
        with_ulu(clear, [
            (Y, "Tuzak bomboş! Sinsi nasıl kaçmış?", {"mood": "worried", "tag": "upset"}),
            (U, "Tuzak eskimiş evlat. Yapışkanı tozla kaplanmış, artık tutmuyor.", {"tag": "calmly"}),
            (Z, "Demek ki tuzak kurmak yetmiyor, bakımını da yapmak lazım.", {}),
        ], props=[(trap, 760, 860)]),
        steps(day, [
            (Z, "Bir: Sarı tuzaklar dolunca ya da tozlanınca yenisiyle değiştirilir.", {"step": 0, "point": True}),
            (Z, "İki: Şişe tuzakların yemi düzenli olarak tazelenir.", {"step": 1, "point": True}),
            (Z, "Üç: Tuzaklar ağacın gölgeli tarafına, göz hizasına asılır ve her hafta kontrol edilir.", {"step": 2, "point": True}),
            (Y, "Bu sefer Sinsi kaçamaz!", {"arms": True, "tag": "determined"}),
        ], [("Değiştir", ic_yellow_trap(6)), ("Yemi tazele", ic_bottle_trap()), ("Doğru yere as", sc.ic_tree_trap())]),
        Shot(sc.bg_coffee(), [
            (B, "Bakın arkadaşlar! Mühendisin yağı bozuk, ben söylemiştim!", {"tag": "loudly"}),
            (B, "Laboratuvar raporu falan yok. Olsa gösterirdi, değil mi?", {"tag": "smugly"}),
        ], gap=0.3, actors=[{"kind": "beton", "x": 560, "scale": 0.84}]),
        duo(day, [
            (Y, "Duydun mu? Kahvede herkese yalan söylüyor!", {"mood": "worried", "tag": "angry"}),
            (Z, "O zaman yarın kahveye gidiyoruz. Yağımızı herkes kendi tatsın.", {"tag": "determined", "gap": 0.6}),
        ]),
        END(10, "yarın 13:00", "Köy Kahvesi"),
    ]
    return render_episode(shots, "BÖLÜM 9", OUT + "S1B9_sinsi_kacti.mp4")


# ---------------------------------------------------------------- 10
def ep10():
    cafe = sc.bg_coffee()
    shots = [
        Shot(cafe, [
            (M, "Hoş geldin evlat. Deden bu masada çay içerdi, Allah rahmet eylesin.", {"tag": "warmly"}),
            (Z, "Sağ olun Muhtar Amca. Bugün herkese yağımızı tattırmaya geldim.", {}),
            (B, "Bozuk yağı mı? Kimse içmez onu!", {"tag": "mockingly"}),
            (M, "Bırak tadına bakalım Beton. Karar ağzın.", {"tag": "firmly"}),
        ], zeynep_x=830, zeynep_scale=0.72, gap=0.28,
            actors=[{"kind": "muhtar", "x": 210, "scale": 0.78, "look": 1}, {"kind": "beton", "x": 520, "scale": 0.78}]),
        steps(cafe, [
            (Z, "Bir: Yağı küçük bir bardağa koyun, avucunuzla ısıtın ve koklayın. Taze çimen kokusu gelmeli.", {"step": 0, "point": True}),
            (Z, "İki: Küçük bir yudum alın, havayla birlikte ağzınızda gezdirin.", {"step": 1, "point": True}),
            (Y, "Sssp! Ayıp olmuyor mu?", {"arms": True, "tag": "giggles"}),
            (Z, "Üç: Boğazınızda hafif bir yakma hissedeceksiniz. Bu, taze yağdaki polifenollerin işareti.", {"step": 2, "point": True}),
        ], [("Kokla", sc.ic_smell()), ("Yudumla", sc.ic_sip()), ("Boğazda yakma", ic_throat())]),
        Shot(cafe, [
            (M, "Maşallah! Bu yağ tıpkı dedenin yağı gibi. Tertemiz!", {"tag": "impressed"}),
            (B, "Hıh. Neyse... Asıl mesele başka.", {"tag": "annoyed"}),
            (M, "Evlat, bir sorun daha var. Arazinin tapusu tartışmalı. Beton Bey belge getirmiş.", {"tag": "worried"}),
            (Z, "Ne belgesi? Dedem bunu hiç anlatmadı...", {"tag": "shocked", "gap": 0.6}),
        ], zeynep_x=830, zeynep_scale=0.72, gap=0.28,
            actors=[{"kind": "muhtar", "x": 210, "scale": 0.78, "look": 1}, {"kind": "beton", "x": 520, "scale": 0.78}]),
        END(11, "bu akşam 20:00", "Anahtar"),
    ]
    return render_episode(shots, "BÖLÜM 10", OUT + "S1B10_koy_kahvesi.mp4")


# ---------------------------------------------------------------- 11
def ep11():
    day = bg_orchard(("p",))
    depot = sc.bg_depot()
    shots = [
        duo(day, [
            (Z, "Dedemin anahtarı... Bahçenin arkasındaki eski depoyu açıyor olmalı.", {"tag": "curious"}),
            (Y, "Depo mu? Orada hayalet var derler!", {"mood": "worried", "tag": "scared"}),
            (Z, "Hayalet yok Zeyto, sadece toz var. Hadi gel.", {"tag": "laughs"}),
        ]),
        duo(depot, [
            (Y, "Vay! Raflarda bir sürü eski şişe ve teneke var!", {"arms": True, "mood": "wow", "tag": "amazed"}),
            (Z, "Dedem yağını burada saklarmış. Bak, her şeyi kurallarına göre yapmış.", {}),
        ]),
        steps(depot, [
            (Z, "Bir: Işık yağı bozar. O yüzden pencere yok, şişeler koyu renkli.", {"step": 0, "point": True}),
            (Z, "İki: Burası hep serin. Yağ için en iyisi on dört ile on sekiz derece arası.", {"step": 1, "point": True}),
            (Y, "Zeytinyağının da yatak odası varmış!", {"arms": True, "tag": "giggles"}),
            (Z, "Üç: Kapaklar sıkı sıkı kapalı. Hava alan yağ çabuk bozulur.", {"step": 2, "point": True}),
        ], [("Işıktan uzak", ic_no_sun()), ("Serin yer", ic_thermo()), ("Kapak kapalı", ic_cap())]),
        card(depot, [
            (Z, "Bir dakika... Rafın arkasına bir fotoğraf sıkışmış.", {"tag": "curious"}),
            (Z, "Dedem... ve arkasında Ulu! Altında yazıyor: Ulu ile, bin dokuz yüz seksen yedi.", {"tag": "emotional"}),
            (Y, "Ulu o zamanlar da kocamanmış!", {"mood": "wow", "gap": 0.6}),
        ], sc.old_photo()),
        END(12, "yarın 13:00", "Eski Fotoğraf"),
    ]
    return render_episode(shots, "BÖLÜM 11", OUT + "S1B11_anahtar.mp4")


# ---------------------------------------------------------------- 12
def ep12():
    clear = bg_clearing(False)
    shots = [
        with_ulu(clear, [
            (Z, "Ulu, bu fotoğrafı tanıyor musun?", {}),
            (U, "Tanımaz olur muyum... O gün deden beni korumak için söz vermişti.", {"tag": "nostalgic"}),
            (Y, "Korumak mı? Kimden?", {"mood": "wow"}),
            (U, "O yıllarda da birileri buradan yol geçirmek istemişti. Deden beni anıt ağaç yaptırmak için başvurdu.", {"tag": "softly"}),
        ]),
        summary(clear, (Z, "Anıt ağaç; yaşı, büyüklüğü ya da tarihi değeriyle öne çıkan, tescillenip koruma altına alınan ağaçtır.", {"point": True}),
                "ANIT AĞAÇ NEDİR?", ["Çok yaşlı ya da çok büyük", "Tarihi, kültürel değeri var", "Tescillenir, koruma altına alınır"]),
        with_ulu(clear, [
            (Z, "Peki başvuru ne oldu? Belge nerede?", {"tag": "curious"}),
            (U, "Deden o belgeyi defterinin arasına koymuştu...", {"tag": "sadly"}),
            (Y, "Yani... kayıp sayfa!", {"arms": True, "mood": "wow", "tag": "gasps"}),
            (Z, "O sayfayı bulursak, Beton Bey buraya asla dokunamaz!", {"tag": "determined", "gap": 0.6}),
        ]),
        END(13, "bu akşam 20:00", "Fırtına"),
    ]
    return render_episode(shots, "BÖLÜM 12", OUT + "S1B12_eski_fotograf.mp4")


# ---------------------------------------------------------------- 13
def ep13():
    night = bg_clearing(True)
    day = bg_orchard(("p",))
    shots = [
        with_ulu(night, [
            (Y, "Rüzgâr çok sert! Uçuyorum!", {"arms": True, "mood": "wow", "tag": "screaming"}),
            (Z, "Zeyto, cebime gir! Ulu, dayan!", {"tag": "shouting"}),
            (U, "Ahh... Dallarım kırılıyor!", {"tag": "pained", "gap": 0.6}),
        ], tint=((20, 26, 60), 0.32), rain=True, flashes=(0.6, 4.2, 7.5)),
        duo(day, [
            (Z, "Fırtına geçti. Ama Ulu'nun iki büyük dalı kırılmış.", {"tag": "sadly"}),
            (Y, "Ona yardım edebilir miyiz?", {"mood": "worried"}),
        ]),
        steps(day, [
            (Z, "Bir: Kırık dal, sağlam yerden, düzgün ve temiz bir kesimle alınır.", {"step": 0, "point": True}),
            (Z, "İki: Büyük kesik yerleri budama macunuyla kapatılır.", {"step": 1, "point": True}),
            (Y, "Ulu'ya yara bandı!", {"arms": True, "tag": "giggles"}),
            (Z, "Üç: Yaralardan hastalık girmesin diye bakırlı ilaç uygulanır.", {"step": 2, "point": True}),
        ], [("Düzgün kes", ic_dry_branch()), ("Macunla kapat", sc.ic_paste()), ("Bakırlı koruma", ic_copper())]),
        with_ulu(night, [
            (Y, "Mühendis Abi! Şimşek çakınca Ulu'nun kovuğunda bir şey parladı!", {"mood": "wow", "tag": "whispers"}),
            (Z, "Ben oraya sığmam... Ama sen sığarsın Zeyto.", {"tag": "thoughtful"}),
            (Y, "Ben mi?!", {"mood": "worried", "tag": "terrified", "gap": 0.6}),
        ], tint=NIGHT, flashes=(0.4,), props_top=[(glow(300), *HOLLOW_GLOW)]),
        END(14, "yarın 13:00", "Kovuğun Korkusu"),
    ]
    return render_episode(shots, "BÖLÜM 13", OUT + "S1B13_firtina.mp4")


# ---------------------------------------------------------------- 14
def ep14():
    dusk = bg_clearing(False)
    shots = [
        with_ulu(dusk, [
            (Y, "Ben o karanlık deliğe girmem! Orada canavar vardır!", {"arms": True, "mood": "worried", "tag": "panicked"}),
            (U, "Zeyto, korkmak ayıp değil. Ama korkusunu yenen cesur olur.", {"tag": "gently"}),
            (Z, "Hem yalnız değilsin. Fenerimi içeri tutarım, sesimi hep duyarsın.", {"tag": "reassuring"}),
        ], props_top=[(glow(260), *HOLLOW_GLOW)]),
        summary(dusk, (Z, "Zaten bu kovuğun bakıma ihtiyacı var. Dedem içini temizler, su birikmesin diye bakardı.", {"point": True}),
                "KOVUK BAKIMI", ["Çürük, gevşek kısımlar temizlenir", "İçinde su birikmesine izin verilmez", "Böcek yuvası olup olmadığına bakılır"]),
        with_ulu(dusk, [
            (Y, "Tamam... Üç deyince giriyorum. Bir... iki... üç!", {"mood": "worried", "tag": "nervously"}),
            (S, "Vızzz... Misafir mi geldi?", {"tag": "whispers"}),
            (Y, "O ses... Sinsi!", {"mood": "wow", "tag": "terrified", "gap": 0.6}),
        ], props_top=[(glow(260), *HOLLOW_GLOW)]),
        END(15, "bu akşam 20:00", "Sinsi'nin Yuvası"),
    ]
    return render_episode(shots, "BÖLÜM 14", OUT + "S1B14_kovugun_korkusu.mp4")


# ---------------------------------------------------------------- 15
def ep15():
    hollow = sc.bg_hollow()
    day = bg_orchard(("p",))
    sinsi_in = [{"kind": "sinsi", "x": 720, "y": 980, "scale": 1.0, "appear": 0.0}]
    shots = [
        Shot(hollow, [
            (S, "Hoş geldin minik zeytin. Burası benim kış evim.", {"tag": "mischievously"}),
            (Y, "Kış evi mi? Sinekler kışın ne yapar ki?", {"mood": "worried", "tag": "nervously"}),
            (S, "Çoğumuz toprağın altında, küçük kozalar içinde uyuruz. Ben bu sıcak kovuğu seçtim.", {"tag": "smugly"}),
        ], zeyto_x=380, gap=0.28, pan=False, actors=sinsi_in),
        steps(day, [
            (Z, "Zeyto, beni duyuyor musun? Sinsi doğru söylüyor! Bir: Zeytin sineği kışı çoğunlukla toprakta, pupa halinde geçirir.", {"step": 0, "point": True}),
            (Z, "İki: Kışın ağaç dibi sürülürse pupalar güneşe ve kuşlara açılır.", {"step": 1, "point": True}),
            (Z, "Üç: Düşen meyveler toplanırsa ilkbaharda çok daha az sinek çıkar.", {"step": 2, "point": True}),
        ], [("Toprakta kışlar", sc.ic_soil_pupa()), ("Ağaç dibini sür", sc.ic_hoe()), ("Düşenleri topla", ic_collect())], zeyto_x=None),
        Shot(hollow, [
            (Y, "Bu bilgi çok işime yarar. Hoşça kal Sinsi!", {"arms": True, "tag": "cheeky"}),
            (S, "Nereye gidiyorsun? Vızzz!", {"tag": "laughs"}),
            (Y, "Mühendis Abi! Kovuğun ağzı yapraklarla kapandı! Çıkamıyorum!", {"mood": "worried", "tag": "panicked"}),
            (S, "Hahaha! Sen de sayfa da burada kalacaksınız!", {"tag": "evil laugh", "gap": 0.6}),
        ], zeyto_x=380, gap=0.28, pan=False, actors=sinsi_in, flashes=(0.0,)),
        END(16, "yarın 13:00", "Kayıp Sayfa"),
    ]
    return render_episode(shots, "BÖLÜM 15", OUT + "S1B15_sinsinin_yuvasi.mp4")


# ---------------------------------------------------------------- 16
def ep16():
    hollow = sc.bg_hollow()
    clear = bg_clearing(False)
    day = bg_orchard(("p",))
    sinsi_in = [{"kind": "sinsi", "x": 720, "y": 980, "scale": 1.0, "appear": 0.0}]
    shots = [
        Shot(hollow, [
            (Y, "Karanlık... Ama korkmuyorum. Mühendis Abi dışarıda, Ulu da beni tutuyor.", {"tag": "bravely"}),
            (S, "Korkmuyor musun? Vızzz!", {"tag": "mockingly"}),
            (Y, "Hayır! Hem sen de aslında yalnızsın, değil mi Sinsi?", {"tag": "gently"}),
            (S, "Ben... Beton Bey bana sıcak bir ev sözü vermişti.", {"tag": "sadly"}),
            (Y, "Bak! Köklerin arasında sararmış bir kâğıt var!", {"arms": True, "mood": "wow", "tag": "excited"}),
        ], zeyto_x=380, gap=0.28, pan=False, actors=sinsi_in, props_top=[(glow(300), 560, 1700)]),
        Shot(hollow, [
            (Y, "Ulu, anıt ağaç. Tescil başvurusu yapıldı, bin dokuz yüz seksen yedi. Buldum!", {"arms": True, "tag": "excited"}),
        ], zeyto_x=840, gap=0.4, pan=False, card=sc.found_page()),
        with_ulu(clear, [
            (Z, "Zeyto! Yaprakları temizledim, çık hadi!", {"tag": "relieved"}),
            (Y, "Buldum Mühendis Abi! Kayıp sayfayı buldum!", {"arms": True, "tag": "cheering"}),
            (U, "Aferin cesur zeytin. Deden seninle gurur duyardı.", {"tag": "proudly"}),
        ]),
        summary(clear, (Z, "Sayfada dedemin bir notu daha var. Yaşlı zeytinin gövdesi içten oyulur, halkaları sayılamaz. Bu yüzden yaşı başka yollarla tahmin edilir.", {"point": True}),
                "ZEYTİN AĞACININ YAŞI", ["Gövde çevresi ölçülür", "Yaşı bilinen ağaçlarla karşılaştırılır", "Kesin yaş için laboratuvar analizi"]),
        Shot(day, [
            (B, "Kâğıt mâğıt umurumda değil! Bu akşam iş makineleriyle geliyorum!", {"tag": "angrily", "gap": 0.6}),
        ], zeynep_x=300, zeyto_x=None, gap=0.4, actors=[{"kind": "beton", "x": 790, "scale": 0.84, "enter": True}]),
        END(17, "bu akşam 20:00", "İş Makineleri"),
    ]
    return render_episode(shots, "BÖLÜM 16", OUT + "S1B16_kayip_sayfa.mp4")


# ---------------------------------------------------------------- 17
def ep17():
    sun = bg_sunset()
    exc = fit(sc.excavator(), width=640)
    shots = [
        Shot(sun, [
            (B, "Çekil önümden mühendis! Bu akşam burayı düzleyeceğiz!", {"tag": "shouting"}),
            (Z, "Bu zeytinliğe tek bir kepçe giremez!", {"tag": "firmly"}),
            (Y, "Abi... makine çok büyük...", {"mood": "worried", "tag": "scared"}),
        ], zeynep_x=270, zeyto_x=480, gap=0.28, pan=False, props=[(exc, 840, 1500)],
            actors=[{"kind": "beton", "x": 760, "scale": 0.72}]),
        summary(sun, (Z, "Beton Bey, bilmiyor musunuz? Zeytinlikler bu ülkede özel bir kanunla korunur.", {"point": True}),
                "ZEYTİNLİKLER KORUNUR", ["Zeytin ağacı izinsiz kesilemez", "Zarar verecek tesisler kısıtlanır", "Anıt ağaçlar ayrıca korunur"]),
        card(sun, [
            (B, "Kanunmuş! O ağaç anıt falan değil!", {"tag": "mockingly"}),
            (Z, "Öyle mi? İşte dedemin belgesi. Ulu, anıt ağaç olarak başvurusu yapılmış bir ağaç.", {"tag": "calmly"}),
        ], sc.found_page()),
        Shot(sun, [
            (B, "Bu... bu eski bir kâğıt parçası!", {"tag": "nervously"}),
            (M, "Dur bakalım Beton! O belgeyi bütün köy görecek. Yarın herkes köy meydanına!", {"tag": "firmly", "gap": 0.6}),
        ], zeynep_x=None, gap=0.28, pan=False, props=[(exc, 900, 1500)],
            actors=[{"kind": "muhtar", "x": 260, "scale": 0.8, "look": 1}, {"kind": "beton", "x": 640, "scale": 0.8}]),
        END(18, "yarın 13:00", "Köy Meydanı"),
    ]
    return render_episode(shots, "BÖLÜM 17", OUT + "S1B17_is_makineleri.mp4")


# ---------------------------------------------------------------- 18
def ep18():
    sq = sc.bg_square()
    trio = [{"kind": "muhtar", "x": 210, "scale": 0.74, "look": 1}, {"kind": "beton", "x": 520, "scale": 0.74}]
    shots = [
        Shot(sq, [
            (M, "Köylüler! Mühendisimiz dedesinin bir belgesini buldu.", {"tag": "loudly"}),
            (Z, "Dedem Ulu'yu anıt ağaç olarak tescil ettirmek için başvurmuş. İşte kanıtı.", {}),
            (B, "Ama... ama tapu benim elimde!", {"tag": "nervously"}),
            (M, "Tapuyu da kontrol ettirdik Beton. Arazi mühendisin dedesinindir. Senin belgen geçersiz.", {"tag": "sternly"}),
        ], zeynep_x=830, zeynep_scale=0.7, gap=0.28, pan=False, actors=trio),
        Shot(sq, [
            (Y, "Bir de Sinsi'nin söyleyeceği var!", {"arms": True, "tag": "excited"}),
            (S, "Vızzz... Laboratuvar raporunu ben çaldım. Beton Bey istedi. Özür dilerim.", {"tag": "ashamed"}),
            (Y, "Bak, Sinsi bile doğruyu söyledi!", {"arms": True, "tag": "proudly"}),
        ], zeynep_x=300, zeyto_x=560, gap=0.28, pan=False, actors=[{"kind": "sinsi", "x": 820, "y": 900, "scale": 0.9, "appear": 0.0}]),
        summary(sq, (Z, "Bundan sonra birlikte üretelim. Bir kooperatif kuralım; sıkımı, ekipmanı ve satışı birlikte yapalım.", {"point": True}),
                "BİRLİKTE GÜÇLÜYÜZ", ["Ortak sıkım: daha taze yağ", "Ortak ekipman: daha az masraf", "Ortak satış: daha iyi fiyat"]),
        Shot(sq, [
            (B, "Siz öyle sanın! Bu iş burada bitmedi!", {"tag": "angrily", "gap": 0.6}),
        ], zeynep_x=830, zeynep_scale=0.7, gap=0.4, pan=False, actors=trio),
        END(19, "bu akşam 20:00", "Dedenin Mektubu"),
    ]
    return render_episode(shots, "BÖLÜM 18", OUT + "S1B18_koy_meydani.mp4")


# ---------------------------------------------------------------- 19
def ep19():
    sun = bg_sunset()
    clear = bg_clearing(False)
    shots = [
        with_ulu(clear, [
            (Z, "Zeytinlik kurtuldu Ulu. Ama defterin son sayfası hâlâ yapışık duruyor.", {"tag": "softly"}),
            (U, "Aç onu evlat. Deden onu sana yazdı.", {"tag": "softly"}),
        ]),
        card(sun, [
            (Z, "Torunum, bu defter artık senin. Ağaçlara iyi bak.", {"tag": "emotional"}),
            (Z, "Onları dinlersen, onlar da seni dinler. Seni çok seviyorum. Deden.", {"tag": "crying"}),
            (Y, "Ağlama Mühendis Abi... Ben de ağlayacağım şimdi.", {"mood": "worried", "tag": "sniffles"}),
        ], sc.letter()),
        summary(clear, (U, "Deden bir de her zeytin farklıdır derdi. Kimi yağ olur, kimi sofraya gider.", {}),
                "YAĞLIK VE SOFRALIK", ["Yağlık: Memecik, Ayvalık", "Sofralık: Domat", "İkisine de uyar: Gemlik"]),
        with_ulu(clear, [
            (Y, "Peki ben... Ben ne olacağım? Yağ mı, sofra mı?", {"mood": "worried", "tag": "worried"}),
            (Z, "Bu karar senin Zeyto.", {"tag": "gently", "gap": 0.6}),
        ]),
        END(20, "yarın 13:00 · Final", "Mühendisin Defteri"),
    ]
    return render_episode(shots, "BÖLÜM 19", OUT + "S1B19_dedenin_mektubu.mp4")


# ---------------------------------------------------------------- 20
def ep20():
    mill = bg_mill()
    clear = bg_clearing(False)
    sun = bg_sunset()
    shots = [
        card(mill, [
            (Z, "İşte ilk şişelerimiz! Üzerinde ne yazıyor bakın: Mühendisin Defteri.", {"tag": "proudly"}),
            (Y, "Kardeşlerim bunun içinde! Çok yakışmışlar!", {"arms": True, "tag": "excited"}),
        ], sc.bottle_label()),
        with_ulu(clear, [
            (Y, "Kararımı verdim. Ne yağ olacağım, ne sofraya gideceğim.", {"tag": "determined"}),
            (Z, "Ne olacaksın peki?", {"tag": "curious"}),
            (Y, "Ulu'nun dibine düşüp toprağa karışacağım. Belki bir gün ben de bir fidan olurum!", {"arms": True, "tag": "hopeful"}),
            (U, "Sabırla büyüyen hazine... Deden de tam böyle derdi.", {"tag": "warmly"}),
        ]),
        summary(sun, (Z, "Yeni sezon zeytinyağımız hazır. Ön sipariş için bize mesaj atmanız yeterli!", {"point": True, "tag": "cheerfully"}),
                "YENİ SEZON YAĞI", ["Yeşil, meyvemsi koku", "Hafif acı, boğazda yakma", "Düşük asitlik: natürel sızma"]),
        card(sun, [
            (Y, "Mühendis Abi! Defterin arka kapağından bir harita düştü!", {"arms": True, "mood": "wow", "tag": "excited"}),
            (Z, "Kayıp Fidan... Dedemin bir sırrı daha varmış.", {"tag": "intrigued", "gap": 0.7}),
        ], sc.new_map()),
        end_shot("Sezon 2 yakında", "Kayıp Fidan", GREEN_OLIVE, cta="Takip et, kaçırma!"),
    ]
    return render_episode(shots, "BÖLÜM 20", OUT + "S1B20_muhendisin_defteri.mp4")


if __name__ == "__main__":
    for w in sys.argv[1:]:
        print(globals()["ep" + w]())
