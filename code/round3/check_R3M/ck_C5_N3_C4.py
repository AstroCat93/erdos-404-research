#!/usr/bin/env python3
"""ck_C5_N3_C4.py -- independent checks of R3M Lemma C5, Proposition N3, Lemma C4 (deterministic
part) and the measurability claim used for B_ell in Theorem C3.

mode C5 : p seed nx n H H2      -- Lemma C5 identity in exact rationals.
          eps := p^(D+D') Coll_(D+D') - p^D Coll_D of the composite window [n, N') (subset-sum DP),
          against (c_N'-c_N)/c_n + sum_{n<=j<N} c_j/(2c_n)[Lam_{N'-j}(x+j) - Lam_{N-j}(x+j)]
                  + sum_{N<=j<N'} c_j/(2c_n) Lam_{N'-j}(x+j),
          Lam_t(y) = p^{V_t(y)} P(1 + sum_{1<=c<t} delta_c pi_c(y) == 0 mod p^{V_t(y)}),
          delta i.i.d. on {-1,0,1} with weights 1/4,1/2,1/4 (exact DP over residues).
mode N3 : p seed smax tmax      -- Lam_t(y) for y = -2 + p^s u (u random unit): checks the lower bound
          Lam_t(y) >= p^{s + v((t-2)!)} 2^-(t+1) for s >= s0, and prints the shell masses
          (1-1/p) p^-s E[Lam_t | v(y+2)=s] (sampled), which must not tend to 0.
mode C4 : p seed nx n0 r        -- deterministic part of Lemma C4 on random x (with forced deep gates):
          if M_{n_(l+1)} < s_l and n_(l+1)-n_(l-1) >= p then D_(l-1)+D_l <= m_(l-1)-M_(l+1) and
          M_(l+1) < m_(l-1); and B_l measurability: on {M_(l+1) < m_(l-1)} eps_l(x) is unchanged
          when x is replaced by x + p^{m_(l-1)} z.
"""
import math
import random
import sys
from fractions import Fraction

from ck_lib import PAdic, collision


def vfact(n, p):
    s = 0
    q = p
    while q <= n:
        s += n // q
        q *= p
    return s


def Lam(P, y, t):
    """exact Lambda_t(y) as a Fraction (y an integer; requires y+i != 0 mod p^prec for i<=t)."""
    p = P.p
    Vt = sum(P.v(y + i) for i in range(1, t + 1))
    md = p ** Vt
    dist = {1 % md: 1}  # residue -> weight (integer, denominators 4 per digit)
    prod = 1
    for c in range(1, t):
        prod = prod * (y + c)
        pc = prod % md
        new = {}
        for r, wgt in dist.items():
            new[r] = new.get(r, 0) + 2 * wgt
            r1 = (r + pc) % md
            new[r1] = new.get(r1, 0) + wgt
            r2 = (r - pc) % md
            new[r2] = new.get(r2, 0) + wgt
        dist = new
    prob = Fraction(dist.get(0, 0), 4 ** (t - 1))
    return p ** Vt * prob


def mode_C5(p, seed, nx, n, H, H2):
    P = PAdic(p, 80)
    rnd = random.Random(seed)
    N, N2 = n + H, n + H + H2
    ok = tot = 0
    for _ in range(nx):
        x = rnd.randrange(P.mod)
        vals = [None] + [P.v(x + i) for i in range(1, N2 + 1)]
        V = [0] * (N2 + 1)
        for j in range(1, N2 + 1):
            V[j] = V[j - 1] + vals[j]
        c = [Fraction(p ** V[j], 2 ** j) for j in range(N2 + 1)]
        D, D2 = V[N] - V[n], V[N2] - V[N]
        if D + D2 > 12:
            continue
        ys = []
        for i in range(N2 - n):
            q = 1
            for k in range(n + 1, n + i + 1):
                q *= x + k
            ys.append(q)
        eps = p ** (D + D2) * collision(ys, p ** (D + D2)) - p ** D * collision(ys, p ** D)
        rhs = (c[N2] - c[N]) / c[n]
        for j in range(n, N):
            rhs += c[j] / (2 * c[n]) * (Lam(P, x + j, N2 - j) - Lam(P, x + j, N - j))
        for j in range(N, N2):
            rhs += c[j] / (2 * c[n]) * Lam(P, x + j, N2 - j)
        tot += 1
        if eps == rhs:
            ok += 1
    print(f"RESULT C5 p={p} n={n} H={H} H2={H2}: identity exact in {ok}/{tot} samples")


def mode_N3(p, seed, smax, tmax):
    P = PAdic(p, 60)
    rnd = random.Random(seed)
    nviol = ntest = 0
    for t in range(3, tmax + 1):
        vf = vfact(t - 2, p)
        bound_const = Fraction(p ** vf, 2 ** (t + 1))
        row = []
        for s in range(1, smax + 1):
            vals = []
            for _ in range(6):
                u = rnd.randrange(1, p)
                hi = rnd.randrange(p ** 10)
                y = -2 + p ** s * (u + p * hi)
                L = Lam(P, y, t)
                vals.append(L)
                if s >= vf and p ** s > t:
                    ntest += 1
                    if L < p ** s * bound_const:
                        nviol += 1
            shell = (1 - Fraction(1, p)) * Fraction(sum(vals), len(vals)) / p ** s
            row.append(f"{float(shell):.4g}")
        print(f"N3 p={p} t={t}: shell masses (1-1/p)p^-s E[Lam_t|v(y+2)=s], s=1..{smax}: {' '.join(row)}"
              f"   (lower bound (1-1/p)p^v((t-2)!)2^-(t+1) = {float((1 - Fraction(1, p)) * bound_const):.4g})")
    print(f"RESULT N3 p={p}: lower-bound violations {nviol}/{ntest}")


def mode_C4(p, seed, nx, n0, r):
    P = PAdic(p, 200)
    rnd = random.Random(seed)
    times = [n0]
    while len(times) < 9:
        times.append(math.ceil(r * times[-1]))
    nimp = nimp_f = nmeas = nmeas_f = 0
    for it in range(nx):
        x = rnd.randrange(P.mod)
        if it % 2 == 1:
            # force a deep gate somewhere in the window range
            i = rnd.randrange(1, times[-1] + 1)
            s = rnd.randrange(1, 12)
            x = (-i + p ** s * rnd.randrange(1, P.mod // p ** s)) % P.mod
        vals = [None] + [P.v(x + i) for i in range(1, times[-1] + 1)]
        V = lambda k: sum(vals[1:k + 1])
        M = lambda k: max(vals[1:k + 1])
        for l in range(1, len(times) - 1):
            nlm, nl, nlp = times[l - 1], times[l], times[l + 1]
            gamma = 2 * vfact(nlm, p) - Fraction(nlp, p - 1)
            s_l = math.floor(gamma / 2) + 1
            mlm = V(nlm)
            Dl1, Dl = V(nl) - V(nlm), V(nlp) - V(nl)
            if M(nlp) < s_l and nlp - nlm >= p:
                nimp += 1
                if not (Dl1 + Dl <= mlm - M(nlp) and M(nlp) < mlm):
                    nimp_f += 1
            if M(nlp) < mlm and Dl1 + Dl <= 9 and l <= 3:
                # eps_l depends only on x mod p^{m_(l-1)}
                def eps_at(xx):
                    ys = []
                    for i in range(nlp - nlm):
                        q = 1
                        for k in range(nlm + 1, nlm + i + 1):
                            q *= xx + k
                        ys.append(q)
                    K, Dd = Dl1 + Dl, Dl1
                    return p ** K * collision(ys, p ** K) - p ** Dd * collision(ys, p ** Dd)
                z = rnd.randrange(1, p ** 20)
                x2 = x + p ** mlm * z
                nmeas += 1
                if eps_at(x) != eps_at(x2):
                    nmeas_f += 1
    print(f"RESULT C4 p={p} n0={n0} r={r}: implication tested {nimp} times, failures {nimp_f}; "
          f"eps_l measurability tested {nmeas} times, failures {nmeas_f}")


def main():
    mode = sys.argv[1]
    a = [int(t) if mode != "C4" or i < 4 else float(t) for i, t in enumerate(sys.argv[2:])]
    if mode == "C5":
        mode_C5(*a)
    elif mode == "N3":
        mode_N3(*a)
    elif mode == "C4":
        mode_C4(int(a[0]), int(a[1]), int(a[2]), int(a[3]), float(a[4]))


if __name__ == "__main__":
    main()
