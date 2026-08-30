#!/usr/bin/env python3
"""
Массовое исправление известных багов по всему сайту.

Исправляет:
1. sitemap.xml — добавляет "/" между доменом и именем файла
   там, где он пропущен
2. canonical / og:url — если случайно указывает на github.io,
   меняет на production-домен crystalwater.kiev.ua (сохраняя путь)
3. og:image — если путь относительный, делает абсолютным
4. опечатка "за бутыля" -> "за бутыль"

Запуск (из корня репозитория crystal-water-site-backup):
    python3 fix_site_issues.py

ПЕРЕД ЗАПУСКОМ: сделайте git commit текущего состояния.
После запуска проверьте отчёт и несколько файлов вручную перед коммитом.
"""

import os
import re
import sys

DOMAIN = "https://crystalwater.kiev.ua"
GITHUB_PAGES_PATTERNS = [
    r"https?://drandromeda\.github\.io/crystal-water-site-backup",
    r"https?://drandromeda\.github\.io",
]
ROOT = "."


def fix_sitemap(report):
    for name in ["sitemap.xml", "sitemap-ua.xml"]:
        path = os.path.join(ROOT, name)
        if not os.path.exists(path):
            report["sitemap_missing"].append(name)
            continue
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Ищем <loc>https://crystalwater.kiev.uaXXX</loc> без слэша
        fixed = re.sub(
            r"(https?://crystalwater\.kiev\.ua)(?!/)([a-zA-Z0-9])",
            r"\1/\2",
            content,
        )
        if fixed != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(fixed)
            report["sitemap_fixed"].append(name)
        else:
            report["sitemap_ok"].append(name)


def fix_html_file(path, report):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()
    original = html

    # 1. canonical/og:url на github.io -> production
    for pattern in GITHUB_PAGES_PATTERNS:
        html = re.sub(pattern, DOMAIN, html)

    # 2. og:image относительный путь -> абсолютный
    #    ищем content="images/..." или content="assets/images/..."
    #    (без http/https и без ведущего /)
    def fix_og_image(m):
        prefix = m.group(1)
        path_value = m.group(2)
        if path_value.startswith(("http://", "https://")):
            return m.group(0)
        if not path_value.startswith("/"):
            path_value = "/" + path_value
        return f'{prefix}{DOMAIN}{path_value}"'

    html = re.sub(
        r'(<meta property="og:image" content=")([^"]+)"',
        fix_og_image,
        html,
    )

    # 3. Опечатка "за бутыля" -> "за бутыль"
    html = html.replace("за бутыля", "за бутыль")

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        report["html_fixed"].append(path)


def main():
    report = {
        "sitemap_fixed": [], "sitemap_ok": [], "sitemap_missing": [],
        "html_fixed": [],
    }

    fix_sitemap(report)

    # Обходим все .html файлы, включая /ua/
    for dirpath, _, filenames in os.walk(ROOT):
        if ".git" in dirpath:
            continue
        for fname in filenames:
            if fname.endswith(".html"):
                fix_html_file(os.path.join(dirpath, fname), report)

    print("=" * 50)
    print("SITEMAP")
    print(f"  Исправлено: {report['sitemap_fixed']}")
    print(f"  Уже ок: {report['sitemap_ok']}")
    print(f"  Не найдено: {report['sitemap_missing']}")

    print(f"\nHTML-файлов исправлено: {len(report['html_fixed'])}")
    for p in report["html_fixed"]:
        print(f"  ✓ {p}")

    print("=" * 50)
    print("Проверьте несколько файлов вручную (особенно og:image и")
    print("canonical), затем:")
    print("  git add -A && git commit -m 'fix sitemap slashes, canonical domain, og:image paths, typo'")
    print("  git push")


if __name__ == "__main__":
    main()
