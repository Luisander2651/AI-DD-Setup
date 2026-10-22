#!/usr/bin/env node
// Evaluador de diseño de ai-dd: mide un candidato (página HTML o URL) contra los criterios de
// diseño de la spec (criterios.json: puertas y KPIs) y deja capturas para el evaluador de la
// rúbrica. Lo usan /design-spec (references/evaluacion.md) en cada vuelta del ciclo y /review
// sobre la build. No instala nada: usa Playwright si ya está (proyecto, global o PLAYWRIGHT_PATH).
//
// Uso:
//   node evaluate.mjs <candidato.html | URL> --criteria <criterios.json> [--out <dir>]
//
// Salida en --out (por defecto .ai/inspect/<nombre>/): capturas por ancho (claro, reducido, sin
// JavaScript), tira del scroll al menor y al mayor ancho (film-<ancho>-NN.png), report.json y
// report.md. Código 0: pasan todas las puertas y KPIs · 1: alguno falla · 2: uso · 3: sin Playwright.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const argv = process.argv.slice(2);
const opt = (name, def) => { const i = argv.indexOf(name); return i >= 0 ? argv[i + 1] : def; };
const target = argv.find((a, i) => !a.startsWith('--') && (i === 0 || !argv[i - 1].startsWith('--')));
const critPath = opt('--criteria');
if (!target || !critPath || argv.includes('-h') || argv.includes('--help')) {
  console.log(fs.readFileSync(new URL(import.meta.url), 'utf8').split('\n').slice(1, 13).map(l => l.replace(/^\/\/ ?/, '')).join('\n'));
  process.exit(target && critPath ? 0 : 2);
}
let C;
try { C = JSON.parse(fs.readFileSync(critPath, 'utf8')); }
catch (e) { console.log(`No pude leer los criterios (${critPath}): ${e.message}`); process.exit(2); }
const G = { contrast: 4.5, contrast_large: 3, touch: 44, overflow: true, focus: true, no_js_content: true,
  reduced_motion_content: true, h1: 1, external_hosts: [], ...(C.gates || {}) };
const widths = (C.widths || [390, 1440]).slice().sort((a, b) => a - b);
const narrow = widths[0], wide = widths[widths.length - 1];
const isUrl = /^https?:\/\//.test(target);
const url = isUrl ? target : pathToFileURL(path.resolve(target)).href;
const name = isUrl ? new URL(target).hostname : path.basename(target).replace(/\.[^.]+$/, '');
const out = path.resolve(opt('--out', path.join('.ai', 'inspect', name)));
fs.mkdirSync(out, { recursive: true });

async function loadPlaywright() {
  const req = createRequire(path.join(process.cwd(), 'noop.js'));
  for (const t of [process.env.PLAYWRIGHT_PATH, 'playwright', 'playwright-core', '@playwright/test'].filter(Boolean)) {
    try { return req(t); } catch {}
  }
  let g = '';
  try { g = execSync('npm root -g', { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim(); } catch {}
  for (const t of ['playwright', 'playwright-core', '@playwright/test', '@playwright/mcp/node_modules/playwright-core']) {
    try { return createRequire(path.join(g, 'noop.js'))(path.join(g, t)); } catch {}
  }
  return null;
}
const pw = await loadPlaywright();
if (!pw) {
  console.log('No encontré Playwright (proyecto, global o PLAYWRIGHT_PATH). Mide a mano con la herramienta de\n' +
    'navegador de la sesión y marca cada puerta y KPI como "no medido" (evaluacion.md §6).');
  process.exit(3);
}
const launch = { headless: true };
if (process.env.CHROMIUM_PATH) launch.executablePath = process.env.CHROMIUM_PATH;
const browser = await pw.chromium.launch(launch);

const gates = new Map();   // id → {name, pass, details[]}
const gate = (id, name, ok, detail) => {
  const g = gates.get(id) || { id, name, pass: true, details: [] };
  if (!ok) { g.pass = false; if (detail) g.details.push(detail); }
  gates.set(id, g);
};
const shots = [];

const initScript = () => {
  window.__aidd = { lcp: 0, cls: 0, moved: new Set() };
  // Lo que de verdad se mueve: transiciones, animaciones CSS o WAAPI y estilos que cambia un script.
  const mark = e => { try { window.__aidd.moved.add(e.target); } catch {} };
  document.addEventListener('transitionrun', mark, true);
  document.addEventListener('animationstart', mark, true);
  new MutationObserver(ms => ms.forEach(m => window.__aidd.moved.add(m.target)))
    .observe(document, { attributes: true, attributeFilter: ['style'], subtree: true });
  const anim = Element.prototype.animate;
  Element.prototype.animate = function (...a) { window.__aidd.moved.add(this); return anim.apply(this, a); };
  try {
    new PerformanceObserver(l => { for (const e of l.getEntries()) window.__aidd.lcp = e.startTime; })
      .observe({ type: 'largest-contentful-paint', buffered: true });
    new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__aidd.cls += e.value; })
      .observe({ type: 'layout-shift', buffered: true });
  } catch {}
};

// Todo lo que se mide dentro de la página. Recibe la configuración y devuelve hallazgos.
const probe = (cfg) => {
  const vw = innerWidth, vh = innerHeight;
  const rgba = s => { const m = s.match(/[\d.]+/g); if (!m) return null; const [r, g, b, a = 1] = m.map(Number); return [r, g, b, a]; };
  const lum = ([r, g, b]) => { const c = [r, g, b].map(v => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }); return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; };
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
  const blend = (fg, bg) => [0, 1, 2].map(i => fg[i] * fg[3] + bg[i] * (1 - fg[3]));
  const hex = c => '#' + c.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
  const closedDetails = el => { const d = el.closest('details:not([open])'); return !!d && !el.closest('summary'); };
  const ignorable = el => el.closest('[aria-hidden="true"],[hidden],.sr-only,.visually-hidden,dialog:not([open]),[inert]') ||
    closedDetails(el) || getComputedStyle(el).display === 'none' || el.getClientRects().length === 0;
  const effOpacity = el => { let o = 1; for (let n = el; n && n.nodeType === 1; n = n.parentElement) { const cs = getComputedStyle(n); o *= parseFloat(cs.opacity); if (cs.visibility === 'hidden') return 0; } return o; };
  const label = el => `${el.tagName.toLowerCase()} "${(el.innerText || el.getAttribute('aria-label') || el.getAttribute('alt') || '').trim().replace(/\s+/g, ' ').slice(0, 40)}"`;
  const bgOf = el => {
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') return null;   // imagen o degradado: no determinado
      const c = rgba(cs.backgroundColor);
      if (c && c[3] > 0.99) return c;
      if (c && c[3] > 0) { const below = bgOf(n.parentElement || document.documentElement) || [255, 255, 255, 1]; return [...blend(c, below), 1]; }
    }
    return [255, 255, 255, 1];
  };
  // Texto visible con nodo de texto propio.
  const textEls = [...document.querySelectorAll('body *')].filter(el => !ignorable(el) && (el.innerText || '').trim() &&
    [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 0) && effOpacity(el) > 0.05);
  const contrastFails = []; let contrastUnknown = 0;
  for (const el of textEls) {
    const cs = getComputedStyle(el);
    const fg = rgba(cs.color), bg = bgOf(el);
    if (!fg) continue;
    if (!bg) { contrastUnknown++; continue; }
    const fs = parseFloat(cs.fontSize), fw = parseInt(cs.fontWeight, 10) || 400;
    const min = (fs >= 24 || (fs >= 18.66 && fw >= 700)) ? cfg.contrast_large : cfg.contrast;
    const r = ratio(fg[3] < 1 ? blend(fg, bg) : fg, bg);
    if (r + 0.005 < min) contrastFails.push(`${label(el)} ${r.toFixed(2)}:1 (mín. ${min})`);
  }
  // Objetivos de toque.
  const touchFails = [];
  for (const el of document.querySelectorAll('a[href],button,input:not([type=hidden]),select,textarea,summary,[role=button],[role=link],[tabindex]:not([tabindex="-1"])')) {
    if (ignorable(el) || effOpacity(el) < 0.05) continue;
    if (el.matches('a') && el.closest('p') && el.closest('p').textContent.trim().length > el.textContent.trim().length + 3) continue; // enlace dentro de un párrafo
    const r = el.getBoundingClientRect();
    if (r.width < cfg.touch - 0.5 || r.height < cfg.touch - 0.5) touchFails.push(`${label(el)} ${Math.round(r.width)}×${Math.round(r.height)}`);
  }
  // Colores fuera del sistema.
  const offTokens = new Map();
  if (cfg.tokens && cfg.tokens.length) {
    const allowed = new Set(cfg.tokens.map(t => t.toLowerCase()));
    for (const el of document.querySelectorAll('body, body *')) {
      if (ignorable(el) || el.closest('[data-ui],iframe,defs,mask,clipPath,pattern,symbol')) continue;
      const cs = getComputedStyle(el);
      const props = ['color', 'backgroundColor'];
      for (const side of ['Top', 'Right', 'Bottom', 'Left']) if (parseFloat(cs[`border${side}Width`]) > 0) props.push(`border${side}Color`);
      if (el.matches('path,rect,circle,ellipse,line,polyline,polygon,text')) props.push('fill', 'stroke');
      for (const p of props) {
        const c = rgba(cs[p] || '');
        if (!c || c[3] === 0) continue;
        if (p === 'color' && ![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
        const h = hex(c);
        if (!allowed.has(h)) offTokens.set(h, (offTokens.get(h) || 0) + 1);
      }
    }
  }
  // Texto encontrado y su posición.
  const find = t => {
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const norm = s => s.replace(/\s+/g, ' ').toLowerCase();
    let n, best = null, chrome = null;   // prefiere el contenido a la barra, el menú y el pie
    while ((n = w.nextNode())) {
      const el = n.parentElement;
      if (!el || ignorable(el) || !norm(n.textContent).includes(norm(t))) continue;
      if (el.closest('header,nav,footer,[role=banner],[role=navigation],[role=contentinfo]')) { chrome = chrome || el; continue; }
      best = el; break;
    }
    best = best || chrome;
    if (!best) {   // el texto puede estar repartido entre varios nodos: busca el elemento más pequeño que lo contiene
      const all = [...document.querySelectorAll('body *')].filter(el => !ignorable(el) && norm(el.innerText || '').includes(norm(t)));
      best = all.sort((a, b) => (a.innerText || '').length - (b.innerText || '').length)[0] || null;
    }
    if (!best) return { found: false };
    const r = best.getBoundingClientRect();
    return { found: true, visible: effOpacity(best) > 0.05, top: r.top + scrollY, bottom: r.bottom + scrollY,
      inFirstScreen: r.top + scrollY < vh && r.bottom + scrollY <= vh + 1 };
  };
  const texts = Object.fromEntries((cfg.texts || []).map(t => [t, find(t)]));
  const heads = [...document.querySelectorAll('h1,h2,h3')].filter(h => !ignorable(h)).map(h => {
    const lh = parseFloat(getComputedStyle(h).lineHeight) || parseFloat(getComputedStyle(h).fontSize) * 1.2;
    return { tag: h.tagName.toLowerCase(), lines: Math.round(h.getBoundingClientRect().height / lh), text: h.textContent.trim().slice(0, 50) };
  });
  const hidden = textEls.length ? [] : [];
  const content = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6,p,li,blockquote,img,button,a,dd,dt,address,td,th')]
    .filter(el => !ignorable(el) && (el.matches('img') || el.textContent.trim().length > 1));
  for (const el of content) {
    const r = el.getBoundingClientRect();
    // Lo que aún no llegó al 85 % de la ventana puede estar esperando su entrada: no cuenta.
    const shown = Math.min(r.bottom, vh * 0.85) - Math.max(r.top, 0);   // parte del elemento dentro de la zona leída
    if (r.width > 4 && r.height > 4 && shown >= r.height * 0.5 && effOpacity(el) < 0.05) hidden.push(label(el));
  }
  // Solapamiento: texto tapado por otro texto, por una imagen o un dibujo, o por una superficie con fondo.
  // Se mira solo lo que está en la ventana; las barras fijas o sticky no cuentan (tapan al desplazarse).
  const overlaps = [];
  const fixedLike = el => { for (let n = el; n && n.nodeType === 1; n = n.parentElement) { const p = getComputedStyle(n).position; if (p === 'fixed' || p === 'sticky') return true; } return false; };
  const painted = el => {
    if (el.matches('img,svg,canvas,video,picture,iframe') || el.closest('svg')) return true;
    const c = rgba(getComputedStyle(el).backgroundColor);
    if (c && c[3] > 0.05) return true;
    return [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
  };
  const lines = [];
  for (const el of textEls) {
    if (effOpacity(el) < 0.05 || fixedLike(el)) continue;
    for (const n of el.childNodes) {
      if (n.nodeType !== 3 || !n.textContent.trim()) continue;
      const rg = document.createRange(); rg.selectNodeContents(n);
      for (const r of rg.getClientRects()) if (r.width > 2 && r.height > 2 && r.bottom > 0 && r.top < vh) lines.push({ el, r });
    }
  }
  const seenPairs = new Set();
  for (let i = 0; i < lines.length; i++) {
    const a = lines[i];
    // Texto sobre texto: líneas de elementos distintos (ni uno dentro del otro) que se cruzan.
    for (let j = i + 1; j < lines.length; j++) {
      const b = lines[j];
      if (a.el === b.el || a.el.contains(b.el) || b.el.contains(a.el)) continue;
      const w = Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left);
      const h = Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top);
      if (w > 4 && h > Math.min(a.r.height, b.r.height) * 0.25) {
        const k = label(a.el) + '|' + label(b.el);
        if (!seenPairs.has(k)) { seenPairs.add(k); overlaps.push(`${label(a.el)} se cruza con ${label(b.el)}`); }
      }
    }
    // Algo pintado encima del texto: se prueban tres puntos de la línea.
    for (const fx of [0.15, 0.5, 0.85]) {
      const x = a.r.left + a.r.width * fx, y = a.r.top + a.r.height / 2;
      if (x < 0 || x >= vw || y < 0 || y >= vh) continue;
      const top = document.elementFromPoint(x, y);
      if (!top || top === a.el || a.el.contains(top) || top.contains(a.el) || fixedLike(top)) continue;
      if (getComputedStyle(top).pointerEvents === 'none' && !top.closest('svg')) continue;
      if (painted(top)) {
        const k = label(a.el) + '^' + label(top);
        if (!seenPairs.has(k)) { seenPairs.add(k); overlaps.push(`${label(a.el)} tapado por ${label(top)}`); }
        break;
      }
    }
  }
  // Fondos propios: regiones (secciones, cabecera, pie) con imagen o degradado de fondo, o con un
  // dibujo o imagen decorativa que cubre al menos un cuarto de la región.
  const regions = [...document.querySelectorAll('body > header, body > footer, main > section, main > header, section, [data-bg]')]
    .filter((el, i, a) => !ignorable(el) && a.indexOf(el) === i);
  const bgRegions = regions.filter(el => {
    const cs = getComputedStyle(el), r = el.getBoundingClientRect(), area = r.width * r.height;
    if (area < 1) return false;
    if (cs.backgroundImage && cs.backgroundImage !== 'none') return true;
    return [...el.querySelectorAll('svg,img,canvas,video,picture')].some(d => {
      if (!(d.closest('[aria-hidden="true"]') || d.getAttribute('alt') === '' || d.getAttribute('role') === 'presentation')) return false;
      const q = d.getBoundingClientRect();
      return q.width * q.height >= area * 0.25;
    });
  }).map(el => `${el.tagName.toLowerCase()}${el.id ? '#' + el.id : ''}`);
  // Imágenes con origen declarado (data-origen en la imagen o en el elemento que la lleva de fondo).
  const imgs = [];
  for (const el of document.querySelectorAll('img, [style*="url("]')) {
    if (ignorable(el)) continue;
    const decorative = el.matches('img') && (el.getAttribute('alt') === '' || el.closest('[aria-hidden="true"]'));
    const src = el.getAttribute('src') || '';
    imgs.push({ src: el.getAttribute('alt') || (src.startsWith('data:') ? 'imagen incrustada' : src.split('/').pop().slice(0, 60)), origen: el.closest('[data-origen]')?.getAttribute('data-origen') || null, decorative });
  }
  for (const el of document.querySelectorAll('body *')) {
    const bi = getComputedStyle(el).backgroundImage;
    if (bi && bi.includes('url(') && !el.matches('[style*="url("]') && !ignorable(el))
      imgs.push({ src: 'fondo de ' + el.tagName.toLowerCase(), origen: el.closest('[data-origen]')?.getAttribute('data-origen') || null, decorative: false });
  }
  const inlineJs = [...document.querySelectorAll('script:not([src])')].reduce((n, s) => n + s.textContent.length, 0);
  return {
    vh, height: document.documentElement.scrollHeight,
    overflow: document.documentElement.scrollWidth - vw,
    h1: document.querySelectorAll('h1').length,
    contrastFails: contrastFails.slice(0, 12), contrastFailCount: contrastFails.length, contrastUnknown,
    touchFails: touchFails.slice(0, 12), touchFailCount: touchFails.length,
    offTokens: [...offTokens.entries()].sort((a, b) => b[1] - a[1]).slice(0, 12),
    texts, heads, hidden: hidden.slice(0, 12), inlineJs, overlaps: overlaps.slice(0, 12), bgRegions, imgs,
    faces: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/["']/g, '')),
    lcp: window.__aidd ? window.__aidd.lcp : 0, cls: window.__aidd ? window.__aidd.cls : 0,
  };
};

const kpis = C.kpis || [];
const allTexts = [...new Set(kpis.flatMap(k => k.texts || (k.text ? [k.text] : [])))];
const cfg = { contrast: G.contrast, contrast_large: G.contrast_large, touch: G.touch, tokens: (C.tokens && C.tokens.colors) || [], texts: allTexts };

async function openPage(width, extra = {}) {
  const ctx = await browser.newContext({ viewport: { width, height: width < 600 ? 844 : width < 1100 ? 1100 : 900 }, ...extra });
  const p = await ctx.newPage();
  const net = { bytes: 0, js: 0, hosts: new Set(), errors: [] };
  p.on('response', async r => {
    try {
      const u = r.url();
      if (/^https?:/.test(u)) net.hosts.add(new URL(u).host);
      const b = await r.body(); net.bytes += b.length;
      if (r.request().resourceType() === 'script') net.js += b.length;
    } catch {}
  });
  p.on('pageerror', e => net.errors.push(String(e.message).slice(0, 160)));
  await p.addInitScript(initScript);
  await p.goto(url, { waitUntil: 'load' });
  await p.waitForTimeout(1300);
  return { ctx, p, net };
}
async function walk(p, m, fn) {   // recorre la página pantalla a pantalla
  const end = Math.max(0, m.height - m.vh), ys = [];
  for (let y = 0; y < end; y += m.vh) ys.push(y);
  ys.push(end);   // la última pantalla, aunque no sea completa
  for (const y of ys) {
    await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(1000); await fn(y);
  }
  await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(800);   // que terminen las transiciones de vuelta
}

const measures = {};
for (const w of widths) {
  const { ctx, p, net } = await openPage(w);
  const first = await p.evaluate(probe, cfg);
  measures[w] = { first, net };
  if (G.overflow) gate('G-desborde', 'Sin desplazamiento horizontal', first.overflow <= 1, `${w}px: ${first.overflow}px de más`);
  if (G.h1) gate('G-h1', `Un solo h1 por página`, first.h1 === G.h1, `${w}px: ${first.h1} h1`);
  for (const e of net.errors) gate('G-errores', 'Sin errores de JavaScript', false, `${w}px: ${e}`);
  const extHosts = [...net.hosts].filter(h => !isUrl || h !== new URL(target).host).filter(h => !G.external_hosts.includes(h));
  if (!isUrl) gate('G-red', 'Sin recursos de otros sitios (salvo los permitidos)', extHosts.length === 0, extHosts.join(', '));
  // Recorrido: contraste, toque y tokens en cada pantalla; contenido que no aparece; tira del scroll.
  const seen = { contrast: new Set(), touch: new Set(), tokens: new Map(), hidden: new Set(), overlap: new Set() };
  let frame = 0;
  await walk(p, first, async () => {
    const m = await p.evaluate(probe, cfg);
    m.contrastFails.forEach(x => seen.contrast.add(x));
    if (w < 1024) m.touchFails.forEach(x => seen.touch.add(x));
    m.offTokens.forEach(([h, n]) => seen.tokens.set(h, (seen.tokens.get(h) || 0) + n));
    m.hidden.forEach(x => seen.hidden.add(x));
    m.overlaps.forEach(x => seen.overlap.add(x));
    if (w === narrow || w === wide) {
      const f = `film-${w}-${String(frame++).padStart(2, '0')}.png`;
      await p.screenshot({ path: path.join(out, f) }); shots.push(f);
    }
  });
  // Captura completa después del recorrido: lo que se revela al bajar ya está a la vista.
  await p.screenshot({ path: path.join(out, `${w}-claro.png`), fullPage: true }); shots.push(`${w}-claro.png`);
  measures[w].dyn = await p.evaluate(() => {
    const moved = window.__aidd ? [...window.__aidd.moved].filter(e => e.isConnected) : [];
    const scenes = [...document.querySelectorAll('[data-scene]')];
    return { moved: new Set(moved).size, scenes: scenes.length,
      scenesLive: scenes.filter(sc => moved.some(m => m === sc || sc.contains(m))).length };
  });
  if (G.contrast) gate('G-contraste', `Contraste de texto ≥ ${G.contrast}:1 (≥ ${G.contrast_large}:1 en texto grande)`, seen.contrast.size === 0, seen.contrast.size ? `${w}px: ${[...seen.contrast].slice(0, 6).join(' · ')}` : '');
  if (G.touch && w < 1024) gate('G-toque', `Objetivos de toque ≥ ${G.touch} px`, seen.touch.size === 0, seen.touch.size ? `${w}px: ${[...seen.touch].slice(0, 6).join(' · ')}` : '');
  if (cfg.tokens.length) gate('G-tokens', 'Solo colores del sistema', seen.tokens.size === 0, seen.tokens.size ? `${w}px: ${[...seen.tokens.entries()].slice(0, 6).map(([h, n]) => `${h}×${n}`).join(', ')}` : '');
  gate('G-solapamiento', 'Ningún texto tapado por otro texto o por un elemento pintado', seen.overlap.size === 0, seen.overlap.size ? `${w}px: ${[...seen.overlap].slice(0, 4).join(' · ')}` : '');
  gate('G-aparece', 'Todo el contenido aparece al recorrer la página', seen.hidden.size === 0, seen.hidden.size ? `${w}px: ${[...seen.hidden].slice(0, 6).join(' · ')}` : '');
  // Foco visible, con el teclado, al mayor ancho.
  // Origen de las imágenes: toda imagen de contenido declara data-origen (propia, generada, muestra,
  // archivo, dibujada). Las de muestra se listan en el informe para sustituirlas antes de publicar.
  const noOrigin = first.imgs.filter(i => !i.origen);
  gate('G-imagenes', 'Toda imagen declara su origen (data-origen)', noOrigin.length === 0, noOrigin.length ? `${w}px: ${noOrigin.slice(0, 4).map(i => i.src || 'img').join(' · ')}` : '');
  if (G.focus && w === wide) {
    const bad = new Set();
    for (let i = 0; i < 60; i++) {
      await p.keyboard.press('Tab');
      const f = await p.evaluate(() => {
        const el = document.activeElement; if (!el || el === document.body) return null;
        const cs = getComputedStyle(el);
        const ring = (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0) || (cs.boxShadow && cs.boxShadow !== 'none');
        return { ring, label: `${el.tagName.toLowerCase()} "${(el.innerText || el.getAttribute('aria-label') || '').trim().slice(0, 30)}"` };
      });
      if (!f) break;
      if (!f.ring) bad.add(f.label);
    }
    gate('G-foco', 'Foco visible en todo elemento interactivo', bad.size === 0, [...bad].slice(0, 6).join(' · '));
  }
  measures[w].first.lcp = first.lcp; measures[w].first.cls = first.cls;
  await ctx.close();
}

// Movimiento reducido y sin JavaScript al menor y al mayor ancho.
for (const w of [...new Set([narrow, wide])]) {
  if (G.reduced_motion_content) {
    const { ctx, p } = await openPage(w, { reducedMotion: 'reduce' });
    const m0 = await p.evaluate(probe, cfg); const hid = new Set();
    await walk(p, m0, async () => (await p.evaluate(probe, cfg)).hidden.forEach(x => hid.add(x)));
    await p.screenshot({ path: path.join(out, `${w}-reducido.png`), fullPage: true }); shots.push(`${w}-reducido.png`);
    gate('G-reducido', 'Todo visible con movimiento reducido', hid.size === 0, hid.size ? `${w}px: ${[...hid].slice(0, 6).join(' · ')}` : '');
    await ctx.close();
  }
  if (G.no_js_content) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, javaScriptEnabled: false });
    const p = await ctx.newPage(); await p.goto(url, { waitUntil: 'load' });
    const m = await p.evaluate(probe, cfg);
    const missing = allTexts.filter(t => !m.texts[t] || !m.texts[t].found);
    gate('G-sin-js', 'Todo el contenido sin JavaScript', m.hidden.length === 0 && missing.length === 0,
      `${w}px: ${[...m.hidden.slice(0, 4), ...missing.map(t => `falta "${t}"`)].join(' · ')}`);
    await p.screenshot({ path: path.join(out, `${w}-sin-js.png`), fullPage: true }); shots.push(`${w}-sin-js.png`);
    await ctx.close();
  }
}
await browser.close();

// KPIs.
const fileBytes = isUrl ? 0 : fs.statSync(path.resolve(target)).size;
const docBytes = Math.max(fileBytes, measures[wide].net.bytes);
const jsBytes = measures[wide].net.js + measures[wide].first.inlineJs;
const kpiResults = kpis.map(k => {
  const ws = (k.widths || widths).filter(w => measures[w]);
  let value, pass;
  const T = (w, t) => measures[w].first.texts[t] || { found: false };
  switch (k.type) {
    case 'above_fold': {   // un texto (la acción principal) en la primera pantalla
      const miss = ws.filter(w => !T(w, k.text).found || !T(w, k.text).inFirstScreen || !T(w, k.text).visible);
      pass = miss.length === 0; value = pass ? `a la vista en ${ws.join(' y ')} px` : `fuera de la primera pantalla en ${miss.join(', ')} px`; break;
    }
    case 'above_fold_all': {   // varios textos en la primera pantalla
      const miss = []; for (const w of ws) for (const t of k.texts) if (!T(w, t).found || !T(w, t).inFirstScreen) miss.push(`"${t}" @${w}`);
      pass = miss.length === 0; value = pass ? `${k.texts.length}/${k.texts.length} a la vista` : `faltan: ${miss.slice(0, 6).join(', ')}`; break;
    }
    case 'visible': {   // textos presentes en la página
      const miss = k.texts.filter(t => !T(wide, t).found);
      pass = miss.length === 0; value = pass ? `${k.texts.length}/${k.texts.length} presentes` : `faltan: ${miss.map(t => `"${t}"`).join(', ')}`; break;
    }
    case 'order': {   // los textos aparecen en este orden en la página
      const bad = ws.filter(w => { const tops = k.texts.map(t => T(w, t).found ? T(w, t).top : NaN); return tops.some(Number.isNaN) || tops.some((v, i) => i && v < tops[i - 1]); });
      pass = bad.length === 0; value = pass ? 'en orden' : `orden roto o texto ausente en ${bad.join(', ')} px`; break;
    }
    case 'max_bytes': value = docBytes; pass = docBytes <= k.value; break;
    case 'max_js_bytes': value = jsBytes; pass = jsBytes <= k.value; break;
    case 'max_lcp_ms': value = Math.round(measures[wide].first.lcp); pass = value <= k.value; break;
    case 'max_cls': value = +measures[wide].first.cls.toFixed(3); pass = value <= k.value; break;
    case 'max_heading_lines': {
      const over = ws.flatMap(w => measures[w].first.heads.filter(h => h.lines > k.value).map(h => `${h.tag}@${w}: ${h.lines}`));
      pass = over.length === 0; value = pass ? `≤ ${k.value} líneas` : over.slice(0, 6).join(', '); break;
    }
    case 'max_page_screens': {
      const s = +(measures[wide].first.height / measures[wide].first.vh).toFixed(1);
      value = s; pass = s <= k.value; break;
    }
    case 'scenes': {   // escenas de scroll que de verdad se mueven al bajar
      const bad = ws.filter(w => (measures[w].dyn?.scenesLive ?? 0) < k.value);
      value = ws.map(w => `${measures[w].dyn?.scenesLive ?? 0}/${measures[w].dyn?.scenes ?? 0}@${w}`).join(' '); pass = bad.length === 0; break;
    }
    case 'moving_elements': {   // elementos que se mueven al cargar y al recorrer la página
      value = Math.min(...ws.map(w => measures[w].dyn?.moved ?? 0)); pass = value >= k.value; break;
    }
    case 'custom_background': {   // regiones con fondo propio (imagen, degradado o dibujo grande)
      value = Math.min(...ws.map(w => measures[w].first.bgRegions.length)); pass = value >= k.value; break;
    }
    case 'max_samples': {   // imágenes de muestra que quedan (0 antes de publicar)
      value = measures[wide].first.imgs.filter(i => i.origen === 'muestra').length; pass = value <= k.value; break;
    }
    case 'fonts_loaded': {   // las familias de marca cargan de verdad (no la fuente de reemplazo)
      const loaded = new Set(measures[wide].first.faces);
      const miss = (k.families || []).filter(f => !loaded.has(f));
      pass = miss.length === 0; value = pass ? 'cargadas' : `no cargan: ${miss.join(', ')}`; break;
    }
    default: value = `tipo desconocido: ${k.type}`; pass = false;
  }
  return { id: k.id, name: k.name, type: k.type, target: k.value ?? k.text ?? k.texts ?? k.families, value, pass };
});

const gateList = [...gates.values()];
const ok = gateList.every(g => g.pass) && kpiResults.every(k => k.pass);
const samples = measures[wide].first.imgs.filter(i => i.origen === 'muestra').map(i => i.src);
const report = { candidate: target, criteria: critPath, widths, measured_pass: ok, gates: gateList, kpis: kpiResults, samples,
  rubric: { threshold: C.threshold ?? 80, floor: C.floor ?? 3, items: C.rubric || null, scored: false }, shots, out };
fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify(report, null, 2));
const fmt = v => typeof v === 'number' && v > 2048 ? `${(v / 1024).toFixed(0)} kB` : String(v);
const md = [`# Evaluación de ${target}`, '', `Criterios: \`${critPath}\` · anchos: ${widths.join(', ')}`, '',
  '## Puertas', '', '| Puerta | Resultado | Detalle |', '|---|---|---|',
  ...gateList.map(g => `| ${g.id} · ${g.name} | ${g.pass ? '✅' : '❌'} | ${g.details.join(' · ').replace(/\|/g, '\\|')} |`),
  '', '## KPIs', '', '| KPI | Objetivo | Medido | Resultado |', '|---|---|---|---|',
  ...kpiResults.map(k => `| ${k.id} · ${k.name} | ${Array.isArray(k.target) ? k.target.join(' · ') : fmt(k.target)} | ${fmt(k.value)} | ${k.pass ? '✅' : '❌'} |`),
  '', `**Imágenes de muestra (sustituir antes de publicar):** ${samples.length ? samples.join(' · ') : 'ninguna'}`,
  '', `**Medición:** ${ok ? 'pasa → evaluar la rúbrica (evaluacion.md §4)' : 'no pasa → el candidato se descarta; sus fallos alimentan el siguiente'}`,
  '', '## Capturas', '', ...shots.map(s => `- ${s}`)].join('\n');
fs.writeFileSync(path.join(out, 'report.md'), md + '\n');
console.log(`${ok ? 'PASA' : 'NO PASA'} · puertas ${gateList.filter(g => g.pass).length}/${gateList.length} · KPIs ${kpiResults.filter(k => k.pass).length}/${kpiResults.length} · ${out}`);
for (const g of gateList.filter(g => !g.pass)) console.log(`  ❌ ${g.id}: ${g.details.slice(0, 3).join(' · ')}`);
for (const k of kpiResults.filter(k => !k.pass)) console.log(`  ❌ ${k.id} ${k.name}: ${fmt(k.value)} (objetivo ${Array.isArray(k.target) ? k.target.join(' · ') : fmt(k.target)})`);
process.exit(ok ? 0 : 1);
