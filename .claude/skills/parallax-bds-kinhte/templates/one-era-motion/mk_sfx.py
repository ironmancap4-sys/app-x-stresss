import json
d = json.load(open("proj/shots.json")); ev = []
def add(t, s, db=0):
    if t >= 0: ev.append({"t": round(t, 3), "sfx": s, "db": db})
for sh in d["shots"]:
    st = sh["start"]; e = sh.get("enter", "T5")
    if e in ("T3", "T2"): add(st - 0.12, "whoosh.wav")
    elif e in ("T1", "T4", "DIS"): add(st - 1.4, "riser.wav", -3)
    elif sh.get("zoomBlur"): add(st, "whoosh.wav", -2)
    else: add(st, "impact.wav", -6)               # cắt cứng: nhịp chạm nhẹ
    for k in sh.get("kw", []): add(st + k["t"], "pop.wav", -2)
    for k in sh.get("montage", []): add(st + k["t"], "impact.wav", -3)
    for k in sh.get("labels", []) + sh.get("callouts", []): add(st + k["t"], "pop.wav", -4)
    for k in sh.get("pins", []): add(st + k["t"] + .2, "pop.wav", 0)
    for k in sh.get("ground", []): add(st + k["t"], "impact.wav", -2)
    for k in sh.get("rings", []):
        for i in range(len(k["km"])): add(st + k["t"] + i * .45, "pop.wav", -3)
    for k in sh.get("movers", []): add(st + k["t"], "whoosh.wav", -8)
    for k in sh.get("draw", []):
        if k["d"] >= .8: add(st + k["t"], "whoosh.wav", -9)
    if sh.get("big"): add(st + sh["big"]["t"], "impact.wav", 0)
    if sh.get("bar"): add(st + sh["bar"]["t"] + .1, "riser.wav", -8)
    for k in (sh.get("timeline") or {}).get("events", []): add(st + k["t"], "pop.wav", -2)
    for k in (sh.get("wall") or {}).get("tiles", []): add(st + k["t"], "whoosh.wav", -6)
    for k in (sh.get("stack") or {}).get("rows", []): add(st + k["t"], "pop.wav", -2)
    if sh.get("clouds"): add(st, "whoosh.wav", 0)
ev.sort(key=lambda x: x["t"]); out = []
for x in ev:  # cùng loại cách nhau ≥0,22 s
    if out and any(o["sfx"] == x["sfx"] and x["t"] - o["t"] < .22 for o in out[-4:]): continue
    out.append(x)
json.dump(out, open("proj/sfx/events.json", "w"), indent=0)
print(len(out), "SFX events")
