# Ví dụ v2: Kinh tế Vĩnh Long, làm theo `references/quy-tac-chuyen-gia.md`

Dọc 1080×1920, 30 fps, 88,6 s, từ một file giọng đọc. `python build.py` sinh `compositions/` từ `src/` (nhúng `geo.json`, `mapjs.js`, `mapcss.css`, nguồn hình trong `footage.json`).

| Thời gian | Chất liệu | Chứng minh câu thoại |
| --- | --- | --- |
| 0–28,4 | Bản đồ vector (`src/geo.html`) | 0–3 s toàn quốc → ĐBSCL → tỉnh; Vĩnh Long sau sáp nhập tô cam 80%; sông Tiền/Hậu chạy sáng theo dòng; TP.HCM, Cần Thơ tô xám + hành lang; "cực tăng trưởng" = viền sáng + sóng lan đúng từ khoá; dải ven biển phía Đông + tiểu vùng trung tâm + đường nối; câu hỏi lớn duy nhất |
| 28,4–37,3 | Cảnh quay thật (`src/foot.html`) | sông nước, chợ nổi ĐBSCL — hoạt động kinh tế thật |
| 37,3–66,74 | Bảng số tích luỹ trên nền bản đồ (`src/board.html`, `rows.py`) | 6 chỉ số icon + số ≥ 84 px + mô tả 36 px, ở lại tới hết |
| 66,74–72 | Ảnh tài liệu gốc (`src/doc.html`) | chụp bài Báo Đầu tư 07/09/2026, trượt chậm tới các đoạn số liệu, đánh dấu |
| 72–78,3 | Google Earth: cầu Mỹ Thuận (`src/earthb.html`) | |
| 78,3–88,6 | Kết (`src/end.html`) | cảnh quay thật có người; phụ đề 1/3 dưới căn trái; 1 thông điệp chốt |

Âm thanh: `sfx_events.json` + `scripts/mix_audio.py` → −14,0 LUFS, đỉnh −1,3 dBTP, SFX thấp hơn giọng 14 dB.
QA: `scripts/qa_frames.py` — còn 6 cờ đã xem: HAZE 67–69 s (trang báo nền trắng), DEAD_EDGE 88,5 s (mặt sông).

## Cảnh quay thật
Footage "Mekong Floating Markets, Ho Chi Minh, Vietnam" — Le Monde en Vidéo, CC BY 3.0 (Wikimedia Commons), tải bản 1080p chuyển mã.
Cắt dọc 570×1014 (x=560) → 1080×1920; ghi tác giả + giấy phép ở chân khung. Đoạn dùng: 60,5 s, 171 s (giữa video); 182,5 s, 204 s (đoạn kết, có người).
Video không quay tại Vĩnh Long nên nhãn ghi "Đồng bằng sông Cửu Long" / "Chợ nổi miền Tây", không gán địa danh sai.
Video "Traditional Vinh Long music" (quay tại Vĩnh Long, CC BY 3.0) chưa tải được do giới hạn tần suất của Wikimedia.
