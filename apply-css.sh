#!/bin/bash
# ============================================
# Crystal Water — подключение CSS ко всем страницам
# ============================================
# Запускать из корня репозитория:
#   cd ~/.openclaw/workspace/crystal-water-site/
#   bash apply-css.sh
#
# ПЕРЕД ЗАПУСКОМ: сделайте git commit текущего состояния,
# чтобы можно было откатить в случае проблем:
#   git add -A && git commit -m "before css injection"

CSS_PATH="/header-footer-responsive.css"   # поменяйте, если файл лежит не в корне

echo "Ищу все .html файлы..."
FILES=$(find . -name "*.html")
COUNT=$(echo "$FILES" | wc -l)
echo "Найдено файлов: $COUNT"

for f in $FILES; do
  if grep -q "header-footer-responsive.css" "$f"; then
    echo "Пропуск (уже подключено): $f"
  else
    sed -i "s#</head>#<link rel=\"stylesheet\" href=\"${CSS_PATH}\">\n</head>#" "$f"
    echo "Подключено: $f"
  fi
done

echo ""
echo "Готово. Проверьте несколько файлов вручную:"
echo "  grep -l 'header-footer-responsive.css' *.html | head -5"
echo ""
echo "Затем закоммитьте:"
echo "  git add -A && git commit -m 'connect header-footer css to all pages'"
echo "  git push"
