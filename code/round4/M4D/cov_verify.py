#!/usr/bin/env python3
"""cov_verify.py -- independent re-check (own code: bitset rotate-or in bin/liftprof) of the round-2 uniform
covering certificates Cov(p,t,H) used in Theorem P of data/round4/reports/M4D.md:
   for every unit K' mod p^c (c = v_p((H-1)!)), the subset sums of y_i(K') = prod_{s=1}^{i} (p^t K' - (H-s)),
   0 <= i < H, cover Z/p^(t+c).
Mode 'all' checks every unit class; mode 'sample:k:seed' checks k random unit classes (plus K'=1).
Also accepts a list of extra (K') to check, e.g. a known failing class (negative control).
usage: cov_verify.py p t H mode [extraK ...]
"""
import os
import random
import subprocess
import sys

CBIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bin', 'liftprof')


def vfact(n, p):
    s, q = 0, p
    while q <= n:
        s += n // q
        q *= p
    return s


def missed(p, t, H, K1):
    c = vfact(H - 1, p)
    mod = p ** (t + c)
    X = p ** t * K1
    ys = []
    y = 1
    for i in range(H):
        ys.append(y % mod)
        y = y * (X - (H - (i + 1))) % mod
    inp = f"{p} {t + c} 0 {H} " + " ".join(str(v) for v in ys)
    out = subprocess.run([CBIN], input=inp, capture_output=True, text=True, check=True).stdout.split()
    return mod - int(out[1]), mod


def main():
    p, t, H = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    mode = sys.argv[4]
    extra = [int(k) for k in sys.argv[5:]]
    c = vfact(H - 1, p)
    units = [k for k in range(1, p ** c + 1) if k % p] if c > 0 else [1]
    if mode == 'all':
        todo = units
    else:
        _, k, sd = mode.split(':')
        rnd = random.Random(int(sd))
        todo = sorted(set([1] + rnd.sample(units, min(int(k), len(units)))))
    fails = []
    for K1 in todo:
        m, mod = missed(p, t, H, K1)
        if m:
            fails.append((K1, m))
    print(f"RESULT cov_verify p={p} t={t} H={H} c={c} modulus=p^{t + c} mode={mode}: classes checked={len(todo)} "
          f"of {len(units)}, classes with misses={len(fails)} {fails[:5]}")
    for K1 in extra:
        m, mod = missed(p, t, H, K1)
        print(f"RESULT cov_verify extra p={p} t={t} H={H} K'={K1}: missed residues={m} of {mod}")


if __name__ == "__main__":
    main()
