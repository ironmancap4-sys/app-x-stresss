T0 = 37.3; END = 66.74
ICON = {
 "bld": '<path d="M4 21V5l8-3 8 3v16M9 21v-4h6v4M8 8h.01M12 8h.01M16 8h.01M8 12h.01M12 12h.01M16 12h.01"/>',
 "money": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/>',
 "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.5 12h11l2-8H6.2"/>',
 "ship": '<path d="M3 17l2 4h14l2-4M5 17V11h14v6M9 11V6h6v5M12 3v3"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
 "crane": '<path d="M4 21h8M6 21V4h2M8 4h12l-3 4M8 8h9M14 8v5M13 13h2v2h-2z"/>',
}
# (icon, số, số lẻ, đơn vị, mô tả, tag, hiện, đếm, tag lúc)
ROWS = [
 ("bld", 2076, 0, "doanh nghiệp", "thành lập mới", "vượt 9,26% kế hoạch năm", 37.45, 37.86, 40.8),
 ("money", 8308, 0, "tỷ đồng", "vốn đăng ký mới", None, 42.95, 43.34, None),
 ("cart", 134414, 0, "tỷ đồng", "bán lẻ hàng hoá &amp; dịch vụ", "+19,34%", 46.3, 48.2, 51.3),
 ("ship", 1.37, 2, "tỷ USD", "xuất siêu", None, 53.0, 53.62, None),
 ("globe", 183, 0, "dự án FDI", "còn hiệu lực", "vốn 5,93 tỷ USD", 55.9, 56.42, 58.4),
 ("crane", 772, 0, "dự án trong nước", "còn hiệu lực", "vốn &gt; 264.000 tỷ đồng", 59.9, 60.16, 62.6),
]
def build():
    html, js = [], []
    for i, (ic, num, dec, unit, desc, tag, t_in, t_cnt, t_tag) in enumerate(ROWS, 1):
        a = round(t_in - T0, 2); dur = round(END - T0 - a, 2)
        tg = f'<span class="tag" id="r{i}-tag">{tag}</span>' if tag else ""
        html.append(f'''      <div class="row clip" id="r{i}" data-start="{a}" data-duration="{dur}" data-track-index="3">
        <span class="ic"><svg viewBox="0 0 24 24">{ICON[ic]}</svg></span>
        <span class="l1"><span class="n" id="r{i}-n">0</span><span class="u">{unit}</span></span>
        <span class="l2">{desc}{tg}</span>
      </div>''')
        js.append(f'''      tl.fromTo("#r{i} > *", {{ opacity: 0, x: -50 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "expo.out", stagger: 0.06 }}, {a});
      (() => {{ const el = document.querySelector("#r{i}-n"), o = {{ v: 0 }};
        tl.fromTo(o, {{ v: 0 }}, {{ v: {num}, duration: 1.1, ease: "power2.out", onUpdate: () => {{ el.textContent = fmt(o.v, {dec}); }} }}, {round(t_cnt - T0, 2)}); }})();''')
        if tag:
            js.append(f'      tl.fromTo("#r{i}-tag", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.8)" }}, {round(t_tag - T0, 2)});')
    return "\n".join(html), "\n".join(js)
