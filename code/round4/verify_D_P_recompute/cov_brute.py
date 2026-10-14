#!/usr/bin/env python3
"""Brute-force validator for covchk.c: subset sums by numpy boolean roll (no bitset
tricks), compared class by class (number of missed residues) with covchk output."""
import subprocess, sys
import numpy as np

def vp(n, p):
    v = 0
    while n % p == 0:
        n //= p; v += 1
    return v

def brute_missing(p, t, H, K):
    c = sum(vp(s, p) for s in range(1, H))
    Q = p ** (t + c)
    S = np.zeros(Q, dtype=bool); S[0] = True
    y = 1
    for i in range(H):
        if i > 0:
            y = y * (p ** t * K - (H - i)) % Q
        S = S | np.roll(S, y % Q)
    return Q - int(S.sum())

def run_c(exe, p, t, H, mode=None, arg=None):
    cmd = [exe, str(p), str(t), str(H)] + ([mode] if mode else []) + ([str(arg)] if arg is not None else [])
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    res = {}
    for l in out.splitlines():
        if l.startswith("K="):
            f = dict(kv.split("=") for kv in l.split()[:3])
            res[int(f["K"])] = int(f["missing"])
    return res

def main():
    exe = sys.argv[1]
    cases = [(3,1,2),(3,2,9),(3,2,8),(5,1,3),(5,1,2),(5,2,10),(5,2,9),(5,3,20),(5,3,19),(7,1,4),(7,1,3),(7,2,7),(7,2,6),
             (7,3,19),(7,3,18),(7,3,17),(7,4,26),(7,4,25),(11,1,5),(11,1,4),(11,2,10),(11,3,18),(11,3,17),
             (13,1,6),(13,1,5),(13,2,10),(13,2,13),(13,2,14),(13,2,18),(13,2,19),(13,3,19),(17,2,11),(19,2,12),(23,2,12),(23,2,11)]
    ok = True; nfail_cases = 0; nclasses = 0
    for (p, t, H) in cases:
        c = sum(vp(s, p) for s in range(1, H))
        r = run_c(exe, p, t, H)
        Ks = [K for K in range(1, max(2, p ** c)) if p ** c == 1 or K % p]
        if p ** c == 1: Ks = [1]
        mism = 0; bad = 0
        for K in Ks:
            b = brute_missing(p, t, H, K)
            if r.get(K) != b: mism += 1
            if b: bad += 1
        nclasses += len(Ks)
        if bad: nfail_cases += 1
        print(f"Cov({p},{t},{H}) c={c}: classes {len(Ks)}, brute not-covered {bad}, mismatches {mism}")
        ok &= (mism == 0 and len(r) == len(Ks))
    # class invariance / lifted representatives
    for (p, t, H, j) in [(7,3,18,5),(7,3,18,123457),(7,4,25,3),(13,2,14,7),(5,3,19,11)]:
        c = sum(vp(s, p) for s in range(1, H))
        r0 = run_c(exe, p, t, H); rl = run_c(exe, p, t, H, "lift", j)
        mism = sum(1 for K in r0 if rl.get(K + j * p ** c) != r0[K])
        mism2 = sum(1 for K in list(r0)[:10] if brute_missing(p, t, H, K + j * p ** c) != r0[K])
        print(f"lift j={j} Cov({p},{t},{H}): classes {len(r0)}, lifted-vs-base mismatches {mism}, brute(lifted, 10 classes) mismatches {mism2}")
        ok &= (mism == 0 and mism2 == 0)
    print(f"{nclasses} classes compared; {nfail_cases} configurations with failing classes")
    print("VALIDATION", "OK" if ok else "FAILED")
main()
