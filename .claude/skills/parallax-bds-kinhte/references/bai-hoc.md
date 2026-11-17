# Bài học đã sửa — lỗi gặp thật khi dựng và cách xử lý

Mỗi mục là lỗi đã xảy ra trong các video Vĩnh Long, One Era (A/B/C) và hạ tầng Đông Bắc. Trước khi giao, đi hết danh sách.

## 1. Số liệu và nguồn

- Whisper nghe nhầm số và tên ("phét tính", "Quán Era", "VRS", "2-park"). Số và tên trên màn hình lấy từ bài báo gốc, không từ bản chép lời.
- Lời đọc khác nguồn (75.000 tỷ vs 75.300 tỷ, 32,8 km vs 30,66 km, "hơn 10 triệu lượt" không có nguồn): màn hình ghi theo nguồn, báo người dùng trong phần giao.
- Không tìm được nguồn cho một con số → KHÔNG đưa lên màn hình, ghi trong nhật ký.
- WebFetch có thể bị chặn dù host đã cho phép; dùng `curl -L --compressed` (trang nén) rồi bóc chữ bằng Python.
- Host bị proxy chặn (403/ENOTFOUND) → xin thêm host qua cài đặt mạng của môi trường; không dùng trang trung gian.

## 2. Tư liệu

- Wikimedia trả 429, Pexels/Pixabay chặn tải tự động: không đổi User-Agent, không lách; thử lại thưa rồi bỏ, ghi vào nhật ký.
- Logo: trang chính thức → press kit → Wikimedia → mạng xã hội chính thức. Không có → huy hiệu chữ (`logo:"", mono:"ABC"`) và báo người dùng. Không vẽ lại.
- Ảnh báo < 1080 px chỉ dùng trong cửa sổ ảnh, không phóng toàn khung. Ảnh 602 px quá nhỏ cho mọi chỗ.
- Mỗi ảnh mượn ghi "Ảnh: <nguồn>" trên màn hình; không dùng ảnh nơi khác giả làm địa điểm thật.

## 3. Bản đồ và nền vệ tinh

- Overpass/OSM hay sập (504, reset): chỉ truy vấn nhỏ (một relation, một tuyến); không có → `scripts/sat_grid.py` cắt ảnh vệ tinh có lưới lat/lng, dò tuyến bằng mắt, vẽ kiểm lên ảnh, ghi "minh hoạ".
- Mây trên khu vực đang nói: `sat_declouds.py` (nhân bản kết cấu); inpaint Telea để lại vệt xám — không dùng.
- Lộ hình chữ nhật navy/ảnh: mỗi mức zoom phải ghép rộng hơn khung lớn nhất ở mức đó, tính cả khi nghiêng và khi đang chuyển mức (`show:[Za,Zb]` lùi muộn hơn hoặc ghép rộng hơn).
- Nghiêng 3D lộ mép mặt phẳng: SVG nới rộng + sương chân trời (flight.py/motion.py đã làm). Quay (bearing) giữ ≤ 30°.
- Nền vệ tinh: làm mềm 0,8 px, tối 20%, giảm bão hoà 15% — cùng một chỉnh màu cho mọi mức.

## 4. Camera (phong cách C)

- Keyframe trung gian lệch nhẹ → Hermite sinh cực trị → camera bò < 1,5 px/khung (lăn tăn mái nhà trên điện thoại). Viết chương: khoá → MỘT cú máy rõ → khoá.
- Tốc độ mặt đất ≤ 25 px/khung; đường xa đi bằng cung bay cao. `flight.py` báo nếu vượt.
- Mờ chuyển động: KHÔNG lọc trong trình duyệt (render chậm 7–100 lần); dùng `mb_post.py` sau render. `data-motion-blur` của HyperFrames không thấy camera vẽ bằng thuộc tính SVG.

## 5. Chữ, nhãn, thẻ — bộ kiểm KHÔNG bắt hết

- `hyperframes check` không thấy chồng chéo giữa hai composition (bản đồ vs HUD dòng nguồn). Phải snapshot ĐÚNG lúc mỗi cửa sổ ảnh/thẻ logo hiện (CAMLOG.md có mục "Mốc cần snapshot") và nhìn bằng mắt.
- Đáy mọi thẻ ≤ y 1380 (dòng nguồn ở 1396, vùng TikTok che từ 1440). Camera nghiêng thì phần dưới khung bị phóng to: đặt thẻ PHÍA TRÊN neo (ly âm).
- Thẻ không chạm mép trái/phải: tâm thẻ cách mép ≥ nửa bề rộng + 60 px.
- Khối 3D vẽ đè lên thẻ HTML: đặt thẻ cao hơn đỉnh khối, hoặc cho thẻ hiện trước khi khối mọc.
- Ghim và thẻ cùng chỗ → ghim tắt trước khi thẻ hiện.
- Hai nhãn cùng neo cùng lúc → đổi neo/ly hoặc tách thời điểm; tiêu đề mặt đất dài → giảm `size`.
- Chữ động phải giữ ≥ 0,5 s + 0,3 s/từ (check báo `line_unread`).
- Nhãn đặt sau khi lọc `if v not in (None,"",False)` sẽ làm mất cờ `lead=False`/`logo=""` — giữ lại các khoá này khi lọc.

## 6. HyperFrames

- CDN bị chặn khi render → chép `gsap.min.js` vào `assets/lib`.
- Composition HUD/footage phải nền trong suốt (motion.css đặt nền navy cho `#root`).
- Tween `letterSpacing` bị lint báo lỗi → chỉ dùng transform/opacity.
- Đồng hồ camera chạy trước tween khi seek → tween đổi dữ liệu (chiều cao khối) phải tự gọi `frame()`.
- Tên biến trùng trong script nhúng (vd `host`) làm cả bản đồ trắng; luôn chạy `npx hyperframes lint` và xem một khung TRƯỚC khi render dài. Render "quá nhanh" bất thường = cảnh trắng.

## 7. Render và xuất

- Lệnh nền bị dừng sau 2 giờ; một render chỉ chạy một lúc (khoá theo tài khoản). Video dài/nặng → `scripts/render_segments.sh` (chia đoạn ≤ 65 s, chạy nối tiếp, ghép `-c copy`, mux âm thanh đầy đủ), rồi kiểm mối nối.
- Cảnh cận Z ≥ 14 nghiêng 3D với ảnh vệ tinh lớn là chậm nhất (~6 khung/phút); tính trước thời gian.
- AAC làm đỉnh vọt từ −1,3 lên −0,4 dBFS → mux `mix.wav` qua `alimiter=limit=0.80`, đo lại ≤ −1 dBTP.
- Không cho hai tiến trình ghi cùng một file; giải mã thử toàn bộ (`ffmpeg -v error -i out.mp4 -f null -`) trước khi gửi.
- Gửi kèm nhật ký: giữ khung, kiểu trực quan, tài sản tải về (tên, URL, độ phân giải, thời điểm dùng — lấy thời điểm từ flight.json, không gõ tay).
