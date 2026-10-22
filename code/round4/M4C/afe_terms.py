#!/usr/bin/env python3
"""afe_terms.py -- Monte Carlo estimates (HEURISTIC, not a proof) of the terms of the annealed series
    sum_k E_z[ min(1, C * eps_{L_{k-1}, L_k}(z)) ]          (report, Theorem F / hypothesis AFE)
and of the L^1 band tails P(B > b) (report, Theorem D2/D3), for z Haar on a residue class r + p Z_p.

eps_{L,L'}(z): the L^2 band mass of R3M Prop C2 for the composite window with elements
y_c = (z+1)...(z+c), 0 <= c < L+L'; D = V_L(z), K = V_{L+L'}(z); band = zeta mod p^K with zeta != 0 mod p^(K-D).
B_{L,L'}(z): the L^1 band mass (same band, sum of |nu^|).
Counts are exact (normalised float64 roll-average, relative error ~1e-15); Fourier sums are float64 FFTs.
A sample with K > KMAX is NOT dropped: it is counted as min(1, C*eps) = 1 and B = +inf (conservative).
usage: afe_terms.py p SEED NZ RES C KMAX L1:L1' [L2:L2' ...]      (lengths in elements; RES = z mod p)
"""
import random
import sys
import time

import numpy as np


def vp(a, p, cap=80):
    if a == 0:
        return cap
    k = 0
    while a % p == 0 and k < cap:
        a //= p
        k += 1
    return k


def band_masses(z, L, L2, p, KMAX, MODBIG):
    vals = [vp((z + i) % MODBIG, p) for i in range(1, L + L2 + 1)]
    D = sum(vals[:L])
    K = sum(vals)
    if K > KMAX:
        return None, D, K, max(vals)
    if K == D:
        return (0.0, 0.0), D, K, max(vals)
    mod = p ** K
    dist = np.zeros(mod, dtype=np.float64)
    dist[0] = 1.0
    y = 1
    for c in range(L + L2):
        dist = 0.5 * (dist + np.roll(dist, y % mod))
        y = y * (z + c + 1) % mod
    F = np.fft.fft(dist)
    idx = np.arange(mod)
    band = (idx % p ** (K - D)) != 0
    a = np.abs(F[band])
    return (float(np.sum(a * a)), float(np.sum(a))), D, K, max(vals)


def main():
    p, seed, NZ, RES = (int(a) for a in sys.argv[1:5])
    C = float(sys.argv[5])
    KMAX = int(sys.argv[6])
    pairs = [tuple(int(t) for t in s.split(":")) for s in sys.argv[7:]]
    rnd = random.Random(seed)
    MODBIG = p ** 80
    print(f"# afe_terms p={p} seed={seed} NZ={NZ} z = {RES} mod p, C={C}, KMAX={KMAX}, pairs={pairs}")
    tot = 0.0
    for (L, L2) in pairs:
        t0 = time.time()
        mins, epss, Bs, over = [], [], [], 0
        for _ in range(NZ):
            z = RES + p * rnd.randrange(MODBIG // p)
            r, D, K, md = band_masses(z, L, L2, p, KMAX, MODBIG)
            if r is None:
                over += 1
                mins.append(1.0)
                Bs.append(float("inf"))
                continue
            eps, B = r
            epss.append(eps)
            Bs.append(B)
            mins.append(min(1.0, C * eps))
        m = float(np.mean(mins))
        se = float(np.std(mins) / np.sqrt(NZ))
        tot += m
        Bs.sort()
        epss.sort()
        q = lambda arr, f: arr[min(len(arr) - 1, int(f * len(arr)))] if arr else float("nan")
        print(f"TERM L={L} L'={L2}: E[min(1,{C:g} eps)] = {m:.3e} +- {se:.1e}  (K>KMAX: {over}/{NZ}); "
              f"median eps={q(epss,.5):.2e} q99={q(epss,.99):.2e}; "
              f"P(B>0.05)={sum(1 for b in Bs if b > 0.05)/NZ:.4f} P(B>0.005)={sum(1 for b in Bs if b > 0.005)/NZ:.4f} "
              f"median B={q(Bs,.5):.2e}  [{time.time()-t0:.0f}s]", flush=True)
    print(f"SUM of estimated terms = {tot:.3e}")


if __name__ == "__main__":
    main()
