#!/usr/bin/env bash
# CORPUS DIVINUS - загрузка открытых источников (фаза Q1)
set -euo pipefail
curl -sL "https://tanzil.net/pub/download/index.php?quranType=uthmani&outFormat=text&agree=true" -o quran_uthmani.txt
echo "Quran Uthmani (PD): $(wc -l < quran_uthmani.txt) строк"

# RU-перевод: Крачковский И.Ю. (PD с 2022 по российскому закону)
# Tanzil: https://tanzil.net/trans/ru.krachkovsky
curl -sL "https://tanzil.net/pub/download/index.php?transID=ru_krachkovsky&outFormat=text&agree=true" -o quran_ru_krachkovsky.txt
echo "Quran Krachkovsky (PD): $(wc -l < quran_ru_krachkovsky.txt) строк"
