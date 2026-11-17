#!/usr/bin/env python3
"""Regenerate sitemap.xml (RU, with xhtml hreflang alternates), llms.txt and llms-full.txt from the pages.
Run after any page change:  python3 build_seo.py"""
import re, glob, subprocess, os, html, datetime
D = 'https://crystalwater.kiev.ua'
SK = re.compile(r'^(READY|actual|footer|header|hero|hreflang|json-ld|head-meta|blocks|404)')
today = datetime.date.today().isoformat()
UAF = {'uslugi-i-tseny.html': 'tsiny.html', 'tekhnologii-ochistki.html': 'tekhnologii-ochystky.html', 'o-nas.html': 'pro-nas.html'}

def lastmod(f):
    r = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', f], capture_output=True, text=True).stdout.strip()
    return r or today

real = sorted(f for f in glob.glob('*.html') if not SK.match(f))
pr = lambda f: '1.0' if f == 'index.html' else '0.9' if f == 'uslugi-i-tseny.html' else '0.8' if f in ('about.html', 'tekhnologii-ochistki.html', 'articles.html', 'o-nas.html') else '0.6'
loc = lambda f: D + '/' + ('' if f == 'index.html' else f)
out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for f in real:
    ua = UAF.get(f, f)
    alt = ''
    if os.path.exists('ua/' + ua):
        alt = ('\n    <xhtml:link rel="alternate" hreflang="ru" href="%s"/>\n    <xhtml:link rel="alternate" hreflang="uk" href="%s/ua/%s"/>'
               '\n    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>') % (loc(f), D, ua, loc(f))
    out.append('  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>%s</priority>%s\n  </url>' % (loc(f), lastmod(f), pr(f), alt))
out.append('</urlset>\n'); open('sitemap.xml', 'w').write('\n'.join(out))

core = {'index.html', 'uslugi-i-tseny.html', 'about.html', 'tekhnologii-ochistki.html', 'articles.html', 'o-nas.html'}
arts = []
for f in real:
    if f in core: continue
    s = open(f, encoding='utf-8').read()
    if '"@type": "Article"' not in s: continue
    h = re.search(r'<h1\b[^>]*>(.*?)</h1>', s, re.S); d = re.search(r'name="description" content="([^"]*)"', s)
    arts.append((html.unescape(re.sub(r'<[^>]+>', '', h.group(1))).strip(), f, html.unescape(d.group(1)) if d else ''))
facts = '''## Факты
- Услуга: доставка очищенной питьевой воды в бутылях 19,9 л на дом и в офис в Броварах и Киеве.
- Марка воды: «Кришталево-чиста питна вода». Очистка: 8 ступеней, обратный осмос, озонная стерилизация, pH около 7,5.
- Цены: бутыль 19,9 л — 100 грн; залог за бутыль — 225 грн; помпа — 160 грн; кулер — цена по запросу. Минимальный заказ — 2 бутыля.
- Адрес: ул. Кооперативная, 3 А, г. Бровары.
- Телефоны: +38 (063) 788-68-80, +38 (063) 530-40-50.
- Telegram: https://t.me/CrystalWaterBro_bot
- График: Пн—Пт 08:00–20:00, Сб—Вс 09:00–17:00.
- Языки сайта: русский (основной), украинский (/ua/).
'''
pages = [('Главная', '', 'Доставка воды, цены, схема очистки'), ('Цены', 'uslugi-i-tseny.html', 'Прайс-лист, залог, пример расчёта, FAQ'),
         ('О компании', 'about.html', 'Как работаем, график, отзывы'), ('Контакты', 'o-nas.html', 'Адрес, телефоны, карта'),
         ('Технологии очистки', 'tekhnologii-ochistki.html', '8 ступеней очистки воды, FAQ'), ('Статьи', 'articles.html', 'Каталог статей о воде')]
core_txt = '\n'.join('- [%s](%s/%s): %s' % (n, D, u, d) for n, u, d in pages)
open('llms.txt', 'w', encoding='utf-8').write('# Crystal Water\n\n> Доставка очищенной питьевой воды (бутыли 19,9 л) в Броварах и Киеве. Обратный осмос и озонная стерилизация.\n\n%s\n## Основные страницы\n%s\n\n## Статьи\n%s\n\n## Дополнительно\n- Полное описание: %s/llms-full.txt\n- Sitemap: %s/sitemap.xml\n- Украинская версия: %s/ua/index.html\n' % (facts, core_txt, '\n'.join('- [%s](%s/%s)' % (n, D, u) for n, u, _ in arts), D, D, D))
open('llms-full.txt', 'w', encoding='utf-8').write('# Crystal Water — полное описание для AI-систем\n\nИнформация на сайте носит справочный характер и не является медицинской консультацией.\n\n%s\n## Основные страницы\n%s\n\n## Статьи (название и краткое описание)\n%s' % (facts, core_txt, '\n'.join('### %s\n%s/%s\n%s\n' % (n, D, u, d) for n, u, d in arts)))
print(len(real), 'urls;', len(arts), 'articles in llms')
