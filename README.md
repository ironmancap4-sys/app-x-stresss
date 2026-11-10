# Skill: video BĐS & kinh tế với camera liên tục + parallax (HyperFrames)

Skill Claude Code tại `.claude/skills/parallax-bds-kinhte/`:

- `SKILL.md` — quy trình: phân tích video mẫu → `STYLE.md` → `CAMERA.md` → dựng từ template → kiểm định bằng số đo.
- `scripts/analyze_refs.py` — đo video mẫu: cắt cảnh, pan/zoom/xoay, % thời gian camera chạy, số lần dừng, chỉ số parallax, bảng màu, contact sheet.
- `template/` — project HyperFrames chạy được: rig camera 3D (perspective thật), đường camera Hermite liên tục vận tốc, 6 lớp độ sâu, nhãn giá gắn vào toà nhà, biểu đồ camera bay dọc.
- `references/` — toán phối cảnh & công thức move, ngữ pháp hình ảnh BĐS/kinh tế, cách đọc số đo.

Cần skill chính thức `/hyperframes` (`npx skills add heygen-com/hyperframes`).

Phân tích thư mục video mẫu trên Windows:

    pip install opencv-python-headless numpy
    python .claude\skills\parallax-bds-kinhte\scripts\analyze_refs.py "C:\Users\Admin\Downloads\video mau" --out phan-tich
