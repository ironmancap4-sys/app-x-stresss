import json
J = lambda n: json.load(open(f"maps/{n}.json"))  # metadata từ sat_tiles.py
SAT = []
for n, show in [("sat07", None), ("sat09", [8.2, 8.9]), ("sat11", [10.0, 10.8]), ("sat13", [12.0, 12.8]), ("sat16", [14.2, 15.0])]:
    m = J(n); SAT.append(dict(img=f"assets/maps/{n}_g.jpg", z=m["z"], x0=m["x0"], y0=m["y0"], w=m["w"], h=m["h"], show=show))
OE = (10.9667, 106.6985)
SITE = [[106.69143, 10.964091], [106.694648, 10.966935], [106.700764, 10.970411], [106.703339, 10.969463], [106.704304, 10.965671], [106.702373, 10.964723],
        [106.699476, 10.965671], [106.697867, 10.964091], [106.695614, 10.964723], [106.693361, 10.964091], [106.691751, 10.963143]]
PTS = {"oneera": [106.6985, 10.9666], "site_n": [106.6995, 10.9700], "site_s": [106.6975, 10.9638], "hcm": [106.7009, 10.7769], "taodan": [106.6930, 10.7740],
       "suoitien": [106.8020, 10.8665], "bd_lab": [106.62, 11.18], "hcm_lab": [106.66, 10.80], "p_vas": [106.6962, 10.9656], "p_kindup": [106.6996, 10.9677],
       "p_meret": [106.7022, 10.9688], "site_w": [106.6918, 10.9640], "site_e": [106.7040, 10.9680], "ring_5": [106.6985, 11.0118], "ring_10": [106.6985, 11.0570], "ring_15": [106.6985, 11.1022]}
CBRE = "Nguồn: CBRE Việt Nam qua CafeF, Báo Đầu tư (03/11/2026)"
OES = "Nguồn: CafeF, Báo Đầu tư (11/2026) · ảnh vệ tinh Esri, Maxar"
GE = "Hình ảnh 3D: Google Earth"
R = "Ảnh phối cảnh của chủ đầu tư (qua CafeF)"
def lay(geo, kind, id, w=5, fill=False, len_=True): return {"geo": geo, "kind": kind, "id": id, "w": w, "fill": fill, "len": len_}
SITEL = lambda id: lay("lines:site", "proj", id, 5, True, True)
sh = []
def S(**k): sh.append(k)
# ================= 0:00–0:31 nguồn cung =================
S(id="a01", start=0, dur=2.45, kind="foot", fx=["M1", "D1", "F1"], media="assets/ge/n_dive.mp4", src="Google Earth: lặn từ trên cao xuống TP.HCM + mây tổng hợp", foot=CBRE, enter="T5",
  big={"t": 0.05, "d": 2.3, "num": 6573, "unit": "căn hộ", "label": "mở bán mới · Quý II/2026"}, clouds=[0, 1.1])
S(id="a02", start=2.45, dur=2.6, kind="foot", fx=["F3", "F1"], media="assets/ge/n_hcm.mp4", src="Google Earth: trung tâm TP.HCM", foot=GE, enter="T3",
  kw=[{"t": 0.1, "d": 2.4, "lines": ["*1.934", "NHÀ LIỀN THỔ"], "pos": "mid"}])
S(id="a03", start=5.05, dur=3.05, kind="map", fx=["M10"], src="Bản đồ vector + vệ tinh Esri", seg="TP.HCM mở rộng", enter="T5",
  keys=[[0, 10.80, 106.85, 8.75], [3.05, 10.86, 106.85, 9.0]],
  layers=[lay("prov:TPHCM_cu", "adm", "a03-hcm", 4, True, False), lay("prov:BD_cu", "adm", "a03-bd", 4, True, False), lay("prov:BRVT_cu", "adm", "a03-br", 4, True, False),
          lay("prov:TPHCM_moi", "adm", "a03-moi", 6, False, True)],
  show=[{"id": "a03-hcm", "t": 0.0, "d": .3}, {"id": "a03-bd", "t": 0.25, "d": .3}, {"id": "a03-br", "t": 0.5, "d": .3}],
  hide=[{"id": "a03-hcm-core", "t": 1.9, "d": .5}, {"id": "a03-bd-core", "t": 1.9, "d": .5}, {"id": "a03-br-core", "t": 1.9, "d": .5}],
  draw=[{"id": "a03-moi", "t": 1.6, "d": 0.9}],
  labels=[{"at": "hcm_lab", "lx": -60, "ly": -260, "align": "c", "big": "TP.HCM", "text": "mở rộng", "color": "adm", "t": 2.0, "d": 1.0}])
S(id="a04", start=8.1, dur=4.85, kind="foot", fx=["F3", "F2"], media="assets/ge/n_tdm.mp4", src="Google Earth: Thủ Dầu Một (Bình Dương cũ)", foot=CBRE, enter="T3", whipDir="R",
  kw=[{"t": 0.95, "d": 1.9, "lines": ["QUÝ II", "*2026"], "pos": "mid"}, {"t": 2.9, "d": 1.8, "lines": ["BÁO CÁO", "*CBRE"], "pos": "mid", "accent": "#2FD3E0"}], busy=True)
S(id="a05", start=12.95, dur=3.05, kind="card", fx=["D4"], src="Thẻ số liệu trên nền vệ tinh mờ", foot=CBRE, enter="T3",
  media="assets/maps/sat11_g.jpg", move="push", dim=0.55,
  stack={"t": 0.0, "top": 700, "rows": [{"t": 0.1, "num": 6573, "unit": "căn hộ", "label": "mở bán mới"}, {"t": 0.5, "num": 1934, "unit": "nhà liền thổ", "label": "mở bán mới"}]})
S(id="a06", start=16.0, dur=2.4, kind="map", fx=["M2"], src="Bản đồ vector + vệ tinh Esri", zoomBlur=True, enter="T5",
  keys=[[0, 10.80, 106.85, 8.9], [0.8, 11.10, 106.70, 9.7], [2.4, 11.12, 106.68, 9.85]],
  layers=[lay("prov:BD_cu", "adm", "a06-bd", 5, True, False)], show=[{"id": "a06-bd", "t": 0.3, "d": .4}],
  labels=[{"at": "bd_lab", "lx": 0, "ly": -170, "align": "c", "big": "BÌNH DƯƠNG CŨ", "color": "adm", "t": 0.9, "d": 1.4}])
S(id="a07", start=18.4, dur=4.35, kind="foot", fx=["F3", "F1"], media="assets/ge/n_tdm.mp4", media_start=0.6, src="Google Earth: Thủ Dầu Một", foot=GE, enter="T3",
  kw=[{"t": 0.3, "d": 1.8, "lines": ["*ĐÔNG BẮC", "SIÊU ĐÔ THỊ"], "pos": "mid"}, {"t": 2.2, "d": 2.0, "lines": ["LỆCH", "*HẲN MỘT PHÍA"], "pos": "mid"}], busy=True)
S(id="a08", start=22.75, dur=2.85, kind="map", fx=["D3", "M4"], src="Bản đồ vector + vệ tinh Esri", foot=CBRE, enter="T5",
  keys=[[0, 10.95, 106.75, 9.35], [2.85, 10.97, 106.74, 9.45]],
  layers=[lay("prov:BD_cu", "adm", "a08-bd", 6, True, True)], draw=[{"id": "a08-bd", "t": 0, "d": .8}], show=[{"id": "a08-bd-fill", "t": 0.6, "d": .4}],
  labels=[{"at": "bd_lab", "lx": 0, "ly": 230, "align": "c", "big": "≈ 80%", "text": "căn hộ mới", "small": "đến từ Bình Dương cũ", "color": "adm", "t": 0.15, "d": 2.6}])
S(id="a09", start=25.6, dur=2.5, kind="foot", fx=["F3", "F2"], media="assets/ge/n_street.mp4", src="Google Earth: khu nhà phố thấp tầng, Thuận An", foot=GE, enter="T3", whipDir="R",
  kw=[{"t": 0.1, "d": 2.3, "lines": ["NHÀ LIỀN THỔ:", "*GẦN *NHƯ *KHÔNG"], "pos": "mid"}])
S(id="a10", start=28.1, dur=2.95, kind="map", fx=["D3"], src="Bản đồ vector + vệ tinh Esri", foot=CBRE, enter="T5",
  keys=[[0, 10.82, 106.72, 9.5], [2.95, 10.80, 106.71, 9.6]],
  layers=[lay("prov:TPHCM_cu", "adm", "a10-hcm", 6, True, False)], show=[{"id": "a10-hcm", "t": 0, "d": .3}],
  labels=[{"at": "hcm_lab", "lx": 0, "ly": -300, "align": "c", "big": "100%", "text": "nhà liền thổ mới", "small": "nằm ở TP.HCM cũ", "color": "adm", "t": 0.1, "d": 2.7}])
# ================= 0:31–1:02 định vị dự án =================
S(id="b01", start=31.05, dur=3.65, kind="foot", fx=["F3", "F1"], media="assets/ge/g1.mp4", src="Google Earth: khu công nghiệp Bình Dương cũ", foot=GE, enter="T3",
  kw=[{"t": 0.6, "d": 2.9, "lines": ["VÙNG", "*CÔNG *NGHIỆP"], "pos": "mid"}])
S(id="b02", start=34.7, dur=4.9, kind="map", fx=["M2"], src="Bản đồ + vệ tinh Esri (z9→z16)", zoomBlur=True, enter="T5", busy=True,
  keys=[[0, 10.90, 106.72, 9.6], [1.6, 10.96, 106.70, 11.8], [3.2, 10.9666, 106.6985, 14.6], [4.9, 10.9666, 106.6985, 15.6]],
  layers=[lay("prov:BD_cu", "adm", "b02-bd", 4, False, False)], hide=[{"id": "b02-bd", "t": 1.4, "d": .6}],
  labels=[{"at": "oneera", "lx": 0, "ly": -220, "align": "c", "big": "THUẬN GIAO", "text": "phường", "color": "adm", "t": 3.4, "d": 1.4}],
  kw=[{"t": 0.6, "d": 2.4, "lines": ["NHÀ CÓ ĐẤT?", "*GẦN *NHƯ *KHÔNG"], "pos": "high"}])
S(id="b03", start=39.6, dur=2.5, kind="map", fx=["M4", "D3"], src="Bản đồ + vệ tinh Esri", enter="T5",
  keys=[[0, 10.9666, 106.6985, 15.6], [2.5, 10.9666, 106.6985, 16.4]],
  layers=[SITEL("b03-site")], draw=[{"id": "b03-site", "t": 0.1, "d": 1.0}], show=[{"id": "b03-site-fill", "t": 1.0, "d": .5}],
  labels=[{"at": "site_s", "lx": 0, "ly": 230, "align": "c", "big": "≈ 50 HA", "text": "khu đô thị mới", "color": "proj", "t": 0.9, "d": 1.4}])
S(id="b04", start=42.1, dur=3.1, kind="foot", fx=["T1", "F3", "F2"], media="assets/img/p1.jpg", move="push", focus="55% 50%", src="Ảnh: CafeF 03/11/2026 – lễ khai trương One Era Galleria", foot="Ảnh: CafeF (03/11/2026)", enter="T1",
  kw=[{"t": 0.15, "d": 2.8, "lines": ["*31/10/2026", "KHAI TRƯƠNG"], "pos": "low"}])
S(id="b05", start=45.2, dur=3.2, kind="map", fx=["M5", "M3"], src="Bản đồ + vệ tinh Esri", enter="T3",
  keys=[[0, 10.9666, 106.6985, 15.8], [3.2, 10.9666, 106.6985, 16.0]], tilt=[0, 1.2, 0, 42], orbit=[0, 3.2, -8, 6],
  layers=[SITEL("b05-site")], show=[{"id": "b05-site", "t": 0, "d": .2}], draw=[{"id": "b05-site", "t": 0, "d": .4}],
  ground=[{"at": "oneera", "text": "THUẬN GIAO", "t": 0.6, "d": 2.5}],
  kw=[{"t": 1.8, "d": 1.3, "lines": ["MỞ CỬA", "*ĐÓN *KHÁCH"], "pos": "high"}])
S(id="b06", start=48.4, dur=2.9, kind="foot", fx=["D1", "F1"], media="assets/ge/n_site_low.mp4", src="Google Earth: công trường One Era", foot=GE, enter="T3",
  big={"t": 0.35, "d": 2.4, "num": 357, "unit": "căn", "label": "nhà phố đầu tiên"})
S(id="b07", start=51.3, dur=4.7, kind="map", fx=["M3", "F3"], src="Bản đồ + vệ tinh Esri", enter="T5",
  keys=[[0, 10.9666, 106.6985, 15.7], [4.7, 10.9666, 106.6985, 15.95]], tilt=[0, 1.0, 0, 38], orbit=[0, 4.7, 12, -12],
  layers=[SITEL("b07-site")], show=[{"id": "b07-site", "t": 0, "d": .2}], draw=[{"id": "b07-site", "t": 0, "d": .4}],
  kw=[{"t": 0.25, "d": 2.2, "lines": ["ONE ERA", "*LÀ *GÌ?"], "pos": "high", "accent": "#2FD3E0"}, {"t": 2.6, "d": 2.0, "lines": ["AI", "*ĐỨNG *SAU?"], "pos": "high", "accent": "#2FD3E0"}], busy=True)
S(id="b08", start=56.0, dur=5.9, kind="foot", fx=["F3", "F1"], media="assets/ge/g3.mp4", src="Google Earth: nút giao QL13 – Vành đai 3", foot=GE, enter="T3", whipDir="R",
  kw=[{"t": 0.8, "d": 2.4, "lines": ["*357 CĂN", "CÓ ĐỦ?"], "pos": "mid"}, {"t": 3.3, "d": 2.3, "lines": ["LẤP", "*CHỖ *TRỐNG"], "pos": "mid"}], busy=True)
# ================= 1:02–1:31 quy mô =================
S(id="c01", start=61.9, dur=2.4, kind="map", fx=["M3", "M4"], src="Bản đồ + vệ tinh Esri", enter="T5",
  keys=[[0, 10.9666, 106.6985, 15.5], [2.4, 10.9666, 106.6985, 15.9]], tilt=[0, 2.4, 20, 45], orbit=[0, 2.4, -20, 0],
  layers=[SITEL("c01-site")], draw=[{"id": "c01-site", "t": 0.1, "d": 0.9}], show=[{"id": "c01-site-fill", "t": 0.9, "d": .4}],
  kw=[{"t": 0.1, "d": 2.1, "lines": ["QUY MÔ"], "pos": "high", "accent": "#2FD3E0"}])
S(id="c02", start=64.3, dur=5.6, kind="foot", fx=["D2", "F1"], media="assets/ge/g2.mp4", src="Google Earth: công trường One Era", foot=OES, enter="T3", busy=True,
  bar={"t": 0.2, "d": 5.2, "label": "Quy mô", "value": 49.5, "max": 50, "unit": "ha", "sub": "≈ 70 sân bóng đá tiêu chuẩn", "top": 760})
S(id="c03", start=69.9, dur=2.55, kind="foot", fx=["D1", "F2"], media="assets/img/p7.jpg", move="panL", focus="60% 50%", src="Ảnh phối cảnh CĐT (The Leader)", foot=R, enter="T3", whipDir="R",
  big={"t": 0.5, "d": 1.9, "text": "> 1 TỶ", "unit": "USD", "label": "tổng vốn đầu tư", "pos": "mid"})
S(id="c04", start=72.45, dur=2.75, kind="map", fx=["D3", "M7"], src="Bản đồ + vệ tinh Esri", enter="T5",
  keys=[[0, 10.9666, 106.6985, 16.1], [2.75, 10.9666, 106.6985, 15.8]],
  layers=[SITEL("c04-site")], show=[{"id": "c04-site", "t": 0, "d": .2}], draw=[{"id": "c04-site", "t": 0, "d": .3}],
  labels=[{"at": "site_n", "lx": 0, "ly": -260, "align": "c", "big": "4.039", "text": "sản phẩm", "color": "proj", "t": 0.6, "d": 2.0}])
S(id="c05", start=75.2, dur=2.8, kind="foot", fx=["F3", "F2"], src="Montage ảnh phối cảnh CĐT (CafeF, The Leader)", foot=R, enter="T5",
  montage=[{"t": 0.0, "media": "assets/img/p3.jpg", "word": "NHÀ PHỐ"}, {"t": 0.95, "media": "assets/img/p6.jpg", "word": "SHOPHOUSE"},
           {"t": 1.65, "media": "assets/img/p4.jpg", "word": "BIỆT THỰ"}, {"t": 2.25, "media": "assets/img/p7.jpg", "word": "CĂN HỘ"}])
S(id="c06", start=78.0, dur=3.95, kind="foot", fx=["D1", "F1"], media="assets/ge/n_site_low.mp4", media_start=1.6, src="Google Earth: công trường One Era", foot=OES, enter="T3",
  big={"t": 2.9, "d": 1.0, "num": 25, "unit": "%", "label": "mật độ xây dựng nhà ở", "pos": "mid"},
  kw=[{"t": 0.1, "d": 2.6, "lines": ["MẬT ĐỘ", "*XÂY *DỰNG"], "pos": "high"}])
S(id="c07", start=81.95, dur=4.85, kind="map", fx=["M4", "D3"], src="Bản đồ + vệ tinh Esri", foot=OES, enter="T5", busy=True,
  keys=[[0, 10.9666, 106.6985, 16.2], [4.85, 10.9666, 106.6985, 16.35]],
  layers=[lay("lines:site", "green", "c07-g", 5, True, True)], draw=[{"id": "c07-g", "t": 0.2, "d": 0.9}], show=[{"id": "c07-g-fill", "t": 1.1, "d": .5}],
  labels=[{"at": "site_s", "lx": 0, "ly": 230, "align": "c", "big": "4 m² ĐẤT", "text": "→ chỉ 1 m² xây nhà", "color": "green", "t": 1.9, "d": 2.8}])
S(id="c08", start=86.8, dur=4.5, kind="foot", fx=["F3", "F2"], media="assets/img/p5.jpg", move="panR", focus="40% 50%", src="Ảnh phối cảnh CĐT (CafeF)", foot=R, enter="T3", whipDir="R",
  kw=[{"t": 0.4, "d": 3.9, "lines": ["CÂY XANH", "*TIỆN *ÍCH"], "pos": "low", "accent": "#4ADE80"}])
# ================= 1:31–2:24 chủ đầu tư & đối tác =================
S(id="d01", start=91.3, dur=3.6, kind="card", fx=["D5"], media="assets/ge/g3.mp4", media_start=2.0, dim=0.55, src="Timeline trên nền Google Earth", foot="Nguồn: SGGP, Znews (09/2025), The Leader, CafeF (2026)", enter="T5",
  timeline={"t": 0.0, "y": 960, "events": [{"t": 1.1, "x": 100, "date": "27/09/2025", "text": "khởi công"}, {"t": 1.9, "x": 380, "date": "24/09/2026", "text": "ký với Longfor"},
                                           {"t": 2.5, "x": 650, "date": "31/10/2026", "text": "khai trương"}]})
S(id="d02", start=94.9, dur=5.0, kind="card", fx=["D6"], media="assets/ge/g2.mp4", media_start=3.0, dim=0.6, src="Tường đối tác trên nền Google Earth", foot="Nguồn: SGGP, Znews, The Leader", enter="T3",
  wall={"t": 0, "top": 640, "tiles": [{"t": 0.6, "name": "Kim Oanh Group", "sub": "chủ đầu tư", "hl": True}, {"t": 2.8, "name": "Sumitomo Forestry", "sub": "Nhật Bản"},
                                       {"t": 3.9, "name": "+ 2 đối tác", "sub": "Nhật Bản"}]})
S(id="d03", start=99.9, dur=4.0, kind="foot", fx=["F3", "F1"], media="assets/ge/g2.mp4", media_start=0.0, src="Google Earth: công trường One Era", foot=GE, enter="T3", whipDir="R",
  kw=[{"t": 0.75, "d": 1.25, "lines": ["KUMAGAI", "*GUMI"], "pos": "mid"}, {"t": 2.05, "d": 1.85, "lines": ["NTT URBAN", "*DEVELOPMENT"], "pos": "mid"}], busy=True)
S(id="d04", start=103.9, dur=2.7, kind="map", fx=["M5"], src="Bản đồ + vệ tinh Esri", enter="T5",
  keys=[[0, 10.9666, 106.6985, 16.0], [2.7, 10.9666, 106.6985, 16.25]], tilt=[0, 1.0, 10, 40],
  layers=[SITEL("d04-site")], show=[{"id": "d04-site", "t": 0, "d": .2}], draw=[{"id": "d04-site", "t": 0, "d": .4}],
  ground=[{"at": "oneera", "text": "KINERA", "t": 0.4, "d": 2.2}],
  labels=[{"at": "site_n", "lx": 0, "ly": -280, "align": "c", "text": "nhà phát triển", "color": "proj", "t": 0.9, "d": 1.7}])
S(id="d05", start=106.6, dur=5.7, kind="foot", fx=["F3", "F2"], media="assets/img/p10.jpg", move="pull", focus="62% 40%", src="Ảnh: The Leader 25/09/2026 – lễ ký kết", foot="Ảnh: The Leader (25/09/2026)", enter="T3",
  kw=[{"t": 2.9, "d": 2.6, "lines": ["THÊM MỘT TÊN", "*RẤT *NẶNG *KÝ"], "pos": "low"}], busy=True)
S(id="d06", start=112.3, dur=3.7, kind="foot", fx=["T2", "F2"], media="assets/img/p8.jpg", move="push", focus="58% 45%", src="Ảnh: The Leader 25/09/2026 – ký kết Kinera × Longfor", foot="Ảnh: The Leader (25/09/2026)", enter="T2",
  callouts=[{"x": 700, "y": 760, "lx": 0, "ly": -170, "align": "c", "big": "LONGFOR", "text": "niêm yết Hồng Kông", "color": "adm", "t": 0.5, "d": 3.0}])
S(id="d07", start=116.0, dur=3.1, kind="card", fx=["D3"], src="Ảnh chụp trích đoạn bài The Leader 25/09/2026", foot="Trích nguyên văn theleader.vn (25/09/2026)", enter="T3",
  doc={"img": "assets/doc/doc_sign.png", "imgW": 1400, "top": 420, "h": 980, "hl": [{"y": 1260, "h": 606, "t": 0.6}], "zoom": {"t": 0.2, "d": 1.4, "y": -420, "scale": 1.12}})
S(id="d08", start=119.1, dur=2.65, kind="foot", fx=["F3", "F1"], media="assets/ge/n_hcm.mp4", src="Google Earth: đô thị (minh hoạ quy mô, không phải dự án Longfor)", foot=GE + " · hình minh hoạ", enter="T3", whipDir="R",
  kw=[{"t": 0.3, "d": 2.2, "lines": ["LONGFOR", "*TỪ *1993"], "pos": "mid"}])
S(id="d09", start=121.75, dur=2.65, kind="foot", fx=["D1", "F2"], media="assets/img/p9.jpg", move="panL", focus="40% 50%", src="Ảnh: The Leader 25/09/2026", foot="Nguồn: The Leader (25/09/2026)", enter="T5",
  big={"t": 0.3, "d": 2.2, "num": 1300, "unit": "dự án", "label": "đã phát triển (hơn)"})
S(id="d10", start=124.4, dur=2.6, kind="map", fx=["M7", "D3"], src="Bản đồ + vệ tinh Esri", enter="T5",
  keys=[[0, 10.9666, 106.6985, 13.0], [2.6, 10.9666, 106.6985, 12.6]],
  layers=[SITEL("d10-site")], show=[{"id": "d10-site", "t": 0, "d": .2}], rings=[{"pt": "oneera", "lat": 10.97, "t": 0.2, "km": [1, 2, 3]}],
  labels=[{"at": "oneera", "lx": 0, "ly": -330, "align": "c", "big": "1,1 TRIỆU", "text": "căn Longfor đã bàn giao", "color": "yel", "t": 0.5, "d": 2.0}])
S(id="d11", start=127.0, dur=2.1, kind="card", fx=["D2"], media="assets/ge/n_hcm.mp4", media_start=1.0, dim=0.5, src="So sánh trên nền Google Earth", foot="Tính từ số liệu The Leader, CafeF", enter="T3",
  bar={"t": 0.0, "d": 2.0, "label": "Longfor giao mỗi năm", "value": 30000, "max": 30000, "unit": "căn", "sub": "One Era cả dự án: 4.039 sản phẩm", "top": 780})
S(id="d12", start=129.1, dur=5.9, kind="foot", fx=["D1", "F2"], media="assets/img/p10.jpg", move="panR", focus="35% 45%", src="Ảnh: The Leader 25/09/2026", foot="Nguồn: The Leader (25/09/2026)", enter="T3", whipDir="R", busy=True,
  kw=[{"t": 0.2, "d": 2.2, "lines": ["DOANH SỐ", "*2025"], "pos": "high"}],
  big={"t": 4.4, "d": 1.4, "num": 10, "unit": "tỷ USD", "label": "doanh số bán năm 2025 (gần)"})
S(id="d13", start=135.0, dur=5.6, kind="card", fx=["D6"], media="assets/img/p7.jpg", move="push", dim=0.6, src="Tường đối tác trên nền phối cảnh", foot="Nguồn: The Leader (25/09/2026)", enter="T5", busy=True,
  wall={"t": 0, "top": 600, "tiles": [{"t": 0.2, "name": "Longfor", "sub": "cùng quy hoạch", "hl": True}, {"t": 2.5, "name": "Surbana Jurong", "sub": "tư vấn quy hoạch"},
                                       {"t": 4.6, "name": "Coteccons", "sub": "hạ tầng"}]})
S(id="d14", start=140.6, dur=3.0, kind="card", fx=["D3"], src="Ảnh chụp trích đoạn bài The Leader", foot="Trích nguyên văn theleader.vn (25/09/2026)", enter="T3",
  doc={"img": "assets/doc/doc_leader.png", "imgW": 1400, "top": 420, "h": 980, "hl": [{"y": 1332, "h": 534, "t": 0.6}], "zoom": {"t": 0.1, "d": 1.3, "y": -560, "scale": 1.12}})
# ================= 2:24–2:50 vị trí & kết nối =================
S(id="e01", start=143.6, dur=3.95, kind="foot", fx=["F3", "F1"], media="assets/ge/g3.mp4", media_start=0.5, src="Google Earth: Vành đai 3 cạnh dự án", foot=GE, enter="T5",
  kw=[{"t": 1.7, "d": 2.1, "lines": ["MỘT NỬA", "*CÂU *CHUYỆN"], "pos": "mid"}])
S(id="e02", start=147.55, dur=3.85, kind="map", fx=["M2", "M5"], src="Bản đồ + vệ tinh Esri", zoomBlur=True, enter="T5",
  keys=[[0, 10.92, 106.73, 11.0], [1.0, 10.9666, 106.6985, 14.6], [3.85, 10.9666, 106.6985, 15.5]],
  layers=[SITEL("e02-site")], show=[{"id": "e02-site", "t": 0.8, "d": .3}], draw=[{"id": "e02-site", "t": 0.8, "d": .5}],
  ground=[{"at": "oneera", "text": "VỊ TRÍ", "t": 0.7, "d": 3.0}])
S(id="e03", start=151.4, dur=5.0, kind="map", fx=["M6", "M9"], src="Bản đồ + vệ tinh Esri", foot=OES, enter="T5", busy=True,
  keys=[[0, 10.9650, 106.6995, 15.25], [5.0, 10.9655, 106.6995, 15.15]],
  layers=[SITEL("e03-site"), lay("lines:ql13", "route", "e03-ql", 6), lay("lines:vd3", "route", "e03-vd", 6), lay("lines:mptv", "route", "e03-mp", 6), lay("lines:ntmk", "route", "e03-nt", 5)],
  show=[{"id": "e03-site", "t": 0, "d": .1}], draw=[{"id": "e03-site", "t": 0, "d": .2}, {"id": "e03-ql", "t": 0.2, "d": 1.0}, {"id": "e03-vd", "t": 1.4, "d": 0.9}, {"id": "e03-mp", "t": 2.2, "d": 0.9}, {"id": "e03-nt", "t": 3.8, "d": 0.8}],
  movers=[{"path": "e03-ql", "t": 0.2, "d": 1.4, "icon": "car"}, {"path": "e03-vd", "t": 1.4, "d": 1.3, "icon": "car"}, {"path": "e03-mp", "t": 2.2, "d": 1.3, "icon": "car"}, {"path": "e03-nt", "t": 3.8, "d": 1.1, "icon": "car"}],
  labels=[{"at": "l_ql13", "lx": -120, "ly": -120, "big": "QL13", "color": "route", "t": 0.5, "d": 4.4}, {"at": "l_vd3", "lx": 70, "ly": -150, "big": "VÀNH ĐAI 3", "color": "route", "t": 1.6, "d": 3.3},
          {"at": "l_mptv", "lx": -180, "ly": 130, "align": "c", "text": "Mỹ Phước – Tân Vạn", "color": "route", "t": 2.4, "d": 2.5}, {"at": "l_ntmk", "lx": -60, "ly": 150, "align": "c", "text": "Nguyễn Thị Minh Khai", "color": "route", "t": 3.9, "d": 1.0}])
S(id="e04", start=156.4, dur=3.2, kind="foot", fx=["F3", "F1"], media="assets/ge/n_ql13.mp4", src="Google Earth: Quốc lộ 13 qua dự án", foot=GE, enter="T3",
  kw=[{"t": 1.9, "d": 1.2, "lines": ["2 TUYẾN", "*METRO"], "pos": "mid", "accent": "#E04BD6"}])
S(id="e05", start=159.6, dur=3.7, kind="map", fx=["M6", "M2"], src="Bản đồ + vệ tinh Esri · sơ đồ hướng tuyến minh hoạ", foot="Hướng tuyến metro: sơ đồ minh hoạ theo quy hoạch, không phải bản vẽ tuyến", enter="T5",
  keys=[[0, 10.9666, 106.6985, 13.6], [1.2, 10.875, 106.745, 12.05], [3.7, 10.87, 106.745, 11.9]], zoomBlur=True,
  layers=[SITEL("e05-site")], show=[{"id": "e05-site", "t": 0, "d": .1}],
  links=[{"a": "site_w", "b": "taodan", "bend": 0.12, "kind": "route", "id": "e05-m1", "w": 6}, {"a": "site_e", "b": "suoitien", "bend": -0.15, "kind": "route", "id": "e05-m2", "w": 6}],
  draw=[{"id": "e05-m1", "t": 1.2, "d": 1.2}, {"id": "e05-m2", "t": 2.3, "d": 1.2}],
  movers=[{"path": "e05-m1", "t": 1.2, "d": 1.4, "icon": "train"}, {"path": "e05-m2", "t": 2.3, "d": 1.3, "icon": "train"}],
  labels=[{"at": "taodan", "lx": -40, "ly": 130, "align": "c", "big": "TAO ĐÀN", "color": "route", "t": 1.9, "d": 1.7}, {"at": "suoitien", "lx": -60, "ly": 120, "align": "c", "big": "SUỐI TIÊN", "color": "route", "t": 2.9, "d": 0.8}])
S(id="e06", start=163.3, dur=2.4, kind="foot", fx=["F1", "D3"], media="assets/ge/n_metro.mp4", src="Google Earth: ga Suối Tiên (metro số 1, đang vận hành)", foot=GE, enter="T5",
  callouts=[{"x": 560, "y": 900, "lx": 0, "ly": -200, "align": "c", "big": "SUỐI TIÊN", "text": "ga metro số 1", "color": "route", "t": 0.2, "d": 2.1}])
S(id="e07", start=165.7, dur=4.4, kind="map", fx=["M7", "M3"], src="Bản đồ + vệ tinh Esri", foot=OES, enter="T5", busy=True,
  keys=[[0, 11.02, 106.6985, 12.35], [4.4, 11.02, 106.6985, 12.15]], tilt=[0, 1.2, 0, 30],
  layers=[SITEL("e07-site")], show=[{"id": "e07-site", "t": 0, "d": .1}], rings=[{"pt": "oneera", "lat": 10.97, "t": 0.2, "km": [5, 10, 15]}],
  labels=[{"at": "ring_5", "lx": 0, "ly": -50, "align": "c", "big": "5 KM", "color": "yel", "t": 0.7, "d": 3.5}, {"at": "ring_10", "lx": 0, "ly": -50, "align": "c", "big": "10 KM", "color": "yel", "t": 1.2, "d": 3.0}, {"at": "ring_15", "lx": 0, "ly": -50, "align": "c", "big": "15 KM", "color": "yel", "t": 1.6, "d": 2.6},
          {"at": "oneera", "lx": 0, "ly": 300, "align": "c", "big": "42 HA", "text": "công viên sinh thái liền kề", "color": "green", "t": 0.3, "d": 4.0}])
# ================= 2:50–3:16 tiện ích =================
S(id="f01", start=170.1, dur=2.9, kind="foot", fx=["F3", "F1"], media="assets/ge/n_site_low.mp4", media_start=0.4, src="Google Earth: công trường One Era", foot=GE, enter="T3",
  kw=[{"t": 0.3, "d": 2.5, "lines": ["TIỆN ÍCH", "*CÓ *TÊN"], "pos": "mid", "accent": "#FACC15"}])
S(id="f02", start=173.0, dur=5.5, kind="map", fx=["M8", "M3"], src="Bản đồ + vệ tinh Esri · vị trí ghim minh hoạ", foot="Vị trí ghim minh hoạ trong khu đô thị", enter="T5", busy=True,
  keys=[[0, 10.9666, 106.6985, 16.2], [5.5, 10.9666, 106.6985, 16.35]], tilt=[0, 1.0, 0, 35], orbit=[0, 5.5, -6, 6],
  layers=[SITEL("f02-site")], show=[{"id": "f02-site", "t": 0, "d": .1}], draw=[{"id": "f02-site", "t": 0, "d": .2}],
  pins=[{"at": "p_vas", "text": "VAS Saigon", "t": 0.0, "left": True}, {"at": "p_kindup", "text": "Kindup", "t": 2.7}, {"at": "p_meret", "text": "Meret", "t": 4.6}])
S(id="f03", start=178.5, dur=3.3, kind="foot", fx=["F3", "F2"], media="assets/img/p6.jpg", move="panU", focus="50% 50%", src="Ảnh phối cảnh CĐT (CafeF)", foot=R, enter="T3", whipDir="R",
  kw=[{"t": 1.0, "d": 2.2, "lines": ["TTTM ·", "*VĂN *PHÒNG", "*HẠNG *A"], "pos": "mid", "accent": "#FACC15"}])
S(id="f04", start=181.8, dur=3.8, kind="foot", fx=["D3", "F2"], media="assets/img/p1.jpg", move="panR", focus="20% 50%", src="Ảnh: CafeF 03/11/2026 – khách tham quan", foot="Ảnh: CafeF (03/11/2026)", enter="T3",
  callouts=[{"x": 420, "y": 1040, "lx": 120, "ly": -260, "big": "KHÔNG CHỈ", "text": "đứng nhìn sa bàn", "color": "yel", "t": 1.6, "d": 2.0}])
S(id="f05", start=185.6, dur=1.9, kind="map", fx=["M4"], src="Bản đồ + vệ tinh Esri", enter="T5",
  keys=[[0, 10.9666, 106.6985, 16.6], [1.9, 10.9666, 106.6985, 17.0]],
  layers=[lay("lines:site", "green", "f05-g", 6, True, True)], draw=[{"id": "f05-g", "t": 0, "d": 0.8}], show=[{"id": "f05-g-fill", "t": 0.6, "d": .4}],
  labels=[{"at": "site_n", "lx": 0, "ly": -260, "align": "c", "big": "ONE PARK", "text": "~1 ha", "color": "green", "t": 0.2, "d": 1.6}])
S(id="f06", start=187.5, dur=5.2, kind="foot", fx=["T4", "F3", "F1"], media="assets/ge/g2.mp4", media_start=1.2, src="Google Earth: công trường One Era (One Park)", foot=GE, enter="T4", busy=True,
  kw=[{"t": 0.9, "d": 1.6, "lines": ["QUẢNG TRƯỜNG", "*2 *HỒ *BƠI"], "pos": "mid", "accent": "#4ADE80"}, {"t": 2.6, "d": 2.4, "lines": ["CÀ PHÊ", "*SÂN *CHƠI"], "pos": "mid", "accent": "#4ADE80"}])
S(id="f07", start=192.7, dur=3.7, kind="foot", fx=["D1", "F2"], media="assets/img/p1.jpg", move="pull", focus="85% 50%", src="Ảnh: CafeF 03/11/2026 – ngày khai trương", foot="Nguồn & ảnh: CafeF (03/11/2026)", enter="T3", whipDir="R",
  big={"t": 1.5, "d": 2.1, "num": 2500, "unit": "người", "label": "đến dự ngày khai trương (khoảng)"})
# ================= 3:16–3:49 sản phẩm =================
S(id="g01", start=196.4, dur=3.25, kind="map", fx=["M3", "M5"], src="Bản đồ + vệ tinh Esri", enter="T5",
  keys=[[0, 10.9666, 106.6985, 15.9], [3.25, 10.9666, 106.6985, 16.1]], tilt=[0, 1.0, 0, 40], orbit=[0, 3.25, 10, -6],
  layers=[SITEL("g01-site")], draw=[{"id": "g01-site", "t": 0, "d": .4}], show=[{"id": "g01-site-fill", "t": 0.3, "d": .3}],
  ground=[{"at": "oneera", "text": "CENTRAL DISTRICT", "t": 0.3, "d": 2.8, "size": 70}])
S(id="g02", start=199.65, dur=3.85, kind="foot", fx=["F3", "F2"], media="assets/img/p4.jpg", move="pull", focus="50% 50%", src="Ảnh phối cảnh CĐT (CafeF)", foot=R, enter="T3",
  kw=[{"t": 0.3, "d": 3.3, "lines": ["PHÂN KHU", "*THẤP *TẦNG ĐẦU TIÊN"], "pos": "low", "accent": "#2FD3E0"}])
S(id="g03", start=203.5, dur=4.4, kind="foot", fx=["D3", "F2"], media="assets/img/p3.jpg", move="panR", focus="30% 50%", src="Ảnh phối cảnh CĐT (CafeF)", foot=R, enter="T3", whipDir="R",
  callouts=[{"x": 520, "y": 1000, "lx": 0, "ly": -330, "align": "c", "big": "TOWNHOUSE", "text": "1 trệt · 2 lầu", "color": "proj", "t": 0.5, "d": 2.0},
            {"x": 520, "y": 1000, "lx": 0, "ly": -330, "align": "c", "big": "NHIỆT ĐỚI", "text": "đương đại", "color": "green", "t": 2.6, "d": 1.6}])
S(id="g04", start=207.9, dur=3.55, kind="map", fx=["M9", "M4"], src="Bản đồ + vệ tinh Esri", foot=OES, enter="T5",
  keys=[[0, 10.9680, 106.7010, 16.3], [3.55, 10.9682, 106.7012, 16.45]],
  layers=[lay("lines:canal", "water", "g04-c", 6)], draw=[{"id": "g04-c", "t": 0.1, "d": 1.4}],
  movers=[{"path": "g04-c", "t": 0.3, "d": 3.0, "icon": "boat"}],
  labels=[{"at": "l_canal", "lx": -110, "ly": -120, "big": "KÊNH SUỐI CÁT", "color": "proj", "t": 2.6, "d": 0.9}])
S(id="g05", start=211.45, dur=5.15, kind="foot", fx=["D1", "F1"], media="assets/ge/n_site_low.mp4", media_start=0.0, src="Google Earth: công trường One Era", foot=OES, enter="T3", busy=True,
  kw=[{"t": 0.2, "d": 2.6, "lines": ["DẠO BỘ", "*ĐẠP *XE"], "pos": "high", "accent": "#2FD3E0"}],
  big={"t": 3.7, "d": 1.3, "num": 2.6, "dec": 1, "unit": "km", "label": "dọc hai bờ kênh (khoảng)", "accent": "#2FD3E0"})
S(id="g06", start=216.6, dur=4.5, kind="foot", fx=["F3", "F2"], media="assets/img/p6.jpg", move="panL", focus="70% 50%", src="Ảnh phối cảnh CĐT (CafeF)", foot=R, enter="T3", whipDir="R",
  kw=[{"t": 0.4, "d": 2.0, "lines": ["SHOPHOUSE"], "pos": "high"}, {"t": 2.4, "d": 2.0, "lines": ["+ TẦNG LỬNG", "*Ở *+ *KINH *DOANH"], "pos": "high"}], busy=True)
S(id="g07", start=221.1, dur=3.5, kind="foot", fx=["D3", "F2"], media="assets/img/p5.jpg", move="push", focus="60% 50%", src="Ảnh phối cảnh CĐT (CafeF)", foot=R, enter="T5",
  callouts=[{"x": 540, "y": 1240, "lx": 0, "ly": -170, "align": "c", "big": "2 MẶT TIỀN", "text": "đại lộ nội khu 25 m", "color": "route", "t": 0.2, "d": 3.2}])
S(id="g08", start=224.6, dur=4.5, kind="map", fx=["M3", "D3"], src="Bản đồ + vệ tinh Esri · vị trí minh hoạ", enter="T5",
  keys=[[0, 10.9666, 106.6985, 16.0], [4.5, 10.9666, 106.6985, 16.2]], tilt=[0, 1.0, 0, 40], orbit=[0, 4.5, -10, 10],
  layers=[SITEL("g08-site")], draw=[{"id": "g08-site", "t": 0, "d": .3}], show=[{"id": "g08-site-fill", "t": 0.2, "d": .3}],
  labels=[{"at": "site_n", "lx": 0, "ly": -260, "align": "c", "big": "ONE PARK", "text": "mặt sau shophouse", "color": "green", "t": 1.9, "d": 2.4}])
# ================= 3:49–4:17 lộ trình & kết =================
S(id="h01", start=229.1, dur=5.3, kind="foot", fx=["D2", "F1"], media="assets/ge/g4.mp4", media_start=0.0, src="Google Earth: toàn cảnh khu dự án", foot=OES, enter="T3", busy=True,
  bar={"t": 0.7, "d": 4.5, "label": "Mở màn", "value": 357, "max": 4039, "unit": "căn", "sub": "trong hơn 4.000 sản phẩm", "top": 760})
S(id="h02", start=234.4, dur=5.2, kind="card", fx=["D5"], media="assets/ge/g4.mp4", media_start=5.2, dim=0.55, src="Timeline trên nền Google Earth", foot="Nguồn: CafeF (07/11/2026)", enter="T3", busy=True,
  timeline={"t": 0.0, "y": 960, "events": [{"t": 0.3, "x": 100, "date": "09/2025", "text": "khởi công"}, {"t": 0.9, "x": 380, "date": "10/2026", "text": "khai trương"},
                                           {"t": 3.2, "x": 650, "date": "QUÝ IV/2028", "text": "bàn giao căn đầu tiên"}]})
S(id="h03", start=239.6, dur=7.0, kind="map", fx=["M2", "M7"], src="Bản đồ + vệ tinh Esri", enter="T5", busy=True, zoomBlur=True,
  keys=[[0, 10.9666, 106.6985, 15.8], [2.0, 10.95, 106.70, 12.6], [4.5, 10.85, 106.78, 9.9], [7.0, 10.86, 106.80, 9.55]],
  layers=[lay("prov:BD_cu", "adm", "h03-bd", 5, True, False), lay("prov:TPHCM_cu", "adm", "h03-hcm", 4, False, False), SITEL("h03-site"),
          lay("lines:ql13", "route", "h03-ql", 5), lay("lines:vd3", "route", "h03-vd", 5), lay("lines:canal", "water", "h03-c", 5)],
  links=[{"a": "site_w", "b": "taodan", "bend": 0.12, "kind": "route", "id": "h03-m1", "w": 5}, {"a": "site_e", "b": "suoitien", "bend": -0.15, "kind": "route", "id": "h03-m2", "w": 5}],
  rings=[{"pt": "oneera", "lat": 10.97, "t": 3.0, "km": [10, 20]}],
  show=[{"id": "h03-site", "t": 0, "d": .1}, {"id": "h03-bd", "t": 2.6, "d": .6}, {"id": "h03-hcm", "t": 3.2, "d": .6}],
  draw=[{"id": "h03-site", "t": 0, "d": .2}, {"id": "h03-ql", "t": 0.2, "d": .8}, {"id": "h03-vd", "t": 0.4, "d": .8}, {"id": "h03-c", "t": 0.6, "d": .8}, {"id": "h03-m1", "t": 3.4, "d": 1.0}, {"id": "h03-m2", "t": 3.8, "d": 1.0}],
  kw=[{"t": 1.0, "d": 2.6, "lines": ["KHOẢNG TRỐNG", "*THẤP *TẦNG"], "pos": "high"}, {"t": 4.0, "d": 2.8, "lines": ["PHÉP THỬ", "*CUỐI *CÙNG"], "pos": "high"}])
S(id="h04", start=246.6, dur=3.6, kind="foot", fx=["F3", "F1"], media="assets/ge/n_wide.mp4", src="Google Earth: toàn cảnh Đông Bắc TP.HCM", foot=GE, enter="T5",
  kw=[{"t": 0.6, "d": 2.8, "lines": ["CƯ DÂN", "*ĐẦU *TIÊN"], "pos": "mid"}])
S(id="h05", start=250.2, dur=3.1, kind="foot", fx=["D3", "F2"], media="assets/img/p5.jpg", move="pull", focus="45% 50%", src="Ảnh phối cảnh CĐT (CafeF)", foot=R, enter="DIS",
  callouts=[{"x": 560, "y": 1150, "lx": 0, "ly": -130, "align": "c", "big": "SÁNG ĐÈN", "text": "dãy shophouse đại lộ 25 m", "color": "yel", "t": 0.3, "d": 2.6}])
S(id="h06", start=253.3, dur=4.14, kind="map", fx=["M4", "M5", "F3"], src="Bản đồ + vệ tinh Esri", enter="T5", exit="none",
  keys=[[0, 10.9666, 106.6985, 15.4], [4.14, 10.9666, 106.6985, 15.8]], tilt=[0, 1.5, 0, 38],
  layers=[SITEL("h06-site")], draw=[{"id": "h06-site", "t": 0, "d": 1.0}], show=[{"id": "h06-site-fill", "t": 0.9, "d": .5}],
  ground=[{"at": "oneera", "text": "ONE ERA", "t": 1.0, "d": 3.1}],
  kw=[{"t": 0.2, "d": 3.9, "lines": ["TỪ TRÊN GIẤY", "*ĐẾN *NGƯỜI", "*THẬT *SỐNG"], "pos": "high", "accent": "#2FD3E0"}])
# ===== cân lại tỉ lệ bản đồ / footage / thẻ =====
def R_(id, **k):
    i = next(n for n, x in enumerate(sh) if x["id"] == id); keep = {q: sh[i][q] for q in ("id", "start", "dur")}; sh[i] = dict(keep, **k)
def U_(id, **k): next(x for x in sh if x["id"] == id).update(k)
R_("a01", kind="map", fx=["M1", "D1"], src="Vệ tinh Esri z7→z9 + mây tổng hợp (bay xuyên mây)", foot=CBRE, enter="T5", clouds=[0, 1.5],
   keys=[[0, 10.95, 106.80, 7.4], [2.45, 10.82, 106.76, 9.3]], big={"t": 0.05, "d": 2.3, "num": 6573, "unit": "căn hộ", "label": "mở bán mới · Quý II/2026"})
R_("a05", kind="map", fx=["D4"], src="Bản đồ + vệ tinh Esri", foot=CBRE, enter="T3",
   keys=[[0, 10.86, 106.80, 9.15], [3.05, 10.86, 106.80, 9.35]], layers=[lay("prov:TPHCM_moi", "adm", "a05-moi", 5, True, False)], show=[{"id": "a05-moi", "t": 0, "d": .3, "to": .55}],
   stack={"t": 0.0, "top": 700, "rows": [{"t": 0.1, "num": 6573, "unit": "căn hộ", "label": "mở bán mới"}, {"t": 0.5, "num": 1934, "unit": "nhà liền thổ", "label": "mở bán mới"}]})
U_("b07", fx=["M3", "M5", "D3"], kw=[], ground=[{"at": "oneera", "text": "ONE ERA", "t": 0.25, "d": 4.2}],
   labels=[{"at": "site_n", "lx": 0, "ly": -300, "align": "c", "big": "AI ĐỨNG SAU?", "color": "proj", "t": 2.6, "d": 2.0}])
R_("c06", kind="map", fx=["M3", "D1"], src="Bản đồ + vệ tinh Esri", foot=OES, enter="T3",
   keys=[[0, 10.9666, 106.6985, 15.7], [3.95, 10.9666, 106.6985, 16.0]], tilt=[0, 1.4, 0, 42], orbit=[0, 3.95, 14, -4],
   layers=[SITEL("c06-site")], draw=[{"id": "c06-site", "t": 0.1, "d": 0.8}], show=[{"id": "c06-site-fill", "t": 0.8, "d": .4}],
   ground=[{"at": "oneera", "text": "MẬT ĐỘ", "t": 0.9, "d": 1.8}],
   big={"t": 2.9, "d": 1.0, "num": 25, "unit": "%", "label": "mật độ xây dựng nhà ở", "pos": "mid"})
U_("c06", fx=["M3", "M5", "D1"])
R_("d11", kind="map", fx=["D2"], src="Bản đồ + vệ tinh Esri", foot="Tính từ số liệu The Leader, CafeF", enter="T5",
   keys=[[0, 10.9666, 106.6985, 12.8], [2.1, 10.9666, 106.6985, 12.5]], layers=[SITEL("d11-site")], show=[{"id": "d11-site", "t": 0, "d": .1}],
   bar={"t": 0.0, "d": 2.0, "label": "Longfor giao mỗi năm", "value": 30000, "max": 30000, "unit": "căn", "sub": "One Era cả dự án: 4.039 sản phẩm", "top": 780})
R_("f04", kind="map", fx=["M3", "D3"], src="Bản đồ + vệ tinh Esri", foot=OES, enter="T3",
   keys=[[0, 10.9666, 106.6985, 15.9], [3.8, 10.9666, 106.6985, 16.15]], tilt=[0, 1.0, 15, 38], orbit=[0, 3.8, 10, -10],
   layers=[SITEL("f04-site")], draw=[{"id": "f04-site", "t": 0, "d": .5}], show=[{"id": "f04-site-fill", "t": 0.3, "d": .3, "to": .7}],
   labels=[{"at": "site_n", "lx": 0, "ly": -300, "align": "c", "big": "KHÔNG CHỈ", "text": "đứng nhìn sa bàn", "color": "yel", "t": 1.4, "d": 2.2}])
U_("g04", fx=["M9"])
U_("e07", fx=["M7"], tilt=None)
R_("g05", kind="map", fx=["D1", "M3", "D3"], src="Bản đồ + vệ tinh Esri", foot=OES, enter="T5", busy=True,
   keys=[[0, 10.9680, 106.7010, 16.2], [5.15, 10.9672, 106.7000, 15.8]], tilt=[0, 1.2, 0, 36],
   layers=[SITEL("g05-site"), lay("lines:canal", "water", "g05-c", 7)], show=[{"id": "g05-site", "t": 0, "d": .1}], draw=[{"id": "g05-c", "t": 0.2, "d": 1.6}, {"id": "g05-site", "t": 0, "d": .2}],
   labels=[{"at": "l_canal", "lx": -120, "ly": -170, "big": "DẠO BỘ", "text": "đạp xe ven kênh", "color": "proj", "t": 0.3, "d": 3.1}],
   big={"t": 3.7, "d": 1.3, "num": 2.6, "dec": 1, "unit": "km", "label": "dọc hai bờ kênh (khoảng)", "accent": "#2FD3E0", "pos": "high"})
for x in sh:
    x["fx"] = ["C1" if (f == "D3" and x["kind"] == "foot") else f for f in x["fx"]]
    if x.get("doc"): x["fx"] = ["DOC"]
def KW(id): return next(x for x in sh if x["id"] == id)
KW("a04")["kw"] = KW("a04")["kw"][:1]; KW("a07")["kw"] = KW("a07")["kw"][:1]; KW("b08")["kw"] = KW("b08")["kw"][:1]
KW("f06")["kw"] = KW("f06")["kw"][:1]; KW("h03")["kw"] = KW("h03")["kw"][1:]
for i in ("b02", "b05", "d12"): KW(i)["kw"] = []
U_("c01", kw=[], fx=["M3", "M4", "M5"], ground=[{"at": "oneera", "text": "QUY MÔ", "t": 0.3, "d": 2.0}])
KW("d03")["kw"] = [{"t": 0.7, "d": 3.1, "lines": ["KUMAGAI GUMI", "*NTT *URBAN"], "pos": "mid"}]
KW("g06")["kw"] = [{"t": 0.4, "d": 2.6, "lines": ["SHOPHOUSE", "*+ *TẦNG *LỬNG"], "pos": "high"}]
U_("d08", kw=[], fx=["C1", "F1"], callouts=[{"x": 560, "y": 1000, "lx": 0, "ly": -300, "align": "c", "big": "LONGFOR", "text": "phát triển bất động sản từ 1993", "color": "adm", "t": 0.3, "d": 2.2}])
U_("e01", kw=[], fx=["C1", "F1"], callouts=[{"x": 540, "y": 1050, "lx": 0, "ly": -330, "align": "c", "big": "VỊ TRÍ", "text": "một nửa câu chuyện còn lại", "color": "w", "t": 1.6, "d": 2.2}])
U_("f01", kw=[], fx=["C1", "F1"], callouts=[{"x": 540, "y": 1050, "lx": 0, "ly": -330, "align": "c", "big": "TIỆN ÍCH", "text": "có tên, có thương hiệu", "color": "yel", "t": 0.3, "d": 2.4}])
U_("h04", kw=[], fx=["C1", "F1"], callouts=[{"x": 540, "y": 1080, "lx": 0, "ly": -360, "align": "c", "big": "CƯ DÂN ĐẦU TIÊN", "text": "sẽ trả lời câu hỏi", "color": "w", "t": 0.6, "d": 2.8}])
U_("g02", kw=[], fx=["C1", "F2"], callouts=[{"x": 540, "y": 1100, "lx": 0, "ly": -380, "align": "c", "big": "PHÂN KHU THẤP TẦNG", "text": "đầu tiên của One Era", "color": "proj", "t": 0.3, "d": 3.3}])
U_("f03", kw=[], fx=["C1", "F2"], callouts=[{"x": 540, "y": 1150, "lx": 0, "ly": -400, "align": "c", "big": "TTTM", "text": "văn phòng hạng A", "color": "yel", "t": 0.6, "d": 2.6}])
U_("e04", kw=[], fx=["C1", "F1"], callouts=[{"x": 540, "y": 1100, "lx": 0, "ly": -380, "align": "c", "big": "2 TUYẾN METRO", "text": "theo quy hoạch", "color": "route", "t": 1.0, "d": 2.1}])
KW("c06")["big"].update(t=2.3, d=1.6); KW("b03")["labels"][0].update(t=0.5, d=1.95)
KW("d02")["wall"]["tiles"][2]["t"] = 3.3
# giữ nhãn / số / chú thích đến hết shot để kịp đọc
for x in sh:
    for l in x.get("labels", []) + x.get("callouts", []):
        if l is (x.get("callouts") or [None])[0] and len(x.get("callouts", [])) > 1: continue
        if not any(o is not l and o.get("t", 0) > l["t"] and o.get("at") == l.get("at") and o.get("x") == l.get("x") for o in x.get("labels", []) + x.get("callouts", [])):
            l["d"] = max(l["d"], x["dur"] - l["t"])
    if x.get("big"): x["big"]["d"] = max(x["big"]["d"], x["dur"] - x["big"]["t"])
for x in sh:   # dùng chữ động thì phải khai F3
    if x.get("kw") and "F3" not in x["fx"]: x["fx"].append("F3")
# chữ động: chỉ giữ trên màn hình đủ đọc (≤1,7 s mỗi cụm) để F3 không chiếm >15%
for x in sh:
    for k in x.get("kw", []):
        nw = sum(len(l.split()) for l in k["lines"]); k["d"] = min(k["d"], 3.8 if x["id"] == "h06" else max(2.0, 0.9 + 0.35 * nw))
# không lặp kiểu vào cảnh (ngoài T5) ở hai cảnh liền nhau
for a, b in zip(sh, sh[1:]):
    if b.get("enter", "T5") == a.get("enter", "T5") and b.get("enter") not in ("T5", None): b["enter"] = "T5"
# điểm cắt bám phách nhạc (100 BPM, lệch pha 0,13 s): dịch ≤0,2 s
BEAT0, BP = 0.13, 0.6
for a, b in zip(sh, sh[1:]):
    nb = round(BEAT0 + round((b["start"] - BEAT0) / BP) * BP, 3)
    if abs(nb - b["start"]) <= 0.2 and nb - a["start"] > 1.6:
        a["dur"] = round(nb - a["start"], 3); end = b["start"] + b["dur"]; b["start"] = nb; b["dur"] = round(end - nb, 3)
for a, b in zip(sh, sh[1:]):
    assert abs(a["start"] + a["dur"] - b["start"]) < 1e-6, (a["id"], b["id"], a["start"] + a["dur"], b["start"])
out = {"duration": 257.44, "audio": "assets/mix.wav", "gsap": "assets/lib/gsap.min.js", "sat": SAT, "points": PTS, "site": SITE, "shots": sh}
json.dump(out, open("proj/shots.json", "w"), ensure_ascii=False, indent=1)
print(len(sh), "shots; end", sh[-1]["start"] + sh[-1]["dur"])
