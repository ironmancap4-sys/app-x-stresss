#!/usr/bin/env python3
"""Ghép ô ảnh vệ tinh Esri World Imagery cho một khung lat/lng ở mức zoom z.

  python sat_tiles.py sat16 16 <lat_trên> <lng_trái> <lat_dưới> <lng_phải> img   -> sat16.jpg + sat16.json {z,x0,y0,w,h}

Phủ RỘNG hơn mọi khung hình camera sẽ thấy ở mức đó (kể cả khi nghiêng 3D) — thiếu là lộ hình chữ nhật navy.
Sau đó chạy sat_declouds.py để xoá mây + chỉnh màu.
"""
#!/usr/bin/env python3
"""Ghép ô ảnh vệ tinh Esri World Imagery (hoặc lớp tham chiếu) cho một khung lat/lng ở mức zoom z.

  python sat_tiles.py sat16 16 <lat_trên> <lng_trái> <lat_dưới> <lng_phải> img   -> sat16.jpg + sat16.json {z,x0,y0,w,h}

Phủ RỘNG hơn mọi khung hình camera sẽ thấy ở mức đó (kể cả khi nghiêng 3D): thiếu là lộ hình chữ nhật navy.
Rồi chạy sat_declouds.py để xoá mây + chỉnh màu."""
import math, io, sys, json, urllib.request, concurrent.futures as cf
from PIL import Image
def xy(lat,lng,z):
    n=2**z; x=(lng+180)/360*n; y=(1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n; return x,y
SV={'img':'World_Imagery','trn':'Reference/World_Transportation','lbl':'Reference/World_Boundaries_and_Places'}
def fetch(layer,z,x,y):
    u=f"https://server.arcgisonline.com/ArcGIS/rest/services/{SV[layer]}/MapServer/tile/{z}/{y}/{x}"
    for _ in range(4):
        try: return Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"tile-fetch/1.0"}),timeout=30).read())).convert("RGBA")
        except Exception as e: err=e
    raise err
def mosaic(name,z,lat1,lng1,lat2,lng2,layers=('img',)):
    x1,y1=xy(lat1,lng1,z); x2,y2=xy(lat2,lng2,z)
    tx=range(int(min(x1,x2)),int(max(x1,x2))+1); ty=range(int(min(y1,y2)),int(max(y1,y2))+1)
    out=Image.new("RGBA",(256*len(tx),256*len(ty)),(0,0,0,255))
    for L in layers:
        with cf.ThreadPoolExecutor(8) as ex:
            futs={ex.submit(fetch,L,z,x,y):(i,j) for i,x in enumerate(tx) for j,y in enumerate(ty)}
            for f,(i,j) in futs.items(): t=f.result(); out.alpha_composite(t,(256*i,256*j))
    out.convert("RGB").save(name+".jpg",quality=88)
    m={"z":z,"x0":tx[0]*256,"y0":ty[0]*256,"w":out.width,"h":out.height}; print(name,m); return m
if __name__=="__main__":
    a=sys.argv; m=mosaic(a[1],int(a[2]),float(a[3]),float(a[4]),float(a[5]),float(a[6]),tuple(a[7].split(',')))
    json.dump(m,open(a[1]+'.json','w'))
