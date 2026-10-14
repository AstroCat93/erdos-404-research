#!/usr/bin/env python3
"""fe_crosscheck.py -- second code path for the numbers of phases 0-2 of fe_verify.py: recomputes chi^2_0, the
Prop D bounds eps_bar_l (l <= L1) and the Prop E bound for the first Markov windows with exact Fractions via
bounds.py (per-c Lemma Q loop with the running maximum M, i.e. the form proved in the report; fe_lib.py uses
suffix products and the window maximum M_W instead).  The c-sum is truncated at c* with the exact tail bound
2^-c* p^top (each term is at most 2^-c-1 p^top).
usage: fe_crosscheck.py ATOMFILE LMAX L1 [RNUM RDEN]
"""
import math
import sys
from fractions import Fraction

from bounds import qconsts, block0_table, lemmaQ_bound
from m4a_lib import vp


def bound_trunc(depth, V, n, N2, top, th, b, p, q, P0):
    H = N2 - n
    a = [V[n + c] - V[n] for c in range(H)]
    cstar = min(H, int(top * math.log2(p)) + 250)
    tot = Fraction(1, 2 ** H)
    for c in range(cstar):
        w = Fraction(1, 2 ** (c + 1))
        if a[c] >= top:
            tot += w
        else:
            f = th - a[c] if th > 0 else 0
            G = lemmaQ_bound(depth, n + c, H - c, top - a[c], f, p, q, P0)   # = p^(top-a_c) * prob
            tot += w * G / p ** (top - a[c])
    if cstar < H:
        tot += Fraction(1, 2 ** cstar)
    return p ** top * tot


def main():
    atomfile, LMAX, L1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    RNUM, RDEN = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (27, 20)
    kv = dict(line.split('=', 1) for line in open(atomfile).read().split() if '=' in line)
    p, n0, xA, m = int(kv['p']), int(kv['n0']), int(kv['xA']), int(kv['m'])
    q = qconsts(p, 8)
    P0 = block0_table(p, 12)
    times = [n0]
    for _ in range(LMAX + 2):
        times.append(-((-RNUM * times[-1]) // RDEN))
    NM = times[LMAX + 1]
    depth = [0] + [vp(xA + i, p) for i in range(1, NM + 1)]
    V = [0] * (NM + 1)
    for i in range(1, NM + 1):
        V[i] = V[i - 1] + depth[i]
    D0 = V[times[1]] - V[times[0]]
    chi = bound_trunc(depth, V, times[0], times[1], D0, 0, None, p, q, P0) - 1
    print(f"chi^2_0 <= {float(chi):.6g}", flush=True)
    logPi = math.log10(1 + chi)
    for l in range(1, LMAX + 1):
        n, N, N2 = times[l - 1], times[l], times[l + 1]
        D, K = V[N] - V[n], V[N2] - V[n]
        if l <= L1:
            bD = bound_trunc(depth, V, n, N2, K, 0, None, p, q, P0)
            logPi += math.log10(bD)    # 1 + eps_bar = p^K Coll_K bound
            print(f"l={l} [{n},{N},{N2}) D={D} K={K} eps_bar(PropD) = {float(bD - 1):.4g}", flush=True)
        else:
            th = min((D + 1) // 2, D - m + 1)
            e = bound_trunc(depth, V, n, N2, K, th, m, p, q, P0)
            print(f"l={l} [{n},{N},{N2}) D={D} K={K} theta={th} log10 E_A eps <= {math.log10(e):.3f}", flush=True)
    print(f"RESULT log10[(1+chi^2_0) prod_(l<=L1)(1+eps_bar_l)] = {logPi:.4f}")


if __name__ == "__main__":
    main()
