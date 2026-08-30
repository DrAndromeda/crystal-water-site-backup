#!/usr/bin/env python3
"""
Полуавтоматическая генерация Article JSON-LD для всех статей.

Логика: скрипт находит все .html файлы, которые выглядят как статьи
(начинаются с цифры — паттерн "43-chistaya-voda...html", это текущий
паттерн именования статей на сайте), вытаскивает существующий <title>
и первый <h1> со страницы, и вставляет заполненный Article JSON-LD
в <head> ПЕРЕД </head>.

⚠️ datePublished ставится как ДАТА ЗАПУСКА СКРИПТА (заглушка) —
это не настоящая дата публикации статьи, потому что на сайте её
нигде не было. Обязательно замени вручную на реальную дату, если
она есть в Obsidian/истории коммитов/архиве старого сайта (Wayback
Machine может показать дату первой индексации).

Запуск (из корня репозитория, ПОСЛЕ hreflang и fix_site_issues):
    python3 generate_article_jsonld.py

ПЕРЕД ЗАПУСКОМ: git commit текущего состояния.
"""

import os
import re
import sys
from datetime import date

DOMAIN = "https://crystalwater.kiev.ua"
ROOT = "."
TODAY = date.today().isoformat()

# Паттерн статей — файлы вида "43-chistaya-voda....html" в корне
ARTICLE_PATTERN = re.compile(r"^\d+-.+\.html$")


def extract_title(html):
    m = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    return m.group(1).strip() if m else None


def extract_h1(html):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.IGNORECASE | re.DOTALL)
    if not m:
        return None
    # убрать вложенные теги, если есть
    return re.sub(r"<[^>]+>", "", m.group(1)).strip()


def extract_description(html):
    m = re.search(
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        html, re.IGNORECASE,
    )
    return m.group(1).strip() if m else None


def already_has_article_schema(html):
    return '"@type": "Article"' in html or "'@type': 'Article'" in html


def build_jsonld(fname, title, description, breadcrumb_name):
    url = f"{DOMAIN}/{fname}"
    desc = description or f"Статья о воде: {title}"
    return f'''
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "Доставка воды Бровары",
      "item": "{DOMAIN}/"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "Статьи о воде",
      "item": "{DOMAIN}/voda-h2o-stati/"
    }},
    {{
      "@type": "ListItem",
      "position": 3,
      "name": "{breadcrumb_name}",
      "item": "{url}"
    }}
  ]
}}
</script>

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "description": "{desc}",
  "author": {{
    "@type": "Organization",
    "name": "Crystal Water"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Crystal Water"
  }},
  "datePublished": "{TODAY}",
  "dateModified": "{TODAY}",
  "mainEntityOfPage": {{
    "@type": "WebPage",
    "@id": "{url}"
  }}
}}
</script>
'''


def process_file(path, fname, report):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    if already_has_article_schema(html):
        report["skipped_has_schema"].append(fname)
        return

    title = extract_title(html) or extract_h1(html)
    if not title:
        report["skipped_no_title"].append(fname)
        return

    description = extract_description(html)
    h1 = extract_h1(html) or title

    block = build_jsonld(fname, title, description, h1)

    idx = html.lower().find("</head>")
    if idx == -1:
        report["no_head_tag"].append(fname)
        return

    new_html = html[:idx] + block + html[idx:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)
    report["updated"].append(fname)


def main():
    report = {
        "updated": [], "skipped_has_schema": [],
        "skipped_no_title": [], "no_head_tag": [],
    }

    for fname in sorted(os.listdir(ROOT)):
        if ARTICLE_PATTERN.match(fname):
            process_file(os.path.join(ROOT, fname), fname, report)

    print("=" * 50)
    print(f"Обновлено статей: {len(report['updated'])}")
    for f in report["updated"]:
        print(f"  ✓ {f}")

    print(f"\nПропущено (уже есть Article schema): {len(report['skipped_has_schema'])}")
    print(f"Пропущено (не найден title/h1, заполнить вручную): {len(report['skipped_no_title'])}")
    for f in report["skipped_no_title"]:
        print(f"  ! {f}")
    print(f"Пропущено (нет </head>): {len(report['no_head_tag'])}")

    print("=" * 50)
    print("⚠️  datePublished/dateModified поставлены как сегодняшняя дата —")
    print("    это ЗАГЛУШКА, замени на реальные даты, если найдёшь их")
    print("    (Wayback Machine, история Obsidian-заметок, и т.п.)")
    print()
    print("Проверьте несколько файлов вручную, затем:")
    print("  git add -A && git commit -m 'add Article JSON-LD to blog posts'")
    print("  git push")


if __name__ == "__main__":
    main()
