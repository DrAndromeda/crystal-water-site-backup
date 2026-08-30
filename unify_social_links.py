#!/usr/bin/env python3
"""
Унификация ссылок на соцсети по всем страницам сайта.

Проблема (найдена при аудите): на разных страницах в футере указаны
разные аккаунты — где-то crystalwater.brovary, где-то
crystalwater.kiev.ua, плюс на некоторых страницах twitter
@CrystalWoter, которого нет на других. Это выглядит как рассинхрон
при копировании шаблона, а не осознанное решение.

⚠️ ПЕРЕД ЗАПУСКОМ: пропиши в CANONICAL_LINKS ниже те аккаунты,
которые пользователь подтвердил как правильные/актуальные — сейчас
там стоят значения, которые я видел в футере главной страницы,
ПРОВЕРЬ их с пользователем перед запуском, не запускай вслепую.

Запуск (из корня репозитория):
    python3 unify_social_links.py
"""

import os
import re
import sys

ROOT = "."

# ⚠️ ПРОВЕРЬ ЭТИ ЗНАЧЕНИЯ С ПОЛЬЗОВАТЕЛЕМ ПЕРЕД ЗАПУСКОМ
CANONICAL_LINKS = {
    "instagram": "https://www.instagram.com/crystalwater.brovary/",
    "facebook": "https://www.facebook.com/crystalwater.brovary/",
    "telegram": "https://t.me/CrystalWaterBro_bot",
}

# Паттерны, которые нужно заменить (варианты, встречавшиеся на сайте)
REPLACEMENTS = [
    (re.compile(r'https?://(www\.)?instagram\.com/crystalwater\.kiev\.ua/?'),
     CANONICAL_LINKS["instagram"]),
    (re.compile(r'https?://(www\.)?facebook\.com/crystalwater\.kiev\.ua/?'),
     CANONICAL_LINKS["facebook"]),
]

# Twitter — на части страниц был @CrystalWoter, на других его не было
# вообще. Если решите убрать твиттер полностью (раз он не везде) —
# раскомментируй этот блок:
REMOVE_TWITTER = True
TWITTER_LINK_PATTERN = re.compile(
    r'<a[^>]*href=["\']https?://(www\.)?twitter\.com/CrystalWoter[^"\']*["\'][^>]*>.*?</a>',
    re.IGNORECASE | re.DOTALL,
)


def process_file(path, report):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()
    original = html

    for pattern, replacement in REPLACEMENTS:
        html = pattern.sub(replacement, html)

    if REMOVE_TWITTER:
        html = TWITTER_LINK_PATTERN.sub("", html)

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        report["updated"].append(path)


def main():
    report = {"updated": []}

    for dirpath, _, filenames in os.walk(ROOT):
        if ".git" in dirpath:
            continue
        for fname in filenames:
            if fname.endswith(".html"):
                process_file(os.path.join(dirpath, fname), report)

    print("=" * 50)
    print(f"Обновлено файлов: {len(report['updated'])}")
    for p in report["updated"]:
        print(f"  ✓ {p}")
    print("=" * 50)
    print("Проверьте несколько файлов вручную, затем:")
    print("  git add -A && git commit -m 'unify social media links across all pages'")
    print("  git push")


if __name__ == "__main__":
    main()
