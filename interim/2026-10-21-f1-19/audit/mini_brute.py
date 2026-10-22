#!/usr/bin/env python3
"""Own brute force (actual factorials, Python big ints) vs rebuilt A', C', C on small cases.
Miss count = #residues mod p^(v(N*!)-v((N*-H)!)) not hit by subset sums of n!/p^{v((N*-H)!)}, N*-H<=n<N*.
Also checks the jump equals t + v((H-1)!) and class invariance (K and K + p^c give the same count)."""
import subprocess, sys, re, random
W = sys.argv[1]
def v(n, p):
    s = 0
    while n: n //= p; s += n
    return s
def brute(p, t, K, H):
    N = p ** t * K; N0 = N - H
    jump = v(N, p) - v(N0, p)  # v(N!) - v(N0!)
    c = v(H - 1, p); assert jump == t + c, (p, t, K, H)
    Q = p ** jump
    f = 1
    import math
    base = math.factorial(N0); vb = v(N0, p); unit = base // p ** vb
    elems = []
    cur = unit % Q
    x = 1
    for n in range(N0, N):
        if n > N0: x = x * n  # n!/N0!
        elems.append((unit * x) % Q)
    reach = 1  # bitmask over Z/Q
    full = (1 << Q) - 1
    for e in elems:
        e %= Q
        if e: reach |= ((reach << e) | (reach >> (Q - e))) & full
    return Q - bin(reach).count('1')
def run(binary, p, t, H, K, k):
    out = subprocess.run([f'{W}/bin/{binary}', str(p), str(t), str(H), str(k), 'pos', str(K)], capture_output=True, text=True).stdout
    m = re.search(r'(?:missing|miss)=(\d+)', out); return int(m.group(1))
rng = random.Random(404)
cases = []
for p, t in [(5, 2), (5, 3), (7, 2), (7, 3), (3, 3), (3, 4), (11, 2)]:
    for H in range(2, p ** t + 1):
        if v(H - 1, p) + t > 7 or p ** (t + v(H - 1, p)) > 200000: continue
        cases.append((p, t, H))
rng.shuffle(cases); cases = cases[:40]
bad = 0; nfail = 0; n = 0
for p, t, H in cases:
    c = v(H - 1, p); M = t + c
    for K in rng.sample([K for K in range(1, 3 * p ** max(c, 1)) if K % p], 2):
        b = brute(p, t, K, H)
        b2 = brute(p, t, K + p ** c, H) if c else b
        for k in sorted({0, min(1, M), M // 2}):
            r = [run(x, p, t, H, K, k) for x in ('fibcov_ip', 'covchk_ip', 'covchk')]
            n += 1
            if any(x != b for x in r) or b2 != b: bad += 1; print('MISMATCH', p, t, H, K, k, b, b2, r)
        nfail += (b > 0)
print(f'mini_brute: {n} comparisons, {nfail} failing (K,H) cases, {bad} mismatches')
