#!/usr/bin/env python3
"""lemma_q_check.py -- exact test of Lemma Q (quenched anti-concentration) of data/round4/reports/M4A.md.

For u in Z_p, t >= 1, delta_0 = 1 and delta_1..delta_{t-1} i.i.d. signed (P(0)=1/2, P(+-1)=1/4),
T(u) = sum_{c<t} delta_c pi_c(u).  Gates: g_1 < g_2 < ... in [1, t] with p | u+g, depths s_r = v(u+g_r),
levels L_r = V_{g_r}(u), blocks r = [g_r, g_{r+1}) (full if g_{r+1} <= t).  Lemma Q claims

  P(v(T(u)) >= k, v(T'(u)) >= f) <= prod_{r>=1, L_r<k, block r full} pi_r,
  pi_r = q_2/p^2                    if s_{r+1} = 1 and L_{r+1} <= min(f, k - M_{g_{r+1}})   (2D harvest)
       = q_d/p^d, d=min(s_{r+1},k-L_r)  otherwise                                         (1D harvest)

with q_s = p^s max_z P(sum_{k<p} delta_k pi_k(-p) == z mod p^s) (universal block constants).
The left side is computed exactly by an integer DP over (T mod p^k, T' mod p^f) (f <= 0: no slope condition).
usage: lemma_q_check.py p SEED NU tmin tmax KMAX FMAX [MODE [CTRL]]   MODE=rand (Haar u) | deep (force a deep gate) | g2 (u = -2 mod p, block-0 factor 1/4: sharper test)
  | p0 (Haar u, exact block-0 probability P0 in the bound) | int (integer-like u, several deep gates, exact P0)
CTRL=x (a number < 1): negative control, the 2D factor q_2/p^2 is multiplied by x (failures expected if the test is sensitive).
"""
import itertools
import random
import sys
from fractions import Fraction

import numpy as np

from m4a_lib import vp

PREC = 80


def q_consts(p, S):
    w = {-1: 1, 0: 2, 1: 1}
    pk = [1]
    for k in range(1, p):
        pk.append(pk[-1] * (k - p))
    mod = p ** S
    L = {}
    for d in itertools.product((-1, 0, 1), repeat=p):
        wt = 1
        for x in d:
            wt *= w[x]
        z = sum(a * b for a, b in zip(d, pk)) % mod
        L[z] = L.get(z, 0) + wt
    out = [Fraction(1)]
    for s in range(1, S + 1):
        m = p ** s
        F = {}
        for z, c in L.items():
            F[z % m] = F.get(z % m, 0) + c
        out.append(Fraction(m * max(F.values()), 4 ** p))
    return out


def exact_prob(u, t, p, k, f):
    """exact P(v(T) >= k, v(T') >= f) as a Fraction (weights 1,2,1 per free digit)."""
    m1 = p ** k
    m2 = p ** max(f, 0)
    st = np.zeros((m1, m2), dtype=np.int64)
    st[1 % m1, 0] = 1  # delta_0 = 1: T = pi_0 = 1, T' = 0
    pc, dpc = 1, 0
    for c in range(1, t):
        dpc = dpc * (u + c) + pc
        pc = pc * (u + c)
        a, b = int(pc % m1), int(dpc % m2)
        st = 2 * st + np.roll(np.roll(st, a, axis=0), b, axis=1) + np.roll(np.roll(st, -a, axis=0), -b, axis=1)
    return Fraction(int(st[0, 0]), 4 ** (t - 1))


def block0_prob(u, p, k, gates_):
    g1 = gates_[0]
    s1 = vp(u + g1, p)
    sp = min(s1, k)
    vals = [1]
    for c in range(1, g1):
        vals.append(vals[-1] * (c - g1))
    w = {-1: 1, 0: 2, 1: 1}
    tot = 0
    for d in itertools.product((-1, 0, 1), repeat=g1 - 1):
        wt = 1
        for xx in d:
            wt *= w[xx]
        z = 1 + sum(a * b for a, b in zip(d, vals[1:]))
        if z % p ** sp == 0:
            tot += wt
    return Fraction(tot, 4 ** (g1 - 1))


def lemma_q_bound(u, t, p, k, f, q, ctrl=Fraction(1)):
    gates = [g for g in range(1, t + 1) if (u + g) % p == 0]
    s = {g: vp(u + g, p) for g in gates}
    V = [0] * (t + 1)
    for i in range(1, t + 1):
        V[i] = V[i - 1] + vp(u + i, p)
    Mpref = {}
    mx = 0
    for i in range(1, t + 1):
        mx = max(mx, vp(u + i, p))
        Mpref[i] = mx
    bound = Fraction(1)
    n2 = n1 = 0
    for r in range(len(gates)):
        g = gates[r]
        L = V[g]
        if L >= k:
            break
        if r + 1 >= len(gates):
            break  # block not full (no next gate within [1, t])
        g2 = gates[r + 1]
        if g2 > t:
            break
        s2 = s[g2]
        L2 = V[g2]
        if s2 == 1 and L2 <= min(f, k - Mpref[g2]):
            bound *= q[2] / p ** 2 * ctrl
            n2 += 1
        else:
            d = min(s2, k - L)
            bound *= q[d] / p ** d
            n1 += 1
    return bound, n2, n1, gates, [s[g] for g in gates]


def main():
    p, seed, NU, tmin, tmax, KMAX, FMAX = (int(a) for a in sys.argv[1:8])
    mode = sys.argv[8] if len(sys.argv) > 8 else 'rand'
    ctrl = Fraction(sys.argv[9]) if len(sys.argv) > 9 else Fraction(1)
    n2tests = 0
    rnd = random.Random(seed)
    q = q_consts(p, 8)
    MOD = p ** PREC
    tests = fails = 0
    worst = 0.0
    nonvac = 0
    for it in range(NU):
        u = rnd.randrange(MOD)
        if mode == 'deep':
            g0 = rnd.randrange(1, tmin)
            sdeep = rnd.randrange(2, 5)
            u = (-g0 + p ** sdeep * rnd.randrange(1, p)) % MOD  # v(u+g0) = sdeep exactly
        b0 = Fraction(1)
        if mode == 'int':
            # integer-like pattern: u = -w + p^40 * unit, so v(u+i) = v(i-w) for i != w: several deep gates
            w0 = rnd.randrange(p + 1, 400)
            u = (-w0 + p ** 40 * rnd.randrange(1, p ** 3)) % MOD
            if rnd.random() < 0.5:
                u = (w0 + p ** 40 * rnd.randrange(1, p ** 3)) % MOD   # v(u+i) = v(i+w0): natural-number-like
        if mode in ('p0', 'int'):
            b0 = None   # use the exact block-0 table P0
        if mode == 'g2':
            # u = -2 mod p: block 0 = {0,1}; T_{<2} = 1 + delta_1 (u+1) is divisible by p only if delta_1 = 1
            # (probability 1/4), and then the history after block 0 is deterministic; so the bound may use 1/4.
            u = (rnd.randrange(MOD // p) * p - 2) % MOD
            b0 = Fraction(1, 4)
        t = rnd.randrange(tmin, tmax + 1)
        Vt = sum(vp(u + i, p) for i in range(1, t + 1))
        for k in range(1, min(KMAX, Vt) + 1):
            for f in range(0, FMAX + 1):
                if p ** (k + f) > 3 * 10 ** 6:
                    continue
                P = exact_prob(u, t, p, k, f)
                B, n2, n1, gates, depths = lemma_q_bound(u, t, p, k, f, q, ctrl)
                if b0 is None:
                    B *= block0_prob(u, p, k, gates) if gates else 1
                else:
                    B *= b0
                n2tests += (n2 > 0)
                tests += 1
                ok = P <= B
                if not ok:
                    fails += 1
                    if fails <= 5: print(f"FAIL u={u % p**12} t={t} k={k} f={f} P={float(P):.4e} bound={float(B):.4e} gates={gates} depths={depths}")
                if P > 0:
                    nonvac += 1
                    worst = max(worst, float(P / B))
        if it % 10 == 0:
            print(f"progress {it}/{NU} tests={tests} fails={fails} max(P/bound)={worst:.4f}", flush=True)
    print(f"RESULT p={p} mode={mode} NU={NU} t in [{tmin},{tmax}] k<={KMAX} f<={FMAX}: {tests} (u,k,f) tests, "
          f"{fails} failures, {nonvac} with P>0, {n2tests} using >=1 2D factor, max P/bound = {worst:.4f}, ctrl={ctrl}")


if __name__ == "__main__":
    main()
