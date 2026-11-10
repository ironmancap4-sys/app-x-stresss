// ===== vmap.js — bản đồ vector tổng quát (Web Mercator, toạ độ thế giới ở mức GEO.Z) =====
// GEO = { Z, prov:{tên: path d}, lab:{key:[x,y]}, lines:{key: path d}, ... } nhúng sẵn (scripts/geo_build.py).
// makeMap({ svg, id, labels, keys:[[t,lat,lng,Z,carry?]], layers:[...], rings:[[t0,dur,rmaxPx,ptKey]] })
//  layer: { geo:"prov:TÊN" | "lines:KHOÁ" | "raw:KHOÁ", cls, id, w (px màn hình), len:true (để vẽ dần bằng dashoffset) }
//       | { img:"assets/x.jpg", z, x0, y0, w, h, id, show:[Za,Zb] (hiện dần theo zoom) }
//       | { link:["ptA","ptB"], bend, cls, id, w }
// Ảnh vệ tinh/tile đặt đúng toạ độ thế giới => bay liền từ bản đồ vùng xuống tận công trường trong 1 cú máy.
function makeMap(opts) {
  const W = 1080, H = 1920, Z0 = GEO.Z, NS = "http://www.w3.org/2000/svg";
  const svg = document.querySelector(opts.svg), world = svg.querySelector(".world");
  const el = (tag, a, parent = world) => { const e = document.createElementNS(NS, tag); for (const k in a) e.setAttribute(k, a[k]); parent.appendChild(e); return e; };
  const stroked = [], imgs = [];
  const S = (e, w) => { if (w) stroked.push([e, w]); return e; };
  const L = GEO.lab;
  const q = (a, b, bend = 0.15) => { const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, dx = b[0] - a[0], dy = b[1] - a[1];
    return `M${a[0]} ${a[1]} Q ${mx - dy * bend} ${my + dx * bend}, ${b[0]} ${b[1]}`; };
  (opts.layers || []).forEach((ly) => {
    if (ly.img) {
      const k = 2 ** (ly.z - Z0);
      const e = el("image", { href: ly.img, x: ly.x0 / k, y: ly.y0 / k, width: ly.w / k, height: ly.h / k, id: ly.id || "", preserveAspectRatio: "none" });
      imgs.push([e, ly.show]); return;
    }
    let d;
    if (ly.link) d = q(L[ly.link[0]], L[ly.link[1]], ly.bend ?? 0.15);
    else { const [ns, key] = ly.geo.split(":"); d = ns === "prov" ? GEO.prov[key] : ns === "lines" ? GEO.lines[key] : GEO[key]; }
    if (!d) { console.warn("vmap: thiếu", ly.geo); return; }
    const a = { d, class: ly.cls || "", id: ly.id || "" };
    if (ly.len || ly.link) a.pathLength = 100;
    S(el("path", a), ly.w);
  });
  const rings = (opts.rings || []).map(([, , , pt]) => S(el("circle", { cx: L[pt][0], cy: L[pt][1], r: 1, class: "ring" }), 4));
  // nhãn HTML (kiểu A tự dựng đường dẫn; kiểu B đặt theo dx/dy)
  const labels = [...document.querySelectorAll(opts.labels)].map((n) => ({ n, p: L[n.dataset.at], dx: +(n.dataset.dx || 0), dy: +(n.dataset.dy || 0) }));
  labels.forEach(({ n, p }) => { if (!p) console.warn("vmap: nhãn thiếu toạ độ", n.dataset.at); });
  document.querySelectorAll(opts.labels + ".la").forEach((n) => {
    const lx = +(n.dataset.lx || 0), ly = +(n.dataset.ly || 0), al = n.dataset.align || (lx >= 0 ? "l" : "r");
    const lead = n.querySelector(".lead"), tx = n.querySelector(".tx");
    if (lead) { lead.style.width = Math.hypot(lx, ly) + "px"; lead.style.transform = `rotate(${Math.atan2(ly, lx)}rad)`; }
    if (tx) { const gx = al === "l" ? 10 : al === "r" ? -10 : 0, gy = al === "c" ? (ly >= 0 ? 12 : -12) : 0;
      tx.style.left = (lx + gx) + "px"; tx.style.top = (ly + gy) + "px";
      tx.style.transform = al === "l" ? "translate(0,-50%)" : al === "r" ? "translate(-100%,-50%)" : (ly >= 0 ? "translate(-50%,0)" : "translate(-50%,-100%)");
      tx.style.textAlign = al === "r" ? "right" : al === "c" ? "center" : "left"; }
  });
  // camera Hermite đơn điệu trên (x, y, Z): vận tốc liên tục, không vọt lố
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
    imgs.forEach(([e, show]) => { if (!show) return; const [a, b] = show; e.style.opacity = String(Math.min(1, Math.max(0, (c.Z - a) / (b - a)))); });
    (opts.rings || []).forEach(([t0, dur, rmax], i) => { const r = rings[i]; const p = (t - t0) / dur;
      if (p < 0 || p > 1) { r.style.opacity = "0"; return; }
      r.setAttribute("r", ((10 + (rmax - 10) * (1 - (1 - p) ** 2)) / s).toFixed(3)); r.style.opacity = (0.95 * (1 - p)).toFixed(3); });
    labels.forEach(({ n, p, dx, dy }) => { if (p) n.style.transform = `translate(${(p[0] * s + tx + dx).toFixed(1)}px, ${(p[1] * s + ty + dy).toFixed(1)}px)`; });
  }
  return { apply, sample };
}
