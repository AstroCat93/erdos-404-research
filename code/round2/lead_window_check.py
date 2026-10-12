#!/usr/bin/env python3
"""lead_window_check.py -- the lead author's own exact test of Proposition 10.6(iii) of note_v2.md
(shares no code with track R1b's mart_check2.py / brute_window.py).  2026-10-12.

For random even x (2-adic, represented mod 2^PREC), times n < N, m = V_n(x), D = V_N(x) - m:
for every path e alive at n whose slope lam = v(S_e'(x)) satisfies the hypotheses
    N - n >= 2 lam,  D + lam <= m - M_n,  lam < m - M_N        ((W1)-(W3) with L = lam),
and for every state s mod 2^lam, compute EXACTLY (over all w mod 2^D, i.e. x_w = x mod 2^m + 2^m w
+ unchanged higher digits, and all f in {0,1}^(N-n))
    E_w #{f : (e,f) alive at N for x_w,  tau_N((e,f), x_w) == s mod 2^lam}
and compare with 2^(W_N - W_n) * a_n^(lam)(tau_n(e,x) mod 2^lam), where
    a_n^(lam)(t) = P_f( sum_{i<2 lam} f_i pi_{n+i}(x)/pi_n(x) == t mod 2^lam ).
Everything is integer arithmetic; aliveness is v(S_{(e,f)}(x_w)) >= V_N(x_w) evaluated directly.
usage: lead_window_check.py SEED NX n N
"""
import random
import sys
from fractions import Fraction

PREC = 512
MOD = 1 << PREC


def v2(a):
    a %= MOD
    if a == 0:
        return PREC
    return (a & -a).bit_length() - 1


def pis(x, N):
    """pi_0..pi_N and their derivatives at x, mod 2^PREC."""
    p = [1]
    dp = [0]
    for j in range(1, N + 1):
        dp.append((dp[-1] * (x + j) + p[-1]) % MOD)
        p.append(p[-1] * (x + j) % MOD)
    return p, dp


def V(x, n):
    return sum(v2(x + i) for i in range(1, n + 1))


def Mx(x, n):
    return max(v2(x + i) for i in range(1, n + 1))


def alive_paths(x, n):
    """all e (tuple, e_0 = 1) alive at n, by DFS with backward-integrality pruning."""
    p, _ = pis(x, n)
    Vs = [0] + [V(x, j) for j in range(1, n + 1)]
    out = []
    stack = [((1,), p[0])]
    while stack:
        e, S = stack.pop()
        j = len(e)
        if v2(S) < Vs[j]:
            continue
        if j == n:
            out.append(e)
            continue
        stack.append((e + (0,), S))
        stack.append((e + (1,), (S + p[j]) % MOD))
    return out


def main():
    seed, NX, n, N = (int(a) for a in sys.argv[1:5])
    rnd = random.Random(seed)
    tested = ok = 0
    done = tries = 0
    lamhist = {}
    while done < NX and tries < 100000:
        tries += 1
        x = rnd.getrandbits(300) & ~1
        m = V(x, n)
        D = V(x, N) - m
        Mn, MN = Mx(x, n), Mx(x, N)
        if D < 1 or D > 9 or MN >= m:
            continue
        p, dp = pis(x, N)
        par = []
        for e in alive_paths(x, n):
            S = sum(p[j] for j in range(n) if e[j]) % MOD
            Sd = sum(dp[j] for j in range(n) if e[j]) % MOD
            lam = v2(Sd)
            if N - n >= 2 * lam and D + lam <= m - Mn and lam < m - MN:
                tau = (-(S >> m) * pow((p[n] >> m) % MOD, -1, MOD)) % MOD   # tau_n = -S/pi_n (2-adic)
                par.append((e, lam, tau))
        if not par:
            continue
        done += 1
        WnN = (N - V(x, N)) - (n - m)
        x0 = x % (1 << m)
        hi = (x >> (m + D)) << (m + D)
        counts = {i: {} for i in range(len(par))}
        for w in range(1 << D):
            xw = x0 + (w << m) + hi
            pw, _ = pis(xw, N)
            VN = V(xw, N)
            for i, (e, lam, _) in enumerate(par):
                Se = sum(pw[j] for j in range(n) if e[j]) % MOD
                for f in range(1 << (N - n)):
                    S = (Se + sum(pw[n + k] for k in range(N - n) if (f >> k) & 1)) % MOD
                    if v2(S) < VN:
                        continue
                    if lam == 0:
                        st = 0
                    else:
                        tauN = (-(S >> VN) * pow((pw[N] >> VN) % MOD, -1, MOD)) % (1 << lam)
                        st = tauN
                    counts[i][st] = counts[i].get(st, 0) + 1
        for i, (e, lam, tau) in enumerate(par):
            lamhist[lam] = lamhist.get(lam, 0) + 1
            # a_n^(lam)(t) at x
            q = [1]
            for j in range(n + 1, n + 2 * lam):
                q.append(q[-1] * (x + j) % MOD)
            hits = {}
            for f in range(1 << (2 * lam)):
                t = sum(q[k] for k in range(2 * lam) if (f >> k) & 1) % (1 << lam) if lam else 0
                hits[t] = hits.get(t, 0) + 1
            a = Fraction(hits.get(tau % (1 << lam) if lam else 0, 0), 1 << (2 * lam))
            rhs = Fraction(2) ** WnN * a
            good = True
            for s in range(1 << lam):
                lhs = Fraction(counts[i].get(s, 0), 1 << D)
                tested += 1
                if lhs != rhs:
                    good = False
            ok += good
        print(f"x#{done}: m={m} D={D} M_n={Mn} M_N={MN} parents={len(par)} lams={sorted(set(l for _, l, _ in par))}", flush=True)
    print(f"LEAD CHECK Prop 10.6(iii): (parent,state) identities tested={tested}; parents all-states-exact={ok}/"
          f"{sum(lamhist.values())}; lambda histogram {dict(sorted(lamhist.items()))}")


if __name__ == "__main__":
    main()
