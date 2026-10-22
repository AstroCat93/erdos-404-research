#!/usr/bin/env python3
"""kavg_l2.py -- K'-averaged L^2 for the covering windows of note §3.7 (round 3, track R3F, target (c)).

Window: y_i(K') = prod_{s=1}^{i} (p^t K' - (H-s)), 0 <= i < H; c = v_p((H-1)!); target modulus p^M, M = t + c.
Assume c <= t.  Then y_i(K') == sigma_i + p^t K' tau_i (mod p^M), sigma_i = y_i(0), tau_i = y_i'(0)  (Lemma C1).
For each K' let nu_K' be the uniform measure on the 2^H subset sums mod p^M and
   L2(K') = sum_{xi != 0 mod p^M} |hat nu_K'(xi)|^2 = p^M Coll(K') / 4^H - 1.
(I)  per class (exact): subset-sum counts c(r) mod p^M by DP (int64, exact since 2^H < 2^62), giving the exact
     number of missed residues and L2(K').
(II) averaged identity (exact, independent of (I)): with delta in {-1,0,1}^H (weights 2,1,1),
     A = sum delta_i sigma_i, B = sum delta_i tau_i,
     sum_{K' mod p^c, all} (L2(K') + 1) = p^M 4^{-H} sum_delta w(delta) p^{v} [p^{t+v} | A],  v = min(v_p(B), c)
     computed by a DP over (A mod p^M, B mod p^c)  (only for 4^H < 2^62).
Prints: #units, #failing units (exact), sum over units of L2, the Markov/Parseval bound
   #failing <= p^M * sum_{units} L2(K'),  #units with L2(K') < p^-M (certified covered by the L^2 criterion),
and checks (I) against (II) when (II) is run.
usage: kavg_l2.py p t H [check2d]
"""
import sys, math
import numpy as np
from fractions import Fraction


def vp(n, p):
    if n == 0:
        return 10 ** 9
    c = 0
    while n % p == 0:
        n //= p; c += 1
    return c


def poly_mul_linear(poly, a):
    """poly(X) * (X - a), poly as list of int coefficients (low degree first)"""
    out = [0] * (len(poly) + 1)
    for k, co in enumerate(poly):
        out[k + 1] += co
        out[k] -= a * co
    return out


def window_polys(H):
    polys = []
    cur = [1]
    for i in range(H):
        if i > 0:
            cur = poly_mul_linear(cur, H - i)
        polys.append(cur)
    return polys


def sumsq_exact(c):
    """exact sum of squares of a nonnegative int64 array (entries < 2^64, length < 2^30): 16-bit limbs,
    each limb-product sum is < len * 2^32 < 2^62, combined in Python integers"""
    assert len(c) < (1 << 30)
    u = c.astype(np.uint64)
    limbs = [((u >> np.uint64(16 * j)) & np.uint64(0xFFFF)).astype(np.int64) for j in range(4)]
    tot = 0
    for j in range(4):
        for k in range(4):
            tot += int(np.sum(limbs[j] * limbs[k], dtype=np.int64)) << (16 * (j + k))
    return tot


def subset_counts(ys, M):
    c = np.zeros(M, dtype=np.int64); c[0] = 1
    for y in ys:
        s = y % M
        c = c + np.roll(c, s) if s else 2 * c
    return c


def main():
    p, t, H = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    check2d = len(sys.argv) > 4
    cc = vp(math.factorial(H - 1), p)
    assert cc <= t, "need c <= t"
    assert H <= 61
    Mexp = t + cc; M = p ** Mexp; pc = p ** cc
    polys = window_polys(H)
    sigma = [P[0] for P in polys]
    tau = [P[1] if len(P) > 1 else 0 for P in polys]
    # verify the linearisation on all classes (exact integers)
    for K in range(pc):
        X = p ** t * K
        for i in range(H):
            yi = sum(co * X ** k for k, co in enumerate(polys[i]))
            assert (yi - sigma[i] - X * tau[i]) % M == 0
    units = [K for K in range(pc) if K % p] if cc > 0 else [1]
    # (sum over all K' needed for the identity check; for c = 0 there is one class)
    allK = list(range(pc)) if cc > 0 else [1]
    res = {}
    for K in allK:
        ys = [(sigma[i] + p ** t * K * tau[i]) % M for i in range(H)]
        cnt = subset_counts(ys, M)
        assert int(cnt.sum()) == 2 ** H
        miss = int(np.count_nonzero(cnt == 0))
        coll = sumsq_exact(cnt)
        L2 = Fraction(M * coll, 4 ** H) - 1
        # per-level collision counts: fold counts mod p^M down to mod p^d
        A2 = [Fraction(1)]                       # A2[d] = p^d * Coll_d / 4^H  (d = 0: 1)
        for d in range(1, Mexp + 1):
            cd = cnt.reshape(p ** (Mexp - d), p ** d).sum(axis=0)
            A2.append(Fraction(p ** d * sumsq_exact(cd), 4 ** H))
        Qd = [A2[d] - A2[d - 1] for d in range(1, Mexp + 1)]
        assert sum(Qd) == L2
        res[K] = (miss, L2, Qd)
    nfail = sum(1 for K in units if res[K][0] > 0)
    sumL2u = sum(res[K][1] for K in units)
    certified = sum(1 for K in units if res[K][1] < Fraction(1, M))
    bound = M * sumL2u
    maxL2 = max(res[K][1] for K in units)
    # Cauchy-Schwarz per level: L1(K') <= sum_d sqrt(N_d Q_d(K'));  epsilon bound (C3)
    Nd = [p ** d - p ** (d - 1) for d in range(1, Mexp + 1)]
    cs_cert = sum(1 for K in units if sum(math.sqrt(Nd[d] * float(res[K][2][d])) for d in range(Mexp)) < 1 - 1e-9)
    EQ = [sum(res[K][2][d] for K in units) / len(units) for d in range(Mexp)]
    eps = sum(math.sqrt(Nd[d] * float(EQ[d])) for d in range(Mexp))
    print(f"   per-level E_units Q_d (exact L2 shell, averaged over unit classes):  " + "  ".join(f"d={d+1}:{float(EQ[d]):.3e}" for d in range(Mexp)))
    print(f"   C3 bound: proportion of failing unit classes <= {eps:.4e}  (true proportion {nfail/len(units):.4e});  "
          f"classes certified by per-class C-S (sum_d sqrt(N_d Q_d) < 1): {cs_cert}/{len(units)}")
    print(f"p={p} t={t} H={H} c={cc} M=p^{Mexp}  units={len(units)}  failing(exact)={nfail}  "
          f"sum_units L2={float(sumL2u):.6e}  Markov bound #failing <= {float(bound):.4e}  "
          f"max L2={float(maxL2):.4e} vs p^-M={1/M:.3e}  L2-certified={certified}/{len(units)}  "
          f"random-model L2~{M*2.0**-H:.3e}", flush=True)
    if check2d:
        assert 4 ** H < 2 ** 62
        # DP over (A mod M, B mod pc) with weights 2 (delta=0), 1 (delta=+-1)
        D = np.zeros((M, pc), dtype=np.int64); D[0, 0] = 1
        for i in range(H):
            sa, sb = sigma[i] % M, tau[i] % pc
            D = 2 * D + np.roll(np.roll(D, sa, axis=0), sb, axis=1) + np.roll(np.roll(D, -sa, axis=0), -sb, axis=1)
        assert int(D.sum()) == 4 ** H
        tot = 0
        for a in range(0, M, p ** t):           # p^t | A
            for b in range(pc):
                w = int(D[a, b])
                if not w:
                    continue
                v = min(vp(b, p), cc) if b else cc
                if (a // p ** t) % (p ** v) == 0:
                    tot += w * p ** v
        lhs = sum(res[K][1] + 1 for K in allK)
        rhs = Fraction(M * tot, 4 ** H)
        print(f"   identity check (all K' mod p^c): per-class sum = {float(lhs):.12e}, 2D-walk formula = {float(rhs):.12e}, equal: {lhs == rhs}")


if __name__ == "__main__":
    main()
