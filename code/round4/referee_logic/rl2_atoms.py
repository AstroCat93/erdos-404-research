"""Test (1a): the hypotheses of Theorem 11.14 (R3M Theorem C3) on the atoms the
two tracks use, recomputed exactly from the definitions.

Usage:
  python3 rl2_atoms.py m4a ATOMFILE [LMAX]     (M4A atoms, n0=300, r=27/20)
  python3 rl2_atoms.py m4c P1 P2 ...           (M4C atom A = p^3 Z_p, n0 = 3p)

m4a: reads x_A and the path from the atom file (nothing else), and checks
  * V_300(x_A) = m, M_300 < m (A is a G_0 atom), D_0, M_405, admissibility;
  * the path: v(S_e(x_A)) >= m and S_e'(x_A) a unit (slope 0) -- exact ints;
  * the schedule n_{l+1} = ceil(27 n_l/20), i_A = (-x_A) mod p^m, the phase
    boundaries (n_{l+1} <= 60000; n_{l+1} < i_A);
  * for EVERY window l with n_{l+1} < i_A: the linear-regime condition
    D_{l-1}+D_l <= m_{l-1} - M_{n_{l+1}}, M_{n_{l+1}} < m_{l-1}, computed by
    an exact digit count of v(x_A+i) (valid for i < i_A, where v(x+i) is
    constant on A); for l >= 9 also floor(D/2)+1 >= m (so Theorem 1 on B = A
    has theta = ceil(D/2)) and Lemma F's M_W <= K - theta.
  * direct valuation sums for the first windows, against the digit count.
m4c: for each p, at random x in p^3 Z_p (exact ints):
  * V_{3p} = 3, M_{3p} = 1, D_0 = v(x+4p) = 1, M_{4p} = 1 (admissibility);
  * 1 + chi^2_{W_0} = p Coll_1(W_0) equals q_1(p) (q_1 by an exact DP);
  * Proposition W: builds the path (first block {0,p-1}, or M4C's explicit
    block at the Wilson prime 13; second/third block by subset-sum search)
    and checks alive at 3p and slope 0 by exact evaluation; also that the
    block {0,p-1} has positive slope exactly when p is a Wilson prime.
"""
import sys
import random
from fractions import Fraction
from rl2_lib import v_p, Vn, Mn, pi_and_deriv, signed_law_1d, pk_coll


def read_atom(fn):
    d = {}
    for line in open(fn):
        line = line.strip()
        if "=" in line:
            k, v = line.split("=", 1)
            d[k.strip()] = v.strip()
    return int(d["p"]), int(d["n0"]), int(d["m"]), int(d["xA"]), d["path"]


def digit_counts(xA, p, m):
    """i_s = least i >= 1 with x_A + i == 0 mod p^s, for s = 1..m."""
    return {s: ((-xA) % p ** s) or p ** s for s in range(1, m + 1)}


def V_M_digits(N, ist, p, m):
    """V_N and M_N on A for N < i_A (= ist[m]): only levels s < m occur."""
    V = 0
    M = 0
    for s in range(1, m):
        i0 = ist[s]
        if i0 <= N:
            V += (N - i0) // p ** s + 1
            M = s
    return V, M


def m4a(fn, lmax):
    p, n0, m, xA, path = read_atom(fn)
    print(f"M4A atom {fn}: p={p} n0={n0} m={m}")
    ok = True
    V300 = Vn(xA, n0, p); M300 = Mn(xA, n0, p)
    n = [n0]
    while len(n) < 2000:
        n.append((27 * n[-1] + 19) // 20)
    V405 = Vn(xA, n[1], p); M405 = Mn(xA, n[1], p)
    D0 = V405 - V300
    adm = D0 <= m - M405 and M405 < m
    print(f"  V_{n0}={V300} (claimed {m})  M_{n0}={M300}  D_0={D0}  M_{n[1]}={M405}  admissible={adm}")
    ok &= (V300 == m) and (M300 < m) and adm
    # path: exact evaluation modulo p^(m+10)
    e = [int(ch) for ch in path]
    assert len(e) == n0 and e[0] == 1
    mod = p ** (m + 10)
    P, Dv = pi_and_deriv(xA, n0, mod)
    S = sum(P[j] for j in range(n0) if e[j]) % mod
    Sd = sum(Dv[j] for j in range(n0) if e[j]) % mod
    vS = v_p(S, p) if S else m + 10
    print(f"  path: v(S_e(x_A)) >= {vS} (need >= {m}); S_e'(x_A) mod p = {Sd % p} (slope 0 iff nonzero)")
    ok &= vS >= m and Sd % p != 0
    # schedule and digits
    ist = digit_counts(xA, p, m)
    iA = ist[m]
    lastA = max(l for l in range(len(n) - 1) if n[l + 1] < iA)   # last l with n_{l+1} < i_A
    ph2 = [l for l in range(9, lastA + 1) if n[l + 1] <= 60000]
    print(f"  i_A = {iA} ({float(iA):.4g});  windows with n_(l+1) < i_A: l <= {lastA};"
          f"  n_{lastA} = {float(n[lastA]):.4g}, n_{lastA+1} = {float(n[lastA+1]):.4g}, n_{lastA+2} = {float(n[lastA+2]):.4g}")
    print(f"  phase 2 (l>=9, n_(l+1)<=60000): l = {ph2[0]}..{ph2[-1]} ({len(ph2)} windows);"
          f" phase 3: l = {ph2[-1]+1}..{lastA} ({lastA - ph2[-1]} windows); phases 2-3 together: {lastA - 8}")
    # direct vs digit formula for the first windows
    for l in range(0, 6):
        Vd, Md = V_M_digits(n[l], ist, p, m)
        if (Vd, Md) != (Vn(xA, n[l], p), Mn(xA, n[l], p)):
            print("  DIGIT FORMULA MISMATCH at", l); ok = False
    mV = {}
    def VM(l):
        if l not in mV:
            mV[l] = V_M_digits(n[l], ist, p, m)
        return mV[l]
    lin_fail = th_fail = F_fail = 0
    rows = []
    for l in range(1, min(lastA, lmax) + 1):
        m_prev, _ = VM(l - 1); m_l, _ = VM(l); m_next, M_next = VM(l + 1)
        D = m_l - m_prev; Dp = m_next - m_l; K = D + Dp
        lin = (K <= m_prev - M_next) and (M_next < m_prev)
        lin_fail += not lin
        if l >= 9:
            theta = -(-D // 2)
            th_fail += not (D // 2 + 1 >= m)
            F_fail += not (M_next <= K - theta)
        if l <= 9:
            rows.append((l, D, K, lin))
    print("  (l, D, K, lin) for l <= 9:", rows)
    print(f"  over l = 1..{min(lastA, lmax)}: linear regime fails in {lin_fail};"
          f" floor(D/2)+1 < m in {th_fail} (l>=9); Lemma F's M_W <= K-theta fails in {F_fail} (l>=9)")
    ok &= lin_fail == 0 and th_fail == 0 and F_fail == 0
    print("RESULT:", "PASS" if ok else "FAILURE")


# ------------------------------------------------------------------ M4C
def q1_exact(p):
    """q_1 = p max_a P(sum_r delta_r r! == a mod p), exact (DP over residues)."""
    fact = [1]
    for r in range(1, p):
        fact.append(fact[-1] * r)
    law = signed_law_1d([f % p for f in fact], p)
    return Fraction(p * int(max(law)), 4 ** p), Fraction(p * int(law[0]), 4 ** p)


def subset_with_sum(elems, target, mod):
    """Indices of a subset of `elems` with sum == target mod `mod` (DP)."""
    reach = {0: []}
    for i, a in enumerate(elems):
        new = dict(reach)
        for s, idx in reach.items():
            t = (s + a) % mod
            if t not in new:
                new[t] = idx + [i]
        reach = new
    return reach.get(target % mod)


def prop_w(p, x):
    """Build M4C's Proposition W path at x in p^3 Z_p; return (alive, slope)."""
    n = 3 * p
    mod = p ** 6
    P, Dv = pi_and_deriv(x, n, mod)
    xi = x // p
    fact = 1
    for r in range(1, p):
        fact *= r
    wp = (fact + 1) // p
    if p == 13:
        first = [0, 1, 2, 3, 4, 8, 9]
    else:
        first = [0, p - 1]
    e = [0] * n
    for j in first:
        e[j] = 1
    S1 = sum(P[j] for j in range(n) if e[j]) % mod
    assert S1 % p == 0, "first block must vanish mod p"
    # second block: elements pi_{p+u}(x), valuation 1; choose to kill digit 1
    el2 = [(P[p + u] // p) % p for u in range(p)]
    tgt = (-(S1 // p)) % p
    idx = subset_with_sum(el2, tgt, p)
    if idx is None:
        return None
    for u in idx:
        e[p + u] = 1
    S2 = sum(P[j] for j in range(n) if e[j]) % mod
    assert S2 % (p * p) == 0
    el3 = [(P[2 * p + u] // (p * p)) % p for u in range(p)]
    tgt = (-(S2 // (p * p))) % p
    idx = subset_with_sum(el3, tgt, p)
    if idx is None:
        return None
    for u in idx:
        e[2 * p + u] = 1
    S = sum(P[j] for j in range(n) if e[j]) % mod
    Sd = sum(Dv[j] for j in range(n) if e[j]) % mod
    V3 = Vn(x, n, p)
    alive = (S % p ** V3 == 0)
    return alive, (Sd % p != 0), V3, wp % p


def m4c(primes):
    rng = random.Random(404)
    ok = True
    for p in primes:
        q1, q1at0 = q1_exact(p)
        nx = 6
        res = []
        for _ in range(nx):
            x = p ** 3 * rng.randrange(1, p ** 8)
            V3 = Vn(x, 3 * p, p); M3 = Mn(x, 3 * p, p)
            D0 = Vn(x, 4 * p, p) - V3; M4 = Mn(x, 4 * p, p)
            adm = (V3 == 3 and M3 == 1 and D0 == 1 and M4 == 1 and D0 <= V3 - M4 and M4 < V3)
            # 1 + chi^2 of W_0 = [3p, 4p) mod p^{D_0}
            P, _ = pi_and_deriv(x + 3 * p, p, p)
            one_chi = pk_coll(P, 1, p)
            w = prop_w(p, x)
            res.append((adm, one_chi == q1, w))
            ok &= adm and one_chi == q1 and w is not None and w[0] and w[1]
        wilson = (res[0][2][3] == 0)
        # the plain block {0,p-1}: slope positive iff Wilson
        x = p ** 3 * rng.randrange(1, p ** 8)
        mod = p ** 4
        P, Dv = pi_and_deriv(x, p, mod)
        s01 = (P[0] + P[p - 1]) % mod
        d01 = (Dv[0] + Dv[p - 1]) % p
        print(f"p={p}: q_1={float(q1):.15g} (max at 0: {q1 == q1at0}); "
              f"atoms admissible {sum(r[0] for r in res)}/{nx}; 1+chi^2(W_0)=q_1 {sum(r[1] for r in res)}/{nx}; "
              f"Prop W path alive & slope 0 {sum(1 for r in res if r[2] and r[2][0] and r[2][1])}/{nx}; "
              f"Wilson={wilson}; block {{0,p-1}}: S==0 mod p {s01 % p == 0}, its own derivative mod p = {d01}")
        ok &= (q1 == q1at0)
    print("RESULT:", "PASS" if ok else "FAILURE")


if __name__ == "__main__":
    if sys.argv[1] == "m4a":
        m4a(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 6)
    else:
        m4c([int(a) for a in sys.argv[2:]])
