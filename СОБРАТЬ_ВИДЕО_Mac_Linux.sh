#!/bin/bash
# Склеивает видео из частей (.part01, .part02, ...) обратно в целые файлы.
# Запуск: откройте терминал в этой папке и выполните:  bash СОБРАТЬ_ВИДЕО_Mac_Linux.sh
cd "$(dirname "$0")"
find . -name '*.part01' | while read -r f; do
  base="${f%.part01}"
  cat "$base".part* > "$base"
  echo "Готово: $base"
done
echo "Все видео собраны. Части (.partXX) можно удалить."
