#!/usr/bin/env python3
"""Per-job progress: chapters with .tr.json / .rv.json out of total."""
import glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
pref = sys.argv[1] if len(sys.argv) > 1 else ""
T = {"tr": 0, "rv": 0, "all": 0}
for f in sorted(glob.glob(os.path.join(HERE, "jobs", pref + "*.json"))):
    j = json.load(open(f))
    n = len(j["chapters"])
    tr = sum(os.path.exists(os.path.join(HERE, "out", c["slug"], c["ch"] + ".tr.json")) for c in j["chapters"])
    rv = sum(os.path.exists(os.path.join(HERE, "out", c["slug"], c["ch"] + ".rv.json")) for c in j["chapters"])
    vt = sum(c["verses"] for c in j["chapters"] if os.path.exists(os.path.join(HERE, "out", c["slug"], c["ch"] + ".tr.json")))
    T["tr"] += vt; T["all"] += j["verses"]
    T["rv"] += sum(c["verses"] for c in j["chapters"] if os.path.exists(os.path.join(HERE, "out", c["slug"], c["ch"] + ".rv.json")))
    print("%s  tr %2d/%2d  rv %2d/%2d  (%d/%d verses translated)" % (j["id"], tr, n, rv, n, vt, j["verses"]))
print("TOTAL verses: translated %d, reviewed %d, of %d" % (T["tr"], T["rv"], T["all"]))
