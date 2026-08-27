# Crystal Water — инструкция для ассистента

## Контекст
Реплейс сайта доставки воды в Броварах. Оригинал: https://crystalwater.kiev.ua/ (не менять, источник контента)
GitHub: https://github.com/DrAndromeda/crystal-water-site-backup
Pages: https://drandromeda.github.io/crystal-water-site-backup/
Все 71 HTML страницы лежат в корне репозитория.

## Приоритет: SEO — не потерять трафик
Не менять URL/slug, title/H1. Хлебные крошки обязательно.

## Баги к исправлению

1. sitemap.xml — 7 URL без / после домена (about.html, articles.html, o-nas.html, prices.html, tech.html, tekhnologii-ochistki.html, uslugi-i-tseny.html). Починить генератор, не только вывод.
2. href="/" — на GitHub Pages ведёт не туда, заменить на href="./"
3. Ссылка на UA — везде /ua/ (папка), не ua.html. Внутренние страницы ссылаются на зеркало slug.
4. og:image — относительные пути заменить на абсолютные (https://crystalwater.kiev.ua/...)
5. Единый набор соцсетей в футере во всех 71 страницах.
6. prices.html: "за бутыля" → "за бутыль"
7. prices.html: артефакты markdown-конвертации (****, /*)

## Новые задачи

A. hreflang на все страницы (RU + UA) — 142 уникальных пары.
B. sitemap-ua.xml — создать по образу sitemap.xml с /ua/... путями. Проверить баг №1.

Работать напрямую с репозиторием, не через фетч GitHub raw.