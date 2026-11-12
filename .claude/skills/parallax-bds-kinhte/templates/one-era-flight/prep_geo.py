import json, math
from shapely.geometry import shape, Polygon, MultiPolygon, box, Point
from shapely.ops import unary_union
from shapely import affinity
import sys
S = sys.argv[1] if len(sys.argv) > 1 else "."   # thư mục có oe/geo/geo.json (geo_build.py) và osm/ne_10m_admin_0_countries.geojson
g = json.load(open(f"{S}/oe/geo/geo.json"))
wx = lambda lng: (lng + 180) / 360 * 256 * 2 ** 8
wy = lambda lat: (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * 256 * 2 ** 8
def path(geom, closed=True):
    polys = [geom] if geom.geom_type == "Polygon" else list(geom.geoms)
    out = []
    for p in polys:
        c = list(p.exterior.coords)
        out.append("M" + " L".join(f"{wx(x):.1f} {wy(y):.1f}" for x, y in c) + (" Z" if closed else ""))
    return " ".join(out)
ne = json.load(open(f"{S}/osm/ne_10m_admin_0_countries.geojson"))
for f in ne["features"]:
    iso = f["properties"].get("ADM0_A3")
    if iso in ("USA", "VNM"):
        geom = shape(f["geometry"]).simplify(0.08 if iso == "USA" else 0.02)
        if iso == "USA":  # bỏ Alaska/Hawaii/đảo xa, giữ lục địa
            geom = unary_union([p for p in geom.geoms if p.area > 3 and p.centroid.x > -130])
        g["prov"][iso] = path(geom); print(iso, len(g["prov"][iso]))
# --- quy hoạch minh hoạ trong ranh dự án (KHÔNG phải bản vẽ của CĐT) ---
SITE = [[106.69143, 10.964091], [106.694648, 10.966935], [106.700764, 10.970411], [106.703339, 10.969463], [106.704304, 10.965671], [106.702373, 10.964723],
        [106.699476, 10.965671], [106.697867, 10.964091], [106.695614, 10.964723], [106.693361, 10.964091], [106.691751, 10.963143]]
site = Polygon(SITE)
mlat = 10.967; kx = 111320 * math.cos(math.radians(mlat)); ky = 110574
siteM = affinity.scale(Polygon([((x - SITE[0][0]) * kx, (y - SITE[0][1]) * ky) for x, y in SITE]), 1, 1, origin=(0, 0))
toLL = lambda x, y: (SITE[0][0] + x / kx, SITE[0][1] + y / ky)
print("site area ha", siteM.area / 1e4)
park_c = (106.6962, 10.9652)   # One Park (minh hoạ, gần mặt QL13 / Galleria)
pc = ((park_c[0] - SITE[0][0]) * kx, (park_c[1] - SITE[0][1]) * ky)
park = Point(pc).buffer(56.4)   # 1 ha
canal = shape({"type": "LineString", "coordinates": []}) if False else None
blocks = []; ang = 30  # hướng lưới theo trục dài khu đất
import itertools
cx, cy = siteM.centroid.x, siteM.centroid.y
for i, j in itertools.product(range(-20, 21), range(-12, 13)):
    bx, by = cx + i * 92, cy + j * 52
    r = affinity.rotate(box(bx - 40, by - 14, bx + 40, by + 14), ang, origin=(cx, cy))
    if siteM.buffer(-12).contains(r) and not r.intersects(park.buffer(25)):
        blocks.append(r)
# chọn đủ ~25% diện tích, ưu tiên quanh tâm
blocks.sort(key=lambda b: b.centroid.distance(Point(cx, cy)))
sel = []; area = 0
for b in blocks:
    if area >= 0.25 * siteM.area: break
    sel.append(b); area += b.area
print("blocks", len(sel), "coverage %.1f%%" % (area / siteM.area * 100))
B = []
for k, b in enumerate(sel):
    c = b.centroid; lng, lat = toLL(c.x, c.y)
    d = Point(c.x, c.y).distance(Point(pc))
    B.append({"lng": round(lng, 6), "lat": round(lat, 6), "w": 80, "d": 28, "ang": -ang, "cd": d < 420})
json.dump(B, open("blocks.json", "w"))
print("central district blocks", sum(b["cd"] for b in B))
# đại lộ nội khu 25 m (minh hoạ): đường thẳng qua One Park theo hướng lưới
p0 = affinity.rotate(Point(pc[0] - 50, pc[1] + 90), 0); 
ax = math.cos(math.radians(ang)); ay = math.sin(math.radians(ang))
a = (pc[0] + 90 * -ay - 30 * ax, pc[1] + 90 * ax - 30 * ay); b = (a[0] + 900 * ax, a[1] + 900 * ay)
la, lb = toLL(*a), toLL(*b)
g["lines"]["blvd"] = f"M{wx(la[0]):.1f} {wy(la[1]):.1f} L{wx(lb[0]):.1f} {wy(lb[1]):.1f}"
g["lab"]["blvd_mid"] = [wx((la[0] + lb[0]) / 2), wy((la[1] + lb[1]) / 2)]
g["prov"]["green_site"] = path(Polygon([toLL(x, y) for x, y in siteM.exterior.coords]))
json.dump(g, open("proj/geo.json", "w"))
print("park", park_c, "blvd", la, lb)
