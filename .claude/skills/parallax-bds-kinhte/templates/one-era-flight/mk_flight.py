"""Kế hoạch bay — One Era · "phép tính 25%" (phong cách C: một camera, một bản đồ)."""
import json
M = lambda n: json.load(open(f"maps/{n}.json"))
SAT = []
for n, show in [("w03", None), ("a05", [3.6, 4.6]), ("sat07", [5.6, 6.4]), ("sat09", [8.3, 9.0]), ("sat11", [9.8, 10.6]), ("sat13", [11.8, 12.6]), ("sat16", [14.0, 14.8])]:
    m = M(n); SAT.append(dict(img=f"assets/maps/{n}_g.jpg", z=m["z"], x0=m["x0"], y0=m["y0"], w=m["w"], h=m["h"], show=show))
OE = [10.9666, 106.6985]; PARK = [10.9652, 106.6962]; CD = [10.9660, 106.6975]; BLVD = [10.96780, 106.69912]
PTS = {"oneera": [106.6985, 10.9666], "site_n": [106.6995, 10.9702], "site_s": [106.6975, 10.9630], "site_w": [106.6928, 10.9652], "site_e": [106.7035, 10.9683],
       "park": [106.6962, 10.9652], "cd": [106.6975, 10.9660], "cd_n": [106.6978, 10.9682], "blvd_mid": [106.69912, 10.96780],
       "hcm": [106.70, 10.78], "hcm_t": [106.70, 10.86], "vn": [106.3, 15.8],
       "atl": [-84.33, 33.80], "dc": [-77.03, 38.90], "ny": [-74.00, 40.71], "hk": [114.17, 22.30], "sg": [103.85, 1.29],
       "hyde": [106.7120, 10.9690], "r400": [106.6962, 10.96882], "r800": [106.6962, 10.97244], "r800w": [106.68888, 10.9652], "q_title": [106.6968, 10.9738],
       "canal_n": [106.70087, 10.97894], "canal_m": [106.70251, 10.96977], "canal_s": [106.70746, 10.96276],
       "p_vas": [106.7008, 10.9690], "p_kind": [106.6992, 10.9679], "p_meret": [106.7026, 10.9674], "p_sport": [106.7032, 10.9659],
       "p_tttm": [106.6948, 10.9648], "p_off": [106.6936, 10.9641], "d1": [106.6930, 10.9650], "d2": [106.7030, 10.9682]}
O = lambda t, z, p=0, b=0, ll=OE: [t, ll[0], ll[1], z, p, b]
cam = [
    # 1 · V2 mở đầu: từ mây xuống Việt Nam → TP.HCM
    [0.0, 13.6, 106.4, 5.2, 0, 0], [3.6, 12.0, 106.6, 6.6, 0, 0], [7.8, 10.86, 106.72, 8.9, 0, 0], [10.6, 10.88, 106.71, 9.5, 12, 0],
    # 2 · V1 bay tới Thuận Giao, vẽ ranh, nghiêng 3D
    [12.6, 10.935, 106.705, 11.3, 18, 0], O(14.8, 14.7, 26), O(17.2, 15.6, 44, -6), O(20.2, 15.85, 48, 4),
    # 3 · V6 khối nhà mọc (25%) → zoom-through phối cảnh
    O(23.4, 16.0, 50, 12), O(27.6, 16.15, 50, 22), O(29.9, 16.9, 40, 24), O(32.6, 17.05, 38, 25),
    # 4 · V8 3/4 khu đất tô xanh, quay chậm
    O(35.2, 16.0, 44, 30), O(40.5, 15.8, 42, 42), O(46.8, 15.45, 30, 48),
    # 5 · V2 Fitwel: thẻ ở dự án → bay ra thế giới → Hoa Kỳ
    O(50.6, 15.1, 12, 22), O(54.0, 15.3, 0, 2), O(56.4, 13.8, 0, 0), [58.6, 24.0, 40.0, 3.25, 0, 0], [61.0, 27.0, -60.0, 3.35, 0, 0],
    [63.6, 37.0, -84.0, 4.45, 0, 0], [66.8, 37.4, -83.0, 4.6, 0, 0],
    # 6 · V4 quay về dự án, vòng đi bộ 5/10 phút quanh One Park
    [69.4, 26.0, -40.0, 3.3, 0, 0], [71.8, 22.0, 60.0, 3.3, 0, 0], [74.0, 11.2, 106.6, 9.8, 0, 0], O(76.4, 15.4, 24, 0, PARK),
    O(81.0, 15.6, 38, 8, PARK), O(85.6, 15.75, 40, 14, PARK), O(89.4, 15.9, 34, 6, PARK),
    # 7 · V3 đi dọc kênh Suối Cát (camera bám đầu tuyến) → One Park → zoom-through
    [91.6, 10.9760, 106.7012, 16.3, 34, 0], [95.0, 10.9720, 106.7020, 16.4, 34, -4], [98.6, 10.9655, 106.7045, 16.4, 34, -8],
    O(102.0, 16.5, 40, -4, PARK), O(104.8, 17.2, 36, 0, PARK), O(108.3, 17.35, 34, 2, PARK),
    # 8 · V5 so diện tích thật: One Park 1 ha · Hyde Park ~42 ha · One Era 49,5 ha
    [111.0, 10.9682, 106.7040, 14.75, 18, 0], [115.4, 10.9684, 106.7045, 14.55, 24, 0],
    # 9 · V7 thả ghim tiện ích, quay chậm
    [118.0, 10.9668, 106.6990, 15.75, 40, -2], [123.5, 10.9668, 106.6990, 15.9, 45, 18], [129.0, 10.9668, 106.6990, 16.0, 45, 30],
    # 10 · V6 357 căn Central District → zoom-through nhà phố → đại lộ 25 m
    O(133.5, 16.2, 46, 34, CD), O(138.8, 16.45, 48, 24, CD), O(143.8, 16.6, 46, 18, CD), O(145.6, 17.3, 38, 16, CD), O(147.4, 17.45, 38, 13, [10.9662, 106.6977]),
    O(150.4, 16.5, 46, 12, BLVD), O(154.0, 16.7, 46, 8, BLVD), O(156.6, 17.35, 38, 6, BLVD),
    # 11 · V8 điểm nóng người đi bộ → "hạ tầng thương mại"
    O(159.8, 17.5, 36, 1, BLVD), O(163.0, 16.4, 44, 0, PARK), O(170.0, 16.3, 42, -12, PARK), O(178.5, 16.1, 46, -22, PARK), O(186.6, 15.5, 34, -12, PARK),
    # 12 · V3 Longfor (Hồng Kông) → dự án
    O(189.6, 14.6, 16, 0), [192.6, 14.5, 108.5, 6.3, 0, 0], [196.0, 15.5, 109.5, 5.35, 0, 0], [205.0, 15.8, 109.8, 5.6, 0, 0], [212.8, 16.2, 110.0, 5.8, 0, 0],
    # 13 · V10 thẻ đối tác: Singapore → về Việt Nam
    [216.2, 5.6, 105.0, 5.85, 0, 0], [220.6, 4.6, 104.8, 6.0, 0, 0], [223.8, 10.6, 106.6, 8.6, 0, 0], O(226.6, 14.9, 20, 0),
    # 14 · V9 các mốc thời gian trên bản đồ
    O(231.5, 15.35, 34, 8), O(236.5, 15.55, 40, 16), O(242.6, 16.05, 44, 20, CD),
    # 15 · V1 kết: ven kênh (zoom-through) → kéo ra thấy mọi lớp → tên dự án phát sáng
    [246.0, 10.9690, 106.7022, 16.6, 40, 10], [248.0, 10.9690, 106.7022, 17.2, 36, 6], [250.9, 10.9690, 106.7022, 17.35, 34, 6],
    [254.0, 10.9660, 106.7000, 14.9, 30, 2], [257.2, 10.9664, 106.6990, 14.75, 34, 0], O(260.2, 15.0, 40, 4),
]
L = lambda geo, kind, id, w=5, fill=False, ln=True: {"geo": geo, "kind": kind, "id": id, "w": w, "fill": fill, "len": ln}
layers = [L("prov:VNM", "adm", "vnm", 4, True, False), L("prov:TPHCM_moi", "adm", "hcm", 5, True, False),
          L("prov:Đồng Nai", "adm", "dn", 3, True, False), L("prov:Tây Ninh", "adm", "tn", 3, True, False), L("prov:Đồng Tháp", "adm", "dt", 3, True, False),
          L("lines:site", "proj", "site", 6, True, True), L("prov:green_site", "green", "gsite", 3, True, False),
          L("prov:USA", "adm", "usa", 4, True, False), L("lines:canal", "water", "canal", 7, False, True), L("lines:blvd", "route", "blvd", 6, False, True),
          L("lines:ql13", "route", "ql13", 5, False, True), L("lines:vd3", "route", "vd3", 5, False, True)]
links = [{"id": "tl1", "a": "d1", "b": "d2", "bend": 0.25, "kind": "yel", "w": 4}, {"id": "tl2", "a": "d2", "b": "park", "bend": -0.3, "kind": "yel", "w": 4}, {"id": "tl3", "a": "park", "b": "cd_n", "bend": 0.3, "kind": "yel", "w": 4}, {"id": "lk_hk", "a": "hk", "b": "oneera", "bend": 0.18, "kind": "route", "w": 5}, {"id": "lk_sg", "a": "sg", "b": "oneera", "bend": -0.2, "kind": "route", "w": 5}]
circles = [{"id": "c_park", "pt": "park", "r_m": 56.4, "kind": "green"}, {"id": "c_hyde", "pt": "hyde", "r_m": 365.6, "kind": "green"},
           {"id": "c_oe", "pt": "oneera", "r_m": 397.0, "kind": "proj"},
           {"id": "h1", "pt": "park", "r_m": 190, "heat": True}, {"id": "h2", "pt": "blvd_mid", "r_m": 150, "heat": True}, {"id": "h3", "pt": "canal_m", "r_m": 170, "heat": True},
           {"id": "h4", "pt": "p_vas", "r_m": 120, "heat": True}]
rings = [{"id": "rg_walk", "pt": "park", "lat": 10.965, "t": 77.4, "km": [0.4, 0.8], "out": 89.0}, {"id": "rg_end", "pt": "oneera", "lat": 10.967, "t": 255.0, "km": [1, 2]}]
movers = [{"path": "canal", "t": 91.9, "d": 6.6, "icon": "bike", "out": 104.0}, {"path": "lk_hk", "t": 196.2, "d": 2.0, "icon": "plane", "out": 214.0},
          {"path": "lk_sg", "t": 217.6, "d": 2.0, "icon": "plane", "out": 223.0}]
lab = []
def la(at, t, d, big=None, text="", small="", color="w", lx=0, ly=-260, align="c", xl=False, unit=None, count=None):
    lab.append({k: v for k, v in dict(at=at, t=t, d=d, big=big, text=text, small=small, color=color, lx=lx, ly=ly, align=align, xl=xl, unit=unit, count=count).items() if v not in (None, "", False)})
# 1
la("hcm", 3.9, 3.6, "TP.HCM", "sau sáp nhập", color="adm", ly=-280)
# 2
la("hcm_t", 11.6, 2.6, "THUẬN GIAO", "phường", color="adm", ly=-230)
la("site_w", 14.7, 2.8, "49,5", "khu đô thị", color="proj", lx=120, ly=-300, xl=True, unit="ha", count={"from": 0, "to": 49.5, "dec": 1})
la("site_w", 17.6, 2.7, "> 1 tỷ", "tổng vốn đầu tư", color="w", lx=120, ly=-300, xl=True, unit="USD")
# 3
la("site_n", 23.4, 2.0, "25", "mật độ xây dựng nhà ở", color="proj", ly=-330, xl=True, unit="%", count={"from": 0, "to": 25})
la("site_n", 25.5, 4.2, "≈ 3/4", "khu đất không đặt móng nhà", color="green", ly=-330, xl=True)
# 5
la("site_n", 53.9, 2.4, "FITWEL ★★★", "hạng Community Site", small="đô thị duy nhất châu Á đạt", color="green", ly=-320)
la("atl", 59.9, 6.6, "CDC", "Kiểm soát & phòng ngừa dịch bệnh", color="adm", lx=0, ly=170, align="c")
la("dc", 61.4, 5.1, "GSA", "cơ quan liên bang Hoa Kỳ", color="adm", lx=-140, ly=-120, align="r")
la("ny", 64.0, 2.7, "Center for Active Design", "đơn vị vận hành Fitwel", color="w", lx=-200, ly=-400, align="c")
# 6
la("r400", 77.8, 7.6, "5 PHÚT", "đi bộ", color="yel", ly=-40)
la("r800w", 78.6, 6.8, "10 PHÚT", "đi bộ", color="yel", lx=30, ly=-70, align="l")
la("oneera", 85.9, 3.4, "≈ 3/4", "nơi nuôi thói quen vận động", color="green", ly=-190)
# 7
la("canal_s", 97.8, 6.0, "≈ 30 PHÚT", "2,6 km dạo bộ · đạp xe hai bờ kênh", color="proj", lx=-320, ly=-300, align="c")
la("park", 100.6, 4.4, "ONE PARK · 1 HA", "quảng trường · 2 hồ bơi", small="cà phê · sân chơi trẻ em", color="green", ly=-300)
# 8
la("hyde", 111.9, 3.6, "HYDE PARK", "≈ 42 ha · liền kề", color="green", ly=-430)
la("oneera", 113.1, 2.4, "ONE ERA", "49,5 ha", color="proj", lx=-300, ly=-200, align="r")
# 10
la("cd_n", 140.3, 4.0, "357", "nhà phố + shophouse", color="proj", ly=-300, xl=True, unit="căn", count={"from": 0, "to": 357})
la("blvd_mid", 153.4, 3.2, "ĐẠI LỘ 25 M", "mặt tiền thứ hai hướng One Park", color="route", ly=-280)
# 11
la("blvd_mid", 178.5, 3.6, "NGUỒN KHÁCH", "từ cư dân, mỗi ngày", color="yel", ly=-300)
# 12
la("hk", 195.8, 8.5, "LONGFOR", "niêm yết Hồng Kông · từ 09/2026", color="route", ly=-260)
la("hk", 204.7, 5.6, "100", "tại 25 thành phố châu Á", color="w", lx=-120, ly=230, xl=True, unit="TTTM", count={"from": 0, "to": 100})
la("hk", 210.6, 2.6, "> 90%", "hài lòng · 17 năm liền", small="Longfor Intelligent Living", color="w", lx=-120, ly=230, xl=True)
# 13
la("sg", 217.4, 4.4, "SURBANA JURONG", "tư vấn quy hoạch", color="route", ly=-470)
la("sg", 219.8, 2.0, "CPG", "thiết kế cảnh quan", color="green", ly=-230)
la("oneera", 222.0, 4.2, "SAVILLS", "quản lý · vận hành", color="w", ly=-280)
# 14
la("d1", 228.4, 3.8, "27/09/2025", "khởi công", color="yel", ly=-260)
la("d2", 230.2, 10.0, "09/2026", "Longfor tham gia", color="yel", ly=-300)
la("park", 232.4, 7.9, "31/10/2026", "One Park mở cửa", color="yel", lx=-230, ly=-200)
la("cd_n", 240.4, 2.6, "QUÝ IV/2028", "bàn giao nhà phố đầu tiên", small="Central District", color="yel", ly=-300, xl=False)
# 15
la("canal_m", 245.0, 3.0, "MỖI SÁNG", "đường ven kênh có người chạy bộ", color="proj", ly=-280)
pins = [{"at": "p_vas", "text": "VAS Saigon", "t": 119.9, "d": 11.5}, {"at": "p_kind", "text": "Kindup", "t": 121.5, "d": 9.9, "left": True},
        {"at": "p_meret", "text": "Meret Health Center", "t": 124.3, "d": 7.1}, {"at": "p_sport", "text": "Khu thể thao", "t": 126.2, "d": 5.2},
        {"at": "p_tttm", "text": "TTTM", "t": 127.3, "d": 4.1}, {"at": "p_off", "text": "Văn phòng hạng A", "t": 128.3, "d": 3.1, "left": True}]
ground = [{"at": "hcm_t", "text": "1 m² XÂY = 1 m² BÁN", "t": 5.0, "d": 5.4, "size": 84}, {"at": "oneera", "text": "ONE ERA", "t": 16.4, "d": 3.8},
          {"at": "q_title", "text": "LÀM VIỆC CHO AI?", "t": 42.6, "d": 4.6, "size": 58}, {"at": "cd", "text": "CENTRAL DISTRICT", "t": 135.6, "d": 4.4, "size": 72},
          {"at": "park", "text": "HẠ TẦNG THƯƠNG MẠI", "t": 182.4, "d": 5.0, "size": 78}, {"at": "oneera", "text": "ONE ERA", "t": 256.4, "d": 3.8, "size": 120}]
ev = []
E = lambda t, act, id, d=.6, **k: ev.append(dict(t=t, act=act, id=id, d=d, **k))
# 1
E(0.8, "show", "vnm", 1.0, to=.9); E(1.6, "show", "vnm-fill", 1.0, to=.5); E(4.0, "show", "hcm", .8); E(4.2, "show", "hcm-fill", .8, to=1)
E(4.6, "show", "dn", .8, to=.4); E(4.6, "show", "tn", .8, to=.4); E(4.6, "show", "dt", .8, to=.4); E(5.6, "hide", "vnm", 1.2)
E(10.9, "hide", "dn", .8); E(10.9, "hide", "tn", .8); E(10.9, "hide", "dt", .8); E(11.4, "dim", "hcm", 1.0, to=.3); E(13.2, "hide", "hcm", 1.0)
# 2
E(14.0, "draw", "site", 1.0); E(15.0, "show", "site-fill", .8, to=1)
# 3
E(21.0, "show", "site-fill", .6, to=.25); E(22.8, "grow", "ot", 2.0); E(23.1, "grow", "cd", 2.0)
# 4
E(33.0, "show", "gsite", .1); E(33.0, "show", "gsite-fill", 1.0, to=1); E(33.2, "tint", "ot", .8, to=.55); E(33.2, "tint", "cd", .8, to=.55)
# 5
E(47.6, "hide", "gsite", .8); E(48.0, "grow", "ot", .9, to=0, ease="power2.in"); E(48.2, "grow", "cd", .9, to=0, ease="power2.in")
E(58.6, "show", "usa", .8); E(59.2, "show", "usa-fill", .8, to=1); E(58.6, "show", "vnm", .8, to=.6); E(66.6, "hide", "usa", 1.2); E(70.0, "hide", "vnm", 1.0)
# 6
E(76.2, "show", "c_park", .6, to=.8); E(85.8, "show", "gsite", .9, to=1); E(89.6, "hide", "gsite", .8)
# 7
E(91.7, "draw", "canal", 6.6); E(100.2, "show", "c_park", .5, to=1)
# 8
E(108.9, "dim", "site", .6, to=.5); E(111.6, "show", "c_hyde", .8); E(113.0, "show", "c_oe", .8, to=.85); E(116.0, "hide", "c_hyde", .8); E(116.0, "hide", "c_oe", .8)
E(116.0, "show", "site", .6, to=1)
# 10
E(132.0, "grow", "ot", 1.6, to=.6); E(132.0, "tint", "ot", .1, to=.5); E(137.4, "grow", "cd", 1.8); E(137.4, "tint", "cd", .1, to=.95)
E(148.0, "show", "canal", .5, to=1); E(150.9, "draw", "blvd", 1.2); E(154.9, "show", "c_park", .4, to=1)
# 11
E(164.4, "show", "h1", 1.0); E(165.6, "show", "h2", 1.0); E(166.8, "show", "h3", 1.0); E(168.0, "show", "h4", 1.0)
E(187.6, "hide", "h1", .8); E(187.6, "hide", "h2", .8); E(187.6, "hide", "h3", .8); E(187.6, "hide", "h4", .8)
E(188.0, "grow", "ot", .9, to=0, ease="power2.in"); E(188.0, "grow", "cd", .9, to=0, ease="power2.in"); E(188.2, "hide", "blvd", .6); E(188.2, "hide", "canal", .6); E(188.2, "hide", "c_park", .6)
# 12–13
E(195.6, "draw", "lk_hk", 2.0); E(217.4, "draw", "lk_sg", 2.0); E(221.8, "hide", "lk_hk", .8); E(223.0, "hide", "lk_sg", .8)
E(229.0, "draw", "tl1", 1.2); E(231.2, "draw", "tl2", 1.2); E(239.4, "draw", "tl3", 1.0)
E(243.2, "hide", "tl1", .8); E(243.2, "hide", "tl2", .8); E(243.2, "hide", "tl3", .8)
# 15 — tích luỹ mọi lớp
E(243.5, "show", "canal", .6, to=1)
E(254.0, "show", "gsite", .8, to=.8); E(254.3, "show", "ql13", .5); E(254.3, "draw", "ql13", 1.0); E(254.5, "draw", "vd3", 1.0); E(254.7, "show", "blvd", .5, to=1)
E(254.9, "show", "c_park", .6, to=1); E(255.2, "show", "h1", .8, to=.7); E(256.0, "draw", "site", 1.2); E(256.0, "show", "site-fill", 1.0, to=1)
foot = [{"t": 29.9, "d": 2.8, "media": "assets/img/p7.jpg", "move": "push", "focus": "55% 50%", "src": "phối cảnh CĐT (The Leader)"},
        {"t": 105.6, "d": 2.8, "media": "assets/img/p1.jpg", "move": "pull", "focus": "60% 50%", "src": "khai trương One Park, ảnh CafeF 03/11/2026"},
        {"t": 144.6, "d": 2.8, "media": "assets/img/p3.jpg", "move": "panR", "focus": "35% 50%", "src": "nhà phố Central District, phối cảnh CĐT (CafeF)"},
        {"t": 156.8, "d": 2.9, "media": "assets/img/p6.jpg", "move": "push", "focus": "50% 60%", "src": "shophouse mặt tiền, phối cảnh CĐT (CafeF)"},
        {"t": 248.1, "d": 2.9, "media": "assets/img/p5.jpg", "move": "push", "focus": "50% 55%", "src": "đường nội khu có người đạp xe, phối cảnh CĐT (CafeF)"}]
legend = [{"t": 33.4, "d": 13.4, "items": [["#4ADE80", "≈ 75% cây xanh · nước · đường đi bộ"], ["#2FD3E0", "≈ 25% xây nhà ở"]]},
          {"t": 164.6, "d": 22.4, "items": [["#FACC15", "lượng người đi bộ (minh hoạ)"], ["#4ADE80", "One Park"], ["#E04BD6", "đại lộ nội khu 25 m"]]}]
src = [{"t": 1.0, "d": 19.0, "text": "Nguồn: CafeF, Báo Đầu tư (11/2026) · ảnh vệ tinh Esri, Maxar"},
       {"t": 21.0, "d": 26.0, "text": "Mật độ ~25%: CafeF (05/2026) · khối nhà là minh hoạ tỉ lệ, không phải bản vẽ quy hoạch"},
       {"t": 52.4, "d": 15.0, "text": "Fitwel 3 sao (Community Site): VnExpress, Znews (2026)"},
       {"t": 76.4, "d": 13.0, "text": "Bán kính đi bộ ước tính 80 m/phút · vị trí One Park minh hoạ"},
       {"t": 91.0, "d": 25.0, "text": "Kênh Suối Cát 2,6 km, One Park 1 ha: CafeF (11/2026) · Hyde Park ~42 ha: Báo Đầu tư — vị trí minh hoạ"},
       {"t": 117.5, "d": 13.0, "text": "Tên tiện ích theo CafeF, Báo Đầu tư · vị trí ghim minh hoạ"},
       {"t": 132.0, "d": 55.0, "text": "Central District, shophouse 2 mặt tiền: CafeF (07/11/2026) · bố trí minh hoạ"},
       {"t": 194.0, "d": 32.0, "text": "Longfor & đối tác: The Leader (25/09/2026)"},
       {"t": 228.0, "d": 15.0, "text": "Mốc thời gian: SGGP (09/2025), The Leader (09/2026), CafeF (11/2026)"}]
chapters = [
    {"t": 0.0, "name": "Phép tính quen thuộc", "V": "V2", "cam": "hạ từ mây xuống VN → TP.HCM (zoom 5.2→9.5)", "layers": "VN, TP.HCM (cam), tỉnh lân cận mờ 40%, tiêu đề mặt đất"},
    {"t": 10.9, "name": "Thuận Giao · 49,5 ha · >1 tỷ USD", "V": "V1", "cam": "fly-to vào dự án, nghiêng 0→48°", "layers": "ranh dự án vẽ + phủ cyan, ONE ERA mặt đất, 2 thẻ số"},
    {"t": 20.4, "name": "Mật độ 25%", "V": "V6", "cam": "quay quanh 4→25°, đẩy vào phối cảnh", "layers": "60 khối 3D mọc, thẻ 25% và ≈3/4"},
    {"t": 32.1, "name": "3/4 khu đất nhường lại", "V": "V8", "cam": "quay chậm 25→48°, kéo ra", "layers": "tô xanh 75% + chú giải, khối mờ, tiêu đề LÀM VIỆC CHO AI?"},
    {"t": 47.2, "name": "Fitwel 3 sao · CDC Hoa Kỳ", "V": "V2", "cam": "về 0° → bay vòng ra thế giới → Đông Hoa Kỳ", "layers": "thẻ Fitwel, Hoa Kỳ (cam), CDC/GSA/Center for Active Design"},
    {"t": 67.1, "name": "Thiết kế khiến người ta vận động", "V": "V4", "cam": "bay vòng về VN → One Park, nghiêng 24→40°", "layers": "vòng 5/10 phút đi bộ, One Park, tô xanh 3/4"},
    {"t": 89.7, "name": "Kênh Suối Cát · One Park", "V": "V3", "cam": "bám đầu tuyến dọc kênh → One Park → zoom-through", "layers": "tuyến kênh + xe đạp, nhãn 30 phút, One Park 1 ha"},
    {"t": 108.5, "name": "Hyde Park ~42 ha", "V": "V5", "cam": "kéo ra 17.4→14.6", "layers": "3 vòng tròn đúng diện tích (1 / 42 / 49,5 ha)"},
    {"t": 115.6, "name": "Tiện ích có tên", "V": "V7", "cam": "quay chậm -2→36°", "layers": "6 ghim vàng: VAS, Kindup, Meret, thể thao, TTTM, văn phòng"},
    {"t": 129.2, "name": "357 căn Central District", "V": "V6", "cam": "đẩy vào CD → zoom-through → đại lộ", "layers": "khối CD sáng, khối khác mờ, thẻ 357, đại lộ 25 m, One Park"},
    {"t": 156.7, "name": "Mảng xanh = hạ tầng thương mại", "V": "V8", "cam": "zoom-through shophouse → quay -22°", "layers": "4 điểm nóng người đi bộ + chú giải"},
    {"t": 187.5, "name": "Longfor", "V": "V3", "cam": "kéo ra châu Á (Z 5.4)", "layers": "tuyến HK→One Era có máy bay, thẻ 100 TTTM, >90%"},
    {"t": 213.5, "name": "Đội ngũ quy hoạch", "V": "V10", "cam": "lướt xuống Singapore → về dự án", "layers": "thẻ Surbana Jurong, CPG, Savills; tuyến SG→One Era"},
    {"t": 226.7, "name": "Lời hứa và mốc thời gian", "V": "V9", "cam": "nghiêng 20→44°, quay 0→20°", "layers": "27/09/2025 · 09/2026 · 31/10/2026 · Quý IV/2028"},
    {"t": 242.9, "name": "Kết", "V": "V1", "cam": "zoom-through ven kênh → kéo ra → về ranh", "layers": "mọi lớp: kênh, xanh, đường, đại lộ, vòng km, ranh phát sáng, ONE ERA"}]
out = {"duration": 260.23, "audio": "assets/mix.wav", "gsap": "assets/lib/gsap.min.js", "sat": SAT, "points": PTS, "blocks": "blocks.json", "blockH": {"ot": 38, "cd": 44},
       "cam": cam, "layers": layers, "links": links, "circles": circles, "rings": rings, "movers": movers, "labels": lab, "pins": pins, "ground": ground,
       "ev": ev, "hud": {"clouds": [0.0, 2.8], "legend": legend, "src": src}, "foot": foot, "cuts": [], "chapters": chapters}
for k in cam: k[5] = round(k[5] * 0.6, 1)
for a, b in zip(cam, cam[1:]): assert b[0] > a[0], (a[0], b[0])
json.dump(out, open("proj/flight.json", "w"), ensure_ascii=False, indent=1)
print(len(cam), "keys", len(lab), "labels", len(ev), "events")
