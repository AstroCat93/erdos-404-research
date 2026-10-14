#!/usr/bin/env python3
"""test_Q.py -- exact test of Lemma Q (quenched value/derivative anti-concentration) and Lemma P (its 1D part)
of the M4C report.

For y in Z_p, t >= 1, delta_0 = 1 and delta_c (1 <= c < t) i.i.d. lazy signed, T = sum delta_c pi_c(y),
T' = sum delta_c pi_c'(y).  Gates g_1 < g_2 < ... in [1, t-1] (p | y+g), depths d_i, levels l_i = d_1+...+d_i,
blocks B_0 = [0, g_1), B_i = [g_i, g_{i+1}) (B_I = [g_I, t)).
Lemma Q: for 1 <= f < k with f <= k - d_max,
   P(v(T) >= k, v(T') >= f) <= prod_{i notin J2, l_i < k} max_a P(S_i = a mod p^{e_i}) * prod_{i in J2} q2(p)/p^2,
   J2 = {i >= 1 : g_{i+1} <= t-1, d_{i+1} = 1, l_i < f},  e_i = min(l_{i+1}, k) - l_i,  S_i = sum_{c in B_i} delta_c pi_c/p^{l_i}.
Lemma P (f = 0, J2 empty): P(v(T) >= k) <= prod_{l_i < k} max_a P(S_i = a mod p^{e_i}).
The left side is computed exactly by a DP over (T mod p^k, T' mod p^f) (integer weights 1,2,1 per digit);
the 1D block maxima exactly from the block elements; q2(p) exactly (qconst.q2).
Negative control: the same bound with each J2 factor q2/p^2 replaced by q2/p^4 (two digits too many;
expected to fail).  Also printed: lhs / (bound with J2 blocks given only their 1D factor) * p^{#J2}, which
measures the 2D gain (it is ~ 1/p, the unused derivative constraint of block 0, when the gain is real).
usage: test_Q.py p SEED NTRIALS TMAX KMAXEXP
"""
import random
import sys
from fractions import Fraction

import numpy as np


def v(a, p, cap):
    a %= p ** cap
    if a == 0:
        return cap
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def block_max(elems, mod):
    """max_a P(sum d_c elems_c = a mod mod) for i.i.d. lazy signed d (exact Fraction)."""
    dist = np.zeros(mod, dtype=object)
    dist[0] = 1
    for a in elems:
        a %= mod
        dist = 2 * dist + np.roll(dist, a) + np.roll(dist, -a)
    return Fraction(int(max(dist)), 4 ** len(elems))


def main():
    p, seed, NT, TMAX, KMAXEXP = (int(a) for a in sys.argv[1:6])
    rnd = random.Random(seed)
    PREC = 40
    mod = p ** PREC
    q2 = exact_q2(p)
    st = dict(trials=0, fail=0, ctrl_fail=0, nonzero=0, with_J2=0, deep=0, max_ratio=0.0)
    for _ in range(NT):
        # environment: random y, sometimes forced deep gates
        y = rnd.randrange(mod)
        if rnd.random() < 0.5:
            y = p * rnd.randrange(mod // p)  # first gate at p: block 0 full
        elif rnd.random() < 0.4:
            g = rnd.randint(1, 3 * p)
            s = rnd.randint(2, 3)
            y = (-g + p ** s * rnd.randrange(p ** (PREC - s))) % mod
        t = rnd.randint(p + 2, TMAX)
        vals = [0] + [v(y + i, p, PREC) for i in range(1, t + 1)]
        if max(vals[1:t]) > 6:
            continue
        gates = [g for g in range(1, t) if vals[g] > 0]
        if not gates:
            continue
        pi = [1] * (t + 1)
        dpi = [0] * (t + 1)
        for j in range(1, t + 1):
            pi[j] = pi[j - 1] * (y + j) % mod
            dpi[j] = (dpi[j - 1] * (y + j) + pi[j - 1]) % mod
        Vt = sum(vals[1:t])  # level of the last block
        lev = [0]
        for g in gates:
            lev.append(lev[-1] + vals[g])
        dmax = max(vals[g] for g in gates)
        k = rnd.randint(2, min(Vt + 1, KMAXEXP))
        if k - dmax < 1:
            continue
        fmax = min(k - dmax, KMAXEXP - k)
        if fmax < 1:
            continue
        f = rnd.randint(min(2, fmax), fmax)
        # exact left side: DP over (T mod p^k, T' mod p^f), delta_0 = 1
        mk, mf = p ** k, p ** f
        dist = np.zeros((mk, mf), dtype=object)
        dist[pi[0] % mk, dpi[0] % mf] = 1
        for c in range(1, t):
            a, b = pi[c] % mk, dpi[c] % mf
            dist = 2 * dist + np.roll(np.roll(dist, a, axis=0), b, axis=1) + np.roll(np.roll(dist, -a, axis=0), -b, axis=1)
        lhs = Fraction(int(dist[0, 0]), 4 ** (t - 1))
        # blocks
        bounds = [0] + gates + [t]
        rhs = Fraction(1)
        rhs_ctrl = Fraction(1)
        rhs_1d = Fraction(1)
        nJ2 = 0
        for i in range(len(gates) + 1):
            li = lev[i]
            if li >= k:
                break
            lo, hi = bounds[i], bounds[i + 1]
            nxt = lev[i + 1] if i + 1 < len(lev) else 10 ** 9
            e = min(nxt, k) - li
            inJ2 = (i >= 1 and i + 1 <= len(gates) and gates[i] <= t - 1 and vals[gates[i]] == 1 and li < f) if i < len(gates) else False
            if inJ2:
                rhs *= q2 / p ** 2
                rhs_ctrl *= q2 / p ** 4
                elems1 = [(pi[c] // p ** li) for c in range(lo, hi) if c > 0]
                rhs_1d *= block_max(elems1, p)
                nJ2 += 1
            else:
                elems = [(pi[c] // p ** li) for c in range(lo, hi) if c > 0]
                # delta_0 = 1 is fixed: block 0 contains c = 0 with deterministic contribution (a shift)
                m = block_max(elems, p ** e) if elems else Fraction(1)
                rhs *= m
                rhs_ctrl *= m
                rhs_1d *= m
        st["trials"] += 1
        st["deep"] += (dmax >= 2)
        if nJ2:
            st["with_J2"] += 1
        if lhs > 0:
            st["nonzero"] += 1
            st["max_ratio"] = max(st["max_ratio"], float(lhs / rhs))
        if lhs > rhs:
            st["fail"] += 1
            print("FAIL", y % p ** 6, t, k, f, gates[:6], float(lhs), float(rhs))
        if lhs > rhs_ctrl:
            st["ctrl_fail"] += 1
        if nJ2:
            st.setdefault("J2_trials_lhs_over_1Dbound_times_p^nJ2", []).append(round(float(lhs / rhs_1d) * p ** nJ2, 3))
    print(f"# test_Q p={p} seed={seed} NT={NT} TMAX={TMAX} KMAXEXP={KMAXEXP}; q2={float(q2):.9f}")
    print("RESULT", st)


def exact_q2(p):
    from math import factorial
    m2 = p * p
    Hm = [0]
    h = 0
    for j in range(1, p):
        h = (h + pow(j, -1, p)) % p
        Hm.append(h)
    dist = {(0, 0): 1}
    f = 1
    for r in range(p):
        if r > 0:
            f = f * r
        a = f % m2
        bb = f * Hm[r] % p
        new = {}
        for (x, yv), w in dist.items():
            for d, m in ((0, 2), (1, 1), (-1, 1)):
                key = ((x + d * a) % m2, (yv + d * bb) % p)
                new[key] = new.get(key, 0) + w * m
        dist = new
    fold = {}
    for (x, yv), w in dist.items():
        key = (x % p, (yv - x // p) % p)
        fold[key] = fold.get(key, 0) + w
    return Fraction(p * p * max(fold.values()), 4 ** p)


if __name__ == "__main__":
    main()
