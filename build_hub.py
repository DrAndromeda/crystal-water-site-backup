#!/usr/bin/env python3
"""Regenerate the article card grid of articles.html and ua/articles.html from all article pages
(pages whose <main> has class article-container). Run after adding articles."""
import re, glob, os, html, sys
CORE = {'index', 'about', 'articles', 'uslugi-i-tseny', 'tekhnologii-ochistki', 'o-nas'}
NEW = set(sys.argv[1:])  # slugs to show first

def info(path, ua):
    s = open(path, encoding='utf-8').read()
    if '"@type": "Article"' not in s: return None
    crumb = re.search(r'<nav class="breadcrumbs".*?<span>(.*?)</span>', s, re.S)
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    d = re.search(r'name="description" content="([^"]*)"', s)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    img = re.search(r'<main.*?<img[^>]*\ssrc="([^"]+)"', s, re.S)
    t = html.unescape(re.sub(r'<[^>]+>', '', (crumb.group(1) if crumb and len(crumb.group(1)) > 8 and crumb.group(1).strip() not in ('Статья', 'Стаття') else h1.group(1)) if h1 else '')).strip()
    d = html.unescape(d.group(1)) if d else ''
    d = d if len(d) <= 110 else d[:107].rsplit(' ', 1)[0] + '…'
    src = img.group(1) if img else 'assets/images/voda.webp'
    chk = src.lstrip('/') if src.startswith('/') else os.path.normpath(os.path.join(os.path.dirname(path), src))
    if not os.path.exists(chk): src = 'assets/images/voda.webp'
    if ua and not src.startswith(('../', 'http')): src = '../' + src
    return t, d, src

def card(slug, t, d, src, ua):
    src = src if not ua or src.startswith(('../', 'http')) else src
    return ('          <a href="%s.html" class="article-card" style="display:block;padding:16px;background:#ebf4ff;border-radius:10px;text-decoration:none;color:#23435d;">\n'
            '            <img src="%s" alt="%s" style="width:100%%;height:130px;object-fit:cover;border-radius:8px;margin-bottom:10px;" loading="lazy" decoding="async" /><h3 style="margin:0 0 6px;font-size:15px;">%s</h3>\n'
            '            <p style="margin:0;font-size:13px;color:#526d84;">%s</p>\n          </a>') % (slug, src, html.escape(t, True), html.escape(t, False), html.escape(d, False))

for ua in (False, True):
    hub = 'ua/articles.html' if ua else 'articles.html'
    items = []
    for f in glob.glob('ua/*.html' if ua else '*.html'):
        slug = os.path.basename(f)[:-5]
        if slug in CORE or slug in ('pro-nas', 'tsiny', 'tekhnologii-ochystky') or re.match(r'^(READY|actual|footer|header|hero|hreflang|json-ld|head-meta)', slug): continue
        i = info(f, ua)
        if i: items.append((slug,) + i)
    items.sort(key=lambda x: (x[0] not in NEW, x[1].lower()))
    s = open(hub, encoding='utf-8').read()
    cards = '\n'.join(card(sl, t, d, src, ua) for sl, t, d, src in items)
    pat = re.compile(r'(<div style="display:grid;grid-template-columns:repeat\(auto-fill,minmax\(280px,1fr\)\);gap:16px;">\n)(.*?)(\n\s*</div>\n\s*</div>\n\s*</div></section>)', re.S)
    assert pat.search(s), hub
    s = pat.sub(lambda m: m.group(1) + cards + m.group(3), s, 1)
    open(hub, 'w', encoding='utf-8').write(s)
    print(hub, len(items), 'cards')
