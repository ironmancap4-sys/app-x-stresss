# Skill: video BĐS & kinh tế với camera liên tục + parallax (HyperFrames)

Skill Claude Code tại `.claude/skills/parallax-bds-kinhte/`:

- `SKILL.md` — quy trình: phân tích video mẫu → `STYLE.md` → `CAMERA.md` → dựng từ template → kiểm định bằng số đo.
- `scripts/analyze_refs.py` — đo video mẫu: cắt cảnh, pan/zoom/xoay, % thời gian camera chạy, số lần dừng, chỉ số parallax, bảng màu, contact sheet.
- `template/` — project dọc 1080×1920 (mặc định, theo phong cách video mẫu): bay vào bản đồ, tuyến neon tự vẽ, ghim, thẻ dự án, mây bay xuyên; rig camera 3D, đường camera Hermite liên tục vận tốc, zoom nội suy log.
- `template-ngang/` — bản 16:9: skyline nhiều lớp, nhãn giá gắn vào toà nhà, biểu đồ camera bay dọc.
- `references/style-mau.md` — phong cách đo từ 5 video mẫu (mục tiêu nghiệm thu).
- `references/` — toán phối cảnh & công thức move, ngữ pháp hình ảnh BĐS/kinh tế, cách đọc số đo.

Cần skill chính thức `/hyperframes` (`npx skills add heygen-com/hyperframes`).

Phân tích thư mục video mẫu trên Windows:

    pip install opencv-python-headless numpy
    python .claude\skills\parallax-bds-kinhte\scripts\analyze_refs.py "C:\Users\Admin\Downloads\video mau" --out phan-tich
