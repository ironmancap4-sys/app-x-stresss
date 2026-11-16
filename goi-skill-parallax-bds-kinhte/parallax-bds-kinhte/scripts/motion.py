#!/usr/bin/env python3
"""motion.py — storyboard shot-by-shot -> project HyperFrames phong cách "bản đồ + footage" điện ảnh.

  python motion.py shots.json <project_dir>          # sinh compositions/ + index.html + SHOTLIST.md + kiểm tra luật

Project cần: fonts.css, assets/fonts, motion.css (design/), vmap2.js (scripts/), geo.json (geo_build.py), audio.
Mỗi shot khai báo "fx" (mã thư viện M1–M10, T1–T5, F1–F3, D1–D6) để bộ kiểm tra soát lặp/tỉ lệ.

shots.json: { "duration": s, "audio": "assets/mix.wav", "gsap": "...", "points": {"key": [lng,lat]},
  "sat": [{img,z,x0,y0,w,h,show}], "shots": [ {
    "id","start","dur","kind":"map|foot|card","fx":[..],"src":"nguồn (cho shot list)",
    "enter":"T1|T2|T3|T4|T5|DIS", "seg","foot","dim":0..0.7,
    "media":"assets/x.mp4|jpg", "move":"push|pull|panL|panR|panU|panD|none", "media_start":0,
    "kw":[{"t","d","lines":["CHỮ","*NHẤN"],"pos":"low|mid|high","accent":"#hex"}],          F3
    "big":{"t","d","num","dec","unit","label","pos","accent"},                              D1
    "bar":{"t","d","label","value","max","unit","sub"},                                     D2
    "timeline":{"t","y","events":[{"t","date","text","x"}]},                                D5
    "wall":{"t","top","tiles":[{"t","name","sub","hl"}]},                                   D6
    "stack":{"t","top","rows":[{"t","num","dec","unit","label"}]},                         D4
    "callouts":[{"x","y","lx","ly","align","big","text","small","color","t","d"}],         (toạ độ màn hình)
    map: "keys":[[t,lat,lng,Z(,carry)]], "tilt":[t0,t1,a0,a1], "orbit":[t0,t1,a0,a1], "clouds":[t0,t1], "zoomBlur":true,
         "layers":[{geo,kind,fill,id,w,len}], "links":[{a,b,bend,kind,id,w}], "movers":[{path,t,d,icon}],
         "rings":[{pt,lat,t,km:[..]}], "pins":[{at,text,t,left}], "ground":[{at,text,t,d}],
         "labels":[{at,lx,ly,align,big,text,small,color,t,d}], "show":[{id,t,d,to}], "hide":[{id,t,d}], "draw":[{id,t,d}]
  } ] }
Thời gian trong shot là cục bộ (0 = start danh nghĩa). T1/T4/DIS tự bắt đầu sớm 0,35 s để hoà/che lên shot trước.
"""
import html, json, math, os, sys

OVER = 0.35
FOOTAGE, MAP, DATA = "foot", "map", "card"

def esc(s): return html.escape(str(s), quote=False)
def vn(v):
    """Số kiểu Việt: 30.000 · 49,5"""
    i, _, d = (f"{v:,.{len(str(v).split('.')[1]) if isinstance(v, float) else 0}f}").partition(".")
    return i.replace(",", ".") + ("," + d if d else "")
def wx(lng): return (lng + 180) / 360 * 256 * 2 ** 8
def wy(lat): r = math.radians(lat); return (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * 256 * 2 ** 8

def words(lines):
    out = []
    for ln in lines:
        ws = [(f'<em><span class="w">{esc(w[1:])}</span></em>' if w.startswith("*") else f'<span class="w">{esc(w)}</span>') for w in ln.split()]
        out.append('<span class="ln">' + " ".join(ws) + "</span>")
    return "".join(out)

def la_html(l, i, sid, mapped):
    lx, ly = l.get("lx", 0), l.get("ly", -120)
    al = l.get("align") or ("l" if lx >= 0 else "r")
    gx = 12 if al == "l" else -12 if al == "r" else 0
    tr = {"l": "translate(0,-50%)", "r": "translate(-100%,-50%)", "c": "translate(-50%,-100%)" if ly < 0 else "translate(-50%,0)"}[al]
    ta = {"l": "left", "r": "right", "c": "center"}[al]
    big = f'<b>{esc(l["big"])}</b>' if l.get("big") else ""
    small = f'<small>{esc(l["small"])}</small>' if l.get("small") else ""
    pos = f'data-at="{l["at"]}"' if mapped else f'style="transform: translate({l["x"]}px, {l["y"]}px)"'
    return (f'<div id="{sid}-la{i}" class="la c-{l.get("color","adm")} {sid}-lab" {pos}>'
            f'<span class="lead" style="width:{math.hypot(lx, ly):.0f}px;transform:rotate({math.atan2(ly, lx):.4f}rad)"></span><span class="dot"></span>'
            f'<span class="tx" style="left:{lx + gx}px;top:{ly}px;transform:{tr};text-align:{ta}">{big}{esc(l.get("text",""))}{small}</span></div>')

PIN_SVG = '<svg class="pi" viewBox="0 0 44 60"><path d="M22 58 C22 58 4 34 4 20 a18 18 0 0 1 36 0 c0 14-18 38-18 38z" fill="#FACC15" stroke="#0E1A2B" stroke-width="3"/><circle cx="22" cy="20" r="7" fill="#0E1A2B"/></svg>'
PLANE_SVG = '<svg class="plane-ic" viewBox="0 0 100 100"><path d="M50 6 L56 40 L92 58 L92 64 L56 54 L54 80 L64 88 L64 92 L50 88 L36 92 L36 88 L46 80 L44 54 L8 64 L8 58 L44 40 Z" fill="#fff" stroke="#0E1A2B" stroke-width="2"/></svg>'

def shot_html(sh, P, prev):
    sid, dur = sh["id"], sh["dur"]
    off = OVER if sh.get("enter") in ("T1", "T4", "DIS") else 0.0
    D = dur + off
    T = lambda t: round(t + off, 3)
    endtxt = round(D - 0.32, 3)
    css = [open(f"{P}/fonts.css").read(), open(f"{P}/motion.css").read()]
    body, tl, pre = [], [], ""
    kind = sh["kind"]
    # ---------- nền
    if kind == MAP:
        body.append(f'<div id="{sid}-z" class="zw"><div id="{sid}-pl" class="plane">'
                    + (f'<svg id="{sid}-map" class="map" width="2400" height="3700" viewBox="0 0 2400 3700" style="left:-660px;top:-1500px" data-layout-allow-overflow><g class="world"></g></svg>'
                     if sh.get("tilt") else f'<svg id="{sid}-map" class="map" width="1080" height="1920" viewBox="0 0 1080 1920" data-layout-allow-overflow><g class="world"></g></svg>'))
        for i, l in enumerate(sh.get("labels", [])): body.append(la_html(l, i, sid, True))
        for i, p in enumerate(sh.get("pins", [])):
            body.append(f'<div id="{sid}-pin{i}" class="pin {"l" if p.get("left") else ""} {sid}-lab" data-at="{p["at"]}"><div class="pw">{PIN_SVG}<span class="pl">{esc(p["text"])}</span></div></div>')
        for i, g in enumerate(sh.get("ground", [])):
            body.append(f'<div id="{sid}-gt{i}" class="ground {sid}-lab" data-at="{g["at"]}"><span{f' style="font-size:{g["size"]}px"' if g.get("size") else ""}>{esc(g["text"])}</span></div>')
        body.append("</div>")
        if sh.get("tilt"): body.append('<div style="position:absolute;left:0;right:0;top:0;height:640px;background:linear-gradient(180deg, rgba(14,26,43,.85), rgba(14,26,43,0))"></div>')
        if sh.get("clouds"):
            import random; rnd = random.Random(7)
            for i in range(9):
                x, y, w = rnd.randint(-300, 900), rnd.randint(-200, 1700), rnd.randint(700, 1300)
                body.append(f'<div class="cloud {sid}-cl" style="left:{x}px;top:{y}px;width:{w}px;height:{int(w*.55)}px;opacity:0"></div>')
        body.append("</div>")
        opts = {"svg": f"#{sid}-map", "labels": f".{sid}-lab", "sat": SAT, "pad": [660, 1500] if sh.get("tilt") else [0, 0], "keys": [[k[0] + off] + k[1:] for k in sh["keys"]],
                "layers": sh.get("layers", []), "links": sh.get("links", []),
                "movers": [dict(m, t=T(m["t"])) for m in sh.get("movers", [])], "rings": [dict(r, t=T(r["t"])) for r in sh.get("rings", [])]}
        tilt = sh.get("tilt"); orb = sh.get("orbit")
        pre = (f"const GEO = {GEOJS};\nObject.assign(GEO.lab, {json.dumps(PTS)});\n{VMAP}\n"
               f"const map = makeMap2({json.dumps(opts, ensure_ascii=False)});\nconst pl = document.querySelector('#{sid}-pl');\n"
               f"const lerp = (a, b, t0, t1, t) => a + (b - a) * Math.min(1, Math.max(0, (t - t0) / (t1 - t0))) ;\n"
               f"const ease = (a, b, t0, t1, t) => {{ const p = Math.min(1, Math.max(0, (t - t0) / (t1 - t0))); const e = p < .5 ? 2*p*p : 1 - (-2*p+2)**2/2; return a + (b - a) * e; }};\n"
               f"const frame = (t) => {{ map.apply(t); let tr = '';\n"
               + (f"  const tx = ease({tilt[2]}, {tilt[3]}, {T(tilt[0])}, {T(tilt[1])}, t); tr += `perspective(1500px) rotateX(${{tx}}deg) scale(${{1 + tx/90}}) `;\n" if tilt else "")
               + (f"  tr += `rotateZ(${{ease({orb[2]}, {orb[3]}, {T(orb[0])}, {T(orb[1])}, t)}}deg) `;\n" if orb else "")
               + "  pl.style.transform = tr;\n"
               + ("  pl.style.filter = `blur(${Math.min(9, map.speedZ(t) * 2.2).toFixed(2)}px)`;\n" if sh.get("zoomBlur") else "")
               + "};\n"
               f"const clock = {{ t: 0 }}; tl.fromTo(clock, {{ t: 0 }}, {{ t: {D}, duration: {D}, ease: 'none', onUpdate: () => frame(clock.t) }}, 0); frame(0);")
        for i, l in enumerate(sh.get("labels", [])):
            tl.append(f'tl.fromTo("#{sid}-la{i} > *", {{opacity:0}}, {{opacity:1, duration:.3}}, {T(l["t"])}); tl.to("#{sid}-la{i} > *", {{opacity:0, duration:.2}}, {min(T(l["t"] + l["d"]), endtxt)});')
        for i, p in enumerate(sh.get("pins", [])):
            tl.append(f'tl.fromTo("#{sid}-pin{i} .pw", {{y:-90, opacity:0}}, {{y:0, opacity:1, duration:.45, ease:"bounce.out"}}, {T(p["t"])}); tl.to("#{sid}-pin{i} .pw", {{opacity:0, duration:.2}}, {endtxt});')
        for i, g in enumerate(sh.get("ground", [])):
            tl.append(f'tl.fromTo("#{sid}-gt{i} span", {{opacity:0, scale:.7, y:60}}, {{opacity:1, scale:1, y:0, duration:.7, ease:"expo.out"}}, {T(g["t"])}); '
                      f'tl.to("#{sid}-gt{i} span", {{opacity:0, duration:.25}}, {min(T(g["t"] + g["d"]), endtxt)});')
        for s in sh.get("show", []): tl.append(f'tl.fromTo("#{s["id"]}", {{opacity:0}}, {{opacity:{s.get("to",1)}, duration:{s.get("d",.5)}}}, {T(s["t"])});')
        for s in sh.get("hide", []): tl.append(f'tl.to("#{s["id"]}", {{opacity:0, duration:{s.get("d",.4)}}}, {T(s["t"])});')
        for s in sh.get("draw", []):
            tl.append(f'tl.fromTo(["#{s["id"]}-core", "#{s["id"]}-glow"], {{strokeDashoffset:110}}, {{strokeDashoffset:0, duration:{s["d"]}, ease:"power1.inOut"}}, {T(s["t"])});')
        if sh.get("clouds"):
            c0, c1 = sh["clouds"]
            tl.append(f'tl.fromTo(".{sid}-cl", {{opacity:0, scale:.5}}, {{opacity:1, scale:1.4, duration:{(c1-c0)*.45}, stagger:.05, ease:"power1.in"}}, {T(c0)}); '
                      f'tl.to(".{sid}-cl", {{opacity:0, scale:3.2, duration:{(c1-c0)*.55}, stagger:.04, ease:"power2.in"}}, {T(c0 + (c1-c0)*.45)});')
    elif sh.get("media"):
        m = sh["media"]
        if m.endswith(".mp4"):
            media = (f'<div id="{sid}-mv" style="position:absolute;inset:0"><video id="{sid}-v" class="clip" src="{m}" muted playsinline data-start="0" data-duration="{D}" '
                     f'data-media-start="{sh.get("media_start",0)}" data-track-index="1" style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover"></video></div>')
        else:
            media = f'<div id="{sid}-mv" style="position:absolute;inset:0"><img src="{m}" alt="" style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;object-position:{sh.get("focus","50% 50%")}" /></div>'
        dim = f'<div style="position:absolute;inset:0;background:rgba(10,18,32,{sh.get("dim",0)})"></div>' if sh.get("dim") else ""
        body.append(f'<div id="{sid}-z" class="zw">{media}{dim}<div class="gtop"></div><div class="gbot"></div></div>')
        mv = sh.get("move", "push" if not m.endswith(".mp4") else "none")
        MOVES = {"push": ("{scale:1.0}", "{scale:1.14}"), "pull": ("{scale:1.16}", "{scale:1.0}"),
                 "panL": ("{scale:1.22, x:90}", "{scale:1.22, x:-90}"), "panR": ("{scale:1.22, x:-90}", "{scale:1.22, x:90}"),
                 "panU": ("{scale:1.2, y:110}", "{scale:1.2, y:-110}"), "panD": ("{scale:1.2, y:-110}", "{scale:1.2, y:110}")}
        if mv in MOVES:
            a, b = MOVES[mv]
            tl.append(f'tl.fromTo("#{sid}-mv", {a}, Object.assign({b}, {{duration:{D}, ease:"none"}}), 0);')
    elif sh.get("montage"):
        # dựng nhanh chuỗi ảnh (0,5–1 s/ảnh) + chữ động cho từng ảnh — dùng cho liệt kê
        ms = sh["montage"]; parts = []
        for i, it in enumerate(ms):
            t1 = ms[i + 1]["t"] if i + 1 < len(ms) else dur
            parts.append(f'<div id="{sid}-m{i}" style="position:absolute;inset:0;opacity:0"><img src="{it["media"]}" alt="" style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;object-position:{it.get("focus","50% 50%")}" /></div>')
            tl.append(f'tl.set("#{sid}-m{i}", {{opacity:1}}, {T(it["t"])}); tl.fromTo("#{sid}-m{i}", {{scale:1.18}}, {{scale:1.0, duration:{t1 - it["t"]:.3f}, ease:"none"}}, {T(it["t"])});')
            if i + 1 < len(ms): tl.append(f'tl.set("#{sid}-m{i}", {{opacity:0}}, {T(t1)});')
            sh.setdefault("kw", []).append({"t": it["t"], "d": t1 - it["t"], "lines": ["*" + w if j == 0 else w for j, w in enumerate([it["word"]])], "pos": "mid", "_quick": True})
        body.append(f'<div id="{sid}-z" class="zw">{"".join(parts)}<div class="gtop"></div><div class="gbot"></div></div>')
    else:
        body.append(f'<div id="{sid}-z" class="zw" style="background:radial-gradient(ellipse at 50% 42%, #18304f, #0E1A2B)"></div>')
    if sh.get("clouds") and kind != MAP:
        import random; rnd = random.Random(11)
        for i in range(10):
            x, y, w = rnd.randint(-400, 900), rnd.randint(-200, 1700), rnd.randint(800, 1400)
            body.append(f'<div class="cloud {sid}-cl" style="left:{x}px;top:{y}px;width:{w}px;height:{int(w*.55)}px"></div>')
        c0, c1 = sh["clouds"]
        tl.append(f'tl.fromTo(".{sid}-cl", {{opacity:1, scale:1}}, {{opacity:0, scale:3.4, duration:{c1-c0}, stagger:.03, ease:"power2.in"}}, {T(c0)});')
    # ---------- lớp chữ / dữ liệu
    for i, l in enumerate(sh.get("callouts", [])):
        body.append(la_html(l, i, sid, False))
        tl.append(f'tl.fromTo("#{sid}-la{i} > *", {{opacity:0}}, {{opacity:1, duration:.3}}, {T(l["t"])}); tl.to("#{sid}-la{i} > *", {{opacity:0, duration:.2}}, {min(T(l["t"] + l.get("d", 99)), endtxt)});')
    for i, k in enumerate(sh.get("kw", [])):
        top = {"low": "top:1180px", "mid": "top:760px", "high": "top:440px"}[k.get("pos", "low")]
        acc = f'--accent:{k["accent"]};' if k.get("accent") else ""
        body.append(f'<h2 id="{sid}-kw{i}" class="kw clip" style="{top};{acc}" data-start="{T(k["t"])}" data-duration="{round(min(k["d"], D - T(k["t"])),3)}" data-track-index="20">{words(k["lines"])}</h2>')
        tl.append(f'tl.fromTo("#{sid}-kw{i} .w", {{opacity:0, scale:1.35, filter:"blur(14px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:.28, ease:"expo.out", stagger:.06}}, {T(k["t"]) + .02});')
        if k.get("_quick"): tl.append(f'tl.set("#{sid}-kw{i} .w", {{opacity:0}}, {min(T(k["t"] + k["d"]), endtxt + .3)});')
        else: tl.append(f'tl.to("#{sid}-kw{i} .w", {{opacity:0, filter:"blur(10px)", duration:.16}}, {min(T(k["t"] + k["d"]) - .18, endtxt)});')
    if sh.get("big"):
        b = sh["big"]; dec = b.get("dec", 0); st = round(b.get("num", 1) * 0.4, dec)
        if b.get("num") is not None and st <= 0: raise SystemExit(f"{sid}: số quá nhỏ để đếm — dùng 'text'")
        top = {"mid": "top:760px", "low": "top:1080px", "high": "top:470px"}[b.get("pos", "mid")]
        acc = f'style="color:{b["accent"]}"' if b.get("accent") else ""
        body.append(f'<div id="{sid}-big" class="bign" style="{top}"><span class="n" id="{sid}-bn" {acc}>{st}</span><span class="u">{esc(b.get("unit",""))}</span>'
                    f'<span class="lb">{esc(b.get("label",""))}</span></div>')
        if b.get("text"):
            body[-1] = body[-1].replace(f'>{st}</span>', f'>{esc(b["text"])}</span>', 1)
            tl.append(f'tl.fromTo("#{sid}-big", {{opacity:0, scale:.7, filter:"blur(14px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:.35, ease:"expo.out"}}, {T(b["t"])}); tl.to("#{sid}-big", {{opacity:0, duration:.2}}, {min(T(b["t"] + b["d"]), endtxt)});')
        else: tl.append(f'(() => {{ const el = document.querySelector("#{sid}-bn"), o = {{v:{st}}}; el.textContent = fmt({st}, {dec}); '
                  f'tl.fromTo("#{sid}-big", {{opacity:0, scale:.8, filter:"blur(12px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:.3, ease:"expo.out"}}, {T(b["t"])}); '
                  f'tl.fromTo(o, {{v:{st}}}, {{v:{b["num"]}, duration:.8, ease:"power2.out", onUpdate: () => {{ el.textContent = fmt(o.v, {dec}); }}}}, {T(b["t"])}); '
                  f'tl.to("#{sid}-big", {{opacity:0, duration:.2}}, {min(T(b["t"] + b["d"]), endtxt)}); }})();')
    if sh.get("bar"):
        b = sh["bar"]
        body.append(f'<div id="{sid}-bar" class="bar" style="top:{b.get("top",900)}px"><div class="bl">{esc(b["label"])}</div><div class="bt"><div class="bf" id="{sid}-bf"></div></div>'
                    f'<div class="bv"><span id="{sid}-bvn">{vn(b["value"])}</span><small>{esc(b.get("unit",""))}</small></div><div class="bs">{esc(b.get("sub",""))}</div></div>')
        tl.append(f'tl.fromTo("#{sid}-bar", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:.3}}, {T(b["t"])}); '
                  f'tl.fromTo("#{sid}-bf", {{scaleX:0}}, {{scaleX:{b["value"]/b["max"]:.3f}, duration:1.1, ease:"power2.out"}}, {T(b["t"]) + .1}); '
                  f'tl.to("#{sid}-bar", {{opacity:0, duration:.2}}, {min(T(b["t"] + b["d"]), endtxt)});')
    if sh.get("timeline"):
        tlx = sh["timeline"]; evs = []
        for i, e in enumerate(tlx["events"]):
            evs.append(f'<div class="ev {"lo" if i % 2 else ""}" id="{sid}-ev{i}" style="left:{e["x"]}px"><i></i><span class="d">{esc(e["date"])}</span><span class="t">{esc(e["text"])}</span></div>')
            tl.append(f'tl.fromTo("#{sid}-ev{i} > *", {{opacity:0, scale:.6}}, {{opacity:1, scale:1, duration:.35, ease:"back.out(2)", stagger:.06}}, {T(e["t"])});')
        body.append(f'<div class="tline" id="{sid}-tl" style="top:{tlx.get("y",900)}px"><div class="ax" id="{sid}-ax"></div>{"".join(evs)}</div>')
        tl.append(f'tl.fromTo("#{sid}-ax", {{scaleX:0}}, {{scaleX:1, duration:.7, ease:"power2.out"}}, {T(tlx["t"])}); tl.to("#{sid}-tl", {{opacity:0, duration:.2}}, {endtxt});')
    if sh.get("wall"):
        w = sh["wall"]; tiles = []
        for i, ti in enumerate(w["tiles"]):
            tiles.append(f'<div class="tile {"hl" if ti.get("hl") else ""}" id="{sid}-ti{i}"><b>{esc(ti["name"])}</b><small>{esc(ti.get("sub",""))}</small></div>')
            fx, fy = [(-900, -300), (900, -200), (-900, 200), (900, 300), (0, 900), (0, -900), (-900, 600), (900, 600)][i % 8]
            tl.append(f'tl.fromTo("#{sid}-ti{i}", {{x:{fx}, y:{fy}, rotation:{(-1)**i*12}, opacity:0}}, {{x:0, y:0, rotation:0, opacity:1, duration:.5, ease:"back.out(1.4)"}}, {T(ti["t"])});')
        body.append(f'<div class="wall" style="top:{w.get("top",420)}px">{"".join(tiles)}</div>')
        tl.append(f'tl.to("#{sid} .tile", {{opacity:0, duration:.2}}, {endtxt});')
    if sh.get("stack"):
        s = sh["stack"]; rows = []
        for i, r in enumerate(s["rows"]):
            dec = r.get("dec", 0); st = round(r["num"] * 0.4, dec)
            rows.append(f'<div class="row" id="{sid}-sr{i}"><b id="{sid}-sn{i}">{st}</b><span>{esc(r.get("unit",""))} · {esc(r["label"])}</span></div>')
            tl.append(f'(() => {{ const el = document.querySelector("#{sid}-sn{i}"), o = {{v:{st}}}; el.textContent = fmt({st}, {dec}); '
                      f'tl.fromTo("#{sid}-sr{i}", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:.3}}, {T(r["t"])}); '
                      f'tl.fromTo(o, {{v:{st}}}, {{v:{r["num"]}, duration:.8, ease:"power2.out", onUpdate: () => {{ el.textContent = fmt(o.v, {dec}); }}}}, {T(r["t"])}); }})();')
        body.append(f'<div class="stack" style="top:{s.get("top",420)}px">{"".join(rows)}</div>')
        tl.append(f'tl.to("#{sid} .stack", {{opacity:0, duration:.2}}, {endtxt});')
    if sh.get("doc"):
        dc = sh["doc"]; k = 860 / dc["imgW"]
        hls = "".join(f'<div id="{sid}-hl{i}" style="position:absolute;left:12px;right:12px;top:{h["y"]*k:.0f}px;height:{h["h"]*k:.0f}px;background:rgba(242,140,40,.30);border-radius:4px;transform-origin:0 50%"></div>' for i, h in enumerate(dc.get("hl", [])))
        body.append(f'<div style="position:absolute;left:70px;width:860px;top:{dc.get("top",420)}px;height:{dc.get("h",1000)}px;background:#FBFAF7;border-radius:14px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.55)" data-layout-allow-overflow>'
                    f'<div id="{sid}-pg" style="position:absolute;left:0;top:0;width:860px;transform-origin:50% {dc.get("origin",40)}%" data-layout-allow-overflow data-layout-allow-overlap><img src="{dc["img"]}" alt="" style="display:block;width:860px" />{hls}</div></div>')
        for i, h in enumerate(dc.get("hl", [])):
            tl.append(f'tl.fromTo("#{sid}-hl{i}", {{scaleX:0, opacity:0}}, {{scaleX:1, opacity:1, duration:.4, ease:"power2.out"}}, {T(h["t"])});')
        z = dc.get("zoom")
        if z: tl.append(f'tl.fromTo("#{sid}-pg", {{y:0, scale:1}}, {{y:{z["y"]}, scale:{z["scale"]}, duration:{z["d"]}, ease:"power2.inOut"}}, {T(z["t"])});')
    if sh.get("seg"):
        body.append(f'<div class="seg clip" id="{sid}-seg" data-start="{T(0.1)}" data-duration="{round(D - T(0.1),3)}" data-track-index="10" data-layout-allow-occlusion><span id="{sid}-sgt">{esc(sh["seg"])}</span></div>')
        tl.append(f'tl.fromTo("#{sid}-sgt", {{opacity:0}}, {{opacity:1, duration:.25}}, {T(0.1)}); tl.to("#{sid}-sgt", {{opacity:0, duration:.2}}, {endtxt});')
    if sh.get("foot"):
        body.append(f'<p class="foot clip" id="{sid}-ft" data-start="{T(0.1)}" data-duration="{round(D - T(0.1),3)}" data-track-index="11" data-layout-ignore><span id="{sid}-ftt">{esc(sh["foot"])}</span></p>')
        tl.append(f'tl.fromTo("#{sid}-ftt", {{opacity:0}}, {{opacity:1, duration:.25}}, {T(0.1)}); tl.to("#{sid}-ftt", {{opacity:0, duration:.2}}, {endtxt});')
    # ---------- vào shot
    e = sh.get("enter", "T5")
    if e == "T3":
        dirx = 1080 if sh.get("whipDir", "L") == "L" else -1080
        tl.insert(0, f'tl.fromTo("#{sid}-z", {{x:{dirx}, filter:"blur(22px)"}}, {{x:0, filter:"blur(0px)", duration:.26, ease:"power3.out"}}, 0);')
    elif e == "T1":
        tl.insert(0, f'tl.fromTo("#root", {{opacity:0}}, {{opacity:1, duration:{OVER}, ease:"none"}}, 0); tl.fromTo("#{sid}-z", {{scale:1.3, filter:"blur(10px)"}}, {{scale:1, filter:"blur(0px)", duration:.5, ease:"power3.out"}}, 0);')
    elif e == "DIS":
        tl.insert(0, f'tl.fromTo("#root", {{opacity:0}}, {{opacity:1, duration:{OVER + .1}, ease:"none"}}, 0);')
    elif e == "T2":
        body.append(f'<div id="{sid}-plane" style="position:absolute;left:0;top:0">{PLANE_SVG}</div>')
        tl.insert(0, f'tl.fromTo("#{sid}-z", {{scale:1.4, filter:"blur(12px)"}}, {{scale:1, filter:"blur(0px)", duration:.35, ease:"power3.out"}}, .15); '
                     f'tl.fromTo("#{sid}-plane", {{x:-260, y:1500, rotation:45, scale:.8, filter:"blur(2px)"}}, {{x:1150, y:-200, scale:1.8, filter:"blur(6px)", duration:.75, ease:"power1.in"}}, 0);')
    elif e == "T4":
        poly, big = sh["_mask"]
        tl.insert(0, f'tl.fromTo("#{sid}-z", {{clipPath:"polygon({poly})"}}, {{clipPath:"polygon({big})", duration:.95, ease:"power2.inOut"}}, 0);')
        css.append(f"#{sid}-z {{ clip-path: polygon({poly}); }}")
    return f"""<template>
  <style>
{chr(10).join(css)}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
{chr(10).join(body)}
  </div>
  <script>
    (() => {{
      const tl = gsap.timeline({{ paused: true }});
      const fmt = (v, dec) => {{ const [i, d] = v.toFixed(dec).split("."); return i.replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ".") + (d ? "," + d : ""); }};
      {pre}
{chr(10).join("      " + l for l in tl)}
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
""", off

def mask_for(prev, site):
    """Đa giác ranh dự án trên màn hình ở khung cuối của shot bản đồ trước -> và đa giác 'phóng' phủ kín khung."""
    k = prev["keys"][-1]; cx, cy, s = wx(k[2]), wy(k[1]), 2 ** (k[3] - 8)
    pts = [((wx(lng) - cx) * s + 540, (wy(lat) - cy) * s + 960) for lng, lat in site]
    mx_ = sum(p[0] for p in pts) / len(pts); my_ = sum(p[1] for p in pts) / len(pts)
    big = [(mx_ + (x - mx_) * 9, my_ + (y - my_) * 9) for x, y in pts]
    f = lambda ps: ", ".join(f"{x:.0f}px {y:.0f}px" for x, y in ps)
    return f(pts), f(big)

def validate(shots, total):
    msg = []; dur = {MAP: 0, FOOTAGE: 0, DATA: 0}; fxdur = {}
    for i, s in enumerate(shots):
        dur[s["kind"]] += s["dur"]
        fxs = list(dict.fromkeys(s["fx"] + [s.get("enter", "T5").replace("DIS", "T5")]))
        for f in fxs:
            fxdur[f] = fxdur.get(f, 0) + (sum(min(k["d"], s["dur"] - k["t"]) for k in s.get("kw", [])) if f == "F3" else s["dur"])
        if s["dur"] > 6 and not s.get("busy"): msg.append(f"{s['id']}: dài {s['dur']:.1f}s > 6s (đánh dấu busy nếu có yếu tố mới mỗi ≤1,5s)")
        if i:
            pf = shots[i - 1]["fx"] + [shots[i - 1].get("enter", "T5")]
            same = set(fxs) & set(pf) - {"T5", "F1", "F2", "C1", "DOC"}
            if same: msg.append(f"{s['id']}: lặp hiệu ứng {sorted(same)} với shot trước")
    run = 1
    for a, b in zip(shots, shots[1:]):
        run = run + 1 if a["kind"] == b["kind"] else 1
        lim = 2 if b["kind"] == MAP else 3 if b["kind"] == FOOTAGE else 2
        if run > lim: msg.append(f"{b['id']}: {run} shot '{b['kind']}' liên tiếp (tối đa {lim})")
    for f, d in fxdur.items():
        if f[0] in "MFD" and f not in ("F1", "F2") and d > 0.15 * total: msg.append(f"{f}: {d:.0f}s > 15% thời lượng")
    unused = sorted(set([f"M{i}" for i in range(1, 11)] + [f"T{i}" for i in range(1, 6)] + ["F1", "F2", "F3"] + [f"D{i}" for i in range(1, 7)]) - set(fxdur))
    if unused: msg.append(f"chưa dùng: {unused}")
    dis = sum(1 for s in shots if s.get("enter") == "DIS")
    if dis > 3: msg.append(f"cross-dissolve {dis} lần > 3")
    if sum(1 for s in shots if "D4" in s["fx"]) > 2: msg.append("D4 dùng quá 2 lần")
    share = {k: v / total for k, v in dur.items()}
    avg = total / len(shots)
    return msg, share, avg

def main():
    global SAT, GEOJS, VMAP, PTS
    sb = json.load(open(sys.argv[1], encoding="utf-8")); P = sys.argv[2]
    SAT = sb.get("sat", []); GEOJS = open(f"{P}/geo.json").read(); VMAP = open(f"{P}/vmap2.js").read()
    PTS = {k: [round(wx(v[0]), 2), round(wy(v[1]), 2)] for k, v in sb.get("points", {}).items()}
    os.makedirs(f"{P}/compositions", exist_ok=True)
    shots = sb["shots"]; hosts = []; rows = []
    for i, sh in enumerate(shots):
        if sh.get("enter") == "T4":
            sh["_mask"] = mask_for(shots[i - 1], sb["site"])
        h, off = shot_html(sh, P, shots[i - 1] if i else None)
        open(f"{P}/compositions/{sh['id']}.html", "w", encoding="utf-8").write(h)
        st = round(sh["start"] - off, 3)
        hosts.append(f'      <div id="{sh["id"]}" data-composition-id="{sh["id"]}" data-composition-src="compositions/{sh["id"]}.html" data-start="{st}" data-duration="{round(sh["dur"] + off,3)}" '
                     f'data-track-index="{1 + i % 2}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{i + 1}"></div>')
        tc = lambda t: f"{int(t // 60)}:{t % 60:05.2f}"
        rows.append(f"| {sh['id']} | {tc(sh['start'])} | {sh['dur']:.2f} | {sh['kind']} | {' '.join(sh['fx'])} | {sh.get('enter','T5')} | {esc(sh.get('src',''))} |")
    open(f"{P}/index.html", "w", encoding="utf-8").write(f"""<!doctype html>
<html lang="vi">
  <head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
    <script src="{sb.get('gsap','https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js')}"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0E1A2B; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{sb['duration']}" data-width="1080" data-height="1920">
{chr(10).join(hosts)}
      <audio id="mix" class="clip" src="{sb.get('audio','assets/mix.wav')}" data-start="0" data-duration="{sb['duration']}" data-track-index="30" data-volume="1"></audio>
    </div>
    <script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
""")
    msg, share, avg = validate(shots, sb["duration"])
    rep = [f"# Shot list ({len(shots)} shot, trung bình {avg:.2f} s)", "",
           f"Tỉ lệ: bản đồ {share[MAP]*100:.0f}% · footage/render {share[FOOTAGE]*100:.0f}% · thẻ dữ liệu/tài liệu {share[DATA]*100:.0f}%", "",
           "| Shot | Timecode | Dài (s) | Loại | Hiệu ứng | Vào | Nguồn hình |", "|---|---|---|---|---|---|---|"] + rows
    rep += ["", "## Kiểm tra luật", ""] + ([f"- {m}" for m in msg] or ["- Đạt tất cả luật nhịp/lặp/tỉ lệ."])
    open(f"{P}/SHOTLIST.md", "w", encoding="utf-8").write("\n".join(rep))
    print(f"{len(shots)} shot · TB {avg:.2f}s · map {share[MAP]*100:.0f}% footage {share[FOOTAGE]*100:.0f}% data {share[DATA]*100:.0f}%")
    for m in msg: print("  !", m)

if __name__ == "__main__":
    main()
