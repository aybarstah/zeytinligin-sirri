"""Turn episode timelines into a voice-over script (who says what, when)."""
import json, sys, glob, os

TITLES = {"B1": "Hasadın 4 altın kuralı", "B2": "Yeşil mi, siyah mı?", "B3": "Zeytinden yağa 5 adım",
          "B4": "Zeytin neden acı?", "B5": "Evde kırma zeytin", "B6": "Yağ nasıl saklanır?",
          "B7": "3 zeytinyağı efsanesi"}
NAMES = {"zeynep": "MÜHENDİS", "zeyto": "ZEYTO   "}


def ts(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


out = ["MÜHENDİSİN DEFTERİ · SESLENDİRME METİNLERİ",
       "",
       "Nasıl kullanılır: Videoyu Instagram'da (Reels düzenleyici > Seslendirme) ya da CapCut'ta açın.",
       "Her satırı yanındaki saniyede, konuşma balonu ekranda belirince okuyun.",
       "Mühendis = kendi doğal sesiniz. Zeyto = biraz daha ince, hızlı ve şaşkın bir ses.",
       "Kayıttan sonra fon müziğinin sesini %20-30'a indirin ki konuşma net duyulsun.",
       ""]
for p in sorted(glob.glob(sys.argv[1] + "/B*.events.json")):
    code = os.path.basename(p).split("_")[0]
    ev = json.load(open(p))
    out.append("=" * 60)
    out.append(f"{code.replace('B', 'BÖLÜM ')} · {TITLES.get(code, '')}   (toplam {ev['total']:.0f} sn)")
    out.append("=" * 60)
    for ln in ev["lines"]:
        out.append(f"[{ts(ln['t'])} – {ts(ln['t'] + ln['dur'])}]  {NAMES[ln['speaker']]}: {ln['text']}")
    if "end" in ev:
        out.append(f"[{ts(ev['end'])}]  (Kapanış kartı: müzik, konuşma yok)")
    out.append("")
open(sys.argv[2], "w").write("\n".join(out))
print(sys.argv[2])
