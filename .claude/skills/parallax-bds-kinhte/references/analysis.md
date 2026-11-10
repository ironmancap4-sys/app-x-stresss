# Phân tích video mẫu bằng `scripts/analyze_refs.py`

```bash
pip install opencv-python-headless numpy
python scripts/analyze_refs.py "<thư mục hoặc file>" --out phan-tich [--width 480] [--step 2]
```

Windows: đường dẫn có dấu cách/dấu tiếng Việt phải đặt trong ngoặc kép; script tự xử lý tên file Unicode. `--step 2` nhanh gấp đôi (đủ dùng cho video 30/60 fps).

## Kết quả

| File | Nội dung |
| --- | --- |
| `SUMMARY.md` | bảng tổng + danh sách cảnh từng video |
| `STYLE_DRAFT.md` | nháp `STYLE.md`: dòng `[ĐO]` đã điền, dòng `[NHÌN]` để điền bằng mắt |
| `summary.json` | toàn bộ số liệu, máy đọc được |
| `<video>/sheet-NN.jpg` | mỗi cảnh một hàng: khung đầu / giữa / cuối + nhãn chuyển động |
| `<video>/motion.png` | tốc độ pan (vàng) và zoom (xanh) theo thời gian; nền xanh lá = camera đang chạy; vạch đỏ = cut |

Xem `sheet-*.jpg` và `motion.png` bằng công cụ đọc ảnh trước khi viết `STYLE.md`.

## Các chỉ số

| Chỉ số | Nghĩa | Dùng để |
| --- | --- | --- |
| `continuity_moving_frac` | % thời gian (trừ khung cắt) camera đang pan/zoom/xoay vượt ngưỡng | mục tiêu tối thiểu cho video của mình |
| `stops_total` | số lần camera đứng yên ≥ 0,4 s | thể loại này thường rất thấp |
| `avg_shot_sec` | độ dài cảnh trung bình | đặt khoảng cách key và độ dài take |
| `cuts_on_motion_frac` | % cut xảy ra khi camera vẫn đang chạy | cao → nối take bằng match-move |
| `match_move_cuts_frac` | % cut mà hướng ra/vào cùng chiều (cos > 0,7) | quy tắc nối take |
| `parallax` (mỗi cảnh) | sai lệch của các điểm so với một chuyển động phẳng duy nhất, chia cho độ lớn chuyển động | ≥ 0,18 → có nhiều lớp độ sâu |
| `layer_spread` | (p90 − p10)/trung vị của vận tốc dọc hướng di chuyển | ≈ chênh lệch tốc độ giữa lớp gần và lớp xa; ≥ 0,6 là parallax rõ |
| `pan_pct_w_s`, `zoom_pct_s` | tốc độ pan (% chiều rộng khung/giây) và zoom (%/giây) | khoảng tốc độ cho `KEYS` |
| `enters_moving` / `exits_moving`, `dir_in` / `dir_out` | cảnh bắt đầu/kết thúc khi camera đang chạy, và theo hướng nào | thiết kế mối nối |
| `palette` | 6 màu chủ đạo theo tỉ lệ diện tích | dòng màu trong `STYLE.md` |

Hướng: `vx` là hướng **hình** trôi; hình trôi sang trái (`vx` < 0) nghĩa là camera đi sang phải.

## Giới hạn — kiểm lại bằng mắt

- Chữ/đồ hoạ HUD đứng yên chiếm nhiều diện tích sẽ kéo tốc độ đo xuống và có thể bị tính là "parallax" (lớp đứng yên so với nền chạy). Đối chiếu với sheet.
- Video có người/xe chuyển động nhiều cũng làm tăng chỉ số parallax.
- Hoà tan dài hoặc whip rất nhanh có thể bị đếm thành 2 cut hoặc bị bỏ sót; `motion.png` cho thấy rõ.
- Nhãn "push-in" có thể là zoom quang học (không có parallax) hoặc dolly thật (có parallax): xem cột parallax cùng hàng.
- Video sau khi tải lại từ mạng xã hội bị nén mạnh: dùng `--width 640` cho ổn định hơn.

## Kiểm định video của mình

Chạy lại script trên bản render của mình cùng thư mục `--out` khác, rồi so từng chỉ số với mẫu. Đây là tiêu chí nghiệm thu "camera liên tục + parallax" trong `SKILL.md` §5.
