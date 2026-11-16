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
