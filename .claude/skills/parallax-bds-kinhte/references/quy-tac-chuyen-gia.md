# Quy tắc bắt buộc: video "giải thích kinh tế – địa phương" (dọc 1080×1920, 30 fps)

Rút ra từ góp ý của các chuyên gia sau bản dựng Vĩnh Long đầu tiên (11/2026). Mục tiêu: **mọi câu thoại phải được CHỨNG MINH bằng hình**, không chỉ lặp lại bằng chữ. Mỗi quy tắc có cách kiểm; một quy tắc không kiểm được thì coi như chưa đạt.

## 1. Chất liệu: ≥ 4 loại, xen kẽ

| Loại | Dùng cho | Nguồn |
| --- | --- | --- |
| Bản đồ đồ hoạ vector 2D | định vị, so sánh, kết nối | Natural Earth/OSM; gộp tỉnh theo nghị quyết sáp nhập hiện hành |
| Cảnh quay thật (flycam/stock) của địa danh được nhắc | ≥ 1 lần ở giữa video, đặt ở khoảng lặng giọng đọc | Wikimedia Commons (CC), Pexels, Pixabay; flycam của người dùng; ghi tác giả + giấy phép trên màn hình |
| Bảng số liệu tích luỹ trên nền bản đồ | phần số liệu | số từ báo chính thống |
| Ảnh tài liệu gốc (bài báo/infographic/báo cáo) làm bằng chứng | sau bảng số liệu, 4–6 s | chụp trang báo (`scripts/doc_capture.js`); KHÔNG thay bằng thẻ chữ |
| 10–15 s cuối | người dẫn, hoặc footage thật có chuyển động | KHÔNG dùng ảnh vệ tinh tĩnh |

Google Earth 3D là hình dựng, không phải cảnh quay thật: dùng được để minh hoạ, nhưng không thay được ô "cảnh quay thật" và "10–15 s cuối". Không tìm được footage hợp lệ thì nói rõ với người dùng, đừng lặng lẽ thay.

**Kiểm:** liệt kê chất liệu theo thời gian trong `CAMERA.md`; đếm ≥ 4 loại; không có 2 đoạn liền nhau cùng loại > 30 s.

## 2. Bản đồ – quy tắc định vị

- **0–3 s:** zoom toàn quốc → vùng → tỉnh. **Giây 2** đã thấy vùng được nhắc tới.
- Tỉnh chính: tô toàn bộ ranh giới hành chính, cam `#F28C28`, độ đục 80% (`fill-opacity: 0.8`), không chỉ chấm/nhãn. Dùng ranh giới **sau sáp nhập** nếu đã có nghị quyết (ghi căn cứ ở chân khung).
- Tỉnh/thành so sánh (TP.HCM, Cần Thơ…): tô xám nhạt toàn ranh giới khi được nhắc.
- Sông được nhắc: vẽ sông phát sáng **chạy theo dòng chảy** (thượng nguồn → cửa biển) + nhãn. Lòng sông lấy từ dữ liệu (Natural Earth/OSM) hoặc dò trên ảnh vệ tinh, không vẽ tay ước lượng.
- "Kết nối / hành lang / bản lề": đường nối động giữa các điểm; camera kéo ra đủ rộng để thấy **cả hai đầu**.
- "Cực tăng trưởng / trung tâm": viền tỉnh phát sáng + vòng sóng lan, **đúng khung hình của từ khoá** (± 0,2 s).
- Mọi elip/vùng đánh dấu nằm trọn trong khung an toàn (cách mép 60 px). Vùng nền (ví dụ cả vùng ĐBSCL) chỉ bật khi đang nói tới nó, rồi tắt.

**Kiểm:** snapshot tại 2,0 s, tại mốc mỗi từ khoá (tên tỉnh, tên sông, "kết nối", "cực tăng trưởng"); nhìn xem hình đúng thứ được đọc chưa và có nằm trong khung an toàn không.

## 3. Chuyển động & nhịp

- Không cảnh nào đứng yên > 6 s; nền giữ lâu thì cứ 3–4 s có yếu tố mới (số, nhãn, hiệu ứng, đổi cỡ cảnh).
- Không giữ cùng một góc Google Earth > 8 s.
- Cắt / đổi chất liệu tại khoảng lặng giọng đọc > 0,4 s. Tìm bằng `ffmpeg -af silencedetect=noise=-30dB:d=0.25`. Giọng đọc liền (ít khoảng > 0,4 s) thì dùng các khoảng dài nhất, ghi rõ trong `CAMERA.md`.
- Chuyển cảnh: whip zoom có motion blur (≤ 0,3 s) hoặc cắt thẳng. **CẤM** chuyển cảnh thu nhỏ làm lộ viền khung: cảnh vào bắt đầu ở `scale ≥ 1` (ví dụ 1,45 → 1), cảnh ra phóng to (1 → 1,35).

**Kiểm:** `qa_frames.py` (STATIC > 6 s); bảng cắt cảnh so với bảng khoảng lặng.

## 4. Kiểm soát lỗi render (trước khi xuất)

- Không mây/mảng trắng mờ, không mảng đen/nâu do ảnh vệ tinh/3D chưa tải, không khung nhoè ngoài chuyển cảnh.
- Không > 5 khung đen/tối liên tiếp ngoài chủ đích.
- Chạy `python scripts/qa_frames.py out.mp4`: DEAD_EDGE (> 5% khung là vùng chết dính mép), HAZE, DARK_RUN, BLUR_RUN, STATIC. Có lỗi → xem ảnh nó lưu, sửa và render lại đoạn đó. Công cụ là bộ lọc thô: mọi cờ phải xem bằng mắt (nền phẳng có chủ đích như thẻ trắng có thể bị gắn cờ).
- Cảnh Google Earth: chọn đoạn không có mảng lưới thủng (thường ở mặt sông rộng); chụp thử 3 khung đầu/giữa/cuối trước khi dùng.

## 5. Chữ trên màn hình

- Không phụ đề chạy theo lời. Mỗi cảnh 1 "dòng neo" (≤ 7 từ) nói ý chính, hiện đúng lúc đọc từ khoá; các ý còn lại do nhãn gắn đồ hoạ (kiểu A/B, `he-thiet-ke.md`) gánh.
- Ngắt dòng thủ công: không để 1 từ đơn lẻ trên một dòng, không tách cụm trong ngoặc kép, mỗi dòng ≥ 2 từ (kiểm bằng `assert` khi sinh phụ đề).
- Chữ không đè nhãn bản đồ: khi hiện chữ to, ẩn nhãn bản đồ hoặc dời camera.
- Giữ: nhãn phân đoạn (kính mờ) ở trên, nguồn ở chân khung; % tăng trưởng = chữ cam + ▲, không nền.

## 6. Số liệu

- **Danh sách tích luỹ:** mỗi chỉ số = icon + số lớn + mô tả; xuất hiện lần lượt **và ở lại**; tới chỉ số cuối thấy cả bộ.
- Đếm số giữ lại; chữ số ≥ 72 px, mô tả ≥ 36 px.
- Sau danh sách: ảnh tài liệu gốc 4–6 s, zoom/trượt chậm vào phần số liệu vừa nói, đánh dấu (highlight) đúng đoạn.
- Số trên màn hình theo **nguồn báo**, không theo bản chép lời (Whisper nghe nhầm số). Lệch giữa lời đọc và nguồn → hiện số nguồn và báo người dùng.

## 7. Âm thanh

- Chuẩn hoá tổng thể −14 LUFS, true peak ≤ −1 dBTP.
- SFX nhẹ: whoosh khi zoom/chuyển cảnh, pop khi số/icon xuất hiện, riser trước câu hỏi lớn; thấp hơn giọng đọc ≥ 12 dB.
- Làm bằng `scripts/make_sfx.py` (SFX tổng hợp, không bản quyền) + `scripts/mix_audio.py voice.mp3 events.json mix.wav --duration <s>`; script in số đo cuối và báo lỗi nếu chưa đạt.

## 8. Đoạn kết

- 10–15 s cuối có điểm neo con người hoặc cảnh quay thật có chuyển động.
- Phụ đề nhỏ đặt 1/3 dưới, căn trái.
- Chữ to chỉ cho đúng 1 thông điệp chốt.
