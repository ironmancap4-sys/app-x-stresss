#!/usr/bin/env python3
"""editor.py — cửa sổ chỉnh tay số liệu / chữ của video phong cách C (flight.json), xem khung, render lại.

  python editor.py <project_dir> [--port 8765] [--duration 131.36]

Mở trình duyệt vào http://localhost:<port>. Mỗi dòng = một nhãn trên bản đồ (thời điểm, số lớn, đơn vị, chữ, chữ nhỏ) và dòng nguồn.
- Lưu: ghi flight.json (giữ bản .bak), sinh lại project bằng flight.py, chạy hyperframes check.
- Xem khung: chụp đúng thời điểm của nhãn (hyperframes snapshot) để kiểm tra trước khi render.
- Render: render_segments.sh → mb_post.py → mux âm thanh có limiter → out/final.mp4 (nút tải về khi xong).
Số đếm (count) tự cập nhật theo số mới nhập. Chỉnh xong lại mk_flight*.py thì flight.json bị ghi đè — sửa ở đây là bản cuối.
"""
import argparse, html, json, os, re, shutil, subprocess, sys, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

ap = argparse.ArgumentParser(); ap.add_argument("project"); ap.add_argument("--port", type=int, default=8765); ap.add_argument("--duration", type=float)
A = ap.parse_args(); P = os.path.abspath(A.project); SK = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FJ = os.path.join(P, "flight.json"); STATE = {"job": None, "log": "", "done": None}
E = lambda s: html.escape(str(s if s is not None else ""), quote=True)

def load(): return json.load(open(FJ, encoding="utf-8"))
def num(s):
    t = re.sub(r"[^\d,.]", "", s or "")
    if not re.search(r"\d", t): return None
    t = t.replace(".", "").replace(",", ".")
    try: return float(t)
    except ValueError: return None

def run(cmd, cwd=P):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=isinstance(cmd, str)); return r.returncode, r.stdout + r.stderr

def page(msg=""):
    F = load(); rows = []
    for i, l in enumerate(F["labels"]):
        if l.get("photo"): kind = "ảnh"
        elif "logo" in l: kind = "thẻ tổ chức"
        else: kind = "số" if l.get("count") or l.get("xl") else "nhãn"
        img = f'<img src="/snap/{i}.png?{int(time.time())}" loading="lazy">' if os.path.exists(f"{P}/out/editor/{i}.png") else ""
        rows.append(f"""<tr><td class=t>{l['t']:.1f}s<br><small>{kind}</small></td>
<td><input name="big_{i}" value="{E(l.get('big'))}" {'disabled' if l.get('photo') else ''}></td>
<td><input name="unit_{i}" value="{E(l.get('unit'))}" class=s {'disabled' if l.get('photo') else ''}></td>
<td><input name="text_{i}" value="{E(l.get('text'))}" class=w></td>
<td><input name="small_{i}" value="{E(l.get('small'))}" {'disabled' if l.get('photo') else ''}></td>
<td><button formaction="/snap?i={i}" class=g>Xem khung</button>{img}</td></tr>""")
    srcs = "".join(f'<tr><td class=t>{s["t"]:.1f}s</td><td colspan=4><input class=x name="src_{i}" value="{E(s["text"])}"></td><td></td></tr>' for i, s in enumerate(F["hud"].get("src", [])))
    job = STATE["job"]; status = ""
    if job: status = f'<div class=box>Đang {job}… (trang tự tải lại)<pre>{E(STATE["log"][-1500:])}</pre></div><meta http-equiv=refresh content=10>'
    elif STATE["done"]: status = f'<div class=box ok>Xong: <a href="/video">tải video mới</a> · <video src="/video" controls width=270></video></div>'
    return f"""<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width"><title>Chỉnh số liệu video</title>
<style>body{{font:15px system-ui;margin:16px;background:#0e1a2b;color:#eef}}table{{border-collapse:collapse;width:100%}}td,th{{border-bottom:1px solid #2a3b55;padding:6px;vertical-align:top}}
input{{width:100%;box-sizing:border-box;background:#14243a;color:#fff;border:1px solid #3a5270;border-radius:6px;padding:6px;font:inherit}}input:disabled{{opacity:.35}}
input.s{{width:90px}}input.w{{min-width:260px}}.t{{white-space:nowrap;color:#9bb}}button{{background:#2fd3e0;color:#0e1a2b;border:0;border-radius:8px;padding:8px 14px;font-weight:700;cursor:pointer}}
button.g{{background:#3a5270;color:#fff;padding:6px 10px}}button.r{{background:#f28c28}}img{{display:block;width:150px;margin-top:6px;border-radius:6px}}
.bar{{position:sticky;top:0;background:#0e1a2b;padding:10px 0;display:flex;gap:10px;flex-wrap:wrap;align-items:center;z-index:2}}.box{{background:#14243a;padding:10px;border-radius:8px;margin:10px 0}}.ok{{border:2px solid #4ade80}}
pre{{white-space:pre-wrap;font-size:12px;color:#9bb}}</style>
<h2>Chỉnh số liệu / chữ trên video</h2><p>Sửa ô cần đổi → <b>Lưu</b> → <b>Xem khung</b> ở dòng đó để kiểm tra → <b>Render video</b> (≈ 50–70 phút).</p>
{f'<div class=box>{E(msg)}</div>' if msg else ''}{status}
<form method=post action=/save><div class=bar><button>Lưu</button><button class=r formaction=/render>Render video</button></div>
<table><tr><th>Lúc</th><th>Số / chữ lớn</th><th>Đơn vị</th><th>Chữ</th><th>Chữ nhỏ</th><th>Kiểm tra</th></tr>{''.join(rows)}
<tr><th colspan=6>Dòng nguồn (cuối màn hình)</th></tr>{srcs}</table></form>"""

def save(form):
    F = load(); shutil.copy(FJ, FJ + ".bak"); changed = 0
    for i, l in enumerate(F["labels"]):
        for k in ("big", "unit", "text", "small"):
            v = form.get(f"{k}_{i}")
            if v is None: continue
            v = v[0].strip()
            if (l.get(k) or "") != v:
                changed += 1
                if v: l[k] = v
                else: l.pop(k, None)
        if l.get("count") and l.get("big"):
            n = num(l["big"])
            if n is not None:
                dec = len(re.split(r",", l["big"])[1].strip("% ")) if "," in l["big"] else 0
                l["count"]["to"] = int(n) if n == int(n) and dec == 0 else n; l["count"]["from"] = 0
                if dec: l["count"]["dec"] = dec
                else: l["count"].pop("dec", None)
            else: l.pop("count")
    for i, s in enumerate(F["hud"].get("src", [])):
        v = form.get(f"src_{i}")
        if v and v[0].strip() != s["text"]: s["text"] = v[0].strip(); changed += 1
    json.dump(F, open(FJ, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    c1, o1 = run([sys.executable, f"{SK}/scripts/flight.py", "flight.json", "."])
    c2, o2 = run(["npx", "-y", "hyperframes@0.9.28", "check", "."])
    ok = "Check passed" in o2
    return f"Đã lưu {changed} thay đổi. hyperframes check: {'ĐẠT' if ok else 'CÓ LỖI — xem khung để kiểm tra'}.\n{o1.strip()[-400:]}"

def snap(i):
    F = load(); l = F["labels"][i]; t = round(l["t"] + min(1.2, l.get("d", 2) / 2), 2)
    out = f"{P}/out/editor/_s"; shutil.rmtree(out, ignore_errors=True); os.makedirs(f"{P}/out/editor", exist_ok=True)
    c, o = run(["npx", "-y", "hyperframes@0.9.28", "snapshot", "--no-end", "--at", str(t), "-o", out, "."])
    fs = [f for f in os.listdir(out) if f.startswith("frame-")] if os.path.isdir(out) else []
    if fs: shutil.copy(f"{out}/{fs[0]}", f"{P}/out/editor/{i}.png"); return f"Khung lúc {t}s đã chụp (ảnh nhỏ ở dòng đó)."
    return "Chụp khung lỗi: " + o[-500:]

def render():
    STATE["job"] = "render"; STATE["done"] = None; STATE["log"] = ""
    dur = A.duration or load()["duration"]
    cmd = (f'bash "{SK}/scripts/render_segments.sh" "{P}" out/raw.mp4 {dur} && '
           f'"{sys.executable}" "{SK}/scripts/mb_post.py" flight.json out/raw.mp4 out/mb.mp4 --shutter 180 && '
           'ffmpeg -v error -y -i out/mb.mp4 -i assets/mix.wav -map 0:v -map 1:a -c:v libx264 -b:v 5000k -maxrate 6500k -bufsize 10000k '
           '-pix_fmt yuv420p -r 30 -movflags +faststart -af "alimiter=limit=0.80:level=disabled" -c:a aac -b:a 192k -shortest out/final.mp4 && echo XONG')
    shutil.rmtree(f"{P}/out/seg", ignore_errors=True)
    p = subprocess.Popen(cmd, cwd=P, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in p.stdout: STATE["log"] += line
    p.wait(); STATE["job"] = None; STATE["done"] = p.returncode == 0 and os.path.exists(f"{P}/out/final.mp4")
    if not STATE["done"]: STATE["log"] += "\nRENDER LỖI"

class H(BaseHTTPRequestHandler):
    def send(self, body, ctype="text/html; charset=utf-8", code=200):
        b = body if isinstance(body, bytes) else body.encode(); self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", len(b)); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        u = urlparse(self.path)
        if u.path.startswith("/snap/"):
            f = f"{P}/out/editor/{os.path.basename(u.path)}"
            return self.send(open(f, "rb").read(), "image/png") if os.path.exists(f) else self.send("không có", code=404)
        if u.path == "/video":
            f = f"{P}/out/final.mp4"
            return self.send(open(f, "rb").read(), "video/mp4") if os.path.exists(f) else self.send("chưa có", code=404)
        self.send(page())
    def do_POST(self):
        form = parse_qs(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode(), keep_blank_values=True); u = urlparse(self.path)
        if STATE["job"]: return self.send(page("Đang render, chờ xong rồi sửa tiếp."))
        msg = save(form)
        if u.path == "/snap": msg += "\n" + snap(int(parse_qs(u.query)["i"][0]))
        if u.path == "/render": threading.Thread(target=render, daemon=True).start(); msg += "\nĐã bắt đầu render."
        self.send(page(msg))
    def log_message(self, *a): pass

print(f"Cửa sổ chỉnh: http://localhost:{A.port}"); ThreadingHTTPServer(("0.0.0.0", A.port), H).serve_forever()
