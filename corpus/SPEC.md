# SPEC — СХЕМА ДАННЫХ CORPUS DIVINUS

## 1. Единица хранения

Один стих = одна строка JSONL (UTF-8, без BOM):

```json
{
  "corpus": "quran",
  "book": 4,
  "chapter": 4,
  "verse": 157,
  "original": "وَقَوْلِهِمْ…",
  "orig_lang": "ar",
  "translit": null,
  "ru": "…",
  "ru_kind": "kratchkovsky",
  "fons_orig": "Tanzil Uthmani (Public Domain)",
  "fons_ru": "Крачковский И.Ю. (1963; PD с 2022)",
  "stamp": "FIDELIS"
}
```

- `corpus`: quran | nt | lxx | hb | enoch1 | enoch2 | iubilaei | rigveda | avesta | stela | columba
- `orig_lang`: ar | he | grc | cu | sa | ae | zh | gez
- `ru_kind`: kratchkovsky | synodal | literal-archivum
- `stamp`: FIDELIS | SUSPECTUS | DAMNATUS

## 2. Правила

1. Нет источника — нет строки. Каждый слой имеет `fons_*`.
2. Нумерация — по изданию источника (Коран — куфийская, 6236; LXX — по Ральфсу).
3. `corpus/data/` и сайт не редактируются руками — только генераторы.
4. Контроль целостности: sha256 + счётчики в `corpus/data/_checksums.json`.
5. Переводный стек: базовый PD-перевод, поверх — дословный слой Архива отдельными файлами.

## 3. Интеграция

JSONL читается построчно любым языком; для Heretic OS — модуль NOOSPHERE. Статические страницы — модуль LIBER (iframe или копия файлов).
