#!/usr/bin/env python3
"""
Phân tích video mẫu (bất động sản / kinh tế) để rút ra "ngữ pháp" camera + parallax.

Đo cho mỗi video:
  - điểm cắt cảnh (cut) và kiểu chuyển (cắt cứng / hoà tan)
  - chuyển động camera theo từng cảnh: pan, tilt, zoom (dolly), xoay; tốc độ chuẩn hoá theo khung
  - độ liên tục: % thời gian camera đang chuyển động, số lần "dừng chết", cắt khi đang chuyển động
  - parallax: các điểm ở độ sâu khác nhau chạy với vận tốc khác nhau (độ tách lớp)
  - bảng màu chủ đạo, contact sheet từng cảnh, đồ thị tốc độ camera

Cách dùng:
  python analyze_refs.py "C:\\Users\\Admin\\Downloads\\video mau" --out phan-tich
  python analyze_refs.py video1.mp4 video2.mp4 --out phan-tich --width 480 --step 1

Yêu cầu: pip install opencv-python-headless numpy
Kết quả: <out>/SUMMARY.md, <out>/STYLE_DRAFT.md, <out>/summary.json và một thư mục cho từng video
(report.json, motion.png, sheet-*.jpg). Mọi con số là ĐO ĐƯỢC; phần nhận xét bằng mắt ghi riêng.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import sys
import tempfile
from pathlib import Path

try:
    import cv2
    import numpy as np
except ImportError:  # pragma: no cover
    sys.exit("Thiếu thư viện: pip install opencv-python-headless numpy")

VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v", ".mpg", ".mpeg", ".wmv", ".flv"}

# Ngưỡng (chuẩn hoá theo khung hình, mỗi giây)
MOVE_PAN = 0.6      # % chiều rộng khung / s  -> coi là đang pan
MOVE_ZOOM = 0.35    # % tỉ lệ / s             -> coi là đang zoom/dolly
MOVE_ROT = 0.15     # độ / s
STOP_MIN_SEC = 0.4  # đứng yên lâu hơn mức này = 1 lần "dừng"
PARALLAX_ON = 0.18  # chỉ số tách lớp >= ngưỡng -> có parallax rõ


# ----------------------------------------------------------------- I/O helpers
def imwrite(path: Path, img) -> None:
    """cv2.imwrite hỏng với đường dẫn có dấu trên Windows -> dùng imencode."""
    params = [cv2.IMWRITE_JPEG_QUALITY, 88] if path.suffix.lower() in (".jpg", ".jpeg") else []
    ok, buf = cv2.imencode(path.suffix, img, params)
    if ok:
        path.write_bytes(buf.tobytes())


def open_video(path: Path):
    cap = cv2.VideoCapture(str(path))
    if cap.isOpened():
        return cap, None
    # Đường dẫn có ký tự Unicode (vd. "video mẫu") đôi khi không mở được trên Windows
    tmpdir = tempfile.mkdtemp(prefix="refvid_")
    tmp = Path(tmpdir) / ("v" + path.suffix.lower())
    shutil.copyfile(path, tmp)
    cap = cv2.VideoCapture(str(tmp))
    return cap, tmpdir


def collect_inputs(items: list[str]) -> list[Path]:
    out: list[Path] = []
    for it in items:
        p = Path(it).expanduser()
        if p.is_dir():
            out += sorted(q for q in p.rglob("*") if q.suffix.lower() in VIDEO_EXT)
        elif p.is_file():
            out.append(p)
        else:
            print(f"[bỏ qua] không tìm thấy: {it}", file=sys.stderr)
    return out


def safe_name(p: Path) -> str:
    keep = "".join(c if c.isalnum() or c in "-_" else "-" for c in p.stem)
    return keep.strip("-")[:60] or "video"


# ----------------------------------------------------------------- per-frame motion
def hsv_hist(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h = cv2.calcHist([hsv], [0, 1], None, [32, 32], [0, 180, 0, 256])
    cv2.normalize(h, h)
    return h


def frame_motion(prev_gray, gray):
    """Ước lượng chuyển động toàn cục + chỉ số parallax giữa 2 khung."""
    h, w = gray.shape
    pts = cv2.goodFeaturesToTrack(prev_gray, maxCorners=500, qualityLevel=0.01, minDistance=7, blockSize=7)
    res = dict(tx=0.0, ty=0.0, scale=1.0, rot=0.0, parallax=None, spread=None, n=0, valid=False)
    if pts is None or len(pts) < 25:
        return res
    nxt, st, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, pts, None, winSize=(21, 21), maxLevel=3)
    if nxt is None:
        return res
    st = st.reshape(-1).astype(bool)
    p0 = pts.reshape(-1, 2)[st]
    p1 = nxt.reshape(-1, 2)[st]
    if len(p0) < 25:
        return res
    # loại các điểm trượt đi quá xa (lỗi tracking)
    flow = p1 - p0
    mag = np.linalg.norm(flow, axis=1)
    keep = mag < 0.25 * w
    p0, p1, flow, mag = p0[keep], p1[keep], flow[keep], mag[keep]
    if len(p0) < 25:
        return res
    M, inl = cv2.estimateAffinePartial2D(p0, p1, method=cv2.RANSAC, ransacReprojThreshold=1.5, maxIters=2000)
    if M is None:
        return res
    a, b = M[0, 0], M[1, 0]
    scale = math.hypot(a, b)
    rot = math.degrees(math.atan2(b, a))
    # chuyển động tịnh tiến quy về tâm khung
    cx, cy = w / 2, h / 2
    center_new = M @ np.array([cx, cy, 1.0])
    tx, ty = center_new[0] - cx, center_new[1] - cy

    pred = (np.hstack([p0, np.ones((len(p0), 1))]) @ M.T)
    resid = np.linalg.norm(p1 - pred, axis=1)
    med_mag = float(np.median(mag))
    parallax = spread = None
    if med_mag > 0.35:  # chỉ đo parallax khi khung thật sự chuyển động
        parallax = float(np.median(resid) / (med_mag + 1e-6))
        # độ tách lớp: dải vận tốc dọc hướng chuyển động chính (p90-p10)/median
        d = np.array([tx, ty])
        if np.linalg.norm(d) > 0.3:
            d = d / np.linalg.norm(d)
            proj = flow @ d
            med = np.median(proj)
            if abs(med) > 0.3:
                spread = float((np.percentile(proj, 90) - np.percentile(proj, 10)) / abs(med))
    res.update(tx=float(tx), ty=float(ty), scale=float(scale), rot=float(rot),
               parallax=parallax, spread=spread, n=int(len(p0)), valid=True)
    return res


# ----------------------------------------------------------------- analysis
def analyze_video(path: Path, out_dir: Path, width: int, step: int) -> dict:
    cap, tmpdir = open_video(path)
    if not cap.isOpened():
        return {"file": str(path), "error": "không mở được video"}
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    nframes = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    W0 = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H0 = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    sw = width
    sh = int(round(H0 * sw / max(W0, 1)))
    dt = step / fps

    times, motions, hist_corr, mad, thumbs = [], [], [], [], []
    palette_samples = []
    prev_gray = prev_hist = None
    idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % step:
            idx += 1
            continue
        small = cv2.resize(frame, (sw, sh), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        hist = hsv_hist(small)
        t = idx / fps
        times.append(t)
        thumbs.append(cv2.resize(small, (320, int(320 * sh / sw))))
        if prev_gray is None:
            motions.append(dict(tx=0, ty=0, scale=1, rot=0, parallax=None, spread=None, n=0, valid=False))
            hist_corr.append(1.0)
            mad.append(0.0)
        else:
            hist_corr.append(float(cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CORREL)))
            mad.append(float(np.mean(cv2.absdiff(prev_gray, gray))))
            motions.append(frame_motion(prev_gray, gray))
        if len(times) % max(1, int(fps // step)) == 0:  # ~1 mẫu màu / giây
            palette_samples.append(cv2.resize(small, (64, int(64 * sh / sw))).reshape(-1, 3))
        prev_gray, prev_hist = gray, hist
        idx += 1
    cap.release()
    if tmpdir:
        shutil.rmtree(tmpdir, ignore_errors=True)
    n = len(times)
    if n < 3:
        return {"file": str(path), "error": "video quá ngắn"}
    duration = (nframes / fps) if nframes else times[-1] + dt

    # ---- cuts: histogram tụt mạnh HOẶC sai khác điểm ảnh vượt xa trung vị, và tracking mất
    mad_arr = np.array(mad)
    base = float(np.median(mad_arr[1:])) + 1e-3
    cut_idx = []
    for i in range(1, n):
        lost = not motions[i]["valid"] or motions[i]["n"] < 40
        hard = hist_corr[i] < 0.55 or (mad_arr[i] > 6 * base and mad_arr[i] > 12)
        soft = hist_corr[i] < 0.8 and mad_arr[i] > 4 * base and lost
        if (hard or soft) and (not cut_idx or i - cut_idx[-1] > max(2, int(0.25 * fps / step))):
            cut_idx.append(i)
    # nhận diện hoà tan: màu sắc (histogram) đổi dần trong các mẫu trước cut.
    # Dùng histogram chứ không dùng sai khác điểm ảnh, vì camera đang lướt cũng tạo sai khác lớn.
    hc = np.array(hist_corr)
    cuts = []
    for i in cut_idx:
        win = hc[max(1, i - 5):i]
        gradual = len(win) >= 4 and np.sum(win < 0.93) >= 3
        cuts.append({"t": round(times[i], 3), "kind": "hoà tan/chuyển dần" if gradual else "cắt cứng"})
    # các khung tại cut không đo chuyển động (là bước nhảy hình)
    for i in cut_idx:
        motions[i] = dict(tx=0, ty=0, scale=1, rot=0, parallax=None, spread=None, n=0, valid=False)

    # ---- chuỗi tốc độ chuẩn hoá
    pan = np.array([math.hypot(m["tx"], m["ty"]) / sw * 100 / dt for m in motions])        # %W/s
    vx = np.array([m["tx"] / sw * 100 / dt for m in motions])
    vy = np.array([m["ty"] / sw * 100 / dt for m in motions])
    zoom = np.array([(m["scale"] - 1) * 100 / dt for m in motions])                        # %/s
    rot = np.array([m["rot"] / dt for m in motions])                                       # deg/s
    valid = np.array([m["valid"] for m in motions])
    # làm mượt nhẹ (cửa sổ ~0.2 s) để bỏ nhiễu tracking
    k = max(1, int(round(0.2 / dt)))
    def smooth(a):
        if k <= 1:
            return a
        return np.convolve(a, np.ones(k) / k, mode="same")
    pan_s, zoom_s, rot_s = smooth(pan), smooth(np.abs(zoom)), smooth(np.abs(rot))
    moving = (pan_s > MOVE_PAN) | (zoom_s > MOVE_ZOOM) | (rot_s > MOVE_ROT)

    # ---- theo từng cảnh
    bounds = [0] + cut_idx + [n]
    shots = []
    for si in range(len(bounds) - 1):
        a, b = bounds[si], bounds[si + 1]
        t0 = times[a]
        t1 = times[b] if b < n else duration
        seg = slice(a + 1, b)  # bỏ khung đầu cảnh
        sv = valid[seg]
        if sv.sum() < 2:
            shots.append(dict(i=si, start=round(t0, 3), end=round(t1, 3), dur=round(t1 - t0, 3), label="quá ngắn"))
            continue
        mv = moving[seg][sv]
        mvx, mvy = float(np.median(vx[seg][sv])), float(np.median(vy[seg][sv]))
        mz, mr = float(np.median(zoom[seg][sv])), float(np.median(rot[seg][sv]))
        par = [m["parallax"] for m in motions[a + 1:b] if m["parallax"] is not None]
        spr = [m["spread"] for m in motions[a + 1:b] if m["spread"] is not None]
        # dừng: đoạn liên tiếp không chuyển động >= STOP_MIN_SEC
        stops, run = 0, 0
        for v in mv:
            run = run + 1 if not v else 0
            if run == int(math.ceil(STOP_MIN_SEC / dt)):
                stops += 1
        sp = pan_s[seg][sv]
        raw = pan[seg][sv]  # chưa làm mượt: tránh rò tốc độ của cảnh bên cạnh qua điểm cắt
        nhead = max(1, int(0.15 / dt))
        head = float(np.mean(raw[:nhead])) if len(raw) else 0.0
        tail = float(np.mean(raw[-nhead:])) if len(raw) else 0.0
        med_speed = float(np.median(sp)) if len(sp) else 0.0
        parallax = float(np.median(par)) if par else None
        spread = float(np.median(spr)) if spr else None
        labels = []
        if abs(mz) > MOVE_ZOOM:
            labels.append("push-in/dolly vào" if mz > 0 else "pull-out/lùi ra")
        if abs(mvx) > MOVE_PAN:
            labels.append("pan/truck " + ("trái→phải" if mvx < 0 else "phải→trái"))  # khung trôi ngược hướng camera
        if abs(mvy) > MOVE_PAN:
            labels.append("tilt/pedestal " + ("lên" if mvy > 0 else "xuống"))
        if abs(mr) > MOVE_ROT:
            labels.append("xoay/roll")
        if not labels:
            labels.append("tĩnh" if mv.mean() < 0.3 else "trôi nhẹ")
        if (parallax or 0) >= PARALLAX_ON or (spread or 0) >= 0.6:
            labels.append("PARALLAX")
        shots.append(dict(
            i=si, start=round(t0, 3), end=round(t1, 3), dur=round(t1 - t0, 3),
            label=", ".join(labels),
            moving_frac=round(float(mv.mean()), 3), stops=stops,
            pan_pct_w_s=round(med_speed, 2), vx=round(mvx, 2), vy=round(mvy, 2),
            zoom_pct_s=round(mz, 3), rot_deg_s=round(mr, 3),
            parallax=None if parallax is None else round(parallax, 3),
            layer_spread=None if spread is None else round(spread, 3),
            enters_moving=bool(head > 0.5 * max(med_speed, MOVE_PAN)),
            exits_moving=bool(tail > 0.5 * max(med_speed, MOVE_PAN)),
            dir_out=[round(float(np.mean(vx[seg][sv][-nhead:])), 2), round(float(np.mean(vy[seg][sv][-nhead:])), 2)],
            dir_in=[round(float(np.mean(vx[seg][sv][:nhead])), 2), round(float(np.mean(vy[seg][sv][:nhead])), 2)],
        ))

    # match-move tại cut: hướng ra của cảnh trước ~ hướng vào cảnh sau
    match = []
    for s0, s1 in zip(shots, shots[1:]):
        if "dir_out" not in s0 or "dir_in" not in s1:
            continue
        a_, b_ = np.array(s0["dir_out"]), np.array(s1["dir_in"])
        if np.linalg.norm(a_) > MOVE_PAN and np.linalg.norm(b_) > MOVE_PAN:
            cos = float(a_ @ b_ / (np.linalg.norm(a_) * np.linalg.norm(b_)))
            match.append(cos)

    # ---- bảng màu (k-means 6 màu)
    palette = []
    if palette_samples:
        data = np.vstack(palette_samples).astype(np.float32)
        if len(data) > 60000:
            data = data[np.random.default_rng(1).choice(len(data), 60000, replace=False)]
        crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.5)
        _, lab, cen = cv2.kmeans(data, 6, None, crit, 3, cv2.KMEANS_PP_CENTERS)
        counts = np.bincount(lab.reshape(-1), minlength=6)
        for ci in np.argsort(-counts):
            bgr = cen[ci]
            palette.append({"hex": "#%02x%02x%02x" % (int(bgr[2]), int(bgr[1]), int(bgr[0])),
                            "share": round(float(counts[ci] / counts.sum()), 3)})

    # ---- tổng hợp
    vm = valid & ~np.isin(np.arange(n), cut_idx)
    durs = [s["dur"] for s in shots]
    pars = [s["parallax"] for s in shots if s.get("parallax") is not None]
    summary = dict(
        file=str(path), fps=round(fps, 3), size=[W0, H0], duration=round(duration, 3),
        shots=len(shots), cuts=cuts,
        avg_shot_sec=round(float(np.mean(durs)), 2), median_shot_sec=round(float(np.median(durs)), 2),
        continuity_moving_frac=round(float(moving[vm].mean()) if vm.any() else 0.0, 3),
        stops_total=int(sum(s.get("stops", 0) for s in shots)),
        cuts_on_motion_frac=round(float(np.mean([s.get("exits_moving", False) for s in shots[:-1]])) if len(shots) > 1 else None, 3)
        if len(shots) > 1 else None,
        match_move_cuts_frac=round(float(np.mean([c > 0.7 for c in match])), 3) if match else None,
        parallax_shots_frac=round(float(np.mean([("PARALLAX" in s.get("label", "")) for s in shots])), 3),
        parallax_median=round(float(np.median(pars)), 3) if pars else None,
        pan_speed_median_pct_w_s=round(float(np.median(pan_s[vm & moving])) if (vm & moving).any() else 0.0, 2),
        pan_speed_p90_pct_w_s=round(float(np.percentile(pan_s[vm & moving], 90)) if (vm & moving).any() else 0.0, 2),
        zoom_speed_median_pct_s=round(float(np.median(zoom_s[vm & moving])) if (vm & moving).any() else 0.0, 3),
        palette=palette,
        shot_list=shots,
    )

    # ---- hình ảnh: đồ thị chuyển động + contact sheets
    vdir = out_dir
    vdir.mkdir(parents=True, exist_ok=True)
    draw_motion_plot(vdir / "motion.png", times, pan_s, zoom_s, moving, [times[i] for i in cut_idx], duration)
    draw_sheets(vdir, thumbs, times, shots, bounds)
    (vdir / "report.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def draw_motion_plot(path, times, pan_s, zoom_s, moving, cut_t, duration):
    Wp, Hp, pad = 1600, 420, 50
    img = np.full((Hp, Wp, 3), 24, np.uint8)
    ymax = max(5.0, float(np.percentile(pan_s, 98)) * 1.2, float(np.percentile(zoom_s, 98)) * 1.2)
    X = lambda t: int(pad + (Wp - 2 * pad) * t / max(duration, 1e-6))
    Y = lambda v: int(Hp - pad - (Hp - 2 * pad) * min(v, ymax) / ymax)
    for i, t in enumerate(times):  # nền xanh = đang chuyển động
        if moving[i]:
            cv2.line(img, (X(t), pad), (X(t), Hp - pad), (40, 60, 40), 2)
    for t in cut_t:
        cv2.line(img, (X(t), pad), (X(t), Hp - pad), (60, 60, 200), 2)
    for arr, col in ((pan_s, (80, 200, 255)), (zoom_s, (255, 160, 90))):
        pts = np.array([[X(t), Y(v)] for t, v in zip(times, arr)], np.int32)
        cv2.polylines(img, [pts], False, col, 2, cv2.LINE_AA)
    cv2.putText(img, "pan %%W/s (vang)  zoom %%/s (xanh)  nen xanh = dang chuyen dong  do = cut   max=%.1f" % ymax,
                (pad, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (230, 230, 230), 1, cv2.LINE_AA)
    for s in range(0, int(duration) + 1, max(1, int(duration // 20) or 1)):
        cv2.putText(img, f"{s}s", (X(s) - 10, Hp - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (160, 160, 160), 1)
    imwrite(path, img)


def draw_sheets(vdir, thumbs, times, shots, bounds, per_sheet=8):
    th, tw = thumbs[0].shape[:2]
    rows = []
    for si in range(len(bounds) - 1):
        a, b = bounds[si], max(bounds[si] + 1, bounds[si + 1] - 1)
        picks = [a, (a + b) // 2, b]
        row = np.hstack([thumbs[min(p, len(thumbs) - 1)] for p in picks])
        bar = np.full((34, row.shape[1], 3), 16, np.uint8)
        s = shots[si]
        txt = f"#{si} {s['start']:.2f}-{s['end']:.2f}s  {ascii_label(s.get('label', ''))}"
        if s.get("parallax") is not None:
            txt += f"  par={s['parallax']}"
        if "pan_pct_w_s" in s:
            txt += f"  pan={s['pan_pct_w_s']}%W/s zoom={s['zoom_pct_s']}%/s"
        cv2.putText(bar, txt[:120], (8, 23), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (235, 235, 235), 1, cv2.LINE_AA)
        rows.append(np.vstack([bar, row]))
    for k in range(0, len(rows), per_sheet):
        imwrite(vdir / f"sheet-{k // per_sheet + 1:02d}.jpg", np.vstack(rows[k:k + per_sheet]))


def ascii_label(s: str) -> str:
    table = {"đ": "d", "Đ": "D"}
    import unicodedata
    s = "".join(table.get(c, c) for c in s)
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


# ----------------------------------------------------------------- reports
def write_reports(out: Path, results: list[dict]) -> None:
    ok = [r for r in results if "error" not in r]
    (out / "summary.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    def med(key):
        vals = [r[key] for r in ok if r.get(key) is not None]
        return round(float(np.median(vals)), 3) if vals else None

    L = ["# Tổng hợp phân tích video mẫu", "",
         "Mọi số liệu dưới đây là ĐO bằng optical flow; nhãn cảnh là phân loại tự động, hãy xác nhận bằng mắt trên sheet-*.jpg.", "",
         "| Video | Dài (s) | Cảnh | TB cảnh (s) | % thời gian camera chạy | Số lần dừng | Cắt khi đang chạy | Match-move | Cảnh có parallax | Pan trung vị %W/s | Zoom trung vị %/s |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        if "error" in r:
            L.append(f"| {Path(r['file']).name} | lỗi: {r['error']} |||||||||| ")
            continue
        L.append(f"| {Path(r['file']).name} | {r['duration']} | {r['shots']} | {r['avg_shot_sec']} | "
                 f"{pct(r['continuity_moving_frac'])} | {r['stops_total']} | {pct(r['cuts_on_motion_frac'])} | "
                 f"{pct(r['match_move_cuts_frac'])} | {pct(r['parallax_shots_frac'])} | "
                 f"{r['pan_speed_median_pct_w_s']} | {r['zoom_speed_median_pct_s']} |")
    L += ["", "## Danh sách cảnh", ""]
    for r in ok:
        L.append(f"### {Path(r['file']).name}")
        L.append("")
        L.append("| # | Bắt đầu | Dài | Chuyển động | %chạy | Dừng | Parallax | Tách lớp | Vào/ra khi đang chạy |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for s in r["shot_list"]:
            L.append(f"| {s['i']} | {s['start']} | {s['dur']} | {s.get('label','')} | {pct(s.get('moving_frac'))} | "
                     f"{s.get('stops','')} | {s.get('parallax','')} | {s.get('layer_spread','')} | "
                     f"{'có' if s.get('enters_moving') else 'không'}/{'có' if s.get('exits_moving') else 'không'} |")
        L.append("")
        L.append("Chuyển cảnh: " + (", ".join(f"{c['t']}s {c['kind']}" for c in r["cuts"]) or "không có cắt — một cú máy liền"))
        L.append("Bảng màu: " + ", ".join(f"{p['hex']} ({pct(p['share'])})" for p in r["palette"]))
        L.append("")
    (out / "SUMMARY.md").write_text("\n".join(L), encoding="utf-8")

    pals = [p["hex"] for r in ok for p in r["palette"][:3]]
    S = ["# STYLE_DRAFT — nháp ngữ pháp hình ảnh (điền tiếp bằng mắt)", "",
         "Các dòng [ĐO] lấy từ analyze_refs.py. Các dòng [NHÌN] phải do người/agent điền sau khi xem sheet-*.jpg và video.", "",
         "## Camera",
         f"- [ĐO] % thời gian camera chuyển động (trung vị các video): {pct(med('continuity_moving_frac'))}  → mục tiêu khi dựng: ≥ con số này",
         f"- [ĐO] Độ dài cảnh trung bình: {med('avg_shot_sec')} s (trung vị {med('median_shot_sec')} s)",
         f"- [ĐO] Tốc độ pan trung vị: {med('pan_speed_median_pct_w_s')} %W/s; p90: {med('pan_speed_p90_pct_w_s')} %W/s",
         f"- [ĐO] Tốc độ zoom/dolly trung vị: {med('zoom_speed_median_pct_s')} %/s",
         f"- [ĐO] Tỉ lệ cắt khi camera đang chạy: {pct(med('cuts_on_motion_frac'))}; cắt match-move cùng hướng: {pct(med('match_move_cuts_frac'))}",
         f"- [ĐO] Tỉ lệ cảnh có parallax: {pct(med('parallax_shots_frac'))}; chỉ số parallax trung vị: {med('parallax_median')}",
         "- [NHÌN] Kiểu chuyển động chủ đạo (dolly vào toà nhà? bay ngang skyline? orbit quanh mô hình?):",
         "- [NHÌN] Số lớp độ sâu thấy được (trời / skyline xa / toà nhà giữa / tiền cảnh / chữ):",
         "- [NHÌN] Chuyển cảnh: tiền cảnh quét qua (foreground wipe)? zoom xuyên vật thể? whip?",
         "", "## Hình ảnh",
         f"- [ĐO] Màu chủ đạo: {', '.join(dict.fromkeys(pals))}",
         "- [NHÌN] Chất liệu: ảnh thật tách lớp / 3D / vector phẳng / bản đồ vệ tinh:",
         "- [NHÌN] Font tiêu đề, cỡ (% chiều cao khung), độ đậm, màu nhấn cho số tăng/giảm:",
         "- [NHÌN] Nhãn số liệu: gắn vào thế giới (world-locked) hay cố định màn hình (HUD)?",
         "- [NHÌN] Biểu đồ: loại, cách vẽ vào, camera có bay dọc đường biểu đồ không:",
         "", "## Nhịp & âm thanh",
         "- [NHÌN] Có lời dẫn? tốc độ (từ/giây). Nhạc nền kiểu gì, có SFX whoosh khi camera lướt?",
         "- [NHÌN] Hook 3 giây đầu là gì:",
         ""]
    (out / "STYLE_DRAFT.md").write_text("\n".join(S), encoding="utf-8")


def pct(v):
    return "—" if v is None else f"{round(100 * v)}%"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="thư mục hoặc file video")
    ap.add_argument("--out", default="phan-tich-video-mau", help="thư mục kết quả")
    ap.add_argument("--width", type=int, default=480, help="chiều rộng khi phân tích (px)")
    ap.add_argument("--step", type=int, default=1, help="lấy 1 khung mỗi N khung (2 = nhanh gấp đôi)")
    args = ap.parse_args()

    vids = collect_inputs(args.inputs)
    if not vids:
        sys.exit("Không có video nào.")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    results = []
    used = set()
    for v in vids:
        name = safe_name(v)
        while name in used:
            name += "_"
        used.add(name)
        print(f"→ {v.name}", flush=True)
        try:
            r = analyze_video(v, out / name, args.width, max(1, args.step))
        except Exception as e:  # một video lỗi không làm hỏng cả lô
            r = {"file": str(v), "error": repr(e)}
        if "error" in r:
            print(f"   lỗi: {r['error']}")
        else:
            print(f"   {r['shots']} cảnh, camera chạy {pct(r['continuity_moving_frac'])} thời gian, "
                  f"parallax ở {pct(r['parallax_shots_frac'])} cảnh")
        results.append(r)
    write_reports(out, results)
    print(f"\nXong: {out / 'SUMMARY.md'}  |  {out / 'STYLE_DRAFT.md'}")


if __name__ == "__main__":
    main()
