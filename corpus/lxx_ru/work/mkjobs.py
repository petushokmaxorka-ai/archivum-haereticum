#!/usr/bin/env python3
"""Write per-chapter Greek inputs (in/<slug>/<ch>.json) and job manifests
(jobs/<phase>-NN.json) of ~TARGET verses each, never splitting a chapter."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NAMES = {"bytie": "Бытие", "ishod": "Исход", "levit": "Левит", "chisla": "Числа", "vtor": "Второзаконие",
         "navin": "Иисус Навин", "sudi": "Книга Судей", "ruf": "Руфь", "carstv1": "1 Царств", "carstv2": "2 Царств",
         "carstv3": "3 Царств", "carstv4": "4 Царств", "par1": "1 Паралипоменон", "par2": "2 Паралипоменон",
         "ezdr1": "2 Ездра (греч. «1 Ездра»)", "ezdr": "1 Ездра", "neem": "Неемия", "esfir": "Есфирь",
         "iudif": "Иудифь", "tovit": "Товит", "makk1": "1 Маккавейская", "makk2": "2 Маккавейская",
         "makk3": "3 Маккавейская", "iov": "Иов", "psaltir": "Псалтирь", "mol_man": "Молитва Манассии",
         "pritchi": "Притчи Соломона", "ekkl": "Екклесиаст", "pesn": "Песнь песней",
         "prem": "Премудрость Соломона", "sir": "Премудрость Иисуса сына Сирахова", "isaia": "Исаия",
         "ieremia": "Иеремия", "plach": "Плач Иеремии", "posl_ier": "Послание Иеремии", "varuh": "Варух",
         "iezek": "Иезекииль", "daniil": "Даниил", "osia": "Осия", "ioil": "Иоиль", "amos": "Амос",
         "avdii": "Авдий", "iona": "Иона", "mihei": "Михей", "naum": "Наум", "avvakum": "Аввакум",
         "sofonia": "Софония", "aggei": "Аггей", "zaharia": "Захария", "malahia": "Малахия"}


def main(phase, slugs, target):
    os.makedirs(os.path.join(HERE, "jobs"), exist_ok=True)
    jobs, cur, n = [], [], 0
    for slug in slugs:
        g = json.load(open(os.path.join(ROOT, "greek", slug + ".json")))
        c = json.load(open(os.path.join(ROOT, "csl", slug + ".json")))
        os.makedirs(os.path.join(HERE, "in", slug), exist_ok=True)
        for ch in sorted(g, key=int):
            vs = sorted(g[ch], key=lambda v: int(v))
            aligned = ch in c and set(c[ch]) == set(g[ch])
            json.dump({"slug": slug, "book": NAMES[slug], "ch": ch,
                       "csl_aligned_by_number": aligned,
                       "verses": [{"v": v, "g": g[ch][v]} for v in vs]},
                      open(os.path.join(HERE, "in", slug, ch + ".json"), "w"), ensure_ascii=False, indent=1)
            if n and n + len(vs) > target * 1.25:
                jobs.append(cur)
                cur, n = [], 0
            cur.append({"slug": slug, "ch": ch, "verses": len(vs), "aligned": aligned})
            n += len(vs)
        if n >= target * 0.8:
            jobs.append(cur)
            cur, n = [], 0
    if cur:
        jobs.append(cur)
    for i, j in enumerate(jobs, 1):
        jid = "%s-%02d" % (phase, i)
        json.dump({"id": jid, "chapters": j, "verses": sum(x["verses"] for x in j)},
                  open(os.path.join(HERE, "jobs", jid + ".json"), "w"), ensure_ascii=False, indent=1)
        books = sorted({x["slug"] for x in j}, key=[x["slug"] for x in j].index)
        print(jid, sum(x["verses"] for x in j), "verses |", ", ".join(
            "%s %s-%s" % (b, [x["ch"] for x in j if x["slug"] == b][0], [x["ch"] for x in j if x["slug"] == b][-1])
            for b in books))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[3].split(","), int(sys.argv[2]))
