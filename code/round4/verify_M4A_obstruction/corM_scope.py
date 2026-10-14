"""corM_scope.py -- scope and obstruction data for Corollary M' of track M4A (data/round4/reports/M4A.md s.6),
at any odd p, with exact integers.  Generalises atom_scope.py (written for Theorem M, p = 7).  No M4A code is
imported.

Usage: python3 corM_scope.py ATOMFILE L1 NBLOCK

For the atom A = xA + p^m Z_p of ATOMFILE and the window times n_0 = 300, n_{l+1} = ceil(27 n_l / 20):
  (S1) V_300(xA) = m, M_300 < m (A is an atom of G_0), the stored path is alive with slope 0 (exact),
       D_0, M_405, admissibility of W_0 (R3M Theorem C3 = note Theorem 11.14).
  (S2) i_A = first position with v(x+i) >= m on A (the first random gate); the phase structure used by M4A
       (phase 1: l <= L1; phase 2: n_{l+1} <= NBLOCK; phase 3: n_{l+1} < i_A; phase 4: the rest);
       max gate depth per phase (all < m, i.e. frozen on A); the linear regime of C3 for every l < l*;
       Theorem 1's slope threshold theta = min(ceil(D/2), D-m+1) = ceil(D/2) and Lemma F's K - M >= theta
       for every Markov window l in (L1, l*).
  (S3) Proposition O1 (Part I of data/round4/checks/M4A_obstruction.md) at this p: the first phase-4 window
       l* has i_A in its SECOND half and no other position of I_A = i_A + p^m N_0 in (n, N'], so the
       untruncated E_A[eps_{l*}] = +infinity: the truncation G' of M4A's phase 4 is necessary at this p.
  (S4) consistency of the phase-1 deterministic thresholds with Prop 11.12: every composite window, read as a
       single window [n, N') mod p^K, has chi^2 >= (p-1) 4^-p, hence Prop D's bound for p^K Coll_K must be
       >= 1 + (p-1) 4^-p.  Checked on M4A's printed chi^2_0 and eps_bar, read from the log
       data/round4/M4A/fe_verify_final.log.
"""
import os
import re
import sys

import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from vo_lib import vp  # noqa: E402

mp.mp.dps = 50
LOG = os.path.join(HERE, '..', '..', '..', 'data', 'round4', 'M4A', 'fe_verify_final.log')


def read_atom(fn):
    d = {}
    for line in open(fn):
        line = line.strip()
        if '=' in line:
            k, v = line.split('=', 1)
            d[k] = v
    return int(d['p']), int(d['n0']), int(d['m']), int(d['xA']), d['path']


def log_eps_bars(p):
    """M4A's printed chi^2_0 and phase-1 eps_bar at this p (from the final FE log)."""
    txt = open(LOG).read()
    blocks = txt.split('=== command:')
    for b in blocks:
        if f'# p={p} ' in b:
            chi = float(re.search(r'chi\^2_0 <= ([0-9.e+-]+)', b).group(1))
            eb = [float(x) for x in re.findall(r'phase1 eps_bar\(PropD\)=([0-9.e+-]+)', b)]
            return chi, eb
    return None, []


def main():
    p, n0, m, xA, path = read_atom(sys.argv[1])
    L1, NBLOCK = int(sys.argv[2]), int(sys.argv[3])
    print(f"p={p} n0={n0} m={m} xA={xA}  (L1={L1}, NBLOCK={NBLOCK})")
    assert n0 >= 2 * p, "C3 needs n_0 >= 2p"
    # ---------------- (S1) ----------------
    times = [n0]
    while len(times) < 3 or times[-1] < 10 * p ** m:
        times.append(-(-27 * times[-1] // 20))
    dep = [0] + [vp(xA + i, p) for i in range(1, times[1] + 1)]
    V300, M300 = sum(dep[1:n0 + 1]), max(dep[1:n0 + 1])
    V405, M405 = sum(dep[1:times[1] + 1]), max(dep[1:times[1] + 1])
    D0 = V405 - V300
    print(f"(S1) V_300={V300} (file m={m})  M_300={M300} < m: {M300 < m}  D_0={D0}  M_405={M405}")
    print(f"     W_0 admissible: D_0 <= m - M_405: {D0 <= m - M405};  M_405 < m: {M405 < m}")
    assert V300 == m and M300 < m and D0 <= m - M405 and M405 < m
    assert len(path) == n0 and path[0] == '1'
    MOD = p ** (m + 5)
    pi, dpi, S, dS = 1, 0, 0, 0
    for j in range(n0):
        if path[j] == '1':
            S, dS = (S + pi) % MOD, (dS + dpi) % MOD
        dpi = (dpi * (xA + j + 1) + pi) % MOD
        pi = pi * (xA + j + 1) % MOD
    print(f"     path: v(S_e(xA)) = {vp(S, p) if S else '>=m+5'} >= m: {S % p ** m == 0};  S_e'(xA) mod p = {dS % p} != 0: {dS % p != 0}")
    assert S % p ** m == 0 and dS % p != 0
    # ---------------- (S2) ----------------
    first = {s: ((-xA) % p ** s) or p ** s for s in range(1, m + 1)}
    iA = first[m]

    def Vd(N):   # V_N on A, N < iA
        assert N < iA
        return sum((N - first[s]) // p ** s + 1 for s in range(1, m) if first[s] <= N)

    def Md(N):
        assert N < iA
        return max([s for s in range(1, m) if first[s] <= N], default=0)

    for N in (n0, times[1], 2457, 20000):
        assert Vd(N) == sum(vp(xA + i, p) for i in range(1, N + 1)), N
        assert Md(N) == max(vp(xA + i, p) for i in range(1, N + 1)), N
    lstar = min(l for l in range(1, len(times) - 1) if times[l + 1] >= iA)
    print(f"(S2) i_A = {iA} (~{float(iA):.4e}; p^m = {float(p ** m):.4e});  first phase-4 window l* = {lstar}")
    ph = {}
    nlin_bad = nF_bad = nth_bad = 0
    first_markov = None
    for l in range(1, lstar):
        n, N, N2 = times[l - 1], times[l], times[l + 1]
        Vn = Vd(n)
        D, K, M2 = Vd(N) - Vn, Vd(N2) - Vn, Md(N2)
        phase = 1 if l <= L1 else (2 if N2 <= NBLOCK else 3)
        ph.setdefault(phase, []).append((l, M2))
        if not (K <= Vn - M2 and M2 < Vn):
            nlin_bad += 1
        if l > L1:
            th = min((D + 1) // 2, D - m + 1)
            if not (D // 2 + 1 >= m and th == (D + 1) // 2 and th >= 1):
                nth_bad += 1
            if not (K - M2 >= th):
                nF_bad += 1
            if first_markov is None:
                first_markov = (l, n, N, N2, D, K, M2, th)
    for k in sorted(ph):
        ls = [a for a, _ in ph[k]]
        print(f"     phase {k}: l = {ls[0]}..{ls[-1]} ({len(ls)} windows), max gate depth = {max(b for _, b in ph[k])} (< m = {m})")
    print(f"     linear regime of C3 fails in {nlin_bad} of the {lstar - 1} windows l < l* (exact, deterministic on A)")
    l, n, N, N2, D, K, M2, th = first_markov
    print(f"     first Markov window l={l} [{n},{N},{N2}): D={D} K={K} M={M2}: floor(D/2)+1={D // 2 + 1} >= m={m}: {D // 2 + 1 >= m}; "
          f"theta={th}; K-M={K - M2} >= theta: {K - M2 >= th}")
    print(f"     over all Markov windows l in ({L1}, {lstar}): theta != ceil(D/2) or floor(D/2)+1 < m in {nth_bad}; K - M < theta in {nF_bad}")
    # ---------------- (S3) ----------------
    n, N, N2 = times[lstar - 1], times[lstar], times[lstar + 1]
    H = N2 - n
    c = iA - 2 - n
    print(f"(S3) l*={lstar}: n={n} N={N} N'={N2}")
    ok = N < iA < N2 and iA + p ** m > N2 and c >= 0 and c + 2 <= H - 1
    print(f"     N < i_A < N': {N < iA < N2};  next point of I_A, i_A + p^m > N': {iA + p ** m > N2};  c = i_A-2-n >= 0 and c+2 <= H-1: {c >= 0 and c + 2 <= H - 1}")
    a_c = Vd(n + c) - Vd(n)
    Dl = Vd(N) - Vd(n)
    K0 = sum((N2 - first[s]) // p ** s + 1 for s in range(1, m) if first[s] <= N2) - (m - 1) - Vd(n)
    s0 = max(m, K0 - a_c)
    term = mp.mpf(p - 1) / p * mp.power(p, m + K0) * mp.power(2, -(H + 2))
    print(f"     H={H} a_c={a_c} D={Dl} K_0=K-v(x+i_A)={K0} s_0=max(m,K_0-a_c)={s0}")
    print(f"     => E_A[eps_l*] >= sum_(s>=s_0) [((p-1)/p) p^(m+K_0) 2^-(H+2) - ((p-1)/p) p^(D+m-s)] = +infinity "
          f"(each term ~ 10^{float(mp.log10(term)):.4e}).  Proposition O1 holds at p={p}: {ok}")
    # ---------------- (S4) ----------------
    floor = mp.mpf(p - 1) / mp.power(4, p)
    chi, eb = log_eps_bars(p)
    print(f"(S4) Prop 11.12 floor (p-1)4^-p = {mp.nstr(floor, 5)};  M4A's chi^2_0 bound = {chi} >= floor: {chi >= floor}")
    print(f"     M4A's phase-1 eps_bar (Prop D - 1) = {eb};  all >= floor: {all(e >= floor for e in eb)}")
    print(f"     (each composite window [n,N') mod p^K is a single window with jump K, so p^K Coll_K - 1 >= floor;"
          f" a Prop D value below 1 + floor would contradict Prop 11.12)")


if __name__ == '__main__':
    main()
