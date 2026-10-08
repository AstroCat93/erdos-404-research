"""Cross-check Theorem F (general K) against an independently computed landscape table
(sibling agent B's CSV: p,a,v_p(a!),status,value,detail ; value = g = f - v_p(a!) when EXACT).
Read-only use of that file as data.
usage: python3 crosscheck_landscape.py <csv> p Kmax
"""
import csv, sys
from core import tauK, vp

path, p, Kmax = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
TAU = {K: tauK(K, p) for K in range(3, Kmax + 1)}
rows = list(csv.DictReader(open(path)))
agree = disagree = explained_exact = unexplained_exact = 0
unexpl = []
for row in rows:
    a = int(row["a"]); st = row["status"]; val = int(row["value"])
    preds = set()
    for K, (t, z) in TAU.items():
        if z:
            continue
        if vp(a + K, p) > t:
            preds.add(t)
    if (a + 1) % p == 0:
        preds.add(0)
    if len(preds) > 1:
        print("INTERNAL INCONSISTENCY a=%d preds=%s" % (a, preds))
    if preds:
        g = preds.pop()
        if st in ("EXACT", "BLOCKED") and val == g:
            agree += 1
        else:
            disagree += 1
            print("DISAGREE a=%d theorem g=%d table=%s %d" % (a, g, st, val))
    else:
        if st == "EXACT":
            unexplained_exact += 1
            unexpl.append((a, val))
print("p=%d rows=%d theorem-covered agree=%d disagree=%d ; EXACT rows not covered (K<=%d): %d"
      % (p, len(rows), agree, disagree, Kmax, unexplained_exact))
print("first uncovered EXACT (a,g):", unexpl[:25])
