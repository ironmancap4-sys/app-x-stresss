"""Kế hoạch bay — "99% vẫn chưa thông xe": hạ tầng quanh One Era (Vành đai 3, QL13, metro). Phong cách C v2."""
import json, math
M = lambda n: json.load(open(f"maps/{n}.json"))
SAT = []
for n, show in [("w03", None), ("a05", [3.6, 4.6]), ("sat07", [5.6, 6.4]), ("sat09", [8.3, 9.0]), ("sat11", [9.8, 10.6]), ("sat13", [11.8, 12.6]), ("sat16", [14.0, 14.8])]:
    m = M(n); SAT.append(dict(img=f"assets/maps/{n}_g.jpg", z=m["z"], x0=m["x0"], y0=m["y0"], w=m["w"], h=m["h"], show=show))
PTS = {"oneera": [106.6985, 10.9666], "site_n": [106.6995, 10.9702], "east_mid": [106.8406, 10.86], "east_s": [106.8296, 10.80], "tanvan": [106.8319, 10.9038],
       "nhontrach": [106.838, 10.765], "lt_air": [107.035, 10.765], "flow_mid": [106.90, 10.735],
       "tn_sec": [106.495, 10.665], "bd_sec": [106.742, 10.962], "hcm_sec": [106.845, 10.835], "dn_sec": [106.875, 10.735], "ring_w": [106.565, 10.84],
       "ntmk_j": [106.697223, 10.95951], "ql13_mid": [106.7105, 10.905], "ongbo": [106.7125, 10.8755], "todo_mid": [106.713, 10.85], "binhtrieu": [106.7125, 10.826],
       "ql13_lab": [106.705, 10.9515], "vd3_lab": [106.690, 10.9631],
       "a1": [106.665, 11.055], "st_tg": [106.716, 10.968], "st_ap": [106.752, 10.945], "st_da": [106.780, 10.910], "suoitien": [106.8140, 10.8790], "bdst_mid": [106.735, 10.958],
       "benthanh": [106.6983, 10.7712], "m1_mid": [106.7558, 10.8085], "bar25": [106.7480, 10.8160], "bar26": [106.7680, 10.8020],
       "hcm_lab": [106.72, 10.86], "map_note": [106.79, 10.97]}
cam = [
    # 1 · V10 hạ từ mây xuống đoạn phía Đông Vành đai 3
    [0.0, 11.3, 106.90, 7.2, 0, 0], [4.2, 10.86, 106.84, 10.6, 0, 0], [8.0, 10.85, 106.84, 11.85, 18, 0], [15.4, 10.85, 106.84, 11.85, 18, 0],
    # 2 · V2 kéo ra Đông Bắc TP.HCM: tuyến nào cũng đã vẽ xong
    [18.4, 10.88, 106.77, 10.55, 4, -3], [21.4, 10.90, 106.745, 10.3, 0, 0], [24.6, 10.90, 106.745, 10.3, 0, 0],
    # 3 · V1 bay tới One Era, nghiêng ngắn (≤ 4 s) khi tới
    [27.6, 10.948, 106.712, 12.35, 10, 0], [30.4, 10.9666, 106.6985, 14.55, 28, 0], [32.6, 10.9666, 106.6985, 14.9, 44, 5], [34.6, 10.9662, 106.6990, 14.6, 30, 6],
    # 4 · V5 toàn tuyến 76 km — tiến độ từng đoạn bằng vòng tròn tỉ lệ
    [37.2, 10.93, 106.70, 12.3, 12, 3], [40.2, 10.83, 106.69, 11.05, 0, 0], [50.0, 10.83, 106.69, 11.05, 0, 0],
    [53.4, 10.90, 106.822, 11.7, 14, 0], [57.4, 10.90, 106.822, 11.7, 14, 0],
    # 5 · V3 xe chạy Tân Vạn → cầu Nhơn Trạch → sân bay Long Thành (bám đầu tuyến)
    [59.6, 10.86, 106.838, 11.45, 18, 0], [62.2, 10.79, 106.85, 11.0, 14, 0], [64.6, 10.755, 106.95, 10.65, 8, 0], [66.4, 10.762, 106.99, 10.55, 4, 0],
    # 6 · V8 QL13: tô trạng thái hành lang (xong / chờ khởi công)
    [69.2, 10.935, 106.73, 11.6, 0, 0], [72.4, 10.92, 106.712, 12.35, 24, 0], [77.0, 10.92, 106.712, 12.35, 24, 0], [80.4, 10.86, 106.713, 12.35, 24, 0], [86.0, 10.86, 106.713, 12.35, 24, 0],
    # 7 · V9 metro TP mới Bình Dương – Suối Tiên: mốc thời gian trên bản đồ
    [89.4, 10.955, 106.745, 11.2, 10, 0], [98.6, 10.955, 106.745, 11.2, 10, 0], [101.0, 10.885, 106.80, 11.75, 14, 0], [104.2, 10.885, 106.80, 11.75, 14, 0],
    # 8 · V6 cột 3D số lượt khách metro số 1
    [106.6, 10.822, 106.758, 11.65, 26, 0], [112.6, 10.822, 106.758, 11.65, 26, 0],
    # 9 · V4 vòng "từng đợt" quanh One Era
    [115.6, 10.955, 106.708, 12.0, 6, 0], [120.0, 10.955, 106.708, 12.0, 6, 0],
    # 10 · V1 kết: zoom-through phối cảnh One Era → kéo ra thấy mọi lớp
    [123.0, 10.9666, 106.6985, 14.55, 0, 0], [125.3, 10.9666, 106.6985, 14.95, 0, 0], [129.3, 10.94, 106.73, 12.3, 16, 0], [130.6, 10.938, 106.732, 12.1, 20, 2],
]
L = lambda geo, kind, id, w=5, fill=False, ln=True, cls=None: {k: v for k, v in dict(geo=geo, kind=kind, id=id, w=w, fill=fill, len=ln, cls=cls).items() if v is not None}
layers = [L("prov:TPHCM_moi", "adm", "hcm", 5, True, False), L("prov:Đồng Nai", "adm", "dn", 3, True, False), L("prov:Tây Ninh", "adm", "tn", 3, True, False),
          L("lines:vd3_ring", "route", "ring", 6), L("lines:vd3_east", "route", "east", 7), L("lines:flow_lt", "route", "flow", 6), L("lines:ltdg", "route", "ltdg", 5),
          L("lines:ql13_done", "route", "q_done", 7), L("lines:ql13_todo", "route", "q_todo", 6, cls="dash"),
          L("prov:ql13_done_buf", "route", "qb_done", 3, True, False), L("prov:ql13_todo_buf", "yel", "qb_todo", 3, True, False),
          L("lines:metro_bdst", "route", "bdst", 6, cls="dash"), L("lines:metro1", "route", "m1", 6), L("lines:site", "proj", "site", 6, True, True)]
P = lambda p: 5200 * math.sqrt(p / 100)
circles = [{"id": "c_tn", "pt": "tn_sec", "r_m": P(95.6), "kind": "route"}, {"id": "c_hcm", "pt": "hcm_sec", "r_m": P(82.1), "kind": "route"},
           {"id": "c_dn", "pt": "dn_sec", "r_m": P(78.8), "kind": "route"}, {"id": "c_bd", "pt": "bd_sec", "r_m": P(71.7), "kind": "route"}]
rings = [{"id": "rg_wave", "pt": "oneera", "lat": 10.967, "t": 116.0, "km": [1.6, 3.2, 4.8], "out": 121.6}]
movers = [{"path": "flow", "t": 58.6, "d": 7.4, "icon": "car", "out": 67.5}, {"path": "bdst", "t": 90.6, "d": 8.6, "icon": "train", "out": 104.6}]
lab = []
def la(at, t, d, big=None, text="", small="", color="w", lx=0, ly=-260, align="c", xl=False, unit=None, count=None, icon=None, **kw):
    lab.append({k: v for k, v in dict(at=at, t=t, d=d, big=big, text=text, small=small, color=color, lx=lx, ly=ly, align=align, xl=xl, unit=unit, count=count, icon=icon, **kw).items() if v not in (None, "", False) or k == "logo"})
# 1 · V10
la("east_mid", 0.6, 7.0, "99", "17 km cầu cạn phía Đông", color="route", ly=-330, xl=True, unit="%", icon="construction", count={"from": 90, "to": 99})
la("east_mid", 4.2, 2.5, photo="assets/img/vd3_caucan.jpg", text="Ảnh: Dân trí", lx=-250, ly=60, w=480, h=300, lead=False)
la("tanvan", 7.9, 3.6, "1%", "phần việc còn lại", color="yel", lx=-60, ly=-250, icon="hourglass_top")
la("nhontrach", 10.5, 2.6, "30/11", "mốc thông xe", color="yel", lx=-40, ly=-240, icon="calendar_month")
la("east_s", 13.3, 2.1, "THIẾU NHỰA · ĐÁ", "chất lượng cao", color="adm", lx=-60, ly=-220, icon="warning")
# 2 · V2
la("hcm_lab", 16.2, 3.4, "ĐÔNG BẮC TP.HCM", "", color="adm", lx=220, ly=-200, icon="location_city")
la("map_note", 19.5, 5.4, "TRÊN BẢN ĐỒ", "tuyến nào cũng đã vẽ xong", color="route", lx=0, ly=-150, icon="route")
la("hcm_lab", 20.6, 2.5, photo="assets/img/vd3_aerial.jpg", text="Ảnh: Thanh Niên", lx=-150, ly=120, w=480, h=300, lead=False)
la("tanvan", 22.6, 2.4, "NGOÀI THỰC ĐỊA", "mỗi tuyến một vạch", color="adm", lx=-80, ly=180, icon="construction")
# 3 · V1
la("ql13_lab", 28.3, 6.0, "QL13", "", color="route", lx=-120, ly=-170, align="r", icon="add_road")
la("vd3_lab", 29.1, 2.3, "VÀNH ĐAI 3", "", color="route", lx=-20, ly=-320, align="c", icon="add_road")
la("site_n", 31.5, 3.0, "ĐI TỚI ĐÂU?", "bao giờ người dân dùng được", color="w", ly=-430, icon="help")
# 4 · V5
la("hcm_lab", 37.0, 2.5, photo="assets/img/vd3_tanvan2.jpg", text="Ảnh: Dân trí · Vành đai 3", lx=0, ly=60, w=480, h=300, lead=False)
la("hcm_lab", 35.6, 1.9, "76", "chiều dài toàn tuyến", color="route", lx=0, ly=-520, xl=True, unit="km", icon="route", count={"from": 0, "to": 76})
la("hcm_lab", 37.6, 2.1, "> 75.300", "tỷ đồng · tổng mức đầu tư", color="w", lx=0, ly=-520, xl=True, unit="tỷ", icon="payments")
la("hcm_lab", 39.8, 4.6, "81%", "giá trị hợp đồng (10/2026)", color="route", lx=0, ly=-520, xl=True, icon="construction")
la("tn_sec", 45.3, 6.4, "95,6%", "Tây Ninh", color="route", lx=80, ly=-160, align="l", icon="check_circle")
la("hcm_sec", 46.4, 5.3, "82,1%", "TP.HCM", color="route", lx=-60, ly=-210, align="r", icon="construction")
la("dn_sec", 46.9, 4.8, "78,8%", "Đồng Nai", color="route", lx=-60, ly=150, align="r", icon="construction")
la("bd_sec", 48.3, 4.0, "71,7%", "Bình Dương cũ · gần One Era", color="adm", lx=40, ly=-230, align="c", icon="hourglass_top")
la("tanvan", 53.4, 2.5, photo="assets/img/tanvan.jpg", text="Ảnh: SGGP", lx=-160, ly=-80, w=480, h=300, lead=False)
la("tanvan", 55.9, 1.7, "QUÝ I/2027", "một số hạng mục nút giao Tân Vạn", color="yel", lx=-60, ly=-250, icon="calendar_month")
# 5 · V3
la("nhontrach", 60.6, 1.9, "CẦU NHƠN TRẠCH", "sang Đồng Nai", color="route", lx=-60, ly=-200, icon="directions_car")
la("lt_air", 62.6, 4.4, "SÂN BAY LONG THÀNH", "≈ 39 km từ Tân Vạn (đo trên bản đồ)", color="route", lx=-120, ly=-230, icon="flight")
la("tanvan", 57.6, 2.6, "TÂN VẠN", "điểm xuất phát", color="route", lx=60, ly=-220, icon="directions_car")
la("ql13_lab", 66.6, 2.6, "QUỐC LỘ 13", "", color="route", lx=0, ly=-260, icon="add_road")
# 6 · V8
la("ql13_mid", 69.2, 2.3, "> 9 KM · 8 LÀN", "Ông Bố → Nguyễn Thị Minh Khai", color="route", lx=0, ly=-300, align="c", icon="swap_horiz")
la("ql13_mid", 71.6, 2.5, photo="assets/img/ql13.jpg", text="Ảnh: Dân trí", lx=0, ly=-120, w=480, h=280, lead=False)
la("ql13_mid", 75.4, 4.6, "Sở Xây dựng TP.HCM", "dự án qua Bình Dương cũ cơ bản hoàn thành", logo="", mono="SXD", lx=0, ly=-120)
la("todo_mid", 80.9, 5.6, "≈ 6 KM", "phía cầu Bình Triệu · chờ khởi công", color="yel", lx=0, ly=-280, align="c", icon="hourglass_top")
# 7 · V9
la("st_tg", 87.9, 2.5, photo="assets/img/metro1_crowd.jpg", text="Ảnh: SGGP · khách chờ metro số 1", lx=0, ly=-60, w=480, h=300, lead=False)
la("a1", 90.0, 3.6, "CUỐI 2026", "dự kiến khởi công", color="yel", lx=40, ly=-220, icon="calendar_month")
la("bdst_mid", 93.8, 4.4, "≈ 30,7 km", "TP mới Bình Dương – Suối Tiên", color="route", lx=0, ly=-360, align="c", xl=True, icon="subway")
la("suoitien", 100.6, 2.5, photo="assets/img/metro1.jpg", text="Ảnh: SGGP · metro số 1", lx=-220, ly=-330, w=480, h=300, lead=False)
la("suoitien", 102.6, 2.0, "2030", "mục tiêu hoàn thành", color="yel", lx=-60, ly=-220, align="c", icon="calendar_month")
# 8 · V6
la("bar25", 104.6, 2.0, "20,5 triệu", "lượt khách năm 2025", color="w", lx=-40, ly=-400, align="c", icon="groups")
la("bar26", 108.6, 4.2, "8,86", "triệu lượt 1/1–19/5/2026", color="route", lx=60, ly=-300, align="c", xl=True, icon="groups", count={"from": 0, "to": 8.86, "dec": 2})
la("m1_mid", 106.7, 1.8, "Metro số 1", "Bến Thành – Suối Tiên", logo="", mono="M1", lx=0, ly=-640, lead=False)
# 9 · V4
la("oneera", 113.2, 2.3, "TỪNG ĐỢT", "", color="w", lx=0, ly=-640, icon="schedule")
la("oneera", 115.8, 2.5, photo="assets/img/ql13b.jpg", text="Ảnh: Dân trí · QL13", lx=0, ly=60, w=480, h=300, lead=False)
la("oneera", 115.6, 6.0, "QL13", "gần như xong", color="yel", lx=0, ly=-150, icon="check_circle")
la("oneera", 117.6, 4.0, "VÀNH ĐAI 3", "khép dần cuối 2026 – đầu 2027", color="yel", lx=0, ly=-320, icon="trending_up")
la("oneera", 120.3, 2.0, "METRO", "cuối thập kỷ", color="yel", lx=0, ly=-490, icon="subway")
# 10 · V1
la("site_n", 126.1, 4.4, "LĂN BÁNH NĂM NÀO?", "câu hỏi nên hỏi thêm", color="w", lx=70, ly=-300, icon="help")
pins = [{"at": "st_tg", "text": "Thuận Giao", "t": 96.3, "d": 4.0}, {"at": "st_ap", "text": "An Phú", "t": 97.2, "d": 3.1}, {"at": "st_da", "text": "Dĩ An", "t": 98.0, "d": 2.3},
        {"at": "suoitien", "text": "Suối Tiên", "t": 99.8, "d": 0.9, "left": True}, {"at": "binhtrieu", "text": "Cầu Bình Triệu", "t": 82.1, "d": 4.3},
        {"at": "ongbo", "text": "Ông Bố", "t": 70.6, "d": 4.6, "left": True}, {"at": "ntmk_j", "text": "Nguyễn Thị Minh Khai", "t": 71.6, "d": 9.0}]
ground = [{"at": "oneera", "text": "ONE ERA", "t": 30.6, "d": 3.8, "size": 100}, {"at": "oneera", "text": "ONE ERA", "t": 127.2, "d": 3.3, "size": 92}]
ev = []
E = lambda t, act, id, d=.6, **k: ev.append(dict(t=t, act=act, id=id, d=d, **k))
# 1
E(2.8, "draw", "east", 3.0)
# 2
E(15.8, "show", "hcm", .8, to=.9); E(16.0, "show", "hcm-fill", .8, to=.8); E(16.4, "show", "dn", .6, to=.4); E(16.4, "show", "tn", .6, to=.4)
E(19.4, "draw", "ring", 2.0); E(19.6, "dim", "east", .6, to=.55); E(19.8, "draw", "q_done", 1.2); E(20.2, "draw", "q_todo", 1.2); E(20.4, "draw", "bdst", 1.6); E(20.6, "draw", "m1", 1.4)
E(24.6, "dim", "hcm", .8, to=.25); E(24.6, "hide", "dn", .8); E(24.6, "hide", "tn", .8)
for i in ("ring", "q_done", "q_todo", "bdst", "m1"): E(25.4, "dim", i, .8, to=.4)
# 3
E(28.2, "draw", "site", 1.0); E(29.0, "show", "site-fill", .8, to=1)
E(34.8, "show", "ring", .6, to=1); E(34.8, "hide", "site", .8)
# 4
for i in ("q_done", "q_todo", "bdst", "m1"): E(35.0, "hide", i, .6)
E(44.8, "show", "c_tn", .5); E(45.9, "show", "c_hcm", .5); E(46.4, "show", "c_dn", .5); E(47.9, "show", "c_bd", .5)
for i in ("c_tn", "c_hcm", "c_dn", "c_bd"): E(53.0, "hide", i, .6)
E(53.2, "dim", "hcm", .6, to=0)
# 5
E(57.6, "dim", "ring", .6, to=.4); E(58.4, "draw", "flow", 7.2)
E(67.2, "hide", "flow", .6)
# 6
E(68.2, "show", "q_done", .1); E(68.2, "draw", "q_done", 1.6); E(69.0, "show", "qb_done", .1); E(69.0, "show", "qb_done-fill", .8, to=1)
E(79.6, "show", "q_todo", .1); E(79.6, "draw", "q_todo", 1.2); E(80.2, "show", "qb_todo", .1); E(80.2, "show", "qb_todo-fill", .8, to=1)
E(87.0, "hide", "qb_done", .6); E(87.0, "hide", "qb_todo", .6); E(87.2, "dim", "q_done", .6, to=.45); E(87.2, "dim", "q_todo", .6, to=.45)
# 7
E(90.4, "show", "bdst", .1); E(90.4, "draw", "bdst", 8.4); E(99.4, "show", "m1", .1); E(99.4, "draw", "m1", 1.6)
# 8
E(105.0, "grow", "m25", 1.6); E(106.8, "grow", "m26", 1.6)
E(113.0, "grow", "m25", .8, to=0, ease="power2.in"); E(113.0, "grow", "m26", .8, to=0, ease="power2.in")
# 10 — tích luỹ mọi lớp
E(121.8, "show", "site", .1); E(121.8, "draw", "site", .9); E(122.4, "show", "site-fill", .6, to=1)
for i in ("ring", "q_done", "q_todo", "bdst", "m1"): E(126.0, "show", i, .8, to=1)
E(126.2, "show", "hcm", .8, to=.5)
foot = [{"t": 122.9, "d": 2.6, "media": "assets/img/p7.jpg", "move": "push", "focus": "55% 50%", "blend": .6, "src": "phối cảnh One Era (CĐT, qua The Leader)"}]
legend = [{"t": 69.4, "d": 17.2, "top": 330, "items": [["route", "đã mở rộng 8 làn", "check_circle"], ["yel", "chờ khởi công", "hourglass_top"]]},
          {"t": 44.6, "d": 8.4, "top": 330, "items": [["route", "tiến độ từng đoạn (vòng tròn ∝ %)", "construction"]]}]
src = [{"t": 0.8, "d": 14.6, "text": "Nguồn: Dân trí (12/11/2026), Thanh Niên (13/11/2026) · Ảnh: Dân trí · ảnh vệ tinh Esri, Maxar"},
       {"t": 15.8, "d": 9.2, "text": "Ảnh: Thanh Niên · toàn tuyến vẽ theo hướng tuyến gần đúng (minh hoạ)"},
       {"t": 35.0, "d": 22.0, "text": "Nguồn: Dân trí (03/10/2026, báo cáo Chính phủ gửi Quốc hội), Thanh Niên (13/11/2026) · Ảnh: SGGP"},
       {"t": 57.6, "d": 9.0, "text": "Hướng tuyến và cự ly đo trên bản đồ, minh hoạ"},
       {"t": 67.4, "d": 19.6, "text": "Nguồn: CafeF (29/05/2026), Dân trí (13/02/2026) · Ảnh: Dân trí · Sở Xây dựng: huy hiệu chữ (không có logo chính thức tải được)"},
       {"t": 87.4, "d": 17.0, "text": "Nguồn: Tiền Phong (07/09/2026), CafeF/VTV (02/11/2026) · hướng tuyến minh hoạ · Ảnh: SGGP"},
       {"t": 104.8, "d": 8.4, "text": "Nguồn: VnExpress (số liệu HURC đến 19/5/2026), Nhân Dân (2025) · cột 3D tỉ lệ theo số lượt"},
       {"t": 122.6, "d": 7.8, "text": "Ảnh phối cảnh: chủ đầu tư One Era (qua The Leader)"}]
blocks = [{"lng": PTS["bar25"][0], "lat": PTS["bar25"][1], "w": 1500, "d": 1500, "ang": 0, "g": "m25"},
          {"lng": PTS["bar26"][0], "lat": PTS["bar26"][1], "w": 1500, "d": 1500, "ang": 0, "g": "m26"}]
chapters = [
    {"t": 0.0, "name": "99% của 17 km cầu cạn", "V": "V10", "cam": "hạ từ mây (Z 7,2 → 12,1), nghiêng 22°", "layers": "đoạn cầu cạn vẽ dần, thẻ 99%, 1%, 30/11, thiếu nhựa · đá, cửa sổ ảnh"},
    {"t": 15.6, "name": "Trên bản đồ vẽ xong", "V": "V2", "cam": "kéo ra Đông Bắc TP.HCM, về 0°", "layers": "TP.HCM sáng (cam), tỉnh lân cận mờ 40%, mọi tuyến vẽ mờ, cửa sổ ảnh"},
    {"t": 25.1, "name": "One Era giữa QL13 và Vành đai 3", "V": "V1", "cam": "fly-to, nghiêng 44° ≤ 4 s", "layers": "ranh One Era vẽ + phủ, nhãn QL13/VĐ3, câu hỏi"},
    {"t": 34.5, "name": "76 km · 75.300 tỷ · 81%", "V": "V5", "cam": "kéo ra toàn tuyến Z 9,8, lia chậm", "layers": "vòng VĐ3, thẻ 76 km / 75.300 tỷ / 81%, 4 vòng tròn tỉ lệ tiến độ, Tân Vạn"},
    {"t": 57.2, "name": "Tân Vạn → Nhơn Trạch → Long Thành", "V": "V3", "cam": "bám đầu tuyến xuống phía Nam rồi sang Đông", "layers": "tuyến có xe chạy, cầu Nhơn Trạch, sân bay Long Thành"},
    {"t": 66.3, "name": "QL13 đi trước một bước", "V": "V8", "cam": "lia dọc QL13 từ Bắc xuống Nam, nghiêng 24°", "layers": "hành lang tô theo trạng thái + chú giải, thẻ 8 làn, logo, 6 km chờ"},
    {"t": 86.7, "name": "Metro TP mới Bình Dương – Suối Tiên", "V": "V9", "cam": "lia theo hướng tuyến về Suối Tiên", "layers": "tuyến vẽ dần có tàu chạy, mốc cuối 2026 / 2030, ghim ga"},
    {"t": 104.4, "name": "Metro số 1: nhu cầu đã rõ", "V": "V6", "cam": "nghiêng 26 → 33°, quay 12°", "layers": "2 cột 3D theo số lượt, thẻ 8,86 triệu, thẻ tổ chức"},
    {"t": 112.8, "name": "Hạ tầng đến theo từng đợt", "V": "V4", "cam": "về One Era, đẩy nhẹ", "layers": "3 vòng: QL13 · VĐ3 · Metro"},
    {"t": 122.6, "name": "Lăn bánh năm nào?", "V": "V1", "cam": "zoom-through → kéo ra Z 11,85", "layers": "mọi lớp + ranh One Era phát sáng + câu hỏi"}]
assets = [
    {"name": "vd3_caucan.jpg", "url": "https://cdnphoto.dantri.com.vn/3m10PVuksY8HMjdIX7qYR8-OgF0=/thumb_w/1020/2026/11/12/vanhdai3baoquyen-1790704110265-1794486191605.jpg", "res": "1020×680", "used": "0:04.2–0:07.4", "note": "Dân trí 12/11/2026, ảnh Bảo Quyên; cửa sổ ảnh 560 px (không phóng to toàn khung)"},
    {"name": "vd3_aerial.jpg", "url": "https://images2.thanhnien.vn/528068263637045248/2026/8/24/edit-vanh-dai-3-di-qua-vinhome-17875581803371189682545.jpeg", "res": "2560×1707", "used": "0:20.6–0:23.5", "note": "Thanh Niên; watermark góc, không che chủ thể"},
    {"name": "tanvan.jpg", "url": "https://image.sggp.org.vn/w2000/Uploaded/2026/ycwkpcvo/2026_09_20/tvan7-2212-1980.jpg.webp", "res": "1280×642", "used": "0:53.5–0:56.4", "note": "SGGP 20/09/2026, ảnh Quốc Hùng"},
    {"name": "ql13.jpg", "url": "https://cdnphoto.dantri.com.vn/O8q_uoHwgKp-RvcLx_AaAVtsJFk=/thumb_w/1920/2026/02/13/morongquoclo13binhduongxuandoan-edited-1770988718424.jpg", "res": "1920×1280", "used": "1:11.6–1:14.5", "note": "Dân trí 13/02/2026; watermark góc"},
    {"name": "metro1_crowd.jpg", "url": "https://image.sggp.org.vn/w2000/Uploaded/2026/ycwkpcvo/2025_12_18/18metro2-7063-4055.jpg.webp", "res": "1280×960", "used": "1:27.9–1:30.9", "note": "SGGP, ảnh Quốc Hùng"},
    {"name": "metro1.jpg", "url": "https://image.sggp.org.vn/w2000/Uploaded/2026/ycwkpcvo/2025_12_18/18mtro-1280-5109.jpg.webp", "res": "1280×799", "used": "1:40.6–1:43.4", "note": "SGGP, ảnh Quốc Hùng"},
    {"name": "p7.jpg (One Era)", "url": "https://theleader.vn/kim-oanh-group-bat-tay-ong-lon-longfor-quy-hoach-khu-do-thi-one-era-d47799.html", "res": "1920×1143", "used": "2:02.9–2:05.5 (zoom-through)", "note": "phối cảnh CĐT, đã dùng ở video trước"},
    {"name": "Material Symbols Rounded (fill) 0.49.0", "url": "https://registry.npmjs.org/@material-symbols/svg-400", "res": "vector", "used": "mọi huy hiệu", "note": "một họ icon, Apache-2.0"},
    {"name": "HCMC Metro logo.svg", "url": "https://commons.wikimedia.org/wiki/File:HCMC_Metro_logo.svg", "res": "vector", "used": "—", "note": "KHÔNG tải được (upload.wikimedia.org trả 429 nhiều lần) → huy hiệu chữ M1"},
    {"name": "logo Sở Xây dựng TP.HCM", "url": "https://sxd.hochiminhcity.gov.vn/", "res": "—", "used": "—", "note": "trang chính thức không phản hồi (502), không có trên Wikimedia → huy hiệu chữ SXD"},
    {"name": "ảnh vệ tinh", "url": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer", "res": "z3–z16", "used": "toàn video", "note": "Esri, Maxar; làm mờ 0,8 px, tối 20%, giảm bão hoà 15%"},
    {"name": "hình học Vành đai 3 gần Tân Vạn", "url": "https://www.openstreetmap.org/relation/13490968", "res": "vector", "used": "0:00–1:07", "note": "OSM (ODbL); đoạn phía Đông dò trên ảnh vệ tinh; phần còn lại gần đúng"}]
out = {"duration": 130.6, "audio": "assets/mix.wav", "gsap": "assets/lib/gsap.min.js", "sat": SAT, "points": PTS, "blocks": blocks, "blockH": {"m25": 20.5 * 900, "m26": 8.86 * 900},
       "cam": cam, "layers": layers, "links": [], "circles": circles, "rings": rings, "movers": movers, "labels": lab, "pins": pins, "ground": ground, "ev": ev,
       "hud": {"clouds": [0.0, 3.0], "legend": legend, "src": src}, "foot": foot, "cuts": [], "allow_lock": True, "chapters": chapters, "assets": assets,
       "motion_blur": {"shutter": 180, "samples": 16}}
for a, b in zip(cam, cam[1:]): assert b[0] > a[0], (a[0], b[0])
json.dump(out, open("proj/flight.json", "w"), ensure_ascii=False, indent=1)
print(len(cam), "keys", len(lab), "labels", len(ev), "events")
