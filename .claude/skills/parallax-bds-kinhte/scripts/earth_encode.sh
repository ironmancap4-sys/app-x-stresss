#!/bin/bash
# Ghép khung Google Earth (10 fps) thành MP4 30 fps 1080x1920, nội suy chuyển động, all-intra để HyperFrames seek chính xác.
# Dùng: earth_encode.sh <thư mục khung> <file ra .mp4> [fps vào, mặc định 10]
set -e
IN="$1"; OUT="$2"; FPS="${3:-10}"
ffmpeg -loglevel error -y -framerate "$FPS" -i "$IN/f%04d.jpg" \
  -vf "scale=1080:1920:flags=lanczos,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,eq=contrast=1.05:saturation=1.05" \
  -c:v libx264 -preset medium -crf 17 -g 1 -pix_fmt yuv420p "$OUT"
