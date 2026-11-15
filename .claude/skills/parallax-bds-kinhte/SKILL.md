---
name: parallax-bds-kinhte
description: Dựng video dọc 9:16 (TikTok/Reels/Shorts) về kinh tế, bất động sản, địa phương trong HyperFrames — từ một file giọng đọc có sẵn ra video hoàn chỉnh: bản đồ vector định vị tỉnh, sông, kết nối; cảnh quay thật; bảng số liệu tích luỹ có nguồn báo chính thống; ảnh tài liệu gốc; Google Earth 3D; camera chuyển động liên tục và parallax; hệ thiết kế báo chí kinh tế; vùng an toàn TikTok; âm thanh −14 LUFS. Dùng khi dựng/sửa video giải thích kinh tế – địa phương, giá nhà, dự án, quy hoạch, hạ tầng, hoặc phân tích video mẫu để học phong cách. Vietnamese economic / real-estate explainer videos with continuous camera and parallax.
---

# Video kinh tế – bất động sản – địa phương (HyperFrames, dọc 9:16)

Skill này nằm trên skill chính thức `/hyperframes` (luật render, CLI). Chưa có thì người dùng tự cài: `npx skills add heygen-com/hyperframes`.
Mục tiêu: **mọi câu thoại được CHỨNG MINH bằng hình**, trình bày theo một hệ thiết kế báo chí kinh tế, xem tốt trên TikTok.

## Luật cốt lõi (chi tiết + cách kiểm trong `references/`)

1. **Chứng minh bằng hình**, ≥ 4 chất liệu xen kẽ: bản đồ vector · cảnh quay thật · bảng số tích luỹ trên nền bản đồ · ảnh tài liệu gốc (+ Google Earth 3D minh hoạ). 10–15 s cuối là người hoặc footage thật có chuyển động. → `quy-tac-chuyen-gia.md`
2. **Số liệu từ báo chính thống**, đọc bài gốc, ghi nguồn + ngày trên màn hình; số trên màn hình theo nguồn, không theo bản chép lời (Whisper hay nghe nhầm số) — lệch thì báo người dùng.
3. **Hệ thiết kế**: 1 phông Be Vietnam Pro; 1 màu nhấn cam `#F28C28` trên nền navy; chỉ 2 kiểu nhãn (A gắn vật thể, B khái niệm); không phụ đề — mỗi cảnh 1 "dòng neo" ≤ 7 từ đúng lúc đọc từ khoá; không vàng, không hộp đen. → `he-thiet-ke.md`
4. **Vùng an toàn TikTok**: không chữ/nhãn ở y < 210, y > 1440, và x > 940 khi 700 < y < 1440 (UI ứng dụng che). Chữ sát đáy sẽ bị caption/tên kênh che.
5. **Không mờ**: chữ ≥ 72% trắng có bóng; nét vẽ ≥ 2 px, đủ sáng trên nền navy.
6. **Camera liên tục, parallax thật**: camera không đứng chết; bản đồ nội suy Hermite (vận tốc liên tục); Google Earth/footage là chuyển động thật; chuyển cảnh = whip zoom ngắn (luôn phóng to, không bao giờ thu nhỏ lộ viền) hoặc cắt thẳng ở khoảng lặng; bản đồ → ảnh: zoom xuyên + hoà 12 khung. Mọi chữ tắt trước điểm chuyển. → `camera-rig.md`
7. **Âm thanh**: −14 LUFS, true peak ≤ −1 dBTP; SFX whoosh/pop/riser thấp hơn giọng ≥ 12 dB.

## Quy trình: từ giọng đọc tới video

Template đã kiểm chứng: `templates/kinh-te-dia-phuong/` (đọc `TEMPLATE.md`). Mỗi bước có script trong `scripts/`.

1. **Giọng đọc** → `python scripts/transcribe_vi.py voice.mp3 transcript.json` (mốc từng từ) và `ffmpeg -i voice.mp3 -af silencedetect=noise=-30dB:d=0.25 -f null -` (khoảng lặng; đổi chất liệu ở khoảng > 0,4 s, thiếu thì dùng khoảng dài nhất).
2. **Kiểm chứng số liệu**: tìm bài báo chính thống, đọc toàn văn, lập bảng số (giá trị, đơn vị, nguồn, ngày). Chụp bằng chứng: `node scripts/doc_capture.js <url> "<đầu tiêu đề>" "<chuỗi đoạn 1>" "<đoạn 2>" "<đoạn 3>"`.
3. **Bản đồ**: viết `geo_config.json` (tỉnh gộp theo nghị quyết hiện hành, điểm, sông, trục bờ biển — mẫu trong template) → `python scripts/geo_build.py geo_config.json geo.json`; xem `work/rivers_preview.jpg`.
4. **Hình thật**: footage giấy phép mở (Wikimedia Commons CC, Pexels, Pixabay; không lách giới hạn tải, không giả trình duyệt), cắt dọc tránh watermark, ghi tác giả + giấy phép; Google Earth: `scripts/earth_capture.js` + `scripts/earth_encode.sh`, rồi chỉnh màu về navy (lệnh trong `he-thiet-ke.md`). Chỉ gắn nhãn địa danh đúng chỗ quay; footage nơi khác ghi chung ("Đồng bằng sông Cửu Long").
5. **Dựng (cách nhanh, khuyên dùng)**: viết `storyboard.json` (mỗi cảnh: `map` bản đồ vector + ảnh vệ tinh trong 1 cú máy, `media` video/ảnh, `board` bảng số tích luỹ, `doc` tài liệu gốc; mốc theo từ khoá) → `python scripts/scenegen.py storyboard.json <project>` sinh toàn bộ cảnh theo hệ thiết kế (vào/ra cảnh, chữ tắt trước chuyển cảnh, chặn số đếm từ 0 đã tự áp). Project cần `fonts.css`, `design.css`, `vmap.js`, `vector_map.css`, `geo.json`. Ví dụ đầy đủ: `templates/one-era/` (257 s, 23 cảnh).
   **Dựng (thủ công)**: copy template, cài phông (`design/install_fonts.sh <project>` nếu thiếu), sửa thời lượng cảnh trong `index.html`, `KEYS` camera + mốc nhãn trong `src/geo.html`, `ROWS` trong `rows.py` (`python rows.py`), đích zoom/highlight trong `src/doc.html`, `footage.json`; `python build.py`.
6. **Âm thanh**: `python scripts/make_sfx.py` → `sfx/`; sửa `sfx_events.json` theo mốc chuyển cảnh/nhãn/số; `python scripts/mix_audio.py voice.mp3 sfx_events.json assets/mix.wav --duration <s>` (script tự đo và báo nếu chưa đạt −14 LUFS/−1 dBTP).
7. **Kiểm tra** (bắt buộc trước khi giao):
   - `npx hyperframes check --json` — sửa hết lỗi (cảnh báo nhãn phân đoạn 24 px là chủ đích).
   - `npx hyperframes snapshot --at <mốc từ khoá>` — nhìn từng khung.
   - render → `python scripts/qa_frames.py out.mp4` (vùng chết, mây/mảng trắng, khung tối/nhoè, đứng yên > 6 s) và `python scripts/style_check.py out.mp4` (contact sheet 1 khung/giây có tô đỏ vùng TikTok che + quét màu vàng). Mọi cờ phải xem ảnh và giải thích; sai → sửa, render lại.
   - Nén giao: `ffmpeg -i out.mp4 -c:v libx264 -b:v 5000k -maxrate 6500k -bufsize 10000k -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k final.mp4`, rồi giải mã thử toàn bộ (`ffmpeg -v error -i final.mp4 -f null -`) trước khi gửi. Không để hai tiến trình ghi cùng một file.

## Phong cách B: "bản đồ + footage" điện ảnh, nhịp nhanh

Khi người dùng muốn nhịp nhanh, thư viện hiệu ứng bản đồ (bay xuyên mây, zoom nhoè, nghiêng 3D, ranh phát sáng, tuyến có xe chạy,
vòng bán kính, ghim) xen footage full-bleed, màu theo nghĩa: đọc `references/motion-library.md`. Dựng bằng
`python scripts/motion.py shots.json <project>` (sinh composition + `SHOTLIST.md` + bộ kiểm luật nhịp/lặp/tỉ lệ). Project cần
`fonts.css`, `motion.css` (design/), `vmap2.js`, `geo.json`, nền vệ tinh (`sat_tiles.py` → `sat_declouds.py`). Ví dụ đầy đủ:
`templates/one-era-motion/` (68 shot, 257 s). Luật 3 (1 màu nhấn) của phong cách A được thay bằng bảng màu theo nghĩa.

## Phong cách C: một camera, một bản đồ sống (Animated Map Infographic)

Khi người dùng muốn MỘT chuyến bay liên tục, không cắt cảnh, thông tin mọc lên từ bản đồ (vẽ ranh, khối 3D, vòng bán kính,
tuyến có xe chạy, ghim, tô màu, mốc thời gian…): đọc `references/flight-style.md`, dựng bằng
`python scripts/flight.py flight.json <project>` (vmap3.js, design/flight.css). Tự kiểm: ≤ 3 cắt cứng, camera không đứng yên
> 1 s, footage ≤ 3 s/lần và ≤ 20%, không hai chương liền nhau cùng kiểu V1–V10, mỗi kiểu ≤ 20%; sinh `CAMLOG.md`.
Ví dụ: `templates/one-era-flight/`, `templates/ha-tang-flight/` (bản v2: chống rung đo theo khung, mờ chuyển động theo vận tốc, huy hiệu icon Material Symbols, thẻ logo, cửa sổ ảnh, nhật ký tài sản).

## Học phong cách từ video mẫu (khi người dùng đưa video tham khảo)

`python scripts/analyze_refs.py "<thư mục video mẫu>" --out phan-tich` → `SUMMARY.md`, `STYLE_DRAFT.md`, contact sheet, đồ thị tốc độ camera; số đo của 5 video mẫu gốc nằm trong `references/style-mau.md` (camera chạy ≥ 85% thời gian, cảnh 2,5–4 s, transition zoom-blur…). Dùng chính script này để đo lại video của mình.

## Templates

| Template | Dùng cho |
| --- | --- |
| `templates/kinh-te-dia-phuong/` (**mặc định**) | giải thích kinh tế – địa phương từ giọng đọc: bản đồ vector + footage + bảng số + tài liệu gốc + Google Earth |
| `templates/one-era-flight/` | phong cách C: `mk_flight.py` → flight.json (một camera 71 keyframe, 15 chương V1–V10), `prep_geo.py`, `mk_sfx3.py` |
| `templates/one-era-motion/` | phong cách B: `mk_shots.py` → shots.json (68 shot, đủ M1–M10/T1–T5/F1–F3/D1–D6), `mk_sfx.py`, ảnh Google Earth `earth-shots/` |
| `templates/one-era/` | ví dụ dựng bằng `scenegen.py`: dự án BĐS (nguồn cung CBRE → vị trí → quy mô → đối tác → giao thông → tiện ích → sản phẩm → lộ trình) |
| `templates/map-dive-parallax/` | video BĐS dọc kiểu bay vào bản đồ, rig camera 3D parallax (tuyến neon, ghim, thẻ dự án) |
| `templates/ngang-parallax/` | bản 16:9: skyline nhiều lớp, nhãn giá gắn toà nhà, biểu đồ camera bay dọc |

## Tham chiếu

| Cần | Đọc |
| --- | --- |
| 8 nhóm quy tắc chuyên gia + cách kiểm | `references/quy-tac-chuyen-gia.md` |
| Phong cách B: thư viện hiệu ứng, màu theo nghĩa, nhịp, SFX theo sự kiện | `references/motion-library.md` |
| Phong cách C: một camera liên tục, lớp trên bản đồ, V1–V10, zoom-through | `references/flight-style.md` |
| Hệ thiết kế, vùng an toàn TikTok, độ rõ tối thiểu | `references/he-thiet-ke.md`, `design/` |
| Rig camera 3D, parallax, Google Earth, nối take | `references/camera-rig.md` |
| Phong cách đo từ video mẫu | `references/style-mau.md`, `references/analysis.md` |
| Từ vựng hình ảnh BĐS/kinh tế, màu tăng/giảm, chữ tiếng Việt | `references/genre-grammar.md` |

## Scripts

| Script | Việc |
| --- | --- |
| `transcribe_vi.py` | chép lời tiếng Việt + mốc từng từ (faster-whisper) |
| `doc_capture.js` | chụp bài báo gốc + vị trí các đoạn số |
| `geo_build.py` | tỉnh gộp, sông dò theo ảnh vệ tinh, dải ven biển, đường/kênh/ranh dự án theo toạ độ → `geo.json` |
| `scenegen.py` | storyboard JSON → toàn bộ project HyperFrames theo hệ thiết kế |
| `vmap.js` | bản đồ vector tổng quát (lớp tỉnh/đường/kênh/ảnh vệ tinh theo toạ độ, nối điểm, vòng sóng, nhãn A/B, camera Hermite) |
| `vector_map.js/.css` | bản đồ vector của template Vĩnh Long; `.css` dùng chung |
| `earth_capture.js`, `earth_encode.sh` | quay Google Earth web từng khung, ghép 30 fps |
| `make_sfx.py`, `mix_audio.py` | SFX tổng hợp; trộn giọng + SFX + nhạc (ducking) + chuẩn hoá loudness có kiểm chứng |
| `make_music.py` | nhạc nền có phách rõ + `beats.json` để cắt theo phách |
| `motion.py`, `vmap2.js`, `design/motion.css` | phong cách B: shots.json → project + SHOTLIST.md + kiểm luật |
| `flight.py`, `vmap3.js`, `design/flight.css` | phong cách C: flight.json → một composition bản đồ + HUD + footage + CAMLOG.md + kiểm luật |
| `sat_tiles.py`, `sat_declouds.py` | ghép ảnh vệ tinh Esri theo mức zoom; xoá mây + chỉnh màu nền |
| `qa_frames.py`, `style_check.py` | kiểm lỗi render; contact sheet + vùng TikTok + màu cấm |
| `analyze_refs.py` | đo video mẫu / video của mình |
