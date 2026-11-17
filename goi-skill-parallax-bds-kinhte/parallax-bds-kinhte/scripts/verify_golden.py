#!/usr/bin/env python3
"""verify_golden.py — so khung hình dựng trên máy này với khung chuẩn (golden) của video mẫu.

  python verify_golden.py make   <project> <golden_dir> --at 2,5.5,...   # (chỉ máy gốc) chụp khung chuẩn
  python verify_golden.py check  <project> <golden_dir> [--min-ssim 0.97] # máy khác: chụp cùng mốc rồi so

Chụp bằng `npx hyperframes@0.9.28 snapshot` (seek đúng thời điểm, cùng engine với render). So SSIM toàn khung (thang xám,
cửa sổ 7 px) + PSNR + tỉ lệ điểm ảnh lệch > 24 mức. Ghi report.md + ảnh so sánh cạnh nhau cho mốc không đạt.
Đạt khi mọi mốc SSIM ≥ min-ssim. Khác font hệ thống/Chromium thường cho SSIM 0,97–0,99 ở mốc nhiều chữ; < 0,95 là sai thật.
"""
import argparse, json, os, subprocess, sys, shutil
import numpy as np, cv2

def snap(project, times, out):
    if os.path.isdir(out): shutil.rmtree(out)
    r = subprocess.run(["npx", "-y", "hyperframes@0.9.28", "snapshot", "--no-end", "--at", ",".join(str(t) for t in times), "-o", out, "."],
                       cwd=project, capture_output=True, text=True)
    if r.returncode: print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit("snapshot lỗi")
    files = sorted(f for f in os.listdir(out) if f.startswith("frame-") and f.endswith(".png"))
    if len(files) != len(times): sys.exit(f"snapshot ra {len(files)} khung, cần {len(times)}")
    return [os.path.join(out, f) for f in files]

def ssim(a, b):
    a = a.astype(np.float64); b = b.astype(np.float64); C1, C2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    mu1, mu2 = cv2.GaussianBlur(a, (7, 7), 1.5), cv2.GaussianBlur(b, (7, 7), 1.5)
    s1 = cv2.GaussianBlur(a * a, (7, 7), 1.5) - mu1 ** 2; s2 = cv2.GaussianBlur(b * b, (7, 7), 1.5) - mu2 ** 2; s12 = cv2.GaussianBlur(a * b, (7, 7), 1.5) - mu1 * mu2
    return float((((2 * mu1 * mu2 + C1) * (2 * s12 + C2)) / ((mu1 ** 2 + mu2 ** 2 + C1) * (s1 + s2 + C2))).mean())

ap = argparse.ArgumentParser(); ap.add_argument("mode", choices=["make", "check"]); ap.add_argument("project"); ap.add_argument("golden")
ap.add_argument("--at"); ap.add_argument("--min-ssim", type=float, default=0.97); a = ap.parse_args()
project, golden = os.path.abspath(a.project), os.path.abspath(a.golden)
if a.mode == "make":
    times = [float(x) for x in a.at.split(",")]; os.makedirs(golden, exist_ok=True)
    frames = snap(project, times, os.path.join(golden, "_snap")); meta = []
    for t, f in zip(times, frames):
        name = f"g{t:07.2f}.jpg"; cv2.imwrite(os.path.join(golden, name), cv2.imread(f), [cv2.IMWRITE_JPEG_QUALITY, 92]); meta.append({"t": t, "file": name})
    shutil.rmtree(os.path.join(golden, "_snap")); json.dump({"frames": meta, "size": [1080, 1920]}, open(os.path.join(golden, "golden.json"), "w"), indent=1)
    print(f"{len(meta)} khung chuẩn -> {golden}"); sys.exit(0)
G = json.load(open(os.path.join(golden, "golden.json"))); times = [f["t"] for f in G["frames"]]
out = os.path.join(project, "out", "verify"); frames = snap(project, times, os.path.join(out, "snap"))
rows, fail = [], 0
for g, f in zip(G["frames"], frames):
    A = cv2.imread(os.path.join(golden, g["file"])); B = cv2.imread(f)
    if A.shape != B.shape: B = cv2.resize(B, (A.shape[1], A.shape[0]))
    s = ssim(cv2.cvtColor(A, cv2.COLOR_BGR2GRAY), cv2.cvtColor(B, cv2.COLOR_BGR2GRAY))
    psnr = cv2.PSNR(A, B); off = float((np.abs(A.astype(int) - B.astype(int)).max(2) > 24).mean() * 100)
    ok = s >= a.min_ssim; fail += not ok
    if not ok: cv2.imwrite(os.path.join(out, f"KHAC_{g['t']}.jpg"), np.hstack([A, B]), [cv2.IMWRITE_JPEG_QUALITY, 80])
    rows.append(f"| {g['t']:.2f} | {s:.4f} | {psnr:.1f} | {off:.2f}% | {'ĐẠT' if ok else 'KHÔNG ĐẠT'} |")
rep = ["# So với khung chuẩn", "", f"Ngưỡng SSIM ≥ {a.min_ssim}", "", "| t (s) | SSIM | PSNR (dB) | điểm ảnh lệch > 24 | Kết quả |", "|---|---|---|---|---|"] + rows
rep += ["", f"**{len(rows) - fail}/{len(rows)} mốc đạt.**" + ("" if not fail else " Mốc không đạt: xem ảnh KHAC_*.jpg (trái = chuẩn, phải = máy này).")]
open(os.path.join(out, "report.md"), "w").write("\n".join(rep)); print("\n".join(rep)); sys.exit(1 if fail else 0)
