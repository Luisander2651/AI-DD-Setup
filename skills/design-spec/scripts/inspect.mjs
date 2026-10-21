#!/usr/bin/env node
// Inspector de diseño de ai-dd: abre una página en Chromium y deja capturas, una tira del scroll y
// un informe con medidas. Lo usa /design-spec (references/inspeccion.md) antes de enseñar opciones
// y /review para comprobar el movimiento. No instala nada: usa Playwright si ya está disponible
// (en el proyecto, global o en PLAYWRIGHT_PATH); si no, dilo y captura con otra herramienta.
//
// Uso:
//   node inspect.mjs <archivo.html | URL> [--out <dir>] [--widths 390,900,1440]
//                    [--mode persuadir|experiencia|operar|leer] [--film-step 0.33] [--max-frames 40]
//
// Salida en --out (por defecto .ai/inspect/<nombre>/): PNG por ancho (claro, oscuro, reducido),
// film-<ancho>-NN.png, report.json y report.md. Código 1 si hay algún FAIL.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const argv = process.argv.slice(2);
if (!argv.length || argv.includes('-h') || argv.includes('--help')) {
  console.log(fs.readFileSync(new URL(import.meta.url), 'utf8').split('\n').slice(1, 12).map(l => l.replace(/^\/\/ ?/, '')).join('\n'));
  process.exit(argv.length ? 0 : 2);
}
const opt = (name, def) => { const i = argv.indexOf(name); return i >= 0 ? argv[i + 1] : def; };
const target = argv.find((a, i) => !a.startsWith('--') && (i === 0 || !argv[i - 1].startsWith('--')));
const widths = opt('--widths', '390,900,1440').split(',').map(Number).filter(Boolean).sort((a, b) => a - b);
const mode = opt('--mode', 'persuadir');
const filmStep = Number(opt('--film-step', '0.33'));
const maxFrames = Number(opt('--max-frames', '40'));
const isUrl = /^https?:\/\//.test(target);
const url = isUrl ? target : pathToFileURL(path.resolve(target)).href;
const name = isUrl ? new URL(target).hostname : path.basename(target).replace(/\.[^.]+$/, '');
const out = path.resolve(opt('--out', path.join('.ai', 'inspect', name)));
fs.mkdirSync(out, { recursive: true });

async function loadPlaywright() {
  const require = createRequire(path.join(process.cwd(), 'noop.js'));
  const tries = [process.env.PLAYWRIGHT_PATH, 'playwright', 'playwright-core', '@playwright/test'].filter(Boolean);
  for (const t of tries) { try { return require(t); } catch {} }
  let g = '';
  try { g = execSync('npm root -g', { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim(); } catch {}
  for (const t of ['playwright', 'playwright-core', '@playwright/test', '@playwright/mcp/node_modules/playwright-core']) {
    try { return createRequire(path.join(g, 'noop.js'))(path.join(g, t)); } catch {}
  }
  return null;
}

const pw = await loadPlaywright();
if (!pw) {
  console.log('No encontré Playwright (ni en el proyecto, ni global, ni en PLAYWRIGHT_PATH).\n' +
    'Captura con la herramienta de navegador de la sesión y dilo en la crítica (inspeccion.md §4).');
  process.exit(3);
}
const launchOpts = { headless: true };
if (process.env.CHROMIUM_PATH) launchOpts.executablePath = process.env.CHROMIUM_PATH;
const browser = await pw.chromium.launch(launchOpts);

const findings = [];
const add = (level, code, width, detail) => findings.push({ level, code, width, detail });
const shots = [];

// Cuenta los elementos que de verdad se mueven: transiciones y animaciones CSS/WAAPI que arrancan.
const initScript = () => {
  window.__aidd = { moved: new Set(), errors: [] };
  const mark = e => { try { window.__aidd.moved.add(e.target); } catch {} };
  document.addEventListener('transitionrun', mark, true);
  document.addEventListener('animationstart', mark, true);
  new MutationObserver(ms => ms.forEach(m => window.__aidd.moved.add(m.target)))
    .observe(document, { attributes: true, attributeFilter: ['style'], subtree: true });
  const orig = Element.prototype.animate;
  Element.prototype.animate = function (...a) { window.__aidd.moved.add(this); return orig.apply(this, a); };
};

// Medidas dentro de la página.
const measure = () => {
  const vw = innerWidth, vh = innerHeight;
  const SEL = 'h1,h2,h3,h4,h5,h6,p,li,blockquote,img,svg,video,canvas,picture,figure,button,a,input,select,textarea,table,dd,dt';
  const effOpacity = el => { let o = 1; for (let n = el; n && n.nodeType === 1; n = n.parentElement) { const cs = getComputedStyle(n); o *= parseFloat(cs.opacity); if (cs.visibility === 'hidden') return 0; } return o; };
  const ignorable = el => el.closest('[aria-hidden="true"],[hidden],.sr-only,.visually-hidden,dialog:not([open]),[inert]') ||
    getComputedStyle(el).display === 'none' || (el.getClientRects().length === 0);
  const content = [...document.querySelectorAll(SEL)].filter(el => !ignorable(el) &&
    (el.matches('img,svg,video,canvas,picture,input,select,textarea') || el.textContent.trim().length > 1));
  const hidden = content.filter(el => {
    const r = el.getBoundingClientRect();
    return r.width > 4 && r.height > 4 && r.right > 0 && r.left < vw && effOpacity(el) < 0.05;
  }).slice(0, 12).map(el => `${el.tagName.toLowerCase()}${el.id ? '#' + el.id : ''} "${(el.textContent || el.getAttribute('alt') || '').trim().slice(0, 40)}"`);
  const heads = [...document.querySelectorAll('h1,h2,h3')].filter(h => !ignorable(h)).map(h => {
    const lh = parseFloat(getComputedStyle(h).lineHeight) || parseFloat(getComputedStyle(h).fontSize) * 1.2;
    return { tag: h.tagName.toLowerCase(), lines: Math.round(h.getBoundingClientRect().height / lh), text: h.textContent.trim().slice(0, 50) };
  });
  const faces = [...document.fonts].map(f => ({ family: f.family.replace(/["']/g, ''), status: f.status }));
  return {
    overflow: document.documentElement.scrollWidth - vw,
    height: document.documentElement.scrollHeight, vh,
    h1: document.querySelectorAll('h1').length,
    hidden, heads, faces,
    viewer: !!document.querySelector('.v-frame'),
    scenes: document.querySelectorAll('[data-scene], .scene').length,
    animations: document.getAnimations ? document.getAnimations().length : 0,
    moved: window.__aidd ? window.__aidd.moved.size : 0,
  };
};
const inView = () => {
  const vw = innerWidth, vh = innerHeight;
  const SEL = 'h1,h2,h3,h4,h5,h6,p,li,blockquote,img,svg,video,canvas,picture,figure,button,a,table,[data-scene] .scene-stage,[data-scene] [class*="stage"],[role="img"],[data-ui]';
  return [...document.querySelectorAll(SEL)].some(el => {
    const r = el.getBoundingClientRect();
    if (r.bottom < vh * 0.1 || r.top > vh * 0.9 || r.right < 0 || r.left > vw || r.width < 4) return false;
    let o = 1; for (let n = el; n && n.nodeType === 1; n = n.parentElement) o *= parseFloat(getComputedStyle(n).opacity);
    return o > 0.05;
  });
};

async function page(width, extra = {}) {
  const ctx = await browser.newContext({ viewport: { width, height: width < 600 ? 844 : width < 1100 ? 1100 : 900 }, ...extra });
  const p = await ctx.newPage();
  const external = new Set();
  p.on('request', r => { const u = r.url(); if (!isUrl && /^https?:/.test(u)) external.add(new URL(u).host); });
  p.on('pageerror', e => add('FAIL', 'error-js', width, String(e.message).slice(0, 160)));
  p.on('console', m => { if (m.type() === 'error') add('WARN', 'consola', width, m.text().slice(0, 160)); });
  await p.addInitScript(initScript);
  await p.goto(url, { waitUntil: 'load' });
  await p.waitForTimeout(1300);   // la carga debe terminar en 1,2 s
  return { ctx, p, external };
}

async function shot(p, file) { await p.screenshot({ path: path.join(out, file), fullPage: true }); shots.push(file); }

let viewer = false;
for (const w of widths) {
  const { ctx, p, external } = await page(w);
  const first = await p.evaluate(measure);
  viewer = first.viewer;
  if (first.overflow > 1) add('FAIL', 'desborde-horizontal', w, `${first.overflow}px más ancho que la ventana`);
  for (const f of first.faces) if (f.status !== 'loaded') add('WARN', 'fuente-no-cargada', w, f.family);
  if (external.size) add(viewer ? 'FAIL' : 'WARN', 'peticiones-externas', w, [...external].join(', '));
  await shot(p, `${w}-claro.png`);

  // Tira del scroll: un fotograma por cada ~1/3 de pantalla, solo en el menor y el mayor ancho.
  if (!viewer && (w === widths[0] || w === widths[widths.length - 1])) {
    const total = first.height - first.vh;
    const step = Math.max(1, Math.round(first.vh * filmStep));
    const n = Math.min(maxFrames, Math.floor(total / step) + 1);
    let empty = [];
    for (let i = 0; i < n; i++) {
      const y = Math.round(i * (total / Math.max(1, n - 1)));
      await p.evaluate(y => window.scrollTo(0, y), y);
      await p.waitForTimeout(220);
      const file = `film-${w}-${String(i).padStart(2, '0')}.png`;
      await p.screenshot({ path: path.join(out, file) });
      shots.push(file);
      if (!(await p.evaluate(inView))) empty.push(i);
    }
    if (empty.length) add('WARN', 'tramo-vacio', w, `fotogramas sin contenido visible: ${empty.join(', ')}`);
    await p.waitForTimeout(1000);
    const after = await p.evaluate(measure);
    // Tras recorrer la página y esperar, lo revelado debe estar visible: vuelve a recorrerla y mide.
    const hiddenAll = new Set();
    for (let y = 0; y <= total; y += first.vh) {
      await p.evaluate(y => window.scrollTo(0, y), y);
      await p.waitForTimeout(950);
      for (const h of (await p.evaluate(measure)).hidden) hiddenAll.add(h);
    }
    if (hiddenAll.size) add('FAIL', 'contenido-que-no-aparece', w, [...hiddenAll].slice(0, 8).join(' · '));
    const moved = after.moved;
    if (['persuadir', 'experiencia'].includes(mode)) {
      if (moved < 8) add('FAIL', 'pagina-quieta', w, `${moved} elementos se mueven al cargar y recorrer (mínimo 8)`);
      else if (moved < 16) add('WARN', 'poco-movimiento', w, `${moved} elementos se mueven (aviso por debajo de 16)`);
    }
    if (after.scenes > 3) add('WARN', 'muchas-escenas', w, `${after.scenes} escenas (máximo 3)`);
    fs.writeFileSync(path.join(out, `medidas-${w}.json`), JSON.stringify({ ...after, moved }, null, 2));
  }
  if (!viewer) {
    if (first.h1 !== 1) add('WARN', 'h1', w, `${first.h1} elementos h1 (se espera 1)`);
    for (const h of first.heads) if (h.lines > 2) add('WARN', 'titular-largo', w, `${h.tag} en ${h.lines} líneas: "${h.text}"`);
  }
  await ctx.close();
}

// Oscuro y movimiento reducido en el menor y el mayor ancho.
for (const w of [widths[0], widths[widths.length - 1]]) {
  const dark = await page(w, { colorScheme: 'dark' });
  await dark.p.evaluate(() => { const b = document.getElementById('toggle-scheme'); if (b && b.getAttribute('aria-pressed') === 'false') b.click(); });
  await dark.p.waitForTimeout(200);
  await shot(dark.p, `${w}-oscuro.png`);
  await dark.ctx.close();

  const red = await page(w, { reducedMotion: 'reduce' });
  await red.p.evaluate(() => { const b = document.getElementById('toggle-motion'); if (b && b.getAttribute('aria-pressed') === 'false') b.click(); });
  await red.p.waitForTimeout(300);
  const hid = new Set();
  const m0 = await red.p.evaluate(measure);
  for (let y = 0; y <= m0.height - m0.vh; y += m0.vh) {
    await red.p.evaluate(y => window.scrollTo(0, y), y);
    await red.p.waitForTimeout(150);
    for (const h of (await red.p.evaluate(measure)).hidden) hid.add(h);
  }
  if (hid.size) add('FAIL', 'oculto-con-movimiento-reducido', w, [...hid].slice(0, 8).join(' · '));
  await red.p.evaluate(() => window.scrollTo(0, 0));
  await shot(red.p, `${w}-reducido.png`);
  await red.ctx.close();

  const nojs = await browser.newContext({ viewport: { width: w, height: 900 }, javaScriptEnabled: false });
  const pj = await nojs.newPage();
  await pj.goto(url, { waitUntil: 'load' });
  const hj = await pj.evaluate(measure);
  if (hj.hidden.length) add('FAIL', 'oculto-sin-javascript', w, hj.hidden.slice(0, 8).join(' · '));
  await pj.screenshot({ path: path.join(out, `${w}-sin-js.png`), fullPage: true });
  shots.push(`${w}-sin-js.png`);
  await nojs.close();
}
await browser.close();

const fails = findings.filter(f => f.level === 'FAIL');
const report = { target, mode, widths, viewer, out, findings, shots };
fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify(report, null, 2));
const md = [`# Inspección de ${target}`, '', `Modo: ${mode} · anchos: ${widths.join(', ')}${viewer ? ' · página de opciones (sin tira de scroll)' : ''}`, '',
  '| Nivel | Código | Ancho | Detalle |', '|---|---|---|---|',
  ...findings.map(f => `| ${f.level} | ${f.code} | ${f.width} | ${String(f.detail).replace(/\|/g, '\\|')} |`),
  findings.length ? '' : '| — | sin hallazgos | — | — |', '', '## Capturas', '', ...shots.map(s => `- ${s}`)].join('\n');
fs.writeFileSync(path.join(out, 'report.md'), md + '\n');
console.log(`${fails.length} FAIL · ${findings.length - fails.length} WARN · ${shots.length} capturas en ${out}`);
for (const f of findings) console.log(`  ${f.level.padEnd(4)} ${f.code} @${f.width}: ${f.detail}`);
process.exit(fails.length ? 1 : 0);
