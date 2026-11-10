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

- Template mặc định `template/` là **dọc 1080×1920**, theo kiểu bay vào bản đồ, có tuyến neon, ghim, thẻ dự án và tiêu đề dưới. Template ngang cũ nằm ở `template-ngang/`.
- Ghép take: đoạn bản đồ (rig) → cinematic-zoom → cảnh 3D Google Earth (`camera-rig.md` §8) → cinematic-zoom → đoạn bản đồ. Xem `camera-rig.md` §6.
- Khi nghiệm thu, chạy `analyze_refs.py` trên bản render. Các chỉ số phải nằm trong cột **Mục tiêu** ở trên.
