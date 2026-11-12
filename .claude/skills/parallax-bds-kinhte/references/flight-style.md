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
