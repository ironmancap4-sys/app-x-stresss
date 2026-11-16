# Ví dụ: One Era (257 s, 23 cảnh) — dựng bằng `scripts/scenegen.py`

1. Giọng đọc → `transcribe_vi.py`; số liệu đối chiếu: CafeF (03 & 07/11/2026), Báo Đầu tư, The Leader (25/09/2026), SGGP, Znews.
2. `geo_build.py geo_config.json geo.json` (TP.HCM cũ / Bình Dương cũ / BR-VT cũ tách riêng; QL13, Vành đai 3, Mỹ Phước–Tân Vạn, Nguyễn Thị Minh Khai, kênh Suối Cát, ranh công trường chọn trên ảnh vệ tinh z16).
3. Ảnh vệ tinh Esri z13 + z16 (làm tối, ngả navy) để bay liền từ bản đồ vùng xuống công trường.
4. Google Earth: `earth-shots/g1..g4.json` → `earth_capture.js` → `earth_encode.sh` → chỉnh màu navy.
5. Ảnh thật/phối cảnh từ bài báo (ghi nguồn trên khung); tài liệu gốc = trích nguyên văn đoạn có số liệu (font lớn cho khung dọc).
6. `python mk_storyboard.py` → `storyboard.json` → `scenegen.py storyboard.json <project>`; `mix_audio.py` với `sfx_events.json` (sinh từ storyboard).
