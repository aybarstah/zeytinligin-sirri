#!/bin/bash
# usage: ./build_main2.sh 6 7 8 9 10   -> renders, mixes, writes out/eleven/<name>.mp4
cd /home/claude/dt
run() {
  for e in "$@"; do
    out=$(python3 make_main2.py $e 2>chk/m2_$e.err | tail -1)
    f=$(python3 -c "import ast;print(ast.literal_eval('''$out''')[0])")
    b=$(basename "$f" .mp4)
    python3 audio.py out/$b.events.json >/dev/null
    ffmpeg -loglevel error -y -i out/$b.mp4 -i out/$b.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart out/eleven/$b.part.mp4 && mv out/eleven/$b.part.mp4 out/eleven/$b.mp4
    echo "DONE $b $(ffprobe -v error -show_entries format=duration -of csv=p=0 out/eleven/$b.mp4)"
  done
}
args=("$@"); half=$(( (${#args[@]} + 1) / 2 ))
run "${args[@]:0:$half}" &
run "${args[@]:$half}" &
wait
echo ALL_DONE
