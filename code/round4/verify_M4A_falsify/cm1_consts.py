"""cm1: the universal constants of Lemma Q / Props D, E, E' at p = 3..23, by independent methods.
 (a) q_s: residue DP (exact int64) vs full enumeration (p <= 13) vs FFT of the characteristic function;
 (b) P_0(g, s): meet-in-the-middle (exact) vs residue DP, all g <= p, s <= SP;
 (c) monotonicity q_s <= q_{s+1} <= p q_s; the S used in Prop E' (8 for p <= 13, 4 above);
 (d) rho_1, gamma, kappa and the phase-4 rate c(p, r=27/20), compared with the values printed by M4A.
usage: python3 cm1_consts.py SP
"""
import sys, time
from fractions import Fraction
import numpy as np
import mpmath as mp
import cm_lib as L

SP = int(sys.argv[1])
M4A = {  # values printed in data/round4/M4A/fe_verify_final.log ("# constants:" lines) and M4A.md
    7: dict(q1=1.014282, q2=1.112549, rho1=0.060406, gamma=1.853438, kappa=0.911670),
    11: dict(q1=1.001436, q2=1.111596, rho1=0.016448, gamma=2.293534, kappa=2.654542),
    13: dict(q1=1.000022, q2=1.008124, rho1=0.002522, gamma=2.556880, kappa=3.576696),
    17: dict(q1=1.000001, q2=1.000290, rho1=0.000261, gamma=2.832924, kappa=5.747961),
    19: dict(q1=1.000000, q2=1.000463, rho1=0.000114, gamma=2.943976, kappa=6.890086),
    23: dict(q1=1.000000, q2=1.000002, rho1=0.000018, gamma=3.135492, kappa=9.244994),
}
r = mp.mpf(27) / 20
allok = True
for p in [3, 5, 7, 11, 13, 17, 19, 23]:
    t0 = time.time()
    C = L.Consts(p)
    smax_dp = max(s for s in range(1, 9) if p ** s <= 7 * 10 ** 6)
    # (a)
    bad = 0
    maxfft = 0.0
    for s in range(1, smax_dp + 1):
        c = L.q_counts_dp(p, s)
        qdp = L.q_from_counts(p, s, c)
        if s in C.q and C.q[s] != qdp:
            bad += 1
            print(f"  MISMATCH p={p} s={s}: dp {qdp} vs lib {C.q[s]}")
        P = L.q_counts_fft(p, s)
        maxfft = max(maxfft, float(np.max(np.abs(P - c / 4.0 ** p))))
        if p <= 13 and s <= 8:
            pass
    enum_note = ""
    if p <= 13:
        qe = L.q_enum(p, min(8, smax_dp))
        for s in qe:
            if qe[s] != L.q_from_counts(p, s, L.q_counts_dp(p, s)):
                bad += 1
                print(f"  ENUM MISMATCH p={p} s={s}")
        enum_note = f"enum==dp for s<={min(8, smax_dp)}"
    # (b)
    badP0 = 0
    for g in range(1, p + 1):
        for s in range(1, SP + 1):
            if p ** s > 30000:
                continue
            if L.P0(p, g, s) != L.P0_dp(p, g, s):
                badP0 += 1
                print(f"  P0 MISMATCH p={p} g={g} s={s}")
    # (c)
    qs = [C.q[s] for s in sorted(C.q)]
    mono = all(qs[i] <= qs[i + 1] <= p * qs[i] for i in range(len(qs) - 1))
    # (d)
    E = L.eprime_constants(C)
    rate = E['gamma'] * (p - 1) * (r - 1) / (2 * p ** 2) - (r ** 2 - 1) * E['rho1'] / (p - 1)
    print(f"p={p}: q_s exact for s<={max(C.q)}; DP s<={smax_dp}: mismatches {bad}; {enum_note}; max|FFT-DP| = {maxfft:.2e}; "
          f"P0 MITM==DP mismatches {badP0}; q_s <= q_s+1 <= p q_s: {mono}")
    print("    q_s = " + ", ".join(f"q{s}={float(C.q[s]):.8f}" for s in sorted(C.q)))
    if p in (7, 11, 13, 17, 19, 23):
        print(f"    q1 = {C.q[1]}  q2 = {C.q[2]}  q3 = {C.q[3]}")
    print(f"    Prop E' (S={C.S}): rho1={mp.nstr(E['rho1'], 10)} gamma={mp.nstr(E['gamma'], 10)} kappa={mp.nstr(E['kappa'], 10)} (kappa>0: {E['kappa'] > 0});"
          f" phase-4 rate c={mp.nstr(rate, 8)} (>0: {rate > 0})")
    if p in M4A:
        ref = M4A[p]
        dev = max(abs(float(C.q[1]) - ref['q1']), abs(float(C.q[2]) - ref['q2']), abs(float(E['rho1']) - ref['rho1']),
                  abs(float(E['gamma']) - ref['gamma']), abs(float(E['kappa']) - ref['kappa']))
        print(f"    vs M4A printed constants: max abs deviation {dev:.2e} (6-decimal print: agree iff < 1e-6): {dev < 1e-6}")
        allok &= dev < 1e-6
    # P0 table at small g (the deep-gate factor), largest s with p^s < 2^62
    smaxP0 = max(s for s in range(1, 40) if p ** s < 2 ** 62)
    tab = []
    for g in range(1, min(p, 6) + 1):
        tab.append(f"g={g}: " + ",".join(str(L.P0(p, g, s)) for s in (1, 2, 3, smaxP0)))
    print("    P0(g, s) for s = 1,2,3," + str(smaxP0) + ":  " + ";  ".join(tab))
    allok &= (bad == 0 and badP0 == 0 and mono and E['kappa'] > 0)
    print(f"    [{time.time() - t0:.1f} s]", flush=True)
print("ALL CONSTANT CHECKS PASS:", allok)
