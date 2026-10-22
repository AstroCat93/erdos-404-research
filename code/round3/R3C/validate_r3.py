#!/usr/bin/env python3
"""validate_r3.py (round 3, track R3C) -- cross-validate the covering programs against the
independent big-integer brute force bigbrute.py, comparing EXACT numbers of uncovered residues.

Programs (binaries given by env, default /tmp/r3_R3C/bin):
  A = fibcov  (code/round2/R3/src/fibcov.c)        all legal fibre levels k with |L_k| <= 24
  C = covchk  (code/round2/review/computation/covchk.c)  all k with |L_k| <= 26
  D = covfast (code/round3/R3C/covfast.c)           all k with |L_k| <= 22, several list/zmax settings
usage: validate_r3.py [A,C,D] [seed]
"""
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from bigbrute import missing, legendre  # noqa: E402

BIN = os.environ.get('R3C_BIN', '/tmp/r3_R3C/bin')


def parse(out, tag, key):
    res = {}
    for line in out.splitlines():
        if line.startswith(tag + ' '):
            d = dict(x.split('=', 1) for x in line.split() if '=' in x)
            res[int(d['K'])] = int(d[key].split('+')[0])
    return res


def runA(p, t, H, k, Ks):
    out = subprocess.run([os.path.join(BIN, 'fibcov'), str(p), str(t), str(H), str(k), 'pos'] + [str(K) for K in Ks],
                         capture_output=True, text=True).stdout
    return parse(out, 'A', 'missing')


def runC(p, t, H, k, Ks):
    out = subprocess.run([os.path.join(BIN, 'covchk'), str(p), str(t), str(H), str(k), 'pos'] + [str(K) for K in Ks],
                         capture_output=True, text=True).stdout
    return parse(out, 'C', 'miss')


def runD(p, t, H, k, Ks, env):
    e = dict(os.environ)
    e.update(env)
    out = subprocess.run([os.path.join(BIN, 'covfast'), str(p), str(t), str(H), str(k), 'pos'] + [str(K) for K in Ks],
                         capture_output=True, text=True, env=e).stdout
    return parse(out, 'D', 'missing')


CASES = [(3, 2, 9), (3, 3, 20), (3, 3, 27), (5, 2, 10), (5, 3, 14), (5, 3, 20), (5, 4, 22), (5, 4, 25),
         (7, 2, 5), (7, 3, 15), (7, 3, 19), (7, 4, 22), (7, 4, 26), (11, 3, 14), (11, 3, 18), (11, 4, 22),
         (13, 3, 16), (13, 3, 19), (13, 4, 21), (13, 4, 24), (17, 3, 20), (17, 3, 24), (19, 3, 22),
         (2, 3, 6), (2, 4, 9),
         # p = 29, 31 analogues of the round-3 runs (c = 0 and c = 1, small t)
         (29, 1, 6), (29, 1, 7), (29, 2, 13), (29, 2, 14), (29, 3, 18), (29, 3, 19), (29, 2, 40), (29, 3, 40),
         (29, 3, 33), (29, 4, 36), (29, 4, 45), (31, 2, 13), (31, 2, 14), (31, 3, 19), (31, 3, 45), (31, 4, 41)]


def main():
    progs = (sys.argv[1] if len(sys.argv) > 1 else 'A,C').split(',')
    random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 20261013)
    ncmp = {x: 0 for x in progs}
    nbad = {x: 0 for x in progs}
    nfail_ref = 0
    for (p, t, H) in CASES:
        c = legendre(H - 1, p)
        M = t + c
        if p ** M > 3 * 10 ** 7:
            continue
        pc = p ** c
        Kall = [K for K in range(1, max(pc, 2) * 3 + p) if K % p]
        Ks = sorted(random.sample(Kall, min(8, len(Kall))))
        ref = {K: missing(p, t, H, K)[1] for K in Ks}
        nfail_ref += sum(1 for K in Ks if ref[K] > 0)
        vals = [legendre(H - 1, p) - legendre(H - 1 - i, p) for i in range(H)]
        for k in range(0, M + 1):
            nlo = sum(1 for v in vals if v < k)
            runs = []
            if 'A' in progs and nlo <= 24:
                runs.append(('A', runA(p, t, H, k, Ks)))
            if 'C' in progs and nlo <= 26:
                runs.append(('C', runC(p, t, H, k, Ks)))
            if 'D' in progs and nlo <= 22:
                for env in ({}, {'COVFAST_LISTMAX': '1'}, {'COVFAST_LISTMAX': '64', 'COVFAST_ZMAX': '0'},
                            {'COVFAST_ZMAX': '1000000000'}, {'COVFAST_LISTMAX': '4096', 'COVFAST_ZMAX': '17'}):
                    runs.append(('D', runD(p, t, H, k, Ks, env)))
            for (name, r) in runs:
                for K in Ks:
                    ncmp[name] += 1
                    if r.get(K) != ref[K]:
                        nbad[name] += 1
                        print('MISMATCH', name, p, t, H, 'k', k, 'K', K, r.get(K), ref[K], flush=True)
        print(f'case p={p} t={t} H={H} M={M}: K={Ks} ref_missing={[ref[K] for K in Ks]}', flush=True)
    for x in progs:
        print(f'VALIDATION program {x}: comparisons={ncmp[x]} mismatches={nbad[x]}')
    print(f'failing (case,K) pairs among references: {nfail_ref}')


if __name__ == '__main__':
    main()
