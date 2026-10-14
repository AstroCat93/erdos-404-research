"""b2_t6_exhaustive.py -- exhaustive-over-residues test of Cor B2', with a direct decomposition
of eps by the pre-window digits (no division by y_{n+d}, no use of Prop B2).

For each configuration (p, n, d, s, N-n-d, N'-N) the gate is x = -(n+d) + p^s w and w runs over ALL
units modulo p^R (higher digits random).  For every case:
  (i)   the composite eps computed from scratch equals the Cor B2' formula;
  (ii)  direct decomposition: for a pre-vector delta_pre (digits at n..n+d-1) put
          T(delta_pre) := P(delta_pre) [p^K P(A + sum_{j>=n+d} delta_j y_j == 0 mod p^K)
                                       - p^D P(A + sum_{j>=n+d} delta_j y_j == 0 mod p^D)],
        computed by meet in the middle over the post digits with the y_j taken relative to n.
        Claim mechanism: T(0) = 2^{-d} p^g eps_post, T(+-pair) = 2^{-d} p^g Delta(r*)/4 each, and
        T = 0 for every other delta_pre (all of them for d <= 3, 6 random ones otherwise);
        sum of T over all delta_pre = eps (d <= 3).
usage: b2_t6_exhaustive.py SEED R3 R5 R7
"""
import itertools
import math
import random
import sys
from fractions import Fraction as Fr

from b2_lib import PREC, SignedLaw, Vrel, elems, hyp_deep, rand_unit, vx


def s_hyp(p, d):
    return next(s for s in range(1, 400) if hyp_deep(p, s, d))


def run_case(p, x, n, N, Np, d, rnd, stats):
    s = vx(x, n + d, p)
    g = Vrel(x, n, n + d, p)
    D, K = Vrel(x, n, N, p), Vrel(x, n, Np, p)
    ys = elems(x, n, Np)
    law = SignedLaw(ys, p, K)
    e = p ** K * law.prob(K) - p ** D * law.prob(D)
    plaw = SignedLaw(elems(x, n + d, Np), p, K - g)
    ep = p ** (K - g) * plaw.prob(K - g) - p ** (D - g) * plaw.prob(D - g)
    if K > g:
        r = pow(x + n + d - 1, -1, p ** (K - g))
        Dl = plaw.rho(K - g, r) - plaw.rho(D - g, r)
    else:
        Dl = Fr(0)
    cr = Fr(p ** g, 2 ** d)
    pred = cr * (ep + Dl / 2) if d >= 2 else Fr(p ** s, 2) * ep
    bad = []
    if e != pred:
        bad.append("(i) identity")
    # (ii) decomposition over pre-vectors
    postlaw = SignedLaw(ys[d:], p, K)          # post digits, y_j relative to n
    pre = ys[:d]
    zero = tuple([0] * d)
    pairs = [tuple([0] * (d - 2) + [1, 1]), tuple([0] * (d - 2) + [-1, -1])] if d >= 2 else []
    allv = list(itertools.product((-1, 0, 1), repeat=d))
    others = [v for v in allv if v != zero and v not in pairs]
    if d > 3:
        others = rnd.sample(others, 6)
    total = Fr(0)

    def T(v):
        A = sum(a * b for a, b in zip(v, pre))
        w = 1
        for t in v:
            w *= 2 if t == 0 else 1
        return Fr(w, 4 ** d) * (p ** K * postlaw.prob(K, -A) - p ** D * postlaw.prob(D, -A))
    t0 = T(zero)
    total += t0
    if t0 != cr * ep:
        bad.append("(ii) T(0)")
    for v in pairs:
        tv = T(v)
        total += tv
        if tv != cr * Dl / 4:
            bad.append("(ii) T(pair)")
    for v in others:
        if T(v) != 0:
            bad.append(f"(ii) T{v}!=0")
    if d <= 3:
        total += sum(T(v) for v in others)
        if total != e:
            bad.append("(ii) sum T != eps")
    if False:
        bad.append("(ii) sum T != eps")
    stats["cases"] += 1
    stats["others_checked"] += len(others)
    if bad:
        stats["fail"] += 1
        print(f"FAIL p={p} n={n} N={N} N'={Np} d={d} s={s} x mod p^30={x % p**30}: {bad}", flush=True)


def main():
    seed = int(sys.argv[1])
    R = {3: int(sys.argv[2]), 5: int(sys.argv[3]), 7: int(sys.argv[4])}
    rnd = random.Random(seed)
    grand = dict(cases=0, fail=0, others_checked=0)
    for p in (7, 5, 3):
        for n in (0, 3, 2 * p):
            for d in range(1, 6):
                s0 = s_hyp(p, d)
                for s in (s0, s0 + 1):
                    for extra1 in (0, 4):
                        for L2 in (p - 1, 2 * p - 2):
                            N = n + d + extra1
                            Np = N + L2
                            if Np - n > 22:
                                continue
                            st = dict(cases=0, fail=0, others_checked=0)
                            mod = p ** R[p]
                            for w0 in range(1, mod):
                                if w0 % p == 0:
                                    continue
                                hi = rnd.randrange(p ** (PREC - s - R[p] - 5))
                                w = w0 + mod * hi
                                x = (-(n + d) + p ** s * w) % p ** PREC
                                run_case(p, x, n, N, Np, d, rnd, st)
                            for k in grand:
                                grand[k] += st[k]
                            print(f"p={p} n={n} d={d} s={s} window [{n},{N},{Np}): all {st['cases']} units mod "
                                  f"p^{R[p]}: failures {st['fail']}", flush=True)
    print("RESULT exhaustive:", grand)


if __name__ == "__main__":
    main()
