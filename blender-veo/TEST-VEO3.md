# Test: Veo 3 có "hiểu" không gian dựng từ Blender không?

Mục tiêu: chỉ tốn khoảng **3–6 lần tạo video** để biết Veo giữ không gian tốt đến đâu, trước khi làm cả dự án.

## Chuẩn bị (miễn phí, làm trong Blender)
1. Dựng một căn phòng đơn giản có **vật mốc dễ nhận ra**: một cửa sổ, một ghế màu đỏ, một bức tranh, một chậu cây.
2. Đặt 2 camera: `Cam_A` (nhìn thẳng vào phòng) và `Cam_B` (cách Cam_A khoảng 2–3 m, góc lệch khoảng 30–45°).
3. Chạy `blender_xuat_cho_ai.py` để lấy `ai_export/keyframes/Cam_A.png` và `Cam_B.png`.

## 3 bài test (trong Google Flow: chọn *Frames to Video*, hoặc dùng phần B trong notebook Colab)

| Bài | Đưa vào Veo | Prompt gợi ý | Kiểm tra điều gì |
|---|---|---|---|
| **T1** | Khung đầu: Cam_A | *Static camera. Soft daylight moves across the room, curtains sway gently. Photorealistic, keep every object exactly in place.* | Veo có giữ nguyên phòng khi camera đứng yên không (dễ nhất) |
| **T2** | Khung đầu: Cam_A, khung cuối: Cam_B | *Smooth slow dolly move through the same room, photorealistic, no new objects, consistent architecture.* | Veo có di chuyển đúng giữa 2 góc nhìn thật không |
| **T3** | Khung đầu: Cam_A | *Camera slowly pans 180 degrees to reveal the rest of the room. Photorealistic.* | Phần phòng Veo chưa được thấy có bị bịa ra không (khó nhất) |

Tiết kiệm tín dụng: dùng **Veo 3 Fast** cho cả 3 bài. Bài nào đạt mới tạo lại bằng bản chất lượng cao.

## Bảng chấm điểm (0 = hỏng, 1 = lệch nhẹ, 2 = giữ đúng)

| Tiêu chí | T1 | T2 | T3 |
|---|---|---|---|
| Vật mốc giữ đúng vị trí (ghế, tranh, cửa sổ) | | | |
| Tường, trần, sàn không cong hoặc biến dạng | | | |
| Không tự thêm hoặc mất đồ vật | | | |
| Ánh sáng khớp với render Blender | | | |
| Độ chân thực tăng lên so với render | | | |

## Đọc kết quả
- **T1 + T2 đạt (≥ 8/10):** dùng Veo cho shot ngắn, chia cảnh theo cặp camera Blender (khung đầu + khung cuối).
- **T3 hỏng (thường gặp):** không để Veo tự xoay camera rộng. Shot cần xoay hoặc bay phức tạp thì chuyển sang **Wan VACE** (phần A trong notebook), vì nó bám theo depth map nên không gian đúng 100%.
- **T1 cũng hỏng:** ảnh render có thể quá "giả" hoặc quá tối. Tăng samples, thêm vật liệu PBR thật và HDRI rồi thử lại.
