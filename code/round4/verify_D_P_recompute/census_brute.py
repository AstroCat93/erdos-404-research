#!/usr/bin/env python3
"""Brute-force validator for census.c: g_p(c) >= G iff -1 is a subset sum of
{pi_b(c) mod p^G : 1 <= b < pG} (terms with b >= pG vanish mod p^G since
v(pi_b) >= floor(b/p)).  Compares with `census p G check` output, class by class."""
import subprocess, sys
import numpy as np

def brute(p, G):
    M = p ** G
    out = []
    for c in range(M):
        S = np.zeros(M, dtype=bool); S[0] = True
        pi = 1
        for b in range(1, p * G):
            pi = pi * (c + b) % M
            if pi:
                S = S | np.roll(S, pi)
        out.append(1 if S[M - 1] else 0)
    return out

def main():
    exe = sys.argv[1]
    ok = True
    for p, G in [(3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (5, 1), (5, 2), (5, 3), (5, 4), (7, 1), (7, 2), (7, 3), (7, 4),
                 (11, 1), (11, 2), (11, 3), (13, 1), (13, 2), (13, 3), (17, 2), (19, 2), (23, 2)]:
        res = subprocess.run([exe, str(p), str(G), "check"], capture_output=True, text=True, check=True).stdout.split("\n")
        dfs = [int(l.split()[1]) for l in res if l.strip()]
        bf = brute(p, G)
        mism = sum(1 for a, b in zip(dfs, bf) if a != b)
        print(f"p={p} G={G}: classes {len(bf)}, survivors brute {sum(bf)}, dfs {sum(dfs)}, mismatches {mism}")
        ok &= (mism == 0 and len(dfs) == len(bf))
    print("VALIDATION", "OK" if ok else "FAILED")
main()
