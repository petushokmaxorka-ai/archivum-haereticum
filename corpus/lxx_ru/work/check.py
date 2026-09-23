#!/usr/bin/env python3
"""Validate a translated chapter file against its Greek input.

usage: python3 check.py out/<slug>/<ch>.tr.json [more files...]
       python3 check.py --all [tr|rv]     (every output file of that stage)
Exit code 0 = OK. Prints one line per problem.
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
GREEK = re.compile(r"[Ͱ-Ͽἀ-῿]")
CYR = re.compile(r"[А-Яа-яЁё]")
MARK = re.compile(r"\[(?:[a-z]|\.\d+)\]")


def load_csl(slug):
    p = os.path.join(HERE, "..", "csl", slug + ".json")
    return json.load(open(p)) if os.path.exists(p) else {}


def check(path):
    probs = []
    try:
        d = json.load(open(path))
    except Exception as e:  # noqa: BLE001
        return ["%s: not valid JSON: %s" % (path, e)]
    slug, ch = str(d.get("slug")), str(d.get("ch"))
    m = re.search(r"out/([^/]+)/([^/.]+)\.(tr|rv)\.json$", os.path.abspath(path))
    if m and (m.group(1), m.group(2)) != (slug, ch):
        return ["%s: file content is %s ch %s but the path says %s ch %s (wrong file written?)" % (
            path, slug, ch, m.group(1), m.group(2))]
    inp = os.path.join(HERE, "in", slug, ch + ".json")
    if not os.path.exists(inp):
        return ["%s: no input %s (slug/ch fields wrong?)" % (path, inp)]
    src = json.load(open(inp))
    want = [x["v"] for x in src["verses"]]
    got = [str(x.get("v")) for x in d.get("verses", [])]
    if got != want:
        miss = [v for v in want if v not in got]
        extra = [v for v in got if v not in want]
        probs.append("%s: verse list differs from input (missing %s, extra %s%s)" % (
            path, miss[:15], extra[:15], ", order differs" if not miss and not extra else ""))
    gmap = {x["v"]: x["g"] for x in src["verses"]}
    for x in d.get("verses", []):
        v, r = str(x.get("v")), (x.get("r") or "").strip()
        tag = "%s %s:%s" % (slug, ch, v)
        if not r:
            probs.append("%s: empty translation" % tag)
            continue
        if not CYR.search(r):
            probs.append("%s: no Cyrillic text" % tag)
        if GREEK.search(r):
            probs.append("%s: Greek letters left in translation" % tag)
        if re.match(r"^\s*\d+[\s.:]", r):
            probs.append("%s: translation starts with a verse number" % tag)
        g = gmap.get(v, "")
        gm, rm = MARK.findall(g), MARK.findall(r)
        if gm != rm:
            probs.append("%s: source markers %s not preserved in order (got %s)" % (tag, gm, rm))
        if g and len(g) > 40:
            ratio = len(r) / len(g)
            if ratio < 0.55 or ratio > 2.6:
                probs.append("%s: suspicious length ratio %.2f (omission or padding?)" % (tag, ratio))
        if r.count("[") != r.count("]"):
            probs.append("%s: unbalanced square brackets" % tag)
    cm = d.get("csl_map")
    if cm is not None:
        csl = load_csl(slug)
        seen = {}
        for gv, refs in cm.items():
            if gv not in gmap and gv != "_unmatched":
                probs.append("%s: csl_map key %s is not a Greek verse of %s:%s" % (path, gv, slug, ch))
            for ref in refs:
                m = re.match(r"^(\d+):(\d+)$", str(ref))
                if not m or m.group(2) not in csl.get(m.group(1), {}):
                    probs.append("%s: csl_map ref %r does not exist in Slavonic %s" % (path, ref, slug))
                    continue
                if ref in seen:
                    probs.append("%s: Slavonic %s assigned twice (%s and %s)" % (path, ref, seen[ref], gv))
                seen[ref] = gv
    return probs


def main():
    args = sys.argv[1:]
    if args and args[0] == "--all":
        stage = args[1] if len(args) > 1 else "tr"
        args = sorted(glob.glob(os.path.join(HERE, "out", "*", "*.%s.json" % stage)))
    allp = []
    for p in args:
        allp += check(p)
    for p in allp:
        print(p)
    print("OK" if not allp else "%d problem(s)" % len(allp))
    sys.exit(1 if allp else 0)


if __name__ == "__main__":
    main()
