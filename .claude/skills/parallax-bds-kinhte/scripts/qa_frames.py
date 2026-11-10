#!/usr/bin/env python3
"""Kiểm lỗi render của video trước khi xuất (mục "kiểm soát lỗi render").

  python qa_frames.py video.mp4 [--out qa] [--fps 2]

Kiểm:
  1. DEAD_EDGE  — vùng chết dính mép/góc (đen, hoặc một màu phẳng như ảnh vệ tinh/3D chưa tải) > 5% diện tích khung.
  2. HAZE       — mảng trắng mờ (mây, sương, tile lỗi) phẳng, ít chi tiết > 8% diện tích.
  3. DARK_RUN   — > 5 khung liên tiếp tối (luma trung bình < 22) ngoài chủ đích.
  4. BLUR_RUN   — > 6 khung liên tiếp nhoè (độ nét < 18% trung vị của cả video): chuyển cảnh dài quá hoặc nguồn mờ.
  5. STATIC     — một khung hình gần như đứng yên > 6 s (vi phạm nhịp).
Kết quả: <out>/QA.md + ảnh khung lỗi. Thoát mã 1 nếu có lỗi -> render lại đoạn đó.
"""
import argparse, os, sys
import cv2, numpy as np

def dead_mask(gray, hsv, block=16):
    h, w = gray.shape
    hb, wb = h // block, w // block
    g = gray[: hb * block, : wb * block].reshape(hb, block, wb, block).astype(np.float32)
    std = g.std(axis=(1, 3)); mean = g.mean(axis=(1, 3))
    sat = hsv[: hb * block, : wb * block, 1].reshape(hb, block, wb, block).astype(np.float32).mean(axis=(1, 3))
    # vùng chết = gần đen, hoặc phẳng tuyệt đối VÀ (tối hoặc mất màu): tile chưa tải, lưới 3D thủng, nền đặc.
    # Mặt nước/bầu trời thật có màu (bão hoà > 14) nên không bị tính.
    flat = (std < 1.2) & ((mean < 70) | (sat < 14))
    black = mean < 12
    return flat | black, mean, std

def edge_connected(mask):
    m = mask.astype(np.uint8)
    n, lab = cv2.connectedComponents(m, connectivity=4)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    border.discard(0)
    return np.isin(lab, list(border)) if border else np.zeros_like(mask)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--out", default="qa"); ap.add_argument("--fps", type=float, default=2.0)
    ap.add_argument("--dead", type=float, default=0.05); ap.add_argument("--haze", type=float, default=0.08)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    cap = cv2.VideoCapture(a.video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    step = max(1, int(round(fps / a.fps)))
    issues = []
    lum, sharp, times, prev, still_since = [], [], [], None, 0.0
    i = 0
    while True:
        ok, fr = cap.read()
        if not ok: break
        t = i / fps
        small = cv2.resize(fr, (270, 480), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        lum.append(float(gray.mean())); times.append(t)
        sharp.append(float(cv2.Laplacian(gray, cv2.CV_64F).var()))
        if prev is not None:
            if float(np.mean(cv2.absdiff(gray, prev))) < 0.6:
                if t - still_since > 6.0:
                    issues.append(("STATIC", t, f"đứng yên từ {still_since:.1f}s")); still_since = t
            else:
                still_since = t
        else:
            still_since = t
        prev = gray
        if i % step == 0:
            hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
            m, mean, std = dead_mask(gray, hsv, block=8)
            frac = edge_connected(m).mean()
            if frac > a.dead:
                issues.append(("DEAD_EDGE", t, f"{frac*100:.1f}% khung là vùng chết dính mép"))
                cv2.imwrite(f"{a.out}/dead_{t:07.2f}.jpg", small)
            s = hsv[..., 1].astype(np.float32); v = hsv[..., 2].astype(np.float32)
            hz = ((v > 185) & (s < 40)).astype(np.uint8)
            hz = cv2.erode(hz, np.ones((5, 5), np.uint8))  # bỏ chữ trắng mảnh, chỉ giữ mảng lớn
            lap = np.abs(cv2.Laplacian(gray, cv2.CV_32F))
            hz = hz & (cv2.blur(lap, (9, 9)) < 6)
            if hz.mean() > a.haze:
                issues.append(("HAZE", t, f"{hz.mean()*100:.1f}% khung là mảng trắng mờ"))
                cv2.imwrite(f"{a.out}/haze_{t:07.2f}.jpg", small)
        i += 1
    lum = np.array(lum); sharp = np.array(sharp)
    med = np.median(sharp)
    def runs(flag, minlen, kind, note):
        k = 0
        for j, f in enumerate(flag):
            k = k + 1 if f else 0
            if k == minlen + 1:
                issues.append((kind, times[j - minlen], note))
    runs(lum < 22, 5, "DARK_RUN", "> 5 khung tối liên tiếp")
    runs(sharp < 0.18 * med, 6, "BLUR_RUN", "> 6 khung nhoè liên tiếp")
    issues.sort(key=lambda x: x[1])
    with open(f"{a.out}/QA.md", "w", encoding="utf-8") as f:
        f.write(f"# QA {os.path.basename(a.video)}\n\n{len(issues)} lỗi.\n\n| Loại | Thời điểm (s) | Chi tiết |\n|---|---|---|\n")
        for k, t, d in issues:
            f.write(f"| {k} | {t:.2f} | {d} |\n")
    for k, t, d in issues:
        print(f"{k:10s} {t:7.2f}s  {d}")
    print(f"{len(issues)} lỗi -> {a.out}/QA.md")
    sys.exit(1 if issues else 0)

if __name__ == "__main__":
    main()
