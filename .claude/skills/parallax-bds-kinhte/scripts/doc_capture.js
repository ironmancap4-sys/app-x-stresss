// Chụp bài báo gốc làm ảnh tài liệu bằng chứng (tiêu đề, ngày, ảnh, các đoạn chứa số liệu).
// Dùng: node doc_capture.js <url> "<câu đầu tiêu đề>" "<chuỗi trong đoạn số 1>" "<chuỗi đoạn số 2>" "<chuỗi đoạn số 3>"
// Ra: article.png (2x) + article.json (vị trí tiêu đề và các đoạn, để zoom/đánh dấu). Cần host báo trong danh sách mạng.
const { chromium } = require('playwright');
const [, , URL, TITLE, P1, P2, P3] = process.argv;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 1400 }, deviceScaleFactor: 2 });
  await p.goto(URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await p.waitForTimeout(6000);
  // ẩn quảng cáo/popup cố định
  await p.addStyleTag({ content: '[class*=ads],[id*=ads],[class*=banner],[class*=popup],iframe,.fixed,[style*="position: fixed"]{display:none!important}' });
  await p.evaluate(() => { for (const e of document.querySelectorAll('*')) { const ps = getComputedStyle(e).position; if (ps === 'fixed' || ps === 'sticky') e.style.setProperty('display','none','important'); } });
  const info = await p.evaluate(([TITLE, P1, P2, P3]) => {
    const ps = [...document.querySelectorAll('p')];
    const find = (s) => { const el = ps.find(e => e.textContent.includes(s)); if (!el) return null; el.scrollIntoView({block:'center'}); const r = el.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height, text: el.textContent.slice(0, 80) }; };
    const tt = TITLE;
    const h1 = [...document.querySelectorAll('h1,h2,div,span')].filter(e => e.children.length === 0 && e.textContent.trim().startsWith(tt))[0]
      || [...document.querySelectorAll('*')].find(e => e.childElementCount===0 && e.textContent.includes(tt));
    h1.scrollIntoView({block:'center'}); const hr = h1.getBoundingClientRect();
    return { title: { x: hr.left + scrollX, y: hr.top + scrollY, w: hr.width, h: hr.height, text: h1.textContent.trim() },
             retail: find(P1), biz: find(P2), fdi: find(P3), docH: document.documentElement.scrollHeight };
  }, [TITLE, P1, P2, P3]);
  console.log(JSON.stringify(info, null, 1));
  await p.evaluate(() => { scrollTo(0, 0); });
  await p.waitForTimeout(800);
  await p.evaluate(() => { for (const e of document.querySelectorAll('*')) { const ps = getComputedStyle(e).position; if (ps === 'fixed' || ps === 'sticky') e.style.setProperty('display','none','important'); } });
  const top = Math.max(0, info.title.y - 70), bottom = info.fdi.y + info.fdi.h + 60;
  await p.screenshot({ path: 'article.png', fullPage: true, clip: { x: info.title.x - 6, y: top, width: info.title.w + 12, height: bottom - top } });
  require('fs').writeFileSync('article.json', JSON.stringify({ ...info, clipTop: top }, null, 1));
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
