#!/usr/bin/env python3
"""Exact test of M4C Lemma H2 (report §2) at p = 7, 11, 13.

  p^K mu_B{v(F)>=K} - p^D mu_B{v(F)>=D}  <=  p^K mu_B{v(F)>=K, 2 v(F')>=D}
for F in Z[X], B = b + p^r Z_p, 2r <= D < K.
Measures are exact: F(y) mod p^K depends on y mod p^K, so mu_B is a count over
the p^(K-r) residues y mod p^K in B (resp. p^(D-r) residues for level D).
Families of F:
  'Tdelta'  : signed window sums sum_c delta_c pi_c(X) (random lazy delta),
  'dbl'     : (X-a)^2 G(X) + p^m H(X), a in B (planted near-double roots),
  'tri'     : (X-a)^3 G(X) + p^m H(X),
  'gate2'   : (X+2)^2-type paths delta=(1,1,1,0..) + small perturbation, B near -2,
  'rand'    : random integer polynomials of degree <= 6.
Control: the same inequality with 2v(F') >= D+2 on the right (must fail
sometimes, showing the test can detect a wrong threshold).
"""
import sys, random, time
import numpy as np


def eval_poly_coeffs(coeffs, ys, m):
    """Horner, coefficients low->high, exact mod m (m^2 < 2^63)."""
    acc = np.zeros_like(ys)
    for c in reversed(coeffs):
        acc = (acc * ys + (c % m)) % m
    return acc


def deriv(coeffs):
    return [i * coeffs[i] for i in range(1, len(coeffs))]


def polymul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r


def polyadd(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]


def pi_poly(c):
    r = [1]
    for i in range(1, c + 1):
        r = polymul(r, [i, 1])
    return r


def counts(F, Fd, p, b, r, K, D, h):
    """returns (#{y in B mod p^K: F=0 mod p^K}, #{y in B mod p^D: F=0 mod p^D},
               #{y in B mod p^K: F=0 mod p^K, F'=0 mod p^h}, same with h+1)"""
    mK = p ** K; mD = p ** D
    ys = (b % p ** r + p ** r * np.arange(p ** (K - r), dtype=np.int64)) % mK
    FK = eval_poly_coeffs(F, ys, mK)
    zK = (FK == 0)
    nK = int(zK.sum())
    ysD = (b % p ** r + p ** r * np.arange(p ** (D - r), dtype=np.int64)) % mD
    nD = int((eval_poly_coeffs(F, ysD, mD) == 0).sum())
    Fdv = eval_poly_coeffs(Fd, ys, mK)
    nKh = int((zK & (Fdv % p ** h == 0)).sum())
    nKh1 = int((zK & (Fdv % p ** (h + 1) == 0)).sum())
    return nK, nD, nKh, nKh1


def main():
    p = int(sys.argv[1]); ntr = int(sys.argv[2]); Kmax = int(sys.argv[3])
    rng = random.Random(4242 + p)
    fams = ['Tdelta', 'dbl', 'tri', 'gate2', 'rand']
    stats = {f: [0, 0, 0, 0, 0.0] for f in fams}  # trials, fails, lhs>0, ctrl viol, max ratio
    t0 = time.time()
    for tr in range(ntr):
        fam = fams[tr % len(fams)]
        r = rng.choice([1, 1, 2, 2, 3])
        D = 2 * r + rng.choice([0, 0, 1, 2])
        K = D + rng.choice([1, 1, 2, 3])
        if K > Kmax or p ** K > 3_000_000:
            continue
        b = rng.randrange(p ** 12)
        if fam == 'Tdelta':
            t = rng.randrange(3, 4 * p)
            F = [0]
            for c in range(t):
                dlt = rng.choice([0, 0, 1, -1])
                if c == 0:
                    dlt = 1
                if dlt:
                    F = polyadd(F, [dlt * x for x in pi_poly(c)])
            if rng.random() < 0.5:
                b = -rng.randrange(1, t + 1) + p ** rng.randrange(1, 4) * rng.randrange(p ** 6)  # B near a gate
        elif fam in ('dbl', 'tri'):
            a = b + p ** r * rng.randrange(p ** 8)
            G = [rng.randrange(-p ** 6, p ** 6) for _ in range(rng.randrange(1, 4))]
            H = [rng.randrange(-p ** 6, p ** 6) for _ in range(rng.randrange(1, 5))]
            m = rng.randrange(r, K + 2)
            base = [-a, 1]
            F = polymul(polymul(base, base), G)
            if fam == 'tri':
                F = polymul(F, base)
            F = polyadd(F, [p ** m * x for x in H])
        elif fam == 'gate2':
            t = rng.randrange(3, 3 * p)
            F = [0]
            for c in range(t):
                dlt = 1 if c < 3 else (rng.choice([0, 0, 0, 1, -1]) if c >= p else 0)
                if dlt:
                    F = polyadd(F, [dlt * x for x in pi_poly(c)])
            b = -2 + p ** rng.randrange(1, r + 2) * rng.randrange(p ** 6)
        else:
            F = [rng.randrange(-p ** 8, p ** 8) for _ in range(rng.randrange(2, 8))]
        Fd = deriv(F)
        h = -(-D // 2)   # 2 v(F') >= D  <=>  v(F') >= ceil(D/2)
        nK, nD, nKh, nKh1 = counts(F, Fd, p, b, r, K, D, h)
        # p^K mu_B(Y_K) = p^K * nK / p^(K-r) = p^r nK ; p^D mu_B(Y_D) = p^r nD
        lhs = nK - nD          # common factor p^r dropped
        rhs = nKh
        rhs_ctrl = int(nKh1) if (2 * (h + 1) >= D + 2) else nKh
        s = stats[fam]
        s[0] += 1
        if lhs > rhs:
            s[1] += 1
            print("  H2 VIOLATION fam=%s p=%d r=%d D=%d K=%d b=%d lhs=%d rhs=%d F=%s" % (fam, p, r, D, K, b, lhs, rhs, F[:6]))
        if lhs > 0:
            s[2] += 1
            s[4] = max(s[4], lhs / rhs if rhs > 0 else float('inf'))
        # control with threshold D+2: v(F') >= ceil((D+2)/2) = h+1
        if lhs > nKh1:
            s[3] += 1
    tot = [0, 0, 0, 0]
    for fam in fams:
        s = stats[fam]
        print("p=%d family %-7s trials %4d  failures %d  (LHS>0 in %4d, max LHS/RHS %.4f)  control(2v(F')>=D+2) violated %d" % (
            p, fam, s[0], s[1], s[2], s[4], s[3]))
        for i in range(4):
            tot[i] += s[i]
    print("p=%d TOTAL: %d trials, %d failures, LHS>0 in %d, control violated %d  [%.0fs]" % (p, tot[0], tot[1], tot[2], tot[3], time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
