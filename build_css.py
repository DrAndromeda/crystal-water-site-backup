#!/usr/bin/env python3
"""Minify css/**/*.css -> *.min.css and point HTML <link> tags at the .min files.
Sources stay editable; run again after editing any CSS:  python3 build_css.py"""
import re, glob, os

def minify(c):
    c = re.sub(r'/\*.*?\*/', '', c, flags=re.S)
    c = re.sub(r'@charset[^;]*;', '', c)
    c = re.sub(r'\s+', ' ', c)
    c = re.sub(r'\s*([{};,>])\s*', r'\1', c)
    c = c.replace(';}', '}')
    return c.strip()

srcs = [f for f in glob.glob('css/**/*.css', recursive=True) if not f.endswith('.min.css')]
for f in srcs:
    open(f[:-4] + '.min.css', 'w', encoding='utf-8').write(minify(open(f, encoding='utf-8').read()))
names = {os.path.relpath(f, 'css') for f in srcs}
n = 0
for h in glob.glob('*.html') + glob.glob('ua/*.html'):
    s = o = open(h, encoding='utf-8').read()
    def sub(m):
        rel = m.group(2)
        return m.group(1) + rel[:-4] + '.min.css' + m.group(3) if rel in names else m.group(0)
    s = re.sub(r'(<link rel="stylesheet" href="(?:\.\./)?css/)([^"]+\.css)(")', lambda m: (m.group(1) + (m.group(2)[:-4] + '.min.css' if m.group(2) in names else m.group(2)) + m.group(3)), s)
    if s != o: open(h, 'w', encoding='utf-8').write(s); n += 1
print(len(srcs), 'files minified;', n, 'pages updated')
