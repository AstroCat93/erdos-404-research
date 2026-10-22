"""t5_global.py -- exact finite-horizon test of Theorem B1' (global form) and of Theorem B1 (per atom)
with adaptive, two-step-predictable window times.

All of Z_p is processed: the atoms of G_0 are enumerated exhaustively (classes mod p^{m_0}); classes
x = -i + O(p^s) with p^s > e (i-1)! are not refined further because the slope-0 population is empty
there (Observation G); this is CHECKED by a DP at a representative of each such class, and the total
measure (atoms + cut classes) is checked to be exactly 1.
For horizon L the program computes, in exact rational arithmetic,
   m* = E[M_0 1_adm],  Q = E[(1+chi_0^2) M_0^2 1_adm],  a_k = E[Mt_k^2],  E[Mt_k]   (k = 0..L),
   delta_L = mu(adm, tau <= L),  Y_L = Mt_L 1{tau > L},
where Mt_k = M_{min(k,tau)} 1_adm is the stopped process of B1', and checks
   (G1) E[Mt_k] = m* for all k (martingale);  (G2) a_0 <= a_1 <= Q;
   (G3) a_{k+1} <= a_k + epsbar_k a_{k-1}  (k = 1..L-1);   (G4) a_L <= Q prod_{k<L}(1+epsbar_k);
   (G5) E[Y_L] >= m* - sqrt(a_L delta_L), Paley-Zygmund mu(Y_L>0) E[Y_L^2] >= E[Y_L]^2, and the
        finite-horizon form of B1':  mu(Y_L>0) >= (m* - sqrt(Pi Q delta_L))^2/(Pi Q) when m* > sqrt(Pi Q delta_L);
   (A)  per admissible atom A (Theorem B1 at horizon L): mu_A(Y_L>0) >= (1-sqrt(Pi_A delta_A))^2/Pi_A
        whenever delta_A < 1/Pi_A, with Pi_A = (1+chi_0^2(A)) prod(1+epsbar);
   (C2) per node (atom of G_l inside {tau>l} with B_{l+1}): E[M_{l+2}^2 - M_{l+1}^2 | node] <= eps_{l+1} M_l^2.
Usage: python3 t5_global.py p n0 n1 rule H L epsbar"""
import sys, math
from fz_lib import *

p, n0, n1 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rule, H, L = sys.argv[4], int(sys.argv[5]), int(sys.argv[6])
EB = Fraction(sys.argv[7])
epsbar = [None] + [EB] * (L + 2)   # epsbar_l for l >= 1
assert n0 >= 2 * p


def cutoff(i):
    s = 1
    while p ** s <= math.e * math.factorial(i - 1):
        s += 1
    return s


CUT = {i: cutoff(i) for i in range(1, n0 + 1)}
KMAX = max(CUT.values()) + 2

# ---------------------------------------------------------------- enumerate atoms of G_0
atoms = []      # (r, m0)
cut_mass = Fraction(0)
obsG_checked = 0; obsG_fail = 0
stack = [(r, 1) for r in range(p)]
while stack:
    r, k = stack.pop()
    mod = p ** k
    zero_i = [i for i in range(1, n0 + 1) if (r + i) % mod == 0]
    if zero_i:
        i = zero_i[0]
        if k >= CUT[i]:
            # Observation G: slope-0 population empty on the whole class; check at representatives
            cut_mass += Fraction(1, mod)
            for rep in (r, r + mod * 3 + mod * mod):
                if prefix(vals(rep, p, n0))[0][n0] > 20:
                    continue
                Z0, _ = dp_profile(rep, p, n0)
                obsG_checked += 1
                if Z0[n0] != 0:
                    obsG_fail += 1
                    print("FAIL Observation G", p, rep, i)
            continue
        for w in range(p):
            stack.append((r + mod * w, k + 1))
        continue
    vl = vals(r, p, n0); V, M = prefix(vl)
    if V[n0] == k:
        atoms.append((r, k))
    elif V[n0] > k:
        for w in range(p):
            stack.append((r + mod * w, k + 1))
    else:
        raise AssertionError("atom missed")
tot_mass = sum(Fraction(1, p ** m) for _, m in atoms) + cut_mass
print(f"RESULT p={p} n0={n0} n1={n1} rule={rule} H={H} L={L} epsbar={EB}: {len(atoms)} atoms of G_0, cut mass {float(cut_mass):.3e}, total mass == 1: {tot_mass == 1}; Observation G checks {obsG_checked}, failures {obsG_fail}")

# ---------------------------------------------------------------- accumulators
S1 = [Fraction(0)] * (L + 1); S2 = [Fraction(0)] * (L + 1)
acc = dict(delta=Fraction(0), EY=Fraction(0), EY2=Fraction(0), PY=Fraction(0))
stats = dict(nodes=0, c2checks=0, c2fail=0, Bheld=0, Bfail_lin=0, Bfail_eps=0, dps=0)


def node(l, r, m, nl, Mval, mu, loc):
    """atom (r mod p^m) of G_l inside {tau > l}; nl = [n_0..n_{l+1}]; Mval = M_l; mu = Haar measure.
       loc: per-adm-atom accumulator. Returns E_node[M_{l+1}^2] * mu (for the C2 check of the parent)."""
    stats['nodes'] += 1
    S1[l] += mu * Mval; S2[l] += mu * Mval ** 2
    if l == L:
        acc['EY'] += mu * Mval; acc['EY2'] += mu * Mval ** 2
        loc['EY'] += mu * Mval
        if Mval > 0:
            acc['PY'] += mu; loc['PY'] += mu
        return None
    N = nl[l + 1]
    vl = vals(r, p, N); V, M = prefix(vl)
    assert V[nl[l]] == m and M[N] < m, "window hypotheses must hold on nodes"
    D = V[N] - m
    cN = c_n(N, V[N], p)
    kids = []
    for w in range(p ** D):
        r2 = r + p ** m * w
        Z0, _ = dp_profile(r2, p, N)
        stats['dps'] += 1
        kids.append((r2, cN * Z0[N]))
    # B_{l+1}: G_l-measurable; needs n_{l+2} = rule(x mod p^{m_l})
    n2 = rule_next(rule, r % p ** m, m, nl[:l + 2], p, H)
    vl2 = vals(r, p, n2); V2, M2 = prefix(vl2)
    lin = cond52(V2, M2, nl[l], N, n2)
    eps = eps_coll(r, p, nl[l], N, n2) if lin else None
    B = lin and eps <= epsbar[l + 1]
    if not lin:
        stats['Bfail_lin'] += 1
    elif not B:
        stats['Bfail_eps'] += 1
    else:
        stats['Bheld'] += 1
    mu2 = mu / p ** D
    if B:
        tot_next2 = Fraction(0); tot_this2 = Fraction(0); have = True
        for r2, M2v in kids:
            res = node(l + 1, r2, m + D, nl[:l + 2] + [n2], M2v, mu2, loc)
            tot_this2 += mu2 * M2v ** 2
            if res is None:
                have = False
            else:
                tot_next2 += res
        if have:
            stats['c2checks'] += 1
            lhs = (tot_next2 - tot_this2) / mu
            if lhs > eps * Mval ** 2:
                stats['c2fail'] += 1
                print("FAIL node C2", l, r, m, lhs, eps * Mval ** 2)
    else:
        for r2, M2v in kids:
            for k in range(l + 1, L + 1):
                S1[k] += mu2 * M2v; S2[k] += mu2 * M2v ** 2
            acc['delta'] += mu2; loc['delta'] += mu2
    return sum(mu2 * M2v ** 2 for _, M2v in kids)


mstar = Fraction(0); Q = Fraction(0); nadm = 0
per_atom = []
for r, m0 in sorted(atoms, key=lambda t: (t[1], t[0])):
    vl = vals(r, p, n1); V, M = prefix(vl)
    if not (M[n1] < m0 and (V[n1] - V[n0]) <= m0 - M[n1]):
        continue
    Z0, _ = dp_profile(r, p, n0)
    if Z0[n0] == 0:
        continue
    nadm += 1
    mu = Fraction(1, p ** m0)
    M0 = c_n(n0, V[n0], p) * Z0[n0]
    ch = chi2(r, p, n0, n1)
    mstar += mu * M0; Q += mu * (1 + ch) * M0 ** 2
    loc = dict(delta=Fraction(0), EY=Fraction(0), PY=Fraction(0))
    node(0, r, m0, [n0, n1], M0, mu, loc)
    per_atom.append((r, m0, mu, M0, ch, loc))

Pi = Fraction(1)
for k in range(1, L):
    Pi *= (1 + epsbar[k])
print(f"RESULT admissible atoms {nadm}; nodes {stats['nodes']}; DPs {stats['dps']}; B held {stats['Bheld']}, B failed (linear regime) {stats['Bfail_lin']}, (eps) {stats['Bfail_eps']}")
print(f"RESULT m* = {float(mstar):.6g}, Q = {float(Q):.6g}, a_k = {[float(x) for x in S2]}, delta_L = {float(acc['delta']):.6g}")
fails = 0
# (G1)
g1 = all(S1[k] == mstar for k in range(L + 1))
print(f"RESULT (G1) E[Mt_k] == m* exactly for k=0..{L}: {g1}  values {[float(x) for x in S1]}")
fails += not g1
# (G2)
g2 = S2[0] <= S2[1] <= Q if L >= 1 else True
print(f"RESULT (G2) a_0 <= a_1 <= Q: {g2}")
fails += not g2
# (G3)
g3 = all(S2[k + 1] <= S2[k] + epsbar[k] * S2[k - 1] for k in range(1, L))
print(f"RESULT (G3) a_(k+1) <= a_k + epsbar_k a_(k-1): {g3}  slacks {[float(S2[k] + epsbar[k] * S2[k - 1] - S2[k + 1]) for k in range(1, L)]}")
fails += not g3
# (G4)
g4 = S2[L] <= Q * Pi
print(f"RESULT (G4) a_L <= Pi Q: {g4}")
fails += not g4
# (G5)
EY, EY2, PY, dl = acc['EY'], acc['EY2'], acc['PY'], acc['delta']
gap = mstar - EY
g5a = gap <= 0 or gap ** 2 <= S2[L] * dl
g5b = PY * EY2 >= EY ** 2
print(f"RESULT (G5) E[Y_L] >= m* - sqrt(a_L delta_L): {g5a}; Paley-Zygmund mu(Y>0)E[Y^2] >= E[Y]^2: {g5b}; mu(Y_L>0) = {float(PY):.6g}")
fails += (not g5a) + (not g5b)
thr = math.sqrt(float(Pi * Q * dl))
if float(mstar) > thr:
    lb = (float(mstar) - thr) ** 2 / float(Pi * Q)
    ok = float(PY) >= lb * (1 - 1e-12)
    print(f"RESULT (G5) B1' finite-horizon bound non-vacuous: mu(Y_L>0) = {float(PY):.6g} >= {lb:.6g}: {ok}")
    fails += not ok
else:
    print(f"RESULT (G5) B1' finite-horizon bound vacuous here (m* = {float(mstar):.4g} <= sqrt(Pi Q delta) = {thr:.4g})")
# (A) per atom
na = 0; nonvac = 0; afail = 0; tight = None
for r, m0, mu, M0, ch, loc in per_atom:
    PiA = (1 + ch) * Pi
    dA = loc['delta'] / mu
    pA = loc['PY'] / mu
    na += 1
    if float(PiA * dA) < 1:
        nonvac += 1
        lb = (1 - math.sqrt(float(PiA * dA))) ** 2 / float(PiA)
        if float(pA) < lb * (1 - 1e-12):
            afail += 1
            print("FAIL per-atom bound", r, m0, float(pA), lb)
        ratio = float(pA) / lb if lb > 0 else None
        if ratio is not None and (tight is None or ratio < tight):
            tight = ratio
print(f"RESULT (A) per-atom Theorem B1 at horizon {L}: {na} admissible atoms, {nonvac} with delta_A < 1/Pi_A, failures {afail}; min ratio mu_A(Y>0)/bound = {tight}")
fails += afail
print(f"RESULT node-level C2 checks {stats['c2checks']}, failures {stats['c2fail']}")
fails += stats['c2fail'] + obsG_fail + (tot_mass != 1)
print(f"SUMMARY t5 p={p} rule={rule} L={L} epsbar={EB}: total failures {fails}")
