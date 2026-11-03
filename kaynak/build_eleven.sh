#!/bin/bash
set -e
cd /home/claude/dt
(python3 make_story.py 1 2 3 > chk/ra.log 2>&1) & p1=$!
(python3 make_story2.py 4 5 6 7 > chk/rb.log 2>&1) & p2=$!
wait $p1; wait $p2
mkdir -p out/eleven
for v in out/B*.mp4; do
  b=$(basename $v .mp4)
  python3 audio.py out/$b.events.json > /dev/null
  ffmpeg -loglevel error -y -i $v -i out/$b.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart out/eleven/$b.part.mp4
  mv out/eleven/$b.part.mp4 out/eleven/$b.mp4
done
echo BUILD_OK
for f in out/eleven/*.mp4; do echo "$(basename $f) $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)"; done
