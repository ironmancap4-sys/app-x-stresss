# One Era — phong cách B (bản đồ + footage điện ảnh)

Video dọc 1080×1920, 30 fps, 257,44 s, 68 shot, dựng bằng `scripts/motion.py`.

1. Nền vệ tinh: `python sat_tiles.py sat07 7 19 97 2 117 img` … (z9: 13.8 104.6 7.8 109.0; z11: 11.75 106.15 9.95 107.4;
   z13: 11.32 106.42 10.6 106.98; z16: 11.025 106.655 10.905 106.745) → `sat_declouds.py` từng ảnh → `proj/assets/maps/`.
2. Google Earth: `node cap.js earth-shots/<shot>.json ge/shots/<shot> 0` (36 khung) → `enc2.sh <shot>`.
3. `python mk_shots.py` → `proj/shots.json` (sửa shot ở đây; phần cuối tự cân tỉ lệ, giữ chữ, bám phách).
4. `python motion.py proj/shots.json proj` → hết cảnh báo "!".
5. `python mk_sfx.py` → `proj/sfx/events.json`; `make_music.py` (100 BPM) rồi dời 0,13 s; `mix_audio.py ... --music`.
6. `npx hyperframes check`, `snapshot`, `render`; `qa_frames.py`, `style_check.py`.

Giới hạn trung thực của bản này: không có video quay thật (Wikimedia/Pexels/Pixabay bị chặn) → footage là Google Earth 3D + ảnh
báo/phối cảnh CĐT; tuyến metro và vị trí ghim tiện ích là sơ đồ minh hoạ (ghi trên màn hình); không có file logo → tường tên.
