# Add UA/RU as 7th menu item on all pages
import re

# RU pages -> UA as 7th item
ru_pages = {
    'index.html': {'active': 'Доставка воды', 'ua': 'ua/index.html'},
    'uslugi-i-tseny.html': {'active': 'Цены', 'ua': 'ua/tsiny.html'},
    'tekhnologii-ochistki.html': {'active': 'Технологии', 'ua': 'ua/tekhnologii-ochystky.html'},
    'articles.html': {'active': 'Статьи', 'ua': 'ua/index.html'},
    'about.html': {'active': 'О нас', 'ua': 'ua/about.html'},
    'o-nas.html': {'active': 'Контакты', 'ua': 'ua/pro-nas.html'},
}

# UA pages -> RU as 7th item
ua_pages = {
    'ua/index.html': {'active': 'Головна', 'ru': '../'},
    'ua/tsiny.html': {'active': 'Ціни', 'ru': '../'},
    'ua/tekhnologii-ochystky.html': {'active': 'Технології', 'ru': '../'},
    'ua/about.html': {'active': 'Про нас', 'ru': '../'},
    'ua/pro-nas.html': {'active': 'Контакти', 'ru': '../'},
}

# UA mapping for UA pages - which pages in UA
ua_menu_items = {
    'ua/index.html': 'ua',
    'ua/tsiny.html': 'ua',
    'ua/tekhnologii-ochystky.html': 'ua',
    'ua/about.html': 'ua',
    'ua/pro-nas.html': 'ua',
}

items_ru = [
    ('./', 'Доставка воды'),
    ('uslugi-i-tseny.html', 'Цены'),
    ('tekhnologii-ochistki.html', 'Технологии'),
    ('articles.html', 'Статьи'),
    ('about.html', 'О нас'),
    ('o-nas.html', 'Контакты'),
]

items_ua = [
    ('index.html', 'Головна'),
    ('tsiny.html', 'Ціни'),
    ('tekhnologii-ochystky.html', 'Технології'),
    ('index.html', 'Статті'),
    ('about.html', 'Про нас'),
    ('pro-nas.html', 'Контакти'),
]

def make_nav(items, active_text, lang_link, lang_label):
    """Build the nav HTML with lang as 7th item"""
    lis = []
    for href, text in items:
        cls = ' class="is-active"' if text == active_text else ''
        lis.append(f'          <li{cls}><a href="{href}">{text}</a></li>')
    # 7th item: language switcher
    lis.append(f'          <li class="nav-lang"><a href="{lang_link}" class="lang-switch">{lang_label}</a></li>')
    return '\n'.join(lis)

# Fix RU pages
for ru_file, info in ru_pages.items():
    with open(ru_file, 'r') as f:
        c = f.read()
    
    # Find and replace the entire nav UL
    old_nav_match = re.search(r'<ul>(.*?)</ul>', c, re.DOTALL)
    if not old_nav_match:
        print(f"  ⚠️ {ru_file}: no <ul> in nav found")
        continue
    
    new_nav = make_nav(items_ru, info['active'], info['ua'], 'UA')
    new_ul = f'<ul>\n{new_nav}\n        </ul>'
    c = c.replace(old_nav_match.group(0), new_ul)
    
    # Remove any standalone header__ua-btn (no longer needed)
    c = c.replace('      <a href="' + info['ua'] + '" class="header__ua-btn">UA</a>\n  </header>', '\n  </header>')
    
    with open(ru_file, 'w') as f:
        f.write(c)
    print(f"  ✅ {ru_file} — UA in menu")

# Fix UA pages
for ua_file, info in ua_pages.items():
    with open(ua_file, 'r') as f:
        c = f.read()
    
    old_nav_match = re.search(r'<ul>(.*?)</ul>', c, re.DOTALL)
    if not old_nav_match:
        print(f"  ⚠️ {ua_file}: no <ul> in nav found")
        continue
    
    new_nav = make_nav(items_ua, info['active'], info['ru'], 'RU')
    new_ul = f'<ul>\n{new_nav}\n        </ul>'
    c = c.replace(old_nav_match.group(0), new_ul)
    
    # Remove standalone RU button if exists
    c = c.replace('      <a href="' + info['ru'] + '" class="header__ua-btn">RU</a>\n  </header>', '\n  </header>')
    
    with open(ua_file, 'w') as f:
        f.write(c)
    print(f"  ✅ {ua_file} — RU in menu")

print("\nВсе страницы обновлены")