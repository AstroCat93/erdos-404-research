#!/usr/bin/env python3
"""b2p_identity.py -- exact test of M4B Corollary B2' (deep gate at distance d), end to end.

For a composite window [n,N) u [N,N') and a gate at n+d (1 <= d <= N-n) of depth s = v(x+n+d):
 (a)  v(x+n+i) = v(d-i) for 1 <= i < d, and g := V_{n+d}-V_n = v((d-1)!) + s;
 (b)  the pre-patterns delta_pre in {-1,0,1}^d with A := sum_{i<d} delta_{n+i} y_{n+i} == 0 mod p^g are
      exactly 0 and +-(e_{d-2}+e_{d-1}); the latter have v(A) = g exactly;
      Coll^pre_g = (3/2) 2^-d (d>=2), = 1/2 (d=1);  P(A == 0 mod p^K) = 2^-d   (when K > g);
 (c)  eps = (c_{n+d}/c_n) [eps_post + Delta(1/(x+n+d-1))/2]  (d>=2),   eps = (p^s/2) eps_post  (d=1),
      with c_{n+d}/c_n = 2^-d p^g, eps_post = eps([n+d,N),[N,N')), Delta(r) = rho'_{K-g}(r) - rho'_{D-g}(r),
      rho'_k(r) = p^k P(B' == r mod p^k), B' the signed sum of the post window elements pi_j/pi_{n+d};
      and |Delta(r)| <= eps_post, so eps/((c_{n+d}/c_n) eps_post) in [1/2, 3/2].
eps and eps_post are computed from the R3M definition (unsigned subset-sum collisions); Delta from the
signed law of the post window.  Everything exact (integers / Fractions).
Hypothesis tested: p^s > e (d-1)!.  Rows marked SUB use p^s <= e (d-1)! (negative control: the claims
are not expected to hold).  NEGd1: at d = 1 the d>=2 formula (with the Delta term) is also evaluated.
usage: b2p_identity.py p SEED NPER n H H2 KMAX PREC DLIST SEXTRA [SUB]
   DLIST e.g. 1,2,3,7 ; SEXTRA = number of depths s above the threshold s_min(d) to try (s_min..s_min+SEXTRA);
   SUB=1 also tries s = s_min-1, s_min-2 (>=1) as negative control.
"""
import sys
import math
import random
from fractions import Fraction
from itertools import product

from b2lib import vp, elems, unsigned_counts, signed_counts, fold, eps_def, vals_and_V


def smin(p, d):
    s = 0
    while p ** s <= math.e * math.factorial(d - 1):
        s += 1
    return max(s, 1)


def one(p, x, n, N, N2, d, s_req, KMAX, PREC, stats, tag):
    v, VV = vals_and_V(x, p, n, N2, PREC)
    s = v[n + d]
    assert s == s_req
    D, K = VV[N], VV[N2]
    if K > KMAX:
        return None
    g = VV[n + d]
    hyp = p ** s > math.e * math.factorial(d - 1)
    res = {}
    # (a)
    res['a'] = all(v[n + i] == vp(d - i, p, 99) for i in range(1, d)) and g == vp(math.factorial(d - 1), p, 99) + s
    # (b) exhaustive over pre-patterns, exact mod p^PREC
    M = p ** PREC
    ypre = elems(x, n, n + d, M)
    zero_g, zero_K = [], []
    for dl in product((-1, 0, 1), repeat=d):
        A = sum(a * b for a, b in zip(dl, ypre)) % M
        vA = vp(A, p, PREC)
        if vA >= g:
            zero_g.append((dl, vA))
        if vA >= K:
            zero_K.append(dl)
    pair = tuple([0] * (d - 2) + [1, 1]) if d >= 2 else None
    exp_g = {tuple([0] * d)} | ({pair, tuple(-t for t in pair)} if d >= 2 else set())
    w = lambda dl: Fraction(1, 2 ** sum(1 for t in dl if t == 0) * 4 ** sum(1 for t in dl if t != 0))
    collg = sum(w(dl) for dl, _ in zero_g)
    p0K = sum(w(dl) for dl in zero_K)
    res['b_set'] = {dl for dl, _ in zero_g} == exp_g
    res['b_vpair'] = all(vA == g for dl, vA in zero_g if any(dl)) if d >= 2 else True
    res['b_coll'] = collg == (Fraction(3, 2 ** (d + 1)) if d >= 2 else Fraction(1, 2))
    res['b_p0K'] = (p0K == Fraction(1, 2 ** d)) if K > g else True
    # (y+2)^2 gloss: pair (1,1) before the gate plus delta_{n+d} = 1 gives y_{n+d-2} (x+n+d)^2
    if d >= 2:
        yy = elems(x, n, n + d + 1, M)
        res['gloss'] = (yy[d - 2] + yy[d - 1] + yy[d]) % M == yy[d - 2] * (x + n + d) ** 2 % M
    # (c) end to end
    yK = elems(x, n, N2, p ** K)
    eps = eps_def(yK, p, D, K)
    Kg, Dg = K - g, D - g
    post = elems(x, n + d, N2, p ** max(Kg, 0)) if Kg > 0 else [0] * (N2 - n - d)
    eps_post = eps_def(post, p, Dg, Kg) if Kg > 0 else Fraction(0)
    Lp = len(post)
    if Kg > 0:
        cs = signed_counts(post, p ** Kg)
        csD = fold(cs, p ** Dg)

        def Delta(r):
            return Fraction(p ** Kg * int(cs[r % p ** Kg]) - p ** Dg * int(csD[r % p ** Dg]), 4 ** Lp)
        r = pow((x + n + d - 1) % p ** Kg, -1, p ** Kg)
        Dl = Delta(r)
        res['B2.2'] = Delta(0) == eps_post
        res['|Delta|<=eps_post'] = abs(Dl) <= eps_post and abs(Delta(-r)) <= eps_post
        res['Delta even'] = Delta(-r) == Dl
    else:
        Dl = Fraction(0)
    ratio_c = Fraction(p ** g, 2 ** d)
    assert ratio_c == Fraction(p ** (VV[n + d]), 2 ** d)
    if d >= 2:
        rhs = ratio_c * (eps_post + Dl / 2)
    else:
        rhs = Fraction(p ** s, 2) * eps_post
        # negative control: the d>=2 formula at d=1, with Delta(1/(x+n))
        if Kg > 0:
            r1 = pow((x + n) % p ** Kg, -1, p ** Kg)
            alt = ratio_c * (eps_post + Delta(r1) / 2)
            stats['NEGd1_tot'] += 1
            stats['NEGd1_differs'] += int(alt != eps)
    res['c_identity'] = (eps == rhs)
    if eps_post > 0:
        q = eps / (ratio_c * eps_post)
        res['c_bounds'] = Fraction(1, 2) <= q <= Fraction(3, 2)
        stats['ratios'].append((d, float(q), hyp))
    else:
        res['c_bounds'] = (eps == 0)
    key = 'hyp' if hyp else 'SUB'
    stats[key + '_n'] += 1
    for k, ok in res.items():
        stats.setdefault(key + ':' + k, [0, 0])
        stats[key + ':' + k][0] += 1
        stats[key + ':' + k][1] += int(not ok)
    if hyp and not all(res.values()):
        print(f"  FAIL {tag} d={d} s={s} g={g} D={D} K={K} x mod p^12={x % p**12} res={res}", flush=True)
    return (d, s, g, D, K, float(eps), float(eps_post), float(Dl))


def main():
    a = sys.argv[1:]
    p, seed, NPER, n, H, H2, KMAX, PREC = (int(t) for t in a[:8])
    dlist = [int(t) for t in a[8].split(',')]
    SEXTRA = int(a[9])
    SUB = len(a) > 10 and a[10] == '1'
    N, N2 = n + H, n + H + H2
    rnd = random.Random(seed)
    stats = {'hyp_n': 0, 'SUB_n': 0, 'NEGd1_tot': 0, 'NEGd1_differs': 0, 'ratios': []}
    for d in dlist:
        if d > H:
            continue
        s0 = smin(p, d)
        slist = list(range(s0, s0 + SEXTRA + 1))
        if SUB:
            slist = [s for s in (s0 - 2, s0 - 1) if s >= 1] + slist
        for s in slist:
            done = tries = 0
            ex = None
            while done < NPER and tries < 400:
                tries += 1
                wv = rnd.randrange(1, p ** (PREC - s))
                if wv % p == 0:
                    continue
                x = (p ** s * wv - n - d) % p ** PREC
                r = one(p, x, n, N, N2, d, s, KMAX, PREC, stats, f"p={p} n={n}")
                if r is None:
                    continue
                done += 1
                ex = r
            mark = '' if p ** s > math.e * math.factorial(d - 1) else ' SUB'
            print(f"p={p} n={n} N={N} N'={N2} d={d} s={s}{mark}: {done} samples (tries {tries})"
                  + (f"; last: g={ex[2]} D={ex[3]} K={ex[4]} eps={ex[5]:.6g} eps_post={ex[6]:.6g} Delta={ex[7]:.6g}" if ex else ""),
                  flush=True)
    print("--- summary (key: [checks, failures]) ---")
    for k in sorted(stats):
        if k != 'ratios':
            print(f"  {k}: {stats[k]}")
    rs = stats['ratios']
    for hh in (True, False):
        for d in sorted({t[0] for t in rs if t[2] == hh}):
            qs = [q for dd, q, h3 in rs if dd == d and h3 == hh]
            print(f"  ratio eps/((c_(n+d)/c_n) eps_post) [{'hyp' if hh else 'SUB'}], d={d}: n={len(qs)} "
                  f"min={min(qs):.4f} max={max(qs):.4f} distinct={len(set(qs))}")
    hf = sum(v[1] for k, v in stats.items() if k.startswith('hyp:'))
    print(f"RESULT p={p} n={n} H={H} H2={H2}: {stats['hyp_n']} cases under the hypothesis, failures {hf}; "
          f"SUB cases {stats['SUB_n']}; NEGd1 (d>=2 formula used at d=1) differs from eps in "
          f"{stats['NEGd1_differs']}/{stats['NEGd1_tot']}")


if __name__ == "__main__":
    main()
