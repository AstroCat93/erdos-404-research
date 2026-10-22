#!/usr/bin/env python3
"""Exact f(a,2) for all even a in [A0, A1] (track R3N, round 3).

For each even a: run program C (dfsW) with K = v2(a!) + G for G = 64, 128, 256, ... until the
run is not reachable; that run prints EXACT f (valid because K > f).  Then certify with the
independent program B (dfsB): K = f must be reachable and K = f+1 must be unreachable with
the same EXACT value.  A witness for K = f (from dfsW) is checked by the exact GMP verifier.
Stops doubling at G > GMAX and reports a lower bound instead.
Usage: python3 -I survey.py A0 A1 GMAX BIN_DIR OUT.csv
"""
import os
import subprocess
import sys
import time


def v2f(n):
    v = 0
    while n:
        n //= 2
        v += n
    return v


def run(binary, a, K, extra=()):
    out = subprocess.run([binary, str(a), str(K), *extra], capture_output=True, text=True).stdout
    reach = None
    exact = None
    for l in out.splitlines():
        if l.startswith('RESULT'):
            reach = 1 if 'reachable=1' in l else 0
        if l.startswith('EXACT'):
            exact = int(l.split(' f=')[1].split()[0])
    return reach, exact


def main():
    A0, A1, GMAX, bindir, outp = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
    C, B, V = f"{bindir}/dfsW", f"{bindir}/dfsB", f"{bindir}/verify_witness_gmp"
    wtmp = f"/tmp/r3_R3N/survey_w_{os.getpid()}.txt"
    with open(outp, 'w') as fo:
        fo.write("a,v2(a!),status,f,g,certB,witness_v2\n")
        for a in range(A0, A1 + 1):
            if a % 2:
                continue
            t0 = time.time()
            va = v2f(a)
            G = 64
            f = None
            while G <= GMAX:
                r, ex = run(C, a, va + G)
                if r == 0:
                    f = ex
                    break
                G *= 2
            if f is None:
                fo.write(f"{a},{va},lower,{va + GMAX},{GMAX},,\n")
                fo.flush()
                print(f"a={a} g>={GMAX} (lower bound only)", flush=True)
                continue
            rb1, _ = run(B, a, f)
            rb0, exb = run(B, a, f + 1)
            certB = (rb1 == 1 and rb0 == 0 and exb == f)
            rc, _ = run(C, a, f, (wtmp,))
            wv = ''
            if f > va:  # nontrivial witness
                out = subprocess.run([V, wtmp, str(a), str(f)], capture_output=True, text=True).stdout
                wv = out.split('v2(sum)=')[1].split()[0] if 'v2(sum)=' in out else 'ERR'
            else:
                wv = str(va)
            fo.write(f"{a},{va},exact,{f},{f - va},{int(certB)},{wv}\n")
            fo.flush()
            if not certB or (wv != 'ERR' and int(wv) != f):
                print(f"PROBLEM a={a} f={f} certB={certB} wv={wv}", flush=True)
            if f - va >= 1000:
                print(f"a={a} f={f} g={f - va} time={time.time() - t0:.1f}s", flush=True)
    try:
        os.remove(wtmp)
    except OSError:
        pass


if __name__ == '__main__':
    main()
