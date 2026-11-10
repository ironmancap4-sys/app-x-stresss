---
name: parallax-bds-kinhte
description: Dựng video bất động sản và kinh tế/tài chính trong HyperFrames với camera chuyển động liên tục và parallax nhiều lớp (2.5D) - giá nhà, dự án, quy hoạch, lãi suất, thị trường, giải thích số liệu. Đọc trước khi dựng, edit hoặc remake video thể loại này, và khi cần phân tích video mẫu để học phong cách camera. Use for real-estate / economics explainer videos with continuous camera moves and parallax in HyperFrames.
---

# Video BĐS & kinh tế: camera liên tục + parallax (HyperFrames)

Skill này nằm TRÊN skill chính thức `/hyperframes`. Luật render (contract), CLI và vòng làm việc vẫn theo `/hyperframes`; ở đây chỉ có những gì riêng của thể loại: **một camera không bao giờ đứng chết, đi xuyên qua một thế giới có độ sâu**, và số liệu BĐS/kinh tế đặt vào thế giới đó.

Chưa có skill chính thức thì người dùng tự cài: `npx skills add heygen-com/hyperframes` (hoặc `npx hyperframes skills update`). Không tự chạy lệnh cài.

**Mặc định của skill = phong cách 5 video mẫu của người dùng** (`references/style-mau.md`): khung **dọc 1080×1920**, bay vào bản đồ vệ tinh → tuyến neon tự vẽ → ghim/thẻ dự án → cảnh 3D kiểu Google Earth (toà nhà, cao tốc dựng 3D từ dữ liệu bản đồ, không phải flycam thật), nối bằng zoom-blur; camera chạy ≥ 85% thời gian, cảnh thật 2,5–4 s. Video ngang chỉ khi được yêu cầu (`template-ngang/`).

## Ba điều không được vi phạm

1. **Camera liên tục.** Trong một take, camera luôn có ít nhất một kênh (x, y, z, orbit) đang chạy; vận tốc liên tục (không giật, không "trượt–dừng–trượt"). Chỉ dừng hẳn khi có chủ đích (`stop: true`) và tối đa một lần mỗi take. Mục tiêu đo được: camera chạy ≥ con số `continuity` của video mẫu (thường ≥ 85% thời gian).
2. **Parallax thật.** Mỗi cảnh có ≥ 3 lớp độ sâu (xa / giữa / gần), cộng thêm tiền cảnh khi camera di chuyển ngang. Parallax sinh ra từ phối cảnh thật (`perspective` + `translateZ`) của rig trong `template/`, không phải từ việc tween từng lớp với hệ số tự bịa.
3. **Chữ đứng yên khi đã đáp.** Camera chạy, chữ thì không: tiêu đề HUD (khoá màn hình) đáp xong là đứng im; nhãn số gắn vào thế giới (world-locked) thì trôi theo camera như một vật thể. Không dùng hiệu ứng "thở/lơ lửng" cho chữ.

## Quy trình

### 1. Học phong cách từ video mẫu (khi có)

```bash
pip install opencv-python-headless numpy
python scripts/analyze_refs.py "<thư mục video mẫu>" --out phan-tich
```

Đọc `phan-tich/SUMMARY.md`, xem `*/sheet-*.jpg` và `*/motion.png`, rồi điền các dòng `[NHÌN]` trong `phan-tich/STYLE_DRAFT.md` và lưu thành `STYLE.md` ở gốc project. Giữ rõ cái gì ĐO, cái gì NHÌN. Chi tiết cách đọc số: `references/analysis.md`.

Video mẫu cho **ngữ pháp** (nhịp cảnh, kiểu move, tốc độ, số lớp, cách chữ vào/ra, bảng màu), không cho nội dung: không lấy logo, giọng, cảnh quay của kênh khác. Muốn dựng lại y hệt một video cụ thể thì dùng `/reverse-any-video`.

Không có video mẫu mới: dùng `references/style-mau.md` (đã đo từ 5 video của người dùng), bổ sung bằng `references/genre-grammar.md`.

### 2. Kịch bản & số liệu

- Một ý chính cho cả video (theo `/hyperframes` → `references/types/explainer.md`, `types/data.md`).
- Mọi con số có nguồn; ghi nguồn nhỏ trên màn hình. Số chưa có nguồn thì ghi "minh hoạ". Một module dữ liệu duy nhất cấp số cho mọi chỗ.
- Lời dẫn tiếng Việt: đo tốc độ đọc thực tế của giọng (TTS/người thật), thường 3–4 âm tiết/giây; mỗi cụm ý ≈ một "điểm dừng" của camera.

### 2b. Có file giọng đọc sẵn

`python scripts/transcribe_vi.py voice.mp3 transcript.json` → lời + mốc từng từ. Mọi số liệu trong lời đọc phải đối chiếu nguồn báo chính thống (đọc bài gốc, ghi tên báo + ngày lên màn hình); Whisper hay nghe nhầm số và tên riêng. Mỗi cảnh/thẻ số đặt theo mốc của từ khoá.

### 3. Thiết kế thế giới & đường camera — `CAMERA.md`

Trước khi viết code, trải câu chuyện thành **một bản đồ thế giới** (các chương nằm nối nhau theo trục x, sâu dần theo z) và lập bảng đường camera:

| t (s) | Camera nhìn vào | z (dolly) | orbit | Lời dẫn / sự kiện tại đây |
| --- | --- | --- | --- | --- |
| 0 | toàn cảnh thành phố | −150 | −4° | hook |
| 8 | toà nhà dự án (depth 300) | 380 | 3° | "giá tăng 12,4%" — nhãn nổi lên |

Mỗi câu lời dẫn → camera *đang tới* đối tượng được nhắc (đến nơi đúng lúc từ khoá được đọc). Chuyển chương bằng chính chuyển động camera (bay ngang qua tiền cảnh, dive vào vật thể, kéo lùi để lộ cảnh mới), không fade giữa hai thế giới. Công thức các kiểu move: `references/camera-rig.md`.

### 4. Dựng từ template

```bash
npx hyperframes init <dir> --skip-skills
cp -r <skill>/template/* <dir>/
```

- `template/` (dọc, mặc định): `compositions/dive.html` = một take bay vào bản đồ: rig camera, lớp bản đồ (depth 0), nhãn/ghim (−30), thẻ dự án (−60), mây bay xuyên (−350), HUD (nhãn đầu trang, tiêu đề dưới, nguồn).
- `template-ngang/` (16:9): `compositions/world.html`, skyline nhiều lớp + biểu đồ.
- Thay bản đồ giả lập bằng ảnh vệ tinh thật hoặc video `bake-basemap` (Esri/Carto, ghi nguồn ảnh trên màn hình); thay lớp giả lập bằng ảnh tách lớp — "Tài sản" trong `references/camera-rig.md`.
- Sửa mảng `KEYS` theo `CAMERA.md`: `at(t, x, y, zoom, tilt, orbit)` nhắm vào điểm (x, y) của bản đồ; `zoom` nội suy theo log nên tốc độ lặn cảm nhận đều.
- Nhiều take (> ~25 s hoặc đổi hẳn không gian): mỗi take một file scene, nối bằng **match-move** (`references/camera-rig.md` §6).
- Đoạn bay bản đồ vệ tinh: ghép ảnh tile nhiều mức (vd. z10 vùng → z13 tỉnh → z15 thành phố), camera `lat/lng + Z` nội suy Hermite, ảnh chi tiết hiện dần khi Z tới; ghim/nhãn chiếu theo toạ độ mỗi khung nên giữ cỡ chữ cố định.
- Cảnh 3D: `scripts/earth_capture.js` + `scripts/earth_encode.sh` (`references/camera-rig.md` §8 A2).
- Video > 15 s có nhạc nền và SFX "whoosh" theo các cú lướt camera (`/hyperframes` → `references/sound.md`).

### 5. Kiểm tra (bắt buộc trước khi giao)

1. `npx hyperframes check --json` — sửa hết lỗi. Nếu báo `dead_stretch` trong lúc camera đang chạy: kiểm tra xem stage/cam của rig (`#d-stage`/`#d-cam` hoặc `#w-stage`/`#w-cam`) có bị gắn `data-layout-ignore` không (gắn vào thì detector không thấy camera).
2. `npx hyperframes snapshot --at <các mốc trong CAMERA.md>` và xem: chữ có bị cắt, nhãn có ra ngoài khung, lớp có hở mép khi dolly lùi/orbit không.
3. Render rồi **đo lại chính video của mình** bằng `analyze_refs.py` và so với cột "Mục tiêu" trong `references/style-mau.md` (hoặc `STYLE.md`): camera chạy ≥ 85%, ≤ 4 lần dừng/phút, cảnh thật 2,5–4 s, ≥ 75% cut khi đang chạy, parallax ≥ 70% cảnh (nội dung BĐS). Lệch thì sửa `KEYS`/cách nối take, không sửa ngưỡng đo.
4. Ghi `REVIEW.md` ngắn: các số đo so với mẫu, chỗ còn khác.

## Tham chiếu

| Cần | Đọc |
| --- | --- |
| Toán phối cảnh, API của rig, công thức từng kiểu move, nối take, lỗi thường gặp, chuẩn bị ảnh tách lớp | `references/camera-rig.md` |
| **Phong cách đo từ 5 video mẫu của người dùng (mặc định)** | `references/style-mau.md` |
| Từ vựng hình ảnh BĐS/kinh tế, màu tăng/giảm, font tiếng Việt, nhịp | `references/genre-grammar.md` |
| Đọc kết quả phân tích video mẫu, giới hạn của phép đo | `references/analysis.md` |
| Project mẫu chạy được, đã qua `check`: dọc bay vào bản đồ (mặc định) / ngang skyline | `template/` / `template-ngang/` |
