#!/usr/bin/env python3
"""doctor.py — kiểm môi trường dựng có giống máy đã làm video mẫu không (phiên bản ghim trong requirements.txt)."""
import importlib, os, re, shutil, subprocess, sys
SK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
want = dict(l.split("==") for l in open(f"{SK}/requirements.txt") if "==" in l and not l.startswith("#"))
mod = {"numpy": "numpy", "pillow": "PIL", "opencv-python-headless": "cv2", "shapely": "shapely", "faster-whisper": "faster_whisper"}
bad = 0
def line(ok, name, have, need):
    global bad; bad += 0 if ok else 1; print(f"{'OK ' if ok else '!! '} {name:24} {have:14} (cần {need})")
for pkg, ver in want.items():
    ver = ver.strip()
    try: m = importlib.import_module(mod[pkg]); have = getattr(m, "__version__", "?")
    except Exception: have = "chưa cài"
    line(have == ver or (pkg == "opencv-python-headless" and have.startswith(ver.rsplit(".", 1)[0])), pkg, have, ver)
line(sys.version_info >= (3, 10), "python", sys.version.split()[0], ">= 3.10")
def cmd(c):
    try: return subprocess.run(c, capture_output=True, text=True, timeout=60).stdout
    except Exception: return ""
ff = re.search(r"ffmpeg version (\S+)", cmd(["ffmpeg", "-version"])); line(bool(ff), "ffmpeg", ff.group(1) if ff else "không có", "6.x")
nv = cmd(["node", "-v"]).strip(); line(nv.startswith("v2") and int(nv[1:3]) >= 18, "node", nv or "không có", ">= 18 (đã dùng v22)")
line(bool(shutil.which("npx")), "npx", "có" if shutil.which("npx") else "không có", "có")
print("\n" + ("Môi trường khớp." if not bad else f"{bad} mục lệch — pip install -r requirements.txt; khác phiên bản có thể làm khung hình lệch nhẹ (bước so khung chuẩn sẽ cho biết)."))
