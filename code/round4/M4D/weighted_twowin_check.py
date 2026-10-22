#!/usr/bin/env python3
"""weighted_twowin_check.py -- exact test of the weighted window identities of data/round4/reports/M4D.md:
Lemma W1 (weighted martingale), Lemma W2 (weighted one-window variance bound),
Proposition W3 (weighted two-window inequality) and Corollary W4 (zero variance under fibre-uniform weights).

Windows W=[n,N), W'=[N,N2), cylinder C = x + p^m Z_p (m = V_n), hypothesis (5.2): D+D2 <= m - M_N2, M_N2 < m.
Parent set: slope-0 paths alive at n, with random positive parent weights w(e).  Window weights q on {0,1}^H,
q2 on {0,1}^H2 (probability vectors).  For every w mod p^(D+D2) (x' = x0 + p^m w + p^(m+D+D2) z, z random):
  M_N(x')  = p^(V_N)  * sum_{(e,f) alive at N, slope 0} w(e) q(f)
  M_N2(x') = p^(V_N2) * sum_{(e,f,f2) alive at N2, slope 0} w(e) q(f) q2(f2)
  M_n      = p^m * sum_e w(e).
Checks (all exact rationals):
  (W1)   E_C M_N = E_C M_N2 = M_n
  (W2)   Var_C(M_N) <= M_n^2 chi2_q,  chi2_q = p^D Coll_D(mu^q) - 1
  (W3)   E_C M_N2^2 - E_C M_N^2 <= eps * M_n^2,  eps = p^(D+D2) Coll_(D+D2)(nu) - p^D Coll_D(nu),
         nu = law of Q_f + p^D u Q_f2 mod p^(D+D2) with f~q, f2~q2 (the weighted composite law)
  (W4)   if q is fibre-uniform (every class r with mu^q(r)>0 has uniform weight on all p^D2 lifts) then eps == 0
         and M_N2 is constant on every cylinder C' = x' + p^(m+D) Z_p with value M_N(C')
  (inh)  every alive child / grandchild of a slope-0 parent has slope 0
Weight modes: 'rand' (random positive rational q, q2), 'unif' (uniform: reproduces R3M Prop C2),
'fib' (q fibre-uniform on all fully lifted classes, if any; q2 random),
'vary' (q random; q2 random and DIFFERENT on each sub-cylinder C' = w mod p^D): checks the adapted form
  (W3') E_C M_N2^2 - E_C M_N^2 <= epst * M_n^2 with epst = p^(D+D2) Coll_(D+D2)(mu^q) - p^D Coll_D(mu^q).
Option MAXPAR: if there are more slope-0 parents, a random subset of MAXPAR of them gets positive weight and the
others weight 0 (allowed: the statements hold for every nonnegative parent weight).
usage: weighted_twowin_check.py p seed nx n H H2 mode [KMAX] [MAXPAR]
"""
import random
import sys
from fractions import Fraction

from m4d_lib import PAdic, products, alive_from_scratch, extend, window_elems, unit_cofactor


def law_weighted(elems, weights, modulus):
    """dict r -> sum of weights[f] over f with sum_i f_i elems[i] == r mod modulus (f as bitmask)."""
    H = len(elems)
    out = {}
    for f in range(1 << H):
        s = 0
        for i in range(H):
            if (f >> i) & 1:
                s += elems[i]
        r = s % modulus
        out[r] = out.get(r, 0) + weights[f]
    return out


def coll(law):
    return sum(c * c for c in law.values())


def main():
    a = sys.argv[1:]
    p, seed, nx, n, H, H2 = (int(t) for t in a[:6])
    mode = a[6]
    kmax = int(a[7]) if len(a) > 7 else 6
    maxpar = int(a[8]) if len(a) > 8 else 10 ** 9
    N, N2 = n + H, n + H + H2
    prec = max(60, 3 * N2 // (p - 1) + 30)
    P = PAdic(p, prec)
    rnd = random.Random(seed)
    st = dict(samples=0, w1=0, w2=0, w3=0, w4eps=0, w4const=0, w4n=0, inh=0, nontriv=0)
    worst = 0.0
    tries = 0
    while st['samples'] < nx and tries < 300000:
        tries += 1
        x = rnd.randrange(P.mod)
        pi, dpi, vals = products(P, x, N2)
        m = sum(vals[1:n + 1])
        VN = sum(vals[1:N + 1])
        VN2 = sum(vals[1:N2 + 1])
        D, D2 = VN - m, VN2 - VN
        MN2 = max(vals[1:N2 + 1])
        if not (MN2 < m and D + D2 <= m - MN2) or D + D2 > kmax or D2 < 1 or D < 1:
            continue
        par_all = alive_from_scratch(P, pi, dpi, vals, n)
        par0 = [t for t in par_all if P.v(t[2]) == 0]
        if not par0:
            continue
        K = D + D2
        mK, mD, mD2 = p ** K, p ** D, p ** D2
        ys = window_elems(x, n, N, mK)
        ys2 = window_elems(x, N, N2, mD2)
        u = unit_cofactor(x, n, N, p, D, mK)
        # window weights
        q2by = None
        if mode == 'unif':
            q = [Fraction(1, 1 << H)] * (1 << H)
            q2 = [Fraction(1, 1 << H2)] * (1 << H2)
        elif mode == 'vary':
            raw = [rnd.randint(1, 9) for _ in range(1 << H)]
            q = [Fraction(c, sum(raw)) for c in raw]
            q2by = {}
            for cls in range(mD):
                raw2 = [rnd.randint(0, 9) for _ in range(1 << H2)]
                if sum(raw2) == 0:
                    raw2[0] = 1
                q2by[cls] = [Fraction(c, sum(raw2)) for c in raw2]
            q2 = q2by[0]
        else:
            raw2 = [rnd.randint(1, 9) for _ in range(1 << H2)]
            q2 = [Fraction(c, sum(raw2)) for c in raw2]
            if mode == 'rand':
                raw = [rnd.randint(1, 9) for _ in range(1 << H)]
                q = [Fraction(c, sum(raw)) for c in raw]
            elif mode == 'fib':
                # fibre-uniform weights on the fully lifted classes of W (band D2)
                lifts = {}
                for f in range(1 << H):
                    s = sum(ys[i] for i in range(H) if (f >> i) & 1) % mK
                    lifts.setdefault(s % mD, {}).setdefault(s, []).append(f)
                full = [r for r, d in lifts.items() if len(d) == mD2]
                if not full:
                    continue
                q = [Fraction(0)] * (1 << H)
                for r in full:
                    for s, fl in lifts[r].items():
                        for f in fl:
                            q[f] = Fraction(1, len(full) * mD2 * len(fl))
            else:
                raise SystemExit("mode must be rand|unif|fib")
        st['samples'] += 1
        if len(par0) > maxpar:
            par0 = rnd.sample(par0, maxpar)
        wts = {b: Fraction(rnd.randint(1, 5)) for (b, _, _) in par0}
        Wn = sum(wts.values())
        Mn = p ** m * Wn
        x0 = x % p ** m
        maskn = (1 << n) - 1
        maskH = (1 << H) - 1
        sum1 = sum1sq = sum2 = sum2sq = Fraction(0)
        byCp = {}   # w mod p^D -> list of (M_N, M_N2)
        for w in range(mK):
            z = rnd.randrange(p ** 6)
            xp = x0 + p ** m * w + p ** (m + K) * z
            pi2, dpi2, vals2 = products(P, xp, N2)
            roots = []
            for (b, _, _) in par0:
                S = sum(pi2[j] for j in range(n) if (b >> j) & 1) % P.mod
                dS = sum(dpi2[j] for j in range(n) if (b >> j) & 1) % P.mod
                roots.append((b, S, dS))
            kids = extend(P, pi2, dpi2, vals2, n, N, roots)
            Z1 = Fraction(0)
            for (b2, S2, dS2) in kids:
                if P.v(dS2) != 0:
                    st['inh'] += 1
                Z1 += wts[b2 & maskn] * q[(b2 >> n) & maskH]
            gk = extend(P, pi2, dpi2, vals2, N, N2, kids)
            if q2by is not None:
                q2 = q2by[w % mD]
            Z2 = Fraction(0)
            for (b3, S3, dS3) in gk:
                if P.v(dS3) != 0:
                    st['inh'] += 1
                Z2 += wts[b3 & maskn] * q[(b3 >> n) & maskH] * q2[b3 >> N]
            M1 = p ** VN * Z1
            M2 = p ** VN2 * Z2
            sum1 += M1
            sum1sq += M1 * M1
            sum2 += M2
            sum2sq += M2 * M2
            byCp.setdefault(w % mD, []).append((M1, M2))
        E1, E2 = sum1 / mK, sum2 / mK
        if not (E1 == Mn and E2 == Mn):
            st['w1'] += 1
        # (W2)
        lawD = law_weighted(ys, q, mD)
        chi2 = mD * coll(lawD) - 1
        var1 = sum1sq / mK - E1 * E1
        if var1 > Mn * Mn * chi2:
            st['w2'] += 1
        # (W3'): adapted bound with epst (fine mass of q alone), valid for any q2 constant on each C'
        lawKq = law_weighted(ys, q, mK)
        lawDq = {}
        for r_, c_ in lawKq.items():
            lawDq[r_ % mD] = lawDq.get(r_ % mD, 0) + c_
        epst = mK * coll(lawKq) - mD * coll(lawDq)
        if sum2sq / mK - sum1sq / mK > epst * Mn * Mn:
            st['w3t'] = st.get('w3t', 0) + 1
        if epst > 0:
            st['wt'] = max(st.get('wt', 0.0), float((sum2sq / mK - sum1sq / mK) / (epst * Mn * Mn)))
        if mode == 'vary':
            continue
        # (W3): weighted composite law nu mod p^K
        lawK = law_weighted(ys, q, mK)
        law2 = law_weighted(ys2, q2, mD2)
        nu = {}
        for r1, c1 in lawK.items():
            for r2, c2 in law2.items():
                s = (r1 + p ** D * u * r2) % mK
                nu[s] = nu.get(s, 0) + c1 * c2
        nuD = {}
        for s, c in nu.items():
            nuD[s % mD] = nuD.get(s % mD, 0) + c
        eps = mK * coll(nu) - mD * coll(nuD)
        lhs = sum2sq / mK - sum1sq / mK
        rhs = eps * Mn * Mn
        if lhs > rhs:
            st['w3'] += 1
        if rhs > 0:
            worst = max(worst, float(lhs / rhs))
            if lhs > 0:
                st['nontriv'] += 1
        # constancy of M_N2 on the sub-cylinders C' (predicted only for fibre-uniform q; recorded in all
        # modes so that the non-fib modes serve as a sensitivity control)
        nonconst = any(any(t[1] != lst[0][0] for t in lst) for lst in byCp.values())
        st['nc_any'] = st.get('nc_any', 0) + (1 if nonconst else 0)
        # (W4)
        if mode == 'fib':
            st['w4n'] += 1
            if eps != 0:
                st['w4eps'] += 1
            for wD, lst in byCp.items():
                mN = lst[0][0]
                if any(t[0] != mN for t in lst) or any(t[1] != mN for t in lst):
                    st['w4const'] += 1
                    break
    print(f"RESULT weighted p={p} n={n} H={H} H2={H2} mode={mode} samples={st['samples']}: "
          f"W1 fails={st['w1']}, W2 fails={st['w2']}, W3' (epst) fails={st.get('w3t', 0)} (max ratio {st.get('wt', 0.0):.4f}), W3 fails={st['w3']} (max lhs/(eps M^2)={worst:.4f}, "
          f"nontrivial={st['nontriv']}), slope-inheritance fails={st['inh']}, "
          f"W4 eps!=0: {st['w4eps']}/{st['w4n']}, W4 non-constant: {st['w4const']}/{st['w4n']}; "
          f"[control] samples with M_N2 non-constant on some C': {st.get('nc_any', 0)}/{st['samples']}")


if __name__ == "__main__":
    main()
