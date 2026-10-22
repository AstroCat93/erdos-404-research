"""t2_martingale.py -- the martingale step of Theorem B1 with ADAPTIVE window times:
on an atom A of G_l (class x mod p^{m_l}) where the window W_l = [n_l, n_{l+1}) satisfies
(W2'),(W3'), with n_{l+1} produced by a two-step-predictable rule, check EXACTLY
  (a) E_A[c_{n_{l+1}} Z0_{n_{l+1}}] = c_{n_l} Z0_{n_l}            (Cor A')
  (b) Prop A(i): no slope-0 path at n_{l+1} has a prefix of slope >= 1 at n_l, and every alive child
      of a slope-0 parent has slope 0;
  (c) the rule returns the same n_{l+1}, n_{l+2} at every lift (constancy on A);
  (d) Z0_{n_l} is constant on A.
Sensitivity: the same checks on windows that violate (W2') or (W3') (deterministic N, chosen too long).
NEGATIVE CONTROL: a 'peeking' choice N(x') in {N1,N2} made from digits finer than m_l (pointwise max of
c_N Z0_N) -- outside the hypothesis of B1 -- must break (a).
Usage: python3 t2_martingale.py SEED NX MAXLIFT"""
import sys, random
from fz_lib import *

seed, NX, MAXLIFT = map(int, sys.argv[1:4])
rng = random.Random(seed)
R = 60
S = dict(atoms=0, a_fail=0, b_fail=0, c_fail=0, d_fail=0, nonzero=0, cross_paths=0,
         out_atoms=0, out_a_fail=0, out_b_fail=0, peek=0, peek_up=0, peek_eq=0)


def check_atom(r, m, p, n, N, sched=None, tag=True):
    """returns (mean_ok, A(i)_ok, const_ok, Z0n, nlifts)"""
    vlr = vals(r, p, N); V, M = prefix(vlr)
    D = V[N] - V[n]
    Zr, _ = dp_profile(r, p, n)
    cn = c_n(n, V[n], p) * Zr[n]
    tot = Fraction(0)
    a_ok = True; c_ok = True; d_ok = True; crossp = 0
    for w in range(p ** D):
        x1 = r + p ** m * w
        Z0, Za, cr = dp_profile(x1, p, N, tag_at=n)
        vl1 = vals(x1, p, N); V1, _ = prefix(vl1)
        tot += c_n(N, V1[N], p) * Z0[N]
        if Z0[n] != Zr[n]:
            d_ok = False
        if cr.get((0, 1), 0) != 0 or cr.get((1, 0), 0) != 0:
            a_ok = False
        crossp += cr.get((1, 1), 0)
        if sched is not None:
            p_, n0, n1, rule, H, l, nref = sched
            ny, my = schedule(x1, p_, n0, n1, rule, H, l + 1)
            if ny[:l + 3] != nref[:l + 3]:
                c_ok = False
    mean = tot / p ** D
    return mean == cn, a_ok, c_ok, d_ok, Zr[n], cn, mean, crossp


for p in (3, 5, 7):
    for rule, H in (('lin', p + 4), ('ladder', 2 * p), ('hash', p + 2)):
        n0 = 2 * p + rng.randrange(0, p); n1 = n0 + rng.randrange(2, p + 1)
        L = 3
        cnt_rule = 0
        tries = 0
        while cnt_rule < NX and tries < 40 * NX:
            tries += 1
            X = rng.randrange(p ** R)
            if rng.random() < 0.3:  # edge cases: x near -k with k beyond n_0
                k = rng.randrange(3, n1 + 3 * p); s = rng.randrange(1, 5)
                X = (-k + p ** s * rng.randrange(1, p ** 30)) % p ** R
            n, m = schedule(X, p, n0, n1, rule, H, L + 1)
            for l in range(0, L + 1):
                N = n[l + 1]; nl = n[l]
                vl = vals(X, p, N); V, M = prefix(vl)
                D = V[N] - V[nl]
                if not condW(V, M, nl, N) or p ** D > MAXLIFT:
                    continue
                r = X % p ** m[l]
                Zr, _ = dp_profile(r, p, nl)
                if Zr[nl] == 0:
                    continue
                res = check_atom(r, m[l], p, nl, N, sched=(p, n0, n1, rule, H, l, n))
                S['atoms'] += 1; cnt_rule += 1
                S['nonzero'] += 1
                S['cross_paths'] += res[7]
                if not res[0]:
                    S['a_fail'] += 1; print("FAIL mean", p, rule, X, l, n, res[4:7])
                if not res[1]:
                    S['b_fail'] += 1; print("FAIL A(i)", p, rule, X, l, n)
                if not res[2]:
                    S['c_fail'] += 1; print("FAIL rule constancy", p, rule, X, l, n)
                if not res[3]:
                    S['d_fail'] += 1; print("FAIL Z0_n constancy", p, rule, X, l, n)
        print(f"RESULT p={p} rule={rule} n0={n0} n1={n1}: {S}")

# sensitivity of the A(i) check: (W3') violated by a gate of depth s >= m_l inside the window,
# tested pointwise at x (A(i) is a pointwise statement)
for p in (3, 5, 7):
    done = 0; tries = 0; bad = 0
    while done < 3 * NX and tries < 400 * NX:
        tries += 1
        n = 2 * p + rng.randrange(0, 2 * p)
        N = n + rng.randrange(2, 2 * p)
        k = rng.randrange(n + 1, N + 1)
        X0 = rng.randrange(p ** R)
        vl = vals(X0, p, n); V, M = prefix(vl)
        if (X0 + k) % p == 0:
            continue
        s = V[n] + rng.randrange(0, 3)
        # force v(X+k) = s while keeping X = X0 mod p^{V[n]+1}... (not needed: only v(X+i), i<=n, must stay)
        X = X0 - ((X0 + k) % p ** s) + p ** s * (1 + p * rng.randrange(p ** 20))
        if vp(X + k, p) != s or X < 0:
            continue
        vl = vals(X, p, N); V, M = prefix(vl)
        if M[N] < V[n] or V[n] > 12:
            continue
        Z0, _, cr = dp_profile(X, p, N, tag_at=n)
        if Z0[n] == 0:
            continue
        done += 1
        if cr.get((0, 1), 0) or cr.get((1, 0), 0):
            bad += 1
    S['out_atoms'] += done; S['out_b_fail'] += bad
    print(f"RESULT sensitivity p={p} (W3' violated by a gate of depth >= m inside the window): {done} points, A(i) violated at {bad}")

# negative control: peeking choice of N from finer digits
for p in (5, 7):
    done = 0; tries = 0
    while done < NX and tries < 400 * NX:
        tries += 1
        X = rng.randrange(p ** R)
        n = 2 * p + rng.randrange(0, 2 * p)
        vl = vals(X, p, n + 3 * p); V, M = prefix(vl)
        cands = [N for N in range(n + 1, n + 3 * p) if condW(V, M, n, N) and V[N] > V[n]]
        if len(cands) < 2:
            continue
        N1, N2 = cands[0], cands[-1]
        if V[N2] == V[N1] or p ** (V[N2] - V[n]) > MAXLIFT:
            continue
        mm = V[n]; r = X % p ** mm
        Zr, _ = dp_profile(r, p, n)
        if Zr[n] == 0:
            continue
        D2 = V[N2] - V[n]
        tot = Fraction(0)
        for w in range(p ** D2):
            x1 = r + p ** mm * w
            Z0, _ = dp_profile(x1, p, N2)
            v1 = c_n(N1, V[N1], p) * Z0[N1]; v2 = c_n(N2, V[N2], p) * Z0[N2]
            tot += max(v1, v2)
        mean = tot / p ** D2
        cn = c_n(n, V[n], p) * Zr[n]
        done += 1; S['peek'] += 1
        if mean > cn:
            S['peek_up'] += 1
        elif mean == cn:
            S['peek_eq'] += 1
        else:
            print("FAIL peek below", p, X, n, N1, N2, mean, cn)
    print(f"RESULT negative control (peeking rule) p={p}: {S['peek']} atoms, E[M_next] > M in {S['peek_up']}, equal in {S['peek_eq']}")
print(f"SUMMARY t2 {S}")
