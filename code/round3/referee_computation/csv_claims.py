#!/usr/bin/env python3
"""Round-3 computational referee: re-derive the table-level claims of note §11.1 (Theorem 11.4 and the
paragraphs after it) from the shipped survey CSVs, with 594 and 17662 set to the exact values of
Theorem 11.2.  Pure bookkeeping on the data; no solver involved."""
import csv, sys


def V(n):
    return n - bin(n).count("1")


rows = {}
for fn in sys.argv[1:]:
    with open(fn) as fh:
        for r in csv.DictReader(fh):
            a, f, st = int(r["a"]), int(r["f"]), r["status"]
            if st == "exact":
                rows[a] = f
rows[594] = 90394
rows[17662] = 221465
even = [a for a in range(2, 32769, 2)]
missing = [a for a in even if a not in rows]
print("even a <= 32768:", len(even), " with exact value:", sum(a in rows for a in even), " missing:", missing[:10])
g = {a: rows[a] - V(a) for a in even}
vals = set(g.values())
print("g takes any of 1,2,4,5:", sorted(vals & {1, 2, 4, 5}))
bad3 = [a for a in even if (g[a] == 3) != (a % 8 == 4)]
print("g=3 <=> a=4 mod 8 violations:", bad3[:10], len(bad3))
top = sorted(even, key=lambda a: -g[a])[:12]
print("largest excesses:", ", ".join("%d:%d" % (a, g[a]) for a in top))
top4096 = sorted([a for a in even if a <= 4096], key=lambda a: -g[a])[:11]
print("largest, a<=4096:", ", ".join("%d:%d" % (a, g[a]) for a in top4096))
top16384 = sorted([a for a in even if a <= 16384], key=lambda a: -g[a])[:3]
print("largest, a<=16384:", ", ".join("%d:%d" % (a, g[a]) for a in top16384))
print("survival law G * #{even a: g >= G} / 16384:")
G = 256
while G <= 131072:
    c = sum(1 for a in even if g[a] >= G)
    print("  G=%6d  count=%4d  G*count/16384=%.3f" % (G, c, G * c / 16384))
    G *= 2
for a in (16382, 32766):
    print("shadow a=%d: f=%d g=%d" % (a, rows[a], g[a]))
