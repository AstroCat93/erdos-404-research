#!/usr/bin/env python3
"""Referee's own (from scratch) numerical test of Proposition 10.6(iii) (one-window identity at p=2)
and of the slope statistics of Obs 10.1.2.  Exact integer arithmetic on 2-adic integers truncated
at B bits (all valuations used are far below B).

mode 'window' n N L trials seed : for random even x with the hypotheses (W1)-(W3) and M_N<m,
   for every alive parent e of length n with slope lam<=L, compute for every state s mod 2^lam
   E_{x' in C} #{f : (e,f) alive at N at x', tau_N = s mod 2^lam}
   by exhaustive averaging over w mod 2^R (x' = x0 + 2^m (w + 2^R h), h random), R = D+lam+2,
   and compare with 2^(W_N-W_n) a_n^(lam)(s_e)  (exact rationals).
mode 'slopes' n count seed : histogram of slopes of alive paths at n for random even x.
"""
import sys, random
from fractions import Fraction
B = 600
MOD = 1 << B
def v2(z):
    z %= MOD
    if z == 0:
        return B
    return (z & -z).bit_length() - 1
def pis(x, n):
    """pi_j(x) mod 2^B and derivatives pi_j'(x), j=0..n"""
    P = [1]; dP = [0]
    for j in range(1, n + 1):
        P.append(P[-1] * (x + j) % MOD)
        dP.append((dP[-1] * (x + j) + P[-2]) % MOD)
    return P, dP
def alive_paths(x, n, P):
    """all words e of length n (e_0=1) alive at n: v(S_e(x)) >= V_n. returns list of (e, S)"""
    V = [v2(P[j]) for j in range(n + 1)]
    pop = [((1,), 1)]
    for j in range(1, n):
        nxt = []
        for e, S in pop:
            for b in (0, 1):
                S2 = (S + b * P[j]) % MOD
                if v2(S2) >= V[j + 1]:
                    nxt.append((e + (b,), S2))
        pop = nxt
    return pop
def S_of(e, P):
    return sum(P[j] for j, b in enumerate(e) if b) % MOD
def inv_odd(a, bits):
    return pow(a, -1, 1 << bits)
def tau(S, Pn, mbits):
    """-S/Pn as 2-adic integer mod 2^mbits (requires v(S)>=v(Pn))"""
    vp = v2(Pn)
    num = (-S) % MOD
    assert v2(num) >= vp or num == 0
    return ((num >> vp) * inv_odd(Pn >> vp, mbits)) % (1 << mbits)

def window(n, N, L, trials, seed):
    rnd = random.Random(seed)
    tested = exact = 0; skipped = 0; states = 0; slopes = {}
    while tested < trials:
        x = rnd.getrandbits(B - 50) * 2
        P, dP = pis(x, N + 2 * L + 4)
        V = [v2(P[j]) for j in range(len(P))]
        Mx = [0] + [max(v2(x + i) for i in range(1, j + 1)) for j in range(1, N + 1)]
        m = V[n]; D = V[N] - m; Mn = Mx[n]; MN = Mx[N]
        if not (N - n >= 2 * L + 2 and D + L <= m - Mn and L < m - MN and MN < m):
            skipped += 1; continue
        pars = alive_paths(x, n, P)
        cand = []
        for e, S in pars:
            dS = sum(dP[j] for j, b in enumerate(e) if b) % MOD
            lam = v2(dS)
            if lam <= L:
                cand.append((e, lam))
        if not cand:
            skipped += 1; continue
        tested += 1
        x0 = x % (1 << m)
        for e, lam in cand:
            slopes[lam] = slopes.get(lam, 0) + 1
            Sx = S_of(e, P)
            se = tau(Sx, P[n], lam + 1) % (1 << lam) if lam > 0 else 0
            # a_n^(lam)(t): distribution of sum_{i<2lam} f_i pi_{n+i}/pi_n mod 2^lam
            a = {}
            ratios = []
            acc = 1
            for i in range(2 * lam):
                if i: acc *= (x + n + i)
                ratios.append(acc)
            for f in range(1 << (2 * lam)):
                tot = sum(ratios[i] for i in range(2 * lam) if f >> i & 1)
                key = tot % (1 << lam) if lam > 0 else 0
                a[key] = a.get(key, 0) + 1
            pred = Fraction(2) ** ((N - V[N]) - (n - V[n])) * Fraction(a.get(se, 0), 1 << (2 * lam))
            R = D + lam + 2
            h = rnd.getrandbits(100)
            counts = {}
            for w in range(1 << R):
                xp = x0 + (1 << m) * (w + (h << R))
                Pp, _ = pis(xp, N)
                Sp = S_of(e, Pp)
                VN = v2(Pp[N])
                for f in range(1 << (N - n)):
                    S2 = Sp
                    for i in range(N - n):
                        if f >> i & 1:
                            S2 += Pp[n + i]
                    S2 %= MOD
                    if v2(S2) >= VN:
                        s = tau(S2, Pp[N], lam + 1) % (1 << lam) if lam > 0 else 0
                        counts[s] = counts.get(s, 0) + 1
            ok = all(Fraction(counts.get(s, 0), 1 << R) == pred for s in range(1 << lam))
            states += 1 << lam
            exact += ok
            if not ok:
                print("MISMATCH", n, N, L, lam, pred, {s: Fraction(cnt, 1 << R) for s, cnt in counts.items()})
    print(f"window n={n} N={N} L={L}: x tested={tested} skipped={skipped} parents={sum(slopes.values())} "
          f"exact={exact} parent-states={states} slopes={dict(sorted(slopes.items()))}")

def slopes(n, count, seed, residue=None):
    rnd = random.Random(seed)
    hist = {}; npaths = 0; nx = 0
    for _ in range(count):
        x = rnd.getrandbits(B - 50) * 2
        if residue is not None:
            r, mod = residue
            x = x - x % mod + r
        P, dP = pis(x, n)
        pop = alive_paths(x, n, P)
        if pop: nx += 1
        for e, S in pop:
            dS = sum(dP[j] for j, b in enumerate(e) if b) % MOD
            l = v2(dS); hist[l] = hist.get(l, 0) + 1; npaths += 1
    print(f"slopes n={n} x={count} (nonempty {nx}) residue={residue} paths={npaths} hist={dict(sorted(hist.items()))}")

if __name__ == '__main__':
    if sys.argv[1] == 'window':
        window(*map(int, sys.argv[2:7]))
    else:
        n, cnt, seed = map(int, sys.argv[2:5])
        res = (int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else None
        slopes(n, cnt, seed, res)
