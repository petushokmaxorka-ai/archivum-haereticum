#!/usr/bin/env python3
"""Parse Rahlfs LXX (MyBible CSV) and the 1751 Slavonic (my-bible.info, civil
script) into per-book JSON: greek/<slug>.json and csl/<slug>.json, each
{"<ch>": {"<v>": text}}."""
import html, json, os, re, collections

HERE = os.path.dirname(os.path.abspath(__file__))

# reader slug -> (MyBible book number(s), Slavonic page)
BOOKS = [
    ("bytie", [10], "bytie"), ("ishod", [20], "ishod"), ("levit", [30], "levit"),
    ("chisla", [40], "chisla"), ("vtor", [50], "vtorozak"), ("navin", [60], "iisus_nav"),
    ("sudi", [70], "sudej"), ("ruf", [80], "ruf"), ("carstv1", [90], "1tsarstv"),
    ("carstv2", [100], "2tsarstv"), ("carstv3", [110], "3tsarstv"), ("carstv4", [120], "4tsarstv"),
    ("par1", [130], "1paralip"), ("par2", [140], "2paralip"), ("ezdr1", [165], "2ezdr"),
    ("ezdr", [150], "1ezdr"), ("neem", [160], "neemii"), ("ezdr2", [], "3ezdr"),
    ("esfir", [190], "esfir"), ("iudif", [180], "iudif"), ("tovit", [170], "tovit"),
    ("makk1", [462], "1makkav"), ("makk2", [464], "2makkav"), ("makk3", [466], "3makkav"),
    ("iov", [220], "iov"), ("psaltir", [230], "psaltir"), ("mol_man", [], None),
    ("pritchi", [240], "prit_solom"), ("ekkl", [250], "ekkles"), ("pesn", [260], "pesn_solom"),
    ("prem", [270], "prem_solom"), ("sir", [280], "prem_sirah"), ("isaia", [290], "pr_isaija"),
    ("ieremia", [300], "pr_ieremija"), ("plach", [310], "plach_ieremii"),
    ("posl_ier", [315], "posl_ieremii"), ("varuh", [320], "pr_varuh"),
    ("iezek", [330], "pr_iezekiil"), ("daniil", [340], "pr_daniil"), ("osia", [350], "pr_osija"),
    ("ioil", [360], "pr_ioil"), ("amos", [370], "pr_amos"), ("avdii", [380], "pr_avdij"),
    ("iona", [390], "pr_iona"), ("mihei", [400], "pr_mihej"), ("naum", [410], "pr_naum"),
    ("avvakum", [420], "pr_avvakum"), ("sofonia", [430], "pr_sofonija"), ("aggei", [440], "pr_aggej"),
    ("zaharia", [450], "pr_zaharija"), ("malahia", [460], "pr_malahija"),
]


def clean_greek(t):
    t = re.sub(r"<S>.*?</S>|<m>.*?</m>", "", t)
    t = re.sub(r"<[^>]+>", "", t)
    return re.sub(r"\s+", " ", t).strip()


def load_greek():
    by = collections.defaultdict(lambda: collections.defaultdict(dict))
    for line in open(os.path.join(HERE, "LXX_final_main.csv"), encoding="utf-8"):
        p = line.rstrip("\n").split("\t")
        if len(p) < 4:
            continue
        b, c, v, t = int(p[0]), p[1], p[2], clean_greek(p[3])
        by[b][c][v] = t
    return by


def load_ccat(name):
    """CCAT morph file (betacode, one word per line) -> {ch: {v: unicode text}}."""
    import betacode.conv as bc
    out, cur = {}, None
    for line in open(os.path.join(HERE, "ccat", name + ".mlxx"), encoding="latin-1"):
        line = line.rstrip("\n")
        m = re.match(r"^[A-Za-z0-9]+\s+(?:(\d+):)?(\d+)\s*$", line)
        if m:
            cur = out.setdefault(m.group(1) or "1", {}).setdefault(m.group(2), [])
            continue
        if cur is None or not line.strip():
            continue
        w = line.split()[0]
        cur.append(bc.beta_to_uni(w))
    return {c: {v: " ".join(ws) for v, ws in vs.items()} for c, vs in out.items()}


def parse_csl(name):
    raw = open(os.path.join(HERE, "csl_html", name + ".html"), encoding="utf-8", errors="replace").read()
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", "", raw, flags=re.S)
    # the text runs from the first chapter heading to the "error report" footer
    start = re.search(r'<p align="center">(?:<a name="g?\d+"[^>]*>\s*</a>)?\s*(?:Глав[аa]|Псалом)\s*\d+', raw)
    raw = raw[start.start():] if start else raw
    raw = re.split(r"Заметили ошибку", raw)[0]
    parts = re.split(r'<p align="center">(?:<a name="g?\d+"[^>]*>\s*</a>)?\s*(?:Глав[аa]|Псалом)\s*(\d+)\.?\s*</p>', raw)
    out = {}
    for i in range(1, len(parts), 2):
        ch = str(int(parts[i]))
        body = parts[i + 1]
        body = re.sub(r"<br\s*/?>", "\n", body)
        body = re.sub(r"</p>", "\n", body)
        body = html.unescape(re.sub(r"<[^>]+>", "", body))
        verses = {}
        cur = None
        for ln in body.split("\n"):
            ln = ln.strip().replace("\xa0", " ")
            if not ln:
                continue
            if re.match(r"^(НАВЕРХ|<<<|>>>|Конец\s+книз)", ln, flags=re.I):
                cur = None
                continue
            m = re.match(r"^(\d+)\.?\s+(.*)$", ln)
            if m:
                cur = m.group(1)
                verses[cur] = m.group(2).strip()
            elif cur is not None:
                verses[cur] += " " + ln
        for k in list(verses):
            v = re.sub(r"\s+", " ", verses[k]).strip()
            v = re.split(r"\s*Конец\s+книз", v)[0].strip()
            verses[k] = v
        if verses:
            out[ch] = verses
    return out


def main():
    g = load_greek()
    os.makedirs(os.path.join(HERE, "greek"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "csl"), exist_ok=True)
    report = []
    for slug, nums, csl in BOOKS:
        gb = {}
        for n in nums:
            for c, vs in g[n].items():
                gb.setdefault(c, {}).update(vs)
        if slug == "daniil":
            # Theodotion, the text the Church (and the Slavonic 1751) reads;
            # Susanna -> ch 13, Bel and the Dragon -> ch 14 as in the Slavonic.
            gb = load_ccat("62.DanielTh")
            gb["13"] = load_ccat("64.SusTh")["1"]
            gb["14"] = load_ccat("60.BelTh")["1"]
        if slug == "mol_man":
            gb = {"1": dict(g[800]["12"])}
        cb = parse_csl(csl) if csl else {}
        if slug == "par2" and "0" in cb.get("36", {}):
            cb["36"].pop("0")  # Prayer of Manasseh is its own book in the reader
        if slug == "mol_man":
            blob = parse_csl("2paralip")["36"]["0"]
            segs = re.split(r"\s*\((\d+)\)\s*", blob)
            cb = {"1": {"0": segs[0]}}
            for i in range(1, len(segs), 2):
                cb["1"][segs[i]] = segs[i + 1]
        json.dump(gb, open(os.path.join(HERE, "greek", slug + ".json"), "w"), ensure_ascii=False, indent=0)
        if slug == "psaltir" and "151" not in cb:  # Ps 151 has no verse numbers on the source page
            cb["151"] = json.load(open(os.path.join(HERE, "csl_ps151.json")))
        json.dump(cb, open(os.path.join(HERE, "csl", slug + ".json"), "w"), ensure_ascii=False, indent=0)
        ng = sum(len(v) for v in gb.values())
        nc = sum(len(v) for v in cb.values())
        same = sum(1 for c in gb if c in cb and set(gb[c]) == set(cb[c]))
        report.append((slug, len(gb), ng, len(cb), nc, same))
    for r in report:
        print("%-9s G ch=%3d v=%5d | C ch=%3d v=%5d | chapters with identical verse sets: %d" % r)


if __name__ == "__main__":
    main()
