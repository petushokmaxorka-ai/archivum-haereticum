#!/usr/bin/env python3
"""Assemble reader data files (kanon/data/<slug>.txt: gzip+base64 JSON) from
greek/, csl/ and the reviewed translations out/<slug>/<ch>.rv.json.

usage: python3 build.py <data_dir> slug [slug...]
Refuses to write a book unless every Greek verse has a reviewed translation.
"""
import base64, gzip, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from mkjobs import NAMES  # noqa: E402

EN = {"bytie": "Genesis", "ishod": "Exodus", "levit": "Leviticus", "chisla": "Numbers", "vtor": "Deuteronomy",
      "navin": "Joshua", "sudi": "Judges", "ruf": "Ruth", "carstv1": "1 Kingdoms", "carstv2": "2 Kingdoms",
      "carstv3": "3 Kingdoms", "carstv4": "4 Kingdoms", "par1": "1 Chronicles", "par2": "2 Chronicles",
      "ezdr1": "1 Esdras", "ezdr": "Ezra", "neem": "Nehemiah", "ezdr2": "4 Ezra", "esfir": "Esther",
      "iudif": "Judith", "tovit": "Tobit", "makk1": "1 Maccabees", "makk2": "2 Maccabees", "makk3": "3 Maccabees",
      "iov": "Job", "psaltir": "Psalms", "mol_man": "Prayer of Manasses", "pritchi": "Proverbs",
      "ekkl": "Ecclesiastes", "pesn": "Song of Songs", "prem": "Wisdom of Solomon", "sir": "Sirach",
      "isaia": "Isaiah", "ieremia": "Jeremiah", "plach": "Lamentations", "posl_ier": "Epistle of Jeremiah",
      "varuh": "Baruch", "iezek": "Ezekiel", "daniil": "Daniel", "osia": "Hosea", "ioil": "Joel", "amos": "Amos",
      "avdii": "Obadiah", "iona": "Jonah", "mihei": "Micah", "naum": "Nahum", "avvakum": "Habakkuk",
      "sofonia": "Zephaniah", "aggei": "Haggai", "zaharia": "Zechariah", "malahia": "Malachi"}

WARN = []
FINAL_HARD = re.compile(r"(?<=[бвгджзклмнпрстфхцчшщ])ъ(?=[\s,.;:!?)»\]]|$)")


def csl_clean(t):
    return FINAL_HARD.sub("", t).strip()


def key(ch, v):
    return "%s:%s" % (ch, v)


def order(k):
    a, b = k.split(":")
    return (int(a), int(b))


def build_from_csl(slug):
    """3 Ezra: no Greek survives; rows follow the Slavonic, translated from it."""
    csl = json.load(open(os.path.join(ROOT, "csl", slug + ".json")))
    rows, missing = {}, []
    for ch in sorted(csl, key=int):
        p = os.path.join(HERE, "out", slug, ch + ".rv.json")
        tr = {str(x["v"]): x["r"].strip() for x in json.load(open(p))["verses"]} if os.path.exists(p) else {}
        for v in sorted(csl[ch], key=int):
            if not tr.get(v):
                missing.append(key(ch, v))
            rows[key(ch, v)] = {"c": csl_clean(csl[ch][v]), "r": tr.get(v, "")}
    if missing:
        raise SystemExit("%s: untranslated verses: %s" % (slug, missing[:20]))
    return {"slug": slug, "ru": NAMES.get(slug, "3 Ездра (апокалипсис)"), "csl_name": EN[slug], "rus_src": "АРХИВ",
            "shifts": {}, "extras": [], "verses": {k: rows[k] for k in sorted(rows, key=order)}}


def build(slug):
    if slug == "ezdr2":
        return build_from_csl(slug)
    g = json.load(open(os.path.join(ROOT, "greek", slug + ".json")))
    csl = json.load(open(os.path.join(ROOT, "csl", slug + ".json")))
    rows, used, maps = {}, set(), {}
    missing, owner = [], {}
    for ch in sorted(g, key=int):
        p = os.path.join(HERE, "out", slug, ch + ".rv.json")
        if not os.path.exists(p):
            missing.append(ch)
            continue
        d = json.load(open(p))
        tr = {str(x["v"]): x["r"].strip() for x in d["verses"]}
        cm = d.get("csl_map")
        if cm is None:  # aligned by number
            cm = {v: ["%s:%s" % (ch, v)] for v in g[ch] if v in csl.get(ch, {})}
        for v in sorted(g[ch], key=int):
            if not tr.get(v):
                missing.append("%s:%s" % (ch, v))
            rows[key(ch, v)] = {"g": g[ch][v], "r": tr.get(v, "")}
            maps[key(ch, v)] = [r for r in cm.get(v, [])]
    if missing:
        raise SystemExit("%s: untranslated chapters/verses: %s" % (slug, missing[:20]))
    # Slavonic text per row; prefix the Slavonic reference when it differs
    for k, refs in maps.items():
        parts = []
        for ref in refs:
            ch, v = ref.split(":")
            t = csl.get(ch, {}).get(v)
            if t is None:
                WARN.append("%s: row %s maps to missing Slavonic %s" % (slug, k, ref))
                continue
            if ref in used:
                WARN.append("%s: Slavonic %s mapped twice (%s and %s); kept on %s" % (slug, ref, owner[ref], k, owner[ref]))
                continue
            used.add(ref)
            owner[ref] = k
            parts.append(csl_clean(t) if ref == k else "[%s] %s" % (ref, csl_clean(t)))
        if parts:
            rows[k]["c"] = " ".join(parts)
    # Slavonic verses with no Greek counterpart: attach after the previous row
    allc = sorted((key(ch, v) for ch in csl for v in csl[ch]), key=order)
    rk = sorted(rows, key=order)
    for ref in allc:
        if ref in used:
            continue
        prev = [k for k in rk if order(k) <= order(ref)]
        tgt = prev[-1] if prev else rk[0]
        ch, v = ref.split(":")
        add = "[%s] %s" % (ref, csl_clean(csl[ch][v]))
        rows[tgt]["c"] = (rows[tgt].get("c", "") + " " + add).strip()
        used.add(ref)
    return {"slug": slug, "ru": NAMES[slug], "csl_name": EN[slug], "rus_src": "АРХИВ",
            "shifts": {}, "extras": [], "verses": {k: rows[k] for k in sorted(rows, key=order)}}


def write(data, path):
    raw = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode()
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as f:
        f.write(raw)
    b = base64.b64encode(buf.getvalue()).decode()
    open(path, "w").write("\n".join(b[i:i + 76] for i in range(0, len(b), 76)) + "\n")


def main():
    out = sys.argv[1]
    for slug in sys.argv[2:]:
        d = build(slug)
        write(d, os.path.join(out, slug + ".txt"))
        vs = d["verses"].values()
        print("%-8s rows=%d g=%d c=%d r=%d" % (slug, len(d["verses"]), sum(1 for x in vs if x.get("g")),
                                              sum(1 for x in vs if x.get("c")), sum(1 for x in vs if x.get("r"))))
    for w in WARN:
        print("WARN", w)


if __name__ == "__main__":
    main()
