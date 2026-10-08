"""Theorem F at p = 2: exact g(a,2) = tau(K,2) on the class a == -K (mod 2^{tau+1}), even K >= 4.
Also the union density of these classes among all a (inclusion-exclusion done exactly mod 2^M)."""
from core import tauK_mitm
rows = []
for K in range(4, 35, 2):
    t, z = tauK_mitm(K, 2, 130)
    assert not z
    rows.append((K, t))
    print("K=%2d tau(K,2)=%3d  class a == %d (mod 2^%d)" % (K, t, (-K) % (2 ** (t + 1)), t + 1), flush=True)
M = 24
covered = bytearray(2 ** M)
for K, t in rows:
    if t + 1 > M:
        continue
    q = 2 ** (t + 1)
    r = (-K) % q
    for a in range(r, 2 ** M, q):
        covered[a] = 1
dens_even = sum(covered[0::2]) / 2 ** (M - 1)
print("fraction of even a covered (classes with tau+1 <= %d): %.6f" % (M, dens_even))
# consistency: overlapping classes must have equal tau
for i, (K, t) in enumerate(rows):
    for K2, t2 in rows[i + 1:]:
        m = min(t, t2) + 1
        if (K - K2) % (2 ** m) == 0 and t != t2:
            print("INCONSISTENT", K, t, K2, t2)
print("consistency check done")
