# Template: giải thích kinh tế – địa phương (dọc 1080×1920, 30 fps)

Project HyperFrames đã kiểm chứng (video Vĩnh Long 88,6 s, 11/2026). Copy cả thư mục, thay dữ liệu, chạy `python build.py`, rồi render.

## Cấu trúc

| Tệp | Vai trò |
| --- | --- |
| `index.html` | gốc: 6 cảnh + 1 `<audio id="mix">` (giọng đọc + SFX đã trộn) |
| `src/geo.html` | bản đồ vector: toàn quốc → vùng → tỉnh, sông, so sánh, kết nối, cực tăng trưởng, câu hỏi lớn; kết bằng zoom xuyên + hoà 12 khung |
| `src/foot.html` | cảnh quay thật giữa video (2 đoạn), dòng neo |
| `tpl/board.tpl.html` + `rows.py` → `src/board.html` | bảng số tích luỹ trên nền bản đồ tỉnh mờ 35% |
| `src/doc.html` | ảnh bài báo gốc: mở bằng tiêu đề, zoom vào đoạn số, highlight cam 30% |
| `src/earthb.html` | 1 cảnh Google Earth (đã chỉnh màu) + nhãn kiểu A trên vật thể |
| `src/end.html` | 10 s cuối: cảnh quay thật có người, 2 dòng neo thay nhau + 1 thông điệp chốt |
| `design.css`, `fonts.css`, `assets/fonts/` | hệ thiết kế (Be Vietnam Pro, token màu, nhãn A/B, dòng neo, vùng an toàn TikTok) |
| `mapjs.js`, `mapcss.css`, `geo.json` | bản đồ vector; `geo.json` sinh bằng `scripts/geo_build.py` |
| `footage.json` | nguồn video cho `foot`/`end` (F1/F2/E1/E2, media-start, dòng ghi nguồn) |
| `sfx_events.json` | mốc SFX cho `scripts/mix_audio.py` |
| `build.py` | nhúng design/map/geo/footage vào `src/*.html` → `compositions/` |

## Làm video mới

1. `transcribe_vi.py voice.mp3 transcript.json` → mốc từng từ; `ffmpeg -af silencedetect` → khoảng lặng.
2. Đặt lại thời lượng cảnh trong `index.html` (đổi chất liệu ở khoảng lặng); cảnh sau bản đồ bắt đầu sớm 0,4 s để hoà.
3. `geo_build.py config.json` → `geo.json` (tỉnh gộp, sông, dải ven biển, điểm). Sửa `KEYS` camera và các mốc nhãn trong `src/geo.html` theo từ khoá.
4. Số liệu: sửa `ROWS` trong `rows.py` (giá trị theo **báo**, mốc = lúc đọc số), chạy đoạn sinh `src/board.html` (xem cuối `rows.py`/README skill).
5. Tài liệu gốc: `doc_capture.js` → `assets/doc/article.png` + vị trí đoạn số → sửa `#d-hl` và đích zoom trong `src/doc.html`.
6. Footage: tải bản quyền mở, cắt dọc tránh watermark → `assets/foot/*.mp4`, sửa `footage.json`. Google Earth: `earth_capture.js` + `earth_encode.sh`, rồi chỉnh màu (lệnh trong `references/he-thiet-ke.md`).
7. `mix_audio.py voice.mp3 sfx_events.json assets/mix.wav --duration <s>`.
8. `python build.py` → `npx hyperframes check` → snapshot → render → `qa_frames.py` + `style_check.py`.

## Tư liệu không kèm theo (tự tạo lại)
- `assets/mix.wav`: giọng đọc + SFX (`mix_audio.py`, SFX từ `make_sfx.py`).
- `assets/foot/*.mp4`: cảnh quay thật (ví dụ Vĩnh Long dùng "Mekong Floating Markets…" — Le Monde en Vidéo, CC BY 3.0, Wikimedia Commons).
- `assets/earth/s4g.mp4`: Google Earth đã chỉnh màu.
- `assets/doc/article.png`: ảnh bài báo.
- Phông đã kèm sẵn trong `assets/fonts/` (Be Vietnam Pro, OFL).
