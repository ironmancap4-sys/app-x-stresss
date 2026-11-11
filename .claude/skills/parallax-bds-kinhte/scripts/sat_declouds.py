#!/usr/bin/env python3
"""Xoá mây khỏi ảnh vệ tinh ghép (sat_tiles.py) rồi chỉnh màu nền "tối, giảm bão hoà" cho bản đồ.

  python sat_declouds.py sat16.jpg [--min-area 900] [--grow 25] [--no-decloud]
  -> sat16_g.jpg (đã xoá mây + chỉnh màu) và sat16_dc.jpg (chỉ xoá mây)

Mây = mảng sáng (V>175), ít màu (S<45), diện tích ≥ min-area px (bỏ qua mái tôn nhỏ); mở rộng `grow` px để
ăn cả viền. Mỗi đám mây được lấp bằng một mảng kết cấu đô thị lấy ở gần đó không có mây (nhân bản có viền mờ) —
KHÔNG dùng inpaint Telea (để lại vệt xám hình sao). Gợi ý: z16 --min-area 900 --grow 25; z13 60/9; z11 30/5.
Luật QA: không được có mây hay ô chưa có ảnh đè lên khu vực đang nói tới.
"""
import argparse
import cv2, numpy as np
from PIL import Image, ImageEnhance

ap = argparse.ArgumentParser()
ap.add_argument("img"); ap.add_argument("--min-area", type=int, default=900); ap.add_argument("--grow", type=int, default=25)
ap.add_argument("--no-decloud", action="store_true")
a = ap.parse_args()
base = a.img.rsplit(".", 1)[0]
im = cv2.imread(a.img)
if not a.no_decloud:
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    v, s = hsv[..., 2].astype(int), hsv[..., 1].astype(int)
    m = cv2.morphologyEx(((v > 175) & (s < 45)).astype(np.uint8) * 255, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    k = cv2.connectedComponentsWithStats(m); keep = np.zeros_like(m)
    for i in range(1, k[0]):
        if k[2][i, 4] >= a.min_area: keep[k[1] == i] = 255
    keep = cv2.dilate(keep, np.ones((a.grow, a.grow), np.uint8))
    print(f"{a.img}: mây {keep.mean() / 2.55:.2f}% diện tích")
    out = im.copy().astype(np.float32); H, W = keep.shape
    cc = cv2.connectedComponentsWithStats(keep)
    for i in range(1, cc[0]):
        x, y, w, h, _ = cc[2][i]; comp = (cc[1] == i).astype(np.uint8)
        pad = 12; x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + w + pad), min(H, y + h + pad)
        cm = cv2.dilate(comp[y0:y1, x0:x1], np.ones((5, 5), np.uint8))
        fe = np.clip(cv2.GaussianBlur(cm.astype(np.float32), (0, 0), 4) * 1.6, 0, 1)[..., None]
        best = None
        for r in (1.2, 1.6, 2.2, 3.0):          # tìm mảng nguồn gần nhất không có mây
            for ang in range(0, 360, 30):
                dx, dy = int(np.cos(np.radians(ang)) * r * max(w, h)), int(np.sin(np.radians(ang)) * r * max(w, h))
                sx, sy = x0 + dx, y0 + dy
                if sx < 0 or sy < 0 or sx + (x1 - x0) > W or sy + (y1 - y0) > H: continue
                bad = keep[sy:sy + y1 - y0, sx:sx + x1 - x0].mean()
                if best is None or bad < best[0]: best = (bad, sx, sy)
            if best and best[0] == 0: break
        if not best: continue
        _, sx, sy = best
        out[y0:y1, x0:x1] = out[y0:y1, x0:x1] * (1 - fe) + im[sy:sy + y1 - y0, sx:sx + x1 - x0].astype(np.float32) * fe
    im = out.astype(np.uint8)
    cv2.imwrite(base + "_dc.jpg", im, [cv2.IMWRITE_JPEG_QUALITY, 92])
p = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
p = ImageEnhance.Color(p).enhance(.55); p = ImageEnhance.Brightness(p).enhance(.62); p = ImageEnhance.Contrast(p).enhance(1.12)
Image.blend(p, Image.new("RGB", p.size, (14, 26, 43)), .15).save(base + "_g.jpg", quality=86)
print("->", base + "_g.jpg")
