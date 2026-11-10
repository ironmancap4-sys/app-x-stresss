# Skill `parallax-bds-kinhte`: video kinh tế – bất động sản – địa phương (HyperFrames, dọc 9:16)

Toàn bộ skill nằm trong `.claude/skills/parallax-bds-kinhte/` — bắt đầu từ `SKILL.md`.

- Từ một file giọng đọc → video hoàn chỉnh: bản đồ vector (tỉnh gộp theo nghị quyết, sông, kết nối), cảnh quay thật, bảng số liệu tích luỹ từ báo chính thống, ảnh tài liệu gốc, Google Earth 3D, camera liên tục + parallax.
- Hệ thiết kế báo chí kinh tế (Be Vietnam Pro, 1 màu nhấn cam, 2 kiểu nhãn, dòng neo), vùng an toàn TikTok, độ rõ tối thiểu, âm thanh −14 LUFS.
- Kiểm tra tự động: `qa_frames.py`, `style_check.py`, `mix_audio.py` (đo loudness), `analyze_refs.py`.

Cài trên máy (Windows): giải nén `parallax-bds-kinhte-skill.zip` vào `%USERPROFILE%\.claude\skills\` (được thư mục `%USERPROFILE%\.claude\skills\parallax-bds-kinhte\SKILL.md`). Cần thêm skill chính thức HyperFrames: `npx skills add heygen-com/hyperframes`.
