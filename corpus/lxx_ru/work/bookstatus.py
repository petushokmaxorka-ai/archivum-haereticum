#!/usr/bin/env python3
"""Per book: chapters with tr / rv, and whether harmonised (H: entries)."""
import glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
for d in sorted(os.listdir(os.path.join(HERE, "in"))):
    chs = [f.split(".")[0] for f in os.listdir(os.path.join(HERE, "in", d))]
    tr = sum(os.path.exists(os.path.join(HERE, "out", d, c + ".tr.json")) for c in chs)
    rv = sum(os.path.exists(os.path.join(HERE, "out", d, c + ".rv.json")) for c in chs)
    hz = os.path.exists(os.path.join(HERE, "out", d, "_harmonized"))
    print("%-9s ch=%3d tr=%3d rv=%3d %s" % (d, len(chs), tr, rv, "HARMONIZED" if hz else ("READY" if rv == len(chs) else "")))
