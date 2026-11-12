# One Era · "phép tính 25%" — phong cách C (một camera, một bản đồ)

Dọc 1080×1920, 30 fps, 260,23 s, 15 chương, 71 keyframe camera, 0 cắt cứng, footage 5 lần × ≤ 2,9 s (5%).
Đọc `references/flight-style.md` trước.

1. Bản đồ: `geo_build.py` (tỉnh, đường, kênh, ranh dự án) → `python prep_geo.py <thư mục dữ liệu>` thêm biên giới Hoa Kỳ/Việt Nam
   (Natural Earth 10m), đại lộ nội khu minh hoạ, vùng xanh, và `blocks.json` — 60 khối minh hoạ phủ đúng 25% diện tích ranh.
2. Nền vệ tinh: `sat_tiles.py` — w03 (z3 cả thế giới), a05 (z5 châu Á 47°N–14°S, 82–140°E), sat07 (27…−7°, 90–124°),
   sat09 (16,5…4,5°, 101,5–112,5°), sat11/13/16 quanh dự án; xoá mây (`sat_declouds.py`) rồi chỉnh màu −20% sáng, −15% bão hoà.
3. `python mk_flight.py` → `proj/flight.json`; `python flight.py proj/flight.json proj` → hết "!" ; xem `CAMLOG.md`.
4. `python mk_sfx3.py proj/flight.json proj/sfx/events.json`; `make_music.py music.wav --dur 260.3 --bpm 96`;
   `mix_audio.py assets/vo.mp3 sfx/events.json assets/mix.wav --duration 260.23 --music music.wav`.
5. `npx hyperframes check`, `snapshot`, `render`.

Minh hoạ (ghi trên màn hình): khối nhà và vị trí One Park/Central District/ghim tiện ích/đại lộ 25 m; vị trí Hyde Park;
lượng người đi bộ; bán kính đi bộ 80 m/phút. Số liệu: CafeF, Báo Đầu tư, VnExpress/Znews (Fitwel 3 sao), The Leader (Longfor).
