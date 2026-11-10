#!/usr/bin/env python3
"""scenegen.py — storyboard JSON -> project HyperFrames (dọc 1080×1920) theo hệ thiết kế của skill.

  python scenegen.py storyboard.json <project_dir>

Project cần có sẵn: fonts.css + assets/fonts (design/install_fonts.sh), design.css, vmap.js, vector_map.css, geo.json (nếu có cảnh map),
assets/mix.wav (mix_audio.py). Sinh ra compositions/<id>.html cho từng cảnh + index.html.

storyboard.json:
{ "duration": 257.44, "audio": "assets/mix.wav",
  "scenes": [ { "id": "s01", "start": 0, "dur": 30.9, "type": "map|media|board|doc",
                "enter": "whip|blend|none", "seg": "Nhãn phân đoạn", "foot": "Nguồn ...",
                "anchors": [ {"t": 0.4, "d": 2.5, "pos": "low|mid", "dim": false, "lines": ["Trái tim", "*châu *thổ"]} ],   # *từ = nhấn cam
                ... theo loại cảnh ... } ] }
 map:   "keys": [[t,lat,lng,Z(,carry)]], "layers": [vmap layer...], "rings": [[t0,dur,rmax,ptKey]],
        "labelsA": [{"at","lx","ly","align","text","small","t","d"}], "tagsB": [{"at","dx","dy","text","t","d"}],
        "show": [{"id","t","d","to"}], "hide": [{"id","t","d"}], "draw": [{"id","t","d"}], "dimMap": 0..1
 media: "src", "kind": "video|image", "fit": "cover|frame", "media_start", "kb": [s0,s1,x0,x1,y0,y1],
        "labelsA": [{"x","y","lx","ly","align","text","small","t","d"}] (toạ độ màn hình), "tagsB": [{"x","y","text","t","d"}]
 board: "rows": [{"icon","num","dec","unit","desc","up","big","t","tup"}], "top": 380, "bg": {map...} | {"img": "..."}
 doc:   "img", "imgW", "imgH", "hl": [{"y","h","t"}], "moves": [{"t","d","y","scale"}]
Quy tắc tự áp: chữ tắt hết trước khung chuyển cảnh; whip zoom luôn phóng to; "blend" = hoà 0,4 s từ cảnh trước (cảnh bắt đầu sớm 0,4 s).
"""
import html, json, os, sys

ICONS = {
 "bld": '<path d="M4 21V5l8-3 8 3v16M9 21v-4h6v4M8 8h.01M12 8h.01M16 8h.01M8 12h.01M12 12h.01M16 12h.01"/>',
 "money": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/>',
 "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.5 12h11l2-8H6.2"/>',
 "ship": '<path d="M3 17l2 4h14l2-4M5 17V11h14v6M9 11V6h6v5M12 3v3"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
 "crane": '<path d="M4 21h8M6 21V4h2M8 4h12l-3 4M8 8h9M14 8v5M13 13h2v2h-2z"/>',
 "area": '<path d="M3 3h18v18H3z"/><path d="M3 9h18M9 3v18" opacity=".5"/>',
 "home": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>',
 "apt": '<rect x="5" y="3" width="14" height="18"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2"/>',
 "leaf": '<path d="M5 19c0-9 6-14 15-14 0 9-5 15-14 15"/><path d="M5 19l8-8"/>',
 "cal": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
 "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
 "people": '<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3 20c0-3.5 2.7-6 6-6s6 2.5 6 6M14 20c0-2.6 1.4-4.5 4-4.5s3.5 1.9 3.5 4.5"/>',
 "school": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/>',
 "health": '<path d="M12 21s-8-5-8-11a4.5 4.5 0 0 1 8-3 4.5 4.5 0 0 1 8 3c0 6-8 11-8 11z"/><path d="M12 9v6M9 12h6"/>',
 "shop": '<path d="M3 9l2-5h14l2 5"/><path d="M4 9v11h16V9"/><path d="M3 9h18"/><path d="M9 20v-6h6v6"/>',
 "office": '<rect x="4" y="2" width="16" height="20"/><path d="M8 6h2M14 6h2M8 10h2M14 10h2M8 14h2M14 14h2M11 22v-4h2v4"/>',
 "handshake": '<path d="M2 12l4-4 5 3 3-2 4 3 4-1"/><path d="M6 8l4 9 3-2 2 2 3-3"/>',
 "flag": '<path d="M5 21V3"/><path d="M5 4h11l-2 4 2 4H5"/>',
}

def esc(s): return html.escape(s, quote=False)

def anchor_html(a, i, sid):
    lines = []
    for ln in a["lines"]:
        ws = []
        for w in ln.split():
            if w.startswith("*"): ws.append(f'<em><span class="w">{esc(w[1:])}</span></em>')
            else: ws.append(f'<span class="w">{esc(w)}</span>')
        lines.append('<span class="ln">' + " ".join(ws) + "</span>")
    return (f'<h2 id="{sid}-a{i}" class="anchor {a.get("pos","low")} clip" data-start="{a["t"]}" data-duration="{a["d"]}" '
            f'data-track-index="20">{"".join(lines)}</h2>')

def label_a(l, i, sid, cls, mapped):
    small = f'<small>{esc(l["small"])}</small>' if l.get("small") else ""
    acc = " acc" if l.get("acc") else ""
    if mapped:
        attrs = f'data-at="{l["at"]}" data-lx="{l.get("lx",0)}" data-ly="{l.get("ly",-80)}" data-align="{l.get("align","")}"'
        inner = '<span class="lead"></span><span class="dot"></span><span class="tx">' + esc(l["text"]) + small + "</span>"
        return f'<div id="{sid}-la{i}" class="la{acc} {cls}" {attrs}>{inner}</div>'
    lx, ly = l.get("lx", 0), l.get("ly", -100)
    import math
    al = l.get("align") or ("l" if lx >= 0 else "r")
    gx = 10 if al == "l" else -10 if al == "r" else 0
    tr = {"l": "translate(0,-50%)", "r": "translate(-100%,-50%)", "c": "translate(-50%,-100%)" if ly < 0 else "translate(-50%,0)"}[al]
    return (f'<div id="{sid}-la{i}" class="la{acc}" style="transform: translate({l["x"]}px, {l["y"]}px)">'
            f'<span class="lead" style="width:{math.hypot(lx, ly):.0f}px; transform: rotate({math.atan2(ly, lx):.4f}rad)"></span><span class="dot"></span>'
            f'<span class="tx" style="left:{lx + gx}px; top:{ly}px; transform:{tr}; text-align:{ {"l":"left","r":"right","c":"center"}[al] }">{esc(l["text"])}{small}</span></div>')

def tag_b(t, i, sid, cls, mapped):
    if mapped:
        return f'<div id="{sid}-tb{i}" class="lb {cls}" data-at="{t["at"]}" data-dx="{t.get("dx",0)}" data-dy="{t.get("dy",-120)}"><span>{esc(t["text"])}</span></div>'
    return f'<div id="{sid}-tb{i}" class="lb" style="transform: translate({t["x"]}px, {t["y"]}px)"><span>{esc(t["text"])}</span></div>'

def fmt_js():
    return 'const fmt = (v, dec) => { const [i, d] = v.toFixed(dec).split("."); return i.replace(/\\B(?=(\\d{3})+(?!\\d))/g, ".") + (d ? "," + d : ""); };'

def scene(sc, nxt, P):
    sid, dur, typ = sc["id"], sc["dur"], sc["type"]
    exit_whip = not (nxt and nxt.get("enter") == "blend") and sc.get("exit", "whip") == "whip"
    css = [open(f"{P}/fonts.css").read(), open(f"{P}/design.css").read()]
    body, js, mapjs = [], [], ""
    tl = []  # JS lines
    # --- nền theo loại
    if typ == "map" or (typ == "board" and sc.get("bg", {}).get("keys")):
        m = sc if typ == "map" else sc["bg"]
        css.append(open(f"{P}/vector_map.css").read())
        dim = m.get("dimMap", 0.35 if typ == "board" else 1)
        body.append(f'<div id="{sid}-z" class="zw"><div class="mapbg"></div><div style="position:absolute;inset:0;opacity:{dim}">'
                    f'<svg id="{sid}-map" class="map" width="1080" height="1920" viewBox="0 0 1080 1920" data-layout-allow-overflow><g class="world"></g></svg></div><div class="mapdots"></div>')
        for i, l in enumerate(m.get("labelsA", [])): body.append(label_a(l, i, sid, f"{sid}-lab", True))
        for i, t in enumerate(m.get("tagsB", [])): body.append(tag_b(t, i, sid, f"{sid}-lab", True))
        body.append("</div>")
        mapjs = ("const GEO = " + open(f"{P}/geo.json").read() + ";\n" + open(f"{P}/vmap.js").read() +
                 f'\nconst map = makeMap({json.dumps({"svg": f"#{sid}-map", "id": sid, "labels": f".{sid}-lab", "keys": m["keys"], "layers": m.get("layers", []), "rings": m.get("rings", [])}, ensure_ascii=False)});\n'
                 f'const clock = {{ t: 0 }}; tl.fromTo(clock, {{ t: 0 }}, {{ t: {dur}, duration: {dur}, ease: "none", onUpdate: () => map.apply(clock.t) }}, 0); map.apply(0);')
        for i, l in enumerate(m.get("labelsA", [])):
            tl.append(f'tl.fromTo("#{sid}-la{i} > *", {{opacity:0}}, {{opacity:1, duration:0.35, ease:"power2.out"}}, {l["t"]});')
            tl.append(f'tl.to("#{sid}-la{i} > *", {{opacity:0, duration:0.25, ease:"power1.in"}}, {min(l["t"] + l["d"], dur - 0.45)});')
        for i, t in enumerate(m.get("tagsB", [])):
            tl.append(f'tl.fromTo("#{sid}-tb{i} > span", {{opacity:0, scale:0.85}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(1.6)"}}, {t["t"]});')
            tl.append(f'tl.to("#{sid}-tb{i} > span", {{opacity:0, duration:0.25, ease:"power1.in"}}, {min(t["t"] + t["d"], dur - 0.45)});')
        for s in m.get("show", []):
            tl.append(f'tl.fromTo("#{s["id"]}", {{opacity:0}}, {{opacity:{s.get("to",1)}, duration:{s.get("d",0.5)}, ease:"power2.out"}}, {s["t"]});')
        for s in m.get("hide", []):
            tl.append(f'tl.to("#{s["id"]}", {{opacity:0, duration:{s.get("d",0.4)}, ease:"power1.in"}}, {s["t"]});')
        for s in m.get("draw", []):
            tl.append(f'tl.fromTo("#{s["id"]}", {{strokeDashoffset:100}}, {{strokeDashoffset:0, duration:{s["d"]}, ease:"power1.inOut"}}, {s["t"]});')
    elif typ == "media" or (typ == "board" and sc.get("bg", {}).get("img")):
        m = sc if typ == "media" else sc["bg"]
        src = m.get("src") or m.get("img")
        kind = m.get("kind", "video" if src.endswith(".mp4") else "image")
        fit = m.get("fit", "cover")
        if kind == "video":
            media = (f'<video id="{sid}-v" class="clip" src="{src}" muted playsinline data-start="0" data-duration="{dur}" '
                     f'data-media-start="{m.get("media_start",0)}" data-track-index="1" style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover"></video>')
        elif fit == "frame":
            media = (f'<img src="{src}" alt="" style="position:absolute;left:-60px;top:-60px;width:1200px;height:2040px;object-fit:cover;filter:blur(28px) brightness(0.45) saturate(0.8)" />'
                     f'<div id="{sid}-kb" style="position:absolute;left:0;top:{m.get("frameTop",500)}px;width:1080px;height:{m.get("frameH",700)}px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.5)">'
                     f'<img src="{src}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover" /></div>')
        else:
            media = f'<div id="{sid}-kb" style="position:absolute;inset:0"><img src="{src}" alt="" style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover" /></div>'
        dimc = f'<div style="position:absolute;inset:0;background:rgba(14,26,43,{m.get("dim",0)})"></div>' if m.get("dim") else ""
        body.append(f'<div id="{sid}-z" class="zw">{media}{dimc}<div class="gtop"></div><div class="gbot"></div></div>')
        if m.get("kb") and kind == "image":
            s0, s1, x0, x1, y0, y1 = m["kb"]
            tl.append(f'tl.fromTo("#{sid}-kb", {{scale:{s0}, x:{x0}, y:{y0}}}, {{scale:{s1}, x:{x1}, y:{y1}, duration:{dur}, ease:"none"}}, 0);')
        if typ == "media":
            for i, l in enumerate(m.get("labelsA", [])):
                body.append(label_a(l, i, sid, "", False))
                tl.append(f'tl.fromTo("#{sid}-la{i} > *", {{opacity:0}}, {{opacity:1, duration:0.35}}, {l["t"]});')
                tl.append(f'tl.to("#{sid}-la{i} > *", {{opacity:0, duration:0.25}}, {min(l["t"] + l["d"], dur - 0.45)});')
            for i, t in enumerate(m.get("tagsB", [])):
                body.append(tag_b(t, i, sid, "", False))
                tl.append(f'tl.fromTo("#{sid}-tb{i} > span", {{opacity:0, scale:0.85}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(1.6)"}}, {t["t"]});')
                tl.append(f'tl.to("#{sid}-tb{i} > span", {{opacity:0, duration:0.25}}, {min(t["t"] + t["d"], dur - 0.45)});')
    elif typ == "doc":
        css.append(f'#{sid}-card{{position:absolute;left:70px;width:860px;top:{sc.get("cardTop",380)}px;height:{sc.get("cardH",1040)}px;background:#FBFAF7;border-radius:14px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.5)}}'
                   f'#{sid}-page{{position:absolute;left:0;top:0;width:860px;transform-origin:50% 0}}'
                   f'#{sid}-page img{{display:block;width:860px}} .hl{{position:absolute;left:14px;right:14px;background:rgba(242,140,40,.30);border-radius:4px;transform-origin:0 50%}}')
        k = 860 / sc["imgW"]
        hls = "".join(f'<div class="hl" id="{sid}-hl{i}" style="top:{h["y"]*k:.0f}px;height:{h["h"]*k:.0f}px"></div>' for i, h in enumerate(sc.get("hl", [])))
        body.append(f'<div id="{sid}-z" class="zw"><div class="mapbg"></div><div class="mapdots"></div><div id="{sid}-card" data-layout-allow-overflow>'
                    f'<div id="{sid}-page" data-layout-allow-overflow data-layout-allow-overlap><img src="{sc["img"]}" alt="" />{hls}</div></div></div>')
        for mv in sc.get("moves", []):
            tl.append(f'tl.to("#{sid}-page", {{y:{mv["y"]}, scale:{mv.get("scale",1)}, duration:{mv["d"]}, ease:"power2.inOut"}}, {mv["t"]});')
        for i, h in enumerate(sc.get("hl", [])):
            tl.append(f'tl.fromTo("#{sid}-hl{i}", {{scaleX:0, opacity:0}}, {{scaleX:1, opacity:1, duration:0.45, ease:"power2.out"}}, {h["t"]});')
    elif typ == "board":
        body.append(f'<div id="{sid}-z" class="zw"><div class="mapbg"></div><div class="mapdots"></div></div>')
        css.append(open(f"{P}/vector_map.css").read())
    # --- bảng số
    if typ == "board":
        css.append(f'#{sid}-list{{position:absolute;left:70px;width:860px;top:{sc.get("top",380)}px}}'
                   f'#{sid}-list .row{{position:relative;height:{sc.get("rowH",150)}px;border-top:1px solid rgba(255,255,255,.10)}}#{sid}-list .row:first-child{{border-top:none}}'
                   '.rin{position:absolute;inset:0;display:flex;align-items:center}'
                   '.ic{flex:none;width:44px;height:44px;margin:0 34px 0 8px;fill:none;stroke:var(--accent);stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}'
                   '.l1{white-space:nowrap;line-height:1}.n{font-size:88px;font-weight:800;font-variant-numeric:tabular-nums;letter-spacing:-.01em}'
                   '.big{font-size:50px;font-weight:800;line-height:1.1;white-space:nowrap}'
                   '.u{margin-left:14px;font-size:32px;font-weight:500;color:var(--ink75)}.l2{margin-top:8px;white-space:nowrap;font-size:28px;font-weight:500;color:var(--ink75)}.l2 .up{margin-left:14px}')
        rows = []
        for i, r in enumerate(sc["rows"], 1):
            a = round(r["t"] - 0.05, 2)
            up = f' <span class="up" id="{sid}-r{i}-up">{esc(r["up"])}</span>' if r.get("up") else ""
            if r.get("num") is not None:
                dec = r.get("dec", 0); start = round(r["num"] * 0.4, dec)
                if start <= 0: raise SystemExit(f"{sid}: số {r['num']} quá nhỏ để đếm (sẽ hiện 0) — dùng 'big' thay vì 'num'")
                main = f'<div class="l1"><span class="n" id="{sid}-r{i}-n">{start}</span><span class="u">{esc(r.get("unit",""))}</span></div>'
                tl.append(f'(() => {{ const el = document.querySelector("#{sid}-r{i}-n"), o = {{ v: {start} }}; el.textContent = fmt({start}, {dec}); '
                          f'tl.fromTo(o, {{ v: {start} }}, {{ v: {r["num"]}, duration: 0.8, ease: "power2.out", onUpdate: () => {{ el.textContent = fmt(o.v, {dec}); }} }}, {a}); }})();')
            else:
                main = f'<div class="l1 big">{esc(r["big"])}</div>'
            desc = f'<div class="l2">{esc(r.get("desc",""))}{up}</div>' if (r.get("desc") or up) else ""
            rows.append(f'<div class="row clip" id="{sid}-r{i}" data-start="{a}" data-duration="{round(dur - a, 2)}" data-track-index="5"><div class="rin">'
                        f'<svg class="ic" viewBox="0 0 24 24">{ICONS.get(r.get("icon","chart"))}</svg><div class="txt">{main}{desc}</div></div></div>')
            tl.append(f'tl.fromTo("#{sid}-r{i} .rin", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.35, ease:"expo.out"}}, {a});')
            if r.get("until"):
                tl.append(f'tl.to("#{sid}-r{i} .rin", {{opacity:0, duration:0.25, ease:"power1.in"}}, {r["until"]});')
            if r.get("up"):
                tl.append(f'tl.fromTo("#{sid}-r{i}-up", {{opacity:0}}, {{opacity:1, duration:0.3}}, {r.get("tup", a + 0.6)});')
        body.append(f'<div id="{sid}-list">' + "".join(rows) + "</div>")
        tl.append(f'tl.to("#{sid}-list .rin", {{opacity:0, duration:0.25, ease:"power1.in"}}, {dur - 0.45});')
    # --- nhãn phân đoạn, chân trang, dòng neo
    if sc.get("seg"):
        body.append(f'<div id="{sid}-seg" class="seg clip" data-start="0.15" data-duration="{round(dur - 0.15, 2)}" data-track-index="10" data-layout-allow-occlusion><span id="{sid}-segt">{esc(sc["seg"])}</span></div>')
        tl.append(f'tl.fromTo("#{sid}-segt", {{opacity:0}}, {{opacity:1, duration:0.3}}, 0.15); tl.to("#{sid}-segt", {{opacity:0, duration:0.25}}, {dur - 0.45});')
    if sc.get("foot"):
        body.append(f'<p id="{sid}-foot" class="foot clip" data-start="0.15" data-duration="{round(dur - 0.15, 2)}" data-track-index="11" data-layout-ignore><span id="{sid}-ft">{esc(sc["foot"])}</span></p>')
        tl.append(f'tl.fromTo("#{sid}-ft", {{opacity:0}}, {{opacity:1, duration:0.3}}, 0.2); tl.to("#{sid}-ft", {{opacity:0, duration:0.25}}, {dur - 0.45});')
    for i, a in enumerate(sc.get("anchors", [])):
        if a.get("dim"):
            body.append(f'<div id="{sid}-dim{i}" style="position:absolute;inset:0;background:rgba(14,26,43,.55);opacity:0"></div>')
            tl.append(f'tl.to("#{sid}-dim{i}", {{opacity:1, duration:0.35}}, {a["t"] - 0.1}); tl.to("#{sid}-dim{i}", {{opacity:0, duration:0.3}}, {min(a["t"] + a["d"], dur - 0.45)});')
        body.append(anchor_html(a, i, sid))
        tl.append(f'tl.fromTo("#{sid}-a{i} .w", {{opacity:0, y:18}}, {{opacity:1, y:0, duration:0.3, ease:"expo.out", stagger:0.09}}, {a["t"] + 0.03});')
        tl.append(f'tl.to("#{sid}-a{i} .w", {{opacity:0, duration:0.18, ease:"power1.in"}}, {min(a["t"] + a["d"] - 0.2, dur - 0.45)});')
    # --- vào / ra cảnh
    enter = sc.get("enter", "whip")
    if enter == "whip":
        tl.insert(0, f'tl.fromTo("#{sid}-z", {{scale:1.4, filter:"blur(10px)"}}, {{scale:1, filter:"blur(0px)", duration:0.2, ease:"power3.out"}}, 0);')
    elif enter == "blend":
        tl.insert(0, f'tl.fromTo("#root", {{opacity:0}}, {{opacity:1, duration:0.4, ease:"none"}}, 0);')
    if exit_whip:
        tl.append(f'tl.fromTo("#{sid}-z", {{scale:1, filter:"blur(0px)"}}, {{scale:1.35, filter:"blur(10px)", duration:0.17, ease:"power3.in", immediateRender:false}}, {dur - 0.17});')
    css.append(".zw{position:absolute;inset:0;transform-origin:540px 960px;overflow:hidden}")
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
      {fmt_js()}
      {mapjs}
      {chr(10).join("      " + l for l in tl)}
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
"""

def main():
    sb = json.load(open(sys.argv[1], encoding="utf-8")); P = sys.argv[2]
    os.makedirs(f"{P}/compositions", exist_ok=True)
    scs = sb["scenes"]; hosts = []
    for i, sc in enumerate(scs):
        nxt = scs[i + 1] if i + 1 < len(scs) else None
        open(f"{P}/compositions/{sc['id']}.html", "w", encoding="utf-8").write(scene(sc, nxt, P))
        hosts.append(f'      <div id="{sc["id"]}" data-composition-id="{sc["id"]}" data-composition-src="compositions/{sc["id"]}.html" data-start="{sc["start"]}" '
                     f'data-duration="{sc["dur"]}" data-track-index="{1 + i % 2}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{i + 1}"></div>')
    gsap = sb.get("gsap", "https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js")
    open(f"{P}/index.html", "w", encoding="utf-8").write(f"""<!doctype html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="{gsap}"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0E1A2B; }} #ground {{ position: absolute; inset: 0; background: #0E1A2B; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{sb['duration']}" data-width="1080" data-height="1920">
      <div id="ground"></div>
{chr(10).join(hosts)}
      <audio id="mix" class="clip" src="{sb.get('audio','assets/mix.wav')}" data-start="0" data-duration="{sb['duration']}" data-track-index="30" data-volume="1"></audio>
    </div>
    <script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
""")
    print(f"{len(scs)} cảnh -> {P}/compositions/, index.html")

if __name__ == "__main__":
    main()
