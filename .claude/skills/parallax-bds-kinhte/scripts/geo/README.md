# Dựng dữ liệu bản đồ vector (ví dụ Vĩnh Long, 11/2026)

1. Ranh giới: Natural Earth `ne_10m_admin_1_states_provinces` (63 tỉnh cũ) → gộp theo NQ 202/2025/QH15 bằng shapely `unary_union`
   (ví dụ Vĩnh Long = Vĩnh Long + Bến Tre + Trà Vinh). OSM/Overpass có ranh giới mới nhưng thường quá tải.
2. Sông: tuyến `Mekong` của `ne_10m_rivers_lake_centerlines` cắt tới điểm hợp lưu, rồi nối tiếp ra cửa biển bằng
   tìm đường ngắn nhất qua điểm ảnh màu nước trên ảnh vệ tinh (skimage `route_through_array`, chi phí thấp ở pixel nước).
   Luôn xem ảnh xem trước đè trên vệ tinh trước khi dùng.
3. Dải ven biển của tỉnh: các điểm ranh giới tỉnh nằm gần trục bờ biển thật (không lấy đường bờ quốc gia, vì nó chạy sâu vào cửa sông).
4. Xuất SVG path ở toạ độ Web Mercator mức Z=8 → `geo.json`; `vector_map.js` dựng các lớp, camera (lat, lng, Z) nội suy Hermite,
   độ dày nét cố định trên màn hình, nhãn HTML gắn toạ độ, vòng sóng tính theo thời gian.
Mã đầy đủ đã dùng: `examples/vinh-long-v2/` trong repo.
