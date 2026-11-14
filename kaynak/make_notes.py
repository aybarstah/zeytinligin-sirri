"""Zeyto'nun Notları #8-#27 — günlük bilgi videoları (her gün 13:00)."""
import sys
from brand import *
from story import Shot, render_episode, bg_orchard, bg_mill
from make_main import end_shot, OUT, ic_copper, ic_dry_branch
from make_story import ic_crate, ic_wash
from make_story2 import bg_kitchen, ic_jar, ic_fridge, ic_no_sun, ic_thermo, ic_cap, ic_salt, ic_water, ic_lab, ic_throat, ic_pan
import scenes2 as sc
import scenes3 as s3

Z, Y = "zeynep", "zeyto"
NOTES = {}


def note(n, slug, title):
    def deco(fn):
        NOTES[n] = (fn, slug, title)
        return fn
    return deco


def make(n, bg, hook, step_lines, items, sum_line, sum_title, sum_items, accent=OLIVE):
    shots = [
        Shot(bg, hook, zeynep_x=330, zeyto_x=790, zeynep_enter=True, gap=0.28),
        Shot(bg, step_lines, zeynep_x=270, zeyto_x=840, gap=0.28, steps=items, accent=accent),
        Shot(bg, [sum_line], zeynep_x=270, zeyto_x=840, gap=0.5, summary=(sum_title, sum_items), accent=accent),
        end_shot("Kaydet, lazım olur!", "Yorumlara yaz", GREEN_OLIVE, cta="Takip et · Her gün 13:00"),
    ]
    fn, slug, title = NOTES[n]
    return render_episode(shots, f"ZEYTO'NUN NOTLARI #{n}", OUT + f"N{n:02d}_{slug}.mp4")


def P(t):
    return (Z, t, {"point": True})


def S_(k, t):
    return (Z, t, {"step": k, "point": True})


KIT = bg_kitchen
MARKET = sc.bg_square


@note(8, "sizma_riviera_rafine", "Sızma mı, riviera mı?")
def n8():
    return make(8, KIT(), [
        (Y, "Markette üç şişe var: sızma, riviera, rafine. Hangisini alayım?", {"mood": "worried", "arms": True}),
        (Z, "Etiketteki o tek kelime her şeyi anlatır. Bak!", {}),
    ], [
        S_(0, "Bir: Natürel sızma, zeytinin sadece mekanik yolla sıkılmasıyla elde edilir. Asitliği en fazla yüzde sıfır virgül sekizdir."),
        S_(1, "İki: Rafine yağ, kusurlu yağların arıtılmasıyla yapılır. Tadı ve kokusu neredeyse yoktur."),
        S_(2, "Üç: Riviera, rafine yağ ile bir miktar natürel yağın karışımıdır."),
    ], [("Natürel sızma", icon_bottle()), ("Rafine: arıtılmış", ic_lab()), ("Riviera: karışım", sc.ic_big_text("R", "karışım"))],
        P("Sen evde hangisini kullanıyorsun? Yorumlara yaz!"), "ETİKET SÖZLÜĞÜ",
        ["Sızma: sadece sıkım, ≤ %0,8", "Rafine: arıtılmış, tatsız", "Riviera: rafine + natürel"])


@note(9, "cilek_secimi", "Çilek nasıl seçilir?")
def n9():
    return make(9, MARKET(), [
        (Y, "Mühendis Abi, bu çilekler kıpkırmızı! Hepsi tatlı mıdır?", {"arms": True, "mood": "wow"}),
        (Z, "Her kırmızı çilek tatlı değildir. Üç işarete bak.", {}),
    ], [
        S_(0, "Bir: Kırmızılık sapına kadar inmeli. Çilek dalından koptuktan sonra olgunlaşmaz."),
        S_(1, "İki: Yeşil yaprakları taze ve dik olsun. Pörsümüşse çilek bekletilmiştir."),
        S_(2, "Üç: Eve gelince yıkamadan, tek kat halinde buzdolabına koy. Yemeden hemen önce yıka."),
    ], [("Sapına kadar kırmızı", icon_strawberry()), ("Taze yeşil yaprak", icon_leaf()), ("Yıkamadan sakla", ic_crate())],
        P("Çileği en çok neyle seversin? Yorumlara yaz!"), "ÇİLEK REHBERİ",
        ["Sapına kadar kırmızı", "Yaprakları taze", "Yıkamadan, buzdolabında"], accent=RED)


@note(10, "acilan_zeytin", "Açılan zeytin nasıl saklanır?")
def n10():
    return make(10, KIT(), [
        (Y, "Kavanozu açtık, bir hafta sonra zeytinler yumuşadı. Neden?", {"mood": "worried"}),
        (Z, "Açılan zeytin üç şeye dikkat ister.", {}),
    ], [
        S_(0, "Bir: Zeytini kendi salamurasından ayırma. Suyunu dökersen çabuk bozulur."),
        S_(1, "İki: Kavanozu buzdolabında sakla ve hep temiz, kuru bir kaşık kullan."),
        S_(2, "Üç: Üstüne ince bir kat zeytinyağı dök. Hava ile teması keser."),
    ], [("Salamurada kalsın", ic_jar()), ("Temiz kaşık", ic_fridge()), ("Üstüne zeytinyağı", icon_bottle())],
        P("Kahvaltıda yeşil mi siyah mı? Yorumlara yaz!"), "AÇILAN ZEYTİN",
        ["Salamurasında kalsın", "Buzdolabı + temiz kaşık", "Üstüne ince kat yağ"])


@note(11, "siyah_zeytin", "Siyah zeytin neden siyah?")
def n11():
    return make(11, KIT(), [
        (Y, "Ben yeşilim, ablam siyah. Biz farklı ağaçtan mıyız?", {"mood": "wow"}),
        (Z, "Hayır! Aynı ağaçta olursunuz. Fark zamanlamada.", {}),
    ], [
        S_(0, "Bir: Zeytin önce yeşildir, olgunlaştıkça mora, sonra siyaha döner."),
        S_(1, "İki: Doğal siyah zeytin dalında olgunlaşır. Kırışık ve aromatik olur."),
        S_(2, "Üç: Bazı siyah zeytinler ise yeşilken havayla karartılır. Etikette demir glukonat yazar."),
    ], [("Yeşil → mor → siyah", icon_branch()), ("Dalında olgun", icon_olive(BLACKOLIVE)), ("Etikete bak", sc.ic_big_text("E579", "demir glukonat"))],
        P("Senin kahvaltılık zeytinin hangisi? Yorumlara yaz!"), "SİYAH ZEYTİN",
        ["Aynı ağaç, farklı olgunluk", "Doğal: dalında kararır", "Etikette E579 = karartılmış"])


@note(12, "domates_buzdolabi", "Domates buzdolabına girer mi?")
def n12():
    return make(12, KIT(), [
        (Y, "Domatesleri buzdolabına diziyorum, taze kalsınlar!", {"arms": True}),
        (Z, "Dur! Soğuk domatesin tadını kaçırır.", {}),
    ], [
        S_(0, "Bir: On iki derecenin altında domatesin aroması azalır, dokusu unlu olur."),
        S_(1, "İki: Domatesi tezgâhta, güneş almayan bir yerde, sapı aşağı bakacak şekilde sakla."),
        S_(2, "Üç: Çok olgunlaştıysa buzdolabına koyabilirsin. Yemeden bir saat önce çıkar."),
    ], [("Soğuk aromayı öldürür", s3.ic_snow()), ("Tezgâhta sakla", s3.ic_tomato()), ("Yemeden önce çıkar", ic_thermo())],
        P("Domatesi buzdolabında mı saklıyordun? Yorumlara yaz!"), "DOMATES KURALI",
        ["12 °C altı tadı bozar", "Tezgâhta, sapı aşağı", "Fazla olgunsa dolaba"], accent=RED)


@note(13, "mandalina_secimi", "Mandalina nasıl seçilir?")
def n13():
    return make(13, MARKET(), [
        (Y, "Mandalinanın en sulusunu nasıl bulurum?", {"mood": "wow"}),
        (Z, "Göze değil, ele güven. Bak nasıl.", {}),
    ], [
        S_(0, "Bir: Eline al. Boyuna göre ağır olan, daha sulu demektir."),
        S_(1, "İki: Kabuğu parlak ve ince olsun. Yumuşak ya da küflü nokta olmasın."),
        S_(2, "Üç: Serin yerde birkaç gün, buzdolabında iki haftaya kadar dayanır."),
    ], [("Ağır olanı seç", s3.ic_scale_heavy()), ("Parlak, ince kabuk", s3.ic_mandarin()), ("Serin sakla", ic_fridge())],
        P("Mandalina mı portakal mı? Yorumlara yaz!"), "MANDALİNA",
        ["Boyuna göre ağır", "Parlak ince kabuk", "Serin yerde sakla"], accent=RED)


@note(14, "erken_hasat", "Erken hasat yağ nedir?")
def n14():
    return make(14, bg_mill(), [
        (Y, "Erken hasat yağ neden bu kadar pahalı?", {"mood": "worried"}),
        (Z, "Çünkü zeytin daha yeşilken toplanır. Ve bunun bir bedeli var.", {}),
    ], [
        S_(0, "Bir: Zeytin olgunlaşmadan, genelde ekimde ya da kasım başında toplanır."),
        S_(1, "İki: Yağı yeşil renkli, otsu kokulu, belirgin acı ve yakıcı olur. Polifenolü yüksektir."),
        S_(2, "Üç: Ama yeşil zeytin az yağ verir. Bir litre için çok daha fazla zeytin gerekir."),
    ], [("Erken toplanır", icon_olive(GREEN_OLIVE)), ("Acı ve yakıcı", ic_throat()), ("Verim düşük", sc.ic_big_text("8-10", "kg / litre"))],
        P("Sen acı yağ sever misin? Yorumlara yaz!"), "ERKEN HASAT",
        ["Yeşil zeytinden", "Acı, yakıcı, otsu", "Az verim, yüksek emek"])


@note(15, "nar", "Nar nasıl seçilir ve ayıklanır?")
def n15():
    return make(15, KIT(), [
        (Y, "Nar ayıklarken her yer kıpkırmızı oldu!", {"mood": "worried", "arms": True}),
        (Z, "Su dolu bir kapla hiç sıçratmadan ayıklarız. Önce seçelim.", {}),
    ], [
        S_(0, "Bir: Ağır, kabuğu sert ve gergin olan narı seç. Olgun nar biraz köşeli görünür."),
        S_(1, "İki: Tepesini kes, dilimlerin çizgisinden kabuğu çiz ve elinle ayır."),
        S_(2, "Üç: Su dolu kapta taneleri ayıkla. Taneler dibe çöker, zarlar yüzeye çıkar."),
    ], [("Ağır, köşeli", icon_pomegranate()), ("Çizgiden ayır", sc.ic_big_text("4-6", "dilim")), ("Suyun içinde ayıkla", s3.ic_bowl_water())],
        P("Narı en çok neye katarsın? Yorumlara yaz!"), "NAR",
        ["Ağır ve köşeli olanı seç", "Çizgisinden ayır", "Su dolu kapta ayıkla"], accent=RED)


@note(16, "meyve_sebze_yikama", "Meyve sebze nasıl yıkanır?")
def n16():
    return make(16, KIT(), [
        (Y, "Elmayı deterjanla yıkasam daha temiz olur, değil mi?", {"arms": True}),
        (Z, "Asla! Deterjan meyvenin kabuğuna siner.", {}),
    ], [
        S_(0, "Bir: Akan su altında, elinle ovarak yıka. Sadece suya batırmak yetmez."),
        S_(1, "İki: Yapraklı sebzeleri yaprak yaprak ayır. Kabuğu sert olanları fırçala."),
        S_(2, "Üç: Hemen yemeyeceksen yıkama. Nem, çürümeyi hızlandırır."),
    ], [("Akan suda ov", s3.ic_tap()), ("Yaprak yaprak", s3.ic_veg_basket()), ("Yemeden önce yıka", ic_water())],
        P("Sen nasıl yıkıyorsun? Yorumlara yaz!"), "DOĞRU YIKAMA",
        ["Akan su + ovma", "Deterjan yok", "Yemeden hemen önce"])


@note(17, "yag_raf_omru", "Zeytinyağı kaç yıl dayanır?")
def n17():
    return make(17, KIT(), [
        (Y, "Babaannemin dolabında üç yıllık yağ var. Daha güzelleşmiştir!", {"arms": True}),
        (Z, "Zeytinyağı şarap değil Zeyto. Bekledikçe kaybeder.", {}),
    ], [
        S_(0, "Bir: Zeytinyağı en iyi hasattan sonraki on iki ile on sekiz ay içinde tüketilir."),
        S_(1, "İki: Bu yüzden şişede hasat yılını ara. Son kullanma tarihi tek başına yetmez."),
        S_(2, "Üç: Yağ bayatlayınca boya ya da eski ceviz gibi kokar. Bu acılık değil, bozulmadır."),
    ], [("12-18 ay", sc.ic_big_text("12-18", "ay")), ("Hasat yılına bak", s3.ic_years()), ("Bayat koku", sc.ic_smell())],
        P("Senin yağının hasat yılı ne? Etikete bak, yorumlara yaz!"), "YAĞIN ÖMRÜ",
        ["En iyisi 12-18 ay içinde", "Hasat yılına bak", "Boya kokusu = bayat"])


@note(18, "kis_sebzeleri", "Kışın mevsiminde ne yenir?")
def n18():
    return make(18, MARKET(), [
        (Y, "Pazarda her şey var. Hangisi gerçekten mevsiminde?", {"mood": "wow"}),
        (Z, "Mevsiminde olan hem daha lezzetli, hem daha uygun fiyatlı.", {}),
    ], [
        S_(0, "Bir: Kış sebzeleri: ıspanak, pırasa, lahana, karnabahar, brokoli, havuç ve kereviz."),
        S_(1, "İki: Kış meyveleri: mandalina, portakal, nar, ayva ve elma."),
        S_(2, "Üç: Sofrada zeytinyağlı pırasa, ıspanak, kereviz. Mevsimin tadı zeytinyağıyla çıkar."),
    ], [("Kış sebzeleri", s3.ic_veg_basket()), ("Kış meyveleri", s3.ic_mandarin()), ("Zeytinyağlılar", icon_bottle())],
        P("Kışın en sevdiğin zeytinyağlı hangisi? Yorumlara yaz!"), "KIŞ SOFRASI",
        ["Ispanak, pırasa, karnabahar", "Mandalina, nar, ayva", "Zeytinyağıyla pişir"])


@note(19, "cografi_isaret", "Coğrafi işaretli zeytinyağı")
def n19():
    return make(19, KIT(), [
        (Y, "Şişede kırmızı yuvarlak bir logo var. Bu ne?", {"mood": "wow"}),
        (Z, "Coğrafi işaret! O yağın nereden geldiğinin garantisi.", {}),
    ], [
        S_(0, "Bir: Coğrafi işaret, bir ürünün özelliğini o bölgeden aldığını gösterir."),
        S_(1, "İki: Ayvalık, Edremit ve Milas zeytinyağları coğrafi işaretlidir."),
        S_(2, "Üç: Logo etikette görünür. Üretim, bölgenin kurallarına göre denetlenir."),
    ], [("Bölgenin garantisi", ic_label_gi_safe()), ("Ayvalık · Edremit · Milas", s3.ic_map_pin()), ("Etikette logo", icon_bottle())],
        P("Senin yöreninki hangisi? Yorumlara yaz!"), "COĞRAFİ İŞARET",
        ["Bölgesinin özelliğini taşır", "Ayvalık, Edremit, Milas", "Etikette logoyu ara"])


def ic_label_gi_safe():
    return s3.ic_label_gi()


@note(20, "gumus_yaprak", "Zeytin yaprağı neden gümüşi?")
def n20():
    return make(20, bg_orchard(("p",)), [
        (Y, "Rüzgâr esince bütün zeytinlik gümüş gibi parlıyor! Neden?", {"arms": True, "mood": "wow"}),
        (Z, "Yaprağın arka yüzünde minik bir sır var.", {}),
    ], [
        S_(0, "Bir: Zeytin yaprağının alt yüzü, mikroskopla görülen minik pullu tüylerle kaplıdır."),
        S_(1, "İki: Bu tüyler ışığı yansıtır. Rüzgârda yapraklar dönünce gümüş gibi parlar."),
        S_(2, "Üç: Aynı tüyler yaprağın su kaybını azaltır. Zeytin bu yüzden kuraklığa dayanır."),
    ], [("Minik pullu tüyler", s3.ic_silver_leaf()), ("Işığı yansıtır", s3.ic_sun_hours()), ("Suyu korur", s3.ic_drop())],
        P("Zeytinliği rüzgârda gördün mü? Yorumlara yaz!"), "GÜMÜŞ YAPRAK",
        ["Alt yüzü pullu tüylerle kaplı", "Işığı yansıtır", "Kuraklığa dayanır"])


@note(21, "bulanik_yag", "Taze yağ neden bulanık?")
def n21():
    return make(21, bg_mill(), [
        (Y, "Yeni sıkım yağımız bulanık! Bozuk mu?", {"mood": "worried"}),
        (Z, "Hayır. Bu, yağın süzülmemiş olduğunu gösterir.", {}),
    ], [
        S_(0, "Bir: Taze sıkılan yağda zeytinin minik parçaları ve biraz su bulunur."),
        S_(1, "İki: Yağ dinlendikçe bu tortu dibe çöker. Üstteki berrak yağ ayrılabilir."),
        S_(2, "Üç: Süzülmemiş yağı daha kısa sürede tüket. Tortu zamanla yağın tadını bozabilir."),
    ], [("Tortu ve su", s3.ic_cloudy()), ("Dinlenince çöker", s3.ic_years()), ("Çabuk tüket", sc.ic_big_text("3-4", "ay"))],
        P("Bulanık yağ mı, berrak yağ mı? Yorumlara yaz!"), "BULANIK YAĞ",
        ["Süzülmemiş, taze yağ", "Tortu dibe çöker", "Daha kısa sürede tüket"])


@note(22, "saksida_zeytin", "Balkonda zeytin yetişir mi?")
def n22():
    return make(22, KIT(), [
        (Y, "Balkonumuzda bir zeytin ağacı olabilir mi?", {"arms": True, "mood": "wow"}),
        (Z, "Olur! Ama üç şartı var.", {}),
    ], [
        S_(0, "Bir: Büyük, altı delikli bir saksı seç. Kırk, elli litre iyi bir başlangıçtır."),
        S_(1, "İki: Günde en az altı saat güneş almalı. Gölge balkonda meyve vermez."),
        S_(2, "Üç: Toprak kuruyunca sula, saksıda su bırakma. Kışın serinlikte kalsın ama ayazdan koru."),
    ], [("Büyük saksı", s3.ic_pot_tree()), ("6 saat güneş", s3.ic_sun_hours()), ("Az ama doğru su", s3.ic_drop())],
        P("Balkonunda hangi bitki var? Yorumlara yaz!"), "SAKSIDA ZEYTİN",
        ["40-50 L, delikli saksı", "Günde 6+ saat güneş", "Az su, ayazdan koru"])


@note(23, "kis_meyve_agaci", "Kışın meyve ağaçlarına bakım")
def n23():
    return make(23, bg_orchard(("p",)), [
        (Y, "Yapraklar döküldü. Ağaçlar kışın tatile mi çıktı?", {"mood": "wow"}),
        (Z, "Onlar dinleniyor, ama biz çalışıyoruz!", {}),
    ], [
        S_(0, "Bir: Yaprak dökümünden sonra hastalıklara karşı bordo bulamacı uygulanır."),
        S_(1, "İki: Ağaçta kalan kurumuş, mumyalaşmış meyveleri ve hastalıklı dalları temizle."),
        S_(2, "Üç: Kış budaması, ağaç dinlenmedeyken, ayazlı günler dışında yapılır."),
    ], [("Bordo bulamacı", s3.ic_bucket_blue()), ("Kuru meyveyi topla", ic_dry_branch()), ("Kış budaması", s3.ic_pruning())],
        P("Bahçende hangi ağaç var? Yorumlara yaz!"), "KIŞ BAKIMI",
        ["Yaprak dökümünde bordo", "Mumya meyveleri topla", "Dinlenmede buda"])


@note(24, "tuzlu_zeytin", "Zeytin çok tuzluysa ne yapmalı?")
def n24():
    return make(24, KIT(), [
        (Y, "Bu zeytin o kadar tuzlu ki dilim yandı!", {"mood": "worried", "arms": True}),
        (Z, "Çözümü basit. Zeytin tuzunu suya bırakır.", {}),
    ], [
        S_(0, "Bir: Yiyeceğin kadar zeytini soğuk suya koy, birkaç saat beklet."),
        S_(1, "İki: Çok tuzluysa suyunu bir iki kez değiştir. Tadına bakarak ilerle."),
        S_(2, "Üç: Süzdükten sonra zeytinyağı, kekik ya da limon kabuğuyla tatlandır. Hemen tüket."),
    ], [("Soğuk suda beklet", ic_water()), ("Suyu değiştir", ic_salt()), ("Yağ ve kekikle tatlandır", icon_bottle())],
        P("Zeytine ne eklersin? Yorumlara yaz!"), "TUZLU ZEYTİN",
        ["Soğuk suda birkaç saat", "Suyu 1-2 kez değiştir", "Yağla tatlandır, hemen ye"])


@note(25, "limon", "Limon nasıl saklanır?")
def n25():
    return make(25, KIT(), [
        (Y, "Limonlar hep buruşuyor, suyu da az çıkıyor.", {"mood": "worried"}),
        (Z, "İki küçük numarayla değişir.", {}),
    ], [
        S_(0, "Bir: Tezgâhta bir hafta dayanır. Buzdolabında, ağzı kapalı poşette haftalarca taze kalır."),
        S_(1, "İki: Sıkmadan önce tezgâhta avucunla bastırarak yuvarla. Daha çok su verir."),
        S_(2, "Üç: Buzdolabından yeni çıktıysa önce ılık suda birkaç dakika beklet."),
    ], [("Kapalı poşette dolapta", ic_fridge()), ("Bastırarak yuvarla", sc.ic_big_text("+", "daha çok su")), ("Ilık su", ic_water())],
        P("Limonu en çok nerede kullanırsın? Yorumlara yaz!"), "LİMON",
        ["Dolapta kapalı poşette", "Sıkmadan önce yuvarla", "Soğuksa ılık suya"])


@note(26, "elma_muz", "Elma ve muz neden ayrı durmalı?")
def n26():
    return make(26, KIT(), [
        (Y, "Meyve tabağına muzu koydum, ertesi gün her şey çok olgunlaşmış!", {"mood": "worried"}),
        (Z, "Suçlu etilen gazı! Bazı meyveler bu gazı salar.", {}),
    ], [
        S_(0, "Bir: Elma, muz, armut ve avokado olgunlaşırken etilen gazı salar."),
        S_(1, "İki: Bu gaz yanındaki meyve ve sebzelerin de hızla olgunlaşıp yumuşamasına yol açar."),
        S_(2, "Üç: Ama ham avokadoyu bir elmayla kese kâğıdına koyarsan çabuk olgunlaşır!"),
    ], [("Etilen salanlar", icon_branch()), ("Ayrı sakla", ic_crate()), ("Avokado numarası", sc.ic_big_text("1-2", "gün"))],
        P("Bu numarayı biliyor muydun? Yorumlara yaz!"), "ETİLEN",
        ["Elma, muz, armut gaz salar", "Diğerlerinden ayrı sakla", "Ham meyveyi elmayla olgunlaştır"], accent=RED)


@note(27, "zeytinyaglilar_soguk", "Zeytinyağlılar neden soğuk yenir?")
def n27():
    return make(27, KIT(), [
        (Y, "Zeytinyağlı fasulyeyi neden sıcak yemiyoruz?", {"mood": "wow"}),
        (Z, "Bunun lezzetli bir sebebi var.", {}),
    ], [
        S_(0, "Bir: Tereyağı soğuyunca donar, ağızda kaba bir his bırakır. Zeytinyağı oda sıcaklığında akışkan kalır."),
        S_(1, "İki: Yemek dinlendikçe sebze, yağı ve aromayı içine çeker. Lezzet oturur."),
        S_(2, "Üç: Zeytinyağlılar az suyla, kısık ateşte, sebzenin kendi suyunda pişer."),
    ], [("Akışkan kalır", icon_bottle()), ("Dinlenince oturur", ic_thermo()), ("Kısık ateş", ic_pan())],
        P("En sevdiğin zeytinyağlıyı yorumlara yaz!"), "ZEYTİNYAĞLILAR",
        ["Soğukta akışkan kalır", "Dinlenince lezzet oturur", "Az su, kısık ateş"])


if __name__ == "__main__":
    for w in sys.argv[1:]:
        print(globals()["n" + w]())
