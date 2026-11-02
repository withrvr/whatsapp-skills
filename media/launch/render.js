// node render.js stills t1 t2 ...   -> stills/t_<t>.png
// node render.js full <fps> <duration> [fromFrame] -> frames/0000.png ...
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [mode, ...rest] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(__dirname, 'launch.html'));
  await page.evaluate(() => window.ready);
  await page.waitForTimeout(300);
  const shot = async (t, file) => {
    await page.evaluate(t => window.render(t), t);
    await page.screenshot({ path: file, type: 'png' });
  };
  if (mode === 'stills') {
    require('fs').mkdirSync(path.resolve(__dirname, 'stills'), { recursive: true });
    for (const t of rest.map(Number)) await shot(t, path.resolve(__dirname, 'stills', `t_${t.toFixed(2)}.png`));
  } else {
    const fps = Number(rest[0] || 30), dur = Number(rest[1] || 22);
    const n = Math.round(fps * dur);
    const from = Number(rest[2] || 0);
    for (let f = from; f < n; f++) {
      await shot(f / fps, path.resolve(__dirname, 'frames', String(f).padStart(4, '0') + '.png'));
      if (f % 60 === 0) console.log(`frame ${f}/${n}`);
    }
  }
  await browser.close();
})();
