#!/usr/bin/env python3
"""
ARCHIVUM HAERETICUM — MCP-сервер Архива Империума Человечества.
Отдаёт агентам ветви, хронологию, пантеоны и досье из репозитория.

Запуск:  pip install mcp && python mcp/server.py  (stdio)
Данные:  ../data/*.json и досье ../  относительно этого файла.
"""

import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

mcp = FastMCP("archivum-haereticum")


def _load(name: str) -> dict:
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


@mcp.tool()
def list_rami() -> list[dict]:
    """Список ветвей корпуса: id, имя, стратегия, классификация, путь к досье."""
    corpus = _load("corpus.json")
    return [
        {
            "id": r["id"],
            "nomen": r["nomen"],
            "strategia": r.get("strategia"),
            "classificatio": r.get("classificatio"),
            "dossier": r.get("dossier"),
        }
        for r in corpus["rami"]
    ]


@mcp.tool()
def get_ramus(ramus_id: str) -> dict:
    """Полное досье ветви по id (aethiopia, armenia, ecclesia-orientis, slavia,
    hibernia, persia-mazda, bactria, al-andalus, islam-sunni, islam-shia,
    islam-ibadi, manichaea). Включает текст досье, если файл есть в архиве."""
    corpus = _load("corpus.json")
    for r in corpus["rami"]:
        if r["id"] == ramus_id:
            result = dict(r)
            dossier = r.get("dossier")
            if dossier:
                path = ROOT / dossier
                if path.exists():
                    result["textus"] = path.read_text(encoding="utf-8")
            return result
    return {"error": f"ramus '{ramus_id}' non inventus", "inventi": [r["id"] for r in corpus["rami"]]}


@mcp.tool()
def get_timeline() -> list[dict]:
    """Хронология корпуса: все события с имперскими датами и печатями достоверности."""
    return _load("timeline.json")["eventus"]


@mcp.tool()
def get_pantheones() -> dict:
    """Восемь пантеонов: органиграмма (Верховный, громовержец, знания, гиганты, потоп, судьба богов)."""
    return _load("pantheones.json")


@mcp.tool()
def search_archivum(query: str) -> list[dict]:
    """Полнотекстовый поиск по всем досье Архива (markdown). Возвращает файл и фрагменты с контекстом."""
    query_lower = query.lower()
    hits = []
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines()):
            if query_lower in line.lower():
                hits.append({"file": str(path.relative_to(ROOT)), "line": i + 1, "fragment": line.strip()[:300]})
        if len(hits) >= 50:
            break
    return hits[:50]


if __name__ == "__main__":
    mcp.run()
