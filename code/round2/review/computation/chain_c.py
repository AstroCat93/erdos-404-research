#!/usr/bin/env python3
"""Referee's chain check (Prop 10.10) from PROGRAM C logs only (logs/*.log).
For each claimed bound: every N = p^t K'' < p^D (t>=1, p !| K'') must be excluded either by a
uniform certificate Cov(p,t,H) over ALL unit classes mod p^c with H+1 < p^t, or by a position
certificate for exactly that K'' with N - H > 1."""
import glob, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
def leg(n, p):
    s = 0
    while n:
        n //= p; s += n
    return s
cov = {}   # (p,t,H) -> {'K': set of K covered, 'Kpc': set of K mod p^c covered, 'bad': set}
for fn in glob.glob(os.path.join(HERE, 'logs', '*.log')):
    for ln in open(fn):
        m = re.match(r"C p=(\d+) t=(\d+) H=(\d+) M=\d+ K=(\d+) Kmodpc=(\d+) miss=(\d+)(\S*) (COVERED|UNCOVERED)", ln)
        if not m:
            continue
        p, t, H, K, Kpc, miss = map(int, m.groups()[:6])
        d = cov.setdefault((p, t, H), {'K': set(), 'Kpc': set(), 'bad': set()})
        if miss == 0 and m.group(8) == 'COVERED' and not m.group(7):
            d['K'].add(K); d['Kpc'].add(Kpc)
        else:
            d['bad'].add(K)
def uniform(p, t, H):
    c = leg(H - 1, p); pc = p ** c
    d = cov.get((p, t, H))
    if not d:
        return False
    need = {K for K in range(1, pc) if K % p} if c > 0 else {0}
    return need <= d['Kpc'] and H + 1 < p ** t
def position(p, t, H, K):
    d = cov.get((p, t, H))
    return bool(d) and K in d['K'] and p ** t * K - H > 1
plans = {
    7: (9, {1: 4, 2: 7, 3: 19, 4: 26, 5: 28, 6: 34}, {7: 40, 8: 47}),
    11: (9, {1: 5, 2: 10, 3: 18, 4: 22, 5: 30, 6: 33}, {7: 40, 8: 44}),
    13: (9, {1: 6, 2: 10, 3: 19, 4: 24, 5: 32, 6: 35, 7: 39}, {8: 47}),
    17: (9, {1: 5, 2: 11, 3: 16, 4: 25, 5: 30, 6: 34, 7: 43}, {8: 47}),
    19: (8, {1: 5, 2: 12, 3: 17, 4: 27, 5: 31, 6: 35}, {7: 45}),
    23: (8, {1: 7, 2: 12, 3: 18, 4: 23, 5: 33, 6: 37}, {7: 43}),
}
for p, (D, uni, posH) in plans.items():
    ok = True; notes = []
    for t in range(1, D):
        if t in uni:
            if not uniform(p, t, uni[t]):
                ok = False; notes.append(f"uniform t={t} H={uni[t]} missing")
            continue
        H = posH[t]
        for K in range(1, p ** (D - t)):
            if K % p == 0:
                continue
            if position(p, t, H, K):
                continue
            if p == 11 and t == 7 and K == 37 and position(p, t, 41, K):
                continue
            ok = False; notes.append(f"pos t={t} K={K}")
    print(f"p={p} D={D}: {'CHAIN OK  f(1,p) >= ' + str(leg(p**D - 1, p)) if ok else 'INCOMPLETE'} {notes[:8]}{' ...' if len(notes) > 8 else ''}")
