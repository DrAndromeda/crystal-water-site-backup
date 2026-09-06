#!/usr/bin/env python3
"""Apply batch 7 and batch 8 content updates to Crystal Water article HTML files."""

import os, re

REPO = "/Users/andromeda/.openclaw/workspace/crystal-water-site-backup"

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# ============================================================
# NEW CONTENT BLOCKS (from batch files)
# ============================================================

# --- BATCH 7 ---

CONTENT_49 = '''  <main>
    <section class="article-content" style="max-width:800px;margin:40px auto;padding:0 16px;line-height:1.6;">
      <h1 style="font-size:32px;color:var(--cw-blue-dark);margin-bottom:24px;">Вкус и характеристики воды после обратного осмоса</h1>

      <h2 style="font-size:24px;color:var(--cw-blue-dark);margin-top:32px;">Вкусовые характеристики</h2>
      <p style="margin-bottom:16px;">Вода после обратного осмоса имеет нейтральный, "чистый" вкус — без хлорного или металлического привкуса, характерного для водопроводной воды.</p>

      <h2 style="font-size:24px;color:var(--cw-blue-dark);margin-top:32px;">Основные характеристики</h2>
      <ul style="margin-bottom:16px;">
        <li style="margin-bottom:8px;">Низкое содержание растворённых солей после мембранной очистки</li>
        <li style="margin-bottom:8px;">Прозрачность</li>
        <li style="margin-bottom:8px;">Отсутствие постороннего запаха</li>
        <li style="margin-bottom:8px;">Возможна последующая минерализация для сбалансированного состава</li>
      </ul>

      <h2 style="font-size:24px;color:var(--cw-blue-dark);margin-top:32px;">Почему может ощущаться "мягче" обычной воды</h2>
      <p style="margin-bottom:16px;">Сниженное содержание солей жёсткости делает вкус воды более мягким по сравнению с водопроводной.</p>

      <p>Подробнее о технологии — <a href="/obratnyij-osmos-i-ego-ispolzovanie.html">обратный осмос: как работает</a>.</p>

      <p style="margin-top:32px;"><a href="articles.html" style="color:#2980b9;">← Все статьи</a> <a href="./" style="color:#2980b9;margin-left:16px;">На главную</a></p>
    </section>
  </main>'''

CONTENT_50 = '''  <main>
    <section class="article-content" style="max-width:800px;margin:40px auto;padding:0 16px;line-height:1.6;">
      <h1 style="font-size:32px;color:var(--cw-blue-dark);margin-bottom:24px;">Схема обратного осмоса: устройство системы по этапам</h1>

      <p style="margin-bottom:16px;">Рассмотрим пошаговую схему прохождения воды через систему обратного осмоса, от входа до выхода очищенной воды.</p>

      <h2 style="font-size:24px;color:var(--cw-blue-dark);margin-top:32px;">Пошаговая схема</h2>
      <ol style="margin-bottom:16px;">
        <li style="margin-bottom:8px;"><strong>Вход</strong> — вода поступает в систему</li>
        <li style="margin-bottom:8px;"><strong>Предфильтр</strong> — механическая очистка от крупных частиц</li>
        <li style="margin-bottom:8px;"><strong>Угольный фильтр</strong> — удаление хлора и органики</li>
        <li style="margin-bottom:8px;"><strong>Мембрана обратного осмоса</strong> — основная тонкая очистка</li>
        <li style="margin-bottom:8px;"><strong>Накопительный бак</strong> — хранение очищенной воды</li>
        <li style="margin-bottom:8px;"><strong>Постфильтр</strong> — финальная полировка перед использованием</li>
      </ol>

      <p>Для сравнения с другими методами читайте <a href="/obratnyij-osmos-i-ego-ispolzovanie.html">статью об обратном осмосе</a>.</p>

      <p style="margin-top:32px;"><a href="articles.html" style="color:#2980b9;">← Все статьи</a> <a href="./" style="color:#2980b9;margin-left:16px;">На главную</a></p>
    </section>
  </main>'''

CONTENT_52 = '''  <main>
    <section class="article-content" style="max-width:800px;margin:40px auto;padding:0 16px;line-height:1.6;">
      <h1 style="font-size:32px;color:var(--cw-blue-dark);margin-bottom:24px;">Вода после обратного осмоса с доставкой в Киев</h1>

      <p style="margin-bottom:16px;">Мы доставляем воду, прошедшую многоступенчатую очистку методом обратного осмоса, в Киев и Броварской район.</p>

      <h2 style="font-size:24px;color:var(--cw-blue-dark);margin-top:32px;">Почему обратный осмос — эффективная технология очистки</h2>
      <ul style="margin-bottom:16px;">
        <li style="margin-bottom:8px;">Удаляет большинство растворённых примесей</li>
        <li style="margin-bottom:8px;">Обеспечивает стабильный состав от партии к партии</li>
        <li style="margin-bottom:8px;">Сочетается с последующей минерализацией для сбалансированного вкуса</li>
      </ul>

      <h2 style="font-size:24px;color:var(--cw-blue-dark);margin-top:32px;">Условия доставки в Киев</h2>
      <p style="margin-bottom:16px;">Уточните зону обслуживания и условия доставки: +380637886880 или на странице <a href="/prices.html">цены</a>.</p>

      <p>Подробнее о технологии — <a href="/obratnyij-osmos-i-ego-ispolzovanie.html">обратный осмос: как работает</a>.</p>

      <p style="margin-top:32px;"><a href="articles.html" style="color:#2980b9;">← Все статьи</a> <a href="./" style="color:#2980b9;margin-left:16px;">На главную</a></p>
    </section>
  </main>'''

CONTENT_55 = '''  <main>
    <section class="article-content" style="max-width:800px;margin:40px auto;padding:0 16px;line-height:1.6;">
      <h1 style="font-size:32px;color:var(--cw-blue-dark);margin-bottom:24px;">Актуальные акции на доставку воды</h1>

      <div style="background:#fff3cd;border:1px solid #ffc107;border-radius:8px;padding:16px;margin-bottom:24px;">
        ⚠️ Эта страница требует регулярного обновления — актуальные акции меняются со временем. Уточните у пользователя текущие действующие предложения перед публикацией, не переносить устаревшие акции с оригинального сайта автоматически.
      </div>

      <h2 style="font-size:24px;color:var(--cw-blue-dark);margin-top:32px;">Постоянное предложение</h2>
      <ul style="margin-bottom:16px;">
        <li style="margin-bottom:8px;">Первая бутыль бесплатно при первом заказе (минимум 2 бутыли)</li>
        <li style="margin-bottom:8px;">Бесплатный экспресс-анализ воды</li>
      </ul>

      <p>Следите за актуальными акциями в нашем <a href="https://t.me/CrystalWaterBro_bot">Telegram</a>.</p>

      <p style="margin-top:32px;"><a href="articles.html" style="color:#2980b9;">← Все статьи</a> <a href="./" style="color:#2980b9;margin-left:16px;">На главную</a></p>
    </section>
  </main>'''

CONTENT_56 = '''  <main>
    <section class="article-content" style="max-width:800px;margin:40px auto;padding:0 16px;line-height:1.6;">
      <h1 style="font-size:32px;color:var(--cw-blue-dark);margin-bottom:24px;">Бутилированная и минеральная вода: в чём разница</h1>

      <h2 style="font-size:24px;color:var(--cw-blue-dark);margin-top:32px;">Сравнение</h2>
      <table style="width:100%;border-collapse:collapse;margin:24px 0;border:1px solid #ddd;">
        <tr><th style="border:1px solid #ddd;padding:12px;background:#eaf6fc;">Параметр</th><th style="border:1px solid #ddd;padding:12px;background:#eaf6fc;">Бутилированная (очищенная)</th><th style="border:1px solid #ddd;padding:12px;background:#eaf6fc;">Минеральная</th></tr>
        <tr><td style="border:1px solid #ddd;padding:12px;">Источник</td><td style="border:1px solid #ddd;padding:12px;">Очищена производственным способом</td><td style="border:1px solid #ddd;padding:12px;">Природный минеральный источник</td></tr>
        <tr><td style="border:1px solid #ddd;padding:12px;">Минерализация</td><td style="border:1px solid #ddd;padding:12px;">Контролируемая, сбалансированная</td><td style="border:1px solid #ddd;padding:12px;">Природная, может быть выше нормы для постоянного питья</td></tr>
        <tr><td style="border:1px solid #ddd;padding:12px;">Рекомендуемое использование</td><td style="border:1px solid #ddd;padding:12px;">Ежедневное питьё</td><td style="border:1px solid #ddd;padding:12px;">Периодическое употребление, по рекомендации врача при лечебном использовании</td></tr>
      </table>

      <h2 style="font-size:24px;color:var(--cw-blue-dark);margin-top:32px;">Что выбрать для ежедневного питья</h2>
      <p style="margin-bottom:16px;">Для регулярного повседневного употребления обычно рекомендуется вода с умеренной, сбалансированной минерализацией — избыточное постоянное потребление лечебно-минеральной воды с высокой концентрацией солей стоит обсудить с врачом.</p>

      <p>Наша вода имеет сбалансированный состав, подходящий для ежедневного питья — <a href="/tekhnologii-ochistki.html">подробнее о технологии</a>.</p>

      <p style="margin-top:32px;"><a href="articles.html" style="color:#2980b9;">← Все статьи</a> <a href="./" style="color:#2980b9;margin-left:16px;">На главную</a></p>
    </section>
  </main>'''

# --- BATCH 7 also has article 51 (kak-proverit-kachestvo-butilirovannoj-vodyi.html) but that's NOT in our task list
# ARTICLES FROM BATCH 7 THAT ARE IN THE TASK:
# 49: kakaya-voda-posle-osmosa-na-vkus-i-xarakteristiki.html ✓
# 50: kak-vyiglyadit-sxema-osmosa-obratnogo.html ✓
# 51: kak-proverit-kachestvo-butilirovannoj-vodyi.html - NOT in task list, skip
# 52: obratnyij-osmos-v-kiev-dlya-ochistki.html ✓
# 53: postoyannyie-akczii-butilirovannaya-voda-krishtalevo-chista.html ✓ (wrong number in task - file is #55 in batch but task says article 4/55)
# Actually wait, let me re-read the task more carefully

# BATCH 7 (task numbering):
# 1. kakaya-voda-posle-osmosa-na-vkus-i-xarakteristiki.html → article 49 → CONTENT_49
# 2. kak-vyiglyadit-sxema-osmosa-obratnogo.html → article 50 → CONTENT_50
# 3. obratnyij-osmos-v-kiev-dlya-ochistki.html → article 52 → CONTENT_52
# 4. postoyannyie-akczii-butilirovannaya-voda-krishtalevo-chista.html → article 55 → CONTENT_55 
# 5. pochemu-luchshaya-butilirovannaya-voda-poleznej-mineralnoj.html → article 56 → CONTENT_56
# 6. filtryi-dlya-vodyi-krishtalevo-chista-pitna-voda.html → article 54 → CONTENT_54 (new-layout)
# 7. ochistka-vodyi-obratnyij-osmos-otlichie-distilyaczii.html → article 53 → CONTENT_53 (new-layout)

# BATCH 8 (task numbering):
# 8. razreshaem-ili-zapreshhaem-pit-kofe-beremennyim.html → SKIP (already updated)
# 9. chto-pit-beremennyim-dlya-otlichnogo-samochuvstviya.html → article 58 → CONTENT_58 (new-layout)
# 10. mineralnaya-voda-dlya-organizma-i-dlya-tela.html → article 59 → CONTENT_59
# 11. zakazat-vodu-prosto-esli-znaesh-o-nej-vse.html → article 60 → CONTENT_60 (new-layout)
# 12. nauchnyij-film-o-vode-i-chistote-zhizni.html → article 61 → CONTENT_61 (placeholder)
# 13. infografik-o-neobxodimosti-i-polze-vodyi.html → article 62 → CONTENT_62 (placeholder)
# 14. chto-nuzhno-znat-pokupaya-vodu-v-butyilke.html → article 63 → CONTENT_63

# --- BATCH 8 ---

CONTENT_58 = '''  <main class="article-container">
    <h1>Питьевой режим при беременности: общие рекомендации</h1>

    <p>Потребность в жидкости может меняться во время беременности — точные рекомендации всегда стоит получать от наблюдающего врача.</p>

    <h2>Общие соображения</h2>
    <ul>
      <li>Поддержание регулярного питьевого режима — часть общего здорового образа жизни</li>
      <li>Выбирайте воду с проверенным стабильным составом</li>
      <li>При отёках или других особенностях — режим питья корректирует врач</li>
    </ul>

    <div style="background:#fff3cd;border:1px solid #ffc107;border-radius:8px;padding:16px;margin:24px 0;">
      ⚠️ Данная статья носит общий информационный характер. Обязательно консультируйтесь с врачом по вопросам питания и питья при беременности.
    </div>

    <p>Для качественной питьевой воды дома — <a href="/prices.html">узнайте об условиях доставки</a>.</p>
  </main>'''

CONTENT_59 = '''  <main>
    <section class="article-content" style="max-width:800px;margin:40px auto;padding:0 16px;line-height:1.6;">
      <h1 style="font-size:32px;color:var(--cw-blue-dark);margin-bottom:24px;">Минеральная вода: состав и особенности употребления</h1>

      <h2 style="font-size:24px;color:var(--cw-blue-dark);margin-top:32px;">Виды минеральной воды по минерализации</h2>
      <ul style="margin-bottom:16px;">
        <li style="margin-bottom:8px;"><strong>Столовая</strong> — низкая минерализация, подходит для регулярного питья</li>
        <li style="margin-bottom:8px;"><strong>Лечебно-столовая</strong> — умеренная минерализация, периодическое употребление</li>
        <li style="margin-bottom:8px;"><strong>Лечебная</strong> — высокая минерализация, употребляется курсами по рекомендации врача</li>
      </ul>

      <h2 style="font-size:24px;color:var(--cw-blue-dark);margin-top:32px;">Как выбрать</h2>
      <p style="margin-bottom:16px;">Для повседневного использования подходит столовая вода с низкой минерализацией. Лечебные виды минеральной воды стоит употреблять по согласованию с врачом, особенно при наличии хронических заболеваний.</p>

      <p>Сравнение с очищенной бутилированной водой — в статье <a href="/pochemu-luchshaya-butilirovannaya-voda-poleznej-mineralnoj.html">бутилированная и минеральная вода</a>.</p>

      <p style="margin-top:32px;"><a href="articles.html" style="color:#2980b9;">← Все статьи</a> <a href="./" style="color:#2980b9;margin-left:16px;">На главную</a></p>
    </section>
  </main>'''

CONTENT_60 = '''  <main class="article-container">
    <h1>Как заказать воду с доставкой в Броварах</h1>

    <h2>Процесс заказа</h2>
    <ol>
      <li>Оставьте заявку по телефону +380637886880 или в <a href="https://t.me/CrystalWaterBro_bot">Telegram</a></li>
      <li>Уточните адрес и удобное время доставки</li>
      <li>Получите воду в удобное вечернее время после 20:00</li>
      <li>Оплатите при получении</li>
    </ol>

    <h2>Условия первого заказа</h2>
    <ul>
      <li>Минимальный заказ — 2 бутыли</li>
      <li>Первая бутыль — бесплатно</li>
      <li>Залог за тару — 225 грн (возвращается)</li>
    </ul>

    <p>Узнайте актуальные цены на странице <a href="/prices.html">цены и условия</a>.</p>
  </main>'''

CONTENT_61 = '''  <main>
    <section class="article-content" style="max-width:800px;margin:40px auto;padding:0 16px;line-height:1.6;">
      <h1 style="font-size:32px;color:var(--cw-blue-dark);margin-bottom:24px;">Наука о воде: что важно знать</h1>

      <div style="background:#fff3cd;border:1px solid #ffc107;border-radius:8px;padding:16px;margin-bottom:24px;">
        ⚠️ Уточнить у пользователя: планируется ли встраивание конкретного видео-фильма, или тема должна быть раскрыта текстово. Не создавать контент "под пустое название" без понимания реального замысла.
      </div>

      <p style="margin-top:32px;"><a href="articles.html" style="color:#2980b9;">← Все статьи</a> <a href="./" style="color:#2980b9;margin-left:16px;">На главную</a></p>
    </section>
  </main>'''

CONTENT_62 = '''  <main>
    <section class="article-content" style="max-width:800px;margin:40px auto;padding:0 16px;line-height:1.6;">
      <h1 style="font-size:32px;color:var(--cw-blue-dark);margin-bottom:24px;">Инфографика: роль воды для организма</h1>

      <div style="background:#fff3cd;border:1px solid #ffc107;border-radius:8px;padding:16px;margin-bottom:24px;">
        ⚠️ Требуется подготовка реальной инфографики (визуального актива). Без готового изображения эта страница будет пустой оболочкой — уточнить у дизайнера/пользователя, планируется ли создание такой инфографики, и на основе каких проверенных источников данных.
      </div>

      <!-- Когда инфографика будет готова, встроить как:
      <img src="/images/infographic-water-benefits.webp" alt="Инфографика: роль воды для организма" width="800" height="1200" loading="lazy"> -->

      <p style="margin-top:32px;"><a href="articles.html" style="color:#2980b9;">← Все статьи</a> <a href="./" style="color:#2980b9;margin-left:16px;">На главную</a></p>
    </section>
  </main>'''

CONTENT_63 = '''  <main>
    <section class="article-content" style="max-width:800px;margin:40px auto;padding:0 16px;line-height:1.6;">
      <h1 style="font-size:32px;color:var(--cw-blue-dark);margin-bottom:24px;">Что нужно знать, покупая воду в бутылке</h1>

      <h2 style="font-size:24px;color:var(--cw-blue-dark);margin-top:32px;">Чек-лист перед покупкой</h2>
      <ul style="margin-bottom:16px;">
        <li style="margin-bottom:8px;">Проверьте маркировку и материал тары</li>
        <li style="margin-bottom:8px;">Убедитесь в целостности упаковки и пломбы</li>
        <li style="margin-bottom:8px;">Обратите внимание на срок годности</li>
        <li style="margin-bottom:8px;">Уточните технологию очистки у производителя</li>
        <li style="margin-bottom:8px;">Запросите сертификаты качества, если покупаете оптом или на регулярной основе</li>
      </ul>

      <h2 style="font-size:24px;color:var(--cw-blue-dark);margin-top:32px;">Разница между разовой покупкой и доставкой</h2>
      <p style="margin-bottom:16px;">Для регулярного использования доставка на дом или в офис удобнее разовых покупок в магазине — не нужно носить тяжёлые бутыли самостоятельно, а условия (залог, обмен тары) заранее прозрачны.</p>

      <p>Узнайте об условиях доставки — <a href="/prices.html">цены и условия заказа</a>.</p>

      <p style="margin-top:32px;"><a href="articles.html" style="color:#2980b9;">← Все статьи</a> <a href="./" style="color:#2980b9;margin-left:16px;">На главную</a></p>
    </section>
  </main>'''

# --- For new-layout articles, replace just the main content (between <main class="article-container"> and </main>)

CONTENT_53 = '''  <main class="article-container">
    <h1>Обратный осмос и дистилляция: в чём разница</h1>

    <table style="width:100%;border-collapse:collapse;margin:24px 0;">
      <tr><th style="border:1px solid #ddd;padding:12px;background:#eaf6fc;">Параметр</th><th style="border:1px solid #ddd;padding:12px;background:#eaf6fc;">Обратный осмос</th><th style="border:1px solid #ddd;padding:12px;background:#eaf6fc;">Дистилляция</th></tr>
      <tr><td style="border:1px solid #ddd;padding:12px;">Принцип</td><td style="border:1px solid #ddd;padding:12px;">Мембранная фильтрация под давлением</td><td style="border:1px solid #ddd;padding:12px;">Испарение и конденсация</td></tr>
      <tr><td style="border:1px solid #ddd;padding:12px;">Энергозатраты</td><td style="border:1px solid #ddd;padding:12px;">Ниже</td><td style="border:1px solid #ddd;padding:12px;">Выше</td></tr>
      <tr><td style="border:1px solid #ddd;padding:12px;">Минералы</td><td style="border:1px solid #ddd;padding:12px;">Частично снижены, возможна минерализация</td><td style="border:1px solid #ddd;padding:12px;">Практически полностью удалены</td></tr>
      <tr><td style="border:1px solid #ddd;padding:12px;">Скорость</td><td style="border:1px solid #ddd;padding:12px;">Быстрее</td><td style="border:1px solid #ddd;padding:12px;">Медленнее</td></tr>
      <tr><td style="border:1px solid #ddd;padding:12px;">Типичное применение</td><td style="border:1px solid #ddd;padding:12px;">Питьевая вода, бытовая фильтрация</td><td style="border:1px solid #ddd;padding:12px;">Лабораторные, технические нужды</td></tr>
    </table>

    <h2 style="font-size:24px;color:var(--cw-blue-dark);margin-top:32px;">Что выбрать для питьевой воды</h2>
    <p>Для повседневного питья обратный осмос с последующей контролируемой минерализацией — более практичный вариант, обеспечивающий как глубокую очистку, так и приятный сбалансированный вкус.</p>

    <p>Подробнее о нашей технологии — <a href="/tekhnologii-ochistki.html">здесь</a>.</p>
  </main>'''

CONTENT_54 = '''  <main class="article-container">
    <h1>Фильтры для воды: виды и как выбрать</h1>

    <h2>Виды бытовых фильтров</h2>
    <ul>
      <li><strong>Фильтр-кувшин</strong> — базовая очистка, недорого</li>
      <li><strong>Проточный фильтр</strong> — устанавливается под мойку, более глубокая очистка</li>
      <li><strong>Система обратного осмоса</strong> — максимальная степень очистки для дома</li>
    </ul>

    <h2>Как выбрать</h2>
    <ul>
      <li>Оцените качество исходной водопроводной воды в вашем районе</li>
      <li>Учитывайте объём ежедневного потребления</li>
      <li>Регулярно меняйте картриджи согласно рекомендациям производителя</li>
    </ul>

    <h2>Альтернатива — доставка готовой очищенной воды</h2>
    <p>Если не хотите заниматься обслуживанием фильтра — доставка готовой многоступенчато очищенной воды избавляет от этой заботы. Подробнее — <a href="/prices.html">цены</a>.</p>
  </main>'''

# ============================================================
# REPLACEMENT RULES
# ============================================================

# Old-layout files: replace everything from <main> to </main>
# New-layout files: replace everything from <main class="article-container"> to </main>

replacement_old_layout = re.compile(
    r'  <main>.*?</main>', re.DOTALL
)

replacement_new_layout = re.compile(
    r'  <main class="article-container">.*?</main>', re.DOTALL
)

# ============================================================
# APPLY
# ============================================================

replacements = [
    # (filename, regex_pattern, new_content)
    # Batch 7 - old layout
    ("kakaya-voda-posle-osmosa-na-vkus-i-xarakteristiki.html", replacement_old_layout, CONTENT_49),
    ("kak-vyiglyadit-sxema-osmosa-obratnogo.html", replacement_old_layout, CONTENT_50),
    ("obratnyij-osmos-v-kiev-dlya-ochistki.html", replacement_old_layout, CONTENT_52),
    ("postoyannyie-akczii-butilirovannaya-voda-krishtalevo-chista.html", replacement_old_layout, CONTENT_55),
    ("pochemu-luchshaya-butilirovannaya-voda-poleznej-mineralnoj.html", replacement_old_layout, CONTENT_56),

    # Batch 7 - new layout
    ("ochistka-vodyi-obratnyij-osmos-otlichie-distilyaczii.html", replacement_new_layout, CONTENT_53),
    ("filtryi-dlya-vodyi-krishtalevo-chista-pitna-voda.html", replacement_new_layout, CONTENT_54),

    # Batch 8 - new layout
    ("chto-pit-beremennyim-dlya-otlichnogo-samochuvstviya.html", replacement_new_layout, CONTENT_58),
    ("zakazat-vodu-prosto-esli-znaesh-o-nej-vse.html", replacement_new_layout, CONTENT_60),

    # Batch 8 - old layout
    ("mineralnaya-voda-dlya-organizma-i-dlya-tela.html", replacement_old_layout, CONTENT_59),
    ("nauchnyij-film-o-vode-i-chistote-zhizni.html", replacement_old_layout, CONTENT_61),
    ("infografik-o-neobxodimosti-i-polze-vodyi.html", replacement_old_layout, CONTENT_62),
    ("chto-nuzhno-znat-pokupaya-vodu-v-butyilke.html", replacement_old_layout, CONTENT_63),
]

success = []
errors = []

for fname, pattern, new_content in replacements:
    fpath = os.path.join(REPO, fname)
    if not os.path.exists(fpath):
        errors.append(f"{fname}: FILE NOT FOUND")
        continue

    content = read_file(fpath)
    new_full, count = pattern.subn(new_content, content)

    if count == 0:
        errors.append(f"{fname}: NO MATCH FOUND for pattern")
        continue

    # Verify H1 is correct
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', new_full)
    if h1_match:
        print(f"  ✓ H1: {h1_match.group(1)[:60]}")

    write_file(fpath, new_full)
    success.append(fname)
    print(f"  ✓ {fname} - replaced {count} occurrence(s)")

print(f"\n=== RESULTS ===")
print(f"Success: {len(success)} files")
for f in success:
    print(f"  ✓ {f}")
print(f"Errors: {len(errors)} files")
for e in errors:
    print(f"  ✗ {e}")