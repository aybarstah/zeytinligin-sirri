import sys
from PIL import Image
import make_main as mm, story
cap = {}
def fake(shots, label, out):
    cap['s'] = shots; cap['l'] = label; return out, 0
mm.render_episode = fake
getattr(mm, "ep" + sys.argv[1])()
shots = cap['s']; bar = story._bar(cap['l'])
frames = []
for s in shots:
    for frac in [0.15, 0.6]:
        t = s.dur * frac
        f = s.render(t, t)
        f.alpha_composite(story._grade()); f.alpha_composite(bar, (0, 0))
        frames.append(f.convert('RGB').resize((270, 480)))
o = Image.new('RGB', (len(frames) * 278, 480), 'white')
for k, f in enumerate(frames): o.paste(f, (k * 278, 0))
o.save(f'chk/main_ep{sys.argv[1]}.png')
ev = story.episode_events(shots)
print([round(s.dur, 1) for s in shots], round(ev['total'], 1))
