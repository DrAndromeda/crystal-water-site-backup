#!/usr/bin/env python3
"""
Генерация sitemap-ua.xml на основе существующего sitemap.xml.

Логика: берёт все <loc> из sitemap.xml, для каждой проверяет,
существует ли соответствующий файл в папке /ua/ с тем же именем.
Если да — добавляет запись в sitemap-ua.xml с путём /ua/....
Если UA-версии файла нет — пропускает и логирует.

Запуск (из корня репозитория, ПОСЛЕ fix_site_issues.py — чтобы
sitemap.xml был уже без бага с пропущенным слэшем):
    python3 generate_sitemap_ua.py

Если sitemap-ua.xml уже существует — скрипт НЕ перезапишет его молча,
а спросит подтверждение (см. флаг --force ниже).
"""

import os
import re
import sys

DOMAIN = "https://crystalwater.kiev.ua"
ROOT = "."
UA_DIR = os.path.join(ROOT, "ua")
SITEMAP_RU = os.path.join(ROOT, "sitemap.xml")
SITEMAP_UA = os.path.join(ROOT, "sitemap-ua.xml")


def extract_locs(sitemap_content):
    return re.findall(r"<loc>(.*?)</loc>", sitemap_content)


def main():
    force = "--force" in sys.argv

    if not os.path.exists(SITEMAP_RU):
        print(f"ОШИБКА: {SITEMAP_RU} не найден.")
        sys.exit(1)

    if os.path.exists(SITEMAP_UA) and not force:
        print(f"⚠️  {SITEMAP_UA} уже существует.")
        print("Если хочешь перезаписать, запусти с флагом --force:")
        print("  python3 generate_sitemap_ua.py --force")
        sys.exit(0)

    with open(SITEMAP_RU, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    locs = extract_locs(content)
    print(f"Найдено {len(locs)} URL в sitemap.xml")

    entries = []
    skipped = []

    for loc in locs:
        # Вычисляем имя файла из URL
        loc_clean = loc.replace(DOMAIN, "").lstrip("/")
        if loc_clean == "" or loc_clean == "index.html":
            fname = "index.html"
        else:
            fname = loc_clean

        ua_path = os.path.join(UA_DIR, fname)
        if os.path.exists(ua_path):
            ua_url = f"{DOMAIN}/ua/{fname}" if fname != "index.html" else f"{DOMAIN}/ua/"
            entries.append(ua_url)
        else:
            skipped.append(fname)

    xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in entries:
        xml_parts.append(f"  <url>\n    <loc>{url}</loc>\n  </url>")
    xml_parts.append("</urlset>")

    with open(SITEMAP_UA, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_parts) + "\n")

    print(f"\n✓ Создан {SITEMAP_UA} с {len(entries)} URL")
    print(f"\n⚠️  Пропущено (нет UA-версии файла): {len(skipped)}")
    for s in skipped:
        print(f"  ! {s}")

    print("\nПроверьте файл, затем:")
    print("  git add -A && git commit -m 'generate sitemap-ua.xml'")
    print("  git push")


if __name__ == "__main__":
    if not os.path.isdir(UA_DIR):
        print(f"ОШИБКА: папка {UA_DIR} не найдена. Запускайте из корня репозитория.")
        sys.exit(1)
    main()
