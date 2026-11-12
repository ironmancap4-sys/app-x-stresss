#!/usr/bin/env python3
"""flight.py — phong cách C "một camera, một bản đồ sống" (Animated Map Infographic) cho HyperFrames.

  python flight.py flight.json <project_dir>    # sinh compositions/map.html, hud.html, fN.html + index.html + CAMLOG.md + kiểm luật

Toàn bộ video là MỘT composition bản đồ dài suốt video với MỘT camera (vmap3.js, Hermite 5 kênh: lat, lng, Z, pitch, bearing).
Thông tin là các LỚP trên bản đồ (bật/tắt bằng sự kiện `ev`), không cắt cảnh. Footage chỉ ghé ≤ 3 s bằng zoom-through.

flight.json:
{ "duration", "audio", "gsap", "sat":[...], "points":{"k":[lng,lat]}, "blocks":"blocks.json", "blockH":{"g":m},
  "cam": [[t,lat,lng,Z,pitch,bearing], ...],
  "layers":[{id,geo,kind,w,fill,len}], "links":[{id,a,b,bend,kind,w}], "circles":[{id,pt,r_m,kind,heat,lat}],
  "rings":[{id,pt,lat,t,km,out}], "movers":[{path,t,d,icon,out}],
  "labels":[{at,lx,ly,align,big,text,small,color,t,d,xl,count}], "pins":[{at,text,t,d,left}], "ground":[{at,text,t,d,size}],
  "ev":[{t,act:"draw|show|hide|dim|grow|fade",id,d,to}],
  "hud":{"clouds":[t0,t1], "legend":[{t,d,items:[[màu,chữ]]}], "src":[{t,d,text}]},
  "foot":[{t,d,media,move,focus,src}],
  "cuts":[t,...],   # cắt cứng (tối đa 3)
  "chapters":[{t,name,V,title}] }
"""
import html, json, math, os, sys

def esc(s): return html.escape(str(s), quote=False)
def wx(lng): return (lng + 180) / 360 * 256 * 2 ** 8
def wy(lat): r = math.radians(lat); return (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * 256 * 2 ** 8
def vn(v, dec=0):
    i, _, d = f"{v:,.{dec}f}".partition("."); return i.replace(",", ".") + ("," + d if d else "")

PIN = '<svg class="pi" viewBox="0 0 44 60"><path d="M22 58 C22 58 4 34 4 20 a18 18 0 0 1 36 0 c0 14-18 38-18 38z" fill="#FACC15" stroke="#0E1A2B" stroke-width="3"/><circle cx="22" cy="20" r="7" fill="#0E1A2B"/></svg>'
PAD = [1100, 2800]

def la_html(l, i):
    lx, ly = l.get("lx", 0), l.get("ly", -120)
    al = l.get("align") or ("l" if lx >= 0 else "r")
    gx = 12 if al == "l" else -12 if al == "r" else 0
    tr = {"l": "translate(0,-50%)", "r": "translate(-100%,-50%)", "c": "translate(-50%,-100%)" if ly < 0 else "translate(-50%,0)"}[al]
    ta = {"l": "left", "r": "right", "c": "center"}[al]
    big = ""
    if l.get("big") is not None:
        big = f'<b class="{"xl" if l.get("xl") else ""}"><span class="cnt" id="la{i}-n">{esc(l["big"])}</span>{f"<u>{esc(l["unit"])}</u>" if l.get("unit") else ""}</b>'
    small = f'<small>{esc(l["small"])}</small>' if l.get("small") else ""
    return (f'<div id="la{i}" class="la c-{l.get("color","w")} mlab" data-at="{l["at"]}">'
            f'<span class="lead" style="width:{math.hypot(lx, ly):.0f}px;transform:rotate({math.atan2(ly, lx):.4f}rad)"></span><span class="dot"></span>'
            f'<span class="tx" style="left:{lx + gx}px;top:{ly}px;transform:{tr};text-align:{ta}">{big}{esc(l.get("text",""))}{small}</span></div>')

def build_map(F, P, tl):
    body = [f'<div class="zw" id="zw"><div class="plane" id="pl">',
            f'<svg id="mapsvg" class="map" width="{1080+2*PAD[0]}" height="{1920+PAD[1]+1400}" viewBox="0 0 {1080+2*PAD[0]} {1920+PAD[1]+1400}" '
            f'style="left:-{PAD[0]}px;top:-{PAD[1]}px" data-layout-allow-overflow><g class="world"></g></svg>', '<div id="blkhost"></div>']
    D = F["duration"]
    for i, l in enumerate(F.get("labels", [])):
        body.append(la_html(l, i))
        end = min(l["t"] + l.get("d", D), D - 0.05)
        tl.append(f'tl.fromTo("#la{i} > *", {{opacity:0}}, {{opacity:1, duration:.35}}, {l["t"]}); tl.to("#la{i} > *", {{opacity:0, duration:.35}}, {end});')
        if l.get("count") is not None:
            c = l["count"]; dec = c.get("dec", 0)
            tl.append(f'(() => {{ const e = document.querySelector("#la{i}-n"), o = {{v:{c["from"]}}}; '
                      f'tl.fromTo(o, {{v:{c["from"]}}}, {{v:{c["to"]}, duration:.8, ease:"power2.out", onUpdate: () => {{ e.textContent = fmt(o.v, {dec}); }}}}, {l["t"]}); }})();')
    for i, p in enumerate(F.get("pins", [])):
        body.append(f'<div id="pin{i}" class="pin {"l" if p.get("left") else ""} mlab" data-at="{p["at"]}"><div class="pw">{PIN}<span class="pl">{esc(p["text"])}</span></div></div>')
        tl.append(f'tl.fromTo("#pin{i} .pw", {{y:-90, opacity:0}}, {{y:0, opacity:1, duration:.45, ease:"bounce.out"}}, {p["t"]}); tl.to("#pin{i} .pw", {{opacity:0, duration:.3}}, {min(p["t"]+p.get("d",D), D-.05)});')
    for i, g in enumerate(F.get("ground", [])):
        sz = f' style="font-size:{g["size"]}px"' if g.get("size") else ""
        body.append(f'<div id="gt{i}" class="ground mlab" data-at="{g["at"]}"><span{sz}>{esc(g["text"])}</span></div>')
        tl.append(f'tl.fromTo("#gt{i} span", {{opacity:0, scale:.7, y:60}}, {{opacity:1, scale:1, y:0, duration:.7, ease:"expo.out"}}, {g["t"]}); '
                  f'tl.to("#gt{i} span", {{opacity:0, scale:1.08, duration:.45, ease:"power2.in"}}, {min(g["t"]+g["d"], D-.05)});')
    body.append("</div>")
    body.append('<div id="fog" style="position:absolute;left:0;right:0;top:0;height:560px;opacity:0;background:linear-gradient(180deg, #0E1A2B 0%, rgba(14,26,43,.85) 28%, rgba(14,26,43,0))"></div>')
    body.append("</div>")
    for e in F.get("ev", []):
        a, t, d = e["act"], e["t"], e.get("d", .6)
        if a == "draw":
            tl.append(f'tl.set("#{e["id"]}", {{opacity:1}}, {t}); tl.fromTo(["#{e["id"]}-core", "#{e["id"]}-glow"], {{strokeDashoffset:110}}, {{strokeDashoffset:0, duration:{d}, ease:"power2.inOut"}}, {t});')
        elif a in ("show", "dim", "fade"):
            to = e.get("to", 1 if a == "show" else .4)
            tl.append(f'tl.to("#{e["id"]}", {{opacity:{to}, duration:{d}, ease:"power1.inOut"}}, {t});')
        elif a == "hide":
            tl.append(f'tl.to("#{e["id"]}", {{opacity:0, duration:{d}, ease:"power1.inOut"}}, {t});')
        elif a == "grow":   # khối 3D mọc lên (nhóm g)
            tl.append(f'tl.to(BHo, {{"{e["id"]}":{e.get("to",1)}, duration:{d}, ease:"{e.get("ease","power3.out")}", onUpdate: () => {{ Object.assign(window.BH, BHo); if (window.__f) window.__f(); }}}}, {t});')
        elif a == "tint":   # độ đậm mặt khối nhóm g (không dùng opacity để giữ 3D)
            tl.append(f'tl.to(".blk.g-{e["id"]}", {{"--a":{e.get("to",.35)}, duration:{d}}}, {t});')
    opts = {"svg": "#mapsvg", "labels": ".mlab", "sat": F["sat"], "pad": PAD, "keys": F["cam"], "blockHost": "#blkhost",
            "layers": F.get("layers", []), "links": F.get("links", []), "circles": F.get("circles", []), "rings": F.get("rings", []),
            "movers": F.get("movers", []), "blocks": F.get("_blocks", []), "blockH": F.get("blockH", {})}
    pre = (f"const GEO = {open(P + '/geo.json').read()};\nObject.assign(GEO.lab, {json.dumps(F['_pts'])});\n{open(P + '/vmap3.js').read()}\n"
           f"const BHo = {json.dumps({g: 0 for g in F.get('blockH', {})})}; window.BH = Object.assign({{}}, BHo);\n"
           f"const map = makeMap3({json.dumps(opts, ensure_ascii=False)});\nconst pl = document.querySelector('#pl');\n"
           "const frame = (t) => { const c = map.apply(t); const k = 1 + c.p / 70;\n"
           "  pl.style.transform = `perspective(1600px) rotateX(${c.p.toFixed(3)}deg) rotateZ(${c.b.toFixed(3)}deg) scale(${k.toFixed(4)})`;\n"
           "  fog.style.opacity = Math.min(1, c.p / 30).toFixed(3); };\n"
           "const fog = document.querySelector('#fog');")
    tl.append("window.__f = () => frame(clock.t);")
    # đồng hồ camera thêm SAU mọi tween để mỗi lần seek, giá trị lớp (chiều cao khối…) đã cập nhật trước khi vẽ khung
    tl.append(f"const clock = {{ t: 0 }}; tl.fromTo(clock, {{ t: 0 }}, {{ t: {D}, duration: {D}, ease: 'none', onUpdate: () => frame(clock.t) }}, 0); frame(0);")
    return body, pre

def build_hud(F, tl):
    D = F["duration"]; body = []; h = F.get("hud", {})
    if h.get("clouds"):
        import random; rnd = random.Random(5); c0, c1 = h["clouds"]
        for i in range(12):
            x, y, w = rnd.randint(-500, 900), rnd.randint(-300, 1800), rnd.randint(900, 1500)
            body.append(f'<div class="cloud hcl" style="left:{x}px;top:{y}px;width:{w}px;height:{int(w*.55)}px"></div>')
        tl.append(f'tl.fromTo(".hcl", {{opacity:1, scale:1}}, {{opacity:0, scale:3.6, duration:{c1-c0}, stagger:.04, ease:"power2.in"}}, {c0});')
    for i, lg in enumerate(h.get("legend", [])):
        items = "".join(f'<div class="li"><i style="background:{c}"></i>{esc(t)}</div>' for c, t in lg["items"])
        body.append(f'<div class="legend" id="lg{i}">{items}</div>')
        tl.append(f'tl.fromTo("#lg{i}", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:.4}}, {lg["t"]}); tl.to("#lg{i}", {{opacity:0, duration:.4}}, {min(lg["t"]+lg["d"], D-.05)});')
    for i, s in enumerate(h.get("src", [])):
        body.append(f'<p class="src" id="src{i}">{esc(s["text"])}</p>')
        tl.append(f'tl.fromTo("#src{i}", {{opacity:0}}, {{opacity:1, duration:.4}}, {s["t"]}); tl.to("#src{i}", {{opacity:0, duration:.4}}, {min(s["t"]+s["d"], D-.05)});')
    return body

def build_foot(f, i, tl):
    m, D = f["media"], f["d"]
    if m.endswith(".mp4"):
        media = f'<video id="fv{i}" class="clip" src="{m}" muted playsinline data-start="0" data-duration="{D}" data-media-start="{f.get("media_start",0)}" data-track-index="1" style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover"></video>'
    else:
        media = f'<img src="{m}" alt="" style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;object-position:{f.get("focus","50% 50%")}" />'
    MOV = {"push": ("{scale:1.30}", "{scale:1.08}"), "pull": ("{scale:1.08}", "{scale:1.26}"), "panL": ("{scale:1.25, x:70}", "{scale:1.25, x:-70}"),
           "panR": ("{scale:1.25, x:-70}", "{scale:1.25, x:70}"), "panU": ("{scale:1.22, y:90}", "{scale:1.22, y:-90}")}
    a, b = MOV[f.get("move", "push")]
    tl.append(f'tl.fromTo("#fm{i}", {a}, Object.assign({b}, {{duration:{D}, ease:"none"}}), 0);')
    blend = f.get("blend", .65)
    tl.append(f'tl.fromTo("#fw{i}", {{opacity:0, filter:"blur(10px)"}}, {{opacity:1, filter:"blur(0px)", duration:{blend}, ease:"power2.out"}}, 0); '
              f'tl.to("#fw{i}", {{opacity:0, filter:"blur(8px)", duration:{blend}, ease:"power2.in"}}, {D - blend});')
    return [f'<div id="fw{i}" style="position:absolute;inset:0;overflow:hidden"><div id="fm{i}" style="position:absolute;inset:0">{media}</div>'
            f'<div class="gtop"></div></div>']

def comp(cid, body, pre, tl, css, bg=True):
    return f"""<template>
  <style>
{css}
    #root {{ position: absolute; inset: 0; overflow: hidden; {"" if bg else "background: transparent;"} }}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{chr(10).join(body)}
  </div>
  <script>
    (() => {{
      const tl = gsap.timeline({{ paused: true }});
      const fmt = (v, dec) => {{ const [i, d] = v.toFixed(dec).split("."); return i.replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ".") + (d ? "," + d : ""); }};
      {pre}
{chr(10).join("      " + l for l in tl)}
      window.__timelines["{cid}"] = tl;
    }})();
  </script>
</template>
"""

def cam_sampler(K):
    """Bản Python của camera Hermite đơn điệu trong vmap3.js (để kiểm tra camera không đứng yên)."""
    T = [k[0] for k in K]; ch = [[wx(k[2]) for k in K], [wy(k[1]) for k in K], [k[3] for k in K], [k[4] if len(k) > 4 else 0 for k in K], [k[5] if len(k) > 5 else 0 for k in K]]
    def slopes(vs):
        n = len(vs); dl = [(vs[i + 1] - vs[i]) / (T[i + 1] - T[i]) for i in range(n - 1)]; m = [0.0] * n
        for i in range(1, n - 1): m[i] = 0 if dl[i - 1] * dl[i] <= 0 else (dl[i - 1] + dl[i]) / 2
        for i in range(n - 1):
            if dl[i] == 0: m[i] = m[i + 1] = 0; continue
            a, b = m[i] / dl[i], m[i + 1] / dl[i]; q = a * a + b * b
            if q > 9: t = 3 / math.sqrt(q); m[i] = t * a * dl[i]; m[i + 1] = t * b * dl[i]
        return m
    M = [slopes(v) for v in ch]
    def at(t):
        t = min(max(t, T[0]), T[-1]); i = 0
        while i < len(T) - 2 and t > T[i + 1]: i += 1
        h = T[i + 1] - T[i]; s = (t - T[i]) / h; s2, s3 = s * s, s * s * s
        return [(2*s3-3*s2+1)*v[i] + (s3-2*s2+s)*h*m[i] + (-2*s3+3*s2)*v[i+1] + (s3-s2)*h*m[i+1] for v, m in zip(ch, M)]
    return at

def validate(F, js_sample=None):
    D = F["duration"]; msg = []
    cuts = F.get("cuts", [])
    if len(cuts) > 3: msg.append(f"{len(cuts)} cắt cứng > 3")
    ft = sum(f["d"] for f in F.get("foot", []))
    for f in F.get("foot", []):
        if f["d"] > 3.0 + 1e-6: msg.append(f"footage @{f['t']}: {f['d']} s > 3 s (bản đồ biến mất quá 3 s)")
    if ft > 0.2 * D: msg.append(f"footage tổng {ft:.1f} s > 20%")
    ch = F["chapters"]; share = {}
    for a, b in zip(ch, ch[1:] + [{"t": D}]):
        share[a["V"]] = share.get(a["V"], 0) + b["t"] - a["t"]
    for a, b in zip(ch, ch[1:]):
        if a["V"] == b["V"]: msg.append(f"chương '{b['name']}' lặp kiểu {b['V']} với chương trước")
    for v, d in share.items():
        if d > 0.2 * D + 1e-6: msg.append(f"{v}: {d:.1f} s > 20%")
    # camera: dừng > 1 s / quay > 90° một lần / chuyển động thẳng đều (không ease)
    K = F["cam"]
    for a, b in zip(K, K[1:]):
        if abs((b[5] if len(b) > 5 else 0) - (a[5] if len(a) > 5 else 0)) > 90: msg.append(f"quay > 90° giữa {a[0]}–{b[0]} s")
        same = all(abs(x - y) < 1e-9 for x, y in zip(a[1:], b[1:]))
        if same and b[0] - a[0] > 1: msg.append(f"camera đứng yên {a[0]}–{b[0]} s")
    # camera không đứng yên quá 1 s: mọi cửa sổ 1 s phải đổi Z ≥ 0,004 (~0,3% tỉ lệ) hoặc nghiêng/quay ≥ 0,15° hoặc lia ≥ 1,5 px
    at = cam_sampler(K); still = []
    t = F["cam"][0][0]
    while t + 1 <= F["cam"][-1][0]:
        a, b = at(t), at(t + 1); sc = 2 ** (a[2] - 8)
        moving = abs(b[2] - a[2]) >= .004 or abs(b[3] - a[3]) >= .15 or abs(b[4] - a[4]) >= .15 or math.hypot(b[0] - a[0], b[1] - a[1]) * sc >= 1.5
        if not moving: still.append(round(t, 1))
        t += 0.25
    if still: msg.append(f"camera gần như đứng yên > 1 s quanh {still[:6]}")
    return msg, share, ft

def main():
    F = json.load(open(sys.argv[1], encoding="utf-8")); P = sys.argv[2]
    F["_pts"] = {k: [round(wx(v[0]), 3), round(wy(v[1]), 3)] for k, v in F.get("points", {}).items()}
    if F.get("blocks"): F["_blocks"] = json.load(open(F["blocks"])) if isinstance(F["blocks"], str) else F["blocks"]
    css = open(f"{P}/fonts.css").read() + open(f"{P}/motion.css").read() + open(f"{P}/flight.css").read()
    os.makedirs(f"{P}/compositions", exist_ok=True); D = F["duration"]
    tl = []; body, pre = build_map(F, P, tl)
    open(f"{P}/compositions/map.html", "w").write(comp("map", body, pre, tl, css))
    tl = []; body = build_hud(F, tl)
    open(f"{P}/compositions/hud.html", "w").write(comp("hud", body, "", tl, css, bg=False))
    hosts = [f'<div id="map" data-composition-id="map" data-composition-src="compositions/map.html" data-start="0" data-duration="{D}" data-track-index="1" data-width="1080" data-height="1920" style="z-index:1"></div>']
    for i, f in enumerate(F.get("foot", [])):
        tl = []; body = build_foot(f, i, tl)
        open(f"{P}/compositions/f{i}.html", "w").write(comp(f"f{i}", body, "", tl, css, bg=False))
        hosts.append(f'<div id="f{i}" data-composition-id="f{i}" data-composition-src="compositions/f{i}.html" data-start="{f["t"]}" data-duration="{f["d"]}" data-track-index="2" data-width="1080" data-height="1920" style="z-index:5"></div>')
    hosts.append(f'<div id="hud" data-composition-id="hud" data-composition-src="compositions/hud.html" data-start="0" data-duration="{D}" data-track-index="3" data-width="1080" data-height="1920" style="z-index:9"></div>')
    open(f"{P}/index.html", "w").write(f"""<!doctype html>
<html lang="vi">
  <head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
    <script src="{F.get('gsap','assets/lib/gsap.min.js')}"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0E1A2B; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
      {chr(10).join("      " + h for h in hosts)}
      <audio id="mix" class="clip" src="{F.get('audio','assets/mix.wav')}" data-start="0" data-duration="{D}" data-track-index="30" data-volume="1"></audio>
    </div>
    <script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
""")
    msg, share, ft = validate(F)
    tc = lambda t: f"{int(t // 60)}:{t % 60:05.2f}"
    rows = ["# Camera log", "", f"Một camera liên tục · {len(F['cam'])} keyframe · cắt cứng: {len(F.get('cuts', []))} · footage {ft:.1f} s ({ft/D*100:.0f}%)", "",
            "| Timecode | Chương | Kiểu chính | Chuyển động camera | Lớp trên bản đồ | Footage |", "|---|---|---|---|---|---|"]
    ch = F["chapters"]
    for a, b in zip(ch, ch[1:] + [{"t": D}]):
        foot = "; ".join(f"{tc(f['t'])} {f.get('src','')}" for f in F.get("foot", []) if a["t"] <= f["t"] < b["t"])
        rows.append(f"| {tc(a['t'])}–{tc(b['t'])} | {esc(a['name'])} | {a['V']} | {esc(a.get('cam',''))} | {esc(a.get('layers',''))} | {esc(foot) or '—'} |")
    rows += ["", "## Keyframe camera", "", "| t (s) | lat | lng | Z | pitch | bearing |", "|---|---|---|---|---|---|"]
    rows += [f"| {k[0]} | {k[1]:.4f} | {k[2]:.4f} | {k[3]:.2f} | {k[4] if len(k)>4 else 0} | {k[5] if len(k)>5 else 0} |" for k in F["cam"]]
    rows += ["", "## Tỉ lệ kiểu trực quan hoá (chương)", ""] + [f"- {v}: {d:.1f} s ({d/D*100:.0f}%)" for v, d in sorted(share.items())]
    rows += ["", "## Kiểm luật", ""] + ([f"- {m}" for m in msg] or ["- Đạt: ≤ 3 cắt cứng, footage ≤ 3 s/lần & ≤ 20%, không chương liền nhau trùng kiểu, mỗi kiểu ≤ 20%, không quay > 90°/lần."])
    open(f"{P}/CAMLOG.md", "w").write("\n".join(rows))
    print(f"map + hud + {len(F.get('foot', []))} footage · cắt {len(F.get('cuts', []))} · footage {ft:.1f}s")
    for m in msg: print("  !", m)

if __name__ == "__main__":
    main()
