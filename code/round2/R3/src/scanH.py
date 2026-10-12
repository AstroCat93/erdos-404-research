#!/usr/bin/env python3
"""scanH.py -- for given p, t and an H range, decide Cov(p,t,H) (uniform over all unit classes
K' mod p^c) with program A, choosing the fibre level k automatically.  For each H prints
HOLDS / FAILS (with the first failing class found).  Optional full mode counts all failing
classes and the total number of missing residues (used for the failure-structure analysis).
usage: scanH.py p t Hlo Hhi [full] [maxQbits_log2]
"""
import math
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, '..', 'bin', 'fibcov')


def vfact(n, p):
    s = 0
    while n:
        n //= p
        s += n
    return s


def choose_k(p, t, H):
    c = vfact(H - 1, p)
    M = t + c
    vals = [c - vfact(H - 1 - i, p) for i in range(H)]
    vals = [vfact(H - 1, p) - vfact(H - 1 - i, p) for i in range(H)]
    best = None
    for k in range(0, M + 1):
        nL = sum(1 for v in vals if v < k)
        nU = H - nL
        F = p ** (M - k)
        if 2 * F / 8 > 3e9 or nL > 36:
            continue
        speed = 60e9 if F / 8 <= 12e6 else 25e9
        cost = (2 ** nL) * 4e-9 + nU * (p ** M) / 8 / speed + (p ** k) * 2e-6
        if best is None or cost < best[0]:
            best = (cost, k)
    return best


def run(p, t, H, full):
    c = vfact(H - 1, p)
    M = t + c
    bk = choose_k(p, t, H)
    if bk is None:
        return None
    est, k = bk
    env = dict(os.environ)
    if not full:
        env['FIBCOV_STOP'] = '1'
        env['FIBCOV_FIBRESTOP'] = '1'
    t0 = time.time()
    r = subprocess.run([A, str(p), str(t), str(H), str(k), 'all'], capture_output=True, text=True, env=env)
    el = time.time() - t0
    lines = r.stdout.splitlines()
    summ = [ln for ln in lines if ln.startswith('SUMMARY')]
    fails = [ln for ln in lines if 'NOT_COVERED' in ln]
    nK = sum(1 for ln in lines if ln.startswith('A '))
    ratio = 2 ** H / p ** M
    return dict(H=H, c=c, M=M, k=k, ratio=ratio, holds=(len(summ) == 1 and 'ALL_COVERED' in summ[0]),
                fails=fails, nchecked=nK, secs=el, summary=summ[0] if summ else r.stderr[-300:])


def main():
    p, t, lo, hi = map(int, sys.argv[1:5])
    full = len(sys.argv) > 5 and sys.argv[5] == 'full'
    maxlog = float(sys.argv[6]) if len(sys.argv) > 6 else 41.5
    for H in range(lo, hi + 1):
        if H > p ** t:
            break
        c = vfact(H - 1, p)
        M = t + c
        if 2 ** H < p ** M:
            print(f"p={p} t={t} H={H} c={c} M={M} ratio={2**H/p**M:.3g}  FAILS (counting: 2^H < p^M)", flush=True)
            continue
        if M * math.log2(p) > maxlog:
            print(f"p={p} t={t} H={H} c={c} M={M}  SKIPPED (p^M too large)", flush=True)
            continue
        res = run(p, t, H, full)
        if res is None:
            print(f"p={p} t={t} H={H} c={c} M={M}  SKIPPED (no feasible k)", flush=True)
            continue
        tag = 'HOLDS' if res['holds'] else 'FAILS'
        extra = ''
        if res['fails']:
            extra = ' first_fail: ' + res['fails'][0].split(' K=')[1].split(' [')[0]
            if full:
                extra = f" failing_classes={len(res['fails'])}/{res['nchecked']}" + extra
        print(f"p={p} t={t} H={H} c={c} M={M} k={res['k']} ratio={res['ratio']:.3g} classes_checked={res['nchecked']} {tag}{extra} [{res['secs']:.1f}s]", flush=True)


if __name__ == '__main__':
    main()
