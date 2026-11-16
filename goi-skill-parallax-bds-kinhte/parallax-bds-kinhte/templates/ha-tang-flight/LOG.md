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