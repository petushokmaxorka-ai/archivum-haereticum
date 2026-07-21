# INTEGRATIO — ВСТРОЙКА В ДАШБОРД HERETIC OS

**MANUFACTORUM · Datum: 020.M3 (переписана после ревизии)**

---

### I. СООТВЕТСТВИЕ МОДУЛЕЙ

| Модуль Heretic OS | Источник данных Архива |
|---|---|
| PRINCIPIUM | `00-manuscriptum-principale/hypothesa-corporis.md` |
| CODEX | `01-eventus-babel/`, `03-rami-ecclesiae/` |
| LIBER | `02-libri-deperditi/` + сайт (тексты корпуса) |
| INQUISITIO | `04-pantheones/`, `05-probatio/` (в т.ч. DAMNATA) |
| MATRIX | `08-matrix-orthodoxa/` |
| CHRONICLE | `09-gentes/`, `data/timeline.json` |
| FORGE | `06-quaestiones-apertae/agenda.md` |
| NOOSPHERE | `data/corpus.json` + `corpus/data/*` (JSONL текстов) |
| SCRIPTORIUM | `07-scriptorium/`, сайт `scriptorium/` |
| MACHINA | `mcp/server.py` — MCP-доступ агентов к Архиву |

### II. ПРЯМОЕ ЧТЕНИЕ (без сервера)

Репозиторий публичный — дашборд может тянуть файлы напрямую:

```
https://raw.githubusercontent.com/petushokmaxorka-ai/archivum-haereticum/main/data/corpus.json
https://raw.githubusercontent.com/petushokmaxorka-ai/archivum-haereticum/main/data/timeline.json
https://raw.githubusercontent.com/petushokmaxorka-ai/archivum-haereticum/main/data/pantheones.json
https://raw.githubusercontent.com/petushokmaxorka-ai/archivum-haereticum/main/README.md
https://raw.githubusercontent.com/petushokmaxorka-ai/archivum-haereticum/main/REPERTORIUM.md
```

### III. ТЕКСТЫ КОРПУСА (JSONL)

Машиночитаемые слои всех завершённых корпусов:

| Набор | Путь | Формат |
|---|---|---|
| Коран (AR) | `corpus/data/quran/ar-quran-uthmani.jsonl` | {s, a, text, ru} |
| Новый Завет | `corpus/data/nt/*.jsonl` (27 книг) | {book, ch, vs, grc, rus} |
| Ветхий Завет | `corpus/data/tanakh/*.jsonl` (39 книг) | {book, ch, vs, he, grc, rus, grc_ref, rus_ref} |
| 1 Енох | `corpus/data/enoch1/enoch1.jsonl` | {ch, vs, gez, grc, eng, rus} |
| 2 Енох | `corpus/data/enoch2/enoch2.jsonl` | {ch, vs, eng, slav_ch} |
| Юбилеи | `corpus/data/jubilees/jubilees.jsonl` | {ch, vs, gez, gez_ref, eng, rus} |

### IV. ЖИВОЙ САЙТ (GitHub Pages)

`https://petushokmaxorka-ai.github.io/archivum-haereticum/`
Разделы: `tanakh/`, `nt/`, `quran/`, `enoch/`, `enoch2/`, `jubilees/`, `scriptorium/`. Статичный HTML — встраивается iframe-ом или прямыми ссылками из любого модуля.

### V. ПЕЧАТИ ДЛЯ UI

Поле `classificatio` в JSON и шапки досье: `FIDELIS` (зелёный/золотой), `SUSPECTUS` (янтарный), `DAMNATUS` (красный). Рекомендация: бейджи в стиле печатей — DAMNATA не скрывать, показывать с протоколом опровержения (это фишка Архива).

### VI. MCP-СЕРВЕР

`mcp/server.py` — FastMCP (stdio). Инструменты: `list_rami`, `get_ramus`, `get_timeline`, `get_pantheones`, `search_archivum`. Запуск:

```bash
pip install mcp
python mcp/server.py
```

### VII. СТРУКТУРНАЯ ПАМЯТЬ

Ревизия 020.M3: создан зал `09-gentes/` (народы и судьбы, 20 досье); `04-pantheones/` очищен до богов и культов (63); README/REPERTORIUM/INTEGRATIO переписаны. При чтении ссылок учитывать новые пути: боснийская и волошская арки, славянские народы — теперь в `09-gentes/`.

---
*Sigillum: STRUCTURA SANATA — MODULI PARATI.*
