"""HEURISTIC Monte Carlo (Knuth importance-sampling tree estimator) for the Fourier L1 shell sums
T(k) = sum_{u unit mod p^k} prod_{n>=N0} |cos(pi u x_n / p^k)|,  x_n = n!/p^{v(N0!)},
with exact big-integer residues (no size limit on p^k).  NOT a proof.
usage: python3 knuth_big.py p N0 samples seed k1 k2 ...
prints k, mean, stderr, rel.stderr, median of log10(estimates), whether k is a gate shell.
"""
import sys, math, random

def vp(n, p):
    c = 0
    while n % p == 0:
        n //= p; c += 1
    return c

def main():
    p, N0, S, seed = map(int, sys.argv[1:5])
    ks = list(map(int, sys.argv[5:]))
    K = max(ks)
    rnd = random.Random(seed)
    BIG = p ** K
    e0 = sum(vp(i, p) for i in range(1, N0 + 1))
    U = 1
    for i in range(1, N0 + 1):
        m = i
        while m % p == 0: m //= p
        U = U * m % BIG
    els = []
    n, l = N0, 0
    while l < K:
        els.append((l, U))
        n += 1
        m = n
        while m % p == 0:
            m //= p; l += 1
        U = U * m % BIG
    levels = set(l for (l, _) in els)
    print(f"# knuth_big p={p} N0={N0} e0={e0} samples={S} (HEURISTIC)")
    print("# k mean stderr rel median_log10 gate_shell")
    for k in ks:
        PW = [p ** i for i in range(k + 1)]
        bydepth = [[] for _ in range(k + 1)]
        for (l, u) in els:
            if l < k: bydepth[k - l].append(u % PW[k - l])
        gate = (k - 1) not in levels
        ests = []
        for _ in range(S):
            u = 0; est = 1.0
            for d in range(k):
                M = PW[d + 1]; lst = bydepth[d + 1]
                w = []
                for t in range(p):
                    if d == 0 and t == 0:
                        w.append(0.0); continue
                    vv = u + t * PW[d]
                    pr = 1.0
                    for x in lst:
                        pr *= abs(math.cos(math.pi * ((vv * x) % M) / M))
                    w.append(pr)
                tot = sum(w)
                if tot <= 0: est = 0.0; break
                est *= tot
                r = rnd.random() * tot; t = 0
                while t < p - 1 and r >= w[t]:
                    r -= w[t]; t += 1
                u += t * PW[d]
            ests.append(est)
        mean = sum(ests) / S
        var = sum((e - mean) ** 2 for e in ests) / max(1, S - 1)
        se = math.sqrt(var / S)
        logs = sorted(math.log10(e) for e in ests if e > 0)
        med = logs[len(logs) // 2] if logs else float('nan')
        print(f"{k:3d} {mean:.4e} {se:.2e} {se/mean if mean>0 else 0:.3f} {med:.2f} {'GATE' if gate else ''}", flush=True)

main()
