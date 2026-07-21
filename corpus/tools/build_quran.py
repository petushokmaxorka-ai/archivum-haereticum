#!/usr/bin/env python3
"""
CORPUS DIVINUS - сборщик Корана.
Вход: текст Tanzil (формат "surah|ayah|текст" или один аят на строку, Uthmani, Public Domain).
Выход:
  corpus/data/quran/ar-quran-uthmani.jsonl   - машиночитаемый корпус
  site/index.html                            - оглавление
  site/quran/NNN.html                        - 114 страниц: слева оригинал (RTL), справа перевод
RU-слой: файл того же формата через --ru (напр., Крачковский, PD с 2022).
Запуск: python3 corpus/tools/build_quran.py --src quran_uthmani.txt [--ru ru.txt] [--out .]
"""
import argparse, html, json, os

SURAH_RU = {1: "Аль-Фатиха (Открывающая)", 2: "Аль-Бакара (Корова)", 3: "Ал Имран", 4: "Ан-Ниса (Женщины)", 5: "Аль-Маида (Трапеза)", 19: "Марьям", 71: "Нух (Ной)", 89: "Аль-Фаджр (Заря)"}

CSS = ":root{--bg:#0a0a0c;--bg2:#101014;--panel:#15151a;--line:#2a2a33;--red:#c8102e;--gold:#c9a227;--ink:#e8e2d5;--dim:#9a937f;--orig:#f2ead6}*{box-sizing:border-box;margin:0;padding:0}body{background:var(--bg);color:var(--ink);font-family:Georgia,serif;line-height:1.55}header.b{background:linear-gradient(180deg,#1a0007,#0a0a0c);border-bottom:3px solid var(--red);padding:1.6rem 1rem;text-align:center}header.b h1{font-size:1.4rem;letter-spacing:.15em;color:var(--orig)}header.b p{color:var(--gold);font-size:.75rem;letter-spacing:.25em;text-transform:uppercase}main{max-width:1150px;margin:0 auto;padding:1.2rem 1rem 3rem}.row{display:grid;grid-template-columns:3rem 1fr 1.1fr;border-bottom:1px solid #1d1d24;align-items:start}.num{grid-column:1;color:var(--dim);font-size:.75rem;padding:.7rem .5rem;text-align:right;align-self:start}.ru{grid-column:2;padding:.7rem .9rem;font-size:.97rem}.ar{grid-column:3;direction:rtl;text-align:right;font-family:'Amiri','Scheherazade New','Traditional Arabic',serif;font-size:1.35rem;line-height:1.9;color:var(--orig);padding:.7rem .9rem;border-left:1px solid #1d1d24}.meta{color:var(--dim);font-size:.78rem;font-style:italic;padding:.6rem 0}nav{padding:.6rem;text-align:center}nav a{color:var(--gold);font-size:.8rem;margin:0 .6rem}a{color:var(--gold)}@media(max-width:760px){.row{grid-template-columns:2rem 1fr 1.1fr}.num{font-size:.7rem;padding:.5rem .3rem}.ru{font-size:.88rem;padding:.55rem .5rem;line-height:1.45}.ar{font-size:1.15rem;line-height:1.75;padding:.55rem .5rem}}@media(max-width:420px){.row{grid-template-columns:1.7rem 1fr 1fr}.num{font-size:.62rem;padding:.4rem .2rem}.ru{font-size:.78rem;padding:.4rem .35rem;line-height:1.35}.ar{font-size:.95rem;line-height:1.6;padding:.4rem .35rem}}"

AYAH_COUNTS = [7,286,200,176,120,165,206,75,129,109,123,111,43,52,99,128,111,110,98,135,112,78,118,64,77,227,93,88,69,60,34,30,73,54,45,83,182,88,75,85,54,53,89,59,37,35,38,29,18,45,60,49,62,55,78,96,29,22,24,13,14,11,11,18,12,12,30,52,52,44,28,28,20,56,40,31,50,40,46,42,29,19,36,25,22,17,19,26,30,20,15,21,11,8,8,19,5,8,8,11,11,8,3,9,5,4,7,3,6,3,5,4,5,6]

def read_plain(path):
    with open(path, encoding="utf-8") as f:
        lines = [l.strip() for l in f.read().splitlines() if l.strip() and not l.startswith("#")]
    assert sum(AYAH_COUNTS) == 6236, "таблица нумерации повреждена"
    assert len(lines) == 6236, f"ожидалось 6236 аятов, получено {len(lines)}"
    rows, i = [], 0
    for s, cnt in enumerate(AYAH_COUNTS, start=1):
        for n in range(1, cnt + 1):
            rows.append((s, n, lines[i])); i += 1
    return rows

def read_tanzil(path):
    with open(path, encoding="utf-8") as f:
        head = f.read(4000)
    first = head.splitlines()[0] if head.splitlines() else ""
    if "|" in first:
        rows = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                s, a, t = line.split("|", 2)
                rows.append((int(s), int(a), t))
        return rows
    return read_plain(path)

def page(title, sub, body, extra=""):
    return ('<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(title)} · Corpus Divinus</title><style>{CSS}</style></head>'
            f'<body><header class="b"><h1>{html.escape(title)}</h1><p>{html.escape(sub)}</p></header>'
            f'<nav><a href="../index.html">✠ Оглавление Корана</a>{extra}</nav><main>{body}</main></body></html>')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--ru")
    ap.add_argument("--out", default=".")
    ap.add_argument("--surah", type=int)
    a = ap.parse_args()

    rows = read_tanzil(a.src)
    ru = {}
    if a.ru:
        for s, n, t in read_tanzil(a.ru):
            ru[(s, n)] = t

    data_dir = os.path.join(a.out, "corpus", "data", "quran")
    site_dir = os.path.join(a.out, "site", "quran")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(site_dir, exist_ok=True)

    with open(os.path.join(data_dir, "ar-quran-uthmani.jsonl"), "w", encoding="utf-8") as f:
        for s, n, t in rows:
            rec = {"corpus": "quran", "book": s, "chapter": s, "verse": n,
                   "original": t, "orig_lang": "ar", "ru": ru.get((s, n)),
                   "fons_orig": "Tanzil Uthmani (Public Domain)",
                   "fons_ru": "Крачковский И.Ю. (PD с 2022)" if ru else None,
                   "stamp": "FIDELIS"}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    by_s = {}
    for s, n, t in rows:
        by_s.setdefault(s, []).append((n, t))

    targets = [a.surah] if a.surah else sorted(by_s)
    links = [f'<a href="quran/{s:03d}.html">{s}. {SURAH_RU.get(s, "Сура " + str(s))}</a>' for s in sorted(by_s)]

    for s in targets:
        body = ['<div class="meta">Оригинал: Tanzil Uthmani (PD) · Перевод: ' + ("Крачковский И.Ю. (PD)" if ru else "RU-слой: фаза Q1b") + " · Печать: ◆ FIDELIS</div>"]
        for n, t in by_s[s]:
            body.append(f'<div class="row"><span class="num">{s}:{n}</span><div class="ar" lang="ar">{html.escape(t)}</div><div class="ru">{html.escape(ru.get((s, n), "—"))}</div></div>')
        prev_l = f'<a href="{s-1:03d}.html">← {s-1}</a>' if s > 1 else ""
        next_l = f'<a href="{s+1:03d}.html">{s+1} →</a>' if s < 114 else ""
        name = SURAH_RU.get(s, f"Сура {s}")
        with open(os.path.join(site_dir, f"{s:03d}.html"), "w", encoding="utf-8") as f:
            f.write(page(f"Сура {s} · {name}", "CORPUS DIVINUS · AL-QUR'AN", "\n".join(body), prev_l + next_l))

    idx_body = ['<div class="meta">CORPUS DIVINUS · Коран: 114 сур, 6236 аятов. Оригинал слева, перевод справа.</div>', '<div style="column-width:280px;column-gap:2rem">']
    idx_body += [f"<p style='margin:.25rem 0'>{l}</p>" for l in links]
    idx_body.append("</div>")
    with open(os.path.join(a.out, "site", "index.html"), "w", encoding="utf-8") as f:
        f.write(page("CORPUS DIVINUS · AL-QUR'AN", "Единый свод · Коран · оригинал + дословный перевод", "\n".join(idx_body)))

    print(f"OK: аятов={len(rows)} сур={len(by_s)} страниц={len(targets)} ru={'да' if ru else 'нет'}")

if __name__ == "__main__":
    main()
