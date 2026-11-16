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
