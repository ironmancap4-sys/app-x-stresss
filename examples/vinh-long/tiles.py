import math, sys, io, json, urllib.request, concurrent.futures as cf
from PIL import Image
def xy(lat, lng, z):
    n = 2 ** z; x = (lng + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return x, y
def fetch(z, x, y):
    u = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    for _ in range(4):
        try: return Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=30).read())).convert("RGB")
        except Exception as e: err = e
    raise err
def mosaic(name, z, lat1, lng1, lat2, lng2):
    x1, y1 = xy(lat1, lng1, z); x2, y2 = xy(lat2, lng2, z)
    tx = range(int(min(x1, x2)), int(max(x1, x2)) + 1); ty = range(int(min(y1, y2)), int(max(y1, y2)) + 1)
    img = Image.new("RGB", (256 * len(tx), 256 * len(ty)))
    with cf.ThreadPoolExecutor(8) as ex:
        futs = {ex.submit(fetch, z, x, y): (i, j) for i, x in enumerate(tx) for j, y in enumerate(ty)}
        for f, (i, j) in futs.items(): img.paste(f.result(), (256 * i, 256 * j))
    img.save(f"{name}.jpg", quality=90)
    meta = {"z": z, "x0": tx[0] * 256, "y0": ty[0] * 256, "w": img.width, "h": img.height}
    print(name, meta); return meta
M = {}
M["delta"] = mosaic("delta", 10, 11.15, 105.15, 9.35, 107.15)
M["vl"] = mosaic("vl", 13, 10.40, 105.82, 10.12, 106.12)
M["city"] = mosaic("city", 15, 10.285, 105.935, 10.225, 106.010)
json.dump(M, open("maps.json", "w"), indent=1)
