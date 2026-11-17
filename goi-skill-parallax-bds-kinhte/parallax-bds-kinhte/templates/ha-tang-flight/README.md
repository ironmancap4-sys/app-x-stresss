# Hạ tầng quanh One Era (Vành đai 3 · QL13 · metro) — phong cách C v2

130,6 s, 10 chương, 37 keyframe, 0 cắt cứng; 9 cửa sổ ảnh báo; huy hiệu Material Symbols; 2 thẻ tổ chức dạng chữ (không tải được logo).
1. `python prep_geo4.py <scratch>` — thêm tuyến (VĐ3 phía Đông dò trên ảnh vệ tinh, đoạn gần Tân Vạn từ OSM, phần còn lại gần đúng), QL13 xong/chờ, metro.
2. `python mk_flight4.py` → proj/flight.json; `python flight.py proj/flight.json proj` → hết "!" (đọc bảng giữ khung + tài sản trong CAMLOG.md).
3. `python mk_sfx3.py proj/flight.json proj/sfx/events.json`; `make_music.py ../music.wav --dur 130.7 --bpm 92`; `mix_audio.py ... --music`.
4. `npx hyperframes check` → `snapshot` đúng các mốc trong CAMLOG.md "Mốc cần snapshot" → `scripts/render_segments.sh proj out/raw.mp4 130.6` (chia đoạn, mux âm thanh có limiter, kiểm mối nối) → `scripts/mb_post.py flight.json out/raw.mp4 out/final.mp4`.
5. Đọc `references/bai-hoc.md` trước khi giao.
