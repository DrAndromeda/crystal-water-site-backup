#!/usr/bin/env python3
"""Site validator. Exit code 1 if any ERROR is found.  Usage: python3 check.py [--strict]
Checks: unique/length title+description, one H1, canonical, hreflang reciprocity, JSON-LD validity,
internal links/images/css exist (HTML comments ignored), orphan pages, tag balance, alt text, noopener."""
import re, glob, os, json, sys, collections
from html.parser import HTMLParser

SK = re.compile(r'^(READY|actual|footer|header|hero|hreflang|json-ld|head-meta)')
SKIP_PAGES = {'blocks.html', '404.html'}
pages = [f for f in sorted(glob.glob('*.html') + glob.glob('ua/*.html')) if not SK.match(os.path.basename(f)) and f not in SKIP_PAGES]
errors, warns = [], []
E = lambda f, m: errors.append('%s: %s' % (f, m)); W = lambda f, m: warns.append('%s: %s' % (f, m))
strip_comments = lambda s: re.sub(r'<!--.*?-->', '', s, flags=re.S)
VOID = {'meta', 'link', 'img', 'br', 'hr', 'input', 'source', 'area', 'base', 'col', 'embed', 'param', 'track', 'wbr'}
TRACK = {'div', 'p', 'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 'section', 'article', 'main', 'header', 'footer', 'nav', 'aside', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'a', 'form', 'select', 'details', 'summary', 'figure', 'blockquote'}

class Bal(HTMLParser):
    def __init__(self): super().__init__(); self.stack = []; self.err = []
    def handle_starttag(self, t, a):
        if t in TRACK: self.stack.append(t)
    def handle_endtag(self, t):
        if t not in TRACK: return
        if t in self.stack:
            while self.stack and self.stack[-1] != t:
                x = self.stack.pop()
                if x not in ('p', 'li', 'td', 'th', 'tr'): self.err.append('unclosed <%s>' % x)
            self.stack.pop()
        else: self.err.append('stray </%s>' % t)

titles = collections.defaultdict(list); descs = collections.defaultdict(list); links_to = collections.Counter(); alts = {}
for f in pages:
    raw = open(f, encoding='utf-8').read(); s = strip_comments(raw); d = os.path.dirname(f); ua = f.startswith('ua/')
    t = re.search(r'<title>(.*?)</title>', s, re.S); ds = re.search(r'name="description" content="([^"]*)"', s)
    if not t: E(f, 'no <title>')
    else:
        tt = t.group(1).strip(); titles[tt].append(f)
        if len(tt) > 70: W(f, 'title %d chars' % len(tt))
    if not ds: E(f, 'no meta description')
    else:
        dd = ds.group(1).strip(); descs[dd].append(f)
        if not 70 <= len(dd) <= 170: W(f, 'description %d chars' % len(dd))
    if len(re.findall(r'<h1\b', s)) != 1: E(f, 'H1 count = %d' % len(re.findall(r'<h1\b', s)))
    can = re.search(r'rel="canonical" href="([^"]+)"', s)
    if not can: E(f, 'no canonical')
    else:
        exp = 'https://crystalwater.kiev.ua/' + ('ua/' if ua else '') + ('' if f == 'index.html' else os.path.basename(f))
        if can.group(1) != exp and not (f == 'index.html' and can.group(1) == 'https://crystalwater.kiev.ua/'): E(f, 'canonical %s != %s' % (can.group(1), exp))
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(b)
        except Exception as e: E(f, 'invalid JSON-LD: %s' % e)
    for u in re.findall(r'(?:href|src)="([^"#?]+)', s):
        if re.match(r'^(https?:|//|mailto:|tel:|data:|javascript:)', u) or u == '/': continue
        base = 'ua' if u.startswith('/ua/') else d
        uu = u[4:] or 'index.html' if u.startswith('/ua/') else u
        p = uu.lstrip('/') if uu.startswith('/') and not u.startswith('/ua/') else os.path.normpath(os.path.join(base, uu))
        if os.path.isdir(p): p = os.path.join(p, 'index.html')
        if not os.path.exists(p): E(f, 'broken link/asset: %s' % u)
        elif p.endswith('.html'): links_to[p] += 1 if p != f else 0
    for m in re.finditer(r'<img\b[^>]*>', s):
        if not re.search(r'\salt=', m.group(0)): E(f, 'img without alt')
    for m in re.finditer(r'<a\b[^>]*target="_blank"[^>]*>', s):
        if 'noopener' not in m.group(0): W(f, 'target=_blank without noopener')
    hl = dict(re.findall(r'hreflang="([^"]+)" href="([^"]+)"', s))
    if 'ru' in hl and 'uk' in hl:
        ru_f = hl['ru'].replace('https://crystalwater.kiev.ua/', '') or 'index.html'; ua_f = hl['uk'].replace('https://crystalwater.kiev.ua/', '')
        if not os.path.exists(ru_f): E(f, 'hreflang ru target missing %s' % ru_f)
        if not os.path.exists(ua_f): E(f, 'hreflang uk target missing %s' % ua_f)
        else:
            back = re.findall(r'hreflang="uk" href="([^"]+)"', open(ru_f, encoding='utf-8').read())
            if back and back[0] != hl['uk']: E(f, 'hreflang not reciprocal with %s' % ru_f)
    else: W(f, 'no ru/uk hreflang pair')
    body = re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S)
    bp = Bal(); bp.feed(body)
    if bp.err: W(f, 'tag balance: %s' % ', '.join(sorted(set(bp.err))[:4]))
for t, fs in titles.items():
    if len(fs) > 1: E(','.join(fs), 'duplicate title')
for t, fs in descs.items():
    if len(fs) > 1: E(','.join(fs), 'duplicate description')
for f in pages:
    if f != 'index.html' and f != 'ua/index.html' and links_to[f] == 0: W(f, 'orphan page (no inbound links)')
# sitemap parity (inventory): every indexable page listed, nothing listed that does not exist
smap = set(re.findall(r'<loc>([^<]+)</loc>', open('sitemap.xml', encoding='utf-8').read())) | set(re.findall(r'<loc>([^<]+)</loc>', open('sitemap-ua.xml', encoding='utf-8').read()))
want = {'https://crystalwater.kiev.ua/' + ('' if f == 'index.html' else f) for f in pages}
for u in sorted(want - smap): E('sitemap', 'page missing from sitemap: %s' % u)
for u in sorted(smap - want): E('sitemap', 'sitemap lists non-existent page: %s' % u)
for m in warns[:60]: print('WARN ', m)
for m in errors: print('ERROR', m)
print('%d pages, %d errors, %d warnings' % (len(pages), len(errors), len(warns)))
sys.exit(1 if errors or (len(sys.argv) > 1 and sys.argv[1] == '--strict' and warns) else 0)
