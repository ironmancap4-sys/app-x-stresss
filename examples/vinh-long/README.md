# Ví dụ: Kinh tế Vĩnh Long (88 s, dọc 9:16)

Dựng bằng skill `parallax-bds-kinhte` từ một file giọng đọc.

- `transcript.json`: lời + mốc từng từ (`scripts/transcribe_vi.py`).
- Số liệu đối chiếu: Báo Đầu tư và Mekong ASEAN, 7/9/2026 (họp báo UBND tỉnh Vĩnh Long, 8 tháng đầu năm 2026). Lời đọc "39,34%" đã được sửa trên màn hình thành +19,34% theo báo.
- `compositions/map1.html` (0–28,2 s): bay bản đồ vệ tinh Esri (ảnh tạo bằng `tiles.py`, toạ độ trong `maps.json`).
- `compositions/earth.html` (28,2–69,4 s): 5 cảnh Google Earth 3D (`earth-shots/s1–s5.json`), zoom-blur ở mỗi mối nối, thẻ số liệu đếm số theo giọng đọc.
- `compositions/src.html` (69,4–74,4 s): thẻ nguồn số liệu.
- `compositions/end.html` (74,4–88,6 s): cảnh 3D s6 + câu kết.

Tài sản không có trong repo (nặng): `assets/vo.mp3`, `assets/maps/*.jpg` (chạy `tiles.py`, làm tối ảnh), `assets/earth/s1–s6.mp4` (chạy `node scripts/earth_capture.js earth-shots/sN.json shots/sN` rồi `scripts/earth_encode.sh shots/sN assets/earth/sN.mp4`).

Đo bằng `analyze_refs.py`: camera chạy 95% thời gian, 3 lần dừng, parallax 100% cảnh, 71% cut khi camera đang chạy.
