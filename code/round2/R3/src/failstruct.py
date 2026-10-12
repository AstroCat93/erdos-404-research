#!/usr/bin/env python3
"""failstruct.py -- structure of covering failures (R3-frontier).

Runs program A over all unit classes K' mod p^c for (p,t,H) (or given K list), dumping up to
DUMP missing residues per failing class, and reports:
  * number / list of failing classes, and their residues K' mod p and mod p^2;
  * total number of missing residues;
  * distribution of the missing x mod p, compared with argmin of the level-1 multiplicity m_1
    (bottleneck.py), and the fraction of missing x lying in argmin classes;
  * symmetry x <-> S_tot(K) - x of the missing set (S_tot = sum of all block elements).
usage: failstruct.py p t H k [DUMP] [K ...]
"""
import os
import re
import subprocess
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from bottleneck import profile, vf  # noqa: E402

A = os.path.join(HERE, '..', 'bin', 'fibcov')


def main():
    p, t, H, k = map(int, sys.argv[1:5])
    dump = int(sys.argv[5]) if len(sys.argv) > 5 else 200
    Ks = sys.argv[6:]
    env = dict(os.environ, FIBCOV_DUMP=str(dump))
    args = [A, str(p), str(t), str(H), str(k)] + (['pos'] + Ks if Ks else ['all'])
    out = subprocess.run(args, capture_output=True, text=True, env=env).stdout
    c = vf(H - 1, p)
    M = t + c
    Q = p ** M
    miss = {}
    tot = {}
    nK = 0
    for line in out.splitlines():
        m = re.match(r"\s+MISS K=(\d+) x=(\d+)", line)
        if m:
            miss.setdefault(int(m.group(1)), []).append(int(m.group(2)))
        m = re.match(r"A .* K=(\d+) missing=(\d+)", line)
        if m:
            nK += 1
            if int(m.group(2)):
                tot[int(m.group(1))] = int(m.group(2))
    prof = profile(p, t, H, kmax=min(2, c, t))
    am1 = set(prof['levels'][1]['argmin']) if 1 in prof['levels'] else set()
    print(f"p={p} t={t} H={H} c={c} M={M} rho={(H-1)%p} R0={prof['R0']:.3g} R*={prof['Rstar']:.3g} classes={nK} failing={len(tot)}")
    if not tot:
        return
    fk = sorted(tot)
    print("  failing K' (first 40):", fk[:40])
    print("  failing K' mod p:", dict(sorted(Counter(K % p for K in fk).items())))
    print("  total missing residues:", sum(tot.values()), " per failing class (first 20):", [tot[K] for K in fk[:20]])
    allx = [(K, x) for K, xs in miss.items() for x in xs]
    xm = Counter(x % p for K, x in allx)
    print("  dumped missing x:", len(allx), " distribution of x mod p:", dict(sorted(xm.items())))
    if am1:
        inarg = sum(1 for K, x in allx if x % p in am1)
        print(f"  argmin_r m_1(r) = {sorted(am1)};  fraction of dumped missing x with x mod p in argmin: {inarg}/{len(allx)}")
    # symmetry check per class (only meaningful when the dump is complete for that class)
    symok = 0
    symtested = 0
    for K, xs in miss.items():
        if len(xs) != tot.get(K, -1):
            continue
        y = [1]
        for i in range(1, H):
            y.append(y[-1] * (p ** t * K - (H - i)) % Q)
        S = sum(y) % Q
        sx = set(xs)
        symtested += 1
        symok += all(((S - x) % Q) in sx for x in xs)
    print(f"  symmetry x -> S_tot - x holds for {symok}/{symtested} completely dumped classes")


if __name__ == '__main__':
    main()
