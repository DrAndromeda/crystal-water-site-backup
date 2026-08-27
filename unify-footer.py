#!/usr/bin/env python3
import os
import re

SITE_ROOT = "/Users/andromeda/.openclaw/workspace/crystal-water-site-backup"

# Читаем эталонный футер из index.html
with open(os.path.join(SITE_ROOT, "index.html"), "r", encoding="utf-8") as f:
    content = f.read()
    # Ищем footer
    footer_match = re.search(r'(<footer[\s\S]*?</footer>)', content)
    if footer_match:
        standard_footer = footer_match.group(1)
        print(f"Эталонный футер извлечен, длина {len(standard_footer)} символов")
    else:
        print("Не удалось извлечь футер из index.html")
        exit(1)

# Обрабатываем все HTML файлы, кроме index.html и файлов в папке ua
for root, dirs, files in os.walk(SITE_ROOT):
    if "ua" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            if file == "index.html":
                continue
            with open(filepath, "r", encoding="utf-8") as f:
                file_content = f.read()
            # Заменяем footer
            new_content = re.sub(r'<footer[\s\S]*?</footer>', standard_footer, file_content, flags=re.DOTALL)
            if new_content != file_content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Обновлен футер в {file}")
            else:
                print(f"Футер не найден или уже совпадает в {file}")