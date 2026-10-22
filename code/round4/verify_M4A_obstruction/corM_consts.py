"""corM_consts.py -- the universal block constants of M4A's Lemma Q at the primes of Corollary M', recomputed
with this track's own code (no M4A code imported), and read through the obstructions.

Usage:
  python3 corM_consts.py consts P1 P2 ...      # exact constants at the listed primes (p <= 31)
  python3 corM_consts.py survey PMIN PMAX      # sign of M4A's asymptotic rate c at every prime in [PMIN, PMAX]

Definitions (data/round4/reports/M4A.md s.4-5): zeta_k i.i.d. signed (P(0)=1/2, P(+-1)=1/4),
  Z = sum_{k<p} zeta_k pi_k(-p),  q_s = p^s max_z P(Z == z mod p^s),
  P_0(g,s) = P(1 + sum_{1<=c<g} zeta_c pi_c(-g) == 0 mod p^s)   (1 <= g <= p),
  q~_s = q_s (s <= S), q_S p^(s-S) (s > S);  rho_1 = (1-1/p) sum_{s>=1} log q~_s / p^(s-1)
       (= log q_1 + sum_{s>=2} (log q~_s - log q~_{s-1}) / p^(s-1), summation by parts);
  gamma = log q_1 - log(q_2/p);  kappa = (p-1) log 2 - log p + rho_1 - gamma (p-1)^2/p^2;
  c = gamma (p-1)(r-1)/(2p^2) - (r^2-1) rho_1/(p-1),  r = 27/20.
M4A uses S = 8 for p <= 13 and S = 4 for p > 13.  rho_1 is non-increasing in S (q~^(S) >= q~^(S') pointwise for
S < S', since q_s <= p q_{s-1}), so rho_1 computed with a smaller S is an upper bound and c a lower bound.

Obstruction reading:
  q_1 > 1 strictly (weights are multiples of 4^-p, p does not divide 4^p): the value-only (supremum-type)
      per-level factor never decays -- the Lemma Q analogue of Cor 10.20 / Prop 11.24.
  q_2/p < 1: the only per-level gain, available only for the joint value+slope event after Theorem 1.
  P_0(2,s) = 1/4 for every s: the double root (y+2)^2 of Prop 11.15(b), at every p.
  q_s / p^s -> max atom of Z (exact integer law) > 0: cost ~ p^s at a depth-s gate (no depth-uniform
      deterministic bound; Theorem 3.10 / Prop 11.23).
Weights are exact integers: numpy int64 for p <= 31 (4^p < 2^63), Python ints (object arrays) beyond.
"""
import math
import sys
from fractions import Fraction

import numpy as np
import mpmath as mp

mp.mp.dps = 40
R = Fraction(27, 20)


def primes(a, b):
    return [q for q in range(max(a, 3), b + 1) if all(q % d for d in range(2, int(q ** 0.5) + 1))]


def signed_law(vals, mod, start=0, obj=False):
    """integer weights (total 4^len(vals)) of start + sum zeta_k vals[k] mod `mod`."""
    cnt = np.zeros(mod, dtype=object if obj else np.int64)
    cnt[start % mod] = 1
    for a in vals:
        a %= mod
        cnt = 2 * cnt + np.roll(cnt, a) + np.roll(cnt, -a)
    return cnt


def pis(p, at, upto):
    """pi_k(at) = (at+1)...(at+k) for k = 0..upto-1 (exact integers)."""
    out = [1]
    for k in range(1, upto):
        out.append(out[-1] * (at + k))
    return out


def qs_from_law(cnt, p, S, tot):
    out = [Fraction(1)]
    for s in range(1, S + 1):
        folded = cnt.reshape(-1, p ** s).sum(axis=0)
        out.append(Fraction(p ** s * int(folded.max()), tot))
    return out


def derived(p, q, S):
    """rho_1, gamma, kappa, rate c (mpmath) from q[1..S] (Fractions)."""
    P = mp.mpf(p)
    lq = [None] + [mp.log(mp.mpf(x.numerator) / x.denominator) for x in q[1:S + 1]]
    rho = lq[1]
    for s in range(2, S + 1):
        rho += (lq[s] - lq[s - 1]) / P ** (s - 1)
    rho += mp.log(P) * P ** (-S) / (1 - 1 / P)
    gamma = lq[1] - (lq[2] - mp.log(P))
    kappa = (p - 1) * mp.log(2) - mp.log(P) + rho - gamma * (P - 1) ** 2 / P ** 2
    r = mp.mpf(R.numerator) / R.denominator
    c = gamma * (P - 1) * (r - 1) / (2 * P ** 2) - (r ** 2 - 1) * rho / (P - 1)
    return rho, gamma, kappa, c


def consts(plist):
    for p in plist:
        assert p <= 31
        tot = 4 ** p
        S = max(s for s in range(1, 9) if p ** s <= 2 * 10 ** 6)
        vals = pis(p, -p, p)                     # pi_k(-p), k = 0..p-1
        law = signed_law(vals, p ** S)
        assert int(law.sum()) == tot
        q = qs_from_law(law, p, S, tot)
        line = ", ".join(f"q_{s}={float(q[s]):.9f}" for s in range(1, S + 1))
        print(f"p={p}: own DP mod p^{S}: {line}")
        print(f"      exact: q_1 = {q[1]}  q_2 = {q[2]}")
        mono = all(q[s - 1] <= q[s] <= p * q[s - 1] for s in range(2, S + 1))
        print(f"      q_1 > 1: {q[1] > 1};  q_2/p = {float(q[2] / p):.6f} < 1: {q[2] < p};  q_(s-1) <= q_s <= p q_(s-1) for s <= {S}: {mono}")
        if p <= 13:   # exact integer law of Z by full enumeration (vectorised): q_s for s <= 8 and the max atom
            Z = np.zeros(1, dtype=np.int64)
            W = np.ones(1, dtype=np.int64)
            for a in vals:
                Z = np.concatenate([Z - a, Z, Z + a])
                W = np.concatenate([W, 2 * W, W])
            uz, inv = np.unique(Z, return_inverse=True)
            wz = np.zeros(len(uz), dtype=np.int64)
            np.add.at(wz, inv, W)
            maxatom = Fraction(int(wz.max()), tot)
            qe = [Fraction(1)]
            for s in range(1, 9):
                _, inv2 = np.unique(np.mod(uz, p ** s), return_inverse=True)
                F = np.zeros(inv2.max() + 1, dtype=np.int64)
                np.add.at(F, inv2, wz)
                qe.append(Fraction(p ** s * int(F.max()), tot))
            assert all(qe[s] == q[s] for s in range(1, S + 1)), p
            print(f"      full enumeration of 3^{p} configurations: equals the DP for q_1..q_{S}: True; "
                  + ", ".join(f"q_{s}={float(qe[s]):.6g}" for s in range(S + 1, 9)))
            print(f"      max atom of Z = {maxatom} = {float(maxatom):.6g};  q_8/p^8 = {float(qe[8] / p ** 8):.6g}"
                  f"  (q_s/p^s decreases to the max atom: a depth-s gate costs ~ p^s * {float(maxatom):.3g})")
            q = qe
            S = 8
        # block 0
        S0 = min(S, 6)
        S0 = max(s_ for s_ in range(1, S0 + 1) if p ** s_ <= 2 * 10 ** 6)
        rows = {}
        for g in range(1, p + 1):
            v = pis(p, -g, g)                    # pi_c(-g), c = 0..g-1
            lw = signed_law(v[1:], p ** S0, start=1)
            T = 4 ** (g - 1)
            rows[g] = [Fraction(int(lw.reshape(-1, p ** s).sum(axis=0)[0]), T) for s in range(0, S0 + 1)]
            if g >= 3:
                assert all(x % (g - 1) == 0 for x in v[1:])   # sum == 1 mod (g-1): never exactly 0
        print(f"      P_0(2,s) = 1/4 for s = 1..{S0}: {all(rows[2][s] == Fraction(1, 4) for s in range(1, S0 + 1))};"
              f"  P_0(1,s)=0: {all(rows[1][s] == 0 for s in range(1, S0 + 1))};  for g >= 3 the block-0 sum is == 1 mod (g-1), never 0")
        big = [(g, float(rows[g][S0])) for g in range(3, p + 1) if rows[g][S0] > 0]
        print(f"      P_0(g,{S0}) > 0 for g >= 3: {big if big else 'none'}")
        Sm = 8 if p <= 13 else 4
        rho, gamma, kappa, c = derived(p, q, Sm)
        print(f"      with M4A's S={Sm}: rho_1={mp.nstr(rho, 7)} gamma={mp.nstr(gamma, 7)} kappa={mp.nstr(kappa, 7)} > 0: {kappa > 0};"
              f"  rate c={mp.nstr(c, 6)} > 0: {c > 0}  (c/2 = {mp.nstr(c / 2, 6)})")


def survey(pmin, pmax):
    worst = None
    for p in primes(pmin, pmax):
        obj = p > 31
        tot = 4 ** p
        vals = pis(p, -p, p)
        law = signed_law(vals, p ** 2, obj=obj)
        q = qs_from_law(law, p, 2, tot)
        rho, gamma, kappa, c = derived(p, q, 2)
        print(f"p={p:3d}: q_1={float(q[1]):.8f} q_2={float(q[2]):.6f} q_2/p={float(q[2] / p):.5f}  rho_1(S=2)<={mp.nstr(rho, 5)}"
              f"  gamma={mp.nstr(gamma, 5)}  kappa>={mp.nstr(kappa, 5)}  rate c>={mp.nstr(c, 5)}  c>0: {c > 0}")
        if worst is None or c < worst[1]:
            worst = (p, c)
    print(f"survey [{pmin},{pmax}]: smallest lower bound for c at p={worst[0]}: {mp.nstr(worst[1], 6)}")


if __name__ == '__main__':
    if sys.argv[1] == 'consts':
        consts([int(a) for a in sys.argv[2:]])
    else:
        survey(int(sys.argv[2]), int(sys.argv[3]))
