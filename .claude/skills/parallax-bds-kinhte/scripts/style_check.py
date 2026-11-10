#!/usr/bin/env python3
"""Kiểm tra cuối theo hệ thiết kế: chụp 1 khung/giây thành contact sheet + quét màu cấm.

  python style_check.py video.mp4 [--out style] [--per-sheet 15]

- sheet-NN.jpg: mỗi ô 1 giây, có nhãn thời gian -> soát bằng mắt: mỗi khung tối đa 1 tiêu đề lớn + 1 nhãn phân đoạn
  + nhãn kiểu A/B; không hộp đen, không phông thứ hai.
- Quét VÀNG (hue OpenCV 21–35, bão hoà và sáng cao) trong lớp đồ hoạ: > 0,3% khung -> cờ YELLOW.
  Cam nhấn #F28C28 có hue ≈ 14 nên không bị tính. Footage thật có vật màu vàng -> xem ảnh để quyết định.
Thoát mã 1 nếu có cờ.
"""
import argparse, os, sys
import cv2, numpy as np

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--out", default="style"); ap.add_argument("--per-sheet", type=int, default=15)
    ap.add_argument("--yellow", type=float, default=0.003)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    cap = cv2.VideoCapture(a.video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    tiles, flags = [], []
    for sec in range(int(n / fps) + 1):
        cap.set(cv2.CAP_PROP_POS_FRAMES, min(n - 1, int(sec * fps + fps / 2)))
        ok, fr = cap.read()
        if not ok: break
        small = cv2.resize(fr, (216, 384), interpolation=cv2.INTER_AREA)
        hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
        y = ((hsv[..., 0] >= 21) & (hsv[..., 0] <= 35) & (hsv[..., 1] > 150) & (hsv[..., 2] > 170)).mean()
        t = small.copy()
        cv2.rectangle(t, (0, 0), (70, 22), (0, 0, 0), -1)
        cv2.putText(t, f"{sec}s", (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        if y > a.yellow:
            flags.append((sec, f"YELLOW {y*100:.2f}%")); cv2.rectangle(t, (0, 0), (215, 383), (0, 255, 255), 3)
        tiles.append(t)
    cols = 5
    for k in range(0, len(tiles), a.per_sheet):
        chunk = tiles[k:k + a.per_sheet]
        while len(chunk) % cols: chunk.append(np.zeros_like(tiles[0]))
        rows = [np.hstack(chunk[i:i + cols]) for i in range(0, len(chunk), cols)]
        cv2.imwrite(f"{a.out}/sheet-{k // a.per_sheet + 1:02d}.jpg", np.vstack(rows))
    for s, m in flags: print(f"{s:4d}s  {m}")
    print(f"{len(tiles)} khung, {len(flags)} cờ -> {a.out}/sheet-*.jpg")
    sys.exit(1 if flags else 0)

if __name__ == "__main__":
    main()
