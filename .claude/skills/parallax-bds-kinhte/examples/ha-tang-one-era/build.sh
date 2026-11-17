#!/bin/bash
# build.sh <thư mục dựng> [--render]
# Dựng LẠI video mẫu "hạ tầng quanh One Era" từ đầu trên máy bất kỳ và chứng minh nó giống bản gốc:
#   1) kiểm môi trường  2) tải + xử lý đầu vào (kiểm hash điểm ảnh)  3) sinh project  4) âm thanh
#   5) hyperframes check  6) so 20 khung chuẩn (SSIM ≥ 0,97)  7) (--render) render chia đoạn + mờ chuyển động
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"; SKILL="$(cd "$HERE/../.." && pwd)"
B="$(mkdir -p "$1" && cd "$1" && pwd)"; PY=${PYTHON:-python3}
echo "== 1. môi trường"; $PY "$SKILL/scripts/doctor.py"
echo "== 2. đầu vào"; $PY "$HERE/fetch_inputs.py" "$B" || echo "!! có đầu vào KHÁC — vẫn dựng tiếp, xem bước 6"
echo "== 3. project"
cp "$HERE"/project/*.json "$HERE/project/fonts.css" "$B/"; cp -r "$HERE/project/icons" "$HERE/project/sfx" "$B/"
cp "$HERE/project/vo.mp3" "$B/assets/vo.mp3"
cp "$SKILL/design/motion.css" "$SKILL/design/flight.css" "$SKILL/scripts/vmap3.js" "$B/"
$PY "$SKILL/scripts/flight.py" "$B/flight.json" "$B"
echo "== 4. âm thanh"
$PY "$SKILL/templates/ha-tang-flight/mk_sfx3.py" "$B/flight.json" "$B/sfx/events.json"
(cd "$B" && $PY "$SKILL/scripts/make_music.py" music.wav --dur 130.7 --bpm 92 >/dev/null)
$PY - "$B/music.wav" "$HERE/inputs.json" <<'PY'
import hashlib, json, sys
ok = hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest() == json.load(open(sys.argv[2]))["audio"]["music"]["sha256"]
print(("KHỚP" if ok else "KHÁC (khác phiên bản numpy?)") + "  music.wav")
PY
(cd "$B" && rm -f assets/mix.wav && $PY "$SKILL/scripts/mix_audio.py" assets/vo.mp3 sfx/events.json assets/mix.wav --duration 130.6 --music music.wav | tail -1)
echo "== 5. hyperframes check"; (cd "$B" && npx -y hyperframes@0.9.28 check . 2>&1 | grep -E "Check (passed|failed)")
echo "== 6. so khung chuẩn"; $PY "$SKILL/scripts/verify_golden.py" check "$B" "$HERE/golden"
if [ "$2" = "--render" ]; then
  echo "== 7. render"; bash "$SKILL/scripts/render_segments.sh" "$B" out/raw.mp4 130.6
  (cd "$B" && $PY "$SKILL/scripts/mb_post.py" flight.json out/raw.mp4 out/mb.mp4 --shutter 180 && \
   ffmpeg -v error -y -i out/mb.mp4 -i assets/mix.wav -map 0:v -map 1:a -c:v libx264 -b:v 5000k -maxrate 6500k -bufsize 10000k -pix_fmt yuv420p -r 30 \
     -movflags +faststart -af "alimiter=limit=0.80:level=disabled" -c:a aac -b:a 192k -shortest out/final.mp4 && echo "video: $B/out/final.mp4")
fi
