import sys, os
sys.path.insert(0, "/home/claude/dt")
from PIL import ImageDraw, ImageFont
import make_ai, make_main

MAP1 = ["S01", "S01", "S02", "S02", "S03", "S03", "S04", "S05", "S06", "S06", "S06", "S07",
        "S08", "S08", "S08", "S09", "S10", "S11", "S11", "S10", "S11", "S12", "S12", "S13"]


def page_text(im):
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(make_main.LORA_I, 78)
    try:
        f.set_variation_by_name("Bold Italic")
    except Exception:
        pass
    cx, cy = im.width / 2, im.height * 0.44
    for i, ln in enumerate(["Ağaçları dinlersen,", "onlar da seni dinler.", "— Deden"]):
        tw = f.getlength(ln)
        x = cx - tw / 2 + (120 if i == 2 else 0)
        d.text((x, cy + i * 110), ln, font=f, fill=(35, 38, 70, 235))


if __name__ == "__main__":
    img_dir = sys.argv[1]
    out = sys.argv[2]
    lines = make_ai.capture_lines(make_main, "ep1")
    assert len(lines) == len(MAP1), len(lines)
    print(make_ai.build(lines, MAP1, img_dir, "BÖLÜM 1", out,
                        end=("Bölüm 2 yarın 20:00", "Ulu'nun Sınavı", "Takip et, hikâyeyi kaçırma!"),
                        overlays={"S02": page_text}))
