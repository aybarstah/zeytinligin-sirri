#!/bin/bash
# usage: ./build_s2.sh make_s2:ep1 make_notes:n8 ...  -> out/eleven/<name>.mp4 (2 parallel streams)
cd /home/claude/dt
run() {
  for job in "$@"; do
    mod=${job%%:*}; fn=${job##*:}
    out=$(python3 -c "import $mod as m; print(m.$fn())" 2>chk/b_$fn.err | tail -1)
    f=$(python3 -c "import ast;print(ast.literal_eval('''$out''')[0])" 2>/dev/null)
    if [ -z "$f" ]; then echo "FAIL $job $(tail -3 chk/b_$fn.err)"; continue; fi
    b=$(basename "$f" .mp4)
    python3 audio.py out/$b.events.json >/dev/null
    ffmpeg -loglevel error -y -i out/$b.mp4 -i out/$b.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart out/eleven/$b.part.mp4 && mv out/eleven/$b.part.mp4 out/eleven/$b.mp4
    echo "DONE $b $(ffprobe -v error -show_entries format=duration -of csv=p=0 out/eleven/$b.mp4)"
  done
}
args=("$@"); A=(); B=()
for i in "${!args[@]}"; do if (( i % 2 == 0 )); then A+=("${args[$i]}"); else B+=("${args[$i]}"); fi; done
run "${A[@]}" & run "${B[@]}" & wait
echo ALL_DONE
