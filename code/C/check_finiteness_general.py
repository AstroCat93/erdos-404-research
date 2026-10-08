"""Theorem F (general K): for p prime, K >= 3 and v_p(a+K) > tau(K,p):  f(a,p) = v_p(a!) + tau(K,p).
Checks: (1) independent DP for many (p,K,a) including K > p and p = 2;
        (2) self-consistency: if K = K' mod p^{min(tau,tau')+1} then tau(K,p) = tau(K',p)
            (otherwise the theorem would assign two values to f on a common class).
"""
from core import tauK, vp_fact, f_exact_upto, vp

TAU = {}
for p in (2, 3, 5, 7):
    Kmax = {2: 22, 3: 20, 5: 18, 7: 16}[p]
    row = []
    for K in range(1, Kmax + 1):
        t, z = tauK(K, p)
        TAU[(K, p)] = (t, z)
        row.append("*" if z else str(t))
    print("p=%d tau(K) K=1..%d:" % (p, Kmax), " ".join(row))

# (2) consistency
bad = 0
for (K, p), (t, z) in TAU.items():
    if z or K < 3:
        continue
    for (K2, p2), (t2, z2) in TAU.items():
        if p2 != p or z2 or K2 <= K or K2 < 3:
            continue
        m = min(t, t2) + 1
        if (K - K2) % (p ** m) == 0 and t != t2:
            bad += 1
            print("INCONSISTENT p=%d K=%d tau=%d K'=%d tau'=%d" % (p, K, t, K2, t2))
print("consistency violations:", bad)

# (1) DP checks
nchk = nbad = 0
for (K, p), (t, z) in sorted(TAU.items(), key=lambda x: (x[0][1], x[0][0])):
    if z or K < 3:
        continue
    mod = p ** (t + 1)
    for s in range(1, 40):
        a = mod * s - K
        if a < 1:
            continue
        if vp(a + K, p) <= t:
            continue
        pred = vp_fact(a, p) + t
        if pred > 140:
            break
        got = f_exact_upto(a, p, pred + 1)
        nchk += 1
        if got != pred:
            nbad += 1
            print("MISMATCH p=%d K=%d a=%d pred=%d got=%d" % (p, K, a, pred, got))
        break  # one a per (p,K) at least
print("DP checks:", nchk, "mismatches:", nbad)
