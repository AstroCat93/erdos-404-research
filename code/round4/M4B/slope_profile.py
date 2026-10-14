#!/usr/bin/env python3
"""slope_profile.py -- HEURISTIC (Monte Carlo over Haar y, float64 DP): slope profile of the normalised
alive mass Lam_a(y) of the signed Lambda-process (delta_0 = 1) at age a, on the truncation event
G = {M_a(y) <= sG}, and the 'Hensel-failure' mass, i.e. the mass of alive strings with
lambda > (V_a - M_a - 1)/2 (the strings to which Lemma B3 cannot be applied at age a).
For comparison, the Kac-Rice heuristic (value and derivative of a random signed polynomial independent
and equidistributed) predicts E[mass with slope = lambda] / E[Lam] ~ (1 - 1/p) p^{-lambda}.
Also stratified by whether some v(y+i) >= 2 with i <= p (an early gate of depth >= 2).
usage: slope_profile.py p SEED NY a sG LL [CAP]
"""
import random
import sys

import numpy as np

PREC = 80


def main():
    p, seed, NY, a, sG, LL = (int(t) for t in sys.argv[1:7])
    CAP = int(sys.argv[7]) if len(sys.argv) > 7 else 9
    rnd = random.Random(seed)
    MOD = p ** PREC

    def vp(z):
        z %= MOD
        if z == 0:
            return PREC
        k = 0
        while z % p == 0:
            z //= p
            k += 1
        return k

    lam_of = np.full(p ** LL, LL)
    for s in range(1, p ** LL):
        t, k = s, 0
        while t % p == 0:
            t //= p
            k += 1
        lam_of[s] = k
    tot = []
    byslope = []
    hf = []
    near = []
    nG = nskip = 0
    for it in range(NY):
        y = rnd.randrange(MOD)
        vals = [0] + [vp(y + i) for i in range(1, a + 1)]
        Va, Ma = sum(vals), max(vals[1:])
        if Ma > sG:
            continue
        nG += 1
        if Va + LL > CAP:
            nskip += 1
            continue
        m1, m2 = p ** Va, p ** LL
        st = np.zeros((m1, m2))
        st[1 % m1, 0] = 1.0
        pc, dpc = 1, 0
        for c in range(1, a):
            dpc = (dpc * (y + c) + pc) % MOD
            pc = pc * (y + c) % MOD
            a_, b_ = int(pc % m1), int(dpc % m2)
            st = 0.5 * st + 0.25 * np.roll(np.roll(st, a_, axis=0), b_, axis=1) \
                + 0.25 * np.roll(np.roll(st, -a_, axis=0), -b_, axis=1)
        row = p ** Va * st[0, :]
        prof = np.zeros(LL + 1)
        for s in range(m2):
            prof[lam_of[s]] += row[s]
        thr = (Va - Ma - 1) / 2.0
        hf.append(sum(prof[l] for l in range(LL + 1) if l > thr))
        near.append(max(vals[1:min(a, p) + 1]) >= 2)
        tot.append(row.sum())
        byslope.append(prof)
    n = len(tot)
    if n == 0:
        print(f"RESULT p={p} a={a} sG={sG}: no samples")
        return
    T = np.array(tot)
    B = np.array(byslope)
    HF = np.array(hf)
    prof = B.mean(axis=0)
    frac = prof / T.mean()
    kr = [(1 - 1 / p) * p ** -l for l in range(LL)] + [p ** -LL]
    print(f"RESULT p={p} a={a} sG={sG}: samples {n} (on G {nG}/{NY}, memory-skipped {nskip}); "
          f"E[Lam_a]={T.mean():.4g}+-{T.std(ddof=1)/np.sqrt(n):.2g}; slope shares "
          + ", ".join(f"{l if l < LL else '>=' + str(LL)}:{frac[l]:.3f}" for l in range(LL + 1))
          + "; Kac-Rice shares " + ", ".join(f"{x:.3f}" for x in kr)
          + f"; E[Hensel-failure mass]={HF.mean():.4g}+-{HF.std(ddof=1)/np.sqrt(n):.2g} "
          f"(share {HF.mean()/T.mean():.3f})", flush=True)
    NE = np.array(near)
    for tag, sel in (("gate of depth>=2 within p of the start", NE), ("no such gate", ~NE)):
        if sel.sum() > 1:
            print(f"   stratum [{tag}]: {sel.sum()} samples, E[Lam_a]={T[sel].mean():.4g}, "
                  f"E[Hensel-failure]={HF[sel].mean():.4g}, share {HF[sel].mean()/T[sel].mean():.3f}, "
                  f"median per-sample share {np.median(HF[sel]/np.maximum(T[sel],1e-300)):.3f}", flush=True)


if __name__ == "__main__":
    main()
