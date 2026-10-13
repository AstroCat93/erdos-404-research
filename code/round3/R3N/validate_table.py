#!/usr/bin/env python3
"""Validate programs dfsW (C) and dfsB (B) against K. Kitamura's exact table f(a,2), a <= 256.

For every even a in the table, each program is run with K = f (expect reachable=1) and
K = f+1 (expect reachable=0 and EXACT f printed equal to the table value).
Usage: python3 -I validate_table.py TABLE.csv BIN_DIR
"""
import csv
import subprocess
import sys

table, bindir = sys.argv[1], sys.argv[2]
rows = []
with open(table) as fh:
    for r in csv.DictReader(fh):
        a, f = int(r['a']), int(r['value'])
        if a % 2 == 0:
            rows.append((a, f))
bad = 0
for prog in ('dfsW', 'dfsB'):
    for a, f in rows:
        for K, want in ((f, 1), (f + 1, 0)):
            out = subprocess.run([f"{bindir}/{prog}", str(a), str(K)], capture_output=True, text=True).stdout
            res = [l for l in out.splitlines() if l.startswith('RESULT')]
            ex = [l for l in out.splitlines() if l.startswith('EXACT')]
            got = None
            if res:
                got = 1 if 'reachable=1' in res[0] else 0
            okx = True
            if want == 0:
                okx = bool(ex) and f" f={f} " in ex[0] + " "
            if got != want or not okx:
                bad += 1
                print(f"MISMATCH {prog} a={a} K={K} want={want} got={got} {ex}")
    print(f"{prog}: checked {len(rows)} even a, 2 runs each", flush=True)
print("ALL_OK" if bad == 0 else f"FAILURES={bad}")
