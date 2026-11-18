#!/usr/bin/env node
/* Critical CSS: for every page, collect the CSS rules that match elements in the first screen
   (desktop 1280x800 + mobile 390x844), inline them in <style id="cw-critical"> and load the full
   bundle without blocking rendering (preload + onload, with <noscript> fallback).
   Needs: puppeteer-core (npm i -D puppeteer-core, or NODE_PATH), Chrome, and a static server on :8765
   (python3 -m http.server 8765).  Usage: node build_critical.js   [page.html ...]   -- idempotent. */
const fs = require('fs'), path = require('path');
let puppeteer; try { puppeteer = require('puppeteer-core'); } catch (e) { console.error('puppeteer-core not found (set NODE_PATH)'); process.exit(2); }
const CHROME = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const SKIP = /^(READY|actual|footer|header|hero|hreflang|json-ld|head-meta)/;
const all = (d) => fs.readdirSync(d).filter(f => f.endsWith('.html') && !SKIP.test(f)).map(f => path.join(d, f));
const pages = process.argv.length > 2 ? process.argv.slice(2) : [...all('.'), ...all('ua')];
const BUNDLE = /<link rel="stylesheet" href="((?:\.\.\/)?css\/b\/[^"]+)">/g;

function strip(html) {
  html = html.replace(/<style class="cw-critical">[\s\S]*?<\/style>\n?/g, '').replace(/<style id="cw-critical">[\s\S]*?<\/style>\n?/g, '');
  html = html.replace(/<noscript><link rel="stylesheet" href="((?:\.\.\/)?css\/b\/[^"]+)"><\/noscript>\n?/g, '');
  return html.replace(/<link rel="preload" href="((?:\.\.\/)?css\/b\/[^"]+)" as="style" onload="[^"]*">/g, '<link rel="stylesheet" href="$1">');
}

const collector = () => {
  const vh = innerHeight, vw = innerWidth;
  const fold = [document.documentElement, document.body];
  for (const e of document.body.querySelectorAll('*')) { const r = e.getBoundingClientRect(); if (r.top < vh && r.bottom > 0 && r.left < vw) fold.push(e); }
  const base = s => s.replace(/::?[a-zA-Z-]+(\([^)]*\))?/g, '').replace(/\s+/g, ' ').trim();
  const match = sel => { try { return sel.split(',').some(p => { const b = base(p); return !b || b === '*' || fold.some(e => e.matches(b)); }); } catch (_) { return true; } };
  const out = [];
  Array.from(document.styleSheets).forEach((sh, si) => {
    if (!sh.href || !/\/css\/b\//.test(sh.href)) return;
    const bn = sh.href.split('/').pop();
    let rules; try { rules = sh.cssRules; } catch (_) { return; }
    [...rules].forEach((r, i) => {
      if (r.type === 1) { if (match(r.selectorText)) out.push({ k: [si, i, -1], bn, css: r.cssText }); }
      else if (r.type === 4) { [...r.cssRules].forEach((c, j) => { if (c.type === 1 && match(c.selectorText)) out.push({ k: [si, i, j], bn, media: r.conditionText || r.media.mediaText, css: c.cssText }); }); }
      else if (r.type === 5 || r.type === 7) out.push({ k: [si, i, -1], bn, css: r.cssText });
      else if (r.type === 12) { [...r.cssRules].forEach((c, j) => { if (c.type === 1 && match(c.selectorText)) out.push({ k: [si, i, j], bn, supports: r.conditionText, css: c.cssText }); }); }
    });
  });
  return out;
};

(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox'] });
  let done = 0, bytes = 0;
  for (const file of pages) {
    const orig = fs.readFileSync(file, 'utf8'); const clean = strip(orig);
    if (!BUNDLE.test(clean)) { BUNDLE.lastIndex = 0; continue; } BUNDLE.lastIndex = 0;
    fs.writeFileSync(file, clean);
    const pg = await browser.newPage(); const keep = new Map();
    for (const [w, h] of [[1280, 800], [390, 844]]) {
      await pg.setViewport({ width: w, height: h });
      await pg.goto('http://localhost:8765/' + file.split(path.sep).join('/'), { waitUntil: 'load' });
      for (const r of await pg.evaluate(collector)) keep.set(r.bn + r.k.join('.') + (r.media ? '@' + r.media : '') + (r.supports ? '#' + r.supports : ''), r);
    }
    await pg.close();
    const rows = [...keep.values()].sort((a, b) => a.k[0] - b.k[0] || a.k[1] - b.k[1] || a.k[2] - b.k[2]);
    const dir = path.dirname(file);
    const rebase = css => css.replace(/url\((["']?)([^)"']+)\1\)/g, (m, q, u) => /^(data:|https?:|\/\/|\/|#)/.test(u) ? m : 'url(' + q + path.relative(dir, path.resolve('css/b', u)).split(path.sep).join('/') + q + ')');
    const perBundle = {};
    for (const bn of new Set(rows.map(r => r.bn))) {
      let css = '', cur = null;
      for (const r of rows.filter(x => x.bn === bn)) {
        const wrap = r.media ? '@media ' + r.media : r.supports ? '@supports ' + r.supports : null;
        if (wrap !== cur) { if (cur) css += '}'; if (wrap) css += wrap + '{'; cur = wrap; }
        css += rebase(r.css);
      }
      if (cur) css += '}';
      perBundle[bn] = css.replace(/\s+/g, ' ').replace(/\s*([{};,>])\s*/g, '$1').replace(/;}/g, '}');
    }
    let html = clean;
    html = html.replace(BUNDLE, (m, href) => {
      const css = perBundle[href.split('/').pop()] || ''; bytes += css.length;
      const pre = '<link rel="preload" href="' + href + '" as="style" onload="this.onload=null;this.rel=\'stylesheet\'"><noscript><link rel="stylesheet" href="' + href + '"></noscript>';
      return (css ? '<style class="cw-critical">' + css + '</style>\n' : '') + pre;
    });
    fs.writeFileSync(file, html); done++;
  }
  console.log('critical CSS inlined on', done, 'pages; avg', Math.round(bytes / Math.max(done, 1) / 1024 * 10) / 10, 'KB');
  await browser.close();
})();
