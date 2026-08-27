#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const SITE_DIR = '/Users/andromeda/.openclaw/workspace/crystal-water-site';

// Common header template
function getHeaderHTML(page) {
  const active = (p) => p === page ? ' class="active"' : '';
  return `<header class="header">
    <div class="container">
      <a class="logo-link" href="/">
        <div class="logo-icon">💧</div>
        <div class="logo-text">Кришталево-чиста питна вода</div>
      </a>
      <nav class="nav">
        <a href="/"${active('home')}>Доставка воды</a>
        <a href="prices.html"${active('prices')}>Цены</a>
        <a href="tech.html"${active('tech')}>Технологии</a>
        <a href="articles.html"${active('articles')}>Статьи</a>
        <a href="about.html"${active('about')}>Контакты</a>
        <a href="ua.html">UA</a>
      </nav>
      <div class="header-phones">
        <a href="tel:+380637886880"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg> +38 (063) 788-68-80</a>
        <a href="tel:+380635304050"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg> +38 (063) 530-40-50</a>
      </div>
    </div>
  </header>`;
}

// Common footer
const FOOTER = `<footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <div class="footer-brand">Crystal Water</div>
          <div class="footer-sub">Доставка питьевой очищенной воды в Броварах и Киеве</div>
          <div class="footer-links">
            <a href="prices.html">Цены</a>
            <a href="tech.html">Технологии</a>
            <a href="articles.html">Статьи</a>
            <a href="about.html">Контакты</a>
          </div>
        </div>
        <div>
          <h4>Телефоны</h4>
          <a class="footer-phone" href="tel:+380637886880">+38 (063) 788-68-80</a>
          <a class="footer-phone2" href="tel:+380635304050">+38 (063) 530-40-50</a>
          <h4 style="margin-top:16px;">Telegram</h4>
          <a href="https://t.me/CrystalWaterBro_bot" target="_blank">@CrystalWaterBro_bot</a>
        </div>
        <div>
          <h4>Адрес и график</h4>
          <div>ул. Кооперативная, 3 А · Бровары</div>
          <div style="margin-top:8px;">Ежедневно 08:00-20:00</div>
          <div>Сб-Вс 09:00-17:00</div>
          <div class="footer-social">
            <a href="https://crystalwater.kiev.ua/ua/">UA</a>
            <a href="https://www.instagram.com/crystalwater.brovary/" target="_blank">Instagram</a>
            <a href="https://www.facebook.com/crystalwater.brovary/" target="_blank">Facebook</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <div>© 2025 Crystal Water. Кришталево-чиста питна вода.</div>
        <div><a href="https://crystalwater.kiev.ua/sitemap.xml">Карта сайта</a></div>
      </div>
    </div>
  </footer>`;

const HTML_CLOSE = '</body>\n</html>';

// Extract content from page between <main> and </body>
function extractMainContent(html) {
  // Try to find <main> ... </main>
  const mainMatch = html.match(/<main>([\s\S]*?)<\/main>/);
  if (mainMatch) return mainMatch[1].trim();
  
  // Try to find body content minus header/footer
  // Look for content after header close and before footer start
  const bodyStart = html.indexOf('<body');
  const bodyEnd = html.lastIndexOf('</body>');
  if (bodyStart === -1 || bodyEnd === -1) return null;
  
  let bodyContent = html.substring(bodyStart, bodyEnd);
  
  // Remove header
  bodyContent = bodyContent.replace(/<header[\s\S]*?<\/header>/, '');
  // Remove footer
  bodyContent = bodyContent.replace(/<footer[\s\S]*?<\/footer>/, '');
  // Remove modal, floating elements, scripts
  bodyContent = bodyContent.replace(/<div class="modal"[\s\S]*?<\/div>/, '');
  bodyContent = bodyContent.replace(/<a class="floating-telegram"[\s\S]*?<\/a>/, '');
  bodyContent = bodyContent.replace(/<button class="scrollup"[\s\S]*?<\/button>/, '');
  // Remove utility bar
  bodyContent = bodyContent.replace(/<div class="utility">[\s\S]*?<\/div>/, '');
  // Remove closing body tag
  bodyContent = bodyContent.replace('</body>', '');
  
  return bodyContent.trim();
}

function getMetaTags(html) {
  // Preserve original meta tags, title, etc
  const headMatch = html.match(/<head>([\s\S]*?)<\/head>/);
  if (!headMatch) return '';
  const headContent = headMatch[1];
  
  // Collect unique non-duplicate meaningful tags
  const keep = [];
  
  // Keep JSON-LD block first
  const jsonldMatch = headContent.match(/<script type="application\/ld\+json">[\s\S]*?<\/script>/);
  if (jsonldMatch) keep.push(jsonldMatch[0]);
  
  // Keep meta tags: description, keywords, og, twitter, canonical
  const lines = headContent.split('\n');
  for (const line of lines) {
    const t = line.trim();
    // Skip: charset, viewport, title, style-remaster css, duplicate favicon
    if (t.includes('charset=')) continue;
    if (t.includes('viewport') && t.includes('width')) continue;
    if (t.startsWith('<title>')) continue;
    if (t.includes('style-remaster.css') || t.includes('style-remaster.css.backup')) continue;
    if (t.includes('style-remaster') && t.includes('stylesheet')) continue;
    if (t.includes('favicon.ico') || t.includes('shortcut icon')) continue;
    if (t.includes('style.css') && t.includes('stylesheet')) continue;
    // Keep: meta, link[rel=canonical], link[rel=alternate]
    if (t.startsWith('<meta') || t.startsWith('<link rel="canonical"') || t.startsWith('<link rel="alternate"')) {
      keep.push(t);
    }
  }
  return keep.join('\n    ');
}

function rebuildPage(filePath, pageId, activeNav) {
  let html = fs.readFileSync(filePath, 'utf-8');
  
  const meta = getMetaTags(html);
  const content = extractMainContent(html);
  
  if (!content) {
    console.log(`✗ Could not extract content from ${filePath}`);
    return;
  }
  
  const titleMatch = html.match(/<title>([^<]*)<\/title>/);
  const title = titleMatch ? titleMatch[1] : 'Crystal Water';
  
  const newHtml = `<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title}</title>
  <link rel="icon" href="images/favicon.ico" type="image/x-icon" />
  <link rel="stylesheet" href="css/crystal-main.css">
  ${meta}
</head>
<body>
  ${getHeaderHTML(pageId)}
  <main class="container" style="padding-top:30px;">
    ${content}
  </main>
  ${FOOTER}
</body>
</html>`;
  
  fs.writeFileSync(filePath, newHtml, 'utf-8');
  console.log(`✓ Rebuilt: ${path.basename(filePath)}`);
}

// Process main pages
const pages = [
  { file: 'about.html', id: 'about' },
  { file: 'prices.html', id: 'prices' },
  { file: 'tech.html', id: 'tech' },
  { file: 'articles.html', id: 'articles' },
];

for (const p of pages) {
  rebuildPage(path.join(SITE_DIR, p.file), p.id);
}

processArticlePages();

function processArticlePages() {
  const articleFiles = fs.readdirSync(SITE_DIR)
    .filter(f => f.endsWith('.html') && !['index.html', 'index_backup_inline.html', 'quick_access.html', 'about.html', 'prices.html', 'tech.html', 'articles.html', 'header.html'].includes(f));
  
  console.log(`\nProcessing ${articleFiles.length} article pages...`);
  
  for (const file of articleFiles) {
    const filePath = path.join(SITE_DIR, file);
    rebuildPage(filePath, 'articles');
  }
}

// Create ua.html
const uaHTML = `<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Crystal Water — Українською</title>
  <link rel="icon" href="images/favicon.ico" type="image/x-icon" />
  <link rel="stylesheet" href="css/crystal-main.css">
  <meta http-equiv="refresh" content="0; url=ua/index.html">
  <meta property="og:title" content="Crystal Water — Українською" />
  <meta property="og:description" content="Кришталево-чиста питна вода — доставка води в Броварах і Києві" />
  <meta property="og:url" content="https://crystalwater.kiev.ua/ua/" />
  <meta property="og:type" content="website" />
  <meta property="og:image" content="https://crystalwater.kiev.ua/assets/images/placeholder.png" />
</head>
<body>
  ${getHeaderHTML('home')}
  <main class="container" style="padding-top:60px;text-align:center;">
    <div class="content-panel">
      <div style="font-size:48px;margin-bottom:16px;">🌊</div>
      <h2>Українська версія</h2>
      <p style="color:#c8e2f5;">Перенаправляємо на українську версію сайту...</p>
      <p><a href="ua/index.html" class="btn">Перейти на українську 🇺🇦</a></p>
    </div>
  </main>
  ${FOOTER}
</body>
</html>`;

fs.writeFileSync(path.join(SITE_DIR, 'ua.html'), uaHTML, 'utf-8');
console.log('✓ Created: ua.html → redirect to /ua/index.html');

console.log('\n✅ All pages rebuilt!');