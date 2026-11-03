import os
from PIL import Image, ImageDraw
from brand import *
from characters import muhendis, zeyto, ZW, ZH

S = 1080
OUT = "/home/claude/dt/out/profil/"
os.makedirs(OUT, exist_ok=True)


def bg(c1, c2=None):
    im = Image.new("RGBA", (S, S), c1 + (255,))
    d = ImageDraw.Draw(im)
    if c2:
        d.ellipse([140, 140, S - 140, S - 140], fill=c2)
    return im, d


def head_bust(scale):
    m = muhendis(0, False, 82, 0)
    m = m.crop((40, 20, 560, 760))           # cap to chest
    return m.resize((int(m.width * scale), int(m.height * scale)), Image.LANCZOS)


# A: engineer bust, big and friendly
im, d = bg(OLIVE, (98, 132, 62))
b = head_bust(1.75)
im.alpha_composite(b, ((S - b.width) // 2, 90))
im.convert("RGB").save(OUT + "profil_A_muhendis.png")

# B: engineer + Zeyto
im, d = bg(CREAM, (238, 226, 190))
b = head_bust(1.45)
im.alpha_composite(b, (90, 130))
z = fit(zeyto(GREEN_OLIVE, 1, False, "happy", -6, 1), height=520)
im.alpha_composite(z, (S - z.width - 70, S - z.height - 130))
im.convert("RGB").save(OUT + "profil_B_muhendis_zeyto.png")

# C: notebook logo
im, d = bg(DARK)
d.rounded_rectangle([290, 200, 790, 880], radius=40, fill=OLIVE)
d.rectangle([290, 200, 350, 880], fill=(56, 80, 32))
d.rectangle([700, 200, 735, 940], fill=RED)
d.polygon([(700, 940), (717, 905), (735, 940)], fill=DARK)
d.rounded_rectangle([390, 300, 690, 520], radius=24, fill=CREAM)
draw_olive(d, 510, 420, 62, GREEN_OLIVE)
d.polygon(leaf_poly(590, 380, 130, 46, -30), fill=LEAF)
t1 = text_image("MÜHENDİSİN", 52, CREAM, 500)
t2 = text_image("DEFTERİ", 78, SUN, 500)
im.alpha_composite(t1, (540 - t1.width // 2, 580))
im.alpha_composite(t2, (540 - t2.width // 2, 660))
im.convert("RGB").save(OUT + "profil_C_defter_logo.png")

# preview: as Instagram shows it (circle) at two sizes
prev = Image.new("RGB", (3 * 360 + 40, 470), (255, 255, 255))
pd = ImageDraw.Draw(prev)
mask = Image.new("L", (320, 320), 0)
ImageDraw.Draw(mask).ellipse([0, 0, 319, 319], fill=255)
mask_s = Image.new("L", (90, 90), 0)
ImageDraw.Draw(mask_s).ellipse([0, 0, 89, 89], fill=255)
for k, f in enumerate(["profil_A_muhendis.png", "profil_B_muhendis_zeyto.png", "profil_C_defter_logo.png"]):
    p = Image.open(OUT + f)
    x = 20 + k * 360
    prev.paste(p.resize((320, 320), Image.LANCZOS), (x, 20), mask)
    prev.paste(p.resize((90, 90), Image.LANCZOS), (x + 115, 360), mask_s)
    pd.text((x + 140, 452), "ABC"[k], fill=(0, 0, 0))
prev.save("/home/claude/dt/chk/profil_preview.png")
print("ok")
