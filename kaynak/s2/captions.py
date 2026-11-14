import json, sys
sys.path.insert(0, "/home/claude/dt")
from make_s2 import TITLES, FILES
from make_notes import NOTES
EPQ = {
 1: ("Ulu'nun bir yavrusu varmış... Ve Beton Bey her şeyi duydu.", "Sizce kayıp fidan hâlâ yaşıyor mu?"),
 2: ("Muhtar, dağdaki bahçenin neden terk edildiğini anlatıyor.", "Sizin köyde hiç ayaz zeytinleri vurdu mu?"),
 3: ("Çantadan vızıltı geliyor... Sinsi geri döndü!", "Sinsi'ye güvenilir mi? Evet mi hayır mı?"),
 4: ("Köprü yıkık, dere coşkun. Zeyto suya düşüyor!", "Sizce çizme izleri kimin?"),
 5: ("Dedenin bahçesi delice ve dikenle dolmuş. Çarpının yerinde ise...", "Fidan nereye gitti sizce?"),
 6: ("Taşın altından dedenin bir notu çıkıyor.", "Limonla yazılmış yazı nasıl okunur, biliyor musunuz?"),
 7: ("Sinsi, Beton Bey'in peşinde!", "Sinsi artık takımın bir parçası mı?"),
 8: ("Ateşin başında görünmez yazı ortaya çıkıyor.", "Siz bu deneyi hiç yaptınız mı?"),
 9: ("Eski okul, kuyu ve kocaman bir zeytin ağacı...", "Otuz yılda fidan ne kadar büyür sizce?"),
 10: ("Kepçe okul bahçesinde. Beton Bey'in elinde bir izin kâğıdı var.", "Sizce bu izin geçerli mi?"),
 11: ("Kanıt lazım: Yapraklar laboratuvara gidiyor.", "Zeytin çeşitlerini ayırt edebilir misiniz?"),
 12: ("Gece nöbeti... ve karanlıkta bir fener.", "Sizin yağınız hiç kışın dondu mu?"),
 13: ("Gövdede dedenin yazısı: Torunum için.", "Hiç aşı yaptınız mı?"),
 14: ("Laboratuvar sonucu geldi!", "Sizin yörenizin yerel zeytin çeşidi ne?"),
 15: ("Köy meydanında büyük toplantı.", "Bir litre yağa kaç kilo zeytin gittiğini biliyor muydunuz?"),
 16: ("Geçen sezonun anahtarı, sonunda kilidini buluyor.", "Anahtarı hatırlayan var mı?"),
 17: ("Sinsi, en zor kararını veriyor.", "Siz Sinsi'nin yerinde olsanız ne yapardınız?"),
 18: ("Beton Bey'in hiç anlatmadığı hikâye.", "Beton Bey'i affeder misiniz?"),
 19: ("Kayıp fidanın yaprakları sararıyor.", "Ağaçlarınızda yaprak sararması oldu mu?"),
 20: ("Sezon finali: Ulu, yavrusuna kavuşuyor.", "Sezon 3'te ne görmek istersiniz? Yorumlara yazın!"),
}
TAGS = "#zeytin #zeytinyağı #ziraatmühendisi #tarım #animasyon #mühendisindefteri #kayıpfidan"
NTAGS = "#zeytinyağı #mutfakbilgisi #meyvesebze #pratikbilgiler #tarım #mühendisindefteri"
out = {}
for n, (hook, q) in EPQ.items():
    nxt = f"📌 Bölüm {n+1} yarın 20:00'de." if n < 20 else "📌 Sezon 3 yakında. Yeni sezon zeytinyağı siparişi için DM."
    out[f"ep{n}"] = f"🫒 Zeytinliğin Sırrı · Sezon 2 · Bölüm {n}: {TITLES[n]}\n\n{hook}\n\n💬 {q}\n{nxt}\n\n{TAGS}"
for n, (fn, slug, title) in NOTES.items():
    out[f"n{n}"] = f"🫒 Zeyto'nun Notları #{n}: {title}\n\nKaydet, lazım olduğunda aç. 💾\n💬 Videodaki soruya cevabını yorumlara yaz!\n📌 Her gün 13:00'te yeni not, 20:00'de yeni bölüm.\n\n{NTAGS}"
json.dump(out, open("/home/claude/dt/s2/captions.json", "w"), ensure_ascii=False, indent=1)
print(out["ep1"]); print(); print(out["n8"])
