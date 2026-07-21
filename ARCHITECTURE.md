# ARCHITECTURE
## Карта Архива: что есть, как устроено, куда класть

**CLASSIFICATIO: ◆ FIDELIS**
Datum: 020.M3

Этот файл — для тех, кто хочет **внести вклад** в Архив или **понять его структуру**. Если вы просто читатель — `README.md` и `REPERTORIUM.md` вам достаточно. Если вы автор нового досье или разработчик MCP — читайте.

---

## I. ОБЩАЯ КАРТА

```
archivum-haereticum/
├── 00-manuscriptum-principale/   PROOEMUM, hypothesа, concordantia
├── 01-eventus-babel/             Башня, Втор 32, Смотрители
├── 02-libri-deperditi/           Утраченные книги
├── 03-rami-ecclesiae/            Ветви церквей
├── 04-pantheones/                Боги и культы (62 досье)
├── 05-probatio/                  PROBATA, DAMNATA, velesova-kniga
├── 06-quaestiones-apertae/       Открытые вопросы
├── 07-scriptorium/                Параллельные Писания
├── 08-matrix-orthodoxa/          Православная матрица
├── 09-gentes/                    Народы и судьбы (20 досье)
│
├── corpus/                        CORPUS DIVINUS (6 корпусов, JSONL)
├── data/                          JSON-ядра (corpus, pantheones, timeline)
├── docs/                          Живой сайт (GitHub Pages)
├── site/                          Собранный сайт (для Actions)
│
├── mcp/server.py                  MCP-сервер для агентов
├── scripts/                       Утилиты
│
├── LICENSE                        CC BY-SA 4.0
├── README.md                       Входная точка
├── REPERTORIUM.md                  Полный реестр
├── GLOSSARY.md                     Термины
├── ARCHITECTURE.md                 Этот файл
├── AUDIT.md                        История ревизий
├── INTEGRATIO.md                   Инструкция встройки в Heretic OS
│
├── .github/workflows/             GitHub Actions
└── (метафайлы: .gitignore, .gitattributes, и т.д.)
```

---

## II. ЗАЛЫ АРХИВА

| Зал | Назначение | Что внутри |
|---|---|---|
| **00** | Принципы | PROOEMIUM, hypothesа, concordantia, CREDO |
| **01** | Башня и Смотрители | babel, vigiles |
| **02** | Утраченные книги | 1 Енох, 2 Енох, Юбилеи, Кебра, Голубиная, Метатрон-Идрис, Наг-Хаммади |
| **03** | Ветви церквей | 9 досье (Эфиопия → Ислам) |
| **04** | Боги и культы | 62 досье (см. `REPERTORIUM.md` §III) |
| **05** | PROBATA/DAMNATA | probata, damnata, velesova-kniga, slavyano-arii |
| **06** | Открытые вопросы | agenda.md |
| **07** | Параллельные Писания | scriptorium/index.html |
| **08** | Православная матрица | 9 досье + DAMNATA-NOSTRA |
| **09** | Народы и судьбы | 20 досье (tribus-slavica → valachia-sclavia) |

---

## III. ФОРМАТ ДОСЬЕ

Каждое досье — файл в Markdown с обязательной структурой:

```markdown
# LATINUM NOMEN
## Русский перевод / подзаголовок

**CLASSIFICATIO: ◆ FIDELIS (что) / ◇ SUSPECTUS (что) / ✠ DAMNATUS (что) / ✚ CREDO (что)**
Datum: 020.M3

---

### I. РАЗДЕЛ — тире-пояснение
[абзацы: нарратив + сноски + IT-метафоры + ссылки на досье]

### II. РАЗДЕЛ
...

### X. VERDICTUM
[3-5 строк итога]

---
*Sigillum: ЛАТИНСКАЯ ФРАЗА — тире-уточнение.*
```

### Обязательные элементы

1. **Заголовок H1** — латинизированное имя (например, `BUDDHISMUS`, `AEGYPTUS`).
2. **Подзаголовок H2** — русский перевод + метафора через дефис.
3. **Строка CLASSIFICATIO** — печать с пояснением. Можно несколько печатей.
4. **Datum** — имперская дата (020.M3 и т.д.).
5. **Нумерованные секции** (I, II, III...) — не подзаголовки H2, а заголовки H3.
6. **VERDICTUM** в конце.
7. **Sigillum** — последняя строка.
8. **Межссылки** через обратные кавычки: `см. \`04-pantheones/anima.md\``.

### Не обязательно, но рекомендуется

- Сноски в формате `[Автор, Год, стр.]` с ISBN где возможно
- Схолии (краткие комментарии в конце раздела) курсивом
- Таблицы для сравнений
- IT-метафоры в духе архива

---

## IV. СИСТЕМА ПЕЧАТЕЙ

**Подробно** — `00/PROOEMIUM.md` §II и `GLOSSARY.md` §I.

Краткое правило:
- **◆ FIDELIS** — ставит архив на основании источников.
- **◇ SUSPECTUS** — ставит архив для рабочих гипотез.
- **✠ DAMNATUS** — ставит архив после протокола опровержения.
- **✚ CREDO** — ставит **только владелец** для личной веры.

**Применение CREDO:**
- Владелец может добавить ✚ к существующему досье Kimi, **не редактируя** Kimi-овский текст, а только строку CLASSIFICATIO.
- В одном досье могут сосуществовать архивная печать + ✚ CREDO.
- ✚ не отменяет архивные печати.

---

## V. JSON-ЯДРА

Три файла в `data/`:

- **`corpus.json`** — массив `rami` (ветви). Поля: `id, nomen, fork, linea, lingua, strategia, servata[], culmen, classificatio, dossier`.
- **`pantheones.json`** — массив `pantheones` (8 пантеонов) + отдельные объекты (sinae_vulgaris, buddhismus).
- **`timeline.json`** — массив `eventus` (события). Поля: `datum_wh40k, anno, eventus, locus, classificatio`.

При добавлении нового досье, если оно относится к ветви, **обновите `corpus.json`**. Если к пантеону — **`pantheones.json`**. Если к событию — **`timeline.json`**.

---

## VI. MCP-СЕРВЕР

`mcp/server.py` — FastMCP-сервер. 5 инструментов:

1. `list_rami()` — список ветвей
2. `get_ramus(ramus_id)` — досье + текст по `dossier`-пути
3. `get_timeline()` — все события
4. `get_pantheones()` — все пантеоны + sinae + buddhismus
5. `search_archivum(query)` — полнотекстовый поиск

Запуск:
```bash
pip install mcp
python mcp/server.py
```

Подключение в `claude-code` / `opencode` / любой MCP-клиент:
```json
{
  "mcpServers": {
    "archivum-haereticum": {
      "command": "python",
      "args": ["mcp/server.py"]
    }
  }
}
```

---

## VII. КАК ДОБАВИТЬ НОВОЕ ДОСЬЕ

1. **Определите зал.** В какой зал положить?
   - Пантеон/культ → `04-pantheones/`
   - Народ/государство → `09-gentes/`
   - Утраченная книга → `02-libri-deperditi/`
   - Ветвь церкви → `03-rami-ecclesiae/`
   - Мифологический сюжет → `04-pantheones/` (если бог/культ) или `00-manuscriptum-principale/concordantia.md` (если слот)

2. **Имя файла.** Латинизированное, нижний регистр, дефис. Примеры: `buddhismus.md`, `taoismus.md`, `09-gentes/slavs/moravia-magna.md`.

3. **Структура досье.** По §III выше.

4. **Печать.** Определите по `PROOEMIUM.md` §II. Не ставьте ✚ CREDO — только владелец.

5. **Межссылки.** Добавьте 2-5 ссылок на существующие досье.

6. **JSON-ядра.** Если досье относится к ветви/пантеону/событию — обновите `data/*.json`.

7. **REPERTORIUM.md.** Добавьте досье в соответствующий раздел.

8. **Пуш.** Коммитьте с сообщением: `Зал XX: [название] — [что внутри]`.

---

## VIII. КАК ОБНОВИТЬ CONCORDATIA

`00/concordantia.md` — главный артефакт архива. При добавлении нового слота (темы):

1. Добавьте секцию в формате III–XXII (одна секция на слот).
2. Добавьте строку в сводную таблицу (§XXIII).
3. Сноски с ISBN где возможно.
4. Связь с другими слотами в VERDICTUM (§XXIV).

---

## IX. СБОРКА САЙТА

Сайт автоматически собирается через GitHub Actions при push в main. Workflow в `.github/workflows/build.yml`:
1. `corpus/tools/fetch_sources.sh` — загружает Tanzil (если нужен).
2. `corpus/tools/build_quran.py` — собирает JSONL и HTML-страницы.
3. `corpus/tools/verify.py` — проверяет sha256 + счётчики.
4. `corpus/tools/assemble_site.sh` (если есть) — копирует Scriptorium и Concordantia.
5. `git commit + push` (если есть изменения).

---

## X. ЛИЦЕНЗИЯ И КОНТРИБЬЮЦИИ

**LICENSE**: CC BY-SA 4.0. Можно копировать, распространять, изменять при условии:
- **Атрибуция** — указать авторство (Heaven Refining Demon Venerable / Kimi, Mavis, petushokmaxorka-ai).
- **Share-alike** — производные работы под той же лицензией.

**Вклады приветствуются** через Pull Request. **Но** вклады должны следовать:
- Латинизированные имена файлов
- Печати по `PROOEMIUM.md` §II
- Структура досье по §III
- Сноски с ISBN/страницами

Владелец оставляет за собой право ✚ CREDO (т.е. личные печати) только в исключительных случаях.

---
*Sigillum: ARCHITECTURA VIVIT — NON IN LITTERIS, SED IN MENTE.*
