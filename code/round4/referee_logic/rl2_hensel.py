"""Test (2): the Hensel reduction on composite windows, M4A (Lemma H +
Theorem 1) against M4C (Lemma H2 + Proposition H'), exactly, from the
statements only.

Usage: python3 rl2_hensel.py p z0 L Lp r [NLAM]

  Composite window with elements pi_c(z), 0 <= c < H = L + Lp (z = x + n),
  D = V_L(z), K = V_H(z), M = max_{i<=H} v(z+i); ball B = z0 + p^r Z_p.
  Requires M < r (frozen gate pattern on B; asserted point by point).

For every z in B mod p^K (all p^(K-r) classes) an exact DP over the lazy
signed digits gives the joint law of (T(z) mod p^K, T'(z) mod p^th),
T = sum_c delta_c pi_c(z).  Counts are exact (CRT over two primes < 2^60).
Printed and compared:
  E_B[eps]           = E_B[p^K Coll_K - p^D Coll_D]
  M4A Thm 1 RHS      = E_B[p^K P(v(T)>=K, v(T')>=th) - p^D P(v(T)>=D, v(T')>=th)],
                       th = min(ceil(D/2), D - r + 1); claimed EQUAL to E_B[eps]
  M4C H' RHS         = E_B[p^K P(v(T)>=K, v(T')>=ceil(D/2))]; claimed >= E_B[eps]
                       when D >= 2r and ceil(D/2) <= K - M
  controls           M4A with th forced to ceil(D/2) when r > floor(D/2)+1;
                       M4C's inequality when D < 2r (not claimed).
With NLAM > 0 it also checks, at NLAM points, the first-index identity
behind Prop H' / Lemma F:
  p^K P(v(T)>=K, v(T')>=ceil(D/2)) = c_H + sum_j (c_j/2) Lambda^{(lambda_j)}_{H-j}(z+j),
  lambda_j = ceil(D/2) - V_j(z), Lambda^{(l)}_t(y) = p^{V_t(y)} P(v(R)>=V_t, v(R')>=l),
  R = 1 + sum_{1<=c<t} delta_c pi_c(y).
"""
import sys
from fractions import Fraction
import numpy as np
from rl2_lib import vals, Vn, Mn, pi_and_deriv

Q = [1152921504606846883, 1152921504606846869]   # primes < 2^60 (checked below)


def is_prime(n):
    if n < 2:
        return False
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % a == 0:
            return n == a
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def crt2(r1, r2):
    q1, q2 = Q
    t = ((r2 - r1) * pow(q1, -1, q2)) % q2
    return r1 + q1 * t


def joint(vals_, ders, mv, md, first_fixed):
    """Per-prime joint weight arrays of (sum delta*vals mod mv, sum delta*ders mod md)."""
    outs = []
    for q in Q:
        cur = np.zeros((mv, md), dtype=np.int64)
        cur[0, 0] = 1
        for c, (a, d) in enumerate(zip(vals_, ders)):
            a %= mv; d %= md
            if c == 0 and first_fixed:
                cur = np.roll(cur, (a, d), axis=(0, 1))
                continue
            cur = (2 * cur + np.roll(cur, (a, d), axis=(0, 1))
                   + np.roll(cur, (-a, -d), axis=(0, 1))) % q
        outs.append(cur)
    return outs


def count(outs, p, k, th):
    """Exact weight of {T == 0 mod p^k, T' == 0 mod p^th}."""
    res = []
    for cur in outs:
        sub = cur[:: p ** k, :] if k > 0 else cur
        if th > 0:
            sub = sub[:, :: p ** th]
        res.append(sum(int(v) for v in sub.ravel()))
    return crt2(res[0] % Q[0], res[1] % Q[1])


def main():
    assert all(is_prime(q) for q in Q) and all(4 * q < 2 ** 63 for q in Q)
    p, z0, L, Lp, r = (int(a) for a in sys.argv[1:6])
    nlam = int(sys.argv[6]) if len(sys.argv) > 6 else 0
    H = L + Lp
    assert 4 ** H < Q[0] * Q[1]
    D = Vn(z0, L, p); K = Vn(z0, H, p); M = Mn(z0, H, p)
    assert M < r, "ball must freeze the gate pattern"
    thA = min(-(-D // 2), D - r + 1)
    thC = -(-D // 2)
    m4c_hyp = D >= 2 * r and thC <= K - M
    th = max(thA, thC, 1)
    mv, md = p ** K, p ** th
    pts = p ** max(K - r, 0)
    print(f"p={p} z0={z0} L={L} L'={Lp} r={r}: D={D} K={K} M={M}; theta_M4A={thA}, ceil(D/2)={thC}; "
          f"M4C hypotheses (D>=2r, ceil(D/2)<=K-M): {m4c_hyp}; M4A theta=ceil(D/2): {thA == thC}; points {pts}")
    tot = 4 ** H
    acc = {k: 0 for k in ("CK", "CD", "AK", "AD", "CK2", "FK", "FD")}
    ref = vals(z0, H, p)
    for t in range(pts):
        z = z0 + p ** r * t
        assert vals(z, H, p) == ref
        P, Dv = pi_and_deriv(z, H, mv * md)
        outs = joint(P, Dv, mv, md, False)
        acc["CK"] += count(outs, p, K, 0)
        acc["CD"] += count(outs, p, D, 0)
        acc["AK"] += count(outs, p, K, max(thA, 0))
        acc["AD"] += count(outs, p, D, max(thA, 0))
        acc["CK2"] += count(outs, p, K, thC)
        acc["FK"] += count(outs, p, K, thC)       # forced-theta control
        acc["FD"] += count(outs, p, D, thC)
    n = pts
    E = Fraction(p ** K * acc["CK"] - p ** D * acc["CD"], tot * n)
    A = Fraction(p ** K * acc["AK"] - p ** D * acc["AD"], tot * n)
    C = Fraction(p ** K * acc["CK2"], tot * n)
    F = Fraction(p ** K * acc["FK"] - p ** D * acc["FD"], tot * n)
    ok = True
    print(f"  E_B[eps]                       = {float(E):.15g}")
    print(f"  M4A Thm 1 RHS (theta={thA})      = {float(A):.15g}   identity exact: {E == A}")
    ok &= E == A
    print(f"  M4C H' RHS (theta=ceil(D/2)={thC}) = {float(C):.15g}   E_B eps <= RHS: {E <= C}"
          f"{'' if m4c_hyp else '   [hypothesis D>=2r fails: control only]'}")
    if m4c_hyp:
        ok &= E <= C
    if thA != thC:
        print(f"  control: M4A identity with theta forced to ceil(D/2): {float(F):.15g}; exact: {E == F}")
    # first-index identity at a few points
    if nlam:
        assert thC <= K - M
        good = 0
        for t in range(min(nlam, pts)):
            z = z0 + p ** r * (t * max(1, pts // nlam))
            P, Dv = pi_and_deriv(z, H, mv * p ** max(thC, 1))
            lhs = Fraction(p ** K * count(joint(P, Dv, mv, p ** max(thC, 1), False), p, K, thC), tot)
            rhs = Fraction(p ** K, 2 ** H)
            for j in range(H):
                y = z + j; tt = H - j
                Vt = Vn(y, tt, p); Vj = Vn(z, j, p)
                lam = thC - Vj
                cj = Fraction(p ** Vj, 2 ** j)
                mdl = p ** max(lam, 1)
                Py, Dy = pi_and_deriv(y, tt, p ** Vt * mdl)
                cnt = count(joint(Py, Dy, p ** Vt, mdl, True), p, Vt, max(lam, 0))
                rhs += cj / 2 * Fraction(p ** Vt * cnt, 4 ** (tt - 1))
            good += lhs == rhs
        print(f"  first-index identity (Prop H' / Lemma F decomposition): exact at {good}/{min(nlam, pts)} points")
        ok &= good == min(nlam, pts)
    print("RESULT:", "PASS" if ok else "FAILURE")


if __name__ == "__main__":
    main()
