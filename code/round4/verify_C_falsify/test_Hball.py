#!/usr/bin/env python3
"""Ball-averaged tests of M4C Proposition H' and of the Lemma-T chain (H' + Lemma P/Q).

On a ball B = z0 + p^r Z_p on which v(z+i) is constant for 1 <= i <= L+L',
with D >= 2r and ceil(D/2) <= K - M (hypothesis (2.2)), compute exactly
  LHS     = E_B[eps(z)],  eps = p^K Coll_K - p^D Coll_D  (composite window, all delta lazy)
  RHS_H'  = c_{L+L'} + sum_j (c_j/2) E_B[Lambda^{(lambda_j)}_{L+L'-j}(z+j)]   (if --exact)
  RHS_T   = c_{L+L'} + sum_j (c_j/2) E_B[ p^{V_t(y)} * (Lemma Q / Lemma P product bound) ]
with exact block maxima and (q2/p^2) per J-block (this is the per-j bound used in
the proof of Lemma T, before the bookkeeping with q-constants).
Checks LHS <= RHS_H' <= ... and LHS <= RHS_T.
"""
import sys, time, random
from fractions import Fraction
sys.path.insert(0, __import__('os').path.dirname(__file__))
from vlib import vp, pis, prob_joint_zero, prob_zero, block_max, gate_data
from qconst_indep import q_exact


def cdiv(a, b):
    return -((-a) // b)


def lemmaQ_bound(p, y, t, k, f, q2):
    """p^k * bound for P(v(R)>=k, v(R')>=f) with delta_0 = 1 fixed (Lemma Q if f>=1 and
    hypotheses hold, else Lemma P)."""
    P, D = pis(y, t)
    gates, depths, levels, blocks = gate_data(y, t, p)
    I = len(gates)
    dmax = max(depths) if depths else 0
    useQ = (f >= 1 and f < k and f <= k - dmax)
    J = [i for i in range(1, I) if depths[i] == 1 and levels[i] < f] if useQ else []
    bd = Fraction(1)
    for i in range(I + 1):
        li = levels[i]
        if li >= k:
            continue
        lnext = levels[i + 1] if i + 1 <= I else 10 ** 9
        e = min(lnext, k) - li
        if i in J:
            bd *= q2 / p ** 2
        else:
            vals = [P[c] // p ** li for c in blocks[i]]
            bd *= block_max(vals, e, p, fixed_first=(i == 0))
    return p ** k * bd, len(J), useQ


def run(p, z0, r, L, Lp, exact, q2):
    t0 = time.time()
    T = L + Lp
    vals = [vp(z0 + i, p) for i in range(1, T + 1)]
    assert all(v < r for v in vals), "valuations not constant on B"
    D = sum(vals[:L]); K = sum(vals); M = max(vals)
    h = cdiv(D, 2)
    assert D >= 2 * r and h <= K - M, ("(2.2) fails", D, r, K, M)
    Vz = [0] * (T + 1)
    for c in range(1, T + 1):
        Vz[c] = Vz[c - 1] + vals[c - 1]
    zs = [z0 % p ** r + p ** r * w for w in range(p ** (K - r))]
    lhs = Fraction(0); rhsT = Fraction(0); rhsH = Fraction(0)
    nJ = 0
    for z in zs:
        Pz, Dz = pis(z, T)
        a = [x % p ** K for x in Pz]
        collK = prob_zero(a, K, p)
        collD = prob_zero([x % p ** D for x in a], D, p)
        lhs += p ** K * collK - p ** D * collD
        # RHS terms
        sT = Fraction(1, 2 ** T) * p ** K
        sH = Fraction(1, 2 ** T) * p ** K
        for j in range(T):
            cj = Fraction(p ** Vz[j], 2 ** j)
            y = z + j; t = T - j
            k = K - Vz[j]           # = V_t(y)
            lam = h - Vz[j]
            bnd, nj, useQ = lemmaQ_bound(p, y, t, k, lam, q2)
            nJ += nj
            sT += cj / 2 * bnd
            if exact:
                Py, Dy = pis(y, t)
                aa = [x % p ** k for x in Py]
                if lam >= 1:
                    bb = [x % p ** lam for x in Dy]
                    pr = prob_joint_zero(aa, bb, k, lam, p, fixed0=True)
                else:
                    pr = prob_zero(aa, k, p, fixed0=True)
                sH += cj / 2 * p ** k * pr
        rhsT += sT; rhsH += sH
    n = len(zs)
    lhs /= n; rhsT /= n; rhsH /= n
    ok1 = lhs <= rhsT
    msg = "p=%d z0=%d r=%d L=%d L'=%d D=%d K=%d M=%d |B mod p^K|=%d: E_B eps = %.6e" % (p, z0 % p ** 6, r, L, Lp, D, K, M, n, float(lhs))
    if exact:
        msg += "  RHS_H' = %.6e (LHS<=RHS_H': %s)" % (float(rhsH), lhs <= rhsH)
        msg += "  RHS_T = %.6e (RHS_H'<=RHS_T: %s)" % (float(rhsT), rhsH <= rhsT)
    else:
        msg += "  RHS_T = %.6e" % float(rhsT)
    msg += "  LHS<=RHS_T: %s  (J-blocks used: %d)  [%.0fs]" % (ok1, nJ, time.time() - t0)
    print(msg, flush=True)
    return ok1


def main():
    p = int(sys.argv[1]); nballs = int(sys.argv[2]); exact = (sys.argv[3] == 'exact')
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    rng = random.Random(31 * p + seed)
    q2, _, _ = q_exact(p, 2)
    for bi in range(nballs):
        g1 = rng.choice([1, 2, p - 1, p, rng.randrange(1, p + 1)]) if not (exact and p >= 7) else 1
        # z0 = -g1 + p*u with u + i != 0 mod p for the first 6 gates -> all gates depth 1
        while True:
            u = rng.randrange(p ** 20)
            if all((u + i) % p != 0 for i in range(0, min(6, p - 1))):
                break
        z0 = -g1 + p * u
        r = 2
        # first window: 4 gates (D = 4 = 2r); second window: 1 more gate (K = 5)
        L = g1 + 3 * p + rng.randrange(0, p)          # contains gates g1, g1+p, g1+2p, g1+3p
        Lp = (g1 + 4 * p) - L + rng.randrange(0, p)   # reaches gate g1+4p, not g1+5p
        run(p, z0, r, L, Lp, exact, q2)


if __name__ == "__main__":
    main()
