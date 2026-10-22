#!/usr/bin/env python3
"""cw5_check.py -- exact test of Corollary W5 of data/round4/reports/M4D.md.
For a window W=[n,N) (jump D) and band D2 (= jump of W'=[N,N2)), with a_r = p^D2/|Lift(r)| - 1 and
m(W;D2) = p^D / sum_r a_r^{-1} (harmonic mean; 0 if some a_r = 0):
  (a) for every probability vector q on {0,1}^H:  Fine(q) := p^(D+D2) Coll_(D+D2)(mu^q) - p^D Coll_D(mu^q) >= m;
  (b) equality for the optimal q* (class r gets mass prop. to 1/a_r, uniform over its lifts and over the f
      representing each lift; uniform over the complete classes if some a_r = 0).
Exact rationals.  Random q: Dirichlet-like integer weights, plus point masses and the uniform vector.
usage: cw5_check.py p seed nx n H H2 nq
"""
import random
import sys
from fractions import Fraction

from m4d_lib import vp_int, window_elems


def fine(sums, q, p, D, K):
    lawK, lawD = {}, {}
    for f, s in enumerate(sums):
        if q[f]:
            lawK[s] = lawK.get(s, 0) + q[f]
            lawD[s % p ** D] = lawD.get(s % p ** D, 0) + q[f]
    return p ** K * sum(c * c for c in lawK.values()) - p ** D * sum(c * c for c in lawD.values())


def main():
    p, seed, nx, n, H, H2, nq = (int(t) for t in sys.argv[1:8])
    rnd = random.Random(seed)
    N, N2 = n + H, n + H + H2
    bad_a = bad_b = done = zero_m = 0
    minratio = None
    while done < nx:
        x = rnd.randrange(p ** 60)
        vals = [vp_int(x + i, p) for i in range(1, N2 + 1)]
        if max(vals) > 20:
            continue
        D = sum(vals[n:N])
        D2 = sum(vals[N:N2])
        K = D + D2
        if K > 8 or D2 < 1:
            continue
        done += 1
        mK = p ** K
        ys = window_elems(x, n, N, mK)
        sums = []
        for f in range(1 << H):
            sums.append(sum(ys[i] for i in range(H) if (f >> i) & 1) % mK)
        lifts = {}
        for f, s in enumerate(sums):
            lifts.setdefault(s % p ** D, {}).setdefault(s, []).append(f)
        a = {}
        for r in range(p ** D):
            k = len(lifts.get(r, {}))
            a[r] = None if k == 0 else Fraction(p ** D2, k) - 1
        complete = [r for r in a if a[r] == 0]
        if complete:
            m = Fraction(0)
            nu = {r: Fraction(1, len(complete)) for r in complete}
            zero_m += 1
        else:
            inv = sum(1 / a[r] for r in a if a[r] is not None)
            m = Fraction(p ** D) / inv
            nu = {r: (1 / a[r]) / inv for r in a if a[r] is not None}
        qstar = [Fraction(0)] * (1 << H)
        for r, w in nu.items():
            L = lifts[r]
            for s, fl in L.items():
                for f in fl:
                    qstar[f] = w / (len(L) * len(fl))
        if fine(sums, qstar, p, D, K) != m:
            bad_b += 1
        qs = [[Fraction(1, 1 << H)] * (1 << H)]
        for _ in range(nq):
            raw = [rnd.randint(0, 6) for _ in range(1 << H)]
            if sum(raw) == 0:
                raw[0] = 1
            qs.append([Fraction(c, sum(raw)) for c in raw])
            pm = [Fraction(0)] * (1 << H)
            pm[rnd.randrange(1 << H)] = Fraction(1)
            qs.append(pm)
        for q in qs:
            F = fine(sums, q, p, D, K)
            if F < m:
                bad_a += 1
            if m > 0:
                rt = F / m
                minratio = rt if minratio is None or rt < minratio else minratio
    print(f"RESULT cw5 p={p} n={n} H={H} H2={H2} samples={done} (m=0 in {zero_m}): (a) Fine(q) < m: {bad_a} "
          f"(of {done * (2 * nq + 1)} weightings; min Fine/m over m>0: {float(minratio) if minratio else 'n/a'}); "
          f"(b) Fine(q*) != m: {bad_b}")


if __name__ == "__main__":
    main()
