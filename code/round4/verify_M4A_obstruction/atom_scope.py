"""atom_scope.py -- scope checks of Theorem M (data/round4/reports/M4A.md section 6) with exact integers.

Usage: python3 atom_scope.py ATOMFILE

Independent re-derivation (no M4A code is imported) of:
  (S1) the atom: V_300(x_A) = 51, the stored path is alive with slope 0, M_405 = 4, D_0 = 17;
  (S2) the phase structure: maximal gate depth in every composite window of phases 1-3, the position
       i_A of the first random (depth >= 51) gate, and that every phase-1..3 window ends below i_A;
  (S3) the window l* whose SECOND half contains i_A, and the data of the divergence lemma
       E_A[eps_{l*}] = +infinity (so some deep-gate truncation is mathematically necessary there; M4A uses G');
  (S4) the final arithmetic of the conclusion (lower bound for mu(K_7 cap A)/mu(A) and for mu(K_7)).
"""
import sys
from fractions import Fraction
import mpmath as mp

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from vo_lib import vp

mp.mp.dps = 60


def read_atom(fn):
    d = {}
    for line in open(fn):
        line = line.strip()
        if '=' in line:
            k, v = line.split('=', 1)
            d[k] = v
    return int(d['p']), int(d['n0']), int(d['m']), int(d['xA']), d['path']


def main():
    p, n0, m, xA, path = read_atom(sys.argv[1])
    print(f"p={p} n0={n0} m={m} xA={xA}")
    # ---- (S1) atom ----
    V300 = sum(vp(xA + i, p) for i in range(1, n0 + 1))
    M300 = max(vp(xA + i, p) for i in range(1, n0 + 1))
    n_ = [n0]
    for _ in range(330):
        n_.append(-(-27 * n_[-1] // 20))  # ceil(27 n / 20), exact
    V405 = sum(vp(xA + i, p) for i in range(1, n_[1] + 1))
    M405 = max(vp(xA + i, p) for i in range(1, n_[1] + 1))
    print(f"(S1) V_300(xA)={V300} (claim {m}) M_300={M300} n_1={n_[1]} V_405={V405} D_0={V405 - V300} M_405={M405}")
    assert V300 == m
    # admissibility of W_0 (R3M: D_j <= m_j - M_{n_{j+1}} and M_{n_{j+1}} < m_j)
    print(f"     admissible window W_0: D_0 <= m - M_405: {V405 - V300 <= m - M405};  M_405 < m: {M405 < m}")
    # path: e_0..e_{n0-1} bits, S_e = sum e_j pi_j(xA); slope = v(S_e'(xA))
    assert len(path) == n0 and path[0] == '1'
    MOD = p ** 90
    pi, dpi = 1, 0
    S, dS = 0, 0
    for j in range(n0):
        if path[j] == '1':
            S = (S + pi) % MOD
            dS = (dS + dpi) % MOD
        # advance to pi_{j+1} = pi_j (x + j + 1)
        dpi = (dpi * (xA + j + 1) + pi) % MOD
        pi = pi * (xA + j + 1) % MOD
    vS = vp(S, p) if S != 0 else '>=90'
    print(f"     path: v_7(S_e(xA)) = {vS} (alive needs >= {m}); S_e'(xA) mod 7 = {dS % p} (slope 0 iff nonzero)")
    assert (S % p ** m == 0) and dS % p != 0
    print("     => on all of A = xA + 7^51 Z_7: S_e(x) == S_e(xA) mod 7^51 and V_300 constant, so e in P^0_300; Z^0_300 >= 1.")

    # ---- (S2) digits and phase structure ----
    first = {}
    for s in range(1, m + 1):
        i_s = (-xA) % p ** s
        first[s] = i_s if i_s >= 1 else p ** s  # first position i >= 1 with p^s | xA + i
    iA = first[m]
    print(f"(S2) i_A = first position with v(x+i) >= 51 on A = {iA}  (~{float(iA):.4e});  7^51 = {float(p ** m):.4e}")

    def V_digit(N):  # V_N on A for N < i_A (positions with v >= s for s <= m-1; none has v >= m)
        return sum((N - first[s]) // p ** s + 1 for s in range(1, m) if first[s] <= N)

    def M_digit(N):
        ss = [s for s in range(1, m) if first[s] <= N]
        return max(ss) if ss else 0

    # sanity: digit formula against direct valuations for a few N
    for N in (300, 405, 547, 4478, 20000):
        Vd = sum(vp(xA + i, p) for i in range(1, N + 1))
        assert Vd == V_digit(N), (N, Vd, V_digit(N))
    print("     digit formula for V_N agrees with direct valuations at N = 300, 405, 547, 4478, 20000")
    maxdep_phase1 = M_digit(n_[9])
    print(f"     phase 1 (l=1..8, windows end at n_9={n_[9]}): max gate depth = {maxdep_phase1}  (M4A s.7 says <= 5)")
    print(f"     phase 2 (l=9..16, end at n_17={n_[17]}): max gate depth = {M_digit(n_[17])}")
    last3 = max(l for l in range(1, 330) if n_[l + 1] < iA)
    print(f"     last l with n_(l+1) < i_A: {last3} (M4A: phase 3 ends at l=306); max depth there = {M_digit(n_[last3 + 1])} (< 51)")
    # linear regime re-check for all l <= last3 (exact): D+D' <= V_{n_{l-1}} - M_{n_{l+1}} and M < V_{n_{l-1}}
    bad = 0
    for l in range(1, last3 + 1):
        Vn, VN, VN2 = V_digit(n_[l - 1]), V_digit(n_[l]), V_digit(n_[l + 1])
        M2 = M_digit(n_[l + 1])
        if not ((VN2 - Vn) <= Vn - M2 and M2 < Vn):
            bad += 1
    print(f"     linear regime (R3M (5.2)) fails in {bad} of the windows l=1..{last3} (deterministic on A)")

    # ---- (S3) the window whose second half contains i_A ----
    ls = [l for l in range(1, 330) if n_[l] < iA < n_[l + 1]]
    assert len(ls) == 1
    l = ls[0]
    n, N, N2 = n_[l - 1], n_[l], n_[l + 1]
    print(f"(S3) i_A lies in the second half (N, N') of composite window l*={l}: n={n} N={N} N'={N2}")
    print(f"     next element of I_A: i_A + 7^51 = {float(iA + p ** m):.4e} > N' = {float(N2):.4e}: {iA + p ** m > N2}")
    H = N2 - n
    c = iA - 2 - n
    assert 0 <= c and c + 2 < H
    # valuations on A at positions in (n, N'] other than i_A are those of xA (depth <= 50)
    D = V_digit(N) - V_digit(n)
    a_c = V_digit(n + c) - V_digit(n)
    K0 = (sum((N2 - first[s]) // p ** s + 1 for s in range(1, m) if first[s] <= N2) - (m - 1)) - V_digit(n)
    # (the digit count up to N' includes i_A once for each s <= m-1; subtracting m-1 removes it)
    print(f"     H={H} c=i_A-2-n={c} a_c={a_c} D={D} K_0 = K - v(x+i_A) = {K0}")
    s0 = max(m, K0 - a_c)
    term = mp.mpf(6) / 7 * mp.power(7, m + K0) * mp.power(2, -(H + 2))
    print(f"     for s = v(x+i_A) >= s_0 = {s0}: the signed path (0^c, sigma, sigma, sigma, 0...) has S = sigma*y_c*(x+i_A)^2,")
    print(f"     v(S) = a_c + 2s >= K_0 + s = K, probability 2^-(H+2); hence eps(x) >= 7^(K_0+s) 2^-(H+2) - 7^D and")
    print(f"     E_A[eps_l*] >= sum_(s>=s_0) [ (6/7) 7^(51+K_0) 2^-(H+2) - (6/7) 7^(D+51-s) ] = +infinity,")
    print(f"     each term ~ 10^{float(mp.log10(term)):.4e} (positive, constant in s).")
    print("     So Markov on the untruncated E_A[eps_l*] is impossible (Prop 11.15(b) mechanism); M4A's phase 4 uses")
    print("     the truncation G' (and the linear regime, which itself caps v(x+i_A)).")

    # ---- (S4) arithmetic of the conclusion ----
    logPi = mp.mpf('25.7344')
    delta = mp.mpf('1.0006e-45')
    Pd = mp.power(10, logPi) * delta
    lb = (1 - mp.sqrt(Pd)) ** 2 / mp.power(10, logPi)
    print(f"(S4) Pi*delta <= 10^{float(mp.log10(Pd)):.5f};  (1-sqrt(Pi delta))^2/Pi >= {mp.nstr(lb, 8)} (claim 1.843e-26: {lb >= mp.mpf('1.843e-26')})")
    mu = mp.mpf('1.843e-26') * mp.power(7, -m)
    print(f"     mu(K_7) >= 1.843e-26 * 7^-51 = {mp.nstr(mu, 6)}  (M4A headline: >= 1.4e-69; s.6: ~1.5e-69)")
    # product check for log10 Pi_A from the listed thresholds
    thr = [mp.mpf('0.504642')] + [mp.mpf(t) for t in ('1.637', '12.93', '98.64', '137.8', '336.3', '3835', '4.643e5', '4.956e7')]
    lp = sum(mp.log10(1 + t) for t in thr) + mp.log10(mp.mpf('2.3843'))
    tail = mp.nprod(lambda i: 1 + mp.power(2, -i), [1, mp.inf])
    print(f"     log10[(1+chi0^2) prod_(l<=8)(1+eps_bar_l) * 2.3843] = {float(lp):.5f} (log rounds the eps_bar to 4 digits);"
          f" prod(1+2^-i) = {mp.nstr(tail, 8)}")


if __name__ == '__main__':
    main()
