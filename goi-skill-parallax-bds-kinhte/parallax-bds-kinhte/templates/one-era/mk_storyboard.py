import json
SAT16 = {"img": "assets/maps/sat16_g.jpg", "z": 16, "x0": 13359360, "y0": 7873024, "w": 3584, "h": 3072, "id": "sat16"}
SAT13 = {"img": "assets/maps/sat13_g.jpg", "z": 13, "x0": 1669120, "y0": 983296, "w": 2048, "h": 2048, "id": "sat13"}
OE = (10.96725, 106.69948)
CBRE = "Nguồn: CBRE Việt Nam qua CafeF, Báo Đầu tư (03/11/2026)"
OEsrc = "Nguồn: CafeF, Báo Đầu tư (11/2026) · Ảnh vệ tinh: Esri"
def site_layers(extra=()):
    return [dict(SAT16, show=None), {"geo": "lines:site", "cls": "site", "w": 3}] + list(extra)
def L(geo, cls, id, w, len_=True): return {"geo": geo, "cls": cls, "id": id, "w": w, "len": len_}
def sc(**k): return k

S = []
# 1. CBRE: TP.HCM mở rộng -> tách Bình Dương cũ
S.append(sc(id="s01", start=0, dur=30.9, type="board", enter="none", seg="Nguồn cung mới · Quý II/2026", foot=CBRE, top=330, rowH=140,
  rows=[{"icon": "apt", "num": 6573, "unit": "căn hộ", "desc": "mở bán mới, TP.HCM mở rộng", "t": 0.25, "until": 12.6},
        {"icon": "home", "num": 1934, "unit": "nhà liền thổ", "desc": "mở bán mới", "t": 2.55, "until": 12.6}],
  bg={"dimMap": 1, "keys": [[0, 15.8, 106.3, 7.25], [2.4, 10.62, 106.85, 8.95], [12.6, 10.66, 106.85, 9.0], [16.6, 10.9, 106.72, 9.35],
                             [22.5, 10.88, 106.75, 9.3], [27.6, 10.78, 106.78, 9.25], [30.9, 10.88, 106.72, 9.45, True]],
      "layers": [{"geo": "prov:TPHCM_moi", "cls": "region", "id": "s01-moi", "w": 3},
                 {"geo": "prov:TPHCM_cu", "cls": "cmp", "id": "s01-hcm", "w": 2}, {"geo": "prov:BRVT_cu", "cls": "cmp", "id": "s01-brvt", "w": 2},
                 {"geo": "prov:BD_cu", "cls": "vl-glow", "id": "s01-bdg", "w": 14}, {"geo": "prov:BD_cu", "cls": "vl", "id": "s01-bd", "w": 3}],
      "show": [{"id": "s01-moi", "t": 1.2, "d": 0.6}, {"id": "s01-bd", "t": 16.6, "d": 0.5}, {"id": "s01-bdg", "t": 16.6, "d": 0.5, "to": 0.6},
               {"id": "s01-hcm", "t": 13.2, "d": 0.4}, {"id": "s01-brvt", "t": 13.2, "d": 0.4, "to": 0.6}],
      "labelsA": [{"at": "TPHCM_moi", "lx": 0, "ly": -60, "align": "c", "text": "TP.HCM mở rộng", "t": 6.3, "d": 6.2},
                  {"at": "bd_lab", "lx": -40, "ly": -150, "align": "c", "text": "Bình Dương cũ", "small": "nay là Đông Bắc TP.HCM", "acc": True, "t": 17.3, "d": 13},
                  {"at": "hcm", "lx": 150, "ly": 90, "align": "l", "text": "TP.HCM cũ", "t": 13.4, "d": 17}],
      "tagsB": [{"at": "bd_lab", "dx": -40, "dy": 70, "text": "≈80% căn hộ mới", "t": 22.9, "d": 8},
                {"at": "bd_lab", "dx": -40, "dy": 135, "text": "0 nhà liền thổ mới", "t": 26.8, "d": 4},
                {"at": "hcm", "dx": 150, "dy": 200, "text": "100% nhà liền thổ", "t": 28.1, "d": 3}]}))
# 2. vùng công nghiệp
S.append(sc(id="s02", start=30.9, dur=7.0, type="media", src="assets/ge/g1.mp4", seg="Đông Bắc TP.HCM", foot="Hình ảnh 3D: Google Earth · khu công nghiệp Bình Dương cũ",
  anchors=[{"t": 1.0, "d": 5.6, "lines": ["Nhà có đất:", "*gần *như *không *có"]}]))
# 3. bay vào Thuận Giao
S.append(sc(id="s03", start=37.9, dur=4.3, type="map", seg="Phường Thuận Giao", foot="Ảnh vệ tinh: Esri, Maxar",
  keys=[[0, 10.95, 106.72, 9.6], [2.2, 10.966, 106.70, 12.6], [4.3, 10.9673, 106.6995, 14.4, True]],
  layers=[dict(SAT13, show=[10.5, 11.6]), dict(SAT16, show=[13.4, 14.2]), {"geo": "prov:BD_cu", "cls": "vl", "id": "s03-bd", "w": 3}],
  show=[{"id": "s03-bd", "t": 0, "d": 0.01, "to": 1}], hide=[{"id": "s03-bd", "t": 1.2, "d": 0.8}],
  labelsA=[{"at": "oneera", "lx": 90, "ly": -110, "text": "Thuận Giao", "acc": True, "t": 1.6, "d": 2.2}]))
# 4. khai trương
S.append(sc(id="s04", start=42.2, dur=6.3, type="media", src="assets/img/p1.jpg", fit="frame", kb=[1.0, 1.08, 0, -20, 0, -10], seg="Khai trương One Era Galleria", foot="Ảnh: CafeF (03/11/2026)",
  tagsB=[{"x": 540, "y": 470, "text": "31/10/2026 · gần 50 ha", "t": 0.2, "d": 5.6}],
  anchors=[{"t": 2.6, "d": 3.3, "lines": ["Mở cửa", "*đón *khách"]}]))
# 5. công trường + câu hỏi
S.append(sc(id="s05", start=48.5, dur=13.4, type="map", seg="One Era · Thuận Giao", foot=OEsrc,
  keys=[[0, 10.9672, 106.6994, 15.7], [6, 10.9672, 106.6994, 15.95], [13.4, 10.9672, 106.6994, 16.1]],
  layers=site_layers([L("lines:site", "coast-glow", "s05-glow", 14)]),
  draw=[{"id": "s05-glow", "t": 0.1, "d": 1.4}],
  labelsA=[{"at": "oneera", "lx": 0, "ly": -330, "align": "c", "text": "One Era", "small": "khu đô thị ~50 ha", "acc": True, "t": 0.3, "d": 2.7}],
  tagsB=[{"at": "oneera", "dx": 0, "dy": 300, "text": "357 căn nhà phố đầu tiên", "t": 0.3, "d": 2.7}],
  anchors=[{"t": 3.1, "d": 9.8, "pos": "mid", "dim": True, "lines": ["One Era", "là *dự *án *thế *nào?"]}]))
# 6. quy mô
S.append(sc(id="s06", start=61.9, dur=29.3, type="board", seg="Quy mô One Era", foot=OEsrc, top=380,
  rows=[{"icon": "area", "num": 49.5, "dec": 1, "unit": "ha", "desc": "≈ 70 sân bóng đá tiêu chuẩn", "t": 3.8},
        {"icon": "money", "big": "> 1 tỷ USD", "desc": "tổng vốn đầu tư", "t": 9.8},
        {"icon": "home", "num": 4039, "unit": "sản phẩm", "desc": "nhà phố · shophouse · biệt thự · căn hộ", "t": 11.2},
        {"icon": "leaf", "num": 25, "unit": "% mật độ xây dựng nhà ở", "desc": "", "up": "4 m² đất → 1 m² xây nhà", "t": 19.2, "tup": 21.9},
        {"icon": "leaf", "big": "Còn lại: cây xanh, tiện ích", "desc": "và đường nội khu", "t": 25.3}],
  bg={"dimMap": 0.35, "keys": [[0, 10.9672, 106.6994, 15.8], [14, 10.966, 106.700, 16.0], [29.3, 10.9672, 106.6994, 15.85]], "layers": site_layers()}))
# 7. chủ đầu tư & đối tác
S.append(sc(id="s07", start=91.2, dur=21.0, type="board", seg="Đứng sau One Era", foot="Nguồn: Báo SGGP, The Leader, Znews", top=330, rowH=140,
  rows=[{"icon": "cal", "big": "27/09/2025", "desc": "khởi công", "t": 1.3, "until": 17.6},
        {"icon": "flag", "big": "Kim Oanh Group", "desc": "chủ đầu tư", "t": 4.4, "until": 17.6},
        {"icon": "handshake", "big": "Sumitomo Forestry", "desc": "đối tác Nhật Bản", "t": 7.6, "until": 17.6},
        {"icon": "handshake", "big": "Kumagai Gumi", "desc": "đối tác Nhật Bản", "t": 9.5, "until": 17.6},
        {"icon": "handshake", "big": "NTT Urban Development", "desc": "đối tác Nhật Bản", "t": 10.8, "until": 17.6},
        {"icon": "bld", "big": "Kinera", "desc": "nhà phát triển", "t": 13.2, "until": 17.6}],
  anchors=[{"t": 18.2, "d": 2.6, "pos": "mid", "lines": ["Thêm một tên", "*rất *nặng *ký"]}]))
# 8. Longfor ký kết
S.append(sc(id="s08", start=112.2, dur=6.9, type="media", src="assets/img/p8.jpg", fit="frame", kb=[1.0, 1.07, 0, 0, 0, -12], seg="24/09/2026 · Ký kết hợp tác", foot="Ảnh: The Leader (25/09/2026)",
  anchors=[{"t": 0.25, "d": 6.1, "lines": ["*Longfor", "bắt tay Kinera"]}]))
# 9. Longfor số liệu
S.append(sc(id="s09", start=119.1, dur=18.3, type="board", seg="Longfor · niêm yết tại Hồng Kông", foot="Nguồn: The Leader (25/09/2026)", top=380,
  rows=[{"icon": "flag", "big": "1993", "desc": "năm thành lập", "t": 0.9},
        {"icon": "bld", "num": 1300, "unit": "dự án", "desc": "đã phát triển (hơn)", "t": 4.0},
        {"icon": "apt", "num": 1.1, "dec": 1, "unit": "triệu căn", "desc": "đã bàn giao (hơn)", "t": 6.3},
        {"icon": "chart", "num": 30000, "unit": "căn / năm", "desc": "bình quân (hơn)", "t": 9.2},
        {"icon": "money", "num": 10, "unit": "tỷ USD", "desc": "doanh số bán năm 2025 (gần)", "t": 14.6}]))
# 10. tài liệu gốc The Leader
S.append(sc(id="s10", start=137.4, dur=6.2, type="doc", seg="Tài liệu gốc · The Leader 25/09/2026", foot="Trích nguyên văn bài viết trên theleader.vn",
  img="assets/doc/doc_leader.png", imgW=1400, imgH=1985,
  hl=[{"y": 546, "h": 678, "t": 0.5}, {"y": 1332, "h": 534, "t": 1.6}], moves=[{"t": 1.2, "d": 1.6, "y": -180, "scale": 1.02}]))
# 11. Google Earth nút giao
S.append(sc(id="s11", start=143.6, dur=6.3, type="media", src="assets/ge/g3.mp4", seg="Vị trí", foot="Hình ảnh 3D: Google Earth",
  anchors=[{"t": 1.8, "d": 4.0, "lines": ["Nửa còn lại", "nằm ở *vị *trí"]}]))
# 12. giao thông
S.append(sc(id="s12", start=149.9, dur=20.2, type="map", seg="Kết nối giao thông", foot=OEsrc + " · metro theo quy hoạch",
  keys=[[0, 10.9672, 106.6994, 15.55], [8, 10.967, 106.6995, 15.45], [20.2, 10.9675, 106.6995, 15.35]],
  layers=site_layers([L("lines:ql13", "coast-glow", "r-ql13g", 14), L("lines:ql13", "coast", "r-ql13", 5),
                      L("lines:vd3", "coast-glow", "r-vd3g", 14), L("lines:vd3", "coast", "r-vd3", 5),
                      L("lines:mptv", "coast-glow", "r-mptvg", 14), L("lines:mptv", "coast", "r-mptv", 5),
                      L("lines:ntmk", "coast-glow", "r-ntmkg", 12), L("lines:ntmk", "coast", "r-ntmk", 4)]),
  draw=[{"id": i, "t": t, "d": 1.0} for i, t in [("r-ql13g", 1.6), ("r-ql13", 1.6), ("r-vd3g", 2.8), ("r-vd3", 2.8), ("r-mptvg", 3.6), ("r-mptv", 3.6), ("r-ntmkg", 5.2), ("r-ntmk", 5.2)]],
  labelsA=[{"at": "l_ql13", "lx": -110, "ly": -130, "text": "Quốc lộ 13", "t": 2.0, "d": 18},
           {"at": "l_vd3", "lx": -60, "ly": -90, "text": "Vành đai 3", "t": 3.1, "d": 17},
           {"at": "l_mptv", "lx": -200, "ly": 120, "align": "c", "text": "Mỹ Phước – Tân Vạn", "t": 3.9, "d": 16},
           {"at": "l_ntmk", "lx": -60, "ly": -70, "text": "Nguyễn Thị Minh Khai", "t": 5.5, "d": 3.0}],
  tagsB=[{"at": "oneera", "dx": -170, "dy": -330, "text": "Metro TDM – Tao Đàn", "t": 11.4, "d": 8.5},
         {"at": "oneera", "dx": 60, "dy": 300, "text": "Metro TDM – Suối Tiên", "t": 13.6, "d": 6.3},
         {"at": "oneera", "dx": 0, "dy": 380, "text": "Liền kề công viên ~42 ha", "t": 16.1, "d": 3.8}]))
# 13. tiện ích
S.append(sc(id="s13", start=170.1, dur=11.7, type="board", seg="Tiện ích nội khu", foot=OEsrc, top=420,
  rows=[{"icon": "school", "big": "VAS Saigon", "desc": "trường liên cấp", "t": 3.0},
        {"icon": "school", "big": "Kindup", "desc": "mầm non quốc tế", "t": 5.6},
        {"icon": "health", "big": "Meret", "desc": "trung tâm chăm sóc sức khoẻ", "t": 7.5},
        {"icon": "office", "big": "TTTM & văn phòng hạng A", "desc": "", "t": 9.4}],
  bg={"dimMap": 0.35, "keys": [[0, 10.9672, 106.6994, 15.9], [11.7, 10.968, 106.6985, 16.05]], "layers": site_layers()}))
# 14. One Park
S.append(sc(id="s14", start=181.8, dur=7.2, type="media", src="assets/ge/g2.mp4", seg="Đã đi vào hoạt động", foot="Hình ảnh 3D: Google Earth",
  anchors=[{"t": 3.9, "d": 3.0, "lines": ["One Park", "*1 *ha *đã *hoạt *động"]}]))
# 15. 2.500 người
S.append(sc(id="s15", start=189.0, dur=7.4, type="media", src="assets/img/p2.jpg", fit="frame", kb=[1.0, 1.08, 0, 10, 0, 0], seg="Ngày khai trương", foot="Ảnh: CafeF (03/11/2026)",
  tagsB=[{"x": 540, "y": 1380, "text": "≈ 2.500 người đến dự", "t": 3.8, "d": 3.1}]))
# 16. Central District
S.append(sc(id="s16", start=196.4, dur=7.1, type="media", src="assets/img/p4.jpg", fit="frame", kb=[1.0, 1.1, 0, -30, 0, 0], seg="Phân khu Central District", foot="Ảnh phối cảnh của chủ đầu tư (qua CafeF)",
  anchors=[{"t": 0.45, "d": 6.1, "lines": ["Central District", "*357 *căn *thấp *tầng"]}]))
# 17. townhouse
S.append(sc(id="s17", start=203.5, dur=7.9, type="media", src="assets/img/p3.jpg", fit="frame", kb=[1.0, 1.08, 0, 20, 0, 0], seg="Townhouse", foot="Ảnh phối cảnh của chủ đầu tư (qua CafeF)",
  tagsB=[{"x": 540, "y": 470, "text": "1 trệt · 2 lầu", "t": 0.6, "d": 6.8}, {"x": 540, "y": 1380, "text": "Nhiệt đới đương đại", "t": 2.7, "d": 4.7}]))
# 18. kênh Suối Cát
S.append(sc(id="s18", start=211.4, dur=5.5, type="map", seg="Kênh Suối Cát", foot=OEsrc,
  keys=[[0, 10.9675, 106.7005, 16.0], [5.5, 10.9675, 106.7008, 16.15]],
  layers=site_layers([L("lines:canal", "rv-glow", "s18-cg", 16), L("lines:canal", "rv", "s18-c", 5)]),
  draw=[{"id": "s18-cg", "t": 0.3, "d": 1.4}, {"id": "s18-c", "t": 0.3, "d": 1.4}],
  labelsA=[{"at": "l_canal", "lx": 90, "ly": -80, "text": "Kênh Suối Cát", "t": 0.6, "d": 4.4}],
  tagsB=[{"at": "oneera", "dx": 0, "dy": 420, "text": "Dạo bộ, đạp xe ~2,6 km", "t": 3.7, "d": 1.4}]))
# 19. shophouse
S.append(sc(id="s19", start=216.9, dur=4.3, type="media", src="assets/img/p6.jpg", fit="frame", kb=[1.0, 1.06, 0, -10, 0, 0], seg="Shophouse", foot="Ảnh phối cảnh của chủ đầu tư (qua CafeF)",
  tagsB=[{"x": 540, "y": 470, "text": "Thêm tầng lửng: ở + kinh doanh", "t": 0.5, "d": 3.3}]))
# 20. hai mặt tiền
S.append(sc(id="s20", start=221.2, dur=7.9, type="media", src="assets/img/p5.jpg", fit="frame", kb=[1.0, 1.08, 0, 15, 0, 0], seg="Shophouse hai mặt tiền", foot="Ảnh phối cảnh của chủ đầu tư (qua CafeF)",
  tagsB=[{"x": 540, "y": 470, "text": "Đại lộ nội khu 25 m", "t": 3.3, "d": 4.1}, {"x": 540, "y": 1380, "text": "Mặt sau: công viên One Park", "t": 5.4, "d": 2.0}]))
# 21. mở màn & bàn giao
S.append(sc(id="s21", start=229.1, dur=11.2, type="board", seg="Lộ trình", foot=OEsrc, top=420,
  rows=[{"icon": "home", "num": 357, "unit": "căn", "desc": "phần mở màn (Central District)", "t": 0.8},
        {"icon": "apt", "num": 4000, "unit": "sản phẩm", "desc": "toàn khu (hơn)", "t": 4.2},
        {"icon": "cal", "big": "Quý IV/2028", "desc": "dự kiến bàn giao những căn đầu tiên", "t": 8.5}],
  bg={"dimMap": 0.35, "keys": [[0, 10.9672, 106.6994, 16.0], [11.2, 10.9672, 106.6994, 15.8]], "layers": site_layers()}))
# 22. tài liệu gốc CafeF
S.append(sc(id="s22", start=240.3, dur=6.9, type="doc", seg="Tài liệu gốc · CafeF 03/11/2026", foot="Trích nguyên văn bài viết trên cafef.vn",
  img="assets/doc/doc_cafef.png", imgW=1400, imgH=1843,
  hl=[{"y": 546, "h": 678, "t": 0.8}], moves=[{"t": 2.4, "d": 2.5, "y": -40, "scale": 1.05}]))
# 23. kết
S.append(sc(id="s23", start=247.2, dur=10.24, type="media", src="assets/ge/g4.mp4", seg="Phép thử cuối cùng", foot="Hình ảnh 3D: Google Earth", exit="none",
  anchors=[{"t": 6.0, "d": 4.24, "lines": ["Từ trên giấy", "đến *người *thật *sống"]}]))
json.dump({"duration": 257.44, "audio": "assets/mix.wav", "gsap": "assets/lib/gsap.min.js", "scenes": S}, open("storyboard.json", "w"), ensure_ascii=False, indent=1)
print(len(S), "cảnh; kiểm tra liền mạch:", all(abs(a["start"] + a["dur"] - b["start"]) < 1e-6 for a, b in zip(S, S[1:])))
