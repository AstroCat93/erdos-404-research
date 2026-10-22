#!/usr/bin/env python3
"""vcl_lemmaQ.py -- independent exact test of M4C Lemma Q (and Lemma P), verify_C_logic track.

For a fixed y in Z_p (given modulo p^PREC), t >= 1, k, f with 1 <= f < k, f <= k - d_max:
  T = sum_{c<t} delta_c pi_c(y),  T' = sum_{c<t} delta_c pi_c'(y),  delta_0 = 1 (as in Lambda), delta_c (c >= 1)
  i.i.d. lazy signed.  LHS = P(v(T) >= k, v(T') >= f) is computed EXACTLY (integer counts, DP over
  (T mod p^k, T' mod p^f)).
  RHS = (q2/p^2)^{|J|} * prod_{i notin J, l_i < k} max_a P(S_i = a mod p^{e_i}), every factor computed exactly
  from the actual block elements (no use of q1/q3), J as defined in Lemma Q.
Also a CONTROL: the same bound with the J-factor q2/p^3 (one more factor p of 'gain'), which must fail sometimes.
Environments: y = -g1 + p*w with w chosen so that some gates are deep / have unit = -1 mod p (as on A), and
random y.
usage: vcl_lemmaQ.py p ntrials seed [forceJ]   (forceJ=1: take f = largest admissible value, so J is usually nonempty)
"""
import random
import sys
from fractions import Fraction

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from vcl_q import q2 as Q2  # noqa: E402

PREC = 40


def v(n, p):
    if n == 0:
        return 10 ** 6
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def pis(y, t, mod):
    """pi_c(y), pi_c'(y) mod `mod` for c < t (exact integers mod mod)."""
    out = []
    pi, pid = 1, 0
    for c in range(t):
        if c > 0:
            pid = (pid * (y + c) + pi) % mod
            pi = pi * (y + c) % mod
        out.append((pi, pid))
    return out


def lhs_exact(y, t, k, f, p):
    mk, mf = p ** k, p ** f
    P = pis(y, t, p ** PREC)
    dist = np.zeros((mk, mf), dtype=object)
    dist[:, :] = 0
    a0, b0 = P[0][0] % mk, P[0][1] % mf     # delta_0 = 1
    dist[a0, b0] = 1
    for c in range(1, t):
        a, b = P[c][0] % mk, P[c][1] % mf
        dist = 2 * dist + np.roll(np.roll(dist, a, 0), b, 1) + np.roll(np.roll(dist, -a, 0), -b, 1)
    return Fraction(int(dist[0, 0]), 4 ** (t - 1))


def block_max(elems_scaled, e, p, first_fixed):
    """max_a P(sum delta_c x_c = a mod p^e), x_c given; if first_fixed, delta of the first element is 1."""
    m = p ** e
    dist = np.zeros(m, dtype=object)
    dist[:] = 0
    start = 0
    if first_fixed:
        dist[elems_scaled[0] % m] = 1
        start = 1
    else:
        dist[0] = 1
    n = 0
    for x in elems_scaled[start:]:
        x %= m
        dist = 2 * dist + np.roll(dist, x) + np.roll(dist, -x)
        n += 1
    return Fraction(int(max(dist)), 4 ** n)


def rhs(y, t, k, f, p, q2, control=False):
    P = pis(y, t, p ** PREC)
    gates = [g for g in range(1, t) if (y + g) % p == 0]
    I = len(gates)
    d = [None] + [v(y + g, p) for g in gates]          # d[1..I]
    lev = [0]
    for i in range(1, I + 1):
        lev.append(lev[-1] + d[i])
    dmax = max(d[1:]) if I else 0
    assert 1 <= f < k and f <= k - dmax
    bounds = [0] + gates + [t]
    J = [i for i in range(1, I) if d[i + 1] == 1 and lev[i] < f]
    out = Fraction(1)
    for i in range(0, I + 1):
        if lev[i] >= k:
            continue
        nxt = lev[i + 1] if i + 1 <= I else 10 ** 6
        e = min(nxt, k) - lev[i]
        if i in J:
            out *= q2 / (p ** 3 if control else p ** 2)
            continue
        elems = [P[c][0] // p ** lev[i] for c in range(bounds[i], bounds[i + 1])]
        assert all(P[c][0] % p ** lev[i] == 0 for c in range(bounds[i], bounds[i + 1]))
        out *= block_max(elems, e, p, first_fixed=(i == 0))
    return out, J, d, lev


def make_y(p, rng, nblk):
    g1 = rng.randrange(1, p + 1)
    # w controls gate depths: gate m (m=0..) is y+g1+mp = p(w+m); depth 1+v(w+m)
    mode = rng.randrange(4)
    w = rng.randrange(p ** (PREC - 2))
    if mode == 0:       # one depth-2 gate at m0, preceded by depth-1 gate with unit = -1 mod p (as on A)
        m0 = rng.randrange(1, nblk)
        w = -m0 + p * rng.randrange(1, p ** 10) * (1 if rng.random() < 0.5 else 1)
    elif mode == 1:     # a deep gate (depth 3..4) at m0
        m0 = rng.randrange(0, nblk)
        dd = rng.randrange(2, 4)
        w = -m0 + p ** dd * rng.randrange(1, p ** 8)
    elif mode == 2:     # first gate itself deep, others depth 1
        dd = rng.randrange(1, 3)
        w = p ** dd * rng.randrange(1, p ** 8)
    y = (-g1 + p * w) % p ** PREC
    return y


def main():
    p = int(sys.argv[1])
    ntr = int(sys.argv[2])
    rng = random.Random(int(sys.argv[3]))
    forceJ = len(sys.argv) > 4 and sys.argv[4] == '1'
    q2 = Q2(p)
    fails = ctrl_viol = withJ = done = 0
    maxratio = Fraction(0)
    maxratio_J = Fraction(0)
    budget = {5: 8, 7: 6, 11: 5}[p]     # k + f <= budget keeps the DP small
    while done < ntr:
        nblk = rng.randrange(3, 6)
        y = make_y(p, rng, nblk)
        g1 = next(g for g in range(1, p + 1) if (y + g) % p == 0)
        t = g1 + (nblk - 1) * p + rng.randrange(1, p + 1)
        gates = [g for g in range(1, t) if (y + g) % p == 0]
        if not gates:
            continue
        dmax = max(v(y + g, p) for g in gates)
        if dmax > 4 or dmax + 2 >= budget:
            continue
        k = rng.randrange(dmax + 2, budget)
        fmax = min(k - dmax, budget - k)
        if fmax < 1:
            continue
        f = fmax if forceJ else rng.randrange(1, fmax + 1)
        L = lhs_exact(y, t, k, f, p)
        R, J, d, lev = rhs(y, t, k, f, p, q2)
        Rc, _, _, _ = rhs(y, t, k, f, p, q2, control=True)
        done += 1
        if J:
            withJ += 1
        if L > R:
            fails += 1
            print(f"FAIL y={y} t={t} k={k} f={f} J={J} d={d} L={float(L):.4e} R={float(R):.4e}")
        if L > Rc:
            ctrl_viol += 1
        if R > 0:
            r = L / R
            maxratio = max(maxratio, r)
            if J:
                maxratio_J = max(maxratio_J, r)
    print(f"p={p}: {done} trials ({withJ} with J nonempty): failures {fails}; max LHS/RHS {float(maxratio):.4f} "
          f"(J nonempty: {float(maxratio_J):.4f}); control (J-factor q2/p^3) violated {ctrl_viol} times")


if __name__ == "__main__":
    main()
