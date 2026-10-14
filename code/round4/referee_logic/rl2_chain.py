"""Test (1b): exact check of the chain of Theorem 11.14 (R3M Cor A', Prop B,
Prop C2, the stopped L^2 recursion and the Paley-Zygmund step) on one atom
A = x0 + p^{m0} Z_p, from the definitions only.

Usage: python3 rl2_chain.py p x0 n0 L T

  windows n_t = n0 + t L, t = 0..T (T = 2 or 3); the valuations v(x+i),
  i <= n_T, must be constant on A (asserted).

Method (independent of the earlier rl_c3core.py, which enumerated parents and
continuations): for every refinement point x' = x0 + p^{m0} w, w mod
p^{m_T - m0}, a DP over ALL 0/1 paths of length n_T (e_0 = 1) with state
(S_e(x') mod p^{m_T}, S_e'(x') mod p) gives, at each n_t, the full slope-0
alive population Z^0_{n_t}(x') = #{e of length n_t : S_e(x') == 0 mod
p^{V_{n_t}}, S_e'(x') != 0 mod p}.  Nothing about parents, children, Hensel
roots or windows is used to count.

Checks, all in exact rationals (M_t = c_{n_t} Z^0_{n_t}, c_n = 2^-n p^{V_n}):
  (a) E[M_t | G_{t-1}] = M_{t-1} on every G_{t-1} atom      (Cor A')
  (b) E_A[M_1^2] <= (1 + chi^2_0) M_0^2, chi^2_0 = p^D Coll_D - 1 of W_0
                                                             (Prop B)
  (c) E[M_{l+1}^2 - M_l^2 | G_{l-1}] <= eps_l M_{l-1}^2 on every G_{l-1}
      atom, eps_l = p^K Coll_K - p^D Coll_D of [n_{l-1}, n_{l+1})  (Prop C2)
  (d) linear-regime conditions of B_l, admissibility of A
  (e) the recursion a_{l+1} <= a_l + epsbar_l a_{l-1} (epsbar_l = max eps_l),
      a_T <= Pi_A M_0^2, and the finite-horizon Paley-Zygmund bound
      mu_A(M_T > 0) >= (E M_T)^2 / E M_T^2 >= 1/Pi_A.
"""
import sys
NPAR = 3
from fractions import Fraction
import numpy as np
from rl2_lib import vals, Vn, Mn, pi_and_deriv, pk_coll, eps_coll


def populations(xp, nt, mT, p, parent=None):
    """Z^0_{n_t}(xp) for all t, by a DP over all paths of length n_T.
    If `parent` (a 0/1 list of length n_0) is given, only its extensions are
    counted (single-parent mode; then only t >= 1 is meaningful)."""
    mod = p ** mT
    nT = nt[-1]
    P, Dv = pi_and_deriv(xp, nT, mod)
    cur = np.zeros((mod, p), dtype=np.int64)
    if parent is None:
        cur[1 % mod, 0] = 1                  # e_0 = 1: S = pi_0 = 1, S' = 0
        j0 = 1
    else:
        S0 = sum(P[j] for j in range(nt[0]) if parent[j]) % mod
        D0 = sum(Dv[j] for j in range(nt[0]) if parent[j]) % p
        cur[S0, D0] = 1
        j0 = nt[0]
    Vt = [Vn(xp, n, p) for n in nt]
    out = {0: 1}
    for j in range(j0, nT):
        a, d = P[j] % mod, Dv[j] % p
        cur = cur + np.roll(cur, (a, d), axis=(0, 1))
        for t, n in enumerate(nt):
            if j == n - 1:
                sub = cur[:: p ** Vt[t], :]
                out[t] = int(sub[:, 1:].sum())
    return [out[t] for t in range(len(nt))]


def main():
    p, x0, n0, L, T = (int(a) for a in sys.argv[1:6])
    nt = [n0 + t * L for t in range(T + 1)]
    m = [Vn(x0, n, p) for n in nt]
    Ms = [Mn(x0, n, p) for n in nt]
    D = [m[t + 1] - m[t] for t in range(T)]
    print(f"p={p} x0={x0} n_t={nt} m_t={m} M_t={Ms} D_t={D}")
    assert n0 >= 2 * p and Ms[0] < m[0]
    assert Ms[T] < m[0], "valuations up to n_T must be constant on A"
    ok = True
    adm = D[0] <= m[0] - Ms[1] and Ms[1] < m[0]
    lin = {l: (D[l - 1] + D[l] <= m[l - 1] - Ms[l + 1] and Ms[l + 1] < m[l - 1]) for l in range(1, T)}
    print(f"(d) admissible: {adm}; linear regime: {lin}")
    ok &= adm and all(lin.values())
    mT = m[T]
    nw = p ** (mT - m[0])
    Z = []
    for w in range(nw):
        xp = x0 + p ** m[0] * w
        assert vals(xp, nt[-1], p) == vals(x0, nt[-1], p)
        Z.append(populations(xp, nt, mT, p))
    Z = np.array(Z, dtype=object)              # (nw, T+1)
    c = [Fraction(p ** m[t], 2 ** nt[t]) for t in range(T + 1)]
    Mt = [[c[t] * int(Z[w, t]) for w in range(nw)] for t in range(T + 1)]
    print(f"Z^0_(n0) on A: {sorted(set(int(z) for z in Z[:, 0]))} (must be constant); "
          f"Z^0_(n_T) range {min(Z[:, T])}..{max(Z[:, T])}")
    ok &= len(set(int(z) for z in Z[:, 0])) == 1
    M0 = Mt[0][0]
    if M0 == 0:
        print("empty slope-0 population: atom not admissible for C3 (Z^0 = 0)")

    def atom(w, t):
        return w % (p ** (m[t] - m[0]))

    def avg(f, ws):
        ws = list(ws)
        return sum((f(w) for w in ws), Fraction(0)) / len(ws)

    # (a) martingale + measurability
    nat = 0
    for t in range(1, T + 1):
        for a in range(p ** (m[t - 1] - m[0])):
            ws = [w for w in range(nw) if atom(w, t - 1) == a]
            if any(Mt[t - 1][w] != Mt[t - 1][ws[0]] for w in ws):
                print("MEASURABILITY FAIL", t - 1, a); ok = False
            if avg(lambda w: Mt[t][w], ws) != Mt[t - 1][ws[0]]:
                print(f"MARTINGALE FAIL t={t} atom={a}"); ok = False
            nat += 1
    print(f"(a) E[M_t|G_(t-1)] = M_(t-1) checked on {nat} atoms")
    # (b) Prop B
    W0 = [1]
    for j in range(nt[0] + 1, nt[1]):
        W0.append(W0[-1] * (x0 + j))
    one_chi = pk_coll(W0, D[0], p)
    a1 = avg(lambda w: Mt[1][w] ** 2, range(nw))
    print(f"(b) 1+chi0^2 = {one_chi} = {float(one_chi):.6f}; E M1^2 = {float(a1):.6e} <= "
          f"{float(one_chi * M0 ** 2):.6e}: {a1 <= one_chi * M0 ** 2}")
    ok &= a1 <= one_chi * M0 ** 2
    # (c) Prop C2 on every G_{l-1} atom
    epsmax = {}
    for l in range(1, T):
        worst = Fraction(0)
        epsmax[l] = Fraction(0)
        for a in range(p ** (m[l - 1] - m[0])):
            ws = [w for w in range(nw) if atom(w, l - 1) == a]
            xr = x0 + p ** m[0] * ws[0]
            e, Dl, Kl = eps_coll(xr, nt[l - 1], nt[l], nt[l + 1], p)
            assert e >= 0
            epsmax[l] = max(epsmax[l], e)
            lhs = avg(lambda w: Mt[l + 1][w] ** 2 - Mt[l][w] ** 2, ws)
            rhs = e * Mt[l - 1][ws[0]] ** 2
            good = lhs <= rhs
            ok &= good
            if rhs > 0:
                worst = max(worst, lhs / rhs)
            if not good:
                print(f"C2 FAIL l={l} atom={a}: {float(lhs)} > {float(rhs)}")
        print(f"(c) C2 at l={l}: checked on {p ** (m[l-1]-m[0])} G_(l-1) atoms; "
              f"eps_l max = {float(epsmax[l]):.6g} (D={Dl}, K={Kl}); worst lhs/rhs = {float(worst):.4f}")
    # (e) recursion and Paley-Zygmund (finite horizon)
    a = [M0 ** 2] + [avg(lambda w, t=t: Mt[t][w] ** 2, range(nw)) for t in range(1, T + 1)]
    rec = a[1] <= one_chi * a[0]
    for l in range(1, T):
        rec &= a[l + 1] <= a[l] + epsmax[l] * a[l - 1]
    Pi = one_chi
    for l in range(1, T):
        Pi *= 1 + epsmax[l]
    mono = all(a[i] <= a[i + 1] for i in range(T))
    EM = avg(lambda w: Mt[T][w], range(nw))
    surv = Fraction(sum(1 for w in range(nw) if Mt[T][w] > 0), nw)
    pz = EM ** 2 / a[T] if a[T] else Fraction(0)
    print(f"(e) a_t = {[f'{float(v):.6e}' for v in a]}; recursion {rec}; monotone {mono}; "
          f"a_T <= Pi M0^2: {a[T] <= Pi * a[0]}")
    print(f"(e) mu_A(M_T>0) = {float(surv):.6f} >= (E M_T)^2/E M_T^2 = {float(pz):.6f} >= 1/Pi_A = {float(1/Pi):.6f}: "
          f"{surv >= pz >= 1 / Pi if M0 else 'n/a'}")
    ok &= rec and mono and a[T] <= Pi * a[0]
    if M0:
        ok &= surv >= pz >= 1 / Pi and EM == M0
    # (f) single-parent equality cases (Prop N / R3M: equality in Prop B and
    #     in Prop C2 when the population is one parent)
    if M0:
        bits = None
        P0, Dv0 = pi_and_deriv(x0, n0, p ** m[0])
        found = []
        for code in range(2 ** (n0 - 1)):
            e = [1] + [(code >> i) & 1 for i in range(n0 - 1)]
            S = sum(P0[j] for j in range(n0) if e[j]) % p ** m[0]
            if S == 0 and sum(Dv0[j] for j in range(n0) if e[j]) % p != 0:
                found.append(e)
                if len(found) == NPAR:
                    break
        eqB = eqC = 0
        for e in found:
            Zs = [populations(x0 + p ** m[0] * w, nt, mT, p, parent=e) for w in range(nw)]
            Ms_ = [[c[t] * Zs[w][t] for w in range(nw)] for t in range(T + 1)]
            m0p = c[0]
            mart = all(avg(lambda w: Ms_[t][w], [w for w in range(nw) if atom(w, t - 1) == a]) ==
                       (m0p if t == 1 else Ms_[t - 1][[w for w in range(nw) if atom(w, t - 1) == a][0]])
                       for t in range(1, T + 1) for a in range(p ** (m[t - 1] - m[0])))
            b_eq = avg(lambda w: Ms_[1][w] ** 2, range(nw)) == one_chi * m0p ** 2
            e1, _, _ = eps_coll(x0, nt[0], nt[1], nt[2], p)
            c_eq = (avg(lambda w: Ms_[2][w] ** 2 - Ms_[1][w] ** 2, range(nw)) == e1 * m0p ** 2)
            ok &= mart
            eqB += b_eq
            eqC += c_eq
        print(f"(f) single parent ({len(found)} parents): martingale ok; Prop B equality {eqB}/{len(found)}; "
              f"Prop C2 (l=1) equality {eqC}/{len(found)}")
        ok &= eqB == len(found) and eqC == len(found)
    print("RESULT:", "ALL CHECKS PASS" if ok else "FAILURE")


if __name__ == "__main__":
    main()
