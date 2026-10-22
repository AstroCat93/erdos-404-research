#!/usr/bin/env python3
"""context_checks.py -- small consistency checks for the obstruction/scope report on M4C (no M4C code used).

1. delta_1(p) = mu{g_p >= 1} = 1 - |Phi_p|/p, with Phi_p the classes r mod p on which g_p = 0 (note Thm 3.5:
   r is NOT in Phi_p iff some B in [1, k*) has 1 + sum_{b in B} pi_b(r) = 0 mod p, k* = least k >= 1 with p | r+k).
   Compared with the round-1 values delta_G(p) of note section 4.7 (rigorous upper bounds for mu(K_p)), this gives
   the average density of K_p on the classes where g_p is not identically 0, as context for M4C's conditional
   lower bounds c_p on A = p^3 Z_p (A lies in the class r = 0, which is never in Phi_p).
2. Prop 11.12 floor: chi^2_{W_0}(A) = q_1 - 1 >= (p-1) 4^{-p} for every listed p (q_1 - 1 from qfourier.log).
usage: context_checks.py qfourier.log
"""
import sys


def delta1(p):
    good = 0
    in_phi = []
    for r in range(p):
        kstar = next(k for k in range(1, p + 1) if (r + k) % p == 0)
        reach = {1 % p}
        pi = 1
        for b in range(1, kstar):
            pi = pi * (r + b) % p
            reach |= {(t + pi) % p for t in reach}
        if 0 in reach:
            good += 1
        else:
            in_phi.append(r)
    return good, in_phi


def main():
    dG = {11: (6, 0.69976), 13: (5, 0.75454), 17: (4, 0.75692), 19: (4, 0.77792), 23: (3, 0.85617)}
    for p in (7, 11, 13, 17, 19, 23, 29, 31):
        good, phi = delta1(p)
        line = f"p={p}: delta_1 = {good}/{p} = {good / p:.5f}; Phi_p = {phi}; 0 in Phi_p: {0 in phi}"
        if p in dG:
            G, v = dG[p]
            line += f"; round-1 delta_{G} = {v} (upper bound for mu(K_p)); delta_G/delta_1 = {v / (good / p):.4f}"
        print(line)
    print("Prop 11.12 floor check, chi^2_{W_0}(A) = q1 - 1 vs (p-1) 4^-p:")
    for ln in open(sys.argv[1]):
        if ln.startswith("p="):
            parts = ln.split()
            p = int(ln.split("=")[1].split()[0])
            q1m1 = float([t for t in parts if t.startswith("q1-1=")][0].split("=")[1])
            fl = (p - 1) * 4.0 ** (-p)
            print(f"  p={p}: q1-1 = {q1m1:.3e} >= {fl:.3e}: {q1m1 >= fl}")


if __name__ == "__main__":
    main()
