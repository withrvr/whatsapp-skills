// node render.js stills t1 t2 ...   -> stills/t_<t>.png
// Env: HTML (composition file, default launch.html next to this script),
//      W / H (viewport, default 1080x1080), OUT (output folder, default this folder)
// node render.js full <fps> <duration> [fromFrame] -> frames/0000.png ...
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [mode, ...rest] = process.argv.slice(2);
  const browser = await chromium.launch();
  const W = Number(process.env.W || 1080), H = Number(process.env.H || 1080);
  const OUT = process.env.OUT ? path.resolve(process.env.OUT) : __dirname;
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(process.env.HTML || path.resolve(__dirname, 'launch.html')));
  await page.evaluate(() => window.ready);
  await page.waitForTimeout(300);
  const shot = async (t, file) => {
    await page.evaluate(t => window.render(t), t);
    await page.screenshot({ path: file, type: 'png' });
  };
  if (mode === 'stills') {
    require('fs').mkdirSync(path.resolve(OUT, 'stills'), { recursive: true });
    for (const t of rest.map(Number)) await shot(t, path.resolve(OUT, 'stills', `t_${t.toFixed(2)}.png`));
  } else {
    const fps = Number(rest[0] || 30), dur = Number(rest[1] || 22);
    const n = Math.round(fps * dur);
    const from = Number(rest[2] || 0);
    for (let f = from; f < n; f++) {
      await shot(f / fps, path.resolve(OUT, 'frames', String(f).padStart(4, '0') + '.png'));
      if (f % 60 === 0) console.log(`frame ${f}/${n}`);
    }
  }
  await browser.close();
})();
