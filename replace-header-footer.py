#!/usr/bin/env python3
import os
import re
import sys

SITE_ROOT = "/Users/andromeda/.openclaw/workspace/crystal-water-site-backup"

with open(os.path.join(SITE_ROOT, "header-new.html"), "r", encoding="utf-8") as f:
    HEADER = f.read().strip()

with open(os.path.join(SITE_ROOT, "footer-new.html"), "r", encoding="utf-8") as f:
    FOOTER = f.read().strip()

BREADCRUMB_HOME = '<a href="./">Доставка воды Бровары</a>'

def get_breadcrumb(filepath):
    """Возвращает HTML хлебных крошек для файла."""
    filename = os.path.basename(filepath)
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
        return f'<nav class="breadcrumbs" aria-label="breadcrumb">{BREADCRUMB_HOME} &raquo; <span>{category}</span></nav>'
    else:
        # Статья - берем название из title
        return f'<nav class="breadcrumbs" aria-label="breadcrumb">{BREADCRUMB_HOME} &raquo; <span>Статья</span></nav>'

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Ищем тело
    body_start = content.find("<body")
    if body_start == -1:
        print(f"  ❌ Нет тега <body> в {os.path.basename(filepath)}")
        return False
    body_end = content.find("</body>", body_start)
    if body_end == -1:
        print(f"  ❌ Нет закрывающего </body> в {os.path.basename(filepath)}")
        return False
    body_end += len("</body>")
    
    old_body = content[body_start:body_end]
    
    # Извлекаем основной контент между header и footer (грубо)
    # Удаляем известные header и footer по классам
    # Просто возьмем все внутри body, потом удалим блоки с помощью regex
    inner = old_body
    # Удаляем существующие header (обычно <header class="header">...)
    inner = re.sub(r'<header[\s\S]*?</header>', '', inner)
    # Удаляем существующий footer
    inner = re.sub(r'<footer[\s\S]*?</footer>', '', inner)
    # Удаляем utility bar если есть
    inner = re.sub(r'<div class="utility"[\s\S]*?</div>', '', inner)
    # Удаляем плавающие кнопки
    inner = re.sub(r'<a class="floating-telegram"[\s\S]*?</a>', '', inner)
    inner = re.sub(r'<button class="scrollup"[\s\S]*?</button>', '', inner)
    inner = re.sub(r'<div class="modal"[\s\S]*?</div>', '', inner)
    # Удаляем лишние пустые строки
    inner = inner.replace('<body', '').replace('</body>', '').strip()
    
    # Собираем новое тело
    breadcrumb = get_breadcrumb(filepath)
    new_body = '<body>\n'
    new_body += HEADER + '\n'
    if breadcrumb:
        new_body += breadcrumb + '\n'
    new_body += '<main class="container">\n'
    new_body += inner + '\n'
    new_body += '</main>\n'
    new_body += FOOTER + '\n'
    new_body += '</body>'
    
    new_content = content[:body_start] + new_body + content[body_end:]
    
    # Записываем обратно
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True

def main():
    # Обрабатываем только HTML файлы в корне, исключая ua папку
    count = 0
    for root, dirs, files in os.walk(SITE_ROOT):
        if "ua" in root:
            continue
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                print(f"Обрабатываю {file}...")
                if process_file(filepath):
                    count += 1
                else:
                    print(f"  Пропущено.")
    print(f"Обработано файлов: {count}")

if __name__ == "__main__":
    main()