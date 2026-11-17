#!/usr/bin/env python3
"""fetch_inputs.py — tải và xử lý LẠI đúng các đầu vào của video mẫu "hạ tầng quanh One Era", kiểm từng file bằng hash điểm ảnh.

  python fetch_inputs.py <thư mục dựng>          # tạo <dựng>/assets/{maps,img,lib,fonts} theo inputs.json

Mỗi đầu vào in một dòng KHỚP / KHÁC. Hash điểm ảnh = sha256(str(shape) + byte RGB) — không phụ thuộc cách nén file của CDN.
KHÁC ở ảnh nguồn = báo/Esri đã đổi ảnh (video vẫn dựng được nhưng sẽ không giống hệt); KHÁC ở ảnh đã xử lý mà nguồn KHỚP
= khác phiên bản Pillow/OpenCV/libjpeg — chạy scripts/doctor.py.
"""
import hashlib, io, json, os, shutil, subprocess, sys, tarfile, urllib.request
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__)); SKILL = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.abspath(sys.argv[1]); M = json.load(open(os.path.join(HERE, "inputs.json")))
pix = lambda im: hashlib.sha256(str(np.asarray(im.convert("RGB")).shape).encode() + np.asarray(im.convert("RGB")).tobytes()).hexdigest()
bad = []
def report(name, ok, note=""):
    print(f"{'KHỚP' if ok else 'KHÁC'}  {name} {note}");
    if not ok: bad.append(name)
def get(url):
    for i in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "skill-repro/1.0"}), timeout=60).read()
        except Exception as e: err = e
    raise err
for d in ("maps", "img", "lib", "fonts"): os.makedirs(f"{OUT}/assets/{d}", exist_ok=True)
work = f"{OUT}/_work"; os.makedirs(work, exist_ok=True)
# ---- nền vệ tinh: sat_tiles.py -> (xoá mây) -> chỉnh màu -> làm mềm
for m in M["maps"]:
    n = m["name"]; raw = f"{work}/{n}.jpg"
    if not os.path.exists(raw):
        subprocess.run([sys.executable, f"{SKILL}/scripts/sat_tiles.py", n] + [str(x) for x in m["tiles"]] + ["img"], cwd=work, check=True, capture_output=True)
    src = raw
    if m.get("extra") and m["extra"].get("crop_w"):
        im = Image.open(raw); im.crop((0, 0, m["extra"]["crop_w"], im.height)).save(f"{work}/{n}_c.jpg", quality=m["extra"]["crop_q"]); src = f"{work}/{n}_c.jpg"
    if m.get("declouds"):
        shutil.copy(raw, f"{work}/{n}_d.jpg")
        subprocess.run([sys.executable, f"{SKILL}/scripts/sat_declouds.py", f"{work}/{n}_d.jpg", "--min-area", str(m["declouds"][0]), "--grow", str(m["declouds"][1])], check=True, capture_output=True)
        src = f"{work}/{n}_d_dc.jpg"
    g = m["grade"]; p = Image.open(src).convert("RGB")
    p = ImageEnhance.Color(p).enhance(g["color"]); p = ImageEnhance.Brightness(p).enhance(g["brightness"]); p = ImageEnhance.Contrast(p).enhance(g["contrast"])
    p.save(f"{work}/{n}_g1.jpg", quality=g["q1"])
    Image.open(f"{work}/{n}_g1.jpg").filter(ImageFilter.GaussianBlur(g["blur"])).save(f"{OUT}/{m['final']}", quality=g["q2"])
    report(m["final"], pix(Image.open(f"{OUT}/{m['final']}")) == m["final_pixel_sha256"])
# ---- ảnh báo / phối cảnh
for ph in M["photos"]:
    try: data = get(ph["url"])
    except Exception as e: report(ph["name"], False, f"(không tải được: {e} — thêm host vào mạng cho phép)"); continue
    im = Image.open(io.BytesIO(data)); ok_src = pix(im) == ph["source_pixel_sha256"]
    im.convert("RGB").save(f"{OUT}/{ph['final']}", quality=ph["quality"])
    ok = pix(Image.open(f"{OUT}/{ph['final']}")) == ph["final_pixel_sha256"]
    report(ph["final"], ok, "" if ok_src else "(ẢNH NGUỒN đã đổi trên báo)")
# ---- GSAP đúng phiên bản
g = M["lib"]["gsap"]; tgz = get(f"https://registry.npmjs.org/gsap/-/gsap-{g['npm'].split('@')[1]}.tgz")
with tarfile.open(fileobj=io.BytesIO(tgz)) as t: js = t.extractfile("package/" + g["file"]).read()
open(f"{OUT}/{g['dest']}", "wb").write(js); report(g["dest"], hashlib.sha256(js).hexdigest() == g["sha256"])
# ---- phông
shutil.copytree(f"{SKILL}/templates/kinh-te-dia-phuong/assets/fonts", f"{OUT}/assets/fonts", dirs_exist_ok=True); print("KHỚP  assets/fonts (kèm trong skill)")
print(f"\n{'TẤT CẢ ĐẦU VÀO KHỚP' if not bad else f'{len(bad)} đầu vào KHÁC: ' + ', '.join(bad)}")
sys.exit(1 if bad else 0)
