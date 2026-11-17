#!/bin/bash
# render_segments.sh <project> <out.mp4> <duration_s> [seg_s=65]
# Render chia đoạn nối tiếp (một render chạy một lúc; lệnh nền bị dừng sau ~2 giờ), ghép không nén lại,
# mux âm thanh đầy đủ assets/mix.wav qua limiter (AAC làm vọt đỉnh), giải mã thử và in độ chênh ở mối nối.
set -e
P="$1"; OUT="$2"; DUR="$3"; SEG="${4:-65}"
cd "$P"; mkdir -p out/seg; : > out/seg/list.txt
i=0; s=0
while python3 -c "import sys; sys.exit(0 if $s < $DUR - 0.01 else 1)"; do
  e=$(python3 -c "print(min($s + $SEG, $DUR))")
  f="out/seg/s$i.mp4"
  if [ ! -s "$f" ]; then npx -y hyperframes@0.9.28 render . -o "$f" --fps 30 --start "$s" --end "$e" > "out/seg/s$i.log" 2>&1; fi
  echo "file 's$i.mp4'" >> out/seg/list.txt; echo "đoạn $i: $s–$e s xong"
  s=$e; i=$((i+1))
done
ffmpeg -v error -y -f concat -safe 0 -i out/seg/list.txt -an -c:v copy out/seg/video.mp4
ffmpeg -v error -y -i out/seg/video.mp4 -i assets/mix.wav -map 0:v -map 1:a -c:v copy -af "alimiter=limit=0.80:level=disabled" -c:a aac -b:a 192k -shortest "$OUT"
ffmpeg -v error -i "$OUT" -f null - && echo "giải mã OK: $OUT"
ffmpeg -hide_banner -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
python3 - "$OUT" "$SEG" "$DUR" <<'PY'
import subprocess, sys, numpy as np
o, seg, dur = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
fr = lambda t: np.frombuffer(subprocess.run(["ffmpeg","-v","error","-ss",str(t),"-i",o,"-frames:v","1","-vf","scale=270:480","-f","rawvideo","-pix_fmt","gray","-"],capture_output=True).stdout,np.uint8).astype(float)
j = seg
while j < dur - 0.1:
    a, b, c = fr(j - .1), fr(j - .033), fr(j + .02)
    print(f"mối nối {j:.0f}s: trong đoạn {abs(b-a).mean():.1f} · qua mối nối {abs(c-b).mean():.1f} (qua mối nối phải ≲ trong đoạn)"); j += seg
PY
