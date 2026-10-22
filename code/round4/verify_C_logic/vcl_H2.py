#!/usr/bin/env python3
"""vcl_H2.py -- independent exact test of M4C Lemma H2 / Proposition H' in the setting where they are used.

Composite window of length n = L + L' at z (elements pi_c(z), c < n), D = V_L(z), K = V_n(z), M = M_n(z).
Ball B = z0 + p^r Z_p with r = M + 1 (all v(z+i), i <= n, constant on B).  Hypotheses (2.2): D >= 2r and
ceil(D/2) <= K - M.  With delta i.i.d. lazy signed (delta_0 included), exactly (int64 counts):
   E_B[eps]  = avg_{z in B mod p^K} ( p^K P(T = 0 mod p^K) - p^D P(T = 0 mod p^D) )
   H         = avg_{z} p^K P( T = 0 mod p^K,  T' = 0 mod p^h ),   h = ceil(D/2)
Lemma H2 summed over delta (= first inequality of Prop H') says E_B[eps] <= H.
Control: the same with h replaced by D (i.e. 'v(T') >= D'), which must fail sometimes.
Pointwise identity of Prop H' (at a few z):  H(z) = c_n + sum_j (c_j/2) Lambda^{(lambda_j)}_{n-j}(z+j).
usage: vcl_H2.py p ntrials seed
"""
import random
import sys

import numpy as np

PREC = 30


def v(n, p):
    if n == 0:
        return 10 ** 6
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def elems(z, n, mod):
    out = []
    pi, pid = 1, 0
    for c in range(n):
        if c > 0:
            pid = (pid * (z + c) + pi) % mod
            pi = pi * (z + c) % mod
        out.append((pi, pid))
    return out


def dp2(E, mk, mh, first_fixed=False):
    """int64 counts of (sum delta_c a_c mod mk, sum delta_c b_c mod mh); weights 2,1,1."""
    dist = np.zeros((mk, mh), dtype=np.int64)
    if first_fixed:
        dist[E[0][0] % mk, E[0][1] % mh] = 1
        rest = E[1:]
    else:
        dist[0, 0] = 1
        rest = E
    for a, b in rest:
        a %= mk
        b %= mh
        dist = 2 * dist + np.roll(np.roll(dist, a, 0), b, 1) + np.roll(np.roll(dist, -a, 0), -b, 1)
    return dist, 4 ** len(rest)


def main():
    p = int(sys.argv[1])
    ntr = int(sys.argv[2])
    rng = random.Random(int(sys.argv[3]))
    done = fails = ctrl = ident_ok = ident_n = 0
    worst = 0.0
    tries = 0
    while done < ntr and tries < 200000:
        tries += 1
        n = rng.randrange(3 * p, 7 * p)
        L = rng.randrange(2 * p, n - 1)
        z0 = rng.randrange(p ** PREC)
        vals = [v(z0 + i, p) for i in range(1, n + 1)]
        M = max(vals)
        r = M + 1
        D = sum(vals[:L])
        K = sum(vals)
        h = -(-D // 2)
        if not (D >= 2 * r and h <= K - M and D < K):
            continue
        if K + h > 10 or K - r > 5 or K > 8:
            continue
        mk, mh = p ** K, p ** h
        z0 %= p ** r
        Es, Hs, Cs = [], [], []
        for w in range(p ** (K - r)):
            z = z0 + p ** r * w
            E = elems(z, n, p ** PREC)
            assert [v(z + i, p) for i in range(1, n + 1)] == vals
            dist, W = dp2(E, mk, mh)
            totK = dist.sum(axis=1)                     # law of T mod p^K
            collK = int(totK[0])
            collD = int(totK[::p ** D].sum())            # residues = 0 mod p^D
            eps = (p ** K * collK - p ** D * collD) / W
            H = p ** K * int(dist[0, 0]) / W
            distc, _ = dp2(E, mk, p ** D)                # control: v(T') >= D
            Hc = p ** K * int(distc[0, 0]) / W
            Es.append(eps)
            Hs.append(H)
            Cs.append(Hc)
        Eb, Hb, Cb = np.mean(Es), np.mean(Hs), np.mean(Cs)
        done += 1
        npos = sum(1 for e in Es if e > 1e-15)
        print(f"  ball z0={z0} r={r} n={n} L={L} D={D} K={K} M={M}: E_B[eps]={Eb:.4e} (eps>0 at {npos}/{len(Es)} pts) H={Hb:.4e} control={Cb:.4e}", flush=True)
        if Eb > Hb * (1 + 1e-12) + 1e-15:
            fails += 1
            print(f"FAIL z0={z0} n={n} L={L} D={D} K={K} M={M}: E_B eps={Eb:.6e} > H={Hb:.6e}")
        if Eb > Cb * (1 + 1e-12) + 1e-15:
            ctrl += 1
        if Hb > 0:
            worst = max(worst, Eb / Hb)
        # pointwise identity at one z of the ball
        if ident_n < 3 * ntr:
            z = z0 + p ** r * rng.randrange(p ** (K - r))
            E = elems(z, n, p ** PREC)
            dist, W = dp2(E, mk, mh)
            Hz = p ** K * int(dist[0, 0]) / W
            Vt = [0]
            for i in range(1, n + 1):
                Vt.append(Vt[-1] + v(z + i, p))
            rhs = 2.0 ** (-n) * p ** K
            for j in range(n):
                y = z + j
                t = n - j
                Vty = Vt[n] - Vt[j]
                lam = h - Vt[j]
                Ey = elems(y, t, p ** PREC)
                mm = p ** max(lam, 0)
                dy, Wy = dp2(Ey, p ** Vty, mm, first_fixed=True)
                Lam = p ** Vty * int(dy[0, 0]) / Wy
                cj = 2.0 ** (-j) * p ** Vt[j]
                rhs += cj / 2 * Lam
            ident_n += 1
            if abs(rhs - Hz) <= 1e-12 * max(1.0, abs(Hz)):
                ident_ok += 1
            else:
                print(f"IDENTITY MISMATCH z={z} n={n}: H(z)={Hz:.12e} rhs={rhs:.12e}")
    print(f"p={p}: {done} balls tested (from {tries} draws); E_B[eps] <= H failures: {fails}; max E_B[eps]/H = {worst:.4f}; "
          f"control (v(T')>=D) violated on {ctrl} balls; pointwise identity of Prop H' exact at {ident_ok}/{ident_n} points")


if __name__ == "__main__":
    main()
