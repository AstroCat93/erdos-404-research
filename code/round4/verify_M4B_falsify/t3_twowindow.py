"""t3_twowindow.py -- the L^2 step of Theorem B1 with ADAPTIVE (two-step-predictable) times.
On an atom C of G_{l-1} (class x mod p^{m_{l-1}}) where (5.2) holds for (W_{l-1}, W_l), with
n_{l+1} produced by the rule from x mod p^{m_{l-1}}, check EXACTLY (rational arithmetic):
  (C2)  E_C[(c_{n_{l+1}} Z0)^2] - E_C[(c_{n_l} Z0)^2] <= eps_l (c_{n_{l-1}} Z0)^2,
        with EQUALITY when Z0_{n_{l-1}} = 1 (single parent: no Cauchy-Schwarz/Minkowski loss);
  (B)   E_C[(c_{n_l} Z0)^2] <= (1 + chi^2_{W_{l-1}}) (c_{n_{l-1}} Z0)^2, equality when Z0 = 1;
  (mart) E_C[c_{n_{l+1}} Z0] = E_C[c_{n_l} Z0] = c_{n_{l-1}} Z0;
  (const) the rule gives the same n_{l+1} at every lift in C;
  (eps)  eps by collisions (exact) = eps by the R3M Fourier-fibre definition (float).
NEGATIVE CONTROL (outside the hypothesis of B1): n_{l+1} chosen ONE-step-predictably, i.e. on each
atom C' of G_l separately, among the candidates N' that satisfy (5.2), so as to maximise
E_{C'}[(c_{N'}Z0)^2]. The C2 bound with max_{N'} eps(N') is then expected to fail for single parents.
Usage: python3 t3_twowindow.py SEED NX MAXLIFT NEGLIFT"""
import sys, random
from fz_lib import *

seed, NX, MAXLIFT, NEGLIFT = map(int, sys.argv[1:5])
rng = random.Random(seed)
R = 60
S = dict(atoms=0, single=0, c2_fail=0, eq_fail=0, B_fail=0, Beq_fail=0, mart_fail=0, const_fail=0,
         eps_fail=0, subset=0, neg=0, neg_viol=0, neg_single=0, neg_single_viol=0)
ratios = []
NXNEG = max(2, NX // 3)


def lifts_profiles(r, m, p, K, T):
    out = []
    for w in range(p ** K):
        x1 = r + p ** m * w
        Z0, _ = dp_profile(x1, p, T)
        out.append((x1, Z0))
    return out


for p in (3, 5, 7):
    for rule, H in (('lin', p + 4), ('hash', p + 2), ('ladder', 2 * p)):
        n0 = 2 * p + rng.randrange(0, p); n1 = n0 + rng.randrange(2, p + 2)
        L = 3
        got = 0; tries = 0
        while got < NX and tries < 60 * NX:
            tries += 1
            X = rng.randrange(p ** R)
            if rng.random() < 0.3:
                k = rng.randrange(3, n1 + 3 * p); s = rng.randrange(1, 5)
                X = (-k + p ** s * rng.randrange(1, p ** 30)) % p ** R
            n, m = schedule(X, p, n0, n1, rule, H, L + 1)
            for l in range(1, L + 1):
                a, b, c = n[l - 1], n[l], n[l + 1]
                vl = vals(X, p, c); V, M = prefix(vl)
                if not cond52(V, M, a, b, c):
                    continue
                K = V[c] - V[a]; D = V[b] - V[a]
                if p ** K > MAXLIFT or K == 0:
                    continue
                mm = m[l - 1]; r = X % p ** mm
                assert mm == V[a]
                Zr, _ = dp_profile(r, p, a)
                if Zr[a] == 0:
                    continue
                prof = lifts_profiles(r, mm, p, K, c)
                ca, cb, cc = c_n(a, V[a], p), c_n(b, V[b], p), c_n(c, V[c], p)
                Mn = ca * Zr[a]
                E2b = sum((cb * Z[b]) ** 2 for _, Z in prof) / p ** K
                E2c = sum((cc * Z[c]) ** 2 for _, Z in prof) / p ** K
                E1b = sum(cb * Z[b] for _, Z in prof) / p ** K
                E1c = sum(cc * Z[c] for _, Z in prof) / p ** K
                eps = eps_coll(r, p, a, b, c)
                ch = chi2(r, p, a, b)
                lhs = E2c - E2b; rhs = eps * Mn ** 2
                S['atoms'] += 1; got += 1
                if lhs > rhs:
                    S['c2_fail'] += 1; print("FAIL C2", p, rule, X, l, n, lhs, rhs)
                if rhs > 0:
                    ratios.append(float(lhs / rhs))
                if E2b > (1 + ch) * Mn ** 2:
                    S['B_fail'] += 1; print("FAIL PropB", p, rule, X, l, n)
                if E1b != Mn or E1c != Mn:
                    S['mart_fail'] += 1; print("FAIL martingale", p, rule, X, l, n, E1b, E1c, Mn)
                if Zr[a] == 1:
                    S['single'] += 1
                    if lhs != rhs:
                        S['eq_fail'] += 1; print("FAIL C2 single-parent equality", p, rule, X, l, n, lhs, rhs)
                    if E2b != (1 + ch) * Mn ** 2:
                        S['Beq_fail'] += 1; print("FAIL PropB equality", p, rule, X, l, n)
                for x1, _ in prof[:: max(1, len(prof) // 7)]:
                    ny, _ = schedule(x1, p, n0, n1, rule, H, l)
                    if ny[:l + 2] != n[:l + 2]:
                        S['const_fail'] += 1; print("FAIL rule constancy on G_{l-1} atom", p, rule, X, l)
                ef = eps_fourier(r, p, a, b, c)
                if abs(ef - float(eps)) > 1e-9 * max(1, ef):
                    S['eps_fail'] += 1; print("FAIL eps fourier", p, X, l, eps, ef)
                # explicit parents: single parent (sharp equalities) and random parent subsets (inequality)
                try:
                    allp = [bt for bt, Sv, Sd in enum_alive(r, p, a, limit=20000) if Sd % p]
                except RuntimeError:
                    allp = []
                if allp:
                    chosen = [[rng.choice(allp)] for _ in range(2)]
                    if len(allp) >= 3:
                        chosen.append(rng.sample(allp, rng.randrange(2, min(5, len(allp)) + 1)))
                    for P in chosen:
                        Yb = [0] * p ** K; Yc = [0] * p ** K
                        for w in range(p ** K):
                            x1 = r + p ** mm * w
                            for bt in P:
                                z0, _ = dp_from_parent(x1, p, c, bt)
                                Yb[w] += z0[b]; Yc[w] += z0[c]
                        MP = ca * len(P)
                        e2b = sum((cb * y) ** 2 for y in Yb) / p ** K
                        e2c = sum((cc * y) ** 2 for y in Yc) / p ** K
                        e1b = sum(cb * y for y in Yb) / p ** K
                        e1c = sum(cc * y for y in Yc) / p ** K
                        lhsP = e2c - e2b; rhsP = eps * MP ** 2
                        if e1b != MP or e1c != MP:
                            S['mart_fail'] += 1; print("FAIL parent martingale", p, X, l, len(P))
                        if len(P) == 1:
                            S['single'] += 1
                            if lhsP != rhsP:
                                S['eq_fail'] += 1; print("FAIL single-parent C2 equality", p, rule, X, l, n, lhsP, rhsP)
                            if e2b != (1 + ch) * MP ** 2:
                                S['Beq_fail'] += 1; print("FAIL single-parent PropB equality", p, rule, X, l, n)
                        else:
                            S['subset'] += 1
                            if lhsP > rhsP:
                                S['c2_fail'] += 1; print("FAIL C2 subset", p, rule, X, l, n, lhsP, rhsP)
                            if e2b > (1 + ch) * MP ** 2:
                                S['B_fail'] += 1; print("FAIL PropB subset", p, rule, X, l, n)
        print(f"RESULT p={p} rule={rule} n0={n0} n1={n1}: {S}")

if ratios:
    ratios.sort()
    print(f"RESULT C2 slack lhs/rhs over {len(ratios)} atoms with eps>0: min {ratios[0]:.4f} median {ratios[len(ratios)//2]:.4f} max {ratios[-1]:.6f}")

# NEGATIVE CONTROL: one-step-predictable choice of n_{l+1}, single explicit parent
for p in (3, 5, 7):
    got = 0; tries = 0
    while got < NXNEG and tries < 400 * NXNEG:
        tries += 1
        X = rng.randrange(p ** R)
        a = 2 * p + rng.randrange(0, 2 * p)
        b = a + rng.randrange(2, p + 2)
        vl = vals(X, p, b + 3 * p); V, M = prefix(vl)
        cands0 = [c for c in range(b + 1, b + 3 * p) if cond52(V, M, a, b, c) and V[c] > V[b]]
        firstc = {}
        for c in cands0:
            firstc.setdefault(V[c], c)   # one candidate per distinct jump D'
        cands = sorted(firstc.values())
        if len(cands) < 2:
            continue
        cmax = max(cands)
        Kmax = V[cmax] - V[a]; D = V[b] - V[a]
        if p ** Kmax > NEGLIFT or D == 0:
            continue
        mm = V[a]; r = X % p ** mm
        try:
            allp = [bt for bt, Sv, Sd in enum_alive(r, p, a, limit=20000) if Sd % p]
        except RuntimeError:
            continue
        if not allp:
            continue
        bt = rng.choice(allp)
        ca, cb = c_n(a, V[a], p), c_n(b, V[b], p)
        Ys = []
        for w in range(p ** Kmax):
            z0, _ = dp_from_parent(r + p ** mm * w, p, cmax, bt)
            Ys.append(z0)
        E2b = sum((cb * z[b]) ** 2 for z in Ys) / p ** Kmax
        groups = {}
        for w, z in enumerate(Ys):
            groups.setdefault(w % p ** D, []).append(z)
        epsv = {c: eps_coll(r, p, a, b, c) for c in cands}
        adv = Fraction(0); fixed = {c: Fraction(0) for c in cands}
        adv2 = Fraction(0); avgeps2 = Fraction(0)
        for key, Zs in groups.items():
            vals_c = {}
            for c in cands:
                cc = c_n(c, V[c], p)
                vals_c[c] = sum((cc * z[c]) ** 2 for z in Zs) / len(Zs)
                fixed[c] += vals_c[c]
            adv += max(vals_c.values())
            # second adversary: maximise the excess over the realised bound eps(N') M^2
            cstar = max(cands, key=lambda c: vals_c[c] - epsv[c] * ca ** 2)
            adv2 += vals_c[cstar]; avgeps2 += epsv[cstar]
        adv /= len(groups); adv2 /= len(groups); avgeps2 /= len(groups)
        if adv2 - E2b > avgeps2 * ca ** 2:
            S['neg_single_viol'] += 1
        S['neg_single'] += 1
        # sanity: each FIXED candidate satisfies the single-parent equality
        for c in cands:
            if fixed[c] / len(groups) - E2b != epsv[c] * ca ** 2:
                S['eq_fail'] += 1; print("FAIL fixed-candidate equality", p, X, a, b, c)
        lhs = adv - E2b; rhs = max(epsv.values()) * ca ** 2
        got += 1; S['neg'] += 1
        if lhs > rhs:
            S['neg_viol'] += 1
            if S['neg_viol'] <= 3:
                print(f"  example p={p} x={X} n={a} N={b} candidates={cands}: adaptive increment {float(lhs):.6g} > max_eps*M^2 {float(rhs):.6g}")
    print(f"RESULT negative control p={p}: one-step-predictable N' (adversary A: maximise E[M^2]) exceeds max_cand eps * M^2 on {S['neg_viol']}/{S['neg']} single-parent atoms; adversary B (maximise excess) exceeds E[eps(N'(x))] * M^2 on {S['neg_single_viol']}/{S['neg_single']} (cumulative)")
print(f"SUMMARY t3 {S}")
