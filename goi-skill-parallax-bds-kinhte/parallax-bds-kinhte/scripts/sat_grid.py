#!/usr/bin/env python3
"""sat_grid.py — cắt ảnh vệ tinh (sat_tiles.py) kèm lưới lat/lng để DÒ tuyến đường khi OSM/Overpass không phản hồi.

  python sat_grid.py sat13.jpg sat13.json out.jpg <lat0> <lat1> <lng0> <lng1> [--step 0.01] [--scale 1.6] [--line lines.json]

lines.json: [[[lat,lng],[lat,lng],...], ...] — vẽ thử tuyến đã dò (hồng) để so với đường trên ảnh rồi chỉnh.
Tuyến dò tay phải ghi "hướng tuyến minh hoạ" trên màn hình nếu không chắc."""
import argparse, json, math
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None
ap = argparse.ArgumentParser(); ap.add_argument("img"); ap.add_argument("meta"); ap.add_argument("out")
for k in ("lat0", "lat1", "lng0", "lng1"): ap.add_argument(k, type=float)
ap.add_argument("--step", type=float, default=0.01); ap.add_argument("--scale", type=float, default=1.6); ap.add_argument("--line")
a = ap.parse_args(); m = json.load(open(a.meta)); IM = Image.open(a.img)
def px(lat, lng):
    n = 2 ** m["z"] * 256; x = (lng + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return x - m["x0"], y - m["y0"]
x0, y1 = px(a.lat0, a.lng0); x1, y0 = px(a.lat1, a.lng1); k = a.scale
im = IM.crop((int(x0), int(y0), int(x1), int(y1))).convert("RGB"); im = im.resize((int(im.width * k), int(im.height * k)))
d = ImageDraw.Draw(im); f = ImageFont.load_default()
lat = math.ceil(a.lat0 / a.step) * a.step
while lat < a.lat1:
    _, y = px(lat, a.lng0); d.line([(0, (y - y0) * k), (im.width, (y - y0) * k)], fill=(255, 255, 0)); d.text((3, (y - y0) * k + 2), f"{lat:.3f}", fill=(255, 255, 0), font=f); lat += a.step
lng = math.ceil(a.lng0 / a.step) * a.step
while lng < a.lng1:
    x, _ = px(a.lat0, lng); d.line([((x - x0) * k, 0), ((x - x0) * k, im.height)], fill=(0, 255, 255)); d.text(((x - x0) * k + 2, 3), f"{lng:.3f}", fill=(0, 255, 255), font=f); lng += a.step
for line in (json.load(open(a.line)) if a.line else []):
    d.line([((px(p[0], p[1])[0] - x0) * k, (px(p[0], p[1])[1] - y0) * k) for p in line], fill=(255, 0, 255), width=3)
im.save(a.out, quality=88); print(a.out, im.size)
