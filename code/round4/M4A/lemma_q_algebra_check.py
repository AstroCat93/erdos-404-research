#!/usr/bin/env python3
"""lemma_q_algebra_check.py -- exact checks of the algebra inside the proof of Lemma Q (2D step) of
data/round4/reports/M4A.md, for random u, random full signed paths delta and random blocks, with t up to ~120
(levels far beyond what the brute-force DP of lemma_q_check.py can reach).  Exact rationals (H_c = sum 1/(u+i)).

For a block j-1 = [g, g+p) whose end gate g_j = g+p has depth 1, with L = V_g(u), y = u+g, alpha = (u+g+p)/p,
omega = pi_g(u)/p^L, tau = T_{<g}/p^L, N = sum_{i=1}^{p-1} 1/(y+i), it checks:
 (1) R_j^{<g_j} = R_{j-1}^{<g} - (1/alpha + p N) p^L tau - p^L (omega/alpha) Ztilde,
     where R_j^{<g'} = sum_{c<g'} delta_c pi_c(u) (p H_c(u) - p H_{g_j}(u)) and
     Ztilde = sum_k delta_{g+k} pi_k(y) (1 + (y+p) sum_{i=k+1}^{p-1} 1/(y+i));
 (2) Ztilde == sum_k delta_{g+k} pi_k(-p)  (mod p^2)   [as p-adic numbers];
 (3) every c >= g_j has v(pi_c(u) (p H_c - p H_{g_j})) >= L_j + 1;   and the same for the (unnormalised) function
     R_j = p T' - p H_{g_j} T: v(R_j - R_j^{<g_j}) >= L_j + 1;
 (4) the deep-end 1D step: if v(y+p) = s then pi_k(y) == pi_k(-p) mod p^s.
usage: lemma_q_algebra_check.py p SEED NTESTS tmax [CTRL]
CTRL=1: negative control (claims (2) and (3b) are tested one digit too strong: mod p^3 and >= L_j+2; failures expected).
"""
import random
import sys
from fractions import Fraction

from m4a_lib import vp

PREC = 60


def vq(fr, p):
    """p-adic valuation of a nonzero Fraction."""
    if fr == 0:
        return 10 ** 9
    return vp(fr.numerator, p) - vp(fr.denominator, p)


def main():
    p, seed, NT, tmax = (int(a) for a in sys.argv[1:5])
    ctrl = len(sys.argv) > 5 and sys.argv[5] == '1'
    e2, e3 = (3, 2) if ctrl else (2, 1)
    rnd = random.Random(seed)
    MOD = p ** PREC
    pk_m = [1]
    for k in range(1, p):
        pk_m.append(pk_m[-1] * (k - p))
    n1 = n2 = n3 = n4 = 0
    bad = 0
    tries = 0
    while n1 < NT and tries < 100 * NT:
        tries += 1
        u = rnd.randrange(MOD)
        if rnd.random() < 0.5:   # integer-like patterns with deep gates
            u = (rnd.randrange(p + 1, 300) * (1 if rnd.random() < 0.5 else -1) + p ** 45 * rnd.randrange(1, p ** 4)) % MOD
        t = rnd.randrange(3 * p, tmax)
        dep = [0] + [vp(u + i, p) for i in range(1, t + 1)]
        if max(dep) >= PREC - 5:
            continue
        gates = [g for g in range(1, t + 1) if dep[g] > 0]
        cands = [r for r in range(len(gates) - 1) if dep[gates[r + 1]] == 1 and gates[r + 1] <= t - 1]
        if not cands:
            continue
        r = rnd.choice(cands)
        g, gj = gates[r], gates[r + 1]
        assert gj == g + p
        delta = [1] + [rnd.choice((-1, 0, 0, 1)) for _ in range(1, t)]
        pi = [Fraction(1)]
        H = [Fraction(0)]
        for c in range(1, t + 1):
            pi.append(pi[-1] * (u + c))
            H.append(H[-1] + Fraction(1, u + c))
        L = sum(dep[1:g + 1])
        Lj = L + 1
        y = u + g
        alpha = Fraction(u + g + p, p)
        omega = pi[g] / p ** L
        Tg = sum(delta[c] * pi[c] for c in range(g))
        tau = Tg / p ** L
        Nn = sum(Fraction(1, y + i) for i in range(1, p))
        Rj = sum(delta[c] * pi[c] * (p * H[c] - p * H[gj]) for c in range(gj))
        Rjm1 = sum(delta[c] * pi[c] * (p * H[c] - p * H[g]) for c in range(g))
        Zt = Fraction(0)
        for k in range(p):
            Ek = sum(Fraction(1, y + i) for i in range(k + 1, p))
            pky = Fraction(1)
            for i in range(1, k + 1):
                pky *= (y + i)
            Zt += delta[g + k] * pky * (1 + (y + p) * Ek)
        lhs = Rj
        rhs = Rjm1 - (1 / alpha + p * Nn) * p ** L * tau - p ** L * (omega / alpha) * Zt
        ok1 = (lhs == rhs)
        n1 += 1
        Zm = sum(delta[g + k] * pk_m[k] for k in range(p))
        ok2 = vq(Zt - Zm, p) >= e2
        n2 += 1
        ok3 = all(vq(pi[c] * (p * H[c] - p * H[gj]), p) >= Lj + 1 for c in range(gj, t) if delta[c] != 0 or True)
        Tfull = sum(delta[c] * pi[c] for c in range(t))
        dT = sum(delta[c] * pi[c] * H[c] for c in range(t))
        Rfull = p * dT - p * H[gj] * Tfull
        ok3b = vq(Rfull - Rj, p) >= Lj + e3
        n3 += 1
        # (4): deep end gate check on some block
        ok4 = True
        for rr in range(len(gates) - 1):
            s = dep[gates[rr + 1]]
            yy = u + gates[rr]
            for k in range(p):
                a = 1
                for i in range(1, k + 1):
                    a = a * (yy + i) % p ** s
                if (a - pk_m[k]) % p ** s != 0:
                    ok4 = False
            n4 += 1
        if not (ok1 and ok2 and ok3 and ok3b and ok4):
            bad += 1
            if bad <= 3: print(f"FAIL u={u % p ** 10} t={t} g={g} ok1={ok1} ok2={ok2} ok3={ok3} ok3b={ok3b} ok4={ok4}")
    print(f"RESULT p={p} tmax={tmax} ctrl={ctrl}: identity (1) {n1} cases, (2) {n2}, (3) {n3}, (4) {n4} blocks; failures {bad}")


if __name__ == "__main__":
    main()
