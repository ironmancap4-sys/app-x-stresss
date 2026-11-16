# SKILL TRỌN GÓI: parallax-bds-kinhte

Một file duy nhất chứa toàn bộ skill để đưa cho bất kỳ AI nào. Thứ tự: SKILL.md (quy trình + chọn phong cách) → references (luật và cách kiểm) → design (CSS) → scripts (mã nguồn) → templates. Muốn dùng lại: tạo đúng các file theo đường dẫn ghi trên mỗi khối mã.

Bỏ ra khỏi file này (có trong bản zip/thư mục): phông chữ .woff2 (tải lại bằng `design/install_fonts.sh`) và các file dữ liệu sinh tự động lớn (geo.json, shots.json, flight.json) — chạy lại script mk_*.py / geo_build.py để tạo.

## FILE: SKILL.md

```markdown
---
name: parallax-bds-kinhte
description: Dựng video dọc 9:16 (TikTok/Reels/Shorts) về kinh tế, bất động sản, địa phương trong HyperFrames — từ một file giọng đọc có sẵn ra video hoàn chỉnh: bản đồ vector định vị tỉnh, sông, kết nối; cảnh quay thật; bảng số liệu tích luỹ có nguồn báo chính thống; ảnh tài liệu gốc; Google Earth 3D; camera chuyển động liên tục và parallax; 3 phong cách (giải thích chậm · bản đồ + footage nhịp nhanh · một camera bay liên tục trên bản đồ sống với icon, thẻ logo, cửa sổ ảnh, chống rung, mờ chuyển động); hệ thiết kế báo chí kinh tế; vùng an toàn TikTok; âm thanh −14 LUFS. Dùng khi dựng/sửa video giải thích kinh tế – địa phương, giá nhà, dự án, quy hoạch, hạ tầng, hoặc phân tích video mẫu để học phong cách. Vietnamese economic / real-estate explainer videos with continuous camera and parallax.
---

# Video kinh tế – bất động sản – địa phương (HyperFrames, dọc 9:16)

Skill này nằm trên skill chính thức `/hyperframes` (luật render, CLI). Chưa có thì người dùng tự cài: `npx skills add heygen-com/hyperframes`.
Mục tiêu: **mọi câu thoại được CHỨNG MINH bằng hình**, trình bày theo một hệ thiết kế báo chí kinh tế, xem tốt trên TikTok.

## Chọn phong cách trước khi dựng

| Phong cách | Khi nào | Công cụ | Đọc |
|---|---|---|---|
| A — giải thích chậm (mặc định) | video kinh tế – địa phương kể chuyện bằng bản đồ + bảng số + tài liệu | `scenegen.py` / template `kinh-te-dia-phuong` | phần dưới |
| B — bản đồ + footage điện ảnh | nhịp nhanh 2,5–4 s/shot, nhiều hiệu ứng M/T/F/D, màu theo nghĩa | `motion.py` | `references/motion-library.md` |
| C — một camera, một bản đồ sống | bay liên tục không cắt cảnh, thông tin mọc lên từ bản đồ, icon, logo, cửa sổ ảnh | `flight.py` + `mb_post.py` | `references/flight-style.md` |

Người dùng đưa một đặc tả phong cách (role/prompt dài) → đối chiếu với bảng trên, chọn phong cách gần nhất rồi áp đúng các luật kiểm của nó.

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
| `mb_post.py` | phong cách C: mờ chuyển động theo vận tốc camera sau render (màn trập 180°) |
| `flight.py`, `vmap3.js`, `design/flight.css` | phong cách C: flight.json → một composition bản đồ + HUD + footage + CAMLOG.md + kiểm luật |
| `sat_tiles.py`, `sat_declouds.py` | ghép ảnh vệ tinh Esri theo mức zoom; xoá mây + chỉnh màu nền |
| `qa_frames.py`, `style_check.py` | kiểm lỗi render; contact sheet + vùng TikTok + màu cấm |
| `analyze_refs.py` | đo video mẫu / video của mình |
```

## FILE: references/analysis.md

````markdown
# Phân tích video mẫu bằng `scripts/analyze_refs.py`

```bash
pip install opencv-python-headless numpy
python scripts/analyze_refs.py "<thư mục hoặc file>" --out phan-tich [--width 480] [--step 2]
```

Windows: đường dẫn có dấu cách/dấu tiếng Việt phải đặt trong ngoặc kép; script tự xử lý tên file Unicode. `--step 2` nhanh gấp đôi (đủ dùng cho video 30/60 fps).

## Kết quả

| File | Nội dung |
| --- | --- |
| `SUMMARY.md` | bảng tổng + danh sách cảnh từng video |
| `STYLE_DRAFT.md` | nháp `STYLE.md`: dòng `[ĐO]` đã điền, dòng `[NHÌN]` để điền bằng mắt |
| `summary.json` | toàn bộ số liệu, máy đọc được |
| `<video>/sheet-NN.jpg` | mỗi cảnh một hàng: khung đầu / giữa / cuối + nhãn chuyển động |
| `<video>/motion.png` | tốc độ pan (vàng) và zoom (xanh) theo thời gian; nền xanh lá = camera đang chạy; vạch đỏ = cut |

Xem `sheet-*.jpg` và `motion.png` bằng công cụ đọc ảnh trước khi viết `STYLE.md`.

## Các chỉ số

| Chỉ số | Nghĩa | Dùng để |
| --- | --- | --- |
| `continuity_moving_frac` | % thời gian (trừ khung cắt) camera đang pan/zoom/xoay vượt ngưỡng | mục tiêu tối thiểu cho video của mình |
| `stops_total` | số lần camera đứng yên ≥ 0,4 s | thể loại này thường rất thấp |
| `avg_shot_sec` | độ dài cảnh trung bình | đặt khoảng cách key và độ dài take |
| `cuts_on_motion_frac` | % cut xảy ra khi camera vẫn đang chạy | cao → nối take bằng match-move |
| `match_move_cuts_frac` | % cut mà hướng ra/vào cùng chiều (cos > 0,7) | quy tắc nối take |
| `parallax` (mỗi cảnh) | sai lệch của các điểm so với một chuyển động phẳng duy nhất, chia cho độ lớn chuyển động | ≥ 0,18 → có nhiều lớp độ sâu |
| `layer_spread` | (p90 − p10)/trung vị của vận tốc dọc hướng di chuyển | ≈ chênh lệch tốc độ giữa lớp gần và lớp xa; ≥ 0,6 là parallax rõ |
| `pan_pct_w_s`, `zoom_pct_s` | tốc độ pan (% chiều rộng khung/giây) và zoom (%/giây) | khoảng tốc độ cho `KEYS` |
| `enters_moving` / `exits_moving`, `dir_in` / `dir_out` | cảnh bắt đầu/kết thúc khi camera đang chạy, và theo hướng nào | thiết kế mối nối |
| `palette` | 6 màu chủ đạo theo tỉ lệ diện tích | dòng màu trong `STYLE.md` |

Hướng: `vx` là hướng **hình** trôi; hình trôi sang trái (`vx` < 0) nghĩa là camera đi sang phải.

## Giới hạn — kiểm lại bằng mắt

- Chữ/đồ hoạ HUD đứng yên chiếm nhiều diện tích sẽ kéo tốc độ đo xuống và có thể bị tính là "parallax" (lớp đứng yên so với nền chạy). Đối chiếu với sheet.
- Video có người/xe chuyển động nhiều cũng làm tăng chỉ số parallax.
- Hoà tan dài hoặc whip rất nhanh có thể bị đếm thành 2 cut hoặc bị bỏ sót; `motion.png` cho thấy rõ.
- Nhãn "push-in" có thể là zoom quang học (không có parallax) hoặc dolly thật (có parallax): xem cột parallax cùng hàng.
- Video sau khi tải lại từ mạng xã hội bị nén mạnh: dùng `--width 640` cho ổn định hơn.

## Kiểm định video của mình

Chạy lại script trên bản render của mình cùng thư mục `--out` khác, rồi so từng chỉ số với mẫu. Đây là tiêu chí nghiệm thu "camera liên tục + parallax" trong `SKILL.md` §5.
````

## FILE: references/camera-rig.md

````markdown
# Camera rig: phối cảnh, API, công thức move, nối take

## 1. Mô hình

```
#w-stage   perspective: P (mặc định 1000px) — ống kính
 └ #w-cam  transform-style: preserve-3d — cả thế giới; CHỈ script đặt transform
    ├ .w-layer[data-depth=3000]  trời
    ├ .w-layer[data-depth=1800]  skyline xa
    ├ ...
    ├ .w-layer[data-depth=0]     mặt phẳng tiêu cự (biểu đồ, bản đồ, nhãn chính)
    └ .w-layer[data-depth=-350]  tiền cảnh (cột, cây, mây) — đi nhanh nhất
HUD (ngoài #w-stage)            chữ khoá màn hình, không đi theo camera
```

- Lớp ở độ sâu `d` được đặt `translateZ(-d) scale((P+d)/P)`: lúc camera ở gốc, mọi thứ hiện đúng kích thước đã thiết kế, nên có thể bố trí từng lớp như bố trí trên khung 1920×1080.
- Camera pan `x` (đo trên mặt phẳng tiêu cự) làm điểm ở độ sâu `d` trôi `x·P/(P+d)` px. Hệ số parallax của lớp = `P/(P+d)`: d = −350 → 1,54 (nhanh hơn camera); 0 → 1; 900 → 0,53; 3000 → 0,25.
- Dolly `z` (> 0 là tiến vào) phóng lớp theo `P/(P+d−z)`: lớp gần phóng nhanh hơn lớp xa → parallax theo chiều sâu khi push-in. Lớp có `P+d−z` < 0,3P mờ dần, < 0,12P biến mất (bay xuyên qua thay vì chọc vào ống kính).
- `orbit`/`tilt` xoay thế giới quanh điểm đang nhìn. Lớp là các tấm phẳng, nên giữ |orbit| ≤ 6–8°, quá mức sẽ thấy mép tấm (hiệu ứng "sách pop-up").

## 2. API của rig

Hai template dùng chung rig. `templates/map-dive-parallax/compositions/dive.html` (dọc, bay vào bản đồ) điều khiển dolly bằng **zoom**:

```js
const at = (t, lx, ly, zoom, tilt = 0, orbit = 0) => ...; // nhắm điểm (lx,ly) của bản đồ (depth 0)
const KEYS = [
  at(0, 560, 980, 0.85),          // mở rộng, đã đang chạy
  at(3.5, 300, 700, 1.8, 6, -2),  // xuyên mây, lặn xuống
  at(10.5, 690, 1280, 2.5, 10, 3) // tới dự án, bản đồ nghiêng 10°
];
```

- `zoom` = độ phóng của mặt bản đồ, nội suy theo `log(zoom)` (lặn đều như flycam), quy ra dolly `z = P·(1 − 1/zoom)`.
- `tilt` (rotateX) nghiêng bản đồ như flycam nhìn xiên, ≤ 12°: ghim/thẻ ở depth âm "đứng" trên mặt đất và trượt so với bản đồ → parallax ngay cả trên bản đồ phẳng. `orbit` (rotateZ) xoay quanh điểm nhìn, ≤ 6°.
- Giới hạn: lớp depth `d` phải giữ `P + d − z ≥ 0,3P` → với nhãn −30, thẻ −60 thì zoom ≤ ~2,8. Lặn sâu hơn (châu lục → phố) dùng video `bake-basemap` làm lớp bản đồ, hoặc ghép nhiều ảnh bản đồ chi tiết tăng dần (ảnh chi tiết đặt chồng đúng vị trí, hiện dần khi zoom tới).

`templates/ngang-parallax/compositions/world.html` dùng `z` trực tiếp:

```js
const P = 1000;           // khớp với CSS perspective
const DUR = 20;           // khớp data-duration của host
const FLOAT = 3;          // rung "flycam" tất định (px), 0 = tắt
const look = (d, lx, ly) => ...;  // đặt điểm (lx,ly) của lớp depth d vào giữa khung
const KEYS = [
  { t: 0,  x: -300, y: -120, z: -150, orbit: -4, tilt: 2 },
  { t: 8,  ...look(300, 3000, 430), z: 380, orbit: 3 },
  { t: 20, x: 5240, y: 40, z: -250, orbit: -3, tilt: 1 },
];
```

- Mỗi kênh (x, y, z, orbit, tilt) nội suy **Hermite đơn điệu** (Fritsch–Carlson): đi qua đúng các key, vận tốc liên tục, không vọt lố. Một kênh đổi chiều tại key thì vận tốc kênh đó về 0 ở đó — sắp key sao cho lúc ấy kênh khác vẫn chạy.
- Key đầu: camera *đã đang chạy* khi video mở (độ dốc = đoạn đầu). Key cuối: đáp nhẹ về 0. `stop: true` ở một key = cố ý dừng mọi kênh tại đó.
- Thời gian camera chạy bằng một tween duy nhất `clock.t: 0 → DUR` (ease `none`) trên timeline; mọi thứ là hàm của thời gian nên render tất định, seek ngược xuôi đều đúng.
- Nhãn/biểu đồ nằm trong lớp thì animate bằng GSAP như thường (đã đặt sẵn `fromTo`). Không animate `transform` của `.w-layer` hay `#w-cam` bằng GSAP — rig sở hữu chúng.

## 3. Tốc độ mặc định (khi không có video mẫu)

| Thông số | Giá trị |
| --- | --- |
| Pan trên mặt phẳng tiêu cự | 8–25 %W/s (150–480 px/s ở 1920) — đo trên màn hình, lớp xa chậm hơn |
| Dolly vào vật thể | z +200…+450 trong 3–5 s |
| Kéo lùi kết | z −200…−300 trong 2,5–4 s |
| Orbit | 0,5–1,5 °/s, tổng ≤ 8° |
| Khoảng cách giữa key | 2,5–4 s; key trùng với cụm lời dẫn |
| Khoảng cách tới vật thể khi tới nơi | vật thể chiếm 35–60% chiều cao khung |

Kiểm tra bằng `analyze_refs.py` trên bản render: pan/zoom trung vị nằm trong khoảng p50–p90 của video mẫu.

## 4. Công thức các kiểu move

| Move | Cách đặt key |
| --- | --- |
| **Push-in vào toà nhà/dự án** | key trước: toàn cảnh, z ≈ 0; key tới: `look(d_toà_nhà, ...)`, z +300…+400, orbit +2…+4°. Nhãn giá nổi lên ở 70–85% quãng đường. |
| **Truck ngang skyline** | x tăng đều qua 2–3 key, y gần như giữ; đặt 1 vật tiền cảnh (depth −300…−450) cắt ngang khung giữa đường để parallax rõ. |
| **Crane lên lộ toàn cảnh** | y từ +250 về −100, tilt +3° → 0, z lùi −100; dùng cho hook hoặc kết. |
| **Bay xuyên mây/tiền cảnh** | lớp mây depth −150…−250; z vượt `P + d − 0,3P` → lớp mờ đi khi camera xuyên qua; lớp sau lộ ra. |
| **Orbit quanh mô hình dự án** | orbit −5° → +5° trong 5–8 s, x bù nhẹ để vật thể giữ giữa khung. |
| **Đi dọc biểu đồ** | biểu đồ ở depth 0; camera x chạy từ đầu tới cuối đường giá trong lúc `strokeDashoffset` vẽ ra, cùng thời lượng, để "ngòi bút" luôn gần giữa khung. Số cuối nổi lên khi camera tới đỉnh. |
| **Dive vào bản đồ** | bản đồ thật dựng sẵn thành video bằng `scripts/bake-basemap.mjs` của `/hyperframes` (take riêng); ghim/nhãn vẽ SVG phía trên; nối với take thành phố bằng match-move theo z. |
| **Kéo lùi kết** | z về −200…−300, orbit nhẹ ngược chiều trước đó; câu kết HUD đáp và đứng yên tới hết. |

## 5. Tài sản (ảnh tách lớp)

- **Nguồn:** ảnh/video Google Earth 3D (§8), ảnh flycam, ảnh/phối cảnh dự án, ảnh đường phố có quyền dùng; hoặc minh hoạ vector vẽ theo lớp. Ảnh nơi thật thì dùng ảnh thật, không vẽ lại.
- **Tách lớp:** Photoshop (Select Subject/Sky), `rembg`, hoặc bản đồ độ sâu (Depth Anything) rồi cắt theo ngưỡng thành 3–5 PNG nền trong suốt. **Vá phần nền** phía sau mỗi lớp trước (content-aware/generative fill), nếu không camera trượt sẽ lộ lỗ.
- **Độ phân giải cần có:** ảnh ở lớp `d` hiện lớn tới `(P+d)/(P+d−z_max)` lần kích thước thiết kế. Ví dụ depth 0, z_max = 400 → 1,67×: khung 1920 cần ảnh ≥ 3200 px. Ảnh rất rộng (skyline dài) cắt thành các ô ≤ 8000 px.
- **Phủ đủ:** mỗi lớp rộng hơn vùng camera quét + 30–50% dự phòng cho dolly lùi/orbit/float; lớp trời và đất kéo dài thoải mái.
- **Đặt ảnh:** `<img src="assets/...">` (không có `/` ở đầu) đặt `position:absolute` trong `.w-layer`, toạ độ theo khung thiết kế của lớp. Ảnh không cần `class="clip"` — nó sống suốt take.
- **Phối cảnh khí quyển:** lớp càng xa càng sáng, ít tương phản, ngả màu trời (thêm một lớp sương mỏng 15–25% opacity giữa xa và giữa). Đây là thứ làm parallax "đọc" được.

Độ sâu gợi ý: trời 2500–4000 · skyline xa 1500–2000 · sương 1200–1400 · khối giữa 700–1000 · vật thể chính 200–400 · mặt phẳng số liệu 0 · tiền cảnh −250…−450.

## 6. Nối nhiều take (match-move)

Một take = một file scene. Mối nối phải liên tục về chuyển động:

0. **Kiểu chính của video mẫu: zoom-blur xuyên tâm.** Dùng shader `cinematic-zoom` của `@hyperframes/shader-transitions` (`npx hyperframes catalog --tag transition --json`), đặt đúng lúc cả hai take đang lao vào cùng chiều (take A zoom vào cuối, take B bắt đầu bằng zoom vào). Thời lượng 0,4–0,7 s. Shader chụp cảnh thành texture: snapshot ngay trước/sau mối nối để chắc parallax 3D vẫn hiển thị đúng. Khoảng 1 lần mỗi 8–15 s (`style-mau.md`).
1. **Cùng vận tốc:** key cuối take A đặt `carry: true` (giữ nguyên vận tốc, không đáp), key đầu take B mặc định đã đang chạy; chỉnh để tốc độ trên màn hình và hướng hai bên khớp nhau (đo bằng `analyze_refs.py`: cột "Vào/ra khi đang chạy", `dir_out`/`dir_in`).
2. **Che mối nối bằng vật thể:**
   - *Foreground wipe:* một cột/toà nhà tiền cảnh lướt qua che kín khung; cắt đúng lúc che kín; take B mở ra bằng một vật tiền cảnh cùng màu đang lướt đi cùng hướng.
   - *Zoom xuyên:* take A dive vào cửa sổ/màn hình/ô bản đồ đến khi màu của nó lấp khung; take B bắt đầu từ chính màu đó và lùi ra.
   - *Whip:* lướt nhanh 0,2–0,3 s có motion blur ngang, hai bên cùng hướng.
3. Không crossfade giữa hai thế giới; hard cut thuần ≤ 1/3 số mối nối.

Rig hiện chạy cả take từ một đồng hồ; khi tách take, sao chép file scene (`dive.html` / `world.html`), đổi id scene (`data-composition-id`, host id, khoá `window.__timelines`) và tiền tố id phần tử cho duy nhất.

## 7. Lỗi thường gặp

| Triệu chứng | Nguyên nhân / cách sửa |
| --- | --- |
| Hết parallax, mọi lớp trôi như một tấm | Có `opacity<1`, `filter`, `overflow:hidden`, `clip-path`, `mix-blend-mode` trên `#w-stage`/`#w-cam` → Chrome làm phẳng 3D. Đưa hiệu ứng xuống từng lớp con. |
| `check` báo `dead_stretch` khi camera đang chạy | `data-layout-ignore` trên `#w-stage`/`#w-cam`; dùng `data-layout-allow-overflow`/`-overlap` thay thế. |
| Một lớp phóng to khổng lồ rồi lật ngược | z vượt quá `P + d`; rig đã làm mờ ở 0,3P→0,12P, nhưng hãy đặt key để không vượt. |
| Lộ mép lớp khi kéo lùi/orbit | lớp chưa đủ rộng; mở rộng 30–50% và snapshot ở các key cực trị. |
| Chữ trong thế giới bị nhoè | chữ bị phóng > 1,3× do dolly; thiết kế ở kích thước cuối, hoặc chuyển sang HUD/depth 0. |
| Giật ở mốc key | hai key quá gần với vận tốc khác nhau; giãn key ≥ 2 s hoặc bỏ key thừa. |
| Render khác preview | có `Math.random`/`Date.now`/`requestAnimationFrame`; mọi thứ phải là hàm của `clock.t`. |
| Motion blur (`data-motion-blur`) làm mất 3D | blur dùng filter trên phần tử; chỉ bật sau khi snapshot xác nhận parallax còn nguyên. |

## 8. Cảnh 3D kiểu Google Earth / Google Maps

Các cảnh "flycam" trong video mẫu thực ra là camera bay trên **mô hình 3D ảnh thật của Google** (toà nhà, cầu, cao tốc dựng 3D). Parallax ở đây là thật, vì đây là hình học 3D. Có hai cách đưa vào HyperFrames:

**A. Google Earth Studio → video (nên dùng trước).**
1. Tạo project ở Google Earth Studio (trình duyệt Chrome, đăng nhập Google, miễn phí).
2. Đặt keyframe camera theo `CAMERA.md`:
   - camera đã chạy sẵn khi mở cảnh;
   - không dừng giữa chừng;
   - ease mềm ở 2 đầu, hoặc để tuyến tính nếu cảnh nối bằng zoom-blur.
3. Xuất chuỗi ảnh ở khung 1080×1920 và 30 fps, rồi ghép thành video bằng lệnh `ffmpeg -framerate 30 -i anh_%03d.jpeg -c:v libx264 -crf 16 -pix_fmt yuv420p canh.mp4` (mẫu tên ảnh `%03d` phải khớp tên file Earth Studio xuất ra).
4. Đưa vào take dạng `<video class="clip" muted playsinline src="assets/canh.mp4">`, đặt full khung.
5. Đặt ghim, nhãn, tuyến neon bằng HTML phía trên:
   - Earth Studio có xuất "3D tracking data", là vị trí trên màn hình của các điểm đánh dấu, dùng cho After Effects. Đổi dữ liệu này sang JSON theo từng khung, rồi cho nhãn bám theo bằng một tween `onUpdate` đọc toạ độ ở frame hiện tại.
   - Chưa có bộ chuyển đổi thì chỉ hiện nhãn lúc camera chậm, rồi chỉnh vị trí bằng snapshot.
6. Ghi nguồn trên màn hình theo yêu cầu của Google ("Google Earth" kèm nhà cung cấp dữ liệu), chữ nhỏ trên nền tối, và gắn `data-layout-ignore` cho dòng này.

**A2. Tự động quay Google Earth web (đã dùng thật cho video Vĩnh Long, 11/2026).**
- `scripts/earth_capture.js` mở Google Earth web trong Chromium headless (Playwright, WebGL qua SwiftShader), chọn Basemap "Clean" (không nhãn, không đường, không biên giới), đưa `#earth-canvas` lên trên giao diện, rồi với mỗi khung: đổi URL `@lat,lng,alt,dist,fov,head,tilt` bằng `history.replaceState` + `popstate` (camera nhảy tức thì, không tải lại trang), chờ cố định ~1,8 s cho tile, chụp.
- Tốc độ thực tế: ~8 s/khung ở dpr 1,5 với 2–3 luồng song song trên 4 nhân → quay 10 fps rồi `scripts/earth_encode.sh` nội suy lên 30 fps (minterpolate, hình mượt, không vỡ khi camera chạy đều).
- Chụp thử góc máy trước bằng chế độ `list` (dpr 1), xem ảnh, chọn góc tránh lỗ lưới 3D (vùng nước/ven sông đôi khi có mảng tối).
- Một cảnh = nội suy tuyến tính từ `from` tới `to` (dist theo log) → camera chạy đều suốt cảnh; nối các cảnh bằng zoom-blur.

**B. Render trực tiếp Google Photorealistic 3D Tiles trong trang (nâng cao, chưa kiểm thử trong skill này).**
- Dùng CesiumJS hoặc three.js kèm 3d-tiles-renderer, với Map Tiles API key. Dựng camera từ chính `KEYS` của rig, nên mọi chuyển động, nhãn và tuyến dùng chung một hệ toạ độ và luôn khớp tuyệt đối.
- Vẽ theo `hf-seek` (`/hyperframes` → `references/runtimes.md`) và dùng `e.detail.waitUntil(...)` để chờ tile tải xong ở mỗi frame. Nếu không chờ, frame sẽ bị thiếu mảnh và mỗi lần render ra một kiểu.
- Cần mạng khi render và có tính phí theo lượt gọi tile. Chỉ chọn cách này khi cần nhãn bám chính xác tuyệt đối hoặc phải dựng rất nhiều cảnh tự động.

Dù chọn cách nào, cảnh 3D vẫn phải đạt cột "Mục tiêu" trong `style-mau.md`: chạy liên tục, vào và ra cảnh khi camera đang lao, và nối với đoạn bản đồ bằng `cinematic-zoom` cùng chiều.
````

## FILE: references/flight-style.md

```markdown
# Phong cách C — "một camera, một bản đồ sống" (Animated Map Infographic)

Dùng khi người dùng muốn cảm giác bay liên tục trên MỘT bản đồ, thông tin "mọc lên từ mặt đất" thay vì cắt cảnh.
Dựng bằng `scripts/flight.py` + `scripts/vmap3.js` + `design/flight.css` (cùng `motion.css` cho màu theo nghĩa).
Ví dụ đầy đủ: `templates/one-era-flight/` (260 s, 15 chương, 0 cắt cứng).

## 1. Luật một camera

- Cả video là MỘT composition bản đồ dài suốt video; camera = keyframe `[t, lat, lng, Z, pitch, bearing]`, nội suy Hermite
  đơn điệu trên cả 5 kênh (không giật, không dừng gắt). Cắt cứng tối đa 3 (khai trong `cuts`), tốt nhất là 0.
- Không bao giờ đứng yên: `flight.py` lấy mẫu camera theo cửa sổ 1 s — phải đổi Z ≥ 0,004, hoặc nghiêng/quay ≥ 0,15°,
  hoặc lia ≥ 1,5 px. Điểm cực trị (Z lên rồi xuống) làm camera chững lại: xếp keyframe đơn điệu qua đoạn giữ.
- Kiểu di chuyển: fly-to (thu nhỏ → lướt → phóng to, 2–3,5 s), đẩy/kéo giữa các tỉ lệ (quốc gia → thành phố → phường →
  dự án), nghiêng 0 → 40–50°, quay chậm (bearing ≤ 90° mỗi lần — thực tế giữ ≤ 30° để góc khung không lộ), bám đầu tuyến.
- Thế giới (Z ≈ 3,2): giữ Z ≥ 3 để Mercator phủ kín chiều cao 1920 px; bearing và pitch về 0.
- Nghiêng mạnh làm lộ mép mặt phẳng: SVG được nới (`PAD` = 1100 trái/phải, 2800 phía trên) + lớp sương chân trời theo pitch.

## 2. Thông tin là các lớp

- Mọi lớp gắn toạ độ thật, kế thừa chuyển động camera; sự kiện trong `ev`: `draw` (vẽ nét), `show`/`dim`/`hide`
  (mờ 40% khi không phải tâm điểm), `grow` (khối 3D mọc), `tint` (độ đậm khối — KHÔNG dùng opacity vì làm phẳng 3D).
- Lớp có thể tích luỹ trong chương rồi dọn trước chương sau; cuối video kéo ra cho thấy mọi lớp cùng lúc.
- Tối đa 2 chuyển động chính cùng lúc (camera + 1 lớp). Thẻ số lớn tối đa 2 trên màn hình.
- Nhãn, ghim, chữ mặt đất nằm trên mặt bản đồ nhưng xoay ngược bearing để luôn đọc thẳng.
- Khi đang nghiêng: đặt nhãn PHÍA TRÊN điểm neo (ly âm). Nhãn phía dưới bị phối cảnh phóng to và rơi khỏi vùng an toàn.
- Vòng tròn/vòng bán kính/điểm nóng vẽ bằng HTML (`.ring`, `.disc`) — SVG `<circle>` vỡ hình khi phóng lớn trong 3D.

## 3. Mười kiểu trực quan (mỗi chương một kiểu chính, không lặp ở hai chương liền nhau, mỗi kiểu ≤ 20%)

| V | Kiểu | Khai báo |
|---|---|---|
| V1 | ranh tự vẽ, phát sáng, rồi phủ 35–50% | layer `fill:true,len:true` + `draw` + `show {id}-fill` |
| V2 | vùng hành chính sáng lên / biến hình, vùng bên cạnh mờ | `prov:` + `show` + `dim to .4` |
| V3 | tuyến có đầu chạy (xe đạp, máy bay), nhãn thời gian ở cuối | `links`/`lines` + `draw` + `movers` |
| V4 | vòng đẳng thời/bán kính (km hoặc phút đi bộ) | `rings:[{pt,km:[.4,.8],t,out}]` |
| V5 | ký hiệu tỉ lệ (hình tròn đúng diện tích) | `circles:[{pt,r_m,kind}]` (r = √(S/π)) |
| V6 | khối 3D mọc từ mặt đất | `blocks` + `grow` + `tint` |
| V7 | chùm ghim tiện ích | `pins` |
| V8 | tô màu theo giá trị / lớp nhiệt + chú giải | `prov:` fill hoặc `circles heat:true` + `hud.legend` |
| V9 | mốc thời gian trên bản đồ, theo thứ tự | `labels` ngày + `links kind:"yel"` nối các mốc |
| V10 | thẻ số lớn có đường dẫn tới vị trí (≤ 2 thẻ) | `labels` `xl:true` + `count` |

## 4. Footage

Chỉ ghé ≤ 3 s/lần, tổng ≤ 20%, bằng zoom-through: camera đẩy vào đúng điểm (Z +0,7 trong ~2 s), footage hoà vào 0,65 s
có nhoè, chuyển động chậm, rồi hoà ra; camera kéo ra từ CÙNG vị trí. Không cắt từ bản đồ sang footage.

## 5. Màu, chữ, nền

Màu theo nghĩa của `motion.css` (cam hành chính, cyan dự án + nước, xanh lá công viên, hồng tím giao thông, vàng khoảng cách/ghim).
Nền vệ tinh làm tối 20%, giảm bão hoà 15% (Brightness .8, Color .85, Contrast 1.05), CÙNG một chỉnh màu cho mọi mức zoom.
Mỗi mức (`sat_tiles.py`) phải phủ rộng hơn khung hình lớn nhất ở mức đó — kể cả khi đang chuyển — nếu không sẽ lộ mép
hình chữ nhật (đặt `show:[Za,Zb]` muộn hơn hoặc ghép rộng hơn). Xoá mây bằng `sat_declouds.py`.
Một họ Be Vietnam Pro; nhãn bản đồ 34–40 px; thẻ số 132 px; tiêu đề chương 58–120 px nằm trên mặt bản đồ; nguồn 19 px ở y≈1396.

## 6. Âm thanh

Một nền nhạc liên tục (`make_music.py`), whoosh khi camera di chuyển lớn, pop cho nhãn/ghim/số, swell trước lộ diện và
zoom-through — `templates/one-era-flight/mk_sfx3.py` sinh từ flight.json. SFX −12 dB dưới giọng; kết quả −14 LUFS, ≤ −1 dBTP.

## 7. Tự kiểm trước khi xuất

`python flight.py flight.json proj` in "!" nếu: > 3 cắt cứng; footage > 3 s/lần hoặc > 20%; chương liền nhau trùng kiểu;
kiểu > 20%; quay > 90° một lần; camera gần như đứng yên > 1 s. Sinh `CAMLOG.md` (timecode, chương, kiểu V, chuyển động camera,
lớp trên bản đồ, footage + bảng keyframe). Rồi `npx hyperframes check` (không lỗi chồng chữ), `snapshot` từng chương
(xem kỹ: mép mặt phẳng khi nghiêng, nhãn bị phối cảnh phóng to, chữ bị khối 3D che, mép ảnh vệ tinh), render, `qa_frames.py`.

Bẫy đã gặp: `#root` của motion.css có nền navy — composition HUD/footage phải để nền trong suốt; đồng hồ camera chạy trước
các tween trong GSAP khi seek, nên tween đổi dữ liệu (chiều cao khối) phải tự gọi lại `frame()`.

## 8. Bản v2 — ổn định, minh hoạ, tài sản thật (áp dụng từ video "Vành đai 3 · QL13 · metro")

**Chống rung** (`flight.py` tự kiểm, tính trên từng khung 30 fps):
- Tốc độ mặt đất ≤ 25 px/khung (lia + zoom + quay + nghiêng quy đổi ra px ở nửa bề ngang khung). Đường xa → bay cung ở độ cao lớn.
- Mỗi đoạn giữ khung (≥ 1 s, < 6 px/khung) chỉ có MỘT kiểu trôi đơn điệu, đổi chiều ≤ 10 lần/5 s; trôi < 1,5 px/khung quá 1,2 s là lỗi
  (gây lăn tăn mái nhà trên điện thoại) → khoá hẳn camera (`allow_lock: true`, keyframe trùng nhau) và để lớp phủ chuyển động.
  Mẹo: viết chương dạng khoá → MỘT cú máy rõ → khoá; tránh keyframe trung gian lệch nhẹ (Hermite sinh cực trị → bò chậm).
- Nghiêng > 35° tối đa 4 s liên tục (khoảnh khắc "hero"); đọc số liệu ở 0–35°.
- Nền vệ tinh làm mềm Gaussian 0,8 px trước khi dùng; không bao giờ làm nét.
- Mờ chuyển động: render KHÔNG lọc trong trình duyệt, rồi `python scripts/mb_post.py flight.json raw.mp4 out.mp4 --shutter 180`
  — mỗi khung lấy vận tốc camera từ đúng đường Hermite, kernel đường thẳng ≥ 16 mẫu theo hướng chuyển động trên màn hình,
  vệt L = vận tốc × 180/360; L < 2 px giữ nguyên (khung giữ/trôi chậm sắc nét); dòng nguồn và đoạn footage giữ sắc; 30 fps không đổi.
  Đã thử: `data-motion-blur` của HyperFrames không thấy camera vẽ bằng thuộc tính SVG (`motion_blur_no_movers`); lọc feGaussianBlur
  trong trang trên cảnh 3D làm render chậm ~7 lần (6 s video mất 985 s). Mờ sau render chỉ mất ~0,1 s/khung.
- Đo `CAMLOG.md`: bảng "Các đoạn giữ khung" (từ–đến, kiểu trôi lia/zoom/quay/nghiêng/khoá, px/khung, số lần đổi chiều).

**Hệ icon** — một họ duy nhất: Material Symbols Rounded (fill), npm `@material-symbols/svg-400` (Apache-2.0); chép SVG cần dùng
vào `proj/icons/<tên>.svg`. Nhãn `icon:"<tên>"` → huy hiệu tròn 84–96 px, glyph trắng trên màu lớp, viền trắng, glow; bật 0 → 110% → 100%
trong 0,35 s. Mọi con số có icon (diện tích→landscape, tiền→payments, căn→apartment, ngày→calendar_month, cự ly/thời gian→route/schedule,
tiến độ→construction, xong→check_circle, chờ→hourglass_top, người→groups, metro→subway, ô tô→directions_car, máy bay→flight).
Chú giải dùng huy hiệu (`items: [[màu, chữ, icon]]`), không ô màu nhỏ. Kiểm: khoảng trống icon > 6 s, ảnh > 20 s.

**Thẻ logo tổ chức** — `logo:"assets/logo/x.svg"` (thẻ trắng bo góc, logo 66% bề rộng, tên + vai trò). Thứ tự tìm: trang chính thức →
press kit → Wikimedia Commons → ảnh đại diện mạng xã hội chính thức. Không vẽ lại, không AI, không chụp màn hình có nền. Không tải được
sau mọi bước → `logo:"", mono:"ABC"` (huy hiệu chữ) và GHI vào `assets` + báo người dùng. Không lách giới hạn tải (Wikimedia 429 → chờ, thử lại thưa, rồi bỏ).

**Cửa sổ ảnh** — `photo:"assets/img/x.jpg"` (+ `w,h`, `text:"Ảnh: <nguồn>"`): thẻ bo góc trượt lên từ ghim, ảnh đẩy chậm 12%, bản đồ
vẫn thấy xung quanh, 1,5–3 s. Ảnh báo < 1080 px chỉ dùng ở cửa sổ, không full-bleed. Đặt thẻ PHÍA TRÊN neo khi camera nghiêng
(phần dưới khung bị phối cảnh phóng to và đè dòng nguồn ở y≈1396).

**Nhật ký tài sản** — khai `assets: [{name,url,res,used,note}]` trong flight.json → bảng "Tài sản tải về" trong CAMLOG.md.
Chữ tối thiểu 36 px (trừ dòng nguồn 19 px).
```

## FILE: references/genre-grammar.md

```markdown
# Ngữ pháp hình ảnh: bất động sản & kinh tế

Giá trị mặc định khi không có video mẫu. Có `STYLE.md` từ video mẫu thì `STYLE.md` thắng.

## Mỗi loại thông tin → một vật thể trong thế giới

Chọn "hình" trước khi chọn hiệu ứng; các câu giống nhau phải ra các hình khác nhau.

| Thông tin | Vật thể trong thế giới | Camera làm gì |
| --- | --- | --- |
| Giá/m², % tăng của một dự án | nhãn giá cắm trên nóc toà nhà (world-locked), đếm số 1,2–1,6 s | push-in tới toà nhà, nhãn nổi ở cuối đường |
| So sánh giá các khu | các toà/cột cao theo giá đứng thành hàng trong thế giới | truck ngang dọc hàng cột |
| Giá theo thời gian | đường giá là "con đường" ở depth 0 | đi dọc đường giá khi nó tự vẽ |
| Vị trí, khoảng cách (km tới trung tâm, metro, vành đai) | bản đồ vệ tinh thật + ghim + đường đo | dive từ trên cao xuống, ghim xuất hiện khi camera dừng chậm |
| Quy hoạch, hạ tầng mới | lớp bản đồ tương lai phủ lên ảnh hiện tại (wipe theo đường) | crane lên để thấy toàn tuyến |
| Cung – cầu | hai nhóm khối nhà/người hội tụ hoặc tách ra | dolly lùi để thấy toàn bộ |
| Lãi suất, tín dụng | một con số rất lớn ở depth 0, các lớp đồng tiền/giấy tờ trôi phía sau | push-in vào con số |
| Chu kỳ thị trường | đường sóng chạy qua các "trạm" năm | truck ngang, mỗi trạm một nhãn |
| Hiểu lầm vs sự thật | câu sai bị gạch, câu đúng in đè | camera không đổi hướng, chỉ dolly nhẹ |

Tránh: slide gạch đầu dòng, ba thẻ xếp hàng, lưới KPI, biểu đồ tròn, mọi số đếm cùng lúc, số không nguồn.

## Màu

- Ngữ nghĩa thị trường Việt Nam (chứng khoán, cũng là thói quen khán giả): **xanh lá = tăng, đỏ = giảm, vàng = tham chiếu/đứng giá**, tím = trần, xanh lam = sàn. Khi video nói về giá BĐS tăng, màu nhấn ấm (vàng/cam) hoặc xanh lá đều được — giữ một quy ước cho cả video và không dùng đỏ cho "tăng".
- Một màu nhấn duy nhất mang nghĩa; phần còn lại trung tính. Nền tối xanh-đêm hoặc sáng giấy tuỳ video mẫu.
- Gradient tuyến tính toàn khung trên nền tối dễ bị banding khi nén H.264: dùng radial hoặc nền đặc + quầng sáng cục bộ.

## Chữ tiếng Việt

- Font phải có bộ dấu tiếng Việt đầy đủ. Có sẵn trong HyperFrames và hỗ trợ tiếng Việt qua Google Fonts: Montserrat, Inter, Roboto, Open Sans, Oswald, Playfair Display, Nunito, EB Garamond. Font khác (Be Vietnam Pro, SVN-…) cần `@font-face` trỏ tới file trong `assets/fonts/`.
- Luôn snapshot một dòng thử có "ữ ặ ỡ ẫ ự Đ" ở cỡ lớn để chắc dấu không vỡ/chồng.
- Số: `font-variant-numeric: tabular-nums`; dấu thập phân là dấu phẩy (12,4%), phân cách nghìn bằng dấu chấm (1.250 tỷ); đơn vị: "triệu/m²", "tỷ đồng".
- Tiêu đề 4–9% chiều cao khung, 1–2 dòng; chữ phụ ≥ 28 px (sàn đọc được trên điện thoại). Một từ nhấn màu.

## Nhịp

- Hook trong 3 s đầu: một câu hỏi hoặc một con số lớn trên toàn cảnh đang chuyển động.
- Mỗi cụm lời dẫn ≈ một chặng camera (2,5–4 s). Chữ đọc được giữ ≥ 0,5 s + 0,3 s/từ.
- Nhãn và chữ xuất hiện khi lời dẫn nhắc tới, không bày sẵn từ đầu cảnh.
- Kết: kéo lùi + một câu chốt, giữ ≥ 2 s.

## Âm thanh

- Nhạc nền (bed) cả video; whoosh nhẹ ở các cú lướt nhanh/foreground wipe, "tick" khi số đếm đáp. Âm thanh bắt đầu sớm hơn hình 40–190 ms với hành động phải "trúng nhịp".
- Theo `/hyperframes` → `references/sound.md` và `/media-use` cho việc lấy nhạc/giọng.
```

## FILE: references/he-thiet-ke.md

```markdown
# Hệ thiết kế: báo chí kinh tế, tối giản, sang

Áp cho mọi video "giải thích kinh tế – địa phương". Một phông, một màu nhấn, hai kiểu nhãn. Mã: `design/design.css` (dán vào `<style>` của mọi scene, cùng `fonts.css` sinh bởi `design/install_fonts.sh`), bản đồ: `scripts/vector_map.css/.js`.

## Phông: chỉ Be Vietnam Pro (đủ dấu tiếng Việt), nạp từ file
| Vai trò | Độ đậm | Cỡ | Ghi chú |
| --- | --- | --- | --- |
| Dòng neo (tiêu đề lớn) | 800 | 64–72 px (mặc định 68) | IN HOA, giãn +1%, 1–2 dòng, mỗi dòng ≥ 2 từ, `white-space: nowrap` từng dòng |
| Số liệu | 800 | 88–96 px | `font-variant-numeric: tabular-nums` |
| Nhãn bản đồ/ảnh (kiểu A) | 600 | 30–34 px (mặc định 32) | bóng mềm, không hộp |
| Mô tả dưới số | 500 | 28–30 px | trắng 88% |
| Nhãn phân đoạn trên cùng | 600 | 24 px | IN HOA, giãn +8%, kính mờ |
| Chân trang nguồn | 500 | 20 px | trắng 72%, đặt dưới nhãn phân đoạn |
Cấm phông tròn/hoạt hình, cấm phông thứ hai.

## Màu (`#root` khai báo biến)
- Nền: navy `#0E1A2B` → `#13243A` (gradient), có lớp chấm 7 px rất mờ để không có mảng phẳng.
- **Màu nhấn duy nhất: cam `#F28C28`**: tỉnh chính (đục 80%), từ khoá nhấn trong dòng neo (`<em>`), icon nét, vạch/vòng sóng, viền thẻ khái niệm, chữ tăng trưởng.
- Chữ: `#FFFFFF`, trắng 88%, trắng 72% (không mờ hơn).
- Trung tính: xám xanh `#8A97A8` — tỉnh lân cận/so sánh, đường kết nối phụ, vùng nền.
- Sông: xanh ngọc giảm sáng 20% (`#2B8E93` quầng, `#8FBFBC` lõi).
- Tăng trưởng: chữ cam + `▲`, không nền (cấm tag xanh lá đặc).
- **Cấm vàng** (`#ffd23f`…), cấm hộp đen đặc, cấm nền xanh dương đặc cho nhãn phân đoạn.

## Thành phần
- `.seg` nhãn phân đoạn: nền trắng 10%, viền trắng 20%, bo 999 px, `backdrop-filter: blur(10px)`.
- `.anchor` dòng neo: ≤ 7 từ, 1 dòng neo cho 1 ý của cảnh, hiện đúng lúc giọng đọc nói từ khoá; `.low` = đáy (bottom 300 px, trong vùng gradient), `.mid` = giữa (chỉ trên nền bản đồ tối). Không có phụ đề chạy theo lời.
- `.la` **Kiểu A — nhãn gắn vật thể** (mọi địa danh): chấm 10 px + đường dẫn 2 px + chữ 32 px bóng (0 0 12px đen 50%); chấm đặt đúng vật thể; đường dẫn đưa chữ ra chỗ trống (ra ngoài tỉnh, không đè sông). Trên bản đồ dùng `data-at/data-lx/data-ly/data-align`, `vector_map.js` tự dựng.
- `.lb` **Kiểu B — thẻ khái niệm** (Vùng đệm?, Cực tăng trưởng, Bản lề kết nối): viền cam 2 px, nền navy 70%, bo 8 px, chữ trắng IN HOA 28 px.
- `.foot` chân trang nguồn.
- `.gtop`/`.gbot` gradient navy 0→85% trên 18% / dưới 22% khung cho mọi ảnh/video, để chữ trắng đọc được mà không cần hộp.

## Vùng an toàn TikTok / Reels / Shorts (bắt buộc)
Giao diện ứng dụng che một phần khung 1080×1920. **Không đặt chữ, số, nhãn, vật thể đang được chỉ vào** trong:
| Vùng | Toạ độ | Bị che bởi |
| --- | --- | --- |
| Trên | y < 210 | thanh "Đang follow / Dành cho bạn", tìm kiếm |
| Dưới | y > 1440 | tên kênh, caption, nhạc, thanh tiến trình |
| Cột phải | x > 940 khi 700 < y < 1440 | avatar, tim, bình luận, lưu, chia sẻ |
Vị trí chuẩn trong `design.css`: nhãn phân đoạn `top: 230px`; chân trang nguồn `top: 300px` (ngay dưới nhãn phân đoạn, không để ở đáy); dòng neo `.low` `bottom: 520px` (đáy chữ ở y ≈ 1400), `.mid` `top: 760px`; mọi khối nội dung lề phải ≥ 140 px (`right: 150px` cho dòng neo, bảng số rộng 860 px từ x = 70, trang báo 880 px). Nhãn bản đồ: chỉnh camera (lệch tâm) để tỉnh và nhãn dưới tỉnh nằm trên y = 1440. `style_check.py` tô đỏ các vùng này trên contact sheet; không chữ nào được nằm trong vùng đỏ.

## Độ rõ tối thiểu (không để chữ và nét vẽ quá mờ)
- Chữ: không dưới 72% trắng (chân trang 72%, mô tả 88%), cỡ ≥ 20 px; chữ trên ảnh/video luôn có bóng đậm (`0 0 12px rgba(0,0,0,.7)`) và nằm trên gradient navy.
- Nét bản đồ: ranh giới ≥ 2 px, màu đủ sáng trên nền navy (`#4F6688`–`#5A7194`); đường kết nối/hành lang ≥ 5 px màu `#B3BECB`; sông lõi `#B5DEDB` 4 px + quầng 14 px; đường dẫn nhãn kiểu A 3 px.
- Lớp làm mờ có chủ đích (bản đồ nền 35% sau bảng số, nền tối sau câu hỏi lớn) chỉ dùng phía sau nội dung chính, không dùng cho chính nội dung cần đọc.

## Ảnh/video
- Google Earth: chỉnh màu trước bằng ffmpeg (không dùng CSS filter):
  `eq=saturation=0.75:contrast=1.08:gamma=0.97,colorbalance=rs=-0.06:gs=-0.02:bs=0.06:rm=-0.02:bm=0.02` (giảm bão hoà 25%, kéo tối về navy, tăng tương phản nhẹ).
- Footage thật: cắt dọc tránh logo watermark, ghi tác giả + giấy phép ở `.foot`; chỉ gắn nhãn kiểu A khi vật thể đứng yên trong khung.
- Chuyển bản đồ → ảnh: zoom xuyên vào tâm tỉnh + hoà màu 12 khung (cảnh sau bắt đầu sớm 0,4 s, opacity 0→1), không cắt thẳng.

## Đồng bộ
- Mọi chữ (dòng neo, nhãn, nhãn phân đoạn, chân trang) tắt hết **trước** khung chuyển cảnh/điểm cắt.
- Ảnh tài liệu giữ tới khi giọng đọc nói xong câu nhắc tới nó; mở bằng toàn bộ tiêu đề, zoom chậm vào đúng đoạn số vừa đọc, highlight cam 30%. Đặt trang lùi vào trong thẻ để zoom không cắt chữ ở mép.
- Bảng số: căn giữa ≤ 920 px, không thẻ nền; icon nét cam 44 px | số trắng 88 px + đơn vị 32 px trắng 75% | mô tả 28 px; đường kẻ trắng 10%; dòng mới hiện cùng lúc với số (fade + trượt lên 20 px), đếm 0,8 s **từ 40% giá trị** (không bao giờ hiện 0); bản đồ tỉnh phóng to ở nền, mờ 35%.

## Kiểm tra cuối
`python scripts/style_check.py out.mp4` → contact sheet 1 khung/giây + cờ màu vàng. Soát từng ô: không chữ nào trong vùng đỏ (TikTok che); tối đa 1 dòng neo + 1 nhãn phân đoạn + nhãn A/B; không hộp đen, không vàng, không phông thứ hai, không chữ còn mờ sang cảnh sau. Sai → sửa và render lại.
```

## FILE: references/motion-library.md

```markdown
# Phong cách B — "bản đồ + footage" điện ảnh (motion.py)

Dùng khi người dùng muốn nhịp nhanh, hiệu ứng bản đồ đa dạng xen footage thật (kiểu motion designer). Phong cách A
(scenegen.py, 1 màu nhấn cam, dòng neo) vẫn là mặc định cho video giải thích chậm. Hai phong cách KHÔNG trộn trong một video.

## Nhịp (bộ kiểm tra trong motion.py tự soát)

- Shot trung bình 2,5–4 s; không shot nào > 6 s trừ khi cứ ≤ 1,5 s có yếu tố mới (đánh dấu `"busy": true`).
- Không quá 2 cảnh bản đồ liên tiếp, không quá 3 footage liên tiếp.
- Tỉ lệ mục tiêu ~50% bản đồ · ~40% footage/render full-bleed · ≤ 10% thẻ số liệu/ảnh tài liệu.
- Cắt theo nhịp lời đọc; điểm cắt cách phách nhạc ≤ 0,2 s thì kéo vào phách (mk_shots.py làm tự động).
- Montage chữ 0,5–0,9 s/ảnh cho danh sách (`montage`).

## Thư viện hiệu ứng — mỗi shot khai `fx`

Không ID nào lặp ở hai shot liền nhau (trừ T5, F1, F2, C1, DOC); không ID nào chiếm > 15% thời lượng; dùng đủ mọi ID.

| ID | Hiệu ứng | Khai báo trong shots.json |
|---|---|---|
| M1 | bay xuyên mây mở đầu | `clouds:[t0,t1]` (bản đồ hoặc footage) |
| M2 | zoom có nhoè chuyển động vùng → quận → ranh | `keys` đổi Z nhanh + `zoomBlur:true` |
| M3 | nghiêng/quay 3D 30–45° | `tilt:[t0,t1,a0,a1]`, `orbit:[...]` (SVG tự nới rộng để mặt phẳng phủ kín khung) |
| M4 | vẽ ranh 1 s rồi phủ màu 35–50%, glow | layer `len:true, fill:true` + `draw` + `show {id-fill}` |
| M5 | chữ phối cảnh nằm trên mặt đất | `ground:[{at,text,t,d,size}]` |
| M6 | tuyến A→B có chấm đầu + nhãn | `links` + `draw` (+ `movers`) |
| M7 | vòng bán kính 5/10/15 km | `rings:[{pt,lat,t,km:[5,10,15]}]` (km thật theo vĩ độ) |
| M8 | thả ghim lệch 0,15 s, nảy | `pins:[{at,text,t,left}]` |
| M9 | lần theo sông/đường có vật chạy (xe, metro, thuyền) | `movers:[{path,t,d,icon:"car|train|boat"}]` |
| M10 | ranh cũ ↔ mới biến hình | hiện lớp cũ, `hide` nét cũ, `draw` ranh mới |
| T1 | zoom xuyên vào footage đúng chỗ | `enter:"T1"` |
| T2 | vật bắc cầu (máy bay) bay ngang | `enter:"T2"` |
| T3 | whip pan có nhoè | `enter:"T3"`, `whipDir:"L|R"` |
| T4 | lộ hình trong mặt nạ ranh dự án rồi nở ra | `enter:"T4"` (shot trước phải là bản đồ; cần `site` top-level) |
| T5 | cắt cứng (mặc định) | — |
| DIS | hoà hình thường — tối đa 3 lần | `enter:"DIS"` |
| F1 | footage/render full-bleed (không letterbox, không viền mờ) | `media` mp4/jpg, `object-fit: cover` |
| F2 | ảnh tĩnh luôn chuyển động | `move: push|pull|panL|panR|panU|panD` — đổi kiểu giữa các render |
| F3 | chữ động có glow + viền, phóng/nhoè vào | `kw:[{t,d,lines,pos,accent}]` (`*từ` = màu nhấn) |
| D1 | số lớn toàn màn hình, đếm lên 0,8 s | `big:{t,d,num,dec,unit,label}` hoặc `big.text` |
| D2 | thanh tiến độ quy mô | `bar:{...}` |
| D3 | số liệu gắn vào bản đồ | `labels` trên bản đồ |
| D4 | danh sách xếp chồng — tối đa 2 lần, ≤ 8 s, số ≥ 56 px | `stack` |
| D5 | timeline | `timeline` |
| D6 | tường đối tác/logo | `wall` |
| C1 | chú thích có đường dẫn trên footage (không thuộc thư viện, được lặp) | `callouts` |
| DOC | trích đoạn bài báo gốc có tô sáng | `doc` |

## Màu theo NGHĨA (motion.css) — trên nền vệ tinh tối, giảm bão hoà

| Màu | Nghĩa |
|---|---|
| cam `#F28C28` | vùng hành chính |
| cyan `#2FD3E0` | ranh dự án + mặt nước |
| xanh lá `#4ADE80` | công viên, cây xanh |
| hồng tím `#E04BD6` | giao thông, kết nối |
| vàng `#FACC15` | bán kính, khoảng cách, ghim tiện ích |

Nét 4–6 px có glow; phủ 35–50%. Giữ đúng nghĩa cả video (đừng dùng cyan cho chữ chung chung).

## Chữ

Một họ Be Vietnam Pro. Chữ động/tiêu đề ExtraBold 90–130 px IN HOA; số lớn 120–160 px; nhãn bản đồ 34–40 px bóng mềm,
không hộp đen; nhãn phân đoạn 26 px; nguồn 18–20 px trắng 60%. Không chữ quan trọng nào < 34 px; không dồn góc trên trái.
Thời gian giữ chữ ≥ 0,5 s + 0,3 s/từ (hyperframes check báo `line_unread`): chữ động giữ ≥ 2 s; nhãn/số giữ tới hết shot.
F3 dễ vượt 15% — chuyển bớt câu sang `callouts` (C1) hoặc `ground` (M5) thay vì rút ngắn thời gian giữ.

## Âm thanh

- SFX cho MỌI sự kiện hình: whoosh (T3/T2/M2, vật chạy), pop (nhãn, ghim, timeline, chữ), riser (trước T1/T4/DIS, thanh D2),
  impact nhẹ (cắt cứng, chữ mặt đất, số lớn) — `templates/one-era-motion/mk_sfx.py` sinh từ shots.json.
- SFX thấp hơn giọng 12 dB; nhạc có phách rõ (`make_music.py`, 100 BPM) dời pha cho trùng điểm cắt, thấp hơn giọng 18 dB, ducking −6 dB.
- Trộn: `mix_audio.py vo.mp3 sfx/events.json assets/mix.wav --duration <s> --music music.wav` → −14 LUFS, TP ≤ −1 dBTP.

## Nền vệ tinh

`sat_tiles.py` ghép z7/z9/z11/z13/z16 (mỗi mức phủ rộng hơn khung hình lớn nhất ở mức đó, tính cả khi nghiêng),
`sat_declouds.py` xoá mây bằng nhân bản kết cấu + chỉnh màu. Hiện dần theo Z bằng `show:[Za,Zb]`.
QA: không mây/ô trống trên khu vực đang nói; không lộ hình chữ nhật ảnh trên nền phẳng; không khung > 40% tối trống > 2 s.

## Kiểm tra trước khi giao

1. `python motion.py shots.json proj` — hết "!" (lặp hiệu ứng, chuỗi cảnh, > 15%, chưa dùng, > 6 s, D4 > 2, DIS > 3).
2. Footage Google Earth đủ dài: `media_start + dur + 0,35` ≤ độ dài clip (36 khung ở 6 fps → 5,7 s).
3. `npx hyperframes check` → "Check passed"; `snapshot --at ...` từng nhóm shot; xem kỹ khung nghiêng, nhãn sát mép, mây.
4. Render → `qa_frames.py`, `style_check.py` (contact sheet 1 khung/giây) → nộp kèm `SHOTLIST.md` (timecode, ID hiệu ứng, nguồn hình).
```

## FILE: references/quy-tac-chuyen-gia.md

```markdown
# Quy tắc bắt buộc: video "giải thích kinh tế – địa phương" (dọc 1080×1920, 30 fps)

Rút ra từ góp ý của các chuyên gia sau bản dựng Vĩnh Long đầu tiên (11/2026). Mục tiêu: **mọi câu thoại phải được CHỨNG MINH bằng hình**, không chỉ lặp lại bằng chữ. Mỗi quy tắc có cách kiểm; một quy tắc không kiểm được thì coi như chưa đạt.

## 1. Chất liệu: ≥ 4 loại, xen kẽ

| Loại | Dùng cho | Nguồn |
| --- | --- | --- |
| Bản đồ đồ hoạ vector 2D | định vị, so sánh, kết nối | Natural Earth/OSM; gộp tỉnh theo nghị quyết sáp nhập hiện hành |
| Cảnh quay thật (flycam/stock) của địa danh được nhắc | ≥ 1 lần ở giữa video, đặt ở khoảng lặng giọng đọc | Wikimedia Commons (CC), Pexels, Pixabay; flycam của người dùng; ghi tác giả + giấy phép trên màn hình |
| Bảng số liệu tích luỹ trên nền bản đồ | phần số liệu | số từ báo chính thống |
| Ảnh tài liệu gốc (bài báo/infographic/báo cáo) làm bằng chứng | sau bảng số liệu, 4–6 s | chụp trang báo (`scripts/doc_capture.js`); KHÔNG thay bằng thẻ chữ |
| 10–15 s cuối | người dẫn, hoặc footage thật có chuyển động | KHÔNG dùng ảnh vệ tinh tĩnh |

Google Earth 3D là hình dựng, không phải cảnh quay thật: dùng được để minh hoạ, nhưng không thay được ô "cảnh quay thật" và "10–15 s cuối". Không tìm được footage hợp lệ thì nói rõ với người dùng, đừng lặng lẽ thay.

**Kiểm:** liệt kê chất liệu theo thời gian trong `CAMERA.md`; đếm ≥ 4 loại; không có 2 đoạn liền nhau cùng loại > 30 s.

## 2. Bản đồ – quy tắc định vị

- **0–3 s:** zoom toàn quốc → vùng → tỉnh. **Giây 2** đã thấy vùng được nhắc tới.
- Tỉnh chính: tô toàn bộ ranh giới hành chính, cam `#F28C28`, độ đục 80% (`fill-opacity: 0.8`), không chỉ chấm/nhãn. Dùng ranh giới **sau sáp nhập** nếu đã có nghị quyết (ghi căn cứ ở chân khung).
- Tỉnh/thành so sánh (TP.HCM, Cần Thơ…): tô xám nhạt toàn ranh giới khi được nhắc.
- Sông được nhắc: vẽ sông phát sáng **chạy theo dòng chảy** (thượng nguồn → cửa biển) + nhãn. Lòng sông lấy từ dữ liệu (Natural Earth/OSM) hoặc dò trên ảnh vệ tinh, không vẽ tay ước lượng.
- "Kết nối / hành lang / bản lề": đường nối động giữa các điểm; camera kéo ra đủ rộng để thấy **cả hai đầu**.
- "Cực tăng trưởng / trung tâm": viền tỉnh phát sáng + vòng sóng lan, **đúng khung hình của từ khoá** (± 0,2 s).
- Mọi elip/vùng đánh dấu nằm trọn trong khung an toàn (cách mép 60 px). Vùng nền (ví dụ cả vùng ĐBSCL) chỉ bật khi đang nói tới nó, rồi tắt.

**Kiểm:** snapshot tại 2,0 s, tại mốc mỗi từ khoá (tên tỉnh, tên sông, "kết nối", "cực tăng trưởng"); nhìn xem hình đúng thứ được đọc chưa và có nằm trong khung an toàn không.

## 3. Chuyển động & nhịp

- Không cảnh nào đứng yên > 6 s; nền giữ lâu thì cứ 3–4 s có yếu tố mới (số, nhãn, hiệu ứng, đổi cỡ cảnh).
- Không giữ cùng một góc Google Earth > 8 s.
- Cắt / đổi chất liệu tại khoảng lặng giọng đọc > 0,4 s. Tìm bằng `ffmpeg -af silencedetect=noise=-30dB:d=0.25`. Giọng đọc liền (ít khoảng > 0,4 s) thì dùng các khoảng dài nhất, ghi rõ trong `CAMERA.md`.
- Chuyển cảnh: whip zoom có motion blur (≤ 0,3 s) hoặc cắt thẳng. **CẤM** chuyển cảnh thu nhỏ làm lộ viền khung: cảnh vào bắt đầu ở `scale ≥ 1` (ví dụ 1,45 → 1), cảnh ra phóng to (1 → 1,35).

**Kiểm:** `qa_frames.py` (STATIC > 6 s); bảng cắt cảnh so với bảng khoảng lặng.

## 4. Kiểm soát lỗi render (trước khi xuất)

- Không mây/mảng trắng mờ, không mảng đen/nâu do ảnh vệ tinh/3D chưa tải, không khung nhoè ngoài chuyển cảnh.
- Không > 5 khung đen/tối liên tiếp ngoài chủ đích.
- Chạy `python scripts/qa_frames.py out.mp4`: DEAD_EDGE (> 5% khung là vùng chết dính mép), HAZE, DARK_RUN, BLUR_RUN, STATIC. Có lỗi → xem ảnh nó lưu, sửa và render lại đoạn đó. Công cụ là bộ lọc thô: mọi cờ phải xem bằng mắt (nền phẳng có chủ đích như thẻ trắng có thể bị gắn cờ).
- Cảnh Google Earth: chọn đoạn không có mảng lưới thủng (thường ở mặt sông rộng); chụp thử 3 khung đầu/giữa/cuối trước khi dùng.

## 5. Chữ trên màn hình

- Không phụ đề chạy theo lời. Mỗi cảnh 1 "dòng neo" (≤ 7 từ) nói ý chính, hiện đúng lúc đọc từ khoá; các ý còn lại do nhãn gắn đồ hoạ (kiểu A/B, `he-thiet-ke.md`) gánh.
- Ngắt dòng thủ công: không để 1 từ đơn lẻ trên một dòng, không tách cụm trong ngoặc kép, mỗi dòng ≥ 2 từ (kiểm bằng `assert` khi sinh phụ đề).
- Chữ không đè nhãn bản đồ: khi hiện chữ to, ẩn nhãn bản đồ hoặc dời camera.
- Giữ: nhãn phân đoạn (kính mờ) ở trên, nguồn ở chân khung; % tăng trưởng = chữ cam + ▲, không nền.

- **Vùng an toàn TikTok:** không chữ/nhãn ở y < 210, y > 1440, và x > 940 trong 700 < y < 1440 (chi tiết `he-thiet-ke.md`). Chữ sát đáy sẽ bị caption và tên kênh che.
- **Không mờ:** chữ ≥ 72% trắng, nét vẽ ≥ 2 px và đủ sáng trên nền navy.

## 6. Số liệu

- **Danh sách tích luỹ:** mỗi chỉ số = icon + số lớn + mô tả; xuất hiện lần lượt **và ở lại**; tới chỉ số cuối thấy cả bộ.
- Đếm số giữ lại; chữ số ≥ 72 px, mô tả ≥ 36 px.
- Sau danh sách: ảnh tài liệu gốc 4–6 s, zoom/trượt chậm vào phần số liệu vừa nói, đánh dấu (highlight) đúng đoạn.
- Số trên màn hình theo **nguồn báo**, không theo bản chép lời (Whisper nghe nhầm số). Lệch giữa lời đọc và nguồn → hiện số nguồn và báo người dùng.

## 7. Âm thanh

- Chuẩn hoá tổng thể −14 LUFS, true peak ≤ −1 dBTP.
- SFX nhẹ: whoosh khi zoom/chuyển cảnh, pop khi số/icon xuất hiện, riser trước câu hỏi lớn; thấp hơn giọng đọc ≥ 12 dB.
- Làm bằng `scripts/make_sfx.py` (SFX tổng hợp, không bản quyền) + `scripts/mix_audio.py voice.mp3 events.json mix.wav --duration <s>`; script in số đo cuối và báo lỗi nếu chưa đạt.

## 8. Đoạn kết

- 10–15 s cuối có điểm neo con người hoặc cảnh quay thật có chuyển động.
- Phụ đề nhỏ đặt 1/3 dưới, căn trái.
- Chữ to chỉ cho đúng 1 thông điệp chốt.
```

## FILE: references/style-mau.md

```markdown
# Phong cách từ 5 video mẫu của người dùng

Nguồn: thư mục `video mau` (5 video, đo bằng `analyze_refs.py` ngày 10/11/2026). Đây là phong cách mặc định của skill. `STYLE.md` riêng của một project vẫn ưu tiên hơn.

| Video | Chủ đề | Dài |
| --- | --- | --- |
| A | Bầu cử giữa nhiệm kỳ Mỹ (chính trị/kinh tế) | 3:14 |
| B | Khu Nam TP.HCM, mạng lưới kết nối, dự án hưởng lợi (BĐS) | 3:28 |
| C | "Bắc Bling", quảng bá du lịch (kinh tế/văn hoá) | 2:35 |
| D | Gangnam hoá rồng, Tây Hồ Tây (đô thị/BĐS) | 5:14 |
| E | Tháo gỡ điểm nghẽn tăng trưởng (kinh tế vĩ mô) | 3:36 |

## [ĐO] Số liệu

| Chỉ số | A | B | C | D | E | **Mục tiêu** |
| --- | --- | --- | --- | --- | --- | --- |
| Khung | 9:16 | 9:16 | 9:16 | 9:16 | 9:16 | **1080×1920, 30 fps** |
| % thời gian camera chạy | 65% | 91% | 85% | 88% | 87% | **≥ 85%** |
| Số lần dừng ≥ 0,4 s / phút | 11,7 | 2,9 | 6,2 | 2,9 | 4,2 | **≤ 4/phút** |
| Cảnh thật, trung vị (s) | 4,0 | 2,3 | 2,4 | 3,3 | 4,1 | **2,5–4 s** |
| Cảnh thật, p90 (s) | 12,2 | 6,5 | 7,4 | 7,4 | 15,5 | **cảnh dài nhất ~7 s, đoạn bản đồ/giải thích tới 12–15 s** |
| Transition dồn dập (zoom-blur/flash) | 17 | 7 | 25 | 24 | 10 | **khoảng 1 lần mỗi 8–15 s** |
| Cắt khi camera đang chạy | 66% | 84% | 63% | 77% | 76% | **≥ 75%** |
| Cắt match-move (cùng hướng) | 92% | 42% | 93% | 55% | 76% | **≥ 75%** |
| Cảnh có parallax | 30% | 71% | 70% | 75% | 25% | BĐS/đô thị **≥ 70%**; vĩ mô/chính trị 25–30% |
| Chỉ số parallax trung vị | 0,035 | 0,23 | 0,04 | 0,22 | 0,03 | BĐS **≈ 0,2** |
| Pan trung vị / p90 (%W/s) | 1,1 / 18 | 2,8 / 22 | 5,0 / 45 | 2,4 / 23 | 2,2 / 20 | **trôi 1–5, lướt nhanh 18–25** |
| Zoom/dolly trung vị (%/s) | 0,8 | 2,6 | 2,1 | 2,8 | 1,6 | **1,5–3 %/s** liên tục |

Hai nhóm rõ rệt:

- **BĐS/đô thị (B, D):** parallax cao vì có nhiều cảnh **3D Google Earth/Google Maps** (camera bay quanh toà nhà, nút giao dựng 3D) cộng với bản đồ nghiêng.
- **Vĩ mô/chính trị (A, E):** chủ yếu là bản đồ phẳng và đồ hoạ, parallax thấp. Ở nhóm này camera vẫn chạy liên tục bằng zoom và pan đều.

Tốc độ thường thấp (trôi 1–5 %W/s), xen các cú lướt rất nhanh khi chuyển. Tức là nhịp **trôi chậm, lướt nhanh, trôi chậm**.

## [NHÌN] Ngữ pháp hình ảnh

Phần này chỉ dựa trên ảnh tổng hợp cảnh của video A và B, cùng đồ thị chuyển động của A, B, D. Video C, D, E chưa được xem bằng mắt.

1. **Bay vào bản đồ vệ tinh (map dive)** từ châu lục, xuống quốc gia (viền trắng), xuống thành phố, rồi xuống khu, liên tục không cắt. Ảnh vệ tinh thật, tông tối.
2. **Lớp thông tin trên bản đồ:**
   - vùng quận/khu tô màu trong suốt (xanh lá, đỏ) có viền;
   - tuyến đường neon cam, vàng hoặc đỏ có quầng sáng, tự vẽ ra;
   - ghim tròn trắng kèm nhãn chữ hoa trên nền đen;
   - thẻ logo dự án nền trắng cắm vào tuyến;
   - nhãn khoanh vùng màu xanh dương.
3. **Cảnh 3D lấy từ Google Earth/Google Maps** (cao tốc, nút giao, thành phố về đêm), không phải flycam quay thật (người dùng xác nhận). Camera bay vòng, lặn, lướt trên mô hình 3D ảnh thật của thành phố, xen giữa các đoạn bản đồ phẳng. Đây là nguồn parallax chính ở nhóm BĐS. Cách làm: `camera-rig.md` §8.
4. **Chuyển cảnh:**
   - phổ biến nhất là zoom-blur xuyên tâm (lao vào hoặc lùi ra);
   - cắt match-move khi đang lướt;
   - chữ làm mờ để ra;
   - hiếm khi dùng hoà tan.
5. **Chữ:**
   - nhãn chủ đề dạng viên thuốc xanh dương ở đầu khung, giữ suốt cả đoạn;
   - tiêu đề lớn chữ hoa đậm, trắng, có một phần nhấn vàng, đặt ở 1/3 dưới hoặc giữa khung;
   - mốc ngày hoặc con số rất lớn màu vàng ("1/10/2026");
   - câu hỏi giữa khung ("CHUYỆN GÌ ĐANG XẢY RA?") rồi làm mờ để ra.
6. **Nhân vật/đồ vật cắt nền (cutout):** người kèm đạo cụ đặt trên bản đồ, chân dung trong thẻ có tên, cột tiền minh hoạ số tiền ("~450 TRIỆU USD"). Các thứ này nằm ở lớp gần camera và tạo parallax trên nền bản đồ.
7. **Infographic nền sáng** (biểu đồ ghế quốc hội hình bán nguyệt) xen giữa để đổi nhịp.
8. **Màu:** nền gần đen hoặc xanh rêu tối từ ảnh vệ tinh, chữ trắng. Màu nhấn gồm vàng `#ffd23f`, cam `#ff7a1a`, xanh lá vùng `#3ccf7a`, xanh dương nhãn `#2f5bd3`, đỏ cho đối lập/giảm.

## Áp vào skill

- Template `templates/map-dive-parallax/` là **dọc 1080×1920**, theo kiểu bay vào bản đồ, có tuyến neon, ghim, thẻ dự án và tiêu đề dưới. Bản ngang ở `templates/ngang-parallax/`.
- Ghép take: đoạn bản đồ (rig) → cinematic-zoom → cảnh 3D Google Earth (`camera-rig.md` §8) → cinematic-zoom → đoạn bản đồ. Xem `camera-rig.md` §6.
- Khi nghiệm thu, chạy `analyze_refs.py` trên bản render. Các chỉ số phải nằm trong cột **Mục tiêu** ở trên.
```

## FILE: design/design.css

```css
    /* ===== HỆ THIẾT KẾ: báo chí kinh tế, tối giản (1 phông, 1 màu nhấn) =====
       VÙNG AN TOÀN TIKTOK (1080×1920): không đặt chữ/nhãn ở y < 210 (thanh trên), y > 1440 (tên kênh, caption, nhạc),
       x > 940 khi 700 < y < 1440 (cột nút tim/bình luận/chia sẻ). Độ rõ: chữ ≥ 72% trắng, nét vẽ ≥ 2 px. */
    #root { --navy0: #0E1A2B; --navy1: #13243A; --accent: #F28C28; --ink: #FFFFFF; --ink75: rgba(255,255,255,0.88); --ink45: rgba(255,255,255,0.72); --neutral: #8A97A8;
      font-family: 'Be Vietnam Pro', sans-serif; color: var(--ink); background: var(--navy0); }
    /* nhãn phân đoạn trên cùng: kính mờ */
    .seg { position: absolute; left: 0; right: 0; top: 230px; text-align: center; }
    .seg > span { display: inline-block; padding: 12px 28px 13px; font-size: 24px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase;
      color: var(--ink); background: rgba(255,255,255,0.10); border: 1.5px solid rgba(255,255,255,0.20); border-radius: 999px; backdrop-filter: blur(10px); }
    /* dòng neo: tiêu đề lớn duy nhất của khung */
    .anchor { position: absolute; left: 70px; right: 150px; text-align: center; font-size: 68px; font-weight: 800; line-height: 1.08; letter-spacing: 0.01em;
      text-transform: uppercase; text-shadow: 0 2px 4px rgba(5,10,20,0.55), 0 6px 30px rgba(5,10,20,0.8); }
    .anchor .ln { display: block; white-space: nowrap; }
    .anchor .w { display: inline-block; }
    .anchor em { font-style: normal; color: var(--accent); }
    .anchor.low { bottom: 520px; } .anchor.mid { top: 760px; }
    /* Kiểu A: nhãn gắn vật thể — chấm 10px + đường dẫn 2px + chữ, không hộp */
    .la { position: absolute; left: 0; top: 0; width: 0; height: 0; }
    .la .dot { position: absolute; left: -5px; top: -5px; width: 10px; height: 10px; border-radius: 50%; background: var(--ink); box-shadow: 0 0 0 3px rgba(14,26,43,0.6); }
    .la .lead { position: absolute; left: 0; top: -1.5px; height: 3px; background: var(--ink); transform-origin: 0 50%; }
    .la .tx { position: absolute; white-space: nowrap; font-size: 32px; font-weight: 600; line-height: 1.1; text-shadow: 0 0 12px rgba(0,0,0,0.7), 0 2px 4px rgba(0,0,0,0.75); }
    .la .tx small { display: block; margin-top: 4px; font-size: 28px; font-weight: 500; color: var(--ink75); }
    .la.acc .dot { background: var(--accent); }
    /* Kiểu B: thẻ khái niệm */
    .lb { position: absolute; left: 0; top: 0; width: 0; height: 0; }
    .lb > span { position: absolute; transform: translate(-50%, -50%); white-space: nowrap; padding: 9px 16px 10px; font-size: 28px; font-weight: 600; letter-spacing: 0.02em;
      text-transform: uppercase; color: var(--ink); background: rgba(14,26,43,0.70); border: 2px solid var(--accent); border-radius: 8px; }
    /* chân trang nguồn */
    .foot { position: absolute; left: 70px; right: 150px; top: 300px; text-align: center; font-size: 20px; font-weight: 500; line-height: 1.4; color: var(--ink45); text-shadow: 0 1px 6px rgba(0,0,0,0.6); }
    /* gradient navy cho ảnh/video: trên 18%, dưới 22% */
    .gtop { position: absolute; left: 0; right: 0; top: 0; height: 420px; background: linear-gradient(180deg, rgba(14,26,43,0.85), rgba(14,26,43,0)); }
    .gbot { position: absolute; left: 0; right: 0; bottom: 0; height: 900px; background: linear-gradient(0deg, rgba(14,26,43,0.85) 0%, rgba(14,26,43,0.75) 45%, rgba(14,26,43,0) 100%); }
    .up { color: var(--accent); font-weight: 600; }
```

## FILE: design/flight.css

```css
    /* ===== flight.css — phong cách C: một camera, một bản đồ sống (dùng cùng motion.css) ===== */
    .plane { transform-style: preserve-3d; }
    #blkhost { position: absolute; left: 0; top: 0; width: 0; height: 0; transform-style: preserve-3d; }
    /* khối 3D (V6): mặt trên + 4 mặt bên; độ đậm qua --a (KHÔNG dùng opacity vì làm phẳng 3D) */
    .blk { position: absolute; left: 0; top: 0; transform-style: preserve-3d; transform-origin: 50% 50%; --a: .9; }
    .blk .f { position: absolute; left: 0; top: 0; transform-origin: 0 0; }
    .blk .top { width: 100%; height: 100%; background: rgba(47,211,224,var(--a)); box-shadow: 0 0 14px rgba(47,211,224,calc(var(--a) * .7)); }
    .blk .s1, .blk .s2 { background: rgba(20,128,140,var(--a)); }
    .blk .s3, .blk .s4 { background: rgba(28,158,170,var(--a)); }
    .heat { mix-blend-mode: screen; }
    .lyr .fill { opacity: 0; }
    /* thẻ số (V10): số lớn 132 px, đơn vị nhỏ */
    .la .tx b.xl { font-size: 132px; letter-spacing: -.01em; font-variant-numeric: tabular-nums; }
    .la .tx b u { text-decoration: none; font-size: 52px; margin-left: 12px; }
    .la.c-w .dot { background: #fff; }
    /* chú giải + dòng nguồn (màn hình, trong vùng an toàn TikTok) */
    .legend { position: absolute; left: 80px; top: 1180px; display: flex; flex-direction: column; gap: 12px; }
    .legend .li { display: flex; align-items: center; gap: 16px; font-size: 34px; font-weight: 700; text-shadow: 0 0 14px rgba(0,0,0,.9), 0 2px 5px rgba(0,0,0,.8); }
    .legend .li i { width: 34px; height: 34px; border-radius: 8px; box-shadow: 0 0 14px currentColor; opacity: .85; }
    .src { position: absolute; left: 80px; right: 160px; top: 1396px; font-size: 19px; font-weight: 500; color: rgba(255,255,255,.6); text-shadow: 0 1px 6px rgba(0,0,0,.9); }
    /* vòng bán kính (V4) và vòng tròn diện tích / điểm nóng (V5, V8) — HTML để không vỡ hình khi phóng lớn */
    .ring, .disc { position: absolute; left: 0; top: 0; border-radius: 50%; }
    .ring { border: 4px solid #FACC15; background: rgba(250,204,21,.07); box-shadow: 0 0 18px rgba(250,204,21,.65), inset 0 0 18px rgba(250,204,21,.35); }
    .disc.k-green { border: 5px solid #4ADE80; background: rgba(74,222,128,.40); box-shadow: 0 0 20px rgba(74,222,128,.7); }
    .disc.k-proj { border: 5px solid #2FD3E0; background: rgba(47,211,224,.35); box-shadow: 0 0 20px rgba(47,211,224,.7); }
    .disc.heat { background: radial-gradient(closest-side, rgba(250,204,21,.85), rgba(242,140,40,.45) 45%, rgba(242,140,40,0)); mix-blend-mode: screen; }
    /* ===== v2: huy hiệu icon, thẻ logo, cửa sổ ảnh; chữ tối thiểu 36 px ===== */
    .la .tx small { font-size: 36px; }
    .legend .li { font-size: 36px; }
    .bdg { display: inline-flex; align-items: center; justify-content: center; width: 84px; height: 84px; border-radius: 50%; flex: none;
      background: var(--bc); box-shadow: 0 0 0 3px #fff, 0 0 22px var(--bc), 0 6px 14px rgba(0,0,0,.45); }
    .bdg svg { width: 54px; height: 54px; }
    .bdg.xl { width: 96px; height: 96px; } .bdg.xl svg { width: 62px; height: 62px; }
    .bdg.sm { width: 72px; height: 72px; } .bdg.sm svg { width: 46px; height: 46px; }
    .la .tx.wi { display: flex; align-items: center; gap: 22px; }
    .la .tx .tb { display: block; }
    .lcard { display: flex; flex-direction: column; align-items: center; width: 400px; padding: 26px 26px 22px; border-radius: 26px; background: #fff;
      color: #0E1A2B; box-shadow: 0 0 0 3px rgba(255,255,255,.6), 0 22px 50px rgba(0,0,0,.5); text-shadow: none !important; white-space: normal; }
    .lcard .lg { display: flex; align-items: center; justify-content: center; width: 100%; height: 150px; }
    .lcard .lg img { width: 66%; max-height: 150px; object-fit: contain; }
    .lcard .mono { display: flex; align-items: center; justify-content: center; width: 140px; height: 140px; border-radius: 50%; background: #0E1A2B; color: #fff; font-size: 52px; font-weight: 800; }
    .lcard .nm { margin-top: 14px; font-size: 38px; font-weight: 800; line-height: 1.1; text-align: center; }
    .lcard .rl { margin-top: 6px; font-size: 36px; font-weight: 600; color: #42526a; line-height: 1.15; text-align: center; }
    .pwin { display: block; padding: 10px; border-radius: 28px; background: rgba(255,255,255,.95); box-shadow: 0 0 0 3px rgba(255,255,255,.5), 0 24px 60px rgba(0,0,0,.55); white-space: normal; }
    .pwin .pimg { display: block; width: 100%; overflow: hidden; border-radius: 20px; }
    .pwin .pimg img { display: block; width: 100%; height: 100%; object-fit: cover; transform-origin: 50% 50%; }
    .pwin .pcap { display: block; padding: 10px 8px 2px; font-size: 36px; font-weight: 700; color: #0E1A2B; text-shadow: none; text-align: center; }
    .disc.k-route { border: 5px solid #E04BD6; background: rgba(224,75,214,.38); box-shadow: 0 0 20px rgba(224,75,214,.7); }
    .disc.k-yel { border: 5px solid #FACC15; background: rgba(250,204,21,.32); box-shadow: 0 0 20px rgba(250,204,21,.7); }
    .disc.k-adm { border: 5px solid #F28C28; background: rgba(242,140,40,.35); box-shadow: 0 0 20px rgba(242,140,40,.7); }
    .lyr.dash .core { stroke-dasharray: 2 1.4; }
    .blk.g-m25 .top, .blk.g-m26 .top { background: rgba(224,75,214,var(--a)); box-shadow: 0 0 16px rgba(224,75,214,.7); }
    .blk.g-m25 .s1, .blk.g-m25 .s2, .blk.g-m26 .s1, .blk.g-m26 .s2 { background: rgba(150,40,145,var(--a)); }
    .blk.g-m25 .s3, .blk.g-m25 .s4, .blk.g-m26 .s3, .blk.g-m26 .s4 { background: rgba(185,55,178,var(--a)); }
    .la .tx.lcard, .la .tx.pwin { white-space: normal; }
```

## FILE: design/install_fonts.sh

```bash
#!/bin/bash
# Tải Be Vietnam Pro (400/500/600/800, bộ vietnamese + latin-ext + latin) từ npm và sinh fonts.css
# Dùng: install_fonts.sh <thư mục project>   -> <project>/assets/fonts/*.woff2 + <project>/fonts.css
set -e
P="$1"; T=$(mktemp -d); cd "$T"
npm pack @fontsource/be-vietnam-pro@5.3.0 >/dev/null 2>&1 && tar xzf fontsource-be-vietnam-pro-5.3.0.tgz
mkdir -p "$P/assets/fonts"
python3 - "$P" <<'PY'
import re, shutil, sys
P = sys.argv[1]; out = []
for w in [400, 500, 600, 800]:
    for block in re.findall(r'@font-face\s*\{[^}]+\}', open(f'package/{w}.css').read()):
        m = re.search(r'files/(be-vietnam-pro-(vietnamese|latin-ext|latin)-\d+-normal\.woff2)', block)
        if not m: continue
        fn = m.group(1); shutil.copy('package/files/' + fn, f'{P}/assets/fonts/{fn}')
        ur = re.search(r'unicode-range:\s*([^;]+);', block).group(1)
        out.append(f"    @font-face {{ font-family: 'Be Vietnam Pro'; font-style: normal; font-weight: {w}; font-display: block; src: url('assets/fonts/{fn}') format('woff2'); unicode-range: {ur}; }}")
open(f'{P}/fonts.css', 'w').write("\n".join(out) + "\n"); print(len(out), "font faces")
PY
```

## FILE: design/motion.css

```css
    /* ===== motion.css — "bản đồ + footage" điện ảnh. Màu theo NGHĨA, giữ nhất quán cả video =====
       cam #F28C28 = vùng hành chính · cyan #2FD3E0 = ranh dự án + mặt nước · xanh lá #4ADE80 = công viên, cây xanh
       hồng tím #E04BD6 = tuyến giao thông, kết nối · vàng #FACC15 = bán kính, khoảng cách, ghim tiện ích
       Vùng an toàn TikTok: chữ ở 210 < y < 1440, x < 940 trong dải 700–1440. Không chữ quan trọng nào < 34 px. */
    #root { --adm: #F28C28; --proj: #2FD3E0; --green: #4ADE80; --route: #E04BD6; --yel: #FACC15;
      --ink: #FFFFFF; --ink75: rgba(255,255,255,.88); --ink50: rgba(255,255,255,.62); --navy: #0E1A2B;
      font-family: 'Be Vietnam Pro', sans-serif; color: var(--ink); background: var(--navy); }
    .zw { position: absolute; inset: 0; transform-origin: 540px 960px; overflow: hidden; }
    .plane { position: absolute; inset: 0; transform-origin: 540px 1100px; }
    .map { position: absolute; left: 0; top: 0; }
    /* lớp đường: core 4–6 px + glow ngoài; fill 35–50% */
    .lyr .fill { stroke: none; fill-opacity: .4; }
    .lyr .glow { fill: none; stroke-linecap: round; stroke-linejoin: round; opacity: .55; filter: blur(5px); }
    .lyr .core { fill: none; stroke-linecap: round; stroke-linejoin: round; }
    .lyr .len { stroke-dasharray: 100 120; stroke-dashoffset: 110; }
    .k-adm .core, .k-adm .glow { stroke: var(--adm); } .k-adm .fill { fill: var(--adm); }
    .k-proj .core, .k-proj .glow { stroke: var(--proj); } .k-proj .fill { fill: var(--proj); }
    .k-water .core, .k-water .glow { stroke: var(--proj); } .k-water .fill { fill: var(--proj); }
    .k-green .core, .k-green .glow { stroke: var(--green); } .k-green .fill { fill: var(--green); }
    .k-route .core, .k-route .glow { stroke: var(--route); } .k-route .fill { fill: var(--route); }
    .k-yel .core, .k-yel .glow { stroke: var(--yel); }
    .ringc { fill: rgba(250,204,21,.06); stroke: var(--yel); }
    /* nhãn bản đồ 34–40 px, bóng mềm, không hộp đen */
    .la { position: absolute; left: 0; top: 0; width: 0; height: 0; }
    .la .dot { position: absolute; left: -7px; top: -7px; width: 14px; height: 14px; border-radius: 50%; background: #fff; box-shadow: 0 0 12px rgba(255,255,255,.8); }
    .la .lead { position: absolute; left: 0; top: -1.5px; height: 3px; background: #fff; transform-origin: 0 50%; }
    .la .tx { position: absolute; white-space: nowrap; font-size: 38px; font-weight: 700; line-height: 1.1;
      text-shadow: 0 0 14px rgba(0,0,0,.85), 0 2px 5px rgba(0,0,0,.8); }
    .la .tx b { display: block; font-size: 64px; font-weight: 800; line-height: 1; }
    .la .tx small { display: block; margin-top: 4px; font-size: 34px; font-weight: 600; color: var(--ink75); }
    .la.c-adm .tx b, .la.c-adm .dot { color: var(--adm); background-color: transparent; } .la.c-adm .dot { background: var(--adm); }
    .la.c-proj .tx b { color: var(--proj); } .la.c-proj .dot { background: var(--proj); }
    .la.c-route .tx b { color: var(--route); } .la.c-route .dot { background: var(--route); }
    .la.c-yel .tx b { color: var(--yel); } .la.c-yel .dot { background: var(--yel); }
    .la.c-green .tx b { color: var(--green); } .la.c-green .dot { background: var(--green); }
    /* ghim tiện ích (M8) */
    .pin { position: absolute; left: 0; top: 0; width: 0; height: 0; }
    .pin .pi { position: absolute; left: -22px; top: -60px; width: 44px; height: 60px; }
    .pin .pl { position: absolute; left: 30px; top: -58px; white-space: nowrap; font-size: 36px; font-weight: 700; text-shadow: 0 0 14px rgba(0,0,0,.9), 0 2px 5px rgba(0,0,0,.8); }
    .pin.l .pl { left: auto; right: 30px; }
    /* chữ phối cảnh nằm trên mặt đất (M5) */
    .ground { position: absolute; left: 0; top: 0; width: 0; height: 0; }
    .ground span { position: absolute; transform: translate(-50%, -50%); white-space: nowrap; font-size: 96px; font-weight: 800; letter-spacing: .06em;
      text-transform: uppercase; color: rgba(255,255,255,.92); -webkit-text-stroke: 2px var(--proj); text-shadow: 0 0 30px rgba(47,211,224,.7); }
    /* chữ động trên footage (F3) */
    .kw { position: absolute; left: 60px; right: 60px; text-align: center; font-size: 112px; font-weight: 800; line-height: 1.02;
      text-transform: uppercase; letter-spacing: .01em; color: #fff; -webkit-text-stroke: 2px rgba(255,255,255,.35);
      text-shadow: 0 0 34px rgba(0,0,0,.55), 0 4px 10px rgba(0,0,0,.7); }
    .kw .ln { display: block; white-space: nowrap; }
    .kw em { font-style: normal; color: var(--accent, var(--adm)); text-shadow: 0 0 28px currentColor, 0 4px 10px rgba(0,0,0,.7); }
    /* số lớn (D1) */
    .bign { position: absolute; left: 60px; right: 60px; text-align: center; }
    .bign .n { font-size: 156px; font-weight: 800; font-variant-numeric: tabular-nums; line-height: 1; letter-spacing: -.01em;
      text-shadow: 0 0 40px rgba(0,0,0,.6), 0 6px 14px rgba(0,0,0,.6); }
    .bign .u { font-size: 58px; font-weight: 800; margin-left: 16px; }
    .bign .lb { display: block; margin-top: 14px; font-size: 44px; font-weight: 700; text-shadow: 0 0 18px rgba(0,0,0,.8); }
    /* thanh quy mô (D2) */
    .bar { position: absolute; left: 90px; width: 800px; }
    .bar .bl { font-size: 40px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; text-shadow: 0 0 14px rgba(0,0,0,.8); }
    .bar .bt { position: relative; margin-top: 18px; height: 26px; border-radius: 13px; background: rgba(255,255,255,.18); overflow: hidden; }
    .bar .bf { position: absolute; left: 0; top: 0; bottom: 0; width: 100%; border-radius: 13px; background: var(--proj); box-shadow: 0 0 24px var(--proj); transform-origin: 0 50%; }
    .bar .bv { margin-top: 18px; font-size: 128px; font-weight: 800; line-height: 1; font-variant-numeric: tabular-nums; text-shadow: 0 0 30px rgba(0,0,0,.6); }
    .bar .bv small { font-size: 54px; margin-left: 12px; }
    .bar .bs { font-size: 38px; font-weight: 600; color: var(--ink75); margin-top: 8px; text-shadow: 0 0 14px rgba(0,0,0,.8); }
    /* timeline (D5) */
    .tline { position: absolute; left: 80px; width: 860px; }
    .tline .ax { position: absolute; left: 0; right: 0; top: 0; height: 4px; background: #fff; transform-origin: 0 50%; box-shadow: 0 0 14px rgba(255,255,255,.6); }
    .tline .ev { position: absolute; top: 0; width: 0; height: 0; }
    .tline .ev i { position: absolute; left: -13px; top: -11px; width: 26px; height: 26px; border-radius: 50%; background: var(--yel); box-shadow: 0 0 18px var(--yel); }
    .tline .ev .d { position: absolute; left: 0; top: -150px; transform: translateX(-50%); white-space: nowrap; font-size: 46px; font-weight: 800; text-shadow: 0 0 16px rgba(0,0,0,.8); }
    .tline .ev .t { position: absolute; left: 0; top: 40px; transform: translateX(-50%); width: 260px; text-align: center; font-size: 34px; font-weight: 600; line-height: 1.2; color: var(--ink75); text-shadow: 0 0 14px rgba(0,0,0,.9); }
    .tline .ev.lo .d { top: 40px; } .tline .ev.lo .t { top: -150px; }
    /* tường đối tác (D6) */
    .wall { position: absolute; left: 70px; width: 870px; display: grid; grid-template-columns: 1fr 1fr; gap: 22px; }
    .tile { height: 170px; border-radius: 18px; background: rgba(255,255,255,.94); color: #0E1A2B; display: flex; flex-direction: column; align-items: center; justify-content: center;
      text-align: center; box-shadow: 0 18px 40px rgba(0,0,0,.45); padding: 0 16px; }
    .tile b { font-size: 44px; font-weight: 800; line-height: 1.05; } .tile small { font-size: 30px; font-weight: 600; color: #4b5b70; margin-top: 8px; }
    .tile.hl { outline: 5px solid var(--adm); }
    /* danh sách xếp chồng (D4, tối đa 2 lần) */
    .stack { position: absolute; left: 80px; width: 860px; }
    .stack .row { display: flex; align-items: baseline; gap: 22px; padding: 14px 0; border-bottom: 1px solid rgba(255,255,255,.18); }
    .stack .row b { font-size: 72px; font-weight: 800; font-variant-numeric: tabular-nums; } .stack .row span { font-size: 38px; font-weight: 600; color: var(--ink75); }
    /* nhãn phân đoạn + nguồn */
    .seg { position: absolute; left: 0; right: 0; top: 230px; text-align: center; }
    .seg > span { display: inline-block; padding: 11px 26px 12px; font-size: 26px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase;
      background: rgba(10,18,32,.45); border: 1.5px solid rgba(255,255,255,.28); border-radius: 999px; backdrop-filter: blur(10px); }
    .foot { position: absolute; left: 70px; right: 150px; top: 300px; text-align: center; font-size: 19px; font-weight: 500; color: rgba(255,255,255,.62);
      text-shadow: 0 1px 6px rgba(0,0,0,.8); }
    .gtop { position: absolute; left: 0; right: 0; top: 0; height: 420px; background: linear-gradient(180deg, rgba(10,18,32,.8), rgba(10,18,32,0)); }
    .gbot { position: absolute; left: 0; right: 0; bottom: 0; height: 900px; background: linear-gradient(0deg, rgba(10,18,32,.85), rgba(10,18,32,.55) 50%, rgba(10,18,32,0)); }
    .cloud { position: absolute; border-radius: 50%; background: radial-gradient(closest-side, rgba(240,244,248,.95), rgba(240,244,248,.5) 55%, rgba(240,244,248,0)); }
    .plane-ic { position: absolute; left: 0; top: 0; width: 220px; height: 220px; }
```

## FILE: scripts/analyze_refs.py

```python
#!/usr/bin/env python3
"""
Phân tích video mẫu (bất động sản / kinh tế) để rút ra "ngữ pháp" camera + parallax.

Đo cho mỗi video:
  - điểm cắt cảnh (cut) và kiểu chuyển (cắt cứng / hoà tan)
  - chuyển động camera theo từng cảnh: pan, tilt, zoom (dolly), xoay; tốc độ chuẩn hoá theo khung
  - độ liên tục: % thời gian camera đang chuyển động, số lần "dừng chết", cắt khi đang chuyển động
  - parallax: các điểm ở độ sâu khác nhau chạy với vận tốc khác nhau (độ tách lớp)
  - bảng màu chủ đạo, contact sheet từng cảnh, đồ thị tốc độ camera

Cách dùng:
  python analyze_refs.py "C:\\Users\\Admin\\Downloads\\video mau" --out phan-tich
  python analyze_refs.py video1.mp4 video2.mp4 --out phan-tich --width 480 --step 1

Yêu cầu: pip install opencv-python-headless numpy
Kết quả: <out>/SUMMARY.md, <out>/STYLE_DRAFT.md, <out>/summary.json và một thư mục cho từng video
(report.json, motion.png, sheet-*.jpg). Mọi con số là ĐO ĐƯỢC; phần nhận xét bằng mắt ghi riêng.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import sys
import tempfile
from pathlib import Path

try:
    import cv2
    import numpy as np
except ImportError:  # pragma: no cover
    sys.exit("Thiếu thư viện: pip install opencv-python-headless numpy")

VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v", ".mpg", ".mpeg", ".wmv", ".flv"}

# Ngưỡng (chuẩn hoá theo khung hình, mỗi giây)
MOVE_PAN = 0.6      # % chiều rộng khung / s  -> coi là đang pan
MOVE_ZOOM = 0.35    # % tỉ lệ / s             -> coi là đang zoom/dolly
MOVE_ROT = 0.15     # độ / s
STOP_MIN_SEC = 0.4  # đứng yên lâu hơn mức này = 1 lần "dừng"
PARALLAX_ON = 0.18  # chỉ số tách lớp >= ngưỡng -> có parallax rõ


# ----------------------------------------------------------------- I/O helpers
def imwrite(path: Path, img) -> None:
    """cv2.imwrite hỏng với đường dẫn có dấu trên Windows -> dùng imencode."""
    params = [cv2.IMWRITE_JPEG_QUALITY, 88] if path.suffix.lower() in (".jpg", ".jpeg") else []
    ok, buf = cv2.imencode(path.suffix, img, params)
    if ok:
        path.write_bytes(buf.tobytes())


def open_video(path: Path):
    cap = cv2.VideoCapture(str(path))
    if cap.isOpened():
        return cap, None
    # Đường dẫn có ký tự Unicode (vd. "video mẫu") đôi khi không mở được trên Windows
    tmpdir = tempfile.mkdtemp(prefix="refvid_")
    tmp = Path(tmpdir) / ("v" + path.suffix.lower())
    shutil.copyfile(path, tmp)
    cap = cv2.VideoCapture(str(tmp))
    return cap, tmpdir


def collect_inputs(items: list[str]) -> list[Path]:
    out: list[Path] = []
    for it in items:
        p = Path(it).expanduser()
        if p.is_dir():
            out += sorted(q for q in p.rglob("*") if q.suffix.lower() in VIDEO_EXT)
        elif p.is_file():
            out.append(p)
        else:
            print(f"[bỏ qua] không tìm thấy: {it}", file=sys.stderr)
    return out


def safe_name(p: Path) -> str:
    keep = "".join(c if c.isalnum() or c in "-_" else "-" for c in p.stem)
    return keep.strip("-")[:60] or "video"


# ----------------------------------------------------------------- per-frame motion
def hsv_hist(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h = cv2.calcHist([hsv], [0, 1], None, [32, 32], [0, 180, 0, 256])
    cv2.normalize(h, h)
    return h


def frame_motion(prev_gray, gray):
    """Ước lượng chuyển động toàn cục + chỉ số parallax giữa 2 khung."""
    h, w = gray.shape
    pts = cv2.goodFeaturesToTrack(prev_gray, maxCorners=500, qualityLevel=0.01, minDistance=7, blockSize=7)
    res = dict(tx=0.0, ty=0.0, scale=1.0, rot=0.0, parallax=None, spread=None, n=0, valid=False)
    if pts is None or len(pts) < 25:
        return res
    nxt, st, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, pts, None, winSize=(21, 21), maxLevel=3)
    if nxt is None:
        return res
    st = st.reshape(-1).astype(bool)
    p0 = pts.reshape(-1, 2)[st]
    p1 = nxt.reshape(-1, 2)[st]
    if len(p0) < 25:
        return res
    # loại các điểm trượt đi quá xa (lỗi tracking)
    flow = p1 - p0
    mag = np.linalg.norm(flow, axis=1)
    keep = mag < 0.25 * w
    p0, p1, flow, mag = p0[keep], p1[keep], flow[keep], mag[keep]
    if len(p0) < 25:
        return res
    M, inl = cv2.estimateAffinePartial2D(p0, p1, method=cv2.RANSAC, ransacReprojThreshold=1.5, maxIters=2000)
    if M is None:
        return res
    a, b = M[0, 0], M[1, 0]
    scale = math.hypot(a, b)
    rot = math.degrees(math.atan2(b, a))
    # chuyển động tịnh tiến quy về tâm khung
    cx, cy = w / 2, h / 2
    center_new = M @ np.array([cx, cy, 1.0])
    tx, ty = center_new[0] - cx, center_new[1] - cy

    pred = (np.hstack([p0, np.ones((len(p0), 1))]) @ M.T)
    resid = np.linalg.norm(p1 - pred, axis=1)
    med_mag = float(np.median(mag))
    parallax = spread = None
    if med_mag > 0.35:  # chỉ đo parallax khi khung thật sự chuyển động
        parallax = float(np.median(resid) / (med_mag + 1e-6))
        # độ tách lớp: dải vận tốc dọc hướng chuyển động chính (p90-p10)/median
        d = np.array([tx, ty])
        if np.linalg.norm(d) > 0.3:
            d = d / np.linalg.norm(d)
            proj = flow @ d
            med = np.median(proj)
            if abs(med) > 0.3:
                spread = float((np.percentile(proj, 90) - np.percentile(proj, 10)) / abs(med))
    res.update(tx=float(tx), ty=float(ty), scale=float(scale), rot=float(rot),
               parallax=parallax, spread=spread, n=int(len(p0)), valid=True)
    return res


# ----------------------------------------------------------------- analysis
def analyze_video(path: Path, out_dir: Path, width: int, step: int) -> dict:
    cap, tmpdir = open_video(path)
    if not cap.isOpened():
        return {"file": str(path), "error": "không mở được video"}
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    nframes = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    W0 = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H0 = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    sw = width
    sh = int(round(H0 * sw / max(W0, 1)))
    dt = step / fps

    times, motions, hist_corr, mad, thumbs = [], [], [], [], []
    palette_samples = []
    prev_gray = prev_hist = None
    idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % step:
            idx += 1
            continue
        small = cv2.resize(frame, (sw, sh), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        hist = hsv_hist(small)
        t = idx / fps
        times.append(t)
        thumbs.append(cv2.resize(small, (320, int(320 * sh / sw))))
        if prev_gray is None:
            motions.append(dict(tx=0, ty=0, scale=1, rot=0, parallax=None, spread=None, n=0, valid=False))
            hist_corr.append(1.0)
            mad.append(0.0)
        else:
            hist_corr.append(float(cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CORREL)))
            mad.append(float(np.mean(cv2.absdiff(prev_gray, gray))))
            motions.append(frame_motion(prev_gray, gray))
        if len(times) % max(1, int(fps // step)) == 0:  # ~1 mẫu màu / giây
            palette_samples.append(cv2.resize(small, (64, int(64 * sh / sw))).reshape(-1, 3))
        prev_gray, prev_hist = gray, hist
        idx += 1
    cap.release()
    if tmpdir:
        shutil.rmtree(tmpdir, ignore_errors=True)
    n = len(times)
    if n < 3:
        return {"file": str(path), "error": "video quá ngắn"}
    duration = (nframes / fps) if nframes else times[-1] + dt

    # ---- cuts: histogram tụt mạnh HOẶC sai khác điểm ảnh vượt xa trung vị, và tracking mất
    mad_arr = np.array(mad)
    base = float(np.median(mad_arr[1:])) + 1e-3
    cut_idx = []
    for i in range(1, n):
        lost = not motions[i]["valid"] or motions[i]["n"] < 40
        hard = hist_corr[i] < 0.55 or (mad_arr[i] > 6 * base and mad_arr[i] > 12)
        soft = hist_corr[i] < 0.8 and mad_arr[i] > 4 * base and lost
        if (hard or soft) and (not cut_idx or i - cut_idx[-1] > max(2, int(0.25 * fps / step))):
            cut_idx.append(i)
    # nhận diện hoà tan: màu sắc (histogram) đổi dần trong các mẫu trước cut.
    # Dùng histogram chứ không dùng sai khác điểm ảnh, vì camera đang lướt cũng tạo sai khác lớn.
    hc = np.array(hist_corr)
    cuts = []
    for i in cut_idx:
        win = hc[max(1, i - 5):i]
        gradual = len(win) >= 4 and np.sum(win < 0.93) >= 3
        cuts.append({"t": round(times[i], 3), "kind": "hoà tan/chuyển dần" if gradual else "cắt cứng"})
    # các khung tại cut không đo chuyển động (là bước nhảy hình)
    for i in cut_idx:
        motions[i] = dict(tx=0, ty=0, scale=1, rot=0, parallax=None, spread=None, n=0, valid=False)

    # ---- chuỗi tốc độ chuẩn hoá
    pan = np.array([math.hypot(m["tx"], m["ty"]) / sw * 100 / dt for m in motions])        # %W/s
    vx = np.array([m["tx"] / sw * 100 / dt for m in motions])
    vy = np.array([m["ty"] / sw * 100 / dt for m in motions])
    zoom = np.array([(m["scale"] - 1) * 100 / dt for m in motions])                        # %/s
    rot = np.array([m["rot"] / dt for m in motions])                                       # deg/s
    valid = np.array([m["valid"] for m in motions])
    # làm mượt nhẹ (cửa sổ ~0.2 s) để bỏ nhiễu tracking
    k = max(1, int(round(0.2 / dt)))
    def smooth(a):
        if k <= 1:
            return a
        return np.convolve(a, np.ones(k) / k, mode="same")
    pan_s, zoom_s, rot_s = smooth(pan), smooth(np.abs(zoom)), smooth(np.abs(rot))
    moving = (pan_s > MOVE_PAN) | (zoom_s > MOVE_ZOOM) | (rot_s > MOVE_ROT)

    # ---- theo từng cảnh
    bounds = [0] + cut_idx + [n]
    shots = []
    for si in range(len(bounds) - 1):
        a, b = bounds[si], bounds[si + 1]
        t0 = times[a]
        t1 = times[b] if b < n else duration
        seg = slice(a + 1, b)  # bỏ khung đầu cảnh
        sv = valid[seg]
        if sv.sum() < 2:
            shots.append(dict(i=si, start=round(t0, 3), end=round(t1, 3), dur=round(t1 - t0, 3), label="quá ngắn"))
            continue
        mv = moving[seg][sv]
        mvx, mvy = float(np.median(vx[seg][sv])), float(np.median(vy[seg][sv]))
        mz, mr = float(np.median(zoom[seg][sv])), float(np.median(rot[seg][sv]))
        par = [m["parallax"] for m in motions[a + 1:b] if m["parallax"] is not None]
        spr = [m["spread"] for m in motions[a + 1:b] if m["spread"] is not None]
        # dừng: đoạn liên tiếp không chuyển động >= STOP_MIN_SEC
        stops, run = 0, 0
        for v in mv:
            run = run + 1 if not v else 0
            if run == int(math.ceil(STOP_MIN_SEC / dt)):
                stops += 1
        sp = pan_s[seg][sv]
        raw = pan[seg][sv]  # chưa làm mượt: tránh rò tốc độ của cảnh bên cạnh qua điểm cắt
        nhead = max(1, int(0.15 / dt))
        head = float(np.mean(raw[:nhead])) if len(raw) else 0.0
        tail = float(np.mean(raw[-nhead:])) if len(raw) else 0.0
        med_speed = float(np.median(sp)) if len(sp) else 0.0
        parallax = float(np.median(par)) if par else None
        spread = float(np.median(spr)) if spr else None
        labels = []
        if abs(mz) > MOVE_ZOOM:
            labels.append("push-in/dolly vào" if mz > 0 else "pull-out/lùi ra")
        if abs(mvx) > MOVE_PAN:
            labels.append("pan/truck " + ("trái→phải" if mvx < 0 else "phải→trái"))  # khung trôi ngược hướng camera
        if abs(mvy) > MOVE_PAN:
            labels.append("tilt/pedestal " + ("lên" if mvy > 0 else "xuống"))
        if abs(mr) > MOVE_ROT:
            labels.append("xoay/roll")
        if not labels:
            labels.append("tĩnh" if mv.mean() < 0.3 else "trôi nhẹ")
        if (parallax or 0) >= PARALLAX_ON or (spread or 0) >= 0.6:
            labels.append("PARALLAX")
        shots.append(dict(
            i=si, start=round(t0, 3), end=round(t1, 3), dur=round(t1 - t0, 3),
            label=", ".join(labels),
            moving_frac=round(float(mv.mean()), 3), stops=stops,
            pan_pct_w_s=round(med_speed, 2), vx=round(mvx, 2), vy=round(mvy, 2),
            zoom_pct_s=round(mz, 3), rot_deg_s=round(mr, 3),
            parallax=None if parallax is None else round(parallax, 3),
            layer_spread=None if spread is None else round(spread, 3),
            enters_moving=bool(head > 0.5 * max(med_speed, MOVE_PAN)),
            exits_moving=bool(tail > 0.5 * max(med_speed, MOVE_PAN)),
            dir_out=[round(float(np.mean(vx[seg][sv][-nhead:])), 2), round(float(np.mean(vy[seg][sv][-nhead:])), 2)],
            dir_in=[round(float(np.mean(vx[seg][sv][:nhead])), 2), round(float(np.mean(vy[seg][sv][:nhead])), 2)],
        ))

    # match-move tại cut: hướng ra của cảnh trước ~ hướng vào cảnh sau
    match = []
    for s0, s1 in zip(shots, shots[1:]):
        if "dir_out" not in s0 or "dir_in" not in s1:
            continue
        a_, b_ = np.array(s0["dir_out"]), np.array(s1["dir_in"])
        if np.linalg.norm(a_) > MOVE_PAN and np.linalg.norm(b_) > MOVE_PAN:
            cos = float(a_ @ b_ / (np.linalg.norm(a_) * np.linalg.norm(b_)))
            match.append(cos)

    # ---- bảng màu (k-means 6 màu)
    palette = []
    if palette_samples:
        data = np.vstack(palette_samples).astype(np.float32)
        if len(data) > 60000:
            data = data[np.random.default_rng(1).choice(len(data), 60000, replace=False)]
        crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.5)
        _, lab, cen = cv2.kmeans(data, 6, None, crit, 3, cv2.KMEANS_PP_CENTERS)
        counts = np.bincount(lab.reshape(-1), minlength=6)
        for ci in np.argsort(-counts):
            bgr = cen[ci]
            palette.append({"hex": "#%02x%02x%02x" % (int(bgr[2]), int(bgr[1]), int(bgr[0])),
                            "share": round(float(counts[ci] / counts.sum()), 3)})

    # ---- gom cut dồn dập (≤ 0,6 s) thành MỘT lần chuyển cảnh: đó thường là transition
    # zoom-blur / flash / glitch nhiều khung, không phải nhiều cảnh thật.
    groups = []
    for c in cuts:
        if groups and c["t"] - groups[-1][-1] <= 0.6:
            groups[-1].append(c["t"])
        else:
            groups.append([c["t"]])
    starts = [0.0] + [g[0] for g in groups] + [duration]
    real = [b - a for a, b in zip(starts, starts[1:]) if b - a > 1e-3]
    transitions = [{"t": g[0], "len": round(g[-1] - g[0], 3), "kind": "burst (zoom-blur/flash)" if len(g) > 1 else "cut"}
                   for g in groups]

    # ---- tổng hợp
    vm = valid & ~np.isin(np.arange(n), cut_idx)
    durs = [s["dur"] for s in shots]
    pars = [s["parallax"] for s in shots if s.get("parallax") is not None]
    summary = dict(
        file=str(path), fps=round(fps, 3), size=[W0, H0], duration=round(duration, 3),
        aspect="dọc 9:16" if H0 > W0 * 1.5 else ("ngang 16:9" if W0 > H0 * 1.5 else f"{W0}:{H0}"),
        shots=len(shots), cuts=cuts,
        transitions=len(transitions), burst_transitions=sum(1 for t in transitions if t["len"] > 0),
        real_shot_median_sec=round(float(np.median(real)), 2), real_shot_mean_sec=round(float(np.mean(real)), 2),
        real_shot_p90_sec=round(float(np.percentile(real, 90)), 2), transition_list=transitions,
        avg_shot_sec=round(float(np.mean(durs)), 2), median_shot_sec=round(float(np.median(durs)), 2),
        continuity_moving_frac=round(float(moving[vm].mean()) if vm.any() else 0.0, 3),
        stops_total=int(sum(s.get("stops", 0) for s in shots)),
        cuts_on_motion_frac=round(float(np.mean([s.get("exits_moving", False) for s in shots[:-1]])) if len(shots) > 1 else None, 3)
        if len(shots) > 1 else None,
        match_move_cuts_frac=round(float(np.mean([c > 0.7 for c in match])), 3) if match else None,
        parallax_shots_frac=round(float(np.mean([("PARALLAX" in s.get("label", "")) for s in shots])), 3),
        parallax_median=round(float(np.median(pars)), 3) if pars else None,
        pan_speed_median_pct_w_s=round(float(np.median(pan_s[vm & moving])) if (vm & moving).any() else 0.0, 2),
        pan_speed_p90_pct_w_s=round(float(np.percentile(pan_s[vm & moving], 90)) if (vm & moving).any() else 0.0, 2),
        zoom_speed_median_pct_s=round(float(np.median(zoom_s[vm & moving])) if (vm & moving).any() else 0.0, 3),
        palette=palette,
        shot_list=shots,
    )

    # ---- hình ảnh: đồ thị chuyển động + contact sheets
    vdir = out_dir
    vdir.mkdir(parents=True, exist_ok=True)
    draw_motion_plot(vdir / "motion.png", times, pan_s, zoom_s, moving, [times[i] for i in cut_idx], duration)
    draw_sheets(vdir, thumbs, times, shots, bounds)
    (vdir / "report.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def draw_motion_plot(path, times, pan_s, zoom_s, moving, cut_t, duration):
    Wp, Hp, pad = 1600, 420, 50
    img = np.full((Hp, Wp, 3), 24, np.uint8)
    ymax = max(5.0, float(np.percentile(pan_s, 98)) * 1.2, float(np.percentile(zoom_s, 98)) * 1.2)
    X = lambda t: int(pad + (Wp - 2 * pad) * t / max(duration, 1e-6))
    Y = lambda v: int(Hp - pad - (Hp - 2 * pad) * min(v, ymax) / ymax)
    for i, t in enumerate(times):  # nền xanh = đang chuyển động
        if moving[i]:
            cv2.line(img, (X(t), pad), (X(t), Hp - pad), (40, 60, 40), 2)
    for t in cut_t:
        cv2.line(img, (X(t), pad), (X(t), Hp - pad), (60, 60, 200), 2)
    for arr, col in ((pan_s, (80, 200, 255)), (zoom_s, (255, 160, 90))):
        pts = np.array([[X(t), Y(v)] for t, v in zip(times, arr)], np.int32)
        cv2.polylines(img, [pts], False, col, 2, cv2.LINE_AA)
    cv2.putText(img, "pan %%W/s (vang)  zoom %%/s (xanh)  nen xanh = dang chuyen dong  do = cut   max=%.1f" % ymax,
                (pad, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (230, 230, 230), 1, cv2.LINE_AA)
    for s in range(0, int(duration) + 1, max(1, int(duration // 20) or 1)):
        cv2.putText(img, f"{s}s", (X(s) - 10, Hp - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (160, 160, 160), 1)
    imwrite(path, img)


def draw_sheets(vdir, thumbs, times, shots, bounds, per_sheet=8):
    th, tw = thumbs[0].shape[:2]
    rows = []
    for si in range(len(bounds) - 1):
        a, b = bounds[si], max(bounds[si] + 1, bounds[si + 1] - 1)
        picks = [a, (a + b) // 2, b]
        row = np.hstack([thumbs[min(p, len(thumbs) - 1)] for p in picks])
        bar = np.full((34, row.shape[1], 3), 16, np.uint8)
        s = shots[si]
        txt = f"#{si} {s['start']:.2f}-{s['end']:.2f}s  {ascii_label(s.get('label', ''))}"
        if s.get("parallax") is not None:
            txt += f"  par={s['parallax']}"
        if "pan_pct_w_s" in s:
            txt += f"  pan={s['pan_pct_w_s']}%W/s zoom={s['zoom_pct_s']}%/s"
        cv2.putText(bar, txt[:120], (8, 23), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (235, 235, 235), 1, cv2.LINE_AA)
        rows.append(np.vstack([bar, row]))
    for k in range(0, len(rows), per_sheet):
        imwrite(vdir / f"sheet-{k // per_sheet + 1:02d}.jpg", np.vstack(rows[k:k + per_sheet]))


def ascii_label(s: str) -> str:
    table = {"đ": "d", "Đ": "D"}
    import unicodedata
    s = "".join(table.get(c, c) for c in s)
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


# ----------------------------------------------------------------- reports
def write_reports(out: Path, results: list[dict]) -> None:
    ok = [r for r in results if "error" not in r]
    (out / "summary.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    def med(key):
        vals = [r[key] for r in ok if r.get(key) is not None]
        return round(float(np.median(vals)), 3) if vals else None

    L = ["# Tổng hợp phân tích video mẫu", "",
         "Mọi số liệu dưới đây là ĐO bằng optical flow; nhãn cảnh là phân loại tự động, hãy xác nhận bằng mắt trên sheet-*.jpg.", "",
         "Cột 'Cảnh thật': gom các cut cách nhau ≤ 0,6 s thành một lần chuyển (transition nhiều khung).", "",
         "| Video | Khung | Dài (s) | Cảnh thật (trung vị/p90 s) | Transition dồn dập | Cảnh | TB cảnh (s) | % thời gian camera chạy | Số lần dừng | Cắt khi đang chạy | Match-move | Cảnh có parallax | Pan trung vị %W/s | Zoom trung vị %/s |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        if "error" in r:
            L.append(f"| {Path(r['file']).name} | lỗi: {r['error']} ||||||||||||| ")
            continue
        L.append(f"| {Path(r['file']).name} | {r['aspect']} | {r['duration']} | "
                 f"{r['real_shot_median_sec']}/{r['real_shot_p90_sec']} | {r['burst_transitions']}/{r['transitions']} | "
                 f"{r['shots']} | {r['avg_shot_sec']} | "
                 f"{pct(r['continuity_moving_frac'])} | {r['stops_total']} | {pct(r['cuts_on_motion_frac'])} | "
                 f"{pct(r['match_move_cuts_frac'])} | {pct(r['parallax_shots_frac'])} | "
                 f"{r['pan_speed_median_pct_w_s']} | {r['zoom_speed_median_pct_s']} |")
    L += ["", "## Danh sách cảnh", ""]
    for r in ok:
        L.append(f"### {Path(r['file']).name}")
        L.append("")
        L.append("| # | Bắt đầu | Dài | Chuyển động | %chạy | Dừng | Parallax | Tách lớp | Vào/ra khi đang chạy |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for s in r["shot_list"]:
            L.append(f"| {s['i']} | {s['start']} | {s['dur']} | {s.get('label','')} | {pct(s.get('moving_frac'))} | "
                     f"{s.get('stops','')} | {s.get('parallax','')} | {s.get('layer_spread','')} | "
                     f"{'có' if s.get('enters_moving') else 'không'}/{'có' if s.get('exits_moving') else 'không'} |")
        L.append("")
        L.append("Chuyển cảnh: " + (", ".join(f"{c['t']}s {c['kind']}" for c in r["cuts"]) or "không có cắt — một cú máy liền"))
        L.append("Bảng màu: " + ", ".join(f"{p['hex']} ({pct(p['share'])})" for p in r["palette"]))
        L.append("")
    (out / "SUMMARY.md").write_text("\n".join(L), encoding="utf-8")

    pals = [p["hex"] for r in ok for p in r["palette"][:3]]
    S = ["# STYLE_DRAFT — nháp ngữ pháp hình ảnh (điền tiếp bằng mắt)", "",
         "Các dòng [ĐO] lấy từ analyze_refs.py. Các dòng [NHÌN] phải do người/agent điền sau khi xem sheet-*.jpg và video.", "",
         "## Camera",
         f"- [ĐO] % thời gian camera chuyển động (trung vị các video): {pct(med('continuity_moving_frac'))}  → mục tiêu khi dựng: ≥ con số này",
         f"- [ĐO] Khung hình: {', '.join(sorted(set(r['aspect'] for r in ok)))}",
         f"- [ĐO] Độ dài cảnh thật (đã gom transition): trung vị {med('real_shot_median_sec')} s, p90 {med('real_shot_p90_sec')} s",
         f"- [ĐO] Tốc độ pan trung vị: {med('pan_speed_median_pct_w_s')} %W/s; p90: {med('pan_speed_p90_pct_w_s')} %W/s",
         f"- [ĐO] Tốc độ zoom/dolly trung vị: {med('zoom_speed_median_pct_s')} %/s",
         f"- [ĐO] Tỉ lệ cắt khi camera đang chạy: {pct(med('cuts_on_motion_frac'))}; cắt match-move cùng hướng: {pct(med('match_move_cuts_frac'))}",
         f"- [ĐO] Tỉ lệ cảnh có parallax: {pct(med('parallax_shots_frac'))}; chỉ số parallax trung vị: {med('parallax_median')}",
         "- [NHÌN] Kiểu chuyển động chủ đạo (dolly vào toà nhà? bay ngang skyline? orbit quanh mô hình?):",
         "- [NHÌN] Số lớp độ sâu thấy được (trời / skyline xa / toà nhà giữa / tiền cảnh / chữ):",
         "- [NHÌN] Chuyển cảnh: tiền cảnh quét qua (foreground wipe)? zoom xuyên vật thể? whip?",
         "", "## Hình ảnh",
         f"- [ĐO] Màu chủ đạo: {', '.join(dict.fromkeys(pals))}",
         "- [NHÌN] Chất liệu: ảnh thật tách lớp / 3D / vector phẳng / bản đồ vệ tinh:",
         "- [NHÌN] Font tiêu đề, cỡ (% chiều cao khung), độ đậm, màu nhấn cho số tăng/giảm:",
         "- [NHÌN] Nhãn số liệu: gắn vào thế giới (world-locked) hay cố định màn hình (HUD)?",
         "- [NHÌN] Biểu đồ: loại, cách vẽ vào, camera có bay dọc đường biểu đồ không:",
         "", "## Nhịp & âm thanh",
         "- [NHÌN] Có lời dẫn? tốc độ (từ/giây). Nhạc nền kiểu gì, có SFX whoosh khi camera lướt?",
         "- [NHÌN] Hook 3 giây đầu là gì:",
         ""]
    (out / "STYLE_DRAFT.md").write_text("\n".join(S), encoding="utf-8")


def pct(v):
    return "—" if v is None else f"{round(100 * v)}%"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="thư mục hoặc file video")
    ap.add_argument("--out", default="phan-tich-video-mau", help="thư mục kết quả")
    ap.add_argument("--width", type=int, default=480, help="chiều rộng khi phân tích (px)")
    ap.add_argument("--step", type=int, default=1, help="lấy 1 khung mỗi N khung (2 = nhanh gấp đôi)")
    args = ap.parse_args()

    vids = collect_inputs(args.inputs)
    if not vids:
        sys.exit("Không có video nào.")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    results = []
    used = set()
    for v in vids:
        name = safe_name(v)
        while name in used:
            name += "_"
        used.add(name)
        print(f"→ {v.name}", flush=True)
        try:
            r = analyze_video(v, out / name, args.width, max(1, args.step))
        except Exception as e:  # một video lỗi không làm hỏng cả lô
            r = {"file": str(v), "error": repr(e)}
        if "error" in r:
            print(f"   lỗi: {r['error']}")
        else:
            print(f"   {r['shots']} cảnh, camera chạy {pct(r['continuity_moving_frac'])} thời gian, "
                  f"parallax ở {pct(r['parallax_shots_frac'])} cảnh")
        results.append(r)
    write_reports(out, results)
    print(f"\nXong: {out / 'SUMMARY.md'}  |  {out / 'STYLE_DRAFT.md'}")


if __name__ == "__main__":
    main()
```

## FILE: scripts/doc_capture.js

```javascript
// Chụp bài báo gốc làm ảnh tài liệu bằng chứng (tiêu đề, ngày, ảnh, các đoạn chứa số liệu).
// Dùng: node doc_capture.js <url> "<câu đầu tiêu đề>" "<chuỗi trong đoạn số 1>" "<chuỗi đoạn số 2>" "<chuỗi đoạn số 3>"
// Ra: article.png (2x) + article.json (vị trí tiêu đề và các đoạn, để zoom/đánh dấu). Cần host báo trong danh sách mạng.
const { chromium } = require('playwright');
const [, , URL, TITLE, P1, P2, P3] = process.argv;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 1400 }, deviceScaleFactor: 2 });
  await p.goto(URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(6000);
  // ẩn quảng cáo/popup cố định
  await p.addStyleTag({ content: '[class*=ads],[id*=ads],[class*=banner],[class*=popup],iframe,.fixed,[style*="position: fixed"]{display:none!important}' });
  await p.evaluate(() => { for (const e of document.querySelectorAll('*')) { const ps = getComputedStyle(e).position; if (ps === 'fixed' || ps === 'sticky') e.style.setProperty('display','none','important'); } });
  const info = await p.evaluate(([TITLE, P1, P2, P3]) => {
    const ps = [...document.querySelectorAll('p')];
    const find = (s) => { const el = ps.find(e => e.textContent.includes(s)); if (!el) return null; el.scrollIntoView({block:'center'}); const r = el.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height, text: el.textContent.slice(0, 80) }; };
    const tt = TITLE;
    const h1 = [...document.querySelectorAll('h1,h2,div,span')].filter(e => e.children.length === 0 && e.textContent.trim().startsWith(tt))[0]
      || [...document.querySelectorAll('*')].find(e => e.childElementCount===0 && e.textContent.includes(tt));
    h1.scrollIntoView({block:'center'}); const hr = h1.getBoundingClientRect();
    return { title: { x: hr.left + scrollX, y: hr.top + scrollY, w: hr.width, h: hr.height, text: h1.textContent.trim() },
             retail: find(P1), biz: find(P2), fdi: find(P3), docH: document.documentElement.scrollHeight };
  }, [TITLE, P1, P2, P3]);
  console.log(JSON.stringify(info, null, 1));
  await p.evaluate(() => { scrollTo(0, 0); });
  await p.waitForTimeout(800);
  await p.evaluate(() => { for (const e of document.querySelectorAll('*')) { const ps = getComputedStyle(e).position; if (ps === 'fixed' || ps === 'sticky') e.style.setProperty('display','none','important'); } });
  const top = Math.max(0, info.title.y - 70), bottom = info.fdi.y + info.fdi.h + 60;
  await p.screenshot({ path: 'article.png', fullPage: true, clip: { x: info.title.x - 6, y: top, width: info.title.w + 12, height: bottom - top } });
  require('fs').writeFileSync('article.json', JSON.stringify({ ...info, clipTop: top }, null, 1));
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
```

## FILE: scripts/earth_capture.js

```javascript
// Quay một cảnh Google Earth 3D thành chuỗi khung JPG, camera nội suy đều giữa 2 điểm (không dừng).
// Dùng:  node earth_capture.js shot.json <thư mục ra> [khung bắt đầu, để chạy tiếp]
// shot.json: {"dpr":1.5,"frames":80,"from":{lat,lng,dist,head,tilt},"to":{...}}  (10 khung = 1 giây)
//            hoặc {"dpr":1,"list":[{...},{...}],"frames":N} để chụp thử nhiều góc máy.
// dist: khoảng cách camera (m), log-nội suy; head: hướng (độ); tilt: nghiêng (độ, 0 = nhìn thẳng xuống).
// Cần mạng tới earth.google.com, kh.google.com, www.gstatic.com, www.google.com, earth-pa.clients6.google.com, htapi.google.com.
// Toạ độ click giao diện (đóng popup, Basemap -> Clean) đo ở viewport 540×960; Google đổi giao diện thì cần đo lại.
const { chromium } = require('playwright');
const fs = require('fs');
const [,, specFile, outDir, startArg] = process.argv;
const spec = JSON.parse(fs.readFileSync(specFile, 'utf8'));
if (startArg) spec.start = parseInt(startArg, 10);
fs.mkdirSync(outDir, { recursive: true });
const url = (c) => `https://earth.google.com/web/@${c.lat.toFixed(6)},${c.lng.toFixed(6)},${c.alt.toFixed(1)}a,${c.dist.toFixed(1)}d,${spec.fov || 35}y,${c.head.toFixed(2)}h,${c.tilt.toFixed(2)}t,0r`;
const lerp = (a, b, s) => a + (b - a) * s;
function cam(i) {
  if (spec.list) return Object.assign({ alt: 10 }, spec.list[i]);
  const s = spec.frames <= 1 ? 0 : i / (spec.frames - 1);
  const A = spec.from, B = spec.to;
  return { lat: lerp(A.lat, B.lat, s), lng: lerp(A.lng, B.lng, s), alt: lerp(A.alt || 10, B.alt || 10, s),
           dist: Math.exp(lerp(Math.log(A.dist), Math.log(B.dist), s)), head: lerp(A.head, B.head, s), tilt: lerp(A.tilt, B.tilt, s) };
}
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: spec.w || 540, height: spec.h || 960 }, deviceScaleFactor: spec.dpr || 2 });
  await p.goto(url(cam(spec.start || 0)), { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(45000);
  // giao diện ở 540×960 CSS px: đóng popup, chọn Basemap → Clean (không nhãn/đường/biên giới)
  await p.mouse.click(455, 228); await p.waitForTimeout(1500);
  await p.mouse.click(49, 864); await p.waitForTimeout(1000);
  await p.mouse.click(500, 40); await p.waitForTimeout(2500);
  await p.mouse.click(507, 288); await p.waitForTimeout(1500);
  await p.mouse.click(28, 28); await p.waitForTimeout(8000);
  await p.evaluate(() => { const c = document.getElementById('earth-canvas'); document.body.appendChild(c);
    c.style.cssText = 'position:fixed;left:0;top:0;width:100vw;height:100vh;z-index:2147483647;'; });
  let prev = null;
  for (let i = spec.start || 0; i < spec.frames; i++) {
    const t0 = Date.now();
    await p.evaluate((u) => { history.replaceState(null, '', u); window.dispatchEvent(new PopStateEvent('popstate')); }, url(cam(i)));
    // chờ cố định: camera dịch rất ít mỗi khung nên tile gần như đã có sẵn
    await p.waitForTimeout(i === (spec.start || 0) ? 6000 : (spec.wait || 1800));
    const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
    fs.writeFileSync(`${outDir}/f${String(i).padStart(4, '0')}.jpg`, buf);
    if (i % 10 === 0) console.log(`frame ${i}/${spec.frames} ${(Date.now() - t0)}ms`);
  }
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
```

## FILE: scripts/earth_encode.sh

```bash
#!/bin/bash
# Ghép khung Google Earth (10 fps) thành MP4 30 fps 1080x1920, nội suy chuyển động, all-intra để HyperFrames seek chính xác.
# Dùng: earth_encode.sh <thư mục khung> <file ra .mp4> [fps vào, mặc định 10]
set -e
IN="$1"; OUT="$2"; FPS="${3:-10}"
ffmpeg -loglevel error -y -framerate "$FPS" -i "$IN/f%04d.jpg" \
  -vf "scale=1080:1920:flags=lanczos,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,eq=contrast=1.05:saturation=1.05" \
  -c:v libx264 -preset medium -crf 17 -g 1 -pix_fmt yuv420p "$OUT"
```

## FILE: scripts/flight.py

```python
#!/usr/bin/env python3
"""flight.py — phong cách C "một camera, một bản đồ sống" (Animated Map Infographic) cho HyperFrames.

  python flight.py flight.json <project_dir>    # sinh compositions/map.html, hud.html, fN.html + index.html + CAMLOG.md + kiểm luật

Toàn bộ video là MỘT composition bản đồ dài suốt video với MỘT camera (vmap3.js, Hermite 5 kênh: lat, lng, Z, pitch, bearing).
Thông tin là các LỚP trên bản đồ (bật/tắt bằng sự kiện `ev`), không cắt cảnh. Footage chỉ ghé ≤ 3 s bằng zoom-through.

flight.json:
{ "duration", "audio", "gsap", "sat":[...], "points":{"k":[lng,lat]}, "blocks":"blocks.json", "blockH":{"g":m},
  "cam": [[t,lat,lng,Z,pitch,bearing], ...],
  "layers":[{id,geo,kind,w,fill,len}], "links":[{id,a,b,bend,kind,w}], "circles":[{id,pt,r_m,kind,heat,lat}],
  "rings":[{id,pt,lat,t,km,out}], "movers":[{path,t,d,icon,out}],
  "labels":[{at,lx,ly,align,big,text,small,color,t,d,xl,count}], "pins":[{at,text,t,d,left}], "ground":[{at,text,t,d,size}],
  "ev":[{t,act:"draw|show|hide|dim|grow|fade",id,d,to}],
  "hud":{"clouds":[t0,t1], "legend":[{t,d,items:[[màu,chữ]]}], "src":[{t,d,text}]},
  "foot":[{t,d,media,move,focus,src}],
  "cuts":[t,...],   # cắt cứng (tối đa 3)
  "chapters":[{t,name,V,title}] }
"""
import html, json, math, os, sys

def esc(s): return html.escape(str(s), quote=False)
def wx(lng): return (lng + 180) / 360 * 256 * 2 ** 8
def wy(lat): r = math.radians(lat); return (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * 256 * 2 ** 8
def vn(v, dec=0):
    i, _, d = f"{v:,.{dec}f}".partition("."); return i.replace(",", ".") + ("," + d if d else "")

PIN = '<svg class="pi" viewBox="0 0 44 60"><path d="M22 58 C22 58 4 34 4 20 a18 18 0 0 1 36 0 c0 14-18 38-18 38z" fill="#FACC15" stroke="#0E1A2B" stroke-width="3"/><circle cx="22" cy="20" r="7" fill="#0E1A2B"/></svg>'
PAD = [1100, 2800]

ICONS = {}   # tên icon -> SVG (Material Symbols Rounded, fill) — nạp trong main() từ thư mục `icons`
def icon_svg(name):
    if name not in ICONS: raise SystemExit(f"thiếu icon '{name}' trong thư mục icons/")
    return ICONS[name]

def badge(name, color, cls=""):
    """Huy hiệu icon tròn: glyph trắng trên màu của lớp, viền trắng mảnh, glow (một họ icon duy nhất)."""
    return f'<span class="bdg {cls}" style="--bc:{COL.get(color, color)}">{icon_svg(name)}</span>'

COL = {"adm": "#F28C28", "proj": "#2FD3E0", "green": "#4ADE80", "route": "#E04BD6", "yel": "#FACC15", "w": "#2FD3E0"}

def la_html(l, i):
    lx, ly = l.get("lx", 0), l.get("ly", -120)
    al = l.get("align") or ("l" if lx >= 0 else "r")
    gx = 12 if al == "l" else -12 if al == "r" else 0
    tr = {"l": "translate(0,-50%)", "r": "translate(-100%,-50%)", "c": "translate(-50%,-100%)" if ly < 0 else "translate(-50%,0)"}[al]
    ta = {"l": "left", "r": "right", "c": "center"}[al]
    lead = (f'<span class="lead" style="width:{math.hypot(lx, ly):.0f}px;transform:rotate({math.atan2(ly, lx):.4f}rad)"></span><span class="dot"></span>'
            if l.get("lead", True) else "")
    head = f'<div id="la{i}" class="la c-{l.get("color","w")} mlab" data-at="{l["at"]}">{lead}'
    pos = f'left:{lx + gx}px;top:{ly}px;transform:{tr};text-align:{ta}'
    if l.get("photo"):   # cửa sổ ảnh neo cạnh ghim (bản đồ vẫn thấy xung quanh)
        w, h = l.get("w", 600), l.get("h", 400)
        return (head + f'<span class="tx pwin" style="{pos};width:{w}px"><span class="pimg" style="height:{h}px">'
                f'<img id="la{i}-img" src="{l["photo"]}" alt="" style="object-position:{l.get("focus","50% 50%")}" /></span>'
                + (f'<span class="pcap">{esc(l["text"])}</span>' if l.get("text") else "") + '</span></div>')
    if l.get("logo") is not None:   # thẻ logo tổ chức: ảnh logo chính thức, hoặc huy hiệu chữ khi không có logo
        inner = (f'<img src="{l["logo"]}" alt="" />' if l["logo"] else f'<span class="mono">{esc(l.get("mono",""))}</span>')
        return (head + f'<span class="tx lcard" style="{pos}"><span class="lg">{inner}</span><span class="nm">{esc(l.get("big",""))}</span>'
                f'<span class="rl">{esc(l.get("text",""))}</span></span></div>')
    big = ""
    if l.get("big") is not None:
        big = f'<b class="{"xl" if l.get("xl") else ""}"><span class="cnt" id="la{i}-n">{esc(l["big"])}</span>{f"<u>{esc(l["unit"])}</u>" if l.get("unit") else ""}</b>'
    small = f'<small>{esc(l["small"])}</small>' if l.get("small") else ""
    ic = badge(l["icon"], l.get("color", "w"), "xl" if l.get("xl") else "") if l.get("icon") else ""
    body = f'<span class="tb">{big}{esc(l.get("text",""))}{small}</span>'
    return head + f'<span class="tx {"wi" if ic else ""}" style="{pos}">{ic}{body}</span></div>'

def build_map(F, P, tl):
    body = [f'<div class="zw" id="zw"><div class="plane" id="pl">',
            f'<svg id="mapsvg" class="map" width="{1080+2*PAD[0]}" height="{1920+PAD[1]+1400}" viewBox="0 0 {1080+2*PAD[0]} {1920+PAD[1]+1400}" '
            f'style="left:-{PAD[0]}px;top:-{PAD[1]}px" data-layout-allow-overflow><g class="world"></g></svg>', '<div id="blkhost"></div>']
    D = F["duration"]
    for i, l in enumerate(F.get("labels", [])):
        body.append(la_html(l, i))
        end = min(l["t"] + l.get("d", D), D - 0.05)
        tl.append(f'tl.fromTo("#la{i} > *", {{opacity:0}}, {{opacity:1, duration:.35}}, {l["t"]}); tl.to("#la{i} > *", {{opacity:0, duration:.35}}, {end});')
        if l.get("icon"):   # huy hiệu bật vào: 0 -> 110% -> 100% trong 0,35 s
            tl.append(f'tl.fromTo("#la{i} .bdg", {{scale:0}}, {{scale:1.1, duration:.22, ease:"power2.out"}}, {l["t"]}); tl.to("#la{i} .bdg", {{scale:1, duration:.13, ease:"power1.inOut"}}, {l["t"] + .22});')
        if l.get("photo") or l.get("logo") is not None:   # cửa sổ ảnh / thẻ logo trượt lên từ ghim
            tl.append(f'tl.fromTo("#la{i} .tx", {{y:70, scale:.85}}, {{y:0, scale:1, duration:.5, ease:"power3.out"}}, {l["t"]});')
            if l.get("photo"): tl.append(f'tl.fromTo("#la{i}-img", {{scale:1.0}}, {{scale:1.12, duration:{max(.5, end - l["t"])}, ease:"none"}}, {l["t"]});')
        if l.get("count") is not None:
            c = l["count"]; dec = c.get("dec", 0)
            tl.append(f'(() => {{ const e = document.querySelector("#la{i}-n"), o = {{v:{c["from"]}}}; '
                      f'tl.fromTo(o, {{v:{c["from"]}}}, {{v:{c["to"]}, duration:.8, ease:"power2.out", onUpdate: () => {{ e.textContent = fmt(o.v, {dec}); }}}}, {l["t"]}); }})();')
    for i, p in enumerate(F.get("pins", [])):
        body.append(f'<div id="pin{i}" class="pin {"l" if p.get("left") else ""} mlab" data-at="{p["at"]}"><div class="pw">{PIN}<span class="pl">{esc(p["text"])}</span></div></div>')
        tl.append(f'tl.fromTo("#pin{i} .pw", {{y:-90, opacity:0}}, {{y:0, opacity:1, duration:.45, ease:"bounce.out"}}, {p["t"]}); tl.to("#pin{i} .pw", {{opacity:0, duration:.3}}, {min(p["t"]+p.get("d",D), D-.05)});')
    for i, g in enumerate(F.get("ground", [])):
        sz = f' style="font-size:{g["size"]}px"' if g.get("size") else ""
        body.append(f'<div id="gt{i}" class="ground mlab" data-at="{g["at"]}"><span{sz}>{esc(g["text"])}</span></div>')
        tl.append(f'tl.fromTo("#gt{i} span", {{opacity:0, scale:.7, y:60}}, {{opacity:1, scale:1, y:0, duration:.7, ease:"expo.out"}}, {g["t"]}); '
                  f'tl.to("#gt{i} span", {{opacity:0, scale:1.08, duration:.45, ease:"power2.in"}}, {min(g["t"]+g["d"], D-.05)});')
    body.append("</div>")
    body.append('<div id="fog" style="position:absolute;left:0;right:0;top:0;height:560px;opacity:0;background:linear-gradient(180deg, #0E1A2B 0%, rgba(14,26,43,.85) 28%, rgba(14,26,43,0))"></div>')
    body.append("</div>")
    for e in F.get("ev", []):
        a, t, d = e["act"], e["t"], e.get("d", .6)
        if a == "draw":
            tl.append(f'tl.set("#{e["id"]}", {{opacity:1}}, {t}); tl.fromTo(["#{e["id"]}-core", "#{e["id"]}-glow"], {{strokeDashoffset:110}}, {{strokeDashoffset:0, duration:{d}, ease:"power2.inOut"}}, {t});')
        elif a in ("show", "dim", "fade"):
            to = e.get("to", 1 if a == "show" else .4)
            tl.append(f'tl.to("#{e["id"]}", {{opacity:{to}, duration:{d}, ease:"power1.inOut"}}, {t});')
        elif a == "hide":
            tl.append(f'tl.to("#{e["id"]}", {{opacity:0, duration:{d}, ease:"power1.inOut"}}, {t});')
        elif a == "grow":   # khối 3D mọc lên (nhóm g)
            tl.append(f'tl.to(BHo, {{"{e["id"]}":{e.get("to",1)}, duration:{d}, ease:"{e.get("ease","power3.out")}", onUpdate: () => {{ Object.assign(window.BH, BHo); if (window.__f) window.__f(); }}}}, {t});')
        elif a == "tint":   # độ đậm mặt khối nhóm g (không dùng opacity để giữ 3D)
            tl.append(f'tl.to(".blk.g-{e["id"]}", {{"--a":{e.get("to",.35)}, duration:{d}}}, {t});')
    opts = {"svg": "#mapsvg", "labels": ".mlab", "sat": F["sat"], "pad": PAD, "keys": F["cam"], "blockHost": "#blkhost",
            "layers": F.get("layers", []), "links": F.get("links", []), "circles": F.get("circles", []), "rings": F.get("rings", []),
            "movers": F.get("movers", []), "blocks": F.get("_blocks", []), "blockH": F.get("blockH", {}),
            "motionBlur": F.get("motion_blur"), "fps": F.get("fps", 30), "blurHost": "#zw"}
    pre = (f"const GEO = {open(P + '/geo.json').read()};\nObject.assign(GEO.lab, {json.dumps(F['_pts'])});\n{open(P + '/vmap3.js').read()}\n"
           f"const BHo = {json.dumps({g: 0 for g in F.get('blockH', {})})}; window.BH = Object.assign({{}}, BHo);\n"
           f"const map = makeMap3({json.dumps(opts, ensure_ascii=False)});\nconst pl = document.querySelector('#pl');\n"
           "const frame = (t) => { const c = map.apply(t); const k = 1 + c.p / 70;\n"
           "  pl.style.transform = `perspective(1600px) rotateX(${c.p.toFixed(3)}deg) rotateZ(${c.b.toFixed(3)}deg) scale(${k.toFixed(4)})`;\n"
           "  fog.style.opacity = Math.min(1, c.p / 30).toFixed(3); };\n"
           "const fog = document.querySelector('#fog');")
    tl.append("window.__f = () => frame(clock.t);")
    # đồng hồ camera thêm SAU mọi tween để mỗi lần seek, giá trị lớp (chiều cao khối…) đã cập nhật trước khi vẽ khung
    tl.append(f"const clock = {{ t: 0 }}; tl.fromTo(clock, {{ t: 0 }}, {{ t: {D}, duration: {D}, ease: 'none', onUpdate: () => frame(clock.t) }}, 0); frame(0);")
    return body, pre

def build_hud(F, tl):
    D = F["duration"]; body = []; h = F.get("hud", {})
    if h.get("clouds"):
        import random; rnd = random.Random(5); c0, c1 = h["clouds"]
        for i in range(12):
            x, y, w = rnd.randint(-500, 900), rnd.randint(-300, 1800), rnd.randint(900, 1500)
            body.append(f'<div class="cloud hcl" style="left:{x}px;top:{y}px;width:{w}px;height:{int(w*.55)}px"></div>')
        tl.append(f'tl.fromTo(".hcl", {{opacity:1, scale:1}}, {{opacity:0, scale:3.6, duration:{c1-c0}, stagger:.04, ease:"power2.in"}}, {c0});')
    for i, lg in enumerate(h.get("legend", [])):
        items = "".join(f'<div class="li">{badge(it[2], it[0], "sm") if len(it) > 2 else f"<i style=\'background:{it[0]}\'></i>"}{esc(it[1])}</div>' for it in lg["items"])
        body.append(f'<div class="legend" id="lg{i}" style="top:{lg.get("top", 1180)}px">{items}</div>')
        tl.append(f'tl.fromTo("#lg{i}", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:.4}}, {lg["t"]}); tl.to("#lg{i}", {{opacity:0, duration:.4}}, {min(lg["t"]+lg["d"], D-.05)});')
    for i, s in enumerate(h.get("src", [])):
        body.append(f'<p class="src" id="src{i}">{esc(s["text"])}</p>')
        tl.append(f'tl.fromTo("#src{i}", {{opacity:0}}, {{opacity:1, duration:.4}}, {s["t"]}); tl.to("#src{i}", {{opacity:0, duration:.4}}, {min(s["t"]+s["d"], D-.05)});')
    return body

def build_foot(f, i, tl):
    m, D = f["media"], f["d"]
    if m.endswith(".mp4"):
        media = f'<video id="fv{i}" class="clip" src="{m}" muted playsinline data-start="0" data-duration="{D}" data-media-start="{f.get("media_start",0)}" data-track-index="1" style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover"></video>'
    else:
        media = f'<img src="{m}" alt="" style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;object-position:{f.get("focus","50% 50%")}" />'
    MOV = {"push": ("{scale:1.30}", "{scale:1.08}"), "pull": ("{scale:1.08}", "{scale:1.26}"), "panL": ("{scale:1.25, x:70}", "{scale:1.25, x:-70}"),
           "panR": ("{scale:1.25, x:-70}", "{scale:1.25, x:70}"), "panU": ("{scale:1.22, y:90}", "{scale:1.22, y:-90}")}
    a, b = MOV[f.get("move", "push")]
    tl.append(f'tl.fromTo("#fm{i}", {a}, Object.assign({b}, {{duration:{D}, ease:"none"}}), 0);')
    blend = f.get("blend", .65)
    tl.append(f'tl.fromTo("#fw{i}", {{opacity:0, filter:"blur(10px)"}}, {{opacity:1, filter:"blur(0px)", duration:{blend}, ease:"power2.out"}}, 0); '
              f'tl.to("#fw{i}", {{opacity:0, filter:"blur(8px)", duration:{blend}, ease:"power2.in"}}, {D - blend});')
    return [f'<div id="fw{i}" style="position:absolute;inset:0;overflow:hidden"><div id="fm{i}" style="position:absolute;inset:0">{media}</div>'
            f'<div class="gtop"></div></div>']

def comp(cid, body, pre, tl, css, bg=True, blur=None):
    return f"""<template>
  <style>
{css}
    #root {{ position: absolute; inset: 0; overflow: hidden; {"" if bg else "background: transparent;"} }}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920"{blur or ""}>
{chr(10).join(body)}
  </div>
  <script>
    (() => {{
      const tl = gsap.timeline({{ paused: true }});
      const fmt = (v, dec) => {{ const [i, d] = v.toFixed(dec).split("."); return i.replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ".") + (d ? "," + d : ""); }};
      {pre}
{chr(10).join("      " + l for l in tl)}
      window.__timelines["{cid}"] = tl;
    }})();
  </script>
</template>
"""

def cam_sampler(K):
    """Bản Python của camera Hermite đơn điệu trong vmap3.js (để kiểm tra camera không đứng yên)."""
    T = [k[0] for k in K]; ch = [[wx(k[2]) for k in K], [wy(k[1]) for k in K], [k[3] for k in K], [k[4] if len(k) > 4 else 0 for k in K], [k[5] if len(k) > 5 else 0 for k in K]]
    def slopes(vs):
        n = len(vs); dl = [(vs[i + 1] - vs[i]) / (T[i + 1] - T[i]) for i in range(n - 1)]; m = [0.0] * n
        for i in range(1, n - 1): m[i] = 0 if dl[i - 1] * dl[i] <= 0 else (dl[i - 1] + dl[i]) / 2
        for i in range(n - 1):
            if dl[i] == 0: m[i] = m[i + 1] = 0; continue
            a, b = m[i] / dl[i], m[i + 1] / dl[i]; q = a * a + b * b
            if q > 9: t = 3 / math.sqrt(q); m[i] = t * a * dl[i]; m[i + 1] = t * b * dl[i]
        return m
    M = [slopes(v) for v in ch]
    def at(t):
        t = min(max(t, T[0]), T[-1]); i = 0
        while i < len(T) - 2 and t > T[i + 1]: i += 1
        h = T[i + 1] - T[i]; s = (t - T[i]) / h; s2, s3 = s * s, s * s * s
        return [(2*s3-3*s2+1)*v[i] + (s3-2*s2+s)*h*m[i] + (-2*s3+3*s2)*v[i+1] + (s3-s2)*h*m[i+1] for v, m in zip(ch, M)]
    return at

def validate(F, js_sample=None):
    D = F["duration"]; msg = []
    cuts = F.get("cuts", [])
    if len(cuts) > 3: msg.append(f"{len(cuts)} cắt cứng > 3")
    ft = sum(f["d"] for f in F.get("foot", []))
    for f in F.get("foot", []):
        if f["d"] > 3.0 + 1e-6: msg.append(f"footage @{f['t']}: {f['d']} s > 3 s (bản đồ biến mất quá 3 s)")
    if ft > 0.2 * D: msg.append(f"footage tổng {ft:.1f} s > 20%")
    ch = F["chapters"]; share = {}
    for a, b in zip(ch, ch[1:] + [{"t": D}]):
        share[a["V"]] = share.get(a["V"], 0) + b["t"] - a["t"]
    for a, b in zip(ch, ch[1:]):
        if a["V"] == b["V"]: msg.append(f"chương '{b['name']}' lặp kiểu {b['V']} với chương trước")
    for v, d in share.items():
        if d > 0.2 * D + 1e-6: msg.append(f"{v}: {d:.1f} s > 20%")
    # camera: dừng > 1 s / quay > 90° một lần / chuyển động thẳng đều (không ease)
    K = F["cam"]
    for a, b in zip(K, K[1:]):
        if abs((b[5] if len(b) > 5 else 0) - (a[5] if len(a) > 5 else 0)) > 90: msg.append(f"quay > 90° giữa {a[0]}–{b[0]} s")
        same = all(abs(x - y) < 1e-9 for x, y in zip(a[1:], b[1:]))
        if same and b[0] - a[0] > 1 and not F.get("allow_lock"): msg.append(f"camera đứng yên {a[0]}–{b[0]} s")
    # camera không đứng yên quá 1 s: mọi cửa sổ 1 s phải đổi Z ≥ 0,004 (~0,3% tỉ lệ) hoặc nghiêng/quay ≥ 0,15° hoặc lia ≥ 1,5 px
    at = cam_sampler(K); still = []
    t = F["cam"][0][0]
    while t + 1 <= F["cam"][-1][0]:
        a, b = at(t), at(t + 1); sc = 2 ** (a[2] - 8)
        moving = abs(b[2] - a[2]) >= .004 or abs(b[3] - a[3]) >= .15 or abs(b[4] - a[4]) >= .15 or math.hypot(b[0] - a[0], b[1] - a[1]) * sc >= 1.5
        if not moving: still.append(round(t, 1))
        t += 0.25
    if still and not F.get("allow_lock"): msg.append(f"camera gần như đứng yên > 1 s quanh {still[:6]}")
    # ---- ổn định (chống rung): tốc độ mặt đất từng khung, giữ khung đơn điệu, nghiêng có thời hạn
    fps = F.get("fps", 30); N = int(D * fps); R = 540   # R: đo tốc độ zoom/quay tại nửa bề ngang khung (540 px)
    hidden = [(f["t"] + .6, f["t"] + f["d"] - .6) for f in F.get("foot", [])]
    def spd(t0, t1):
        a, b = at(t0), at(t1); sc = 2 ** ((a[2] + b[2]) / 2 - 8)
        return (math.hypot(b[0] - a[0], b[1] - a[1]) * sc + abs(b[2] - a[2]) * math.log(2) * R
                + abs(b[4] - a[4]) * math.pi / 180 * R + abs(b[3] - a[3]) * math.pi / 180 * 900), [b[i] - a[i] for i in range(5)]
    sp = [spd(i / fps, (i + 1) / fps) for i in range(N)]
    fast = [round(i / fps, 2) for i, (v, _) in enumerate(sp) if v > F.get("max_px_frame", 25) and not any(h0 <= i / fps <= h1 for h0, h1 in hidden)]
    if fast: msg.append(f"camera nhanh hơn {F.get('max_px_frame', 25)} px/khung ở {len(fast)} khung, từ {fast[0]} s (tối đa {max(v for v, _ in sp):.1f})")
    holds = []; i = 0
    while i < N:
        if sp[i][0] < 6:
            j = i
            while j < N and sp[j][0] < 6: j += 1
            if (j - i) / fps >= 1.0:
                seg = sp[i:j]; med = sorted(v for v, _ in seg)[len(seg) // 2]
                flips = sum(1 for c in range(5) for k in range(1, len(seg)) if seg[k][1][c] * seg[k - 1][1][c] < 0 and abs(seg[k][1][c]) > 1e-7)
                tot = [sum(d[c] for _, d in seg) for c in range(5)]; sc = 2 ** (at(i / fps)[2] - 8)
                parts = {"lia": math.hypot(tot[0], tot[1]) * sc, "zoom": abs(tot[2]) * math.log(2) * R, "quay": abs(tot[4]) * math.pi / 180 * R, "nghiêng": abs(tot[3]) * math.pi / 180 * 900}
                kind = "khoá" if med < .05 else max(parts, key=parts.get)
                holds.append((i / fps, j / fps, kind, med, flips))
                per5 = flips / max(1e-6, (j - i) / fps) * 5
                if per5 > 10: msg.append(f"giữ {i/fps:.1f}–{j/fps:.1f} s: đổi chiều {flips} lần (> 10 / 5 s)")
                crawl = sum(1 for v, _ in seg if .05 <= v < 1.5) / fps   # bò dưới 1,5 px/khung (trừ đoạn khoá hẳn)
                if crawl > 1.2: msg.append(f"giữ {i/fps:.1f}–{j/fps:.1f} s có {crawl:.1f} s trôi < 1,5 px/khung → tăng trôi hoặc khoá hẳn")
            i = j
        else: i += 1
    F["_holds"] = holds
    run = 0; t0 = None
    for i in range(N):
        p_ = at(i / fps)[3]
        if p_ > 35.5:
            run += 1; t0 = t0 if t0 is not None else i / fps
        else:
            if run / fps > 4.05: msg.append(f"nghiêng > 35° kéo dài {run/fps:.1f} s từ {t0:.1f} s (tối đa 4 s)")
            run = 0; t0 = None
    # ---- mật độ minh hoạ: icon mỗi 4–6 s, ảnh mỗi 15–20 s
    ic = sorted([l["t"] for l in F.get("labels", []) if l.get("icon") or l.get("logo") is not None or l.get("photo")] + [p["t"] for p in F.get("pins", [])])
    gaps = [(a, b) for a, b in zip([1.0] + ic, ic + [D - 1]) if b - a > F.get("icon_gap", 6.0)]
    if gaps: msg.append("khoảng trống icon > 6 s: " + ", ".join(f"{a:.1f}–{b:.1f}" for a, b in gaps[:6]))
    im = sorted([l["t"] for l in F.get("labels", []) if l.get("photo")] + [f["t"] for f in F.get("foot", [])])
    gaps = [(a, b) for a, b in zip([0.0] + im, im + [D]) if b - a > F.get("img_gap", 20.0)]
    if gaps: msg.append("khoảng trống ảnh > 20 s: " + ", ".join(f"{a:.1f}–{b:.1f}" for a, b in gaps[:6]))
    imgs = sum(min(l.get("d", 3), 3) for l in F.get("labels", []) if l.get("photo")) + ft
    if imgs > 0.2 * D: msg.append(f"ảnh/footage tổng {imgs:.1f} s > 20%")
    return msg, share, ft

def main():
    F = json.load(open(sys.argv[1], encoding="utf-8")); P = sys.argv[2]
    if os.path.isdir(f"{P}/icons"):
        import re as _re
        for fn in os.listdir(f"{P}/icons"):
            if fn.endswith(".svg"):
                ICONS[fn[:-4]] = _re.sub(r'<svg[^>]*?viewBox="([^"]+)"[^>]*>', r'<svg viewBox="\1">', open(f"{P}/icons/{fn}").read()).replace("<path", '<path fill="#fff"')
    F["_pts"] = {k: [round(wx(v[0]), 3), round(wy(v[1]), 3)] for k, v in F.get("points", {}).items()}
    if F.get("blocks"): F["_blocks"] = json.load(open(F["blocks"])) if isinstance(F["blocks"], str) else F["blocks"]
    css = open(f"{P}/fonts.css").read() + open(f"{P}/motion.css").read() + open(f"{P}/flight.css").read()
    os.makedirs(f"{P}/compositions", exist_ok=True); D = F["duration"]
    tl = []; body, pre = build_map(F, P, tl)
    mb = F.get("motion_blur")   # {"shutter":180,"samples":16} -> mờ chuyển động khi render
    mbattr = ""   # mờ chuyển động do vmap3.js tự tính theo vận tốc camera (blur có sẵn của HyperFrames không thấy camera vẽ bằng thuộc tính SVG)
    open(f"{P}/compositions/map.html", "w").write(comp("map", body, pre, tl, css))
    tl = []; body = build_hud(F, tl)
    # HUD (nguồn, chú giải) cố định trên màn hình: không mờ chuyển động
    open(f"{P}/compositions/hud.html", "w").write(comp("hud", body, "", tl, css, bg=False, blur=None))
    hosts = [f'<div id="map" data-composition-id="map" data-composition-src="compositions/map.html" data-start="0" data-duration="{D}" data-track-index="1" data-width="1080" data-height="1920" style="z-index:1"></div>']
    for i, f in enumerate(F.get("foot", [])):
        tl = []; body = build_foot(f, i, tl)
        open(f"{P}/compositions/f{i}.html", "w").write(comp(f"f{i}", body, "", tl, css, bg=False))
        hosts.append(f'<div id="f{i}" data-composition-id="f{i}" data-composition-src="compositions/f{i}.html" data-start="{f["t"]}" data-duration="{f["d"]}" data-track-index="2" data-width="1080" data-height="1920" style="z-index:5"></div>')
    hosts.append(f'<div id="hud" data-composition-id="hud" data-composition-src="compositions/hud.html" data-start="0" data-duration="{D}" data-track-index="3" data-width="1080" data-height="1920" style="z-index:9"></div>')
    open(f"{P}/index.html", "w").write(f"""<!doctype html>
<html lang="vi">
  <head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
    <script src="{F.get('gsap','assets/lib/gsap.min.js')}"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0E1A2B; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920"{mbattr}>
      {chr(10).join("      " + h for h in hosts)}
      <audio id="mix" class="clip" src="{F.get('audio','assets/mix.wav')}" data-start="0" data-duration="{D}" data-track-index="30" data-volume="1"></audio>
    </div>
    <script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
""")
    msg, share, ft = validate(F)
    tc = lambda t: f"{int(t // 60)}:{t % 60:05.2f}"
    rows = ["# Camera log", "", f"Một camera liên tục · {len(F['cam'])} keyframe · cắt cứng: {len(F.get('cuts', []))} · footage {ft:.1f} s ({ft/D*100:.0f}%)", "",
            "| Timecode | Chương | Kiểu chính | Chuyển động camera | Lớp trên bản đồ | Footage |", "|---|---|---|---|---|---|"]
    ch = F["chapters"]
    for a, b in zip(ch, ch[1:] + [{"t": D}]):
        foot = "; ".join(f"{tc(f['t'])} {f.get('src','')}" for f in F.get("foot", []) if a["t"] <= f["t"] < b["t"])
        rows.append(f"| {tc(a['t'])}–{tc(b['t'])} | {esc(a['name'])} | {a['V']} | {esc(a.get('cam',''))} | {esc(a.get('layers',''))} | {esc(foot) or '—'} |")
    rows += ["", "## Keyframe camera", "", "| t (s) | lat | lng | Z | pitch | bearing |", "|---|---|---|---|---|---|"]
    rows += [f"| {k[0]} | {k[1]:.4f} | {k[2]:.4f} | {k[3]:.2f} | {k[4] if len(k)>4 else 0} | {k[5] if len(k)>5 else 0} |" for k in F["cam"]]
    rows += ["", "## Các đoạn giữ khung (≥ 1 s, < 6 px/khung)", "", "| Từ | Đến | Kiểu trôi | Tốc độ trung vị (px/khung) | Đổi chiều |", "|---|---|---|---|---|"]
    rows += [f"| {tc(a)} | {tc(b)} | {k} | {m:.2f} | {fl} |" for a, b, k, m, fl in F.get("_holds", [])]
    if F.get("assets"):
        rows += ["", "## Tài sản tải về", "", "| Tên | Nguồn (URL) | Độ phân giải | Dùng lúc | Ghi chú |", "|---|---|---|---|---|"]
        rows += [f"| {a['name']} | {a['url']} | {a.get('res','')} | {a.get('used','')} | {esc(a.get('note',''))} |" for a in F["assets"]]
    rows += ["", "## Tỉ lệ kiểu trực quan hoá (chương)", ""] + [f"- {v}: {d:.1f} s ({d/D*100:.0f}%)" for v, d in sorted(share.items())]
    rows += ["", "## Kiểm luật", ""] + ([f"- {m}" for m in msg] or ["- Đạt: ≤ 3 cắt cứng, footage ≤ 3 s/lần & ≤ 20%, không chương liền nhau trùng kiểu, mỗi kiểu ≤ 20%, không quay > 90°/lần."])
    open(f"{P}/CAMLOG.md", "w").write("\n".join(rows))
    print(f"map + hud + {len(F.get('foot', []))} footage · cắt {len(F.get('cuts', []))} · footage {ft:.1f}s")
    for m in msg: print("  !", m)

if __name__ == "__main__":
    main()
```

## FILE: scripts/geo_build.py

```python
#!/usr/bin/env python3
"""Dựng dữ liệu bản đồ vector (geo.json) cho template kinh-te-dia-phuong.

  pip install shapely scikit-image numpy pillow
  python geo_build.py config.json out/geo.json [--work work/]

Nguồn: Natural Earth 10m (admin-0, admin-1, sông) từ raw.githubusercontent.com/nvkelso/natural-earth-vector,
ảnh vệ tinh Esri World Imagery (để dò lòng sông). Cần các host đó trong danh sách mạng.

config.json (ví dụ Vĩnh Long, NQ 202/2025/QH15):
{
  "country": "VNM",
  "merge": {"Vĩnh Long": ["Vĩnh Long","Bến Tre","Trà Vinh"], "Cần Thơ": ["Can Tho","Sóc Trăng","Hau Giang"],
            "TP.HCM": ["Hồ Chí Minh city","Bình Dương","Bà Rịa - Vũng Tàu"], "Đồng Tháp": ["Ðong Tháp","Tiền Giang"],
            "An Giang": ["An Giang","Kiên Giang"], "Cà Mau": ["Cà Mau","Bạc Liêu"], "Tây Ninh": ["Tây Ninh","Long An"]},
  "focus": "Vĩnh Long", "compare": ["TP.HCM", "Cần Thơ"],
  "region": ["Vĩnh Long","Cần Thơ","An Giang","Đồng Tháp","Cà Mau"],
  "points": {"pt_hcm": [106.7009,10.7769], "pt_ct": [105.7469,10.0452], "pt_vl": [105.9722,10.2537], "region": [105.55,9.85]},
  "label_points": {"rv_tien": [106.33,10.335], "rv_hau": [105.60,10.25]},
  "rivers": {
    "tien": {"ne_name": "Mekong", "ne_end": [106.118663,10.237576], "cut_at": [105.9105,10.2764], "trace_to": [106.78,10.215]},
    "hau":  {"ne_name": "Mekong", "ne_end": [105.837983,10.004991], "trace_from": [105.838,10.005], "trace_to": [106.36,9.57]}
  },
  "coast_axis": [[106.80,10.24],[106.33,9.56]],
  "satellite": {"z": 10, "bbox": [104.4, 8.6, 107.8, 12.0]}
}
Tên tỉnh trong "merge" phải đúng như Natural Earth (in ra bằng --list). Luôn xem `work/rivers_preview.jpg` trước khi dùng.
"""
import argparse, io, json, math, os, sys, urllib.request
import concurrent.futures as cf

NE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
UA = {"User-Agent": "geo-build/1.0"}
Z = 8; N = 256 * 2 ** Z

def fetch(url, path):
    if not os.path.exists(path):
        urllib.request.urlretrieve(url, path)
    return path

def mx(lng, z=Z): return (lng + 180) / 360 * 256 * 2 ** z
def my(lat, z=Z):
    r = math.radians(lat); return (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * 256 * 2 ** z
def inv(x, y, z):
    n = 256 * 2 ** z; return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n)))), x / n * 360 - 180

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("config"); ap.add_argument("out"); ap.add_argument("--work", default="work")
    ap.add_argument("--list", action="store_true", help="in tên tỉnh Natural Earth của nước rồi thoát")
    a = ap.parse_args()
    from shapely.geometry import shape, mapping, Point, LineString
    from shapely.ops import unary_union, substring
    C = json.load(open(a.config, encoding="utf-8")); os.makedirs(a.work, exist_ok=True)
    adm1 = json.load(open(fetch(NE + "ne_10m_admin_1_states_provinces.geojson", f"{a.work}/adm1.geojson"), encoding="utf-8"))
    prov = {f["properties"]["name"]: shape(f["geometry"]).buffer(0) for f in adm1["features"] if f["properties"].get("adm0_a3") == C["country"]}
    if a.list:
        print("\n".join(sorted(prov))); return
    adm0 = json.load(open(fetch(NE + "ne_10m_admin_0_countries.geojson", f"{a.work}/adm0.geojson"), encoding="utf-8"))
    country = [shape(f["geometry"]) for f in adm0["features"] if f["properties"].get("ADM0_A3") == C["country"]][0]

    # 1. gộp tỉnh
    G = {k: unary_union([prov[x].buffer(0.003) for x in v]).buffer(-0.003).simplify(0.003) for k, v in C["merge"].items()}
    P = lambda c: f"{mx(c[0]):.1f} {my(c[1]):.1f}"
    ring = lambda cs: "M" + " L".join(P(c) for c in cs) + "Z"
    def poly_d(g, min_area=0.0005):
        ps = [g] if g.geom_type == "Polygon" else list(g.geoms)
        return " ".join(ring(p.exterior.coords) + "".join(ring(i.coords) for i in p.interiors) for p in ps if p.area >= min_area)
    line_d = lambda cs: "M" + " L".join(P(c) for c in cs)
    out = {"Z": Z, "prov": {k: poly_d(g) for k, g in G.items()}, "lab": {}}
    out["prov"]["_vn"] = poly_d(country.simplify(0.008), 0.02)
    for k, g in G.items():
        p = g.representative_point(); out["lab"][k] = [round(mx(p.x), 1), round(my(p.y), 1)]
    if C.get("region"): out["region"] = poly_d(unary_union([G[k] for k in C["region"]]).buffer(0.01).buffer(-0.01), 0.01)
    for k, (lng, lat) in {**C.get("points", {}), **C.get("label_points", {})}.items():
        out["lab"][k] = [round(mx(lng), 1), round(my(lat), 1)]

    # 1b. đường/kênh/ranh dự án khai báo bằng toạ độ: "lines": {"ql13": [[lng,lat],...]}, "polys": {"site": [[lng,lat],...]}
    out["lines"] = {k: line_d(v) for k, v in C.get("lines", {}).items()}
    for k, v in C.get("polys", {}).items():
        out["lines"][k] = line_d(v) + "Z"
    # 2. sông: nhánh Natural Earth (cắt) + dò tiếp ra cửa biển trên ảnh vệ tinh (tuỳ chọn)
    if not C.get("rivers"):
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        json.dump(out, open(a.out, "w", encoding="utf-8")); print(f"{a.out}: {len(G)} vùng, {len(out['lines'])} đường"); return
    import numpy as np
    from PIL import Image, ImageDraw
    from skimage.graph import route_through_array
    sat = C["satellite"]; z = sat["z"]; w, s_, e, n_ = sat["bbox"]
    x0, x1 = int(mx(w, z) // 256), int(mx(e, z) // 256); y0, y1 = int(my(n_, z) // 256), int(my(s_, z) // 256)
    img = Image.new("RGB", (256 * (x1 - x0 + 1), 256 * (y1 - y0 + 1)))
    def tile(xy):
        x, y = xy; u = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
        return xy, Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read())).convert("RGB")
    with cf.ThreadPoolExecutor(8) as ex:
        for (x, y), t in ex.map(tile, [(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]):
            img.paste(t, (256 * (x - x0), 256 * (y - y0)))
    k = 2; arr = np.asarray(img).astype(float)[::k, ::k]
    R, Gc, B = arr[..., 0], arr[..., 1], arr[..., 2]
    water = (R > Gc) & (Gc > B) & (R > 95) & ((R - B) > 25) & (Gc > 70)   # nước phù sa nâu nhạt
    cost = np.where(water, 1.0, 25.0)
    pix = lambda lng, lat: (int((my(lat, z) - 256 * y0) / k), int((mx(lng, z) - 256 * x0) / k))
    def trace(a_, b_):
        path, _ = route_through_array(cost, pix(*a_), pix(*b_), fully_connected=True, geometric=True)
        return [[round(ln, 5), round(la, 5)] for la, ln in (inv(c * k + 256 * x0, r * k + 256 * y0, z) for r, c in path[::3])]
    rv = json.load(open(fetch(NE + "ne_10m_rivers_lake_centerlines.geojson", f"{a.work}/rivers.geojson"), encoding="utf-8"))
    pv = img.copy(); dr = ImageDraw.Draw(pv)
    for name, cfg in C.get("rivers", {}).items():
        ne = [shape(f["geometry"]) for f in rv["features"] if f["properties"].get("name") == cfg["ne_name"]][0]
        part = min(ne.geoms, key=lambda p: Point(p.coords[-1]).distance(Point(cfg["ne_end"])))
        if "cut_at" in cfg:
            part = substring(part, 0, part.project(Point(cfg["cut_at"])))
        start = cfg.get("trace_from", cfg.get("cut_at"))
        pts = [list(c) for c in part.coords] + trace(tuple(start), tuple(cfg["trace_to"]))[1:]
        pts = [list(c) for c in LineString(pts).simplify(0.004).coords]
        out[name] = line_d(pts)
        dr.line([(mx(x, z) - 256 * x0, my(y, z) - 256 * y0) for x, y in pts], fill=(80, 200, 255), width=6)
    pv.resize((pv.width // 2, pv.height // 2)).save(f"{a.work}/rivers_preview.jpg")

    # 3. dải ven biển của tỉnh trọng tâm: điểm ranh giới gần trục bờ biển
    if "coast_axis" in C:
        g = G[C["focus"]]; big = max(g.geoms, key=lambda p: p.area) if g.geom_type != "Polygon" else g
        axis = LineString(C["coast_axis"])
        pts = sorted([p for p in big.exterior.coords if axis.distance(Point(p)) < 0.06], key=lambda p: axis.project(Point(p)))
        line = [pts[0]]
        for p in pts[1:]:
            if Point(p).distance(Point(line[-1])) < 0.12: line.append(p)
        out["coast"] = line_d(line)
        m = LineString(line).interpolate(0.45, normalized=True); out["lab"]["coast"] = [round(mx(m.x), 1), round(my(m.y), 1)]
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w", encoding="utf-8"))
    print(f"{a.out}: {len(G)} tỉnh, sông {list(C.get('rivers', {}))}; xem {a.work}/rivers_preview.jpg")

if __name__ == "__main__":
    main()
```

## FILE: scripts/make_music.py

```python
#!/usr/bin/env python3
"""Nhạc nền beat rõ, tổng hợp tất định (không bản quyền) để dựng theo nhịp.

  python make_music.py out.wav --dur 257.44 [--bpm 100] [--seed 3]

In ra danh sách mốc beat (giây) vào out.beats.json để cắt cảnh/SFX theo nhịp.
Cấu trúc: intro 2 nhịp (pad) -> groove (kick 1&3, clap 2&4, hi-hat 1/8, bass theo hợp âm Am–F–C–G) -> outro nhỏ dần.
"""
import argparse, json, wave
import numpy as np

SR = 48000

def env(n, a=0.005, r=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / r)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("--dur", type=float, required=True)
    ap.add_argument("--bpm", type=float, default=100); ap.add_argument("--seed", type=int, default=3)
    a = ap.parse_args(); rng = np.random.default_rng(a.seed)
    n = int(a.dur * SR); L = np.zeros(n); R = np.zeros(n)
    beat = 60 / a.bpm; bar = 4 * beat
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G (MIDI)
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    def add(sig, t0, pan=0.0, g=1.0):
        i = int(t0 * SR); j = min(n, i + len(sig))
        if i >= n or j <= i: return
        L[i:j] += sig[: j - i] * g * (1 - pan) ; R[i:j] += sig[: j - i] * g * (1 + pan)
    kick_n = int(0.35 * SR); tk = np.arange(kick_n) / SR
    kick = np.sin(2 * np.pi * np.cumsum(50 + 110 * np.exp(-tk * 30)) / SR) * env(kick_n, 0.002, 0.12)
    clap_n = int(0.25 * SR); clap = rng.standard_normal(clap_n) * env(clap_n, 0.002, 0.06)
    clap = np.convolve(clap, np.ones(6) / 6, "same")
    hat_n = int(0.06 * SR); hat = np.diff(rng.standard_normal(hat_n + 1)) * env(hat_n, 0.001, 0.015)
    beats = []
    t = 0.0; k = 0
    while t < a.dur:
        b = k % 4; barno = k // 4; intro = barno < 2; outro = t > a.dur - 2 * bar
        beats.append(round(t, 4))
        if not intro:
            g = 0.5 if outro else 1.0
            if b in (0, 2): add(kick, t, 0, 0.9 * g)
            if b in (1, 3): add(clap, t, 0.1, 0.28 * g)
            add(hat, t + beat / 2, -0.3, 0.16 * g); add(hat, t, -0.3, 0.09 * g)
        if b == 0:  # hợp âm + bass mỗi ô nhịp
            ch = chords[barno % 4]; dn = int(bar * SR); tt = np.arange(dn) / SR
            pad = sum(np.sin(2 * np.pi * hz(m) * tt + 0.3 * np.sin(2 * np.pi * 0.2 * tt)) for m in ch) / 3
            pad *= np.minimum(1, tt / 0.6) * np.minimum(1, (bar - tt) / 0.6)
            add(pad, t, 0.0, 0.10)
            if not intro:
                for q in range(8):
                    bn = int(beat / 2 * SR); tb = np.arange(bn) / SR
                    bs = np.tanh(2.2 * np.sin(2 * np.pi * hz(ch[0] - 24) * tb)) * env(bn, 0.004, 0.18)
                    add(bs, t + q * beat / 2, 0, 0.22 * (0.5 if outro else 1))
        t += beat; k += 1
    fade = np.ones(n); fo = int(3 * SR); fade[-fo:] = np.linspace(1, 0, fo); fi = int(1.5 * SR); fade[:fi] = np.linspace(0, 1, fi)
    st = np.stack([L * fade, R * fade], 1); st /= np.max(np.abs(st)) + 1e-9; st *= 0.9
    with wave.open(a.out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
    json.dump({"bpm": a.bpm, "beats": beats}, open(a.out.rsplit(".", 1)[0] + ".beats.json", "w"))
    print(f"{a.out}: {a.dur:.1f} s, {a.bpm} BPM, {len(beats)} beat")

if __name__ == "__main__":
    main()
```

## FILE: scripts/make_sfx.py

```python
#!/usr/bin/env python3
"""Tạo SFX tổng hợp, tất định, không bản quyền: whoosh, pop, riser (48 kHz, stereo WAV)."""
import numpy as np, wave, sys, os
SR = 48000
rng = np.random.default_rng(7)
def write(name, x):
    x = np.clip(x / (np.max(np.abs(x)) + 1e-9) * 0.89, -1, 1)
    st = np.stack([x, x], 1) if x.ndim == 1 else x
    with wave.open(name, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())
def onepole_lp(x, fc):  # fc: mảng tần số cắt theo thời gian
    y = np.zeros_like(x); a = np.exp(-2 * np.pi * fc / SR); s = 0.0
    for i in range(len(x)):
        s = (1 - a[i]) * x[i] + a[i] * s; y[i] = s
    return y
def whoosh(dur=0.55):
    n = int(SR * dur); t = np.linspace(0, 1, n)
    noise = rng.standard_normal(n)
    fc = 300 + 5200 * np.sin(np.pi * t) ** 2          # quét lên rồi xuống
    lp = onepole_lp(noise, fc); hp = lp - onepole_lp(lp, np.full(n, 180.0))
    env = np.sin(np.pi * t) ** 1.6
    pan = np.sin(np.pi * t)
    x = hp * env
    return np.stack([x * (1.1 - pan * 0.5), x * (0.6 + pan * 0.5)], 1)
def pop(dur=0.12):
    n = int(SR * dur); t = np.arange(n) / SR
    f = 1250 * np.exp(-t * 28) + 420
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 38) + 0.25 * rng.standard_normal(n) * np.exp(-t * 300)
def riser(dur=1.4):
    n = int(SR * dur); t = np.linspace(0, 1, n)
    f = 180 * (2 ** (t * 2.6)); ph = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sin(ph) + 0.4 * np.sin(2 * ph)
    noise = onepole_lp(rng.standard_normal(n), 400 + 6000 * t ** 2)
    env = t ** 2.2
    return (0.55 * tone + 0.8 * noise) * env
os.makedirs("out", exist_ok=True)
write("out/whoosh.wav", whoosh()); write("out/pop.wav", pop()); write("out/riser.wav", riser())
print("ok")
```

## FILE: scripts/mb_post.py

```python
#!/usr/bin/env python3
"""mb_post.py — mờ chuyển động THẬT theo vận tốc camera, làm sau render (giữ nguyên 30 fps, không đổi tốc khung).

  python mb_post.py flight.json raw.mp4 out.mp4 [--shutter 180] [--min 2] [--samples 16]

Vì sao làm sau: lọc mờ trong trình duyệt trên cảnh 3D + ảnh vệ tinh lớn làm render chậm ~7 lần (≈ 6 giờ / 2 phút video).
Ở đây mỗi khung lấy vận tốc camera từ đúng đường Hermite của vmap3.js (cam_sampler trong flight.py), quy ra vector màn hình
(theo bearing, phóng theo pitch), độ dài vệt L = vận tốc × shutter/360. L < min px → giữ nguyên khung (khung đứng/trôi chậm sắc nét).
Kernel đường thẳng ≥ `samples` mẫu, khử răng cưa; zoom/quay thêm vệt đều nhỏ. Vùng UI cố định (dòng nguồn, chú giải, đoạn footage)
được giữ sắc: dòng nguồn y 1380–1450 và các đoạn `foot` không bị làm mờ.
"""
import argparse, json, math, subprocess, sys, os
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flight import cam_sampler

ap = argparse.ArgumentParser()
ap.add_argument("flight"); ap.add_argument("raw"); ap.add_argument("out")
ap.add_argument("--shutter", type=float, default=180); ap.add_argument("--min", type=float, default=2.0); ap.add_argument("--samples", type=int, default=16); ap.add_argument("--offset", type=float, default=0, help="giây bắt đầu nếu raw là đoạn --start")
a = ap.parse_args()
F = json.load(open(a.flight)); at = cam_sampler(F["cam"]); fps = F.get("fps", 30)
W, H = 1080, 1920
foot = [(f["t"], f["t"] + f["d"]) for f in F.get("foot", [])]
keep = [(1380, 1450)]                                    # dải dòng nguồn (UI màn hình) giữ sắc

def vel(t):
    p, q = at(t - 0.5 / fps), at(t + 0.5 / fps); s = 2 ** ((p[2] + q[2]) / 2 - 8)
    br = math.radians((p[4] + q[4]) / 2); mx, my = (q[0] - p[0]) * s, (q[1] - p[1]) * s
    vx = mx * math.cos(br) - my * math.sin(br); vy = (mx * math.sin(br) + my * math.cos(br)) * (1 + (p[3] + q[3]) / 2 / 90)
    rad = (abs(q[2] - p[2]) * math.log(2) * 540 + abs(q[4] - p[4]) * math.pi / 180 * 540) * 0.5
    return -vx, -vy, rad                                  # cảnh trôi NGƯỢC chiều camera

def kernel(dx, dy, n):
    L = math.hypot(dx, dy); size = int(math.ceil(L)) | 1; size = max(size, 3)
    k = np.zeros((size, size), np.float32); c = (size - 1) / 2
    for i in range(n):                                    # n mẫu dọc vệt, nội suy song tuyến (khử răng cưa)
        f = i / (n - 1) - 0.5; x, y = c + dx * f, c + dy * f; x0, y0 = int(x), int(y); fx, fy = x - x0, y - y0
        for (xx, yy, w) in ((x0, y0, (1 - fx) * (1 - fy)), (x0 + 1, y0, fx * (1 - fy)), (x0, y0 + 1, (1 - fx) * fy), (x0 + 1, y0 + 1, fx * fy)):
            if 0 <= xx < size and 0 <= yy < size: k[yy, xx] += w
    return k / k.sum()

dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.raw, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-i", a.raw,
                        "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", a.out], stdin=subprocess.PIPE)
n = 0; blurred = 0; Lmax = 0
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    t = a.offset + n / fps; img = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    vx, vy, rad = vel(t); sh = a.shutter / 360
    dx, dy = vx * sh, vy * sh; L = math.hypot(dx, dy) + rad * sh
    if L >= a.min and not any(f0 + .1 <= t <= f1 - .1 for f0, f1 in foot):
        if math.hypot(dx, dy) < 1e-3: dx = L
        else: dx, dy = dx * L / math.hypot(dx, dy), dy * L / math.hypot(dx, dy)
        out = cv2.filter2D(img, -1, kernel(dx, dy, max(a.samples, int(L) + 1)), borderType=cv2.BORDER_REPLICATE)
        for y0, y1 in keep: out[y0:y1] = img[y0:y1]
        img = out; blurred += 1; Lmax = max(Lmax, L)
    enc.stdin.write(np.ascontiguousarray(img).tobytes()); n += 1
enc.stdin.close(); enc.wait(); dec.wait()
print(f"{n} khung · làm mờ {blurred} khung ({blurred / max(n,1) * 100:.0f}%) · vệt dài nhất {Lmax:.1f} px · shutter {a.shutter}°")
```

## FILE: scripts/mix_audio.py

```python
#!/usr/bin/env python3
"""Trộn giọng đọc + SFX và chuẩn hoá loudness cho video mạng xã hội.

  python mix_audio.py voice.mp3 events.json out.wav [--sfx-below 14] [--lufs -14] [--tp -1]

events.json: [{"t": 27.9, "sfx": "whoosh.wav"}, {"t": 37.9, "sfx": "pop.wav", "db": -2}, ...]
  - "t" giây trên trục thời gian video; "db" chỉnh thêm cho riêng sự kiện (mặc định 0).
  - Mức SFX tự đặt = loudness giọng đọc − sfx-below (mặc định 14 dB, yêu cầu ≥ 12 dB).
Kết quả: WAV 48 kHz stereo, đã loudnorm 2 lượt về -14 LUFS, true peak ≤ -1 dBTP; in ra số đo kiểm chứng.
Cần ffmpeg, numpy.
"""
import argparse, json, re, subprocess, sys, wave
import numpy as np

SR = 48000

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True)

def decode(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()

def lufs_of(x):
    """Loudness tích hợp (LUFS) của mảng stereo, qua ffmpeg ebur128. Âm ngắn < 0,4 s: lặp lại để đo được."""
    if len(x) < SR * 3:
        reps = int(np.ceil(SR * 3 / max(len(x), 1)))
        x = np.concatenate([np.concatenate([x, np.zeros((SR // 2, 2), np.float32)])] * reps)
    p = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                        "-af", "ebur128=peak=true", "-f", "null", "-"], input=x.astype(np.float32).tobytes(),
                       capture_output=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", p.stderr.decode())
    return float(m[-1]) if m else -70.0

def write_wav(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("voice"); ap.add_argument("events"); ap.add_argument("out")
    ap.add_argument("--sfx-below", type=float, default=12.0)
    ap.add_argument("--lufs", type=float, default=-14.0)
    ap.add_argument("--tp", type=float, default=-1.0)
    ap.add_argument("--duration", type=float, default=None, help="độ dài video (s); mặc định = giọng đọc")
    ap.add_argument("--music", default=None, help="nhạc nền (wav/mp3); tự ducking khi có giọng")
    ap.add_argument("--music-below", type=float, default=18.0, help="nhạc thấp hơn giọng bao nhiêu dB (mặc định 18)")
    a = ap.parse_args()

    vo = decode(a.voice)
    n = int(SR * a.duration) if a.duration else len(vo)
    mix = np.zeros((max(n, len(vo)), 2), np.float32)
    mix[:len(vo)] += vo
    L_vo = lufs_of(vo)
    target_sfx = L_vo - a.sfx_below
    events = json.load(open(a.events, encoding="utf-8"))
    base = a.events.rsplit("/", 1)[0] + "/" if "/" in a.events else ""
    cache = {}
    for e in events:
        f = e["sfx"] if e["sfx"].startswith("/") else base + e["sfx"]
        if f not in cache:
            s = decode(f); cache[f] = (s, lufs_of(s))
        s, L = cache[f]
        g = 10 ** ((target_sfx - L + e.get("db", 0)) / 20)
        i = int(e["t"] * SR)
        j = min(len(mix), i + len(s))
        if i < len(mix):
            mix[i:j] += s[: j - i] * g
    mix = mix[:n] if a.duration else mix
    if a.music:
        mu = decode(a.music)[: len(mix)]
        if len(mu) < len(mix): mu = np.concatenate([mu, np.zeros((len(mix) - len(mu), 2), np.float32)])
        Lm = lufs_of(mu); mu *= 10 ** ((L_vo - a.music_below - Lm) / 20)
        # ducking: giảm thêm 6 dB khi giọng đang nói (bao RMS 60 ms, nhả 300 ms)
        v = np.abs(np.pad(vo, ((0, max(0, len(mix) - len(vo))), (0, 0)))[: len(mix)]).mean(1)
        w = int(0.06 * SR); envv = np.convolve(v, np.ones(w) / w, "same")
        talk = (envv > 0.02).astype(np.float32); rel = int(0.3 * SR)
        talk = np.convolve(talk, np.ones(rel) / rel, "same").clip(0, 1)
        mix += mu * (1 - 0.5 * talk)[:, None]
        print(f"nhạc nền: {Lm:.1f} LUFS -> {L_vo - a.music_below:.1f} LUFS, ducking -6 dB khi có giọng")
    tmp = a.out + ".pre.wav"
    write_wav(tmp, mix / max(1.0, float(np.max(np.abs(mix)))))

    # loudnorm 2 lượt
    p = run(["ffmpeg", "-hide_banner", "-i", tmp, "-af", f"loudnorm=I={a.lufs}:TP={a.tp}:LRA=11:print_format=json", "-f", "null", "-"])
    st = json.loads(re.findall(r"\{[^{}]+\}", p.stderr)[-1])
    af = (f"loudnorm=I={a.lufs}:TP={a.tp}:LRA=11:measured_I={st['input_i']}:measured_TP={st['input_tp']}:"
          f"measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:linear=true,"
          f"alimiter=limit={10 ** ((a.tp - 0.3) / 20):.4f}:level=disabled")
    run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-af", af, "-ar", str(SR), a.out])
    # đo kiểm chứng
    p = run(["ffmpeg", "-hide_banner", "-i", a.out, "-af", "ebur128=peak=true", "-f", "null", "-"])
    I = re.findall(r"I:\s+(-?[\d.]+) LUFS", p.stderr)[-1]
    TP = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", p.stderr)[-1]
    print(f"giọng đọc {L_vo:.1f} LUFS | SFX đặt ở {target_sfx:.1f} LUFS (thấp hơn {a.sfx_below} dB) | {len(events)} sự kiện")
    print(f"KẾT QUẢ: {I} LUFS, true peak {TP} dBTP -> {a.out}")
    if float(I) < a.lufs - 1 or float(I) > a.lufs + 1 or float(TP) > a.tp:
        print("CẢNH BÁO: chưa đạt chuẩn loudness", file=sys.stderr); sys.exit(2)

if __name__ == "__main__":
    main()
```

## FILE: scripts/motion.py

```python
#!/usr/bin/env python3
"""motion.py — storyboard shot-by-shot -> project HyperFrames phong cách "bản đồ + footage" điện ảnh.

  python motion.py shots.json <project_dir>          # sinh compositions/ + index.html + SHOTLIST.md + kiểm tra luật

Project cần: fonts.css, assets/fonts, motion.css (design/), vmap2.js (scripts/), geo.json (geo_build.py), audio.
Mỗi shot khai báo "fx" (mã thư viện M1–M10, T1–T5, F1–F3, D1–D6) để bộ kiểm tra soát lặp/tỉ lệ.

shots.json: { "duration": s, "audio": "assets/mix.wav", "gsap": "...", "points": {"key": [lng,lat]},
  "sat": [{img,z,x0,y0,w,h,show}], "shots": [ {
    "id","start","dur","kind":"map|foot|card","fx":[..],"src":"nguồn (cho shot list)",
    "enter":"T1|T2|T3|T4|T5|DIS", "seg","foot","dim":0..0.7,
    "media":"assets/x.mp4|jpg", "move":"push|pull|panL|panR|panU|panD|none", "media_start":0,
    "kw":[{"t","d","lines":["CHỮ","*NHẤN"],"pos":"low|mid|high","accent":"#hex"}],          F3
    "big":{"t","d","num","dec","unit","label","pos","accent"},                              D1
    "bar":{"t","d","label","value","max","unit","sub"},                                     D2
    "timeline":{"t","y","events":[{"t","date","text","x"}]},                                D5
    "wall":{"t","top","tiles":[{"t","name","sub","hl"}]},                                   D6
    "stack":{"t","top","rows":[{"t","num","dec","unit","label"}]},                         D4
    "callouts":[{"x","y","lx","ly","align","big","text","small","color","t","d"}],         (toạ độ màn hình)
    map: "keys":[[t,lat,lng,Z(,carry)]], "tilt":[t0,t1,a0,a1], "orbit":[t0,t1,a0,a1], "clouds":[t0,t1], "zoomBlur":true,
         "layers":[{geo,kind,fill,id,w,len}], "links":[{a,b,bend,kind,id,w}], "movers":[{path,t,d,icon}],
         "rings":[{pt,lat,t,km:[..]}], "pins":[{at,text,t,left}], "ground":[{at,text,t,d}],
         "labels":[{at,lx,ly,align,big,text,small,color,t,d}], "show":[{id,t,d,to}], "hide":[{id,t,d}], "draw":[{id,t,d}]
  } ] }
Thời gian trong shot là cục bộ (0 = start danh nghĩa). T1/T4/DIS tự bắt đầu sớm 0,35 s để hoà/che lên shot trước.
"""
import html, json, math, os, sys

OVER = 0.35
FOOTAGE, MAP, DATA = "foot", "map", "card"

def esc(s): return html.escape(str(s), quote=False)
def vn(v):
    """Số kiểu Việt: 30.000 · 49,5"""
    i, _, d = (f"{v:,.{len(str(v).split('.')[1]) if isinstance(v, float) else 0}f}").partition(".")
    return i.replace(",", ".") + ("," + d if d else "")
def wx(lng): return (lng + 180) / 360 * 256 * 2 ** 8
def wy(lat): r = math.radians(lat); return (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * 256 * 2 ** 8

def words(lines):
    out = []
    for ln in lines:
        ws = [(f'<em><span class="w">{esc(w[1:])}</span></em>' if w.startswith("*") else f'<span class="w">{esc(w)}</span>') for w in ln.split()]
        out.append('<span class="ln">' + " ".join(ws) + "</span>")
    return "".join(out)

def la_html(l, i, sid, mapped):
    lx, ly = l.get("lx", 0), l.get("ly", -120)
    al = l.get("align") or ("l" if lx >= 0 else "r")
    gx = 12 if al == "l" else -12 if al == "r" else 0
    tr = {"l": "translate(0,-50%)", "r": "translate(-100%,-50%)", "c": "translate(-50%,-100%)" if ly < 0 else "translate(-50%,0)"}[al]
    ta = {"l": "left", "r": "right", "c": "center"}[al]
    big = f'<b>{esc(l["big"])}</b>' if l.get("big") else ""
    small = f'<small>{esc(l["small"])}</small>' if l.get("small") else ""
    pos = f'data-at="{l["at"]}"' if mapped else f'style="transform: translate({l["x"]}px, {l["y"]}px)"'
    return (f'<div id="{sid}-la{i}" class="la c-{l.get("color","adm")} {sid}-lab" {pos}>'
            f'<span class="lead" style="width:{math.hypot(lx, ly):.0f}px;transform:rotate({math.atan2(ly, lx):.4f}rad)"></span><span class="dot"></span>'
            f'<span class="tx" style="left:{lx + gx}px;top:{ly}px;transform:{tr};text-align:{ta}">{big}{esc(l.get("text",""))}{small}</span></div>')

PIN_SVG = '<svg class="pi" viewBox="0 0 44 60"><path d="M22 58 C22 58 4 34 4 20 a18 18 0 0 1 36 0 c0 14-18 38-18 38z" fill="#FACC15" stroke="#0E1A2B" stroke-width="3"/><circle cx="22" cy="20" r="7" fill="#0E1A2B"/></svg>'
PLANE_SVG = '<svg class="plane-ic" viewBox="0 0 100 100"><path d="M50 6 L56 40 L92 58 L92 64 L56 54 L54 80 L64 88 L64 92 L50 88 L36 92 L36 88 L46 80 L44 54 L8 64 L8 58 L44 40 Z" fill="#fff" stroke="#0E1A2B" stroke-width="2"/></svg>'

def shot_html(sh, P, prev):
    sid, dur = sh["id"], sh["dur"]
    off = OVER if sh.get("enter") in ("T1", "T4", "DIS") else 0.0
    D = dur + off
    T = lambda t: round(t + off, 3)
    endtxt = round(D - 0.32, 3)
    css = [open(f"{P}/fonts.css").read(), open(f"{P}/motion.css").read()]
    body, tl, pre = [], [], ""
    kind = sh["kind"]
    # ---------- nền
    if kind == MAP:
        body.append(f'<div id="{sid}-z" class="zw"><div id="{sid}-pl" class="plane">'
                    + (f'<svg id="{sid}-map" class="map" width="2400" height="3700" viewBox="0 0 2400 3700" style="left:-660px;top:-1500px" data-layout-allow-overflow><g class="world"></g></svg>'
                     if sh.get("tilt") else f'<svg id="{sid}-map" class="map" width="1080" height="1920" viewBox="0 0 1080 1920" data-layout-allow-overflow><g class="world"></g></svg>'))
        for i, l in enumerate(sh.get("labels", [])): body.append(la_html(l, i, sid, True))
        for i, p in enumerate(sh.get("pins", [])):
            body.append(f'<div id="{sid}-pin{i}" class="pin {"l" if p.get("left") else ""} {sid}-lab" data-at="{p["at"]}"><div class="pw">{PIN_SVG}<span class="pl">{esc(p["text"])}</span></div></div>')
        for i, g in enumerate(sh.get("ground", [])):
            body.append(f'<div id="{sid}-gt{i}" class="ground {sid}-lab" data-at="{g["at"]}"><span{f' style="font-size:{g["size"]}px"' if g.get("size") else ""}>{esc(g["text"])}</span></div>')
        body.append("</div>")
        if sh.get("tilt"): body.append('<div style="position:absolute;left:0;right:0;top:0;height:640px;background:linear-gradient(180deg, rgba(14,26,43,.85), rgba(14,26,43,0))"></div>')
        if sh.get("clouds"):
            import random; rnd = random.Random(7)
            for i in range(9):
                x, y, w = rnd.randint(-300, 900), rnd.randint(-200, 1700), rnd.randint(700, 1300)
                body.append(f'<div class="cloud {sid}-cl" style="left:{x}px;top:{y}px;width:{w}px;height:{int(w*.55)}px;opacity:0"></div>')
        body.append("</div>")
        opts = {"svg": f"#{sid}-map", "labels": f".{sid}-lab", "sat": SAT, "pad": [660, 1500] if sh.get("tilt") else [0, 0], "keys": [[k[0] + off] + k[1:] for k in sh["keys"]],
                "layers": sh.get("layers", []), "links": sh.get("links", []),
                "movers": [dict(m, t=T(m["t"])) for m in sh.get("movers", [])], "rings": [dict(r, t=T(r["t"])) for r in sh.get("rings", [])]}
        tilt = sh.get("tilt"); orb = sh.get("orbit")
        pre = (f"const GEO = {GEOJS};\nObject.assign(GEO.lab, {json.dumps(PTS)});\n{VMAP}\n"
               f"const map = makeMap2({json.dumps(opts, ensure_ascii=False)});\nconst pl = document.querySelector('#{sid}-pl');\n"
               f"const lerp = (a, b, t0, t1, t) => a + (b - a) * Math.min(1, Math.max(0, (t - t0) / (t1 - t0))) ;\n"
               f"const ease = (a, b, t0, t1, t) => {{ const p = Math.min(1, Math.max(0, (t - t0) / (t1 - t0))); const e = p < .5 ? 2*p*p : 1 - (-2*p+2)**2/2; return a + (b - a) * e; }};\n"
               f"const frame = (t) => {{ map.apply(t); let tr = '';\n"
               + (f"  const tx = ease({tilt[2]}, {tilt[3]}, {T(tilt[0])}, {T(tilt[1])}, t); tr += `perspective(1500px) rotateX(${{tx}}deg) scale(${{1 + tx/90}}) `;\n" if tilt else "")
               + (f"  tr += `rotateZ(${{ease({orb[2]}, {orb[3]}, {T(orb[0])}, {T(orb[1])}, t)}}deg) `;\n" if orb else "")
               + "  pl.style.transform = tr;\n"
               + ("  pl.style.filter = `blur(${Math.min(9, map.speedZ(t) * 2.2).toFixed(2)}px)`;\n" if sh.get("zoomBlur") else "")
               + "};\n"
               f"const clock = {{ t: 0 }}; tl.fromTo(clock, {{ t: 0 }}, {{ t: {D}, duration: {D}, ease: 'none', onUpdate: () => frame(clock.t) }}, 0); frame(0);")
        for i, l in enumerate(sh.get("labels", [])):
            tl.append(f'tl.fromTo("#{sid}-la{i} > *", {{opacity:0}}, {{opacity:1, duration:.3}}, {T(l["t"])}); tl.to("#{sid}-la{i} > *", {{opacity:0, duration:.2}}, {min(T(l["t"] + l["d"]), endtxt)});')
        for i, p in enumerate(sh.get("pins", [])):
            tl.append(f'tl.fromTo("#{sid}-pin{i} .pw", {{y:-90, opacity:0}}, {{y:0, opacity:1, duration:.45, ease:"bounce.out"}}, {T(p["t"])}); tl.to("#{sid}-pin{i} .pw", {{opacity:0, duration:.2}}, {endtxt});')
        for i, g in enumerate(sh.get("ground", [])):
            tl.append(f'tl.fromTo("#{sid}-gt{i} span", {{opacity:0, scale:.7, y:60}}, {{opacity:1, scale:1, y:0, duration:.7, ease:"expo.out"}}, {T(g["t"])}); '
                      f'tl.to("#{sid}-gt{i} span", {{opacity:0, duration:.25}}, {min(T(g["t"] + g["d"]), endtxt)});')
        for s in sh.get("show", []): tl.append(f'tl.fromTo("#{s["id"]}", {{opacity:0}}, {{opacity:{s.get("to",1)}, duration:{s.get("d",.5)}}}, {T(s["t"])});')
        for s in sh.get("hide", []): tl.append(f'tl.to("#{s["id"]}", {{opacity:0, duration:{s.get("d",.4)}}}, {T(s["t"])});')
        for s in sh.get("draw", []):
            tl.append(f'tl.fromTo(["#{s["id"]}-core", "#{s["id"]}-glow"], {{strokeDashoffset:110}}, {{strokeDashoffset:0, duration:{s["d"]}, ease:"power1.inOut"}}, {T(s["t"])});')
        if sh.get("clouds"):
            c0, c1 = sh["clouds"]
            tl.append(f'tl.fromTo(".{sid}-cl", {{opacity:0, scale:.5}}, {{opacity:1, scale:1.4, duration:{(c1-c0)*.45}, stagger:.05, ease:"power1.in"}}, {T(c0)}); '
                      f'tl.to(".{sid}-cl", {{opacity:0, scale:3.2, duration:{(c1-c0)*.55}, stagger:.04, ease:"power2.in"}}, {T(c0 + (c1-c0)*.45)});')
    elif sh.get("media"):
        m = sh["media"]
        if m.endswith(".mp4"):
            media = (f'<div id="{sid}-mv" style="position:absolute;inset:0"><video id="{sid}-v" class="clip" src="{m}" muted playsinline data-start="0" data-duration="{D}" '
                     f'data-media-start="{sh.get("media_start",0)}" data-track-index="1" style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover"></video></div>')
        else:
            media = f'<div id="{sid}-mv" style="position:absolute;inset:0"><img src="{m}" alt="" style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;object-position:{sh.get("focus","50% 50%")}" /></div>'
        dim = f'<div style="position:absolute;inset:0;background:rgba(10,18,32,{sh.get("dim",0)})"></div>' if sh.get("dim") else ""
        body.append(f'<div id="{sid}-z" class="zw">{media}{dim}<div class="gtop"></div><div class="gbot"></div></div>')
        mv = sh.get("move", "push" if not m.endswith(".mp4") else "none")
        MOVES = {"push": ("{scale:1.0}", "{scale:1.14}"), "pull": ("{scale:1.16}", "{scale:1.0}"),
                 "panL": ("{scale:1.22, x:90}", "{scale:1.22, x:-90}"), "panR": ("{scale:1.22, x:-90}", "{scale:1.22, x:90}"),
                 "panU": ("{scale:1.2, y:110}", "{scale:1.2, y:-110}"), "panD": ("{scale:1.2, y:-110}", "{scale:1.2, y:110}")}
        if mv in MOVES:
            a, b = MOVES[mv]
            tl.append(f'tl.fromTo("#{sid}-mv", {a}, Object.assign({b}, {{duration:{D}, ease:"none"}}), 0);')
    elif sh.get("montage"):
        # dựng nhanh chuỗi ảnh (0,5–1 s/ảnh) + chữ động cho từng ảnh — dùng cho liệt kê
        ms = sh["montage"]; parts = []
        for i, it in enumerate(ms):
            t1 = ms[i + 1]["t"] if i + 1 < len(ms) else dur
            parts.append(f'<div id="{sid}-m{i}" style="position:absolute;inset:0;opacity:0"><img src="{it["media"]}" alt="" style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;object-position:{it.get("focus","50% 50%")}" /></div>')
            tl.append(f'tl.set("#{sid}-m{i}", {{opacity:1}}, {T(it["t"])}); tl.fromTo("#{sid}-m{i}", {{scale:1.18}}, {{scale:1.0, duration:{t1 - it["t"]:.3f}, ease:"none"}}, {T(it["t"])});')
            if i + 1 < len(ms): tl.append(f'tl.set("#{sid}-m{i}", {{opacity:0}}, {T(t1)});')
            sh.setdefault("kw", []).append({"t": it["t"], "d": t1 - it["t"], "lines": ["*" + w if j == 0 else w for j, w in enumerate([it["word"]])], "pos": "mid", "_quick": True})
        body.append(f'<div id="{sid}-z" class="zw">{"".join(parts)}<div class="gtop"></div><div class="gbot"></div></div>')
    else:
        body.append(f'<div id="{sid}-z" class="zw" style="background:radial-gradient(ellipse at 50% 42%, #18304f, #0E1A2B)"></div>')
    if sh.get("clouds") and kind != MAP:
        import random; rnd = random.Random(11)
        for i in range(10):
            x, y, w = rnd.randint(-400, 900), rnd.randint(-200, 1700), rnd.randint(800, 1400)
            body.append(f'<div class="cloud {sid}-cl" style="left:{x}px;top:{y}px;width:{w}px;height:{int(w*.55)}px"></div>')
        c0, c1 = sh["clouds"]
        tl.append(f'tl.fromTo(".{sid}-cl", {{opacity:1, scale:1}}, {{opacity:0, scale:3.4, duration:{c1-c0}, stagger:.03, ease:"power2.in"}}, {T(c0)});')
    # ---------- lớp chữ / dữ liệu
    for i, l in enumerate(sh.get("callouts", [])):
        body.append(la_html(l, i, sid, False))
        tl.append(f'tl.fromTo("#{sid}-la{i} > *", {{opacity:0}}, {{opacity:1, duration:.3}}, {T(l["t"])}); tl.to("#{sid}-la{i} > *", {{opacity:0, duration:.2}}, {min(T(l["t"] + l.get("d", 99)), endtxt)});')
    for i, k in enumerate(sh.get("kw", [])):
        top = {"low": "top:1180px", "mid": "top:760px", "high": "top:440px"}[k.get("pos", "low")]
        acc = f'--accent:{k["accent"]};' if k.get("accent") else ""
        body.append(f'<h2 id="{sid}-kw{i}" class="kw clip" style="{top};{acc}" data-start="{T(k["t"])}" data-duration="{round(min(k["d"], D - T(k["t"])),3)}" data-track-index="20">{words(k["lines"])}</h2>')
        tl.append(f'tl.fromTo("#{sid}-kw{i} .w", {{opacity:0, scale:1.35, filter:"blur(14px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:.28, ease:"expo.out", stagger:.06}}, {T(k["t"]) + .02});')
        if k.get("_quick"): tl.append(f'tl.set("#{sid}-kw{i} .w", {{opacity:0}}, {min(T(k["t"] + k["d"]), endtxt + .3)});')
        else: tl.append(f'tl.to("#{sid}-kw{i} .w", {{opacity:0, filter:"blur(10px)", duration:.16}}, {min(T(k["t"] + k["d"]) - .18, endtxt)});')
    if sh.get("big"):
        b = sh["big"]; dec = b.get("dec", 0); st = round(b.get("num", 1) * 0.4, dec)
        if b.get("num") is not None and st <= 0: raise SystemExit(f"{sid}: số quá nhỏ để đếm — dùng 'text'")
        top = {"mid": "top:760px", "low": "top:1080px", "high": "top:470px"}[b.get("pos", "mid")]
        acc = f'style="color:{b["accent"]}"' if b.get("accent") else ""
        body.append(f'<div id="{sid}-big" class="bign" style="{top}"><span class="n" id="{sid}-bn" {acc}>{st}</span><span class="u">{esc(b.get("unit",""))}</span>'
                    f'<span class="lb">{esc(b.get("label",""))}</span></div>')
        if b.get("text"):
            body[-1] = body[-1].replace(f'>{st}</span>', f'>{esc(b["text"])}</span>', 1)
            tl.append(f'tl.fromTo("#{sid}-big", {{opacity:0, scale:.7, filter:"blur(14px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:.35, ease:"expo.out"}}, {T(b["t"])}); tl.to("#{sid}-big", {{opacity:0, duration:.2}}, {min(T(b["t"] + b["d"]), endtxt)});')
        else: tl.append(f'(() => {{ const el = document.querySelector("#{sid}-bn"), o = {{v:{st}}}; el.textContent = fmt({st}, {dec}); '
                  f'tl.fromTo("#{sid}-big", {{opacity:0, scale:.8, filter:"blur(12px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:.3, ease:"expo.out"}}, {T(b["t"])}); '
                  f'tl.fromTo(o, {{v:{st}}}, {{v:{b["num"]}, duration:.8, ease:"power2.out", onUpdate: () => {{ el.textContent = fmt(o.v, {dec}); }}}}, {T(b["t"])}); '
                  f'tl.to("#{sid}-big", {{opacity:0, duration:.2}}, {min(T(b["t"] + b["d"]), endtxt)}); }})();')
    if sh.get("bar"):
        b = sh["bar"]
        body.append(f'<div id="{sid}-bar" class="bar" style="top:{b.get("top",900)}px"><div class="bl">{esc(b["label"])}</div><div class="bt"><div class="bf" id="{sid}-bf"></div></div>'
                    f'<div class="bv"><span id="{sid}-bvn">{vn(b["value"])}</span><small>{esc(b.get("unit",""))}</small></div><div class="bs">{esc(b.get("sub",""))}</div></div>')
        tl.append(f'tl.fromTo("#{sid}-bar", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:.3}}, {T(b["t"])}); '
                  f'tl.fromTo("#{sid}-bf", {{scaleX:0}}, {{scaleX:{b["value"]/b["max"]:.3f}, duration:1.1, ease:"power2.out"}}, {T(b["t"]) + .1}); '
                  f'tl.to("#{sid}-bar", {{opacity:0, duration:.2}}, {min(T(b["t"] + b["d"]), endtxt)});')
    if sh.get("timeline"):
        tlx = sh["timeline"]; evs = []
        for i, e in enumerate(tlx["events"]):
            evs.append(f'<div class="ev {"lo" if i % 2 else ""}" id="{sid}-ev{i}" style="left:{e["x"]}px"><i></i><span class="d">{esc(e["date"])}</span><span class="t">{esc(e["text"])}</span></div>')
            tl.append(f'tl.fromTo("#{sid}-ev{i} > *", {{opacity:0, scale:.6}}, {{opacity:1, scale:1, duration:.35, ease:"back.out(2)", stagger:.06}}, {T(e["t"])});')
        body.append(f'<div class="tline" id="{sid}-tl" style="top:{tlx.get("y",900)}px"><div class="ax" id="{sid}-ax"></div>{"".join(evs)}</div>')
        tl.append(f'tl.fromTo("#{sid}-ax", {{scaleX:0}}, {{scaleX:1, duration:.7, ease:"power2.out"}}, {T(tlx["t"])}); tl.to("#{sid}-tl", {{opacity:0, duration:.2}}, {endtxt});')
    if sh.get("wall"):
        w = sh["wall"]; tiles = []
        for i, ti in enumerate(w["tiles"]):
            tiles.append(f'<div class="tile {"hl" if ti.get("hl") else ""}" id="{sid}-ti{i}"><b>{esc(ti["name"])}</b><small>{esc(ti.get("sub",""))}</small></div>')
            fx, fy = [(-900, -300), (900, -200), (-900, 200), (900, 300), (0, 900), (0, -900), (-900, 600), (900, 600)][i % 8]
            tl.append(f'tl.fromTo("#{sid}-ti{i}", {{x:{fx}, y:{fy}, rotation:{(-1)**i*12}, opacity:0}}, {{x:0, y:0, rotation:0, opacity:1, duration:.5, ease:"back.out(1.4)"}}, {T(ti["t"])});')
        body.append(f'<div class="wall" style="top:{w.get("top",420)}px">{"".join(tiles)}</div>')
        tl.append(f'tl.to("#{sid} .tile", {{opacity:0, duration:.2}}, {endtxt});')
    if sh.get("stack"):
        s = sh["stack"]; rows = []
        for i, r in enumerate(s["rows"]):
            dec = r.get("dec", 0); st = round(r["num"] * 0.4, dec)
            rows.append(f'<div class="row" id="{sid}-sr{i}"><b id="{sid}-sn{i}">{st}</b><span>{esc(r.get("unit",""))} · {esc(r["label"])}</span></div>')
            tl.append(f'(() => {{ const el = document.querySelector("#{sid}-sn{i}"), o = {{v:{st}}}; el.textContent = fmt({st}, {dec}); '
                      f'tl.fromTo("#{sid}-sr{i}", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:.3}}, {T(r["t"])}); '
                      f'tl.fromTo(o, {{v:{st}}}, {{v:{r["num"]}, duration:.8, ease:"power2.out", onUpdate: () => {{ el.textContent = fmt(o.v, {dec}); }}}}, {T(r["t"])}); }})();')
        body.append(f'<div class="stack" style="top:{s.get("top",420)}px">{"".join(rows)}</div>')
        tl.append(f'tl.to("#{sid} .stack", {{opacity:0, duration:.2}}, {endtxt});')
    if sh.get("doc"):
        dc = sh["doc"]; k = 860 / dc["imgW"]
        hls = "".join(f'<div id="{sid}-hl{i}" style="position:absolute;left:12px;right:12px;top:{h["y"]*k:.0f}px;height:{h["h"]*k:.0f}px;background:rgba(242,140,40,.30);border-radius:4px;transform-origin:0 50%"></div>' for i, h in enumerate(dc.get("hl", [])))
        body.append(f'<div style="position:absolute;left:70px;width:860px;top:{dc.get("top",420)}px;height:{dc.get("h",1000)}px;background:#FBFAF7;border-radius:14px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.55)" data-layout-allow-overflow>'
                    f'<div id="{sid}-pg" style="position:absolute;left:0;top:0;width:860px;transform-origin:50% {dc.get("origin",40)}%" data-layout-allow-overflow data-layout-allow-overlap><img src="{dc["img"]}" alt="" style="display:block;width:860px" />{hls}</div></div>')
        for i, h in enumerate(dc.get("hl", [])):
            tl.append(f'tl.fromTo("#{sid}-hl{i}", {{scaleX:0, opacity:0}}, {{scaleX:1, opacity:1, duration:.4, ease:"power2.out"}}, {T(h["t"])});')
        z = dc.get("zoom")
        if z: tl.append(f'tl.fromTo("#{sid}-pg", {{y:0, scale:1}}, {{y:{z["y"]}, scale:{z["scale"]}, duration:{z["d"]}, ease:"power2.inOut"}}, {T(z["t"])});')
    if sh.get("seg"):
        body.append(f'<div class="seg clip" id="{sid}-seg" data-start="{T(0.1)}" data-duration="{round(D - T(0.1),3)}" data-track-index="10" data-layout-allow-occlusion><span id="{sid}-sgt">{esc(sh["seg"])}</span></div>')
        tl.append(f'tl.fromTo("#{sid}-sgt", {{opacity:0}}, {{opacity:1, duration:.25}}, {T(0.1)}); tl.to("#{sid}-sgt", {{opacity:0, duration:.2}}, {endtxt});')
    if sh.get("foot"):
        body.append(f'<p class="foot clip" id="{sid}-ft" data-start="{T(0.1)}" data-duration="{round(D - T(0.1),3)}" data-track-index="11" data-layout-ignore><span id="{sid}-ftt">{esc(sh["foot"])}</span></p>')
        tl.append(f'tl.fromTo("#{sid}-ftt", {{opacity:0}}, {{opacity:1, duration:.25}}, {T(0.1)}); tl.to("#{sid}-ftt", {{opacity:0, duration:.2}}, {endtxt});')
    # ---------- vào shot
    e = sh.get("enter", "T5")
    if e == "T3":
        dirx = 1080 if sh.get("whipDir", "L") == "L" else -1080
        tl.insert(0, f'tl.fromTo("#{sid}-z", {{x:{dirx}, filter:"blur(22px)"}}, {{x:0, filter:"blur(0px)", duration:.26, ease:"power3.out"}}, 0);')
    elif e == "T1":
        tl.insert(0, f'tl.fromTo("#root", {{opacity:0}}, {{opacity:1, duration:{OVER}, ease:"none"}}, 0); tl.fromTo("#{sid}-z", {{scale:1.3, filter:"blur(10px)"}}, {{scale:1, filter:"blur(0px)", duration:.5, ease:"power3.out"}}, 0);')
    elif e == "DIS":
        tl.insert(0, f'tl.fromTo("#root", {{opacity:0}}, {{opacity:1, duration:{OVER + .1}, ease:"none"}}, 0);')
    elif e == "T2":
        body.append(f'<div id="{sid}-plane" style="position:absolute;left:0;top:0">{PLANE_SVG}</div>')
        tl.insert(0, f'tl.fromTo("#{sid}-z", {{scale:1.4, filter:"blur(12px)"}}, {{scale:1, filter:"blur(0px)", duration:.35, ease:"power3.out"}}, .15); '
                     f'tl.fromTo("#{sid}-plane", {{x:-260, y:1500, rotation:45, scale:.8, filter:"blur(2px)"}}, {{x:1150, y:-200, scale:1.8, filter:"blur(6px)", duration:.75, ease:"power1.in"}}, 0);')
    elif e == "T4":
        poly, big = sh["_mask"]
        tl.insert(0, f'tl.fromTo("#{sid}-z", {{clipPath:"polygon({poly})"}}, {{clipPath:"polygon({big})", duration:.95, ease:"power2.inOut"}}, 0);')
        css.append(f"#{sid}-z {{ clip-path: polygon({poly}); }}")
    return f"""<template>
  <style>
{chr(10).join(css)}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
{chr(10).join(body)}
  </div>
  <script>
    (() => {{
      const tl = gsap.timeline({{ paused: true }});
      const fmt = (v, dec) => {{ const [i, d] = v.toFixed(dec).split("."); return i.replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ".") + (d ? "," + d : ""); }};
      {pre}
{chr(10).join("      " + l for l in tl)}
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
""", off

def mask_for(prev, site):
    """Đa giác ranh dự án trên màn hình ở khung cuối của shot bản đồ trước -> và đa giác 'phóng' phủ kín khung."""
    k = prev["keys"][-1]; cx, cy, s = wx(k[2]), wy(k[1]), 2 ** (k[3] - 8)
    pts = [((wx(lng) - cx) * s + 540, (wy(lat) - cy) * s + 960) for lng, lat in site]
    mx_ = sum(p[0] for p in pts) / len(pts); my_ = sum(p[1] for p in pts) / len(pts)
    big = [(mx_ + (x - mx_) * 9, my_ + (y - my_) * 9) for x, y in pts]
    f = lambda ps: ", ".join(f"{x:.0f}px {y:.0f}px" for x, y in ps)
    return f(pts), f(big)

def validate(shots, total):
    msg = []; dur = {MAP: 0, FOOTAGE: 0, DATA: 0}; fxdur = {}
    for i, s in enumerate(shots):
        dur[s["kind"]] += s["dur"]
        fxs = list(dict.fromkeys(s["fx"] + [s.get("enter", "T5").replace("DIS", "T5")]))
        for f in fxs:
            fxdur[f] = fxdur.get(f, 0) + (sum(min(k["d"], s["dur"] - k["t"]) for k in s.get("kw", [])) if f == "F3" else s["dur"])
        if s["dur"] > 6 and not s.get("busy"): msg.append(f"{s['id']}: dài {s['dur']:.1f}s > 6s (đánh dấu busy nếu có yếu tố mới mỗi ≤1,5s)")
        if i:
            pf = shots[i - 1]["fx"] + [shots[i - 1].get("enter", "T5")]
            same = set(fxs) & set(pf) - {"T5", "F1", "F2", "C1", "DOC"}
            if same: msg.append(f"{s['id']}: lặp hiệu ứng {sorted(same)} với shot trước")
    run = 1
    for a, b in zip(shots, shots[1:]):
        run = run + 1 if a["kind"] == b["kind"] else 1
        lim = 2 if b["kind"] == MAP else 3 if b["kind"] == FOOTAGE else 2
        if run > lim: msg.append(f"{b['id']}: {run} shot '{b['kind']}' liên tiếp (tối đa {lim})")
    for f, d in fxdur.items():
        if f[0] in "MFD" and f not in ("F1", "F2") and d > 0.15 * total: msg.append(f"{f}: {d:.0f}s > 15% thời lượng")
    unused = sorted(set([f"M{i}" for i in range(1, 11)] + [f"T{i}" for i in range(1, 6)] + ["F1", "F2", "F3"] + [f"D{i}" for i in range(1, 7)]) - set(fxdur))
    if unused: msg.append(f"chưa dùng: {unused}")
    dis = sum(1 for s in shots if s.get("enter") == "DIS")
    if dis > 3: msg.append(f"cross-dissolve {dis} lần > 3")
    if sum(1 for s in shots if "D4" in s["fx"]) > 2: msg.append("D4 dùng quá 2 lần")
    share = {k: v / total for k, v in dur.items()}
    avg = total / len(shots)
    return msg, share, avg

def main():
    global SAT, GEOJS, VMAP, PTS
    sb = json.load(open(sys.argv[1], encoding="utf-8")); P = sys.argv[2]
    SAT = sb.get("sat", []); GEOJS = open(f"{P}/geo.json").read(); VMAP = open(f"{P}/vmap2.js").read()
    PTS = {k: [round(wx(v[0]), 2), round(wy(v[1]), 2)] for k, v in sb.get("points", {}).items()}
    os.makedirs(f"{P}/compositions", exist_ok=True)
    shots = sb["shots"]; hosts = []; rows = []
    for i, sh in enumerate(shots):
        if sh.get("enter") == "T4":
            sh["_mask"] = mask_for(shots[i - 1], sb["site"])
        h, off = shot_html(sh, P, shots[i - 1] if i else None)
        open(f"{P}/compositions/{sh['id']}.html", "w", encoding="utf-8").write(h)
        st = round(sh["start"] - off, 3)
        hosts.append(f'      <div id="{sh["id"]}" data-composition-id="{sh["id"]}" data-composition-src="compositions/{sh["id"]}.html" data-start="{st}" data-duration="{round(sh["dur"] + off,3)}" '
                     f'data-track-index="{1 + i % 2}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{i + 1}"></div>')
        tc = lambda t: f"{int(t // 60)}:{t % 60:05.2f}"
        rows.append(f"| {sh['id']} | {tc(sh['start'])} | {sh['dur']:.2f} | {sh['kind']} | {' '.join(sh['fx'])} | {sh.get('enter','T5')} | {esc(sh.get('src',''))} |")
    open(f"{P}/index.html", "w", encoding="utf-8").write(f"""<!doctype html>
<html lang="vi">
  <head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
    <script src="{sb.get('gsap','https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js')}"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0E1A2B; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{sb['duration']}" data-width="1080" data-height="1920">
{chr(10).join(hosts)}
      <audio id="mix" class="clip" src="{sb.get('audio','assets/mix.wav')}" data-start="0" data-duration="{sb['duration']}" data-track-index="30" data-volume="1"></audio>
    </div>
    <script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
""")
    msg, share, avg = validate(shots, sb["duration"])
    rep = [f"# Shot list ({len(shots)} shot, trung bình {avg:.2f} s)", "",
           f"Tỉ lệ: bản đồ {share[MAP]*100:.0f}% · footage/render {share[FOOTAGE]*100:.0f}% · thẻ dữ liệu/tài liệu {share[DATA]*100:.0f}%", "",
           "| Shot | Timecode | Dài (s) | Loại | Hiệu ứng | Vào | Nguồn hình |", "|---|---|---|---|---|---|---|"] + rows
    rep += ["", "## Kiểm tra luật", ""] + ([f"- {m}" for m in msg] or ["- Đạt tất cả luật nhịp/lặp/tỉ lệ."])
    open(f"{P}/SHOTLIST.md", "w", encoding="utf-8").write("\n".join(rep))
    print(f"{len(shots)} shot · TB {avg:.2f}s · map {share[MAP]*100:.0f}% footage {share[FOOTAGE]*100:.0f}% data {share[DATA]*100:.0f}%")
    for m in msg: print("  !", m)

if __name__ == "__main__":
    main()
```

## FILE: scripts/qa_frames.py

```python
#!/usr/bin/env python3
"""Kiểm lỗi render của video trước khi xuất (mục "kiểm soát lỗi render").

  python qa_frames.py video.mp4 [--out qa] [--fps 2]

Kiểm:
  1. DEAD_EDGE  — vùng chết dính mép/góc (đen, hoặc một màu phẳng như ảnh vệ tinh/3D chưa tải) > 5% diện tích khung.
  2. HAZE       — mảng trắng mờ (mây, sương, tile lỗi) phẳng, ít chi tiết > 8% diện tích.
  3. DARK_RUN   — > 5 khung liên tiếp tối (luma trung bình < 22) ngoài chủ đích.
  4. BLUR_RUN   — > 6 khung liên tiếp nhoè (độ nét < 18% trung vị của cả video): chuyển cảnh dài quá hoặc nguồn mờ.
  5. STATIC     — một khung hình gần như đứng yên > 6 s (vi phạm nhịp).
Kết quả: <out>/QA.md + ảnh khung lỗi. Thoát mã 1 nếu có lỗi -> render lại đoạn đó.
"""
import argparse, os, sys
import cv2, numpy as np

def dead_mask(gray, hsv, block=16):
    h, w = gray.shape
    hb, wb = h // block, w // block
    g = gray[: hb * block, : wb * block].reshape(hb, block, wb, block).astype(np.float32)
    std = g.std(axis=(1, 3)); mean = g.mean(axis=(1, 3))
    sat = hsv[: hb * block, : wb * block, 1].reshape(hb, block, wb, block).astype(np.float32).mean(axis=(1, 3))
    # vùng chết = gần đen, hoặc phẳng tuyệt đối VÀ (tối hoặc mất màu): tile chưa tải, lưới 3D thủng, nền đặc.
    # Mặt nước/bầu trời thật có màu (bão hoà > 14) nên không bị tính.
    flat = (std < 1.2) & ((mean < 70) | ((sat < 14) & (mean < 150)))   # trời sáng phẳng là bình thường
    black = mean < 12
    return flat | black, mean, std

def edge_connected(mask):
    m = mask.astype(np.uint8)
    n, lab = cv2.connectedComponents(m, connectivity=4)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    border.discard(0)
    return np.isin(lab, list(border)) if border else np.zeros_like(mask)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--out", default="qa"); ap.add_argument("--fps", type=float, default=2.0)
    ap.add_argument("--dead", type=float, default=0.05); ap.add_argument("--haze", type=float, default=0.08)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    cap = cv2.VideoCapture(a.video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    step = max(1, int(round(fps / a.fps)))
    issues = []
    lum, sharp, times, prev, still_since = [], [], [], None, 0.0
    i = 0
    while True:
        ok, fr = cap.read()
        if not ok: break
        t = i / fps
        small = cv2.resize(fr, (270, 480), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        lum.append(float(gray.mean())); times.append(t)
        sharp.append(float(cv2.Laplacian(gray, cv2.CV_64F).var()))
        if prev is not None:
            if float(np.mean(cv2.absdiff(gray, prev))) < 0.6:
                if t - still_since > 6.0:
                    issues.append(("STATIC", t, f"đứng yên từ {still_since:.1f}s")); still_since = t
            else:
                still_since = t
        else:
            still_since = t
        prev = gray
        if i % step == 0:
            hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
            m, mean, std = dead_mask(gray, hsv, block=8)
            frac = edge_connected(m).mean()
            if frac > a.dead:
                issues.append(("DEAD_EDGE", t, f"{frac*100:.1f}% khung là vùng chết dính mép"))
                cv2.imwrite(f"{a.out}/dead_{t:07.2f}.jpg", small)
            s = hsv[..., 1].astype(np.float32); v = hsv[..., 2].astype(np.float32)
            hz = ((v > 185) & (s < 40)).astype(np.uint8)
            hz = cv2.erode(hz, np.ones((5, 5), np.uint8))  # bỏ chữ trắng mảnh, chỉ giữ mảng lớn
            lap = np.abs(cv2.Laplacian(gray, cv2.CV_32F))
            hz = hz & (cv2.blur(lap, (9, 9)) < 6)
            if hz.mean() > a.haze:
                issues.append(("HAZE", t, f"{hz.mean()*100:.1f}% khung là mảng trắng mờ"))
                cv2.imwrite(f"{a.out}/haze_{t:07.2f}.jpg", small)
        i += 1
    lum = np.array(lum); sharp = np.array(sharp)
    med = np.median(sharp)
    def runs(flag, minlen, kind, note):
        k = 0
        for j, f in enumerate(flag):
            k = k + 1 if f else 0
            if k == minlen + 1:
                issues.append((kind, times[j - minlen], note))
    runs(lum < 22, 5, "DARK_RUN", "> 5 khung tối liên tiếp")
    runs(sharp < 0.18 * med, 6, "BLUR_RUN", "> 6 khung nhoè liên tiếp")
    issues.sort(key=lambda x: x[1])
    with open(f"{a.out}/QA.md", "w", encoding="utf-8") as f:
        f.write(f"# QA {os.path.basename(a.video)}\n\n{len(issues)} lỗi.\n\n| Loại | Thời điểm (s) | Chi tiết |\n|---|---|---|\n")
        for k, t, d in issues:
            f.write(f"| {k} | {t:.2f} | {d} |\n")
    for k, t, d in issues:
        print(f"{k:10s} {t:7.2f}s  {d}")
    print(f"{len(issues)} lỗi -> {a.out}/QA.md")
    sys.exit(1 if issues else 0)

if __name__ == "__main__":
    main()
```

## FILE: scripts/sat_declouds.py

```python
#!/usr/bin/env python3
"""Xoá mây khỏi ảnh vệ tinh ghép (sat_tiles.py) rồi chỉnh màu nền "tối, giảm bão hoà" cho bản đồ.

  python sat_declouds.py sat16.jpg [--min-area 900] [--grow 25] [--no-decloud]
  -> sat16_g.jpg (đã xoá mây + chỉnh màu) và sat16_dc.jpg (chỉ xoá mây)

Mây = mảng sáng (V>175), ít màu (S<45), diện tích ≥ min-area px (bỏ qua mái tôn nhỏ); mở rộng `grow` px để
ăn cả viền. Mỗi đám mây được lấp bằng một mảng kết cấu đô thị lấy ở gần đó không có mây (nhân bản có viền mờ) —
KHÔNG dùng inpaint Telea (để lại vệt xám hình sao). Gợi ý: z16 --min-area 900 --grow 25; z13 60/9; z11 30/5.
Luật QA: không được có mây hay ô chưa có ảnh đè lên khu vực đang nói tới.
"""
import argparse
import cv2, numpy as np
from PIL import Image, ImageEnhance

ap = argparse.ArgumentParser()
ap.add_argument("img"); ap.add_argument("--min-area", type=int, default=900); ap.add_argument("--grow", type=int, default=25)
ap.add_argument("--no-decloud", action="store_true")
a = ap.parse_args()
base = a.img.rsplit(".", 1)[0]
im = cv2.imread(a.img)
if not a.no_decloud:
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    v, s = hsv[..., 2].astype(int), hsv[..., 1].astype(int)
    m = cv2.morphologyEx(((v > 175) & (s < 45)).astype(np.uint8) * 255, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    k = cv2.connectedComponentsWithStats(m); keep = np.zeros_like(m)
    for i in range(1, k[0]):
        if k[2][i, 4] >= a.min_area: keep[k[1] == i] = 255
    keep = cv2.dilate(keep, np.ones((a.grow, a.grow), np.uint8))
    print(f"{a.img}: mây {keep.mean() / 2.55:.2f}% diện tích")
    out = im.copy().astype(np.float32); H, W = keep.shape
    cc = cv2.connectedComponentsWithStats(keep)
    for i in range(1, cc[0]):
        x, y, w, h, _ = cc[2][i]; comp = (cc[1] == i).astype(np.uint8)
        pad = 12; x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + w + pad), min(H, y + h + pad)
        cm = cv2.dilate(comp[y0:y1, x0:x1], np.ones((5, 5), np.uint8))
        fe = np.clip(cv2.GaussianBlur(cm.astype(np.float32), (0, 0), 4) * 1.6, 0, 1)[..., None]
        best = None
        for r in (1.2, 1.6, 2.2, 3.0):          # tìm mảng nguồn gần nhất không có mây
            for ang in range(0, 360, 30):
                dx, dy = int(np.cos(np.radians(ang)) * r * max(w, h)), int(np.sin(np.radians(ang)) * r * max(w, h))
                sx, sy = x0 + dx, y0 + dy
                if sx < 0 or sy < 0 or sx + (x1 - x0) > W or sy + (y1 - y0) > H: continue
                bad = keep[sy:sy + y1 - y0, sx:sx + x1 - x0].mean()
                if best is None or bad < best[0]: best = (bad, sx, sy)
            if best and best[0] == 0: break
        if not best: continue
        _, sx, sy = best
        out[y0:y1, x0:x1] = out[y0:y1, x0:x1] * (1 - fe) + im[sy:sy + y1 - y0, sx:sx + x1 - x0].astype(np.float32) * fe
    im = out.astype(np.uint8)
    cv2.imwrite(base + "_dc.jpg", im, [cv2.IMWRITE_JPEG_QUALITY, 92])
p = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
p = ImageEnhance.Color(p).enhance(.55); p = ImageEnhance.Brightness(p).enhance(.62); p = ImageEnhance.Contrast(p).enhance(1.12)
Image.blend(p, Image.new("RGB", p.size, (14, 26, 43)), .15).save(base + "_g.jpg", quality=86)
print("->", base + "_g.jpg")
```

## FILE: scripts/sat_tiles.py

```python
#!/usr/bin/env python3
"""Ghép ô ảnh vệ tinh Esri World Imagery cho một khung lat/lng ở mức zoom z.

  python sat_tiles.py sat16 16 <lat_trên> <lng_trái> <lat_dưới> <lng_phải> img   -> sat16.jpg + sat16.json {z,x0,y0,w,h}

Phủ RỘNG hơn mọi khung hình camera sẽ thấy ở mức đó (kể cả khi nghiêng 3D) — thiếu là lộ hình chữ nhật navy.
Sau đó chạy sat_declouds.py để xoá mây + chỉnh màu.
"""
#!/usr/bin/env python3
"""Ghép ô ảnh vệ tinh Esri World Imagery (hoặc lớp tham chiếu) cho một khung lat/lng ở mức zoom z.

  python sat_tiles.py sat16 16 <lat_trên> <lng_trái> <lat_dưới> <lng_phải> img   -> sat16.jpg + sat16.json {z,x0,y0,w,h}

Phủ RỘNG hơn mọi khung hình camera sẽ thấy ở mức đó (kể cả khi nghiêng 3D): thiếu là lộ hình chữ nhật navy.
Rồi chạy sat_declouds.py để xoá mây + chỉnh màu."""
import math, io, sys, json, urllib.request, concurrent.futures as cf
from PIL import Image
def xy(lat,lng,z):
    n=2**z; x=(lng+180)/360*n; y=(1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n; return x,y
SV={'img':'World_Imagery','trn':'Reference/World_Transportation','lbl':'Reference/World_Boundaries_and_Places'}
def fetch(layer,z,x,y):
    u=f"https://server.arcgisonline.com/ArcGIS/rest/services/{SV[layer]}/MapServer/tile/{z}/{y}/{x}"
    for _ in range(4):
        try: return Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"tile-fetch/1.0"}),timeout=30).read())).convert("RGBA")
        except Exception as e: err=e
    raise err
def mosaic(name,z,lat1,lng1,lat2,lng2,layers=('img',)):
    x1,y1=xy(lat1,lng1,z); x2,y2=xy(lat2,lng2,z)
    tx=range(int(min(x1,x2)),int(max(x1,x2))+1); ty=range(int(min(y1,y2)),int(max(y1,y2))+1)
    out=Image.new("RGBA",(256*len(tx),256*len(ty)),(0,0,0,255))
    for L in layers:
        with cf.ThreadPoolExecutor(8) as ex:
            futs={ex.submit(fetch,L,z,x,y):(i,j) for i,x in enumerate(tx) for j,y in enumerate(ty)}
            for f,(i,j) in futs.items(): t=f.result(); out.alpha_composite(t,(256*i,256*j))
    out.convert("RGB").save(name+".jpg",quality=88)
    m={"z":z,"x0":tx[0]*256,"y0":ty[0]*256,"w":out.width,"h":out.height}; print(name,m); return m
if __name__=="__main__":
    a=sys.argv; m=mosaic(a[1],int(a[2]),float(a[3]),float(a[4]),float(a[5]),float(a[6]),tuple(a[7].split(',')))
    json.dump(m,open(a[1]+'.json','w'))
```

## FILE: scripts/scenegen.py

```python
#!/usr/bin/env python3
"""scenegen.py — storyboard JSON -> project HyperFrames (dọc 1080×1920) theo hệ thiết kế của skill.

  python scenegen.py storyboard.json <project_dir>

Project cần có sẵn: fonts.css + assets/fonts (design/install_fonts.sh), design.css, vmap.js, vector_map.css, geo.json (nếu có cảnh map),
assets/mix.wav (mix_audio.py). Sinh ra compositions/<id>.html cho từng cảnh + index.html.

storyboard.json:
{ "duration": 257.44, "audio": "assets/mix.wav",
  "scenes": [ { "id": "s01", "start": 0, "dur": 30.9, "type": "map|media|board|doc",
                "enter": "whip|blend|none", "seg": "Nhãn phân đoạn", "foot": "Nguồn ...",
                "anchors": [ {"t": 0.4, "d": 2.5, "pos": "low|mid", "dim": false, "lines": ["Trái tim", "*châu *thổ"]} ],   # *từ = nhấn cam
                ... theo loại cảnh ... } ] }
 map:   "keys": [[t,lat,lng,Z(,carry)]], "layers": [vmap layer...], "rings": [[t0,dur,rmax,ptKey]],
        "labelsA": [{"at","lx","ly","align","text","small","t","d"}], "tagsB": [{"at","dx","dy","text","t","d"}],
        "show": [{"id","t","d","to"}], "hide": [{"id","t","d"}], "draw": [{"id","t","d"}], "dimMap": 0..1
 media: "src", "kind": "video|image", "fit": "cover|frame", "media_start", "kb": [s0,s1,x0,x1,y0,y1],
        "labelsA": [{"x","y","lx","ly","align","text","small","t","d"}] (toạ độ màn hình), "tagsB": [{"x","y","text","t","d"}]
 board: "rows": [{"icon","num","dec","unit","desc","up","big","t","tup"}], "top": 380, "bg": {map...} | {"img": "..."}
 doc:   "img", "imgW", "imgH", "hl": [{"y","h","t"}], "moves": [{"t","d","y","scale"}]
Quy tắc tự áp: chữ tắt hết trước khung chuyển cảnh; whip zoom luôn phóng to; "blend" = hoà 0,4 s từ cảnh trước (cảnh bắt đầu sớm 0,4 s).
"""
import html, json, os, sys

ICONS = {
 "bld": '<path d="M4 21V5l8-3 8 3v16M9 21v-4h6v4M8 8h.01M12 8h.01M16 8h.01M8 12h.01M12 12h.01M16 12h.01"/>',
 "money": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/>',
 "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.5 12h11l2-8H6.2"/>',
 "ship": '<path d="M3 17l2 4h14l2-4M5 17V11h14v6M9 11V6h6v5M12 3v3"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
 "crane": '<path d="M4 21h8M6 21V4h2M8 4h12l-3 4M8 8h9M14 8v5M13 13h2v2h-2z"/>',
 "area": '<path d="M3 3h18v18H3z"/><path d="M3 9h18M9 3v18" opacity=".5"/>',
 "home": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>',
 "apt": '<rect x="5" y="3" width="14" height="18"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2"/>',
 "leaf": '<path d="M5 19c0-9 6-14 15-14 0 9-5 15-14 15"/><path d="M5 19l8-8"/>',
 "cal": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
 "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
 "people": '<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3 20c0-3.5 2.7-6 6-6s6 2.5 6 6M14 20c0-2.6 1.4-4.5 4-4.5s3.5 1.9 3.5 4.5"/>',
 "school": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/>',
 "health": '<path d="M12 21s-8-5-8-11a4.5 4.5 0 0 1 8-3 4.5 4.5 0 0 1 8 3c0 6-8 11-8 11z"/><path d="M12 9v6M9 12h6"/>',
 "shop": '<path d="M3 9l2-5h14l2 5"/><path d="M4 9v11h16V9"/><path d="M3 9h18"/><path d="M9 20v-6h6v6"/>',
 "office": '<rect x="4" y="2" width="16" height="20"/><path d="M8 6h2M14 6h2M8 10h2M14 10h2M8 14h2M14 14h2M11 22v-4h2v4"/>',
 "handshake": '<path d="M2 12l4-4 5 3 3-2 4 3 4-1"/><path d="M6 8l4 9 3-2 2 2 3-3"/>',
 "flag": '<path d="M5 21V3"/><path d="M5 4h11l-2 4 2 4H5"/>',
}

def esc(s): return html.escape(s, quote=False)

def anchor_html(a, i, sid):
    lines = []
    for ln in a["lines"]:
        ws = []
        for w in ln.split():
            if w.startswith("*"): ws.append(f'<em><span class="w">{esc(w[1:])}</span></em>')
            else: ws.append(f'<span class="w">{esc(w)}</span>')
        lines.append('<span class="ln">' + " ".join(ws) + "</span>")
    return (f'<h2 id="{sid}-a{i}" class="anchor {a.get("pos","low")} clip" data-start="{a["t"]}" data-duration="{a["d"]}" '
            f'data-track-index="20">{"".join(lines)}</h2>')

def label_a(l, i, sid, cls, mapped):
    small = f'<small>{esc(l["small"])}</small>' if l.get("small") else ""
    acc = " acc" if l.get("acc") else ""
    if mapped:
        attrs = f'data-at="{l["at"]}" data-lx="{l.get("lx",0)}" data-ly="{l.get("ly",-80)}" data-align="{l.get("align","")}"'
        inner = '<span class="lead"></span><span class="dot"></span><span class="tx">' + esc(l["text"]) + small + "</span>"
        return f'<div id="{sid}-la{i}" class="la{acc} {cls}" {attrs}>{inner}</div>'
    lx, ly = l.get("lx", 0), l.get("ly", -100)
    import math
    al = l.get("align") or ("l" if lx >= 0 else "r")
    gx = 10 if al == "l" else -10 if al == "r" else 0
    tr = {"l": "translate(0,-50%)", "r": "translate(-100%,-50%)", "c": "translate(-50%,-100%)" if ly < 0 else "translate(-50%,0)"}[al]
    return (f'<div id="{sid}-la{i}" class="la{acc}" style="transform: translate({l["x"]}px, {l["y"]}px)">'
            f'<span class="lead" style="width:{math.hypot(lx, ly):.0f}px; transform: rotate({math.atan2(ly, lx):.4f}rad)"></span><span class="dot"></span>'
            f'<span class="tx" style="left:{lx + gx}px; top:{ly}px; transform:{tr}; text-align:{ {"l":"left","r":"right","c":"center"}[al] }">{esc(l["text"])}{small}</span></div>')

def tag_b(t, i, sid, cls, mapped):
    if mapped:
        return f'<div id="{sid}-tb{i}" class="lb {cls}" data-at="{t["at"]}" data-dx="{t.get("dx",0)}" data-dy="{t.get("dy",-120)}"><span>{esc(t["text"])}</span></div>'
    return f'<div id="{sid}-tb{i}" class="lb" style="transform: translate({t["x"]}px, {t["y"]}px)"><span>{esc(t["text"])}</span></div>'

def fmt_js():
    return 'const fmt = (v, dec) => { const [i, d] = v.toFixed(dec).split("."); return i.replace(/\\B(?=(\\d{3})+(?!\\d))/g, ".") + (d ? "," + d : ""); };'

def scene(sc, nxt, P):
    sid, dur, typ = sc["id"], sc["dur"], sc["type"]
    exit_whip = not (nxt and nxt.get("enter") == "blend") and sc.get("exit", "whip") == "whip"
    css = [open(f"{P}/fonts.css").read(), open(f"{P}/design.css").read()]
    body, js, mapjs = [], [], ""
    tl = []  # JS lines
    # --- nền theo loại
    if typ == "map" or (typ == "board" and sc.get("bg", {}).get("keys")):
        m = sc if typ == "map" else sc["bg"]
        css.append(open(f"{P}/vector_map.css").read())
        dim = m.get("dimMap", 0.35 if typ == "board" else 1)
        body.append(f'<div id="{sid}-z" class="zw"><div class="mapbg"></div><div style="position:absolute;inset:0;opacity:{dim}">'
                    f'<svg id="{sid}-map" class="map" width="1080" height="1920" viewBox="0 0 1080 1920" data-layout-allow-overflow><g class="world"></g></svg></div><div class="mapdots"></div>')
        for i, l in enumerate(m.get("labelsA", [])): body.append(label_a(l, i, sid, f"{sid}-lab", True))
        for i, t in enumerate(m.get("tagsB", [])): body.append(tag_b(t, i, sid, f"{sid}-lab", True))
        body.append("</div>")
        mapjs = ("const GEO = " + open(f"{P}/geo.json").read() + ";\n" + open(f"{P}/vmap.js").read() +
                 f'\nconst map = makeMap({json.dumps({"svg": f"#{sid}-map", "id": sid, "labels": f".{sid}-lab", "keys": m["keys"], "layers": m.get("layers", []), "rings": m.get("rings", [])}, ensure_ascii=False)});\n'
                 f'const clock = {{ t: 0 }}; tl.fromTo(clock, {{ t: 0 }}, {{ t: {dur}, duration: {dur}, ease: "none", onUpdate: () => map.apply(clock.t) }}, 0); map.apply(0);')
        for i, l in enumerate(m.get("labelsA", [])):
            tl.append(f'tl.fromTo("#{sid}-la{i} > *", {{opacity:0}}, {{opacity:1, duration:0.35, ease:"power2.out"}}, {l["t"]});')
            tl.append(f'tl.to("#{sid}-la{i} > *", {{opacity:0, duration:0.25, ease:"power1.in"}}, {min(l["t"] + l["d"], dur - 0.45)});')
        for i, t in enumerate(m.get("tagsB", [])):
            tl.append(f'tl.fromTo("#{sid}-tb{i} > span", {{opacity:0, scale:0.85}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(1.6)"}}, {t["t"]});')
            tl.append(f'tl.to("#{sid}-tb{i} > span", {{opacity:0, duration:0.25, ease:"power1.in"}}, {min(t["t"] + t["d"], dur - 0.45)});')
        for s in m.get("show", []):
            tl.append(f'tl.fromTo("#{s["id"]}", {{opacity:0}}, {{opacity:{s.get("to",1)}, duration:{s.get("d",0.5)}, ease:"power2.out"}}, {s["t"]});')
        for s in m.get("hide", []):
            tl.append(f'tl.to("#{s["id"]}", {{opacity:0, duration:{s.get("d",0.4)}, ease:"power1.in"}}, {s["t"]});')
        for s in m.get("draw", []):
            tl.append(f'tl.fromTo("#{s["id"]}", {{strokeDashoffset:100}}, {{strokeDashoffset:0, duration:{s["d"]}, ease:"power1.inOut"}}, {s["t"]});')
    elif typ == "media" or (typ == "board" and sc.get("bg", {}).get("img")):
        m = sc if typ == "media" else sc["bg"]
        src = m.get("src") or m.get("img")
        kind = m.get("kind", "video" if src.endswith(".mp4") else "image")
        fit = m.get("fit", "cover")
        if kind == "video":
            media = (f'<video id="{sid}-v" class="clip" src="{src}" muted playsinline data-start="0" data-duration="{dur}" '
                     f'data-media-start="{m.get("media_start",0)}" data-track-index="1" style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover"></video>')
        elif fit == "frame":
            media = (f'<img src="{src}" alt="" style="position:absolute;left:-60px;top:-60px;width:1200px;height:2040px;object-fit:cover;filter:blur(28px) brightness(0.45) saturate(0.8)" />'
                     f'<div id="{sid}-kb" style="position:absolute;left:0;top:{m.get("frameTop",500)}px;width:1080px;height:{m.get("frameH",700)}px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.5)">'
                     f'<img src="{src}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover" /></div>')
        else:
            media = f'<div id="{sid}-kb" style="position:absolute;inset:0"><img src="{src}" alt="" style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover" /></div>'
        dimc = f'<div style="position:absolute;inset:0;background:rgba(14,26,43,{m.get("dim",0)})"></div>' if m.get("dim") else ""
        body.append(f'<div id="{sid}-z" class="zw">{media}{dimc}<div class="gtop"></div><div class="gbot"></div></div>')
        if m.get("kb") and kind == "image":
            s0, s1, x0, x1, y0, y1 = m["kb"]
            tl.append(f'tl.fromTo("#{sid}-kb", {{scale:{s0}, x:{x0}, y:{y0}}}, {{scale:{s1}, x:{x1}, y:{y1}, duration:{dur}, ease:"none"}}, 0);')
        if typ == "media":
            for i, l in enumerate(m.get("labelsA", [])):
                body.append(label_a(l, i, sid, "", False))
                tl.append(f'tl.fromTo("#{sid}-la{i} > *", {{opacity:0}}, {{opacity:1, duration:0.35}}, {l["t"]});')
                tl.append(f'tl.to("#{sid}-la{i} > *", {{opacity:0, duration:0.25}}, {min(l["t"] + l["d"], dur - 0.45)});')
            for i, t in enumerate(m.get("tagsB", [])):
                body.append(tag_b(t, i, sid, "", False))
                tl.append(f'tl.fromTo("#{sid}-tb{i} > span", {{opacity:0, scale:0.85}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(1.6)"}}, {t["t"]});')
                tl.append(f'tl.to("#{sid}-tb{i} > span", {{opacity:0, duration:0.25}}, {min(t["t"] + t["d"], dur - 0.45)});')
    elif typ == "doc":
        css.append(f'#{sid}-card{{position:absolute;left:70px;width:860px;top:{sc.get("cardTop",380)}px;height:{sc.get("cardH",1040)}px;background:#FBFAF7;border-radius:14px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.5)}}'
                   f'#{sid}-page{{position:absolute;left:0;top:0;width:860px;transform-origin:50% 0}}'
                   f'#{sid}-page img{{display:block;width:860px}} .hl{{position:absolute;left:14px;right:14px;background:rgba(242,140,40,.30);border-radius:4px;transform-origin:0 50%}}')
        k = 860 / sc["imgW"]
        hls = "".join(f'<div class="hl" id="{sid}-hl{i}" style="top:{h["y"]*k:.0f}px;height:{h["h"]*k:.0f}px"></div>' for i, h in enumerate(sc.get("hl", [])))
        body.append(f'<div id="{sid}-z" class="zw"><div class="mapbg"></div><div class="mapdots"></div><div id="{sid}-card" data-layout-allow-overflow>'
                    f'<div id="{sid}-page" data-layout-allow-overflow data-layout-allow-overlap><img src="{sc["img"]}" alt="" />{hls}</div></div></div>')
        for mv in sc.get("moves", []):
            tl.append(f'tl.to("#{sid}-page", {{y:{mv["y"]}, scale:{mv.get("scale",1)}, duration:{mv["d"]}, ease:"power2.inOut"}}, {mv["t"]});')
        for i, h in enumerate(sc.get("hl", [])):
            tl.append(f'tl.fromTo("#{sid}-hl{i}", {{scaleX:0, opacity:0}}, {{scaleX:1, opacity:1, duration:0.45, ease:"power2.out"}}, {h["t"]});')
    elif typ == "board":
        body.append(f'<div id="{sid}-z" class="zw"><div class="mapbg"></div><div class="mapdots"></div></div>')
        css.append(open(f"{P}/vector_map.css").read())
    # --- bảng số
    if typ == "board":
        css.append(f'#{sid}-list{{position:absolute;left:70px;width:860px;top:{sc.get("top",380)}px}}'
                   f'#{sid}-list .row{{position:relative;height:{sc.get("rowH",150)}px;border-top:1px solid rgba(255,255,255,.10)}}#{sid}-list .row:first-child{{border-top:none}}'
                   '.rin{position:absolute;inset:0;display:flex;align-items:center}'
                   '.ic{flex:none;width:44px;height:44px;margin:0 34px 0 8px;fill:none;stroke:var(--accent);stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}'
                   '.l1{white-space:nowrap;line-height:1}.n{font-size:88px;font-weight:800;font-variant-numeric:tabular-nums;letter-spacing:-.01em}'
                   '.big{font-size:50px;font-weight:800;line-height:1.1;white-space:nowrap}'
                   '.u{margin-left:14px;font-size:32px;font-weight:500;color:var(--ink75)}.l2{margin-top:8px;white-space:nowrap;font-size:28px;font-weight:500;color:var(--ink75)}.l2 .up{margin-left:14px}')
        rows = []
        for i, r in enumerate(sc["rows"], 1):
            a = round(r["t"] - 0.05, 2)
            up = f' <span class="up" id="{sid}-r{i}-up">{esc(r["up"])}</span>' if r.get("up") else ""
            if r.get("num") is not None:
                dec = r.get("dec", 0); start = round(r["num"] * 0.4, dec)
                if start <= 0: raise SystemExit(f"{sid}: số {r['num']} quá nhỏ để đếm (sẽ hiện 0) — dùng 'big' thay vì 'num'")
                main = f'<div class="l1"><span class="n" id="{sid}-r{i}-n">{start}</span><span class="u">{esc(r.get("unit",""))}</span></div>'
                tl.append(f'(() => {{ const el = document.querySelector("#{sid}-r{i}-n"), o = {{ v: {start} }}; el.textContent = fmt({start}, {dec}); '
                          f'tl.fromTo(o, {{ v: {start} }}, {{ v: {r["num"]}, duration: 0.8, ease: "power2.out", onUpdate: () => {{ el.textContent = fmt(o.v, {dec}); }} }}, {a}); }})();')
            else:
                main = f'<div class="l1 big">{esc(r["big"])}</div>'
            desc = f'<div class="l2">{esc(r.get("desc",""))}{up}</div>' if (r.get("desc") or up) else ""
            rows.append(f'<div class="row clip" id="{sid}-r{i}" data-start="{a}" data-duration="{round(dur - a, 2)}" data-track-index="5"><div class="rin">'
                        f'<svg class="ic" viewBox="0 0 24 24">{ICONS.get(r.get("icon","chart"))}</svg><div class="txt">{main}{desc}</div></div></div>')
            tl.append(f'tl.fromTo("#{sid}-r{i} .rin", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.35, ease:"expo.out"}}, {a});')
            if r.get("until"):
                tl.append(f'tl.to("#{sid}-r{i} .rin", {{opacity:0, duration:0.25, ease:"power1.in"}}, {r["until"]});')
            if r.get("up"):
                tl.append(f'tl.fromTo("#{sid}-r{i}-up", {{opacity:0}}, {{opacity:1, duration:0.3}}, {r.get("tup", a + 0.6)});')
        body.append(f'<div id="{sid}-list">' + "".join(rows) + "</div>")
        tl.append(f'tl.to("#{sid}-list .rin", {{opacity:0, duration:0.25, ease:"power1.in"}}, {dur - 0.45});')
    # --- nhãn phân đoạn, chân trang, dòng neo
    if sc.get("seg"):
        body.append(f'<div id="{sid}-seg" class="seg clip" data-start="0.15" data-duration="{round(dur - 0.15, 2)}" data-track-index="10" data-layout-allow-occlusion><span id="{sid}-segt">{esc(sc["seg"])}</span></div>')
        tl.append(f'tl.fromTo("#{sid}-segt", {{opacity:0}}, {{opacity:1, duration:0.3}}, 0.15); tl.to("#{sid}-segt", {{opacity:0, duration:0.25}}, {dur - 0.45});')
    if sc.get("foot"):
        body.append(f'<p id="{sid}-foot" class="foot clip" data-start="0.15" data-duration="{round(dur - 0.15, 2)}" data-track-index="11" data-layout-ignore><span id="{sid}-ft">{esc(sc["foot"])}</span></p>')
        tl.append(f'tl.fromTo("#{sid}-ft", {{opacity:0}}, {{opacity:1, duration:0.3}}, 0.2); tl.to("#{sid}-ft", {{opacity:0, duration:0.25}}, {dur - 0.45});')
    for i, a in enumerate(sc.get("anchors", [])):
        if a.get("dim"):
            body.append(f'<div id="{sid}-dim{i}" style="position:absolute;inset:0;background:rgba(14,26,43,.55);opacity:0"></div>')
            tl.append(f'tl.to("#{sid}-dim{i}", {{opacity:1, duration:0.35}}, {a["t"] - 0.1}); tl.to("#{sid}-dim{i}", {{opacity:0, duration:0.3}}, {min(a["t"] + a["d"], dur - 0.45)});')
        body.append(anchor_html(a, i, sid))
        tl.append(f'tl.fromTo("#{sid}-a{i} .w", {{opacity:0, y:18}}, {{opacity:1, y:0, duration:0.3, ease:"expo.out", stagger:0.09}}, {a["t"] + 0.03});')
        tl.append(f'tl.to("#{sid}-a{i} .w", {{opacity:0, duration:0.18, ease:"power1.in"}}, {min(a["t"] + a["d"] - 0.2, dur - 0.45)});')
    # --- vào / ra cảnh
    enter = sc.get("enter", "whip")
    if enter == "whip":
        tl.insert(0, f'tl.fromTo("#{sid}-z", {{scale:1.4, filter:"blur(10px)"}}, {{scale:1, filter:"blur(0px)", duration:0.2, ease:"power3.out"}}, 0);')
    elif enter == "blend":
        tl.insert(0, f'tl.fromTo("#root", {{opacity:0}}, {{opacity:1, duration:0.4, ease:"none"}}, 0);')
    if exit_whip:
        tl.append(f'tl.fromTo("#{sid}-z", {{scale:1, filter:"blur(0px)"}}, {{scale:1.35, filter:"blur(10px)", duration:0.17, ease:"power3.in", immediateRender:false}}, {dur - 0.17});')
    css.append(".zw{position:absolute;inset:0;transform-origin:540px 960px;overflow:hidden}")
    return f"""<template>
  <style>
{chr(10).join(css)}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
{chr(10).join(body)}
  </div>
  <script>
    (() => {{
      const tl = gsap.timeline({{ paused: true }});
      {fmt_js()}
      {mapjs}
      {chr(10).join("      " + l for l in tl)}
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
"""

def main():
    sb = json.load(open(sys.argv[1], encoding="utf-8")); P = sys.argv[2]
    os.makedirs(f"{P}/compositions", exist_ok=True)
    scs = sb["scenes"]; hosts = []
    for i, sc in enumerate(scs):
        nxt = scs[i + 1] if i + 1 < len(scs) else None
        open(f"{P}/compositions/{sc['id']}.html", "w", encoding="utf-8").write(scene(sc, nxt, P))
        hosts.append(f'      <div id="{sc["id"]}" data-composition-id="{sc["id"]}" data-composition-src="compositions/{sc["id"]}.html" data-start="{sc["start"]}" '
                     f'data-duration="{sc["dur"]}" data-track-index="{1 + i % 2}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{i + 1}"></div>')
    gsap = sb.get("gsap", "https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js")
    open(f"{P}/index.html", "w", encoding="utf-8").write(f"""<!doctype html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="{gsap}"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0E1A2B; }} #ground {{ position: absolute; inset: 0; background: #0E1A2B; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{sb['duration']}" data-width="1080" data-height="1920">
      <div id="ground"></div>
{chr(10).join(hosts)}
      <audio id="mix" class="clip" src="{sb.get('audio','assets/mix.wav')}" data-start="0" data-duration="{sb['duration']}" data-track-index="30" data-volume="1"></audio>
    </div>
    <script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
""")
    print(f"{len(scs)} cảnh -> {P}/compositions/, index.html")

if __name__ == "__main__":
    main()
```

## FILE: scripts/style_check.py

```python
#!/usr/bin/env python3
"""Kiểm tra cuối theo hệ thiết kế: chụp 1 khung/giây thành contact sheet + quét màu cấm.

  python style_check.py video.mp4 [--out style] [--per-sheet 15]

- sheet-NN.jpg: mỗi ô 1 giây, có nhãn thời gian và vùng TikTok che (đỏ mờ) -> soát bằng mắt: không chữ/nhãn nào nằm trong vùng đỏ; mỗi khung tối đa 1 tiêu đề lớn + 1 nhãn phân đoạn
  + nhãn kiểu A/B; không hộp đen, không phông thứ hai.
- Quét VÀNG (hue OpenCV 21–35, bão hoà và sáng cao) trong lớp đồ hoạ: > 0,3% khung -> cờ YELLOW.
  Cam nhấn #F28C28 có hue ≈ 14 nên không bị tính. Footage thật có vật màu vàng -> xem ảnh để quyết định.
Thoát mã 1 nếu có cờ.
"""
import argparse, os, sys
import cv2, numpy as np

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--out", default="style"); ap.add_argument("--per-sheet", type=int, default=15)
    ap.add_argument("--yellow", type=float, default=0.003)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    cap = cv2.VideoCapture(a.video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    tiles, flags = [], []
    for sec in range(int(n / fps) + 1):
        cap.set(cv2.CAP_PROP_POS_FRAMES, min(n - 1, int(sec * fps + fps / 2)))
        ok, fr = cap.read()
        if not ok: break
        small = cv2.resize(fr, (216, 384), interpolation=cv2.INTER_AREA)
        hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
        y = ((hsv[..., 0] >= 21) & (hsv[..., 0] <= 35) & (hsv[..., 1] > 150) & (hsv[..., 2] > 170)).mean()
        t = small.copy()
        # tô vùng bị giao diện TikTok che (đỏ mờ): trên 0–210, dưới 1440–1920, cột phải x>940 khi 700<y<1440
        ov = t.copy(); k = 216 / 1080
        for (x0, y0, x1, y1) in [(0, 0, 1080, 210), (0, 1440, 1080, 1920), (940, 700, 1080, 1440)]:
            cv2.rectangle(ov, (int(x0 * k), int(y0 * k)), (int(x1 * k), int(y1 * k)), (0, 0, 255), -1)
        t = cv2.addWeighted(ov, 0.18, t, 0.82, 0)
        cv2.rectangle(t, (0, 0), (70, 22), (0, 0, 0), -1)
        cv2.putText(t, f"{sec}s", (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        if y > a.yellow:
            flags.append((sec, f"YELLOW {y*100:.2f}%")); cv2.rectangle(t, (0, 0), (215, 383), (0, 255, 255), 3)
        tiles.append(t)
    cols = 5
    for k in range(0, len(tiles), a.per_sheet):
        chunk = tiles[k:k + a.per_sheet]
        while len(chunk) % cols: chunk.append(np.zeros_like(tiles[0]))
        rows = [np.hstack(chunk[i:i + cols]) for i in range(0, len(chunk), cols)]
        cv2.imwrite(f"{a.out}/sheet-{k // a.per_sheet + 1:02d}.jpg", np.vstack(rows))
    for s, m in flags: print(f"{s:4d}s  {m}")
    print(f"{len(tiles)} khung, {len(flags)} cờ -> {a.out}/sheet-*.jpg")
    sys.exit(1 if flags else 0)

if __name__ == "__main__":
    main()
```

## FILE: scripts/transcribe_vi.py

```python
#!/usr/bin/env python3
"""Chép lời tiếng Việt kèm mốc thời gian TỪNG TỪ (để đặt camera/chữ khớp giọng đọc).

  pip install faster-whisper numpy
  python transcribe_vi.py voice.mp3 transcript.json [--model small|medium|<thư mục model CTranslate2>]

Cần ffmpeg. Whisper hay nghe sai tên riêng và số (vd. "sông Tiền" -> "xong tiền", "19,34%" -> "39,34%"):
mọi con số đưa lên màn hình phải đối chiếu với nguồn báo, không lấy từ bản chép lời.
"""
import argparse, json, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

ap = argparse.ArgumentParser()
ap.add_argument("audio"); ap.add_argument("out"); ap.add_argument("--model", default="small")
a = ap.parse_args()
pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", a.audio, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
audio = np.frombuffer(pcm, dtype=np.float32)
m = WhisperModel(a.model, device="cpu", compute_type="int8")
segs, _ = m.transcribe(audio, language="vi", word_timestamps=True, beam_size=5)
out = []
for s in segs:
    out.append({"start": s.start, "end": s.end, "text": s.text.strip(),
                "words": [{"w": w.word.strip(), "s": w.start, "e": w.end} for w in s.words]})
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}", flush=True)
json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
```

## FILE: scripts/vector_map.css

```css
    .mapbg { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 42%, #13243A 0%, #0E1A2B 100%); }
    .map { position: absolute; left: 0; top: 0; }
    .map .vn { fill: #172A42; stroke: #5A7194; }
    .map .prov { fill: none; stroke: #4F6688; }
    .map .region { fill: #8A97A8; fill-opacity: 0.18; stroke: #B3BECB; opacity: 0; }
    .map .cmp { fill: #8A97A8; fill-opacity: 0.45; stroke: #B7C1CD; opacity: 0; }
    .map .vl { fill: #F28C28; fill-opacity: 0.8; stroke: #F8B677; opacity: 0; }
    .map .vl-glow { fill: none; stroke: #F28C28; opacity: 0; filter: blur(7px); }
    .map .rv-glow { fill: none; stroke: #33A3A8; opacity: 0.85; filter: blur(5px); stroke-linecap: round; stroke-dasharray: 100 120; stroke-dashoffset: 110; }
    .map .rv { fill: none; stroke: #B5DEDB; stroke-linecap: round; stroke-dasharray: 100 120; stroke-dashoffset: 110; }
    .map .coast-glow { fill: none; stroke: #F28C28; opacity: 0.9; filter: blur(6px); stroke-linecap: round; stroke-dasharray: 100 120; stroke-dashoffset: 110; }
    .map .coast { fill: none; stroke: #FFFFFF; stroke-linecap: round; stroke-dasharray: 100 120; stroke-dashoffset: 110; }
    .map .center { fill: #8A97A8; fill-opacity: 0.2; stroke: #B3BECB; opacity: 0; }
    .map .corr { fill: none; stroke: #B3BECB; stroke-linecap: round; stroke-dasharray: 100 120; stroke-dashoffset: 110; }
    .map .con { fill: none; stroke: #B3BECB; stroke-linecap: round; stroke-dasharray: 100 120; stroke-dashoffset: 110; }
    .map .ring { fill: none; stroke: #F28C28; opacity: 0; }
    .mapdots { position: absolute; inset: 0; pointer-events: none; background: radial-gradient(circle at 2px 2px, rgba(170,195,230,0.12) 1.1px, transparent 1.6px) 0 0 / 7px 7px; }
    .map .site { fill: #F28C28; fill-opacity: 0.32; stroke: #F8B677; }
```

## FILE: scripts/vector_map.js

```javascript
// ===== Bản đồ vector (Web Mercator, toạ độ thế giới ở mức Z=8) — dùng chung cho các cảnh =====
// GEO = { prov:{tên:d}, region:d, tien:d, hau:d, coast:d, lab:{key:[x,y]} } được nhúng sẵn phía trên.
function makeMap(opts) {
  const W = 1080, H = 1920, Z0 = GEO.Z;
  const NS = "http://www.w3.org/2000/svg";
  const svg = document.querySelector(opts.svg), world = svg.querySelector(".world");
  const el = (tag, attrs, parent = world) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); parent.appendChild(e); return e; };
  const stroked = []; // [el, screenWidthPx]
  const S = (e, w) => { stroked.push([e, w]); return e; };
  // lớp vẽ
  S(el("path", { d: GEO.prov._vn, class: "vn" }), 2);
  for (const k in GEO.prov) if (!k.startsWith("_")) S(el("path", { d: GEO.prov[k], class: "prov", "data-name": k }), 2);
  const region = S(el("path", { d: GEO.region, class: "region", id: opts.id + "-region" }), 3);
  const fill = {};
  for (const k of ["TP.HCM", "Cần Thơ"]) fill[k] = S(el("path", { d: GEO.prov[k], class: "cmp", id: opts.id + "-" + (k === "TP.HCM" ? "hcm" : "ct") }), 2);
  const vlGlow = S(el("path", { d: GEO.prov["Vĩnh Long"], class: "vl-glow", id: opts.id + "-vlglow" }), 14);
  const vl = S(el("path", { d: GEO.prov["Vĩnh Long"], class: "vl", id: opts.id + "-vl" }), 3);
  const rv = {};
  for (const k of ["tien", "hau"]) {
    rv[k + "g"] = S(el("path", { d: GEO[k], class: "rv-glow", pathLength: 100, id: opts.id + "-" + k + "g" }), 14);
    rv[k] = S(el("path", { d: GEO[k], class: "rv", pathLength: 100, id: opts.id + "-" + k }), 4);
  }
  const coastG = S(el("path", { d: GEO.coast, class: "coast-glow", pathLength: 100, id: opts.id + "-coastg" }), 18);
  const coast = S(el("path", { d: GEO.coast, class: "coast", pathLength: 100, id: opts.id + "-coast" }), 5);
  const L = GEO.lab;
  const center = el("circle", { cx: L.pt_ct[0] + 6, cy: L.pt_ct[1] + 14, r: 46, class: "center", id: opts.id + "-center" });
  S(center, 3);
  const q = (a, b, bend) => { const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, dx = b[0] - a[0], dy = b[1] - a[1];
    return `M${a[0]} ${a[1]} Q ${mx - dy * bend} ${my + dx * bend}, ${b[0]} ${b[1]}`; };
  const corridor = S(el("path", { d: q(L.pt_hcm, L.pt_vl, 0.18) + " " + q(L.pt_vl, L.pt_ct, 0.12).replace("M", "L").replace(/^L[^Q]+/, ""), class: "corr", pathLength: 100, id: opts.id + "-corr" }), 6);
  corridor.setAttribute("d", q(L.pt_hcm, L.pt_vl, 0.18) + " " + q(L.pt_vl, L.pt_ct, 0.12).replace(/^M[^Q]+/, ""));
  const conE = S(el("path", { d: q(L.pt_vl, L.coast, -0.25), class: "con", pathLength: 100, id: opts.id + "-cone" }), 5);
  const conC = S(el("path", { d: q(L.pt_vl, [L.pt_ct[0] + 6, L.pt_ct[1] + 14], 0.3), class: "con", pathLength: 100, id: opts.id + "-conc" }), 5);
  const rings = [0, 1, 2].map((i) => el("circle", { cx: L["Vĩnh Long"][0], cy: L["Vĩnh Long"][1] - 20, r: 1, class: "ring", id: opts.id + "-ring" + i }));
  rings.forEach((r) => S(r, 4));
  // nhãn HTML gắn toạ độ
  const labels = [...document.querySelectorAll(opts.labels)].map((n) => ({ n, p: L[n.dataset.at], dx: +(n.dataset.dx || 0), dy: +(n.dataset.dy || 0) }));
  // Kiểu A: chấm tại vật thể, đường dẫn tới (lx,ly), chữ canh theo hướng đường dẫn
  document.querySelectorAll(opts.labels + ".la").forEach((n) => {
    const lx = +(n.dataset.lx || 0), ly = +(n.dataset.ly || 0), al = n.dataset.align || (lx >= 0 ? "l" : "r");
    const lead = n.querySelector(".lead"), tx = n.querySelector(".tx");
    if (lead) { lead.style.width = Math.hypot(lx, ly) + "px"; lead.style.transform = `rotate(${Math.atan2(ly, lx)}rad)`; }
    if (tx) { const gx = al === "l" ? 10 : al === "r" ? -10 : 0, gy = al === "c" ? (ly >= 0 ? 12 : -12) : 0;
      tx.style.left = (lx + gx) + "px"; tx.style.top = (ly + gy) + "px";
      tx.style.transform = al === "l" ? "translate(0,-50%)" : al === "r" ? "translate(-100%,-50%)" : (ly >= 0 ? "translate(-50%,0)" : "translate(-50%,-100%)");
      tx.style.textAlign = al === "r" ? "right" : al === "c" ? "center" : "left"; }
  });
  const ringR = { r0: 0, r1: 0, r2: 0 };

  // camera: (lat,lng,Z) -> Hermite đơn điệu trên x,y,Z => vận tốc liên tục
  const mx = (lng) => ((lng + 180) / 360) * 256 * 2 ** Z0;
  const my = (lat) => { const r = (lat * Math.PI) / 180; return ((1 - Math.log(Math.tan(r) + 1 / Math.cos(r)) / Math.PI) / 2) * 256 * 2 ** Z0; };
  const KEYS = opts.keys.map(([t, lat, lng, Z, carry]) => ({ t, x: mx(lng), y: my(lat), Z, carry }));
  const TS = KEYS.map((k) => k.t);
  const slopes = (vs) => { const n = vs.length, dl = [], m = new Array(n).fill(0);
    for (let k = 0; k < n - 1; k++) dl[k] = (vs[k + 1] - vs[k]) / (TS[k + 1] - TS[k]);
    m[0] = opts.startMoving === false ? 0 : dl[0]; m[n - 1] = KEYS[n - 1].carry ? dl[n - 2] : 0;
    for (let k = 1; k < n - 1; k++) m[k] = dl[k - 1] * dl[k] <= 0 ? 0 : (dl[k - 1] + dl[k]) / 2;
    for (let k = 0; k < n - 1; k++) { if (dl[k] === 0) { m[k] = 0; m[k + 1] = 0; continue; }
      const a = m[k] / dl[k], b = m[k + 1] / dl[k], s = a * a + b * b;
      if (s > 9) { const tau = 3 / Math.sqrt(s); m[k] = tau * a * dl[k]; m[k + 1] = tau * b * dl[k]; } }
    return m; };
  const C = {}; ["x", "y", "Z"].forEach((c) => { const vs = KEYS.map((k) => k[c]); C[c] = { vs, m: slopes(vs) }; });
  const sample = (t) => { t = Math.min(Math.max(t, TS[0]), TS[TS.length - 1]); let i = 0; while (i < TS.length - 2 && t > TS[i + 1]) i++;
    const h = TS[i + 1] - TS[i], s = (t - TS[i]) / h, s2 = s * s, s3 = s2 * s, o = {};
    ["x", "y", "Z"].forEach((c) => { const { vs, m } = C[c];
      o[c] = (2 * s3 - 3 * s2 + 1) * vs[i] + (s3 - 2 * s2 + s) * h * m[i] + (-2 * s3 + 3 * s2) * vs[i + 1] + (s3 - s2) * h * m[i + 1]; });
    return o; };
  function apply(t) {
    const c = sample(t), s = 2 ** (c.Z - Z0), tx = W / 2 - c.x * s, ty = H / 2 - c.y * s;
    world.setAttribute("transform", `translate(${tx.toFixed(2)} ${ty.toFixed(2)}) scale(${s.toFixed(5)})`);
    stroked.forEach(([e, w]) => e.setAttribute("stroke-width", (w / s).toFixed(4)));
    (opts.rings || []).forEach(([t0, dur, rmax], i) => { const r = rings[i]; if (!r) return;
      const p = (t - t0) / dur;
      if (p < 0 || p > 1) { r.style.opacity = "0"; return; }
      const rr = 10 + (rmax - 10) * (1 - (1 - p) ** 2);
      r.setAttribute("r", (rr / s).toFixed(3)); r.style.opacity = (0.95 * (1 - p)).toFixed(3); });
    labels.forEach(({ n, p, dx, dy }) => { n.style.transform = `translate(${(p[0] * s + tx + dx).toFixed(1)}px, ${(p[1] * s + ty + dy).toFixed(1)}px)`; });
  }
  return { apply, ringR, sample };
}
```

## FILE: scripts/vmap.js

```javascript
// ===== vmap.js — bản đồ vector tổng quát (Web Mercator, toạ độ thế giới ở mức GEO.Z) =====
// GEO = { Z, prov:{tên: path d}, lab:{key:[x,y]}, lines:{key: path d}, ... } nhúng sẵn (scripts/geo_build.py).
// makeMap({ svg, id, labels, keys:[[t,lat,lng,Z,carry?]], layers:[...], rings:[[t0,dur,rmaxPx,ptKey]] })
//  layer: { geo:"prov:TÊN" | "lines:KHOÁ" | "raw:KHOÁ", cls, id, w (px màn hình), len:true (để vẽ dần bằng dashoffset) }
//       | { img:"assets/x.jpg", z, x0, y0, w, h, id, show:[Za,Zb] (hiện dần theo zoom) }
//       | { link:["ptA","ptB"], bend, cls, id, w }
// Ảnh vệ tinh/tile đặt đúng toạ độ thế giới => bay liền từ bản đồ vùng xuống tận công trường trong 1 cú máy.
function makeMap(opts) {
  const W = 1080, H = 1920, Z0 = GEO.Z, NS = "http://www.w3.org/2000/svg";
  const svg = document.querySelector(opts.svg), world = svg.querySelector(".world");
  const el = (tag, a, parent = world) => { const e = document.createElementNS(NS, tag); for (const k in a) e.setAttribute(k, a[k]); parent.appendChild(e); return e; };
  const stroked = [], imgs = [];
  const S = (e, w) => { if (w) stroked.push([e, w]); return e; };
  const L = GEO.lab;
  const q = (a, b, bend = 0.15) => { const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, dx = b[0] - a[0], dy = b[1] - a[1];
    return `M${a[0]} ${a[1]} Q ${mx - dy * bend} ${my + dx * bend}, ${b[0]} ${b[1]}`; };
  (opts.layers || []).forEach((ly) => {
    if (ly.img) {
      const k = 2 ** (ly.z - Z0);
      const e = el("image", { href: ly.img, x: ly.x0 / k, y: ly.y0 / k, width: ly.w / k, height: ly.h / k, id: ly.id || "", preserveAspectRatio: "none" });
      imgs.push([e, ly.show]); return;
    }
    let d;
    if (ly.link) d = q(L[ly.link[0]], L[ly.link[1]], ly.bend ?? 0.15);
    else { const [ns, key] = ly.geo.split(":"); d = ns === "prov" ? GEO.prov[key] : ns === "lines" ? GEO.lines[key] : GEO[key]; }
    if (!d) { console.warn("vmap: thiếu", ly.geo); return; }
    const a = { d, class: ly.cls || "", id: ly.id || "" };
    if (ly.len || ly.link) a.pathLength = 100;
    S(el("path", a), ly.w);
  });
  const rings = (opts.rings || []).map(([, , , pt]) => S(el("circle", { cx: L[pt][0], cy: L[pt][1], r: 1, class: "ring" }), 4));
  // nhãn HTML (kiểu A tự dựng đường dẫn; kiểu B đặt theo dx/dy)
  const labels = [...document.querySelectorAll(opts.labels)].map((n) => ({ n, p: L[n.dataset.at], dx: +(n.dataset.dx || 0), dy: +(n.dataset.dy || 0) }));
  labels.forEach(({ n, p }) => { if (!p) console.warn("vmap: nhãn thiếu toạ độ", n.dataset.at); });
  document.querySelectorAll(opts.labels + ".la").forEach((n) => {
    const lx = +(n.dataset.lx || 0), ly = +(n.dataset.ly || 0), al = n.dataset.align || (lx >= 0 ? "l" : "r");
    const lead = n.querySelector(".lead"), tx = n.querySelector(".tx");
    if (lead) { lead.style.width = Math.hypot(lx, ly) + "px"; lead.style.transform = `rotate(${Math.atan2(ly, lx)}rad)`; }
    if (tx) { const gx = al === "l" ? 10 : al === "r" ? -10 : 0, gy = al === "c" ? (ly >= 0 ? 12 : -12) : 0;
      tx.style.left = (lx + gx) + "px"; tx.style.top = (ly + gy) + "px";
      tx.style.transform = al === "l" ? "translate(0,-50%)" : al === "r" ? "translate(-100%,-50%)" : (ly >= 0 ? "translate(-50%,0)" : "translate(-50%,-100%)");
      tx.style.textAlign = al === "r" ? "right" : al === "c" ? "center" : "left"; }
  });
  // camera Hermite đơn điệu trên (x, y, Z): vận tốc liên tục, không vọt lố
  const mx = (lng) => ((lng + 180) / 360) * 256 * 2 ** Z0;
  const my = (lat) => { const r = (lat * Math.PI) / 180; return ((1 - Math.log(Math.tan(r) + 1 / Math.cos(r)) / Math.PI) / 2) * 256 * 2 ** Z0; };
  const KEYS = opts.keys.map(([t, lat, lng, Z, carry]) => ({ t, x: mx(lng), y: my(lat), Z, carry }));
  const TS = KEYS.map((k) => k.t);
  const slopes = (vs) => { const n = vs.length, dl = [], m = new Array(n).fill(0);
    for (let k = 0; k < n - 1; k++) dl[k] = (vs[k + 1] - vs[k]) / (TS[k + 1] - TS[k]);
    m[0] = opts.startMoving === false ? 0 : dl[0]; m[n - 1] = KEYS[n - 1].carry ? dl[n - 2] : 0;
    for (let k = 1; k < n - 1; k++) m[k] = dl[k - 1] * dl[k] <= 0 ? 0 : (dl[k - 1] + dl[k]) / 2;
    for (let k = 0; k < n - 1; k++) { if (dl[k] === 0) { m[k] = 0; m[k + 1] = 0; continue; }
      const a = m[k] / dl[k], b = m[k + 1] / dl[k], s = a * a + b * b;
      if (s > 9) { const tau = 3 / Math.sqrt(s); m[k] = tau * a * dl[k]; m[k + 1] = tau * b * dl[k]; } }
    return m; };
  const C = {}; ["x", "y", "Z"].forEach((c) => { const vs = KEYS.map((k) => k[c]); C[c] = { vs, m: slopes(vs) }; });
  const sample = (t) => { t = Math.min(Math.max(t, TS[0]), TS[TS.length - 1]); let i = 0; while (i < TS.length - 2 && t > TS[i + 1]) i++;
    const h = TS[i + 1] - TS[i], s = (t - TS[i]) / h, s2 = s * s, s3 = s2 * s, o = {};
    ["x", "y", "Z"].forEach((c) => { const { vs, m } = C[c];
      o[c] = (2 * s3 - 3 * s2 + 1) * vs[i] + (s3 - 2 * s2 + s) * h * m[i] + (-2 * s3 + 3 * s2) * vs[i + 1] + (s3 - s2) * h * m[i + 1]; });
    return o; };
  function apply(t) {
    const c = sample(t), s = 2 ** (c.Z - Z0), tx = W / 2 - c.x * s, ty = H / 2 - c.y * s;
    world.setAttribute("transform", `translate(${tx.toFixed(2)} ${ty.toFixed(2)}) scale(${s.toFixed(5)})`);
    stroked.forEach(([e, w]) => e.setAttribute("stroke-width", (w / s).toFixed(4)));
    imgs.forEach(([e, show]) => { if (!show) return; const [a, b] = show; e.style.opacity = String(Math.min(1, Math.max(0, (c.Z - a) / (b - a)))); });
    (opts.rings || []).forEach(([t0, dur, rmax], i) => { const r = rings[i]; const p = (t - t0) / dur;
      if (p < 0 || p > 1) { r.style.opacity = "0"; return; }
      r.setAttribute("r", ((10 + (rmax - 10) * (1 - (1 - p) ** 2)) / s).toFixed(3)); r.style.opacity = (0.95 * (1 - p)).toFixed(3); });
    labels.forEach(({ n, p, dx, dy }) => { if (p) n.style.transform = `translate(${(p[0] * s + tx + dx).toFixed(1)}px, ${(p[1] * s + ty + dy).toFixed(1)}px)`; });
  }
  return { apply, sample };
}
```

## FILE: scripts/vmap2.js

```javascript
// ===== vmap2.js — bản đồ "neon trên vệ tinh" cho motion.py =====
// GEO (geo_build.py) nhúng sẵn. makeMap2(opts):
//  opts.sat: [{img,z,x0,y0,w,h,show:[Za,Zb]|null}]          nền vệ tinh nhiều mức (đã làm tối, giảm bão hoà)
//  opts.layers: [{geo:"prov:X"|"lines:K", kind:"adm|proj|water|green|route", fill:bool, id, w, len}]
//  opts.links: [{a:"pt", b:"pt", bend, kind, id, w}]       đường nối giữa 2 điểm (route A->B)
//  opts.movers: [{path:id, t, d, icon:"car|train|boat|dot"}] icon chạy theo path (M6 đầu chấm, M9)
//  opts.rings: [{pt, t, km:[5,10,15]}]                      vòng bán kính theo km thật (M7)
//  opts.keys: [[t,lat,lng,Z(,carry)]]                       camera Hermite
// Trả về { apply(t), speedZ(t) } — speedZ dùng cho blur khi zoom nhanh (M2).
function makeMap2(opts) {
  const W = 1080, H = 1920, Z0 = GEO.Z, NS = "http://www.w3.org/2000/svg";
  // opts.pad: SVG lớn hơn khung (trái/trên) để khi nghiêng 3D (M3) mặt phẳng vẫn phủ kín màn hình
  const PL = (opts.pad || [0, 0])[0], PT = (opts.pad || [0, 0])[1];
  const svg = document.querySelector(opts.svg), world = svg.querySelector(".world");
  const el = (tag, a, parent = world) => { const e = document.createElementNS(NS, tag); for (const k in a) e.setAttribute(k, a[k]); parent.appendChild(e); return e; };
  const stroked = [], imgs = [], movers = [], rings = [];
  const S = (e, w) => { stroked.push([e, w]); return e; };
  const L = GEO.lab;
  (opts.sat || []).forEach((m) => { const k = 2 ** (m.z - Z0);
    imgs.push([el("image", { href: m.img, x: m.x0 / k, y: m.y0 / k, width: m.w / k, height: m.h / k, preserveAspectRatio: "none" }), m.show]); });
  const q = (a, b, bend = 0.15) => { const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, dx = b[0] - a[0], dy = b[1] - a[1];
    return `M${a[0]} ${a[1]} Q ${mx - dy * bend} ${my + dx * bend}, ${b[0]} ${b[1]}`; };
  const addLine = (d, ly) => {
    const kind = ly.kind || "adm", w = ly.w || 5, id = ly.id || "";
    const g = el("g", { id, class: "lyr k-" + kind });
    if (ly.fill) S(el("path", { d, class: "fill", id: id + "-fill" }, g), 0);
    const ga = { d, class: "glow", id: id + "-glow" }, ca = { d, class: "core", id: id + "-core" };
    if (ly.len) { ga.pathLength = 100; ca.pathLength = 100; ga.class += " len"; ca.class += " len"; }
    S(el("path", ga, g), w * 3.2); S(el("path", ca, g), w);
    return g;
  };
  (opts.layers || []).forEach((ly) => { const [ns, key] = ly.geo.split(":");
    const d = ns === "prov" ? GEO.prov[key] : ns === "lines" ? GEO.lines[key] : GEO[key];
    if (!d) { console.warn("vmap2: thiếu", ly.geo); return; } addLine(d, ly); });
  (opts.links || []).forEach((lk) => addLine(q(L[lk.a], L[lk.b], lk.bend ?? 0.15), Object.assign({ len: true, kind: "route" }, lk)));
  const ICON = {
    car: '<rect x="-14" y="-8" width="28" height="16" rx="5" fill="#fff"/><rect x="-7" y="-6" width="11" height="12" rx="2" fill="#E04BD6"/>',
    train: '<rect x="-17" y="-9" width="34" height="18" rx="8" fill="#fff"/><rect x="-11" y="-5" width="8" height="7" rx="1.5" fill="#E04BD6"/><rect x="2" y="-5" width="8" height="7" rx="1.5" fill="#E04BD6"/>',
    boat: '<path d="M-16 0 L16 0 L10 9 L-10 9 Z" fill="#fff"/><path d="M-2 0 L-2 -14 L9 -2 Z" fill="#2FD3E0"/>',
    dot: '<circle r="9" fill="#fff"/><circle r="16" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="3"/>',
  };
  (opts.movers || []).forEach((mv) => {
    const path = svg.querySelector("#" + mv.path + "-core"); if (!path) return;
    const g = el("g", { class: "mover", opacity: 0 }); g.innerHTML = ICON[mv.icon || "dot"];
    movers.push({ g, path, len: path.getTotalLength(), mv });
  });
  (opts.rings || []).forEach((rg) => { const lat = rg.lat || 11;
    const mpp = (156543.03 * Math.cos((lat * Math.PI) / 180)) / 2 ** Z0;
    rg.km.forEach((km, i) => { const c = S(el("circle", { cx: L[rg.pt][0], cy: L[rg.pt][1], r: 0.01, class: "ringc" }), 4);
      rings.push({ c, R: (km * 1000) / mpp, t0: rg.t + i * 0.45 }); }); });
  const mx = (lng) => ((lng + 180) / 360) * 256 * 2 ** Z0;
  const my = (lat) => { const r = (lat * Math.PI) / 180; return ((1 - Math.log(Math.tan(r) + 1 / Math.cos(r)) / Math.PI) / 2) * 256 * 2 ** Z0; };
  const KEYS = opts.keys.map(([t, lat, lng, Z, carry]) => ({ t, x: mx(lng), y: my(lat), Z, carry }));
  const TS = KEYS.map((k) => k.t);
  const slopes = (vs) => { const n = vs.length, dl = [], m = new Array(n).fill(0);
    for (let k = 0; k < n - 1; k++) dl[k] = (vs[k + 1] - vs[k]) / (TS[k + 1] - TS[k]);
    m[0] = opts.startMoving === false ? 0 : dl[0]; m[n - 1] = KEYS[n - 1].carry ? dl[n - 2] : 0;
    for (let k = 1; k < n - 1; k++) m[k] = dl[k - 1] * dl[k] <= 0 ? 0 : (dl[k - 1] + dl[k]) / 2;
    for (let k = 0; k < n - 1; k++) { if (dl[k] === 0) { m[k] = 0; m[k + 1] = 0; continue; }
      const a = m[k] / dl[k], b = m[k + 1] / dl[k], s = a * a + b * b;
      if (s > 9) { const tau = 3 / Math.sqrt(s); m[k] = tau * a * dl[k]; m[k + 1] = tau * b * dl[k]; } }
    return m; };
  const C = {}; ["x", "y", "Z"].forEach((c) => { const vs = KEYS.map((k) => k[c]); C[c] = { vs, m: slopes(vs) }; });
  const sample = (t) => { t = Math.min(Math.max(t, TS[0]), TS[TS.length - 1]); let i = 0; while (i < TS.length - 2 && t > TS[i + 1]) i++;
    const h = TS[i + 1] - TS[i], s = (t - TS[i]) / h, s2 = s * s, s3 = s2 * s, o = {};
    ["x", "y", "Z"].forEach((c) => { const { vs, m } = C[c];
      o[c] = (2 * s3 - 3 * s2 + 1) * vs[i] + (s3 - 2 * s2 + s) * h * m[i] + (-2 * s3 + 3 * s2) * vs[i + 1] + (s3 - s2) * h * m[i + 1]; });
    return o; };
  const labels = [...document.querySelectorAll(opts.labels)].map((n) => ({ n, p: L[n.dataset.at] }));
  function apply(t) {
    const c = sample(t), s = 2 ** (c.Z - Z0), tx = W / 2 - c.x * s, ty = H / 2 - c.y * s;
    world.setAttribute("transform", `translate(${(tx + PL).toFixed(2)} ${(ty + PT).toFixed(2)}) scale(${s.toFixed(5)})`);
    stroked.forEach(([e, w]) => w && e.setAttribute("stroke-width", (w / s).toFixed(4)));
    imgs.forEach(([e, show]) => { if (show) e.style.opacity = String(Math.min(1, Math.max(0, (c.Z - show[0]) / (show[1] - show[0])))); });
    movers.forEach(({ g, path, len, mv }) => { const p = (t - mv.t) / mv.d;
      if (p < 0) { g.setAttribute("opacity", 0); return; }
      const e = Math.min(1, p), pe = e < 0.5 ? 2 * e * e : 1 - (-2 * e + 2) ** 2 / 2, pt = path.getPointAtLength(len * pe),
        pt2 = path.getPointAtLength(Math.min(len, len * pe + 0.5)), ang = (Math.atan2(pt2.y - pt.y, pt2.x - pt.x) * 180) / Math.PI;
      g.setAttribute("opacity", 1);
      g.setAttribute("transform", `translate(${pt.x} ${pt.y}) scale(${((mv.size || 2) / s).toFixed(5)}) rotate(${mv.icon === "dot" ? 0 : ang})`); });
    rings.forEach(({ c: ci, R, t0 }) => { const p = Math.min(1, Math.max(0, (t - t0) / 0.8)); ci.setAttribute("r", Math.max(0.01, R * (1 - (1 - p) ** 3)));
      ci.style.opacity = p > 0 ? 1 : 0; });
    labels.forEach(({ n, p }) => { if (p) n.style.transform = `translate(${(p[0] * s + tx).toFixed(1)}px, ${(p[1] * s + ty).toFixed(1)}px)`; });
  }
  const speedZ = (t) => Math.abs(sample(t + 0.04).Z - sample(t - 0.04).Z) / 0.08;
  return { apply, sample, speedZ, rings };
}
```

## FILE: scripts/vmap3.js

```javascript
// ===== vmap3.js — MỘT camera liên tục trên MỘT bản đồ sống (flight.py) =====
// GEO (geo_build.py) nhúng sẵn. makeMap3(opts):
//  opts.keys: [[t,lat,lng,Z,pitch,bearing]]  camera Hermite đơn điệu trên CẢ 5 kênh (không giật, không dừng gắt)
//  opts.sat: [{img,z,x0,y0,w,h,show:[Za,Zb]|null, hide:[Za,Zb]}]  nền vệ tinh nhiều mức (hiện/ẩn theo Z)
//  opts.layers / opts.links / opts.movers / opts.rings  như vmap2 (rings có thể có id)
//  opts.circles: [{id, pt, r_m, kind, heat}]   hình tròn đúng diện tích theo mét (V5) hoặc điểm nóng (V8)
//  opts.blocks: [{lng,lat,w,d,ang,g}]           khối 3D mọc từ mặt đất (V6); chiều cao theo nhóm g: window.BH[g] (0..1) × opts.blockH[g] (m)
//  opts.pad: [trái, trên]                       SVG rộng hơn khung để khi nghiêng/xoay vẫn phủ kín
// Trả về { apply(t) -> camera, sample(t) }.
function makeMap3(opts) {
  const W = 1080, H = 1920, Z0 = GEO.Z, NS = "http://www.w3.org/2000/svg";
  const PL = (opts.pad || [0, 0])[0], PT = (opts.pad || [0, 0])[1];
  const svg = document.querySelector(opts.svg), world = svg.querySelector(".world");
  const el = (tag, a, parent = world) => { const e = document.createElementNS(NS, tag); for (const k in a) e.setAttribute(k, a[k]); parent.appendChild(e); return e; };
  const stroked = [], imgs = [], movers = [], rings = [];
  const S = (e, w) => { stroked.push([e, w]); return e; };
  const L = GEO.lab;
  const mx = (lng) => ((lng + 180) / 360) * 256 * 2 ** Z0;
  const my = (lat) => { const r = (lat * Math.PI) / 180; return ((1 - Math.log(Math.tan(r) + 1 / Math.cos(r)) / Math.PI) / 2) * 256 * 2 ** Z0; };
  const m2w = (lat) => 2 ** Z0 / (156543.03 * Math.cos((lat * Math.PI) / 180));   // mét -> đơn vị thế giới (Z0)
  const defs = el("defs", {});
  defs.innerHTML = '<radialGradient id="heatg"><stop offset="0" stop-color="#FACC15" stop-opacity=".85"/><stop offset=".45" stop-color="#F28C28" stop-opacity=".45"/><stop offset="1" stop-color="#F28C28" stop-opacity="0"/></radialGradient>';
  (opts.sat || []).forEach((m) => { const k = 2 ** (m.z - Z0);
    imgs.push([el("image", { href: m.img, x: m.x0 / k, y: m.y0 / k, width: m.w / k, height: m.h / k, preserveAspectRatio: "none" }), m.show, m.hide]); });
  const q = (a, b, bend = 0.15) => { const mx_ = (a[0] + b[0]) / 2, my_ = (a[1] + b[1]) / 2, dx = b[0] - a[0], dy = b[1] - a[1];
    return `M${a[0]} ${a[1]} Q ${mx_ - dy * bend} ${my_ + dx * bend}, ${b[0]} ${b[1]}`; };
  const addLine = (d, ly) => {
    const kind = ly.kind || "adm", w = ly.w || 5, id = ly.id || "";
    const g = el("g", { id, class: "lyr k-" + kind + (ly.cls ? " " + ly.cls : ""), opacity: ly.op ?? 0 });
    if (ly.fill) S(el("path", { d, class: "fill", id: id + "-fill", style: "opacity:0" }, g), 0);
    const ga = { d, class: "glow", id: id + "-glow" }, ca = { d, class: "core", id: id + "-core" };
    if (ly.len) { ga.pathLength = 100; ca.pathLength = 100; ga.class += " len"; ca.class += " len"; }
    S(el("path", ga, g), w * 3.2); S(el("path", ca, g), w);
    return g;
  };
  (opts.layers || []).forEach((ly) => { const [ns, key] = ly.geo.split(":");
    const d = ns === "prov" ? GEO.prov[key] : ns === "lines" ? GEO.lines[key] : GEO[key];
    if (!d) { console.warn("vmap3: thiếu", ly.geo); return; } addLine(d, ly); });
  (opts.links || []).forEach((lk) => addLine(q(L[lk.a], L[lk.b], lk.bend ?? 0.15), Object.assign({ len: true, kind: "route" }, lk)));
  const host0 = () => document.querySelector(opts.blockHost || "body"), discs = [];
  (opts.circles || []).forEach((c) => { const p = L[c.pt], R = c.r_m * m2w(c.lat || 11);
    const e = document.createElement("div"); e.id = c.id; e.className = "disc " + (c.heat ? "heat" : "k-" + (c.kind || "proj")); e.style.opacity = 0;
    host0().appendChild(e); discs.push({ e, p, R }); });
  const ICON = {
    car: '<rect x="-14" y="-8" width="28" height="16" rx="5" fill="#fff"/><rect x="-7" y="-6" width="11" height="12" rx="2" fill="#E04BD6"/>',
    train: '<rect x="-17" y="-9" width="34" height="18" rx="8" fill="#fff"/><rect x="-11" y="-5" width="8" height="7" rx="1.5" fill="#E04BD6"/><rect x="2" y="-5" width="8" height="7" rx="1.5" fill="#E04BD6"/>',
    bike: '<circle r="13" fill="#fff"/><path d="M-7 3 L-2 -5 L5 3 M-2 -5 L3 -5" stroke="#2FD3E0" stroke-width="2.6" fill="none" stroke-linecap="round"/><circle cx="-7" cy="3" r="3.2" fill="none" stroke="#2FD3E0" stroke-width="2"/><circle cx="6" cy="3" r="3.2" fill="none" stroke="#2FD3E0" stroke-width="2"/>',
    plane: '<path d="M14 0 L-6 -12 L-3 -2 L-12 -2 L-15 -7 L-17 -7 L-15 0 L-17 7 L-15 7 L-12 2 L-3 2 L-6 12 Z" fill="#fff"/>',
    dot: '<circle r="9" fill="#fff"/><circle r="16" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="3"/>',
  };
  (opts.movers || []).forEach((mv) => {
    const path = svg.querySelector("#" + mv.path + "-core"); if (!path) return;
    const g = el("g", { class: "mover", opacity: 0 }); g.innerHTML = ICON[mv.icon || "dot"];
    movers.push({ g, path, len: path.getTotalLength(), mv });
  });
  (opts.rings || []).forEach((rg) => { const lat = rg.lat || 11;
    rg.km.forEach((km, i) => { const e = document.createElement("div"); e.className = "ring"; if (rg.id) e.dataset.g = rg.id; host0().appendChild(e);
      rings.push({ e, p: L[rg.pt], R: km * 1000 * m2w(lat), t0: rg.t + i * 0.45, t1: rg.out ?? 1e9 }); }); });
  // ---- khối 3D (V6)
  const host = document.querySelector(opts.blockHost || "body"), blocks = [];
  window.BH = window.BH || {};
  (opts.blocks || []).forEach((b) => {
    const e = document.createElement("div"); e.className = "blk g-" + b.g;
    e.innerHTML = '<i class="f top"></i><i class="f s1"></i><i class="f s2"></i><i class="f s3"></i><i class="f s4"></i>';
    host.appendChild(e); const k = m2w(b.lat);
    blocks.push({ e, f: [...e.children], x: mx(b.lng), y: my(b.lat), w: b.w * k, d: b.d * k, ang: b.ang || 0, g: b.g, k }); });
  // ---- camera Hermite 5 kênh
  const KEYS = opts.keys.map(([t, lat, lng, Z, p = 0, b = 0]) => ({ t, x: mx(lng), y: my(lat), Z, p, b }));
  const TS = KEYS.map((k) => k.t);
  const slopes = (vs) => { const n = vs.length, dl = [], m = new Array(n).fill(0);
    for (let k = 0; k < n - 1; k++) dl[k] = (vs[k + 1] - vs[k]) / (TS[k + 1] - TS[k]);
    m[0] = 0; m[n - 1] = 0;
    for (let k = 1; k < n - 1; k++) m[k] = dl[k - 1] * dl[k] <= 0 ? 0 : (dl[k - 1] + dl[k]) / 2;
    for (let k = 0; k < n - 1; k++) { if (dl[k] === 0) { m[k] = 0; m[k + 1] = 0; continue; }
      const a = m[k] / dl[k], b = m[k + 1] / dl[k], s = a * a + b * b;
      if (s > 9) { const tau = 3 / Math.sqrt(s); m[k] = tau * a * dl[k]; m[k + 1] = tau * b * dl[k]; } }
    return m; };
  const CH = ["x", "y", "Z", "p", "b"], C = {};
  CH.forEach((c) => { const vs = KEYS.map((k) => k[c]); C[c] = { vs, m: slopes(vs) }; });
  const sample = (t) => { t = Math.min(Math.max(t, TS[0]), TS[TS.length - 1]); let i = 0; while (i < TS.length - 2 && t > TS[i + 1]) i++;
    const h = TS[i + 1] - TS[i], s = (t - TS[i]) / h, s2 = s * s, s3 = s2 * s, o = {};
    CH.forEach((c) => { const { vs, m } = C[c];
      o[c] = (2 * s3 - 3 * s2 + 1) * vs[i] + (s3 - 2 * s2 + s) * h * m[i] + (-2 * s3 + 3 * s2) * vs[i + 1] + (s3 - s2) * h * m[i + 1]; });
    return o; };
  const labels = [...document.querySelectorAll(opts.labels)].map((n) => ({ n, p: L[n.dataset.at] }));
  // ---- mờ chuyển động theo vận tốc camera (màn trập 180° = nửa quãng đi trong 1 khung)
  // Lọc trên khung nhìn 1080×1920 (opts.blurHost), không lọc cả SVG khổng lồ; chỉ bật khi vệt ≥ 2 px (dưới đó mắt không thấy).
  const MB = opts.motionBlur, fps = opts.fps || 30;
  let mbHost = null, fe = null;
  if (MB) { mbHost = document.querySelector(opts.blurHost);
    const ns = document.createElementNS(NS, "svg"); ns.setAttribute("width", 0); ns.setAttribute("height", 0); ns.style.position = "absolute";
    ns.innerHTML = '<filter id="mbf" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB"><feGaussianBlur id="mbg" stdDeviation="0 0" edgeMode="duplicate"/></filter>';
    document.body.appendChild(ns); fe = ns.querySelector("#mbg"); }
  function blurAt(t) {
    if (!MB) return;
    const a = sample(t - 0.5 / fps), b = sample(t + 0.5 / fps), s = 2 ** ((a.Z + b.Z) / 2 - Z0), sh = (MB.shutter || 180) / 360;
    const br = ((a.b + b.b) / 2) * Math.PI / 180, mx_ = (b.x - a.x) * s, my_ = (b.y - a.y) * s;
    const vx = Math.abs(mx_ * Math.cos(br) - my_ * Math.sin(br)), vy = Math.abs(mx_ * Math.sin(br) + my_ * Math.cos(br)) * (1 + a.p / 90);
    const rad = (Math.abs(b.Z - a.Z) * Math.LN2 * 540 + Math.abs(b.b - a.b) * Math.PI / 180 * 540) * 0.5;
    const Lx = (vx + rad) * sh, Ly = (vy + rad) * sh;                      // độ dài vệt (px)
    if (Math.max(Lx, Ly) < (MB.min || 2)) { mbHost.style.filter = ""; return; }
    fe.setAttribute("stdDeviation", `${(Lx / 3.46).toFixed(2)} ${(Ly / 3.46).toFixed(2)}`); mbHost.style.filter = "url(#mbf)";
  }
  function apply(t) {
    blurAt(t);
    const c = sample(t), s = 2 ** (c.Z - Z0), tx = W / 2 - c.x * s, ty = H / 2 - c.y * s;
    world.setAttribute("transform", `translate(${(tx + PL).toFixed(2)} ${(ty + PT).toFixed(2)}) scale(${s.toFixed(6)})`);
    stroked.forEach(([e, w]) => w && e.setAttribute("stroke-width", (w / s).toFixed(5)));
    imgs.forEach(([e, show, hide]) => { let o = 1;
      if (show) o = Math.min(1, Math.max(0, (c.Z - show[0]) / (show[1] - show[0])));
      if (hide) o *= Math.min(1, Math.max(0, (hide[1] - c.Z) / (hide[1] - hide[0])));
      e.style.opacity = String(o); e.style.display = o > 0.001 ? "" : "none"; });
    movers.forEach(({ g, path, len, mv }) => { const p = (t - mv.t) / mv.d;
      if (p < 0 || (mv.out && t > mv.out)) { g.setAttribute("opacity", 0); return; }
      const e = Math.min(1, p), pe = e < 0.5 ? 2 * e * e : 1 - (-2 * e + 2) ** 2 / 2, pt = path.getPointAtLength(len * pe),
        pt2 = path.getPointAtLength(Math.min(len, len * pe + 0.5)), ang = (Math.atan2(pt2.y - pt.y, pt2.x - pt.x) * 180) / Math.PI;
      g.setAttribute("opacity", 1);
      g.setAttribute("transform", `translate(${pt.x} ${pt.y}) scale(${((mv.size || 2) / s).toFixed(6)}) rotate(${mv.icon === "dot" || mv.icon === "bike" ? 0 : ang})`); });
    const place = (e, p, r) => { e.style.width = e.style.height = (2 * r).toFixed(1) + "px";
      e.style.transform = `translate(${(p[0] * s + tx - r).toFixed(1)}px, ${(p[1] * s + ty - r).toFixed(1)}px)`; };
    rings.forEach(({ e, p, R, t0, t1 }) => { const k = Math.min(1, Math.max(0, (t - t0) / 0.8)), fo = t > t1 ? Math.max(0, 1 - (t - t1) / 0.6) : 1;
      e.style.opacity = k > 0 ? fo : 0; if (k > 0 && fo > 0) place(e, p, R * s * (1 - (1 - k) ** 3)); });
    discs.forEach(({ e, p, R }) => place(e, p, R * s));
    // nhãn nằm trên mặt bản đồ nhưng xoay ngược bearing để luôn đọc thẳng
    labels.forEach(({ n, p }) => { if (p) n.style.transform = `translate(${(p[0] * s + tx).toFixed(1)}px, ${(p[1] * s + ty).toFixed(1)}px) rotate(${(-c.b).toFixed(2)}deg)`; });
    blocks.forEach((b) => { const g = window.BH[b.g] || 0;
      if (g <= 0.001) { b.e.style.display = "none"; return; } b.e.style.display = "";
      const w = b.w * s, d = b.d * s, h = (opts.blockH?.[b.g] || 20) * b.k * s * g;
      b.e.style.width = w + "px"; b.e.style.height = d + "px";
      b.e.style.transform = `translate(${(b.x * s + tx - w / 2).toFixed(1)}px, ${(b.y * s + ty - d / 2).toFixed(1)}px) rotate(${b.ang}deg)`;
      const [top, s1, s2, s3, s4] = b.f;
      top.style.transform = `translateZ(${h.toFixed(2)}px)`;
      s1.style.cssText = `width:${w}px;height:${h}px;top:0;transform:rotateX(90deg)`;
      s2.style.cssText = `width:${w}px;height:${h}px;top:${d}px;transform:rotateX(90deg)`;
      s3.style.cssText = `width:${h}px;height:${d}px;left:0;transform:rotateY(-90deg)`;
      s4.style.cssText = `width:${h}px;height:${d}px;left:${w}px;transform:rotateY(-90deg)`; });
    return c;
  }
  const speed = (t) => { const a = sample(t - 0.05), b = sample(t + 0.05), s = 2 ** (a.Z - Z0);
    return { pan: Math.hypot(b.x - a.x, b.y - a.y) * s / 0.1, Z: Math.abs(b.Z - a.Z) / 0.1, p: Math.abs(b.p - a.p) / 0.1, b: Math.abs(b.b - a.b) / 0.1 }; };
  return { apply, sample, speed };
}
```

## FILE: templates/ha-tang-flight/LOG.md

```markdown
# Nhật ký giao — "99% vẫn chưa thông xe" (hạ tầng quanh One Era)

1080×1920 · 30 fps cố định · 130,6 s · một camera liên tục, 0 cắt cứng · bản đồ không biến mất quá 2,6 s (1 lần zoom-through)

## (b) Kiểu trực quan hoá theo chương

| Timecode | Chương | Kiểu chính | Chuyển động camera | Lớp trên bản đồ | Footage |
|---|---|---|---|---|---|
| 0:00.00–0:15.60 | 99% của 17 km cầu cạn | V10 | hạ từ mây (Z 7,2 → 12,1), nghiêng 22° | đoạn cầu cạn vẽ dần, thẻ 99%, 1%, 30/11, thiếu nhựa · đá, cửa sổ ảnh | — |
| 0:15.60–0:25.10 | Trên bản đồ vẽ xong | V2 | kéo ra Đông Bắc TP.HCM, về 0° | TP.HCM sáng (cam), tỉnh lân cận mờ 40%, mọi tuyến vẽ mờ, cửa sổ ảnh | — |
| 0:25.10–0:34.50 | One Era giữa QL13 và Vành đai 3 | V1 | fly-to, nghiêng 44° ≤ 4 s | ranh One Era vẽ + phủ, nhãn QL13/VĐ3, câu hỏi | — |
| 0:34.50–0:57.20 | 76 km · 75.300 tỷ · 81% | V5 | kéo ra toàn tuyến Z 9,8, lia chậm | vòng VĐ3, thẻ 76 km / 75.300 tỷ / 81%, 4 vòng tròn tỉ lệ tiến độ, Tân Vạn | — |
| 0:57.20–1:06.30 | Tân Vạn → Nhơn Trạch → Long Thành | V3 | bám đầu tuyến xuống phía Nam rồi sang Đông | tuyến có xe chạy, cầu Nhơn Trạch, sân bay Long Thành | — |
| 1:06.30–1:26.70 | QL13 đi trước một bước | V8 | lia dọc QL13 từ Bắc xuống Nam, nghiêng 24° | hành lang tô theo trạng thái + chú giải, thẻ 8 làn, logo, 6 km chờ | — |
| 1:26.70–1:44.40 | Metro TP mới Bình Dương – Suối Tiên | V9 | lia theo hướng tuyến về Suối Tiên | tuyến vẽ dần có tàu chạy, mốc cuối 2026 / 2030, ghim ga | — |
| 1:44.40–1:52.80 | Metro số 1: nhu cầu đã rõ | V6 | nghiêng 26 → 33°, quay 12° | 2 cột 3D theo số lượt, thẻ 8,86 triệu, thẻ tổ chức | — |
| 1:52.80–2:02.60 | Hạ tầng đến theo từng đợt | V4 | về One Era, đẩy nhẹ | 3 vòng: QL13 · VĐ3 · Metro | — |
| 2:02.60–2:10.60 | Lăn bánh năm nào? | V1 | zoom-through → kéo ra Z 11,85 | mọi lớp + ranh One Era phát sáng + câu hỏi | 2:02.90 phối cảnh One Era (CĐT, qua The Leader) |


Không hai chương liền nhau cùng kiểu; V1 dùng 2 lần không liền nhau (mở One Era và kết), mỗi kiểu ≤ 20% thời lượng.

## (a) Các đoạn giữ khung (≥ 1 s, < 6 px/khung)

| Từ | Đến | Kiểu trôi | Tốc độ trung vị (px/khung) | Đổi chiều |
|---|---|---|---|---|
| 0:06.87 | 0:15.80 | khoá | 0.00 | 0 |
| 0:18.33 | 0:25.10 | zoom | 0.23 | 1 |
| 0:31.77 | 0:33.53 | quay | 3.58 | 2 |
| 0:39.53 | 0:50.60 | khoá | 0.00 | 0 |
| 0:52.90 | 1:06.73 | lia | 3.64 | 4 |
| 1:11.77 | 1:26.40 | khoá | 0.00 | 0 |
| 1:28.90 | 1:39.10 | khoá | 0.00 | 0 |
| 1:40.57 | 1:44.73 | khoá | 0.00 | 0 |
| 1:46.03 | 1:53.00 | khoá | 0.00 | 0 |
| 1:55.23 | 2:00.33 | khoá | 0.00 | 0 |
| 2:03.07 | 2:05.60 | zoom | 1.75 | 1 |


Chống rung (flight.py kiểm trên từng khung): tốc độ mặt đất tối đa ≤ 25 px/khung; mọi đoạn giữ đổi chiều ≤ 10 lần/5 s; không đoạn trôi < 1,5 px/khung quá 1,2 s (giữ đọc số liệu = khoá hẳn camera, chỉ lớp phủ chuyển động); nghiêng > 35° chỉ ≤ 4 s (31,8–33,5 s, khoảnh khắc tới One Era).
Mờ chuyển động: màn trập 180°, kernel đường thẳng ≥ 16 mẫu theo vận tốc camera trên màn hình, 988/3918 khung (25%, đúng các cú máy), vệt dài nhất 6 px; khung giữ để sắc. Nền vệ tinh làm mềm Gaussian 0,8 px, tối 20%, giảm bão hoà 15%.

## (c) Tài sản tải về

| Tên | Nguồn (URL) | Độ phân giải | Dùng lúc | Ghi chú |
|---|---|---|---|---|
| vd3_caucan.jpg | https://cdnphoto.dantri.com.vn/3m10PVuksY8HMjdIX7qYR8-OgF0=/thumb_w/1020/2026/11/12/vanhdai3baoquyen-1790704110265-1794486191605.jpg | 1020×680 | 0:04.20–0:06.70 (cửa sổ ảnh) | Dân trí 12/11/2026, ảnh Bảo Quyên; cửa sổ ảnh 560 px (không phóng to toàn khung) |
| vd3_aerial.jpg | https://images2.thanhnien.vn/528068263637045248/2026/8/24/edit-vanh-dai-3-di-qua-vinhome-17875581803371189682545.jpeg | 2560×1707 | 0:20.60–0:23.10 (cửa sổ ảnh) | Thanh Niên; watermark góc, không che chủ thể |
| tanvan.jpg | https://image.sggp.org.vn/w2000/Uploaded/2026/ycwkpcvo/2026_09_20/tvan7-2212-1980.jpg.webp | 1280×642 | 0:53.40–0:55.90 (cửa sổ ảnh) | SGGP 20/09/2026, ảnh Quốc Hùng |
| ql13.jpg | https://cdnphoto.dantri.com.vn/O8q_uoHwgKp-RvcLx_AaAVtsJFk=/thumb_w/1920/2026/02/13/morongquoclo13binhduongxuandoan-edited-1770988718424.jpg | 1920×1280 | 1:12.40–1:14.90 (cửa sổ ảnh) | Dân trí 13/02/2026; watermark góc |
| metro1_crowd.jpg | https://image.sggp.org.vn/w2000/Uploaded/2026/ycwkpcvo/2025_12_18/18metro2-7063-4055.jpg.webp | 1280×960 | 1:27.90–1:30.40 (cửa sổ ảnh) | SGGP, ảnh Quốc Hùng |
| metro1.jpg | https://image.sggp.org.vn/w2000/Uploaded/2026/ycwkpcvo/2025_12_18/18mtro-1280-5109.jpg.webp | 1280×799 | 1:40.60–1:43.10 (cửa sổ ảnh) | SGGP, ảnh Quốc Hùng |
| p7.jpg (One Era) | https://theleader.vn/kim-oanh-group-bat-tay-ong-lon-longfor-quy-hoach-khu-do-thi-one-era-d47799.html | 1920×1143 | 2:02.90–2:05.50 (zoom-through) | phối cảnh CĐT, đã dùng ở video trước |
| vd3_tanvan2.jpg | https://cdnphoto.dantri.com.vn/q2g5lStQyOdc-OY2GeDVOKJGzuM=/thumb_w/1020/2026/10/02/vanhdai3baoquyen-1790704239788-1790951935727.jpg | 1020×680 | 0:37.00–0:39.50 (cửa sổ ảnh) | Dân trí 03/10/2026, ảnh Bảo Quyên (nút giao Tân Vạn) |
| ql13b.jpg | https://cdnphoto.dantri.com.vn/AL04UWPs3xTN_LLUIE581haT4gc=/thumb_w/1920/2026/02/13/morongquoclo13binhduongxuandoan-edited-1770988644048.jpg | 1920×1280 | 1:55.80–1:58.30 (cửa sổ ảnh) | Dân trí 13/02/2026; watermark góc |
| Material Symbols Rounded (fill) 0.49.0 | https://registry.npmjs.org/@material-symbols/svg-400 | vector | mọi huy hiệu | một họ icon, Apache-2.0 |
| HCMC Metro logo.svg | https://commons.wikimedia.org/wiki/File:HCMC_Metro_logo.svg | vector | — | KHÔNG tải được (upload.wikimedia.org trả 429 nhiều lần) → huy hiệu chữ M1 |
| logo Sở Xây dựng TP.HCM | https://sxd.hochiminhcity.gov.vn/ | — | — | trang chính thức không phản hồi (502), không có trên Wikimedia → huy hiệu chữ SXD |
| ảnh vệ tinh | https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer | z3–z16 | toàn video | Esri, Maxar; làm mờ 0,8 px, tối 20%, giảm bão hoà 15% |
| hình học Vành đai 3 gần Tân Vạn | https://www.openstreetmap.org/relation/13490968 | vector | 0:00–1:07 | OSM (ODbL); đoạn phía Đông dò trên ảnh vệ tinh; phần còn lại gần đúng |

Icon dùng (Material Symbols Rounded, fill): add_road, calendar_month, check_circle, construction, directions_car, flight, groups, help, hourglass_top, location_city, payments, route, schedule, subway, swap_horiz, trending_up, warning.

## Số liệu & nguồn

- 17 km cầu cạn phía Đông ≈ 99% khối lượng; mốc 30/11; thiếu nhựa và đá chất lượng cao — Dân trí 12/11/2026, Thanh Niên 13/11/2026.
- Vành đai 3 dài ≈ 76,3 km, tổng mức đầu tư > 75.300 tỷ — Thanh Niên 13/11/2026 (lời đọc nói "hơn 75.000 tỷ"; màn hình ghi 75.300 theo nguồn).
- 81% giá trị hợp đồng; Tây Ninh 95,6%, TP.HCM 82,1%, Đồng Nai 78,8%, Bình Dương cũ 71,7%; hạng mục nút giao Tân Vạn lùi sang quý I/2027 — Dân trí 03/10/2026 (báo cáo Chính phủ gửi Quốc hội).
- QL13: đoạn hơn 9 km Ông Bố – Nguyễn Thị Minh Khai 8 làn, cơ bản hoàn thành — CafeF 29/05/2026, Dân trí 13/02/2026; đoạn ≈ 6 km phía cầu Bình Triệu chờ khởi công. Con số "mở rộng lên 60 m" chưa tìm được nguồn nên KHÔNG đưa lên màn hình.
- Metro TP mới Bình Dương – Suối Tiên: Tiền Phong 07/09/2026 ghi 30,66 km qua Thuận Giao, An Phú, Dĩ An…, khởi công cuối 2026, xong 2030. Lời đọc nói 32,8 km — màn hình ghi ≈ 30,7 km theo nguồn.
- Metro số 1: "hơn 10 triệu lượt trong 5 tháng" chưa tìm được nguồn; số có nguồn là 8,86 triệu lượt từ 1/1 đến 19/5/2026 (VnExpress, số liệu HURC) và 20,5 triệu lượt năm 2025 — màn hình dùng số có nguồn.

## Giới hạn trung thực

- Logo: không có logo thật nào lên hình. HCMC Metro (Wikimedia trả 429 liên tục — không lách giới hạn) và Sở Xây dựng TP.HCM (trang chính thức trả 502, không có trên Wikimedia) → huy hiệu chữ M1, SXD.
- Hình học: đoạn Vành đai 3 phía Đông dò trên ảnh vệ tinh, đoạn gần Tân Vạn từ OpenStreetMap; phần vòng còn lại, tuyến metro mới và đường tới sân bay Long Thành là hướng tuyến gần đúng (ghi "minh hoạ" trên màn hình).
- Cột 3D số lượt khách metro: chiều cao tỉ lệ theo số lượt, không phải độ cao thật.
- Ảnh báo 1020–1280 px chỉ dùng trong cửa sổ ảnh (không phóng toàn khung). Ảnh phối cảnh One Era là ảnh của chủ đầu tư (qua The Leader).
- Mờ chuyển động làm sau render (cùng 30 fps), vì lọc trong trình duyệt làm render chậm ~7 lần.
```

## FILE: templates/ha-tang-flight/README.md

```markdown
# Hạ tầng quanh One Era (Vành đai 3 · QL13 · metro) — phong cách C v2

130,6 s, 10 chương, 37 keyframe, 0 cắt cứng; 9 cửa sổ ảnh báo; huy hiệu Material Symbols; 2 thẻ tổ chức dạng chữ (không tải được logo).
1. `python prep_geo4.py <scratch>` — thêm tuyến (VĐ3 phía Đông dò trên ảnh vệ tinh, đoạn gần Tân Vạn từ OSM, phần còn lại gần đúng), QL13 xong/chờ, metro.
2. `python mk_flight4.py` → proj/flight.json; `python flight.py proj/flight.json proj` → hết "!" (đọc bảng giữ khung + tài sản trong CAMLOG.md).
3. `python mk_sfx3.py proj/flight.json proj/sfx/events.json`; `make_music.py ../music.wav --dur 130.7 --bpm 92`; `mix_audio.py ... --music`.
4. `npx hyperframes check` → snapshot → render (≈ 35 phút, chậm nhất ở cảnh cận One Era nghiêng 3D) → `mb_post.py flight.json raw.mp4 mb.mp4` → mux `mix.wav` qua `alimiter=limit=0.80` (AAC làm vọt đỉnh).
```

## FILE: templates/ha-tang-flight/mk_flight4.py

```python
"""Kế hoạch bay — "99% vẫn chưa thông xe": hạ tầng quanh One Era (Vành đai 3, QL13, metro). Phong cách C v2."""
import json, math
M = lambda n: json.load(open(f"maps/{n}.json"))
SAT = []
for n, show in [("w03", None), ("a05", [3.6, 4.6]), ("sat07", [5.6, 6.4]), ("sat09", [8.3, 9.0]), ("sat11", [9.8, 10.6]), ("sat13", [11.8, 12.6]), ("sat16", [14.0, 14.8])]:
    m = M(n); SAT.append(dict(img=f"assets/maps/{n}_g.jpg", z=m["z"], x0=m["x0"], y0=m["y0"], w=m["w"], h=m["h"], show=show))
PTS = {"oneera": [106.6985, 10.9666], "site_n": [106.6995, 10.9702], "east_mid": [106.8406, 10.86], "east_s": [106.8296, 10.80], "tanvan": [106.8319, 10.9038],
       "nhontrach": [106.838, 10.765], "lt_air": [107.035, 10.765], "flow_mid": [106.90, 10.735],
       "tn_sec": [106.495, 10.665], "bd_sec": [106.742, 10.962], "hcm_sec": [106.845, 10.835], "dn_sec": [106.875, 10.735], "ring_w": [106.565, 10.84],
       "ntmk_j": [106.697223, 10.95951], "ql13_mid": [106.7105, 10.905], "ongbo": [106.7125, 10.8755], "todo_mid": [106.713, 10.85], "binhtrieu": [106.7125, 10.826],
       "ql13_lab": [106.705, 10.9515], "vd3_lab": [106.690, 10.9631],
       "a1": [106.665, 11.055], "st_tg": [106.716, 10.968], "st_ap": [106.752, 10.945], "st_da": [106.780, 10.910], "suoitien": [106.8140, 10.8790], "bdst_mid": [106.735, 10.958],
       "benthanh": [106.6983, 10.7712], "m1_mid": [106.7558, 10.8085], "bar25": [106.7480, 10.8160], "bar26": [106.7680, 10.8020],
       "hcm_lab": [106.72, 10.86], "map_note": [106.79, 10.97]}
cam = [
    # 1 · V10 hạ từ mây xuống đoạn phía Đông Vành đai 3
    [0.0, 11.3, 106.90, 7.2, 0, 0], [4.2, 10.86, 106.84, 10.6, 0, 0], [8.0, 10.85, 106.84, 11.85, 18, 0], [15.4, 10.85, 106.84, 11.85, 18, 0],
    # 2 · V2 kéo ra Đông Bắc TP.HCM: tuyến nào cũng đã vẽ xong
    [18.4, 10.88, 106.77, 10.55, 4, -3], [21.4, 10.90, 106.745, 10.3, 0, 0], [24.6, 10.90, 106.745, 10.3, 0, 0],
    # 3 · V1 bay tới One Era, nghiêng ngắn (≤ 4 s) khi tới
    [27.6, 10.948, 106.712, 12.35, 10, 0], [30.4, 10.9666, 106.6985, 14.55, 28, 0], [32.6, 10.9666, 106.6985, 14.9, 44, 5], [34.6, 10.9662, 106.6990, 14.6, 30, 6],
    # 4 · V5 toàn tuyến 76 km — tiến độ từng đoạn bằng vòng tròn tỉ lệ
    [37.2, 10.93, 106.70, 12.3, 12, 3], [40.2, 10.83, 106.69, 11.05, 0, 0], [50.0, 10.83, 106.69, 11.05, 0, 0],
    [53.4, 10.90, 106.822, 11.7, 14, 0], [57.4, 10.90, 106.822, 11.7, 14, 0],
    # 5 · V3 xe chạy Tân Vạn → cầu Nhơn Trạch → sân bay Long Thành (bám đầu tuyến)
    [59.6, 10.86, 106.838, 11.45, 18, 0], [62.2, 10.79, 106.85, 11.0, 14, 0], [64.6, 10.755, 106.95, 10.65, 8, 0], [66.4, 10.762, 106.99, 10.55, 4, 0],
    # 6 · V8 QL13: tô trạng thái hành lang (xong / chờ khởi công)
    [69.2, 10.935, 106.73, 11.6, 0, 0], [72.4, 10.92, 106.712, 12.35, 24, 0], [77.0, 10.92, 106.712, 12.35, 24, 0], [80.4, 10.86, 106.713, 12.35, 24, 0], [86.0, 10.86, 106.713, 12.35, 24, 0],
    # 7 · V9 metro TP mới Bình Dương – Suối Tiên: mốc thời gian trên bản đồ
    [89.4, 10.955, 106.745, 11.2, 10, 0], [98.6, 10.955, 106.745, 11.2, 10, 0], [101.0, 10.885, 106.80, 11.75, 14, 0], [104.2, 10.885, 106.80, 11.75, 14, 0],
    # 8 · V6 cột 3D số lượt khách metro số 1
    [106.6, 10.822, 106.758, 11.65, 26, 0], [112.6, 10.822, 106.758, 11.65, 26, 0],
    # 9 · V4 vòng "từng đợt" quanh One Era
    [115.6, 10.955, 106.708, 12.0, 6, 0], [120.0, 10.955, 106.708, 12.0, 6, 0],
    # 10 · V1 kết: zoom-through phối cảnh One Era → kéo ra thấy mọi lớp
    [123.0, 10.9666, 106.6985, 14.55, 0, 0], [125.3, 10.9666, 106.6985, 14.95, 0, 0], [129.3, 10.94, 106.73, 12.3, 16, 0], [130.6, 10.938, 106.732, 12.1, 20, 2],
]
L = lambda geo, kind, id, w=5, fill=False, ln=True, cls=None: {k: v for k, v in dict(geo=geo, kind=kind, id=id, w=w, fill=fill, len=ln, cls=cls).items() if v is not None}
layers = [L("prov:TPHCM_moi", "adm", "hcm", 5, True, False), L("prov:Đồng Nai", "adm", "dn", 3, True, False), L("prov:Tây Ninh", "adm", "tn", 3, True, False),
          L("lines:vd3_ring", "route", "ring", 6), L("lines:vd3_east", "route", "east", 7), L("lines:flow_lt", "route", "flow", 6), L("lines:ltdg", "route", "ltdg", 5),
          L("lines:ql13_done", "route", "q_done", 7), L("lines:ql13_todo", "route", "q_todo", 6, cls="dash"),
          L("prov:ql13_done_buf", "route", "qb_done", 3, True, False), L("prov:ql13_todo_buf", "yel", "qb_todo", 3, True, False),
          L("lines:metro_bdst", "route", "bdst", 6, cls="dash"), L("lines:metro1", "route", "m1", 6), L("lines:site", "proj", "site", 6, True, True)]
P = lambda p: 5200 * math.sqrt(p / 100)
circles = [{"id": "c_tn", "pt": "tn_sec", "r_m": P(95.6), "kind": "route"}, {"id": "c_hcm", "pt": "hcm_sec", "r_m": P(82.1), "kind": "route"},
           {"id": "c_dn", "pt": "dn_sec", "r_m": P(78.8), "kind": "route"}, {"id": "c_bd", "pt": "bd_sec", "r_m": P(71.7), "kind": "route"}]
rings = [{"id": "rg_wave", "pt": "oneera", "lat": 10.967, "t": 116.0, "km": [1.6, 3.2, 4.8], "out": 121.6}]
movers = [{"path": "flow", "t": 58.6, "d": 7.4, "icon": "car", "out": 67.5}, {"path": "bdst", "t": 90.6, "d": 8.6, "icon": "train", "out": 104.6}]
lab = []
def la(at, t, d, big=None, text="", small="", color="w", lx=0, ly=-260, align="c", xl=False, unit=None, count=None, icon=None, **kw):
    lab.append({k: v for k, v in dict(at=at, t=t, d=d, big=big, text=text, small=small, color=color, lx=lx, ly=ly, align=align, xl=xl, unit=unit, count=count, icon=icon, **kw).items() if v not in (None, "", False) or k == "logo"})
# 1 · V10
la("east_mid", 0.6, 7.0, "99", "17 km cầu cạn phía Đông", color="route", ly=-330, xl=True, unit="%", icon="construction", count={"from": 90, "to": 99})
la("east_mid", 4.2, 2.5, photo="assets/img/vd3_caucan.jpg", text="Ảnh: Dân trí", lx=-250, ly=-60, w=480, h=300, lead=False)
la("tanvan", 7.9, 3.6, "1%", "phần việc còn lại", color="yel", lx=-60, ly=-250, icon="hourglass_top")
la("nhontrach", 10.5, 2.6, "30/11", "mốc thông xe", color="yel", lx=-40, ly=-240, icon="calendar_month")
la("east_s", 13.3, 2.1, "THIẾU NHỰA · ĐÁ", "chất lượng cao", color="adm", lx=-60, ly=-220, icon="warning")
# 2 · V2
la("hcm_lab", 16.2, 3.4, "ĐÔNG BẮC TP.HCM", "", color="adm", lx=220, ly=-200, icon="location_city")
la("map_note", 19.5, 5.4, "TRÊN BẢN ĐỒ", "tuyến nào cũng đã vẽ xong", color="route", lx=0, ly=-150, icon="route")
la("hcm_lab", 20.6, 2.5, photo="assets/img/vd3_aerial.jpg", text="Ảnh: Thanh Niên", lx=-260, ly=-80, w=480, h=300, lead=False)
la("tanvan", 22.6, 2.4, "NGOÀI THỰC ĐỊA", "mỗi tuyến một vạch", color="adm", lx=-80, ly=180, icon="construction")
# 3 · V1
la("ql13_lab", 28.3, 6.0, "QL13", "", color="route", lx=-120, ly=-170, align="r", icon="add_road")
la("vd3_lab", 29.1, 2.3, "VÀNH ĐAI 3", "", color="route", lx=-20, ly=-320, align="c", icon="add_road")
la("site_n", 31.5, 3.0, "ĐI TỚI ĐÂU?", "bao giờ người dân dùng được", color="w", ly=-430, icon="help")
# 4 · V5
la("hcm_lab", 37.0, 2.5, photo="assets/img/vd3_tanvan2.jpg", text="Ảnh: Dân trí · Vành đai 3", lx=-230, ly=-260, w=480, h=300, lead=False)
la("hcm_lab", 35.6, 1.9, "76", "chiều dài toàn tuyến", color="route", lx=0, ly=-520, xl=True, unit="km", icon="route", count={"from": 0, "to": 76})
la("hcm_lab", 37.6, 2.1, "> 75.300", "tỷ đồng · tổng mức đầu tư", color="w", lx=0, ly=-520, xl=True, unit="tỷ", icon="payments")
la("hcm_lab", 39.8, 4.6, "81%", "giá trị hợp đồng (10/2026)", color="route", lx=0, ly=-520, xl=True, icon="construction")
la("tn_sec", 45.3, 6.4, "95,6%", "Tây Ninh", color="route", lx=80, ly=-160, align="l", icon="check_circle")
la("hcm_sec", 46.4, 5.3, "82,1%", "TP.HCM", color="route", lx=-60, ly=-210, align="r", icon="construction")
la("dn_sec", 46.9, 4.8, "78,8%", "Đồng Nai", color="route", lx=-60, ly=150, align="r", icon="construction")
la("bd_sec", 48.3, 4.0, "71,7%", "Bình Dương cũ · gần One Era", color="adm", lx=40, ly=-230, align="c", icon="hourglass_top")
la("tanvan", 53.4, 2.5, photo="assets/img/tanvan.jpg", text="Ảnh: SGGP", lx=-160, ly=-80, w=480, h=300, lead=False)
la("tanvan", 55.9, 1.7, "QUÝ I/2027", "một số hạng mục nút giao Tân Vạn", color="yel", lx=-60, ly=-250, icon="calendar_month")
# 5 · V3
la("nhontrach", 60.6, 1.9, "CẦU NHƠN TRẠCH", "sang Đồng Nai", color="route", lx=-60, ly=-200, icon="directions_car")
la("lt_air", 62.6, 4.4, "SÂN BAY LONG THÀNH", "≈ 39 km từ Tân Vạn (đo trên bản đồ)", color="route", lx=-120, ly=-230, icon="flight")
la("tanvan", 57.6, 2.6, "TÂN VẠN", "điểm xuất phát", color="route", lx=60, ly=-220, icon="directions_car")
la("ql13_lab", 66.6, 2.6, "QUỐC LỘ 13", "", color="route", lx=0, ly=-260, icon="add_road")
# 6 · V8
la("ql13_mid", 69.2, 2.3, "> 9 KM · 8 LÀN", "Ông Bố → Nguyễn Thị Minh Khai", color="route", lx=0, ly=-300, align="c", icon="swap_horiz")
la("ql13_mid", 72.4, 2.5, photo="assets/img/ql13.jpg", text="Ảnh: Dân trí", lx=-40, ly=-160, w=480, h=280, lead=False)
la("ql13_mid", 75.4, 4.6, "Sở Xây dựng TP.HCM", "dự án qua Bình Dương cũ cơ bản hoàn thành", logo="", mono="SXD", lx=0, ly=-120)
la("todo_mid", 80.9, 5.6, "≈ 6 KM", "phía cầu Bình Triệu · chờ khởi công", color="yel", lx=0, ly=-280, align="c", icon="hourglass_top")
# 7 · V9
la("st_tg", 87.9, 2.5, photo="assets/img/metro1_crowd.jpg", text="Ảnh: SGGP · khách chờ metro số 1", lx=0, ly=-60, w=480, h=300, lead=False)
la("a1", 90.0, 3.6, "CUỐI 2026", "dự kiến khởi công", color="yel", lx=40, ly=-220, icon="calendar_month")
la("bdst_mid", 93.8, 4.4, "≈ 30,7 km", "TP mới Bình Dương – Suối Tiên", color="route", lx=0, ly=-360, align="c", xl=True, icon="subway")
la("suoitien", 100.6, 2.5, photo="assets/img/metro1.jpg", text="Ảnh: SGGP · metro số 1", lx=-220, ly=-330, w=480, h=300, lead=False)
la("suoitien", 102.6, 2.0, "2030", "mục tiêu hoàn thành", color="yel", lx=-60, ly=-220, align="c", icon="calendar_month")
# 8 · V6
la("bar25", 104.6, 2.0, "20,5 triệu", "lượt khách năm 2025", color="w", lx=-40, ly=-400, align="c", icon="groups")
la("bar26", 108.6, 4.2, "8,86", "triệu lượt 1/1–19/5/2026", color="route", lx=60, ly=-300, align="c", xl=True, icon="groups", count={"from": 0, "to": 8.86, "dec": 2})
la("m1_mid", 106.7, 1.8, "Metro số 1", "Bến Thành – Suối Tiên", logo="", mono="M1", lx=0, ly=-640, lead=False)
# 9 · V4
la("oneera", 113.2, 2.3, "TỪNG ĐỢT", "", color="w", lx=0, ly=-640, icon="schedule")
la("oneera", 115.8, 2.5, photo="assets/img/ql13b.jpg", text="Ảnh: Dân trí · QL13", lx=0, ly=60, w=480, h=300, lead=False)
la("oneera", 115.6, 6.0, "QL13", "gần như xong", color="yel", lx=0, ly=-150, icon="check_circle")
la("oneera", 117.6, 4.0, "VÀNH ĐAI 3", "khép dần cuối 2026 – đầu 2027", color="yel", lx=0, ly=-320, icon="trending_up")
la("oneera", 120.3, 2.0, "METRO", "cuối thập kỷ", color="yel", lx=0, ly=-490, icon="subway")
# 10 · V1
la("site_n", 126.1, 4.4, "LĂN BÁNH NĂM NÀO?", "câu hỏi nên hỏi thêm", color="w", lx=70, ly=-300, icon="help")
pins = [{"at": "st_tg", "text": "Thuận Giao", "t": 96.3, "d": 4.0}, {"at": "st_ap", "text": "An Phú", "t": 97.2, "d": 3.1}, {"at": "st_da", "text": "Dĩ An", "t": 98.0, "d": 2.3},
        {"at": "suoitien", "text": "Suối Tiên", "t": 99.8, "d": 0.9, "left": True}, {"at": "binhtrieu", "text": "Cầu Bình Triệu", "t": 82.1, "d": 4.3},
        {"at": "ongbo", "text": "Ông Bố", "t": 70.0, "d": 2.3, "left": True}, {"at": "ntmk_j", "text": "Nguyễn Thị Minh Khai", "t": 70.4, "d": 1.9}]
ground = [{"at": "oneera", "text": "ONE ERA", "t": 30.6, "d": 3.8, "size": 100}, {"at": "oneera", "text": "ONE ERA", "t": 127.2, "d": 3.3, "size": 92}]
ev = []
E = lambda t, act, id, d=.6, **k: ev.append(dict(t=t, act=act, id=id, d=d, **k))
# 1
E(2.8, "draw", "east", 3.0)
# 2
E(15.8, "show", "hcm", .8, to=.9); E(16.0, "show", "hcm-fill", .8, to=.8); E(16.4, "show", "dn", .6, to=.4); E(16.4, "show", "tn", .6, to=.4)
E(19.4, "draw", "ring", 2.0); E(19.6, "dim", "east", .6, to=.55); E(19.8, "draw", "q_done", 1.2); E(20.2, "draw", "q_todo", 1.2); E(20.4, "draw", "bdst", 1.6); E(20.6, "draw", "m1", 1.4)
E(24.6, "dim", "hcm", .8, to=.25); E(24.6, "hide", "dn", .8); E(24.6, "hide", "tn", .8)
for i in ("ring", "q_done", "q_todo", "bdst", "m1"): E(25.4, "dim", i, .8, to=.4)
# 3
E(28.2, "draw", "site", 1.0); E(29.0, "show", "site-fill", .8, to=1)
E(34.8, "show", "ring", .6, to=1); E(34.8, "hide", "site", .8)
# 4
for i in ("q_done", "q_todo", "bdst", "m1"): E(35.0, "hide", i, .6)
E(44.8, "show", "c_tn", .5); E(45.9, "show", "c_hcm", .5); E(46.4, "show", "c_dn", .5); E(47.9, "show", "c_bd", .5)
for i in ("c_tn", "c_hcm", "c_dn", "c_bd"): E(53.0, "hide", i, .6)
E(53.2, "dim", "hcm", .6, to=0)
# 5
E(57.6, "dim", "ring", .6, to=.4); E(58.4, "draw", "flow", 7.2)
E(67.2, "hide", "flow", .6)
# 6
E(68.2, "show", "q_done", .1); E(68.2, "draw", "q_done", 1.6); E(69.0, "show", "qb_done", .1); E(69.0, "show", "qb_done-fill", .8, to=1)
E(79.6, "show", "q_todo", .1); E(79.6, "draw", "q_todo", 1.2); E(80.2, "show", "qb_todo", .1); E(80.2, "show", "qb_todo-fill", .8, to=1)
E(87.0, "hide", "qb_done", .6); E(87.0, "hide", "qb_todo", .6); E(87.2, "dim", "q_done", .6, to=.45); E(87.2, "dim", "q_todo", .6, to=.45)
# 7
E(90.4, "show", "bdst", .1); E(90.4, "draw", "bdst", 8.4); E(99.4, "show", "m1", .1); E(99.4, "draw", "m1", 1.6)
# 8
E(105.0, "grow", "m25", 1.6); E(106.8, "grow", "m26", 1.6)
E(113.0, "grow", "m25", .8, to=0, ease="power2.in"); E(113.0, "grow", "m26", .8, to=0, ease="power2.in")
# 10 — tích luỹ mọi lớp
E(121.8, "show", "site", .1); E(121.8, "draw", "site", .9); E(122.4, "show", "site-fill", .6, to=1)
for i in ("ring", "q_done", "q_todo", "bdst", "m1"): E(126.0, "show", i, .8, to=1)
E(126.2, "show", "hcm", .8, to=.5)
foot = [{"t": 122.9, "d": 2.6, "media": "assets/img/p7.jpg", "move": "push", "focus": "55% 50%", "blend": .6, "src": "phối cảnh One Era (CĐT, qua The Leader)"}]
legend = [{"t": 69.4, "d": 17.2, "top": 330, "items": [["route", "đã mở rộng 8 làn", "check_circle"], ["yel", "chờ khởi công", "hourglass_top"]]},
          {"t": 44.6, "d": 8.4, "top": 330, "items": [["route", "tiến độ từng đoạn (vòng tròn ∝ %)", "construction"]]}]
src = [{"t": 0.8, "d": 14.6, "text": "Nguồn: Dân trí (12/11/2026), Thanh Niên (13/11/2026) · Ảnh: Dân trí · ảnh vệ tinh Esri, Maxar"},
       {"t": 15.8, "d": 9.2, "text": "Ảnh: Thanh Niên · toàn tuyến vẽ theo hướng tuyến gần đúng (minh hoạ)"},
       {"t": 35.0, "d": 22.0, "text": "Nguồn: Dân trí (03/10/2026, báo cáo Chính phủ gửi Quốc hội), Thanh Niên (13/11/2026) · Ảnh: SGGP"},
       {"t": 57.6, "d": 9.0, "text": "Hướng tuyến và cự ly đo trên bản đồ, minh hoạ"},
       {"t": 67.4, "d": 19.6, "text": "Nguồn: CafeF (29/05/2026), Dân trí (13/02/2026) · Ảnh: Dân trí · Sở Xây dựng: huy hiệu chữ (không có logo chính thức tải được)"},
       {"t": 87.4, "d": 17.0, "text": "Nguồn: Tiền Phong (07/09/2026), CafeF/VTV (02/11/2026) · hướng tuyến minh hoạ · Ảnh: SGGP"},
       {"t": 104.8, "d": 8.4, "text": "Nguồn: VnExpress (số liệu HURC đến 19/5/2026), Nhân Dân (2025) · cột 3D tỉ lệ theo số lượt"},
       {"t": 122.6, "d": 7.8, "text": "Ảnh phối cảnh: chủ đầu tư One Era (qua The Leader)"}]
blocks = [{"lng": PTS["bar25"][0], "lat": PTS["bar25"][1], "w": 1500, "d": 1500, "ang": 0, "g": "m25"},
          {"lng": PTS["bar26"][0], "lat": PTS["bar26"][1], "w": 1500, "d": 1500, "ang": 0, "g": "m26"}]
chapters = [
    {"t": 0.0, "name": "99% của 17 km cầu cạn", "V": "V10", "cam": "hạ từ mây (Z 7,2 → 12,1), nghiêng 22°", "layers": "đoạn cầu cạn vẽ dần, thẻ 99%, 1%, 30/11, thiếu nhựa · đá, cửa sổ ảnh"},
    {"t": 15.6, "name": "Trên bản đồ vẽ xong", "V": "V2", "cam": "kéo ra Đông Bắc TP.HCM, về 0°", "layers": "TP.HCM sáng (cam), tỉnh lân cận mờ 40%, mọi tuyến vẽ mờ, cửa sổ ảnh"},
    {"t": 25.1, "name": "One Era giữa QL13 và Vành đai 3", "V": "V1", "cam": "fly-to, nghiêng 44° ≤ 4 s", "layers": "ranh One Era vẽ + phủ, nhãn QL13/VĐ3, câu hỏi"},
    {"t": 34.5, "name": "76 km · 75.300 tỷ · 81%", "V": "V5", "cam": "kéo ra toàn tuyến Z 9,8, lia chậm", "layers": "vòng VĐ3, thẻ 76 km / 75.300 tỷ / 81%, 4 vòng tròn tỉ lệ tiến độ, Tân Vạn"},
    {"t": 57.2, "name": "Tân Vạn → Nhơn Trạch → Long Thành", "V": "V3", "cam": "bám đầu tuyến xuống phía Nam rồi sang Đông", "layers": "tuyến có xe chạy, cầu Nhơn Trạch, sân bay Long Thành"},
    {"t": 66.3, "name": "QL13 đi trước một bước", "V": "V8", "cam": "lia dọc QL13 từ Bắc xuống Nam, nghiêng 24°", "layers": "hành lang tô theo trạng thái + chú giải, thẻ 8 làn, logo, 6 km chờ"},
    {"t": 86.7, "name": "Metro TP mới Bình Dương – Suối Tiên", "V": "V9", "cam": "lia theo hướng tuyến về Suối Tiên", "layers": "tuyến vẽ dần có tàu chạy, mốc cuối 2026 / 2030, ghim ga"},
    {"t": 104.4, "name": "Metro số 1: nhu cầu đã rõ", "V": "V6", "cam": "nghiêng 26 → 33°, quay 12°", "layers": "2 cột 3D theo số lượt, thẻ 8,86 triệu, thẻ tổ chức"},
    {"t": 112.8, "name": "Hạ tầng đến theo từng đợt", "V": "V4", "cam": "về One Era, đẩy nhẹ", "layers": "3 vòng: QL13 · VĐ3 · Metro"},
    {"t": 122.6, "name": "Lăn bánh năm nào?", "V": "V1", "cam": "zoom-through → kéo ra Z 11,85", "layers": "mọi lớp + ranh One Era phát sáng + câu hỏi"}]
assets = [
    {"name": "vd3_caucan.jpg", "url": "https://cdnphoto.dantri.com.vn/3m10PVuksY8HMjdIX7qYR8-OgF0=/thumb_w/1020/2026/11/12/vanhdai3baoquyen-1790704110265-1794486191605.jpg", "res": "1020×680", "used": "0:04.2–0:07.4", "note": "Dân trí 12/11/2026, ảnh Bảo Quyên; cửa sổ ảnh 560 px (không phóng to toàn khung)"},
    {"name": "vd3_aerial.jpg", "url": "https://images2.thanhnien.vn/528068263637045248/2026/8/24/edit-vanh-dai-3-di-qua-vinhome-17875581803371189682545.jpeg", "res": "2560×1707", "used": "0:20.6–0:23.5", "note": "Thanh Niên; watermark góc, không che chủ thể"},
    {"name": "tanvan.jpg", "url": "https://image.sggp.org.vn/w2000/Uploaded/2026/ycwkpcvo/2026_09_20/tvan7-2212-1980.jpg.webp", "res": "1280×642", "used": "0:53.5–0:56.4", "note": "SGGP 20/09/2026, ảnh Quốc Hùng"},
    {"name": "ql13.jpg", "url": "https://cdnphoto.dantri.com.vn/O8q_uoHwgKp-RvcLx_AaAVtsJFk=/thumb_w/1920/2026/02/13/morongquoclo13binhduongxuandoan-edited-1770988718424.jpg", "res": "1920×1280", "used": "1:11.6–1:14.5", "note": "Dân trí 13/02/2026; watermark góc"},
    {"name": "metro1_crowd.jpg", "url": "https://image.sggp.org.vn/w2000/Uploaded/2026/ycwkpcvo/2025_12_18/18metro2-7063-4055.jpg.webp", "res": "1280×960", "used": "1:27.9–1:30.9", "note": "SGGP, ảnh Quốc Hùng"},
    {"name": "metro1.jpg", "url": "https://image.sggp.org.vn/w2000/Uploaded/2026/ycwkpcvo/2025_12_18/18mtro-1280-5109.jpg.webp", "res": "1280×799", "used": "1:40.6–1:43.4", "note": "SGGP, ảnh Quốc Hùng"},
    {"name": "p7.jpg (One Era)", "url": "https://theleader.vn/kim-oanh-group-bat-tay-ong-lon-longfor-quy-hoach-khu-do-thi-one-era-d47799.html", "res": "1920×1143", "used": "2:02.9–2:05.5 (zoom-through)", "note": "phối cảnh CĐT, đã dùng ở video trước"},
    {"name": "Material Symbols Rounded (fill) 0.49.0", "url": "https://registry.npmjs.org/@material-symbols/svg-400", "res": "vector", "used": "mọi huy hiệu", "note": "một họ icon, Apache-2.0"},
    {"name": "HCMC Metro logo.svg", "url": "https://commons.wikimedia.org/wiki/File:HCMC_Metro_logo.svg", "res": "vector", "used": "—", "note": "KHÔNG tải được (upload.wikimedia.org trả 429 nhiều lần) → huy hiệu chữ M1"},
    {"name": "logo Sở Xây dựng TP.HCM", "url": "https://sxd.hochiminhcity.gov.vn/", "res": "—", "used": "—", "note": "trang chính thức không phản hồi (502), không có trên Wikimedia → huy hiệu chữ SXD"},
    {"name": "ảnh vệ tinh", "url": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer", "res": "z3–z16", "used": "toàn video", "note": "Esri, Maxar; làm mờ 0,8 px, tối 20%, giảm bão hoà 15%"},
    {"name": "hình học Vành đai 3 gần Tân Vạn", "url": "https://www.openstreetmap.org/relation/13490968", "res": "vector", "used": "0:00–1:07", "note": "OSM (ODbL); đoạn phía Đông dò trên ảnh vệ tinh; phần còn lại gần đúng"}]
out = {"duration": 130.6, "audio": "assets/mix.wav", "gsap": "assets/lib/gsap.min.js", "sat": SAT, "points": PTS, "blocks": blocks, "blockH": {"m25": 20.5 * 900, "m26": 8.86 * 900},
       "cam": cam, "layers": layers, "links": [], "circles": circles, "rings": rings, "movers": movers, "labels": lab, "pins": pins, "ground": ground, "ev": ev,
       "hud": {"clouds": [0.0, 3.0], "legend": legend, "src": src}, "foot": foot, "cuts": [], "allow_lock": True, "chapters": chapters, "assets": assets,
       "motion_blur": {"shutter": 180, "samples": 16}}
for a, b in zip(cam, cam[1:]): assert b[0] > a[0], (a[0], b[0])
json.dump(out, open("proj/flight.json", "w"), ensure_ascii=False, indent=1)
print(len(cam), "keys", len(lab), "labels", len(ev), "events")
```

## FILE: templates/ha-tang-flight/mk_sfx3.py

```python
"""SFX theo sự kiện của kế hoạch bay: whoosh khi camera di chuyển lớn, pop cho nhãn/ghim/số, swell trước lộ diện lớn."""
import json, sys
F = json.load(open(sys.argv[1])); ev = []
add = lambda t, s, db=0: ev.append({"t": round(max(0, t), 3), "sfx": s, "db": db})
K = F["cam"]
for a, b in zip(K, K[1:]):
    big = abs(b[3] - a[3]) > 0.9 or abs(b[2] - a[2]) > 1 or abs(b[4] - a[4]) > 12
    if big: add(a[0] + 0.1, "whoosh.wav", -3 if abs(b[3] - a[3]) > 2.5 else -7)
for l in F["labels"]: add(l["t"], "pop.wav", -1 if l.get("xl") else -4)
for p in F["pins"]: add(p["t"] + 0.25, "pop.wav", 0)
for g in F["ground"]: add(g["t"] - 0.9, "riser.wav", -7); add(g["t"] + 0.1, "impact.wav", -6)
for f in F["foot"]: add(f["t"] - 0.9, "riser.wav", -5); add(f["t"] + f["d"] - 0.3, "whoosh.wav", -6)
for r in F["rings"]:
    for i in range(len(r["km"])): add(r["t"] + i * .45, "pop.wav", -3)
for e in F["ev"]:
    if e["act"] == "grow" and e.get("to", 1) > 0.5: add(e["t"], "riser.wav", -8)
    if e["act"] == "draw" and e.get("d", .6) >= 1: add(e["t"], "whoosh.wav", -10)
    if e["act"] == "show" and e["id"].startswith(("c_", "h")) and e.get("to", 1) > .7: add(e["t"], "pop.wav", -6)
for m in F["movers"]: add(m["t"], "whoosh.wav", -9)
add(0.0, "whoosh.wav", 0)
ev.sort(key=lambda x: x["t"]); out = []
for x in ev:
    if out and any(o["sfx"] == x["sfx"] and x["t"] - o["t"] < .25 for o in out[-5:]): continue
    out.append(x)
json.dump(out, open(sys.argv[2], "w"), indent=0); print(len(out), "SFX")
```

## FILE: templates/ha-tang-flight/prep_geo4.py

```python
"""Hình học cho video hạ tầng Đông Bắc TP.HCM (toạ độ lng/lat).
Nguồn: (T) dò trên ảnh vệ tinh Esri z13; (O) OpenStreetMap relation 13490968 (ODbL); (L) đường cục bộ One Era đã dùng;
(A) điểm mốc gần đúng — chỉ dùng ở tỉ lệ vùng, ghi "hướng tuyến minh hoạ"."""
import json, math, sys
S = sys.argv[1]
g = json.load(open(f"{S}/p3/proj/geo.json"))
wx = lambda lng: (lng + 180) / 360 * 256 * 2 ** 8
wy = lambda lat: (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * 256 * 2 ** 8
P = lambda pts: "M" + " L".join(f"{wx(b):.2f} {wy(a):.2f}" for a, b in pts)   # pts: (lat,lng)
east = [(10.765, 106.838), (10.7807, 106.8286), (10.7908, 106.8293), (10.80, 106.8296), (10.81, 106.830), (10.8195, 106.830), (10.8254, 106.831),
        (10.8321, 106.8346), (10.8397, 106.8376), (10.85, 106.8402), (10.86, 106.8406), (10.875, 106.838), (10.89, 106.833), (10.9038, 106.8319)]   # (T)
bd = [(10.9038, 106.8319), (10.925, 106.80), (10.945, 106.77), (10.962, 106.742), (10.974, 106.72), (10.9789, 106.7003),
      (10.971359, 106.696579), (10.963143, 106.690464), (10.960616, 106.687567), (10.957456, 106.682739)]                                 # (A)+(L)
west = [(10.957456, 106.682739), (10.948, 106.655), (10.952, 106.62), (10.935, 106.592), (10.89, 106.575), (10.84, 106.565), (10.79, 106.555),
        (10.74, 106.535), (10.70, 106.51), (10.665, 106.495)]                                                                                    # (A)
south = [(10.765, 106.838), (10.745, 106.86), (10.725, 106.88)]                                                                                   # (A) Nhơn Trạch
g["lines"]["vd3_east"] = P(east)
g["lines"]["vd3_ring"] = P(list(reversed(south)) + east + bd[1:] + west[1:])
g["lines"]["vd3_bd"] = P(bd)
g["lines"]["vd3_tn"] = P([(10.70, 106.51), (10.665, 106.495)])
g["lines"]["ltdg"] = P([(10.7908, 106.8293), (10.789, 106.86), (10.785, 106.90), (10.78, 106.95), (10.775, 107.0), (10.765, 107.035)])            # (A) cao tốc → sân bay Long Thành
ql13_done = [(10.966777, 106.682739), (10.962827, 106.690464), (10.95951, 106.697223), (10.951452, 106.70527), (10.941213, 106.708488),
             (10.92, 106.7098), (10.90, 106.7105), (10.8755, 106.7125)]                                                                          # (L)+(T)
g["lines"]["ql13_done"] = P(ql13_done[2:])     # từ ngã ba Nguyễn Thị Minh Khai tới Ông Bố (~9 km)
g["lines"]["ql13_todo"] = P([(10.8755, 106.7125), (10.86, 106.713), (10.84, 106.713), (10.826, 106.7125)])                                     # (T) ~6 km tới cầu Bình Triệu
m1 = [(10.7712, 106.6983), (10.7815, 106.7075), (10.7955, 106.7155), (10.7985, 106.7230), (10.8016, 106.7339), (10.8028, 106.7425),
      (10.8085, 106.7558), (10.8213, 106.7585), (10.8325, 106.7639), (10.8463, 106.7716), (10.8592, 106.7889), (10.8664, 106.8012), (10.8790, 106.8140)]   # (A) metro số 1
g["lines"]["metro1"] = P(m1)
bdst = [(11.055, 106.665), (11.03, 106.68), (11.005, 106.70), (10.985, 106.715), (10.976, 106.712), (10.968, 106.716), (10.958, 106.735),
        (10.945, 106.752), (10.930, 106.770), (10.910, 106.780), (10.895, 106.795), (10.882, 106.808), (10.8790, 106.8140)]                       # (A) theo mô tả Tiền Phong 07/09/2026
g["lines"]["metro_bdst"] = P(bdst)
km = lambda pts: sum(math.hypot((b[0]-a[0])*110.57, (b[1]-a[1])*111.32*math.cos(math.radians(a[0]))) for a, b in zip(pts, pts[1:]))
print("east %.1f km | ql13_done %.1f | ql13_todo %.1f | metro1 %.1f | bdst %.1f | ring %.1f" % (km(east), km(ql13_done[2:]), km([(10.8755,106.7125),(10.826,106.7125)]), km(m1), km(bdst), km(list(reversed(south)) + east + bd[1:] + west[1:])))
json.dump(g, open(f"{S}/p4/proj/geo.json", "w"))
```

## FILE: templates/kinh-te-dia-phuong/TEMPLATE.md

```markdown
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
```

## FILE: templates/kinh-te-dia-phuong/build.py

```python
#!/usr/bin/env python3
"""Ghép GEO + mapjs + mapcss vào các scene trong src/ -> compositions/."""
import json, os, glob
D = os.path.dirname(os.path.abspath(__file__))
FOOT = json.load(open(f"{D}/footage.json"))
geo = open(f"{D}/geo.json").read(); mapjs = open(f"{D}/mapjs.js").read(); mapcss = open(f"{D}/mapcss.css").read(); design = open(f"{D}/fonts.css").read() + open(f"{D}/design.css").read()
os.makedirs(f"{D}/compositions", exist_ok=True)
for f in glob.glob(f"{D}/src/*.html"):
    s = open(f, encoding="utf-8").read()
    s = s.replace("/*GEOJSON*/", "const GEO = " + geo + ";").replace("/*MAPJS*/", mapjs).replace("/*MAPCSS*/", mapcss).replace("/*DESIGN*/", design)
    s = s.replace('<div id="g-whip">', '<div id="g-whip"><div class="mapbg"></div>')
    for k, v in FOOT.items(): s = s.replace("/*" + k + "*/", str(v))
    open(f"{D}/compositions/" + os.path.basename(f), "w", encoding="utf-8").write(s)
    print("built", os.path.basename(f))
```

## FILE: templates/kinh-te-dia-phuong/design.css

```css
    /* ===== HỆ THIẾT KẾ: báo chí kinh tế, tối giản (1 phông, 1 màu nhấn) =====
       VÙNG AN TOÀN TIKTOK (1080×1920): không đặt chữ/nhãn ở y < 210 (thanh trên), y > 1440 (tên kênh, caption, nhạc),
       x > 940 khi 700 < y < 1440 (cột nút tim/bình luận/chia sẻ). Độ rõ: chữ ≥ 72% trắng, nét vẽ ≥ 2 px. */
    #root { --navy0: #0E1A2B; --navy1: #13243A; --accent: #F28C28; --ink: #FFFFFF; --ink75: rgba(255,255,255,0.88); --ink45: rgba(255,255,255,0.72); --neutral: #8A97A8;
      font-family: 'Be Vietnam Pro', sans-serif; color: var(--ink); background: var(--navy0); }
    /* nhãn phân đoạn trên cùng: kính mờ */
    .seg { position: absolute; left: 0; right: 0; top: 230px; text-align: center; }
    .seg > span { display: inline-block; padding: 12px 28px 13px; font-size: 24px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase;
      color: var(--ink); background: rgba(255,255,255,0.10); border: 1.5px solid rgba(255,255,255,0.20); border-radius: 999px; backdrop-filter: blur(10px); }
    /* dòng neo: tiêu đề lớn duy nhất của khung */
    .anchor { position: absolute; left: 70px; right: 150px; text-align: center; font-size: 68px; font-weight: 800; line-height: 1.08; letter-spacing: 0.01em;
      text-transform: uppercase; text-shadow: 0 2px 4px rgba(5,10,20,0.55), 0 6px 30px rgba(5,10,20,0.8); }
    .anchor .ln { display: block; white-space: nowrap; }
    .anchor .w { display: inline-block; }
    .anchor em { font-style: normal; color: var(--accent); }
    .anchor.low { bottom: 520px; } .anchor.mid { top: 760px; }
    /* Kiểu A: nhãn gắn vật thể — chấm 10px + đường dẫn 2px + chữ, không hộp */
    .la { position: absolute; left: 0; top: 0; width: 0; height: 0; }
    .la .dot { position: absolute; left: -5px; top: -5px; width: 10px; height: 10px; border-radius: 50%; background: var(--ink); box-shadow: 0 0 0 3px rgba(14,26,43,0.6); }
    .la .lead { position: absolute; left: 0; top: -1.5px; height: 3px; background: var(--ink); transform-origin: 0 50%; }
    .la .tx { position: absolute; white-space: nowrap; font-size: 32px; font-weight: 600; line-height: 1.1; text-shadow: 0 0 12px rgba(0,0,0,0.7), 0 2px 4px rgba(0,0,0,0.75); }
    .la .tx small { display: block; margin-top: 4px; font-size: 28px; font-weight: 500; color: var(--ink75); }
    .la.acc .dot { background: var(--accent); }
    /* Kiểu B: thẻ khái niệm */
    .lb { position: absolute; left: 0; top: 0; width: 0; height: 0; }
    .lb > span { position: absolute; transform: translate(-50%, -50%); white-space: nowrap; padding: 9px 16px 10px; font-size: 28px; font-weight: 600; letter-spacing: 0.02em;
      text-transform: uppercase; color: var(--ink); background: rgba(14,26,43,0.70); border: 2px solid var(--accent); border-radius: 8px; }
    /* chân trang nguồn */
    .foot { position: absolute; left: 70px; right: 150px; top: 300px; text-align: center; font-size: 20px; font-weight: 500; line-height: 1.4; color: var(--ink45); text-shadow: 0 1px 6px rgba(0,0,0,0.6); }
    /* gradient navy cho ảnh/video: trên 18%, dưới 22% */
    .gtop { position: absolute; left: 0; right: 0; top: 0; height: 420px; background: linear-gradient(180deg, rgba(14,26,43,0.85), rgba(14,26,43,0)); }
    .gbot { position: absolute; left: 0; right: 0; bottom: 0; height: 900px; background: linear-gradient(0deg, rgba(14,26,43,0.85) 0%, rgba(14,26,43,0.75) 45%, rgba(14,26,43,0) 100%); }
    .up { color: var(--accent); font-weight: 600; }
```

## FILE: templates/kinh-te-dia-phuong/fonts.css

```css
    @font-face { font-family: 'Be Vietnam Pro'; font-style: normal; font-weight: 400; font-display: block; src: url('assets/fonts/be-vietnam-pro-vietnamese-400-normal.woff2') format('woff2'); unicode-range: U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,U+01AF-01B0,U+0300-0301,U+0303-0304,U+0308-0309,U+0323,U+0329,U+1EA0-1EF9,U+20AB; }
    @font-face { font-family: 'Be Vietnam Pro'; font-style: normal; font-weight: 400; font-display: block; src: url('assets/fonts/be-vietnam-pro-latin-ext-400-normal.woff2') format('woff2'); unicode-range: U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF; }
    @font-face { font-family: 'Be Vietnam Pro'; font-style: normal; font-weight: 400; font-display: block; src: url('assets/fonts/be-vietnam-pro-latin-400-normal.woff2') format('woff2'); unicode-range: U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD; }
    @font-face { font-family: 'Be Vietnam Pro'; font-style: normal; font-weight: 500; font-display: block; src: url('assets/fonts/be-vietnam-pro-vietnamese-500-normal.woff2') format('woff2'); unicode-range: U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,U+01AF-01B0,U+0300-0301,U+0303-0304,U+0308-0309,U+0323,U+0329,U+1EA0-1EF9,U+20AB; }
    @font-face { font-family: 'Be Vietnam Pro'; font-style: normal; font-weight: 500; font-display: block; src: url('assets/fonts/be-vietnam-pro-latin-ext-500-normal.woff2') format('woff2'); unicode-range: U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF; }
    @font-face { font-family: 'Be Vietnam Pro'; font-style: normal; font-weight: 500; font-display: block; src: url('assets/fonts/be-vietnam-pro-latin-500-normal.woff2') format('woff2'); unicode-range: U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD; }
    @font-face { font-family: 'Be Vietnam Pro'; font-style: normal; font-weight: 600; font-display: block; src: url('assets/fonts/be-vietnam-pro-vietnamese-600-normal.woff2') format('woff2'); unicode-range: U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,U+01AF-01B0,U+0300-0301,U+0303-0304,U+0308-0309,U+0323,U+0329,U+1EA0-1EF9,U+20AB; }
    @font-face { font-family: 'Be Vietnam Pro'; font-style: normal; font-weight: 600; font-display: block; src: url('assets/fonts/be-vietnam-pro-latin-ext-600-normal.woff2') format('woff2'); unicode-range: U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF; }
    @font-face { font-family: 'Be Vietnam Pro'; font-style: normal; font-weight: 600; font-display: block; src: url('assets/fonts/be-vietnam-pro-latin-600-normal.woff2') format('woff2'); unicode-range: U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD; }
    @font-face { font-family: 'Be Vietnam Pro'; font-style: normal; font-weight: 800; font-display: block; src: url('assets/fonts/be-vietnam-pro-vietnamese-800-normal.woff2') format('woff2'); unicode-range: U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,U+01AF-01B0,U+0300-0301,U+0303-0304,U+0308-0309,U+0323,U+0329,U+1EA0-1EF9,U+20AB; }
    @font-face { font-family: 'Be Vietnam Pro'; font-style: normal; font-weight: 800; font-display: block; src: url('assets/fonts/be-vietnam-pro-latin-ext-800-normal.woff2') format('woff2'); unicode-range: U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF; }
    @font-face { font-family: 'Be Vietnam Pro'; font-style: normal; font-weight: 800; font-display: block; src: url('assets/fonts/be-vietnam-pro-latin-800-normal.woff2') format('woff2'); unicode-range: U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD; }
```

## FILE: templates/kinh-te-dia-phuong/footage.json

```json
{
 "F1SRC": "assets/foot/f1.mp4",
 "F1MS": 0,
 "F1LOC": "Đồng bằng sông Cửu Long",
 "F2SRC": "assets/foot/f2.mp4",
 "F2MS": 0,
 "F2LOC": "Chợ nổi miền Tây",
 "FSRC": "Video: Le Monde en Vidéo · CC BY 3.0 (Wikimedia Commons)",
 "E1SRC": "assets/foot/e1.mp4",
 "E1MS": 0,
 "E2SRC": "assets/foot/e2.mp4",
 "E2MS": 0,
 "ESRC": "Video: Le Monde en Vidéo · CC BY 3.0 (Wikimedia Commons)"
}
```

## FILE: templates/kinh-te-dia-phuong/geo_config.json

```json
{
 "country": "VNM",
 "merge": {
  "Vĩnh Long": [
   "Vĩnh Long",
   "Bến Tre",
   "Trà Vinh"
  ],
  "Cần Thơ": [
   "Can Tho",
   "Sóc Trăng",
   "Hau Giang"
  ],
  "TP.HCM": [
   "Hồ Chí Minh city",
   "Bình Dương",
   "Bà Rịa - Vũng Tàu"
  ],
  "Đồng Tháp": [
   "Ðong Tháp",
   "Tiền Giang"
  ],
  "An Giang": [
   "An Giang",
   "Kiên Giang"
  ],
  "Cà Mau": [
   "Cà Mau",
   "Bạc Liêu"
  ],
  "Tây Ninh": [
   "Tây Ninh",
   "Long An"
  ]
 },
 "focus": "Vĩnh Long",
 "compare": [
  "TP.HCM",
  "Cần Thơ"
 ],
 "region": [
  "Vĩnh Long",
  "Cần Thơ",
  "An Giang",
  "Đồng Tháp",
  "Cà Mau"
 ],
 "points": {
  "pt_hcm": [
   106.7009,
   10.7769
  ],
  "pt_ct": [
   105.7469,
   10.0452
  ],
  "pt_vl": [
   105.9722,
   10.2537
  ],
  "region": [
   105.55,
   9.85
  ]
 },
 "label_points": {
  "rv_tien": [
   106.33,
   10.335
  ],
  "rv_hau": [
   105.6,
   10.25
  ]
 },
 "rivers": {
  "tien": {
   "ne_name": "Mekong",
   "ne_end": [
    106.118663,
    10.237576
   ],
   "cut_at": [
    105.9105,
    10.2764
   ],
   "trace_to": [
    106.78,
    10.215
   ]
  },
  "hau": {
   "ne_name": "Mekong",
   "ne_end": [
    105.837983,
    10.004991
   ],
   "trace_from": [
    105.838,
    10.005
   ],
   "trace_to": [
    106.36,
    9.57
   ]
  }
 },
 "coast_axis": [
  [
   106.8,
   10.24
  ],
  [
   106.33,
   9.56
  ]
 ],
 "satellite": {
  "z": 10,
  "bbox": [
   104.4,
   8.6,
   107.8,
   12.0
  ]
 }
}
```

## FILE: templates/kinh-te-dia-phuong/index.html

```html
<!doctype html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #0E1A2B; }
      #ground { position: absolute; inset: 0; background: #0E1A2B; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="88.6" data-width="1080" data-height="1920">
      <div id="ground"></div>
      <!--HOSTS-->
      <div id="geo" data-composition-id="geo" data-composition-src="compositions/geo.html" data-start="0" data-duration="28.4" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="foot" data-composition-id="foot" data-composition-src="compositions/foot.html" data-start="28" data-duration="9.3" data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="board" data-composition-id="board" data-composition-src="compositions/board.html" data-start="37.3" data-duration="29.44" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="doc" data-composition-id="doc" data-composition-src="compositions/doc.html" data-start="66.74" data-duration="7.56" data-track-index="4" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="earthb" data-composition-id="earthb" data-composition-src="compositions/earthb.html" data-start="74.3" data-duration="4" data-track-index="5" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="end" data-composition-id="end" data-composition-src="compositions/end.html" data-start="78.3" data-duration="10.3" data-track-index="6" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <audio id="mix" class="clip" src="assets/mix.wav" data-start="0" data-duration="88.6" data-track-index="20" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
```

## FILE: templates/kinh-te-dia-phuong/mapcss.css

```css
    .mapbg { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 42%, #13243A 0%, #0E1A2B 100%); }
    .map { position: absolute; left: 0; top: 0; }
    .map .vn { fill: #172A42; stroke: #5A7194; }
    .map .prov { fill: none; stroke: #4F6688; }
    .map .region { fill: #8A97A8; fill-opacity: 0.18; stroke: #B3BECB; opacity: 0; }
    .map .cmp { fill: #8A97A8; fill-opacity: 0.45; stroke: #B7C1CD; opacity: 0; }
    .map .vl { fill: #F28C28; fill-opacity: 0.8; stroke: #F8B677; opacity: 0; }
    .map .vl-glow { fill: none; stroke: #F28C28; opacity: 0; filter: blur(7px); }
    .map .rv-glow { fill: none; stroke: #33A3A8; opacity: 0.85; filter: blur(5px); stroke-linecap: round; stroke-dasharray: 100 120; stroke-dashoffset: 110; }
    .map .rv { fill: none; stroke: #B5DEDB; stroke-linecap: round; stroke-dasharray: 100 120; stroke-dashoffset: 110; }
    .map .coast-glow { fill: none; stroke: #F28C28; opacity: 0.9; filter: blur(6px); stroke-linecap: round; stroke-dasharray: 100 120; stroke-dashoffset: 110; }
    .map .coast { fill: none; stroke: #FFFFFF; stroke-linecap: round; stroke-dasharray: 100 120; stroke-dashoffset: 110; }
    .map .center { fill: #8A97A8; fill-opacity: 0.2; stroke: #B3BECB; opacity: 0; }
    .map .corr { fill: none; stroke: #B3BECB; stroke-linecap: round; stroke-dasharray: 100 120; stroke-dashoffset: 110; }
    .map .con { fill: none; stroke: #B3BECB; stroke-linecap: round; stroke-dasharray: 100 120; stroke-dashoffset: 110; }
    .map .ring { fill: none; stroke: #F28C28; opacity: 0; }
    .mapdots { position: absolute; inset: 0; pointer-events: none; background: radial-gradient(circle at 2px 2px, rgba(170,195,230,0.12) 1.1px, transparent 1.6px) 0 0 / 7px 7px; }
```

## FILE: templates/kinh-te-dia-phuong/mapjs.js

```javascript
// ===== Bản đồ vector (Web Mercator, toạ độ thế giới ở mức Z=8) — dùng chung cho các cảnh =====
// GEO = { prov:{tên:d}, region:d, tien:d, hau:d, coast:d, lab:{key:[x,y]} } được nhúng sẵn phía trên.
function makeMap(opts) {
  const W = 1080, H = 1920, Z0 = GEO.Z;
  const NS = "http://www.w3.org/2000/svg";
  const svg = document.querySelector(opts.svg), world = svg.querySelector(".world");
  const el = (tag, attrs, parent = world) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); parent.appendChild(e); return e; };
  const stroked = []; // [el, screenWidthPx]
  const S = (e, w) => { stroked.push([e, w]); return e; };
  // lớp vẽ
  S(el("path", { d: GEO.prov._vn, class: "vn" }), 2);
  for (const k in GEO.prov) if (!k.startsWith("_")) S(el("path", { d: GEO.prov[k], class: "prov", "data-name": k }), 2);
  const region = S(el("path", { d: GEO.region, class: "region", id: opts.id + "-region" }), 3);
  const fill = {};
  for (const k of ["TP.HCM", "Cần Thơ"]) fill[k] = S(el("path", { d: GEO.prov[k], class: "cmp", id: opts.id + "-" + (k === "TP.HCM" ? "hcm" : "ct") }), 2);
  const vlGlow = S(el("path", { d: GEO.prov["Vĩnh Long"], class: "vl-glow", id: opts.id + "-vlglow" }), 14);
  const vl = S(el("path", { d: GEO.prov["Vĩnh Long"], class: "vl", id: opts.id + "-vl" }), 3);
  const rv = {};
  for (const k of ["tien", "hau"]) {
    rv[k + "g"] = S(el("path", { d: GEO[k], class: "rv-glow", pathLength: 100, id: opts.id + "-" + k + "g" }), 14);
    rv[k] = S(el("path", { d: GEO[k], class: "rv", pathLength: 100, id: opts.id + "-" + k }), 4);
  }
  const coastG = S(el("path", { d: GEO.coast, class: "coast-glow", pathLength: 100, id: opts.id + "-coastg" }), 18);
  const coast = S(el("path", { d: GEO.coast, class: "coast", pathLength: 100, id: opts.id + "-coast" }), 5);
  const L = GEO.lab;
  const center = el("circle", { cx: L.pt_ct[0] + 6, cy: L.pt_ct[1] + 14, r: 46, class: "center", id: opts.id + "-center" });
  S(center, 3);
  const q = (a, b, bend) => { const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, dx = b[0] - a[0], dy = b[1] - a[1];
    return `M${a[0]} ${a[1]} Q ${mx - dy * bend} ${my + dx * bend}, ${b[0]} ${b[1]}`; };
  const corridor = S(el("path", { d: q(L.pt_hcm, L.pt_vl, 0.18) + " " + q(L.pt_vl, L.pt_ct, 0.12).replace("M", "L").replace(/^L[^Q]+/, ""), class: "corr", pathLength: 100, id: opts.id + "-corr" }), 6);
  corridor.setAttribute("d", q(L.pt_hcm, L.pt_vl, 0.18) + " " + q(L.pt_vl, L.pt_ct, 0.12).replace(/^M[^Q]+/, ""));
  const conE = S(el("path", { d: q(L.pt_vl, L.coast, -0.25), class: "con", pathLength: 100, id: opts.id + "-cone" }), 5);
  const conC = S(el("path", { d: q(L.pt_vl, [L.pt_ct[0] + 6, L.pt_ct[1] + 14], 0.3), class: "con", pathLength: 100, id: opts.id + "-conc" }), 5);
  const rings = [0, 1, 2].map((i) => el("circle", { cx: L["Vĩnh Long"][0], cy: L["Vĩnh Long"][1] - 20, r: 1, class: "ring", id: opts.id + "-ring" + i }));
  rings.forEach((r) => S(r, 4));
  // nhãn HTML gắn toạ độ
  const labels = [...document.querySelectorAll(opts.labels)].map((n) => ({ n, p: L[n.dataset.at], dx: +(n.dataset.dx || 0), dy: +(n.dataset.dy || 0) }));
  // Kiểu A: chấm tại vật thể, đường dẫn tới (lx,ly), chữ canh theo hướng đường dẫn
  document.querySelectorAll(opts.labels + ".la").forEach((n) => {
    const lx = +(n.dataset.lx || 0), ly = +(n.dataset.ly || 0), al = n.dataset.align || (lx >= 0 ? "l" : "r");
    const lead = n.querySelector(".lead"), tx = n.querySelector(".tx");
    if (lead) { lead.style.width = Math.hypot(lx, ly) + "px"; lead.style.transform = `rotate(${Math.atan2(ly, lx)}rad)`; }
    if (tx) { const gx = al === "l" ? 10 : al === "r" ? -10 : 0, gy = al === "c" ? (ly >= 0 ? 12 : -12) : 0;
      tx.style.left = (lx + gx) + "px"; tx.style.top = (ly + gy) + "px";
      tx.style.transform = al === "l" ? "translate(0,-50%)" : al === "r" ? "translate(-100%,-50%)" : (ly >= 0 ? "translate(-50%,0)" : "translate(-50%,-100%)");
      tx.style.textAlign = al === "r" ? "right" : al === "c" ? "center" : "left"; }
  });
  const ringR = { r0: 0, r1: 0, r2: 0 };

  // camera: (lat,lng,Z) -> Hermite đơn điệu trên x,y,Z => vận tốc liên tục
  const mx = (lng) => ((lng + 180) / 360) * 256 * 2 ** Z0;
  const my = (lat) => { const r = (lat * Math.PI) / 180; return ((1 - Math.log(Math.tan(r) + 1 / Math.cos(r)) / Math.PI) / 2) * 256 * 2 ** Z0; };
  const KEYS = opts.keys.map(([t, lat, lng, Z, carry]) => ({ t, x: mx(lng), y: my(lat), Z, carry }));
  const TS = KEYS.map((k) => k.t);
  const slopes = (vs) => { const n = vs.length, dl = [], m = new Array(n).fill(0);
    for (let k = 0; k < n - 1; k++) dl[k] = (vs[k + 1] - vs[k]) / (TS[k + 1] - TS[k]);
    m[0] = opts.startMoving === false ? 0 : dl[0]; m[n - 1] = KEYS[n - 1].carry ? dl[n - 2] : 0;
    for (let k = 1; k < n - 1; k++) m[k] = dl[k - 1] * dl[k] <= 0 ? 0 : (dl[k - 1] + dl[k]) / 2;
    for (let k = 0; k < n - 1; k++) { if (dl[k] === 0) { m[k] = 0; m[k + 1] = 0; continue; }
      const a = m[k] / dl[k], b = m[k + 1] / dl[k], s = a * a + b * b;
      if (s > 9) { const tau = 3 / Math.sqrt(s); m[k] = tau * a * dl[k]; m[k + 1] = tau * b * dl[k]; } }
    return m; };
  const C = {}; ["x", "y", "Z"].forEach((c) => { const vs = KEYS.map((k) => k[c]); C[c] = { vs, m: slopes(vs) }; });
  const sample = (t) => { t = Math.min(Math.max(t, TS[0]), TS[TS.length - 1]); let i = 0; while (i < TS.length - 2 && t > TS[i + 1]) i++;
    const h = TS[i + 1] - TS[i], s = (t - TS[i]) / h, s2 = s * s, s3 = s2 * s, o = {};
    ["x", "y", "Z"].forEach((c) => { const { vs, m } = C[c];
      o[c] = (2 * s3 - 3 * s2 + 1) * vs[i] + (s3 - 2 * s2 + s) * h * m[i] + (-2 * s3 + 3 * s2) * vs[i + 1] + (s3 - s2) * h * m[i + 1]; });
    return o; };
  function apply(t) {
    const c = sample(t), s = 2 ** (c.Z - Z0), tx = W / 2 - c.x * s, ty = H / 2 - c.y * s;
    world.setAttribute("transform", `translate(${tx.toFixed(2)} ${ty.toFixed(2)}) scale(${s.toFixed(5)})`);
    stroked.forEach(([e, w]) => e.setAttribute("stroke-width", (w / s).toFixed(4)));
    (opts.rings || []).forEach(([t0, dur, rmax], i) => { const r = rings[i]; if (!r) return;
      const p = (t - t0) / dur;
      if (p < 0 || p > 1) { r.style.opacity = "0"; return; }
      const rr = 10 + (rmax - 10) * (1 - (1 - p) ** 2);
      r.setAttribute("r", (rr / s).toFixed(3)); r.style.opacity = (0.95 * (1 - p)).toFixed(3); });
    labels.forEach(({ n, p, dx, dy }) => { n.style.transform = `translate(${(p[0] * s + tx + dx).toFixed(1)}px, ${(p[1] * s + ty + dy).toFixed(1)}px)`; });
  }
  return { apply, ringR, sample };
}
```

## FILE: templates/kinh-te-dia-phuong/rows.py

```python
T0 = 37.3; END = 66.74
ICON = {
 "bld": '<path d="M4 21V5l8-3 8 3v16M9 21v-4h6v4M8 8h.01M12 8h.01M16 8h.01M8 12h.01M12 12h.01M16 12h.01"/>',
 "money": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/>',
 "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.5 12h11l2-8H6.2"/>',
 "ship": '<path d="M3 17l2 4h14l2-4M5 17V11h14v6M9 11V6h6v5M12 3v3"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
 "crane": '<path d="M4 21h8M6 21V4h2M8 4h12l-3 4M8 8h9M14 8v5M13 13h2v2h-2z"/>',
}
# (icon, số, số lẻ, đơn vị, mô tả, tăng trưởng, lúc hiện = lúc đọc số, lúc hiện tăng trưởng)
ROWS = [
 ("bld", 2076, 0, "doanh nghiệp", "thành lập mới", "vượt 9,26% kế hoạch năm", 37.86, 40.8),
 ("money", 8308, 0, "tỷ đồng", "vốn đăng ký mới", None, 43.34, None),
 ("cart", 134414, 0, "tỷ đồng", "bán lẻ hàng hoá &amp; dịch vụ", "+19,34%", 48.2, 51.3),
 ("ship", 1.37, 2, "tỷ USD", "xuất siêu", None, 53.62, None),
 ("globe", 183, 0, "dự án FDI", "còn hiệu lực", "vốn 5,93 tỷ USD", 56.42, 58.4),
 ("crane", 772, 0, "dự án trong nước", "còn hiệu lực", "vốn hơn 264.000 tỷ đồng", 60.16, 62.6),
]
def build():
    html, js = [], []
    for i, (ic, num, dec, unit, desc, up, t_in, t_up) in enumerate(ROWS, 1):
        a = round(t_in - T0 - 0.05, 2); dur = round(END - T0 - a, 2)
        upx = f' <span class="up" id="r{i}-up">▲ {up}</span>' if up else ""
        start = round(num * 0.4, dec)
        html.append(f'''      <div class="row clip" id="r{i}" data-start="{a}" data-duration="{dur}" data-track-index="3"><div class="rin">
        <svg class="ic" viewBox="0 0 24 24">{ICON[ic]}</svg>
        <div class="txt"><div class="l1"><span class="n" id="r{i}-n">{start}</span><span class="u">{unit}</span></div><div class="l2">{desc}{upx}</div></div>
      </div></div>''')
        js.append(f'''      tl.fromTo("#r{i} .rin", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }}, {a});
      (() => {{ const el = document.querySelector("#r{i}-n"), o = {{ v: {start} }}; el.textContent = fmt({start}, {dec});
        tl.fromTo(o, {{ v: {start} }}, {{ v: {num}, duration: 0.8, ease: "power2.out", onUpdate: () => {{ el.textContent = fmt(o.v, {dec}); }} }}, {a}); }})();''')
        if up:
            js.append(f'      tl.fromTo("#r{i}-up", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power2.out" }}, {round(t_up - T0, 2)});')
    return "\n".join(html), "\n".join(js)

if __name__ == "__main__":
    # python rows.py  -> sinh src/board.html từ tpl/board.tpl.html
    import os
    D = os.path.dirname(os.path.abspath(__file__))
    h, j = build()
    s = open(f"{D}/tpl/board.tpl.html", encoding="utf-8").read().replace("<!--ROWS-->", h).replace("/*ROWJS*/", j)
    open(f"{D}/src/board.html", "w", encoding="utf-8").write(s)
    print("src/board.html:", len(ROWS), "dòng số liệu")
```

## FILE: templates/kinh-te-dia-phuong/sfx_events.json

```json
[
 {
  "t": 0.82,
  "sfx": "sfx/whoosh.wav",
  "db": -6
 },
 {
  "t": 2.22,
  "sfx": "sfx/whoosh.wav",
  "db": -6
 },
 {
  "t": 2.8,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 5.52,
  "sfx": "sfx/whoosh.wav",
  "db": -6
 },
 {
  "t": 5.7,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 7.7,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 9.7,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 10.92,
  "sfx": "sfx/whoosh.wav",
  "db": -6
 },
 {
  "t": 13.52,
  "sfx": "sfx/whoosh.wav",
  "db": -6
 },
 {
  "t": 15.7,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 17.9,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 21.0,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 21.55,
  "sfx": "sfx/riser.wav",
  "db": 0
 },
 {
  "t": 22.2,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 27.82,
  "sfx": "sfx/whoosh.wav",
  "db": -3
 },
 {
  "t": 37.02,
  "sfx": "sfx/whoosh.wav",
  "db": 0
 },
 {
  "t": 37.86,
  "sfx": "sfx/pop.wav",
  "db": 0
 },
 {
  "t": 40.8,
  "sfx": "sfx/pop.wav",
  "db": -4
 },
 {
  "t": 43.34,
  "sfx": "sfx/pop.wav",
  "db": 0
 },
 {
  "t": 48.2,
  "sfx": "sfx/pop.wav",
  "db": 0
 },
 {
  "t": 51.3,
  "sfx": "sfx/pop.wav",
  "db": -4
 },
 {
  "t": 53.62,
  "sfx": "sfx/pop.wav",
  "db": 0
 },
 {
  "t": 56.42,
  "sfx": "sfx/pop.wav",
  "db": 0
 },
 {
  "t": 58.4,
  "sfx": "sfx/pop.wav",
  "db": -4
 },
 {
  "t": 60.16,
  "sfx": "sfx/pop.wav",
  "db": 0
 },
 {
  "t": 62.6,
  "sfx": "sfx/pop.wav",
  "db": -4
 },
 {
  "t": 66.46,
  "sfx": "sfx/whoosh.wav",
  "db": 0
 },
 {
  "t": 71.84,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 74.02,
  "sfx": "sfx/whoosh.wav",
  "db": 0
 },
 {
  "t": 78.02,
  "sfx": "sfx/whoosh.wav",
  "db": 0
 }
]
```

## FILE: templates/kinh-te-dia-phuong/src/board.html

```html
<template>
  <style>
    /*DESIGN*/
    #root { position: absolute; inset: 0; overflow: hidden; }
    /*MAPCSS*/
    #b-zoom { position: absolute; inset: 0; transform-origin: 540px 960px; }
    #b-mapwrap { position: absolute; inset: 0; opacity: 0.35; }
    #b-list { position: absolute; left: 70px; width: 860px; top: 380px; }
    .row { position: relative; height: 150px; border-top: 1px solid rgba(255,255,255,0.10); }
    .row:first-child { border-top: none; }
    .rin { position: absolute; inset: 0; display: flex; align-items: center; }
    .ic { flex: none; width: 44px; height: 44px; margin: 0 34px 0 8px; fill: none; stroke: var(--accent); stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
    .l1 { white-space: nowrap; line-height: 1; }
    .n { font-size: 88px; font-weight: 800; font-variant-numeric: tabular-nums; letter-spacing: -0.01em; }
    .u { margin-left: 14px; font-size: 32px; font-weight: 500; color: var(--ink75); }
    .l2 { margin-top: 8px; white-space: nowrap; font-size: 28px; font-weight: 500; color: var(--ink75); }
    .l2 .up { margin-left: 14px; font-size: 28px; }
  </style>
  <div id="root" data-composition-id="board" data-width="1080" data-height="1920">
    <div id="b-zoom">
      <div class="mapbg"></div>
      <div id="b-mapwrap">
        <svg id="b-map" class="map" width="1080" height="1920" viewBox="0 0 1080 1920" data-layout-allow-overflow><g class="world"></g></svg>
      </div>
      <div class="mapdots"></div>
    </div>
    <div id="b-seg" class="seg clip" data-start="0.2" data-duration="28.85" data-track-index="2" data-layout-allow-occlusion><span id="b-seg-t">Vĩnh Long · 8 tháng đầu năm 2026</span></div>
    <div id="b-list">
      <div class="row clip" id="r1" data-start="0.51" data-duration="28.93" data-track-index="3"><div class="rin">
        <svg class="ic" viewBox="0 0 24 24"><path d="M4 21V5l8-3 8 3v16M9 21v-4h6v4M8 8h.01M12 8h.01M16 8h.01M8 12h.01M12 12h.01M16 12h.01"/></svg>
        <div class="txt"><div class="l1"><span class="n" id="r1-n">830.0</span><span class="u">doanh nghiệp</span></div><div class="l2">thành lập mới <span class="up" id="r1-up">▲ vượt 9,26% kế hoạch năm</span></div></div>
      </div></div>
      <div class="row clip" id="r2" data-start="5.99" data-duration="23.45" data-track-index="3"><div class="rin">
        <svg class="ic" viewBox="0 0 24 24"><rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/></svg>
        <div class="txt"><div class="l1"><span class="n" id="r2-n">3323.0</span><span class="u">tỷ đồng</span></div><div class="l2">vốn đăng ký mới</div></div>
      </div></div>
      <div class="row clip" id="r3" data-start="10.85" data-duration="18.59" data-track-index="3"><div class="rin">
        <svg class="ic" viewBox="0 0 24 24"><circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.5 12h11l2-8H6.2"/></svg>
        <div class="txt"><div class="l1"><span class="n" id="r3-n">53766.0</span><span class="u">tỷ đồng</span></div><div class="l2">bán lẻ hàng hoá &amp; dịch vụ <span class="up" id="r3-up">▲ +19,34%</span></div></div>
      </div></div>
      <div class="row clip" id="r4" data-start="16.27" data-duration="13.17" data-track-index="3"><div class="rin">
        <svg class="ic" viewBox="0 0 24 24"><path d="M3 17l2 4h14l2-4M5 17V11h14v6M9 11V6h6v5M12 3v3"/></svg>
        <div class="txt"><div class="l1"><span class="n" id="r4-n">0.55</span><span class="u">tỷ USD</span></div><div class="l2">xuất siêu</div></div>
      </div></div>
      <div class="row clip" id="r5" data-start="19.07" data-duration="10.37" data-track-index="3"><div class="rin">
        <svg class="ic" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/></svg>
        <div class="txt"><div class="l1"><span class="n" id="r5-n">73.0</span><span class="u">dự án FDI</span></div><div class="l2">còn hiệu lực <span class="up" id="r5-up">▲ vốn 5,93 tỷ USD</span></div></div>
      </div></div>
      <div class="row clip" id="r6" data-start="22.81" data-duration="6.63" data-track-index="3"><div class="rin">
        <svg class="ic" viewBox="0 0 24 24"><path d="M4 21h8M6 21V4h2M8 4h12l-3 4M8 8h9M14 8v5M13 13h2v2h-2z"/></svg>
        <div class="txt"><div class="l1"><span class="n" id="r6-n">309.0</span><span class="u">dự án trong nước</span></div><div class="l2">còn hiệu lực <span class="up" id="r6-up">▲ vốn hơn 264.000 tỷ đồng</span></div></div>
      </div></div>
    </div>
    <p id="b-foot" class="foot clip" data-start="0.2" data-duration="28.85" data-track-index="4" data-layout-ignore><span id="b-foot-t">Nguồn: UBND tỉnh Vĩnh Long, họp báo 7/9/2026 · Báo Đầu tư, Mekong ASEAN</span></p>
  </div>
  <script>
    (() => {
      /*GEOJSON*/
      /*MAPJS*/
      const DUR = 29.44;
      // tỉnh phóng to ở nền, mờ 35%, trôi chậm + đổi cỡ mỗi ~4 s
      const map = makeMap({ svg: "#b-map", id: "b", labels: ".none", keys: [
        [0, 9.98, 106.25, 9.85], [4.2, 9.95, 106.3, 10.0], [8.4, 10.02, 106.2, 9.8], [12.6, 9.96, 106.28, 9.98],
        [16.8, 10.0, 106.22, 9.82], [21.0, 9.95, 106.27, 10.0], [25.2, 9.99, 106.23, 9.85], [29.44, 9.97, 106.25, 9.92],
      ] });
      document.querySelector("#b-vl").style.opacity = "1";
      document.querySelector("#b-vlglow").style.opacity = "0.5";
      const tl = gsap.timeline({ paused: true });
      const clock = { t: 0 };
      tl.fromTo(clock, { t: 0 }, { t: DUR, duration: DUR, ease: "none", onUpdate: () => map.apply(clock.t) }, 0);
      map.apply(0);
      tl.fromTo("#b-zoom", { scale: 1.4, filter: "blur(10px)" }, { scale: 1, filter: "blur(0px)", duration: 0.2, ease: "power3.out" }, 0);
      tl.fromTo(["#b-seg-t", "#b-foot-t"], { opacity: 0 }, { opacity: 1, duration: 0.35 }, 0.2);
      const fmt = (v, dec) => { const [i, d] = v.toFixed(dec).split("."); return i.replace(/\B(?=(\d{3})+(?!\d))/g, ".") + (d ? "," + d : ""); };
      tl.fromTo("#r1 .rin", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }, 0.51);
      (() => { const el = document.querySelector("#r1-n"), o = { v: 830.0 }; el.textContent = fmt(830.0, 0);
        tl.fromTo(o, { v: 830.0 }, { v: 2076, duration: 0.8, ease: "power2.out", onUpdate: () => { el.textContent = fmt(o.v, 0); } }, 0.51); })();
      tl.fromTo("#r1-up", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, 3.5);
      tl.fromTo("#r2 .rin", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }, 5.99);
      (() => { const el = document.querySelector("#r2-n"), o = { v: 3323.0 }; el.textContent = fmt(3323.0, 0);
        tl.fromTo(o, { v: 3323.0 }, { v: 8308, duration: 0.8, ease: "power2.out", onUpdate: () => { el.textContent = fmt(o.v, 0); } }, 5.99); })();
      tl.fromTo("#r3 .rin", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }, 10.85);
      (() => { const el = document.querySelector("#r3-n"), o = { v: 53766.0 }; el.textContent = fmt(53766.0, 0);
        tl.fromTo(o, { v: 53766.0 }, { v: 134414, duration: 0.8, ease: "power2.out", onUpdate: () => { el.textContent = fmt(o.v, 0); } }, 10.85); })();
      tl.fromTo("#r3-up", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, 14.0);
      tl.fromTo("#r4 .rin", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }, 16.27);
      (() => { const el = document.querySelector("#r4-n"), o = { v: 0.55 }; el.textContent = fmt(0.55, 2);
        tl.fromTo(o, { v: 0.55 }, { v: 1.37, duration: 0.8, ease: "power2.out", onUpdate: () => { el.textContent = fmt(o.v, 2); } }, 16.27); })();
      tl.fromTo("#r5 .rin", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }, 19.07);
      (() => { const el = document.querySelector("#r5-n"), o = { v: 73.0 }; el.textContent = fmt(73.0, 0);
        tl.fromTo(o, { v: 73.0 }, { v: 183, duration: 0.8, ease: "power2.out", onUpdate: () => { el.textContent = fmt(o.v, 0); } }, 19.07); })();
      tl.fromTo("#r5-up", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, 21.1);
      tl.fromTo("#r6 .rin", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }, 22.81);
      (() => { const el = document.querySelector("#r6-n"), o = { v: 309.0 }; el.textContent = fmt(309.0, 0);
        tl.fromTo(o, { v: 309.0 }, { v: 772, duration: 0.8, ease: "power2.out", onUpdate: () => { el.textContent = fmt(o.v, 0); } }, 22.81); })();
      tl.fromTo("#r6-up", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, 25.3);
      // mọi chữ tắt trước chuyển cảnh, rồi whip zoom ra
      tl.to(["#b-list .rin", "#b-seg-t", "#b-foot-t"], { opacity: 0, duration: 0.25, ease: "power1.in" }, DUR - 0.45);
      tl.fromTo("#b-zoom", { scale: 1, filter: "blur(0px)" }, { scale: 1.35, filter: "blur(10px)", duration: 0.17, ease: "power3.in", immediateRender: false }, DUR - 0.17);
      window.__timelines["board"] = tl;
    })();
  </script>
</template>
```

## FILE: templates/kinh-te-dia-phuong/src/doc.html

```html
<template>
  <style>
    /*DESIGN*/
    #root { position: absolute; inset: 0; overflow: hidden; }
    #d-zoom { position: absolute; inset: 0; transform-origin: 540px 960px; background: radial-gradient(ellipse at 50% 42%, #13243A, #0E1A2B); }
    #d-dots { position: absolute; inset: 0; background: radial-gradient(circle at 2px 2px, rgba(170,195,230,0.12) 1.1px, transparent 1.6px) 0 0 / 7px 7px; }
    #d-card { position: absolute; left: 60px; width: 880px; top: 360px; height: 1070px; background: #FBFAF7; border-radius: 14px; overflow: hidden; box-shadow: 0 30px 80px rgba(0,0,0,0.5); }
    #d-page { position: absolute; left: 0; top: 0; width: 880px; height: 2080px; transform-origin: 50% 0; }
    #d-page img { position: absolute; left: 45px; top: 36px; width: 790px; height: 1965px; }
    #d-hl { position: absolute; left: 40px; width: 800px; top: 1617px; height: 165px; background: rgba(242,140,40,0.30); border-radius: 4px; transform-origin: 0 50%; }
  </style>
  <div id="root" data-composition-id="doc" data-width="1080" data-height="1920">
    <div id="d-zoom">
      <div id="d-dots"></div>
      <div id="d-card" data-layout-allow-overflow>
        <div id="d-page" data-layout-allow-overflow data-layout-allow-overlap>
          <img src="assets/doc/article.png" alt="" />
          <div id="d-hl"></div>
        </div>
      </div>
    </div>
    <div id="d-seg" class="seg clip" data-start="0.2" data-duration="6.9" data-track-index="2" data-layout-allow-occlusion><span id="d-seg-t">Tài liệu gốc · Báo Đầu tư 07/09/2026</span></div>
    <p id="d-foot" class="foot clip" data-start="0.2" data-duration="6.9" data-track-index="3" data-layout-ignore><span id="d-foot-t">Ảnh chụp bài viết trên baodautu.vn, đăng 07/09/2026</span></p>
  </div>
  <script>
    (() => {
      const tl = gsap.timeline({ paused: true });
      const DUR = 7.56; // 66.74 -> 74.3 (giữ tới khi đọc xong "...8 tháng đầu năm")
      tl.fromTo("#d-zoom", { scale: 1.4, filter: "blur(10px)" }, { scale: 1, filter: "blur(0px)", duration: 0.2, ease: "power3.out" }, 0);
      tl.fromTo(["#d-seg-t", "#d-foot-t"], { opacity: 0 }, { opacity: 1, duration: 0.35 }, 0.2);
      // mở bằng toàn bộ tiêu đề + ảnh họp báo, rồi zoom chậm vào đoạn có 2.076 / 8.308
      tl.fromTo("#d-page", { y: 0, scale: 1 }, { y: 0, scale: 1.02, duration: 2.6, ease: "sine.inOut" }, 0);
      tl.to("#d-page", { y: -1335, scale: 1.1, duration: 2.8, ease: "power2.inOut" }, 2.6);
      tl.to("#d-page", { y: -1370, scale: 1.12, duration: DUR - 5.4, ease: "sine.out" }, 5.4);
      tl.fromTo("#d-hl", { scaleX: 0, opacity: 0 }, { scaleX: 1, opacity: 1, duration: 0.5, ease: "power2.out" }, 5.1);
      tl.to(["#d-seg-t", "#d-foot-t"], { opacity: 0, duration: 0.25, ease: "power1.in" }, DUR - 0.45);
      tl.fromTo("#d-zoom", { scale: 1, filter: "blur(0px)" }, { scale: 1.35, filter: "blur(10px)", duration: 0.17, ease: "power3.in", immediateRender: false }, DUR - 0.17);
      window.__timelines["doc"] = tl;
    })();
  </script>
</template>
```

## FILE: templates/kinh-te-dia-phuong/src/earthb.html

```html
<template>
  <style>
    /*DESIGN*/
    #root { position: absolute; inset: 0; overflow: hidden; }
    #ew { position: absolute; inset: 0; transform-origin: 540px 960px; }
    #ew video { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
  </style>
  <div id="root" data-composition-id="earthb" data-width="1080" data-height="1920">
    <div id="ew"><video id="ebv" class="clip" src="assets/earth/s4g.mp4" muted playsinline data-start="0" data-duration="4" data-media-start="0.6" data-track-index="1"></video></div>
    <div class="gtop" data-layout-allow-occlusion></div>
    <div class="gbot" data-layout-allow-occlusion></div>
    <div id="e-seg" class="seg clip" data-start="0.2" data-duration="3.4" data-track-index="2" data-layout-allow-occlusion><span id="e-seg-t">Hạ tầng kết nối</span></div>
    <!-- Kiểu A: chấm đặt đúng trên cầu Mỹ Thuận trong khung -->
    <div id="e-la" class="la clip" data-start="0.3" data-duration="3.3" data-track-index="3" style="transform: translate(560px, 800px)">
      <span class="lead" style="width: 190px; transform: rotate(-0.85rad)"></span><span class="dot"></span>
      <span class="tx" style="left: 134px; top: -132px; transform: translate(0,-50%)">Cầu Mỹ Thuận 1 &amp; 2</span>
    </div>
    <h2 id="ea" class="anchor low clip" data-start="1.8" data-duration="1.85" data-track-index="4"><span class="ln"><span class="w">Vận</span> <span class="w">hội</span></span><span class="ln"><em><span class="w">chưa</span> <span class="w">từng</span> <span class="w">có</span></em></span></h2>
    <p id="e-foot" class="foot clip" data-start="0.2" data-duration="3.4" data-track-index="5" data-layout-ignore><span id="e-foot-t">Hình ảnh 3D: Google Earth</span></p>
  </div>
  <script>
    (() => {
      const tl = gsap.timeline({ paused: true });
      const DUR = 4.0; // 74.3 -> 78.3
      tl.fromTo("#ew", { scale: 1.4, filter: "blur(10px)" }, { scale: 1, filter: "blur(0px)", duration: 0.2, ease: "power3.out" }, 0);
      tl.fromTo(["#e-seg-t", "#e-foot-t"], { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.2);
      tl.fromTo("#e-la > *", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, 0.3);
      tl.fromTo("#ea .w", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.25, ease: "expo.out", stagger: 0.08 }, 1.85);
      tl.to(["#e-la > *", "#ea .w", "#e-seg-t", "#e-foot-t"], { opacity: 0, duration: 0.2, ease: "power1.in" }, DUR - 0.4);
      tl.fromTo("#ew", { scale: 1, filter: "blur(0px)" }, { scale: 1.35, filter: "blur(10px)", duration: 0.17, ease: "power3.in", immediateRender: false }, DUR - 0.17);
      window.__timelines["earthb"] = tl;
    })();
  </script>
</template>
```

## FILE: templates/kinh-te-dia-phuong/src/end.html

```html
<template>
  <style>
    /*DESIGN*/
    #root { position: absolute; inset: 0; overflow: hidden; }
    .nw { position: absolute; inset: 0; transform-origin: 540px 960px; }
    .nw video { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
  </style>
  <div id="root" data-composition-id="end" data-width="1080" data-height="1920">
    <div id="nw1" class="nw"><video id="nv1" class="clip" src="/*E1SRC*/" muted playsinline data-start="0" data-duration="4.94" data-media-start="/*E1MS*/" data-track-index="1"></video></div>
    <div id="nw2" class="nw"><video id="nv2" class="clip" src="/*E2SRC*/" muted playsinline data-start="4.94" data-duration="5.36" data-media-start="/*E2MS*/" data-track-index="1"></video></div>
    <div class="gtop" data-layout-allow-occlusion></div>
    <div class="gbot" data-layout-allow-occlusion></div>
    <div id="n-seg" class="seg clip" data-start="0.2" data-duration="10.1" data-track-index="2" data-layout-allow-occlusion><span id="n-seg-t">Bài toán phía trước</span></div>
    <h2 id="na1" class="anchor low clip" data-start="1.65" data-duration="1.45" data-track-index="3"><span class="ln"><span class="w">Tái</span> <span class="w">cấu</span> <span class="w">trúc</span></span><span class="ln"><em><span class="w">đô</span> <span class="w">thị</span></em></span></h2>
    <h2 id="na2" class="anchor low clip" data-start="3.45" data-duration="1.3" data-track-index="3"><span class="ln"><span class="w">Giải</span> <span class="w">toả</span></span><span class="ln"><em><span class="w">nút</span> <span class="w">giao</span> <span class="w">thông</span></em></span></h2>
    <h2 id="nf" class="anchor low clip" data-start="5.05" data-duration="5.25" data-track-index="3">
      <span class="ln"><span class="w">Chuyển</span> <span class="w">hoá</span> <span class="w">nội</span> <span class="w">lực</span></span>
      <span class="ln"><span class="w">thành</span> <em><span class="w">giá</span> <span class="w">trị</span> <span class="w">thực</span></em></span>
    </h2>
    <p id="n-foot" class="foot clip" data-start="0.2" data-duration="10.1" data-track-index="4" data-layout-ignore><span id="n-foot-t">/*ESRC*/</span></p>
  </div>
  <script>
    (() => {
      const tl = gsap.timeline({ paused: true });
      tl.fromTo("#nw1", { scale: 1.4, filter: "blur(10px)" }, { scale: 1, filter: "blur(0px)", duration: 0.2, ease: "power3.out" }, 0);
      tl.fromTo(["#n-seg-t", "#n-foot-t"], { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.2);
      const aIn = (sel, at, gap = 0.09) => tl.fromTo(`${sel} .w`, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.25, ease: "expo.out", stagger: gap }, at);
      const aOut = (sel, at) => tl.to(`${sel} .w`, { opacity: 0, duration: 0.15, ease: "power1.in" }, at);
      aIn("#na1", 1.68); aOut("#na1", 2.95);
      aIn("#na2", 3.48); aOut("#na2", 4.6);   // tắt trước điểm cắt 4.94
      aIn("#nf", 5.1, 0.14);
      window.__timelines["end"] = tl;
    })();
  </script>
</template>
```

## FILE: templates/kinh-te-dia-phuong/src/foot.html

```html
<template>
  <style>
    /*DESIGN*/
    #root { position: absolute; inset: 0; overflow: hidden; }
    #f-all { position: absolute; inset: 0; }
    .fw { position: absolute; inset: 0; transform-origin: 540px 960px; }
    .fw video { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
  </style>
  <div id="root" data-composition-id="foot" data-width="1080" data-height="1920">
    <div id="f-all">
      <div id="fw1" class="fw"><video id="fv1" class="clip" src="/*F1SRC*/" muted playsinline data-start="0" data-duration="5" data-media-start="/*F1MS*/" data-track-index="1"></video></div>
      <div id="fw2" class="fw"><video id="fv2" class="clip" src="/*F2SRC*/" muted playsinline data-start="5" data-duration="4.3" data-media-start="/*F2MS*/" data-track-index="1"></video></div>
      <div class="gtop" data-layout-allow-occlusion></div>
      <div class="gbot" data-layout-allow-occlusion></div>
    </div>
    <div id="f-seg" class="seg clip" data-start="0.45" data-duration="8.5" data-track-index="2" data-layout-allow-occlusion><span id="f-seg-t">Kinh tế vùng châu thổ</span></div>
    <h2 id="fa1" class="anchor low clip" data-start="1.3" data-duration="3.5" data-track-index="3"><span class="ln"><span class="w">Chỉ</span> <span class="w">số</span> <span class="w">kinh</span> <span class="w">tế</span></span><span class="ln"><em><span class="w">mới</span> <span class="w">nhất</span></em></span></h2>
    <h2 id="fa2" class="anchor low clip" data-start="6.5" data-duration="2.5" data-track-index="3"><span class="ln"><span class="w">Tốc</span> <span class="w">độ</span></span><span class="ln"><em><span class="w">đáng</span> <span class="w">kinh</span> <span class="w">ngạc</span></em></span></h2>
    <p id="f-foot" class="foot clip" data-start="0.45" data-duration="8.5" data-track-index="4" data-layout-ignore><span id="f-foot-t">/*FSRC*/</span></p>
  </div>
  <script>
    (() => {
      const tl = gsap.timeline({ paused: true });
      const DUR = 9.3;
      // hoà từ bản đồ (đang zoom xuyên vào tỉnh) sang cảnh quay trong 12 khung
      tl.fromTo("#f-all", { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "none" }, 0);
      tl.fromTo("#fw1", { scale: 1.12 }, { scale: 1, duration: 1.2, ease: "power2.out" }, 0);
      const fade = (sel, at, d = 0.3) => tl.fromTo(sel, { opacity: 0 }, { opacity: 1, duration: d, ease: "power2.out" }, at);
      const out = (sel, at, d = 0.2) => tl.to(sel, { opacity: 0, duration: d, ease: "power1.in" }, at);
      const anchorIn = (sel, at) => tl.fromTo(`${sel} .w`, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.3, ease: "expo.out", stagger: 0.1 }, at);
      fade("#f-seg-t", 0.45); fade("#f-foot-t", 0.5);
      anchorIn("#fa1", 1.3); out("#fa1 .w", 4.65);
      // cắt thẳng ở 5.0; chữ đã tắt trước đó
      anchorIn("#fa2", 6.5);
      out(["#fa2 .w", "#f-seg-t", "#f-foot-t"], DUR - 0.45);
      tl.fromTo("#fw2", { scale: 1, filter: "blur(0px)" }, { scale: 1.35, filter: "blur(10px)", duration: 0.17, ease: "power3.in", immediateRender: false }, DUR - 0.17);
      window.__timelines["foot"] = tl;
    })();
  </script>
</template>
```

## FILE: templates/kinh-te-dia-phuong/src/geo.html

```html
<template>
  <style>
    /*DESIGN*/
    #root { position: absolute; inset: 0; overflow: hidden; }
    /*MAPCSS*/
    #g-zoom { position: absolute; inset: 0; transform-origin: 540px 960px; }
    #g-qdim { position: absolute; inset: 0; background: rgba(14,26,43,0.55); opacity: 0; }
  </style>
  <div id="root" data-composition-id="geo" data-width="1080" data-height="1920">
    <div id="g-zoom">
      <div class="mapbg"></div>
      <svg id="g-map" class="map" width="1080" height="1920" viewBox="0 0 1080 1920" data-layout-allow-overflow><g class="world"></g></svg>
      <div class="mapdots"></div>
      <!-- Kiểu A: địa danh -->
      <div class="la g-lab" id="l-reg" data-at="region" data-lx="0" data-ly="-150" data-align="c"><span class="lead"></span><span class="dot"></span><span class="tx">Đồng bằng sông Cửu Long</span></div>
      <div class="la acc g-lab" id="l-vl" data-at="Vĩnh Long" data-lx="0" data-ly="250" data-align="c"><span class="lead"></span><span class="dot"></span><span class="tx">Vĩnh Long<small>gồm Vĩnh Long, Bến Tre, Trà Vinh cũ</small></span></div>
      <div class="la g-lab" id="l-tien" data-at="rv_tien" data-lx="60" data-ly="-90"><span class="lead"></span><span class="dot"></span><span class="tx">Sông Tiền</span></div>
      <div class="la g-lab" id="l-hau" data-at="rv_hau" data-lx="-60" data-ly="90"><span class="lead"></span><span class="dot"></span><span class="tx">Sông Hậu</span></div>
      <div class="la g-lab" id="l-hcm" data-at="pt_hcm" data-lx="70" data-ly="-80"><span class="lead"></span><span class="dot"></span><span class="tx">TP.HCM</span></div>
      <div class="la g-lab" id="l-ct" data-at="pt_ct" data-lx="-80" data-ly="70"><span class="lead"></span><span class="dot"></span><span class="tx">Cần Thơ</span></div>
      <div class="la g-lab" id="l-coast" data-at="coast" data-lx="-90" data-ly="240" data-align="c"><span class="lead"></span><span class="dot"></span><span class="tx">Dải ven biển phía Đông</span></div>
      <div class="la g-lab" id="l-center" data-at="pt_ct" data-lx="-30" data-ly="150" data-align="c"><span class="lead"></span><span class="dot"></span><span class="tx">Tiểu vùng trung tâm</span></div>
      <!-- Kiểu B: khái niệm -->
      <div class="lb g-lab" id="l-buf" data-at="pt_vl" data-dx="-40" data-dy="-110"><span>Vùng đệm?</span></div>
      <div class="lb g-lab" id="l-pole" data-at="Vĩnh Long" data-dx="0" data-dy="-230"><span>Cực tăng trưởng</span></div>
      <div class="lb g-lab" id="l-hinge" data-at="pt_vl" data-dx="60" data-dy="-120"><span>Bản lề kết nối</span></div>
    </div>
    <div id="g-qdim"></div>
    <div id="g-seg" class="seg clip" data-start="0.15" data-duration="22.6" data-track-index="2" data-layout-allow-occlusion><span id="g-seg-t">Vị trí · Vĩnh Long</span></div>
    <h1 id="a1" class="anchor low clip" data-start="0.3" data-duration="2.5" data-track-index="3"><span class="ln"><span class="w">Trái</span> <span class="w">tim</span> <em><span class="w">châu</span> <span class="w">thổ</span></em></span></h1>
    <h2 id="a2" class="anchor low clip" data-start="10.5" data-duration="2.75" data-track-index="3"><span class="ln"><span class="w">Chiến</span> <span class="w">lược</span></span><span class="ln"><em><span class="w">phát</span> <span class="w">triển</span> <span class="w">vùng</span></em></span></h2>
    <h2 id="aq" class="anchor mid clip" data-start="22.95" data-duration="4.85" data-track-index="3">
      <span class="ln"><span class="w">Vĩnh</span> <span class="w">Long</span> <span class="w">đã</span></span>
      <span class="ln"><em><span class="w">tích</span> <span class="w">lũy</span></em> <span class="w">được</span> <span class="w">gì?</span></span>
    </h2>
    <p id="g-foot" class="foot clip" data-start="0" data-duration="27.7" data-track-index="4" data-layout-ignore><span id="g-foot-t">Bản đồ: Natural Earth · gộp tỉnh theo NQ 202/2025/QH15</span></p>
  </div>
  <script>
    (() => {
      /*GEOJSON*/
      /*MAPJS*/
      const DUR = 28.4;
      const map = makeMap({ svg: "#g-map", id: "g", labels: ".g-lab", rings: [[15.6, 1.5, 300], [16.05, 1.5, 300], [16.5, 1.5, 300]], keys: [
        // tâm camera lệch nam ~0,3° so với tỉnh => tỉnh nằm cao hơn, nhãn dưới tỉnh không rơi vào vùng caption TikTok
        [0.0, 16.2, 105.9, 7.22], [1.6, 10.15, 105.75, 8.55], [2.9, 9.78, 106.15, 9.3], [4.4, 9.82, 106.12, 9.22],
        [7.3, 10.12, 106.35, 9.02], [10.1, 10.08, 106.25, 9.0], [12.0, 9.5, 105.35, 8.45], [15.6, 9.72, 106.22, 9.62],
        [17.4, 9.72, 106.15, 9.55], [19.6, 9.68, 106.18, 9.22], [22.8, 9.7, 106.15, 9.28],
        [27.6, 10.02, 106.2, 10.15], [28.4, 9.98, 106.25, 11.6, true],   // zoom xuyên vào tâm tỉnh trước khi hoà sang cảnh quay
      ] });
      const tl = gsap.timeline({ paused: true });
      const clock = { t: 0 };
      tl.fromTo(clock, { t: 0 }, { t: DUR, duration: DUR, ease: "none", onUpdate: () => map.apply(clock.t) }, 0);
      map.apply(0);
      const inA = (sel, at) => tl.fromTo(`${sel} > *`, { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "power2.out" }, at);
      const outA = (sel, at) => tl.to(`${sel} > *`, { opacity: 0, duration: 0.25, ease: "power1.in" }, at);
      const inB = (sel, at) => tl.fromTo(`${sel} > span`, { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }, at);
      const outB = (sel, at) => tl.to(`${sel} > span`, { opacity: 0, duration: 0.25, ease: "power1.in" }, at);
      const show = (sel, at, d = 0.5, to = 1) => tl.fromTo(sel, { opacity: 0 }, { opacity: to, duration: d, ease: "power2.out" }, at);
      const hide = (sel, at, d = 0.4) => tl.to(sel, { opacity: 0, duration: d, ease: "power1.in" }, at);
      const draw = (sel, at, d) => tl.fromTo(sel, { strokeDashoffset: 100 }, { strokeDashoffset: 0, duration: d, ease: "power1.inOut" }, at);
      const anchorIn = (sel, at, gap = 0.1) => tl.fromTo(`${sel} .w`, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.3, ease: "expo.out", stagger: gap }, at);
      const anchorOut = (sel, at) => tl.to(`${sel} .w`, { opacity: 0, duration: 0.2, ease: "power1.in" }, at);

      tl.fromTo("#g-seg-t", { opacity: 0 }, { opacity: 1, duration: 0.35 }, 0.15);
      tl.fromTo("#g-foot-t", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.3);
      anchorIn("#a1", 0.35); anchorOut("#a1", 2.55);
      show("#g-region", 0.6, 0.6); inA("#l-reg", 1.3); outA("#l-reg", 2.7); hide("#g-region", 3.0, 0.6);
      show("#g-vl", 2.4, 0.4); show("#g-vlglow", 2.4, 0.4, 0.55); inA("#l-vl", 2.8);
      draw("#g-tieng", 3.0, 1.3); draw("#g-tien", 3.0, 1.3); inA("#l-tien", 3.3);
      draw("#g-haug", 3.7, 1.3); draw("#g-hau", 3.7, 1.3); inA("#l-hau", 4.0);
      outA("#l-tien", 5.4); outA("#l-hau", 5.4); inB("#l-buf", 5.7);
      show("#g-hcm", 7.6, 0.4); inA("#l-hcm", 7.7);
      show("#g-ct", 9.6, 0.4); inA("#l-ct", 9.7);
      draw("#g-corr", 6.3, 3.8);
      outB("#l-buf", 10.1);
      hide(["#g-tien", "#g-tieng", "#g-hau", "#g-haug"], 10.2, 0.6);
      tl.to("#g-region", { opacity: 1, duration: 0.3 }, 10.4);
      outA("#l-vl", 10.3); anchorIn("#a2", 10.55); anchorOut("#a2", 13.0); inA("#l-vl", 13.25);
      inA("#l-reg", 11.0); outA("#l-reg", 13.1); hide("#g-region", 13.2, 0.6);
      hide(["#g-hcm", "#g-ct", "#g-corr"], 11.2, 0.6); outA("#l-hcm", 11.2); outA("#l-ct", 11.2);
      tl.to("#g-vlglow", { opacity: 1, duration: 0.3 }, 15.5);
      inB("#l-pole", 15.7); outB("#l-pole", 17.4);
      tl.to("#g-vlglow", { opacity: 0.55, duration: 0.5 }, 17.4);
      inB("#l-hinge", 17.9); outB("#l-hinge", 20.4); outA("#l-vl", 20.4);
      draw("#g-coastg", 20.6, 1.0); draw("#g-coast", 20.6, 1.0); inA("#l-coast", 21.0);
      draw("#g-cone", 18.7, 1.6);
      show("#g-center", 21.9, 0.5); inA("#l-center", 22.2);
      draw("#g-conc", 21.4, 1.0);
      outA("#l-coast", 22.75); outA("#l-center", 22.75);
      hide(["#g-cone", "#g-conc", "#g-coast", "#g-coastg", "#g-center"], 22.8, 0.4);
      tl.to("#g-qdim", { opacity: 1, duration: 0.4 }, 22.85);
      hide("#g-seg-t", 22.5, 0.3);
      anchorIn("#aq", 22.98, 0.14);
      // mọi chữ tắt hết trước khi hoà sang cảnh quay (28.0)
      anchorOut("#aq", 27.55); hide("#g-foot-t", 27.45, 0.25);
      tl.to("#g-qdim", { opacity: 0, duration: 0.5 }, 27.4);
      window.__timelines["geo"] = tl;
    })();
  </script>
</template>
```

## FILE: templates/kinh-te-dia-phuong/tpl/board.tpl.html

```html
<template>
  <style>
    /*DESIGN*/
    #root { position: absolute; inset: 0; overflow: hidden; }
    /*MAPCSS*/
    #b-zoom { position: absolute; inset: 0; transform-origin: 540px 960px; }
    #b-mapwrap { position: absolute; inset: 0; opacity: 0.35; }
    #b-list { position: absolute; left: 70px; width: 860px; top: 380px; }
    .row { position: relative; height: 150px; border-top: 1px solid rgba(255,255,255,0.10); }
    .row:first-child { border-top: none; }
    .rin { position: absolute; inset: 0; display: flex; align-items: center; }
    .ic { flex: none; width: 44px; height: 44px; margin: 0 34px 0 8px; fill: none; stroke: var(--accent); stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
    .l1 { white-space: nowrap; line-height: 1; }
    .n { font-size: 88px; font-weight: 800; font-variant-numeric: tabular-nums; letter-spacing: -0.01em; }
    .u { margin-left: 14px; font-size: 32px; font-weight: 500; color: var(--ink75); }
    .l2 { margin-top: 8px; white-space: nowrap; font-size: 28px; font-weight: 500; color: var(--ink75); }
    .l2 .up { margin-left: 14px; font-size: 28px; }
  </style>
  <div id="root" data-composition-id="board" data-width="1080" data-height="1920">
    <div id="b-zoom">
      <div class="mapbg"></div>
      <div id="b-mapwrap">
        <svg id="b-map" class="map" width="1080" height="1920" viewBox="0 0 1080 1920" data-layout-allow-overflow><g class="world"></g></svg>
      </div>
      <div class="mapdots"></div>
    </div>
    <div id="b-seg" class="seg clip" data-start="0.2" data-duration="28.85" data-track-index="2" data-layout-allow-occlusion><span id="b-seg-t">Vĩnh Long · 8 tháng đầu năm 2026</span></div>
    <div id="b-list">
<!--ROWS-->
    </div>
    <p id="b-foot" class="foot clip" data-start="0.2" data-duration="28.85" data-track-index="4" data-layout-ignore><span id="b-foot-t">Nguồn: UBND tỉnh Vĩnh Long, họp báo 7/9/2026 · Báo Đầu tư, Mekong ASEAN</span></p>
  </div>
  <script>
    (() => {
      /*GEOJSON*/
      /*MAPJS*/
      const DUR = 29.44;
      // tỉnh phóng to ở nền, mờ 35%, trôi chậm + đổi cỡ mỗi ~4 s
      const map = makeMap({ svg: "#b-map", id: "b", labels: ".none", keys: [
        [0, 9.98, 106.25, 9.85], [4.2, 9.95, 106.3, 10.0], [8.4, 10.02, 106.2, 9.8], [12.6, 9.96, 106.28, 9.98],
        [16.8, 10.0, 106.22, 9.82], [21.0, 9.95, 106.27, 10.0], [25.2, 9.99, 106.23, 9.85], [29.44, 9.97, 106.25, 9.92],
      ] });
      document.querySelector("#b-vl").style.opacity = "1";
      document.querySelector("#b-vlglow").style.opacity = "0.5";
      const tl = gsap.timeline({ paused: true });
      const clock = { t: 0 };
      tl.fromTo(clock, { t: 0 }, { t: DUR, duration: DUR, ease: "none", onUpdate: () => map.apply(clock.t) }, 0);
      map.apply(0);
      tl.fromTo("#b-zoom", { scale: 1.4, filter: "blur(10px)" }, { scale: 1, filter: "blur(0px)", duration: 0.2, ease: "power3.out" }, 0);
      tl.fromTo(["#b-seg-t", "#b-foot-t"], { opacity: 0 }, { opacity: 1, duration: 0.35 }, 0.2);
      const fmt = (v, dec) => { const [i, d] = v.toFixed(dec).split("."); return i.replace(/\B(?=(\d{3})+(?!\d))/g, ".") + (d ? "," + d : ""); };
/*ROWJS*/
      // mọi chữ tắt trước chuyển cảnh, rồi whip zoom ra
      tl.to(["#b-list .rin", "#b-seg-t", "#b-foot-t"], { opacity: 0, duration: 0.25, ease: "power1.in" }, DUR - 0.45);
      tl.fromTo("#b-zoom", { scale: 1, filter: "blur(0px)" }, { scale: 1.35, filter: "blur(10px)", duration: 0.17, ease: "power3.in", immediateRender: false }, DUR - 0.17);
      window.__timelines["board"] = tl;
    })();
  </script>
</template>
```

## FILE: templates/map-dive-parallax/assets/README.md

```markdown
# assets/

Đặt ở đây ảnh tách lớp (PNG nền trong suốt), video bản đồ đã bake, nhạc, font.
Đường dẫn trong HTML luôn là `assets/...` (không có `/` ở đầu).
Gợi ý đặt tên: `L3000-troi.png`, `L1800-skyline-xa.png`, `L900-khoi-giua.png`, `L300-du-an.png`, `L-350-tien-canh.png`
(số đầu = data-depth của lớp sẽ chứa ảnh).
```

## FILE: templates/map-dive-parallax/compositions/dive.html

```html
<template>
  <style>
    #root {
      position: absolute;
      inset: 0;
      overflow: hidden;
      font-family: var(--font-display), "Montserrat", sans-serif;
      color: var(--color-ink);
    }

    /* ---------- CAMERA RIG (khung dọc 1080×1920) ----------
       KHÔNG đặt opacity<1, filter, overflow:hidden, clip-path, mix-blend-mode lên #d-stage / #d-cam:
       Chrome sẽ làm phẳng 3D và mất parallax. */
    #d-stage {
      position: absolute;
      inset: 0;
      perspective: 1000px; /* = P trong script */
      perspective-origin: 50% 50%;
    }
    #d-cam {
      position: absolute;
      left: 0;
      top: 0;
      width: 1080px;
      height: 1920px;
      transform-style: preserve-3d;
      transform-origin: 540px 960px 0;
    }
    .d-layer {
      position: absolute;
      left: 0;
      top: 0;
      width: 1080px;
      height: 1920px;
      transform-origin: 540px 960px 0;
    }
    .d-layer > * {
      position: absolute;
    }

    /* Bản đồ (depth 0). Thay #d-map-svg bằng ảnh vệ tinh/bản đồ thật hoặc video bake-basemap. */
    #d-map-svg {
      left: -1080px;
      top: -1920px;
    }
    #d-route-glow {
      fill: none;
      stroke: var(--color-route);
      stroke-width: 34;
      stroke-linecap: round;
      opacity: 0.55;
    }
    #d-route-core {
      fill: none;
      stroke: var(--color-accent);
      stroke-width: 11;
      stroke-linecap: round;
    }
    #d-zone {
      fill: var(--color-zone);
      fill-opacity: 0.28;
      stroke: var(--color-zone);
      stroke-width: 5;
    }

    /* Ghim & nhãn nổi trên bản đồ (depth âm = cao hơn mặt đất -> parallax khi camera nghiêng/xoay) */
    .pin {
      width: 0;
      height: 0;
    }
    .pin-dot {
      position: absolute;
      left: -15px;
      top: -15px;
      width: 30px;
      height: 30px;
      border-radius: 50%;
      background: #fff;
      border: 7px solid #111;
      box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.35);
    }
    .pin-tag {
      position: absolute;
      left: 26px;
      top: -27px;
      padding: 8px 16px 9px;
      white-space: nowrap;
      font-size: 32px;
      font-weight: 800;
      letter-spacing: 0.02em;
      text-transform: uppercase;
      background: rgba(10, 10, 10, 0.82);
      border-radius: 8px;
    }
    #d-zone-tag {
      left: 470px;
      top: 1395px;
      padding: 10px 22px 12px;
      font-size: 44px;
      font-weight: 900;
      text-transform: uppercase;
      color: #08130c;
      background: var(--color-zone);
      border-radius: 10px;
    }

    /* Thẻ dự án (logo) cắm trên tuyến */
    #d-card {
      left: 570px;
      top: 1100px;
      width: 260px;
    }
    #d-card .card-box {
      display: block;
      padding: 20px 22px 18px;
      background: #fff;
      color: #0e2a4a;
      border-radius: 18px;
      text-align: center;
      box-shadow: 0 18px 50px rgba(0, 0, 0, 0.45);
    }
    #d-card .card-k {
      display: block;
      font-size: 30px;
      font-weight: 700;
      letter-spacing: 0.08em;
      color: #5b6f86;
    }
    #d-card .card-name {
      display: block;
      font-size: 46px;
      font-weight: 900;
      line-height: 1.05;
    }
    #d-card-stem {
      left: 697px;
      top: 1222px;
      width: 6px;
      height: 70px;
      background: #fff;
    }

    /* Mây tiền cảnh: camera bay xuyên qua lúc mở đầu */
    .cloud {
      border-radius: 50%;
      background: radial-gradient(closest-side, rgba(235, 240, 245, 0.85), rgba(235, 240, 245, 0.35) 55%, rgba(235, 240, 245, 0));
    }
    #d-cl-a { left: -260px; top: 520px; width: 900px; height: 520px; }
    #d-cl-b { left: 520px; top: 1150px; width: 980px; height: 560px; }
    #d-cl-c { left: 180px; top: 1650px; width: 760px; height: 420px; }
    #d-cl-d { left: 560px; top: 180px; width: 700px; height: 400px; }

    /* ---------- HUD (khoá màn hình) ---------- */
    #h-scrim {
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      height: 820px;
      background: linear-gradient(180deg, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0.55) 70%, rgba(0, 0, 0, 0.7) 100%);
    }
    #h-pill {
      position: absolute;
      left: 0;
      right: 0;
      top: 190px;
      text-align: center;
    }
    #h-pill span {
      display: inline-block;
      padding: 12px 30px 14px;
      font-size: 36px;
      font-weight: 800;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      background: var(--color-pill);
      border-radius: 999px;
    }
    .h-title {
      position: absolute;
      left: 80px;
      right: 80px;
      text-align: center;
      font-weight: 900;
      text-transform: uppercase;
      line-height: 1.04;
      text-shadow: 0 6px 30px rgba(0, 0, 0, 0.55);
    }
    .h-title span {
      display: inline-block;
    }
    .h-title em {
      font-style: normal;
      color: var(--color-accent);
    }
    #h-hook {
      bottom: 430px;
      font-size: 104px;
    }
    #h-mid {
      bottom: 470px;
      font-size: 64px;
    }
    #h-end {
      bottom: 400px;
      font-size: 70px;
    }
    #h-end .big {
      display: block;
      margin-top: 10px;
      font-size: 168px;
      color: var(--color-accent);
      font-variant-numeric: tabular-nums;
      letter-spacing: -0.02em;
    }
    #h-source {
      position: absolute;
      left: 0;
      right: 0;
      bottom: 150px;
      text-align: center;
      font-size: 28px;
      font-weight: 600;
      color: rgba(255, 255, 255, 0.82);
    }
  </style>

  <div id="root" data-composition-id="dive" data-width="1080" data-height="1920">
    <div id="d-stage" data-layout-allow-overflow data-layout-allow-overlap>
      <div id="d-cam" data-layout-allow-overflow data-layout-allow-overlap>
        <!-- data-depth: px sau mặt phẳng tiêu cự (âm = gần camera hơn). Xếp từ xa đến gần. -->
        <div id="d-map" class="d-layer" data-depth="0">
          <svg id="d-map-svg" width="3240" height="5760" viewBox="-1080 -1920 3240 5760">
            <defs>
              <filter id="d-f-terrain" filterUnits="userSpaceOnUse" x="-1080" y="-1920" width="3240" height="5760">
                <feTurbulence type="fractalNoise" baseFrequency="0.0032" numOctaves="5" seed="4" />
                <feColorMatrix type="matrix"
                  values="0.55 0 0 0 -0.06
                          0.58 0 0 0 -0.04
                          0.42 0 0 0 -0.07
                          0    0 0 0 1" />
              </filter>
            </defs>
            <rect x="-1080" y="-1920" width="3240" height="5760" filter="url(#d-f-terrain)" />
            <g id="d-urban"></g>
            <path d="M-1080 380 C -500 520, 0 760, 160 980 S 420 1500, 980 1560 S 1700 1900, 2160 2300"
              fill="none" stroke="#1d2b33" stroke-width="70" stroke-linecap="round" />
            <path d="M-1080 380 C -500 520, 0 760, 160 980 S 420 1500, 980 1560 S 1700 1900, 2160 2300"
              fill="none" stroke="#2f4652" stroke-width="34" stroke-linecap="round" />
            <g id="d-roads"></g>
            <path id="d-zone" d="M470 1110 L780 1060 L900 1250 L860 1470 L600 1520 L430 1380 Z" />
            <path id="d-route-glow" pathLength="100" stroke-dasharray="100 120" stroke-dashoffset="110"
              d="M250 650 C 330 800, 420 900, 480 1000 S 640 1220, 700 1300 C 760 1420, 820 1600, 900 1750" />
            <path id="d-route-core" pathLength="100" stroke-dasharray="100 120" stroke-dashoffset="110"
              d="M250 650 C 330 800, 420 900, 480 1000 S 640 1220, 700 1300 C 760 1420, 820 1600, 900 1750" />
          </svg>
        </div>
        <div id="d-labels" class="d-layer" data-depth="-30">
          <div id="d-pin-center" class="pin" style="left: 250px; top: 650px">
            <span class="pin-dot"></span><span class="pin-tag">Trung tâm</span>
          </div>
          <div id="d-pin-node" class="pin" style="left: 480px; top: 1000px">
            <span class="pin-dot"></span><span class="pin-tag">Nút giao A</span>
          </div>
          <div id="d-pin-ring" class="pin" style="left: 900px; top: 1750px">
            <span class="pin-dot"></span><span class="pin-tag" style="left: auto; right: 26px">Vành đai 3</span>
          </div>
          <div id="d-zone-tag">Khu Nam</div>
        </div>
        <div id="d-proj" class="d-layer" data-depth="-60">
          <div id="d-card-stem"></div>
          <div id="d-card">
            <span class="card-box"><span class="card-k">KHU ĐÔ THỊ</span><span class="card-name">DỰ ÁN X</span></span>
          </div>
        </div>
        <div id="d-clouds" class="d-layer" data-depth="-350">
          <div id="d-cl-a" class="cloud"></div>
          <div id="d-cl-b" class="cloud"></div>
          <div id="d-cl-c" class="cloud"></div>
          <div id="d-cl-d" class="cloud"></div>
        </div>
      </div>
    </div>

    <div id="h-scrim" data-layout-allow-occlusion></div>
    <div id="h-pill" data-layout-allow-occlusion class="clip" data-start="0.3" data-duration="19.7" data-track-index="2">
      <span id="h-pill-t">Khu Nam · TP.HCM</span>
    </div>
    <h1 id="h-hook" class="h-title clip" data-start="0.2" data-duration="3.9" data-track-index="3">
      <span>Khu</span> <span>Nam</span> <span>sẽ</span> <em><span>thay</span> <span>đổi</span></em> <span>thế</span> <span>nào?</span>
    </h1>
    <h2 id="h-mid" class="h-title clip" data-start="4.9" data-duration="4.7" data-track-index="4">
      <span>Tuyến</span> <span>mới</span> <span>nối</span> <span>thẳng</span> <em><span>vào</span> <span>trung</span> <span>tâm</span></em>
    </h2>
    <h2 id="h-end" class="h-title clip" data-start="15.6" data-duration="4.4" data-track-index="5">
      <span>Thông</span> <span>xe</span> <span>toàn</span> <span>tuyến</span>
      <span class="big">1/10/2026</span>
    </h2>
    <p id="h-source" class="clip" data-start="0" data-duration="20" data-track-index="6" data-layout-ignore>
      <span id="h-source-t">Bản đồ &amp; mốc thời gian minh hoạ — thay bằng nguồn thật</span>
    </p>
  </div>

  <script>
    (() => {
      // ================= CAMERA RIG =================
      const P = 1000;          // = perspective trong CSS
      const W = 1080, H = 1920;
      const DUR = 20;          // = data-duration của host
      const FLOAT = 2.5;       // rung flycam tất định (px); 0 = tắt

      const cam = document.querySelector("#d-cam");
      const layers = [...cam.querySelectorAll(":scope > .d-layer")].map((el) => ({ el, d: parseFloat(el.dataset.depth) }));
      layers.forEach(({ el, d }) => {
        el.style.transform = `translate3d(0px, 0px, ${-d}px) scale(${(P + d) / P})`;
      });

      // (lx, ly) của lớp depth d -> camera x,y để điểm đó vào giữa khung
      const look = (d, lx, ly) => ({ x: ((lx - W / 2) * (P + d)) / P, y: ((ly - H / 2) * (P + d)) / P });
      const at = (t, lx, ly, zoom, tilt = 0, orbit = 0, extra = {}) => ({ t, ...look(0, lx, ly), zoom, tilt, orbit, ...extra });

      // ---- Đường camera. zoom = độ phóng của mặt bản đồ (depth 0); nội suy theo log(zoom)
      // nên tốc độ "lặn" cảm nhận đều. tilt: nghiêng bản đồ như flycam (≤ 12°). orbit: xoay quanh điểm nhìn.
      // stop:true = cố ý dừng (hiếm); carry:true ở key cuối = giữ vận tốc để nối take sau.
      const KEYS = [
        at(0, 560, 980, 0.85, 0, 0),
        at(3.5, 300, 700, 1.8, 6, -2),        // xuyên mây, lặn xuống trung tâm
        at(7, 480, 1000, 1.9, 9, 0),          // cưỡi theo tuyến đang tự vẽ
        at(10.5, 690, 1280, 2.5, 10, 3),      // tới dự án
        at(13, 660, 1240, 2.7, 8, 6),         // orbit chậm quanh dự án, vùng khu vực hiện ra
        at(16.5, 600, 1350, 1.15, 3, 2),      // kéo lùi lộ toàn tuyến (bản đồ dồn lên trên, chừa chỗ cho tiêu đề)
        at(20, 600, 1450, 0.85, 0, -2),       // đáp nhẹ
      ];
      KEYS.forEach((k) => { k.lz = Math.log(k.zoom); });
      const CH = ["x", "y", "lz", "orbit", "tilt"];

      function slopes(ts, vs, stops) {
        const n = ts.length, dl = [], m = new Array(n).fill(0);
        for (let k = 0; k < n - 1; k++) dl[k] = (vs[k + 1] - vs[k]) / (ts[k + 1] - ts[k]);
        m[0] = dl[0];                                       // mở đầu: camera đã đang chạy
        m[n - 1] = KEYS[n - 1].carry ? dl[n - 2] : 0;       // kết: đáp nhẹ, hoặc giữ vận tốc
        for (let k = 1; k < n - 1; k++) m[k] = dl[k - 1] * dl[k] <= 0 ? 0 : (dl[k - 1] + dl[k]) / 2;
        for (let k = 0; k < n - 1; k++) {
          if (dl[k] === 0) { m[k] = 0; m[k + 1] = 0; continue; }
          const a = m[k] / dl[k], b = m[k + 1] / dl[k], s = a * a + b * b;
          if (s > 9) { const tau = 3 / Math.sqrt(s); m[k] = tau * a * dl[k]; m[k + 1] = tau * b * dl[k]; }
        }
        stops.forEach((st, k) => { if (st) m[k] = 0; });
        return m;
      }
      const TS = KEYS.map((k) => k.t);
      const STOPS = KEYS.map((k) => !!k.stop);
      const CURVES = {};
      CH.forEach((c) => { const vs = KEYS.map((k) => k[c] ?? 0); CURVES[c] = { vs, m: slopes(TS, vs, STOPS) }; });

      function sample(t) {
        t = Math.min(Math.max(t, TS[0]), TS[TS.length - 1]);
        let i = 0;
        while (i < TS.length - 2 && t > TS[i + 1]) i++;
        const h = TS[i + 1] - TS[i], s = (t - TS[i]) / h, s2 = s * s, s3 = s2 * s;
        const o = {};
        CH.forEach((c) => {
          const { vs, m } = CURVES[c];
          o[c] = (2 * s3 - 3 * s2 + 1) * vs[i] + (s3 - 2 * s2 + s) * h * m[i] + (-2 * s3 + 3 * s2) * vs[i + 1] + (s3 - s2) * h * m[i + 1];
        });
        o.z = P * (1 - Math.exp(-o.lz));     // zoom -> dolly
        o.x += FLOAT * (Math.sin(2 * Math.PI * 0.13 * t + 1.3) + 0.6 * Math.sin(2 * Math.PI * 0.31 * t + 0.2));
        o.y += FLOAT * 0.7 * (Math.sin(2 * Math.PI * 0.11 * t + 2.1) + 0.5 * Math.sin(2 * Math.PI * 0.27 * t));
        return o;
      }
      function apply(t) {
        const c = sample(t);
        cam.style.transform =
          `translateZ(${c.z}px) rotateX(${c.tilt}deg) rotateZ(${c.orbit}deg) translate3d(${-c.x}px, ${-c.y}px, 0px)`;
        layers.forEach(({ el, d }) => {
          const dist = P + d - c.z;
          el.style.opacity = String(Math.min(1, Math.max(0, (dist - 0.12 * P) / (0.18 * P))));
        });
      }

      // ---- Đường phố & khu đô thị giả lập (thay bằng bản đồ thật). Tất định: mulberry32.
      function mulberry32(a) {
        return () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
          t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
      }
      const NS = "http://www.w3.org/2000/svg";
      const rnd = mulberry32(11);
      const urban = document.querySelector("#d-urban");
      for (let i = 0; i < 140; i++) {
        const cx = 250 + (rnd() - 0.5) * 1500 * Math.sqrt(rnd()), cy = 700 + (rnd() - 0.4) * 1900 * Math.sqrt(rnd());
        const e = document.createElementNS(NS, "ellipse");
        e.setAttribute("cx", cx.toFixed(0)); e.setAttribute("cy", cy.toFixed(0));
        e.setAttribute("rx", (40 + rnd() * 140).toFixed(0)); e.setAttribute("ry", (30 + rnd() * 110).toFixed(0));
        e.setAttribute("fill", `rgba(${150 + rnd() * 40 | 0},${150 + rnd() * 30 | 0},${140 + rnd() * 30 | 0},${(0.06 + rnd() * 0.1).toFixed(2)})`);
        urban.appendChild(e);
      }
      const roads = document.querySelector("#d-roads");
      for (let i = 0; i < 120; i++) {
        let x = -900 + rnd() * 2900, y = -1700 + rnd() * 5300, a = rnd() * Math.PI * 2;
        let d = `M${x.toFixed(0)} ${y.toFixed(0)}`;
        for (let k = 0; k < 7; k++) {
          a += (rnd() - 0.5) * 0.7; x += Math.cos(a) * (120 + rnd() * 220); y += Math.sin(a) * (120 + rnd() * 220);
          d += ` L${x.toFixed(0)} ${y.toFixed(0)}`;
        }
        const p = document.createElementNS(NS, "path");
        p.setAttribute("d", d); p.setAttribute("fill", "none");
        p.setAttribute("stroke", `rgba(225,222,210,${(0.18 + rnd() * 0.25).toFixed(2)})`);
        p.setAttribute("stroke-width", (2 + rnd() * 5).toFixed(1)); p.setAttribute("stroke-linejoin", "round");
        roads.appendChild(p);
      }

      // ================= TIMELINE =================
      const tl = gsap.timeline({ paused: true });
      const clock = { t: 0 };
      tl.fromTo(clock, { t: 0 }, { t: DUR, duration: DUR, ease: "none", onUpdate: () => apply(clock.t) }, 0);
      apply(0);

      const wordsIn = (sel, at, gap = 0.08) => tl.fromTo(`${sel} span`, { opacity: 0, filter: "blur(10px)", scale: 1.08 },
        { opacity: 1, filter: "blur(0px)", scale: 1, duration: 0.18, ease: "power4.out", stagger: gap }, at);
      const wordsOut = (sel, at) => tl.to(`${sel} span`, { opacity: 0, filter: "blur(10px)", duration: 0.18, ease: "power2.in", stagger: 0.03 }, at);
      const pop = (sel, at) => tl.fromTo(sel, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.6)" }, at);

      // Mây chỉ xuất hiện lúc mở đầu (camera bay xuyên); không quay lại khi kéo lùi
      tl.to(".cloud", { opacity: 0, duration: 1.2, ease: "power1.in" }, 4.2);
      tl.fromTo("#h-pill-t", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }, 0.3);
      wordsIn("#h-hook", 0.25, 0.07);
      wordsOut("#h-hook", 3.9);

      // Tuyến tự vẽ trong lúc camera cưỡi theo: đoạn tới dự án (≈62% chiều dài), rồi phần còn lại khi kéo lùi
      ["#d-route-glow", "#d-route-core"].forEach((s) => {
        tl.fromTo(s, { strokeDashoffset: 110 }, { strokeDashoffset: 38, duration: 6.8, ease: "power1.inOut" }, 3.8);
        tl.to(s, { strokeDashoffset: 0, duration: 2.6, ease: "power2.inOut" }, 13.2);
      });
      pop("#d-pin-center", 2.6);
      pop("#d-pin-node", 6.3);
      wordsIn("#h-mid", 4.9, 0.08);
      wordsOut("#h-mid", 9.4);

      tl.fromTo("#d-card-stem", { scaleY: 0, transformOrigin: "50% 100%" }, { scaleY: 1, duration: 0.3, ease: "power3.out" }, 9.6);
      tl.fromTo("#d-card .card-box", { opacity: 0, y: 40, scale: 0.85 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "back.out(1.5)" }, 9.75);
      tl.fromTo("#d-zone", { opacity: 0 }, { opacity: 1, duration: 0.9, ease: "power2.out" }, 11);
      pop("#d-zone-tag", 11.4);
      pop("#d-pin-ring", 14.6);

      wordsIn("#h-end", 15.6, 0.08);
      tl.fromTo("#h-source-t", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.6);

      window.__timelines["dive"] = tl;
    })();
  </script>
</template>
```

## FILE: templates/map-dive-parallax/index.html

```html
<!doctype html>
<html
  lang="vi"
  data-composition-variables='[
    {"id":"color-ground","type":"color","label":"Nền","default":"#101210"},
    {"id":"color-ink","type":"color","label":"Chữ","default":"#ffffff"},
    {"id":"color-accent","type":"color","label":"Nhấn (vàng)","default":"#ffd23f"},
    {"id":"color-route","type":"color","label":"Tuyến đường (cam)","default":"#ff7a1a"},
    {"id":"color-pill","type":"color","label":"Nhãn đầu trang","default":"#2f5bd3"},
    {"id":"color-zone","type":"color","label":"Vùng khu vực","default":"#3ccf7a"},
    {"id":"font-display","type":"string","label":"Font tiêu đề","default":"Montserrat"}
  ]'
>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {
        --color-ground: #101210;
        --color-ink: #ffffff;
        --color-accent: #ffd23f;
        --color-route: #ff7a1a;
        --color-pill: #2f5bd3;
        --color-zone: #3ccf7a;
        --font-display: "Montserrat";
      }
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      html,
      body {
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: var(--color-ground);
      }
      #ground {
        position: absolute;
        inset: 0;
        background: var(--color-ground);
      }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="20"
      data-width="1080"
      data-height="1920"
    >
      <div id="ground"></div>
      <!-- Một take = một cú máy liền. Nối nhiều take: references/camera-rig.md §6 (cinematic-zoom / match-move). -->
      <div
        id="dive"
        data-composition-id="dive"
        data-composition-src="compositions/dive.html"
        data-start="0"
        data-duration="20"
        data-track-index="1"
        data-track-kind="graphics"
        data-width="1080"
        data-height="1920"
      ></div>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
```

## FILE: templates/ngang-parallax/assets/README.md

```markdown
# assets/

Đặt ở đây ảnh tách lớp (PNG nền trong suốt), video bản đồ đã bake, nhạc, font.
Đường dẫn trong HTML luôn là `assets/...` (không có `/` ở đầu).
Gợi ý đặt tên: `L3000-troi.png`, `L1800-skyline-xa.png`, `L900-khoi-giua.png`, `L300-du-an.png`, `L-350-tien-canh.png`
(số đầu = data-depth của lớp sẽ chứa ảnh).
```

## FILE: templates/ngang-parallax/compositions/world.html

```html
<template>
  <style>
    #root {
      position: absolute;
      inset: 0;
      overflow: hidden;
      font-family: var(--font-display), "Montserrat", sans-serif;
      color: var(--color-ink);
    }

    /* ---------- CAMERA RIG ----------
       #w-stage: ống kính (perspective). #w-cam: toàn bộ thế giới, chỉ JS đặt transform.
       KHÔNG đặt opacity < 1, filter, overflow:hidden, mix-blend-mode, clip-path lên
       #w-stage / #w-cam: Chrome sẽ làm phẳng 3D và mất parallax. */
    #w-stage {
      position: absolute;
      inset: 0;
      perspective: 1000px; /* = P trong script, đổi cả hai cùng lúc */
      perspective-origin: 50% 50%;
    }
    #w-cam {
      position: absolute;
      left: 0;
      top: 0;
      width: 1920px;
      height: 1080px;
      transform-style: preserve-3d;
      transform-origin: 960px 540px 0;
    }
    .w-layer {
      position: absolute;
      left: 0;
      top: 0;
      width: 1920px;
      height: 1080px;
      transform-origin: 960px 540px 0;
    }
    .w-layer > * {
      position: absolute;
    }

    /* ---------- LỚP NỀN (thay bằng PNG tách lớp của bạn) ---------- */
    #w-sky-fill {
      left: -6000px;
      top: -3000px;
      width: 16000px;
      height: 8000px;
      background: radial-gradient(
          ellipse 1800px 900px at 6300px 3500px,
          rgba(242, 181, 68, 0.35),
          rgba(242, 181, 68, 0) 70%
        ),
        linear-gradient(180deg, #16233a 0%, #2b3b58 38%, #8a6f62 47%, #2b3b58 49%, #1a2638 100%);
    }
    #w-far-svg,
    #w-mid-svg {
      left: -1600px;
      top: 0;
    }
    #w-haze-fill {
      left: -4000px;
      top: 380px;
      width: 14000px;
      height: 900px;
      background: linear-gradient(180deg, rgba(43, 59, 88, 0) 0%, rgba(120, 128, 150, 0.28) 45%, rgba(43, 59, 88, 0) 100%);
    }

    /* Toà nhà chính (hero) + nhãn giá gắn vào thế giới */
    #w-hero-bld {
      left: 2850px;
      top: 300px;
      width: 300px;
      height: 1600px;
      background: repeating-linear-gradient(
          180deg,
          rgba(255, 214, 140, 0.55) 0 10px,
          rgba(0, 0, 0, 0) 10px 34px
        ),
        linear-gradient(90deg, #1d2a40 0%, #2f4466 55%, #1a2538 100%);
      background-size: 100% 100%, 100% 100%;
      border-top: 6px solid var(--color-accent);
    }
    #w-hero-tag {
      left: 2780px;
      top: 120px;
      width: 440px;
      text-align: center;
    }
    #w-hero-tag .tag-box {
      display: inline-block;
      padding: 18px 30px 20px;
      background: rgba(13, 20, 32, 0.86);
      border: 3px solid var(--color-accent);
      border-radius: 14px;
    }
    #w-hero-tag .tag-k {
      display: block;
      font-size: 24px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      opacity: 0.8;
    }
    #w-hero-num {
      display: block;
      font-size: 84px;
      font-weight: 900;
      color: var(--color-accent);
      font-variant-numeric: tabular-nums;
      line-height: 1.05;
    }
    #w-hero-stem {
      left: 2998px;
      top: 262px;
      width: 4px;
      height: 40px;
      background: var(--color-accent);
    }

    /* Biểu đồ đặt TRONG thế giới (depth 0): camera bay tới nó, đường giá là "con đường" */
    #w-chart-panel {
      left: 4990px;
      top: 150px;
      width: 1220px;
      height: 700px;
      border-radius: 22px;
      background: rgba(10, 16, 27, 0.82);
      border: 2px solid rgba(244, 241, 234, 0.12);
    }
    #w-chart {
      left: 5050px;
      top: 250px;
      width: 1100px;
      height: 560px;
    }
    #w-chart .axis {
      stroke: rgba(244, 241, 234, 0.35);
      stroke-width: 2;
    }
    #w-chart-line {
      fill: none;
      stroke: var(--color-accent);
      stroke-width: 9;
      stroke-linecap: round;
      stroke-linejoin: round;
    }
    #w-chart-area {
      fill: rgba(242, 181, 68, 0.14);
    }
    #w-chart .yr {
      font-size: 34px;
      font-weight: 700;
      fill: rgba(244, 241, 234, 0.7);
    }
    #w-chart-end {
      left: 5970px;
      top: 200px;
      font-size: 54px;
      font-weight: 900;
      color: var(--color-accent);
      font-variant-numeric: tabular-nums;
    }

    /* Tiền cảnh: cột/cây tối, đi qua khung hình rất nhanh = parallax mạnh + che mối nối */
    .fg-pillar {
      background: linear-gradient(90deg, #05080d 0%, #111a28 60%, #05080d 100%);
    }
    #w-fg-a {
      left: 1560px;
      top: -400px;
      width: 200px;
      height: 2200px;
    }
    #w-fg-b {
      left: 6830px;
      top: -500px;
      width: 260px;
      height: 2400px;
    }

    /* ---------- HUD (khoá theo màn hình, không đi theo camera) ---------- */
    .hud-title {
      position: absolute;
      left: 160px;
      top: 150px;
      width: 1400px;
      font-size: 92px;
      font-weight: 900;
      line-height: 1.04;
      letter-spacing: -0.02em;
    }
    .hud-title span,
    .hud-kicker span {
      display: inline-block;
    }
    .hud-title em {
      font-style: normal;
      color: var(--color-accent);
    }
    .hud-kicker {
      position: absolute;
      left: 160px;
      bottom: 150px;
      font-size: 40px;
      font-weight: 700;
    }
    #hud-chart-title {
      top: 110px;
      font-size: 58px;
    }
    #hud-close {
      top: auto;
      bottom: 110px;
      font-size: 84px;
    }
    #hud-source {
      position: absolute;
      right: 120px;
      bottom: 64px;
      padding: 6px 14px;
      font-size: 22px;
      background: rgba(5, 8, 13, 0.6);
      border-radius: 6px;
      opacity: 0.85;
    }
  </style>

  <div id="root" data-composition-id="world" data-width="1920" data-height="1080">
    <div id="w-stage" data-layout-allow-overflow data-layout-allow-overlap>
      <div id="w-cam" data-layout-allow-overflow data-layout-allow-overlap>
        <!-- data-depth: px phía sau mặt phẳng tiêu cự (âm = tiền cảnh). Xếp từ xa đến gần. -->
        <div id="w-sky" class="w-layer" data-depth="3000"><div id="w-sky-fill"></div></div>
        <div id="w-far" class="w-layer" data-depth="1800" data-seed="7" data-skyline="far">
          <svg id="w-far-svg" width="11000" height="3200"></svg>
        </div>
        <div id="w-haze" class="w-layer" data-depth="1350"><div id="w-haze-fill"></div></div>
        <div id="w-mid" class="w-layer" data-depth="900" data-seed="21" data-skyline="mid">
          <svg id="w-mid-svg" width="12000" height="3200"></svg>
        </div>
        <div id="w-hero" class="w-layer" data-depth="300">
          <div id="w-hero-bld"></div>
          <div id="w-hero-stem"></div>
          <div id="w-hero-tag">
            <span class="tag-box">
              <span class="tag-k">Giá TB / m² · 12 tháng</span>
              <span id="w-hero-num">+0,0%</span>
            </span>
          </div>
        </div>
        <div id="w-plane" class="w-layer" data-depth="0">
          <div id="w-chart-panel"></div>
          <svg id="w-chart" viewBox="0 0 1100 560">
            <line class="axis" x1="40" y1="500" x2="1080" y2="500" />
            <path id="w-chart-area" d="M60 430 L220 405 L380 380 L540 395 L700 330 L860 250 L1040 150 L1040 500 L60 500 Z" />
            <path id="w-chart-line" pathLength="100" stroke-dasharray="100 120" stroke-dashoffset="110"
              d="M60 430 L220 405 L380 380 L540 395 L700 330 L860 250 L1040 150" />
            <text class="yr" x="60" y="545" text-anchor="middle">2019</text>
            <text class="yr" x="540" y="545" text-anchor="middle">2022</text>
            <text class="yr" x="1040" y="545" text-anchor="middle">2026</text>
          </svg>
          <div id="w-chart-end">×1,9</div>
        </div>
        <div id="w-fg" class="w-layer" data-depth="-350">
          <div id="w-fg-a" class="fg-pillar"></div>
          <div id="w-fg-b" class="fg-pillar"></div>
        </div>
      </div>
    </div>

    <!-- HUD: clip có thời gian; chỉ animate phần tử con -->
    <h1 id="hud-hook" class="hud-title clip" data-start="0.5" data-duration="4.4" data-track-index="2">
      <span>Giá</span> <span>căn</span> <span>hộ</span> <span>sẽ</span> <span>đi</span> <span>về</span> <em><span>đâu?</span></em>
    </h1>
    <p id="hud-kicker" class="hud-kicker clip" data-start="7.2" data-duration="3.8" data-track-index="3">
      <span>Khu trung tâm</span> <span>·</span> <span>giá bán trung bình</span>
    </p>
    <h2 id="hud-chart-title" class="hud-title clip" data-start="12.8" data-duration="4.2" data-track-index="4">
      <span>Giá</span> <span>căn</span> <span>hộ</span> <span>2019–2026</span>
    </h2>
    <h2 id="hud-close" class="hud-title clip" data-start="17.4" data-duration="2.6" data-track-index="5">
      <span>Cung</span> <span>thiếu,</span> <em><span>giá</span> <span>giữ</span> <span>đà</span> <span>tăng</span></em>
    </h2>
    <p id="hud-source" class="clip" data-start="7" data-duration="13" data-track-index="6" data-layout-ignore>
      <span id="hud-source-t">Số liệu minh hoạ — thay bằng nguồn thật</span>
    </p>
  </div>

  <script>
    (() => {
      // ================= CAMERA RIG =================
      const P = 1000; // = perspective trong CSS
      const W = 1920, H = 1080;
      const DUR = 20; // = data-duration của host
      const FLOAT = 3; // biên độ "drone float" (px). 0 = tắt.

      const cam = document.querySelector("#w-cam");
      const layers = [...cam.querySelectorAll(":scope > .w-layer")].map((el) => ({
        el,
        d: parseFloat(el.dataset.depth),
      }));

      // Bù tỉ lệ: phần tử trong lớp có depth d hiện đúng kích thước thiết kế khi camera ở gốc.
      layers.forEach(({ el, d }) => {
        el.style.transform = `translate3d(0px, 0px, ${-d}px) scale(${(P + d) / P})`;
      });

      // Điểm (lx, ly) trong lớp có depth d -> toạ độ camera để đặt nó vào giữa khung.
      const look = (d, lx, ly) => ({ x: ((lx - W / 2) * (P + d)) / P, y: ((ly - H / 2) * (P + d)) / P });

      // ---- Đường camera: các KEY nội suy Hermite đơn điệu, vận tốc liên tục.
      // x,y: pan (px trên mặt phẳng tiêu cự)  z: dolly (+ tiến vào, − lùi ra)
      // orbit/tilt: xoay quanh điểm nhìn (độ). stop:true = cố ý dừng (hiếm).
      // Key cuối mặc định "đáp" nhẹ; carry:true ở key cuối = giữ vận tốc (nối match-move sang take sau).
      const hero = look(300, 3000, 430);
      const chart = look(0, 5600, 560);
      const KEYS = [
        { t: 0, x: -300, y: -120, z: -150, orbit: -4, tilt: 2 },
        { t: 4, x: 700, y: -40, z: 60, orbit: -1, tilt: 1 },
        { t: 8, x: hero.x, y: hero.y, z: 380, orbit: 3, tilt: 0 },
        { t: 11, x: 3900, y: 0, z: 250, orbit: 1, tilt: 0 },
        { t: 14, x: chart.x, y: chart.y, z: 180, orbit: 0, tilt: 0 },
        { t: 17, x: chart.x + 380, y: 60, z: 230, orbit: -1, tilt: 0 },
        { t: 20, x: chart.x + 600, y: 40, z: -250, orbit: -3, tilt: 1 },
      ];
      const CH = ["x", "y", "z", "orbit", "tilt"];

      function slopes(ts, vs, stops) {
        const n = ts.length, dl = [], m = new Array(n).fill(0);
        for (let k = 0; k < n - 1; k++) dl[k] = (vs[k + 1] - vs[k]) / (ts[k + 1] - ts[k]);
        m[0] = dl[0];
        m[n - 1] = KEYS[n - 1].carry ? dl[n - 2] : 0; // cuối: đáp nhẹ, hoặc giữ vận tốc để nối take
        for (let k = 1; k < n - 1; k++) m[k] = dl[k - 1] * dl[k] <= 0 ? 0 : (dl[k - 1] + dl[k]) / 2;
        for (let k = 0; k < n - 1; k++) {
          if (dl[k] === 0) { m[k] = 0; m[k + 1] = 0; continue; }
          const a = m[k] / dl[k], b = m[k + 1] / dl[k];
          const s = a * a + b * b;
          if (s > 9) { const tau = 3 / Math.sqrt(s); m[k] = tau * a * dl[k]; m[k + 1] = tau * b * dl[k]; }
        }
        stops.forEach((st, k) => { if (st) m[k] = 0; });
        return m;
      }
      const TS = KEYS.map((k) => k.t);
      const STOPS = KEYS.map((k) => !!k.stop);
      const CURVES = {};
      CH.forEach((c) => {
        const vs = KEYS.map((k) => k[c] ?? 0);
        CURVES[c] = { vs, m: slopes(TS, vs, STOPS) };
      });
      function sample(t) {
        t = Math.min(Math.max(t, TS[0]), TS[TS.length - 1]);
        let i = 0;
        while (i < TS.length - 2 && t > TS[i + 1]) i++;
        const h = TS[i + 1] - TS[i], s = (t - TS[i]) / h, s2 = s * s, s3 = s2 * s;
        const out = {};
        CH.forEach((c) => {
          const { vs, m } = CURVES[c];
          out[c] = (2 * s3 - 3 * s2 + 1) * vs[i] + (s3 - 2 * s2 + s) * h * m[i] +
            (-2 * s3 + 3 * s2) * vs[i + 1] + (s3 - s2) * h * m[i + 1];
        });
        // drone float: tổng sin cố định pha -> tất định, không dùng Math.random
        out.x += FLOAT * (Math.sin(2 * Math.PI * 0.13 * t + 1.3) + 0.6 * Math.sin(2 * Math.PI * 0.31 * t + 0.2));
        out.y += FLOAT * 0.7 * (Math.sin(2 * Math.PI * 0.11 * t + 2.1) + 0.5 * Math.sin(2 * Math.PI * 0.27 * t));
        return out;
      }
      function apply(t) {
        const c = sample(t);
        cam.style.transform =
          `translateZ(${c.z}px) rotateX(${c.tilt}deg) rotateY(${c.orbit}deg) translate3d(${-c.x}px, ${-c.y}px, 0px)`;
        // Bay xuyên: lớp sắp chạm ống kính mờ dần thay vì phóng to vô hạn
        layers.forEach(({ el, d }) => {
          const dist = P + d - c.z;
          el.style.opacity = String(Math.min(1, Math.max(0, (dist - 0.12 * P) / (0.18 * P))));
        });
      }

      // ---- Skyline giả lập có seed (thay bằng ảnh thật). Tất định: mulberry32.
      function mulberry32(a) {
        return () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
          t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
      }
      const NS = "http://www.w3.org/2000/svg";
      cam.querySelectorAll("[data-skyline]").forEach((layer) => {
        const svg = layer.querySelector("svg");
        const far = layer.dataset.skyline === "far";
        const rnd = mulberry32(parseInt(layer.dataset.seed, 10));
        const base = far ? 700 : 860;
        let x = 0;
        while (x < parseFloat(svg.getAttribute("width"))) {
          const w = (far ? 70 : 110) + rnd() * (far ? 140 : 220);
          const h = (far ? 60 : 110) + Math.pow(rnd(), 1.8) * (far ? 240 : 380);
          const r = document.createElementNS(NS, "rect");
          r.setAttribute("x", x.toFixed(1));
          r.setAttribute("y", (base - h).toFixed(1));
          r.setAttribute("width", (w - (far ? 6 : 14)).toFixed(1));
          r.setAttribute("height", (h + 2600).toFixed(1));
          r.setAttribute("fill", far ? "#3b4a66" : "#1f2c42"); // xa: sáng & xanh hơn (phối cảnh khí quyển)
          svg.appendChild(r);
          if (!far) {
            for (let wy = base - h + 24; wy < base + 200; wy += 34) {
              if (rnd() < 0.45) continue;
              const win = document.createElementNS(NS, "rect");
              win.setAttribute("x", (x + 12 + rnd() * (w - 50)).toFixed(1));
              win.setAttribute("y", wy.toFixed(1));
              win.setAttribute("width", "14");
              win.setAttribute("height", "10");
              win.setAttribute("fill", "rgba(255,214,140,0.55)");
              svg.appendChild(win);
            }
          }
          x += w;
        }
      });

      // ================= TIMELINE =================
      const tl = gsap.timeline({ paused: true });
      const clock = { t: 0 };
      tl.fromTo(clock, { t: 0 }, { t: DUR, duration: DUR, ease: "none", onUpdate: () => apply(clock.t) }, 0);
      apply(0);

      // Chữ vào từng từ bằng blur, đứng yên khi đã đáp, ra bằng blur ngắn.
      const wordsIn = (sel, at, gap = 0.08) => tl.fromTo(`${sel} span`, { opacity: 0, filter: "blur(8px)" },
        { opacity: 1, filter: "blur(0px)", duration: 0.16, ease: "power4.out", stagger: gap }, at);
      const wordsOut = (sel, at) => tl.to(`${sel} span`, { opacity: 0, filter: "blur(8px)", duration: 0.18,
        ease: "power2.in", stagger: 0.03 }, at);

      wordsIn("#hud-hook", 0.5, 0.09);
      wordsOut("#hud-hook", 4.45);

      // Nhãn giá gắn vào toà nhà (world-locked): nổi lên khi camera tới, đếm số 1,4 s rồi đứng yên.
      tl.fromTo("#w-hero-tag .tag-box", { opacity: 0, y: 30, scale: 0.92 },
        { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "expo.out" }, 6.9);
      tl.fromTo("#w-hero-stem", { scaleY: 0, transformOrigin: "50% 100%" }, { scaleY: 1, duration: 0.3, ease: "power3.out" }, 6.8);
      const num = document.querySelector("#w-hero-num");
      const cnt = { v: 0 };
      tl.fromTo(cnt, { v: 0 }, { v: 12.4, duration: 1.4, ease: "power2.out",
        onUpdate: () => { num.textContent = "+" + cnt.v.toFixed(1).replace(".", ",") + "%"; } }, 7.1);

      wordsIn("#hud-kicker", 7.2, 0.1);
      wordsOut("#hud-kicker", 10.7);

      // Biểu đồ: đường giá tự vẽ trong lúc camera trượt dọc theo nó.
      tl.fromTo("#w-chart-area", { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "power2.out" }, 12.6);
      tl.fromTo("#w-chart-line", { strokeDashoffset: 110 }, { strokeDashoffset: 0, duration: 3.2, ease: "power2.inOut" }, 12.6);
      tl.fromTo("#w-chart-end", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, 15.7);
      wordsIn("#hud-chart-title", 12.8, 0.08);
      wordsOut("#hud-chart-title", 16.75);

      wordsIn("#hud-close", 17.4, 0.09);
      tl.fromTo("#hud-source-t", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 7);

      window.__timelines["world"] = tl;
    })();
  </script>
</template>
```

## FILE: templates/ngang-parallax/index.html

```html
<!doctype html>
<html
  lang="vi"
  data-composition-variables='[
    {"id":"color-ground","type":"color","label":"Nền","default":"#0d1420"},
    {"id":"color-ink","type":"color","label":"Chữ","default":"#f4f1ea"},
    {"id":"color-accent","type":"color","label":"Nhấn (tăng giá)","default":"#f2b544"},
    {"id":"color-down","type":"color","label":"Nhấn (giảm giá)","default":"#e5484d"},
    {"id":"font-display","type":"string","label":"Font tiêu đề","default":"Montserrat"}
  ]'
>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {
        --color-ground: #0d1420;
        --color-ink: #f4f1ea;
        --color-accent: #f2b544;
        --color-down: #e5484d;
        --font-display: "Montserrat";
      }
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      html,
      body {
        width: 1920px;
        height: 1080px;
        overflow: hidden;
        background: var(--color-ground);
      }
      #ground {
        position: absolute;
        inset: 0;
        background: var(--color-ground);
      }
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="20"
      data-width="1920"
      data-height="1080"
    >
      <div id="ground"></div>
      <!-- Một cảnh = một "take" camera liên tục. Nhiều take: thêm host mới, nối bằng match-move (references/camera-rig.md §6). -->
      <div
        id="world"
        data-composition-id="world"
        data-composition-src="compositions/world.html"
        data-start="0"
        data-duration="20"
        data-track-index="1"
        data-track-kind="graphics"
        data-width="1920"
        data-height="1080"
      ></div>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
```

## FILE: templates/one-era-flight/README.md

```markdown
# One Era · "phép tính 25%" — phong cách C (một camera, một bản đồ)

Dọc 1080×1920, 30 fps, 260,23 s, 15 chương, 71 keyframe camera, 0 cắt cứng, footage 5 lần × ≤ 2,9 s (5%).
Đọc `references/flight-style.md` trước.

1. Bản đồ: `geo_build.py` (tỉnh, đường, kênh, ranh dự án) → `python prep_geo.py <thư mục dữ liệu>` thêm biên giới Hoa Kỳ/Việt Nam
   (Natural Earth 10m), đại lộ nội khu minh hoạ, vùng xanh, và `blocks.json` — 60 khối minh hoạ phủ đúng 25% diện tích ranh.
2. Nền vệ tinh: `sat_tiles.py` — w03 (z3 cả thế giới), a05 (z5 châu Á 47°N–14°S, 82–140°E), sat07 (27…−7°, 90–124°),
   sat09 (16,5…4,5°, 101,5–112,5°), sat11/13/16 quanh dự án; xoá mây (`sat_declouds.py`) rồi chỉnh màu −20% sáng, −15% bão hoà.
3. `python mk_flight.py` → `proj/flight.json`; `python flight.py proj/flight.json proj` → hết "!" ; xem `CAMLOG.md`.
4. `python mk_sfx3.py proj/flight.json proj/sfx/events.json`; `make_music.py music.wav --dur 260.3 --bpm 96`;
   `mix_audio.py assets/vo.mp3 sfx/events.json assets/mix.wav --duration 260.23 --music music.wav`.
5. `npx hyperframes check`, `snapshot`, `render`.

Minh hoạ (ghi trên màn hình): khối nhà và vị trí One Park/Central District/ghim tiện ích/đại lộ 25 m; vị trí Hyde Park;
lượng người đi bộ; bán kính đi bộ 80 m/phút. Số liệu: CafeF, Báo Đầu tư, VnExpress/Znews (Fitwel 3 sao), The Leader (Longfor).
```

## FILE: templates/one-era-flight/blocks.json

```json
[{"lng": 106.698878, "lat": 10.966774, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.69864, "lat": 10.967181, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.699116, "lat": 10.966366, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.698149, "lat": 10.966358, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.699607, "lat": 10.96719, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.698402, "lat": 10.967588, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.699354, "lat": 10.965959, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.697911, "lat": 10.966765, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.699845, "lat": 10.966782, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.699369, "lat": 10.967597, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.698387, "lat": 10.96595, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.697673, "lat": 10.967172, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.699131, "lat": 10.968004, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.698624, "lat": 10.965543, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.700083, "lat": 10.966375, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.698164, "lat": 10.967995, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.697435, "lat": 10.967579, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.698893, "lat": 10.968411, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.70032, "lat": 10.965968, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.700336, "lat": 10.967606, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.69742, "lat": 10.965942, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.700574, "lat": 10.967198, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.700098, "lat": 10.968013, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.697658, "lat": 10.965534, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.697182, "lat": 10.966349, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.697926, "lat": 10.968403, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.69986, "lat": 10.96842, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.697895, "lat": 10.965127, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.696944, "lat": 10.966756, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.700812, "lat": 10.966791, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.697197, "lat": 10.967987, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.698655, "lat": 10.968819, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.701049, "lat": 10.966384, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.699622, "lat": 10.968827, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.696706, "lat": 10.967163, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.701065, "lat": 10.968022, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.699384, "lat": 10.969235, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.696468, "lat": 10.967571, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.701287, "lat": 10.965977, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.700827, "lat": 10.968429, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.701303, "lat": 10.967614, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.701541, "lat": 10.967207, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.700589, "lat": 10.968836, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.696215, "lat": 10.96634, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.701779, "lat": 10.9668, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.695977, "lat": 10.966747, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.700351, "lat": 10.969243, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.701525, "lat": 10.965569, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.700113, "lat": 10.969651, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.695739, "lat": 10.967155, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.702016, "lat": 10.966393, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.701794, "lat": 10.968438, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.702032, "lat": 10.96803, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.701556, "lat": 10.968845, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.702254, "lat": 10.965985, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.701318, "lat": 10.969252, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.695486, "lat": 10.965924, "w": 80, "d": 28, "ang": -30, "g": "cd"}, {"lng": 106.70227, "lat": 10.967623, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.70108, "lat": 10.969659, "w": 80, "d": 28, "ang": -30, "g": "ot"}, {"lng": 106.702508, "lat": 10.967216, "w": 80, "d": 28, "ang": -30, "g": "ot"}]
```

## FILE: templates/one-era-flight/mk_flight.py

```python
"""Kế hoạch bay — One Era · "phép tính 25%" (phong cách C: một camera, một bản đồ)."""
import json
M = lambda n: json.load(open(f"maps/{n}.json"))
SAT = []
for n, show in [("w03", None), ("a05", [3.6, 4.6]), ("sat07", [5.6, 6.4]), ("sat09", [8.3, 9.0]), ("sat11", [9.8, 10.6]), ("sat13", [11.8, 12.6]), ("sat16", [14.0, 14.8])]:
    m = M(n); SAT.append(dict(img=f"assets/maps/{n}_g.jpg", z=m["z"], x0=m["x0"], y0=m["y0"], w=m["w"], h=m["h"], show=show))
OE = [10.9666, 106.6985]; PARK = [10.9652, 106.6962]; CD = [10.9660, 106.6975]; BLVD = [10.96780, 106.69912]
PTS = {"oneera": [106.6985, 10.9666], "site_n": [106.6995, 10.9702], "site_s": [106.6975, 10.9630], "site_w": [106.6928, 10.9652], "site_e": [106.7035, 10.9683],
       "park": [106.6962, 10.9652], "cd": [106.6975, 10.9660], "cd_n": [106.6978, 10.9682], "blvd_mid": [106.69912, 10.96780],
       "hcm": [106.70, 10.78], "hcm_t": [106.70, 10.86], "vn": [106.3, 15.8],
       "atl": [-84.33, 33.80], "dc": [-77.03, 38.90], "ny": [-74.00, 40.71], "hk": [114.17, 22.30], "sg": [103.85, 1.29],
       "hyde": [106.7120, 10.9690], "r400": [106.6962, 10.96882], "r800": [106.6962, 10.97244], "r800w": [106.68888, 10.9652], "q_title": [106.6968, 10.9738],
       "canal_n": [106.70087, 10.97894], "canal_m": [106.70251, 10.96977], "canal_s": [106.70746, 10.96276],
       "p_vas": [106.7008, 10.9690], "p_kind": [106.6992, 10.9679], "p_meret": [106.7026, 10.9674], "p_sport": [106.7032, 10.9659],
       "p_tttm": [106.6948, 10.9648], "p_off": [106.6936, 10.9641], "d1": [106.6930, 10.9650], "d2": [106.7030, 10.9682]}
O = lambda t, z, p=0, b=0, ll=OE: [t, ll[0], ll[1], z, p, b]
cam = [
    # 1 · V2 mở đầu: từ mây xuống Việt Nam → TP.HCM
    [0.0, 13.6, 106.4, 5.2, 0, 0], [3.6, 12.0, 106.6, 6.6, 0, 0], [7.8, 10.86, 106.72, 8.9, 0, 0], [10.6, 10.88, 106.71, 9.5, 12, 0],
    # 2 · V1 bay tới Thuận Giao, vẽ ranh, nghiêng 3D
    [12.6, 10.935, 106.705, 11.3, 18, 0], O(14.8, 14.7, 26), O(17.2, 15.6, 44, -6), O(20.2, 15.85, 48, 4),
    # 3 · V6 khối nhà mọc (25%) → zoom-through phối cảnh
    O(23.4, 16.0, 50, 12), O(27.6, 16.15, 50, 22), O(29.9, 16.9, 40, 24), O(32.6, 17.05, 38, 25),
    # 4 · V8 3/4 khu đất tô xanh, quay chậm
    O(35.2, 16.0, 44, 30), O(40.5, 15.8, 42, 42), O(46.8, 15.45, 30, 48),
    # 5 · V2 Fitwel: thẻ ở dự án → bay ra thế giới → Hoa Kỳ
    O(50.6, 15.1, 12, 22), O(54.0, 15.3, 0, 2), O(56.4, 13.8, 0, 0), [58.6, 24.0, 40.0, 3.25, 0, 0], [61.0, 27.0, -60.0, 3.35, 0, 0],
    [63.6, 37.0, -84.0, 4.45, 0, 0], [66.8, 37.4, -83.0, 4.6, 0, 0],
    # 6 · V4 quay về dự án, vòng đi bộ 5/10 phút quanh One Park
    [69.4, 26.0, -40.0, 3.3, 0, 0], [71.8, 22.0, 60.0, 3.3, 0, 0], [74.0, 11.2, 106.6, 9.8, 0, 0], O(76.4, 15.4, 24, 0, PARK),
    O(81.0, 15.6, 38, 8, PARK), O(85.6, 15.75, 40, 14, PARK), O(89.4, 15.9, 34, 6, PARK),
    # 7 · V3 đi dọc kênh Suối Cát (camera bám đầu tuyến) → One Park → zoom-through
    [91.6, 10.9760, 106.7012, 16.3, 34, 0], [95.0, 10.9720, 106.7020, 16.4, 34, -4], [98.6, 10.9655, 106.7045, 16.4, 34, -8],
    O(102.0, 16.5, 40, -4, PARK), O(104.8, 17.2, 36, 0, PARK), O(108.3, 17.35, 34, 2, PARK),
    # 8 · V5 so diện tích thật: One Park 1 ha · Hyde Park ~42 ha · One Era 49,5 ha
    [111.0, 10.9682, 106.7040, 14.75, 18, 0], [115.4, 10.9684, 106.7045, 14.55, 24, 0],
    # 9 · V7 thả ghim tiện ích, quay chậm
    [118.0, 10.9668, 106.6990, 15.75, 40, -2], [123.5, 10.9668, 106.6990, 15.9, 45, 18], [129.0, 10.9668, 106.6990, 16.0, 45, 30],
    # 10 · V6 357 căn Central District → zoom-through nhà phố → đại lộ 25 m
    O(133.5, 16.2, 46, 34, CD), O(138.8, 16.45, 48, 24, CD), O(143.8, 16.6, 46, 18, CD), O(145.6, 17.3, 38, 16, CD), O(147.4, 17.45, 38, 13, [10.9662, 106.6977]),
    O(150.4, 16.5, 46, 12, BLVD), O(154.0, 16.7, 46, 8, BLVD), O(156.6, 17.35, 38, 6, BLVD),
    # 11 · V8 điểm nóng người đi bộ → "hạ tầng thương mại"
    O(159.8, 17.5, 36, 1, BLVD), O(163.0, 16.4, 44, 0, PARK), O(170.0, 16.3, 42, -12, PARK), O(178.5, 16.1, 46, -22, PARK), O(186.6, 15.5, 34, -12, PARK),
    # 12 · V3 Longfor (Hồng Kông) → dự án
    O(189.6, 14.6, 16, 0), [192.6, 14.5, 108.5, 6.3, 0, 0], [196.0, 15.5, 109.5, 5.35, 0, 0], [205.0, 15.8, 109.8, 5.6, 0, 0], [212.8, 16.2, 110.0, 5.8, 0, 0],
    # 13 · V10 thẻ đối tác: Singapore → về Việt Nam
    [216.2, 5.6, 105.0, 5.85, 0, 0], [220.6, 4.6, 104.8, 6.0, 0, 0], [223.8, 10.6, 106.6, 8.6, 0, 0], O(226.6, 14.9, 20, 0),
    # 14 · V9 các mốc thời gian trên bản đồ
    O(231.5, 15.35, 34, 8), O(236.5, 15.55, 40, 16), O(242.6, 16.05, 44, 20, CD),
    # 15 · V1 kết: ven kênh (zoom-through) → kéo ra thấy mọi lớp → tên dự án phát sáng
    [246.0, 10.9690, 106.7022, 16.6, 40, 10], [248.0, 10.9690, 106.7022, 17.2, 36, 6], [250.9, 10.9690, 106.7022, 17.35, 34, 6],
    [254.0, 10.9660, 106.7000, 14.9, 30, 2], [257.2, 10.9664, 106.6990, 14.75, 34, 0], O(260.2, 15.0, 40, 4),
]
L = lambda geo, kind, id, w=5, fill=False, ln=True: {"geo": geo, "kind": kind, "id": id, "w": w, "fill": fill, "len": ln}
layers = [L("prov:VNM", "adm", "vnm", 4, True, False), L("prov:TPHCM_moi", "adm", "hcm", 5, True, False),
          L("prov:Đồng Nai", "adm", "dn", 3, True, False), L("prov:Tây Ninh", "adm", "tn", 3, True, False), L("prov:Đồng Tháp", "adm", "dt", 3, True, False),
          L("lines:site", "proj", "site", 6, True, True), L("prov:green_site", "green", "gsite", 3, True, False),
          L("prov:USA", "adm", "usa", 4, True, False), L("lines:canal", "water", "canal", 7, False, True), L("lines:blvd", "route", "blvd", 6, False, True),
          L("lines:ql13", "route", "ql13", 5, False, True), L("lines:vd3", "route", "vd3", 5, False, True)]
links = [{"id": "tl1", "a": "d1", "b": "d2", "bend": 0.25, "kind": "yel", "w": 4}, {"id": "tl2", "a": "d2", "b": "park", "bend": -0.3, "kind": "yel", "w": 4}, {"id": "tl3", "a": "park", "b": "cd_n", "bend": 0.3, "kind": "yel", "w": 4}, {"id": "lk_hk", "a": "hk", "b": "oneera", "bend": 0.18, "kind": "route", "w": 5}, {"id": "lk_sg", "a": "sg", "b": "oneera", "bend": -0.2, "kind": "route", "w": 5}]
circles = [{"id": "c_park", "pt": "park", "r_m": 56.4, "kind": "green"}, {"id": "c_hyde", "pt": "hyde", "r_m": 365.6, "kind": "green"},
           {"id": "c_oe", "pt": "oneera", "r_m": 397.0, "kind": "proj"},
           {"id": "h1", "pt": "park", "r_m": 190, "heat": True}, {"id": "h2", "pt": "blvd_mid", "r_m": 150, "heat": True}, {"id": "h3", "pt": "canal_m", "r_m": 170, "heat": True},
           {"id": "h4", "pt": "p_vas", "r_m": 120, "heat": True}]
rings = [{"id": "rg_walk", "pt": "park", "lat": 10.965, "t": 77.4, "km": [0.4, 0.8], "out": 89.0}, {"id": "rg_end", "pt": "oneera", "lat": 10.967, "t": 255.0, "km": [1, 2]}]
movers = [{"path": "canal", "t": 91.9, "d": 6.6, "icon": "bike", "out": 104.0}, {"path": "lk_hk", "t": 196.2, "d": 2.0, "icon": "plane", "out": 214.0},
          {"path": "lk_sg", "t": 217.6, "d": 2.0, "icon": "plane", "out": 223.0}]
lab = []
def la(at, t, d, big=None, text="", small="", color="w", lx=0, ly=-260, align="c", xl=False, unit=None, count=None):
    lab.append({k: v for k, v in dict(at=at, t=t, d=d, big=big, text=text, small=small, color=color, lx=lx, ly=ly, align=align, xl=xl, unit=unit, count=count).items() if v not in (None, "", False)})
# 1
la("hcm", 3.9, 3.6, "TP.HCM", "sau sáp nhập", color="adm", ly=-280)
# 2
la("hcm_t", 11.6, 2.6, "THUẬN GIAO", "phường", color="adm", ly=-230)
la("site_w", 14.7, 2.8, "49,5", "khu đô thị", color="proj", lx=120, ly=-300, xl=True, unit="ha", count={"from": 0, "to": 49.5, "dec": 1})
la("site_w", 17.6, 2.7, "> 1 tỷ", "tổng vốn đầu tư", color="w", lx=120, ly=-300, xl=True, unit="USD")
# 3
la("site_n", 23.4, 2.0, "25", "mật độ xây dựng nhà ở", color="proj", ly=-330, xl=True, unit="%", count={"from": 0, "to": 25})
la("site_n", 25.5, 4.2, "≈ 3/4", "khu đất không đặt móng nhà", color="green", ly=-330, xl=True)
# 5
la("site_n", 53.9, 2.4, "FITWEL ★★★", "hạng Community Site", small="đô thị duy nhất châu Á đạt", color="green", ly=-320)
la("atl", 59.9, 6.6, "CDC", "Kiểm soát & phòng ngừa dịch bệnh", color="adm", lx=0, ly=170, align="c")
la("dc", 61.4, 5.1, "GSA", "cơ quan liên bang Hoa Kỳ", color="adm", lx=-140, ly=-120, align="r")
la("ny", 64.0, 2.7, "Center for Active Design", "đơn vị vận hành Fitwel", color="w", lx=-200, ly=-400, align="c")
# 6
la("r400", 77.8, 7.6, "5 PHÚT", "đi bộ", color="yel", ly=-40)
la("r800w", 78.6, 6.8, "10 PHÚT", "đi bộ", color="yel", lx=30, ly=-70, align="l")
la("oneera", 85.9, 3.4, "≈ 3/4", "nơi nuôi thói quen vận động", color="green", ly=-190)
# 7
la("canal_s", 97.8, 6.0, "≈ 30 PHÚT", "2,6 km dạo bộ · đạp xe hai bờ kênh", color="proj", lx=-320, ly=-300, align="c")
la("park", 100.6, 4.4, "ONE PARK · 1 HA", "quảng trường · 2 hồ bơi", small="cà phê · sân chơi trẻ em", color="green", ly=-300)
# 8
la("hyde", 111.9, 3.6, "HYDE PARK", "≈ 42 ha · liền kề", color="green", ly=-430)
la("oneera", 113.1, 2.4, "ONE ERA", "49,5 ha", color="proj", lx=-300, ly=-200, align="r")
# 10
la("cd_n", 140.3, 4.0, "357", "nhà phố + shophouse", color="proj", ly=-300, xl=True, unit="căn", count={"from": 0, "to": 357})
la("blvd_mid", 153.4, 3.2, "ĐẠI LỘ 25 M", "mặt tiền thứ hai hướng One Park", color="route", ly=-280)
# 11
la("blvd_mid", 178.5, 3.6, "NGUỒN KHÁCH", "từ cư dân, mỗi ngày", color="yel", ly=-300)
# 12
la("hk", 195.8, 8.5, "LONGFOR", "niêm yết Hồng Kông · từ 09/2026", color="route", ly=-260)
la("hk", 204.7, 5.6, "100", "tại 25 thành phố châu Á", color="w", lx=-120, ly=230, xl=True, unit="TTTM", count={"from": 0, "to": 100})
la("hk", 210.6, 2.6, "> 90%", "hài lòng · 17 năm liền", small="Longfor Intelligent Living", color="w", lx=-120, ly=230, xl=True)
# 13
la("sg", 217.4, 4.4, "SURBANA JURONG", "tư vấn quy hoạch", color="route", ly=-470)
la("sg", 219.8, 2.0, "CPG", "thiết kế cảnh quan", color="green", ly=-230)
la("oneera", 222.0, 4.2, "SAVILLS", "quản lý · vận hành", color="w", ly=-280)
# 14
la("d1", 228.4, 3.8, "27/09/2025", "khởi công", color="yel", ly=-260)
la("d2", 230.2, 10.0, "09/2026", "Longfor tham gia", color="yel", ly=-300)
la("park", 232.4, 7.9, "31/10/2026", "One Park mở cửa", color="yel", lx=-230, ly=-200)
la("cd_n", 240.4, 2.6, "QUÝ IV/2028", "bàn giao nhà phố đầu tiên", small="Central District", color="yel", ly=-300, xl=False)
# 15
la("canal_m", 245.0, 3.0, "MỖI SÁNG", "đường ven kênh có người chạy bộ", color="proj", ly=-280)
pins = [{"at": "p_vas", "text": "VAS Saigon", "t": 119.9, "d": 11.5}, {"at": "p_kind", "text": "Kindup", "t": 121.5, "d": 9.9, "left": True},
        {"at": "p_meret", "text": "Meret Health Center", "t": 124.3, "d": 7.1}, {"at": "p_sport", "text": "Khu thể thao", "t": 126.2, "d": 5.2},
        {"at": "p_tttm", "text": "TTTM", "t": 127.3, "d": 4.1}, {"at": "p_off", "text": "Văn phòng hạng A", "t": 128.3, "d": 3.1, "left": True}]
ground = [{"at": "hcm_t", "text": "1 m² XÂY = 1 m² BÁN", "t": 5.0, "d": 5.4, "size": 84}, {"at": "oneera", "text": "ONE ERA", "t": 16.4, "d": 3.8},
          {"at": "q_title", "text": "LÀM VIỆC CHO AI?", "t": 42.6, "d": 4.6, "size": 58}, {"at": "cd", "text": "CENTRAL DISTRICT", "t": 135.6, "d": 4.4, "size": 72},
          {"at": "park", "text": "HẠ TẦNG THƯƠNG MẠI", "t": 182.4, "d": 5.0, "size": 78}, {"at": "oneera", "text": "ONE ERA", "t": 256.4, "d": 3.8, "size": 120}]
ev = []
E = lambda t, act, id, d=.6, **k: ev.append(dict(t=t, act=act, id=id, d=d, **k))
# 1
E(0.8, "show", "vnm", 1.0, to=.9); E(1.6, "show", "vnm-fill", 1.0, to=.5); E(4.0, "show", "hcm", .8); E(4.2, "show", "hcm-fill", .8, to=1)
E(4.6, "show", "dn", .8, to=.4); E(4.6, "show", "tn", .8, to=.4); E(4.6, "show", "dt", .8, to=.4); E(5.6, "hide", "vnm", 1.2)
E(10.9, "hide", "dn", .8); E(10.9, "hide", "tn", .8); E(10.9, "hide", "dt", .8); E(11.4, "dim", "hcm", 1.0, to=.3); E(13.2, "hide", "hcm", 1.0)
# 2
E(14.0, "draw", "site", 1.0); E(15.0, "show", "site-fill", .8, to=1)
# 3
E(21.0, "show", "site-fill", .6, to=.25); E(22.8, "grow", "ot", 2.0); E(23.1, "grow", "cd", 2.0)
# 4
E(33.0, "show", "gsite", .1); E(33.0, "show", "gsite-fill", 1.0, to=1); E(33.2, "tint", "ot", .8, to=.55); E(33.2, "tint", "cd", .8, to=.55)
# 5
E(47.6, "hide", "gsite", .8); E(48.0, "grow", "ot", .9, to=0, ease="power2.in"); E(48.2, "grow", "cd", .9, to=0, ease="power2.in")
E(58.6, "show", "usa", .8); E(59.2, "show", "usa-fill", .8, to=1); E(58.6, "show", "vnm", .8, to=.6); E(66.6, "hide", "usa", 1.2); E(70.0, "hide", "vnm", 1.0)
# 6
E(76.2, "show", "c_park", .6, to=.8); E(85.8, "show", "gsite", .9, to=1); E(89.6, "hide", "gsite", .8)
# 7
E(91.7, "draw", "canal", 6.6); E(100.2, "show", "c_park", .5, to=1)
# 8
E(108.9, "dim", "site", .6, to=.5); E(111.6, "show", "c_hyde", .8); E(113.0, "show", "c_oe", .8, to=.85); E(116.0, "hide", "c_hyde", .8); E(116.0, "hide", "c_oe", .8)
E(116.0, "show", "site", .6, to=1)
# 10
E(132.0, "grow", "ot", 1.6, to=.6); E(132.0, "tint", "ot", .1, to=.5); E(137.4, "grow", "cd", 1.8); E(137.4, "tint", "cd", .1, to=.95)
E(148.0, "show", "canal", .5, to=1); E(150.9, "draw", "blvd", 1.2); E(154.9, "show", "c_park", .4, to=1)
# 11
E(164.4, "show", "h1", 1.0); E(165.6, "show", "h2", 1.0); E(166.8, "show", "h3", 1.0); E(168.0, "show", "h4", 1.0)
E(187.6, "hide", "h1", .8); E(187.6, "hide", "h2", .8); E(187.6, "hide", "h3", .8); E(187.6, "hide", "h4", .8)
E(188.0, "grow", "ot", .9, to=0, ease="power2.in"); E(188.0, "grow", "cd", .9, to=0, ease="power2.in"); E(188.2, "hide", "blvd", .6); E(188.2, "hide", "canal", .6); E(188.2, "hide", "c_park", .6)
# 12–13
E(195.6, "draw", "lk_hk", 2.0); E(217.4, "draw", "lk_sg", 2.0); E(221.8, "hide", "lk_hk", .8); E(223.0, "hide", "lk_sg", .8)
E(229.0, "draw", "tl1", 1.2); E(231.2, "draw", "tl2", 1.2); E(239.4, "draw", "tl3", 1.0)
E(243.2, "hide", "tl1", .8); E(243.2, "hide", "tl2", .8); E(243.2, "hide", "tl3", .8)
# 15 — tích luỹ mọi lớp
E(243.5, "show", "canal", .6, to=1)
E(254.0, "show", "gsite", .8, to=.8); E(254.3, "show", "ql13", .5); E(254.3, "draw", "ql13", 1.0); E(254.5, "draw", "vd3", 1.0); E(254.7, "show", "blvd", .5, to=1)
E(254.9, "show", "c_park", .6, to=1); E(255.2, "show", "h1", .8, to=.7); E(256.0, "draw", "site", 1.2); E(256.0, "show", "site-fill", 1.0, to=1)
foot = [{"t": 29.9, "d": 2.8, "media": "assets/img/p7.jpg", "move": "push", "focus": "55% 50%", "src": "phối cảnh CĐT (The Leader)"},
        {"t": 105.6, "d": 2.8, "media": "assets/img/p1.jpg", "move": "pull", "focus": "60% 50%", "src": "khai trương One Park, ảnh CafeF 03/11/2026"},
        {"t": 144.6, "d": 2.8, "media": "assets/img/p3.jpg", "move": "panR", "focus": "35% 50%", "src": "nhà phố Central District, phối cảnh CĐT (CafeF)"},
        {"t": 156.8, "d": 2.9, "media": "assets/img/p6.jpg", "move": "push", "focus": "50% 60%", "src": "shophouse mặt tiền, phối cảnh CĐT (CafeF)"},
        {"t": 248.1, "d": 2.9, "media": "assets/img/p5.jpg", "move": "push", "focus": "50% 55%", "src": "đường nội khu có người đạp xe, phối cảnh CĐT (CafeF)"}]
legend = [{"t": 33.4, "d": 13.4, "items": [["#4ADE80", "≈ 75% cây xanh · nước · đường đi bộ"], ["#2FD3E0", "≈ 25% xây nhà ở"]]},
          {"t": 164.6, "d": 22.4, "items": [["#FACC15", "lượng người đi bộ (minh hoạ)"], ["#4ADE80", "One Park"], ["#E04BD6", "đại lộ nội khu 25 m"]]}]
src = [{"t": 1.0, "d": 19.0, "text": "Nguồn: CafeF, Báo Đầu tư (11/2026) · ảnh vệ tinh Esri, Maxar"},
       {"t": 21.0, "d": 26.0, "text": "Mật độ ~25%: CafeF (05/2026) · khối nhà là minh hoạ tỉ lệ, không phải bản vẽ quy hoạch"},
       {"t": 52.4, "d": 15.0, "text": "Fitwel 3 sao (Community Site): VnExpress, Znews (2026)"},
       {"t": 76.4, "d": 13.0, "text": "Bán kính đi bộ ước tính 80 m/phút · vị trí One Park minh hoạ"},
       {"t": 91.0, "d": 25.0, "text": "Kênh Suối Cát 2,6 km, One Park 1 ha: CafeF (11/2026) · Hyde Park ~42 ha: Báo Đầu tư — vị trí minh hoạ"},
       {"t": 117.5, "d": 13.0, "text": "Tên tiện ích theo CafeF, Báo Đầu tư · vị trí ghim minh hoạ"},
       {"t": 132.0, "d": 55.0, "text": "Central District, shophouse 2 mặt tiền: CafeF (07/11/2026) · bố trí minh hoạ"},
       {"t": 194.0, "d": 32.0, "text": "Longfor & đối tác: The Leader (25/09/2026)"},
       {"t": 228.0, "d": 15.0, "text": "Mốc thời gian: SGGP (09/2025), The Leader (09/2026), CafeF (11/2026)"}]
chapters = [
    {"t": 0.0, "name": "Phép tính quen thuộc", "V": "V2", "cam": "hạ từ mây xuống VN → TP.HCM (zoom 5.2→9.5)", "layers": "VN, TP.HCM (cam), tỉnh lân cận mờ 40%, tiêu đề mặt đất"},
    {"t": 10.9, "name": "Thuận Giao · 49,5 ha · >1 tỷ USD", "V": "V1", "cam": "fly-to vào dự án, nghiêng 0→48°", "layers": "ranh dự án vẽ + phủ cyan, ONE ERA mặt đất, 2 thẻ số"},
    {"t": 20.4, "name": "Mật độ 25%", "V": "V6", "cam": "quay quanh 4→25°, đẩy vào phối cảnh", "layers": "60 khối 3D mọc, thẻ 25% và ≈3/4"},
    {"t": 32.1, "name": "3/4 khu đất nhường lại", "V": "V8", "cam": "quay chậm 25→48°, kéo ra", "layers": "tô xanh 75% + chú giải, khối mờ, tiêu đề LÀM VIỆC CHO AI?"},
    {"t": 47.2, "name": "Fitwel 3 sao · CDC Hoa Kỳ", "V": "V2", "cam": "về 0° → bay vòng ra thế giới → Đông Hoa Kỳ", "layers": "thẻ Fitwel, Hoa Kỳ (cam), CDC/GSA/Center for Active Design"},
    {"t": 67.1, "name": "Thiết kế khiến người ta vận động", "V": "V4", "cam": "bay vòng về VN → One Park, nghiêng 24→40°", "layers": "vòng 5/10 phút đi bộ, One Park, tô xanh 3/4"},
    {"t": 89.7, "name": "Kênh Suối Cát · One Park", "V": "V3", "cam": "bám đầu tuyến dọc kênh → One Park → zoom-through", "layers": "tuyến kênh + xe đạp, nhãn 30 phút, One Park 1 ha"},
    {"t": 108.5, "name": "Hyde Park ~42 ha", "V": "V5", "cam": "kéo ra 17.4→14.6", "layers": "3 vòng tròn đúng diện tích (1 / 42 / 49,5 ha)"},
    {"t": 115.6, "name": "Tiện ích có tên", "V": "V7", "cam": "quay chậm -2→36°", "layers": "6 ghim vàng: VAS, Kindup, Meret, thể thao, TTTM, văn phòng"},
    {"t": 129.2, "name": "357 căn Central District", "V": "V6", "cam": "đẩy vào CD → zoom-through → đại lộ", "layers": "khối CD sáng, khối khác mờ, thẻ 357, đại lộ 25 m, One Park"},
    {"t": 156.7, "name": "Mảng xanh = hạ tầng thương mại", "V": "V8", "cam": "zoom-through shophouse → quay -22°", "layers": "4 điểm nóng người đi bộ + chú giải"},
    {"t": 187.5, "name": "Longfor", "V": "V3", "cam": "kéo ra châu Á (Z 5.4)", "layers": "tuyến HK→One Era có máy bay, thẻ 100 TTTM, >90%"},
    {"t": 213.5, "name": "Đội ngũ quy hoạch", "V": "V10", "cam": "lướt xuống Singapore → về dự án", "layers": "thẻ Surbana Jurong, CPG, Savills; tuyến SG→One Era"},
    {"t": 226.7, "name": "Lời hứa và mốc thời gian", "V": "V9", "cam": "nghiêng 20→44°, quay 0→20°", "layers": "27/09/2025 · 09/2026 · 31/10/2026 · Quý IV/2028"},
    {"t": 242.9, "name": "Kết", "V": "V1", "cam": "zoom-through ven kênh → kéo ra → về ranh", "layers": "mọi lớp: kênh, xanh, đường, đại lộ, vòng km, ranh phát sáng, ONE ERA"}]
out = {"duration": 260.23, "audio": "assets/mix.wav", "gsap": "assets/lib/gsap.min.js", "sat": SAT, "points": PTS, "blocks": "blocks.json", "blockH": {"ot": 38, "cd": 44},
       "cam": cam, "layers": layers, "links": links, "circles": circles, "rings": rings, "movers": movers, "labels": lab, "pins": pins, "ground": ground,
       "ev": ev, "hud": {"clouds": [0.0, 2.8], "legend": legend, "src": src}, "foot": foot, "cuts": [], "chapters": chapters}
for k in cam: k[5] = round(k[5] * 0.6, 1)
for a, b in zip(cam, cam[1:]): assert b[0] > a[0], (a[0], b[0])
json.dump(out, open("proj/flight.json", "w"), ensure_ascii=False, indent=1)
print(len(cam), "keys", len(lab), "labels", len(ev), "events")
```

## FILE: templates/one-era-flight/mk_sfx3.py

```python
"""SFX theo sự kiện của kế hoạch bay: whoosh khi camera di chuyển lớn, pop cho nhãn/ghim/số, swell trước lộ diện lớn."""
import json, sys
F = json.load(open(sys.argv[1])); ev = []
add = lambda t, s, db=0: ev.append({"t": round(max(0, t), 3), "sfx": s, "db": db})
K = F["cam"]
for a, b in zip(K, K[1:]):
    big = abs(b[3] - a[3]) > 0.9 or abs(b[2] - a[2]) > 1 or abs(b[4] - a[4]) > 12
    if big: add(a[0] + 0.1, "whoosh.wav", -3 if abs(b[3] - a[3]) > 2.5 else -7)
for l in F["labels"]: add(l["t"], "pop.wav", -1 if l.get("xl") else -4)
for p in F["pins"]: add(p["t"] + 0.25, "pop.wav", 0)
for g in F["ground"]: add(g["t"] - 0.9, "riser.wav", -7); add(g["t"] + 0.1, "impact.wav", -6)
for f in F["foot"]: add(f["t"] - 0.9, "riser.wav", -5); add(f["t"] + f["d"] - 0.3, "whoosh.wav", -6)
for r in F["rings"]:
    for i in range(len(r["km"])): add(r["t"] + i * .45, "pop.wav", -3)
for e in F["ev"]:
    if e["act"] == "grow" and e.get("to", 1) > 0.5: add(e["t"], "riser.wav", -8)
    if e["act"] == "draw" and e.get("d", .6) >= 1: add(e["t"], "whoosh.wav", -10)
    if e["act"] == "show" and e["id"].startswith(("c_", "h")) and e.get("to", 1) > .7: add(e["t"], "pop.wav", -6)
for m in F["movers"]: add(m["t"], "whoosh.wav", -9)
add(0.0, "whoosh.wav", 0)
ev.sort(key=lambda x: x["t"]); out = []
for x in ev:
    if out and any(o["sfx"] == x["sfx"] and x["t"] - o["t"] < .25 for o in out[-5:]): continue
    out.append(x)
json.dump(out, open(sys.argv[2], "w"), indent=0); print(len(out), "SFX")
```

## FILE: templates/one-era-flight/prep_geo.py

```python
import json, math
from shapely.geometry import shape, Polygon, MultiPolygon, box, Point
from shapely.ops import unary_union
from shapely import affinity
import sys
S = sys.argv[1] if len(sys.argv) > 1 else "."   # thư mục có oe/geo/geo.json (geo_build.py) và osm/ne_10m_admin_0_countries.geojson
g = json.load(open(f"{S}/oe/geo/geo.json"))
wx = lambda lng: (lng + 180) / 360 * 256 * 2 ** 8
wy = lambda lat: (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * 256 * 2 ** 8
def path(geom, closed=True):
    polys = [geom] if geom.geom_type == "Polygon" else list(geom.geoms)
    out = []
    for p in polys:
        c = list(p.exterior.coords)
        out.append("M" + " L".join(f"{wx(x):.1f} {wy(y):.1f}" for x, y in c) + (" Z" if closed else ""))
    return " ".join(out)
ne = json.load(open(f"{S}/osm/ne_10m_admin_0_countries.geojson"))
for f in ne["features"]:
    iso = f["properties"].get("ADM0_A3")
    if iso in ("USA", "VNM"):
        geom = shape(f["geometry"]).simplify(0.08 if iso == "USA" else 0.02)
        if iso == "USA":  # bỏ Alaska/Hawaii/đảo xa, giữ lục địa
            geom = unary_union([p for p in geom.geoms if p.area > 3 and p.centroid.x > -130])
        g["prov"][iso] = path(geom); print(iso, len(g["prov"][iso]))
# --- quy hoạch minh hoạ trong ranh dự án (KHÔNG phải bản vẽ của CĐT) ---
SITE = [[106.69143, 10.964091], [106.694648, 10.966935], [106.700764, 10.970411], [106.703339, 10.969463], [106.704304, 10.965671], [106.702373, 10.964723],
        [106.699476, 10.965671], [106.697867, 10.964091], [106.695614, 10.964723], [106.693361, 10.964091], [106.691751, 10.963143]]
site = Polygon(SITE)
mlat = 10.967; kx = 111320 * math.cos(math.radians(mlat)); ky = 110574
siteM = affinity.scale(Polygon([((x - SITE[0][0]) * kx, (y - SITE[0][1]) * ky) for x, y in SITE]), 1, 1, origin=(0, 0))
toLL = lambda x, y: (SITE[0][0] + x / kx, SITE[0][1] + y / ky)
print("site area ha", siteM.area / 1e4)
park_c = (106.6962, 10.9652)   # One Park (minh hoạ, gần mặt QL13 / Galleria)
pc = ((park_c[0] - SITE[0][0]) * kx, (park_c[1] - SITE[0][1]) * ky)
park = Point(pc).buffer(56.4)   # 1 ha
canal = shape({"type": "LineString", "coordinates": []}) if False else None
blocks = []; ang = 30  # hướng lưới theo trục dài khu đất
import itertools
cx, cy = siteM.centroid.x, siteM.centroid.y
for i, j in itertools.product(range(-20, 21), range(-12, 13)):
    bx, by = cx + i * 92, cy + j * 52
    r = affinity.rotate(box(bx - 40, by - 14, bx + 40, by + 14), ang, origin=(cx, cy))
    if siteM.buffer(-12).contains(r) and not r.intersects(park.buffer(25)):
        blocks.append(r)
# chọn đủ ~25% diện tích, ưu tiên quanh tâm
blocks.sort(key=lambda b: b.centroid.distance(Point(cx, cy)))
sel = []; area = 0
for b in blocks:
    if area >= 0.25 * siteM.area: break
    sel.append(b); area += b.area
print("blocks", len(sel), "coverage %.1f%%" % (area / siteM.area * 100))
B = []
for k, b in enumerate(sel):
    c = b.centroid; lng, lat = toLL(c.x, c.y)
    d = Point(c.x, c.y).distance(Point(pc))
    B.append({"lng": round(lng, 6), "lat": round(lat, 6), "w": 80, "d": 28, "ang": -ang, "cd": d < 420})
json.dump(B, open("blocks.json", "w"))
print("central district blocks", sum(b["cd"] for b in B))
# đại lộ nội khu 25 m (minh hoạ): đường thẳng qua One Park theo hướng lưới
p0 = affinity.rotate(Point(pc[0] - 50, pc[1] + 90), 0); 
ax = math.cos(math.radians(ang)); ay = math.sin(math.radians(ang))
a = (pc[0] + 90 * -ay - 30 * ax, pc[1] + 90 * ax - 30 * ay); b = (a[0] + 900 * ax, a[1] + 900 * ay)
la, lb = toLL(*a), toLL(*b)
g["lines"]["blvd"] = f"M{wx(la[0]):.1f} {wy(la[1]):.1f} L{wx(lb[0]):.1f} {wy(lb[1]):.1f}"
g["lab"]["blvd_mid"] = [wx((la[0] + lb[0]) / 2), wy((la[1] + lb[1]) / 2)]
g["prov"]["green_site"] = path(Polygon([toLL(x, y) for x, y in siteM.exterior.coords]))
json.dump(g, open("proj/geo.json", "w"))
print("park", park_c, "blvd", la, lb)
```

## FILE: templates/one-era-motion/README.md

```markdown
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
```

## FILE: templates/one-era-motion/cap.js

```javascript
// Quay một cảnh Google Earth 3D thành chuỗi khung JPG, camera nội suy đều giữa 2 điểm (không dừng).
// Dùng:  node earth_capture.js shot.json <thư mục ra> [khung bắt đầu, để chạy tiếp]
// shot.json: {"dpr":1.5,"frames":80,"from":{lat,lng,dist,head,tilt},"to":{...}}  (10 khung = 1 giây)
//            hoặc {"dpr":1,"list":[{...},{...}],"frames":N} để chụp thử nhiều góc máy.
// dist: khoảng cách camera (m), log-nội suy; head: hướng (độ); tilt: nghiêng (độ, 0 = nhìn thẳng xuống).
// Cần mạng tới earth.google.com, kh.google.com, www.gstatic.com, www.google.com, earth-pa.clients6.google.com, htapi.google.com.
// Toạ độ click giao diện (đóng popup, Basemap -> Clean) đo ở viewport 540×960; Google đổi giao diện thì cần đo lại.
const { chromium } = require('playwright');
const fs = require('fs');
const [,, specFile, outDir, startArg] = process.argv;
const spec = JSON.parse(fs.readFileSync(specFile, 'utf8'));
if (startArg) spec.start = parseInt(startArg, 10);
fs.mkdirSync(outDir, { recursive: true });
const url = (c) => `https://earth.google.com/web/@${c.lat.toFixed(6)},${c.lng.toFixed(6)},${c.alt.toFixed(1)}a,${c.dist.toFixed(1)}d,${spec.fov || 35}y,${c.head.toFixed(2)}h,${c.tilt.toFixed(2)}t,0r`;
const lerp = (a, b, s) => a + (b - a) * s;
function cam(i) {
  if (spec.list) return Object.assign({ alt: 10 }, spec.list[i]);
  const s = spec.frames <= 1 ? 0 : i / (spec.frames - 1);
  const A = spec.from, B = spec.to;
  return { lat: lerp(A.lat, B.lat, s), lng: lerp(A.lng, B.lng, s), alt: lerp(A.alt || 10, B.alt || 10, s),
           dist: Math.exp(lerp(Math.log(A.dist), Math.log(B.dist), s)), head: lerp(A.head, B.head, s), tilt: lerp(A.tilt, B.tilt, s) };
}
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: spec.w || 540, height: spec.h || 960 }, deviceScaleFactor: spec.dpr || 2 });
  await p.goto(url(cam(spec.start || 0)), { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(45000);
  // giao diện ở 540×960 CSS px: đóng popup, chọn Basemap → Clean (không nhãn/đường/biên giới)
  await p.mouse.click(455, 228); await p.waitForTimeout(1500);
  await p.mouse.click(49, 864); await p.waitForTimeout(1000);
  await p.mouse.click(500, 40); await p.waitForTimeout(2500);
  await p.mouse.click(507, 288); await p.waitForTimeout(1500);
  await p.mouse.click(28, 28); await p.waitForTimeout(8000);
  await p.evaluate(() => { const c = document.getElementById('earth-canvas'); document.body.appendChild(c);
    c.style.cssText = 'position:fixed;left:0;top:0;width:100vw;height:100vh;z-index:2147483647;'; });
  let prev = null;
  for (let i = spec.start || 0; i < spec.frames; i++) {
    const t0 = Date.now();
    await p.evaluate((u) => { history.replaceState(null, '', u); window.dispatchEvent(new PopStateEvent('popstate')); }, url(cam(i)));
    // chờ cố định: camera dịch rất ít mỗi khung nên tile gần như đã có sẵn
    await p.waitForTimeout(i === (spec.start || 0) ? 6000 : (spec.wait || 1800));
    const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
    fs.writeFileSync(`${outDir}/f${String(i).padStart(4, '0')}.jpg`, buf);
    if (i % 10 === 0) console.log(`frame ${i}/${spec.frames} ${(Date.now() - t0)}ms`);
  }
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
```

## FILE: templates/one-era-motion/earth-shots/n_dive.json

```json
{"dpr": 1.5, "frames": 60, "from": {"lat": 10.85, "lng": 106.72, "dist": 900000, "head": 0, "tilt": 0}, "to": {"lat": 10.85, "lng": 106.72, "dist": 28000, "head": 15, "tilt": 35}}
```

## FILE: templates/one-era-motion/earth-shots/n_hcm.json

```json
{"dpr": 1.5, "frames": 36, "from": {"lat": 10.7765, "lng": 106.7045, "dist": 2600, "head": 200, "tilt": 62}, "to": {"lat": 10.777, "lng": 106.704, "dist": 2000, "head": 235, "tilt": 66}}
```

## FILE: templates/one-era-motion/earth-shots/n_metro.json

```json
{"dpr": 1.5, "frames": 36, "from": {"lat": 10.8665, "lng": 106.802, "dist": 1100, "head": 250, "tilt": 62}, "to": {"lat": 10.8668, "lng": 106.8015, "dist": 850, "head": 280, "tilt": 66}}
```

## FILE: templates/one-era-motion/earth-shots/n_mptv.json

```json
{"dpr": 1.5, "frames": 36, "from": {"lat": 10.974, "lng": 106.7085, "dist": 750, "head": 40, "tilt": 68}, "to": {"lat": 10.9755, "lng": 106.71, "dist": 620, "head": 60, "tilt": 70}}
```

## FILE: templates/one-era-motion/earth-shots/n_ql13.json

```json
{"dpr": 1.5, "frames": 36, "from": {"lat": 10.9595, "lng": 106.698, "dist": 800, "head": 330, "tilt": 68}, "to": {"lat": 10.964, "lng": 106.695, "dist": 650, "head": 330, "tilt": 70}}
```

## FILE: templates/one-era-motion/earth-shots/n_site_low.json

```json
{"dpr": 1.5, "frames": 36, "from": {"lat": 10.9673, "lng": 106.6995, "dist": 700, "head": 120, "tilt": 70}, "to": {"lat": 10.9675, "lng": 106.6998, "dist": 560, "head": 150, "tilt": 72}}
```

## FILE: templates/one-era-motion/earth-shots/n_street.json

```json
{"dpr": 1.5, "frames": 36, "from": {"lat": 10.953, "lng": 106.706, "dist": 520, "head": 30, "tilt": 70}, "to": {"lat": 10.9535, "lng": 106.7055, "dist": 430, "head": 55, "tilt": 73}}
```

## FILE: templates/one-era-motion/earth-shots/n_tdm.json

```json
{"dpr": 1.5, "frames": 36, "from": {"lat": 10.981, "lng": 106.653, "dist": 2400, "head": 300, "tilt": 58}, "to": {"lat": 10.9805, "lng": 106.654, "dist": 1900, "head": 330, "tilt": 63}}
```

## FILE: templates/one-era-motion/earth-shots/n_wide.json

```json
{"dpr": 1.5, "frames": 36, "from": {"lat": 10.9673, "lng": 106.6995, "dist": 6000, "head": 210, "tilt": 50}, "to": {"lat": 10.9673, "lng": 106.6995, "dist": 9000, "head": 225, "tilt": 45}}
```

## FILE: templates/one-era-motion/enc2.sh

```bash
#!/bin/bash
# enc2.sh <tên shot> : khung Google Earth (6 fps -> 30 fps nội suy, ~5,7 s cho 36 khung) -> chỉnh màu navy -> proj/assets/ge/
# Chạy từ thư mục làm việc có ge/shots/<tên>/ và proj/. SKILL = đường dẫn tới skill.
SKILL=${SKILL:-.claude/skills/parallax-bds-kinhte}
$SKILL/scripts/earth_encode.sh ge/shots/$1 ge/$1_raw.mp4 6 && ffmpeg -loglevel error -y -i ge/$1_raw.mp4 -vf "eq=saturation=0.75:contrast=1.08:gamma=0.97,colorbalance=rs=-0.06:gs=-0.02:bs=0.06:rm=-0.02:bm=0.02" -c:v libx264 -crf 17 -g 1 -pix_fmt yuv420p proj/assets/ge/$1.mp4 && echo "OK $1"
```

## FILE: templates/one-era-motion/mk_sfx.py

```python
import json
d = json.load(open("proj/shots.json")); ev = []
def add(t, s, db=0):
    if t >= 0: ev.append({"t": round(t, 3), "sfx": s, "db": db})
for sh in d["shots"]:
    st = sh["start"]; e = sh.get("enter", "T5")
    if e in ("T3", "T2"): add(st - 0.12, "whoosh.wav")
    elif e in ("T1", "T4", "DIS"): add(st - 1.4, "riser.wav", -3)
    elif sh.get("zoomBlur"): add(st, "whoosh.wav", -2)
    else: add(st, "impact.wav", -6)               # cắt cứng: nhịp chạm nhẹ
    for k in sh.get("kw", []): add(st + k["t"], "pop.wav", -2)
    for k in sh.get("montage", []): add(st + k["t"], "impact.wav", -3)
    for k in sh.get("labels", []) + sh.get("callouts", []): add(st + k["t"], "pop.wav", -4)
    for k in sh.get("pins", []): add(st + k["t"] + .2, "pop.wav", 0)
    for k in sh.get("ground", []): add(st + k["t"], "impact.wav", -2)
    for k in sh.get("rings", []):
        for i in range(len(k["km"])): add(st + k["t"] + i * .45, "pop.wav", -3)
    for k in sh.get("movers", []): add(st + k["t"], "whoosh.wav", -8)
    for k in sh.get("draw", []):
        if k["d"] >= .8: add(st + k["t"], "whoosh.wav", -9)
    if sh.get("big"): add(st + sh["big"]["t"], "impact.wav", 0)
    if sh.get("bar"): add(st + sh["bar"]["t"] + .1, "riser.wav", -8)
    for k in (sh.get("timeline") or {}).get("events", []): add(st + k["t"], "pop.wav", -2)
    for k in (sh.get("wall") or {}).get("tiles", []): add(st + k["t"], "whoosh.wav", -6)
    for k in (sh.get("stack") or {}).get("rows", []): add(st + k["t"], "pop.wav", -2)
    if sh.get("clouds"): add(st, "whoosh.wav", 0)
ev.sort(key=lambda x: x["t"]); out = []
for x in ev:  # cùng loại cách nhau ≥0,22 s
    if out and any(o["sfx"] == x["sfx"] and x["t"] - o["t"] < .22 for o in out[-4:]): continue
    out.append(x)
json.dump(out, open("proj/sfx/events.json", "w"), indent=0)
print(len(out), "SFX events")
```

## FILE: templates/one-era-motion/mk_shots.py

```python
import json
J = lambda n: json.load(open(f"maps/{n}.json"))  # metadata từ sat_tiles.py
SAT = []
for n, show in [("sat07", None), ("sat09", [8.2, 8.9]), ("sat11", [10.0, 10.8]), ("sat13", [12.0, 12.8]), ("sat16", [14.2, 15.0])]:
    m = J(n); SAT.append(dict(img=f"assets/maps/{n}_g.jpg", z=m["z"], x0=m["x0"], y0=m["y0"], w=m["w"], h=m["h"], show=show))
OE = (10.9667, 106.6985)
SITE = [[106.69143, 10.964091], [106.694648, 10.966935], [106.700764, 10.970411], [106.703339, 10.969463], [106.704304, 10.965671], [106.702373, 10.964723],
        [106.699476, 10.965671], [106.697867, 10.964091], [106.695614, 10.964723], [106.693361, 10.964091], [106.691751, 10.963143]]
PTS = {"oneera": [106.6985, 10.9666], "site_n": [106.6995, 10.9700], "site_s": [106.6975, 10.9638], "hcm": [106.7009, 10.7769], "taodan": [106.6930, 10.7740],
       "suoitien": [106.8020, 10.8665], "bd_lab": [106.62, 11.18], "hcm_lab": [106.66, 10.80], "p_vas": [106.6962, 10.9656], "p_kindup": [106.6996, 10.9677],
       "p_meret": [106.7022, 10.9688], "site_w": [106.6918, 10.9640], "site_e": [106.7040, 10.9680], "ring_5": [106.6985, 11.0118], "ring_10": [106.6985, 11.0570], "ring_15": [106.6985, 11.1022]}
CBRE = "Nguồn: CBRE Việt Nam qua CafeF, Báo Đầu tư (03/11/2026)"
OES = "Nguồn: CafeF, Báo Đầu tư (11/2026) · ảnh vệ tinh Esri, Maxar"
GE = "Hình ảnh 3D: Google Earth"
R = "Ảnh phối cảnh của chủ đầu tư (qua CafeF)"
def lay(geo, kind, id, w=5, fill=False, len_=True): return {"geo": geo, "kind": kind, "id": id, "w": w, "fill": fill, "len": len_}
SITEL = lambda id: lay("lines:site", "proj", id, 5, True, True)
sh = []
def S(**k): sh.append(k)
# ================= 0:00–0:31 nguồn cung =================
S(id="a01", start=0, dur=2.45, kind="foot", fx=["M1", "D1", "F1"], media="assets/ge/n_dive.mp4", src="Google Earth: lặn từ trên cao xuống TP.HCM + mây tổng hợp", foot=CBRE, enter="T5",
  big={"t": 0.05, "d": 2.3, "num": 6573, "unit": "căn hộ", "label": "mở bán mới · Quý II/2026"}, clouds=[0, 1.1])
S(id="a02", start=2.45, dur=2.6, kind="foot", fx=["F3", "F1"], media="assets/ge/n_hcm.mp4", src="Google Earth: trung tâm TP.HCM", foot=GE, enter="T3",
  kw=[{"t": 0.1, "d": 2.4, "lines": ["*1.934", "NHÀ LIỀN THỔ"], "pos": "mid"}])
S(id="a03", start=5.05, dur=3.05, kind="map", fx=["M10"], src="Bản đồ vector + vệ tinh Esri", seg="TP.HCM mở rộng", enter="T5",
  keys=[[0, 10.80, 106.85, 8.75], [3.05, 10.86, 106.85, 9.0]],
  layers=[lay("prov:TPHCM_cu", "adm", "a03-hcm", 4, True, False), lay("prov:BD_cu", "adm", "a03-bd", 4, True, False), lay("prov:BRVT_cu", "adm", "a03-br", 4, True, False),
          lay("prov:TPHCM_moi", "adm", "a03-moi", 6, False, True)],
  show=[{"id": "a03-hcm", "t": 0.0, "d": .3}, {"id": "a03-bd", "t": 0.25, "d": .3}, {"id": "a03-br", "t": 0.5, "d": .3}],
  hide=[{"id": "a03-hcm-core", "t": 1.9, "d": .5}, {"id": "a03-bd-core", "t": 1.9, "d": .5}, {"id": "a03-br-core", "t": 1.9, "d": .5}],
  draw=[{"id": "a03-moi", "t": 1.6, "d": 0.9}],
  labels=[{"at": "hcm_lab", "lx": -60, "ly": -260, "align": "c", "big": "TP.HCM", "text": "mở rộng", "color": "adm", "t": 2.0, "d": 1.0}])
S(id="a04", start=8.1, dur=4.85, kind="foot", fx=["F3", "F2"], media="assets/ge/n_tdm.mp4", src="Google Earth: Thủ Dầu Một (Bình Dương cũ)", foot=CBRE, enter="T3", whipDir="R",
  kw=[{"t": 0.95, "d": 1.9, "lines": ["QUÝ II", "*2026"], "pos": "mid"}, {"t": 2.9, "d": 1.8, "lines": ["BÁO CÁO", "*CBRE"], "pos": "mid", "accent": "#2FD3E0"}], busy=True)
S(id="a05", start=12.95, dur=3.05, kind="card", fx=["D4"], src="Thẻ số liệu trên nền vệ tinh mờ", foot=CBRE, enter="T3",
  media="assets/maps/sat11_g.jpg", move="push", dim=0.55,
  stack={"t": 0.0, "top": 700, "rows": [{"t": 0.1, "num": 6573, "unit": "căn hộ", "label": "mở bán mới"}, {"t": 0.5, "num": 1934, "unit": "nhà liền thổ", "label": "mở bán mới"}]})
S(id="a06", start=16.0, dur=2.4, kind="map", fx=["M2"], src="Bản đồ vector + vệ tinh Esri", zoomBlur=True, enter="T5",
  keys=[[0, 10.80, 106.85, 8.9], [0.8, 11.10, 106.70, 9.7], [2.4, 11.12, 106.68, 9.85]],
  layers=[lay("prov:BD_cu", "adm", "a06-bd", 5, True, False)], show=[{"id": "a06-bd", "t": 0.3, "d": .4}],
  labels=[{"at": "bd_lab", "lx": 0, "ly": -170, "align": "c", "big": "BÌNH DƯƠNG CŨ", "color": "adm", "t": 0.9, "d": 1.4}])
S(id="a07", start=18.4, dur=4.35, kind="foot", fx=["F3", "F1"], media="assets/ge/n_tdm.mp4", media_start=0.6, src="Google Earth: Thủ Dầu Một", foot=GE, enter="T3",
  kw=[{"t": 0.3, "d": 1.8, "lines": ["*ĐÔNG BẮC", "SIÊU ĐÔ THỊ"], "pos": "mid"}, {"t": 2.2, "d": 2.0, "lines": ["LỆCH", "*HẲN MỘT PHÍA"], "pos": "mid"}], busy=True)
S(id="a08", start=22.75, dur=2.85, kind="map", fx=["D3", "M4"], src="Bản đồ vector + vệ tinh Esri", foot=CBRE, enter="T5",
  keys=[[0, 10.95, 106.75, 9.35], [2.85, 10.97, 106.74, 9.45]],
  layers=[lay("prov:BD_cu", "adm", "a08-bd", 6, True, True)], draw=[{"id": "a08-bd", "t": 0, "d": .8}], show=[{"id": "a08-bd-fill", "t": 0.6, "d": .4}],
  labels=[{"at": "bd_lab", "lx": 0, "ly": 230, "align": "c", "big": "≈ 80%", "text": "căn hộ mới", "small": "đến từ Bình Dương cũ", "color": "adm", "t": 0.15, "d": 2.6}])
S(id="a09", start=25.6, dur=2.5, kind="foot", fx=["F3", "F2"], media="assets/ge/n_street.mp4", src="Google Earth: khu nhà phố thấp tầng, Thuận An", foot=GE, enter="T3", whipDir="R",
  kw=[{"t": 0.1, "d": 2.3, "lines": ["NHÀ LIỀN THỔ:", "*GẦN *NHƯ *KHÔNG"], "pos": "mid"}])
S(id="a10", start=28.1, dur=2.95, kind="map", fx=["D3"], src="Bản đồ vector + vệ tinh Esri", foot=CBRE, enter="T5",
  keys=[[0, 10.82, 106.72, 9.5], [2.95, 10.80, 106.71, 9.6]],
  layers=[lay("prov:TPHCM_cu", "adm", "a10-hcm", 6, True, False)], show=[{"id": "a10-hcm", "t": 0, "d": .3}],
  labels=[{"at": "hcm_lab", "lx": 0, "ly": -300, "align": "c", "big": "100%", "text": "nhà liền thổ mới", "small": "nằm ở TP.HCM cũ", "color": "adm", "t": 0.1, "d": 2.7}])
# ================= 0:31–1:02 định vị dự án =================
S(id="b01", start=31.05, dur=3.65, kind="foot", fx=["F3", "F1"], media="assets/ge/g1.mp4", src="Google Earth: khu công nghiệp Bình Dương cũ", foot=GE, enter="T3",
  kw=[{"t": 0.6, "d": 2.9, "lines": ["VÙNG", "*CÔNG *NGHIỆP"], "pos": "mid"}])
S(id="b02", start=34.7, dur=4.9, kind="map", fx=["M2"], src="Bản đồ + vệ tinh Esri (z9→z16)", zoomBlur=True, enter="T5", busy=True,
  keys=[[0, 10.90, 106.72, 9.6], [1.6, 10.96, 106.70, 11.8], [3.2, 10.9666, 106.6985, 14.6], [4.9, 10.9666, 106.6985, 15.6]],
  layers=[lay("prov:BD_cu", "adm", "b02-bd", 4, False, False)], hide=[{"id": "b02-bd", "t": 1.4, "d": .6}],
  labels=[{"at": "oneera", "lx": 0, "ly": -220, "align": "c", "big": "THUẬN GIAO", "text": "phường", "color": "adm", "t": 3.4, "d": 1.4}],
  kw=[{"t": 0.6, "d": 2.4, "lines": ["NHÀ CÓ ĐẤT?", "*GẦN *NHƯ *KHÔNG"], "pos": "high"}])
S(id="b03", start=39.6, dur=2.5, kind="map", fx=["M4", "D3"], src="Bản đồ + vệ tinh Esri", enter="T5",
  keys=[[0, 10.9666, 106.6985, 15.6], [2.5, 10.9666, 106.6985, 16.4]],
  layers=[SITEL("b03-site")], draw=[{"id": "b03-site", "t": 0.1, "d": 1.0}], show=[{"id": "b03-site-fill", "t": 1.0, "d": .5}],
  labels=[{"at": "site_s", "lx": 0, "ly": 230, "align": "c", "big": "≈ 50 HA", "text": "khu đô thị mới", "color": "proj", "t": 0.9, "d": 1.4}])
S(id="b04", start=42.1, dur=3.1, kind="foot", fx=["T1", "F3", "F2"], media="assets/img/p1.jpg", move="push", focus="55% 50%", src="Ảnh: CafeF 03/11/2026 – lễ khai trương One Era Galleria", foot="Ảnh: CafeF (03/11/2026)", enter="T1",
  kw=[{"t": 0.15, "d": 2.8, "lines": ["*31/10/2026", "KHAI TRƯƠNG"], "pos": "low"}])
S(id="b05", start=45.2, dur=3.2, kind="map", fx=["M5", "M3"], src="Bản đồ + vệ tinh Esri", enter="T3",
  keys=[[0, 10.9666, 106.6985, 15.8], [3.2, 10.9666, 106.6985, 16.0]], tilt=[0, 1.2, 0, 42], orbit=[0, 3.2, -8, 6],
  layers=[SITEL("b05-site")], show=[{"id": "b05-site", "t": 0, "d": .2}], draw=[{"id": "b05-site", "t": 0, "d": .4}],
  ground=[{"at": "oneera", "text": "THUẬN GIAO", "t": 0.6, "d": 2.5}],
  kw=[{"t": 1.8, "d": 1.3, "lines": ["MỞ CỬA", "*ĐÓN *KHÁCH"], "pos": "high"}])
S(id="b06", start=48.4, dur=2.9, kind="foot", fx=["D1", "F1"], media="assets/ge/n_site_low.mp4", src="Google Earth: công trường One Era", foot=GE, enter="T3",
  big={"t": 0.35, "d": 2.4, "num": 357, "unit": "căn", "label": "nhà phố đầu tiên"})
S(id="b07", start=51.3, dur=4.7, kind="map", fx=["M3", "F3"], src="Bản đồ + vệ tinh Esri", enter="T5",
  keys=[[0, 10.9666, 106.6985, 15.7], [4.7, 10.9666, 106.6985, 15.95]], tilt=[0, 1.0, 0, 38], orbit=[0, 4.7, 12, -12],
  layers=[SITEL("b07-site")], show=[{"id": "b07-site", "t": 0, "d": .2}], draw=[{"id": "b07-site", "t": 0, "d": .4}],
  kw=[{"t": 0.25, "d": 2.2, "lines": ["ONE ERA", "*LÀ *GÌ?"], "pos": "high", "accent": "#2FD3E0"}, {"t": 2.6, "d": 2.0, "lines": ["AI", "*ĐỨNG *SAU?"], "pos": "high", "accent": "#2FD3E0"}], busy=True)
S(id="b08", start=56.0, dur=5.9, kind="foot", fx=["F3", "F1"], media="assets/ge/g3.mp4", src="Google Earth: nút giao QL13 – Vành đai 3", foot=GE, enter="T3", whipDir="R",
  kw=[{"t": 0.8, "d": 2.4, "lines": ["*357 CĂN", "CÓ ĐỦ?"], "pos": "mid"}, {"t": 3.3, "d": 2.3, "lines": ["LẤP", "*CHỖ *TRỐNG"], "pos": "mid"}], busy=True)
# ================= 1:02–1:31 quy mô =================
S(id="c01", start=61.9, dur=2.4, kind="map", fx=["M3", "M4"], src="Bản đồ + vệ tinh Esri", enter="T5",
  keys=[[0, 10.9666, 106.6985, 15.5], [2.4, 10.9666, 106.6985, 15.9]], tilt=[0, 2.4, 20, 45], orbit=[0, 2.4, -20, 0],
  layers=[SITEL("c01-site")], draw=[{"id": "c01-site", "t": 0.1, "d": 0.9}], show=[{"id": "c01-site-fill", "t": 0.9, "d": .4}],
  kw=[{"t": 0.1, "d": 2.1, "lines": ["QUY MÔ"], "pos": "high", "accent": "#2FD3E0"}])
S(id="c02", start=64.3, dur=5.6, kind="foot", fx=["D2", "F1"], media="assets/ge/g2.mp4", src="Google Earth: công trường One Era", foot=OES, enter="T3", busy=True,
  bar={"t": 0.2, "d": 5.2, "label": "Quy mô", "value": 49.5, "max": 50, "unit": "ha", "sub": "≈ 70 sân bóng đá tiêu chuẩn", "top": 760})
S(id="c03", start=69.9, dur=2.55, kind="foot", fx=["D1", "F2"], media="assets/img/p7.jpg", move="panL", focus="60% 50%", src="Ảnh phối cảnh CĐT (The Leader)", foot=R, enter="T3", whipDir="R",
  big={"t": 0.5, "d": 1.9, "text": "> 1 TỶ", "unit": "USD", "label": "tổng vốn đầu tư", "pos": "mid"})
S(id="c04", start=72.45, dur=2.75, kind="map", fx=["D3", "M7"], src="Bản đồ + vệ tinh Esri", enter="T5",
  keys=[[0, 10.9666, 106.6985, 16.1], [2.75, 10.9666, 106.6985, 15.8]],
  layers=[SITEL("c04-site")], show=[{"id": "c04-site", "t": 0, "d": .2}], draw=[{"id": "c04-site", "t": 0, "d": .3}],
  labels=[{"at": "site_n", "lx": 0, "ly": -260, "align": "c", "big": "4.039", "text": "sản phẩm", "color": "proj", "t": 0.6, "d": 2.0}])
S(id="c05", start=75.2, dur=2.8, kind="foot", fx=["F3", "F2"], src="Montage ảnh phối cảnh CĐT (CafeF, The Leader)", foot=R, enter="T5",
  montage=[{"t": 0.0, "media": "assets/img/p3.jpg", "word": "NHÀ PHỐ"}, {"t": 0.95, "media": "assets/img/p6.jpg", "word": "SHOPHOUSE"},
           {"t": 1.65, "media": "assets/img/p4.jpg", "word": "BIỆT THỰ"}, {"t": 2.25, "media": "assets/img/p7.jpg", "word": "CĂN HỘ"}])
S(id="c06", start=78.0, dur=3.95, kind="foot", fx=["D1", "F1"], media="assets/ge/n_site_low.mp4", media_start=1.6, src="Google Earth: công trường One Era", foot=OES, enter="T3",
  big={"t": 2.9, "d": 1.0, "num": 25, "unit": "%", "label": "mật độ xây dựng nhà ở", "pos": "mid"},
  kw=[{"t": 0.1, "d": 2.6, "lines": ["MẬT ĐỘ", "*XÂY *DỰNG"], "pos": "high"}])
S(id="c07", start=81.95, dur=4.85, kind="map", fx=["M4", "D3"], src="Bản đồ + vệ tinh Esri", foot=OES, enter="T5", busy=True,
  keys=[[0, 10.9666, 106.6985, 16.2], [4.85, 10.9666, 106.6985, 16.35]],
  layers=[lay("lines:site", "green", "c07-g", 5, True, True)], draw=[{"id": "c07-g", "t": 0.2, "d": 0.9}], show=[{"id": "c07-g-fill", "t": 1.1, "d": .5}],
  labels=[{"at": "site_s", "lx": 0, "ly": 230, "align": "c", "big": "4 m² ĐẤT", "text": "→ chỉ 1 m² xây nhà", "color": "green", "t": 1.9, "d": 2.8}])
S(id="c08", start=86.8, dur=4.5, kind="foot", fx=["F3", "F2"], media="assets/img/p5.jpg", move="panR", focus="40% 50%", src="Ảnh phối cảnh CĐT (CafeF)", foot=R, enter="T3", whipDir="R",
  kw=[{"t": 0.4, "d": 3.9, "lines": ["CÂY XANH", "*TIỆN *ÍCH"], "pos": "low", "accent": "#4ADE80"}])
# ================= 1:31–2:24 chủ đầu tư & đối tác =================
S(id="d01", start=91.3, dur=3.6, kind="card", fx=["D5"], media="assets/ge/g3.mp4", media_start=2.0, dim=0.55, src="Timeline trên nền Google Earth", foot="Nguồn: SGGP, Znews (09/2025), The Leader, CafeF (2026)", enter="T5",
  timeline={"t": 0.0, "y": 960, "events": [{"t": 1.1, "x": 100, "date": "27/09/2025", "text": "khởi công"}, {"t": 1.9, "x": 380, "date": "24/09/2026", "text": "ký với Longfor"},
                                           {"t": 2.5, "x": 650, "date": "31/10/2026", "text": "khai trương"}]})
S(id="d02", start=94.9, dur=5.0, kind="card", fx=["D6"], media="assets/ge/g2.mp4", media_start=3.0, dim=0.6, src="Tường đối tác trên nền Google Earth", foot="Nguồn: SGGP, Znews, The Leader", enter="T3",
  wall={"t": 0, "top": 640, "tiles": [{"t": 0.6, "name": "Kim Oanh Group", "sub": "chủ đầu tư", "hl": True}, {"t": 2.8, "name": "Sumitomo Forestry", "sub": "Nhật Bản"},
                                       {"t": 3.9, "name": "+ 2 đối tác", "sub": "Nhật Bản"}]})
S(id="d03", start=99.9, dur=4.0, kind="foot", fx=["F3", "F1"], media="assets/ge/g2.mp4", media_start=0.0, src="Google Earth: công trường One Era", foot=GE, enter="T3", whipDir="R",
  kw=[{"t": 0.75, "d": 1.25, "lines": ["KUMAGAI", "*GUMI"], "pos": "mid"}, {"t": 2.05, "d": 1.85, "lines": ["NTT URBAN", "*DEVELOPMENT"], "pos": "mid"}], busy=True)
S(id="d04", start=103.9, dur=2.7, kind="map", fx=["M5"], src="Bản đồ + vệ tinh Esri", enter="T5",
  keys=[[0, 10.9666, 106.6985, 16.0], [2.7, 10.9666, 106.6985, 16.25]], tilt=[0, 1.0, 10, 40],
  layers=[SITEL("d04-site")], show=[{"id": "d04-site", "t": 0, "d": .2}], draw=[{"id": "d04-site", "t": 0, "d": .4}],
  ground=[{"at": "oneera", "text": "KINERA", "t": 0.4, "d": 2.2}],
  labels=[{"at": "site_n", "lx": 0, "ly": -280, "align": "c", "text": "nhà phát triển", "color": "proj", "t": 0.9, "d": 1.7}])
S(id="d05", start=106.6, dur=5.7, kind="foot", fx=["F3", "F2"], media="assets/img/p10.jpg", move="pull", focus="62% 40%", src="Ảnh: The Leader 25/09/2026 – lễ ký kết", foot="Ảnh: The Leader (25/09/2026)", enter="T3",
  kw=[{"t": 2.9, "d": 2.6, "lines": ["THÊM MỘT TÊN", "*RẤT *NẶNG *KÝ"], "pos": "low"}], busy=True)
S(id="d06", start=112.3, dur=3.7, kind="foot", fx=["T2", "F2"], media="assets/img/p8.jpg", move="push", focus="58% 45%", src="Ảnh: The Leader 25/09/2026 – ký kết Kinera × Longfor", foot="Ảnh: The Leader (25/09/2026)", enter="T2",
  callouts=[{"x": 700, "y": 760, "lx": 0, "ly": -170, "align": "c", "big": "LONGFOR", "text": "niêm yết Hồng Kông", "color": "adm", "t": 0.5, "d": 3.0}])
S(id="d07", start=116.0, dur=3.1, kind="card", fx=["D3"], src="Ảnh chụp trích đoạn bài The Leader 25/09/2026", foot="Trích nguyên văn theleader.vn (25/09/2026)", enter="T3",
  doc={"img": "assets/doc/doc_sign.png", "imgW": 1400, "top": 420, "h": 980, "hl": [{"y": 1260, "h": 606, "t": 0.6}], "zoom": {"t": 0.2, "d": 1.4, "y": -420, "scale": 1.12}})
S(id="d08", start=119.1, dur=2.65, kind="foot", fx=["F3", "F1"], media="assets/ge/n_hcm.mp4", src="Google Earth: đô thị (minh hoạ quy mô, không phải dự án Longfor)", foot=GE + " · hình minh hoạ", enter="T3", whipDir="R",
  kw=[{"t": 0.3, "d": 2.2, "lines": ["LONGFOR", "*TỪ *1993"], "pos": "mid"}])
S(id="d09", start=121.75, dur=2.65, kind="foot", fx=["D1", "F2"], media="assets/img/p9.jpg", move="panL", focus="40% 50%", src="Ảnh: The Leader 25/09/2026", foot="Nguồn: The Leader (25/09/2026)", enter="T5",
  big={"t": 0.3, "d": 2.2, "num": 1300, "unit": "dự án", "label": "đã phát triển (hơn)"})
S(id="d10", start=124.4, dur=2.6, kind="map", fx=["M7", "D3"], src="Bản đồ + vệ tinh Esri", enter="T5",
  keys=[[0, 10.9666, 106.6985, 13.0], [2.6, 10.9666, 106.6985, 12.6]],
  layers=[SITEL("d10-site")], show=[{"id": "d10-site", "t": 0, "d": .2}], rings=[{"pt": "oneera", "lat": 10.97, "t": 0.2, "km": [1, 2, 3]}],
  labels=[{"at": "oneera", "lx": 0, "ly": -330, "align": "c", "big": "1,1 TRIỆU", "text": "căn Longfor đã bàn giao", "color": "yel", "t": 0.5, "d": 2.0}])
S(id="d11", start=127.0, dur=2.1, kind="card", fx=["D2"], media="assets/ge/n_hcm.mp4", media_start=1.0, dim=0.5, src="So sánh trên nền Google Earth", foot="Tính từ số liệu The Leader, CafeF", enter="T3",
  bar={"t": 0.0, "d": 2.0, "label": "Longfor giao mỗi năm", "value": 30000, "max": 30000, "unit": "căn", "sub": "One Era cả dự án: 4.039 sản phẩm", "top": 780})
S(id="d12", start=129.1, dur=5.9, kind="foot", fx=["D1", "F2"], media="assets/img/p10.jpg", move="panR", focus="35% 45%", src="Ảnh: The Leader 25/09/2026", foot="Nguồn: The Leader (25/09/2026)", enter="T3", whipDir="R", busy=True,
  kw=[{"t": 0.2, "d": 2.2, "lines": ["DOANH SỐ", "*2025"], "pos": "high"}],
  big={"t": 4.4, "d": 1.4, "num": 10, "unit": "tỷ USD", "label": "doanh số bán năm 2025 (gần)"})
S(id="d13", start=135.0, dur=5.6, kind="card", fx=["D6"], media="assets/img/p7.jpg", move="push", dim=0.6, src="Tường đối tác trên nền phối cảnh", foot="Nguồn: The Leader (25/09/2026)", enter="T5", busy=True,
  wall={"t": 0, "top": 600, "tiles": [{"t": 0.2, "name": "Longfor", "sub": "cùng quy hoạch", "hl": True}, {"t": 2.5, "name": "Surbana Jurong", "sub": "tư vấn quy hoạch"},
                                       {"t": 4.6, "name": "Coteccons", "sub": "hạ tầng"}]})
S(id="d14", start=140.6, dur=3.0, kind="card", fx=["D3"], src="Ảnh chụp trích đoạn bài The Leader", foot="Trích nguyên văn theleader.vn (25/09/2026)", enter="T3",
  doc={"img": "assets/doc/doc_leader.png", "imgW": 1400, "top": 420, "h": 980, "hl": [{"y": 1332, "h": 534, "t": 0.6}], "zoom": {"t": 0.1, "d": 1.3, "y": -560, "scale": 1.12}})
# ================= 2:24–2:50 vị trí & kết nối =================
S(id="e01", start=143.6, dur=3.95, kind="foot", fx=["F3", "F1"], media="assets/ge/g3.mp4", media_start=0.5, src="Google Earth: Vành đai 3 cạnh dự án", foot=GE, enter="T5",
  kw=[{"t": 1.7, "d": 2.1, "lines": ["MỘT NỬA", "*CÂU *CHUYỆN"], "pos": "mid"}])
S(id="e02", start=147.55, dur=3.85, kind="map", fx=["M2", "M5"], src="Bản đồ + vệ tinh Esri", zoomBlur=True, enter="T5",
  keys=[[0, 10.92, 106.73, 11.0], [1.0, 10.9666, 106.6985, 14.6], [3.85, 10.9666, 106.6985, 15.5]],
  layers=[SITEL("e02-site")], show=[{"id": "e02-site", "t": 0.8, "d": .3}], draw=[{"id": "e02-site", "t": 0.8, "d": .5}],
  ground=[{"at": "oneera", "text": "VỊ TRÍ", "t": 0.7, "d": 3.0}])
S(id="e03", start=151.4, dur=5.0, kind="map", fx=["M6", "M9"], src="Bản đồ + vệ tinh Esri", foot=OES, enter="T5", busy=True,
  keys=[[0, 10.9650, 106.6995, 15.25], [5.0, 10.9655, 106.6995, 15.15]],
  layers=[SITEL("e03-site"), lay("lines:ql13", "route", "e03-ql", 6), lay("lines:vd3", "route", "e03-vd", 6), lay("lines:mptv", "route", "e03-mp", 6), lay("lines:ntmk", "route", "e03-nt", 5)],
  show=[{"id": "e03-site", "t": 0, "d": .1}], draw=[{"id": "e03-site", "t": 0, "d": .2}, {"id": "e03-ql", "t": 0.2, "d": 1.0}, {"id": "e03-vd", "t": 1.4, "d": 0.9}, {"id": "e03-mp", "t": 2.2, "d": 0.9}, {"id": "e03-nt", "t": 3.8, "d": 0.8}],
  movers=[{"path": "e03-ql", "t": 0.2, "d": 1.4, "icon": "car"}, {"path": "e03-vd", "t": 1.4, "d": 1.3, "icon": "car"}, {"path": "e03-mp", "t": 2.2, "d": 1.3, "icon": "car"}, {"path": "e03-nt", "t": 3.8, "d": 1.1, "icon": "car"}],
  labels=[{"at": "l_ql13", "lx": -120, "ly": -120, "big": "QL13", "color": "route", "t": 0.5, "d": 4.4}, {"at": "l_vd3", "lx": 70, "ly": -150, "big": "VÀNH ĐAI 3", "color": "route", "t": 1.6, "d": 3.3},
          {"at": "l_mptv", "lx": -180, "ly": 130, "align": "c", "text": "Mỹ Phước – Tân Vạn", "color": "route", "t": 2.4, "d": 2.5}, {"at": "l_ntmk", "lx": -60, "ly": 150, "align": "c", "text": "Nguyễn Thị Minh Khai", "color": "route", "t": 3.9, "d": 1.0}])
S(id="e04", start=156.4, dur=3.2, kind="foot", fx=["F3", "F1"], media="assets/ge/n_ql13.mp4", src="Google Earth: Quốc lộ 13 qua dự án", foot=GE, enter="T3",
  kw=[{"t": 1.9, "d": 1.2, "lines": ["2 TUYẾN", "*METRO"], "pos": "mid", "accent": "#E04BD6"}])
S(id="e05", start=159.6, dur=3.7, kind="map", fx=["M6", "M2"], src="Bản đồ + vệ tinh Esri · sơ đồ hướng tuyến minh hoạ", foot="Hướng tuyến metro: sơ đồ minh hoạ theo quy hoạch, không phải bản vẽ tuyến", enter="T5",
  keys=[[0, 10.9666, 106.6985, 13.6], [1.2, 10.875, 106.745, 12.05], [3.7, 10.87, 106.745, 11.9]], zoomBlur=True,
  layers=[SITEL("e05-site")], show=[{"id": "e05-site", "t": 0, "d": .1}],
  links=[{"a": "site_w", "b": "taodan", "bend": 0.12, "kind": "route", "id": "e05-m1", "w": 6}, {"a": "site_e", "b": "suoitien", "bend": -0.15, "kind": "route", "id": "e05-m2", "w": 6}],
  draw=[{"id": "e05-m1", "t": 1.2, "d": 1.2}, {"id": "e05-m2", "t": 2.3, "d": 1.2}],
  movers=[{"path": "e05-m1", "t": 1.2, "d": 1.4, "icon": "train"}, {"path": "e05-m2", "t": 2.3, "d": 1.3, "icon": "train"}],
  labels=[{"at": "taodan", "lx": -40, "ly": 130, "align": "c", "big": "TAO ĐÀN", "color": "route", "t": 1.9, "d": 1.7}, {"at": "suoitien", "lx": -60, "ly": 120, "align": "c", "big": "SUỐI TIÊN", "color": "route", "t": 2.9, "d": 0.8}])
S(id="e06", start=163.3, dur=2.4, kind="foot", fx=["F1", "D3"], media="assets/ge/n_metro.mp4", src="Google Earth: ga Suối Tiên (metro số 1, đang vận hành)", foot=GE, enter="T5",
  callouts=[{"x": 560, "y": 900, "lx": 0, "ly": -200, "align": "c", "big": "SUỐI TIÊN", "text": "ga metro số 1", "color": "route", "t": 0.2, "d": 2.1}])
S(id="e07", start=165.7, dur=4.4, kind="map", fx=["M7", "M3"], src="Bản đồ + vệ tinh Esri", foot=OES, enter="T5", busy=True,
  keys=[[0, 11.02, 106.6985, 12.35], [4.4, 11.02, 106.6985, 12.15]], tilt=[0, 1.2, 0, 30],
  layers=[SITEL("e07-site")], show=[{"id": "e07-site", "t": 0, "d": .1}], rings=[{"pt": "oneera", "lat": 10.97, "t": 0.2, "km": [5, 10, 15]}],
  labels=[{"at": "ring_5", "lx": 0, "ly": -50, "align": "c", "big": "5 KM", "color": "yel", "t": 0.7, "d": 3.5}, {"at": "ring_10", "lx": 0, "ly": -50, "align": "c", "big": "10 KM", "color": "yel", "t": 1.2, "d": 3.0}, {"at": "ring_15", "lx": 0, "ly": -50, "align": "c", "big": "15 KM", "color": "yel", "t": 1.6, "d": 2.6},
          {"at": "oneera", "lx": 0, "ly": 300, "align": "c", "big": "42 HA", "text": "công viên sinh thái liền kề", "color": "green", "t": 0.3, "d": 4.0}])
# ================= 2:50–3:16 tiện ích =================
S(id="f01", start=170.1, dur=2.9, kind="foot", fx=["F3", "F1"], media="assets/ge/n_site_low.mp4", media_start=0.4, src="Google Earth: công trường One Era", foot=GE, enter="T3",
  kw=[{"t": 0.3, "d": 2.5, "lines": ["TIỆN ÍCH", "*CÓ *TÊN"], "pos": "mid", "accent": "#FACC15"}])
S(id="f02", start=173.0, dur=5.5, kind="map", fx=["M8", "M3"], src="Bản đồ + vệ tinh Esri · vị trí ghim minh hoạ", foot="Vị trí ghim minh hoạ trong khu đô thị", enter="T5", busy=True,
  keys=[[0, 10.9666, 106.6985, 16.2], [5.5, 10.9666, 106.6985, 16.35]], tilt=[0, 1.0, 0, 35], orbit=[0, 5.5, -6, 6],
  layers=[SITEL("f02-site")], show=[{"id": "f02-site", "t": 0, "d": .1}], draw=[{"id": "f02-site", "t": 0, "d": .2}],
  pins=[{"at": "p_vas", "text": "VAS Saigon", "t": 0.0, "left": True}, {"at": "p_kindup", "text": "Kindup", "t": 2.7}, {"at": "p_meret", "text": "Meret", "t": 4.6}])
S(id="f03", start=178.5, dur=3.3, kind="foot", fx=["F3", "F2"], media="assets/img/p6.jpg", move="panU", focus="50% 50%", src="Ảnh phối cảnh CĐT (CafeF)", foot=R, enter="T3", whipDir="R",
  kw=[{"t": 1.0, "d": 2.2, "lines": ["TTTM ·", "*VĂN *PHÒNG", "*HẠNG *A"], "pos": "mid", "accent": "#FACC15"}])
S(id="f04", start=181.8, dur=3.8, kind="foot", fx=["D3", "F2"], media="assets/img/p1.jpg", move="panR", focus="20% 50%", src="Ảnh: CafeF 03/11/2026 – khách tham quan", foot="Ảnh: CafeF (03/11/2026)", enter="T3",
  callouts=[{"x": 420, "y": 1040, "lx": 120, "ly": -260, "big": "KHÔNG CHỈ", "text": "đứng nhìn sa bàn", "color": "yel", "t": 1.6, "d": 2.0}])
S(id="f05", start=185.6, dur=1.9, kind="map", fx=["M4"], src="Bản đồ + vệ tinh Esri", enter="T5",
  keys=[[0, 10.9666, 106.6985, 16.6], [1.9, 10.9666, 106.6985, 17.0]],
  layers=[lay("lines:site", "green", "f05-g", 6, True, True)], draw=[{"id": "f05-g", "t": 0, "d": 0.8}], show=[{"id": "f05-g-fill", "t": 0.6, "d": .4}],
  labels=[{"at": "site_n", "lx": 0, "ly": -260, "align": "c", "big": "ONE PARK", "text": "~1 ha", "color": "green", "t": 0.2, "d": 1.6}])
S(id="f06", start=187.5, dur=5.2, kind="foot", fx=["T4", "F3", "F1"], media="assets/ge/g2.mp4", media_start=1.2, src="Google Earth: công trường One Era (One Park)", foot=GE, enter="T4", busy=True,
  kw=[{"t": 0.9, "d": 1.6, "lines": ["QUẢNG TRƯỜNG", "*2 *HỒ *BƠI"], "pos": "mid", "accent": "#4ADE80"}, {"t": 2.6, "d": 2.4, "lines": ["CÀ PHÊ", "*SÂN *CHƠI"], "pos": "mid", "accent": "#4ADE80"}])
S(id="f07", start=192.7, dur=3.7, kind="foot", fx=["D1", "F2"], media="assets/img/p1.jpg", move="pull", focus="85% 50%", src="Ảnh: CafeF 03/11/2026 – ngày khai trương", foot="Nguồn & ảnh: CafeF (03/11/2026)", enter="T3", whipDir="R",
  big={"t": 1.5, "d": 2.1, "num": 2500, "unit": "người", "label": "đến dự ngày khai trương (khoảng)"})
# ================= 3:16–3:49 sản phẩm =================
S(id="g01", start=196.4, dur=3.25, kind="map", fx=["M3", "M5"], src="Bản đồ + vệ tinh Esri", enter="T5",
  keys=[[0, 10.9666, 106.6985, 15.9], [3.25, 10.9666, 106.6985, 16.1]], tilt=[0, 1.0, 0, 40], orbit=[0, 3.25, 10, -6],
  layers=[SITEL("g01-site")], draw=[{"id": "g01-site", "t": 0, "d": .4}], show=[{"id": "g01-site-fill", "t": 0.3, "d": .3}],
  ground=[{"at": "oneera", "text": "CENTRAL DISTRICT", "t": 0.3, "d": 2.8, "size": 70}])
S(id="g02", start=199.65, dur=3.85, kind="foot", fx=["F3", "F2"], media="assets/img/p4.jpg", move="pull", focus="50% 50%", src="Ảnh phối cảnh CĐT (CafeF)", foot=R, enter="T3",
  kw=[{"t": 0.3, "d": 3.3, "lines": ["PHÂN KHU", "*THẤP *TẦNG ĐẦU TIÊN"], "pos": "low", "accent": "#2FD3E0"}])
S(id="g03", start=203.5, dur=4.4, kind="foot", fx=["D3", "F2"], media="assets/img/p3.jpg", move="panR", focus="30% 50%", src="Ảnh phối cảnh CĐT (CafeF)", foot=R, enter="T3", whipDir="R",
  callouts=[{"x": 520, "y": 1000, "lx": 0, "ly": -330, "align": "c", "big": "TOWNHOUSE", "text": "1 trệt · 2 lầu", "color": "proj", "t": 0.5, "d": 2.0},
            {"x": 520, "y": 1000, "lx": 0, "ly": -330, "align": "c", "big": "NHIỆT ĐỚI", "text": "đương đại", "color": "green", "t": 2.6, "d": 1.6}])
S(id="g04", start=207.9, dur=3.55, kind="map", fx=["M9", "M4"], src="Bản đồ + vệ tinh Esri", foot=OES, enter="T5",
  keys=[[0, 10.9680, 106.7010, 16.3], [3.55, 10.9682, 106.7012, 16.45]],
  layers=[lay("lines:canal", "water", "g04-c", 6)], draw=[{"id": "g04-c", "t": 0.1, "d": 1.4}],
  movers=[{"path": "g04-c", "t": 0.3, "d": 3.0, "icon": "boat"}],
  labels=[{"at": "l_canal", "lx": -110, "ly": -120, "big": "KÊNH SUỐI CÁT", "color": "proj", "t": 2.6, "d": 0.9}])
S(id="g05", start=211.45, dur=5.15, kind="foot", fx=["D1", "F1"], media="assets/ge/n_site_low.mp4", media_start=0.0, src="Google Earth: công trường One Era", foot=OES, enter="T3", busy=True,
  kw=[{"t": 0.2, "d": 2.6, "lines": ["DẠO BỘ", "*ĐẠP *XE"], "pos": "high", "accent": "#2FD3E0"}],
  big={"t": 3.7, "d": 1.3, "num": 2.6, "dec": 1, "unit": "km", "label": "dọc hai bờ kênh (khoảng)", "accent": "#2FD3E0"})
S(id="g06", start=216.6, dur=4.5, kind="foot", fx=["F3", "F2"], media="assets/img/p6.jpg", move="panL", focus="70% 50%", src="Ảnh phối cảnh CĐT (CafeF)", foot=R, enter="T3", whipDir="R",
  kw=[{"t": 0.4, "d": 2.0, "lines": ["SHOPHOUSE"], "pos": "high"}, {"t": 2.4, "d": 2.0, "lines": ["+ TẦNG LỬNG", "*Ở *+ *KINH *DOANH"], "pos": "high"}], busy=True)
S(id="g07", start=221.1, dur=3.5, kind="foot", fx=["D3", "F2"], media="assets/img/p5.jpg", move="push", focus="60% 50%", src="Ảnh phối cảnh CĐT (CafeF)", foot=R, enter="T5",
  callouts=[{"x": 540, "y": 1240, "lx": 0, "ly": -170, "align": "c", "big": "2 MẶT TIỀN", "text": "đại lộ nội khu 25 m", "color": "route", "t": 0.2, "d": 3.2}])
S(id="g08", start=224.6, dur=4.5, kind="map", fx=["M3", "D3"], src="Bản đồ + vệ tinh Esri · vị trí minh hoạ", enter="T5",
  keys=[[0, 10.9666, 106.6985, 16.0], [4.5, 10.9666, 106.6985, 16.2]], tilt=[0, 1.0, 0, 40], orbit=[0, 4.5, -10, 10],
  layers=[SITEL("g08-site")], draw=[{"id": "g08-site", "t": 0, "d": .3}], show=[{"id": "g08-site-fill", "t": 0.2, "d": .3}],
  labels=[{"at": "site_n", "lx": 0, "ly": -260, "align": "c", "big": "ONE PARK", "text": "mặt sau shophouse", "color": "green", "t": 1.9, "d": 2.4}])
# ================= 3:49–4:17 lộ trình & kết =================
S(id="h01", start=229.1, dur=5.3, kind="foot", fx=["D2", "F1"], media="assets/ge/g4.mp4", media_start=0.0, src="Google Earth: toàn cảnh khu dự án", foot=OES, enter="T3", busy=True,
  bar={"t": 0.7, "d": 4.5, "label": "Mở màn", "value": 357, "max": 4039, "unit": "căn", "sub": "trong hơn 4.000 sản phẩm", "top": 760})
S(id="h02", start=234.4, dur=5.2, kind="card", fx=["D5"], media="assets/ge/g4.mp4", media_start=5.2, dim=0.55, src="Timeline trên nền Google Earth", foot="Nguồn: CafeF (07/11/2026)", enter="T3", busy=True,
  timeline={"t": 0.0, "y": 960, "events": [{"t": 0.3, "x": 100, "date": "09/2025", "text": "khởi công"}, {"t": 0.9, "x": 380, "date": "10/2026", "text": "khai trương"},
                                           {"t": 3.2, "x": 650, "date": "QUÝ IV/2028", "text": "bàn giao căn đầu tiên"}]})
S(id="h03", start=239.6, dur=7.0, kind="map", fx=["M2", "M7"], src="Bản đồ + vệ tinh Esri", enter="T5", busy=True, zoomBlur=True,
  keys=[[0, 10.9666, 106.6985, 15.8], [2.0, 10.95, 106.70, 12.6], [4.5, 10.85, 106.78, 9.9], [7.0, 10.86, 106.80, 9.55]],
  layers=[lay("prov:BD_cu", "adm", "h03-bd", 5, True, False), lay("prov:TPHCM_cu", "adm", "h03-hcm", 4, False, False), SITEL("h03-site"),
          lay("lines:ql13", "route", "h03-ql", 5), lay("lines:vd3", "route", "h03-vd", 5), lay("lines:canal", "water", "h03-c", 5)],
  links=[{"a": "site_w", "b": "taodan", "bend": 0.12, "kind": "route", "id": "h03-m1", "w": 5}, {"a": "site_e", "b": "suoitien", "bend": -0.15, "kind": "route", "id": "h03-m2", "w": 5}],
  rings=[{"pt": "oneera", "lat": 10.97, "t": 3.0, "km": [10, 20]}],
  show=[{"id": "h03-site", "t": 0, "d": .1}, {"id": "h03-bd", "t": 2.6, "d": .6}, {"id": "h03-hcm", "t": 3.2, "d": .6}],
  draw=[{"id": "h03-site", "t": 0, "d": .2}, {"id": "h03-ql", "t": 0.2, "d": .8}, {"id": "h03-vd", "t": 0.4, "d": .8}, {"id": "h03-c", "t": 0.6, "d": .8}, {"id": "h03-m1", "t": 3.4, "d": 1.0}, {"id": "h03-m2", "t": 3.8, "d": 1.0}],
  kw=[{"t": 1.0, "d": 2.6, "lines": ["KHOẢNG TRỐNG", "*THẤP *TẦNG"], "pos": "high"}, {"t": 4.0, "d": 2.8, "lines": ["PHÉP THỬ", "*CUỐI *CÙNG"], "pos": "high"}])
S(id="h04", start=246.6, dur=3.6, kind="foot", fx=["F3", "F1"], media="assets/ge/n_wide.mp4", src="Google Earth: toàn cảnh Đông Bắc TP.HCM", foot=GE, enter="T5",
  kw=[{"t": 0.6, "d": 2.8, "lines": ["CƯ DÂN", "*ĐẦU *TIÊN"], "pos": "mid"}])
S(id="h05", start=250.2, dur=3.1, kind="foot", fx=["D3", "F2"], media="assets/img/p5.jpg", move="pull", focus="45% 50%", src="Ảnh phối cảnh CĐT (CafeF)", foot=R, enter="DIS",
  callouts=[{"x": 560, "y": 1150, "lx": 0, "ly": -130, "align": "c", "big": "SÁNG ĐÈN", "text": "dãy shophouse đại lộ 25 m", "color": "yel", "t": 0.3, "d": 2.6}])
S(id="h06", start=253.3, dur=4.14, kind="map", fx=["M4", "M5", "F3"], src="Bản đồ + vệ tinh Esri", enter="T5", exit="none",
  keys=[[0, 10.9666, 106.6985, 15.4], [4.14, 10.9666, 106.6985, 15.8]], tilt=[0, 1.5, 0, 38],
  layers=[SITEL("h06-site")], draw=[{"id": "h06-site", "t": 0, "d": 1.0}], show=[{"id": "h06-site-fill", "t": 0.9, "d": .5}],
  ground=[{"at": "oneera", "text": "ONE ERA", "t": 1.0, "d": 3.1}],
  kw=[{"t": 0.2, "d": 3.9, "lines": ["TỪ TRÊN GIẤY", "*ĐẾN *NGƯỜI", "*THẬT *SỐNG"], "pos": "high", "accent": "#2FD3E0"}])
# ===== cân lại tỉ lệ bản đồ / footage / thẻ =====
def R_(id, **k):
    i = next(n for n, x in enumerate(sh) if x["id"] == id); keep = {q: sh[i][q] for q in ("id", "start", "dur")}; sh[i] = dict(keep, **k)
def U_(id, **k): next(x for x in sh if x["id"] == id).update(k)
R_("a01", kind="map", fx=["M1", "D1"], src="Vệ tinh Esri z7→z9 + mây tổng hợp (bay xuyên mây)", foot=CBRE, enter="T5", clouds=[0, 1.5],
   keys=[[0, 10.95, 106.80, 7.4], [2.45, 10.82, 106.76, 9.3]], big={"t": 0.05, "d": 2.3, "num": 6573, "unit": "căn hộ", "label": "mở bán mới · Quý II/2026"})
R_("a05", kind="map", fx=["D4"], src="Bản đồ + vệ tinh Esri", foot=CBRE, enter="T3",
   keys=[[0, 10.86, 106.80, 9.15], [3.05, 10.86, 106.80, 9.35]], layers=[lay("prov:TPHCM_moi", "adm", "a05-moi", 5, True, False)], show=[{"id": "a05-moi", "t": 0, "d": .3, "to": .55}],
   stack={"t": 0.0, "top": 700, "rows": [{"t": 0.1, "num": 6573, "unit": "căn hộ", "label": "mở bán mới"}, {"t": 0.5, "num": 1934, "unit": "nhà liền thổ", "label": "mở bán mới"}]})
U_("b07", fx=["M3", "M5", "D3"], kw=[], ground=[{"at": "oneera", "text": "ONE ERA", "t": 0.25, "d": 4.2}],
   labels=[{"at": "site_n", "lx": 0, "ly": -300, "align": "c", "big": "AI ĐỨNG SAU?", "color": "proj", "t": 2.6, "d": 2.0}])
R_("c06", kind="map", fx=["M3", "D1"], src="Bản đồ + vệ tinh Esri", foot=OES, enter="T3",
   keys=[[0, 10.9666, 106.6985, 15.7], [3.95, 10.9666, 106.6985, 16.0]], tilt=[0, 1.4, 0, 42], orbit=[0, 3.95, 14, -4],
   layers=[SITEL("c06-site")], draw=[{"id": "c06-site", "t": 0.1, "d": 0.8}], show=[{"id": "c06-site-fill", "t": 0.8, "d": .4}],
   ground=[{"at": "oneera", "text": "MẬT ĐỘ", "t": 0.9, "d": 1.8}],
   big={"t": 2.9, "d": 1.0, "num": 25, "unit": "%", "label": "mật độ xây dựng nhà ở", "pos": "mid"})
U_("c06", fx=["M3", "M5", "D1"])
R_("d11", kind="map", fx=["D2"], src="Bản đồ + vệ tinh Esri", foot="Tính từ số liệu The Leader, CafeF", enter="T5",
   keys=[[0, 10.9666, 106.6985, 12.8], [2.1, 10.9666, 106.6985, 12.5]], layers=[SITEL("d11-site")], show=[{"id": "d11-site", "t": 0, "d": .1}],
   bar={"t": 0.0, "d": 2.0, "label": "Longfor giao mỗi năm", "value": 30000, "max": 30000, "unit": "căn", "sub": "One Era cả dự án: 4.039 sản phẩm", "top": 780})
R_("f04", kind="map", fx=["M3", "D3"], src="Bản đồ + vệ tinh Esri", foot=OES, enter="T3",
   keys=[[0, 10.9666, 106.6985, 15.9], [3.8, 10.9666, 106.6985, 16.15]], tilt=[0, 1.0, 15, 38], orbit=[0, 3.8, 10, -10],
   layers=[SITEL("f04-site")], draw=[{"id": "f04-site", "t": 0, "d": .5}], show=[{"id": "f04-site-fill", "t": 0.3, "d": .3, "to": .7}],
   labels=[{"at": "site_n", "lx": 0, "ly": -300, "align": "c", "big": "KHÔNG CHỈ", "text": "đứng nhìn sa bàn", "color": "yel", "t": 1.4, "d": 2.2}])
U_("g04", fx=["M9"])
U_("e07", fx=["M7"], tilt=None)
R_("g05", kind="map", fx=["D1", "M3", "D3"], src="Bản đồ + vệ tinh Esri", foot=OES, enter="T5", busy=True,
   keys=[[0, 10.9680, 106.7010, 16.2], [5.15, 10.9672, 106.7000, 15.8]], tilt=[0, 1.2, 0, 36],
   layers=[SITEL("g05-site"), lay("lines:canal", "water", "g05-c", 7)], show=[{"id": "g05-site", "t": 0, "d": .1}], draw=[{"id": "g05-c", "t": 0.2, "d": 1.6}, {"id": "g05-site", "t": 0, "d": .2}],
   labels=[{"at": "l_canal", "lx": -120, "ly": -170, "big": "DẠO BỘ", "text": "đạp xe ven kênh", "color": "proj", "t": 0.3, "d": 3.1}],
   big={"t": 3.7, "d": 1.3, "num": 2.6, "dec": 1, "unit": "km", "label": "dọc hai bờ kênh (khoảng)", "accent": "#2FD3E0", "pos": "high"})
for x in sh:
    x["fx"] = ["C1" if (f == "D3" and x["kind"] == "foot") else f for f in x["fx"]]
    if x.get("doc"): x["fx"] = ["DOC"]
def KW(id): return next(x for x in sh if x["id"] == id)
KW("a04")["kw"] = KW("a04")["kw"][:1]; KW("a07")["kw"] = KW("a07")["kw"][:1]; KW("b08")["kw"] = KW("b08")["kw"][:1]
KW("f06")["kw"] = KW("f06")["kw"][:1]; KW("h03")["kw"] = KW("h03")["kw"][1:]
for i in ("b02", "b05", "d12"): KW(i)["kw"] = []
U_("c01", kw=[], fx=["M3", "M4", "M5"], ground=[{"at": "oneera", "text": "QUY MÔ", "t": 0.3, "d": 2.0}])
KW("d03")["kw"] = [{"t": 0.7, "d": 3.1, "lines": ["KUMAGAI GUMI", "*NTT *URBAN"], "pos": "mid"}]
KW("g06")["kw"] = [{"t": 0.4, "d": 2.6, "lines": ["SHOPHOUSE", "*+ *TẦNG *LỬNG"], "pos": "high"}]
U_("d08", kw=[], fx=["C1", "F1"], callouts=[{"x": 560, "y": 1000, "lx": 0, "ly": -300, "align": "c", "big": "LONGFOR", "text": "phát triển bất động sản từ 1993", "color": "adm", "t": 0.3, "d": 2.2}])
U_("e01", kw=[], fx=["C1", "F1"], callouts=[{"x": 540, "y": 1050, "lx": 0, "ly": -330, "align": "c", "big": "VỊ TRÍ", "text": "một nửa câu chuyện còn lại", "color": "w", "t": 1.6, "d": 2.2}])
U_("f01", kw=[], fx=["C1", "F1"], callouts=[{"x": 540, "y": 1050, "lx": 0, "ly": -330, "align": "c", "big": "TIỆN ÍCH", "text": "có tên, có thương hiệu", "color": "yel", "t": 0.3, "d": 2.4}])
U_("h04", kw=[], fx=["C1", "F1"], callouts=[{"x": 540, "y": 1080, "lx": 0, "ly": -360, "align": "c", "big": "CƯ DÂN ĐẦU TIÊN", "text": "sẽ trả lời câu hỏi", "color": "w", "t": 0.6, "d": 2.8}])
U_("g02", kw=[], fx=["C1", "F2"], callouts=[{"x": 540, "y": 1100, "lx": 0, "ly": -380, "align": "c", "big": "PHÂN KHU THẤP TẦNG", "text": "đầu tiên của One Era", "color": "proj", "t": 0.3, "d": 3.3}])
U_("f03", kw=[], fx=["C1", "F2"], callouts=[{"x": 540, "y": 1150, "lx": 0, "ly": -400, "align": "c", "big": "TTTM", "text": "văn phòng hạng A", "color": "yel", "t": 0.6, "d": 2.6}])
U_("e04", kw=[], fx=["C1", "F1"], callouts=[{"x": 540, "y": 1100, "lx": 0, "ly": -380, "align": "c", "big": "2 TUYẾN METRO", "text": "theo quy hoạch", "color": "route", "t": 1.0, "d": 2.1}])
KW("c06")["big"].update(t=2.3, d=1.6); KW("b03")["labels"][0].update(t=0.5, d=1.95)
KW("d02")["wall"]["tiles"][2]["t"] = 3.3
# giữ nhãn / số / chú thích đến hết shot để kịp đọc
for x in sh:
    for l in x.get("labels", []) + x.get("callouts", []):
        if l is (x.get("callouts") or [None])[0] and len(x.get("callouts", [])) > 1: continue
        if not any(o is not l and o.get("t", 0) > l["t"] and o.get("at") == l.get("at") and o.get("x") == l.get("x") for o in x.get("labels", []) + x.get("callouts", [])):
            l["d"] = max(l["d"], x["dur"] - l["t"])
    if x.get("big"): x["big"]["d"] = max(x["big"]["d"], x["dur"] - x["big"]["t"])
for x in sh:   # dùng chữ động thì phải khai F3
    if x.get("kw") and "F3" not in x["fx"]: x["fx"].append("F3")
# chữ động: chỉ giữ trên màn hình đủ đọc (≤1,7 s mỗi cụm) để F3 không chiếm >15%
for x in sh:
    for k in x.get("kw", []):
        nw = sum(len(l.split()) for l in k["lines"]); k["d"] = min(k["d"], 3.8 if x["id"] == "h06" else max(2.0, 0.9 + 0.35 * nw))
# không lặp kiểu vào cảnh (ngoài T5) ở hai cảnh liền nhau
for a, b in zip(sh, sh[1:]):
    if b.get("enter", "T5") == a.get("enter", "T5") and b.get("enter") not in ("T5", None): b["enter"] = "T5"
# điểm cắt bám phách nhạc (100 BPM, lệch pha 0,13 s): dịch ≤0,2 s
BEAT0, BP = 0.13, 0.6
for a, b in zip(sh, sh[1:]):
    nb = round(BEAT0 + round((b["start"] - BEAT0) / BP) * BP, 3)
    if abs(nb - b["start"]) <= 0.2 and nb - a["start"] > 1.6:
        a["dur"] = round(nb - a["start"], 3); end = b["start"] + b["dur"]; b["start"] = nb; b["dur"] = round(end - nb, 3)
for a, b in zip(sh, sh[1:]):
    assert abs(a["start"] + a["dur"] - b["start"]) < 1e-6, (a["id"], b["id"], a["start"] + a["dur"], b["start"])
out = {"duration": 257.44, "audio": "assets/mix.wav", "gsap": "assets/lib/gsap.min.js", "sat": SAT, "points": PTS, "site": SITE, "shots": sh}
json.dump(out, open("proj/shots.json", "w"), ensure_ascii=False, indent=1)
print(len(sh), "shots; end", sh[-1]["start"] + sh[-1]["dur"])
```

## FILE: templates/one-era-motion/sfx_events.json

```json
[
{
"t": 0,
"sfx": "impact.wav",
"db": -6
},
{
"t": 0,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 2.41,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 2.63,
"sfx": "pop.wav",
"db": -2
},
{
"t": 4.93,
"sfx": "impact.wav",
"db": -6
},
{
"t": 6.53,
"sfx": "whoosh.wav",
"db": -9
},
{
"t": 6.93,
"sfx": "pop.wav",
"db": -4
},
{
"t": 7.81,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 8.88,
"sfx": "pop.wav",
"db": -2
},
{
"t": 12.95,
"sfx": "impact.wav",
"db": -6
},
{
"t": 13.05,
"sfx": "pop.wav",
"db": -2
},
{
"t": 13.45,
"sfx": "pop.wav",
"db": -2
},
{
"t": 16.0,
"sfx": "whoosh.wav",
"db": -2
},
{
"t": 16.9,
"sfx": "pop.wav",
"db": -4
},
{
"t": 18.28,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 18.7,
"sfx": "pop.wav",
"db": -2
},
{
"t": 22.93,
"sfx": "impact.wav",
"db": -6
},
{
"t": 22.93,
"sfx": "whoosh.wav",
"db": -9
},
{
"t": 23.08,
"sfx": "pop.wav",
"db": -4
},
{
"t": 25.48,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 25.7,
"sfx": "pop.wav",
"db": -2
},
{
"t": 28.1,
"sfx": "impact.wav",
"db": -6
},
{
"t": 28.2,
"sfx": "pop.wav",
"db": -4
},
{
"t": 30.93,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 31.65,
"sfx": "pop.wav",
"db": -2
},
{
"t": 34.7,
"sfx": "whoosh.wav",
"db": -2
},
{
"t": 38.1,
"sfx": "pop.wav",
"db": -4
},
{
"t": 39.73,
"sfx": "impact.wav",
"db": -6
},
{
"t": 39.83,
"sfx": "whoosh.wav",
"db": -9
},
{
"t": 40.23,
"sfx": "pop.wav",
"db": -4
},
{
"t": 40.73,
"sfx": "riser.wav",
"db": -3
},
{
"t": 42.28,
"sfx": "pop.wav",
"db": -2
},
{
"t": 45.01,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 45.73,
"sfx": "impact.wav",
"db": -2
},
{
"t": 48.4,
"sfx": "impact.wav",
"db": -6
},
{
"t": 48.75,
"sfx": "impact.wav",
"db": 0
},
{
"t": 51.13,
"sfx": "impact.wav",
"db": -6
},
{
"t": 51.38,
"sfx": "impact.wav",
"db": -2
},
{
"t": 53.73,
"sfx": "pop.wav",
"db": -4
},
{
"t": 55.81,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 56.73,
"sfx": "pop.wav",
"db": -2
},
{
"t": 61.93,
"sfx": "impact.wav",
"db": -6
},
{
"t": 62.03,
"sfx": "whoosh.wav",
"db": -9
},
{
"t": 62.23,
"sfx": "impact.wav",
"db": -2
},
{
"t": 64.21,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 64.63,
"sfx": "riser.wav",
"db": -8
},
{
"t": 69.73,
"sfx": "impact.wav",
"db": -6
},
{
"t": 70.23,
"sfx": "impact.wav",
"db": 0
},
{
"t": 72.45,
"sfx": "impact.wav",
"db": -6
},
{
"t": 73.05,
"sfx": "pop.wav",
"db": -4
},
{
"t": 75.13,
"sfx": "impact.wav",
"db": -6
},
{
"t": 76.08,
"sfx": "impact.wav",
"db": -3
},
{
"t": 76.78,
"sfx": "impact.wav",
"db": -3
},
{
"t": 77.38,
"sfx": "impact.wav",
"db": -3
},
{
"t": 78.01,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 79.03,
"sfx": "impact.wav",
"db": -2
},
{
"t": 80.43,
"sfx": "impact.wav",
"db": 0
},
{
"t": 81.95,
"sfx": "impact.wav",
"db": -6
},
{
"t": 82.15,
"sfx": "whoosh.wav",
"db": -9
},
{
"t": 83.85,
"sfx": "pop.wav",
"db": -4
},
{
"t": 86.68,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 87.2,
"sfx": "pop.wav",
"db": -2
},
{
"t": 91.33,
"sfx": "impact.wav",
"db": -6
},
{
"t": 92.43,
"sfx": "pop.wav",
"db": -2
},
{
"t": 93.23,
"sfx": "pop.wav",
"db": -2
},
{
"t": 93.83,
"sfx": "pop.wav",
"db": -2
},
{
"t": 94.81,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 95.53,
"sfx": "whoosh.wav",
"db": -6
},
{
"t": 97.73,
"sfx": "whoosh.wav",
"db": -6
},
{
"t": 98.23,
"sfx": "whoosh.wav",
"db": -6
},
{
"t": 99.73,
"sfx": "impact.wav",
"db": -6
},
{
"t": 100.43,
"sfx": "pop.wav",
"db": -2
},
{
"t": 103.93,
"sfx": "impact.wav",
"db": -6
},
{
"t": 104.33,
"sfx": "impact.wav",
"db": -2
},
{
"t": 104.83,
"sfx": "pop.wav",
"db": -4
},
{
"t": 106.48,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 109.5,
"sfx": "pop.wav",
"db": -2
},
{
"t": 112.21,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 112.83,
"sfx": "pop.wav",
"db": -4
},
{
"t": 115.81,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 118.93,
"sfx": "impact.wav",
"db": -6
},
{
"t": 119.23,
"sfx": "pop.wav",
"db": -4
},
{
"t": 121.93,
"sfx": "impact.wav",
"db": -6
},
{
"t": 122.23,
"sfx": "impact.wav",
"db": 0
},
{
"t": 124.33,
"sfx": "impact.wav",
"db": -6
},
{
"t": 124.53,
"sfx": "pop.wav",
"db": -3
},
{
"t": 124.83,
"sfx": "pop.wav",
"db": -4
},
{
"t": 125.43,
"sfx": "pop.wav",
"db": -3
},
{
"t": 127.0,
"sfx": "impact.wav",
"db": -6
},
{
"t": 127.1,
"sfx": "riser.wav",
"db": -8
},
{
"t": 129.01,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 133.53,
"sfx": "impact.wav",
"db": 0
},
{
"t": 135.13,
"sfx": "impact.wav",
"db": -6
},
{
"t": 135.33,
"sfx": "whoosh.wav",
"db": -6
},
{
"t": 137.63,
"sfx": "whoosh.wav",
"db": -6
},
{
"t": 139.73,
"sfx": "whoosh.wav",
"db": -6
},
{
"t": 140.41,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 143.53,
"sfx": "impact.wav",
"db": -6
},
{
"t": 145.13,
"sfx": "pop.wav",
"db": -4
},
{
"t": 147.73,
"sfx": "whoosh.wav",
"db": -2
},
{
"t": 148.43,
"sfx": "impact.wav",
"db": -2
},
{
"t": 151.33,
"sfx": "impact.wav",
"db": -6
},
{
"t": 151.53,
"sfx": "whoosh.wav",
"db": -8
},
{
"t": 151.83,
"sfx": "pop.wav",
"db": -4
},
{
"t": 152.73,
"sfx": "whoosh.wav",
"db": -8
},
{
"t": 152.93,
"sfx": "pop.wav",
"db": -4
},
{
"t": 153.53,
"sfx": "whoosh.wav",
"db": -8
},
{
"t": 153.73,
"sfx": "pop.wav",
"db": -4
},
{
"t": 155.13,
"sfx": "whoosh.wav",
"db": -8
},
{
"t": 155.23,
"sfx": "pop.wav",
"db": -4
},
{
"t": 156.28,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 157.4,
"sfx": "pop.wav",
"db": -4
},
{
"t": 159.73,
"sfx": "whoosh.wav",
"db": -2
},
{
"t": 160.93,
"sfx": "whoosh.wav",
"db": -8
},
{
"t": 161.63,
"sfx": "pop.wav",
"db": -4
},
{
"t": 162.03,
"sfx": "whoosh.wav",
"db": -8
},
{
"t": 162.63,
"sfx": "pop.wav",
"db": -4
},
{
"t": 163.33,
"sfx": "impact.wav",
"db": -6
},
{
"t": 163.53,
"sfx": "pop.wav",
"db": -4
},
{
"t": 165.73,
"sfx": "impact.wav",
"db": -6
},
{
"t": 165.93,
"sfx": "pop.wav",
"db": -3
},
{
"t": 166.38,
"sfx": "pop.wav",
"db": -3
},
{
"t": 166.83,
"sfx": "pop.wav",
"db": -3
},
{
"t": 167.33,
"sfx": "pop.wav",
"db": -4
},
{
"t": 169.81,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 170.23,
"sfx": "pop.wav",
"db": -4
},
{
"t": 172.93,
"sfx": "impact.wav",
"db": -6
},
{
"t": 173.13,
"sfx": "pop.wav",
"db": 0
},
{
"t": 175.83,
"sfx": "pop.wav",
"db": 0
},
{
"t": 177.73,
"sfx": "pop.wav",
"db": 0
},
{
"t": 178.21,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 178.93,
"sfx": "pop.wav",
"db": -4
},
{
"t": 181.93,
"sfx": "impact.wav",
"db": -6
},
{
"t": 183.33,
"sfx": "pop.wav",
"db": -4
},
{
"t": 185.53,
"sfx": "impact.wav",
"db": -6
},
{
"t": 185.53,
"sfx": "whoosh.wav",
"db": -9
},
{
"t": 185.73,
"sfx": "pop.wav",
"db": -4
},
{
"t": 185.93,
"sfx": "riser.wav",
"db": -3
},
{
"t": 188.23,
"sfx": "pop.wav",
"db": -2
},
{
"t": 192.61,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 194.23,
"sfx": "impact.wav",
"db": 0
},
{
"t": 196.33,
"sfx": "impact.wav",
"db": -6
},
{
"t": 196.63,
"sfx": "impact.wav",
"db": -2
},
{
"t": 199.53,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 199.95,
"sfx": "pop.wav",
"db": -4
},
{
"t": 203.53,
"sfx": "impact.wav",
"db": -6
},
{
"t": 204.03,
"sfx": "pop.wav",
"db": -4
},
{
"t": 206.13,
"sfx": "pop.wav",
"db": -4
},
{
"t": 207.73,
"sfx": "impact.wav",
"db": -6
},
{
"t": 207.83,
"sfx": "whoosh.wav",
"db": -9
},
{
"t": 210.33,
"sfx": "pop.wav",
"db": -4
},
{
"t": 211.33,
"sfx": "impact.wav",
"db": -6
},
{
"t": 211.53,
"sfx": "whoosh.wav",
"db": -9
},
{
"t": 211.63,
"sfx": "pop.wav",
"db": -4
},
{
"t": 215.03,
"sfx": "impact.wav",
"db": 0
},
{
"t": 216.61,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 217.13,
"sfx": "pop.wav",
"db": -2
},
{
"t": 220.93,
"sfx": "impact.wav",
"db": -6
},
{
"t": 221.13,
"sfx": "pop.wav",
"db": -4
},
{
"t": 224.53,
"sfx": "impact.wav",
"db": -6
},
{
"t": 226.43,
"sfx": "pop.wav",
"db": -4
},
{
"t": 228.98,
"sfx": "whoosh.wav",
"db": 0
},
{
"t": 229.9,
"sfx": "riser.wav",
"db": -8
},
{
"t": 234.4,
"sfx": "impact.wav",
"db": -6
},
{
"t": 234.7,
"sfx": "pop.wav",
"db": -2
},
{
"t": 235.3,
"sfx": "pop.wav",
"db": -2
},
{
"t": 237.6,
"sfx": "pop.wav",
"db": -2
},
{
"t": 239.53,
"sfx": "whoosh.wav",
"db": -2
},
{
"t": 239.93,
"sfx": "whoosh.wav",
"db": -9
},
{
"t": 242.53,
"sfx": "pop.wav",
"db": -3
},
{
"t": 242.93,
"sfx": "whoosh.wav",
"db": -9
},
{
"t": 242.98,
"sfx": "pop.wav",
"db": -3
},
{
"t": 243.33,
"sfx": "whoosh.wav",
"db": -9
},
{
"t": 243.53,
"sfx": "pop.wav",
"db": -2
},
{
"t": 246.73,
"sfx": "impact.wav",
"db": -6
},
{
"t": 247.33,
"sfx": "pop.wav",
"db": -4
},
{
"t": 248.93,
"sfx": "riser.wav",
"db": -3
},
{
"t": 250.63,
"sfx": "pop.wav",
"db": -4
},
{
"t": 253.33,
"sfx": "impact.wav",
"db": -6
},
{
"t": 253.33,
"sfx": "whoosh.wav",
"db": -9
},
{
"t": 253.53,
"sfx": "pop.wav",
"db": -2
},
{
"t": 254.33,
"sfx": "impact.wav",
"db": -2
}
]
```

## FILE: templates/one-era/README.md

```markdown
# Ví dụ: One Era (257 s, 23 cảnh) — dựng bằng `scripts/scenegen.py`

1. Giọng đọc → `transcribe_vi.py`; số liệu đối chiếu: CafeF (03 & 07/11/2026), Báo Đầu tư, The Leader (25/09/2026), SGGP, Znews.
2. `geo_build.py geo_config.json geo.json` (TP.HCM cũ / Bình Dương cũ / BR-VT cũ tách riêng; QL13, Vành đai 3, Mỹ Phước–Tân Vạn, Nguyễn Thị Minh Khai, kênh Suối Cát, ranh công trường chọn trên ảnh vệ tinh z16).
3. Ảnh vệ tinh Esri z13 + z16 (làm tối, ngả navy) để bay liền từ bản đồ vùng xuống công trường.
4. Google Earth: `earth-shots/g1..g4.json` → `earth_capture.js` → `earth_encode.sh` → chỉnh màu navy.
5. Ảnh thật/phối cảnh từ bài báo (ghi nguồn trên khung); tài liệu gốc = trích nguyên văn đoạn có số liệu (font lớn cho khung dọc).
6. `python mk_storyboard.py` → `storyboard.json` → `scenegen.py storyboard.json <project>`; `mix_audio.py` với `sfx_events.json` (sinh từ storyboard).
```

## FILE: templates/one-era/earth-shots/g1.json

```json
{"dpr": 1.5, "frames": 70, "from": {"lat": 10.9285, "lng": 106.708, "dist": 2600, "head": 20, "tilt": 60}, "to": {"lat": 10.9295, "lng": 106.707, "dist": 1900, "head": 60, "tilt": 64}}
```

## FILE: templates/one-era/earth-shots/g2.json

```json
{"dpr": 1.5, "frames": 80, "from": {"lat": 10.96725, "lng": 106.69948, "dist": 1900, "head": 300, "tilt": 62}, "to": {"lat": 10.96725, "lng": 106.69948, "dist": 1350, "head": 350, "tilt": 66}}
```

## FILE: templates/one-era/earth-shots/g3.json

```json
{"dpr": 1.5, "frames": 70, "from": {"lat": 10.9628, "lng": 106.6905, "dist": 1500, "head": 30, "tilt": 62}, "to": {"lat": 10.963, "lng": 106.691, "dist": 1100, "head": 80, "tilt": 66}}
```

## FILE: templates/one-era/earth-shots/g4.json

```json
{"dpr": 1.5, "frames": 110, "from": {"lat": 10.96725, "lng": 106.69948, "dist": 1400, "head": 200, "tilt": 64}, "to": {"lat": 10.96725, "lng": 106.69948, "dist": 3600, "head": 232, "tilt": 56}}
```

## FILE: templates/one-era/geo_config.json

```json
{
 "country": "VNM",
 "merge": {
  "TPHCM_cu": [
   "Hồ Chí Minh city"
  ],
  "BD_cu": [
   "Bình Dương"
  ],
  "BRVT_cu": [
   "Bà Rịa - Vũng Tàu"
  ],
  "TPHCM_moi": [
   "Hồ Chí Minh city",
   "Bình Dương",
   "Bà Rịa - Vũng Tàu"
  ],
  "Đồng Nai": [
   "Đông Nam Bộ",
   "Bình Phước"
  ],
  "Tây Ninh": [
   "Tây Ninh",
   "Long An"
  ],
  "Đồng Tháp": [
   "Ðong Tháp",
   "Tiền Giang"
  ],
  "Lâm Đồng": [
   "Lâm Đồng",
   "Đắk Nông",
   "Bình Thuận"
  ]
 },
 "focus": "BD_cu",
 "points": {
  "oneera": [
   106.69948,
   10.96725
  ],
  "thuangiao": [
   106.69948,
   10.96725
  ],
  "tdm": [
   106.6527,
   10.9804
  ],
  "hcm": [
   106.7009,
   10.7769
  ],
  "brvt": [
   107.17,
   10.5
  ],
  "bd_lab": [
   106.62,
   11.18
  ],
  "l_ql13": [
   106.702051,
   10.955402
  ],
  "l_vd3": [
   106.693361,
   10.966935
  ],
  "l_mptv": [
   106.709776,
   10.974519
  ],
  "l_ntmk": [
   106.694326,
   10.966303
  ],
  "l_canal": [
   106.702695,
   10.969779
  ]
 },
 "lines": {
  "ql13": [
   [
    106.682739,
    10.966777
   ],
   [
    106.690464,
    10.962827
   ],
   [
    106.697223,
    10.95951
   ],
   [
    106.702051,
    10.955402
   ],
   [
    106.70527,
    10.951452
   ],
   [
    106.708488,
    10.941213
   ]
  ],
  "vd3": [
   [
    106.682739,
    10.957456
   ],
   [
    106.687567,
    10.960616
   ],
   [
    106.690464,
    10.963143
   ],
   [
    106.693361,
    10.966935
   ],
   [
    106.696579,
    10.971359
   ],
   [
    106.700281,
    10.978943
   ]
  ],
  "mptv": [
   [
    106.704626,
    10.978943
   ],
   [
    106.709776,
    10.974519
   ],
   [
    106.715698,
    10.969147
   ]
  ],
  "ntmk": [
   [
    106.689016,
    10.976099
   ],
   [
    106.692395,
    10.970095
   ],
   [
    106.694326,
    10.966303
   ],
   [
    106.697545,
    10.959984
   ]
  ],
  "canal": [
   [
    106.700764,
    10.978943
   ],
   [
    106.701247,
    10.974203
   ],
   [
    106.701086,
    10.971043
   ],
   [
    106.702695,
    10.969779
   ],
   [
    106.704304,
    10.966935
   ],
   [
    106.70527,
    10.964091
   ],
   [
    106.707523,
    10.962511
   ]
  ]
 },
 "polys": {
  "site": [
   [
    106.69143,
    10.964091
   ],
   [
    106.694648,
    10.966935
   ],
   [
    106.700764,
    10.970411
   ],
   [
    106.703339,
    10.969463
   ],
   [
    106.704304,
    10.965671
   ],
   [
    106.702373,
    10.964723
   ],
   [
    106.699476,
    10.965671
   ],
   [
    106.697867,
    10.964091
   ],
   [
    106.695614,
    10.964723
   ],
   [
    106.693361,
    10.964091
   ],
   [
    106.691751,
    10.963143
   ]
  ]
 }
}
```

## FILE: templates/one-era/mk_storyboard.py

```python
import json
SAT16 = {"img": "assets/maps/sat16_g.jpg", "z": 16, "x0": 13359360, "y0": 7873024, "w": 3584, "h": 3072, "id": "sat16"}
SAT13 = {"img": "assets/maps/sat13_g.jpg", "z": 13, "x0": 1669120, "y0": 983296, "w": 2048, "h": 2048, "id": "sat13"}
OE = (10.96725, 106.69948)
CBRE = "Nguồn: CBRE Việt Nam qua CafeF, Báo Đầu tư (03/11/2026)"
OEsrc = "Nguồn: CafeF, Báo Đầu tư (11/2026) · Ảnh vệ tinh: Esri"
def site_layers(extra=()):
    return [dict(SAT16, show=None), {"geo": "lines:site", "cls": "site", "w": 3}] + list(extra)
def L(geo, cls, id, w, len_=True): return {"geo": geo, "cls": cls, "id": id, "w": w, "len": len_}
def sc(**k): return k

S = []
# 1. CBRE: TP.HCM mở rộng -> tách Bình Dương cũ
S.append(sc(id="s01", start=0, dur=30.9, type="board", enter="none", seg="Nguồn cung mới · Quý II/2026", foot=CBRE, top=330, rowH=140,
  rows=[{"icon": "apt", "num": 6573, "unit": "căn hộ", "desc": "mở bán mới, TP.HCM mở rộng", "t": 0.25, "until": 12.6},
        {"icon": "home", "num": 1934, "unit": "nhà liền thổ", "desc": "mở bán mới", "t": 2.55, "until": 12.6}],
  bg={"dimMap": 1, "keys": [[0, 15.8, 106.3, 7.25], [2.4, 10.62, 106.85, 8.95], [12.6, 10.66, 106.85, 9.0], [16.6, 10.9, 106.72, 9.35],
                             [22.5, 10.88, 106.75, 9.3], [27.6, 10.78, 106.78, 9.25], [30.9, 10.88, 106.72, 9.45, True]],
      "layers": [{"geo": "prov:TPHCM_moi", "cls": "region", "id": "s01-moi", "w": 3},
                 {"geo": "prov:TPHCM_cu", "cls": "cmp", "id": "s01-hcm", "w": 2}, {"geo": "prov:BRVT_cu", "cls": "cmp", "id": "s01-brvt", "w": 2},
                 {"geo": "prov:BD_cu", "cls": "vl-glow", "id": "s01-bdg", "w": 14}, {"geo": "prov:BD_cu", "cls": "vl", "id": "s01-bd", "w": 3}],
      "show": [{"id": "s01-moi", "t": 1.2, "d": 0.6}, {"id": "s01-bd", "t": 16.6, "d": 0.5}, {"id": "s01-bdg", "t": 16.6, "d": 0.5, "to": 0.6},
               {"id": "s01-hcm", "t": 13.2, "d": 0.4}, {"id": "s01-brvt", "t": 13.2, "d": 0.4, "to": 0.6}],
      "labelsA": [{"at": "TPHCM_moi", "lx": 0, "ly": -60, "align": "c", "text": "TP.HCM mở rộng", "t": 6.3, "d": 6.2},
                  {"at": "bd_lab", "lx": -40, "ly": -150, "align": "c", "text": "Bình Dương cũ", "small": "nay là Đông Bắc TP.HCM", "acc": True, "t": 17.3, "d": 13},
                  {"at": "hcm", "lx": 150, "ly": 90, "align": "l", "text": "TP.HCM cũ", "t": 13.4, "d": 17}],
      "tagsB": [{"at": "bd_lab", "dx": -40, "dy": 70, "text": "≈80% căn hộ mới", "t": 22.9, "d": 8},
                {"at": "bd_lab", "dx": -40, "dy": 135, "text": "0 nhà liền thổ mới", "t": 26.8, "d": 4},
                {"at": "hcm", "dx": 150, "dy": 200, "text": "100% nhà liền thổ", "t": 28.1, "d": 3}]}))
# 2. vùng công nghiệp
S.append(sc(id="s02", start=30.9, dur=7.0, type="media", src="assets/ge/g1.mp4", seg="Đông Bắc TP.HCM", foot="Hình ảnh 3D: Google Earth · khu công nghiệp Bình Dương cũ",
  anchors=[{"t": 1.0, "d": 5.6, "lines": ["Nhà có đất:", "*gần *như *không *có"]}]))
# 3. bay vào Thuận Giao
S.append(sc(id="s03", start=37.9, dur=4.3, type="map", seg="Phường Thuận Giao", foot="Ảnh vệ tinh: Esri, Maxar",
  keys=[[0, 10.95, 106.72, 9.6], [2.2, 10.966, 106.70, 12.6], [4.3, 10.9673, 106.6995, 14.4, True]],
  layers=[dict(SAT13, show=[10.5, 11.6]), dict(SAT16, show=[13.4, 14.2]), {"geo": "prov:BD_cu", "cls": "vl", "id": "s03-bd", "w": 3}],
  show=[{"id": "s03-bd", "t": 0, "d": 0.01, "to": 1}], hide=[{"id": "s03-bd", "t": 1.2, "d": 0.8}],
  labelsA=[{"at": "oneera", "lx": 90, "ly": -110, "text": "Thuận Giao", "acc": True, "t": 1.6, "d": 2.2}]))
# 4. khai trương
S.append(sc(id="s04", start=42.2, dur=6.3, type="media", src="assets/img/p1.jpg", fit="frame", kb=[1.0, 1.08, 0, -20, 0, -10], seg="Khai trương One Era Galleria", foot="Ảnh: CafeF (03/11/2026)",
  tagsB=[{"x": 540, "y": 470, "text": "31/10/2026 · gần 50 ha", "t": 0.2, "d": 5.6}],
  anchors=[{"t": 2.6, "d": 3.3, "lines": ["Mở cửa", "*đón *khách"]}]))
# 5. công trường + câu hỏi
S.append(sc(id="s05", start=48.5, dur=13.4, type="map", seg="One Era · Thuận Giao", foot=OEsrc,
  keys=[[0, 10.9672, 106.6994, 15.7], [6, 10.9672, 106.6994, 15.95], [13.4, 10.9672, 106.6994, 16.1]],
  layers=site_layers([L("lines:site", "coast-glow", "s05-glow", 14)]),
  draw=[{"id": "s05-glow", "t": 0.1, "d": 1.4}],
  labelsA=[{"at": "oneera", "lx": 0, "ly": -330, "align": "c", "text": "One Era", "small": "khu đô thị ~50 ha", "acc": True, "t": 0.3, "d": 2.7}],
  tagsB=[{"at": "oneera", "dx": 0, "dy": 300, "text": "357 căn nhà phố đầu tiên", "t": 0.3, "d": 2.7}],
  anchors=[{"t": 3.1, "d": 9.8, "pos": "mid", "dim": True, "lines": ["One Era", "là *dự *án *thế *nào?"]}]))
# 6. quy mô
S.append(sc(id="s06", start=61.9, dur=29.3, type="board", seg="Quy mô One Era", foot=OEsrc, top=380,
  rows=[{"icon": "area", "num": 49.5, "dec": 1, "unit": "ha", "desc": "≈ 70 sân bóng đá tiêu chuẩn", "t": 3.8},
        {"icon": "money", "big": "> 1 tỷ USD", "desc": "tổng vốn đầu tư", "t": 9.8},
        {"icon": "home", "num": 4039, "unit": "sản phẩm", "desc": "nhà phố · shophouse · biệt thự · căn hộ", "t": 11.2},
        {"icon": "leaf", "num": 25, "unit": "% mật độ xây dựng nhà ở", "desc": "", "up": "4 m² đất → 1 m² xây nhà", "t": 19.2, "tup": 21.9},
        {"icon": "leaf", "big": "Còn lại: cây xanh, tiện ích", "desc": "và đường nội khu", "t": 25.3}],
  bg={"dimMap": 0.35, "keys": [[0, 10.9672, 106.6994, 15.8], [14, 10.966, 106.700, 16.0], [29.3, 10.9672, 106.6994, 15.85]], "layers": site_layers()}))
# 7. chủ đầu tư & đối tác
S.append(sc(id="s07", start=91.2, dur=21.0, type="board", seg="Đứng sau One Era", foot="Nguồn: Báo SGGP, The Leader, Znews", top=330, rowH=140,
  rows=[{"icon": "cal", "big": "27/09/2025", "desc": "khởi công", "t": 1.3, "until": 17.6},
        {"icon": "flag", "big": "Kim Oanh Group", "desc": "chủ đầu tư", "t": 4.4, "until": 17.6},
        {"icon": "handshake", "big": "Sumitomo Forestry", "desc": "đối tác Nhật Bản", "t": 7.6, "until": 17.6},
        {"icon": "handshake", "big": "Kumagai Gumi", "desc": "đối tác Nhật Bản", "t": 9.5, "until": 17.6},
        {"icon": "handshake", "big": "NTT Urban Development", "desc": "đối tác Nhật Bản", "t": 10.8, "until": 17.6},
        {"icon": "bld", "big": "Kinera", "desc": "nhà phát triển", "t": 13.2, "until": 17.6}],
  anchors=[{"t": 18.2, "d": 2.6, "pos": "mid", "lines": ["Thêm một tên", "*rất *nặng *ký"]}]))
# 8. Longfor ký kết
S.append(sc(id="s08", start=112.2, dur=6.9, type="media", src="assets/img/p8.jpg", fit="frame", kb=[1.0, 1.07, 0, 0, 0, -12], seg="24/09/2026 · Ký kết hợp tác", foot="Ảnh: The Leader (25/09/2026)",
  anchors=[{"t": 0.25, "d": 6.1, "lines": ["*Longfor", "bắt tay Kinera"]}]))
# 9. Longfor số liệu
S.append(sc(id="s09", start=119.1, dur=18.3, type="board", seg="Longfor · niêm yết tại Hồng Kông", foot="Nguồn: The Leader (25/09/2026)", top=380,
  rows=[{"icon": "flag", "big": "1993", "desc": "năm thành lập", "t": 0.9},
        {"icon": "bld", "num": 1300, "unit": "dự án", "desc": "đã phát triển (hơn)", "t": 4.0},
        {"icon": "apt", "num": 1.1, "dec": 1, "unit": "triệu căn", "desc": "đã bàn giao (hơn)", "t": 6.3},
        {"icon": "chart", "num": 30000, "unit": "căn / năm", "desc": "bình quân (hơn)", "t": 9.2},
        {"icon": "money", "num": 10, "unit": "tỷ USD", "desc": "doanh số bán năm 2025 (gần)", "t": 14.6}]))
# 10. tài liệu gốc The Leader
S.append(sc(id="s10", start=137.4, dur=6.2, type="doc", seg="Tài liệu gốc · The Leader 25/09/2026", foot="Trích nguyên văn bài viết trên theleader.vn",
  img="assets/doc/doc_leader.png", imgW=1400, imgH=1985,
  hl=[{"y": 546, "h": 678, "t": 0.5}, {"y": 1332, "h": 534, "t": 1.6}], moves=[{"t": 1.2, "d": 1.6, "y": -180, "scale": 1.02}]))
# 11. Google Earth nút giao
S.append(sc(id="s11", start=143.6, dur=6.3, type="media", src="assets/ge/g3.mp4", seg="Vị trí", foot="Hình ảnh 3D: Google Earth",
  anchors=[{"t": 1.8, "d": 4.0, "lines": ["Nửa còn lại", "nằm ở *vị *trí"]}]))
# 12. giao thông
S.append(sc(id="s12", start=149.9, dur=20.2, type="map", seg="Kết nối giao thông", foot=OEsrc + " · metro theo quy hoạch",
  keys=[[0, 10.9672, 106.6994, 15.55], [8, 10.967, 106.6995, 15.45], [20.2, 10.9675, 106.6995, 15.35]],
  layers=site_layers([L("lines:ql13", "coast-glow", "r-ql13g", 14), L("lines:ql13", "coast", "r-ql13", 5),
                      L("lines:vd3", "coast-glow", "r-vd3g", 14), L("lines:vd3", "coast", "r-vd3", 5),
                      L("lines:mptv", "coast-glow", "r-mptvg", 14), L("lines:mptv", "coast", "r-mptv", 5),
                      L("lines:ntmk", "coast-glow", "r-ntmkg", 12), L("lines:ntmk", "coast", "r-ntmk", 4)]),
  draw=[{"id": i, "t": t, "d": 1.0} for i, t in [("r-ql13g", 1.6), ("r-ql13", 1.6), ("r-vd3g", 2.8), ("r-vd3", 2.8), ("r-mptvg", 3.6), ("r-mptv", 3.6), ("r-ntmkg", 5.2), ("r-ntmk", 5.2)]],
  labelsA=[{"at": "l_ql13", "lx": -110, "ly": -130, "text": "Quốc lộ 13", "t": 2.0, "d": 18},
           {"at": "l_vd3", "lx": -60, "ly": -90, "text": "Vành đai 3", "t": 3.1, "d": 17},
           {"at": "l_mptv", "lx": -200, "ly": 120, "align": "c", "text": "Mỹ Phước – Tân Vạn", "t": 3.9, "d": 16},
           {"at": "l_ntmk", "lx": -60, "ly": -70, "text": "Nguyễn Thị Minh Khai", "t": 5.5, "d": 3.0}],
  tagsB=[{"at": "oneera", "dx": -170, "dy": -330, "text": "Metro TDM – Tao Đàn", "t": 11.4, "d": 8.5},
         {"at": "oneera", "dx": 60, "dy": 300, "text": "Metro TDM – Suối Tiên", "t": 13.6, "d": 6.3},
         {"at": "oneera", "dx": 0, "dy": 380, "text": "Liền kề công viên ~42 ha", "t": 16.1, "d": 3.8}]))
# 13. tiện ích
S.append(sc(id="s13", start=170.1, dur=11.7, type="board", seg="Tiện ích nội khu", foot=OEsrc, top=420,
  rows=[{"icon": "school", "big": "VAS Saigon", "desc": "trường liên cấp", "t": 3.0},
        {"icon": "school", "big": "Kindup", "desc": "mầm non quốc tế", "t": 5.6},
        {"icon": "health", "big": "Meret", "desc": "trung tâm chăm sóc sức khoẻ", "t": 7.5},
        {"icon": "office", "big": "TTTM & văn phòng hạng A", "desc": "", "t": 9.4}],
  bg={"dimMap": 0.35, "keys": [[0, 10.9672, 106.6994, 15.9], [11.7, 10.968, 106.6985, 16.05]], "layers": site_layers()}))
# 14. One Park
S.append(sc(id="s14", start=181.8, dur=7.2, type="media", src="assets/ge/g2.mp4", seg="Đã đi vào hoạt động", foot="Hình ảnh 3D: Google Earth",
  anchors=[{"t": 3.9, "d": 3.0, "lines": ["One Park", "*1 *ha *đã *hoạt *động"]}]))
# 15. 2.500 người
S.append(sc(id="s15", start=189.0, dur=7.4, type="media", src="assets/img/p2.jpg", fit="frame", kb=[1.0, 1.08, 0, 10, 0, 0], seg="Ngày khai trương", foot="Ảnh: CafeF (03/11/2026)",
  tagsB=[{"x": 540, "y": 1380, "text": "≈ 2.500 người đến dự", "t": 3.8, "d": 3.1}]))
# 16. Central District
S.append(sc(id="s16", start=196.4, dur=7.1, type="media", src="assets/img/p4.jpg", fit="frame", kb=[1.0, 1.1, 0, -30, 0, 0], seg="Phân khu Central District", foot="Ảnh phối cảnh của chủ đầu tư (qua CafeF)",
  anchors=[{"t": 0.45, "d": 6.1, "lines": ["Central District", "*357 *căn *thấp *tầng"]}]))
# 17. townhouse
S.append(sc(id="s17", start=203.5, dur=7.9, type="media", src="assets/img/p3.jpg", fit="frame", kb=[1.0, 1.08, 0, 20, 0, 0], seg="Townhouse", foot="Ảnh phối cảnh của chủ đầu tư (qua CafeF)",
  tagsB=[{"x": 540, "y": 470, "text": "1 trệt · 2 lầu", "t": 0.6, "d": 6.8}, {"x": 540, "y": 1380, "text": "Nhiệt đới đương đại", "t": 2.7, "d": 4.7}]))
# 18. kênh Suối Cát
S.append(sc(id="s18", start=211.4, dur=5.5, type="map", seg="Kênh Suối Cát", foot=OEsrc,
  keys=[[0, 10.9675, 106.7005, 16.0], [5.5, 10.9675, 106.7008, 16.15]],
  layers=site_layers([L("lines:canal", "rv-glow", "s18-cg", 16), L("lines:canal", "rv", "s18-c", 5)]),
  draw=[{"id": "s18-cg", "t": 0.3, "d": 1.4}, {"id": "s18-c", "t": 0.3, "d": 1.4}],
  labelsA=[{"at": "l_canal", "lx": 90, "ly": -80, "text": "Kênh Suối Cát", "t": 0.6, "d": 4.4}],
  tagsB=[{"at": "oneera", "dx": 0, "dy": 420, "text": "Dạo bộ, đạp xe ~2,6 km", "t": 3.7, "d": 1.4}]))
# 19. shophouse
S.append(sc(id="s19", start=216.9, dur=4.3, type="media", src="assets/img/p6.jpg", fit="frame", kb=[1.0, 1.06, 0, -10, 0, 0], seg="Shophouse", foot="Ảnh phối cảnh của chủ đầu tư (qua CafeF)",
  tagsB=[{"x": 540, "y": 470, "text": "Thêm tầng lửng: ở + kinh doanh", "t": 0.5, "d": 3.3}]))
# 20. hai mặt tiền
S.append(sc(id="s20", start=221.2, dur=7.9, type="media", src="assets/img/p5.jpg", fit="frame", kb=[1.0, 1.08, 0, 15, 0, 0], seg="Shophouse hai mặt tiền", foot="Ảnh phối cảnh của chủ đầu tư (qua CafeF)",
  tagsB=[{"x": 540, "y": 470, "text": "Đại lộ nội khu 25 m", "t": 3.3, "d": 4.1}, {"x": 540, "y": 1380, "text": "Mặt sau: công viên One Park", "t": 5.4, "d": 2.0}]))
# 21. mở màn & bàn giao
S.append(sc(id="s21", start=229.1, dur=11.2, type="board", seg="Lộ trình", foot=OEsrc, top=420,
  rows=[{"icon": "home", "num": 357, "unit": "căn", "desc": "phần mở màn (Central District)", "t": 0.8},
        {"icon": "apt", "num": 4000, "unit": "sản phẩm", "desc": "toàn khu (hơn)", "t": 4.2},
        {"icon": "cal", "big": "Quý IV/2028", "desc": "dự kiến bàn giao những căn đầu tiên", "t": 8.5}],
  bg={"dimMap": 0.35, "keys": [[0, 10.9672, 106.6994, 16.0], [11.2, 10.9672, 106.6994, 15.8]], "layers": site_layers()}))
# 22. tài liệu gốc CafeF
S.append(sc(id="s22", start=240.3, dur=6.9, type="doc", seg="Tài liệu gốc · CafeF 03/11/2026", foot="Trích nguyên văn bài viết trên cafef.vn",
  img="assets/doc/doc_cafef.png", imgW=1400, imgH=1843,
  hl=[{"y": 546, "h": 678, "t": 0.8}], moves=[{"t": 2.4, "d": 2.5, "y": -40, "scale": 1.05}]))
# 23. kết
S.append(sc(id="s23", start=247.2, dur=10.24, type="media", src="assets/ge/g4.mp4", seg="Phép thử cuối cùng", foot="Hình ảnh 3D: Google Earth", exit="none",
  anchors=[{"t": 6.0, "d": 4.24, "lines": ["Từ trên giấy", "đến *người *thật *sống"]}]))
json.dump({"duration": 257.44, "audio": "assets/mix.wav", "gsap": "assets/lib/gsap.min.js", "scenes": S}, open("storyboard.json", "w"), ensure_ascii=False, indent=1)
print(len(S), "cảnh; kiểm tra liền mạch:", all(abs(a["start"] + a["dur"] - b["start"]) < 1e-6 for a, b in zip(S, S[1:])))
```

## FILE: templates/one-era/sfx_events.json

```json
[
 {
  "t": 0.25,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 2.55,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 22.9,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 26.8,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 28.1,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 30.62,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 37.62,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 41.92,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 42.4,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 48.22,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 48.8,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 50.2,
  "sfx": "sfx/riser.wav",
  "db": -2
 },
 {
  "t": 61.62,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 65.7,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 71.7,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 73.1,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 81.1,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 87.2,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 90.92,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 92.5,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 95.6,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 98.8,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 100.7,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 102.0,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 104.4,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 108.0,
  "sfx": "sfx/riser.wav",
  "db": -2
 },
 {
  "t": 111.92,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 118.82,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 120.0,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 123.1,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 125.4,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 128.3,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 133.7,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 137.12,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 143.32,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 149.62,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 161.3,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 163.5,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 166.0,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 169.82,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 173.1,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 175.7,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 177.6,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 179.5,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 181.52,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 188.72,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 192.8,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 196.12,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 203.22,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 204.1,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 206.2,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 211.12,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 215.1,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 216.62,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 217.4,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 220.92,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 224.5,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 226.6,
  "sfx": "sfx/pop.wav",
  "db": -5
 },
 {
  "t": 228.82,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 229.9,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 233.3,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 237.6,
  "sfx": "sfx/pop.wav",
  "db": -1
 },
 {
  "t": 240.02,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 },
 {
  "t": 246.92,
  "sfx": "sfx/whoosh.wav",
  "db": -2
 }
]
```

## Không nhúng (có trong thư mục/zip)

- templates/ha-tang-flight/flight.json
- templates/kinh-te-dia-phuong/assets/fonts/be-vietnam-pro-latin-400-normal.woff2
- templates/kinh-te-dia-phuong/assets/fonts/be-vietnam-pro-latin-500-normal.woff2
- templates/kinh-te-dia-phuong/assets/fonts/be-vietnam-pro-latin-600-normal.woff2
- templates/kinh-te-dia-phuong/assets/fonts/be-vietnam-pro-latin-800-normal.woff2
- templates/kinh-te-dia-phuong/assets/fonts/be-vietnam-pro-latin-ext-400-normal.woff2
- templates/kinh-te-dia-phuong/assets/fonts/be-vietnam-pro-latin-ext-500-normal.woff2
- templates/kinh-te-dia-phuong/assets/fonts/be-vietnam-pro-latin-ext-600-normal.woff2
- templates/kinh-te-dia-phuong/assets/fonts/be-vietnam-pro-latin-ext-800-normal.woff2
- templates/kinh-te-dia-phuong/assets/fonts/be-vietnam-pro-vietnamese-400-normal.woff2
- templates/kinh-te-dia-phuong/assets/fonts/be-vietnam-pro-vietnamese-500-normal.woff2
- templates/kinh-te-dia-phuong/assets/fonts/be-vietnam-pro-vietnamese-600-normal.woff2
- templates/kinh-te-dia-phuong/assets/fonts/be-vietnam-pro-vietnamese-800-normal.woff2
- templates/kinh-te-dia-phuong/geo.json
- templates/one-era-flight/flight.json
- templates/one-era-motion/shots.json
- templates/one-era/storyboard.json