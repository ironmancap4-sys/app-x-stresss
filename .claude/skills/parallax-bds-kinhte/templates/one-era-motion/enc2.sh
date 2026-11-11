#!/bin/bash
# enc2.sh <tên shot> : khung Google Earth (6 fps -> 30 fps nội suy, ~5,7 s cho 36 khung) -> chỉnh màu navy -> proj/assets/ge/
# Chạy từ thư mục làm việc có ge/shots/<tên>/ và proj/. SKILL = đường dẫn tới skill.
SKILL=${SKILL:-.claude/skills/parallax-bds-kinhte}
$SKILL/scripts/earth_encode.sh ge/shots/$1 ge/$1_raw.mp4 6 && ffmpeg -loglevel error -y -i ge/$1_raw.mp4 -vf "eq=saturation=0.75:contrast=1.08:gamma=0.97,colorbalance=rs=-0.06:gs=-0.02:bs=0.06:rm=-0.02:bm=0.02" -c:v libx264 -crf 17 -g 1 -pix_fmt yuv420p proj/assets/ge/$1.mp4 && echo "OK $1"
