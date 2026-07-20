# INTEGRATIO — ВСТРОЙКА В ДАШБОРД HERETIC OS

**MANUFACTORUM · Datum: 020.M3**

---

### I. СООТВЕТСТВИЕ МОДУЛЕЙ

| Модуль Heretic OS | Источник данных Архива |
|---|---|
| PRINCIPIUM | `00-manuscriptum-principale/hypothesa-corporis.md` |
| CODEX | `01-eventus-babel/`, `03-rami-ecclesiae/` |
| LIBER | `02-libri-deperditi/` |
| INQUISITIO | `04-pantheones/`, `05-probatio/` (в т.ч. DAMNATA) |
| FORGE | `06-quaestiones-apertae/agenda.md` |
| CHRONICLE | `data/timeline.json` — готовая хронология с датами `781.M2` |
| NOOSPHERE | `data/corpus.json` — граф ветвей, стратегии, классификации |
| MACHINA | `mcp/server.py` — MCP-доступ агентов к Архиву |

### II. ПРЯМОЕ ЧТЕНИЕ (без сервера)

Репозиторий публичный — дашборд может тянуть файлы напрямую:

```
https://raw.githubusercontent.com/petushokmaxorka-ai/archivum-haereticum/main/data/corpus.json
https://raw.githubusercontent.com/petushokmaxorka-ai/archivum-haereticum/main/data/timeline.json
https://raw.githubusercontent.com/petushokmaxorka-ai/archivum-haereticum/main/data/pantheones.json
https://raw.githubusercontent.com/petushokmaxorka-ai/archivum-haereticum/main/README.md
```

### III. ПЕЧАТИ ДЛЯ UI

Поле `classificatio` в JSON и шапки досье: `FIDELIS` (зелёный/золотой), `SUSPECTUS` (янтарный), `DAMNATUS` (красный). Рекомендация: бейджи в стиле печатей — DAMNATA не скрывать, показывать с протоколом опровержения (это фишка Архива).

### IV. MCP-СЕРВЕР

`mcp/server.py` — FastMCP (stdio). Инструменты: `list_rami`, `get_ramus`, `get_timeline`, `get_pantheones`, `search_archivum`. Запуск:

```bash
pip install mcp
python mcp/server.py
```

Подключение в конфиг агента (claude-code / opencode / любой MCP-клиент):

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

### V. ДАТЫ

Имперский формат: `781.M2` = 781 год 2-го тысячелетия; `431.M1` = 431 год 1-го. В `timeline.json` оба поля (`datum_wh40k`, `anno`) — сортировка по `anno`.

---
*Sigillum: ARCHIVUM SERVIT COGITATORI.*