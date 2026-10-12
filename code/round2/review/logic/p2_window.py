#!/usr/bin/env python3
"""Referee's independent test of Proposition 10.6(iii) (one-window identity, slope <= L) and of
Prop 10.6(i) slope inheritance, written from the statement in note_v2.md §10.1 only.

x is a 2-adic integer represented by a B-bit integer (B large); all valuations used are < B.
Alive paths at n are built by incremental extension (backward integrality).
For each parent e in P^{1,L}_n(x) and each state s mod 2^lam, we compute exactly
   LHS(s) = E_{x' in x+2^m Z_2} #{f in {0,1}^{N-n}: (e,f) alive at N at x', tau_N == s mod 2^lam}
by averaging over all w mod 2^D (higher digits of w random, to test they do not matter),
and compare with RHS = 2^{W_N-W_n} a_n^{(lam)}(s_e).
Usage: p2_window.py SEED NTRIALS
"""
import random
import sys
from fractions import Fraction

B = 600
MOD = 1 << B


def v2(z):
    z %= MOD
    if z == 0:
        return B
    return (z & -z).bit_length() - 1


def pis(x, N):
    """pi_j(x), pi_j'(x) for j=0..N, mod 2^B"""
    P = [1]; dP = [0]
    for j in range(1, N + 1):
        P.append(P[-1] * (x + j) % MOD)
        dP.append((dP[-1] * (x + j) + P[-2]) % MOD)
    return P, dP


def alive_paths(x, n):
    """list of (word, S, S') for words of length n alive at n"""
    P, dP = pis(x, n)
    V = [v2(P[j]) for j in range(n + 1)]
    pop = [((1,), 1, 0)]  # length-1 word e0=1, S = pi_0 = 1; alive at 1 iff v(1) >= V_1
    pop = [q for q in pop if v2(q[1]) >= V[1]]
    for j in range(1, n):
        new = []
        for (w, S, dS) in pop:
            for b in (0, 1):
                S2 = (S + b * P[j]) % MOD
                if v2(S2) >= V[j + 1]:
                    new.append((w + (b,), S2, (dS + b * dP[j]) % MOD))
        pop = new
    return pop, V


def test_once(rng, L):
    # random even x; many random bits
    x = rng.getrandbits(B) & ~1
    n = rng.randint(24, 40)
    P, dP = pis(x, n + 40)
    V = [v2(P[j]) for j in range(len(P))]
    Mx = lambda k: max(v2(x + i) for i in range(1, k + 1))
    m = V[n]
    W = lambda k: k - V[k]
    results = []
    for N in range(n + 2 * L + 2, n + 2 * L + 8):
        D = V[N] - m
        if not (Mx(N) < m and D + L <= m - Mx(n) and L < m - Mx(N)):
            continue
        if D > 10:
            continue
        pop, _ = alive_paths(x, n)
        par = [(w, S, dS) for (w, S, dS) in pop if v2(dS) <= L]
        if not par:
            return None
        x0 = x % (1 << m)
        nw = 1 << D
        for (w_e, S_e_x, dS_e_x) in par:
            lam = v2(dS_e_x)
            # RHS
            ratio = [1]
            for i in range(1, 2 * lam):
                ratio.append(ratio[-1] * (x + n + i) % MOD)
            cnt = {}
            for f in range(1 << (2 * lam)):
                tsum = sum(ratio[i] for i in range(2 * lam) if f >> i & 1) % (1 << lam)
                cnt[tsum] = cnt.get(tsum, 0) + 1
            # s_e = tau_n(e,x) mod 2^lam
            tau_n = (-S_e_x * pow(P[n] >> m, -1, MOD)) % MOD  # tau = -S/pi_n ; S divisible by 2^m
            tau_n = ((-(S_e_x >> m)) * pow(P[n] >> m, -1, MOD)) % MOD
            s_e = tau_n % (1 << lam)
            a_s = Fraction(cnt.get(s_e, 0), 1 << (2 * lam))
            rhs = Fraction(2) ** (W(N) - W(n)) * a_s
            # LHS: average over w mod 2^D
            lhs = [Fraction(0)] * (1 << lam)
            for wl in range(nw):
                w = wl + (rng.getrandbits(B) << D)
                xp = (x0 + (w << m)) % MOD
                Pp, dPp = pis(xp, N)
                Se = sum(Pp[j] for j in range(n) if w_e[j]) % MOD
                dSe = sum(dPp[j] for j in range(n) if w_e[j]) % MOD
                VN = v2(Pp[N])
                assert VN == V[N] and v2(Pp[n]) == m
                for f in range(1 << (N - n)):
                    S = Se
                    dS = dSe
                    for k in range(N - n):
                        if f >> k & 1:
                            S += Pp[n + k]; dS += dPp[n + k]
                    S %= MOD
                    if v2(S) >= VN:
                        # slope inheritance (Prop 10.6(i))
                        assert v2(dS) == lam, ("slope changed", lam, v2(dS))
                        tauN = ((-(S >> VN)) * pow(Pp[N] >> VN, -1, MOD)) % (1 << max(lam, 1))
                        lhs[tauN % (1 << lam)] += Fraction(1, nw)
            ok = all(l == rhs for l in lhs)
            results.append((n, N, D, lam, ok, [str(l) for l in lhs], str(rhs)))
        return results
    return None


def main():
    seed = int(sys.argv[1]); trials = int(sys.argv[2])
    rng = random.Random(seed)
    tot = good = 0
    lamseen = {}
    for _ in range(trials):
        L = rng.choice([2, 3, 4])
        r = test_once(rng, L)
        if not r:
            continue
        for (n, N, D, lam, ok, lhs, rhs) in r:
            tot += 1; good += ok
            lamseen[lam] = lamseen.get(lam, 0) + 1
            if not ok:
                print("MISMATCH", n, N, D, lam, lhs, rhs)
    print(f"parents tested {tot}, identity exact {good}; slopes seen {sorted(lamseen.items())}")


if __name__ == '__main__':
    main()
