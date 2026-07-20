#!/usr/bin/env bash
# CORPUS DIVINUS - загрузка открытых источников (фаза Q1)
set -euo pipefail
curl -sL "https://tanzil.net/pub/download/index.php?quranType=uthmani&outFormat=text&agree=true" -o quran_uthmani.txt
echo "Quran Uthmani (PD): $(wc -l < quran_uthmani.txt) строк"
