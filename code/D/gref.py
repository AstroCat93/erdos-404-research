#!/usr/bin/env python3
"""Reference (big-int) computation of g(a,p) = f(a,p) - v_p(a!), capped at M.

c-recursion: for A with min A = a, put S_N = sum_{n in A, n<N} n! and c_N = S_N / N!.
Then c_{N+1} = (c_N + eps_N)/(N+1), eps_a = 1, eps_N in {0,1}.
f(a,p) >= v_p(a!) + M  iff some choice keeps c_N p-integral up to the last N
with v_p(N!/a!) <= M, and then c_N + eps_N == 0 mod p^{remaining}.
We keep c_N modulo p^{r_N}, r_N = M - v_p(N!/a!).

Returns (g, witness_or_None) where g == M means 'g >= M'.
"""
import sys


def vp(n, p):
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def g_capped(a, p, M, want_witness=False):
    # population: dict residue -> one witness set (tuple) (only if want_witness)
    r = M
    pop = {0: (a,) if want_witness else None}
    N = a
    vacc = 0  # v_p(N!/a!)
    while True:
        t = vp(N + 1, p)
        u = (N + 1) // p ** t
        eps_choices = (1,) if N == a else (0, 1)
        if t >= r:
            # success test: c + eps == 0 mod p^r
            mod = p ** r
            for c, w in pop.items():
                for e in eps_choices:
                    if (c + e) % mod == 0:
                        wit = None
                        if want_witness:
                            wit = w if (e == 0 or N == a) else w + (N,)
                        return M, wit
            # death: best valuation
            best = -1
            for c in pop:
                for e in eps_choices:
                    x = (c + e) % mod
                    best = max(best, vp(x, p) if x else r)
            return vacc + best, None
        mod_new = p ** (r - t)
        inv = pow(u, -1, mod_new)
        newpop = {}
        pt = p ** t
        for c, w in pop.items():
            for e in eps_choices:
                x = c + e
                if x % pt == 0:
                    nc = ((x // pt) * inv) % mod_new
                    if nc not in newpop:
                        if want_witness:
                            newpop[nc] = w if (e == 0 or N == a) else w + (N,)
                        else:
                            newpop[nc] = None
        if not newpop:
            mod = p ** r
            best = -1
            for c in pop:
                for e in eps_choices:
                    x = (c + e) % mod
                    best = max(best, vp(x, p) if x else r)
            return vacc + best, None
        pop = newpop
        r -= t
        vacc += t
        N += 1


def check_witness(w, p):
    from math import factorial
    s = sum(factorial(n) for n in w)
    return vp(s, p)


if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    M = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    from math import factorial
    for a in range(1, 17):
        g, w = g_capped(a, p, M, want_witness=True)
        va = vp(factorial(a), p)
        msg = f"a={a} g={g} f={'>=' if g==M else ''}{va+g}"
        if w is not None:
            msg += f" witness_v={check_witness(w,p)} len={len(w)}"
        print(msg, flush=True)
