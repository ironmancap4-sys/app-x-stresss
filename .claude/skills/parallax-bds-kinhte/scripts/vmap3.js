// ===== vmap3.js — MỘT camera liên tục trên MỘT bản đồ sống (flight.py) =====
// GEO (geo_build.py) nhúng sẵn. makeMap3(opts):
//  opts.keys: [[t,lat,lng,Z,pitch,bearing]]  camera Hermite đơn điệu trên CẢ 5 kênh (không giật, không dừng gắt)
//  opts.sat: [{img,z,x0,y0,w,h,show:[Za,Zb]|null, hide:[Za,Zb]}]  nền vệ tinh nhiều mức (hiện/ẩn theo Z)
//  opts.layers / opts.links / opts.movers / opts.rings  như vmap2 (rings có thể có id)
//  opts.circles: [{id, pt, r_m, kind, heat}]   hình tròn đúng diện tích theo mét (V5) hoặc điểm nóng (V8)
//  opts.blocks: [{lng,lat,w,d,ang,g}]           khối 3D mọc từ mặt đất (V6); chiều cao theo nhóm g: window.BH[g] (0..1) × opts.blockH[g] (m)
//  opts.pad: [trái, trên]                       SVG rộng hơn khung để khi nghiêng/xoay vẫn phủ kín
// Trả về { apply(t) -> camera, sample(t) }.
function makeMap3(opts) {
  const W = 1080, H = 1920, Z0 = GEO.Z, NS = "http://www.w3.org/2000/svg";
  const PL = (opts.pad || [0, 0])[0], PT = (opts.pad || [0, 0])[1];
  const svg = document.querySelector(opts.svg), world = svg.querySelector(".world");
  const el = (tag, a, parent = world) => { const e = document.createElementNS(NS, tag); for (const k in a) e.setAttribute(k, a[k]); parent.appendChild(e); return e; };
  const stroked = [], imgs = [], movers = [], rings = [];
  const S = (e, w) => { stroked.push([e, w]); return e; };
  const L = GEO.lab;
  const mx = (lng) => ((lng + 180) / 360) * 256 * 2 ** Z0;
  const my = (lat) => { const r = (lat * Math.PI) / 180; return ((1 - Math.log(Math.tan(r) + 1 / Math.cos(r)) / Math.PI) / 2) * 256 * 2 ** Z0; };
  const m2w = (lat) => 2 ** Z0 / (156543.03 * Math.cos((lat * Math.PI) / 180));   // mét -> đơn vị thế giới (Z0)
  const defs = el("defs", {});
  defs.innerHTML = '<radialGradient id="heatg"><stop offset="0" stop-color="#FACC15" stop-opacity=".85"/><stop offset=".45" stop-color="#F28C28" stop-opacity=".45"/><stop offset="1" stop-color="#F28C28" stop-opacity="0"/></radialGradient>';
  (opts.sat || []).forEach((m) => { const k = 2 ** (m.z - Z0);
    imgs.push([el("image", { href: m.img, x: m.x0 / k, y: m.y0 / k, width: m.w / k, height: m.h / k, preserveAspectRatio: "none" }), m.show, m.hide]); });
  const q = (a, b, bend = 0.15) => { const mx_ = (a[0] + b[0]) / 2, my_ = (a[1] + b[1]) / 2, dx = b[0] - a[0], dy = b[1] - a[1];
    return `M${a[0]} ${a[1]} Q ${mx_ - dy * bend} ${my_ + dx * bend}, ${b[0]} ${b[1]}`; };
  const addLine = (d, ly) => {
    const kind = ly.kind || "adm", w = ly.w || 5, id = ly.id || "";
    const g = el("g", { id, class: "lyr k-" + kind + (ly.cls ? " " + ly.cls : ""), opacity: ly.op ?? 0 });
    if (ly.fill) S(el("path", { d, class: "fill", id: id + "-fill", style: "opacity:0" }, g), 0);
    const ga = { d, class: "glow", id: id + "-glow" }, ca = { d, class: "core", id: id + "-core" };
    if (ly.len) { ga.pathLength = 100; ca.pathLength = 100; ga.class += " len"; ca.class += " len"; }
    S(el("path", ga, g), w * 3.2); S(el("path", ca, g), w);
    return g;
  };
  (opts.layers || []).forEach((ly) => { const [ns, key] = ly.geo.split(":");
    const d = ns === "prov" ? GEO.prov[key] : ns === "lines" ? GEO.lines[key] : GEO[key];
    if (!d) { console.warn("vmap3: thiếu", ly.geo); return; } addLine(d, ly); });
  (opts.links || []).forEach((lk) => addLine(q(L[lk.a], L[lk.b], lk.bend ?? 0.15), Object.assign({ len: true, kind: "route" }, lk)));
  const host0 = () => document.querySelector(opts.blockHost || "body"), discs = [];
  (opts.circles || []).forEach((c) => { const p = L[c.pt], R = c.r_m * m2w(c.lat || 11);
    const e = document.createElement("div"); e.id = c.id; e.className = "disc " + (c.heat ? "heat" : "k-" + (c.kind || "proj")); e.style.opacity = 0;
    host0().appendChild(e); discs.push({ e, p, R }); });
  const ICON = {
    car: '<rect x="-14" y="-8" width="28" height="16" rx="5" fill="#fff"/><rect x="-7" y="-6" width="11" height="12" rx="2" fill="#E04BD6"/>',
    train: '<rect x="-17" y="-9" width="34" height="18" rx="8" fill="#fff"/><rect x="-11" y="-5" width="8" height="7" rx="1.5" fill="#E04BD6"/><rect x="2" y="-5" width="8" height="7" rx="1.5" fill="#E04BD6"/>',
    bike: '<circle r="13" fill="#fff"/><path d="M-7 3 L-2 -5 L5 3 M-2 -5 L3 -5" stroke="#2FD3E0" stroke-width="2.6" fill="none" stroke-linecap="round"/><circle cx="-7" cy="3" r="3.2" fill="none" stroke="#2FD3E0" stroke-width="2"/><circle cx="6" cy="3" r="3.2" fill="none" stroke="#2FD3E0" stroke-width="2"/>',
    plane: '<path d="M14 0 L-6 -12 L-3 -2 L-12 -2 L-15 -7 L-17 -7 L-15 0 L-17 7 L-15 7 L-12 2 L-3 2 L-6 12 Z" fill="#fff"/>',
    dot: '<circle r="9" fill="#fff"/><circle r="16" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="3"/>',
  };
  (opts.movers || []).forEach((mv) => {
    const path = svg.querySelector("#" + mv.path + "-core"); if (!path) return;
    const g = el("g", { class: "mover", opacity: 0 }); g.innerHTML = ICON[mv.icon || "dot"];
    movers.push({ g, path, len: path.getTotalLength(), mv });
  });
  (opts.rings || []).forEach((rg) => { const lat = rg.lat || 11;
    rg.km.forEach((km, i) => { const e = document.createElement("div"); e.className = "ring"; if (rg.id) e.dataset.g = rg.id; host0().appendChild(e);
      rings.push({ e, p: L[rg.pt], R: km * 1000 * m2w(lat), t0: rg.t + i * 0.45, t1: rg.out ?? 1e9 }); }); });
  // ---- khối 3D (V6)
  const host = document.querySelector(opts.blockHost || "body"), blocks = [];
  window.BH = window.BH || {};
  (opts.blocks || []).forEach((b) => {
    const e = document.createElement("div"); e.className = "blk g-" + b.g;
    e.innerHTML = '<i class="f top"></i><i class="f s1"></i><i class="f s2"></i><i class="f s3"></i><i class="f s4"></i>';
    host.appendChild(e); const k = m2w(b.lat);
    blocks.push({ e, f: [...e.children], x: mx(b.lng), y: my(b.lat), w: b.w * k, d: b.d * k, ang: b.ang || 0, g: b.g, k }); });
  // ---- camera Hermite 5 kênh
  const KEYS = opts.keys.map(([t, lat, lng, Z, p = 0, b = 0]) => ({ t, x: mx(lng), y: my(lat), Z, p, b }));
  const TS = KEYS.map((k) => k.t);
  const slopes = (vs) => { const n = vs.length, dl = [], m = new Array(n).fill(0);
    for (let k = 0; k < n - 1; k++) dl[k] = (vs[k + 1] - vs[k]) / (TS[k + 1] - TS[k]);
    m[0] = 0; m[n - 1] = 0;
    for (let k = 1; k < n - 1; k++) m[k] = dl[k - 1] * dl[k] <= 0 ? 0 : (dl[k - 1] + dl[k]) / 2;
    for (let k = 0; k < n - 1; k++) { if (dl[k] === 0) { m[k] = 0; m[k + 1] = 0; continue; }
      const a = m[k] / dl[k], b = m[k + 1] / dl[k], s = a * a + b * b;
      if (s > 9) { const tau = 3 / Math.sqrt(s); m[k] = tau * a * dl[k]; m[k + 1] = tau * b * dl[k]; } }
    return m; };
  const CH = ["x", "y", "Z", "p", "b"], C = {};
  CH.forEach((c) => { const vs = KEYS.map((k) => k[c]); C[c] = { vs, m: slopes(vs) }; });
  const sample = (t) => { t = Math.min(Math.max(t, TS[0]), TS[TS.length - 1]); let i = 0; while (i < TS.length - 2 && t > TS[i + 1]) i++;
    const h = TS[i + 1] - TS[i], s = (t - TS[i]) / h, s2 = s * s, s3 = s2 * s, o = {};
    CH.forEach((c) => { const { vs, m } = C[c];
      o[c] = (2 * s3 - 3 * s2 + 1) * vs[i] + (s3 - 2 * s2 + s) * h * m[i] + (-2 * s3 + 3 * s2) * vs[i + 1] + (s3 - s2) * h * m[i + 1]; });
    return o; };
  const labels = [...document.querySelectorAll(opts.labels)].map((n) => ({ n, p: L[n.dataset.at] }));
  // ---- mờ chuyển động theo vận tốc camera (màn trập 180° = nửa quãng đi trong 1 khung)
  // Lọc trên khung nhìn 1080×1920 (opts.blurHost), không lọc cả SVG khổng lồ; chỉ bật khi vệt ≥ 2 px (dưới đó mắt không thấy).
  const MB = opts.motionBlur, fps = opts.fps || 30;
  let mbHost = null, fe = null;
  if (MB) { mbHost = document.querySelector(opts.blurHost);
    const ns = document.createElementNS(NS, "svg"); ns.setAttribute("width", 0); ns.setAttribute("height", 0); ns.style.position = "absolute";
    ns.innerHTML = '<filter id="mbf" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB"><feGaussianBlur id="mbg" stdDeviation="0 0" edgeMode="duplicate"/></filter>';
    document.body.appendChild(ns); fe = ns.querySelector("#mbg"); }
  function blurAt(t) {
    if (!MB) return;
    const a = sample(t - 0.5 / fps), b = sample(t + 0.5 / fps), s = 2 ** ((a.Z + b.Z) / 2 - Z0), sh = (MB.shutter || 180) / 360;
    const br = ((a.b + b.b) / 2) * Math.PI / 180, mx_ = (b.x - a.x) * s, my_ = (b.y - a.y) * s;
    const vx = Math.abs(mx_ * Math.cos(br) - my_ * Math.sin(br)), vy = Math.abs(mx_ * Math.sin(br) + my_ * Math.cos(br)) * (1 + a.p / 90);
    const rad = (Math.abs(b.Z - a.Z) * Math.LN2 * 540 + Math.abs(b.b - a.b) * Math.PI / 180 * 540) * 0.5;
    const Lx = (vx + rad) * sh, Ly = (vy + rad) * sh;                      // độ dài vệt (px)
    if (Math.max(Lx, Ly) < (MB.min || 2)) { mbHost.style.filter = ""; return; }
    fe.setAttribute("stdDeviation", `${(Lx / 3.46).toFixed(2)} ${(Ly / 3.46).toFixed(2)}`); mbHost.style.filter = "url(#mbf)";
  }
  function apply(t) {
    blurAt(t);
    const c = sample(t), s = 2 ** (c.Z - Z0), tx = W / 2 - c.x * s, ty = H / 2 - c.y * s;
    world.setAttribute("transform", `translate(${(tx + PL).toFixed(2)} ${(ty + PT).toFixed(2)}) scale(${s.toFixed(6)})`);
    stroked.forEach(([e, w]) => w && e.setAttribute("stroke-width", (w / s).toFixed(5)));
    imgs.forEach(([e, show, hide]) => { let o = 1;
      if (show) o = Math.min(1, Math.max(0, (c.Z - show[0]) / (show[1] - show[0])));
      if (hide) o *= Math.min(1, Math.max(0, (hide[1] - c.Z) / (hide[1] - hide[0])));
      e.style.opacity = String(o); e.style.display = o > 0.001 ? "" : "none"; });
    movers.forEach(({ g, path, len, mv }) => { const p = (t - mv.t) / mv.d;
      if (p < 0 || (mv.out && t > mv.out)) { g.setAttribute("opacity", 0); return; }
      const e = Math.min(1, p), pe = e < 0.5 ? 2 * e * e : 1 - (-2 * e + 2) ** 2 / 2, pt = path.getPointAtLength(len * pe),
        pt2 = path.getPointAtLength(Math.min(len, len * pe + 0.5)), ang = (Math.atan2(pt2.y - pt.y, pt2.x - pt.x) * 180) / Math.PI;
      g.setAttribute("opacity", 1);
      g.setAttribute("transform", `translate(${pt.x} ${pt.y}) scale(${((mv.size || 2) / s).toFixed(6)}) rotate(${mv.icon === "dot" || mv.icon === "bike" ? 0 : ang})`); });
    const place = (e, p, r) => { e.style.width = e.style.height = (2 * r).toFixed(1) + "px";
      e.style.transform = `translate(${(p[0] * s + tx - r).toFixed(1)}px, ${(p[1] * s + ty - r).toFixed(1)}px)`; };
    rings.forEach(({ e, p, R, t0, t1 }) => { const k = Math.min(1, Math.max(0, (t - t0) / 0.8)), fo = t > t1 ? Math.max(0, 1 - (t - t1) / 0.6) : 1;
      e.style.opacity = k > 0 ? fo : 0; if (k > 0 && fo > 0) place(e, p, R * s * (1 - (1 - k) ** 3)); });
    discs.forEach(({ e, p, R }) => place(e, p, R * s));
    // nhãn nằm trên mặt bản đồ nhưng xoay ngược bearing để luôn đọc thẳng
    labels.forEach(({ n, p }) => { if (p) n.style.transform = `translate(${(p[0] * s + tx).toFixed(1)}px, ${(p[1] * s + ty).toFixed(1)}px) rotate(${(-c.b).toFixed(2)}deg)`; });
    blocks.forEach((b) => { const g = window.BH[b.g] || 0;
      if (g <= 0.001) { b.e.style.display = "none"; return; } b.e.style.display = "";
      const w = b.w * s, d = b.d * s, h = (opts.blockH?.[b.g] || 20) * b.k * s * g;
      b.e.style.width = w + "px"; b.e.style.height = d + "px";
      b.e.style.transform = `translate(${(b.x * s + tx - w / 2).toFixed(1)}px, ${(b.y * s + ty - d / 2).toFixed(1)}px) rotate(${b.ang}deg)`;
      const [top, s1, s2, s3, s4] = b.f;
      top.style.transform = `translateZ(${h.toFixed(2)}px)`;
      s1.style.cssText = `width:${w}px;height:${h}px;top:0;transform:rotateX(90deg)`;
      s2.style.cssText = `width:${w}px;height:${h}px;top:${d}px;transform:rotateX(90deg)`;
      s3.style.cssText = `width:${h}px;height:${d}px;left:0;transform:rotateY(-90deg)`;
      s4.style.cssText = `width:${h}px;height:${d}px;left:${w}px;transform:rotateY(-90deg)`; });
    return c;
  }
  const speed = (t) => { const a = sample(t - 0.05), b = sample(t + 0.05), s = 2 ** (a.Z - Z0);
    return { pan: Math.hypot(b.x - a.x, b.y - a.y) * s / 0.1, Z: Math.abs(b.Z - a.Z) / 0.1, p: Math.abs(b.p - a.p) / 0.1, b: Math.abs(b.b - a.b) / 0.1 }; };
  return { apply, sample, speed };
}
