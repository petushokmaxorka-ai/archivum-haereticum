#!/usr/bin/env python3
"""Проверка целостности корпуса: счётчики + sha256."""
import hashlib, sys

path = sys.argv[1] if len(sys.argv) > 1 else "quran_uthmani.txt"
expected = int(sys.argv[2]) if len(sys.argv) > 2 else 6236
h = hashlib.sha256()
with open(path, "rb") as f:
    for chunk in iter(lambda: f.read(65536), b""):
        h.update(chunk)
with open(path, encoding="utf-8") as f:
    lines = sum(1 for l in f.read().splitlines() if l.strip())
print(f"lines={lines} sha256={h.hexdigest()}")
assert lines == expected, f"FAIL: ожидалось {expected}, получено {lines}"
print("INTEGRITAS: OK")
