# Ngữ pháp hình ảnh: bất động sản & kinh tế

Giá trị mặc định khi không có video mẫu. Có `STYLE.md` từ video mẫu thì `STYLE.md` thắng.

## Mỗi loại thông tin → một vật thể trong thế giới

Chọn "hình" trước khi chọn hiệu ứng; các câu giống nhau phải ra các hình khác nhau.

| Thông tin | Vật thể trong thế giới | Camera làm gì |
| --- | --- | --- |
| Giá/m², % tăng của một dự án | nhãn giá cắm trên nóc toà nhà (world-locked), đếm số 1,2–1,6 s | push-in tới toà nhà, nhãn nổi ở cuối đường |
| So sánh giá các khu | các toà/cột cao theo giá đứng thành hàng trong thế giới | truck ngang dọc hàng cột |
| Giá theo thời gian | đường giá là "con đường" ở depth 0 | đi dọc đường giá khi nó tự vẽ |
| Vị trí, khoảng cách (km tới trung tâm, metro, vành đai) | bản đồ vệ tinh thật + ghim + đường đo | dive từ trên cao xuống, ghim xuất hiện khi camera dừng chậm |
| Quy hoạch, hạ tầng mới | lớp bản đồ tương lai phủ lên ảnh hiện tại (wipe theo đường) | crane lên để thấy toàn tuyến |
| Cung – cầu | hai nhóm khối nhà/người hội tụ hoặc tách ra | dolly lùi để thấy toàn bộ |
| Lãi suất, tín dụng | một con số rất lớn ở depth 0, các lớp đồng tiền/giấy tờ trôi phía sau | push-in vào con số |
| Chu kỳ thị trường | đường sóng chạy qua các "trạm" năm | truck ngang, mỗi trạm một nhãn |
| Hiểu lầm vs sự thật | câu sai bị gạch, câu đúng in đè | camera không đổi hướng, chỉ dolly nhẹ |

Tránh: slide gạch đầu dòng, ba thẻ xếp hàng, lưới KPI, biểu đồ tròn, mọi số đếm cùng lúc, số không nguồn.

## Màu

- Ngữ nghĩa thị trường Việt Nam (chứng khoán, cũng là thói quen khán giả): **xanh lá = tăng, đỏ = giảm, vàng = tham chiếu/đứng giá**, tím = trần, xanh lam = sàn. Khi video nói về giá BĐS tăng, màu nhấn ấm (vàng/cam) hoặc xanh lá đều được — giữ một quy ước cho cả video và không dùng đỏ cho "tăng".
- Một màu nhấn duy nhất mang nghĩa; phần còn lại trung tính. Nền tối xanh-đêm hoặc sáng giấy tuỳ video mẫu.
- Gradient tuyến tính toàn khung trên nền tối dễ bị banding khi nén H.264: dùng radial hoặc nền đặc + quầng sáng cục bộ.

## Chữ tiếng Việt

- Font phải có bộ dấu tiếng Việt đầy đủ. Có sẵn trong HyperFrames và hỗ trợ tiếng Việt qua Google Fonts: Montserrat, Inter, Roboto, Open Sans, Oswald, Playfair Display, Nunito, EB Garamond. Font khác (Be Vietnam Pro, SVN-…) cần `@font-face` trỏ tới file trong `assets/fonts/`.
- Luôn snapshot một dòng thử có "ữ ặ ỡ ẫ ự Đ" ở cỡ lớn để chắc dấu không vỡ/chồng.
- Số: `font-variant-numeric: tabular-nums`; dấu thập phân là dấu phẩy (12,4%), phân cách nghìn bằng dấu chấm (1.250 tỷ); đơn vị: "triệu/m²", "tỷ đồng".
- Tiêu đề 4–9% chiều cao khung, 1–2 dòng; chữ phụ ≥ 28 px (sàn đọc được trên điện thoại). Một từ nhấn màu.

## Nhịp

- Hook trong 3 s đầu: một câu hỏi hoặc một con số lớn trên toàn cảnh đang chuyển động.
- Mỗi cụm lời dẫn ≈ một chặng camera (2,5–4 s). Chữ đọc được giữ ≥ 0,5 s + 0,3 s/từ.
- Nhãn và chữ xuất hiện khi lời dẫn nhắc tới, không bày sẵn từ đầu cảnh.
- Kết: kéo lùi + một câu chốt, giữ ≥ 2 s.

## Âm thanh

- Nhạc nền (bed) cả video; whoosh nhẹ ở các cú lướt nhanh/foreground wipe, "tick" khi số đếm đáp. Âm thanh bắt đầu sớm hơn hình 40–190 ms với hành động phải "trúng nhịp".
- Theo `/hyperframes` → `references/sound.md` và `/media-use` cho việc lấy nhạc/giọng.
