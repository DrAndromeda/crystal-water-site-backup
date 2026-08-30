#!/usr/bin/env python3
"""
Автоматическая вставка hreflang-тегов во все страницы сайта.

Логика: для каждого .html файла в корне репозитория (RU-версия)
ищем соответствующий файл в /ua/ с тем же именем. Если найден —
вставляем в <head> обеих страниц пару hreflang-ссылок друг на друга.
Если UA-версии нет — пропускаем файл и логируем это в отчёт.

Запуск (из корня репозитория crystal-water-site-backup):
    python3 add_hreflang.py

ПЕРЕД ЗАПУСКОМ: сделайте git commit текущего состояния.
"""

import os
import re
import sys

DOMAIN = "https://crystalwater.kiev.ua"
ROOT = "."  # корень репозитория, запускать скрипт из него
UA_DIR = os.path.join(ROOT, "ua")

SKIP_FILES = {"index.html"}  # index.html обрабатывается отдельно ниже как "/"


def hreflang_block(ru_url, ua_url):
    return (
        f'<link rel="alternate" hreflang="ru" href="{ru_url}" />\n'
        f'<link rel="alternate" hreflang="uk" href="{ua_url}" />\n'
        f'<link rel="alternate" hreflang="x-default" href="{ru_url}" />\n'
    )


def already_has_hreflang(html):
    return 'hreflang=' in html


def insert_before_head_close(html, block):
    idx = html.lower().find("</head>")
    if idx == -1:
        return None  # нет закрывающего </head> — файл странный, пропускаем
    return html[:idx] + block + html[idx:]


def process_pair(ru_path, ua_path, ru_url, ua_url, report):
    for path, url_self, url_other, lang_self in [
        (ru_path, ru_url, ua_url, "ru"),
        (ua_path, ua_url, ru_url, "uk"),
    ]:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()

        if already_has_hreflang(html):
            report["skipped_already_has"].append(path)
            continue

        block = hreflang_block(ru_url, ua_url)
        new_html = insert_before_head_close(html, block)

        if new_html is None:
            report["no_head_tag"].append(path)
            continue

        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)
        report["updated"].append(path)


def main():
    report = {"updated": [], "skipped_already_has": [], "no_head_tag": [], "no_ua_pair": []}

    # Главная страница отдельно (URL без имени файла)
    ru_index = os.path.join(ROOT, "index.html")
    ua_index = os.path.join(UA_DIR, "index.html")
    if os.path.exists(ru_index) and os.path.exists(ua_index):
        process_pair(ru_index, ua_index, f"{DOMAIN}/", f"{DOMAIN}/ua/", report)
    else:
        report["no_ua_pair"].append(ru_index)

    # Остальные .html файлы в корне
    for fname in sorted(os.listdir(ROOT)):
        if not fname.endswith(".html") or fname in SKIP_FILES:
            continue
        ru_path = os.path.join(ROOT, fname)
        ua_path = os.path.join(UA_DIR, fname)

        if not os.path.isfile(ru_path):
            continue

        ru_url = f"{DOMAIN}/{fname}"
        ua_url = f"{DOMAIN}/ua/{fname}"

        if os.path.exists(ua_path):
            process_pair(ru_path, ua_path, ru_url, ua_url, report)
        else:
            report["no_ua_pair"].append(ru_path)

    # Отчёт
    print("=" * 50)
    print(f"Обновлено файлов: {len(report['updated'])}")
    for p in report["updated"]:
        print(f"  ✓ {p}")

    print(f"\nПропущено (уже есть hreflang): {len(report['skipped_already_has'])}")
    for p in report["skipped_already_has"]:
        print(f"  - {p}")

    print(f"\n⚠️  Нет пары в /ua/ (пропущено): {len(report['no_ua_pair'])}")
    for p in report["no_ua_pair"]:
        print(f"  ! {p}")

    print(f"\n⚠️  Нет тега </head> (пропущено, проверить вручную): {len(report['no_head_tag'])}")
    for p in report["no_head_tag"]:
        print(f"  ! {p}")

    print("=" * 50)
    print("Готово. Проверьте несколько файлов вручную, затем:")
    print("  git add -A && git commit -m 'add hreflang tags to RU/UA pairs'")
    print("  git push")


if __name__ == "__main__":
    if not os.path.isdir(UA_DIR):
        print(f"ОШИБКА: папка {UA_DIR} не найдена. Запускайте скрипт из корня репозитория.")
        sys.exit(1)
    main()
