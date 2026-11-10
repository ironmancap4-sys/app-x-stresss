// ===== Bản đồ vector (Web Mercator, toạ độ thế giới ở mức Z=8) — dùng chung cho các cảnh =====
// GEO = { prov:{tên:d}, region:d, tien:d, hau:d, coast:d, lab:{key:[x,y]} } được nhúng sẵn phía trên.
function makeMap(opts) {
  const W = 1080, H = 1920, Z0 = GEO.Z;
  const NS = "http://www.w3.org/2000/svg";
  const svg = document.querySelector(opts.svg), world = svg.querySelector(".world");
  const el = (tag, attrs, parent = world) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); parent.appendChild(e); return e; };
  const stroked = []; // [el, screenWidthPx]
  const S = (e, w) => { stroked.push([e, w]); return e; };
  // lớp vẽ
  el("path", { d: GEO.prov._vn, class: "vn" });
  for (const k in GEO.prov) if (!k.startsWith("_")) S(el("path", { d: GEO.prov[k], class: "prov", "data-name": k }), 1.6);
  const region = S(el("path", { d: GEO.region, class: "region", id: opts.id + "-region" }), 3);
  const fill = {};
  for (const k of ["TP.HCM", "Cần Thơ"]) fill[k] = S(el("path", { d: GEO.prov[k], class: "cmp", id: opts.id + "-" + (k === "TP.HCM" ? "hcm" : "ct") }), 2);
  const vlGlow = S(el("path", { d: GEO.prov["Vĩnh Long"], class: "vl-glow", id: opts.id + "-vlglow" }), 14);
  const vl = S(el("path", { d: GEO.prov["Vĩnh Long"], class: "vl", id: opts.id + "-vl" }), 3);
  const rv = {};
  for (const k of ["tien", "hau"]) {
    rv[k + "g"] = S(el("path", { d: GEO[k], class: "rv-glow", pathLength: 100, id: opts.id + "-" + k + "g" }), 14);
    rv[k] = S(el("path", { d: GEO[k], class: "rv", pathLength: 100, id: opts.id + "-" + k }), 4);
  }
  const coastG = S(el("path", { d: GEO.coast, class: "coast-glow", pathLength: 100, id: opts.id + "-coastg" }), 18);
  const coast = S(el("path", { d: GEO.coast, class: "coast", pathLength: 100, id: opts.id + "-coast" }), 5);
  const L = GEO.lab;
  const center = el("circle", { cx: L.pt_ct[0] + 6, cy: L.pt_ct[1] + 14, r: 46, class: "center", id: opts.id + "-center" });
  S(center, 3);
  const q = (a, b, bend) => { const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, dx = b[0] - a[0], dy = b[1] - a[1];
    return `M${a[0]} ${a[1]} Q ${mx - dy * bend} ${my + dx * bend}, ${b[0]} ${b[1]}`; };
  const corridor = S(el("path", { d: q(L.pt_hcm, L.pt_vl, 0.18) + " " + q(L.pt_vl, L.pt_ct, 0.12).replace("M", "L").replace(/^L[^Q]+/, ""), class: "corr", pathLength: 100, id: opts.id + "-corr" }), 6);
  corridor.setAttribute("d", q(L.pt_hcm, L.pt_vl, 0.18) + " " + q(L.pt_vl, L.pt_ct, 0.12).replace(/^M[^Q]+/, ""));
  const conE = S(el("path", { d: q(L.pt_vl, L.coast, -0.25), class: "con", pathLength: 100, id: opts.id + "-cone" }), 5);
  const conC = S(el("path", { d: q(L.pt_vl, [L.pt_ct[0] + 6, L.pt_ct[1] + 14], 0.3), class: "con", pathLength: 100, id: opts.id + "-conc" }), 5);
  const rings = [0, 1, 2].map((i) => el("circle", { cx: L["Vĩnh Long"][0], cy: L["Vĩnh Long"][1] - 20, r: 1, class: "ring", id: opts.id + "-ring" + i }));
  rings.forEach((r) => S(r, 4));
  // nhãn HTML gắn toạ độ
  const labels = [...document.querySelectorAll(opts.labels)].map((n) => ({ n, p: L[n.dataset.at], dx: +(n.dataset.dx || 0), dy: +(n.dataset.dy || 0) }));
  // Kiểu A: chấm tại vật thể, đường dẫn tới (lx,ly), chữ canh theo hướng đường dẫn
  document.querySelectorAll(opts.labels + ".la").forEach((n) => {
    const lx = +(n.dataset.lx || 0), ly = +(n.dataset.ly || 0), al = n.dataset.align || (lx >= 0 ? "l" : "r");
    const lead = n.querySelector(".lead"), tx = n.querySelector(".tx");
    if (lead) { lead.style.width = Math.hypot(lx, ly) + "px"; lead.style.transform = `rotate(${Math.atan2(ly, lx)}rad)`; }
    if (tx) { const gx = al === "l" ? 10 : al === "r" ? -10 : 0, gy = al === "c" ? (ly >= 0 ? 12 : -12) : 0;
      tx.style.left = (lx + gx) + "px"; tx.style.top = (ly + gy) + "px";
      tx.style.transform = al === "l" ? "translate(0,-50%)" : al === "r" ? "translate(-100%,-50%)" : (ly >= 0 ? "translate(-50%,0)" : "translate(-50%,-100%)");
      tx.style.textAlign = al === "r" ? "right" : al === "c" ? "center" : "left"; }
  });
  const ringR = { r0: 0, r1: 0, r2: 0 };

  // camera: (lat,lng,Z) -> Hermite đơn điệu trên x,y,Z => vận tốc liên tục
  const mx = (lng) => ((lng + 180) / 360) * 256 * 2 ** Z0;
  const my = (lat) => { const r = (lat * Math.PI) / 180; return ((1 - Math.log(Math.tan(r) + 1 / Math.cos(r)) / Math.PI) / 2) * 256 * 2 ** Z0; };
  const KEYS = opts.keys.map(([t, lat, lng, Z, carry]) => ({ t, x: mx(lng), y: my(lat), Z, carry }));
  const TS = KEYS.map((k) => k.t);
  const slopes = (vs) => { const n = vs.length, dl = [], m = new Array(n).fill(0);
    for (let k = 0; k < n - 1; k++) dl[k] = (vs[k + 1] - vs[k]) / (TS[k + 1] - TS[k]);
    m[0] = opts.startMoving === false ? 0 : dl[0]; m[n - 1] = KEYS[n - 1].carry ? dl[n - 2] : 0;
    for (let k = 1; k < n - 1; k++) m[k] = dl[k - 1] * dl[k] <= 0 ? 0 : (dl[k - 1] + dl[k]) / 2;
    for (let k = 0; k < n - 1; k++) { if (dl[k] === 0) { m[k] = 0; m[k + 1] = 0; continue; }
      const a = m[k] / dl[k], b = m[k + 1] / dl[k], s = a * a + b * b;
      if (s > 9) { const tau = 3 / Math.sqrt(s); m[k] = tau * a * dl[k]; m[k + 1] = tau * b * dl[k]; } }
    return m; };
  const C = {}; ["x", "y", "Z"].forEach((c) => { const vs = KEYS.map((k) => k[c]); C[c] = { vs, m: slopes(vs) }; });
  const sample = (t) => { t = Math.min(Math.max(t, TS[0]), TS[TS.length - 1]); let i = 0; while (i < TS.length - 2 && t > TS[i + 1]) i++;
    const h = TS[i + 1] - TS[i], s = (t - TS[i]) / h, s2 = s * s, s3 = s2 * s, o = {};
    ["x", "y", "Z"].forEach((c) => { const { vs, m } = C[c];
      o[c] = (2 * s3 - 3 * s2 + 1) * vs[i] + (s3 - 2 * s2 + s) * h * m[i] + (-2 * s3 + 3 * s2) * vs[i + 1] + (s3 - s2) * h * m[i + 1]; });
    return o; };
  function apply(t) {
    const c = sample(t), s = 2 ** (c.Z - Z0), tx = W / 2 - c.x * s, ty = H / 2 - c.y * s;
    world.setAttribute("transform", `translate(${tx.toFixed(2)} ${ty.toFixed(2)}) scale(${s.toFixed(5)})`);
    stroked.forEach(([e, w]) => e.setAttribute("stroke-width", (w / s).toFixed(4)));
    (opts.rings || []).forEach(([t0, dur, rmax], i) => { const r = rings[i]; if (!r) return;
      const p = (t - t0) / dur;
      if (p < 0 || p > 1) { r.style.opacity = "0"; return; }
      const rr = 10 + (rmax - 10) * (1 - (1 - p) ** 2);
      r.setAttribute("r", (rr / s).toFixed(3)); r.style.opacity = (0.95 * (1 - p)).toFixed(3); });
    labels.forEach(({ n, p, dx, dy }) => { n.style.transform = `translate(${(p[0] * s + tx + dx).toFixed(1)}px, ${(p[1] * s + ty + dy).toFixed(1)}px)`; });
  }
  return { apply, ringR, sample };
}
