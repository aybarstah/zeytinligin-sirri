import subprocess, os, sys
from PIL import Image, ImageDraw, ImageFilter
from brand import font, F_BOLD, F_MED, SUN, CREAM, DARK, OLIVE
W, H = 1080, 1920
EP = {1: ("S1B1_dedemin_defteri_v3", "Dedemin Defteri"), 2: ("S1B2_ulunun_sinavi_v3", "Ulu'nun Sınavı"),
      3: ("S1B3_sinsinin_plani_v3", "Sinsi'nin Planı"), 4: ("S1B4_beton_bey", "Beton Bey"),
      5: ("S1B5_ulu_hastalandi", "Ulu Hastalandı"), 6: ("S1B6_gece_kazisi", "Gece Kazısı"), 7: ("S1B7_ilk_yag", "İlk Yağ"),
      8: ("S1B8_asitlik_testi", "Asitlik Testi"), 9: ("S1B9_sinsi_kacti", "Sinsi Kaçtı"), 10: ("S1B10_koy_kahvesi", "Köy Kahvesi"),
      11: ("S1B11_anahtar", "Anahtar"), 12: ("S1B12_eski_fotograf", "Eski Fotoğraf"), 13: ("S1B13_firtina", "Fırtına"),
      14: ("S1B14_kovugun_korkusu", "Kovuğun Korkusu"), 15: ("S1B15_sinsinin_yuvasi", "Sinsi'nin Yuvası"),
      16: ("S1B16_kayip_sayfa", "Kayıp Sayfa"), 17: ("S1B17_is_makineleri", "İş Makineleri"), 18: ("S1B18_koy_meydani", "Köy Meydanı"),
      19: ("S1B19_dedenin_mektubu", "Dedenin Mektubu"), 20: ("S1B20_muhendisin_defteri", "Mühendisin Defteri")}
CLIP = 12.0
SCR = "/tmp/claude-0/-home-claude/d0c632b1-4532-5cb4-a684-996a9f7f43ea/scratchpad/st"
os.makedirs(SCR, exist_ok=True)


def pill():
    t = "Bölümün tamamı profilde"
    f = font(F_BOLD, 46)
    w = int(f.getlength(t)) + 120
    im = Image.new("RGBA", (W, 140), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0 = (W - w) // 2
    d.rounded_rectangle([x0, 20, x0 + w, 120], radius=50, fill=SUN + (245,))
    d.polygon([(x0 + 40, 48), (x0 + 40, 92), (x0 + 76, 70)], fill=DARK)
    d.text((x0 + 96, 38), t, font=f, fill=DARK)
    return im


def card(bg_png, n, title, final=False):
    bg = Image.open(bg_png).convert("RGB").filter(ImageFilter.GaussianBlur(18)).convert("RGBA")
    bg.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 150)))
    d = ImageDraw.Draw(bg)
    rows = [("SEZON FİNALİ" if final else "YENİ BÖLÜM", 64, CREAM, 660), (f"BÖLÜM {n}", 150, SUN, 760),
            (title, 82, (255, 255, 255), 960), ("YAYINDA", 64, CREAM, 1080), ("Tamamı profildeki Reels'te", 50, SUN, 1300)]
    for t, s, c, y in rows:
        f = font(F_BOLD, s)
        d.text(((W - f.getlength(t)) / 2, y), t, font=f, fill=c, stroke_width=5, stroke_fill=(0, 0, 0))
    return bg


def build(n):
    base, title = EP[n]
    src = f"out/eleven/{base}.mp4"
    out = f"out/hikaye/hikaye_bolum_{n:02d}.mp4"
    frame = f"{SCR}/f{n}.png"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", "6", "-i", src, "-frames:v", "1", frame], check=True)
    cpng = f"{SCR}/c{n}.png"
    card(frame, n, title, final=(n == 20)).convert("RGB").save(cpng)
    ppng = f"{SCR}/p.png"
    pill().save(ppng)
    fc = (f"[0:v]trim=0:{CLIP},setpts=PTS-STARTPTS[v0];[v0][2:v]overlay=0:1560:enable='gte(t,1)'[v1];"
          f"[1:v]scale={W}:{H},format=yuv420p,trim=0:3,setpts=PTS-STARTPTS,fade=t=in:st=0:d=0.3[v2];"
          f"[v1]format=yuv420p[v1f];[v1f][v2]concat=n=2:v=1:a=0[v];"
          f"[0:a]atrim=0:{CLIP},asetpts=PTS-STARTPTS,afade=t=out:st={CLIP-0.8}:d=0.8[a0];"
          f"anullsrc=r=44100:cl=stereo,atrim=0:3[a1];[a0][a1]concat=n=2:v=0:a=1[a]")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-loop", "1", "-framerate", "30", "-t", "3", "-i", cpng,
                    "-i", ppng, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-r", "30",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", out + ".part.mp4"], check=True)
    os.replace(out + ".part.mp4", out)
    return out


if __name__ == "__main__":
    for n in [int(x) for x in sys.argv[1:]]:
        print(build(n))
