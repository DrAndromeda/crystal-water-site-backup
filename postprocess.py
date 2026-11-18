#!/usr/bin/env python3
"""Idempotent post-processing for all pages (run after build_new.py / build_ua.py / build_hub.py):
WebP src + width/height, srcset for article/hub images, heading order, a11y attributes, UA a11y strings.
Needs Pillow:  python3 postprocess.py"""
import re, glob, os
from PIL import Image

SK = re.compile(r'^(READY|actual|footer|header|hero|hreflang|json-ld|head-meta)')
pages = [f for f in sorted(glob.glob('*.html') + glob.glob('ua/*.html')) if not SK.match(os.path.basename(f))]

def variant(p, w):
    out = os.path.splitext(p)[0] + '-%d.webp' % w
    if not os.path.exists(out):
        im = Image.open(p); im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(out, 'WEBP', quality=78, method=6)

def to_avif(p):
    """AVIF sibling of a .webp file (quality tuned for size); returns path or None."""
    a = os.path.splitext(p)[0] + '.avif'
    if not os.path.exists(a):
        try:
            im = Image.open(p); im = im.convert('RGBA' if im.mode in ('P', 'RGBA', 'LA') else 'RGB')
            im.save(a, 'AVIF', quality=55, speed=6)
        except Exception:
            return None
    return a

def to_webp(p):
    w = os.path.splitext(p)[0] + '.webp'
    if not os.path.exists(w):
        im = Image.open(p); im = im.convert('RGBA' if im.mode in ('P', 'RGBA', 'LA') else 'RGB')
        if im.width > 1600: im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
        im.save(w, 'WEBP', quality=80, method=6)
    return w

def images(s, f):
    base = os.path.dirname(f); art = 'class="article-container"' in s
    def sub(m):
        t = m.group(0); src = re.search(r'\ssrc="([^"]+)"', t)
        if not src: return t
        u = src.group(1)
        if u.startswith(('http', '//', 'data:')): return t
        p = u.lstrip('/') if u.startswith('/') else os.path.normpath(os.path.join(base, u))
        if re.search(r'\.(png|jpe?g)$', u, re.I) and os.path.exists(p):
            w = to_webp(p); t = t.replace(u, os.path.splitext(u)[0] + '.webp'); u = os.path.splitext(u)[0] + '.webp'; p = w
        if not os.path.exists(p): return t
        if not re.search(r'\swidth=', t) and not re.search(r'\sheight=', t) and p.endswith(('.webp', '.png', '.jpg', '.jpeg', '.gif')):
            try: W, H = Image.open(p).size; t = t.replace('<img', '<img width="%d" height="%d"' % (W, H), 1)
            except Exception: pass
        # ratio mismatch: stale width/height attrs reserve the wrong box -> layout shift; use the real file size
        wa, ha = re.search(r'\swidth="(\d+)"', t), re.search(r'\sheight="(\d+)"', t)
        if wa and ha and p.endswith(('.webp', '.png', '.jpg', '.jpeg', '.gif')):
            try:
                W0, H0 = Image.open(p).size
                if abs(int(wa.group(1)) / int(ha.group(1)) - W0 / H0) / (W0 / H0) > 0.03:
                    t = re.sub(r'\swidth="\d+"', ' width="%d"' % W0, t, 1); t = re.sub(r'\sheight="\d+"', ' height="%d"' % H0, t, 1)
            except Exception: pass
        in_card = 'article-card' in s[max(0, m.start() - 400):m.start()]
        if 'srcset=' not in t and p.endswith('.webp') and not re.search(r'-\d+\.webp$', u) and (art or in_card):
            W = Image.open(p).size[0]; ws = [w for w in (480, 800) if w < W - 100]
            if ws:
                for w in ws: variant(p, w)
                ss = ', '.join('%s %dw' % (os.path.splitext(u)[0] + '-%d.webp' % w, w) for w in ws) + ', %s %dw' % (u, W)
                sizes = '(max-width: 600px) 100vw, 330px' if in_card else '(max-width: 832px) calc(100vw - 32px), 800px'
                t = t[:-1].rstrip('/ ').rstrip() + ' srcset="%s" sizes="%s"' % (ss, sizes) + (' />' if t.endswith('/>') else '>')
        return t
    s = re.sub(r'<img\b[^>]*>', sub, s)
    return picturize(s, f)

def picturize(s, f):
    """Wrap local .webp <img> in <picture> with AVIF source (same srcset/sizes), once."""
    base = os.path.dirname(f)
    def wrap(m):
        t = m.group(0); pos = m.start()
        before = s[max(0, pos - 400):pos]
        if before.rfind('<picture') > before.rfind('</picture>'): return t
        src = re.search(r'\ssrc="([^"]+\.webp)"', t)
        if not src or src.group(1).startswith(('http', '//')): return t
        u = src.group(1); p = u.lstrip('/') if u.startswith('/') else os.path.normpath(os.path.join(base, u))
        if not os.path.exists(p) or not to_avif(p): return t
        ss = re.search(r'\ssrcset="([^"]*)"', t); sz = re.search(r'\ssizes="([^"]*)"', t)
        if ss:
            parts = []
            for item in ss.group(1).split(', '):
                url, _, w = item.partition(' ')
                q = url.lstrip('/') if url.startswith('/') else os.path.normpath(os.path.join(base, url))
                if os.path.exists(q) and to_avif(q): parts.append(url[:-5] + '.avif ' + w)
            avif_set = ', '.join(parts) if parts else u[:-5] + '.avif'
        else: avif_set = u[:-5] + '.avif'
        return '<picture><source type="image/avif" srcset="%s"%s>%s</picture>' % (avif_set, (' sizes="%s"' % sz.group(1)) if sz else '', t)
    return re.sub(r'<img\b[^>]*>', wrap, s)

def headings(s):
    spans = [(m.start(), m.end()) for m in re.finditer(r'<script.*?</script>|<style.*?</style>|<!--.*?-->', s, re.S)]
    inmask = lambda i: any(a <= i < b for a, b in spans)
    heads = [m for m in re.finditer(r'<(/?)h([1-6])\b', s) if not inmask(m.start())]
    pairs, stack = [], []
    for m in heads:
        if m.group(1) == '': stack.append(m)
        elif stack: pairs.append((stack.pop(), m))
    pairs.sort(key=lambda p: p[0].start()); prev = 0; remap = {}; edits = []
    for o, c in pairs:
        L = int(o.group(2)); eff = remap.get(L, L)
        if prev and eff > prev + 1: eff = prev + 1; remap[L] = eff
        for k in list(remap):
            if k > L: del remap[k]
        if eff != L: edits.append((o.start(), c.start(), L, eff))
        prev = eff
    for a, b, L, E in sorted(edits, reverse=True):
        s = s[:b] + s[b:].replace('</h%d' % L, '</h%d' % E, 1)
        s = s[:a] + s[a:].replace('<h%d' % L, '<h%d' % E, 1)
    return s

def a11y(s, ua):
    s = re.sub(r'<iframe\b(?![^>]*\stitle=)', lambda m: m.group(0) + ' title="%s"' % ('Карта проїзду' if ua else 'Карта проезда'), s)
    s = re.sub(r'<select name="bottles"(?![^>]*aria-label)', lambda m: m.group(0) + ' aria-label="%s"' % ('Кількість бутелів' if ua else 'Количество бутылей'), s)
    def noop(m):
        t = m.group(0)
        if 'noopener' in t: return t
        if re.search(r'\srel="', t): return re.sub(r'\srel="([^"]*)"', lambda r: ' rel="%s noopener"' % r.group(1).strip(), t, 1)
        return t[:-1] + ' rel="noopener">'
    s = re.sub(r'<a\b[^>]*target="_blank"[^>]*>', noop, s)
    def yt(m):
        t = m.group(0); v = re.search(r'/embed/([\w-]{6,})', t)
        if not v: return t
        title = re.search(r'title="([^"]*)"', t); title = title.group(1) if title else ('Відео' if ua else 'Видео')
        vid = v.group(1)
        return ('<span class="cw-yt"><a href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener" data-yt="%s" data-title="%s">'
                '<img src="https://i.ytimg.com/vi/%s/hqdefault.jpg" alt="%s" width="480" height="360" loading="lazy" decoding="async">'
                '<b aria-hidden="true">&#9654;</b><span class="cw-yt-label">%s</span></a></span>') % (vid, vid, title, vid, title, 'Дивитися на YouTube' if ua else 'Смотреть на YouTube')
    s = re.sub(r'<iframe\b[^>]*(?:youtube|youtu\.be)[^>]*>\s*</iframe>', yt, s)
    if 'data-yt=' in s and 'yt-facade.js' not in s:
        s = s.replace('</body>', '<script src="%sassets/js/yt-facade.js" defer></script>\n</body>' % ('../' if ua else ''), 1)
    s = re.sub(r'(src=")https?://(?:www\.)?youtube\.com/embed/', r'\1https://www.youtube-nocookie.com/embed/', s)
    if ua:
        s = re.sub(r'srcset="([^"]*)"', lambda m: 'srcset="%s"' % re.sub(r'(^|, )(?=(?:assets|images)/)', r'\1../', m.group(1)), s)
    s = re.sub(r'(<img\b[^>]*bottle_real[^>]*style=")(?![^"]*object-fit)', r'\1object-fit:contain;', s)
    s = re.sub(r'<main\b(?![^>]*\sid=)', '<main id="main"', s, 1)
    if ua:
        s = s.replace('Перейти к содержимому', 'Перейти до вмісту').replace('aria-label="Главное меню"', 'aria-label="Головне меню"')
    if 'id="orderForm"' in s and 'cw-noscript' not in s:
        msg = ('Для відправки форми потрібен JavaScript. Зателефонуйте: <a href="tel:+380637886880">+38 (063) 788-68-80</a> або напишіть у <a href="https://t.me/CrystalWaterBro_bot" rel="noopener">Telegram</a>.' if ua else
               'Для отправки формы нужен JavaScript. Позвоните: <a href="tel:+380637886880">+38 (063) 788-68-80</a> или напишите в <a href="https://t.me/CrystalWaterBro_bot" rel="noopener">Telegram</a>.')
        s = s.replace('</form>', '</form>\n<noscript><p class="cw-noscript cw-note">%s</p></noscript>' % msg, 1)
    s = s.replace("document.getElementById('hamburger').addEventListener(", "var hb = document.getElementById('hamburger'); hb && hb.addEventListener(")
    return s

n = 0
for f in pages:
    s = o = open(f, encoding='utf-8').read()
    s = images(s, f); s = headings(s); s = a11y(s, f.startswith('ua/'))
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print(n, 'pages updated')
