"""t6_atom_j.py -- Theorem B1 (per atom) at a starting time j >= 1, where the atom A of G_j and the
next time n_{j+1} are themselves RANDOM (n_{j+1} = rule(x mod p^{m_{j-1}})).  Random admissible atoms
of G_j are sampled; on each, the stopped process Mt_k = M_{min(k,tau_j)} (k = j..L) is computed EXACTLY
on all sub-atoms, and we check
   E_A[Mt_k] = M_j(A) for all k;  a_k := E_A[Mt_k^2]:  a_j <= a_{j+1} <= (1+chi_j^2) M_j^2,
   a_{k+1} <= a_k + epsbar a_{k-1};  and the horizon-L form of B1:
   mu_A(Y_L > 0) >= (1 - sqrt(Pi_A delta_A))^2 / Pi_A whenever delta_A < 1/Pi_A.
Usage: python3 t6_atom_j.py SEED p n0 n1 rule H j L epsbar NATOMS"""
import sys, random, math
from fz_lib import *

seed = int(sys.argv[1]); p, n0, n1 = map(int, sys.argv[2:5]); rule = sys.argv[5]
H, j, L = map(int, sys.argv[6:9]); EB = Fraction(sys.argv[9]); NAT = int(sys.argv[10])
rng = random.Random(seed)
R = 60
st = dict(atoms=0, mart_fail=0, a_fail=0, rec_fail=0, nonvac=0, bound_fail=0, minratio=None, tries=0)


def run(l, r, m, nl, Mval, mu, acc):
    """node = atom of G_l inside {tau_j > l}; relative measure mu inside A."""
    acc['S1'][l] += mu * Mval; acc['S2'][l] += mu * Mval ** 2
    if l == L:
        if Mval > 0:
            acc['PY'] += mu
        return
    N = nl[l + 1]
    vl = vals(r, p, N); V, M = prefix(vl)
    assert V[nl[l]] == m and M[N] < m
    D = V[N] - m; cN = c_n(N, V[N], p)
    kids = []
    for w in range(p ** D):
        r2 = r + p ** m * w
        Z0, _ = dp_profile(r2, p, N)
        kids.append((r2, cN * Z0[N]))
    n2 = rule_next(rule, r % p ** m, m, nl[:l + 2], p, H)
    vl2 = vals(r, p, n2); V2, M2 = prefix(vl2)
    B = cond52(V2, M2, nl[l], N, n2) and eps_coll(r, p, nl[l], N, n2) <= EB
    mu2 = mu / p ** D
    for r2, M2v in kids:
        if B:
            run(l + 1, r2, m + D, nl[:l + 2] + [n2], M2v, mu2, acc)
        else:
            for k in range(l + 1, L + 1):
                acc['S1'][k] += mu2 * M2v; acc['S2'][k] += mu2 * M2v ** 2
            acc['delta'] += mu2


while st['atoms'] < NAT and st['tries'] < 300 * NAT:
    st['tries'] += 1
    X = rng.randrange(p ** R)
    n, m = schedule(X, p, n0, n1, rule, H, j + 1)
    a, b = n[j], n[j + 1]
    vl = vals(X, p, b); V, M = prefix(vl)
    mj = m[j]
    if not (M[b] < mj and V[b] - V[a] <= mj - M[b]):
        continue
    r = X % p ** mj
    Z0, _ = dp_profile(r, p, a)
    if Z0[a] == 0:
        continue
    # the atom must be an atom of G_j: check n_0..n_{j+1} constant on it (two lifts)
    for _ in range(2):
        ny, my = schedule(r + p ** mj * rng.randrange(p ** 20), p, n0, n1, rule, H, j)
        assert ny[:j + 2] == n[:j + 2] and my[j] == mj
    Mj = c_n(a, V[a], p) * Z0[a]
    acc = dict(S1=[Fraction(0)] * (L + 1), S2=[Fraction(0)] * (L + 1), PY=Fraction(0), delta=Fraction(0))
    run(j, r, mj, n[:j + 2], Mj, Fraction(1), acc)
    st['atoms'] += 1
    S1, S2 = acc['S1'], acc['S2']
    if any(S1[k] != Mj for k in range(j, L + 1)):
        st['mart_fail'] += 1; print("FAIL per-atom martingale", X, n, [float(t) for t in S1[j:]])
    ch = chi2(r, p, a, b)
    if not (S2[j] <= S2[j + 1] <= (1 + ch) * Mj ** 2):
        st['a_fail'] += 1; print("FAIL a_j <= a_{j+1} <= (1+chi2) M^2", X, n)
    for k in range(j + 1, L):
        if S2[k + 1] > S2[k] + EB * S2[k - 1]:
            st['rec_fail'] += 1; print("FAIL recursion", X, n, k)
    PiA = (1 + ch) * (1 + EB) ** (L - 1 - j)
    dA = acc['delta']
    if float(PiA * dA) < 1:
        st['nonvac'] += 1
        lb = (1 - math.sqrt(float(PiA * dA))) ** 2 / float(PiA)
        if float(acc['PY']) < lb * (1 - 1e-12):
            st['bound_fail'] += 1; print("FAIL per-atom B1 bound", X, n, float(acc['PY']), lb)
        ratio = float(acc['PY']) / lb
        st['minratio'] = ratio if st['minratio'] is None else min(st['minratio'], ratio)
print(f"RESULT p={p} n0={n0} n1={n1} rule={rule} H={H} j={j} L={L} epsbar={EB}: {st}")
print(f"SUMMARY t6 failures {st['mart_fail'] + st['a_fail'] + st['rec_fail'] + st['bound_fail']}")
