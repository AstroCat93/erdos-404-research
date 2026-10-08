"""Gap theorem check against sibling landscape CSV (read-only data).
p odd, a = p*m0 + (p-k), j = v_p(m0+1), L = L_p (Sigma(E_p) covers Z/p^L):
  tau(k,p) <= j  =>  g = tau(k,p)
  tau(k,p) >  j  =>  g >= e_{m*} - e_{m0} + L,  m* = min{m > m0 : v_p(m+1) >= L}
usage: python3 crosscheck_gap.py csv p L
"""
import csv, sys
from core import tau, vp, e_block

path, p, L = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
T = {k: (tau(k, p)[0] if k != 2 else 10 ** 9) for k in range(1, p + 1)}
ok = bad = 0
for row in csv.DictReader(open(path)):
    a = int(row["a"]); st = row["status"]; g = int(row["value"])
    m0, r = divmod(a, p); k = p - r
    j = vp(m0 + 1, p)
    if T[k] <= j:
        good = st in ("EXACT", "BLOCKED") and g == T[k]
    else:
        m = m0 + 1
        while vp(m + 1, p) < L:
            m += 1
        lb = e_block(m, p) - e_block(m0, p) + L
        good = (st == "GE" and g >= min(lb, g)) or (st == "EXACT" and g >= lb)
        if st == "GE" and g < lb:
            good = True  # table only certifies a smaller lower bound; not a contradiction
        if st == "EXACT" and g < lb:
            good = False
    if good:
        ok += 1
    else:
        bad += 1
        print("VIOLATION a=%d k=%d j=%d tau=%d status=%s g=%d" % (a, k, j, T[k], st, g))
print("p=%d L=%d rows ok=%d violations=%d" % (p, L, ok, bad))
