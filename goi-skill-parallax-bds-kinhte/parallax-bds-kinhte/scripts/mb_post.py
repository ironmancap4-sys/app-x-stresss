#!/usr/bin/env python3
"""mb_post.py — mờ chuyển động THẬT theo vận tốc camera, làm sau render (giữ nguyên 30 fps, không đổi tốc khung).

  python mb_post.py flight.json raw.mp4 out.mp4 [--shutter 180] [--min 2] [--samples 16]

Vì sao làm sau: lọc mờ trong trình duyệt trên cảnh 3D + ảnh vệ tinh lớn làm render chậm ~7 lần (≈ 6 giờ / 2 phút video).
Ở đây mỗi khung lấy vận tốc camera từ đúng đường Hermite của vmap3.js (cam_sampler trong flight.py), quy ra vector màn hình
(theo bearing, phóng theo pitch), độ dài vệt L = vận tốc × shutter/360. L < min px → giữ nguyên khung (khung đứng/trôi chậm sắc nét).
Kernel đường thẳng ≥ `samples` mẫu, khử răng cưa; zoom/quay thêm vệt đều nhỏ. Vùng UI cố định (dòng nguồn, chú giải, đoạn footage)
được giữ sắc: dòng nguồn y 1380–1450 và các đoạn `foot` không bị làm mờ.
"""
import argparse, json, math, subprocess, sys, os
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flight import cam_sampler

ap = argparse.ArgumentParser()
ap.add_argument("flight"); ap.add_argument("raw"); ap.add_argument("out")
ap.add_argument("--shutter", type=float, default=180); ap.add_argument("--min", type=float, default=2.0); ap.add_argument("--samples", type=int, default=16); ap.add_argument("--offset", type=float, default=0, help="giây bắt đầu nếu raw là đoạn --start")
a = ap.parse_args()
F = json.load(open(a.flight)); at = cam_sampler(F["cam"]); fps = F.get("fps", 30)
W, H = 1080, 1920
foot = [(f["t"], f["t"] + f["d"]) for f in F.get("foot", [])]
keep = [(1380, 1450)]                                    # dải dòng nguồn (UI màn hình) giữ sắc

def vel(t):
    p, q = at(t - 0.5 / fps), at(t + 0.5 / fps); s = 2 ** ((p[2] + q[2]) / 2 - 8)
    br = math.radians((p[4] + q[4]) / 2); mx, my = (q[0] - p[0]) * s, (q[1] - p[1]) * s
    vx = mx * math.cos(br) - my * math.sin(br); vy = (mx * math.sin(br) + my * math.cos(br)) * (1 + (p[3] + q[3]) / 2 / 90)
    rad = (abs(q[2] - p[2]) * math.log(2) * 540 + abs(q[4] - p[4]) * math.pi / 180 * 540) * 0.5
    return -vx, -vy, rad                                  # cảnh trôi NGƯỢC chiều camera

def kernel(dx, dy, n):
    L = math.hypot(dx, dy); size = int(math.ceil(L)) | 1; size = max(size, 3)
    k = np.zeros((size, size), np.float32); c = (size - 1) / 2
    for i in range(n):                                    # n mẫu dọc vệt, nội suy song tuyến (khử răng cưa)
        f = i / (n - 1) - 0.5; x, y = c + dx * f, c + dy * f; x0, y0 = int(x), int(y); fx, fy = x - x0, y - y0
        for (xx, yy, w) in ((x0, y0, (1 - fx) * (1 - fy)), (x0 + 1, y0, fx * (1 - fy)), (x0, y0 + 1, (1 - fx) * fy), (x0 + 1, y0 + 1, fx * fy)):
            if 0 <= xx < size and 0 <= yy < size: k[yy, xx] += w
    return k / k.sum()

dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.raw, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-i", a.raw,
                        "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", a.out], stdin=subprocess.PIPE)
n = 0; blurred = 0; Lmax = 0
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    t = a.offset + n / fps; img = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    vx, vy, rad = vel(t); sh = a.shutter / 360
    dx, dy = vx * sh, vy * sh; L = math.hypot(dx, dy) + rad * sh
    if L >= a.min and not any(f0 + .1 <= t <= f1 - .1 for f0, f1 in foot):
        if math.hypot(dx, dy) < 1e-3: dx = L
        else: dx, dy = dx * L / math.hypot(dx, dy), dy * L / math.hypot(dx, dy)
        out = cv2.filter2D(img, -1, kernel(dx, dy, max(a.samples, int(L) + 1)), borderType=cv2.BORDER_REPLICATE)
        for y0, y1 in keep: out[y0:y1] = img[y0:y1]
        img = out; blurred += 1; Lmax = max(Lmax, L)
    enc.stdin.write(np.ascontiguousarray(img).tobytes()); n += 1
enc.stdin.close(); enc.wait(); dec.wait()
print(f"{n} khung · làm mờ {blurred} khung ({blurred / max(n,1) * 100:.0f}%) · vệt dài nhất {Lmax:.1f} px · shutter {a.shutter}°")
