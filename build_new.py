#!/usr/bin/env python3
"""Create new RU article pages from <dir>/<slug>.ru.txt (same format as build_ua.py input),
copying the head/header/footer of an existing article as template.
Usage: python3 build_new.py <dir>   (then copy <slug>.ua.txt to the UA translations dir and run build_ua.py, build_hub.py)"""
import re, sys, os, glob, json, html
D = "https://crystalwater.kiev.ua"
TEMPLATE = '3-znachenie-vody-v-zhizni-cheloveka.html'

def faq_pairs(main):
    sec = re.search(r'<h2[^>]*>(?:Частые вопросы|Часті питання)</h2>(.*?)(?=<div class="cta-block"|<aside|</main>)', main, re.S)
    out = []
    if sec:
        for q, a in re.findall(r'<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>', sec.group(1), re.S):
            out.append((html.unescape(re.sub(r'<[^>]+>', '', q)).strip(), html.unescape(re.sub(r'<[^>]+>', '', a)).strip()))
    return out

def build(slug, tdir):
    t = open(os.path.join(tdir, slug + '.ru.txt'), encoding='utf-8').read()
    m = re.match(r'TITLE: (.*)\nDESC: (.*)\nCRUMB: (.*)\n===MAIN===\n(.*)', t, re.S)
    title, desc, crumb, main = [x.strip() for x in m.groups()]
    s = open(TEMPLATE, encoding='utf-8').read()
    url = '%s/%s.html' % (D, slug)
    et, ed = html.escape(title, quote=True), html.escape(desc, quote=True)
    s = re.sub(r'<title>.*?</title>', '<title>%s</title>' % html.escape(title, quote=False), s, 1, flags=re.S)
    s = re.sub(r'(name="description" content=")[^"]*(")', lambda x: x.group(1) + ed + x.group(2), s)
    s = re.sub(r'(property="og:title" content=")[^"]*(")', lambda x: x.group(1) + et + x.group(2), s)
    s = re.sub(r'(property="og:description" content=")[^"]*(")', lambda x: x.group(1) + ed + x.group(2), s)
    s = re.sub(r'(property="og:url" content=")[^"]*(")', lambda x: x.group(1) + url + x.group(2), s)
    s = re.sub(r'(rel="canonical" href=")[^"]*(")', lambda x: x.group(1) + url + x.group(2), s)
    s = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', '', s, flags=re.S)
    h1 = html.unescape(re.sub(r'<[^>]+>', '', re.search(r'<h1[^>]*>(.*?)</h1>', main, re.S).group(1))).strip()
    art = {"@context": "https://schema.org", "@type": "Article", "headline": h1[:110], "description": desc, "inLanguage": "ru",
           "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "author": {"@type": "Organization", "name": "Crystal Water"},
           "publisher": {"@type": "Organization", "name": "Crystal Water", "url": D + "/"}}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Доставка воды Бровары", "item": D + "/"},
        {"@type": "ListItem", "position": 2, "name": "Статьи о воде", "item": D + "/articles.html"},
        {"@type": "ListItem", "position": 3, "name": crumb, "item": url}]}
    blocks = [art, bc]
    faq = faq_pairs(main)
    if faq:
        blocks.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    ld = ''.join('\n  <script type="application/ld+json">\n%s\n  </script>' % json.dumps(b, ensure_ascii=False, indent=2) for b in blocks)
    s = s.replace('</head>', ld + '\n</head>', 1)
    s = re.sub(r'<main\b.*?</main>', lambda _: main, s, 1, flags=re.S)
    s = re.sub(r'(<nav class="breadcrumbs"[^>]*>.*?<span>)(.*?)(</span>)', lambda x: x.group(1) + html.escape(crumb, quote=False) + x.group(3), s, 1, flags=re.S)
    if 'id="main"' not in s: s = re.sub(r'<main\b', '<main id="main"', s, 1)
    open(slug + '.html', 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    tdir = sys.argv[1]
    for f in sorted(glob.glob(os.path.join(tdir, '*.ru.txt'))):
        sl = os.path.basename(f)[:-7]; build(sl, tdir); print('built', sl)
