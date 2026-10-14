"""fe_lib.py -- rigorous (outward-rounded interval) evaluation of the bounds of track M4A, round 4
(data/round4/reports/M4A.md):

  Prop D  : p^top Coll_top <= blocklevel(top, th=0)       (pointwise; gives eps <= p^K Coll_K - 1, chi^2 <= p^D Coll_D - 1)
  Prop E  : E_B[eps] <= blocklevel(top=K, th=theta)        (B a ball of radius p^-b with constant gate pattern)
  Prop E' : E_B[eps] <= Eprime(K, H, f', sigma)            (closed form; only needs K, H, f' = min(theta, K - sigma),
                                                            and sigma >= every gate depth in the composite window)
Interval arithmetic: mpmath.iv at 200 bits; every returned bound is the upper endpoint of an interval that contains
the exact value of the formula.  The formulas are those of bounds.py (exact Fractions), which bounds_check.py tests
against exact collision computations.
"""
import math
from fractions import Fraction

from mpmath import iv, mpf

from bounds import qconsts, block0_table, qconsts_dp, block0_table_dp

iv.prec = 200


def I(x):
    if isinstance(x, int):
        return iv.mpf(x)
    return iv.mpf(x.numerator) / iv.mpf(x.denominator)


def up(x):
    """upper endpoint of an interval, as an mpf."""
    return mpf(x.b)


class Consts:
    def __init__(self, p, S=8, S0=12):
        self.p = p
        self.S = S
        self.S0 = S0
        if p <= 13:
            self.q = qconsts(p, S)
            self.P0 = block0_table(p, S0)
        else:   # residue DPs (validated against the enumerations for p <= 13 by qdp_check.py)
            self.S = S = min(S, 4)
            self.S0 = S0 = min(S0, 4)
            self.q = qconsts_dp(p, S)
            self.P0 = block0_table_dp(p, S0)
        self.qI = [I(x) for x in self.q]
        self.P0I = {g: [I(x) for x in row] for g, row in self.P0.items()}
        P = iv.mpf(p)
        self.logq = [None] + [iv.log(self.qI[s]) for s in range(1, S + 1)]
        # q~_s = q_s (s <= S), q_S p^(s-S) (s > S): Delta_s = log q~_s - log q~_{s-1}
        rho = self.logq[1]
        for s in range(2, S + 1):
            rho += (self.logq[s] - self.logq[s - 1]) / P ** (s - 1)
        rho += iv.log(P) * P ** (-S) / (1 - 1 / P)
        self.rho1 = rho
        self.gamma = self.logq[1] - iv.log(self.qI[2] / P)
        self.kappa = (p - 1) * iv.log(iv.mpf(2)) - iv.log(P) + self.rho1 - self.gamma * iv.mpf(p - 1) ** 2 / P ** 2

    def qt(self, s):
        if s <= self.S:
            return self.qI[s]
        return self.qI[self.S] * iv.mpf(self.p) ** (s - self.S)

    def logqt(self, s):
        if s <= self.S:
            return self.logq[s]
        return self.logq[self.S] + (s - self.S) * iv.log(iv.mpf(self.p))


def blocklevel(C, depth, V, n, N2, top, th, MW):
    """Upper bound (interval) for p^top [2^-H + sum_{c<H} 2^{-c-1} P0(g1,min(s1,top-a_c)) Suf(first block)]
    = the Prop D bound (th <= 0) or the Prop E bound (th >= 1, with f' = min(th, top - MW)).
    depth[i] = v(x+i), V[i] = V_i(x) for i <= N2 (absolute positions); the window is (n, N2]."""
    p = C.p
    H = N2 - n
    P = iv.mpf(p)
    gates = [i for i in range(n + 1, N2 + 1) if depth[i] > 0]
    fprime = min(th, top - MW) if th > 0 else None
    costs = []
    for j in range(len(gates) - 1):
        g, g2 = gates[j], gates[j + 1]
        Ls = V[g] - V[n]
        if Ls >= top:
            break
        Le = V[g2] - V[n]
        if th > 0 and depth[g2] == 1 and Le <= fprime:
            costs.append(C.qI[2] / P ** 2)
        else:
            d = min(depth[g2], top - Ls)
            costs.append(C.qt(d) / P ** d)
    Suf = [iv.mpf(1)] * (len(costs) + 1)
    for j in range(len(costs) - 1, -1, -1):
        Suf[j] = costs[j] * Suf[j + 1]
    tot = iv.mpf(2) ** (-H)
    cstar = min(H, int(top * math.log2(p)) + 700)
    gi = 0
    two = iv.mpf(2)
    for c in range(cstar):
        ac = V[n + c] - V[n]
        w = two ** (-(c + 1))
        if ac >= top:
            tot += w
            continue
        while gates[gi] <= n + c:
            gi += 1
        g1 = gates[gi] - (n + c)
        s1 = depth[gates[gi]]
        k = top - ac
        pr = C.P0I[g1][min(s1, k, C.S0)]
        sf = Suf[gi] if gi < len(Suf) else iv.mpf(1)
        tot += w * pr * sf
    if cstar < H:
        tot += two ** (-cstar)
    return P ** top * tot


def Eprime(C, K, H, fprime, sigma):
    """Prop E': closed-form upper bound (interval) for E_B[eps]."""
    p = C.p
    P = iv.mpf(p)
    two = iv.mpf(2)
    t1 = P ** K * two ** (-H) * (1 + two ** p)
    Dtot = C.logqt(sigma) - C.logq[1]
    expo = (K * C.rho1 + Dtot + C.gamma * (2 - iv.mpf(1) / p)
            - C.gamma * (fprime - sigma + 1) * iv.mpf(p - 1) ** 2 / P ** 2)
    ek = iv.exp(-C.kappa)
    t2 = two ** (p + sigma * (p - 1)) * iv.exp(expo) * ek / (1 - ek)
    return t1 + t2
