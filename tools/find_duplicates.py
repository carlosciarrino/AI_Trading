#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict

root = Path(".")

files = defaultdict(list)

for f in root.rglob("*.py"):
    if ".git" in f.parts:
        continue
    files[f.name].append(f)

print("=" * 60)
print("Duplicate Python Modules")
print("=" * 60)

duplicates = False

for name in sorted(files):
    if len(files[name]) > 1:
        duplicates = True
        print(f"\n{name}")
        for p in files[name]:
            print(f"   {p}")

if not duplicates:
    print("\nNo duplicate module names found.")

print("\nDone.")
