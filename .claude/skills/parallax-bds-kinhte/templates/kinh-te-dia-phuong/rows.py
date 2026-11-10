T0 = 37.3; END = 66.74
ICON = {
 "bld": '<path d="M4 21V5l8-3 8 3v16M9 21v-4h6v4M8 8h.01M12 8h.01M16 8h.01M8 12h.01M12 12h.01M16 12h.01"/>',
 "money": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/>',
 "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.5 12h11l2-8H6.2"/>',
 "ship": '<path d="M3 17l2 4h14l2-4M5 17V11h14v6M9 11V6h6v5M12 3v3"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
 "crane": '<path d="M4 21h8M6 21V4h2M8 4h12l-3 4M8 8h9M14 8v5M13 13h2v2h-2z"/>',
}
# (icon, số, số lẻ, đơn vị, mô tả, tăng trưởng, lúc hiện = lúc đọc số, lúc hiện tăng trưởng)
ROWS = [
 ("bld", 2076, 0, "doanh nghiệp", "thành lập mới", "vượt 9,26% kế hoạch năm", 37.86, 40.8),
 ("money", 8308, 0, "tỷ đồng", "vốn đăng ký mới", None, 43.34, None),
 ("cart", 134414, 0, "tỷ đồng", "bán lẻ hàng hoá &amp; dịch vụ", "+19,34%", 48.2, 51.3),
 ("ship", 1.37, 2, "tỷ USD", "xuất siêu", None, 53.62, None),
 ("globe", 183, 0, "dự án FDI", "còn hiệu lực", "vốn 5,93 tỷ USD", 56.42, 58.4),
 ("crane", 772, 0, "dự án trong nước", "còn hiệu lực", "vốn hơn 264.000 tỷ đồng", 60.16, 62.6),
]
def build():
    html, js = [], []
    for i, (ic, num, dec, unit, desc, up, t_in, t_up) in enumerate(ROWS, 1):
        a = round(t_in - T0 - 0.05, 2); dur = round(END - T0 - a, 2)
        upx = f' <span class="up" id="r{i}-up">▲ {up}</span>' if up else ""
        start = round(num * 0.4, dec)
        html.append(f'''      <div class="row clip" id="r{i}" data-start="{a}" data-duration="{dur}" data-track-index="3"><div class="rin">
        <svg class="ic" viewBox="0 0 24 24">{ICON[ic]}</svg>
        <div class="txt"><div class="l1"><span class="n" id="r{i}-n">{start}</span><span class="u">{unit}</span></div><div class="l2">{desc}{upx}</div></div>
      </div></div>''')
        js.append(f'''      tl.fromTo("#r{i} .rin", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }}, {a});
      (() => {{ const el = document.querySelector("#r{i}-n"), o = {{ v: {start} }}; el.textContent = fmt({start}, {dec});
        tl.fromTo(o, {{ v: {start} }}, {{ v: {num}, duration: 0.8, ease: "power2.out", onUpdate: () => {{ el.textContent = fmt(o.v, {dec}); }} }}, {a}); }})();''')
        if up:
            js.append(f'      tl.fromTo("#r{i}-up", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power2.out" }}, {round(t_up - T0, 2)});')
    return "\n".join(html), "\n".join(js)

if __name__ == "__main__":
    # python rows.py  -> sinh src/board.html từ tpl/board.tpl.html
    import os
    D = os.path.dirname(os.path.abspath(__file__))
    h, j = build()
    s = open(f"{D}/tpl/board.tpl.html", encoding="utf-8").read().replace("<!--ROWS-->", h).replace("/*ROWJS*/", j)
    open(f"{D}/src/board.html", "w", encoding="utf-8").write(s)
    print("src/board.html:", len(ROWS), "dòng số liệu")
