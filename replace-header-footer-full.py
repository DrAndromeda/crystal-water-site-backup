#!/usr/bin/env python3
import os
import re

SITE_ROOT = "/Users/andromeda/.openclaw/workspace/crystal-water-site-backup"

with open(os.path.join(SITE_ROOT, "header-new.html"), "r", encoding="utf-8") as f:
    NEW_HEADER = f.read().strip()

with open(os.path.join(SITE_ROOT, "footer-new.html"), "r", encoding="utf-8") as f:
    NEW_FOOTER = f.read().strip()

CSS_LINK = '<link rel="stylesheet" href="css/header-footer-responsive.css">'

def get_breadcrumb(filepath, filename):
    if filename == "index.html":
        return None
    # Определяем категорию
    if filename in ["about.html", "prices.html", "tech.html", "articles.html"]:
        category = {
            "about.html": "Контакты",
            "prices.html": "Цены",
            "tech.html": "Технологии очистки",
            "articles.html": "Статьи о воде"
        }.get(filename)
        return f'<nav class="breadcrumbs" aria-label="breadcrumb"><a href="./">Доставка воды Бровары</a> &raquo; <span>{category}</span></nav>'
    else:
        # Статья - просто статья
        return f'<nav class="breadcrumbs" aria-label="breadcrumb"><a href="./">Доставка воды Бровары</a> &raquo; <span>Статья</span></nav>'

def process_file(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Добавляем CSS ссылку в head, если нет
    if CSS_LINK not in content:
        # Вставляем после <head> или перед </head>
        head_close = content.find("</head>")
        if head_close != -1:
            content = content[:head_close] + "\n  " + CSS_LINK + content[head_close:]
    
    # Заменяем header
    # Удаляем существующий header (и utility bar)
    new_content = re.sub(r'<div class="utility"[\s\S]*?</div>', '', content)
    new_content = re.sub(r'<header[\s\S]*?</header>', NEW_HEADER, new_content, flags=re.DOTALL)
    
    # Вставляем хлебные крошки после header
    breadcrumb = get_breadcrumb(filepath, filename)
    if breadcrumb:
        # Найти позицию после header
        header_pos = new_content.find("</header>")
        if header_pos != -1:
            new_content = new_content[:header_pos + len("</header>")] + "\n" + breadcrumb + new_content[header_pos + len("</header>"):]
    
    # Заменяем footer
    new_content = re.sub(r'<footer[\s\S]*?</footer>', NEW_FOOTER, new_content, flags=re.DOTALL)
    
    # Удаляем старые плавающие кнопки и модалки (можно оставить)
    # new_content = re.sub(r'<a class="floating-telegram"[\s\S]*?</a>', '', new_content)
    # new_content = re.sub(r'<button class="scrollup"[\s\S]*?</button>', '', new_content)
    # new_content = re.sub(r'<div class="modal"[\s\S]*?</div>', '', new_content)
    
    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False

def main():
    count = 0
    for root, dirs, files in os.walk(SITE_ROOT):
        if "ua" in root:
            continue
        for file in files:
            if file.endswith(".html") and file not in ["header-footer.html", "hreflang-template.html", "header-new.html", "footer-new.html"]:
                filepath = os.path.join(root, file)
                print(f"Обрабатываю {file}...")
                if process_file(filepath):
                    count += 1
                    print(f"  Обновлен.")
                else:
                    print(f"  Без изменений.")
    print(f"Обработано файлов: {count}")

if __name__ == "__main__":
    main()