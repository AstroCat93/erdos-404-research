#!/usr/bin/env python3
"""oddp_window_check_B.py -- second, independent exact test of the odd-p one-window identity
(Proposition R3M-A).  Shares no code with oddp_window_check.py:
  * aliveness and targets are computed by the carry recursion tau_{j+1} = (tau_j - e_j)/(x+j+1)
    in Z/p^k with explicitly tracked precision (no evaluation of S_e);
  * slopes lam_e = v_p(S_e'(x)) are computed from python-flint integer polynomials
    S_e(X) = sum_j e_j (X+1)...(X+j), differentiated symbolically and evaluated mod p^K;
  * the frozen-state weights a_n^(lam) are computed by a residue-distribution DP (convolution),
    not by enumerating subsets.
Statement tested (for every parent e alive at n with slope lam satisfying (W1)-(W3) with L = lam,
and every s mod p^lam):
   p^-D #{(w,f): (e,f) alive at N for x_w, tau_N == s (p^lam)}  ==  2^(N-n) p^-D a_n^(lam)(tau_n(e,x)).
usage: oddp_window_check_B.py p SEED NX n N [DMAX [MAXPAR]]  (MAXPAR: at most this many parents per slope value per x)
"""
import random
import sys
from fractions import Fraction
import flint

K = 110  # base-p precision


def val(a, p):
    if a == 0:
        return 10 ** 6
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k


def carry_walk(x, bits, p, tau=0, prec=K, start=0):
    """Run the carry recursion from time `start` with target tau (known mod p^prec) along `bits`.
    Returns (tau, prec) at the end, or None if the path dies (tau - e not divisible)."""
    for k, e in enumerate(bits):
        j = start + k
        z = x + j + 1
        d = val(z, p)
        t = (tau - e) % p ** prec
        if d > 0:
            if d > prec:
                return None  # cannot decide: treat as error
            if t % p ** d != 0:
                return None
            t //= p ** d
            prec -= d
            u = z // p ** d
        else:
            u = z
        tau = (t * pow(u % p ** prec, -1, p ** prec)) % p ** prec
    return tau, prec


def enum_alive(x, n, p):
    out = []
    stack = [((1,), carry_walk(x, (1,), p))]
    while stack:
        bits, st = stack.pop()
        if st is None:
            continue
        if len(bits) == n:
            out.append((bits, st))
            continue
        tau, prec = st
        for b in (0, 1):
            stack.append((bits + (b,), carry_walk(x, (b,), p, tau, prec, len(bits))))
    return out


def slope(x, bits, p):
    X = flint.fmpz_poly([0, 1])
    S = flint.fmpz_poly([0])
    pi = flint.fmpz_poly([1])
    for j, b in enumerate(bits):
        if b:
            S += pi
        pi = pi * (X + (j + 1))
    dS = S.derivative()
    return val(int(dS(x)) % p ** K, p) if int(dS(x)) % p ** K else K


def frozen_weight(x, n, lam, p):
    """a_n^(lam) as a dict residue -> Fraction, by DP over residues mod p^lam."""
    mod = p ** lam
    dist = {0: 1}
    y = 1
    for i in range(p * lam):
        new = {}
        for r, c in dist.items():
            new[r] = new.get(r, 0) + c
            r2 = (r + y) % mod
            new[r2] = new.get(r2, 0) + c
        dist = new
        y = y * (x + n + i + 1)
    tot = 2 ** (p * lam)
    return {r: Fraction(c, tot) for r, c in dist.items()}


def main():
    p, seed, NX, n, N = (int(a) for a in sys.argv[1:6])
    DMAX = int(sys.argv[6]) if len(sys.argv) > 6 else 5
    MAXPAR = int(sys.argv[7]) if len(sys.argv) > 7 else 10 ** 9
    rnd = random.Random(seed + 1000003)
    done = tries = 0
    nst = okp = totp = 0
    lamh = {}
    while done < NX and tries < 200000:
        tries += 1
        x = rnd.randrange(p ** K)
        vs = [val(x + i, p) for i in range(1, N + 1)]
        m = sum(vs[:n])
        D = sum(vs[n:N])
        Mn, MN = max(vs[:n]), max(vs)
        if D < 1 or D > DMAX or MN >= m:
            continue
        parents = []
        for bits, (tau, prec) in enum_alive(x, n, p):
            lam = slope(x, bits, p)
            if N - n >= p * lam and D + lam <= m - Mn and lam < m - MN:
                parents.append((bits, lam, tau))
        if MAXPAR < 10 ** 9:
            bylam = {}
            for item in parents:
                bylam.setdefault(item[1], []).append(item)
            parents = []
            for lam_, items in sorted(bylam.items()):
                rnd.shuffle(items)
                parents.extend(items[:MAXPAR])
        if not parents:
            continue
        done += 1
        x0 = x % p ** m
        top = x - x % p ** (m + D)
        counts = [{} for _ in parents]
        for w in range(p ** D):
            xw = x0 + p ** m * w + top
            for i, (bits, lam, _) in enumerate(parents):
                st = carry_walk(xw, bits, p)
                if st is None:
                    print("FAIL parent not alive at x_w")
                    continue
                # extend over all f by DFS on the recursion
                stack = [(0, st)]
                while stack:
                    k, s2 = stack.pop()
                    if s2 is None:
                        continue
                    if k == N - n:
                        tN = s2[0] % p ** lam
                        counts[i][tN] = counts[i].get(tN, 0) + 1
                        continue
                    for b in (0, 1):
                        stack.append((k + 1, carry_walk(xw, (b,), p, s2[0], s2[1], n + k)))
        for i, (bits, lam, tau) in enumerate(parents):
            totp += 1
            lamh[lam] = lamh.get(lam, 0) + 1
            a = frozen_weight(x, n, lam, p).get(tau % p ** lam, Fraction(0))
            rhs = Fraction(2 ** (N - n), p ** D) * a
            good = all(Fraction(counts[i].get(s, 0), p ** D) == rhs for s in range(p ** lam))
            nst += p ** lam
            okp += good
            if not good:
                print("MISMATCH", lam, counts[i], rhs)
        print(f"x#{done}: m={m} D={D} parents={len(parents)}", flush=True)
    print(f"RESULT(B) p={p} n={n} N={N}: states tested={nst}; parents exact={okp}/{totp}; lambda histogram {dict(sorted(lamh.items()))}")


if __name__ == "__main__":
    main()
