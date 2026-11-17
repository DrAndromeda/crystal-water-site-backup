#!/usr/bin/env python3
"""CSS build: minify sources + bundle consecutive local <link rel=stylesheet> runs into one file per unique set.
Sources (css/*.css, css/pages/*.css) stay editable. Bundles live in css/b/ (manifest: css/b/manifest.json).
Run after editing any CSS or after build_new/build_ua/build_core:   python3 build_css.py"""
import re, glob, os, json, hashlib

def minify(c):
    c = re.sub(r'/\*.*?\*/', '', c, flags=re.S)
    c = re.sub(r'@charset[^;]*;', '', c)
    c = re.sub(r'\s+', ' ', c)
    c = re.sub(r'\s*([{};,>])\s*', r'\1', c)
    return c.replace(';}', '}').strip()

def rebase_urls(css, src_dir, out_dir):
    def sub(m):
        q, u = m.group(1), m.group(2)
        if re.match(r'^(data:|https?:|//|/|#)', u): return m.group(0)
        return 'url(%s%s%s)' % (q, os.path.relpath(os.path.normpath(os.path.join(src_dir, u)), out_dir).replace(os.sep, '/'), q)
    return re.sub(r'url\((["\']?)([^)"\']+)\1\)', sub, css)

MAN = 'css/b/manifest.json'
os.makedirs('css/b', exist_ok=True)
manifest = json.load(open(MAN)) if os.path.exists(MAN) else {}
LINK = r'<link rel="stylesheet" href="((?:\.\./)?css/[^"]+)"\s*/?>'
RUN = re.compile(r'(?:[ \t]*' + LINK + r'[ \t]*\n?){1,}')
pages = [f for f in glob.glob('*.html') + glob.glob('ua/*.html')]
used = set(); made = 0
def source_of(href):
    href = re.sub(r'^\.\./', '', href)
    if href.startswith('css/b/'):
        return manifest.get(os.path.basename(href)[:-8], [])
    return [href.replace('.min.css', '.css')]

for f in pages:
    s = o = open(f, encoding='utf-8').read(); pre = '../' if f.startswith('ua/') else ''
    def run(m):
        global made
        srcs = []
        for h in re.findall(LINK, m.group(0)):
            for x in source_of(h):
                if x not in srcs: srcs.append(x)
        srcs = [x for x in srcs if os.path.exists(x)]
        if not srcs: return m.group(0)
        key = hashlib.md5('|'.join(srcs).encode()).hexdigest()[:10]
        name = 'css/b/%s.min.css' % key; manifest[key] = srcs; used.add(key)
        css = ''.join(rebase_urls(minify(open(x, encoding='utf-8').read()), os.path.dirname(x), 'css/b') + '\n' for x in srcs)
        open(name, 'w', encoding='utf-8').write(css); made += 1
        return '<link rel="stylesheet" href="%s%s">\n' % (pre, name)
    s = RUN.sub(run, s)
    s = re.sub(r'<script src="(https?:[^"]+)"(?![^>]*(?:defer|async))', r'<script src="\1" defer', s)
    if s != o: open(f, 'w', encoding='utf-8').write(s)
for k in list(manifest):
    if k not in used:
        manifest.pop(k); 
        p = 'css/b/%s.min.css' % k
        if os.path.exists(p): os.remove(p)
json.dump(manifest, open(MAN, 'w'), indent=1)
# remove legacy *.min.css siblings (now only bundles are served)
for f in glob.glob('css/**/*.min.css', recursive=True):
    if not f.startswith('css/b/'): os.remove(f)
print(len(manifest), 'bundles;', sum(os.path.getsize(f) for f in glob.glob('css/b/*.css')) // 1024, 'KB total')
