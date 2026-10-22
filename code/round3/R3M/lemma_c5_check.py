#!/usr/bin/env python3
"""lemma_c5_check.py -- exact check of the decomposition (Lemma R3M-C5) of the fine-scale mass
eps(W, W') of a composite window [n, N') = [n, N) u [N, N') through the SIGNED carry process:

   eps = p^K Coll_K - p^D Coll_D            (K = V_N' - V_n, D = V_N - V_n)
       = c_N'/c_n - c_N/c_n + sum_{n<=j<N} (c_j/(2 c_n)) [Lam_{N'-j}(x+j) - Lam_{N-j}(x+j)]
                            + sum_{N<=j<N'} (c_j/(2 c_n)) Lam_{N'-j}(x+j),
   c_t = 2^-t p^{V_t(x)},  Lam_t(y) = p^{V_t(y)} * P_delta( 1 + sum_{1<=c<t} delta_c pi_c(y) == 0 mod p^{V_t(y)} ),
   delta_c i.i.d. with P(0) = 1/2, P(+1) = P(-1) = 1/4.
Both sides are computed in exact rational arithmetic (residue-distribution DPs with integer weights).
usage: lemma_c5_check.py p SEED NX n H H2 [KMAX]
"""
import random
import sys
from fractions import Fraction

PREC = 120


def vp(a, p):
    if a == 0:
        return PREC
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def coll(elems, p, K):
    mod = p ** K
    dist = {0: 1}
    for y in elems:
        y %= mod
        new = dict(dist)
        for r, c in dist.items():
            r2 = (r + y) % mod
            new[r2] = new.get(r2, 0) + c
        dist = new
    T = 2 ** len(elems)
    return Fraction(sum(c * c for c in dist.values()), T * T)


def signed_Lam(y, t, p):
    """Lam_t(y) exactly: p^{V_t(y)} * P(1 + sum_{1<=c<t} d_c pi_c(y) == 0 mod p^{V_t(y)})."""
    V = sum(vp(y + i, p) for i in range(1, t + 1))
    mod = p ** V
    dist = {1 % mod: 1}  # weights: total 4^(t-1)
    pc = 1
    for c in range(1, t):
        pc = pc * (y + c) % mod
        new = {}
        for r, w in dist.items():
            new[r] = new.get(r, 0) + 2 * w
            r1 = (r + pc) % mod
            new[r1] = new.get(r1, 0) + w
            r2 = (r - pc) % mod
            new[r2] = new.get(r2, 0) + w
        dist = new
    return Fraction(p ** V * dist.get(0, 0), 4 ** (t - 1))


def main():
    p, seed, NX, n, H, H2 = (int(a) for a in sys.argv[1:7])
    KMAX = int(sys.argv[7]) if len(sys.argv) > 7 else 8
    N, N2 = n + H, n + H + H2
    MOD = p ** PREC
    rnd = random.Random(seed)
    done = ok = tries = 0
    while done < NX and tries < 100000:
        tries += 1
        x = rnd.randrange(MOD)
        V = [0]
        for i in range(1, N2 + 1):
            V.append(V[-1] + vp((x + i) % MOD, p))
        D = V[N] - V[n]
        K = V[N2] - V[n]
        if K > KMAX or D < 1:
            continue
        done += 1
        elems = []
        y = 1
        for k in range(N2 - n):
            elems.append(y)
            y = y * (x + n + k + 1) % MOD
        eps = p ** K * coll(elems, p, K) - p ** D * coll(elems, p, D)
        c = lambda t: Fraction(p ** V[t], 2 ** t)
        rhs = c(N2) / c(n) - c(N) / c(n)
        for j in range(n, N):
            rhs += c(j) / (2 * c(n)) * (signed_Lam(x + j, N2 - j, p) - signed_Lam(x + j, N - j, p))
        for j in range(N, N2):
            rhs += c(j) / (2 * c(n)) * signed_Lam(x + j, N2 - j, p)
        good = (eps == rhs)
        ok += good
        print(f"x#{done}: D={D} K={K} eps={float(eps):.6f} decomposition={float(rhs):.6f} exact_equal={good}", flush=True)
    print(f"RESULT p={p} n={n} H={H} H2={H2}: Lemma C5 identity exact in {ok}/{done} samples")


if __name__ == "__main__":
    main()
