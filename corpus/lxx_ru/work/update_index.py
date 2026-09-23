#!/usr/bin/env python3
"""Refresh the book cards and the summary line of olp-vethozaveta/index.html
from the data files actually present in kanon/data.

usage: python3 update_index.py <olp-vethozaveta dir>
"""
import base64, gzip, json, os, re, sys

TITLES = {"Винокуров": "интерлиняр А. Винокурова", "Юнгеров": "пер. П. А. Юнгерова",
          "АРХИВ": "перевод Архива с греческого LXX"}
BADGES = {"Винокуров": "ВИН", "Юнгеров": "ЮНГ", "АРХИВ": "◆ АРХИВ"}


def load(datadir, slug):
    parts, i = [], 0
    while os.path.exists(os.path.join(datadir, slug, "%02d.txt" % i)):
        parts.append(open(os.path.join(datadir, slug, "%02d.txt" % i)).read())
        i += 1
    if not parts:
        p = os.path.join(datadir, slug + ".txt")
        if not os.path.exists(p):
            return None
        parts = [open(p).read()]
    t = re.sub(r"\s+", "", "".join(parts))
    return json.loads(gzip.decompress(base64.b64decode(t)))


def main():
    root = sys.argv[1]
    datadir = os.path.join(root, "kanon", "data")
    idx = os.path.join(root, "index.html")
    s = open(idx, encoding="utf-8").read()
    tot = gtot = rtot = rbooks = nbooks = 0

    def card(m):
        nonlocal tot, gtot, rtot, rbooks, nbooks
        slug, name = m.group(1), m.group(2)
        nbooks += 1
        d = load(datadir, slug)
        if d is None:
            return m.group(0)
        vs = list(d["verses"].values())
        n, ng, nr = len(vs), sum(1 for v in vs if v.get("g")), sum(1 for v in vs if v.get("r"))
        tot, gtot, rtot = tot + n, gtot + ng, rtot + nr
        src = d.get("rus_src") or "АРХИВ"
        if nr:
            rbooks += 1
        title = TITLES.get(src, src)
        if slug == "ezdr2" and src == "АРХИВ":
            title = "перевод Архива со славянской редакции 1751 (греческий не сохранился)"
        prog = "" if nr else ' <span class="prog">· рус. слой готовится</span>'
        return ("<a class='bk' href='kanon/?b=%s'><span class='bn'>%s</span><span class='bc'>%d ст. · ΓΡ %d · РУ %d</span>"
                "<span class='bt' title='%s'>%s</span>%s</a>" % (slug, name, n, ng, nr, title, BADGES.get(src, src), prog))

    s = re.sub(r"<a class='bk' href='kanon/\?b=([^']+)'><span class='bn'>([^<]+)</span>.*?</a>", card, s)
    s = re.sub(r"Итого: <b>\d+ стихов хребта</b> · греческий слой \d+ стихов · русский слой \d+ стихов · "
               r"книг с готовым русским слоем: \d+ из \d+",
               "Итого: <b>%d стихов хребта</b> · греческий слой %d стихов · русский слой %d стихов · "
               "книг с готовым русским слоем: %d из %d" % (tot, gtot, rtot, rbooks, nbooks), s)
    open(idx, "w", encoding="utf-8").write(s)
    print("books=%d with data; verses=%d greek=%d russian=%d; books with Russian=%d/%d"
          % (sum(1 for _ in re.finditer(r"class='bk'", s)), tot, gtot, rtot, rbooks, nbooks))


if __name__ == "__main__":
    main()
