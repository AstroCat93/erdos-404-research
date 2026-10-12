#!/usr/bin/env python3
"""chain.py -- assemble certified lower bounds for f(1,p) from the coverage logs of program A
(fibcov) and program B (fibcov2/fibcov2b), requiring BOTH programs for every certificate used.

Argument (note.md Lemma 1.3, Theorem 3.12; first-failure form):
  Let N* be the least N > 1 with not P(1,p,N).  Then p | N*; write t = v_p(N*).
  * If Cov(p,t,H) holds uniformly (all unit classes K' mod p^c) and H + 1 < p^t, then
    N* - H >= p^t - H > 1 and P(1,p,N*-H) => P(1,p,N*): contradiction.
  * If N* = p^t K'' and the single block of length H ending at N* covers (position certificate)
    and N* - H > 1, again a contradiction.
  Hence if every multiple N of p with N < p^D is excluded by one of these, then P(1,p,p^D - 1)
  holds and f(1,p) >= v_p((p^D - 1)!).
usage: chain.py SPECFILE         (spec: lines "p D", "uniform t H", "pos t H Kmin Kmax")
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# log directories: colon-separated list in $R3_LOGS (lead's 2026-10-12 change), default ../logs_original
LOGS_LIST = os.environ.get('R3_LOGS', os.path.join(HERE, '..', 'logs_original')).split(':')


def vf(n, p):
    s = 0
    while n:
        n //= p
        s += n
    return s


def collect():
    A, B = {}, {}
    for fn in [f for L in LOGS_LIST for f in glob.glob(os.path.join(L, '*.log'))]:
        for line in open(fn, errors='replace'):
            m = re.match(r"A p=(\d+) t=(\d+) H=(\d+) c=\d+ M=\d+ K=(\d+) missing=(\d+) (COVERED|NOT_COVERED)", line)
            if m:
                p, t, H, K, miss = map(int, m.groups()[:5])
                if miss == 0 and m.group(6) == 'COVERED':
                    A.setdefault((p, t, H), set()).add(K)
                continue
            m = re.match(r"B p=(\d+) t=(\d+) H=(\d+) M=\d+ K=(\d+) notcovered=(\d+) (OK|FAIL)", line)
            if m:
                p, t, H, K, nc = map(int, m.groups()[:5])
                if nc == 0 and m.group(6) == 'OK':
                    B.setdefault((p, t, H), set()).add(K)
    return A, B


def uniform_ok(S, p, t, H):
    c = vf(H - 1, p)
    if c == 0:
        return len(S) > 0
    pc = p ** c
    need = {K for K in range(1, pc) if K % p}
    have = {K % pc for K in S}
    return need <= have


def main():
    spec = [ln.split() for ln in open(sys.argv[1]) if ln.strip() and not ln.startswith('#')]
    A, B = collect()
    p, D = int(spec[0][0]), int(spec[0][1])
    uni = {}
    pos = {}
    ok = True
    for row in spec[1:]:
        if row[0] == 'uniform':
            t, H = int(row[1]), int(row[2])
            a = uniform_ok(A.get((p, t, H), set()), p, t, H)
            b = uniform_ok(B.get((p, t, H), set()), p, t, H)
            cond = H + 1 < p ** t
            print(f"uniform Cov({p},{t},{H}): A={a} B={b} H+1<p^t={cond}")
            if a and b and cond:
                uni[t] = H
            else:
                ok = False
        elif row[0] == 'pos':
            t, H, k0, k1 = map(int, row[1:5])
            Ks = [K for K in range(k0, k1 + 1) if K % p]
            a = all(K in A.get((p, t, H), set()) for K in Ks)
            b = all(K in B.get((p, t, H), set()) for K in Ks)
            cond = all(p ** t * K - H > 1 for K in Ks)
            missA = [K for K in Ks if K not in A.get((p, t, H), set())]
            missB = [K for K in Ks if K not in B.get((p, t, H), set())]
            print(f"positions depth {t}, H={H}, K''={k0}..{k1} ({len(Ks)} positions): A={a} B={b} N*-H>1={cond}"
                  + (f"  missingA={missA[:10]}" if missA else '') + (f"  missingB={missB[:10]}" if missB else ''))
            if a and b and cond:
                pos.setdefault(t, set()).update(Ks)
            else:
                ok = False
    # verify exclusion of every multiple of p below p^D
    for t in range(1, D):
        if t in uni:
            continue
        # need every K'' with p^t K'' < p^D, p not | K''
        need = {K for K in range(1, p ** (D - t)) if K % p}
        if not need <= pos.get(t, set()):
            print(f"depth {t}: NOT all positions below p^{D} certified ({len(need - pos.get(t, set()))} missing)")
            ok = False
    if ok:
        print(f"CHAIN OK: no first failure below {p}^{D}; f(1,{p}) >= v_{p}(({p}^{D}-1)!) = {vf(p**D - 1, p)}")
    else:
        print("CHAIN INCOMPLETE")


if __name__ == '__main__':
    main()
