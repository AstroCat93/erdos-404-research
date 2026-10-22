"""t0_validate.py -- validate the library: DP slope-0 counts vs brute force over all paths;
eps by collisions (exact) vs eps by the R3M Fourier-fibre definition (float); chi^2 >= 0.
Usage: python3 t0_validate.py SEED NSAMP"""
import sys, random
from fz_lib import *

seed = int(sys.argv[1]); NS = int(sys.argv[2])
rng = random.Random(seed)
fails = 0; tests = 0
for p in (3, 5, 7):
    R = 40
    pts = [rng.randrange(p ** R) for _ in range(NS)]
    # edge cases: x close to -1, -2, -k
    for k in (1, 2, 3, 4, 5, 6, 7, 9, 12, 14):
        for s in (1, 2, 3, 5):
            pts.append((-k + p ** s * rng.randrange(1, p ** 20)) % p ** R)
    for X in pts:
        for n in (2 * p, 2 * p + 1, min(16, 2 * p + 3), 16):
            if n > 16:
                continue
            Z0, Za = dp_profile(X, p, n)
            b0, ba = brute_profile(X, p, n)
            tests += 1
            if (Z0[n], Za[n]) != (b0, ba):
                fails += 1
                print("MISMATCH dp/brute", p, X, n, Z0[n], Za[n], b0, ba)
    print(f"RESULT dp-vs-brute p={p}: tests so far {tests}, failures {fails}")

# eps: collisions vs Fourier fibres
ef = 0; et = 0; maxrel = 0.0
for p in (3, 5, 7):
    for _ in range(NS):
        X = rng.randrange(p ** 40)
        n = rng.randrange(2 * p, 4 * p)
        N = n + rng.randrange(2, p + 4)
        Np = N + rng.randrange(2, p + 4)
        vl = vals(X, p, Np); V, M = prefix(vl)
        if V[Np] - V[n] > (6 if p == 3 else 4 if p == 5 else 3):
            continue
        e1 = eps_coll(X, p, n, N, Np)
        e2 = eps_fourier(X, p, n, N, Np)
        et += 1
        rel = abs(float(e1) - e2) / max(1e-12, abs(float(e1)) + 1e-12)
        if abs(float(e1) - e2) > 1e-9 * max(1.0, abs(e2)):
            ef += 1
            print("MISMATCH eps", p, X, n, N, Np, e1, e2)
        if e1 < 0:
            ef += 1
            print("FAIL eps<0", p, X, n, N, Np, e1)
        c = chi2(X, p, n, N)
        if c < 0:
            ef += 1
            print("FAIL chi2<0", p, X, n, N, c)
print(f"RESULT eps coll-vs-fourier: {et} tests, {ef} failures")
print(f"SUMMARY t0 dp/brute {tests} tests {fails} fail; eps {et} tests {ef} fail")
