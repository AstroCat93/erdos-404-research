#!/usr/bin/env python3
"""Rigorous 'gap' table for f(a,p):  for each a, pick N > a (multiple of p) whose tail set E_N
covers p^{e(N)}Z/p^{e(R)}Z (verified by frontier.py from N0=N up to R).  Then exactly one of:
  * P(a,p,N) false  ->  f(a,p) = max_F v_p(sum_F) over F subset [a,N) with min F = a   (exact, < e(N))
  * P(a,p,N) true   ->  f(a,p) >= e(R).
usage: gap.py p amax extra   (extra = R - N for the frontier runs)"""
import sys, math, subprocess, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
p, amax, extra = map(int, sys.argv[1:4])
def vp(n):
    v = 0
    while n % p == 0: n //= p; v += 1
    return v
def e(N): return sum(vp(k) for k in range(1, N + 1))
cache = {}
def frontier(N):
    if N in cache: return cache[N]
    log = os.path.join(HERE, '..', 'data', f'gap_frontier_p{p}_N{N}.log')
    if os.path.exists(log): os.remove(log)
    T2 = {3: 18, 5: 11, 7: 10}.get(p, 8); tm = {3: 16, 5: 11, 7: 9}.get(p, 7)
    subprocess.run([sys.executable, os.path.join(HERE, 'frontier.py'), str(p), str(N), str(N + extra), str(2 * p * p if p < 5 else p * p), str(tm), str(8 * p + 40), log, '0', str(T2), '7'], capture_output=True, text=True)
    txt = open(log).read()
    m = re.findall(r'FRONTIER .*?\(R=(\d+), e\(R\)=(\d+)\)', txt)
    R, eR = map(int, m[-1])
    cache[N] = (R, eR)
    return cache[N]
rows = []
for a in range(1, amax + 1):
    if vp(a + 1) >= 1:
        rows.append((a, 'trivial (a = -1 mod p)', math.factorial(a) and sum(vp(k) for k in range(1, a + 1)))); continue
    N = (a // p + 1) * p
    # find first N whose frontier reaches beyond N+p*p (i.e. tail looks full) -- try up to 6 candidates
    for _ in range(8):
        R, eR = frontier(N)
        if R >= N + extra - p: break
        N += p
    eN = e(N); Mod = p ** eN
    # DP over subsets of (a, N) of residues mod p^{e(N)} (sum includes a!)
    S = {math.factorial(a) % Mod}
    for n in range(a + 1, N):
        f = math.factorial(n) % Mod
        S |= {(s + f) % Mod for s in S}
    if 0 in S:
        rows.append((a, f'f >= {eR} (P(a,p,{N}) true; E_{N} verified to cover mod p^{eR}, R={R})', None))
    else:
        best = max((vp(s) if s else eN) for s in S)
        rows.append((a, f'f = {best} exactly (P(a,p,{N}) false; v_p(a!)={e(a)})', best))
for r in rows: print(f"p={p} a={r[0]}: {r[1]}")
