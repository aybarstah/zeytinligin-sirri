#!/bin/bash
set -e
cd /home/claude/dt
(python3 make_main.py 1 > chk/rm.log 2>&1; python3 make_story.py 1 2 3 > chk/ra.log 2>&1) & p1=$!
(python3 make_story2.py 4 5 6 7 > chk/rb.log 2>&1) & p2=$!
wait $p1; wait $p2
python3 audio.py out/*.events.json > chk/audio.log
mkdir -p out/sesli
for v in out/B*.mp4 out/S1B*.mp4; do
  b=$(basename $v .mp4)
  ffmpeg -loglevel error -y -i $v -i out/$b.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -shortest -movflags +faststart out/sesli/$b.part.mp4
  mv out/sesli/$b.part.mp4 out/sesli/$b.mp4
done
python3 voice_script.py out out/seslendirme_metni_bolum_1-7.txt
echo BUILD_OK
