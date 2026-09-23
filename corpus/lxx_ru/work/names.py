#!/usr/bin/env python3
"""Index a book for the harmonisation pass.

usage: python3 names.py <slug> [--term GREEKSTEM]...
Without --term: every capitalised Greek word (proper names, divine titles)
with its occurrences, grouped by a normalised stem, plus the Russian text of
the first occurrences, so inconsistent renderings are easy to spot.
With --term: every verse whose Greek contains that stem (accent-insensitive),
Greek next to the current Russian (reviewed .rv.json, else draft .tr.json).
"""
import collections, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))


def strip(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def load(slug):
    rows = []
    d = os.path.join(HERE, "in", slug)
    for f in sorted(os.listdir(d), key=lambda x: int(x.split(".")[0])):
        ch = f.split(".")[0]
        g = json.load(open(os.path.join(d, f)))
        r = {}
        for st in ("rv", "tr"):
            p = os.path.join(HERE, "out", slug, "%s.%s.json" % (ch, st))
            if os.path.exists(p):
                r = {x["v"]: x["r"] for x in json.load(open(p))["verses"]}
                break
        for x in g["verses"]:
            rows.append((ch, x["v"], x["g"], r.get(x["v"], "")))
    return rows


def main():
    slug = sys.argv[1]
    terms = [a for i, a in enumerate(sys.argv) if i > 1 and sys.argv[i - 1] == "--term"]
    rows = load(slug)
    if terms:
        for t in terms:
            ts = strip(t)
            print("=== %s" % t)
            for ch, v, g, r in rows:
                if ts in strip(g):
                    print("%s:%s | %s\n      | %s" % (ch, v, g, r))
        return
    occ = collections.defaultdict(list)
    for ch, v, g, r in rows:
        for w in re.findall(r"[Ͱ-Ͽἀ-῿]+", g):
            if w[0].isupper():
                occ[strip(w)[:5]].append((w, ch, v))
    for stem, lst in sorted(occ.items(), key=lambda kv: -len(kv[1])):
        forms = sorted({w for w, _, _ in lst})
        refs = ", ".join("%s:%s" % (c, v) for _, c, v in lst[:12])
        print("%-8s x%-4d %s  [%s%s]" % (stem, len(lst), " / ".join(forms[:6]), refs, " …" if len(lst) > 12 else ""))


if __name__ == "__main__":
    main()
