// Quay một cảnh Google Earth 3D thành chuỗi khung JPG, camera nội suy đều giữa 2 điểm (không dừng).
// Dùng:  node earth_capture.js shot.json <thư mục ra> [khung bắt đầu, để chạy tiếp]
// shot.json: {"dpr":1.5,"frames":80,"from":{lat,lng,dist,head,tilt},"to":{...}}  (10 khung = 1 giây)
//            hoặc {"dpr":1,"list":[{...},{...}],"frames":N} để chụp thử nhiều góc máy.
// dist: khoảng cách camera (m), log-nội suy; head: hướng (độ); tilt: nghiêng (độ, 0 = nhìn thẳng xuống).
// Cần mạng tới earth.google.com, kh.google.com, www.gstatic.com, www.google.com, earth-pa.clients6.google.com, htapi.google.com.
// Toạ độ click giao diện (đóng popup, Basemap -> Clean) đo ở viewport 540×960; Google đổi giao diện thì cần đo lại.
const { chromium } = require('playwright');
const fs = require('fs');
const [,, specFile, outDir, startArg] = process.argv;
const spec = JSON.parse(fs.readFileSync(specFile, 'utf8'));
if (startArg) spec.start = parseInt(startArg, 10);
fs.mkdirSync(outDir, { recursive: true });
const url = (c) => `https://earth.google.com/web/@${c.lat.toFixed(6)},${c.lng.toFixed(6)},${c.alt.toFixed(1)}a,${c.dist.toFixed(1)}d,${spec.fov || 35}y,${c.head.toFixed(2)}h,${c.tilt.toFixed(2)}t,0r`;
const lerp = (a, b, s) => a + (b - a) * s;
function cam(i) {
  if (spec.list) return Object.assign({ alt: 10 }, spec.list[i]);
  const s = spec.frames <= 1 ? 0 : i / (spec.frames - 1);
  const A = spec.from, B = spec.to;
  return { lat: lerp(A.lat, B.lat, s), lng: lerp(A.lng, B.lng, s), alt: lerp(A.alt || 10, B.alt || 10, s),
           dist: Math.exp(lerp(Math.log(A.dist), Math.log(B.dist), s)), head: lerp(A.head, B.head, s), tilt: lerp(A.tilt, B.tilt, s) };
}
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: spec.w || 540, height: spec.h || 960 }, deviceScaleFactor: spec.dpr || 2 });
  await p.goto(url(cam(spec.start || 0)), { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(45000);
  // giao diện ở 540×960 CSS px: đóng popup, chọn Basemap → Clean (không nhãn/đường/biên giới)
  await p.mouse.click(455, 228); await p.waitForTimeout(1500);
  await p.mouse.click(49, 864); await p.waitForTimeout(1000);
  await p.mouse.click(500, 40); await p.waitForTimeout(2500);
  await p.mouse.click(507, 288); await p.waitForTimeout(1500);
  await p.mouse.click(28, 28); await p.waitForTimeout(8000);
  await p.evaluate(() => { const c = document.getElementById('earth-canvas'); document.body.appendChild(c);
    c.style.cssText = 'position:fixed;left:0;top:0;width:100vw;height:100vh;z-index:2147483647;'; });
  let prev = null;
  for (let i = spec.start || 0; i < spec.frames; i++) {
    const t0 = Date.now();
    await p.evaluate((u) => { history.replaceState(null, '', u); window.dispatchEvent(new PopStateEvent('popstate')); }, url(cam(i)));
    // chờ cố định: camera dịch rất ít mỗi khung nên tile gần như đã có sẵn
    await p.waitForTimeout(i === (spec.start || 0) ? 6000 : (spec.wait || 1800));
    const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
    fs.writeFileSync(`${outDir}/f${String(i).padStart(4, '0')}.jpg`, buf);
    if (i % 10 === 0) console.log(`frame ${i}/${spec.frames} ${(Date.now() - t0)}ms`);
  }
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
