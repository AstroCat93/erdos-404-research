# (1) Lemma 11.37(a) congruence P_m(r) == eps*e_{p-1-r} mod p^{J_m}, J_m = 1+v_p(m+1), for many m.
# (2) theta_set construction (Cor 11.39(b)): per block keep one subset per distinct residue mod p^{J_m},
#     uniform law; check exact collision mass at block levels C_{a_m} <= prod p^{J}/dist_p(J).
import sys
from math import factorial
import numpy as np
from itertools import combinations

def vp(n, p):
    c = 0
    while n % p == 0: n //= p; c += 1
    return c

def vfact(n, p):
    s, q = 0, p
    while q <= n: s += n // q; q *= p
    return s

def cong(p, mmax):
    e = [(-1)**u * factorial(p-1)//factorial(u) for u in range(p)]
    eps = -1 if p == 2 else 1
    bad = 0
    for m in range(0, mmax):
        J = 1 + vp(m+1, p); md = p**J
        P = 1
        for r in range(p):
            if r > 0: P *= (p*m + r)
            if (P - eps*e[p-1-r]) % md: bad += 1
    return bad

def setcheck(p, m0, K):
    e = [(-1)**u * factorial(p-1)//factorial(u) for u in range(p)]
    subs = {0}
    for x in e: subs |= {s+x for s in subs}
    distp = lambda j: len({s % p**j for s in subs})
    mod = p**K
    e0 = vfact(p*m0, p)
    P = np.zeros(mod); P[0] = 1.0   # law of Y - Y' (difference of two independent copies)
    m = m0; bound = 1.0; out = []
    while True:
        a = vfact(p*m, p) - e0
        if a >= K: break
        J = 1 + vp(m+1, p)
        xs = [(factorial(p*m + r) // p**e0) % mod for r in range(p)]
        # all 2^p subset sums mod p^K, pick one per residue mod p^{a+J} (i.e. relative residue mod p^J)
        reps = {}
        for mask in range(1 << p):
            s = sum(xs[r] for r in range(p) if mask >> r & 1) % mod
            key = (s // p**a) % p**J if a + J <= K else s  # relative residue
            reps.setdefault(key, s)
        vals = list(reps.values())
        if a + J <= K:
            assert len(vals) == distp(J), (p, m, len(vals), distp(J))
        q = np.zeros(mod)
        for v in vals: q[v] += 1.0/len(vals)
        qh = np.fft.fft(q)
        diff = np.real(np.fft.ifft(qh*np.conj(qh)))  # law of Y-Y'
        P = np.real(np.fft.ifft(np.fft.fft(P)*np.fft.fft(diff)))
        if a + J <= K:
            bound *= p**J / distp(J)
            Ck = p**(a+J) * P[::p**(a+J)].sum()
            out.append((m, a+J, Ck, bound))
            if Ck > bound*(1+1e-9): print("VIOLATION", p, m, a+J, Ck, bound)
        m += 1
    return out

if __name__ == "__main__":
    for p, mm in [(2, 4000), (3, 3000), (5, 2000), (7, 1000), (11, 400), (13, 300)]:
        print("congruence 11.37(a) p=%d m<%d bad=%d" % (p, mm, cong(p, mm)))
    for p, m0, K in [(2, 1, 16), (2, 3, 14), (3, 1, 11), (3, 2, 10), (5, 1, 7), (7, 1, 6)]:
        out = setcheck(p, m0, K)
        print("set-measure p=%d m0=%d:" % (p, m0), " ".join("k=%d C=%.5g<=%.5g" % (k, c, b) for (_, k, c, b) in out))
