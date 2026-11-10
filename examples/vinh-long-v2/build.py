#!/usr/bin/env python3
"""Ghép GEO + mapjs + mapcss vào các scene trong src/ -> compositions/."""
import json, os, glob
D = os.path.dirname(os.path.abspath(__file__))
FOOT = json.load(open(f"{D}/footage.json"))
geo = open(f"{D}/geo.json").read(); mapjs = open(f"{D}/mapjs.js").read(); mapcss = open(f"{D}/mapcss.css").read()
os.makedirs(f"{D}/compositions", exist_ok=True)
for f in glob.glob(f"{D}/src/*.html"):
    s = open(f, encoding="utf-8").read()
    s = s.replace("/*GEOJSON*/", "const GEO = " + geo + ";").replace("/*MAPJS*/", mapjs).replace("/*MAPCSS*/", mapcss)
    s = s.replace('<div id="g-whip">', '<div id="g-whip"><div class="mapbg"></div>')
    for k, v in FOOT.items(): s = s.replace("/*" + k + "*/", str(v))
    open(f"{D}/compositions/" + os.path.basename(f), "w", encoding="utf-8").write(s)
    print("built", os.path.basename(f))
