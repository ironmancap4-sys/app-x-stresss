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


Lỗi đã gặp thật khi dựng phong cách C (thẻ đè dòng nguồn, khối 3D che thẻ, render quá 2 giờ, AAC vọt đỉnh, OSM sập…): xem `references/bai-hoc.md`.
