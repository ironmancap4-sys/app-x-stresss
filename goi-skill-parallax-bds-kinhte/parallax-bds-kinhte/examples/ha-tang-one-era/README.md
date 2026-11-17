# Video mẫu chuẩn: "99% vẫn chưa thông xe" (hạ tầng quanh One Era) — kiểm máy mới

Đây là video cuối cùng đã giao (phong cách C, 130,6 s). Thư mục này cho phép MỘT MÁY KHÁC dựng lại đúng video đó và
CHỨNG MINH kết quả giống bản gốc, trước khi dùng máy đó làm video mới.

```bash
pip install -r ../../requirements.txt
bash build.sh ~/dung-thu              # ~15 phút: kiểm môi trường, tải đầu vào, sinh project, âm thanh, check, so 20 khung chuẩn
bash build.sh ~/dung-thu --render     # thêm render đầy đủ (~70 phút) + mờ chuyển động -> ~/dung-thu/out/final.mp4
```

| Bước | Kiểm gì | Đạt khi |
|---|---|---|
| doctor.py | Python, numpy, Pillow, OpenCV, shapely, ffmpeg, node đúng phiên bản ghim | "Môi trường khớp." |
| fetch_inputs.py | 7 ảnh vệ tinh (tải Esri + xoá mây + chỉnh màu), 9 ảnh báo, GSAP 3.15.0, phông | mọi dòng "KHỚP" (hash điểm ảnh) |
| music.wav | nhạc nền sinh từ seed cố định | "KHỚP" |
| mix_audio | giọng + 91 SFX + nhạc | −14,1 LUFS, đỉnh −1,3 dBTP |
| hyperframes check | lint, layout, runtime | "Check passed" |
| verify_golden.py | 20 khung tại mọi chương (mây, nghiêng 3D, cửa sổ ảnh, thẻ logo, cột 3D, zoom-through) so với `golden/` | 20/20 SSIM ≥ 0,97 |

Kết quả trên máy sạch (17/11/2026): 18/18 đầu vào khớp từng điểm ảnh, nhạc khớp, 20/20 khung đạt (SSIM 0,985–0,996).
Thử dịch một nhãn số 80 px → khung đó SSIM 0,949, KHÔNG ĐẠT: bộ so đủ nhạy để bắt lệch bố cục.
Khung chuẩn so với video đã giao (sau nén 5 Mbps) ở các đoạn giữ khung: SSIM ≈ 0,975.

## Khi không đạt

- Đầu vào KHÁC kèm "ẢNH NGUỒN đã đổi": báo/Esri đã thay ảnh — video vẫn đúng bố cục, chỉ khác ảnh đó.
- Đầu vào KHÁC mà nguồn khớp, hoặc nhạc KHÁC: lệch phiên bản thư viện → `pip install -r requirements.txt`.
- Không tải được: mở mạng cho các host trong `inputs.json` (cdnphoto.dantri.com.vn, image.sggp.org.vn, images2.thanhnien.vn,
  i.ex-cdn.com, server.arcgisonline.com, registry.npmjs.org).
- Khung KHÔNG ĐẠT: mở `out/verify/KHAC_<t>.jpg` (trái = chuẩn, phải = máy này). Lệch chữ toàn bộ = thiếu phông/khác Chromium
  (hyperframes@0.9.28 tự tải trình duyệt riêng; xoá cache `~/.cache/hyperframes` rồi chạy lại).

`vo.mp3` là giọng đọc gốc của video mẫu, chỉ dùng để kiểm máy. Muốn gửi skill mà không kèm giọng đọc: xoá file này; bước
âm thanh sẽ lỗi nhưng bước so khung (chỉ hình) vẫn chạy được nếu tạo `assets/mix.wav` im lặng
(`ffmpeg -f lavfi -i anullsrc=r=48000:cl=stereo -t 130.6 assets/mix.wav`).
