# Gói skill `parallax-bds-kinhte` — hướng dẫn gửi và cài

Dựng video dọc 9:16 (TikTok/Reels/Shorts) về kinh tế, bất động sản, hạ tầng trong HyperFrames, từ một file giọng đọc ra video hoàn chỉnh.

## Trong thư mục này

| File | Dùng khi |
|---|---|
| `parallax-bds-kinhte/` | thư mục skill đầy đủ (SKILL.md, references, design, scripts, templates, phông chữ) |
| `parallax-bds-kinhte.skill` | tải lên ứng dụng Claude (Settings → Capabilities → Skills → Upload skill) |
| `parallax-bds-kinhte.zip` | cùng nội dung với `.skill`, cho nơi chỉ nhận .zip |
| `parallax-bds-kinhte_ALL-IN-ONE.md` | một file văn bản duy nhất để dán/đính kèm cho AI khác (ChatGPT, Gemini…), chứa toàn bộ quy trình và mã nguồn |

## Cài đặt

- **Claude Code**: chép thư mục `parallax-bds-kinhte/` vào `~/.claude/skills/` (dùng mọi dự án) hoặc `<dự án>/.claude/skills/` (chỉ dự án đó).
- **Ứng dụng Claude (claude.ai / desktop)**: tải `parallax-bds-kinhte.skill` lên phần Skills.
- **AI khác**: gửi `parallax-bds-kinhte_ALL-IN-ONE.md` và yêu cầu làm theo; AI cần môi trường chạy được mã.

Skill này đứng trên skill chính thức HyperFrames: `npx skills add heygen-com/hyperframes`.

## Phần mềm cần có trên máy dựng

- Node.js 18+ (HyperFrames chạy bằng `npx hyperframes@0.9.28`), Chromium/Playwright (render, chụp Google Earth).
- Python 3.10+ với `numpy`, `pillow`, `opencv-python`, `shapely`, `faster-whisper` (chép lời tiếng Việt).
- `ffmpeg`.
- Mạng tới: nền vệ tinh Esri (server.arcgisonline.com), các báo nguồn, Wikimedia/Pexels (footage), npm (icon Material Symbols, phông).

## Đảm bảo máy khác làm ra video giống (BẮT BUỘC lần đầu)

Sau khi cài, trên máy mới chạy:

```bash
cd parallax-bds-kinhte
pip install -r requirements.txt
bash examples/ha-tang-one-era/build.sh ~/dung-thu
```

Script tự kiểm phiên bản công cụ, tải lại đúng các ảnh vệ tinh/ảnh báo của video mẫu và đối chiếu từng điểm ảnh, dựng lại video
mẫu rồi so 20 khung hình với khung chuẩn của video đã giao. Phải ra "TẤT CẢ ĐẦU VÀO KHỚP" và "20/20 mốc đạt" thì máy đó mới làm
video giống. Thêm `--render` để xuất luôn video đầy đủ (~70 phút). Không đạt: xem `examples/ha-tang-one-era/README.md`.

## Ba phong cách có sẵn

| Phong cách | Kết quả | Công cụ chính | Ví dụ |
|---|---|---|---|
| A — giải thích chậm | bản đồ vector + bảng số + tài liệu gốc + Google Earth | `scenegen.py` | `templates/kinh-te-dia-phuong`, `templates/one-era` |
| B — bản đồ + footage nhịp nhanh | 2,5–4 s/shot, thư viện hiệu ứng M1–M10/T1–T5/F1–F3/D1–D6, màu theo nghĩa | `motion.py` | `templates/one-era-motion` |
| C — một camera bay liên tục | 0 cắt cứng, lớp thông tin mọc trên bản đồ, icon, thẻ logo, cửa sổ ảnh, chống rung, mờ chuyển động | `flight.py`, `mb_post.py` | `templates/one-era-flight`, `templates/ha-tang-flight` |

Mỗi công cụ tự kiểm luật (nhịp, lặp hiệu ứng, tốc độ camera, vùng an toàn TikTok…) và xuất nhật ký: `SHOTLIST.md` (B) hoặc `CAMLOG.md` (C).

## Lưu ý khi dùng

- Số liệu trên màn hình phải theo bài báo gốc, không theo bản chép lời; lệch thì báo người dùng.
- Không lách giới hạn tải (Wikimedia 429…), không vẽ lại logo. Không tải được logo chính thức → huy hiệu chữ và ghi rõ trong nhật ký.
- Phần minh hoạ (hướng tuyến gần đúng, vị trí ghim, khối nhà) phải ghi "minh hoạ" trên màn hình.

## Bản cập nhật (17/11/2026) — đã gộp mọi chỉnh sửa làm cùng nhau

- `references/bai-hoc.md` (MỚI): toàn bộ lỗi đã gặp thật qua các video Vĩnh Long, One Era, hạ tầng Đông Bắc và cách sửa — số liệu theo nguồn chứ không theo lời đọc, ảnh/logo bị chặn tải, mây và mép ảnh vệ tinh, camera bò chậm, thẻ ảnh đè dòng nguồn, khối 3D che thẻ, render quá 2 giờ, AAC vọt đỉnh, OSM sập…
- `SKILL.md`: luật cốt lõi ghi rõ luật nào chỉ của phong cách A (1 màu cam) và B/C dùng màu theo nghĩa; thêm luật 8 "đọc bai-hoc.md trước khi giao"; bảng chọn phong cách.
- `scripts/render_segments.sh` (MỚI): render chia đoạn, ghép, mux âm thanh có limiter, đo mối nối.
- `scripts/sat_grid.py` (MỚI): dò tuyến đường trên ảnh vệ tinh có lưới toạ độ khi OSM không phản hồi.
- `flight.py`: CAMLOG.md có thêm "Mốc cần snapshot" (mọi lúc cửa sổ ảnh/thẻ logo/số lớn hiện) vì bộ kiểm HyperFrames không thấy chồng chéo giữa bản đồ và HUD.
- Sửa lỗi template: cờ `lead=False` và `logo=""` không bị lọc mất.

## Bản cập nhật kiểm máy mới (17/11/2026)

- `examples/ha-tang-one-era/` (MỚI): video mẫu chuẩn dựng lại được từ đầu — danh sách đầu vào kèm hash điểm ảnh, 20 khung chuẩn, `build.sh`.
- `scripts/doctor.py`, `requirements.txt` (MỚI): ghim và kiểm phiên bản numpy/Pillow/OpenCV/shapely/ffmpeg/node.
- `scripts/verify_golden.py` (MỚI): so khung dựng với khung chuẩn bằng SSIM; ra ảnh so sánh cho mốc lệch.
- Đã thử trên thư mục sạch: 18/18 đầu vào khớp, 20/20 khung đạt (SSIM 0,985–0,996); dịch một nhãn 80 px thì bị bắt (SSIM 0,949).
- `examples/ha-tang-one-era/project/vo.mp3` là giọng đọc gốc của video mẫu — xoá nếu không muốn gửi kèm (xem README của ví dụ).
