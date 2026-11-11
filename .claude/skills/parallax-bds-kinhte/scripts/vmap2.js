// ===== vmap2.js — bản đồ "neon trên vệ tinh" cho motion.py =====
// GEO (geo_build.py) nhúng sẵn. makeMap2(opts):
//  opts.sat: [{img,z,x0,y0,w,h,show:[Za,Zb]|null}]          nền vệ tinh nhiều mức (đã làm tối, giảm bão hoà)
//  opts.layers: [{geo:"prov:X"|"lines:K", kind:"adm|proj|water|green|route", fill:bool, id, w, len}]
//  opts.links: [{a:"pt", b:"pt", bend, kind, id, w}]       đường nối giữa 2 điểm (route A->B)
//  opts.movers: [{path:id, t, d, icon:"car|train|boat|dot"}] icon chạy theo path (M6 đầu chấm, M9)
//  opts.rings: [{pt, t, km:[5,10,15]}]                      vòng bán kính theo km thật (M7)
//  opts.keys: [[t,lat,lng,Z(,carry)]]                       camera Hermite
// Trả về { apply(t), speedZ(t) } — speedZ dùng cho blur khi zoom nhanh (M2).
function makeMap2(opts) {
  const W = 1080, H = 1920, Z0 = GEO.Z, NS = "http://www.w3.org/2000/svg";
  // opts.pad: SVG lớn hơn khung (trái/trên) để khi nghiêng 3D (M3) mặt phẳng vẫn phủ kín màn hình
  const PL = (opts.pad || [0, 0])[0], PT = (opts.pad || [0, 0])[1];
  const svg = document.querySelector(opts.svg), world = svg.querySelector(".world");
  const el = (tag, a, parent = world) => { const e = document.createElementNS(NS, tag); for (const k in a) e.setAttribute(k, a[k]); parent.appendChild(e); return e; };
  const stroked = [], imgs = [], movers = [], rings = [];
  const S = (e, w) => { stroked.push([e, w]); return e; };
  const L = GEO.lab;
  (opts.sat || []).forEach((m) => { const k = 2 ** (m.z - Z0);
    imgs.push([el("image", { href: m.img, x: m.x0 / k, y: m.y0 / k, width: m.w / k, height: m.h / k, preserveAspectRatio: "none" }), m.show]); });
  const q = (a, b, bend = 0.15) => { const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, dx = b[0] - a[0], dy = b[1] - a[1];
    return `M${a[0]} ${a[1]} Q ${mx - dy * bend} ${my + dx * bend}, ${b[0]} ${b[1]}`; };
  const addLine = (d, ly) => {
    const kind = ly.kind || "adm", w = ly.w || 5, id = ly.id || "";
    const g = el("g", { id, class: "lyr k-" + kind });
    if (ly.fill) S(el("path", { d, class: "fill", id: id + "-fill" }, g), 0);
    const ga = { d, class: "glow", id: id + "-glow" }, ca = { d, class: "core", id: id + "-core" };
    if (ly.len) { ga.pathLength = 100; ca.pathLength = 100; ga.class += " len"; ca.class += " len"; }
    S(el("path", ga, g), w * 3.2); S(el("path", ca, g), w);
    return g;
  };
  (opts.layers || []).forEach((ly) => { const [ns, key] = ly.geo.split(":");
    const d = ns === "prov" ? GEO.prov[key] : ns === "lines" ? GEO.lines[key] : GEO[key];
    if (!d) { console.warn("vmap2: thiếu", ly.geo); return; } addLine(d, ly); });
  (opts.links || []).forEach((lk) => addLine(q(L[lk.a], L[lk.b], lk.bend ?? 0.15), Object.assign({ len: true, kind: "route" }, lk)));
  const ICON = {
    car: '<rect x="-14" y="-8" width="28" height="16" rx="5" fill="#fff"/><rect x="-7" y="-6" width="11" height="12" rx="2" fill="#E04BD6"/>',
    train: '<rect x="-17" y="-9" width="34" height="18" rx="8" fill="#fff"/><rect x="-11" y="-5" width="8" height="7" rx="1.5" fill="#E04BD6"/><rect x="2" y="-5" width="8" height="7" rx="1.5" fill="#E04BD6"/>',
    boat: '<path d="M-16 0 L16 0 L10 9 L-10 9 Z" fill="#fff"/><path d="M-2 0 L-2 -14 L9 -2 Z" fill="#2FD3E0"/>',
    dot: '<circle r="9" fill="#fff"/><circle r="16" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="3"/>',
  };
  (opts.movers || []).forEach((mv) => {
    const path = svg.querySelector("#" + mv.path + "-core"); if (!path) return;
    const g = el("g", { class: "mover", opacity: 0 }); g.innerHTML = ICON[mv.icon || "dot"];
    movers.push({ g, path, len: path.getTotalLength(), mv });
  });
  (opts.rings || []).forEach((rg) => { const lat = rg.lat || 11;
    const mpp = (156543.03 * Math.cos((lat * Math.PI) / 180)) / 2 ** Z0;
    rg.km.forEach((km, i) => { const c = S(el("circle", { cx: L[rg.pt][0], cy: L[rg.pt][1], r: 0.01, class: "ringc" }), 4);
      rings.push({ c, R: (km * 1000) / mpp, t0: rg.t + i * 0.45 }); }); });
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
  const labels = [...document.querySelectorAll(opts.labels)].map((n) => ({ n, p: L[n.dataset.at] }));
  function apply(t) {
    const c = sample(t), s = 2 ** (c.Z - Z0), tx = W / 2 - c.x * s, ty = H / 2 - c.y * s;
    world.setAttribute("transform", `translate(${(tx + PL).toFixed(2)} ${(ty + PT).toFixed(2)}) scale(${s.toFixed(5)})`);
    stroked.forEach(([e, w]) => w && e.setAttribute("stroke-width", (w / s).toFixed(4)));
    imgs.forEach(([e, show]) => { if (show) e.style.opacity = String(Math.min(1, Math.max(0, (c.Z - show[0]) / (show[1] - show[0])))); });
    movers.forEach(({ g, path, len, mv }) => { const p = (t - mv.t) / mv.d;
      if (p < 0) { g.setAttribute("opacity", 0); return; }
      const e = Math.min(1, p), pe = e < 0.5 ? 2 * e * e : 1 - (-2 * e + 2) ** 2 / 2, pt = path.getPointAtLength(len * pe),
        pt2 = path.getPointAtLength(Math.min(len, len * pe + 0.5)), ang = (Math.atan2(pt2.y - pt.y, pt2.x - pt.x) * 180) / Math.PI;
      g.setAttribute("opacity", 1);
      g.setAttribute("transform", `translate(${pt.x} ${pt.y}) scale(${((mv.size || 2) / s).toFixed(5)}) rotate(${mv.icon === "dot" ? 0 : ang})`); });
    rings.forEach(({ c: ci, R, t0 }) => { const p = Math.min(1, Math.max(0, (t - t0) / 0.8)); ci.setAttribute("r", Math.max(0.01, R * (1 - (1 - p) ** 3)));
      ci.style.opacity = p > 0 ? 1 : 0; });
    labels.forEach(({ n, p }) => { if (p) n.style.transform = `translate(${(p[0] * s + tx).toFixed(1)}px, ${(p[1] * s + ty).toFixed(1)}px)`; });
  }
  const speedZ = (t) => Math.abs(sample(t + 0.04).Z - sample(t - 0.04).Z) / 0.08;
  return { apply, sample, speedZ, rings };
}
