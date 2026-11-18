#!/usr/bin/env python3
"""Apply the shared content blocks to every article page (RU + UA): FAQ accordion (FAQBlock),
ServiceCards and HowItWorks steps before the CTA. Idempotent (<!-- cw:art --> markers).  python3 build_blocks.py"""
import re, glob, os, html
SK = re.compile(r'^(READY|actual|footer|header|hero|hreflang|json-ld|head-meta|blocks|404)')
L = {
 'ru': dict(price='uslugi-i-tseny.html', h='Закажите воду Crystal Water', cards=[
        ('Бутыль 19,9 л', '100 грн', 'Очищенная вода «Кришталево-чиста питна вода». Залог за бутыль — 225 грн, минимальный заказ — 2 бутыля.', 'Смотреть условия'),
        ('Помпа Blue Rain', '160 грн', 'Для разлива воды из бутыли. Кулер — наличие и цену уточняйте у менеджера.', 'Подробнее'),
        ('Экспресс-анализ воды', 'Бесплатно', 'Измерим TDS и жёсткость вашего образца воды.', 'Узнать больше')],
        steps_h='Как заказать: 4 шага', steps=[('Выберите количество', 'Минимум 2 бутыля по 19,9 л.'), ('Оставьте заявку', 'Форма на сайте, телефон или Telegram.'), ('Получите воду', 'Бровары и Киев, в том числе после 20:00.'), ('Заказывайте снова', 'Повторный заказ — без повторного залога.')]),
 'ua': dict(price='tsiny.html', h='Замовте воду Crystal Water', cards=[
        ('Бутель 19,9 л', '100 грн', 'Очищена вода «Кришталево-чиста питна вода». Застава за бутель — 225 грн, мінімальне замовлення — 2 бутлі.', 'Дивитися умови'),
        ('Помпа Blue Rain', '160 грн', 'Для розливу води з бутля. Кулер — наявність і ціну уточнюйте в менеджера.', 'Докладніше'),
        ('Експрес-аналіз води', 'Безкоштовно', 'Виміряємо TDS і жорсткість вашого зразка води.', 'Дізнатися більше')],
        steps_h='Як замовити: 4 кроки', steps=[('Оберіть кількість', 'Мінімум 2 бутлі по 19,9 л.'), ('Залиште заявку', 'Форма на сайті, телефон або Telegram.'), ('Отримайте воду', 'Бровари та Київ, зокрема після 20:00.'), ('Замовляйте знову', 'Повторне замовлення — без повторної застави.')]),
}
def blocks(lang):
    c = L[lang]
    out = '<!-- cw:art -->\n<section class="cw-block"><h2>%s</h2>\n<div class="cw-cards">\n' % c['h']
    for t, price, d, btn in c['cards']:
        out += '  <a class="cw-card" href="%s"><h3>%s</h3><span class="cw-price">%s</span><p>%s</p><span class="cw-btn">%s</span></a>\n' % (c['price'], t, price, d, btn)
    out += '</div></section>\n<section class="cw-block"><h2>%s</h2>\n<ol class="cw-steps">\n' % c['steps_h']
    for t, d in c['steps']: out += '  <li><strong>%s</strong>%s</li>\n' % (t, d)
    return out + '</ol></section>\n<!-- /cw:art -->\n'

def faq_to_block(m_html):
    pat = re.compile(r'<h2[^>]*>(Частые вопросы|Часті запитання)</h2>\s*((?:<h3[^>]*>.*?</h3>\s*<p[^>]*>.*?</p>\s*)+)', re.S)
    def conv(m):
        items = re.findall(r'<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>', m.group(2), re.S)
        out = '<section class="cw-block cw-faq"><h2>%s</h2>\n' % m.group(1)
        for q, a in items: out += '  <details><summary>%s</summary><p>%s</p></details>\n' % (q.strip(), a.strip())
        return out + '</section>\n'
    return pat.sub(conv, m_html, 1)

import json
MAN = json.load(open('css/b/manifest.json')) if os.path.exists('css/b/manifest.json') else {}
def has_blocks(s):
    if 'css/blocks.css' in s: return True
    return any('css/blocks.css' in MAN.get(os.path.basename(h)[:-8], []) for h in re.findall(r'href="([^"]*css/b/[^"]+)"', s))

n = 0
for f in sorted(glob.glob('*.html') + glob.glob('ua/*.html')):
    if SK.match(os.path.basename(f)): continue
    s = o = open(f, encoding='utf-8').read()
    if '"@type": "Article"' not in s or 'class="article-container"' not in s: continue
    lang = 'ua' if f.startswith('ua/') else 'ru'
    s = re.sub(r'<!-- cw:art -->.*?<!-- /cw:art -->\n?', '', s, flags=re.S)
    s = faq_to_block(s)
    i = s.find('<div class="cta-block"')
    if i < 0: i = s.find('<aside class="cw-disclaimer"')
    if i < 0: i = s.rfind('</main>')
    s = s[:i] + blocks(lang) + s[i:]
    if not has_blocks(s):
        pre = '../' if lang == 'ua' else ''
        s = re.sub(r'(<link rel="stylesheet" href="[^"]*"[^>]*>)', lambda x: x.group(1) + '\n  <link rel="stylesheet" href="%scss/blocks.css">' % pre, s, 1)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print(n, 'article pages updated')
