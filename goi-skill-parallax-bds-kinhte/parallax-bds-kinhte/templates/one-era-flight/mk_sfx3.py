"""SFX theo sự kiện của kế hoạch bay: whoosh khi camera di chuyển lớn, pop cho nhãn/ghim/số, swell trước lộ diện lớn."""
import json, sys
F = json.load(open(sys.argv[1])); ev = []
add = lambda t, s, db=0: ev.append({"t": round(max(0, t), 3), "sfx": s, "db": db})
K = F["cam"]
for a, b in zip(K, K[1:]):
    big = abs(b[3] - a[3]) > 0.9 or abs(b[2] - a[2]) > 1 or abs(b[4] - a[4]) > 12
    if big: add(a[0] + 0.1, "whoosh.wav", -3 if abs(b[3] - a[3]) > 2.5 else -7)
for l in F["labels"]: add(l["t"], "pop.wav", -1 if l.get("xl") else -4)
for p in F["pins"]: add(p["t"] + 0.25, "pop.wav", 0)
for g in F["ground"]: add(g["t"] - 0.9, "riser.wav", -7); add(g["t"] + 0.1, "impact.wav", -6)
for f in F["foot"]: add(f["t"] - 0.9, "riser.wav", -5); add(f["t"] + f["d"] - 0.3, "whoosh.wav", -6)
for r in F["rings"]:
    for i in range(len(r["km"])): add(r["t"] + i * .45, "pop.wav", -3)
for e in F["ev"]:
    if e["act"] == "grow" and e.get("to", 1) > 0.5: add(e["t"], "riser.wav", -8)
    if e["act"] == "draw" and e.get("d", .6) >= 1: add(e["t"], "whoosh.wav", -10)
    if e["act"] == "show" and e["id"].startswith(("c_", "h")) and e.get("to", 1) > .7: add(e["t"], "pop.wav", -6)
for m in F["movers"]: add(m["t"], "whoosh.wav", -9)
add(0.0, "whoosh.wav", 0)
ev.sort(key=lambda x: x["t"]); out = []
for x in ev:
    if out and any(o["sfx"] == x["sfx"] and x["t"] - o["t"] < .25 for o in out[-5:]): continue
    out.append(x)
json.dump(out, open(sys.argv[2], "w"), indent=0); print(len(out), "SFX")
