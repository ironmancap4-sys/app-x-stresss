# Hệ thiết kế: báo chí kinh tế, tối giản, sang

Áp cho mọi video "giải thích kinh tế – địa phương". Một phông, một màu nhấn, hai kiểu nhãn. Mã: `design/design.css` (dán vào `<style>` của mọi scene, cùng `fonts.css` sinh bởi `design/install_fonts.sh`), bản đồ: `scripts/vector_map.css/.js`.

## Phông: chỉ Be Vietnam Pro (đủ dấu tiếng Việt), nạp từ file
| Vai trò | Độ đậm | Cỡ | Ghi chú |
| --- | --- | --- | --- |
| Dòng neo (tiêu đề lớn) | 800 | 64–72 px (mặc định 68) | IN HOA, giãn +1%, 1–2 dòng, mỗi dòng ≥ 2 từ, `white-space: nowrap` từng dòng |
| Số liệu | 800 | 88–96 px | `font-variant-numeric: tabular-nums` |
| Nhãn bản đồ/ảnh (kiểu A) | 600 | 30–34 px (mặc định 32) | bóng mềm, không hộp |
| Mô tả dưới số | 500 | 28–30 px | trắng 88% |
| Nhãn phân đoạn trên cùng | 600 | 24 px | IN HOA, giãn +8%, kính mờ |
| Chân trang nguồn | 500 | 20 px | trắng 72%, đặt dưới nhãn phân đoạn |
Cấm phông tròn/hoạt hình, cấm phông thứ hai.

## Màu (`#root` khai báo biến)
- Nền: navy `#0E1A2B` → `#13243A` (gradient), có lớp chấm 7 px rất mờ để không có mảng phẳng.
- **Màu nhấn duy nhất: cam `#F28C28`**: tỉnh chính (đục 80%), từ khoá nhấn trong dòng neo (`<em>`), icon nét, vạch/vòng sóng, viền thẻ khái niệm, chữ tăng trưởng.
- Chữ: `#FFFFFF`, trắng 88%, trắng 72% (không mờ hơn).
- Trung tính: xám xanh `#8A97A8` — tỉnh lân cận/so sánh, đường kết nối phụ, vùng nền.
- Sông: xanh ngọc giảm sáng 20% (`#2B8E93` quầng, `#8FBFBC` lõi).
- Tăng trưởng: chữ cam + `▲`, không nền (cấm tag xanh lá đặc).
- **Cấm vàng** (`#ffd23f`…), cấm hộp đen đặc, cấm nền xanh dương đặc cho nhãn phân đoạn.

## Thành phần
- `.seg` nhãn phân đoạn: nền trắng 10%, viền trắng 20%, bo 999 px, `backdrop-filter: blur(10px)`.
- `.anchor` dòng neo: ≤ 7 từ, 1 dòng neo cho 1 ý của cảnh, hiện đúng lúc giọng đọc nói từ khoá; `.low` = đáy (bottom 300 px, trong vùng gradient), `.mid` = giữa (chỉ trên nền bản đồ tối). Không có phụ đề chạy theo lời.
- `.la` **Kiểu A — nhãn gắn vật thể** (mọi địa danh): chấm 10 px + đường dẫn 2 px + chữ 32 px bóng (0 0 12px đen 50%); chấm đặt đúng vật thể; đường dẫn đưa chữ ra chỗ trống (ra ngoài tỉnh, không đè sông). Trên bản đồ dùng `data-at/data-lx/data-ly/data-align`, `vector_map.js` tự dựng.
- `.lb` **Kiểu B — thẻ khái niệm** (Vùng đệm?, Cực tăng trưởng, Bản lề kết nối): viền cam 2 px, nền navy 70%, bo 8 px, chữ trắng IN HOA 28 px.
- `.foot` chân trang nguồn.
- `.gtop`/`.gbot` gradient navy 0→85% trên 18% / dưới 22% khung cho mọi ảnh/video, để chữ trắng đọc được mà không cần hộp.

## Vùng an toàn TikTok / Reels / Shorts (bắt buộc)
Giao diện ứng dụng che một phần khung 1080×1920. **Không đặt chữ, số, nhãn, vật thể đang được chỉ vào** trong:
| Vùng | Toạ độ | Bị che bởi |
| --- | --- | --- |
| Trên | y < 210 | thanh "Đang follow / Dành cho bạn", tìm kiếm |
| Dưới | y > 1440 | tên kênh, caption, nhạc, thanh tiến trình |
| Cột phải | x > 940 khi 700 < y < 1440 | avatar, tim, bình luận, lưu, chia sẻ |
Vị trí chuẩn trong `design.css`: nhãn phân đoạn `top: 230px`; chân trang nguồn `top: 300px` (ngay dưới nhãn phân đoạn, không để ở đáy); dòng neo `.low` `bottom: 520px` (đáy chữ ở y ≈ 1400), `.mid` `top: 760px`; mọi khối nội dung lề phải ≥ 140 px (`right: 150px` cho dòng neo, bảng số rộng 860 px từ x = 70, trang báo 880 px). Nhãn bản đồ: chỉnh camera (lệch tâm) để tỉnh và nhãn dưới tỉnh nằm trên y = 1440. `style_check.py` tô đỏ các vùng này trên contact sheet; không chữ nào được nằm trong vùng đỏ.

## Độ rõ tối thiểu (không để chữ và nét vẽ quá mờ)
- Chữ: không dưới 72% trắng (chân trang 72%, mô tả 88%), cỡ ≥ 20 px; chữ trên ảnh/video luôn có bóng đậm (`0 0 12px rgba(0,0,0,.7)`) và nằm trên gradient navy.
- Nét bản đồ: ranh giới ≥ 2 px, màu đủ sáng trên nền navy (`#4F6688`–`#5A7194`); đường kết nối/hành lang ≥ 5 px màu `#B3BECB`; sông lõi `#B5DEDB` 4 px + quầng 14 px; đường dẫn nhãn kiểu A 3 px.
- Lớp làm mờ có chủ đích (bản đồ nền 35% sau bảng số, nền tối sau câu hỏi lớn) chỉ dùng phía sau nội dung chính, không dùng cho chính nội dung cần đọc.

## Ảnh/video
- Google Earth: chỉnh màu trước bằng ffmpeg (không dùng CSS filter):
  `eq=saturation=0.75:contrast=1.08:gamma=0.97,colorbalance=rs=-0.06:gs=-0.02:bs=0.06:rm=-0.02:bm=0.02` (giảm bão hoà 25%, kéo tối về navy, tăng tương phản nhẹ).
- Footage thật: cắt dọc tránh logo watermark, ghi tác giả + giấy phép ở `.foot`; chỉ gắn nhãn kiểu A khi vật thể đứng yên trong khung.
- Chuyển bản đồ → ảnh: zoom xuyên vào tâm tỉnh + hoà màu 12 khung (cảnh sau bắt đầu sớm 0,4 s, opacity 0→1), không cắt thẳng.

## Đồng bộ
- Mọi chữ (dòng neo, nhãn, nhãn phân đoạn, chân trang) tắt hết **trước** khung chuyển cảnh/điểm cắt.
- Ảnh tài liệu giữ tới khi giọng đọc nói xong câu nhắc tới nó; mở bằng toàn bộ tiêu đề, zoom chậm vào đúng đoạn số vừa đọc, highlight cam 30%. Đặt trang lùi vào trong thẻ để zoom không cắt chữ ở mép.
- Bảng số: căn giữa ≤ 920 px, không thẻ nền; icon nét cam 44 px | số trắng 88 px + đơn vị 32 px trắng 75% | mô tả 28 px; đường kẻ trắng 10%; dòng mới hiện cùng lúc với số (fade + trượt lên 20 px), đếm 0,8 s **từ 40% giá trị** (không bao giờ hiện 0); bản đồ tỉnh phóng to ở nền, mờ 35%.

## Kiểm tra cuối
`python scripts/style_check.py out.mp4` → contact sheet 1 khung/giây + cờ màu vàng. Soát từng ô: không chữ nào trong vùng đỏ (TikTok che); tối đa 1 dòng neo + 1 nhãn phân đoạn + nhãn A/B; không hộp đen, không vàng, không phông thứ hai, không chữ còn mờ sang cảnh sau. Sai → sửa và render lại.
