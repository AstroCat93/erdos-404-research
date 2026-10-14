"""Exact test of the shared core (R3M Cor A', Prop B, Prop C2 and the L^2
recursion / stopping of Theorem C3 = note Theorem 11.14) at an odd prime p,
from the definitions only.

Usage: python3 rl_c3core.py p x0 n0 L EPSBAR2_MODE

  p   odd prime
  x0  integer representative of the atom A = x0 + p^{m0} Z_p, m0 = V_{n0}(x0)
  n0  first window time (n0 >= 2p); windows have length L:
      n_t = n0 + t*L for t = 0..3
  EPSBAR2_MODE  'none' (no stopping) or 'median' (choose epsbar_2 = median of
      eps_2 over the G_1 atoms, so that tau = 2 on some atoms)

What is computed exactly (python ints / Fractions):
  * all 2^(n0-1) paths of length n0 at x0; the alive ones (any slope);
  * for every refinement point x' = x0 + p^{m0} w, w mod p^{m3-m0}:
    the full slope-0 populations Z^0_{n_t}(x') for t=1,2,3, counted as
    (alive parent at n0) x (continuation) with aliveness v(S) >= V_{n_t} and
    slope v(S') = 0 tested directly on the child.  By backward integrality
    (F2: p^{V_n} | pi_j for j >= n) every path alive at n_t restricts to a
    path alive at n0, so this is the complete population.
  * chi^2 of W_0, eps_1 and eps_2 both as p^K Coll_K - p^D Coll_D (Fractions)
    and as the Fourier band mass sum_{xi != 0} |mu_W'(xi)|^2 F_W(xi) (floats).
Checks: martingale (Cor A'), Prop B, Prop C2 at l=1 and on every G_1 atom at
l=2, single-parent equality in B and C2, slope inheritance, measurability of
Z_t and eps_l, and the stopped recursion a_{l+1} <= a_l + epsbar_l a_{l-1}.
"""
import sys
import cmath
from fractions import Fraction
import numpy as np
from rl_lib import vp, V, Mx, pis_and_derivs_mod, subset_sums, coll_times_pk


def joint_hist(vals, ders, modv, p):
    """Histogram over all subsets of (sum vals mod modv, sum ders mod p)."""
    s = np.zeros(1, dtype=np.int64)
    d = np.zeros(1, dtype=np.int64)
    for a, b in zip(vals, ders):
        s = np.concatenate([s, (s + a) % modv])
        d = np.concatenate([d, (d + b) % p])
    key = s * p + d
    return np.bincount(key, minlength=modv * p).reshape(modv, p)


def fourier_eps(x, n, N, Np, p):
    """eps(W,W') as the Fourier band mass (R3M Prop C2 definition), float."""
    D = V(x, N, p) - V(x, n, p)
    Dp = V(x, Np, p) - V(x, N, p)
    K = D + Dp
    modK = p ** K
    # law of W mod p^{D+D'}: elements pi_j(x)/pi_n(x), n <= j < N
    elW = []
    cur = 1
    for j in range(n, N):
        if j > n:
            cur = cur * (x + j)
        elW.append(cur % modK)
    # W' law mod p^{D'}: pi_j(x)/pi_N(x), N <= j < N'
    elWp = []
    cur = 1
    for j in range(N, Np):
        if j > N:
            cur = cur * (x + j)
        elWp.append(cur % (p ** Dp))
    sW = subset_sums(elW, modK)
    sWp = subset_sums(elWp, p ** Dp)
    muW = np.bincount(sW, minlength=modK) / len(sW)
    muWp = np.bincount(sWp, minlength=p ** Dp) / len(sWp)
    hatW = np.array([sum(muW[r] * cmath.exp(-2j * cmath.pi * r * z / modK)
                         for r in range(modK)) for z in range(modK)])
    hatWp = np.array([sum(muWp[r] * cmath.exp(-2j * cmath.pi * r * xi / p ** Dp)
                          for r in range(p ** Dp)) for xi in range(p ** Dp)])
    # u = pi_N(x)/(p^D pi_n(x)) mod p^{D'}
    num = 1
    for i in range(n + 1, N + 1):
        num *= (x + i)
    assert vp(num, p) == D
    u = (num // p ** D) % (p ** Dp)
    uinv = pow(u, -1, p ** Dp)
    eps = 0.0
    for xi in range(1, p ** Dp):
        F = sum(abs(hatW[z]) ** 2 for z in range(modK)
                if z % (p ** Dp) == (xi * uinv) % (p ** Dp))
        eps += abs(hatWp[xi]) ** 2 * F
    return eps


def composite_eps(x, n, N, Np, p):
    """eps = p^K Coll_K - p^D Coll_D of the composite window [n, N')."""
    D = V(x, N, p) - V(x, n, p)
    K = V(x, Np, p) - V(x, n, p)
    el = []
    cur = 1
    for j in range(n, Np):
        if j > n:
            cur = cur * (x + j)
        el.append(cur % (p ** K))
    return coll_times_pk(el, K, p) - coll_times_pk(el, D, p), D, K


def main():
    p = int(sys.argv[1]); x0 = int(sys.argv[2]); n0 = int(sys.argv[3])
    L = int(sys.argv[4]); mode = sys.argv[5]
    nt = [n0 + t * L for t in range(4)]
    m = [V(x0, n, p) for n in nt]
    Ms = [Mx(x0, n, p) for n in nt]
    D = [m[t + 1] - m[t] for t in range(3)]
    print(f"p={p} x0={x0} times={nt} m={m} M={Ms} D={D}")
    assert n0 >= 2 * p
    assert Ms[0] < m[0], "A must be a G_0 atom"
    assert Ms[3] < m[0], "valuations up to n3 must be constant on A"
    adm = D[0] <= m[0] - Ms[1] and Ms[1] < m[0]
    lin1 = D[0] + D[1] <= m[0] - Ms[2] and Ms[2] < m[0]
    lin2 = D[1] + D[2] <= m[1] - Ms[3] and Ms[3] < m[1]
    print(f"admissible(W0)={adm}  lin_1={lin1}  lin_2={lin2}")
    PREC = m[3]
    mod = p ** PREC
    # ---- parents at n0 (all 2^(n0-1) paths, evaluated at x0) ----
    pis0, _ = pis_and_derivs_mod(x0, n0, p ** m[0])
    S_all = (1 + subset_sums(pis0[1:], p ** m[0])) % (p ** m[0])
    alive = np.nonzero(S_all == 0)[0]
    bits = ((alive[:, None] >> np.arange(n0 - 1)[None, :]) & 1).astype(np.int64)
    print(f"paths of length {n0}: {len(S_all)}; alive at x0: {len(alive)}")
    nw = p ** (PREC - m[0])
    Zt = np.zeros((4, nw), dtype=object)
    slope0_parent = None
    Y = {1: [], 2: []}           # per slope-0 parent descendant counts
    bad_inherit = 0
    for w in range(nw):
        xp = x0 + p ** m[0] * w
        # valuations constant on A
        assert [V(xp, n, p) for n in nt] == m
        P, Dv = pis_and_derivs_mod(xp, nt[3], mod)
        P = np.array(P, dtype=np.int64); Dv = np.array(Dv, dtype=np.int64)
        S = (1 + bits @ P[1:n0]) % mod
        Sd = (bits @ Dv[1:n0]) % p
        assert np.all(S % (p ** m[0]) == 0)            # aliveness constant on A
        s0 = (Sd != 0)
        if slope0_parent is None:
            slope0_parent = s0.copy()
        assert np.array_equal(s0, slope0_parent)        # slope constant on A
        Zt[0, w] = int(s0.sum())
        for t in (1, 2, 3):
            modt = p ** m[t]
            H = joint_hist(list(P[n0:nt[t]] % modt), list(Dv[n0:nt[t]] % p),
                           modt, p)
            rows = H[(-S) % modt]                       # (A, p)
            tot = rows.sum(axis=1) - rows[np.arange(len(S)), (-Sd) % p]
            Zt[t, w] = int(tot.sum())
            # slope inheritance: descendants of slope>0 parents have slope>0
            bad_inherit += int(tot[~s0].sum())
            if t in (1, 2):
                Y[t].append(tot[s0].astype(object))
    print(f"slope-0 parents Z0={Zt[0,0]}; slope-0 descendants of slope>0 parents: {bad_inherit}")
    c = [Fraction(p ** m[t], 2 ** nt[t]) for t in range(4)]
    Mt = [[c[t] * Zt[t, w] for w in range(nw)] for t in range(4)]
    M0 = Mt[0][0]
    ok = True

    def atom(w, t):  # index of the G_t atom containing x0 + p^{m0} w
        return w % (p ** (m[t] - m[0]))

    # measurability: Z_t constant on G_t atoms
    for t in (1, 2):
        for w in range(nw):
            if Zt[t, w] != Zt[t, atom(w, t)]:
                print("MEASURABILITY FAIL", t, w); ok = False
    # (a) martingale
    for t in (1, 2, 3):
        groups = {}
        for w in range(nw):
            groups.setdefault(atom(w, t - 1), []).append(Mt[t][w])
        for a, vals in groups.items():
            mean = sum(vals, Fraction(0)) / len(vals)
            prev = Mt[t - 1][a]
            if mean != prev:
                print(f"MARTINGALE FAIL t={t} atom={a}: {mean} vs {prev}"); ok = False
    print("(a) martingale E[M_t | G_{t-1}] = M_{t-1}: checked on",
          sum(p ** (m[t - 1] - m[0]) for t in (1, 2, 3)), "atoms")
    # chi^2 of W0 and eps_1 at x0
    elW0 = []
    cur = 1
    for j in range(nt[0], nt[1]):
        if j > nt[0]:
            cur *= (x0 + j)
        elW0.append(cur % (p ** D[0]))
    one_plus_chi2 = coll_times_pk(elW0, D[0], p)
    eps1, d1, k1 = composite_eps(x0, nt[0], nt[1], nt[2], p)
    eps1F = fourier_eps(x0, nt[0], nt[1], nt[2], p)
    print(f"1+chi0^2 = {one_plus_chi2} = {float(one_plus_chi2):.6f}")
    print(f"eps_1 (Coll form) = {eps1} = {float(eps1):.9f}; Fourier band form = {eps1F:.9f}")
    if abs(float(eps1) - eps1F) > 1e-9:
        print("EPS IDENTIFICATION FAIL (l=1)"); ok = False
    EM = lambda t, ws: sum((Mt[t][w] ** 2 for w in ws), Fraction(0)) / len(ws)
    allw = range(nw)
    a = [M0 ** 2, EM(1, allw), EM(2, allw), EM(3, allw)]
    # (b) Prop B
    lhsB = a[1]; rhsB = one_plus_chi2 * M0 ** 2
    print(f"(b) Prop B: E[M1^2]={float(lhsB):.6e} <= (1+chi^2)M0^2={float(rhsB):.6e}: {lhsB <= rhsB}")
    ok &= lhsB <= rhsB
    # (c) Prop C2 at l = 1 on the atom A
    lhsC = a[2] - a[1]; rhsC = eps1 * M0 ** 2
    print(f"(c) C2 l=1: E[M2^2]-E[M1^2]={float(lhsC):.6e} <= eps1*M0^2={float(rhsC):.6e}: {lhsC <= rhsC}"
          f"  ratio={float(lhsC/rhsC) if rhsC else float('nan'):.4f}")
    ok &= lhsC <= rhsC
    # (d) Prop C2 at l = 2 on every G_1 atom; eps_2 measurable w.r.t. G_1
    eps2 = {}
    worst = 0.0
    for at in range(p ** (m[1] - m[0])):
        ws = [w for w in allw if atom(w, 1) == at]
        e2s = set()
        for w in ws[:: max(1, len(ws) // 3)]:
            xp = x0 + p ** m[0] * w
            e2s.add(composite_eps(xp, nt[1], nt[2], nt[3], p)[0])
        if len(e2s) != 1:
            print("EPS_2 NOT CONSTANT ON G_1 ATOM", at); ok = False
        e2 = e2s.pop(); eps2[at] = e2
        xr = x0 + p ** m[0] * at
        e2F = fourier_eps(xr, nt[1], nt[2], nt[3], p)
        if abs(float(e2) - e2F) > 1e-9:
            print("EPS IDENTIFICATION FAIL (l=2)", at); ok = False
        lhs = EM(3, ws) - EM(2, ws)
        rhs = e2 * Mt[1][at] ** 2
        good = lhs <= rhs
        ok &= good
        if rhs:
            worst = max(worst, float(lhs / rhs))
        print(f"(d) C2 l=2 atom {at}: eps2={float(e2):.6f} (Fourier {e2F:.6f}) "
              f"lhs={float(lhs):.4e} rhs={float(rhs):.4e} ok={good}")
    print(f"(d) worst ratio lhs/rhs over G_1 atoms: {worst:.4f}")
    # (f) single-parent equality cases of Prop B and Prop C2
    Y1 = np.array(Y[1]).T; Y2 = np.array(Y[2]).T   # (parents, w)
    eqB = eqC = 0
    for i in range(Y1.shape[0]):
        e1 = sum((Fraction(int(v)) * c[1]) ** 2 for v in Y1[i]) / nw
        e2 = sum((Fraction(int(v)) * c[2]) ** 2 for v in Y2[i]) / nw
        eqB += (e1 == one_plus_chi2 * c[0] ** 2)
        eqC += (e2 - e1 == eps1 * c[0] ** 2)
    print(f"(f) single parent: Prop B equality {eqB}/{Y1.shape[0]}, C2 equality {eqC}/{Y1.shape[0]}")
    ok &= (eqB == Y1.shape[0]) and (eqC == Y1.shape[0])
    ok &= bad_inherit == 0
    # (e) stopped recursion of Theorem C3 (tau over l = 1, 2)
    epsbar1 = eps1
    e2vals = sorted(eps2.values())
    epsbar2 = e2vals[len(e2vals) // 2] if mode == 'median' else e2vals[-1]
    stop2 = {at: eps2[at] > epsbar2 for at in eps2}   # B_2 fails -> tau = 2
    Mtil = [[Mt[t][w] for w in allw] for t in range(4)]
    for w in allw:
        if stop2[atom(w, 1)]:
            Mtil[3][w] = Mt[2][w]                      # stopped at l = 2
    at_ = [M0 ** 2] + [sum((v ** 2 for v in Mtil[t]), Fraction(0)) / nw for t in (1, 2, 3)]
    # martingale of the stopped process
    for w0 in range(p ** (m[2] - m[0])):
        ws = [w for w in allw if atom(w, 2) == w0]
        if sum((Mtil[3][w] for w in ws), Fraction(0)) / len(ws) != Mtil[2][w0]:
            print("STOPPED MARTINGALE FAIL"); ok = False
    r1 = at_[1] <= one_plus_chi2 * at_[0]
    r2 = at_[2] <= at_[1] + epsbar1 * at_[0]
    r3 = at_[3] <= at_[2] + epsbar2 * at_[1]
    mono = at_[0] <= at_[1] <= at_[2] <= at_[3]
    Pi = one_plus_chi2 * (1 + epsbar1) * (1 + epsbar2)
    supb = at_[3] <= Pi * M0 ** 2
    nstop = sum(stop2.values())
    print(f"(e) stopping: epsbar2={float(epsbar2):.6f}, tau=2 on {nstop}/{len(stop2)} G_1 atoms")
    print(f"(e) a = {[f'{float(v):.6e}' for v in at_]}")
    print(f"(e) a1<=(1+chi2)a0 {r1}; a2<=a1+epsbar1 a0 {r2}; a3<=a2+epsbar2 a1 {r3}; "
          f"monotone {mono}; a3<=Pi*M0^2 {supb}")
    ok &= r1 and r2 and r3 and mono and supb
    print("RESULT:", "ALL CHECKS PASS" if ok else "FAILURE")


if __name__ == "__main__":
    main()
