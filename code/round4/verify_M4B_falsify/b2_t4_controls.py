"""b2_t4_controls.py -- negative controls and boundary cases for M4B Cor B2'.

C1  hypothesis violated: 1 <= s with p^s <= e (d-1)! (gate too shallow for its distance).
    Records how often (b) Coll^pre_g = (3/2)2^{-d}, the identity (c), and the band [1/2,3/2] fail.
C2  d = 1 with the d >= 2 formula (the JSON statement of the claim does not exclude d = 1):
    Coll^pre_g = 1/2 (not (3/2)/2 = 3/4), and eps vs 2^{-1}p^s[eps_post + Delta(1/(x+n))/2].
C3  wrong argument in Delta: eps vs (c_{n+d}/c_n)[eps_post + Delta(r)/2] with r = 0 and r = 1
    instead of r* = 1/(x+n+d-1) (shows the identity is sharp, not a loose bound).
C4  gate in the SECOND window (d > N-n), as used by M4B Prop B5: checks Coll^pre_g = (3/2)2^{-d}
    (d >= 2) and p^K Coll_K <= (3/2)(c_{n+d}/c_n) p^{K-g}; records that g > D can occur, so the
    split identity of Cor B2'(c) has no meaning there (eps^post undefined).
C5  algebra behind the 'double root' reading: y_{n+d-2}+y_{n+d-1}+y_{n+d} = y_{n+d-2}(x+n+d)^2.
usage: b2_t4_controls.py SEED NCASES
"""
import itertools
import math
import random
import sys
from fractions import Fraction as Fr

from b2_lib import SignedLaw, Vrel, elems, forced_x, hyp_deep, vp, vx


def pre_stats(ys, d, p, g, K):
    collg = collK = 0
    for dl in itertools.product((-1, 0, 1), repeat=d):
        A = sum(a * b for a, b in zip(dl, ys[:d]))
        w = 1
        for t in dl:
            w *= 2 if t == 0 else 1
        if A % p ** g == 0:
            collg += w
        if A % p ** K == 0:
            collK += w
    return Fr(collg, 4 ** d), Fr(collK, 4 ** d)


def split_parts(x, n, N, Np, d, p):
    g = Vrel(x, n, n + d, p)
    D = Vrel(x, n, N, p)
    K = Vrel(x, n, Np, p)
    ys = elems(x, n, Np)
    law = SignedLaw(ys, p, K)
    e = p ** K * law.prob(K) - p ** D * law.prob(D)
    post = elems(x, n + d, Np)
    plaw = SignedLaw(post, p, K - g)
    ep = p ** (K - g) * plaw.prob(K - g) - p ** (D - g) * plaw.prob(D - g)

    def Delta(r):
        if K - g == 0:
            return Fr(0)
        return plaw.rho(K - g, r) - plaw.rho(D - g, r)
    return g, D, K, ys, e, ep, Delta


def main():
    seed, NC = int(sys.argv[1]), int(sys.argv[2])
    rnd = random.Random(seed)
    # ---------------- C1 ----------------
    c1 = dict(cases=0, b_fail=0, c_fail=0, band_fail=0, a_fail=0)
    c1_rows = {}
    while c1["cases"] < NC:
        p = rnd.choice((3, 5, 7))
        d = rnd.randint(3, 8)
        bad_s = [s for s in range(1, 40) if hyp_deep(p, s, d) is False]
        if not bad_s:
            continue
        s = rnd.choice(bad_s)
        n = rnd.randint(0, 30)
        N = n + d + rnd.randint(0, 5)
        Np = N + rnd.randint(1, 8)
        if Np - n > 20:
            continue
        x = forced_x(p, n + d, s, rnd)
        g, D, K, ys, e, ep, Delta = split_parts(x, n, N, Np, d, p)
        if D < g:
            continue
        a_ok = all(vx(x, n + i, p) == vp(d - i, p) for i in range(1, d))
        collg, collK = pre_stats(ys, d, p, g, K)
        cr = Fr(p ** g, 2 ** d)
        rstar = pow(x + n + d - 1, -1, p ** (K - g)) if K > g else 0
        pred = cr * (ep + Delta(rstar) / 2)
        c1["cases"] += 1
        key = (p, d, s)
        row = c1_rows.setdefault(key, [0, 0, 0, 0, 0])
        row[0] += 1
        if not a_ok:
            c1["a_fail"] += 1
            row[1] += 1
        if collg != Fr(3, 2) / 2 ** d:
            c1["b_fail"] += 1
            row[2] += 1
        if e != pred:
            c1["c_fail"] += 1
            row[3] += 1
        if ep > 0 and not (Fr(1, 2) <= e / (cr * ep) <= Fr(3, 2)):
            c1["band_fail"] += 1
            row[4] += 1
    print("C1 (hypothesis p^s > e(d-1)! violated):", c1)
    print("   per (p,d,s): [cases, (a) fails, (b) fails, (c) fails, band fails]")
    for k in sorted(c1_rows):
        print("   ", k, c1_rows[k])

    # ---------------- C2 ----------------
    c2 = dict(cases=0, coll_eq_half=0, d1_identity_ok=0, d2formula_ok=0, Kg=0)
    while c2["cases"] < NC:
        p = rnd.choice((3, 5, 7))
        s = rnd.randint(1, 8)
        n = rnd.randint(0, 30)
        N = n + 1 + rnd.randint(0, 7)
        Np = N + rnd.randint(1, 9)
        if Np - n > 20:
            continue
        x = forced_x(p, n + 1, s, rnd)
        g, D, K, ys, e, ep, Delta = split_parts(x, n, N, Np, 1, p)
        if K == g:
            c2["Kg"] += 1
            continue
        collg, collK = pre_stats(ys, 1, p, g, K)
        c2["cases"] += 1
        if collg == Fr(1, 2):
            c2["coll_eq_half"] += 1
        if e == Fr(p ** s, 2) * ep:
            c2["d1_identity_ok"] += 1
        r1 = pow(x + n, -1, p ** (K - g))
        if e == Fr(p ** g, 2) * (ep + Delta(r1) / 2):
            c2["d2formula_ok"] += 1
    print("C2 (d = 1):", c2, " [d2formula_ok counts cases where the d>=2 formula happens to hold]")

    # ---------------- C3 ----------------
    c3 = dict(cases=0, r0_ok=0, r1_ok=0, rstar_ok=0)
    while c3["cases"] < NC:
        p = rnd.choice((3, 5, 7))
        d = rnd.randint(2, 7)
        s0 = next(s for s in range(1, 99) if hyp_deep(p, s, d))
        s = s0 + rnd.randint(0, 3)
        n = rnd.randint(0, 30)
        N = n + d + rnd.randint(0, 6)
        Np = N + rnd.randint(1, 10)
        if Np - n > 20:
            continue
        x = forced_x(p, n + d, s, rnd)
        g, D, K, ys, e, ep, Delta = split_parts(x, n, N, Np, d, p)
        if K == g:
            continue
        cr = Fr(p ** g, 2 ** d)
        rstar = pow(x + n + d - 1, -1, p ** (K - g))
        c3["cases"] += 1
        c3["rstar_ok"] += e == cr * (ep + Delta(rstar) / 2)
        c3["r0_ok"] += e == cr * (ep + Delta(0) / 2)
        c3["r1_ok"] += e == cr * (ep + Delta(1) / 2)
    print("C3 (argument of Delta):", c3)

    # ---------------- C4 ----------------
    c4 = dict(cases=0, coll_fail=0, b5_fail=0, g_gt_D=0, PK_fail=0)
    while c4["cases"] < NC:
        p = rnd.choice((3, 5, 7))
        n = rnd.randint(0, 30)
        N = n + rnd.randint(1, 6)
        d = (N - n) + rnd.randint(1, 6)
        if d > 8:
            continue
        Np = n + d + rnd.randint(1, 8)
        if Np - n > 20:
            continue
        s0 = next(s for s in range(1, 99) if hyp_deep(p, s, d))
        s = s0 + rnd.randint(0, 3)
        x = forced_x(p, n + d, s, rnd)
        g = Vrel(x, n, n + d, p)
        D = Vrel(x, n, N, p)
        K = Vrel(x, n, Np, p)
        ys = elems(x, n, Np)
        collg, collK = pre_stats(ys, d, p, g, K)
        law = SignedLaw(ys, p, K)
        c4["cases"] += 1
        if g > D:
            c4["g_gt_D"] += 1
        if collg != Fr(3, 2) / 2 ** d:
            c4["coll_fail"] += 1
        if K > g and collK != Fr(1, 2 ** d):
            c4["PK_fail"] += 1
        if p ** K * law.prob(K) > Fr(3, 2) * Fr(p ** g, 2 ** d) * p ** (K - g):
            c4["b5_fail"] += 1
    print("C4 (gate in the second window, d > N-n):", c4)

    # ---------------- C5 ----------------
    c5 = dict(cases=0, fail=0)
    for _ in range(NC):
        p = rnd.choice((3, 5, 7))
        n = rnd.randint(0, 30)
        d = rnd.randint(2, 9)
        x = rnd.randrange(p ** 50)
        ys = elems(x, n, n + d + 1)
        c5["cases"] += 1
        if ys[d - 2] + ys[d - 1] + ys[d] != ys[d - 2] * (x + n + d) ** 2:
            c5["fail"] += 1
    print("C5 (y_{n+d-2}+y_{n+d-1}+y_{n+d} = y_{n+d-2}(x+n+d)^2):", c5)


if __name__ == "__main__":
    main()
