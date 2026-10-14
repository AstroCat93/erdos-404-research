#!/usr/bin/env python3
"""sb_probe.py -- HEURISTIC probe (Monte Carlo over Haar y, float64 DP) of hypothesis (S_B) of the M4B report.

Signed carry process from y with delta_0 = 1 (the Lambda-process of R3M Lemma C5): strings delta in
{-1,0,1}^a, weights (1/4,1/2,1/4), F_delta = sum_{c<a} delta_c pi_c(y), alive at age a iff v(F) >= V_a(y),
slope lambda = v(F'(y)).  For a chain step [a, a'] the REGIME of Lemma B3/Theorem B4 is
   lambda <= L(y) := min( floor((V_a - M_a - 1)/2), V_a - M_a - D, V_a - M_a' - 1, floor((a'-a)/p),
                          V_a - 1 - sG )                                   (D = V_a' - V_a),
on the truncation event G = {M_a'(y) <= sG}.  The program estimates, over Haar y (truncated by G):
   Lam_a      = p^{V_a} P(alive at a)                    (total normalised mass at age a)
   NR_a       = p^{V_a} P(alive at a, non-regime)        (non-regime parent mass)
   H_a        = p^{V_a'} P(alive at a', prefix non-regime at a)   (the quantity bounded by (S_B))
   Lam_a'     = total normalised mass at a'.
Dense DP over (F mod p^{V_a'}, F' mod p^LL), LL = Lmax+2 slope classes (exact class up to Lmax+1).
Samples with V_a' + LL > CAP are skipped (memory) and counted.  Not a proof of anything.
usage: sb_probe.py p SEED NY a a' sG [CAP]
"""
import random
import sys

import numpy as np

PREC = 80


def main():
    p, seed, NY, a, a2, sG = (int(t) for t in sys.argv[1:7])
    CAP = int(sys.argv[7]) if len(sys.argv) > 7 else 8
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

    acc = {'Lam_a': [], 'NR_a': [], 'H_a': [], 'Lam_a2': [], 'R_child': []}
    nG = nskip = 0
    Lthr_hist = {}
    for it in range(NY):
        y = rnd.randrange(MOD)
        vals = [0] + [vp(y + i) for i in range(1, a2 + 1)]
        V = np.cumsum(vals)
        Ma, Ma2 = max(vals[1:a + 1]), max(vals[1:a2 + 1])
        if Ma2 > sG:
            continue
        nG += 1
        Va, Va2 = int(V[a]), int(V[a2])
        D = Va2 - Va
        L = min((Va - Ma - 1) // 2, Va - Ma - D, Va - Ma2 - 1, (a2 - a) // p, Va - 1 - sG)
        Lthr_hist[L] = Lthr_hist.get(L, 0) + 1
        LL = max(L, 0) + 2
        if Va2 + LL > CAP:
            nskip += 1
            continue
        m1, m2 = p ** Va2, p ** LL
        st = np.zeros((m1, m2))
        st[1 % m1, 0] = 1.0
        pc, dpc = 1, 0
        for c in range(1, a2):
            dpc = (dpc * (y + c) + pc) % MOD
            pc = pc * (y + c) % MOD
            if c == a:
                # classify at age a
                aliveS = np.arange(0, m1, p ** Va)
                lam = np.full(m2, LL)
                for s in range(1, m2):
                    t, k = s, 0
                    while t % p == 0:
                        t //= p
                        k += 1
                    lam[s] = k
                lam[0] = LL  # slope >= LL
                nonreg = lam > L
                mass_alive = st[aliveS, :]
                Lam_a = p ** Va * mass_alive.sum()
                NR_a = p ** Va * mass_alive[:, nonreg].sum()
                keep = np.zeros_like(st)
                keep[np.ix_(aliveS, np.where(nonreg)[0])] = st[np.ix_(aliveS, np.where(nonreg)[0])]
                regpart = np.zeros_like(st)
                regpart[np.ix_(aliveS, np.where(~nonreg)[0])] = st[np.ix_(aliveS, np.where(~nonreg)[0])]
                st_full = st
                st = keep
                st_reg = regpart
            a_ = int(pc % m1)
            b_ = int(dpc % m2)
            upd = lambda arr: 0.5 * arr + 0.25 * np.roll(np.roll(arr, a_, axis=0), b_, axis=1) \
                + 0.25 * np.roll(np.roll(arr, -a_, axis=0), -b_, axis=1)
            st = upd(st)
            if c >= a:
                st_full = upd(st_full)
                st_reg = upd(st_reg)
        H_a = p ** Va2 * st[0, :].sum()
        Lam_a2 = p ** Va2 * st_full[0, :].sum()
        R_child = p ** Va2 * st_reg[0, :].sum()
        acc['Lam_a'].append(Lam_a)
        acc['NR_a'].append(NR_a)
        acc['H_a'].append(H_a)
        acc['Lam_a2'].append(Lam_a2)
        acc['R_child'].append(R_child)
    n = len(acc['Lam_a'])
    if n == 0:
        print(f"RESULT p={p} a={a} a'={a2} sG={sG}: no samples (G-hits {nG}, skipped {nskip})")
        return

    def ms(key):
        arr = np.array(acc[key])
        return f"{arr.mean():.4g}+-{arr.std(ddof=1) / np.sqrt(len(arr)) if len(arr) > 1 else 0:.2g}"
    print(f"RESULT p={p} a={a} a'={a2} sG={sG}: samples {n} (on G {nG}/{NY}, skipped for memory {nskip}); "
          f"thresholds L: {dict(sorted(Lthr_hist.items()))}; E[Lam_a]={ms('Lam_a')} E[NR_a]={ms('NR_a')} "
          f"E[H_a]={ms('H_a')} E[regime children]={ms('R_child')} E[Lam_a']={ms('Lam_a2')}", flush=True)


if __name__ == "__main__":
    main()
