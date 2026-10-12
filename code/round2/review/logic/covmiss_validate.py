#!/usr/bin/env python3
"""Validate covmiss.c against a numpy brute force on small cases (missing counts must agree)."""
import subprocess, random, numpy as np

def vf(n, p):
    s = 0
    while n:
        n //= p; s += n
    return s

def brute(p, t, H, K):
    c = vf(H - 1, p); M = p ** (t + c); X = p ** t * K
    R = np.zeros(M, dtype=bool); R[0] = True; y = 1
    for i in range(H):
        if i > 0:
            y = (y * (X - (H - i))) % M
        R = R | np.roll(R, y)
    return int(M - R.sum())

rng = random.Random(7)
cases = [(13, 2, 14, 1), (13, 2, 18, 1), (13, 2, 19, 1), (7, 3, 22, 1), (7, 3, 19, 3), (5, 3, 20, 2), (11, 3, 18, 5),
         (3, 2, 9, 1), (5, 2, 9, 1), (7, 2, 12, 2)]
for _ in range(14):
    p = rng.choice([3, 5, 7, 11, 13]); t = rng.randint(1, 3); H = rng.randint(3, min(26, p ** t))
    c = vf(H - 1, p)
    if p ** (t + c) > 3e7:
        continue
    K = rng.randint(1, max(1, p ** max(c, 1) - 1))
    if K % p == 0:
        K += 1
    cases.append((p, t, H, K))
bad = 0
for (p, t, H, K) in cases:
    out = subprocess.run(["./covmiss", str(p), str(t), str(H), str(K)], capture_output=True, text=True).stdout
    m = int(out.strip().split("missing=")[-1])
    b = brute(p, t, H, K)
    print(p, t, H, K, "covmiss", m, "brute", b, "OK" if m == b else "MISMATCH")
    bad += (m != b)
print("mismatches:", bad, "of", len(cases))
