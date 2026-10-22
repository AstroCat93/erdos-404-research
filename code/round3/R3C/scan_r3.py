#!/usr/bin/env python3
"""scan_r3.py (round 3, track R3C) -- minimal uniform H_t scans with TWO programs.

For p, t and H = Hlo..Hhi (stopping after the first H that holds, unless --all):
  * 2^H < p^M                     -> FAIL by counting (proved)
  * (H-1) mod p < rho0(p)         -> FAIL by Lemma 10.11 (proved); not recomputed
  * otherwise program A (fibcov, 'all' mode, stop at the first failing class) decides;
      - if A finds a failing class K: program C (covchk) recomputes that class (pos K) and must
        report the same exact number of missed residues  -> FAIL (two programs)
      - if A covers every class: program C runs over all classes with representatives K'+LIFT*p^c
        (LIFT=2, different from A's)  -> HOLD only if C also reports ALL_COVERED.
Fibre level k: the cost model of the round-2 referee's scan.py (least estimated cost).
usage: scan_r3.py p t Hlo Hhi [--all]
"""
import os
import subprocess
import sys

BIN = os.environ.get('R3C_BIN', '/tmp/r3_R3C/bin')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from predict import rho0  # noqa: E402


def leg(n, p):
    s = 0
    while n:
        n //= p
        s += n
    return s


def choose_k(p, t, H):
    c = leg(H - 1, p)
    M = t + c
    vals = [leg(H - 1, p) - leg(H - 1 - i, p) for i in range(H)]
    best = None
    for k in range(0, M + 1):
        nlo = sum(1 for v in vals if v < k)
        nhi = H - nlo
        F = p ** (M - k)
        if F > 2 ** 33 or nlo > 24:
            continue
        cost = 2.0 ** nlo * 3 + nhi * p ** M / 64.0 + p ** k * 2.0 ** max(0, nlo - 20)
        if best is None or cost < best[0]:
            best = (cost, k)
    return best[1]


def run(cmd, env=None):
    e = dict(os.environ)
    e.update(env or {})
    r = subprocess.run(cmd, capture_output=True, text=True, env=e)
    return r.stdout


def main():
    p, t, Hlo, Hhi = map(int, sys.argv[1:5])
    allH = '--all' in sys.argv
    r0 = rho0(p)
    print(f"# scan p={p} t={t} H={Hlo}..{Hhi} rho0={r0}", flush=True)
    for H in range(Hlo, Hhi + 1):
        if H + 1 >= p ** t:
            print(f"H={H}: H+1 >= p^t, stop"); break
        c = leg(H - 1, p)
        M = t + c
        if 2 ** H < p ** M:
            print(f"p={p} t={t} H={H} c={c} M={M}: FAILS by counting (2^{H} < {p}^{M})", flush=True)
            continue
        if (H - 1) % p < r0:
            print(f"p={p} t={t} H={H} c={c} M={M}: FAILS by Lemma 10.11 ((H-1) mod p = {(H-1) % p} < rho0 = {r0})", flush=True)
            continue
        k = choose_k(p, t, H)
        outA = run([os.path.join(BIN, 'fibcov'), str(p), str(t), str(H), str(k), 'all'], {'FIBCOV_STOP': '1'})
        failA = [l for l in outA.splitlines() if l.startswith('A ') and 'NOT_COVERED' in l]
        sumA = [l for l in outA.splitlines() if l.startswith('SUMMARY')]
        if failA:
            d = dict(x.split('=') for x in failA[0].split() if '=' in x)
            K, missA = int(d['K']), int(d['missing'])
            outC = run([os.path.join(BIN, 'covchk'), str(p), str(t), str(H), str(k), 'pos', str(K)])
            lc = [l for l in outC.splitlines() if l.startswith('C ')]
            dC = dict(x.split('=') for x in lc[0].split() if '=' in x)
            missC = int(dC['miss'])
            agree = 'AGREE' if missC == missA else 'DISAGREE'
            print(f"p={p} t={t} H={H} c={c} M={M} k={k}: FAILS  class K={K}: A missing={missA}, C miss={missC} [{agree}]", flush=True)
            print("    A: " + failA[0], flush=True)
            print("    C: " + lc[0], flush=True)
            continue
        outC = run([os.path.join(BIN, 'covchk'), str(p), str(t), str(H), str(k), 'cls', '2'])
        endC = [l for l in outC.splitlines() if l.startswith('END C')]
        badC = [l for l in outC.splitlines() if l.startswith('C ') and 'UNCOVERED' in l]
        okC = endC and 'ALL_COVERED' in endC[0] and not badC
        verdict = 'HOLDS' if okC else 'A_HOLDS_C_DISAGREES'
        print(f"p={p} t={t} H={H} c={c} M={M} k={k}: {verdict}", flush=True)
        print("    " + sumA[0], flush=True)
        print("    " + (endC[0] if endC else 'C: no END line'), flush=True)
        # keep the full per-class lines in the log
        for l in outA.splitlines():
            if l.startswith('A '):
                print("    " + l)
        for l in outC.splitlines():
            if l.startswith('C '):
                print("    " + l)
        if not allH and okC:
            break


if __name__ == '__main__':
    main()
