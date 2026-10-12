#!/usr/bin/env python3
"""validate.py -- cross-validate program A (fibcov, all fibre levels k), program B (fibcov2, all
levels kb and several sparse settings) and the brute-force reference (brute.py logic) on small
instances, comparing the exact NUMBER of uncovered residues for every position K tested.
"""
import os
import random
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brute import missing, vfact  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, '..', 'bin')


def runA(p, t, H, k, Ks):
    out = subprocess.run([os.path.join(BIN, 'fibcov'), str(p), str(t), str(H), str(k), 'pos'] + [str(K) for K in Ks],
                         capture_output=True, text=True).stdout
    res = {}
    for line in out.splitlines():
        if line.startswith('A '):
            d = dict(x.split('=') for x in line.split() if '=' in x)
            res[int(d['K'])] = int(d['missing'])
    return res


def runB(p, t, H, kb, sp, Ks):
    out = subprocess.run([os.path.join(BIN, os.environ.get('BPROG', 'fibcov2')), str(p), str(t), str(H), str(kb), str(sp)] + [str(K) for K in Ks],
                         capture_output=True, text=True).stdout
    res = {}
    for line in out.splitlines():
        if line.startswith('B '):
            d = dict(x.split('=') for x in line.split() if '=' in x)
            res[int(d['K'])] = int(d['notcovered'])
    return res


def main():
    random.seed(20261011)
    cases = [(3, 2, 9), (3, 3, 20), (3, 3, 27), (5, 2, 10), (5, 3, 14), (5, 3, 20), (5, 4, 22), (5, 4, 25),
             (7, 2, 5), (7, 3, 15), (7, 3, 19), (7, 4, 22), (7, 4, 26), (11, 3, 14), (11, 3, 18), (11, 4, 22),
             (13, 3, 16), (13, 3, 19), (13, 4, 21), (13, 4, 24), (17, 3, 20), (17, 3, 24), (19, 3, 22), (2, 3, 6), (2, 4, 9)]
    nchk = 0
    nbad = 0
    nfailcases = 0
    for (p, t, H) in cases:
        c = vfact(H - 1, p)
        M = t + c
        if p**M > 3 * 10**7:
            continue
        pc = p**c
        Kall = [K for K in range(1, max(pc, 2) * 3) if K % p]
        Ks = sorted(random.sample(Kall, min(12, len(Kall))))
        ref = {K: missing(p, t, H, K)[1] for K in Ks}
        nfailcases += sum(1 for K in Ks if ref[K] > 0)
        vals = [vfact(H - 1, p) - vfact(H - 1 - i, p) for i in range(H)]
        okk = [k for k in range(0, M + 1) if sum(1 for v in vals if v < k) <= 24]
        for k in okk:
            # A requires PK | elements in U; any k in [0, M] is legal
            rA = runA(p, t, H, k, Ks)
            for K in Ks:
                nchk += 1
                if rA.get(K) != ref[K]:
                    nbad += 1
                    print('MISMATCH A', p, t, H, 'k', k, 'K', K, rA.get(K), ref[K])
        for kb in okk:
            for sp in (0, 1, 3):
                rB = runB(p, t, H, kb, sp, Ks)
                for K in Ks:
                    nchk += 1
                    if rB.get(K) != ref[K]:
                        nbad += 1
                        print('MISMATCH B', p, t, H, 'kb', kb, 'sp', sp, 'K', K, rB.get(K), ref[K])
        print(f'case p={p} t={t} H={H} M={M}: K={Ks} ref_missing={[ref[K] for K in Ks]}', flush=True)
    print(f'VALIDATION comparisons={nchk} mismatches={nbad} (failing (case,K) pairs among references: {nfailcases})')


if __name__ == '__main__':
    main()
