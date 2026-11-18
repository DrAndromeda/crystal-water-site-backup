#!/usr/bin/env python3
"""Text lint for IMPROVEMENTS.md task 4 ("texts 10/10"). Scans visible text (RU + UA) of all pages.
Rules: no AI-slop / hype words, no unsupported superlatives, no cliches, no medical promises.
Negations ("не лечит", "не заменяет врача") are allowed. Exit 1 on hits.   python3 lint_text.py [-v]"""
import re, glob, os, sys
SK = re.compile(r'^(READY|actual|footer|header|hero|hreflang|json-ld|head-meta|blocks|404)')
RULES = [
 ('ai-slop', r'\b(bespoke|seamless\w*|tailored|holistic|transformative|cutting[- ]edge|state[- ]of[- ]the[- ]art)\b'),
 ('hype', r'\b(идеальн\w*|уникальн\w*|непревзойд\w*|революцион\w*|инновацион\w*|премиальн\w*|абсолютн\w*|ідеальн\w*|унікальн\w*|неперевершен\w*|революційн\w*|інноваційн\w*|преміальн\w*|абсолютн\w*)'),
 ('best-claim', r'\b(?:лучш(?:ая|ий|ее|ие|ую|ей|его|ему|им|их|ими)|найкращ\w+|кращ(?:а|ий|і|у|ого|ому|им|их))\b(?:\W+\w+){0,2}?\W+(?:вод\w+|сервис\w*|доставк\w+|компани\w+|качеств\w+|очистк\w+|технолог\w+|фильтр\w*|сервіс\w*|якіст\w+|очищенн\w+)|\b(?:вод\w+|сервис\w*|доставк\w+|компани\w+|качеств\w+|очистк\w+|технолог\w+|фильтр\w*|сервіс\w*|якіст\w+|очищенн\w+)\W+(?:\w+\W+){0,2}?(?:лучш(?:ая|ий|ее|ие|ую|ей|его|ему|им|их|ими)|найкращ\w+)\b'),
 ('health-claim', r'(долголети\w*|здоровь\w+ на долгие|поправ\w+ здоровь\w+|улучш\w+ (?:общее )?(?:состояни\w+|самочувстви\w+) (?:здоровья|организма)|здоровья на долги\w+ год\w*|омолож\w+|продлева\w+ жизнь|быть абсолютно здоров\w+|довголіт\w*|здоров.я на довгі|поліпш\w+ здоров.я|покращ\w+ (?:загальний )?стан здоров.я|продовжу\w+ життя|бути абсолютно здоров\w+|оздоровлен\w+|оздоровл\w+)'),
 ('cliche', r'(индивидуальн\w+ подход|широк\w+ спектр|высок\w+ качеств\w+ услуг|команда профессионалов|надёжный партн[её]р|надежный партн[её]р|в наше время|на сегодняшний день|не секрет, что|як відомо|індивідуальн\w+ підхід|широк\w+ спектр|команда професіоналів|надійн\w+ партнер|у наш час|на сьогоднішній день)'),
 ('medical-promise', r'(?<!не )(?<!не заменяет и не )(лечит\b|излечи\w*|вылечи\w*|исцел\w*|детокс\w*|выводит токсины|очищает организм|укрепляет иммунитет|повышает иммунитет|на клеточном уровне|омолажива\w*|похудени\w+ гарантир\w*|лікує\b|вилікує\w*|зцілює\w*|виводить токсини|очищає організм|зміцнює імунітет|підвищує імунітет|на клітинному рівні)'),
]
NEG = re.compile(r'(не|ни|нет|нельзя|без|ні|немає)\s+\w{0,12}\s*$', re.I)
hits = {}
for f in sorted(glob.glob('*.html') + glob.glob('ua/*.html')):
    if SK.match(os.path.basename(f)): continue
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->|<aside class="cw-disclaimer".*?</aside>|<blockquote.*?</blockquote>|<p class="review-text">.*?</p>', '', s, flags=re.S)
    b = re.search(r'<body.*', s, re.S)
    t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', (b.group(0) if b else s)))
    for name, rx in RULES:
        for x in re.finditer(rx, t, re.I):
            ctx = t[max(0, x.start() - 40):x.end() + 20]
            if name == 'medical-promise' and NEG.search(t[max(0, x.start() - 25):x.start()]): continue
            hits.setdefault(f, []).append((name, x.group(0), ctx))
tot = sum(len(v) for v in hits.values())
if '-v' in sys.argv:
    for f, v in hits.items():
        for n, w, c in v: print('%s [%s] %s | …%s…' % (f, n, w, c))
import collections
c = collections.Counter(n for v in hits.values() for n, _, _ in v)
print('%d hits in %d files: %s' % (tot, len(hits), dict(c)))
sys.exit(1 if tot else 0)
