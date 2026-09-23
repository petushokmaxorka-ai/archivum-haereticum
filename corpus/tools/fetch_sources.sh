#!/usr/bin/env bash
# CORPUS DIVINUS - загрузка открытых источников (фаза Q1)
set -euo pipefail
curl -fsSL "https://tanzil.net/pub/download/index.php?quranType=uthmani&outFormat=text&agree=true" -o quran_uthmani.txt
echo "Quran Uthmani (PD): $(wc -l < quran_uthmani.txt) строк"

# RU-перевод: Крачковский И.Ю. (PD с 2022 по российскому закону)
# Tanzil: https://tanzil.net/trans/ru.krachkovsky
# Формат txt-2: "сура|аят|текст" (+ блок комментариев "#" в конце).
# Старый адрес pub/download/index.php?transID=... отдаёт HTML-страницу, а не текст.
curl -fsSL "https://tanzil.net/trans/?transID=ru.krachkovsky&type=txt-2" -o quran_ru_krachkovsky.txt
echo "Quran Krachkovsky (PD): $(grep -c '|' quran_ru_krachkovsky.txt) аятов"
