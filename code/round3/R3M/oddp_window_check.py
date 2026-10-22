#!/usr/bin/env python3
"""oddp_window_check.py -- exact, state-by-state test of the odd-p one-window identity
(Proposition R3M-A of data/round3/reports/R3M.md; the odd-p analogue of note.md Prop 10.6).

For a prime p, random x in Z_p (PREC random base-p digits), times n < N, m = V_n(x), D = V_N(x) - m:
for every path e (e_0 = 1) alive at n whose slope lam = v_p(S_e'(x)) satisfies, with L = lam,
    (W1) N - n >= p*L,   (W2) D + L <= m - M_n,   (W3) L < m - M_N,
and for every state s mod p^lam, compute EXACTLY (over all w mod p^D, x_w = (x mod p^m) + p^m w
+ unchanged digits >= m + D, and all f in {0,1}^(N-n))
    LHS(s) = p^-D * #{(w, f) : (e,f) alive at N for x_w, tau_N((e,f), x_w) == s mod p^lam}
and compare with
    RHS    = 2^(N-n) p^-D a_n^(lam)(tau_n(e,x) mod p^lam),
    a_n^(lam)(t) = P_{f in {0,1}^(p lam)} ( sum_{i < p lam} f_i pi_{n+i}(x)/pi_n(x) == t mod p^lam ).
Also checks slope inheritance (every child has slope lam) and that the parent set, lam and
tau_n mod p^lam do not depend on w.  Aliveness is decided by direct evaluation of
v_p(S_{(e,f)}(x_w)) >= V_N(x_w) on integers mod p^PREC.

usage: oddp_window_check.py p SEED NX n N [DMAX [MAXPAR]]
MAXPAR (default unlimited): for each x keep at most MAXPAR parents of each slope value (random choice).
Written for round 3 (track R3M); shares no code with code/round2/R1b/*.py or lead_window_check.py.
"""
import random
import sys
from fractions import Fraction

PREC = 120  # base-p digits carried


def vp(a, p, MOD):
    a %= MOD
    if a == 0:
        return PREC
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def main():
    p, seed, NX, n, N = (int(a) for a in sys.argv[1:6])
    DMAX = int(sys.argv[6]) if len(sys.argv) > 6 else 5
    MAXPAR = int(sys.argv[7]) if len(sys.argv) > 7 else 10 ** 9
    MOD = p ** PREC
    rnd = random.Random(seed)

    def prods(x, upto):
        """pi_0..pi_upto and derivatives pi_j' at x, mod p^PREC."""
        P = [1]
        dP = [0]
        for j in range(1, upto + 1):
            dP.append((dP[-1] * (x + j) + P[-1]) % MOD)
            P.append(P[-1] * (x + j) % MOD)
        return P, dP

    def Vlist(x, upto):
        out = [0]
        for i in range(1, upto + 1):
            out.append(out[-1] + vp(x + i, p, MOD))
        return out

    def alive(x, n_):
        P, _ = prods(x, n_)
        Vs = Vlist(x, n_)
        res = []
        stack = [((1,), 1)]
        while stack:
            e, S = stack.pop()
            j = len(e)
            if vp(S, p, MOD) < Vs[j]:
                continue
            if j == n_:
                res.append(e)
                continue
            stack.append((e + (0,), S))
            stack.append((e + (1,), (S + P[j]) % MOD))
        return res

    tested_states = 0
    parents_ok = 0
    parents_tot = 0
    inherit_fail = 0
    const_fail = 0
    lamhist = {}
    done = tries = 0
    while done < NX and tries < 200000:
        tries += 1
        x = rnd.randrange(MOD)
        Vs = Vlist(x, N)
        m = Vs[n]
        D = Vs[N] - m
        Mn = max(vp(x + i, p, MOD) for i in range(1, n + 1))
        MN = max(vp(x + i, p, MOD) for i in range(1, N + 1))
        if D < 1 or D > DMAX or MN >= m:
            continue
        P, dP = prods(x, N)
        par = []
        for e in alive(x, n):
            S = sum(P[j] for j in range(n) if e[j]) % MOD
            Sd = sum(dP[j] for j in range(n) if e[j]) % MOD
            lam = vp(Sd, p, MOD)
            L = lam
            if N - n >= p * L and D + L <= m - Mn and L < m - MN:
                tau = (-(S // p ** m) * pow((P[n] // p ** m) % MOD, -1, MOD)) % MOD
                par.append((e, lam, tau))
        if MAXPAR < 10 ** 9:
            bylam = {}
            for item in par:
                bylam.setdefault(item[1], []).append(item)
            par = []
            for lam_, items in sorted(bylam.items()):
                rnd.shuffle(items)
                par.extend(items[:MAXPAR])
        if not par:
            continue
        done += 1
        x0 = x % p ** m
        hi = (x // p ** (m + D)) * p ** (m + D)
        cnt = [dict() for _ in par]
        for w in range(p ** D):
            xw = x0 + w * p ** m + hi
            Pw, dPw = prods(xw, N)
            Vw = Vlist(xw, N)
            if Vw[n] != m or Vw[N] != m + D:
                const_fail += 1
            if w < 2:
                al = set(alive(xw, n))
                if any(e not in al for e, _, _ in par):
                    const_fail += 1
            # subset sums of the window, and of the derivative window
            sums = [(0, 0)]
            for k in range(N - n):
                yk, dyk = Pw[n + k], dPw[n + k]
                sums = sums + [((s + yk) % MOD, (sd + dyk) % MOD) for (s, sd) in sums]
            # index of sums: bit k of the list index <-> f_k (by construction of the doubling)
            for i, (e, lam, tau) in enumerate(par):
                Se = sum(Pw[j] for j in range(n) if e[j]) % MOD
                Sde = sum(dPw[j] for j in range(n) if e[j]) % MOD
                if w < 2:
                    lam_w = vp(Sde, p, MOD)
                    tau_w = (-(Se // p ** m) * pow((Pw[n] // p ** m) % MOD, -1, MOD)) % MOD
                    if lam_w != lam or (tau_w - tau) % p ** lam != 0:
                        const_fail += 1
                for (s, sd) in sums:
                    S = (Se + s) % MOD
                    if vp(S, p, MOD) < Vw[N]:
                        continue
                    if vp((Sde + sd) % MOD, p, MOD) != lam:
                        inherit_fail += 1
                    tauN = (-(S // p ** Vw[N]) * pow((Pw[N] // p ** Vw[N]) % MOD, -1, MOD)) % p ** lam if lam else 0
                    cnt[i][tauN] = cnt[i].get(tauN, 0) + 1
        for i, (e, lam, tau) in enumerate(par):
            parents_tot += 1
            lamhist[lam] = lamhist.get(lam, 0) + 1
            # frozen-state weight a_n^(lam)(tau mod p^lam)
            q = [1]
            for j in range(n + 1, n + p * lam):
                q.append(q[-1] * (x + j) % MOD)
            hits = {}
            for f in range(1 << (p * lam)):
                t = sum(q[k] for k in range(p * lam) if (f >> k) & 1) % (p ** lam)
                hits[t] = hits.get(t, 0) + 1
            a = Fraction(hits.get(tau % p ** lam, 0), 1 << (p * lam))
            rhs = Fraction(2 ** (N - n), p ** D) * a
            good = True
            for s in range(p ** lam):
                tested_states += 1
                if Fraction(cnt[i].get(s, 0), p ** D) != rhs:
                    good = False
                    print("MISMATCH", "x mod p^m+D =", x % p ** (m + D), "lam", lam, "s", s,
                          Fraction(cnt[i].get(s, 0), p ** D), rhs)
            parents_ok += good
        print(f"x#{done}: m={m} D={D} M_n={Mn} M_N={MN} parents={len(par)} "
              f"lams={sorted(set(l for _, l, _ in par))}", flush=True)
    print(f"RESULT p={p} n={n} N={N}: (parent,state) identities tested={tested_states}; "
          f"parents with all states exact={parents_ok}/{parents_tot}; inheritance failures={inherit_fail}; "
          f"constancy failures={const_fail}; lambda histogram {dict(sorted(lamhist.items()))}")


if __name__ == "__main__":
    main()
