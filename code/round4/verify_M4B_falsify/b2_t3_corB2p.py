"""b2_t3_corB2p.py -- exact falsification test of M4B Corollary B2' (deep gate at distance d).

Hypotheses of the claim: composite window [n,N) u [N,N'), 1 <= d <= N-n, s = v(x+n+d) with
p^s > e (d-1)!, K > g (the case K = g is also run: there eps = 0 and the claim is trivial).
Checked exactly for every case:
  (a)  v(x+n+i) = v(d-i) (1 <= i < d) and g := V_{n+d}-V_n = v((d-1)!) + s;
  (b)  by explicit enumeration of all 3^d pre-vectors as exact integers A = sum_{i<d} delta_i y_{n+i}:
       the set {delta : p^g | A} is {0, +-(e_{d-2}+e_{d-1})} (d >= 2), {0} (d = 1); the two nontrivial
       A have valuation exactly g; Coll^pre_g = (3/2)2^{-d} (d>=2), 1/2 (d=1); P(p^K | A) = 2^{-d};
  (c)  eps (computed directly from the composite law, no splitting) equals
          d >= 2:  2^{-d} p^g [eps^post + (1/2) Delta(1/(x+n+d-1))],
          d  = 1:  (p^s/2) eps^post,
       where eps^post = eps([n+d,N),[N,N')) and Delta(r) = rho'_{K-g}(r) - rho'_{D-g}(r) are computed
       directly from the post window; |Delta(r*)| <= eps^post, Delta(-r*) = Delta(r*), and
       (1/2) <= eps / ((c_{n+d}/c_n) eps^post) <= 3/2.
Families: 'rand' (random windows/positions, s from s_hyp(d) to s_hyp(d)+4, sometimes s up to 60),
'negk' (x close to -k: n in [0,k-1], d = k-n, incl. n = 0 with x ~ -1, -2, -3 and s up to 60),
'two' (a second deep gate inside the post window, of depth up to s+12),
'end' (d = N-n: the first post window is empty), 'short' (N'-(n+d) < p, so K = g possible).
usage: b2_t3_corB2p.py SEED NCASES MMAX
"""
import itertools
import math
import random
import sys
from fractions import Fraction as Fr

from b2_lib import (SignedLaw, Vrel, elems, eps, forced_x, hyp_deep, vp, vx)


def s_hyp(p, d):
    return next(s for s in range(1, 400) if hyp_deep(p, s, d))


def check_case(p, x, n, N, Np, d, fam, out):
    s = vx(x, n + d, p)
    assert 1 <= d <= N - n
    assert hyp_deep(p, s, d) is True
    bad = []
    # (a)
    for i in range(1, d):
        if vx(x, n + i, p) != vp(d - i, p):
            bad.append(f"(a) v(x+n+{i})")
    g = Vrel(x, n, n + d, p)
    if g != vp(math.factorial(d - 1), p) + s if d > 1 else g != s:
        bad.append("(a) g")
    D = Vrel(x, n, N, p)
    K = Vrel(x, n, Np, p)
    ys = elems(x, n, Np)
    # (b) explicit enumeration of the pre-vectors (exact integers)
    pre = ys[:d]
    collg = 0
    collK = 0
    sols = []
    for dl in itertools.product((-1, 0, 1), repeat=d):
        A = sum(a * b for a, b in zip(dl, pre))
        w = 1
        for t in dl:
            w *= 2 if t == 0 else 1
        if A % p ** g == 0:
            collg += w
            sols.append(dl)
            if A != 0 and vp(A, p) != g:
                bad.append("(b) nontrivial A has valuation != g")
        if A % p ** K == 0:
            collK += w
    collg = Fr(collg, 4 ** d)
    collK = Fr(collK, 4 ** d)
    if d >= 2:
        exp_sols = {tuple([0] * d), tuple([0] * (d - 2) + [1, 1]), tuple([0] * (d - 2) + [-1, -1])}
        exp_collg = Fr(3, 2) / 2 ** d
    else:
        exp_sols = {(0,)}
        exp_collg = Fr(1, 2)
    if set(sols) != exp_sols:
        bad.append(f"(b) solution set {sols[:6]}")
    if collg != exp_collg:
        bad.append(f"(b) Coll^pre_g={collg}")
    if K > g and collK != Fr(1, 2 ** d):
        bad.append(f"(b) P(A=0 mod p^K)={collK}")
    # (c) direct eps, direct eps_post, Delta at r* = 1/(x+n+d-1)
    law = SignedLaw(ys, p, K)
    e_dir = p ** K * law.prob(K) - p ** D * law.prob(D)
    post = elems(x, n + d, Np)
    Kg, Dg = K - g, D - g
    plaw = SignedLaw(post, p, Kg)
    e_post = p ** Kg * plaw.prob(Kg) - p ** Dg * plaw.prob(Dg)
    e_post2, Dp, Kp = eps(x, n + d, N, Np, p)
    if (Dp, Kp) != (Dg, Kg) or e_post2 != e_post:
        bad.append("eps_post inconsistent")
    cratio = Fr(p ** g, 2 ** d)
    if Kg > 0:
        rstar = pow(x + n + d - 1, -1, p ** Kg)
        Delta = plaw.rho(Kg, rstar) - plaw.rho(Dg, rstar)
        Delta_m = plaw.rho(Kg, -rstar) - plaw.rho(Dg, -rstar)
    else:
        Delta = Delta_m = Fr(0)
    if Delta != Delta_m:
        bad.append("Delta not even at r*")
    if abs(Delta) > e_post:
        bad.append("|Delta(r*)| > eps_post")
    if d >= 2:
        pred = cratio * (e_post + Delta / 2)
    else:
        pred = Fr(p ** s, 2) * e_post
        if cratio != Fr(p ** s, 2):
            bad.append("d=1: c_{n+1}/c_n != p^s/2")
    if e_dir != pred:
        bad.append(f"(c) identity: eps={float(e_dir):.6g} pred={float(pred):.6g}")
    ratio = None
    if e_post > 0:
        ratio = e_dir / (cratio * e_post)
        if not (Fr(1, 2) <= ratio <= Fr(3, 2)):
            bad.append(f"(c) ratio {float(ratio)} outside [1/2,3/2]")
    elif e_dir != 0:
        bad.append("eps_post = 0 but eps != 0")
    out["cases"] += 1
    out["by_fam"][fam] = out["by_fam"].get(fam, 0) + 1
    out["by_p"][p] = out["by_p"].get(p, 0) + 1
    out["maxs"] = max(out["maxs"], s)
    out["maxK"] = max(out["maxK"], K)
    if K == g:
        out["K_eq_g"] += 1
    out["Kg_hist"][min(K - g, 10)] = out["Kg_hist"].get(min(K - g, 10), 0) + 1
    if ratio is not None and d >= 2:
        out["rmin"] = min(out["rmin"], ratio)
        out["rmax"] = max(out["rmax"], ratio)
        out["n_ratio"] += 1
        if ratio != 1:
            out["ratio_ne_1"] += 1
    if ratio is not None and d == 1 and ratio != 1:
        bad.append("d=1 ratio != 1")
    if bad:
        out["fail"] += 1
        print(f"FAIL fam={fam} p={p} n={n} N={N} N'={Np} d={d} s={s} D={D} K={K} g={g} "
              f"x mod p^40={x % p**40}: {bad}", flush=True)
    return dict(p=p, n=n, N=N, Np=Np, d=d, s=s, D=D, K=K, g=g, eps=e_dir, eps_post=e_post,
                Delta=Delta, ratio=ratio)


def main():
    seed, NC, MMAX = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rnd = random.Random(seed)
    out = dict(cases=0, fail=0, by_fam={}, by_p={}, maxs=0, maxK=0, K_eq_g=0,
               rmin=Fr(10), rmax=Fr(0), n_ratio=0, ratio_ne_1=0, Kg_hist={})
    examples = []
    while out["cases"] < NC:
        fam = rnd.choice(["rand", "rand", "negk", "two", "end", "short"])
        p = rnd.choice((3, 5, 7, 7))
        dmax = {3: 7, 5: 8, 7: 9}[p]
        extra = None
        if fam == "negk":
            k = rnd.randint(1, 10)
            n = rnd.randint(0, k - 1)
            d = k - n
            if d > dmax:
                continue
            N = n + d + rnd.randint(0, 6)
            Np = N + rnd.randint(1, MMAX - (N - n) if MMAX - (N - n) >= 1 else 1)
        else:
            n = rnd.choice([0, 1, 2] + list(range(3, 40)))
            d = rnd.randint(1, dmax)
            if fam == "end":
                N = n + d
            else:
                N = n + d + rnd.randint(0, 7)
            if fam == "short":
                Np = max(N + 1, n + d + rnd.randint(1, p - 1))
            else:
                Np = N + rnd.randint(1, 10)
        if Np - n > MMAX:
            continue
        s0 = s_hyp(p, d)
        if rnd.random() < 0.15:
            s = rnd.randint(s0, 60)
        else:
            s = s0 + rnd.randint(0, 4)
        if fam == "two":
            # second gate at distance d + t p^s from n, inside the post window
            ts = [t for t in range(1, 30) if t % p and d + t * p ** s <= Np - n]
            if not ts:
                # make room: shrink s to s0 and lengthen the window if possible
                s = s0
                ts = [t for t in range(1, 30) if t % p and d + t * p ** s <= MMAX]
                if not ts:
                    continue
                t = rnd.choice(ts)
                Np = max(Np, n + d + t * p ** s + rnd.randint(1, 3))
                if Np - n > MMAX:
                    continue
            else:
                t = rnd.choice(ts)
            extra = (t, rnd.randint(1, 12))
        x = forced_x(p, n + d, s, rnd, extra)
        r = check_case(p, x, n, N, Np, d, fam, out)
        if len(examples) < 12 and r["d"] >= 2 and r["ratio"] is not None:
            examples.append(r)
        if out["cases"] % 50 == 0:
            print(f"progress: {out['cases']} cases, failures {out['fail']}, by family {out['by_fam']}, "
                  f"max s {out['maxs']}, max K {out['maxK']}", flush=True)
    print("examples (d>=2):")
    for r in examples:
        print(f"  p={r['p']} [{r['n']},{r['N']},{r['Np']}) d={r['d']} s={r['s']} g={r['g']} D={r['D']} K={r['K']} "
              f"eps={float(r['eps']):.6g} eps_post={float(r['eps_post']):.6g} Delta(r*)={float(r['Delta']):.6g} "
              f"ratio={float(r['ratio']):.6f}")
    print(f"ratio range over d>=2 cases with eps_post>0: [{float(out['rmin']):.6f}, {float(out['rmax']):.6f}] "
          f"({out['n_ratio']} cases, ratio != 1 in {out['ratio_ne_1']})")
    print("histogram of K-g (10 means >= 10):", dict(sorted(out["Kg_hist"].items())))
    print("RESULT corB2p:", {k: (float(v) if isinstance(v, Fr) else v) for k, v in out.items()})


if __name__ == "__main__":
    main()
