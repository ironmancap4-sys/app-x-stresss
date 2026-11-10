#!/usr/bin/env python3
"""Dựng dữ liệu bản đồ vector (geo.json) cho template kinh-te-dia-phuong.

  pip install shapely scikit-image numpy pillow
  python geo_build.py config.json out/geo.json [--work work/]

Nguồn: Natural Earth 10m (admin-0, admin-1, sông) từ raw.githubusercontent.com/nvkelso/natural-earth-vector,
ảnh vệ tinh Esri World Imagery (để dò lòng sông). Cần các host đó trong danh sách mạng.

config.json (ví dụ Vĩnh Long, NQ 202/2025/QH15):
{
  "country": "VNM",
  "merge": {"Vĩnh Long": ["Vĩnh Long","Bến Tre","Trà Vinh"], "Cần Thơ": ["Can Tho","Sóc Trăng","Hau Giang"],
            "TP.HCM": ["Hồ Chí Minh city","Bình Dương","Bà Rịa - Vũng Tàu"], "Đồng Tháp": ["Ðong Tháp","Tiền Giang"],
            "An Giang": ["An Giang","Kiên Giang"], "Cà Mau": ["Cà Mau","Bạc Liêu"], "Tây Ninh": ["Tây Ninh","Long An"]},
  "focus": "Vĩnh Long", "compare": ["TP.HCM", "Cần Thơ"],
  "region": ["Vĩnh Long","Cần Thơ","An Giang","Đồng Tháp","Cà Mau"],
  "points": {"pt_hcm": [106.7009,10.7769], "pt_ct": [105.7469,10.0452], "pt_vl": [105.9722,10.2537], "region": [105.55,9.85]},
  "label_points": {"rv_tien": [106.33,10.335], "rv_hau": [105.60,10.25]},
  "rivers": {
    "tien": {"ne_name": "Mekong", "ne_end": [106.118663,10.237576], "cut_at": [105.9105,10.2764], "trace_to": [106.78,10.215]},
    "hau":  {"ne_name": "Mekong", "ne_end": [105.837983,10.004991], "trace_from": [105.838,10.005], "trace_to": [106.36,9.57]}
  },
  "coast_axis": [[106.80,10.24],[106.33,9.56]],
  "satellite": {"z": 10, "bbox": [104.4, 8.6, 107.8, 12.0]}
}
Tên tỉnh trong "merge" phải đúng như Natural Earth (in ra bằng --list). Luôn xem `work/rivers_preview.jpg` trước khi dùng.
"""
import argparse, io, json, math, os, sys, urllib.request
import concurrent.futures as cf

NE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
UA = {"User-Agent": "geo-build/1.0"}
Z = 8; N = 256 * 2 ** Z

def fetch(url, path):
    if not os.path.exists(path):
        urllib.request.urlretrieve(url, path)
    return path

def mx(lng, z=Z): return (lng + 180) / 360 * 256 * 2 ** z
def my(lat, z=Z):
    r = math.radians(lat); return (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * 256 * 2 ** z
def inv(x, y, z):
    n = 256 * 2 ** z; return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n)))), x / n * 360 - 180

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("config"); ap.add_argument("out"); ap.add_argument("--work", default="work")
    ap.add_argument("--list", action="store_true", help="in tên tỉnh Natural Earth của nước rồi thoát")
    a = ap.parse_args()
    from shapely.geometry import shape, mapping, Point, LineString
    from shapely.ops import unary_union, substring
    C = json.load(open(a.config, encoding="utf-8")); os.makedirs(a.work, exist_ok=True)
    adm1 = json.load(open(fetch(NE + "ne_10m_admin_1_states_provinces.geojson", f"{a.work}/adm1.geojson"), encoding="utf-8"))
    prov = {f["properties"]["name"]: shape(f["geometry"]).buffer(0) for f in adm1["features"] if f["properties"].get("adm0_a3") == C["country"]}
    if a.list:
        print("\n".join(sorted(prov))); return
    adm0 = json.load(open(fetch(NE + "ne_10m_admin_0_countries.geojson", f"{a.work}/adm0.geojson"), encoding="utf-8"))
    country = [shape(f["geometry"]) for f in adm0["features"] if f["properties"].get("ADM0_A3") == C["country"]][0]

    # 1. gộp tỉnh
    G = {k: unary_union([prov[x].buffer(0.003) for x in v]).buffer(-0.003).simplify(0.003) for k, v in C["merge"].items()}
    P = lambda c: f"{mx(c[0]):.1f} {my(c[1]):.1f}"
    ring = lambda cs: "M" + " L".join(P(c) for c in cs) + "Z"
    def poly_d(g, min_area=0.0005):
        ps = [g] if g.geom_type == "Polygon" else list(g.geoms)
        return " ".join(ring(p.exterior.coords) + "".join(ring(i.coords) for i in p.interiors) for p in ps if p.area >= min_area)
    line_d = lambda cs: "M" + " L".join(P(c) for c in cs)
    out = {"Z": Z, "prov": {k: poly_d(g) for k, g in G.items()}, "lab": {}}
    out["prov"]["_vn"] = poly_d(country.simplify(0.008), 0.02)
    for k, g in G.items():
        p = g.representative_point(); out["lab"][k] = [round(mx(p.x), 1), round(my(p.y), 1)]
    out["region"] = poly_d(unary_union([G[k] for k in C["region"]]).buffer(0.01).buffer(-0.01), 0.01)
    for k, (lng, lat) in {**C.get("points", {}), **C.get("label_points", {})}.items():
        out["lab"][k] = [round(mx(lng), 1), round(my(lat), 1)]

    # 2. sông: nhánh Natural Earth (cắt) + dò tiếp ra cửa biển trên ảnh vệ tinh
    import numpy as np
    from PIL import Image, ImageDraw
    from skimage.graph import route_through_array
    sat = C["satellite"]; z = sat["z"]; w, s_, e, n_ = sat["bbox"]
    x0, x1 = int(mx(w, z) // 256), int(mx(e, z) // 256); y0, y1 = int(my(n_, z) // 256), int(my(s_, z) // 256)
    img = Image.new("RGB", (256 * (x1 - x0 + 1), 256 * (y1 - y0 + 1)))
    def tile(xy):
        x, y = xy; u = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
        return xy, Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read())).convert("RGB")
    with cf.ThreadPoolExecutor(8) as ex:
        for (x, y), t in ex.map(tile, [(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]):
            img.paste(t, (256 * (x - x0), 256 * (y - y0)))
    k = 2; arr = np.asarray(img).astype(float)[::k, ::k]
    R, Gc, B = arr[..., 0], arr[..., 1], arr[..., 2]
    water = (R > Gc) & (Gc > B) & (R > 95) & ((R - B) > 25) & (Gc > 70)   # nước phù sa nâu nhạt
    cost = np.where(water, 1.0, 25.0)
    pix = lambda lng, lat: (int((my(lat, z) - 256 * y0) / k), int((mx(lng, z) - 256 * x0) / k))
    def trace(a_, b_):
        path, _ = route_through_array(cost, pix(*a_), pix(*b_), fully_connected=True, geometric=True)
        return [[round(ln, 5), round(la, 5)] for la, ln in (inv(c * k + 256 * x0, r * k + 256 * y0, z) for r, c in path[::3])]
    rv = json.load(open(fetch(NE + "ne_10m_rivers_lake_centerlines.geojson", f"{a.work}/rivers.geojson"), encoding="utf-8"))
    pv = img.copy(); dr = ImageDraw.Draw(pv)
    for name, cfg in C.get("rivers", {}).items():
        ne = [shape(f["geometry"]) for f in rv["features"] if f["properties"].get("name") == cfg["ne_name"]][0]
        part = min(ne.geoms, key=lambda p: Point(p.coords[-1]).distance(Point(cfg["ne_end"])))
        if "cut_at" in cfg:
            part = substring(part, 0, part.project(Point(cfg["cut_at"])))
        start = cfg.get("trace_from", cfg.get("cut_at"))
        pts = [list(c) for c in part.coords] + trace(tuple(start), tuple(cfg["trace_to"]))[1:]
        pts = [list(c) for c in LineString(pts).simplify(0.004).coords]
        out[name] = line_d(pts)
        dr.line([(mx(x, z) - 256 * x0, my(y, z) - 256 * y0) for x, y in pts], fill=(80, 200, 255), width=6)
    pv.resize((pv.width // 2, pv.height // 2)).save(f"{a.work}/rivers_preview.jpg")

    # 3. dải ven biển của tỉnh trọng tâm: điểm ranh giới gần trục bờ biển
    if "coast_axis" in C:
        g = G[C["focus"]]; big = max(g.geoms, key=lambda p: p.area) if g.geom_type != "Polygon" else g
        axis = LineString(C["coast_axis"])
        pts = sorted([p for p in big.exterior.coords if axis.distance(Point(p)) < 0.06], key=lambda p: axis.project(Point(p)))
        line = [pts[0]]
        for p in pts[1:]:
            if Point(p).distance(Point(line[-1])) < 0.12: line.append(p)
        out["coast"] = line_d(line)
        m = LineString(line).interpolate(0.45, normalized=True); out["lab"]["coast"] = [round(mx(m.x), 1), round(my(m.y), 1)]
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w", encoding="utf-8"))
    print(f"{a.out}: {len(G)} tỉnh, sông {list(C.get('rivers', {}))}; xem {a.work}/rivers_preview.jpg")

if __name__ == "__main__":
    main()
