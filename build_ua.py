#!/usr/bin/env python3
"""Assemble /ua/ pages from RU pages + translated <main>/title/description.

Usage: python3 build_ua.py <translations_dir>
  translations_dir/<slug>.txt  format:
    TITLE: ...\nDESC: ...\nCRUMB: ...\n===MAIN===\n<main>...</main>
Also rewrites RU pages: language-switch link + hreflang (ru/uk/x-default),
and regenerates sitemap-ua.xml.
"""
import re, sys, os, glob, json, html, datetime

D = "https://crystalwater.kiev.ua"
SKIP = re.compile(r'^(READY|actual|footer|header|hero|hreflang|json-ld|head-meta)')
RU2UA = {'index.html': 'index.html', 'uslugi-i-tseny.html': 'tsiny.html',
         'tekhnologii-ochistki.html': 'tekhnologii-ochystky.html', 'o-nas.html': 'pro-nas.html'}
UA2RU = {v: k for k, v in RU2UA.items()}
ua_name = lambda ru: RU2UA.get(ru, ru)
ru_name = lambda ua: UA2RU.get(ua, ua)
ru_url = lambda ru: D + '/' + ('' if ru == 'index.html' else ru)
ua_url = lambda ua: D + '/ua/' + ua

DICT = [
 ('Доставка воды Бровары', 'Доставка води Бровари'), ('Доставка воды', 'Головна'),
 ('Технологии', 'Технології'), ('Статьи о воде', 'Статті про воду'), ('Статьи', 'Статті'),
 ('О нас', 'Про нас'), ('Контакты', 'Контакти'), ('Цены', 'Ціни'), ('Главная', 'Головна'),
 ('Доставка очищенной питьевой воды в Броварах и Киеве. Чистая вода для дома и офиса.',
  'Доставка очищеної питної води в Броварах і Києві. Чиста вода для дому та офісу.'),
 ('Свяжитесь с нами', "Зв'яжіться з нами"), ('Адрес и график', 'Адреса та графік'),
 ('ул. Кооперативная, 3 А, Бровары', 'вул. Кооперативна, 3 А, Бровари'),
 ('Пн-Пт: 08:00 - 20:00', 'Пн-Пт: 08:00 - 20:00'), ('Сб-Вс: 09:00 - 17:00', 'Сб-Нд: 09:00 - 17:00'),
 ('© 2025 Crystal Water. Кришталево-чиста питна вода. Все права защищены.',
  '© 2025 Crystal Water. Кришталево-чиста питна вода. Усі права захищені.'),
 ('📞 Позвонить', '📞 Подзвонити'), ('Открыть Telegram', 'Відкрити Telegram'), ('Закрыть', 'Закрити'),
 ('Наверх', 'Вгору'), ('Статья', 'Стаття'),
]

def mapped_href(v, ua_page):
    """RU-relative link -> link valid from /ua/ page."""
    m = re.match(r'^([^#?]*)([#?].*)?$', v); path, tail = m.group(1), m.group(2) or ''
    if re.match(r'^(https?:|//|mailto:|tel:|data:|#|javascript:)', v) or not path:
        return v
    if path.startswith('/') and not path.startswith('//'):
        if path == '/ua/': return 'index.html' + tail
        if path.startswith('/ua/'): return path[4:] + tail
        if path.endswith('.html') and path.count('/') == 1: return ua_name(path[1:]) + tail
        if re.match(r'^/(assets|images|css|js)/', path): return '..' + path + tail
    if path in ('./', '/', ''):
        return 'index.html' + tail
    if path.startswith('ua/'):
        return path[3:] + tail
    if path.endswith('.html') and '/' not in path:
        return ua_name(path) + tail
    if re.match(r'^(\./)?(assets|images|css|js)/', path):
        return '../' + path.lstrip('./') + tail
    return v

def rewrite_links(s):
    s = re.sub(r'((?:href|src|poster|data-src|action)=")([^"]*)(")', lambda m: m.group(1) + mapped_href(m.group(2), True) + m.group(3), s)
    s = re.sub(r"url\((['\"]?)(?:\./)?(images|assets)/", lambda m: "url(%s../%s/" % (m.group(1), m.group(2)), s)
    return s

EXTRA = [('Перейти к содержимому', 'Перейти до вмісту'), ('Главное меню', 'Головне меню'),
         ('aria-label="Количество бутылей"', 'aria-label="Кількість бутелів"'),
         ('Зачем нужна бутилированная вода в рационе', 'Навіщо бутильована вода в раціоні'),
         ('Преимущества профессиональной очистки перед бытовыми фильтрами', 'Переваги професійного очищення порівняно з побутовими фільтрами'),
         ('<option>1 бутыль</option>', '<option>1 бутель</option>'), ('<option>2 бутыли</option>', '<option>2 бутелі</option>'),
         ('<option>3 бутыли</option>', '<option>3 бутелі</option>'), ('<option>4 бутыли</option>', '<option>4 бутелі</option>'),
         ('<option>5+ бутылей</option>', '<option>5+ бутелів</option>'), ('Количество', 'Кількість')]

def tr(s):
    for a, b in EXTRA:
        s = s.replace(a, b)
    for a, b in DICT:
        if len(a) >= 15:
            s = s.replace(a, b)
        else:
            s = re.sub(r'>(\s*)' + re.escape(a) + r'(\s*)<', lambda m: '>' + m.group(1) + b + m.group(2) + '<', s)
            s = s.replace('"' + a + '"', '"' + b + '"')
    return s

def hreflang(ru_page, ua_page):
    return ('  <link rel="alternate" hreflang="ru" href="%s" />\n  <link rel="alternate" hreflang="uk" href="%s" />\n'
            '  <link rel="alternate" hreflang="x-default" href="%s" />\n') % (ru_url(ru_page), ua_url(ua_page), ru_url(ru_page))

def set_head_links(s, canonical, ru_page, ua_page):
    s = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*"[^>]*>', '', s)
    s = re.sub(r'<link rel="canonical"[^>]*>\n?', '', s)
    block = '  <link rel="canonical" href="%s" />\n' % canonical + hreflang(ru_page, ua_page)
    return s.replace('</head>', block + '</head>', 1)

JSONLD_UA = {
 'Бровары': 'Бровари', 'Киев': 'Київ', 'Вода питьевая Crystal Water, 19 л': 'Питна вода Crystal Water, 19 л',
 'Питьевая очищенная вода в бутыли 19 л с доставкой на дом и в офис в Броварах и Киеве.': 'Питна очищена вода в бутлі 19 л з доставкою додому й в офіс у Броварах і Києві.',
 'Доставка питьевой воды': 'Доставка питної води', 'Доставка воды на дом': 'Доставка води додому', 'Доставка воды в офис': 'Доставка води в офіс',
 'Доставка воды': 'Головна', 'ул. Кооперативная, 3 А': 'вул. Кооперативна, 3 А',
}

def jsonld_fix(s, title, desc, crumb, ru_page, ua_page):
    def fix(m):
        try: data = json.loads(m.group(2))
        except Exception: return m.group(0)
        def walk(o, parent=None):
            if isinstance(o, dict):
                t = o.get('@type')
                for k, v in list(o.items()):
                    if isinstance(v, str):
                        if v in JSONLD_UA and k in ('name', 'serviceType', 'description', 'streetAddress', 'addressLocality'): o[k] = JSONLD_UA[v]
                        elif v.startswith(D) and v.endswith('.html'):
                            o[k] = ua_url(ua_name(v.rsplit('/', 1)[1]))
                        elif v == D + '/':
                            o[k] = D + '/ua/index.html'
                        elif t == 'Article' and k == 'headline': o[k] = title.split(' | ')[0].split(' — ')[0][:110]
                        elif t == 'Article' and k == 'description': o[k] = desc
                        elif k == 'name':
                            for a, b in DICT:
                                if v == a: o[k] = b
                            if t == 'ListItem' and o.get('position') == 3: o[k] = crumb
                    else: walk(v, o)
                if t == 'Article': o['inLanguage'] = 'uk'
            elif isinstance(o, list):
                for x in o: walk(x)
        walk(data)
        return m.group(1) + json.dumps(data, ensure_ascii=False, indent=2) + m.group(3)
    return re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', fix, s, flags=re.S)

def regen_faq(s, main):
    """FAQPage JSON-LD must match the visible (translated) FAQ: rebuild it from the translated main."""
    s = re.sub(r'\s*<script type="application/ld\+json">\s*\{[^<]*"@type":\s*"FAQPage".*?</script>', '', s, flags=re.S)
    pairs = []
    sec = re.search(r'<h2[^>]*>(?:Частые вопросы|Часті запитання)</h2>(.*?)(?=<div class="cta-block"|<aside|</main>|$)', main, re.S)
    if sec:
        for q, a in re.findall(r'<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>', sec.group(1), re.S) + re.findall(r'<summary>(.*?)</summary>\s*<p[^>]*>(.*?)</p>', sec.group(1), re.S):
            pairs.append((html.unescape(re.sub(r'<[^>]+>', '', q)).strip(), html.unescape(re.sub(r'<[^>]+>', '', a)).strip()))
    if pairs:
        obj = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}
        s = s.replace('</head>', '\n  <script type="application/ld+json">\n%s\n  </script>\n</head>' % json.dumps(obj, ensure_ascii=False, indent=2), 1)
    return s

def build(slug, tdir):
    ru_page = slug + '.html'; ua_page = ua_name(ru_page)
    s = open(ru_page, encoding='utf-8').read()
    cand = [os.path.join(tdir, slug + '.ua.txt'), os.path.join(tdir, slug + '.txt')]
    t = open(next(c for c in cand if os.path.exists(c)), encoding='utf-8').read()
    m = re.match(r'TITLE: (.*)\nDESC: (.*)\nCRUMB: (.*)\n===MAIN===\n(.*)', t, re.S)
    title, desc, crumb, main = m.group(1).strip(), m.group(2).strip(), m.group(3).strip(), m.group(4).strip()
    et, ed = html.escape(title, quote=True), html.escape(desc, quote=True)
    s = s.replace('<html lang="ru"', '<html lang="uk"')
    s = re.sub(r'<title>.*?</title>', '<title>%s</title>' % html.escape(title, quote=False), s, 1, flags=re.S)
    s = re.sub(r'(name="description" content=")[^"]*(")', lambda x: x.group(1) + ed + x.group(2), s)
    s = re.sub(r'(property="og:title" content=")[^"]*(")', lambda x: x.group(1) + et + x.group(2), s)
    s = re.sub(r'(property="og:description" content=")[^"]*(")', lambda x: x.group(1) + ed + x.group(2), s)
    s = re.sub(r'(property="og:url" content=")[^"]*(")', lambda x: x.group(1) + ua_url(ua_page) + x.group(2), s)
    s = re.sub(r'(property="og:locale" content=")[^"]*(")', r'\1uk_UA\2', s)
    if re.search(r'<main\b', s):
        s = re.sub(r'<main\b.*?</main>', lambda _: main, s, 1, flags=re.S)
    else:  # pages without <main>: content sits between </header> and <footer>
        s = re.sub(r'(</header>\s*).*?(\s*<footer)', lambda x: x.group(1) + main + x.group(2), s, 1, flags=re.S)
    # breadcrumb last crumb + static strings
    s = re.sub(r'(<nav class="breadcrumbs"[^>]*>.*?<span>)(.*?)(</span>)', lambda x: x.group(1) + html.escape(crumb, quote=False) + x.group(3), s, 1, flags=re.S)
    if re.search(r'<main\b(?![^>]*\sid=)', s): s = re.sub(r'<main\b(?![^>]*\sid=)', '<main id="main"', s, 1)
    s = jsonld_fix(s, title, desc, crumb, ru_page, ua_page)
    s = regen_faq(s, main)
    # language switch before link rewriting
    s = re.sub(r'<li class="nav-lang"><a href="[^"]*" class="lang-switch">UA</a></li>',
               '<li class="nav-lang"><a href="../%s" class="lang-switch">RU</a></li>' % ('' if ru_page == 'index.html' else ru_page), s)
    s = rewrite_links(s)
    s = tr(s)
    s = set_head_links(s, ua_url(ua_page), ru_page, ua_page)
    open('ua/' + ua_page, 'w', encoding='utf-8').write(s)

def patch_ru(ru_page):
    s = open(ru_page, encoding='utf-8').read()
    ua_page = ua_name(ru_page)
    s = re.sub(r'(<li class="nav-lang"><a href=")[^"]*(" class="lang-switch">UA</a></li>)', r'\1ua/%s\2' % ua_page, s)
    s = set_head_links(s, ru_url(ru_page), ru_page, ua_page)
    open(ru_page, 'w', encoding='utf-8').write(s)

def patch_existing_ua(ua_page):
    """Hand-made UA pages: fix canonical/hreflang and nav links."""
    p = 'ua/' + ua_page; s = open(p, encoding='utf-8').read(); ru_page = ru_name(ua_page)
    s = set_head_links(s, ua_url(ua_page), ru_page, ua_page)
    s = re.sub(r'(<li class="nav-lang"><a href=")[^"]*(" class="lang-switch">RU</a></li>)', r'\1../%s\2' % ('' if ru_page == 'index.html' else ru_page), s)
    s = re.sub(r'(<li><a href=")[^"]*(">Статті</a></li>)', r'\1articles.html\2', s)
    s = re.sub(r'(<li[^>]*><a href=")[^"]*(">Про нас</a></li>)', r'\1about.html\2', s)
    open(p, 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    tdir = sys.argv[1]
    slugs = sorted({re.sub(r'(\.ua)?\.txt$', '', os.path.basename(f)) for f in glob.glob(os.path.join(tdir, '*.txt')) if not f.endswith('.ru.txt')})
    for sl in slugs: build(sl, tdir)
    for ru in list(RU2UA) + [sl + '.html' for sl in slugs]:
        if os.path.exists(ru): patch_ru(ru)
    patch_existing_ua('index.html')
    today = datetime.date.today().isoformat()
    pages = sorted(os.path.basename(f) for f in glob.glob('ua/*.html'))
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        out.append('  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>' % (ua_url(p), today, '0.8' if p in UA2RU or p in ('about.html', 'articles.html') else '0.6'))
    out.append('</urlset>\n')
    open('sitemap-ua.xml', 'w', encoding='utf-8').write('\n'.join(out))
    print('built', len(slugs), 'pages;', len(pages), 'in ua sitemap')
